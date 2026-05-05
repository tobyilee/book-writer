# 3장. 첫 Worker를 띄우자 — Mac에서 5분 만에 글로벌 배포

월요일 아침이라고 해보자. 커피 한 잔을 옆에 두고 빈 디렉토리 하나를 새로 열었다. 2장에서 V8 isolate 이야기를 한참 듣고 나서, 머릿속에는 "그래서 이게 정말 5ms 안에 뜬다고?"라는 의심이 한 줄 남았다. 표를 아무리 들여다봐도 손에 잡히지 않는다. 그 의심을 풀 길은 하나뿐이다. **직접 한 번 띄워보는 것이다.**

이번 장의 약속은 단순하다. Mac에서 명령어 몇 줄로 `Hello, edge`라고 답하는 Worker 한 개를 도쿄·LA·런던 PoP에 동시에 올린다. 그 다음 `wrangler tail`로 로그가 떨어지는 광경을 본다. 처음부터 끝까지 다해도 5분 남짓이다. 길어야 10분. 한번 함께 해보자.

## 도구 준비 — Homebrew로 Node와 pnpm만

먼저 도구다. 익숙한 도구일수록 가볍게 가는 편이 낫다. 우리에게 필요한 건 셋뿐이다. **Node 22 이상, pnpm, 그리고 Wrangler.** 이 중 Node와 pnpm은 Homebrew로 한 번에 깐다.

```bash
brew install node@22 pnpm
node --version   # v22.x.x
pnpm --version   # 9.x 이상
```

여기서 한 가지 함정이 있다. Wrangler 자체도 Homebrew에 비슷한 이름의 패키지가 있는데, 그건 비공식이다. Cloudflare 공식 문서가 권장하는 방법은 **프로젝트 단위로 pnpm devDependency에 넣는 것**이다. 글로벌 설치(`npm i -g wrangler`)도 가능하긴 한데, 프로젝트마다 다른 버전을 요구할 때 머리가 아파진다. 어떤 프로젝트는 wrangler 3.x를 요구하고 어떤 프로젝트는 4.x를 쓰는데, 글로벌은 한 버전밖에 없다. 난감해진다. 그래서 처음부터 프로젝트 안에 가두는 편이 깔끔하다.

```bash
# 글로벌 설치 — 권장하지 않는다
npm i -g wrangler

# 프로젝트 단위 설치 — 권장
pnpm add -D wrangler@latest
```

왜 이렇게 강조하느냐. 이건 단순한 취향 문제가 아니다. Cloudflare Workers는 빠르게 변하는 플랫폼이다. wrangler 버전마다 지원하는 바인딩, 명령어 옵션, `wrangler.toml` 필드가 바뀐다. 팀에서 한 명은 4.10에서 동작하는데 다른 한 명은 3.80에 머물러 있다면, 같은 `pnpm dev` 명령에 대해 결과가 달라진다. CI에서는 또 다른 버전이 돈다. 이쯤 되면 디버깅이 아니라 점성술이 된다. 끔찍한 일이다.

프로젝트의 lockfile에 wrangler 버전이 박혀 있으면 이 모든 혼란이 사라진다. `pnpm install` 한 번이면 모든 환경에서 같은 버전이 깔린다. 그러니 처음부터 그렇게 가자.

## `wrangler login` — OAuth 한 번이면 끝

도구가 깔렸으면 Cloudflare 계정과 묶어야 한다. AWS의 IAM access key를 처음 만들 때의 그 의식 — `aws configure`, access key 입력, region 입력, 출력 포맷 입력 — 같은 게 있을 것 같지만 없다. Cloudflare는 OAuth 흐름이다.

```bash
pnpm dlx wrangler login
```

명령을 치면 브라우저가 열리고 Cloudflare 대시보드 로그인 페이지로 간다. 이미 로그인되어 있으면 권한 승인 화면이 뜬다. "Allow"를 누르면 끝이다. 터미널에 다시 돌아오면 `Successfully logged in.`이라는 한 줄이 떨어져 있다. AWS의 access key·secret key 페어를 어디에 둘지 고민하는 시간보다 짧다.

토큰은 어디에 저장될까. 홈 디렉토리의 Wrangler 설정 폴더에 들어간다. macOS에서는 대체로 `~/.config/.wrangler/` 또는 `~/.wrangler/config/` 경로에 OAuth 토큰이 저장된다(버전에 따라 위치가 살짝 달라진다). 토큰을 직접 들여다볼 일은 거의 없지만, "이 토큰이 어디 있는지 모르고 쓰는 건 찜찜하다"는 마음이 든다면 한 번 확인해보자.

```bash
ls ~/.config/.wrangler/ 2>/dev/null || ls ~/.wrangler/config/ 2>/dev/null
```

CI에서는 OAuth가 안 통한다. 대신 `CLOUDFLARE_API_TOKEN` 환경변수를 쓴다. 대시보드 → My Profile → API Tokens에서 `Edit Cloudflare Workers` 템플릿으로 토큰을 발급받아 GitHub Actions의 secret에 넣어두면 된다. 로컬은 OAuth, CI는 API token — 이 분리를 처음부터 머릿속에 박아두자. 나중에 권한 문제로 헤매는 시간이 줄어든다.

## 첫 프로젝트 — `pnpm create cloudflare`

이제 본론이다. 빈 디렉토리에서 시작하는 게 아니라, Cloudflare가 제공하는 템플릿 생성기로 한 번에 셋업하자. AWS의 `sam init`이나 `cdk init`과 비슷하지만 훨씬 가볍다.

```bash
pnpm create cloudflare@latest hello-edge
```

또는 npm을 더 좋아한다면 같은 일을 하는 명령이 있다.

```bash
npm create cloudflare@latest hello-edge
```

명령을 치면 인터랙티브 프롬프트가 줄줄이 나온다. 하나씩 보자.

- **What would you like to start with?** → `Hello World example`을 고르자. 가장 단순한 시작점이다. Hono 같은 프레임워크 템플릿도 있지만, 그건 6장에서 다룬다. 지금은 빈 캔버스가 낫다.
- **Which template would you like to use?** → `Worker only`. Static Assets·Workers + Pages 같은 옵션은 9장에서 다룬다.
- **Which language do you want to use?** → `TypeScript`. 이 책은 TS로 간다.
- **Do you want to use git for version control?** → `Yes`.
- **Do you want to deploy your application?** → 일단 `No`. 코드를 한 번 들여다본 다음 손으로 배포하는 편이 감을 잡기에 낫다.

생성이 끝나면 `hello-edge/` 디렉토리가 만들어져 있다. 들어가서 구조를 살펴보자.

```bash
cd hello-edge
ls
```

대체로 이런 모습이다.

```
hello-edge/
├── node_modules/
├── src/
│   └── index.ts
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── wrangler.jsonc        # 또는 wrangler.toml
└── worker-configuration.d.ts
```

`src/index.ts`를 열어보면 정말 단순하다.

```ts
export default {
  async fetch(request, env, ctx): Promise<Response> {
    return new Response('Hello World!');
  },
} satisfies ExportedHandler<Env>;
```

이 한 덩어리가 Worker의 본질이다. Lambda 핸들러처럼 보이지만 입력이 다르다. `request`는 Web Fetch API의 `Request` 객체 그대로다. `env`는 Bindings(나중에 KV·D1·R2가 들어올 자리). `ctx`는 `waitUntil`·`passThroughOnException` 같은 실행 컨텍스트. **AWS SDK가 끼어들 자리가 없다.** 표준 Web API와 Bindings 두 가지로 모든 것이 끝난다. 이게 2장에서 말한 "리전이 사라진 자리에 Bindings가 들어선다"의 첫 인상이다.

`wrangler.jsonc`도 한 번 보자.

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "hello-edge",
  "main": "src/index.ts",
  "compatibility_date": "2025-04-01",
  "observability": {
    "enabled": true
  }
}
```

세 줄이 핵심이다. `name`은 Worker 식별자이자 `<name>.<account>.workers.dev` URL의 일부가 된다. `main`은 엔트리 파일. `compatibility_date`는 2장에서 다룬 그 좌표계 — 이 날짜의 런타임 동작으로 고정된다는 뜻이다. Lambda runtime 버전과 비슷하지만 더 세밀하다. `observability.enabled`는 대시보드의 Logs 탭에서 실시간 로그를 볼 수 있게 해주는 스위치다. 켜둔 채로 가자.

## "Hello, edge"로 한 줄 고치기

기본 템플릿이 `Hello World!`라고 답하는데, 이건 너무 평범하다. 우리가 *edge*에서 도는 코드라는 걸 직접 느끼려면 이 자리에 어디서 응답이 떨어졌는지 표시해주는 게 낫다. Cloudflare는 매 요청에 어느 PoP에서 응답했는지를 `request.cf.colo` 같은 메타데이터로 담아준다. 이걸 응답 본문에 같이 넣어보자.

`src/index.ts`를 이렇게 고친다.

```ts
export default {
  async fetch(request, env, ctx): Promise<Response> {
    const colo = (request.cf as any)?.colo ?? 'unknown';
    const country = (request.cf as any)?.country ?? 'unknown';
    return new Response(
      `Hello, edge! served from ${colo} (${country})\n`,
      { headers: { 'content-type': 'text/plain; charset=utf-8' } }
    );
  },
} satisfies ExportedHandler<Env>;
```

`request.cf`는 Workers 런타임이 끼워주는 메타데이터 묶음이다. `colo`는 응답을 처리한 데이터센터의 IATA 공항 코드(예: `NRT`는 도쿄 나리타, `LAX`는 LA, `LHR`은 런던 히드로). `country`는 사용자의 국가 코드. 이 한 줄이 글로벌 배포의 첫 증거가 된다.

## `wrangler dev` — 로컬에서 production을 그대로

배포에 앞서 로컬에서 한 번 띄워보자.

```bash
pnpm dev
```

`package.json`의 `dev` 스크립트가 `wrangler dev`를 부른다. 잠시 기다리면 이런 화면이 뜬다.

```
⛅️ wrangler 4.x.x
-------------------
Your worker has access to the following bindings:
- (none)
[wrangler:info] Ready on http://localhost:8787
```

브라우저에서 `http://localhost:8787`을 열거나, 다른 터미널에서 `curl`을 날려보자.

```bash
curl http://localhost:8787
# Hello, edge! served from unknown (unknown)
```

응답이 떨어진다. 그런데 `colo`와 `country`가 `unknown`으로 나온다. 왜일까? **로컬 모드에서는 Cloudflare edge가 끼어주는 메타데이터가 없기 때문이다.** `wrangler dev`는 기본적으로 `workerd`라는 production과 같은 V8 런타임을 우리 Mac에 띄워서 isolate를 시뮬레이션한다. 정확한 isolate 동작은 그대로 재현하지만, "어느 PoP에서 도는가" 같은 글로벌 메타데이터는 진짜 PoP에서만 채워진다.

이 메타데이터까지 보고 싶다면 `--remote` 플래그를 쓰면 된다.

```bash
pnpm dlx wrangler dev --remote
```

이렇게 하면 코드는 우리 Mac에서 편집하지만 실행은 Cloudflare edge에서 일어난다. 로컬에서 시뮬레이션이 어려운 일부 기능(특정 Zone 기능, 일부 cf 메타데이터)을 테스트할 때 유용하다. 다만 매번 edge로 왕복하므로 핫 리로드 속도가 느리다. 평소에는 로컬 모드, 가끔 검증할 때 `--remote` — 이렇게 두 모드를 오가는 편이 낫다.

자, 이제 마음에 든다. 배포해보자.

## `wrangler deploy` — 한 줄로 글로벌 배포

```bash
pnpm dlx wrangler deploy
```

또는 `package.json`에 `deploy` 스크립트가 잡혀 있으면 `pnpm deploy`로도 된다. 명령을 치면 이런 출력이 줄줄이 떨어진다.

```
Total Upload: 0.42 KiB / gzip: 0.30 KiB
Worker Startup Time: 4 ms
Uploaded hello-edge (1.85 sec)
Deployed hello-edge triggers (0.81 sec)
  https://hello-edge.<your-account>.workers.dev
Current Version ID: 01234567-89ab-...
```

**2초 남짓이다.** 이 한 줄에 충분히 음미할 거리가 있다. `Worker Startup Time: 4 ms` — 우리 Worker의 콜드스타트가 4ms라는 뜻이다. Lambda에서 JVM 띄우는 데 보통 2~3초 걸리던 그 시간을 떠올려보자. SnapStart로 줄여도 100ms 단위였다. Workers는 그 자리에서 단순히 한 자릿수다. 그리고 `Deployed hello-edge triggers` — 이 한 줄이 떨어진 순간, 우리 코드는 이미 330개 넘는 PoP에 동시 배포되어 있다. CDN의 invalidation을 기다릴 필요가 없다. 이건 가장자리 얘기가 아니라 본체 얘기다.

URL을 받아 브라우저에서 열거나 `curl`을 한 번 쳐보자.

```bash
curl https://hello-edge.<your-account>.workers.dev
# Hello, edge! served from ICN (KR)
```

서울에서 응답이 떨어졌다(ICN은 인천공항 코드). 한국에서 접속했으니 가장 가까운 PoP가 골랐다. 이게 edge-first의 첫 손맛이다.

## 도쿄·LA·런던에서 정말로 도는지 확인하기

같은 Worker가 다른 대륙에서도 잘 도는지 직접 검증해보자. 가장 단순한 방법은 응답 헤더의 `cf-ray`를 보는 것이다. `cf-ray`는 매 요청에 Cloudflare가 붙이는 식별자인데, 끝부분 세 글자가 응답한 PoP의 공항 코드다.

```bash
curl -v https://hello-edge.<your-account>.workers.dev 2>&1 | grep -i cf-ray
# < cf-ray: 8a1b2c3d4e5f6789-ICN
```

여기서는 `ICN`이 떨어졌다. 우리 머신이 한국이니 당연하다. 그렇다면 다른 나라에서 들어오는 척하려면 어떻게 할까? 가장 손쉬운 길은 외부 검증 도구를 쓰는 것이다.

- **무료 글로벌 ping/HTTP 체크 서비스**(검색하면 여럿 있다)에 우리 워커 URL을 넣어보면, 도쿄·LA·런던·시드니에서 실제로 호출했을 때의 응답 시간과 헤더를 보여준다.
- 또는 VPN을 일본·미국·유럽 끝점으로 바꿔가며 같은 `curl`을 반복해도 된다.

실측이 번거롭다면 응답 본문에 우리가 넣어둔 `colo`만 봐도 충분하다. 일본 VPN으로 들어오면 `NRT` 또는 `KIX`(오사카), 미국 서부 VPN이면 `LAX` 또는 `SFO`, 영국이면 `LHR`이 떨어진다. **같은 코드, 같은 URL, 다른 PoP.** AWS에서 같은 일을 하려면 us-east-1, ap-northeast-1, eu-west-1 세 군데에 Lambda를 따로 배포하고 Route 53 latency-based routing을 걸어야 한다. 시간으로 따지면 한나절이다. Workers는 한 줄로 끝났다.

## `wrangler tail`로 실시간 로그 보기

배포가 됐으니 운영 감각도 한 번 잡자. CloudWatch Logs에 익숙한 사람이라면 "그래서 로그는 어디서 보지?"가 다음 의문일 것이다. 로컬에서는 `wrangler dev`의 콘솔에 그대로 떨어졌다. 배포된 Worker의 로그는 어떻게 볼까?

가장 손쉬운 방법은 `wrangler tail`이다.

```bash
pnpm dlx wrangler tail hello-edge
```

명령을 치면 그 자리에서 스트리밍이 시작된다. 다른 터미널에서 `curl`을 몇 번 던져보자.

```bash
curl https://hello-edge.<your-account>.workers.dev
curl https://hello-edge.<your-account>.workers.dev
```

`tail` 쪽 터미널에 요청 한 건씩 떨어지는 광경이 뜬다. 응답 코드, URL, `colo`, `country`까지. `console.log`를 코드에 넣어두면 그 출력도 그대로 따라온다. CloudWatch에 5~10초 지연으로 도착하는 로그를 기다리던 시간을 생각하면, 이건 거의 즉각이다.

```ts
console.log('request received', { colo, country, path: new URL(request.url).pathname });
```

이 한 줄을 넣고 다시 배포하면(`pnpm dlx wrangler deploy`), `wrangler tail`에 구조화된 로그가 떨어진다. 디버깅의 첫 도구다.

물론 `tail`은 사람이 보는 도구다. 운영 환경에서는 로그를 어딘가에 영속시켜야 한다. 그건 13장 운영 챕터에서 Workers Logpush로 R2·외부 APM에 보내는 패턴을 다룬다. 지금은 "실시간으로 일단 보인다"는 감각만 챙기자.

대시보드에서도 같은 일을 할 수 있다. Cloudflare 대시보드 → Workers & Pages → `hello-edge` → Logs 탭에 들어가면 `wrangler tail`과 같은 스트림이 브라우저에서 흐른다. 그 옆 Metrics 탭에서는 요청 수, CPU time, error rate, 응답 시간 분포가 시각화된다. CloudWatch의 통합 대시보드에 비하면 단출하지만, **첫 운영 감각을 잡는 데는 충분하다**. 더 깊은 관측은 외부 APM(Sentry·Baselime·Axiom·Datadog)으로 보내는 패턴이 표준이다 — 이것도 13장에서 다룬다.

## 이 기술이 무너지는 자리

처음 배포까지 한 사이클을 도는 동안 모든 게 매끄럽게 흘러갔다면, 그건 운이 좋았던 거다. 실제로는 다음 다섯 자리에서 자주 발이 걸린다. 미리 알아두자.

**첫째, `workers.dev` 도메인은 검색 엔진에서 페널티를 받는다.** `<name>.<account>.workers.dev`로 영원히 살 생각은 하지 말자. 개발·테스트용으로는 더없이 편하지만, 일반 사용자에게 노출하는 production URL이라면 custom domain을 붙여야 한다. Cloudflare에 도메인을 옮겨두었다면 대시보드에서 Routes 또는 Custom Domain을 한 번 눌러주면 끝이다. DNS 전파가 보통 몇 분 안에 끝나지만, 가끔 30분 넘게 걸리는 경우가 있어 답답할 수 있다. 찜찜하다면 `dig` 또는 `nslookup`으로 확인하면서 가자. workers.dev에 production 트래픽을 그대로 두는 건 나중에 SEO 문제를 한 번 만나야 깨닫는 종류의 실수다. 처음부터 피하는 편이 낫다.

**둘째, 무료 plan의 일일 한도는 100,000 요청이다.** Workers Free에는 100k req/일·CPU 10ms/요청 한도가 있다. 친구들 몇 명이 호기심에 눌러보는 정도라면 차고 넘치지만, 한 번 입소문을 타거나 봇이 무차별 호출하면 하루 안에 한도에 도달한다. 한도를 넘으면 그 날의 나머지 요청은 1015 에러로 거절된다. production에 가까워졌다면 Workers Paid($5/월)로 올라가자. 1천만 요청까지 포함이고 추가 사용량은 100만 req당 $0.30이다. 이쯤 가격이면 EC2 t3.nano 한 대 값이다. 망설일 자리가 아니다.

**셋째, npm 패키지 중 Node API 깊이 의존하는 것은 V8 isolate에서 안 돈다.** `node:fs`로 파일 시스템에 쓰는 라이브러리, `child_process`로 외부 프로세스 부르는 라이브러리, native binding을 가진 라이브러리(Sharp, bcrypt 같은) — 이런 건 그대로 못 쓴다. 일부 Node API는 `compatibility_flags`에 `nodejs_compat`을 켜면 동작한다. `wrangler.jsonc`에 한 줄 추가하면 된다.

```jsonc
{
  "compatibility_flags": ["nodejs_compat"]
}
```

이렇게 켜두면 `node:buffer`, `node:crypto`, `node:url`, `node:stream` 같은 자주 쓰는 모듈이 polyfill로 들어온다. 그래도 `node:fs`처럼 디스크 I/O를 요구하는 모듈은 여전히 안 된다. 이건 polyfill로 해결할 일이 아니라 isolate 모델 자체의 경계다. 기존 Node 백엔드를 그대로 옮기려고 하면 이 자리에서 발이 걸린다. 어떤 의존성이 안 도는지 미리 한 번 점검하는 편이 낫다(2장의 "Workers에서 절대 못 하는 것 7가지" 점검표가 그 자리다).

**넷째, route 충돌이다.** 같은 zone에 여러 Worker가 있고 route가 겹치면, Cloudflare는 가장 구체적인 패턴 하나만 활성화한다. `*.example.com/*`에 Worker A가 잡혀 있는데 `api.example.com/*`에 Worker B를 새로 잡으면, `api.example.com`의 트래픽은 B로 간다. 익숙해지기 전에는 "왜 이 요청이 저 Worker로 가지?"라며 30분 동안 디버깅하게 된다. 대시보드의 Routes 탭에서 현재 활성 route 목록을 한눈에 볼 수 있으니, 새 Worker를 붙이기 전에 한 번 들여다보자.

**다섯째, `compatibility_date`를 그대로 두면 새 기능이 안 들어온다.** 템플릿이 만들어 준 날짜는 그 시점의 런타임 동작으로 고정된다. 6개월 뒤 Cloudflare가 멋진 새 API를 발표해도, 우리 Worker의 `compatibility_date`가 옛날 그대로면 새 API가 안 보인다. 고치는 건 한 줄이지만, 한 번 올리고 나면 동작 변화가 있을 수 있으니 staging에서 한 번 돌리고 가는 편이 낫다. 분기마다 한 번씩 날짜를 갱신하는 습관을 들이자. 광고가 아니라 실무 권유다.

이 다섯 자리만 넘기면, 첫 배포부터 실서비스로 가는 길이 꽤 매끄럽다.

## 정리 — 손끝의 성취가 머리의 혼란을 진정시킨다

1장에서 우리는 "Cloudflare는 또 하나의 클라우드가 아니다"라는 말 한 줄을 받았다. 2장에서는 V8 isolate·리전 부재·Bindings·Compatibility Date라는 새 좌표계를 머리로 한 번 그려봤다. 표를 봐도 그림이 도식적이고, 손에 잡히지 않았을 것이다.

이 장에서 우리는 그 좌표계 위에 첫 점을 찍었다. **Mac에서 wrangler를 깔고, 한 줄짜리 코드를 짜고, 한 명령으로 글로벌 배포까지.** 5분 안에 한 사이클이 돌았다. 도쿄·LA·런던에서 같은 응답이 떨어지는 광경을 직접 봤고, `wrangler tail`에 로그가 즉시 흐르는 감각을 손에 쥐었다. 머리의 혼란이 한 번 진정됐다면, 이 챕터의 일은 다 한 셈이다.

다음 4장에서는 이 감각 위에 지도를 펼친다. Lambda·S3·DynamoDB·CloudFront·Step Functions — AWS의 익숙한 이름들이 Cloudflare의 어느 자리에 어떻게 자리 잡는지 카탈로그를 본격적으로 그려본다. 동시에 1:1 매핑이 거짓말이 되는 다섯 가지 패턴도 미리 표시해둔다. 4장이 지도라면, 5장은 그 지도 위에서 "그래서 내 워크로드 중 무엇을 옮길 것인가"의 결정 도구가 된다. 그 두 장이 지나면, 6장부터는 본격 실무다.

**지금 이 순간 우리 손에는 워커 도메인 하나가 있다.** `https://hello-edge.<account>.workers.dev`. 이 작은 한 줄짜리 Worker가 누적 실습 프로젝트 `toby-shop`의 시드다. 6장에서 라우팅·미들웨어·인증이 붙고, 7장에서 D1과 Drizzle이 들어오고, 12장에서는 결제 후 영수증 Workflow와 RAG 챗봇까지 얹는다. 한 줄에서 시작해 한 권의 책 분량으로 자라간다. 그 첫 줄을 우리 손으로 깐 것이다. 자, 다음 장으로 넘어가보자.
