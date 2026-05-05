# 저술 계획

본 계획은 `01_reference.md` (2026년 5월 시점 통합 레퍼런스)와 `toby-book-writing-style.md` (평어체·청유형·수사적 질문 중심의 토비 문체)를 토대로 한다. 1차 계획에 대한 리뷰 피드백(03_review_log.md Top 5)을 반영한 v2 버전이다. 핵심 메시지는 단 하나다 — **Cloudflare는 "또 하나의 클라우드"가 아니라 멘탈 모델이 다른 edge-first 플랫폼이다.** 이 책은 AWS에 익숙한 개발자가 Cloudflare를 1:1 매핑으로만 보다가 핵심을 놓치는 함정을 피하게 해주는 안내서다.

---

## 1. 책 제목 후보

### 후보 A — 정공법형
**『AWS 개발자를 위한 Cloudflare 본격 활용 가이드』**
- 부제 후보: *또 하나의 클라우드가 아니라 — Workers·D1·R2·OpenNext·AI Gateway로 멘탈 모델을 다시 그리는 길잡이*
- 톤: 실용서·기술 레퍼런스 톤. 한 눈에 무엇을 다루는지 분명.
- 포지셔닝: 검색·서점 분류에서 "Cloudflare 한국어 가이드" 슬롯에 정확히 꽂히는 제목. 부제 첫머리 "또 하나의 클라우드가 아니라"가 책의 핵심 메시지를 표지에서부터 약속.
- 강점: 독자가 책장을 펼치는 순간 망설임이 없다. AWS 키워드가 들어가 있어 잠재 독자(AWS 백엔드 경력자)가 자기 책임을 즉시 인지. 부제가 메시지(메탈 모델 전환)를 함께 약속.
- 약점: 무난해서 "또 하나의 비교서"로 보일 위험. 부제가 그 우려를 흡수해야 함.

### 후보 B — 감성·서사형
**『리전 너머로 — AWS 개발자가 다시 만나는 서버리스』**
- 부제 후보: *V8 isolate 위에서 Spring과 Lambda를 잊고 Cloudflare를 사고하기*
- 톤: 에세이형 기술서. 개발자의 여정·전환의 감각을 환기.
- 포지셔닝: "리전·VPC·서브넷" 너머의 세계로 향하는 항해 메타포. 토비 문체("자, 함께 살펴보자")와 자연스럽게 어울린다.
- 강점: 단순 비교서가 아닌 "사고 전환을 돕는 책"임을 표지에서부터 약속할 수 있다.
- 약점: 검색 키워드가 약해 노출이 줄 수 있음.

### 후보 C — 실용 키워드형
**『Cloudflare Workers 실전 — AWS에서 넘어온 개발자를 위한 길잡이』**
- 부제 후보: *Lambda를 떠나지 않고도 Edge를 곁에 두는 법*
- 톤: 실용 키워드 + 후크. 서점·검색 친화.
- 포지셔닝: "Cloudflare Workers"라는 압도적 검색 키워드를 전면에 두고, "AWS에서 넘어온"이라는 차별화 슬로건으로 좁힘.
- 강점: 노출·클릭 친화. 부제의 "Lambda를 떠나지 않고도"는 하이브리드 운영(이 책의 권장 패턴)을 정확히 한 줄로 약속.
- 약점: 다소 마케팅 느낌. 토비 문체의 차분함과는 살짝 결이 다를 수 있음.

**추천:** **후보 A** (『AWS 개발자를 위한 Cloudflare 본격 활용 가이드』 — 부제는 강화안)

이유:
1. 책의 주제·대상 독자·범위를 가장 정직하게 압축한다. "본격 활용"이라는 단어가 단순 입문서가 아니라 실무 깊이까지 다룬다는 신호를 준다.
2. 강화된 부제 *"또 하나의 클라우드가 아니라 — ..."* 가 책의 핵심 메시지를 표지에서 약속해 검색 키워드와 메시지를 동시에 잡는다.
3. 토비 문체는 본문에서 차분하게 살리되, 표지·제목은 군더더기 없이 정공법으로 가는 편이 책 전체의 신뢰를 더한다.

---

## 2. 책 특성

| 항목 | 값 |
|---|---|
| **장르** | 기술 실용서 / 가이드북 (멘탈 모델 전환 + 마이그레이션 매뉴얼 성격 결합) |
| **분량** | 290~330쪽 (한국어 단행본 기준), 약 110,000~125,000 단어 / 한글 21만~25만 자 |
| **챕터 수** | 본문 14장 + 부록 6편 |
| **난이도** | 중급. AWS·백엔드 경력 전제. JS/TS는 기초만 있으면 따라올 수 있도록 단계 설명. Java/Spring 비교는 멘탈 매핑·마이그레이션 챕터에 한정. |
| **주력 코드 언어** | TypeScript (Workers + Hono + Drizzle) — 1순위. Java/Spring 코드는 §3, §4, §11, §14에서 비교용으로 등장. |
| **로컬 환경 전제** | macOS + Homebrew + Node 22+ + pnpm + wrangler@latest. 모든 실습은 Mac에서 그대로 실행 가능. |
| **저자** | Toby-AI |
| **언어** | 한국어 본문, 코드·제품명·약어는 영문 유지 |

### 독자 여정 (이 책을 다 읽고 났을 때)

진입 상태 — Lambda·DynamoDB·S3·CloudFront 위에 Spring/Node 앱을 운영하고 있으나, 해외 사용자 지연·egress 비용·점점 늘어나는 운영 부담을 느낀다. Cloudflare 이름은 들어봤지만 "Lambda의 더 싼 대안" 정도로 모호하게 알고 있다.

출구 상태 — Workers의 V8 isolate 모델이 왜 Lambda 컨테이너 모델과 본질적으로 다른지 손끝으로 안다. 자신의 시스템에서 어떤 부분을 Cloudflare로 옮기고 어떤 부분을 AWS에 남길지 의사결정 프레임을 갖췄다. 첫 Worker를 배포해봤고, D1·KV·Durable Objects를 워크로드 패턴별로 고를 줄 알며, RDS는 그대로 두고 Hyperdrive로 edge에서 살리는 하이브리드 패턴을 직접 그릴 수 있다. Workflows·Queues·Cron Triggers로 Step Functions·SQS·Spring `@Scheduled`의 자리를 다시 채울 수 있다. 무엇보다 2025년 outage·vendor lock-in 같은 정직한 위험을 인지한 채로 결단한다 — Cloudflare를 "도입"하는 것이 아니라, 자기 아키텍처에 "올바른 자리"를 내준다.

### 핵심 약속(Promise)

> **이 책을 다 읽으면, AWS 위에 쌓아온 시스템을 부수지 않고도 Cloudflare를 가장 효과적인 자리에 끼워 넣을 수 있다.**

---

## 3. 본문 구성 — 14장

흐름은 *왜 → 멘탈 → 첫 성공 → 매핑 → 결정 프레임 → 본격 사용 → 데이터(KV·D1) → 데이터(DO·R2) → 프론트(Next.js) → Hyperdrive → 보안/Zero Trust → AI·비동기·스케줄 → 운영·정직성 → 마이그레이션*. 각 장은 단독으로도 가치 있되 연결해 읽으면 멘탈 모델 전환 → 결정 → 실무 적용 → 결단의 큰 곡선을 그린다.

### 글쓰기 원칙 (모든 챕터 공통)

- 각 챕터 끝에 **"이 기술이 무너지는 자리"** 박스 1개를 둔다. 광고로 보이지 않게 하는 가장 단순한 약속.
- Spring/Java 멘탈 다리는 5·6·7·9·11·14장에 박스 형태로 명시한다 (`@Transactional`, `@Async`, JDBC `HikariCP`, `@Scheduled` 매핑).
- 모든 실습은 누적 프로젝트 `toby-shop`에서 진화한다 (아래 §3.A 지도 참조).

---

### §3.A 누적 실습 프로젝트 지도 — `toby-shop`

이 책의 실습은 한 도메인(`toby-shop` — 작은 e-commerce SaaS)을 기반으로 챕터마다 한 겹씩 쌓아 올린다. 각 챕터 끝에서 깃 브랜치(`ch3-hello`, `ch6-data` 등)로 체크포인트가 남는다.

| 챕터 | 실습 결과물 | 누적 vs 분기 |
|---|---|---|
| 1장 | "내 시스템에 Cloudflare가 들어올 자리 3곳" 워크북 한 장 | 분기 (워크북) |
| 2장 | "Workers에서 절대 못 하는 것 7가지" 자가 점검표 | 분기 (워크북) |
| 3장 | 빈 Worker 1개 — `hello-edge.<sub>.workers.dev` 글로벌 배포 | 누적 시작 |
| 4장 | 자기 시스템 아키텍처에 매핑 색칠 | 분기 (워크북) |
| **5장** | **"toby-shop의 옮길 자리·남길 자리" 결정 워크시트** | **분기 (워크북)** |
| 6장 | Hono 라우팅 + 인증 미들웨어 + KV 세션 + DI/테스트 | 누적 (Worker 1) |
| 7장 | KV 세션 유지 + D1 + Drizzle 사용자 프로필 추가 | 누적 (Worker 1 진화) |
| 8장 | DO 채팅방 + R2 첨부 업로드 (`toby-shop` 고객지원) | 누적 (Worker 2 분기) |
| 9장 | Next.js 14 상점 프론트(OpenNext) + Cloudflare Images | 누적 (Web 1 신규) |
| 10장 | 기존 RDS(또는 Neon) → Hyperdrive 바인딩 — 주문 도메인 | 누적 (Worker 1 진화) |
| 11장 | Auth.js 소셜 로그인 + cloudflared로 보호된 어드민 | 누적 (Worker 1 진화 + 어드민 추가) |
| 12장 | Workflows로 결제 후 영수증 발송 + Queue + Cron으로 장애 알림 + RAG 챗봇 | 누적 (Worker 1·2 진화) |
| 13장 | Logpush(R2) + Sentry observability + 단일 벤더 의존 점검표 | 누적 (운영 레이어) |
| 14장 | 가상 AWS-only 스택 → Cloudflare 하이브리드 8단계 로드맵 | 분기 (워크북 + 시뮬레이션) |

각 챕터 "실습 결과물" 항목 끝에 **"누적 / 분기"**가 명시돼 있다.

---

### §3.B 토픽별 깊이 표 — 같은 토픽이 어디서 어디까지

같은 토픽이 여러 챕터에 등장할 때, 어디가 깊이고 어디가 언급인지 사전에 약속한다. 저술 단계의 중복·공백 가드.

| 토픽 | 1장 | 2장 | 4장 | 5장 | 6장 | 7장 | 10장 | 13장 | 14장 |
|---|---|---|---|---|---|---|---|---|---|
| **V8 isolate** | 한 단락 | **본격** | — | — | — | — | — | — | — |
| **Bindings** | 한 줄 | 개념 | 매핑 | — | 코드 | 코드 | 코드 | — | — |
| **Compatibility Date** | — | **본격** | 매핑 한 줄 | 운영 | — | — | — | 함정 | — |
| **KV** | 한 줄 | — | 매핑 | — | — | **본격** | — | 운영 | 마이그레이션 |
| **D1** | — | — | 매핑 | — | — | — | 비교 | — | — |
| **D1 + Drizzle** | — | — | — | — | — | **본격** | 비교 | — | — |
| **Durable Objects** | — | — | 매핑 | — | — | 비교 | **본격(8장)** | — | — |
| **R2** | 한 줄 | — | 매핑 | — | — | — | **본격(8장)** | egress 함정 | 마이그레이션 |
| **Hyperdrive** | — | — | 매핑 한 줄 | — | — | D1 비교 | — | **본격(10장)** | — |
| **OpenNext** | — | — | — | — | — | — | — | **본격(9장)** | — |
| **Workflows / Queues / Cron** | — | — | 매핑 한 줄 | — | — | — | — | — | **본격(12장)** |
| **AI Gateway / Workers AI / Vectorize** | 한 줄 | — | 매핑 | — | — | — | — | — | **본격(12장)** |
| **Zero Trust / Tunnel / WAF** | — | — | 매핑 | — | — | — | — | — | **본격(11장)** |
| **2025 outage** | 1단락 | — | — | — | — | — | — | — | **본격(13장)** |
| **vendor lock-in** | 1단락 | — | — | — | — | — | — | — | **본격(13장)** |
| **"옮길까 말까" 결정** | 한 줄 | — | 매핑 함정 | **본격** | — | — | — | — | "어떻게 옮기는가"로 이어짐 |

---

### Chapter 1. 왜 또 하나의 클라우드가 아닌가 — Edge-first의 시대

- **챕터 한 줄 요약:** AWS 개발자가 Cloudflare를 "더 싼 Lambda"로 오해하는 함정을 무너뜨리고, 이 책을 왜 끝까지 읽어야 하는지 약속한다.
- **핵심 질문**
  1. Cloudflare를 "또 하나의 클라우드"로 보면 무엇을 놓치게 되는가?
  2. AWS를 떠나지 않고도 Cloudflare가 들어와야 할 자리는 어디인가?
- **주요 내용**
  - Edge-first 플랫폼이라는 개념: 리전·VPC가 사라진 자리에 PoP·Bindings·Compatibility Date가 들어선다
  - 2025년 두 차례 outage가 가르쳐준 것 — "Cloudflare를 쓸까 말까"가 아니라 "어디에 어디까지 의존할까" (한 단락 맛보기, 본격은 13장)
  - egress free·콜드스타트 5ms·DDoS 기본 포함이라는 세 가지 명시적 약속
  - **이 책이 다루지 않는 것** 박스: GPU 추론·Spring Batch·복잡한 PrivateLink·Python Workers (의도적 제외 명시)
  - 이 책을 읽으면 좋은 사람: 해외 사용자 지연·미디어 egress·점진 마이그레이션이 고민인 백엔드 경력자
  - 책의 나침반 — 14장의 지도와 누적 프로젝트 `toby-shop`의 한 줄 소개
- **예상 분량:** 12~15쪽 / 약 5,500 단어 (도입부 + 책 전체 약속)
- **의존성:** 없음 (오프닝)
- **실습 결과물:** "내 시스템에서 Cloudflare가 들어와야 할 후보 자리 3곳" 종이 워크북 한 장. (분기)

---

### Chapter 2. 멘탈 모델을 다시 그리자 — V8 Isolate가 바꾸는 가정

- **챕터 한 줄 요약:** Lambda의 컨테이너 모델로 Workers를 이해하려는 시도를 무너뜨리고, V8 isolate·리전 부재·Bindings·Compatibility Date라는 네 기둥을 세운다.
- **핵심 질문**
  1. Workers 콜드스타트가 5ms 미만인 이유는 무엇이며, 그 대가로 무엇을 포기하는가?
  2. 리전 개념이 사라진 자리에 무엇이 들어서는가?
- **주요 내용**
  - V8 isolate vs Firecracker microVM — 같은 "서버리스"라는 단어 아래의 다른 행성
  - 한 isolate의 trade-off: 임의 바이너리 불가, full Node API 불가, OS syscall 불가, 멀티스레딩 불가
  - Spectre 방어와 `Date.now()` 동작 (Workers 안에서는 시간이 멈춘 것처럼 보인다)
  - 리전이 사라진 자리: PoP·Jurisdiction·D1 location hint·DO location hint
  - Bindings — Spring `@Autowired`와 IAM role을 한 추상으로 묶은 것
  - Compatibility Date — Lambda runtime 버전·Spring Boot 버전과 어떻게 다른가
  - 멘탈 매핑 표 1: Spring/Lambda 개념 → Workers 등가물 한 페이지 요약
- **예상 분량:** 20~22쪽 / 약 8,500 단어 (1차안 26쪽에서 슬림화. 운영 멘탈 일부는 4장 매핑으로 이동)
- **의존성:** 1장
- **실습 결과물:** "Workers에서 절대 못 하는 것 7가지" 자가 점검표. (분기)

---

### Chapter 3. 첫 Worker를 띄우자 — Mac에서 5분 만에 글로벌 배포

- **챕터 한 줄 요약:** wrangler 설치부터 Hello World 배포·로그 보기·시크릿 등록까지 한 사이클을 완주해 "내 코드가 정말로 글로벌 PoP에서 도는구나"를 손으로 느끼게 한다.
- **핵심 질문**
  1. AWS 개발자가 처음 Workers를 띄울 때 가장 헷갈리는 한 가지는 무엇인가?
  2. SAM/CDK 없이도 IaC적 안정감을 어떻게 얻는가?
- **주요 내용**
  - macOS 환경 준비: Homebrew·Node·pnpm·wrangler (글로벌 설치를 권하지 않는 이유)
  - `wrangler login` vs `CLOUDFLARE_API_TOKEN` — 로컬과 CI의 분리
  - `pnpm create cloudflare` 첫 프로젝트 — Hono 템플릿
  - `wrangler.toml` 핵심 필드 — name·main·compatibility_date·bindings 첫 인상
  - `wrangler dev` 로컬 모드 vs `--remote` — workerd가 production을 그대로 재현
  - 첫 배포: `wrangler deploy` → workers.dev 도메인에서 응답 확인
  - 실시간 로그(`wrangler tail`)와 대시보드 observability — CloudWatch와 무엇이 다른가
  - 첫 시크릿: `wrangler secret put` — `.dev.vars`와 production secret의 분리
  - 헷갈리기 쉬운 5가지 — `.env` vs `.dev.vars`, `compatibility_date` 갱신 시점, custom domain vs route, Workers vs Pages, free vs paid
- **예상 분량:** 20~24쪽 / 약 8,500 단어
- **의존성:** 2장
- **실습 결과물:** `hello-edge` Worker 한 개가 워커 도메인에 배포돼 있고, 시크릿 1개·로그 tail까지 한 사이클 경험. (누적 시작 — `toby-shop` 리포의 시드)

---

### Chapter 4. AWS ↔ Cloudflare 매핑 카탈로그 — 1:1 표가 거짓말이 되는 지점들

- **챕터 한 줄 요약:** 컴퓨트·스토리지·네트워크·보안·관측·AI 영역의 매핑을 카탈로그로 정리하되, "한 줄 매핑이 거짓말이 되는 경계"를 분명히 표시한다.
- **핵심 질문**
  1. Lambda·S3·DynamoDB·CloudFront 같은 익숙한 이름들은 Cloudflare 어느 자리에 어떻게 자리 잡는가?
  2. 1:1 매핑이 깨지는 경우(특히 DynamoDB·EventBridge·PrivateLink)는 어떻게 다뤄야 하는가?
- **주요 내용**
  - 컴퓨트 매핑: Lambda↔Workers, Lambda@Edge↔Workers (사실상 흡수), ECS/Fargate↔Workers Containers, Step Functions↔Workflows
  - **Workers Containers 강화 박스 (2~3쪽)**: 0.5 vCPU·4GiB 한도, "ECS를 언제 유지하나"의 의사결정선
  - 스토리지·DB 매핑: S3↔R2, RDS↔(D1 / Hyperdrive), ElastiCache↔(Cache API + KV + DO 조합), OpenSearch↔Vectorize
  - **DynamoDB 한 줄 매핑은 거짓말이다** — 사용 패턴별로 KV / D1 / Durable Objects로 갈라지는 이유 (7·8장 예고편)
  - 네트워크·전달: CloudFront↔Cloudflare CDN, Route 53↔Cloudflare DNS, API Gateway↔Workers Routes + Hono, SQS↔Queues, SNS/EventBridge↔(약함, 직접 구성)
  - 보안·인증: IAM의 정교한 정책 언어에 직접 등가물이 없다는 사실, Cognito↔Access + 외부 IdP, WAF↔Cloudflare WAF + Bot Management + Turnstile
  - 관측: CloudWatch는 한 제품으로 흡수돼 있지만 Cloudflare는 Workers Logs + Logpush + 외부 APM 조합이 표준
  - AI: Bedrock↔Workers AI + AI Gateway, Knowledge Bases↔Vectorize
  - 비동기·스케줄: Step Functions↔Workflows, SQS↔Queues, EventBridge·`@Scheduled`↔Cron Triggers (12장 예고편)
  - "AWS 등가물이 없는 것들" 박스: AI Gateway, egress free, Compatibility Date, Cloudflare Tunnel
  - **챕터 끝 박스 — "매핑 표가 거짓말을 하는 5가지 패턴"**
  - 한 페이지 빠른 참조 표 — 부록 B로 이어진다
- **예상 분량:** 22~26쪽 / 약 9,500 단어
- **의존성:** 2장 (멘탈 모델)
- **실습 결과물:** 자기 시스템 아키텍처 다이어그램 위에 "1:1 매핑 / 패턴별로 갈라지는 / 등가물이 없는" 부분을 색칠한 워크북 한 장. (분기)

---

### Chapter 5. 옮길까 말까 — Cloudflare로 가야 할 워크로드 판별법 (신설)

- **챕터 한 줄 요약:** 매핑 카탈로그를 본 직후, "그래서 내 워크로드 중 무엇을 옮기고 무엇을 남길 것인가"의 결정 프레임을 본격 챕터로 갖춘다. 책의 핵심 약속("올바른 자리를 내준다")의 핵심 도구.
- **핵심 질문**
  1. 어떤 워크로드는 Cloudflare로 가도 되고, 어떤 워크로드는 절대 옮기면 안 되는가?
  2. 결정의 기준이 비용·지연·일관성·운영 부담 중 어디에 있어야 하는가?
- **주요 내용**
  - **5축 결정 트리**:
    1. 요청 패턴 — spike-y vs steady, 글로벌 vs 단일 리전
    2. 데이터 일관성 — eventually consistent로 충분한가, strong consistency가 필요한가, transactional인가
    3. 글로벌성 — 사용자 지리 분포, 지연 SLO, 데이터 jurisdiction
    4. 패키지·런타임 의존 — Node API 깊이 사용, 임의 바이너리, full JVM, OS syscall
    5. 컴플라이언스·격리 — VPC 격리·PrivateLink·강한 region lock·HIPAA·KISA 가이드
  - **절대 옮기면 안 되는 워크로드** 박스:
    - 대용량 GPU 추론 (Workers AI 모델 외)
    - JVM 무거운 라이브러리 의존 (Spring 전체 컨텍스트, batch + JPA)
    - 강한 region lock (한국 데이터 주권 + 단일 KR 리전 강제)
    - OS syscall 의존 (FFmpeg 직접 호출, 로컬 디스크 캐시)
    - 30초+ 장기 동기 batch (Workers CPU time 한도와 무관하게 architecturally 잘못됨)
    - 복잡한 PrivateLink·VPC peering 위주 워크로드
  - **자가 진단 체크리스트 18개 항목** — Yes/No 답으로 가중 점수 산출, 결과는 "Move now / Move later / Don't move" 세 갈래
  - **워크로드 9패턴 결정 매트릭스**: 정적 자산 / API gateway 앞단 / read-heavy 캐시 / write-heavy DB / long-running orchestration / WebSocket 채팅 / 미디어 storage / 인증 게이트웨이 / RAG 검색 — 각 패턴의 권장 행동
  - **의사결정 워크시트** — 부록 B와 연계, 독자가 자기 시스템 5~10개 컴포넌트를 표에 채워 넣어 결정 1차안을 만든다
  - **사례 인용**: Liftosaur(KV 회귀)·velopert(Pages 회귀)·Baselime(95% 절감)·Rebal AI(이중 운영) — 결정의 양쪽 끝을 정직하게 보여준다
  - 14장과의 관계: 5장은 "무엇을 옮길 것인가"의 결정 프레임, 14장은 "어떻게 옮길 것인가"의 8단계 시퀀스
- **예상 분량:** 16~20쪽 / 약 7,500 단어
- **의존성:** 4장 (매핑 카탈로그)
- **실습 결과물:** `toby-shop`의 가상 컴포넌트 8개를 결정 매트릭스에 넣어 "Move now / Move later / Don't move"로 분류한 워크시트 한 장. 6~12장에서 실제로 옮길 것·남길 것이 이 결정 위에서 진행된다. (분기 — 누적 프로젝트의 결정 베이스)

---

### Chapter 6. Workers 본격 사용법 — Spring 멘탈을 Hono로 다시 그리자

- **챕터 한 줄 요약:** 라우팅·미들웨어·DI·테스트·시크릿이라는 Spring 개발자의 다섯 가지 익숙한 도구를 Workers + Hono 환경에서 어떻게 다시 짜는지 코드로 보여준다. (D1 + Drizzle은 7장으로 이동해 5장 분량을 22쪽 내외로 슬림화)
- **핵심 질문**
  1. `@RestController`·`@Component` 같은 안전망 없이 어떻게 같은 품질의 코드를 짤 수 있는가?
  2. Spring의 `SecurityFilterChain`을 Workers에서 어떻게 다시 그릴까?
- **주요 내용**
  - `fetch(request, env, ctx)` — Workers의 본질 진입점
  - Hono 도입 — Express에 가까운 라우팅·미들웨어 체인
  - 미들웨어 패턴: Auth → Rate Limit → Cache → Proxy → Log 체인을 코드로
  - DI 다시 그리기: Bindings(env)가 사실상 런타임 주입. 테스트에서는 `getBindingsProxy()` 또는 `@cloudflare/vitest-pool-workers`
  - 환경별 분리: `[env.staging]`, `[env.production]`, `wrangler secret put --env`
  - 비교 코드 1: Spring Boot `UserController` → Workers + Hono로 옮긴 같은 기능 (D1 부분은 7장 예고편으로 placeholder)
  - 비교 코드 2: Spring Security 인증 필터 → Hono 미들웨어 + KV 세션
  - 코드 품질 도구: `wrangler types`로 자동 생성되는 `Env` 타입, ESLint·Biome·Prettier
  - 모노레포 구조 권장: `apps/api`, `apps/web`, `packages/shared` (db 패키지는 7장에서 추가)
- **예상 분량:** 22~24쪽 / 약 9,500 단어 (1차안 26~30쪽 → 슬림화)
- **의존성:** 3장 (첫 Worker), 4장 (매핑), 5장 (결정 프레임)
- **실습 결과물:** 사용자 CRUD API의 라우팅·미들웨어·KV 세션·인증 한 벌. vitest로 단위 테스트 통과. D1은 다음 장에서 추가. (누적)

---

### Chapter 7. 데이터 1 — KV와 D1, 워크로드 패턴으로 골라 쓰기

- **챕터 한 줄 요약:** "DynamoDB 대안"이라는 잘못된 묶음을 풀어, KV는 read-heavy·세션·플래그에, D1은 SQL·관계형 데이터에 어떻게 다른 자리를 잡는지 보여준다. 6장에서 미뤘던 D1 + Drizzle 실습이 이 챕터의 본격 진입.
- **핵심 질문**
  1. KV의 "최대 60초 전파"는 무엇을 허용하고 무엇을 금지하는가?
  2. D1의 SQLite 모델은 어디까지 production을 견디는가?
- **주요 내용**
  - KV — eventually consistent (60s)·per-key 1 write/s·secondary index 없음·range query 없음
  - KV가 빛나는 자리: 세션·feature flag·API key·configuration·hot read
  - KV가 무너지는 자리: 검색·정렬·강한 일관성 — Liftosaur 사례를 솔직히 인용
  - D1 — SQLite at edge·JOIN/CTE/트랜잭션 가능·1 DB 10GB·자동 read replica
  - D1 sustained write: 500~2k/s — write-heavy(2k+ TPS) 워크로드는 부적합 (Hyperdrive 예고편)
  - **D1 + Drizzle 본격 실습** — 마이그레이션·타입 안전성·`drizzle-kit` 워크플로우
  - **Spring `@Transactional` 멘탈을 어떻게 옮길까** 박스 (1~2쪽)
  - 비교 표: D1 vs Neon vs PlanetScale vs Turso (각자의 sweet spot)
  - 의사결정 플로차트 1: 내 데이터는 KV인가 D1인가 (다음 챕터 DO·R2와 함께 마무리)
  - 실습: 6장에서 만든 사용자 API에 D1 + Drizzle 스키마·마이그레이션을 추가, 세션은 KV에 그대로
  - **챕터 끝 박스 — "KV·D1이 무너지는 자리"**
- **예상 분량:** 22~26쪽 / 약 9,500 단어
- **의존성:** 6장
- **실습 결과물:** 6장 사용자 API에 D1 + Drizzle이 붙고, 세션 저장소는 KV로 분리된 형태로 진화. `drizzle-kit migrate`까지 한 번 돌아본다. (누적)

---

### Chapter 8. 데이터 2 — Durable Objects와 R2, 그리고 Cache API

- **챕터 한 줄 요약:** Actor 모델·강한 일관성·WebSocket Hibernation을 가진 Durable Objects, egress free의 R2, 요청 단위 ephemeral Cache API를 워크로드 패턴별로 다룬다.
- **핵심 질문**
  1. Durable Objects는 왜 "DynamoDB의 trans 버전"이 아니라 actor 모델로 이해해야 하는가?
  2. R2의 egress free는 어떤 워크로드에서 진짜 의미가 있고, 어디서 환상이 깨지는가?
- **주요 내용**
  - Durable Objects의 본질: 전역 단일 인스턴스 + 고정 위치 + 강한 일관성 + 자체 SQLite
  - Erlang/Elixir/Akka/Orleans와의 친척 관계
  - **Spring `@Async`·Akka actor와 Durable Objects의 거리** 박스 (1~2쪽)
  - 유즈케이스: 채팅방·실시간 협업 문서·재고·예약·턴 게임·per-user rate limit·multiplayer
  - **WebSocket Hibernation API** — long-lived connection의 비용 모델을 뒤집는 한 수
  - DO migrations: 클래스 추가·이름 변경 시 `[[migrations]]` 태그 필수, 안 그러면 배포 거부
  - R2 — S3 호환 API의 어디까지가 호환이고 어디부터 다른지 (Lifecycle·Glacier·Object Lock 부재)
  - egress free의 진짜 의미와 한계: Class A/B operations 과금, AWS→R2 inbound는 AWS egress로 잡힘
  - presigned URL·multipart upload·`aws-sdk` endpoint만 바꾸기 패턴
  - Cache API — 요청 단위 ephemeral KV. CloudFront edge cache와 무엇이 다른가
  - 의사결정 플로차트 2 (완성판): KV / D1 / DO / R2 / Cache API / Hyperdrive 6갈래 분기
  - 실습: `toby-shop` 고객지원 채팅방 DO + WebSocket Hibernation + R2에 첨부 파일 업로드 + presigned URL 발급 한 사이클
  - **챕터 끝 박스 — "DO·R2가 무너지는 자리"**
- **예상 분량:** 24~28쪽 / 약 10,000 단어
- **의존성:** 7장 (KV·D1)
- **실습 결과물:** `toby-shop` 어드민 옆에 WebSocket 고객지원 채팅방 Worker 1개 신규. 본문은 DO storage에, 첨부는 R2 presigned URL로. (누적 — Worker 2 분기)

---

### Chapter 9. Next.js on Cloudflare — Workers Static Assets·OpenNext의 현실

- **챕터 한 줄 요약:** 데이터 두 챕터로 백엔드 깊이에 들어간 호흡을 프론트로 한 번 환기. Pages가 Workers Static Assets로 흡수된 흐름과 OpenNext 어댑터의 현재 한계를 정직하게 정리하고, 어떤 Next.js 앱은 옮겨도 되고 어떤 앱은 미루는 게 옳은지 의사결정선을 그린다.
- **핵심 질문**
  1. Pages가 maintenance 모드인 지금, 새 Next.js 앱은 어디에 배포해야 하는가?
  2. OpenNext on Cloudflare가 어디까지 production을 견디는가?
- **주요 내용**
  - Pages → Workers Static Assets 흡수의 배경과 현 시점(2026 5월) 권장
  - 3가지 옵션 비교: Pages (legacy), Workers Static Assets, `@opennextjs/cloudflare`
  - Edge Runtime export 미지원 — Vercel용 코드를 그대로 옮기면 무엇이 깨지는가
  - 스크립트 크기 한도 (Free 3MiB / Paid 10MiB)와 Sharp·Prisma engine 같은 큰 의존성 처리
  - SSR·ISR·SSG·Edge runtime — Cloudflare에서 각각 어떻게 실현되는가
  - 이미지 최적화: Cloudflare Images vs Vercel Image Optimization 비용·기능 비교
  - velopert (veltrends) Pages → Vercel 회귀 사례를 솔직히 인용 — 모든 Next.js 앱이 이전 대상은 아니다
  - Vinext (2026 실험적 라인) 추적 가이드 — 책 출간 후 어떻게 따라가야 하는지
  - 실습: `toby-shop` 상점 프론트(SSR + 이미지 최적화 + ISR 한 페이지)를 OpenNext로 빌드해 Workers Static Assets에 배포
  - **챕터 끝 박스 — "OpenNext가 무너지는 자리"**
- **예상 분량:** 20~24쪽 / 약 8,500 단어
- **의존성:** 3장, 6장
- **실습 결과물:** `toby-shop` 상점 프론트(Next.js 14)가 Workers Static Assets + Worker SSR로 배포되어 7장 사용자 API와 연동. Cloudflare Images로 상품 이미지 최적화 동작. (누적 — Web 1 신규)

---

### Chapter 10. Hyperdrive로 RDS를 그대로 살려두기 — 가장 risk-low한 첫 발걸음

- **챕터 한 줄 요약:** 프론트 환기 후 다시 백엔드로. D1으로 옮기지 않고도 Aurora·RDS를 그대로 두고 edge에서 빠르게 — 점진 이행의 핵심 무기를 손에 쥔다. 다음 11장 Zero Trust(EC2 사설망 끌어오기)와 자연스럽게 이어진다.
- **핵심 질문**
  1. Workers는 TCP 직접 연결이 안 되는데 어떻게 RDS를 쓸 수 있는가?
  2. Hyperdrive 도입은 기존 RDS·Aurora 운영을 무엇이든 깨뜨리는가?
- **주요 내용**
  - Workers의 TCP 한계와 Hyperdrive가 푸는 문제 (TCP 1 + TLS 3 + DB auth 3 = 7 round-trip 흡수)
  - Hyperdrive는 DB가 아니라 connection pool + query cache다 — 이름의 함정
  - **JDBC HikariCP ↔ Hyperdrive 비교 한 페이지** — Spring 개발자의 다리
  - AWS RDS·Aurora에 그대로 붙이는 절차 (publicly accessible 옵션·Security Group·SSL)
  - transaction mode 동작 — 한 트랜잭션 동안 연결 점유, 끝나면 풀로 반환
  - Drizzle / Kysely / pg 라이브러리와의 호환성
  - 2025년 가격 정책 — 무료 plan에서도 Hyperdrive 사용 가능
  - 점진 이전의 첫 걸음으로서의 Hyperdrive — "DB는 AWS, 컴퓨트는 Cloudflare" 하이브리드 패턴
  - 실측 케이스: 해외 사용자 p95 응답시간이 어떻게 줄어드는지 (레퍼런스 §10.3 인용)
  - 함정: connection limit·long-running transaction·prepared statement 차이
  - Neon serverless Postgres + Hyperdrive 조합 — 풀패키지 edge Postgres 패턴
  - **챕터 끝 박스 — "Hyperdrive가 무너지는 자리"**
- **예상 분량:** 18~20쪽 / 약 7,500 단어
- **의존성:** 6장 (Workers), 7장 (D1과의 경계)
- **실습 결과물:** `toby-shop`의 주문 도메인을 가상의 Aurora-compat Postgres(또는 Neon free)에 Hyperdrive 바인딩으로 붙은 Worker로 구성. Drizzle로 마이그레이션·쿼리까지 동작. (누적)

---

### Chapter 11. 보안과 Zero Trust — Access·Tunnel·WAF·Turnstile·Auth.js

- **챕터 한 줄 요약:** AWS Verified Access·IAM·Cognito·Site-to-Site VPN의 자리를 Cloudflare One 스택이 어떻게 다시 채우는지, 그리고 일반 사용자 인증은 Auth.js·Lucia·Clerk을 어떻게 얹는지 정리한다.
- **핵심 질문**
  1. IAM의 정교한 정책 언어를 잃은 자리에 Cloudflare에서 무엇을 세워야 하는가?
  2. EC2 private subnet을 외부에 노출하지 않고 어떻게 Cloudflare로 안전하게 끌어오는가?
- **주요 내용**
  - Cloudflare One / Zero Trust 스택 한눈에 — Access·Tunnel·Gateway·CASB
  - Cloudflare Access — SaaS·자체 앱 앞단의 SSO + device posture, OIDC/SAML IdP, 브라우저 기반 SSH/VNC
  - Cloudflare Tunnel (cloudflared) — EC2 private subnet을 outbound-only로 끌어오는 표준 패턴 (10장 Hyperdrive와 짝)
  - WAF + Bot Management + Turnstile + API Shield — 통합 보안 스택의 레이어 구성
  - Turnstile은 invisible challenge — 일반 사용자에게 CAPTCHA UI 안 보임
  - Workers 인증 라이브러리 4가지 비교: Auth.js / Lucia / Clerk / 자체 (Hono + JWT + KV)
  - Workers Secrets / Secrets Store / `.dev.vars` — secret 관리의 3중 레이어
  - 실습 1: Auth.js + D1 어댑터로 소셜 로그인 (Google·GitHub) — `toby-shop`의 사용자 로그인
  - 실습 2: cloudflared로 Mac 로컬 또는 EC2의 어드민 대시보드를 Cloudflare Access 뒤로 노출
  - 함정: IAM처럼 세밀한 IAM policy 언어가 없으므로 Bindings + Access policy + WAF rule 3중 조합으로 권한을 표현해야 함
  - **챕터 끝 박스 — "Zero Trust가 무너지는 자리"**
- **예상 분량:** 20~24쪽 / 약 8,500 단어
- **의존성:** 6장 (Workers), 8장 (DO·R2 — bucket 권한 패턴), 10장 (Hyperdrive 사설망)
- **실습 결과물:** `toby-shop`에 소셜 로그인이 붙고 어드민 페이지가 cloudflared + Access 뒤에 노출. WAF rule·Turnstile 위젯까지 연결. (누적)

---

### Chapter 12. AI·Workflows·Queues — Step Functions·SQS·`@Scheduled` 너머

- **챕터 한 줄 요약:** edge inference의 Workers AI, 글로벌 분산 벡터 DB Vectorize, 모델 프록시 AI Gateway를 Bedrock과 비교해 자리매김하고, 같은 챕터에서 Workflows·Queues·Cron Triggers로 비동기·orchestration·스케줄의 빈자리를 채운다. 1차안에서 누락 지적된 비동기 영역을 본격 다룬다.
- **핵심 질문**
  1. Bedrock을 그대로 쓰면서도 AI Gateway를 앞단에 두는 게 왜 의미가 있는가?
  2. **Step Functions의 ASL을 코드로 다시 쓰면 어떻게 보이는가?**
  3. **Spring `@Scheduled`·Spring Batch를 Cloudflare에서는 어떻게 대체하는가?**
  4. Workers AI vs Bedrock — 어떤 워크로드를 어디로 보내야 하는가?
- **주요 내용**

  **Part 1. AI 영역 (12쪽 내외)**
  - Workers AI — Cloudflare GPU 인프라 위 LLM·임베딩·이미지 모델, Neuron 단위 과금
  - Bedrock vs Workers AI 의사결정 표 — latency-critical edge·간편함은 Workers AI / VPC 격리·Knowledge Bases·enterprise feature는 Bedrock
  - Vectorize — 글로벌 분산, 인덱스당 5M vector, 계정당 50k namespace, **hybrid search 미지원** (2026 기준)
  - pgvector / OpenSearch와의 비교 표 — 언제 Vectorize, 언제 기존 OpenSearch 유지
  - **AI Gateway** — 70+ 모델 / 12+ provider 단일 endpoint, 캐싱(최대 90% 지연 감소), rate limit, retries, model fallback, 비용·토큰 분석
  - AI Gateway를 Bedrock 앞에 두는 패턴 — AWS 모델은 그대로 두고 관측·캐시만 Cloudflare로

  **Part 2. Workflows — durable execution 멘탈 모델 (8쪽 내외)**
  - Workflows의 본질: durable execution. 코드가 step 단위로 영속되고, instance가 죽어도 다음 step부터 재개
  - **Step Functions ASL ↔ Workflows step API** 코드 비교 한 페이지
  - `step.do(...)` / `step.sleep(...)` / `step.waitForEvent(...)` — 외부 대기는 비용에 잡히지 않는다는 비용 모델
  - Spring Batch와의 거리 — 짧은 multi-step orchestration은 Workflows, 거대한 배치는 ECS 유지 (5장 결정 프레임 재인용)
  - 실습: 결제 후 영수증 발송 Workflow (결제 검증 → DB 기록 → 이메일 큐 push → 영수증 PDF 생성 → R2 저장 → 사용자 알림)

  **Part 3. Queues — SQS·EventBridge의 자리 (6쪽 내외)**
  - Queue producer/consumer 한 사이클
  - 배치 소비·재시도·dead-letter queue
  - SQS와의 비용·기능 비교 표
  - 실습: 위 Workflow의 이메일 발송 부분을 Queue consumer로 분리

  **Part 4. Cron Triggers — `@Scheduled`의 자리 (4쪽 내외)**
  - cron 문법과 wrangler.toml 설정
  - Spring `@Scheduled` ↔ Cron Trigger 매핑 표
  - 실습: 매시 정각마다 외부 health check를 돌고 실패 시 Queue로 알림 발사

  **Part 5. Agentic 영역 짧은 둘러보기 (2~3쪽)**
  - Dynamic Workers (open beta) — AI agent의 untrusted code 실행 sandbox
  - Cloudflare Agents API — Queues + Workflows + DO를 묶은 멀티 step agent
  - 실습: 작은 RAG 챗봇 — Vectorize에 문서 임베딩 저장 → AI Gateway 거쳐 Workers AI 또는 Bedrock에 질문 → 응답 캐싱

  **챕터 끝 박스 — "Workflows·Queues·AI 각각이 무너지는 자리"**

- **예상 분량:** 28~32쪽 / 약 12,500 단어 (1차안 11장 20~24쪽에서 비동기·스케줄 통합으로 자연 확장)
- **의존성:** 6장 (Workers), 8장 (DO — Agents에서 actor 모델 재활용), 5장 (결정 프레임 — 무엇을 Workflows로 옮길지)
- **실습 결과물:** `toby-shop`에 결제 후 영수증 Workflow + 이메일 Queue + 매시 health check Cron이 추가되고, 어드민 옆에 작은 RAG 챗봇이 붙는다. 같은 질문 두 번째에는 AI Gateway 캐시 hit으로 응답 시간이 명백히 줄어든다. (누적)

---

### Chapter 13. 운영과 정직한 한계 — 비용·관측·outage·lock-in

- **챕터 한 줄 요약:** 이 책이 Cloudflare 광고가 아님을 가장 분명히 드러내는 장. 비용 모델의 함정, observability 공백, 2025년 outage 교훈, vendor lock-in을 정직하게 다룬다.
- **핵심 질문**
  1. Workers의 "I/O 대기 시간 무료" 가격 모델이 깨지는 시나리오는 어떤 모습인가?
  2. 단일 벤더 의존의 위험을 안고 갈 만한 회피 전략은 무엇인가?
- **주요 내용**
  - Workers Standard 가격 모델 깊이 — CPU time × 요청 수, I/O 대기 무료
  - 실측 사례 비교: Baselime 95% 절감 (검증) / TechPreneur $50K 절감 [unverified — 정직하게 표기] / Liftosaur 회귀 사례
  - egress free의 진짜 한계: Class A/B operations·AWS→R2 inbound 청구서·요청 수 누적
  - Observability 공백 — CloudWatch 단일 제품 부재, Logpush + 외부 APM(Datadog·New Relic·Baselime·Axiom·Sentry) 조합이 표준
  - Workers Logs 실시간 tail vs Logpush 구조적 export — 어떤 상황에서 무엇을 쓰는가
  - **2025년 11월 18일 outage 케이스 스터디** — Bot Management config 파일이 ClickHouse 권한 변경으로 2배 크기가 되어 proxy panic, Workers KV·Turnstile·Dashboard까지 영향. 본문은 압축, 상세 타임라인은 부록 F로 분리
  - 2025년 12월 5일 outage와 두 사건이 가르쳐 준 것
  - **단일 벤더 의존 회피 전략** — DNS는 secondary 운영, 핵심 데이터는 R2 외에 백업 sink 1곳, critical path는 Workers + Lambda 이중 운영(Rebal AI 사례)
  - **Vendor lock-in 정직한 인식** — Workers 코드 자체는 Web standards로 portable하지만 Bindings·DO·D1·KV API는 Cloudflare 고유
  - V8 보안 패치를 Chrome stable보다 먼저 production에 푸는 정책 — 빠른 보안 vs 검증 안 된 패치 양가성
  - 운영 체크리스트 한 페이지: 배포 전·배포 후·incident response·정기 점검
- **예상 분량:** 20~22쪽 / 약 8,500 단어 (outage 상세 타임라인은 부록 F로 분리해 본문 슬림화)
- **의존성:** 1~12장의 모든 기술 챕터
- **실습 결과물:** `toby-shop`에 Logpush(R2) + Sentry observability 한 사이클이 추가되고, 단일 벤더 의존 점검표 한 장이 채워진다. (누적 — 운영 레이어)

---

### Chapter 14. 마이그레이션 전략 — Strangler Fig 8단계로 어떻게 옮기는가

- **챕터 한 줄 요약:** 5장에서 "무엇을 옮길 것인가"를 결정했다면, 14장은 "어떻게 옮길 것인가"의 시퀀스다. Spring Boot + Lambda + DynamoDB + S3 스택을 점진적으로 Cloudflare로 끌어오는 8단계 시나리오. 아무것도 부수지 않고 가장 risk-low한 순서로.
- **핵심 질문**
  1. 어떤 순서로 옮겨야 한 번에 너무 많은 것이 흔들리지 않는가?
  2. 5장에서 결정한 "Move now" 항목들을 어떤 시퀀스로 풀어낼 것인가?
- **주요 내용**
  - Strangler Fig 패턴의 본질 — 옛 나무를 베지 않고 새 나무가 옛 나무를 감싸 자라게 한다
  - **8단계 권장 순서**: DNS → CDN/WAF → Tunnel(사설망) → Edge 로직(Lambda@Edge) → API Gateway → Stateless Lambda → Data (S3→R2 / DDB→KV·D1·DO) → AI(Bedrock + AI Gateway) + 비동기(Step Functions → Workflows)
  - 각 단계의 위험·예상 효과·롤백 전략을 한 표에 (레퍼런스 §10.3 시나리오 확장)
  - 가상 시나리오 — 월 $8,000 스택을 24주에 걸쳐 $2,500~$3,500로 이전하는 4단계 로드맵
  - **하이브리드가 최종 형태일 수 있다** — DB는 AWS, 컴퓨트는 Cloudflare; Heavy job은 ECS, edge·API는 Workers; Backup은 R2, primary는 S3
  - 5장 결정 프레임 재호출 — "옮기지 말아야 할 것"은 14장에서도 옮기지 않는다
  - 실측 지표 모니터링: 비용·p95·error rate를 어디에서 어떻게 보는지
  - 책의 마지막 약속 — Cloudflare를 "도입"하지 말고, 자기 아키텍처에 "올바른 자리"를 내주자
- **예상 분량:** 22~26쪽 / 약 9,500 단어
- **의존성:** 1~13장 모두 (마이그레이션은 책 전체의 응축)
- **실습 결과물:** 5장에서 만든 결정 워크시트 + `toby-shop` 누적 프로젝트 위에 그린 "8단계 마이그레이션 로드맵" 워크북 — 각 단계마다 위험·예상 효과·롤백 전략·KPI를 채워 넣은 한 장의 그림. (분기 — 책의 마지막 능동 학습)

---

## 4. 내러티브 아크

이 책은 독자의 감정을 한 직선이 아니라 활처럼 휘게 만든다. 호기심 → 혼란 → 첫 성공 → 지도 → 결정 → 자신감 → 실무 적용 → 정직한 위험 인식 → 결단의 곡선이다.

- **호기심 (1장)**: "Cloudflare가 또 하나의 클라우드가 아니라고? 그렇다면 무엇인가?" 책을 펼친 사람이 다음 페이지로 넘어갈 이유를 만든다.
- **혼란 (2장)**: V8 isolate·리전 부재·Bindings를 마주하며 익숙한 가정이 흔들린다. 의도된 혼란이다 — 멘탈 모델을 갈아엎지 않으면 이후 챕터는 모두 1:1 매핑의 함정에 빠진다.
- **첫 성공 (3장)**: Mac에서 5분 만에 Hello World가 글로벌 PoP에 배포된다. 손끝의 성취가 머리의 혼란을 진정시킨다.
- **지도 잡기 (4장)**: 매핑 카탈로그로 전체 영토를 한눈에 본다. 1:1 매핑이 거짓말이 되는 경계를 미리 표시해 둠으로써 다음 챕터들의 깊이 있는 탐험을 예고한다.
- **결정 (5장 — 신설)**: 매핑을 본 직후 "그래서 내가 무엇을 옮길 것인가"의 결정 프레임을 손에 쥔다. 이 챕터가 6~12장의 깊이 있는 기술 챕터에 들어가기 전 호흡을 끊고, 책 전체의 약속("올바른 자리를 내준다")의 도구를 본격 챕터로 약속한다. 5장 끝의 결정 워크시트는 14장 마이그레이션 시퀀스의 베이스가 된다.
- **자신감 (6장)**: Spring 멘탈을 Hono로 다시 그리며 "내가 알던 것을 잃지 않는다"는 안도감을 얻는다. 비교 코드 한 쌍이 이 챕터의 감정 핵심.
- **데이터 깊이 (7·8장)**: KV·D1·DO·R2를 워크로드 패턴별로 다루며 가장 깊은 기술 곡선에 들어간다. 8장 끝의 의사결정 플로차트에서 자신감이 1차 정점에 이른다.
- **호흡 환기 (9장)**: 데이터 두 챕터의 누적 피로를 Next.js·OpenNext로 한 번 환기. 백엔드에서 프론트로 점프하며 시야가 한 번 트인다.
- **백엔드 복귀와 점진 이전 (10장)**: Hyperdrive로 RDS를 그대로 살리며 "아무것도 부수지 않아도 된다"는 안도감을 얻는다. 9장의 환기 후 다시 백엔드로 돌아오면서 11장 보안과 자연스럽게 연결된다.
- **확장 (11·12장)**: Zero Trust 보안과 AI·비동기·스케줄 영역으로 확장된다. 12장은 1차안에서 누락됐던 Workflows·Queues·Cron Triggers를 본격 다뤄 Step Functions·SQS·`@Scheduled` 개발자의 빈자리를 채운다. 책의 폭이 가장 넓어지는 지점.
- **정직한 위험 인식 (13장)**: 책 전체에서 가장 무거운 챕터. 2025년 outage 사례·observability 공백·vendor lock-in을 마주하며 "이 책은 광고가 아니다"라는 신뢰가 굳어진다. 감정 곡선이 한 번 가라앉는다.
- **결단 (14장)**: 가라앉은 감정 위에 8단계 마이그레이션 로드맵이 얹힌다. 5장의 "무엇을 옮길 것인가"가 14장의 "어떻게 옮길 것인가"로 닫힌다. 마지막 페이지에서 독자는 "내 시스템에 Cloudflare가 어디까지 들어와도 좋은가"에 대해 자기 답을 갖게 된다.

각 챕터 사이에는 짧은 전환 문단을 두어 ("앞 장에서 우리는 ...을 살펴봤다. 이제 ...을 다뤄보자") 흐름이 끊기지 않도록 한다.

---

## 5. 부록

### 부록 A — Wrangler CLI 치트시트

- 자주 쓰는 명령 한 페이지 (init·dev·deploy·tail·secret·types·d1·kv·r2·queues·workflows)
- 환경별 명령 패턴 (`--env staging`, `--remote`, `--local`)
- 트러블슈팅 자주 묻는 5가지

### 부록 B — AWS ↔ Cloudflare 빠른 진단 카드

- 4장 매핑을 그대로 압축하는 게 아니라, **증상 → 매핑 깨짐 패턴 → 어디로 가야 하나** 형식으로 차별화
- 컴퓨트·스토리지·DB·네트워크·보안·관측·AI·비동기 8개 영역
- "1:1이 깨지는 곳"을 색상으로 표시
- 5장 결정 워크시트와 짝을 이루는 의사결정 보조 카드

### 부록 C — 비용 시뮬레이션 워크시트 + 폭주 시나리오

- Workers / R2 / D1 / DO / Workers AI / AI Gateway / Workflows / Queues 단가표 (2026 5월 기준 + 갱신 가이드)
- "내 워크로드 비용 추정" 빈 칸 워크시트 — 트래픽·egress·DB write·LLM neuron 입력 → 월 비용 산출
- AWS 동일 워크로드와의 비교 칸
- **비용이 폭주하는 5가지 시나리오 + 각각의 조기 경고 신호** (13장 본문과 보완 관계)

### 부록 D — 추천 라이브러리·도구 목록 + Python Workers 한 페이지

- Hono / Drizzle / Kysely / Auth.js / Lucia / Clerk / Cloudflare Vite plugin / OpenNext / vitest-pool-workers
- 외부 APM 선택 가이드 (Sentry / Baselime / Axiom / Datadog / New Relic)
- **Python Workers 한 페이지** — 1장에서 의도적 제외로 명시한 영역의 우회로 안내

### 부록 E — 책 이후 추적 가이드

- Cloudflare 변동성이 크기 때문에 분기마다 체크할 공식 페이지·블로그·커뮤니티 목록
- Vinext·Dynamic Workers·Workers Containers GPU·Vectorize hybrid search 같은 "곧 바뀔" 영역 추적 포인트
- 한국어 커뮤니티 추적 채널 (RIDI·velog·OKKY·페북 그룹)

### 부록 F — 트러블슈팅 모음 (신설)

- **2025-11-18 / 12-05 outage 상세 타임라인** (13장 본문에서 분리)
- Hyperdrive 연결 실패 패턴 5가지 (SG·SSL·publicly accessible·prepared statement·long-running tx)
- OpenNext 빌드 에러 자주 보이는 7가지
- DO migrations 배포 거부 메시지 해독표
- Workflows instance 멈춤 디버깅 절차
