# 11장. 보안과 Zero Trust — Access·Tunnel·WAF·Turnstile·Auth.js

VPC와 Security Group, NACL과 IAM 정책으로 그어둔 경계가 익숙한 우리에게 "경계가 없다"는 말은 처음에 끔찍하게 들린다. 우리는 사설망 안쪽을 안전한 거실, 바깥쪽을 위험한 길거리로 그려두는 데 익숙하다. EC2는 거실 안에 있어야 하고, ALB만이 길거리에 발을 내놓는다. 누군가 "EC2를 outbound-only로만 노출해 보세요"라고 말하면, 평생 IP 화이트리스트로 살아온 백엔드 개발자의 머릿속에서는 빨간불이 들어온다. 그게 Spring `SecurityFilterChain`을 한 줄씩 짜며 익혀온 직감이다.

그런데 잠시 멈춰 생각해 보자. 우리가 그어둔 그 경계는 정말 안전한 경계였던가? VPN을 한 번 뚫고 들어온 사용자는 그 안에서 어디든 갈 수 있었다. SG를 한 번 잘못 열면 RDS가 인터넷 전체에 노출됐다. 사내망 안쪽이라는 이유로 인증 없이 도는 어드민 페이지가 한두 개씩은 있었다. "안쪽이니까 안전하다"는 가정이 사실은 가장 무른 가정이었던 셈이다.

Zero Trust는 이 가정을 처음부터 거꾸로 뒤집는다. **경계로 신뢰를 만들지 말고, identity로 신뢰를 만들자.** 어떤 네트워크에서 들어오든, 사용자·디바이스가 누구인지·무엇인지를 매 요청마다 묻자. IP로 신뢰하는 게 아니라 사람으로 신뢰하자. 이 한 줄이 Cloudflare Access·Tunnel·WAF·Turnstile·API Shield가 한 묶음으로 엮이는 출발점이다.

이번 장에서는 IAM의 정교한 정책 언어를 잃은 자리에 무엇을 어떻게 다시 세울지, EC2 사설 서브넷을 외부에 노출하지 않고도 어떻게 Cloudflare로 안전하게 끌어올지, 그리고 일반 사용자 인증은 Auth.js·Lucia·Clerk·자체 JWT 중 무엇을 골라 얹을지를 차례로 살펴보자. 마지막엔 사내 Grafana를 한 번에 노출해보는 작은 워크스루로 손에 익히자.

### Spring SecurityContext에 익숙한 사람을 위한 다리

본격적인 도구 이야기로 들어가기 전, Spring 개발자가 머릿속에 들고 있는 그림 한 장을 먼저 옮겨두자. Spring Security를 한 번이라도 깊이 짜본 사람이라면 `SecurityFilterChain` → `AuthenticationManager` → `SecurityContextHolder`라는 흐름이 머리에 박혀 있을 것이다. 요청이 들어오면 필터 체인이 한 줄씩 검사하고, 인증이 끝난 사용자는 `Authentication` 객체로 컨텍스트에 박힌다. 이후 어디에서든 `@PreAuthorize`나 `SecurityContextHolder.getContext()`로 그 사용자를 꺼내 쓴다.

Cloudflare로 옮기면 이 흐름이 분해된다. `SecurityFilterChain`의 역할이 한 곳에 모이지 않고 여러 자리에 흩어진다 — Cloudflare 엣지에서 도는 WAF·Bot·Access 한 단, Worker 안에서 도는 Hono 미들웨어 한 단, 그리고 origin에서 한 번 더 검증하는 한 단. 처음엔 이 흩어짐이 어색하다. "한 곳에서 다 잡는 게 깔끔하지 않나?"라는 의심이 든다.

그렇지만 다시 생각해 보자. Spring의 한 곳 모음이 깔끔해 보였던 건 같은 JVM·같은 프로세스 안에서 도는 신뢰 모델이 깔려 있어서였다. 분산된 엣지·다중 PoP·여러 Worker가 한 도메인을 처리하는 그림에서는 한 곳에 모으는 게 오히려 위험하다. 엣지에서 거를 수 있는 건 엣지에서 거르고(거기서 막으면 origin이 안 부른다 = 비용·지연 절감), Worker가 봐야 할 건 Worker가 보고, origin이 신뢰의 마지막 보루로 한 번 더 검증한다. 같은 책임을 세 단에 나눠 두는 그림이다.

기억해두자 — Cloudflare 세계의 보안은 한 줄짜리 `SecurityFilterChain`이 아니라, **여러 단의 점진적 거름망**이다. 처음엔 흩어져 보이지만, 익숙해지면 각 단의 책임이 또렷해 디버깅이 쉬워진다.

## 경계 대신 identity — Cloudflare Access

먼저 Cloudflare Access부터 살펴보자. 한 줄로 줄이면 이렇다 — **모든 앱 앞단에 SSO 게이트를 한 겹 두는 도구.** AWS 세계에서 가까운 그림을 그린다면 IAM Identity Center + Verified Access의 조합이다. Verified Access는 ZTNA(Zero Trust Network Access)를 표방하며 네트워크 단의 VPN을 identity 기반으로 갈아치우는 제품이고, Identity Center는 SSO·사용자·그룹을 관리한다. Cloudflare Access는 이 두 자리를 한 제품에서 다룬다.

작동 그림은 간단하다. `admin.toby-shop.com` 같은 서브도메인 앞에 Access 정책을 건다. 사용자가 그 도메인을 열면, 자기 회사 SSO(Google Workspace·Okta·Azure AD·GitHub·OIDC·SAML 어떤 IdP든)로 로그인하라는 페이지가 먼저 뜬다. 로그인이 성공하면 Access가 짧은 수명의 JWT를 쿠키에 박아주고, 그 쿠키를 들고 들어오는 요청만 뒤쪽 origin에 도달한다. 이때 origin은 EC2일 수도, Workers일 수도, 사내 Jenkins일 수도 있다. Access는 그 앞에 무엇이 있든 신경 쓰지 않는다 — 자기 일은 사람이 누군지 묻는 것뿐이다.

여기까지 보면 "그게 뭐 대단한가, ALB + Cognito로도 비슷하게 한다"고 말할 수 있다. 그런데 한 꺼풀 더 들어가 보면 차이가 보인다.

첫째, **device posture**다. 회사 노트북에만 발급된 디바이스 인증서가 있는 기기, OS가 최신 패치된 기기, 디스크 암호화가 켜진 기기에서만 들어오게 하는 정책을 한 줄로 건다. AWS Verified Access도 비슷한 그림을 그릴 수 있지만 설정의 무게가 다르다. Cloudflare Access에서는 Zero Trust 대시보드에서 체크박스 몇 개로 끝난다.

둘째, **앱 단위 정책**이다. IAM처럼 service·resource·action을 거대한 정책 문서로 묶지 않고, 한 도메인·한 경로마다 "이 그룹의 사람들만 들어올 수 있다"라고 끊어 표현한다. 정책 언어로서의 표현력은 IAM보다 좁지만, 실무에서 실제로 쓰는 패턴 — 어드민 페이지는 admin 그룹만, 스테이징은 dev 그룹만, 외부 협력사는 vendor 그룹만 — 을 한눈에 짜기엔 오히려 가볍다.

셋째, **브라우저 기반 SSH·VNC·RDP**다. Access 뒤쪽의 EC2에 SSH를 붙는데, 클라이언트는 그냥 브라우저 한 장이다. SSH 키를 노트북마다 뿌리고 관리하던 절차가, "Access로 로그인하면 브라우저 안에서 터미널이 열린다"로 바뀐다. 처음 보면 "이게 진짜 보안이 되나?" 싶지만, 실제로는 SSH 키 분실·노트북 도난 같은 사고를 한 단계 줄여준다. Cloudflare가 사용자별로 짧은 수명 인증서를 자동 발급해 EC2 OpenSSH에 꽂는 구조라, 키가 사용자 손에 영구히 남지 않는다.

기억해두자. Cloudflare Access의 본질은 한 줄이다 — **모든 트래픽 앞에 identity 한 겹을 둔다.** IP 화이트리스트를 더 정교하게 만드는 게 아니라, 아예 IP 자체를 신뢰의 기준으로 쓰지 않는 그림이다.

### IAM의 빈자리, 어떻게 다시 채울까

Spring 세계에서 `SecurityFilterChain`은 모든 요청 앞단에서 인증·인가를 잡아준다. AWS 세계에서는 IAM이 그 자리에 있다. Cloudflare로 넘어오면 그 정교한 정책 언어가 한 번에 사라진 자리에 약간의 공허함이 남는다. "그래서 Worker A는 R2 bucket B에 어떤 권한으로 닿는 거지?" 같은 질문이 생긴다.

답은 세 줄로 갈라진다.

- **Worker ↔ 리소스 권한**은 `wrangler.toml`의 Bindings로 표현한다. Worker가 어떤 KV·D1·R2·Queue·DO에 닿을 수 있는지가 코드 옆에 선언으로 박힌다. IAM role의 Resource·Action을 Bindings 한 줄이 흡수한 셈이다. 정책 문서가 아니라 코드 옆 설정 파일이라 짧고 또렷하다.
- **사람·디바이스 ↔ 앱 권한**은 Cloudflare Access 정책으로 표현한다. 이쪽은 IAM Identity Center + Verified Access의 자리.
- **외부 클라이언트 ↔ API 권한**은 WAF 룰·API Shield·mTLS로 표현한다. IAM의 service-to-service 권한 영역.

세 자리가 한 제품으로 묶이지 않는다는 게 처음엔 흩어져 보인다. 그렇지만 다시 생각해 보면, IAM도 사실 한 제품이라기보다 여러 컨셉을 한 정책 언어 아래 묶어둔 것이었다. Cloudflare는 그 묶음을 풀어 컨셉별로 다른 도구에 나눠 담은 셈이다. 익숙해지면 각자의 책임이 명확해 디버깅이 오히려 쉬워진다.

## Cloudflare Tunnel — outbound-only로 사설망 끌어오기

이제 EC2 이야기를 해보자. 10장에서 우리는 RDS를 publicly accessible로 두고 SG에 Cloudflare egress IP를 화이트리스트했다. 동작은 한다. 그런데 찜찜하다. RDS가 인터넷에 노출돼 있다는 사실 자체가 보안팀의 잠을 줄인다.

다른 길은 없을까? 있다. **Cloudflare Tunnel**이다. 이름이 생경하지만, 동작은 단순하다. 사설망 안쪽 어딘가에 `cloudflared`라는 작은 데몬을 한 대 띄운다. 이 데몬은 사설망 안쪽에서 Cloudflare 엣지로 outbound 연결을 연다 — 들어오는 포트는 하나도 열지 않는다. Cloudflare는 그 outbound 연결을 잡아두고, 외부에서 들어오는 요청을 그 연결을 타고 사설망 안쪽으로 흘려보낸다.

이걸 그림으로 보면 한 줄이다.

```
[외부 사용자] → [Cloudflare 엣지] ↘
                                  ↓ (outbound-only tunnel)
                        [사설망 안쪽 cloudflared] → [RDS / EC2 서비스]
```

사설망 입장에서는 inbound 포트가 0개다. SG는 0/0에 대해 인바운드를 모두 닫아도 된다. 외부에서 RDS로 직접 닿는 길은 없다. 그런데도 Cloudflare 엣지에서 들어오는 정당한 요청은 사설망 안쪽 RDS로 이어진다. AWS 세계의 Site-to-Site VPN이나 PrivateLink가 풀어주던 문제를, outbound-only 모델로 더 가볍게 푼 셈이다.

처음 들으면 "outbound가 양방향으로 동작하나?" 싶다. 그렇다 — TCP를 outbound로 한 번 열어두면 그 위로 양방향 데이터가 흐른다. WebSocket이나 SSH의 reverse port forwarding을 쓴 사람이라면 익숙한 그림이다. Cloudflare Tunnel은 이 패턴을 production-grade로 다듬어 둔 것이다.

### 손가락으로 한 번 띄워 보자

말로만 풀면 멀리 있는 이야기 같다. 손가락을 움직여 보자. EC2 한 대에서 사내 Grafana(`localhost:3000`)를 외부에 노출하는 시나리오를 가정한다.

```bash
# EC2 안에서, cloudflared 설치 (Amazon Linux 기준)
curl -L --output cloudflared.rpm \
  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm
sudo rpm -ivh cloudflared.rpm

# Cloudflare 계정에 로그인 (브라우저로 OAuth)
cloudflared tunnel login

# 새 터널 만들기
cloudflared tunnel create toby-grafana
# → Tunnel 이름과 ID, credentials 파일 경로 출력

# 터널을 도메인에 매핑
cloudflared tunnel route dns toby-grafana grafana.toby-shop.com

# config.yml 작성
cat > ~/.cloudflared/config.yml <<'YAML'
tunnel: toby-grafana
credentials-file: /home/ec2-user/.cloudflared/<UUID>.json
ingress:
  - hostname: grafana.toby-shop.com
    service: http://localhost:3000
  - service: http_status:404
YAML

# systemd 서비스로 띄우기
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

이 한 사이클이면 EC2 SG에서 80·443·3000 어떤 포트도 열지 않은 채로, `https://grafana.toby-shop.com`이 외부에서 동작한다. cloudflared가 EC2 안쪽에서 Cloudflare 엣지로 outbound 연결을 유지하고, Cloudflare가 그 연결을 타고 사용자 요청을 흘려보낸다.

이 자리에 Cloudflare Access를 한 줄 더 얹으면 — 그러니까 같은 도메인에 Access 정책을 걸면 — Grafana 앞에 SSO 게이트가 자동으로 끼어든다. Google Workspace 로그인을 통과한 사람만 Grafana로 들어가고, 들어가는 즉시 Grafana는 자기 인증 없이도 사용자가 누군지 헤더로 받을 수 있다 (`Cf-Access-Authenticated-User-Email` 같은 헤더). 사내 어드민 도구의 인증을 Access로 한 곳에 모아두면, Grafana·Jenkins·Argo·Kibana 어떤 도구든 자기 SSO 통합을 따로 하지 않아도 된다.

기억해두자 — `cloudflared`는 **데몬**이다. EC2가 죽으면 그 EC2의 터널도 같이 죽는다. Production에서는 한 터널을 여러 cloudflared replica가 함께 들고 있게 띄워야 한다 (같은 터널 ID를 여러 EC2에 띄우면 자동으로 부하 분산이 된다). 이건 ALB의 가용성을 직접 짊어지는 그림과 비슷하다 — 가볍지만 운영자의 책임이 늘어난 셈이다.

## WAF·Bot Management·Turnstile — 한 묶음으로 보자

Tunnel과 Access가 "들여보낼 사람"을 다룬다면, WAF·Bot Management·Turnstile은 "들이지 말아야 할 트래픽"을 다룬다. 이쪽은 Cloudflare 보안 스택의 가장 익숙한 얼굴 — DDoS 막아주는 그 회사라는 인상의 출처다.

세 도구가 어떻게 다른지부터 풀어보자.

**WAF**는 OWASP Top 10 같은 잘 알려진 공격 패턴을 룰셋으로 잡아준다. SQL injection, XSS, RCE 시도를 패턴 매칭으로 거른다. Cloudflare는 Managed Ruleset(Cloudflare가 직접 관리)·OWASP Ruleset·Custom Rule 세 단을 제공한다. 우리가 직접 룰을 짠다면 Custom Rule 쪽이다 — "특정 경로로 들어오는 PUT 요청은 차단하라" 같은 식으로 표현 언어를 써서 한 줄씩 쌓는다.

**Bot Management**는 패턴 매칭이 아닌 **신호 기반**이다. JA3 fingerprint, TLS 특성, 요청 간격, behavior pattern 등 수십 가지 신호를 모아 사람·legitimate bot·악성 bot을 구분해 점수로 매긴다. 점수가 임계치 아래면 차단·challenge·로그만 남기고 통과 같은 행동을 룰로 건다. 이 영역은 머신러닝 기반이라 우리가 룰을 직접 짜기보다는 점수를 활용해 정책을 쓰는 쪽이다.

**Turnstile**은 클라이언트 사이드의 신호를 한 번 더 잡는 위젯이다. CAPTCHA를 대체하는 자리에 들어간다. 흥미로운 점은 — 일반 사용자에게는 **invisible challenge**라 UI가 거의 보이지 않는다는 것이다. 봇 의심이 강한 경우에만 사용자에게 한 번 클릭을 요청하거나 추가 검증을 한다. reCAPTCHA에 길들여진 사용자에게는 거의 마찰이 없다. 회원가입·로그인·비밀번호 재설정 같은 form 앞에 자주 얹는다.

세 도구를 한 묶음으로 보면 이렇다. WAF는 알려진 패턴, Bot Management는 행동 신호, Turnstile은 클라이언트 신호. 같은 적을 세 각도에서 보는 셈이다. Cloudflare 공식 가이드는 셋을 함께 쓰는 통합 패턴을 권한다 — 통과시킬지 막을지 결정할 때 세 점수를 함께 본다.

### Workers에서 Turnstile 한 줄 검증

Turnstile 위젯을 form에 붙이면 클라이언트는 토큰 한 장을 받는다. 이 토큰을 서버가 한 번 검증해야 의미가 있다. Workers에서는 한 줄짜리 fetch면 끝난다.

```ts
import { Hono } from "hono";

const app = new Hono<{ Bindings: { TURNSTILE_SECRET: string } }>();

app.post("/signup", async (c) => {
  const body = await c.req.parseBody();
  const token = body["cf-turnstile-response"] as string;

  const verify = await fetch(
    "https://challenges.cloudflare.com/turnstile/v0/siteverify",
    {
      method: "POST",
      body: new URLSearchParams({
        secret: c.env.TURNSTILE_SECRET,
        response: token,
        remoteip: c.req.header("CF-Connecting-IP") ?? "",
      }),
    },
  );
  const result = (await verify.json()) as { success: boolean };

  if (!result.success) {
    return c.json({ error: "verification failed" }, 403);
  }

  // 정상 회원가입 흐름...
  return c.json({ ok: true });
});

export default app;
```

`CF-Connecting-IP` 헤더는 Cloudflare가 자동으로 박아주는 진짜 클라이언트 IP다. ALB의 `X-Forwarded-For`와 비슷한 자리지만, Cloudflare 엣지가 위변조를 막아준다는 점이 다르다. 기억해두자 — `X-Forwarded-For`는 우리가 한 번 더 검증해야 할 헤더고, `CF-Connecting-IP`는 신뢰해도 되는 헤더다.

## mTLS와 API Shield — B2B API의 정직한 신뢰

지금까지의 도구는 사용자·브라우저를 다뤘다. 그렇다면 서버 ↔ 서버는 어떤가? 우리 API를 외부 회사 시스템이 호출한다면? IP 화이트리스트로 막던 그 자리는 Cloudflare에서 무엇으로 채울까?

답은 **mTLS**다. 클라이언트도 서버도 서로의 인증서를 검증하는 양방향 TLS. 한쪽 방향만 인증하던 보통 HTTPS와 달리, 서버도 클라이언트가 가진 인증서를 검증해 "이 클라이언트는 우리가 사전에 발급한 인증서를 가진 신뢰 가능한 상대다"를 확인한다.

Cloudflare에서 이걸 거는 자리가 **API Shield**다. API Shield는 mTLS 외에도 schema validation(우리 OpenAPI 명세에 안 맞는 요청을 거르는 것)·sequence rules(API 호출 순서가 정상인지 검증)·sensitive data detection 같은 도구를 묶어 둔다. 외부 파트너에게 API를 여는 자리, 모바일 앱이 우리 백엔드에 붙는 자리, 내부 서비스 간 통신을 한 단 더 단단히 묶는 자리에서 쓴다.

설정의 큰 틀은 이렇다. Cloudflare에 우리 자체 CA를 등록하고, 그 CA로 클라이언트 인증서를 발급해 파트너에게 준다. Cloudflare 룰에서 "이 도메인·이 경로로 들어오는 요청은 우리 CA로 발급된 클라이언트 인증서가 있어야 통과시킨다"를 한 줄 건다. 통과한 요청에는 인증서 정보가 헤더로 박혀 origin에 전달된다. origin Worker는 그 헤더로 "어느 파트너의 요청인가"를 확인한다.

기억해두자 — mTLS는 사용자 인증이 아니라 **클라이언트 시스템 인증**이다. 사람을 식별하지 않는다. B2B API·모바일 앱·내부 서비스 간처럼 클라이언트가 시스템인 자리에서 쓴다. 사람 인증과는 결이 다르다는 점을 흐리지 말자.

### 사례 — 공개 API에 mTLS·WAF·Turnstile 한 줄로

`toby-shop`이 외부 파트너에게 주문 조회 API를 열었다고 해보자. 요구사항은 셋이다 — 파트너 시스템 외에는 못 부르게, 알려진 공격 패턴은 엣지에서 거르게, 사람 흉내 내는 봇은 별도 신호로 한 번 더 잡게.

세 도구를 차곡차곡 쌓아 본다.

**1단 — WAF 룰 한 줄.** `partners.toby-shop.com/orders`로 들어오는 요청은 GET·POST만 허용하고, body에 SQL injection·XSS 패턴이 보이면 차단. Cloudflare Managed Ruleset과 OWASP Ruleset을 켜고, Custom Rule 한 줄을 더 얹는다 — "이 경로의 PUT·DELETE 요청은 무조건 block".

**2단 — API Shield mTLS.** 파트너 회사마다 우리 CA로 발급한 클라이언트 인증서를 한 장씩 준다. Cloudflare 룰에 "이 도메인으로 들어오는 요청은 우리 CA 인증서가 있어야 통과"를 한 줄 건다. 인증서 없는 요청은 엣지에서 403으로 끊긴다 — origin Worker는 이 요청을 보지도 못한다.

**3단 — Turnstile은 form 위에만.** 이 API는 시스템 ↔ 시스템이라 Turnstile은 안 붙인다. 다만 같은 도메인의 파트너 셀프서비스 화면(예: 신규 파트너 가입 form, API key 발급 화면) 앞에는 Turnstile을 한 줄 얹는다. 사람의 form 제출과 봇의 form 제출을 구분하는 자리다.

origin Worker는 이렇게 짤 수 있다.

```ts
import { Hono } from "hono";

const app = new Hono();

app.use("/orders/*", async (c, next) => {
  // mTLS로 검증된 클라이언트 인증서 정보가 헤더로 박혀 있다
  const certHeader = c.req.header("Cf-Client-Cert-Spki");
  const partnerId = c.req.header("Cf-Client-Cert-Subject-DN");

  if (!certHeader || !partnerId) {
    return c.json({ error: "client cert required" }, 401);
  }

  // 파트너별 권한 분기
  c.set("partnerId", partnerId);
  await next();
});

app.get("/orders/:id", async (c) => {
  const partnerId = c.get("partnerId");
  // partnerId 기반으로 그 파트너가 볼 수 있는 주문만 반환
  return c.json({ id: c.req.param("id"), partnerId });
});

export default app;
```

`Cf-Client-Cert-*` 헤더는 Cloudflare가 mTLS 검증 후 박아주는 헤더다. origin은 이 헤더를 신뢰해 파트너를 식별한다. 단 — origin이 Cloudflare를 거치지 않은 요청을 받지 않게 막는 건 우리 책임이다 (origin SG에서 Cloudflare IP만 허용하거나, origin이 들어오는 토큰을 한 번 더 검증). 안 그러면 누군가 origin 직접 IP를 알아내 헤더를 위조해 들어올 수 있다.

이 세 단을 함께 켜두면, 파트너 API의 보안은 거의 자동이 된다. 우리가 직접 짜는 건 partner-별 권한 로직 한 줄뿐이다. ALB + WAF + Lambda Authorizer + Cognito + KMS의 조합으로 같은 그림을 그리려고 했던 사람이라면, 이 단순함이 살짝 어이없게 느껴질 수 있다. 그게 정상이다.

## Workers + Auth.js·Lucia·Clerk — 일반 사용자 인증

이제 화제를 바꿔 일반 사용자 회원가입·소셜 로그인·세션 관리로 넘어가 보자. 이쪽은 Access의 영역이 아니라 — Access는 SSO 게이트로 앱 앞단에 두는 것 — 우리 앱 안쪽에서 Auth.js·Lucia·Clerk·자체 구현으로 직접 짜는 영역이다.

네 갈래를 비교해 보자.

**Auth.js (NextAuth)** — Next.js 생태계에서 가장 무난한 선택. OAuth provider 50개 이상이 기본으로 들어 있고, OpenNext on Cloudflare 환경에서도 잘 돈다. session storage를 D1 또는 KV에 둘 수 있다. Drizzle 어댑터까지 짝으로 쓰면 7장에서 그렸던 D1 + Drizzle 그림과 자연스럽게 이어진다.

**Lucia** — Workers·Edge에 친화적인 minimal auth 라이브러리. "magic" 적은 코드로 명시적인 흐름을 짠다. Auth.js가 너무 큰 추상으로 느껴지는 사람, refresh token rotation·session invalidation 같은 동작을 손에 쥐고 짜고 싶은 사람에게 잘 맞는다. DB는 D1 또는 Hyperdrive 너머의 Postgres 어디든.

**Clerk** — SaaS형 인증 서비스. 회원가입·로그인·MFA·비밀번호 재설정·이메일 확인 같은 모든 흐름을 Clerk에 위임한다. UI 컴포넌트도 함께 제공된다. 도입 속도가 가장 빠르지만, 사용자 수에 비례해 비용이 든다. MVP·짧은 사이클로 출시해야 하는 자리에서 쓸 만하다.

**자체 구현 (Hono + JWT + KV)** — 가장 가벼운 길. Hono 미들웨어 한 줄로 JWT 검증, KV에 세션 저장, OAuth 콜백은 직접 짜기. 의존성이 적고 코드를 손에 쥐고 있다는 안도감이 있다. 다만 refresh token rotation, session revoke, OAuth 50개 provider 호환 같은 디테일을 모두 직접 책임진다.

어떤 걸 고를까? 정답은 없지만 가이드는 이렇다.

- 새 SaaS · MVP · 짧은 사이클이라면 **Clerk**
- Next.js 위에 평범한 소셜 로그인이라면 **Auth.js**
- Workers 단독 · 코드 정밀 제어가 필요하면 **Lucia**
- 인증 흐름이 단순하고 의존성을 줄이고 싶으면 **Hono + JWT + KV**

5장의 결정 프레임 표현으로 옮기면 — Clerk은 "Move now·운영 부담 최소", Auth.js는 "표준 패턴 그대로", Lucia는 "edge-native 가벼움", 자체는 "lock-in 회피"가 각각의 sweet spot이다.

### Auth.js + D1 + Workers — 코드 한 토막

가장 흔한 그림인 Auth.js + D1 + Google 로그인을 코드로 그려 보자. OpenNext 위가 아니라 순수 Workers + Hono 환경이다.

```ts
// src/auth.ts — Auth.js v5 코어 설정
import { Auth } from "@auth/core";
import Google from "@auth/core/providers/google";
import { D1Adapter } from "@auth/d1-adapter";

type Env = {
  AUTH_SECRET: string;
  GOOGLE_CLIENT_ID: string;
  GOOGLE_CLIENT_SECRET: string;
  DB: D1Database;
};

export function authHandler(req: Request, env: Env) {
  return Auth(req, {
    adapter: D1Adapter(env.DB),
    secret: env.AUTH_SECRET,
    providers: [
      Google({
        clientId: env.GOOGLE_CLIENT_ID,
        clientSecret: env.GOOGLE_CLIENT_SECRET,
      }),
    ],
    session: { strategy: "database" },
    trustHost: true,
  });
}
```

Hono 라우터에 붙이는 자리는 한 줄이다.

```ts
// src/index.ts
import { Hono } from "hono";
import { authHandler } from "./auth";

const app = new Hono<{ Bindings: Env }>();

// /auth/* 모든 요청을 Auth.js에 위임 — signin, callback, signout, session 등
app.all("/auth/*", (c) => authHandler(c.req.raw, c.env));

// 보호된 라우트 — 세션이 없으면 401
app.get("/me", async (c) => {
  const sessionRes = await fetch(
    new URL("/auth/session", c.req.url),
    { headers: c.req.raw.headers },
  );
  const session = (await sessionRes.json()) as { user?: { email: string } };
  if (!session.user) return c.json({ error: "unauthenticated" }, 401);
  return c.json({ email: session.user.email });
});

export default app;
```

`wrangler.toml`에는 D1 바인딩과 secret 세 개를 적어준다.

```toml
name = "toby-shop-auth"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[d1_databases]]
binding = "DB"
database_name = "toby-shop"
database_id = "your-d1-id"

# AUTH_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET은
# wrangler secret put 으로 등록
```

```bash
wrangler secret put AUTH_SECRET
wrangler secret put GOOGLE_CLIENT_ID
wrangler secret put GOOGLE_CLIENT_SECRET
```

이 한 사이클이면 Google 소셜 로그인이 동작한다. 사용자가 `/auth/signin/google`로 들어가면 Google OAuth로 보내지고, 콜백이 돌아오면 Auth.js가 D1에 사용자·계정·세션을 기록한다. 세션은 쿠키로 클라이언트에 박히고, 우리는 `/auth/session` 엔드포인트로 현재 세션을 언제든 조회할 수 있다.

세션을 KV에 두고 싶다면 `D1Adapter` 자리에 KV 어댑터로 바꾸면 된다. 7장에서 본 KV vs D1 결정과 결이 같다 — 세션은 read-heavy + eventually consistent로 충분하니 KV가 잘 맞는 자리다. 다만 Auth.js의 표준 KV 어댑터는 별도 패키지를 골라야 하고, 일부는 커뮤니티 메인테인이다. 시작은 D1 어댑터로 안정적으로, 트래픽이 늘면 세션만 KV로 분리하는 흐름이 무난하다.

### KV 세션의 일관성 — 60초의 의미

KV에 세션을 둘 때 한 번 짚어둘 게 있다. KV는 eventually consistent이고 전파에 최대 60초가 걸린다. 사용자가 로그아웃을 누르고 KV의 세션 키를 지웠다고 해도, 다른 PoP에서는 잠깐 옛 세션이 보일 수 있다는 뜻이다. 이게 무엇을 의미하는지 두 갈래로 정리하자.

**보통 로그인·로그아웃 흐름에서는 문제 없다.** 사용자가 한 PoP에서 로그인하고, 같은 사용자가 같은 디바이스로 같은 PoP 근처에서 다시 들어오는 게 보통이다. 같은 PoP의 KV는 즉시 일관된다. 글로벌 전파 60초가 보이는 자리는 다른 PoP에서 들어오는 매우 드문 케이스다.

**중요한 보안 이벤트에서는 한 단 더.** 비밀번호 변경 직후·다른 디바이스 강제 로그아웃·세션 revoke 같은 자리에서는 KV의 60초 전파가 위험할 수 있다. 이 자리에는 D1에 "revoked sessions" 테이블 한 장을 두고, 미들웨어가 세션 검증 시 D1을 한 번 더 보게 짠다. read는 D1로 한 번 더 가지만, security-critical 동작은 즉시 일관성을 보장한다. KV의 빠름과 D1의 일관성을 한 자리에 섞는 패턴이다.

기억해두자 — KV·D1·DO 중 어느 한 도구로 세션을 다 풀려고 하지 말자. 세션의 read와 revoke는 일관성 요구가 다르다. **빠른 read는 KV, 즉시 revoke는 D1**으로 갈라두는 편이 낫다.

### 사례 — Workers + Auth.js로 Google 로그인 + KV 세션 한 사이클

위 그림을 그대로 손가락에 옮겨 보자. `toby-shop` 사용자가 Google로 로그인하고, 세션은 KV에서 빠르게 읽고, 로그아웃은 D1의 revocation 테이블에 한 줄을 박아 즉시 무효화하는 그림이다.

```ts
// src/middleware/session.ts
import type { MiddlewareHandler } from "hono";

type Env = {
  SESSIONS: KVNamespace;
  DB: D1Database;
};

export const sessionMiddleware: MiddlewareHandler<{ Bindings: Env }> = async (
  c,
  next,
) => {
  const sessionToken = c.req.header("Cookie")
    ?.match(/session=([^;]+)/)?.[1];

  if (!sessionToken) {
    c.set("user", null);
    return next();
  }

  // 1단 — KV에서 세션 읽기 (빠름, eventually consistent)
  const session = await c.env.SESSIONS.get(sessionToken, "json") as
    | { userId: string; email: string; expiresAt: number }
    | null;

  if (!session || session.expiresAt < Date.now()) {
    c.set("user", null);
    return next();
  }

  // 2단 — D1에서 revoke 여부 확인 (강한 일관성)
  const revoked = await c.env.DB.prepare(
    "SELECT 1 FROM revoked_sessions WHERE token = ? LIMIT 1",
  )
    .bind(sessionToken)
    .first();

  if (revoked) {
    // KV에서도 지워둔다 (eventual cleanup)
    c.executionCtx.waitUntil(c.env.SESSIONS.delete(sessionToken));
    c.set("user", null);
    return next();
  }

  c.set("user", { id: session.userId, email: session.email });
  await next();
};
```

로그인 콜백 자리는 Auth.js에 위임하되, 세션 발급 후 KV에 한 줄 박는 hook을 한 단 추가한다.

```ts
// src/auth.ts (events hook)
events: {
  signIn: async ({ user, env }) => {
    const token = crypto.randomUUID();
    const expiresAt = Date.now() + 30 * 24 * 60 * 60 * 1000; // 30일
    await env.SESSIONS.put(
      token,
      JSON.stringify({ userId: user.id, email: user.email, expiresAt }),
      { expirationTtl: 30 * 24 * 60 * 60 },
    );
    // 쿠키 박는 자리는 Auth.js 또는 직접 Set-Cookie로
  },
  signOut: async ({ token, env }) => {
    // KV에서도 지우고, D1에도 revocation 박기
    await env.SESSIONS.delete(token);
    await env.DB.prepare(
      "INSERT INTO revoked_sessions (token, revoked_at) VALUES (?, ?)",
    )
      .bind(token, Date.now())
      .run();
  },
},
```

이 한 사이클이면 사용자 로그인 흐름은 KV의 빠름을, 로그아웃·revoke는 D1의 강한 일관성을 함께 누린다. Spring 개발자의 익숙한 그림으로 옮기면 — Spring Session + Redis(빠른 세션) + DB(audit log) 조합과 비슷한 자리에 있다. 다만 우리는 두 도구가 한 wrangler.toml 안에 바인딩으로 묶여 있어 운영의 무게가 가볍다.

여기에 11장 앞부분의 도구를 한 줄씩 더 얹어 보자. 로그인 form 앞에는 Turnstile 한 단(브루트포스 봇 차단), 회원가입에는 WAF rate limit 한 단(같은 IP에서 분당 10회 이상 가입 시도 차단), 그리고 어드민 페이지는 Access 한 단으로 한 번 더 막는다. 그러면 사용자 인증 한 묶음이 — Cloudflare 엣지의 WAF·Turnstile·Access · Worker 안의 Hono 미들웨어 · KV·D1의 데이터 단 — 세 층으로 쌓이고, 각 층의 책임이 또렷이 갈라진다. Spring `SecurityFilterChain` 한 줄에 모든 걸 모으던 그림과는 결이 다르지만, 분산 환경에서는 이 갈라짐이 더 안정적이다.

## 사례 — 사내 Grafana를 한 번에 노출

이번 장의 도구들을 한 그림으로 묶어 보자. `toby-shop` 운영팀이 사내 Grafana를 외부에서 쓰고 싶어 한다. 요구사항은 셋이다.

1. EC2의 어떤 포트도 외부에 열지 말 것
2. 회사 Google Workspace 계정으로만 들어갈 수 있을 것
3. 회사 발급 노트북에서만 들어갈 수 있을 것

전통적인 AWS 패턴이라면 — VPN 한 번 깔고, ALB에 Cognito Authorizer 붙이고, 회사 노트북 인증을 Cognito 위에 또 한 겹 짜는 — 이 세 줄을 풀어내는 데 며칠이 걸린다. Cloudflare 한 묶음으로는 한나절이면 된다. 절차를 그려 보자.

**1단계 — Cloudflare Tunnel로 EC2 노출.** EC2에 cloudflared 데몬을 띄우고 `localhost:3000`(Grafana)을 `grafana.toby-shop.com`에 매핑한다. 앞서 본 명령어 그대로다. 이 시점에 EC2의 SG는 inbound 0/0을 모두 닫아도 된다.

**2단계 — Cloudflare Access 정책 부착.** Zero Trust 대시보드에서 `grafana.toby-shop.com`에 Access 애플리케이션을 만든다. Identity provider는 Google Workspace로 추가하고 (OIDC client ID·secret 한 번 입력), 정책은 "이메일 도메인이 `@toby-shop.com`인 사용자만 통과"로 한 줄 건다.

**3단계 — Device posture 추가.** 같은 정책에 device posture 조건을 한 줄 더 건다 — "디바이스 인증서가 발급된 노트북만 통과". 회사가 발급한 노트북에는 mTLS 클라이언트 인증서를 미리 깔아 두는 식이다. 또는 더 단순한 길로, WARP 클라이언트가 동작 중이고 회사 zone에 enroll된 디바이스만 통과로 잡을 수도 있다.

**4단계 — Grafana 인증 위임.** Grafana는 자기 인증 화면을 끄고, Access가 박아 주는 `Cf-Access-Authenticated-User-Email` 헤더를 신뢰해 사용자를 식별하도록 설정한다 (Grafana의 `auth.proxy` 모드). Access의 JWT signature를 한 번 더 검증하면 더 안전하다 — Cloudflare 공식 JWKS endpoint에서 키를 받아 Grafana가 직접 검증할 수 있다.

이 네 단계로 끝이다. 결과 — 외부에서 `grafana.toby-shop.com`을 열면 회사 Google 로그인 → device posture 검사 → Access JWT 발급 → Grafana 도착이라는 흐름이 자동으로 돈다. EC2의 어떤 포트도 외부에 열지 않은 채로. SG는 깨끗하고, 보안팀은 잠을 더 잔다.

같은 패턴으로 Jenkins·Argo·Kibana·내부 어드민 페이지를 한 도메인씩 더해 가면 된다. `cloudflared` config의 `ingress` 항목에 한 줄씩 늘리고, Access 애플리케이션에 한 개씩 등록하기. SSO 통합을 도구마다 따로 짜던 세계와는 무게가 다르다.

## 무너지는 자리 — Zero Trust도 만능은 아니다

이 책이 광고서가 아닌 이상 한 번 더 정직하게 짚고 가자. 위에서 푼 그림들이 어디서 무너지는가.

**Access는 enterprise IdP에 깊이 의존한다.** Google Workspace·Okta·Azure AD 같은 IdP가 살아 있어야 동작한다. IdP가 죽으면 Access 뒤의 모든 앱이 같이 죽는다. 회사가 IdP 한 곳에 묶이는 셈이라, IdP 자체의 가용성이 critical path가 된다. 이건 AWS Identity Center에 묶이는 그림과 비슷한 무게다 — 단일 의존을 받아들이는 결단이 필요하다.

**Tunnel은 cloudflared 데몬의 운영 부담을 새로 만든다.** ALB가 알아서 풀어주던 가용성·헬스체크·로깅을 우리가 cloudflared replica로 짊어진다. 한 EC2에만 cloudflared를 띄우면 그 EC2가 죽는 순간 터널이 끊긴다. Production에서는 최소 두 대 이상에 같은 터널 ID로 cloudflared를 띄워야 하고, 그 데몬의 헬스·로그·버전 업그레이드를 운영 절차에 포함해야 한다. 무료라고 해서 운영비가 0인 건 아니다.

**Bot Management와 Turnstile은 일부 정교한 봇을 못 잡는다.** 사람이 쓰는 도구를 흉내 내거나, residential proxy를 거쳐 사람처럼 행동하는 봇은 점수가 사람 가까이 나온다. 결제 abuse·credential stuffing 같은 자리에서는 Cloudflare 한 단에 모두 맡기지 말고, 우리 application logic에 rate limit·abuse detection 한 단을 더 넣는 편이 낫다. "Cloudflare가 막아줄 거야"라는 가정은 위험하다.

**mTLS는 인증서 운영의 책임을 가져온다.** 발급·rotation·revocation을 우리가 직접 짊어진다. 한 파트너의 인증서가 만료되면 그 순간 그 파트너의 통신이 끊긴다. 만료 알림과 자동 rotation 절차를 미리 깔아두지 않으면, 6개월 뒤 새벽 알림이 울린다. 끔찍한 일이다.

**IAM의 정교한 정책 언어는 정말 등가물이 없다.** 우리가 IAM의 condition·NotAction·resource ARN 패턴 같은 정밀한 표현에 익숙하다면, Cloudflare의 Bindings + Access policy + WAF rule 조합은 처음에 거칠게 느껴질 수 있다. 표현력의 한계다. 정교한 권한 그래프를 그리는 자리는 Cloudflare 단독이 어렵다 — 외부 IAM 시스템(Okta·Auth0·OPA·자체 권한 서비스)을 한 단 더 두는 편이 낫다.

**Access의 JWT 검증을 origin에서 안 하면 우회 위험이 있다.** Cloudflare 엣지를 거치지 않고 origin에 직접 닿는 경로가 한 줄이라도 있다면 — 누군가 origin IP를 알아내거나, DNS를 우회한다면 — Access가 무용지물이 된다. origin이 들어오는 JWT를 직접 검증하거나, origin이 Cloudflare 엣지에서 온 트래픽만 받도록 mTLS·Cloudflare-only IP 화이트리스트를 origin SG에 한 단 더 두는 게 안전하다.

이 한계들이 도구를 못 쓰게 만드는 건 아니다. 다만 "Cloudflare 켰으니 안전하다"는 단순한 가정으로 잠을 너무 깊이 자지는 말자는 이야기다. Zero Trust의 핵심은 "어디서도 신뢰를 가정하지 말 것" 아닌가. 도구 자체에도 그 원칙을 적용해 보자.

## 마무리

이번 장에서 우리는 IAM·Cognito·Verified Access·Site-to-Site VPN의 자리를 Cloudflare One 스택이 어떻게 다시 채우는지 살펴봤다. 핵심은 한 줄이다 — **경계가 아니라 identity로 신뢰를 만든다.** Access는 사람·디바이스를 매 요청마다 묻고, Tunnel은 사설망을 outbound-only로 끌어오며, WAF·Bot Management·Turnstile은 들이지 말아야 할 트래픽을 세 각도에서 거른다. mTLS와 API Shield는 시스템 ↔ 시스템 신뢰를, Auth.js·Lucia·Clerk·자체 JWT는 일반 사용자 인증을 채운다.

10장의 Hyperdrive와 자연스럽게 짝을 이룬다는 점도 다시 짚어두자. 10장에서 우리는 RDS를 publicly accessible로 두는 그림을 그렸지만, 그게 찜찜하다면 11장의 Cloudflare Tunnel로 사설망 안쪽에서 outbound-only로 RDS를 노출할 수 있다. 두 장을 함께 읽으면, "DB는 AWS, 컴퓨트는 Cloudflare" 하이브리드 패턴이 보안 측면에서도 닫힌 그림이 된다.

기억해두자. Zero Trust는 도구가 아니라 멘탈 모델이다. Access·Tunnel·WAF·Turnstile·mTLS는 그 멘탈을 구현하는 도구일 뿐, 도구를 켜는 것만으로 Zero Trust가 완성되지는 않는다. "어디서도 신뢰를 가정하지 말 것"이라는 한 줄을 우리 시스템 곳곳에 적용해 보자 — 그게 이번 장의 진짜 약속이다.

다음 장에서는 시야를 또 한 번 넓혀, AI·Workflows·Queues·Cron Triggers로 비동기·orchestration·스케줄·LLM 영역을 살펴보자. Step Functions와 SQS, `@Scheduled`와 Bedrock의 빈자리에 Cloudflare가 무엇을 어떻게 들여놓는지가 다음 페이지에서 펼쳐진다.
