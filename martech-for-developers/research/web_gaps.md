<!-- 검색 시점: 2026-07-25 기준 -->

# 카테고리 정의·아이덴티티 갭 필러 리서치 (web #4)

검색 수행일: **2026-07-25**
슬러그: `martech-for-developers` / genre: `tech-book`
역할: 앞선 web #1~#3이 조회 실패로 비워 둔 P0 항목만 표적 보강. 이미 확보된 항목(Insider One 개발자 표면, Segment Spec, Adobe XDM, 20개 벤더 대조표, Hightouch composable CDP 정의, Fivetran→Census, Rokt→mParticle)은 재수집하지 않았다.

## 이 문서를 읽는 규칙 (fact-checker 필독)

이 세션의 도구는 두 종류의 결과를 준다. 둘을 구분하지 않으면 사실 규율이 무너지므로, 모든 항목에 등급을 붙였다.

| 등급 | 의미 | 책에 쓸 수 있는가 |
|------|------|------------------|
| **[FETCHED]** | WebFetch로 해당 URL의 페이지를 실제로 열어 본문에서 가져온 것 | ✅ 인용 가능 |
| **[2차 인용]** | 실제로 fetch한 페이지가 *다른 출처의 문장*을 명시적 귀속과 함께 인용한 것 | ⚠️ 반드시 "A가 인용한 B의 정의" 형태로만 |
| **[검색 요약]** | WebSearch가 돌려준 합성 요약문. 원 페이지를 열지 못함 | ❌ **인용 금지.** 후속 검증 대상 |

> **[검색 요약]은 문장이 그럴듯해도 원문 대조가 안 된 것이다.** 특히 CDP 정의처럼 널리 회자되는 문장은 검색 요약이 기억과 구분되지 않는다. 이 문서에서 [검색 요약]으로 표시된 것은 전부 "아직 확인 안 됨"으로 취급하라.

---

## P0-1. CDP Institute 공식 CDP 정의 — **부분 확보 (2차 인용만) + 1차 대체 확보**

### 결론 요약

- `cdpinstitute.org` **1차 조회 실패 — 사이트 전역 403** (`/wp-content/` PDF 경로까지 포함, 총 4개 URL 시도). 아래 "확인 불가 목록" 참조.
- 대신 **더 나은 것을 얻었다**: CDP라는 용어를 처음 만든 David Raab 본인의 블로그 원문 2건을 fetch했다. 창립자의 1차 서술이므로 기관 페이지보다 서술 가치가 높다.
- 유명한 "packaged software…" 정의는 **2차 인용으로만** 확보했다.

---

### 1-A. [FETCHED] 용어가 처음 만들어진 순간 — Raab, 2013-04-25

- **출처 URL:** http://customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html
- **제목:** "I've Discovered a New Class of System: the Customer Data Platform. Causata Is An Example."
- **저자:** David Raab
- **발행일:** 2013년 4월 25일 (목)
- **신뢰성:** 최상 (용어 창시자의 1차 기록)
- **[출처 URL | 발행일 2013-04-25 | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문):**

> "These systems that gather customer data from multiple sources, combine information related to the same individuals, perform predictive analytics on the resulting database, and use the results to guide marketing treatments across multiple channels."

> "I'll step in myself, and hereby christen the concept as 'Customer Data Platform'."

> "systems that closely couple just those features with the goal of feeding data as well as recommendations to execution systems"

**핵심 주장:** 2013년 4월, Raab은 기존 카테고리로 설명되지 않는 시스템군을 발견하고 직접 "Customer Data Platform"이라 명명했다. 최초 정의의 구성 요소는 네 가지 — ① 여러 소스에서 고객 데이터 수집 ② 동일 인물의 정보 결합 ③ 결과 DB 위에서 예측 분석 ④ 다채널 마케팅 처리 안내.

> **책에 쓸 때의 주의:** "2013년에 CDP라는 말이 생겼다"는 이 페이지로 직접 뒷받침된다. `christen`("명명하다")이라는 동사를 본인이 썼다는 점이 서술 포인트다.

**관련 섹션 힌트:** "CDP는 어디서 왔는가" — 카테고리의 탄생을 사람 한 명의 블로그 포스트로 추적할 수 있다는 것 자체가 martech 카테고리가 어떻게 만들어지는지 보여주는 장면.

---

### 1-B. [FETCHED] Raab의 정식화된 정의 — 2015-01-18

- **출처 URL:** http://customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html
- **제목:** "Customer Data Platforms Revisited: The Future of Marketing Data"
- **저자:** David M. Raab
- **발행일:** 2015년 1월 18일 (일)
- **신뢰성:** 최상
- **[출처 URL | 발행일 2015-01-18 | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문):**

> "a marketer-controlled system that builds a multi-source customer database and exposes it to external execution systems"

원래 CDP로 분류했던 벤더군에 대한 서술:

> "B2B predictive lead scoring and customer success management; campaign management with an integrated customer database; and data management platforms to support online advertising"

**핵심 주장:** 2015년 시점 정의의 결정적 단어는 **marketer-controlled**(마케터가 통제하는)다. 기술적 능력이 아니라 *누가 이 시스템을 소유·운영하는가*가 정의에 들어가 있다. 개발자 독자에게 이건 중요한 힌트다 — CDP는 처음부터 "IT가 아니라 마케터가 직접 쓸 수 있는 것"을 겨냥한 카테고리였다.

---

### 1-C. [FETCHED] CDP와 다른 시스템의 관계 — Raab의 벤 다이어그램, 2017-03-23

- **출처 URL:** https://customerexperiencematrix.blogspot.com/2017/03/wondering-how-customer-data-platforms.html
- **제목:** "Wondering How Customer Data Platforms Relate to Other Marketing Systems? Here's a Picture"
- **저자:** David Raab
- **발행일:** 2017년 3월 23일 (목)
- **신뢰성:** 최상
- **[출처 URL | 발행일 2017-03-23 | 검색 시점 2026-07-25]**

**핵심 주장 — 3개 축으로 전 카테고리를 가르는 프레임:**

Raab은 세 가지 기능의 조합으로 카테고리를 구분한다.
1. **Unifying customer data** (고객 데이터를 통합하는가)
2. **Making data accessible to other systems** (다른 시스템이 그 데이터를 읽을 수 있는가)
3. **Selecting messages** (메시지를 고르는가)

| 시스템 | 데이터 통합 | 외부 접근 허용 | 메시지 선택 |
|--------|------------|---------------|------------|
| **CDP** | ✅ | ✅ | ❌ |
| **JOE** (Journey Orchestration Engine) | ✅ | ❌ | ✅ |
| **MDM** (Master Data Management) | ✅ | ❌ | ❌ |
| **MAP** (Marketing Automation Platform) | ❌ | ❌ | ✅ |
| **DMP** | ❌ | ❌ | ✅ |
| **CRM** | ❌ | ❌ | ✅ (영업 중심) |
| **Data Lake** | ❌ | ✅ | ❌ |
| **ECDP** (Enterprise CDP) | — | — | — (IT가 통제하는 CDP 등가물) |

> ⚠️ **이 표는 fetch한 페이지의 서술을 정리한 것이지만, 표 형태는 원문 그대로가 아니라 이 리서처의 재구성이다.** 원문은 벤 다이어그램 이미지와 산문 서술이다. 책에 표로 옮길 때 "Raab의 2017년 벤 다이어그램을 표로 재구성"이라고 명시할 것.

**책에 쓰기 좋은 지점:** 개발자에게 martech 카테고리를 설명할 때 "제품 이름 20개 외우기"가 아니라 **"세 개의 예/아니오 질문"**으로 좌표를 잡아 줄 수 있다. 이 프레임이 그 뼈대가 된다.

**⚠️ 상충 주의:** 이 표는 DMP를 "데이터를 통합하지 않는다"로 분류한다. 그런데 Adobe Audience Manager 공식 문서는 자사 DMP를 "Unifies data into audience profiles"라고 자기 규정한다(P0-2 참조). **애널리스트 분류 vs 벤더 자기 규정의 정면 충돌** — 아래 "상충·불확실 항목" 참조.

---

### 1-D. [2차 인용] 유명한 "packaged software…" 정의 — Informatica가 CDPI에 귀속시킨 문장

- **fetch한 페이지 URL:** https://www.informatica.com/resources/articles/what-is-a-customer-data-platform.html
- **fetch한 페이지 제목:** "Customer Data Platform: Capabilities and Benefits"
- **발행일:** 페이지에 표시 없음 — **확인 불가**
- **신뢰성:** 중 (인용 자체는 fetch됨, 그러나 원 출처인 cdpinstitute.org는 열지 못함)
- **[출처 URL | 발행일 미표기 | 검색 시점 2026-07-25]**

**Informatica 페이지가 fetch된 본문에서 명시적 귀속과 함께 인용한 문장:**

> 귀속 문구: "The Customer Data Platform Institute (CDPI) defines a CDP as…"
> 인용된 정의: **"packaged software that creates a persistent, unified customer database that is accessible to other systems."**

> 🚨 **fact-checker 주의:** 이 문장은 과제 지시문이 명시적으로 경고한 "널리 회자되는 문장"이다. **CDP Institute 원문(cdpinstitute.org)은 이 세션에서 열지 못했다.** 따라서 책에 쓸 때 두 가지 중 하나만 허용된다.
> 1. `(2차 인용)` — "Informatica가 CDP Institute의 정의로 인용한 바에 따르면…"
> 2. 아예 쓰지 말고 **1-A/1-B의 Raab 1차 원문으로 대체** ← **권장**
>
> "CDP Institute는 CDP를 …라고 정의한다"라고 1차 출처인 양 쓰면 안 된다.

**같은 페이지에서 fetch한 카테고리 연대기 서술 (역시 Informatica의 서술, CDPI 아님):**

> "CDPs emerged in the mid-2010s as a way to combine both customer (CRM) and context (DMP)."

또한 이 페이지는 1990년대 CRM이 "helped organizations keep track of information about their known customers"였고, 2000년대 DMP가 조직으로 하여금 "enrich their data with third-party sources"할 수 있게 했다고 서술한다.

> ⚠️ 이 연대기는 벤더 마케팅 페이지의 서술이다. 신뢰성 **중**. 연도 주장의 근거로 단독 사용 금지.

---

### 1-E. [FETCHED] 용어 창시 시점의 교차 확인 — Wikipedia

- **출처 URL:** https://en.wikipedia.org/wiki/Customer_data_platform
- **신뢰성:** 중 (백과사전, 그러나 1-A의 1차 출처와 **일치**하므로 교차 확인 가치 있음)
- **[출처 URL | 발행일 미상(위키) | 검색 시점 2026-07-25]**

**fetch한 본문 인용:**

> "In April 2013, marketing technology analyst David Raab coined the term 'Customer Data Platform.'"

> CDP vs DMP 구분: "a CDP collects, stores, models, and activates first-party customer data" / "a data management platform (DMP) is a data onboarding system that provides access to large, anonymous third-party datasets to enrich or target new audiences."

**교차 확인 결과:** "2013년 4월"이 1-A에서 fetch한 Raab 블로그 원문의 발행일(2013-04-25)과 **정확히 일치**한다. → **"CDP라는 용어는 2013년 4월 David Raab이 만들었다"는 서술은 1차 출처로 뒷받침된 사실로 취급 가능.** ✅

**CDP Institute 창립 연도:** 이 페이지에는 없음. "Interest in the category increased following 2016"만 있음. → **창립 연도 확인 불가.**

---

## P0-2. DMP / CRM / MA / CEM의 정의와 역사

> **총평:** 이 항목은 **부분 확보**다. DMP와 CRM은 벤더 1차 문서로 확보했다. **MA와 CEM은 1차 문서 확보에 실패했다.** 각 카테고리의 "등장 시점" 근거는 대부분 확보하지 못했다 — 아래에 정직하게 표시한다.

---

### 2-A. DMP (Data Management Platform) — **확보 (Adobe 공식 문서 2건)**

#### [FETCHED] Adobe Experience Platform — DMP destinations overview

- **출처 URL:** https://experienceleague.adobe.com/en/docs/experience-platform/destinations/catalog/data-management/overview
- **제목:** "Data Management Platform (DMP) destinations overview | Adobe Experience Platform"
- **최종 갱신일:** **2026년 5월 23일** (페이지 표기)
- **신뢰성:** 최상 (벤더 공식 제품 문서)
- **[출처 URL | 갱신일 2026-05-23 | 검색 시점 2026-07-25]**

**인용 가능한 구절:**

> DMP는 "enable advertisers, publishers, and agencies to build unique audience profiles, identify their most valuable segments, and use them across any digital channel."

**주의:** 이 페이지는 쿠키·익명 데이터·서드파티 데이터를 **정의의 구성 요소로 명시하지 않는다.** "audience profiles", "segments"라는 표현은 나오지만 "서드파티 쿠키 기반"이라는 서술은 **이 페이지에 없다.**

#### [FETCHED] Adobe Audience Manager Overview

- **출처 URL:** https://experienceleague.adobe.com/en/docs/audience-manager/user-guide/overview/aam-overview
- **제목:** "Audience Manager Overview | Adobe Audience Manager"
- **최종 갱신일:** **2026년 5월 21일**
- **신뢰성:** 최상
- **[출처 URL | 갱신일 2026-05-21 | 검색 시점 2026-07-25]**

**인용 가능한 구절:**

> "Unifies data into audience profiles, giving you a complete customer view across devices and channels. Create look-alike models, build audience segments and groups of profiles, and supplement with second- and third-party data sources."

**확보된 사실:**
- AAM은 **퍼스트파티 데이터**를 web analytics·CRM·device data·e-commerce 등 여러 채널에서 수집한다.
- **세컨드파티·서드파티 데이터 소스로 보강**할 수 있다 ← 이건 원문에 명시적으로 있다. ✅
- **look-alike 모델링**이 명시적 기능으로 나온다. ✅

**⚠️ 확보 실패:** 이 페이지에는 **쿠키·디바이스 ID·익명 프로필에 대한 언급이 없다.** 따라서 **"DMP는 서드파티 쿠키 기반이다"라는 문장을 Adobe 공식 문서로 뒷받침할 수 없다.**

> 🚨 **fact-checker 필독:** "DMP = 서드파티 쿠키 기반, 익명 세그먼트" 는 업계에서 사실상 상식이지만, **이 세션에서 1차 벤더 문서로 확인하지 못했다.** 가장 가까운 fetch된 근거는 Wikipedia(1-E)의 "large, anonymous third-party datasets"뿐이다. 책에 이 대비를 쓸 거라면 Wikipedia 수준 근거임을 인지하고, IAB 원문이나 Google/LiveRamp 문서로 **추가 검증이 필요**하다.

#### [실패] IAB Data Usage & Control Primer (2013) — 퍼스트/세컨드/서드파티 데이터 정의

- **시도 URL:** https://www.iab.com/wp-content/uploads/2015/04/IABDataPrimerFinal.pdf
- **결과:** PDF가 **바이너리/압축 스트림으로 반환되어 본문 텍스트 추출 실패.** 메타데이터상 2013년 작성 PowerPoint 기반 PDF라는 것만 확인됨.
- **판정:** **확인 불가 (본문 미조회)** — 이 문서에서 퍼스트/세컨드/서드파티 데이터 정의를 인용하지 마라.
- **후속 리서처 힌트:** 파일은 로컬에 저장됨. PDF 텍스트 추출 도구(`pdftotext` 등)로 재시도하면 확보 가능할 수 있다. IAB는 이 주제의 최적 1차 출처다.

---

### 2-B. CRM — **부분 확보 (Salesforce Trailhead 1차 문서). 기원·연도는 확인 불가**

#### [FETCHED] Salesforce Trailhead — Salesforce CRM Basics

- **출처 URL:** https://trailhead.salesforce.com/content/learn/modules/lex_implementation_basics/lex_implementation_basics_welcome
- **모듈명:** "Salesforce CRM Basics"
- **발행일:** 페이지 표기 없음 — **확인 불가**
- **신뢰성:** 최상 (벤더 공식 학습 문서)
- **[출처 URL | 발행일 미표기 | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문):**

> "CRM stands for Customer Relationship Management. This technology allows you to manage relationships with your customers and prospects and track data related to all of your interactions."

> CRM은 "helps teams collaborate, both internally and externally, gather insights from social media, track important metrics, and communicate via email, phone, social, and other channels."

**개발자에게 결정적인 부분 — CRM의 데이터 모델 (fetch한 원문 그대로):**

> - **Accounts:** "Accounts are the companies you're doing business with."
> - **Contacts:** "Contacts are the people who work at an Account."
> - **Leads:** "Leads are potential prospects. You haven't yet qualified that they're ready to buy or what product they need."
> - **Opportunities:** "Opportunities are qualified leads that you've converted. When you convert the Lead, you create an Account and Contact along with the Opportunity."

**관련 섹션 힌트 — 이게 이 리서치에서 가장 쓸모 있는 발견 중 하나다:**

개발자에게 CRM을 설명하는 가장 빠른 길은 **스키마**다. Account(회사) 1 : N Contact(사람), Lead(미자격 잠재고객)는 별도 테이블에 있다가 자격 검증되면 **Account + Contact + Opportunity 세 레코드로 변환(convert)된다**. 이 "Lead 변환" 모델은 개발자가 처음 보면 이상하게 느끼는 지점이자, CRM이 왜 "고객 DB"가 아니라 "영업 파이프라인 DB"인지 보여주는 핵심이다. B2B 영업 프로세스가 스키마에 그대로 박혀 있다.

#### ❌ CRM 용어의 기원·연도 — **확인 불가**

- 검색 요약은 "1995년에 용어가 공식적으로 만들어졌다"거나 Bob Kestnbaum·Tom Siebel·Gartner Group 등 여러 후보를 나열했고, Salesforce 창업(1999, Marc Benioff)도 언급했다. **그러나 이들 중 어느 것도 1차 출처 페이지를 열어 확인하지 못했다.** 출처도 전부 서드파티 블로그(fitsmallbusiness, insightly, crmswitch 등)였다.
- `https://www.salesforce.com/crm/what-is-crm/` → **HTTP 403.**
- **판정: 확인 불가.** **CRM 용어가 만들어진 연도·인물을 책에 단정적으로 쓰지 마라.** 검색 요약 자체가 "누가 만들었는지 논쟁이 있다"고 말한다는 점만이 확인된 사실에 가깝고, 그마저도 1차 확인이 안 됐다.

#### 🇰🇷 한국식 "CRM 마케팅" 용법 — ✅ **확인됨 (한국어 소스 2건 fetch)**

> **이건 이번 리서치에서 대상 독자(한국 개발자)에게 가장 중요한 발견 중 하나다.** 한국에서 "CRM 마케팅"이라는 말은 Salesforce식 CRM(영업 파이프라인 관리)과 **다른 것을 가리킨다.**

##### [FETCHED] 노티플라이(Notifly) — "CRM 마케팅이란? 연차별 CRM 마케터 업무 및 역량, 솔루션 비교"

- **출처 URL:** https://blog.notifly.tech/crm-marketing-introduction/
- **저자:** 노티플라이
- **발행일:** **2023년 10월 24일**
- **신뢰성:** 중 (한국 martech 벤더 블로그 — 업계 용법의 증거로는 적절, 중립적 정의로는 아님)
- **[출처 URL | 발행일 2023-10-24 | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문 그대로):**

> CRM 마케팅이란 "고객이 자사 플랫폼(서비스)에 유입되었을때, 말을 걸고, 구매를 유도하고, 구매한 이후 재탐색을 유도하는 등, **리텐션을 높이는 모든 고객대상 마케팅**"

**채널 (fetch한 원문):**
> "푸시, 모달(IAM), 카카오 알림톡, 카카오 친구톡, 문자 메시지, 이메일 - 총 6가지가 대표적인 매체"

##### [FETCHED] FlareLane — "CRM 마케팅이란 무엇일까? 개념, 활용 전략 비교"

- **출처 URL:** https://blog.flarelane.co.kr/what-is-crm-marketing-concepts-strategies-and-common-mistakes/
- **발행일:** **2025년 4월 22일**
- **신뢰성:** 중 (한국 martech 벤더 블로그)
- **[출처 URL | 발행일 2025-04-22 | 검색 시점 2026-07-25]**

**인용 가능한 구절:**

> CRM 마케팅은 "고객 관리와 데이터 분석을 통해 고객 가치를 극대화하는 전략입니다. 신규 고객을 유치하고 기존 고객의 충성도를 높이는 것을 목표로 하며"

**현장에서 자주 하는 실수 (fetch한 원문 — 챕터 오프닝 소재로 좋다):**
1. **데이터 분석 부족** — "고객 데이터를 수집했지만 단순히 이름이나 이메일만 확인한 뒤 무작정 일괄적인 마케팅 메시지를 발송"
2. **과도한 메시지 발송** — "푸시 알림을 과도하게 발송해 고객을 괴롭힙니다"
3. **단기 성과 집중** — 재구매 유도 전략 없이 할인만 반복
4. **수동 데이터 관리** — 엑셀로 일일이 입력하며 오류 발생
5. **고객 피드백 무시**

##### 🎯 이 발견의 의미 (책에 반드시 반영할 것)

| | **영미권 "CRM"** [FETCHED: Salesforce Trailhead] | **한국 "CRM 마케팅"** [FETCHED: 노티플라이·FlareLane] |
|---|---|---|
| 핵심 대상 | **영업(sales)** — Lead → Opportunity 파이프라인 | **리텐션** — 기존 고객 재구매·재방문 |
| 주 사용자 | 영업사원 | 마케터(그로스) |
| 대표 행위 | 레코드 관리·상담 이력·딜 관리 | **메시지 발송** (푸시·알림톡·문자·이메일) |
| 핵심 객체 | Account / Contact / Lead / Opportunity | 세그먼트 / 캠페인 / 메시지 |
| 서구 대응 카테고리 | CRM | **오히려 MA·CEP(고객 인게이지먼트 플랫폼)에 가깝다** |

> **개발자 독자에게 이건 함정이다.** 한국 회사에서 "CRM 팀"이 요구사항을 들고 오면, 그들이 원하는 건 Salesforce가 아니라 **푸시·알림톡 발송 시스템**일 가능성이 높다. 같은 세 글자가 태평양을 건너면서 뜻이 바뀌었다.
>
> ⚠️ **단, 신뢰성 등급 주의:** 두 출처 모두 **한국 martech 벤더의 자사 블로그**다. 업계에서 그 말이 그렇게 쓰인다는 *용법의 증거*로는 충분하지만, 중립적 정의로 인용하면 안 된다. 책에는 **"국내 CDP/메시징 벤더들은 이 말을 …라는 뜻으로 쓴다"**는 형태로 쓸 것. 카카오 알림톡이 채널 목록 상위에 오는 것 자체가 한국 시장 고유성의 증거다.

---

### 2-C. MA (Marketing Automation) — ✅ **확보 (Salesforce Trailhead 1차 문서 2건, 우회 성공)**

> 💡 앞선 시도들(`business.adobe.com` 타임아웃, Marketo 문서의 정의가 영상에만 존재)이 실패한 뒤 **Trailhead 경로로 우회해 확보했다.**

#### [FETCHED] Trailhead — "Beginner's Guide to B2B Marketing Automation" / Get Started with Account Engagement

- **출처 URL:** https://trailhead.salesforce.com/content/learn/modules/pardot-basics-lightning/get-started-with-pardot-lightning
- **모듈명:** "Beginner's Guide to B2B Marketing Automation" (유닛: Get Started with Account Engagement)
- **발행일:** 페이지 표기 없음 — **확인 불가. 조회 2026-07-25 기준.**
- **신뢰성:** 최상 (벤더 공식 학습 문서)
- **[출처 URL | 발행일 미표기 | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문 그대로):**

> "Marketing Cloud Account Engagement is Salesforce's **B2B marketing automation** solution."

> "If you're a business with marketing and sales teams that work to drive pipeline and grow revenue, Account Engagement can **automate your marketing activities and unite your marketing and sales departments** so that they can work better together."

**핵심 개념 — 개발자가 스키마로 이해할 수 있는 부분 (fetch한 원문):**

> **Prospect:** "An anonymous visitor that has converted and is now identified. A record of the prospect will exist in Account Engagement, **similar to a lead record in Sales Cloud or other CRMs**."

> **Score:** "A prospect's score is a **numerical value** indicating how interested they are in your product or service."

> **Grade:** "A prospect's grade is represented by a **letter (A, B, C, D, etc.)**. It indicates how closely a prospect fits the profile of your **ideal prospect**."

> **Lead Qualification:** "The process of finding the gold needles in the haystack of prospects"

> 🎯 **책에 쓰기 좋은 지점 — score와 grade는 축이 두 개다.** 개발자에게 이건 즉시 이해된다: **score = 행동(얼마나 관심을 보였나, 숫자)**, **grade = 속성(우리 이상적 고객상에 얼마나 맞나, 등급)**. 행동 데이터와 속성 데이터를 **일부러 분리해서** 각각 채점하고 둘을 조합해 영업에 넘긴다. "리드 스코어링"이 단일 점수라고 생각하면 이 설계를 놓친다.
>
> 그리고 **"anonymous visitor가 converted되어 identified된다"**는 서술은 P0-3의 익명→식별 전환과 정확히 같은 문제다. MA 제품도 아이덴티티 문제를 자기 방식으로 풀고 있다.

#### [FETCHED] Trailhead — Integrate Lead Nurturing Into Your Marketing Strategy

- **출처 URL:** https://trailhead.salesforce.com/content/learn/modules/pardot-lead-nurturing-lightning/integrate-lead-nurturing-into-your-marketing-strategy
- **모듈명:** "Integrate Lead Nurturing Into Your Marketing Strategy"
- **발행일:** 페이지 표기 없음 — **확인 불가. 조회 2026-07-25 기준.**
- **신뢰성:** 최상
- **[출처 URL | 발행일 미표기 | 검색 시점 2026-07-25]**

**리드 너처링의 정의 (fetch한 원문 그대로):**

> "The process of developing and maintaining relationships with customers at every stage of their journey, usually through marketing and communication messaging."

**자동화 트리거 (fetch한 원문):**

> Account Engagement는 "automates lead nurturing by **triggering emails based on a person's behavior or a preset time interval**."

**주의 (fetch 결과의 정직한 보고):** 이 모듈 본문에는 "B2B", "buyer journey", "drip campaign"이라는 표현이 **나오지 않는다.** Engagement Studio가 주 자동화 도구로 제시된다. → "MA = drip campaign"이라는 통념을 이 문서로 뒷받침하지 마라.

**✅ 확보된 것 / ❌ 여전히 확인 불가:**

| 항목 | 상태 |
|------|------|
| 마케팅 자동화(B2B) 정의 | ✅ Salesforce 1차 문서로 확보 |
| 리드 스코어링(score/grade 2축) | ✅ 확보 |
| 리드 너처링 정의 | ✅ 확보 |
| "B2B 중심" 특성 | ✅ 확보 ("Salesforce's B2B marketing automation solution") |
| Pardot → Account Engagement 개명 | ⚠️ 문서가 "Marketing Cloud Account Engagement"를 쓰고 URL에 `pardot`이 남아 있음. **개명 시점은 확인 불가** — Data 360 건과 동일하게 처리할 것 |
| Marketo / HubSpot / Eloqua 출시 연도 | ❌ **확인 불가** |
| MA 카테고리 등장 시점 | ❌ **확인 불가** |

**보조 근거 (1-B에서 fetch됨):**
Raab의 2015년 글은 원래 CDP 후보군에 "B2B predictive lead scoring and customer success management"를 포함시켰다. → **B2B 리드 스코어링이 2015년 시점에 독립된 시스템 카테고리로 존재했다**는 것은 1차 출처로 확인된다. ✅

---

### 2-D. CEM / CXM (Customer Experience Management) — ❌ **확인 불가**

- **시도:** `https://www.gartner.com/en/information-technology/glossary/customer-experience-management-cem` → **HTTP 403.**
- 검색 요약은 Gartner 정의를 "the practice of designing and reacting to customer interactions to meet or exceed their expectations, leading to greater customer satisfaction, loyalty and advocacy"로 제시했으나, **원 페이지를 열지 못했다.**
- **판정: 확인 불가. 이 정의를 Gartner에 귀속시켜 인용하지 마라.**
- 다른 1차 후보(Adobe·SAP 공식 CEM 정의)는 이 세션에서 시도하지 못했다.

---

### 카테고리 비교축 정리표 (개발자용)

> ⚠️ **이 표는 합성물이다.** 각 셀의 근거 등급이 다르다. 셀마다 근거를 표시했다. 표 전체를 하나의 출처에서 온 것처럼 인용하지 마라.

| 축 | **CRM** | **DMP** | **CDP** | **MA** | **CEM/CXM** |
|----|---------|---------|---------|--------|-------------|
| **누구의 데이터인가** | 퍼스트파티 (자사가 입력) `[FETCHED: Trailhead]` | 퍼스트파티 + **세컨드·서드파티 보강** `[FETCHED: Adobe AAM]` | 퍼스트파티 `[FETCHED: Wikipedia — 신뢰성 중]` | 퍼스트파티 (자사 사이트 방문자→prospect) `[FETCHED: Trailhead]` | 확인 불가 |
| **식별 수준** | **식별된 개인/회사** (Account·Contact 레코드) `[FETCHED: Trailhead]` | 확인 불가 — Adobe 문서에 익명/쿠키 언급 없음. Wikipedia는 "anonymous" `[신뢰성 중]` | 확인 불가 (1차 미확보) | **익명 방문자 → 전환되면 식별된 prospect** `[FETCHED: Trailhead]` | 확인 불가 |
| **주 용도** | **영업 파이프라인 관리** `[FETCHED: Trailhead — Lead→Opportunity 변환]` | **광고 타겟팅·오디언스 세그먼트·look-alike** `[FETCHED: Adobe AAM]` | 데이터 통합 + 외부 시스템에 노출 `[FETCHED: Raab 2015/2017]` | **B2B 리드 너처링 + 스코어링 → 영업에 인계** `[FETCHED: Trailhead]` | 확인 불가 |
| **데이터를 남에게 열어 주는가** | ❌ `[FETCHED: Raab 2017 벤 다이어그램]` | ❌ `[FETCHED: Raab 2017]` ⚠️벤더 자기규정과 충돌 | **✅ 이것이 CDP의 정의적 특징** `[FETCHED: Raab 2015/2017]` | ❌ `[FETCHED: Raab 2017 — MAP]` | 확인 불가 |
| **메시지를 고르는가** | ✅ (영업 중심) `[FETCHED: Raab 2017]` | ✅ `[FETCHED: Raab 2017]` | ❌ `[FETCHED: Raab 2017]` | ✅ **행동 또는 시간 간격으로 이메일 트리거** `[FETCHED: Trailhead]` | 확인 불가 |
| **고유한 점수 체계** | — | — | — | **score(행동, 숫자) + grade(적합도, 문자)** `[FETCHED: Trailhead]` | 확인 불가 |
| **데이터 보존 주체** | 벤더 클라우드 (Salesforce: "stored securely in the cloud") `[검색 요약 — 약함]` | 확인 불가 | **자체 영속 DB 구축** `[2차 인용: CDPI via Informatica]` | 벤더 (Account Engagement 내 prospect 레코드) `[FETCHED: Trailhead]` | 확인 불가 |
| **등장 시점** | 확인 불가 | 확인 불가 | **2013년 4월 명명** `[FETCHED: Raab 원문 + Wikipedia 교차 확인]` ✅ | 확인 불가 | 확인 불가 |

**표의 상태:** CRM·DMP·CDP·MA **4개 열은 1차 문서로 채워졌다.** ❌ **CEM/CXM 열은 통째로 비어 있다 — 이 카테고리를 책의 비교표에 넣지 마라.** 그리고 **"등장 시점" 행은 CDP를 빼면 전부 확인 불가**다. 카테고리 연대기를 서술하려면 추가 리서치가 필요하다.

**🇰🇷 여기에 한 열을 더 붙여야 한다 — 한국의 "CRM 마케팅":** 위 2-B의 대조표 참조. 한국 현장의 "CRM 마케팅"은 이 표의 **CRM 열이 아니라 MA 열 쪽(메시지 발송·리텐션)에 가깝다.** 대상 독자가 한국 개발자인 이상 이 어긋남을 빼놓으면 안 된다.

---

## P0-3. Identity Resolution 벤더 문서 — ✅ **초과 확보 (요구 2개 → 실제 4개 벤더)**

> 이 항목이 이번 리서치의 최대 수확이다. 앞선 리서처가 "가장 어려운 문제"로 지목만 하고 미확보했던 병합 규칙·오병합 방지 장치를 **네 벤더의 공식 문서에서 전부 확보**했다. 네 벤더가 같은 문제를 서로 다른 이름으로 푸는 것을 나란히 놓을 수 있다 — 책의 한 챕터가 통째로 나온다.

---

### 3-A. [FETCHED] Segment — Identity Resolution (GitHub raw 우회 성공)

- **출처 URL (개요):** https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/unify/identity-resolution/index.md
- **출처 URL (규칙):** https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/unify/identity-resolution/identity-resolution-settings.md
- **신뢰성:** 최상 (벤더 공식 문서의 소스 리포지토리)
- **발행일:** 리포지토리 마크다운 — 페이지 내 날짜 표기 없음. **`develop` 브랜치 최신 상태 기준, 조회 2026-07-25**
- **[출처 URL | 발행일 미표기(리포 최신) | 검색 시점 2026-07-25]**

> 💡 **우회 경로 기록:** `segment.com`은 403이지만 **`raw.githubusercontent.com/segmentio/segment-docs/develop/src/...`는 열린다.** 디렉터리 목록은 `github.com/segmentio/segment-docs/tree/develop/src/unify/identity-resolution`로 확인 가능. 후속 리서처는 이 경로를 쓸 것.
>
> 확인된 파일 목록: `index.md`, `identity-resolution-settings.md`, `externalids.md`, `identity-resolution-onboarding.md`, `identity-warehouse.md`, `ecommerce-example.md`, `use-cases.md`, `space-setup.md`, `delete-profile-identifier-api.md`

**인용 가능한 구절:**

> "The Identity Graph merges the complete history of each customer into a single profile, no matter where they interact with your business."

> "Identity Resolution allows you to understand a user's interaction across web, mobile, server, and third-party partner touch-points in real time, using an online and offline ID graph with support for cookie IDs, device IDs, emails, and custom external IDs."

**병합의 세 가지 결과 (fetch한 원문):**
1. **"Create a new profile"** — 매칭되는 식별자가 없을 때
2. **"Add to existing profile"** — 하나의 프로필이 모든 식별자와 매칭될 때
3. **"Merge existing profiles"** — 복수 프로필이 식별자와 매칭될 때

**기본 우선순위 (priority):**
> `user_id`가 1순위, `email`이 2순위, 그리고 "all other identifiers are in alphabetical order beginning from rank 3."

**기본 개수 제한 (limit):**
- `user_id`: **1**
- 그 외 모든 식별자: **5**
- (커스텀 설정 예시로 `email: 1`, `user_id: 2` 같은 조합이 문서에 제시됨)

**충돌 해소 알고리즘 (fetch한 원문 기반 서술):**
어떤 식별자가 최종 프로필에서 자기 limit을 초과하면, 시스템은 priority 순위를 참조한다. 들어온 이벤트의 **낮은 우선순위 식별자가 강등(demote)되고**, 더 높은 우선순위 식별자만으로 매칭을 재평가한다.

**문서에 실린 구체적 예시 (그대로 책에 쓸 수 있는 시나리오):**
> 기존 프로필이 `user_id: abc123`, `email: jane@example1.com`을 갖고 있다. 새 이벤트가 `user_id: abc456`과 **같은 email**을 갖고 들어온다. `user_id`의 limit이 1이고 priority(1위)가 email(2위)보다 높으므로 → **email이 강등되고, 새 `user_id`를 위한 새 프로필이 만들어진다.**

**오병합 방지 — Blocked Values (fetch한 원문):**
기본적으로 차단을 권장하는 값들:
- 0과 대시로만 이루어진 값 (정규식 패턴)
- `-1`
- `null`
- `anonymous`

> 🎯 **책에 쓰기 좋은 지점:** 개발자라면 즉시 이해한다 — **`user_id`에 `"null"` 문자열이 들어가는 순간 전 세계 유저가 한 명으로 합쳐진다.** 이게 martech에서 가장 유명한 사고 유형이고, 벤더들이 기본 차단 목록을 문서 첫 페이지에 두는 이유다.

---

### 3-B. [FETCHED] Adobe Experience Platform — Identity Service & Graph Linking Rules

#### Identity Service 개요

- **출처 URL:** https://experienceleague.adobe.com/en/docs/experience-platform/identity/home
- **제목:** "Identity Service Overview | Adobe Experience Platform"
- **최종 갱신일:** **2026년 6월 18일**
- **신뢰성:** 최상
- **[출처 URL | 갱신일 2026-06-18 | 검색 시점 2026-07-25]**

**인용 가능한 구절:**

> "Identity Service is a service within Experience Platform that links (or unlinks) identities to maintain identity graphs."

> identity graph = **"a collection of identities that represent a single customer."**

> 링크가 만들어지는 조건: "when the identity namespace and the identity values match"

> Identity Service는 조직이 "link disparate identities together, thus giving you with a visual representation of how a customer interacts with your brand across different channels"할 수 있게 한다.

**⚠️ 확인 불가 항목:** 이 페이지는 **결정론적(deterministic)인지 확률론적(probabilistic)인지 명시하지 않는다.** 그래프 크기 제한도 이 페이지에는 **없다.**

#### Identity Graph Linking Rules — **오병합 방지의 핵심 문서**

- **출처 URL:** https://experienceleague.adobe.com/en/docs/experience-platform/identity/features/identity-graph-linking-rules/overview
- **제목:** "Identity Graph Linking Rules | Adobe Experience Platform"
- **최종 갱신일:** **2026년 6월 18일**
- **신뢰성:** 최상
- **[출처 URL | 갱신일 2026-06-18 | 검색 시점 2026-07-25]**

**핵심 개념 — Adobe는 오병합을 "graph collapse"라고 부른다:**

> 문제 상황: "certain data could try to merge multiple disparate profiles into a single profile" — 이를 **"graph collapse"**라 지칭.
> 기능의 목적: "prevent these unwanted merges"

**문서가 열거하는 오병합 유발 시나리오 (fetch한 원문 기반):**

1. **공유 디바이스** — 한 기기에 여러 사용자가 로그인하면 정상적으론 신원이 병합되어 버린다.
2. **가짜 연락처 데이터** — 사용자가 허위 전화번호·이메일을 넣는 경우. 규칙으로 "limit one person to just one CRMID, phone number, and/or email address" 가능.
3. **오류 식별자 값** — `user_null`, `not-specified` 같은 값이 서로 다른 CRMID를 병합시킨다.
4. **과잉 병합 방지** — unique namespace를 설정해 "two disparate person identifiers from merging into one identity graph"를 막는다.

**두 가지 메커니즘 (fetch한 원문):**
- **Unique namespace** — 그래프당 네임스페이스당 신원 1개로 제한
- **Namespace priority** — 프로필 조각 연결 시 네임스페이스 중요도 순위

> 🎯 **Segment와 Adobe가 같은 문제를 같은 방식으로 푼다.** Segment = "priority + limit + blocked values", Adobe = "namespace priority + unique namespace + 오류값 처리". **용어만 다르고 구조가 동일하다** — 개발자 독자에게 "벤더가 달라도 문제는 하나"임을 보여주는 최고의 대조 사례.

---

### 3-C. [FETCHED] mParticle — IDSync

#### IDSync 개요

- **출처 URL:** https://docs.mparticle.com/guides/idsync/introduction/
- **최종 갱신일:** **2026년 7월 16일** (매우 신선)
- **신뢰성:** 최상
- **[출처 URL | 갱신일 2026-07-16 | 검색 시점 2026-07-25]**

**인용 가능한 구절:**

> "IDSync is mParticle's identity resolution framework, enabling you to create a unified view of your customers, with improved data governance, policy, and security."

#### 사용자 식별 절차

- **출처 URL:** https://docs.mparticle.com/guides/idsync/identify-users/
- **신뢰성:** 최상
- **발행일:** 페이지 표기 미확인 — **확인 불가**
- **[출처 URL | 발행일 미확인 | 검색 시점 2026-07-25]**

**identity resolution 3단계 (fetch한 원문):**

1. **Identification request** — "An identification request is made via one of the mParticle platform SDKs or the HTTP API."
2. **Profile matching** — "mParticle iterates through your account's identity priority in ascending order, comparing the identifiers included in the request with each identifier in your identity priority."
3. **Profile return or creation** — 매칭되는 기존 프로필을 반환하거나, 설정된 identity strategy에 따라 새 익명 프로필을 생성한다.

**identity priority의 근거 (fetch한 원문 — 개발자에게 직관적인 설명):**

> "a customer ID or email address is more likely to be unique to a single user than a device ID, because a device ID could be shared by multiple users."

**익명 → 식별 전환 처리 (profile conversion strategy):**

> 익명 브라우징 후 로그인하면 mParticle은 별도 프로필을 만들지 않는다. 대신 "adds the provided login ID to the existing anonymous profile" — 고객 여정 기록이 쪼개지지 않게 한다.

**Login ID 무결성 규칙 (검색 요약 — 원문 미확인, ⚠️ [검색 요약] 등급):**
> "a record with at least one login ID can only be returned if the identify request includes a matching login ID" 및 unique ID 설정 관련 서술은 **검색 요약에서만 나왔고 fetch로 확인하지 못했다.** 인용 전 `docs.mparticle.com/guides/idsync/components/` 또는 `/user-data/` 재조회 필요.

> 🎯 **책에 쓰기 좋은 지점 — 익명→식별 전환은 개발자가 가장 자주 틀리는 곳이다.** 로그인 시점에 (a) 새 프로필을 만들지 (b) 기존 익명 프로필을 승격시킬지의 선택이 데이터 품질을 가른다. mParticle은 이걸 **설정 가능한 "strategy"로 명시적으로 노출**한다 — 즉 벤더도 정답이 하나가 아님을 인정한다는 뜻.

---

### 3-D. [FETCHED] Bloomreach — Hard ID / Soft ID

#### Customer identification

- **출처 URL:** https://documentation.bloomreach.com/engagement/docs/customer-identification
- **제목:** "Customer identification"
- **최종 갱신:** 페이지에 **"9 days ago"(상대 표기)** — 절대 날짜 미표기. 조회 시점 2026-07-25 기준.
- **신뢰성:** 최상
- **[출처 URL | 갱신 "9 days ago" (상대 표기) | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문):**

> **Soft ID:** "A soft ID typically represents a cookie. One customer can have multiple soft IDs when they use multiple devices to visit your website."

> **Hard ID:** "A hard ID often represents the email address that the customer used to register. Every customer can have multiple hard IDs, but each hard ID can only have one value."

**그래프 크기 제한 — ✅ 이 항목의 유일한 구체적 수치:**
- **Soft ID: 같은 타입당 최대 64개.** 초과 시 **least-recently-used** 항목을 제거한다.
- Hard ID: 고객당 복수 허용, 단 하나의 hard ID 식별자는 값 하나만 가진다.

**대소문자 함정 (fetch한 원문):**
> Hard ID는 case-sensitive라 중복 프로필이 생길 수 있다. 문서 표현: "This creates one customer unrecognized due to case differences, which could result in **sending an email twice to the same customer**."
> 권장 대책: "Automatically convert IDs to lowercase to prevent duplicate profiles."

**되돌릴 수 없는 설정:** soft ID를 삭제·개명하거나 hard ID로 바꾸는 것은 불가능하다. 구조 변경은 Customer Success Manager 문의 필요.

#### Merging

- **출처 URL:** https://documentation.bloomreach.com/engagement/docs/merging
- **제목:** "Merging"
- **최종 갱신:** **"9 days ago"(상대 표기)**, 조회 2026-07-25
- **신뢰성:** 최상
- **[출처 URL | 갱신 "9 days ago" (상대 표기) | 검색 시점 2026-07-25]**

**병합 동작 (fetch한 원문):**

> "When a customer visits your website using their phone and later through a PC, the platform sees this as 2 separate customers with 2 different cookies. Once they're identified on both devices—after making a purchase or logging in—the 2 profiles are automatically merged into one, together with all their historical events and customer properties."

**병합 규칙 (fetch한 원문):**
- "No 2 customers can exist with the same hard or soft ID at the same time in the same project."
- "It isn't possible to merge customer profiles with different hard IDs of the same type." ← **서로 다른 이메일을 가진 두 프로필은 병합되지 않는다**는 뜻. 오병합 방지의 근본 장치.
- 동일 soft ID가 서로 다른 hard ID 타입의 프로필에 걸쳐 존재하면, soft ID는 최신 프로필로 이동하되 **과거 이벤트는 원래 프로필에 남는다.**
- 이벤트·속성은 source → destination 고객으로 이동 (DB 생성 순서로 결정).
- 속성 이름이 겹치면 **새 값이 옛 값을 덮어쓴다.**
- 병합 시 `merge` 이벤트가 기록된다.

**공유 디바이스 문제 (fetch한 원문):**
> hard ID가 없을 때: Customer 1이 Customer 2의 기기에서 접속하면 시스템은 이를 별개 인물로 인식하지 못하고 **추가 soft ID로 취급해 Customer 2의 프로필에 붙인다** — "leaving you with one profile where there should be two."
> 대책: email을 hard ID로 지정할 것.

**병합의 비가역성:** 문서에 **명시되어 있지 않음 — 확인 불가.**

---

### 3-E. 네 벤더 종합 대조표 (⚠️ 리서처 재구성 — 각 셀은 위 각 벤더 문서에서 fetch됨)

| | **Segment** | **Adobe AEP** | **mParticle** | **Bloomreach** |
|---|---|---|---|---|
| **기능 이름** | Identity Resolution / Unify | Identity Service | IDSync | Customer identification / Merging |
| **그래프 단위 용어** | Identity Graph | identity graph ("a collection of identities that represent a single customer") | user profile | customer profile |
| **식별자 구분** | identifiers (user_id, email, 기타) | identity namespace + value | identity priority 목록 | **hard ID / soft ID** |
| **우선순위 장치** | priority (user_id 1위, email 2위, 나머지 알파벳순) | **namespace priority** | **identity priority** (오름차순 순회) | hard ID > soft ID |
| **개수 제한** | user_id: 1, 그 외: 5 (기본값) | unique namespace = 그래프당 1개 | unique ID 설정 `[검색 요약]` | **soft ID 타입당 64개 (초과 시 LRU 제거)** |
| **오병합 방지 명칭** | blocked values | **"graph collapse" 방지** | (명시 명칭 미확인) | hard ID 지정 권고 |
| **차단 대상 값** | `-1`, `null`, `anonymous`, 0/대시 패턴 | `user_null`, `not-specified` 등 | 확인 불가 | 확인 불가 |
| **익명→식별 전환** | child session → parent session 병합 | 확인 불가 | **profile conversion strategy** (익명 프로필에 login ID 추가) | 로그인/구매 시 자동 병합 |
| **문서 최신성** | 리포 최신 (날짜 미표기) | 2026-06-18 | 2026-07-16 | "9 days ago" |

**이 표에서 나오는 서술 포인트 3개:**
1. **네 벤더 모두 "우선순위 + 개수 제한"이라는 같은 두 손잡이를 준다.** 이름만 다르다.
2. **오병합은 벤더가 인정하는 알려진 실패 모드다.** Adobe는 아예 "graph collapse"라는 고유 명칭까지 붙였다.
3. **구체적 그래프 크기 제한을 문서에 숫자로 명시한 건 Bloomreach(64)뿐이다.** 나머지는 이 세션에서 확인 못 했다.

---

## P1-4. 서버사이드 vs 클라이언트사이드 — ✅ **확보 (Segment 공식 가이드)**

### [FETCHED] Segment — Collecting Data on the Client or Server

- **출처 URL:** https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/guides/how-to-guides/collect-on-client-or-server.md
- **제목:** "Collecting Data on the Client or Server"
- **발행일:** 리포 마크다운, 날짜 미표기 — **`develop` 브랜치 최신 기준, 조회 2026-07-25**
- **신뢰성:** 최상
- **[출처 URL | 발행일 미표기(리포 최신) | 검색 시점 2026-07-25]**

**클라이언트사이드로 보내야 하는 것 (fetch한 원문 기반):**
- DB에 보통 저장하지 않는 데이터 — page view, click, scroll 행동
- 클라이언트에서 잡는 게 가장 쉬운 신호 — **UTM 파라미터, 디바이스 정보, 재방문자 쿠키 데이터**
- **일부 분석 목적지는 쿠키에 의존하기 때문에 브라우저에서 보낸 이벤트만 받을 수 있다** ← 개발자가 "다 서버에서 보내면 되지"라고 생각할 때 부딪히는 벽

**서버사이드로 보내야 하는 것 (fetch한 원문):**
- **결제 이벤트** — "accuracy for payments is so important"
- 서버 데이터가 더 신뢰할 만하다: **"client-side data is fine for watching general trending, but it's never going to be perfect."**
- DB 계산이 필요한 파생 지표
- **"sensitive information is also best kept out of browsers."**

### [FETCHED] Segment — Sources 개요 (보조)

- **출처 URL:** https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/sources/index.md
- **제목:** "Sources Overview" (`src/connections/sources/index.md`)
- **발행일:** 리포 마크다운, 날짜 미표기 — **`develop` 브랜치 최신 기준, 조회 2026-07-25**
- **신뢰성:** 최상 (벤더 공식 문서의 소스 리포지토리)
- **[출처 URL | 발행일 미표기(리포 최신) | 검색 시점 2026-07-25]**

**선택 가이드 (fetch한 원문 기반):**
- Analytics.js에 대해: "Segment recommends it over server-side libraries as the simplest installation for any website"
- 모바일 SDK가 "the best way to simplify your iOS, Android, and Xamarin app tracking"
- 서버사이드는 **"when device-mode tracking (tracking on the client) doesn't work"**일 때 쓰라고 안내

**소스 3분류 (fetch한 원문):**
1. **Event Streams Sources** — 웹사이트 라이브러리(Analytics.js) / 모바일 SDK / 서버 라이브러리
2. **Cloud App Sources** — Object Cloud Sources / Event Cloud Sources
3. **Reverse ETL Sources** — BigQuery, Databricks, Postgres, Redshift, Snowflake

> 🎯 **책에 쓰기 좋은 지점:** "클라이언트냐 서버냐"는 취향 문제가 아니라 **데이터 종류가 결정한다.** Segment 자신의 결론이 명쾌하다 — 클라이언트 데이터는 "일반적 추세 관찰용으로는 충분하지만 결코 완벽하지 않다". 결제는 서버, 스크롤은 클라이언트. 그리고 **일부 목적지는 쿠키 때문에 브라우저 발신만 받는다**는 제약이 순수한 아키텍처 판단을 막는다.

---

## P1-5. Salesforce Data Cloud — ✅ **확보. 다만 중요한 발견: 제품명이 "Data 360"으로 바뀌었다**

> 💡 **앞선 리서처의 4개 URL이 404였던 이유가 이것으로 보인다.** 2026-07-25 시점 Salesforce 개발자 문서는 이 제품을 **"Data 360"**이라 부른다. `data-cloud`가 URL 경로에는 아직 남아 있다.

### [FETCHED] Data 360 Architecture (Data 360 Developer Guide)

- **출처 URL:** https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html
- **제목:** "Data 360 Architecture | Get Started with Data 360 Development | Data 360 Developer Guide"
- **발행일:** 페이지 표기 없음 — **확인 불가. 조회 시점 2026-07-25 기준 내용.**
- **신뢰성:** 최상 (벤더 공식 개발자 문서)
- **[출처 URL | 발행일 미표기 | 검색 시점 2026-07-25]**

**인용 가능한 구절 (fetch한 원문):**

> "Data 360's architecture is designed to ingest, process, unify, and activate customer data from various sources."

**아키텍처 3계층 (fetch한 원문 기반):**
- **상단:** Data 360 Home org / Companion org / 외부 LLM의 관계
- **중단:** Data 360 Home org 내부 기능
- **하단:** 기반 역량 — governance, security, sandboxes, Data Cloud One

**수집·정규화 (개발자가 볼 지점):**
> Salesforce 제품과 **"over 270 connectors, APIs, SDKs, and MuleSoft integration capabilities"**로부터 데이터가 유입된다.
> 데이터는 **DLO(Data Lake Objects)**에 저장된 뒤 **C360 Data Model 스키마**를 통해 **DMO(Data Model Objects)**로 매핑된다.
> 사전 로드된 데이터 모델에 **"over 300 industry-agnostic objects"**가 있다.

**Unification — 아이덴티티 해석 (P0-3과 직결, fetch한 원문):**

> **"The identity resolution process involves applying match rules to group individuals, and reconciliation rules to select the best quality data from these groups to generate a gold standard unified profile."**

> 🎯 **이건 P0-3 대조표에 넣을 다섯 번째 벤더다.** Salesforce는 병합을 **match rules**(그룹핑)와 **reconciliation rules**(그룹 안에서 최선의 값 고르기) **두 단계로 분리**한다. Segment·Adobe·mParticle·Bloomreach 어디에도 이만큼 명시적인 2단계 분리는 없었다. "gold standard unified profile"이라는 표현도 인용 가치가 있다 — 마케팅 업계가 흔히 말하는 "golden record"의 벤더 공식 판이다.

**Activation:** 세그멘테이션·인사이트·리포팅·오케스트레이션을 통해 "marketing campaigns, apps, flows, and external systems"로 내보낸다.

**⚠️ 제품명에 관한 정확한 서술 방법:**
- fetch한 문서는 본문에서 **"Data 360"을 쓰면서 섹션 제목·도움말 링크에는 "Data Cloud"가 남아 있다.**
- **문서에 개명 발표일이나 개명 사실 자체에 대한 명시적 서술은 없다.**
- 따라서 책에는 이렇게만 써라: **"2026-07-25 기준 `developer.salesforce.com` 문서는 이 제품을 Data 360으로 표기하며, URL 경로와 일부 섹션 제목에는 Data Cloud가 남아 있다."**
- ❌ "Salesforce가 20XX년에 Data Cloud를 Data 360으로 개명했다"라고 **개명 사건으로 쓰지 마라 — 근거 없음.**

**실패한 경로:** `architect.salesforce.com/docs/architect/fundamentals/guide/data-360-architecture` → **HTTP 403.** (검색 요약에는 lakehouse/S3/Parquet 언급이 있었으나 **원문 미확인 → 인용 금지**)

---

## P1-6. CDP 4분류 (Data / Analytics / Campaign / Delivery CDP) — ❌ **확인 불가 — 이 분류를 책에 쓰지 마라**

### 판정 근거를 정직하게 기록한다

**검색은 일관되게 이 분류가 CDP Institute(Raab)의 것이라고 말했다.** 최소 3개의 서로 다른 검색이 4개 카테고리 이름과 "동심원" 구조, "Campaign과 Delivery CDP가 전체 벤더의 2/3, 업계 고용의 3/4" 같은 구체적 수치까지 제시했다.

**그러나 원 출처를 하나도 열지 못했다:**

| 시도한 경로 | 결과 |
|---|---|
| `cdpinstitute.org/cdp-institute/cdp-vendor-classification-one-more-draft/` | **HTTP 403** |
| `cdpinstitute.org/what-is-a-cdp/` | **HTTP 403** |
| CDP Institute Industry Update PDF 2건 (`/wp-content/uploads/...`) | **HTTP 403** |
| Raab 블로그 2024-05 "Filling the Gaps for a Composable CDP" | **[FETCHED] — 그러나 4개 카테고리 명칭이 본문에 없음** ← 결정적 |
| Raab 블로그 2019-06 "It's CDP Time for Marketing Cloud Vendors" | **[FETCHED] — 네 용어 모두 본문에 없음이 명시적으로 확인됨** ← 두 번째 부정 확인 |

**Raab 블로그에서 실제로 fetch된 관련 서술 (부정 증거 2건):**

*(1) 2024-05-09, "Filling the Gaps for a Composable CDP"*
- 102개 고객 데이터 관리 기능을 **11개 카테고리**로 나눈 설문을 다룬다: "data capture, data sources, ingestion, data preparation, data storage, identity linking, customer profiles, data sharing, process integration, segment creation, and segment (i.e., audience) output"
- → **11개 분류이지 4개 분류가 아니다.**

*(2) 2019-06-17, "It's CDP Time for Marketing Cloud Vendors"*
- 이 글은 **"Data CDP", "Analytics CDP", "Campaign CDP", "Delivery CDP" 네 용어를 하나도 쓰지 않는다** (fetch로 명시 확인).
- 대신 시장 분열을 이렇게 서술한다: 벤더들이 "focus on data collection, unification, and access functions and those with marketing functions for analytics and personalization"로 갈린다. 그리고 "CDPs with a full set of marketing applications become direct competitors of the marketing clouds."
- → **개념적으로 비슷한 스펙트럼은 존재하지만, 4분류 라벨 체계는 확인되지 않는다.**

> **부정 확인이 2건 쌓였다.** Raab 본인 블로그 2개 글에서 네 용어가 나오지 않았다. 이건 "못 찾았다"보다 강한 결과다.

### 🚨 최종 판정

> **확인 불가 — 이 분류를 책에 쓰지 마라.**
>
> 검색 요약 여러 건이 일치한다는 것은 확인이 아니다. 특히 이 4분류는 위키·벤더 블로그·SEO 아티클을 통해 널리 복제된 형태라 검색 합성 요약이 서로를 강화할 뿐이다. **"널리 통용되는 분류"라고 완화해서 쓰는 것도 금지한다.**
>
> 굳이 CDP 유형 구분이 필요하다면, **fetch로 확인된 Raab 2017년 3축 벤 다이어그램(1-C)을 쓰라.** 그건 1차 출처로 확보되어 있다.

**후속 재시도 경로 (다른 세션·다른 네트워크에서):** cdpinstitute.org 403이 풀리는지. Raab 블로그 2019-06은 이미 확인했고 없었다 — 남은 후보는 2021-01 아카이브 정도이며 기대치는 낮다.

---

## P2-7. Martech 랜드스케이프 규모 — ✅ **확보 (원문 fetch, 2026년판)**

### [FETCHED] chiefmartec — 2026 Marketing Technology Landscape Supergraphic

- **출처 URL:** https://chiefmartec.com/2026/05/2026-marketing-technology-landscape-supergraphic-peak-martech-achieved-maybe/
- **제목:** "2026 Marketing Technology Landscape Supergraphic: Peak Martech Achieved! (Maybe)"
- **저자:** Scott Brinker (chiefmartec 바이라인)
- **발행일:** **2026년 5월 5일**
- **신뢰성:** 최상 (랜드스케이프 발행 당사자의 1차 발표 글)
- **[출처 URL | 발행일 2026-05-05 | 검색 시점 2026-07-25]**

**확보된 수치 — 이 숫자들은 원문에서 직접 나온 것이다:**

| 항목 | 값 |
|------|-----|
| **2026년 총 솔루션 수** | **15,505** |
| 전년 대비 성장률 | **0.79%** |
| 추가된 제품 | **1,488** |
| 제거된 제품 | **1,367** |

**인용 가능한 구절 (fetch한 원문):**

> "The martech landscape effectively stopped growing this year, up just 0.79% to 15,505 products."

> "After 15 years of relentless expansion, we may have finally hit peak martech — or at least a plateau."

> "1,488 products were added, while 1,367 were removed."

> 🎯 **책에 쓰기 좋은 지점:** "Martech 5000"이라는 별명은 **2017년경 숫자에서 온 화석**이다. 2026년 현재는 **15,505개**다. 그런데 더 흥미로운 건 **총량이 멈췄는데 내부 회전은 계속된다**는 점 — 1,488개가 들어오고 1,367개가 나갔다. 개발자 독자에게 이건 "이 바닥의 벤더 하나를 붙잡고 배우는 건 무의미하고, 구조를 배워야 한다"는 논증의 실증 근거가 된다.

> ⚠️ **fact-checker 주의 — 비슷하지만 다른 숫자가 돌아다닌다:** 검색 결과에 `martech.org`의 "The number of martech tools is now **15,384**"라는 헤드라인이 있었다. **이 페이지는 fetch하지 않았다.** 15,384가 어느 연도·어느 집계인지 확인되지 않았다. **책에는 fetch로 확인된 15,505(2026년판)만 쓰고, 반드시 "2026년판 기준"이라고 연도를 못박아라.**

---

## 상충·불확실 항목

### ① CDP 정의가 두 갈래다 — 둘 다 실제 확보됨, 해소하지 말고 서술하라

| | Raab 2015 [FETCHED] | CDPI via Informatica [2차 인용] |
|---|---|---|
| 정의 | "a **marketer-controlled** system that builds a multi-source customer database and exposes it to external execution systems" | "**packaged software** that creates a persistent, unified customer database that is accessible to other systems" |
| 강조점 | **누가 통제하는가** (마케터) | **어떤 형태의 물건인가** (패키지 소프트웨어) |

**같은 사람/기관 계열에서 나왔는데 정의의 축이 다르다.** "marketer-controlled"는 조직적 정의고 "packaged software"는 제품 형태 정의다. 후자는 **직접 만든 데이터 웨어하우스를 CDP에서 배제하는 효과**가 있다 — composable CDP 논쟁(앞선 리서처가 Hightouch 정의로 확보)이 정확히 이 지점을 공격한다. **책에서 이 긴장을 그대로 보여주는 게 낫다.**

### ② 애널리스트 분류 vs 벤더 자기 규정 — DMP는 데이터를 통합하는가?

- **Raab 2017 [FETCHED]:** DMP는 "메시지를 고르지만 데이터를 통합하지 않고 개방 접근도 제공하지 않는다"
- **Adobe Audience Manager 공식 문서 [FETCHED]:** AAM은 "**Unifies data into audience profiles**, giving you a complete customer view across devices and channels"

**정면 충돌이다.** 둘 다 1차 출처에서 나왔다 — 단, **근거의 형태가 다르다는 점에 주의**: Adobe 쪽은 페이지 본문의 **축자 인용**이고, Raab 2017 쪽은 원문의 **벤 다이어그램 이미지를 fetch 요약으로 옮긴 것**이다(1-C의 ⚠️ 주석 참조). 충돌 자체는 실재하지만, 양쪽을 똑같이 "인용문"으로 취급하지는 마라. **판정하지 마라.** 이건 martech 카테고리 논쟁의 전형 — 애널리스트가 카테고리 경계를 좁게 긋고, 벤더는 자기 제품을 넓게 규정한다. 개발자 독자에게 **"카테고리 이름을 믿지 말고 기능을 확인하라"**는 교훈의 실물 사례로 쓰기에 최적이다.

### ③ Martech 총량 숫자 두 개 — 15,505 vs 15,384

위 P2-7 참조. **15,505만 확인됨.**

### ④ Salesforce 제품명 — Data Cloud / Data 360 혼재

위 P1-5 참조. **개명 사건으로 쓰지 말 것.**

### ⑤ 🇰🇷 "CRM"이라는 세 글자가 한국과 영미권에서 다른 것을 가리킨다

**둘 다 fetch된 출처로 확인됨.** 이건 "상충"이라기보다 **용어의 지역적 분기**이고, 대상 독자가 한국 개발자인 이 책에서는 **반드시 명시적으로 다뤄야 할 항목**이다.

- **Salesforce Trailhead [FETCHED]:** CRM = 고객·잠재고객 관계 관리 기술, 핵심 객체는 Account/Contact/**Lead/Opportunity** → **영업 파이프라인**
- **노티플라이·FlareLane [FETCHED, 신뢰성 중]:** CRM 마케팅 = "리텐션을 높이는 모든 고객대상 마케팅", 채널은 **푸시·카카오 알림톡·친구톡·문자·이메일** → **메시지 발송/리텐션**

**판정하지 마라 — 둘 다 자기 맥락에서 맞다.** 책에서는 "한국 현장에서 CRM 마케팅이라고 하면 보통 후자를 뜻한다"고 **용법의 차이로** 서술할 것. 다만 한국어 출처 2건이 모두 **자사 솔루션을 파는 벤더 블로그**임을 감안해, 중립적 정의가 아니라 **업계 용법의 증거**로만 쓸 것.

### ⑥ 한국어 소스 커버리지: 2건 (모두 벤더 블로그)

이번 갭 필러에서 확보한 한국어 소스는 위 2건뿐이며, 둘 다 신뢰성 **중**이다. 중립적 한국어 1차 소스(학회·정부·표준 문서)는 확보하지 못했다.

---

## 확인 불가 목록

> 이것들도 유효한 리서치 결과다. **아래 항목에 대해 책에 단정적 서술을 쓰지 마라.**

### A. 접근 차단 (HTTP 403) — 후속 리서처를 위한 지도

| 도메인/URL | 상태 | 비고 |
|---|---|---|
| `cdpinstitute.org` **전체** | **403 (사이트 전역)** | `/about/`, `/what-is-a-cdp/`, `/cdp-institute/cdp-vendor-classification-one-more-draft/`, `/wp-content/uploads/...pdf` **4개 경로 모두 차단.** **PDF 우회도 막혔다** — 이건 확정적 부정 결과다 |
| `salesforce.com/crm/what-is-crm/` | **403** | ✅ **우회 성공: `trailhead.salesforce.com`은 열린다.** 후속 리서처는 Trailhead를 쓸 것 |
| `gartner.com` 용어집 | **403** | CEM 정의 확보 실패 |
| `architect.salesforce.com` | **403** | ✅ 우회 성공: `developer.salesforce.com/docs/...`는 열린다 |
| `business.adobe.com/products/marketo.html` | **ETIMEDOUT** | 재시도 가치 있음 |
| `iab.com` PDF | 200이지만 **바이너리 미파싱** | 로컬 저장됨. PDF 텍스트 추출로 재시도 가능 |

**✅ 이 세션에서 열리는 것으로 확인된 경로 (후속 리서처는 이걸 우선 쓸 것):**
- `raw.githubusercontent.com/segmentio/segment-docs/develop/src/...` (segment.com 403 우회)
- `experienceleague.adobe.com` (Adobe 전 제품 문서)
- `docs.mparticle.com`
- `documentation.bloomreach.com`
- `developer.salesforce.com/docs/...`
- `trailhead.salesforce.com`
- `chiefmartec.com`
- `customerexperiencematrix.blogspot.com` (Raab 블로그 — 1차 출처의 보고)

### B. 내용 확보 실패 — 책에 쓸 수 없는 것들

| 항목 | 상태 | 재시도 경로 |
|---|---|---|
| **CDP Institute 공식 정의 (1차)** | 확인 불가 — 2차 인용만 확보 | Raab 1차 원문(1-A/1-B)으로 **대체 권장** |
| **CDP Institute 창립 연도** | 확인 불가 | — |
| **CRM 용어의 기원·연도·창시자** | 확인 불가 (검색 요약만, 서드파티 블로그 출처) | — |
| ~~MA(마케팅 자동화) 정의~~ | ✅ **해소됨** — Trailhead로 우회 확보 (2-C) | — |
| ~~리드 스코어링 정의~~ | ✅ **해소됨** — Trailhead에서 score/grade 2축 확보 | — |
| ~~한국식 "CRM 마케팅" 용법~~ | ✅ **해소됨** — 한국어 소스 2건 fetch (2-B) | — |
| **Marketo/HubSpot/Pardot/Eloqua 출시 연도** | 확인 불가 | 각 벤더 연혁 페이지 |
| **Pardot → Account Engagement 개명 시점** | 확인 불가 (문서에 신·구 명칭 혼재, 개명일 없음) | Salesforce 릴리스 노트 |
| **CEM/CXM 정의** | ❌ 확인 불가 (Gartner 403) — **비교표에서 제외 권장** | Adobe·SAP·Microsoft Dynamics 공식 문서 |
| **각 카테고리 등장 시점 전반** | 확인 불가 (CDP 2013만 예외) | 애널리스트 리포트 |
| **"DMP는 서드파티 쿠키 기반" 명제** | 확인 불가 (Adobe 문서에 쿠키 언급 없음) | IAB PDF 텍스트 추출, LiveRamp·The Trade Desk 문서 |
| **CDP 4분류** | ❌ **확인 불가 — 사용 금지** (부정 확인 2건) | P1-6 참조 |
| **mParticle login ID 무결성 규칙** | 검색 요약만 | `docs.mparticle.com/guides/idsync/components/` |
| **Adobe 결정론/확률론 여부** | 확인 불가 | Identity Service 하위 문서 |
| **Bloomreach 병합 비가역성** | 확인 불가 | — |

---

## 신선도 원장

| 소스 | URL | 발행일/갱신일 | 검색 시점 | 관련 항목 | 등급 |
|------|-----|--------------|-----------|-----------|------|
| Raab — CDP 명명 원글 | customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html | **2013-04-25** | 2026-07-25 | P0-1 | FETCHED |
| Raab — CDP Revisited | customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html | **2015-01-18** | 2026-07-25 | P0-1 | FETCHED |
| Raab — 시스템 관계 벤 다이어그램 | customerexperiencematrix.blogspot.com/2017/03/wondering-how-customer-data-platforms.html | **2017-03-23** | 2026-07-25 | P0-1, P0-2 | FETCHED |
| Raab — Composable CDP | customerexperiencematrix.blogspot.com/2024/05/back-in-february-i-mentioned-that-cdp.html | **2024-05-09** | 2026-07-25 | P1-6 (부정 확인) | FETCHED |
| Informatica — CDP 문서 | informatica.com/resources/articles/what-is-a-customer-data-platform.html | 미표기 | 2026-07-25 | P0-1 | **2차 인용** |
| Wikipedia — CDP | en.wikipedia.org/wiki/Customer_data_platform | 미상 | 2026-07-25 | P0-1, P0-2 | FETCHED (신뢰성 중) |
| Adobe — DMP destinations | experienceleague.adobe.com/en/docs/experience-platform/destinations/catalog/data-management/overview | **2026-05-23** | 2026-07-25 | P0-2 | FETCHED |
| Adobe — AAM Overview | experienceleague.adobe.com/en/docs/audience-manager/user-guide/overview/aam-overview | **2026-05-21** | 2026-07-25 | P0-2 | FETCHED |
| Adobe — AAM DMP 튜토리얼 | experienceleague.adobe.com/en/docs/audience-manager-learn/tutorials/intro-to-audience-manager/audience-manager-overview-of-a-dmp | **2026-05-21** | 2026-07-25 | P0-2 (정의 없음) | FETCHED |
| Salesforce Trailhead — CRM Basics | trailhead.salesforce.com/content/learn/modules/lex_implementation_basics/lex_implementation_basics_welcome | 미표기 | 2026-07-25 | P0-2 | FETCHED |
| Adobe — Marketo 리드 스코어링 | experienceleague.adobe.com/en/docs/marketo-learn/tutorials/lead-and-data-management/lead-scoring-learn | **2026-05-12** | 2026-07-25 | P0-2 (정의 없음) | FETCHED |
| Trailhead — B2B Marketing Automation 입문 | trailhead.salesforce.com/content/learn/modules/pardot-basics-lightning/get-started-with-pardot-lightning | 미표기 | 2026-07-25 | P0-2 (MA) | FETCHED |
| Trailhead — Lead Nurturing 전략 | trailhead.salesforce.com/content/learn/modules/pardot-lead-nurturing-lightning/integrate-lead-nurturing-into-your-marketing-strategy | 미표기 | 2026-07-25 | P0-2 (MA) | FETCHED |
| 🇰🇷 노티플라이 — CRM 마케팅이란? | blog.notifly.tech/crm-marketing-introduction/ | **2023-10-24** ⚠️ 3년 경과 | 2026-07-25 | P0-2 (한국 용법) | FETCHED (신뢰성 중) |
| 🇰🇷 FlareLane — CRM 마케팅이란 무엇일까? | blog.flarelane.co.kr/what-is-crm-marketing-concepts-strategies-and-common-mistakes/ | **2025-04-22** | 2026-07-25 | P0-2 (한국 용법) | FETCHED (신뢰성 중) |
| Raab — It's CDP Time for Marketing Cloud Vendors | customerexperiencematrix.blogspot.com/2019/06/its-cdp-time-for-marketing-cloud-vendors.html | **2019-06-17** | 2026-07-25 | P1-6 (부정 확인) | FETCHED |
| Segment — Identity Resolution 개요 | raw.githubusercontent.com/segmentio/segment-docs/develop/src/unify/identity-resolution/index.md | 리포 최신 | 2026-07-25 | P0-3 | FETCHED |
| Segment — Identity Resolution 설정 | raw.githubusercontent.com/segmentio/segment-docs/develop/src/unify/identity-resolution/identity-resolution-settings.md | 리포 최신 | 2026-07-25 | P0-3 | FETCHED |
| Adobe — Identity Service Overview | experienceleague.adobe.com/en/docs/experience-platform/identity/home | **2026-06-18** | 2026-07-25 | P0-3 | FETCHED |
| Adobe — Identity Graph Linking Rules | experienceleague.adobe.com/en/docs/experience-platform/identity/features/identity-graph-linking-rules/overview | **2026-06-18** | 2026-07-25 | P0-3 | FETCHED |
| mParticle — IDSync Overview | docs.mparticle.com/guides/idsync/introduction/ | **2026-07-16** | 2026-07-25 | P0-3 | FETCHED |
| mParticle — Identify Users | docs.mparticle.com/guides/idsync/identify-users/ | 미확인 | 2026-07-25 | P0-3 | FETCHED |
| Bloomreach — Customer identification | documentation.bloomreach.com/engagement/docs/customer-identification | **"9 days ago"** (상대 표기) | 2026-07-25 | P0-3 | FETCHED |
| Bloomreach — Merging | documentation.bloomreach.com/engagement/docs/merging | **"9 days ago"** (상대 표기) | 2026-07-25 | P0-3 | FETCHED |
| Segment — Client or Server | raw.githubusercontent.com/segmentio/segment-docs/develop/src/guides/how-to-guides/collect-on-client-or-server.md | 리포 최신 | 2026-07-25 | P1-4 | FETCHED |
| Segment — Sources 개요 | raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/sources/index.md | 리포 최신 | 2026-07-25 | P1-4 | FETCHED |
| Salesforce — Data 360 Architecture | developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html | 미표기 | 2026-07-25 | P1-5 | FETCHED |
| chiefmartec — 2026 Landscape | chiefmartec.com/2026/05/2026-marketing-technology-landscape-supergraphic-peak-martech-achieved-maybe/ | **2026-05-05** | 2026-07-25 | P2-7 | FETCHED |

**신선도 총평:**
- **매우 신선 (2026년 5~7월 갱신):** Adobe 전 문서, mParticle, Bloomreach, chiefmartec. 이 항목들은 그대로 써도 된다.
- **역사적 1차 기록 (2013~2024, Raab 블로그):** 오래된 것이 결함이 아니다 — 용어가 만들어진 순간의 기록이라 가치가 있다. 단 **"2013년 당시의 정의"**임을 본문에 반드시 명시할 것. 특히 2015년 정의를 현재 정의처럼 쓰면 안 된다.
- **⚠️ 구버전 정보 가능성:** 노티플라이 글(**2023-10-24, 약 3년 경과**)은 한국 CRM 마케팅 시장이 빠르게 변한 기간을 지났다. 채널 목록·솔루션 비교 부분은 지금과 다를 수 있다. **정의 문장만 쓰고 솔루션·시장 현황 서술은 인용하지 말 것.**
- **날짜 미표기:** Trailhead·Salesforce 개발자 문서·Segment 리포 마크다운은 페이지에 발행일이 없다. 전부 **"2026-07-25 조회 기준"**으로만 표기할 것.
- **상대 표기:** Bloomreach 2건은 "9 days ago"로만 표시된다. **절대 날짜로 변환해 적지 마라** — 상대 표기 그대로 기록했다.

---

## 참고문헌

**1차 소스 (FETCHED)**

1. Raab, David. "I've Discovered a New Class of System: the Customer Data Platform. Causata Is An Example." *Customer Experience Matrix*, 2013-04-25. http://customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html
2. Raab, David M. "Customer Data Platforms Revisited: The Future of Marketing Data." *Customer Experience Matrix*, 2015-01-18. http://customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html
3. Raab, David. "Wondering How Customer Data Platforms Relate to Other Marketing Systems? Here's a Picture." *Customer Experience Matrix*, 2017-03-23. https://customerexperiencematrix.blogspot.com/2017/03/wondering-how-customer-data-platforms.html
4. Raab, David. "Filling the Gaps for a Composable CDP." *Customer Experience Matrix*, 2024-05-09. http://customerexperiencematrix.blogspot.com/2024/05/back-in-february-i-mentioned-that-cdp.html
5. Brinker, Scott. "2026 Marketing Technology Landscape Supergraphic: Peak Martech Achieved! (Maybe)." *chiefmartec*, 2026-05-05. https://chiefmartec.com/2026/05/2026-marketing-technology-landscape-supergraphic-peak-martech-achieved-maybe/
6. Adobe. "Data Management Platform (DMP) destinations overview." *Adobe Experience Platform Documentation*, 갱신 2026-05-23. https://experienceleague.adobe.com/en/docs/experience-platform/destinations/catalog/data-management/overview
7. Adobe. "Audience Manager Overview." *Adobe Audience Manager Documentation*, 갱신 2026-05-21. https://experienceleague.adobe.com/en/docs/audience-manager/user-guide/overview/aam-overview
8. Adobe. "Identity Service Overview." *Adobe Experience Platform Documentation*, 갱신 2026-06-18. https://experienceleague.adobe.com/en/docs/experience-platform/identity/home
9. Adobe. "Identity Graph Linking Rules." *Adobe Experience Platform Documentation*, 갱신 2026-06-18. https://experienceleague.adobe.com/en/docs/experience-platform/identity/features/identity-graph-linking-rules/overview
10. Segment. "Identity Resolution Overview." *segment-docs* (GitHub, develop 브랜치), 조회 2026-07-25. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/unify/identity-resolution/index.md
11. Segment. "Identity Resolution Settings." *segment-docs* (GitHub, develop 브랜치), 조회 2026-07-25. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/unify/identity-resolution/identity-resolution-settings.md
12. Segment. "Collecting Data on the Client or Server." *segment-docs* (GitHub, develop 브랜치), 조회 2026-07-25. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/guides/how-to-guides/collect-on-client-or-server.md
13. mParticle. "IDSync Overview." *mParticle Documentation*, 갱신 2026-07-16. https://docs.mparticle.com/guides/idsync/introduction/
14. mParticle. "IDSync | Identify Users." *mParticle Documentation*, 조회 2026-07-25. https://docs.mparticle.com/guides/idsync/identify-users/
15. Bloomreach. "Customer identification." *Bloomreach Engagement Documentation*, 갱신 "9 days ago", 조회 2026-07-25. https://documentation.bloomreach.com/engagement/docs/customer-identification
16. Bloomreach. "Merging: How profile merging works in Bloomreach." *Bloomreach Engagement Documentation*, 갱신 "9 days ago", 조회 2026-07-25. https://documentation.bloomreach.com/engagement/docs/merging
17. Salesforce. "Data 360 Architecture." *Data 360 Developer Guide*, 조회 2026-07-25. https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-architecture.html
18. Salesforce. "Salesforce CRM Basics." *Trailhead*, 조회 2026-07-25. https://trailhead.salesforce.com/content/learn/modules/lex_implementation_basics/lex_implementation_basics_welcome
19. Salesforce. "Beginner's Guide to B2B Marketing Automation — Get Started with Account Engagement." *Trailhead*, 조회 2026-07-25. https://trailhead.salesforce.com/content/learn/modules/pardot-basics-lightning/get-started-with-pardot-lightning
20. Salesforce. "Integrate Lead Nurturing Into Your Marketing Strategy." *Trailhead*, 조회 2026-07-25. https://trailhead.salesforce.com/content/learn/modules/pardot-lead-nurturing-lightning/integrate-lead-nurturing-into-your-marketing-strategy
21. Raab, David. "It's CDP Time for Marketing Cloud Vendors." *Customer Experience Matrix*, 2019-06-17. — **P1-6 부정 확인 근거.** http://customerexperiencematrix.blogspot.com/2019/06/its-cdp-time-for-marketing-cloud-vendors.html

**한국어 소스 (신뢰성 중 — 벤더 블로그, 업계 용법의 증거로만 사용)**

22. 노티플라이. "CRM 마케팅이란? 연차별 CRM 마케터 업무 및 역량, 솔루션 비교." 2023-10-24. ⚠️ 약 3년 경과 — 정의 문장만 사용 권장. https://blog.notifly.tech/crm-marketing-introduction/
23. FlareLane. "CRM 마케팅이란 무엇일까? 개념, 활용 전략 비교." 2025-04-22. https://blog.flarelane.co.kr/what-is-crm-marketing-concepts-strategies-and-common-mistakes/

**2차 인용 / 신뢰성 중 (인용 시 반드시 등급 표시)**

24. Informatica. "Customer Data Platform: Capabilities and Benefits." 조회 2026-07-25. — **CDP Institute 정의의 2차 인용원.** https://www.informatica.com/resources/articles/what-is-a-customer-data-platform.html
25. Wikipedia. "Customer data platform." 조회 2026-07-25. https://en.wikipedia.org/wiki/Customer_data_platform
