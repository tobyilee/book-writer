# Insider One과 Braze로 하는 기업 마케팅 레퍼런스

- 합성일: 2026-11-03 (리서치 검색 시점 동일: 2026-11-03)
- genre: tech-book / slug: insider-braze-marketing / 대상: 기업 마케팅에 입문한 한국 주니어 마케터
- 원천: `research/web.md`(웹, 자료 1~35) · `research/papers.md`(논문, A1~K4) · `research/community.md`(커뮤니티, 패턴 1~8·휴리스틱 1~6·사례 1~4·논쟁 A~D). 원천 파일은 fact-checker의 1차 대조 근거로 보존한다.

## 0. 읽는 법과 표기 규칙

**출처 태그.** 모든 주장 끝에 `[유형 · 원천ID · 등급]`을 붙였다.
- 유형: **웹**(벤더 공식 문서·보도자료·매체) / **논문** / **커뮤니티**(리뷰·실무 블로그·포럼)
- 원천ID: `W{n}` = web.md 자료 번호, `P-{id}` = papers.md 논문 ID, `C-패턴{n}`·`C-휴{n}`·`C-사례{n}`·`C-논쟁{x}` = community.md 항목
- 등급(원천 표기 그대로): 웹은 **최상 / 최상~중 / 중**. 논문은 **[abstract 확인] / [2차 출처 확인] / 미확인**. 커뮤니티는 전부 **커뮤니티 의견, 검증 필요**이며, 검색 스니펫으로만 본 것은 **[스니펫]**.

**본문 고정 기준.** 두 벤더 모두 2025~2026년에 회사명·AI 기능명·문서 URL을 여러 번 바꿨다(Insider → Insider One, Sirius AI → Agent One, Sage AI → BrazeAI, `/sage_ai/` → `/brazeai/`). 본문 기능 서술은 **"2026-11 기준"**으로 못 박는다 [웹 · W7(원 리서치 주의문) · 최상].

**벤더 수치.** 벤더 고객 사례 수치는 모두 벤더 자체 발표(self-reported)다. 독립 검증된 수치가 아니다. 기준값·표본·유의성이 공개되지 않았으므로 본문에서는 "회사 측 발표에 따르면" / "벤더 발표"로 표기한다 [웹 · W 서두 / 커뮤니티 · C-사례 서두].

### 0.1 단정 금지 목록 (저술가·fact-checker 필독)

원천에서 경고가 붙은 항목을 한곳에 모았다. 각 항목의 원문 경고를 그대로 옮긴다.

| # | 항목 | 원문 경고 / 허용 표현 | 원천 |
|---|---|---|---|
| X1 | Braze의 카카오 **알림톡** 지원 | "알림톡(정보성)·브랜드 메시지 지원 여부는 이 글과 문서 어디에도 명시 없음. 본문에서 'Braze가 알림톡을 지원한다'고 단정하지 말 것." 확인된 것은 **친구톡**뿐. KakaoTalk "Create message" 문서 URL은 404. | W19, W 수집 한계 |
| X2 | Insider One의 **카카오톡** 지원 | "Insider One은 공식 페이지·Academy에서 카카오톡 지원을 확인하지 못함 — Architect의 'Call an API'(웹훅) 요소로 외부 메시징 사업자 연동 가능성은 있으나 1차 근거 없음." 한국어 플랫폼 페이지에도 "카카오톡·알림톡 언급 없음". → 단정 금지, 운영자/벤더 확인 필요. | W2, W·D절, W 수집 한계 |
| X3 | 벤더 고객 사례 수치 전부 | 자체 보고. "벤더 발표" 명시. Samsung 사례는 "페이지 내 표현 불일치 … 본문 인용 시 헤드라인 문장만 쓰고 '벤더 발표' 명시 권장." | W15, C-사례 서두 |
| X4 | Reichheld & Sasser "이탈 5% 감소 → 이익 25~85% 증가" | "실증 연구가 아니라 사례 기반 추정 … Byron Sharp 등이 '사고 실험에 가깝고 리텐션 비용을 0으로 가정'했다고 비판 [2차 출처 확인]. 책에서 쓰려면 '업계에 널리 퍼진 주장이지만 근거는 약하다'는 반례 소재로 쓰는 편이 안전하다." **원천 수치는 "25~85%"다.** 업계에서 흔히 도는 "25~95%" 표기는 이번 리서치 원천에 없다 — 쓰려면 별도 출처 확인. "신규 획득 비용은 유지 비용의 5배"도 학술 출처 미확인. | P-(주의 문헌) |
| X5 | Lemmens & Gupta 2020 이익 증가 폭 | 보도 매체마다 수치 상이(최소 4% / 2,800만 달러 / 2배 이상) "→ 책에서는 구체 수치 인용을 피하고 '이익 기준 타기팅이 더 낫다'는 방향만 쓸 것." | P-C3 |
| X6 | Kumar & Venkatesan 2005 멀티채널 고객 매출 배수 | "구체 수치 … 확인하지 못함 → 수치 인용 금지." | P-J3 |
| X7 | 넷플릭스 추천 "연간 10억 달러 이상 절감" | "회사 내부 추정이며 외부 검증 불가 — '넷플릭스가 스스로 추정한 값'으로 표기." | P-H2 |
| X8 | Rust·Lemon·Zeithaml 2004 수치 | "abstract 수치는 확인하지 못함 → 수치 인용 금지, 개념만 사용." | P-A2 |
| X9 | Kumar·Zhang·Luo 2014 | "수치 인용은 피할 것." | P-G3 |
| X10 | Braze 가격 인하 알림 "분당 10개 아이템 업데이트" 제한 | "구버전 정보, 쓰지 말 것." | W29 |
| X11 | Insider 레거시 개인화 태그 문법(`{{ attribute \| default }}` 류) | "문서 표현이 불일치 — 본문에서 확정 문법으로 쓰지 말 것." | W10 |
| X12 | Insider UCD 속성 상한 200 / 기본 120 | "검색 스니펫 기준, 버전별 문서 차이 있음. fact-checker는 현행 Data Points 문서로 재확인 필요." | W9 |
| X13 | 업리프트 고객 4분류(Persuadables·Sure things·Lost causes·Sleeping dogs) | "이 논문에 그대로 나오는지는 미확인이므로 '업계에서 흔히 쓰는 분류' 정도로 표기." | P-D1 |
| X14 | Verhoef·Kannan·Inman 2015 옴니채널 정의 문장 | "정의 문장은 본문 미확인 → 직접 인용 금지, 의역만." | P-J1 |
| X15 | Lemon & Verhoef 2016 접점 4분류명 | "본문에 분류명을 그대로 쓸 경우 fact-check 대상으로 둘 것." | P-A1 |
| X16 | 인프런 강의 소개의 Braze 사용 기업(야놀자·크몽·우아한형제들·리디·하이퍼커넥트·사람인) | "강의 홍보문, 1차 확인 아님. 본문에 고객명으로 쓰려면 각 사 공개 자료 확인 필요." | W34, C-패턴2 |
| X17 | 정보통신망법 세부(야간 발송 시간대·수신 동의 갱신 주기 등) | 원천에 1차 법령·KISA 자료 없음. "법규는 web 리서치 및 KISA 1차 소스와 대조해야 한다." 논문 리서치도 "국내 개인정보보호법 관련 학술 논문은 … 다루지 못했다." → 구체 시각·주기·과태료 수치는 이 레퍼런스에 근거가 없다. | C-패턴5, P 수집 한계 |
| X18 | Mehrotra 2016 규모(20명·1만 건·474건) | "추출 품질 낮음 → 미확인 취급 권장." | P-F5 |
| X19 | Neslin 2006 "로짓이 판별분석·트리보다 좋았다" | "원문 확인 전 단정 금지." | P-C1 |
| X20 | Sirius AI "마케팅 팀 60% 생산성 향상" | 자사 주장, 발행일 미확인(2023년경), "구버전 정보일 수 있음." | W4 |
| X21 | 학술적으로 검증된 STO 효과 | "무작위 실험으로 검증된 STO 논문은 찾지 못했다 — 벤더 주장 수치는 … '벤더 발표 수치'로 표기할 것." | P-F1 |
| X22 | G2 평점 Insider One 4.8(약 1,413건) / Braze 4.5(약 1,685건) | 검색 시점 스니펫, fact-checker 확인 필요. Insider 한국어 페이지의 "G2 4.8/5.0"은 벤더 표기. | C-논쟁B, W2 |
| X23 | Insider 고객 수 | 1,500+(2024-11) vs 2,000+(2025-12 이후) 시점 차이. "본문에서는 '2,000+ (2025-12 자사 발표)'를 쓰는 것이 안전." | W2 |
| X24 | Canvas 진입 방식(scheduled / action-based / API-triggered) | Canvas 페이지에 상세 없음 — "일반 지식, fact-checker 재확인 필요." | W22 |
| X25 | Braze Liquid 기본값 문법 `{{${first_name} \| default: '고객'}}` | "이번에 원문 미확인." | W23 |

---

## 1. 개념과 정의

### 1.1 두 제품의 정체와 포지셔닝 (2026-11 기준)

**Insider One (구 Insider)**
- 2025-12-09(뉴욕 데이트라인, 뉴스룸 목록상 2025-12-08) 사명을 Insider에서 Insider One으로 변경 [웹 · W1 · 최상(1차, 자사 홍보)]. 주제의 "2025년 리브랜딩"은 **확인됨: 2025-12-09 발표**. 도메인은 insiderone.com(구 useinsider.com은 리다이렉트/병행 — 페이지에 도메인 변경 명시 없음).
  > "AI no longer belongs inside MarTech. It now sits above it." — Hande Cilingir, Co-Founder and CEO
  > "In our first decade, we led all the seismic moves in the industry from mobile to AI." — Hande Cilingir
- 회사 수치(2025-12 기준): 고객 2,000+ / 30+ 시장 / 15개 산업 / 임직원 1,500+ / 50+ 국적 / 6개 대륙 30+ 오피스 [웹 · W1 · 최상]. (CEO 정식 표기는 Hande Cilingir — 한국어 기사 원문은 "Hande Schlinger"로 오기 [W3])
- 제품 구성(보도자료): Agent One™ (Agent One™ Teams, Agent One™ Audiences), Customer Data Management, Personalization, Journey Orchestration, Reporting & Data, Behavioral Analytics [웹 · W1 · 최상].
- 한국어 플랫폼 페이지 모듈명: "고객 데이터 관리", "Insider One AI", "개인화", "여정 오케스트레이션", "리포팅 & 데이터", "행동 분석". 100개 이상 데이터 소스 연동 [웹 · W2 · 최상]. 문구: "더 빠른 실행과 성과를 위한 AI".
- 벤더 표기 규모 수치: 1,500개 이상 브랜드(시점 차이 — X23), G2 4.8/5.0, 사용자 프로필 10억+, 월 푸시 400억 건, 월 이메일 16억 건 [웹 · W2 · 최상(벤더 표기)].
- 포지셔닝: "에이전틱 고객 참여 플랫폼". 2026 Gartner MQ for **Personalization Engines** Leader(자사 발표상 5회째), MMH MQ는 2025-06 자사 자료 기준 "Visionary", 2026 Gartner Peer Insights Customers' Choice(MMH) 2회 연속 [웹 · W17 · 중(벤더 인용, Gartner 원문 미열람)]. 2026 MMH MQ에서 Insider One의 위치는 확인 못함.
- 차별점: 온사이트 개인화·추천(Smart Recommender, Web Suite, Category Optimizer, InStory, 사이트 검색 Eureka) [웹 · W·D절 · 원 리서처 정리].
- 회사 동향: Bluecore(미국 리테일 마테크, 엔터프라이즈 브랜드 400+, ALO Yoga·Sephora·The North Face) 인수 2026-05-13 발표(일부 2차 매체는 2026-06-03 — 1차 발표일 05-13 채택), 금액 비공개, Transparent ID Network 편입. OpenAI 파트너십 2026-03(제3자 타임라인 기준, 1차 날짜 미확인) [웹 · W5 · 중].

**Braze**
- 포지셔닝: "고객 참여 플랫폼(Customer Engagement Platform)". Gartner MQ for Multichannel Marketing Hubs 리더 — 2025(3년 연속, 11개 벤더 평가), 2026(4년 연속). 2026 배치에 대해 Braze 측 표현: "highest for Ability to Execute and furthest for Completeness of Vision". 2026 Critical Capabilities에서 Multichannel Engagement·Omnichannel Workflow Innovation 1위 [웹 · W33 · 최상~중].
- 규모: 글로벌 MAU 78억 이상 / 연간 처리 메시지 3조 9천억 건 이상(2026-04 기준) [웹 · W18 · 최상]. 약 70개국 2,000개+ 기업 사용(2024-11 기준) [웹 · W34 · 중]. 2025-11-25~12-01 메시지 1,000억+ 건, BFCM 최대 599억 건(전년 대비 19%↑) [웹 · W32 · 최상(자사)].
- 비교 축 요약: Insider=개인화 엔진 강점, Braze=MMH 강점 [웹 · W17·W33 · 원 리서처 정리].

### 1.2 한국 시장 조직·생태계

- **Braze 코리아**: GM 고주연(2024-11). 공식 리셀링 파트너 AB180(에이비일팔공) — 2017년부터 라이선스·컨설팅 [웹 · W34 · 중]. 2026-04-08 AWS 기반 국내 데이터센터 오픈 + 카카오톡 채널 출시 [웹 · W18 · 최상]. 리셀러 마티니 아이오 "3년만에 300억 매출"(바이라인네트워크, 2025-12-04) [커뮤니티 · C-사례4 · 검증 필요]. 브레이즈 커넥션 서울 2024 연사: Braze, CJ올리브네트웍스, 잡플래닛, 마티니; 네이버웹툰 이종한 리드 CRM 효율화 사례(수치 없음) [웹 · W34 · 중].
- **인사이더 코리아**: 컨트리 헤드 이진우(2024-11). 2024-11-01 시리즈E $500M(General Atlantic 주도) 유치와 함께 2027년까지 한국에 1,500억 원 투자·일자리 60개 창출 계획. 한국 고객으로 삼성전자·대한항공·롯데호텔·GS샵, 부제에 현대캐피탈. 고객 1,500+, 포춘 500의 약 1/3(2024-11 기준). 기업가치 미공개 [웹 · W3 · 최상].
  > "인사이더는 시작부터 가장 빠르고 쉬운 온보딩 경험을 제공합니다" — 이진우
  > "지난 1년 동안 150개 브랜드가 자동 마이그레이터와 사전 구축된 인터그레이션을 활용하여 기존 클라우드에서 인사이더로 성공적으로 전환했습니다." — Serhat Soyuerel, 공동창업자·CRO
- 채용 시장 신호: "Braze를 활용해 앱 푸시, 인앱 팝업, 카카오 메시지 등 다양한 채널의 CRM 캠페인을 기획하고 운영해요" 같은 문구 반복 [커뮤니티 · C-패턴2 · 검증 필요].

### 1.3 용어 표기 후보 (계획의 '용어 표기' 재료)

| 개념 | Braze | Insider One | 비고 |
|---|---|---|---|
| 여정 빌더 | Canvas (기본 편집기 = Canvas Flow, 2022 출시) | Architect | **Insider도 여정 설계 화면을 "Canvas"라 부름 → Braze Canvas와 혼동 주의** [W8] |
| 여정 노드 | 컴포넌트(component)/단계(step) | Element | [W22, W8] |
| 진입 지점 | 진입(entry)·트리거 | Trigger = Starter | [W8] |
| 사용자 DB | 사용자 프로필(user profile) | UCD(Unified Customer Database) | [W21, W9] |
| 사용자 식별자 | external_id, braze_id(익명), alias(label+name) | identifiers 객체(이메일·전화·user ID) | [W21, W9] |
| 템플릿 언어 | Liquid (GA) | Liquid(얼리 액세스) / Dynamic Content(레거시) | [W23, W10] |
| AI 브랜드 | BrazeAI™ (구 Sage AI) | Agent One™ (구 Sirius AI), "Insider One AI" | [W24, W4] |
| 발송 시간 최적화 | Intelligent Timing | Send Time Optimization | [W25, W12] |
| 최적 채널 | Intelligent Channel filter (구 Most Engaged) | Next Best Channel | [W25, W13] |
| 자동 승자 | Optimize with BrazeAI (구 Intelligent Selection), Winning Path | A/B autowinner | [W24, W7] |
| 추천 | AI item recommendations | Smart Recommender | [W24, W11] |

### 1.4 학술 개념 (이론 배경 박스용)

- **고객 여정**: CX를 구매 전(prepurchase)·구매(purchase)·구매 후(postpurchase) 단계에 걸친 여러 접점의 총합으로 개념화. 접점을 브랜드 소유·파트너 소유·고객 소유·사회적/외부 접점으로 나눔(분류명은 X15) [논문 · P-A1 · Lemon & Verhoef 2016, 원문 미확인·널리 알려진 구조 기반 요약]. 쓰임: Canvas/Architect를 "여정 3단계 위에 접점을 배치하는 도구"로 소개, "회사가 통제할 수 있는 접점은 전체 경험의 일부일 뿐".
- **고객 자산(customer equity)** = 모든 고객의 CLV 합. 리텐션·획득·브랜드 투자를 같은 저울에 올림 [논문 · P-A2 · 개념만, X8].
- **RFM과 CLV**: RFM 세 값만으로 확률 모델(Pareto/NBD + 감마-감마)을 통해 고객별 CLV 계산. "등가치 곡선(iso-value curve)" — CDNOW 데이터 적용 [논문 · P-B1 · 2차 출처 확인]. BG/NBD는 Pareto/NBD와 비슷한 예측력을 쉬운 계산으로 [논문 · P-B2]. 계보 원논문 Schmittlein et al. 1987 [논문 · P-B3]. CLV 모델 지도 서베이 [논문 · P-B4 · 2차 출처 확인]. 주니어용 단순화: "CLV = (고객이 남아 있을 확률 × 한 번에 쓰는 돈 × 얼마나 자주)의 미래 합을 지금 가치로 할인한 것" [P-B4 독자 전달 제안].
- **멀티채널 vs 옴니채널**: 채널을 따로 관리 vs 채널·접점을 통합 관리해 고객 경험·성과 최적화(의역만, X14) [논문 · P-J1]. "이메일팀, 앱푸시팀, 카카오톡 담당이 따로 노는 것 = 멀티채널, 한 고객 프로필 위에서 조율 = 옴니채널" [P-J1 독자 전달 제안]. 멀티채널 고객 관리 정의·5대 과제 [논문 · P-J2 · 2차 출처 확인].
- **업리프트 모델링**: 처치가 고객 결과에 주는 증분 효과 모델링. 세 갈래 — Two-Model, Class Transformation, 직접 모델링 [논문 · P-D1 · PMLR abstract 확인].
  > "Uplift modeling can be particularly useful for personalized promotional campaigns, where the potential benefit caused by a promotion needs to be weighed against the potential costs." (CIKM 2023 튜토리얼, arXiv 2308.09066, Abstract — 저자명 미확인) [논문 · P-D3 · abstract 확인]
- **SRM(표본비 불일치)**: 실험군·대조군 배정 비율이 기대와 다른 상황 [논문 · P-E3 · abstract 확인].
  > "Just like fever is a symptom for multiple types of illness, an SRM is a symptom for a variety of data quality issues." (Abstract)

---

## 2. 기능 영역별 핵심 (Braze ↔ Insider One)

### 2.1 데이터 모델 — 프로필·식별자·이벤트·속성

**Braze** [웹 · W21 · 최상, 날짜 미표기 — 2026-11 조회]
- 프로필에 사용자 영속 데이터 저장. external_id 없는 사용자 = 익명 사용자(기기별 braze_id). external_id로 여러 기기에서 같은 프로필 식별. alias(label+name 쌍)로 다른 식별자 참조.
- 익명 프로필이 기존 사용자로 식별되면 익명 프로필은 orphan 처리되고 일부 누락 필드만 복사.
- 커스텀 이벤트는 캠페인·Canvas 트리거·세그먼트에 사용, 이벤트 속성(properties)은 트리거 조건·개인화·전환·분석에 사용. 시계열 분석이 필요 없으면 커스텀 속성(카운터)으로.
- 커스텀 이벤트·속성 개수에 고정 대시보드 상한은 없음(데이터 형태·수집량·워크스페이스 성능에 좌우).
  > "All persistent data associated with a user is stored in their user profile."
  > "Any user without a designated `external_id` is called an anonymous user."
  > "An `external_id` allows you to identify the same user profile across multiple devices."
  > "Not all data is merged from the anonymous profile."
  > 커스텀 이벤트는 "actions taken by, or updates about, your users."

**Insider One** [웹 · W9 · 최상, 2026-08-28]
- UCD는 모든 Insider One 제품을 떠받치는 핵심 CDP. 이메일·전화번호·user ID 같은 식별자로 레코드 통합. 웹·앱에서 같은 식별자로 로그인하면 "Last Visited Product" 같은 속성이 통합됨.
- 이벤트 = 타임스탬프가 붙은 행동 기록, 속성 = 프로필 정보. 기본(default) vs 커스텀(custom). 커스텀은 월 데이터 포인트 소비에 영향.
  > "The Unified Customer Database (UCD) is the core Customer Data Platform (CDP) that powers all Insider One products."
  > "Only fields placed in the identifiers object are ever evaluated for identity resolution." (검색 스니펫 기준 — 본문 확인 권장)
  > "Custom events and custom attributes affect your monthly data point consumption." (검색 스니펫 기준)
- 속성 총 200개/기본 120개 — X12(재확인 필요).

**비용과 데이터 설계** [커뮤니티 · C-패턴7 · 검증 필요]
- Braze: "The billing is tricky to understand because I have to work out how many message credits I need" (AWS Marketplace, matias d., 2026-10-31). "Braze is very expensive. Period." 비용은 데이터 포인트 추가, SMS(Twilio), 콘텐츠 카드 같은 애드온으로 증가 (The Grow Getter, 2023-11-10). "The cost for data usage limits us from importing all of our data." (Fivetran 블로그 인용, 이해관계 있음) [스니펫].
- Insider: "The price is not very cheap for Insider, especially when compared to other platforms" (PeerSpot, 2026-10-08).
- 함의: "모든 데이터를 다 넣자"가 공짜가 아니다 — 어떤 속성·이벤트를 보낼지가 비용 결정. 가격 정책 세부는 Braze 공식 data points 문서(https://braze.com/docs/ko/user_guide/data/infrastructure/data_points/)와 대조 필요.

**데이터 의존성(현장)** [커뮤니티 · C-패턴3 · 검증 필요]
- 세그먼트·트리거·개인화의 재료는 모두 SDK가 심은 이벤트와 속성이고, 그것을 정하고 심는 일은 개발 조직 백로그에 들어간다. "마케터의 자율성은 도입 초기 데이터 설계 품질에 비례한다"는 커뮤니티 진단.
  > "이벤트 택소노미가 잘 구축되어 있으면 필요한 데이터가 빠짐없이 일관되게 쌓이기 때문에 여러 팀이 공통된 지표를 신뢰하며 소통할 수 있습니다." — 아이보스
  > "마케터의 고충 역시 데이터로부터 비롯되는 경우가 많다. 최근엔 데이터 리터러시로 인한 '데이터 갈증'을 호소하는 마케터가 늘고 있다." / "메시지 발송을 위해 두 명의 마케터 혹은 개발자와 데이터 분석가 각각 한 명이 필요하다." — 디지털인사이트 기고(마티니 아이오, Braze 리셀러 — 이해관계 있음)

### 2.2 세그먼트·예측 세그먼트

**Insider One — Predictive Segments** [웹 · W13 · 최상, 2026-08-27]
- 유형: "Likelihood to Purchase", "User Engagement", "Customer Lifecycle Status", "Discount Affinity", "Attribute Affinity"(계정별 사용 가능 범위 상이). 이탈(churn) 전용 유형명은 페이지에 없음, "churn risk"는 예시로만 등장.
- Likelihood to Purchase = 향후 7일 내 구매 가능성 높은 사용자 식별(스니펫).
- SMS Likelihood to Engage는 7일간 SMS 클릭 100건·발송 1,000건 이상 필요(스니펫 기준, 재확인 필요).

**Braze — Predictive Suite** [웹 · W26 · 최상, 날짜 미표기 — 2026-11 조회]
- Predictive Churn: 이탈의 정의를 회사가 직접 정함. 활성 예측 최대 3개(프리뷰 모드 1개). 사용자에게 0~100 이탈 위험 점수(높을수록 이탈 가능성↑). 업데이트 주기 선택. 최소 데이터 요건 미확인.
- Predictive Events: 특정 행동(예: 구매) 가능성 점수.
- Predictive Suite는 측정 결과로 학습하고 자체 정확도를 보고(Braze Agents는 결과로 학습하지 않음).
  > Predictive Suite "puts machine learning tools directly in your hands"

**세그먼트 운영 휴리스틱** [커뮤니티 · C-휴1 · 검증 필요]
- 처음부터 잘게 쪼개지 말고 발송 가능한 모수부터 확인.
  > "실제 발송 가능한 모수를 파악하는 게 가장 중요해요." — 고구마팜(갱언니, 2022-04-25)
  > "처음부터 너무 세분화하기보다 적정한 모수를 먼저 확보하는 것이 중요하다" — 아이보스 계열 실무 글 [스니펫]
- 크몽 CRM 마케터 강의: RFM·코호트로 고객을 먼저 분류한 뒤 Braze 세그먼트 설정(데이터 설계가 먼저) — https://comento.kr/class/pt/content/braze를-활용한-crm-마케팅-개인화/76
- Insider 리뷰 불만: "we still can't combine audience filters with dynamic segments." (리테일, 2026-10-30) / "Initial segment rules also needed manual adjustments to filter out already purchased items." (Victor Adolfo G.) [커뮤니티 · C-패턴8].

**학술 근거 — "누구에게 보낼 것인가"**
- 이탈 모델 토너먼트: 정확도 차이만으로 이탈 방지 캠페인 수익이 **수십만 달러** 달라질 수 있다 [논문 · P-C1 · Neslin et al. 2006 · 2차 출처 확인]. "Braze/Insider One의 예측 이탈 점수도 결국 모델이다. 모델 품질이 곧 돈이다."
- **Retention Futility**: 이탈 위험이 가장 높은 고객이 최선 타깃이 아닐 수 있다 — 위험도가 아니라 캠페인 민감도(업리프트)로 타기팅. 두 필드 실험. 민감도 기준 타기팅이 이탈률을 **4.1~8.7%p** 줄였다(위험도 기준 대비) [논문 · P-C2 · Ascarza 2018 · 2차 출처 확인: AMA·MSI 소개문]. 2023 AMA Weitz-Winer-O'Dell 상 [2차 출처 확인]. 결정적 장면 후보: "이탈 예측 점수 상위 10%에게 쿠폰을 보냈는데 효과가 없었다 — 왜?"
- 이익 기준 타기팅이 위험도·반응도 기준보다 낫다(방향만, X5). 저자 인정: 이 방법이 누가 이탈할지 예측하는 데는 오히려 오차가 더 크다 [논문 · P-C3 · Lemmens & Gupta 2020 · 2차 출처 확인]. 서사: "위험도 → 반응도 → 이익" 3단 진화.
- RFM 세그먼트의 이론 배경 = P-B1 (1.4 참조). "최근성이 낮은 VIP는 이미 떠났을 수 있다."

### 2.3 채널

**Insider One 채널** [웹 · W1·W2·W7 · 최상]
- 보도자료(2025-12): Web, Email, Site Search, Conversational CX, WhatsApp, Web Push, InStory, App, SMS & RCS.
- 한국어 페이지: 웹, 앱, 이메일, 웹 푸시, SMS 및 RCS, WhatsApp, 인스토리, 대화형 CX, 사이트 검색. 광고 연동: TikTok·Facebook·Instagram. **카카오톡·알림톡 언급 없음**(X2).
- Architect 채널(2026-02-12 문서): Web push, App push, Email, SMS, WhatsApp, Onsite, In-app, Facebook Custom Audiences, Call an API, Google Ads.
- WhatsApp Commerce: MindBehind 인수(2023-01-10) 후 Meta BSP가 되어 출시(2023-03-21) — 상품 카드·카테고리 리스트·카탈로그·대화 흐름·결제 연동 [웹 · W16 · 중, 구버전 정보일 수 있음(2023)]. 한국 독자에게는 해외 시장 채널로 소개.

**Braze 채널** [웹 · W28 · 최상, 2026-11 조회 / 릴리스노트 2025-05-27]
- 인프로덕트: 인앱 메시지(fullscreen·modal·slideup·서베이), Content Cards, Banners.
- 아웃오브프로덕트: Email, Transactional email, Landing pages, LINE, Live notifications, Push(Android·iOS·Web), SMS/MMS/RCS, Webhooks, WhatsApp. KakaoTalk은 사이드바에 별도 섹션.
- 시작 가이드(스페인어판)는 RCS·WhatsApp·Banners·Content Cards를 애드온 표시. 2025-05 릴리스: RCS Android·iOS GA, Banners GA.
- 2025년 추가: RCS·배너·WhatsApp Commerce·WhatsApp Flows·WhatsApp 광고 Audience Sync [웹 · W32 · 최상(자사)].

**푸시 알림의 현실(학술)**
- 하루 평균 **63.5개** 알림, 대부분 메신저와 이메일 — 표본 15명, 1주일 [논문 · P-F3 · Pielot et al. 2014 · 2차 출처 확인]. "당신의 마케팅 푸시는 하루 60여 개 알림 중 하나다."
- 4만 명 이상·약 2억 건 알림 대규모 분석 [논문 · P-F4 · Sahami Shirazi et al. 2014 · 2차 출처 확인, 세부 결과 미확인].
- 중요하거나 유용한 내용의 알림도 방해가 될 수 있다 [논문 · P-F5 · Mehrotra et al. 2016 · 2차 출처 확인, 규모는 X18].
- 푸시의 인과 효과(MRT, 1,255명·89일, 하루 6개 시각 중 하나에서 매번 50:50 무작위화) [논문 · P-F2 · Bidargaddi et al. 2018 · **abstract 확인**]:
  - 24시간 내 앱 참여 확률 **3.9% 증가**(위험비 1.039, 95% CI 1.01–1.08)
  - 주말 **8.7%** vs 주중 **2.5%**(차이 유의하지 않음, P=.18)
  - 효과 최대: 주말 낮 12:30, **11.8%** 증가(90% CI)
  - 시간 경과에 따른 효과 약화 경향, 유의하지 않음(P=.84)
  > "Users were estimated to be 3.9% more likely to engage with the app in the next 24 hours when a tailored health message was sent versus when it was not sent" (Abstract, Results)
  - 주의: 헬스 앱 — 이커머스 앱 푸시의 대규모 무작위 실험 논문은 찾지 못함.

**피로도·빈도** [커뮤니티 · C-패턴5 · 검증 필요]
  > "발송 빈도가 너무 잦으면 안 돼요." — 고구마팜(2022-04-25). 자주 보내면 할인 직후 구매 고객이 불쾌해하고 할인만 기다리는 고객이 생긴다. 치명적 실수: "행동 기반의 유저 활동을 분석하지 않거나 브랜딩 메시지 없이 무작정 CRM 채널을 확장하고" 앱 푸시 고도화에만 매달리는 것.
  > "CRM 마케팅의 업무를 단순히 push 메세지 보내는 것으로 생각한다." / "Push 발송은 Action item 중의 하나이다." — 이오플래닛(헨리퀀, 2022-06-16)
  > "발송된 CRM 메시지는 되돌릴 수 없으므로 철저한 여정 설계와 테스트가 필요하다" — 아이보스·고구마팜 등 [스니펫]
- Airship(벤더, 2026-08) [스니펫]: 과다 발송 유저는 서서히 무시하지 않고 푸시 수신 거부·OS 알림 권한 해제·앱 삭제처럼 단호하게 행동.
- Braze 블로그(벤더) [스니펫]: 주간 전체 상한과 채널별 상한(예: 하루 푸시 상한)을 겹쳐 쓰라. 상한 override가 잦으면 상한이 너무 낮게 잡힌 신호.
- Insider Architect도 빈도 제한(frequency capping)을 공통 기능으로 제공 [웹 · W7 · 최상].
- 학술: 마케팅 강도(발송 빈도 등)가 옵트인·옵트아웃 시점에 영향, 옵트아웃 시점을 늦춰 이익을 높일 수 있음 — 빈도 캡의 학술 근거 [논문 · P-G3 · Kumar, Zhang & Luo 2014 · 2차 출처 확인(동일 저자군 학위논문 abstract), 수치 금지].
- 원인 진단: 캠페인 단위 CTR만 보면 더 보낼수록 이득처럼 보이고, 피로도 비용(수신 거부·앱 삭제)은 캠페인 리포트에 잡히지 않는다. 여러 팀이 각자 보내면 전역 빈도 상한 부재가 드러난다 [커뮤니티 · C-패턴5].

### 2.4 여정 빌더 — Insider Architect vs Braze Canvas

**Insider Architect** [웹 · W6·W7·W8 · 최상]
- 정의(2026-08-27): AI 기반 옴니채널 여정 빌더, 통합 고객 DB 기반.
  > "orchestrate high-performing customer journeys across every connected platform."
  > "AI-backed marketing automation tool" (Feature Set, 2026-02-12)
- 구성요소(문서 목차): Starter Elements, Wait Elements, Check Elements, Channel Elements, Action Elements, Journey A/B Split, Next Best Channel, Dynamic Content, Components, Journey Analytics.
- 흐름: starter에서 시작해 행동·속성 기반 if/else 분기. 공통 기능 — 속성 기반 개인화, 크로스 플랫폼, 빈도 제한, 최적 채널 선택, 발송 시간 최적화.
- 흐름 제어: 실시간·날짜 기반 starter, 반응/기간 내 이벤트/행동·속성 분기, 채널 도달 가능성(reachability) 체크, 사전 구축 유스케이스·예측 세그먼트, A/B split·A/B autowinner, 기간/시간대 wait, 흐름 중 속성 업데이트, 진입 제한·자격 규칙·종료 조건(exit criteria).
- 리포트: 실시간 흐름 통계, 채널별·여정 전체 통계, 성과 대시보드, A/B 통계, 데이터 export, 전환 목표, last-touch 어트리뷰션.
- 테스트: 테스트 발송, 랜덤 테스트, 샘플 프로필로 동적 콘텐츠 미리보기, 사용자 추적, Dry Run.
- 용어(Terms to Know, 2025-11-14) — 용어집 장 재료:
  - Trigger(=Starter): 여정의 첫 단계, 조건에 맞는 사용자 진입
  - Element: 흐름 위의 노드(채널, 체크포인트, starter 등)
  - Condition(criteria): 진입시키거나 여정 안에서 걸러내는 속성·이벤트·세그먼트
  - Path: 체크 조건·도달성 체크·A/B split 이후 갈라지는 가지
  - Live Actions: 보낸 메시지에 사용자가 특정 행동을 할 때까지 붙잡아 두는 대기 지점
  - Layer: 여정 안에서 사용자 상호작용 횟수, 두 번째 메시지 효과 확인
  - Conversion Goal / Conversion Attribution Model(예: 마지막 클릭 채널에 전량 귀속)
  - Dry Run: 실제 발송 없이 진입 인원·흐름 시뮬레이션
  - Sunset: 신규 진입은 막고 기존 사용자는 계속 진행
  - Promotional vs Transactional Use Case: 프로모션은 opt-in 필요, 트랜잭션(주문 확인·비밀번호 재설정)은 opt-in 불요
- 가격 인하 스타터 **On Price Drop**(2026-09-03): 상품 가격이 내려가면(Product Feed에서 추적) 자동 진입. 기본 이벤트 Product Page View, 대신 위시리스트 담기·장바구니 담기·커스텀 "가격 알림 구독" 이벤트 지정 가능. 하락률 설정(예시 20%), 원가·하락률로 상품 제외 필터. 가격 인상은 트리거 불가. 카탈로그 소스 Clickstream, XML, Catalog API — 상품 미방문자에게 도달하려면 XML/Catalog API만 가능. Back in Stock 스타터 별도 존재 [웹 · W14 · 최상].
  > "triggers the journey immediately when the price drops."
  > "Events without a Product ID parameter cannot be used with price drop condition."

**Braze Canvas** [웹 · W22 · 최상, 날짜 미표기 — 2026-11 조회]
- 정의: 여러 메시지를 묶어 여정을 만드는 시각적 여정 빌더.
  > "Canvas is a unified interface where marketers craft campaigns with multiple messages"
- 컴포넌트(2026-11 목록): Action Paths, Agent, Audience Paths, Canvas Audience Sync, Experiment Paths(Winning Path 포함), Content Optimizer, Context, Decision Split, Delay, Feature Flag, Message, Send to Destination, User Update.
- 그 외 문서: Exit criteria, Canvas 템플릿, 버전 히스토리, 복제, 알림, 테스트, 사용자 경로 미리보기, 리텐션·퍼널 리포트, QA 체크리스트.
- 진입 방식 상세는 X24. "Canvas Flow"(2022 출시)는 현재 Canvas의 기본 편집기.
- 카탈로그 가격 인하 알림 [웹 · W29 · 최상]: 아이템 ID와 `type` 배열(`price_drop`)을 담은 커스텀 이벤트로 구독. 규칙은 퍼센트 변화 또는 절대값 변화(스크린샷 예 3%, 본문 예 50%). opt-in 사용자만 수신, Quiet Hours 등 Canvas 설정 그대로 적용. Canvas 트리거명 "Perform Price Drop Event"(재입고는 "Back in stock"). 수치(2026-11 기준): 알림 속도 분당 10,000명 이하 / "Notify all subscribed users" 시 10분간 100,000명 / 하루 최대 50,000개 업데이트 상품이 트리거 대상 / 동시 활성 구독 최대 1억 / 구독 유지 90일(그 안에 가격 미하락 시 해지). 구버전 제한은 X10.

**현장의 여정 빌더 고충** [커뮤니티 · C-패턴8·C-패턴1 · 검증 필요]
- Braze [스니펫]: "캔버스 빌더가 매우 제한적이며, 예를 들어 복사·붙여넣기 기능이 없다", "캔버스가 분기와 복제가 많아 복잡해지면 전체 구조를 파악하기 어렵다" (TrustRadius·Capterra, 직접 열람 403). ※ 공식 문서상 Canvas "복제" 기능은 존재 [W22] — 리뷰의 "복사·붙여넣기"는 단계 단위 편집을 말하는 것으로 보이나 확인 필요.
- Insider [스니펫]: Architect가 "without asking engineers every time" 여정을 짤 수 있다는 호평 / 2024년 3.0점 리뷰 "steep initial learning curve" (Gartner 리뷰).
- 진단: 여정 설계를 문서화(목표·진입 조건·이탈 조건·전환 이벤트)하지 않고 툴 위에서 바로 그리면 분기가 쌓여 아무도 전체를 이해하지 못함. "이미 구매한 사람 제외" 같은 exit 조건 누락이 대표 사고.

### 2.5 개인화·템플릿 — Liquid

**Braze Liquid** [웹 · W23 · 최상, 날짜 미표기 — 2026-11 조회]
- Shopify가 만든 오픈소스 템플릿 언어. 발송 전 메시지 내 Liquid를 수신자 데이터로 치환. Objects·Tags·Filters·Operators. "Liquid 5 from Shopify"까지 지원(일부 미지원 — 발송 전 테스트 필수). 신규 배열·수학 필터: at_least, at_most, compact, concat, sort_natural, where.
  > "Liquid is an open-source template language created by Shopify and used by Braze to power dynamic personalization."
  > 코드: `{{${first_name}}}`, `{{${city}}}`, `{% if ${language} == 'en' %}`, `{{"Big Sale" | upcase}}`
- 기본값 문법은 X25. Connected Content(외부 API 호출 개인화)는 BlaBlaCar 사례에서 사용 확인.
- Braze는 Shopify Liquid를 100% 지원하지 않는다(Braze 공식 FAQ https://braze.com/docs/user_guide/messaging/design_and_edit/personalize/liquid/faq) [커뮤니티 · C-패턴4가 인용 — web 리서치와 대조 필요]. W23의 "일부 미지원"과 방향 일치.

**Insider One Liquid / Dynamic Content** [웹 · W10 · 최상, 2026-10-20]
- Liquid 지원은 **얼리 액세스**(Insider One 팀에 문의해 참여). 지원 채널: App Push(standalone), Web Push, Enhanced Templates, Web Templates, Email, Transactional Email API v2, Architect 여정 내 Email·Enhanced Templates. 문법: 출력 `{{ }}`, 로직 `{% %}`, 필터 `|`.
  > `{{ price | times: 100 | round }}`
  > `{%- if condition -%}` ... `{%- endif -%}`
  > (web templates 문서) `{{ attribute.first_name }}` — 검색 스니펫 기준
- 레거시 개인화 = Dynamic Content(이벤트·이벤트 파라미터·속성으로 콘텐츠 개인화). 레거시 태그 형식은 X11. Liquid 태그 빌더 목록에는 PII가 나오지 않는다는 제약(스니펫).
- 비교 요지: "Braze Liquid는 GA·정식 기능(Liquid 5까지). Insider One Liquid는 2026-10 기준 얼리 액세스, 기본은 Dynamic Content." [웹 · W·D절]
- **문법 차이 주의(저술가용):** Braze 예시는 `{{${first_name}}}`(달러·중괄호 속성 참조), Insider 예시는 `{{ attribute.first_name }}`(스니펫). 두 제품 코드를 섞어 쓰지 말 것.

**Liquid 현장 고충과 휴리스틱** [커뮤니티 · C-패턴4·C-휴2·C-휴3 · 검증 필요]
- G2 [스니펫]: Liquid 의존 탓에 "steep learning curve and heavy QA burden" (직접 열람 403).
- 긍정: "it gives me a straightforward way to check the Liquid scripting by previewing it with different values" (AWS Marketplace, Yashaswi J., QA, 2026-10-28).
- [스니펫]: Connected Content를 익혀야 하고 Liquid·HTML·API·웹훅 기본 지식이 도움.
- Mavlers(Braze 에이전시, 이해관계): "limited developer time, steep Liquid learning curves, and delays in A/B testing".
- 진단: Liquid는 문법보다 **"값이 없을 때"(nil/blank) 처리와 발송 전 미리보기 QA**에서 사고가 난다.
  > "If there's no first name, we make sure we don't have any blank spaces." — Phiture(Alejandra Escobal, 2023-06-20)
  > "the CRM manager takes care of all the settings except the actual sending." / "CRM teams typically have limited resources" — 같은 글
- Phiture 예제 코드 자체에 변수명 불일치(`order_ide`/`order_id`, `product_link`/`product_url`, `favoriteProduct`/`favoriteProducts`) — 리서처 관찰, 원문 재확인 필요. QA 장 실례 후보.
- 세그먼트를 커스텀 속성으로 '굳혀서' 참조 [스니펫, Braze Bonfire]:
  > "The easiest way to do this is add a custom attribute to users in your segment then use liquid to insert your content based on that attribute."
- AI로 Liquid 작성 보조 흐름: BrazeAI Liquid Assistant, Claude Code 활용 강의(패스트캠퍼스 "물경력 NO! 몸값 올리는 AI CRM 완전 정복 : Liquid 커스텀·API 개인화 캠페인(w. Braze & Claude Code)"). 기능명은 1차 소스 확인 필요 [커뮤니티 · C-패턴4·C-패턴2]. 1차 소스상 BrazeAI Generative AI는 "카피·이미지·Liquid·HTML 템플릿·콘텐츠 리뷰 — Operator 경유" [웹 · W24 · 최상]. "Liquid Assistant"라는 이름은 1차 문서 목록에서 확인되지 않음.

**개인화 효과의 학술 근거 — "맥락 의존"**
- 제목줄에 이름 → 오픈 확률 약 **20%** 상대 증가(약 9.05% → 10.80%), 주 실험 세일즈 리드 **31%** 증가, 수신 거부 감소(수치 미확인) [논문 · P-G1 · Sahni, Wheeler & Chintagunta 2018 · 2차 출처 확인].
- **반대 증거:** 2023 Marketing Letters 34(4)(DOI 10.1007/s11002-023-09701-7, 제목·저자 미확인)가 이름 개인화 효과 재현 실패 — 오픈율·클릭률 개선 없음 [논문 · P-G1 · 2차 출처 확인: RePEc 요약].
- 반려동물 앱 필드 실험(595명): 개인화 푸시 > 일반 푸시, 보호자 이름 + 반려동물 이름 > 반려동물 이름만. 참여 이력 데이터 삽입도 효과가 있었으나 이름 개인화만 한 것보다 유의하게 더 크지는 않음 [논문 · P-F6 · Kim, Kim, Choi 2025 · abstract 확인]. 표본 작고 단일 앱.
- 서사 제안: "개인화는 효과가 있다/없다"가 아니라 "우리 고객에서 테스트해 보라" (G1 + 반례 + F6).

### 2.6 AI 기능

**BrazeAI (2026-11 기능 목록)** [웹 · W24 · 최상, 날짜 미표기]
- BrazeAI Operator(대시보드 대화형으로 캠페인·Canvas 구축·검토·분석), Braze Agents(발송 시점에 한 사용자 단위로 분류·라우팅·보강·작성), Decisioning Studio Go(수신자별 콘텐츠·타이밍·빈도 개인화), Decisioning Studio Pro(오퍼 포함 전 레버를 비즈니스·재무 지표에 맞춰 최적화), Intelligent Timing, Intelligent Channel filter, Optimize with BrazeAI(변형 테스트 후 승자로 트래픽 이동 — 구 Intelligent Selection), Winning Paths, Content Optimizer(beta), Generative AI(카피·이미지·Liquid·HTML 템플릿·콘텐츠 리뷰 — Operator 경유), Predictive Churn·Predictive Events(0~100 점수), AI item recommendations(딥러닝 카탈로그 추천), Braze MCP server(PII 제외 데이터를 Claude·Cursor 등 AI 도구에 노출).
- 연혁(신선도 주의): 2023-06-27 "Sage AI by Braze"로 AI 기능군 발표 → 이후 BrazeAI™로 통칭(일본어판 공식 글 2024-07 업데이트에서 "BrazeAI" 표기). 공식 개명 공지는 못 찾음. 문서 URL `/sage_ai/` → `/brazeai/` [웹 · W24 · 최상].
- 2025년(연간 리뷰, 2025-12-17): BrazeAI Decisioning Studio 정식 출시(강화학습으로 고객별 채널·메시지·오퍼·타이밍·빈도 결정), BrazeAI Agent Console 베타(Canvas·Catalog 안에서 리드 스코어링·현지화·여정 개인화), BrazeAI Operator 베타, Braze MCP Server, ChatGPT 앱 연동·ChatGPT Atlas Web SDK 지원 [웹 · W32 · 최상(자사)]. ※ 2025-12 시점 "베타"였던 Operator·Agent Console의 2026-11 현재 상태는 W24 목록상 명시 없음 — 본문에서 GA라고 쓰지 말 것.
- Decisioning Studio의 기원: OfferFit 인수 완료 2025-06-02. 인수가 $325M(2차 집계 기준, 재확인 필요) [웹 · W32].

**Insider One AI / Agent One** [웹 · W4 · 최상(공식 보도자료 신디케이션)]
- 2026-09-17 Agent One을 "자율 고객 참여를 위한 자기 최적화 지능 시스템"으로 발표. Agent One Teams(마케터 측: 목표·가드레일 설정 → 다음 최적 행동 선택, 기획·콘텐츠·오케스트레이션·최적화 전용 에이전트 호출, 결과로 학습) + Agent One Audiences(고객 측: 고객이 자기 말로 표현한 의도 해석). 명명된 에이전트: Shopping Agent, Support Agent.
  > "Agent One was built natively as one intelligence system" — Muharrem Derinkök, CPO
  > "Agent One autonomously makes and acts upon millions of decisions" — Serhat Soyuerel, CRO
- **연혁 주의:** 2025-03에 이미 "Agent One™" 출시 발표(Sirius AI™ 위에 구축된 자율 에이전트, Insight Agent 등). 2026-09 발표는 Teams/Audiences 구조로 재정의한 것. G2 제품명 "Insider One (Agent One, ex-Sirius AI)" → Sirius AI는 Agent One으로 흡수된 구 브랜드로 보는 것이 타당. Sirius AI 원 출시 주장은 X20.
- 2024-11: "생성형 AI를 활용하고, 고객 여정의 모든 단계에서 팀을 안내하는 Insider One AI 파일럿에 추가 투자를 계획하고 있습니다." — Muharrem Derinkok [웹 · W3].
- OpenAI 파트너십: 플랫폼과 Agent One 전반에 OpenAI 기반 지능 내장 [웹 · W5 · 중].

**발송 시간 최적화 비교**
- Braze Intelligent Timing [웹 · W25 · 최상]: 사용자별 과거 상호작용 통계 분석으로 "가장 참여도 높은 시간"(5분 단위 반올림)에 발송. 데이터: 세션 시간, 푸시 direct/influenced open, 이메일 클릭·오픈(기계 오픈 제외), SMS 클릭(링크 단축·고급 추적 켠 경우). 폴백: Most popular(워크스페이스 평균 세션 시작 시각) / Custom. 세션 데이터가 전혀 없으면 사용자 현지 오후 5시. 인앱·웹훅은 즉시 전달, API 트리거 캠페인에선 사용 불가, Canvas에선 Message 단계에서 설정.
  > "Use Intelligent Timing to deliver your message to each user when Braze determines a user's optimal send time"
- Insider Send Time Optimization [웹 · W12 · 최상, 2026-08-28]: 채널 단계에서 사용자별 최적 시간까지 대기 후 발송. 채널 Web Push, App Push, Email, SMS, WhatsApp. App Push·SMS·WhatsApp은 모바일 활동, Email·Web Push는 웹 활동으로 묶어 계산. 클릭을 가장 신뢰할 상호작용으로 가중, Architect 채널 클릭만 고려, 하루를 시간 단위로 나눠 산출. 24시간 범위. Silent hours 설정 가능(최적 시각이 걸리면 다음 최적 시각). 폴백 Send immediately / Send at. 제약: Dry Run·테스트 상태에서는 동작 안 함. 활성화 시 해당 채널에 Override Global Frequency Capping이 자동으로 켜짐.
  > "the best time to send for each individual user"
- 학술: 개인별 상위 10개 시간대 오픈율 **19.24%** vs 무작위 10개 시간대 **16.48%**(상대 약 17% 향상), 약 100만 고객·5개월, 관찰 데이터 기반(무작위 필드 실험 아님) [논문 · P-F1 · Singh et al. 2020, arXiv 프리프린트, 동료 심사 미확인 · 2차 출처 확인]. 학술 근거는 얇다(X21). Bidargaddi 2018의 시각별 효과 차이도 STO 근거로 쓸 수 있음(2.3).

**최적 채널**
- Braze Intelligent Channel filter(구 Most Engaged) — 선택 채널이 "최적" 채널인 사용자만 선별 [웹 · W25 · 최상].
  > "The `Intelligent Channel` filter (previously `Most Engaged`) selects the portion of your audience"
- Insider Next Best Channel — 사용자별 채널 참여 확률 점수를 읽고 도달 가능한 채널만 남겨 해당 경로로 보냄(스니펫) [웹 · W13 · 최상].

**AI 기능에 대한 현장 평가** — 4장 논쟁 C 참조.

### 2.7 추천

**Insider Smart Recommender** [웹 · W11 · 최상, 2026-10-26]
- 목적별 6개 그룹(2026-10 기준. 2024년 구 문서는 4개 그룹 — 구버전 정보일 수 있음):
  1. 인기·성과로 전환 유도: Top Sellers, Most Popular, Trending Products, Most Valuable Products
  2. 상품 발견·참여: New Arrivals, Real-Time User Engagement(트랜스포머 모델로 세션 내 실시간 브라우징 기반), User-Based, Chef(60일간 조합 테스트 후 슬롯별 최적 조합 자동 선택)
  3. 개인화: Recently Viewed, User-Based, Purchased with Last Purchased, Real-Time User Engagement
  4. 장바구니·AOV 증대: Purchased Together, Complementary Products(LLM 기반 추론으로 보완 카테고리 판단), Checkout Recommendation(무료배송 등 임계값 도달 도움, 이미 충족 시 미노출), Viewed Together
  5. 대안 제시: Similar Products, Visually Similar Products(이미지 비교), Viewed Together
  6. 캠페인·비즈니스 목표: Manual Merchandising·Mixed Strategy(신규 전략에서 더는 제공 안 됨 → Bundle Strategy 슬롯 사용), Highest Discounted Products, Location-Based Top Sellers(IP 위치)
- 관련: 유사도 엔진 페이지, BYOR(Bring Your Own Recommendation) 문서 존재.

**Braze** [웹 · W24 · 최상]: AI item recommendations(딥러닝 카탈로그 추천), Decisioning Studio(크로스셀 매핑).

**학술**
- Amazon 아이템 기반 협업 필터링 — "이 상품을 산 고객이 함께 산 상품", 상품 간 유사도를 오프라인 사전 계산 [논문 · P-H1 · Linden, Smith & York 2003 · 수치 미확인]. 함께 본/함께 산 추천 블록의 원리 설명용.
- Netflix: 추천이 시청 시간 **약 80%**에서 선택에 영향(나머지는 검색), 홈페이지에서 시청 시간 **3시간 중 2시간** 발견, 연간 **10억 달러 이상** 절감(X7) [논문 · P-H2 · Gomez-Uribe & Hunt 2015 · 2차 출처 확인].
- 추천의 비즈니스 가치 측정 리뷰: 오프라인 정확도 개선이 실제 비즈니스 가치로 이어지는지는 불분명 [논문 · P-H3 · Jannach & Jugovac 2019 · abstract 확인]. "추천 블록 넣었더니 CTR 올랐다 — 그게 매출 증분인가?"로 2.8과 연결.

### 2.8 테스트와 성과 측정

**도구 기능**
- Braze [웹 · W25·W22 · 최상]: 다변량 테스트 변형 최대 8개, 시작 후 제목·본문 변경 시 실험 무효화. Intelligent Selection(Optimize with BrazeAI) — 반복 발송 캠페인·변형 2개 이상·전환 이벤트 필요, 단일 발송엔 불가, 학습 기간 후 최종 분배 결정. Canvas Experiment Paths(Winning Path 포함), 리텐션·퍼널 리포트.
- Insider [웹 · W7·W8 · 최상]: Journey A/B Split, A/B autowinner, A/B 통계, 전환 목표, last-touch 어트리뷰션(Conversion Attribution Model 예: 마지막 클릭 채널에 전량 귀속), Dry Run, 랜덤 테스트.
- 데이터 export: Braze Currents(2.9), Insider 데이터 export [W7].

**현장** [커뮤니티 · C-패턴6·C-휴4 · 검증 필요]
- Monzo(Rodrigo Baptista, Senior Data Scientist, 2025-09-03): 유저의 2.5%를 6개월간 CRM 메시지에서 무작위 제외하는 유니버설 홀드아웃 운영. 어트리뷰션을 홀드아웃 기준으로 하향 보정(예: 홀드아웃 기준 100건, 어트리뷰션 200건이면 계수 0.5).
  > 어트리뷰션 모델은 "tend to claim too much"
  > "Individual experiment uplifts are non additive."
- CRM 실험 강의 [스니펫]: 캠페인 한 번의 대조군으로는 빈도·피로도 효과를 볼 수 없다 — 발송 주기(cadence)는 따로 실험하고 글로벌 홀드아웃 유지.
- Insider 리뷰: "The dashboard analytics still feel limited and not very flexible"(리테일, 2026-10-30) / "Sometimes it's hard to dig up the analytics we are looking for."(여행업) / "Third-party integrations, revenue analytics, and campaign analytics are very weak for me."(금융업).
- Braze 리뷰: "the dashboard makes it simple to see what's working at a glance." (Bret C.)
- 진단: 툴 대시보드는 열람·클릭 중심이고 "보내지 않았으면 어땠을까"는 대조군 설계 없이는 답할 수 없다. 성숙한 팀은 툴 밖(DW·BI)으로 데이터를 빼서 측정. 주니어는 CTR을 성과로 착각하기 쉽다.

**학술 — 효과는 작고, 대조군으로만 보인다**
- 25개 대규모 필드 실험(대부분 수백만 고객, 디지털 광고비 합계 280만 달러): 무작위 실험을 해도 광고 수익률을 정밀하게 재기 매우 어렵다. 유의미한 신뢰구간을 얻으려면 실험이 **1,000만 인-주(person-weeks)를 넘기기** 쉽다 [논문 · P-D4 · Lewis & Rao 2015 · 2차 출처 확인]. "컨트롤 그룹 5%로 효과를 보려 했는데 '유의하지 않음'만 나온다"의 이론적 설명.
- 고스트 광고: 대조군에 "노출되었을 사람"을 기록만 해 비용·노이즈 감소 [논문 · P-D5 · Johnson, Lewis & Nubbemeyer 2017 · 세부 수치 미확인]. 2017 Paul E. Green 상, 2022 Weitz-Winer-O'Dell 상 [2차 출처 확인].
- Facebook **663개** 실험 기준 비실험적 방법(DML, SPSM) 검증 — DML이 SPSM보다 낫지만 둘 다 잘 맞추지 못함. 리프트 추정의 절대 퍼센트포인트 차이 중앙값 퍼널 상단 **115%**, 중단 **107%**, 하단 **62%** [논문 · P-D6 · Gordon, Moakler & Zettelmeyer 2023 · 2차 출처 확인: arXiv abstract 인용]. "컨트롤 그룹 없이 '보낸 사람 vs 안 보낸 사람'을 비교하면 왜 안 되는가"의 가장 강력한 최신 증거.
- 온라인 통제 실험 가이드 [논문 · P-E1 · Kohavi et al. 2009 · abstract 확인]:
  > "Controlled experiments embody the best scientific design for establishing a causal relationship between changes and their influence on user-observable behavior."
  > "Our experience indicates that significant learning and return-on-investment (ROI) are seen when development teams listen to their customers, not to the Highest Paid Person's Opinion (HiPPO)."
- 교과서: Kohavi, Tang & Xu 2020 — SRM, 가드레일 지표, 신선도/초두 효과 [논문 · P-E2]. 더 읽을거리 추천.
- SRM: Microsoft 실험의 약 **6%**에서 발생 [논문 · P-E3 · 2차 출처 확인: Microsoft Research ExP 블로그]. 집필용 응용 예(저자 추론 아님): "50:50으로 나눴는데 이메일 수신자가 52:48이다" — 발송 실패·하드 바운스·푸시 토큰 없는 사용자 제외가 한쪽에만 걸리면 SRM.
- 엿보기(peeking) [논문 · P-E4 · Johari et al. 2022 · abstract 확인]:
  > "these inferences are wholly unreliable if users endogenously choose samples sizes by continuously monitoring their tests."
  "캠페인 대시보드를 매일 열어 보고 '이겼다' 싶을 때 끄면 안 되는 이유."
- 직관의 착각 [논문 · P-E5 · Kohavi, Deng & Vermeer 2022 · abstract 확인; 세부 항목(Twyman's law 등) 원문 미확인].
- 밴딧 — 실험하면서 동시에 이기기:
  - LinUCB: Yahoo! 프런트 페이지 **3,300만 건 이상** 이벤트, 맥락 없는 밴딧 대비 **클릭 12.5% 향상**, 데이터가 적을수록 이점 증가 [논문 · P-I1 · Li et al. 2010 · abstract 확인].
    > "Results showed a 12.5% click lift compared to a standard context-free bandit algorithm, and the advantage becomes even greater when data gets more scarce."
  - 톰슨 샘플링 실무 해설(Google 애널리틱스 콘텐츠 실험) [논문 · P-I2 · Scott 2015 · 세부 수치 미확인].
  - 소매은행 디스플레이 캠페인(노출 **7억 5천만 회 이상**): 2개월간 고객 획득률 **8% 향상**, 추가 비용 없음. 전환 대신 **클릭률을 최적화했다면 고객 획득이 약 10% 감소**했을 것 [논문 · P-I3 · Schwartz, Bradlow & Fader 2017 · 2차 출처 확인]. 교훈: 자동 승자 선택의 목표 지표를 클릭으로 잡으면 진짜 목표(전환)가 나빠진다 — Braze Intelligent Selection의 "전환 이벤트 필요"와 연결.
- 참여 ≠ 이익 [논문 · P-G2 · Wang, Lu & Shi 2022 · **abstract 확인**]: 미국 대형 세차 체인(구독형) 필드 실험. 보름 간격 이메일 2통(1개월) → 5개월 후 리텐션 가능성 **7.4% 증가**, 5개월간 이탈 오즈 **26.3% 감소**, 구독자 기간당 서비스 이용량 **7.0% 증가**, 효과는 시간이 지나며 감쇠·두 번째 메일 이후 **피로** 신호. 중간 등급 저빈도·최상위 등급은 이익 증가, 중간 등급 고빈도·기본 등급은 이익 **감소** → 선택적 발송 권고.
  > "Our study highlights that email engagement is a double-edged sword"
- 성과를 오픈율이 아니라 고객 가치 변화로 보라 — P-A2(개념만).

### 2.9 통합·데이터 연동

- **Braze Currents** [웹 · W27 · 최상]: 참여 이벤트의 실시간 데이터 스트림. Avro 형식으로 데이터 파트너에 export — Braze에서 나가는 가장 세분화된 export. CDP 라우팅: Tealium, Segment, mParticle. 엔타이틀먼트(커넥터별 Engagement Events, Customer Behavior Events, User Profiles and Attributes)로 과금 통제. 다수 Pro/Enterprise 패키지에 포함, 가격은 담당 AM 문의. S3·Snowflake·Redshift는 사이드바 문서에 등장하나 이 페이지에서 네이티브 목적지로 확인 안 됨(단, 카카오스타일 사례는 S3로 스트리밍 — 3.2).
  > "a real-time data stream of your engagement events"
  > "Engagement Events entitlements are required for each standard Currents connector you create."
- Braze Cloud Data Ingestion(유저 모델링 데이터 연동) — AB180 발표 소개 [웹 · W34 · 중].
- Braze Audience Sync(Facebook·Google 광고, 2025년 WhatsApp 광고 추가), Connected Content, Webhooks, Send to Destination, Braze MCP server, Shopify 연동 개선(2025) [웹 · W22·W24·W31·W32].
- Insider: 100개 이상 데이터 소스 연동 통합 허브 [W2], Architect "Call an API", Facebook Custom Audiences, Google Ads 요소 [W7], 카탈로그 소스 Clickstream·XML·Catalog API [W14], 자동 마이그레이터·사전 구축 인터그레이션(150개 브랜드 전환 주장, 2024-11) [W3].
- 현장 [커뮤니티 · C-패턴3 · 검증 필요]:
  - Braze: "Connecting API endpoints and setting up team workspace permission roles required unexpected workarounds." (Sung N., 2026-10-24) / "we had to develop a whole workaround." (구독 관리 기능, matias d., 2026-10-31)
  - Insider: "the initial setup still required developer help for custom API integrations" (Victor Adolfo G., 2026-10-06) / "We also had some questions during the integration, so we weren't fully independent there." (Kevin V., 2026-09-25)
  - The Grow Getter(전 Braze 사용자, 2023-11-10): 실시간 인사이트에는 "complex tech integration - that takes a lot of engineering resources". "1 engineer/marketing-tech specialist"를 3~4개월. "Not all CRMs are created equal. Some are more implementation heavy than others." "P.S: I still love Braze."

### 2.10 한국 특화 — 카카오톡·데이터 현지화·법규

**Braze 카카오톡 (2026-04 출시)** [웹 · W18·W19·W20 · 최상]
- 2026-04-08: AWS 기반 국내 데이터센터 오픈 — 전화번호 등 개인식별정보를 국내에 저장·활용, 데이터 현지화 요건 대응. 카카오 비즈니스 메시지와 연동되는 카카오톡 메시징 채널 출시.
  > "국내 기업들은 현지화된 기능과 글로벌 플랫폼의 강력한 인프라를 동시에 충족할 수 있는 균형을 필요로 해왔다." — Shahid Nizami, Braze APAC VP
  > "브레이즈 플랫폼과 카카오톡 비즈니스 메시지의 통합으로 브랜드의 고객 참여 역량이 크게 확대될 것으로 기대한다." — 전현수, 카카오 AD도메인 성과리더
- 국내 카카오톡 사용자 약 4,900만(2026-04 기준). 블로그: "97%의 보급률"(Statista 인용), "약 4,900만 명의 활성 사용자".
- **친구톡 지원**(2026-04-07 블로그): 텍스트·이미지·와이드 이미지·와이드 아이템 리스트. 대시보드 공급자 관리, 노코드 작성기·실시간 테스트, 동적 개인화(상품 추천·포인트·실시간 알림), 클릭 추적 기반 리타깃팅(미클릭자에게 푸시·이메일 후속), Canvas로 카카오톡+푸시·이메일·웹·유료 미디어 연동, Audience Sync로 카카오톡 전환자 광고 노출 중단. 산업별 예: 리테일(장바구니 이탈·플래시 세일), 미디어(재참여·콘텐츠 추천), 금융(온보딩·맞춤 프로모션).
  > "친구톡 메시지는 카카오톡 플랫폼에서 내 채널을 팔로우하는 카카오톡 친구에게 메시지를 보낼 수 있는 기능입니다."
  > "대시보드 내 공급자 관리와 일회성 자격 증명 입력으로 설정을 간소화하세요."
- **알림톡·브랜드 메시지: 미확인 — X1.**
- 설정(Set up KakaoTalk 문서, 날짜 미표기 © 2026 — 2026-11 조회):
  > KakaoTalk "is a messaging channel that enables broadcast messaging and 1:1 chat with users."
  - 지원 파트너: CJ올리브네트웍스 또는 Infobip.
  - 사전 요건: 지원 파트너 계정, 카카오톡 비즈니스 채널(사업자등록증·대표자 신분증 등 비즈니스 인증), 유효한 Sender Key, 채널 관리자 연락처, 공급자에 Braze 클러스터 IP 허용(allowlist).
  - 제약: Sender Key는 한 번에 한 워크스페이스에만 연동. CJ올리브네트웍스는 단일 공통 ID에 매핑된 채널만 등록 가능. 채널 정보는 제출 서류와 정확히 일치해야 함. 전화번호는 E.164 형식만(예 `+821025749774`). Infobip은 광고 메시지 발송 시 고객센터 연락처 필수.
  - 단계: (1) 공급자 대시보드에 Braze IP 허용(CJ: 계정 관리 > 상세 보기 > 센터 & 업로드 IP 허용 목록) (2) 카카오톡 채널 관리자센터에서 비즈니스 채널 신청 (3) 자격 증명 수집 — CJ: Comm.One 로그인 ID·Sender Key·채널명·발신번호·크리덴셜 ID/PW / Infobip: API base URL·API key·sender key·sender profile UUID·채널명 (4) Braze Partner Integrations > Technology Partners에서 공급자 선택·입력·저장 (5) E.164 전화번호로 사용자 CSV/API 임포트.
  - ※ 예시 전화번호 `+821025749774`는 문서 예시 원문 — 본문 예시로 쓸 때는 가상의 번호로 바꾸는 편이 안전(실제 번호일 가능성 배제 불가).

**Insider One 한국 채널** — 카카오톡 미확인(X2). 한국어 페이지 채널 목록은 웹·앱·이메일·웹 푸시·SMS 및 RCS·WhatsApp·인스토리·대화형 CX·사이트 검색 [W2].

**한국 채널 비용·법규(현장 수준만)** [커뮤니티 · C-패턴5 · 검증 필요]
- "플러스친구와 LMS는 비용이 비싸고, 앱푸시·인앱·eDM은 비용이 적은 편" [스니펫].
- 앱푸시 외에 알림톡·친구톡·LMS 비용 구조가 있고, 정보통신망법 광고성 정보 규정(야간 발송·수신 동의)이 있다 — **1차 법령/KISA 자료 미확보(X17).**
- 동의 관련 도구 개념: Insider의 Promotional(opt-in 필요) vs Transactional(opt-in 불요) 구분 [W8]. Braze 가격 인하 알림은 opt-in 사용자만 수신, Quiet Hours 적용 [W29]. Insider STO의 Silent hours [W12]. Infobip 광고 메시지 고객센터 연락처 필수 [W20]. → 법규 장에서 "도구가 제공하는 장치"로는 쓸 수 있으나, 법 조문 해석과 연결하려면 1차 확인 필요.

**프라이버시·동의 (학술)**
- EU e-Privacy Directive(2002/58/EC) 전후 9,596개 캠페인·330만 명 응답자, 유럽 광고 효과 평균 **약 65% 감소**(측정 지표는 "설문으로 측정한 구매 의향") [논문 · P-K1 · Goldfarb & Tucker 2011 · 2차 출처 확인, 본문 직접 확인 못 함]. 1st-party 데이터·동의 기반 CRM 서사의 출발점.
- GDPR 옵트인: 중개업체 관찰 소비자 수 **12.5% 감소**, 남은 소비자는 더 오래 추적 가능(약 **8%** — 한 2차 요약에만, 보수적으로), 남은 소비자의 평균 가치가 올라 손실 대부분 상쇄, ML 예측 정확도 유의하게 나빠지지 않음 [논문 · P-K2 · Aridor, Che & Salz 2023 · 2차 출처 확인]. "동의한 고객은 줄지만 더 선명해진다."
- GDPR 다음 주 EU 대상 웹사이트 벤더 사용 **15% 감소**, 시장 집중도 **17% 증가**, 2018년 말 대부분 회복되었지만 광고 벤더 범주는 지속 [논문 · P-K3 · Johnson, Shriver & Goldberg 2023 · abstract 확인]. 부록/칼럼용.
- 유럽 인기 웹사이트 **60% 이상**이 쿠키 동의 배너, 독일 방문자 **8만 명 이상** 3개 실험 — 하단(왼쪽) 배너 상호작용↑, 이진 선택이 개별 허용보다 추적 수락↑, 넛지가 큰 영향 [논문 · P-K4 · Utz et al. 2019 · abstract 확인].
  > "Our experiments show that seemingly small implementation decisions can substantially impact whether and how people interact with consent notices."
  - 쿠키 배너 연구이므로 푸시 권한·수신 동의 UI에는 "같은 원리가 적용될 가능성"으로 조심스럽게 연결. 넛지는 다크 패턴·법적 리스크와 함께.
- 멀티채널 유도: 이탈리아 도서 소매 3만 명 이상, 4개 캠페인 — 잘 설계된 캠페인이 멀티채널 고객 비율·평균 수익성을 모두 높였고, 효과는 **비금전 인센티브**에서 나옴(반발 감소·지각된 통제감 증가) [논문 · P-J4 · Montaguti, Neslin & Valentini 2016 · 2차 출처 확인]. "쿠폰 없이도 채널 확장(앱 설치·카카오 채널 추가)을 유도할 수 있다."

---

## 3. 대표 사례

> 모든 성과 수치는 **벤더 게재/자체 보고**다(X3). 기준값·표본·유의성 비공개.

### 3.1 잡코리아 × Braze (한국, 개인화·온보딩) [웹 · W30 · 최상(1차, 자체 보고) / 커뮤니티 · C-사례1]
- 날짜 미표기. 본문 통계 "23년 7월 기준", 캠페인 2023-11경, 2024 상반기 계획 언급 — 구버전 정보일 수 있음. 파트너: 팀 맥소노미(Team Maxonomy).
- 문제: 지원 이후 단계(서류·면접·결과) 추적 불가, 프로필·이력서 작성 전엔 신입/경력 구분 불가, 경력자 구직 활동 민감성 탓 푸시 타이밍 어려움, 웹 푸시는 리소스 대비 효과 불명확해 보류.
- 실행: 마케터가 개발 도움 없이 세그먼트 구성. 커스텀 속성은 Canvas·실시간·CSV 일회성 업로드로 갱신. Liquid로 가입일을 날짜 형식으로 바꿔 경과 일수 계산(가입일과 현재일 차이), 기업명·직무·희망 직무·경력 연수로 개인화. 이력서 미등록자 대상 슬라이드업 인앱. 랜덤 샘플 사전 테스트, 색상·크리에이티브·아이콘(로고·마스코트) A/B 테스트. 채널: 푸시, 인앱(IAM), 웹 인앱.
  > 카피 예: "잡코리아에 가입한 n일동안, 경쟁자들은 연봉 UP하고 있어요!"
  > "CRM 담당자인 제가 다양한 시도를 할 수 있었던 배경에는 Braze가 있었습니다." — 한은파 매니저, 잡코리아
- 성과(벤더 게재): "평균 CTR 4-5배 증가"(커뮤니티 원천의 문장: "이전과 비슷한 모수여도 평균 CTR이 4~5배 수준이나 오를 정도로 좋은 유입 성과"), 지원자 데이터 개인화 메시지 CTR "5%p 이상 향상", 슬라이드업 모달 CTR "두 자리 수에 육박"(같은 목표 다른 인앱 대비 약 4%p↑), CVR은 대조군(CG)보다 높음.
- 회원 수: 개인회원 2,200만+·기업회원 220만(2023-07 기준; 본문 내 "2천만 누적회원" 표기 불일치).
- 쓰임: Liquid 개인화 장의 대표 실습(날짜 계산 → 문구 삽입), 마케터 자율성의 긍정 사례.

### 3.2 카카오스타일(지그재그) × Braze (한국, 측정) [커뮤니티 · C-사례2 · 벤더 게재, 게재일 미표기]
- Braze Currents로 메시지 참여 이벤트를 AWS S3에 실시간 스트리밍, 회원 등급·연령·구매 이력과 결합해 QuickSight 대시보드, 세그먼트별 크리에이티브 반응을 프로모션 팀에 공유. 채널: 푸시·인앱·카카오톡 채널.
- 성과(벤더 게재): "our app traffic has jumped by 35%"
- 출처 URL이 `www-origin.braze.com` 도메인 — 정식 URL 확인 권장.
- 쓰임: "툴 밖으로 데이터를 빼야 진짜 분석이 된다."

### 3.3 BlaBlaCar × Braze (해외, 장바구니(예약) 이탈) [웹 · W31 · 최상(자체 보고), 날짜 미표기 — 2022년 이후]
- Canvas Flow로 예약 이탈 여정. 진입 세그먼트(예약자/카풀 검색·조회자/버스 검색·조회자/나머지), Action Paths로 1시간 등 정해진 시간 대기 후 미예약자 분기, Experiment Paths로 대조군, 커스텀 이벤트 속성으로 검색 지역 삽입, Connected Content, Audience Sync로 미전환자에게 Facebook·Google 광고. 채널: 이메일, 푸시, Content Cards, 인앱, 웹훅, Audience Sync.
  > "up to a 48% uplift in their message click rate and up to a 30% uplift in conversions (bookings)"
- 쓰임: 장바구니 이탈 따라하기의 모델 케이스.

### 3.4 Samsung × Insider (한국 본사, 시장 미특정) [웹 · W15 · 중~최상, 사례 페이지 날짜 미표기 — 2026-11 조회, 구버전일 수 있음]
- 갤럭시 노트 출시 20일. Architect, Web Push(재방문·장바구니 회수), 개인화 검색·Web Overlays, Category Optimizer, Smart Recommender.
- 헤드라인: "Increases Conversions by 275% in 20 days"
  > "With all strategies combined, we were able to increase conversions by 275% in just 20 days." — Samsung CMO(실명 없음)
- 세부: 웹 푸시로 전환 24% 증가, CTR 14% 증가, Category Optimizer로 CVR 10% 증가, 20일간 갤럭시 노트 매출의 9%.
- **경고:** 275%가 "CVR 증가"인지 "CVR 기여"인지, 9%가 전체 매출 대비인지 Overlays 매출인지 페이지 내 표현 불일치 — 헤드라인 문장만 쓰고 "벤더 발표" 명시.

### 3.5 adidas × Insider (해외, 온사이트 개인화·크로스셀) [웹 · W15 · 이미지 경로상 2023-07 추정]
- Web Suite, 예측 세그먼트, 사이드 메뉴 쿠폰, Category Optimizer, Smart Recommender.
- 헤드라인: "increased AOV by 259% and conversion rate by 13%"
- 세부: 신규 사용자 AOV 259% 증가(1개월), 첫 구매 전환 82% 증가, 재방문자 전환 35.3%·수익성 42.1% 증가, 모바일 세션당 조회 상품 수 67.3% 증가, 모바일 전환 50.3% 증가, Smart Recommender로 사용자당 매출 18.8% 증가(**제목은 18.5% — 불일치**), 장바구니 담기까지 시간 76.5% 감소, 홈페이지 전환 13% 증가.

### 3.6 Insider 사례 목록 헤드라인 (2026-11 조회, 원문 그대로) [웹 · W15]
Coca-Cola "increased CVR by 19%" / Toyota "increased test drive applications by 166%" / Lexus "drove 12X ROI growth" / Renault "decreased wait times by 93% and drove CVR by 4%"(WhatsApp) / PUMA "increased CVR by 27%" / New Balance "uplifts conversion rate by 556%" / Nissan "increased test drive applications by 53.6% in two weeks" / Garanti BBVA "increased conversion rates by up to 502%" / Braun "Influenced 18% of Ecommerce Revenue in 8 Months" / Avis "saved 39% of costs in 12 months". Hyundai·Levi's·Generali·HP·Lenovo는 헤드라인 수치 없음.

### 3.7 WhatsApp Commerce (Insider, 해외) [웹 · W16 · 중, 2023]
- 출시 자료: 한 리테일러가 장바구니 이탈 61% 감소, 월 AOV 38% 개선. Clarins 멕시코: WhatsApp 매출 20배, opt-in 400% 증가, 2년간 디지털 순매출 기여 8% 증가(사례 집적 사이트 casestudies.com).

### 3.8 레노버 코리아 × Insider [커뮤니티 · C-사례3 · [스니펫], 2023-10 게시]
- 자사몰 오디언스별 맞춤 경험, 담당자가 고관여 제품군에 고객 여정 자동화 추천. 구체 수치 미확인.
- Insider 한국어 고객 페이지의 "웹사이트 개인화 캠페인으로 전환율 최대 78% 개선" — 브랜드·조건 불분명(벤더 게재).

### 3.9 Braze 2025 연간 리뷰 속 사례 [웹 · W32 · 최상(자사), 자체 보고]
24S 장바구니 담기율 7%↑·구매 전환 35%↑ / Kayo Sports FY24 구독 14%↑·크로스셀 105%↑(가격 20% 인상에도) / Stash 유료 구독자 130만+ / Wendy's 인앱 노출 1,000만+·신규 디지털 계정 55만+.

### 3.10 네이버웹툰 × Braze [웹 · W34 · 중]
- 브레이즈 커넥션 서울 2024에서 CRM 효율화 사례 발표 — 수치 없음.
  > "네이버 웹툰 이종한 리드와 함께 네이버 웹툰의 CRM(고객 관계 관리) 효율성을 강화했던 사례를 상세히 공유해 주목을 받았다."

### 3.11 Monzo (해외, 측정 방법론) — 2.8 참조 [커뮤니티 · C-휴4].

---

## 4. 논쟁점·상충 관점

### 논쟁 A: "비기술 마케터도 혼자 쓸 수 있다" vs "개발·데이터 리소스 없이는 반쪽짜리" [커뮤니티 · C-논쟁A]
- **관점 A (혼자 가능):** Braze 라이프사이클 마케터 — 크로스채널 오케스트레이션·실시간 세그먼트, SQL 불필요 [스니펫, Capterra]. Insider 금융업(2026-09-22): "my team could build and optimize journeys fully independently without heavy technical support." 잡코리아: 마케터가 개발 도움 없이 세부 세그먼트 구성(W30).
- **관점 B (리소스 필수):** The Grow Getter "complex tech integration - that takes a lot of engineering resources." / Insider Victor Adolfo G. "the initial setup still required developer help for custom API integrations" / Braze Sung N. "required unexpected workarounds."
- 커뮤니티의 화해 지점: 도입·연동 단계는 개발 의존, 데이터가 잘 깔린 뒤 운영 단계는 마케터 자율. 주니어가 들어가는 시점(이미 도입된 회사인지)에 따라 체감이 정반대.

### 논쟁 B: 학습 곡선 — 쉬운가 가파른가 [커뮤니티 · C-패턴1]
- **관점 A (쉽다):** "It is very easy to understand and use for day-to-day promotional and transactional communications." (Braze, Yashaswi J., 2026-10-28)
- **관점 B (가파르다):** "Because Braze is so feature-dense, configuring campaigns can feel overly complicated." (Bret C., 2026-10-26) / "there is a steep learning curve that makes getting use to it difficult" [스니펫] / "steeper learning curve and more time required during the initial implementation than other plug-and-play marketing automation platforms like Pardot and Marketo. But it is so worth it." [스니펫] / "for non-technical teams, some of the advanced features (events, integrations, dynamic content, liquid templating) can have a learning curve" / "can feel overwhelming if you have a lean team" [스니펫]. Insider: "There was a steeper learning curve than we expected, and the implementation process could have been smoother." (여행업, 2026-10-29) / "there is a big learning curve and the platform is complex." (패션업, 2026-10-29). G2 집계: Insider One 리뷰 약 81건 "steep learning curve", 약 37건 "time-consuming setup" [스니펫].
- 갈리는 지점: 단발 푸시·이메일은 쉽고, 캔버스/여정·이벤트 데이터·동적 콘텐츠로 넘어가면 어렵다. 커뮤니티 진단: 고급 기능이 전부 데이터 모델 이해를 전제하기 때문.

### 논쟁 C: Insider One vs Braze — 어느 쪽이 쉬운가, 무엇에 강한가 [커뮤니티 · C-논쟁B / 웹 · W·D절]
- **관점 A (Insider가 쉽다·웹 개인화 강점):** CleverTap 비교 글(경쟁사 — 편향) — Insider가 셋업·지원에서 높은 점수 [스니펫]. G2 평점 X22. "the human customer service stands out and has been remarkable"(여행업, 2026-10-29). Gartner Personalization Engines Leader(W17).
- **관점 B (Braze가 복잡 여정·앱 중심에 강함):** 같은 비교에서 Braze는 복잡한 캔버스 기반 여정에 강하다는 평, Insider도 셋업이 "overwhelming"할 수 있다는 지적 [스니펫]. Gartner MMH 리더 4년 연속(W33).
- 주의: 비교 콘텐츠 대부분이 벤더(Insider 자사 블로그, CleverTap)가 쓴 것. 웹 리서치도 "3자 비교 블로그(경쟁사 작성 비교글 다수 — 편향)"를 제외했다. 독립 실무자 비교 토론(Reddit 등) 미확보. 한국 채널 축에서는 2026-11 현재 Braze만 카카오톡(친구톡)이 확인됨.

### 논쟁 D: AI 기능 — 생산성 도구인가, 아직 미덥지 않은가 [커뮤니티 · C-논쟁C]
- **관점 A:** "I find the AI Agent really helpful, especially since I can now use prompts to create gamified pop-ups." (Insider 금융업, 2026-10-19). BrazeAI Liquid Assistant가 개발자 개입 없이 Liquid를 쓰게 한다(에이전시 주장).
- **관점 B:** "On the AI side, it's not always consistent" (Kevin V., 2026-09-25) / "The AI feels only average overall: accuracy, consistency, explainability, controls, and trust are all just mid-level." (금융업, 2026-09-22) / "I did not enjoy using Insider AI to generate copies" (PeerSpot, 2026-10-08).
- 벤더 측 주장(관점 A 쪽 1차): Agent One "autonomously makes and acts upon millions of decisions"(W4). Braze는 Predictive Suite는 결과로 학습·정확도 보고하지만 Braze Agents는 결과로 학습하지 않는다고 스스로 구분(W26).
- 쓰임: "AI가 써준 Liquid·카피도 결국 QA는 사람이 한다."

### 논쟁 E: 피로도 관리의 단위 — 발송량 vs 관련성 vs 측정 [커뮤니티 · C-논쟁D]
- **관점 A (빈도 상한):** Braze 권고 — 전역·채널별 상한 겹쳐 쓰기(벤더).
- **관점 B (관련성):** Airship — 발송 수보다 관련성(벤더). 고구마팜 — "브랜딩 메시지 없이 무작정 CRM 채널을 확장"이 실수.
- **관점 C (측정):** 피로도는 캠페인 단위 실험으로 보이지 않으므로 cadence 실험·글로벌 홀드아웃(CRM 실험 강의, Monzo). 학술: Wang·Lu·Shi 2022의 두 번째 메일 이후 피로 신호(P-G2).
- 도구 간 긴장: Insider STO를 켜면 Override Global Frequency Capping이 자동으로 켜진다(W12) — STO와 빈도 상한이 충돌하는 지점.

### 논쟁 F: 개인화 효과 — 있다 vs 재현 안 된다 [논문 · P-G1·P-F6]
- **관점 A:** Sahni et al. 2018 이름 개인화 오픈 약 20%↑, 리드 31%↑ [2차 출처 확인]. Kim·Kim·Choi 2025 이름 두 개 효과 [abstract 확인]. 잡코리아 CTR 4~5배(벤더 게재).
- **관점 B:** 2023 Marketing Letters 재현 실패 [2차 출처 확인].
- 결론 방향: 맥락 의존 — 자기 고객으로 테스트.

### 논쟁 G: 리텐션의 경제성 — 통념 vs 근거
- **관점 A (업계 통념):** Reichheld & Sasser 1990 "이탈 5% 감소 → 이익 25~85% 증가"(HBR 기사, 은행 지점 85%·보험 중개 50%·자동차 정비 체인 30%) [2차 출처 확인]; "신규 획득 비용은 유지 비용의 5배"(학술 출처 미확인).
- **관점 B (비판):** 사례 기반 추정, Byron Sharp 등 "사고 실험에 가깝고 리텐션 비용을 0으로 가정" 비판 [2차 출처 확인]. Ascarza 2018 — 고위험 고객 겨냥 리텐션은 헛수고일 수 있음. Wang·Lu·Shi 2022 — 참여 증가가 이익을 깎을 수 있음.
- 사용 규칙: X4.

### 상충 데이터 (수치 불일치) 모음
| 항목 | 상충 | 처리 |
|---|---|---|
| Insider 고객 수 | 1,500+(2024-11) vs 2,000+(2025-12~) | X23 |
| Bluecore 인수일 | 2026-05-13(1차) vs 2026-06-03(일부 2차) | 05-13 채택 |
| Samsung 275%·9% | 지표 정의 불일치 | 헤드라인만 |
| adidas Smart Recommender | 18.8% vs 제목 18.5% | 인용 시 둘 다 병기하거나 생략 |
| 잡코리아 회원 수 | 2,200만+ vs "2천만 누적회원" | 시점·정의 명시 |
| Smart Recommender 그룹 수 | 6개(2026-10) vs 4개(2024 구 문서) | 6개, "2026-10 기준" |
| Lemmens & Gupta 효과 | 4% / 2,800만 달러 / 2배 이상 | X5 |
| Reichheld 수치 | 원천 25~85% vs 흔한 표기 25~95% | X4 |
| Braze Canvas "복제" | 공식 문서엔 복제 기능 / 리뷰는 "복사·붙여넣기 없음" | 범위 차이 가능, 확인 필요 |

---

## 5. 실무 적용 팁

### 5.1 유스케이스 ↔ 기능 매핑 (본문 설계 힌트) [웹 · W·C절 기반 + 논문 연결]

| 유스케이스 | Braze | Insider One | 근거 | 학술 연결 |
|---|---|---|---|---|
| 온보딩 | Canvas + 커스텀 속성/이벤트, 인앱 슬라이드업 | Architect starter + Wait/Check | W22, W30 / W6~8 | P-A1 |
| 장바구니 이탈 | Canvas Action Paths + Experiment Paths + Connected Content + Audience Sync | Architect + Web Push 장바구니 회수, WhatsApp Commerce | W31 / W15, W16 | P-D6(대조군 필요) |
| Win-back | Predictive Churn(0~100) + Intelligent Channel | Predictive Segments + Next Best Channel | W25, W26 / W13 | P-C2, P-C3 |
| 크로스셀 | AI item recommendations(카탈로그), Decisioning Studio | Smart Recommender(Purchased Together·Complementary 등) | W24 / W11 | P-H1, P-H3 |
| 로열티 | Liquid로 포인트 개인화, 친구톡 동적 콘텐츠 | Dynamic Content/Liquid(얼리 액세스) | W19, W23 / W10 | P-B1(RFM) |
| 가격 인하 알림 | Catalog trigger "Perform Price Drop Event" | Architect "On Price Drop" starter | W29 / W14 | — |
| 발송 시간 | Intelligent Timing | Send Time Optimization | W25 / W12 | P-F1, P-F2 |
| A/B 테스트 | 다변량(최대 8 변형), Intelligent Selection/Optimize, Winning Path | Journey A/B Split, A/B autowinner | W25, W22 / W7 | P-E1~E5, P-I1~I3 |
| 멀티채널 유도 | Canvas 크로스채널 | Architect 크로스 플랫폼 | W22 / W7 | P-J4 |

### 5.2 현장 노하우 (커뮤니티 휴리스틱, 검증 필요)
1. **발송 가능한 모수부터** — 세그먼트를 처음부터 잘게 쪼개지 말 것 [C-휴1].
2. **Liquid는 "값이 없을 때"를 반드시 설계하고 여러 값으로 미리보기** [C-휴2]. Braze 공식 FAQ도 Liquid가 들어간 메시지는 발송 전 모두 테스트하라고 권함. Insider는 샘플 프로필로 동적 콘텐츠 미리보기 기능 제공(W7).
3. **Liquid로 세그먼트를 복잡하게 판별하지 말고 커스텀 속성으로 굳혀 참조** [C-휴3].
4. **전체 효과는 유니버설 홀드아웃, 개별 기여는 어트리뷰션을 홀드아웃에 맞춰 보정** [C-휴4, Monzo]. 학술 근거 P-D4·P-D6.
5. **도입 전 '마케팅 테크 담당 1명'을 3~4개월 붙일 수 있는지 확인** — "1 engineer/marketing-tech specialist"; 실시간 커뮤니케이션 의존도("heavily reliant on real time communications")가 낮으면 다른 CRM 고려 [C-휴5, The Grow Getter].
6. **CRM은 푸시가 아니라 "why·what·how"부터** [C-휴6, 이오플래닛].
   > "실행을 위한 \"why, what, how\" 가 정말 중요하다."
   > "언제, 어떤 내용으로, 무엇을 유저에게 제공할 지에 따라" 고객 경험이 좋아지거나 이탈이 생긴다.
7. **여정은 툴 위에서 바로 그리지 말고 문서화부터** — 목표·진입 조건·이탈 조건·전환 이벤트. "이미 구매한 사람 제외" exit 조건 누락 주의 [C-패턴8].
8. **반응 확인 무한 반복** — "고객의 반응을 확인하는 과정을 무한 반복하는 거죠" (고구마팜) [C-패턴5].

### 5.3 도구별 함정 체크리스트 (1차 문서 기반)
- Braze Intelligent Timing: API 트리거 캠페인에선 사용 불가, 인앱·웹훅은 즉시 전달, 세션 데이터 없으면 현지 오후 5시 [W25].
- Braze 다변량: 시작 후 제목·본문 변경 시 실험 무효화. Intelligent Selection은 단일 발송 불가·전환 이벤트 필요 [W25].
- Braze 익명→식별 병합: "Not all data is merged from the anonymous profile." [W21]
- Braze 카카오톡: Sender Key 1 워크스페이스, E.164 형식, 채널 정보 서류 일치 [W20].
- Insider STO: Dry Run·테스트 상태에서 동작 안 함, 켜면 Override Global Frequency Capping 자동 ON [W12].
- Insider On Price Drop: Product ID 파라미터 없는 이벤트 불가, 가격 인상 트리거 불가, 미방문자 도달은 XML/Catalog API만 [W14].
- Insider Liquid: 얼리 액세스 — 계정에서 쓸 수 있는지 먼저 확인 [W10].
- Insider 커스텀 이벤트·속성: 월 데이터 포인트 소비에 영향 [W9].
- Insider 프로모션 여정: opt-in 필요 [W8].

### 5.4 학술 소재 활용 가이드 [논문 · 챕터별 활용 팁]
- 가장 강한 "반전" 소재 3개: Ascarza 2018(고위험 고객 겨냥은 헛수고), Gordon et al. 2023(관찰 분석 오차 중앙값 62~115%), Wang·Lu·Shi 2022(메일 2통이 리텐션은 올리고 이익은 깎음).
- "효과는 작다" 현실 감각: Bidargaddi 2018 +3.9%, Singh 2020 19.24% vs 16.48%, Lewis & Rao 2015 "1,000만 인-주".
- 재현 실패도 가르치기: Sahni 2018 vs 2023 Marketing Letters.
- 수치를 쓰면 안 되는 곳: X4~X9.
- 비유 후보(원 리서처 제안): 등고선 지도(등가치 곡선), '가장 아픈 환자'가 아니라 '치료가 듣는 환자'(업리프트), 노이즈 낀 라디오의 작은 목소리(Lewis & Rao), 열은 여러 병의 증상(SRM), 카지노 슬롯머신(밴딧).

### 5.5 주니어 학습 경로 (부록 "더 배우기" 재료) [웹 · W35 · 최상~중]
- Braze: 무료 Practitioner Learning Path(https://lab.braze.com/path/braze-practitioner), Braze Certified Practitioner 시험 60분·합격 후 3년 유효, 장바구니 이탈 코스(https://learning.braze.com/build-an-abandoned-cart-user-journey). 비고객도 Practitioner 시험 준비 콘텐츠 접근 가능하다는 커뮤니티 답변(2023, 구버전일 수 있음).
- Insider One: Insider One Academy(academy.insiderone.com).
- 한국어 유료 강의(인프런·패스트캠퍼스·코멘토)는 존재하나 품질 편차 — 인프런 수강평(sihyun park, 2022-11-12, 3점): 정확한 절차 없이 "이렇게 입력하라"식, CSV 업로드 예시에 파일 형식 안내 없음, 수강 동기 "Braze 강의 중 가장 저렴해서" [커뮤니티 · C-패턴2].
  > "CRM 마케터의 채용 공고 자격요건/우대사항 등에는 브레이즈 활용 역량이 포함되어 있습니다. 그러나 마땅히 배울 곳도, 알려줄 수 있는 사람도 많지 않은 것이 현실입니다." — 인프런 강의 소개(홍보 성격)
- 서문 포지셔닝 근거: "이 책이 당신의 사수다" [C-패턴2 활용 제안].

### 5.6 챕터 오프닝 장면 후보 (커뮤니티 제안)
- 1장: "첫 주에 푸시는 보냈다. 그런데 캔버스를 여는 순간 막혔다" [C-패턴1]
- 데이터 장: "세그먼트를 만들려는데 필요한 이벤트가 없다. 개발팀 지라 티켓은 3주 뒤" [C-패턴3]
- 측정 장: "CTR 12%를 보고했더니 팀장이 물었다. '안 보냈으면 몇 명이 샀을까?'" [C-패턴6]
- Win-back 장: "이탈 예측 점수 상위 10%에게 쿠폰을 보냈는데 효과가 없었다 — 왜?" [P-C2]
- 테스트 장: "50:50으로 나눴는데 이메일 수신자가 52:48이다" [P-E3 응용]

---

## 6. 참고문헌

### 6.1 웹 (벤더 공식·매체)
- Insider One. Insider Becomes Insider One. https://insiderone.com/news/insider-becomes-insider-one/ , 2025-12-09 (뉴스룸 목록 2025-12-08). [W1]
- Insider One. 플랫폼(한국어). https://insiderone.com/ko/platform/ , 날짜 미표기 — 2026-11 조회. [W2]
- Insider. 인사이더 시리즈E 및 한국 투자 발표. https://insiderone.com/ko/news/insider-kr-invest-1500-krw-create-60-jobs-following-500m-usd-series-e (영문 https://www.businesswire.com/news/home/20241031435852/en/), 2024-11-01. [W3]
- Insider One. Agent One 출시 보도자료. https://techintelpro.com/news/ai/agentic-ai/insider-one-introduces-agent-one-for-autonomous-customer-engagement , https://insiderone.com/zh-hant/news/insider-one-autonomous-customer-engagment/ , 2026-09-17. 2025-03 Agent One: https://useinsider.com/?p=520348 . G2: https://ai.g2.com/evaluations/categories/marketing/insider-one-agent-one-ex-sirius-ai . Sirius AI: https://martechseries.com/predictive-ai/ai-platforms-machine-learning/insider-announces-sirius-ai-the-worlds-most-comprehensive-generative-ai-solution-for-cx-making-marketing-teams-60-more-productive/ (발행일 미확인). [W4]
- Pulse 2.0 / FirstMark. Insider One acquires Bluecore. https://pulse2.com/insider-one-acquires-bluecore-to-expand-agentic-ai-customer-engagement-platform/ , https://firstmark.com/story/bluecore-acquired-by-insider-one/ , 2026-05-13. Insider One. OpenAI partnership. https://insiderone.com/news/openai-partnership/ , 2026-03(1차 날짜 미확인). [W5]
- Insider One Academy. Introduction to Architect. https://academy.insiderone.com/docs/introduction-to-architect.md , 2026-08-27. [W6]
- Insider One Academy. Architect Feature Set. https://academy.insiderone.com/docs/architect-feature-set.md , 2026-02-12. [W7]
- Insider One Academy. Architect Terms to Know. https://academy.insiderone.com/docs/architect-terms-to-know.md , 2025-11-14. [W8]
- Insider One Academy. Unified Customer Database (UCD). https://academy.insiderone.com/docs/unified-customer-database-ucd.md , 2026-08-28; https://academy.insiderone.com/docs/default-events-attributes ; https://academy.insiderone.com/v1/docs/how-identifiers-work-in-insider-one . [W9]
- Insider One Academy. Liquid Tags. https://academy.insiderone.com/docs/liquid-tags.md , 2026-10-20; https://academy.insiderone.com/docs/liquid-in-web-templates.md . [W10]
- Insider One Academy. Smart Recommender Algorithms. https://academy.insiderone.com/docs/smart-recommender-algorithms.md , 2026-10-26; https://insiderone.com/smart-recommender-similarity-engine/ ; https://academy.insiderone.com/docs/bring-your-own-recommendation . [W11]
- Insider One Academy. Architect Send Time Optimization. https://academy.insiderone.com/docs/architect-send-time-optimization.md , 2026-08-28. [W12]
- Insider One Academy. Predictive Segments. https://academy.insiderone.com/docs/likelihood-to-churn , https://academy.insiderone.com/docs/predictive-segments-user-engagement.md , https://academy.insiderone.com/docs/use-cases-for-predictive-segments-1 , 2026-08-27. [W13]
- Insider One Academy. On Price Drop. https://academy.insiderone.com/docs/on-price-drop , https://academy.insiderone.com/docs/architect-use-case-price-drop.md , https://academy.insiderone.com/docs/create-a-price-drop-web-push.md , 2026-09-03. [W14]
- Insider One. Case Studies(목록·Samsung·adidas). https://insiderone.com/case-studies/ , https://insiderone.com/case-studies/samsung/ , https://insiderone.com/case-studies/adidas/ , 날짜 미표기 — 2026-11 조회. [W15]
- PR Newswire. Insider launches WhatsApp Commerce. https://www.prnewswire.co.uk/news-releases/insider-launches-whatsapp-commerce-to-help-brands-deliver-end-to-end-buying-experiences-and-becomes-a-meta-business-solution-provider-bsp-301777122.html , 2023-03-21; tech.eu. https://tech.eu/2023/01/10/insider-picks-up-meta-certified-conversational-commerce-tool-mindbehind/ , 2023-01-10; casestudies.com. Clarins. https://www.casestudies.com/company/insider-one/case-study/clarins-boosts-whatsapp-sales-20x-with-insider . [W16]
- Insider One. Gartner MQ 2026 Personalization Engines / Peer Insights. https://insiderone.com/es/gartner-magic-quadrant-2026-personalization-engines/ , https://insiderone.com/fr/insider-one-nomme-leader-dans-le-magic-quadrant-2026-de-gartner-pour-les-moteurs-de-personnalisation/ , https://insiderone.com/es/news/es-insider-one-ha-sido-reconocida-en-2026-como-la-eleccion-de-los-clientes-de-gartner-peer-insights-para-centros-de-marketing-multicanal/ , 2026. [W17]
- Braze. 국내 데이터센터 오픈·카카오톡 채널 출시. https://www.braze.com/ko/press-releases/korea-data-center-kakaotalk-launch , 2026-04-08; 벤처스퀘어(한혜선) https://www.venturesquare.net/1074738/ ; 뉴스와이어 https://www.newswire.co.kr/newsRead.php?no=1031969 . [W18]
- Braze. 카카오톡 지원. https://www.braze.com/ko/resources/articles/braze-kakaotalk-support , 2026-04-07. [W19]
- Braze Docs. Set up KakaoTalk. https://www.braze.com/docs/user_guide/message_building_by_channel/kakaotalk/kakaotalk_setup , 날짜 미표기(© 2026) — 2026-11 조회. [W20]
- Braze Docs. User profile lifecycle / Custom events. https://www.braze.com/docs/user_guide/data/user_data_collection/user_profile_lifecycle , https://www.braze.com/docs/user_guide/data/custom_data/custom_events , 2026-11 조회. [W21]
- Braze Docs. Canvas. https://www.braze.com/docs/user_guide/engagement_tools/canvas , 2026-11 조회. [W22]
- Braze Docs. Liquid. https://www.braze.com/docs/user_guide/personalization_and_dynamic_content/liquid , 2026-11 조회. Liquid FAQ: https://braze.com/docs/user_guide/messaging/design_and_edit/personalize/liquid/faq . [W23, C-패턴4]
- Braze Docs. BrazeAI. https://www.braze.com/docs/user_guide/brazeai , 2026-11 조회. Business Wire. Sage AI by Braze. https://www.businesswire.com/news/home/20230627094460/en , 2023-06-27; https://www.braze.com/ja/resources/articles/sage-ai-by-braze-announcement (2024-07 업데이트). [W24]
- Braze Docs. Intelligent Timing / Intelligent Channel / Intelligent Selection. https://www.braze.com/docs/user_guide/brazeai/intelligence/intelligent_timing , https://www.braze.com/docs/user_guide/brazeai/intelligence/intelligent_channel , https://braze.com/docs/user_guide/brazeai/intelligence/intelligent_selection , 2026-11 조회. [W25]
- Braze Docs. Predictive Churn / Predictive Suite. https://www.braze.com/docs/user_guide/brazeai/predictive_suite/predictive_churn , https://www.braze.com/docs/user_guide/brazeai/predictive_suite , 2026-11 조회. [W26]
- Braze Docs. Currents. https://www.braze.com/docs/user_guide/data/braze_currents , 2026-11 조회. [W27]
- Braze Docs. Channels. https://braze.com/docs/user_guide/channels , https://www.braze.com/docs/es/user_guide/get_started/campaigns_and_canvases/ , 2026-11 조회; Release notes https://www.braze.com/docs/releases/2025/5_27_25 , 2025-05-27. [W28]
- Braze Docs. Price drop / Back in stock notifications. https://braze.com/docs/user_guide/data/activation/catalogs/catalog_triggers/price_drop_notifications/ , https://braze.com/docs/user_guide/data/activation/catalogs/catalog_triggers/back_in_stock_notifications , 2026-11 조회. [W29]
- Braze. 잡코리아 고객 사례. https://www.braze.com/ko/customers/jobkorea-case-study , 날짜 미표기(통계 2023-07 기준). [W30]
- Braze. BlaBlaCar case study. https://www.braze.com/customers/blablacar-case-study-abandoned-cart , 날짜 미표기. [W31]
- Braze. 2025 연간 리뷰. https://www.braze.com/ko/resources/articles/braze-2025-year-in-review , 2025-12-17; OfferFit 인수 완료 https://www.braze.com/press-releases/braze-completes-acquisition-of-offerfit , 2025-06-02. [W32]
- Braze. 2025 Gartner MQ MMH Leader. https://www.braze.com/press-releases/braze-named-a-leader-in-2025-gartner-magic-quadrant-for-multichannel-marketing-hubs-for-third-consecutive-year- , 2025-09; IT Brief Australia. https://itbrief.com.au/story/braze-named-gartner-leader-for-fourth-straight-year , 2026-09-25; https://www.braze.com/resources/reports-and-guides/gartner-magic-quadrant-mmh-2026 . [W33]
- 벤처스퀘어. 브레이즈 커넥션 서울 2024. https://www.venturesquare.net/945620 , 2024-11-06. 인프런 Braze 강의 https://www.inflearn.com/course/crm-마케팅-브레이즈 . [W34]
- Braze. Certification / Practitioner path / Abandoned cart course. https://braze.com/docs/user_guide/administer/personal/braze_certification , https://lab.braze.com/path/braze-practitioner , https://learning.braze.com/build-an-abandoned-cart-user-journey , 2026-11 조회. [W35]

### 6.2 논문·학술
- Lemon, K. N., & Verhoef, P. C. Understanding Customer Experience Throughout the Customer Journey. Journal of Marketing, 80(6), 69–96. DOI 10.1509/jm.15.0420, 2016. [P-A1]
- Rust, R. T., Lemon, K. N., & Zeithaml, V. A. Return on Marketing: Using Customer Equity to Focus Marketing Strategy. Journal of Marketing, 68(1), 109–127. DOI 10.1509/jmkg.68.1.109.24030, 2004. [P-A2]
- Reichheld, F. F., & Sasser, W. E. Jr. Zero Defections: Quality Comes to Services. Harvard Business Review, 1990년 9–10월호, pp.105–111 (권호 68(5) 미확인, DOI 없음). [P-주의]
- Fader, P. S., Hardie, B. G. S., & Lee, K. L. RFM and CLV: Using Iso-Value Curves for Customer Base Analysis. Journal of Marketing Research, 42(4), 415–430. DOI 10.1509/jmkr.2005.42.4.415, 2005. [P-B1]
- Fader, P. S., Hardie, B. G. S., & Lee, K. L. "Counting Your Customers" the Easy Way: An Alternative to the Pareto/NBD Model. Marketing Science, 24(2), 275–284. DOI 10.1287/mksc.1040.0098, 2005. [P-B2]
- Schmittlein, D. C., Morrison, D. G., & Colombo, R. Counting Your Customers: Who Are They and What Will They Do Next? Management Science, 33(1), 1–24. DOI 10.1287/mnsc.33.1.1, 1987. [P-B3]
- Gupta, S., Hanssens, D., Hardie, B., Kahn, W., Kumar, V., Lin, N., Ravishanker, N., & Sriram, S. Modeling Customer Lifetime Value. Journal of Service Research, 9(2), 139–155. DOI 10.1177/1094670506293810, 2006. [P-B4]
- Neslin, S. A., Gupta, S., Kamakura, W., Lu, J., & Mason, C. H. Defection Detection. Journal of Marketing Research, 43(2), 204–211. DOI 10.1509/jmkr.43.2.204, 2006. [P-C1]
- Ascarza, E. Retention Futility: Targeting High-Risk Customers Might Be Ineffective. Journal of Marketing Research, 55(1), 80–98. DOI 10.1509/jmr.16.0163, 2018. [P-C2]
- Lemmens, A., & Gupta, S. Managing Churn to Maximize Profits. Marketing Science, 39(5), 956–973. DOI 10.1287/mksc.2020.1229, 2020. [P-C3]
- Gutierrez, P., & Gérardy, J.-Y. Causal Inference and Uplift Modelling: A Review of the Literature. PMLR 67, 1–13. https://proceedings.mlr.press/v67/gutierrez17a.html , 2017. [P-D1]
- Devriendt, F., Moldovan, D., & Verbeke, W. A Literature Survey and Experimental Evaluation of the State-of-the-Art in Uplift Modeling. Big Data, 6(1), 13–41. DOI 10.1089/big.2017.0104, 2018. [P-D2]
- (저자 미확인). Uplift Modeling: From Causal Inference to Personalization. CIKM 2023 튜토리얼. DOI 10.1145/3583780.3615298 / arXiv 2308.09066, 2023. [P-D3]
- Lewis, R. A., & Rao, J. M. The Unfavorable Economics of Measuring the Returns to Advertising. The Quarterly Journal of Economics, 130(4), 1941–1973. DOI 10.1093/qje/qjv023, 2015. [P-D4]
- Johnson, G. A., Lewis, R. A., & Nubbemeyer, E. I. Ghost Ads. Journal of Marketing Research, 54(6), 867–884. DOI 10.1509/jmr.15.0297, 2017. [P-D5]
- Gordon, B. R., Moakler, R., & Zettelmeyer, F. Close Enough? A Large-Scale Exploration of Non-Experimental Approaches to Advertising Measurement. Marketing Science, 42(4), 768–793. DOI 10.1287/mksc.2022.1413 / arXiv 2201.07055, 2023. [P-D6]
- Kohavi, R., Longbotham, R., Sommerfield, D., & Henne, R. M. Controlled Experiments on the Web: Survey and Practical Guide. Data Mining and Knowledge Discovery, 18(1), 140–181. DOI 10.1007/s10618-008-0114-1, 2009. [P-E1]
- Kohavi, R., Tang, D., & Xu, Y. Trustworthy Online Controlled Experiments. Cambridge University Press. DOI 10.1017/9781108653985, 2020. [P-E2]
- Fabijan, A., Gupchup, J., Gupta, S., Omhover, J., Qin, W., Vermeer, L., & Dmitriev, P. Diagnosing Sample Ratio Mismatch in Online Controlled Experiments. KDD '19, 2156–2164. DOI 10.1145/3292500.3330722, 2019. [P-E3]
- Johari, R., Koomen, P., Pekelis, L., & Walsh, D. Always Valid Inference: Continuous Monitoring of A/B Tests. Operations Research, 70(3), 1806–1821. DOI 10.1287/opre.2021.2135, 2022. [P-E4]
- Kohavi, R., Deng, A., & Vermeer, L. A/B Testing Intuition Busters. KDD '22, 3168–3177. DOI 10.1145/3534678.3539160, 2022. [P-E5]
- Singh, H., Sinha, M., Sinha, A. R., Garg, S., & Banerjee, N. An RNN-Survival Model to Decide Email Send Times. arXiv 2004.09900, 2020. [P-F1]
- Bidargaddi, N., Almirall, D., Murphy, S., Nahum-Shani, I., Kovalcik, M., Pituch, T., Maaieh, H., & Strecher, V. To Prompt or Not to Prompt? JMIR mHealth and uHealth, 6(11), e10123. DOI 10.2196/10123, 2018. [P-F2]
- Pielot, M., Church, K., & de Oliveira, R. An In-Situ Study of Mobile Phone Notifications. MobileHCI '14, 233–242. DOI 10.1145/2628363.2628364, 2014. [P-F3]
- Sahami Shirazi, A., Henze, N., Dingler, T., Pielot, M., Weber, D., & Schmidt, A. Large-Scale Assessment of Mobile Notifications. CHI '14, 3055–3064. DOI 10.1145/2556288.2557189, 2014. [P-F4]
- Mehrotra, A., Pejovic, V., Vermeulen, J., Hendley, R., & Musolesi, M. My Phone and Me. CHI '16, 1021–1032. DOI 10.1145/2858036.2858566, 2016. [P-F5]
- Kim, Kim, & Choi (given name 미확인). Push the Paw: A Field Experiment on Personalised Push Notifications and User Engagement. Australasian Marketing Journal, 34(1), 76–85. DOI 10.1177/14413582251356702 (SSRN 10.2139/ssrn.4993370), 온라인 2025-07. [P-F6]
- Sahni, N. S., Wheeler, S. C., & Chintagunta, P. Personalization in Email Marketing: The Role of Noninformative Advertising Content. Marketing Science, 37(2), 236–258. DOI 10.1287/mksc.2017.1066, 2018. 반례: Marketing Letters 34(4), DOI 10.1007/s11002-023-09701-7, 2023 (제목·저자 미확인). [P-G1]
- Wang, Lu, & Shi (given name 미확인). Does Customer Email Engagement Improve Profitability? Manufacturing & Service Operations Management, 24(5), 2703–2721. DOI 10.1287/msom.2022.1122, 2022. [P-G2]
- Kumar, V., Zhang, X., & Luo, A. Modeling Customer Opt-In and Opt-Out in a Permission-Based Marketing Context. Journal of Marketing Research, 51(4), 403–419. DOI 10.1509/jmr.13.0169, 2014. [P-G3]
- Linden, G., Smith, B., & York, J. Amazon.com Recommendations: Item-to-Item Collaborative Filtering. IEEE Internet Computing, 7(1), 76–80. DOI 10.1109/MIC.2003.1167344, 2003. [P-H1]
- Gomez-Uribe, C. A., & Hunt, N. The Netflix Recommender System. ACM TMIS, 6(4), 1–19. DOI 10.1145/2843948, 2015. [P-H2]
- Jannach, D., & Jugovac, M. Measuring the Business Value of Recommender Systems. ACM TMIS, 10(4), 1–23. DOI 10.1145/3370082 / arXiv 1908.08328, 2019. [P-H3]
- Li, L., Chu, W., Langford, J., & Schapire, R. E. A Contextual-Bandit Approach to Personalized News Article Recommendation. WWW '10, 661–670. DOI 10.1145/1772690.1772758 / arXiv 1003.0146, 2010. [P-I1]
- Scott, S. L. Multi-Armed Bandit Experiments in the Online Service Economy. Applied Stochastic Models in Business and Industry, 31(1), 37–45. DOI 10.1002/asmb.2104, 2015. [P-I2]
- Schwartz, E. M., Bradlow, E. T., & Fader, P. S. Customer Acquisition via Display Advertising Using Multi-Armed Bandit Experiments. Marketing Science, 36(4), 500–522. DOI 10.1287/mksc.2016.1023, 2017. [P-I3]
- Verhoef, P. C., Kannan, P. K., & Inman, J. J. From Multi-Channel Retailing to Omni-Channel Retailing. Journal of Retailing, 91(2), 174–181. DOI 10.1016/j.jretai.2015.02.005, 2015. [P-J1]
- Neslin, S. A., Grewal, D., Leghorn, R., Shankar, V., Teerling, M. L., Thomas, J. S., & Verhoef, P. C. Challenges and Opportunities in Multichannel Customer Management. Journal of Service Research, 9(2), 95–112. DOI 10.1177/1094670506293559 (Crossref 조회 미실시), 2006. [P-J2]
- Kumar, V., & Venkatesan, R. Who Are the Multichannel Shoppers and How Do They Perform? Journal of Interactive Marketing, 19(2), 44–62. DOI 10.1002/dir.20034, 2005. [P-J3]
- Montaguti, E., Neslin, S. A., & Valentini, S. Can Marketing Campaigns Induce Multichannel Buying and More Profitable Customers? Marketing Science, 35(2), 201–217. DOI 10.1287/mksc.2015.0923, 2016. [P-J4]
- Goldfarb, A., & Tucker, C. E. Privacy Regulation and Online Advertising. Management Science, 57(1), 57–71. DOI 10.1287/mnsc.1100.1246, 2011. [P-K1]
- Aridor, G., Che, Y.-K., & Salz, T. The Effect of Privacy Regulation on the Data Industry: Empirical Evidence from GDPR. The RAND Journal of Economics, 54(4), 695–730. DOI 10.1111/1756-2171.12455, 2023 (NBER WP 26900, 2020). [P-K2]
- Johnson, G. A., Shriver, S. K., & Goldberg, S. G. Privacy and Market Concentration. Management Science, 69(10), 5695–5721. DOI 10.1287/mnsc.2023.4709, 2023. [P-K3]
- Utz, C., Degeling, M., Fahl, S., Schaub, F., & Holz, T. (Un)informed Consent: Studying GDPR Consent Notices in the Field. CCS '19, 973–990. DOI 10.1145/3319535.3354212 / arXiv 1909.02638, 2019. [P-K4]

### 6.3 커뮤니티·실무
- AWS Marketplace. Braze 리뷰 목록. https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-mizcm7d44hr2s?page=9 (page=32, page=51), 2026-10 작성분.
- AWS Marketplace. Insider One 리뷰 목록(G2·Gartner·PeerSpot 신디케이션). https://aws.amazon.com/marketplace/reviews/reviews-list/prodview-dc6vbfqmn2y3y?page=97 , 2026-09~10 작성분.
- Capterra. Braze(Appboy) 리뷰. https://www.capterra.com/p/155423/Appboy/reviews?page=2 , https://capterra.com/p/155423/Appboy/reviews/ [스니펫].
- G2. Insider 리뷰 https://g2.com/products/insider/reviews?page=4 , https://www.g2.com/survey_responses/insider-review-5133670 ; Braze 리뷰 https://www.g2.com/survey_responses/braze-review-3176630 ; 비교 https://www.g2.com/compare/braze-vs-insider-vs-iterable [스니펫].
- TrustRadius. Braze 리뷰. https://trustradius.com/reviews/braze-2024-04-12-09-11-34 [스니펫].
- Gartner Peer Insights. Insider One. https://www.gartner.com/reviews/market/multichannel-marketing-hubs/vendor/insider-one [스니펫].
- CleverTap. Braze vs Insider. https://clevertap.com/blog/braze-vs-insider/ (경쟁사, 편향) [스니펫].
- Braze Bonfire. Using Liquid to identify users in a segment. https://community.braze.com/discussions/orchestration/using-liquid-to-identify-users-in-a-segment/4812/replies/4813 [스니펫].
- Braze 블로그. Don't bury customers in notifications. https://www.braze.com/resources/articles/dont-bury-customers-notifications.md [스니펫].
- Airship. https://www.airship.com/?p=28399 , 2026-08 [스니펫].
- The Grow Getter. Why are high-growth scaleups going…. https://thegrowthspurt98.beehiiv.com/p/why-are-high-growth-scaleups-going , 2023-11-10.
- Phiture (Alejandra Escobal). How to deploy Liquid code in CRM. https://phiture.com/mobilegrowthstack/how-to-deploy-liquid-code-crm/ , 2023-06-20.
- Mavlers. BrazeAI Liquid Assistant. https://www.mavlers.com/blog/brazeai-liquid-assistant-lifecycle-marketing/ (에이전시, 이해관계).
- Fivetran. Data API costs Braze. https://www.fivetran.com/blog/data-api-costs-braze-fivetran-activations (연동 벤더, 이해관계) [스니펫].
- Monzo (Rodrigo Baptista). Beyond the last click: how Monzo measures CRM's true impact. https://monzo.com/blog/beyond-the-last-click-how-monzo-measures-crms-true-impact , 2025-09-03.
- datainterview. CRM lifecycle experiments. https://www.datainterview.com/courses/marketing-ads-analytics/crm-lifecycle-experiments [스니펫].
- Braze. KakaoStyle case study. https://www-origin.braze.com/customers/kakaostyle-case-study , 게재일 미표기.
- Insider. Lenovo Korean Case Study. https://useinsider.com/assets/media/2023/10/Lenovo-Korean-Case-Study.pdf , 2023-10 [스니펫]. Insider 한국어 고객 페이지 https://insiderone.com/ko/customers/ .
- 벤처스퀘어. Braze 카카오톡 채널·데이터센터. https://www.venturesquare.net/fr/1074745/ , 2026-04-08.
- 바이라인네트워크. 마티니 아이오 3년만에 300억 매출. https://byline.network/2025/12/4-374/ , 2025-12-04.
- 고구마팜 (갱언니). CRM 마케팅의 기본 공식 feat. 푸시 메시지. https://gogumafarm.kr/crm-마케팅의-기본-공식-feat-푸시-메시지/ , 2022-04-25.
- 이오플래닛 (헨리퀀). https://eopla.net/magazines/1248 , 2022-06-16.
- 아이보스. 이벤트 택소노미 글 https://www.i-boss.co.kr/ab-6141-68205 ; 실무 요약 https://www.i-boss.co.kr/ab-6141-67309&PB_1499924161=33 [스니펫]; 채용 https://www.i-boss.co.kr/ab-2795-7339 .
- 디지털인사이트 (마티니 아이오 기고). https://ditoday.com/?p=82062 (Braze 리셀러, 이해관계).
- 리멤버 채용. https://career.rememberapp.co.kr/job/posting/324537 .
- 인프런. CRM 마케팅 브레이즈 강의 https://www.inflearn.com/course/crm-마케팅-브레이즈?cid=329457 ; 수강평 https://www.inflearn.com/community/reviews/105541 , 2022-11-12.
- 패스트캠퍼스. AI CRM 완전 정복(w. Braze & Claude Code). https://fastcampus.co.kr/mktg_online_AiBraze .
- 코멘토. Braze를 활용한 CRM 마케팅 개인화. https://comento.kr/class/pt/content/braze를-활용한-crm-마케팅-개인화/76 .

---

## 7. 리서치 한계

**커버하지 못한 영역**
- **카카오 알림톡·브랜드 메시지**: Braze 공식 자료는 친구톡만 명시, KakaoTalk "Create message" 문서 URL 404. Insider One의 카카오톡 지원은 어떤 1차 자료에서도 확인 못함 → 본문 단정 금지, 운영자/벤더 확인 필요 (X1, X2).
- **한국 법규(정보통신망법·개인정보보호법)**: 1차 법령·KISA 자료 미수집, 학술 논문도 범위 밖. 현장 언급(야간 발송·수신 동의)만 있음 → 법규 서술이 필요하면 추가 리서치 필수 (X17).
- **가격**: 두 제품 모두 비공개·견적 기반. 데이터 포인트·메시지 크레딧 과금 구조는 커뮤니티 불만으로만 확인. Braze Currents 가격은 "담당 AM 문의".
- **한국 고객 사례 수치**: Braze는 잡코리아 1건(+카카오스타일 벤더 게재 1건)만 수치 확보, 네이버웹툰은 수치 없음. Insider는 삼성(글로벌, 한국 시장 미특정) 외 한국 고객(대한항공·롯데호텔·GS샵·현대캐피탈)의 공개 사례·수치 없음, 레노버 코리아는 스니펫만.
- **Insider 한국어 소스 빈약**: 한국어 독립 후기 사실상 0건, 영어 리뷰(AWS 집계)와 벤더 사례 의존. 전체적으로 Braze 쪽 자료가 훨씬 많아 두 제품의 서술 밀도가 비대칭이 될 위험.
- **학술 근거가 얇은 영역**: 무작위 실험으로 검증된 개인별 STO 논문 없음, 이커머스 앱 마케팅 푸시의 대규모 무작위 실험 논문 없음(헬스 앱·반려동물 앱뿐).
- **미확인 수치(재확인 필요)**: Insider UCD 속성 상한 200/기본 120, SMS 예측 최소 데이터, Braze Liquid 기본값 문법, Canvas 진입 방식 상세, Predictive Churn 최소 데이터 요건, OfferFit 인수가($325M), Braze Operator·Agent Console의 현재 GA 여부.

**접근 실패**
- **Reddit**(r/marketing, r/emailmarketing, r/ProductManagement) WebFetch 차단, 검색 엔진도 스레드 미반환 → 원문 토론 0건. LinkedIn 미접근.
- G2·Capterra·TrustRadius 개별 페이지 403 → 검색 스니펫과 AWS Marketplace 신디케이션으로 대체.
- Braze Bonfire 스레드 본문 렌더 실패(스니펫 1건). 브런치·velog·요즘IT·커리어리에서 Braze/Insider 도입기 미발견.
- academy.insiderone.com 검색 페이지 404, Gartner MQ 원문(유료) 미열람.
- 다수 논문(JMR·Marketing Science·HBR 등) 유료 — 수치는 abstract 또는 2차 출처로 확인, 등급 표시. 일부 저자 given name 미확인(D3, F6, G2, G1 반례).

**편향·이해관계 소스**: 마티니 아이오(Braze 리셀러), Mavlers(Braze 에이전시), CleverTap·Insider 비교 글(경쟁사), Fivetran·RudderStack(연동 벤더), Airship(벤더), 강의 판매 페이지. 해당 항목에 표기함.

**피인용수**: Crossref 기준이라 Google Scholar보다 크게 낮음 — "피인용 수천 회" 같은 표현을 쓰려면 Scholar 수치 별도 확인.

**보강 권고(원 리서처)**: 운영자 계정으로 Reddit·LinkedIn·커리어리 직접 검색, Braze Bonfire 원문 확보, Insider 한국 지사 사례집 확보, 카카오 알림톡 지원 여부를 양 벤더에 직접 확인.

**실패한 리서처**: 없음(web·paper·community 3종 모두 산출).

---

## 신선도 원장

| 원천 | 발행일 / 버전 시점 | 검색·조회 시점 | 비고 |
|---|---|---|---|
| research/web.md 전체 | — | 2026-11-03 | 본문 "2026-11 기준" 고정 |
| research/papers.md 전체 | 피인용수 Crossref 2026-11-03 조회 | 2026-11-03 | |
| research/community.md 전체 | — | 2026-11-03 | AWS 리뷰 2026-09~10 최신, 한국 실무 글 2022년 다수 |
| W1 Insider One 리브랜딩 | 2025-12-09 (목록 2025-12-08) | 2026-11 | 수치 2025-12 기준 |
| W2 Insider 한국어 플랫폼 | 날짜 미표기 | 2026-11 조회 | 1,500+ 고객 표기는 구시점 |
| W3 Insider 시리즈E·한국 투자 | 2024-11-01 | 2026-11 | 수치 2024-11 기준 |
| W4 Agent One 재출시 | 2026-09-17 (원 출시 2025-03, Sirius AI ~2023 미확인) | 2026-11 | |
| W5 Bluecore 인수 / OpenAI | 2026-05-13 / 2026-03(미확인) | 2026-11 | |
| W6 Architect 소개 | 2026-08-27 | 2026-11 | |
| W7 Architect Feature Set | 2026-02-12 | 2026-11 | |
| W8 Architect Terms | 2025-11-14 | 2026-11 | |
| W9 UCD | 2026-08-28 | 2026-11 | 속성 상한 수치는 스니펫 |
| W10 Insider Liquid | 2026-10-20 | 2026-11 | 얼리 액세스 상태 |
| W11 Smart Recommender | 2026-10-26 (구 문서 2024) | 2026-11 | 6그룹 |
| W12 Insider STO | 2026-08-28 | 2026-11 | |
| W13 Predictive Segments | 2026-08-27 | 2026-11 | |
| W14 On Price Drop | 2026-09-03 | 2026-11 | |
| W15 Insider 사례 | 날짜 미표기 (adidas ~2023-07 추정) | 2026-11 조회 | 구버전일 수 있음 |
| W16 WhatsApp Commerce | 2023-03-21 / 2023-01-10 | 2026-11 | 구버전일 수 있음 |
| W17 Insider Gartner | 2026 (MMH Visionary는 2025-06 자료) | 2026-11 | |
| W18 Braze 데이터센터·카카오톡 | 2026-04-08 | 2026-11 | 수치 2026-04 기준 |
| W19 Braze 카카오톡 블로그 | 2026-04-07 | 2026-11 | |
| W20 Set up KakaoTalk | 날짜 미표기(© 2026) | 2026-11 조회 | |
| W21~W29 Braze Docs | 날짜 미표기 | 2026-11 조회 | W28 릴리스노트 2025-05-27 |
| W24 BrazeAI 연혁 | Sage AI 2023-06-27, BrazeAI 표기 2024-07 | 2026-11 | |
| W30 잡코리아 | 날짜 미표기, 통계 2023-07, 캠페인 ~2023-11 | 2026-11 | 구버전일 수 있음 |
| W31 BlaBlaCar | 날짜 미표기(2022년 이후) | 2026-11 | |
| W32 Braze 2025 연간 리뷰 | 2025-12-17 / OfferFit 2025-06-02 | 2026-11 | |
| W33 Braze Gartner | 2025-09(보고서 2025-09-22) / 2026-09-25 | 2026-11 | |
| W34 브레이즈 커넥션 서울 | 2024-11-06 (행사 11-05) | 2026-11 | 수치 2024-11 기준 |
| W35 Braze 인증 | 날짜 미표기 (커뮤니티 답변 2023) | 2026-11 조회 | |
| P-A1~P-K4 | 1987~2025 (각 참고문헌 연도) | 2026-11-03 | P-F6 온라인 2025-07, P-F1 arXiv 2020 |
| C 커뮤니티 리뷰(AWS) | 2026-09-22~2026-10-31 | 2026-11-03 | |
| C Capterra/G2/TrustRadius | 미표기 (TrustRadius 2024-04-12, Gartner 3.0점 2024) | 2026-11-03 | 스니펫 |
| C Monzo | 2025-09-03 | 2026-11-03 | |
| C Grow Getter | 2023-11-10 | 2026-11-03 | |
| C Phiture | 2023-06-20 | 2026-11-03 | |
| C 고구마팜 / 이오플래닛 | 2022-04-25 / 2022-06-16 | 2026-11-03 | 구버전일 수 있음 |
| C 인프런 수강평 | 2022-11-12 | 2026-11-03 | |
| C Airship | 2026-08 | 2026-11-03 | 스니펫 |
| C 바이라인 마티니 | 2025-12-04 | 2026-11-03 | |
| C 레노버 코리아 PDF | 2023-10 | 2026-11-03 | 스니펫 |
| C 카카오스타일 | 게재일 미표기 | 2026-11-03 | |
