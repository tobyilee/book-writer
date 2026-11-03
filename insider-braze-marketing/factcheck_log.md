## 01장 (라운드 1)

### ❌ 정정
- "두 회사 모두 2025년부터 2026년 사이에 사명, AI 기능 이름, 문서 주소를 여러 번 바꿨다" → "Insider One은 사명을 바꿨고, 두 회사 모두 AI 기능 이름과 문서 주소를…" — Braze는 사명 변경 없음(Sage AI→BrazeAI, /sage_ai/→/brazeai/만 해당). 근거: 01_reference.md 0절·1.3
- "2026년 11월 기준 공개 자료로 확인되는 것은 친구톡뿐이다" → "채널을 친구로 추가한 고객에게 보내는 마케팅 메시지(Braze가 '친구톡'이라고 부르는 것)뿐이다" — 근거: research/korea-compliance.md 자료 4-1 ("support for KakaoTalk marketing messages", "can only message friends of the channel"), 4장과 표현 통일
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — 수치는 모두 시점 명기됨)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: Lemon & Verhoef(2016) 접점 4분류명 brand-owned·partner-owned·customer-owned·social/external — 웹 2차 확인(AMA 2021 Sheth 수상 소개, 다수 2차 문헌 일치). 원고에 원어 분류명 병기. 구매 전·구매·구매 후 3단계 일치(papers.md P-A1)
- 인용 5건(이오플래닛 2건+"why, what, how", Cilingir, 인프런, 채용 공고 문구, 리뷰 3건 날짜 2026-10) — community.md·reference 1.1/4절 일치
- 수치·날짜 12건(Insider One 리브랜딩 2025-12-09, 6개 모듈, 100+ 소스, 2,000+/1,500+ 시점, Gartner PE Leader 5회째·MMH Visionary 2025-06, Braze MMH 4년 연속, MAU 78억·3조 9천억 건 2026-04, 2026-04-08 데이터센터, AB180 2017, 시리즈E·1,500억 원·2027, 한국 고객사) — reference 1.1·1.2 일치
- 표 1 두 도구 대표 이름 — reference 1.3·2.x 일치
### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- Insider 속성 상한 `(사실 확인 필요)` 해소(X12): "문서 버전마다 다르게 나타난다" → "2026년 11월 Academy 문서 기준 UCD 속성 합계 200개(기본 120·커스텀 80), 커스텀 증설 요청 가능, 커스텀 이벤트 종류 무제한·커스텀 이벤트 파라미터 80개, 계정별 상이" — 웹 2차: academy.insiderone.com/docs/attributes-events-guide (구 useinsider 2024-02 문서의 180개는 구버전)
- identifiers `(검색 요약 기준, 사실 확인 필요)` 해소 → "(2026-11 Academy 문서 기준)" — 웹 2차: academy.insiderone.com "How Identifiers Work in Insider One"(identifiers 버킷만 identity resolution에 사용; 기본 식별자 email·phone·UUID)
- 커스텀 이벤트·속성의 월 데이터 포인트 영향 "(검색 요약 기준)" → "(2026-11 기준)" — Academy Attributes and Events 문서로 재확인
### ✅ 확인 (요약)
- Braze 문서 인용 5건(user profile, external_id, anonymous user, "Not all data is merged", custom events 정의) — reference 2.1 일치
- 이벤트 속성 용도, 시계열 불필요 시 커스텀 속성 권고, 고정 상한 없음, Cloud Data Ingestion·Currents — reference 2.1·2.9 일치
- 리뷰 인용 4건(billing, data usage(Fivetran 인용·이해관계 표기), Insider 금융업·Victor Adolfo G., Braze Sung N.) 및 날짜 범위 2026-09~10 — community.md 일치
- 아이보스 이벤트 택소노미 인용 — reference 2.1 일치
### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- "활성 상태로 둘 수 있는 예측은 최대 3개" → 개요 페이지 3개 vs 예측 생성 페이지 "five concurrently active churn predictions" 불일치를 병기하고 계약 조건 확인 권고 — 웹 2차: braze.com/docs/…/predictive_churn/ (3개), …/creating_a_churn_prediction/ (5개, 구매 전 preview 1개)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- Predictive Churn 최소 데이터 `(사실 확인 필요)` 해소 → "고정 수치는 공개되어 있지 않고, 이탈 정의를 입력하면 대시보드가 필요한 과거 이탈자·비이탈자 최소 인원을 보여 준다" — 웹 2차: creating_a_churn_prediction ("Braze must have this minimum count of users available in historical data")
- Likelihood to Purchase 7일 `(사실 확인 필요)` 해소 → "점수가 모델 기준선을 넘은 사용자는 향후 7일 안에 구매할 것으로 본다" — 웹 2차: academy.insiderone.com/docs/predictive-segments-likelihood-to-purchase ("expected to make a purchase within the next seven days")
- Attribute Affinity `(세부 정의는 사실 확인 필요)` 해소 → "지난 30일 상품 상호작용 기반, 브랜드·카테고리·색상 같은 속성 선호" — 웹 2차: academy.insiderone.com/v1/docs/attribute-affinity
- Discount Affinity "이름대로라면" 추정 → 문서 정의(할인 시 구매 가능성 높은 사용자, 최근 6개월 데이터, 이커머스 전용)로 교체 — 웹 2차: Academy Predictive Segments FAQ·Discount Affinity 문서
### ✅ 확인 (요약)
- 고구마팜 인용(2022), 아이보스 "적정한 모수" — community.md 일치
- Architect reachability 체크, Condition 정의 — reference 2.4 일치
- Fader·Hardie·Lee(2005) iso-value curve, CLV 단순화, Neslin 2006(2차 출처 표기 유지) — papers.md·reference 1.4/2.2 일치
- Predictive Suite 인용·0~100 점수·정확도 보고, Predictive Segments 5유형(2026-08), churn 전용 유형 없음 — reference 2.2 일치
- 리뷰 인용 2건(2026-10) — community.md 일치
### 미해소
- (없음)

## 04장 (라운드 1)

### ❌ 정정
- Insider One 카카오톡: "공식 페이지와 Academy 문서 어디에서도 카카오톡 지원을 확인하지 못했다… 1차 자료는 없다" → "네이티브 채널은 미확인, Academy의 Call an API 사용 사례 문서가 Architect에서 카카오톡 메시지를 보내는 커스텀 연동을 소개(문서는 'AlimTalk API'라 부르나 예시 엔드포인트는 친구에게 보내기 API 형태 → 알림톡 지원으로 볼 수 없음)" — 근거: research/korea-compliance.md 자료 4-2
- 표 1 Insider One 친구톡 칸 → "네이티브 채널은 확인되지 않음 — Call an API 커스텀 연동 사례만 문서화"; Braze 행 이름 "친구톡" → "채널 친구 대상 마케팅 메시지(친구톡)"; 브랜드 메시지 Braze 칸 → "확인되지 않음 — 현재는 채널 친구만 가능" — 근거: korea-compliance.md 4-1·4-2
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- Braze 알림톡·브랜드 메시지 문단 보강: 발표 글 "KakaoTalk marketing messages", 문서 "For now, KakaoTalk can only message friends of the channel." 인용 추가, 카카오 브랜드 메시지 출시(2025-05)·친구톡 2025년 말 종료(대행사 안내 기준, 카카오 공식 공지 미확인)·Braze 설정의 브랜드 메시지 API 자격 증명(발송 경로 문서 미명시) 명기 — 근거: korea-compliance.md 3-3·3-5·4-1
- 표 2 "친구톡(Braze, 2026-11 기준)" → "카카오톡 채널 친구 대상 메시지(Braze, 2026-11 기준)" — 친구톡 상품 종료 표기와의 충돌 회피
- RCS `(사실 확인 필요)` 해소 → "기본 메시지 앱 안에서 고화질 이미지·버튼·인증된 브랜드 발신자 프로필 같은 풍부한 형식(Braze 문서 기준)" — 웹 2차: braze.com/docs/…/sms_mms_rcs/rcs
### ✅ 확인 (요약)
- 플러스친구 `(사실 확인 필요)` 해소: 플러스친구 → 카카오톡 채널(중간 명칭 '톡채널') 개명 확인 — 웹 2차(아이보스 보도·실무 블로그), 마커만 삭제
- Bidargaddi et al.(2018) 설정·수치(상용 직장 웰빙 앱 JOOL, 사용자 1,255명·89일, 하루 6개 시각 중 하나 50:50 무작위화, 3.9%, 주말 8.7%·주중 2.5%, P=.18) — 웹 2차: PMC6293241 초록 원문과 일치 ("직장인 웰빙 앱" 유지)
- Pielot·Church·de Oliveira 2014(15명·1주·일기·63.5개), Mehrotra 2016(2차 출처 표기 유지) — papers.md 일치
- Braze 채널 목록·Banners/RCS 2025-05 GA·애드온(스페인어판)·2025 연간 리뷰 채널, The Grow Getter(2023) — reference 2.3 일치
- Insider 채널(2025-12 보도자료·한국어 페이지·Architect 2026-02), MindBehind 2023-01·WhatsApp Commerce 2023-03 — reference 2.3 일치
- Braze 카카오톡 4,900만(2026-04), 친구톡 블로그 인용·형식, 설정 요건·제약(CJ올리브네트웍스·Infobip, Sender Key 1워크스페이스, E.164, Infobip 고객센터 연락처) — reference 2.10·web.md 일치
- Quiet Hours / Silent hours, Promotional/Transactional, Airship(벤더 표기), "플러스친구와 LMS…" 인용(스니펫 표기) — reference 일치
### 미해소
- (없음)

## 05장 (라운드 1)

### ❌ 정정
- Send to Destination "여정 중의 정보를 외부 시스템으로 내보낸다" → "고객을 이 Canvas에서 다른 Canvas로 보낸다. 외부 API 호출 없이 Braze 안에서 여정끼리 잇는다" — 근거: Braze Docs Send to Destination step ("allows you to send users from one Canvas to another", 2026-11 조회)
- User Update 표 "잡코리아는 Canvas로 커스텀 속성을 실시간 갱신했다" → "잡코리아도 커스텀 속성 갱신에 Canvas를 활용했다" — 근거: 01_reference.md 3.1 (Canvas·실시간·CSV 갱신은 별개 수단)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (기존 "2026-11 기준" 표기 유지 — 컴포넌트 목록·Canvas Flow·Content Optimizer 베타)
### ✅ 확인 (요약)
- X24 진입 방식 3종(scheduled / action-based / API-triggered) — Braze Docs Create a Canvas로 확인, (사실 확인 필요) 해소, API 기반에 `/canvas/trigger/send` 한 줄 보강
- Decision Split(세그먼트·필터 조건, 예/아니오 두 갈래, 도착 시점 평가), Audience Paths(최대 8그룹, 첫 일치 경로 우선), Action Paths(기본 즉시 진행 / ranked order 켜면 기간 종료까지 보유) — Braze Docs 각 컴포넌트 문서로 확인, 마커 3건 해소·설명 보강
- Context("create and update one or more variables for a user as they move through a Canvas", 워크스페이스별 가용성), Feature Flag(여정 지점에서 플래그 부여) — Braze Docs로 확인, 마커 2건 해소
- 컴포넌트 13종 목록 — Braze Docs Canvas components 인덱스와 일치. Content Optimizer 베타 — Braze 2026 릴리스 노트·문서와 일치
- Canvas 정의 인용, Canvas Flow(2022) 기본 편집기, Intelligent Timing Message 단계 설정, BlaBlaCar Action Paths·Audience Sync, Braze Agents, 다변량 시작 후 변경 시 무효, 테스트·버전 히스토리·복제, 리뷰 인용 2건("feature-dense" 포함) — 01_reference.md·research/community.md와 일치
### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- Components "여러 Element를 묶어 다시 쓰는 단위로 보인다" → "진입 제한, 대조군, 여정 우선순위, 여정 편집, 테스트처럼 여정을 운영하는 설정과 도구를 모아 둔 문서 묶음" — 근거: Insider One Academy "Architect Journey Components" 인덱스(하위: Launch Settings, Journey Test, Journey Entry Capping, Control Group, Journey Prioritization, Edit Journeys 등)
- 번역표 "외부 시스템 호출 | Send to Destination 등" → "웹훅(Message 단계의 채널)" — 근거: Send to Destination은 Canvas 간 이동(Braze Docs), 외부 호출은 웹훅 채널(01_reference.md 5장 연동·BlaBlaCar 채널 목록)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (기존 문서 갱신일·"2026-11 기준" 표기 유지)
### ✅ 확인 (요약)
- Action Elements — Academy "Architect Action Elements": Update User Attribute, Update Static Segment. 마커 해소, Update Static Segment 한 구절 보강
- Terms to Know(2025-11-14): Trigger=Starter, Live Actions, Layer, Conversion Attribution Model, Sunset("closes the entrance gate… users already in the journey can proceed"), Promotional(opt-in 필요)/Transactional(opt-in 무시) — Academy 원문으로 확인
- Architect 소개(2026-08-27)·Feature Set(2026-02-12) 인용, 목차 계열, 채널 10종, 흐름 제어·리포트·테스트 목록, STO Dry Run 미동작, On Price Drop·Back in Stock — research/web.md 자료 6·7·8, 01_reference.md와 일치
- 리뷰 인용("already purchased items", "without asking engineers every time", 2024 3.0점 "steep initial learning curve", 2026-10 여행업 "steeper learning curve") — research/community.md·01_reference.md와 일치
### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- 기본값 서술: "정확한 문법은 원문 대조가 필요" → 확인된 문법으로 대체하되, Braze 문서의 "빈 값 종류에 따라 기본값이 나오지 않는 경우" 주의를 일반화된 문장으로만 반영(문서 내 blank 정의가 페이지 간 엇갈려 구체 규칙은 싣지 않음)
### 🕒 신선도
- (기존 "2026-11 기준" 표기 유지 — Braze Liquid GA, Insider Liquid 얼리 액세스)
### ✅ 확인 (요약)
- X25 Braze 기본값 문법 — Braze Docs "Setting default values": `{{ ${first_name} | default: 'Valued User' }}`. 본문에 `{{ ${first_name} | default: '고객' }}` 추가, 마커 해소
- 예시 4의 빈 값 비교 `{% if ${first_name} == blank %}` — Braze Docs Conditional logic 원문과 일치, 캡션의 확인 필요 문구 삭제
- Insider `{{ attribute.first_name }}` — Academy "Liquid in Web Templates" 원문으로 확인(같은 문서의 `| default: "Dear Customer"` 예도 추가). Liquid 태그 빌더 PII 미노출("Personally identifiable information is not listed there") 확인. 마커 2건 해소
- Insider Liquid Tags(2026-10-20) 얼리 액세스·지원 채널 목록 — Academy 원문과 일치
- Phiture(Alejandra Escobal, 2023-06-20) 인용 및 변수명 불일치(`order_ide`/`order_id`, `product_link`(JSON 페이로드)/`product_url`(Liquid), `favoriteProduct`/`favoriteProducts`) — 원문 확인, 마커 해소·전언형 삭제
- Braze Liquid 정의 인용·Liquid 5·신규 필터·100% 미지원 FAQ, Connected Content(BlaBlaCar), 잡코리아(속성 갱신·날짜 계산·카피·CTR 4~5배 벤더 게재 2023), Sahni et al. 2018(9.05%→10.80%, 약 20%, 리드 31%, 2차 출처), 2023 Marketing Letters 재현 실패, 2025 반려동물 앱 595명, BrazeAI 생성형 AI의 Liquid·HTML 지원, "Liquid Assistant" 미확인 — 01_reference.md·research/*.md와 일치
### 미해소
- (없음)
## 08장 (라운드 1)

### ❌ 정정
- "Operator와 Agent Console은 베타로 소개됐고, 2026-11 기능 목록에는 정식 출시 여부가 따로 적혀 있지 않다" → "2025-12 연간 리뷰에서 베타로 소개됐다. 2026-11 목록에서 Operator는 상태 표시 없이 올라 있고, Agent Console이라는 이름은 목록에 따로 보이지 않는다" — 근거: W32(연간 리뷰), 웹 2차 braze.com/docs/user_guide/brazeai (2026-11-03 조회: 상태 라벨은 Content Optimizer "beta"뿐, Agent Console 미기재). 핵심 요약 bullet에도 "2025-12에 베타로 소개" 보강.
- Smart Recommender 그룹 "새 상품 발견" → "상품 발견" — 근거: 01_reference W11 (2그룹은 "상품 발견·참여")
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — 원고가 이미 "2026-11 기준"·연도 표기를 붙임)
### ✅ 확인 (요약)
- 명칭 연혁(Sage AI 2023-06-27, `/sage_ai/`→`/brazeai/`, Intelligent Selection→Optimize with BrazeAI, Most Engaged→Intelligent Channel, Agent One 2025-03·2026-09-17, G2 표기) — W24·W4
- BrazeAI 기능 지도(Operator·Braze Agents·Decisioning Studio Go/Pro·OfferFit 2025-06-02·MCP server·Content Optimizer beta·Liquid Assistant 미기재) — W24·W32, 웹 2차 Braze Docs 일치
- Intelligent Timing·Insider STO 동작·제약 8건, Next Best Channel, Optimize 조건 — W25·W12·W13
- 논문 수치: Singh et al. 2020(19.24%/16.48%, 프리프린트), Schwartz·Bradlow·Fader 2017(7.5억 노출, 8%, 약 10%) — papers.md·01_reference
- 리뷰 인용 3건(2026-09-25, 2026-09-22, 2026-10-08)·금융업 리뷰(2026-10-19), Soyuerel 인용 — community.md·W4
### 미해소
- (없음)

## 09장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "(광고)" 표기 단락의 `(사실 확인 필요)` 해소: 일반 원칙(광고 시작 부분 "(광고)")은 실무 통설로, 2026-03 개정 후 "제목이 있는 메시지는 제목·본문 모두 표기"는 발송 대행사 공지(solapi 2026-04-08, 7차 개정 언급) 기준으로 출처 층위 명시, 앱 푸시 표기 위치·명칭·수신거부 표기는 "공개 자료로 확정되지 않음 → 안내서 원문·법무 검토"로 명시. 웹 2차: 보안뉴스 2026-03-04, solapi 공지, Hackle·openads 해설 — 앱 푸시 세부 위치는 1차 원문으로 확인 불가.
### 🕒 신선도
- (없음 — 장 전체가 2026-11 기준·출처 층위를 이미 명시)
### ✅ 확인 (요약)
- 제50조 ③ 야간(21:00~08:00) 별도 사전 동의 + 대통령령 매체(전자우편) 예외 — korea-compliance 1-1·1-2, 웹 2차: law.go.kr 본문은 JS 렌더로 미확보, korea.legal 미러·itwiki 조문 전재("오후 9시부터 그 다음 날 오전 8시까지 … 별도의 사전 동의") + 실무 해설 다수 일치. 원고가 이미 "law.go.kr 원문 대조 권장"·"실무 해설" 층위로 기술해 유지.
- 제50조 요약표 8행(①~⑧, 거래관계 6개월은 "실무 해설"로 표기됨) — korea-compliance 1-1~1-3과 일치
- 2026 개정(법률 제21500호, 2026-03-31 공포, 2026-10-01 시행, 정보보호수준 평가 2027-04-01, 매출액 최대 6% 과징금, 정책브리핑 2026-09-30 인용) — 1-7
- 안내서 개정 내용(모호한 동의 문구 금지, 포인트 소멸 안내 광고성, 앱 푸시 거부 시 로그인 요구 금지), 2년 정기 확인(실무 해석 표기), 개인정보보호법 제22조 동의 분리 — 1-3·1-4·2-1
- 카카오 3종 표·알림톡 링크 유의·브랜드 메시지 08:00~20:50, Braze 카카오톡(2026-04, CJ올리브네트웍스·Infobip, "For now…" 인용, 20:50~08:00 공급자 강제, 알림톡 미기재), Insider Call an API — 3-1~3-5·4-1·4-2
- Infobip 고객센터 연락처 필수, 국내 데이터센터 2026-04, 가격 인하 알림 opt-in, Promotional/Transactional — W18·W20·W29·W8
- 고구마팜 2022-04-25, Airship 2026-08, Braze 블로그 상한, Wang·Lu·Shi 2022, Aridor·Che·Salz 2023(12.5%), Utz et al. 2019(독일 8만+), Montaguti 외 2016 — 01_reference
### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- `(사실 확인 필요)` 해소: "Canvas 진입 방식의 정확한 명칭과 옵션은 Braze Docs에서 확인" → "Canvas 진입 방식은 Scheduled, Action-Based, API-Triggered 세 가지(2026-11 Braze Docs 기준), 여기서는 Action-Based" — 근거: X24 + 웹 2차 braze.com/docs/.../create_a_canvas (action-based: "opening your app, making a purchase, or triggering a custom event")
- 잡코리아 속성 갱신 "Canvas 안에서 속성을 실시간으로 업데이트" → "Canvas 안에서 업데이트하기도 하고, 실시간으로 갱신하기도 하고, CSV…" — 근거: W30 요약("Canvas·실시간·CSV 일회성 업로드로 갱신")
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — 잡코리아 사례 시점(통계 2023-07, 캠페인 ~2023-11) 이미 명시)
### ✅ 확인 (요약)
- 잡코리아 카피·인용·고민 4가지·실행(Liquid 경과일, 슬라이드업 인앱, 랜덤 샘플, A/B, 채널 3종)·성과(CTR 4~5배, 5%p+, 두 자릿수 근접·약 4%p, CVR 대조군 대비↑, 자체 보고) — W30
- Canvas 컴포넌트(Message·Delay·Audience Paths·Decision Split·Action Paths·Experiment Paths·Exit criteria), Quiet Hours — W22·W29
- Architect(Starter 실시간, Wait/Check/Channel, 채널 App push·Email·In-app·Onsite, Promotional/Transactional, reachability, Journey A/B Split, Dry Run, STO Dry Run 미동작) — W6~W8·W12
### 미해소
- (없음)
## 11장 (라운드 1)

### ❌ 정정
- "세 가지 진입 방식(일정 기반·행동 기반·API 기반, 사실 확인 필요) … 정확한 선택지 이름은 Braze Docs에서 확인하자" → "일정 기반(Scheduled)·행동 기반(Action-Based)·API 기반(API-Triggered)"로 확정, 확인 권유 문장 삭제 — 근거: braze.com/docs Create a Canvas, Entry Controls 라벨 (2026-11-03 웹 확인, X24 해소)
- "Back in Stock Starter" → "On Back in Stock Starter" — 근거: academy.insiderone.com/docs/architect-journey-starter-on-back-in-stock (2026-09-03)
### ⚠️ 약화·삭제 / 보강
- [리서치 공백] 재입고 소절: 마커 삭제, 1차 문서로 확인한 내용을 넣음 — Braze: `type`에 `back_in_stock`, 재고 0인 상품만 구독 가능, 숫자형 재고 필드가 0보다 커지면 발송, 행동 기반 Canvas의 Back in stock 트리거, 분당 10,000명·하루 50,000개·구독 90일 (braze.com/docs back_in_stock_notifications). Insider One: 기본 이벤트 Product Page View(위시리스트 등으로 변경 가능), Product ID 필요, Clickstream·XML·Catalog API, 재고 수량 조건 불가·재고 있음/품절만 판단 (Academy 2026-09-03)
- "재고가 몇 개 이상 들어왔을 때 알릴지도 정해야 한다" → 두 트리거 모두 품절→재고 있음 전환 기준이니 수량에 맞춘 대상 조절은 여정 쪽에서 챙겨야 한다는 문장으로 바꿈 (위 문서와 맞춤)
### 🕒 신선도
- 재입고 한도는 "2026-11 기준 Braze 문서", Insider Starter는 "2026-09 Academy 문서 기준"으로 시점 명기
### ✅ 확인 (요약)
- BlaBlaCar 구조(네 무리·Action Paths 1시간·이벤트 속성·Connected Content·Experiment Paths·Audience Sync·채널)·"up to 48%/30%"(벤더 발표 표기 있음) — 01_reference 3.3/W31
- Samsung 헤드라인 "275% in 20 days"(벤더 발표 표기, 세부 수치 미인용) — 3.4/W15, X3 준수
- Braze 가격 인하 한도 5건(분당 10,000·10분 100,000·하루 50,000·1억·90일), Perform Price Drop Event, opt-in·Quiet Hours — W29 및 Braze 문서
- Insider On Price Drop 기본 이벤트·필터·제약·카탈로그 소스, Academy 인용문 — W14
- Braze 카카오톡 2026-04 출시·리테일 장바구니 이탈 예시 — W18/W19
- Insider Live Actions·reachability·Dry Run·Promotional opt-in·Liquid 얼리 액세스·Journey A/B Split — W7/W8/W10
- Gordon 외 2023 (663개, 하단 62%·상단 115%) — P-D6
### 미해소
- (없음)

## 12장 (라운드 1)

### ⚠️ 약화·삭제
- "정액 구독에서는 고객이 더 자주 와도 매출은 그대로인데 서비스 원가는 늘어나기 때문으로 보인다(사실 확인 필요)" → 논문 abstract가 밝힌 설명(늘어난 이용량 = 운영 비용, 그 비용이 리텐션 이득을 넘는 고객군에서 이익 감소)과 "요금은 그대로"라는 추론을 분리하고, 뒤의 것을 "논문이 직접 밝힌 내용이 아니라 이 책의 해석"으로 표시 — 근거: papers.md G2, MSOM abstract(IDEAS/RePEc·INFORMS 요약, 웹 확인; 서비스는 tiered subscription)
### ✅ 확인 (요약)
- Reichheld & Sasser 1990 "25~85%", 업종 예, Byron Sharp 비판 — X4 준수
- Predictive Churn 0~100·활성 예측 3개(프리뷰 1개), Insider Predictive Segments 유형·churn 전용 유형 없음 — W26/W13
- Ascarza 2018 JMR, 두 필드 실험, 4.1~8.7%p(AMA·MSI 소개 출처 표기) — P-C2
- Lemmens & Gupta 2020 방향만 서술(X5 준수), 업리프트 4분류는 "업계에서 흔히 쓰는"(X13 준수)
- Smart Recommender 6그룹(2026-10)·2024년 4그룹, 알고리즘 목록·Chef 60일·Bundle Strategy — W11
- Decisioning Studio Go/Pro, AI item recommendations — W24
- adidas "AOV 259%·conversion 13%"(벤더 발표), 18.8% vs 18.5% — 3.5/W15
- Linden·Smith·York 2003, Jannach & Jugovac 2019 — P-H1/P-H3
- Wang·Lu·Shi 2022 수치 7.4%·26.3%·7.0%, 등급별 이익, 피로, "double-edged sword" — P-G2(abstract 확인)
### 미해소
- (없음)

## 13장 (라운드 1)

### ✅ 확인 (사실 확인 필요 주석 해소)
- Braze 다변량: 변형 최대 8개 + 메시지를 받지 않는 대조군 가능, 발송 시작 후 제목·본문을 고치면 실험 무효 — 웹 확인: braze.com/docs create_multivariate_campaign ("Users in the control group don't receive the test…"). 주석 삭제
### ✅ 확인 (요약)
- Gordon, Moakler & Zettelmeyer 2023 62/107/115% — P-D6
- Lewis & Rao 2015 25개 실험·1,000만 인-주; Bidargaddi 2018 3.9% — P-D4/P-F2
- Experiment Paths·Winning Path·Optimize with BrazeAI(구 Intelligent Selection) 요건 — W25/W22
- Insider Journey A/B Split·A/B autowinner·Conversion Goal·last-touch — W7/W8
- Schwartz·Bradlow·Fader 2017 약 10% — P-I3
- SRM 약 6%(Microsoft)·"fever" 인용 — P-E3; Johari 2022 "wholly unreliable" — P-E4; Kohavi 2009 HiPPO — P-E1
- Monzo(Rodrigo Baptista, 2025-09, 2.5%·6개월·보정 계수 예·인용 2건) — C-휴4
- 리뷰 인용(Insider 리테일 2026-10·여행업, Braze 대시보드) — C-패턴6
- Currents(Avro·Tealium/Segment/mParticle·엔타이틀먼트·Pro/Enterprise 포함) — W27
- 카카오스타일 S3·QuickSight·앱 트래픽 35%(벤더 게재, 게재일 미표기 표기 있음) — 3.2
### 미해소
- (없음)

## 14장 (라운드 1)

### ❌ 정정
- 카카오 소절: Braze 카카오톡 = CJ올리브네트웍스·Infobip을 거치는 채널 친구 대상 마케팅 메시지로 명시, Insider One은 네이티브 채널 미확인·Architect Call an API로 직접 설정하는 사용 사례 문서뿐, 알림톡은 "두 도구 모두" 미확인으로 정리 — 근거: research/korea-compliance.md 자료 4-1·4-2, X1·X2
- "13장에서 여러 번 인용한 Kohavi, Tang & Xu의 『Trustworthy Online Controlled Experiments』" → "13장에서 인용한 Kohavi가 Tang, Xu와 함께 쓴 …" — 13장은 이 책이 아니라 Kohavi 외 2009 논문을 인용함 (P-E1/P-E2)
- "기술 지원 없이 우리 팀이 여정을 완전히 독립적으로" → "큰 기술 지원 없이 …" — 원문 "without heavy technical support" (C-패턴1, 금융업 2026-09-22)
### ✅ 확인 (요약)
- The Grow Getter(2023-11-10) 인용 4건·3~4개월 — C-패턴1/7, C-휴5
- Gartner: Insider One 2026 Personalization Engines Leader, Braze MMH 4년 연속 Leader — "회사 측 발표" 표기 있음 (W17/W33)
- 리뷰 인용(Insider 2026-10, Braze 2026-10 워크스페이스 권한 우회) — C-패턴1
- 비용 요인(데이터 포인트·메시지 크레딧·SMS/Content Cards 애드온, Insider 커스텀 이벤트·속성의 데이터 포인트 소비) — C-패턴7, W9
- Braze Certified Practitioner 60분·3년 유효(2026-11 기준 표기), Practitioner Learning Path, 장바구니 이탈 코스 — W35
- 인프런 수강평(2022) — C-패턴2
### 미해소
- (없음)

## 13장 (라운드 2 — 수락 게이트 f)

수락 게이트(05_acceptance.md (f))가 되돌린 원장 공백 보강. 원고는 수정하지 않음(13장 보강은 chapter-writer 몫). 근거는 research/braze-analytics.md에 정리, 검색 시점 2026-11-03, 모두 벤더 공식 문서.

### ✅ 확인
- Braze Canvas 분석: 상단 요약(발송·총 진입·전환/전환율·총 매출·총 이탈·Reachable users), 단계별 진입/이동/이탈·고유 수신자·전환·매출, Revenue Breakdown, Analyze Variants(변형별 전환·대조 변형 대비 Uplift·신뢰도), Funnel/Retention 탭 — braze.com/docs …/measuring_and_testing_with_canvas_analytics/
- 전환 귀속 규칙(진입당 이벤트별 1회, 최근 메시지 귀속) — 같은 문서
- Braze 캠페인 분석: 채널별 결과, Unique Opens/Clicks 7일 창, Primary Conversions·Conversions B~D, 대조군 있을 때만 Confidence(unpooled Z-검정, 95%) — Reports 개요, ab_testing/analytics, report_metrics
- Braze 리포트 목록: Report Builder(New/legacy; 행·드릴다운·대시보드 추가), Dashboard Builder, Query Builder, Engagement reports(정기 CSV), Custom events·Revenue, Funnel, Retention(최대 30일) — analytics/reporting/, report_builder/
- Braze Global Control Group: 존재. 1~15 정수 %, 권장 ≥1,000명·≤10%, 태그 예외(거래성), API 캠페인은 발송(API 트리거 Content Card 제외), 크기 변경 = 비활성화 후 재생성(재셔플, 복구 불가), 셔플 월 1회 이하·실험 3개월 권장, 워크스페이스당 1개, 피처 플래그 실험 불가, Global Control Group Report 지표 — engagement_tools/testing/global_control_group/

### ⚠️ 약화 지침 (작성 시)
- 리포트 기능의 베타/GA 상태는 문서에 표기 없음 → 상태 단정 금지
- Canvas 상단 요약에 unique opens/clicks 없음 → Canvas 요약 지표로 쓰지 말 것

### 확인되지 않음
- Insider One 전역/유니버설 대조군: Academy에서 해당 기능 문서 미발견(캠페인 단위 대조군, OnSite 대조군 분석만 확인; Architect 대시보드 섹션엔 대조군 언급 없음). 본문에는 "2026-11 기준 Academy에서 확인되지 않음"으로, 부재를 단정하지 않는다.

### 미해소
- (없음) — 13장 논지는 "확인되지 않음" 표기로 유지 가능
