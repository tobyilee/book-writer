# 9장. 분산 시스템의 보안 — 인증·인가·secret·망분리

팀 슬랙에 누군가 깃허브 public repo에 `.env`를 푸시했다는 알림이 떴다고 해보자. 그 파일 안에는 AWS access key가 통째로 들어 있다. 5분 안에 누군가 그 키로 EC2를 켜고 비트코인을 채굴한다. 청구서는 다음 날 아침에 도착한다 — 만 달러 단위로.

이런 일이 흔할까? 사실 매우 흔하다. GitHub에는 매일 수천 개의 secret이 실수로 push된다. 자동 봇이 GitHub의 공개 push를 실시간으로 스캔해, 노출된 AWS key·GCP service account·Stripe key를 분 단위로 채굴한다. **secret을 코드에서 분리하지 않은 한 줄의 게으름이 회사를 흔든다.**

보안은 production의 가장 약한 고리고, 우리가 매일 만지는 영역이다. 그런데도 한국 시스템 디자인 책 대부분이 보안을 "별도 책의 주제"로 미루거나 한 페이지로 처리한다. 분산 환경의 위협 모델, 인증·인가의 표준 패턴, secret 관리, 한국 망분리 환경, Zero Trust — 빌딩 블록의 일부로 한 박자씩 짚어 가자. 마지막엔 모든 새 endpoint 설계 시 자동으로 던질 5가지 질문을 손에 챙겨 두자.

## 분산 환경 위협 모델 — 3축으로 가르기

분산 시스템의 보안을 다룰 때 가장 먼저 그릴 그림이 위협 모델이다. 누가 누구에게 "나는 X다"라고 증명해야 하는지를 명확히 가르는 작업. 크게 세 축이 있다.

**1. Service-to-service (내부).** 우리 service A가 service B를 호출한다. A는 B에게 "나는 우리 회사의 신뢰받는 service"임을 증명해야 한다. mTLS, SPIFFE, service mesh가 이 영역.

**2. User-to-service (외부).** 사용자가 우리 API를 호출한다. 사용자는 우리에게 "나는 user 12345"임을 증명해야 한다. OAuth2/OIDC, JWT, session token이 이 영역.

**3. Admin-to-system (운영).** 운영자가 인프라에 접근한다. 운영자는 인프라에게 "나는 인증된 staff이고, 이 권한이 있다"를 증명해야 한다. SSO, MFA, JIT(Just-In-Time) access가 이 영역.

이 세 축의 신뢰 경계와 공격 표면이 모두 다르다. 그래서 한 가지 도구로 해결되지 않는다. 예를 들어 OAuth2는 (2)에는 표준이지만 (1)·(3)에는 부적합. mTLS는 (1)에는 표준이지만 (2)에는 사용자 경험 측면에서 거의 안 쓴다.

| 축 | 신뢰 경계 | 표준 도구 | 공격 표면 |
|----|---------|----------|---------|
| Service-to-service | 회사 내부 망 | mTLS, SPIFFE, service mesh | network sniff, lateral movement |
| User-to-service | 인터넷 ↔ API | OAuth2, JWT, session token | credential theft, replay, CSRF |
| Admin-to-system | staff ↔ 인프라 | SSO, MFA, JIT, audit log | insider threat, key leak |

각 축마다 다른 도구가 들어간다는 사실을 머릿속에 그려 두자. 보안 도입 시 첫 질문은 "어느 축의 위협이 우리에게 critical한가"이다.

## 인증·인가 두 단계 구분 — Authentication vs Authorization

용어부터 정리하자. 비슷한 발음 때문에 자주 혼동된다.

- **Authentication (AuthN, 인증):** "나는 누구다"를 증명. ID/password, OAuth login.
- **Authorization (AuthZ, 인가):** "나는 이걸 할 권한이 있다"를 증명. RBAC, ABAC, scope.

이 두 단계는 별개로 처리되는 편이 낫다. 인증은 한 번만 (login 시점), 인가는 매 요청마다 검증.

### OAuth2/OIDC 표준 흐름

웹·모바일 인증의 사실상 표준이 OAuth2 (RFC 6749)와 그 위의 OpenID Connect다. 흐름 4가지를 짧게 정리하자.

**1. Authorization Code Grant + PKCE (권장).** 가장 안전한 흐름. 모바일·SPA에 사용. PKCE(Proof Key for Code Exchange)는 authorization code 탈취 공격을 막는다.

```
1. User → Authorization Server: "log in" + PKCE challenge
2. Authorization Server → User: "이 client에 이 권한 줄까?"
3. User → Authorization Server: "yes"
4. Authorization Server → Client: authorization code
5. Client → Token Server: code + PKCE verifier
6. Token Server → Client: access_token + refresh_token
```

**2. Client Credentials.** Service-to-service에 사용. user 없음, client_id + client_secret으로 직접 token 받음.

**3. Implicit (Deprecated).** SPA에서 한때 쓰였으나 보안 위험으로 사실상 폐기. Authorization Code + PKCE로 대체.

**4. Resource Owner Password Credentials (Deprecated).** username + password를 client가 받음. 매우 위험. legacy migration용으로만 한정.

새 시스템이라면 **무조건 Authorization Code + PKCE**가 답이다. 다른 흐름은 legacy 호환 또는 service-to-service(Client Credentials)로 한정.

### JWT — 검증·만료·rotation

OAuth2의 access_token은 보통 **JWT** (JSON Web Token, RFC 7519) 포맷이다. 다음과 같이 생겼다.

```
header.payload.signature

eyJhbGciOiJIUzI1NiJ9.
eyJzdWIiOiIxMjM0NSIsImV4cCI6MTYzMjQwMDAwMH0.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

3개 부분으로 나뉘고, signature가 위변조를 막는다. 자체 검증이 가능해 server-to-server 통신에서 stateless 인증이 가능하다.

JWT의 함정은 두 가지다.

**1. 만료(expiry) 없는 token.** JWT에 `exp` claim을 안 넣으면 영원히 유효하다. 한 번 탈취당하면 영영 막을 수 없다. 그래서 access_token은 보통 **15분~1시간** 짧게.

**2. Refresh token rotation.** access_token이 짧으면 사용자가 자주 로그인해야 한다. 그래서 refresh_token을 함께 발급해 자동 갱신. 그런데 refresh_token이 탈취되면 새 access_token을 무한히 발급 가능. 대처는 **refresh token rotation** — refresh로 새 access를 받을 때마다 refresh 자체도 바꾼다. 옛 refresh는 즉시 invalidate.

```
초기: refresh_v1 발급
사용: refresh_v1 → access_v1 + refresh_v2 발급, refresh_v1 invalidate
도난: 공격자가 refresh_v1 사용 시도 → invalidate된 토큰 → 자동 차단 + 사용자 모든 세션 강제 로그아웃
```

이 패턴이 OAuth2 Best Current Practice (RFC 8252)의 표준이다. 한국 핀테크에서는 default로 적용된다.

### RBAC vs ABAC

인가(authorization)는 두 모델이 있다.

**RBAC (Role-Based).** "user에게 role을 부여, role마다 권한 set." 단순하고 직관적. user_id → role → permissions. Spring Security, Django, Rails의 기본 모델.

**ABAC (Attribute-Based).** "user의 attribute + resource의 attribute + context로 permission 결정." 더 유연하지만 복잡. AWS IAM의 condition, Open Policy Agent (OPA)가 ABAC.

대부분의 시스템에는 RBAC로 시작하고, 복잡한 조건(시간·지역·자원 attribute)이 필요해질 때 ABAC를 추가한다. 처음부터 ABAC 전체를 깔면 운영 부담이 크다.

## Service-to-Service 신뢰 — mTLS와 SPIFFE

내부 service 간 통신은 다른 모델이 필요하다. OAuth2 token을 service 간에 흘리는 건 어색하고 위험하다. 그래서 등장한 표준이 **mTLS** (mutual TLS)다.

TLS는 보통 client가 server를 검증한다(우리가 브라우저에서 https 사이트 접속 시). mTLS는 server도 client를 검증한다. 양쪽이 서로의 인증서를 제시하고 검증.

```
service A → service B: 내 cert 보낸다 + B의 cert 검증
service B → service A: 내 cert 보낸다 + A의 cert 검증
양쪽 OK → secure channel
```

이 모양은 다음을 약속한다.

- **상호 인증.** A는 정말 B와 통신 중이라는 확신, B도 마찬가지.
- **암호화.** 중간에서 sniff해도 내용을 못 본다.
- **무결성.** 메시지 위변조가 불가능.

mTLS의 운영 부담이 크다. 모든 service에 인증서를 발급·갱신·revoke해야 한다. 이걸 자동화하는 표준이 **SPIFFE/SPIRE**다.

**SPIFFE** (Secure Production Identity Framework For Everyone)는 service identity를 표준화한다. 각 service에 `spiffe://example.org/ns/prod/sa/payment` 같은 URI를 부여하고, 그 URI를 cert에 박는다. **SPIRE**가 이 cert를 자동 발급·갱신.

그리고 **service mesh** (Istio, Linkerd)가 mTLS를 자동화한다. application code는 plain HTTP를 쓰고, sidecar proxy가 mTLS를 처리. 6장 로드 밸런서·서비스 메시 챕터에서 이미 그 trade-off를 다뤘다.

## Secret 관리 — Vault·KMS의 진짜 운영 과제

서두의 `.env` 사고로 돌아오자. secret을 안전하게 다루는 표준은 무엇인가?

### 평문 secret 금지

다음은 모두 끔찍한 패턴이다.

- **`.env` 파일을 git에 commit.** GitHub 검색에서 가장 자주 노출되는 파턴.
- **환경변수에 직접 박기.** docker-compose, K8s manifest에 평문 적기.
- **로그에 secret 출력.** 디버깅용 `print(config)`가 production에서 통째로 secret을 CloudWatch에 보낸다.
- **에러 메시지에 secret 포함.** stack trace가 secret과 함께 사용자에게 표시.

이 모양들은 secret이 어딘가에 영구적으로 남게 만든다. 한 번 노출되면 회수 불가능. **rotation해야 한다.**

### 표준 도구

- **HashiCorp Vault.** open source의 사실상 표준. dynamic secret, KMS, transit encryption까지. 운영 부담 있음.
- **AWS Secrets Manager.** managed. AWS 친화 팀 default.
- **AWS Parameter Store.** 더 가벼움. 작은 시스템에 적합.
- **GCP Secret Manager.** GCP의 동등 도구.
- **KMS (Key Management Service).** 암호화 key 자체를 관리. 다른 secret 도구의 backbone이 되기도.

이 도구들이 약속하는 핵심 두 가지가 **rotation과 revocation 자동화**다.

**Rotation.** 매 30일·90일마다 secret을 자동으로 바꾼다. 옛 secret이 노출되어도 30일 후엔 무효. 사람이 손으로 돌리던 시절에는 "이번 분기 secret rotation 안 함" 같은 상태가 흔했다. 자동화가 이걸 푼다.

**Revocation.** secret이 노출된 게 발견되면 즉시 invalidate. application들이 자동으로 새 secret을 fetch.

이 두 자동화가 안 되는 secret 도구는 사실 의미가 적다. 평문보다 약간 나은 정도. 새 시스템 도입 시 이 두 능력을 1순위로 확인하는 편이 낫다.

### Application 수준의 패턴

application 코드에서 secret을 안전하게 가져오는 패턴.

```python
# 나쁜 예 — 환경변수 직접 사용
db_password = os.environ['DB_PASSWORD']  # 어디서 왔는지 추적 불가

# 좋은 예 — Vault에서 매 요청 또는 lease로 받기
db_password = vault.read('secret/database')['password']

# 더 좋은 예 — IAM 기반 짧은 lease
db_creds = vault.read_aws_database_credentials('db-role-prod')
# db_creds는 1시간 lease, 자동 rotation
```

가장 안전한 모양이 **dynamic secret**이다. application이 시작할 때 1시간짜리 short-lived credential을 발급받는다. 시간이 지나면 자동 만료. 한 application이 노출돼도 1시간 후엔 그 credential이 무효.

## 한국 환경의 망분리 (한국 2·9)

한국 금융·공공·일부 대기업에는 다른 나라에 없는 보안 요건이 있다. **망분리**다.

**전자금융감독규정**은 금융권에 인터넷망과 업무망을 물리적으로 분리할 것을 요구한다. 즉 결제·송금·계좌 처리하는 시스템은 인터넷에 직접 노출되면 안 된다. 공공기관·일부 대기업도 비슷한 요건이 있다.

이 요건이 클라우드 아키텍처에 미치는 영향이 크다.

**1. Public cloud 그대로 못 쓴다.** AWS·GCP의 일반 region은 인터넷 연결이 default. 망분리 환경에 그대로 쓸 수 없다.

**2. Hybrid cloud 모델 등장.** 인터넷 노출 부분은 public cloud, 내부 처리 부분은 private cloud 또는 자체 IDC. AWS Outposts, GCP Anthos, Azure Stack이 이 시나리오.

**3. VPN / Direct Connect 필수.** public cloud와 internal 망 연결을 위해 dedicated network 연결.

**4. CI/CD 분리.** 코드를 internal 망에 배포하기 위한 별도 pipeline. 인터넷에서 가져온 dependency가 내부 망에 들어오는 과정 검증.

한국 핀테크의 대표 사례 셋을 짚자.

**토스 hybrid cloud.** 토스페이먼츠는 public(AWS) + private(자체) 혼합. critical한 결제 코어는 private, 외부 인증·통신은 public. 이 결정이 progressive rollout, multi-region DR 같은 운영 패턴까지 영향을 준다.

**LINE 자체 IDC.** LINE은 도쿄·한국에 자체 IDC를 운영. 메시징·사용자 데이터가 외부 cloud에 안 나간다. 글로벌 서비스에 자체 인프라 운영 능력이 있는 회사의 모델.

**카카오뱅크 보안 architecture.** 카카오뱅크는 99.99% SLA + 망분리 + 24/7 운영. 메인프레임 → MSA 전환 중에도 망분리 요건을 유지. tech.kakaobank.com에 일부 architecture 공개.

한국 백엔드가 글로벌 회사로 이직하면 가장 낯선 게 망분리가 없다는 점이다. 반대로 글로벌 회사가 한국 진출할 때 가장 큰 장벽이 망분리 대응이다.

> 💡 한국 환경 한 줄 가이드 — **금융·공공·대기업 안의 시스템이라면 망분리 요건을 먼저 확인하자.** 그 요건이 아키텍처의 큰 차원(public vs private, cloud vs IDC)을 결정한다. AWS Outposts·자체 IDC가 단순 선택지가 아니라 필수가 되는 경우가 흔하다.

## Zero Trust — 신뢰 경계가 사라진 시대

전통적인 보안 모델은 **perimeter security(경계 기반 보안)**다. "방화벽 안은 안전, 밖은 위험"이라는 모양. 회사 망 안에 들어온 호출은 신뢰, 밖에서 온 호출은 검증.

이 모델이 깨졌다. 클라우드, 모바일, SaaS, 원격 근무가 perimeter를 사라지게 했다. 우리 직원의 노트북은 카페 wifi에서, 가정 인터넷에서, 호텔에서 모든 곳에서 회사 system에 접속한다. "회사 망 안"이라는 개념 자체가 모호하다.

**Zero Trust**는 이걸 정면으로 받아들인다. "기본은 불신, 모든 호출에 인증을 강제."

Google이 2009년 Operation Aurora 사건 이후 도입한 **BeyondCorp** 모델이 Zero Trust의 사실상 시작이다. 핵심 원칙은 다음과 같다.

- **모든 호출에 인증.** 회사 망 안에서 온 호출이라도 검증.
- **device trust + user trust 결합.** 사용자 ID만이 아니라 device의 무결성도 검증.
- **least privilege.** 작업에 필요한 최소 권한만 부여.
- **continuous verification.** 한 번 인증한 session도 주기적 재검증.

한국 백엔드에서도 Zero Trust 채택이 늘고 있다. 토스·카카오 일부 시스템에 BeyondCorp 모델이 도입된 사례가 있다. perimeter security의 한계를 절감한 후 자연스럽게 가는 방향이다.

## API Gateway와 백엔드의 책임 분리

6장에서 다룬 API Gateway가 보안에도 핵심 역할을 한다. 책임 분리의 모양을 그려 두자.

**API Gateway 책임:**
- Rate limiting (DDoS 1차 방어)
- WAF (SQL injection, XSS 패턴)
- 인증 위임 (OAuth2 검증, JWT verification)
- TLS termination (or pass-through)

**Backend 책임:**
- 비즈니스 인가 (이 user가 이 resource를 정말 볼 수 있는가)
- 도메인 룰 (잔고 검증, 재고 검증)
- 감사 로그 (누가 무엇을 했는지 audit)

이 분리가 왜 중요한가? **gateway는 평면적 룰(이 user는 이 endpoint 호출 가능)에 강하고, backend는 도메인 룰(이 user는 이 specific 자원에 접근 가능)에 강하다.** 둘을 안 가르고 backend에 다 박으면, backend 코드가 보안 로직으로 비대해진다. 둘을 안 가르고 gateway에 다 박으면, gateway가 도메인을 알아야 해서 backend와 결합도가 높아진다.

## DB 접근 통제 — Least Privilege

application이 DB에 접근할 때 항상 admin 권한으로 접근하는 경우가 많다. 끔찍하다. application이 SQL injection으로 침해당하면 DB 전체가 노출된다.

표준 패턴은 **least privilege**다. application별로 별도 DB user를 만들고, 그 user에게 최소 권한만 부여.

```sql
-- 결제 service는 결제 테이블만, 그것도 SELECT/INSERT만
CREATE USER payment_app;
GRANT SELECT, INSERT ON payments TO payment_app;
GRANT SELECT ON users TO payment_app;

-- 다른 테이블엔 접근 불가
```

추가로 **IAM 기반 DB auth**가 secret 없이 접근하는 모양을 가능하게 한다.

- **AWS IAM DB auth.** RDS Postgres·MySQL에서 IAM role로 인증. password 없음.
- **GCP Cloud SQL IAM.** 동등 기능.

이 모양이 가능한 환경에서는 DB password를 secret store에 두지 않아도 된다. application의 IAM identity가 곧 DB 접근 권한이 된다.

## 비밀번호·PII 저장

사용자 password와 PII (Personally Identifiable Information)는 별도 보호가 필요하다.

### Password 저장

평문 저장은 절대 금지. hash 저장이 표준인데, 일반 hash(MD5·SHA-256)는 빠르게 brute force 가능. 그래서 **bcrypt, scrypt, argon2** 같은 의도적으로 느린 hash를 쓴다.

```python
import bcrypt

# 저장 시
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# rounds=12 → 2^12=4096회 반복. 한 password hash에 ~200ms.

# 검증 시
if bcrypt.checkpw(password.encode(), hashed):
    # OK
```

bcrypt의 12 round가 2026년 표준. CPU가 발전하면 14·16으로 올라갈 것. argon2는 GPU 공격에도 강하지만 의존성이 무거워, 새 시스템 외에는 bcrypt가 default.

**rainbow table 방어:** salt가 hash마다 다르게 박혀, 미리 계산된 rainbow table 공격 불가. bcrypt는 salt를 자동 처리.

### 한국 개인정보보호법 맥락

한국에서는 **주민번호·신용정보**가 별도 강력 보호 대상이다. 개인정보보호법 + 신용정보법.

- 주민번호: 저장 자체가 제한. 꼭 필요한 경우만, 별도 암호화(AES-256+) + 접근 통제.
- 신용정보: 신용정보법으로 별도 보호. 일반 PII보다 강한 통제.
- 일반 PII (이름·이메일·전화): encryption at rest + in transit, 접근 로그.

한국 핀테크에서 새 시스템 만들 때 가장 먼저 챙길 게 이 법적 요건이다. "그냥 PII 저장" 같은 단순한 답은 한국에서 불법이 될 수 있다.

## OWASP API Security Top 10 — 백엔드 시각 3가지

OWASP가 API 보안 위협 Top 10을 정기적으로 발표한다. 그 중 백엔드 개발자가 가장 자주 만나는 3가지를 짚자.

**1. Broken Object Level Authorization (BOLA).** 가장 흔한 함정. user A가 user B의 자원에 접근할 수 있는 endpoint. `GET /users/123/orders`에서 123이 자기 user_id가 아니어도 조회 가능한 경우.

```python
# 나쁜 예 — 인증만 검증, 인가는 누락
def get_orders(user_id):
    if not is_authenticated():
        return 401
    return db.query("SELECT * FROM orders WHERE user_id=?", user_id)

# 좋은 예 — 인가 검증 추가
def get_orders(user_id):
    if not is_authenticated() or current_user.id != user_id:
        return 403
    return db.query("SELECT * FROM orders WHERE user_id=?", user_id)
```

**2. Mass Assignment.** request body를 그대로 ORM에 넣으면 위험한 필드까지 갱신. 예를 들어 `User` 객체에 `is_admin` 필드가 있는데, 사용자가 자기 프로필 update 요청에 `is_admin=true`를 끼워 보내면?

```python
# 나쁜 예
def update_user(req):
    user.update(**req.json())  # 사용자가 보낸 모든 필드 적용

# 좋은 예 — allowlist
def update_user(req):
    allowed = {'name', 'email', 'phone'}
    updates = {k: v for k, v in req.json().items() if k in allowed}
    user.update(**updates)
```

**3. Server-Side Request Forgery (SSRF).** 사용자가 보낸 URL을 server가 그대로 fetch하면, 내부 망의 sensitive endpoint(`http://169.254.169.254/`의 AWS metadata service)에 접근 가능.

```python
# 나쁜 예
url = request.json['callback_url']
response = requests.get(url)

# 좋은 예 — allowlist + 내부 IP 차단
if not is_allowed_domain(url) or is_internal_ip(url):
    return 400
```

이 셋만 챙겨도 한국 백엔드에서 자주 만나는 보안 사고의 대부분이 막힌다.

## 사고 사례 — 2022 카카오 SK C&C 화재

한국 보안 사례 중 가장 잘 알려진 게 2022년 10월 카카오 데이터센터 화재다. SK C&C 판교 IDC에 화재가 나서 카카오의 다수 서비스가 멈췄다. 보안 사건은 아니지만, **신뢰성·보안의 경계**에 있는 사고였다.

이 사고에서 드러난 보안·운영 관점의 교훈 몇 가지.

1. **자체 IDC 단일 의존성의 위험.** 다른 region·다른 데이터센터에 hot standby가 없었다. multi-region이 이후 한국 기업의 표준 화두로 격상.
2. **DR(Disaster Recovery) 계획 vs 실제 실행 gap.** DR 계획은 있었으나 실제 실행은 며칠 걸렸다. 정기 DR drill이 없으면 계획서는 종이일 뿐.
3. **secret·인증서의 multi-region 분배.** 데이터센터가 죽으면 그 안의 secret도 함께 죽는다. KMS·Vault의 multi-region 복제가 critical.

이 사고 이후 한국 기업의 multi-region·multi-cloud 채택이 빠르게 늘었다. 보안과 신뢰성은 한 차원에서 만난다.

## 모든 새 endpoint에 던질 5가지 질문

이 챕터의 핵심 통찰을 5가지 질문으로 압축하자. 새 endpoint를 설계할 때 자동으로 떠올리는 5가지다.

1. **인증?** 누가 호출하는지 어떻게 검증하는가? OAuth2/JWT, mTLS, IAM 중 무엇?
2. **인가?** 인증된 사용자가 이 자원에 접근할 권한이 있는가? object level까지 검증하는가?
3. **Secret 어디서 어떻게?** 평문 박지 않았는가? secret store에서 dynamic하게 가져오는가?
4. **Rotation?** secret이 30일·90일마다 자동 갱신되는가?
5. **Audit log?** 누가 무엇을 언제 했는지 기록되는가? 사후 추적 가능한가?

이 다섯이 머릿속에 있으면 코드 리뷰에서 "이 endpoint는 BOLA 검증 빠진 것 같은데?", "이 secret은 어디서 왔어?" 같은 질문이 자연스럽게 나온다. **그리고 그 다섯 질문이 자동으로 떠오를 때, 0장에서 약속한 6번째 약속 — "보안이 별도 영역이 아니라 모든 빌딩 블록 위에 깔린 통제 평면(control plane)임이 손에 박힌다" — 의 회수가 여기서 일어난다.**

## Callback 예고

보안은 이 책의 후속 챕터에서 다음 자리에 핵심으로 다시 등장한다.

- **19장 결제·금융.** 결제 audit chain·blameless postmortem이 9장의 control plane(인증·인가·secret·audit log) 위에서 작동.

6장 로드 밸런서·서비스 메시에서 다룬 mTLS·service mesh도 9장의 service-to-service 위협 모델 위에서 작동하는데, 이건 6장에서 이미 함께 짚었다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 분산 시스템 보안의 지형이 손에 잡혀 있다. 3축 위협 모델(service-to-service·user-to-service·admin-to-system), OAuth2/OIDC·JWT·RBAC/ABAC, mTLS·SPIFFE·service mesh, Vault·KMS의 rotation·revocation, 한국 망분리(전자금융감독규정 + 토스·LINE·카카오뱅크 사례), Zero Trust·BeyondCorp, API Gateway 책임 분리, OWASP API Top 10, 그리고 2022 카카오 화재의 교훈까지가 한 묶음이다.

기억해두자. 보안은 production의 가장 약한 고리고, 우리가 매일 만지는 영역이다. `.env`를 git에 push하는 한 줄 게으름이 회사를 흔든다. secret을 코드에서 분리하고, 모든 endpoint에 5가지 질문(인증·인가·secret·rotation·audit)을 자동으로 던지는 습관이 우리 시스템의 1번 안전망이다.

다음 부에서는 케이스 스터디로 넘어간다. 빌딩 블록과 패턴을 다 갖춘 우리가, 실제 시스템(채팅·피드·검색·결제·이커머스)을 어떻게 조립하는지를 함께 본다. 이 챕터의 보안 통찰이 그 시스템들 모두의 control plane으로 깔린다.

---

**reference 한계 명시:** 02_plan §3 9장 사양에 적힌 대로 보안은 본 리서치에서 부분 커버. 본 챕터는 02_plan §3 9장 사양 + 일반 보안 지식 기반. OAuth2 RFC 6749/8252, OWASP API Security Top 10 (2023), 전자금융감독규정 등 1차 자료로 추가 검증·보강이 필요하다(검증 필요).
