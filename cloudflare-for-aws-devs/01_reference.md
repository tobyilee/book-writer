# AWS 개발자를 위한 Cloudflare 본격 활용 가이드 — 통합 레퍼런스

## 0. 책 정보 요약

- **주제:** AWS를 주력으로 써온 개발자를 위한 Cloudflare 본격 활용 가이드
- **대상 독자:** Java/Spring/AWS 백엔드 경력자, React/Next.js/TS/JS 기초 보유, 로컬은 macOS
- **저자:** Toby-AI
- **리서치 시점:** 2026년 5월 (Cloudflare 변동성이 크기 때문에 최소 분기마다 재확인 필요)
- **핵심 메시지:** Cloudflare는 "또 하나의 클라우드"가 아니라, AWS와 멘탈 모델이 다른 edge-first 플랫폼이다. 1:1 대응으로만 보면 핵심을 놓친다.

---

## 1. 개념 정의 사전

| 용어 | 한 줄 정의 | AWS 비유 (느슨하게) |
|---|---|---|
| **Cloudflare Workers** | V8 isolate 기반 서버리스 런타임. 코드는 Cloudflare 글로벌 네트워크의 모든 데이터센터에서 실행된다. | Lambda + Lambda@Edge 의 혼합, 단 컨테이너 없음 |
| **V8 Isolate** | 한 V8 프로세스 안에서 격리된 JS 실행 컨텍스트. 자체 힙·GC를 가지지만 OS 프로세스를 새로 띄우지 않는다. | Lambda execution context의 더 가벼운 형태 |
| **Durable Objects (DO)** | 전역적으로 유일한 객체 인스턴스 + 고정된 실행 위치 + 강한 일관성 스토리지. Actor 모델에 가장 가깝다. | DynamoDB + Lambda + ElastiCache 의 조합을 한 추상으로 묶은 것 |
| **D1** | SQLite-at-edge. Workers에 바인딩되는 관리형 SQLite. | 작은 RDS Postgres + read replica의 SQLite 버전 |
| **KV** | 글로벌 key-value 저장소. eventually consistent (최대 60초 전파). | DynamoDB Global Table의 단순화·완화 버전 |
| **R2** | S3 호환 object storage. **egress 무료**가 핵심 차별점. | S3 |
| **Hyperdrive** | 외부 Postgres/MySQL에 대한 글로벌 connection pool + 쿼리 캐시. DB가 아니라 connection 가속기. | RDS Proxy의 글로벌 버전 |
| **Workers Routes / Custom Domains** | URL 패턴 → Worker 매핑. | API Gateway + CloudFront behavior |
| **Workflows** | Workers 위의 durable execution engine. step 단위 자동 재시도·상태 영속화. | Step Functions |
| **Queues** | Cloudflare 네이티브 메시지 큐. | SQS (단순 큐) |
| **Workers AI** | Cloudflare 인프라 위 LLM/임베딩 inference 서비스. Neuron 단위 과금. | Bedrock |
| **Vectorize** | 글로벌 분산 벡터 DB. | OpenSearch k-NN, pgvector |
| **AI Gateway** | LLM 요청 프록시. 캐싱·rate limit·관측·모델 fallback. | (AWS에 정확한 등가물 없음. 자체 구축이 일반적) |
| **Cloudflare Access / Zero Trust / Tunnel** | SASE 패키지. 사용자·디바이스 기반 접근 제어 + 사설 네트워크로의 outbound-only tunnel. | IAM Identity Center + Verified Access + Site-to-Site VPN/PrivateLink |
| **Pages → Workers Static Assets** | 정적 사이트 호스팅. 2025년 4월부터 Pages는 사실상 maintenance 모드, 신규 기능은 Workers로 흡수. | Amplify Hosting |
| **Wrangler** | Cloudflare 개발자 플랫폼 CLI (`wrangler dev`, `wrangler deploy`, `wrangler types`...). | SAM CLI / CDK CLI |
| **`wrangler.toml` / `wrangler.jsonc`** | Worker 설정 파일. 바인딩(KV, R2, D1, Queue, Service 등) 선언. | `template.yaml`, `cdk.json` |
| **Bindings** | Worker가 다른 리소스(KV, R2, DO 등)를 호출하기 위한 타입 안전한 핸들. IAM role + SDK client 두 역할을 합친다. | IAM permission + AWS SDK client |
| **Compatibility Date / Flags** | Workers 런타임 동작을 시점 기반으로 고정시키는 메커니즘. | (AWS에 직접 등가물 없음. Lambda runtime 버전 + feature flag와 비슷) |

---

## 2. AWS ↔ Cloudflare 1:1 매핑 표

각 행: (a) 기능 동등성/차이, (b) 가격 모델, (c) 콜드스타트/지연/리전 모델, (d) 마이그레이션 주의점.

### 2.1 컴퓨트

| AWS | Cloudflare | 매핑 노트 |
|---|---|---|
| **Lambda** | **Workers** | (a) 둘 다 함수형 서버리스. 그러나 Lambda는 컨테이너+JVM/Node 런타임, Workers는 V8 isolate에서 JS/TS/Python/WASM/Rust(WASM 컴파일) 실행. Lambda는 임의 바이너리·패키지 자유, Workers는 Web standards API + 일부 Node compat. (b) Lambda: 100ms 단위 GB-s + 요청 수, Workers Standard: CPU time(요청 단위) 기반. **I/O 대기 시간은 과금되지 않음.** Standard 요금제는 Worker당 1M req/$0.30 + CPU 100만 ms/$0.02 같은 식. 무료 plan에 100k req/일 포함. (c) Lambda 콜드스타트 200ms~수초(언어/패키지 따라), Workers는 5ms 미만. (d) JVM·heavy npm 패키지·OS 호출이 필요한 워크로드는 옮길 수 없음. 1MB(Free)·10MB(Paid) 스크립트 크기 제한. |
| **Lambda@Edge** | **Workers** | (a) Lambda@Edge는 CloudFront 동기 트리거에 묶여 있고 리전 한정 + 큰 콜드스타트. Workers는 모든 PoP에서 동시 실행이 기본값. (c) Lambda@Edge는 동남아·남미에서 400~600ms 콜드스타트가 보고됨. Workers는 글로벌 균일. |
| **ECS / Fargate** | **Workers Containers (Dynamic Workers / Containers)** | (a) Cloudflare Containers는 Docker 이미지를 받아 글로벌 PoP에서 실행. wrangler deploy 한 번으로 ~10초 내 글로벌 배포. ECS+Fargate는 1~3 리전, 빌드·푸시·롤링 업데이트로 3~5분. (b) Cloudflare는 10ms 단위 빌링. Workers Paid($5/mo) 필요. (c) Cloudflare 한도: 인스턴스당 0.5 vCPU / 4 GiB RAM (확장 예정). 더 큰 워크로드는 여전히 ECS/Fargate가 우위. (d) GPU·대용량 인스턴스·VPC 깊이 연동이 필요하면 ECS 유지. |
| **Step Functions** | **Workflows (GA, 2024 11월 발표 → 2025 GA)** | (a) Step Functions는 ASL DSL + IaC가 필요. Workflows는 코드(`step.do(...)`, `step.sleep(...)`)로 작성. (b) 핵심 차이: Workflows는 **실행 중인 CPU 시간만 과금**, sleep·외부 API 대기 시 $0. Step Functions는 state transition 단위 과금이라 long-poll·승인 대기가 비용에 그대로 잡힘. (d) AWS 서비스 통합(IAM·S3·SNS 등 200+ 액션)이 풍부한 Step Functions의 ecosystem 종속성을 옮기기는 쉽지 않음. |

### 2.2 스토리지·DB

| AWS | Cloudflare | 매핑 노트 |
|---|---|---|
| **S3** | **R2** | (a) S3 호환 API(완전한 호환은 아니지만 PUT/GET/multipart/presigned URL 등 핵심 커버). (b) **egress free**가 결정타. R2 storage ~$0.015/GB·월, Class A/B operations 별도. S3 Standard ~$0.023/GB·월 + $0.09/GB egress. 50TB egress 시나리오에서 R2가 30~99% 저렴한 사례 다수. (d) Lifecycle policy·Glacier·Object Lock 같은 enterprise 기능 일부 부재. SDK는 `aws-sdk` 그대로 endpoint만 R2로 바꿔 사용 가능. |
| **DynamoDB** | **KV / D1 / Durable Objects 중 선택** | "DynamoDB = ?" 한 줄 매핑은 잘못된 모델. 사용 패턴별로 갈라짐 → §5 참고. KV는 read-heavy·세션·플래그, D1은 SQL 쿼리·관계형, DO는 강한 일관성·per-entity·WebSocket. |
| **DynamoDB (transactional)** | **Durable Objects** | DO는 transactional·strongly consistent·serializable. 재고·예약·턴 기반 게임 같은 race condition 방어가 필요한 곳. |
| **DynamoDB (read-heavy + 글로벌 복제)** | **KV** | KV는 eventually consistent (최대 60s 전파), per-key 1 write/s 한도. credential·config·세션 데이터에 적합. |
| **Aurora / RDS** | **D1 (관계형, 작은 규모) / Hyperdrive (기존 RDS·Aurora에 그대로 붙임)** | D1은 SQLite at edge, max 10GB/DB. 기존 Postgres/MySQL 그대로 쓰려면 Hyperdrive로 connection pool + query cache. Hyperdrive는 TCP handshake(1)·TLS(3)·DB auth(3) 총 7 round-trip을 글로벌 풀에서 흡수. |
| **ElastiCache (Redis)** | **Cache API + KV / Durable Objects + Upstash Redis (3rd party)** | ElastiCache는 TCP 기반 → Workers에서 직접 못 씀. Cloudflare에서는 Cache API(요청 단위 ephemeral KV), KV(전역 eventual), DO(per-key strong)를 조합. Upstash처럼 REST 기반 Redis만 edge에서 사용 가능. |
| **OpenSearch (vector)** | **Vectorize** | Vectorize는 글로벌 분산, 인덱스당 5M vector / 계정당 50k namespace. **hybrid search 미지원**(2026 기준). 큰 규모·hybrid search는 OpenSearch 유지가 합리적. |

### 2.3 네트워크·전달

| AWS | Cloudflare | 매핑 노트 |
|---|---|---|
| **CloudFront** | **Cloudflare CDN (기본 포함)** | (a) Cloudflare는 모든 PoP가 풀스택(컴퓨트·캐시·WAF). CloudFront PoP는 캐시 + 제한된 함수, 무거운 컴퓨트는 Lambda@Edge 별도. (c) Purge 속도: Cloudflare ~150ms 글로벌, CloudFront 10~15분. (b) Cloudflare 무료 플랜에서 무제한 대역폭·DDoS 방어·SSL 포함. CloudFront는 트래픽·요청 모두 과금. |
| **Route 53** | **Cloudflare DNS** | (c) 평균 lookup: Cloudflare ~11~13ms, Route 53 ~20ms. (b) Cloudflare DNS는 도메인당 무료(기본). Route 53는 hosted zone $0.50/월 + 쿼리 과금. (d) 복잡한 weighted/geo/failover 라우팅은 Route 53가 더 풍부. |
| **API Gateway (REST/HTTP)** | **Workers Routes + Hono (또는 itty-router 등)** | API Gateway에 해당하는 별도 제품이 없다. URL 패턴·custom domain은 Workers Routes로, 미들웨어·라우팅·검증은 코드(특히 Hono)로 구현. AI 트래픽이라면 **AI Gateway**가 별도. |
| **SQS** | **Queues** | at-least-once, 메시지 본문 <128KB, 기본 보존 4일, batch·DLQ·retry 지원. Worker consumer는 push 기반 호출. egress 비용 없음. |
| **SNS / EventBridge** | **Queues + Workers (직접 fan-out) / Pub/Sub (베타)** | 1:N pub/sub, 패턴 매칭·rule 기반 라우팅 대응 제품이 약함. EventBridge 수준의 sophisticated routing은 Workers + DO·Queues로 직접 구성. |
| **Site-to-Site VPN / PrivateLink** | **Cloudflare Tunnel (cloudflared) / Cloudflare One** | cloudflared가 사설망 내부에서 outbound-only tunnel을 Cloudflare로 연다. 양방향·서버 발신 트래픽이 필요하면 Cloudflare Mesh 별도. PrivateLink 같은 cross-VPC private endpoint와는 모델이 다르다. |

### 2.4 보안·인증

| AWS | Cloudflare | 매핑 노트 |
|---|---|---|
| **IAM (사용자·서비스 인증)** | (1:1 등가 없음) | Worker 간 권한은 Bindings(코드 레벨)로, 사람·디바이스 액세스는 Cloudflare Access. IAM role의 정교한 정책 언어는 Cloudflare에 등가물 없음. |
| **Cognito** | **Cloudflare Access + 외부 IdP / Auth.js·Clerk·Lucia** | Cloudflare Access는 SASE 관점이라 SaaS·앱에 SSO 거는 데 강함. 일반 사용자 회원가입·소셜 로그인은 Workers 위에 Auth.js / Clerk / Lucia 같은 라이브러리를 얹는 패턴. |
| **AWS Verified Access** | **Cloudflare Access** | 둘 다 ZTNA. Cloudflare Access는 OIDC/SAML 다양 IdP, 브라우저 기반 SSH/VNC 등 개발자 친화 기능. |
| **WAF** | **Cloudflare WAF + Bot Management + Turnstile + API Shield** | Cloudflare 보안 스택은 상품 묶음. Turnstile은 CAPTCHA 대체(invisible challenge). API Shield는 schema validation + mTLS. |
| **Secrets Manager / Parameter Store** | **Workers Secrets / Secrets Store / `.dev.vars`** | 로컬 `.dev.vars` (gitignore), 배포 secret은 `wrangler secret put`. 2025년 발표된 Secrets Store는 account-level 중앙 관리. |

### 2.5 관측성

| AWS | Cloudflare | 매핑 노트 |
|---|---|---|
| **CloudWatch Logs** | **Workers Logs (실시간 tail) + Workers Logpush (R2/S3/Datadog/New Relic 등으로 push)** | Logpush는 Workers Paid·Enterprise만, 100만 req당 $0.05. 검색·alerting은 Cloudflare 자체 기능보다는 외부 sink로 보내는 패턴이 일반적. |
| **CloudWatch Metrics** | **Workers Analytics + Workers Analytics Engine** | Analytics Engine은 사용자 정의 이벤트를 SQL로 쿼리. 커스텀 메트릭에 적합. |
| **X-Ray** | **Workers Trace Events / 외부 APM (Sentry, Baselime, Axiom)** | 분산 트레이스는 Cloudflare 자체로는 부족. Logpush로 외부 APM에 보내는 게 표준 패턴. |

### 2.6 AI·신영역

| AWS | Cloudflare | 매핑 노트 |
|---|---|---|
| **Bedrock** | **Workers AI** | (b) Workers AI: $0.011/1k Neurons + 일 10k Neurons 무료. Bedrock은 모델별 토큰 단위 + 일부 캐시 할인 (Anthropic은 cache write 과금, Titan은 무료). Bedrock은 모델 카탈로그·enterprise feature가 두텁고, Workers AI는 edge inference·간편함이 강점. |
| **Bedrock + custom 게이트웨이** | **AI Gateway** | AI Gateway는 70+ 모델 / 12+ provider를 단일 endpoint로. 캐싱(동일 요청 최대 90% 지연 감소), rate limit, retries, model fallback, 비용·토큰 분석. |

---

## 3. Workers 멘탈 모델 — Spring·Lambda 개발자 관점

### 3.1 V8 Isolate 런타임의 본질

- Lambda는 함수마다 **컨테이너(microVM, Firecracker)** 를 띄운다. 컨테이너 재사용으로 warm 상태가 되어도 처음 한 번은 200ms~수 초가 걸린다 ([Cloudflare Workers vs AWS Lambda](https://www.morphllm.com/comparisons/cloudflare-workers-vs-lambda)).
- Workers는 **단일 V8 프로세스 안에서 isolate를 켠다**. isolate는 자기만의 heap·GC를 가지지만 OS 레벨 자원은 공유. 그래서 **5ms 미만의 콜드스타트**가 가능하다 ([Cloudflare Workers V8 Isolates](https://www.kunalganglani.com/blog/cloudflare-workers-v8-isolates-ai-agents)).
- 트레이드오프:
  - 임의 바이너리·full Node API·OS syscall 불가.
  - 멀티스레딩 불가 (Spectre 방어 정책의 일부 — `Date.now()`는 스크립트 실행 중 고정값을 반환).
  - 한 요청당 CPU 시간 제한(기본 30초, 그러나 과금은 무료 50ms~Standard에서 더 유연 / 과거 Bundled 50ms 설정이 자동 마이그레이션됨).

### 3.2 보안·격리 모델 (Spring 개발자가 의외로 신경 써야 하는 부분)

- 같은 isolate 안 컨텍스트는 heap·compiled code cache를 공유하므로, **Spectre 류 side channel이 이론적으로 가능**. Cloudflare는 (1) 로컬 시간 측정 차단, (2) 동시성 차단, (3) MPK 같은 하드웨어 격리, (4) V8 보안 패치를 Chrome 안정 채널보다 먼저 production에 배포 — 등으로 방어한다 ([Cloudflare Workers Security Model](https://blog.cloudflare.com/mitigating-spectre-and-other-security-threats-the-cloudflare-workers-security-model/)).
- "V8 보안 패치를 Chrome stable보다 먼저 production에 푸는" 정책은 HN에서 양가적 평가를 받는다 ([HN 46458963](https://news.ycombinator.com/item?id=46458963)) — 빠른 보안 대응이지만 안 익은 패치가 production에 들어갈 가능성도.
- Spring 보안 멘탈 모델(`SecurityFilterChain`, IAM role 기반 권한)은 **Bindings + Cloudflare Access + WAF 룰**의 조합으로 다시 짜야 한다.

### 3.3 요청-응답·미들웨어·DI를 어떻게 옮길까

- 요청-응답: Workers의 export default는 `fetch(request, env, ctx)`. Hono를 얹으면 Express에 가까운 라우팅·미들웨어 체인을 얻는다 ([Hono on Workers](https://hono.dev/docs/getting-started/cloudflare-workers)).
- 미들웨어: Hono의 `use()`/`every()`/`some()` 패턴으로 Auth → Rate Limit → Cache → Proxy → Log 체인 구성 ([Production API Gateway on Workers with Hono](https://dev.to/young_gao/building-a-production-api-gateway-on-cloudflare-workers-with-hono-2lhg)).
- DI: Spring 같은 컨테이너는 없지만, Bindings(env)가 사실상 "런타임이 주입해주는 의존성"이다. `env.DB`, `env.MY_BUCKET`, `env.MY_QUEUE`. 테스트 시 모킹은 `getBindingsProxy()` 또는 vitest pool로.
- 트랜잭션: Workers 자체에 트랜잭션 개념 없음. D1은 statement-level transaction, DO는 storage 단에 transactional. 분산 트랜잭션이 필요하면 DO를 트랜잭션 코디네이터로 쓰는 패턴.
- 장기 작업: Spring Batch / @Scheduled 류는 **Cron Triggers + Workflows** 조합. 외부 API 대기는 무료 — 이게 Step Functions와의 가장 큰 비용 차별점.

### 3.4 코드 비교 — 같은 기능, 다른 멘탈

**Spring Boot의 친숙한 코드**

```java
@RestController
@RequestMapping("/users")
class UserController {
    private final UserRepository repo;
    UserController(UserRepository repo) { this.repo = repo; }

    @GetMapping("/{id}")
    User get(@PathVariable Long id) {
        return repo.findById(id).orElseThrow();
    }
}
```

**Workers + Hono + D1**

```ts
import { Hono } from "hono";

type Bindings = { DB: D1Database };

const app = new Hono<{ Bindings: Bindings }>();

app.get("/users/:id", async (c) => {
  const id = c.req.param("id");
  const row = await c.env.DB
    .prepare("SELECT * FROM users WHERE id = ?")
    .bind(id)
    .first();
  if (!row) return c.notFound();
  return c.json(row);
});

export default app;
```

**핵심 차이**:
- DI 컨테이너 없음. `c.env.DB`가 런타임 주입.
- Repository 추상화·JPA 없음. SQL 직접 또는 Drizzle/Kysely 사용.
- 트랜잭션 모델은 D1 statement 또는 batch. JPA의 `@Transactional`처럼 자동 propagation 없음.
- 어디에서 도는가? — Spring Boot는 EC2/ECS의 정해진 리전. Workers는 사용자에게 가장 가까운 PoP.

### 3.5 운영 멘탈 모델 차이

- AWS는 "리전·VPC·서브넷·Security Group" 위에 모든 게 얹힌다. Cloudflare는 **리전 개념이 사실상 없다** — 코드는 글로벌 PoP에 동시 배포되고, 데이터 국지화가 필요하면 Jurisdiction(EU 등) 또는 D1 location hint, DO location hints로 조절.
- 배포 단위: Lambda는 함수, Workers는 "Worker 1개 = 라우팅·바인딩·코드의 묶음" — Spring Boot 모듈이 더 가까운 비유.

---

## 4. 로컬 개발 워크플로우 (Mac 기준)

### 4.1 도구 설치

- **권장**: `pnpm add -D wrangler@latest` (또는 `bun add -d wrangler@latest`). 글로벌 설치(`npm i -g wrangler`)는 버전 어긋남 위험 ([Install/Update Wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update/)).
- Homebrew용 wrangler 패키지는 비공식이라 Cloudflare 공식 권장 안 함.
- 인증: `wrangler login` (브라우저 OAuth) 또는 `CLOUDFLARE_API_TOKEN` 환경변수 (CI에서 권장).

### 4.2 `wrangler dev` 동작

- 기본은 **로컬 모드** (workerd 런타임을 로컬에 띄움). 그래서 production과 같은 V8 isolate 동작을 그대로 재현한다.
- `--remote` 플래그로 Cloudflare edge에서 직접 실행 가능 (로컬 머신에서 시뮬레이션 안 되는 일부 기능 — 예: 일부 Zone 기능 — 테스트용).
- `wrangler dev --local`은 D1·R2·KV·Queues를 SQLite/디스크 기반으로 로컬 시뮬레이션 ([Local development](https://developers.cloudflare.com/workers/development-testing/)).
- Pages/Workers Static Assets와 같이 띄우려면 `wrangler pages dev`도 가능 (단 Pages는 흡수 중이라 새 프로젝트에는 Workers Static Assets 권장).

### 4.3 패키지 매니저 선택 가이드

- **pnpm**: 모노레포·디스크 효율 측면에서 제일 무난. 책 예제도 pnpm 권장.
- **bun**: 속도·번들러 통합이 좋지만, Workers SDK 일부 도구가 bun lockfile에 약간 까칠한 시기가 있었다(2024). 2026년 시점은 대체로 안정.
- **npm**: 무난하지만 모노레포에선 워크스페이스 도구로는 약함.

### 4.4 TypeScript 설정

- 옛날 방식: `npm install -D @cloudflare/workers-types` + tsconfig `types: ["@cloudflare/workers-types"]` ([Write Workers in TypeScript](https://developers.cloudflare.com/workers/languages/typescript/)).
- 권장 방식(2024~): `wrangler types` → `worker-configuration.d.ts` 자동 생성, 그 안에 `Env` 타입과 compat date 기반 runtime types가 들어옴 ([Automatically generated types](https://blog.cloudflare.com/automatically-generated-types/)).
- `nodejs_compat` 플래그를 켜면 `@types/node`도 함께 설치.

### 4.5 시크릿·환경변수

- 로컬: `.dev.vars` (gitignore 필수). `.env`와 동시에 쓰지 말 것 — `.dev.vars` 존재 시 `.env`는 무시 ([Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)).
- 배포: `wrangler secret put MY_SECRET` → 새 Worker 버전이 즉시 배포됨. 대시보드에서 값은 보이지 않음.
- 다중 환경: `wrangler.toml`의 `[env.staging]` / `[env.production]` 블록 + `wrangler secret put --env staging`.
- 신규: **Cloudflare Secrets Store** (account-level 중앙 관리). 여러 Worker에서 동일 secret 참조하는 경우에 적합.

### 4.6 `wrangler.toml` 핵심 필드 (Spring 개발자가 처음 보면 헷갈리는 것들)

```toml
name = "my-api"                       # Worker 식별자 (URL의 일부가 됨)
main = "src/index.ts"                 # 엔트리 파일
compatibility_date = "2025-04-01"     # 이 날짜의 런타임 동작으로 고정
compatibility_flags = ["nodejs_compat"]

[[kv_namespaces]]
binding = "SESSIONS"
id = "..."                            # 프로덕션 KV namespace ID

[[r2_buckets]]
binding = "MEDIA"
bucket_name = "my-media"

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "..."

[[durable_objects.bindings]]
name = "ROOM"
class_name = "ChatRoom"

[[migrations]]                        # DO 클래스 변경 시 필수
tag = "v1"
new_classes = ["ChatRoom"]

[env.staging]
vars = { LOG_LEVEL = "debug" }

[env.production]
vars = { LOG_LEVEL = "info" }
```

- **`compatibility_date`**: AWS의 Lambda runtime 버전과 비슷한 역할. 한 번 정하면 그 시점의 런타임 동작이 고정됨. 새 기능 쓰려면 날짜를 올린다.
- **Bindings**: Spring의 `@Autowired`나 AWS의 IAM role을 합친 개념. `env.DB.prepare(...)`처럼 코드에서 직접 사용. 권한·SDK가 분리돼 있는 AWS 모델과 다르다.
- **DO migrations**: Durable Object 클래스 추가/이름 변경 시 마이그레이션 태그 필요. 안 그러면 배포 거부됨.

### 4.7 모노레포 구조 (Workers + Next.js)

권장 레이아웃 예시:

```
apps/
  web/           # Next.js (OpenNext for Cloudflare로 Worker로 빌드)
  api/           # Workers + Hono (REST API)
  worker-jobs/   # Cron Triggers + Workflows
packages/
  db/            # Drizzle ORM 스키마 (D1 또는 Hyperdrive 대상)
  shared/        # 공통 타입·유틸
```

- `apps/web`은 `@opennextjs/cloudflare`로 빌드, Workers Static Assets에 정적 자원 + Worker로 SSR.
- 각 앱마다 `wrangler.toml` 분리, 공통 binding(KV·D1)은 같은 namespace 공유.
- Vite plugin (`@cloudflare/vite-plugin`)이 2025년에 발표되어 React Router·Astro·Next.js(부분)에 점진적으로 적용 ([Pages Workers Again](https://www.brycewray.com/posts/2025/11/pages-workers-again-revisited/)).

---

## 5. 데이터·스토리지 심화

### 5.1 선택 가이드 ([Choosing a data or storage product](https://developers.cloudflare.com/workers/platform/storage-options/))

| 상황 | 추천 | 이유 |
|---|---|---|
| 세션·플래그·API key·설정 | KV | read-heavy + 글로벌 + eventual OK |
| 사용자 데이터·ad-hoc SQL·관계형 | D1 | SQL + read replica + 비용 저렴 |
| 카운터·재고·예약·턴 게임 | Durable Objects | strong consistency + serializable |
| 멀티테넌트 SaaS의 per-tenant 상태 | Durable Objects | per-entity 격리 + 자체 SQLite |
| 채팅·실시간 대시보드·multiplayer | Durable Objects + WebSocket Hibernation | 영속 연결 + idle 시 과금 X |
| 큰 파일·미디어·백업 | R2 | egress free + S3 호환 |
| 기존 Postgres/MySQL 살리기 | Hyperdrive | 7 round-trip 흡수 + query cache |
| 작은 캐시 / hot path | Cache API | 요청 단위 ephemeral KV |

### 5.2 D1 깊이 보기

- SQLite 기반 → JOIN·CTE·트랜잭션 전부 됨.
- 1 DB 최대 10GB ([D1 vs Neon vs PlanetScale](https://bejamas.com/compare/cloudflare-d1-vs-neon-vs-planetscale)).
- Read replica는 자동, write는 primary로 → write-heavy(2k+ TPS) 워크로드는 부적합.
- Sustained write 비교 — D1: 500~2k/s, Turso: 1~5k/s, PostgreSQL/MySQL: 10k~50k/s.
- Workers Paid 기본 포함량: 250억 row read, 5천만 row write, 5GB storage.

### 5.3 Durable Objects 깊이 보기

- Actor 모델: Erlang/Elixir/Akka/Orleans와 비슷한 모델 ([What are Durable Objects](https://developers.cloudflare.com/durable-objects/concepts/what-are-durable-objects/)).
- 한 객체는 전역에서 단일 인스턴스 → 이 안에서는 single-threaded처럼 작동, 그래서 race condition 없음.
- 자체 SQLite 스토리지 (per-DO). D1과 달리 하나의 객체에 종속.
- **WebSocket Hibernation API**: 클라이언트가 연결 유지 중이어도 DO가 메모리에서 내려가면 GB-s 과금 발생 안 함 → 채팅 같은 long-lived connection 비용 절감 ([Use WebSockets](https://developers.cloudflare.com/durable-objects/best-practices/websockets/)).
- 유즈케이스: chat room, 실시간 협업 문서, 인벤토리, multiplayer, 사용자별 rate limit.

### 5.4 KV 한계

- eventual consistency, **최대 60초 전파** ([Workers KV Practice Guide](https://eastondev.com/blog/en/posts/dev/20260422-cloudflare-workers-kv-guide/)).
- per-key 1 write/s.
- 보조 인덱스·범위 쿼리 없음 → DynamoDB의 secondary index를 기대하면 안 됨. 이게 Liftosaur가 Workers를 떠난 결정적 이유 중 하나 ([Liftosaur](https://www.liftosaur.com/blog/posts/how-i-moved-liftosaur-from-cloudflare-workers-to-lambda/)).

### 5.5 R2 실무 노트

- S3 호환이지만 100% 호환은 아님. 대부분의 SDK는 endpoint 변경만으로 동작. Lifecycle·Glacier·Object Lock 일부 부재.
- multipart upload, presigned URL, S3 API 모두 지원.
- 가격(2026 기준 정리): storage ~$0.015/GB·월, Class A ops $4.50/M, Class B ops $0.36/M, **egress $0**.
- 미디어 스트리밍·백업·LLM 학습 데이터처럼 egress가 큰 워크로드에서 90~99% 절감 사례 다수 ([R2 vs S3](https://yconsulting.substack.com/p/cloudflare-r2-vs-the-big-3-a-deep)).

### 5.6 Hyperdrive 메커니즘

- Cloudflare 네트워크 내에 connection pool 유지 → Worker 호출 때마다 7 round-trip(TCP 1 + TLS 3 + DB auth 3)을 흡수 ([How Hyperdrive works](https://developers.cloudflare.com/hyperdrive/concepts/how-hyperdrive-works/)).
- **transaction mode**로 동작. 한 트랜잭션 동안 단일 연결을 점유, 끝나면 풀로 반환.
- AWS RDS/Aurora에 그대로 붙일 수 있음 ([AWS RDS and Aurora](https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/aws-rds-aurora/)).
- 2025년 가격 정책 변경: 무료 plan 사용자에게도 Hyperdrive 무료 제공 ([Pools across the sea](https://blog.cloudflare.com/how-hyperdrive-speeds-up-database-access/)).

---

## 6. Next.js on Cloudflare 현황

### 6.1 옵션 비교 (2026 5월 시점)

| 방식 | 권장도 | 메모 |
|---|---|---|
| **Cloudflare Pages** | ▲ (legacy) | 2025년 4월 이후 사실상 maintenance. 새 프로젝트는 Workers로 ([Migrate from Pages](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/)). |
| **Workers Static Assets** | ◎ | 정적 SPA·SSG에 적합. Worker 코드 + 정적 자원이 한 배포 단위. |
| **`@opennextjs/cloudflare`** | ◎ (Next.js 풀 기능) | 1.0-beta 시점에 대부분의 Next 14/15 앱이 동작. 한계: Edge Runtime 미지원(Node runtime만), Windows 미완전 지원 ([OpenNext Cloudflare](https://opennext.js.org/cloudflare)). |
| **Vercel** | (외부) | DX·Next 기능 풀커버. 비용·벤더 종속이 단점. |

### 6.2 OpenNext 한계 (2026 5월)

- Edge Runtime export 미지원 → Vercel용 코드를 그대로 옮기면 일부 라우트가 Node runtime에서만 돈다.
- Workers 스크립트 크기: Free 3MiB / Paid 10MiB. 큰 의존성(예: Prisma engine, Sharp)은 빠지거나 다른 방식 필요.
- `use cache` (composable caching)는 다음 메이저 릴리즈에 예정.
- 좋아진 점: crypto/dns/timers/tls/net 등 핵심 Node 모듈이 Workers runtime에 native로 들어옴, 나머지는 polyfill.

### 6.3 이미지 최적화

- **Cloudflare Images**: 5,000 transforms/월 무료, 이후 $0.50/1,000. 외부 origin(R2/S3/직접) 사용 시 transform 비용만 ([Cloudflare Images Pricing](https://developers.cloudflare.com/images/pricing/)).
- Vercel Image Optimization 대비 큰 폭 저렴. AWS+자체 구축이 가장 저렴할 수 있지만 운영 비용 고려 시 Cloudflare Images가 균형점.

### 6.4 Vinext (2026)

- Cloudflare가 직접 만드는 Vite 플러그인 형태 Next 호환 어댑터 ([cloudflare/vinext](https://github.com/cloudflare/vinext)). OpenNext와 별개의 실험적 라인. 책 시점에 따라 추적 필요.

---

## 7. 보안·인증·네트워크

### 7.1 Cloudflare One / Zero Trust 스택

- **Access**: SaaS·자체 앱 앞단에 SSO + 정책 + device posture. OIDC/SAML 다양 IdP, 브라우저 기반 SSH/VNC 같은 개발자 친화 기능 ([Zero Trust Access Compared](https://inventivehq.com/blog/cloudflare-access-vs-aws-verified-access-vs-azure-entra-vs-google-beyondcorp)).
- **Tunnel (cloudflared)**: 사설망에 outbound-only 터널. EC2 private subnet도 cloudflared 띄우면 외부 노출 없이 접근 가능 ([Zero Trust EC2](https://blog.saintmalik.me/cloudflare-zero-trust-security-ec2/)).
- **Gateway**: DNS·HTTP 필터링.
- **CASB**: SaaS 보안.

### 7.2 WAF / Bot / Turnstile / API Shield

- 통합 패턴: 네트워크 레이어(WAF + Bot Management) + 클라이언트 시그널(Turnstile) ([Integrate Turnstile, WAF & Bot Management](https://developers.cloudflare.com/turnstile/tutorials/integrating-turnstile-waf-and-bot-management/)).
- API Shield: schema validation + mTLS for trusted clients.
- Turnstile은 대체로 **invisible challenge** — 일반 사용자에게 CAPTCHA UI 안 보여줌.

### 7.3 Workers 인증 라이브러리 패턴

- **Auth.js (NextAuth)**: Next.js + OpenNext 환경에서 가장 무난.
- **Lucia**: Workers·Edge 친화적 minimal auth. DB는 D1 또는 Postgres(via Hyperdrive).
- **Clerk**: SaaS형, 빠른 도입. 비용은 사용자 수 비례.
- **자체 구현**: Hono + JWT + KV(세션) 패턴이 가장 가볍지만, refresh token rotation 등은 직접 책임.

---

## 8. AI·서버리스 신영역

### 8.1 Workers AI vs Bedrock

- Workers AI는 **edge에서 inference**. Cloudflare GPU 인프라에서 LLM·임베딩·이미지 모델 직접 실행. Neuron 단위 과금 ([Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)).
- Bedrock은 region 내 inference 서비스. 모델 카탈로그(Anthropic, Cohere, Mistral, Titan 등) 풍부, enterprise 기능(VPC endpoint, Model evaluation, Knowledge Bases) 다양.
- 선택 기준: latency-critical edge 호출 → Workers AI. 컴플라이언스·VPC 격리·강한 enterprise feature → Bedrock. Anthropic Claude를 **Sonnet 최신** 같은 형태로 빠르게 쓰려면 둘 다 가능.

### 8.2 Vectorize vs OpenSearch / pgvector

| 기준 | Vectorize | pgvector | OpenSearch |
|---|---|---|---|
| 위치 | edge 분산 | 기존 Postgres 안 | 별도 클러스터 |
| 통합 | Workers/AI Gateway 즉시 | SQL/RDB와 트랜잭션 | full-text + vector |
| 한계 | hybrid search 미지원 | 단일 DB 스케일 한계 | 운영 복잡도 |

### 8.3 AI Gateway

- LLM 트래픽 프록시. 70+ 모델, 12+ provider ([AI Gateway features](https://developers.cloudflare.com/ai-gateway/features/)).
- 캐싱: 동일 요청 글로벌 캐시 → 90%까지 지연 감소.
- Rate limit, retries, fallback, cost·token 분석.
- Bedrock·Portkey·자체 게이트웨이와 비교 시 **observability + 캐싱이 한 제품에서** 되는 게 강점 ([LLM Prompt Caching 비교](https://www.antstack.com/blog/comparison-of-llm-prompt-caching-cloudflare-ai-gateway-portkey-and-amazon-bedrock/)).

### 8.4 Agentic 신영역 (2026)

- **Dynamic Workers (open beta, 2026)**: AI agent의 untrusted code 실행을 위한 isolate 기반 sandbox. 컨테이너 기반(Firecracker)보다 100x 빠른 시작 ([Dynamic Workers](https://www.infoq.com/news/2026/04/cloudflare-dynamic-workers-beta/)).
- **Agents API**: Cloudflare 자체 agent 프레임워크. Queues + Workflows + DO를 묶어 멀티 step agent 구성.

---

## 9. 비용·성능 실무

### 9.1 가격 모델의 핵심 차이

- Lambda는 **GB-s × duration** + 요청 수. I/O 대기 동안에도 메모리 lock.
- Workers Standard는 **CPU time × 요청 수**. **외부 API/DB 응답 대기 시간은 무료** ([Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/)).
- 의미: AI 호출·외부 API·DB 쿼리 위주 워크로드일수록 Workers 가격 우위가 커진다.

### 9.2 실측 사례

- **Baselime**: AWS Lambda + ECS → Workers 풀 마이그레이션, 3명·3개월 미만. AWS Lambda 비용 -85%, 정규 가격 적용 시 일 $790 → $25, **95% 절감** ([Baselime case](https://blog.cloudflare.com/80-percent-lower-cloud-cost-how-baselime-moved-from-aws-to-cloudflare/)).
- **TechPreneur startup**: Lambda 월 $7,000 (invocations + API Gateway $2,100 + CloudWatch $600 + data transfer $1,100) → Workers 마이그레이션으로 연 ~$50,000 절감 ([TechPreneur Medium](https://techpreneurr.medium.com/from-aws-lambda-to-cloudflare-workers-our-50k-annual-savings-story-7dcd1851d44c)) [unverified — 개인 블로그, 정확한 트래픽 형상 검증 어려움].
- **Rebal AI**: Workers와 Lambda 동시 운영. Lambda@Edge 콜드스타트 동남아·남미에서 400~600ms, Workers는 글로벌 균일 ([Rebal AI](https://blog.rebalai.com/en/2026/03/09/cloudflare-workers-vs-aws-lambda-which-edge-runtim/)).
- **반대 사례 — Liftosaur**: Workers → Lambda 회귀. 이유: KV는 secondary index·range query 없음, Node 라이브러리 못 씀, 1MB 스크립트 한도, KV backup 어려움 ([Liftosaur](https://www.liftosaur.com/blog/posts/how-i-moved-liftosaur-from-cloudflare-workers-to-lambda/)).

### 9.3 egress free의 의미와 한계

- 의미: 미디어·백업·AI 모델 가중치 등 outbound 큰 워크로드에서 압도적 절감.
- 한계: Class A operations(쓰기/list)·Class B(읽기)는 과금. 요청 수가 매우 많으면 결국 비용 누적.
- 또 한계: AWS 다른 서비스에서 R2로 데이터를 보내는 inbound는 AWS egress로 잡힘. 옮길 때 한 번 큰 청구서가 올 수 있다.

### 9.4 Workers AI / Vectorize 가격 감각

- Workers AI: $0.011/1k Neurons, 일 10k Neurons 무료. Llama 3.1 8B 1k 토큰 ≈ 약 X Neurons (모델별 환산 표는 공식 페이지 확인 필요).
- Vectorize: 무료 plan 한도 내에서는 hobby·MVP에 충분. 스케일 시 인덱스·query 단위 과금.

---

## 10. 마이그레이션 전략

### 10.1 권장 순서 (Strangler Fig 패턴 적용)

1. **DNS 이전**: 우선 Cloudflare DNS로 옮기기. 트래픽 자체는 그대로 AWS origin으로. 위험 거의 없음.
2. **CDN/WAF 단**: Cloudflare 앞단에서 캐시·WAF·Bot Management 적용. CloudFront 비용·Lambda@Edge 일부를 Cloudflare로 흡수.
3. **사설망 노출 제거**: ALB의 public 노출을 Cloudflare Tunnel로 대체.
4. **에지 로직**: Lambda@Edge / CloudFront Functions에 있는 헤더 조작·A/B 테스트·인증 검증 → Workers로 이전 (콜드스타트 이득).
5. **API gateway 흡수**: 새 엔드포인트는 Workers Routes + Hono로. 기존 API Gateway는 점진적 제거.
6. **상태 없는 Lambda**: 의존성 가벼운 Node Lambda → Workers로 포팅.
7. **데이터 — 가장 마지막**: S3 → R2 (egress 큰 버킷부터), DynamoDB → KV/D1/DO (사용 패턴별 분리), RDS는 그대로 두고 Hyperdrive 앞에 두기.
8. **AI**: Bedrock 호출에 AI Gateway를 앞단으로 넣어 캐싱·관측. 점차 적합한 모델은 Workers AI로.

### 10.2 하이브리드 패턴 (현실적인 권장)

- **DB는 AWS, 컴퓨트는 Cloudflare**: Hyperdrive로 RDS/Aurora를 그대로 사용. 큰 데이터 자산을 옮기지 않고도 edge 이득 확보.
- **Heavy job은 ECS/Fargate, edge·API는 Workers**: 30s 이상 걸리는 batch나 GPU 추론은 AWS, 사용자 facing 경로는 Cloudflare.
- **Backup은 R2, primary는 S3 (또는 그 반대)**: 점진적 전환 + 비용 비교.

### 10.3 가상 시나리오 — Spring + Lambda + DynamoDB + S3 스택의 점진 이전

**현재 스택 가정**:
- Spring Boot API on ECS Fargate (Java 21, RDS Aurora Postgres 연결)
- 일부 image-resize Lambda (Node + Sharp)
- DynamoDB (사용자 세션)
- S3 (사용자 업로드 미디어, 매월 30TB 다운로드)
- CloudFront + Route 53 + WAF
- 월 비용 ~$8,000 (egress·CloudWatch·Lambda 포함)

**4단계 이전 시나리오**:

| Phase | 목표 | 작업 | 위험 | 예상 효과 |
|---|---|---|---|---|
| 0주 | DNS 이전 | Route 53 → Cloudflare DNS, proxy off로 시작 → on 단계적 | 낮음 | DNS query 비용 감소, lookup 속도 향상 |
| 2주 | 미디어 이전 | S3 → R2 동기 (rclone), CloudFront → Cloudflare CDN | 중간 (cache 동작 검증) | 월 $2,700 → $200 (egress 90%+ 절감) |
| 6주 | Edge 로직 | image-resize Lambda → Cloudflare Images + Worker | 낮음 (별도 endpoint) | Lambda·CloudWatch 비용 감소 |
| 10주 | 세션·인증 | DynamoDB 세션 → Workers KV (TTL + per-key 1 write/s OK) | 낮음 | DDB on-demand 비용 절감 |
| 16주 | API 부분 이전 | Spring Boot 일부 stateless endpoint → Workers + Hono. RDS는 Hyperdrive로 그대로 사용 | 중간 (런타임 차이) | 콜드스타트·EC2 비용 감소 |
| 24주+ | Heavy job 유지 | batch·report·long-running은 ECS 유지 | — | 하이브리드 안정 운영 |

**유지해야 할 것**:
- Spring Boot 모놀리스의 핵심 도메인은 그대로 ECS. JVM·Spring DI·트랜잭션 모델을 한 번에 옮기지 않는다.
- RDS Aurora를 그대로 두고 Hyperdrive 앞단으로 — 가장 risk-low한 컴퓨트 이전 패턴.

**계량 지표**:
- 월 비용 $8,000 → 추정 $2,500~$3,500 (egress 절감이 가장 큼).
- p95 응답시간: CDN+Workers 도입 후 해외 사용자 -200~400ms (Argo 경로 + edge SSR).

### 10.4 흔한 함정

- **Vendor lock-in 인식**: Workers 코드 자체는 Web standards라서 이론적으로 portable. 실제로는 Bindings·DO·D1·KV API가 Cloudflare 고유 → 옮기려면 추상화 레이어 필요. Cloudflare는 공식적으로 "no lock-in"을 강조하지만 커뮤니티는 "feature-level lock-in이 명백하다"고 본다 ([HN 29356036](https://news.ycombinator.com/item?id=29356036)).
- **Observability 공백**: CloudWatch 대비 단일 제품 부재. Logpush + 외부 APM(Datadog, New Relic, Baselime, Axiom, Sentry) 조합이 필수.
- **2025년 11월 18일 대규모 장애**: Bot Management config 파일이 ClickHouse 권한 변경으로 2배 크기가 되어 proxy panic. Workers KV·Turnstile·Dashboard까지 영향, 11:20~17:06 UTC 동안 부분/전체 장애 ([2025-11-18 Outage](https://blog.cloudflare.com/18-november-2025-outage/)). 단일 벤더 의존 위험에 대한 대비책은 책에서 반드시 다뤄야 한다.
- **Pages → Workers 전환의 도메인 스위칭**: 공식 문서 가이드가 부족하다는 평 ([Alex Zappa](https://alex.zappa.dev/blog/cloudflare-pages-to-workers-migration/)).

---

## 11. 커뮤니티 논쟁점·실패 사례

### 11.1 "Workers는 production-ready인가" 논쟁

- **긍정**: "관리 안 해도 되는 영역이 늘어나서 build에 집중할 수 있다", "콜드스타트가 없는 게 production UX에서 큰 차이" ([HN 35526356](https://news.ycombinator.com/item?id=35526356)).
- **부정**:
  - 2025년 두 차례 글로벌 outage(11/18, 12/5). 단일 벤더에 너무 많은 트래픽 집중 위험 ([HN 46162656](https://news.ycombinator.com/item?id=46162656), [HN 45973709](https://news.ycombinator.com/item?id=45973709)).
  - V8 보안 패치를 Chrome stable보다 먼저 production에 배포하는 정책 — 일부 개발자는 "더 빠른 보안", 일부는 "검증 안 된 패치" ([HN 46458963](https://news.ycombinator.com/item?id=46458963)).
  - Framework 호환성: 2025년 4월 Vite plugin 발표 시 React Router만 지원, Next.js 미지원, Astro는 6.0 베타에서야 추가 ([Pages Workers Again](https://www.brycewray.com/posts/2025/11/pages-workers-again-revisited/)).

### 11.2 초기 도입자 실패 사례

- **Liftosaur**: KV 한계(secondary index/range/backup 부재) + Node 라이브러리 부재(이미지 처리) + 1MB 스크립트 한도 → DynamoDB로 회귀, Lambda layers로 의존성 해결 ([Liftosaur](https://www.liftosaur.com/blog/posts/how-i-moved-liftosaur-from-cloudflare-workers-to-lambda/)).
- **velopert (veltrends)**: Cloudflare Pages로 처음 배포(무료 + 트래픽 증가에도 무료 유지), 성능 이슈로 Vercel로 이전 ([velopert blog](https://velog.io/@velopert/veltrends-dev-review)) — Cloudflare Pages SSR의 Node 호환성 한계가 원인으로 보임.

### 11.3 한국 커뮤니티 의견 정리

- **리디(RIDI)**: CloudFront 대체가 아니라 보완 — 해외 트래픽·Argo Smart Routing 가치 인정. 도입 후 해외 leg 지연 개선 ([RIDI 도입 후기](https://ridicorp.com/story/cloudflare-dos-and-donts/)).
- **velog "aws...? cloudflare! 그는 신인가?"**: Cloudflare + Hono + Drizzle + D1 조합이 압도적으로 편하다는 후기. DDoS 방어·WAF·Zero Trust 기본 포함이라 "DDoS 청구서 폭탄" 걱정 없음 ([velog](https://velog.io/@doublezeroman/aws-cloudflare)).
- **marinesnow34** (개인 기술블로그): Workers의 가장 큰 제약으로 (1) Express·AWS SDK 그대로 못 씀, (2) 50ms CPU 한도 시절의 이미지 최적화 불가 — 두 가지를 꼽음 ([marinesnow34](https://marinesnow34.github.io/2024/04/25/worker1/)). (※ 50ms는 옛 Bundled 모델 한도. 현재는 Standard 모델로 더 유연.)
- **clien**: 청원수 사이트 같은 트래픽 스파이크 프로젝트에서 무료 Workers 한도가 충분, 100만 요청 $0.30 수준에 만족.

### 11.4 자주 인용되는 외부 비교 (D1 vs Planetscale vs Neon vs Turso)

- D1: SQLite·간편함·통합·낮은 write throughput.
- Planetscale: 2024년 4월부터 무료 tier 폐지. write 성능 우수, branching DX 강점.
- Neon: serverless Postgres, scale-to-zero, project당 0.5GB 무료, 100 project까지.
- Turso: libSQL(SQLite fork) 분산, 무료 5GB. 2025년 1월 신규 가입자 scale-to-zero 폐지 → always-on.
- 책 권장 의사결정: "내 워크로드가 Workers 안에서 닫혀 있고 SQLite로 충분한가" → D1. "Postgres 생태계·고급 인덱스·확장이 필요" → Neon (Hyperdrive 통해). "MySQL + branching DX" → Planetscale.

---

## 12. 출처 목록

### 공식 문서
- [Cloudflare Workers Overview](https://developers.cloudflare.com/workers/)
- [Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- [Workers Limits](https://developers.cloudflare.com/workers/platform/limits/)
- [Workers Security Model](https://developers.cloudflare.com/workers/reference/security-model/)
- [Choosing a data or storage product](https://developers.cloudflare.com/workers/platform/storage-options/)
- [Durable Objects Overview](https://developers.cloudflare.com/durable-objects/)
- [Durable Objects: What are they](https://developers.cloudflare.com/durable-objects/concepts/what-are-durable-objects/)
- [Use WebSockets with Durable Objects](https://developers.cloudflare.com/durable-objects/best-practices/websockets/)
- [Workers KV](https://developers.cloudflare.com/kv/)
- [D1 (in storage options page)](https://developers.cloudflare.com/workers/platform/storage-options/)
- [R2 vs S3 (Cloudflare 비교 페이지)](https://www.cloudflare.com/pg-cloudflare-r2-vs-aws-s3/)
- [Hyperdrive how it works](https://developers.cloudflare.com/hyperdrive/concepts/how-hyperdrive-works/)
- [Hyperdrive connection pooling](https://developers.cloudflare.com/hyperdrive/concepts/connection-pooling/)
- [Hyperdrive AWS RDS Aurora](https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/aws-rds-aurora/)
- [Cloudflare Queues](https://developers.cloudflare.com/queues/)
- [Cloudflare Workflows](https://developers.cloudflare.com/workflows/)
- [Workers Containers](https://workers.cloudflare.com/product/containers)
- [AI Gateway](https://developers.cloudflare.com/ai-gateway/)
- [AI Gateway Caching](https://developers.cloudflare.com/ai-gateway/features/caching/)
- [Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Vectorize Overview](https://developers.cloudflare.com/vectorize/)
- [Cloudflare One Overview](https://developers.cloudflare.com/cloudflare-one/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- [Cloudflare Tunnel on AWS deploy guide](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/deployment-guides/aws/)
- [Turnstile + WAF + Bot Management](https://developers.cloudflare.com/turnstile/tutorials/integrating-turnstile-waf-and-bot-management/)
- [Workers Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Wrangler install](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- [Wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/)
- [Workers TypeScript](https://developers.cloudflare.com/workers/languages/typescript/)
- [Cloudflare Images Pricing](https://developers.cloudflare.com/images/pricing/)
- [Workers Logs](https://developers.cloudflare.com/workers/observability/logs/)
- [Workers Logpush](https://developers.cloudflare.com/workers/observability/logs/logpush/)
- [Cloudflare Workers Routes](https://developers.cloudflare.com/workers/configuration/routing/routes/)
- [Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [Cache API](https://developers.cloudflare.com/workers/runtime-apis/cache/)
- [Migrate from Pages to Workers](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/)

### Cloudflare 블로그·엔지니어링
- [Mitigating Spectre and Other Security Threats](https://blog.cloudflare.com/mitigating-spectre-and-other-security-threats-the-cloudflare-workers-security-model/)
- [Workers: the Fast Serverless Platform](https://blog.cloudflare.com/cloudflare-workers-the-fast-serverless-platform/)
- [New Workers pricing — never pay to wait on I/O](https://blog.cloudflare.com/workers-pricing-scale-to-zero/)
- [Workflows GA: production-ready durable execution](https://blog.cloudflare.com/workflows-ga-production-ready-durable-execution/)
- [Building Workflows: Durable Execution on Workers](https://blog.cloudflare.com/building-workflows-durable-execution-on-workers/)
- [Workers Durable Objects Beta](https://blog.cloudflare.com/introducing-workers-durable-objects/)
- [Pools across the sea: Hyperdrive free](https://blog.cloudflare.com/how-hyperdrive-speeds-up-database-access/)
- [Building Vectorize](https://blog.cloudflare.com/building-vectorize-a-distributed-vector-database-on-cloudflare-developer-platform/)
- [OpenNext Cloudflare adapter announcement](https://blog.cloudflare.com/deploying-nextjs-apps-to-cloudflare-workers-with-the-opennext-adapter/)
- [Baselime moved from AWS to Cloudflare](https://blog.cloudflare.com/80-percent-lower-cloud-cost-how-baselime-moved-from-aws-to-cloudflare/)
- [Improving Workers Types](https://blog.cloudflare.com/improving-workers-types/)
- [Automatically generated types](https://blog.cloudflare.com/automatically-generated-types/)
- [Hono on Cloudflare (founder story)](https://blog.cloudflare.com/the-story-of-web-framework-hono-from-the-creator-of-hono/)
- [2025-11-18 Outage post-mortem](https://blog.cloudflare.com/18-november-2025-outage/)
- [Python Workers redux](https://blog.cloudflare.com/python-workers-advancements/)
- [Benchmarking Edge Network Performance](https://blog.cloudflare.com/benchmarking-edge-network-performance/)
- [Secrets and Environment Variables to Workers](https://blog.cloudflare.com/workers-secrets-environment/)
- [Cloudflare Secrets Store](https://blog.cloudflare.com/secrets-store/)
- [Workers Logpush GA](https://blog.cloudflare.com/workers-logpush-ga/)
- [Introducing Cloudflare Queues](https://blog.cloudflare.com/introducing-cloudflare-queues/)

### 비교·분석 글
- [OpenNext Cloudflare](https://opennext.js.org/cloudflare)
- [3 Years of OpenNext](https://opennext.js.org/news/2026-03-25-3-years-of-opennext)
- [Workers vs Lambda 2026 (Morph)](https://www.morphllm.com/comparisons/cloudflare-workers-vs-lambda)
- [Workers vs Lambda Edge: Six Months of Production (Rebal AI)](https://blog.rebalai.com/en/2026/03/09/cloudflare-workers-vs-aws-lambda-which-edge-runtim/)
- [Cold Start Comparison (Ddosify)](https://medium.com/ddosify/cold-start-comparison-of-aws-lambda-and-cloudflare-workers-a3f9021ee60a)
- [Workers vs Lambda Edge Computing (ZeonEdge)](https://zeonedge.com/blog/cloudflare-workers-vs-aws-lambda-edge-computing-comparison)
- [Workers V8 Isolates 100x Faster (Kunal Ganglani)](https://www.kunalganglani.com/blog/cloudflare-workers-v8-isolates-ai-agents)
- [R2 vs S3 (digitalapplied)](https://www.digitalapplied.com/blog/cloudflare-r2-vs-aws-s3-comparison)
- [R2 vs Big 3 (yconsulting)](https://yconsulting.substack.com/p/cloudflare-r2-vs-the-big-3-a-deep)
- [DNS comparison (mechcloud)](https://dev.to/mechcloud_academy/cloudflare-dns-vs-aws-route-53-comprehensive-comparative-report-13mk)
- [DNS comparison (spendbase)](https://www.spendbase.co/blog/cloud/amazon-route-53-vs-cloudflare-dns-which-one-fits-your-stack/)
- [Containers vs ECS Fargate vs others (inventivehq)](https://inventivehq.com/blog/cloudflare-containers-vs-aws-ecs-eks-vs-azure-aks-vs-google-gke-comparison)
- [Cloudflare Containers Pricing comparison (HAMY)](https://hamy.xyz/blog/2025-04_cloudflare-containers-comparison)
- [Sliplane: Cloudflare Containers everything to know](https://sliplane.io/blog/cloudflare-released-containers-everything-you-need-to-know)
- [Durable Execution Showdown (Medium)](https://medium.com/@rajaravivarman/durable-execution-showdown-aws-lambda-durable-functions-vs-temporal-vs-cloudflare-workflows-6a7785b851b4)
- [LLM Prompt Caching: AI Gateway vs Portkey vs Bedrock (AntStack)](https://www.antstack.com/blog/comparison-of-llm-prompt-caching-cloudflare-ai-gateway-portkey-and-amazon-bedrock/)
- [pgvector vs OpenSearch (Instaclustr)](https://www.instaclustr.com/education/vector-database/pgvector-vs-opensearch-for-vector-databases-5-differences-and-how-to-choose/)
- [D1 vs Neon vs PlanetScale (Bejamas)](https://bejamas.com/compare/cloudflare-d1-vs-neon-vs-planetscale)
- [Edge Database Benchmarks](https://dev.to/algoorgoal/edge-database-benchmarks-2eac)
- [Hono on Workers production API gateway](https://dev.to/young_gao/building-a-production-api-gateway-on-cloudflare-workers-with-hono-2lhg)
- [CDN comparison (inventivehq)](https://inventivehq.com/blog/cloudflare-vs-aws-cloudfront-vs-azure-cdn-vs-google-cloud-cdn-comparison)
- [Workers KV in Practice (eastondev)](https://eastondev.com/blog/en/posts/dev/20260422-cloudflare-workers-kv-guide/)
- [Thinking in Networks not Databases (Jilles Soeters)](https://jilles.me/thinking-in-networks-cloudflare-storage/)
- [Vantage: Workers vs Lambda new pricing](https://www.vantage.sh/blog/cloudflare-workers-vs-aws-lambda-cost)

### 학술·심화
- [arXiv 2502.15775 — Serverless Edge Computing: Taxonomy & Literature Review (2025)](https://arxiv.org/abs/2502.15775)
- [arXiv 2310.08437 — Cold Start Latency in Serverless: Systematic Review](https://arxiv.org/html/2310.08437v2)
- [arXiv 2105.04995 — Engineering and Benchmarking a Serverless Edge System](https://arxiv.org/abs/2105.04995v1)
- [arXiv 2104.14087 — LaSS: Latency Sensitive Serverless](https://arxiv.org/abs/2104.14087)
- [arXiv 2401.02271 — Seamless Serverless across Edge-Cloud Continuum](https://arxiv.org/abs/2401.02271)
- [arXiv 2111.06563 — Serverless Platforms on the Edge: Performance Analysis](https://ar5iv.labs.arxiv.org/html/2111.06563)
- [arXiv 2403.00515 — Are Unikernels Ready for Serverless on the Edge?](https://arxiv.org/html/2403.00515v1)
- [arXiv 2404.12621 — Research on WebAssembly Runtimes: A Survey](https://arxiv.org/html/2404.12621v1)
- [GWU SRDS19 — Challenges and Opportunities for Efficient Serverless at the Edge](https://www2.seas.gwu.edu/~gparmer/publications/srds19awsm.pdf)
- [InfoQ — Fine-Grained Sandboxing with V8 Isolates (Cloudflare)](https://www.infoq.com/presentations/cloudflare-v8/)
- [InfoQ — Cloudflare Dynamic Workers Open Beta (2026)](https://www.infoq.com/news/2026/04/cloudflare-dynamic-workers-beta/)

### 커뮤니티 (HN·Reddit·블로그)
- [HN 35526356 — "Workers production-ready" 토론](https://news.ycombinator.com/item?id=35526356)
- [HN 46458963 — V8 보안 패치를 Chrome stable보다 먼저 푸는 정책](https://news.ycombinator.com/item?id=46458963)
- [HN 46162656 — 2025-12-05 Outage 토론](https://news.ycombinator.com/item?id=46162656)
- [HN 45973709 — 2025-11-18 post-mortem 토론](https://news.ycombinator.com/item?id=45973709)
- [HN 45584281 — Workers CPU Performance Benchmarks](https://news.ycombinator.com/item?id=45584281)
- [HN 29356036 — "벤더 락인" 시각](https://news.ycombinator.com/item?id=29356036)
- [HN 29226841 — Workers self-host 가능 여부](https://news.ycombinator.com/item?id=29226841)
- [Liftosaur — Workers → Lambda 회귀 사례](https://www.liftosaur.com/blog/posts/how-i-moved-liftosaur-from-cloudflare-workers-to-lambda/)
- [TechPreneur — Workers 마이그레이션 $50K 절감](https://techpreneurr.medium.com/from-aws-lambda-to-cloudflare-workers-our-50k-annual-savings-story-7dcd1851d44c) [unverified]
- [Bryce Wray — From Pages to Workers (again) revisited](https://www.brycewray.com/posts/2025/11/pages-workers-again-revisited/)
- [Alex Zappa — Pages to Workers migration mess](https://alex.zappa.dev/blog/cloudflare-pages-to-workers-migration/)
- [Vibe Coding With Fred — Pages deprecated 2025 migration](https://vibecodingwithfred.com/blog/pages-to-workers-migration/)
- [Cogley.jp — Cloudflare Pages vs Workers 2026](https://cogley.jp/articles/cloudflare-pages-to-workers-migration)
- [Cloudflare Outage 11/18 Analysis (mgx.dev)](https://mgx.dev/blog/cloudflare1119)
- [Reliability lessons from 2025 Cloudflare outage (Gremlin)](https://www.gremlin.com/blog/reliability-lessons-from-the-2025-cloudflare-outage)
- [Saintmalik — Securing EC2 with Cloudflare Tunnel](https://blog.saintmalik.me/cloudflare-zero-trust-security-ec2/)

### 한국어
- [RIDI — Cloudflare 도입 후기 (Argo Smart Routing)](https://ridicorp.com/story/cloudflare-dos-and-donts/)
- [velog — aws...? cloudflare! 그는 신인가? (D1+Hono+Drizzle 후기)](https://velog.io/@doublezeroman/aws-cloudflare)
- [velog — Cloudflare Workers로 부동산 가격 체크](https://velog.io/@gh4777/CloudFlare-Workers%EB%A1%9C-%EB%B6%80%EB%8F%99%EC%82%B0-%EA%B0%80%EA%B2%A9-%EC%B2%B4%ED%81%AC%ED%95%98%EA%B8%B0)
- [velog — veltrends 개발 후기 (Pages → Vercel 이전)](https://velog.io/@velopert/veltrends-dev-review)
- [marinesnow34 — Workers vs Lambda 비교](https://marinesnow34.github.io/2024/04/25/worker1/)
- [bohyeon.dev — Cloudflare를 웹 애플리케이션 최고의 장소로](https://ktseo41.github.io/blog/log/making-cloudflare-for-web.html)
- [Morgenrøde — Cloudflare Workers 소개 / 서버리스 앱 개발](https://ryanking13.github.io/2020/07/26/introducing-cf-workers-1.html/)
- [bgpworks — Cloudflare Workers 서버리스](https://medium.com/bgpworks/cloudflare-workers-%EC%84%9C%EB%B2%84%EB%A6%AC%EC%8A%A4-4de0d9d6aeb2)
- [cro.sH — Workers Rust SDK 사용기](https://blog.cro.sh/posts/cloudflare-workers-rust/)

---

## 13. 리서치 한계 (커버하지 못했거나 깊이가 부족한 영역)

1. **arXiv·학술 논문**: V8 isolate-based serverless를 Cloudflare 자체 환경에서 정량 측정한 peer-reviewed 논문은 거의 없다 (Cloudflare는 자체 엔지니어링 블로그·InfoQ 발표가 사실상 1차 소스). edge serverless 일반론 논문은 Raspberry Pi·OpenWhisk 기반이 다수라 Workers 특정 결론을 내리기 어렵다.
2. **2026년 정확한 Workers 가격표**: Standard 모델 전환 이후 세부 단가는 Cloudflare 공식 페이지를 책 집필 시점에 직접 확인해야 한다. 본 레퍼런스에는 대표적 단가만 포함.
3. **Spring Boot 4 + GraalVM Native + Workers Containers**의 결합은 미디엄 글 1건 수준의 자료만 있고, 실무 사례는 빈약 ([CodeTalks Medium](https://medium.com/@tuteja_lovish/serverless-spring-boot-at-the-edge-deploying-spring-apps-to-cloudflare-workers-deno-for-bb4e584a2a30)). 책에서 실험적 섹션으로 다룰 가치는 있으나 권장 패턴까지 단언하기 어렵다.
4. **AWS PrivateLink ↔ Cloudflare 등가물**: 정확한 1:1은 없고, Tunnel + Mesh + Workers VPC의 조합으로 부분 대체. 운영 사례 자료가 부족하다.
5. **한국 커뮤니티 OKKY·디스크**: 검색에서 OKKY 게시글이 직접 노출되지 않았다. 한국 사례는 RIDI·velog 중심으로 보강했지만, 더 많은 현장 후기는 책 집필 시 직접 OKKY·페북 그룹 등에서 모을 필요가 있다.
6. **2025년 12월 5일 outage**: HN 토론은 확인했지만 Cloudflare 공식 post-mortem 본문까지 깊이 분석하지 못함. 책에서 인용 시 원문 확인 필요.
7. **Workers Containers GPU·대용량 RAM**: 2026 5월 시점 0.5 vCPU / 4GiB가 한계. 향후 변경이 빠를 영역이라 책 집필 직전 재확인 권장.
