# Cloudflare를 나의 클라우드로 — 저술 계획

- 슬러그: `cloudflare-developer-cloud` · 장르: `tech-book` · 저자: Toby-AI · delegation_mode: production
- 계획 작성: 2026-10-03 (book-planner). 근거: `01_reference.md`(2026-10-03 합성), `profiles/tech-book/*`
- 이 계획의 모든 가격·한도·상태는 **2026-10-03 기준**이다. 저술가는 수치를 옮길 때 반드시 `01_reference.md` §2·§7·§9를 다시 대조한다.

---

## 제목 후보

1. **『Cloudflare를 나의 클라우드로 — 정적 사이트부터 Spring 백엔드까지, 무료로 시작해 안전하게 운영하기』**
   톤: 동반자적·실전. 포지셔닝: "CDN 회사"로만 알던 Cloudflare를 자기 앱의 배포·운영 기반으로 쓰는 법. JS/TS와 JVM 개발자를 한 책에서 함께 받는다.
2. **『엣지에서 시작하는 1인 클라우드 — Workers·Tunnel·Zero Trust로 앱을 올리고, 잇고, 지키기』**
   톤: 기술 중심·간결. 포지셔닝: 1인·소규모 팀의 운영 플랫폼. 세 동사(올리기·잇기·지키기)가 책의 부 구성과 일치한다. 단점: "1인"이 팀 단위 독자를 밀어낼 수 있다.
3. **『Cloudflare 개발자 플랫폼 실전 — 무료 티어 극대화와 과금 방어까지』**
   톤: 실무 레퍼런스. 포지셔닝: 비용 관점이 가장 앞에 선다. 단점: 책의 절반인 Tunnel·JVM·Zero Trust가 제목에서 사라진다.

**추천:** 1번. 사용자 요청의 핵심 문장("자신이 만든 앱과 서비스를 배포하고 운영하는 클라우드로 사용")을 그대로 제목으로 옮겼고, 부제가 진행 축(정적 사이트 → Spring 백엔드)과 비용 축(무료로 시작 → 안전하게 운영)을 함께 담는다.

> **기각한 제목 방향:** "청구서 걱정 없이", "요금 폭탄 없는" 류의 약속형 제목은 쓰지 않는다. 2026-10-03 기준 Cloudflare에는 계정 전체를 덮는 하드 지출 상한이 없고(§2-3, C-23), R2는 무료 범위를 넘으면 차단이 아니라 과금된다(§2-4). 제목이 지킬 수 없는 약속을 하면 13장의 정직한 서술과 충돌한다. 부제의 "안전하게"는 "겹겹의 장치를 써서"라는 뜻이고, 본문이 그 범위를 정확히 밝힌다.

---

## 책 특성

- **장르:** tech-book (Toby 문체, 평어체·청유형)
- **분량:** 본문 14장 순수 산문 약 153,000자 + 부록 3종 산문 약 9,000자 = **약 162,000자**(코드·표·mermaid·인용 블록 제외). 코드·표를 포함한 실제 원고는 이보다 30~40% 길어진다.
- **분량 오버라이드:** 실습 코드가 많은 실용 기술서라 기본값(3,000~6,000자)을 넘긴다. 챕터당 순수 산문 **8,000~13,000자**, 소절(`###`) **5~8개**, **소절당 순수 산문 3,000자 상한**. 자수는 표·코드 블록·mermaid·인용 블록을 제외한 산문 기준이다 (scaffolds.md 스케일 규칙).
- **난이도:** 중급. 웹 백엔드나 프런트엔드로 실서비스를 한 번 이상 만들어본 개발자를 전제한다. 클라우드(AWS 등)를 깊이 알 필요는 없다.
- **대상 독자:** Java·Kotlin(Spring Boot)과 JS/TS·React·Next.js·Node.js로 개발해본 개발자. 사이드 프로젝트·사내 도구·작은 SaaS를 직접 배포·운영하려는 사람.
- **독자 여정:**
  - **진입 상태:** "Cloudflare는 DNS와 CDN을 무료로 주는 곳" 정도로 안다. Vercel·AWS·VPS 중 어디에 올릴지 고민하고, 무료라는 말에 끌리지만 "갑자기 큰 청구서가 오면?"이 불안하다. Spring 개발자는 "내 JVM 서버는 어디에 두지?"라는 질문에 답을 못 찾았다.
  - **출구 상태:** 정적 사이트 → API → 데이터 → 풀스택 앱 → 기존 Spring 백엔드 연결 → 외부 서비스 통합 → 보안·Zero Trust → 캐싱 → 비용 방어까지 직접 구성해 하나의 서비스를 출시할 수 있다. 무엇을 Cloudflare 안에 두고 무엇을 밖에 둘지 스스로 판단하고, 유료 계정에서도 겹겹의 장치로 비용 사고의 반경을 제한할 수 있다.
  - **각성 지점:** 3장(Workers는 Node 서버가 아니다 — JVM 습관이 깨지는 곳), 4장("DB 하나"라는 전제가 깨지는 곳), 13장(하드캡은 없다 — 알림과 차단은 다르다).

---

## 내러티브 아크

책은 **올리기 → 잇기 → 지키기 → 운영하기**의 네 부로 흐르고, 하나의 예제 서비스 `moim`(개발자 밋업 신청 서비스)이 장마다 자란다.

**1부 올리기(1~5장)**는 가장 작은 것부터 시작한다. 1장에서 Cloudflare 플랫폼의 지도와 "isolate–컨테이너–VM" 격리 스펙트럼을 펼쳐 독자가 앞으로 만날 제품들의 자리를 먼저 잡게 한다. 2장에서 정적 사이트와 React SPA를 Workers에 올리며 "Pages인가 Workers인가"라는 첫 혼란을 정리하고, 3장에서 API를 만들며 Workers 런타임이 JVM·Node 서버와 어떻게 다른지 몸으로 익힌다. 4장은 데이터와 상태의 선택지(D1·KV·Durable Objects·R2·Queues·Workflows)를 비교하며 "DB 하나에 스키마 하나"라는 익숙한 전제를 흔들고, 5장은 프런트를 Next.js(vinext)로 키우며 프레임워크 어댑터의 위험과 배포 파이프라인을 다룬다. 1부가 끝나면 독자는 Cloudflare 안에서만 돌아가는 완결된 서비스를 갖는다.

**2부 잇기(6~8장)**는 Cloudflare 밖으로 손을 뻗는다. 많은 독자에게는 이미 돌아가는 Spring Boot 서버가 있다. 6장에서 Cloudflare Tunnel로 포트를 열지 않고 그 서버를 세상에 내놓고, 7장에서 JVM 백엔드의 세 착지점(Tunnel 뒤 VM, Containers, Workers와 공유하는 외부 DB)을 비교한다. 8장은 결제·메일·DB·AI·IaC처럼 "안에서 할까, 밖에서 할까"를 매번 묻게 되는 통합 전략을 정리한다. 1부 다음에 2부를 두는 이유는, Cloudflare 안의 모델을 먼저 알아야 "무엇을 밖에 둘지"를 판단할 수 있기 때문이다.

**3부 지키기(9~10장)**는 만들어 연결한 것을 보호한다. 9장은 공개 앱의 방어(Turnstile·WAF·레이트 리미팅·시크릿·`workers.dev` 뒷문)를, 10장은 운영자와 내부 시스템을 위한 Cloudflare One(Access·Cloudflare One Client·서비스 토큰·Mesh)을 다룬다. 공개 표면을 먼저 막고 내부 경계를 다음에 세우는 순서다. 10장에서 Spring Security로 Access JWT를 검증하며 2부의 Spring 서버가 다시 등장한다.

**4부 운영하기(11~14장)**는 서비스를 오래 굴리는 문제다. 11장 캐싱은 성능과 비용이 동시에 걸린 주제라 4부의 입구에 둔다(Workers Cache를 켜면 오히려 과금되는 함정이 12·13장으로 이어진다). 12장은 무료 티어를 설계 전략으로 다루고, 13장은 유료 계정에서 하드캡 없이 비용을 방어하는 다층 장치를 실제 사고 사례와 함께 구현한다. 비용 이야기를 뒤에 몰아둔 것은 아니다 — 매 장에 "비용 메모" 박스를 두고, 처음으로 결제가 걸리는 4장(R2 구독)과 7장(Workers Paid·Containers)에는 최소 안전장치 박스를 미리 넣는다. 12·13장은 흩어진 비용 지식을 하나의 전략으로 묶는 자리다. 14장은 `moim`의 출시 점검을 따라 전 과정을 되짚고, 장애·단일 벤더 리스크와 베타 제품의 전망까지 정리하며 닫는다.

---

## 설계 근거

- **채택한 구조: "하나의 서비스가 자라는 4부 구성(올리기 → 잇기 → 지키기 → 운영하기)"**
  1. **사용자가 요청한 진행 축을 그대로 척추로 삼았다.** "간단한 웹사이트부터 웹 서비스와 앱, 기타 다양한 서비스"는 난이도 순서이자 아키텍처 성장 순서다. 예제 서비스 `moim`이 정적 사이트(2장) → API(3장) → 데이터(4장) → 풀스택(5장) → Spring 연결(6~7장) → 외부 통합(8장)으로 자라면, 독자는 제품 목록이 아니라 "다음에 무엇이 필요해지는가"의 순서로 제품을 만난다.
  2. **"어디에 무엇을 둘까"라는 판단을 가르치는 데 초점을 맞췄다.** 대상 독자는 코드를 쓸 줄 안다. 그들에게 부족한 것은 D1이냐 Hyperdrive냐, Containers냐 Tunnel 뒤 VM이냐, 존 캐시냐 Workers Cache냐 같은 선택 기준이다. 그래서 비교 대조형 장(4·7·11장)을 각 부의 핵심에 배치했다.
  3. **JVM 독자에게 진짜 답을 준다.** "Workers에는 JVM이 없다"는 사실을 3장에서 정면으로 다루고, 6장(Tunnel)·7장(Containers·Hyperdrive·Queues pull·R2 Java SDK)·8장(SMTP·Pulumi Java)·10장(Spring Security의 Access JWT 검증)에 걸쳐 Spring 서버가 서비스의 한 축으로 계속 등장하게 했다.
  4. **예제 서비스 `moim`을 쓰는 이유:** 개발자 밋업 신청 서비스는 정적 소개 페이지, 신청 폼(봇 방어 필요), 선착순 좌석(강한 일관성 필요), 발표 자료 업로드(객체 저장), 확인 메일(큐), 유료 티켓(외부 결제·웹훅), 운영자 화면(Zero Trust), 행사 페이지(캐싱), 기존 회원·정산 시스템(Spring)을 자연스럽게 요구한다. 커버리지 항목 대부분이 억지 없이 들어맞는다. 반대로 `moim`에 어색한 제품(Browser Run·Images·Workers AI·Vectorize)은 억지로 넣지 않고 "다른 쓰임" 사이드바로 뺀다 — 예제가 제품 쇼케이스로 변질되는 것을 막는 규칙이다.
- **기각한 대안 1: 제품별 카탈로그 구조** (Workers 장, D1 장, R2 장, Tunnel 장… 공식 문서 목차 순서) — 기각 사유: 공식 문서를 한국어로 다시 쓰는 책이 되고, 독자의 실제 질문인 "이 상황에서 무엇을 고를까"에 답하지 못한다. 무료 티어·과금 방어·외부 통합 같은 가로지르는 주제가 제품 장마다 조각나 흩어진다. 게다가 2026년에만 Pages→Workers, WARP→Cloudflare One Client, Browser Rendering→Browser Run 같은 개명·재편이 잇따랐다(§0) — 제품 카탈로그는 가장 빨리 낡는 구조다.
- **기각한 대안 2: 돈을 앞에 두는 구조** (1~2장에서 무료 한도와 과금 방어를 먼저 다루고 나서 개발로 진입) — 기각 사유: 실제 비용 사고의 원인(DO alarm 재등록 루프, 프리뷰마다 생기는 DO 인스턴스, D1 `ON CONFLICT` 누락으로 인한 쓰기 폭증, Workers Cache를 켜면 정적 자산까지 과금되는 구조)은 해당 제품을 알기 전에는 이해할 수 없는 이야기다. 앞에서 듣는 경고는 추상적인 공포만 남긴다. 대신 1장에 "돈의 지도" 첫 스케치, 매 장 "비용 메모", 첫 결제 지점(4장 R2, 7장 Workers Paid)에 최소 안전장치 박스를 두고, 12·13장에서 묶는 방식을 택했다.
- **기각한 대안 3: JS 트랙과 JVM 트랙의 분리** (같은 주제를 JS/TS 편과 Spring 편으로 나누거나 JVM을 부록으로) — 기각 사유: Workers 런타임은 어차피 JS/TS(Wasm 경유는 실용 경로가 아님)라 트랙을 나누면 내용이 겹친다. 더 중요한 것은 JVM 독자의 진짜 질문이 "Spring을 Workers로 옮기는 법"이 아니라 "Spring을 어디에 두고 Workers와 어떻게 잇는가"라는 아키텍처 질문이라는 점이다. 이 질문은 통합 서사 안에서만 답할 수 있다.
- **기각한 대안 4: Cloudflare One을 독립 부(3~4장 분량)로 확대** — 기각 사유: Gateway의 기업 트래픽 필터링·CASB·원격 브라우저 격리·전용 출구 IP는 1인·소규모 팀 개발자에게 과잉이고, 상당수가 유료 애드온(§3-6)이며 리서치 공백(§11 #6)도 크다. 독자에게 실제로 쓸모 있는 Access(관리자 화면·Spring 보호·서비스 토큰)·Cloudflare One Client·Mesh·Tunnel 사설 라우팅을 한 장(10장)에 압축하고, Tunnel과의 연결은 6장이 받친다.
- **사용자 문구 해석 메모:** 요청의 "Cloudflare one을 적용"은 제품명 Cloudflare One(Zero Trust)으로도, "Cloudflare 하나를 클라우드로"로도 읽힌다. 이 계획은 두 해석을 모두 덮는다 — 전자는 10장(+6장), 후자는 책 전체의 진행 축이다.

---

## 커버리지 매트릭스

| # | 필수 항목 | 주 담당 장 | 보조 장 | 비고 |
|---|---|---|---|---|
| 1 | 간단한 웹사이트 → 웹 서비스·앱 → 기타 서비스 (점진적 구축) | 2 → 3 → 4 → 5 | 6·7·8 | `moim`이 장마다 자란다(예제 상태 표 참조). 기타 서비스(메일·AI·Browser Run·Images)는 8장 + "다른 쓰임" 사이드바 |
| 2 | Cloudflare One 적용 (Access·Gateway·Cloudflare One Client·Mesh) | **10** | 6, 14 | 6장: Tunnel(Cloudflare One의 연결 축). 10장: Access 정책·좌석·IdP·서비스 토큰·Client·Gateway DNS 필터·Mesh·사설 호스트명 라우팅·SSH |
| 3 | 인증과 보안 (Access JWT·Turnstile·WAF·레이트 리미팅·시크릿) | **9, 10** | 5, 8 | 9장: Turnstile·WAF·레이트 리미팅·시크릿·`workers.dev`. 10장: Access JWT(Workers `ctx.access`·Node·Spring)·서비스 토큰·IdP. 5장: CVE 패치("WAF는 패치를 대체하지 않는다"). 8장: Stripe 웹훅 서명 검증 |
| 4 | 캐싱 | **11** | 2, 5, 13 | 2장: 정적 자산·캐시 헤더 기초. 5장: Next.js ISR/`"use cache"` 제약. 13장: Workers Cache 과금 함정 회수 |
| 5 | 무료 티어 극대화 | **12** | 1, 전 장 "비용 메모", 부록 A | "청구 대신 에러" 모델, R2 예외, 계정 분리, 가용성 트레이드오프 |
| 6 | 안전한 유료 사용·과금 제한 (하드캡 없음을 정직하게) | **13** | 4, 7 (최소 안전장치 박스), 부록 B | 알림 ≠ 차단 구분, `limits.*`, Budget alerts, Billable Usage API, AI Gateway spend limits, 자작 서킷 브레이커 |
| 7 | Cloudflare 밖 서비스와의 통합 전략 | **8** | 7, 14 | Hyperdrive(Neon·Supabase·PlanetScale·MySQL), R2 S3 호환, Stripe, 메일, AI Gateway, 출구 IP, IaC. 14장: 단일 벤더 리스크와 출구 전략 |
| 8 | Cloudflare Tunnel (`cloudflared`) | **6** | 7, 8, 10 | 7장: Spring 상시 운영 경로. 8장: 고정 출구 IP 우회(호스트명 라우팅). 10장: Access 결합·사설 라우팅·SSH |
| 9 | JVM 독자 적합성 (Java/Kotlin/Spring) | **7** | 3, 6, 8, 10 | 3장: JVM 멘탈 모델 vs isolate. 6장: Spring Boot를 Tunnel 뒤에. 7장: **Containers**(정산 배치)·**Tunnel** 상시 운영·**Hyperdrive**로 Postgres 공유·Queues HTTP pull 소비자·R2를 AWS SDK for Java v2로. 8장: Email SMTP(`JavaMailSender`)·Pulumi Java. 10장: **Spring Security로 Access JWT 검증**(JWKS·`aud`·키 회전) |

---

## 예제 서비스 `moim` — 고정 명세와 장별 상태

병렬 저술가가 같은 이름을 쓰도록 아래를 정전으로 삼는다. 여기 없는 이름이 필요하면 같은 규칙(소문자·하이픈, 바인딩은 대문자 스네이크)으로 짓고, 그 장 안에서만 쓴다.

**고정 명세**

| 항목 | 값 |
|---|---|
| 서비스 | `moim` — 개발자 밋업 신청 서비스 (행사 소개, 참가 신청, 선착순 좌석, 발표 자료 업로드, 유료 티켓, 운영자 화면) |
| 독자 도메인(존) | `example.com` (독자는 자기 도메인으로 바꿔 읽는다). 서브도메인은 **한 단계만** 쓴다 — 무료 Universal SSL 범위를 벗어나지 않게 |
| 웹 호스트 | `moim.example.com` — 프런트 Worker `moim-web` |
| API 경로 | `moim.example.com/api/*` — API Worker `moim-api` (Hono, TypeScript) |
| 운영자 화면 | `moim.example.com/admin/*` — 10장에서 Access로 보호 |
| Spring 서버 | `moim-core` — **Java·Spring Boot**, 회원·결제 정산 담당. 6장부터 VPS(또는 집 서버)에서 실행, 호스트 `core.example.com`으로 Tunnel 공개. 포트 `8080` |
| D1 | DB `moim-db`, 바인딩 `DB` (행사·신청 내역) |
| KV | 네임스페이스 `moim-config`, 바인딩 `CONFIG` (행사 설정·기능 플래그 — 드물게 바뀌는 값만) |
| Durable Objects | 클래스 `EventSeats`, 바인딩 `SEATS` (행사별 선착순 좌석 카운터, SQLite 백엔드) |
| R2 | 버킷 `moim-uploads`, 바인딩 `UPLOADS` (발표 자료). ⚠ `ASSETS`는 정적 자산 바인딩 이름이므로 쓰지 않는다 |
| Queues | `moim-mail`(바인딩 `MAIL_QUEUE`, Worker 소비자 — 확인 메일), `moim-settlement`(바인딩 `SETTLEMENT_QUEUE`, `moim-core`가 HTTP pull로 소비) |
| Workflows | `ReminderWorkflow`, 바인딩 `REMINDER` (행사 전날 리마인더) |
| Hyperdrive | 바인딩 `HYPERDRIVE` → 외부 Postgres(Neon). `moim-core`와 `moim-api`가 공유 |
| Containers | 클래스 `ReportContainer`, 바인딩 `REPORT` (`moim-core`의 정산 리포트 배치 이미지) |
| Email Sending | 바인딩 `EMAIL` (8장, Workers Paid 필요) |
| 레이트 리미팅 | 바인딩 `RATE_LIMITER` (9장) |
| 서킷 브레이커 | Worker `moim-guard` (13장, Cron + Billable Usage API + 기능별 카운터) |

**장별 종료 상태** (각 장 끝에서 존재하는 것)

| 장 | 종료 시점의 `moim` |
|---|---|
| 2 | `moim-web`: 정적 소개 페이지 + React SPA(Vite), `moim.example.com` 커스텀 도메인, `workers_dev: false` |
| 3 | `moim-api`(Hono): `GET /api/events`, `POST /api/events/:id/rsvp`(아직 메모리 목업), 로컬 테스트(`@cloudflare/vitest-plugin`), Workers Logs 켬 |
| 4 | `moim-api`에 `DB`·`CONFIG`·`SEATS`·`UPLOADS`·`MAIL_QUEUE`·`REMINDER` 연결. R2 구독(결제수단 등록)이 처음 생긴다. `moim-mail` 소비자는 아직 메일을 실제로 보내지 않는다 — 로그만 남기거나 검증된 자기 주소로만 보낸다(실제 발송은 8장의 `EMAIL`) |
| 5 | `moim-web`이 Next.js(vinext)로 전환 — 행사 상세 SSR, `moim-api`와 Service binding. Workers Builds + PR별 Preview. **`moim-web`은 계속 `wrangler.jsonc` + Wrangler 프로젝트로 둔다**(vinext는 Vite 플러그인이므로 Wrangler 경로로 배포). vinext 1.0 init이 `cf` 프로젝트(`cloudflare.config.ts`)를 기본으로 만든다는 사실은 5장 본문에서 밝히고, Wrangler 경로로 두는 구체 절차는 `(사실 확인 필요)`로 남겨 fact-checker가 판정한다. `cf` 전환은 전망 박스로만. 이후 장의 `limits.*`·CI 배포 명령은 모두 `wrangler.jsonc`·`wrangler deploy` 기준 |
| 6 | `moim-core`(Spring Boot)가 VPS에서 `cloudflared`(원격 관리 터널)로 `core.example.com`에 공개. Postgres는 아직 같은 VPS에 있다(7장에서 Neon으로 이전). `moim-core`는 10장 전까지 자체 Spring 인증(기존 로그인)으로 보호된 상태 — "열린 문"이 아니라 "Cloudflare가 아직 앞에서 지켜주지 않는 문"으로 서술. Quick Tunnel로 로컬 데모 |
| 7 | 계정이 **Workers Paid**로 전환. Postgres를 Neon으로 옮기고 `moim-core`·`moim-api`가 공유(Hyperdrive). `moim-settlement` 큐를 Spring이 HTTP pull. 정산 리포트 배치를 `ReportContainer`로. R2를 Java SDK로 읽기 |
| 8 | Stripe 유료 티켓 웹훅(`POST /api/webhooks/stripe`), `EMAIL`로 확인 메일, Terraform 또는 Pulumi(Java)로 리소스 정의, GitHub Actions(`wrangler-action`) |
| 9 | 신청 폼에 Turnstile + `siteverify`, Free Managed Ruleset 확인, Rate limiting rule 1개 + `RATE_LIMITER`, 시크릿 정리 |
| 10 | `/admin/*`와 `core.example.com`을 Access로 보호, `moim-core`가 Spring Security로 `Cf-Access-Jwt-Assertion` 검증, `moim-api`→`moim-core` 호출은 서비스 토큰, 팀원 SSH는 `cloudflared access ssh` |
| 11 | `moim-web`(행사 상세 SSR)에 Workers Cache 켬 — 신청 마감 시 `ctx.cache.purge({ tags })`로 태그 퍼지, 상태 문구 HTML은 `max-age` 60초. `moim-api`에는 켜지 않음(Service binding 호출 과금 회피). 행사 목록 API는 Cache API 30초. 존 캐시·Cache Rules·`CDN-Cache-Control`·invalidate는 Spring 오리진(`moim-core`) 경로에서 시연. *(2026-10-03 editor 갱신 — Worker가 그린 HTML은 존 캐시를 거치지 않으므로)* |
| 12 | `moim`의 월간 사용량 시뮬레이션 표 (Free로 어디까지 버티는가) |
| 13 | `moim-guard` 서킷 브레이커, Worker별 `limits`, 예산 알림 설정, AI Gateway spend limit |
| 14 | 전체 아키텍처 그림과 출시 점검 완료 |

> 예제 코드 분량 원칙: 장마다 "그 장의 새 개념"만 전체 코드로 보여주고, 앞 장에서 만든 부분은 생략 표시(`// ...앞 장과 동일`)로 줄인다. 전체 소스 저장소를 가정하지 않는다.

---

## 용어 표기

병렬 저술가 공통 기준이다. 제품명은 영문 공식 표기를 그대로 쓰고, 일반 개념은 한국어로 쓴다.

**명칭 변경 — 쓸 표기 / 쓰지 않을 표기 (§0)**

| 쓸 표기 | 쓰지 않을 표기 | 규칙 |
|---|---|---|
| **Cloudflare One Client** | WARP Client, WARP | 첫 등장 시 "Cloudflare One Client(구 WARP Client)", 이후 본명만 |
| **Cloudflare Mesh**, **Mesh node** | WARP Connector | 첫 등장 시 "Mesh node(구 WARP Connector)" |
| **Browser Run** | Browser Rendering | 첫 등장 시 "Browser Run(구 Browser Rendering)". 개명 월은 단정하지 않는다(C-12) |
| **Cloudflare Tunnel**(독립 제품, 대시보드 **Networking > Tunnels**) | "Zero Trust 메뉴 안의 Tunnel" | 사설망·VPN 대체 용도만 "Cloudflare One의 Tunnel 문서"로 언급 |
| **vinext**(Next.js 기본 권장), **OpenNext**(기존 앱 유지 경로) | "Next.js on Cloudflare = OpenNext" | vinext 상태는 C-1 권장 표현 |
| **Workers + 정적 자산**(새 사이트) | "새 사이트는 Pages로" | Pages는 "계속 지원되나 신규 비권장" |
| **Workers Sites**: 폐기(deprecated) | — | 새 프로젝트에 쓰지 않는다고만 언급 |
| **`@cloudflare/vitest-plugin`** | `@cloudflare/vitest-pool-workers` | |
| **Agents Week 2026**(2026년 4월) | "2026년 Developer Week" | 2026년 행사명은 Agents Week(4월·8월), Birthday Week(9월 28일~10월 2일) |
| **Kotlin/Wasm: Beta** | "Kotlin/Wasm stable" | |
| Worker 크기 한도 **비압축 64 MiB(Free·Paid 동일, 2026-09-04~)** | 3 MB / 10 MB / 15 MB | |
| `nodejs_compat`: compatibility date 2026-08-04 이상이면 **기본 켜짐** | "플래그를 꼭 넣어야 한다" | |
| `cloudflared proxy-dns`: **제거됨** | — | Cloudflare One Client·Mesh node로 대체 |

**핵심 용어**

| 용어 | 이 책의 표기 |
|---|---|
| Workers / Worker | 플랫폼은 "Workers", 배포 단위 하나는 "Worker"(영문). "워커"로 음차하지 않는다 |
| Durable Objects | 영문. 장 안 첫 등장 후 "DO" 약어 허용 |
| D1, KV, R2, Queues, Workflows, Hyperdrive, Containers | 영문 제품명. 일반 명사로 쓸 때는 "큐", "워크플로", "컨테이너" |
| 바인딩(binding) | "바인딩". Service binding은 "Service binding"(영문) |
| 정적 자산(static assets) | "정적 자산" |
| 존(zone) | "존". 처음 한 번 "도메인 단위의 설정 공간"으로 풀이 |
| 엣지 / 오리진 | "엣지", "오리진" |
| 콜드 스타트 | "콜드 스타트" |
| compatibility date | "호환성 날짜(compatibility date)" 첫 등장 후 "호환성 날짜" |
| Cloudflare One / Zero Trust | 제품군은 "Cloudflare One", 개념은 "제로 트러스트". 첫 등장 시 "Cloudflare One(Zero Trust)" |
| Access, Gateway, Turnstile, WAF | 영문 제품명 |
| 레이트 리미팅 | 개념은 "레이트 리미팅". WAF 기능은 "Rate limiting rule", Workers 기능은 "`ratelimit` 바인딩" |
| Workers Cache / Cache API / 존 캐시 | 세 경로를 이 이름으로 구분(11장) |
| 하드캡 | "계정 단위 지출 상한(하드캡)". 첫 등장 후 "하드캡" |
| Budget alerts / Billable Usage | "예산 알림(Budget alerts)", "Billable Usage 대시보드/API" |
| Free / Workers Paid | 요금제 이름은 영문 고정. "무료 플랜"은 Free, "유료 플랜"은 Workers Paid. 존 요금제(Free·Pro·Business)와 Workers Paid가 별개임을 1장에서 밝힘 |
| 서비스 토큰 | "서비스 토큰(service token)" |
| Quick Tunnel / Protected Quick Tunnel | 영문 |

**코드·서술 규약**

- **Workers 코드:** TypeScript. 프레임워크는 Hono(API)·vinext(Next.js)·Vite(SPA). Python Workers는 언급만.
- **설정 파일:** `wrangler.jsonc`(TOML 쓰지 않음). `compatibility_date`는 **`"2026-09-01"`로 통일** — `nodejs_compat`를 따로 넣지 않는다.
- **CLI:** Wrangler v4가 본문 기본. `cf` CLI는 전망 박스에만. 단 vinext 1.0의 init이 `cf`를 기본으로 쓴다는 사실은 5장에서 밝힌다.
- **Spring 예제:** **Java + Spring Boot**(Kotlin 사용자도 읽기 쉬운 수준으로). Spring Boot·Spring Security의 구체 버전은 레퍼런스에 없으므로 버전 의존 API를 피하고, 써야 하면 `(사실 확인 필요)`를 붙인다. *(사용자 판단 항목: Kotlin으로 바꿀 수 있음)*
- **저자 작성 예제 표시:** 공식 예제가 없는 코드(Spring Security의 Access JWT 검증, Containers 위 Spring Boot 이미지, `moim-guard` 서킷 브레이커)는 본문에 "공식 예제가 없어 직접 작성한 예제"라고 밝힌다.
- **날짜 표기:** 가격·한도·상태 뒤에 "({제품} 문서 2026-10-03 기준)" 또는 "(2026년 10월 기준)". 금액은 USD `$` 표기, 원화 환산은 하지 않는다.
- **고정 박스 이름(통일):**
  - `> **비용 메모**` — 그 장 기능의 무료 범위·과금 단위·초과 시 동작. 장당 1~2개.
  - `> **최소 안전장치**` — 처음 결제가 걸리는 4장·7장에만.
  - `> **다른 쓰임: {제품}**` — `moim`에 어울리지 않는 제품 소개.
  - `> **전망: {제품} ({상태}, 2026-10-03 기준)**` — 베타·비공개 베타 제품. 본문 지시가 아니라 전망으로만 서술하고 "빠르게 바뀔 수 있다"는 문구를 붙인다.
  - `> **논쟁: {질문}**` — 레퍼런스 §4 논쟁을 양쪽 관점 병기로 박스화할 때(12장 논쟁 F, 13장 논쟁 G). *(2026-10-03 editor 추가 — 저술 단계에서 생긴 형식을 정식 박스로 인정)*
  - 박스 표기 형식: 제목 줄(`> **제목**`) 다음 줄부터 본문(`> ...`). 제목 뒤 ` — ` 인라인 본문은 쓰지 않는다.
- **`### 이 장의 핵심`:** 개념 밀도가 높은 **3·4·7·10·11·13장에만** 둔다(3~5불릿, 헤딩 표기 고정). 나머지 장에는 두지 않는다.
- **그림:** mermaid, 캡션 `그림 N. {설명}`(장마다 1부터). 장별 권장 그림은 챕터 목록에 적었다.

---

## 교차 주제 담당표 (중복 방지)

한 주제는 한 장이 깊게 다루고, 나머지 장은 "N장 참조"로 한두 문장만 쓴다.

| 주제 | 담당 장 | 다른 장의 처리 |
|---|---|---|
| Pages → Workers 이전 박스, Workers Sites 폐기 | 2 | 언급만 |
| `workers.dev` 끄기(`"workers_dev": false`)와 WAF 우회 뒷문 | **9** | 2장: 설정 한 줄 + "이유는 9장". 13장: 체크리스트 항목으로만 |
| Workers 런타임 한도(CPU·메모리·6연결·시작 1초·64 MiB) | 3 | 13장은 `limits.*`를 비용 관점으로만 |
| 테스트(`@cloudflare/vitest-plugin`), 로컬 개발, remote bindings | 3 | — |
| D1·KV·DO·R2·Queues·Workflows 선택과 기초 | 4 | — |
| DO alarm "이미 있는지 확인 후 등록" 코드 | **4** (올바른 패턴) | 13장: $34,895 사례 분석에서 4장 코드를 회수 |
| KV 최종 일관성·전파 지연(C-25), KV Instant 전망 | 4 | 13장: 언급만 |
| vinext/OpenNext, CVE 패치, Smart Placement | 5 | 7장: Placement Hints만 |
| Workers Builds·Preview·`wrangler-action` | 5 (빌드·프리뷰), 8 (`wrangler-action`·IaC) | 13장: "프리뷰에서 DO 바인딩 빼기"만 |
| Quick Tunnel / Protected Quick Tunnel(`--allowed-mail`), `wrangler tunnel` | **6** | 8장: Stripe 웹훅 로컬 테스트에서 참조만 |
| Tunnel vs Tailscale vs ngrok (논쟁 C) | 6 | 10장: 한 문장 회수 |
| Hyperdrive 기본 설정(Spring과 공유) | **7** | — |
| Hyperdrive 공급자별 주의(Neon TCP 드라이버, Supabase direct, PlanetScale·MySQL `disableEval`) | **8** | — |
| R2 S3 호환(Java SDK v2 `chunkedEncodingEnabled(false)`) | 7 | 8장: JS SDK·Sippy·presigned URL |
| 고정 출구 IP 문제와 Tunnel 호스트명 라우팅 우회 | 8 | 10장: 사설 라우팅 관점으로 한 문장 |
| Turnstile, WAF Free Managed Ruleset, Rate limiting rule vs `ratelimit` 바인딩, 시크릿 | **9** | 13장: 비용 방어 층으로 참조만 |
| Access JWT 검증(Workers `ctx.access`·Node `jose`·Spring Security) | **10** | 6·7장: "10장에서 검증한다" 예고만 |
| "Make all Workers private by default", Require Access protection | 10 | 9장: 언급만 |
| Workers Cache의 과금 함정 | **11** | 2·12·13장: 한 문장 + "11장 참조" |
| 무료 티어 "청구 대신 에러" 표, R2 예외, 계정 분리 | **12** | 전 장 비용 메모는 해당 제품만 |
| 하드캡 부재, 예산 알림, Billable Usage API, Threshold billing, 서킷 브레이커, 사고 사례 | **13** | 1·12장: 결론 한 문장만 |
| 관측성(Workers Logs·Traces·OTel)과 2026-12-01 가격 전환 | 3 (켜기), 14 (운영), 13 (비용) | — |
| 장애와 단일 벤더 리스크 (논쟁 A) | **14** | 8장: 통합 원칙 한 문장 |
| 무료 티어 선의 vs 미끼 (논쟁 F) | 12 | — |

**충돌 원장(§7) 장별 배정** — 해당 장 저술가는 그 항목의 "책 권장 표현"을 따른다.
1장: C-28, C-33, C-23(결론만) · 3장: C-13, C-8 · 4장: C-3, C-4, C-5, C-10, C-11, C-22, C-25, C-34(Orleans), C-37 · 5장: C-1 · 6장: C-7, C-18, C-39 · 7장: C-8, C-16 · 8장: C-12, C-19, C-36, C-2(Vectorize 사이드바 시) · 9장: C-30 · 10장: C-29, C-32, C-35 · 11장: C-21, C-34(S3-FIFO) · 12장: C-6, C-37 · 13장: C-5, C-14, C-20, C-23, C-26(인용 금지), C-27 · 14장: C-24, §9 재확인 목록 전체

---

## 통권 변주 배정표

| 장 | 오프닝 기법 (소재) | 클로징 기법 | 스캐폴드 유형 |
|---|---|---|---|
| 1 | 정의 뒤집기 — "Cloudflare는 CDN 회사"라는 통념 뒤집기 | 열린 질문 — "이 지도에서 내 서비스는 어디에 놓일까?" | 개념 도입형 |
| 2 | 인용·일화 — r/CloudFlare "Help me understand Workers vs Pages (I'm confused!)" | 적용 과제 — 자기 사이트를 지금 올려보고 확인할 세 가지 | 문제-해결형 |
| 3 | 상황 가정 — Spring 개발자가 Worker에 static 캐시 맵과 스레드 풀을 만들려 한다 | 습관 대조표로 매듭 — "JVM에서의 습관 / Workers에서의 습관" | 개념 도입형 |
| 4 | 실패 장면 — 에러 0개로 조용히 실패한 KV 레이트 리미터(Kuryzhev) | 결정 플로차트로 닫기 — "이 데이터는 어디에?" mermaid | 비교 대조형 |
| 5 | 수사적 질문 — "Next.js를 Vercel이 아닌 곳에 올리면 무엇을 잃을까?" | 한 문장 여운 — 프레임워크는 바뀌고 어댑터는 늦는다 | 사례 분석형 |
| 6 | 상황 가정 — 금요일 저녁 데모, 집 서버의 Spring Boot를 외부에 보여줘야 한다 | 운영 명령 세 줄로 닫기 — 서비스 등록·7844 점검·버전 1년 규칙 | 문제-해결형 |
| 7 | 앞 장 콜백 — Tunnel로 꺼낸 Spring 서버, 그런데 서버 전원이 꺼지면? | 의사결정 표로 닫기 — 세 착지점 × 상황 | 비교 대조형 |
| 8 | 인용·일화 — HN "Too many ways to do the same thing, none of them great" | 원칙 한 줄 압축 — "밖에 둘 것은 표준 프로토콜로 잇는다" | 사례 분석형 |
| 9 | 실패 장면 — 커스텀 도메인 WAF를 우회해 `workers.dev`로 들어온 봇(white_viel) | 공격자 시점 되짚기 — 방어선을 공격자 경로로 다시 걷기 | 문제-해결형 |
| 10 | 정의 뒤집기 — "사내망 안이면 안전하다"를 NIST SP 800-207 문장으로 뒤집기 | 자가 진단 질문 세 개 — 우리 팀에 무엇이 필요한가 | 개념 도입형 |
| 11 | 인용·일화 — 배포 후 stale HTML, "you're always guessing which cache layer is the problem"(Manchitsanan) | 오해 정정으로 닫기 — "캐시를 켜면 싸진다"는 오해 | 비교 대조형 |
| 12 | 상황 가정 — `moim` 행사가 커뮤니티 1면에 올라 트래픽이 몰린다면 | 계산 결과로 닫기 — `moim` 월간 사용량 시뮬레이션 표 | 사례 분석형 |
| 13 | 충격적 수치·사실 — $34,895 청구서(결말 미확인 명시) | 오늘 밤 할 일 다섯 가지 + 부록 B 연결 | 문제-해결형 |
| 14 | 인용·일화 — GeekNews "Cloudflare가 안되어서 온갖 서비스가 중단되니 지옥이더군요.." | 닫는 매듭 — 여정 회고와 독자가 가져갈 관점 | 종합 정리형 |

**점검:** 인접 장 오프닝 중복 없음. 상황 가정 3회(3·6·12장) ≤ ⌊14/3⌋=4. 클로징 14종 모두 다름. 비교 대조형은 4·7·11장으로 서로 인접하지 않음. 마지막 장은 종합 정리형 + 닫는 매듭. "다음 장에서는 ~" 공식 클로징은 어느 장에도 배정하지 않았다 — 이음이 필요하면 클로징 기법 안에서 한 문장으로만.

---

## 챕터 목록

### 1부 올리기

### 1장. Cloudflare를 나의 클라우드로 — 지도부터 펼치기
- **핵심 질문:** CDN으로만 알던 Cloudflare 위에 내 앱 전체를 올린다는 것은 무슨 뜻이고, 무엇이 되고 무엇이 안 되는가?
- **주요 내용:**
  - 플랫폼 지도: 컴퓨트(Workers·Containers)·저장(KV·D1·DO·R2·Queues·Workflows·Hyperdrive)·네트워크와 보안(Tunnel·Cloudflare One·WAF·Turnstile·캐시) — §1-1. mermaid 플랫폼 지도
  - 격리 스펙트럼: isolate(Workers) – microVM(Firecracker 계열, Containers) – VM. New Kids 초록 인용(웜 지연 ~40ms → ~10ms, "limits the execution environment"), Shahrad "45%… once per hour or less" — 사이드 프로젝트 독자와의 연결 (C-28: 초록 문장만)
  - 요금 구조 첫 스케치: 존 요금제(Free·Pro·Business)와 Workers Paid($5/월 최소)는 별개, Free는 대부분 "청구 대신 에러", 계정 하드캡은 2026-10 기준 없다(결론 한 문장, 자세히는 13장)
  - JVM 개발자에게 미리 하는 정직한 말: Workers에는 JVM이 없다 — 그래도 이 책이 Spring 서버를 버리지 않는 이유(6·7·10장 예고)
  - 예제 서비스 `moim` 소개와 책의 네 부 구성
- **독자가 얻는 것:** 앞으로 만날 제품들의 위치와 서로의 관계, 요금 구조의 큰 틀, 이 책의 여정 지도.
- **오프닝 기법:** 정의 뒤집기
- **클로징 기법:** 열린 질문
- **스캐폴드 유형:** 개념 도입형
- **그림:** 플랫폼 지도, 격리 스펙트럼
- **예상 분량:** 8,000자

### 2장. 첫 배포 — 정적 사이트와 SPA를 Workers에 올리기
- **핵심 질문:** 새 사이트는 Pages인가 Workers인가? 무료·무제한 정적 자산을 어떻게 온전히 누리는가?
- **주요 내용:**
  - "Start new projects with Workers." — Pages 신규 비권장, Workers Sites 폐기의 배경(§0-6·0-7, §3-1)
  - C3(`npm create cloudflare`), `@cloudflare/vite-plugin`, Wrangler 4.68.0+의 `wrangler deploy` 자동 구성, `wrangler.jsonc` 기본 골격(호환성 날짜 규약)
  - React SPA: `assets.not_found_handling: "single-page-application"`로 Worker 호출 없이 무료 라우팅, `run_worker_first` 경로는 Worker 요청으로 계산된다는 점
  - 커스텀 도메인 연결, DNS를 Cloudflare로 옮기는 흐름, `"workers_dev": false` 한 줄(이유는 9장)
  - 기존 Pages 사용자 박스: 마이그레이션 가이드 요점과 현장 반응("following it is no walk in the park.")
  - 비용 메모: 정적 자산 무료·무제한, 파일 수 한도(Free 20,000 / Paid 100,000), Workers Cache를 켜면 정적 자산도 과금(11장 참조)
- **독자가 얻는 것:** `moim-web`을 자기 도메인으로 배포하고, 정적 자산이 무료로 남는 구성 원칙을 안다.
- **오프닝 기법:** 인용·일화
- **클로징 기법:** 적용 과제
- **스캐폴드 유형:** 문제-해결형
- **그림:** 요청이 정적 자산과 Worker로 갈라지는 경로
- **예상 분량:** 10,000자

### 3장. Workers 런타임 — JVM 개발자의 멘탈 모델 바꾸기
- **핵심 질문:** Workers는 왜 Node 서버도, Spring 서버도 아닌가? 그 차이를 알고 API를 어떻게 설계하는가?
- **주요 내용:**
  - isolate 모델: 요청마다 깨어나는 실행, 전역 상태를 믿지 않는 설계, 스레드 없음, 128 MB 메모리를 isolate 안의 동시 요청이 공유. Spectre 대응 박스(Schwarzl et al. ESORICS 2022 + Firecracker 인용 병기, 저자 순서는 출판본)
  - 웹 표준 API 코드라는 관점(ECMA-429 언급은 "2025년 12월 1판" 수준), `nodejs_compat` 기본 켜짐(호환성 날짜 2026-08-04 이상), `node:fs`, 폴리필 shim의 함정
  - `moim-api`를 Hono로: 라우팅, 요청 검증, Service binding 미리보기, 같은 존의 다른 Worker를 전역 `fetch()`로 부르면 실패한다는 제약
  - 한도와 에러: CPU(Free 10ms·Paid 기본 30초/최대 5분), Error 1102, 동시 대기 연결 6개(2026-04 완화), 시작 시간 1초, 크기 64 MiB(C-13)
  - 개발 루프: Wrangler v4 로컬 개발, remote bindings, `@cloudflare/vitest-plugin` 테스트, `observability.enabled`로 Workers Logs 켜기
  - Wasm 경로의 현실: Kotlin/Wasm Beta, TeaVM 실험의 한계 — "Spring을 Workers로 옮기는 길은 주력 경로가 아니다"
  - 전망 박스: `cf` CLI(2026-09-28 베타), Python Workers GA(2026-09-21)는 언급만
- **독자가 얻는 것:** Workers에서 안전하게 쓸 수 있는 코딩 습관과 피해야 할 JVM 습관, 테스트까지 갖춘 `moim-api`의 뼈대.
- **오프닝 기법:** 상황 가정
- **클로징 기법:** 습관 대조표로 매듭
- **스캐폴드 유형:** 개념 도입형
- **그림:** 요청-isolate 수명 주기
- **이 장의 핵심:** 둔다
- **예상 분량:** 11,000자

### 4장. 데이터와 상태 — D1·KV·Durable Objects·R2·Queues·Workflows 고르기
- **핵심 질문:** "DB 하나에 스키마 하나"에 익숙한 개발자는 엣지의 데이터 선택지를 어떻게 나눠 써야 하는가?
- **주요 내용:**
  - D1: SQLite 기반, DB당 Free 500 MB·Paid 10 GB(상향 불가), 2026-09-01부터 Free 일일 한도 초과 시 쿼리 실패. 트랜잭션이 여러 요청을 넘지 못한다는 한계, 인덱스 없는 풀 스캔 = rows read 과금. 논쟁 B(10 GB는 결함인가 설계인가 — kentonv 이해관계자 표기)
  - KV: 최종 일관성, 키당 초당 1회 쓰기, "느리게 바뀌는 설정"에만(C-25 권장 표현: 블로그 실측 p99 4.38초를 전형값으로, 상한 문구는 재확인 표시). 전망 박스: KV Instant(2026-10-01 비공개 베타, 쓰기 $0.10 "per operation" 경고)
  - Durable Objects: `EventSeats`로 선착순 좌석 — 강한 일관성이 필요한 곳. 신규 네임스페이스는 SQLite 전용(2026-07-09), Orleans와 "유사한 모델"(영감 단정 금지, C-34), 128 MB Duration 과금과 WebSocket Hibernation, **alarm은 `getAlarm()`으로 존재 확인 후 등록**(이 코드의 담당 장)
  - R2: S3 호환·이그레스 무료, 발표 자료 업로드, presigned URL. **R2 구독 체크아웃이 이 책에서 처음 결제수단을 요구하는 지점**
  - Queues(Free 포함, 일 10,000 ops, 메시지당 대개 3 ops)와 Workflows(step·storage 과금 예고, 기본 보존 7일 — C-3·C-4·C-10 권장 표현)
  - **최소 안전장치 박스:** R2는 무료 범위를 넘으면 차단이 아니라 과금된다(§2-4 권장 표현), 단위 올림, 401 요청은 비과금 — 지금 할 일 세 가지(예산 알림 확인·버킷 공개 범위·presigned URL)와 "13장에서 전체 방어선을 세운다"
  - 선택 가이드: kentonv의 "작은 DB 여러 개" vs Hyperdrive + 외부 Postgres(7장 예고)
- **독자가 얻는 것:** 데이터 종류별로 저장소를 고르는 기준과, 각 저장소의 비용이 터지는 지점.
- **오프닝 기법:** 실패 장면
- **클로징 기법:** 결정 플로차트로 닫기
- **스캐폴드 유형:** 비교 대조형
- **그림:** "이 데이터는 어디에?" 결정 플로차트
- **이 장의 핵심:** 둔다
- **예상 분량:** 13,000자

### 5장. 풀스택 앱 — React와 Next.js를 Workers에서
- **핵심 질문:** Next.js 같은 프레임워크를 Vercel 밖에서 운영할 때 어떤 위험을 지고, 어떻게 줄이는가?
- **주요 내용:**
  - 사례: OpenNext 버전 지연 이슈들(#972·#1049 "Downgrading to 16.0.10 fixed it immediately."·#1157·#653·#1214) — 어댑터가 프레임워크를 따라가는 구조의 위험
  - vinext: 공식 권장 기본(2026-08-25 가이드), 1.0.0 출시(2026-09-28)와 가이드의 beta 표기(C-1), `npx vinext check`, `vinext init`(1.0에서 `cf` 기본), `"use cache"` 제한 지원 → 그 기능에 기대는 앱은 OpenNext 유지가 합리적일 수 있음. 논쟁 E(기대·경계, Vercel 측 공개는 이해관계자 표기)
  - `moim-web`을 Next.js(App Router)로 전환: 행사 상세 SSR, `moim-api`와 Service binding(추가 요청 요금 없음). 대안: Vite 플러그인의 React Router v8·TanStack Start SSR
  - "WAF는 패치를 대체하지 않는다" — 2026-05 React/Next.js CVE 패치 버전
  - 성능: Smart Placement(전 플랜, 분석 최대 15분), 다모앙 일화(LA 라우팅, 체감 10~20%, Argo) — 일화임을 표기
  - 배포 파이프라인: Workers Builds(GitHub 연결, 기본 Node.js 24.18.0), PR별 Worker Previews(`wrangler preview`, 4.135.0+) — 프리뷰마다 DO·Containers 네임스페이스가 따로 생긴다는 사실(13장의 복선)
  - 비용 메모: SSR 요청은 Worker 요청, 정적 자산은 무료
- **독자가 얻는 것:** 프레임워크 선택(vinext/OpenNext/React Router) 기준과 프리뷰 배포까지 갖춘 풀스택 `moim`.
- **오프닝 기법:** 수사적 질문
- **클로징 기법:** 한 문장 여운
- **스캐폴드 유형:** 사례 분석형
- **그림:** `moim-web`(Next.js) ↔ `moim-api` Service binding 구조
- **예상 분량:** 11,000자

### 2부 잇기

### 6장. Cloudflare Tunnel — 포트를 열지 않고 서버를 세상에 내놓기
- **핵심 질문:** 공인 IP도, 열린 포트도 없이 내 서버를 안전하게 공개하려면?
- **주요 내용:**
  - 원리: `cloudflared`가 바깥으로 연결을 맺는다 — 두 데이터센터로 장기 연결 4개, 모든 플랜에서 사용 가능(2026-09-11 문서)
  - 원격 관리 터널(권장, 토큰만 있으면 실행 — 토큰 관리 주의) vs 로컬 관리 터널(`config.yml`·ingress·`route dns`). 대시보드 Networking > Tunnels
  - `moim-core`(Spring Boot, `localhost:8080`)를 `core.example.com`으로 공개: systemd 서비스(`--token-file`), Docker, Kubernetes 예시. Spring 쪽 설정(프록시 헤더 신뢰 등)은 버전 의존 API를 피해 서술
  - Quick Tunnel(계정 없이, 200 동시 요청, SSE 미지원 — "신기능"이 아님, C-39)과 Protected Quick Tunnel(`--allowed-mail`, 2026-10-02), `wrangler tunnel quick-start`·Vite에서 `t` 키. 이 주제의 담당 장
  - 운영: replica는 HA용이지 LB용이 아니다(C-7), 오토스케일링 비권장, 7844 포트(UDP/TCP) 아웃바운드와 2026.5.2+ 사전 점검, 지원 버전은 최신 릴리스 1년 이내, Windows 자동 업데이트 없음, `proxy-dns` 제거
  - 걸림돌: 대용량 비디오 약관(FAQ 문구만, C-18), Free 존 업로드 100 MB, gRPC 이슈 #491과 우회 — Spring gRPC 독자 주의
  - 논쟁 C: Tunnel(TLS 종단 위치) vs Tailscale vs ngrok(익명 터널 비판, 이해관계자 표기). 현장 합의 — 공개 노출은 Tunnel + Access, 사설 접근은 Tailscale
  - Access를 앞에 붙이는 것은 10장에서 — 지금은 "아직 문이 열려 있다"는 경고만
- **독자가 얻는 것:** Spring 서버를 포함한 어떤 오리진이든 Tunnel로 공개하고 운영하는 방법과 그 한계.
- **오프닝 기법:** 상황 가정
- **클로징 기법:** 운영 명령 세 줄로 닫기
- **스캐폴드 유형:** 문제-해결형
- **그림:** `cloudflared` 아웃바운드 연결과 요청 경로
- **예상 분량:** 11,000자

### 7장. Spring Boot의 자리 — JVM 백엔드를 어디에 두고 어떻게 잇는가
- **핵심 질문:** JVM이 없는 Workers 옆에서 Java·Kotlin 백엔드는 어디에 살아야 하는가?
- **주요 내용:**
  - 세 착지점 비교: (A) Tunnel 뒤 VM·집 서버(상시 API), (B) Cloudflare Containers(Workers Paid 전용, 2026-04-13 GA), (C) 기존 클라우드에 두고 Placement Hints·Workers VPC(베타, 전망 박스)로 잇기
  - Containers 상세: `linux/amd64`, 인스턴스 타입(lite~standard-4), 메모리·디스크는 프로비저닝 기준·CPU는 활성 사용 기준 과금, 콜드 스타트 "대개 1~3초"(공식 문구만, 6배 개선은 블로그 주장으로 표기 — C-16), 내장 오토스케일링 없음, 인스턴스마다 DO, 한국 이그레스 $0.05/GB. `moim-core`의 **정산 리포트 배치**를 `ReportContainer`로 — "가끔, 몰아서" 쓰는 작업에 맞는 이유(논쟁 D 양쪽 인용). **저자 작성 예제**: Spring Boot 이미지, JVM 힙과 인스턴스 타입, CRaC/GraalVM 네이티브 이미지 검토 — 공식 문서에 Spring Boot 언급이 없음을 밝힌다
  - **계산 예시(저자 검증):** `standard-1` 상시 가동 월 비용을 공식 단가로 직접 계산해 작은 VM과 비교(sliplane의 $82.44는 이해관계자 수치로 병기)
  - Hyperdrive로 Postgres 공유: Postgres를 Neon으로 옮기고 `moim-core`(JDBC)와 `moim-api`(`pg`/Postgres.js via `HYPERDRIVE`)가 같은 DB를 쓰는 구조, 한도(Free 쿼리 10만/일, 원본 연결 ~20). 공급자별 주의는 8장
  - Queues HTTP pull: `moim-api`가 `moim-settlement`에 넣고 Spring이 API 토큰으로 당겨 처리(`visibility_timeout_ms`, `batch_size`, ack)
  - R2를 AWS SDK for Java v2로: 엔드포인트, `region auto`, `pathStyleAccessEnabled(true)`, `chunkedEncodingEnabled(false)` 없으면 403
  - **최소 안전장치 박스:** Workers Paid로 전환하는 순간 Free의 "에러로 멈춤"이 "과금으로 계속"으로 바뀐다 — 지금 할 일: 모든 Worker에 `limits.cpu_ms`·`limits.subrequests`, 예산 알림 임계치, Containers 인스턴스 수 상한을 거는 설정이 있는지 공식 문서에서 확인(레퍼런스에 옵션명이 없으므로 이름을 지어내지 않는다), 13장 예고
  - 전망 박스: 인바운드 TCP·gRPC(비공개 베타, 2026-08-03)
  - Access로 `core.example.com`을 닫는 일은 10장에서
- **독자가 얻는 것:** 자기 Spring 서비스를 상시 API·배치·데이터 공유 관점으로 나눠 착지점을 고르는 기준과, 그 비용 계산법.
- **오프닝 기법:** 앞 장 콜백
- **클로징 기법:** 의사결정 표로 닫기
- **스캐폴드 유형:** 비교 대조형
- **그림:** `moim-core`의 세 착지점과 연결선(Tunnel·Hyperdrive·Queues·Containers)
- **이 장의 핵심:** 둔다
- **예상 분량:** 13,000자

### 8장. Cloudflare 밖과 함께 — DB·결제·메일·AI·IaC 통합 전략
- **핵심 질문:** 무엇을 Cloudflare 안에서 하고 무엇을 밖에 맡길 것인가? 밖에 둔 것은 어떻게 이을 것인가?
- **주요 내용:**
  - 통합의 판단 기준: 데이터의 무게(어디에 오래 남는가), 표준 프로토콜(Postgres·S3·SMTP·OIDC)로 잇는가, 빠져나갈 수 있는가
  - 외부 DB: Hyperdrive 공급자별 주의 — Neon은 serverless 드라이버 대신 TCP 드라이버, Supabase는 풀러 대신 direct 연결 문자열(근거가 Neon/Supabase 문서 경유임을 표기), PlanetScale 통합 청구, MySQL GA(2026-08-07, `mysql2`의 `disableEval: true`), OpenNext #1214 번들링 우회
  - 결제: Stripe 웹훅 `POST /api/webhooks/stripe` — 원본 body `.text()` + `constructEventAsync`, 프레임워크가 JSON을 먼저 파싱하면 깨지는 이유, 서드파티 패키지 취약점 공지. 로컬 수신 테스트는 Protected Quick Tunnel(6장 참조)
  - 메일: Email Routing(수신 무료)과 Email Sending(공개 베타, Paid 월 3,000통) — `EMAIL` 바인딩, Spring은 SMTP(`smtp.mx.cloudflare.net:465`)로 `JavaMailSender` 발송(SMTP 표준 기반 추론임을 표기), 신규 계정 일일 할당량
  - 객체 저장 이전: R2 JS SDK, Sippy(S3·Azure Blob 호환), presigned URL로 Worker 경유 비용 줄이기
  - AI: 외부 LLM 호출을 AI Gateway로(캐싱·레이트 리밋 무료, spend limit은 13장), Workers AI는 "다른 쓰임" 사이드바(10,000 Neurons/일, C-19)
  - 고정 출구 IP 문제: PG·사내 API의 IP 화이트리스트 — 계정 전용 출구 IP는 Enterprise 제품, 비Enterprise 우회는 Tunnel 호스트명 라우팅(§3-9 권장 표현, C-36)
  - IaC·CI: Terraform provider v5(2026-10 기준 v5.27.0), Pulumi(Java SDK 가능), 그리고 5장의 Workers Builds 대신 GitHub Actions로 배포하려는 팀을 위한 `cloudflare/wrangler-action@v4`와 최소 권한 토큰
  - 다른 쓰임 사이드바: Browser Run(구 Browser Rendering), Images(Free 초과 시 9422·과금 없음)
- **독자가 얻는 것:** 외부 서비스를 붙일 때의 판단 틀과, DB·결제·메일·AI·IaC 각각의 검증된 연결 방법.
- **오프닝 기법:** 인용·일화
- **클로징 기법:** 원칙 한 줄 압축
- **스캐폴드 유형:** 사례 분석형
- **그림:** `moim`과 외부 서비스 연결도
- **예상 분량:** 12,000자

### 3부 지키기

### 9장. 공개 앱 지키기 — Turnstile·WAF·레이트 리미팅·시크릿
- **핵심 질문:** 누구나 들어올 수 있는 신청 폼과 API를 무료 범위 안에서 어떻게 지키는가?
- **주요 내용:**
  - 사례로 시작: 커스텀 도메인의 WAF를 우회해 `workers.dev`로 들어온 봇 — `"workers_dev": false` 또는 workers.dev 앞 Access(kentonv 답변, 원문 오타 유지 규칙). 이 주제의 담당 장
  - Turnstile: 위젯 + 백엔드 `siteverify` 두 부분 — 두 번째가 없으면 보호가 없다, 대시보드의 미검증 위젯 표시, Free 위젯 20개·무제한 챌린지, Cloudflare 밖에서도 단독 사용 가능
  - WAF: Free Managed Ruleset 기본 배포, "WAF는 패치를 대체하지 않는다"(5장 회수)
  - 레이트 리미팅 두 층: WAF Rate limiting rule(Free 1개, 10초 기간·10초 완화, Path 필드, IP 기준) vs Workers `ratelimit` 바인딩(GA) — 어디서 무엇을 세는가. KV 카운터는 안 된다(4장 회수)
  - 시크릿: `wrangler secret`, `secrets` 필수 선언(2026-03-25), 로컬 `.dev.vars` 관리, Wrangler 인증 정보의 OS 키체인 저장, API 토큰 최소 권한
  - mTLS·API Shield는 개인 범위 밖(Enterprise 경계) — 짧게
  - DDoS가 내 일인가: Jonker et al. IMC'17(2017년 데이터임을 밝힘, C-30 인용 금지 수치 주의)
  - 앱 사용자 로그인(OIDC·소셜 로그인)과 Access의 경계 — 고객 로그인은 앱의 몫, 운영자·내부 시스템은 10장의 Access
- **독자가 얻는 것:** 공개 표면의 방어선 네 겹과 각 층이 막는 것/못 막는 것.
- **오프닝 기법:** 실패 장면
- **클로징 기법:** 공격자 시점 되짚기
- **스캐폴드 유형:** 문제-해결형
- **그림:** 요청이 거치는 방어 층(WAF → Rate limiting → Worker → Turnstile siteverify)
- **예상 분량:** 10,000자

### 10장. Cloudflare One — 작은 팀을 위한 제로 트러스트
- **핵심 질문:** 운영자 화면, Spring 서버, 팀원의 SSH를 VPN 없이 어떻게 닫아두는가?
- **주요 내용:**
  - 개념: NIST SP 800-207의 두 문장과 BeyondCorp(초록만, C-29) — 네트워크 위치가 아니라 사용자·기기로 판단
  - 좌석과 플랜: Free "50 user limit", Pay-as-you-go "연간 결제 기준 사용자당 월 $7"(C-35), 인증 이벤트로 좌석 소비·비활성 사용자 자동 제거 없음, 서비스 토큰은 좌석 비소비. Mesh의 "50 nodes and 50 users free" 문구를 Access 근거로 쓰지 않는다
  - Access 앱 만들기: `/admin/*`와 `core.example.com` 보호, IdP(신규 조직 기본 Cloudflare IdP, OTP, GitHub·Google 등은 generic OIDC로 — 전용 가이드 미확인 표기), Require Access protection(기본 차단), "Make all Workers private by default"(2026-08-14)
  - **Access JWT 검증 (이 주제의 담당 장):** Workers는 `ctx.access`(Service binding·RPC로 전파되지 않음, 정적 자산 라우터 뒤에서는 전달되지 않음), Node는 `jose`로 `Cf-Access-Jwt-Assertion` 검증, **Spring은 Spring Security Resource Server로 JWKS(`/cdn-cgi/access/certs`)·`aud`·`exp` 검증 — 공식 Java 예제가 없어 직접 작성한 예제**, 키 회전 6주·이전 키 7일 유효를 반영한 JWKS 캐시
  - 서비스 토큰: `moim-api` → `moim-core` 호출, `CF-Access-Client-Id`/`Secret` 헤더, strict 모드(2026-10-05 이후 생성 조직은 기본·해제 불가), 계정당 50개, 회전
  - Cloudflare One Client(구 WARP Client)와 기기 posture, Gateway DNS 필터링 기초, Mesh(구 WARP Connector)로 스테이징 사설망, Tunnel 호스트명 기반 사설 라우팅(Cloudflare One 고객 무료)
  - 팀원 SSH: `cloudflared access ssh` ProxyCommand + Access 정책
  - 유료 경계: 원격 브라우저 격리·전용 출구 IP는 애드온 — 짧게. 현장 반응(대시보드·Client 설정의 어려움 일화)
  - OAuth 2.1은 "초안"(C-32)
- **독자가 얻는 것:** 관리자 화면과 내부 서버를 Access로 닫고, 오리진(특히 Spring)에서 그 결과를 검증하는 완결된 흐름.
- **오프닝 기법:** 정의 뒤집기
- **클로징 기법:** 자가 진단 질문 세 개
- **스캐폴드 유형:** 개념 도입형
- **그림:** Access 인증 흐름(사용자 → Access → Tunnel → Spring, JWT 검증 지점)
- **이 장의 핵심:** 둔다
- **예상 분량:** 13,000자

### 4부 운영하기

### 11장. 캐싱 — 세 가지 캐시 경로와 무효화
- **핵심 질문:** 존 캐시, Workers Cache, Cache API 중 무엇을 언제 쓰며, 바뀐 콘텐츠는 어떻게 내리는가?
- **주요 내용:**
  - 출발점: HTML은 기본 `DYNAMIC`, Page Rules는 deprecated → Cache Rules(Free 10개), Tiered Cache·Smart Topology는 Free 포함 (C-21: 날짜 단정 금지)
  - 세 경로 비교(§3-8 표): Workers Cache(Worker 실행 없이 응답, 기본 tiered, 요청 병합, 태그 퍼지 — **켜면 HIT·정적 자산까지 요청 과금**, 이 함정의 담당 장), Cache API(데이터센터 로컬, 병합 없음, `cache.put`은 SWR·SIE 미지원), `fetch()`의 `cf` 옵션(미들웨어형)
  - "Workers는 캐시 앞에서 실행된다" — 캐시해도 Worker 요청은 과금, 캐시는 Smart Placement보다 먼저
  - 표준과 헤더: RFC 9111, `CDN-Cache-Control`(RFC 9213)로 "브라우저엔 짧게, 엣지엔 길게", `stale-while-revalidate`(비동기, 2026-02-26)·`stale-if-error` — 벤더 구현 범위는 1차 문서로
  - 캐시 키와 HIT율: one-hit-wonder 74%(Maggs & Sitaraman), 쿼리스트링으로 키를 쪼개면 생기는 일. "Cloudflare가 S3-FIFO를 쓴다"고 쓰지 않는다(C-34)
  - 무효화: invalidate(재검증, 2026-09-28) vs purge, Free 퍼지 요청 분당 5회, Cache Response Rules로 `Set-Cookie` 제거. `moim` 행사 상세 페이지를 태그로 묶고 신청 마감 시 무효화
  - Next.js 쪽: ISR와 `"use cache"` 제약(5장 회수), 배포 후 stale HTML 디버깅 순서(HTML·서비스 워커·CDN)
  - 유료 경계: Cache Reserve
- **독자가 얻는 것:** 콘텐츠 종류별 캐시 경로 선택표, 비용까지 고려한 캐시 설정, 배포 후 캐시 문제를 층별로 진단하는 순서.
- **오프닝 기법:** 인용·일화
- **클로징 기법:** 오해 정정으로 닫기
- **스캐폴드 유형:** 비교 대조형
- **그림:** 요청이 세 캐시 경로를 지나는 흐름
- **이 장의 핵심:** 둔다
- **예상 분량:** 11,000자

### 12장. 무료로 어디까지 — 무료 티어를 설계 전략으로
- **핵심 질문:** 무료 티어를 "언젠가 넘어설 맛보기"가 아니라 운영 전략으로 쓰려면 무엇을 알아야 하는가?
- **주요 내용:**
  - 사례: `moim` 행사가 커뮤니티에 소개돼 트래픽이 몰리는 하루 — 무엇이 먼저 바닥나는가
  - "청구 대신 에러" 표: Workers 1027(라우트별 fail open/closed), KV·Hyperdrive·Workers AI 에러, D1 실패 + 이메일, Images 9422, Observability 수집 중단(2026-12-01~), `run_worker_first` 429 — **예외: R2는 과금**(C-37 권장 표현). 이 표의 담당 장
  - 무료로 공짜인 것들: 정적 자산 무제한, Turnstile, Tunnel, Access 50명, Queues 일 10,000 ops, Cron 5개, Email Routing, Analytics Engine(현재 미과금, C-6)
  - Free에서 안 되는 것: Containers, Email Sending(자기 주소 외), 일부 대형 AI 모델, Cache Reserve, Trace Events Logpush
  - 가용성 트레이드오프: 무료 한도는 비용을 지키지만 사용자에게 에러 화면을 보여준다(eliasoliedev 사례) — 라우트별 fail open/closed 선택
  - 계정 분리 전략: 실험·공개 API는 Free 계정, 운영은 Paid 계정(simonw 휴리스틱) — 장단점
  - 학술 연결: 대부분의 애플리케이션은 드물게 호출된다(Shahrad) — 무료 티어가 맞는 서비스의 모양
  - 논쟁 F 박스: 무료 티어는 선의인가 미끼인가(neya의 "$200/mo → $2000+", 카지노 사례 일반화 금지)
  - **계산:** `moim`의 월간 사용량 시뮬레이션(요청·D1 행·KV·Queues·R2) — 공식 한도와 대조한 표
- **독자가 얻는 것:** 자기 서비스의 사용량을 한도에 대조해보는 계산법과, 무료로 버틸 구간을 의도적으로 설계하는 법.
- **오프닝 기법:** 상황 가정
- **클로징 기법:** 계산 결과로 닫기
- **스캐폴드 유형:** 사례 분석형
- **그림:** (선택) `moim` 사용량 vs 무료 한도 막대
- **예상 분량:** 9,000자

### 13장. 유료 계정에서 안전하게 — 하드캡 없는 세상의 다층 방어
- **핵심 질문:** 계정 전체 지출 상한이 없는 상태에서 유료 계정의 비용 사고를 어떻게 막고, 터졌을 때 반경을 어떻게 줄이는가?
- **주요 내용:**
  - 사례: $34,895 청구서(DO `onStart()`의 alarm 재등록 + 60개 넘는 프리뷰 배포, "청구서가 나왔다"까지만 — C-20), $4,868(D1 `ON CONFLICT` 누락, 18일 뒤 $4,586.64 면제, 그 사이 계정 정지). 찜찜한 코드 → 4장의 올바른 alarm 패턴 회수. RetainDB·다모앙 금액은 쓰지 않거나 일반화(C-26·C-27)
  - 정직한 결론: 2026-10 기준 계정 단위 하드캡은 없다(C-23 권장 표현). 알림과 차단은 다르다 — 이 장의 담당 주제
  - 알림·가시성 층: 예산 알림(정보 전용·하루 지연·Workers Paid 기본료 제외, 2026-07부터 $10 기본 알림 순차 적용 — C-14), Billable Usage 대시보드와 API(하루 단위 갱신), 제품별 사용량 알림, Threshold billing(상한이 아니라 중간 정산)
  - 차단 층: `limits.cpu_ms`·`limits.subrequests`(호출 단위 브레이크 — 호출 횟수는 못 막는다), WAF·`ratelimit`(9장), `workers.dev` 끄기(9장), AI Gateway spend limits(AI Gateway 트래픽 한정 실제 차단)
  - 설계 층: DO Hibernation, alarm 존재 확인, 프리뷰 환경에서 DO 바인딩 제거, D1 인덱스·`ON CONFLICT`, Queues 배치·재시도 비용, Workers Cache 과금(11장), Observability 유료 자동 계속(2026-12-01~), Containers 한국 이그레스
  - **`moim-guard` 구현(저자 작성 예제):** Cron Worker가 Billable Usage API를 폴링하고 기능별 자체 카운터로 70/90/100% 단계 대응 — Little Bear Apps 3단 서킷 브레이커를 참고하되, 하루 지연을 기능별 실시간 카운터로 보완하는 이유. Cloudflare가 문서화한 패턴이 아님을 밝힌다
  - 논쟁 G 박스: 알림이면 충분한가, 하드캡이 필요한가(타사 하드캡 주장은 미검증 표기)
  - 청구 분쟁에 대한 태도: 면제를 기대하지 말고 사전 차단
  - DO SQLite 스토리지 과금 개시는 "목표일 2026-01-07로 예고"(C-5)
- **독자가 얻는 것:** 유료 계정에 겹쳐 둘 장치의 목록과 각 장치가 막는 것·못 막는 것, 직접 만든 서킷 브레이커.
- **오프닝 기법:** 충격적 수치·사실
- **클로징 기법:** 오늘 밤 할 일 다섯 가지 + 부록 B 연결
- **스캐폴드 유형:** 문제-해결형
- **그림:** 다층 방어 그림(알림 · 호출 단위 상한 · 트래픽 차단 · 설계 · 자작 차단기)
- **이 장의 핵심:** 둔다
- **예상 분량:** 12,000자

### 14장. 출시, 그리고 그 너머
- **핵심 질문:** 지금까지 만든 `moim`을 출시해도 되는가? Cloudflare에 기대는 서비스를 오래 운영하려면 무엇을 마음에 둬야 하는가?
- **주요 내용:**
  - 되짚기: `moim` 전체 아키텍처를 한 장의 그림으로 — 올리기·잇기·지키기·운영하기가 어떻게 맞물렸나
  - 출시 점검 워크스루: 보안(9·10장), 캐시(11장), 비용(12·13장, 부록 B), 관측(Workers Logs·Traces 오픈 베타·OTel 내보내기, Observability 가격 전환 2026-12-01)
  - 장애와 단일 벤더 리스크(논쟁 A): 2025-11-18·2025-12-05·2026-02-20 장애, 2026-08-08 R2 장애(데이터 유실 여부 단정 금지, C-24) — 양쪽 관점 병기, 출구 전략 점검(표준 프로토콜로 이은 것들: Postgres·S3·SMTP·OIDC, vinext의 이식성)
  - 베타 지도(2026-10-03 기준): vinext 가이드 beta 표기, `cf` CLI, Workers VPC, KV Instant, 인바운드 TCP·gRPC, Email Sending, Cloudflare Traces — §9 재확인 목록과 함께 "출간 이후 바뀌었을 수 있다"
  - 실전 프레임워크: 새 기능을 붙일 때 묻는 질문 다섯 개(어디에 둘까 · 무엇으로 이을까 · 누가 들어올까 · 얼마가 들까 · 멈추면 어떻게 될까)
- **독자가 얻는 것:** 출시 판단의 기준과, 책 전체를 하나의 사고 절차로 묶은 관점.
- **오프닝 기법:** 인용·일화
- **클로징 기법:** 닫는 매듭(여정 회고와 독자가 가져갈 관점)
- **스캐폴드 유형:** 종합 정리형
- **그림:** `moim` 최종 아키텍처
- **예상 분량:** 9,000자

---

## 부록

### 부록 A. 가격·한도 치트시트 (2026-10-03 기준)
- §2-1·§2-2를 독자용으로 압축. 열: 제품 / Free 한도 / Workers Paid 포함량 / 초과 단가 / **Free 초과 시 동작(에러로 멈춤 vs 과금)** / 기준 문서·날짜.
- R2 예외, Workers Cache 과금, KV Instant 단가 경고를 표 안 주석으로.
- 표 머리에 "가격은 자주 바뀐다 — 공식 가격 페이지를 함께 확인하자" 안내.
- **예상 분량:** 산문 3,000자 + 표

### 부록 B. 출시 전 과금 안전 체크리스트
- §5 "유료 전환 시 안전장치 체크리스트"와 13장 내용을 체크박스 목록으로. 각 항목에 담당 장 번호.
- 항목마다 "이 장치는 알림인가, 차단인가" 표시.
- **예상 분량:** 산문 4,000자 + 목록

### 부록 C. 명칭 변경 대조표와 도구 버전 (2026-10 기준)
- §0 명칭·상태 변경표(독자용 축약), §8 도구 버전 표(wrangler 4.147.0, `@cloudflare/vite-plugin` 1.62.5, `@cloudflare/vitest-plugin` 1.3.6, C3 2.73.2, `cloudflared` 2026.9.3, vinext 1.0.1, OpenNext 1.20.8, wrangler-action v4.1.3, Terraform provider v5.27.0).
- **예상 분량:** 산문 2,000자 + 표

> 참고문헌·판권은 editor가 작성한다(참고문헌은 `01_reference.md` §10 원장 그대로).

---

## 분량 합계

| 구분 | 순수 산문 |
|---|---|
| 1~14장 | 8,000 + 10,000 + 11,000 + 13,000 + 11,000 + 11,000 + 13,000 + 12,000 + 10,000 + 13,000 + 11,000 + 9,000 + 12,000 + 9,000 = **153,000자** |
| 부록 A·B·C | 3,000 + 4,000 + 2,000 = 9,000자 (+ 표·목록) |
| 합계 | **약 162,000자** (순수 산문 기준, 표·코드 제외) |

---

## 저술 운영 메모

- **권장 저술 묶음(연속, 예제 이정표와 일치):** 묶음 1 = 1~4장(Cloudflare 안에서 데이터까지) / 묶음 2 = 5~7장(풀스택과 Spring 연결, Workers Paid 전환) / 묶음 3 = 8~10장(외부 통합과 보안) / 묶음 4 = 11~14장(운영과 출시) + 부록. 뒤 묶음 저술가는 "예제 서비스 `moim` — 장별 종료 상태" 표를 앞 장의 정전으로 삼는다.
- **필독 구역:** 모든 저술가는 `01_reference.md` §0(명칭 변경), §2(가격·한도), §7(충돌 원장 — 위 장별 배정), §9(출간 직전 재확인)를 쓰기 전에 읽는다.
- **베타 제품 규칙:** KV Instant(비공개 베타), 인바운드 TCP·gRPC(비공개 베타), `cf` CLI(베타), Workers VPC(베타·무료), Email Sending(공개 베타), Cloudflare Traces(오픈 베타)는 `> **전망: ...**` 박스나 "베타" 명시와 함께 쓴다. 단 Email Sending은 8장 본문 실습에 쓰되 공개 베타임을 밝히고, Workers VPC는 7장에서 전망 박스로만 쓴다.
- **이해관계자 표기:** kentonv(Cloudflare), Vercel, ngrok, Pinggy, sliplane 발언은 레퍼런스의 `[이해관계자]` 라벨을 본문에서도 "Cloudflare 엔지니어인 ~", "경쟁 PaaS 공동창업자인 ~"처럼 드러낸다.
- **커뮤니티 원문 인용:** 영어 원문을 그대로 인용하고 바로 뒤에 우리말로 풀어준다. 오타가 있는 원문(`wranlger`, `nost`)은 그대로 두고 "(원문 그대로)"를 붙인다.

---

## 리서치 한계와 계획상 대응

- **Spring Security의 Access JWT 검증 공식 예제 없음(§11 #1)** → 10장에서 저자 작성 예제로 명시. JWKS URL·`aud`·키 회전 사실만 1차 근거로 쓴다.
- **Spring Boot on Containers·on Tunnel 실사용기 0건(§11 #2)** → 7장은 공식 단가로 직접 계산한 비용 예시와 저자 작성 구성으로 채우고, 실사용 검증이 없음을 밝힌다.
- **Spring Boot·Spring Security 버전 정보가 레퍼런스에 없음** → 버전 의존 API는 `(사실 확인 필요)`로 남기고 fact-checker가 판정.
- **한국어 현장 자료가 빈약(§11 #14)** → 오프닝·사례가 영어 HN 자료에 기운다. 한국어 근거(다모앙·GeekNews·잡가이버)는 2·5·12·14장에 우선 배치.
- **Supabase·Clerk/Auth0·Stripe의 Cloudflare 1차 가이드 없음** → 근거가 타사 문서 경유임을 본문에 표시(8·10장).

---

## 개정 이력

- 2026-10-03 — 초안 작성 (book-planner)
- 2026-10-03 — **사용자 승인** (Phase 3). 제목 1번 확정: 『Cloudflare를 나의 클라우드로 — 정적 사이트부터 Spring 백엔드까지, 무료로 시작해 안전하게 운영하기』. Spring 예제 언어는 **Java**(Kotlin은 차이가 있는 곳에서만 짧게 메모).
- 2026-10-03 — 갭 보강 리서치 `research/web_gaps.md` 반영 (오케스트레이터):
  - **5장 vinext:** vinext 1.0 init은 기본으로 `cf` CLI + `cloudflare.config.ts`를 만들고 `wrangler.jsonc`는 만들지 않는다. Wrangler 경로는 `--legacy-wrangler-cloudflare-init` 플래그 뒤에만 있다(PR #3504, 2026-09-27). `moim-web`은 책 전체의 `wrangler.jsonc` 일관성(13장 `limits.*`, CI) 때문에 계획대로 Wrangler 경로에 두되, 5장은 (1) 기본 경로가 `cf`라는 사실, (2) 이 책이 "legacy"라 이름 붙은 플래그를 일부러 쓰는 이유와 그 위험, (3) `cloudflare.config.ts`와 `wrangler.jsonc`의 대응을 정직하게 밝힌다. 기존 `(사실 확인 필요)` 대신 web_gaps.md §1의 명령을 쓴다. 공식 가이드(2026-08-25)가 아직 beta 표기·Wrangler 바인딩 안내라 1.0과 어긋난다는 점도 밝힌다.
  - **7·10장 Spring:** Spring Boot 4.1.1 / Spring Security 7.1.1 (2026-08-20 GA, Java 17+) 기준. Access JWT는 `Bearer ` 접두사가 없으므로 `HeaderBearerTokenResolver("Cf-Access-Jwt-Assertion")`가 필요하다. `issuer-uri` 단독 대신 `jwk-set-uri`를 명시한다.
  - **7장 Containers:** 신규 앱은 Durable Object Container API(`ctx.container`) 권장(2026-09-29 문서). `start()` 기본 인스턴스가 `lite`(256 MiB)라 JVM은 인스턴스를 명시해야 한다. JVM 공식 예제는 0건 — 저자 작성 예제로 명시.
- 2026-10-03 — **저술 묶음 확정:** 1~4 / 5~7 / 8~10 / 11~14 + 부록 B. 부록 A(가격·한도 치트시트)·C(명칭 변경·도구 버전)는 레퍼런스 §2·§8에서 기계적으로 옮기는 표라 editor가 뒷부속으로 작성한다.
- 2026-10-03 — **통합 반영 (editor, `integration_flags.md` 1·5·9):** 장별 종료 상태 표 11장 행을 실제 원고(Workers Cache + 태그 퍼지, 존 캐시는 Spring 오리진)로 갱신. 고정 박스에 `> **논쟁: …**` 추가. DO 클래스 선언은 책 전체 선언형 `exports`로 통일(4·7·13장, Wrangler 설정 문서 2026-10-02·Containers Wrangler 설정 2026-09-29). 용어 추가: Worker Previews·프리뷰 주소는 "프리뷰", Cloudflare 변경 공지는 본문에서 "changelog"(괄호 출처 표기는 "Changelog YYYY-MM-DD" 유지).
- 2026-10-03 — **출간 후 정전 메모 (오케스트레이터):** 수락 게이트 수정 라운드 1과 마감 패스 이후 `04_manuscript.md`가 정전이다. `chapters/*_final.md`는 그 이전 상태(AWS SDK v3 presigned 예제, 4장 형태와 다른 메일 소비자, 중복 `export default` 등)이므로, 재실행 매트릭스의 '특정 챕터 수정' 시에는 해당 장을 `04_manuscript.md`에서 추출해 출발점으로 삼는다. 또한 `01_reference.md` §3-3 논쟁 B는 kentonv의 10GB 발언을 D1에 오귀속한다 — 실제로는 Durable Objects SQLite DB에 관한 발언(HN 47696640).
