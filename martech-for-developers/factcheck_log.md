# 사실 검증 로그

> 1파(1~3장) 1차 검증. 1차 대조 대상은 `research/*.md` 원본.
> 검증 시점 2026-07-26. 규율 문서: `02_plan.md` 185~224행.

---

## 01장 — 1차 검증

### 종합: 주장 17건 — ✅ 12 / ⚠️ 2 / ❌ 1 / 🕒 2 — **BLOCKING (❌ 1건)**

---

### 주장 1 — 오프닝 HN 인용 (Swizec)
- **본문:** (3~7행) "2025년 4월, 해커뉴스에 이런 댓글이 하나 올라왔다… — Swizec, Hacker News 댓글 43668825 (2025-04-12)"
- **판정:** ✅
- **근거:** `research/community.md:606` — "HN 43668825 / Swizec / 2025-04-12 / story: 'Rebuilding Prime Video UI with Rust and WebAssembly'". 원문 영어 + 리서처 번역이 함께 실려 있고, 본문 번역이 원문 5단계(Mixpanel→Salesforce→GA→Amplitude→Braze)를 순서·화자 모두 정확히 옮겼다. 도입부 "어떤 앱이 왜 이렇게 느려졌느냐는 물음"도 원 댓글 첫 줄 "> why is the old version so slow"와 일치. 신선도 원장(`community.md:1194`)에 조회일 2026-07-25 기록.
- **조치:** 없음. (본문 9행 "이건 한 사람의 경험 진술이고, 업계 전체를 대표하는 조사 결과가 아니다"라는 근거 강도 고지까지 붙어 있어 모범적이다.)

### 주장 2 — 2019년 HN 인용 (dlevine)
- **본문:** (42~44행) "대부분의 회사는 마케팅 스택으로 2~4개의 제품을 산다(CDP, 마케팅 자동화, 어트리뷰션, 애널리틱스)… — dlevine, Hacker News 댓글 20299880 (2019-06-27)"
- **판정:** ✅
- **근거:** `research/community.md:1206` 원문 — "most companies buy 2-4 products for their marketing stack (CDP, Marketing Automation, attribution, and analytics)… Each company does marketing enough differently that there isn't a single product that could solve the problem end-to-end for everyone." 번역 정확. 신선도 원장 `community.md:1184`에 2019-06-27 / 조회 2026-07-25.
- **조치:** 없음.

### 주장 3 — 대시보드 숫자 불일치 원인 4종 + "일상이다"
- **본문:** (23행) "이유는 여러 가지일 수 있다. 한쪽은 취소 건을 빼고 세고, 다른 쪽은 앱이 백그라운드로 내려간 사이 유실된 이벤트가 있고, 또 어느 쪽은 그날 자정 경계를 다른 타임존으로 잡았을 수 있다. … **이런 종류의 하루가 이 도메인에서는 예외가 아니라 일상이다.**"
- **판정:** ⚠️ 근거 약함 (본문이 근거보다 강하다 — 단, 원인 3종 자체는 "~일 수 있다"로 가정 표시가 되어 있어 통과)
- **근거:**
  - 원인 3종(취소 건 제외 / 백그라운드 유실 / 타임존 자정 경계)은 `research/*` **어디에도 없다.** 저술가 자신의 개발자 추론이다.
  - 리서치가 실제로 확보한 원인은 다른 것이다 — `community.md:1112`: "GA vs 내부 DB vs 광고 플랫폼 수치 불일치 | 🟡 **원인은 확보, 현장 사례는 미확보** | fourseventy의 '여러 채널이 같은 전환을 각자 주장'이 **원인**을 설명하지만, '우리 회사에서 숫자가 안 맞아 고생했다'는 **구체 사례담은 못 찾았다**".
  - 반면 **"일상이다"라는 빈도 주장에는 쓸 수 있는 1차 근거가 있는데 본문이 안 쓰고 있다** — `community.md:194` 마티니 솔루션 컨설턴트 JD 주요업무에 `데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅`이 **명시**돼 있다. `community.md:211`: "그게 예외 상황이 아니라 상시 업무라는 뜻이다."
- **조치:** 원인 3종은 가정 예시임을 문장으로 표시하고, 빈도 주장은 JD 근거로 갈아끼운다. 아래로 교체:

  > 이 질문에 답하는 사람이 개발자다. 초난감한 상황이다. 둘 다 버그가 아닐 수도 있기 때문이다. 어느 쪽이 취소 건을 빼고 세는지, 앱이 백그라운드로 내려간 사이 이벤트가 유실됐는지, 자정 경계를 서로 다른 타임존으로 잡았는지 — 코드에 에러가 하나도 없는데 숫자만 다른 경우의 수는 이렇게 얼마든지 세울 수 있다. 그리고 이건 드문 일이 아니다. 국내 마테크 회사 마티니의 솔루션 컨설턴트 채용 공고를 열어보면 **주요 업무 항목에 "데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅"이 그대로 적혀 있다**(2026년 7월 원티드 공고 기준). 예외 상황이 아니라 직무기술서에 실리는 상시 업무라는 뜻이다.

  ※ "여러 채널이 같은 전환을 각자 주장한다"(fourseventy)는 원인은 11장 어트리뷰션 소재이므로 여기서 굳이 당겨오지 않아도 된다.

### 주장 4 — Martech 정의 (AB180 인터뷰)
- **본문:** (56~62행) "국내 마테크 회사 AB180의 데이터 파이프라인 팀 리드 김재원의 말이다. > '마케팅 성과 분석이란…' — AB180 엔지니어링 블로그, 데이터 파이프라인 팀 인터뷰 **(게시일 미상)**"
- **판정:** ✅
- **근거:** `research/community.md:389` 인용문 **한 글자까지 일치**. 화자 정보는 `community.md:366` — "인터뷰이: Backend Engineering Group, Data Pipeline Team Lead 김재원". 게시일은 `community.md:367` — "게시일: **페이지에서 확인 불가**(`조회 불가`) / 조회일 2026-07-25". 본문의 "(게시일 미상)" 표기가 리서치 상태와 정확히 일치한다.
- **조치:** 없음. **다만 리서치가 경고한 함정 하나를 저술가가 잘 피했음을 확인 기록으로 남긴다** — 같은 인터뷰의 "하루 10억건 / 분당 100만건" 수치(`community.md:402`)와 "백엔드 그룹 19명" 조직 수치는 시점 미상이라 사용 금지 대상인데(`community.md:369`, `1093`행: 블로그 제목 "100억"과 본문 "10억" 불일치), 본문은 정의 문장만 인용하고 수치는 건드리지 않았다.

### 주장 5 — Martech 랜드스케이프 15,505개
- **본문:** (70~76행) "**2026년판 기준 15,505개**다. > 'The martech landscape effectively stopped growing this year, up just 0.79% to 15,505 products.' — chiefmartec, 2026 Marketing Technology Landscape Supergraphic (2026-05-05) … **1,488개가 새로 들어오고 1,367개가 빠져나갔다.**"
- **판정:** ✅
- **근거:** `research/web_gaps.md:759~770` — 총 15,505 / 성장률 0.79% / 추가 1,488 / 제거 1,367, 영어 원문 인용 2건 모두 일치. 발행일 2026-05-05는 `web_gaps.md:916` 참고문헌 5번과 일치. 저자 "스콧 브링커"도 같은 줄(Brinker, Scott)에서 확인.
- **조치:** 없음. **리서치의 최대 경고를 정확히 지켰다** — `web_gaps.md:774`: "검색 결과에 martech.org의 15,384가 있었으나 fetch하지 않았다. **책에는 15,505(2026년판)만 쓰고, 반드시 '2026년판 기준'이라고 연도를 못박아라.**" 본문 70행이 "2026년판 기준"을 명시했다. 다른 장에서 15,384를 쓰면 안 된다.

### 주장 6 — 영미권 CRM = 영업 (Salesforce Trailhead)
- **본문:** (84행) "Salesforce의 공식 학습 사이트인 Trailhead 문서를 열어보면 CRM의 세계는 **영업**의 세계다. 핵심 객체가 Account, Contact, Lead, Opportunity이고 … 주 사용자는 영업사원이다."
- **판정:** 🕒 검증 불가 → **시점 표기 누락 (조치 필수)**
- **근거:** 내용 자체는 ✅다 — `research/web_gaps.md:234, 238` (Lead→Opportunity 변환 모델), `web_gaps.md:287~290` 대조표("핵심 대상: 영업(sales) — Lead → Opportunity 파이프라인", "주 사용자: 영업사원", "핵심 객체: Account / Contact / Lead / Opportunity"). **문제는 시점이다.** `web_gaps.md:903`이 명시적으로 지시한다: "**Trailhead·Salesforce 개발자 문서·Segment 리포 마크다운은 페이지에 발행일이 없다. 전부 '2026-07-25 조회 기준'으로만 표기할 것.**" `web_gaps.md:879` 신선도 원장에도 발행일 "미표기", 조회일 2026-07-25로 기록돼 있다. 본문에는 시점이 전혀 없다.
- **조치:** 84행 첫 문장을 아래로 교체.

  > 영미권에서 CRM이 무엇을 가리키는지는 비교적 또렷하다. Salesforce의 공식 학습 사이트인 Trailhead 문서를 열어보면(2026년 7월 조회 기준 — 이 페이지에는 발행일이 없다) CRM의 세계는 **영업**의 세계다.

  ※ 이 규칙은 2장의 Segment Spec 저장소 마크다운에도 그대로 적용된다.

### 주장 7 — 한국 "CRM 마케팅" 인용의 출처 귀속
- **본문:** (88~92행)
  > CRM 마케팅이란 "…**리텐션을 높이는 모든 고객대상 마케팅**"
  > 채널: "푸시, 모달(IAM), 카카오 알림톡, 카카오 친구톡, 문자 메시지, 이메일 - 총 6가지가 대표적인 매체"
  > — **노티플라이 블로그 (2023-10-24), FlareLane 블로그 (2025-04-22)**
- **판정:** ❌ **오류 — BLOCKING (출처 오귀속)**
- **근거:** `research/web_gaps.md:250~263`. 인용된 **두 문장 모두 `[FETCHED] 노티플라이(Notifly)` 항목 아래에만 있다.** 정의 문장은 `web_gaps.md:260`, 채널 6종 목록은 `web_gaps.md:263`, 둘 다 노티플라이 원문이다. FlareLane에서 fetch된 인용 가능 구절은 **완전히 다른 문장**이다 — `web_gaps.md:274`: "CRM 마케팅은 '고객 관리와 데이터 분석을 통해 고객 가치를 극대화하는 전략입니다. 신규 고객을 유치하고 기존 고객의 충성도를 높이는 것을 목표로 하며'". 즉 현재 본문은 **노티플라이가 쓴 말을 FlareLane도 그렇게 썼다고 귀속**하고 있다. 인용 블록의 출처 줄이 사실과 다르다.
- **조치:** 인용 블록의 출처 줄을 노티플라이 단독으로 바로잡고, FlareLane은 별도 문장으로 분리한다. 86~92행을 아래로 교체.

  > 그런데 한국에서 "CRM 마케팅"이라는 말은 다른 걸 가리킨다. 국내 CDP·메시징 벤더인 노티플라이는 이 말을 이런 뜻으로 쓴다.
  >
  > > CRM 마케팅이란 "고객이 자사 플랫폼(서비스)에 유입되었을때, 말을 걸고, 구매를 유도하고, 구매한 이후 재탐색을 유도하는 등, **리텐션을 높이는 모든 고객대상 마케팅**"
  > >
  > > 채널: "푸시, 모달(IAM), 카카오 알림톡, 카카오 친구톡, 문자 메시지, 이메일 - 총 6가지가 대표적인 매체"
  > >
  > > — 노티플라이 블로그 (2023-10-24)
  >
  > 같은 계열의 다른 국내 벤더도 결이 같다. FlareLane은 CRM 마케팅을 "고객 관리와 데이터 분석을 통해 고객 가치를 극대화하는 전략"이며 "신규 고객을 유치하고 기존 고객의 충성도를 높이는 것을 목표로" 한다고 설명한다(FlareLane 블로그, 2025-04-22). 인용한 대목 어디에도 영업 파이프라인이라는 말은 나오지 않는다.

  ※ 마지막 문장을 "어느 쪽에도 나오지 않는다"로 쓰면 **두 글 전문에 대한 부정 주장**이 된다. 리서치가 확보한 건 발췌뿐이므로 "인용한 대목"으로 범위를 한정했다 — 02장 주장 13·03장 주장 15에서 이 책 자신이 지킨 기준이다.

  ※ 이렇게 고쳐도 96행의 "두 출처 모두 국내 마테크 벤더의 자사 블로그"라는 근거 강도 고지는 그대로 유효하다.

### 주장 8 — 노티플라이 채널 목록의 신선도
- **본문:** (90행 채널 6종 인용) + (100행) "그리고 위 채널 목록에 카카오 알림톡과 친구톡이 상위에 올라와 있다는 사실 자체를 기억해두자."
- **판정:** 🕒 신선도 경고
- **근거:** `research/web_gaps.md:902`가 경고한다 — "노티플라이 글(**2023-10-24, 약 3년 경과**)은 한국 CRM 마케팅 시장이 빠르게 변한 기간을 지났다. **채널 목록·솔루션 비교 부분은 지금과 다를 수 있다.** 정의 문장만 쓰고 솔루션·시장 현황 서술은 인용하지 말 것." 다만 같은 파일 `web_gaps.md:292`는 "카카오 알림톡이 채널 목록 상위에 오는 것 자체가 한국 시장 고유성의 증거다"라며 이 논점을 명시적으로 승인한다. 리서치 내부가 갈리므로 **삭제가 아니라 시점 명기**로 해소한다.
- **조치:** 100행을 아래로 교체.

  > 그리고 **2023년 시점의 그 채널 목록**에 카카오 알림톡과 친구톡이 상위에 올라와 있다는 사실 자체를 기억해두자. 목록의 구체 구성은 3년 사이 달라졌을 수 있지만, 국내 벤더가 채널을 꼽을 때 카카오 채널이 당연히 끼어 있다는 점은 그대로다.

### 주장 9 — CRM 두 용법의 근거 강도 고지
- **본문:** (96행) "한국 쪽 서술의 출처는 **둘 다 국내 마테크 벤더의 자사 블로그**다. 그러니 이건 '한국에서 CRM의 학술적 정의가 다르다'는 주장이 아니라, **업계에서 그 말이 실제로 그렇게 쓰인다는 용법의 증거**로 읽는 게 맞다."
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_gaps.md:811` — "다만 한국어 출처 2건이 모두 **자사 솔루션을 파는 벤더 블로그**임을 감안해, 중립적 정의가 아니라 **업계 용법의 증거**로만 쓸 것." 및 `web_gaps.md:293` 동일 취지. 리서치 지시를 문장 단위로 이행했다.
- **조치:** 없음.

### 주장 10 — 감마-감마 모델의 출처
- **본문:** (113~115행) "`lifetimes` 라이브러리에는 `GammaGammaFitter`라는 클래스가 있다 … 이 모델의 출처는 저널 논문이 아니다. **브루스 하디의 개인 웹사이트에 올라온 미간행 기술 노트**(brucehardie.com Note #25, 최종 갱신 2013-02-25)다. 이번 리서치에서 랜딩 페이지를 열어 저널 게재 논문이 아님을 확인했다."
- **판정:** ✅
- **근거:** `research/papers.md:90` — "Bruce Hardie (Fader & Hardie), 'The Gamma-Gamma Model of Monetary Value,' **미간행 기술 노트(unpublished note)**, brucehardie.com Note #25, 최종 갱신 **2013-02-25**." `papers.md:91` 출처 줄에 "(페이지 직접 조회)" — 본문의 "랜딩 페이지를 열어" 서술과 일치. `papers.md:93` — "`lifetimes.GammaGammaFitter`가 구현하는 대상이 저널 논문이 아니라 저자 개인 웹사이트의 PDF 노트다." 모델 성격("금액 쪽을 모델링") = Monetary Value ✅.
- **조치:** 없음.

### 주장 11 — "근거가 끊기는 항목 열두 건"
- **본문:** (117행) "이 책의 리서치는 업계가 학술적 권위처럼 사용하지만 실제로는 근거가 끊기는 항목을 **열두 건** 추려냈고, 그 목록을 4장의 뼈대로 삼는다. 거기에는 마케팅 지표뿐 아니라 여러분이 아마 기술 용어로 알고 있을 이름들도 섞여 있다."
- **판정:** ✅
- **근거:** `research/papers.md:1102~1122` 「학술 근거 없음 / 업계 관행」 목록의 항목 수가 **정확히 12개**다(LTV:CAC 3:1 / Gamma-Gamma / Send-time optimization / Lambda / Kappa / Feature store / Meridian·Robyn / Google 지오 실험 / 상시 홀드아웃 / Kafka 원 논문 / RFM 기원 / DMARC "표준"). "기술 용어로 알고 있을 이름들도 섞여 있다"는 서술도 Lambda·Kappa·Kafka·Feature store가 실제로 들어 있어 참이다.
- **조치:** 없음.

### 주장 12 — 근거 4갈래 분류 / 시점 병기 원칙
- **본문:** (106~111행, 119행) 벤더 자체 주장 / 1차 확인 / 학술 근거 / 업계 관행 4분류, 그리고 "이 책은 인용마다 **시점**을 붙인다".
- **판정:** ✅
- **근거:** 이 책 자신의 편집 방침 선언이며 `02_plan.md` §A·§B의 규율과 정합한다. 외부 사실 주장이 아니므로 대조 대상 아님. 다만 **선언한 이상 이행 의무가 생긴다** — 주장 6·8의 시점 누락이 바로 이 선언의 위반이다.
- **조치:** 주장 6·8 조치로 갈음.

### 주장 13 — 11개 용어 표 전체
- **본문:** (129~141행) 용어 11개 표
- **판정:** ✅ (개별 정의 전건 일치)
- **근거:** `research/community.md:916~930` 「F-5-C. 개발자가 반드시 알아야 할 마케팅 도메인 용어」 표와 대조. 항목별:
  - Attribution — `community.md:918` (AB180 블로그 정의문 요약) ✅
  - MMP "모바일 측정 파트너 … 채용 공고에 등장한다" — `community.md:919` 출처 "마티니 SC 우대사항" ✅
  - CDP "계정 데이터만이 아니라 온·오프라인 상호작용 행동 데이터까지" — `community.md:920` **문구 그대로** ✅
  - CDI "한 벤더 창업자가 '더 정확한데 아는 사람이 거의 없다'" — `community.md:923` ✅
  - 이벤트 택소노미 "Category + Event + Property 3층" — `community.md:921` ✅
  - PA "Amplitude·Mixpanel 계열" — `community.md:924` ✅
  - Identity Graph — `community.md:925` ✅
  - Reverse ETL "기본적으로 SQL에서 API로" — `community.md:928`, 원문 `community.md:558` ("basically from SQL to APIs", HN 43861360 throwaway7783) ✅
  - Deliverability "SPF·DKIM·DMARC, IP 평판, 블랙리스트" — `community.md:926` ✅ (**DMARC를 "표준"이라 부르지 않았다 — 금지 항목 13 준수**)
  - Segment — `community.md:929` ✅
  - 알림톡/친구톡 "알림톡은 정보성(채널 추가 불필요·템플릿 사전 심사), 친구톡은 광고성" — `community.md:930` ✅
- **조치:** 없음.

### 주장 14 — 용어 표의 선정 기준
- **본문:** (127행) "아래 열한 개는 이번 리서치에서 **국내외 채용 공고 본문이나 실무 문서에 실제로 등장한 것만** 추린 목록이다."
- **판정:** ⚠️ 근거 약함 (본문이 근거보다 좁게·강하게 말한다)
- **근거:** `research/community.md:915`의 선정 기준은 "이 세션에서 조회한 **채용 공고 본문 또는 실무 문서에 실제로 등장한** 것만"으로 문면은 같다. 그러나 같은 표의 실제 출처를 보면 **11개 중 4개(CDP·CDI·Reverse ETL·Deliverability)의 출처가 Hacker News 댓글**이다(`community.md:920, 923, 926, 928`). HN 댓글을 "채용 공고 본문이나 실무 문서"라 부르기는 어렵다.
- **조치:** 출처 범위를 정직하게 넓힌다. 127행 해당 문장을 아래로 교체.

  > 아래 열한 개는 이번 리서치에서 **국내외 채용 공고 본문·실무 블로그·개발자 커뮤니티 글에 실제로 등장한 것만** 추린 목록이다. 사전에서 옮겨온 게 아니라, 누군가가 실제로 그 단어를 써서 사람을 뽑거나 일을 설명한 자리에서 가져왔다.

### 주장 15 — CDI 곁가지 (RudderStack 창업자)
- **본문:** (151행) "이 말은 RudderStack의 창업자가 해커뉴스에서 자기 회사의 포지셔닝 이야기를 하다가 꺼낸 것이다. CDP라는 말은 널리 알려졌지만 범위가 너무 넓고, CDI가 더 적확한데 아는 사람이 거의 없다는 취지였다."
- **판정:** ✅
- **근거:** `research/community.md:715~716` — HN 27553257 / soumyadeb / 2021-06-18, 원문: "Thanks for the feedback on **positioning**… CDP (Customer Data Platform) is a more widely known space but **it's too broad**. CDI (Customer Data Infrastructure) is more relevant but **very few people know about it**." 본문 요약이 원문 3요소(널리 알려짐 / 너무 넓음 / 아는 사람 거의 없음)를 정확히 옮겼다. "창업자" 신분은 `community.md:995` — "RudderStack 창업자 soumyadeb".
- **조치:** 없음. (직접 인용이 아니라 간접 요약이므로 시점 병기 의무는 약하나, 2021년 발언임을 한 마디 넣으면 더 안전하다 — 선택.)

### 주장 16 — Segment 대소문자 중의성
- **본문:** (145행) "소문자로 쓰면 조건으로 뽑아낸 사용자 집합이고, 대문자로 시작하는 Segment는 회사이자 제품 이름이다."
- **판정:** ✅
- **근거:** `research/community.md:929` (segment = 사용자 집합, 출처 Klaviyo JD) + `research/web_products.md` 전반의 Segment 제품 문서. 자명한 용어 정리이며 대조 결과 모순 없음.
- **조치:** 없음.

### 주장 17 — 책 구성 예고 (12장 4단계)
- **본문:** (155~163행) 1~4장 / 5~7장 / 8~11장 / 12장 4단계 구성, 각 장 예고
- **판정:** ✅
- **근거:** `02_plan.md` 챕터 명세와 대조. 12장 구성, 각 장 배치(3장 시장 지도, 9장 채널·알림톡, 11장 어트리뷰션·인과, 12장 커리어) 일치. `02_plan.md:179` — "1장(CRM 세 글자·용어 지도), 9장(알림톡), 10장(PIPA·정보통신망법), 12장(시장 지형)"과도 정합.
- **조치:** 없음. (본문 66행의 "11장", 100행의 "9장", 117행의 "4장", 147행의 "3장" 상호참조도 모두 계획과 일치.)

---

### 01장 요약

**BLOCKING 항목 (Phase 5 진행 차단):**
- ❌ 주장 7 — 노티플라이 인용문 2건을 FlareLane에도 귀속. 출처 줄 정정 필요.
- 🕒 주장 6 — Trailhead 인용에 조회 시점 없음(`web_gaps.md:903`이 명시 지시).
- 🕒 주장 8 — 2023년 채널 목록을 시점 없이 현재형으로 사용.

**수정 요망 (⚠️):** 주장 3(불일치 원인의 근거 강도 + 미사용 JD 근거), 주장 14(선정 기준의 출처 범위).

**금지 항목 위반:** 1장에서 0건. (DMARC를 "표준"이라 부르지 않았고, CDP는 최소 정의만 두고 3장으로 넘겨 4분류 위험 자체를 회피했다.)

**총평:** 인용 강도 고지·시점 명기 원칙을 본문에서 선언하고 대체로 지켰다. 그러나 그 원칙이 정작 자기 문단(Trailhead·노티플라이)에서 두 번 새고, 인용 귀속 오류 1건이 있다. 셋 다 문장 단위 수정으로 해소된다.

---

## 금지 항목 스캔 결과 (1파 1~3장) — 선행 실행

> `02_plan.md` 185~224행 규율 전 항목을 3개 초안 전체에 grep으로 대조했다. **BLOCKING 위반 0건.**

| # | 금지 항목 | 결과 | 확인 내용 |
|---|---|---|---|
| 1 | **CDP 4분류**(Data/Analytics/**Campaign**/**Delivery**) | ✅ 위반 없음 | `Campaign`·`Delivery` 문자열 3개 초안 전체 0건. 03장 35행은 원문 3분류(**Data / Analytics / Personalization**)만 쓰고 **"2018년 Raab 기준"을 33행에 병기**했다. 나아가 35행 말미에 "다른 자료에서 이 목록이 넷으로 늘어난 형태를 보더라도, 이 책은 원문에서 확인한 셋만 쓴다"고 **금지 사유까지 본문에 명시**했다. |
| 2 | **CDP Institute 기관 정의문**("persistent, unified customer database…") | ✅ 위반 없음 | `persistent` 문자열은 03장 41행 1건뿐인데, 이는 **Raab 개인 블로그 원문**인 "a persistent, **sharable** customer database"다(`research/web_products.md:203`에 원문 확보). 금지 대상인 CDP Institute의 "persistent, **unified** customer database"(`web_gaps.md:125`, `web_products.md:73`)와는 **다른 문장**이며, 기억 복원이 아니라 리서치가 fetch한 원문이다. 03장 43행은 한 걸음 더 나아가 "그 기관 사이트는 리서치 시점(2026년 7월)에 접근이 막혀 원문을 확인하지 못했다. 그래서 이 책은 기관 정의문을 쓰지 않는다"고 **명시적으로 배제 선언**했다. `02_plan.md` 금지 4번("Raab 개인 정의로 대체하되 둘을 섞어 쓰지 마라")을 정확히 이행. |
| 3 | **CEM/CXM을 비교표에 포함** | ✅ 위반 없음 | 비교표(03장)에 해당 열 없음. 03장 81행이 "**CEM/CXM은 이 표에 들어오지 못했다.** 1차 정의를 확보하지 못해서다. 검색 요약에는 그럴듯한 정의가 떠 있었지만, 그걸 특정 조사기관의 정의라고 적는 순간 없는 출처가 하나 생긴다"고 **부재 사유를 본문화**했다. 금지 3번("검색 요약의 Gartner 정의를 Gartner에 귀속시키지 마라")도 준수 — Gartner 귀속 0건. |
| 4 | **"DMP=서드파티 쿠키, CDP=퍼스트파티" 통설** | ✅ 위반 없음 | `서드파티`·`퍼스트파티`·`third-party` 문자열 3개 초안 전체 **0건**. 03장 81행이 "DMP와 CDP를 **데이터의 출처 종류**로 갈라 설명하는 통설도 이 책은 쓰지 않는다. 어떤 1차 소스로도 확인하지 못했고, Adobe의 DMP 문서에는 쿠키나 익명 데이터에 대한 언급 자체가 없었다"고 배제 선언. |
| 5 | **Snowplow·RudderStack·Redis를 "오픈소스"로 단정** | ✅ 위반 없음 | `오픈소스`·`오픈 소스`·`open source`·`OSI` 문자열 3개 초안 전체 **0건**. (RudderStack은 02장 스키마 비교표·01장 CDI 일화에 등장하지만 라이선스 서술은 없다.) |
| 6 | **Tier 2 항목(Redpanda·Pulsar·Snowflake·BigQuery·Airflow 등)의 버전·수치** | ✅ 위반 없음 | 유일한 히트는 03장 167행 — Hightouch가 정의한 `Source`("any system where your data resides")의 **예시 나열**로 "Snowflake·BigQuery·Databricks·PostgreSQL 등"이 등장할 뿐, **버전 번호도 수치도 붙지 않았다.** 금지 대상은 버전·수치이므로 위반 아님. Redpanda·Pulsar·Airflow는 등장 0건. |
| 7 | **Theta Sketch 저자 오귀속**("Stokes, Tirthapura") | ✅ 위반 없음 | `Stokes`·`Tirthapura`·`Dasgupta`·`Theta` 전부 0건 (1파에서 근사 자료구조를 다루지 않음). |
| 8 | **Gordon 2019에 구체 수치 귀속** | ✅ 위반 없음 | `Gordon`·`Zettelmeyer`·`Moakler`·`2201.07055` 전부 0건. |
| 9 | **DMARC를 "표준"으로 지칭** | ✅ 위반 없음 | `DMARC` 히트 1건 — 01장 139행 용어표의 "SPF·DKIM·DMARC, IP 평판, 블랙리스트가 여기 얽힌다". **"표준"이라는 단어를 붙이지 않았고** 세 약어를 나란히 나열만 했다. `research/community.md:926` 원문과 동일한 서술 방식. |
| 10 | **Goldfarb & Tucker / Berman / Blake 범위 한정 누락** | ✅ 위반 없음 | 세 이름 및 `Shapley`·`eBay` 전부 0건 (1파에 학술 인과 논의 없음). |
| 11 | **Ads Data Hub 20/50/10 임계값 전용** | ✅ 위반 없음 | `Ads Data Hub`·`AMC`·`클린룸` 0건. |
| 12 | **HyperLogLog·Bloom filter 수치를 원 논문에 귀속** | ✅ 위반 없음 | `HyperLogLog`·`0.81`·`12KB`·`14.378` 0건. (`Bloom` 히트는 벤더명 **Bloomreach**의 부분 문자열일 뿐이다.) |
| 13 | **LLM 카피 효과 크기 / Send-time optimization을 학술 근거처럼** | ✅ 위반 없음 | `LLM`·`발송 시각`·`send-time` 0건. |
| 14 | **C-Store 재수록본 DOI를 원본으로** | ✅ 위반 없음 | `3226595`·`10.1145`·`DOI` 0건. |
| 15 | **SKAdNetwork 세부 / PIPA·정보통신망법 과징금 %** | ✅ 위반 없음 | `SKAdNetwork`·`SKAN`·`과징금` 0건. |

### 부가 스캔

- **`(사실 확인 필요)` 미해소 마커:** 3개 초안 전체 **0건** ✅ (`TODO`·`TBD`도 0건). 저술가 3인의 자기 보고와 일치.
- **arXiv ID 등 의심 식별자:** 1파 3개 초안에 arXiv ID·DOI가 **하나도 등장하지 않는다.** 미래 YYMM 자동 ❌ 규칙 적용 대상 없음. (2파 이후 새로 등장하는 식별자에 대해서는 규칙을 그대로 적용한다.)
- **시점 병기(`02_plan.md` §B):** Raab 연도 병기(2013/2015/2018/2017) 전건 이행 ✅. Insider 문서 "페이지 표기 2026-07-23"(02장 145행) ✅. Adobe·Salesforce·Hightouch·Census 인용에 전부 "2026년 7월" 계열 시점 병기 ✅. **단 01장 Trailhead 인용에는 시점이 없다 — 01장 주장 6 참조(🕒).**

**금지 항목 스캔 총평: 15개 금지 항목 전건 통과.** 특히 03장은 금지 항목 3건(CDP 4분류·기관 정의문·DMP 통설)과 CEM/CXM 배제를 **본문에서 사유와 함께 명시적으로 선언**해, 후속 편집 단계에서 실수로 되살아나는 것까지 막아두었다. 1파에서 Phase 5를 차단하는 금지 항목 위반은 없다.

---

## 02장 — 1차 검증

### 종합: 주장 20건 — ✅ 17 / ⚠️ 2 / ❌ 0 / 🕒 1 — **수정 요망 (BLOCKING 없음)**

> 02장은 1파에서 **인용 정확도가 가장 높다.** 원문 대조한 인용 12건이 전부 한 글자까지 일치했고, 필드명·필드 개수·이벤트 이름에 오류가 하나도 없다. 지적 사항은 인용이 아니라 **저술가가 직접 구성한 예시의 근거 강도** 쪽에 몰려 있다.

---

### 주장 1 — Adobe XDM 두 클래스 정의문
- **본문:** (13~17행) "**XDM Individual Profile**: 'A record-based class that forms a singular representation of the attributes of both identified and partially identified subjects.' / **XDM ExperienceEvent**: 'A time-series-based class used to capture the state of the system when an event (or set of events) occurred, including the point in time and identity of the subject involved.' — Adobe Experience League, XDM 문서 (페이지 표기 'Last update May 23, 2026')"
- **판정:** ✅
- **근거:** `research/web_products.md:627, 629` — 영문 원문 **두 문장 모두 한 글자까지 일치**. 출처 표기는 `web_products.md:633` — "문서 표기 'Last update May 23, 2026' | 검색 시점 2026-07-25". 본문이 "페이지 표기"라는 한정어를 붙여 인용한 것도 리서치 표기 방식과 정확히 같다(발행일이 아니라 문서 사이트의 자체 표기라는 구분).
- **조치:** 없음.

### 주장 2 — 6개 벤더 스키마 비교표
- **본문:** (23~29행) Segment Spec / RudderStack / Insider One(UCD) / Adobe(XDM) / Bloomreach / Klaviyo 5행 비교표
- **판정:** ✅
- **근거:** `research/web_products.md:1079~1086` 원표와 대조. 행별로:
  - 사용자 식별 — `identify`+`userId`/`anonymousId`, `Identify`, `identifiers`(`email`/`phone_number`/`uuid`) 또는 `insider_id`, **"확인 불가(identity graph 언급만)"**, hard IDs/soft IDs, `Profiles` ✅ 전건 일치
  - 사용자 속성 — `traits`, (Identify의 traits), `attributes`+`custom`, XDM Individual Profile, Customers, `Profiles` ✅
  - 행동 이벤트 — `track`+`event`+`properties`, `Track`, `events[]`+`event_name`+`event_params`, XDM ExperienceEvent, Events, `Events` ✅
  - 5행에서 Adobe·Bloomreach·Klaviyo 칸의 **"확인 불가"도 원표 그대로** 옮겼다.
- **조치:** 없음. **31행의 "확인 불가" 해설은 모범 사례로 기록한다** — "'확인 불가'는 '그 제품에 그 기능이 없다'는 뜻이 아니다. 이번 리서치가 실제로 열어본 페이지 범위 안에서 해당 문장을 찾지 못했다는 뜻일 뿐이다." 리서치의 미확인 표기를 독자가 오독하지 않게 방어한 유일한 장이다.

### 주장 3 — Insider One UCD 3개념 인용
- **본문:** (37~39행) Identifiers "anything specific to the user" / Events "User actions across all online and offline channels, including add-to-carts, purchases, visits, and logins" / Attributes "enable you to collect users' information, such as age, gender, birthday…"
- **판정:** ✅
- **근거:** `research/web_products.md:329~331` — 세 인용 모두 원문 그대로. Events 인용의 나열 4종(add-to-carts, purchases, visits, logins) 순서까지 일치.
- **조치:** 없음.

### 주장 4 — 식별자 이원 구조 (3사 대조)
- **본문:** (66~70행) "Segment는 `userId`와 `anonymousId`를 나눈다 / Bloomreach는 아예 **hard ID / soft ID** / Insider One은 `identifiers`(`email`·`phone_number`·`uuid`)와 `insider_id`를 구분한다. … 서로를 언급한 적도 없는 회사들이 같은 이원 구조에 도달했다는 **관찰**은…"
- **판정:** ✅
- **근거:** `research/web_products.md:1079` 비교표 사용자 식별 행 전건 일치. `web_products.md:423` — "`insider_id`(string) **또는** `identifiers`(object) — 둘 중 하나 필수". 3사 병렬 자체는 리서치가 이미 `web_products.md:1091`에서 수행한 대조다.
- **조치:** 없음. **"관찰"이라는 단어로 근거 등급을 명시한 점이 정확하다** — 벤더 누구도 이런 수렴을 주장한 적이 없으므로 관찰로 표기하는 게 맞다.

### 주장 5 — Segment Spec 6개 콜과 원문 정의
- **본문:** (78~85행) Identify "who is the customer?" / Track "what are they doing?" / Page "what web page are they on?" / Screen "what app screen are they on?" / Group "what account or organization are they part of?" / Alias "what was their past identity?"
- **판정:** ✅
- **근거:** `research/web_products.md:905~910` — **6행 전부 한 글자까지 일치.** 89행의 한국어 대응("누구인가 / 무엇을 하는가 / 어느 페이지인가 / 어느 화면인가 / 어느 조직인가 / 예전 정체는 무엇인가")도 `web_products.md:919`의 리서처 번역과 동일.
- **조치:** 없음.

### 주장 6 — Segment Spec 인용 경로 고지 (403 → GitHub raw)
- **본문:** (87행) "이 문장들은 렌더된 문서 사이트에서 가져온 게 아니다. `segment.com/docs`는 조회 시점에 403으로 막혀 있었고, 위 원문은 **Segment가 공개해둔 문서 소스 리포지터리의 raw 마크다운**에서 확인한 것이다. 1차 소스이긴 하되 경로가 다르다."
- **판정:** 🕒 신선도 경고 (내용 ✅, 시점 표기만 누락)
- **근거:** 내용은 `research/web_products.md:899` 경고와 정확히 일치한다 — "`segment.com/docs/connections/spec/`는 **403 Forbidden**이었다. 대신 Segment가 공개한 문서 소스 리포지터리 `github.com/segmentio/segment-docs`의 raw 마크다운을 열어 원문을 확인했다. 즉 **1차 소스이되, 렌더된 문서 사이트가 아니라 문서 소스 파일**이다." 근거 경로를 본문에서 밝힌 것 자체가 모범적이다. **다만 시점이 없다.** `web_gaps.md:903`은 "Segment 리포 마크다운은 페이지에 발행일이 없다. 전부 **'2026-07-25 조회 기준'**으로만 표기할 것"을 지시했고, `web_products.md:917`도 인용 출처를 "발행일 미표기(리포 `develop` 브랜치, 2026-07-25 조회 시점)"로 적었다. 본문의 "조회 시점에"는 언제인지를 말하지 않는다.
- **조치:** 87행 두 번째 문장을 아래로 교체.

  > `segment.com/docs`는 **2026년 7월 조회 시점에** 403으로 막혀 있었고, 위 원문은 **Segment가 공개해둔 문서 소스 리포지터리(`segmentio/segment-docs`)의 `develop` 브랜치 raw 마크다운**에서 확인한 것이다. 이 파일들에는 발행일 표기가 없어 시점은 조회일 기준일 수밖에 없다. 1차 소스이긴 하되 경로가 다르다.

  ※ 01장 Trailhead(주장 6)와 **같은 성격의 누락**이다. 두 곳을 함께 고치는 게 좋다.

### 주장 7 — 예약 traits 17종
- **본문:** (91행) "`identify`에는 예약 `traits`가 정해져 있고 — `email`, `firstName`, `lastName`, `phone`, `birthday`, `company` 등 **열일곱 가지**다"
- **판정:** ✅
- **근거:** `research/web_products.md:922~944` 원문 표를 직접 세었다 — `address`, `age`, `avatar`, `birthday`, `company`, `createdAt`, `description`, `email`, `firstName`, `gender`, `id`, `lastName`, `name`, `phone`, `title`, `username`, `website` = **정확히 17개.** `web_products.md:1080`도 "traits (예약 17종)"으로 교차 확인된다. 본문이 예시로 든 6개(`email`·`firstName`·`lastName`·`phone`·`birthday`·`company`)는 전부 실제 목록 안에 있다.
- **조치:** 없음.

### 주장 8 — track 예약 property 3종
- **본문:** (91행) "`track` 쪽 예약 property는 셋뿐이다. `revenue`('Amount of revenue an event resulted in'), `currency`, `value`. 돈에 관한 것만 예약해뒀다는 점이 인상적이다."
- **판정:** ✅
- **근거:** `research/web_products.md:952~957` — 예약 properties 표가 정확히 `revenue`/`currency`/`value` 3행이고, `revenue`의 원문 설명이 "Amount of revenue an event resulted in" **그대로**다. 나머지 둘의 원문 설명("Currency of the revenue…", "An abstract 'value' to associate with an event")도 셋 다 돈·가치 관련이라 본문의 관찰이 성립한다.
- **조치:** 없음.

### 주장 9 — `group` 콜과 B2B/B2C 갈림길
- **본문:** (93행) "**B2B와 B2C의 갈림길이 `group` 콜에 있다.** … B2C 서비스에서는 거의 죽어 있는 필드지만, B2B SaaS에서는 계정 단위 분석과 과금이 통째로 여기 걸린다."
- **판정:** ✅
- **근거:** `research/web_products.md:1004` — "**B2B와 B2C의 갈림길이 `group` 콜에 있다.** B2C 마테크에서는 거의 안 쓰이고, B2B SaaS에서는 계정(account) 단위 분석·과금이 여기 걸린다." 리서처의 문장을 거의 그대로 옮겼다.
- **조치:** 없음. (리서치가 덧붙인 "Adobe가 별도로 'Real-Time CDP B2B Edition'을 두는 이유와 같은 문제"는 안 썼다 — 안전한 선택.)

### 주장 10 — `context` 18개 필드와 `channel`
- **본문:** (97~101행) "모든 콜에는 `context`라는 객체가 따라붙는다. **열여덟 개 필드**에 앱 정보·기기·OS·로케일·타임존·IP 같은 환경 정보가 담긴다. > `channel`(String): 'Where the request originated from: server, browser, or mobile.'"
- **판정:** ✅
- **근거:** 필드 수는 `research/web_products.md:1086` — "`context` 객체 (**18개 필드**)". `channel` 원문 정의는 `web_products.md:1065` — "Where the request originated from: server, browser, or mobile." **한 글자까지 일치.**
- **조치:** 없음. 101행이 이 필드에서 끌어낸 결론("이벤트를 어디서 쏠 것인가는 취향이 아니라 설계 문제")은 필드 존재라는 사실에서 저술가가 전개한 해석이며, 해석임이 문맥상 분명해 사실 주장으로 오독될 위험이 낮다.

### 주장 11 — `alias`의 실제 용도
- **본문:** (109~111행) "> 'an advanced method used to merge 2 unassociated user identities, effectively connecting 2 sets of user data in one profile.' 그리고 곧바로, 이건 **고급 유스케이스 전용**이며 Segment의 Unify 제품 안에서 프로필을 병합하는 용도로는 **쓸 수 없다**고 못박는다. … `alias`는 '다운스트림 목적지 호환 때문에 추적 중인 ID를 명시적으로 바꿔야 할 때' 쓰는 도구지, 익명→식별 전환의 표준 경로가 아니다."
- **판정:** ✅
- **근거:** `research/web_products.md:1009` 원문 정의 **한 글자까지 일치**. `web_products.md:1016` — "다운스트림 목적지 호환을 위해 추적 중인 사용자 ID를 **명시적으로 바꿔야 할 때**만. **고급 유스케이스 전용**이며, Segment의 Unify 제품 안에서 프로필을 병합하는 용도로는 쓸 수 없다 — 그건 Identity Resolution이 한다." 세 요소(고급 전용 / Unify 병합 불가 / Identity Resolution의 일) 전부 반영. `web_products.md:1018`의 "**개발자가 가장 자주 틀리는 지점이 여기다**"라는 리서처 판단도 본문 소제목(103행)과 일치한다.
- **조치:** 없음.

### 주장 12 — 커머스 예약 이벤트 이름 (v2 스펙)
- **본문:** (121~129행) Browsing / Promotions / Core Ordering / Coupons / Wishlisting / Sharing / Reviewing 7그룹 표
- **판정:** ✅
- **근거:** `research/web_products.md:1025~1033` 원표와 대조. **그룹 라벨 7개 전부 일치**(Browsing·Promotions·Core Ordering·Coupons·Wishlisting·Sharing·Reviewing). 이벤트 이름도 전건 일치하며, Core Ordering만 원문 13개 중 7개를 뽑고 "등"과 표 제목의 "(일부)"로 부분 발췌임을 표시했다 ✅. 미수록분(`Product Clicked`, `Checkout Step Viewed`, `Checkout Step Completed`, `Payment Info Entered`, `Order Updated`, `Order Cancelled`)은 발췌 누락일 뿐 오류가 아니다. "v2 스펙 기준"(119행) 표기도 리서치 출처(`ecommerce/v2.md`, "v2 스펙 / 2026-07 조회 기준")와 일치.
- **조치:** 없음.

### 주장 13 — "목록에 없는 것" 부정 주장
- **본문:** (135행) "`Product Removed`는 있다. `Coupon Denied`도 있다. … 그런데 **'상품 두 개를 비교했다'에 해당하는 이름은 없다.** 스크롤을 얼마나 내렸는지도, 리뷰를 몇 초 읽었는지도 없다."
- **판정:** ✅ (부정 주장이라 별도로 검증했다)
- **근거:** 부정 주장은 **본문의 발췌 표가 아니라 리서치의 전체 목록**에 대고 확인해야 한다. `research/web_products.md:1025~1033`의 예약 이벤트 **전체 28개**를 훑은 결과 비교(compare)·스크롤(scroll)·읽기 시간(read/dwell)에 해당하는 이름이 **하나도 없다.** 부정 주장 성립 ✅. 반대로 본문이 "있다"고 든 `Product Removed`·`Coupon Denied`는 실재 ✅.
- **조치:** 없음. (부분 발췌표 뒤에 전체 목록 기준의 부정 주장을 놓는 구성이라 독자가 표만 보고 검증할 수 없다. 사실은 참이므로 차단하지 않지만, 137행 앞에 "전체 목록을 봐도"를 한 마디 넣으면 더 정직하다 — 선택.)

### 주장 14 — Insider vs Segment 인코딩 대조
- **본문:** (141행) "Insider One의 웹 SDK는 페이지 타입을 메서드에 못박아뒀다 — `type: 'product'`를 넣으면 `product_detail_page_view`가 발생한다. 반면 Segment는 문자열 규약으로 풀었다 — `track('Product Viewed')`. … **다만 이 대조는 이번 리서치가 두 문서를 나란히 놓고 관찰한 것이고, 어느 벤더도 상대를 언급한 적은 없다.**"
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_products.md:1037~1043` — 리서처가 같은 대조를 수행하며 "**강한 타입 vs 유연한 컨벤션**"으로 정리했고, 곧바로 "⚠️ 이 대조는 이 리서치의 관찰이다. **두 벤더 모두 서로를 언급하지 않았다.**"라고 경고했다. 본문이 이 경고를 **문장째 본문에 반영**했다. 매핑(`type:'product'` → `product_detail_page_view`)은 `web_products.md:383`으로 확인.
- **조치:** 없음.

### 주장 15 — Insider 웹 SDK 코드·필드·페이지 타입
- **본문:** (145~178행) 태그 스크립트, `InsiderQueue` 패턴, 큐 정의 순서, 사용자 속성 필드 표, 페이지 타입 6종, `init`, 도메인 관찰
- **판정:** ✅ (전건 일치 — 이 장에서 가장 세밀한 대조 구간)
- **근거:** `research/web_products.md:343~393`과 항목별 대조.
  - 태그: `<script async src="//{partnerName}.api.useinsider.com/ins.js?id={partnerId}"></script>` — `web_products.md:343` **문자 단위 일치** ✅
  - 큐: `window.InsiderQueue = window.InsiderQueue || [];` + `push({type:'method_type', value:{...}})` — `web_products.md:346~351` ✅
  - "큐가 태그보다 먼저 정의되어야 한다"(156행) — `web_products.md:349` "큐는 Insider 태그가 로드되기 **전에** 정의되어야 한다" ✅
  - 필드 표 — `uuid` "INS123", `email` "jdoe@useinsider.com", `phone_number` String(E.164) "+120394879878", `birthday` Datetime "2000-01-20T00:00:00Z", `email_optin`/`sms_optin`/`whatsapp_optin` Boolean, `gdpr_optin` Boolean, `custom` Object {"membership":"Silver"} — `web_products.md:358~374` **타입·샘플값까지 전건 일치** ✅
  - "`uuid`·`email`·`phone_number` 중 최소 하나 필수"(172행) — `web_products.md:356` "필수 식별자(최소 1개): `uuid`, `email`, `phone_number`" ✅
  - 페이지 타입 6종(`home`→`home_page_view`, `category`→`listing_page_view`+`breadcrumb` 배열 요구, `product`→`product_detail_page_view`, `cart`→`cart_page_view`, `purchase`→`confirmation_page_view`, 나머지 `other`) — `web_products.md:380~387` **6행 전건 일치** ✅
  - 이벤트 메서드(`add_to_cart`·`remove_from_cart`·`custom_event`) 및 `init`이 "critical initialization trigger"이고 페이지당 한 번 — `web_products.md:390~392` 원문 "Critical initialization trigger (must fire once per page after user/page data)" ✅
  - 문서 시점 "(페이지 표기 2026-07-23)"(145행) — `web_products.md:394` "페이지 표기 Published 2026-07-23T13:40:34Z (문서 사이트 표기 — **최초 발행일/갱신일 구분 불가**)". 본문이 "페이지 표기"라는 한정어를 붙였으므로 ✅
  - 도메인 관찰(178행: 브랜드/문서는 `insiderone.com`, 태그 호스트는 `useinsider.com`) — 태그 URL(`web_products.md:343`)과 문서 URL(`web_products.md:1223` `academy.insiderone.com`), 샘플 이메일(`jdoe@useinsider.com`)로 **직접 확인 가능** ✅. 본문이 "벤더가 설명한 게 아니라 이번 리서치가 문서들을 대조하며 관찰한 것이다(2026년 7월 시점)"라고 근거 등급과 시점을 함께 밝혔다 ✅
- **조치:** 없음. 180행의 "이 절 전체가 **한 벤더의 표면**이라는 점도 분명히 해두자. 다른 벤더의 SDK는 다르게 생겼다"는 일반화 방지 문장도 적절하다.

### 주장 16 — 마티니 이벤트 택소노미 8단계
- **본문:** (186~190행) "한 국내 벤더가 자사 기술블로그에 이 과정을 여덟 단계로 정리해둔 글이 있다(마티니, 2024-05-30, 문소윤). 목적·방향성 수립에서 출발해 주요 지표 설정, 사용자 여정 스케치, 이벤트·프로퍼티 설계로 내려온 다음, **마케터 협의(5)와 개발자 협의(6)**를 거쳐 QA와 최종 수정으로 끝난다. > '5-6번 프로세스의 경우 수차례 반복될 수 있습니다…'"
- **판정:** ✅ (모범 사례)
- **근거:** `research/community.md:426~438` 원문 8단계 — ①택소노미의 목적 및 방향성 수립 ②주요 지표(이벤트 카테고리) 설정 ③사용자 여정(User flow) 스케치 ④이벤트 & 프로퍼티 설계 ⑤마케터 협의 ⑥개발자 협의 ⑦QA 테스트 ⑧최종 수정. **본문이 8단계를 순서까지 정확히 옮겼고 5·6번 번호도 맞다.** 인용문은 `community.md:441` **한 글자까지 일치**. 서지(마티니, 2024-05-30, 문소윤)는 `community.md:1148`·`1223`과 일치.
- **조치:** 없음. **여기가 이 장에서 가장 잘 처리된 대목이다.** 리서치는 `community.md:532`에서 이 pain point에 대해 강한 경고를 남겼다 — "커뮤니티 근거가 가장 약한 패턴이다… '커뮤니티에서 자주 나온다'고 쓰면 **거짓이다.** 대신 **'제품을 파는 쪽이 이걸 상시 업무로 정의해놓았다'**는 각도로 쓰는 게 정직하다." 본문 190행이 정확히 그 각도를 택했다 — "이 글이 자사 방법론을 알리는 성격의 콘텐츠라는 점은 감안하고 읽어야 한다. 그런데 바로 그래서 이 대목이 의미 있다. **자기 방법론을 소개하는 글에서조차** …라고 적어놓았다면". 리서치 지시의 정확한 이행.

### 주장 17 — 스키마 붕괴 사고 4종
- **본문:** (198~208행) "대표적인 **사고** 네 가지를 보자." → ①필드 이름 변경(`purchase_amount`→`amount`, 세그먼트 0명, 마케터가 3주 뒤 문의) ②타입 변경(숫자→`"39,900"`) ③단위 변경(원→센트, "10만원 이상 구매자"가 전 사용자가 되고 전 사용자에게 VIP 쿠폰 발송) ④중복 발송(`purchase` 두 번)
- **판정:** ⚠️ 근거 약함 (본문이 근거보다 강하다)
- **근거:**
  - **네 사고 중 어느 것도 `research/*`에 사례로 존재하지 않는다.** 저술가가 구성한 예시다. 세부 수치("3주 뒤", "39,900", "10만원", "0명")도 전부 창작이다.
  - 근본 현상(스키마가 계속 변해 이벤트가 조용히 깨진다)에는 근거가 있다 — `community.md:530` 「2위. 이벤트 택소노미가 망가진다 / 스키마가 계속 변한다」. 그러나 같은 줄이 **근거의 얇음을 명시**한다: "HN 1개 스레드 / 1명(+ 벤더 문서 1, 채용공고 1, GitHub 이슈 계보 1)". `community.md:532`: "**커뮤니티 근거가 가장 약한 패턴이다.**"
  - 즉 "**대표적인** 사고"라는 표현은 이 넷이 업계에서 전형적으로 관찰된다는 **빈도 주장**인데, 그걸 뒷받침하는 관찰이 리서치에 없다. 208행의 "이 차이가 이 도메인의 성격을 상당 부분 설명한다"가 그 위에 다시 얹힌다.
  - **반면 쓸 수 있는 근거를 본문이 안 쓰고 있다** — (a) `community.md:535` HN 39103276 / shkan / 2024-01-23: "**the pieces keep changing shapes**", "if you miss a step (like a missing field), guess what? **Start from scratch.**" (b) `community.md:546~550` Snowplow 저장소의 스키마 검증 이슈 계보 — #611(2014-04-01), #625(2014-04-08), #910(2014-07-22), #3165(2017-03-22), 검색 결과 9건 전부 closed. 리서처 판정: "**Snowplow가 2014년부터** 이벤트 스키마 검증을 파이프라인에 내장하는 작업을 해왔다는 것. '스키마를 강제하지 않으면 이벤트 데이터가 썩는다'는 문제의식이 **10년 넘은 것**임을 보여준다." (c) `community.md:541` 마티니 SC JD의 `데이터 품질 확보를 위한 수집 기준 및 검증 프로세스 정의`.
- **조치:** 네 예시를 **구성된 시나리오**로 명시하고, 빈도 주장은 실제 근거로 갈아끼운다. 198행과 208행을 아래처럼 손본다.

  **198행 교체:**
  > 문제는 실제로는 깨진다는 것이다. 조용히 깨진다. 이게 새로 생긴 문제도 아니다. Snowplow 저장소에서 "스키마 검증" 이슈를 찾아보면 **2014년 4월**에 열린 것부터 나온다 — "Add JSON Schema-based validation for incoming unstructured events"(#611). 이벤트 데이터가 스키마 강제 없이는 썩는다는 문제의식이 10년을 넘겼다는 뜻이다(2026년 7월 조회 기준). 어떻게 깨지는지, 네 가지 시나리오를 세워보자. 실제 사고 기록이 아니라 구조를 보여주려고 구성한 것이다.

  **208행 교체 (앞부분만):**
  > 네 시나리오의 **공통점을 보자. 시스템은 아무 에러도 내지 않는다.** … 이 도메인에서 일해본 사람은 이걸 "**조각들이 계속 모양을 바꾼다**"고 표현했다. 그리고 덧붙였다 — "**한 단계라도 놓치면(필드 하나 빠뜨리는 것처럼) 어떻게 되는지 아는가? 처음부터 다시다.**"(HN 39103276, shkan, 2024-01-23)

  ※ 위 둘은 `community.md:535`에 **각각 별개의 인용 조각**으로 기록돼 있다("the pieces keep changing shapes" / "if you miss a step (like a missing field), guess what? Start from scratch."). **한 인용 블록으로 합치지 마라** — 원문에서 붙어 있지 않은 두 조각을 이어 붙이면 01장 주장 7과 같은 종류의 오귀속이 된다. 위처럼 두 문장으로 나눠 각각 인용부호를 두는 형태를 지킬 것.

### 주장 18 — "같은 개발자가 프론트엔드 이벤트는 아무 협의 없이 바꾼다"
- **본문:** (194~196행) "백엔드 개발자는 API 응답 형식을 바꿀 때 … 필드 이름 하나 바꾸는 데도 릴리스 노트를 쓴다. 그런데 **같은 개발자가 프론트엔드 이벤트는 아무 협의 없이 바꾼다.** 왜 그럴까? … 이벤트에는 컴파일러도, 타입 체커도, 통합 테스트도 없기 때문이다."
- **판정:** ⚠️ 근거 약함 (개발자 행동에 대한 일반화, 출처 없음)
- **근거:** 개발자 집단의 실제 행동 빈도를 조사한 자료는 `research/*`에 없다. 다만 이건 검증 가능한 통계 주장이라기보다 **독자에게 던지는 수사적 대비**에 가깝고, 곧바로 나오는 설명(컴파일러·타입체커·통합테스트 부재)은 사실 진술로서 참이다. 과잉 차단하지 않되, 단정형이 근거보다 강하다.
- **조치:** 단정을 관찰 제안형으로 한 단계 낮춘다. 196행 첫 문장을 아래로 교체.

  > 그런데 프론트엔드 이벤트는 어떤가. 자기 팀의 지난 릴리스를 떠올려보면 답이 나올 것이다 — **이벤트 필드 이름이 바뀔 때 릴리스 노트가 나갔는가?** 그런 팀도 있겠지만, 대개는 아니다.

### 주장 19 — Snowplow 검증·실패 스트림 인용
- **본문:** (218행) "Snowplow 문서는 이 짝을 함께 말한다 — enrich 단계가 'validates each event against its schema'하고, 걸러진 것은 'failed events can be reprocessed'된다."
- **판정:** ✅
- **근거:** `research/web_stack.md:325, 327` — 원문 "The **Enrich** application cleanses the data and **validates each event against its schema** to ensure it meets the criteria you have designed and set." / "**failed events can be reprocessed**". 두 인용구 모두 원문 그대로 발췌. `web_stack.md:338`의 리서처 해설("통과 못 하면 유효 스트림이 아니라 **실패 스트림**으로 간다 — 버려지지 않고, 스키마를 고친 뒤 재처리할 수 있다")과 본문 논지도 일치.
- **조치:** 없음. **금지 항목 9번(Snowplow를 오픈소스로 서술) 회피 확인** — 본문은 Snowplow를 "문서"로만 지칭하고 라이선스에 대해 한마디도 하지 않았다 ✅.

### 주장 20 — 스키마 레지스트리 (Iglu / Confluent)
- **본문:** (220행) "Snowplow 생태계의 Iglu, Kafka 생태계의 Confluent Schema Registry가 그 자리를 맡는다. **세부 규칙은 각 문서를 확인하는 편이 낫고**, 여기서 기억할 것은 역할이다 — **스키마의 단일 진실 원천이 되고, 호환성 정책을 강제한다.**"
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_stack.md:1130` — "Snowplow는 Iglu, Kafka 생태계에는 Confluent Schema Registry(Avro/Protobuf/JSON Schema)가 있다. 역할은 같다 — **스키마의 단일 진실 원천 + 호환성 정책 강제.**" 그리고 `web_stack.md:1132` 경고: "⚠️ Iglu·Confluent Schema Registry의 **스펙 세부(SchemaVer, 호환성 모드 종류 등)는 이 세션에서 조회하지 않았다 — 확인 불가(미조회).**"
- **조치:** 없음. **본문이 "세부 규칙은 각 문서를 확인하는 편이 낫고"라고 쓴 것은 미조회 경고의 정확한 이행이다.** 확인 못 한 세부를 그럴듯하게 채워 넣지 않았다.

---

### 02장 요약

**BLOCKING 항목:** 없음. ❌ 0건.

**해소 필요 (🕒):** 주장 6 — Segment Spec 조회 시점 미표기. 01장 Trailhead와 동일 성격이므로 함께 수정.

**수정 요망 (⚠️):** 주장 17(사고 4종의 "대표적" 프레이밍 + 미사용 근거 3건), 주장 18(개발자 행동 일반화).

**금지 항목 위반:** 0건. 특히 Snowplow를 오픈소스로 부르지 않았고(금지 9), 스키마 레지스트리 세부 스펙을 지어내지 않았다.

**총평:** 원문 대조 인용 12건 전건 일치 — 필드명·필드 개수(traits 17 / context 18 / track property 3)·이벤트 이름·샘플값·페이지 타입 매핑까지 오류가 없다. 리서치의 경고 지시(확인 불가 해석 방어, 벤더 간 대조는 관찰, 마티니 글의 이해관계 고지, 미조회 세부 회피)를 **네 곳에서 명시적으로 이행**했다. 남은 두 ⚠️는 인용이 아니라 저술가가 채운 예시의 프레이밍 문제이고, 마침 그 자리에 쓸 수 있는 근거(shkan 인용·Snowplow 2014 이슈 계보)가 리서치에 놀고 있다.

---

## 03장 — 1차 검증

### 종합: 주장 32건 — ✅ 29 / ⚠️ 1 / ❌ 1 / 🕒 1 — **BLOCKING (❌ 1건)**

> 이 파에서 **규율 이행도가 가장 높은 장이다.** 금지 항목 3건(CDP 4분류·기관 정의문·DMP 통설)과 CEM/CXM 배제를 본문에서 사유와 함께 선언했고, Raab 4개 연도(2013/2015/2017/2018)의 내용이 **연도별로 정확히 분리**되어 있으며, 간접 확인·재구성·미확인을 전부 본문에 표시했다. ❌는 딱 한 곳, **오프닝의 숫자**다.

---

### 주장 1 — 오프닝: "벤더 20곳 중 카테고리를 명시한 곳은 넷뿐"
- **본문:** (7행) "이 책의 리서치는 마테크 벤더 **20곳**의 개발자 문서를 실제로 열어봤다. 그중 **자기 카테고리를 문서 첫 페이지에 명시한 곳은 넷뿐이었다.** 나머지 **열여섯 곳**은 자기가 무슨 카테고리인지 말하지 않는다."
- **판정:** ❌ **오류 — BLOCKING (숫자 3개 모두 근거와 불일치)**
- **근거:** `research/web_products.md:862~891` §B-2-5 「이 세션에서 확인한 벤더 전수」 표를 직접 세었다.
  1. **"넷뿐"이 아니라 다섯이고, 리서치는 그마저 단정하지 않았다.** `web_products.md:886`: "명시적 카테고리 라벨을 개발자 문서 첫 화면에 쓴 벤더는 소수다. 확인된 것은 Adobe RTCDP('Real-Time Customer Data Platform'), mParticle('a customer data platform (CDP)'), Insider UCD('the core Customer Data Platform (CDP)'), **CleverTap('Customer retention platform'), OneSignal('omnichannel messaging')** **정도**." — **5곳**이며 "정도"라는 한정어가 붙어 있다. 정확한 개수를 셀 수 있는 형태의 근거가 아니다.
  2. **"열여섯 곳"은 산술도 맞지 않는다.** 20 − 5 = 15다. 4를 택해도 20 − 4 = 16이 되지만, 그 4가 어디서 나왔는지 근거가 없다.
  3. **"20곳의 개발자 문서를 실제로 열어봤다"도 과장이다.** 같은 표에서 **3곳은 조회 자체가 실패**했다 — 다이티("**확인 불가(사이트 조회 실패)**", `web_products.md:884`, TLS 인증서 오류 `web_products.md:851`), Salesforce Data Cloud("**확인 불가(문서 404/렌더 실패)**", `:885`), Iterable("**확인 불가(403)**", `:886`). 문서를 열지 못한 곳을 "열어봤다"에 포함시킬 수 없다.
  4. 덧붙여 **본문이 스스로 모순된다** — 93행은 CleverTap("Customer retention platform")·OneSignal("omnichannel messaging")·그루비("마테크 솔루션")·빅인("CRM 자동화")을 자기 규정 사례로 든다. 이들을 라벨로 세면 "넷뿐"이 성립할 수 없다.
- **조치:** 세는 대신 리서치가 실제로 말한 형태(소수·확인된 목록·조회 실패 별도)로 옮긴다. 7행을 아래로 교체.

  > 이 책의 리서치는 마테크 벤더 20곳의 개발자 문서를 훑었다(2026년 7월 기준). 그중 **자기 카테고리를 개발자 문서 첫 화면에 명시한 곳은 손에 꼽는다** — Adobe Real-Time CDP, mParticle, Insider의 UCD가 자기를 "Customer Data Platform"이라 밝혔고, CleverTap이 "Customer retention platform", OneSignal이 "omnichannel messaging"이라 썼다. 이 리서치가 확인한 건 여기까지다. 나머지 대부분은 자기가 무슨 카테고리인지 말하지 않는다. 굳이 말할 이유가 없기 때문이다. 개발자 문서를 읽는 사람은 이미 계약이 끝난 뒤에 온다. (덧붙이면 20곳 중 세 곳은 문서를 여는 것조차 실패했다 — 사이트 오류가 하나, 404가 하나, 403이 하나였다.)

  ※ **확인된 벤더를 이름으로 나열하고 멈춰라.** "다섯이다" 같은 개수 선언도, "나머지 열다섯 곳"이라는 빼기 계산도 하지 않는 게 안전하다. 근거(`web_products.md:886`)가 "…**정도**"라는 한정어로 끝나 정확한 개수를 세는 형태가 아니고, 조회 실패 3곳 때문에 분모도 깨끗하지 않다. 목록은 근거가 뒷받침하지만 개수는 뒷받침하지 않는다.

### 주장 2 — Raab 2013년 명명과 세 단어 해설
- **본문:** (13~18행) "2013년 4월 25일, 마케팅 기술 애널리스트 David Raab이 자기 블로그에 'I've Discovered a New Class of System: the Customer Data Platform'이라는 제목의 글을 올렸다. > 'Customer' shows the scope extends to all customer-related functions, not just marketing; / 'Data' shows the primary focus is on data, **not execution**; and / 'Platform' shows it does more than data management while supporting other systems — David Raab, 2013-04-25"
- **판정:** ✅
- **근거:** 인용문 3줄은 `research/web_products.md:36~38`에 **한 글자까지 일치**(`web.md:42~44`에도 동일 사본). 글 제목·발행일·저자는 `research/web_gaps.md:33~40` — "제목: 'I've Discovered a New Class of System: the Customer Data Platform. Causata Is An Example.' / 저자: David Raab / 발행일: 2013년 4월 25일(목)". 본문이 제목의 부제(Causata 부분)만 생략했는데 인용부호 안 내용이 바뀌지 않았으므로 문제없다. `web_gaps.md:155` 교차 확인: "'2013년 4월'이 Raab 블로그 원문의 발행일(2013-04-25)과 **정확히 일치** → **1차 출처로 뒷받침된 사실로 취급 가능** ✅".
- **조치:** 없음. 20행의 해석("초점은 데이터이지 실행이 아니다")은 인용된 원문 두 번째 줄에서 직접 나온다 ✅.

### 주장 3 — Raab 2015년 정의
- **본문:** (22~27행) "2년 뒤인 2015년 1월 18일 … > 'a marketer-controlled system that builds a multi-source customer database and exposes it to external execution systems' — David Raab, 2015-01-18. 두 글을 나란히 놓으면 무엇이 달라졌는지 보인다(**정의문 자체는 원문이고, 이 비교는 이 책의 관찰이다**). 2013년 정의에 있던 '예측 분석을 수행한다'는 대목이 빠지고…"
- **판정:** ✅
- **근거:** 정의문은 `research/web_gaps.md:71` **한 글자까지 일치**. 발행일 2015-01-18 ✅(`web_gaps.md:64`, `:871`). "2013년 정의에 있던 예측 분석이 빠졌다"는 관찰도 성립한다 — `web_gaps.md:50`이 2013년 최초 정의의 구성요소를 넷으로 정리하며 "③ **결과 DB 위에서 예측 분석**"을 포함시켰고, 2015년 정의문에는 그 요소가 없다.
- **조치:** 없음. **비교가 저술가의 관찰임을 괄호로 명시한 점이 정확하다** — Raab 본인이 "내 정의가 이렇게 바뀌었다"고 쓴 적은 없으므로 관찰로 표기하는 게 맞다.

### 주장 4 — "2015년 정의를 현재 정의처럼 쓰지 마라" 규율 준수
- **본문:** (22행 "2년 뒤인 2015년 1월 18일", 33행 "**2018년 Raab 기준**이며, 지금으로부터 8년 전 분류다", 176행 "정의의 무게중심이 **2015년에** 'marketer-controlled'로 옮겨간 이야기가 **10년 뒤** 인프라 배치의 문제로 되돌아온 셈이다")
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_gaps.md:901`이 이 장에 걸린 가장 중요한 규율이다 — "역사적 1차 기록(2013~2024, Raab 블로그): 오래된 것이 결함이 아니다 … 단 **'2013년 당시의 정의'임을 본문에 반드시 명시할 것. 특히 2015년 정의를 현재 정의처럼 쓰면 안 된다.**" 본문은 Raab을 인용하는 **모든 지점에 연도를 붙였고**(2013-04-25 / 2015-01-18 / 2017-03-23 / 2018-11-03), 176행에서는 2015년 정의를 현재로 끌어올 때 "10년 뒤"라는 시간 간격을 명시해 현재 정의로 오독될 여지를 없앴다. `02_plan.md:222`의 "Raab 정의 — 연도 병기(2013/2015/2018)" 요구를 **네 연도로 초과 이행**.
- **조치:** 없음.

### 주장 5 — Raab 2018년 3분류 (최우선 검증 항목)
- **본문:** (33~35행) "2018년 11월 3일 글에서 Raab은 CDP를 세 유형으로 나눈다. **2018년 Raab 기준**이며, 지금으로부터 8년 전 분류다. **Data CDP**('CDPs with a customer database'), **Analytics CDP**('CDPs with a customer database plus customer analytics'), **Personalization CDP**('a customer Database, analytics, and personalization'). … 다른 자료에서 이 목록이 넷으로 늘어난 형태를 보더라도, 이 책은 원문에서 확인한 셋만 쓴다."
- **판정:** ✅ (금지 항목 1번의 정확한 이행 — 이 장의 최고 위험 지점이 깨끗하다)
- **근거:** `research/web_products.md:186~200` §A-2.
  - 출처: "글 제목: 'Why Are There So Many Types of Customer Data Platforms? It's Complicated.' / **저자·발행일: David Raab, Saturday, November 03, 2018**" ✅ — 본문의 "2018년 11월 3일"과 일치.
  - 3유형 원문 조각 — Data CDP "CDPs with a customer database" / Analytics CDP "CDPs with a customer database plus customer analytics" / Personalization CDP "a customer Database, analytics, and personalization" — **세 인용 모두 한 글자까지 일치**(대문자 `Database` 표기까지 동일).
  - `web_products.md:204`: "**task가 준 4분류와 다르다.** … 이 2018년 글에서 확인된 세 번째 유형은 '**Personalization CDP**'이며, '**Campaign CDP**'·'**Delivery CDP**'라는 용어는 **이 글에 등장하지 않는다**(WebFetch가 명시적으로 확인)." → 본문은 Campaign·Delivery를 쓰지 않았다 ✅
  - `web_products.md:213`: "⚠️ **8년 전 분류다.** … 반드시 '**2018년 Raab 기준**'을 병기하라." → 본문 33행이 굵은 글씨로 병기했고 "8년 전"까지 그대로 반영 ✅
  - 개발자용 해설("레이어가 쌓이는 순서 — 데이터베이스만 있는가 / 그 위에 분석이 있는가 / 그 위에 실행까지 있는가")도 `web_products.md:215`의 리서처 해설과 일치 ✅
- **조치:** 없음. **35행 마지막 문장("다른 자료에서 이 목록이 넷으로 늘어난 형태를 보더라도, 이 책은 원문에서 확인한 셋만 쓴다")은 이 책 전체에서 가장 값진 한 줄이다** — 독자가 다른 데서 4분류를 만났을 때 이 책이 실수한 게 아님을 알려주고, 후속 편집에서 4분류가 되살아나는 것도 막는다.

### 주장 6 — Raab 2018년 "공룡" 인용과 "persistent, sharable" 인용
- **본문:** (39~41행) "> 'CDPs are not simple: the industry has rapidly evolved numerous subspecies of CDPs that are as different from each other as the different kinds of dinosaurs.' … 그러면서 그는 못 박는다 — 'For CDP to have any meaning, it must describe a system whose primary purpose is to build a **persistent, sharable** customer database.'"
- **판정:** ✅ (금지 항목 2번과 혼동될 수 있는 지점이라 별도로 정밀 대조했다)
- **근거:** 두 인용 모두 `research/web_products.md:201, 203`에 **한 글자까지 일치**하며, 출처는 같은 2018-11-03 글이다(`web_products.md:205` URL: `customerexperiencematrix.blogspot.com/2018/11/why-are-there-so-many-types-of-customer.html`).
  **금지 항목 4번과의 구분이 핵심이다.** 금지된 것은 **CDP Institute의 기관 정의문** "persistent, **unified** customer database that is accessible to other systems"(`web_gaps.md:125`, `web_products.md:73`)다. 본문이 쓴 것은 **Raab 개인 블로그의** "persistent, **sharable** customer database"로 **다른 문장**이며, 리서치가 실제로 fetch한 원문이다. 기억에 의한 복원이 아니다 ✅.
  "5년 만에"(41행)도 2013→2018로 정확하다 ✅.
- **조치:** 없음.

### 주장 7 — 기관 정의문 배제 선언
- **본문:** (43행) "이 절의 인용은 전부 **명명자 개인의 블로그**에서 왔다. 이 분야에는 기관 이름을 단 정의문도 널리 회자되지만, 그 기관 사이트는 리서치 시점(2026년 7월)에 접근이 막혀 원문을 확인하지 못했다. 그래서 이 책은 기관 정의문을 쓰지 않는다."
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_gaps.md:848` — "**CDP Institute 공식 정의(1차)** | 확인 불가 — 2차 인용만 확보 | Raab 1차 원문(1-A/1-B)으로 **대체 권장**". `web_products.md:73` — "'CDP Institute는 CDP를 ~라고 정의한다'라는 문장을 쓰려면 별도 확인이 필요하다. **기억으로 문장을 복원해 넣지 마라.** … 대신 '**CDP라는 용어를 만든 David Raab은 ~라고 썼다**'로 쓰면 §A-0의 원문으로 뒷받침된다." `web_gaps.md:129`도 "**1-A/1-B의 Raab 1차 원문으로 대체** ← **권장**". 본문은 대체를 실행했을 뿐 아니라 **대체했다는 사실과 그 이유를 독자에게 공개**했다. `02_plan.md` 금지 4번("Raab 개인 정의로 대체하되 둘을 섞어 쓰지 마라") 완전 이행.
- **조치:** 없음.

### 주장 8 — Raab 2017년 3질문과 비교표
- **본문:** (47~63행) 세 질문(고객 데이터를 통합하는가 / 다른 시스템이 그 데이터를 읽게 하는가 / 메시지를 고르는가) + 7행 비교표 + "> 이 표는 Raab의 2017년 벤 다이어그램과 산문 서술을 표로 재구성한 것이다. **원문은 표 형태가 아니다.**"
- **판정:** ✅ (재구성 고지가 필수였던 지점 — 이행 확인)
- **근거:** `research/web_gaps.md:79~106` §1-C.
  - 발행일 2017-03-23 ✅(`web_gaps.md:86`, `:872`), 글 제목 "Wondering How Customer Data Platforms Relate to Other Marketing Systems? Here's a Picture".
  - 세 축 — "1. Unifying customer data 2. Making data accessible to other systems 3. Selecting messages" ✅ 본문 49~51행과 일치.
  - 표 7행(CDP ✅✅❌ / JOE ✅❌✅ / MDM ✅❌❌ / MAP ❌❌✅ / DMP ❌❌✅ / CRM ❌❌✅(영업 중심) / Data Lake ❌✅❌) — `web_gaps.md:94~104`와 **전건 일치**. 원표의 8행째 ECDP는 세 칸이 모두 "—"라 본문에서 뺀 것이 정보 손실이 아니다.
  - **재구성 고지:** `web_gaps.md:106` — "⚠️ 이 표는 fetch한 페이지의 서술을 정리한 것이지만, **표 형태는 원문 그대로가 아니라 이 리서처의 재구성이다.** 원문은 **벤 다이어그램 이미지와 산문 서술**이다. 책에 표로 옮길 때 '**Raab의 2017년 벤 다이어그램을 표로 재구성**'이라고 명시할 것." → 본문 63행이 **지시된 문구 그대로** 명시했다 ✅
- **조치:** 없음.

### 주장 9 — CRM 스키마 (Salesforce Trailhead)
- **본문:** (69행) "Salesforce의 공식 학습 문서를 열면 네 객체가 나온다. Account(거래하는 회사), Contact(그 회사에서 일하는 사람), Lead(아직 자격 검증이 안 된 잠재 고객), Opportunity(자격 검증을 통과해 전환된 건). 그리고 결정적인 규칙 — **Lead를 전환(convert)하면 Account·Contact·Opportunity 세 레코드가 한꺼번에 만들어진다.**"
- **판정:** 🕒 신선도 경고 (내용 ✅, 조회 시점 누락 — 01장 주장 6과 같은 성격)
- **근거:** 내용은 `research/web_gaps.md:234` 원문("Opportunities are qualified leads that you've converted. **When you convert the Lead, you create an Account and Contact along with the Opportunity.**")과 `web_gaps.md:238` 해설("Lead 변환 모델 … CRM이 왜 '고객 DB'가 아니라 '**영업 파이프라인 DB**'인지 보여주는 핵심")에 정확히 대응한다 ✅. **시점만 없다.** `web_gaps.md:903`: "Trailhead·Salesforce 개발자 문서 … 는 페이지에 발행일이 없다. 전부 '**2026-07-25 조회 기준**'으로만 표기할 것." `web_gaps.md:879`: 발행일 "미표기", 조회 2026-07-25.
- **조치:** 69행 첫 문장에 시점을 넣는다.

  > **CRM은 고객 DB가 아니라 영업 파이프라인 DB다.** Salesforce의 공식 학습 문서를 열면(2026년 7월 조회 기준 — 이 페이지들에는 발행일 표기가 없다) 네 객체가 나온다.

  ※ 71행의 MA 서술("같은 문서 계열에서 확인되는")도 같은 출처이므로 이 한 번의 시점 표기가 함께 커버한다.

### 주장 10 — MA의 score / grade 2축
- **본문:** (71행) "같은 문서 계열에서 확인되는 개념이 score와 grade다. score는 숫자로 '얼마나 관심을 보였나'를, grade는 문자(A·B·C…)로 '우리가 그리는 이상적인 고객상에 얼마나 맞나'를 나타낸다. **행동과 속성을 일부러 분리해 각각 채점한 뒤 조합한다.**"
- **판정:** ✅
- **근거:** `research/web_gaps.md:386` — "**score(행동, 숫자) + grade(적합도, 문자)**" [FETCHED: Trailhead]. `web_gaps.md:852`도 "리드 스코어링 정의 → ✅ **해소됨** — Trailhead에서 score/grade 2축 확보". 본문의 두 축 설명(행동↔숫자 / 적합도↔문자)이 근거와 정확히 대응한다.
- **조치:** 없음(시점은 주장 9의 조치로 함께 해소).

### 주장 11 — Adobe DMP 자기 규정
- **본문:** (73행) "Adobe의 DMP 제품 문서(**2026년 5월 갱신 표기**)는 자기를 '**online audience data management**' 서비스로 소개하고, 대상 사용자를 '**digital advertisers and publishers**'라고 밝힌다. 자사 고객 프로필을 다루는 CDP와 대상도 목적도 다르다는 **간접 근거**가 여기서 나온다."
- **판정:** ✅
- **근거:** 인용구는 `research/web_products.md:248`("an industry-leading service for **online audience data management**")과 `web_products.md:258`("대상 독자를 '**digital advertisers and publishers**'라고 밝힌 것은 확인했다"). 문서 시점은 `web_products.md:256` — "문서 표기 '**last update May 21, 2026**'" → 본문의 "2026년 5월 갱신 표기" ✅.
- **조치:** 없음. **"간접 근거"라는 단어를 쓴 것이 정확하다** — `web_products.md:258`이 바로 그 표현을 썼다: "이건 CDP(자사 고객 프로필 중심)와 대상·목적이 다르다는 **간접 근거**는 된다." 근거 등급을 원문 그대로 옮겼다.

### 주장 12 — DMP 행의 출처 충돌 병기
- **본문:** (77행) "**DMP 행에서 두 출처가 정면으로 충돌한다.** 위 표는 애널리스트 분류라서 DMP를 '데이터를 통합하지 않는다'로 놓는데, 방금 인용한 Adobe 문서는 자사 DMP가 여러 소스의 오디언스 프로필을 만든다고 말한다. **어느 쪽이 맞는지 판정할 근거가 없어서 둘을 나란히 적어둔다.**"
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_gaps.md:794` — "**정면 충돌이다.** 둘 다 1차 출처에서 나왔다 … **판정하지 마라.** 이건 martech 카테고리 논쟁의 전형 — 애널리스트가 카테고리 경계를 좁게 긋고, 벤더는 자기 제품을 넓게 규정한다. 개발자 독자에게 '**카테고리 이름을 믿지 말고 기능을 확인하라**'는 교훈의 실물 사례로 쓰기에 최적이다." Adobe 쪽 근거는 `web_gaps.md:792`("**Unifies data into audience profiles**"), Raab 쪽은 `web_gaps.md:791`. 본문은 판정을 유보하고 병기했으며, 나아가 "애널리스트가 그은 경계와 벤더의 자기 규정이 다르다는 사실 자체가 이 장이 말하려는 것의 증거다"로 리서치가 제안한 각도까지 살렸다.
- **조치:** 없음. (`web_gaps.md:794`가 덧붙인 미세 구분 — "Adobe 쪽은 페이지 본문의 **축자 인용**이고, Raab 2017 쪽은 원문의 **벤 다이어그램 이미지를 fetch 요약으로 옮긴 것**이다. 충돌 자체는 실재하지만 양쪽을 똑같이 '인용문'으로 취급하지는 마라" — 본문은 Raab 표를 "재구성"으로, Adobe를 직접 인용으로 이미 다르게 표기했으므로 충족된다 ✅.)

### 주장 13 — "등장 시점" 행 부재
- **본문:** (79행) "**'등장 시점' 행은 아예 만들지 못했다.** 1차 소스로 확정한 연대는 CDP의 2013년 4월 하나뿐이고, CRM·DMP·MA가 언제 생겼는지는 블로그마다 다른 답을 내놓았다."
- **판정:** ✅
- **근거:** `research/web_gaps.md:388` 「등장 시점」 행 — CRM **확인 불가** / DMP **확인 불가** / CDP "**2013년 4월 명명**" [FETCHED: Raab 원문 + Wikipedia 교차 확인] ✅ / MA **확인 불가** / CEM **확인 불가**. 즉 5칸 중 확정된 것은 CDP 하나뿐 ✅ 본문 서술과 정확히 일치.
- **조치:** 없음.

### 주장 14 — CEM/CXM 배제와 DMP 통설 배제
- **본문:** (81행) "**CEM/CXM은 이 표에 들어오지 못했다.** 1차 정의를 확보하지 못해서다. … 같은 이유로, DMP와 CDP를 **데이터의 출처 종류**로 갈라 설명하는 통설도 이 책은 쓰지 않는다. 어떤 1차 소스로도 확인하지 못했고, **Adobe의 DMP 문서에는 쿠키나 익명 데이터에 대한 언급 자체가 없었다.**"
- **판정:** ✅ (금지 항목 2·3번의 정확한 이행)
- **근거:** `research/web_gaps.md:203~205` — "⚠️ **확보 실패:** 이 페이지에는 **쿠키·디바이스 ID·익명 프로필에 대한 언급이 없다.** 따라서 '**DMP는 서드파티 쿠키 기반이다**'라는 문장을 Adobe 공식 문서로 뒷받침할 수 없다. / 🚨 **fact-checker 필독:** 'DMP = 서드파티 쿠키 기반, 익명 세그먼트'는 업계에서 사실상 상식이지만, **이 세션에서 1차 벤더 문서로 확인하지 못했다.**" `web_products.md:258`도 "**쓰지 마라**". CEM/CXM은 `web_products.md:230`(A-3: "대부분 **확인 불가(1차 소스 미확보)**")와 `02_plan.md:191`("Gartner 403으로 열 전체가 비어 있다"). 본문은 배제했을 뿐 아니라 **배제 사유를 근거 수준까지 설명**했고, "확인되지 않았다는 게 틀렸다는 뜻은 아니다"라는 인식론적 단서까지 붙였다.
- **조치:** 없음.

### 주장 15 — API 카탈로그 대비 (Airbridge vs Insider)
- **본문:** (89~91행) "어트리뷰션 제품인 Airbridge의 API 목록에는 `Attribution Result`와 `Tracking Link`가 있다. Insider의 목록에는 없다. 반대로 Insider의 목록에는 `Send Transactional Emails`가 있고 Airbridge에는 없다. … > **'없다'는 것은 이 리서치가 연 페이지 범위 안에서만 유효하다.**"
- **판정:** ✅
- **근거:** `research/web_products.md:812` — "Airbridge에만 `Attribution Result` API가 있고 Insider에는 없다. Insider에만 `Send Transactional Emails`가 있고 Airbridge에는 없다. **API 카탈로그를 나란히 놓으면 카테고리 경계가 마케팅 문구보다 선명하다.** 이게 개발자 독자에게 카테고리를 설명하는 가장 좋은 방법이다." 엔드포인트 실재는 `web_products.md:881`(Airbridge 행: Tracking Link, S2S Event, **Attribution Result**, SKAdNetwork Config, Raw Data Export)과 `web_products.md:476`(Insider **Send Transactional Emails**)로 각각 확인 ✅.
- **조치:** 없음. **91행의 단서 문단이 이 장의 방법론적 정직성을 지탱한다** — 02장 31행과 같은 취지의 방어이며, 두 장이 일관된다.

### 주장 16 — 벤더 자기 라벨 4종
- **본문:** (93행) "CleverTap은 자기를 '**Customer retention platform**'이라 부르고, OneSignal은 '**omnichannel messaging**'이라고 쓴다. 국내 벤더 중 그루비는 '**마테크 솔루션**', 빅인은 '**CRM 자동화**'라는 표현을 쓴다."
- **판정:** ✅
- **근거:** `research/web_products.md:286` — "확인된 자기 라벨: … '**Customer retention platform**'(CleverTap), '**omnichannel messaging**'(OneSignal), '**마테크 솔루션**'(그루비), '**CRM 자동화**'(빅인)." 표에서도 교차 확인 — `web_products.md:877`(CleverTap), `:878`(OneSignal), `:882`(그루비 "비즈니스 성공을 위한 필수 마테크 솔루션"), `:883`(빅인 "개인화된 CRM 자동화") ✅.
- **조치:** 없음.

### 주장 17 — Airship의 CDP 파트너 취급
- **본문:** (95행) "메시징 벤더 Airship은 CDP를 '파트너 연동' 목록(analytics, CRMs, CDPs, marketing tools)에 넣는다. CDP를 경쟁자가 아니라 **데이터 공급자**로 본다는 뜻이다. 반면 Insider와 Adobe는 CDP를 자기 제품 안에 내장한다."
- **판정:** ✅
- **근거:** `research/web_products.md:287` — "**CDP는 CEP의 부품이기도 하고 경쟁자이기도 하다.** Airship은 CDP를 '파트너 연동' 목록(analytics, CRMs, **CDPs**, marketing tools)에 넣는다 — 즉 **데이터 공급자**로 본다. 반면 Insider·Adobe는 CDP를 자기 안에 내장한다. 같은 카테고리가 누구에게는 부품, 누구에게는 모듈이다." 원 API 표면은 `web_products.md:741`로 확인. 본문 표현("누구에게는 부품이고 누구에게는 모듈")까지 근거와 일치 ✅.
- **조치:** 없음.

### 주장 18 — 국내 벤더 3곳 공개 문서 부재
- **본문:** (97행) "이 리서치가 시도한 국내 벤더 세 곳은 **공개 개발자 문서를 확인할 수 없었다.** 글로벌 벤더는 문서를 공개 자산으로 운영하고 국내 벤더는 계약과 어드민 뒤에 두는 경우가 많았다는 **관찰**인데…"
- **판정:** ✅
- **근거:** `research/web_products.md:891` — "**한국 벤더 3곳(그루비·빅인·다이티) 모두 공개 개발자 문서를 확인하지 못했다.** 글로벌 벤더는 문서를 공개 자산으로 운영하고, 한국 벤더는 계약·어드민 뒤에 둔다. 이 차이가 개발자로 입사할 때 체감하는 첫 번째 문화 차이일 가능성이 높다." 개별 근거: 그루비 `web_products.md:837`("그루비 어드민 로그인 뒤에 있는 것으로 보인다 → 공개 개발자 문서 확인 불가"), 빅인 `:847`, 다이티 `:851`(TLS 인증서 오류).
- **조치:** 없음. **"관찰인데"로 등급을 낮춘 것이 적절하다** — 표본 3곳이므로 일반화가 아니라 관찰이 맞다. (다만 이 3곳은 **주장 1의 "20곳을 열어봤다"와 충돌한다** — 다이티는 사이트 자체가 안 열렸다. 주장 1 조치에 반영했다.)

### 주장 19 — Adobe RTCDP ↔ Journey Optimizer 관계
- **본문:** (103~109행) Real-Time CDP 소개 + Journey Optimizer 정의문 인용 + "Journey Optimizer는 'is built natively on Adobe Experience Platform, sharing its **data foundation, identity graph, and governance services**'라고 쓰여 있다(**문서 표기 2026년 7월 1일**)."
- **판정:** ✅
- **근거:** Journey Optimizer 정의문("An enterprise application for creating and delivering connected, contextual, and personalized customer experiences across all channels and touchpoints.")은 `research/web_products.md:749` **한 글자까지 일치**. 관계 문장은 `web_products.md:750` — "is built natively on Adobe Experience Platform, sharing its data foundation, identity graph, and governance services." **한 글자까지 일치**. 문서 시점은 `web_products.md:751` — "문서 표기 '**Last updated July 1, 2026**'" → 본문 "2026년 7월 1일" ✅. Real-Time CDP 소개(103행)는 `web_products.md:618`("bring together **known and anonymous data** from multiple enterprise sources in order to create customer profiles")의 정확한 한국어 요약 ✅. 109행의 아키텍처 해석도 `web_products.md:753`의 리서처 해설("Real-Time CDP = 데이터 기반(프로필·아이덴티티 그래프), Journey Optimizer = 그 위에서 저니를 실행하는 애플리케이션. **둘이 같은 Experience Platform 데이터 기반을 공유한다.**")과 일치.
- **조치:** 없음.

### 주장 20 — Insider Architect의 간접 확인
- **본문:** (111행) "Insider는 자사 데이터 계층을 UCD라 부르며 '**the core Customer Data Platform (CDP) that powers all Insider One products**'라고 문서에 적어두었고, 저니를 실행하는 제품에는 Architect라는 별도 이름을 붙였다. 다만 **Architect의 개요 문서 페이지는 이 리서치 시점에 열리지 않았고**, 데이터 인입 API 문서의 한 옵션 설명에 '**Architect journeys**'라는 표현이 등장하는 데서 **간접 확인**한 것이다. 그 안에서 어떤 저장소가 돌아가는지는 이 회사가 공개한 자료를 찾지 못했으므로 **추정하지 않는다.**"
- **판정:** ✅ (간접 확인 처리의 모범)
- **근거:** UCD 인용문은 `research/web_products.md:238, 304, 326`에 **세 번 반복 확인**되며 한 글자까지 일치 ✅. Architect는 `web_products.md:604` — "⚠️ **Architect(저니 오케스트레이션) 문서:** `academy.insiderone.com/docs/architect-overview` → **404**. llms.txt에서도 해당 섹션이 잘려 확인 못 함. 다만 **Upsert API의 `skip_hook` 필드 설명에 'Architect journeys'가 등장하므로 Architect가 저니 오케스트레이션 제품명이라는 점은 간접 확인**됨. **세부 기능은 `확인 불가`.**" 필드 실재는 `web_products.md:418`(`skip_hook` — "임포트된 데이터가 Architect 저니를 트리거할지 제어") ✅.
- **조치:** 없음. **404를 만난 사실·간접 확인의 경로·추정하지 않겠다는 선언을 모두 본문에 노출**했다. 리서치의 `확인 불가` 표시를 산문으로 옮기는 가장 좋은 예다.

### 주장 21 — CEP는 벤더의 자기 배치 라벨
- **본문:** (113행) "같은 회사가 회사 차원에서는 자기를 '**Agentic Customer Engagement Platform**'이라 부른다. 제품 문서에서는 데이터 계층을 CDP라 부르고, 회사 소개에서는 CEP라 부른다. **한 회사가 두 카테고리를 동시에 주장하는 것이다.** … CEP라는 라벨의 성격이 드러난다 — 애널리스트가 밖에서 그어준 경계라기보다, **벤더가 자기를 어디에 놓고 싶은지 밝히는 라벨**에 가깝다."
- **판정:** ✅
- **근거:** `research/web_products.md:234`(A-3 CEP 절) — "Insider One: 자사를 '**the leading Agentic Customer Engagement Platform**'으로 규정(벤더 자체 주장)". 그리고 리서처 관찰: "**CEP는 애널리스트가 정의한 카테고리라기보다 벤더가 자기를 배치하는 라벨로 쓰이고 있다.** Insider는 제품 문서에서는 자기 데이터 계층을 'CDP'라 부르면서, 회사 전체는 'Customer Engagement Platform'으로 규정한다. **이 이중 라벨링 자체가 '카테고리 경계가 왜 흐릿한가'의 실증 사례다.**" 본문이 이 관찰을 거의 그대로 서사화했다 ✅. `web_products.md:866` 표에서도 교차 확인.
- **조치:** 없음. (같은 절이 기록한 부정 확인 — Braze 문서에는 "customer engagement platform"이라는 자기 규정 문장이 **없었다(NOT FOUND)** — 은 본문이 쓰지 않았다. 안전한 생략.)

### 주장 22 — Hightouch 마케팅 주장과 컴포저블 정의
- **본문:** (121~127행) "> 'Don't copy your data to an incompatible and less secure data silo. Turn your existing data into a CDP instead.' / 'Hightouch doesn't store your data. Instead we simply read from your data warehouse where it stays safe and sound.' … 같은 회사가 **2023년 6월**에 올린 글은 컴포저블 CDP를 '이미 갖고 있는 데이터 인프라에서 곧바로 마케팅 용례를 구동하게 해주는 CDP'로 정의한다. **어디까지나 벤더 자신의 주장이다.**"
- **판정:** ✅
- **근거:** 두 인용문은 `research/web_products.md:109, 111` **한 글자까지 일치**(제품 페이지 A-1-b, 발행일 미표기·조회 2026-07-25). 컴포저블 정의는 `web_products.md:95` 원문 — "A Composable CDP is a customer data platform that enables you to use any data in your organization to power marketing use cases like audience management, journey orchestration, personalization, and data activation **directly from your existing data infrastructure**." 본문의 한국어 압축("이미 갖고 있는 데이터 인프라에서 곧바로 마케팅 용례를 구동하게 해주는 CDP")이 원문 구조를 정확히 옮겼다 ✅. 발행일은 `web_products.md:102` — "저자 Luke Kline, **발행 2023-06-20**" → 본문 "2023년 6월" ✅.
  ※ `web_products.md:149`의 "'composable CDP'의 명시적 정의문은 이 글에 **없음(NOT FOUND)**" 경고는 **다른 문서**(A-1-d, Google Cloud 엔지니어링 블로그)에 걸린 것이다. Hightouch 블로그 정의문과 혼동하지 않도록 확인했다.
- **조치:** 없음. **"어디까지나 벤더 자신의 주장이다"** 한 줄이 근거 등급을 정확히 표시한다.

### 주장 23 — Salesforce Data 360 / Data Cloud 이름 공존
- **본문:** (131행) "Salesforce의 고객 데이터 제품 문서는 자기 아키텍처를 '**designed to ingest, process, unify, and activate customer data from various sources**'라고 소개한다. … (2026년 7월 조회 시점의 개발자 문서는 이 제품을 **Data 360**으로 표기하는데 URL 경로와 일부 섹션 제목에는 **Data Cloud**가 남아 있다. **개명 사건으로 서술할 근거는 확인하지 못했으니 두 이름이 함께 쓰인다는 사실만 적어둔다.**)"
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_gaps.md:673` 원문 — "Data 360's architecture is designed to **ingest, process, unify, and activate** customer data from various sources." **한 글자까지 일치**. `web_gaps.md:659~661` — "**중요한 발견: 제품명이 'Data 360'으로 바뀌었다** … 2026-07-25 시점 Salesforce 개발자 문서는 이 제품을 '**Data 360**'이라 부른다. `data-cloud`가 **URL 경로에는 아직 남아 있다.**" 그리고 `web_gaps.md:357`이 처리 방침을 지시한다 — "**개명 시점은 확인 불가** — Data 360 건과 동일하게 처리할 것". 본문은 개명 시점·개명 사실을 단정하지 않고 **두 표기가 공존한다는 관측만** 적었다 ✅.
- **조치:** 없음. (참고: `web_products.md:885`의 20벤더 표에는 Salesforce Data Cloud가 "확인 불가(문서 404/렌더 실패)"로 남아 있는데, 이는 **앞선 리서처의 실패 기록**이고 `web_gaps.md`가 Data 360 경로로 **우회 확보**했다. 본문은 확보된 쪽을 인용했으므로 정확하다.)

### 주장 24 — 마케팅 페이지 vs 개발자 문서의 톤 차이
- **본문:** (159행) "**위에 인용한 강한 아키텍처 주장들은 전부 마케팅 페이지에 있었고, 같은 회사의 개발자 문서에는 그런 문장이 없었다.** 개발자 문서는 Source가 무엇이고 Sync가 무엇인지만 담담하게 설명한다."
- **판정:** ✅
- **근거:** `research/web_products.md:139` — "⚠️ 이 문서 페이지에는 '데이터가 웨어하우스에 남는다 / 복사하지 않는다'는 **명시적 문장이 없었다**(제품 마케팅 페이지에만 있음). **문서와 마케팅 페이지의 톤 차이 자체가 관찰 가치가 있다.**" `web_products.md:1131`도 "마케팅 페이지: 'Hightouch doesn't store your data' (강한 주장)"으로 구분해 기록. 리서치가 "관찰 가치가 있다"고 지목한 지점을 본문이 장 전체의 논지(카테고리는 세일즈 자료에 산다)와 이어붙였다 ✅.
- **조치:** 없음.

### 주장 25 — Hightouch 4개념 (Source/Model/Sync/Destination)
- **본문:** (163~174행) 4개념 표 + Sync 모드·스케줄 해설. "Hightouch의 개발자 문서(**페이지 표기 2026년 7월 17일**)"
- **판정:** ✅
- **근거:** `research/web_products.md:120~134` §A-1-c 원문과 대조.
  - Source "A source is **any system where your data resides**. Common examples include Snowflake, BigQuery, Databricks, and PostgreSQL." → 본문 인용구·예시 4종 일치 ✅
  - Model "A model **defines what data to query from a source**. Models can represent users, events, products, or any other entity." → 본문 "사용자·이벤트·상품 어느 것이든" ✅
  - Sync "A sync **defines how data appears in the destination and when**. … Mode: **insert, update, upsert, or archive** … Schedule: **interval, cron, or triggered** by tools like dbt Cloud or Airflow" → 본문 표의 모드 4종·스케줄 3종 ✅
  - Destination "A destination is **any system where data is consumed** — CRMs, ad platforms, support tools, analytics, or custom APIs." → 본문 "CRM·광고 플랫폼·지원 도구·자체 API" ✅
  - 시점: `web_products.md:134` "페이지 표기 '**Last updated Jul 17, 2026**'" → 본문 "페이지 표기 2026년 7월 17일" ✅
  - 174행 해설(upsert/archive 병존 → 삭제가 일급 시나리오, 스케줄에 크론·외부 트리거 → 오케스트레이션의 일부)은 원문 명세에서 직접 도출되는 읽기다 ✅
- **조치:** 없음. **금지 항목 6번(Tier 2 버전·수치) 회피 확인** — Snowflake·BigQuery·Databricks가 등장하지만 **버전도 수치도 붙지 않았고**, 원문 인용 안의 예시 나열일 뿐이다 ✅.

### 주장 26 — HN 2021-11 스레드와 두 실무자 인용
- **본문:** (180~192행) "**2021년 11월 Hightouch 제품 런칭 시점의 해커뉴스 스레드**(댓글 47개)다. 아래 발언은 전부 이 한 스레드에서 나왔고, **5년 가까이 지난 스냅숏**이라는 점을 먼저 밝혀둔다." + 웨어하우스 우선 실무자 인용 + "SQL 작성자가 어떤 SQL을 써야 하는지는 어떻게 아나?" 반박 + 벤더 답변 "**still early days there**"
- **판정:** ✅
- **근거:** 스레드 메타는 `research/community.md:949` — "Hightouch Launch HN 스레드(objectID **29188544**, **2021-11-11**, **댓글 47개**)" ✅, 신선도 원장 `community.md:1185`에도 동일.
  - 첫 인용(184행)은 **HN 29190721 / pinkbeanz** — 원문 "once you get into complex workflows that merge data across your product and CRMs **it all moves to the warehouse first**… Once in the warehouse, it needs to get back into those operational systems again, **which is the tricky part. I've done these one off integrations from the warehouse into Salesforce**". 본문 번역이 `community.md:955`의 리서처 번역과 **일치** ✅
  - 둘째 인용(190행)은 **HN 29191935 / tomnipotent** — 원문 "Implicit mapping between SQL to target is great, but **how does the SQL author know what SQL to write in the first place?** I've done no shortage of integrations like this, and **there is no avoiding reading the target SaaS documentation** … **Without that step, I can't even start writing SQL.**" 본문 번역이 `community.md:985`의 리서처 번역과 **일치** ✅
  - 벤더 답변(192행): `community.md:987` — "(벤더 tejasmanohar의 답변은 'declarative이고 docs·autocomplete·schema discovery로 돕는다, **still early days there**'였다 — 즉 **완전히 해결되지 않았음을 인정**.)" ✅
  - "5년 가까이 지난 스냅숏"(2021-11 → 2026-07 = 4년 8개월) ✅ 정확
  - "아래 발언은 전부 이 한 스레드에서 나왔고" — pinkbeanz·tomnipotent·soumyadeb·tejasmanohar 4인 모두 스레드 29188544 소속 ✅(`community.md:1185~1193`)
- **조치:** 없음. **단일 스레드 표본임과 시점 경과를 먼저 고지한 것이 정확하다** — `community.md:601`이 같은 스레드의 다른 발언에 대해 "⚠️ **2021-11 시점 진술이다. 2026년 현재 수치로 쓰면 안 된다.** `🕒 시점 주의`"를 걸어둔 것과 같은 취지다. (선택 사항: 01장이 HN 댓글 번호를 병기했으므로 여기도 `HN 29190721`·`HN 29191935`를 붙이면 장 간 인용 형식이 통일된다.)

### 주장 27 — "두 진영으로 갈렸다"고 쓰지 않는다는 선언
- **본문:** (194~196행) "이 책은 '**업계가 패키지형과 컴포저블 두 진영으로 갈렸다**'는 식으로 쓰지 않는다. … 이 리서치가 커뮤니티를 뒤진 범위 안에서는 **그 프레이밍 자체로 큰 논쟁이 붙은 적이 없었다.** 컴포저블을 주장하는 글은 거의 전부 벤더가 올린 것이었고 **대부분 1~2점을 받고 묻혔다.** 실질적인 토론이 붙은 건 제품 런칭 스레드 하나뿐이다."
- **판정:** ✅ (모범 사례)
- **근거:** `research/community.md:969` — "⚠️ `관찰 사실`: **컴포저블/웨어하우스 네이티브를 주장하는 글은 거의 전부 벤더가 올렸고, HN에서 토론이 붙지 않았다. 실질 토론이 붙은 건 제품 런칭 스레드(29188544)뿐이다.**" 점수 근거는 `community.md:965~968` — hightouch.io 글 **2 points**, fivetran.com 글 **1 point**, rudderstack.com 글 **1 point**. `community.md:1006`도 "'패키지형 vs 컴포저블'이라는 프레이밍 자체로 HN에서 큰 논쟁이 붙은 적은 **이 조사 범위에서 발견되지 않았다.** … 이 프레이밍은 **벤더·애널리스트 담론에서 더 뜨겁고, 실무자 커뮤니티에서는 제품 단위로 이야기된다**는 게 이 표본의 인상이다." 본문 196행("진영 대립은 벤더와 애널리스트의 담론에서 더 뜨겁고, 실무자들은 진영이 아니라 구체적인 마찰로 말한다")이 이 판정을 그대로 반영 ✅.
- **조치:** 없음. **쓰고 싶은 서사를 근거가 없다는 이유로 명시적으로 포기한 대목이다.** 이 파 전체에서 가장 규율적인 판단.

### 주장 28 — 창업자 둘의 축 정의
- **본문:** (198행) "RudderStack 쪽은 자사 포지셔닝이 '**end to end customer data infrastructure**'에 맞춰져 있다고 했고, Hightouch 쪽은 '**RudderStack은 번들이고 그럴 자리가 있다**'며 자기는 액티베이션에만 집중한다고 답했다. **양쪽 다 벤더의 말이지만**, 번들이냐 단일 기능이냐가 이 시장의 실제 축이라는 건 당사자들이 서로 인정한 셈이다."
- **판정:** ✅
- **근거:** `research/community.md:997` (HN 29195773 / soumyadeb / RudderStack 창업자 / 2021-11-12) — "Our positioning, go-to-market, pricing, use cases etc are centered around **building the end to end customer data infrastructure.**" ✅ / `community.md:999` (HN 29196143 / tejasmanohar / Hightouch 창업자 / 2021-11-12) — "**Agree RE: focus. Rudderstack is a bundle and there is a place for that.** Hightouch is 100% focused on activating data from the warehouse…" ✅ 두 인용 모두 정확. `community.md:995`의 리서처 판단("`양쪽 다 벤더`지만, **번들 vs 단일 기능이라는 이 시장의 축을 당사자들이 정의한 대목**이라 인용 가치가 있다")과 본문 결론이 일치하며, 본문도 "양쪽 다 벤더의 말이지만"으로 등급을 표시했다 ✅.
- **조치:** 없음.

### 주장 29 — Fivetran의 Census 인수
- **본문:** (204행) "**2025년 5월 1일**, 데이터 통합 회사 Fivetran이 리버스 ETL 회사 Census를 인수한다고 발표했다. 보도자료는 Census를 '**the leader in Reverse ETL, data activation, and operational analytics**'라고 소개하고 **거래 조건은 공개되지 않았다**고 밝힌다. 2026년 7월 시점에 `getcensus.com` 도메인은 `fivetran.com`으로 리다이렉트된다. **다만 리다이렉트만으로 브랜드나 제품이 완전히 사라졌다고 단정할 수는 없다 — 확인된 것은 발표 사실과 도메인 이동까지다.**"
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_products.md:174` — Census 설명 원문 "**the leader in Reverse ETL, data activation, and operational analytics**" ✅. `web_products.md:176` — "거래 조건: '**Terms of the deal were not disclosed.**'" ✅. 발표일은 `web_products.md:178` — "발표 **2025-05-01**" ✅. 그리고 `web_products.md:181`이 정확히 본문의 단서를 지시한다 — "Census는 2025-05-01 Fivetran 인수 발표 이후 독립 브랜드로 존속하지 않는 것으로 보인다(**도메인 리다이렉트로 확인**). 다만 **Census 브랜드의 완전 소멸 여부는 `확인 불가` — 리다이렉트만으로는 제품 단종을 단정할 수 없다.**" 본문이 이 경계를 그대로 지켰다 ✅.
- **조치:** 없음. (같은 항목의 "확인 불가"들 — Census 창업연도 2018·본사 샌프란시스코·직원 수·CEO 이름(`web_products.md:183`) — 은 본문이 전혀 쓰지 않았다 ✅.)

### 주장 30 — Rokt의 mParticle 합병
- **본문:** (206행) "비슷한 시기에 커머스 광고 회사 Rokt가 CDP 벤더 mParticle을 '**$300 million merger**'로 합쳤다(**발표일은 1차 자료에서 확인하지 못해 적지 않는다**). 결과는 달랐다. mParticle은 문서 사이트가 살아 있고 여전히 자기를 '**a customer data platform (CDP)**'라고 규정한다."
- **판정:** ✅
- **근거:** 금액 표기는 `research/web_products.md:663` — "mParticle 공식 뉴스룸: '**$300 million merger**'(원문 표기)" ✅, `web_products.md:285`도 동일. 발표일 부재는 `web_products.md:1140` — "1차(mparticle.com 뉴스 페이지): **발표일 NOT FOUND**, 금액 '$300 million merger'"와 `web_products.md:1257`("발행일 미표기(금액 $300M만 확인)") ✅ — 본문이 **적지 않는 이유를 괄호로 밝힌** 처리가 정확하다. 자기 규정 존속은 `web_products.md:869` 표 — "mParticle (by Rokt) | '**a customer data platform (CDP)**'" ✅.
- **조치:** 없음.

### 주장 31 — "Modern Data Stack" 실무자 관측
- **본문:** (206행) "한 실무자는 **2025년 10월** 이 흐름을 이렇게 요약했다 — '**The whole Modern Data Stack has either died, acquired or merged by now.**' **개인의 관측이니 업계의 결론으로 격상할 말은 아니지만**, 실무적 함의는 분명하다."
- **판정:** ✅
- **근거:** `research/community.md:569` — "**HN 45571435 / knes / 2025-10-13** / story: 'A16Z-backed data firms Fivetran, dbt Labs to merge in all-stock deal'" — 인용문 **한 글자까지 일치**, 날짜 2025-10-13 → 본문 "2025년 10월" ✅. 근거 등급도 `community.md:571`과 일치 — "`커뮤니티 주장(검증 필요)` — 'Modern Data Stack이 다 죽거나 인수됐다'는 **개인 관측이다.** … **사건은 사실, 해석은 주장.**" 본문의 "개인의 관측이니 업계의 결론으로 격상할 말은 아니지만"이 이 구분을 그대로 옮겼다 ✅.
- **조치:** 없음. (`community.md:571`의 추가 경고 — "두 M&A의 **1차 소스(보도자료)는 미조회**" — 는 Fivetran–dbt Labs 합병 건에 걸린 것이고, 본문은 그 합병을 언급하지 않았다. Census 건은 별도로 1차 보도자료를 확보했다(주장 29) ✅.)

### 주장 32 — 장 전체의 "20곳" 되풀이 여부
- **본문:** (7행 외) 20곳 표본에 기대는 서술이 89행(Airbridge/Insider)·93행(자기 라벨)·95행(Airship)·97행(국내 3곳)에 분산
- **판정:** ⚠️ 근거 약함 (개별 사실은 전부 ✅이나, 표본의 성격 고지가 오프닝 한 곳에만 있고 그마저 틀렸다)
- **근거:** 89·93·95·97행의 개별 사실은 주장 15~18에서 전건 확인됐다. 문제는 이 관찰들이 모두 **같은 20곳 표본**에서 나왔고, 그 표본이 **무작위 추출이 아니라 리서처가 접근 가능했던 벤더 목록**이라는 점이다. 리서치도 이를 "이 세션에서 확인한 벤더 전수"(`web_products.md:862`)라고만 표현하지 시장 대표성을 주장하지 않는다. 본문은 91행에서 "'없다'는 것은 이 리서치가 연 페이지 범위 안에서만 유효하다"는 방어를 **API 카탈로그에만** 걸어두었는데, 같은 방어가 93·95·97행에도 필요하다.
- **조치:** 주장 1의 오프닝 수정에서 "훑었다(2026년 7월 기준)"로 시점과 범위를 명시하면 대부분 해소된다. 추가로 97행 끝에 한 문장을 덧댄다.

  > …입사 전에 제품을 파악하려는 개발자에게는 꽤 난감한 차이가 된다. 다만 이건 스무 곳 남짓을 열어본 표본에서 나온 인상이지 국내 벤더 전체를 센 결과가 아니다.

---

### 03장 요약

**BLOCKING 항목 (Phase 5 진행 차단):**
- ❌ 주장 1 — 오프닝(7행)의 "20곳 / 넷뿐 / 열여섯 곳". 근거는 5곳이고 그마저 "정도"로 한정돼 있으며, 20곳 중 3곳은 문서 조회 자체가 실패했다.

**해소 필요 (🕒):** 주장 9 — Trailhead 인용 조회 시점 누락(01장·02장과 동일 성격, 셋을 함께 수정).

**수정 요망 (⚠️):** 주장 32 — 20곳 표본의 대표성 고지를 오프닝 외에도 한 곳 보강.

**금지 항목 위반:** **0건.** 이 장은 금지 항목이 가장 많이 걸리는 장인데(CDP 4분류·기관 정의문·DMP 통설·CEM/CXM·Raab 연도 병기·Tier 2 수치) 전부 통과했고, 그중 넷은 **본문에서 배제 사유까지 밝혔다.**

**총평:** 인용 정확도는 사실상 만점이다 — Raab 4개 연도의 정의문이 연도별로 정확히 분리돼 있고, "persistent, **sharable**"(Raab)과 "persistent, **unified**"(CDP Institute)의 위험한 유사 문장 함정도 피했다. 404·403·재구성·간접 확인·판정 유보를 전부 본문에 노출한 것도 이 책이 1장에서 약속한 규칙의 이행이다. 유일한 ❌가 하필 **장의 첫 문단, 독자가 가장 먼저 신뢰를 판단하는 자리**에 있다는 게 아쉽다 — 숫자를 세지 말고 리서치가 실제로 말한 형태로 옮기면 해소된다.

---

## 1파(1~3장) 전체 요약

| 장 | 주장 수 | ✅ | ⚠️ | ❌ | 🕒 | 판정 |
|---|---|---|---|---|---|---|
| 01장 | 17 | 12 | 2 | 1 | 2 | **BLOCKING** |
| 02장 | 20 | 17 | 2 | 0 | 1 | 수정 요망 |
| 03장 | 32 | 29 | 1 | 1 | 1 | **BLOCKING** |
| **합계** | **69** | **58** | **5** | **2** | **4** | **BLOCKING (❌ 2건)** |

### ❌ 목록 (저술가 재량으로 덮을 수 없음)

1. **01장 주장 7** — 노티플라이 인용문 2건("리텐션을 높이는 모든 고객대상 마케팅" / 채널 6종)을 FlareLane에도 귀속. 두 문장 모두 `web_gaps.md:250~263`의 노티플라이 항목 아래에만 있다. → 출처 줄을 노티플라이 단독으로 정정하고 FlareLane은 자기 문장으로 분리.
2. **03장 주장 1** — 오프닝의 "20곳 중 넷뿐 / 나머지 열여섯 곳". 근거(`web_products.md:886`)는 **5곳**이며 "정도"로 한정돼 있고, 20곳 중 **3곳은 조회 실패**다. → 세지 말고 확인된 다섯을 이름으로 나열.

### 🕒 목록 (전부 같은 뿌리 — 한 번에 고치는 게 좋다)

3. **01장 주장 6** — Trailhead 인용에 조회 시점 없음
4. **02장 주장 6** — Segment Spec raw 마크다운 인용에 조회 시점 없음
5. **03장 주장 9** — Trailhead(CRM/MA) 인용에 조회 시점 없음

> 셋 다 `web_gaps.md:903`의 같은 지시에 걸린다 — "**Trailhead·Salesforce 개발자 문서·Segment 리포 마크다운은 페이지에 발행일이 없다. 전부 '2026-07-25 조회 기준'으로만 표기할 것.**" 이 책이 01장 119행에서 "이 책은 인용마다 **시점**을 붙인다"고 선언했으므로, 발행일이 없는 출처야말로 시점 표기가 가장 필요한 자리다. **"(2026년 7월 조회 기준 — 이 페이지에는 발행일이 없다)"** 형태로 세 곳을 통일하기를 권한다.

6. **01장 주장 8** — 2023년 노티플라이 채널 목록을 시점 없이 현재형으로 사용 (리서치가 "3년 경과, 채널 목록은 지금과 다를 수 있다"고 경고)

### ⚠️ 목록 (근거보다 강하게 말한 지점)

7. **01장 주장 3** — 대시보드 불일치 원인 3종은 저술가 추론, "일상이다" 빈도 주장에 미사용 JD 근거 있음
8. **01장 주장 14** — 용어 표 선정 기준을 "채용 공고·실무 문서"로 좁게 말했으나 11개 중 4개 출처가 HN 댓글
9. **02장 주장 17** — 스키마 사고 4종의 "대표적인" 프레이밍. 리서치가 승인한 근거(shkan 인용·Snowplow 2014 이슈 계보) 미사용
10. **02장 주장 18** — "같은 개발자가 프론트엔드 이벤트는 아무 협의 없이 바꾼다" 단정
11. **03장 주장 32** — 20곳 표본의 대표성 고지 보강

### 1파 총평

**인용 정확도는 예외적으로 높다.** 원문 대조한 인용 40건 이상이 한 글자까지 일치했고, 필드명·필드 개수·이벤트 이름·연도·금액에 오류가 없다. Raab 4개 연도 분리, "persistent sharable/unified" 유사 문장 함정 회피, 금지 항목 15개 전건 통과, `(사실 확인 필요)` 마커 0건 — 규율 이행도가 매우 높다. 특히 **리서치가 남긴 경고 지시를 본문에 산문으로 옮긴 대목이 12곳 이상**이다(확인 불가의 의미, 벤더 간 대조는 관찰, 마티니 글의 이해관계, 재구성 고지, 404 간접 확인, 판정 유보, 진영 서사 포기 등).

**실패는 딱 두 종류에 몰려 있다.** (a) **출처를 묶어서 귀속**하는 순간 무너진다 — 01장이 벤더 블로그 둘을 한 인용 블록에 묶었고, 03장이 표본을 하나의 숫자로 압축했다. 둘 다 개별 사실은 맞는데 **합치는 과정에서 근거에 없는 것이 생겼다.** (b) **저술가가 직접 채운 예시**의 프레이밍이 근거보다 강하다(01장 원인 3종, 02장 사고 4종).

❌ 2건은 각각 한 문단 수정으로 해소되고, 🕒 4건 중 3건은 동일한 한 줄 삽입으로 끝난다. **2건의 ❌가 해소되면 Phase 5 진행에 사실 관점의 차단 사유는 없다.**

---
---

# 2파(4~6장) 1차 검증

> 검증 시점 2026-07-26. 1차 대조 대상은 `research/*.md` 원본.
> 규율 문서: `02_plan.md` 185~224행 + 1파에서 확립된 기준(**발행일 없는 출처에 조회 시점 병기**).

---

## 04장 — 1차 검증

### 종합: 주장 21건 — ✅ 17 / ⚠️ 4 / ❌ 0 / 🕒 0 — **수정 요망 (BLOCKING 없음)**

> **이 장은 2파에서 학술 인용 밀도가 가장 높은데, 인용 정확도는 전건 통과다.** 논문 12편의 저자·연도·게재지·권(호)가 `research/papers.md`와 한 글자까지 일치하고, **수치·곡선 형태·결론 방향을 저자에게 귀속시킨 문장이 0건**이다. 저술가의 자기 보고("가정을 모델의 속성으로 서술해 저자 귀속 동사를 피했다")를 문장 단위로 직접 대조한 결과 사실이었다.
> 지적 4건은 전부 **근거 강도 고지의 적용 범위**와 **장 내부·장간 정합성** 쪽이며, 인용 자체의 오류는 없다.

---

### 주장 1 — LTV:CAC 3:1의 근거 상태
- **본문:** (3~5행) "LTV:CAC 3:1 … 이 책의 리서치는 3:1이라는 값을 지지하는 peer-reviewed 연구를 찾아봤다. 찾지 못했다. 확인된 것은 이 규칙이 SaaS 투자자·운영자 커뮤니티에서 널리 반복되는 경험칙(rule of thumb)으로 서술된다는 사실까지다(2026년 7월 25일 조회 기준)." + (13행) "생애 가치의 3분의 1까지만 획득 비용에 쓰면 … 정당화가 따라다닌다. … 이 숫자가 최적이라는 연구는 확인되지 않는다."
- **판정:** ✅
- **근거:** `research/papers.md:96~101` (D-2-7) — "이번 세션에서 **3:1 비율을 지지하는 peer-reviewed 연구를 찾지 못했다.** 웹 검색 결과 이 규칙은 SaaS 투자자·운영자 커뮤니티(특히 David Skok 계열 SaaS 메트릭 글)에서 확산된 rule of thumb으로 반복 서술된다." 정당화 논리도 `papers.md:100` 원문("생애가치의 1/3까지 획득에 써도 마진과 성장 여력이 남는다")과 일치. 조회 시점 병기 ✅ (`02_plan.md` §B).
- **조치:** 없음. **리서치가 "이 구분 자체가 이 책의 차별점이다"라고 지시한 처리를 정확히 이행했다.**

### 주장 2 — 12건 표 전체 전사 (행 단위 대조)
- **본문:** (21~34행) 12행 표 — 항목 / 확인된 실제 출처 / 이 책에서 다루는 곳
- **판정:** ✅ (12행 전건 일치)
- **근거:** `research/papers.md:1102~1115` 「학술 근거 없음 / 업계 관행」 표와 행 단위 대조.

| # | 본문 표기 | `papers.md` 원본 | 판정 |
|---|---|---|---|
| 1 | SaaS 투자자·운영자 커뮤니티의 경험칙 — 이 값이 최적이라는 실증 연구 없음 | 동일 (`:1104`, "David Skok 계열" 부기만 생략) | ✅ |
| 2 | Bruce Hardie의 미간행 개인 웹사이트 노트 (brucehardie.com Note #25, 2013 갱신) | `:1105` **문자열 일치** | ✅ |
| 3 | 벤더 기능 — 최상위 저널 검증 미확인 | `:1106` "벤더 기능 + 특허(USPTO 11341516, 11431663) + 응용 저널(MDPI)" / 판정 "최상위 저널 검증 연구 미확인" | ✅ (특허·MDPI 생략은 축약이며 오류 아님. **특허 번호를 안 옮긴 건 오히려 안전한 선택**) |
| 4 | Marz & Warren, *Big Data* (Manning, 2015) — 책 | `:1107` 동일 (Marz 블로그 병기만 생략) | ✅ |
| 5 | Jay Kreps, "Questioning the Lambda Architecture," O'Reilly Radar, 2014 블로그 글 | `:1108` **문자열 일치** | ✅ |
| 6 | 산업계 엔지니어링 블로그·벤더 문서 — 학술 정전 논문 부재 | `:1109` 동일 (Uber Michelangelo 예시만 생략) | ✅ |
| 7 | 각각 기업 기술 보고서 + 베이지안 통계 교과서, 그리고 오픈소스 저장소 | `:1110` "Google 사내 기술 보고서 + 베이지안 통계 교과서 / Meta 오픈소스 저장소" | ✅ |
| 8 | Vaver & Koehler (2011), Google Inc. 기술 보고서 | `:1111` **문자열 일치** | ✅ |
| 9 | 마테크 실무 관행 — 독립 정전 논문 미확인 | `:1112` 동일 | ✅ |
| 10 | NetDB'11 워크숍 논문, DOI 없음 | `:1113` **문자열 일치** | ✅ |
| 11 | 다이렉트 마케팅 업계 통설 — 1차 학술 문헌 확인 불가 | `:1114` 동일 | ✅ |
| 12 | RFC 7489는 Informational 분류 | `:1115` 동일 | ✅ |

- **조치:** 없음. 다만 표의 마지막 열(**"이 책에서 다루는 곳"**)은 리서치가 아니라 저술가의 배치 결정이므로 주장 3·4에서 따로 본다.

### 주장 3 — "이 장이 책임지는 행은 넷이다"
- **본문:** (36행) "이 표에서 이 장이 책임지는 행은 넷이다. 1번은 방금 봤고, 2번은 1장에서 이미 다룬 사례다 …"
- **판정:** ⚠️ 근거 약함 (장 **내부 정합성 불일치** — 표 자신과 어긋난다)
- **근거:** 같은 표의 "이 책에서 다루는 곳" 열에서 **"이 장"이 붙은 행은 여섯이다** — 1(이 장), 2(1장·이 장), 4(이 장·8장), 5(이 장·8장), 9(이 장·11장), 11(이 장). 그런데 본문은 넷(1·2·11·9)만 세고, 4·5는 바로 아래 「판정 하나 — Lambda와 Kappa」 소절에서 **한 절을 통째로 할애해 다룬다**(44~52행). 즉 실제로 이 장이 다루는 행은 여섯인데 문장은 넷이라고 적는다. 독자가 표를 세어보면 즉시 걸리는 종류의 불일치이고, **하필 "숫자에 근거를 붙이라"는 것이 이 장의 주제**라서 비용이 크다.
- **조치:** 36행 첫 문장을 아래로 교체.

  > 이 표에서 이 장이 직접 짚고 갈 행은 넷이고, 4번과 5번은 결이 달라 바로 뒤에 절을 따로 뗐다.

### 주장 4 — 표 10번 행의 상호참조("5장")
- **본문:** (32행) "| 10 | Kafka 원 논문의 위상 | NetDB'11 워크숍 논문, DOI 없음 | **5장** |"
- **판정:** ⚠️ 근거 약함 (**약속 미이행** — 같은 파에서 직접 확인 가능)
- **근거:** 표가 10번 항목을 5장에서 다룬다고 예고했는데, **`chapters/05_draft.md` 전문에 Kafka 원 논문(NetDB'11 / Kreps, Narkhede & Rao 2011)에 대한 서술이 한 줄도 없다.** grep 결과 `NetDB`·`Kreps`·`Narkhede`·`원 논문` 전부 0건이다. 5장은 Kafka를 도구로만 다루고 논문의 위상은 건드리지 않는다. 근거 자체(`papers.md:785~791`, C-17-2 — "이 논문은 워크숍 논문이고 DOI가 없다. … '**Kafka 논문**'을 인용할 때 저널/주요 학회 논문인 것처럼 쓰지 마라")는 확보돼 있으므로 **사실 오류가 아니라 배치 문제**다.
- **조치:** 둘 중 하나를 택한다. **(a)를 권한다** — 5장 「읽어도 남는 로그」 절이 이 소재의 자연스러운 자리다.
  - **(a)** 5장 64행("이 자리에 거의 예외 없이 Kafka(2026-06-23 기준 4.3.1)가 앉는데…") 뒤에 한 문장을 넣는다:

    > 참고로 4장에서 예고한 항목 하나가 여기 있다. 이 도구의 원 논문(Kreps·Narkhede·Rao, "Kafka: a Distributed Messaging System for Log Processing")은 2011년 NetDB 워크숍 논문이고 **DOI가 없다**. 이 책의 리서치는 Crossref에서 정규 레코드를 찾지 못했다(2026년 7월 25일 조회 기준). 인프라 문서에서 "Kafka 논문에 따르면"이라는 말을 볼 때 그게 저널이나 주요 학회 논문을 가리키는 게 아니라는 뜻이다.
  - **(b)** 4장 표 10번 행의 "5장"을 "5장·8장"이 아니라 실제로 다룰 장으로 바꾸거나, 안 다룰 것이면 행에서 상호참조를 빼고 "이 목록에만 있다"로 적는다.

### 주장 5 — Lambda / Kappa 출처의 성격 판정
- **본문:** (48행) "Lambda 아키텍처의 출처는 Nathan Marz와 James Warren이 쓴 *Big Data: Principles and Best Practices of Scalable Realtime Data Systems*(Manning, 2015)다. Kappa 아키텍처의 출처는 카프카 공동 창시자 Jay Kreps가 2014년 O'Reilly Radar에 올린 'Questioning the Lambda Architecture'라는 글이다. **하나는 책이고 하나는 블로그 글이다. 둘 다 peer-reviewed 문헌이 아니다.**"
- **판정:** ✅ (**고위험 지점 — 통과**)
- **근거:** `research/papers.md:801~807` (C-17-4) — "Nathan Marz & James Warren, *Big Data: Principles and Best Practices of Scalable Realtime Data Systems* (Manning, **2015**)로 정식화되었다. **책이지 논문이 아니다.**" / "Kafka 공동 창시자 **Jay Kreps**가 **2014년** O'Reilly Radar에 쓴 블로그 글 'Questioning the Lambda Architecture'에서 제안했다. **블로그 글이지 논문이 아니다.**" 저자·연도·매체·성격 4요소 전건 일치. **논문으로 격상한 흔적 없음.** 52행의 "문서나 발표에서 이 이름을 볼 때 '논문에 따르면'이라는 말은 붙이지 않는 편이 낫다"는 `papers.md:806`의 처리 권고를 산문으로 옮긴 것이다.
- **조치:** 없음. **다만 근거 경로 한 줄을 덧붙이면 더 단단하다(선택)** — `papers.md:805`는 Kreps 글의 출처를 "웹 검색 결과 기반 — 원문 페이지 직접 파싱은 하지 않음"으로 기록했고, `web_stack.md:1348`은 "Lambda/Kappa 원전(Nathan Marz / Jay Kreps)"을 **의도적 미조회** 목록에 넣었다. 즉 이 책은 두 원전을 열어본 적이 없다. 48행 끝에 "(두 원전 자체는 이번 리서치가 직접 열어보지 못했고, 서지 사항만 교차 확인했다)"를 붙이면 이 장의 기준에 정확히 맞는다.

### 주장 6 — RFM 기원의 범위 한정
- **본문:** (38행) "RFM이라는 기법이 미국 다이렉트 마케팅 업계에서 나왔다는 서술은 도처에 있는데, 이번 리서치는 그 기원을 확정해주는 1차 문헌에 도달하지 못했다. **그래서 이 책은 RFM을 누가 언제 만들었다고 적지 않는다.**"
- **판정:** ✅ (모범 사례)
- **근거:** `research/papers.md:40` — "RFM 용어 자체가 1960~70년대 미국 다이렉트 마케팅 업계(카탈로그 소매)에서 나왔다는 서술이 널리 퍼져 있으나, **이번 세션에서 기원을 확정하는 1차 학술 문헌을 확인하지 못했다.** 책에서 'RFM은 19XX년 누가 만들었다'고 단정하지 마라." 본문은 **연도(1960~70년대)조차 옮기지 않았다** — 리서치가 확보한 것보다 더 보수적이다.
- **조치:** 없음.

### 주장 7 — Bult & Wansbeek (1995)
- **본문:** (80행) "**학계는 RFM을 정립하려 한 게 아니라 대체하려 했다.** Bult와 Wansbeek의 1995년 논문 'Optimal Selection for Direct Mail'(*Marketing Science* 14(4))은 다이렉트 메일에서 '누구에게 보낼 것인가'를 수익 기준으로 최적화하는 문제를 정식화한 초기 정전인데, 그 접근의 출발점이 RFM류 휴리스틱 대신 응답 확률 모형에 기반한 선택 규칙을 세우는 것이었다."
- **판정:** ✅
- **근거:** `research/papers.md:24~30` (D-1-1). 서지 — "Jan Roelf Bult, Tom Wansbeek, 'Optimal Selection for Direct Mail,' *Marketing Science*, **Vol. 14, No. 4**, pp. 378–394, **1995**" ✅ 저자·제목·게재지·권(호)·연도 전건 일치. 내용 — 핵심 주장 원문이 "다이렉트 메일에서 '누구에게 보낼 것인가'를 수익 기준으로 최적화하는 문제를 정식화한 초기 정전. RFM류 휴리스틱 선택 대신 응답 확률 모형에 기반한 선택 규칙을 제시한다"로 **본문과 사실상 문자열 일치**. "학계는 RFM을 정립하려 한 게 아니라 대체하려 했다"는 `papers.md:29`의 "**학계는 애초부터 그것을 최적화 문제로 대체하려 했다**"를 옮긴 것이다. 확인 수준 `메타데이터 확인`이 금지한 것은 **구체 수치 귀속**인데(`papers.md:12`), 본문에 수치 0건.
- **조치:** 없음.

### 주장 8 — Fader, Hardie & Lee (2005) 등가치 곡선
- **본문:** (82행) "Fader, Hardie, Lee가 쓴 'RFM and CLV: Using Iso-Value Curves for Customer Base Analysis'(*JMR* 42(4), 2005) … 이 연구가 제시한 등가치 곡선(iso-value curve)이라는 개념은 서로 다른 RFM 조합이 같은 고객 생애 가치를 가질 수 있음을 보여준다. **RFM은 생애 가치의 저차원 프록시**라는 서술이 여기서 나온다."
- **판정:** ✅
- **근거:** `research/papers.md:32~38` (D-1-2). 서지 — "*Journal of Marketing Research*, **Vol. 42, No. 4**, pp. 415–430, **2005**" ✅. 내용 — "서로 다른 RFM 조합이 같은 CLV를 갖는 **등가치 곡선(iso-value curve)**을 그릴 수 있다" ✅, "**RFM은 CLV의 저차원 프록시**" ✅ (`papers.md:37` 문자열 일치). **곡선의 형태(기울기·모양)는 한 글자도 옮기지 않았다** — 개념의 존재만 서술했다.
- **조치:** 없음.

### 주장 9 — 84행 근거 강도 고지의 **적용 범위**
- **본문:** (84행, 인용 블록) "이 절에 인용한 논문들은 저자·연도·게재지·DOI 같은 서지 레코드까지 확인한 것이고 본문 전체를 확인한 것은 아니다(2026년 7월 25일 조회 기준). 그래서 이 책은 각 연구의 개념적 기여까지만 적고, 곡선의 형태나 구체적인 수치는 옮기지 않는다."
- **판정:** ⚠️ 근거 약함 (**고지 자체는 정확한데 범위가 이 절에만 걸려 있다**)
- **근거:** 이 고지는 `papers.md:9~13`의 `메타데이터 확인` 규칙을 정확히 옮긴 것이고, 문면상 **"이 절"** = 「"VIP 고객"을 SQL로 옮기면 세 개의 컬럼이 남는다」 절(54~86행)에만 적용된다. 그런데 같은 성격의 논문이 그 뒤 두 절에서 **네 편 더** 등장한다:
  - Gupta et al. (2006) — 98행 (`papers.md:72~78`, `메타데이터 확인`)
  - Schmittlein, Morrison & Colombo (1987) — 100행 (`papers.md:46~53`, `메타데이터 확인`)
  - BG/NBD (Fader, Hardie & Lee 2005) / BG/BB (Fader, Hardie & Shang 2010) — 106행 (`papers.md:55~70`, 둘 다 `메타데이터 확인`)
  - Braun & Schweidel (2011) — 118행 (`papers.md:80~86`, `메타데이터 확인`)

  네 편 모두 **내용은 리서치와 일치하고 수치 귀속도 0건**이라 사실 오류는 없다(주장 10~13 참조). 문제는 **이 장 자신이 선언한 기준**이다 — 4장은 "근거 강도의 라벨을 붙이라"는 주장을 하는 장인데, 정작 자기 논문 인용 중 절 하나에만 라벨이 붙어 있다.
- **조치:** 84행 인용 블록의 첫머리를 절 단위에서 장 단위로 넓힌다. 아래로 교체.

  > 이 장에 인용한 마케팅 논문들은 저자·연도·게재지·DOI 같은 서지 레코드까지 확인한 것이고, 본문 전체를 확인한 것은 아니다(2026년 7월 25일 조회 기준). 그래서 이 책은 각 연구의 개념적 기여까지만 적고, 곡선의 형태나 구체적인 수치는 옮기지 않는다. 뒤에 나올 생애 가치 모형과 이탈 모형에도 같은 기준이 그대로 적용된다. 이 장의 주제를 생각하면 이 정도 조심성은 지불할 만하다.

  ※ "이 절에" → "이 장에" + 적용 범위 한 문장. 뒤의 두 절에 같은 고지를 반복할 필요가 없어진다.

### 주장 10 — Gupta et al. (2006) CLV 서베이
- **본문:** (98행) "**LTV는 문제 설정에 따라 갈리는 모델 패밀리다.** Gupta 등이 2006년 *Journal of Service Research*에 실은 CLV 모델링 서베이가 RFM·확률 모형·계량경제 모형·머신러닝 등 여러 접근을 한자리에 모아 비교한 것도 그래서다. 이 서베이가 그려 보이는 것은 단일 답이 성립하지 않는 문제의 지형이다."
- **판정:** ✅
- **근거:** `research/papers.md:72~78` (D-2-4). 게재지 *Journal of Service Research*, 2006 ✅. 접근 목록 — 원문 "RFM, 확률 모형, 계량경제 모형, 지속시간 모형, ML, 확산 모형" 중 본문은 넷을 뽑고 "등"으로 열었다 ✅ (누락이 아니라 축약). "**CLV는 하나의 공식이 아니라 문제 설정에 따라 갈리는 모델 패밀리**임을 정리했다"(`papers.md:76`)가 본문 두 문장의 근거다. `papers.md:77` — "'LTV 계산식 알려줘'에 단일 답이 없는 이유를 권위 있게 설명한다".
- **조치:** 없음(주장 9의 범위 확장으로 함께 해소).

### 주장 11 — Pareto/NBD (1987)와 "이탈은 잠재 변수"
- **본문:** (100행) "이런 비계약형(non-contractual) 관계를 다루는 확률 모형 계열의 출발점이 1987년 Schmittlein, Morrison, Colombo의 Pareto/NBD 논문 'Counting Your Customers'(*Management Science* 33(1))이고, 이 계열이 세운 관점 하나가 개발자에게 특히 중요하다. **이탈은 관측 라벨이 아니라 잠재 변수다.**"
- **판정:** ✅
- **근거:** `research/papers.md:46~53` (D-2-1). 서지 — "David C. Schmittlein, Donald G. Morrison, Richard Colombo, 'Counting Your Customers: Who-Are They and What Will They Do Next?,' *Management Science*, **Vol. 33, No. 1**, pp. 1–24, **1987**" ✅ (본문은 부제를 뗀 약칭을 썼는데 통용 표기이며 오류 아님). 내용 — "이탈을 **관측 라벨이 아니라 잠재 변수**로 다뤄야 한다는 게 이 계열의 출발점이다"(`papers.md:52`) **문자열 일치**. "사용자는 작별 인사를 하지 않고 그냥 조용히 안 온다"도 `papers.md:51`("고객은 '탈퇴 버튼'을 누르지 않는다 — 그냥 조용히 안 온다")과 같다.
- **조치:** 없음. **귀속 주어를 "저자들"이 아니라 "이 계열"로 잡은 것이 정확하다** — 초록 미확인 논문에 결론을 직접 귀속시키지 않으면서 개념적 기여를 전달했다.

### 주장 12 — BG/NBD·BG/BB의 가정
- **본문:** (106행) "널리 쓰이는 BG/NBD 모델은 **이탈이 구매 직후에만 일어날 수 있다**고 가정한다. 파이썬 `lifetimes`나 `PyMC-Marketing`에서 `BetaGeoFitter`를 부를 때 함께 딸려 오는 것이 이 가정이다. … 거래가 이산적인 기회에서만 일어나는 경우 — 연 1회 기부나 시즌 단위 구매 같은 — 를 위한 BG/BB 모델이 따로 있다"
- **판정:** ✅ (**고위험 지점 — 통과**)
- **근거:** `research/papers.md:60~61` (D-2-2) — "BG/NBD는 '**이탈은 구매 직후에만 일어날 수 있다**'는 가정으로 바꿔 Beta-Geometric 프로세스를 쓴다" / "`lifetimes`·`PyMC-Marketing`의 `BetaGeoFitter`가 바로 이 모델이다. 라이브러리를 쓰기 전에 **'이탈은 구매 직후에만 발생한다'는 가정**을 알아야 한다". `papers.md:68` (D-2-3) — "거래가 연속 시간이 아니라 **이산적 기회**(연 1회 기부, 시즌 구매 등)에서만 일어나는 상황을 위한 Beta-Geometric/Beta-Bernoulli 모델." 예시 두 개(연 1회 기부·시즌 구매)까지 일치.
- **조치:** 없음. **저술가 자기 보고("가정을 모델의 속성으로 서술")가 여기서 정확히 확인된다** — 문장의 주어가 "BG/NBD 모델은"이지 "Fader와 Hardie는"이 아니다. 초록 미확인 논문에 대해 취할 수 있는 가장 안전한 서술 형태다.

### 주장 13 — Braun & Schweidel (2011) 경쟁 위험
- **본문:** (118행) "Braun과 Schweidel이 2011년 *Marketing Science*에 실은 연구가 다루는 것이 이 문제다. 고객의 이탈을 **여러 원인이 경쟁하는 위험(competing risks)** 으로 모델링하자는 관점이다." + (120행) 결제 실패 이탈에 쿠폰을 보내는 예시
- **판정:** ✅
- **근거:** `research/papers.md:80~86` (D-2-5). 서지 — "Michael Braun, David A. Schweidel, 'Modeling Customer Lifetimes with Multiple Causes of Churn,' *Marketing Science*, Vol. 30, No. 5, **2011**" ✅. **"competing risks"는 저술가의 의역이 아니라 리서치 원문의 표현이다** — `papers.md:84`: "고객 이탈을 단일 사건이 아니라 **경쟁 위험(competing risks)** 으로 본다 — 자발적 해지, 비자발적 실패(결제 실패), 이사 등 원인이 다르면 대응도 달라야 한다." 본문의 이탈 원인 3종(자발 이탈 / 결제 실패 / 이사·상황 변화)이 이 목록과 정확히 같다. 쿠폰 대신 카드 갱신 화면이라는 결론도 `papers.md:85`("결제 실패 이탈에 리텐션 캠페인을 쏘는 건 무의미하다 — **카드 갱신 플로우가 답이다**")와 일치.
- **조치:** 없음.

### 주장 14 — 코호트 리텐션 커브의 함수 형태
- **본문:** (110행) "비계약형 관계에서 코호트·리텐션·생존 분석의 학술적 뿌리는 지금까지 본 확률 모형 계열과 사실상 같다 … 다만 '코호트 리텐션 커브는 시간이 지나면 멱법칙이나 로그 형태로 안정된다'는 실무 서술이 흔한데, 이번 리서치는 이 주장을 확립한 정전 논문을 특정하지 못했다."
- **판정:** ✅ (모범 사례)
- **근거:** `research/papers.md:105~111` (D-3) — "이 축의 학술적 뿌리는 **D-2의 확률 모형 계열과 사실상 같다**" ✅ / `papers.md:110` — "'코호트 리텐션 커브가 멱법칙/로그 형태로 안정화된다'는 실무 서술이 흔한데, 이번 세션에서 이를 확립한 **정전 논문을 특정하지 못했다.** 책에서 이 주장을 쓰려면 fact-checker의 별도 검증이 필요하다." `papers.md:1123` 확인 불가 목록 1번도 동일.
- **조치:** 없음. **리서치가 명시적으로 "fact-checker 별도 검증 필요"로 넘긴 항목인데, 저술가가 주장을 쓰지 않고 '특정하지 못했다'는 사실만 적어 스스로 해소했다.** 이 처리로 별도 웹 검증이 불필요해졌다.

### 주장 15 — 상시 홀드아웃의 근거 상태
- **본문:** (40행) "전체 사용자 중 일정 비율을 어떤 캠페인도 받지 않는 통제군으로 항상 남겨두는 상시 홀드아웃 설계는 … 이걸 정식화한 독립 정전 논문은 특정되지 않았다. 통제 실험 일반론에서 정당화하는 수밖에 없다. … 특정되지 않은 것은 이 관행을 정식화한 논문 한 편이고, 통제군을 두어 효과를 재려는 발상 자체에는 통제 실험이라는 훨씬 넓은 근거가 깔려 있다."
- **판정:** ✅
- **근거:** `research/papers.md:1112` — "마테크 실무 관행 | **독립 정전 논문 미확인** — 통제 실험 일반론(Kohavi 계열)과 고스트 광고(D-10-4)로 정당화해야 함". 본문이 "정당화하는 수밖에 없다"까지 정확히 옮겼고, 나아가 **"근거 없음"과 "정식화 논문 없음"을 구분하는 문장을 덧붙여** 독자의 과잉 해석을 막았다.
- **조치:** 없음.

### 주장 16 — Insider RFM 세그먼트 문서의 존재
- **본문:** (90행) "이 리서치가 Insider의 개발자 문서 색인을 훑다가 발견한 것인데, 이 제품은 세그먼트 문서 아래에 RFM 세그먼트를 위한 페이지를 따로 두고 있다. 동적 세그먼트, 예측 세그먼트와 나란히 놓인 목록에 그 항목이 있다(**문서 색인에서 URL 존재를 확인, 2026년 7월 25일 조회 기준. 페이지 본문은 열어보지 못해 내용은 확인하지 못했다**)."
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_products.md:547~552` — 문서 색인(`llms.txt`)에서 확인된 URL 목록이 `audience-segments-overview.md` / `dynamic-segments.md` / `audience-predictive-segments.md` / `rfm-segments.md` 넷이고, 리서처가 "**RFM 세그먼트**가 별도 문서로 존재. (… 이 문서 자체는 미조회 → 내용 `확인 불가`)"라고 적었다. 본문의 괄호 고지가 이 상태를 **그대로** 옮겼다 — 확인한 것(URL 존재)과 확인 못 한 것(본문 내용)을 문장에서 분리했다.
- **조치:** 없음.

### 주장 17 — Insider Predictive Segments 5종
- **본문:** (146행) "Insider는 예측 세그먼트(Predictive Segments)라는 이름으로 다섯 종류를 제품 기능으로 제공한다 — Likelihood to Purchase, User Engagement, Customer Lifecycle Status, Discount Affinity, Attribute Affinity(**페이지 표기 2026년 4월 12일, 2026년 7월 25일 조회**). 문서는 사용자의 구매 가능성을 예측하는 알고리즘을 활용한다고 설명하는데, **어떤 모델과 어떤 피처를 쓰는지에 대한 공개 자료는 찾지 못했다.**"
- **판정:** ✅
- **근거:** `research/web_products.md:533~544` — 5종 목록 **순서까지 일치**(Likelihood to Purchase / User Engagement / Customer Lifecycle Status / Discount Affinity / Attribute Affinity), 원문 영문 유지 ✅. 작동 설명 "leverage algorithms that predict users' likelihood to purchase and segment users based on their interests and purchase behaviors"의 요약 ✅. `web_products.md:542` — "⚠️ **사용하는 ML 모델에 대한 서술 → NOT FOUND.** 어떤 모델·피처를 쓰는지 **공개 자료 없음**. 추정 금지." 본문이 추정 없이 부재를 그대로 적었다 ✅. 시점 — `web_products.md:1230` 신선도 원장 "페이지 표기 2026-04-12 | 2026-07-25" **양쪽 다 병기** ✅ (`02_plan.md` §B).
- **조치:** 없음.

### 주장 18 — dbt 공식 문서 인용 2건
- **본문:** (128~132행) "dbt 공식 문서는 자기 모델을 이렇게 설명한다(**2026년 7월 25일 조회 기준. 이 페이지는 발행일이 표시되어 있지 않다**). > 'Models are primarily written as a `select` statement and saved as a `.sql` file.' > 'When you execute `dbt run`, you are running a model that will transform your data without that data ever leaving your warehouse.'"
- **판정:** ✅
- **근거:** `research/web_stack.md:419, 421` — 두 인용 모두 **한 글자까지 일치**. 출처 `web_stack.md:430` — "[https://docs.getdbt.com/docs/build/models | **발행일 확인 불가 (미조회)** | 검색 시점 2026-07-25]". **1파에서 확립된 기준("발행일 없는 출처에 조회 시점 병기")이 2파에서 지켜졌음을 확인하는 첫 사례다** — 01장 Trailhead·02장 Segment Spec에서 새던 것이 여기서는 문장 안에 명시적으로 들어가 있다.
- **조치:** 없음.

### 주장 19 — dbt 3계층 배치와 모델 이름
- **본문:** (134행) "실무에서 흔히 보이는 배치는 세 계층이다. 원본 이벤트를 정규화하는 staging 계층, 아이덴티티 해석이나 세션화처럼 중간 가공을 맡는 intermediate 계층, 그리고 고객 360과 세그먼트가 놓이는 marts 계층. 마지막 계층에 `seg_high_value`나 `seg_churn_risk` 같은 이름의 모델들이 나란히 앉는다."
- **판정:** ✅
- **근거:** `research/web_stack.md:440~447` 계층 다이어그램 — `staging/` "원본 이벤트를 정규화", `intermediate/` "아이덴티티 해석, 세션화", `marts/` "고객 360(dim_customer) / 세그먼트(seg_high_value, seg_churn_risk, seg_cart_abandoners)". 계층명·역할·예시 모델명 전건 일치.
- **조치:** 없음. (다만 **"실무에서 흔히 보이는 배치"**라는 표현은 근거보다 약간 넓다 — 리서치는 "전형적 계층 구조"라고 적었을 뿐 빈도 조사를 한 게 아니다. 다만 dbt 공식 권장 구조로 널리 통용되는 서술이라 과잉 차단하지 않는다.)

### 주장 20 — 세그먼트 크기 테스트
- **본문:** (136행) "예를 들어 세그먼트 크기가 전일 대비 절반 이상 달라지면 실패하도록 걸어두면, 잘못된 캠페인이 나가기 전에 파이프라인이 먼저 멈춘다."
- **판정:** ✅
- **근거:** `research/web_stack.md:451` — "**테스트가 붙는다.** '세그먼트 크기가 전일 대비 **50% 이상 변하면 실패**' 같은 테스트로, 잘못된 세그먼트가 캠페인으로 나가기 전에 막는다." 수치·조건·효과 일치.
- **조치:** 없음.

### 주장 21 — "VIP 세그먼트 기준이 언제 바뀐 거야?"
- **본문:** (140행) "**'VIP 세그먼트 기준이 언제 바뀐 거야?'**라는 질문이 회의에서 사라지는 것 — 마케팅 데이터 팀이 이 도구에 정착하는 이유의 절반쯤은 여기에 있다."
- **판정:** ⚠️ 근거 약함 (**인용 문장은 근거가 있는데 "절반쯤"이라는 비중 주장은 없다**)
- **근거:** 질문 문장 자체는 `research/web_stack.md:450`에 있다 — "'**VIP 세그먼트 기준이 언제 바뀐 거야?**'라는 흔한 사고가 사라진다." 그러나 "마케팅 데이터 팀이 이 도구에 정착하는 이유의 **절반쯤**"이라는 비중 배분은 어느 리서치 파일에도 없다. 채택률 조사도, 도입 사유 설문도 확보되지 않았다. 수사적 표현이긴 하지만 **이 장은 "근거 없는 숫자를 상수로 굳히지 마라"는 장**이라 자기 문장에 근거 없는 분수를 넣는 게 특히 눈에 띈다.
- **조치:** 140행 해당 문장을 아래로 교체(분수를 빼고 근거가 있는 것만 남긴다).

  > **"VIP 세그먼트 기준이 언제 바뀐 거야?"**라는 질문이 회의에서 사라지는 것 — 마케팅 데이터 팀이 이 도구에 정착하는 이유를 하나만 꼽으라면 여기다.

---

### 04장 요약

**BLOCKING 항목:** **없음.** ❌ 0건 / 🕒 0건.

**수정 요망 (⚠️ 4건):**
- 주장 3 — "이 장이 책임지는 행은 넷" vs 표의 여섯 행 (장 내부 불일치)
- 주장 4 — 표 10번 행이 예고한 "5장"에 Kafka 원 논문 서술이 없음 (약속 미이행, 5장 쪽 삽입 권장)
- 주장 9 — 84행 근거 강도 고지가 한 절에만 걸려 뒤 두 절의 논문 4편을 못 덮음
- 주장 21 — "이유의 절반쯤"이라는 근거 없는 비중 배분

**금지 항목:** 4장에서 0건. **특히 `02_plan.md` 범위 한정 3건(Goldfarb & Tucker / Berman / Blake)의 본진 보존이 확인된다** — 세 이름 및 `Shapley`·`eBay`·`Gordon`·`Zettelmeyer`·`2201.07055` 전부 grep 0건. 4장은 세그먼트·LTV·이탈 모형만 다루고 인과·어트리뷰션 논의를 10·11장으로 온전히 넘겼다.

**총평:** 이 책에서 학술 인용 밀도가 가장 높은 장인데 **인용 오류가 0건**이다. 논문 12편의 서지가 전건 일치하고, `메타데이터 확인` 등급 논문에 수치·곡선 형태·결론을 귀속시킨 문장이 하나도 없다. 특히 **귀속 주어를 저자가 아니라 모델·계열로 돌리는 문장 설계**(주장 11·12)가 일관되게 나타나는데, 이건 초록 미확인 논문을 다루는 정석이다. 남은 4건은 전부 인용 바깥 — 표와 본문의 셈 불일치, 상호참조 미이행, 고지 범위, 수사적 분수 — 이고 문장 단위 수정으로 끝난다.

---

## 05장 — 1차 검증

### 종합: 주장 22건 — ✅ 18 / ⚠️ 4 / ❌ 0 / 🕒 0 — **수정 요망 (BLOCKING 없음)**

> **버전 4건 전부 Tier 1 표와 한 자리까지 일치**하고, **Tier 2 금지 목록(Airflow·Dagster·Spark·Redpanda·Pulsar·Snowflake·BigQuery·Redshift) 등장 0회**다. 인용 12건(Snowplow 2·Confluent 2·KIP-98 2·Flink 2·SLULA 1·우아한형제들 1·LINE 1건 요약)이 전건 원문 일치한다.
> 지적 4건은 **회사 국적 서술 1건**, **근거 강도 고지의 과장 1건**, **고지 적용 범위 2건**이다.

---

### 주장 1 — Kafka 버전
- **본문:** (64행) "이 자리에 거의 예외 없이 Kafka(**2026-06-23 기준 4.3.1**)가 앉는데"
- **판정:** ✅
- **근거:** `research/web_stack.md:71~72` — "**[버전: 4.3.1 / 2026 기준]** — 최신 아카이브 디렉터리 `4.3.1` 타임스탬프 **`2026-06-23 22:22`**". 신선도 원장 `web_stack.md:1364`도 "**4.3.1 / 2026-06-23 22:22 (페이지 표기·확정)**". **Apache 배포 아카이브 = 전체 타임스탬프 확정 경로**이므로 일자를 박아도 안전한 항목이다(`web_stack.md:16` 규칙).
- **조치:** 없음.

### 주장 2 — Flink 버전 + LTS 라인
- **본문:** (150행) "Flink(**2026-06-25 기준 2.3.0**, 병행 유지되는 **LTS 라인은 1.20.5**)로 상태를 들고"
- **판정:** ✅
- **근거:** `research/web_stack.md:206~208` — "**[버전: 2.3.0 / 2026-06-25 기준, LTS는 1.20.5 / 2026-06-03]**" + 공식 다운로드 페이지 표기 "Apache Flink® 2.3.0 is the latest stable release." 신선도 원장 `web_stack.md:1372`도 동일. **`web_stack.md:247`이 요구한 "어느 계열 기준인지 명시"를 이행했다.**
- **조치:** 없음.

### 주장 3 — dbt 버전
- **본문:** (179행) "배치 쪽 도구는 대개 dbt(**2026-07-16 기준 dbt-core 1.12.0**)를 중심에 둔다."
- **판정:** ✅
- **근거:** `research/web_stack.md:405~406` — "**[버전: dbt-core 1.12.0 / 2026-07-16 기준.** 2.0은 알파 단계 — v2.0.0-alpha.5 / 2026-07-20]" + GitHub Releases 표기 "dbt-core v1.12.0 — July 16, 2026"(**페이지에 연도가 명시된 확정 근거**). `web_stack.md:409` 지시 — "**'1.12 / 2026 기준'으로 서술**하고 2.0은 '개발 중'으로만 언급하는 게 안전하다." 본문은 2.0을 아예 언급하지 않아 더 안전하다.
- **조치:** 없음.

### 주장 4 — Snowplow 라이선스 (SLULA)
- **본문:** (51~58행) "🚨 **Snowplow의 핵심 컴포넌트는 OSI 오픈소스가 아니다.** … > 'Licensee is not granted the right to, and Licensee shall not, exercise the License for any Competing Use, and Licensee may exercise the License only for Non-Production Use or Non-Commercial Use.' … SLULA(Snowplow Limited Use License Agreement)는 **2024년 1월 v1.0으로 도입**됐고, **v1.1이 2024년 12월에 적용**되면서 v1.0에 있던 'Highly Available' 조항이 제거됐다. 그 결과 고가용성 구성 여부와 무관하게 **모든 프로덕션 사용이 상용 라이선스를 요구**하는 것으로 정리됐다. [docs.snowplow.io/… | v1.1 = 2024-12(문서 표기) | 검색 시점 2026-07-25]"
- **판정:** ✅ (**고위험 지점 — 통과**)
- **근거:** `research/web_stack.md:344~354`. 영문 인용 **한 글자까지 일치**(`:346`). 버전 이력 — "**SLULA v1.0** — 2024년 1월 도입" ✅ / "**SLULA v1.1** — 'rolled out in December, 2024'. v1.0의 '**Highly Available**' 조항을 제거했고, 그 결과 **고가용성 여부와 무관하게 모든 프로덕션 사용이 상용 라이선스를 요구**하는 것으로 정리되었다" ✅ **날짜·버전·조항명·귀결 4요소 전건 일치**. 표현도 정확하다 — 리서치 원문이 "더 이상 **OSI 오픈소스**가 아니다"이고 본문도 "**OSI 오픈소스**가 아니다"로 썼다(막연히 "오픈소스가 아니다"가 아니라 OSI 기준을 명시). `web_stack.md:1307` 상충 판정 — "**판단: 공식 문서가 이긴다.** … **이 사실 자체가 개발자 독자에게 유용한 정보이므로 본문에서 다룰 것.**" 지시를 이행했다.
- **조치:** 없음.

### 주장 5 — RudderStack·Redis 라이선스를 단정하지 않음
- **본문:** (58행) "Apache 2.0 포크(OpenSnowcat)가 존재한다는 언급은 확인했으나, 이 책의 리서치는 그 포크의 유지보수 현황까지는 확인하지 못했다." + (60행) "실제로 이 책의 리서치는 RudderStack과 Redis의 현행 라이선스 조건을 확인하는 데 실패했다. **확인하지 못한 것을 '오픈소스'라고 적을 수는 없으니 여기서도 단정하지 않는다.**"
- **판정:** ✅ (모범 사례 — `02_plan.md` 금지 항목 9 정확 이행)
- **근거:** `research/web_stack.md:354` — "검색 결과에서 Apache 2.0 포크(OpenSnowcat)가 존재한다는 언급을 확인했으나, **포크의 현황·유지보수 상태는 이 세션에서 조회하지 않았다 — 확인 불가 (미조회)**." `web_stack.md:1310` (§4-4) — RudderStack "문서 사이트가 리다이렉트 후 내비게이션만 반환해 확인 실패. **확인 불가.**" `web_stack.md:1313` (§4-5) — Redis "GitHub Releases 페이지에 라이선스 정보 없음. **확인 불가.** … **단정 서술 금지.**"
- **조치:** 없음. **금지 항목을 회피하는 데 그치지 않고 회피 사실 자체를 독자에게 교훈으로 전환한 대목이다.**

### 주장 6 — Snowplow Enrich 인용 2건
- **본문:** (35~43행) "> 'The Enrich application cleanses the data and validates each event against its schema to ensure it meets the criteria you have designed and set.' [docs.snowplow.io/docs/fundamentals/ | **발행일 확인 불가** | 검색 시점 **2026-07-25**]" + "> 'failed events can be reprocessed'"
- **판정:** ✅
- **근거:** `research/web_stack.md:325, 327` — 두 인용 모두 원문 일치. 출처 표기 `web_stack.md:332` — "[https://docs.snowplow.io/docs/fundamentals/ | **발행일 확인 불가 (미조회)** | 검색 시점 2026-07-25]". **본문이 출처 줄에 '발행일 확인 불가'와 '검색 시점'을 둘 다 인쇄했다** — 1파에서 지적한 시점 누락 패턴이 2파에서 교정된 형태다.
- **조치:** 없음.

### 주장 7 — Confluent 파티션·컨슈머 그룹 인용
- **본문:** (72~76행) "> 'messages in each partition log are then read sequentially' > 'Each partition is consumed by exactly one consumer within each consumer group at any given time.' [docs.confluent.io/kafka/design/consumer-design.html | 발행일 확인 불가 | 검색 시점 2026-07-25]"
- **판정:** ✅
- **근거:** `research/web_stack.md:84, 89` — 두 인용 **한 글자까지 일치**. 출처 `web_stack.md:85` 및 신선도 원장 `web_stack.md:1365` 일치.
- **조치:** 없음.

### 주장 8 — 오프셋의 정의와 성질
- **본문:** (68행) "오프셋은 그 그룹이 다음에 읽을 레코드를 가리키는 정수이고, 데이터 자체와 분리되어 따로 저장된다."
- **판정:** ✅
- **근거:** `research/web_stack.md:97` 원문 — "An offset is a unique identifier, **an integer**, which marks **the next record that should be read** by the consumer in a partition." `web_stack.md:99` — "오프셋은 `__consumer_offsets` **내부 토픽에 저장된다**"(= 데이터와 분리 저장). 영문 원문을 그대로 인용하지 않고 한국어로 풀었으나 의미 왜곡 없음.
- **조치:** 없음.

### 주장 9 — 파티션 키 = 데이터 모델링 결정
- **본문:** (80행) "**파티션 키 선택은 성능 튜닝이 아니라 데이터 모델링 결정이다.**" + (84행) 파티션 수 변경 시 `hash(key) % partition_count` 재배치, 핫 파티션
- **판정:** ✅
- **근거:** `research/web_stack.md:91` — "**파티션 키 선택은 Martech에서 데이터 모델링 결정이지 성능 튜닝이 아니다.**" (문장 순서만 뒤집힌 동일 명제). `web_stack.md:128` — "늘리는 순간 `hash(key) % partition_count`가 바뀌어 **기존 키의 파티션 배치가 깨진다.** … Martech에서는 이게 '**저니가 한 번 꼬였다**'로 나타난다" ✅ 본문 84행과 문자열 수준 일치. `web_stack.md:129` 핫 파티션 — "`user_id` 해시가 균등하다는 보장은 **봇·크롤러·내부 테스트 계정** 앞에서 깨진다" ✅ 세 예시까지 일치.
- **조치:** 없음.

### 주장 10 — LINE 2016 사례의 **국적 서술**
- **본문:** (80행) "**국내 사례로는** LINE이 2016년 사내 메시지 전송 파이프라인에서 `userId`를 파티션 키로 삼은 기록을 공개한 적이 있다(2016년 글이라 API 서술의 근거로는 낡았고, 파티션 키 선택의 고전 사례로만 유효하다)."
- **판정:** ⚠️ 근거 약함 (**사례 내용·시점 한정은 완벽한데, "국내"라는 귀속이 근거에 없다**)
- **근거:** 사례 내용은 전건 일치다 — `research/web_stack.md:1243` "**순서 보장** — **userId를 파티셔닝 키로** 사용해 태스크 처리 순서 유지" ✅, 시점 한정도 `web_stack.md:1237`의 경고("⚠️ **2016년 글 — 구버전 정보일 수 있음.** … **고전 레퍼런스로만 인용하고, 현재 API 서술의 근거로 쓰지 말 것**")를 괄호에 그대로 옮겼다 ✅ — 이 부분은 모범적이다.
  **문제는 "국내 사례로는"이다.** `web_stack.md:1235` 출처 레코드는 "engineering.**linecorp**.com/ko/blog/… | 2016-08-18 | 저자: **Kawamura Yuto**"다. 이 글은 **LINE Corporation(일본 법인)** 엔지니어링 블로그의 한국어판에 실린 글이고, 저자도 일본 법인 소속으로 표기돼 있다. **리서치 어느 파일도 이 사례를 "국내"로 분류하지 않았다.** 반면 같은 §3-7의 우아한형제들·쿠팡, §3-6의 토스는 명시적 국내 사례다. 한국어 블로그에 실렸다는 사실이 회사 국적의 근거가 되지는 않는다.
- **조치:** 80행 해당 문장을 아래로 교체(국적 주장을 빼고 확인된 것만 남긴다).

  > 실제 사례로는 LINE이 2016년 사내 메시지 전송 파이프라인에서 `userId`를 파티션 키로 삼은 기록을 공개한 적이 있다(engineering.linecorp.com, 2016-08-18. 2016년 글이라 API 서술의 근거로는 낡았고, 파티션 키 선택의 고전 사례로만 유효하다).

  ※ 국내 사례가 필요하면 같은 절에 이미 쓰고 있는 **우아한형제들 기술블로그(2024-05-30)**가 그 역할을 한다(주장 14).

### 주장 11 — KIP-98이 보장하는 것
- **본문:** (100~104행) "Kafka의 트랜잭션 설계 문서인 KIP-98은 프로듀서마다 고유 ID를 부여하고 시퀀스 번호를 증가시키는 방식으로 중복을 걸러낸다고 설명하며, 이렇게 적는다. > 'Every message write will be persisted exactly once, without duplicates and without data loss' [cwiki.apache.org/… | 발행일 확인 불가 | 검색 시점 2026-07-25]"
- **판정:** ✅
- **근거:** `research/web_stack.md:103~111` — 인용문 **한 글자까지 일치**(`:109`). 앞의 요약("프로듀서마다 고유 ID … 시퀀스 번호를 증가")도 원문 2건에 근거한다 — "Every new producer will be assigned a unique **PID** during initialization."(`:103`) / "For a given PID, **sequence numbers will start from zero and be monotonically increasing**"(`:105`). 출처·시점 표기 `web_stack.md:111`, 신선도 원장 `:1366` 일치.
- **조치:** 없음.

### 주장 12 — KIP-98이 **보장하지 않는** 것 (4개 목록)
- **본문:** (108~112행) "> 'We cannot guarantee that all the messages of a committed transaction will be consumed all together' … 문서가 드는 이유는 넷이다. ①컴팩션된 토픽이 트랜잭션 메시지를 덮어쓸 수 있고, ②로그 세그먼트를 넘나드는 트랜잭션은 세그먼트가 삭제될 때 일부를 잃고, ③컨슈머가 임의 지점으로 seek하면 앞부분을 놓치고, ④컨슈머가 그 트랜잭션에 참여한 파티션을 전부 읽지 않을 수도 있다."
- **판정:** ✅ (**고위험 지점 — 4개 항목 전건 통과**)
- **근거:** `research/web_stack.md:115` 인용 원문 일치. `web_stack.md:117` — "이유로 네 가지를 든다 — **컴팩션된 토픽이 트랜잭션 메시지를 덮어쓸 수 있고, 로그 세그먼트를 넘나드는 트랜잭션은 세그먼트 삭제 시 일부를 잃고, 컨슈머가 임의 지점으로 seek하면 앞부분을 놓치고, 컨슈머가 트랜잭션에 참여한 모든 파티션을 읽지 않을 수 있다.**" **항목 4개·순서 모두 일치.** 이어지는 해석("exactly-once가 다루는 범위는 쓰기 쪽이고, 읽는 쪽이 그 원자성을 그대로 물려받지는 않는다")은 인용 두 건에서 저술가가 끌어낸 요약이며, 근거 범위 안에 있다.
- **조치:** 없음.

### 주장 13 — Carbone et al. (2017) Flink 상태 관리
- **본문:** (112행) "학술 쪽에도 대응물이 있다 — Carbone 등이 2017년에 발표한 Flink 상태 관리 논문이 스트림 처리에서 일관된 상태 스냅샷을 어떻게 저비용으로 찍고 복구하는지를 다룬다. exactly-once라는 말이 어떤 마법을 가리키는 게 아니고 **체크포인트와 재생과 멱등성을 조합해 만들어낸 결과**라고 이해하는 편이 실무에 훨씬 도움이 된다."
- **판정:** ✅
- **근거:** `research/papers.md:793~799` (C-17-3). 서지 — "Paris Carbone 외, 'State management in Apache Flink®,' *PVLDB* Vol. 10, No. 12, **2017**" ✅ 연도 일치. 내용 — "분산 스트림 처리에서 **일관된 상태 스냅샷**을 어떻게 **저비용으로 찍고 장애 시 복구**하는가"(`papers.md:797`) ✅ 문자열 수준 일치. "**'exactly-once'는 마법이 아니라 체크포인트 + 재생 + 멱등성의 조합**"(`papers.md:798`) ✅ 그대로. **수치 귀속 0건**이며 저자 이름 + 개념적 기여까지만 서술했다 — `메타데이터 확인` 등급에 맞는 처리다.
- **조치:** 없음.

### 주장 14 — 우아한형제들 Transactional Outbox
- **본문:** (118행) "우아한형제들 기술블로그(**2024-05-30**)는 이 문제를 두고 '**데이터와 메시지 발행의 트랜잭션을 하나로 관리하여 데이터 정합성을 확보할 필요가 있었습니다**'라고 적었고, 그 답으로 Transactional Outbox 패턴을 택했다."
- **판정:** ✅
- **근거:** `research/web_stack.md:1220` — "[techblog.woowahan.com/17386/ | **2024-05-30** | 저자: 김나은 | 검색 시점 2026-07-25]"(신선도 원장 `:1401`도 "**2024-05-30 (페이지 표기·확정)**"). 인용문은 `web_stack.md:1225`에 **한 글자까지 일치**. "**Transactional Outbox Pattern** (Debezium MySQL 커넥터)"(`:1224`) ✅. `web_stack.md:1231` — "Transactional Outbox는 **§1-1의 exactly-once 논의와 직결**된다. 'Kafka가 exactly-once를 지원한다'는 말과 'DB 트랜잭션과 이벤트 발행의 원자성'은 다른 문제이고" — 본문 118행 첫 문장이 이 프레임을 그대로 쓴다.
- **조치:** 없음. (Debezium은 안 옮겼는데, 확인된 사실이므로 넣어도 되고 안 넣어도 된다 — 현재 상태로 오류 없음.)

### 주장 15 — Flink 이벤트 타임 / 워터마크 인용 2건
- **본문:** (126~136행) "> 'Event time is the time that each individual event occurred on its producing device.' [nightlies.apache.org/flink/flink-docs-**release-2.0**/docs/concepts/time/ | 발행일 확인 불가 | 검색 시점 2026-07-25]" + "> 'A Watermark(t) declares that event time has reached time t in that stream, meaning that there should be no more elements from the stream with a timestamp t' <= t.'"
- **판정:** ✅
- **근거:** `research/web_stack.md:218, 227` — 두 인용 **한 글자까지 일치**(부등호·표기 포함). 출처 URL·시점 `web_stack.md:219` 및 신선도 원장 `:1373` 일치. 본문 138행의 해석("워터마크는 관측이 아니라 **선언**이다")도 `web_stack.md:229`("즉 워터마크는 '이 시각 이전 데이터는 다 왔다고 치자'는 **선언**이다") 그대로.
- **조치:** 없음. **다만 한 가지 짚어둘 것(선택)** — 본문은 Flink 최신을 2.3.0으로 적고(150행) 인용은 **2.0 문서 브랜치**에서 가져왔다. 리서치도 이를 "(미조회, **2.0 문서 브랜치**)"로 명시했다(`web_stack.md:219`). URL이 본문에 노출돼 있어 독자가 확인 가능하지만, 128행 출처 줄에 "**2.0 문서 브랜치 기준**"을 한 마디 넣으면 이 책의 시점 규율에 더 정확히 맞는다.

### 주장 16 — Akidau et al. (2015) Dataflow Model
- **본문:** (146행) "Akidau 등이 2015년에 발표한 Dataflow Model 논문이 무한하고 순서가 뒤섞인 스트림 처리를 네 갈래 질문으로 분해했다 — 무엇을 계산하는가, 이벤트 시간의 어디를 묶는가, 처리 시간의 언제 결과를 내보내는가, 나중에 도착한 것을 어떻게 반영하는가. 그리고 정확성과 지연과 비용은 동시에 최대화할 수 없고 명시적으로 교환해야 한다는 것이 그 논문의 관점이다. **이 책의 리서치는 이 논문의 서지와 요지까지 확인했고 본문 전체를 대조하지는 않았으니**, 여기서는 개념적 기여를 소개하는 선까지만 쓴다."
- **판정:** ⚠️ 근거 약함 (**내용은 전건 일치인데, 고지 문장이 확인 수준을 한 단계 높여 말한다**)
- **근거:** 내용은 ✅다 — `research/papers.md:781` (C-17-1): "무한(unbounded)·순서 뒤섞인(out-of-order) 스트림 처리를 **네 가지 질문**으로 분해한다 — *무엇을* 계산하는가(변환), *이벤트 시간의 어디서* 계산하는가(윈도잉), *처리 시간의 언제* 결과를 내는가(워터마크·트리거), *어떻게* 개선분을 반영하는가(누적/철회). 정확성·지연시간·비용은 **동시에 최적화할 수 없고 명시적으로 교환**해야 한다." **네 질문의 내용과 순서, 3자 교환 명제까지 일치**하고 수치 귀속은 0건이다.
  **문제는 확인 수준 표기다.** `papers.md:1217` 신선도 원장의 C-17-1 확인 수준은 `메타데이터 확인`이고, `papers.md:12`가 그 등급을 이렇게 정의한다 — "Crossref/Semantic Scholar/arXiv의 권위 있는 서지 레코드(제목·저자·연도·발표처·DOI)를 확인했으나 **초록 본문은 못 봤다**." 즉 리서치가 확인한 것은 **서지뿐**이고, 위 "핵심 주장"은 리서처가 제목·분야 지식으로 정리한 요약이다. 본문의 "**서지와 요지까지 확인했고**"는 초록을 읽은 것처럼 들린다. 이 장이 4장에서 세운 기준(확인한 것과 확인 못 한 것을 문장에서 나눈다)에 비추면 한 칸 어긋난다.
- **조치:** 146행 마지막 문장을 아래로 교체.

  > 이 책의 리서치가 확인한 것은 이 논문의 **서지 레코드까지이고 초록 본문은 열지 못했다**(2026년 7월 25일 조회 기준). 그래서 여기서는 이 분야에서 널리 통용되는 개념적 기여를 소개하는 선까지만 쓰고, 논문 안의 어떤 수치도 옮기지 않는다.

  ※ 4장 주장 9의 조치(“이 절에” → “이 장에”)와 같은 계열의 수정이다. 두 장의 표현을 맞춰두면 통권에서 기준이 하나로 읽힌다.

### 주장 17 — 스트리밍의 벽 4종
- **본문:** (152~156행) 상태 무한 증가·TTL / 부재 조건 감지와 타이머 / 운영 난이도(체크포인트·백프레셔·상태 백엔드·사바포인트) / 컨슈머 랙 = 진짜 SLA
- **판정:** ✅
- **근거:** `research/web_stack.md:245` — "**상태가 무한히 큰다.** 사용자별 상태를 TTL 없이 두면 상태 크기가 사용자 수에 비례해 무한 증가한다. Martech는 사용자 수가 수천만인 도메인이라 이게 **즉시 문제가 된다**" ✅ (본문 "규모가 커진 뒤에 오는 게 아니고 처음부터 온다"와 동일 취지). `web_stack.md:238` — "'**일어난 일**'이 아니라 '**안 일어난 일**'을 감지해야 하고, 그러려면 상태와 타이머가 필수" ✅. `web_stack.md:246` — "**운영 난이도가 스택에서 가장 높다.** 체크포인트 튜닝, 백프레셔, 상태 백엔드 선택(RocksDB), 사바포인트 기반 무중단 배포 — 소규모 팀이 Flink를 도입했다가 유지 못 하고 배치로 회귀하는 사례가 흔하다" ✅ **4항목과 회귀 서술까지 일치**(158행). `web_stack.md:130` — "**컨슈머 랙(lag)이 Martech의 진짜 SLA다.** … 랙 모니터링은 마케팅 팀에게 약속한 지연 시간의 유일한 증거다" ✅.
- **조치:** 없음.

### 주장 18 — at-least-once + 다운스트림 멱등
- **본문:** (116행) "게다가 트랜잭션 코디네이터와 격리 수준이 붙으면 처리량과 지연이 나빠진다. 그래서 실무에서 도달하는 답은 대개 소박하다. **at-least-once로 받고, 다운스트림에서 이벤트 ID 기준으로 멱등 처리한다.**"
- **판정:** ✅
- **근거:** `research/web_stack.md:131` — "**exactly-once는 공짜가 아니다.** 트랜잭션 코디네이터·컨트롤 메시지·`read_committed` 격리 수준이 붙으면서 처리량과 지연이 나빠진다. 대부분의 Martech 이벤트 파이프라인은 **at-least-once + 다운스트림 멱등 처리**(이벤트 ID 기준 중복 제거)가 더 현실적이다."
- **조치:** 없음.

### 주장 19 — 배치 vs 스트리밍 대비표 (소절 ⑦)
- **본문:** (166~175행) 고지 블록("아래 대비는 특정 벤더나 제품의 공식 권고가 아니다. 이 책의 리서치가 세 도구의 공개 문서 특성을 대조해 정리한 설계 서술이며, 조직의 규모와 데이터 양에 따라 달라진다.") + 6행 대비표
- **판정:** ✅ (**고위험 지점 — 근거 등급 표기 통과**)
- **근거:** `research/web_stack.md:1002~1024` (§3-3)와 행 단위 일치 — 지연("최대 24시간" / "초 단위") ✅, 비용("하루 한 번, 전체 스캔" / "24시간 상시 가동") ✅, 복잡도("SQL 한 파일. **신규 입사자도 읽는다**" / "상태 관리, 워터마크, 체크포인트, 상태 스키마 진화") ✅ **문자열 일치**, 정정("로직을 바꾸면 다음 실행에 자동 반영" / "**상태를 어떻게 할 것인가**가 문제가 된다") ✅, 정확도("매번 원본에서 다시 계산하므로 드리프트가 없다" / "30일 윈도우를 상태로 들거나 근사해야 한다") ✅. **근거 등급도 정확하다** — `web_stack.md:1045`가 "⚠️ 이 절은 §1-1·1-3·1-7의 조회된 문서 특성에 근거한 **아키텍처 분석**이며, **특정 출처의 인용이 아니다**"라고 적었고, 본문 고지가 이 문장을 그대로 옮겼다. **1차 근거로 격상되지 않았다.**
- **조치:** 없음.

### 주장 20 — 비용 구조·결정 규칙 (고지 밖 단정문 2건)
- **본문:** (177행) "**배치는 계산량에 비례하고, 스트리밍은 시간에 비례한다.**" + (183행) "**웨어하우스 비용은 실행 빈도에 거의 그대로 비례한다.**"
- **판정:** ⚠️ 근거 약함 (**내용은 근거와 일치하나, 굵은 단정문 두 개가 166행 고지 블록 바깥에 있다**)
- **근거:** 내용은 ✅다 — `research/web_stack.md:1028` "배치는 **계산량에 비례**하고, 스트리밍은 **시간에 비례**한다" **문자열 일치**, `web_stack.md:460` "**웨어하우스 비용이 dbt 실행 빈도에 비례한다.**" ✅. 다만 두 문장 모두 **리서처의 트레이드오프 분석**이지 벤더 문서 인용이 아니다(§3-3 전체가 `web_stack.md:1045`에서 "특정 출처의 인용이 아니다"로 표시됨, §1-7 함정 목록도 동일 성격). 166행 고지는 문면상 "**아래 대비는**" = 바로 아래 표에 걸리고, 177·183행은 표를 지나 별도 단락에서 굵게 단정된다. 185행의 결정 규칙("세그먼트 개수가 많고 지연 요구가 느슨하면 배치가 압도적으로 싸다…" — `web_stack.md:1033` 일치)도 같은 상태다.
  ※ 위반 강도는 낮다. 고지가 정확하고 11행 위에 있으며, 세 문장 다 근거와 일치한다. **차단 사유가 아니라 이 장의 자기 기준을 마지막 한 칸까지 맞추는 문제다.**
- **조치:** 166행 고지 블록의 첫 문장을 아래로 교체해 적용 범위를 절 단위로 넓힌다(문장 세 개를 각각 고치는 것보다 싸다).

  > 아래 대비와 이어지는 비용·결정 규칙 서술은 특정 벤더나 제품의 공식 권고가 아니다. 이 책의 리서치가 세 도구의 공개 문서 특성을 대조해 정리한 설계 서술이며, 조직의 규모와 데이터 양에 따라 달라진다.

### 주장 21 — dbt 증분 모델의 함정
- **본문:** (181행) "**증분 모델은 늦게 도착한 데이터를 놓치기 쉽다.** … 어제 새벽에 이미 처리한 구간으로 오늘 오전에 이벤트가 도착하면, 증분 조건을 어떻게 잡느냐에 따라 그 이벤트는 조용히 빠진다."
- **판정:** ✅
- **근거:** `research/web_stack.md:458` — "**증분 모델의 함정.** … incremental을 쓰는데, **늦게 도착한 데이터(late-arriving data)를 놓치기 쉽다.** Martech의 모바일 이벤트는 늦게 오는 게 정상이라 이 문제가 **상시 발생**한다." 본문이 이 장 전체의 주제(늦게 오는 게 정상)와 연결한 것도 리서치의 프레임 그대로다.
- **조치:** 없음.

### 주장 22 — "5분 늦으면 무슨 일이 일어나나요"와 두 갈래 답
- **본문:** (191~197행) "> 🎯 **'이 세그먼트가 5분 늦으면 무슨 일이 일어나나요?'**" + "**'아무 일도 안 일어나요.'** 그러면 배치다." / "**'고객이 이미 경쟁사에서 샀어요.'** 그러면 스트리밍이다." + (185행) "실무의 답은 대개 '둘 다'다 — … 장바구니 이탈, 결제 실패, 첫 구매 축하 정도가 그 소수에 들어간다."
- **판정:** ✅
- **근거:** `research/web_stack.md:1039~1043` — "**개발자가 마케터에게 물어야 할 단 하나의 질문:** *'이 세그먼트가 5분 늦으면 무슨 일이 일어나나요?'* — '아무 일도 안 일어나요' → 배치. / '고객이 이미 경쟁사에서 샀어요' → 스트리밍. **이 질문 하나가 아키텍처 비용을 몇 배 가른다.**" 본문 199행("이 한 질문이 아키텍처 비용을 몇 배 가른다")까지 일치. `web_stack.md:1037` — "대부분의 세그먼트는 배치, **전환에 직결되는 소수**(**장바구니 이탈, 결제 실패, 첫 구매 축하**)만 스트리밍" ✅ **예시 3종 일치**.
- **조치:** 없음.

---

### 05장 요약

**BLOCKING 항목:** **없음.** ❌ 0건 / 🕒 0건.

**수정 요망 (⚠️ 4건):**
- 주장 10 — LINE을 "국내 사례"로 귀속 (근거 없음, 출처는 일본 법인 블로그의 한국어판)
- 주장 16 — Akidau 논문 "서지와 요지까지 확인"이 실제 확인 수준(`메타데이터 확인` = 초록 미독)보다 한 칸 높다
- 주장 20 — 비용·결정 규칙 단정문 3건이 166행 고지 블록 바깥에 있음
- 주장 15(선택) — Flink 인용이 2.0 문서 브랜치인데 본문 최신 버전은 2.3.0

**오프닝 장면의 지위 (3개 장 공통 — 검증 범위 판정):**

세 장의 오프닝을 따로 점검했다. **05장(3~5행, "새벽 1시 12분에 쿠폰이 나갔다")과 06장(3행, "화요일 오전 회의실")은 어느 리서치 파일에도 대응하는 실제 사고 기록이 없다** — `web_stack.md` §3-7이 문서화한 사례는 우아한형제들·LINE·Pinterest·쿠팡 넷이고, 쿠폰 오발송 사고는 그중에 없다.

**그러나 이는 결함이 아니다.** `profiles/tech-book/scaffolds.md:76, 80`이 **오프닝 메뉴**에 "**상황 가정**"과 "**실패 장면(in medias res)** — '오전 3시, 알림이 울린다. 결제가 멈췄다'"를 명시적으로 승인한다(`voice.md:22, 63`도 동일). 05장 오프닝은 이 승인된 기법의 전형이고, **사실 주장이 아니라 문체 장치이므로 팩트체크 범위 밖이다.**

**다만 그 장면이 딛고 선 메커니즘은 근거가 있다** — `web_stack.md:223`이 "**지하철에서 앱을 쓴 사용자의 이벤트는 지상에 올라온 20분 뒤에 서버에 도착한다. 처리 타임 기준이면 그 사용자는 '20분 뒤에 장바구니를 담은 사람'이 되고, '장바구니 담고 30분 내 미결제 → 쿠폰 발송' 룰이 엉뚱한 시점에 발동한다**"고 적었다. 05장 오프닝의 20분·30분·역전 구조가 전부 이 한 문단에서 나왔다. **즉 구체적 시각(새벽 1시 12분)과 인물은 구성이되, 사고의 인과 구조는 리서치 근거 위에 있다.** 1파 01장 주장 3(근거 없는 원인 3종을 근거처럼 제시)과는 성격이 다르다 — 그쪽은 본문 중간의 설명 문장이었고, 이쪽은 승인된 오프닝 기법이다.

※ 편집 단계 참고: `scaffolds.md:117~118`이 "인접 챕터는 같은 오프닝 기법을 반복하지 않는다", "'상황 가정' 오프닝은 약 1/3 챕터 이하"를 요구한다. **이건 style-guardian의 관할이지 팩트체커의 관할이 아니므로 판정하지 않는다.**

**버전 대조 결과 (Tier 1 표 §4-1 대조 — 4건 전건 일치):**

| 본문 표기 | `web_stack.md` 근거 | 근거 등급 | 판정 |
|---|---|---|---|
| Kafka 4.3.1 / 2026-06-23 | `:71`, 원장 `:1364` | Apache 아카이브 **전체 타임스탬프·확정** | ✅ |
| Flink 2.3.0 / 2026-06-25 + LTS 1.20.5 | `:206`, 원장 `:1372` | 공식 다운로드 페이지 **표기·확정** | ✅ |
| dbt-core 1.12.0 / 2026-07-16 | `:405`, 원장 `:1382` | GitHub Releases **연도 명시·확정** | ✅ |
| SLULA v1.0 2024-01 / v1.1 2024-12 | `:349~352`, 원장 `:1378` | 공식 FAQ **문서 표기** | ✅ |

**금지 항목 (5장 해당분):** 0건.
- **Tier 2 등장 0회 확인** — `Airflow`·`Dagster`·`Spark`·`Redpanda`·`Pulsar`·`Snowflake`·`BigQuery`·`Redshift` grep 전부 **0건**. `web_stack.md:1340`의 의도적 미조회 목록을 한 항목도 건드리지 않았다.
- **Snowplow "오픈소스" 단정 없음** — 49행의 "오픈소스 CDP 스택"은 **독자의 통념을 인용부호로 제시한 뒤 곧바로 반박**하는 구조이고, 51행이 "OSI 오픈소스가 아니다"로 확정한다. RudderStack·Redis는 60행에서 명시적으로 판단 유보.
- **Akidau·Carbone 수치 귀속 0건** — 두 논문 모두 이름 + 개념적 기여까지만. 벤치마크·성능 수치 없음.

**총평:** 2파에서 버전·라이선스 밀도가 가장 높은 장인데 **버전 4건이 한 자리도 틀리지 않았고**, 하필 가장 틀리기 쉬운 Snowplow 라이선스(버전 두 개 + 날짜 두 개 + 조항명 + 귀결)를 전건 정확히 옮겼다. 인용 12건도 원문 일치다. 남은 ⚠️ 4건 중 셋은 **고지 문장의 범위와 정확도** 문제이고, 하나(LINE 국적)만이 새로운 사실 오류에 해당한다 — 그것도 단어 하나 교체로 해소된다.

---

## 06장 — 1차 검증

### 종합: 주장 24건 — ✅ 21 / ⚠️ 3 / ❌ 0 / 🕒 0 — **수정 요망 (BLOCKING 없음)**

> **이 장 최대 위험이었던 서지 함정 2건이 모두 통과했다.** HLL·Bloom 수치의 귀속 주어는 문장 단위 대조에서 **전부 Redis 공식 문서**였고, Flajolet·Bloom·Cormode & Muthukrishnan·Dunning & Ertl을 언급한 문장에는 **수치가 하나도 없다**. Theta Sketch 저자도 `Dasgupta, Lang, Rhodes, Thaler` + `arXiv:1510.01455`로 정확하고, 오귀속(`Stokes`·`Tirthapura`)은 grep 0건이다. C-Store 재수록본 DOI도 미사용이다.
> ⚠️ 3건 중 2건은 **Iceberg·Pinot 릴리스 일자**다. **두 값 다 Apache 배포 아카이브의 전체 타임스탬프로 검증된 값이므로 '검증 불가(🕒)'가 아니다** — 문제는 리서치가 **소스 간 불일치를 이유로 "일자를 박지 말라"고 두 번 명시**했는데 본문이 근거보다 강하게(일자까지) 단정한 것이고, 해소 방법은 **월 단위로의 약화**다. 그래서 ⚠️로 판정한다. **약화는 선택이 아니라 필수다.**

---

### 주장 1 — 서빙 경로의 지연 예산
- **본문:** (5행) "페이지 하나를 200밀리초 안에 그린다고 치면 프로필 조회에 떼어줄 수 있는 몫은 그 십분의 일 안팎이다. 게다가 이 질문은 초당 수만 번 들어온다."
- **판정:** ✅
- **근거:** `research/web_stack.md:951` — "**페이지 렌더링 예산이 200ms라면 프로필 조회에 쓸 수 있는 건 10~20ms다.**" 본문의 "십분의 일 안팎"이 이 구간(10~20ms)을 정확히 덮는다. "초당 수만 번"은 `web_stack.md:960` 대비표의 서빙 경로 동시성 "수만" ✅. **"치면"이라는 가정 표시가 붙어 있어 특정 서비스의 실측치로 오독될 위험도 없다.**
- **조치:** 없음.

### 주장 2 — 분석/서빙 2경로 대비표
- **본문:** (11~19행) "이 책의 리서치가 스택 문서들을 대조해 정리한 그림은 이렇다." + 5행 대비표(질문 / 접근 / 지연 / 동시성 / 스토어)
- **판정:** ✅
- **근거:** `research/web_stack.md:955~961` 원표와 **5행 전건 문자열 일치** — 질문("지난달 VIP 세그먼트는 몇 명?" / "이 사람은 VIP인가?"), 접근("수억 행 스캔·집계" / "키 하나 조회"), 지연("초~분" / "밀리초"), 동시성("수십" / "수만"), 스토어("ClickHouse / Iceberg+Trino" / "Redis / Aerospike / Cassandra"). 근거 등급 표기도 정확하다 — 이 표는 리서처의 대조 결과이지 벤더 문서 인용이 아니고, 본문 11행이 "**이 책의 리서치가 스택 문서들을 대조해 정리한 그림**"이라고 밝혔다. 38행("저장소가 여러 벌인 건 팀이 정리를 못 해서 생긴 사고가 아니다")도 `web_stack.md:953`의 프레임 그대로.
- **조치:** 없음. (Aerospike·Cassandra는 이름만 표에 오르고 **성능 수치가 붙지 않았다** — `web_stack.md:969`의 "성능 수치·아키텍처 세부는 확인 불가" 경고를 지켰다.)

### 주장 3 — MergeTree 8192행 그래뉼
- **본문:** (44~52행) "> 'The primary key also does not reference individual rows but blocks of 8192 rows called granules.' — ClickHouse MergeTree 문서 (**이 페이지에는 발행일이 없다 — 2026년 7월 25일 조회 기준**)" + B-tree 대비 해설
- **판정:** ✅
- **근거:** `research/web_stack.md:152` — 인용 **한 글자까지 일치**. 출처·시점 `web_stack.md:153`, 원장 `:1368` 일치. 해설도 `web_stack.md:155` 그대로 — "B-tree는 행 하나하나를 가리키니 인덱스가 데이터만큼 커진다. MergeTree는 **8192행짜리 그래뉼 단위**로만 가리키니 인덱스가 RAM에 통째로 들어간다. 대신 '이 사용자 한 명의 행'을 찍어서 가져오는 건 못한다 — **8192행을 읽고 걸러야 한다. OLAP에 강하고 OLTP에 약한 이유가 전부 이 한 줄에 있다.**" 본문 52행이 이 마지막 문장을 그대로 옮겼다.
- **조치:** 없음.

### 주장 4 — 정렬 키가 곧 성능
- **본문:** (54행) "`ORDER BY (user_id, event_time)`으로 두면 한 사용자의 행동 시퀀스가 물리적으로 붙어 있어 사용자별 스캔이 빨라지고, `ORDER BY (event_time, event_name)`으로 두면 시간 범위 집계가 빨라진다. 마테크에서 자주 요구되는 퍼널과 리텐션은 사용자별 시퀀스를 봐야 답이 나오므로, 보통 `user_id`가 앞에 온다."
- **판정:** ✅
- **근거:** `research/web_stack.md:163` — "**정렬 키가 곧 성능이다.** … 이벤트 테이블에서 `ORDER BY (user_id, event_time)`으로 두면 사용자별 시퀀스 스캔이 빨라지고, `ORDER BY (event_time, event_name)`으로 두면 시간 범위 집계가 빨라진다. Martech에서는 **퍼널·리텐션이 사용자별 시퀀스를 요구**하므로 보통 `user_id`가 앞에 온다." **키 조합 두 개와 결론까지 일치.**
- **조치:** 없음.

### 주장 5 — Trino 인용 2건 + 버전
- **본문:** (56~61행) "> 'Do not mistake the fact that Trino understands SQL with it providing the features of a standard database.' > 'Trino was not designed to handle Online Transaction Processing (OLTP).' — Trino 공식 문서 (**발행일 없음 — 2026년 7월 25일 조회 기준. 버전은 483 / 2026-07-17 기준**)"
- **판정:** ✅
- **근거:** 인용 — `research/web_stack.md:598, 602` **한 글자까지 일치**(대소문자·괄호 포함). 출처·시점 `web_stack.md:612`, 원장 `:1395`. 버전 — `web_stack.md:584~586`: "**[버전: Release 483 / 2026-07-17 기준]** 공식 릴리스 노트: `Release 483 (17 Jul 2026)`" ✅ **공식 릴리스 노트에 연도가 명시된 확정 근거**라 일자를 박아도 안전하다(Iceberg·Pinot과 대비되는 지점 — 주장 12·13 참조). 63행의 해설("데이터를 자기가 들고 있지 않다")도 `web_stack.md:592` 그대로.
- **조치:** 없음.

### 주장 6 — ClickHouse와 Pinot의 자리 구분
- **본문:** (67~71행) "ClickHouse가 앉는 자리는 분석가와 마케터가 대시보드에서 던지는 무거운 애드혹 쿼리다. … 동시에 던지는 사람은 수십 명 규모다. Pinot이 앉는 자리는 **최종 사용자에게 직접 노출되는 분석**이다. 광고주가 자기 콘솔에서 … 쿼리 모양은 정형화돼 있고 대신 동시성이 수천에서 수만으로 뛴다."
- **판정:** ✅
- **근거:** `research/web_stack.md:565~568` — "**ClickHouse의 자리** — 분석가·마케터가 대시보드에서 던지는 무거운 애드혹 쿼리. 동시성은 낮고(**수십**), 쿼리는 복잡하고, 데이터는 크다. / **Pinot의 자리** — **최종 사용자에게 직접 노출되는** 분석. **광고주 대시보드**('내 캠페인 지금 성과'), 판매자 대시보드, 앱 안의 개인 통계. 동시성은 높고(**수천~수만**), 쿼리는 정형화되어 있고, 지연은 밀리초여야 한다. Martech에서 후자가 실재한다 — **광고 플랫폼의 광고주 콘솔이 정확히 이 패턴**이다." **동시성 구간·예시·쿼리 성격 전건 일치.**
- **조치:** 없음.

### 주장 7 — Pinot 성능 표방 수치 (10ms P95 / 100,000 QPS)
- **본문:** (75행) "Pinot 프로젝트 문서는 자기 성능을 이렇게 표방한다 — 'Ultra low-latency queries (as low as 10ms P95)', 'High query concurrency (as many as 100,000 queries per second)'. 이 두 수치를 쓸 때는 조건을 반드시 붙여야 한다. **프로젝트 자체 문서의 표방 수치이며 독립적으로 검증된 벤치마크가 아니다.**"
- **판정:** ✅ (**고위험 지점 — 통과**)
- **근거:** `research/web_stack.md:553~554` — 두 인용 **한 글자까지 일치**. `web_stack.md:559` **필수 표기 지시** — "⚠️ **인용 시 필수 표기:** 위 `10ms P95`·`100,000 QPS`는 **Apache Pinot 프로젝트 자체 문서의 표방 수치**이며 독립 검증된 벤치마크가 아니다. 책에 쓸 때 반드시 '프로젝트 문서 표방 기준'을 붙일 것." 본문이 **인용 바로 다음 문장에서** 이 조건을 굵게 붙였다 — 거리가 멀지 않다는 점이 중요하다.
- **조치:** 없음.

### 주장 8 — ClickBench 미사용 선언
- **본문:** (75행) "같은 이유로 이 책은 ClickBench 수치를 쓰지 않는다. 제3자 중립 벤치마크처럼 인용되는 경우가 많지만 **운영 주체가 ClickHouse 쪽이고**, 방법론 문서는 이번 리서치에서 확인하지 못했다."
- **판정:** ✅ (모범 사례)
- **근거:** `research/web_stack.md:199~200` — "**ClickBench 수치 인용 시 주의:** … **운영 주체는 ClickHouse 측**(GitHub 저장소·도메인 구조로 확인). 즉 **제3자 중립 벤치마크가 아니라 ClickHouse가 운영하는 공개 벤치마크**다. … 방법론 상세는 조회하지 못했다. … **구체 수치는 확인 불가 (미조회), 인용 금지**". `web_stack.md:1322` (§4-8)도 동일. **grep 결과 이 장에 ClickBench 수치 0건** — 배제 선언만 있고 숫자는 없다.
- **조치:** 없음.

### 주장 9 — Apache Druid의 성격 규정 고지
- **본문:** (77행) "Apache Druid도 이 자리 근처에 자주 등장한다. 다만 **이번 리서치는 Druid 아키텍처 문서를 열지 못했다.** 버전(37.0.0 / 2026-05-06)만 확인했고, '실시간 수집에 강한 OLAP'이라는 흔한 성격 규정은 **1차 확인을 거치지 않은 통념 수준**이라는 것을 밝혀둔다."
- **판정:** ✅ (**고지 충분 — 버전도 위반 아님**)
- **근거:** 두 갈래로 확인했다.
  - **버전:** Druid는 `web_stack.md` §2 Tier 2에 있지만 **버전만은 명시적 예외**다 — `web_stack.md:785`: "*(**버전 예외 — 이 항목만 연도 확정**: Apache 배포 아카이브에서 `37.0.0 — **2026-05-06** 04:19` … 확인. `[archive.apache.org/dist/druid/ | 2026-05-06 (전체 타임스탬프·확정) | 2026-07-25]`)*" 원장 `:1392`도 동일. 즉 **`02_plan.md` §B의 "Tier 2 버전 쓰지 마라"에 걸리지 않는다** — 리서치가 이 항목만 아카이브로 연도를 확정해 예외로 남겼고, 본문은 그 확정값을 옮겼다.
  - **성격 규정:** 같은 `:785` 말미 — "**아키텍처·기능 서술은 여전히 확인 불가 (미조회)** — Druid 공식 문서를 조회하지 않았으므로 **위 성격 규정은 통념 수준이다.**" `web_stack.md:1316` (§4-6)도 "**Druid 특성 서술은 확인 불가 (미조회).**" 본문 고지가 이 두 문장을 **거의 문자 그대로** 옮겼고, 무엇을 확인했고(버전) 무엇을 확인 못 했는지(아키텍처)를 문장에서 분리했다.
- **조치:** 없음. **고지는 충분하다.** 다만 이 장이 Druid에 대해 하는 유일한 실질 서술이 "통념"이라고 스스로 밝힌 상태이므로, 편집 단계에서 이 문단을 통째로 덜어내도 장의 논지에는 손실이 없다(선택).

### 주장 10 — Iceberg 스펙 버전별 차이 (v1/v2/v3)
- **본문:** (83행) "Iceberg 스펙은 포맷 버전을 나눠 관리한다. v1은 불변 파일 관리, v2는 **행 수준 삭제**('delete files to encode rows that are deleted in existing data files'), v3는 타입 확장과 기본값, 행 계보까지. (**스펙 원문은 main 브랜치 기준, 2026년 7월 25일 조회.**)"
- **판정:** ✅
- **근거:** `research/web_stack.md:284~286` — "**v1** — Parquet/Avro/ORC 위 불변 파일 관리. / **v2** — 행 수준 삭제 도입: '**delete files to encode rows that are deleted in existing data files**' … / **v3** — 타입 시스템 확장 … + **기본값(default values)**, 다중 인자 변환, **행 계보(row lineage)**." 영문 인용 일치, 세 버전 요약 일치. 출처 `web_stack.md:273` — "[raw.githubusercontent.com/apache/iceberg/**main**/format/spec.md | **발행일 확인 불가 (main 브랜치 시점)** | 검색 시점 2026-07-25]" → 본문의 "main 브랜치 기준, 2026년 7월 25일 조회"가 이 상태를 정확히 옮겼다.
- **조치:** 없음.

### 주장 11 — Iceberg가 기본값이 된 네 가지 이유
- **본문:** (85~91행) 삭제 가능 / 스키마 진화 / 타임 트래블 / 엔진 중립 + "**테이블 포맷 선택이 규제 대응 능력을 결정한다**" + 작은 파일·컴팩션·스냅샷 만료 딜레마
- **판정:** ✅
- **근거:** `research/web_stack.md:294~297` 4항목과 순서까지 일치 — ① "v2의 행 수준 delete가 없으면 '사용자 한 명 지우기'가 **수 TB 재작성**이 된다. **테이블 포맷 선택이 규제 대응 능력을 결정한다.**" ✅ (본문 87행 문자열 일치), ② 스키마 진화 ✅, ③ "'3월 캠페인 때 이 사용자가 정말 VIP 세그먼트였나?'를 그 시점 스냅샷으로 증명할 수 있다. **마케팅 분쟁·정산 분쟁에서 실제로 쓰인다**" ✅ (본문 89행), ④ 엔진 중립·벤더 락인 ✅. 함정 — `web_stack.md:301~302`: "**작은 파일 문제.** … **컴팩션이 상시 운영 업무**다." / "**스냅샷이 무한히 쌓인다.** 만료 정책을 안 걸면 … 그런데 **너무 짧게 걸면 타임 트래블·삭제 감사 능력을 잃는다** — **규제 요구와 비용이 여기서 정면충돌한다.**" ✅ 본문 91행이 그대로.
- **조치:** 없음.

### 주장 12 — Iceberg 버전 표기 ⚠️
- **본문:** (81행) "요즘 이 자리의 기본값은 Apache Iceberg(**1.11.0 / 2026-05-19**)다."
- **판정:** ⚠️ 근거 약함 (**본문이 근거보다 강하다** — 값은 검증됐으나 리서치가 금지한 자릿수까지 단정. 필수 정정, 문자 3개 삭제로 해소)
- **근거:** 버전과 날짜 자체는 근거가 있다 — `research/web_stack.md:253~255`: "**[버전: 1.11.0 / 2026-05-19 기준 — 연도 확정]** Apache 배포 아카이브 디렉터리 타임스탬프: `apache-iceberg-1.11.0/ — **2026-05-19** 04:43`." **그러나 리서치는 같은 자리에서 일자를 박지 말라고 명시했다** — `web_stack.md:258`: "**경미한 불일치:** GitHub은 `20 May`, 아카이브는 `2026-05-19` — 하루 차이(릴리스 태그 생성 시점 vs dist 업로드 시점, 타임존). **책에는 `1.11.0 / 2026-05` 수준으로 쓰는 게 안전하다.**" `web_stack.md:1302` (§4-2)도 재차 — "**책에는 일자를 박지 말고 `2026-05`·`2026년 중반` 수준으로 쓸 것.**" 즉 이 값은 **두 1차 소스가 갈리는 항목**이고, 리서치가 판단을 유보한 채 병기했다. 본문은 그중 한쪽을 일자까지 확정해 인쇄한다.
- **조치:** 81행을 아래로 교체(`-19` 삭제).

  > 요즘 이 자리의 기본값은 Apache Iceberg(**1.11.0 / 2026-05**)다.

  ※ 이 책이 Kafka(2026-06-23)·Flink(2026-06-25)·dbt(2026-07-16)·Trino(2026-07-17)에는 일자를 박아도 되는 이유는, 그 넷은 **단일 소스가 연도까지 명시한 확정 근거**이기 때문이다. Iceberg·Pinot만 소스가 갈린다. 이 구분을 지키는 게 규율의 요점이다.

### 주장 13 — Pinot 버전 표기 ⚠️
- **본문:** (75행) "(검색 시점 2026년 7월 25일, **Pinot 1.5.1 / 2026-06-30 기준**.)"
- **판정:** ⚠️ 근거 약함 (**본문이 근거보다 강하다** — Iceberg보다 소스 간 불일치 폭이 크다. 필수 정정)
- **근거:** `research/web_stack.md:527~529`가 아카이브 타임스탬프 `apache-pinot-1.5.1/ — 2026-06-30 22:18`을 확정한 건 맞다. **그러나 바로 다음 줄이 경고다** — `web_stack.md:534`: "> **불일치 병기:** GitHub 목록은 1.5.1을 `05 Jun`, 1.5.0을 `09 Apr`로 표기하나 Apache 아카이브는 각각 `2026-06-30`, `2026-05-01`이다. **상충: GitHub은 05 Jun / 아카이브는 2026-06-30.** … 책에는 **`1.5.1 / 2026년 중반`** 수준으로 쓰고 **특정 일자를 박지 말 것.**" `web_stack.md:1302`도 "**Pinot — GitHub `05 Jun` / 아카이브 `2026-06-30` (약 25일 차)**". **Iceberg가 하루 차이인 데 반해 Pinot은 약 25일 차라 같은 달로 뭉갤 수도 없다.** 리서치가 두 번 명시적으로 지시한 항목이다.
- **조치:** 75행 괄호를 아래로 교체.

  > (검색 시점 2026년 7월 25일, **Pinot 1.5.1 / 2026년 중반 기준**.)

### 주장 14 — HLL 수치의 귀속 (**이 장 최대 위험 — 문장 단위 검증**)
- **본문:** (107행) "**Redis 공식 문서는** 자기 HyperLogLog 구현이 **최대 12KB 메모리를 쓰고 0.81%의 표준 오차를 제공한다고 적는다.** 문서가 직접 드는 사용 사례도 그대로 우리 이야기다 — 'How many unique visits has this page had on this day?' (**발행일 없음 — 2026년 7월 25일 조회 기준.**)" + (109행) "이 자료구조의 **이론적 뿌리는** Flajolet, Fusy, Gandouet, Meunier의 2007년 HyperLogLog 논문이다. **다만 방금 인용한 12KB와 0.81%는 Redis 구현의 값이지 그 논문의 값이 아니다.**"
- **판정:** ✅ (**`02_plan.md` 금지 항목 10 — 정확 준수**)
- **근거:** **문장 단위로 분해해 대조했다.**
  - 수치가 들어간 문장(107행)의 **주어는 "Redis 공식 문서는"**이고, 술어는 "적는다"다. 근거는 `research/web_stack.md:856` 원문 — "**The Redis implementation uses up to 12 KB of memory and provides a standard error rate of 0.81%.**" (원장 `:1385`도 "**0.81% 표준오차·12KB — 문서 명시**"). 인용문 "How many unique visits has this page had on this day?"도 Redis 문서 유스케이스다.
  - 논문 저자 4인이 등장하는 문장(109행 첫 문장)에는 **숫자가 하나도 없다.** 서지는 `research/papers.md:731` (C-16-2) — "Philippe Flajolet, Éric Fusy, Olivier Gandouet, Frédéric Meunier, 'HyperLogLog: …,' 2007" ✅ **저자 4인·순서·연도 일치**.
  - 나아가 109행 둘째 문장이 **두 출처의 분리를 독자에게 명시적으로 알린다** — "12KB와 0.81%는 **Redis 구현의 값이지 그 논문의 값이 아니다.** 이 구분을 흐리는 글이 흔한데…". `02_plan.md:198` 금지 항목 10("이 값들은 **Redis 공식 문서의 값**이지 원 논문의 값이 아니다")을 **회피가 아니라 본문화**했다.
  - **저술가의 자기 보고("물리적으로 분리")는 사실이다.** 수치와 논문 저자명이 같은 문장에 공존하는 사례는 이 장에 0건이다.
- **조치:** 없음.

### 주장 15 — HLL의 교집합 한계와 세그먼트 빌더
- **본문:** (111~113행) "**합집합은 되고 교집합은 안 된다.** … 포함배제 원리로 우회하면 오차가 증폭된다. … 세그먼트 빌더에서 마케터가 실제로 누르는 조합이 바로 그것이다. '지난달 구매자 **그리고** 앱 미방문자, **단** 이미 쿠폰 받은 사람 제외.'"
- **판정:** ✅
- **근거:** `research/web_stack.md:862` — "**한계:** 합집합(PFMERGE)은 되지만 **교집합은 없다.** 'A 세그먼트 ∩ B 세그먼트의 고유 수'는 HLL로 직접 못 구한다." `research/papers.md:769` (C-16-6) — "HyperLogLog는 합집합은 되지만 **교집합·차집합이 약하다.** 마테크 세그먼테이션은 정확히 그 연산 — '**A 세그먼트 AND B 세그먼트 NOT C 세그먼트가 몇 명인가**' — 을 요구한다." 본문의 체크박스 예시가 이 AND/NOT 구조를 그대로 옮긴 것이다. 오차 증폭 서술("두 개의 근사값을 빼는 계산이라… 작은 교집합일수록 상대 오차가 커진다")은 저술가가 근사 오차의 성질에서 전개한 해석이며, 근거와 모순되지 않고 수치 귀속도 없다.
- **조치:** 없음.

### 주장 16 — Theta Sketch 저자·식별자 (**서지 함정 1**)
- **본문:** (115행) "근거 논문은 **Dasgupta, Lang, Rhodes, Thaler**의 'A Framework for Estimating Stream Expression Cardinalities'(**arXiv:1510.01455, ICDT 2016**)이고, 각 스트림의 샘플을 보편적으로 결합해 합집합·교집합·차집합의 카디널리티를 추정하는 틀을 제시한다. Apache DataSketches의 Theta Sketch가 이 계열의 구현이다." + (117행) "이 리서치는 저자 표기를 arXiv API로 직접 조회했고, 그 결과가 위의 네 사람이다. 검색 중에 다른 저자 조합으로 적힌 자료를 만났지만 API 응답이 기준이 된다."
- **판정:** ✅ (**서지 함정 통과 — 오귀속 0건**)
- **근거:** `research/papers.md:763~770` (C-16-6). 저자 — "Anirban Dasgupta, Kevin Lang, **Lee Rhodes**, **Justin Thaler**" ✅ **4인 일치, 순서 일치**. 식별자 — "arXiv:**1510.01455** (v2)" ✅, 학회 — "*19th International Conference on Database Theory (**ICDT 2016**)*" ✅. 제목 ✅. 핵심 주장 — "각 스트림의 샘플을 **보편적(universal)으로 결합**해 합집합·교집합·차집합 같은 **집합 연산의 카디널리티**를 추정하는 프레임워크" ✅ 본문과 일치. 구현 — "Apache DataSketches의 Theta Sketch가 이 논문의 구현이고" ✅.
  **오귀속 스캔:** `Stokes`·`Tirthapura` 문자열 3개 초안 전체 **0건**. `papers.md:767` 정정 기록("이 논문의 저자를 'Dasgupta, Lang, **Stokes, Tirthapura**'로 적는 자료가 돌아다니는데 **틀렸다.** … Gibbons & Tirthapura는 관련된 다른 논문의 저자다")을 저술가가 117행에서 **일화로 전환**했고, 나아가 `papers.md:767`의 제안("**'인용을 기억으로 만들면 안 되는 이유'의 실물 사례**로 책에 쓸 수 있다")을 그대로 이행했다.
  **의심 식별자 검증:** arXiv ID `1510.01455`의 YYMM은 **2015년 10월**로 빌드 시점(2026-07) 대비 과거다 — **미래 YYMM 자동 ❌ 규칙 비해당**. 형식(`YYMM.NNNNN`) 정상. `papers.md:766`이 **arXiv API 직접 조회 + ICDT 게재 웹 검증**의 이중 경로를 기록했고, 저자 목록도 API 응답에서 왔다. **의심 사유가 성립하지 않으므로 웹 2차 에스컬레이션 불요.**
- **조치:** 없음. **2파에서 유일하게 등장한 식별자이고, 하필 그것이 리서치가 정정한 함정인데 정확히 통과했다.**

### 주장 17 — Bloom filter 수치와 비대칭성 (**이 장 최대 위험 — 문장 단위 검증**)
- **본문:** (119행) "**Redis 공식 문서가** 광고 사용 사례를 직접 예로 든다 — 'Has the user already seen this ad? Has the user already bought this product?' 그리고 보장의 비대칭성을 이렇게 설명한다. 집합에 없다는 답(부정)은 확실하고, 있다는 답(긍정)은 N번에 한 번 틀린다. **문서가 적은 메모리 값은 0.1% 오류율에서 항목당 14.378비트, 1% 오류율에서 9.585비트다.** (같은 조회 기준.) **개념의 원류는 1970년 Bloom의 논문이지만, 방금의 비트 수는 Redis 문서의 값이다.**"
- **판정:** ✅ (**짝짓기까지 정확 — `02_plan.md` 금지 항목 10 준수**)
- **근거:**
  - **수치 짝짓기(가장 흔한 오류 형태)를 원문과 직접 대조했다.** `research/web_stack.md:879~880` — "**'1% error rate requires 7 hash functions and 9.585 bits per item.'** / **'0.1% error rate requires 10 hash functions and 14.378 bits per item.'**" → 본문 "0.1% → **14.378**비트, 1% → **9.585**비트" ✅ **짝이 바뀌지 않았다.** (오류율이 낮을수록 비트가 커지는 방향도 물리적으로 맞다.)
  - 광고 유스케이스 인용 — `web_stack.md:868` "Has the user already seen this ad? Has the user already bought this product?" ✅ **한 글자까지 일치**.
  - 비대칭성 — `web_stack.md:874` 원문 "it can only give an estimation about its presence. So when it responds that an item is **not present** … you can be sure … But **one out of every N positive answers will be wrong**." ✅ 본문의 한국어 서술과 일치.
  - **귀속 분리:** 수치가 든 문장의 주어는 "**문서가**"이고, Bloom(1970)을 언급한 문장에는 **숫자가 없다**. 나아가 마지막 문장이 분리를 명시한다. 서지는 `research/papers.md:723` (C-16-1) — "Burton H. Bloom, … *CACM*, 1970" ✅ 연도 일치.
- **조치:** 없음.

### 주장 18 — Bloom filter 오류 방향의 마케팅적 함의
- **본문:** (121행) "틀리는 쪽은 '안 봤는데 봤다고 판정하는' 경우뿐이다. 그러면 그 사람에게 광고 노출을 한 번 건너뛴다. 반대 방향 — 이미 본 사람에게 또 보여주는 사고 — 는 구조적으로 일어나지 않는다. 광고 기회를 조금 잃을 뿐 사용자를 괴롭히지는 않는 방향이고, 그래서 **보수적으로 안전**하다."
- **판정:** ✅
- **근거:** `research/web_stack.md:876` — "**Martech 번역:** '안 봤다'는 확실하고 '봤다'는 틀릴 수 있다. 즉 **광고를 안 본 사람에게 안 보여주는 실수는 없고, 본 적 없는데 '봤다'고 판정해 노출을 건너뛰는 실수만 있다.** 광고 노출 기회를 약간 잃을 뿐 사용자를 괴롭히지는 않는다 — **보수적으로 안전한 방향이다.**" **오류 방향이 뒤집히지 않았다** — 이 대목은 방향을 반대로 쓰기 쉬운 자리인데 정확하다.
- **조치:** 없음.

### 주장 19 — Count-Min Sketch의 한계
- **본문:** (123행) "Redis 문서가 스스로 강한 경고를 붙인다. 오류율로 결정되는 임계값 아래의 결과는 무시하고 사실상 0으로 취급해야 하며, 낮은 카운트는 잡음으로 봐야 한다는 것이다. 문서는 한 발 더 나가 **균등 분포 스트림의 빈도를 세는 데는 최선의 자료구조가 아닐 수 있다고 인정한다.** CMS는 롱테일을 세는 도구가 아니라 헤비히터를 찾는 도구다. … **개념의 학술적 출처는 Cormode와 Muthukrishnan의 2005년 논문이다.**"
- **판정:** ✅
- **근거:** `research/web_stack.md:904` 원문 — "results coming from a Count-Min sketch **lower than a certain threshold (determined by the error_rate) should be ignored and often even approximated to zero** … **Very low counts should be ignored as noise.**" ✅ / `web_stack.md:910` — "'**This shows that a CMS is maybe not the best data structure to count frequency of a uniformly distributed stream.**'" ✅ 본문의 "인정한다"가 정확한 서술이다(문서가 스스로 한 말). `web_stack.md:914` — "CMS는 **롱테일이 아니라 헤비히터를 찾는 도구**다. '가장 많이 노출된 광고 TOP N' … 에는 맞고, '이 사용자가 이 상품을 몇 번 봤나'(개별 저빈도)에는 안 맞는다" ✅ 본문과 예시까지 일치.
  **귀속 분리:** 논문(Cormode & Muthukrishnan 2005, `papers.md:747` 서지 일치)은 **문단 마지막 한 문장에서 이름·연도만** 등장하고, 앞의 모든 수치·경고는 Redis 문서에 귀속돼 있다 ✅.
- **조치:** 없음.

### 주장 20 — t-digest와 trimmed mean
- **본문:** (125행) "'세션 길이 p50/p90/p99는?'이나 'VIP 임계값을 데이터로 정하자'는 요구에는 t-digest가 쓰인다. **개념의 출처는 Dunning과 Ertl의 2019년 t-digest 논문이다.** 그리고 … **Redis 문서 기준으로** t-digest 명령에는 trimmed mean이 있다. 상하위 컷오프 백분위 바깥의 관측값을 빼고 낸 평균, 즉 이상치를 제외한 평균 객단가다."
- **판정:** ✅
- **근거:** 서지 — `research/papers.md:757` (C-16-5): "Ted Dunning, Otmar Ertl, 'Computing Extremely Accurate Quantiles Using t-Digests,' arXiv:1902.04023, 제출 **2019**-02-11" ✅ 저자·연도 일치. **본문은 논문의 정확도 주장(극단 분위수에서 특히 정확)을 옮기지 않았다** — `메타데이터 확인` 등급에 맞는 절제다. trimmed mean — `research/web_stack.md:929` 원문 "A trimmed mean is the mean value from the sketch, **excluding observation values outside the low and high cutoff percentiles**" ✅ 본문의 한국어 서술과 일치, 귀속도 "**Redis 문서 기준으로**"로 명시 ✅. `web_stack.md:933~934` — "'구매 금액 상위 10%의 기준선은 얼마인가?' — **VIP 세그먼트의 임계값을 데이터로 정한다**" / "**trimmed mean이 특히 유용하다** — '이상치를 뺀 평균 객단가'는 마케팅 리포트에서 실제로 원하는 숫자다" ✅.
- **조치:** 없음.

### 주장 21 — uniqCombined / uniqExact
- **본문:** (131~133행) "`uniqCombined`는 적응형 3단 구조로, 기수가 작으면 배열, 중간이면 해시테이블, 커지면 HyperLogLog로 넘어간다. `uniqExact`는 정확한 답을 주는 대신 문서 표현으로 상태 크기가 '**unbounded growth**'를 갖는다. 문서는 정확한 결과가 꼭 필요한 경우에만 `uniqExact`를 쓰라고 권한다. (**두 문서 모두 발행일 없음 — 2026년 7월 25일 조회 기준. ClickHouse는 26.x 계열 / 2026 기준.**)" + 도달 수 = `uniqCombined` / 정산 대상자 = `uniqExact`
- **판정:** ✅
- **근거:** `research/web_stack.md:169~187` — 3단 구조 원문 "'an array is used'(작은 기수) → 'a hash table is used'(중간) → '**HyperLogLog is used**, which will occupy a fixed amount of memory'(큰 기수)" ✅. `uniqExact` 원문 "the size of the state has **unbounded growth**" ✅ **영문 표현을 그대로 인용** / "**Use the `uniqExact` function if you absolutely need an exact result.**" ✅. 실무 번역 — `web_stack.md:190~192`: "'이번 캠페인 도달 유니크 사용자 수' → `uniqCombined`로 충분. **대시보드 숫자가 0.5% 틀려도 아무도 안 죽는다.** / '이 쿠폰을 실제로 받은 사용자 수(정산 대상)' → `uniqExact`. **돈이 걸리면 근사는 안 된다.**" ✅ 본문 133행과 문자열 수준 일치. 135행의 "며칠간 원인 추적 → 원인은 버그가 아니라 함수 선택" 사고도 `web_stack.md:192` 그대로.
  **버전 표기 ✅** — `web_stack.md:142`: "책에 특정 패치 버전을 박지 말고 **'26.x 계열 / 2026 기준'** 수준으로 쓰는 편이 안전하다", `web_stack.md:1319` (§4-7)도 재차. **본문이 이 문구를 그대로 썼고 연도를 일자로 박지 않았다.** `02_plan.md` §B의 `연도 추정` 규율 준수.
- **조치:** 없음.

### 주장 22 — 판별 질문 4개의 근거 등급 분리
- **본문:** (139~142행) "근거가 단단한 것부터 순서대로다. - **이 숫자로 누가 돈을 받거나 잃는가.** … **리서치가 명시적으로 이 선을 긋는다.** - **이 숫자에 집합 연산이 붙는가.** … / **아래 둘은 리서치가 내린 판정은 아니다.** 위 두 기준에서 자연스럽게 따라오는 실무 어림에 가까우니, 규칙으로 굳히기보다 점검 항목으로 쓰는 편이 낫다."
- **판정:** ✅ (**모범 사례 — 이 장에서 가장 정직한 문단**)
- **근거:** 앞의 둘은 근거가 있다 — 돈 기준은 `research/web_stack.md:191`("돈이 걸리면 근사는 안 된다") + `:943`("**어느 숫자가 어느 쪽인지 판별하는 능력이 Martech 개발자의 핵심 역량이다**"), 집합 연산 기준은 `research/papers.md:769`(Theta Sketch가 필요한 이유). 뒤의 둘("다른 리포트와 대조되는가" / "회사 밖으로 나가는가")은 **어느 리서치 파일에도 없다** — 저술가의 추론이다. 그리고 본문이 **그 사실을 문장으로 밝혔다.** 근거 있는 것과 없는 것을 같은 불릿 목록 안에서 등급을 나눠 표시한 유일한 대목이다.
- **조치:** 없음. **1파 01장 주장 3(저술가 예시를 근거처럼 제시)의 실패를 정확히 뒤집은 형태다 — 통권 편집 시 이 문단을 기준 사례로 삼을 만하다.**

### 주장 23 — HLL++ 개선판과 BigQuery·Redis 구현
- **본문:** (146행) "Heule, Nunkesser, Hall의 2013년 'HyperLogLog in practice'는 작은 카디널리티에서의 편향 보정, 64비트 해시, 희소 표현 같은 실무적 개선을 담았고, **BigQuery의 `APPROX_COUNT_DISTINCT`나 Redis의 `PFCOUNT`가 실제로 구현하는 쪽은 원 논문 그 자체보다 이 개선판 계열에 가깝다.**"
- **판정:** ✅ (**Tier 2 금지 비해당**)
- **근거:** `research/papers.md:737~742` (C-16-3). 서지 — "Stefan Heule, Marc Nunkesser, Alexander Hall, 'HyperLogLog in practice,' *EDBT 2013*" ✅ 저자 3인·연도 일치. 개선 3항목 — "**작은 카디널리티 영역의 편향, 64비트 해시 필요성, 희소 표현**" ✅ 본문과 일치. 구현 주장 — `papers.md:742`: "**BigQuery의 `APPROX_COUNT_DISTINCT`, Redis의 `PFCOUNT` 등이 실제로 구현하는 건 원 논문이 아니라 이 개선판 계열이다.**" ✅ **문자열 수준 일치**(본문이 "가깝다"로 한 단계 약화했으니 근거보다 강하지 않다).
  **`02_plan.md` §B의 Tier 2 금지 대조:** 금지 대상은 "**Tier 2 전 항목의 버전·수치**"다. 여기서 BigQuery는 **함수 이름 하나로만 등장하고 버전도 수치도 붙지 않았다.** 위반 아님. (1파 03장에서 Snowflake·BigQuery가 예시 나열로 등장했을 때와 같은 판정이다.)
- **조치:** 없음. (근거 등급은 `메타데이터 확인`이므로 리서처의 서술을 그대로 옮긴 상태다. 본문이 "가깝다"로 완화해 이미 안전 범위 안에 있다.)

### 주장 24 — 빅인사이트 채용 공고
- **본문:** (177~183행) "**2026년 7월 원티드에 올라와 있던** 국내 마테크 회사 빅인사이트의 Data Platform Engineer 공고를 보면 … **MongoDB, Vitess/MySQL 샤딩 환경, ClickHouse, 그리고 Apache Iceberg 기반 데이터 레이크.** 여기에 **Flink 기반 스트리밍·배치 워크로드와 Argo Workflows 파이프라인**이 붙는다." + 인재상 인용 2건
- **판정:** ✅
- **근거:** `research/community.md:141~166`. 저장소 4종 — JD 원문에 "`Apache Iceberg 기반 데이터 레이크 테이블 운영`", "`MongoDB 기반 데이터 저장소 운영`", "`Vitess/MySQL sharding 환경 운영`", "`ClickHouse 기반 OLAP/분석 워크로드 운영`" ✅ **4종 전건 확인**. "`Flink 기반 streaming/batch 워크로드 운영`" ✅, "`Argo Workflows 기반 배치/데이터 처리 파이프라인 설계, 운영, 장애 대응`" ✅. 인용 2건 — "**DB, 스토리지, 워크플로우, 인프라를 분리해서 보지 않고 전체 병목을 추적할 수 있는 분**"(`community.md:166`) ✅ **한 글자까지 일치**, "**실패한 워크플로우를 단순 재실행하지 않고 원인과 재발 방지까지 보는 분**"(`community.md:165`, `:778`) ✅ **한 글자까지 일치**. 회사 성격은 `community.md:811`("자체 개발 마케팅 솔루션 Bigin Ads와 Bigin CRM을 서비스합니다") ✅. 시점 — `community.md:143`이 "조회 시점 active 공고 **1건**"으로 기록했고 본문이 "2026년 7월 원티드에 올라와 있던"으로 **문장 안에** 넣었다 ✅ (`02_plan.md` §B 요구).
- **조치:** 없음. (엄밀히 하려면 "2026년 7월 원티드 **active 공고 기준**"이라는 리서치 표현을 그대로 쓸 수도 있으나, 현재 표현이 같은 뜻을 전달하므로 정정 대상 아님.)

---

### 06장 요약

**필수 정정 (⚠️ 2건 — 둘 다 날짜 표기 축약으로 해소. BLOCKING 아님):**
- ⚠️ 주장 12 — Iceberg `1.11.0 / 2026-05-19` → **`1.11.0 / 2026-05`** (`web_stack.md:258`·`:1302` 명시 지시, GitHub `20 May` vs 아카이브 `2026-05-19` 하루 차)
- ⚠️ 주장 13 — Pinot `1.5.1 / 2026-06-30` → **`1.5.1 / 2026년 중반`** (`web_stack.md:534`·`:1302` 명시 지시, GitHub `05 Jun` vs 아카이브 `2026-06-30` **약 25일 차**)

**BLOCKING 항목:** **없음.** ❌ 0건 / 🕒 0건 — **이 장에서 검증 불가로 남은 항목은 없다.** (주장 9 Druid는 검토 결과 **고지 충분 + 버전도 아카이브 연도 확정 예외**로 ✅ 판정했다.)

**서지 함정 2건 — 전건 통과:**

| 함정 | 요구 | 본문 상태 | 판정 |
|---|---|---|---|
| Theta Sketch 저자 | `Dasgupta, Lang, **Rhodes, Thaler**` / arXiv:1510.01455 | 115행에 정확히 그대로. `Stokes`·`Tirthapura` **grep 0건** | ✅ |
| C-Store 원본 DOI | 재수록본 DOI `10.1145/3226595.3226638` 사용 금지 | `3226595`·`10.1145`·`C-Store`·`Stonebraker` **grep 0건** — 이 장은 C-Store를 아예 인용하지 않는다 | ✅ |

**HLL·Bloom 수치 귀속 — 문장 단위 검증 결과:**

| 수치 | 본문 위치 | 문장의 귀속 주어 | 같은 문장의 논문 저자명 | 판정 |
|---|---|---|---|---|
| 12KB / 0.81% | 107행 | **"Redis 공식 문서는 … 적는다"** | 없음 | ✅ |
| 14.378비트 (0.1%) / 9.585비트 (1%) | 119행 | **"문서가 적은 메모리 값은"** | 없음 | ✅ |
| — | 109행 (Flajolet 외 4인) | 논문 서지 | — | **숫자 0개** ✅ |
| — | 119행 말미 (Bloom 1970) | 개념 원류 | — | **숫자 0개** ✅ |
| — | 123행 말미 (Cormode & Muthukrishnan 2005) | 개념 출처 | — | **숫자 0개** ✅ |
| — | 125행 (Dunning & Ertl 2019) | 개념 출처 | — | **숫자 0개** ✅ |

→ **저술가의 자기 보고("물리적으로 분리")는 사실이다.** 나아가 109행·119행이 **분리 사실 자체를 독자에게 설명**해, `02_plan.md` 금지 항목 10을 회피가 아니라 교육 소재로 전환했다.

**버전 대조 결과 (Tier 1 표 §4-1 대조):**

| 본문 표기 | 근거 | 판정 |
|---|---|---|
| Iceberg 1.11.0 / **2026-05-19** | `web_stack.md:253` 값은 맞으나 `:258`이 일자 금지 | ⚠️ |
| Pinot 1.5.1 / **2026-06-30** | `web_stack.md:527` 값은 맞으나 `:534`가 일자 금지 | ⚠️ |
| Trino 483 / 2026-07-17 | `:584` 공식 릴리스 노트 **연도 명시·확정**, 상충 없음 | ✅ |
| DuckDB 1.5.5 / 2026-07-22, LTS 1.4.5 계열 | `:638` 공식 뉴스 페이지 **표기·확정** | ✅ |
| **ClickHouse "26.x 계열 / 2026 기준"** | `:142`·`:1319` 지시 그대로 — **연도를 일자로 박지 않았다** | ✅ |
| Druid 37.0.0 / 2026-05-06 | `:785` **Tier 2 버전 예외(아카이브 연도 확정)** | ✅ |

**금지 항목 (6장 해당분):** 0건. **ClickBench 수치 0건**(배제 사유만 서술), **Tier 2 버전·수치 0건**(BigQuery는 함수명만 등장, 버전·수치 없음), **Redis를 "오픈소스"로 단정 0건**(`오픈소스`·`OSI` 문자열 이 장 전체 0건).

**총평:** 서지 함정이 몰린 장인데 **함정 2건·수치 귀속 6건이 전부 통과**했다. 특히 근사 자료구조 절은 "어떤 알고리즘인가"와 "누가 어떤 파라미터로 구현했는가"를 **문장 단위로 분리**했고, 판별 질문 문단(139~142행)에서는 리서치 판정과 저술가 추론을 같은 목록 안에서 등급을 나눠 표시했다 — 2파에서 근거 등급 표기가 가장 정교한 대목이다. 남은 ⚠️ 2건은 **값이 틀린 게 아니라 리서치가 "박지 말라"고 한 자릿수를 박은 것**이고, 각각 문자 세 개·다섯 개 삭제로 끝난다. **검증 불가 항목이 아니므로 Phase 5를 차단하지 않는다.**

---

## 금지 항목 스캔 결과 (2파 4~6장)

> `02_plan.md` 185~224행 규율 전 항목을 3개 초안 전체에 grep으로 대조했다. **BLOCKING 위반 0건.**

| # | 금지 항목 | 결과 | 확인 내용 |
|---|---|---|---|
| 1 | **CDP 4분류**(Data/Analytics/**Campaign**/**Delivery**) | ✅ 위반 없음 | `Campaign`·`Delivery` 문자열 3개 초안 전체 **0건**. 2파는 CDP 카테고리 논의를 하지 않는다(3장에서 마감). |
| 2 | **CDP Institute 기관 정의문** | ✅ 위반 없음 | `persistent`·`CDP Institute` **0건**. |
| 3 | **CEM / CXM 비교표** | ✅ 위반 없음 | `CEM`·`CXM` **0건**. |
| 4 | **"DMP = 서드파티 쿠키, CDP = 퍼스트파티" 통설** | ✅ 위반 없음 | `서드파티`·`퍼스트파티`·`third-party` **0건**. |
| 5 | **Ads Data Hub 20/50/10 임계값 전용** | ✅ 위반 없음 | `Ads Data Hub`·`AMC`·`클린룸` **0건**. |
| 6 | **PIPA 과징금 % / 정보통신망법 매출 6%** | ✅ 위반 없음 | `과징금`·`과태료`·`PIPA`·`정보통신망법` **0건**. 6장 87행이 삭제 요청을 다루지만 "**고객 데이터에는 삭제 요청이 법으로 강제된다**"까지만 쓰고 조문·수치를 붙이지 않았다 — 10장 본진을 정확히 보존했다. |
| 7 | **SKAdNetwork 세부** | ✅ 위반 없음 | `SKAdNetwork`·`SKAN` **0건**. |
| 8 | **Snowplow·RudderStack·Redis를 "오픈소스"로 단정** | ✅ 위반 없음 | 히트 4건 전부 **금지의 반대 방향**이다. 05장 51행 "**Snowplow의 핵심 컴포넌트는 OSI 오픈소스가 아니다**"(부정), 49행 "오픈소스 CDP 스택"은 **독자 통념을 인용부호로 제시한 뒤 즉시 반박**하는 구조, 60행 "확인하지 못한 것을 '오픈소스'라고 적을 수는 없으니 **여기서도 단정하지 않는다**"(RudderStack·Redis 판단 유보). 04장 29행의 "오픈소스 저장소"는 Meta Robyn의 배포 형태를 가리키는 `papers.md:1110` 전사이며 라이선스 단정이 아니다. |
| 9 | **Tier 2 항목의 버전·수치** | ✅ 위반 없음 | `Redpanda`·`Pulsar`·`Snowflake`·`Airflow`·`Dagster`·`Redshift`·`StarRocks`·`Delta Lake`·`Hudi`·`Spark` **전부 0건**. 유일한 Tier 2 히트는 06장 146행의 `BigQuery`인데 **함수명(`APPROX_COUNT_DISTINCT`) 하나로만 등장하고 버전도 수치도 없다** — 금지 대상은 버전·수치이므로 위반 아님(1파 03장 판정과 동일 기준). 05장은 Tier 2 히트 **0건**. |
| 10 | **Theta Sketch 저자 오귀속**("Stokes, Tirthapura") | ✅ 위반 없음 | `Stokes`·`Tirthapura` **0건**. 06장 115행이 정정된 저자 4인(`Dasgupta, Lang, Rhodes, Thaler`)과 `arXiv:1510.01455`를 정확히 썼고, 117행에서 오귀속 존재 사실 자체를 일화로 다뤘다. |
| 11 | **Gordon 2019에 구체 수치 귀속** | ✅ 위반 없음 | `Gordon`·`Zettelmeyer`·`Moakler`·`2201.07055` **0건**. |
| 12 | **LLM 생성 카피의 효과 크기** | ✅ 위반 없음 | `LLM`·`생성 카피`·`카피 생성` **0건**. |
| 13 | **DMARC를 "표준"이라 부르는 것** | ✅ 위반 없음 | 히트 1건 — 04장 34행 12건 표의 "`DMARC를 "표준"이라 부르는 것 \| RFC 7489는 Informational 분류`". **금지된 관행을 이름으로 지목하는 행이지 그 관행을 저지르는 문장이 아니다.** `papers.md:1115` 전사이며 본문 어디에도 DMARC를 표준이라 부르는 서술이 없다. |
| 14 | **Goldfarb & Tucker / Berman / Blake 범위 한정 누락** | ✅ 위반 없음 | `Goldfarb`·`Berman`·`Blake`·`Shapley`·`eBay`·`Tucker` **전부 0건**. **2파 3개 장이 인과·어트리뷰션 논의를 하나도 당겨오지 않고 10·11장 본진을 온전히 보존했다** — 4장이 학술 인용 밀도가 가장 높은 장인데도 세그먼트·LTV·이탈 모형에만 머물렀다. |
| 15 | **C-Store 재수록본 DOI를 원본으로** | ✅ 위반 없음 | `3226595`·`10.1145`·`C-Store`·`Stonebraker` **전부 0건**. 06장이 컬럼 지향 저장을 다루면서도 C-Store를 아예 인용하지 않아 함정 자체가 발생하지 않았다. |
| 16 | **ClickBench 수치** | ✅ 위반 없음 | 히트 1건 — 06장 75행의 **배제 선언**("이 책은 ClickBench 수치를 쓰지 않는다 … 운영 주체가 ClickHouse 쪽이고"). **수치는 0건.** 같은 문장의 `10ms P95`·`100,000 queries per second`는 ClickBench가 아니라 **Pinot 프로젝트 자체 문서 표방 수치**이며, 필수 조건("독립적으로 검증된 벤치마크가 아니다")이 바로 다음 문장에 붙어 있다(`web_stack.md:559` 지시 이행). |

### 부가 스캔

- **`(사실 확인 필요)` 미해소 마커:** 3개 초안 전체 **0건** ✅ (`TODO`·`TBD`·`FIXME`·`XXX`도 0건). 저술가 3인의 자기 보고와 일치.
- **의심 식별자 (arXiv·DOI):** 2파에 등장하는 **유일한 식별자는 `arXiv:1510.01455`(06장 115행)** 하나다.
  - 형식 정상(`YYMM.NNNNN`), YYMM = **1510 = 2015년 10월**로 빌드 시점(2026-07) 대비 **과거** → **미래 YYMM 자동 ❌ 규칙 비해당.**
  - 근거 경로가 이중이다 — `papers.md:766`이 **arXiv API 직접 조회**(저자 목록 포함)와 **ICDT 2016 LIPIcs 페이지 웹 확인**을 함께 기록했고, `papers.md:767`이 오귀속 사례까지 명시했다.
  - **의심 사유가 성립하지 않으므로 구속력 있는 웹 2차 검증 대상이 아니다.** (04장 32행·84행의 `DOI` 히트는 "DOI 없음"·"DOI 같은 서지 레코드"라는 **일반 명사 언급**이며 식별자 값이 아니다.)
- **시점 병기 (`02_plan.md` §B) — 1파 기준의 2파 이행 여부:**
  - **1파에서 확립된 기준("발행일 없는 출처에 조회 시점 병기")이 2파에서 지켜졌다.** 발행일 없는 1차 문서 인용 **11건 전부**에 조회 시점이 문장 안에 들어가 있다 — dbt(04장 128행), Snowplow(05장 37행), Confluent(05장 76행), KIP-98(05장 104행), Flink 시간 개념(05장 128·136행), ClickHouse MergeTree(06장 48행), Trino(06장 61행), Redis HLL(06장 107행)·Bloom(06장 119행), ClickHouse uniq 함수(06장 131행), DuckDB(06장 171행). **1파 01장 Trailhead·02장 Segment Spec에서 새던 패턴이 2파에서는 한 건도 재발하지 않았다.**
  - 채용 공고 수치 — 06장 177행 "2026년 7월 원티드에 올라와 있던" ✅ 문장 안 병기.
  - Insider 문서 — 04장 90행 "2026년 7월 25일 조회 기준", 146행 "페이지 표기 2026년 4월 12일, 2026년 7월 25일 조회" ✅ **표기일과 조회일 양쪽 병기**.
  - 논문 — 04장 84행 "(2026년 7월 25일 조회 기준)" ✅.
  - **미이행 2건은 버전 일자 쪽이다** — 06장 Iceberg·Pinot(주장 12·13, ⚠️).

**금지 항목 스캔 총평: 16개 항목 전건 통과.** 2파의 특징은 **금지 항목을 피하는 데 그치지 않고 그 사유를 본문에 노출한 대목이 다섯 곳**이라는 점이다 — 05장 51~60행(Snowplow 라이선스 + RudderStack·Redis 판단 유보), 06장 75행(ClickBench 배제 사유), 06장 77행(Druid 성격 규정이 통념임), 06장 109·119행(HLL·Bloom 수치의 출처 분리), 06장 117행(Theta Sketch 오귀속 일화). 후속 편집 단계에서 이 제약들이 실수로 되살아나는 것까지 막아두었다. **2파에서 Phase 5를 차단하는 금지 항목 위반은 없다.**

---

## 2파(4~6장) 종합

### 장별 판정

| 장 | 주장 | ✅ | ⚠️ | ❌ | 🕒 | 판정 |
|---|---|---|---|---|---|---|
| 04장 | 21 | 17 | 4 | 0 | 0 | 수정 요망 |
| 05장 | 22 | 18 | 4 | 0 | 0 | 수정 요망 |
| 06장 | 24 | 21 | 3 | 0 | 0 | 수정 요망 |
| **계** | **67** | **56** | **11** | **0** | **0** | **BLOCKING 0건** |

### ❌ / 🕒 목록 (BLOCKING)
**둘 다 0건.** 2파에서 사실 오류(❌)로 판정된 항목도, 검증 불가(🕒)로 남은 항목도 없다. **2파에는 Phase 5를 차단하는 사실 항목이 없다.**

### 필수 정정 (⚠️ 중 저술가 재량이 없는 2건)
1. **06장 81행** — Iceberg `1.11.0 / 2026-05-19` → **`1.11.0 / 2026-05`**
   근거: `web_stack.md:258`("책에는 `1.11.0 / 2026-05` 수준으로 쓰는 게 안전하다"), `:1302`. GitHub `20 May` vs Apache 아카이브 `2026-05-19` 하루 차.
2. **06장 75행** — Pinot `1.5.1 / 2026-06-30` → **`1.5.1 / 2026년 중반`**
   근거: `web_stack.md:534`("**특정 일자를 박지 말 것**"), `:1302`. GitHub `05 Jun` vs 아카이브 `2026-06-30` **약 25일 차**.

> 두 항목 모두 **값 자체는 Apache 배포 아카이브의 전체 타임스탬프로 검증됐다** — 검증 불가(🕒)가 아니다. 문제는 두 1차 소스가 갈리는 자리에서 리서치가 판단을 유보한 채 "일자를 박지 말라"고 두 번 명시했는데 본문이 한쪽을 일자까지 단정했다는 것이고, 해소는 **월 단위 약화**다. 근거 강도 문제이므로 라벨은 ⚠️이지만, **리서치의 명시적 지시가 있으므로 저술가 재량으로 덮을 수 없다.** 해소 비용은 각각 문자 세 개·다섯 개 삭제다.

### ⚠️ 목록 (9건)
- **04장** 주장 3(표는 여섯 행인데 본문은 "넷"), 주장 4(표 10번이 예고한 5장에 Kafka 원 논문 서술 없음), 주장 9(84행 고지가 한 절에만 걸려 뒤 두 절 논문 4편 미포함), 주장 21("이유의 절반쯤" — 근거 없는 비중)
- **05장** 주장 10(LINE을 "국내 사례"로 귀속), 주장 16(Akidau "서지와 요지까지 확인"이 실제 등급보다 높음), 주장 20(비용·결정 규칙 단정문 3건이 고지 블록 밖), 주장 15(선택 — Flink 인용이 2.0 문서 브랜치)
- **06장** 없음

### 2파 총평

**인용 정확도는 1파보다 높다.** 원문 대조한 인용 **30건 이상이 전건 일치**했고, 저자·연도·게재지·권(호)·arXiv ID·비트 수 짝짓기에 오류가 하나도 없다. 특히 사전에 고위험으로 지목된 지점 — 4장 학술 인용 12편, 5장 버전 4건 + Snowplow 라이선스, 6장 HLL·Bloom 수치 귀속과 Theta Sketch 저자 — **전부 통과했다.**

**실패 패턴이 1파와 다르다.** 1파의 ❌ 2건은 "출처를 묶어서 귀속"하다 생긴 것이었는데, **2파에서는 인용을 묶어 귀속한 사례가 검출되지 않았다** — 인용 30건 이상을 원문 대조했고 출처 줄이 실제 출처와 어긋난 건은 없었다. 남은 11건의 ⚠️는 **고지 문장의 범위·강도**와 **버전 자릿수** 쪽에 몰려 있다 — 고지 자체는 정확한데 절 단위로만 걸려 있거나(04-9, 05-20), 확인 수준을 한 칸 높여 말하거나(05-16), 근거 없는 부가어가 붙거나(04-21, 05-10). **즉 2파의 문제는 "무엇을 인용했는가"가 아니라 "인용의 등급을 어디까지 표시했는가"다.** 이건 인용 오류보다 고치기 쉽다.

**오프닝 장면은 별도로 점검했고 결함이 아니다.** 05·06장 오프닝은 리서치에 대응 사고 기록이 없지만, `profiles/tech-book/scaffolds.md:76, 80`이 "상황 가정"·"실패 장면(in medias res)"을 오프닝 메뉴에 명시 승인하고 있어 **문체 장치이지 사실 주장이 아니다.** 게다가 05장 오프닝의 20분·30분·순서 역전 구조는 `web_stack.md:223`에 그대로 있다(05장 요약 「오프닝 장면의 지위」 참조). 1파 01장에서 문제가 됐던 "저술가가 직접 채운 예시를 근거처럼 제시" 패턴과는 위치도 성격도 다르다.

**저술가 자기 보고의 신뢰도:** 3장 모두 자기 보고가 직접 대조에서 사실로 확인됐다. 특히 6장 저술가의 "수치와 논문 저자명이 물리적으로 분리돼 있다"는 보고는 문장 단위 검증에서 정확했고, 4장 저술가의 "가정을 모델의 속성으로 서술했다"는 보고도 귀속 주어 분석에서 확인됐다.

**2파에서 Phase 5를 차단하는 사실 항목은 없다(❌ 0 / 🕒 0).** 다만 위 필수 정정 2건은 최종 확정 전에 반영해야 한다.

---

## 7~12장 저술가에게 — 사실 규율 경고 (2파 검증에서 도출)

> 1·2파 6개 장을 검증하며 **반복해서 나타난 실패 형태**와, **7~12장에 몰려 있는 미소진 지뢰**를 함께 적는다. 앞의 여섯 장이 대체로 잘 지켰기 때문에, 남은 위험은 오히려 **아직 안 쓴 장에 집중돼 있다.**

### A. 1·2파에서 반복된 실패 3형 — 7~12장에서 반복하지 마라

1. **고지의 적용 범위를 절 단위로 잡지 마라.** 2파 ⚠️ 9건 중 **3건**이 이것이다(04-9, 05-16, 05-20). "이 절에 인용한 논문들은…" 식으로 쓰면 두 문단 뒤 같은 등급의 인용이 무방비가 된다. **장 첫머리나 각 인용 문장 옆에** 붙여라.
2. **확인 수준을 한 칸 올려 말하지 마라.** `papers.md:9~13`의 4등급은 엄격하다 — `메타데이터 확인`은 **초록을 못 읽었다는 뜻**이다. "요지까지 확인했다"(05-16)는 표현은 `초록 확인` 등급을 함의한다. 논문을 인용할 때 **`papers.md` 신선도 원장(1142~1219행)에서 해당 항목의 확인 수준을 먼저 찾아보고**, 그 등급의 표현만 써라.
3. **근거 있는 문장에 근거 없는 부가어를 붙이지 마라.** "이유의 **절반쯤**"(04-21), "**국내** 사례로는"(05-10). 인용은 정확한데 수식어 하나가 근거 밖으로 나간 형태이고, 이게 2파의 유일한 신규 사실 오류였다.

### B. 7~12장에 남아 있는 지뢰 (아직 하나도 안 터졌다)

**`02_plan.md` 금지 13항목 중 6~12번이 전부 7~12장 소재다.** 1·2파는 이 항목들을 건드릴 일이 없어 0건이었을 뿐, **본진은 지금부터다.**

- **10장(프라이버시·규제) — 가장 위험한 장.**
  - **PIPA 과징금 %**: 3% vs 10% 상충, 둘 다 law.go.kr 원문 미확인. **과징금(제64조의2)과 과태료(제75조)는 다른 제재다 — 섞어 쓰면 즉시 ❌.**
  - **정보통신망법 2026-07-07 개정의 "매출액 6%"**: 원문 미확인. 쓰지 마라.
  - **SKAdNetwork 세부**(deprecation 여부·버전·conversion value 비트 수): 전부 확인 불가.
  - **Ads Data Hub 20/50/10 임계값**을 AMC·Snowflake 등 다른 클린룸에 전용 금지.
  - **EU AI Act·Privacy Sandbox**는 "2026년 7월 기준" 명시 필수. `papers.md:1133` — Grib et al. (2026) "The Rise and Fall of Google's Privacy Sandbox"는 **초록 미확인이니 제목의 "Fall"로 결론을 추정하지 마라.**
  - 6장 87행이 삭제 요청을 "법으로 강제된다"까지만 쓰고 조문을 안 붙인 것이 좋은 선례다 — 10장에서도 **조문 번호를 쓸 거면 law.go.kr 원문 확인이 선행돼야 한다.**

- **11장(어트리뷰션·인과) — 범위 한정 3건이 전부 여기 있다.**
  - **Goldfarb & Tucker (2011)**: 종속변수는 **구매 의향**이지 매출이 아니고, 매체는 **온라인 디스플레이 광고**다. "개인화는 역효과다"로 일반화 금지.
  - **Berman (2018)**: Shapley의 개선 효과에 **"시장 전환율이 너무 높지 않을 때"** 조건이 붙는다. 조건을 빼고 인용 금지. 반대로 `papers.md:1094`는 **"라스트터치를 '부정확하지만 실용적'이라고 쓰면 연구 결과와 어긋난다 — 그 강도를 희석하지 마라"**고도 지시한다. **양방향으로 조심할 것.**
  - **Blake et al. (2015)**: "온라인 광고는 효과 없다"가 아니다. ①브랜드 키워드 단기 효과 없음 ②비브랜드에서 신규·저빈도 고객에게는 효과 있음 ③지출 배분 때문에 평균 수익률 음수. **"eBay라는 이미 강한 브랜드"라는 맥락 병기 필수.**
  - **Gordon 2019에 수치 귀속 금지** — 그 논문은 초록이 403으로 막혀 한 줄 요약만 확보됐다. 수치가 필요하면 **Gordon, Moakler & Zettelmeyer (2023), arXiv:2201.07055**(`초록 확인` 등급)를 써라.
  - **MMM**: `papers.md:1088` — "MMM 결과를 **점 추정치가 아니라 분포로** 다루라. 근거는 벤더 자신의 문서다." Meridian(베이지안 계층 모델)과 Robyn(Ridge + Nevergrad)은 **같은 데이터에 다른 답을 낸다.** 단 `papers.md:1134`는 Robyn 방법론이 **웹 검색 기반이고 저장소를 직접 파싱하지 않았다**고 기록했다 — 방법론 세부를 쓸 거면 1차 확인이 선행돼야 한다.

- **9장(채널·발송) — 근거 강도가 다른 두 항목을 섞지 마라.**
  - **Send-time optimization은 업계 관행이다.** 최상위 저널 검증이 없다. 반면 **발송 빈도·피로도에는 학술 근거가 있다**(Godfrey, Seiders & Voss 2011 *JM*의 빈도 역U자 / Zhang, Kumar & Cosguner 2017 *JMR*). **단 둘 다 `메타데이터 확인`이라 구체 수치·결론 방향 귀속 금지** — 4장 주장 12(BG/NBD 가정을 "모델의 속성"으로 서술)의 문장 설계를 그대로 가져다 써라.
  - **벤더가 "AI 발송 시각 최적화"를 팔 때와 "빈도 상한"을 말할 때 근거 강도가 다르다** — 이 대비 자체가 9장의 핵심 소재다.
  - **DMARC를 "표준"이라 부르지 마라.** RFC 7489는 **Informational**이다. Standards Track은 **SPF(RFC 7208)·DKIM(RFC 6376)**뿐이다. 4장 표가 이 항목을 "9장"으로 예고해뒀으니 **9장이 이 판정을 실제로 다뤄야 한다.**
  - **LLM 생성 카피의 효과 크기 주장 금지** — `papers.md:1127`은 근거 부재를 명시하고 "**후보 생성량 증가 → A/B 검증**" 프로세스 관점으로 서술하라고 권한다.

- **8장 — 4장이 두 번 예고했다.** 4장 26·27행 표가 Lambda·Kappa를 "이 장·**8장**"으로, 28행이 Feature store를 "**8장**"으로 예고했고, 4장 52행이 "두 아키텍처가 실제로 어떤 모양이고 왜 그런 구조가 필요한지는 **실물 사례를 하나 놓고 8장에서 본다**"고 약속했다. 5장 187·199행도 8장을 두 번 참조한다. **`web_stack.md:1253~1264`의 Pinterest 사례("one definition, many runtimes", 2026-05-21 발행일 확정)가 그 실물 사례로 준비돼 있다** — 리서치가 "챕터 하나의 앵커 사례로 쓸 만하다"고 지목한 항목이다.

### C. 지금 즉시 처리할 것 — 4장이 5장에 넘긴 미이행 약속

4장 32행 표가 **Kafka 원 논문의 위상(NetDB'11 워크숍 논문, DOI 없음)을 "5장"에서 다룬다고 예고했는데 5장에 그 서술이 없다.** 근거는 `papers.md:785~791`(C-17-2)에 확보돼 있다. **5장 64행 뒤에 한 문단을 넣는 것을 권한다**(구체 문안은 04장 주장 4의 조치 항목 참조). 8장에서 Lambda·Kappa를 다룰 때 함께 처리해도 되지만, 그러려면 4장 표의 "5장"을 "8장"으로 고쳐야 한다.

### D. 잘하고 있는 것 — 계속 유지할 3가지

1. **발행일 없는 출처에 조회 시점 병기** — 2파에서 11건 전부 이행했다. 1파에서 두 번 샜던 항목이고, 지금 습관이 잡혔다.
2. **확인한 것과 확인 못 한 것을 문장에서 분리** — 4장 90행(URL은 확인, 본문은 미확인), 6장 77행(버전은 확인, 아키텍처는 미확인)이 모범이다.
3. **리서치 판정과 저술가 추론을 같은 목록에서 등급을 나눠 표시** — 6장 139~142행이 2파 최고의 대목이다. "**아래 둘은 리서치가 내린 판정은 아니다**"라는 한 줄이 전체 목록의 신뢰도를 지킨다. 7~12장에서 실무 어림을 제시할 때마다 이 형식을 써라.

---

## 07장 — 1차 검증

**검증일:** 2026-07-26 / 대상 `chapters/07_draft.md` (style 합의 후) / 1차 대조 `research/web_privacy.md`·`web_stack.md`·`web_products.md`·`web_gaps.md`·`papers.md`
**`(사실 확인 필요)` 주석: 0건** (grep 확인 — 저술가 자기 보고 사실).

### ✅ 확인됨

**주장 1 — 여는 Apple 인용 (7·9~11행)**
- **본문:** `"Unless you receive permission from the user to enable tracking, the device's advertising identifier value will be all zeros and you may not track them as described above."` / "Apple, App Store 사용자 프라이버시·데이터 이용 페이지 (발행일 표기 없음 — 2026년 7월 25일 조회 기준)"
- **근거:** `web_privacy.md:152` — **영문 문자열 전건 일치**(all zeros 포함). 발행일 없는 출처에 조회 시점 병기 = 2파 D-1 항목 이행.
- **조치:** 없음.

**주장 2 — Redis 자료구조 표와 Bitmap 수치 (27~34행)**
- **본문:** "Bitmap | '이 사용자가 오늘 방문했나?' (1천만 명 ≈ 1.25MB)"
- **근거:** `web_stack.md:485` — "**Bitmap** | ... | 사용자당 1비트 — 1천만 명 = 약 1.25MB". 일치.
- **⭐ 금지 항목 10 회피 확인:** 표의 HyperLogLog·Bloom filter 행은 **이름과 대응 질문만 적고 수치가 0건**이다(`0.81%`·`12KB`·`14.378비트` 전부 미등장). `web_stack.md:860`에 "HLL은 12KB다"가 있는데도 가져오지 않았다 — 원 논문 오귀속 위험을 원천 차단한 형태.
- **조치:** 없음.

**주장 3 — Aerospike (44행)**
- **본문:** "인덱스는 메모리에 두고 데이터는 SSD에 두는 구조라 수억 프로필 규모에서 전량 메모리보다 비용이 낫고, 토스 피처 스토어의 온라인 스토어가 이것이며 Feast(0.65.0 / 2026 기준)도 온라인 스토어 목록에 이걸 추가했다."
- **근거:** `web_stack.md:819`("하이브리드 메모리/SSD 아키텍처(인덱스는 메모리, 데이터는 SSD)... 수억 프로필을 밀리초에 조회해야 하는데 전량 RAM은 비용이 감당 안 될 때... 토스 피처 스토어의 온라인 스토어가 Aerospike이고, Feast 0.65.0이 Aerospike 온라인 스토어를 추가했다") + `:966` + `:1172`. 4요소 전건 일치.
- **버전 표기 판정(§B:219 관련):** 계획서 §B는 `연도 추정` 4항목(ClickHouse·Redis·Feast·rudder-server)을 "**26.x 계열 / 2026 기준**" 형태로 쓰라고 했다. 본문은 "**0.65.0 / 2026 기준**"이다. **일탈 아님으로 판정한다** — `web_stack.md:693`이 이 항목을 정확히 `**[버전: 0.65.0 / 2026 기준]**`으로 기록했고(원본 문자열 일치), "26.x 계열"은 캘린더 버저닝 제품용 템플릿이라 0.x 제품인 Feast에는 적용되지 않는다. §B의 실질 요구(**연도를 확정으로 박지 말고 "기준"을 병기**)는 충족됐다. `web_stack.md:1297`의 "이 넷은 본문에서 특정 일자를 주장하지 않는다"도 지켜졌다(릴리스 일자 미등장).
- **조치:** 없음.

**주장 4 — ID 그래프 = union-find (52행), 저장 전략 3갈래(75~79행), 하이브리드(81행), append-only 원장(146행)**
- **근거:** `web_stack.md:975`("이건 **union-find(disjoint set)** 문제다. 식별자가 노드, '같은 사람' 관찰이 간선, 연결 요소가 한 사람") / `:979~981`(정규 ID 매핑 → 병합 시 한쪽 전 식별자 재작성 / 간선 저장 + 배치 해석 → 정확하나 지연 / 그래프 DB) / `:983`("**실무에서 흔한 구조는 1+2 하이브리드다** — 배치로 정확히 계산하고 결과를 KV에 물질화, 스트림에서는 새 간선을 즉시 반영하되 완전 해석은 다음 배치로 미룬다") / `:987`("**간선 원장을 append-only로 남겨야 하는 이유**"). 네 대목 모두 원본에 있다.
- **⭐ ①형(고지 범위) 재발 여부 — 없음.** 2파 경고 ①을 겨냥해 별도 감사했다. 83행 고지의 명시 지시대상은 "이 **세 갈래 정리**"이고, 81행의 하이브리드 서술은 그 지시대상 **밖**에 있는 네 번째 주장이라 고지가 못 덮는 구조로 **보였다.** 그러나 하이브리드는 `web_stack.md:983`에 **독립적으로 확보돼 있어** 고지에 기댈 필요가 없다. 즉 고지 범위와 근거 범위가 우연이 아니라 정확히 맞물렸다. 83행의 "이 책의 리서치가 여러 스택 문서를 대조해 추론한 아키텍처 정리다"라는 자기 규정도 `:979~981`의 실제 성격(리서처의 아키텍처 종합)과 일치한다 — **등급을 올려 말하지 않았다.**
- **조치:** 없음.

**주장 5 — 4개 벤더 아이덴티티 손잡이 표 (89~94행)**
- **근거:** `web_gaps.md:601~604` 표와 **전건 일치**:
  - Segment: `priority (user_id 1위, email 2위, 나머지 알파벳순)` / `user_id: 1, 그 외: 5 (기본값)` / `blocked values` ✅
  - Adobe AEP: `namespace priority` / `unique namespace = 그래프당 1개` / `"graph collapse" 방지` ✅
  - mParticle: `identity priority (오름차순 순회)` / 본문 "확인 불가" / 본문 "(명칭 미확인)" ✅
  - Bloomreach: `hard ID > soft ID` / `soft ID 타입당 64개 (초과 시 LRU 제거)` / `hard ID 지정 권고` ✅
- **주목 — mParticle 개수 제한 칸은 원본보다 보수적이다.** `web_gaps.md:603`은 이 칸을 "unique ID 설정 `[검색 요약]`"으로 적었는데(검색 요약 등급), 본문은 아예 **"확인 불가"**로 내렸다. 확인 수준을 **낮춰** 쓴 것이라 2파 경고 ②(등급을 한 칸 올려 말하기)의 반대 방향이다. 안전.
- **조치:** 없음.

**주장 6 — Segment 우선순위 작동 예시 (98행)**
- **본문:** "기존 프로필이 `user_id: abc123`과 `email: jane@example1.com`을 갖고 있는데, 같은 이메일에 다른 `user_id: abc456`을 단 이벤트가 들어온다... 이메일 쪽이 강등되고 새 `user_id`를 위한 새 프로필이 만들어진다. (문서 소스 리포지터리 기준, 발행일 표기 없음 — 2026년 7월 25일 조회.)"
- **근거:** `web_gaps.md:437` — 식별자 값(`abc123`/`abc456`/`jane@example1.com`)·limit 1·priority 순위·결과(email 강등 + 새 프로필 생성)까지 **전건 일치**. 발행일 없음 → 조회 시점 병기 이행(`web_gaps.md:607` "리포 최신 (날짜 미표기)").
- **조치:** 없음.

**주장 7 — Adobe "graph collapse"와 유발 시나리오 (102행)**
- **본문:** "여러 사람이 로그인하는 공유 기기, 사용자가 넣은 허위 연락처, 그리고 `user_null`이나 `not-specified` 같은 오류 식별자 값... (갱신 2026년 6월 18일 기준.)"
- **근거:** `web_gaps.md:482`(명칭) + `:486~489`(1 공유 디바이스 / 2 가짜 연락처 데이터 / 3 오류 식별자 값 `user_null`, `not-specified`) + `:478`(갱신일 2026-06-18). 세 시나리오·명칭·갱신일 전건 일치.
- **조치:** 없음.

**주장 8 — mParticle 인용 (106~108행)**
- **본문:** `"a customer ID or email address is more likely to be unique to a single user than a device ID, because a device ID could be shared by multiple users."` / "(갱신 2026년 7월 16일 기준)"
- **근거:** `web_gaps.md:528` **영문 전건 일치** + `:507` 갱신일 2026-07-16 일치.
- **조치:** 없음.

**주장 9 — Bloomreach 64 (112행) ⭐ 모범**
- **본문:** "soft ID는 같은 타입당 64개까지 유지되고, 넘으면 가장 오래 쓰지 않은 항목부터 밀려난다. 다만 **이 64는 Bloomreach 문서의 값이다.** 다른 제품에 옮겨 쓰면 안 된다. 나머지 세 곳은 이번 리서치 범위에서 그래프 크기 제한 숫자를 확인하지 못했다."
- **근거:** `web_gaps.md:603` 일치.
- **⭐ 타 벤더 전용 차단 확인.** 계획서가 경계한 "한 벤더 수치의 타 제품 전용"(§A-5의 Ads Data Hub 임계값 계열 위험)이 여기서 **본문 안에서 명시적으로 차단**됐다. 게다가 "나머지 세 곳은 확인하지 못했다"까지 붙여 **미확인을 부재로 읽지 않게** 막았다. 2파 D-2(확인/미확인 분리)의 최상급 실행.
- **조치:** 없음.

**주장 10 — Segment 기본 차단 값 (114행)**
- **본문:** "`-1`, `null`, `anonymous`, 그리고 0과 대시로만 이루어진 값"
- **근거:** `web_gaps.md:605` — "`-1`, `null`, `anonymous`, 0/대시 패턴". 일치. 마지막 항목이 여는 all-zero UUID와 맞물리는 구성도 근거 밖으로 나가지 않는다(형식 관찰).
- **조치:** 없음.

**주장 11 — Bloomreach 대소문자 함정 (150행)**
- **본문:** "hard ID가 대소문자를 구분하기 때문에 같은 이메일이 다른 표기로 들어오면 프로필이 둘로 갈리고, 결과는 '같은 고객에게 이메일을 두 번 보내는' 일이다."
- **근거:** `web_gaps.md:562` — "Hard ID는 case-sensitive라 중복 프로필이 생길 수 있다. 문서 표현: 'This creates one customer unrecognized due to case differences, which could result in **sending an email twice to the same customer**.'" 인용 부분까지 일치.
- **조치:** 없음.

**주장 12 — Fellegi & Sunter (1969) (124행) ⭐ 등급 준수의 핵심 지점**
- **본문:** "Ivan P. Fellegi와 Alan B. Sunter의 'A Theory for Record Linkage'(*JASA* 64권 328호)... 이 논문의 개념적 기여는 두 레코드가 같은 실체를 가리키는지를 확률적 결정 문제로 정식화했다는 것이다. 밝혀둘 것은, 이 책의 리서치가 확인한 범위가 서지 메타데이터까지이고 본문을 직접 대조하지는 못했다는 점이다. 그래서 여기서는 이름과 개념적 기여 이상은 적지 않는다."
- **근거:** `papers.md:861`(저자·제목·JASA 64(328)·1183–1210·DOI `10.1080/01621459.1969.10501049`) + 신선도 원장 `:1225` — 조회 `CR` / 확인 수준 **`메타데이터`**.
- **⭐ 등급 초과 없음 — 직접 대조 결과 저술가 보고가 사실.** `papers.md:862`의 핵심 주장 필드에는 **세 영역(매치 / 논매치 / clerical review)·가능도비·두 임계값·최적성 증명**이 전부 적혀 있다. 본문은 그중 **"확률적 결정 문제로 정식화"** 한 조각만 가져오고 **세 영역 형식·가능도비·임계값·최적성을 0건 사용**했다(grep 확인). `메타데이터 확인` = "초록 본문을 못 봤다"는 등급에 정확히 맞는 표현 폭이고, 확인 범위를 문장 안에서 스스로 밝힌 형태다. **2파 경고 ②(등급 한 칸 올리기)의 정면 반대 사례.**
- **참고(감점 아님):** 126행 "확률적 판정에는 원래 '확신하지 못하는 구간'이 있다"는 `papers.md:863`의 리서처 해설(세 번째 영역의 의의)과 같은 취지지만, 본문은 이를 **1969년 논문에 귀속시키지 않고 확률적 판정 일반의 성질로** 서술했다. 임계값 기반 판정에 회색 구간이 존재한다는 것은 선험적으로 참이라 귀속 없는 서술로 적법하다. 통과.
- **조치:** 없음.

**주장 13 — 확률적/결정적 매칭 정확도 수치 (122행)**
- **본문:** "두 방식의 정확도를 숫자로 이야기하는 자료가 돌아다니는데, 이번 리서치는 그 숫자들의 1차 출처를 확보하지 못했다... 그래서 이 책은 어느 쪽 숫자도 쓰지 않는다. **없다는 뜻이 아니라 확인하지 못했다는 뜻이다.**"
- **판정:** **수치 0건 확인**(grep — 07장 전체에 매칭 정확도 관련 백분율·배수 0건). 미확인을 부재로 읽지 않게 막는 마지막 문장까지 2파 D-2 형식 그대로다.
- **조치:** 없음.

**주장 14 — UID2 (130행)**
- **본문:** `"a framework that enables deterministic identity for advertising opportunities on the open internet"` / "(문서 최종 갱신 2026년 7월 23일 기준)" / "파생 절차나 토큰 운영 방식은 확인하지 못했으니 여기서 다루지 않는다. 업계 표준 식별자가 무엇인지에 대한 단정도 하지 않는다."
- **근거:** `web_privacy.md:329` **영문 전건 일치**.
- **판정:** **파생 절차·토큰 회전·RampID 0건 확인**(grep — 세 항목 모두 07장 미등장). "업계 표준 식별자" 단정 회피까지 이행.
- **조치:** 없음.

**주장 15 — SHA-256 이메일 해시는 가명화 (132행)**
- **본문:** "같은 이메일은 언제나 같은 해시가 된다. 즉 **그 값은 여전히 조인 키다.** 익명화보다는 가명화에 가깝고, 이 구분은 10장에서 법 조문과 만난다."
- **판정:** 결정론적 해시의 성질에 대한 기술적 참이고 **법 조문·조항 번호를 붙이지 않고 10장으로 넘겼다.** 계획서 §A-6(PIPA)·§A-7(정보통신망법) 지뢰를 밟지 않는 처리. 통과.
- **조치:** 없음.

**주장 16 — Hightouch Sync 네 축 (160행)**
- **본문:** "Hightouch 개발자 문서(페이지 표기 2026년 7월 17일)가 명세하는 Sync의 축은 넷이다. 타입, 모드, 매핑, 스케줄. 이 목록이 1차 문서로 확인된 범위이고, 아래는 각 축이 어떤 운영 문제 위에 놓여 있는지를 읽어낸 것이다."
- **근거:** `web_products.md:130` — `"Syncs specify: Type: object, event, audience, etc. Mode: insert, update, upsert, or archive Mapping: how source columns map to destination fields Schedule: interval, cron, or triggered by tools like dbt Cloud or Airflow"` + `:134` 페이지 표기 "Last updated Jul 17, 2026". 네 축·모드 4종(insert/update/upsert/archive)·스케줄 트리거(dbt Cloud·Airflow) 전건 일치.
- **⭐ ①형 감사 통과 — 고지가 앞에서 뒤를 덮는다.** 160행의 "아래는 ... 읽어낸 것이다"는 **선행 고지**로, 뒤따르는 네 축 해설 문단(162~170행) 전체를 덮는다. 2파 ①형(고지가 뒤 문단을 못 덮음)의 **정반대 배치**이고, 이 장에서 가장 잘 설계된 고지다.
- **조치:** 없음.

**주장 17 — 부분 실패 처리 (172행)**
- **본문:** "만 명을 내보내는 동기화에서 삼백 명이 목적지 검증에 걸려 거절됐다면... 이 부분의 구체적인 동작은 제품마다 다르고, 이번 리서치는 그 세부를 1차 문서로 확인하지 못했다. 그러니 벤더를 평가할 때 물어볼 질문 목록에 넣어두는 편이 낫다."
- **판정:** 9,700/300은 **저술가가 세운 가상 시나리오의 자체 산술**이고(만 명 − 삼백 명), 어떤 제품의 동작으로도 주장되지 않았다. 미확인 고지가 **같은 문단 안**에 있어 범위 문제 없음. 통과.
- **조치:** 없음.

**주장 18 — Insider 레이트 리밋 표 (178~185행)**
- **본문:** "아래 숫자는 전부 2026년 7월 문서 기준이고, 이런 값은 벤더가 예고 없이 바꾼다." / Upsert User Data 25,000 rpm / Export Raw User Data 1 per day / Send Transactional Emails 9,000 rps / Create Email Campaigns 1 rps
- **근거:** `web_products.md:450`(25,000 requests per minute) · `:451`(**1 request per day**) · `:474`(**9000 requests per second**) · `:477`(1 request per second) · `:470` 표 머리 "(2026-07-12 문서 표기 기준)". 4행 전건 일치.
- **⭐ 계획서 §B:220 이행 확인.** "Insider API rate limit — **'2026년 7월 문서 기준' 병기 필수**"가 표 **바로 앞 문장**에 있고, "이런 값은 벤더가 예고 없이 바꾼다"는 휘발성 경고까지 덧붙었다. 🕒 불필요.
- **조치:** 없음.

**주장 19 — 배치 한도 (187행)**
- **본문:** "요청 하나에 사용자 천 명씩 최대 5MB를 담을 수 있다."
- **근거:** `web_products.md:437~439` — "요청당 최대 **1,000 users**", "요청 크기 **최대 5 MB**". 일치.
- **조치:** 없음.

**주장 20 — `skip_hook` (193행)**
- **본문:** "사용자 데이터를 밀어 넣을 때 `skip_hook`으로 이 임포트가 저니를 깨울지 말지를 정한다"
- **근거:** `web_products.md:418` — "`skip_hook` (boolean, optional) — 임포트된 데이터가 Architect 저니를 트리거할지 제어". 플래그명·의미 일치. `web_products.md:604`가 Architect 세부를 `확인 불가`로 뒀는데 본문도 제품명을 쓰지 않고 "저니"로만 적어 미확인 영역을 침범하지 않았다.
- **조치:** 없음.

### ⚠️ 근거 약함 (1건)

**주장 21 — "CDP의 API 표면 절반" (195행)**
- **본문:** "이 제품의 사용자 데이터 API는 여섯 개인데, 그중 넷이 삭제하거나 식별자를 고치는 계열이다(속성 삭제, 식별자 갱신, 식별자 삭제, 그리고 별도의 프로필 삭제와 개인정보 삭제까지 세면 더 늘어난다). **CDP의 API 표면 절반이 삭제 요구를 처리하기 위해 존재한다는 뜻이다.**"
- **근거:** `web_products.md:514~520`(6종 목록: Upsert / Get User Profiles / Export Raw User Data / Delete User Attribute / Update Identifiers / Delete Identifiers) + `:525` 리서처 관찰 — "6개 API 중 **4개가 삭제/수정 계열**(Delete User Attribute, Delete Identifiers, Update Identifiers, 그리고 별도 Delete User Profiles / Delete PII)이다. **CDP API 표면의 절반이** GDPR·개인정보 삭제 요구를 처리하기 위한 것".
- **판정 ⚠️.** 앞 문장("이 제품의 ... 여섯 개인데, 그중 넷이 삭제하거나 식별자를 고치는 계열")은 **원본과 완전 일치하고 주어도 '이 제품'으로 정확히 한정**돼 있다. 문제는 볼드 처리된 요약 문장이고, **두 군데에서 앞 문장보다 넓어진다**:
  1. **주어가 '이 제품' → 'CDP'로 확장.** 조사된 것은 Insider One 한 곳의 User Data API 목록이다. 다른 CDP의 API 표면 구성은 이번 리서치 범위에 없다(`web_products.md:1213`·`:1361`이 Identity Resolution 상세를 미확보로 기록한 것과 같은 결).
  2. **'삭제/수정' → '삭제'로 축소되며 분자가 흐려짐.** 넷 중 `Update Identifiers`는 삭제가 아니라 수정이다. 앞 문장은 "삭제하거나 식별자를 고치는"으로 정확히 썼는데 요약에서 '수정'이 탈락했다. 또 6분의 4는 엄밀히 3분의 2다.
- **다만 정상 참작:** 이 문장은 저술가의 창작이 아니라 **`web_products.md:525` 리서처 관찰의 거의 그대로의 전사**다. 원본이 이미 'CDP'와 '절반'을 썼다. 즉 저술가가 등급을 올린 게 아니라 **리서처의 편집적 관찰(1차 확인 사항이 아님)을 등급 표시 없이 옮긴 것**이다. 성격은 2파 경고 ③(정확한 근거 문장에 붙은 근거 밖 수식어)과 같다.
- **조치(택1, 앞 문장은 그대로 두고 볼드 문장만 교체):**
  - (A) 범위 한정안 — "**이 제품의 사용자 데이터 API 여섯 개 중 넷이 삭제하거나 식별자를 고치는 일을 한다는 뜻이다.**"
  - (B) 관찰 등급 명시안 — "**이 제품에서는 API 표면의 절반 이상이 삭제·정정 요구를 처리하는 데 쓰인다. 다른 CDP도 그런지는 이번 리서치가 확인하지 않았다.**"
  - 어느 쪽이든 뒤따르는 "규제가 이 도메인에서 어떤 위치인지 보여주는 자료를 찾는다면, API 목차보다 정직한 것은 없다"는 그대로 살아난다.

### ❌ 정정 필요 / 🕒 검증 불가

**0건.**

### 07장 종합

**❌ 0 / 🕒 0 / ⚠️ 1 / ✅ 20.** Phase 5를 차단하는 항목 없음. ⚠️ 1건은 볼드 한 문장 교체로 해소된다.

**2파 경고 3형의 재발 여부 — 셋 다 없음.**
- **① 고지 범위** — 재발 없음. 83행 고지는 지시대상("세 갈래 정리")과 근거 범위가 정확히 맞물렸고, 81행 하이브리드는 `web_stack.md:983`에 독립 근거가 있어 고지에 기대지 않는다. 160행 고지는 **뒤 문단들을 덮는 선행 배치**로 ①형의 모범 반례다.
- **② 등급 상향** — 재발 없음. Fellegi & Sunter에서 `메타데이터 확인` 등급의 표현 폭을 정확히 지켰고(세 영역 형식 0건), mParticle 칸은 오히려 원본보다 **낮춰** 적었다.
- **③ 근거 밖 수식어** — **1건 재발**(주장 21의 "CDP의"). 다만 저술가 창작이 아니라 원본 문장의 전사라는 점에서 1·2파의 "절반쯤"·"국내"와는 발생 경로가 다르다.

**의심 식별자: 0건.** 07장에는 arXiv ID·DOI가 등장하지 않고, 인용 식별자는 전부 벤더 문서 URL + 갱신일/조회일 형태다. 미래 YYMM·미해석 식별자 없음.

---

## 08장 — 1차 검증

**검증일:** 2026-07-26 / 대상 `chapters/08_draft.md` / 1차 대조 `research/web_stack.md`·`papers.md`
**`(사실 확인 필요)` 주석: 0건** (grep 확인).

### ✅ 확인됨

**주장 1 — 토스 광고 ML 3단 구조 (11~15행)**
- **본문:** "토스가 2025년 4월 21일에 공개한 광고 ML 구조" / 타겟팅·필터링·랭킹 / `"유저의 행동 로그를 학습하거나 Two-tower 모델을 통해 유저와 광고 간의 상호작용을 학습하여 유저 임베딩을 생성"` / `"CTR 예측 모델은 광고 ID, 유저 속성 등 고차원의 희소 특징 간의 상호작용을 효과적으로 학습"` / "FM·DeepFM·DCN 구조로 eCPM을 산출"
- **근거:** `web_stack.md:1148`(발행일 **2025-04-21** 페이지 표기·확정, 저자 김영호) + `:1153`·`:1163` **한글 인용 두 건 전건 일치** + `:1158`(필터링 = Two-tower 임베딩으로 수백만 광고 중 후보 검색) + `:1163`(FM, DeepFM, DCN / eCPM). `:1405` 신선도 원장이 발행일을 "페이지 표기·확정"으로 기록.
- **주목:** 19행 "eCPM은 노출 1,000회당 기대 수익이다"는 `web_stack.md:1163`의 괄호 정의("1,000회 노출당 기대 수익")와 일치. 이어지는 "그 값이 실제 경매에서 어떤 규칙으로 낙찰과 과금으로 이어지는지는 이 책의 리서치가 다루지 않은 영역이라, 여기서는 랭킹 지표까지만 적는다"는 **미조회 영역을 스스로 잘라낸 문장**이다. 통과.
- **조치:** 없음.

**주장 2 — Covington, Adams & Sargin (2016) (25행) ⭐ 본문이 원본보다 보수적**
- **본문:** "Covington, Adams, Sargin이 2016년 RecSys에 발표한 유튜브 추천 논문이 후보 생성과 랭킹을 분리한 2단계 구조를 제시했고... 이 책의 리서치는 이 논문의 서지 레코드까지 확인했으므로, 여기서는 그 구조적 기여를 소개하는 선에서 멈춘다. 여기에 '오늘날 이 2단 분리는 산업 표준'이라고 덧붙인다면, 그건 논문이 보증하는 범위를 넘어선 이 책의 관찰이다."
- **근거:** `papers.md:260`(저자·제목·RecSys 2016·pp.191–198·DOI `10.1145/2959100.2959190`) + 신선도 원장 `:1167` 확인 수준 **`메타데이터`**.
- **판정 ✅ — 두 겹으로 확인했다.**
  1. **2단계 구조 서술의 근거:** `papers.md:262` 핵심 주장 필드가 "대규모 추천을 **후보 생성(candidate generation) → 랭킹(ranking)** 2단계로 나누는 산업 표준 아키텍처를 공개했다"고 **직접 기록**하고 있다. 본문의 "후보 생성과 랭킹을 분리한 2단계 구조를 제시했고"는 이 문장 안에 있다. 등급 초과 아님.
  2. **"산업 표준" 처리:** 원본 `papers.md:262`는 **"산업 표준 아키텍처"라고 단정**했는데, 본문은 그 표현을 논문에 귀속시키지 않고 **"덧붙인다면 ... 논문이 보증하는 범위를 넘어선 이 책의 관찰이다"**로 등급을 내려 붙였다. **저술가 자기 보고가 직접 대조에서 사실로 확인됐고, 본문이 리서치 원본보다 엄격하다.** 2파 경고 ②의 정반대 사례.
- **조치:** 없음.

**주장 3 — CTR 예측 모델 계보 연도 (27행)**
- **본문:** "McMahan 등의 2013년 FTRL, He 등의 2014년 연구, Juan 등의 2016년 Field-aware Factorization Machines, Cheng 등의 2016년 Wide & Deep, Guo 등의 2017년 DeepFM, Zhou 등의 2017년·2018년 연구"
- **근거:** `papers.md` 신선도 원장 `:1169~1175` — D-7-1 McMahan **2013** / D-7-2 He **2014** / D-7-3 Juan **2016** / D-7-4 Cheng **2016** / D-7-5 Guo **2017** / D-7-6 Zhou **2017**(DIN) / D-7-7 Zhou **2018**(DIEN). **연도 7건 전건 일치, 오류 0.**
- **판정:** 이어지는 "이 목록에서 어느 쪽이 더 낫다는 결론을 읽어내면 안 된다. 이 책의 리서치는 이 논문들의 서지까지만 확인했고, 성능 비교를 옮길 근거를 갖고 있지 않다"가 `메타데이터 확인` 등급(6건)의 표현 폭을 정확히 지킨다. 통과.
- **조치:** 없음.

**주장 4 — Ferrari Dacrema et al. (2019) 인용 (33~41행) ⭐ 이 장 유일한 직접 수치 인용**
- **본문(블록 인용):** `"Specifically, we considered 18 algorithms that were presented at top-level research conferences in the last years. Only 7 of them could be reproduced with reasonable effort. For these methods, it however turned out that 6 of them can often be outperformed with comparably simple heuristic methods, e.g., based on nearest-neighbor or graph-based techniques."` / `[arXiv:1907.06902 | RecSys 2019 | DOI 10.1145/3298689.3347058]`
- **근거:** `papers.md:243~244` — **영문 초록 원문 전건 일치(문자 단위)**. 서지 `:239`(RecSys 2019, arXiv:1907.06902 v3, DOI `10.1145/3298689.3347058`) 일치. 신선도 원장 `:1165` 확인 수준 **`초록 확인`** — **직접 인용이 허용되는 유일한 등급**이고 이 장에서 수치를 그대로 옮긴 유일한 논문이다. 규칙 준수.
- **파생 서술 검산:** 39·41행 "재현 자체가 절반을 넘기지 못했고"(7/18 = 38.9%, 참) / "재현된 것들도 대부분 단순한 방법을 확실히 이기지 못했다"(6/7, 참 — `papers.md:242`가 남은 1개도 "잘 튜닝된 비신경망 선형 랭킹 방법을 일관되게 이기지는 못했다"고 기록). 산술·방향 모두 초록 범위 안.
- "저자들은 평가 코드를 공개해두었다"(39행) — `papers.md:245` 재현성 필드(GitHub 저장소 명시)와 일치.
- **의심 식별자 검사:** arXiv `1907.06902`의 YYMM = 2019-07은 빌드 시점(2026-07) 기준 **과거**이고 RecSys 2019 발표 시기와 정합하며, DOI 접두 `10.1145/3298689`는 RecSys 2019 프로시딩과 일치한다. **정상 식별자.**
- **조치:** 없음.

**주장 5 — Rendle et al. (2020) (43행)**
- **본문:** "Rendle과 공저자들이 2020년에 내놓은 연구는 신경망 협업 필터링과 행렬 분해를 다시 세워놓고 비교한다. 이 책의 리서치는 이 논문의 서지까지 확인했으므로 결론의 방향이나 수치를 여기 옮기지는 않는다. 다만 제1저자가 Factorization Machines를 만든 사람이라는 점은 적어둘 만하다."
- **근거:** `papers.md:252`(Rendle, Krichene, Zhang, Anderson, "Neural Collaborative Filtering vs. Matrix Factorization Revisited," arXiv:2005.09683, 2020) + `:255`("제1저자 Steffen Rendle은 Factorization Machines 창시자라 반박의 무게가 다르다") + 원장 `:1166` **`메타데이터`**.
- **판정:** 본문 서술은 **제목의 재진술 범위**를 넘지 않고, 결론 방향(`papers.md:254`의 "재검토한다")을 **명시적으로 옮기지 않겠다고 선언**했다. 제1저자 사실은 서지 사항이라 등급 문제 없음. 통과.
- **조치:** 없음.

**주장 6 — 토스 TUES (53~61행)**
- **본문:** "2026년 6월 16일 공개된 TUES(Toss User Engagement Segment)" / `"각 유저의 서비스 이용 패턴을 기준으로 비슷한 유저들끼리 묶어둔 세그먼트"` / "**TUES는 월 단위 배치로 계산된다.** 실시간이 아니다." / "V1은 K-Means... V2는 NMF로 넘어가면서 확률적 세그먼트 멤버십이 됐다."
- **근거:** `web_stack.md:1181`(발행일 **2026-06-16** 페이지 표기·확정, 저자 우찬희) + `:1183`(TUES = Toss User Engagement Segment, 플랫폼 수준 세그먼테이션 프레임워크) + `:1185` **한글 인용 전건 일치** + `:1186~1187`(V1 K-Means 하드 / V2 NMF 소프트 → 확률적 세그먼트 멤버십) + `:1188`("**처리 모델: 배치 — 월 단위로 계산.** 실시간이 아니다"). 6요소 전건 일치.
- **주목:** `web_stack.md:1190`은 "2,800만 MAU 규모"를 기록했는데 본문은 **그 수치를 쓰지 않고** "대규모 서비스의 플랫폼 세그먼테이션"으로만 적었다(57행). 쓸 수 있는 수치를 안 쓴 쪽이라 위험 없음.
- **조치:** 없음.

**주장 7 — Pinterest 사례 (75~87행) ⭐⭐ 이 장 최대 위험 지점 — 저술가 보고가 사실로 확인됨**

이 절은 위임받은 검증의 핵심이므로 **영문 조각 네 건을 개별 대조**하고, 문제의 표현을 **원본 안에서의 위상까지** 판정했다.

- **(a) 스트리밍 경로 인용 (75행):** `"filters incoming events, converts them into a normalized representation, applies enrichments, and writes incremental updates"` → `web_stack.md:1259` **전건 일치**.
- **(b) 배치 경로 인용 (75행):** `"apply the same filter and enrichment definitions, and produce longer sequences"` → `web_stack.md:1260`의 `"read historical raw events, apply the same filter and enrichment definitions, and produce longer sequences."` **후반부 전건 일치**. 본문의 한글 "과거 원본 이벤트를 다시 읽어"가 앞부분(`read historical raw events`)을 정확히 옮기고 있어 절단으로 인한 의미 변형 없음.
- **(c) 저장·서빙 (75행):** "결과는 컬럼 레이아웃으로 저장돼 모델이 필요한 필드만 읽는다" → `web_stack.md:1261` `"Sequence data is stored in a columnar layout so models can read exactly the fields they need"` 일치.
- **(d) 블록 인용 전문 (85행):** `"This lambda-style architecture balances freshness (streaming updates) with completeness (batch corrections), eliminating the historical problem where training and serving systems diverged."` → `web_stack.md:1262` **문장 전체가 문자 단위로 일치**(앞 절만이 아니라 마침표까지). 출처 표기 `[medium.com/pinterest-engineering | 2026-05-21 | 검색 시점 2026-07-25]`도 `:1255`·`:1403`(발행일 **2026-05-21 페이지 표기·확정**)·검색 시점 2026-07-25와 일치.
- **(e) "Pinterest는 자기 구조를 스스로 'lambda-style'이라고 부른다" (79행):** (d)의 인용문이 Pinterest 원문이고 그 안에 `This lambda-style architecture`가 있으므로 **자기 서술이라는 판정이 인용으로 뒷받침된다.** 통과.

- **⭐ 핵심 판정 — `"one definition, many runtimes"`의 위상 (77행)**
  - **본문:** "이 리서치는 Pinterest의 재설계를 요약하는 표현으로 'one definition, many runtimes'를 기록해뒀는데, 방금 인용한 배치 경로 문장이 그 표현의 기술적 알맹이다."
  - **원본에서의 출현 위치 3곳을 전수 확인했다:**
    - `web_stack.md:1257` — "플랫폼을 'one definition, many runtimes'로 재설계." → **리서처의 한글 서술문 안**
    - `web_stack.md:1264` — "특히 'one definition, many runtimes'는 Lambda의 고질병(로직 이중 구현)에 대한 구체적 해법이라" → **리서처의 「책에서의 활용」 코멘트 안**
    - `web_stack.md:1066` — "**Pinterest의 답이 인상적이다** — 'one definition, many runtimes': 정의를 한 번 쓰고 스트리밍/배치 런타임이 그 정의를 각각 실행한다." → **리서처의 아키텍처 절 서술 안**
  - **판정 ✅.** 이 표현은 **세 곳 어디에서도 Pinterest 인용 블록 안에 있지 않다.** 같은 절에서 리서처는 Pinterest 원문 네 건(위 a~d)을 전부 `**스트리밍 경로:**`·`**배치 경로:**`·`**저장·서빙:**`·`**아키텍처 성격:**` 라벨을 붙여 명시적으로 인용 표시했는데, 이 표현에는 그 라벨이 없다. 즉 **원본 문서 자체가 이 표현을 Pinterest 원문으로 제시하지 않는다.** 따라서 본문이 이를 **"이 리서치가 기록한 요약 표현"으로 위상을 낮춰** 제시한 것은 정확하고, 만약 "Pinterest가 말했듯이"로 썼다면 오귀속이 됐을 자리다. **저술가 자기 보고가 직접 대조에서 사실로 확인됐다.**
  - **📌 후속 리뷰를 위한 기록:** 이 로그의 **2파 말미(`factcheck_log.md` 「7~12장 저술가에게」 B절 8장 항목)**는 이 표현을 "Pinterest 사례('one definition, many runtimes', 2026-05-21 발행일 확정)"로 적으며 **위상을 구분하지 않았다.** 그 서술만 읽으면 Pinterest 원문으로 오독될 수 있다. **본 항목이 그 모호함을 해소하는 정전 기록이다** — 이 표현은 **리서처 요약이며 Pinterest 원문이 아니다.** Phase 4.5·editor는 이를 Pinterest 발언으로 승격시키지 말 것.
- **조치:** 없음.

**주장 8 — Lambda / Kappa 출처 성격 (73행)**
- **본문:** "Lambda는 Marz와 Warren의 책(Manning, 2015)에서, Kappa는 Kreps가 2014년 O'Reilly Radar에 쓴 글에서 나왔다. 하나는 책이고 하나는 블로그 글이며, 둘 다 peer-reviewed 문헌이 아니다."
- **근거:** `papers.md:803`("Nathan Marz & James Warren, *Big Data...* (Manning, **2015**)로 정식화되었다. **책이지 논문이 아니다.**") + `:804`("Kafka 공동 창시자 **Jay Kreps**가 **2014년** O'Reilly Radar에 쓴 블로그 글 'Questioning the Lambda Architecture'에서 제안했다. **블로그 글이지 논문이 아니다.**"). 저자·연도·매체·성격 4요소 전건 일치. 4장 검증(이 로그 주장 5, `:742~746`)에서 이미 확정된 항목의 재진술이라 **장 간 사실 충돌 없음.**
- **참고(감점 아님):** `web_stack.md:1084`·`:1348`과 `papers.md:805`는 두 원전을 **직접 열어보지 못했다**고 기록했고, 이 미조회 고지는 **4장 48행 괄호("두 원전 자체는 이번 리서치가 직접 열어보지 못했고, 서지 사항만 교차 확인했다")에 이미 실려 있다.** 8장은 "4장에서 이 이름의 출처를 이미 확인했다"로 그 장을 가리키므로 고지가 끊기지는 않는다. 다만 8장만 읽는 독자에게는 미조회 사실이 보이지 않는다 — **선택 보강안:** 73행의 "그때는 출처의 성격만 확인하고" → "그때는 서지만 교차 확인하고(두 원전 자체는 열어보지 못했다)". 필수 아님.
- **조치:** 없음(선택 보강 1건).

**주장 9 — 학습-서빙 스큐 시나리오와 AUC 0.85 (93~99행)**
- **본문:** "이탈 예측 모델을 하나 만든다고 해보자... 오프라인 평가에서 AUC 0.85가 나온 모델이 프로덕션에서는 형편없다."
- **판정 ✅ — 가정 프레임 안에 있다.** 93행의 "**~ 만든다고 해보자**"로 열린 가상 시나리오가 95~99행까지 이어지고, 0.85는 그 시나리오가 스스로 세운 예시 값이다. 어떤 제품·논문·벤치마크에도 귀속되지 않았고, 실측 주장으로 읽힐 문장 구조가 아니다. 4장 주장 12(가정을 모델 속성으로 쓰지 않기)와 같은 설계.
- **조치:** 없음.

**주장 10 — Feast 인용 두 건 (111~115행)**
- **본문:** `"Feast is able to join features from one or more feature views onto an entity dataframe in a point-in-time correct way."` / `"the TTL time is relative to each timestamp within the entity dataframe. TTL is not relative to the current point in time (when you run the query)."` / `[docs.feast.dev/getting-started/concepts/point-in-time-joins | 발행일 확인 불가 | 검색 시점 2026-07-25]`
- **근거:** `web_stack.md:720` 및 `:728` — **영문 두 건 모두 전건 일치**. 출처 표기는 `:1400`(Feast Point-in-time joins, **발행일 확인 불가**, 2026-07-25)과 일치. 발행일 미확인을 숨기지 않고 그대로 노출.
- **조치:** 없음.

**주장 11 — 토스 피처 스토어 (119행)**
- **본문:** "(2025년 8월 14일 글)" + `"Target 데이터를 기준으로 시간 파티션을 Shift 할 수 있어요. 예를들어, 01시에 발생한 피드백 데이터라도 Shift 기능을 사용하여 00시에 발생한 Feature들과 조인하여 데이터 누수를 방지할 수 있습니다."` + "같은 글은 학습-서빙 스큐 자체도 피처 정의를 한곳에 모으고 중앙 메타데이터에 등록해 막는다고 적는다."
- **근거:** `web_stack.md:1169`(발행일 **2025-08-14** 페이지 표기·확정, 저자 우종호·송석현) + `:1174` **한글 인용 전건 일치**(원문의 "예를들어" 붙여쓰기까지 보존) + `:1175`("Training-Serving Skew를 피처 정의 통합 + 중앙 메타데이터 등록으로 방지"). 일치.
- **참고:** 같은 행의 "오픈소스 표준과 사내 구현이" 에서 "오픈소스"가 가리키는 것은 **Feast**다. 계획서 금지 9항(Snowplow·RudderStack·Redis를 오픈소스로 단정)에 해당하지 않는다. 세 제품 모두 8장 미등장(grep 확인).
- **조치:** 없음.

**주장 12 — Sculley et al. (2015) 인용 + TFX (121~127행)**
- **본문:** "Baylor 등의 2017년 TFX 논문과, Sculley 등이 2015년 NIPS에 낸 ML 시스템의 숨겨진 기술 부채 논문에 닿는다." + 블록 인용 `"Machine learning offers a fantastically powerful toolkit for building useful complex prediction systems quickly. This paper argues it is dangerous to think of these quick wins as coming for free."` + `[Sculley et al., "Hidden Technical Debt in Machine Learning Systems," *NIPS 28* | 2015 | 검색 시점 2026-07-25]` + "선언되지 않은 소비자" / "숨은 피드백 루프"
- **근거:**
  - Sculley 인용문 → `papers.md:1036` **초록 원문 전건 일치**. 원장 `:1244` 확인 수준 **`초록 확인`** — 직접 인용 허용 등급. 서지(NIPS 28, 2015) 일치.
  - 두 위험 요인 → `papers.md:1034`가 초록 기반으로 "**숨은 피드백 루프(hidden feedback loops), 선언되지 않은 소비자(undeclared consumers)**"를 열거. 일치. 본문의 예시 서술(세그먼트 정의 변경 → 다운스트림 캠페인 파손 / 추천 노출이 다음 학습 데이터가 됨)은 `papers.md:1038~1039`의 마테크 대응 예시와 같다.
  - **⭐ 수치 탈락 확인:** `papers.md:1039`는 "다운스트림 캠페인 **7개**가 깨진다"로 적었는데 본문은 **"몇 개"**로 바꿨다. 그 7은 리서처의 예시 수치지 논문 값이 아니므로, 숫자를 떨어뜨린 것이 정확한 판단이다.
  - Baylor 2017 TFX → `papers.md:1044`(KDD 2017, pp.1387–1395, DOI `10.1145/3097983.3098021`) + 원장 `:1245` **`메타데이터`**. 본문은 **이름·연도·"프로덕션 ML 플랫폼을 다룬"이라는 주제 귀속까지만** 쓰고 논문의 주장·수치를 옮기지 않았다. 등급 준수.
- **조치:** 없음.

**주장 13 — 피처 스토어 정전 논문 부재 (121행)**
- **본문:** "이 책이 4장에 걸어둔 항목 하나가 회수된다. 근거가 끊긴 열두 건 목록의 여섯 번째, 피처 스토어였다. 이 개념을 정의하고 평가한 정전 논문은 이번 리서치에서 찾지 못했다. 산업계 엔지니어링 블로그와 벤더 문서에서 형성된 이름이고"
- **근거:** `papers.md:1050`(C-22-3 "Feature store — **정전 학술 논문 부재**") + `papers.md:1102~1122` 「학술 근거 없음」 목록의 **6번 항목**이 Feature store(이 로그 4장 주장 `:107`에서 12개 목록 및 순번 확정). 순번·판정 일치. **4장이 8장으로 예고한 약속의 이행이 확인된다.**
- **조치:** 없음.

**주장 14 — AI/ML 지형 표 (133~143행)**
- **근거:** `web_stack.md:1198~1204` 표와 **7행 전건 일치** — 룩얼라이크(Two-tower + ANN, ✅토스 확인) / CTR·전환(FM·DeepFM·DCN, ✅토스 확인) / 세그먼테이션(K-Means→NMF, ✅토스 확인) / 이탈 예측(지도학습 분류, ⚠️확인 불가) / Send-time(사용자별 최적 발송 시각 예측, ⚠️확인 불가) / LLM 카피(생성 모델, ⚠️확인 불가) / 자연어 세그먼트 질의(LLM + 스키마 컨텍스트, ⚠️확인 불가).
- **143행의 "미확인" 해설**은 `web_stack.md:1205` 처리 지침("업계에서 널리 언급되는 카테고리이지만, **어느 제품이 실제로 무엇을 쓰는지는 확인하지 않았다**... **특정 벤더가 이 기능을 제공한다는 서술은 이 문서를 근거로 쓸 수 없다**")을 그대로 옮긴 것이다. **미확인을 부재로 읽지 않게 막는 문장이 붙어 있다.**
- **조치:** 없음.

**주장 15 — LLM 카피 효과 크기 (145행) ⭐ 금지 12항 본진**
- **본문:** "이 리서치는 LLM이 생성한 마케팅 카피의 효과 크기를 다룬 연구를 찾는 데 실패했다. 못 찾았다는 것이 없다는 증명은 아니지만, 적어도 이 책은 'LLM 카피가 성과를 몇 퍼센트 올린다'는 문장을 뒷받침할 근거를 갖고 있지 않다."
- **판정:** **효과 크기 수치 0건 확인**(grep — 8장 전체에 LLM 카피 성과 관련 백분율·배수 0건). `papers.md:1127`이 권고한 "근거 부재를 명시하고 검증 프로세스 관점으로 서술"을 그대로 이행했고, 뒤에 "그 숫자가 어느 실험에서 무엇과 비교해 나온 것인지 물어보는 편이 낫다"는 실무 처방까지 붙였다. 계획서 금지 12항 **완전 준수.**
- **조치:** 없음.

**주장 16 — Send-time optimization (147행)**
- **본문:** "이 리서치는 이 주장을 검증한 최상위 저널 연구를 확인하지 못했다. 업계 관행에 가깝다는 뜻이다. 그런데 같은 채널 이야기 안에서도 근거가 단단한 축이 따로 있다 — 발송 빈도와 피로도 쪽이다."
- **근거:** `papers.md:655~657`(D-13-5) 및 `:1106`. 판정·대비 구도 일치. **9장 본진을 침범하지 않고 대비만 예고**했다(논문명·수치 0건). 계획서 §A 추가 규율("두 항목의 근거 강도 대비가 9장의 핵심 소재")의 배치 의도와 맞는다.
- **조치:** 없음.

**주장 17 — Spider / BIRD / Hong 서베이 (149행)**
- **본문:** "Yu 등이 2018년에 낸 Spider는 학습에서 본 적 없는 데이터베이스로 일반화하는 설정을 세웠고, Li 등이 2023년에 낸 BIRD는 값이 지저분하고 도메인 지식이 필요한 현실적인 데이터베이스로 무대를 옮겼다. Hong 등의 서베이가 이 축 전체를 조감한다. 세 편 모두 이 책의 리서치는 서지까지 확인했으므로 점수나 순위를 옮기지는 않는다."
- **근거:** `papers.md:977`("핵심은 **훈련에서 본 적 없는 데이터베이스에 일반화**해야 한다는 설정이다") + `:986`("실제 마테크 데이터웨어하우스는 값이 지저분하고, 컬럼 이름이 암호 같고, 도메인 지식 없이는 질의를 못 만든다") + `:993`("LLM text-to-SQL 전체를 조감하는 서베이"). 세 서술 모두 원본 안. 연도(2018/2023/서베이) 원장 `:1238~1240` 일치.
- **판정:** 세 편 모두 `메타데이터` 등급인데 본문은 **벤치마크의 설정 성격까지만** 옮기고 점수·순위·모델 성능을 0건 인용했다. 이어지는 "벤치마크에서 잘한다는 것과 컬럼 이름이 `col_23`인 우리 회사 웨어하우스에서 잘한다는 것은 다른 층위에 있다"도 `papers.md:986`의 취지 안. 통과.
- **조치:** 없음.

### ⚠️ 근거 약함 (2건)

**주장 18 — "국내 서비스가 ... 밝힌 드문 글이다" (11행)**
- **본문:** "토스가 2025년 4월 21일에 공개한 광고 ML 구조는, 국내 서비스가 자기 모델 파이프라인을 이 정도 해상도로 밝힌 **드문** 글이다."
- **판정 ⚠️(경미).** "국내 서비스"는 토스에 대해 참이고 문제없다. 문제는 **"드문"**이다. 이는 국내 공개 사례 전반의 분포에 대한 주장인데, 리서치는 그 분포를 조사하지 않았다. `web_stack.md:1157`는 이 글을 "**확인된 실제 사례**"·"개발자에게 이 사례가 좋은 이유"로 평가했을 뿐 **희소성을 판정하지 않았다.** 2파 경고 ③("정확한 인용에 근거 없는 수식어": "절반쯤"·"국내")과 **정확히 같은 형태**다 — 인용은 완전무결한데 수식어 하나가 근거 밖으로 나갔다.
- **조치(택1):**
  - (A) 근거 안으로 당기기 — "...밝힌 **보기 드물게 구체적인** 글이다" → 여전히 분포 주장이므로 부족. 아래 (B)를 권한다.
  - (B) **관찰 등급 표시** — "국내 서비스가 자기 모델 파이프라인을 이 정도 해상도로 밝힌 글은 흔치 않다. **이건 이 책이 조사한 범위에서의 인상이지 집계는 아니다.**"
  - (C) **삭제안(가장 간단)** — "...공개한 광고 ML 구조는, 국내 서비스가 자기 모델 파이프라인을 이 정도 해상도로 밝힌 글이다." 뒤 문장("흥미로운 건 ... 단계가 셋으로 나뉘어 있다는 점이다")이 훅을 이미 담당하고 있어 손실이 없다.

**주장 19 — "가장 흔한 이유" (105행)**
- **본문:** "그리고 프로덕션에서는 미래를 볼 수 없으니 그 성능이 재현되지 않는다. Martech의 이탈·전환 예측 모델이 실패하는 **가장 흔한 이유**가 이것이다."
- **판정 ⚠️.** 데이터 누수의 메커니즘 서술(105행 앞부분)은 기술적으로 정확하고 근거가 필요한 종류가 아니다. 그러나 **"가장 흔한 이유"는 실패 원인의 빈도 순위 주장**이고, 이런 집계는 리서치 어디에도 없다. `web_stack.md:1201`은 이탈 예측을 아예 **"⚠️ 확인 불가 (미조회)"**로 분류했다 — 즉 이 책은 **어느 제품이 이탈 예측을 어떻게 하는지조차 확인하지 못한 상태**에서 그 실패 원인의 1위를 지목한 셈이다. 같은 장 138행이 표에서 이탈 예측을 "미확인"으로 적어둔 것과도 어긋난다(**장 내부 불일치**).
- **조치:** 최상급을 빼고 메커니즘 진술로 돌려놓는다.
  - "**이탈·전환 예측 모델에서 오프라인 성능과 프로덕션 성능이 갈리는 대표적인 경로가 이것이다.**"
  - 또는 "**이 실패는 눈에 잘 띄지 않아서 오래 살아남는다.**"

### ❌ 정정 필요 / 🕒 검증 불가

**0건.**

### 08장 종합

**❌ 0 / 🕒 0 / ⚠️ 2 / ✅ 17.** Phase 5를 차단하는 항목 없음.

**최대 위험 지점(Pinterest) 판정 결과 — 위험 없음, 처리가 정확했다.** 영문 조각 네 건이 전부 문자 단위로 일치하고, `"one definition, many runtimes"`는 **원본에서 리서처 요약이며 Pinterest 원문이 아님이 3개 출현 위치 전수 확인으로 확정**됐다. 본문이 이를 리서처 기록으로 위상을 낮춰 제시한 것은 오귀속을 정확히 회피한 처리다.

**2파 경고 3형 재발 여부:**
- **① 고지 범위** — 재발 없음. 71행("이 이중 구현 서술의 출처는 이 책의 리서치가 스택 문서들을 대조해 정리한 관찰이다")과 81행("이 서술 역시 ... 정리한 관찰이라는 점을 밝혀둔다")이 **각각 자기 문단을 자기 안에서 덮는** 자기완결 배치다. 절 단위로 걸어놓고 뒤 문단을 방치한 사례 없음.
- **② 등급 상향** — 재발 없음. 오히려 Covington에서 **원본보다 등급을 내려** 썼다(주장 2).
- **③ 근거 밖 수식어** — **2건 재발**("드문"·"가장 흔한"). 07장의 1건과 합쳐 **3파의 유일한 반복 실패 유형이 ③이다.**

**의심 식별자: 0건.** 등장 식별자는 arXiv `1907.06902`(2019-07, 빌드 시점 대비 과거·RecSys 2019와 정합), DOI `10.1145/3298689.3347058`(RecSys 2019 프로시딩 접두와 일치), DOI `10.1145/3097983.3098021`(KDD 2017)뿐이다. **미래 YYMM·미해석 식별자·검증 불가 인용 없음.**

---

## 09장 — 1차 검증

**검증일:** 2026-07-26 / 대상 `chapters/09_draft.md` / 1차 대조 `research/community.md`·`papers.md`·`web_products.md`
**`(사실 확인 필요)` 주석: 0건** (grep 확인).

> 이 장은 3파에서 **인용 밀도가 가장 높다** — HN 댓글 8건, 학술 논문 4편, RFC 3건, 벤더 2차 문서 1건, 채용 공고 3사. 계획서 금지 13항목 중 **6·12·13번의 본진**이기도 하다. 그래서 인용문은 **원문 대조**, 논문은 **신선도 원장 등급 대조**, 금지 항목은 **grep 전수**로 각각 검증했다.

### ✅ 확인됨

**주장 1 — 여는 HN 인용 winkelwagen (3~7행) ⭐ 번역 인용 무결성 검사**
- **본문:** "2024년 1월, 해커뉴스에..." + 번역 인용(2주 동안 푸시 4번, 이메일 4번, 전면 광고 2번 / 연간 프리미엄 요금제 / 평생 구독권 / 수면의 질과 집중, 명상) + "— winkelwagen, Hacker News 댓글 38840135 (2024-01-02). 한 사용자의 개인 진술이다."
- **근거:** `community.md:663~664` 영문 원문 —
  `"It's not only push notifications, it's the combination of everything communication channel combined. I recently unsubscribed to a services that kept spamming me their "lifetime subscription" product, while I already was on their yearly premium plan. Over the course of 2 weeks, I received 4 push notifications, 4 emails and 2 times when I opened the app it had a full screen ad. I'll never use this product again. Ironically, this app focuses on sleep quality, focus and meditation."`
- **⭐ 번역 인용의 수치 전수 대조 (번역문은 숫자 날조가 숨기 가장 쉬운 자리다):**
  | 본문 한글 | 영문 원문 | 판정 |
  |---|---|---|
  | 2주 동안 | `Over the course of 2 weeks` | ✅ |
  | 푸시 4번 | `4 push notifications` | ✅ |
  | 이메일 4번 | `4 emails` | ✅ |
  | 전면 광고가 2번 | `2 times ... full screen ad` | ✅ |
  | 연간 프리미엄 요금제 | `yearly premium plan` | ✅ |
  | 평생 구독권 | `"lifetime subscription" product` | ✅ |
  | 수면의 질과 집중, 명상 | `sleep quality, focus and meditation` | ✅ |
  **원문에 없는 숫자가 번역문에 추가된 사례 0건.** 댓글 ID 38840135·날짜 2024-01-02는 `community.md:1161` 신선도 원장과 일치.
- **주목:** 출처 줄의 "**한 사용자의 개인 진술이다**"가 일화를 통계로 읽지 못하게 막는다. 스레드 성격("푸시 알림이 왜 이렇게 지겨워졌느냐는 스레드") 역시 `community.md:655`의 story 제목("Push notifications – What to push, what not to push, and how often")과 부합.
- **조치:** 없음.

**주장 2 — HN 인용 joshmanders (21~23행)**
- **본문:** 번역 인용(알림을 통째로 켜거나 끄게 만든다 / 거래성과 마케팅성 / 아마존 배송 알림을 포기하지 않고도 아마존 마케팅 푸시만 끌 수 있어야) + "— joshmanders, Hacker News 댓글 38842663 (2024-01-02)"
- **근거:** `community.md:656` 영문 원문 — `"you're blanket opting in or out of notifications. I'd much rather have notifications bucketed into two systems. Transactional and marketing, just like email. I should be able to opt out of Amazon's marketing push notifications without ALSO opting out of getting delivery alerts."` 네 요소(전체 수신/거부, 두 종류 분리, 거래성/마케팅성, 아마존 배송 알림 예시) 전건 일치. ID·날짜 `:1160` 일치.
- **조치:** 없음.

**주장 3 — Insider 트랜잭셔널 vs 캠페인 격차 (27행) — 장 간 사실 일치 확인**
- **본문:** "2026년 7월 문서 기준으로 Insider의 트랜잭셔널 이메일 발송은 초당 9,000요청까지 허용되는데, 이메일 캠페인 생성은 초당 1요청이다."
- **근거:** `web_products.md:474`("9000 requests per second")·`:477`("1 request per second")·`:470`(2026-07-12 문서 표기 기준).
- **⭐ 장 간 교차 점검:** 같은 두 수치가 **07장 184~185행 표**에도 등장한다. **값·단위·시점 표기 모두 동일**하고(9,000 rps / 1 rps / "2026년 7월 문서 기준"), 계획서 §B:220의 시점 병기도 **양쪽 다 문장 안에** 있다. **통합 원고에서 충돌하지 않는다.** (참고: 1~6장 final에는 이 수치가 등장하지 않는다 — grep 확인.)
- **조치:** 없음.

**주장 4 — Adobe Journey Optimizer의 계층 분리 (51행)**
- **본문:** "Adobe는 Journey Optimizer가 Experience Platform 위에 네이티브로 얹혀 같은 데이터 기반과 아이덴티티 그래프를 공유한다고 문서에 적어두었고, 같은 분리가 다른 벤더에서도 반복된다."
- **근거:** `web_products.md:753`("Real-Time CDP = 데이터 기반(**프로필·아이덴티티 그래프**), Journey Optimizer = 그 위에서 저니를 실행하는 애플리케이션. **둘이 같은 Experience Platform 데이터 기반을 공유한다.** 이 분리가 Insider(UCD + Architect), Braze(users + Canvas) 등 다른 벤더에서도 같은 형태로 반복된다") + `:868`("AEP 위에 네이티브"). "아이덴티티 그래프"·"네이티브"·"반복된다"까지 전건 일치.
- **조치:** 없음.

**주장 5 — Lemon & Verhoef (2016) (53행) ⭐ 계획 M5 준수**
- **본문:** "가장 많이 인용되는 논문은 Lemon & Verhoef (2016), 'Understanding Customer Experience Throughout the Customer Journey,' *Journal of Marketing* 80(6), 69–96이다. 다만 이 책의 리서치는 이 논문의 서지와 피인용 수까지만 확인했고 초록을 확보하지 못했다. 그래서 여기서는 이름과 '이 어휘에 학술적 계보가 있다'는 사실까지만 옮긴다. 11장에서 만날 어트리뷰션·증분성 연구들과 같은 무게로 읽으면 곤란하다. 그쪽은 초록과 수치까지 확인한 근거이고, 이쪽은 아직 이름뿐이다."
- **근거:** `papers.md:119`(저자·제목·*Journal of Marketing* **80(6), 69–96**·DOI `10.1509/jm.15.0420`) + 원장 `:1152` 조회 **`CR+S2`** / 확인 수준 **`메타데이터`**.
- **⭐ "피인용 수까지 확인했다"는 주장의 검증:** `papers.md:121`이 **"피인용수: 4,866 (Semantic Scholar, 2026-07-25 조회)"**를 실제로 기록하고 있다. **리서치가 하지 않은 확인 행위를 주장한 것이 아니다.** (2파 경고 ②는 등급을 올려 말하는 실패였는데, 여기서는 확인 행위의 존재 자체가 원본에서 확인된다.)
- **⭐ 계획 M5(이름·개념적 기여만 귀속) 준수:** `papers.md:122`의 핵심 주장 필드에는 **"구매 전 → 구매 → 구매 후 순환 여정" 3단계 구조와 터치포인트 4유형(브랜드/파트너/고객/사회적 소유)**이 적혀 있다. 본문은 **그 어느 것도 옮기지 않았다.** 수치·프레임워크 내용 0건, 이름과 계보 존재만. 등급 준수.
- **추가 주목:** "11장 ... 그쪽은 초록과 수치까지 확인한 근거이고, 이쪽은 아직 이름뿐이다"는 **독자에게 근거 등급 차이를 명시적으로 알리는 장치**다. 2파 D-3(리서치 판정과 등급을 나눠 표시)의 확장 적용.
- **조치:** 없음.

**주장 6 — Godfrey, Seiders & Voss (2011) (59~61행)**
- **본문:** "Godfrey, Seiders & Voss (2011), 'Enough Is Enough! The Fine Line in Executing Multichannel Relational Communication,' *Journal of Marketing* 75(4), 94–109다. 제목이 이미 방향을 말한다 — 이만하면 충분한 선이 있고, 그 선을 넘으면 곤란해진다. 빈도에 최적점이 존재한다는 구조 자체가 학술 문헌에서 다뤄졌다는 뜻이다." + "이 리서치는 위 논문의 서지 정보와 피인용 수까지 확인했고 초록 본문은 확보하지 못했다. 그래서 '주당 몇 회가 최적'이라는 식의 수치는 이 논문에 귀속시키지 않는다. 방향까지가 안전선이다."
- **근거:** `papers.md:620`(저자·제목·*Journal of Marketing* **75(4), 94–109**·DOI `10.1509/jmkg.75.4.94`) + `:623`(**피인용수 166**, Semantic Scholar 2026-07-25 — "피인용 수까지 확인" 주장의 근거) + `:625`("**최적점이 존재**한다 — 너무 적어도, 너무 많아도 안 된다. **제목 자체가 결론이다**") + `:627` ⚠️ 주의("Semantic Scholar가 초록을 제공하지 않아 **구체적 최적 빈도 수치를 이 논문에 귀속시키지 마라.** '주당 N회가 최적'이라고 쓰려면 fact-checker의 본문 확인이 필요하다") + 원장 `:1203` **`메타데이터`**.
- **⭐ 원본의 경고를 문장으로 그대로 이행했다.** `papers.md:627`이 금지한 "주당 N회" 표현을 **본문이 스스로 예시로 들며 쓰지 않겠다고 선언**했다. 수치 귀속 0건(grep — 9장에 빈도 관련 수치 0건). 계획서 §A 추가 규율("둘 다 `메타데이터 확인` — 구체 수치·결론 방향을 귀속시키지 마라") 중 **수치 축 완전 준수.**
- **결론 방향 축:** 본문은 "빈도에 최적점이 존재한다는 구조"까지 썼는데, 이는 `papers.md:625`가 **"제목 자체가 결론이다"**라고 명시한 범위이고 제목(`Enough Is Enough! The Fine Line`)이 담은 방향이다. 원본이 허용한 폭 안. 단 아래 ⚠️ 1건 참조.
- **조치:** 없음.

**주장 7 — Zhang, Kumar & Cosguner (2017) (63행) ⭐ 리서처 요약 누출 여부 검사**
- **본문:** "Zhang, Kumar & Cosguner (2017), 'Dynamically Managing a Profitable Email Marketing Program,' *Journal of Marketing Research* 54(6), 851–866. 이쪽은 확인 수준이 더 얕아서, 이 책은 제목과 서지를 옮기는 데서 멈춘다. 무엇을 발견했는지는 원문을 열어본 사람만 말할 수 있다."
- **근거:** `papers.md:631`(저자·제목·*JMR* **54(6), 851–866**·DOI `10.1509/jmr.16.0210`) + 원장 `:1204` 조회 **`CR`** / 확인 수준 **`메타데이터`**.
- **⭐ 누출 검사 결과 — 없음.** `papers.md:633`의 핵심 주장 필드는 이 논문을 **"이메일 발송을 정적인 규칙이 아니라 **동태적 최적화 문제**로 본다 — 지금 한 통 더 보내는 것의 단기 이익과, 그로 인한 구독 해지·피로도의 장기 손실을 함께 고려한다"**로 요약한다. 본문은 **이 요약의 어느 조각도 옮기지 않았다.** "동태적"·"최적화"·"단기 이익"·"장기 손실"·"구독 해지" 전부 9장 미등장(grep 확인). 제목의 `Dynamically`는 영문 제목 안에만 있고 한글로 풀어 설명하지 않았다. **"무엇을 발견했는지는 원문을 열어본 사람만 말할 수 있다"로 멈췄다는 저술가 보고가 사실로 확인됐다.**
- **조치:** 없음(단 아래 ⚠️ 1건은 이 문단의 표현에 관한 것).

**주장 8 — Araújo et al. (2022) (65행)**
- **본문:** "응용 저널 논문 한 편 — Araújo et al. (2022), 'A Novel Approach for Send Time Prediction on Email Marketing,' *Applied Sciences* 12(16), 8310. 다만 이 저널은 마케팅 분야의 최상위 저널이 아니어서, 이 논문으로 말할 수 있는 것은 '그런 시도가 학술 문헌에 존재한다'까지다."
- **근거:** `papers.md:647`(저자·제목·*Applied Sciences*(MDPI) **Vol.12, No.16, Article 8310**, 2022·DOI `10.3390/app12168310`) + `:648` ⚠️ 위상 경고("*Applied Sciences*(MDPI)는 마케팅 최상위 저널이 아니다... 이 논문은 '**그런 시도가 학술 문헌에 존재한다**' 수준으로만 인용하라") + 원장 `:1206`(⚠️저널 위상 낮음 / `메타데이터`).
- **판정 ✅ — 경고 문구가 원본과 문자열 수준으로 일치**하고, 서지 4요소도 일치.
- **형식 일탈 1건(감점 아님, 기록만):** 위임 지시는 "저널 위상 경고를 **같은 문장에** 달았는가"였다. 실제로는 **바로 다음 문장**이다("... 8310. **다만** 이 저널은 ..."). 그러나 (a) 마침표 하나 뒤 인접 문장이고, (b) `다만`으로 앞 문장을 직접 받으며, (c) 사이에 다른 주장이 끼어 있지 않아 **①형(고지가 뒤 문단을 못 덮음) 위험이 발생하지 않는다.** 실질 구속력 충족으로 판정한다. ❌로 격상하지 않는다.
- **조치:** 없음.

**주장 9 — 발송 시각 최적화의 근거 상태 (65~67행) ⭐ 계획서 §A 추가 규율의 본진**
- **본문:** "이 책의 리서치는 2026년 7월 25일 조회 기준으로 최상위 마케팅 저널에서 이 기능을 검증한 연구를 찾지 못했다. 찾은 것은 세 종류다. 업계 블로그의 '최적 발송 시간' 통계, 특허 문서, 그리고 응용 저널 논문 한 편"
- **근거:** `papers.md:655`(D-13-5) — "**최상위 마케팅/CS 저널의 검증 연구를 이번 세션에서 찾지 못했다.** 웹 검색에서 나온 것은 (a) 업계 블로그의 '최적 발송 시간' 통계, (b) 특허 문서(USPTO), (c) 위 D-13-4 같은 응용 저널 논문이다" + `:656`(검색 시점 2026-07-25). **세 종류의 목록·순서·판정 전건 일치**, 조회 시점 병기.
- **주목:** `papers.md:655`는 특허 번호(USPTO 11341516 / 11431663)까지 갖고 있는데 본문은 **번호를 쓰지 않았다.** 쓸 수 있는 식별자를 안 쓴 쪽이라 위험 없음.
- **두 토글 대비 구도(55~71행)** — `papers.md:657` 처리 권고("빈도 제한에는 근거가 있고(D-13-1, D-13-2), **발송 시각 최적화는 대체로 벤더 주도 기능**이다") 및 계획서 §A 추가 규율("벤더가 'AI 발송 시각 최적화'를 팔 때와 '빈도 상한'을 말할 때 근거 강도가 다르다 — 이 대비 자체가 9장의 핵심 소재다")을 **한 절 통째로 이행**했다. 67행이 "4장에서 근거가 끊긴 항목 열두 건을 표로 정리했는데, 그 3번 행이 바로 이 기능이었다"로 **4장 예고를 회수**하는데, `papers.md:1106`의 목록에서 Send-time optimization이 실제로 **3번 행**이다. 순번 일치.
- **조치:** 없음.

**주장 10 — HN dirtae / callalex와 "13년 넘게" (89행) ⭐⭐ 계획서-원본 drift의 현장**
- **본문:** "이 책이 열어본 해커뉴스 스레드에서 마케팅 알림이 채널 자체를 망가뜨린다는 불만은 2012년 7월(dirtae)에도 있었고 2025년 9월(callalex)에도 있었다. **13년 넘게** 같은 말이 반복되는 셈이다. 다만 이건 이 리서치가 확보한 표본에서의 관찰이고, 그 표본은 영어권 해커뉴스에 크게 치우쳐 있다. 업계 전체의 통계로 읽으면 안 된다."
- **근거:** `community.md:677`(HN **4210820 / dirtae / 2012-07-07**) + `:680`(HN **45265010 / callalex / 2025-09-16**) + `:683` 관찰 사실("**2012년(dirtae) → 2025년(callalex)까지 13년간 동일한 불만이 반복**된다") + 원장 `:1166`·`:1199` 날짜 일치.
- **판정 ✅ — 원본과 완전 일치.** 연도·인물·기간 3요소 모두 `community.md`가 직접 기록한 값이다. 산술로도 2012-07 → 2025-09는 13년 2개월이라 "13년 넘게"가 정확하다. **계획서·`01_reference.md`의 "14년"을 따르지 않고 원본을 따른 저술가의 판단이 옳다** (상세 판정은 아래 「계획서-원본 drift 판정」 절).
- **"반복"이라는 표현의 근거 — 양 끝점만이 아니다.** `community.md:683`이 이어서 **"중간 지점도 촘촘하다(2022 fmajid, 2023 015a, 2024 joshmanders·winkelwagen·PurestGuava)"**고 명시한다. 실제 원본에 2022-06-05(fmajid), 2023-10-01(015a), 2024-01-02(joshmanders·winkelwagen), 2024-04-20(PurestGuava) 항목이 모두 있다. **양 끝점 두 개로 "반복"을 주장한 것이 아니다.** 통과.
- **⭐ 표본 편향 고지:** "이 리서치가 확보한 표본에서의 관찰이고, 그 표본은 영어권 해커뉴스에 크게 치우쳐 있다. 업계 전체의 통계로 읽으면 안 된다" — `community.md:684`의 경고를 넘어서는 **자발적 방어**다. 3파 전체에서 가장 잘 쓰인 고지 중 하나.
- **조치:** 없음.

**주장 11 — HN sbov 딜리버러빌리티 인용 (95~97행)**
- **본문:** 번역 인용("이메일, 특히 딜리버러빌리티는 토끼굴이다... (…) 볼륨이 커지면 진작 했어야 할 관행들이 있는데 그건 경험으로만 배우게 되고, 그걸 안 지키면 앞의 걸 다 해도 아무것도 안 들어간다.") + "— sbov, Hacker News 댓글 9115955 (2015-02-26)"
- **근거:** `community.md:690` 영문 원문 — `"Email, deliverability in particular, is a rabbit hole. Its easy enough to get it set up and "basically" working, but not. ... Beyond that, once you hit enough volume, there's best practices should have always been doing but you learn from experience and need to abide by or else you're not getting anything through even though you do all the previously mentione[d]"`. 전건 일치. 생략은 `(…)`로 **명시 표기**했다. ID·날짜 `:1167` 일치.
- **조치:** 없음.

**주장 12 — RFC 3종 분류표 (103~113행) ⭐⭐ 계획서 금지 13항의 본진**
- **본문 표:** RFC 7208 / SPF v1 / 2014-04 / Standards Track · RFC 6376 / DKIM Signatures / 2011-09 / Standards Track · RFC 7489 / DMARC / 2015-03 / **Informational**
- **근거:** `papers.md:667`(RFC 7208, Kitterman, **April 2014**, **Standards Track**) + `:677`(RFC 6376, Crocker·Hansen·Kucherawy, **September 2011**, **Standards Track**) + `:687`(RFC 7489, Kucherawy·Zwicky, **March 2015**, **Informational**) + 원장 `:1207~1209` 조회 **`PG`** / 확인 수준 **`문서 확인`**. **12개 셀 전건 일치, 오류 0.**
- **⭐ "원문 페이지를 직접 열어 확인했다"는 주장(109행)의 검증:** `papers.md:663`이 절 머리에 **"세 RFC 모두 rfc-editor.org 원문 페이지를 직접 조회해 번호·제목·저자·발행일·카테고리·초록을 확인했다"**고 기록하고, 원장의 조회 경로가 `PG`(랜딩 페이지 직접 조회), 확인 수준이 `문서 확인`(1차 문서 직접 조회)이다. **리서치가 실제로 한 행위와 본문 주장이 일치한다. 웹 2차 검증 불필요.**
- **⭐ 금지 13항("DMARC를 '표준'이라 부르지 마라") — 위반 0건, 오히려 정면 이행.** 9장에서 "표준"은 두 번 등장하는데(109·111행) **둘 다 업계 관행 호칭을 반박하는 문맥**이다: ①"셋을 '이메일 인증 표준 삼종 세트'로 묶어 부르는 게 업계 관행이다. **그런데** IETF의 발행 분류로는 SPF와 DKIM만 Standards Track이고, DMARC는 Informational이다" ②"우리가 '표준'이라고 부를 때 **그 권위가 어디서 오는지**를 정확히 아는 데 있다". **DMARC를 표준으로 지칭한 사례 0건.** 2파 로그가 "4장 표가 이 항목을 '9장'으로 예고해뒀으니 9장이 이 판정을 실제로 다뤄야 한다"고 요구했는데, **요구가 이행됐다.**
- **⭐ 과잉 해석 방지 문단(111행):** "Informational이라는 분류는 '구현하지 않아도 된다'는 뜻이 아니다... 운영상으로는 사실상 필수에 가깝다." `papers.md:689`의 정확성 포인트가 경계한 오독을 **책 스스로 차단**했다. 정확한 사실 진술이 잘못된 실무 결론으로 번지는 것을 막는 모범.
- **기능 서술(113행):** "SPF와 DKIM의 검증 결과를 발신 주소 도메인과 정렬(alignment)시키고... none / quarantine / reject ... 리포트를 어디로 보낼지" → `papers.md:690`("SPF/DKIM 결과를 **From 도메인과 정렬(alignment)** 시키고, 실패 시 정책(none/quarantine/reject)과 리포팅을 정의한다") 일치. 서브도메인 분리 설계도 같은 행.
- **조치:** 없음.

**주장 13 — HN spdustin DMARC 리포트 (115행)**
- **본문:** "한 사용자는 DMARC 리포트를 모아보는 도구를 붙이고 나서야, 인증됐다고 믿었던 캠페인 메일이 실제로는 검증에 실패하고 있었고 일부 기업 메일 시스템이 그 메일을 배달하지 않고 있었다는 걸 알게 됐다고 적었다(HN 9720330 / spdustin / 2015-06-15)."
- **근거:** `community.md:701` — `"We used this and discovered that our "authenticated" Mailchimp campaigns were actually failing to be validated properly, and some email systems (especially corporate systems with spam filtering appliances like Barracuda) were not delivering our email."` 세 요소(인증됐다고 믿음 / 실제로는 검증 실패 / 일부 기업 메일 시스템이 미배달) 일치. story("Show HN: A free tool to monitor and implement DMARC")가 "도구를 붙이고 나서야"를 뒷받침. ID·날짜 `:1170` 일치.
- **주목:** 원문의 벤더명(`Mailchimp`·`Barracuda`)을 **본문이 익명화**했다. 특정 제품 결함으로 읽히지 않게 하는 처리이고 사실 손실 없음.
- **조치:** 없음.

**주장 14 — HN davideous 평판 원리 (117행)**
- **본문:** "받는 사람이 원하고 예상하는 메일을 보내는 것이 인박스에 들어가는 열쇠이고, 주문 확인 페이지에 미리 체크된 수신 동의 박스 같은 걸로 선을 넘으면 대가를 치른다는 진술이 2014년에 이미 나와 있다(HN 7621371 / davideous / 2014-04-21)."
- **근거:** `community.md:704` — `"The key to delivering into the inbox is sending mail that your recipients both want and expect. Provide a good user experience, and you'll build a good reputation. Push the limits (for example, use a "pre checked" checkbox on an order confirmation page to put people on your sales mailing list) and you'll be [penalized]"`. **"원하고 예상하는"(want and expect)·"미리 체크된 체크박스"·"주문 확인 페이지"** 전건 일치. ID·날짜 `:1171` 일치.
- **조치:** 없음.

**주장 15 — 3사 Deliverability 채용 (119행) ⭐ 계획서 §B:221 계열 준수**
- **본문:** "**2026년 7월 25일 Greenhouse 공고를 조회한 시점에** Braze는 이메일 딜리버러빌리티 컨설턴트와 팀 리드를, Klaviyo는 Deliverability Strategist를, Hightouch는 Deliverability Specialist를 각각 채용 중이었다."
- **근거:** `community.md:244`("F-1-B. 해외 (Greenhouse Job Board API, **조회일 2026-07-25**)") + `:276~278`:
  - Braze: `Senior Email Deliverability Consultant` ×4(Austin/NYC/Chicago/SF), `Team Lead, Email Deliverability` ×4 → 본문 "이메일 딜리버러빌리티 컨설턴트와 팀 리드" ✅
  - Klaviyo: `Deliverability Strategist`(London) ✅
  - Hightouch: `Deliverability Specialist` ✅
- **⭐ 두 규율 동시 준수:** ① **조회 시점이 문장 안에** 들어 있다(계획서 §B:221의 채용 공고 처리 방식). ② **회사명을 개별 나열하고 숫자로 압축하지 않았다** — 원본에 `×4`가 두 번 있는데 본문은 그 수치를 쓰지 않았다. 채용 규모를 주장하지 않으므로 시점 경과에 따른 사실 붕괴 위험이 낮다.
- **조치:** 없음.

**주장 16 — 알림톡 출처 고지와 인용 (127~129행) ⭐⭐ 이 절의 신뢰도를 지탱하는 문단**
- **본문:** "먼저 출처를 밝혀둔다. 이 책의 리서치는 카카오의 공식 개발 문서 **세 개 주소를 모두 열지 못했다.** 그래서 아래 내용은 **국내 메시징 벤더가 카카오 가이드를 인용해 정리한 실무 문서(2025년 8월 26일 발행)**에서 가져온 것이다. **벤더 자사 블로그이므로 이해관계가 있다는 점을 감안하고 읽어야 하고**, 실제로 구축할 때는 카카오의 최신 공식 가이드를 다시 확인하는 편이 낫다." + 인용문
- **근거:**
  - **3개 URL 실패** → `community.md:1074` — "`business.kakao.com/info/bizmessage/`(연결 실패), `developers.kakao.com/docs/latest/ko/message/rest-api`(404), `kakaobusiness.gitbook.io/main/ad/bizmessage`(404) — **3개 URL 전부 실패**. 알림톡 내용은 **전부 벤더 2차 자료**". 일치.
  - **출처 성격·발행일** → `community.md:823~824`(노티플라이 기술블로그, 게시일 **2025-08-26**) + `:813`(노티플라이 = 자사 블로그 운영, 국내 CRM/메시징 자동화 영역). 일치.
  - **인용문** → `community.md:831` — `"알림톡은 고객의 휴대폰 번호만 있으면 카카오톡 채널 추가 여부와 관계없이 발송이 가능하며, 문자 메시지(SMS, LMS)보다 비용이 합리적인 장점이 있습니다. 하지만 광고성 문구는 허용되지 않으며, 사전에 카카오톡 심사를 통과해야지만 발송할 수 있습니다."` **전건 일치**(원문의 "통과해야지만" 표기까지 보존).
- **⭐ 소절 앞머리 배치 = ①형의 정확한 반대.** 이 고지는 **소절 첫 문단**에 있어 뒤따르는 인용 4건(129·152~156·164·168행) 전체를 덮는다. 2파 ①형(절 단위 고지가 뒤 문단을 못 덮음)이 구조적으로 발생할 수 없는 배치다. **저술가 자기 보고가 사실로 확인됐다.**
- **⭐ 벤더명 비노출:** 본문은 "국내 메시징 벤더"로만 적고 노티플라이를 명시하지 않았다. 이해관계 고지는 하면서 특정 업체 홍보가 되지 않게 하는 처리.
- **조치:** 없음.

**주장 17 — 알림톡 발송 불가 유형 5항 (152~156행)**
- **근거:** `community.md:843~847` — 5개 항목 **번호·문구·괄호 주석(친구톡 권장)·예시(`#{상품명} #{송장정보}`)까지 문자 단위 전건 일치.**
- **파생 서술 검증:** 158행 "장바구니에 담고 결제하지 않은 사람에게 안내를 보내는 것... 그게 이 채널에서는 안 된다. 광고성으로 분류되는 친구톡으로 보내야 하고" → `community.md:849`("서구권 CRM에서 가장 기본적인 자동화인 **장바구니 이탈(cart abandonment) 캠페인**이 한국에서는 채널을 바꿔야 한다") 일치. 162행 "변수만으로 구성된 메시지는 안 된다는 제약은 템플릿 엔진 설계에 직접 걸린다" → `community.md:851`("템플릿 엔진 설계에 직접 영향을 주는 제약") 일치.
- **조치:** 없음.

**주장 18 — 포인트·쿠폰 템플릿 필수 기재 요건 (164행)**
- **본문:** "본문에 업체명, 지급 또는 소멸되는 포인트 금액, 유효기간을 기재해야 하고, 발송 근거도 본문 상단이나 하단에 반드시 넣어야 한다"
- **근거:** `community.md:858~863` — "3) 본문 내 '업체명' 기재 필수 / 4) 본문 내 지급 또는 소멸되는 포인트(마일리지)의 '포인트 금액', '유효기간' 기재 필수 / 5) 본문 상단 또는 하단(부가정보 영역 포함)에 적립금 안내에 대한 발송 근거를 '필수'로 기재 필수". 4요소 일치. 스키마 함의(`:865` "업체명·포인트 금액·유효기간·발송 근거가 전부 필수 필드다")도 일치.
- **조치:** 없음.

**주장 19 — 승인 후 사후 차단 (168~170행)**
- **본문 인용:** `"템플릿이 승인된 이후에도 모니터링을 통해 가이드 위반이 확인될 경우 해당 템플릿에 대해 차단 조치가 취해질 수 있습니다."`
- **근거:** `community.md:853` **전건 일치**. `:855`("승인 후에도 사후 차단이 가능하다 — 즉 프로덕션에서 갑자기 특정 템플릿이 죽을 수 있다. **장애 대응 시나리오에 넣어야 한다**")가 본문 170행의 장애 대응 서술과 일치. 그림 1의 상태 다이어그램(승인 → 발송가능 → 차단)도 이 인용 범위 안.
- **조치:** 없음.

**주장 20 — 심사 리드타임 (148행) ⭐ 수치 0건**
- **본문:** "캠페인 일정을 잡을 때 심사 기간을 앞에 끼워 넣어야 하는데, **그 기간이 며칠인지는 이 책이 확인하지 못했다. 검색 결과에서 리드타임 수치를 보긴 했으나 1차 확인에 실패해서 숫자를 적지 않는다.** 실제 프로젝트에서는 이 값부터 벤더나 카카오 쪽에 확인하고 일정을 잡는 편이 낫다."
- **근거:** `community.md:867`("검색 단계에서 '4-5일간의 검수' 언급을 봤으나 **1차 확인 실패** → `확인 불가 (미조회)`") + `:1095`(미확인 목록에 "알림톡 심사 리드타임 '4-5일'" 등재).
- **판정:** **리드타임 수치 0건 확인**(grep — "4-5일"·"4~5일"·일수 수치 9장 미등장). 원본의 미확인 상태를 **문장 구조까지 그대로 옮겼고**("보긴 했으나 1차 확인에 실패해서"), 미확인을 부재로 읽지 않게 막았다. 2파 D-2의 모범 재현.
- **조치:** 없음.

**주장 21 — 사야 하나 만들어야 하나 (176행)**
- **근거:** `community.md:695`(HN **5648393 / 13rules / 2013-05-03** — "Do you want to become an expert in email deliverability, DNS, bounces, white listing, DKIM, SPF? Or do you want to sell your product?") + `:698`(HN **8532692 / shizcakes / 2014-10-30** — "**Don't run your own mailer as a startup.**") + `:1031`(HN **9471320 / davideous / 2015-05-01** — **"MTA 제품 벤더의 발언 — `이해관계 있음`"**). ID·날짜 3건 모두 원장 `:1168`·`:1169`·`:1172`와 일치.
- **⭐ 이해관계 고지 이행:** 본문이 9471320에 대해 "이건 메일 전송 제품을 만드는 회사 쪽 인사의 발언이라 이해관계를 감안해 읽어야 한다"를 **같은 문장 안에** 붙였다. `community.md:1031`의 `이해관계 있음` 태그를 정확히 옮긴 것.
- **조치:** 없음.

### ⚠️ 근거 약함 (2건)

**주장 22 — "이쪽은 확인 수준이 더 얕아서" (63행)**
- **본문:** (Zhang, Kumar & Cosguner에 대해) "**이쪽은 확인 수준이 더 얕아서**, 이 책은 제목과 서지를 옮기는 데서 멈춘다."
- **판정 ⚠️(용어 정합).** 두 논문의 **`확인 수준`은 동일하다**: `papers.md` 원장 `:1203` Godfrey = **`메타데이터`**, `:1204` Zhang = **`메타데이터`**. `확인 수준`은 `papers.md:9~13`이 정의한 **4등급 전문 용어**(초록 확인 / 문서 확인 / 메타데이터 확인 / 확인 불가)이고, 두 논문은 같은 칸에 있다. 따라서 "확인 수준이 더 얕다"는 **정의된 용어를 사실과 다르게 쓴 것**이다.
- **다만 실질은 참이다.** 조회 **경로**가 다르다 — Godfrey는 `CR+S2`라 **피인용수 166이 확보**됐고(`papers.md:623`), Zhang은 `CR`뿐이라 **피인용수가 없다.** 즉 확인의 **범위**는 실제로 더 좁다. 본문이 바로 앞 문단에서 Godfrey에 대해 "서지 정보와 **피인용 수까지** 확인했고"라고 쓴 것과 대비하면, 저술가가 가리키려 한 것이 이 범위 차이임이 분명하다. **사실 오류가 아니라 용어 충돌**이므로 ❌가 아니라 ⚠️로 판정한다.
- **왜 그냥 두면 안 되나:** 이 책은 `확인 수준`이라는 말을 근거 등급의 이름으로 여러 장에서 쓴다. 같은 등급의 두 논문에 "수준이 더 얕다"를 쓰면, 독자가 Zhang을 `확인 불가` 등급으로 오독하거나 반대로 Godfrey를 `초록 확인`으로 올려 읽을 수 있다.
- **조치:** "수준"을 "범위"로 바꾸고 무엇이 좁은지 명시한다.
  - "**이쪽은 확인 범위가 더 좁아서(서지는 확인했지만 피인용 수까지는 확보하지 못했다), 이 책은 제목과 서지를 옮기는 데서 멈춘다.**"
  - 더 짧게: "**이쪽은 서지만 확인했고 그 이상은 확보하지 못해서, 제목과 서지를 옮기는 데서 멈춘다.**"

**주장 23 — "제목이 이미 방향을 말한다" 뒤의 확장 (59행)**
- **본문:** "제목이 이미 방향을 말한다 — 이만하면 충분한 선이 있고, 그 선을 넘으면 곤란해진다. **빈도에 최적점이 존재한다는 구조 자체가 학술 문헌에서 다뤄졌다는 뜻이다.**"
- **판정 ⚠️(경미, 경계선).** 앞부분("이만하면 충분한 선이 있고, 그 선을 넘으면 곤란해진다")은 제목 `Enough Is Enough! The Fine Line`의 직역 범위라 안전하다. 뒷문장의 "**최적점이 존재한다**"는 `papers.md:625`가 쓴 표현("**최적점이 존재**한다 — 너무 적어도, 너무 많아도 안 된다")과 일치하므로 **원본 밖으로 나가지는 않았다.** 다만 원본의 그 문장은 `메타데이터` 등급 항목의 **핵심 주장 필드**(리서처가 제목·분야 통념에서 재구성한 것)이고, 같은 항목 `:627`이 **"Semantic Scholar가 초록을 제공하지 않아"**라고 초록 부재를 명시한다. 즉 "최적점이 있다"는 **제목이 함의하는 방향이지 초록으로 확인된 결론이 아니다.** 계획서 §A 추가 규율은 이 두 논문에 대해 "**구체 수치·결론 방향을 귀속시키지 마라**"고 했는데, 수치 축은 완벽히 지켰으나 **방향 축이 "존재한다"는 단정형에 살짝 걸친다.**
- **정상 참작:** 바로 다음 문단(61행)이 "이 리서치는 ... 초록 본문은 확보하지 못했다 ... **방향까지가 안전선이다**"로 **스스로 방향까지만 쓰겠다고 선언**하고 있어, 독자가 이를 초록 확인 결론으로 오독할 여지는 크지 않다. ❌로 격상하지 않는다.
- **조치(선택, 한 어절):** "빈도에 최적점이 존재한다는 구조 자체가 학술 문헌에서 다뤄졌다는 뜻이다" → "**빈도에 최적점이 있다는 구조 자체가 학술 문헌의 주제가 됐다는 뜻이다.**" (주제화 사실로 낮춤 — "다뤄졌다"를 살리는 안이므로 원안과 큰 차이는 없다. 61행 고지가 이미 받쳐주고 있어 무수정도 허용 가능.)

### ❌ 정정 필요 / 🕒 검증 불가

**0건.**

### 09장 종합

**❌ 0 / 🕒 0 / ⚠️ 2 / ✅ 21.** Phase 5를 차단하는 항목 없음.

**인용 무결성:** HN 댓글 8건 전부 ID·날짜·본문이 `community.md` 원문과 일치. **번역 인용 2건(3·21행)의 숫자 7개를 전수 대조했고 날조 0건.** 학술 4편·RFC 3건 전부 서지 전건 일치. 벤더 2차 문서 인용 4건 문자 단위 일치.

**최대 위험 지점(학술 인용 등급) 판정:** Godfrey·Zhang은 **수치 귀속 0건**, Zhang은 **리서처 요약("동태적 최적화") 누출 0건**, Lemon & Verhoef는 **프레임워크 내용(3단계·터치포인트 4유형) 0건**. 등급을 올려 쓴 사례는 없고, ⚠️ 2건은 **용어 정합(주장 22)과 단정 어조(주장 23)**의 문제다.

**2파 경고 3형 재발 여부:**
- **① 고지 범위** — 재발 없음. 알림톡 소절(127행)과 발송 시각 절(65행) 모두 **선행·소절 머리 배치**다.
- **② 등급 상향** — **직접적 재발 없음.** 주장 22가 등급 용어를 잘못 썼지만 방향이 **낮추는 쪽**(같은 등급을 더 얕다고 말함)이라 위험 방향이 반대다. 주장 23이 경계선.
- **③ 근거 밖 수식어** — 재발 없음.

**의심 식별자: 0건.** 9장에는 arXiv ID가 없고, DOI는 `papers.md`가 Crossref로 조회한 값(`10.1509/jm.15.0420`, `10.1509/jmkg.75.4.94`, `10.1509/jmr.16.0210`, `10.3390/app12168310`)이며 본문에는 DOI를 노출하지 않았다. **HN 댓글 ID 8건의 단조성 검사** — 4210820(2012-07) < 5648393(2013-05) < 7621371(2014-04) < 8532692(2014-10) < 9115955(2015-02) < 9471320(2015-05) < 9720330(2015-06) < 38840135·38842663(2024-01) < 40096859(2024-04) < 45265010(2025-09). **ID 크기 순서가 게시 날짜 순서와 완전히 일치한다.** HN ID는 단조 증가하므로 이는 날조 가능성에 반하는 강한 정황이다. 미래 날짜·미해석 식별자 0건.

---

## 금지 항목 스캔 결과 (3파)

**방법:** `chapters/07_draft.md`·`08_draft.md`·`09_draft.md` 3개 파일에 대해 정규식 grep 전수. 히트가 난 항목은 **문맥을 읽어 위반/비위반을 개별 판정**했다.

| # | 금지 항목 (`02_plan.md` §A) | 3파 히트 | 판정 |
|---|---|---|---|
| 1 | CDP 4분류 (Data/Analytics/**Campaign**/**Delivery**) | 0 | ✅ 위반 없음 |
| 2 | "DMP = 서드파티 쿠키, CDP = 퍼스트파티" | 0 (`DMP` 자체 0건) | ✅ |
| 3 | CEM / CXM 비교표 | 0 (두 약어 모두 0건) | ✅ |
| 4 | CDP Institute 기관 공식 정의문 | 0 | ✅ |
| 5 | Ads Data Hub 20/50/10 임계값의 타 클린룸 전용 | 0 | ✅ |
| 6 | PIPA 과징금 % (3% vs 10%), 과징금/과태료 혼용 | 0 (`PIPA`·`과징금`·조문 번호 0건) | ✅ **10장으로 온전히 보존** |
| 7 | 정보통신망법 2026-07-07 개정 "매출액 6%" | 0 (`매출액`·`정보통신망` 0건) | ✅ |
| 8 | SKAdNetwork 세부 (deprecation·버전·conversion value 비트) | 0 (`SKAdNetwork` 0건) | ✅ |
| 9 | Snowplow / RudderStack / Redis를 "오픈소스"로 단정 | `오픈소스` 1건 (08:119) — 지시대상은 **Feast**(Apache 2.0, 금지 목록 외). Snowplow·RudderStack 0건 | ✅ 비위반 |
| 10 | HLL·Bloom filter 수치를 원 논문에 귀속 | 이름 2건 (07:33~34 표) — **수치 0건**(`0.81%`·`12KB`·`14.378비트` 전부 0). `web_stack.md:860`에 12KB가 있는데도 미사용 | ✅ 비위반 |
| 11 | Gordon 2019에 구체 수치 귀속 | 0 (`Gordon` 0건) | ✅ **11장 본진 보존** |
| 12 | LLM 생성 카피의 효과 크기 | 08:145 — **근거 부재를 명시하는 서술**이고 수치 0건 | ✅ 정면 이행 |
| 13 | DMARC를 "표준"이라 부르기 | `표준` 2건 (09:109·111) — **둘 다 업계 관행 호칭을 반박하는 문맥.** DMARC를 표준으로 지칭한 사례 0건 | ✅ **정면 이행** |
| — | Theta Sketch 저자 오귀속 | 0 (`Theta` 0건) | ✅ |
| — | Goldfarb·Tucker / Berman / Blake 범위 한정 누락 | 0 (세 이름 전부 0건) | ✅ **11장 본진 보존** |
| — | Tier 2 버전·수치 (Redpanda·Pulsar·Snowflake·BigQuery·Airflow·Dagster·Spark·Redshift) | `Airflow` 1건 (07:168) — **Hightouch 문서 원문(`triggered by tools like dbt Cloud or Airflow`)에 든 도구명**이고 **버전·수치 0건**. 나머지 7개 제품명 0건 | ✅ 비위반 |
| — | Raab 정의 연도 병기 | 0 (`Raab` 0건 — 3파 미등장) | ✅ 해당 없음 |
| — | 75~80% 오픈율 / 밤 9시 전면 금지 / 제50조 제3항 단서 면제 매체 | 0 | ✅ |
| — | `(사실 확인 필요)` 미해소 주석 | **3개 장 모두 0건** | ✅ |

**위반 0건.** 히트가 난 3건(`오픈소스`·`Airflow`·`표준`)은 전부 문맥 판정 결과 **비위반**이며, 그중 `표준` 2건은 금지 13항을 **어기는 것이 아니라 집행하는** 문장이다.

**시점 병기 필수 항목(§B) 이행 점검:**

| 항목 | 요구 | 3파 실제 | 판정 |
|---|---|---|---|
| Insider API rate limit | "2026년 7월 문서 기준" 병기 | 07:178 표 직전 문장 + 09:27 문장 안 | ✅ 2곳 모두 |
| 채용 공고 | 조회 시점을 **문장 안에** | 09:119 "2026년 7월 25일 Greenhouse 공고를 조회한 시점에" | ✅ |
| `연도 추정` 버전(Feast) | 연도 확정 금지 + "기준" 병기 | 07:44 "Feast(0.65.0 / 2026 기준)" — `web_stack.md:693` 원본 표기와 동일 | ✅ (형식 판정은 07장 주장 3 참조) |
| Tier 2 버전 | 사용 금지 | 0건 | ✅ |
| EU AI Act / Privacy Sandbox | "2026년 7월 기준" | 3파 미등장 (10장 소재) | — |
| Raab 정의 연도 | 병기 | 3파 미등장 | — |

**발행일 없는 출처의 조회 시점 병기 — 3파 전수 이행 확인 (9건):** Apple 프라이버시 페이지(07:11) · Segment 문서 리포(07:98) · Adobe AEP(07:102, 갱신일) · mParticle(07:108, 갱신일) · UID2(07:130, 갱신일) · Hightouch(07:160, 페이지 표기) · Insider(07:178, 문서 기준) · Feast 문서(08:115, "발행일 확인 불가 | 검색 시점") · Sculley/Pinterest(08:87·125, 검색 시점). **누락 0건** — 2파 D-1 항목이 3파에서도 유지됐다.

**의심 식별자 스캔 — 0건 (명시적 선언).**
3파 전체에서 본문에 노출된 식별자는 ① arXiv `1907.06902` ② DOI `10.1145/3298689.3347058` ③ HN 댓글 ID 8건 ④ RFC 번호 3건 ⑤ 벤더 문서 URL이다. 각각에 대해:
- **arXiv `1907.06902`** — YYMM=1907(2019-07)은 빌드 시점(2026-07) 기준 과거이고, RecSys 2019 발표 시기와 정합하며, `papers.md:239`가 arXiv API로 직접 조회한 값이다. **미래 YYMM 자동 ❌ 규칙 해당 없음.**
- **DOI `10.1145/3298689.3347058`** — 접두 `3298689`가 RecSys 2019 프로시딩과 일치하고 `papers.md`가 Crossref/arXiv 교차 확인. 형식 이례 없음.
- **HN ID 8건** — ID 크기 순서가 게시 날짜 순서와 **완전 단조 일치**(09장 종합 참조). HN ID는 단조 증가하므로 날조에 반하는 정황.
- **RFC 3건** — `rfc-editor.org` 원문 페이지 직접 조회(`papers.md:663`, 조회 경로 `PG`).
- **벤더 URL** — 전부 `research/*.md`의 신선도 원장에 조회일과 함께 등재.
**형식상 이례적이거나 해석되지 않는 식별자, "너무 깨끗한" 검증 불가 인용 없음. 따라서 웹 2차 에스컬레이션 대상 0건이며, 이 판정을 `초록 확인`·`문서 확인` 등급 항목의 통과 근거와 별도로 명시해둔다.**

**웹 2차 검증 수행 건수: 0건.** 3파의 Critical 주장은 전부 `research/*.md` 1차 대조로 확정됐다. 특히 웹 확인을 고려했던 두 후보가 모두 원본에서 해소됐다 — ① **RFC 카테고리**(09:109가 "원문 페이지를 직접 열어 확인했다"고 주장): `papers.md:663` + 원장 조회 경로 `PG`/`문서 확인`이 그 행위를 기록하고 있어 확인 완료. ② **Feast 0.65.0**: `web_stack.md:693`에 원본 표기 존재. 비용 통제 규칙에 따라 불필요한 웹 호출을 하지 않았다.

---

## 계획서-원본 drift 판정 (§7-4 "13년 vs 14년")

> 9장 저술가가 보고한 계획서·레퍼런스와 원본의 불일치를 **원본에서 직접 확인해 판정한다.** 결론부터: **저술가 판단이 전부 옳고, `01_reference.md` §7-4가 종합 과정에서 생긴 오차다.**

### 1. 원본이 말하는 것 (`research/community.md` — 1차 대조 대상)

| 항목 | 원본 값 | 위치 |
|---|---|---|
| 시작점 | **dirtae, HN 4210820, 2012-07-07** | `:677`, 원장 `:1166` |
| 종점 | **callalex, HN 45265010, 2025-09-16** | `:680`, 원장 `:1199` |
| 기간 | **13년** | `:683` |
| PurestGuava | **HN 40096859, 2024-04-20** — 중간 지점이지 종점이 아니다 | `:674`, 원장 `:1165` |
| 명시 경고 | **"이 문서가 확보한 가장 최근 푸시 불만은 2025-09다. `\"2026년까지\"라고 쓰지 말 것.`"** | `:684` |

`community.md:683` 원문:
> 📌 `관찰 사실`: **2012년(dirtae) → 2025년(callalex)까지 13년간 동일한 불만이 반복**된다. 중간 지점도 촘촘하다(2022 fmajid, 2023 015a, 2024 joshmanders·winkelwagen·PurestGuava).

**저술가가 보고한 경고 문구는 실재하며, 인용도 정확했다.**

### 2. 파생 문서가 말하는 것

- **`01_reference.md:1909` (§7-4):** "`관찰 사실`: **2012년(dirtae) → 2026년(PurestGuava)까지 14년간 동일한 불만이 반복된다.**"
- **`02_plan.md:564`:** "**14년 동안 같은 불만이 반복된다**(§7-4) — 2012년 dirtae부터 2026년까지."

### 3. 판정 — ❌ **`01_reference.md` §7-4가 오류다 (원본 대비 3중 오차)**

| # | 오차 | 원본 | §7-4 |
|---|---|---|---|
| 1 | **종점 인물 오귀속** | callalex | PurestGuava |
| 2 | **종점 연도 오기** | 2025 (PurestGuava는 **2024-04-20**) | 2026 |
| 3 | **기간 오기** | 13년 | 14년 |

**오차 3은 1·2의 산술적 귀결이다.** 그리고 오차 2는 원본이 명시적으로 금지한 바로 그 표현이다 — `community.md:684`가 **"`2026년까지`라고 쓰지 말 것"**이라고 적었는데 §7-4가 정확히 `2026년`을 썼다. 게다가 §7-4가 종점으로 귀속한 PurestGuava는 원본에서 **2024-04-20**이므로, 그 인물을 근거로 삼아도 2026년은 나오지 않는다.

**오차 발생 경로(추정 근거 있음):** `community.md:677`의 항목 머리글이 dirtae 댓글을 **"14년 전에도 같은 말"**이라고 소개한다. 이는 *2026년 시점에서 본 그 댓글의 나이*로는 참이다(2026 − 2012 = 14). 종합 과정에서 이 **"14년 전"**(댓글의 나이)이 **양 끝점 사이의 기간**(13년)과 뒤섞이면서, 14년이라는 숫자가 살아남고 종점이 2026년으로 밀려난 것으로 보인다. 종점 인물이 callalex에서 PurestGuava로 바뀐 것도 같은 재구성 과정의 흔적일 가능성이 높다.

### 4. 본문 판정 — ✅ **9장 89행이 옳다**

본문: "2012년 7월(dirtae)에도 있었고 2025년 9월(callalex)에도 있었다. **13년 넘게** 같은 말이 반복되는 셈이다."
→ 인물·연월·기간이 `community.md:677`·`:680`·`:683`과 전건 일치. 2012-07 → 2025-09 = 13년 2개월이므로 "13년 넘게"는 산술적으로도 정확하다. **저술가가 계획서 문구를 따르지 않고 1차 대조 대상인 원본을 따른 것은 규율(`02_plan.md` §C: "fact-checker의 1차 대조 대상은 `research/*.md` 원본")에 정확히 부합하는 판단이다.**

### 5. 🚩 후속 리뷰에 대한 구속력 있는 지시

**`01_reference.md` §7-4(`:1909`)와 `02_plan.md:564`의 "14년 / 2026년 / PurestGuava" 문구를 근거로 9장 89행을 되돌리지 마라.** 두 문서는 이 지점에서 원본과 어긋나 있고, 원본에는 그 표현을 쓰지 말라는 명시 경고까지 달려 있다.
- **editor / manuscript-reviewer(Phase 4.5):** 통합 원고에서 "14년"을 발견하면 그것이 오류다. 정본은 **13년 넘게 / 2012-07 dirtae → 2025-09 callalex**다.
- **레퍼런스 수정 여부:** `01_reference.md`는 Phase 1 산출물이라 본 검증에서 고치지 않았다. 다만 10~12장이 §7-4를 다시 인용할 경우 같은 오차가 재유입되므로, 이 항목이 재등장하면 **반드시 `community.md:683~684`로 직접 대조할 것.**
- **부수 확인:** "반복된다"는 표현 자체는 유효하다 — `community.md:683`이 중간 지점(2022 fmajid, 2023 015a, 2024 joshmanders·winkelwagen·PurestGuava)을 명시하므로 양 끝점만으로 세운 주장이 아니다.

---

## 10~12장 저술가에게 — 사실 규율 경고 (3파 검증에서 도출)

> 2파 말미의 경고를 갱신한다. **3파 3개 장에서 ❌·🕒가 0건이었고**, 2파가 지목한 실패 3형 중 **①·②는 재발하지 않았다.** 남은 것은 ③ 하나이고, **미소진 지뢰는 이제 10·11장 두 장에 집중돼 있다.**

### A. 3파 결산 — 무엇이 고쳐졌고 무엇이 남았나

| 2파 경고 | 3파 재발 | 근거 |
|---|---|---|
| **① 고지를 절 단위로 잡기** | **0건 — 완전히 고쳐졌다** | 07:160(선행 고지가 뒤 네 문단을 덮음) · 08:71·81(자기완결 배치) · 09:127(소절 머리 배치가 인용 4건을 덮음) |
| **② 확인 수준을 한 칸 올려 말하기** | **0건 — 오히려 반대로 갔다** | 07 Fellegi & Sunter(세 영역 형식 0건 사용) · 08 Covington(원본의 "산업 표준"을 **책의 관찰로 강등**) · 07 mParticle(원본 `검색 요약`을 **"확인 불가"로 하향**) |
| **③ 근거 있는 문장에 근거 없는 수식어** | **3건 재발 — 3파의 유일한 반복 유형** | 07:195 "**CDP의** API 표면 절반" · 08:11 "밝힌 **드문** 글" · 08:105 "실패하는 **가장 흔한** 이유" |

**③에 대해 10~12장이 알아야 할 것:** 세 건의 형태가 완전히 같다. **인용·수치·메커니즘은 전부 정확한데, 문장 끝에 붙은 한 단어가 근거 범위 밖으로 나간다.** 특히 두 가지 어휘군을 조심하라.
1. **범주 확장어** — "CDP의", "업계는", "대부분의 제품은". 조사한 것이 벤더 한 곳이면 주어를 그 벤더로 유지하라.
2. **분포·순위 주장어** — "드문", "가장 흔한", "대표적인", "보통은". 이건 집계를 전제하는 말인데 이 책은 어느 축에서도 집계를 하지 않았다. 쓰려면 "**이 책이 조사한 범위에서는**"을 붙이거나 지워라.

**초고를 넘기기 전 자가 점검 한 줄:** 각 절에서 **가장 강한 형용사·부사 하나**를 찾아, 그 단어를 지지하는 문장이 `research/*.md`에 실제로 있는지만 확인하라. 3파의 ⚠️ 5건 중 3건이 이 한 번의 점검으로 걸렸을 것이다.

### B. 10장 — 여전히 가장 위험한 장 (지뢰가 여기 몰려 있다)

3파가 10장 소재를 **전부 건드리지 않고 넘겼다.** 7장 132행("이 구분은 10장에서 법 조문과 만난다"), 9장 29행("이 관문들의 법적 근거는 10장에서 정리한다"), 9장 172행("야간 발송처럼 법이 직접 걸리는 제약은 10장에서 조문과 함께 본다")이 **10장에 세 개의 약속을 걸어뒀다.** 즉 이 장은 조문을 피할 수 없다.

- **조문 번호를 쓸 거면 law.go.kr 원문 확인이 선행돼야 한다.** 9장 172행이 "조문과 함께 본다"고 약속했으므로 회피가 아니라 **확인**이 답이다. 확인 못 하면 약속 문구를 "법이 직접 거는 제약"까지로 낮춰야 하고, 그러면 9장 172행도 함께 고쳐야 한다.
- **PIPA 과징금 %(3% vs 10%)** — 둘 다 원문 미확인. **과징금(제64조의2)과 과태료(제75조)는 다른 제재다. 섞어 쓰면 즉시 ❌.**
- **정보통신망법 2026-07-07 개정 "매출액 6%"** — 원문 미확인. 쓰지 마라.
- **SKAdNetwork 세부**(deprecation 여부·버전·conversion value 비트 수) — 전부 확인 불가. 7장이 all-zero IDFA로 열었기 때문에 10장에서 이 주제로 이어가고 싶은 유혹이 크다. **7장은 IDFA 값의 형식까지만 썼다. 그 선을 넘지 마라.**
- **Ads Data Hub 20/50/10 임계값**을 AMC·Snowflake 등 다른 클린룸에 전용 금지. **7장 112행의 Bloomreach 64 처리를 그대로 복제하라** — "이 값은 X 문서의 값이다. 다른 제품에 옮겨 쓰면 안 된다"를 본문 안에 박는 형태다. 3파에서 가장 잘 작동한 방어 문장이다.
- **EU AI Act·Privacy Sandbox** — "2026년 7월 기준" 명시 필수. `papers.md:1133` Grib et al. (2026) "The Rise and Fall of Google's Privacy Sandbox"는 **초록 미확인이니 제목의 "Fall"로 결론을 추정하지 마라.**
- **삭제 요구는 이미 세 장이 예고했다** — 7장 152행("그래프가 부정확하면 삭제도 부정확해진다"), 7장 195행(삭제 계열 API), 6장 87행(삭제 요청 법적 강제). 10장은 이 셋을 받아야 한다. 단 **7장 195행의 "CDP의 API 표면 절반"은 ⚠️ 판정을 받은 문장이니, 10장이 그 표현을 인용해 재확산시키지 마라.**

### C. 11장 — 범위 한정 3건이 전부 여기 있다 (3파에서 하나도 안 썼다)

**`Gordon`·`Goldfarb`·`Berman`·`Blake` 네 이름 모두 3파 전체에서 0건이다.** 본진이 온전히 보존됐다는 뜻이고, 동시에 **위험도 전부 11장에 남았다는 뜻이다.**

- **Goldfarb & Tucker (2011)** — 종속변수는 **구매 의향**이지 매출이 아니고, 매체는 **온라인 디스플레이 광고**다. "개인화는 역효과다"로 일반화 금지. (`papers.md:1155` — 이 항목은 **`초록 확인`** 등급이라 인용 폭은 넓다. 대신 범위 한정이 그만큼 더 중요하다.)
- **Berman (2018)** — Shapley 개선 효과에 **"시장 전환율이 너무 높지 않을 때"** 조건이 붙는다. 조건을 빼고 인용 금지. 반대로 `papers.md:1094`는 **"라스트터치를 '부정확하지만 실용적'이라고 쓰면 연구 결과와 어긋난다 — 그 강도를 희석하지 마라"**고도 지시한다. **양방향으로 조심할 것.**
- **Blake et al. (2015)** — "온라인 광고는 효과 없다"가 아니다. ①브랜드 키워드 단기 효과 없음 ②비브랜드에서 신규·저빈도 고객에게는 효과 있음 ③지출 배분 때문에 평균 수익률 음수. **"eBay라는 이미 강한 브랜드"라는 맥락 병기 필수.**
- **Gordon 2019에 수치 귀속 금지** — `papers.md:1193`이 이 항목을 "초록 **요약본만** ⚠️"으로 기록했다. 수치가 필요하면 **Gordon, Moakler & Zettelmeyer (2022/2023), arXiv:2201.07055**(`초록 확인` 등급, `papers.md:1194`)를 써라. **두 논문을 한 문장에 섞지 마라.**
- **MMM** — `papers.md:1088`: "MMM 결과를 **점 추정치가 아니라 분포로** 다루라." Meridian(베이지안 계층)과 Robyn(Ridge + Nevergrad)은 **같은 데이터에 다른 답을 낸다.** 단 `papers.md:1134`는 Robyn 방법론이 **웹 검색 기반이고 저장소를 직접 파싱하지 않았다**고 기록했다 — 방법론 세부를 쓸 거면 1차 확인이 선행돼야 한다.
- **9장이 11장에 등급 약속을 걸었다.** 9장 53행이 "**11장에서 만날 어트리뷰션·증분성 연구들 ... 그쪽은 초록과 수치까지 확인한 근거이고**"라고 적었다. 이건 11장에 대한 **사실 주장**이다. 위 목록에서 `초록 확인`은 Goldfarb & Tucker, Berman, Blake(NBER), Gordon 2023 넷이고 **Gordon 2019는 아니다.** 11장이 Gordon 2019를 초록·수치 근거처럼 다루면 9장 53행이 거짓이 된다.

### D. 12장 — 확인해둘 것 두 가지

- **채용 데이터는 이미 두 번 예고됐다.** 9장 119행("이 채용 지형이 커리어 선택에 무엇을 뜻하는지는 12장에서 다시 본다")과 9장 176행("어느 쪽에 앉을 것인가는 12장의 질문이다"). 근거는 `community.md:244~282`(Greenhouse, 조회일 2026-07-25)에 두텁게 있다.
- **채용 수치를 쓸 거면 조회 시점을 문장 안에 넣어라** — 계획서 §B:221. `community.md:249~252`가 **Census / RudderStack / Snowplow / Segment / mParticle은 Greenhouse 404로 조회 실패**라고 기록했으니, "주요 벤더 전부"류의 표현을 쓰면 안 된다. **조회된 4사(Braze·Klaviyo·Twilio·Hightouch)로 주어를 한정하라.** 이게 ③형을 피하는 자리다.
- **국내 채용 수치**는 `02_plan.md` §B:221이 "**2026년 7월 원티드 active 공고 기준**"을 문장 안에 넣으라고 명시했다.

### E. 잘하고 있는 것 — 계속 유지할 4가지

1. **미확인을 부재로 읽지 않게 막는 마지막 문장.** 07:122 "**없다는 뜻이 아니라 확인하지 못했다는 뜻이다**" / 08:145 "못 찾았다는 것이 없다는 증명은 아니지만" / 09:148 "**보긴 했으나 1차 확인에 실패해서 숫자를 적지 않는다**". 3파에서 가장 일관되게 잘 쓰인 장치다.
2. **한 벤더의 수치에 전용 금지를 본문에서 박기.** 07:112(Bloomreach 64)가 정본이다. 10장의 Ads Data Hub 임계값에 그대로 복제하라.
3. **인용 표현의 위상을 낮춰 제시하기.** 08:77이 `"one definition, many runtimes"`를 Pinterest 발언이 아니라 **리서치의 요약 표현**으로 정확히 표시했다. 원본을 확인해보니 실제로 리서처 요약이었다. 영문 표현이 큰따옴표에 싸여 있다고 해서 자동으로 원문 인용은 아니다 — **원본에서 인용 라벨이 붙어 있는지 확인하고 쓰라.**
4. **표본 편향을 자발적으로 고지하기.** 09:89 "그 표본은 영어권 해커뉴스에 크게 치우쳐 있다. 업계 전체의 통계로 읽으면 안 된다." 커뮤니티 증언을 쓰는 10·12장에서 특히 필요하다.

### F. 즉시 처리 — 아직 미이행인 4장의 약속 1건

2파 로그 C절이 지적한 항목이 **3파에서도 이행되지 않았다.** 4장 32행 표가 **Kafka 원 논문의 위상(NetDB'11 워크숍 논문, DOI 없음)을 "5장"에서 다룬다고 예고했는데 5장에 그 서술이 없고, 8장에서도 처리되지 않았다.** 8장이 Lambda·Kappa 출처 성격은 다뤘지만(08:73) Kafka 원 논문 위상은 언급하지 않았다. 근거는 `papers.md:785~791`(C-17-2)에 확보돼 있다.
- **선택지 1:** 5장에 한 문단 추가(2파 로그의 권고안 유지).
- **선택지 2:** 4장 32행 표의 "5장"을 실제로 다룰 장으로 고친다.
- **어느 쪽이든 editor 통합 단계 전에 결정해야 한다.** 지금 상태로 두면 4장이 존재하지 않는 서술을 가리키는 상호참조 오류로 Phase 4.5에서 잡힌다.

---

### 3파 최종 요약

| 장 | ✅ | ⚠️ | ❌ | 🕒 | 차단 여부 |
|---|---|---|---|---|---|
| 07 | 20 | 1 | 0 | 0 | 없음 |
| 08 | 17 | 2 | 0 | 0 | 없음 |
| 09 | 21 | 2 | 0 | 0 | 없음 |
| **계** | **58** | **5** | **0** | **0** | **Phase 5 차단 항목 없음** |

**금지 항목 위반 0건 / 의심 식별자 0건 / `(사실 확인 필요)` 미해소 0건 / 웹 2차 에스컬레이션 0건.**

**저술가 자기 보고의 신뢰도:** 3개 장 모두 자기 보고가 직접 대조에서 사실로 확인됐다. 특히 **8장 저술가의 "`one definition, many runtimes`의 위상을 낮췄다"는 보고**는 원본 3개 출현 위치 전수 확인으로 정확했고, **9장 저술가의 계획서-원본 drift 보고**는 원본 대조 결과 **3중 오차를 정확히 짚은 것**으로 확인됐다(§7-4가 종점 인물·연도·기간을 모두 틀렸다). **9장 저술가가 계획서를 따르지 않고 원본을 따른 판단은 옳았다.**

**최종 확정 전 반영 권고 5건(전부 ⚠️, 문장 단위 교체):** 07 주장 21(CDP → 이 제품) · 08 주장 18("드문" 처리) · 08 주장 19("가장 흔한 이유" 처리) · 09 주장 22("확인 수준" → "확인 범위") · 09 주장 23(선택).

---

## 3파 보유 검증 (검증 종료 전 추가 확인 3건)

> 장별 로그를 쓴 뒤 **산문에 섞여 있어 수치로 안 읽히는 주장**과 **파생 문서(4장 표) 대조가 빠진 상호참조**를 다시 훑었다. 3건 모두 ✅로 해소됐고 판정 수치는 바뀌지 않는다.

**추가 1 — 07:23 ClickHouse 그래뉼 수치 `8192` ✅**
- **본문:** "8192행 그래뉼 단위로만 데이터를 가리키는 인덱스로는 한 사람을 찍어 올 수 없으니까." + "페이지 하나를 200밀리초에 그린다고 하면 프로필 조회에 떼어줄 수 있는 몫은 10~20밀리초 남짓이다."
- **근거:** `web_stack.md:152` ClickHouse 공식 문서 원문 인용 — `"The primary key also does not reference individual rows but blocks of 8192 rows called granules."` + `:155`("MergeTree는 **8192행짜리 그래뉼 단위**로만 가리키니 ... '이 사용자 한 명의 행'을 찍어서 가져오는 건 못한다") + `:951`("페이지 렌더링 예산이 **200ms**라면 프로필 조회에 쓸 수 있는 건 **10~20ms**다 ... MergeTree는 8192행 그래뉼 단위로만 접근하고"). **세 수치(8192 / 200ms / 10~20ms) 모두 원본 일치.**
- **장 간 일관성:** 같은 수치가 **6장 final 46·50·52·188행**에 이미 있고, 6장은 ClickHouse 공식 문서 **원문을 직접 인용**해 근거를 세웠다(46행). 07:23은 그 확립된 사실의 **역참조**이므로 새 주장이 아니다. 값·의미 모두 6장과 일치 — 충돌 없음.
- **판정:** ✅. 제품 기본값이지만 1차 문서(공식 문서 인용)로 확보된 값이고, 계획서 §B의 Tier 2 미조회 목록에 ClickHouse **버전**은 있어도 이 구조 상수는 해당하지 않는다(본문도 버전을 쓰지 않았다).

**추가 2 — 4장 표 행 번호 상호참조 ✅ (파생 문서 대조)**
- 08:121과 09:67은 각각 "근거가 끊긴 열두 건 목록의 **여섯 번째**, 피처 스토어" / "그 **3번 행**이 바로 이 기능이었다(발송 시각 최적화)"라고 **4장 표를 가리킨다.** 장별 로그에서는 `papers.md:1102~1122` 원본으로만 대조했는데, 독자가 실제로 펴보는 것은 **4장이 인쇄한 표**다. §7-4 drift와 같은 실패 유형(원본은 맞는데 파생 문서가 틀림)이 가능한 자리라 재확인했다.
- **근거:** `chapters/04_final.md:25` — `| 3 | Send-time optimization | 벤더 기능 — 최상위 저널 검증 미확인 | 9장 |` / `:28` — `| 6 | Feature store | 산업계 엔지니어링 블로그·벤더 문서 — 학술 정전 논문 부재 | 8장 |`
- **판정:** ✅✅. 행 번호(3·6)와 **예고 장(9장·8장)까지 인쇄된 표와 정확히 일치**한다. 4장이 8·9장에 건 예고를 두 장이 각각 정확한 행 번호로 회수했다. **파생 문서 오차 없음.**

**추가 3 — ③형 판정 기준의 일관성 명시 (07:195와 08:7의 처리가 갈린 이유)**
- 07:195("**CDP의** API 표면 절반")는 ⚠️, 08:7("공개된 프로덕션 사례를 열어보면 실제로 돌아가고 있는 것은 임베딩과 랭킹과 클러스터링이다")는 ✅로 갈랐다. **두 문장의 출처 성격은 같다** — 둘 다 리서처의 편집적 관찰을 옮긴 것이다(`web_products.md:525` / `web_stack.md:1214`, 후자는 원본이 "토스 사례 세 개가 이걸 **증명한다**"고까지 썼다). 기준이 자의적으로 보이지 않도록 갈림의 근거를 남긴다.
- **08:7이 통과한 이유 두 가지:**
  1. **문장 안에 범위 한정어가 있다** — "**공개된 프로덕션 사례를 열어보면**"이 주장의 적용 범위를 공개 사례로 스스로 묶는다. 또 서술어가 "코어가 아니다"(원본)가 아니라 "**인터페이스 층에 가깝다**"로 완화돼 있다. 즉 원본보다 약하게 썼다.
  2. **증거 기반이 같은 장 안에서 공개된다** — 133~141행 표가 무엇이 토스 사례로 확인됐고 무엇이 미확인인지를 7행 전부 나열하고, 143행이 "어느 제품이 실제로 어떤 모델과 어떤 피처를 쓰는지 밝힌 공개 1차 문서에 이 리서치가 도달하지 못했다"고 못박는다. 독자가 7행의 근거 폭을 직접 세어볼 수 있다.
- **07:195가 걸린 이유:** 두 조건이 **모두 없다.** 주어가 "이 제품"에서 "**CDP**"로 넓어지는데 한정어가 없고, 그 확장을 뒷받침하거나 제한하는 서술이 인접 문단 어디에도 없다. 바로 앞 문장이 "**이 제품의**"로 정확히 한정해뒀기 때문에 확장이 더 도드라진다.
- **정리된 기준(10~12장에도 적용):** 리서처의 편집적 관찰을 본문에 옮길 때, **(a) 범위 한정어를 문장 안에 두거나 (b) 근거 폭을 같은 장에서 독자에게 보여주면** 통과. 둘 다 없이 범주 주어(“CDP는/업계는”)나 분포 주장어(“드문/가장 흔한”)만 넘어오면 ⚠️.

**추가 검증으로 인한 판정 변경: 없음.** 3파 최종 집계는 **✅ 61 / ⚠️ 5 / ❌ 0 / 🕒 0**로 갱신한다(장별 ✅ 58 + 추가 확인 3건).

---

# 4파 (10~12장) — 이 책의 마지막 팩트체크

**검증일:** 2026-07-25 / **대조 기준:** `research/*.md` 원본 1차, `01_reference.md`는 §번호 위치잡이용
**규율 문서:** `02_plan.md:185~224`(인용 금지 13항목·서지 함정 2건·범위 한정 3건·시점 병기 §B) + 본 로그 3파 말미 "10~12장 사실 규율 경고"(2028~2103행)

---

## 마커 해소 (10장 정보통신망법)

> **`chapters/10_draft.md:127` 문단 끝 `(사실 확인 필요 — 시행령의 면제 매체 범위)`**
> 리서치가 "martech 구현에 가장 중요한 미결 항목"(`web_privacy.md:738`)으로 남긴 유일한 BLOCKING 마커다. Critical 주장이므로 **웹 2차 에스컬레이션을 수행했다.**

### 판정: ✅ **해소 — 확인됨(단, 확인 등급을 본문에 명기하는 조건부)**

### 무엇을 확인했나

**확인된 조문 (2차 소스가 인용한 형태 — 조·항 번호는 아래 확신도 표 참조):** 정보통신망 이용촉진 및 정보보호 등에 관한 법률 **시행령 제61조(영리목적의 광고성 정보 전송기준) 제2항**

> "법 제50조제3항 단서에서 '대통령령으로 정하는 매체'란 **전자우편**을 말한다."

**앱 푸시의 지위:** 면제 대상이 **아니다.** 앱 푸시 SDK 벤더(핑거푸시)의 개발자 가이드가 자사 App Push 표기의무 항목에서 명시한다 — "야간에 광고성 정보를 보내기 위해서는 **별도의 야간광고전송에 대한 수신동의를 받아야 합니다**." 면제 조항은 전자우편에만 적용된다.

### 확인 경로와 등급 (정직하게 기록한다)

| 시도 | 결과 |
|---|---|
| law.go.kr 시행령 검색 프레임 (`lsSc.do`) | ❌ 검색 폼만 반환 (JS 셸) |
| law.go.kr 법령명 URL (`/법령/…시행령/제61조`) | ❌ 제목만 반환, 조문 본문 없음 |
| lbox.kr 시행령 제61조 | ❌ HTTP 403 |
| 국민건강보험공단 법령 전문 미러 | ❌ 개정 이력만, 조문 본문 없음 |
| WebSearch ×2 (독립 질의) | ✅ 두 질의 모두 "시행령 제61조 = 전자우편"으로 수렴 |
| 발송 벤더 법령 안내(smspop) | ✅ **조문을 항 번호까지 verbatim 인용** — "제61조 ② 법 제50조제3항 단서에서 '대통령령으로 정하는 매체'란 전자우편을 말한다" |
| 앱 푸시 SDK 벤더 가이드(fingerpush) | ✅ 동일 조문 + **앱 푸시는 별도 야간 동의 필요**를 명시 |

**등급:** `조문 문언 확인 — law.go.kr 원문 프레임 미도달, 개정 이력 미확인.` 리서치가 `web_privacy.md:700`에 남긴 "2차 자료: 예외 매체 = 전자우편 (신뢰성 중, 시행령 원문 미확인)"보다 **한 칸 올라갔다** — 문언이 서로 독립적인 4개 소스에서 일치하고, 그중 둘이 조문을 축약 없이 인용한다. 그러나 **1차 원문(법제처) 자체는 이번에도 열지 못했다.**

**두 가지를 분리해서 봐야 한다 — 확신도가 다르다.**

| 요소 | 확신도 | 근거 |
|---|---|---|
| **면제 매체 = 전자우편** | **높음** | 독립 4개 소스 수렴, 그중 2개가 조문 문언을 축약 없이 인용. 리서치의 2차 자료(`:700`)와도 일치 |
| **앱 푸시는 비면제** | **높음** | 앱 푸시 SDK 벤더가 **자기 서비스의 법적 의무로** 명시 — 이해관계가 오히려 신뢰를 높이는 방향(면제라고 말할 유인이 있는데 반대로 말한다) |
| **"제61조 제2항"이라는 조·항 번호** | **중간** | 한 소스만 항 번호까지 인용. 현행 시행령 대조 못 함 |
| **현행성 (2026-07-07 개정법에 대응하는 시행령인가)** | **낮음 — 미확인** | 검색 노출 메타데이터가 `시행 2025-05-20 / 대통령령 제35533호`로 법률보다 앞섬. `web_privacy.md:844`에 시행령 일부개정 뉴스레터가 있고, `:554`는 개정법이 과징금 산정을 시행령에 새로 위임했다고 기록 |

**그래서 조치안은 실질(전자우편·앱 푸시)만 본문에 올리고 조·항 번호와 개정본 특정은 뺐다.** 이 책의 3파 규율(로그 2077행, "확인 수준을 한 칸 올려 말하지 말 것")과 계획서 §B 시점 병기를 함께 만족시키는 형태다.

### 저술가 조치안 (BLOCKING — 반드시 이행)

**`10_draft.md:127`의 마지막 두 문장을 아래로 교체하고, `(사실 확인 필요 — 시행령의 면제 매체 범위)` 마커를 삭제하라.**

**[원문 — 삭제 대상]**
> 그리고 뒤에 단서가 붙어 있다. 대통령령이 정하는 매체는 이 규칙을 따르지 않는데, 어떤 매체가 면제되는지와 앱 푸시가 거기 들어가는지는 이 책이 시행령 원문으로 확인하지 못했다. "밤 9시 이후엔 아무것도 못 보낸다"도, "우리 채널은 예외다"도 지금 여기서 쓸 수 없다. (사실 확인 필요 — 시행령의 면제 매체 범위)

**[교체 — 삽입할 문장]**
> 그리고 뒤에 단서가 붙어 있다. 대통령령이 정하는 매체는 이 규칙을 따르지 않는다. 그 매체가 무엇인지는 시행령이 정하는데, **전자우편**이다. 즉 야간 시간대에 별도 동의 없이 나갈 수 있는 매체는 이메일뿐이고, **앱 푸시는 면제 대상이 아니다.** 다만 확인 등급은 밝혀두자(2026년 7월 25일 조회 기준). 이 책은 법제처 원문 프레임에 끝내 도달하지 못했고, 이 조문은 문언을 그대로 인용한 복수의 2차 소스 — 발송 사업자와 앱 푸시 SDK 벤더가 각자 자기 서비스의 법적 의무를 안내한 문서 — 로 확인했다. 문언이 서로 다른 출처에서 일치하지만, 1차 원문을 봤다고는 쓰지 않겠다. **시행령의 개정 이력도 확인하지 못했다.**

**이 문장을 이렇게 좁힌 이유 3가지 (저술가는 이 제약을 넘지 마라):**

1. **"알림톡"을 넣지 마라 — 9장과 범주가 충돌한다.** 초안 검토 중 한 번 넣었다가 뺐다. 9장 127·131·160행이 알림톡을 "**템플릿 사전 심사를 받는 정보성 채널**"로 정의하고 "**광고성 문구는 허용되지 않으며**"를 인용해 못박았으며, 광고성은 **친구톡**으로 간다고 썼다(9:154~162, `community.md:844~849`). **광고성 정보를 애초에 실을 수 없는 채널을 "광고성 정보 야간 제한의 비면제 매체"로 열거하면 범주 오류이고 9장과 어긋난다.**
2. **"문자"도 빼라 — 직접 근거가 없다.** 확보한 벤더 문서 중 fingerpush는 **앱 푸시**를, smspop은 **문자**를 각각 자기 서비스 기준으로 안내하지만, 조치안이 근거로 삼은 명시적 진술("별도의 야간광고전송에 대한 수신동의를 받아야 합니다")은 **앱 푸시 가이드의 문장**이다. 열거를 늘리면 그만큼 추론이 섞인다. **"전자우편 외에는 면제가 아니다"는 단서 문언 자체에서 따라 나오므로 열거 없이도 설계 결론(채널별 정책 테이블)은 그대로 선다.**
3. **"제61조 제2항"이라는 조·항 번호를 본문에서 뺐다.** 항 번호까지 verbatim으로 인용한 소스가 있지만(smspop), **이 책이 확인한 시행령이 어느 개정본인지 확정하지 못했다.** 근거: ① `web_privacy.md:844`가 「정보통신망법 **시행령 일부개정**: 주요 내용과 시사점」 뉴스레터를 소스 목록에 갖고 있다 ② `web_privacy.md:554`가 2026-07-07 개정법의 과징금을 "**시행령으로 정하는** 매출액의 6% 이하"로 기록해 **시행령에 신규 위임이 생겼음을 시사**한다 ③ 검색 과정에서 노출된 시행령 메타데이터는 `시행 2025-05-20 / 대통령령 제35533호`로 **2026-07-07 법률보다 앞선다.** **면제 매체가 전자우편이라는 실질은 4개 소스에서 견고하지만, 항 번호와 현행성은 그렇지 않다.** 조·항 번호를 본문에 쓰고 싶다면 law.go.kr에서 현행 시행령을 직접 확인한 뒤 대통령령 번호와 시행일을 함께 적어라. **확인 못 하면 위 문장대로 두는 것이 정확하다.**

**이 축소가 무엇을 잃지 않는가:** ① 마커가 사라진다 ② 앱 푸시가 야간 별도 동의 대상이라는 **martech 구현 직결 결론**이 그대로 남는다 ③ 9장 172행의 약속은 **법 제50조 제3항 원문**(`web_privacy.md:532`, law.go.kr 확인 ✅)으로 이미 이행돼 있고 시행령 확인과 무관하다.

**이 교체가 만드는 효과 3가지:**
1. **마커가 사라진다** — Phase 5 차단 해제.
2. **9장 172행의 약속("야간 발송처럼 법이 직접 걸리는 제약은 10장에서 조문과 함께 본다")이 완전히 이행된다.** 3파 로그 2050행이 "회피가 아니라 확인이 답이다"라고 지시한 그 자리다. 9장 172행을 낮출 필요가 없어졌다.
3. **바로 다음 문단(129행)의 설계 결론이 더 강해진다.** "채널마다 규칙이 다를 수 있으니"가 이제 "다를 수 있으니"가 아니라 "실제로 다르니"가 된다 — 저술가 재량이지만 129행 첫 문장의 "확인되지 않은 부분이 남아도 설계 결론은 나온다"는 **"확인하고 나면 설계 결론은 더 분명해진다"**로 고치는 편이 정합한다.

**주의 — 여기서 더 나가지 마라.** 확인된 것은 **면제 매체가 전자우편이라는 사실 하나**다. 시행령 제61조의 나머지 항(예: 제1항의 거래 종료 후 6개월 등)은 이번에 확인 대상이 아니었으므로 본문에 쓰지 마라. 그리고 **정보통신망법 2026-07-07 개정의 "매출액 6%" 과징금은 여전히 원문 미확인 금지 항목이다** — 이번 확인이 그 항목까지 풀어준 것이 아니다.

**출처:**
- 정보통신망법 시행령 — smspop.co.kr 「야간광고 전송제한 안내」 (조문을 "제61조 ② 법 제50조제3항 단서에서 '대통령령으로 정하는 매체'란 전자우편을 말한다"로 verbatim 인용, 2026-07-25 조회. **개정본 특정 불가**)
- developers.fingerpush.com 「광고성 정보 전송 가이드라인 — APP PUSH」 (앱 푸시 야간 별도 동의 의무 명시, 2026-07-25 조회)
- 대조 기준: `research/web_privacy.md:532`(법 제50조 제3항 단서 원문 ✅), `:548`·`:700`·`:738`(시행령 미확인 기록)

---

## 10장 — 1차 검증

> 3파 로그가 "여전히 가장 위험한 장 — 지뢰가 여기 몰려 있다"(2046행)고 지목한 장이다. 법령 금지 항목 6종, 브라우저 정책 날짜 축, 범위 한정 인용 1건, 그리고 유일한 BLOCKING 마커가 전부 이 장에 있었다.
>
> **결과: 주장 37건 — ❌ 0 / 🕒 0 / ⚠️ 1 / ✅ 36. 금지 항목 위반 0건. 마커 1건 해소(위 섹션).**

### ❌ 정정 필요 — **0건**

### 🕒 검증 불가 — **0건**

### ⚠️ 근거 약함 / 보강 권고 — 1건

**주장 24 — Ads Data Hub 임계값에 "다른 제품에 전용 금지" 방어 문장이 없다 (10:187)**
- **본문:** "Ads Data Hub 문서는 노이즈 주입에 결과 행당 약 20명, difference check에 약 50명, 클릭·전환 데이터만 조회할 때 약 10명의 고유 사용자가 필요하다고 적는다(조회 시점 2026년 7월 25일)."
- **수치 자체는 ✅ 완전 일치** — `web_privacy.md:366` 원문 인용: `"Noise injection requires approximately 20 unique users per result row. Difference checks require approximately 50 unique users per result row. Queries of only click and conversion data require approximately 10 unique users per result row."` 출처 귀속(Ads Data Hub 문서)도 정확하고, 조회 시점도 문장 안에 있다. **AMC·Snowflake로 전용한 흔적 0건** — 바로 다음 문단의 AWS Clean Rooms 서술에는 숫자가 하나도 없다(통제 수단 이름만 나열). **금지 항목 위반 아님.**
- **그런데 3파 로그 2054행이 명시적으로 지시한 것이 빠졌다:** "**7장 112행의 Bloomreach 64 처리를 그대로 복제하라** — '이 값은 X 문서의 값이다. 다른 제품에 옮겨 쓰면 안 된다'를 본문 안에 박는 형태다. 3파에서 가장 잘 작동한 방어 문장이다." 현재 초안은 출처를 밝히기만 하고, **독자가 이 숫자를 다른 클린룸으로 옮기는 것을 막는 문장이 없다.**
- **왜 이 장에서 특히 필요한가:** 바로 앞 문장이 "임계값을 수치로 공개한 곳은 많지 않다"이다. 이 문장은 독자에게 "그럼 공개 안 한 곳도 비슷하겠지"라는 추론을 열어준다. 방어 문장이 없으면 이 장이 스스로 오용의 다리를 놓는 셈이다.
- **보강안 (한 문장 삽입, 187행 첫 문장 뒤):**
  > "이 세 숫자는 **Ads Data Hub 문서의 값**이다. 다른 클린룸의 임계값은 이 책이 확인하지 못했으니, 이 값을 AMC나 Snowflake 쪽으로 옮겨 쓰면 안 된다."
- **근거:** `web_privacy.md:366`(수치 원문) / `:730`(Snowflake 집계 임계값 미확인) / `02_plan.md:193`(금지 항목 5) / 본 로그 2054·2078행 / `chapters/07_final.md:112`(정본 패턴)

### ✅ 확인됨 — 36건

**A. 법령 축 (10건) — 금지 항목이 가장 조밀한 구역, 전건 통과**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 1 | 개인정보 보호법 "2025년 10월 2일 시행, 법률 제20897호" | `web_privacy.md:779` (시행 2025-10-02, 법률 제20897호, 2025-04-01 일부개정) | ✅ |
| 2 | 제30조 제1항 7호 "인터넷 접속정보파일 등 자동수집 장치에 관한 사항" | `web_privacy.md:430~441` law.go.kr 원문 인용, 7호 문언 정확 | ✅ |
| 3 | 시행령 제31조 제1항 — 국외 이전 근거 + 국외 직접 수집 시 처리 국가명 | `web_privacy.md:475~478` 원문 인용 2호·4호 | ✅ |
| 4 | 시행령 제17조 동의 4조건 (법률 제17조와 구분 명시) | `web_privacy.md:454~462` 원문 인용 4개 호 전부 일치. **"법률 제17조와 헷갈리기 쉬우니 조심하자"는 `:456`의 경고를 독자에게 그대로 전달한 것** | ✅✅ |
| 5 | 제75조 제2항 인용 "제16조제3항ㆍ제22조제5항을 위반하여 재화 또는 서비스의 제공을 거부한 자" | `web_privacy.md:470` 원문 인용 verbatim 일치 | ✅ |
| 6 | **"과징금은 과태료와 별개의 제재인데, 상한 비율은 자료마다 숫자가 달라 원문을 확인하기 전까지 적지 않는다"** | `web_privacy.md:498`·`:678~681`·`02_plan.md:194` | ✅✅✅ |
| 7 | 제37조의2 제4항 자동화된 결정 공개 의무 + GDPR 제22조 대응 | `web_privacy.md:449`(제4항 원문 인용) / `:585~590`(GDPR Art.22 + 대응 관계 명시) | ✅ |
| 8 | "(시행일은 부칙을 확인하지 못해 적지 않는다)" | `web_privacy.md:451`·`:736` — 시행일 부칙 미확인 기록과 정확히 일치 | ✅✅ |
| 9 | 정보통신망법 "2026년 7월 7일 시행, 법률 제21305호" / 제50조 제1항 명시적 사전 동의 / 제3항 원문 인용 | `web_privacy.md:785`·`:526~532` 원문 인용 verbatim | ✅ |
| 10 | 제50조 제8항 정기적 수신동의 재확인 → `verified_at` | `web_privacy.md:652` 원문 인용 | ✅ |

**주장 6이 이 장에서 가장 중요한 통과다.** 계획서 §A-6이 "3% vs 10% 상충, 둘 다 원문 미확인. **과징금(제64조의2)과 과태료(제75조)는 다른 제재다 — 섞어 쓰지 마라**"라고 이중 금지를 걸었는데, 저술가는 **① 숫자를 하나도 쓰지 않았고 ② 두 제재가 별개임을 독자에게 명시했으며 ③ 왜 안 쓰는지까지 밝혔다.** 금지를 회피가 아니라 서술로 전환한 형태다. 이 책이 3파에서 확립한 "미확인을 부재로 읽지 않게 막는 마지막 문장"(로그 2077행) 패턴의 법령 버전이다.

**B. 브라우저·플랫폼 정책 축 (9건) — "기억으로 쓰면 거의 틀린다"고 지목된 축, 전건 원본 일치**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 11 | 2025-04-22 Chavez 글 + 인용 `"made the decision to maintain our current approach to offering users third-party cookie choice in Chrome"` | `web_privacy.md:50`(발행일·저자)·`:54`(원문 인용) verbatim | ✅ |
| 12 | 2025-10-17 은퇴 발표 + 인용 `"After evaluating ecosystem feedback about their expected value and in light of their low levels of adoption, we've decided to retire the following Privacy Sandbox technologies."` | `web_privacy.md:60`·`:63` verbatim | ✅ |
| 13 | **"은퇴 목록에는 … 열한 개가 열거됐다"** | `web_privacy.md:65` 원문 열거 실수 — Attribution Reporting API, IP Protection, On-Device Personalization, Private Aggregation, Shared Storage, Protected Audience, Protected App Signals, Related Website Sets, SelectURL, SDK Runtime, Topics = **정확히 11개** | ✅✅ |
| 14 | "CHIPS, FedCM, Private State Tokens는 계속 지원" | `web_privacy.md:66` 3개 정확 일치 | ✅ |
| 15 | IP Protection — 4월 3분기 런칭 예고 → 10월 상태 페이지 출시 안 함. "반년 만의 번복" | `web_privacy.md:56`·`:78`·`:689~691` (원본 표현 "6개월 만의 번복") | ✅ |
| 16 | Safari 2020년 3월 크로스사이트 쿠키 기본 차단 | `web_privacy.md:113`(2020-03-24, Wilander) | ✅ |
| 17 | **Firefox "2022년 6월부터 데스크톱 기본값으로"** | `web_privacy.md:138`·`:761`(2022-06-14). `:139`가 "**챕터에서 쓸 때 플랫폼을 한정하라**"고 경고했는데 **저술가가 '데스크톱'을 문장 안에 넣었다.** 버전 번호는 쓰지 않았다(미확인 항목) | ✅✅ |
| 18 | ITP 7일 인용 `"…deleting all of a website's script-writable storage after seven days of Safari use without user interaction on the site."` + 삭제 대상 목록 | `web_privacy.md:117`(verbatim)·`:118`(IndexedDB, LocalStorage, Media keys, SessionStorage, Service Worker registrations and cache) | ✅ |
| 19 | 2020년 11월 12일 CNAME 클로킹 탐지 + 쿠키 만료 7일 캡 | `web_privacy.md:123`(2020-11-12)·`:126` 원문 `"caps the expiry of any cookies set in the HTTP response to 7 days"` | ✅ |

**주장 13이 4파에서 가장 검증 가치가 높았던 수치다.** "열한 개"는 기억으로 쓰면 틀리기 쉬운 개수인데 원본 열거와 정확히 일치했다. 그리고 저술가가 **본문에 나열한 4개(Topics, Protected Audience, Attribution Reporting, IP Protection)가 전부 원본 목록 안에 있다** — "등"으로 얼버무린 뒤 목록 밖 항목을 섞는 흔한 실패가 없다.

**C. 수집·동의 축 (8건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 20 | ATT tracking 정의 원문 인용 + "발행일 표기가 없는 정책 페이지다. 2026년 7월 25일 조회 기준" | `web_privacy.md:147` verbatim. 조회일 병기 형식은 §B 요구 충족 | ✅ |
| 21 | GTM 서버사이드 `client` 정의 원문 인용 + "날짜 표기가 없는 문서다(2026년 7월 25일에 열어봤다)" | `web_privacy.md:194` verbatim | ✅ |
| 22 | Meta CAPI 48시간 창 원문 인용 + `eventID`/`event_id`, `event`/`event_name` 매칭 규칙 | `web_privacy.md:216`·`:221` verbatim | ✅ |
| 23 | Segment 수집 가이드 — 결제·민감정보는 서버 / UTM·디바이스·재방문자 쿠키는 클라이언트 / 일부 목적지는 브라우저 발신만 수신 | `web_gaps.md:628~634` 세 항목 전부 원문 대응 | ✅ |
| 25 | TCF v2.3이 현재 버전 + 인용 `"Starting 1st March, 2026: Any TC String created without the disclosedVendor segment will be deemed invalid."` + 전환 안내 문서 2025-06-19 | `web_privacy.md:244`(발행일)·`:245`·`:248` verbatim | ✅ |
| 26 | v2.2 — 개인화 광고·콘텐츠 프로필 목적에서 정당한 이익 제거, 동의만 허용 / GDPR 제6조 제1항 6가지 근거 / (a)와 (f)의 다툼 | `web_privacy.md:252`(Purpose 3·4·5·6에서 LI 제거)·`:565~578`(Art.6(1) 6개 표)·`:579` | ✅ |
| 27 | Consent Mode 파라미터 **일곱 개** (광고 저장소·광고용 사용자 데이터·광고 개인화·분석·기능·개인화·보안) + 기본/고급 모드 트레이드오프(일반 모델 vs 광고주별 모델) | `web_privacy.md:260~270` 7개 표 정확 일치 + `:272~273` Basic/Advanced 원문 인용. **`:258`이 경고한 "Consent Mode v2" 라벨을 쓰지 않았다** | ✅✅ |
| 28 | GPC — W3C Working Draft 2026-06-11 / `Sec-GPC: 1` / `navigator.globalPrivacyControl` / 캘리포니아 법무장관실의 존중 의무 + "발행일 표기가 없어 조회일만 남긴다" | `web_privacy.md:771`(2026-06-11 WD)·`:282`·`:288`·`:610`(`"it must be honored"`)·`:606`(발행일 표기 없음) | ✅ |

**D. 클린룸·학술 축 (3건) — §3-K(C-20) 처리**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 29 | "이 리서치는 클린룸 벤더 문서에서 PSI나 k-익명성이라는 용어를 확인하지 못했다" + Sweeney(2002)·Pinkas, Schneider & Zohner(2018)·Dwork, McSherry, Nissim & Smith(2006) **계보만** | `web_privacy.md:403~406`("어느 벤더 공식 문서에서도 확인하지 못했다", "**학술 개념으로 소개하는 건 가능하나 특정 벤더 제품이 그걸 쓴다고 쓰지 마라**") + `papers.md:913`·`:937`·`:904` 서지 3건 전부 정확 | ✅✅✅ |
| 30 | AWS Clean Rooms 통제 수단 — 분석 규칙, 암호화 상태 연산, 분석 로그, 차등 프라이버시, ID 네임스페이스 (숫자 0개) | `web_privacy.md:345~353` 원문 인용 대응 | ✅ |
| 31 | Ads Data Hub — 값이 0이거나 null인 사용자 ID 이벤트는 임계값 계산에 미포함 | `web_privacy.md:369` 원문 `"events with zeroed or null user IDs don't count toward the aggregation threshold"` | ✅ |

**주장 29는 계획서가 §3-K에 건 제약을 완벽히 지켰다.** 세 논문 모두 `papers.md`에서 **`메타데이터` 등급**(:1230·:1231·:1234)인데, 저술가는 **수치도 정리(theorem) 내용도 하나도 옮기지 않고 "누가 언제 낸 계보"까지만 썼다.** 게다가 벤더 문서에 그 용어가 없다는 **negative finding을 먼저 밝힌 뒤** 학술 개념을 소개하는 순서를 택했다 — 독자가 "그럼 제품이 그걸 쓰는구나"로 읽을 여지를 앞에서 닫았다.

**E. 범위 한정 인용 (1건) — 계획서 §범위 한정 3건 중 1건이 이 장에 있다**

**주장 32 — Goldfarb & Tucker (2011) ✅✅ (범위 한정 정위치)**
- **본문 197~201행:** 서지 "*Marketing Science* 30(3), 389–404" → 초록 원문 인용 → **바로 다음 문단 첫머리에** "범위는 정확히 지키자. 이 연구의 종속변수는 **구매 의향**이지 실제 매출이 아니고, 매체는 **온라인 디스플레이 광고**다. **'개인화는 역효과다'로 넓히면 논문이 말하지 않은 것을 말하게 된다.**"
- **근거:** `papers.md:148`(서지 — 권·호·페이지 전부 일치) / `:153`(초록 원문 — **verbatim 일치**) / `:154`(범위 한정 문언 — 계획서 §213과 동일) / 등급 `초록 확인`(`:1155`)이라 직접 인용 허용 범위 안
- **판정 근거 3가지:**
  1. **범위 한정이 인용 직후 문단에 있다.** 3파 로그 2036행이 "고지를 절 단위로 잡기"를 ①형 실패로 지목했는데, 이 배치는 인용과 한정 사이에 다른 주장이 끼지 않는다. 저술가 자기 보고("인용 직후에 배치했다")가 **직접 대조에서 사실로 확인됐다.**
  2. **일반화 금지가 부정문으로 명시돼 있다.** "'개인화는 역효과다'로 넓히면"이라는 금지 대상 문장을 **본문이 직접 인쇄한 뒤 기각한다.** 독자가 이 논문을 인용할 때 저지를 오류를 미리 이름 붙여둔 형태다.
  3. **절 제목이 논문보다 넓게 나가지 않는다.** 절 제목이 "개인화는 세게 할수록 좋아지지 않는다"인데, 이는 논문의 "결합하면 각각보다 못하다"와 방향이 같고 "역효과"보다 약하다.
- **`10.1287/mksc.1100.0583` DOI를 본문에 쓰지 않은 것도 무해하다** — 권·호·페이지로 특정되고, 서지가 원본과 일치한다.

**F. 서지 함정 처리 (1건)**

**주장 33 — Tucker (2013/2014) ✅ (상충을 본문에 노출)**
- **본문 205행:** "Tucker의 'Social Networks, Personalized Advertising, and Privacy Controls'(DOI `10.1509/jmr.10.0355`, **서지에 권과 연도가 상충해 2013/2014로 적는다**)"
- **근거:** `papers.md:1131`("서지 상충 — Crossref에 Vol.50(2013)과 Vol.51(2013) 두 레코드. **DOI `10.1509/jmr.10.0355` 사용, 권/연도는 출판사 페이지 재확인 필요**") / `:170~173` / `:1157`(⚠️상충 표시)
- **판정:** 원본이 지시한 처리와 **정확히 일치한다** — ① DOI로 지목 ② 권·연도를 단정하지 않음 ③ 상충 사실을 독자에게 공개. 리서치가 "fact-checker가 출판사 페이지로 재확인할 것"이라 했으나, **본문이 권·연도 주장을 아예 하지 않으므로 재확인 없이도 오류가 성립할 수 없다.** 확인 부담을 주장 제거로 해소한 정확한 판단이다.
- 인접 2건도 등급대로다 — White et al. (2007/2008)·Awad & Krishnan (2006) 모두 `메타데이터` 등급(`papers.md:1156`·`:1158`)인데 본문이 "**둘 다 서지까지만 확인해 이름만 적어둔다**"고 명시했다.

**G. 커뮤니티 인용 (2건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 34 | jacksnipe 인용 + "HN 32158458 (2022-07-19)" + "**법률 비전문가의 진술이다**" | `community.md:629`(ID·작성자·날짜 일치)·`:1196` | ✅ |
| 35 | 크립토 셰레딩 + "이 방식을 소개한 사람 본인이 일반적인 회사에는 당분간 현실성이 없다고 덧붙였다(HN 30684445 / tybit / 2022-03-15). **관행 소개이지 권고가 아니다**" | `community.md:624~626` — 원본의 "발언자 본인이 '일반 회사엔 당분간 현실성 없다'고 덧붙였다"까지 그대로 전달 | ✅✅ |
| 36 | scrollaway 수집/처리 구분 (HN 18989137 / 2019-01-24) + "**역시 비전문가의 법 해석이지만**" | `community.md:641`·`:1198`(2019-01-24) | ✅ |

**H. 저술가가 마커 없이 선제 해소한 항목 (1건) — 특기 사항**

**주장 37 — Meta CAPI 탄생 배경 ✅✅ (두 번째 마커 후보를 negative finding으로 전환)**
- **본문 81행:** "(CAPI가 광고 차단기 때문에 만들어졌다는 설명이 널리 도는데, **Meta 공식 문서에서 그 문장을 찾지는 못했다. 통설로 알아두자.**)"
- **근거:** `web_privacy.md:209` — "⚠️ **정직한 표기:** 이 공식 문서 페이지에는 '광고 차단기 때문에 만들었다'는 문장이 **없다**. 브라우저 제약을 CAPI의 존재 이유로 쓸 때는 Meta 공식 진술이 아니라 업계 통설로 표기하라. **(`(사실 확인 필요)` 마커 대상)**"
- **판정:** 리서치가 **명시적으로 마커를 붙이라고 지목한 두 번째 지점**인데, 저술가가 마커 대신 **본문 문장으로 해소했다.** 형태도 정확하다 — 통설의 존재를 인정하고, 공식 확인 실패를 밝히고, 등급("통설")을 라벨로 부여한다. **결과적으로 이 장의 마커는 1건만 남았고, 그것도 위에서 해소됐다.**
- **부수 확인:** 같은 리서치 문단(`:225`)에 "브라우저 쪽이 **30~40%** 잘려나가기 때문"이라는 수치가 있는데, **저술가가 이 숫자를 쓰지 않았다.** 그 수치는 리서처 서사 블록 안에 있고 1차 출처 귀속이 없다. 쓰지 않은 판단이 옳다.

### 계획서 §B 시점 병기 점검 (10장 해당분)

| 요구 | 이행 |
|---|---|
| Privacy Sandbox "2026년 7월 기준" 명시 | ✅ 13행 "**2026년 7월 기준으로** 두 문장 다 성립하지 않는다" — 절 첫머리에 배치 |
| TCF 현재 버전 시점 | ✅ 87행 "**2026년 7월 기준** 현재 버전은 v2.3" |
| 날짜 없는 벤더 문서 4건(ATT·GTM·Meta·Consent Mode·CA AG) | ✅ 전부 "2026년 7월 25일 조회/확인" 병기 |
| **EU AI Act** | ✅ **의도적 미사용 — 저술가 보고가 사실로 확인됐다.** `grep -c "AI Act" 10_draft.md` = 0. `web_privacy.md:640~648`이 이 항목에 "페이지 최종 갱신일 없음 / AI Omnibus 반영 여부 확인 못 함 / Article 5 원문 미조회 / 일반적 광고 개인화가 걸린다는 근거 확인 불가"로 **네 겹의 경고**를 달았다. 쓰지 않은 것이 이 장에서 가장 안전한 선택이다 |

### 금지 항목 스캔 (10장)

| 금지 항목 | 결과 |
|---|---|
| PIPA 과징금 % (3% / 10%) | **0건** ✅ (주장 6에서 부재 사유까지 서술) |
| 과징금(제64조의2)과 과태료(제75조) 혼동 | **0건** ✅ (본문이 둘을 명시적으로 분리) |
| 정보통신망법 "매출액 6%" | **0건** ✅ (`grep` 확인 — "매출액"·"6%" 모두 0) |
| SKAdNetwork 세부 | **0건** ✅ (문자열 자체가 0회. 7장 all-zero IDFA에서 이어가려는 유혹을 넘지 않았다 — 로그 2053행 준수) |
| Ads Data Hub 20/50/10 타 클린룸 전용 | **0건** ✅ (수치는 ADH에만, AWS는 숫자 없음) |
| PSI·k-익명성을 벤더 제품에 귀속 | **0건** ✅ (negative finding 선행) |
| Goldfarb & Tucker 범위 한정 누락 | **0건** ✅ (인용 직후 배치) |
| Theta Sketch·C-Store·CDP 4분류·CEM/CXM·DMARC·Snowplow 라이선스·Tier 2 버전 | **0건** ✅ (이 장의 소재 아님, 문자열 전무) |

### 3파 경고 ③형(근거 밖 수식어) 재발 점검 — **0건**

3파에서 유일하게 재발한 유형이라 절별 최강 형용사를 전수 점검했다. 확인된 것은 오히려 **반대 방향**이다 — 저술가가 원본보다 **약하게** 쓴 자리가 4곳이다.

| 원본 | 10장 본문 | 방향 |
|---|---|---|
| `web_privacy.md:120` "이게 '왜 우리 재방문 식별률이 계속 떨어지나'의 **기술적 정답이다**" | 47행 "그 **상당 부분이** 여기서 설명된다" | 하향 ✅ |
| `web_privacy.md:356` 제목 "**유일하게** 구체 임계값이 공개된 소스" | 185행 "임계값을 수치로 공개한 곳은 **많지 않다**" | 하향 ✅ |
| `web_privacy.md:600` "`sec-gpc` 한 줄이 법적 의미를 갖는 **첫 헤더다**" | 103행 "**아마** … **최초의 한 줄일 것이다**" | 하향 ✅ |
| `web_privacy.md:139` "Firefox는 기본으로 파티셔닝한다(플랫폼 한정하라)" | 35행 "**데스크톱 기본값으로**" | 범위 축소 ✅ |

**범주 확장어("CDP의"·"업계는"·"대부분의 제품은") 0건 / 분포·순위 주장어("드문"·"가장 흔한"·"대표적인") 0건.** 표 하나가 저자 도출임을 스스로 밝힌 자리(153행 "이 표는 법령과 벤더 문서에서 **이 책이 도출한 정리이지 공식 목록은 아니다**")도 있다.

### 10장 총평

**이 책에서 사실 위험이 가장 높았던 장이 ❌ 0건으로 통과했다.** 법령 6종 금지 항목을 전부 피했을 뿐 아니라, 그중 가장 위험한 PIPA 과징금 항목은 **"왜 안 쓰는지"까지 본문에 남겨 독자가 다른 자료의 수치를 만났을 때 경계하게 만들었다.** 브라우저 정책 축의 날짜·개수(2025-04-22 / 2025-10-17 / 11개 / 3개 / 7일 / 48시간 / 20·50·10)는 **전부 원본과 자릿수까지 일치**했다. 유일한 미결이던 시행령 마커도 웹 2차 검증으로 해소됐고, 그 결과 9장 172행이 건 약속까지 완전히 이행된다.

**보강 권고 1건(주장 24, Ads Data Hub 전용 금지 문장)은 사실 오류가 아니라 방어 장치 누락이다.** 문장 하나 삽입으로 끝나며 Phase 5를 차단하지 않는다. 다만 3파 로그가 "가장 잘 작동한 방어 문장"이라 지목해 명시적으로 복제를 지시한 항목이므로 반영을 권한다.

---

## 11장 — 1차 검증

> 3파 로그 2058행이 "**범위 한정 3건이 전부 여기 있다 — `Gordon`·`Goldfarb`·`Berman`·`Blake` 네 이름 모두 3파 전체에서 0건**"이라고 지목한 장이다. 위험이 온전히 보존된 채 이 장으로 넘어왔고, 여기에 **9장이 이 장의 근거 등급에 대해 미리 사실 주장을 걸어둔 것**(로그 2067행)까지 겹쳐 있었다.
>
> **결과: ❌ 0 / 🕒 0 / ⚠️ 2 / ✅ 26. 금지 항목 위반 0건.**

### ❌ 정정 필요 — **0건**

### 🕒 검증 불가 — **0건**

### ⚠️ 근거 약함 — 2건

**주장 A — "거의 모든 도구의 기본값 자리에 앉아 있다" (11:25) / "가장 널리 쓰인다" (11:39)**
- **본문 25행:** "가장 널리 쓰이는 배분 규칙은 라스트터치다. … 구현이 단순하고 설명하기 쉬워서 **거의 모든 도구의 기본값 자리에 앉아 있다.**"
- **본문 39행:** "**기술적으로 가장 편한 규칙이 가장 널리 쓰인다**는 이야기인데"
- **원본이 지지하는 범위:** `papers.md:1093` — "실무에서 라스트터치는 **여전히 기본값이다.** 계산이 싸고, 설명이 쉽고, 채널 팀 간 정치적 분쟁이 적기 때문이다." / `papers.md:420` Berman 초록 원문 — `"a common attribution method known as last-touch"`.
- **어긋나는 지점:** 원본은 **"기본값이다"**(상태 서술)와 **"common"**(빈도 형용사)까지다. 본문의 **"거의 모든 도구의"**는 **제품 전수를 전제하는 분포 주장**이고, 이 책은 어트리뷰션 제품의 기본값 설정을 어느 축에서도 집계하지 않았다. 3파 로그 2042행이 "**분포·순위 주장어** — '드문', '가장 흔한', '대표적인', '보통은'. 이건 집계를 전제하는 말인데 이 책은 어느 축에서도 집계를 하지 않았다"고 지목한 바로 그 어휘군이다. **③형 재발 1건.**
- **정정안 (둘 중 하나):**
  - (a) "구현이 단순하고 설명하기 쉬워서 **오랫동안 기본값 자리를 지켜왔다.**" — 원본의 "여전히 기본값이다"에 정확히 대응
  - (b) "…해서 거의 모든 도구의 기본값 자리에 앉아 있다"를 유지하려면 **Berman 초록의 `common`을 근거로 노출**하라 — "Berman의 초록도 이 방식을 '흔한(common) 어트리뷰션 방법'이라 부른다."
- **39행 부수 지적:** 세 번째 이유를 원본의 "**채널 팀 간 정치적 분쟁이 적다**"에서 "**채널 간 데이터 교환이 필요 없다**"로 바꿔 썼다. 기술적으로 타당한 설명이지만 **원본에 없는 저자 추론**이다. 유지하려면 "이건 이 책의 해석인데"를 붙이거나, 원본 이유(정치적 분쟁)를 함께 놓아라. 그리고 같은 문장의 "**가장 널리 쓰인다**"도 (a)와 같은 방식으로 낮추는 편이 일관된다.
- **주의:** 이 정정은 **라스트터치에 대한 Berman의 판정 강도를 건드리지 않는다.** `papers.md:1094`가 "그 강도를 희석하지 마라"고 못박은 것은 **연구 결과**(안 쓰느니만 못하다)이지 **보급률 서술**이 아니다. 33행의 강도는 그대로 두어야 한다 — 아래 주장 3 참조.

**주장 B — 9장 55행(초안 53행)이 11장에 건 등급 약속이 11장 본문과 부분적으로 어긋난다 (장 간 정합)**

→ 별도 섹션 「9장 ↔ 11장 Gordon 등급 정합 판정」에서 다룬다. **11장이 아니라 9장을 고치는 항목이고, ⚠️ 등급이며 Phase 5를 차단하지 않는다.**

### ✅ 확인됨 — 26건

**A. Gordon 계열 — 이 장의 최대 위험 지대, 전건 통과 (7건)**

**주장 1 — 모든 증분성 수치가 2023 논문 귀속인가 ✅✅✅ (직접 grep 수행)**

| 수치 | 본문 위치 | `papers.md` 원본 | 일치 |
|---|---|---|---|
| 대규모 실험 **663건** | 51행, 69행, 160행 | `:521` "Facebook의 **대규모 실험 663건**을 분석했다" | ✅ |
| **5,000개 이상**의 사용자 수준 피처 | 51행, 69행, 160행 | `:522` "**5,000개 이상의 사용자 수준 피처**에 접근했다 — 대부분의 광고주나 측정 파트너가 접근할 수 있는 것보다 훨씬 풍부한 데이터다" (본문 51행이 이 단서까지 옮겼다) | ✅ |
| RCT 중앙값 **29 / 18 / 5** | 53~57행 표 | `:524` | ✅ |
| DML 중앙값 **83 / 58 / 24** | 53~57행 표 | `:525` | ✅ |
| SPSM 중앙값 **173 / 176 / 64** | 53~57행 표 | `:526` | ✅ |

**초록 원문 대조(`papers.md:529`):** `"The median RCT lifts are 29%, 18%, and 5% for the upper, middle, and lower funnel outcomes, respectively. Using DML (SPSM), the median lift by funnel is 83% (173%), 58% (176%), and 24% (64%), respectively…"` — **아홉 개 숫자가 퍼널 단계별 배치까지 정확히 일치한다.** 표의 행·열 배치도 초록의 대응 관계를 뒤집지 않았다.

**귀속 검증:** `grep -c "2019" chapters/11_draft.md` = **0**. 저술가 자기 보고("문서 내 2019 0회")가 **직접 grep으로 사실 확인됐다.** 서지는 59행에 한 번, 인용 출처는 67행에 한 번, 둘 다 **"(2023)"과 `arXiv:2201.07055`를 함께** 달았다. **`papers.md:1194`의 `초록 확인` 등급 안에서만 움직인다.**

**주장 2 — "다섯 배에서 열세 배" ✅✅ (원본보다 보수적)**
- **본문 61행:** "5와 24, 5와 64를 나눠보면 대략 다섯 배에서 열세 배다. **이 배수 계산은 논문 초록에 그대로 실린 문장이 아니고 위 표의 값을 이 책이 나눈 결과지만, 나눗셈에 해석의 여지는 없다.**"
- **판정:** 저술가 자기 보고가 사실이고, **원본보다 한 칸 낮춰 썼다.** `papers.md:531`은 이 배수를 리서치 자신의 결론으로 단정한다("즉 **5배에서 13배 과대추정**이다"). 초록 원문(`:529`)에는 배수가 없다. 저술가는 원본이 단정한 것을 **책의 계산으로 강등하고 그 사실을 명시**했다. 3파 로그 2037행이 칭찬한 "확인 수준을 한 칸 **내려** 말하기" 패턴의 재현이다.
- **부수:** 서지 `*Marketing Science* 42(4), 768–793, 2023` / DOI `10.1287/mksc.2022.1413` — `papers.md:517`과 권·호·페이지·연도·DOI 전부 일치. 저자 3인 순서(Gordon, Moakler, Zettelmeyer)도 일치.

**주장 3 — 결론 인용 + 오독 차단 ✅**
- 65행 인용("대규모 실험과 풍부한 사용자 수준 데이터에 접근할 수 있었음에도 우리는 광고 캠페인의 인과 효과를 신뢰성 있게 추정할 수 없었다")은 초록 마지막 대목의 번역이며 `:517~531` 서술과 방향이 일치한다.
- 73행이 **"이 결과는 광고 플랫폼이 숫자를 부풀린다는 고발이 아니다"**라고 오독을 선제 차단한다. 연구 수행 주체(Facebook 데이터 접근)와 평가 대상(관측 기반 인과 추정 방법론)을 구분해준다. 원본 `:531`의 취지("개발자의 직관을 반박한다")와 어긋나지 않으며, 오히려 벤더 비난으로 오용될 여지를 닫았다.

**B. 범위 한정 인용 3건 중 2건 (계획서 §212~215) — 전건 통과**

**주장 4 — Berman (2018) ✅✅✅ (양방향 한정 모두 이행)**

계획서와 3파 로그가 이 인용에 **서로 반대 방향의 두 요구**를 걸었다. 둘 다 지켜졌다.

| 요구 | 이행 위치 | 판정 |
|---|---|---|
| **조건절 필수** — "시장 전환율이 너무 높지 않을 때"를 빼고 인용 금지 (`papers.md:424`, 계획서 §214) | 29행 인용문 **안에** 이미 포함 + 35행에서 **다시 명시** ("**'시장의 전환율이 너무 높지 않을 때'라는 조건**이 붙어 있다. 이 조건을 떼고 '<span>Shapley를 쓰면 개선된다</span>'로 옮기면 논문이 하지 않은 말이 된다") | ✅✅ |
| **강도를 희석하지 마라** — 라스트터치를 "부정확하지만 실용적"으로 쓰면 연구 결과와 어긋난다 (`papers.md:1094`, 로그 2063행) | 33행 — "**'라스트터치는 부정확하다'와 '라스트터치를 쓰면 안 쓰느니만 못하다'는 다른 층위의 주장이다.** 뒤쪽은 이 규칙이 오차를 남기는 데서 그치지 않고, 그 오차가 입찰 행동을 왜곡해 광고주 자신의 이익을 깎는다고 말한다" + **절 제목이 "라스트터치는 안 쓰느니만 못하다"** | ✅✅ |
| 이론 모델 단서 | 35행 "이 논문은 **이론 모델과 분석적 결과**를 제시한다. 대규모 관측 데이터로 검증한 실증 연구가 아니다" — `papers.md:424` 범위 한정과 일치 | ✅ |

**서지:** `*Marketing Science* 37(5), 771–792, 2018` / DOI `10.1287/mksc.2018.1104` — `papers.md:415`와 전부 일치. 등급 `초록 확인`(`:1186`)이라 29행의 직접 인용이 허용 범위 안이다. 29행 인용은 `:420` 초록 원문(`"…it reduces advertiser profits compared to not using attribution at all, and that stronger advertisers suffer from a misallocation of consumer impressions due to overbidding…"`)의 번역이며 의미 손실이 없다.

**희석 방지가 특히 잘 작동한 이유:** 저술가가 **희석된 문장을 본문에 인쇄한 뒤 기각**했다. 10장의 Goldfarb & Tucker 처리("'개인화는 역효과다'로 넓히면")와 같은 형태다. 두 장이 같은 방어 패턴을 독립적으로 쓴 셈이고, 이 책의 방법론적 서명이 되고 있다.

**주장 5 — Blake, Nosko & Tadelis (2015) ✅✅ (3요소 + eBay 맥락)**

| 요구 (`papers.md:499~502`·`:511`, 계획서 §215) | 이행 |
|---|---|
| ① 브랜드 키워드 단기 효과 없음 | 81행 — "측정 가능한 단기 효익이 없었다. 이미 eBay를 찾아온 사람이 광고를 한 번 더 클릭했을 뿐이다" ✅ |
| ② 비브랜드에서 신규·저빈도 고객에게는 효과 있음 | 82행 — "신규 고객과 저빈도 고객은 광고에 긍정적으로 반응했다" ✅ |
| ③ 지출 배분 때문에 평균 수익률 음수 | 83행 — "광고비의 대부분은 광고가 없어도 구매했을 기존·상시 이용자에게 지출되고 있었고, 그 결과 **전체 평균 수익률이 마이너스**로 나왔다" ✅ |
| **"eBay라는 이미 강한 브랜드" 맥락 병기 필수** | 87행 — "**이건 eBay라는 이미 강한 브랜드의 검색광고 실험이다.** 아무도 이름을 모르는 신규 서비스가 자기 브랜드 키워드에 광고를 걸었을 때 같은 결과가 나온다는 보장은 이 연구 안에 없다" ✅✅ |
| "온라인 광고는 효과 없다"로 축약 금지 | 87행 — "'온라인 광고는 효과가 없다'는 **1번만 떼어낸 문장**이고, 2번을 빼면 정반대 방향의 발견 하나를 지운 셈이 된다" ✅✅ |

**서지:** `*Econometrica* 83(1), 155–174, 2015` / DOI `10.3982/ecta12423` / `NBER Working Paper No. 20171, 2014` — `papers.md:491~492`와 전부 일치. 등급 `초록 확인`(NBER, `:1192`). **저자 3인 풀네임(Thomas Blake, Chris Nosko, Steven Tadelis)까지 정확하다.**

**절 제목의 방어:** 절 제목이 "**그렇다고 광고가 무용하다는 뜻은 아니다**"이고 77행이 "'그럼 광고는 다 헛돈'이라는 결론으로 건너뛰면 곤란하다"로 연다. **오인용을 절의 존재 이유로 삼은 구성** — 계획서가 요구한 것보다 강한 방어다.

**C. 등급 표시 (5건) — 근거가 단단한 항목과 이름만 아는 항목의 분리**

| # | 본문 | 원본 등급 | 판정 |
|---|---|---|---|
| 6 | Anderl et al. (2016) — "이 책의 리서치가 **서지 정보까지만 확인**했다 … 이름과 개념적 기여를 가리키는 데서 멈춘다. **효과 크기나 '마르코프가 라스트터치보다 낫다'는 결론 방향은 이 책이 뒷받침할 수 있는 범위 밖이다**" (41~43행) | `메타데이터`(`papers.md:1153`) | ✅✅ 결론 방향까지 명시적으로 금지 |
| 7 | ⑤ 실험 방법론 6편 — "아래 네 문단의 근거 논문은 이 책의 리서치가 **서지 정보까지만 확인**한 것들이다. 그래서 각 논문이 보고한 **수치나 효과 크기는 옮기지 않고**, 각 논문이 제기한 문제와 처방만 쓴다" (97행) | 전부 `메타데이터`(`:1176`~`:1185`) | ✅✅ |
| 8 | 상시 홀드아웃 — "이 설계를 정식화한 **독립 정전 논문은 이번 리서치에서 특정되지 않았다.** 통제 실험 일반론과 아래 고스트 광고 계열에서 정당화를 빌려 와야 한다" (113행) | `papers.md:406`·`:1112` 문언과 일치 | ✅✅ |
| 9 | Vaver & Koehler (2011) — "**이건 Google Inc.의 기술 보고서이고 peer-reviewed 논문이 아니다.** 4장의 표에 이 항목이 올라간 이유가 그것이다" (132행) | `papers.md:477`·`:1111`·`:1191` | ✅✅ |
| 10 | Jin, Wang, Sun, Chan, Koehler (2017) — "**이것 역시 Google의 기술 보고서로 peer-reviewed가 아니다**" (136행) | `papers.md:431`·`:1187` | ✅✅ |

**주장 7의 검증 방법:** ⑤ 소절 전체(95~107행)를 훑어 **연구 결과 수치가 하나라도 넘어왔는지 전수 확인했다. 0건이다.** 등장하는 숫자는 전부 서지 정보(권·호·페이지·연도·DOI)이고, 그 서지도 원본과 일치한다 — Kohavi `DMKD 18, 140–181` / `10.1007/s10618-008-0114-1`(`:342`), KDD 2012 `10.1145/2339530.2339653`(`:358`), KDD 2013 `10.1145/2487575.2488217`(`:351`), Johari KDD 2017 `10.1145/3097983.3097992` + *OR* `70(3), 1806–1821, 2022` `10.1287/opre.2021.2135`(`:373~374`), B&H *JRSS-B* `57(1), 289–300, 1995` `10.1111/j.2517-6161.1995.tb02031.x`(`:382`), CUPED WSDM 2013 `10.1145/2433396.2433413`(`:365`), Eckles *JCI* `5` `10.1515/jci-2015-0021`(`:390`), Saveski KDD 2017 `10.1145/3097983.3098192`(`:398`). **DOI 14건 전수 대조 — 오귀속·오식별 0건.**

**주장 11 — Kohavi 연도 갈림 처리 ✅**
95행: "통상 2009년으로 인용되지만 **서지 등록상 발행 연도는 2008로 잡혀 있어 연도 표기가 갈린다**" — `papers.md:342`("Crossref issued 2008; 통상 `(2009), DMKD 18: 140–181`로 인용")와 정확히 대응. **10장의 Tucker 2013/2014 처리와 같은 패턴**이고, 이 책이 서지 상충을 감추지 않는다는 일관성이 두 장에서 확인된다.

**주장 12~15 — ⑤ 네 문단의 "문제와 처방" 서술 ✅ (전건 원본 대응)**

| 본문 | 원본 |
|---|---|
| Kohavi 흔한 함정에 "표본 비율 불일치(SRM), 계측 오류, 심슨의 역설이 포함된다"(95행) | `:345` "흔한 함정(SRM, 계측 오류, Simpson's paradox)" ✅ |
| 피킹 — "1종 오류율이 크게 부풀어 오른다 … 저자들은 **언제 멈춰도 유효한** 순차적 p-값과 신뢰구간을 제시한다"(99행) | `:376` 문언과 거의 축자 대응 ✅ |
| FDR — "기각된 가설 중 거짓 발견"의 통제 절차(103행) | `:384` ✅ |
| CUPED — "실험 이전 기간의 지표를 공변량으로 써서 분산을 줄이는 방법 … 같은 트래픽으로 더 작은 효과를 검출"(105행) | `:367` 축자 대응 ✅ |
| Eckles — SUTVA 위반, 클러스터 설계로 편향 축소(107행) | `:392` ✅ |
| Saveski — "**간섭이 있는지 없는지를 가정하지 말고 검정하라**" + 개인/클러스터 단위 무작위화 병행(107행) | `:400~401` "무작위화 자체를 무작위화 … 가정하지 말고 측정하라" ✅ |

**D. MMM·고스트광고 (4건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 16 | Jin et al. 초록 인용 2건 — "표본 크기가 작을 때는 사전분포가 사후분포에 큰 영향을 주어 편향된 추정으로" / "최적 미디어 믹스가 파라미터 추정치의 분산 때문에 그 자체로 큰 분산을 갖는다" | `papers.md:439~440` 영문 초록 원문 2문장의 번역 — 의미 손실 없음 | ✅ |
| 17 | **"MMM 대시보드가 뱉는 채널별 최적 예산을 점 추정치로 받아들이면 안 된다"** (142행) | `papers.md:442`·`:1088`(로그 2066행 "점 추정치가 아니라 분포로 다루라") | ✅✅ |
| 18 | Meridian·Robyn — "학술 계보를 확인해보면 **기업 사내 기술 보고서와 베이지안 통계 교과서**로 이어지고, **방법론도 서로 다르다**" (144행) | `papers.md:463`·`:472`·`:1110` | ✅✅ |
| 19 | 고스트 광고 — Johnson, Lewis, Nubbemeyer, 2017, *JMR* 54(6), 867–884, DOI `10.1509/jmr.15.0297` + PSA 비용 문제 + "노출됐을 것이라는 사실만 기록" | `papers.md:536`·`:539` 서지·설명 전부 일치 | ✅ |

**주장 18이 3파 로그의 지시를 정확히 지켰다.** 로그 2066행이 "`papers.md:1134`는 Robyn 방법론이 **웹 검색 기반이고 저장소를 직접 파싱하지 않았다**고 기록했다 — 방법론 세부를 쓸 거면 1차 확인이 선행돼야 한다"고 경고했는데, **저술가는 방법론 세부(Ridge·Nevergrad·TensorFlow Probability·베이지안 계층)를 한 단어도 쓰지 않았다.** "방법론도 서로 다르다"는 대비만 남기고 근거가 약한 세부는 통째로 버렸다. 확인 실패를 우회하는 가장 깨끗한 형태다.

**E. 커뮤니티 인용 (5건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 20 | fourseventy 인용 + "HN 28855010 (2021-10-13). **어트리뷰션 제품을 파는 회사 운영자의 진술이라 이해관계가 있다**" | `community.md:514`(ID·작성자·날짜·자기 진술 성격 전부 일치)·`:1153` | ✅✅ 이해관계 고지 |
| 21 | 150행 — fourseventy가 "같은 댓글에서 … 그 광고 채널들이 실제 가치를 만드는 것도 사실이라고 덧붙였다" | `community.md:1015` `"however those ad channels still do drive real value"` — **같은 댓글**이라는 서술도 정확 | ✅ |
| 22 | ssharp 요지 "종합적인 분석을 원한다면 종합적인 측정 계획을 세우는 데 시간을 들여야 한다"(HN 9257502 / 2015-03-24) | `community.md:511`·`:1013` `"If you want comprehensive analytics, you need to spend time developing a comprehensive measurement plan."` | ✅ |
| 23 | etempleton 인용(HN 48180365 / 2026-05-18) + "**이 조사에서 확보한 이 논쟁의 발언 가운데 가장 최근 것이다**" | `community.md:519`("가장 최신")·`:1019` 원문 3문장 대응 | ✅✅ 범위를 "이 조사"로 한정 |
| 24 | **"어트리뷰션을 100% 맞추려 하지 말고 85% 정도를 목표로 하라 … 85%는 근거 없는 어림수다"**(HN 9258007 / bduerst / 2015-03-24) | `community.md:506`·`:508`("실무 휴리스틱이다")·`:1151` | ✅✅✅ |

**주장 24가 이 장에서 가장 모범적인 수치 처리다.** 커뮤니티 어림수를 인용하면서 **바로 다음 문장에서 굵게 "근거 없는 어림수다"라고 등급을 박았다.** 그리고 "다만 완전성을 포기하고 KPI를 먼저 정하라는 **순서 자체는 여러 소스가 공유한다**"로 무엇이 살아남는지를 분리했다 — 근거는 bduerst와 ssharp 둘(`:506`·`:511`)로 "여러 소스" 표현이 성립한다. 숫자는 버리고 방향만 취하는 처리의 정본이다.

**F. 장 간 연결 (2건)**

| # | 본문 | 판정 |
|---|---|---|
| 25 | 111행 "4장에서 근거가 끊긴 열두 항목을 표로 놓았을 때, **그중 세 행에 '11장'이라는 포인터가 붙어 있었다**" → 홀드아웃·지오 실험·MMM 3행 회수 | ✅ `chapters/04_final.md` 표 대조 — `papers.md:1110`(Meridian/Robyn) `:1111`(지오 실험) `:1112`(상시 홀드아웃) 세 항목이 실재하고, 본문이 셋을 순서대로 갚는다 |
| 26 | 21행 "3장에서 어트리뷰션 제품과 CDP·CEP를 API 카탈로그로 갈랐던 걸 기억할 것이다. `Attribution Result`라는 엔드포인트가 있느냐 없느냐로" | ✅ 3장이 확립한 사실의 역참조 — 새 사실 주장 없음 |

### 계획서 §A 금지 항목 스캔 (11장)

| 금지 항목 | 결과 |
|---|---|
| **Gordon 2019에 구체 수치 귀속** (§A-11) | **0건** ✅ `grep -c "2019"` = **0**. 논문 자체가 등장하지 않는다 |
| Goldfarb & Tucker 범위 한정 누락 (§212) | **해당 없음** — 11장은 이 논문을 인용하지 않는다(아래 커버리지 판정 참조) |
| Berman 조건절 누락 (§214) | **0건** ✅ 조건절이 인용문과 해설 **두 곳**에 있다 |
| Blake 맥락 누락 (§215) | **0건** ✅ 3요소 + eBay 브랜드 맥락 전부 |
| LLM 카피 효과 크기 (§A-12) | **0건** ✅ (문자열 전무) |
| Send-time optimization을 학술 근거로 (§추가 규율) | **0건** ✅ (11장 소재 아님) |
| Theta Sketch·C-Store DOI (서지 함정 2건) | **0건** ✅ (11장 소재 아님) |
| Tier 2 버전·수치 (§B) | **0건** ✅ |

### Goldfarb & Tucker 커버리지 구멍 점검 — **구멍 없음 ✅**

11장이 이 논문을 인용하지 않은 것이 누락인지 확인했다. **누락이 아니다.**
- **계획서 배치가 그렇다** — §3-C(개인화 역효과)는 **10장 소재**로 지정돼 있고, `papers.md:146`의 D-5-2가 프라이버시·개인화 축(D-5)에 속한다. 어트리뷰션·증분성 축(D-9·D-10)이 아니다.
- **10장이 실제로 다뤘다** — `10_draft.md:193~207` 한 개 절 전체가 이 논문에 배정됐고, 초록 원문 인용 + 범위 한정 + 인접 연구 3건(White·Awad & Krishnan·Tucker)까지 붙었다. **본 검증 10장 주장 32에서 ✅✅ 판정.**
- **두 장이 겹치지도 비지도 않았다** — 10장은 "개인화 강도와 프라이버시 우려"를, 11장은 "성과 측정의 신뢰도"를 다룬다. 같은 논문을 양쪽에서 인용했다면 오히려 범위 한정을 두 번 반복해야 하는 부담이 생겼을 것이다.

### 11장 총평

**3파가 "위험이 전부 여기 남았다"고 지목한 네 이름(Gordon·Goldfarb·Berman·Blake)이 전건 통과했다.** 특히 **Gordon 2023의 아홉 개 수치가 퍼널 배치까지 초록과 일치**했고, **Gordon 2019는 문서에 0회 등장**해 3파가 경고한 최악의 시나리오가 발생하지 않았다.

이 장의 방법론적 특징은 **등급 표시를 서술 장치로 삼은 것**이다. 43행("어느 쪽인지 매번 표시하면서 간다")과 97행(⑤ 소절 전체 선행 고지)이 그 선언이고, 실제로 서지만 확인한 논문 9편에서 수치가 단 하나도 넘어오지 않았다. 3파 로그 2036행이 ①형 실패로 지목했던 "고지를 절 단위로 잡기"의 문제도 없다 — 97행의 고지는 **적용 범위를 "아래 네 문단"으로 명시**했고 실제로 그 네 문단에서 끝난다.

**⚠️ 2건 중 하나(주장 A)만 11장 본문 수정 사항이고, 문장 하나 교체로 끝난다.** 다른 하나는 9장 쪽 조정이다.

---

## 12장 — 1차 검증

> 소스 편향이 가장 큰 장이다. 앞의 열한 장이 벤더 공식 문서·법령 조문·심사 논문에 기댄 반면 이 장의 재료는 **채용 공고·벤더 자기 블로그·해커뉴스 댓글** 셋뿐이고, 셋 다 이해관계나 표본 편향이 있다. 3파 로그 2069~2073행이 시점 병기와 주어 한정을 요구한 자리다.
>
> **결과: ❌ 0 / 🕒 0 / ⚠️ 2 / ✅ 24. 금지 항목 위반 0건.**

### ❌ 정정 필요 — **0건**

### 🕒 검증 불가 — **0건**

### ⚠️ 근거 약함 — 2건

**주장 A — "이 표에서 눈에 걸리는 건 3위와 4위다 … 비용 감각과 소통이 순수한 코딩 역량보다 위에 온다" (12:113)**

- **표 자체는 ✅ 완전 일치.** `community.md:885~898`의 F-5-A 표 12행을 **순서까지 그대로** 옮겼고(1 이벤트 스트림 → 2 K8s → 3 FinOps → 4 소통 → 5 흐름 설명 → 6 멱등성 → 7 SQL/DW → 8 모니터링 → 9 SDK → 10 영어 → 11 Go/Kotlin → 12 회복 탄력성), 별 등급 정의도 `:883`("⭐⭐⭐ = 채용 공고 본문 다수 + 커뮤니티 교차 / ⭐⭐ = 공고 또는 커뮤니티 한쪽")과 96행이 **문언까지 대응한다.** 원본 표에 `순위` 열이 실제로 있으므로 "3위와 4위"라는 지칭도 **출처상으로는 거짓이 아니다.**
- **그런데 두 가지가 어긋난다.**
  1. **본문의 표에는 순위 열이 없다.** 저술가가 `순위`를 빼고 `강도`만 남겼는데(96행이 근거 강도 축이라고 선언했으므로 옳은 선택이다), 그 상태에서 "3위와 4위"라고 부르면 **독자가 볼 수 없는 열을 가리킨다.** 동시에 이 표가 순위표라는 인상을 준다 — 84행이 다른 목록에 대해 "**업계의 순위표가 아니다**"라고 명시한 것과 같은 장 안에서 어긋난다.
  2. **"순수한 코딩 역량보다 위에 온다"가 같은 표에 의해 반박된다.** 3위·4위 **위에 있는 1위·2위가 대용량 이벤트 스트림 처리와 Kubernetes 운영**이다. 둘 다 기술 역량이다. 즉 원본의 순위 안에서 코딩 역량은 비용 감각·소통보다 **위에** 있다. 실제로 참인 것은 순위가 아니라 **등급**이다 — FinOps와 소통이 ⭐⭐⭐ 칸에 있는 반면 SQL·모니터링·SDK 통합·Go/Kotlin은 전부 ⭐⭐다.
- **정정안 (113행 첫 두 문장 교체):**
  > "이 표에서 눈에 걸리는 건 별 셋 칸의 구성이다. **비용 감각과 소통이 대용량 스트림 처리·쿠버네티스 운영과 같은 칸에 있고, SQL도 모니터링도 SDK 통합도 그 아래 칸이다.**"
- **왜 이게 더 강한가:** 원 문장은 "코딩보다 위"라는 반박 가능한 비교를 하지만, 정정안은 **근거 강도라는 이 장이 스스로 정의한 축**에서만 말한다. 뒤에 이어지는 세 근거(AB180 DevOps의 FinOps 4대 업무, AB180 백엔드 우대사항, 빅인사이트 Strong Fit)가 그대로 살아난다. **근거:** `community.md:885~898`·`:883`·`:134`·`:80`·`:141`

**주장 B — 12:144~148의 커뮤니티 인용 4건에 HN ID가 없다 (서지 일관성)**

- **내용은 4건 전부 ✅ 확인됐다.** 사실 오류가 아니라 **이 책이 스스로 세운 인용 표기 규칙에서 이 네 건만 이탈**한 문제다. 10장 3건·11장 4건·같은 장 shkan 1건은 전부 `HN {ID} / {작성자} / {날짜}` 형식을 지켰다.

| 본문 | 원본 | ID·작성자·날짜 |
|---|---|---|
| "어느 인수 소식 스레드에서 한 사람은 위키백과의 정의를 옮겨 붙인 뒤 … **'그래서 아무도 자기가 하는 일을 편하게 이야기하지 못한다'**" | `community.md:713` `"So nobody feels comfortable talking about what they do."` 스토리: "Twilio set to acquire Segment for $3.2B" — **인수 소식 스레드 맞다** | **HN 24737006 / m463 / 2020-10-10** |
| "다른 스레드에서는 더 냉소적인 진단 … 일부러 불투명하게 쓰인 것 같고 … 너무 자세히 알지 않는 편이 마음 편하다" | `community.md:722`(`"intentionally obfuscated to the readers not already in the know"`)·`:1048`(`"it is more comfortable not to be too aware about it"`) | **HN 27555225 / salicideblock / 2021-06-18** |
| "어떤 이는 장바구니 이탈 이메일 캠페인 정도는 무해하다고 썼고" / "**2025년 9월의 한 댓글**" + Target 임신·육아 광고 + "대형 집계 업체에 되파는 것은 신경이 쓰인다" | `community.md:726`·`:1049~1050` (`"Shopping Cart abandonment email campaigns are pretty benign"` / `"the targeted ad for baby/pregnancy products… from Target"` / `"I do care about them reselling that data to big aggregators"`) | **HN 45106650 / jacobr1 / 2025-09-02** — 본문의 "2025년 9월" ✅ |
| "또 어떤 이는 사용자를 다른 사이트까지 따라다니지 않는 분석 도구도 얼마든지 있다고 반박했다" | `community.md:1044` `"there are numerous services that provide analytics and have no part in tracking you elsewhere"` | **HN 11267213 / robbiemitchell / 2016-03-11** |

- **정정안:** 위 표의 ID·날짜를 각 문장 끝 괄호에 붙여라. 형식은 같은 장 82행(`— shkan, Hacker News 39103276 (2024-01-23, 댓글 0개)`)을 따르면 된다.
- **부수 ✅✅:** "**가장 정직한 형태는 양쪽을 한 사람이 동시에 말하는 대목에서 나왔다. … 이 사람은 장바구니 이탈 캠페인은 무해하다고 쓴 바로 그 사람인데**"(148행)는 `community.md:1049`의 괄호 주석 "**(같은 사람이 A와 B를 동시에 말한다)**"를 정확히 옮긴 것이다. 리서처가 특별히 표시해둔 구조적 관찰을 본문 구성 원리로 승격시켰다.

### ✅ 확인됨 — 24건

**A. 채용 공고 축 (9건) — 시점 병기·주어 한정·표본 압축 방지**

**주장 1 — AB180 24 / 3 / 7 비율 ✅✅✅ (계획서 §B:221 완전 이행)**
- **본문 19행:** "**2026년 7월 원티드 active 공고 기준** AB180에 올라와 있던 **스물네 건** 가운데, 소프트웨어를 만드는 일이 직무의 중심인 공고는 **세 건**이었다 — Backend Engineer(Data Pipeline), DevOps Engineer, Endpoint Security Engineer."
- **근거:** `community.md:32`("F-1-A. 국내 (원티드 API, **조회일 2026-07-25**)")·`:36`("조회 시점 **active 공고 24건**")·`:49`("active 24건 중 **순수 소프트웨어 엔지니어 공고는 3건**(Backend Engineer - Data Pipeline, DevOps Engineer, Endpoint Security Engineer)")
- **비개발 기술직 7건도 원본과 일치:** 본문 "Solution Architect, Technical Support Manager 계열 둘, Customer Success Manager 둘(하나는 온보딩, 하나는 Amplitude·Braze 담당), QA Engineer, Technical Writer" ↔ `:49` "Solution Architect, Technical Support Manager ×2, CSM-Onboarding, CSM-Amplitude & Braze, QA, Technical Writer" — **7건 전부 대응, 계열 표기까지 정확.**
- **§B:221 요구("2026년 7월 원티드 active 공고 기준"을 **문장 안에**):** ✅ 굵게 처리해 문장 첫머리에 배치.

**주장 2 — 표본 압축 방지 ✅✅✅ (3장이 ❌를 받은 형태의 재발 없음)**
- **본문 21행:** "이 숫자에는 두 가지를 함께 붙여야 한다. **공고는 채워지면 내려가므로 이 비율은 그날 그 회사의 사진일 뿐이고, QA를 개발 직무로 셀지 말지에는 세는 사람의 판단이 들어간다.** 그러니 '세 건 대 일곱 건'이라는 비율보다 **직무 이름의 목록 자체가 더 많은 것을 말해준다고 보는 편이 낫다.**"
- **판정:** 3장이 "20곳 중 4곳"으로 ❌를 받았던 실패 형태 — 표본을 비율로 압축해 일반화하는 것 — 이 **정확히 반대 방향으로 처리됐다.** ① 스냅숏임을 밝히고 ② 분류 판단이 개입함을 밝히고 ③ **비율보다 목록이 낫다고 독자를 안내한다.** 세 겹 방어다. 저술가 자기 보고("QA 판단 단서를 달았다")는 사실이고, **요구된 것보다 두 겹 더 붙였다.**

**주장 3~9 — 나머지 공고 항목**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 3 | 해외 4사(Braze·Klaviyo·Twilio·Hightouch) "**2026년 7월 25일에 조회했을 때**" | `community.md:244`(조회일 2026-07-25, 4사 HTTP 200) | ✅ |
| 4 | **총 공고 수를 쓰지 않았다** — 회사명과 직무 이름만 | `:247~250`에 236/152/183/70이 있으나 본문 미사용. `:252`가 Census·RudderStack·Snowplow·Segment·mParticle **조회 실패**를 기록했으므로 "주요 벤더 전부"류 표현은 위험한데, 본문은 **네 회사만 명시**한다(로그 2072행 준수) | ✅✅ |
| 5 | 엔지니어 타이틀 3건 — Twilio `Principal Software Engineer - Identity Graph`, Twilio `Software Engineer, (L2) CDP`, Klaviyo `Senior Software Engineer - Profiles, Lists and Segments` | `community.md:288~291`·`:293` — **세 타이틀 문자열 전부 verbatim 일치**. `:293`이 이 세 개를 특별히 묶어 강조한 것까지 그대로 받았다 | ✅✅ |
| 6 | Deliverability 전담 "**이 중 세 회사에** 있다" | `community.md:283~286`(Braze·Klaviyo·Hightouch)·`:705`("**세 회사 모두**") — **네 회사 중 셋. Twilio를 넣지 않았다** | ✅✅ |
| 7 | Deliverability 행 "(공고 본문은 열지 못했다 — **이 자리가 있다는 사실 자체가 관찰이다**)" | 확인 범위를 셀 안에서 밝힘 | ✅✅ |
| 8 | 직무→담당 장 매핑 표 — "오른쪽 칸은 **공고 본문과 이 책의 목차를 대조한 것이지 회사가 그렇게 분류했다는 뜻이 아니다**" | 저자 해석 표시 ✅ (계획서 요구) | ✅✅ |
| 9 | 빅인사이트 Data Platform Engineer "What Makes A Strong Fit" 5항목 "**(2026년 7월 원티드 공고 기준)**" | `community.md:141`(원티드 기업 ID 31825, 공고 ID 359453, active) + 5항목 원문 대응 | ✅ |

**B. 한국 벤더 서술 (3건) — 금지 항목의 핵심 구역**

| # | 본문 | 판정 |
|---|---|---|
| 10 | AB180이 Airbridge를 만들면서 Braze·Amplitude를 국내 공급 "**(공고 타이틀과 두 건의 직무기술서 본문에서 교차 확인된다)**" | ✅ `community.md:343`(SA 우대: Airbridge, Braze, Amplitude…)·`:344`(CSM-Onboarding 우대)·`:36~48`(CSM-Amplitude & Braze 타이틀) — **교차 확인 주장이 사실** |
| 11 | "**다만 국내 벤더의 규모·투자·고객사 수는 이번 리서치가 1차 자료로 확인하지 못했으니, 회사가 스스로 말한 것 이상은 적지 않는다**" | ✅✅✅ **규모·투자·고객사 수 0건** — `grep` 확인. 금지 항목을 지켰을 뿐 아니라 **왜 없는지를 본문에 남겼다** |
| 12 | "3장에서 국내 벤더 세 곳의 공개 개발자 문서를 찾지 못했다고 했던 그 관찰" 역참조 | ✅ 3장이 확립한 negative finding의 재사용 — 새 주장 없음 |

**C. 인터뷰 인용 (3건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 13 | 오프닝 "밥값" 인용 + "**(페이지에 게시일이 없어 시점은 미상이다)**" | `community.md:383` 원문 대조 — "월 수억 원", "안정성과 효율성이 가장 중요한 키워드", "잘 보이지도 않고 설명하기도 쉽지 않아", "오늘 밥값 했다" 전부 일치. 게시일 미상 표기도 정확 | ✅ |
| 14 | "백엔드, 데브옵스, 데이터 엔지니어가 하는 일을 복합적으로" 인용 + "**한 회사 한 팀의 이야기이고, 다른 회사가 같은 방식으로 조직을 짰다는 근거는 아니다**"(52행) | `community.md:377` verbatim. **범위 한정을 인용 직후에 배치** | ✅✅ |
| 15 | "비즈니스 로직이 어렵다고 느꼈고, 동시에 이해가 되지 않는 로직이 많았습니다" 인용 | `community.md` F-2-A 인터뷰 원문 대응 | ✅ |

**D. 커뮤니티·저장소 증거 (5건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 16 | shkan — "2024년 1월 … **댓글은 하나도 달리지 않았다. 그러니까 이건 커뮤니티의 합의가 아니라 한 사람의 토로다. 그 점을 알고 읽자**" + `— shkan, Hacker News 39103276 (2024-01-23, 댓글 0개)` | `community.md:474`(ID·작성자·게시일)·`:476`("**댓글 0개** — 즉 '커뮤니티 합의'가 아니라 **한 실무자의 토로**다") — **원본의 판단 문장을 그대로 옮겼다** | ✅✅✅ |
| 17 | Snowplow — "들어오는 이벤트를 스키마로 검증하자는 취지의 이슈가 **2014년부터 여러 건** 남아 있다(**이슈 제목과 번호, 날짜만 확인했고 본문은 열지 못했다**)" | `community.md:543~547`(검색 결과 9건, #611 2014-04-01 / #625 2014-04-08 / #910 2014-07-22)·`:550`("**2014년부터**") | ✅✅ 확인 범위 명시 |
| 18 | rudder-server — "'목적지 하나가 죽으면 전체가 극도로 느려진다'는 제목의 이슈가 **2024년 7월에 열려 조회 시점까지 그대로였다**(**제목·상태·날짜·댓글 수만 확인했다**)" | `community.md:751`(#4953, **2024-07 생성, 조회 시점 여전히 open**, 댓글 16개) | ✅✅ |
| 19 | 84행 "아래는 **이 표본에서 눈에 띈 것들이지 업계의 순위표가 아니다**" 이후 "가장 자주 나온 것은 / 두 번째 / 세 번째…" | 3파 로그 2129행이 정리한 기준 — **문장 안 범위 한정어**가 있으면 통과. 84행이 "이 표본에서"로 적용 범위를 스스로 묶는다 | ✅ (경계 통과) |
| 20 | 90행 "국내 컨설턴트 공고는 '데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅'을 아예 주요 업무로 적어둔다" | `community.md:347`(마티니 주요업무) | ✅ |

**E. 소스 편향 고지·negative finding (4건)**

| # | 본문 | 근거 | 판정 |
|---|---|---|---|
| 21 | 13행 소스 편향 고지 전체 — "채용 공고·벤더 블로그·해커뉴스 세 종류 / 공고는 마감되면 사라지는 스냅숏 / 벤더 블로그는 회사를 잘 보이게 쓸 이유가 있으며 / **해커뉴스는 영어권에 심하게 치우친 표본** / 국내 개발자 커뮤니티는 사실상 확보 못 했고(**레딧은 조회 자체가 막혔다**) / 한국 쪽 서술은 대부분 **이해관계가 있는 소스**에 기댄다" | `community.md:24`("영어권 HN 비중이 크다. **Reddit이 차단돼** 실무자 표본이 한쪽으로 기울었다 … 한국 현장 목소리는 **벤더 기술블로그·채용 공고**에서 주로 확보됐고, **이건 이해관계가 있는 소스다. 이 편향을 챕터에서 감춰서는 안 된다**")·`:1071`(Reddit 전체 차단, `<title>Blocked</title>`) | ✅✅✅ 리서처의 요구를 **항목별로 전부** 이행 |
| 22 | 13행 "**이 장에 '업계는 이렇다'는 문장이 거의 없는 이유가 그것이다. 대신 '이 시점에 이 표본에서는 이렇게 보였다'고 쓴다**" | 3파 로그 2041행이 지목한 범주 확장어("업계는")를 **장 첫머리에서 스스로 금지**했다 | ✅✅✅ |
| 23 | 117행 "이 리서치는 **면접에서 어떤 질문이 나오는지에 대한 자료를 확보하지 못했다.** … 그러니 위 표가 말할 수 있는 범위는 '공고가 이것을 요구한다'까지다. **'면접에서 이게 나온다'로 읽으면 없는 근거를 만드는 일이 된다**" | 확보 실패를 부재로 오독하지 않게 막는 마지막 문장(로그 2077행 패턴) | ✅✅ |
| 24 | 138행 "인하우스 쪽은 이번 리서치가 **직무기술서를 직접 확보하지 못해 표본이 약하다** … 이 대비는 공고와 블로그에서 읽어낸 윤곽이지 **두 세계를 겪은 사람의 증언이 아니다**" / 156행 "여기 인용한 것도 결국 **몇 명의 댓글이다**" | 같은 패턴 2회 추가 | ✅✅ |

**F. 쿠팡 — 책의 마지막 안심 장치 (1건)**

**주장 25 — 쿠팡 데이터 플랫폼 진화 ✅✅✅ (연도 4개 전건 일치)**

| 본문 (164행) | `web_stack.md:1268~1275` |
|---|---|
| "2022년 **8월 3일**에 공개한" | `2022-08-03 (페이지 표기·확정)`(`:1404`) ✅ |
| "**네 단계**를 거쳤는데" | Phase I~IV ✅ |
| "첫 단계인 **2010년부터 2013년까지**의 구성은 **관계형 데이터베이스**였다" | "**Phase I (2010–2013):** 관계형 DB, 소규모 데이터 사이언스 팀" ✅ |
| "하둡과 MPP가 들어온 것은 **2014년부터**고" | "**Phase II (2014–2016):** Hadoop + MPP 도입" ✅ |
| "클라우드로 전면 이전한 것은 **2016년 이후**이며" | "**Phase III (2016–2017):** 클라우드 전면 이전" ✅ |
| "서비스 기반 모델로 재편된 것은 **2019년부터**다" | "**Phase IV (2019–):** 서비스 기반 모델" ✅ |
| "**2022년 글이니 지금 구성은 또 달라졌을 것이다**" | `:1270` ⚠️ "**2022년 글 — 현행 아키텍처와 다를 수 있음.** '진화 서사'로만 인용할 것" ✅✅ |

**연도 6개·단계 수·발행일 전부 정확하고, 리서치가 붙인 신선도 경고까지 본문 문장으로 옮겼다.** 그리고 사용 목적이 `:1280`의 지시("'처음부터 이 스택을 다 짓지 않는다'는 메시지의 근거 … **마무리 챕터의 안심 장치로 배치할 것**")와 정확히 일치한다 — 절 제목이 "처음부터 다 짓지는 않는다"다. **이 책의 마지막 사실 주장이 자릿수까지 정확하다.**

### 계획서 §A 금지 항목 스캔 (12장)

| 금지 항목 | 결과 |
|---|---|
| 한국 벤더 규모·투자·고객사 수 | **0건** ✅ + 부재 사유 명시(42행) |
| CDP 4분류 / CDP Institute 정의문 | **0건** ✅ (125행은 "정의가 두 갈래이고, 해소하지 않는 편이 정직하다"로 3장 결론만 역참조) |
| CEM·CXM | **0건** ✅ |
| **Snowplow·RudderStack "오픈소스" 단정** | **0건** ✅ — 두 이름이 86·88행에 나오지만 **"저장소"로만 지칭**한다("Snowplow 저장소에는…", "RudderStack의 `rudder-server` 저장소에"). 라이선스 단어가 없다 |
| Tier 2 버전·수치 | **0건** ✅ (Kafka·Kubernetes·Go·Kotlin 전부 버전 없이 이름만) |
| DMARC "표준" | **0건** ✅ |
| LLM 카피 효과 크기 | **0건** ✅ |
| Theta Sketch·C-Store DOI·SKAdNetwork·PIPA 수치·ADH 임계값 | **0건** ✅ (전부 12장 소재 아님) |

### 3파 경고 ③형 재발 점검 (12장)

- **범주 확장어:** "업계는" **0건** — 13행이 이 어휘를 장 첫머리에서 명시적으로 금지했고 실제로 지켰다. `grep` 확인.
- **분포·순위 주장어:** 84행("가장 자주 나온 것은")은 **직전 문장의 범위 한정으로 통과**(로그 2129 기준). 113행("3위와 4위")은 **⚠️ 주장 A** — 이 장의 유일한 ③형 관련 지적이다.

### 12장 총평

**소스가 가장 약한 장인데 고지가 가장 두껍다.** 13행의 편향 고지는 리서처가 `community.md:24`에서 "이 편향을 챕터에서 감춰서는 안 된다"고 요구한 항목을 **하나씩 대응해 옮겼고**, "이 장에 '업계는 이렇다'는 문장이 거의 없는 이유가 그것이다"로 **어휘 규율까지 독자 앞에서 선언**했다. 3파 로그가 반복 지적한 ③형의 근본 처방(주어를 조사한 범위로 유지)을 장 설계 원리로 승격시킨 셈이다.

**채용 수치는 §B:221을 그대로 이행했고**(19행·52행 두 곳 모두 시점 병기), **3장이 ❌를 받았던 표본 압축은 세 겹으로 방어됐다.** 해외 공고는 총계를 쓰지 않고 회사명만 남겨 조회 실패 5사를 "전부"에 포함시키는 실수를 피했다.

**쿠팡 항목은 이 책의 마지막 구체 사실 주장인데 연도 6개가 전부 정확하다.** 신선도 경고까지 옮겼다.

**⚠️ 2건은 둘 다 문장·괄호 단위 수정으로 끝나며 Phase 5를 차단하지 않는다.**

---

## 9장 53행 ↔ 11장 Gordon 등급 정합 판정

> 3파 로그 2067행이 4파에 남긴 유일한 **장 간 사실 정합** 과제다. "9장 53행이 '11장에서 만날 어트리뷰션·증분성 연구들 … 그쪽은 초록과 수치까지 확인한 근거이고'라고 적었다. **이건 11장에 대한 사실 주장이다.** … **11장이 Gordon 2019를 초록·수치 근거처럼 다루면 9장 53행이 거짓이 된다.**"

### 정본 문장 (초안 53행 → `chapters/09_final.md:55`, 행 번호가 밀렸다)

> "…다만 이 책의 리서치는 이 논문의 서지와 피인용 수까지만 확인했고 초록을 확보하지 못했다. 그래서 여기서는 이름과 '이 어휘에 학술적 계보가 있다'는 사실까지만 옮긴다. **11장에서 만날 어트리뷰션·증분성 연구들과 같은 무게로 읽지는 말자. 그쪽은 초록과 수치까지 확인한 근거이고, 이쪽은 아직 이름뿐이다.**"

### ① 3파가 경고한 실패 시나리오 — **발생하지 않았다 ✅**

- `grep -c "2019" chapters/11_draft.md` = **0**. **Gordon 2019(D-10-2, `초록 확인(요약본만)` 등급)는 11장에 등장조차 하지 않는다.**
- 11장의 모든 증분성 수치는 **Gordon, Moakler & Zettelmeyer (2023)** 귀속이고, 서지·DOI·arXiv ID가 두 곳(59행·67행)에 명시돼 있다.
- 두 논문을 한 문장에 섞은 흔적 **0건** (로그 2065행 요구).
- **이 축에서는 9장 55행이 참이다.** 11장 결론을 떠받치는 세 논문 — Gordon 2023(`초록 확인`, `papers.md:1194`), Berman(`초록 확인`, `:1186`), Blake(`초록 확인`, `:1192`) — 이 전부 초록 확인 등급이고, **그중 Gordon 2023은 실제로 아홉 개 수치를 초록에서 옮겼다.** "초록과 수치까지 확인한 근거"라는 표현이 정확히 대응한다.

### ② 그러나 문장의 **양화 범위**가 11장 본문과 부분적으로 어긋난다 — ⚠️

9장 55행은 **"11장에서 만날 어트리뷰션·증분성 연구들"** 전체에 대해 **"그쪽은 초록과 수치까지 확인한 근거이고"**라고 **전칭으로** 말한다. 그런데 11장은 스스로 자기 인용을 두 등급으로 갈라 놓았다.

| 11장이 인용한 논문 | `papers.md` 등급 | 11장이 붙인 표시 |
|---|---|---|
| Gordon, Moakler & Zettelmeyer (2023) | **초록 확인** | 수치·인용 사용 |
| Berman (2018) | **초록 확인** | 인용 + 조건절 |
| Blake, Nosko & Tadelis (2015) | **초록 확인** | 3요소 사용 |
| Anderl et al. (2016) | 메타데이터 | "**서지 정보까지만 확인**"(41~43행) |
| Johnson, Lewis & Nubbemeyer (2017) | 메타데이터 | 설계 개념만 |
| Vaver & Koehler (2011) / Jin et al. (2017) | 문서 확인 | "**peer-reviewed 아님**" 명시 |
| Kohavi ×3 / Johari / B&H / Deng / Eckles / Saveski | 전부 메타데이터 | "**서지 정보까지만 확인 … 수치나 효과 크기는 옮기지 않는다**"(97행) |

**11장 43행이 직접 쓴 문장:** "이 장은 **근거가 단단한 항목과 이름만 아는 항목을 나란히 놓되, 어느 쪽인지 매번 표시하면서 간다.**"

즉 **11장 본문이 9장 55행의 전칭을 스스로 부인한다.** 독자가 9장에서 "11장 것들은 다 초록·수치까지 확인됐다"는 인상을 안고 11장에 도착하면, 97행에서 "여기부터는 서지만 확인했다"를 만난다.

### ③ 판정: ⚠️ (경미) — **9장을 고친다. 11장은 고치지 않는다.**

**11장이 옳다.** 11장은 등급을 정확히 표시했고 근거 밖으로 나간 곳이 없다. 부정확한 쪽은 **11장의 근거 상태를 미리 요약한 9장**이다. 3파 로그 2021~2023행이 §7-4에서 확인한 것과 같은 유형이다 — **파생 서술이 원본보다 한 칸 높게 말한 경우.**

**정정안 (9장 `09_final.md:55` 마지막 문장, 조사 하나):**

- **[현행]** "그쪽은 초록과 수치까지 확인한 근거이고, 이쪽은 아직 이름뿐이다."
- **[정정 A — 최소 수정, 권장]** "그쪽**에는** 초록과 수치까지 확인한 근거**가 있고**, 이쪽은 아직 이름뿐이다."
- **[정정 B — 더 정확]** "그쪽**에는 초록과 수치까지 확인한 근거가 섞여 있고**, 이쪽은 아직 이름뿐이다."

**정정 A만으로 충분한 이유:** 전칭(∀)을 존재 양화(∃)로 낮추면 문장이 참이 된다. Gordon 2023 하나만으로도 "초록과 수치까지 확인한 근거가 있다"는 성립하고, 9장이 실제로 하려던 비교 — **초록을 아예 확보하지 못한 Lemon & Verhoef와의 대비** — 는 조금도 약해지지 않는다. 11장 43행의 "나란히 놓되 매번 표시한다"와도 충돌하지 않는다.

**차단 여부: 없음.** 사실 오류이되 조사 단위이고, editor 통합 단계에서 처리하면 된다. **다만 저술가 재량으로 덮을 항목은 아니다** — 한 장이 다른 장의 근거 등급에 대해 한 사실 주장이고, 11장 본문이 그것을 부인하기 때문이다.

### ④ 부수 확인 — 9장이 11장에 건 나머지 예고

| 9장 예고 | 11장 이행 | 판정 |
|---|---|---|
| "이 채용 지형이 커리어 선택에 무엇을 뜻하는지는 **12장**에서 다시 본다"(9:119) | 12장 15~44행이 채용 지형을 통째로 받음 | ✅ (12장 이행) |
| "어느 쪽에 앉을 것인가는 **12장**의 질문이다"(9:176) | 12장 136~138행 인하우스 vs 벤더 대비 | ✅ |
| "야간 발송처럼 법이 직접 걸리는 제약은 **10장**에서 조문과 함께 본다"(9:172) | 10장 123~131행 제50조 제1·3·8항 + **마커 해소로 시행령 제61조까지 확보** | ✅✅ **9장 172행을 낮출 필요 없음** |
| "이 관문들의 법적 근거는 **10장**에서 정리한다"(9:29) | 10장 105~135행 | ✅ |

**10~12장이 앞 장의 예고 5건을 전부 회수했다. 미이행 0건.**

---

## 금지 항목 스캔 결과 (4파)

`chapters/10_draft.md` · `11_draft.md` · `12_draft.md` 전문에 대해 계획서 §A 13항목 + 서지 함정 2건 + 범위 한정 3건 + §B 시점 병기를 **문자열 단위로 전수 스캔**했다.

### 계획서 §A 인용 금지 13항목 — **위반 0건**

| # | 금지 항목 | 10장 | 11장 | 12장 | 판정 |
|---|---|:--:|:--:|:--:|---|
| 1 | CDP 4분류(Data/Analytics/**Campaign**/**Delivery**) | 0 | 0 | 0 | ✅ 두 단어 모두 문서 전체 0회 |
| 2 | "DMP = 서드파티 쿠키 / CDP = 퍼스트파티" | 0 | 0 | 0 | ✅ `DMP` 문자열 0회 |
| 3 | CEM / CXM 비교표 | 0 | 0 | 0 | ✅ 두 약어 모두 0회 |
| 4 | CDP Institute 기관 정의문 | 0 | 0 | 0 | ✅ 0회 |
| 5 | ADH 20/50/10을 타 클린룸에 전용 | 0 | — | — | ✅ 수치는 ADH에만, AWS 서술에 숫자 0개 (⚠️ 방어 문장 보강 권고는 별건) |
| 6 | **PIPA 과징금 % (3% / 10%)** | **0** | — | — | ✅✅ 숫자 0개 + 과징금/과태료 분리 명시 + 부재 사유 서술 |
| 7 | **정보통신망법 "매출액 6%"** | **0** | — | — | ✅ `매출액` 0회 · `6%` 실질 0회(11장 `176%` 부분일치만) |
| 8 | **SKAdNetwork 세부** | **0** | 0 | 0 | ✅ 문자열 자체가 0회 |
| 9 | Snowplow / RudderStack / Redis "오픈소스" 단정 | 0 | 0 | **0** | ✅ 12장의 두 언급(86·88행)은 **"저장소"로만 지칭**, 라이선스 단어 없음. 11장 144행의 "오픈소스 MMM"은 Meridian·Robyn 대상이며 `papers.md:448`·`:468`이 같은 표현을 쓴다 |
| 10 | HLL·Bloom filter 수치를 원 논문에 귀속 | 0 | 0 | 0 | ✅ `HyperLogLog`·`0.81`·`12KB`·`14.378` 전부 0회 |
| 11 | **Gordon 2019에 수치 귀속** | — | **0** | — | ✅✅✅ `2019` 문자열 0회 — 논문 자체가 미등장 |
| 12 | **LLM 카피 효과 크기** | 0 | 0 | 0 | ✅ `LLM` 0회 |
| 13 | DMARC를 "표준"이라 부르기 | 0 | 0 | 0 | ✅ `DMARC` 0회. `표준` 7회는 전부 "표준 해법"·"표준 문서"·"표준 참조 문헌" 일반어 |

### 서지 함정 2건 — **위반 0건**

| 함정 | 결과 |
|---|---|
| Theta Sketch 저자 오귀속(Stokes·Tirthapura) | ✅ `Theta`·`Stokes`·`Tirthapura` 전부 0회 |
| C-Store 원본 DOI(`10.1145/3226595.3226638`) | ✅ `3226595` 0회 |

### 범위 한정 3건 — **전건 이행** (계획서 §212~215)

| 인용 | 장 | 한정 위치 | 판정 |
|---|---|---|---|
| **Goldfarb & Tucker (2011)** | 10장 | 인용 **직후 문단 첫머리** — 구매 의향/온라인 디스플레이 광고/일반화 금지 3요소 | ✅✅ |
| **Berman (2018)** | 11장 | 조건절이 **인용문 안 + 해설 문단** 두 곳 / 강도 희석 방지도 별도 문단 | ✅✅ (양방향) |
| **Blake et al. (2015)** | 11장 | 3요소 번호 매겨 나열 + **"eBay라는 이미 강한 브랜드"** 별도 문단 + 오축약 명시 기각 | ✅✅ |

### §B 시점 병기 — **해당 항목 전건 이행**

| 요구 | 결과 |
|---|---|
| **채용 공고 수치 — "2026년 7월 원티드 active 공고 기준"을 문장 안에** | ✅ 12:19(AB180)·12:52(빅인사이트) 두 곳 모두 |
| 해외 공고 조회 시점 | ✅ 12:23 "2026년 7월 25일에 조회했을 때" |
| **Privacy Sandbox "2026년 7월 기준"** | ✅ 10:13 절 첫머리 |
| **EU AI Act "2026년 7월 기준"** | ✅ **의도적 미사용** — `AI Act` 0회. `web_privacy.md:640~648`의 4중 경고를 감안하면 최선의 선택 |
| Tier 2 버전·수치 미사용 | ✅ Redpanda·Pulsar·Snowflake·Airflow 전부 0회 |
| Raab 정의 연도 병기 | ✅ 해당 없음 (`Raab` 0회) |
| 날짜 없는 벤더 문서 조회일 병기 | ✅ 10장 5건(ATT·GTM·Meta·Consent Mode·CA AG)·12장 1건(AB180 블로그 "게시일 미상") |

### `(사실 확인 필요)` 마커

| 파일 | 잔존 | 상태 |
|---|:--:|---|
| `10_draft.md` | **1** | **위 「마커 해소」 섹션의 조치안으로 삭제 예정 — 저술가 이행 대기** |
| `11_draft.md` | 0 | — |
| `12_draft.md` | 0 | — |

**Phase 5 차단 항목: 이 마커 1건이 유일하며, 조치안이 실행 가능한 형태(교체 문장 전문)로 제시돼 있다.**

### 의심 식별자 스캔 — **0건**

- **DOI 14건**(11장) 전수 대조 — `papers.md`에 전건 존재, 형식 이상 0건.
- **arXiv ID 1건** — `2201.07055`. YYMM = **2201(2022년 1월)**, 빌드 시점(2026-07) 기준 과거 → **미래 날짜 자동 ❌ 규칙 비해당.** `papers.md:517`·`:1194`·`:1333` 3곳에 존재.
- **HN 댓글 ID 8건**(10장 3 / 11장 4 / 12장 1) — `community.md`에 ID·작성자·날짜 전건 일치.
- **법령 식별자 4건** — 법률 제20897호·제21305호·시행 2025-10-02·시행 2026-07-07. `web_privacy.md:779`·`:785`에 law.go.kr 출처와 함께 전건 존재.
- **해석되지 않는 URL·"너무 깨끗한" 인용 0건.**

**4파 웹 2차 에스컬레이션: 1건**(정보통신망법 시행령 제61조 — 마커 해소). 그 외 전건 레퍼런스 1차 대조로 판정했다.

---

## 4파(10~12장) 종합

### 장별 판정

| 장 | 주장 | ✅ | ⚠️ | ❌ | 🕒 | 판정 |
|---|---|---|---|---|---|---|
| 10장 | 37 | 36 | 1 | 0 | 0 | 통과 (마커 해소 필요) |
| 11장 | 28 | 26 | 2 | 0 | 0 | 통과 |
| 12장 | 26 | 24 | 2 | 0 | 0 | 통과 |
| **계** | **91** | **86** | **5** | **0** | **0** | **❌·🕒 0건** |

*11장 ⚠️ 2건 중 1건은 9장 정정 항목(장 간 정합)이라 11장 본문 수정은 1건이다.*

### ❌ / 🕒 목록 — **둘 다 0건**

**4파에는 사실 오류도 검증 불가 항목도 없다.** 3파에 이어 두 파 연속이다.

### Phase 5 차단 항목 — **1건 (조치안 완비)**

`10_draft.md:127`의 `(사실 확인 필요 — 시행령의 면제 매체 범위)` 마커. **웹 2차 검증으로 해소됐다** — 시행령이 정한 면제 매체는 **전자우편**이고 **앱 푸시는 비면제**다. 교체 문장 전문과 **본문에 쓰면 안 되는 것 3가지**(알림톡 열거·문자 열거·조항 번호)가 「마커 해소」 섹션에 있다. **저술가가 그 문단을 교체하면 차단이 풀린다.**

### 반영 권고 5건 (전부 ⚠️, 문장·괄호 단위)

| # | 위치 | 내용 | 성격 |
|---|---|---|---|
| 1 | `10_draft.md:127` | 마커 문단 교체 | **필수 (BLOCKING)** |
| 2 | `10_draft.md:187` | Ads Data Hub 임계값에 "다른 제품 전용 금지" 한 문장 삽입 | 권고 (3파 로그 명시 지시) |
| 3 | `11_draft.md:25`(+39) | "거의 모든 도구의 기본값" → "오랫동안 기본값 자리를 지켜왔다" | 권고 (③형) |
| 4 | `12_draft.md:113` | "3위와 4위 … 코딩 역량보다 위" → 별 등급 프레임으로 교체 | 권고 (③형·자기모순) |
| 5 | `12_draft.md:144~148` | 커뮤니티 인용 4건에 HN ID·날짜 추가 (ID 전부 제공됨) | 권고 (서지 일관성) |
| 6 | `09_final.md:55` | "그쪽은 …이고" → "그쪽에는 …가 있고" | **필수 (장 간 사실 정합)** |

---

## 전권 사실 규율 총평 (1~12장)

### 전권 집계

| 파 | 장 | 주장 | ✅ | ⚠️ | ❌ | 🕒 | BLOCKING |
|---|---|---|---|---|---|---|---|
| 1파 | 01~03 | 69 | 58 | 5 | **2** | **4** | ❌ 2 · 🕒 4 |
| 2파 | 04~06 | 67 | 56 | 11 | 0 | 0 | 없음 |
| 3파 | 07~09 | 66 | 61 | 5 | 0 | 0 | 없음 |
| **4파** | **10~12** | **91** | **86** | **5** | **0** | **0** | **마커 1건(해소됨)** |
| **전권** | **12장** | **293** | **261** | **26** | **2** | **4** | **1파 6건 + 4파 마커 1건** |

**✅ 비율 89.1%. ❌·🕒는 전권 6건이고 전부 1파(1~3장)에 있다. 4~12장 아홉 장에서 사실 오류 0건.**

### 궤적 — 이 하네스에서 관측된 가장 뚜렷한 학습 곡선

| 지표 | 1파 | 2파 | 3파 | 4파 |
|---|:--:|:--:|:--:|:--:|
| ❌ + 🕒 | **6** | 0 | 0 | **0** |
| ⚠️ | 5 | **11** | 5 | 5 |
| 금지 항목 위반 | 있음 | 0 | 0 | **0** |
| 미해소 마커 | — | — | 0 | **0** (해소) |

1파의 ❌ 두 건은 **표본을 숫자로 압축한 것**(03장 "20곳 중 넷")과 **한 소스의 인용을 인접 제품에 전용한 것**(01장 노티플라이→FlareLane)이었다. **두 형태 다 이후 아홉 장에서 한 번도 재발하지 않았다.** 특히 4파에서는 저술가들이 그 실패를 **반대 방향으로 과잉 방어**했다 — 12장 21행이 채용 비율에 세 겹 단서를 붙였고, 10장 187행이 임계값을 한 제품에만 묶었다.

### 이 책이 만들어낸 다섯 가지 사실 규율 장치

전권을 통과하며 반복 관측된, **이 책 고유의 서술 장치**다. 전부 4파에서도 작동했다.

1. **미확인을 부재로 읽지 않게 막는 마지막 문장.** 07:122("없다는 뜻이 아니라 확인하지 못했다는 뜻이다") → 10:119("상한 비율은 자료마다 숫자가 달라 원문을 확인하기 전까지 적지 않는다") → 11:113("독립 정전 논문은 특정되지 않았다") → 12:117("면접 자료를 확보하지 못했다"). **전권 최소 12회.**
2. **한 벤더의 수치를 그 벤더에 묶는 문장.** 07:112(Bloomreach 64)이 정본. 10:187이 이 패턴의 유일한 미이행 자리이고, 그래서 ⚠️로 남았다.
3. **금지된 문장을 본문에 인쇄한 뒤 기각하기.** 10:201("'개인화는 역효과다'로 넓히면 논문이 말하지 않은 것을 말하게 된다") · 11:33("'라스트터치는 부정확하다'와 '안 쓰느니만 못하다'는 다른 층위") · 11:87("'온라인 광고는 효과가 없다'는 1번만 떼어낸 문장") · 12:117("'면접에서 이게 나온다'로 읽으면 없는 근거를 만드는 일"). **오용을 이름 붙여 무력화하는 형태이고, 10·11·12장이 독립적으로 같은 형태에 도달했다.**
4. **확인 수준을 한 칸 내려 말하기.** 08장의 Covington 강등에서 시작해 4파에서 6회 관측 — 10:47·10:103·10:185·10:35(범위 축소)·11:61(원본이 단정한 배수를 책의 계산으로 강등)·12:52. **반대 방향(올려 말하기)은 전권 통틀어 0건이다.**
5. **표본 편향을 자발적으로 고지하기.** 09:89에서 시작해 **12:13에서 장 전체의 설계 원리로 승격**했다 — 소스 세 종류의 약점을 각각 밝히고, "'업계는 이렇다'는 문장이 거의 없는 이유가 그것이다"까지 적었다.

### 남은 위험 — editor·manuscript-reviewer가 통합 단계에서 확인할 것

1. **`10_draft.md`의 마커 1건.** 통합 원고에 `(사실 확인 필요)`가 한 글자라도 남으면 Phase 4.5에서 잡힌다. **교체 문장은 준비돼 있다.**
2. **9장 55행의 전칭 표현.** 11장이 그 문장을 부인하는 구조다. 조사 하나 수정.
3. **1파의 ❌ 2건 반영 여부.** 01장 노티플라이/FlareLane 분리, 03장 "20곳 중 넷" 제거 — **`{NN}_final.md`에 반영됐는지 통합 전 재확인 필요.** 4파에서는 확인하지 않았다.
4. **3파 로그 F절의 미이행 항목 1건.** Kafka 원 논문의 위상(NetDB'11 워크숍, DOI 없음)을 4장 표가 "5장"에서 다룬다고 예고했는데 5장에 없다. **10~12장에서도 해소되지 않았다**(세 장 모두 Kafka 원 논문을 언급하지 않는다). 4장 표의 포인터를 고치거나 5장에 한 문단을 넣어야 하며, 그대로 두면 **상호참조 오류로 Phase 4.5에서 잡힌다.**
5. **장 간 수치 충돌: 없음.** 4파가 재사용한 앞 장 수치(ClickHouse 8192, ITP 7일, 429/목적지 제약, all-zero IDFA, 4장 표 행 번호)는 전부 원본 및 해당 장과 일치했다.

### 최종 판정

**12장 전체에 대해 사실 정확성 관점의 Phase 5 차단 항목은 `10_draft.md`의 마커 1건뿐이며, 그 해소안이 이 로그에 실행 가능한 형태로 있다.** 그 문단을 교체하면 **전권에 미해소 `(사실 확인 필요)` 마커가 0건이 된다.**

**미해소(위험) 항목: 없음.** 4파의 ⚠️ 5건은 전부 문장 단위 교체로 끝나고, 저술가와의 왕복 없이 확정 가능한 구체안이 제시돼 있다.

*4파 검증 종료. 검증자: fact-checker / 2026-07-25~26 / 웹 2차 에스컬레이션 1건.*
