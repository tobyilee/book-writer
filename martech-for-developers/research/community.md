# Martech 커리어·현장 커뮤니티 리서치

검색 수행일: **2026-07-25**
담당 축: 커리어·조직·현장 pain point·한국 시장 지형 (F-1 ~ F-5)
slug: `martech-for-developers` / genre: `tech-book`

## 수집 방법과 신뢰도 규율 (먼저 읽을 것)

이 문서의 모든 인용은 **이 세션에서 실제로 내려받은 페이지·API 응답에서 복사한 것**이다. 검색 스니펫이나 요약 모델이 재구성한 문장은 인용으로 쓰지 않았다.

- **인용 파이프라인:** 인용할 것은 전부 `curl`로 원본(JSON/HTML)을 받아 추출했다. 요약형 페치는 "이 페이지에 채용 공고가 있는가" 같은 **탐색 용도로만** 썼다.
- **사용한 1차 채널:**
  - HN Algolia API (`hn.algolia.com/api/v1/search?tags=comment`, `/items/{id}`) — 댓글 원문(`comment_text`/`text`) 그대로
    - ⚠️ **HN 개별 댓글 URL(`news.ycombinator.com/item?id=...`)은 Algolia `objectID`에서 파생한 것**이며, 개별 HN 페이지를 직접 열지는 않았다. 매핑 규칙은 확정적이지만 "조회했다"고는 할 수 없다.
  - Greenhouse Job Board API (`boards-api.greenhouse.io/v1/boards/{slug}/jobs`) — 해외 JD 원문
  - 원티드 내부 API (`wanted.co.kr/api/chaos/jobs/v1/{id}/details`) — 국내 JD 원문(주요업무/자격요건/우대사항 필드 그대로)
  - GitHub Search API, 기업 엔지니어링 블로그·기술 블로그 HTML
- **라벨 규약:**
  - `커뮤니티 주장 (검증 필요)` — 익명 개인의 진술. 사실로 격상 금지.
  - `관찰 사실` — "이런 불만이 N건의 독립 소스에서 반복 관찰됐다"는 것 자체. 이건 기록해도 되는 사실.
  - `(2차 인용)` — 벤더/언론이 자기 주장으로 낸 수치.
  - `조회 불가` — 접근 실패. 기억으로 메우지 않았다.

> ⚠️ **책 저술 시 주의:** 이 문서의 pain point는 **영어권 HN 비중이 크다.** Reddit이 차단돼 실무자 표본이 한쪽으로 기울었다(아래 "조회 불가" 참조). 한국 현장 목소리는 **개인 커뮤니티 글이 아니라 벤더 기술블로그·채용 공고**에서 주로 확보됐고, 이건 이해관계가 있는 소스다. 이 편향을 챕터에서 감춰서는 안 된다.

---

# F-1. 채용 공고 원자료 (전부 2026-07-25 조회)

채용 공고는 "면접·업무에서 실제로 요구되는 역량"의 **1차 소스**다. 커뮤니티 인상론보다 이쪽이 훨씬 단단하다.

## F-1-A. 국내 (원티드 API, 조회일 2026-07-25)

### AB180 (에이비일팔공) — 원티드 기업 ID 476

조회 시점 **active 공고 24건**. 전체 직무 타이틀(원문 그대로):

```
Security & Privacy Compliance Manager / Head of Sales / Revenue Operations Team Lead /
Account Manager / Security & Privacy Team Lead / Endpoint Security Engineer (Junior) /
Enterprise Account Executive / Technical Writer / Partnership Manager / Account Executive /
Finance Manager / Global Technical Support Manager / Technical Support manager /
Solution Architect / Customer Success Manager - Onboarding / DevOps Engineer /
Head of Customer Success / Customer Success Manager - Amplitude & Braze /
QA Engineer (병역특례 가능) / Backend Engineer - Data Pipeline / Marketing Team Lead /
Product Manager / Sales Strategy Manager / Head of Product
```

**관찰 사실:** active 24건 중 **순수 소프트웨어 엔지니어 공고는 3건**(Backend Engineer - Data Pipeline, DevOps Engineer, Endpoint Security Engineer)이고, **기술을 쓰지만 개발자가 아닌 직무**(Solution Architect, Technical Support Manager ×2, CSM-Onboarding, CSM-Amplitude & Braze, QA, Technical Writer)가 **7건**이다. 이 비율 자체가 이 책의 핵심 논지 중 하나다 — Martech 벤더사에서 "기술을 아는 사람"의 자리는 개발자 자리보다 넓다.

---

#### [1] Backend Engineer - Data Pipeline (공고 ID 330977, active)

원문 그대로:

**주요업무**
```
• 사용자가 광고 서버를 거쳐 원하는 곳으로 잘 이동할 수 있도록 도와주는 웹 서버를 개발합니다.
• 실시간으로 수집되는 대용량 이벤트를 분석하여 마케팅 성과를 고객에게 제공합니다.
• 글로벌 광고 파트너사들과의 server to server 연동을 지원합니다.
```

**자격요건**
```
• 3년 이상의 웹 백엔드 개발 경력, 또는 그에 준하는 역량을 가지신 분
• Kotlin 또는 Golang 을 활용한 백엔드 개발 경험이 있으신 분
• AWS, GCP, Azure와 같은 클라우드 서비스 위에서의 개발 경험이 있으신 분
• 테스트 코드 작성 경험이 있으신 분
```

**우대사항**
```
• Kafka 또는 Queue를 활용한 분산 처리 개발 경험이 있으신 분
• Grafana, New Relic, Sentry와 같은 모니터링 도구 사용 경험이 있으신 분
• 더 적은 비용으로 시스템을 운영하는 비용 관리 경험이 있으신 분
• 시스템이 휴먼 에러를 잡아줄 수 있는 환경을 구축해 보신 분
```

> 📌 **책에 쓸 포인트:** 우대사항에 **"더 적은 비용으로 시스템을 운영하는 비용 관리 경험"**과 **"시스템이 휴먼 에러를 잡아줄 수 있는 환경"**이 나란히 있다. Martech 백엔드는 기능 개발보다 **비용·안정성**이 먼저다. 아래 AB180 엔지니어링 블로그 인터뷰(F-2)와 정확히 호응한다.

#### [2] Solution Architect (공고 ID 370636, active) — "개발자 아닌데 개발 알아야 하는" 직무의 표본

**주요업무**
```
• 솔루션 도입단계에서 SDK 설치법과 제품 사용법에 대한 세션을 진행합니다.
• 제품 사용 과정에서 Customer Success Manager, Engineering Group, 고객사 개발팀 등
  여러 채널과의 협업을 통해 고객이 대면하는 다양한 기술적 문제를 해결합니다.
• 신규 기능 및 업데이트 내용을 선제적으로 파악하고, 전사 및 고객사에 효과적으로 공유합니다.
• 이슈를 체계적으로 관리하고, 솔루션 가이드 작성 및 제품 개선에 적극 기여합니다.
```

**자격요건**
```
• 2년 이상의 안드로이드 혹은 iOS 개발 경험이 있거나 하나 이상의 기술 언어(Java, Kotlin, Swift 등)에 능통하신 분
• 개발자 및 비개발자와 논리적이고 구조화된 커뮤니케이션이 가능하신 분
• 모바일 및 웹 기술에 대한 이해도가 있으신 분
• 비즈니스 영어 커뮤니케이션이 가능하신 분
```

**우대사항**
```
• 비즈니스 케이스, 마케팅 업계 니즈 등에 대한 이해가 있으신 분
• 세일즈 엔지니어링 또는 솔루션 컨설팅 등 유관 업무 경력이 있으신 분
• Mar-Tech SaaS 솔루션 사용 경험이 있으신 분(Airbridge, Braze, Amplitude, Google Analytics, Mixpanel 등)
• Backend 또는 Data Warehouse 관련 기본지식이나 실무 경험이 있으신 분
```

#### [3] Customer Success Manager - Onboarding (공고 ID 370582, active)

**주요업무 발췌**
```
• 에어브릿지, 브레이즈, 앰플리튜드 등 솔루션의 초기 연동 가이드를 제공하고 실행할 수 있도록 지원합니다.
• SDK와 API를 활용하여 데이터가 안정적으로 전송·연동될 수 있는 구조를 설계하고 적용 과정을 관리합니다.
```
**자격요건 발췌**
```
• API, SDK 등의 복잡한 테크 지식을 쉽고 효과적으로 전달할 수 있으신 분
• 마케팅팀·제품팀 등 다양한 부서와 협업하여 데이터 흐름을 설계·개선한 경험이 있으신 분
```
**우대사항 발췌**
```
• Attribution, CRM, Product Analysis (Airbridge, Appsflyer, Braze, Insider, Amplitude, GA4 등)
  솔루션 사용 또는 연동 경험이 있으신 분
```

#### [4] DevOps Engineer (공고 ID 365460, active)

**주요업무**
```
• AWS와 Kubernetes(K8S) 기반 서비스 인프라를 운영하고 고도화합니다.
• 생산성과 안정성을 높이기 위한 개발 환경과 CI/CD 파이프라인을 운영하고 고도화합니다.
• SRE(Site Reliability Engineering) 및 Observability 시스템을 운영하고 고도화합니다.
• 비용 가시성을 높이고 효율을 개선하는 FinOps를 운영하고 고도화합니다.
```

> 📌 **FinOps가 DevOps JD의 4대 업무 중 하나로 명문화**돼 있다. Martech에서 비용은 곁가지가 아니라 직무 정의다.

---

### 빅인사이트 (원티드 기업 ID 31825) — Data Platform Engineer (공고 ID 359453, active)

조회 시점 active 공고 **1건**. 이 1건이 국내 Martech 데이터 플랫폼 스택의 가장 구체적인 표본이다.

**주요업무 (원문)**
```
• AWS EKS 기반 데이터 플랫폼 운영 및 개선
• Argo Workflows 기반 배치/데이터 처리 파이프라인 설계, 운영, 장애 대응
• Go 또는 Python을 활용한 데이터 처리 도구, 운영 자동화 도구, 내부 CLI 개발
• Apache Iceberg 기반 데이터 레이크 테이블 운영
• S3 기반 데이터 적재, 변환, 검증, backfill 파이프라인 관리
• MongoDB 기반 데이터 저장소 운영, 스키마 설계, 인덱스/쿼리 성능 개선
• Vitess/MySQL sharding 환경 운영 및 장애 대응
• ClickHouse 기반 OLAP/분석 워크로드 운영 및 성능 최적화
• Flink 기반 streaming/batch 워크로드 운영
• Kubernetes 리소스 request/limit, HPA, Karpenter, nodegroup 기반 스케일링 최적화
• Prometheus/Grafana 기반 모니터링 지표 정의 및 알람 개선
• AWS 비용 구조를 고려한 리소스 최적화
• 장애 발생 시 로그, 메트릭, 이벤트 기반 원인 분석 및 재발 방지
```

**"What Makes A Strong Fit" (원문 — 이건 그대로 챕터에 쓸 만하다)**
```
• 데이터 파이프라인과 Kubernetes 운영을 함께 볼 수 있는 분
• 실패한 워크플로우를 단순 재실행하지 않고 원인과 재발 방지까지 보는 분
• DB, 스토리지, 워크플로우, 인프라를 분리해서 보지 않고 전체 병목을 추적할 수 있는 분
• 배치 처리의 idempotency, backfill, retry, 중복 처리 문제를 중요하게 생각하는 분
• 비용과 안정성 사이의 트레이드오프를 숫자로 판단할 수 있는 분
• 반복적인 운영 작업을 코드와 자동화로 줄이는 분
• 데이터 품질, 처리 지연, 리소스 병목을 운영 지표로 관리하려는 분
```

> 📌 **"실패한 워크플로우를 단순 재실행하지 않고 원인과 재발 방지까지 보는 분"** — 이 한 줄이 Martech 데이터 엔지니어의 일상을 요약한다. 재실행으로 때우고 싶은 유혹이 상시 존재한다는 뜻이기 때문이다.

---

### 마티니아이오 (원티드 기업 ID 37366) — 솔루션 컨설턴트 (공고 ID 349957, active)

조회 시점 active 공고 **12건**. 그중 개발/기술 직무는 사실상 이 1건이고, 나머지는 CRM 마케터·CSM·세일즈·BA다. **국내 Martech 대행/컨설팅 회사의 인력 구성**을 보여주는 표본.

**주요업무 (원문)**
```
1. 마테크 아키텍처 설계
   Appsflyer / Amplitude / Braze 기반 전체 데이터 구조 설계
   SDK / Server-side / Hybrid 트래킹 전략 수립
   이벤트 택소노미(Event Naming, Property 구조) 설계
   데이터 품질 확보를 위한 수집 기준 및 검증 프로세스 정의

2. 시스템 연동 및 기술 설계
   고객사 개발 환경에 맞는 시스템 연동 및 기술 설계
   세일즈단에서의 기술 관련 고객사 개발/기술 관련 문의 응대

3. 기술 이슈 해결 및 고도화
   데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅
   대용량 데이터 환경에서의 성능/비용 최적화 구조 설계
   고객사의 데이터/마케팅 구조 개선 제안

4. 내부/외부 기술 리딩
   CSM/AE/CRM팀/그로스팀 등과 협업하여 기술 의사결정 지원
   고객사 개발팀과 직접 협업하여 구현 방향 가이드
```

**자격요건 발췌**
```
• 데이터 흐름을 End-to-End로 이해하고 설명할 수 있는 분
• API / Webhook / ETL 구조에 대한 이해를 갖추신 분
• 테스트 목적의 간단한 클라이언트/서버 환경 구축이 가능하신 분
• 여러 이해관계자(개발, 마케팅, 기획)와 커뮤니케이션 할 수 있는 능력이 있으신 분
```

> 📌 **이 JD는 F-3의 pain point 목록을 그대로 업무 정의로 옮겨놓은 문서다.** "데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅"이 **직무기술서에 명시**돼 있다는 건, 그게 예외 상황이 아니라 상시 업무라는 뜻이다. 챕터 오프닝으로 강력하다.

---

### 채널코퍼레이션 / 채널톡 (원티드 기업 ID 8)

조회 시점 active 공고 **40건**. 기술 직무: Software Engineer(222071), Software Engineer, Senior(338292), DevOps Engineer(162049), Applied AI Engineer(294072), MachineLearning Engineer(346442), **Forward Deployed Engineer(324639)**, Data Analyst(358218), AX Consultant(376537).

#### Forward Deployed Engineer (공고 ID 324639, active) — 원문 발췌
```
• 고객사 현장(데이터, 프로세스, 조직 구조 등)을 깊이 이해하고, 실제 문제를 정확히 진단한 뒤,
  빠르게 해결 방안을 설계·구현·검증하여 즉각적인 비즈니스 임팩트를 만드는 역할을 합니다.
• AX팀, 세일즈, CS, 운영, 제품팀 등과 긴밀히 협업하며, 설계한 AI 기반 솔루션이
  현장에서 안정적으로 작동하도록 끝까지 책임지고 개선합니다.
• 위 과정에서 만들어진 프로토타입과 레시피를 재사용 가능한 형태로 정리하여,
  제품팀이 이를 기반으로 보다 넓은 고객에게 제공할 수 있도록 스케일 가능한 구조로 전환합니다.
```
**자격요건 첫 항목이 기술이 아니다:**
```
• 회복 탄력성 : 복잡한 이해관계와 반복되는 실패 속에서도 빠르게 회복하고,
  새로운 해결책을 집요하게 탐색하는 분
```

> 📌 자격요건 5개 중 **기술 스택 언급이 0개**이고, 전부 태도·커뮤니케이션·학습 민첩성이다. Forward Deployed 계열 직무의 성격을 보여주는 좋은 대조 사례.

#### [참고] 채널톡 백엔드 서버 개발자 (공고 ID 34197) — **마감된 공고**
`status: close`, `due_time: 2022-12-14`. 즉 **2022년 공고**다. 현재 스택의 근거로 쓰면 안 된다.
공고 본문에 초봉 관련 문구("초봉을 업계 최고 수준인 6,500만 원으로 인상했습니다")가 있으나 **2022년 시점 회사 자기 주장** `(2차 인용, 시점 2022)`.

> ⚠️ **신선도 경고 — 채널톡 DAU 수치 충돌:** 검색 요약은 "하루 800만명"을, 마감 공고(2022) 본문 기반 요약은 "3 million daily"를 제시했다. **두 수치 모두 이 세션에서 1차 확인하지 못했다.** → `확인 불가`. 책에서 채널톡 규모를 쓰려면 공식 발표를 별도 확인할 것.

---

## F-1-B. 해외 (Greenhouse Job Board API, 조회일 2026-07-25)

| 회사 | 보드 slug | 전체 공고 | 엔지니어링·기술 관련 | 비고 |
|------|-----------|----------|---------------------|------|
| Braze | `braze` | 236 | 79 | HTTP 200 |
| Klaviyo | `klaviyo` | 152 | 63 | HTTP 200 |
| Twilio (Segment 모회사) | `twilio` | 183 | 92 | HTTP 200 |
| Hightouch | `hightouch` | 70 | 34 | HTTP 200 |
| Census / RudderStack / Snowplow / Segment / mParticle | — | — | — | **조회 불가** (Greenhouse 404, 다른 ATS 사용 추정) |

### 반복 등장하는 "개발자 외 기술 직무" — 실제 공고 타이틀

이게 F-1에서 가장 중요한 발견이다. 네 회사에서 **동일 계열 직무가 대량으로 반복**된다:

**Solutions Engineer / Solutions Consultant (프리세일즈)**
- Hightouch: `Solutions Engineer, Enterprise East (Pre-Sales)`, `Solutions Engineer, Enterprise West (Pre-Sales)`, `Solutions Engineer, Mid-Market (Pre-Sales)`, `Solutions Engineer, Mid-Market, EMEA`, `Solutions Engineer, Senior Enterprise (Pre-Sales)`, `Manager, Solutions Engineering`, `Manager, Solutions Engineering, Mid-Market` — **7건**
- Braze: `Solutions Consultant, Emerging Enterprise, General Business` ×5(도시별), `Solutions Engineer, Security & Privacy` ×4, `Lead Solutions Consultant`, `Senior Lead AI Solutions Consultant`, `Team Lead, Solutions Consulting`, `Team Lead Solutions Consultant, Financial Services` ×3, `Solutions Architect`, `Technical Architect`, `Senior Lead Field Architect` ×4
- Twilio: `Presales Engineer`, `Senior Presales Engineer`, `Principal Presales Engineer` ×3, `Presales Architect`, `Senior Manager, Presales Engineering`
- Klaviyo: `Lead Solution Engineer (Presales)`, `Senior Pre-Sales Solutions Engineer - Enterprise`, `Senior Solution Architect - Professional Services`

**Technical Account Manager (TAM)**
- Braze: `Technical Account Manager` ×5(Chicago/SF/Toronto/NYC/Austin)
- Hightouch: `Technical Account Manager` (India), `TAM, Enterprise (East)`, `TAM, Enterprise (West)`, `TAM, Mid-Market`
- Twilio: `Technical Account Manager` ×6

**Forward Deployed 계열 — 2026년 현재 확산 중**
- Hightouch: `Forward Deployed Analytics Engineer`(2026-07-21 갱신), `Forward Deployed Marketing Data Scientist`
- Twilio: `Forward Deployed Engineer` ×2 (US, UK)
- Braze: `Forward-Deployed Data Scientist`(Tokyo), `Forward-Deployed Data Scientist II`(Paris, London)
- 채널톡(국내): `Forward Deployed Engineer`

**Deliverability(도달률) 전담 직무 — 별도 커리어 트랙으로 존재**
- Braze: `Senior Email Deliverability Consultant` ×4(Austin/NYC/Chicago/SF, 2026-07-17 갱신), `Team Lead, Email Deliverability` ×4
- Klaviyo: `Deliverability Strategist`(London)
- Hightouch: `Deliverability Specialist`

**Analytics Engineer**
- Klaviyo: `Analytics Engineer`(Boston, 2026-07-23 갱신)
- Twilio: `Staff, Analytics Engineer, GTM Data Science & Analytics`
- Hightouch: `Forward Deployed Analytics Engineer`

**제품 도메인이 그대로 팀 이름인 엔지니어 직무 (Martech 특유)**
- Klaviyo: `Senior Software Engineer - Profiles, Lists and Segments`, `Lead Software Engineer, Messaging Infrastructure`, `Software Engineer II, Messaging Infrastructure`, `Senior Product Manager, Profiles Platform`, `Lead Product Manager, Core Data`, `Software Engineer - Advanced Reporting`, `Engineering Manager - Data Automation`, `Senior Integrations Engineer`
- Braze: `Engineering Manager, Data Streaming`, `Engineering Manager, Email` ×5, `Senior Software Engineer, Content Cards`, `Senior Software Engineer I, Reporting`
- Twilio: `Software Engineer, (L2) CDP`, `Principal Software Engineer - Identity Graph`, `Software Engineer (L2) Email`, `Staff, Software Engineer (L4) - Email`, `Software Engineer (L3) Data Substrate`, `Staff Software Engineer (L4) Data Platform`, `Software Engineer, Identity`
- Hightouch: `Software Engineer, Streaming Systems`, `Principal Engineer, Streaming Systems`, `Software Engineer, Destinations`(EM), `Software Engineer, Customer Studio Backend`, `Software Engineer, Native Delivery`, `Software Engineer, Control Plane`, `Software Engineer, Distributed Systems`

> 📌 **`Principal Software Engineer - Identity Graph`(Twilio), `Software Engineer, (L2) CDP`(Twilio), `Senior Software Engineer - Profiles, Lists and Segments`(Klaviyo)** — 이 세 타이틀만 봐도 Martech 백엔드의 핵심 문제가 무엇인지 드러난다: **아이덴티티 해석(identity resolution)과 프로필/세그먼트 저장·조회**. 일반 웹 백엔드에는 없는 도메인이다.

### 해외 JD 본문 발췌 (원문, 조회일 2026-07-25)

**Hightouch — Solutions Engineer, Mid-Market (Pre-Sales)** (갱신 2026-06-30)
> "This role is for someone who wants to own the technical win. As a Mid-Market Solutions Engineer at Hightouch, you will partner with your Account Executives to drive the full technical sales motion from deep discovery and architectural solutioning to tailored product demonstrations and rigorous technical validation. You will own relationships with technical champions, co-develop account strategy, and guide customers to our solutions by navigating complex, multi-stakeholder buying committees..."

Hightouch 자사 소개 문구 `(2차 인용, 벤더 자기 주장)`:
> "Hightouch is an Agentic Marketing Platform powered by the industry-leading Composable CDP. ... Named a Leader in the 2026 Gartner® Magic Quadrant™ for Customer Data Platforms, Hightouch is trusted by leading enterprises like Domino's, Spotify, Aritzia, Cars.com, Ramp, and PetSmart."

**Braze — Technical Account Manager** (갱신 2026-07-01)
> "As a Technical Account Manager, you will own the ongoing technical relationship through the entire lifecycle of customers in your portfolio, collaborating very closely alongside the Customer Success and wider account teams. This role will serve as a trusted technical advisor responsible for defining the Braze technology strategy for customers who have purchased the TAM premium service offering and helping them unlock value from their use of the Braze platform."

**Klaviyo — Analytics Engineer** (갱신 2026-07-23)
> "Our Analytics Engineering team sits within a hub-and-spoke model, partnering closely with Go-To-Market (GTM), Product, Engineering, and Business Intelligence teams to build scalable, trusted data systems. You'll work at the intersection of business and engineering, owning core data models, enabling self-service analytics... This role combines deep technical execution with high-impact business partnership, requiring you to translate ambiguous needs into scalable data products."

**Hightouch — Forward Deployed Analytics Engineer** (갱신 2026-07-21)
> "We are looking for a highly analytical and customer-obsessed Forward Deployed Analytics Engineer to bridge the gap between our customers' complex legacy reporting environments and the future of agentic data exploration. Sitting within the Solutions & Success organization, you will be the tip of the spear in helping our enterprise customers activate the full power of Hightouch's Agentic CDP. Your core mission is to deeply understand our customers' existing marketing and BI reports, reverse-engineer their logic, and cleanly tra[nslate]..."

> 📌 **"reverse-engineer their logic"** — 고객사가 이미 쓰던 리포트의 계산 로직을 역설계하는 게 직무의 핵심 미션으로 적혀 있다. F-3의 "숫자가 안 맞는다" 문제와 정확히 같은 뿌리다.

---

## F-1-C. 반복 등장 기술 스택·요구 역량 집계

**집계 근거:** 위에서 **본문까지 실제로 읽은 국내 공고 7건**(AB180 4건, 빅인 1건, 마티니 1건, 채널톡 FDE 1건) + **해외 공고 본문 4건** + 해외 타이틀 268건. 표본이 작으므로 "출현 빈도"이지 "시장 점유율"이 아니다.

### 언어·런타임
| 항목 | 근거 |
|------|------|
| **Python** | 빅인 Data Platform(필수), AB180 Data Engineer(검색 요약 기반이라 `미확인`) |
| **Go(Golang)** | AB180 Backend-Data Pipeline(필수, Kotlin 택1), 빅인(필수, Python 택1) — **2/2 국내 데이터 파이프라인 공고에서 필수 후보** |
| **Kotlin** | AB180 Backend-Data Pipeline(필수, Go 택1) |
| **Java/Kotlin/Swift** | AB180 Solution Architect(택1 능통) |

### 데이터 인프라 (국내 공고 본문 기준 출현)
| 항목 | 출현 |
|------|------|
| **Kubernetes / EKS** | 빅인(필수), AB180 DevOps(필수) — 2건 |
| **AWS** | 빅인, AB180 Backend, AB180 DevOps — 3건 |
| **workflow orchestration (Argo/Airflow/Dagster)** | 빅인(필수) |
| **Kafka / Queue 분산처리** | AB180 Backend(우대) |
| **ClickHouse** | 빅인(필수 업무 + 우대 상세) |
| **Apache Iceberg / S3 데이터레이크** | 빅인 |
| **Flink (streaming/batch)** | 빅인 |
| **Vitess / MySQL sharding** | 빅인 |
| **MongoDB** | 빅인 |
| **Prometheus / Grafana** | 빅인(필수), AB180 Backend(우대: Grafana/New Relic/Sentry) |
| **Snowflake / BigQuery** | 마티니 솔루션 컨설턴트(우대) |

### 도메인 지식 — "우대사항"에 반복 등장하는 것
**Martech 제품명 자체가 우대사항**이라는 게 이 업계의 특징이다.
- `Airbridge, Braze, Amplitude, Google Analytics, Mixpanel` — AB180 Solution Architect 우대
- `Airbridge, Appsflyer, Braze, Insider, Amplitude, GA4` — AB180 CSM-Onboarding 우대
- `Appsflyer / Amplitude / Braze` — 마티니 솔루션 컨설턴트 주요업무
- `MMP, CRM, PA(Product Analytics)` — 마티니 우대
- `Attribution` — AB180 CSM 우대, 마티니 주요업무

**즉 "MMP / CDP / CRM / PA" 4개 약어와 대표 제품명은 개발자도 반드시 알아야 하는 어휘다.** (→ F-5)

### 비기술 요구 역량 (반복)
| 역량 | 출현 |
|------|------|
| **개발자·비개발자 양쪽과 소통** | AB180 SA, AB180 CSM, 마티니 SC, 채널톡 FDE — **4/7 국내 공고** |
| **비즈니스 영어** | AB180 SA(필수), AB180 CSM(필수) — 2건 |
| **비용·안정성 트레이드오프** | AB180 Backend(우대), AB180 DevOps(FinOps), 빅인(Strong Fit) — 3건 |
| **문서화·가이드 작성** | AB180 SA, 마티니 SC — 2건 |

---

# F-2. Martech 회사의 팀 구성과 역할

## F-2-A. 1차 소스: AB180 엔지니어링 블로그 — Data Pipeline Team 인터뷰

출처: https://engineering.ab180.co/stories/data-pipeline-team-interview
글쓴이: Soeun Choi(최소은) / 인터뷰이: Backend Engineering Group, Data Pipeline Team Lead 김재원
게시일: **페이지에서 확인 불가** (`조회 불가`) / 조회일 2026-07-25

> ⚠️ 게시일이 페이지에 없어 **시점 미상**이다. 본문에 "지금 백엔드 엔지니어링 그룹은 총 19명" 같은 조직 규모 수치가 있는데, **시점 없는 조직 수치**이므로 책에 그대로 쓰면 위험하다. 쓸 거면 "인터뷰 당시" 라고 명시할 것.

### 조직 구조 (원문 인용)

> "제가 합류했을 당시엔 Data Pipeline '팀'이 아니라 '파트'였는데요, 백엔드 조직 규모도 작았고 한 사람이 담당하는 백엔드 시스템의 범위도 넓어서, 각자 담당하는 파트 리드를 맡는 방식이었어요. 이후 팀원이 늘어나면서 점점 파트 규모가 커졌고, 최근에는 팀으로 승격하게 되어 제가 리드를 맡게 되었습니다. **지금 백엔드 엔지니어링 그룹은 총 19명, Data Pipeline 팀에는 저까지 7명의 팀원이 함께하고 있어요.**" `(시점 미상)`

### 역할 경계가 흐리다 — 이 책의 중요한 논지

> "저를 포함한 **AB180 백엔드 그룹의 엔지니어 분들은 흔히 말하는 백엔드, 데브옵스, 데이터 엔지니어가 하는 일을 복합적으로 하고 있습니다.** Data Pipline팀도 마찬가지인데요, 데이터 수집부터 처리, 적재 관리 등 흔히 데이터 엔지니어가 하는 영역까지 담당하고 있습니다. 전문성이 떨어질까 걱정할 수도 있겠지만, 저처럼 어느 한 분야도 놓치기 싫고, 모두 경험해보고 싶은 사람에게는 성장에 큰 도움이 된다고 생각합니다."

> 📌 **책에 쓸 포인트:** "백엔드 / 데브옵스 / 데이터 엔지니어" 경계가 Martech 벤더에서는 실무상 합쳐진다. 독자(웹/앱 개발 경험자)가 가장 궁금해할 "나는 어느 직무로 가야 하나"에 대한 현실적 답: **경계가 생각보다 흐리다.**

### 무엇이 중요한 일인가 — 안정성과 비용

> "많은 고객사가 월 수억 원에 달하는 마케팅 예산을 집행하고 비용을 정산할 때 사용하는 데이터를 다루기 때문에, **저희 팀에게는 안정성과 효율성이 가장 중요한 키워드입니다.** 그래서 신규 기능 개발만큼이나 기존 서비스의 성능 최적화 또는 안정성 보완 작업을 많이 합니다. **보통 최적화나 안정화 작업은 잘 보이지도 않고, 설명하기도 쉽지 않아 외부에서는 잘 몰라줄 때가 많지만**, 정말 중요한 작업이고 나름의 성취감도 커서 보람을 많이 느낍니다. 특히 큰 장애를 잘 방지했거나 큰 비용 절감을 이뤄낸 작업을 했을 땐 **"오늘 밥값 했다" 하며 자랑할 때가 많아요.**"

> 📌 **"오늘 밥값 했다"** — 챕터 오프닝 후보 1순위. 한국어 원문의 생활감이 살아 있고, "Martech 개발자의 성취는 눈에 안 보이는 곳에 있다"는 이 책의 주제를 한 문장으로 압축한다.

### 도메인 정의 — 개발자 관점

> "AB180은 마케팅 성과 분석 솔루션 회사입니다. **마케팅 성과 분석이란 어떤 광고를 사용자가 봤다는 것에 대한 기록, 이를 통해 설치나 구매 등의 전환을 일으켰다는 기록을 놓치지 않고 수집해서 인과관계 분석을 돕는 것**인데요, Mar-Tech는 이 과정을 기술적으로 풀어 가는 비즈니스 분야라고 생각해 주시면 됩니다."

### 비용 최적화가 "기억에 남는 프로젝트"인 이유

> "팀에서 잘 활용하고 있는 Amazon DynamoDB 비용을 최적화한 프로젝트가 가장 기억에 남습니다. DynamoDB는 사용하기 편하고, 고가용성이 잘 보장되는 만큼 비용이 많이 나가기 때문에 저희 서버 비용의 큰 부분을 차지하는 인프라 중 하나인데요, **처음에는 처리하는 트래픽에 비해 말도 안 되게 많은 비용을 내고 있어서 개선이 많이 필요했습니다.** 먼저 필요 없는 기능을 삭제하거나 스펙을 줄이는 등 정책적인 변경을 제안해서 쉽고 크게 비용을 줄였습니다. ... 처음엔 간단한 실험을 통해 **데이터 저장 방식이나 접근 패턴에 따라 어떻게 과금되는지 정확히 파악했고**, 더 효율적인 방식으로 테이블 구조를 바꿔 꽤 많은 비용을 절약했습니다."

### 비즈니스 로직의 난이도

> "제가 처음 입사했을 때 **비즈니스 로직이 어렵다고 느꼈고, 동시에 이해가 되지 않는 로직이 많았습니다.** 그래서 당시 CTO, CPO님 자리에 찾아가 옆에 앉아서 로직에 대해 토론하는 시간을 자주 가졌는데..."

> 📌 대상 독자(마케팅 도메인 지식 없는 개발자)에게 직접 꽂히는 대목. **"기술이 어려운 게 아니라 비즈니스 로직이 어렵다"**는 것이 Martech 신입의 첫 벽이다.

### 트래픽 규모 (벤더 자기 발표, `2차 인용`)
> "AB180이 직접 개발한 마케팅 성과분석 소프트웨어 에어브릿지는 200개가 넘는 고객사의 마케팅 데이터를 실시간으로 수집, 처리하고 있습니다. 비즈니스의 성장에 따라 **분당 100만건, 하루 10억건이 넘는 대용량 이벤트 데이터**가 들어오고 있고..."
> (제목은 "하루 100억 트래픽도 끄떡없는 시스템" 인데 본문은 "하루 10억건"이다 — **제목과 본문 수치가 불일치**. 책에 쓸 땐 본문 수치 + 시점 미상 명시, 또는 사용 회피 권장.)

## F-2-B. 채용 공고에서 역전 추론한 역할 지도

| 역할 | 실제로 하는 일 (JD 근거) | 부딪히는 지점 |
|------|------------------------|--------------|
| **Backend / Data Pipeline Engineer** | 이벤트 수집 웹서버, 실시간 대용량 이벤트 처리, 광고 파트너사 S2S 연동 (AB180 330977) | 비용 vs 안정성, 휴먼 에러 방지 |
| **Data Platform Engineer** | K8s·워크플로우·레이크·OLAP 운영, backfill/idempotency (빅인 359453) | 실패 워크플로우 재실행 유혹, 병목이 DB·스토리지·인프라 어디인지 |
| **DevOps / SRE** | 인프라·CI/CD·Observability·**FinOps** (AB180 365460) | 비용 가시성 |
| **Solutions / Sales Engineer (프리세일즈)** | "own the technical win", 아키텍처 솔루셔닝·데모·기술 검증 (Hightouch) / SDK 설치 세션·기술 이슈 해결 (AB180 370636) | 세일즈 일정 vs 기술적 사실 |
| **Solution Consultant** | 이벤트 택소노미 설계, SDK/서버사이드/하이브리드 트래킹 전략, **데이터 불일치·Attribution 오류·이벤트 누락 트러블슈팅** (마티니 349957) | 고객사 개발팀과 직접 협업 |
| **Implementation / Onboarding (CSM-Onboarding)** | 초기 연동 가이드, SDK·API 데이터 전송 구조 설계·적용 관리, 실무자 교육 (AB180 370582) | "복잡한 테크 지식을 쉽게 전달" |
| **Technical Account Manager** | 계약 라이프사이클 전체의 기술 관계 소유, 기술 전략 정의, 채택·리텐션 견인 (Braze) | CS팀·계정팀과의 경계 |
| **Analytics Engineer** | GTM·Product 도메인 데이터 모델 소유, self-service 분석 지원, "모호한 요구를 확장 가능한 데이터 제품으로 번역" (Klaviyo) | 비즈니스 파트너십 + 기술 실행 |
| **Forward Deployed Engineer** | 고객사 현장 진단 → 빠른 설계·구현·검증 → 재사용 가능한 형태로 제품팀 이관 (채널톡 324639) / 고객 기존 리포트 로직 역설계 (Hightouch) | **반복되는 실패**(JD가 "회복 탄력성"을 1번 자격요건으로 명시) |
| **Deliverability 전담** | Braze·Klaviyo·Hightouch 모두 별도 직무로 보유 | (JD 본문 미조회 → `조회 불가`) |

## F-2-C. 개발자와 마케터의 협업 마찰 — 프로세스 문서로 확인

출처: 마티니(Martinee) 기술블로그, "이벤트 택소노미 완벽 설계하기(1) (ft.네이버 시리즈)"
글쓴이: 문소윤 / 게시일: **2024-05-30** / 조회일 2026-07-25
URL: https://blog.martinee.io/post/designing-perfect-event-taxonomy-naver-series

이 글은 이벤트 택소노미 구축 프로세스를 **8단계**로 명시한다 (원문):

```
1. 택소노미의 목적 및 방향성 수립
2. 주요 지표(이벤트 카테고리) 설정
3. 사용자 여정(User flow) 스케치
4. 이벤트 & 프로퍼티 설계
5. 마케터 협의
6. 개발자 협의
7. QA 테스트
8. 최종 수정
```

**5~6단계에 대한 원문 서술 — 마찰이 그대로 드러난다:**

> "**5-6번 프로세스의 경우 수차례 반복될 수 있습니다.** 모든 담당자들과의 합의점이 반영된 택소노미를 설계하기까지란 많은 소통과 협의가 필요한 데다, **마케터의 요구사항을 운 좋게 완벽히 반영했다고 하더라도 기능상 점검과 동작 검증이 불가피하기 때문입니다.**"

> "**6. 개발자 협의** — 마케터와 협의 하에 설계된 1차 택소노미를 바탕으로 개발자와 검토하는 단계입니다. 개발자에게 택소노미의 전반적인 프로세스를 설명하면 **개발자는 애널리틱스를 토대로 구현 가능성을 판단합니다.** 일반적으로 마케터와 함께 미팅에 참석해 개발상의 이슈를 파악하고 개선점을 논의합니다."

> "**7. QA 테스트** — ... 담당자와 최종 협의된 논리적 설계에 따라 **데이터 로그가 올바르게 적재되는지 확인합니다.** 이 단계에서 잔존된 오류 및 결함을 발견하게 되거나..."

**택소노미 정의 (원문 — 용어 정리에 유용)**
> "이벤트 택소노미는 크게 '이벤트 유형(Event Category)', '이벤트(Event)', '이벤트 속성(Property)'의 세 가지 항목으로 구성됩니다."

**설계 전 유의사항 (원문)**
> "사실 이벤트 택소노미는 본격적으로 설계하는 당시보다, **설계하기 전 목적과 방향성을 분명히 하는 데 더 중점을 두어야 합니다. 목적과 방향성이 불분명한 상태로 설계를 시작하면 추후 수정이 잦아지고 설계가 복잡해지면서 혼동이 잦을 수 있기 때문입니다.**"

> 📌 벤더의 자사 방법론 홍보 글이라는 점은 감안해야 한다 `(이해관계 있음)`. 다만 **"마케터 협의 ↔ 개발자 협의가 수차례 반복된다"**를 벤더 스스로 프로세스 문서에 적어놓은 것은, 그 반복이 예외가 아니라 표준이라는 방증이다.

## F-2-D. 벤더사 vs 인하우스 — 개발자 경험 차이

`관찰 사실` 기반 대조 (JD·블로그 근거만):

| | **벤더사 (제품 만드는 쪽)** | **인하우스 (제품 쓰는 쪽)** |
|--|--------------------------|---------------------------|
| 근거 | AB180·빅인·Braze·Klaviyo·Hightouch JD | (직접 JD 확보 못함 → **부분 조회 불가**) |
| 규모 문제 | 전 고객사 이벤트 총량이 곧 트래픽. "분당 100만건" 급 | 자사 트래픽만 |
| 고객이 누구 | 다른 회사의 마케터·개발자. Solution Architect·TAM·CSM 계층이 두껍다 | 사내 마케터 |
| 반복되는 직무 | Solutions Engineer, TAM, Forward Deployed, Deliverability 전담 | Analytics Engineer, Growth Engineer 계열 |

> ⚠️ **인하우스 쪽 표본이 약하다.** 당근·토스·무신사·컬리·배민의 그로스/마케팅 플랫폼 직무 JD를 직접 조회하지 못했다(아래 조회 불가). 인하우스 서술은 이 문서 근거만으로 단정하지 말 것.

---

# F-3. 현장 pain point (인용 포함)

## 🥇 최고 오프닝 재료: "The Agonizing Reality of Developing Communication Services for Marketing Teams"

- HN objectID **39103276** / 작성자 **shkan** / 게시일 **2024-01-23** / 조회일 2026-07-25
- URL: https://news.ycombinator.com/item?id=39103276
- **댓글 0개** — 즉 "커뮤니티 합의"가 아니라 **한 실무자의 토로**다. `커뮤니티 주장 (검증 필요)`

원문 인용:

> "Ever set up email services? It's like living in a Groundhog Day loop. First, you create events to track stuff, then toss in a Customer Data Platform (CDP) like Segment, connect it with your email sender of choice (say hello, CustomerIO), and voila! But wait, it's not that easy. **It's a loop of integration, testing, fixing, and doing it all over again.**"
>
> "**It's not a job; it's a tech Groundhog Day where you wake up to the same problems, over and over. Bugs become your alarm clock, and every integration feels like déjà vu.**"
>
> "Now, let's groove to the dance of the back-and-forth. Create events, set up CDP, integrate with email, and **if you miss a step (like a missing field), guess what? Start from scratch.**"
>
> "Imagine your data as a puzzle, but here's the catch: **the pieces keep changing shapes.** Moving data to fit communication tools is like solving a Rubik's Cube blindfolded. Every twist and turn feels like a gamble, and just when you think you've cracked it, a missing piece throws you off."

번역(의역):
> "이메일 서비스 세팅해본 적 있나? 그건 사랑의 블랙홀(Groundhog Day) 루프 속에 사는 것과 같다. 먼저 추적할 이벤트를 만들고, Segment 같은 CDP를 얹고, 원하는 이메일 발송 도구(CustomerIO 같은)와 연결하면 짠— 그런데 그렇게 쉽지 않다. **통합하고, 테스트하고, 고치고, 처음부터 다시 하는 루프다.**"
> "**이건 직업이 아니라 기술판 사랑의 블랙홀이다. 같은 문제로 매일 아침 깨어난다. 버그가 알람시계고, 모든 연동이 데자뷰다.**"

> 📌 이 글은 **책 전체의 테제를 한 실무자가 먼저 말해버린 문서**다. 오프닝으로 쓰되, "댓글 0개인 개인 토로"임을 밝히는 게 정직하다.

## 반복 관찰 순위 (독립 소스 건수 표기)

> ⚠️ **건수 해석 규약 (중요):** 한 스레드에서 여러 명이 말한 것은 **독립 관측 1건**이다. 그래서 아래는 **`독립 스레드 수 / 발언자 수`** 두 숫자를 병기한다. 책에서 "N건에서 관찰됐다"고 쓸 때는 **앞의 숫자(스레드 수)**를 써야 한다. 채용 공고·벤더 문서는 커뮤니티가 아니므로 별도 표기했다.
>
> 그리고 이건 "업계 순위"가 아니라 **"이 표본에서의 빈도"**다. 표본은 HN에 심하게 치우쳐 있다.

### 1위. Attribution(기여도)은 원리적으로 안 맞는다 — **HN 5개 스레드 / 6명** (+ 채용공고 2건)

> 스레드 내역: "Why is it so hard to calculate ROI in Google Analytics?"(bduerst·ssharp 2명), "What if performance advertising is just an analytics scam?"(fourseventy), "Hershey Bets on Agentic AI…"(etempleton), "The Udemy Pyramid Scheme"(shopinterest), "Launch HN: Orbiter"(zhangwins)

가장 많이 관찰된 패턴. 그리고 특이하게도 **커뮤니티·JD·벤더 문서에서 모두** 나온다.

**HN 9258007 / bduerst / 2015-03-24 / story: "Why is it so hard to calculate ROI in Google Analytics?"**
> "**Marketing attribution is the bane of most marketers' existence, if only because it's never good enough.** No matter which service you're using, you're always going to find funnel use-cases that the service can't track, can't calculate, etc. It's the double edged sword of using an open web. Your best bet is to sit down, figure out what your channel KPIs are, and then try to do 85% attribution with your different activities. **Going for 100%, with GA or any other tool, is just going to drive you mad.**"

> 📌 **"85%를 목표로 하라. 100%를 노리면 미친다"** — 이건 실무 휴리스틱이다. (→ 아래 휴리스틱 섹션)

**HN 9257502 / ssharp / 2015-03-24 / 같은 스토리**
> "Marketing attribution isn't a super-easy problem to solve. But **complaining that GA doesn't know that a person saw a Facebook ad at some point before ultimately subscribing (and interacting with more ads along the way) is a bit like complaining that your car isn't also a boat and plane.** If you want comprehensive analytics, you need to spend time developing a comprehensive measurement plan and then spend time doing the reporting."

**HN 28855010 / fourseventy / 2021-10-13 / story: "What if performance advertising is just an analytics scam?"** — 어트리뷰션 회사 운영자의 자기 진술
> "It's well known that the self reported performance numbers from Google Ads and Facebook Ads are inflated, however those ad channels still do drive real value. I run an ecommerce marketing attribution company (ThoughtMetric) so I have first hand knowledge and data about this subject. **The most common source of inflation in Google/FB self reported performance numbers is multiple ad channels taking credit for the same order. If a customer clicks a Google ad then clicks a Facebook Ad then makes a purchase, each ad channel will claim credit for that purchase.**"

> 📌 **"숫자가 왜 안 맞느냐"의 가장 흔한 기술적 원인이 여기 있다:** 각 광고 플랫폼이 **같은 전환을 각자 자기 것이라고 주장**한다. 그래서 플랫폼 합계 > 실제 매출이 된다. 개발자가 마케터에게 설명해야 하는 첫 번째 개념.

**HN 48180365 / etempleton / 2026-05-18 / story: "Hershey Bets on Agentic AI to Rethink $2B in Marketing Spend"** — 가장 최신
> "My guess is they have to wait to measure the downstream impact of their marketing. And **marketing attribution is notoriously fuzzy. If a tv ad runs on may 1 what is the attribution window to someone buying a Hershey bar? How do you know they saw the ad? And that the ad influenced their purchase behavior? The answer is you really don't do you come up with some kind of formula based a few assumptions.** Ultimately I am highly skeptical. **Ad tech is almost always a repackaging of the same product with a new name.**"

**HN 7713052 / shopinterest / 2014-05-07**
> "Only very, very sophisticated systems can track multi-source/multi touch and even less can do multi attribution on the fly."

**HN 22516451 / zhangwins / 2020-03-08**
> "Was this ML attribution model output explainable / deterministic? **I've seen some really complicated marketing attribution models in the past and hear it was something of a never-ending battle to understand and arrive at the "right" model.**"

**JD 근거 (커뮤니티 아님, 회사 공식 문서):** 마티니 솔루션 컨설턴트 JD 주요업무에 `데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅` 명시. AB180 CSM 우대사항에 `Attribution` 명시.

### 2위. 이벤트 택소노미가 망가진다 / 스키마가 계속 변한다 — **HN 1개 스레드 / 1명** (+ 벤더 문서 1, 채용공고 1, GitHub 이슈 계보 1)

> ⚠️ **커뮤니티 근거가 가장 약한 패턴이다.** HN 쪽은 shkan 1명뿐이고, 나머지는 벤더 문서·JD·GitHub 이슈 제목이다. "커뮤니티에서 자주 나온다"고 쓰면 **거짓이다.** 대신 **"제품을 파는 쪽이 이걸 상시 업무로 정의해놓았다"**는 각도로 쓰는 게 정직하다.

**HN 39103276 / shkan / 2024-01-23** (위 인용)
> "**the pieces keep changing shapes**", "if you miss a step (like a missing field), guess what? Start from scratch."

**마티니 블로그 / 2024-05-30** — 프로세스 자체가 반복 루프로 설계됨
> "5-6번 프로세스(마케터 협의 ↔ 개발자 협의)의 경우 **수차례 반복될 수 있습니다.**"
> "목적과 방향성이 불분명한 상태로 설계를 시작하면 **추후 수정이 잦아지고 설계가 복잡해지면서 혼동이 잦을 수 있기 때문입니다.**"

**JD 근거:** 마티니 SC JD — `이벤트 택소노미(Event Naming, Property 구조) 설계`, `데이터 품질 확보를 위한 수집 기준 및 검증 프로세스 정의`, 그리고 트러블슈팅 항목에 `이벤트 누락`.

**GitHub — Snowplow 레포의 스키마 검증 이슈 계보** (조회일 2026-07-25)
`repo:snowplow/snowplow` + `schema validation in:title` 검색 결과 **9건**, 전부 closed. 대표:
- [#611] "Add JSON Schema-based validation for incoming unstructured events" (2014-04-01)
- [#625] "Add JSON Schema-based validation for incoming custom contexts" (2014-04-08)
- [#910] "Scala Common Enrich: add JSON Schema validation for events" (2014-07-22)
- [#3165] "Scala Common Enrich: validation errors should identify schema as well as fields" (2017-03-22)

> 📌 `관찰 사실`: Snowplow가 **2014년부터** 이벤트 스키마 검증을 파이프라인에 내장하는 작업을 해왔다는 것. "스키마를 강제하지 않으면 이벤트 데이터가 썩는다"는 문제의식이 10년 넘은 것임을 보여준다.
> ⚠️ 이슈 **본문은 미조회**(GitHub core API rate limit 소진). 제목·번호·날짜만 확인했다.

### 3위. reverse ETL / 데이터 활성화(activation)의 운영 고통과 사업적 취약성 — **HN 3개 스레드 / 5명**

> 스레드 내역: "Fivetran to acquire Census"(throwaway7783·skadamat·r1290 3명), "Fivetran, dbt Labs to merge"(knes), "The rise of industrial software"(dzonga). — 즉 **절반 이상이 한 스레드(Census 인수)에서 나왔다.** 독립 관측으로는 3건이다.

**HN 43861360 / throwaway7783 / 2025-05-01 / story: "Fivetran to acquire Census"** — 가장 날 선 진단
> "**The data is only as solid as you make it to be. Ultimately reverse ETL is just a technology (basically from SQL to APIs). The quality/correctness of data is someone else's headache. I've been there and done that, and reverse ETL is a feature-product with huge churn. See how Hightouch pivoted hard from that into CDP.**"

번역:
> "데이터는 네가 만든 만큼만 단단하다. 결국 reverse ETL은 그냥 기술일 뿐이다(기본적으로 SQL에서 API로 보내는 것). **데이터의 품질/정확성은 남의 골칫거리다.** 나도 해봤는데, **reverse ETL은 이탈률이 엄청난 기능성 제품이다.** Hightouch가 거기서 CDP로 얼마나 세게 피벗했는지 봐라."

> 📌 이 인용은 **F-3(운영 고통)과 논쟁점(컴포저블 CDP) 양쪽에 걸친다.** 그리고 실제로 Hightouch의 2026년 자사 소개가 "Agentic Marketing Platform powered by the industry-leading Composable CDP"인 걸 이 세션에서 확인했으므로, 이 실무자의 2025년 관측은 **사후적으로 맞았다**.

**HN 43861129 / skadamat / 2025-05-01 / 같은 스토리** — 방향에 따라 난이도가 다르다는 통찰
> "The challenge of syncing from stubborn SaaS tools to your data warehouse / database I suspect is different than syncing data from your data warehouse / database back to SaaS tools. Specifically, **reverse ETL has to incorporate more context from the business I guess so the data that lands in the 3rd party tools is actually solid.**"

**HN 45571435 / knes / 2025-10-13 / story: "A16Z-backed data firms Fivetran, dbt Labs to merge in all-stock deal"** — 시장 통합
> "Fivetran acquired Census (reverse-etl) & Tobiko (dbt alternative). I wonder who's next to really consolidate their platform play and compete with the old legacy MDM provider like Informatica. Data Observability or Catalog like Monte Carlo and Atlan. **The whole Modern Data Stack has either died, acquired or merged by now.**"

> 📌 `커뮤니티 주장 (검증 필요)` — "Modern Data Stack이 다 죽거나 인수됐다"는 개인 관측이다. 다만 **Fivetran의 Census 인수(2025-05 HN 스토리)와 Fivetran–dbt Labs 합병(2025-10 HN 스토리)이라는 두 사건 자체는 HN 스토리 제목으로 확인**했다. 사건은 사실, 해석은 주장.
> ⚠️ 두 M&A의 **1차 소스(보도자료)는 미조회**. 책에 쓰려면 별도 확인 필요. `(2차 인용)`

**HN 46449687 / dzonga / 2026-01-01 / story: "The rise of industrial software"** — 최신
> "sometimes I wonder if people who write such articles know that 85% of commercial software is not for the Consumer Market but Enterprise / Businesses etc **where unspoken, odd rules, mismatched integrations rule the day.** something "simple" as reverse ETL - a lot of value is locked within that..."
> (※ "85%"는 이 사람의 어림수 `커뮤니티 주장 (검증 필요)`. 인용 시 수치는 빼는 게 안전.)

#### 3위 보강 — reverse ETL이 기술적으로 왜 어려운가 (Hightouch Launch HN, 2021-11-11, objectID 29188544)

이 스레드는 **댓글 47개짜리 실제 토론**이고, 아래 두 발언은 이 축의 **가장 구체적인 기술 자료**다.

**HN 29192626 / kashishg (Hightouch 공동창업자 — `벤더, 이해관계 있음`)** — 그럼에도 기술 서술은 구체적이다
> "On a high level, ETL/ELT is about sending data from your SaaS tools into your data warehouse (you are reading from different tools). Reverse ETL is about getting data from your warehouse into tools (writing into different tools). **Building ELT is a fundamentally different technical challenge than building Reverse ETL. Aspects like types, rate limits, and destination state (knowing whether data already exists in a destination) are unique to Reverse ETL. Visibility becomes challenging too as some destinations have unique quirks, like API contracts where you write to them but you don't know if the write was successful or completed until later.**"

번역:
> "**ELT를 만드는 것과 Reverse ETL을 만드는 것은 근본적으로 다른 기술 과제다. 타입, rate limit, 그리고 목적지 상태(데이터가 이미 거기 있는지 아는 것)는 Reverse ETL에만 있는 문제다.** 가시성도 어려워진다 — **어떤 목적지는 쓰기를 했는데 그게 성공했는지 완료됐는지를 나중에야 알 수 있는 API 계약을 갖고 있다.**"

> 📌 **"쓰고 나서 성공 여부를 나중에야 안다"** — 이게 reverse ETL 운영 고통(API rate limit, 동기화 실패)의 기술적 뿌리다. 챕터에서 쓸 핵심 개념. 벤더 발언이지만 **자기 제품 자랑이 아니라 문제 난이도 설명**이라 인용 가치가 있다(단, 출처를 벤더로 밝힐 것).

**HN 29191794 / tejasmanohar (Hightouch 공동창업자 `벤더`)** — 선언형 매핑과 자동 rate limit 처리
> "The syncs are declarative, not imperative. They don't map 1:1 to API calls by design. You tell us what you want the destination to look like, and we figure out how... Under the hood, **we do all the lookups, caching, batch API calls using the bulk API, automatically handle rate limits, and only send changes from your database.**"

**HN 29192643 / joshwget** — 필드 단위 source-of-truth라는 실무 원칙 (→ 휴리스틱 H7)
> "By syncing data to a particular field in Salesforce, **you're effectively saying that the source of truth for that field is the warehouse, and not Salesforce. If you expect a human to update a field, then Salesforce is the source of truth for that field, and Hightouch shouldn't write to it!**"

#### 3-B위. 실시간 세그먼트의 실제 지연 — **HN 1개 스레드 / 1명** (벤더 자기 인정)

**HN 29192403 / tejasmanohar (Hightouch 공동창업자) / 2021-11-11** — `벤더 발언이지만 자기에게 불리한 내용이라 신뢰도가 있다`
> "Good callout. Sometimes, **I joke that warehouse ingestion latency is the bane of my existence**, but it's improving... **Our average customer runs Hightouch syncs roughly every hour, but we can actually run syncs up to every minute!** HT has a lot of optimizations like only sending changes to destinations instead of all data every run."

> 📌 **"평균 고객은 1시간에 한 번 동기화한다"** — 웨어하우스 기반 활성화의 **실질 지연이 분/시간 단위**임을 벤더가 직접 말한 대목(2021년 시점). "실시간 CDP"라는 마케팅 표현과 실제 운영의 간극을 보여주는 자료.
> ⚠️ **2021-11 시점 진술이다.** 2026년 현재 수치로 쓰면 안 된다. `🕒 시점 주의`

### 3-C위. SDK가 계속 늘어난다 — 앱이 느려지는 조직적 이유 — **HN 1개 스레드 / 1명**

**HN 43668825 / Swizec / 2025-04-12 / story: "Rebuilding Prime Video UI with Rust and WebAssembly"**
> "> why is the old version so slow
> In my experience of building consumer web applications, they all start fast.
> Then someone says **"We need to track every interaction in mixpanel. What's even the point if we don't know it happened"**.
> Then the sales team says **"We need to track in Salesforce, nobody on our team looks at mixpanel"**
> Then the marketing team goes **"We must consolidate in google analytics, nothing else fits our usecase"**
> Then the other product team says **"We need Amplitude"**
> Then the re-engagement marketing team goes **"Braze for us please, we must know when customers do a thing so we can trigger cam[paigns]"**"

번역:
> "왜 옛날 버전이 느리냐고? 내 경험상 컨슈머 웹앱은 다 빠르게 시작한다. 그러다 누가 말한다 **"모든 인터랙션을 Mixpanel로 추적해야 해. 일어난 걸 모르면 무슨 의미가 있어?"** 그러면 세일즈팀이 **"Salesforce에도 추적해야 해, 우리 팀은 아무도 Mixpanel 안 봐"** 그러면 마케팅팀이 **"GA로 통합해야 해"** 그러면 다른 프로덕트팀이 **"우리는 Amplitude 필요해"** 그러면 리인게이지먼트 마케팅팀이 **"우리는 Braze요"**"

> 📌 **챕터 오프닝 후보 3순위 — 그리고 이 책 독자에게 가장 직접적이다.** "왜 우리 앱에는 추적 SDK가 다섯 개나 붙어 있는가"에 대한 답이 **기술이 아니라 조직**이라는 것. 그리고 F-3(6위)의 dlevine 인용("most companies buy 2-4 products for their marketing stack")과 정확히 호응한다.

### 3-D위. 삭제 요청 처리 / 동의 신호 — **HN 4개 스레드 / 6명**

이건 **개발자가 구현해야 하는 규제 요구사항**이라 이 책에 필수다.

**HN 30684445 / tybit / 2022-03-15 / story: "Some discouraging anecdotes on how services handle account deletions"** — 실제 해법
> "At big tech companies I've seen and heard about, the answer is **crypto shredding. Encrypt all PII at rest with a per user data key. GDPR deletion requests can then delete the data key.** This isn't perfect, but it's a step in the right direction IMO. **Unfortunately I don't see it being feasible for a typical company anytime soon.**"

> 📌 **크립토 셰레딩(crypto shredding)** — 사용자별 키로 PII를 암호화해두고, 삭제 요청이 오면 **키만 지우는** 기법. 백업·로그·파이프라인 곳곳에 흩어진 이벤트 데이터를 물리적으로 지우는 게 불가능에 가깝다는 문제를 우회한다. `커뮤니티 주장`이지만 **구체적이고 챕터에 쓸 만한 기법**이다. 다만 발언자 본인이 "일반 회사엔 당분간 현실성 없다"고 덧붙였다.

**HN 32158458 / jacksnipe / 2022-07-19 / story: "Soft deletion probably isn't worth it"**
> "The ONLY reason that you should avoid soft deletion is that **deleting things permanently in a soft-deletion-based system is hard and error prone. GDPR, among other regulations, requires that you be able to do this sometimes; and it requires that the data REALLY BE GONE.**"

> 📌 소프트 삭제(soft delete)가 기본값인 웹 백엔드 습관이 **Martech에서는 규제 위반이 된다.** 독자(웹 개발 경험자)의 기존 습관이 깨지는 지점 — 좋은 챕터 재료.

**HN 24196643 / mixedbit / 2020-08-18** — 삭제 기한 `커뮤니티 주장 (법률 해석, 검증 필요)`
> "I'm not a lawyer, but my understanding is that **GDPR requires companies to remove user data upon request in reasonable time-frame. If you keep not deletable backups for one month in order to improve reliability of your service, then my understanding is that it is fine to fulfill the GDPR data deletion requests withing one month period, not immediately.**"
> ⚠️ **비전문가의 법률 해석이다.** 책에 기한 수치를 쓰려면 GDPR 원문 확인 필수. `확인 불가`

**Deliveroo–Braze 동의 논쟁 (HN 스토리 "Deliveroo users are getting defrauded", 2019-01-24) — 3명**
- **HN 18988240 / K0nserv**:
> "I found Deliveroo **sending highly detailed location information to a marketing company(Braze)** yesterday. **I can't remember ever giving explicit consent for this and AFAIK under GDPR just covering this in a Privacy Policy is not enough.**"
- **HN 18989137 / scrollaway** (반론):
> "No, it's not that clear cut... Deliveroo clearly needs location data; **that they happen to be sending it to Braze is fine if they signed a DPA. So the question is, is the data sent to Braze exclusively for marketing? More critically: If it is collected regardless of consent, does processing still follow consent? (Collecting and processing of data are two different things)**"
- **HN 18989323 / Nursie**:
> "**under the GDPR, they must gain permission to process your information for any marketing purposes.**"

> 📌 **"수집과 처리는 다른 것"(scrollaway)** — 동의 모델 설계의 핵심 구분이고, 개발자가 이벤트 파이프라인에 **동의 신호를 어디까지 전파해야 하는지**를 결정하는 기준이다. 그리고 이 논쟁의 대상이 **Braze**라는 점이 이 책에 특히 의미 있다 — 독자가 입사할 수도 있는 회사가 프라이버시 논쟁의 한복판에 있다.
> ⚠️ 세 명 모두 **법률 비전문가의 GDPR 해석**이다. `커뮤니티 주장 (검증 필요)`

### 4위. 푸시/메시지 채널의 opt-out과 "거래성 vs 광고성" 분리 실패 — **HN 5개 스레드 / 6명**

> 스레드 내역: "Push notifications – What to push…"(joshmanders·winkelwagen 2명), "Teens inundated with phone prompts"(015a), "I only care about the helpful notifications"(fmajid), "Android features I envy as an iPhone user"(PurestGuava), "Powerful targeting for iOS push notifications"(dirtae)

이 축은 **개발자가 직접 설계로 해결해야 하는 문제**라 이 책에 특히 중요하다.

**HN 38842663 / joshmanders / 2024-01-02 / story: "Push notifications – What to push, what not to push, and how often"** — 설계 요구사항이 그대로 들어있다
> "The thing I have a problem with in this method is **you're blanket opting in or out of notifications. I'd much rather have notifications bucketed into two systems. Transactional and marketing, just like email. I should be able to opt out of Amazon's marketing push notifications without ALSO opting out of getting delivery alerts.**"

번역:
> "이 방식의 문제는 알림을 **뭉뚱그려 전체 수신/거부**한다는 거다. 나는 알림이 **이메일처럼 거래성과 마케팅성 두 개로 분리**되면 좋겠다. 아마존의 마케팅 푸시를 끄면서 배송 알림은 계속 받을 수 있어야 한다."

> 📌 **챕터 오프닝 후보 2순위.** 개발자 독자가 "아 이건 내가 만드는 쪽 얘기구나" 하고 즉시 감정 이입할 수 있는 요구사항이다. 그리고 실제로 이게 **동의(consent) 모델 설계**의 핵심이다.

**HN 38840135 / winkelwagen / 2024-01-02 / 같은 스토리** — 채널 합산 피로도
> "**It's not only push notifications, it's the combination of everything communication channel combined.** I recently unsubscribed to a services that kept spamming me their "lifetime subscription" product, while **I already was on their yearly premium plan.** Over the course of 2 weeks, I received **4 push notifications, 4 emails and 2 times when I opened the app it had a full screen ad.** I'll never use this product again. Ironically, this app focuses on sleep quality, focus and meditation."

> 📌 **"이미 연간 프리미엄 결제한 사람에게 평생 구독권을 광고했다"** — 세그먼트에서 기존 구매자를 제외(suppression)하지 못한 전형적 실패. 개발자가 만드는 세그먼트 로직의 결과가 어떻게 체감되는지 보여주는 구체 사례. 2주간 푸시 4 + 이메일 4 + 전면광고 2라는 숫자까지 있어 오프닝으로 쓰기 좋다.

**HN 37729412 / 015a / 2023-10-01 / story: "Teens inundated with phone prompts day and night"** — 다크패턴
> "Bumble is really similar and disgusting. By default, notifications are enabled for both messages (which are a pretty good thing to have notifications turned on for) and once or twice a day Peak Cringe marketing push notifications. They have the ability to turn off specific kinds of notifications, but **one of the categories is "The Good Stuff: Turning these off means you'll miss out on our most exciting pushes of all!"**"

**HN 31633159 / fmajid / 2022-06-05 / story: "I only care about the helpful notifications, not the promotional ones"**
> "Heh. **I was woken up by an Uber greenwashing marketing notification.** ... Apple's policies ban the use of push notifications for marketing purposes, but they don't enforce it nor do they provide a way for customers to report violation, so that policy is completely useless."

**HN 40096859 / PurestGuava / 2024-04-20**
> "I switched back to iPhone recently from Android and I do miss being able to silence, specifically, marketing push notifications when they arrive. **iOS is either all or nothing unless the app itself lets you selectively turn off marketing push notifications (and they usually don't).**"

**HN 4210820 / dirtae / 2012-07-07 / story: "Powerful targeting for iOS push notifications"** — 14년 전에도 같은 말
> "Please do not encourage developers to send push notifications that contain marketing messages... **Rampant abuse of push notifications in this way is ruining the push notification mechanism for developers that use them appropriately**, because users are growing tired of being blasted with unwanted push notifications, so they reflexively reject push notifications when any app asks for permission."

**HN 45265010 / callalex / 2025-09-16 / story: "Things you can do with a Software Defined Radio (2024)"** — 가장 최근 사례
> "Citizen is really enshittified... they use all kinds of predatory editorial tactics and **push notifications and marketing copy to instill primal fear that your neighborhood is imminently burning down and you will get shot if you don't subscribe to a higher tier of service from them.** Crime is way down in the US but you really don't feel that way when you are a subscriber/user of Citizen."

> 📌 `관찰 사실`: **2012년(dirtae) → 2025년(callalex)까지 13년간 동일한 불만이 반복**된다. 중간 지점도 촘촘하다(2022 fmajid, 2023 015a, 2024 joshmanders·winkelwagen·PurestGuava). "채널 피로도는 해결된 적 없는 문제"라는 서술의 근거로 쓸 수 있다.
> ⚠️ 이 문서가 확보한 **가장 최근 푸시 불만은 2025-09**다. "2026년까지"라고 쓰지 말 것.

### 5위. 이메일 딜리버러빌리티는 별도의 전문 영역이다 — **HN 5개 스레드 / 5명** ✅ (중복 없음)

**HN 9115955 / sbov / 2015-02-26 / story: "Invented here syndrome"** — 가장 정확한 요약
> "**Email, deliverability in particular, is a rabbit hole.** Its easy enough to get it set up and "basically" working, but not. Basically, you're using in your favorite language's mail sending library to send an email out. The next level is figuring out all the standards surrounding email that those third party systems know and implement for you. This will help deliverability, to a point. **Beyond that, once you hit enough volume, there's best practices should have always been doing but you learn from experience and need to abide by or else you're not getting anything through even though you do all the previously mentione[d]**"

번역:
> "**이메일, 특히 딜리버러빌리티는 토끼굴이다.** 설정해서 '기본적으로' 돌아가게 하는 건 쉽다. 그런데 아니다. ... 그 다음 단계는 서드파티 시스템들이 알아서 구현해주던 이메일 표준들을 전부 파악하는 것이다. 여기까진 도움이 된다, 어느 지점까지는. **그 너머는, 볼륨이 커지면 진작 했어야 할 베스트 프랙티스가 있는데 그건 경험으로만 배우고, 안 지키면 앞의 걸 다 해도 아무것도 안 들어간다.**"

**HN 5648393 / 13rules / 2013-05-03 / story: "Building Stuff To Help You Sell The Stuff You Build"** — 사라, 만들지 마라
> "**Do you want to become an expert in email deliverability, DNS, bounces, white listing, DKIM, SPF? Or do you want to sell your product?** It boils down to that. Spend your time doing what you are GREAT at and what you WANT to do."

**HN 8532692 / shizcakes / 2014-10-30 / story: "Startup Fuck-ups: How we lost 25% of our monthly revenue overnight"**
> "This could be solved an even more fundamental way: **Don't run your own mailer as a startup.** There are lots of companies that will be responsible for email deliverability on your behalf, via an API. If it took them 3 months to notice no mail was being sent at all, **imagine how long it's going to take them to figure out that their IP is blacklisted in Spamhaus** or any number of other deliverability issues?"

**HN 9720330 / spdustin / 2015-06-15 / story: "Show HN: A free tool to monitor and implement DMARC"** — 조용한 실패
> "We used this and discovered that **our "authenticated" Mailchimp campaigns were actually failing to be validated properly, and some email systems (especially corporate systems with spam filtering appliances like Barracuda) were not delivering our email.** DMARC didn't help tell us that our mail wasn't being delivered, per se, but once we made a change (our own spf/dkim records...) our following campaigns have seen a higher deliver rate"

**HN 7621371 / davideous / 2014-04-21 / story: "Most of the Amazon SES IP blacklisted by SpamCannibal"** — 평판의 원리
> "The key to delivering into the inbox is **sending mail that your recipients both want and expect.** Provide a good user experience, and you'll build a good reputation. **Push the limits (for example, use a "pre checked" checkbox on an order confirmation page to put people on your sales mailing list) and you'll be** [penalized]"

> 📌 `관찰 사실`: Braze·Klaviyo·Hightouch **세 회사 모두 Deliverability 전담 직무를 별도로 채용 중**(F-1)이라는 사실과, 위 5건의 "이건 토끼굴이다" 증언이 서로를 보강한다. **"왜 딜리버러빌리티 전담자가 따로 있는가"**에 대한 답이 된다.

### 6위. CDP는 무엇을 하는 회사인지 설명하기 어렵다 (정체성·프라이버시 불편) — **HN 3개 스레드 / 4명**

> 스레드 내역: "Twilio set to acquire Segment"(m463), "From Show HN to Series A in One Year"(soumyadeb·salicideblock 2명), "We already live in social credit"(jacobr1)

**HN 24737006 / m463 / 2020-10-10 / story: "Twilio set to acquire Segment for $3.2B"**
> Wikipedia 정의를 인용한 뒤: "**So nobody feels comfortable talking about what they do.**"

**HN 27553257 / soumyadeb / 2021-06-18 / story: "From Show HN to Series A in One Year"** — RudderStack 측 인사의 진술
> "Yes, we are a Segment alternative. Thanks for the feedback on positioning. **This is something we are still figuring out (and will probably do for a long time). CDP (Customer Data Platform) is a more widely known space but it's too broad. CDI (Customer Data Infrastructure) is more relevant but very few people know about it**"

**HN 27555225 / salicideblock / 2021-06-18 / 같은 스토리** — 냉소
> "The cynic in me suspects that this is intentionally obfuscated to the readers not already in the know. Where[as] a few of the general public are likely the target user of a CDP, **they are likely the actual target of the product: they will have their data and interactions detailely stored and processed via this platform. However well done this may be, it is more comfortable not to be too aware about it.**"

**HN 45106650 / jacobr1 / 2025-09-02 / story: "We already live in social credit, we just don't call it that"**
> "**The wave of CRM is CDP. Customer Data Platform. The key is that it isn't just your basic account data, but all the behavioral data across various system interactions both online and off** (if applicable). Shopping Cart abandonment email campaigns are pretty benign. But the outrage around the targeted ad for baby/pregnancy products that made the news from Target a few years ago is just the start for what more insightful data signals can give you."

> 📌 **책에 반드시 다뤄야 할 정서:** 개발자 커뮤니티에는 Martech에 대한 **윤리적 불편감**이 깔려 있다. "내가 만드는 게 감시 도구 아닌가"라는 질문. 이 책이 이걸 피하면 독자에게 정직하지 않다. 최소 한 챕터 또는 한 절이 필요하다.

### 7위. 데이터 저장소 선택과 스키마 유연성 — **HN 2개 스레드 / 2명**

**HN 30887509 / kfk / 2022-04-02 / story: "A database for 2022"**
> "I was in a demo call from Bla[ze], a CDP (Customer Data Platform), Segment.io competitor. Their underlying db seems to be MongoDB and for a CDP makes a lot of sense. **In a CDP you collect all kind of data on n hard ids that identify 1 person interacting with your web assets, schemaless and json first is a lot easier to reason in this context than SQL. This is because you keep enriching your profile with additional attributes over time.** Can PostgreSQL do this? Absolutely, but it's not its main feature."

> 📌 빅인 Data Platform Engineer JD가 **MongoDB + ClickHouse + Vitess/MySQL + Iceberg를 동시에** 요구하는 이유를 설명해준다: 프로필은 스키마리스, 분석은 OLAP, 트랜잭션은 샤딩된 RDBMS.

**HN 33816288 / ac2u / 2022-12-01 / story: "Ask HN: Should I build or buy data infrastructure products?"**
> "**Data is very much an organisation problem first, a tech problem second**, you'll have to prove to yourself and others around you that you can gain actually statistically significant insights before you invest hours and dollars. So it's in everyone's interest to get "good" working fast and cheap before you worry about perfect."

### 8위. 운영 장애 — 목적지 하나가 죽으면 전체가 느려진다 (GitHub) — **레포 1개 / 이슈 목록** (커뮤니티 발언 아님)

**RudderStack `rudder-server` 이슈 목록** (GitHub Search API, 조회일 2026-07-25)
`repo:rudderlabs/rudder-server is:issue`, comments 내림차순 상위:

| # | 제목 | 상태 | 생성일 | 댓글 |
|---|------|------|--------|------|
| 4588 | Crashing with "panic: failed to migrate ds" | open | 2024-04-18 | 23 |
| **4953** | **Rudderstack becomes extremely slow when you have one destination down** | **open** | 2024-07-31 | 16 |
| 6630 | Backup Errors: Container logs inundated with errors about archiver failing. | open | 2026-01-25 | 15 |
| 1390 | Rudderstack backend crash after sending test event | closed | 2021-10-30 | 15 |
| 6353 | RudderStack on Docker always returns 404 | closed | 2025-09-16 | 13 |
| 5079 | Clickhouse - Default Partition should be monthly rather than daily | closed | 2024-09-10 | 9 |
| 503 | High CPU usage for low traffic website. | closed | 2020-08-22 | 7 |

> 📌 **#4953 "하나의 목적지가 죽으면 RudderStack 전체가 극도로 느려진다"** — 이벤트 라우팅 시스템의 **격리(isolation) 실패**라는 전형적 아키텍처 문제. 2024-07 생성, **조회 시점 여전히 open**, 댓글 16개. Martech 파이프라인 설계 챕터의 실증 사례로 강력하다.
> ⚠️ **이슈 본문·댓글 원문은 미조회** (GitHub core API rate limit 소진: `remaining: 0`). **제목·상태·날짜·댓글 수만 확인했다.** 인용문으로 쓰려면 재조회 필요.

## 실무 휴리스틱 (커뮤니티가 공유하는 대처법)

### H1. 어트리뷰션은 85%를 목표로 하라 — 100%를 노리면 미친다
- 출처: HN 9258007 / bduerst / 2015-03-24
> "Your best bet is to sit down, figure out what your channel KPIs are, and then try to do 85% attribution with your different activities. **Going for 100%, with GA or any other tool, is just going to drive you mad.**"
- `커뮤니티 주장 (검증 필요)` — 85%라는 숫자는 근거 없는 어림수다. 다만 **"완전성을 포기하고 KPI를 먼저 정하라"는 순서**는 여러 소스가 공유한다(ssharp도 "comprehensive measurement plan"을 먼저 만들라고 함).

### H2. 딜리버러빌리티는 사라, 만들지 마라
- 출처: HN 5648393 / 13rules / 2013-05-03, HN 8532692 / shizcakes / 2014-10-30
> "Do you want to become an expert in email deliverability, DNS, bounces, white listing, DKIM, SPF? Or do you want to sell your product?"
> "Don't run your own mailer as a startup."
- ⚠️ **단, 이건 "제품 쓰는 쪽" 조언이다.** 이 책의 독자는 **제품 만드는 쪽**에 갈 수도 있고, 그쪽에서는 이게 바로 핵심 역량이다(Braze `Team Lead, Email Deliverability`). **벤더/인하우스에 따라 정반대의 조언**이 된다는 점이 이 책에서 짚을 지점.

### H3. 이벤트 택소노미는 "설계 전 목적 합의"가 설계 자체보다 중요하다
- 출처: 마티니 블로그 / 문소윤 / 2024-05-30
> "목적과 방향성이 불분명한 상태로 설계를 시작하면 추후 수정이 잦아지고 설계가 복잡해지면서 혼동이 잦을 수 있기 때문입니다."
- `벤더 방법론 (이해관계 있음)`

### H4. 알림은 거래성/마케팅성으로 분리해서 opt-out을 따로 받아라
- 출처: HN 38842663 / joshmanders / 2024-01-02
- `커뮤니티 주장`이지만 **설계 권고로서 타당하고**, 이메일에서는 이미 표준 관행이다.

### H5. 실패한 워크플로우를 재실행으로 때우지 마라
- 출처: 빅인사이트 Data Platform Engineer JD (채용 공고 = 회사 공식 문서)
> "실패한 워크플로우를 단순 재실행하지 않고 원인과 재발 방지까지 보는 분"
> "배치 처리의 idempotency, backfill, retry, 중복 처리 문제를 중요하게 생각하는 분"

### H6. 데이터는 기술 문제이기 이전에 조직 문제다
- 출처: HN 33816288 / ac2u / 2022-12-01
> "Data is very much an organisation problem first, a tech problem second"

### H7. Source of truth를 **필드 단위로** 정하라
- 출처: HN 29192643 / joshwget / 2021-11-11
> "By syncing data to a particular field in Salesforce, you're effectively saying that **the source of truth for that field is the warehouse, and not Salesforce. If you expect a human to update a field, then Salesforce is the source of truth for that field**, and Hightouch shouldn't write to it!"
- 📌 "시스템 단위"가 아니라 **"필드 단위"**로 소유권을 정한다는 발상. 사람이 편집하는 필드에는 파이프라인이 쓰면 안 된다. 동기화 충돌·덮어쓰기 사고를 예방하는 실무 원칙.

### H8. 삭제 요청은 크립토 셰레딩으로 우회한다
- 출처: HN 30684445 / tybit / 2022-03-15
> "Encrypt all PII at rest with a per user data key. GDPR deletion requests can then delete the data key."
- ⚠️ 발언자 본인이 "일반 회사엔 당분간 현실성 없다"고 단서를 달았다. `커뮤니티 주장 (검증 필요)`

### H9. 소프트 삭제를 기본값으로 두지 마라 (Martech 한정)
- 출처: HN 32158458 / jacksnipe / 2022-07-19
> "GDPR... requires that you be able to do this sometimes; and it requires that **the data REALLY BE GONE.**"

---

# F-4. 한국 Martech 시장 지형

> ⚠️ **이 절은 이 문서에서 가장 약한 부분이다.** 회사 규모·투자·고객사 수치는 공식 발표/보도자료를 1차 확인해야 하는데, **이 세션에서 그 1차 소스를 거의 조회하지 못했다.** 아래는 대부분 채용 공고·자사 블로그에서 **회사가 스스로 말한 내용**이다.

## F-4-A. 확인된 국내 플레이어 (조회일 2026-07-25)

| 회사 | 이 세션에서 실제로 확인한 것 | 확인 못한 것 |
|------|---------------------------|-------------|
| **AB180 (에이비일팔공)** | 원티드 기업 ID 476, active 공고 24건. 자사 엔지니어링 블로그 운영(engineering.ab180.co). 자사 제품 **Airbridge(에어브릿지)** = 마케팅 성과분석(어트리뷰션) 솔루션. **Braze·Amplitude를 국내에 함께 공급**(CSM 공고 타이틀 `Customer Success Manager - Amplitude & Braze`, CSM-Onboarding JD의 "에어브릿지, 브레이즈, 앰플리튜드 등 솔루션"에서 확인) | 투자·매출·고객사 수 1차 확인 불가. "아시아 유일 공식 측정 파트너", "국내 1위 MMP"는 **검색 요약에서만 본 벤더 마케팅 문구** → `확인 불가 (미조회)` |
| **채널코퍼레이션 / 채널톡** | 원티드 기업 ID 8, active 공고 40건. Forward Deployed Engineer·Applied AI Engineer·AX Consultant 채용 중 | DAU 수치 **상충**(800만 vs 3M) → `확인 불가`. 2022년 마감 공고의 초봉 6,500만원은 `(2차 인용, 시점 2022)` |
| **빅인사이트 (빅인)** | 원티드 기업 ID 31825, active 공고 1건(Data Platform Engineer). 원티드 기업 소개 문구: "자체 개발 마케팅 솔루션 **Bigin Ads**와 **Bigin CRM**을 서비스합니다" `(2차 인용, 회사 자기 소개)` | 규모·투자·고객사 전부 미조회 |
| **마티니아이오 (Martinee)** | 원티드 기업 ID 37366, active 공고 12건(솔루션 컨설턴트 1, CRM 마케터 3, CSM, BA, 세일즈 등). 자사 블로그 blog.martinee.io 운영. 원티드 소개: "파트너사의 웹/앱 서비스 성장에 필요한 Growth, CRM, Performance Marketing 풀 스택" `(2차 인용)`. 블로그에 언급된 프로젝트 고객사: "밀리의 서재 · 버거킹 · 무신사 · 한샘 · 웍스아웃 · 발란 · KFC · 두나무 · 오늘의 집" `(2차 인용, 벤더 자기 주장, 2024-05-30 기준)` | 규모·투자 미조회 |
| **노티플라이 (Notifly)** | 자사 블로그 blog.notifly.tech 운영, 카카오 알림톡 관련 실무 가이드 발행(2025-08-26). 국내 CRM/메시징 자동화 영역 | 회사 규모·제품 상세 미조회 |
| **인사이더 (Insider)** | 원티드 기업 ID **813** 존재 확인 (`인사이더(INSIDER)`) | **공고 목록·JD 미조회** → `조회 불가` |
| **그루비 (Groobee)** | 원티드에 `그루비엑스`(ID 29976)가 검색됨 — **동일 회사인지 확인 못함** | 공고·제품 전부 미조회 → `조회 불가` |
| **다이티 (Dighty)** | 원티드 검색 결과 **0건** | `조회 불가` |
| **브레이즈 코리아** | AB180이 국내에 공급한다는 사실만 간접 확인 | 한국 오피스 직접 채용 여부 `조회 불가` |

> ⚠️ **AB180이 Airbridge(자사 제품)와 Braze·Amplitude(해외 제품 국내 공급)를 동시에 다룬다**는 구조는 이 세션에서 JD 두 건으로 교차 확인됐다. 이건 한국 Martech 시장의 중요한 특징 — **국내 벤더가 동시에 해외 솔루션의 리셀러/파트너**이고, 그래서 CSM·Solution Architect 직무가 "여러 제품의 연동"을 다룬다.

## F-4-B. 한국 특유의 채널: 카카오 알림톡 — 개발 관점

출처: 노티플라이 기술블로그, "카카오 알림톡 심사 한번에 통과하기"
게시일 **2025-08-26** / 조회일 2026-07-25 / URL: https://blog.notifly.tech/alimtalk-screening-guide/
`(벤더 블로그, 이해관계 있음 — 다만 카카오 공식 가이드를 인용해 정리한 실무 문서)`

> ⚠️ **카카오 공식 개발 문서는 조회 실패**했다(아래 조회 불가 참조). 아래 내용은 **벤더가 정리한 2차 자료**다.

### 개발자에게 중요한 구조적 사실 (원문 인용)

> "카카오알림톡은 고객이 반드시 알아야 하는 주문, 예약, 결제, 배송 등과 같은 정보를 카카오톡을 통해 안내하는 서비스입니다. **알림톡은 고객의 휴대폰 번호만 있으면 카카오톡 채널 추가 여부와 관계없이 발송이 가능하며**, 문자 메시지(SMS, LMS)보다 비용이 합리적인 장점이 있습니다. **하지만 광고성 문구는 허용되지 않으며, 사전에 카카오톡 심사를 통과해야지만 발송할 수 있습니다.**"

> 📌 **이게 한국 Martech의 가장 큰 구조적 차이다.** 서구권 CRM(Braze·Klaviyo)은 이메일/푸시/SMS를 "동의만 있으면 원하는 내용을 보낼 수 있는" 채널로 다룬다. 한국의 알림톡은 **템플릿 단위로 플랫폼 사전 심사**를 받아야 한다. 즉 **메시지 내용이 배포 파이프라인의 심사 대상**이 된다. 개발자 입장에서는 "템플릿 등록 → 심사 요청 → 상태 조회"라는 **비동기 승인 워크플로우**를 시스템에 넣어야 한다는 뜻이다.

### 정보성 vs 광고성 경계 — 여기서 개발과 마케팅이 충돌한다

> "**알림톡은 고객이 확인해야 하는 정보이거나 고객이 먼저 특정 액션을 완료하고 그에 대한 결과 또는 진행 과정을 안내하는 경우에 발송할 수 있습니다.** 예를들어 주문 접수, 결제 완료, 예약 안내처럼 사실 전달이 명확한 메시지는 쉽게 승인됩니다. 하지만 이벤트 안내나 할인 혜택을 조건으로 '개인정보 등록'을 요구하거나, 수신자가 동의하지 않은 앱 설치를 유도하는 문구가 들어갈 경우 알림톡으로 발송할 수 없습니다."

> "신규 회원 가입을 축하하며, 신규 회원 쿠폰에 대한 '정보'를 제공하는 쿠폰은 어떨까요? ... **주의할 점은 신규 회원 쿠폰이 발급되었다는 내용과 함께 쿠폰 사용을 유도하는 내용이 포함되지 않아야 합니다. 고객이 직접 요청하거나 발급한 것이 아니기 때문에 광고성으로 분류되어 반려될 수 있습니다.**"

### 블랙리스트 (발송 불가 유형) — 원문 그대로

> "1) 특가 상품 알림 안내(친구톡 권장)
> 2) 장바구니 등록 상품 안내(친구톡 권장)
> 3) 포인트 지급에 명시적으로 동의하지 않은 수신자에게 발송하는 포인트 적립/소멸 메시지(마일리지, 쿠폰, 적립금 포함) 발송
> 4) 쿠폰 발급(마일리지, 포인트, 적립금 포함) 후 빠른 시일 내 소멸하는 쿠폰의 메시지
> 5) **변수만으로 구성된 메시지 불가 ex) #{상품명} #{송장정보}**"

> 📌 **"장바구니 등록 상품 안내는 알림톡 불가, 친구톡 권장"** — 서구권 CRM에서 가장 기본적인 자동화인 **장바구니 이탈(cart abandonment) 캠페인**이 한국에서는 채널을 바꿔야 한다. 이건 개발자가 캠페인 엔진을 설계할 때 **채널 라우팅 규칙**으로 구현해야 하는 도메인 지식이다.
>
> 📌 **"변수만으로 구성된 메시지 불가"** — 템플릿 엔진 설계에 직접 영향을 주는 제약. 개발자가 모르면 심사에서 반려당한다.

> "**템플릿이 승인된 이후에도 모니터링을 통해 가이드 위반이 확인될 경우 해당 템플릿에 대해 차단 조치가 취해질 수 있습니다.**"

> 📌 **승인 후에도 사후 차단이 가능**하다 — 즉 프로덕션에서 갑자기 특정 템플릿이 죽을 수 있다. 장애 대응 시나리오에 넣어야 한다.

### 쿠폰·포인트 알림톡의 필수 기재 요건 (원문)
> "포인트, 마일리지 알림톡 심사기준
> 1) 포인트 지급에 동의를 하는 경우에 '예외적'으로 가능
> 2) 비회원은 불가하며 회원에게만 발송 가능
> 3) 본문 내 '업체명' 기재 필수
> 4) 본문 내 지급 또는 소멸되는 포인트(마일리지)의 '포인트 금액', '유효기간' 기재 필수
> 5) 본문 상단 또는 하단(부가정보 영역 포함)에 적립금 안내에 대한 발송 근거를 '필수'로 기재 필수"

> 📌 이 요건들은 **템플릿 변수 스키마 설계**로 직결된다: 업체명·포인트 금액·유효기간·발송 근거가 전부 필수 필드다.

### 심사 리드타임
검색 단계에서 "4-5일간의 검수" 언급을 봤으나 **1차 확인 실패** → `확인 불가 (미조회)`. 책에 리드타임 수치를 쓰려면 카카오 공식 문서 재확인 필요.

## F-4-C. 한국 개발자 커뮤니티에서 반복되는 화제

⚠️ **이 항목은 사실상 수집 실패했다.** OKKY·GeekNews·커리어리·velog에서 Martech 관련 **개발자 토론 스레드를 확보하지 못했다**(사유는 조회 불가 목록 참조). 확보된 한국어 자료는 전부 **벤더 기술블로그**(마티니, 노티플라이, AB180)로, 이건 커뮤니티가 아니다.

`관찰 사실`: **한국어 Martech 콘텐츠 생태계는 개발자 커뮤니티가 아니라 벤더 블로그가 주도한다**는 것 자체가 발견이다. 이 세션의 한국어 검색에서 상위에 뜬 것은 전부 martinee.io / notifly.tech / bizgo.io / solapi.com / 1point.kr 같은 **솔루션 벤더의 콘텐츠 마케팅**이었다.
> ⚠️ 단, 이건 **검색 결과 상위 노출 기준의 인상**이며, 체계적 조사가 아니다. 단정하지 말 것.

---

# F-5. 개발자가 준비해야 할 것

## F-5-A. 반복적으로 요구되는 역량 — 근거와 함께

**"근거 강도" 표기:** ⭐⭐⭐ = 채용 공고 본문 다수 + 커뮤니티 교차 / ⭐⭐ = 공고 또는 커뮤니티 한쪽 / ⭐ = 단일 소스

| 순위 | 역량 | 근거 | 강도 |
|-----|------|------|-----|
| 1 | **대용량 이벤트 스트림 처리** (Kafka/Queue, 실시간+배치) | AB180 330977 주요업무·우대, 빅인 359453(Flink, Argo), AB180 블로그("분당 100만건") | ⭐⭐⭐ |
| 2 | **클라우드 + Kubernetes 운영** | 빅인(필수), AB180 DevOps(필수), AB180 Backend(필수: AWS/GCP/Azure) | ⭐⭐⭐ |
| 3 | **비용을 숫자로 판단하는 감각 (FinOps)** | AB180 Backend 우대("더 적은 비용으로 운영하는 비용 관리 경험"), AB180 DevOps 업무("FinOps"), 빅인 Strong Fit("비용과 안정성 사이의 트레이드오프를 숫자로 판단"), AB180 블로그(DynamoDB 최적화 회고) | ⭐⭐⭐ |
| 4 | **개발자·비개발자 양쪽과 소통** | AB180 SA·CSM, 마티니 SC, 채널톡 FDE(자격요건 2번) — 국내 공고 4/7 | ⭐⭐⭐ |
| 5 | **데이터 흐름을 End-to-End로 설명하는 능력** | 마티니 SC 자격요건 명문화, 빅인 Strong Fit("전체 병목을 추적"), Klaviyo AE("translate ambiguous needs") | ⭐⭐⭐ |
| 6 | **멱등성·backfill·retry·중복 처리** | 빅인 Strong Fit 명문화, AB180 Backend 우대("휴먼 에러를 잡아주는 환경") | ⭐⭐ |
| 7 | **SQL + 데이터 웨어하우스(Snowflake/BigQuery)** | 마티니 우대, Klaviyo AE 직무 전체 | ⭐⭐ |
| 8 | **모니터링·옵저버빌리티** | 빅인(Prometheus/Grafana 필수), AB180 Backend 우대(Grafana/New Relic/Sentry), AB180 DevOps | ⭐⭐ |
| 9 | **SDK 통합 경험 (iOS/Android/Web)** | AB180 SA(2년 이상 모바일 개발), AB180 CSM(SDK·API 구조 설계) | ⭐⭐ |
| 10 | **비즈니스 영어** | AB180 SA·CSM 둘 다 **필수**(우대 아님) | ⭐⭐ |
| 11 | **Go 또는 Kotlin** | AB180 Backend(택1 필수), 빅인(Go/Python 택1 필수) | ⭐⭐ |
| 12 | **실패 내성·회복 탄력성** | 채널톡 FDE 자격요건 **1번**, Hightouch FDAE("tip of the spear") | ⭐⭐ |

> 📌 **주목:** 3위(비용)와 4위(소통)가 순수 코딩 역량보다 위에 온다. 이건 표본이 작아서가 아니라, **여러 공고가 반복해서 명시**하기 때문이다. 대상 독자(웹/앱 개발 경험 풍부, 마케팅 도메인 무지)에게 전할 메시지: **부족한 건 코딩이 아니라 도메인과 비용 감각이다.**

## F-5-B. 면접 질문·과제 유형

⚠️ **수집 실패.** 잡플래닛·블라인드·면접 후기 커뮤니티를 조회하지 못했다. **"이런 질문이 나온다"고 쓸 근거가 이 문서에는 없다.**

대신 **채용 공고에서 역추론 가능한 것**만 적는다 (`추론이지 후기가 아님` — 책에서 "면접에서 나온다"고 쓰면 안 되고 "공고가 요구한다"로 써야 한다):

- AB180 Backend: Kotlin/Go 중 하나, 분산 처리(Kafka), 테스트 코드, **비용 최적화 경험담**
- 빅인: 장애 상황에서 "로그와 메트릭을 기반으로 원인을 좁혀가는" 과정 설명 — JD가 이 능력을 필수로 명시했으므로 면접에서 물을 개연성이 높다 `추론`
- AB180 SA / 마티니 SC: **비개발자에게 기술 개념을 설명하는 능력**이 자격요건이므로 검증 방식이 존재할 것 `추론`
- 채널톡 FDE: "짧은 시간 안에 PoC를 만들어 적용해본 경험"이 자격요건 — 포트폴리오/과제형일 개연성 `추론`

## F-5-C. 개발자가 반드시 알아야 할 마케팅 도메인 용어

**선정 기준:** 이 세션에서 조회한 **채용 공고 본문 또는 실무 문서에 실제로 등장한** 것만.

### 필수 (공고/문서에 반복 등장)
| 용어 | 뜻 (조회한 소스 기준) | 출처 |
|------|---------------------|------|
| **Attribution (어트리뷰션/기여도)** | "어떤 광고를 사용자가 봤다는 기록, 이를 통해 설치나 구매 등의 전환을 일으켰다는 기록을 놓치지 않고 수집해서 인과관계 분석을 돕는 것" | AB180 엔지니어링 블로그 |
| **MMP (Mobile Measurement Partner)** | 모바일 측정 파트너 | 마티니 SC 우대사항 |
| **CDP (Customer Data Platform)** | 계정 데이터만이 아니라 온·오프라인 상호작용 행동 데이터까지 모으는 플랫폼 | HN 45106650 jacobr1 |
| **CDI (Customer Data Infrastructure)** | CDP의 대안 명칭. "더 정확하지만 아는 사람이 거의 없다" | HN 27553257 soumyadeb (RudderStack) |
| **이벤트 택소노미 (Event Taxonomy)** | 이벤트 유형(Category) + 이벤트(Event) + 속성(Property) 3층 분류 체계 | 마티니 블로그, 마티니 SC JD |
| **Event / Property** | 사용자 행동(이벤트)과 그에 딸린 세부 정보(속성) | 마티니 블로그 |
| **PA (Product Analytics)** | 제품 분석 (Amplitude, Mixpanel 계열) | 마티니 SC 우대사항 |
| **Identity Graph / Identity Resolution** | 여러 식별자를 한 사람으로 묶는 것 | Twilio `Principal Software Engineer - Identity Graph`, HN 30887509("n hard ids that identify 1 person") |
| **Reverse ETL** | 웨어하우스 → SaaS 도구로 데이터를 되돌려 보내는 것. "기본적으로 SQL에서 API로" | HN 43861360 throwaway7783 |
| **Deliverability (딜리버러빌리티)** | 메일이 실제 수신함에 도달하는 능력. SPF/DKIM/DMARC, IP 평판, 블랙리스트 | HN 9115955, 9720330, 7621371 |
| **Segment (세그먼트)** | 조건으로 뽑아낸 사용자 집합 | Klaviyo `Profiles, Lists and Segments` |
| **알림톡 / 친구톡** | 한국 전용. 알림톡=정보성(채널 추가 불필요, 사전 템플릿 심사), 친구톡=광고성 | 노티플라이 블로그 |

### 조직·직무 용어 (공고 타이틀에서 확인)
`Solutions Engineer(SE) / Solutions Consultant` · `Technical Account Manager(TAM)` · `Forward Deployed Engineer(FDE)` · `Analytics Engineer(AE)` · `Growth Engineer` · `Implementation/Onboarding` · `Pre-Sales` · `GTM(Go-To-Market)` · `Professional Services`

### ⚠️ 이 문서로는 정의를 확인 못한 용어 (책에서 다루되 별도 조사 필요)
`MTU(Monthly Tracked Users)` 과금, `Consent Mode`, `Server-side Tagging`, `Cohort`, `Funnel`, `LTV`, `Churn`, `Suppression List`, `Frequency Capping`, `Holdout` (※ HN 25626483 johnrgrace가 holdout 매트릭스를 언급한 건 봤으나 정의 확인 안 됨)

---

# 논쟁점 (관점 A / 관점 B 병기)

> ⚠️ **중요한 한계:** 아래 논쟁 중 **1번은 실무자 발언을 일부만 확보**했고, 벤더 자료를 배제했다. 검색 상위에 뜬 composable vs packaged 자료는 **전부 이해관계자(cdp.com, mParticle, MessageGears, Datawhistl 등)**였고, 그들이 내놓은 "양쪽 다 옳다" 식 정리는 실무자 목소리가 아니므로 **의도적으로 제외**했다.

## 논쟁 1. 패키지형 CDP vs 컴포저블/웨어하우스 네이티브 CDP

**관점 A — 웨어하우스가 진실의 원천이어야 한다 (컴포저블 지지)**

이 진영의 **비(非)벤더 실무자 발언**은 Hightouch Launch HN 스레드(objectID 29188544, 2021-11-11, 댓글 47개)에서 확보했다.

- **HN 29190721 / pinkbeanz** — 실제로 손으로 해본 사람의 논거
> "It starts there, but then **once you get into complex workflows that merge data across your product and CRMs it all moves to the warehouse first.** Typical flow is a Fivetran or Stitch into the warehouse, lots of dbt models, then business models fit for consumption down stream. **Once in the warehouse, it needs to get back into those operational systems again, which is the tricky part. I've done these one off integrations from the warehouse into Salesforce** (creating leads, converting them, moving stages all based off product usage), **and into marketing tools** (customer segmentation built using SQL in the warehouse, then sent to marketing automation tools). **Being able to feed tools directly off the warehouse instead of writing one off integrations is t[he value]**"

번역:
> "거기서 시작한다. 그런데 **제품과 CRM에 걸쳐 데이터를 합치는 복잡한 워크플로우로 들어가면 전부 웨어하우스가 먼저**가 된다. ... **웨어하우스에 들어가고 나면 그걸 다시 운영 시스템으로 되돌려야 하는데, 그게 까다로운 부분이다. 나는 웨어하우스에서 Salesforce로 가는 일회성 연동들을 직접 해봤다**(제품 사용량 기반으로 리드 생성·전환·단계 이동), **마케팅 도구로 가는 것도**(웨어하우스에서 SQL로 만든 세그먼트를 마케팅 자동화 도구로 전송). **일회성 연동을 직접 짜는 대신 도구를 웨어하우스에서 바로 먹일 수 있다는 게 [가치다]**"

> 📌 **관점 A의 가장 좋은 근거**: 벤더가 아니라 **"일회성 연동을 직접 짜본 사람"**이 왜 웨어하우스 우선인지 설명한다. 이 책 독자가 정확히 겪게 될 일이다.

- **HN 29190740 / gurubavan** — 왜 각 SaaS에 데이터가 이미 있는데도 부족한가
> "**The Salesforce data is in Salesforce, and the HubSpot data is in HubSpot, and the Mixpanel data is in Mixpanel, but those applications don't have each others data** (not to mention missing any transformations on top). E.g. As a sales rep, you can benefit from understanding product usage and marketing activity for a contact in salesforce"

- (참고) 벤더 측 포지션 글들 — 전부 HN에서 **1~2점, 사실상 무반응**:
  - "Why Your Customer Data Platform Should Be the Data Warehouse" (hightouch.io, HN 28908715, 2021-10-18, 2 points)
  - "Ask HN: Warehouse as the Customer Data Platform?" (fivetran.com, HN 28903837, 2021-10-18, 1 point)
  - "Traditional Customer Data Platforms have failed, time for headless CDP now" (rudderstack.com, HN 33707462, 2022-11-22, 1 point)
  - "Open CDP - Turn any data warehouse into a customer data platform" (Multiwoven, HN 39698826, 2024-03-13)
  - "Castled - Warehouse-Native Braze Alternative" (Show HN, HN 34595468, 2023-01-31) — 창업자 aruntdharan:
    > "We started our journey by building an open-source Reverse ETL solution to make the warehouse data actionable to marketers. **However, after talking to 100s of marketers, we realised that modern B2C marketers needed to use billions of customer data points from the data warehouse to run personalised mark[eting]**"
  - ⚠️ `관찰 사실`: **컴포저블/웨어하우스 네이티브를 주장하는 글은 거의 전부 벤더가 올렸고, HN에서 토론이 붙지 않았다.** 실질 토론이 붙은 건 제품 런칭 스레드(29188544)뿐이다.

**관점 B-1 — 전제 자체가 의심스럽다 / 추상화가 새어나온다 (실무자 비판)**

- **HN 29190655 / pantulis** — 전제 질문
> ""They want their data in their primary tools—the SaaS applications where they spend their days—so they can use it to actually operate their business."
> I'm obviously missing something here, but thinking in terms of "operationalizing" data that comes from some kind of analytical environment, **was not the data in their operational SaaS tools in the first place?**"

- **HN 29191935 / tomnipotent** — "SQL만 쓰면 된다"는 주장에 대한 가장 날카로운 반박
> "Implicit mapping between SQL to target is great, but **how does the SQL author know what SQL to write in the first place? I've done no shortage of integrations like this, and there is no avoiding reading the target SaaS documentation to know what their schema looks like so I can shape data accordingly. Without that step, I can't even start writing SQL.**"

번역:
> "SQL에서 타깃으로의 암묵적 매핑은 좋다. 그런데 **애초에 SQL 작성자가 어떤 SQL을 써야 하는지는 어떻게 아나? 나도 이런 연동을 숱하게 해봤는데, 데이터를 맞게 빚으려면 타깃 SaaS 문서를 읽어서 스키마가 어떻게 생겼는지 파악하는 걸 피할 방법이 없다. 그 단계 없이는 SQL을 시작조차 못 한다.**"

> 📌 **"결국 목적지 API 문서를 읽어야 한다"** — 컴포저블 CDP가 약속하는 "SQL만 알면 된다"의 한계를 실무자가 지적한 대목. 이 책 독자에게 매우 실용적인 경고다. (벤더 tejasmanohar의 답변은 "declarative이고 docs·autocomplete·schema discovery로 돕는다, **still early days there**"였다 — 즉 **완전히 해결되지 않았음을 인정**.)

**관점 B-2 — reverse ETL/컴포저블은 제품으로서 취약하다**
- HN 43861360 / throwaway7783 / 2025-05-01:
> "Ultimately reverse ETL is just a technology (basically from SQL to APIs). **The quality/correctness of data is someone else's headache.** I've been there and done that, and **reverse ETL is a feature-product with huge churn. See how Hightouch pivoted hard from that into CDP.**"
- HN 43866025 / r1290 / 2025-05-02:
> "I think that both etl and reverse etl is going open source route. With this ai world we live in now. **You just need dagster or temporal - and a few lines of python.**"
- HN 45571435 / knes / 2025-10-13:
> "**The whole Modern Data Stack has either died, acquired or merged by now.**"

**참고 — 경쟁사들끼리의 공개 대화 (같은 스레드, 이례적으로 솔직하다)**

RudderStack 창업자 soumyadeb와 Hightouch 창업자 tejasmanohar가 런칭 스레드에서 직접 주고받았다. `양쪽 다 벤더`지만, **번들 vs 단일 기능이라는 이 시장의 축을 당사자들이 정의한 대목**이라 인용 가치가 있다.

- **HN 29195773 / soumyadeb (RudderStack 창업자) / 2021-11-12**:
> "RudderStack founder here. We tend to believe we have a pretty good reverse-ETL product too which can be used standalone without event collection. **Best is class is a moving target anyway and upto customers to judge :)** However, I do agree on the point around focus. Our positioning, go-to-market, pricing, use cases etc are centered around **building the end to end customer data infrastructure.** There are folks who already have pieces of the stack or don't need a full CDI (e.g. non PLG B2B companies) and only need reverse-ETL."
- **HN 29196143 / tejasmanohar (Hightouch 창업자) / 2021-11-12**:
> "**Agree RE: focus. Rudderstack is a bundle and there is a place for that.** Hightouch is 100% focused on activating data from the warehouse... just like Fivetran are laser-focused on SaaS data ingest or Snowplow on behavioral/event data ingest"

> 📌 **"번들이냐 단일 기능이냐"**가 이 시장의 실제 축이다. 그리고 F-3(3위) throwaway7783의 2025년 진단("reverse ETL은 이탈률 큰 기능성 제품")과 2021년의 이 대화를 나란히 놓으면 **4년에 걸친 시장 서사**가 만들어진다. 챕터 구성에 유용.

**이 문서의 정직한 결론:**
- **양쪽 다 비(非)벤더 실무자 발언을 확보했다** — A는 pinkbeanz·gurubavan, B는 pantulis·tomnipotent. 다만 **모두 같은 하나의 스레드(29188544, 2021-11)**에서 나왔고, **2021년 시점**이다. 🕒
- `관찰 사실`: **"패키지형 vs 컴포저블"이라는 프레이밍 자체로 HN에서 큰 논쟁이 붙은 적은 이 조사 범위에서 발견되지 않았다.** 벤더 포지션 글들은 1~2점으로 묻혔다. 이 프레이밍은 **벤더·애널리스트 담론에서 더 뜨겁고, 실무자 커뮤니티에서는 제품 단위로 이야기된다**는 게 이 표본의 인상이다.
- 책에서 "업계가 둘로 갈렸다"는 식으로 쓰면 **벤더 마케팅을 그대로 옮기는 것**이 된다. 대신 **"실무자는 진영이 아니라 구체적 마찰(목적지 API 문서, 지연, 상태 추적)로 말한다"**는 각도가 이 자료에 충실하다.
→ 📌 **후속 리서치 필요:** dbt Community Slack 아카이브, Locally Optimistic, r/dataengineering(차단 해제 시), **2024~2026년 시점의 컴포저블 토론** 재조사.

## 논쟁 2. 어트리뷰션은 유용한가, 자기기만인가

**관점 A — 불완전해도 쓸모 있다**
- HN 9257502 / ssharp / 2015-03-24:
> "complaining that GA doesn't know that a person saw a Facebook ad at some point before ultimately subscribing... is a bit like complaining that your car isn't also a boat and plane. **If you want comprehensive analytics, you need to spend time developing a comprehensive measurement plan.**"
- HN 28855010 / fourseventy / 2021-10-13:
> "It's well known that the self reported performance numbers from Google Ads and Facebook Ads are inflated, **however those ad channels still do drive real value.**"

**관점 B — 근본적으로 가정에 기댄 숫자다**
- HN 48180365 / etempleton / 2026-05-18:
> "**The answer is you really don't[;] do you come up with some kind of formula based [on] a few assumptions.** Ultimately I am highly skeptical. **Ad tech is almost always a repackaging of the same product with a new name.**"
- HN 24742387 / XCSme / 2020-10-10 (다른 사람 말을 인용하며 반박하는 맥락):
> "> Currently analytics is a fraud, analytics is useless, it is what you do about that data which is important" — 원 발언자는 미상. XCSme는 이에 반박: "This is like saying food is a scam and useless and that it's only important when you eat it."

## 논쟁 3. 딜리버러빌리티/메시징 인프라는 사야 하나 만들어야 하나

**관점 A — 사라**
- HN 5648393 / 13rules: "Do you want to become an expert in email deliverability, DNS, bounces, white listing, DKIM, SPF? Or do you want to sell your product?"
- HN 8532692 / shizcakes: "**Don't run your own mailer as a startup.**"

**관점 B — 볼륨이 커지면 자체 운영이 경제적이다**
- HN 9471320 / davideous / 2015-05-01 (MTA 제품 벤더의 발언 — `이해관계 있음`):
> "One advantage of running licensed software on your network is that **you don't pay per-message fees, so for higher volume it's really economical compared to a service like SendGrid.**"

**📌 이 책에 중요한 재구성:** 이 논쟁은 **독자가 어느 쪽 회사에 가느냐로 답이 갈린다.** 인하우스라면 A, **Martech 벤더라면 이게 곧 제품이므로 B가 아니라 "그게 우리 일"**이다. Braze가 `Team Lead, Email Deliverability`를 4개 도시에서 뽑고 있다는 사실(F-1)이 이를 뒷받침한다.

## 논쟁 4. Martech를 만드는 일은 윤리적으로 편한가

**관점 A — 정상적인 비즈니스 인프라다**
- HN 45106650 / jacobr1: "**Shopping Cart abandonment email campaigns are pretty benign.**"
- HN 11267213 / robbiemitchell / 2016-03-11:
> "there are numerous services that provide analytics and have no part in tracking you elsewhere. Is Mailchimp involved in cookie trading? Segment? Intercom? Mixpanel? **To my knowledge, no**"

**관점 B — 설명하기 불편하다는 것 자체가 신호다**
- HN 24737006 / m463: "**So nobody feels comfortable talking about what they do.**"
- HN 27555225 / salicideblock: "they will have their data and interactions detailely stored and processed via this platform. However well done this may be, **it is more comfortable not to be too aware about it.**"
- HN 45106650 / jacobr1 (같은 사람이 A와 B를 동시에 말한다):
> "**But the outrage around the targeted ad for baby/pregnancy products that made the news from Target a few years ago is just the start** for what more insightful data signals can give you. I don't really care about most retailers knowing what I buy. **I do care about them reselling that data to big aggregators that know everything I buy, where I go and when**"

## 논쟁 5. 마케팅 알림은 채널 자체를 망치는가

**관점 A — 남용이 채널을 죽인다**
- HN 4210820 / dirtae / 2012-07-07: "**Rampant abuse of push notifications in this way is ruining the push notification mechanism for developers that use them appropriately**"
- HN 37735717 / tsukikage / 2023-10-02:
> "**The entire purpose of getting you to install a mobile phone app is to push marketing notifications at you in a way that forces you to interact with them**, if only to individually dismiss them. Whatever it is /you/ want to do with the app is incidental to this"

**관점 B — 도구 문제가 아니라 분리·통제 설계 문제다**
- HN 38842663 / joshmanders: 거래성/마케팅성 버킷 분리 요구 (위 인용)
- HN 24630925 / NicolasGorden / 2020-09-29 (마케터 자기 진술 `이해관계 있음`):
> "Marketing guy here. **75%-80% open rate for many of my campaigns tells me the title is misleading**, those pixels are firing in all the major providers. **Putting people in email/SMS funnels based on which emails they read is ENOURMOUSLY beneficial to my clients.**"
> (※ 75~80% 오픈율은 **검증되지 않은 개인 주장**이며 업계 평균과 크게 다르다. 수치는 인용하지 말 것.)

---

# 확인 불가·조회 불가 목록

**이 목록은 실패의 기록이자, 후속 리서치 지시서다. 책에서 이 항목들을 아는 척하면 안 된다.**

## 접근이 차단된 채널
| 대상 | 시도 | 결과 |
|------|------|------|
| **Reddit 전체** (r/dataengineering, r/analytics, r/marketing, r/ExperiencedDevs) | `www.reddit.com/*.json` (요약 페치 + curl 양쪽) | **차단**. curl은 `<title>Blocked</title>` 반환. **이 축의 표본이 HN으로 심하게 기울어진 주원인** |
| **GeekNews (news.hada.io) 검색** | `/search?q=CDP`, `마테크`, `마케팅` | 검색 결과가 JS 렌더링. **파싱 결과 0건** |
| **잡플래닛 / 블라인드 / 면접 후기** | 미시도(로그인 벽 예상) | **F-5-B(면접 질문) 전체가 공백** |
| **카카오 비즈메시지 공식 개발 문서** | `business.kakao.com/info/bizmessage/`(연결 실패), `developers.kakao.com/docs/latest/ko/message/rest-api`(404), `kakaobusiness.gitbook.io/main/ad/bizmessage`(404) | **3개 URL 전부 실패**. 알림톡 내용은 전부 벤더 2차 자료 |
| **GitHub 이슈 본문·댓글** | `api.github.com/repos/.../issues/4953` | **rate limit 소진**(core 60/h, remaining 0). 제목·날짜·댓글수만 확보, **본문 인용 불가** |

## 조회 실패한 회사·공고
| 대상 | 결과 |
|------|------|
| **다이티(Dighty)** | 원티드 검색 0건. 전혀 확인 못함 |
| **그루비(Groobee)** | `그루비엑스`(원티드 ID 29976)가 검색됐으나 **동일 회사 확인 불가**, 공고 미조회 |
| **인사이더(Insider) 한국** | 원티드 기업 ID 813 존재만 확인, **공고·JD 미조회** |
| **브레이즈 한국 오피스** | 직접 채용 여부 미확인 |
| **Census / RudderStack / Snowplow / Segment / mParticle 채용** | Greenhouse 404 (다른 ATS 사용). **Lever/Ashby 미시도** |
| **당근·토스·무신사·컬리·배민의 그로스/마케팅 플랫폼 직무** | **전혀 미조회**. F-2-D의 인하우스 서술이 약한 이유 |
| **AB180 recruit.ab180.co 자체 채용 페이지** | JS 렌더링, 공고 목록 추출 실패 (원티드로 우회) |

## 수치 충돌·시점 미상 (책에 쓰기 전 재확인 필수)
| 항목 | 문제 |
|------|------|
| **채널톡 DAU** | 검색요약 "하루 800만명" vs 2022년 공고 기반 "3 million daily" — **둘 다 1차 미확인** |
| **AB180 엔지니어링 블로그 게시일** | 페이지에 없음. "백엔드 그룹 19명", "Data Pipeline 7명", "분당 100만건/하루 10억건" 전부 **시점 미상** |
| **AB180 블로그 제목 vs 본문** | 제목 "하루 100억 트래픽" vs 본문 "하루 10억건" — **불일치** |
| **Fivetran의 Census 인수 / Fivetran–dbt Labs 합병** | HN 스토리 제목으로만 확인. **보도자료 1차 미조회** |
| **알림톡 심사 리드타임 "4-5일"** | 검색 스니펫에서만 봄. `확인 불가` |
| **AB180 "국내 1위 MMP", "아시아 유일 공식 측정 파트너"** | 검색 요약의 벤더 마케팅 문구. **1차 미확인** |

## 🔴 요청됐으나 자료를 확보하지 못한 주제 (F-3 지정 항목 대비)

과제가 F-3에서 **명시적으로 지정한 주제** 중 이 문서가 답하지 못한 것들이다. 채널 차단이 아니라 **주제 커버리지의 공백**이므로 따로 적는다.

| 요청 주제 | 상태 | 비고 |
|----------|------|------|
| CDP 도입 실패·후회담 ("샀는데 결국 안 쓴다") | ❌ **미확보** | 도입 후회 회고를 한 건도 못 찾았다. 벤더 블로그의 "anti-patterns" 글(HN 42145030 제목만 확인)은 벤더 자료라 제외했다 |
| **벤더 락인 / MTU·이벤트 볼륨 과금 불만** | ❌ **미확보** | MTU 과금에 대한 실무자 불만 0건. `Segment pricing`, `MTU` 쿼리 미실행 |
| 실시간 세그먼트의 실제 지연·비용 | 🟡 **부분 확보** | 지연은 벤더 자기 인정 1건(3-B위, 2021년 시점). **비용 쪽은 0건** |
| 딜리버러빌리티·스팸 | ✅ 확보 (5개 스레드) | — |
| **푸시 opt-out** | ✅ 확보 (5개 스레드) | — |
| 프라이버시/동의 구현 (삭제 요청, 동의 신호 전파) | ✅ 확보 (4개 스레드, 3-D위) | 단, 전부 **법률 비전문가의 해석** |
| 마케터 요청 vs 시스템 가능의 간극 | 🟡 **간접 확보** | 마티니 블로그의 "마케터 협의↔개발자 협의 수차례 반복"과 Swizec의 SDK 증식 인용이 근접하지만, **개발자가 "이건 못 한다"고 말하는 직접 증언은 못 찾았다** |
| **AI/LLM 기능에 대한 현장 냉소 또는 실제 효용** | ❌ **거의 미확보** | 유일한 근접: HN 48180365 etempleton(2026-05-18) "Ad tech is almost always a repackaging of the same product with a new name" — Hershey의 agentic AI 마케팅에 대한 회의. **Braze/Klaviyo의 AI 기능에 대한 실사용 후기는 0건.** 반면 채용 공고 쪽은 AI 직무가 폭증 중(Braze `Applied AI Architect` ×4, `BrazeAI Operator`, Klaviyo `Customer Agent` 계열 6건+, 채널톡 `Applied AI Engineer`·`AX Consultant`) → **공고와 현장 후기 사이의 공백 자체가 흥미로운 발견이지만, 후기 없이 단정하면 안 된다** |
| GA vs 내부 DB vs 광고 플랫폼 수치 불일치 | 🟡 **원인은 확보, 현장 사례는 미확보** | fourseventy의 "여러 채널이 같은 전환을 각자 주장"이 **원인**을 설명하지만, "우리 회사에서 숫자가 안 맞아 고생했다"는 **구체 사례담은 못 찾았다** |

> 📌 **책 저술 시:** 위 ❌ 항목을 다루려면 **추가 리서치가 필수**다. 이 문서만 근거로 쓰면 안 된다. 특히 **MTU 과금 불만**과 **AI 기능 현장 반응**은 대상 독자가 실제로 궁금해할 주제인데 공백이다.

## 미시도(다음 세션 우선순위)
1. **Lever/Ashby API**로 Census·RudderStack·Snowplow·Klaviyo 외 벤더 JD 확보
2. **Stack Exchange API** (`api.stackexchange.com/2.3/search/advanced?...&filter=withbody`) — 이번에 연결은 확인했으나(30건 반환, quota 299) **내용 분석 미실시**
3. **Lobsters** `lobste.rs/s/{id}.json`, **Dev.to** `dev.to/api/articles?tag=` — 미시도
4. **국내 인하우스 JD** (당근·토스·무신사·컬리·배민 그로스/마케팅플랫폼)
5. **dbt Community / Locally Optimistic 공개 아카이브** — 논쟁 1의 A진영 실무자 목소리 확보용
6. **GitHub 이슈 본문** — rate limit 회복 후 RudderStack #4953, #4588, #6630

---

# 신선도 원장

| 소스 | URL | 게시일 | 검색 시점 | 관련 항목 |
|------|-----|--------|----------|----------|
| 원티드 AB180 기업 공고 목록 (ID 476) | `wanted.co.kr/api/chaos/companies/v1/476/jobs` | active 스냅샷 | 2026-07-25 | F-1-A, F-2-B |
| AB180 Backend Engineer - Data Pipeline | `wanted.co.kr/wd/330977` | active(마감일 없음) | 2026-07-25 | F-1-A, F-1-C, F-5-A |
| AB180 Solution Architect | `wanted.co.kr/wd/370636` | active | 2026-07-25 | F-1-A, F-2-B |
| AB180 CSM - Onboarding | `wanted.co.kr/wd/370582` | active | 2026-07-25 | F-1-A, F-2-B |
| AB180 DevOps Engineer | `wanted.co.kr/wd/365460` | active | 2026-07-25 | F-1-A, F-5-A |
| 빅인사이트 Data Platform Engineer | `wanted.co.kr/wd/359453` | active | 2026-07-25 | F-1-A, F-1-C, F-5-A |
| 마티니아이오 솔루션 컨설턴트 | `wanted.co.kr/wd/349957` | active | 2026-07-25 | F-1-A, F-2-B, F-3 |
| 채널톡 Forward Deployed Engineer | `wanted.co.kr/wd/324639` | active | 2026-07-25 | F-1-A, F-2-B |
| 채널톡 백엔드 서버 개발자 | `wanted.co.kr/wd/34197` | **마감 2022-12-14** | 2026-07-25 | F-1-A (구자료 주의) |
| Braze 채용 보드 (236건) | `boards-api.greenhouse.io/v1/boards/braze/jobs` | 개별 공고 2026-07-01~07-24 갱신 | 2026-07-25 | F-1-B |
| Braze Technical Account Manager | `boards-api.greenhouse.io/v1/boards/braze/jobs/7872122` | 갱신 2026-07-01 | 2026-07-25 | F-1-B, F-2-B |
| Klaviyo 채용 보드 (152건) | `boards-api.greenhouse.io/v1/boards/klaviyo/jobs` | 2026-06-23~07-24 갱신 | 2026-07-25 | F-1-B |
| Klaviyo Analytics Engineer | `.../klaviyo/jobs/7737707003` | 갱신 2026-07-23 | 2026-07-25 | F-1-B, F-2-B |
| Twilio 채용 보드 (183건) | `boards-api.greenhouse.io/v1/boards/twilio/jobs` | 2026-07-24~25 갱신 | 2026-07-25 | F-1-B |
| Hightouch 채용 보드 (70건) | `boards-api.greenhouse.io/v1/boards/hightouch/jobs` | 2026-06-16~07-21 갱신 | 2026-07-25 | F-1-B |
| Hightouch Solutions Engineer, Mid-Market | `.../hightouch/jobs/5535187004` | 갱신 2026-06-30 | 2026-07-25 | F-1-B, F-2-B |
| Hightouch Forward Deployed Analytics Engineer | `.../hightouch/jobs/6122160004` | 갱신 2026-07-21 | 2026-07-25 | F-1-B, F-2-B |
| AB180 엔지니어링 블로그 - Data Pipeline Team 인터뷰 | `engineering.ab180.co/stories/data-pipeline-team-interview` | **미상** | 2026-07-25 | F-2-A |
| 마티니 - 이벤트 택소노미 완벽 설계하기(1) | `blog.martinee.io/post/designing-perfect-event-taxonomy-naver-series` | **2024-05-30** | 2026-07-25 | F-2-C, F-3(2위), H3 |
| 노티플라이 - 카카오 알림톡 심사 한번에 통과하기 | `blog.notifly.tech/alimtalk-screening-guide/` | **2025-08-26** | 2026-07-25 | F-4-B |
| HN 39103276 (shkan) | `news.ycombinator.com/item?id=39103276` | 2024-01-23 | 2026-07-25 | F-3 오프닝 |
| HN 9258007 (bduerst) | `news.ycombinator.com/item?id=9258007` | 2015-03-24 | 2026-07-25 | F-3(1위), H1 |
| HN 9257502 (ssharp) | `news.ycombinator.com/item?id=9257502` | 2015-03-24 | 2026-07-25 | F-3(1위), 논쟁2 |
| HN 28855010 (fourseventy) | `news.ycombinator.com/item?id=28855010` | 2021-10-13 | 2026-07-25 | F-3(1위), 논쟁2 |
| HN 48180365 (etempleton) | `news.ycombinator.com/item?id=48180365` | **2026-05-18** | 2026-07-25 | F-3(1위), 논쟁2 |
| HN 43861360 (throwaway7783) | `news.ycombinator.com/item?id=43861360` | 2025-05-01 | 2026-07-25 | F-3(3위), 논쟁1 |
| HN 43861129 (skadamat) | `news.ycombinator.com/item?id=43861129` | 2025-05-01 | 2026-07-25 | F-3(3위) |
| HN 43866025 (r1290) | `news.ycombinator.com/item?id=43866025` | 2025-05-02 | 2026-07-25 | 논쟁1 |
| HN 45571435 (knes) | `news.ycombinator.com/item?id=45571435` | 2025-10-13 | 2026-07-25 | F-3(3위), 논쟁1 |
| HN 46449687 (dzonga) | `news.ycombinator.com/item?id=46449687` | **2026-01-01** | 2026-07-25 | F-3(3위) |
| HN 38842663 (joshmanders) | `news.ycombinator.com/item?id=38842663` | 2024-01-02 | 2026-07-25 | F-3(4위), H4, 논쟁5 |
| HN 38840135 (winkelwagen) | `news.ycombinator.com/item?id=38840135` | 2024-01-02 | 2026-07-25 | F-3(4위) |
| HN 37729412 (015a) | `news.ycombinator.com/item?id=37729412` | 2023-10-01 | 2026-07-25 | F-3(4위) |
| HN 37735717 (tsukikage) | `news.ycombinator.com/item?id=37735717` | 2023-10-02 | 2026-07-25 | 논쟁5 |
| HN 31633159 (fmajid) | `news.ycombinator.com/item?id=31633159` | 2022-06-05 | 2026-07-25 | F-3(4위) |
| HN 40096859 (PurestGuava) | `news.ycombinator.com/item?id=40096859` | 2024-04-20 | 2026-07-25 | F-3(4위) |
| HN 4210820 (dirtae) | `news.ycombinator.com/item?id=4210820` | 2012-07-07 | 2026-07-25 | F-3(4위), 논쟁5 |
| HN 9115955 (sbov) | `news.ycombinator.com/item?id=9115955` | 2015-02-26 | 2026-07-25 | F-3(5위) |
| HN 5648393 (13rules) | `news.ycombinator.com/item?id=5648393` | 2013-05-03 | 2026-07-25 | F-3(5위), H2, 논쟁3 |
| HN 8532692 (shizcakes) | `news.ycombinator.com/item?id=8532692` | 2014-10-30 | 2026-07-25 | F-3(5위), H2, 논쟁3 |
| HN 9720330 (spdustin) | `news.ycombinator.com/item?id=9720330` | 2015-06-15 | 2026-07-25 | F-3(5위) |
| HN 7621371 (davideous) | `news.ycombinator.com/item?id=7621371` | 2014-04-21 | 2026-07-25 | F-3(5위) |
| HN 9471320 (davideous) | `news.ycombinator.com/item?id=9471320` | 2015-05-01 | 2026-07-25 | 논쟁3 |
| HN 24737006 (m463) | `news.ycombinator.com/item?id=24737006` | 2020-10-10 | 2026-07-25 | F-3(6위), 논쟁4 |
| HN 27553257 (soumyadeb) | `news.ycombinator.com/item?id=27553257` | 2021-06-18 | 2026-07-25 | F-3(6위), F-5-C |
| HN 27555225 (salicideblock) | `news.ycombinator.com/item?id=27555225` | 2021-06-18 | 2026-07-25 | F-3(6위), 논쟁4 |
| HN 45106650 (jacobr1) | `news.ycombinator.com/item?id=45106650` | 2025-09-02 | 2026-07-25 | F-3(6위), 논쟁4, F-5-C |
| HN 11267213 (robbiemitchell) | `news.ycombinator.com/item?id=11267213` | 2016-03-11 | 2026-07-25 | 논쟁4 |
| HN 30887509 (kfk) | `news.ycombinator.com/item?id=30887509` | 2022-04-02 | 2026-07-25 | F-3(7위), F-5-C |
| HN 33816288 (ac2u) | `news.ycombinator.com/item?id=33816288` | 2022-12-01 | 2026-07-25 | F-3(7위), H6 |
| HN 24630925 (NicolasGorden) | `news.ycombinator.com/item?id=24630925` | 2020-09-29 | 2026-07-25 | 논쟁5 |
| HN 24742387 (XCSme) | `news.ycombinator.com/item?id=24742387` | 2020-10-10 | 2026-07-25 | 논쟁2 |
| HN 22516451 (zhangwins) | `news.ycombinator.com/item?id=22516451` | 2020-03-08 | 2026-07-25 | F-3(1위) |
| HN 7713052 (shopinterest) | `news.ycombinator.com/item?id=7713052` | 2014-05-07 | 2026-07-25 | F-3(1위) |
| HN 20299880 (dlevine) | `news.ycombinator.com/item?id=20299880` | 2019-06-27 | 2026-07-25 | 참고(아래) |
| **HN 29188544 (Hightouch Launch HN, 댓글 47개 전문)** | `hn.algolia.com/api/v1/items/29188544` | **2021-11-11** | 2026-07-25 | 논쟁1, F-3(3위 보강, 3-B위), H7 |
| ├ HN 29190721 (pinkbeanz) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | 논쟁1 관점A |
| ├ HN 29190740 (gurubavan) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | 논쟁1 관점A |
| ├ HN 29190655 (pantulis) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | 논쟁1 관점B-1 |
| ├ HN 29191935 (tomnipotent) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | 논쟁1 관점B-1 |
| ├ HN 29192626 / 29191794 (kashishg / tejasmanohar, 벤더) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | F-3(3위 보강) |
| ├ HN 29192403 (tejasmanohar, 벤더) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | F-3(3-B위) 🕒 |
| ├ HN 29192643 (joshwget) | 위 스레드 내 | 2021-11-11 | 2026-07-25 | H7 |
| └ HN 29195773 / 29196143 (soumyadeb / tejasmanohar) | 위 스레드 내 | 2021-11-12 | 2026-07-25 | 논쟁1 참고 |
| HN 43668825 (Swizec) | `news.ycombinator.com/item?id=43668825` | **2025-04-12** | 2026-07-25 | F-3(3-C위) SDK 증식 |
| HN 30684445 (tybit) | `news.ycombinator.com/item?id=30684445` | 2022-03-15 | 2026-07-25 | F-3(3-D위), H8 |
| HN 32158458 (jacksnipe) | `news.ycombinator.com/item?id=32158458` | 2022-07-19 | 2026-07-25 | F-3(3-D위), H9 |
| HN 24196643 (mixedbit) | `news.ycombinator.com/item?id=24196643` | 2020-08-18 | 2026-07-25 | F-3(3-D위) `법률해석 주의` |
| HN 18988240 / 18989137 / 18989323 (K0nserv / scrollaway / Nursie) | `news.ycombinator.com/item?id=18988240` 외 | 2019-01-24 | 2026-07-25 | F-3(3-D위) Deliveroo–Braze |
| HN 45265010 (callalex) | `news.ycombinator.com/item?id=45265010` | **2025-09-16** | 2026-07-25 | F-3(4위) 최신 푸시 사례 |
| HN 34595468 (aruntdharan, Castled) | `news.ycombinator.com/item?id=34595468` | 2023-01-31 | 2026-07-25 | 논쟁1 관점A(벤더) |
| HN 42158993 (malisper) | `news.ycombinator.com/item?id=42158993` | 2024-11-16 | 2026-07-25 | 참고: 이메일 도구 지형 |
| GitHub rudderlabs/rudder-server 이슈 목록 | `api.github.com/search/issues?q=repo:rudderlabs/rudder-server+is:issue` | 이슈별 2020~2026 | 2026-07-25 | F-3(8위) |
| GitHub snowplow/snowplow 스키마 검증 이슈 | `api.github.com/search/issues?q=repo:snowplow/snowplow+schema+validation` | 2014~2017 | 2026-07-25 | F-3(2위) |

**추가 확보 인용 (미분류, 챕터 재료용)**
- HN 20299880 / dlevine / 2019-06-27 / story: "Building Lyft's Marketing Automation Platform":
> "There are products that solve different parts of this problem, but **most companies buy 2-4 products for their marketing stack (CDP, Marketing Automation, attribution, and analytics).** For things like LTV prediction, you would either need to buy an additional piece of software or do it yourself. **Each company does marketing enough differently that there isn't a single product that could solve the problem end-to-end for everyone.**"
> 📌 "왜 Martech 스택은 항상 여러 제품의 조합인가"에 대한 실무자 설명. 연동 지옥의 구조적 원인.

---

# 참고문헌

## 채용 공고 (1차 소스, 전부 2026-07-25 조회)
1. 원티드 — 에이비일팔공(AB180) 채용 공고 24건 및 개별 상세 (ID 330977, 370636, 370582, 365460)
2. 원티드 — 빅인사이트 Data Platform Engineer (ID 359453)
3. 원티드 — 마티니아이오 솔루션 컨설턴트 (ID 349957) 외 12건
4. 원티드 — 채널코퍼레이션/채널톡 40건 및 Forward Deployed Engineer (ID 324639), 백엔드 서버 개발자 (ID 34197, 마감)
5. Greenhouse Job Board API — Braze(236) / Klaviyo(152) / Twilio(183) / Hightouch(70)

## 기업 기술 블로그 (이해관계 있음)
6. AB180 엔지니어링, "하루 100억 트래픽도 끄떡없는 시스템을 만드는 팀으로 - Data Pipeline Team 인터뷰" (게시일 미상)
7. 마티니(Martinee) 문소윤, "이벤트 택소노미 완벽 설계하기(1) (ft.네이버 시리즈)", 2024-05-30
8. 노티플라이(Notifly), "카카오 알림톡 심사 한번에 통과하기", 2025-08-26

## 커뮤니티 (Hacker News, 전부 원문 인용)
9. HN 댓글 34건 — 상세는 위 신선도 원장 참조. 수집 경로: `hn.algolia.com/api/v1/search?tags=comment` (쿼리: `reverse ETL`, `Segment analytics tracking`, `marketing attribution`, `email deliverability`, `push notification marketing`, `CDP customer data`)
10. HN 39103276, shkan, "The Agonizing Reality of Developing Communication Services for Marketing Teams", 2024-01-23

## 코드 저장소
11. GitHub — `rudderlabs/rudder-server` 이슈 목록 (제목·상태·날짜만)
12. GitHub — `snowplow/snowplow` 스키마 검증 이슈 9건 (제목·날짜만)
