<!-- 병합본: web_products.md + web_stack.md + web_privacy.md + web_gaps.md -->
<!-- 원본 4파일도 이 디렉터리에 보존됨. 하네스 계약상 research/web.md 경로를 채우기 위한 연결본 -->
<!-- 검색 수행일: 2026-07-25 -->

<!-- ===== web_products.md ===== -->

<!-- 검색 시점: 2026-07-25 기준 -->
<!-- 담당: web-researcher #1 (제품 카테고리 분류학 + 벤더 1차 소스 축) -->
<!-- genre: tech-book / slug: martech-for-developers -->

# Martech 제품 카테고리·벤더 리서치 (web #1)

검색 수행일: **2026-07-25**

## 이 문서의 사실 규율

- 모든 인용문(`>` 블록 또는 큰따옴표)은 **이 세션에서 WebFetch로 실제로 연 페이지**에서 가져온 것이다.
- WebFetch는 페이지 원문이 아니라 소형 모델이 읽고 답한 결과를 돌려준다. 따라서 **따옴표로 감싼 것만 원문 인용(verbatim)**으로 취급하고, 따옴표 없는 서술은 `요지(paraphrase)`로 표시했다.
- 발행일이 페이지에 없으면 `발행일 미표기`. 문서 사이트의 자동 타임스탬프는 `문서 사이트 표기 — 최초 발행일/갱신일 구분 불가`로 명시했다.
- 열지 못한 페이지에서 얻은 정보는 쓰지 않았다. 필요한데 못 연 것은 `## 확인 불가 목록`에 남겼다.
- 벤더가 자기 제품을 설명한 문장은 전부 `벤더 자체 주장`이다. 사실로 승격하지 않았다.

---

## A. 카테고리 분류학

### A-0. ✅ CDP라는 말을 만든 사람의 원문 — David Raab, 2013년 4월 25일

> **이 자료가 A축의 앵커다.** CDP Institute 사이트는 열지 못했지만(§A-0-1), **CDP Institute의 창립자 David Raab이 자기 블로그에서 이 카테고리를 처음 명명한 글**을 원문으로 확보했다. 저자가 확인되는 1차 소스이며, 카테고리의 기원을 다루는 데 이보다 나은 근거는 없다.

**글 제목:** "I've Discovered a New Class of System: the Customer Data Platform. Causata Is An Example."
**발행일:** Thursday, April 25, 2013

**이런 시스템이 하는 일 (원문):**

> "These systems that gather customer data from multiple sources, combine information related to the same individuals, perform predictive analytics on the resulting database, and use the results to guide marketing treatments across multiple channels."

**이름을 붙이는 대목 (원문):**

> "I'll step in myself, and hereby christen the concept as 'Customer Data Platform'. Aside from having a relatively available three letter abbreviation (see Acronym Finder for other uses of CDP), the merits of this name include:
>
> - "Customer" shows the scope extends to all customer-related functions, not just marketing;
> - "Data" shows the primary focus is on data, not execution; and
> - "Platform" shows it does more than data management while supporting other systems"

[http://customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html | 2013-04-25 | 검색 시점 2026-07-25]

> **책에서 이 자료가 갖는 힘:** "CDP라는 이름의 세 단어가 각각 무엇을 주장하는가"를 **작명자 본인의 문장**으로 설명할 수 있다. Customer(마케팅만이 아니다) / Data(실행이 아니라 데이터가 중심이다) / Platform(다른 시스템을 떠받친다). 이 세 줄이 §A-4에서 관찰한 "카테고리가 왜 흐릿한가"의 원인이기도 하다 — 이름 자체가 세 방향으로 열려 있다.
> ⚠️ **13년 전 글이다.** 카테고리의 *기원*을 말할 때만 쓰고, 현재 제품의 정의로 쓰지 마라.

**2015년의 다듬어진 정의 (같은 저자, 원문):**

> "a marketer-controlled system that builds a multi-source customer database and exposes it to external execution systems"

**글 제목:** "Customer Data Platforms Revisited: The Future of Marketing Data" / **발행일:** 2015-01-18
⚠️ 이 글에서 DMP·CRM·마케팅 자동화·데이터 웨어하우스와의 명시적 대비 → **NOT FOUND**

[http://customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html | 2015-01-18 | 검색 시점 2026-07-25]

> **2013 → 2015 정의 변화가 흥미롭다.** 2013년 정의에는 "perform predictive analytics"가 들어 있었는데, 2015년 정의에서는 빠지고 **"marketer-controlled"**와 **"exposes it to external execution systems"**가 들어왔다. 즉 **분석은 필수 요건에서 빠지고, 소유권(마케터가 통제한다)과 개방성(외부 실행 시스템에 노출한다)이 핵심으로 올라왔다.**
> 개발자 독자에게: "CDP는 왜 데이터를 자기 안에 가둬두지 않고 밖으로 내보내는가"의 답이 정의 자체에 박혀 있다.
> ⚠️ 위 비교는 이 리서치의 관찰이다. 두 정의문만 사실이다.

### A-0-1. ⚠️ 남은 결손 — CDP Institute 사이트의 공식 정의 원문

이 축의 앵커가 되어야 할 **CDP Institute(cdpinstitute.org)의 공식 CDP 정의를 이 세션에서 확보하지 못했다.**

- `https://www.cdpinstitute.org/learning-center/what-is-a-cdp/` → **HTTP 403 Forbidden**
- `https://www.cdpinstitute.org/cdp-basics/` → **HTTP 403 Forbidden**
- `https://www.cdpinstitute.org/about/` → **HTTP 403 Forbidden**
- `https://cdpinstitute.org/learning-center/what-is-a-cdp/` (www 없이) → **HTTP 403 Forbidden**
- `https://sea.cdpinstitute.org/cdp-basics/` → **DNS 조회 실패 (ENOTFOUND)**
- `https://web.archive.org/web/2026/https://www.cdpinstitute.org/...` → **도구가 web.archive.org 접근 불가**

**판정: `확인 불가 (cdpinstitute.org 사이트 전역 403 — 2026-07-25 조회 실패, 기관 공식 정의문 미확보)`**

> **완화됨:** §A-0에서 **작명자 David Raab 본인의 원문 정의 2건(2013·2015)**을 확보했으므로, "CDP가 무엇인지"를 1차 소스로 설명할 수는 있다. 다만 그건 **개인 저자의 블로그 정의**이고, **CDP Institute라는 기관의 공식 정의문은 여전히 없다.** 둘을 섞어 쓰지 마라.
>
> **책 저술 시 주의:** "CDP Institute는 CDP를 ~라고 정의한다"라는 문장을 쓰려면 별도 확인이 필요하다. 기억으로 문장을 복원해 넣지 마라 — "persistent, unified customer database that is accessible to other systems" 계열 문장은 널리 회자되지만 이 세션에서 원문 대조를 하지 못했다. 대신 **"CDP라는 용어를 만든 David Raab은 ~라고 썼다"**로 쓰면 §A-0의 원문으로 뒷받침된다.
>
> [출처 URL 다수 | 조회 실패 | 검색 시점 2026-07-25]

관련해서 **확보한 주변 사실:**
- ✅ **"CDP"라는 용어의 최초 명명 시점: 2013년 4월 25일**, David Raab의 블로그 글. **1차 확인 완료** (§A-0)
- 검색 결과 페이지 타이틀이 `"The CDP Institute Backstory | CDP Institute / Customer Data Alliance"`로 표기됨 → CDP Institute가 **"Customer Data Alliance"**라는 이름을 병기하고 있을 가능성. **미확인 — 페이지를 열지 못했다.** `확인 불가`
- David Raab이 CDP Institute의 창립자라는 사실 → **`확인 불가 (1차 소스 미확보)`.** 단, 그가 CDP를 명명한 인물이라는 것은 §A-0으로 확인됨.
- CDP Institute 설립 연도 → **`확인 불가`**

### A-0-2. Gartner의 CDP 정의 — 확인 불가

- `https://www.gartner.com/en/information-technology/glossary/customer-data-platform-cdp` → **HTTP 403 Forbidden**
- **판정: `확인 불가 (gartner.com 403 — 2026-07-25 조회 실패)`**
- Forrester 공개 정의 페이지도 이번 세션에서 조회하지 못함. `확인 불가 (미조회)`

> 애널리스트 정의(Gartner/Forrester)는 대부분 페이월·봇 차단 뒤에 있다. 책에서 인용하려면 벤더가 인용한 형태(= 2차 인용)로 쓰거나, 아예 쓰지 않는 편이 안전하다.

### A-1. 확보한 1차/1차-준하는 정의

#### A-1-a. Composable CDP — Hightouch 정의 (벤더 자체 주장, 1차)

> "A Composable CDP is a customer data platform that enables you to use any data in your organization to power marketing use cases like audience management, journey orchestration, personalization, and data activation directly from your existing data infrastructure."

패키지형 CDP와의 대비 (요지 + 부분 인용):
- 전통적 CDP는 네 가지 구성요소(데이터 저장 / identity resolution / 오디언스 빌딩 / 데이터 싱크)를 **묶어서** 팔고, 그래서 전부를 지불해야 한다. (요지)
- Composable CDP는 "start with your current data (wherever it is) and activate it immediately rather than implementing and purchasing an entirely new tool that stores data outside of your data infrastructure."
- Composable CDP의 역할: "an activation and audience management layer" — Reverse ETL로 구동되며 "a middleman between your data assets and your marketing tools"로 동작하고, 고객 데이터를 **스스로 저장하지 않는다.**

[https://hightouch.com/blog/composable-cdp | 저자 Luke Kline, 발행 2023-06-20 | 검색 시점 2026-07-25]
⚠️ **3년 전 글 — 구버전 정보일 수 있음.** 다만 "composable CDP" 개념 정의 자체는 안정적이다.

#### A-1-b. Hightouch 제품 페이지 — warehouse-native 주장 (벤더 자체 주장, 1차)

> "A Composable CDP built for marketers that can be deployed in weeks, mastered in minutes, and never copies your data."

> "Don't copy your data to an incompatible and less secure data silo. Turn your existing data into a CDP instead."

> "Hightouch doesn't store your data. Instead we simply read from your data warehouse where it stays safe and sound."

제품 모듈 (원문 표기):
| 모듈 | 설명 (원문) |
|---|---|
| Hightouch Events | "Collect data directly into your data warehouse" |
| Identity Resolution | "Analyze and organize your data into a single source of truth" |
| Customer Studio | "Activate any type of data to power any use case" |

[https://hightouch.com/platform/composable-cdp | 발행일 미표기 | 검색 시점 2026-07-25]

**개발자 관점 해설 포인트:** "패키지형 CDP는 데이터를 복사해 자기 저장소에 넣고, 컴포저블 CDP는 웨어하우스를 그대로 읽는다" — 이 한 문장이 두 갈래를 가르는 핵심 아키텍처 차이다. 위 세 인용문이 그 근거로 쓸 수 있는 1차 문장이다.

#### A-1-c. Hightouch 개발자 문서 — 코어 개념 4종 (1차, 개발자 표면)

> **Source**: "A source is any system where your data resides. Common examples include Snowflake, BigQuery, Databricks, and PostgreSQL."

> **Model**: "A model defines what data to query from a source. Models can represent users, events, products, or any other entity."

> **Sync**: "A sync defines how data appears in the destination and when. Syncs specify: Type: object, event, audience, etc. Mode: insert, update, upsert, or archive Mapping: how source columns map to destination fields Schedule: interval, cron, or triggered by tools like dbt Cloud or Airflow"

> **Destination**: "A destination is any system where data is consumed — CRMs, ad platforms, support tools, analytics, or custom APIs."

[https://hightouch.com/docs/getting-started/concepts | 페이지 표기 "Last updated Jul 17, 2026" (문서 사이트 표기) | 검색 시점 2026-07-25]

⚠️ 이 문서 페이지에는 "데이터가 웨어하우스에 남는다 / 복사하지 않는다"는 **명시적 문장이 없었다**(제품 마케팅 페이지에만 있음). 문서와 마케팅 페이지의 톤 차이 자체가 관찰 가치가 있다.

**관련 섹션:** "컴포저블 CDP는 어떻게 동작하는가" 챕터. Source → Model → Sync → Destination 4단계는 reverse ETL의 표준 멘탈 모델로 그대로 쓸 수 있다.

#### A-1-d. 웨어하우스 위 CDP 레퍼런스 아키텍처 — Google Cloud 엔지니어링 블로그

BigQuery + Reverse ETL 아키텍처 구성 (요지, 원문 정의문은 없음):
1. **데이터 수집** — Google Analytics 같은 이벤트 수집 도구가 BigQuery로 스트리밍, Fivetran 같은 ETL/ELT가 나머지 조직 데이터를 적재
2. **단일 진실 원천** — BigQuery가 중앙 데이터 웨어하우스 역할
3. **데이터 모델링** — Google Cloud의 컴퓨트·AI/ML 도구로 모델링
4. **액티베이션 레이어** — Hightouch가 BigQuery 바로 위에 얹혀 동기화
5. **Reverse ETL** — BigQuery에서 200+ 다운스트림 도구로 싱크 (비주얼 에디터 또는 SQL/dbt)

⚠️ "composable CDP"의 명시적 정의문은 이 글에 **없음(NOT FOUND)**.

[https://cloud.google.com/blog/products/data-analytics/hightouch-composable-cdp-built-on-bigquery | 저자 Nate Wardwell(Hightouch)·Tom Cannon(Google Cloud), 발행 2023-09-02 | 검색 시점 2026-07-25]
⚠️ **구버전 정보일 수 있음 (2023년 글).** "200+ destinations"라는 수치는 2023년 기준 — 현재 수치와 다를 수 있다.

#### A-1-e. RudderStack — 문서 조회 결과 (부분 확인)

`https://www.rudderstack.com/docs/`를 열었으나:
- RudderStack의 **공식 자기 정의 문장 → NOT FOUND** (해당 페이지에 없음)
- **warehouse-native / warehouse-first를 명시적으로 표방하는 문장 → NOT FOUND** (해당 페이지에 없음)
- 다만 **지원 이벤트 타입은 명시적으로 확인됨**: `Track`, `Identify`, `Screen`, `Group`, `Alias`, `Reset` + `Flush API`, `Shutdown API`
- Reverse ETL 기능과 웨어하우스 소스(Snowflake, BigQuery, Redshift, Databricks, PostgreSQL, MySQL, Trino, Amazon S3) 언급 확인
- 발행/갱신일 → NOT FOUND

[https://www.rudderstack.com/docs/ | 발행일 미표기 | 검색 시점 2026-07-25]

**주목:** RudderStack의 이벤트 타입 6종이 Segment Spec(§B-3-1)과 **거의 동일**하다 — `Reset`이 추가된 것 외에는 일치. 이건 업계 공통 문법이 존재한다는 강한 증거다.

#### A-1-f. Census — 독립 제품에서 Fivetran으로 흡수됨 (⚠️ 중요한 시장 변화)

- `https://www.getcensus.com/blog/what-is-a-composable-cdp` → **301 리다이렉트 → `https://www.fivetran.com/learn`** (호스트가 바뀜)
- 즉 **getcensus.com 도메인이 fivetran.com으로 넘어갔다.** 2026-07-25 시점에 확인.

Fivetran 공식 보도자료에서 확인한 사실:
- **발표일: 2025년 5월 1일** (May 1, 2025)
- Census 설명 (원문): "the leader in Reverse ETL, data activation, and operational analytics"
- Fivetran 측 인용: "Our Reverse ETL service has been pivotal in making that a reality for our customers"
- 거래 조건: "Terms of the deal were not disclosed."

[https://www.fivetran.com/press/fivetran-signs-agreement-to-acquire-census-delivering-the-first-end-to-end-data-movement-platform-for-the-ai-era | 발표 2025-05-01 | 검색 시점 2026-07-25]

⚠️ **책 저술 시 필수 반영:** "Hightouch / Census / RudderStack" 3강 구도로 컴포저블 CDP를 설명하면 **낡은 서술이 된다.** Census는 2025-05-01 Fivetran 인수 발표 이후 독립 브랜드로 존속하지 않는 것으로 보인다(도메인 리다이렉트로 확인). 다만 **Census 브랜드의 완전 소멸 여부는 `확인 불가`** — 리다이렉트만으로는 제품 단종을 단정할 수 없다.

**확인 불가 항목:** Census 창업연도(2018)·본사(샌프란시스코)·직원 수(50+)·CEO Boris Jabes 합류 — 전부 **검색 결과 요약에만 있고 1차 페이지에서 확인하지 못함**. 쓰려면 재확인 필요.

### A-2. CDP 유형 분류 — ✅ Raab 원문으로 확보 (단, task가 준 4분류와 다르다)

**글 제목:** "Why Are There So Many Types of Customer Data Platforms? It's Complicated."
**저자·발행일:** David Raab, Saturday, November 03, 2018

**Raab이 제시한 3단계 분류 (원문 조각):**

| 유형 | 원문 |
|---|---|
| **Data CDP** | "CDPs with a customer database" |
| **Analytics CDP** | "CDPs with a customer database plus customer analytics" |
| **Personalization CDP** | "a customer Database, analytics, and personalization" |

추가로 언급된 것: **Marketing Suite CDPs** — 실행(delivery) 시스템이 거꾸로 확장해 데이터베이스·분석·개인화를 흡수한 형태. 다만 Raab은 이런 것들이 CDP 정의를 의미 없을 정도로 늘린다고 지적한다. (요지)

**카테고리 혼란에 대한 Raab 본인의 진술 (원문):**

> "CDPs are not simple: the industry has rapidly evolved numerous subspecies of CDPs that are as different from each other as the different kinds of dinosaurs."

> "For CDP to have any meaning, it must describe a system whose primary purpose is to build a persistent, sharable customer database."

[http://customerexperiencematrix.blogspot.com/2018/11/why-are-there-so-many-types-of-customer.html | 2018-11-03 | 검색 시점 2026-07-25]

> ⚠️ **중요 — task가 준 4분류와 다르다.**
> 이 리서치에 주어진 커버 축은 "Data CDP / Analytics CDP / **Campaign** CDP / **Delivery** CDP"였다. 그러나 이 2018년 글에서 확인된 세 번째 유형은 **"Personalization CDP"**이며, **"Campaign CDP"·"Delivery CDP"라는 용어는 이 글에 등장하지 않는다** (WebFetch가 명시적으로 확인).
>
> **판정:**
> - `Data CDP` / `Analytics CDP` → **✅ Raab 2018 원문 확인**
> - `Personalization CDP` → **✅ Raab 2018 원문 확인** (task 목록에 없던 것)
> - `Campaign CDP` / `Delivery CDP` → **이 글에서는 확인 불가.** CDP Institute가 별도로 쓰는 용어일 가능성이 있으나 **cdpinstitute.org 403으로 검증 실패.**
>
> **책에 쓸 때:** "Data / Analytics / Personalization" 3분류를 2018년 Raab 기준으로 쓰고, Campaign/Delivery는 쓰지 마라. 또는 후속 리서치로 CDP Institute 원문을 확보한 뒤 쓰라.
> ⚠️ **8년 전 분류다.** 현재 CDP Institute의 공식 분류와 다를 수 있다 — 반드시 "2018년 Raab 기준"을 병기하라.

> **개발자 독자에게 이 3분류가 왜 유용한가:** 데이터베이스만 있는가(Data) / 그 위에 분석이 있는가(Analytics) / 그 위에 실행까지 있는가(Personalization) — **레이어가 쌓이는 순서**로 되어 있다. §A-1-b의 Hightouch(데이터를 저장조차 하지 않는 액티베이션 레이어)와 §B의 Insider(UCD + 세그먼트 + 채널 실행까지 전부)를 이 축 위에 놓으면 시장 지도가 바로 그려진다.

### A-3. DMP / CRM / MA / CEM / CEP의 정의와 경계

**대부분 `확인 불가 (1차 소스 미확보)`.** 이번 세션에서 확보한 것은 다음 뿐이다:

#### CEP(Customer Engagement Platform) — 벤더 자기 규정으로 확인
- Insider One: 자사를 "the leading Agentic Customer Engagement Platform" / "#1 Platform for AI-Powered Customer Engagement"로 규정 (벤더 자체 주장, §B 참조)
- Braze: `braze.com/docs` 홈페이지에는 "customer engagement platform"이라는 **명시적 자기 규정 문장이 없었다 (NOT FOUND)**. 확인된 가장 가까운 문장은 "Learn how to use the Braze platform to foster a more impactful customer experience."

> **관찰 (책에 쓸 만한 것):** CEP는 **애널리스트가 정의한 카테고리라기보다 벤더가 자기를 배치하는 라벨**로 쓰이고 있다. Insider는 제품 문서에서는 자기 데이터 계층을 "CDP"라 부르면서(§B-B), 회사 전체는 "Customer Engagement Platform"으로 규정한다. 이 이중 라벨링 자체가 "카테고리 경계가 왜 흐릿한가"의 실증 사례다.

#### CDP — 벤더가 스스로 "CDP"라고 쓴 1차 문장 3건 (CDP Institute 대체 근거)

CDP Institute 정의를 못 구한 대신, **벤더가 자기 제품을 CDP라고 규정한 원문 3건**은 확보했다. 정의 대신 "업계가 CDP라는 말을 어떻게 쓰는가"의 근거로는 쓸 수 있다.

| 벤더 | 원문 | 출처 |
|---|---|---|
| Adobe | "Use Adobe Real-Time Customer Data Platform (Real-Time CDP) to bring together known and anonymous data from multiple enterprise sources in order to create customer profiles that can be used to provide personalized customer experiences across all channels and devices in real time." | experienceleague.adobe.com/.../rtcdp/home |
| mParticle | "a customer data platform (CDP) that simplifies how you collect and connect your user data to hundreds of vendors without needing to manage multiple integrations." | docs.mparticle.com |
| Insider One | "the core Customer Data Platform (CDP) that powers all Insider One products" | academy.insiderone.com/.../unified-customer-database-ucd |

**세 문장의 공통 요소를 뽑으면** (이 리서치의 관찰, 인용 아님): ① 여러 소스의 데이터를 모은다 ② 고객 프로필/식별을 만든다 ③ 다른 시스템이 그걸 쓸 수 있게 한다. 세 벤더가 독립적으로 같은 세 가지를 말한다.

⚠️ 이건 **정의가 아니라 관찰**이다. 책에서 "CDP의 정의는 다음과 같다"고 쓰려면 여전히 CDP Institute 원문이 필요하다.

#### DMP(Data Management Platform) — 부분 확인

**Adobe Audience Manager**가 Adobe의 DMP 제품이며, 문서에서 확인된 자기 설명 (원문 조각):

> "an industry-leading service for online audience data management"

> 디지털 광고주·퍼블리셔에게 "the tools they need to control and leverage their data assets to help drive sales success"를 제공한다

- ⚠️ **"DMP"라는 용어 자체의 정의문 → NOT FOUND**
- ⚠️ **DMP vs CDP 대비 진술 → NOT FOUND**
- ⚠️ **서드파티 데이터·쿠키에 대한 설명 → NOT FOUND** (문서에 "Second and Third Party Data"라는 기능 항목은 존재)

[https://experienceleague.adobe.com/en/docs/audience-manager/user-guide/aam-home | 문서 표기 "last update May 21, 2026" | 검색 시점 2026-07-25]

> **확보한 것과 못 한 것을 분명히:** Adobe의 DMP 제품이 자기를 **"online audience data management"**라 부르고 대상 독자를 **"digital advertisers and publishers"**라고 밝힌 것은 확인했다. 이건 CDP(자사 고객 프로필 중심)와 대상·목적이 다르다는 **간접 근거**는 된다. 그러나 **"DMP는 서드파티 쿠키 기반이고 CDP는 퍼스트파티 데이터 기반이다"** 같은 흔한 설명은 **이 세션에서 어떤 1차 소스로도 확인하지 못했다.** 쓰지 마라.

#### MA(마케팅 자동화) — 부분 확인

**Adobe Marketo Engage** 문서 (원문):

> "Modern demand marketing strategies require end-to-end engagement to deliver the best possible customer experiences. Learn how to achieve this with Marketo Engage—part of Adobe Experience Cloud"

- ⚠️ **"marketing automation"이라는 카테고리의 독립적 정의문 → NOT FOUND.** 문서는 Marketo Engage의 기능(demand generation, 이메일·dynamic chat·CRM 연동)만 서술한다.

[https://experienceleague.adobe.com/en/docs/marketo/using/home | 문서 표기 "last update June 16, 2026" | 검색 시점 2026-07-25]

#### CRM / CEM
- **`확인 불가 (조회 실패 또는 미조회)`**
  - HubSpot CRM 개발자 문서(`developers.hubspot.com/docs/reference/api/crm/understanding-the-crm`) → **307 리다이렉트 → `app.hubspot.com` 로그인** (인증 필요)
  - Salesforce → `help.salesforce.com`은 JS 렌더 셸만 반환, `developer.salesforce.com` 경로 404 (§B-2-1)
  - CEM(Customer Experience Management) → **미조회**
- 다만 CRM 쪽 간접 근거 1건: 빅인(Bigin)이 "개인화된 CRM 자동화"라는 표현을 씀 (§B-2-4). 한국에서 "CRM 마케팅"이라는 용어가 글로벌의 CEP/MA 자리를 차지하고 있을 가능성 — **가설, 미검증.**

> **⚠️ A-3 축 총평 (research-lead에게):** "각 용어가 언제 왜 생겼는지"라는 task 요구 중 **CDP만 1차 소스로 답할 수 있다**(§A-0, 2013년 명명). DMP·MA·CRM·CEM의 기원과 정의는 이 리서치로 채우지 못했다. **벤더 제품 문서는 카테고리를 정의하지 않는다** — 이게 이번 라운드의 구조적 교훈이다. 카테고리 정의·역사는 애널리스트 글이나 위키피디아 같은 다른 소스 유형이 필요하다.

### A-4. "카테고리 경계가 왜 흐릿한가" — 확보한 실증 근거

애널리스트/벤더의 **공개 논평 텍스트는 확보하지 못했다** (`확인 불가`). 대신 **문서 대조로 직접 관찰된 경계 흐림 사례** 3건을 기록한다. 이건 인용이 아니라 이 리서치의 관찰이므로 책에서는 "문서를 열어보면 이렇다"는 형태로 써야 한다.

1. **한 회사가 두 카테고리를 동시에 주장한다.** Insider One은 회사 차원에서는 "Customer Engagement Platform"(insiderone.com), 제품 문서에서는 자사 UCD를 "the core Customer Data Platform (CDP)"라고 부른다(academy.insiderone.com). → CEP 안에 CDP가 모듈로 들어있는 구조.
2. **CDP라는 이름이 서로 다른 아키텍처를 가리킨다.** Hightouch는 "never copies your data"를 차별점으로 내세우는데(=데이터를 저장하지 않음), Insider UCD는 이벤트·속성을 자기 DB에 저장한다(=저장함). 둘 다 CDP라 불린다.
3. **인접 카테고리가 CDP 쪽으로 이동한다.** ETL 회사(Fivetran)가 Reverse ETL 회사(Census)를 인수해 "end-to-end data movement platform"이 되었다(2025-05-01). 커머스 광고 회사(Rokt)가 CDP(mParticle)를 "$300 million merger"로 합쳤다. 데이터 인프라·광고·마테크의 경계가 인수합병으로 지워지는 중.
4. **같은 일에 다른 라벨을 붙인다.** 이 리서치가 문서를 연 20개 벤더에서 확인된 자기 라벨: "Customer Data Platform"(Adobe·mParticle·Insider UCD), "Customer Engagement Platform"(Insider 회사 차원), **"Customer retention platform"(CleverTap)**, **"omnichannel messaging"(OneSignal)**, "마테크 솔루션"(그루비), "CRM 자동화"(빅인). → §B-2-5 요약표.
5. **CDP는 CEP의 부품이기도 하고 경쟁자이기도 하다.** Airship은 CDP를 "파트너 연동" 목록(analytics, CRMs, **CDPs**, marketing tools)에 넣는다 — 즉 데이터 공급자로 본다. 반면 Insider·Adobe는 CDP를 자기 안에 내장한다. 같은 카테고리가 누구에게는 부품, 누구에게는 모듈이다.

---

## B. Insider / Insider One

### B-A. 확인된 사실 vs 확인 불가 목록

#### ✅ 이 세션에서 1차 소스로 확인한 것

| 항목 | 확인 내용 | 출처 |
|---|---|---|
| 현재 브랜드명 | **"Insider One"** — 공식 도메인 `insiderone.com`, 문서 사이트 `academy.insiderone.com` | insiderone.com |
| 자기 규정 | "#1 Platform for AI-Powered Customer Engagement", "the leading Agentic Customer Engagement Platform" (벤더 자체 주장) | insiderone.com |
| 제품 모듈 라인업 | Insider One AI™, Customer Data Management, Personalization, Journey Orchestration, Reporting & Data, Behavioral Analytics | insiderone.com |
| AI 제품명 | **"Insider One AI™"**(우산 브랜드), **"Agent One™"**(에이전틱 AI) | insiderone.com |
| 채널 | Web, Email, Site Search, Conversational CX, WhatsApp, Web Push, InStory, App, SMS & RCS | insiderone.com |
| CDP 모듈 이름 | **Unified Customer Database (UCD)** — "the core Customer Data Platform (CDP) that powers all Insider One products" | academy.insiderone.com |
| 웹 태그 | `<script async src="//{partnerName}.api.useinsider.com/ins.js?id={partnerId}"></script>` | academy |
| API 호스트 | `https://unification.useinsider.com/api/user/v1/...` | academy |
| 인증 헤더 | `X-PARTNER-NAME`, `X-REQUEST-TOKEN` | academy |
| Series E | $500M, 리드 General Atlantic, 발표 **2024-11-01**, "28 countries across five continents" | insiderone.com/news |
| 고객 규모 주장 | "Insider One enables 1,500+ customers across the globe, including Nike, Samsung, L'Oreal, Unilever, Allianz, Walt Disney, ING Group, Toyota, Singapore Airlines, and GAP..." (벤더 자체 주장) | insiderone.com/news |

#### ❌ 확인 불가 (조회했으나 근거 못 찾음)

| 항목 | 상태 |
|---|---|
| 설립 연도 | **확인 불가** — `insiderone.com/about/`는 채용 페이지였고 창업 정보 없음. 보도자료 boilerplate에도 없음 |
| 본사 소재지 | **확인 불가** — 보도자료 발신지가 New York으로 표기됐을 뿐, "headquarters" 명시 없음 |
| 총 누적 투자액 | **확인 불가** (1차 소스에서 NOT FOUND) |
| 기업 가치·유니콘 등극 시점 | **확인 불가** (1차 소스에서 NOT FOUND) |
| 한국 법인/오피스 유무 | **확인 불가 (미조회)** |
| 내부 아키텍처 (DB 종류, 스트리밍 엔진 등) | **공개 자료 없음** — Insider가 스스로 공개한 자료를 찾지 못했다. 추정 금지 |

> ⚠️ **중요:** 설립연도 2012 / 이스탄불 본사 / 2022년 유니콘 / 누적 $772M 같은 숫자는 검색 결과 요약(Tracxn·PitchBook·Tech.eu 등)에만 있었고 **1차 페이지에서 확인하지 못했다.** 책에 쓰려면 재확인이 필요하다. 지금 상태로는 `(2차 인용, 미검증)`.

### B-B. Unified Customer Database (UCD) — Insider의 CDP 레이어

> "the core Customer Data Platform (CDP) that powers all Insider One products"

핵심 개념 3종 (문서 원문 기준):
- **Identifiers** — "anything specific to the user" (이메일 주소, 전화번호, user ID 등). 여러 소스의 데이터를 하나로 묶는 열쇠.
- **Events** — "User actions across all online and offline channels, including add-to-carts, purchases, visits, and logins." 이벤트는 파라미터를 가질 수 있다("Product Name", "Product Color" 등).
- **Attributes** — "enable you to collect users' information, such as age, gender, birthday, and singular items for each user" (예: "Last Visited Product")

[https://academy.insiderone.com/docs/unified-customer-database-ucd | 페이지 표기 Published/Updated 2026-04-22 (문서 사이트 표기 — 최초 발행일/갱신일 구분 불가) | 검색 시점 2026-07-25]

**개발자용 멘탈 모델:** identifiers = 조인 키 / events = append-only 시계열 / attributes = 사용자 행의 컬럼. Segment의 `userId`+`traits`+`track` 3분할과 거의 같은 구조다(§B-3-1 대조).

**관련 섹션:** "CDP 안에는 무엇이 들어있나" 챕터. 벤더가 다르면 이름만 다르고 개념은 같다는 걸 보여주는 대조표의 한 축.

### B-C. Insider 웹 SDK — 개발자가 실제로 만지는 표면 (1차, 매우 구체적)

**태그 스크립트 (원문):**
```html
<script async src="//{partnerName}.api.useinsider.com/ins.js?id={partnerId}"></script>
```

**큐 객체 (원문):**
```javascript
window.InsiderQueue = window.InsiderQueue || [];
```
- 큐는 Insider 태그가 로드되기 **전에** 정의되어야 한다.
- 데이터 푸시 패턴: `window.InsiderQueue.push({type: 'method_type', value: {...}})`

**사용자 속성 스키마 (`type: 'user'`) — 문서 표 원문:**

필수 식별자(최소 1개): `uuid`, `email`, `phone_number`

| Field | Type | Required | Sample |
|-------|------|----------|--------|
| `uuid` | String | No* | "INS123" |
| `email` | String | No* | "jdoe@useinsider.com" |
| `phone_number` | String (E.164) | No* | "+120394879878" |
| `name` | String | No | "John" |
| `surname` | String | No | "Doe" |
| `gender` | String | No | "M" |
| `birthday` | Datetime | No | "2000-01-20T00:00:00Z" |
| `age` | Number | No | 33 |
| `language` | String | No** | "en_US" |
| `country` | String (ISO-3166 alpha-2) | No | "ID" |
| `city` | String | No | "Jakarta" |
| `email_optin` | Boolean | No | true |
| `sms_optin` | Boolean | No | true |
| `whatsapp_optin` | Boolean | No | false |
| `gdpr_optin` | Boolean | No*** | true |
| `custom` | Object | No | {"membership": "Silver"} |

\* 최소 1개 식별자 필수 / \*\* 다수 유스케이스에서 필요 / \*\*\* GDPR 준수 시 필요

**페이지 타입 메서드 (원문):**
| type | 발생 이벤트 | 비고 |
|---|---|---|
| `home` | "Home Page View" (`home_page_view`) | |
| `category` | "Listing Page View" (`listing_page_view`) | `breadcrumb` 배열 필요 |
| `product` | "Product Page View" (`product_detail_page_view`) | |
| `cart` | "Cart Page View" (`cart_page_view`) | |
| `purchase` | "Purchase" (`confirmation_page_view`) | |
| `other` | "Other Page View" (`other_page_view`) | |

**이벤트 메서드 (원문):**
- `type: 'add_to_cart'` / `type: 'remove_from_cart'` → `item_added_to_cart` / `item_removed_from_cart`
- `type: 'custom_event'` → `event_name` 파라미터 필수, `event_parameters` 객체 허용
- `type: 'init'` — "Critical initialization trigger (must fire once per page after user/page data)"
- `type: 'currency'` — 사용자 통화 설정 (예: "USD")

[https://academy.insiderone.com/docs/insider-web-sdk-integration-guide | 페이지 표기 Published 2026-07-23T13:40:34Z (문서 사이트 표기 — 최초 발행일/갱신일 구분 불가) | 검색 시점 2026-07-25]

> ⚠️ **책에 쓸 만한 관찰 — 브랜드는 바뀌었지만 API는 안 바뀌었다.**
> 브랜드·문서 도메인은 `insiderone.com`인데, **태그 스크립트 호스트는 여전히 `useinsider.com`**이고 샘플 이메일도 `jdoe@useinsider.com`이다. API 호스트도 `unification.useinsider.com`. 리브랜딩이 프레젠테이션 레이어에만 적용되고 데이터 평면은 레거시 도메인을 유지하는, 실무에서 아주 흔한 패턴. (2026-07-25 시점 관찰)

### B-D. Insider REST API — 엔드포인트·헤더·레이트 리밋 (1차)

#### 인증
- 헤더 2종: `X-PARTNER-NAME`, `X-REQUEST-TOKEN`
- 문서 원문 주의사항: "Header names vary by API. The pattern below applies to the Unification and UCD APIs. For SMS, WhatsApp, Email, Web Push, Recommendation, and Eureka, check the header names on each API's own reference page."
- 예시 엔드포인트: `https://unification.useinsider.com/api/user/v1/profile`
- 레이트 리밋 언급 → 이 페이지에는 **NOT FOUND** (별도 페이지 참조)

[https://academy.insiderone.com/docs/api-authentication-tokens | 페이지 표기 2026-07-23T08:54:35Z (문서 사이트 표기) | 검색 시점 2026-07-25]

#### Upsert User Data API — 데이터 인입의 핵심 엔드포인트

- **엔드포인트:** `https://unification.useinsider.com/api/user/v1/upsert`
- **메서드:** `POST`
- **헤더:** `X-PARTNER-NAME`(소문자 partner name), `X-REQUEST-TOKEN`, `Content-Type: application/json`

**요청 바디 스키마 (문서 기준 필드명):**

최상위:
- `skip_hook` (boolean, optional) — 임포트된 데이터가 Architect 저니를 트리거할지 제어
- `error_callback_endpoint` (URL, optional) — unification 에러 통지 엔드포인트
- `users` (array, **required**)

user 객체:
- `insider_id` (string) **또는** `identifiers` (object) — 둘 중 하나 필수
- `attributes` (object, optional)
- `events` (array, optional)
- `not_append` / `append` (boolean, optional) — 속성 덮어쓰기 동작 제어

`identifiers` 객체: `email`, `phone_number`, `uuid`, 또는 커스텀 식별자

event 필드:
- `event_name` (string, **required**)
- `timestamp` (**RFC 3339** 형식, **required**)
- `event_params` (object, optional)
- `event_group_id` (string, purchase/cart_page_view 이벤트에 required)

**배치·레이트 제한:**
- 요청당 최대 **1,000 users**
- 레이트 리밋 **25,000 requests/minute** (Delete User Attribute API와 공유)
- 요청 크기 **최대 5 MB**

[https://academy.insiderone.com/docs/upsert-user-data-api | 페이지 내 참조 날짜 2026-07-24 | 검색 시점 2026-07-25]

#### API 레이트 리밋 전체표 (2026-07-12 문서 표기 기준)

**개발자 독자에게 이 표가 왜 중요한가:** Martech 백엔드를 다루는 개발자가 가장 먼저 부딪히는 벽이 레이트 리밋이다. 채널별로 3~4 자릿수 차이가 난다.

**Unification APIs**
| API | 리밋 |
|---|---|
| Upsert User Data | "25,000 requests per minute" |
| Export Raw User Data | **"1 request per day"** |
| Delete User Attribute | "25,000 requests per minute" |
| Update Identifiers | "2000 requests per minute" |
| Delete Identifiers | "1,000 requests per minute" |
| Delete User Profiles | "10,000 requests per minute" |
| Delete User's PII Data | "500 requests per minute" |

**Contact APIs**
| API | 리밋 |
|---|---|
| Upload First-Party Segments | "100 requests per second" |
| Resubscribe Email Users V1 | "600 requests per minute" |
| Resubscribe SMS Users | "600 requests per minute" |
| Resubscribe WhatsApp Users | "600 requests per minute" |

**Web Push APIs**
| API | 리밋 |
|---|---|
| Create/Launch/Delete Single Web Pushes (V1) | "30 requests per minute" |
| Launch Single Web Pushes V2 | "6000 requests per minute" |
| Web Push Analytics | "30 requests per minute in aggregate" |

**Mail APIs**
| API | 리밋 |
|---|---|
| Send Transactional Emails | **"9000 requests per second"** |
| Create Email Campaigns | "1 request per second" |
| Template Migrator (V1 & V2) | "60 requests per minute" |

**Mobile APIs**
| API | 리밋 |
|---|---|
| Send Bulk/Basic Segment App Pushes | "1000 requests per minute" |
| Send Targeted App Pushes | "10000 requests per minute" |
| Send Advanced App Pushes | "1000 requests per minute" |
| Message Center API | "5000 requests per minute" |
| InApp Details | "1000 requests per minute" |
| FCM Certificate | "1000 requests per minute" |

**기타**
| API | 리밋 |
|---|---|
| Verify (channels/templates) | "25 requests per minute" |
| Verify (OTP 생성/검증) | "750 requests per minute" |
| SMS Transactional Single | "200 requests per second" |
| SMS Transactional Bulk | "5 requests per second" |
| SMS Analytics | "100 requests per minute" |
| WhatsApp Transactional | "1000 requests per second" |
| WhatsApp Conversational | "10 requests per second" |
| Analytics APIs | "100 requests per minute" |
| Architect Analytics APIs | "200 requests per minute" |
| Catalog APIs | "60 requests per minute" |
| Recommendation APIs | "1000 calls per minute" |

[https://academy.insiderone.com/docs/api-rate-limits | 페이지 표기 2026-07-12T12:39:05Z (문서 사이트 표기) | 검색 시점 2026-07-25]

⚠️ **버전·수치 규율:** 위 숫자는 전부 **2026-07-12 문서 표기 기준**이다. 레이트 리밋은 벤더가 예고 없이 바꾼다. 책에 넣을 때 "2026년 7월 문서 기준"을 반드시 병기하라.

**관련 섹션:** "Martech 백엔드는 왜 배치와 스트리밍을 둘 다 갖는가" / "레이트 리밋과 백프레셔" 챕터.

#### User Data API 목록 (엔드포인트 미확인)

문서 오버뷰에서 확인한 6종:
1. Upsert User Data API
2. Get User Profiles API
3. Export Raw User Data API
4. Delete User Attribute API
5. Update Identifiers API
6. Delete Identifiers API

⚠️ 이 오버뷰 페이지에는 엔드포인트 URL·HTTP 메서드·헤더·필드명이 **NOT FOUND**(개별 문서 페이지에 있음).

[https://academy.insiderone.com/docs/ucd-user-data-apis-overview | 페이지 표기 Published/Updated 2026-07-14T14:30 (문서 사이트 표기) | 검색 시점 2026-07-25]

> **관찰:** 6개 API 중 **4개가 삭제/수정 계열**(Delete User Attribute, Delete Identifiers, Update Identifiers, 그리고 별도 Delete User Profiles / Delete PII)이다. CDP API 표면의 절반이 GDPR·개인정보 삭제 요구를 처리하기 위한 것 — 개발자 독자에게 "마테크에서 규제는 부가 기능이 아니라 API 설계의 절반"이라는 점을 보여주는 근거.

### B-E. Segments — 오디언스 레이어

일반 오버뷰 페이지에서는 정의문을 얻지 못했다(NOT FOUND). 확인된 것:
- 오디언스 세그먼트는 "behavior, interests, unique attributes, affinity, purchase history, and more"를 근거로 생성된다. (요지 — 원문 조각)
- [https://academy.insiderone.com/docs/audience-segments-overview | 페이지 표기 2026-04-17 | 검색 시점 2026-07-25]

**Predictive Segments — 예측 세그먼트 5종 (확인됨):**
1. Likelihood to Purchase
2. User Engagement
3. Customer Lifecycle Status
4. Discount Affinity
5. Attribute Affinity

작동 설명 (원문 조각): "leverage algorithms that predict users' likelihood to purchase and segment users based on their interests and purchase behaviors"

⚠️ **사용하는 ML 모델에 대한 서술 → NOT FOUND.** 어떤 모델·피처를 쓰는지 **공개 자료 없음**. 추정 금지.

[https://academy.insiderone.com/docs/audience-predictive-segments | 페이지 표기 2026-04-12 | 검색 시점 2026-07-25]

문서 인덱스(llms.txt)에서 확인한 세그먼트 문서 URL:
- `https://academy.insiderone.com/docs/audience-segments-overview.md`
- `https://academy.insiderone.com/docs/dynamic-segments.md`
- `https://academy.insiderone.com/docs/audience-predictive-segments.md`
- `https://academy.insiderone.com/docs/rfm-segments.md`

→ **RFM 세그먼트**가 별도 문서로 존재. (RFM = Recency/Frequency/Monetary, 고전 마케팅 세그멘테이션 기법. 이 문서 자체는 미조회 → 내용 `확인 불가`)

### B-F. Insider 모바일 SDK

**iOS SDK (GitHub 1차):**
> "Insider iOS SDK provides a set of frameworks for integrating Insider services into your iOS application. The SDK includes modules for mobile interaction, geofencing, and advanced notifications."

모듈·버전 (README 표기):
| 모듈 | 버전 |
|---|---|
| InsiderMobile | v15.1.1 |
| InsiderGeofence | v1.2.4 |
| InsiderMobileAdvancedNotification | v2.4.0 |
| InsiderWebView | v1.0.0 |
| InsiderLiveActivities | v1.0.0 |

- 리포지터리 최신 릴리스 표기: **v1.9.1** (릴리스 날짜는 이 페이지에서 NOT FOUND)
- 설치 안내: "See Insider's iOS SDK Setup for documentation" → `academy.insiderone.com/docs/ios-basic-sdk-setup`
- API 메서드명 → README에는 **NOT FOUND**

[https://github.com/useinsider/Insider-iOS-SDK | 발행일 미표기 (버전 v15.1.1 / 2026년 7월 조회 기준) | 검색 시점 2026-07-25]

⚠️ **상충 주의:** GitHub 조직 이름은 `useinsider`(레거시), 표시 이름은 `InsiderOne`. 모듈 버전(InsiderMobile v15.1.1)과 리포 릴리스 태그(v1.9.1)가 서로 다른 체계다 — 인용 시 어느 쪽 버전인지 명시할 것.

**iOS 초기화 코드·메서드명:** `ios-basic-sdk-setup` 페이지는 인덱스 페이지였고 실제 코드가 **NOT FOUND**. 실제 코드는 `/docs/ios-initialize-sdk`에 있다고 안내됨 → **미조회, `확인 불가`**.
[https://academy.insiderone.com/docs/ios-basic-sdk-setup | 페이지 표기 2026-01-04T18:01:23Z | 검색 시점 2026-07-25]

**Flutter:** `flutter_insider` 패키지가 pub.dev에 존재 (검색 결과로만 확인, 페이지 미조회 → 세부사항 `확인 불가`)

**Android:** `github.com/useinsider/KotlinDemo` 존재 (검색 결과로만 확인 → 세부사항 `확인 불가`)

### B-G. Insider 문서 구조 (llms.txt로 확인)

`academy.insiderone.com`은 **`/llms.txt` 문서 인덱스를 제공한다** — AI 에이전트용 문서 색인을 갖춘 최신 문서 사이트 패턴. 최상위 섹션:
1. Getting Started
2. Integration & Setup (SDK, data, channels, product catalogs)
3. Audience & Segmentation
4. Campaign Management (Email, Web Push, App Push, WhatsApp, SMS)
5. Analytics & Reporting
6. Administration

확인된 채널 문서 URL:
- Email: `https://academy.insiderone.com/docs/email-channel.md`
- Web Push: `https://academy.insiderone.com/docs/web-push-overview.md`
- App Push: `https://academy.insiderone.com/docs/app-push.md`
- WhatsApp: `https://academy.insiderone.com/docs/whatsapp-overview.md`
- SMS: `https://academy.insiderone.com/docs/developer-guide-sms-channel-setup.md`
- Recommendation: `https://academy.insiderone.com/docs/recommendation-setup-1.md`
- **Eureka**: `https://academy.insiderone.com/docs/developer-guide-eureka-setup.md` (제품명 "Eureka" — 사이트 서치 계열로 추정되나 **미조회, 기능 `확인 불가`**)

[https://academy.insiderone.com/llms.txt | 발행일 미표기 | 검색 시점 2026-07-25]

⚠️ **Architect(저니 오케스트레이션) 문서:** `academy.insiderone.com/docs/architect-overview` → **404**. llms.txt에서도 해당 섹션이 잘려 확인 못 함. 다만 Upsert API의 `skip_hook` 필드 설명에 "Architect journeys"가 등장하므로 **Architect가 저니 오케스트레이션 제품명이라는 점은 간접 확인**됨. 세부 기능은 `확인 불가`.

---

## B-2. 경쟁·인접 제품

> **읽는 법:** 아래는 전부 **각 벤더의 공식 문서 페이지를 이 세션에서 직접 열어** 얻은 것이다. 따옴표 안은 원문, 그 밖은 요지. "NOT FOUND"는 그 페이지에 해당 문장이 없었다는 뜻이지 "그 회사가 그렇지 않다"는 뜻이 아니다.
>
> **자기 규정 문장을 못 찾은 벤더가 많다는 것 자체가 발견이다.** 여러 벤더가 자기 문서 첫 페이지에서 "우리는 X 플랫폼이다"라고 말하지 않는다. 카테고리 이름은 문서가 아니라 세일즈 자료에 산다.

### B-2-1. 패키지형 CDP 계열

#### Adobe Real-Time CDP — 유일하게 정의문이 또렷한 케이스

> "Use Adobe Real-Time Customer Data Platform (Real-Time CDP) to bring together known and anonymous data from multiple enterprise sources in order to create customer profiles that can be used to provide personalized customer experiences across all channels and devices in real time."

- **개발자 통합 표면:** Adobe Experience Platform 위에 네이티브로 얹혀 있고, 데이터 모델은 **XDM(Experience Data Model)** 스키마를 쓴다.
- [https://experienceleague.adobe.com/en/docs/experience-platform/rtcdp/home | 문서 표기 2026-06-18 | 검색 시점 2026-07-25]

**XDM — 개발자가 실제로 다루는 스키마 시스템 (1차):**

> XDM 정의: "A publicly documented specification designed to improve the power of digital experiences. It provides common structures and definitions that allow any application to use to communicate with Experience Platform services."

> **XDM Individual Profile**: "A record-based class that forms a singular representation of the attributes of both identified and partially identified subjects."

> **XDM ExperienceEvent**: "A time-series-based class used to capture the state of the system when an event (or set of events) occurred, including the point in time and identity of the subject involved."

스키마 구성 (요지): 스키마는 "a base class and zero or more schema field groups"로 이루어진다. Schema Library가 표준 XDM 컴포넌트를 제공하고, 커스텀 스키마도 만들 수 있다.

[https://experienceleague.adobe.com/en/docs/experience-platform/xdm/home | 문서 표기 "Last update May 23, 2026" | 검색 시점 2026-07-25]

**Real-Time Customer Profile (1차):**

> "see a holistic view of each individual customer by combining data from multiple channels, including online, offline, CRM, and third party"

> union schema: "a merged view of all profile fragments for that entity across datasets, referred to as the 'union view' and made possible through what is known as a union schema"

> XDM Individual Profile은 "the preferred class upon which to build a schema when describing customer record data"

> XDM ExperienceEvent에 대해: "time series data can describe events such as items being added to a cart, links being clicked, and videos viewed"

⚠️ identity graph / identity namespace의 명시적 정의문 → **NOT FOUND** (문서에 "an identity graph for each customer"라는 표현은 등장하나 정의는 없음)

[https://experienceleague.adobe.com/en/docs/experience-platform/profile/home | 문서 표기 2026-07-03 | 검색 시점 2026-07-25]

> **이 자료가 책에서 갖는 가치:** Adobe의 `XDM Individual Profile`(레코드 기반, 시간 무관 속성) vs `XDM ExperienceEvent`(시계열, 불변) 이분법은 **모든 CDP의 내부 구조를 설명하는 가장 명료한 1차 문장**이다. Insider의 `attributes` vs `events`, Segment의 `traits` vs `track`과 정확히 같은 축이다. 개발자에게 "CDP 안에는 사용자 테이블 하나와 이벤트 로그 하나가 있다"를 벤더 원문으로 뒷받침할 수 있다.

#### mParticle (현재: mParticle by Rokt)

> 자기 규정 (문서 원문): "a customer data platform (CDP) that simplifies how you collect and connect your user data to hundreds of vendors without needing to manage multiple integrations."

- **SDK:** Android, iOS, Web
- **API 표면:** Events API (HTTP / Node / Python / Ruby 구현 제공), **Profile API** — "Real-time API to drive user personalization", **Firehose API** — "Build your own custom integrations"
- 아이덴티티: "Manage user identities with **IDSync**" (제품명 IDSync)
- ⚠️ `MPID`, "Identity API" 라는 명칭 → 이 페이지에서 **NOT FOUND**
- [https://docs.mparticle.com/ | 문서 표기 "Last Updated: 7/16/2026" | 검색 시점 2026-07-25]

**⚠️ 소유권 변경 — 책에 반영 필요:**
- `developer.mparticle.com` → **DNS 조회 실패 (ENOTFOUND)** — 구 개발자 도메인이 사라졌다.
- mParticle 공식 뉴스룸: **"$300 million merger"** (원문 표기). mParticle을 "real-time customer data platform (CDP)"로 지칭.
- mParticle 측 문장: "At mParticle, our mission has always been to simplify customer data management and empower multi-channel brands to create meaningful connections with their customers."
- 발표일 → 이 페이지에서 **NOT FOUND**. (검색 결과 요약은 2025년 1월이라 하나 **1차 확인 불가**)
- [https://www.mparticle.com/news/rokt-and-mparticle-merge/ | 발행일 미표기 | 검색 시점 2026-07-25]

#### Twilio Segment

- `https://segment.com/docs/` → **HTTP 403 Forbidden** (사이트 전역 봇 차단)
- 문서 소스 리포지터리에서 확인된 유일한 자기 설명 문장: **"Learn how to use Segment to collect, responsibly manage, and integrate your customer data with hundreds of tools."**
- "CDP"라는 자기 규정, Connections/Protocols/Unify/Engage 제품 구분 → **NOT FOUND**
- [https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/index.md | 발행일 미표기 | 검색 시점 2026-07-25]

⚠️ Segment의 실질적 기여는 제품보다 **Spec(§B-3-1)**이다. 카테고리 자기 규정은 확보 실패.

#### Bloomreach Engagement

- 자기 규정(카테고리 라벨) → **NOT FOUND**
- **데이터 모델 3종:** Customers / Events / Catalogs
  - Customers (원문): "Understand how the platform recognizes and merges customer profiles using **hard IDs and soft IDs**"
  - Catalogs: 상품·콘텐츠 저장소 (검색 가능한 속성 보유)
- **SDK:** Web(JavaScript SDK), iOS, Android, React Native, Flutter, MAUI, Xamarin, Python SDK(GitHub)
- 모바일 SDK 설명 (원문): "iOS, Android, and other framework SDKs to track behavior, send push notifications, and personalize in-app content"
- **API 표면:** REST API — "Authenticate, call the API, and work with available methods to send and retrieve data", Webhook(시나리오 자동화), **Kafka 연동(직접 데이터 스트리밍)**
- 발행일: 상대 시각 표기만("about 2 months ago"), 절대 날짜 **NOT FOUND**
- [https://documentation.bloomreach.com/engagement/docs | 발행일 미표기 | 검색 시점 2026-07-25]

> **주목 — hard ID vs soft ID.** Bloomreach는 식별자를 두 등급으로 나눈다. 이건 Segment의 `userId` vs `anonymousId`와 같은 문제의 다른 이름이다. **식별자 이원화는 CDP 전 벤더의 공통 설계**라는 걸 보여주는 세 번째 사례(Segment / Insider / Bloomreach).
> **Kafka 연동을 문서 첫 페이지에 노출한 유일한 벤더**이기도 하다 — 개발자 친화 지표.

#### Salesforce Data Cloud — 확인 실패
- `https://developer.salesforce.com/docs/data/data-cloud-dev/overview` → **404**
- `https://developer.salesforce.com/docs/data/data-cloud-ref/guide/c360dm-api.html` → **404**
- `https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-develop.html` → **404**
- `https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud.htm&type=5` → 페이지는 열렸으나 **JS 렌더링 셸만 반환, 내용 NOT FOUND**
- **판정: `확인 불가 (2026-07-25 조회 실패 — 문서 URL 구조 변경 추정 + JS 렌더링 의존)`**

### B-2-2. CEP / 캠페인·저니 오케스트레이션 계열

#### Braze
- 자기 규정 카테고리 문장 → **NOT FOUND**. 문서 홈에서 확인된 가장 가까운 문장: "Learn how to use the Braze platform to foster a more impactful customer experience." / "Integrate and activate your app or site with the Braze SDK."
- REST API 자기 설명 (원문): **"Braze provides a high-performance REST API to allow you to track users, send messages, export data, and more."**
- 문서 홈 상단 노출 개발자 표면: **"POST: Track users endpoint"**, **"User attributes object"**
- SDK 플랫폼 목록, Canvas(저니 오케스트레이션) → 이 페이지에서 **NOT FOUND**
- [https://www.braze.com/docs/ | 발행일 미표기 | 검색 시점 2026-07-25]

⚠️ Braze를 "customer engagement platform"이라 부르는 서술은 **이 세션에서 원문 확인 실패**. 널리 그렇게 알려져 있으나 인용하지 말 것.

#### MoEngage
- 슬로건 (원문): **"Engage your users with intelligent, cross-channel experiences"**
- 카테고리 자기 규정 → **NOT FOUND**
- **SDK:** iOS(Swift & Objective-C), Android(Kotlin & Java), Web(JavaScript), React Native, Flutter, Unity
- **API 표면 (원문):** "Explore endpoints for data ingestion, campaigns, segments, templates, subscriptions, and more."
- ⚠️ `developers.moengage.com` → **301 리다이렉트 → `moengage.com/docs/`** (개발자 서브도메인이 본 사이트로 흡수됨)
- 발행일 → **NOT FOUND**
- [https://moengage.com/docs/ | 발행일 미표기 | 검색 시점 2026-07-25]

#### CleverTap
- 자기 규정 (원문): **"Customer retention platform that provides the functionality to integrate app analytics and marketing."**
  → **"retention platform"** — CDP도 CEP도 아닌 제3의 라벨을 쓴다. 카테고리 명명이 얼마나 제각각인지 보여주는 좋은 사례.
- **SDK (9종, 이 리서치가 확인한 최다):** iOS, Android, Cordova, Flutter, React Native, Unity, Web, **KaiOS**, **Unreal**
- **API 표면:** Event APIs의 "Upload Events", Profile APIs의 "Upload User Profiles"
- 발행일: 상대 시각("7 months ago")만, 절대 날짜 **NOT FOUND**
- [https://developer.clevertap.com/docs/ | 발행일 미표기 | 검색 시점 2026-07-25]

#### OneSignal
- 자기 설명 (원문): **"Start building faster with comprehensive guides, example code, and platform overviews for omnichannel messaging."**
- 카테고리: **"omnichannel messaging"** (= 메시징 인프라 성격. CDP 아님)
- **채널:** Push(모바일·웹), Email, SMS & RCS, In-app messages, Live Activities(iOS)
- **API 표면:** REST API, SDK, Webhooks
- SDK 플랫폼 목록 → 이 페이지에서 **NOT FOUND**
- 발행일 → **NOT FOUND**
- [https://documentation.onesignal.com/docs | 발행일 미표기 | 검색 시점 2026-07-25]

#### Airship
- 자기 설명 (원문): **"your complete guide to push notifications, SMS, email, in-app messaging, Scenes, and more"**
- 카테고리 라벨 → **NOT FOUND**
- **SDK:** iOS, Android, Web, React Native, Flutter
- **채널:** Push, SMS/MMS/RCS, Email, In-app messaging, **Scenes**(네이티브 인앱·웹 경험), **Wallet**
- **API 표면 (요지):** messaging / audience operations / **event streaming** / wallet workflows용 REST API, Open Channel API 연동, 파트너 연동(analytics, CRMs, **CDPs**, marketing tools)
- 문서 내 최신 항목 날짜: **2026-07-23** (Message Center Scenes 릴리스)
- ⚠️ `docs.airship.com` → **301 → `www.airship.com/docs/`**
- [https://www.airship.com/docs/ | 문서 내 최신 항목 2026-07-23 | 검색 시점 2026-07-25]

> **Airship이 "파트너 연동" 목록에 CDP를 넣은 것**이 카테고리 경계를 보여준다. 메시징 벤더는 CDP를 **경쟁자가 아니라 데이터 공급자**로 본다.

#### Adobe Journey Optimizer
- 정의 (원문): **"An enterprise application for creating and delivering connected, contextual, and personalized customer experiences across all channels and touchpoints."**
- Real-Time CDP / Experience Platform과의 관계 (원문): "is built natively on Adobe Experience Platform, sharing its data foundation, identity graph, and governance services."
- [https://experienceleague.adobe.com/en/docs/journey-optimizer/using/get-started/get-started | 문서 표기 "Last updated July 1, 2026" | 검색 시점 2026-07-25]

> **Adobe 사례가 CDP와 CEP의 관계를 가장 명료하게 드러낸다.** Real-Time CDP = 데이터 기반(프로필·아이덴티티 그래프), Journey Optimizer = 그 위에서 저니를 실행하는 애플리케이션. **둘이 같은 Experience Platform 데이터 기반을 공유한다.** 이 분리가 Insider(UCD + Architect), Braze(users + Canvas) 등 다른 벤더에서도 같은 형태로 반복된다.

#### Klaviyo
- **API 버저닝 방식 (개발자에게 중요):** **날짜 기반 버저닝.** 문서에 노출된 버전들: `v2022-10-17`, `v2023-01-24`, `v2023-06-15`, `v2024-02-15`, `v2024-10-15`, `v2025-01-15`, **`v2026-07-15`(조회 시점 최신)**
- **코어 리소스:** Profiles / Events / Lists / Segments / Campaigns / Flows
- **인증 3종:** "Private key authentication" (`Authorization: Klaviyo-API-Key` 헤더), 테크 파트너용 OAuth, 클라이언트사이드 엔드포인트용 "Public key authentication"(company ID/site ID)
- **레이트 리밋 (원문):** "fixed-window rate limiting algorithm with two distinct windows: burst (short) and steady (long)" — 초과 시 HTTP 429
- API 스타일: **JSON:API** 규약 채택, `relationships` 객체 사용
- SDK 구체 목록 → **NOT FOUND** ("Install one of our new SDKs" 안내만)
- [https://developers.klaviyo.com/en/reference/api_overview | 최신 API 버전 v2026-07-15 기준 | 검색 시점 2026-07-25]

> **Klaviyo의 날짜 버저닝 + burst/steady 이중 레이트 리밋 창**은 책에서 "마테크 API는 어떻게 진화하는가"를 설명할 때 Insider(단일 분당 리밋)와 대조하기 좋은 1차 사례다.

#### Iterable — 확인 실패
- `https://support.iterable.com/hc/en-us/categories/360002357451-API-Docs` → **HTTP 403 Forbidden**
- **판정: `확인 불가 (2026-07-25 조회 실패)`**

#### Salesforce Marketing Cloud — 미조회
- **판정: `확인 불가 (미조회)`**

### B-2-3. 어트리뷰션(MMP) 계열 — CDP/CEP와 카테고리가 다르다

> **⚠️ 카테고리 구분 근거의 한계를 먼저 밝힌다.** "어트리뷰션 제품은 CDP/CEP와 다르다"를 **벤더가 스스로 선언한 문장으로는 확보하지 못했다.** 아래는 각 벤더 공식 문서의 **기능 목록·API 이름**에서 드러나는 차이다. 책에 쓸 때는 "문서를 열어보면 API 이름이 다르다"는 관찰 형태로 서술하고, 정의로 단정하지 마라.

#### AppsFlyer
- 자기 설명 (원문): **"AppsFlyer empowers marketers and helps them make better decisions."** (카테고리 라벨 아님)
- SDK 연동 시 (원문): **"attribution out-of-the-box"**
- 기능 축: Cross-platform attribution / Mobile and web analytics / Fraud detection / Privacy management and preservation
- **SDK:** 네이티브 Android·iOS + 플러그인 Unity, React Native, Flutter
- **API 표면:** Server-to-server events API (mobile), App list API, App management API V2.0, User management API, **Click Signing API**
- ⚠️ "install attribution" / "conversion"의 정확한 표현 → **NOT FOUND**
- [https://dev.appsflyer.com/hc/docs | 발행일 미표기 | 검색 시점 2026-07-25]

#### Adjust
- 자기 규정 문장 → **NOT FOUND**
- **SDK (14종):** Android, iOS, Unity, Flutter, React Native, Cordova, Cocos2d-x, MAUI, Corona, Web, Smart Banner, Windows, **Steamworks**, Adobe Experience Extension
- 측정 기능 (원문 조각): "Send event information", "Record ad revenue information", **"Get attribution information"**, "Send subscription information", "Uninstall and reinstall measurement"
- [https://dev.adjust.com/en/sdk | © 2026 Adjust GmbH 표기, 발행일 미표기 | 검색 시점 2026-07-25]

#### Airbridge (AB180) — 한국 벤더
- API 자기 설명 (원문): **"Airbridge provides an environment where you can maximize your marketing performance through an API."**
- API 스타일 (원문): "is organized in the form of REST, has a resource-oriented URL, returns JSON responses, and uses standard HTTP response codes and authentication."
- 카테고리 자기 규정 → **NOT FOUND**. 다만 제품 목록에 **"Web + app attribution"**, **"ROAS measurement"**, "iOS & SKAN", "Marketing analytics", "Deep linking", "Audience manager", "Fraud protection", "Data export"가 명시됨.
- **API 표면 (10종):** Tracking Link, **Server-to-Server Event**, Actuals Report, Revenue Report, Active Users Report, Retention Report, **Raw Data Export**, **Attribution Result**, Self-Serve Data Upload, **SKAdNetwork Configuration API**
- ⚠️ `developers.airbridge.io` → **301 → `help.airbridge.io`**
- [https://help.airbridge.io/en/references/introduction | 문서 표기 "Last updated April 8, 2026" | 검색 시점 2026-07-25]
- [https://help.airbridge.io/docs | © 2026 표기 | 검색 시점 2026-07-25]

#### Branch — 미조회
- **판정: `확인 불가 (미조회)`**

> **관찰 — API 이름이 카테고리를 드러낸다 (이 리서치의 관찰, 벤더 주장 아님).**
>
> | | CDP/CEP (Insider·Braze·mParticle) | 어트리뷰션 (AppsFlyer·Adjust·Airbridge) |
> |---|---|---|
> | 핵심 API | Upsert User / Track Users / Events API | **Attribution Result**, Tracking Link, SKAdNetwork Config |
> | 리포트 API | 캠페인 분석 | **Actuals / Revenue / Retention / ROAS Report** |
> | 존재 이유 | 프로필을 만들고 메시지를 보낸다 | **어느 광고가 이 설치·전환을 만들었는지 귀속(attribute)한다** |
>
> Airbridge에만 `Attribution Result` API가 있고 Insider에는 없다. Insider에만 `Send Transactional Emails`가 있고 Airbridge에는 없다. **API 카탈로그를 나란히 놓으면 카테고리 경계가 마케팅 문구보다 선명하다.** 이게 개발자 독자에게 카테고리를 설명하는 가장 좋은 방법이다.
>
> ⚠️ 위 표는 이 리서치가 각 벤더 문서에서 확인한 API 이름을 재배열한 것이다. 각 항목의 존재는 사실이지만, "없다"는 진술은 **이 세션에서 조회한 페이지 범위 안에서만** 유효하다.

### B-2-4. 한국 벤더

#### 채널톡 (Channel Talk)
- **개발자 포털:** `developers.channel.io` (영문 문서)
- 자기 설명 (원문 조각): "A Guide to Open API and SDK usages", "Installation guides for SDK on each platform", "References to Open API and SDK."
- **SDK:** JavaScript, iOS, Android, React Native
- **API/웹훅 표면:** Open API, Webhook, Open API for Documents, Snippet, FrontALF, TTS(Text-to-Speech)
- 발행일 → **NOT FOUND**
- [https://developers.channel.io/docs | 발행일 미표기 | 검색 시점 2026-07-25]

**카테고리:** 문서상 자기 규정 **NOT FOUND**. SDK·기능 구성상 상담/인앱 메신저(고객 커뮤니케이션) 계열로 보이며 CDP도 CEP도 아니다. **단 이 판정은 이 리서치의 유추다 — 벤더 자체 규정으로 서술하지 말 것.**

#### 그루비 (Groobee) — 플레이티어(Plateer)
- 자기 규정 (원문): **"비즈니스 성공을 위한 필수 마테크 솔루션"**
- 데이터 수집 (원문): **"사이트에서 발생하는 모든 행동 데이터를 자동으로 수집합니다"**, "이커머스 업계에서 가장 많이 활용하는 고객 행동 데이터"
- 연동 방식 (원문): **"스크립트, SDK만 설치하면"**, "간단한 스크립트 설치만으로 그루비를 시작하실 수 있습니다."
- API (원문): **"그루비 API 하나로 쉽게 연동해 사용하실 수 있습니다"**
- 운영사: 페이지 하단 표기 **"COPYRIGHT 2023 Plateer Inc."**
- [https://groobee.net/tech/data/ | 발행일 미표기 (저작권 표기 2023) | 검색 시점 2026-07-25]

⚠️ 저작권 표기가 2023 — **페이지가 갱신되지 않았을 가능성.** 현재 기능 셋과 다를 수 있다.
⚠️ 상세 개발자 문서(REST API 스펙, 커스텀 데이터 설정)는 **그루비 어드민 로그인 뒤**에 있는 것으로 보인다 → **공개 개발자 문서 확인 불가.** 한국 마테크 벤더에서 흔한 패턴이며, 그 자체가 개발자 독자에게 유의미한 관찰이다.

#### 빅인 (Bigin) — 빅인사이트(biginsight)
- 카테고리 자기 규정("CDP"/"CRM 마케팅") → **NOT FOUND**
- 확인된 가장 가까운 문장 (원문): **"고객들의 데이터를 기반으로 개인화된 CRM 자동화가 필요할 때, Bigin 4.0 하나면 충분합니다."**
- **제품 라인업:** Bigin 4.0 (메인), Bigin Ads — "Bigin Ads와 Bigin을 결합하여 유입~전환까지 풀퍼널 전략 수립"
- 개발자 연동(스크립트/API/SDK) 명시 → **NOT FOUND**. 확인된 유일한 연동 언급: **"카페24 API를 연동하여 데이터를 간편하게 연동할 수 있습니다."**
- 페이지 내 날짜: 2025.12.03 / 2025.10.29 / 2025.09.24 / 2025.07.25, 저작권 "ⓒ 2023 biginsight"
- [https://bigin.io/ | 페이지 내 최신 날짜 2025-12-03 | 검색 시점 2026-07-25]

⚠️ **공개 개발자 문서 확인 불가.** 커머스 플랫폼(카페24) API 연동을 앞세운다는 점이 특징 — 한국 이커머스 생태계에 맞춘 통합 전략.
⚠️ "Bigin CDP"라는 별도 제품이 있다는 서술은 **검색 결과(2차 매체)에만** 있었고 공식 사이트에서 확인하지 못했다. `확인 불가`.

#### 다이티 (Dighty) — NHN DATA
- `https://dighty.com/` → **TLS 인증서 불일치 오류** (인증서 altnames가 `*.api.touchclass.com` / `*.admin.touchclass.com` — 전혀 다른 서비스)
- `https://www.dighty.com/` → **동일 오류**
- `https://blog.dighty.com/` → **HTTP 403 Forbidden**
- **판정: `확인 불가 (2026-07-25 3개 URL 전부 조회 실패)`**
- 검색 결과 페이지 타이틀에 "AI 고객 데이터 통합 플랫폼 | 다이티 Dighty"가 보이나 **원문 미확인**. NHN DATA 운영·2019년 출시·에이스카운터/AI박스/오디언스매니저/캠페인매니저 구성 등은 전부 **2차 매체 요약에만 존재, 미검증**.

⚠️ **인증서 오류는 그 자체로 기록 가치가 있다.** 2026-07-25 기준 `dighty.com`이 정상 서빙되지 않는 것으로 관찰됨. 다만 이것만으로 서비스 종료를 단정할 수는 없다(일시적 인프라 문제 가능).

#### AB180 (Airbridge 운영사)
- Airbridge 제품 정보는 §B-2-3 참조. **AB180 회사 자체 정보는 미조회 → `확인 불가`.**

### B-2-5. 요약표 — 이 세션에서 확인한 벤더 전수

| 벤더 | 문서에서 확인한 자기 규정 | 개발자 표면 (확인된 것) | 공식 문서 URL |
|---|---|---|---|
| Insider One | "Agentic Customer Engagement Platform" / UCD는 "the core Customer Data Platform (CDP)" | ins.js 태그, `InsiderQueue`, Upsert/Get/Export/Delete API, iOS·Android·Flutter SDK | academy.insiderone.com |
| Adobe Real-Time CDP | "bring together known and anonymous data ... in real time" | XDM 스키마, Individual Profile / ExperienceEvent 클래스 | experienceleague.adobe.com |
| Adobe Journey Optimizer | "An enterprise application for creating and delivering connected, contextual, and personalized customer experiences" | AEP 위에 네이티브 | experienceleague.adobe.com |
| mParticle (by Rokt) | "a customer data platform (CDP)" | Events API(HTTP/Node/Python/Ruby), Profile API, Firehose API, IDSync / Android·iOS·Web SDK | docs.mparticle.com |
| Twilio Segment | NOT FOUND | Spec(identify/track/page/screen/group/alias) — §B-3-1 | segment.com/docs (403) |
| Bloomreach Engagement | NOT FOUND | Customers/Events/Catalogs, hard ID·soft ID, REST + Webhook + **Kafka** / JS·iOS·Android·RN·Flutter·MAUI·Xamarin·Python SDK | documentation.bloomreach.com |
| Braze | NOT FOUND | "high-performance REST API", Track users endpoint, User attributes object | braze.com/docs |
| MoEngage | "Engage your users with intelligent, cross-channel experiences" | data ingestion/campaigns/segments/templates/subscriptions 엔드포인트 / iOS·Android·Web·RN·Flutter·Unity SDK | moengage.com/docs |
| CleverTap | **"Customer retention platform"** | Upload Events, Upload User Profiles / SDK 9종(KaiOS·Unreal 포함) | developer.clevertap.com |
| OneSignal | **"omnichannel messaging"** | REST API, Webhooks / Push·Email·SMS&RCS·In-app·Live Activities | documentation.onesignal.com |
| Airship | NOT FOUND ("push, SMS, email, in-app messaging, Scenes") | REST(messaging/audience/event streaming/wallet), Open Channel API / iOS·Android·Web·RN·Flutter | airship.com/docs |
| Klaviyo | NOT FOUND | JSON:API, 날짜 버저닝(v2026-07-15), Profiles/Events/Lists/Segments/Campaigns/Flows, burst+steady 레이트 리밋 | developers.klaviyo.com |
| AppsFlyer | "empowers marketers..." (카테고리 아님) | "attribution out-of-the-box", S2S events API, Click Signing API / Android·iOS + Unity·RN·Flutter | dev.appsflyer.com |
| Adjust | NOT FOUND | Attribution info, ad revenue, subscription, uninstall/reinstall 측정 / SDK 14종 | dev.adjust.com |
| Airbridge (AB180) | NOT FOUND (제품: "Web + app attribution", "ROAS measurement") | Tracking Link, S2S Event, **Attribution Result**, SKAdNetwork Config, Raw Data Export | help.airbridge.io |
| 채널톡 | NOT FOUND | Open API, Webhook, Snippet, TTS / JS·iOS·Android·RN SDK | developers.channel.io |
| 그루비 (Plateer) | **"비즈니스 성공을 위한 필수 마테크 솔루션"** | 스크립트·SDK 설치, "그루비 API" (상세 스펙은 어드민 내부) | groobee.net |
| 빅인 (biginsight) | NOT FOUND ("개인화된 CRM 자동화") | 카페24 API 연동 (공개 개발자 문서 확인 불가) | bigin.io |
| 다이티 (NHN DATA) | **확인 불가 (사이트 조회 실패)** | 확인 불가 | dighty.com (TLS 오류) |
| Salesforce Data Cloud | **확인 불가 (문서 404/렌더 실패)** | 확인 불가 | — |
| Iterable | **확인 불가 (403)** | 확인 불가 | — |

> **이 표에서 바로 읽히는 것 (책에 쓸 만한 관찰):**
> 1. **명시적 카테고리 라벨을 개발자 문서 첫 화면에 쓴 벤더는 소수다.** 확인된 것은 Adobe RTCDP("Real-Time Customer Data Platform"), mParticle("a customer data platform (CDP)"), Insider UCD("the core Customer Data Platform (CDP)"), CleverTap("Customer retention platform"), OneSignal("omnichannel messaging") 정도. 나머지는 NOT FOUND. **카테고리 이름은 개발자 문서가 아니라 세일즈 자료에 산다.**
> 2. **같은 일을 하는데 라벨이 제각각이다** — CDP / Customer Engagement Platform / Customer retention platform / omnichannel messaging / 마테크 솔루션 / CRM 자동화.
> 3. **한국 벤더 3곳(그루비·빅인·다이티) 모두 공개 개발자 문서를 확인하지 못했다.** 글로벌 벤더는 문서를 공개 자산으로 운영하고, 한국 벤더는 계약·어드민 뒤에 둔다. 이 차이가 개발자로 입사할 때 체감하는 첫 번째 문화 차이일 가능성이 높다.

---

## B-3. 개발자 통합 표면의 공통 문법

### B-3-1. Segment Spec — 업계 사실상의 표준 (1차, GitHub 원본 문서)

> ⚠️ **조회 경로 주의:** `segment.com/docs/connections/spec/`는 **403 Forbidden**이었다. 대신 Segment가 공개한 문서 소스 리포지터리 `github.com/segmentio/segment-docs`의 raw 마크다운을 열어 원문을 확인했다. 즉 **1차 소스이되, 렌더된 문서 사이트가 아니라 문서 소스 파일**이다.

#### 6개 API 콜과 각각의 한 줄 정의 (원문)

| 콜 | 원문 정의 |
|---|---|
| **Identify** | "who is the customer?" |
| **Track** | "what are they doing?" |
| **Page** | "what web page are they on?" |
| **Screen** | "what app screen are they on?" |
| **Group** | "what account or organization are they part of?" |
| **Alias** | "what was their past identity?" |

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/index.md | 발행일 미표기 (리포 `develop` 브랜치, 2026-07-25 조회 시점) | 검색 시점 2026-07-25]

**책에 쓸 만한 포인트:** 이 6개 질문 — "누구인가 / 무엇을 하는가 / 어느 페이지인가 / 어느 화면인가 / 어느 조직인가 / 예전 정체는 무엇인가" — 이 마테크 데이터 수집의 전부다. 개발자에게 이보다 짧은 도메인 입문은 없다.

#### identify 콜 (원문)

> "The Segment Identify call lets you tie a user to their actions and record traits about them. It includes a unique User ID and any optional traits you know about the user, like their email and name."

필드: `userId`, `anonymousId`, `traits`, `context`, `type`, `channel`, `integrations`, `messageId`, `receivedAt`, `sentAt`, `timestamp`, `version`

**예약 traits (원문 표):**

| Trait | Type |
|---|---|
| `address` | Object |
| `age` | Number |
| `avatar` | String |
| `birthday` | Date |
| `company` | Object |
| `createdAt` | Date |
| `description` | String |
| `email` | String |
| `firstName` | String |
| `gender` | String |
| `id` | String |
| `lastName` | String |
| `name` | String |
| `phone` | String |
| `title` | String |
| `username` | String |
| `website` | String |

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/identify.md | 발행일 미표기 | 검색 시점 2026-07-25]

#### track 콜 (원문)

> "The Track API call is how you record any actions your users perform, along with any properties that describe the action."

필드: `event`(액션 이름, 예 "User Registered"), `properties`(액션을 설명하는 부가 정보), `userId`, `anonymousId`

**예약 properties (원문):**
| Property | Type | 설명 (원문) |
|---|---|---|
| `revenue` | Number | "Amount of revenue an event resulted in" |
| `currency` | String | "Currency of the revenue an event resulted in" |
| `value` | Number | "An abstract 'value' to associate with an event" |

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/track.md | 발행일 미표기 | 검색 시점 2026-07-25]

#### page 콜 (원문)

> "The Page call lets you record whenever a user sees a page of your website, along with any optional properties about the page."

필드: `type`("page"), `name`(예 "Home"), `category`, `properties`

**예약 properties (원문 표):**
| Property | Type | 용도 |
|---|---|---|
| `path` | String | URL 경로 (기본값 `location.pathname`) |
| `referrer` | String | 이전 페이지의 전체 URL |
| `search` | String | URL의 쿼리스트링 부분 |
| `title` | String | 페이지 타이틀 (`document.title`에서) |
| `url` | String | 전체 페이지 URL |
| `keywords` | Array [String] | SEO용 페이지 콘텐츠 설명 키워드 |

구현 노트 (요지): analytics.js에서는 Page 콜이 기본 스니펫에 **자동 포함**되며, 라이브러리가 `title`·`path`·`url`·`referrer`·`search`를 자동 수집한다.

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/page.md | 발행일 미표기 | 검색 시점 2026-07-25]

#### screen 콜 (원문)

> "The Screen call lets you record whenever a user sees a screen, the mobile equivalent of Page, in your mobile app, along with any properties about the screen."

필드: `name`(String, 예 "Home", "Signup"), `properties`(Object) + 공통 필드(`type`, `anonymousId`, `userId`, `timestamp`, `channel`, `context`, `integrations`, `messageId`)

예약 property: `name` (String) — "Name of the screen. This is reserved for future use."

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/screen.md | 발행일 미표기 | 검색 시점 2026-07-25]

#### group 콜 (원문)

> "The Group API call is how you associate an individual user with a group, such as a company, organization, account, project, or team."

- 사용자는 **여러 그룹에 속할 수 있다.**
- 필드: `groupId`(그룹 고유 식별자), `traits`(그룹 고유 속성 — 예: industry, employees 수), `userId`, `anonymousId`

**예약 group traits (원문 표):** `address`(Object: city/country/postalCode/state/street), `avatar`(String), `createdAt`(Date, ISO-8601 권장), `description`(String), `email`(String), `employees`(String), `id`(String), `industry`(String), `name`(String), `phone`(String), `website`(String), `plan`(String)

주의 (요지): traits는 **대소문자를 구분하지 않으며**, null 값을 넣으면 이전에 설정된 값을 대체한다.

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/group.md | 발행일 미표기 | 검색 시점 2026-07-25]

> **B2B와 B2C의 갈림길이 `group` 콜에 있다.** B2C 마테크에서는 거의 안 쓰이고, B2B SaaS에서는 계정(account) 단위 분석·과금이 여기 걸린다. Adobe가 별도로 "Real-Time CDP **B2B Edition**"을 두는 이유와 같은 문제다.

#### alias 콜 (원문)

> "an advanced method used to merge 2 unassociated user identities, effectively connecting 2 sets of user data in one profile."

| Field | Type | 원문 설명 |
|---|---|---|
| `userId` | String | "The user's new identity, or an existing identity that you wish to merge with the `previousId`" |
| `previousId` | String (optional) | "The existing ID you've referred to the user by" (Anonymous ID이거나 이전에 부여한 User ID) |

사용 시점 (요지): 다운스트림 목적지 호환을 위해 추적 중인 사용자 ID를 **명시적으로 바꿔야 할 때**만. **고급 유스케이스 전용**이며, Segment의 Unify 제품 안에서 프로필을 병합하는 용도로는 쓸 수 없다 — 그건 Identity Resolution이 한다.

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/alias.md | 발행일 미표기 | 검색 시점 2026-07-25]

> **개발자가 가장 자주 틀리는 지점이 여기다.** "익명 사용자가 로그인했다"를 `alias`로 처리하려 들지만, Segment 문서는 그건 Identity Resolution의 일이라고 명시한다. 익명 → 식별 전환은 **모든 CDP에서 가장 어려운 문제**이며, Bloomreach의 hard ID/soft ID, Adobe의 identity graph, Insider의 Update Identifiers API가 전부 같은 문제를 각자 다르게 푼 결과다.

#### E-commerce Spec — 예약 이벤트 이름 전체 (원문)

Segment는 커머스 이벤트 이름을 **표준화해 두었다.** 이 이름들을 그대로 쓰면 다운스트림 도구가 별도 매핑 없이 해석한다. (v2 스펙)

| 그룹 | 예약 이벤트 이름 |
|---|---|
| **Browsing** | `Products Searched`, `Product List Viewed`, `Product List Filtered` |
| **Promotions** | `Promotion Viewed`, `Promotion Clicked` |
| **Core Ordering** | `Product Clicked`, `Product Viewed`, `Product Added`, `Product Removed`, `Cart Viewed`, `Checkout Started`, `Checkout Step Viewed`, `Checkout Step Completed`, `Payment Info Entered`, `Order Completed`, `Order Updated`, `Order Refunded`, `Order Cancelled` |
| **Coupons** | `Coupon Entered`, `Coupon Applied`, `Coupon Denied`, `Coupon Removed` |
| **Wishlisting** | `Product Added to Wishlist`, `Product Removed from Wishlist`, `Wishlist Product Added to Cart` |
| **Sharing** | `Product Shared`, `Cart Shared` |
| **Reviewing** | `Product Reviewed` |

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/ecommerce/v2.md | 발행일 미표기 (v2 스펙 / 2026-07 조회 기준) | 검색 시점 2026-07-25]

> **Insider와 나란히 놓고 보면:**
> Insider는 커머스 이벤트를 **SDK 메서드 타입**으로 못박았다 (`type: 'product'` → `product_detail_page_view`, `type: 'add_to_cart'` → `item_added_to_cart`).
> Segment는 **이벤트 이름 문자열 규약**으로 풀었다 (`track('Product Viewed')`, `track('Product Added')`).
>
> 같은 도메인 지식(커머스 퍼널)을 한쪽은 **타입 시스템**으로, 다른 쪽은 **네이밍 컨벤션**으로 인코딩한 것. 개발자에게 익숙한 트레이드오프다 — 강한 타입 vs 유연한 컨벤션.
> ⚠️ 이 대조는 이 리서치의 관찰이다. 두 벤더 모두 서로를 언급하지 않았다.

#### context 객체 — 모든 콜에 공통으로 붙는 환경 정보 (원문 표)

| Field | Type | Description (원문) |
|-------|------|-------------|
| `active` | Boolean | "Whether a user is active...usually used to flag an Identify call to just update the traits but not 'last seen.'" |
| `app` | Object | "Dictionary of information about the current application, containing `name`, `version`, and `build`." |
| `campaign` | Object | "Dictionary of information about the campaign that resulted in the API call" |
| `device` | Object | "Dictionary of information about the device" |
| `ip` | String | "Current user's IP address." |
| `library` | Object | "Dictionary of information about the library making the requests to the API" |
| `locale` | String | "Locale string for the current user, for example `en-US`." |
| `network` | Object | "Dictionary of information about the current network connection" |
| `os` | Object | "Dictionary of information about the operating system" |
| `page` | Object | "Dictionary of information about the current page in the browser" |
| `referrer` | Object | "Dictionary of information about the way the user was referred" |
| `screen` | Object | "Dictionary of information about the device's screen" |
| `timezone` | String | "Timezones are sent as `tzdata` strings" |
| `groupId` | String | "Group / Account ID" |
| `traits` | Object | "Dictionary of `traits` of the current user" |
| `userAgent` | String | "User agent of the device making the request." |
| `userAgentData` | Object | "The user agent data of the device making the request" |
| `channel` | String | "Where the request originated from: server, browser, or mobile." |

⚠️ `common.md`에는 최상위 공통 필드(messageId/timestamp/userId/anonymousId/integrations/receivedAt/sentAt/originalTimestamp/type/version)가 **Jekyll include 템플릿으로 참조**되어 있어 raw 마크다운에서 각각의 설명 문장을 얻지 못했다. JSON 예시 안에는 전부 등장한다. 각 필드의 정의문은 `확인 불가 (템플릿 미전개)`.

[https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/common.md | 발행일 미표기 | 검색 시점 2026-07-25]

**`channel` 필드가 특히 중요하다:** "server, browser, or mobile" — 즉 **서버사이드 / 클라이언트사이드 구분이 스펙의 일급 필드로 박혀 있다.** 개발자 독자가 "어디서 이벤트를 쏘느냐"를 왜 고민해야 하는지의 근거.

### B-3-2. 벤더 간 공통 문법 대조표 (이 리서치가 연 문서들 기준)

같은 개념이 벤더마다 다른 이름을 갖는다. **아래는 이 세션에서 실제로 문서를 연 3개 벤더만 대조한 것이다.**

| 개념 | Segment Spec | RudderStack | Insider One (UCD) | Adobe (XDM) | Bloomreach | Klaviyo |
|---|---|---|---|---|---|---|
| 사용자 식별 | `identify` + `userId` / `anonymousId` | `Identify` | `identifiers` (`email`/`phone_number`/`uuid`) 또는 `insider_id` | 확인 불가 (identity graph 언급만) | **hard IDs / soft IDs** | `Profiles` |
| 사용자 속성 | `traits` (예약 17종) | (Identify의 traits) | `attributes` + `custom` 객체 | **XDM Individual Profile** (record-based class) | Customers | `Profiles` |
| 행동 이벤트 | `track` + `event` + `properties` | `Track` | `events[]` + `event_name` + `event_params` | **XDM ExperienceEvent** (time-series-based class) | Events | `Events` |
| 화면/페이지 | `page` / `screen` | `Page`(웹) / `Screen` | `type: 'home'/'category'/'product'/'cart'/'purchase'/'other'` | 확인 불가 | 확인 불가 | 확인 불가 |
| 조직/계정 | `group` | `Group` | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 |
| 신원 병합 | `alias` | `Alias` | Update Identifiers API | 확인 불가 | (hard/soft ID 병합) | 확인 불가 |
| 세션 리셋 | (스펙에 없음) | `Reset` | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 |
| 환경 메타 | `context` 객체 (18개 필드) | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 |
| 오디언스 | (Personas — 확인 불가) | 확인 불가 | Segments (Dynamic/Predictive/RFM) | 확인 불가 | 확인 불가 | `Segments`, `Lists` |
| 상품 카탈로그 | 확인 불가 | 확인 불가 | Catalog APIs (레이트 리밋표에서 확인) | 확인 불가 | **Catalogs** | 확인 불가 |

> **가장 중요한 축 — "사용자 속성 vs 행동 이벤트"의 이원 구조가 전 벤더에 공통이다.**
> Adobe가 이걸 가장 명시적으로 표현한다: `XDM Individual Profile`은 "A record-based class", `XDM ExperienceEvent`는 "A time-series-based class". 즉 **레코드 하나 + 시계열 로그 하나**. Segment의 `traits`/`track`, Insider의 `attributes`/`events`, Bloomreach의 Customers/Events가 전부 같은 구조다.
> 개발자에게: **CDP의 핵심 스키마는 사실상 두 테이블이다.** 나머지는 그 위의 뷰·조인·인덱스다.

**관찰 1 — 수렴:** Segment와 RudderStack은 이벤트 타입 이름이 사실상 동일하다(RudderStack에 `Reset` 추가). 후발 주자가 Segment Spec을 사실상 표준으로 채택했다고 볼 수 있다. **단, RudderStack이 "Segment Spec을 따른다"고 명시한 문장은 확인하지 못했다 → 단정 금지, 관찰로만 서술.**

**관찰 2 — 발산:** Insider는 페이지 뷰를 **커머스 도메인에 특화된 고정 타입**(`home`/`category`/`product`/`cart`/`purchase`)으로 못박았다. Segment의 범용 `page` 콜과 대조적. → CEP/CDP 벤더가 어느 산업을 겨냥하느냐가 스키마 설계에 그대로 드러난다.

### B-3-3. 배치 vs 스트리밍, 레이트 리밋 — 확보한 구체 수치

이 축에서 **실제 숫자를 확보한 유일한 벤더는 Insider One**이다(§B-D 레이트 리밋 표). 요약하면:
- **인입(ingest)은 크게 열려 있다:** Upsert 25,000 req/min, 요청당 1,000 users, 5MB
- **추출(export)은 극단적으로 좁다:** Export Raw User Data **1 request per day**
- **채널 발송은 트랜잭셔널이 캠페인보다 훨씬 넓다:** Transactional Email 9,000 req/sec vs Create Email Campaign 1 req/sec

> **개발자 독자용 해석:** 이 비대칭이 마테크 아키텍처의 본질을 드러낸다. 데이터는 들어오기 쉽고 나가기 어렵다(=락인), 그리고 "한 명에게 즉시 보내는 것"과 "모두에게 한 번에 보내는 것"은 완전히 다른 시스템이다.
> ⚠️ 위 해석은 이 리서치의 관찰이지 벤더의 설명이 아니다. 수치만 사실이다(2026-07 문서 기준).

---

## 상충·불확실 항목

1. **Insider 버전 체계 이원화 (재확인 완료 — 상충 아님)**
   - README의 모듈 버전: `InsiderMobile v15.1.1`, `InsiderGeofence v1.2.4`, `InsiderMobileAdvancedNotification v2.4.0`, `InsiderWebView v1.0.0`, `InsiderLiveActivities v1.0.0`
   - **릴리스 페이지 재조회 결과 (`/releases`): 최신 태그 `1.9.1`, 날짜 표기 "07 Jul" (연도 미표기)**
   - → 두 체계가 **공존한다**: 리포지터리 릴리스 태그(SPM 패키지 버전)와 내부 프레임워크 모듈 버전이 별개. 상충이 아니라 이원 체계다.
   - ⚠️ **인용 시 반드시 어느 쪽인지 명시하라.** "Insider iOS SDK 버전"이라고만 쓰면 모호하다. 그리고 `1.9.1`은 **연도가 확인되지 않았다** — "2026년 7월 조회 시점 최신 태그"로만 쓸 것.
   - [https://github.com/useinsider/Insider-iOS-SDK/releases | 태그 1.9.1 / "07 Jul" 표기, 연도 확인 불가 | 검색 시점 2026-07-25]

2. **Insider 브랜드 vs 인프라 도메인 상충(의도된 것으로 보임)**
   - 브랜드/문서: `insiderone.com`, `academy.insiderone.com`
   - 태그·API 호스트: `useinsider.com`, `unification.useinsider.com`
   - GitHub 조직 slug: `useinsider` / 표시명 `InsiderOne`
   - → 상충이라기보다 **리브랜딩 진행 중 상태**. 둘 다 2026-07-25 시점에 유효.

3. **Insider 회사 사실관계 — 1차 vs 2차 불일치 가능성**
   - 1차(insiderone.com/news, 2024-11-01): "28 countries across five continents", "1,500+ customers"
   - 2차(검색 결과 요약): 설립 2012, 이스탄불 본사, 2022 유니콘, 누적 $772M
   - → **1차 소스에서 설립연도·본사·누적투자액을 확인하지 못했다.** 2차 수치는 미검증. `상충 여부 자체를 판정할 수 없음`.

4. **Hightouch 문서 vs 마케팅 페이지 온도 차**
   - 마케팅 페이지: "Hightouch doesn't store your data" (강한 주장)
   - 개발자 문서(concepts): 해당 주장 **NOT FOUND**
   - → 상충은 아니지만, **강한 아키텍처 주장이 마케팅 면에만 있다**는 점은 기록해 둘 가치가 있다.

5. **CDP Institute 조직명**
   - 검색 결과 페이지 타이틀: "CDP Institute / Customer Data Alliance"
   - 현재 공식 명칭이 무엇인지 **원문 확인 불가**(403)

6. **mParticle 합병 발표일**
   - 1차(mparticle.com 뉴스 페이지): 발표일 **NOT FOUND**, 금액 "$300 million merger"
   - 2차(검색 결과 요약): 2025년 1월
   - → **1차에서 날짜 확인 불가.** 금액만 1차 확인됨. 날짜를 쓰려면 재확인 필요.

7. **Census / mParticle의 현재 존속 상태**
   - Census: `getcensus.com` → `fivetran.com`으로 301 (도메인 이관 확인)
   - mParticle: `developer.mparticle.com` DNS 소멸했으나 `docs.mparticle.com`은 살아 있고 2026-07-16 갱신 표기, 문서에서 여전히 "a customer data platform (CDP)"로 자기 규정
   - → **두 인수의 결과가 서로 다르다.** Census는 브랜드가 흡수된 것으로 보이고, mParticle은 브랜드·문서를 유지한다. **단, Census 제품 단종 여부는 `확인 불가`** — 리다이렉트만으로 단정할 수 없다.

8. **다이티(dighty.com) TLS 인증서 불일치**
   - 인증서 altnames가 `*.api.touchclass.com` / `*.admin.touchclass.com`으로, 도메인과 무관
   - → 2026-07-25 시점에 정상 서빙되지 않음. **서비스 종료인지 일시적 인프라 문제인지 판정 불가.**

9. **문서 사이트 타임스탬프의 의미**
   - Insider Academy는 다수 페이지가 Published와 Updated가 **동일 초 단위 타임스탬프**를 갖는다(예: 2026-04-22T09:21:05Z 양쪽). → 빌드/렌더 시각일 가능성이 높다.
   - CleverTap·Bloomreach는 상대 시각("7 months ago", "about 2 months ago")만 노출 → 절대 날짜 **확인 불가**.
   - → **문서 사이트 날짜를 "발행일"로 인용하지 마라.** 이 문서는 전부 `페이지 표기`로만 기록했다.

---

## 확인 불가 목록

### 조회 시도했으나 접근 실패 (HTTP 403 / 404 / DNS)
| URL | 결과 |
|---|---|
| `https://www.cdpinstitute.org/learning-center/what-is-a-cdp/` | 403 |
| `https://www.cdpinstitute.org/cdp-basics/` | 403 |
| `https://www.cdpinstitute.org/about/` | 403 |
| `https://cdpinstitute.org/learning-center/what-is-a-cdp/` | 403 |
| `https://sea.cdpinstitute.org/cdp-basics/` | DNS ENOTFOUND |
| `https://www.gartner.com/en/information-technology/glossary/customer-data-platform-cdp` | 403 |
| `https://segment.com/docs/connections/spec/` | 403 (→ GitHub raw로 우회 성공) |
| `https://academy.insiderone.com/docs/unified-customer-database-overview` | 404 (→ `-ucd` 슬러그로 성공) |
| `https://academy.insiderone.com/docs/architect-overview` | 404 |
| `https://hightouch.com/docs/getting-started/overview` | 404 (→ `/concepts`로 성공) |
| `https://web.archive.org/...` | 도구가 접근 불가 |
| `https://www.getcensus.com/blog/what-is-a-composable-cdp` | 301 → fivetran.com (호스트 변경) |
| `https://developer.mparticle.com/` | **DNS ENOTFOUND** (도메인 소멸) |
| `https://segment.com/docs/` | 403 (→ GitHub raw로 부분 우회) |
| `https://support.iterable.com/hc/en-us/categories/360002357451-API-Docs` | 403 |
| `https://developer.salesforce.com/docs/data/data-cloud-dev/overview` | 404 |
| `https://developer.salesforce.com/docs/data/data-cloud-ref/guide/c360dm-api.html` | 404 |
| `https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-develop.html` | 404 |
| `https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud.htm&type=5` | 열렸으나 JS 렌더 셸만 반환 |
| `https://experienceleague.adobe.com/en/docs/experience-platform/rtcdp/overview` | 404 (→ `/rtcdp/home`으로 성공) |
| `https://developers.klaviyo.com/en/docs/welcome_to_klaviyo_apis` | 404 (→ `/reference/api_overview`로 성공) |
| `https://dighty.com/`, `https://www.dighty.com/` | **TLS 인증서 altnames 불일치** |
| `https://blog.dighty.com/` | 403 |
| `https://developers.airbridge.io/docs` | 301 → help.airbridge.io |
| `https://developers.moengage.com/hc/en-us` | 301 → moengage.com/docs |
| `https://docs.airship.com/` | 301 → www.airship.com/docs |

### 열었으나 원하는 내용이 없었음 (NOT FOUND)
- Braze의 명시적 카테고리 자기 규정 문장, SDK 플랫폼 목록, Canvas 설명 (`braze.com/docs`)
- RudderStack의 자기 정의·warehouse-native 표방 문장 (`rudderstack.com/docs`)
- Hightouch 문서의 "데이터를 복사하지 않는다" 주장 (`/docs/getting-started/concepts` — 마케팅 페이지에만 있음)
- Insider 설립연도·본사·누적투자액·기업가치 (`insiderone.com/about/`, `insiderone.com/news/...`)
- Insider iOS SDK의 API 메서드명 (GitHub README, `ios-basic-sdk-setup`)
- Insider Predictive Segments의 ML 모델 설명
- Segment `common.md`의 최상위 공통 필드 개별 설명문 (Jekyll include 미전개)
- Segment의 "CDP" 자기 규정, Connections/Protocols/Unify/Engage 제품 구분
- Adobe의 identity graph / identity namespace 정의문
- mParticle의 `MPID`, "Identity API" 명칭, 합병 발표일
- Bloomreach·Klaviyo·Airship·Adjust·Airbridge의 카테고리 자기 규정 문장
- Klaviyo SDK 구체 목록
- OneSignal SDK 플랫폼 목록
- 빅인(Bigin)의 개발자 연동 방식(스크립트/API/SDK), "Bigin CDP" 제품 존재 여부
- 그루비 REST API 상세 스펙 (어드민 로그인 뒤로 추정)

### 아예 조회하지 못함 (미조회)
- **카테고리 1차 정의:** DMP / CRM / MA(마케팅 자동화) / CEM, CDP 유형 4분류(Data/Analytics/Campaign/Delivery), Forrester 공개 정의
- **벤더:** Salesforce Marketing Cloud, Branch, AB180 회사 정보, Insider·Braze 등의 한국 법인/오피스
- **Insider 세부:** Architect(저니 오케스트레이션) 상세, Eureka(제품 정체), RFM Segments, Dynamic Segments, 채널별 문서, iOS `/docs/ios-initialize-sdk`, Android/Flutter SDK 상세, Recommendation API 상세
- **B-3 미확보 축:** 서버사이드 vs 클라이언트사이드 SDK 선택 기준의 벤더 공식 서술, 웹훅 스펙 상세, 배치 vs 스트리밍 인입의 벤더 공식 비교, **Identity Resolution 상세 문서**(Segment Unify / Adobe Identity Service / Bloomreach hard·soft ID 병합 규칙)
- Insider 내부 아키텍처 → **공개 자료 없음** (추정 금지)

---

## 신선도 원장

| 소스 | URL | 발행일 / "{버전}/{연도} 기준" | 검색 시점 | 관련 축 | 신뢰성 |
|---|---|---|---|---|---|
| Insider One 홈 | https://insiderone.com/ | 발행일 미표기 (© 2026 표기) | 2026-07-25 | B | 최상(1차) |
| Insider Web SDK 가이드 | https://academy.insiderone.com/docs/insider-web-sdk-integration-guide | 페이지 표기 2026-07-23 (문서 사이트 표기) | 2026-07-25 | B, B-3 | 최상(1차) |
| Insider UCD | https://academy.insiderone.com/docs/unified-customer-database-ucd | 페이지 표기 2026-04-22 | 2026-07-25 | A, B | 최상(1차) |
| Insider API 인증 | https://academy.insiderone.com/docs/api-authentication-tokens | 페이지 표기 2026-07-23 | 2026-07-25 | B | 최상(1차) |
| Insider Upsert API | https://academy.insiderone.com/docs/upsert-user-data-api | 페이지 참조일 2026-07-24 | 2026-07-25 | B, B-3 | 최상(1차) |
| Insider Rate Limits | https://academy.insiderone.com/docs/api-rate-limits | 페이지 표기 2026-07-12 | 2026-07-25 | B, B-3 | 최상(1차) |
| Insider User Data APIs | https://academy.insiderone.com/docs/ucd-user-data-apis-overview | 페이지 표기 2026-07-14 | 2026-07-25 | B | 최상(1차) |
| Insider Segments 개요 | https://academy.insiderone.com/docs/audience-segments-overview | 페이지 표기 2026-04-17 | 2026-07-25 | B | 최상(1차) |
| Insider Predictive Segments | https://academy.insiderone.com/docs/audience-predictive-segments | 페이지 표기 2026-04-12 | 2026-07-25 | B | 최상(1차) |
| Insider iOS SDK 설정 | https://academy.insiderone.com/docs/ios-basic-sdk-setup | 페이지 표기 2026-01-04 | 2026-07-25 | B | 최상(1차) |
| Insider 문서 인덱스 | https://academy.insiderone.com/llms.txt | 발행일 미표기 | 2026-07-25 | B | 최상(1차) |
| Insider iOS SDK (GitHub) | https://github.com/useinsider/Insider-iOS-SDK | InsiderMobile v15.1.1 / 2026년 7월 조회 기준 | 2026-07-25 | B | 최상(1차) |
| Insider Series E 보도자료 | https://insiderone.com/news/insider-announces-500m-series-e-led-by-general-atlantic/ | 2024-11-01 | 2026-07-25 | B | 최상(1차) |
| Segment Spec index | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/index.md | 발행일 미표기 (develop 브랜치 / 2026-07 조회 기준) | 2026-07-25 | B-3 | 최상(1차 문서 소스) |
| Segment Spec identify | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/identify.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment Spec track | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/track.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment Spec common | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/common.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment Spec page | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/page.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment Spec screen | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/screen.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment Spec group | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/group.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment Spec alias | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/alias.md | 발행일 미표기 | 2026-07-25 | B-3 | 최상(1차) |
| Segment E-commerce Spec v2 | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/ecommerce/v2.md | v2 스펙 / 2026-07 조회 기준 | 2026-07-25 | B-3 | 최상(1차) |
| Hightouch composable CDP 블로그 | https://hightouch.com/blog/composable-cdp | 2023-06-20 (Luke Kline) ⚠️ 3년 경과 | 2026-07-25 | A | 최상(1차, 단 구버전 가능) |
| Hightouch 제품 페이지 | https://hightouch.com/platform/composable-cdp | 발행일 미표기 | 2026-07-25 | A | 최상(1차, 마케팅) |
| Hightouch 개발자 문서 | https://hightouch.com/docs/getting-started/concepts | "Last updated Jul 17, 2026" | 2026-07-25 | A | 최상(1차) |
| Google Cloud 엔지니어링 블로그 | https://cloud.google.com/blog/products/data-analytics/hightouch-composable-cdp-built-on-bigquery | 2023-09-02 ⚠️ 구버전 가능 | 2026-07-25 | A | 최상(회사 엔지니어링 블로그) |
| RudderStack 문서 | https://www.rudderstack.com/docs/ | 발행일 미표기 | 2026-07-25 | A, B-3 | 최상(1차) |
| Fivetran → Census 인수 보도자료 | https://www.fivetran.com/press/fivetran-signs-agreement-to-acquire-census-... | 2025-05-01 | 2026-07-25 | A | 최상(1차) |
| Braze 문서 홈 | https://www.braze.com/docs/ | 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차) |
| 채널톡 개발자 문서 | https://developers.channel.io/docs | 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차) |
| Adobe Real-Time CDP 홈 | https://experienceleague.adobe.com/en/docs/experience-platform/rtcdp/home | 문서 표기 2026-06-18 | 2026-07-25 | A, B-2 | 최상(1차) |
| Adobe XDM 시스템 개요 | https://experienceleague.adobe.com/en/docs/experience-platform/xdm/home | 문서 표기 "Last update May 23, 2026" | 2026-07-25 | A, B-2, B-3 | 최상(1차) |
| Adobe Real-Time Customer Profile | https://experienceleague.adobe.com/en/docs/experience-platform/profile/home | 문서 표기 2026-07-03 | 2026-07-25 | A, B-2 | 최상(1차) |
| Adobe Journey Optimizer | https://experienceleague.adobe.com/en/docs/journey-optimizer/using/get-started/get-started | 문서 표기 "Last updated July 1, 2026" | 2026-07-25 | A, B-2 | 최상(1차) |
| mParticle 문서 | https://docs.mparticle.com/ | 문서 표기 "Last Updated: 7/16/2026" | 2026-07-25 | B-2 | 최상(1차) |
| mParticle × Rokt 합병 발표 | https://www.mparticle.com/news/rokt-and-mparticle-merge/ | 발행일 미표기 (금액 $300M만 확인) | 2026-07-25 | A, B-2 | 최상(1차) |
| Segment docs 소스 index | https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/index.md | 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차 문서 소스) |
| Bloomreach Engagement 문서 | https://documentation.bloomreach.com/engagement/docs | 상대 시각만("about 2 months ago"), 절대 날짜 미확인 | 2026-07-25 | B-2, B-3 | 최상(1차) |
| MoEngage 문서 | https://moengage.com/docs/ | 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차) |
| CleverTap 개발자 문서 | https://developer.clevertap.com/docs/ | 상대 시각만("7 months ago") | 2026-07-25 | B-2 | 최상(1차) |
| OneSignal 문서 | https://documentation.onesignal.com/docs | 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차) |
| Airship 문서 | https://www.airship.com/docs/ | 문서 내 최신 항목 2026-07-23 | 2026-07-25 | B-2 | 최상(1차) |
| Klaviyo API 개요 | https://developers.klaviyo.com/en/reference/api_overview | **API 버전 v2026-07-15 기준** | 2026-07-25 | B-2, B-3 | 최상(1차) |
| AppsFlyer 개발자 문서 | https://dev.appsflyer.com/hc/docs | 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차) |
| Adjust SDK 문서 | https://dev.adjust.com/en/sdk | © 2026 표기, 발행일 미표기 | 2026-07-25 | B-2 | 최상(1차) |
| Airbridge API 레퍼런스 | https://help.airbridge.io/en/references/introduction | 문서 표기 "Last updated April 8, 2026" | 2026-07-25 | B-2 | 최상(1차) |
| Airbridge 도움말 홈 | https://help.airbridge.io/docs | © 2026 표기 | 2026-07-25 | B-2 | 최상(1차) |
| 그루비 데이터 수집 연동 | https://groobee.net/tech/data/ | 저작권 표기 2023 ⚠️ 갱신 안 된 가능성 | 2026-07-25 | B-2 | 최상(1차, 단 구버전 가능) |
| 빅인 공식 사이트 | https://bigin.io/ | 페이지 내 최신 날짜 2025-12-03, 저작권 2023 | 2026-07-25 | B-2 | 최상(1차) |
| **David Raab — CDP 최초 명명** | http://customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html | **2013-04-25** ⚠️ 13년 경과 — 기원 서술 전용 | 2026-07-25 | A | 최상(저자 확인 1차) |
| **David Raab — CDP 정의 개정** | http://customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html | **2015-01-18** ⚠️ 11년 경과 | 2026-07-25 | A | 최상(저자 확인 1차) |
| **David Raab — CDP 유형 분류** | http://customerexperiencematrix.blogspot.com/2018/11/why-are-there-so-many-types-of-customer.html | **2018-11-03** ⚠️ 8년 경과 — "2018년 Raab 기준" 병기 필수 | 2026-07-25 | A | 최상(저자 확인 1차) |
| Adobe Audience Manager (DMP) | https://experienceleague.adobe.com/en/docs/audience-manager/user-guide/aam-home | 문서 표기 "last update May 21, 2026" | 2026-07-25 | A | 최상(1차) |
| Adobe Marketo Engage (MA) | https://experienceleague.adobe.com/en/docs/marketo/using/home | 문서 표기 "last update June 16, 2026" | 2026-07-25 | A | 최상(1차) |
| Insider iOS SDK 릴리스 | https://github.com/useinsider/Insider-iOS-SDK/releases | 태그 1.9.1, "07 Jul" (연도 미표기) | 2026-07-25 | B | 최상(1차) |

---

## 참고문헌 (이 세션에서 실제로 연 URL 전체)

**성공적으로 fetch한 URL:**
1. https://insiderone.com/
2. https://academy.insiderone.com/docs/insider-web-sdk-integration-guide
3. https://academy.insiderone.com/docs/unified-customer-database-ucd
4. https://academy.insiderone.com/docs/ucd-user-data-apis-overview
5. https://academy.insiderone.com/docs/api-authentication-tokens
6. https://academy.insiderone.com/docs/upsert-user-data-api
7. https://academy.insiderone.com/docs/api-rate-limits
8. https://academy.insiderone.com/docs/audience-segments-overview
9. https://academy.insiderone.com/docs/audience-predictive-segments
10. https://academy.insiderone.com/docs/ios-basic-sdk-setup
11. https://academy.insiderone.com/llms.txt
12. https://github.com/useinsider/Insider-iOS-SDK
13. https://insiderone.com/news/insider-announces-500m-series-e-led-by-general-atlantic/
14. https://insiderone.com/about/ (열렸으나 채용 페이지 — 회사 정보 없음)
15. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/index.md
16. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/identify.md
17. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/track.md
18. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/common.md
19. https://hightouch.com/blog/composable-cdp
20. https://hightouch.com/platform/composable-cdp
21. https://hightouch.com/docs/getting-started/concepts
22. https://cloud.google.com/blog/products/data-analytics/hightouch-composable-cdp-built-on-bigquery
23. https://www.rudderstack.com/docs/
24. https://www.fivetran.com/press/fivetran-signs-agreement-to-acquire-census-delivering-the-first-end-to-end-data-movement-platform-for-the-ai-era
25. https://www.braze.com/docs/
26. https://developers.channel.io/docs
27. https://experienceleague.adobe.com/en/docs/experience-platform/rtcdp/home
28. https://experienceleague.adobe.com/en/docs/experience-platform/xdm/home
29. https://experienceleague.adobe.com/en/docs/experience-platform/profile/home
30. https://experienceleague.adobe.com/en/docs/journey-optimizer/using/get-started/get-started
31. https://docs.mparticle.com/
32. https://www.mparticle.com/news/rokt-and-mparticle-merge/
33. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/index.md
34. https://documentation.bloomreach.com/engagement/docs
35. https://moengage.com/docs/
36. https://developer.clevertap.com/docs/
37. https://documentation.onesignal.com/docs
38. https://www.airship.com/docs/
39. https://developers.klaviyo.com/en/reference/api_overview
40. https://dev.appsflyer.com/hc/docs
41. https://dev.adjust.com/en/sdk
42. https://help.airbridge.io/docs
43. https://help.airbridge.io/en/references/introduction
44. https://groobee.net/tech/data/
45. https://bigin.io/
46. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/page.md
47. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/screen.md
48. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/group.md
49. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/alias.md
50. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/ecommerce/v2.md
51. http://customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html
52. http://customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html
53. http://customerexperiencematrix.blogspot.com/2018/11/why-are-there-so-many-types-of-customer.html
54. https://customerexperiencematrix.blogspot.com/2013/04/ (월별 아카이브)
55. https://experienceleague.adobe.com/en/docs/audience-manager/user-guide/aam-home
56. https://experienceleague.adobe.com/en/docs/marketo/using/home
57. https://github.com/useinsider/Insider-iOS-SDK/releases

**접근 실패한 URL:** 위 `## 확인 불가 목록` 표 참조.

---

## 후속 리서치 권고 (research-lead에게)

이 리서치가 **task 커버 축 중 채우지 못한 것**을 우선순위로 정리한다.

### P0 — 책의 뼈대가 걸려 있어서 반드시 필요
1. ~~CDP Institute 공식 정의 원문~~ → **부분 해결.** **작명자 David Raab의 원문 3건(2013 명명 / 2015 정의 개정 / 2018 유형 분류)을 확보**했다(§A-0, §A-2). 남은 것은 **CDP Institute라는 기관의 공식 정의문**뿐이며, 이는 여전히 403. `blogspot.com`은 열리므로 Raab의 다른 글로 더 파고들 여지가 있다.
2. ~~CDP 유형 4분류~~ → **해결 + 정정.** Raab 2018 원문은 **Data / Analytics / Personalization** 3분류다. **"Campaign CDP"·"Delivery CDP"는 그 글에 없다** — task가 준 목록이 틀렸거나 다른 출처의 용어다. §A-2 참조. **책에 4분류로 쓰지 마라.**
3. **DMP / CRM / MA / CEM의 1차 정의와 역사** — **여전히 최대 결손.** 이번에 Adobe Audience Manager(DMP 제품)·Marketo Engage(MA 제품) 문서를 열었으나 **카테고리 자체의 정의문은 둘 다 NOT FOUND.**
   - **교훈: 벤더 제품 문서는 카테고리를 정의하지 않는다.** 다음 라운드는 소스 유형을 바꿔라 — Raab 블로그(blogspot은 열림), 위키피디아, 애널리스트 공개 글, 마테크 전문 매체(martech.org 등).
   - 특히 **"DMP는 서드파티 쿠키, CDP는 퍼스트파티"**라는 통설은 **어떤 1차 소스로도 확인 못 했다.** 검증 없이 쓰지 마라.

### P1 — 개발자 독자에게 실질적으로 중요
4. ~~Segment E-commerce Spec 예약 이벤트 목록~~ → **✅ 확보 완료** (§B-3-1)
5. ~~Segment `page`/`screen`/`group`/`alias` 개별 스펙~~ → **✅ 확보 완료** (§B-3-1)
6. **Salesforce Data Cloud** — 이번에 URL 4개 전부 실패. Trailhead 또는 다른 문서 트리 필요.
7. **서버사이드 vs 클라이언트사이드 SDK 선택 기준** — 벤더 공식 서술을 한 건도 못 찾았다. Segment의 "Which SDK should I use" 계열 문서 권장.
8. **Identity Resolution 상세** — 이 리서치가 "가장 어려운 문제"로 지목했으나(§B-3-1 alias 항목) 어느 벤더의 상세 문서도 열지 못했다. Segment Unify Identity Resolution, Adobe Identity Service, Bloomreach hard/soft ID 병합 규칙 중 최소 하나는 필요.

### P2 — 있으면 좋음
8. Insider Architect(저니 오케스트레이션) 상세, Eureka 제품 정체
9. Iterable(403), Branch, Salesforce Marketing Cloud
10. 다이티(Dighty) — 사이트 자체가 조회 불가 상태. 재확인 필요
11. 각 벤더의 한국 법인/오피스 유무 (대상 독자가 한국 개발자이므로 실용적 가치 있음)

### 이 리서치가 특히 강한 지점 (다른 리서처와 중복 피하기용)
- **CDP 카테고리의 기원** — 작명자 David Raab의 2013/2015/2018 원문 3건. "CDP라는 말이 언제 왜 생겼는가"를 1차 소스로 답할 수 있다.
- **Insider One 개발자 표면 전부** — 태그·큐 객체·사용자 속성 표·페이지 타입·이벤트 메서드·Upsert API 스키마·전 API 레이트 리밋표. 1차 원문 기준.
- **Segment Spec 코어 4문서** (index/identify/track/common) — GitHub raw 원문.
- **20개 벤더 자기 규정·개발자 표면 대조표** (§B-2-5).
- **CDP·CEP·어트리뷰션 3개 카테고리의 API 카탈로그 대조** (§B-2-3 말미) — 마케팅 문구 없이 카테고리를 가르는 방법.
- **2025~2026 시장 통합 사실 2건** (Fivetran→Census 2025-05-01, Rokt→mParticle $300M) — 1차 소스 확인.

<!-- ===== web_stack.md ===== -->

<!-- 검색 시점: 2026-07-25 기준 -->
<!-- 담당: web-researcher #2 / 축: 대규모 고객 데이터 수집·분석 오픈소스 기술 스택 -->
<!-- slug: martech-for-developers / genre: tech-book -->

# 고객 데이터 수집·분석 오픈소스 스택 리서치 (web #2)

검색 수행일: **2026-07-25**

## 이 문서를 읽는 규칙 (fact-checker 대조 기준)

이 문서는 Phase 4 fact-checker의 1차 대조 근거다. 다음 규율을 지켜서 작성했다.

1. **버전 번호·발행일·수치·인용문은 이 세션에서 실제로 fetch한 페이지에서만 가져왔다.** fetch하지 않은 항목은 `확인 불가 (미조회)`로 표기했다.
2. **Tier 2 항목은 의도적으로 조회하지 않았다.** 예산을 Tier 1 깊이에 집중하기 위한 결정이며, 따라서 Tier 2의 모든 버전은 `버전 확인 불가 (미조회)`다. **Tier 2 단락의 서술은 개념적 포지셔닝이며, 챕터에 수치·버전으로 옮기면 안 된다.**
3. **GitHub Releases의 연도 표기는 신뢰할 수 없다 — 이 문서가 실증했다.** GitHub 릴리스 목록·태그 페이지는 날짜를 `20 May 08:47` 형태로만 반환했고, 개별 태그 페이지를 다시 열어도 **`YEAR NOT ON PAGE`**였다(Iceberg 1.11.0, Pinot 1.5.1, Druid 37.0.0에서 각각 확인). 더 결정적으로, **Snowplow의 최상단 항목 `22.01 Western Ghats – 31 Jan`은 CalVer상 2022년 1월인데도 연도 없이 렌더링됐다** — 즉 "연도가 없으면 당해 연도"라는 추론은 **반례가 존재한다.**
   → 따라서 **연도가 필요한 항목은 Apache 배포 아카이브(`archive.apache.org/dist/...`, 전체 타임스탬프 출력)로 재확인**했다. 재확인한 것은 `페이지 표기·확정`, 릴리스 주기로만 추정한 것은 `연도 추정 — 확정 아님`으로 원장에 구분해 적었다. **`연도 추정` 항목을 챕터에 연도까지 박아 쓰면 안 된다.**
4. **벤치마크 수치는 운영 주체를 병기했다.** 벤더 자체 벤치마크·프로젝트 자체 문서의 성능 주장은 그렇게 표시했다.
5. 이 리서치의 담당 축은 **기술 스택**이다. 프라이버시 규제·벤더 제품 비교·커뮤니티 여론은 다른 에이전트 담당이므로 여기서는 기술적 함의 수준에서만 스친다.

---

## 0. 스택 전체 지도 (수집 → 처리 → 저장 → 활성화)

개발자 독자에게 가장 먼저 심어줘야 하는 그림. Martech의 데이터 스택은 결국 **다섯 개 층**이고, 층마다 "왜 이 도구인가"의 답이 다르다.

```
[1] 수집(Collection)          웹/앱/서버 이벤트를 스키마 검증해서 받아낸다
     Snowplow, RudderStack, Jitsu, OpenTelemetry(제품 텔레메트리)
                 │
                 ▼
[2] 전송·버퍼(Transport)      순서·내구성·재처리 가능성을 보장하는 로그
     Apache Kafka, Redpanda, Apache Pulsar
                 │
        ┌────────┴────────┐
        ▼                 ▼
[3a] 스트림 처리        [3b] 배치 처리·변환
  Flink, Kafka Streams,   dbt, Spark, Airflow/Dagster
  Spark Structured
  Streaming, Materialize
        │                 │
        ▼                 ▼
[4] 저장(Storage)
   - 이벤트 분석 OLAP:      ClickHouse, Druid, Pinot, StarRocks
   - 레이크하우스:          Iceberg / Delta Lake / Hudi (on Parquet)
   - 웨어하우스:            Snowflake, BigQuery, Redshift
   - 질의 엔진:             Trino, DuckDB
   - 실시간 프로필 KV:      Redis, Aerospike, Cassandra/ScyllaDB
   - 피처:                  Feast
                 │
                 ▼
[5] 활성화(Activation)        세그먼트를 실제 채널·광고 플랫폼으로 내보낸다
     Reverse ETL (RudderStack 등), 저니 엔진, 캠페인 트리거
```

**개발자가 잡아야 할 축 세 개:**

- **지연(latency) 축** — 이 이벤트가 세그먼트에 반영되기까지 몇 초/몇 시간이 허용되나? 이 질문 하나가 Flink냐 dbt냐를 가른다.
- **기수(cardinality) 축** — 사용자 수준 유니크 카운트를 정확히 세야 하나, 근사해도 되나? 이 질문이 `uniqExact` vs HyperLogLog를 가른다.
- **조회 패턴 축** — 집계 스캔(OLAP)인가, 단건 프로필 조회(KV)인가? 같은 고객 데이터인데 저장소가 두 벌인 이유가 여기 있다.

이 세 축을 챕터 초반에 세워두면, 이후 모든 도구 선택이 "이 축의 어디에 있느냐"로 설명된다.

---

## 1. Tier 1 상세

---

### 1-1. Apache Kafka

**[버전: 4.3.1 / 2026 기준]** — 최신 아카이브 디렉터리 `4.3.1` 타임스탬프 `2026-06-23 22:22`, 직전 `4.3.0`은 `2026-05-20 16:04`.
`[https://archive.apache.org/dist/kafka/ | 디렉터리 타임스탬프 2026-06-23 | 검색 시점 2026-07-25]`

> **조회 실패 기록:** `https://kafka.apache.org/downloads`, `https://kafka.apache.org/documentation/#design`, `https://kafka.apache.org/43/documentation.html#design`는 모두 내비게이션 셸만 반환했다(Kafka 공식 문서는 단일 거대 HTML + 앵커 구조라 추출이 실패). `https://github.com/apache/kafka/releases`는 "There aren't any releases here" — Apache Kafka는 GitHub Releases를 쓰지 않는다. 따라서 **버전은 Apache 아카이브**, **개념은 Confluent 공식 문서와 KIP 위키**로 대체 조회했다.

#### 이게 뭔가

분산 커밋 로그. "메시지 큐"라고 부르면 절반만 맞다. 큐는 읽으면 사라지지만 Kafka는 **읽어도 남는다.** 이 한 가지 차이가 Martech에서 결정적이다 — 같은 클릭스트림을 실시간 세그먼트 엔진도 읽고, 웨어하우스 적재기도 읽고, 6개월 뒤 새 모델 학습용 백필도 읽는다.

#### 어떻게 동작하나

**파티션과 순서 보장.** 토픽은 파티션으로 쪼개지고, 순서는 **파티션 안에서만** 보장된다.

> "messages in each partition log are then read sequentially"
> `[https://docs.confluent.io/kafka/design/consumer-design.html | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

Confluent 문서는 컨슈머 관점에서 이를 못박는다:

> "Each partition is consumed by exactly one consumer within each consumer group at any given time."

**Martech에서의 함의가 여기서 나온다.** 사용자 이벤트를 `user_id`로 파티셔닝하면 한 사용자의 이벤트는 반드시 한 파티션에 들어가고, 따라서 "장바구니 담기 → 결제 → 환불" 순서가 뒤집히지 않는다. 반대로 `event_type`으로 파티셔닝하면 한 사용자의 이벤트가 흩어지고, 저니(journey) 상태 머신이 "결제를 먼저 보고 장바구니를 나중에 보는" 사고가 난다. **파티션 키 선택은 Martech에서 데이터 모델링 결정이지 성능 튜닝이 아니다.**

**컨슈머 그룹과 오프셋.**

> "In Kafka, a consumer group is a set of consumers from the same application that work together to consume and process messages from one or more topics."

> "A consumer offset is used to track the progress of a consumer group. An offset is a unique identifier, an integer, which marks the next record that should be read by the consumer in a partition."

오프셋은 `__consumer_offsets` 내부 토픽에 저장된다. 파티션 할당 프로토콜은 두 가지 — 전통적 리더 기반 모델과, **4.0에서 도입된 브로커 측 분산 방식**(같은 문서 기준).

**Exactly-once.** 여기가 개발자가 가장 많이 오해하는 지점이고, 면접 단골이다. KIP-98 원문:

> "Every new producer will be assigned a unique PID during initialization."

> "For a given PID, sequence numbers will start from zero and be monotonically increasing"

> "Messages with a lower sequence number result in a duplicate error, which can be ignored by the producer. Messages with a higher number result in an out-of-sequence error, which indicates that some messages have been lost, and is fatal."

> "Every message write will be persisted exactly once, without duplicates and without data loss"

`[https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

**그런데 KIP-98은 보장하지 않는 것도 명시한다:**

> "We cannot guarantee that all the messages of a committed transaction will be consumed all together"

이유로 네 가지를 든다 — 컴팩션된 토픽이 트랜잭션 메시지를 덮어쓸 수 있고, 로그 세그먼트를 넘나드는 트랜잭션은 세그먼트 삭제 시 일부를 잃고, 컨슈머가 임의 지점으로 seek하면 앞부분을 놓치고, 컨슈머가 트랜잭션에 참여한 모든 파티션을 읽지 않을 수 있다.

#### Martech에서 어디에 쓰이나

1. **이벤트 수집의 척추.** 수집기(Snowplow Collector, RudderStack)가 Kafka로 밀어넣고, 그 뒤 모든 소비자가 각자 속도로 읽는다.
2. **저니 트리거의 입력.** Flink/Kafka Streams가 컨슈머로 붙어 "장바구니 담고 30분간 결제 없음" 같은 조건을 감지한다.
3. **재처리(replay).** 세그먼트 로직 버그를 고쳤을 때, 오프셋을 되감아 지난 30일 이벤트를 다시 흘리면 세그먼트가 복구된다. **이 능력이 Martech에서 Kafka를 대체 불가로 만든다** — 일반 메시지 큐로는 못 한다.
4. **Transactional Outbox.** 주문 DB 트랜잭션과 이벤트 발행의 정합성을 맞추는 패턴 (§3-6 우아한형제들 사례 참조).

#### 트레이드오프·운영 함정 (개발자가 알아야 할 것)

- **파티션 수는 되돌리기 어렵다.** 늘릴 수는 있지만, 늘리는 순간 `hash(key) % partition_count`가 바뀌어 **기존 키의 파티션 배치가 깨진다.** 사용자별 순서 보장이 그 시점에 한 번 무너진다. Martech에서는 이게 "저니가 한 번 꼬였다"로 나타난다.
- **핫 파티션.** `user_id` 해시가 균등하다는 보장은 봇·크롤러·내부 테스트 계정 앞에서 깨진다. 특정 사용자가 초당 수천 이벤트를 쏘면 그 파티션만 밀린다.
- **컨슈머 랙(lag)이 Martech의 진짜 SLA다.** "실시간 세그먼트"라고 광고했는데 컨슈머 랙이 20분이면 실시간이 아니다. 랙 모니터링은 마케팅 팀에게 약속한 지연 시간의 유일한 증거다.
- **exactly-once는 공짜가 아니다.** 트랜잭션 코디네이터·컨트롤 메시지·`read_committed` 격리 수준이 붙으면서 처리량과 지연이 나빠진다. 대부분의 Martech 이벤트 파이프라인은 **at-least-once + 다운스트림 멱등 처리**(이벤트 ID 기준 중복 제거)가 더 현실적이다.
- **리밸런싱 스톰.** 컨슈머가 죽었다 살아나면 파티션 재할당이 일어나고, 그 사이 처리가 멈춘다. 저니 엔진처럼 상태를 들고 있는 컨슈머에게는 치명적이다.

---

### 1-2. ClickHouse

**[버전: v26.7.1.1315-stable / 2026 기준, LTS 라인은 v26.3.17.56-lts 및 v25.8.28.1-lts]**
GitHub Releases 목록에서 `v26.7.1.1315-stable — 22 Jul 21:14`, `v26.3.17.56-lts — 20 Jul 06:56`, `v25.8.28.1-lts — 05 Jul 12:16` 확인.
`[https://github.com/ClickHouse/ClickHouse/releases | 릴리스 목록 표기 (연도 미표기 — 2026 추정) | 검색 시점 2026-07-25]`

> **주의:** ClickHouse는 릴리스 빈도가 매우 높다(위 목록에서 6월 말~7월 사이에만 10개 이상). 책에 특정 패치 버전을 박지 말고 **"26.x 계열 / 2026 기준"** 수준으로 쓰는 편이 안전하다. 안정 라인(stable)과 LTS 라인이 병행 릴리스되는 구조도 함께 설명할 것.

#### 이게 뭔가

컬럼 지향 OLAP 데이터베이스. Martech 문맥에서는 "수십억 건의 이벤트 테이블에서 퍼널·리텐션·코호트를 초 단위로 뽑는 엔진".

#### 어떻게 동작하나

**MergeTree — 희소 인덱스가 핵심.** 공식 문서:

> "The primary key also does not reference individual rows but blocks of 8192 rows called granules."
> `[https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

이게 B-tree 인덱스와의 결정적 차이다. B-tree는 행 하나하나를 가리키니 인덱스가 데이터만큼 커진다. MergeTree는 **8192행짜리 그래뉼 단위**로만 가리키니 인덱스가 RAM에 통째로 들어간다. 대신 "이 사용자 한 명의 행"을 찍어서 가져오는 건 못한다 — 8192행을 읽고 걸러야 한다. **OLAP에 강하고 OLTP에 약한 이유가 전부 이 한 줄에 있다.**

> "Insert operations create table parts which are merged by a background process with other table parts."

> "Partition pruning ensures partitions are omitted from reading when the query allows it."

> "designed for high data ingest rates and huge data volumes"

**정렬 키가 곧 성능이다.** MergeTree의 primary key는 파트 내 정렬 순서를 결정한다. 이벤트 테이블에서 `ORDER BY (user_id, event_time)`으로 두면 사용자별 시퀀스 스캔이 빨라지고, `ORDER BY (event_time, event_name)`으로 두면 시간 범위 집계가 빨라진다. Martech에서는 **퍼널·리텐션이 사용자별 시퀀스를 요구**하므로 보통 `user_id`가 앞에 온다.

#### 고유 사용자 수: uniqExact vs uniqCombined (HyperLogLog)

이 대목은 개발자 독자에게 가장 인상적으로 전달할 수 있는 지점이다. "MAU 2,847,193명"이라는 숫자가 사실은 근사값일 수 있다는 이야기.

**uniqCombined** — 적응형 3단 구조:

> "an array is used" (작은 기수) → "a hash table is used" (중간) → "HyperLogLog is used, which will occupy a fixed amount of memory" (큰 기수)
> `[https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqcombined | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

특성:
> "Consumes several times less memory" / "Calculates with several times higher accuracy"

한계 (**책에 반드시 넣을 함정**):
> "the result will have very high error for cardinalities significantly larger than `UINT_MAX`"
> "the error will raise quickly after a few tens of billions of distinct values"

문서는 그 이상 기수에는 `uniqCombined64`를 권한다.

**uniqExact** — 정확하지만 무한히 커진다:

> "The `uniqExact` function uses more memory than `uniq`, because the size of the state has unbounded growth as the number of different values increases."
> "Use the `uniqExact` function if you absolutely need an exact result. Otherwise use the `uniq` function."
> `[https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqexact | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

**Martech 번역:**
- "이번 캠페인 도달 유니크 사용자 수" → `uniqCombined`로 충분. 대시보드 숫자가 0.5% 틀려도 아무도 안 죽는다.
- "이 쿠폰을 실제로 받은 사용자 수(정산 대상)" → `uniqExact`. 돈이 걸리면 근사는 안 된다.
- **이 구분을 못 하는 팀이 겪는 사고:** 마케팅 대시보드와 정산 리포트의 유니크 수가 안 맞아서 며칠간 원인 추적. 원인은 버그가 아니라 함수 선택이었다.

#### 트레이드오프·운영 함정

- **UPDATE/DELETE가 사실상 배치 작업이다.** ClickHouse의 mutation은 파트를 다시 쓴다. GDPR 삭제 요청(§횡단 주제)이 들어올 때 "사용자 한 명 지우기"가 테이블 전체 재작성으로 번질 수 있다. `ReplacingMergeTree`·파티션 단위 DROP 같은 설계를 미리 해둬야 한다.
- **JOIN이 약하다.** 고객 360을 만들 때 큰 테이블끼리 조인하면 무너진다. 보통 비정규화(넓은 이벤트 테이블)로 푼다.
- **머지가 밀리면 쿼리가 느려진다.** 작은 INSERT를 초당 수천 번 날리면 파트가 폭증하고 백그라운드 머지가 못 따라간다. **배치 INSERT가 원칙**이며, 이 때문에 Kafka → ClickHouse 사이에 버퍼링 계층이 필요하다.
- **ClickBench 수치 인용 시 주의:** ClickBench는 분석 DBMS 벤치마크로 `Combined / Cold Run / Hot Run / Load Time / Storage Size`를 측정한다. **운영 주체는 ClickHouse 측**(GitHub 저장소·도메인 구조로 확인). 즉 **제3자 중립 벤치마크가 아니라 ClickHouse가 운영하는 공개 벤치마크**다. 책에 수치를 쓸 거라면 반드시 이 사실을 병기할 것. 방법론 상세는 조회하지 못했다.
  `[https://benchmark.clickhouse.com/ | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]` — **구체 수치는 확인 불가 (미조회), 인용 금지**

---

### 1-3. Apache Flink

**[버전: 2.3.0 / 2026-06-25 기준, LTS는 1.20.5 / 2026-06-03]**
공식 다운로드 페이지: "Apache Flink® 2.3.0 is the latest stable release." 최근 릴리스 — 2.3.0 (2026-06-25), 2.2.1 (2026-05-15), 2.1.3 (2026-06-14), 1.20.5 LTS (2026-06-03).
`[https://flink.apache.org/downloads/ | 릴리스 날짜 페이지 표기 2026-06-25 | 검색 시점 2026-07-25]`

#### 이게 뭔가

상태를 가진(stateful) 스트림 처리 엔진. Martech에서 "실시간 세그먼트"와 "저니 트리거"라고 부르는 것의 실체는 대부분 Flink 잡이다.

#### 어떻게 동작하나

**이벤트 타임 vs 처리 타임 — Martech에서 이건 철학 문제다.**

> "Event time is the time that each individual event occurred on its producing device."
> `[https://nightlies.apache.org/flink/flink-docs-release-2.0/docs/concepts/time/ | 발행일 확인 불가 (미조회, 2.0 문서 브랜치) | 검색 시점 2026-07-25]`

문서는 처리 타임을 "가장 단순하고 빠르지만 분산 환경에서 결정론적이지 않다"고 정리한다. 이벤트 타임은 순서 뒤바뀜을 다뤄야 하지만 **재처리해도 같은 결과가 나온다**.

**Martech에서 이게 왜 결정적인가:** 지하철에서 앱을 쓴 사용자의 이벤트는 지상에 올라온 20분 뒤에 서버에 도착한다. 처리 타임 기준이면 그 사용자는 "20분 뒤에 장바구니를 담은 사람"이 되고, "장바구니 담고 30분 내 미결제 → 쿠폰 발송" 룰이 엉뚱한 시점에 발동한다. 이벤트 타임이면 실제로 담은 시각 기준으로 계산된다.

**워터마크 — 문서의 정의를 그대로 외울 가치가 있다:**

> "A Watermark(t) declares that event time has reached time t in that stream, meaning that there should be no more elements from the stream with a timestamp t' <= t."

즉 워터마크는 "이 시각 이전 데이터는 다 왔다고 치자"는 **선언**이다. 병렬 스트림에서는 여러 입력의 **최소** 이벤트 타임을 추적한다.

**지각 데이터(allowed lateness).** 워터마크를 넘겨 도착한 이벤트를 버리지 않고, 설정한 허용 지각 시간 안이면 결과를 갱신할 수 있다. 문서 표현으로는 "완전성과 적시성 사이의 균형".

**상태 관리.** Flink가 다른 스트림 도구와 갈리는 지점. 세션 윈도우("30분간 활동 없으면 세션 종료"), 패턴 매칭("A 다음 B가 오는데 C는 없이"), 사용자별 누적 카운터가 전부 상태다. 이 상태는 체크포인트로 내구성 있게 저장되고, 잡이 죽었다 살아나도 복원된다.

#### Martech에서 어디에 쓰이나

- **실시간 세그먼트 유지.** "최근 7일 3회 이상 구매" 같은 조건을 배치로 밤에 계산하는 대신, 이벤트가 올 때마다 상태를 갱신해 세그먼트 멤버십을 즉시 반영.
- **저니/오케스트레이션 트리거.** 세션 윈도우 + 타이머로 "장바구니 이탈 30분" 같은 **부재(absence) 조건**을 감지. 이게 어렵다 — "일어난 일"이 아니라 "안 일어난 일"을 감지해야 하고, 그러려면 상태와 타이머가 필수다.
- **실시간 집계 지표.** 캠페인 노출·클릭을 분 단위로 집계해 예산 소진 제어(pacing).
- **스트림 조인.** 광고 노출 스트림과 전환 스트림을 사용자·시간 윈도우로 조인해 어트리뷰션 계산.

#### 트레이드오프·운영 함정

- **워터마크 지연 설정이 곧 비즈니스 결정이다.** 지연을 5초로 잡으면 모바일 오프라인 이벤트를 대량으로 놓치고, 30분으로 잡으면 "실시간"이 30분 지연 시스템이 된다. **마케터에게 "실시간"이라고 말하기 전에 워터마크 값을 먼저 합의해야 한다.**
- **상태가 무한히 큰다.** 사용자별 상태를 TTL 없이 두면 상태 크기가 사용자 수에 비례해 무한 증가한다. Martech는 사용자 수가 수천만인 도메인이라 이게 즉시 문제가 된다.
- **운영 난이도가 스택에서 가장 높다.** 체크포인트 튜닝, 백프레셔, 상태 백엔드 선택(RocksDB), 사바포인트 기반 무중단 배포 — 소규모 팀이 Flink를 도입했다가 유지 못 하고 배치로 회귀하는 사례가 흔하다.
- **버전 경계 주의.** Flink는 2.x 계열과 1.20.x LTS가 병행 중이고(위 다운로드 페이지 기준) API 변화가 있다. 책에 코드를 넣을 거라면 **어느 계열 기준인지 명시**해야 한다.

---

### 1-4. Apache Iceberg

**[버전: 1.11.0 / 2026-05-19 기준 — 연도 확정]**
Apache 배포 아카이브 디렉터리 타임스탬프: `apache-iceberg-1.11.0/ — 2026-05-19 04:43`.
`[https://archive.apache.org/dist/iceberg/ | 2026-05-19 (전체 타임스탬프·확정) | 검색 시점 2026-07-25]`

> **연도 확정까지의 경위 (fact-checker 참고):** ① `iceberg.apache.org/releases/`·`/spec/`은 내비게이션 메뉴만 반환 — `1.11.0 (Latest)`는 **문서 버전 셀렉터 라벨**이고 날짜가 없어 근거로 쓰지 않았다. ② GitHub Releases는 `20 May 08:47`로 **연도 없음**. ③ 개별 태그 페이지(`/releases/tag/apache-iceberg-1.11.0`)를 열어도 **`YEAR NOT ON PAGE`**. ④ 최종적으로 Apache 아카이브에서 `2026-05-19 04:43`을 확정했다.
> **경미한 불일치:** GitHub은 `20 May`, 아카이브는 `2026-05-19` — 하루 차이(릴리스 태그 생성 시점 vs dist 업로드 시점, 타임존). 책에는 **`1.11.0 / 2026-05` 수준**으로 쓰는 게 안전하다.
> 스펙 본문은 아래 raw markdown으로 별도 조회했다.

#### 이게 뭔가

**테이블 포맷**이지 스토리지 엔진이 아니다. S3에 흩어진 Parquet 파일 더미 위에 "이건 하나의 테이블이고, 스키마는 이거고, 지금 스냅샷은 이거다"라는 메타데이터 층을 씌운 규격.

#### 어떻게 동작하나

스펙 원문:

> "Table metadata file tracks the table schema, partitioning config, custom properties, and snapshots of the table contents."

> "Data files in snapshots are tracked by one or more manifest files that contain a row for each data file in the table, the file's partition data, and its metrics."

`[https://raw.githubusercontent.com/apache/iceberg/main/format/spec.md | 발행일 확인 불가 (main 브랜치 시점) | 검색 시점 2026-07-25]`

구조는 3층이다: **테이블 메타데이터 파일 → 매니페스트 리스트(스냅샷당 1개) → 매니페스트 파일들 → 데이터 파일들.** 스냅샷은 특정 시점의 테이블 상태이고, 새 쓰기는 새 스냅샷을 만든다. 여기서 **타임 트래블**과 **원자적 커밋**이 자연히 나온다 — 메타데이터 포인터를 원자적으로 바꾸는 게 커밋의 전부다.

**스키마 진화 규칙 (스펙 원문):**

> "Valid primitive type promotions are: `int` to `long`, `float` to `double`, and `decimal(P, S)` to `decimal(P', S)` if P' > P."

> "any struct can evolve through deleting fields, adding new fields, renaming existing fields, reordering existing fields, or promoting a primitive using the valid type promotions"

**포맷 버전별 차이:**
- **v1** — Parquet/Avro/ORC 위 불변 파일 관리.
- **v2** — 행 수준 삭제 도입: "delete files to encode rows that are deleted in existing data files" — 데이터 파일을 다시 쓰지 않고 삭제/수정 가능.
- **v3** — 타입 시스템 확장: "New data types: nanosecond timestamp(tz), unknown, variant, geometry, geography" + 기본값(default values), 다중 인자 변환, **행 계보(row lineage)**.

(GitHub 릴리스 노트에서도 v3 관련 항목 확인 — 1.10.0의 "Spec: Update v3 summary, add row lineage", 1.11.0의 "Spec: bring back added-rows in snapshot fields".)

#### Martech에서 어디에 쓰이나 — 왜 고객 데이터 레이크하우스의 기본값이 되었나

이게 이 항목의 핵심이고, 개발자 독자가 "아 그래서"를 느끼는 지점이다.

1. **삭제할 수 있어야 한다.** 고객 데이터는 삭제 요청(GDPR/개인정보보호법)이 법적으로 강제된다. v2의 행 수준 delete가 없으면 "사용자 한 명 지우기"가 **수 TB 재작성**이 된다. 테이블 포맷 선택이 규제 대응 능력을 결정한다.
2. **스키마가 계속 변한다.** 이벤트 스키마는 제품이 바뀔 때마다 필드가 붙는다. 컬럼 추가·이름 변경·순서 변경을 데이터 재작성 없이 하는 능력이 필수.
3. **타임 트래블이 감사·재현의 근거다.** "3월 캠페인 때 이 사용자가 정말 VIP 세그먼트였나?"를 그 시점 스냅샷으로 증명할 수 있다. 마케팅 분쟁·정산 분쟁에서 실제로 쓰인다.
4. **엔진 중립.** 같은 테이블을 Spark로 쓰고, Trino로 질의하고, Flink로 스트리밍 적재하고, DuckDB로 로컬 탐색한다. 벤더 락인을 피하는 유일한 실용적 경로.

#### 트레이드오프·운영 함정

- **작은 파일 문제.** 스트리밍 적재는 작은 Parquet 파일을 대량 생산하고, 매니페스트가 비대해지며 스캔 플래닝이 느려진다. **컴팩션이 상시 운영 업무**다.
- **스냅샷이 무한히 쌓인다.** 만료 정책(expire snapshots)을 안 걸면 스토리지 비용과 메타데이터 크기가 계속 는다. 그런데 **너무 짧게 걸면 타임 트래블·삭제 감사 능력을 잃는다** — 규제 요구와 비용이 여기서 정면충돌한다.
- **카탈로그가 또 하나의 운영 대상.** Hive Metastore / REST catalog / Glue 중 뭘 쓸지, 그게 SPOF가 되지 않을지.
- **포맷 버전 호환.** v3 기능을 쓰면 v3를 못 읽는 엔진에서 못 읽는다. 여러 엔진이 붙는 Martech 스택에서 특히 조심.

---

### 1-5. Snowplow

**[버전: 확인 불가 — 아래 사유 참조]**
`https://github.com/snowplow/snowplow/releases`는 조회되었으나 최신 항목이 `22.01 Western Ghats — 31 Jan`, 그 앞이 `21.08 North Cascades — 31 Aug`, `R119 …` 형태였다. **이 모노레포 릴리스 라인은 현재 활성 릴리스 채널이 아니다**(현대 Snowplow는 컴포넌트별 저장소로 분리됨). 따라서 **현행 버전은 확인 불가 (미조회)**로 기록한다.
`[https://github.com/snowplow/snowplow/releases | 목록 표기, 연도 미표기 | 검색 시점 2026-07-25]`

#### 이게 뭔가

**스키마 검증을 1급 시민으로 만든 이벤트 수집 파이프라인.** 다른 수집 도구가 "일단 받고 나중에 정리"라면, Snowplow는 "스키마에 안 맞으면 유효 스트림에 넣지 않는다".

#### 어떻게 동작하나

공식 문서 기준 파이프라인:

- **Trackers** — 웹·모바일·서버·IoT에서 이벤트 생성 → Collector로 전송
- **Collector** — 원본을 클라우드 스토리지(S3/GCS)에 먼저 보존한 뒤 Enrich로 전달
- **Enrich** — 검증과 보강. 문서 원문:
  > "The **Enrich** application cleanses the data and validates each event against its schema to ensure it meets the criteria you have designed and set."
- **실패 이벤트 처리** — 검증 실패 레코드는 버려지지 않는다:
  > "failed events can be reprocessed"
- **Loaders** — 웨어하우스(Redshift/Snowflake/BigQuery)·레이크(S3/GCS/ADLS)로 적재
- 설계 철학:
  > "direct access to your raw Snowplow event data at the atomic level"

`[https://docs.snowplow.io/docs/fundamentals/ | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

#### 왜 "검증 기반 수집"이 중요한가 (개발자에게 이 대목을 팔아야 한다)

개발자에게 익숙한 비유: **이벤트 스키마는 API 스펙이다.** 그런데 대부분의 조직에서 이벤트는 API 없이 던져진다 — 프론트엔드 개발자가 `purchase_amount`를 문자열로 보내고, 다른 팀은 `purchaseAmount`로 보내고, 어떤 릴리스에서는 필드가 빠진다. 이게 몇 달 쌓이면 **아무도 이벤트 테이블을 못 믿는다.**

Snowplow의 답은 Iglu 스키마 레지스트리 + self-describing JSON이다. 이벤트가 자기 스키마 URI를 들고 다니고, Enrich가 그 스키마로 검증한다. 통과 못 하면 유효 스트림이 아니라 **실패 스트림**으로 간다 — 버려지지 않고, 스키마를 고친 뒤 재처리할 수 있다.

> **참고:** Iglu·self-describing JSON의 세부 스펙 문서는 이 세션에서 직접 조회하지 못했다. 위 개념 서술은 `fundamentals` 페이지의 검증 서술에 근거하며, **Iglu 스펙 세부(스키마 URI 형식·SchemaVer 규칙 등)는 확인 불가 (미조회)**다.

#### 트레이드오프·운영 함정 — 그리고 **라이선스 (반드시 책에 넣을 것)**

**Snowplow의 핵심 컴포넌트는 더 이상 OSI 오픈소스가 아니다.** 공식 FAQ:

> "Licensee is not granted the right to, and Licensee shall not, exercise the License for any Competing Use, and Licensee may exercise the License only for Non-Production Use or Non-Commercial Use."

버전 이력:
- **SLULA v1.0** — 2024년 1월 도입
- **SLULA v1.1** — "rolled out in December, 2024". v1.0의 "Highly Available" 조항을 제거했고, 그 결과 **고가용성 여부와 무관하게 모든 프로덕션 사용이 상용 라이선스를 요구**하는 것으로 정리되었다.

`[https://docs.snowplow.io/docs/licensing/limited-use-license-faq/ | v1.1 = 2024년 12월 (문서 표기) | 검색 시점 2026-07-25]`

**개발자 독자에게 이건 결정적 정보다.** "오픈소스 CDP 스택"이라며 Snowplow를 골랐다가 프로덕션 배포 직전에 라이선스 문제를 발견하는 사고가 실제로 일어난다. 검색 결과에서 Apache 2.0 포크(OpenSnowcat)가 존재한다는 언급을 확인했으나, **포크의 현황·유지보수 상태는 이 세션에서 조회하지 않았다 — 확인 불가 (미조회)**.

기타 함정:
- **스키마 설계가 선행 비용이다.** 검증의 이점은 스키마를 잘 설계했을 때만 나온다. 성급하게 시작하면 스키마 변경 요청이 병목이 된다.
- **실패 이벤트를 실제로 모니터링하지 않으면 무의미하다.** 검증 실패가 조용히 쌓이면 "데이터가 없다"는 사고가 뒤늦게 터진다.

---

### 1-6. RudderStack

**[버전: rudder-server v1.81.1 / 2026 기준]** — GitHub Releases: `v1.81.1 — 22 Jul 12:04`, `v1.81.0 — 21 Jul 05:09`.
`[https://github.com/rudderlabs/rudder-server/releases | 릴리스 목록 표기, 연도 미표기 (2026 추정) | 검색 시점 2026-07-25]`

#### 이게 뭔가

**warehouse-native CDP.** 데이터를 자기 SaaS에 복사해 보관하는 전통적 CDP와 달리, **고객의 데이터 웨어하우스를 단일 진실 원천으로 두고** 그 위에서 수집·활성화를 수행한다.

#### 어떻게 동작하나

공식 문서 기준 세 축:

1. **Event Stream** — SDK와 클라우드 앱 연동으로 웹·모바일·서버 이벤트 수집
2. **Reverse ETL** — SQL 모델·오디언스로 웨어하우스의 데이터를 비즈니스 도구로 되돌려 보냄
3. **Warehouse-Native 아키텍처** — Snowflake, BigQuery, Redshift, Databricks, PostgreSQL, MySQL, Trino와 직접 연동

SDK는 웹(JavaScript)·모바일(iOS/Android)·서버사이드(Node, Python, Java, Go 등)·크로스플랫폼을 지원하며, 200개 이상의 클라우드 앱·데스티네이션 연동을 제공한다.

**Segment 호환:** 문서에 "Segment to RudderStack Migration Guide"가 존재하며, 이는 Segment 이벤트 트래킹 API 규격과의 호환을 시사한다.

`[https://www.rudderstack.com/docs/ | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

> **라이선스 확인 실패:** `https://docs.rudderstack.com/rudderstack-open-source/`는 `https://rudderstack.com/docs/rudderstack-open-source/`로 리다이렉트되었고, 재조회 시 내비게이션만 반환했다. **RudderStack의 오픈소스 라이선스 종류는 확인 불가 (미조회)** — 책에 "오픈소스"라고 단정해 쓰지 말고, 저술 시 재확인 필요. (Snowplow 사례가 보여주듯 이 카테고리의 라이선스는 변동이 잦다.)

#### Martech에서 어디에 쓰이나 — Reverse ETL이 왜 중요한가

개발자에게 이 개념을 설명할 때 쓸 프레임: **ETL은 "데이터를 창고로", Reverse ETL은 "창고에서 현장으로".**

전통적 흐름은 앱 → 웨어하우스에서 끝났다. 분석가가 SQL로 "지난 30일 3회 이상 구매 + 최근 7일 미방문" 세그먼트를 만들면, 그 결과는 **웨어하우스 테이블 안에 갇혀 있었다.** 마케터가 그 세그먼트로 광고를 돌리려면 CSV로 뽑아서 광고 플랫폼에 업로드했다 — 수동, 지연, 오류.

Reverse ETL은 그 테이블을 광고 플랫폼·이메일 툴·CRM의 API로 동기화한다. 그래서 **"세그먼트 정의 = SQL 쿼리"**가 성립하고, 개발자·분석가가 이해하는 언어로 마케팅 타깃팅을 관리할 수 있게 된다. dbt(§1-7)와 짝을 이루는 이유가 여기 있다.

#### 트레이드오프·운영 함정

- **웨어하우스 왕복 지연.** warehouse-native의 대가는 지연이다. 웨어하우스에 적재 → 모델 실행 → Reverse ETL 동기화까지 시간이 걸린다. **"실시간 세그먼트"를 원하면 이 경로로는 안 된다** — 스트림 경로(Flink)가 따로 필요하다.
- **동기화 비용.** Reverse ETL은 대상 API의 rate limit에 부딪히고, 웨어하우스 컴퓨트를 반복 소모한다. 전량 동기화 vs 증분 동기화 설계가 비용을 가른다.
- **셀프호스팅 운영 부담.** 오픈소스로 돌리면 rudder-server·트랜스포머·데이터플레인을 직접 운영해야 한다.

---

### 1-7. dbt

**[버전: dbt-core 1.12.0 / 2026-07-16 기준. 2.0은 알파 단계 — v2.0.0-alpha.5 / 2026-07-20]**
GitHub Releases 표기: `dbt-core v1.12.0 — July 16, 2026`, `v2.0.0-alpha.5 — July 20, 2026`, `dbt-core v1.11.12 — July 1, 2026`.
`[https://github.com/dbt-labs/dbt-core/releases | 릴리스 날짜 표기 2026-07-16 | 검색 시점 2026-07-25]`

> **주의:** 2.0이 알파 상태라는 점은 책 집필 시점에 다시 확인해야 한다. 알파 → 정식 사이에 API가 바뀔 수 있으므로 **"1.12 / 2026 기준"으로 서술**하고 2.0은 "개발 중"으로만 언급하는 게 안전하다.

#### 이게 뭔가

**SQL 변환을 소프트웨어 엔지니어링처럼 관리하는 도구.** 개발자 독자에게는 이렇게 소개하면 즉시 통한다 — "SQL에 버전 관리·의존성 그래프·테스트·CI를 붙인 것".

#### 어떻게 동작하나

공식 문서:

> "Models are primarily written as a `select` statement and saved as a `.sql` file."

> "When you execute `dbt run`, you are running a model that will transform your data without that data ever leaving your warehouse."

> "A project is a directory of a `.yml` file (the project configuration) and either `.sql` or `.py` files (the models)."

> "A model is a single file containing a final `select` statement, and a project can have multiple models, and models can even reference each other."

Python 모델도 지원한다:
> "Starting in version 1.3, dbt Core and dbt support Python models. Python models are useful for training or deploying data science models, complex transformations..."

`[https://docs.getdbt.com/docs/build/models | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

> **확인 불가:** 머티리얼라이제이션(view/table/incremental/ephemeral) 세부, `ref()` 함수, DAG, 테스트의 상세는 이 페이지에 없었고 별도 페이지를 조회하지 않았다 — **확인 불가 (미조회)**. 책에 쓰려면 `docs.getdbt.com/docs/build/materializations` 등을 별도 확인할 것.

#### Martech에서 어디에 쓰이나 — 고객 360과 세그먼트를 SQL로 관리하는 패턴

이 항목의 핵심 서사. **"세그먼트 정의"라는 마케팅 개념이 개발자 세계에서 어떻게 생겼는지** 보여주는 최고의 사례다.

전형적 계층 구조:

```
staging/       원본 이벤트를 정규화 (stg_events, stg_orders, stg_users)
    ↓ ref()
intermediate/  아이덴티티 해석, 세션화 (int_identity_graph, int_sessions)
    ↓ ref()
marts/         고객 360 (dim_customer)
               세그먼트 (seg_high_value, seg_churn_risk, seg_cart_abandoners)
```

여기서 나오는 실무적 미덕:
- **세그먼트가 코드다.** PR로 리뷰되고, git blame으로 "이 정의를 누가 왜 바꿨는지" 추적된다. "VIP 세그먼트 기준이 언제 바뀐 거야?"라는 흔한 사고가 사라진다.
- **테스트가 붙는다.** "세그먼트 크기가 전일 대비 50% 이상 변하면 실패" 같은 테스트로, 잘못된 세그먼트가 캠페인으로 나가기 전에 막는다.
- **의존성 그래프가 영향 범위를 알려준다.** 원본 이벤트 필드 하나가 바뀔 때 어떤 세그먼트가 영향받는지 DAG가 보여준다.
- **Reverse ETL(§1-6)의 입력이 된다.** dbt가 만든 `seg_*` 테이블을 RudderStack이 광고 플랫폼으로 내보낸다.

#### 트레이드오프·운영 함정

- **배치다.** dbt는 스케줄 실행이다. "실시간 세그먼트"는 dbt로 못 만든다(§3-3 참조).
- **증분 모델의 함정.** 대형 이벤트 테이블을 매번 풀스캔하면 웨어하우스 비용이 폭발하므로 incremental을 쓰는데, **늦게 도착한 데이터(late-arriving data)**를 놓치기 쉽다. Martech의 모바일 이벤트는 늦게 오는 게 정상이라 이 문제가 상시 발생한다.
- **모델이 수백 개로 늘면 실행 시간이 SLA가 된다.** "매일 아침 9시 캠페인 전에 세그먼트가 준비돼야 한다"가 dbt 실행 시간에 걸린다.
- **웨어하우스 비용이 dbt 실행 빈도에 비례한다.** 세그먼트를 1시간마다 갱신하고 싶은 마케팅 요구와 비용이 정면 충돌한다.

---

### 1-8. Redis

**[버전: 8.8.1 / 2026 기준. 8.10은 RC 단계 — 8.10-RC2, 20 Jul]**
GitHub Releases: `8.8.1 — 23 Jul 19:30`, `8.6.5 — 23 Jul 19:27`, `8.4.5 — 23 Jul 19:24`, `8.2.8 — 23 Jul 19:20`, `7.4.10 — 23 Jul 18:01`, `8.10-RC2 — 20 Jul 18:23 (Pre-release)`.
`[https://github.com/redis/redis/releases | 릴리스 목록 표기, 연도 미표기 (2026 추정) | 검색 시점 2026-07-25]`

> 여러 유지보수 라인(8.8/8.6/8.4/8.2/7.4/7.2/6.2)이 같은 날 동시 패치된 패턴 — 보안 패치 배포로 보이나 **릴리스 노트 본문은 조회하지 않았다(확인 불가)**. 라이선스 정보도 이 페이지에는 없었다 — **Redis 라이선스 현황은 확인 불가 (미조회)**. (이 영역도 최근 몇 년 변동이 있었던 것으로 알려져 있으므로 책에 단정 서술 금지.)

#### 이게 뭔가

Martech에서 Redis는 캐시가 아니다. **밀리초 단위 의사결정 계층**이다. 사용자가 페이지를 여는 그 순간, 200ms 안에 "이 사람에게 이 배너를 보여줄까?"를 답해야 하는 자리.

#### 어떻게 동작하나 — 자료구조가 마케팅 질문에 어떻게 매핑되나

이 매핑 표가 이 항목의 핵심 산출물이다.

| Redis 자료구조 | 마케팅 질문 | 왜 이게 맞나 |
|---|---|---|
| **Hash** | "이 사용자의 프로필 속성은?" | 프로필 필드를 한 키에 모아 O(1) 조회 |
| **Set / Sorted Set** | "이 사용자가 속한 세그먼트는?" / "실시간 인기 상품 TOP 10은?" | 집합 연산(교집합=세그먼트 AND 조건), 점수 기반 랭킹 |
| **HyperLogLog** | "오늘 이 캠페인의 고유 도달 수는?" | 12KB 고정 메모리로 수십억 기수 근사 |
| **Bitmap** | "이 사용자가 오늘 방문했나?" (수천만 명 × 일별) | 사용자당 1비트 — 1천만 명 = 약 1.25MB |
| **String + TTL** | "이 사용자에게 오늘 푸시를 몇 번 보냈나?" (frequency capping) | INCR + EXPIRE로 원자적 카운터 + 자동 만료 |
| **Bloom filter** | "이 사용자가 이 광고를 이미 봤나?" | 사용자당 작은 필터로 재노출 방지 |

**HyperLogLog — 공식 문서 수치 (책에 그대로 쓸 수 있음):**

> "the Redis implementation for HyperLogLog, is less than 1%"
> "you no longer need to use an amount of memory proportional to the number of items counted, and instead can use a constant amount of memory; 12k bytes in the worst case"
> "The Redis implementation uses up to 12 KB of memory and provides a standard error rate of 0.81%."
> "The HyperLogLog can estimate the cardinality of sets with up to 18,446,744,073,709,551,616 (2^64) members."

명령: `PFADD` O(1), `PFCOUNT` O(1), `PFMERGE` O(N).

문서가 직접 드는 사용 사례가 그대로 Martech다:
> "How many unique visits has this page had on this day?"
> "Storing the IP address or any other kind of personal identifier is against the law in some countries, which makes it impossible to get unique visitor statistics on your website."

`[https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

**PFMERGE가 Martech에서 특별한 이유:** 캠페인별·일별 HLL을 따로 만들어두면, "이번 주 전체 고유 도달"을 원본 이벤트 재스캔 없이 **HLL 병합만으로** 구할 수 있다. 배치 집계 설계에서 이건 큰 차이다.

#### Martech에서 어디에 쓰이나

1. **실시간 프로필 조회** — 개인화 렌더링 시 사용자 속성·세그먼트 멤버십을 밀리초에 가져온다.
2. **Frequency capping** — "같은 광고 하루 3회 이상 금지". `INCR user:123:ad:456:20260725` + `EXPIRE`.
3. **Rate limiting** — "같은 사용자에게 푸시 1시간 1회". 슬라이딩 윈도우를 Sorted Set으로.
4. **중복 제거** — 이벤트 ID 기준 멱등 처리(§1-1의 at-least-once 보완).
5. **실시간 카운터** — 캠페인 예산 소진 제어.

#### 트레이드오프·운영 함정

- **메모리가 비용이다.** 수천만 사용자 프로필을 전부 Redis에 두면 비싸다. 핫 프로필만 두고 콜드는 다른 스토어로 계층화하거나, Aerospike처럼 SSD 하이브리드를 쓰는 선택지가 나온다(§3-2, 토스 사례 §3-6).
- **내구성 모델을 이해해야 한다.** RDB/AOF 설정에 따라 장애 시 손실 범위가 달라진다. "frequency cap 카운터가 리셋되어 같은 광고가 10번 나갔다"는 실제 사고 유형.
- **키 설계가 곧 아키텍처다.** TTL 없는 키는 영원히 남는다. 사용자 수 × 캠페인 수만큼 키가 생기는 설계는 순식간에 터진다.
- **HLL은 합집합만 된다.** `PFMERGE`는 합집합이고 **교집합은 없다.** "세그먼트 A와 B 둘 다 속한 고유 사용자 수"는 HLL로 직접 못 구한다 — 포함배제 원리로 근사하면 오차가 증폭된다. **이건 실무에서 자주 걸리는 함정이다.**

---

### 1-9. Apache Pinot (실시간 인입 + 저지연 집계)

> **선택 사유:** Druid와 Pinot 중 **Pinot을 Tier 1으로** 골랐다. Martech에서 이 계층의 요구는 "사용자에게 직접 보이는(user-facing) 저지연 분석 + 높은 동시성 + 프로필 업서트"인데, Pinot 문서가 이 요구를 명시적 수치로 표방하고 업서트를 지원하기 때문이다. **Druid는 Tier 2로 강등**(§2 참조).

**[버전: 1.5.1 / 2026-06-30 기준 — 연도 확정]**
Apache 배포 아카이브: `apache-pinot-1.5.1/ — 2026-06-30 22:18`, `apache-pinot-1.5.0/ — 2026-05-01 20:23`.
`[https://archive.apache.org/dist/pinot/ | 2026-06-30 (전체 타임스탬프·확정) | 검색 시점 2026-07-25]`

릴리스 성격은 GitHub Releases에서 확인: 1.5.1은 Netty/Log4j/BouncyCastle 등 의존성 CVE 대응 **보안 패치**("0 critical and 0 high"), 1.5.0은 멀티스테이지 쿼리 엔진 개선·UNNEST·조인 확장·멀티클러스터 라우팅 페더레이션 프레임워크.
`[https://github.com/apache/pinot/releases | 연도 미표기 (태그 페이지도 YEAR NOT ON PAGE) | 검색 시점 2026-07-25]`

> **불일치 병기:** GitHub 목록은 1.5.1을 `05 Jun`, 1.5.0을 `09 Apr`로 표기하나 Apache 아카이브는 각각 `2026-06-30`, `2026-05-01`이다. **상충: GitHub은 05 Jun / 아카이브는 2026-06-30.** (릴리스 태그 생성과 dist 업로드 시점 차이로 보인다.) 책에는 **`1.5.1 / 2026년 중반`** 수준으로 쓰고 특정 일자를 박지 말 것.

#### 이게 뭔가

실시간 스트림을 곧바로 인입하면서 밀리초대 집계 쿼리를 높은 동시성으로 처리하는 분산 OLAP 스토어.

#### 어떻게 동작하나

공식 문서:

- **Controller** — "The Pinot controller schedules and re-schedules resources in a Pinot cluster when metadata changes or a node fails."
- **Broker** — "The broker's responsibility is to route queries to the appropriate server instances" / "collects and merges the responses from all servers into a final result."
- **Server** — "offline servers host segments created by ingesting batch data" / "real-time servers ingest data from streaming sources, like Apache Kafka®, Apache Pulsar®, or AWS Kinesis."
- **Minion** — "A Pinot minion is an optional cluster component that executes background tasks on table data apart from the query processes performed by brokers and servers."
- **Segment** — "A Pinot segment is a partition." (Helix 용어 기준)
- **Offline table** — "Offline tables contain data from batch sources like CSV, Avro, or Parquet files."
- **Real-time table** — "Streaming data ends up in conventional segment files just like batch data, but is first accumulated in an in-memory data structure known as a consuming segment."

**성능 표방 (프로젝트 자체 문서 기준 — 제3자 벤치마크 아님):**
> "Ultra low-latency queries (as low as 10ms P95)"
> "High query concurrency (as many as 100,000 queries per second)"
> "real-time, user-facing use cases" / "High data freshness"

`[https://docs.pinot.apache.org/architecture-and-concepts/concepts/architecture.md | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

> **⚠️ 인용 시 필수 표기:** 위 `10ms P95`·`100,000 QPS`는 **Apache Pinot 프로젝트 자체 문서의 표방 수치**이며 독립 검증된 벤치마크가 아니다. 책에 쓸 때 반드시 "프로젝트 문서 표방 기준"을 붙일 것. (첫 조회 URL `https://docs.pinot.apache.org/basics/architecture`는 404였고, 404 페이지가 안내한 `.md` 경로로 재조회해 얻었다.)

#### Martech에서 어디에 쓰이나

**ClickHouse와 겹치는 것 같지만 자리가 다르다.** 개발자 독자에게 이 구분을 명확히 해줘야 한다.

- **ClickHouse의 자리** — 분석가·마케터가 대시보드에서 던지는 무거운 애드혹 쿼리. 동시성은 낮고(수십), 쿼리는 복잡하고, 데이터는 크다.
- **Pinot의 자리** — **최종 사용자에게 직접 노출되는** 분석. 광고주 대시보드("내 캠페인 지금 성과"), 판매자 대시보드, 앱 안의 개인 통계. 동시성은 높고(수천~수만), 쿼리는 정형화되어 있고, 지연은 밀리초여야 한다.

Martech에서 후자가 실재한다 — 광고 플랫폼의 광고주 콘솔이 정확히 이 패턴이다.

**업서트**: 실시간 테이블에서 같은 기본 키의 최신 레코드로 갱신하는 기능이 있어, **변경되는 사용자 프로필/세그먼트 상태를 스트림으로 유지**하는 데 쓸 수 있다.
> ⚠️ 업서트의 세부 동작·제약(파티셔닝 요구, 메모리 비용 등)은 이 세션에서 조회하지 않았다 — **확인 불가 (미조회)**.

#### 트레이드오프·운영 함정

- **운영 컴포넌트가 많다.** Controller/Broker/Server/Minion + ZooKeeper(Helix) — ClickHouse 단일 바이너리 대비 진입 장벽이 높다.
- **인덱스를 미리 설계해야 한다.** star-tree·inverted·bloom 등 인덱스 종류를 테이블 설계 시점에 정해야 하고, 이는 쿼리 패턴을 미리 안다는 전제다. **애드혹 탐색에는 안 맞는다.**
  > ⚠️ 인덱스 종류별 세부는 확인 불가 (미조회) — 위 목록은 조회 결과에 명시적으로 열거되지 않았다. 책에 쓰려면 별도 확인 필요.
- **1.5.1이 보안 패치 릴리스**라는 점은, 이 계층 도구들이 대량의 JVM 의존성을 끌고 다닌다는 현실을 보여준다. 사내 보안 스캔 통과가 지속적 운영 업무가 된다.

---

### 1-10. Trino

**[버전: Release 483 / 2026-07-17 기준]**
공식 릴리스 노트: `Release 483 (17 Jul 2026)`, `482 (25 Jun 2026)`, `481 (11 May 2026)`, `480 (24 Mar 2026)`, `479 (14 Dec 2025)`.
`[https://trino.io/docs/current/release.html | 릴리스 날짜 페이지 표기 2026-07-17 | 검색 시점 2026-07-25]`

> Trino는 단조 증가 정수 릴리스 번호(semver 아님)를 쓴다. 개발자 독자에게 짚어줄 만한 특징.

#### 이게 뭔가

**저장하지 않는 SQL 질의 엔진.** 데이터는 S3·Kafka·PostgreSQL·MongoDB 어디에 있든 그대로 두고, Trino가 커넥터로 붙어 하나의 SQL로 질의한다.

#### 어떻게 동작하나 / 무엇이 아닌가

공식 문서가 "아닌 것"을 아주 분명히 말한다 — 이 인용들이 책에서 값지다:

> "Do not mistake the fact that Trino understands SQL with it providing the features of a standard database."

> "Trino is not a replacement for databases like MySQL, PostgreSQL or Oracle."

> "Trino was not designed to handle Online Transaction Processing (OLTP)."

무엇인가:
> "Trino is a tool designed to efficiently query vast amounts of data using distributed queries."

> "Trino is not limited to accessing HDFS. Trino can be and has been extended to operate over different kinds of data sources, including traditional relational databases and other data sources such as Cassandra."

용도:
> "data warehousing and analytics: data analysis, aggregating large amounts of data and producing reports"

`[https://trino.io/docs/current/overview/use-cases.html | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

#### Martech에서 어디에 쓰이나 — 연합 질의가 왜 여기서 특히 유용한가

고객 데이터는 **구조적으로 흩어져 있다.** 이건 설계 실패가 아니라 정상 상태다:

- 이벤트 → S3 Iceberg 테이블
- 주문·회원 정보 → 프로덕션 PostgreSQL/MySQL
- 캠페인 발송 이력 → 마케팅 SaaS가 내려준 CSV
- 실시간 세그먼트 상태 → Kafka 토픽

"지난달 이 캠페인을 받은 사람 중 실제 구매한 사람"을 알려면 이 넷을 조인해야 한다. 전부 한 웨어하우스로 옮기는 데 몇 달 걸린다. **Trino는 그 이주를 기다리지 않고 지금 답을 준다.**

레이크하우스 위에서는 Iceberg 커넥터로 S3 위 테이블을 SQL로 질의하는 표준 경로가 된다.

#### 트레이드오프·운영 함정

- **소스 시스템을 죽일 수 있다.** 프로덕션 MySQL에 커넥터를 붙여놓고 무거운 조인을 던지면 서비스 DB가 넘어간다. **Martech 분석 쿼리는 크기 예측이 어려워서 특히 위험하다.**
- **연합 조인은 데이터를 네트워크로 끌어온다.** "Trino가 알아서 최적화하겠지"가 아니다. 큰 테이블 두 개를 서로 다른 소스에서 조인하면 둘 다 Trino 워커로 빨려온다.
- **메모리 기반이라 거대 조인에서 OOM.** 워커 메모리 설정과 쿼리 크기의 싸움.
- **결과 재현성이 없다.** 소스가 계속 변하므로 어제 쿼리와 오늘 쿼리 결과가 다르다. 정산·감사에는 스냅샷(Iceberg 타임 트래블)이 필요하다.

---

### 1-11. DuckDB

**[버전: 1.5.5 / 2026-07-22 기준. LTS는 1.4.5 / 2026-06-17]**
공식 뉴스 페이지: 1.5.5 (2026-07-22), 1.5.4 "Variegata" (2026-06-17), 1.4.5 LTS "Andium" (2026-06-17), 1.5.3 (2026-05-20), 1.5.0 (2026-03-09).
`[https://duckdb.org/news/ | 릴리스 날짜 페이지 표기 2026-07-22 | 검색 시점 2026-07-25]`

#### 이게 뭔가

**인프로세스 분석 DB.** "분석용 SQLite"라는 비유가 가장 빠르다. 서버가 없다. 라이브러리를 import하면 그게 데이터베이스다.

#### 어떻게 동작하나

**인프로세스 임베디드 구조.** 공식 문서:

> "DuckDB does not run as a separate process, but completely **embedded within a host process**."

이 한 줄이 모든 걸 설명한다. 서버 프로세스가 없으니 네트워크 왕복도, 직렬화 비용도, 배포 복잡도도 없다. §1-10의 Trino가 "분산 워커 클러스터"인 것과 정반대 극단이다.

**컬럼 지향 벡터화 실행 엔진:**

> "DuckDB uses a **columnar-vectorized query execution engine**, where queries are still interpreted, but a large batch of values (a 'vector') are processed in one operation."

행 하나씩 처리하는 전통적 인터프리터와 달리 **벡터 단위(값 묶음)로 처리**한다. 인터프리터의 오버헤드를 벡터 크기만큼 분산시키는 것 — 컴파일 없이 컴파일에 가까운 성능을 얻는 절충안이다. ClickHouse(§1-2)가 같은 계열의 선택을 한 이유와 같다.

**복사 없는 직접 질의:**

> "the DuckDB Python package can run queries directly on Pandas data without ever importing or copying any data."

Parquet·CSV·JSON을 임포트 없이 직접 읽는다. **Martech 실무에서 이건 크다** — S3에서 내린 이벤트 Parquet에 바로 SQL을 던질 수 있다.

**그 외 (문서 기준):**
- **ACID** — 대량 작업에 최적화된 자체 MVCC로 트랜잭션 보장
- **확장성** — 커스텀 타입·함수·파일 포맷을 확장 메커니즘으로. Parquet 지원과 타임존 처리도 확장으로 구현되어 있다
- **단순성** — 외부 의존성 없이 단일 헤더/구현 파일 쌍으로 컴파일. **"SQLite 수준의 배포 용이성 + OLAP 지향"**이라는 포지션이 여기서 나온다

`[https://duckdb.org/why_duckdb | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

> ⚠️ 스토리지 포맷 세부·Iceberg/httpfs 등 개별 확장·성능 벤치마크는 여전히 **확인 불가 (미조회)**. 위 서술은 `why_duckdb` 페이지에 명시된 범위로 한정된다.

#### Martech에서 어디에 쓰이나

개발자 독자가 **오늘 당장 써볼 수 있는** 유일한 항목이라서, 책의 실습 챕터에 가장 적합하다.

1. **세그먼트 로직 로컬 검증.** 웨어하우스에서 100만 행 샘플을 Parquet으로 내리고, 노트북에서 DuckDB로 세그먼트 SQL을 수십 번 반복 실행하며 다듬는다. 웨어하우스 비용 0.
2. **데이터 품질 조사.** "이 이벤트 필드가 언제부터 null이 됐지?"를 S3 Parquet에 직접 물어본다.
3. **임베디드 분석.** 사내 툴이나 CLI 안에 분석 기능을 넣을 때 별도 DB 서버 없이.
4. **파이프라인 단위 테스트.** dbt 모델 로직을 CI에서 DuckDB로 검증 — 실제 웨어하우스 없이 테스트가 돈다.
5. **책의 실습 환경.** 독자가 `pip install duckdb` 한 줄로 이벤트 분석·퍼널 쿼리를 따라 할 수 있다. **이 책에 실습을 넣는다면 DuckDB가 최선의 선택이다.**

#### 트레이드오프·운영 함정

- **단일 프로세스.** 동시 다중 사용자 서비스용이 아니다. 프로덕션 대시보드 백엔드로 쓰면 안 된다.
- **메모리 한계.** 노트북 RAM을 넘는 데이터는 (스필 기능이 있어도) 느려진다.
- **버전 라인이 둘.** 1.5.x와 1.4.x LTS가 병행 중이므로, 책에 코드를 넣을 때 **어느 라인 기준인지 명시**해야 한다. DuckDB는 과거 스토리지 포맷 호환성 이슈로 알려진 적이 있으므로 특히 주의.

---

### 1-12. Feast

**[버전: 0.65.0 / 2026 기준]** — GitHub Releases: `v0.65.0 — 20 Jul 13:28` (릴리스 노트에 **Aerospike·ScyllaDB 온라인 스토어 지원 추가**, OpenLineage 컨슈머 연동 언급), `v0.64.0 — 13 Jun 11:22`, `v0.63.0 — 04 May 03:44`.
`[https://github.com/feast-dev/feast/releases | 릴리스 목록 표기, 연도 미표기 (2026 추정) | 검색 시점 2026-07-25]`

> **주목:** 0.65.0에서 Aerospike·ScyllaDB가 온라인 스토어로 추가된 것은 §3-2(아이덴티티 스토어)와 정확히 맞물리는 신호다 — 피처 스토어의 온라인 계층이 요구하는 특성이 Martech 프로필 스토어의 요구와 같다는 방증.

#### 이게 뭔가

**피처 스토어.** ML 모델이 쓰는 입력값(피처)을 학습 시점과 서빙 시점에 **일관되게** 공급하는 계층.

#### 어떻게 동작하나

공식 문서:

> "Feast's architecture is designed to be flexible and scalable. It is composed of several components that work together to provide a feature store."

> Feast는 "a Push Model to ingest data from different sources and store feature values in the online store"를 사용한다.

> "supports feature transformation for On Demand and Streaming data sources"

> "precomputing features is the recommended optimal path to ensure low latency performance"

`[https://docs.feast.dev/getting-started/architecture/overview | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

**Point-in-time join — 이게 피처 스토어의 존재 이유다:**

> "Feast is able to join features from one or more feature views onto an entity dataframe in a point-in-time correct way."

> "Feast is able to reproduce the state of features at a specific point in the past."

> "For each row within the entity dataframe, Feast will query and join the selected features from the appropriate feature view data source."

> "will scan backward in time from the entity dataframe timestamp up to a maximum of the TTL time specified"

> "the TTL time is relative to each timestamp within the entity dataframe. TTL is not relative to the current point in time (when you run the query)."

`[https://docs.feast.dev/getting-started/concepts/point-in-time-joins | 발행일 확인 불가 (미조회) | 검색 시점 2026-07-25]`

#### 왜 온라인/오프라인 스토어가 분리되나 — 학습-서빙 스큐

개발자 독자에게 이 개념을 설명하는 가장 좋은 예시가 Martech에 있다.

**이탈 예측 모델을 만든다고 하자.** 피처 중 하나가 "지난 30일 구매 횟수"다.

- **학습 시점** — 분석가가 웨어하우스에서 `SELECT COUNT(*) ... WHERE date BETWEEN ...`으로 뽑는다. 배치 SQL.
- **서빙 시점** — 실시간으로 예측해야 하니 백엔드 개발자가 Redis에서 카운터를 읽는다. 완전히 다른 코드.

두 계산이 **미묘하게 다르다.** 학습 쪽은 환불 건을 제외했는데 서빙 쪽은 포함한다. 학습 쪽은 UTC 기준이고 서빙 쪽은 KST다. 모델은 오프라인 평가에서 AUC 0.85가 나왔는데 프로덕션에서는 형편없다. **이게 학습-서빙 스큐다.**

피처 스토어의 답: **피처 정의를 한 곳에 등록하고, 오프라인 스토어(학습용 히스토리)와 온라인 스토어(서빙용 최신값)로 같은 정의를 물질화(materialize)한다.**

**데이터 누수(leakage)와 point-in-time correctness:** 위 문서 인용이 말하는 "과거 특정 시점의 피처 상태를 재현"이 없으면, 학습 데이터에 **미래 정보가 새어든다.** 예: "2026-03-01에 이탈했는가"를 라벨로 쓰면서 피처는 오늘 기준 "지난 30일 구매 횟수"를 쓰면, 모델은 이탈 이후의 행동까지 보고 학습한다. 오프라인 성능은 환상적이고 프로덕션은 무너진다. **Martech의 이탈 예측·전환 예측 모델이 실패하는 가장 흔한 이유가 이것이다.**

#### 트레이드오프·운영 함정

- **물질화 지연.** 온라인 스토어는 배치 물질화로 채워지는 경우가 많아, "최신 피처"가 사실 몇 시간 전 값일 수 있다.
- **온라인/오프라인 스토어를 둘 다 운영해야 한다.** 인프라 비용과 복잡도가 두 배.
- **작은 팀에겐 과할 수 있다.** 모델이 두세 개면 피처 스토어 없이도 규율만으로 관리 가능하다. 모델·피처가 수십 개로 늘 때 가치가 나온다.
- **0.x 버전대다.** 0.65.0이라는 버전은 API 안정성이 semver 1.0 수준으로 보장되지 않는다는 신호. 책에 코드를 넣을 때 버전 명시 필수.

---

## 2. Tier 2 포지셔닝

> **⚠️ 이 절의 모든 항목: `버전 확인 불가 (미조회)`.** 리서치 예산을 Tier 1 깊이에 집중하기 위해 의도적으로 조회하지 않았다. 아래 서술은 **개념적 포지셔닝**이며, 챕터에 **버전·수치·성능 주장으로 옮기면 안 된다.** 옮기려면 저술 시점에 공식 문서를 별도 확인할 것. (Tier 1의 사례가 보여주듯, 기억 기반 버전은 거의 항상 틀린다.)

### 스트리밍 전송 계층

**Redpanda** — Kafka API 호환, C++ 구현, ZooKeeper/JVM 없음. **언제 고르나:** 운영 인력이 적은데 Kafka 생태계 호환성은 필요할 때. 단일 바이너리 운영이 매력. 라이선스 모델을 반드시 확인할 것.

**Apache Pulsar** — 스토리지(BookKeeper)와 서빙 분리, 멀티 테넌시·지역 간 복제가 1급 기능, 큐 시맨틱과 스트림 시맨틱을 모두 지원. **언제 고르나:** 여러 브랜드/테넌트의 Martech 데이터를 한 클러스터에서 격리 운영해야 할 때, 지역 간 복제가 요구사항일 때.

### 수집 계층

**Jitsu** — 오픈소스 이벤트 수집·라우팅. Segment 스타일 API에 가벼운 셀프호스팅. **언제 고르나:** Snowplow의 스키마 규율까지는 필요 없고, 라이선스 자유도와 간편함이 중요할 때.

**OpenTelemetry** — **제품 텔레메트리와 마케팅 이벤트의 관계**를 짚을 좋은 소재. OTel은 관측성(trace/metric/log)용 표준이고, 마케팅 이벤트는 비즈니스 의미 단위다. 겹치는 것 같지만 목적이 다르다 — OTel 스팬은 "이 요청이 340ms 걸렸다", 마케팅 이벤트는 "이 사람이 장바구니에 담았다". **다만 수렴 압력이 있다:** 둘 다 "사용자 행동의 시계열"이고, OTel의 시맨틱 컨벤션·수집 파이프라인(Collector) 설계는 이벤트 수집 설계와 배울 게 많다. **언제 고르나:** 마케팅 이벤트 파이프라인을 OTel로 대체하려 하지 말 것. 다만 OTel Collector를 이벤트 라우팅에 재활용하는 선택지는 실재한다.

### 스트림 처리

**Kafka Streams** — 별도 클러스터 없이 애플리케이션 라이브러리로 동작. **언제 고르나:** 이미 JVM 서비스가 있고, 상태 있는 처리가 필요하지만 Flink 클러스터를 운영할 여력은 없을 때. (LINE 사례 §3-6 참조 — "Kafka Streams는 '라이브러리'입니다"라는 인용이 이 성격을 정확히 짚는다.)

**Spark Structured Streaming** — 마이크로배치 기반. **언제 고르나:** 이미 Spark 배치 자산이 크고, 초 단위 지연이면 충분할 때. 배치와 스트리밍 코드를 통합하고 싶을 때.

**Materialize** — 증분 유지 관리되는 뷰(incrementally maintained materialized view)를 SQL로. **언제 고르나:** "이 세그먼트를 항상 최신으로 유지"를 Flink 코드가 아니라 SQL로 선언하고 싶을 때. Martech 세그먼트와 개념적 궁합이 매우 좋은 카테고리.

**Arroyo** — Rust 기반 스트림 처리 엔진, SQL 중심. **언제 고르나:** Flink의 운영 부담 없이 SQL 스트림 처리를 원할 때. 성숙도를 반드시 확인할 것.

### 분석 스토어

**Apache Druid** — 실시간 인입 + 시계열 롤업에 강한 원조격. Controller 대신 Coordinator/Overlord/Historical/MiddleManager 구조. **언제 고르나:** 시간 기반 대시보드·모니터링이 주 용도이고, 롤업(사전 집계)으로 비용을 줄이고 싶을 때. Pinot과 자리가 겹치나 롤업·시계열 지향이 상대적으로 강하다.
*(**버전 예외 — 이 항목만 연도 확정**: Apache 배포 아카이브에서 `37.0.0 — 2026-05-06 04:19`, `36.0.0 — 2026-05-01 23:41`, `35.0.0 — 2025-11-05 22:01` 확인. `[https://archive.apache.org/dist/druid/ | 2026-05-06 (전체 타임스탬프·확정) | 2026-07-25]`. GitHub Releases는 `08 May`로 연도 미표기였고 태그 페이지도 `YEAR NOT ON PAGE`였다. **아키텍처·기능 서술은 여전히 확인 불가 (미조회)** — Druid 공식 문서를 조회하지 않았으므로 위 성격 규정은 통념 수준이다.)*

**StarRocks** — MPP 분석 DB, 조인 성능과 레이크하우스 질의를 함께 노림. **언제 고르나:** ClickHouse의 약한 조인이 병목인데 고객 360처럼 조인이 본질적일 때.

### 테이블 포맷·저장 포맷

**Delta Lake** — Databricks 진영 테이블 포맷. **언제 고르나:** 이미 Databricks/Spark 중심 조직일 때.

**Apache Hudi** — 업서트·증분 처리에 강점을 두고 출발한 포맷. **언제 고르나:** CDC(변경 데이터 캡처) 기반 증분 적재가 핵심 워크로드일 때. 고객 프로필 테이블처럼 갱신이 잦은 경우.

**Parquet** — 포맷 자체. 컬럼 지향 + 열별 압축 + 열별 통계(min/max)로 **프레디킷 푸시다운**이 가능하다. Iceberg/Delta/Hudi는 전부 이 위에 얹힌 메타데이터 층이라는 점을 개발자에게 짚어줄 것 — "테이블 포맷 vs 파일 포맷"의 구분이 이 스택 이해의 관문이다.

### 웨어하우스 (아키텍처 특성)

**Snowflake** — 스토리지/컴퓨트 완전 분리, "가상 웨어하우스" 단위로 컴퓨트를 켜고 끔. 비용 모델이 **컴퓨트 사용 시간 기반**이라, dbt 실행 빈도를 늘리면 비용이 선형으로 는다. **언제 고르나:** 워크로드별 컴퓨트 격리(마케팅 팀 쿼리가 데이터 엔지니어링 잡을 방해하지 않게)가 중요할 때.

**BigQuery** — 서버리스, 슬롯 기반 실행. **온디맨드는 스캔한 바이트 기준 과금**이라 "SELECT *"가 곧 돈이다. 파티셔닝·클러스터링이 비용 최적화의 핵심. **언제 고르나:** 운영 인력 없이 시작하고 싶을 때, GA4 등 Google 생태계와 붙을 때(Martech에서 실제로 큰 이유).

**Redshift** — 전통적으로 노드 기반, 이후 서버리스·RA3(스토리지 분리) 옵션 추가. **언제 고르나:** AWS 생태계 통합이 지배적 제약일 때.

> ⚠️ 세 웨어하우스의 **현행 비용 모델·기능 세부는 확인 불가 (미조회)**. 위는 아키텍처 성격 수준의 서술이며, 가격·슬롯·크레딧 관련 구체 수치는 절대 기억으로 쓰지 말 것.

### 오케스트레이션

**Airflow** — DAG를 Python으로. 사실상 업계 표준. **언제 고르나:** 이질적 시스템을 순서대로 엮는 게 주 과제일 때.

**Dagster** — 자산(asset) 중심 모델. "이 테이블은 어떤 테이블들로부터 만들어지는가"를 1급 개념으로. **언제 고르나:** dbt와 궁합이 좋고, 데이터 계보(lineage)와 데이터 품질을 오케스트레이션에 통합하고 싶을 때.

**Airbyte** — ELT 커넥터 플랫폼. **언제 고르나:** 광고 플랫폼·CRM·결제 SaaS 등 수십 개 소스에서 데이터를 끌어와야 할 때. Martech은 소스가 많은 게 특징이라 이 카테고리가 실제로 중요하다.

### KV / 프로필 스토어

**Cassandra / ScyllaDB** — 넓은 컬럼 스토어, 쓰기 처리량과 수평 확장에 강함. ScyllaDB는 C++ 재구현. **언제 고르나:** 프로필·이벤트 이력이 Redis 메모리에 안 들어갈 규모이고, 파티션 키 기준 조회가 지배적일 때.

**Aerospike** — 하이브리드 메모리/SSD 아키텍처(인덱스는 메모리, 데이터는 SSD). **언제 고르나:** 수억 프로필을 밀리초에 조회해야 하는데 전량 RAM은 비용이 감당 안 될 때. **애드테크/Martech에서 실사용이 두터운 카테고리** — 토스 피처 스토어의 온라인 스토어가 Aerospike이고(§3-6), Feast 0.65.0이 Aerospike 온라인 스토어를 추가했다(§1-12). 두 신호가 같은 방향을 가리킨다.

**RocksDB** — 임베디드 LSM 트리 KV 엔진. 직접 쓰기보다 **다른 시스템의 내부 엔진**으로 만난다 — Flink 상태 백엔드, Kafka Streams 상태 스토어가 대표적. **언제 고르나:** 직접 고르는 게 아니라, Flink 상태 튜닝을 할 때 "이게 RocksDB 튜닝이구나"를 알아야 할 때.

### 벡터 DB

**pgvector** — PostgreSQL 확장. **언제 고르나:** 이미 Postgres를 쓰고 있고 벡터 규모가 크지 않을 때. 별도 시스템 추가 없이 시작.

**Qdrant / Milvus** — 전용 벡터 검색 엔진. **언제 고르나:** 사용자·상품 임베딩이 수천만~수억 규모이고 필터링 결합 ANN 검색이 필요할 때.

**Martech에서 벡터 DB가 왜 나오나:** ① 룩얼라이크 오디언스 — 사용자 임베딩의 최근접 이웃이 곧 "비슷한 고객"이다(토스 사례 §3-6의 Two-tower 임베딩이 정확히 이 구조). ② 상품 추천 후보 생성. ③ LLM 기반 자연어 세그먼트 질의의 RAG 계층.

> ⚠️ 세 벡터 DB 모두 **확인 불가 (미조회)**.

---

## 3. 횡단 주제

---

### 3-1. 근사 자료구조 — 마케팅 질문과 자료구조의 매핑

이 절이 개발자 독자에게 가장 "새로운 지식"이 될 부분이다. 핵심 서사: **마케팅 지표는 대부분 정확할 필요가 없고, 그 사실을 이용하면 메모리를 수천 배 아낄 수 있다.**

#### 매핑 표

| 마케팅 질문 | 자료구조 | 정확도 | 메모리 | 근거 |
|---|---|---|---|---|
| "이번 캠페인 고유 도달 수는?" | HyperLogLog | 표준 오차 0.81% | 최대 12KB (고정) | Redis 공식 문서 |
| "이 사용자가 이 광고를 이미 봤나?" | Bloom filter | 거짓 양성만 발생, 거짓 음성 없음 | 0.1% 오류율 시 항목당 14.378비트 | Redis 공식 문서 |
| "이 사용자가 이 광고를 봤나?" + 삭제 필요 | Cuckoo filter | 삭제 가능 | — | Redis 공식 문서 |
| "이 상품/캠페인의 노출 빈도는?" | Count-Min Sketch | 임계값 이상만 신뢰 | 폭 w = 2/error | Redis 공식 문서 |
| "세션 길이의 p50/p90/p99는?" | t-digest | compression 파라미터로 조절 | 압축된 센트로이드 | Redis 공식 문서 |

#### HyperLogLog — 고유 사용자 수

§1-8의 인용 그대로:
> "The Redis implementation uses up to 12 KB of memory and provides a standard error rate of 0.81%."
> "The HyperLogLog can estimate the cardinality of sets with up to 18,446,744,073,709,551,616 (2^64) members."
`[https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ | 발행일 확인 불가 | 2026-07-25]`

**대비를 만드는 계산:** 1,000만 명의 고유 방문자를 Set으로 세면 사용자 ID를 전부 저장해야 한다. HLL은 12KB다. **이 대비가 이 절 전체의 훅이다.**

**한계:** 합집합(PFMERGE)은 되지만 **교집합은 없다.** "A 세그먼트 ∩ B 세그먼트의 고유 수"는 HLL로 직접 못 구한다.

#### Bloom filter — 이미 본 사용자 제외 / frequency capping

**Redis 공식 문서가 광고 사용 사례를 직접 든다** — 책에 그대로 쓸 수 있는 인용:

> "Ad placement (retail, advertising) — This application answers these questions: Has the user already seen this ad? Has the user already bought this product?"

> "Use a Bloom filter for every user, storing all bought products. The recommendation engine suggests a new product and checks if the product is in the user's Bloom filter."

보장의 비대칭성 — 이걸 개발자에게 정확히 전달해야 한다:

> "A Bloom filter can guarantee the absence of an item from a set, but it can only give an estimation about its presence. So when it responds that an item is not present in a set (a negative answer), you can be sure that indeed is the case. But one out of every N positive answers will be wrong."

**Martech 번역:** "안 봤다"는 확실하고 "봤다"는 틀릴 수 있다. 즉 **광고를 안 본 사람에게 안 보여주는 실수는 없고, 본 적 없는데 "봤다"고 판정해 노출을 건너뛰는 실수만 있다.** 광고 노출 기회를 약간 잃을 뿐 사용자를 괴롭히지는 않는다 — **보수적으로 안전한 방향이다.** 이 방향성 분석이 개발자에게 "아, 이래서 이걸 쓰는구나"를 준다.

메모리 수치 (문서 원문):
> "1% error rate requires 7 hash functions and 9.585 bits per item."
> "0.1% error rate requires 10 hash functions and 14.378 bits per item."
> "0.01% error rate requires 14 hash functions and 19.170 bits per item."

Set과의 대비:
> "For a set of IP addresses, for example, we would have around 40 bytes (320 bits) per item - considerably higher than the 19.170 bits we need for a Bloom filter with a 0.01% false positives rate."

용량 초과 시 동작 (운영 함정):
> "Adding an item to a Bloom filter never fails due to the data structure 'filling up'. Instead, the error rate starts to grow."
> 자동 스케일 시 "latency for adds stays the same, but the latency for presence checks increases" — 서브필터가 쌓이면 조회가 느려진다.

Cuckoo와의 비교:
> "Bloom filters typically exhibit better performance and scalability when inserting items... Cuckoo filters are quicker on check operations and also allow deletions."

**Martech 함의:** 삭제가 필요하면(사용자가 캠페인에서 이탈해 노출 이력을 리셋해야 하면) Cuckoo, 아니면 Bloom.

`[https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/ | 발행일 확인 불가 | 2026-07-25]`
원 논문 링크 (문서가 제시): Burton H. Bloom, "Space/Time Trade-offs in Hash Coding with Allowable Errors" — 문서에 링크 존재. **논문 자체는 미조회.**

#### Count-Min Sketch — 빈도 추정

> "Count-Min Sketch is a probabilistic data structure in Redis Open Source that can be used to estimate the frequency of events/elements in a stream of data."
> "It uses a sub-linear space at the expense of over-counting some events due to collisions."

**가장 중요한 경고 (그대로 인용할 것):**
> "It is very important to know that the results coming from a Count-Min sketch lower than a certain threshold (determined by the error_rate) should be ignored and often even approximated to zero. So Count-Min sketch is indeed a data-structure for counting frequencies of elements in a stream, but it's only useful for higher counts. Very low counts should be ignored as noise."

임계값 공식:
> `threshold = error * total_count`

문서의 균등분포 예시가 교육적이다 — 1,000개 원소가 각각 500회면 error 0.001에서 임계값이 500이 되어 **아무것도 못 믿는다.** 문서는 직접 이렇게 결론짓는다:
> "This shows that a CMS is maybe not the best data structure to count frequency of a uniformly distributed stream."

정규분포/헤비히터 예시에서는 임계값 2,000이 평균 500과 8,000 사이에 놓여 잘 작동한다.

**Martech 번역:** CMS는 **롱테일이 아니라 헤비히터를 찾는 도구**다. "가장 많이 노출된 광고 TOP N", "가장 많이 본 상품"에는 맞고, "이 사용자가 이 상품을 몇 번 봤나"(개별 저빈도)에는 안 맞는다. **이 구분을 못 하면 조용히 틀린 숫자를 보고 있게 된다.**

`[https://redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/ | 발행일 확인 불가 | 2026-07-25]`
원 논문 링크 (문서 제시): "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" — 링크 존재. **논문 자체는 미조회.**

#### t-digest — 분위수

> "t-digest is a data structure that will estimate a percentile point without having to store and order all the data points in a set."

> "The `COMPRESSION` argument is used to specify the tradeoff between accuracy and memory consumption. The default value is 100. Higher values mean more accuracy."

병합 가능:
> "suppose we measure latencies for 3 servers, and we want to calculate the 90%, 95%, and 99% latencies for all the servers combined" → `TDIGEST.MERGE`

trimmed mean:
> "A trimmed mean is the mean value from the sketch, excluding observation values outside the low and high cutoff percentiles."

**Martech 번역:**
- "우리 사용자의 세션 길이 중앙값과 p90은?" — 평균은 소수의 봇/이상치가 망친다. 분위수가 진실을 말한다.
- "구매 금액 상위 10%의 기준선은 얼마인가?" — VIP 세그먼트의 임계값을 데이터로 정한다. `TDIGEST.QUANTILE 0.9`.
- **trimmed mean이 특히 유용하다** — "이상치를 뺀 평균 객단가"는 마케팅 리포트에서 실제로 원하는 숫자다.
- 병합 가능성 덕에 지역별·채널별로 따로 만든 다음 합칠 수 있다.

`[https://redis.io/docs/latest/develop/data-types/probabilistic/t-digest/ | 발행일 확인 불가 | 2026-07-25]`
원 논문 링크 (문서 제시): "The t-digest: Efficient estimates of distributions" (ScienceDirect) — 링크 존재. **논문 자체는 미조회.**

#### 이 절을 챕터로 쓸 때의 프레임

**"마케터가 요구하는 정확도와 시스템이 지불하는 비용은 협상 가능하다."**
개발자는 보통 "정확한 숫자"를 기본값으로 삼는다. 하지만 MAU 숫자가 2,847,193이든 2,847,900이든 어떤 마케팅 의사결정도 바뀌지 않는다. **그 0.81%의 오차를 받아들이는 대가로 메모리를 수천 배 아낀다.** 반대로 쿠폰 정산 대상자 수는 한 명도 틀리면 안 된다. **어느 숫자가 어느 쪽인지 판별하는 능력이 Martech 개발자의 핵심 역량이다.**

---

### 3-2. 아이덴티티 스토어 — 밀리초 프로필 조회와 ID 그래프

#### 요구사항이 왜 특수한가

Martech의 개인화는 **사용자가 페이지를 여는 그 순간** 답을 내야 한다. 페이지 렌더링 예산이 200ms라면 프로필 조회에 쓸 수 있는 건 10~20ms다. 이건 OLAP 스토어(ClickHouse·Trino)로는 불가능한 요구다 — §1-2에서 봤듯 MergeTree는 8192행 그래뉼 단위로만 접근하고, §1-10에서 봤듯 Trino는 "not designed to handle OLTP"라고 문서가 직접 못박는다.

**그래서 같은 고객 데이터가 두 벌 존재한다.** 이게 개발자가 처음 Martech 아키텍처 다이어그램을 볼 때 "왜 이렇게 중복이 많지?"라고 느끼는 이유이고, 답은 **조회 패턴이 근본적으로 다르기 때문**이다.

| | 분석 경로 | 서빙 경로 |
|---|---|---|
| 질문 | "지난달 VIP 세그먼트는 몇 명?" | "이 사람은 VIP인가?" |
| 접근 | 수억 행 스캔·집계 | 키 하나 조회 |
| 지연 | 초~분 | 밀리초 |
| 동시성 | 수십 | 수만 |
| 스토어 | ClickHouse / Iceberg+Trino | Redis / Aerospike / Cassandra |

#### KV 스토어 선택 기준

- **Redis** — 가장 빠르고 자료구조가 풍부하다(§1-8 표). 전량 메모리라 비용이 규모에 비례해 커진다.
- **Aerospike** — 인덱스는 메모리, 데이터는 SSD. **수억 프로필 규모에서 비용/성능 균형**. 토스 피처 스토어의 온라인 스토어가 이것(§3-6), Feast 0.65.0이 온라인 스토어로 추가(§1-12).
- **Cassandra / ScyllaDB** — 쓰기 처리량과 수평 확장. 프로필 이력까지 넓게 보관할 때.

> ⚠️ Aerospike·Cassandra·ScyllaDB의 성능 수치·아키텍처 세부는 **확인 불가 (미조회)**.

#### ID 그래프 — 어떻게 저장하나

**문제:** 한 사람이 여러 식별자를 가진다. 로그인 전 웹 쿠키, 로그인 후 회원 ID, 모바일 앱 디바이스 ID, 이메일 해시, 광고 ID. "이 다섯 개가 같은 사람"임을 알아야 개인화가 성립한다.

**개발자에게 익숙한 자료구조로 설명하면:** 이건 **union-find(disjoint set)** 문제다. 식별자가 노드, "같은 사람" 관찰이 간선, 연결 요소가 한 사람.

저장 전략은 대략 세 갈래로 갈린다:

1. **정규 ID 매핑 테이블** — `identifier → canonical_person_id`를 KV에 평탄화. 조회는 O(1)로 가장 빠르다. 단점: 두 사람이 사실 한 사람이었다고 판명되어 병합할 때, **한쪽의 모든 식별자를 다시 써야 한다.**
2. **간선 저장 + 배치 해석** — 관찰된 간선만 저장하고, 배치(dbt/Spark)로 연결 요소를 계산해 매핑 테이블을 재생성. 정확하지만 지연이 있다.
3. **그래프 DB** — 관계를 1급으로. 유연하지만 밀리초 조회 요구와 궁합이 나쁠 수 있다.

**실무에서 흔한 구조는 1+2 하이브리드다** — 배치로 정확히 계산하고 결과를 KV에 물질화, 스트림에서는 새 간선을 즉시 반영하되 완전 해석은 다음 배치로 미룬다. §3-3의 배치/스트리밍 이중 구조와 정확히 같은 패턴이다.

**함정 (Martech 특유):**
- **과병합이 프라이버시 사고다.** 공용 PC의 쿠키를 두 사람의 계정에 잘못 연결하면, A의 구매 이력이 B에게 개인화되어 노출된다. **이건 버그가 아니라 사고다.**
- **병합은 되돌리기 어렵다.** 잘못 합친 두 프로필을 다시 가르는 건 원본 간선 이력을 보존해야만 가능하다. **간선 원장을 append-only로 남겨야 하는 이유.**
- **삭제 요청이 그래프를 관통한다.** "내 데이터 지워줘"는 그 사람의 모든 식별자에 연결된 데이터를 지우라는 뜻이고, 그러려면 ID 그래프가 정확해야 한다.

> ⚠️ 이 소절의 저장 전략 서술은 **공개 1차 문서를 직접 조회한 것이 아니라 스택 문서들에서 추론한 아키텍처 정리**다. 책에 쓸 때 "일반적 패턴" 수준으로 서술하고, 특정 제품의 구현이라고 단정하지 말 것.

---

### 3-3. 배치 vs 스트리밍 세그먼트 계산

개발자 독자가 Martech에서 가장 자주 마주칠 설계 결정. **같은 세그먼트를 두 방식으로 만들 수 있고, 결과는 같은데 비용·지연·복잡도가 완전히 다르다.**

#### 예시 세그먼트

"최근 30일 내 3회 이상 구매했고, 최근 7일간 앱을 열지 않은 사용자"

#### 배치 경로

```
Kafka → (적재) → Iceberg/웨어하우스 → dbt 모델 (매일 새벽 3시) → seg_churn_risk 테이블 → Reverse ETL → 광고 플랫폼
```

- **지연:** 최대 24시간. 오늘 오후에 조건을 만족해도 내일 새벽에야 세그먼트에 들어간다.
- **비용:** 하루 한 번, 전체 스캔. 웨어하우스 컴퓨트를 그만큼만 쓴다.
- **복잡도:** SQL 한 파일. 신규 입사자도 읽는다.
- **재계산:** 로직을 바꾸면 다음 실행에 자동 반영. **정정이 쉽다.**
- **정확도:** 매번 원본에서 다시 계산하므로 드리프트가 없다.

#### 스트리밍 경로

```
Kafka → Flink (사용자별 상태: 30일 구매 카운트 + 마지막 앱 오픈 시각 + 타이머) → 세그먼트 진입/이탈 이벤트 → Redis/Pinot → 실시간 활성화
```

- **지연:** 초 단위.
- **비용:** 24시간 상시 가동. 사용자 수만큼 상태를 메모리/RocksDB에 유지.
- **복잡도:** 상태 관리, 워터마크, 체크포인트, 상태 스키마 진화. **운영 난이도가 몇 배다.**
- **재계산:** 로직을 바꾸면 **상태를 어떻게 할 것인가**가 문제가 된다. 처음부터 다시 흘려야 하나? 사바포인트에서 이어야 하나? **정정이 어렵다.**
- **미묘한 함정:** "30일 윈도우"를 스트림에서 유지하려면 30일치 이벤트를 상태로 들고 있거나, 슬라이딩 카운터를 근사해야 한다. **"최근 7일 미방문"처럼 부재 조건은 타이머로만 감지된다** — 아무 이벤트도 오지 않는 사용자를 어떻게 알아채나? 타이머를 걸어둬야 한다.

#### 비용 구조의 차이 (개발자가 놓치는 지점)

배치는 **계산량에 비례**하고, 스트리밍은 **시간에 비례**한다.

- 배치: 세그먼트 100개를 하루 한 번 = 하루 100번의 스캔 비용.
- 스트리밍: 세그먼트 100개 = 100개의 Flink 잡이 24시간 돌거나, 하나의 잡이 100개 상태를 유지. **사용자가 조용한 새벽 시간에도 클러스터는 켜져 있다.**

**따라서 결정 규칙:** 세그먼트가 많고 지연 요구가 느슨하면 배치가 압도적으로 싸다. 세그먼트가 소수인데 지연이 결정적이면 스트리밍이 정당하다.

#### 실무의 답은 대개 "둘 다"

**Lambda 아키텍처의 Martech 버전이 여기서 자연스럽게 나온다(§3-4).** 대부분의 세그먼트는 배치, **전환에 직결되는 소수**(장바구니 이탈, 결제 실패, 첫 구매 축하)만 스트리밍.

**개발자가 마케터에게 물어야 할 단 하나의 질문:** *"이 세그먼트가 5분 늦으면 무슨 일이 일어나나요?"*
- "아무 일도 안 일어나요" → 배치.
- "고객이 이미 경쟁사에서 샀어요" → 스트리밍.

이 질문 하나가 아키텍처 비용을 몇 배 가른다. **책의 실용적 하이라이트로 쓸 만한 문장.**

> ⚠️ 이 절은 §1-1·1-3·1-7의 조회된 문서 특성에 근거한 **아키텍처 분석**이며, 특정 출처의 인용이 아니다.

---

### 3-4. Lambda / Kappa 아키텍처의 고객 데이터 플랫폼 버전

#### Lambda — 배치 층 + 속도 층

**원형:** 배치 층이 전체 데이터에서 정확한 뷰를 만들고, 속도 층이 최근 데이터로 근사 뷰를 만들고, 서빙 층이 둘을 합친다.

**CDP에서의 형태:**
- 배치 층 — Iceberg/웨어하우스 위 dbt가 밤새 고객 360과 세그먼트를 정확히 재계산
- 속도 층 — Flink가 오늘 들어온 이벤트로 세그먼트 델타를 유지
- 서빙 층 — 조회 시 "어제까지의 배치 결과 + 오늘의 스트림 델타"를 합쳐 응답

**Pinterest 사례가 정확히 이 구조다** (§3-6):
> "Streaming Path... Batch Path... This lambda-style architecture balances freshness (streaming updates) with completeness (batch corrections)"
`[https://medium.com/pinterest-engineering/making-user-sequence-data-more-cost-efficient-faster-and-easier-to-use-2a56a928cae1 | 2026-05-21 | 2026-07-25]`

**Lambda의 고질병:** 같은 세그먼트 로직을 SQL(배치)과 Java/Flink(스트림)로 **두 번 구현**해야 한다. 두 구현이 미묘하게 갈라지면 "배치 대시보드와 실시간 개인화가 다른 답을 준다"는 사고가 난다. Martech에서는 이게 마케터의 신뢰를 무너뜨린다.

**Pinterest의 답이 인상적이다** — "one definition, many runtimes": 정의를 한 번 쓰고 스트리밍/배치 런타임이 그 정의를 각각 실행한다. 두 구현이 갈라지는 문제를 정의 계층 통합으로 푼 것.

#### Kappa — 스트림 하나로 통일

**원형:** 배치 층을 없애고, 모든 것을 스트림으로 처리한다. 재계산이 필요하면 로그를 처음부터 다시 흘린다.

**CDP에서의 형태:** Kafka에 원본 이벤트를 충분히 길게(또는 티어드 스토리지로 무기한) 보관하고, 세그먼트 로직이 바뀌면 새 Flink 잡을 오프셋 0부터 돌려 새 결과를 만든 뒤 전환.

**Kappa가 성립하는 조건:**
- 이벤트 로그가 완전한 진실이어야 한다. **그런데 Martech는 안 그런 경우가 많다** — CRM의 회원 등급, 결제 시스템의 환불, 오프라인 매장 구매는 이벤트 스트림 밖에서 온다.
- 재처리 비용을 감당할 수 있어야 한다. 3년치 이벤트를 다시 흘리는 건 며칠짜리 작업일 수 있다.

**현실:** 순수 Kappa로 가는 Martech 스택은 드물다. 웨어하우스에 있는 마스터 데이터(회원·상품·주문)와의 조인이 본질적이기 때문이다. **다만 "이벤트 로그를 진실의 원천으로 두고 파생을 재계산 가능하게 만든다"는 Kappa의 철학은 거의 모든 현대 CDP가 채택했다.**

#### 개발자에게 전달할 핵심

**"두 층이 존재하는 건 게으름이 아니라 물리다."** 정확성과 신선도는 동시에 최대화할 수 없다. Lambda는 그걸 인정하고 둘 다 만든 것, Kappa는 신선도를 택하고 정확성을 재처리로 회수하려는 것. **Martech 아키텍처 다이어그램이 복잡해 보이는 이유의 절반이 이 트레이드오프다.**

> ⚠️ Lambda/Kappa의 원전(Nathan Marz, Jay Kreps의 글)은 이 세션에서 조회하지 않았다 — **원전 출처는 확인 불가 (미조회)**. 인용하려면 별도 확인 필요. 위 서술 중 Pinterest 관련 부분만 조회된 근거가 있다.

---

### 3-5. 스키마·데이터 계약 (data contract)

#### 왜 이게 Martech에서 특히 치명적인가

일반 백엔드에서 잘못된 데이터는 에러 로그를 남기고 알림이 울린다. **Martech에서 잘못된 이벤트는 조용히 잘못된 캠페인을 발송한다.**

구체적 사고 시나리오 — 책에 쓸 만한 것들:

1. **필드 이름이 바뀌었다.** 앱 릴리스에서 `purchase_amount` → `amount`. 세그먼트 SQL은 `purchase_amount`를 참조한다. NULL이 되고, "고액 구매자" 세그먼트가 **0명이 된다.** 아무도 에러를 안 본다 — 쿼리는 성공했다. 마케터는 "이번 달 VIP 캠페인 성과가 왜 없지?"라고 3주 뒤에 묻는다.
2. **타입이 바뀌었다.** `amount`가 숫자에서 문자열 `"39,900"`으로. 합계가 이상해지거나 조용히 0이 된다.
3. **단위가 바뀌었다.** 원 → 센트. "10만원 이상 구매자" 세그먼트가 **전 사용자**가 된다. 그리고 전 사용자에게 VIP 쿠폰이 나간다. **이건 돈이 나가는 사고다.**
4. **이벤트가 중복 발송된다.** SDK 버그로 `purchase`가 두 번 찍히면 구매 횟수 기반 세그먼트가 전부 부풀려진다.

**공통점: 시스템은 아무 에러도 내지 않는다.** 데이터 파이프라인은 성공했고, SQL은 실행됐고, 캠페인은 발송됐다. **틀린 대상에게.**

#### 스키마 검증이 답인 이유

§1-5에서 본 Snowplow의 접근:
> "The **Enrich** application cleanses the data and validates each event against its schema to ensure it meets the criteria you have designed and set."
> "failed events can be reprocessed"
`[https://docs.snowplow.io/docs/fundamentals/ | 발행일 확인 불가 | 2026-07-25]`

**두 문장이 함께 중요하다.** 검증만 하고 실패 이벤트를 버리면 데이터 손실이다. 검증하고 **격리해서 보관하고 재처리 가능하게** 만드는 게 완성형이다.

#### 개발자에게 익숙한 프레임으로

**이벤트 스키마 = API 스펙.** 백엔드 개발자는 API 응답 형식을 바꿀 때 버저닝하고, 컨슈머에게 알리고, 마이그레이션 기간을 둔다. 그런데 **같은 개발자가 프론트엔드 이벤트는 아무 협의 없이 바꾼다.** 왜? 이벤트에는 컴파일러도, 타입 체커도, 통합 테스트도 없기 때문이다.

**데이터 계약(data contract)은 그 빈자리를 메우려는 시도다:**
- 스키마를 코드 저장소에 두고 PR로 리뷰
- CI에서 스키마 호환성 검사(하위 호환 깨지면 빌드 실패)
- 프로듀서 SDK가 스키마에서 타입 생성 → 컴파일 타임에 잡힘
- 런타임 검증 → 실패 스트림으로 격리
- 소비자(세그먼트 SQL·모델)가 어느 필드에 의존하는지 계보 추적 → 영향 범위 산정

**Iceberg의 스키마 진화 규칙(§1-4)이 저장 계층에서 같은 문제를 다룬다:**
> "Valid primitive type promotions are: `int` to `long`, `float` to `double`, and `decimal(P, S)` to `decimal(P', S)` if P' > P."

허용되는 변경을 **명시적으로 열거**한다는 점이 핵심이다. 이건 곧 "이 변경은 안전하고 저 변경은 안전하지 않다"는 계약이다.

#### 스키마 레지스트리

Snowplow는 Iglu, Kafka 생태계에는 Confluent Schema Registry(Avro/Protobuf/JSON Schema)가 있다. 역할은 같다 — **스키마의 단일 진실 원천 + 호환성 정책 강제.**

> ⚠️ Iglu·Confluent Schema Registry의 스펙 세부(SchemaVer, 호환성 모드 종류 등)는 이 세션에서 조회하지 않았다 — **확인 불가 (미조회)**.

#### 이 절의 챕터 프레임

**"타입 시스템 없는 데이터에 타입 시스템을 되돌려주기."** 개발자 독자는 타입 안정성의 가치를 이미 안다. 이벤트 데이터가 타입 없는 세계라는 걸 깨닫는 순간, 왜 Martech 데이터 팀이 스키마에 그렇게 집착하는지 이해한다.

---

### 3-6. AI/ML 층

> **주의:** 이 절은 **공개 문서·공개 기술블로그에서 확인된 것만** 기록한다. 벤더 제품이 "AI로 무엇을 한다"는 마케팅 주장은 이 축의 담당이 아니고, 확인되지 않은 것은 쓰지 않았다.

#### 확인된 실제 사례: 토스 광고 ML 스택

한국 개발자 독자에게 가장 가치 있는 사례다 — **국내 서비스가 어떤 모델 구조를 실제로 쓰는지** 공개한 드문 글.

`[https://toss.tech/article/ads-ml | 2025-04-21 | 저자: 김영호 (토스 Ads Performance 팀 ML Engineer) | 검색 시점 2026-07-25]`

3단 구조:

1. **Targeting — Lookalike**
   > "유저의 행동 로그를 학습하거나 Two-tower 모델을 통해 유저와 광고 간의 상호작용을 학습하여 유저 임베딩을 생성"

   → 광고주의 타겟 오디언스와 유사한 잠재 고객 탐색. **§2의 벡터 DB가 필요해지는 지점이 정확히 여기다** — 임베딩 최근접 이웃 검색.

2. **Filtering — 후보군 선정**
   Two-tower 임베딩으로 수백만 광고 중 관련성 높은 후보를 빠르게 검색.

3. **Ranking — CTR 예측**
   > "CTR 예측 모델은 광고 ID, 유저 속성 등 고차원의 희소 특징 간의 상호작용을 효과적으로 학습"

   FM, DeepFM, DCN 구조로 eCPM(1,000회 노출당 기대 수익) 산출.

**개발자에게 이 사례가 좋은 이유:** "추천 시스템"이라는 뭉뚱그린 말 대신 **후보 생성 → 필터링 → 랭킹**이라는 3단 파이프라인 구조를 보여주고, 각 단계에 다른 모델이 들어간다는 걸 명확히 한다. 그리고 이 구조가 광고·상품 추천·콘텐츠 추천에 공통으로 적용된다.

#### 확인된 실제 사례: 토스 피처 스토어 (학습-서빙 일관성)

`[https://toss.tech/article/feature-store-trainkit | 2025-08-14 | 저자: 우종호·송석현 (토스 ML Platform Team) | 검색 시점 2026-07-25]`

- **오프라인 스토어:** Hive 테이블 (배치 처리 데이터, 모델 학습용)
- **온라인 스토어:** **Aerospike** — 저지연 추론 지원, 메모리/SSD 하이브리드
- **데이터 누수 방지 (원문 인용):**
  > "Target 데이터를 기준으로 시간 파티션을 Shift 할 수 있어요. 예를들어, 01시에 발생한 피드백 데이터라도 Shift 기능을 사용하여 00시에 발생한 Feature들과 조인하여 데이터 누수를 방지할 수 있습니다."
- Training-Serving Skew를 피처 정의 통합 + 중앙 메타데이터 등록으로 방지

**§1-12(Feast)와 나란히 놓으면 완벽한 대비가 된다** — 오픈소스 표준(Feast)과 실제 사내 구현(토스 Trainkit)이 같은 문제를 같은 방식으로 푼다는 걸 보여준다. **개발자 독자에게 "이건 이론이 아니라 실무"라는 확신을 준다.**

#### 확인된 실제 사례: 토스 TUES — 세그먼테이션에 ML 적용

`[https://toss.tech/article/tues | 2026-06-16 | 저자: 우찬희 (Director of Data Analytics, Toss) | 검색 시점 2026-07-25]`

TUES = Toss User Engagement Segment. 플랫폼 수준 사용자 세그먼테이션 프레임워크.

- 원문 인용: **"각 유저의 서비스 이용 패턴을 기준으로 비슷한 유저들끼리 묶어둔 세그먼트"**
- **V1:** K-Means Clustering (하드 클러스터링) → 룰 기반 세그먼트
- **V2:** NMF (Nonnegative Matrix Factorization, 소프트 클러스터링) → **확률적 세그먼트 멤버십**
- **처리 모델: 배치 — 월 단위로 계산.** 실시간이 아니다.

**이 사례가 §3-3(배치 vs 스트리밍)의 완벽한 실증이다.** 2,800만 MAU 규모의 플랫폼 세그먼테이션이 **월 배치**로 돈다. "모든 게 실시간이어야 한다"는 개발자의 직관이 틀렸다는 증거.

**그리고 V1→V2의 하드→소프트 클러스터링 전환이 흥미롭다:** 사람은 하나의 세그먼트에 딱 떨어지지 않는다. 확률적 멤버십이 마케팅 현실에 더 맞는다.

#### AI/ML 층의 지형 (개념 정리)

| 과제 | 접근 | Martech 맥락 | 확인 상태 |
|---|---|---|---|
| 룩얼라이크 오디언스 | Two-tower 임베딩 + ANN 검색 | 기존 고객과 유사한 잠재 고객 | ✅ 토스 사례 확인 |
| CTR/전환 예측 | FM / DeepFM / DCN | 광고 랭킹, eCPM 산출 | ✅ 토스 사례 확인 |
| 세그먼테이션 | K-Means → NMF | 플랫폼 수준 사용자 그룹화 | ✅ 토스 사례 확인 |
| 이탈 예측 | 지도학습 분류 | 이탈 위험 세그먼트 | ⚠️ 확인 불가 (미조회) |
| Send-time optimization | 사용자별 최적 발송 시각 예측 | 푸시·이메일 발송 타이밍 | ⚠️ 확인 불가 (미조회) |
| LLM 카피 생성 | 생성 모델 | 캠페인 문구 변형 생성 | ⚠️ 확인 불가 (미조회) |
| 자연어 세그먼트 질의 (text-to-SQL) | LLM + 스키마 컨텍스트 | "지난달 3번 산 사람" → SQL | ⚠️ 확인 불가 (미조회) |

> **⚠️ 확인 불가 항목 처리 지침:** 이탈 예측·send-time optimization·LLM 카피 생성·text-to-SQL은 이 세션에서 **공개 1차 문서를 조회하지 못했다.** 업계에서 널리 언급되는 카테고리이지만, **어느 제품이 실제로 무엇을 쓰는지는 확인하지 않았다.** 책에 쓸 때는 "이런 과제 영역이 있다" 수준의 서술로 제한하거나, 저술 시점에 별도 리서치를 요청할 것. **특정 벤더가 이 기능을 제공한다는 서술은 이 문서를 근거로 쓸 수 없다.**

#### 이 절의 챕터 프레임

**"Martech의 AI는 대부분 LLM이 아니다."** 2026년의 독자는 "AI"를 들으면 LLM을 떠올리지만, Martech에서 실제로 돈을 버는 ML은 **임베딩·랭킹·클러스터링**이다. 토스 사례 세 개가 이걸 증명한다. LLM은 그 위에 얹히는 인터페이스 계층(카피 생성, 자연어 질의)이지 코어가 아니다. 이 구분을 명확히 하는 게 이 챕터의 가치다.

---

### 3-7. 실제 회사 아키텍처 사례

> 각 항목은 **실제로 fetch해서 발행일을 확인한 것만** 기록했다.

#### 우아한형제들 — Kafka 기반 배달 이벤트 파이프라인

`[https://techblog.woowahan.com/17386/ | 2024-05-30 | 저자: 김나은 | 검색 시점 2026-07-25]`

일 100만 건 이상의 배달을 처리하는 분산 이벤트 기반 아키텍처. 세 가지 축:

1. **안전한 주문-배달 처리** — 이벤트 순서 보장 + **Transactional Outbox Pattern** (Debezium MySQL 커넥터)
   > "데이터와 메시지 발행의 트랜잭션을 하나로 관리하여 데이터 정합성을 확보할 필요가 있었습니다."
2. **이벤트 버스** — Spring Cloud RemoteApplicationEvent로 여러 배달 서버의 인메모리 설정값 동기화
3. **실시간 분석** — Kafka Streams로 배달 이벤트 실시간 집계 → 대시보드
   > "카프카 스트림즈는 메시지를 활용한 실시간 집계, 분석 시스템으로 실시간 데이터 스트리밍 및 분석 시스템에 적합한 플랫폼입니다."
   > "카프카는 분산 스트리밍 플랫폼으로, 대량의 데이터를 처리하고 실시간으로 전송하는 데 사용됩니다."

**책에서의 활용:** Transactional Outbox는 **§1-1의 exactly-once 논의와 직결**된다. "Kafka가 exactly-once를 지원한다"는 말과 "DB 트랜잭션과 이벤트 발행의 원자성"은 다른 문제이고, 후자를 푸는 게 Outbox 패턴이다. Martech에서 "주문은 됐는데 이벤트가 안 갔다"(또는 반대)는 세그먼트를 조용히 망가뜨린다.

#### LINE — Kafka Streams 내부 메시지 파이프라인

`[https://engineering.linecorp.com/ko/blog/applying-kafka-streams-for-internal-message-delivery-pipeline | 2016-08-18 | 저자: Kawamura Yuto | 검색 시점 2026-07-25]`

> ⚠️ **2016년 글 — 구버전 정보일 수 있음.** Kafka Streams API는 이후 크게 변했다. **고전 레퍼런스로만 인용하고, 현재 API 서술의 근거로 쓰지 말 것.**

해결한 문제:
1. **확장성** — 단일 인스턴스 큐 병목 → 파티션된 Kafka 토픽으로 분산
2. **내구성** — 휘발성 인메모리 Redis 큐 → 디스크 기반 영속 저장
   > "서버가 어떤 이유로 종료되면 queue의 내용 역시 모두 잃게 됩니다."
3. **순서 보장** — **userId를 파티셔닝 키로** 사용해 태스크 처리 순서 유지

성격 규정 (인용 가치 높음):
> "Kafka Streams는 '라이브러리'입니다. 실행 프레임워크가 아니기 때문에 사용자가 수동으로 구동해야 합니다."

격리의 가치:
> "프로세싱을 격리시키게 되면 동일 consumer 컨텍스트 내에서 연관되지 않은 태스크 처리 중 발생한 스토리지 요청이 오래 걸리거나 실패처럼 보이는 상황에서도 다른 프로세서들의 태스크 처리가 멈추지 않도록 할 수 있습니다."

**책에서의 활용:** **"userId를 파티션 키로"가 §1-1에서 설명한 순서 보장 원리의 실제 적용 사례다.** 이론과 실무를 잇는 다리로 쓸 것. 또 "Kafka Streams는 라이브러리다"라는 규정은 §2의 Kafka Streams vs Flink 선택 기준을 정확히 짚는다.

#### Pinterest — 사용자 시퀀스 데이터 플랫폼

`[https://medium.com/pinterest-engineering/making-user-sequence-data-more-cost-efficient-faster-and-easier-to-use-2a56a928cae1 | 2026-05-21 | 저자: Pinterest Engineering (Ajay Venkatakrishnan, Le Zhang, Eric Shang, Pihui Wei, Connor Votroubek, Yi He, Camilo Munoz, Simin Li) | 검색 시점 2026-07-25]`

**가장 최신이자 이 리서치에서 가장 값진 사례.** ML 모델용 "사용자 시퀀스"(사용자 이벤트의 순서 있는 보강 리스트) 플랫폼을 "one definition, many runtimes"로 재설계.

- **스트리밍 경로:** 실시간 인덱서가 "filters incoming events, converts them into a normalized representation, applies enrichments, and writes incremental updates."
- **배치 경로:** 스케줄 잡이 "read historical raw events, apply the same filter and enrichment definitions, and produce longer sequences."
- **저장·서빙:** "Sequence data is stored in a columnar layout so models can read exactly the fields they need" + 피처 이름으로 시퀀스를 조회하는 온라인 서빙 API
- **아키텍처 성격:** "This lambda-style architecture balances freshness (streaming updates) with completeness (batch corrections), eliminating the historical problem where training and serving systems diverged."

**책에서의 활용:** 이 하나의 사례가 **§3-3(배치 vs 스트리밍), §3-4(Lambda), §1-12(학습-서빙 스큐)를 전부 관통한다.** 챕터 하나의 앵커 사례로 쓸 만하다. 특히 "one definition, many runtimes"는 Lambda의 고질병(로직 이중 구현)에 대한 구체적 해법이라 인용 가치가 높다.

#### 쿠팡 — 데이터 플랫폼 진화 4단계

`[https://medium.com/coupang-engineering/big-data-platform-evolving-from-start-up-to-big-tech-company-26f9fcb9c13 | 2022-08-03 | 저자: Narendra Parihar, 정재화, 김중훈 | 검색 시점 2026-07-25]`

> ⚠️ **2022년 글 — 현행 아키텍처와 다를 수 있음.** "진화 서사"로만 인용할 것.

- **Phase I (2010–2013):** 관계형 DB, 소규모 데이터 사이언스 팀
- **Phase II (2014–2016):** Hadoop + MPP 도입. 폭증하는 데이터 대응. **피크 시간대 병목 발생**
- **Phase III (2016–2017):** 클라우드 전면 이전, 20배 성장 대응. 로깅 프레임워크 개선 + 데이터 웨어하우스 클러스터 분리
- **Phase IV (2019–):** 서비스 기반 모델 — 클러스터 라이프사이클 관리, 스케줄 오토스케일링, 사전 빌드 머신 이미지, 모니터링

원문 인용:
> "쿠팡은 데이터 중심 회사입니다. 고객의 상품 구매 프로세스 내 단계 모두 데이터에 기반해 설계합니다."

**책에서의 활용:** **"처음부터 이 스택을 다 짓지 않는다"**는 메시지의 근거. 개발자 독자가 이 책의 스택 지도(§0)를 보고 압도되지 않게 하려면, "쿠팡도 관계형 DB에서 시작했다"는 사실이 필요하다. **책 초반이나 마무리 챕터의 안심 장치로 배치할 것.**

#### 확인 실패 / 미조회

- **Netflix 실시간 분산 그래프 (Part 1)** — `https://netflixtechblog.com/how-and-why-netflix-built-a-real-time-distributed-graph-part-1-...`는 Medium 글로벌 아이덴티티로 **307 리다이렉트**되어 본문 조회 실패. 검색 결과에서 제목과 "Oct, 2025" 표기를 봤으나 **본문·발행일 확정 불가 — 확인 불가 (미조회)**.
- **카카오 데이터정보플랫폼팀 글** — 검색 결과에 URL이 나왔으나 본문 미조회. **확인 불가 (미조회)**.
- **당근·토스 쇼핑 추천** — 검색 결과에 URL 확인, 본문 미조회. **확인 불가 (미조회)**.
- **Uber RAMEN, Netflix Kafka/Flink 상세** — 검색 요약에만 등장. **1차 출처 미조회 — 인용 금지.**

---

## 4. 상충·불확실 항목

1. **GitHub Releases 날짜의 연도 누락 (전 항목에 걸친 구조적 문제 — 해결됨)**
   - 관찰: GitHub 릴리스 목록도, 개별 태그 페이지도 연도를 출력하지 않았다(`YEAR NOT ON PAGE` × 3: Iceberg 1.11.0, Pinot 1.5.1, Druid 37.0.0).
   - **반례로 확인된 사실:** Snowplow 최상단 항목 `22.01 Western Ghats – 31 Jan`은 **2022년 1월**인데도 연도 없이 렌더링됐다. 따라서 "연도 없음 = 당해 연도"는 **틀린 추론**이다.
   - **해결:** Iceberg·Pinot·Druid는 Apache 배포 아카이브(전체 타임스탬프)로 연도를 확정했다(각각 2026-05-19 / 2026-06-30 / 2026-05-06).
   - **미해결 잔여:** ClickHouse·Redis·Feast·rudder-server는 Apache 프로젝트가 아니라 아카이브 대체 경로가 없었다. 이들은 **릴리스 주기(2~6주)로 보아 2026이 압도적으로 유력**하지만 `연도 추정 — 확정 아님`이다. 다행히 이 넷은 본문에서 특정 일자를 주장하지 않는다.

2. **Iceberg·Pinot의 GitHub 날짜 vs Apache 아카이브 날짜**
   - 상충: Iceberg — GitHub `20 May` / 아카이브 `2026-05-19` (하루 차)
   - 상충: Pinot — GitHub `05 Jun` / 아카이브 `2026-06-30` (약 25일 차)
   - **원인 추정:** 릴리스 태그 생성 시점과 dist 업로드 시점의 차이. **판단하지 않고 병기한다.** 책에는 일자를 박지 말고 `2026-05`·`2026년 중반` 수준으로 쓸 것.
   - 추가 이상: Iceberg GitHub 목록에서 `1.10.2 — 18 May`가 `1.10.1 — 22 Dec`보다 위에 있다 — **목록 순서를 시간순으로 해석하면 안 된다.**

3. **Snowplow의 "오픈소스" 지위**
   - 상충: 일반적 통념·다수 블로그는 Snowplow를 "오픈소스 이벤트 파이프라인"으로 소개 / 공식 라이선스 FAQ는 핵심 컴포넌트가 SLULA(비프로덕션·비상업 한정) 아래 있음을 명시.
   - **판단: 공식 문서가 이긴다.** 책에서 Snowplow를 "오픈소스"로 무조건 분류하면 안 된다. **이 사실 자체가 개발자 독자에게 유용한 정보이므로 본문에서 다룰 것.**

4. **RudderStack의 오픈소스 라이선스**
   - 문서 사이트가 리다이렉트 후 내비게이션만 반환해 확인 실패. **확인 불가.** "오픈소스 CDP"라는 통상적 서술을 그대로 쓰지 말고 저술 시 재확인.

5. **Redis 라이선스**
   - GitHub Releases 페이지에 라이선스 정보 없음. **확인 불가.** 최근 몇 년 라이선스 변동이 있었던 영역이므로 단정 서술 금지.

6. **Druid vs Pinot의 자리**
   - 두 프로젝트 문서가 서로 겹치는 영역을 주장한다. 이 문서는 Pinot을 "user-facing 저지연·고동시성" 쪽으로, Druid를 "시계열·롤업" 쪽으로 정리했으나 **이건 조회된 Pinot 문서 + 일반 통념에 근거한 정리**이며 Druid 측 문서를 조회한 결과가 아니다. **Druid 특성 서술은 확인 불가 (미조회).**

7. **ClickHouse 버전 라인**
   - `v26.7.1.1315-stable`(22 Jul)이 `v26.5.6.64-stable`(23 Jul)보다 버전은 높은데 릴리스는 하루 빠르다. **여러 라인이 병행 패치되는 구조**이므로 "최신 = 가장 높은 버전"이 아니다. 책에 "최신 버전은 X"라고 쓰면 거의 확실히 틀린다. **"26.x 계열 / 2026 기준"으로 서술할 것.**

8. **ClickBench의 중립성**
   - 제3자 벤치마크처럼 인용되는 경우가 많으나, **운영 주체가 ClickHouse**다. 인용 시 반드시 병기. 방법론 문서는 미조회.

---

## 5. 확인 불가 목록 (미조회 / 조회 실패)

### 조회 시도했으나 실패
| 항목 | URL | 실패 사유 |
|---|---|---|
| Kafka 다운로드/설계 문서 | `kafka.apache.org/downloads`, `/documentation/#design`, `/43/documentation.html#design` | 내비게이션 셸만 반환 (단일 거대 HTML + 앵커 구조) |
| Kafka GitHub Releases | `github.com/apache/kafka/releases` | "There aren't any releases here" — Apache Kafka는 GH Releases 미사용 |
| Iceberg 릴리스·스펙 (공식 사이트) | `iceberg.apache.org/releases/`, `/spec/` | 내비게이션 메뉴만 반환 (raw GitHub md로 우회 성공) |
| Pinot 아키텍처 (1차 시도) | `docs.pinot.apache.org/basics/architecture` | 404 (안내된 `.md` 경로로 재조회 성공) |
| RudderStack 오픈소스 라이선스 | `docs.rudderstack.com/rudderstack-open-source/` → `rudderstack.com/docs/...` | 리다이렉트 후 내비게이션만 반환 |
| Netflix 실시간 분산 그래프 | `netflixtechblog.com/how-and-why-netflix-built-...` | Medium 글로벌 아이덴티티로 307 리다이렉트 |
| ClickBench 방법론 | `benchmark.clickhouse.com/` | 방법론·시스템 목록·공정성 서술이 페이지 본문에 미포함 |

### 의도적으로 조회하지 않음 (예산 배분 결정)
- **Tier 2 전 항목의 버전·수치** — Redpanda, Pulsar, Jitsu, OpenTelemetry, Spark Structured Streaming, Kafka Streams, Materialize, Arroyo, StarRocks, Delta Lake, Hudi, Parquet, Snowflake·BigQuery·Redshift, Airflow, Dagster, Airbyte, Cassandra/ScyllaDB, Aerospike, RocksDB, pgvector/Qdrant/Milvus
- **근사 자료구조 원 논문 본문** — Bloom(1970), Count-Min Sketch, t-digest. Redis 공식 문서가 링크는 제시하나 논문 본문은 미조회. (논문 축은 paper-researcher 담당)
- **dbt 머티리얼라이제이션·ref()·테스트 상세 페이지**
- **Feast 오프라인 스토어·레지스트리·물질화 상세**
- **DuckDB 스토리지 포맷·개별 확장(Iceberg/httpfs) 세부** (`why_duckdb`의 아키텍처 개요는 §1-11에 조회 완료)
- **Snowplow Iglu / self-describing JSON 스펙**
- **Pinot 인덱스 종류·업서트 상세**
- **Confluent Schema Registry 문서**
- **Lambda/Kappa 원전** (Nathan Marz / Jay Kreps)

### 전혀 근거를 확보하지 못한 주제 (별도 리서치 필요)
- **이탈 예측 / send-time optimization / LLM 카피 생성 / text-to-SQL 자연어 세그먼트** — 어느 제품이 실제로 무엇을 쓰는지 공개 1차 문서 미확보
- **Uber RAMEN, Netflix Kafka/Flink 파이프라인 세부** — 검색 요약에만 등장, 1차 출처 미조회
- **카카오·당근의 CDP/세그먼트 아키텍처** — URL은 확인, 본문 미조회
- **벤더 CDP 제품(Segment, Braze, Amplitude 등)의 내부 아키텍처** — 이 축의 담당 범위 밖

---

## 신선도 원장

> **연도 표기 규칙:** `연도 미표기(2026 추정)`는 GitHub Releases 목록에서 연도가 출력되지 않은 항목이다. GitHub는 당해 연도에 연도를 생략하므로 2026으로 추정했으나 **확정 근거는 아니다.** `페이지 표기`는 페이지에 연도까지 명시된 것으로 **확정 근거**다.

| 소스 | URL | 발행일 또는 "{버전}/{연도} 기준" | 검색 시점 | 관련 항목 |
|---|---|---|---|---|
| Apache Kafka 아카이브 | archive.apache.org/dist/kafka/ | **4.3.1 / 2026-06-23 22:22 (페이지 표기·확정)**, 4.3.0 / 2026-05-20 | 2026-07-25 | §1-1 |
| Confluent Kafka Consumer Design | docs.confluent.io/kafka/design/consumer-design.html | 발행일 확인 불가 | 2026-07-25 | §1-1 |
| Kafka KIP-98 (Exactly Once) | cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging | 발행일 확인 불가 | 2026-07-25 | §1-1 |
| ClickHouse GitHub Releases | github.com/ClickHouse/ClickHouse/releases | **26.x 계열 / 2026 기준** (v26.7.1.1315-stable — 22 Jul, v26.3.17.56-lts — 20 Jul, v25.8.28.1-lts — 05 Jul). 연도 미표기(2026 추정) | 2026-07-25 | §1-2 |
| ClickHouse MergeTree 문서 | clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree | 발행일 확인 불가 | 2026-07-25 | §1-2 |
| ClickHouse uniqCombined | clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqcombined | 발행일 확인 불가 | 2026-07-25 | §1-2, §3-1 |
| ClickHouse uniqExact | clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqexact | 발행일 확인 불가 | 2026-07-25 | §1-2, §3-1 |
| ClickBench | benchmark.clickhouse.com | 발행일 확인 불가 / **운영 주체: ClickHouse (중립 아님)** | 2026-07-25 | §1-2 |
| Apache Flink 다운로드 | flink.apache.org/downloads/ | **2.3.0 / 2026-06-25 (페이지 표기·확정)**, 1.20.5 LTS / 2026-06-03 | 2026-07-25 | §1-3 |
| Flink 시간 개념 문서 | nightlies.apache.org/flink/flink-docs-release-2.0/docs/concepts/time/ | 발행일 확인 불가 (2.0 문서 브랜치) | 2026-07-25 | §1-3 |
| **Iceberg Apache 아카이브** | archive.apache.org/dist/iceberg/ | **1.11.0 / 2026-05-19 04:43 (전체 타임스탬프·확정)** | 2026-07-25 | §1-4 |
| Iceberg GitHub Releases | github.com/apache/iceberg/releases | `20 May` — **연도 미표기**, 태그 페이지도 YEAR NOT ON PAGE. 아카이브와 하루 차이 | 2026-07-25 | §1-4, §4 |
| Iceberg 스펙 (raw md) | raw.githubusercontent.com/apache/iceberg/main/format/spec.md | main 브랜치 시점, 발행일 확인 불가 | 2026-07-25 | §1-4, §3-5 |
| Snowplow Fundamentals | docs.snowplow.io/docs/fundamentals/ | 발행일 확인 불가 | 2026-07-25 | §1-5, §3-5 |
| Snowplow SLULA FAQ | docs.snowplow.io/docs/licensing/limited-use-license-faq/ | **SLULA v1.0 / 2024년 1월, v1.1 / 2024년 12월 (문서 표기)** | 2026-07-25 | §1-5, §4 |
| Snowplow GitHub Releases (모노레포) | github.com/snowplow/snowplow/releases | 최신 `22.01 Western Ghats — 31 Jan` — **비활성 릴리스 라인, 현행 버전 확인 불가** | 2026-07-25 | §1-5 |
| RudderStack 문서 | rudderstack.com/docs/ | 발행일 확인 불가 | 2026-07-25 | §1-6 |
| rudder-server GitHub Releases | github.com/rudderlabs/rudder-server/releases | **v1.81.1 / 2026 기준** (22 Jul, 연도 미표기 — 2026 추정) | 2026-07-25 | §1-6 |
| dbt-core GitHub Releases | github.com/dbt-labs/dbt-core/releases | **1.12.0 / 2026-07-16 (페이지 표기·확정)**, 2.0.0-alpha.5 / 2026-07-20 | 2026-07-25 | §1-7 |
| dbt 모델 문서 | docs.getdbt.com/docs/build/models | 발행일 확인 불가 | 2026-07-25 | §1-7 |
| Redis GitHub Releases | github.com/redis/redis/releases | **8.8.1 / 2026 기준** (23 Jul, 연도 미표기 — 2026 추정), 8.10-RC2 (pre-release) | 2026-07-25 | §1-8 |
| Redis HyperLogLog 문서 | redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ | 발행일 확인 불가 / **0.81% 표준오차·12KB — 문서 명시** | 2026-07-25 | §1-8, §3-1 |
| Redis Bloom filter 문서 | redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/ | 발행일 확인 불가 / **비트/항목 수치 문서 명시** | 2026-07-25 | §3-1 |
| Redis Count-Min Sketch 문서 | redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/ | 발행일 확인 불가 | 2026-07-25 | §3-1 |
| Redis t-digest 문서 | redis.io/docs/latest/develop/data-types/probabilistic/t-digest/ | 발행일 확인 불가 | 2026-07-25 | §3-1 |
| **Pinot Apache 아카이브** | archive.apache.org/dist/pinot/ | **1.5.1 / 2026-06-30 22:18 (전체 타임스탬프·확정)**, 1.5.0 / 2026-05-01 | 2026-07-25 | §1-9 |
| Pinot GitHub Releases | github.com/apache/pinot/releases | `05 Jun` — **연도 미표기**, 태그 페이지도 YEAR NOT ON PAGE. **아카이브와 일자 불일치** | 2026-07-25 | §1-9, §4 |
| Pinot 아키텍처 문서 | docs.pinot.apache.org/architecture-and-concepts/concepts/architecture.md | 발행일 확인 불가 / **10ms P95·100K QPS는 프로젝트 자체 표방** | 2026-07-25 | §1-9 |
| **Druid Apache 아카이브** | archive.apache.org/dist/druid/ | **37.0.0 / 2026-05-06 04:19 (전체 타임스탬프·확정)**, 36.0.0 / 2026-05-01, 35.0.0 / 2025-11-05 | 2026-07-25 | §2 |
| Druid GitHub Releases | github.com/apache/druid/releases | `08 May` — **연도 미표기**, 태그 페이지도 YEAR NOT ON PAGE | 2026-07-25 | §2 |
| Trino 릴리스 노트 | trino.io/docs/current/release.html | **483 / 2026-07-17 (페이지 표기·확정)** | 2026-07-25 | §1-10 |
| Trino Use Cases | trino.io/docs/current/overview/use-cases.html | 발행일 확인 불가 | 2026-07-25 | §1-10 |
| DuckDB News | duckdb.org/news/ | **1.5.5 / 2026-07-22 (페이지 표기·확정)**, 1.4.5 LTS / 2026-06-17 | 2026-07-25 | §1-11 |
| DuckDB — Why DuckDB | duckdb.org/why_duckdb | 발행일 확인 불가 | 2026-07-25 | §1-11 |
| Feast GitHub Releases | github.com/feast-dev/feast/releases | **0.65.0 / 2026 기준** (20 Jul, 연도 미표기 — 2026 추정). Aerospike·ScyllaDB 온라인 스토어 추가 | 2026-07-25 | §1-12, §3-2 |
| Feast 아키텍처 개요 | docs.feast.dev/getting-started/architecture/overview | 발행일 확인 불가 | 2026-07-25 | §1-12 |
| Feast Point-in-time joins | docs.feast.dev/getting-started/concepts/point-in-time-joins | 발행일 확인 불가 | 2026-07-25 | §1-12 |
| 우아한형제들 — 카프카 활용 | techblog.woowahan.com/17386/ | **2024-05-30 (페이지 표기·확정)** / 저자 김나은 | 2026-07-25 | §3-7 |
| LINE — Kafka Streams | engineering.linecorp.com/ko/blog/applying-kafka-streams-for-internal-message-delivery-pipeline | **2016-08-18 (페이지 표기·확정)** / 저자 Kawamura Yuto / ⚠️ 구버전 | 2026-07-25 | §2, §3-7 |
| Pinterest — User Sequence | medium.com/pinterest-engineering/making-user-sequence-data-more-cost-efficient-faster-and-easier-to-use-2a56a928cae1 | **2026-05-21 (페이지 표기·확정)** | 2026-07-25 | §3-4, §3-7 |
| 쿠팡 — 데이터 플랫폼 진화 | medium.com/coupang-engineering/big-data-platform-evolving-from-start-up-to-big-tech-company-26f9fcb9c13 | **2022-08-03 (페이지 표기·확정)** / ⚠️ 구버전 | 2026-07-25 | §3-7 |
| 토스 — 광고 ML | toss.tech/article/ads-ml | **2025-04-21 (페이지 표기·확정)** / 저자 김영호 | 2026-07-25 | §3-6 |
| 토스 — Feature Store & Trainkit | toss.tech/article/feature-store-trainkit | **2025-08-14 (페이지 표기·확정)** / 저자 우종호·송석현 | 2026-07-25 | §3-2, §3-6 |
| 토스 — TUES 세그먼테이션 | toss.tech/article/tues | **2026-06-16 (페이지 표기·확정)** / 저자 우찬희 | 2026-07-25 | §3-3, §3-6 |

---

## 참고문헌

### 공식 1차 소스 — 릴리스·버전 (실제 조회)
1. Apache Kafka Archive — https://archive.apache.org/dist/kafka/
1b. Apache Iceberg Archive (연도 확정용) — https://archive.apache.org/dist/iceberg/
1c. Apache Pinot Archive (연도 확정용) — https://archive.apache.org/dist/pinot/
1d. Apache Druid Archive (연도 확정용) — https://archive.apache.org/dist/druid/
2. ClickHouse Releases — https://github.com/ClickHouse/ClickHouse/releases
3. Apache Flink Downloads — https://flink.apache.org/downloads/
4. Apache Iceberg Releases — https://github.com/apache/iceberg/releases
5. Apache Pinot Releases — https://github.com/apache/pinot/releases
6. Apache Druid Releases — https://github.com/apache/druid/releases
7. Trino Release Notes — https://trino.io/docs/current/release.html
8. DuckDB News — https://duckdb.org/news/
9. dbt-core Releases — https://github.com/dbt-labs/dbt-core/releases
10. Redis Releases — https://github.com/redis/redis/releases
11. Feast Releases — https://github.com/feast-dev/feast/releases
12. rudder-server Releases — https://github.com/rudderlabs/rudder-server/releases
13. Snowplow Releases (비활성 라인) — https://github.com/snowplow/snowplow/releases

### 공식 1차 소스 — 개념·스펙 (실제 조회)
14. Apache Iceberg Table Spec — https://raw.githubusercontent.com/apache/iceberg/main/format/spec.md
15. Kafka KIP-98: Exactly Once Delivery and Transactional Messaging — https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging
16. Confluent — Kafka Consumer Design — https://docs.confluent.io/kafka/design/consumer-design.html
17. ClickHouse — MergeTree — https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
18. ClickHouse — uniqCombined — https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqcombined
19. ClickHouse — uniqExact — https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqexact
20. Flink — Timely Stream Processing — https://nightlies.apache.org/flink/flink-docs-release-2.0/docs/concepts/time/
21. Apache Pinot — Architecture — https://docs.pinot.apache.org/architecture-and-concepts/concepts/architecture.md
22. Trino — Use Cases — https://trino.io/docs/current/overview/use-cases.html
23. dbt — About dbt models — https://docs.getdbt.com/docs/build/models
24. Feast — Architecture Overview — https://docs.feast.dev/getting-started/architecture/overview
25. Feast — Point-in-time joins — https://docs.feast.dev/getting-started/concepts/point-in-time-joins
26. Snowplow — Fundamentals — https://docs.snowplow.io/docs/fundamentals/
27. Snowplow — Limited Use License FAQ — https://docs.snowplow.io/docs/licensing/limited-use-license-faq/
28. RudderStack — Documentation — https://www.rudderstack.com/docs/
29. Redis — HyperLogLog — https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/
30. Redis — Bloom filter — https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/
31. Redis — Count-min sketch — https://redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/
32. Redis — t-digest — https://redis.io/docs/latest/develop/data-types/probabilistic/t-digest/
33. ClickBench — https://benchmark.clickhouse.com/
33b. DuckDB — Why DuckDB — https://duckdb.org/why_duckdb

### 회사 엔지니어링 블로그 (실제 조회, 발행일 확인)
34. 우아한형제들 — 우리 팀은 카프카를 어떻게 사용하고 있을까 (2024-05-30, 김나은) — https://techblog.woowahan.com/17386/
35. LINE Engineering — 내부 데이터 파이프라인에 Kafka Streams 적용하기 (2016-08-18, Kawamura Yuto) — https://engineering.linecorp.com/ko/blog/applying-kafka-streams-for-internal-message-delivery-pipeline
36. Pinterest Engineering — Making User-Sequence Data More Cost-Efficient, Faster, and Easier to Use (2026-05-21) — https://medium.com/pinterest-engineering/making-user-sequence-data-more-cost-efficient-faster-and-easier-to-use-2a56a928cae1
37. 쿠팡 엔지니어링 — 데이터 플랫폼: 스타트업에서 이커머스 최강자까지의 진화 (2022-08-03) — https://medium.com/coupang-engineering/big-data-platform-evolving-from-start-up-to-big-tech-company-26f9fcb9c13
38. 토스 — 토스는 어떻게 광고를 보여줄까? 토스 애즈 ML 톺아보기 (2025-04-21, 김영호) — https://toss.tech/article/ads-ml
39. 토스 — 토스가 다양한 ML 모델을 만드는 법: Feature Store & Trainkit (2025-08-14, 우종호·송석현) — https://toss.tech/article/feature-store-trainkit
40. 토스 — 2,800만 MAU를 이해하는 유저 Segmentation, TUES (2026-06-16, 우찬희) — https://toss.tech/article/tues

### 검색으로 URL만 확인, 본문 미조회 (인용 금지)
- Netflix TechBlog — How and Why Netflix Built a Real-Time Distributed Graph, Part 1 (리다이렉트로 조회 실패)
- 토스 — 토스 쇼핑 추천 시스템: 멀티 스테이지 접근법 — https://toss.tech/article/35215
- 카카오 — 데이터 엔지니어링 관련 글 — https://tech.kakao.com/2022/06/16/data-engineering/
- OpenSnowcat (Snowplow의 Apache 2.0 포크) — 존재만 확인

---

## 수집 한계 (스킬 형식 준수)

- **접근 실패한 자료:** §5 표 참조 (Kafka 공식 문서, Iceberg 공식 사이트 스펙, RudderStack 라이선스 페이지, Netflix TechBlog, ClickBench 방법론).
- **의도적으로 제외한 소스 유형:**
  - 커뮤니티 여론(Reddit/HN/GeekNews) — community-researcher 담당
  - 학술 논문 본문 — paper-researcher 담당 (근사 자료구조 원 논문 링크는 §3-1에 소재만 남겨둠)
  - 프라이버시 규제·벤더 제품 비교 — 다른 축 담당
  - 날짜 없는 나열형 "Top 10 CDP tools" 류 아티클 — 신뢰성 하
- **Tier 2 미조회는 예산 배분 결정**이며 실패가 아니다. 대신 **모든 Tier 2 항목에 `버전 확인 불가` 표기**로 fact-checker가 오인용을 잡을 수 있게 했다.

<!-- ===== web_privacy.md ===== -->

<!-- 검색 시점: 2026-07-25 기준 -->
# 프라이버시·동의·아이덴티티·규제 리서치 (web #3)

검색 수행일: **2026-07-25**
담당 축: E-1 브라우저 정책 / E-2 서버사이드 태깅 / E-3 동의 관리 / E-4 아이덴티티 / E-5 클린룸 / E-6 규제 / E-7 코드에 남는 흔적
슬러그: `martech-for-developers` · 장르: `tech-book` · 대상 독자: 한국 개발자

> **작성 규율 (fact-checker 대조 기준)**
> - 이 문서의 모든 날짜·버전·조문 번호·정책 상태는 **2026-07-25에 실제로 fetch한 페이지**에서만 가져왔다.
> - fetch하지 못한 항목은 `확인 불가 (미조회)` 또는 `조문 원문 미확인`으로 명시했다.
> - 페이지 수집 도구가 요약 모델을 거치므로, **원문 그대로임이 확실한 문장만 따옴표로 인용**했고 나머지는 `요지:`로 표기했다. 챕터에 직접 인용할 때는 `요지:` 항목을 따옴표로 감싸지 마라.
> - **이 축은 2025~2026년에 여러 번 뒤집혔다.** 기억으로 쓰면 거의 틀린다. 아래 "기억과 달랐던 항목"을 먼저 읽어라.

---

## ⚠️ 먼저 읽을 것 — 2026-07-25 기준 "기억과 다른" 핵심 5가지

| # | 흔한 오해 (2024년까지의 상식) | 2026-07-25 기준 실제 |
|---|---|---|
| 1 | "Chrome이 서드파티 쿠키를 없앤다" | **폐지 계획 자체가 철회됐다.** 2025-04-22 Google이 "현재 방식 유지" 발표, 별도 프롬프트도 안 띄운다 |
| 2 | "Privacy Sandbox가 쿠키를 대체한다" | **Privacy Sandbox 광고 API 대부분이 폐기됐다.** 2025-10-17 Topics·Protected Audience·Attribution Reporting 등 은퇴 발표, Chrome 144(2026-01-13)에서 deprecate, M150에서 제거 예정 |
| 3 | "IAB TCF는 v2.2가 최신" | **v2.3.** 2026-03-01부터 `disclosedVendors` 세그먼트 없는 TC String은 무효 |
| 4 | "정보통신망법 스팸 위반은 과태료" | **2026-07-07 시행 개정법(법률 제21305호)으로 과징금 도입** — 매출액 6% 이하 |
| 5 | "EU AI Act는 2026-08-02에 전면 적용" | AI Omnibus로 일부 고위험 규정이 **2027-12-02 / 2028-08-02로 연기**됐다 |

---

## E-1. 서드파티 쿠키·브라우저 정책 현재 상태

### E-1-1. Chrome / Google — 두 번의 대반전

**변화 궤적 (이 책이 개발자에게 설명해야 하는 "왜 이렇게 됐나"):**

```
2020~2023  Privacy Sandbox 제안, 서드파티 쿠키 단계적 폐지 로드맵 발표
2024-01    Chrome 사용자 1%에 서드파티 쿠키 기본 차단 테스트 시작
   ↓
2025-04-22 반전 ①: "폐지 안 한다" — 현재 선택 방식 유지, 별도 프롬프트 없음
   ↓
2025-10-17 반전 ②: Privacy Sandbox 광고 API 대부분 은퇴 (같은 날 영국 CMA도 규제 약속 해제)
   ↓
2026-01-13 Chrome 144 stable — Protected Audience / Private Aggregation / Shared Storage deprecate
   ↓
2026-06-12 Topics API 사용률 4.9% of page loads (blink-dev 스레드 갱신)
   ↓
M150       제거 예정 (Topics, Protected Audience, Private Aggregation)
```

**① 서드파티 쿠키 폐지 철회 (2025-04-22)**
- 출처: <https://privacysandbox.google.com/blog/privacy-sandbox-next-steps> | 발행일 **2025-04-22** | 저자 Anthony Chavez (VP, Privacy Sandbox) | 검색 시점 2026-07-25
- 신뢰성: **최상** (Google 공식 1차 소스)
- 인용:
  > "not be rolling out a new standalone prompt for third-party cookies"
  > "made the decision to maintain our current approach to offering users third-party cookie choice in Chrome"
- 요지: 이유로 업계 이해관계자 간 견해차, 프라이버시 강화 기술 채택 가속, 전 세계 규제 환경 변화를 들었다. Privacy Sandbox API에 대해서는 "may have a different role to play in supporting the ecosystem"이라며 로드맵 재검토를 예고했다.
- **트라젝토리 주의:** 이 글은 "IP Protection을 2025년 3분기에 런칭하겠다"고 했으나, 아래 ②의 상태 페이지에서는 IP Protection이 **Discontinue (Do Not Launch)** 로 뒤집혔다. 6개월 만의 번복 — 이 축을 기억으로 쓰면 안 되는 이유의 교과서적 사례다.
- 관련 섹션: 챕터 오프닝 훅, "왜 서버사이드로 갔나"의 전제

**② Privacy Sandbox 기술 은퇴 (2025-10-17)**
- 출처: <https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies> | 발행일 **2025-10-17** | 저자 Anthony Chavez | 검색 시점 2026-07-25
- 신뢰성: **최상**
- 인용:
  > "After evaluating ecosystem feedback about their expected value and in light of their low levels of adoption, we've decided to retire the following Privacy Sandbox technologies."
  > "We've heard clearly from marketers and publishers the importance of scaled measurement solutions to understand the impact of advertising campaigns."
- **은퇴 목록 (원문 열거):** Attribution Reporting API, IP Protection, On-Device Personalization, Private Aggregation, Shared Storage, Protected Audience, Protected App Signals, Related Website Sets, SelectURL, SDK Runtime, Topics
- **계속 지원:** CHIPS, FedCM, Private State Tokens
- 관련 섹션: "표준 대체재가 사라진 뒤 남은 것" — 이게 서버사이드/퍼스트파티로의 압력을 오히려 키운 지점

**③ 기능별 현재 상태 (공식 status 페이지)**
- 출처: <https://privacysandbox.google.com/overview/status> | 페이지 최종 갱신 **2025-10-17** | 검색 시점 2026-07-25
- 신뢰성: **최상**
- ⚠️ **신선도 주의:** 이 status 페이지의 최종 갱신일은 2025-10-17이다. 2026년 갱신본은 **확인 불가 (미조회)**. 아래 M144/M150 마일스톤은 별도의 2026년 소스(Chrome 릴리스 노트·blink-dev)로 교차 확인했다.

| 구분 | 기능 |
|---|---|
| **계속 지원 (Continue to Support)** | CHIPS (Chrome 114+ 기본 지원), FedCM (Chrome 108 shipped), Fenced Frames (GA), Private State Tokens, Storage/Network State Partitioning, Storage Access API (Chrome 119+ 기본), User-Agent Client Hints, User-Agent Reduction, Bounce Tracking Mitigations |
| **폐기·제거 예정 (Deprecate and Remove)** | Aggregation Service, Attribution Reporting, Private Aggregation, **Protected Audience**, Related Website Sets, Shared Storage, **Topics** |
| **출시 안 함 (Discontinue / Do Not Launch)** | **IP Protection**, Partitioned Popins, Fenced Storage Read, Private Proofs, Probabilistic Reveal Tokens, Script Blocking |
| **Android** | Attribution Reporting, On-Device Personalization, Protected App Signals, Protected Audience, SDK Runtime, Topics — 전부 phaseout 예정 |

**④ 실제 제거 마일스톤 (2026년 소스)**
- 출처: <https://developer.chrome.com/release-notes/144> | Chrome 144 **stable 릴리스 2026-01-13** | 검색 시점 2026-07-25 | 신뢰성 **최상**
  - 요지: Chrome 144 릴리스 노트에 Private Aggregation API, Shared Storage API, Protected Audience API의 deprecation이 명시돼 있다. 세 API 모두 "서드파티 쿠키 현행 유지 발표에 따라 Chrome이 해당 API를 deprecate·remove할 계획"이라는 취지의 동일 문구를 쓴다. ⚠️ 이 문구는 수집 도구가 세 항목을 합쳐 재구성한 것이라 **원문 그대로가 아니다 — 따옴표로 인용하지 마라.** 직접 인용이 필요하면 릴리스 노트를 다시 열어라.
  - ⚠️ Topics, Attribution Reporting, Related Website Sets는 이 릴리스 노트의 deprecation 섹션에는 등장하지 않았다.
- 출처: <https://groups.google.com/a/chromium.org/g/blink-dev/c/_R85yctz4Rs> ("Intent to Deprecate and Remove: Topics API") | 최초 게시 **2025-11-08** | 저자 Yao Xiao | 검색 시점 2026-07-25 | 신뢰성 **최상** (Chromium 공식 프로세스)
  - "Deprecate in M144", "remove in M150"
  - 최초 제안 시점 사용률: "Currently, ~13% of page loads use Topics API"
  - **2026-06-12 갱신 사용률: "Currently the usage is 4.9% of page loads"** ← 2026년 dated 근거
- 출처: <https://groups.google.com/a/chromium.org/g/topics-api-announce/c/iQX7PC3S0Ds> (PSA) | 게시 **2025-12-05** | 저자 Sam Dutton | 신뢰성 **최상**
- **M150의 실제 stable 릴리스 날짜: 확인 불가 (미조회)** — chromiumdash.appspot.com/schedule은 JS 렌더링이라 본문 추출 실패. 챕터에 M150 날짜를 쓰지 마라.

**⑤ 영국 CMA의 규제 약속 해제 (2025-10-17)**
- 출처: <https://www.gov.uk/cma-cases/investigation-into-googles-privacy-sandbox-browser-changes> / 결정문 PDF <https://assets.publishing.service.gov.uk/media/68f213ce06e6515f7914c728/Decision_to_release_the_commitments_previously_accepted_by_the_CMA_in_respect_of_Google_s_Privacy_Sandbox_proposals.pdf> | 결정일 **2025-10-17** | 검색 시점 2026-07-25 | 신뢰성 **최상** (영국 정부 공식) — ⚠️ 결정문 PDF 본문은 미조회, 검색 결과 요약 기준
- 요지: CMA는 2022년 2월 Google의 Privacy Sandbox 관련 약속(commitments)을 수용했으나, Google이 서드파티 쿠키 제한 계획을 철회하면서 원래의 경쟁 우려가 더 이상 성립하지 않는다고 판단, 2025-10-17 약속을 해제했다.
- **개발자용 서사 포인트:** Privacy Sandbox는 "프라이버시 프로젝트"였던 동시에 "경쟁법 감시 대상"이었다. 규제가 풀린 날과 API가 죽은 날이 같은 날이다.
- 관련 섹션: "Martech은 왜 기술만으로 설명되지 않는가"

### E-1-2. Safari / WebKit — ITP

**① ITP 최초 도입 (2017)**
- 출처: <https://webkit.org/blog/7675/intelligent-tracking-prevention/> | 발행 **2017-06-05** | 저자 John Wilander | 신뢰성 **최상**
- 인용:
  > "Intelligent Tracking Prevention is a new WebKit feature that reduces cross-site tracking by further limiting cookies and other website data."
  > "A machine learning model is used to classify which top privately-controlled domains have the ability to track the user cross-site, based on the collected statistics."
- 분류기가 쓰는 세 가지 통계 벡터 (원문): "subresource under number of unique domains, sub frame under number of unique domains, and number of unique domains redirected to"
- 초기 시간 규칙 (원문 인용):
  > "If the user has not interacted with example.com in the last 30 days, example.com website data and cookies are immediately purged."
  > "If the user interacted with example.com the last 24 hours, its cookies will be available when example.com is a third-party."
  > "If the user interacted with example.com the last 30 days but not the last 24 hours, example.com gets to keep its cookies but they will be partitioned."
- ⚠️ **구버전 정보 주의:** 위 24시간/30일 규칙은 2017년 초기 설계다. 2020년 전면 차단으로 대체됐다(아래 ②). 챕터에서는 "초기에는 이랬다"는 역사 서술로만 써라.

**② 서드파티 쿠키 전면 차단 (2020)**
- 출처: <https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/> | 발행 **2020-03-24** | 저자 John Wilander | 신뢰성 **최상**
- 인용:
  > "Cookies for cross-site resources are now blocked by default across the board."
  > "Safari continues to pave the way for privacy on the web, this time as the first mainstream browser to fully block third-party cookies by default."
  > "ITP has aligned the remaining script-writable storage forms with the existing client-side cookie restriction, deleting all of a website's script-writable storage after seven days of Safari use without user interaction on the site."
- **7일 삭제 대상 스토리지:** IndexedDB, LocalStorage, Media keys, SessionStorage, Service Worker registrations and cache
- 요지: ITP 분류기는 계속 동작하며 bounce tracker, tracker collusion, link decoration tracking을 탐지한다. delayed bounce tracking 탐지 로직도 추가됐다.
- **개발자 함의:** `localStorage`에 넣은 익명 방문자 ID가 7일 뒤 사라진다. 이게 "왜 우리 재방문 식별률이 계속 떨어지나"의 기술적 정답이다.

**③ CNAME 클로킹 방어 (2020)**
- 출처: <https://webkit.org/blog/11338/cname-cloaking-and-bounce-tracking-defense/> | 발행 **2020-11-12** | 저자 John Wilander | 신뢰성 **최상**
- 인용:
  > "CNAME stands for canonical name record and maps one domain name to another as part of the Domain Name System, or DNS."
  > "ITP now detects third-party CNAME cloaking requests and caps the expiry of any cookies set in the HTTP response to 7 days."
- 요지: 사이트 소유자가 서브도메인을 서드파티 도메인으로 CNAME 매핑하면, 그 서드파티가 퍼스트파티와 같은 권한을 얻는다. WebKit은 연구에서 "1,762 websites CNAME cloaking 56 trackers in total"이 확인됐다고 밝혔고, 프라이버시뿐 아니라 보안 문제도 지적했다 — "250 websites of banks, healthcare companies, restaurant chains, and civil rights groups had been compromised" (CNAME 레코드 관리 부실).
- 탐지 조건 요지: 퍼스트파티 서브리소스의 CNAME이 퍼스트파티 도메인과도, top frame host의 CNAME과도 다를 때 적용된다.
- **이게 E-2 서버사이드 태깅의 CNAME 논쟁에 대한 브라우저 벤더의 공개 입장이다.** 서버사이드 태깅을 CNAME으로 구현하면 Safari에서 쿠키 수명이 7일로 잘린다.
- 관련 섹션: E-2와 반드시 교차 참조

### E-1-3. Firefox — Total Cookie Protection

- 출처: <https://blog.mozilla.org/en/products/firefox/firefox-rolls-out-total-cookie-protection-by-default-to-all-users-worldwide/> | 발행 **2022-06-14** (업데이트 2024-08-28) | 신뢰성 **최상**
- 인용:
  > "creating a separate 'cookie jar' for each website you visit"
  > "Any time a website, or third-party content embedded in a website, deposits a cookie in your browser, that cookie is confined to the cookie jar assigned to only that website."
- 요지: 2022년 6월 전 세계 Firefox 데스크톱 사용자에게 기본값으로 롤아웃됐다. 차단이 아니라 **파티셔닝**이다 — 쿠키를 없애는 게 아니라 사이트별 항아리에 가둬 크로스사이트 연결을 끊는다.
- ⚠️ `support.mozilla.org/en-US/kb/total-cookie-protection`은 로드 실패 — Firefox **버전 번호는 확인 불가 (미조회)**. 또한 위 발표는 **데스크톱** 기준이다. Android·iOS Firefox의 현재 기본값은 **확인 불가**. 챕터에서 "Firefox는 기본으로 파티셔닝한다"고 쓸 때 플랫폼을 한정하라.
- **개발자 함의:** Chrome의 CHIPS(`Partitioned` 쿠키 속성)와 같은 방향. "서드파티 쿠키가 있냐 없냐"가 아니라 "파티션 키가 뭐냐"로 문제가 옮겨갔다.

### E-1-4. Apple — ATT / SKAdNetwork / AdAttributionKit

**① App Tracking Transparency**
- 출처: <https://developer.apple.com/app-store/user-privacy-and-data-use/> | 신뢰성 **최상** | 발행일 표기 없음 (상시 갱신 정책 페이지) | 검색 시점 2026-07-25
- **Apple의 "tracking" 정의 (원문 인용) — 이 정의가 챕터의 핵심 인용이다:**
  > "Tracking refers to the act of linking user or device data collected from your app with user or device data collected from other companies' apps, websites, or offline properties for targeted advertising or advertising measurement purposes. Tracking also refers to sharing user or device data with data brokers."
- tracking 예시 (원문 인용):
  > "Placing a third-party SDK in your app that combines user data from your app with user data from other developers' apps to target advertising or measure advertising efficiency, even if you don't use the SDK for these purposes."
- 요구사항 (원문 인용):
  > "In iOS 14.5, iPadOS 14.5, and tvOS 14.5 or later, you need to receive the user's permission through the AppTrackingTransparency (ATT) framework in order to track them or access their device's advertising identifier."
  > "Unless you receive permission from the user to enable tracking, the device's advertising identifier value will be all zeros and you may not track them as described above."
- **개발자 함의:** 거부 시 IDFA가 `00000000-0000-0000-0000-000000000000`. null이 아니라 **0으로 채워진 유효한 형태의 UUID**다. 이걸 그대로 ID 그래프에 넣으면 전 세계 거부 사용자가 한 사람으로 병합된다 — E-4의 over-merge 사례로 그대로 쓸 수 있다.

**② ATT 프레임워크 API**
- 출처: <https://developer.apple.com/documentation/apptrackingtransparency> (JSON: `/tutorials/data/documentation/apptrackingtransparency.json`) | 신뢰성 **최상** | 검색 시점 2026-07-25
- 인용:
  > "Request user authorization to access app-related data for tracking the user or the device."
  > "You must use the AppTrackingTransparency framework if your app collects data about end users and shares it with other companies for purposes of tracking across apps and web sites."
- API: `requestTrackingAuthorization(completionHandler:)`, `trackingAuthorizationStatus`
- Info.plist 키: `NSUserTrackingUsageDescription` — "A message that informs the user why an app is requesting permission to use data for tracking the user or the device."
- 플랫폼 가용성 (공식 표): iOS 14.0 / iPadOS 14.0 / Mac Catalyst 14.0 / macOS 11.0 / tvOS 14.0 / visionOS 1.0

**③ SKAdNetwork ↔ AdAttributionKit**
- ⚠️ **정밀도 낮음.** `developer.apple.com/documentation/adattributionkit/adattributionkit-skadnetwork-interoperability` 본문 추출 실패 (SPA). 아래는 developer.apple.com 도메인 한정 검색 결과 요약 수준이다.
- 요지 (신뢰성 **중** — 원문 미확인): AdAttributionKit은 SKAdNetwork를 대체(deprecate)하는 게 아니라 그 위에 얹혀 상호운용된다. SKAdNetwork에 이미 등록된 광고 네트워크는 별도 등록이 필요 없다고 안내된다. AdAttributionKit은 WWDC24에서 소개됐다(<https://developer.apple.com/videos/play/wwdc2024/10060/>).
- **챕터에 SKAdNetwork의 deprecation 여부·버전 번호·conversion value 비트 수를 쓰지 마라. 전부 확인 불가 (미조회).**

### E-1-5. 이 변화가 만든 기술적 귀결 — ⚠️ 오독 금지

Privacy Sandbox가 죽었다고 **서드파티 쿠키가 정상으로 돌아온 게 아니다.** 2026-07-25 기준 실제 상태:

- Safari: 서드파티 쿠키 **기본 전면 차단** (2020년부터, 변함 없음)
- Firefox: **사이트별 파티셔닝** 기본값 (2022년부터, 변함 없음)
- Chrome: 폐지는 안 하지만 **1% 테스트 그룹과 사용자 선택 UI는 유지**, CHIPS로 파티션 쿠키 표준화
- Privacy Sandbox: 표준화된 **대체 API가 사라졌다**

→ 결론: **문제는 그대로인데 표준 해법만 없어졌다.** 그래서 압력은 오히려 커졌다 — 퍼스트파티 데이터, 로그인 기반 식별, 서버사이드 수집, 벤더 종속적 클린룸으로. 이게 E-2~E-5가 존재하는 이유다.

---

## E-2. 서버사이드 태깅 / 수집 아키텍처

### E-2-1. Google Tag Manager 서버사이드

- 출처: <https://developers.google.com/tag-platform/tag-manager/server-side> | 신뢰성 **최상** | 발행일 표기 없음 | 검색 시점 2026-07-25
- 인용:
  > "Server-side tagging is a way to instrument your tags to measure user activity wherever it happens."
  > "Server containers use the same tag, trigger, and variable model that you're used to, while also providing new tools."
- 공식이 내세우는 세 가지 이점 (원문 항목): "Improve page performance", "Unlock more detailed user privacy controls", "Improve data quality"

- 출처: <https://developers.google.com/tag-platform/tag-manager/server-side/send-data> | 신뢰성 **최상**
- **client 정의 (원문 인용) — 서버사이드 태깅의 핵심 개념:**
  > "Clients are adapters between the software running on a user's device and your server-side Tag Manager container. They receive measurement data from a device, transform that data into one or more events, process the data in the container, and package the results to be sent back to the device."
- 퍼스트파티 도메인 관련 (원문 인용):
  > "To send data in a true first-party context, you need to serve Google scripts, such as the Google Analytics library, from your own servers."
- 전송 방식 요지: GA4 태그는 Image pixel, Fetch API, XHR, 그리고 서버 컨테이너 도메인에서 로드된 iframe 안에서 도는 Service Worker를 transport로 지원한다.

**개발자 관점 정리:**
- 브라우저 → **내 도메인**(태깅 서버) → Google/Meta/기타 벤더. 브라우저는 서드파티 도메인을 직접 안 본다.
- 그래서 광고 차단기의 도메인 블록리스트와 ITP의 서드파티 규칙을 우회한다 — 그리고 **바로 그 이유로 CNAME 클로킹 논쟁이 붙었다**(E-1-3 참조).

### E-2-2. Meta Conversions API

- 출처: <https://developers.facebook.com/docs/marketing-api/conversions-api> | 신뢰성 **최상** | 검색 시점 2026-07-25
- 인용:
  > "designed to create a connection between an advertiser's marketing data...from an advertiser's server, website platform, mobile app, or CRM to Meta systems"
- 요지: 서버 이벤트는 Meta Pixel이나 iOS/Android SDK로 보낸 이벤트와 "processed like events sent using the Meta Pixel"이라고 명시된다.
- ⚠️ **정직한 표기:** 이 공식 문서 페이지에는 "광고 차단기 때문에 만들었다"는 문장이 **없다**. 브라우저 제약을 CAPI의 존재 이유로 쓸 때는 Meta 공식 진술이 아니라 업계 통설로 표기하라. (`(사실 확인 필요)` 마커 대상)

### E-2-3. 중복 제거 (dedup) — 개발자가 실제로 짜는 부분

- 출처: <https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events> | 신뢰성 **최상** | 검색 시점 2026-07-25
- **권장 방식 (원문 인용):**
  > "We determine if events are identical based on their **ID** and **name**. So, for an event to be deduplicated:
  > 1. In corresponding events, a Meta Pixel's `eventID` must match the Conversion API's `event_id`.
  > 2. In corresponding events, a Meta Pixel's `event` must match the Conversion API's `event_name`."
- **폴백 방식 (원문 인용):**
  > "If you have configured the `external_id` and/or `fbp` parameters to be passed via both browser and server, we take care to remove duplicate events automatically."
- **시간 창 (원문 인용) — 이 48시간이 챕터에 쓸 구체 수치다:**
  > "If we find the same server key combination (`event_id` and `event_name`) **and** browser key combination (`eventID` and `event`) sent to the same Pixel ID within 48 hours, we discard the subsequent events."
  > "events are only deduplicated if they are received within 48 hours of when we receive the first event with a given `event_id`"

**챕터에 쓸 개발자 서사:**
> 브라우저에서도 보내고 서버에서도 보낸다. 둘 다 보내는 이유는 브라우저 쪽이 30~40% 잘려나가기 때문이고, 둘 다 보내면 같은 구매가 두 번 카운트된다. 그래서 주문 ID 같은 걸로 `event_id`를 만들어 양쪽에 똑같이 실어 보낸다 — 이게 martech 백엔드 개발자가 입사 첫 주에 만나는 코드다. 48시간 창을 넘기는 지연 배치 잡을 짜면 중복이 그대로 통과한다.

**어떤 걸 브라우저에서, 어떤 걸 서버에서 보내나 (설계 원칙 정리 — 출처 없는 저자 정리로 표기할 것):**
- 브라우저만 아는 것: 페이지 URL, referrer, 클릭 ID(`fbclid`/`gclid`), 브라우저 쿠키(`_fbp`), 화면·UA
- 서버만 아는 것: 확정된 주문 금액, 결제 성공 여부, 환불, 로그인 사용자 ID, 오프라인 전환
- 양쪽에 필요한 것: `event_id` (dedup 키), 동의 상태

### E-2-4. 상충 지점 — 서버사이드 태깅의 "프라이버시 강화" 주장

- Google 공식 문서는 서버사이드 태깅의 이점으로 "Unlock more detailed user privacy controls"를 든다.
- WebKit은 CNAME 클로킹을 **추적 회피 수법**으로 규정하고 쿠키 수명을 7일로 캡한다.
- **두 입장은 정면으로 충돌한다. 병기하고 결론 내지 마라.** 챕터에서는 "같은 아키텍처가 벤더 문서에서는 프라이버시 강화로, 브라우저 벤더 블로그에서는 회피 수법으로 불린다"는 긴장 자체를 보여주는 게 정직하다.

---

## E-3. 동의 관리 (CMP)

### E-3-1. IAB Europe TCF — 현재 v2.3

- 출처: <https://iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/> | 발행 **2025-06-19** | 신뢰성 **최상** (IAB Europe 공식)
- **현재 버전: v2.3** (기억이 흔히 "v2.2"라고 답하는 지점)
- 핵심 변경 요지: 벤더가 Special Purposes와 Legitimate Interest 기반 Purposes를 동시에 선언할 때, LI 비트가 0이면 "공개 안 함"인지 "사용자가 거부함"인지 구분이 안 되는 모호성이 있었다. v2.3은 **`disclosedVendors` 세그먼트를 필수화**해 이 모호성을 해소한다.
- **날짜 (원문 인용):**
  > "Starting 1st March, 2026: Any TC String created without the disclosedVendor segment will be deemed invalid."
  - 전환 기간 종료: **2026-02-28**. 이후 생성된 `disclosedVendors` 없는 TC String은 무효.
- v2.2 배경 (출처: <https://iabeurope.eu/tcf/>, <https://iabeurope.eu/tcf-2-2-launches-all-you-need-to-know/> | 신뢰성 최상 | 발행 2023):
  - v2.2 출시일 **2023-05-16**. 벨기에 DPA가 검증한 Action Plan을 반영한 개정.
  - 요지: Purpose 3·4·5·6(개인화 광고/콘텐츠 프로필 생성·이용)에 대해 **Legitimate Interest를 법적 근거로 선택할 수 없게** 하고 consent만 허용. 법률 용어를 사용자 친화적 설명 + 실사용 예시로 교체. 벤더는 수집 데이터 범주·보유 기간·정당한 이익을 추가 공개. CMP는 첫 화면에 법적 근거를 구하는 **벤더 총수**를 표시. "모두 동의" 원클릭 버튼이 있으면 재방문 시 **"모두 철회" 원클릭**도 동등하게 제공해야 함.
- 관련 섹션: "동의는 UI가 아니라 프로토콜이다" — TC String이라는 인코딩된 문자열이 광고 요청에 실려 다닌다는 걸 개발자에게 보여주는 대목

### E-3-2. Google Consent Mode

- 출처: <https://developers.google.com/tag-platform/security/concepts/consent-mode> | 신뢰성 **최상** | 검색 시점 2026-07-25
- ⚠️ **버전 표기 주의:** 이 공식 개요 문서는 파라미터를 나열할 뿐 "v2"라는 버전 라벨을 문서 제목에서 쓰지 않는다. 챕터에서 "Consent Mode v2"라고 쓸 거면 "2023년 11월에 `ad_user_data`·`ad_personalization` 두 파라미터가 추가된 개정"이라는 사실 기준으로 쓰는 게 안전하다.
- **파라미터 전체 (공식 문서 원문 정의):**

| 파라미터 | 원문 정의 |
|---|---|
| `ad_storage` | "Enables storage, such as cookies (web) or device identifiers (apps), related to advertising." |
| `ad_user_data` | "Sets consent for sending user data to Google for online advertising purposes." |
| `ad_personalization` | "Sets consent for personalized advertising." |
| `analytics_storage` | "Enables storage, such as cookies (web) or device identifiers (apps), related to analytics, for example, visit duration." |
| `functionality_storage` | "Enables storage that supports the functionality of the website or app, for example, language settings" |
| `personalization_storage` | "Enables storage related to personalization, for example, video recommendations" |
| `security_storage` | "Enables storage related to security such as authentication functionality, fraud prevention, and other user protection" |

- 추가 신호: `ads_data_redaction` — 요지: 사용자가 동의를 거부했을 때 저장된 광고 데이터를 삭제하도록 하는 설정
- **Basic vs Advanced (원문 인용) — 개발자가 실제로 고르는 갈림길:**
  - Basic: "Prevent Google tags from loading until a user interacts with a consent banner", "no data transferred to Google prior to user interaction" → "general model (less detailed modeling)"
  - Advanced: "Google tags load when a user opens the website or app", 동의 전에도 기본 동의 설정 하에서 "measurements without cookies"를 전송 → "advertiser-specific model (more detailed modeling)"
- **챕터 포인트:** Advanced 모드는 "동의 안 했는데도 뭔가 보낸다"이고, 그 대가로 더 정교한 전환 모델링을 받는다. 이 트레이드오프를 개발자가 코드 한 줄로 정하게 되는 게 martech의 특징적 긴장이다. (EEA 트래픽에 대한 EU user consent policy 요구사항은 <https://support.google.com/tagmanager/answer/13695607> — ⚠️ 본문 미조회)

### E-3-3. Global Privacy Control (GPC)

- 출처: <https://www.w3.org/TR/gpc/> | **Working Draft, 발행일 2026-06-11** | 신뢰성 **최상** (W3C 공식) | 검색 시점 2026-07-25
- **상태: W3C Working Draft** (Recommendation 아님). 2024년 11월 W3C Privacy Working Group의 공식 work item으로 채택돼 표준화 진행 중. (work item 채택 시점은 검색 결과 기반 — 신뢰성 중)
- **HTTP 헤더 (원문 인용):**
  > "The `Sec-GPC` header field is a mechanism for expressing a person's general universal preference for a do-not-sell-or-share interaction in HTTP requests (for any request method)."
  ```
  Sec-GPC-field-name  = "Sec-GPC"
  Sec-GPC-field-value = "1"
  ```
- **DOM 프로퍼티 (원문 인용):**
  > "The `globalPrivacyControl` property enables a client-side script to determine what `Sec-GPC` header field value was sent when loading the top-level browsing context's active document."
  - `Navigator`와 `WorkerNavigator` 양쪽에 readonly boolean으로 노출.
- **개발자 함의:** DNT(Do Not Track)와 달리 GPC는 **법적 구속력이 있다** — 캘리포니아에서는 반드시 존중해야 한다(E-6-5). 즉 `req.headers['sec-gpc'] === '1'` 한 줄이 법적 의미를 갖는 첫 헤더다. 챕터에서 DNT의 실패와 대비시키면 좋다.

### E-3-4. 개발자가 실제로 구현하는 것 (저자 정리 — 출처 없음, 사실 주장 아님)

- 동의 신호를 **어디까지 전파해야 하나**: 브라우저 태그 → 서버 컨테이너 → 이벤트 스트림 → 웨어하우스 → 다운스트림 활성화(광고 플랫폼 오디언스 싱크). 한 곳이라도 빠지면 "동의 철회했는데 광고가 계속 따라온다"가 된다.
- **동의 철회 시 이미 수집된 데이터**: 스트림(Kafka 등)에 이미 흘러간 이벤트, 웨어하우스 파티션, 벤더 쪽에 이미 싱크된 오디언스, 백업 스냅샷 — 네 군데를 다 처리해야 한다. E-7에서 이어감.
- ⚠️ 위 두 항목은 이 리서치에서 **1차 출처로 확인한 사실이 아니다.** 챕터에서 수치나 단정 없이 설계 서술로만 쓰라.

---

## E-4. 아이덴티티 레졸루션 / ID 그래프

### E-4-1. 결정적 vs 확률적 매칭

- 출처: <https://liveramp.com/uk/blog/probabilistic-vs-deterministic-matching>, <https://docs.liveramp.com/connect/en/deterministic-matching.html>, <https://segment.com/blog/identity-resolution/> | 신뢰성 **중~최상** (벤더 공식 문서 + 벤더 블로그) | ⚠️ **본문 미조회 — 검색 결과 요약 기준. 아래 문구를 따옴표로 인용하지 마라.**
- **결정적(deterministic) 요지:** 이미 알고 있는 식별자(이메일, 전화번호, 디바이스 ID, 사용자 ID)의 일치로 병합한다. 관측된 데이터에 근거하므로 "이 사용자가 그걸 했다"를 확신할 수 있다. 정밀도(precision)가 높다.
- **확률적(probabilistic) 요지:** 예측 알고리즘으로 "아마 같은 사람일 것"을 추정한다. 디바이스 핑거프린팅, IP 매칭, 화면 해상도, OS, 위치, Wi-Fi 네트워크, 행동·브라우징 데이터를 통계 모델에 넣어 일정 신뢰수준에서 묶는다. 정밀도는 낮지만 결정적 데이터가 없을 때 **커버리지(scale)**를 얻는다.
- **한 줄 대비 (저자 정리 — 인용 아님):** 결정적은 *이 사용자가 그걸 했다*(관측·확실), 확률적은 *이 사용자가 그걸 할 것이다*(추정·신뢰구간).
- **개발자 번역 (저자 정리):** 결정적 매칭은 조인 키가 있는 `JOIN`이고, 확률적 매칭은 유사도 임계값이 있는 `fuzzy match`다. 후자는 임계값 하나 잘못 잡으면 서로 다른 사람이 한 프로필로 합쳐진다.

### E-4-2. ID 그래프 자료구조 관점 (저자 정리 — 1차 출처 없음)

⚠️ 아래는 이번 리서치에서 벤더 문서로 확인한 내용이 **아니다.** 개발자 독자를 위한 설계 서술로만 쓰고, 수치나 "업계 표준" 같은 단정은 붙이지 마라.

- ID 그래프는 노드(식별자: 쿠키 ID, 디바이스 ID, 이메일 해시, 로그인 ID, 전화번호)와 엣지(관측된 동시 등장)로 이루어진 그래프다. 프로필 하나 = 연결 컴포넌트 하나.
- 병합은 사실상 **union-find(disjoint set)**다. 새 관측이 들어오면 두 컴포넌트를 union한다.
- **union은 되돌리기 어렵다** — 이게 실무 위험의 핵심이다. 잘못 합쳐진 두 사람을 다시 떼려면 병합 이력 전체를 재생(replay)해야 한다. 그래서 성숙한 시스템은 병합 결과가 아니라 **관측 이벤트 원장**을 진실의 원천으로 두고 그래프를 파생물로 재계산한다.
- **오병합(over-merge)의 대표 트리거:**
  - 공용 기기 (가족 태블릿, 매장 키오스크, 사무실 공용 PC)
  - 널·플레이스홀더 식별자 — ATT 거부 시의 all-zero IDFA(E-1-4), `null` 문자열, `test@example.com`
  - 이메일 별칭·역할 계정 (`info@`, `noreply@`)
  - 기기 초기화 후 광고 ID 재발급
- **미병합(under-merge)의 대표 트리거:** 익명 세션에서 장바구니에 담고 로그인 후 결제 — 로그인 순간 익명 프로필과 회원 프로필을 잇지 못하면 "첫 구매 고객"으로 잘못 분류된다.
- **익명 → 로그인 전환 시 프로필 병합**이 martech 개발자가 가장 자주 만나는 실전 문제다. 로그인 콜백에서 익명 ID와 회원 ID를 alias 이벤트로 묶고, 그 전에 쌓인 이벤트를 소급 재귀속(backfill)할지 말지를 정해야 한다.

### E-4-3. 대체 식별자 — UID2

- 출처: <https://unifiedid.com/docs/intro> | **문서 최종 갱신 2026-07-23** (검색 시점 이틀 전 — 매우 신선) | 신뢰성 **최상** (프로젝트 공식 문서)
- 인용:
  > "UID2 is a framework that enables deterministic identity for advertising opportunities on the open internet"
- 요지: 웹사이트·모바일 앱·CTV를 아우르며, 인증된 통합 경로(certified integration paths)로 토큰을 관리·교환한다. 프로젝트는 활발히 유지되고 있고 다수의 통합 가이드·SDK·엔드포인트가 제공된다.
- 라이선스 (원문 인용): "All work and artifacts are licensed under the Apache License, Version 2.0"
- ⚠️ **미확인 항목 — 챕터에 쓰지 마라:** raw UID2가 이메일/전화번호에서 어떻게 파생되는지(해싱·솔팅 절차), 토큰의 정의와 회전 주기, RampID의 현재 상태. 전부 **확인 불가 (미조회)**. `unifiedid.com/docs/intro`의 개요 섹션에는 해당 설명이 없었다.
- **이메일 해시(SHA-256)의 현재 상태: 확인 불가 (미조회).** 챕터에서 "SHA-256 이메일 해시가 업계 표준 식별자다"라고 단정하지 마라. 다만 UID2가 스스로를 "deterministic identity" 프레임워크로 규정한다는 사실은 인용 가능하다.
- **개발자용 논점 (저자 정리):** 이메일을 SHA-256으로 해싱해도 그건 익명화가 아니라 **가명화**다. 같은 이메일은 항상 같은 해시가 되므로 여전히 조인 키다. 이 구분이 E-6의 가명정보 논의와 바로 연결된다.

---

## E-5. 데이터 클린룸

### E-5-1. AWS Clean Rooms — 가장 상세하게 문서화된 1차 소스

- 출처: <https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html> | 신뢰성 **최상** | 발행일 표기 없음 (상시 갱신 문서) | 검색 시점 2026-07-25
- **정의 (원문 인용):**
  > "AWS Clean Rooms helps you and your partners analyze and collaborate on your collective datasets to gain new insights without revealing underlying data to one another."
  > "When you run queries or jobs, AWS Clean Rooms reads data from that data's original location and applies built-in analysis rules to help you maintain control over that data."
- **내장 통제 수단 (원문 목록 인용):**
  > - "Analysis rules to restrict SQL queries and provide output constraints."
  > - "Cryptographic Computing for Clean Rooms to keep data encrypted, even as queries are processed, to comply with stringent data handling policies."
  > - "Analysis logs to review queries and jobs in AWS Clean Rooms and help support audits."
  > - "Differential privacy to protect against user-identification attempts. AWS Clean Rooms Differential Privacy is a fully-managed capability that protects the privacy of your users with mathematically-backed techniques and intuitive controls that you can apply in a few steps."
  > - "AWS Clean Rooms ML to allow two parties to identify similar users in their data without the need to share their data with each other."
- **동작 방식 (원문 인용) — 개발자가 이해할 워크플로:**
  > "In AWS Clean Rooms, you create a collaboration and add the AWS accounts that you want to invite, or create a membership to join a collaboration that you've been invited to. You then link the data resources needed for your use case: configured tables for event data, configured dataset associations for ML training and inference data, configured models for ML modeling, or ID namespaces for entity resolution. You have the option to create or approve analysis templates to agree in advance on the exact queries and jobs that you want to allow in a collaboration."
- **주목:** "ID namespaces for entity resolution" — 클린룸과 아이덴티티 레졸루션(E-4)이 같은 제품 안에서 만난다. AWS Entity Resolution과의 연동도 명시돼 있다.
- **PSI(Private Set Intersection): 이 문서에는 명시되지 않았다.** 대신 "Cryptographic Computing for Clean Rooms"라는 이름으로 암호화 상태 질의를 제공한다. 챕터에서 AWS Clean Rooms가 PSI를 쓴다고 쓰지 마라 — `확인 불가 (미조회)`.

### E-5-2. Google Ads Data Hub — 유일하게 구체 임계값이 공개된 소스

- 출처: <https://developers.google.com/ads-data-hub/guides/intro>, <https://developers.google.com/ads-data-hub/guides/privacy-checks> | 신뢰성 **최상** | 검색 시점 2026-07-25
- 정의 (원문 인용):
  > "Ads Data Hub enables customized analysis that aligns with your specific business objectives, while protecting user privacy and upholding Google's high standards of data security."
  > "Ads Data Hub ensures end-user privacy by enforcing privacy checks and aggregating Google data before it leaves the Google-owned Google Cloud project."
- 결과 저장: "Results from the queries you run using Ads Data Hub are written to BigQuery datasets in a Google Cloud project that you own."
- **프라이버시 메커니즘 (원문 인용):** "static checks, data access budgets, aggregation checks, difference checks, and noise injection to enforce privacy"
- **구체 임계값 (원문 인용) — 이 숫자들이 챕터의 핵심 팩트다:**
  > "Noise injection requires approximately 20 unique users per result row. Difference checks require approximately 50 unique users per result row. Queries of only click and conversion data require approximately 10 unique users per result row."
- 부가 (원문 인용):
  > "Rows omitted from results due to privacy restrictions" → filtered rows
  > "events with zeroed or null user IDs don't count toward the aggregation threshold"
  > "don't attempt to disaggregate data to disambiguate sets of users that don't meet our aggregation requirements"
- data access budget 소진 경고 메시지 타입: `DATA_ACCESS_BUDGET_IS_NEARLY_EXHAUSTED`
- **개발자 서사:** "SQL은 쓸 수 있는데 `SELECT`가 20명 미만이면 행이 그냥 사라진다." 쿼리 결과가 조용히 비어 있는 걸 디버깅하는 게 클린룸 엔지니어링의 일상이다. 그리고 `events with zeroed or null user IDs don't count` — E-1-4의 all-zero IDFA가 여기서 다시 등장한다.

### E-5-3. Amazon Marketing Cloud

- 출처: <https://advertising.amazon.com/solutions/products/amazon-marketing-cloud> | 신뢰성 **최상** (Amazon 공식 제품 페이지) | 발행일 표기 없음 | 검색 시점 2026-07-25
- 인용:
  > "Amazon Marketing Cloud (AMC) is a secure, privacy-safe, and cloud-based clean room solution in which advertisers can easily perform analytics and build audiences across pseudonymized signals"
  > "AMC only accepts pseudonymized information"
  > "You can only access aggregated, anonymous outputs from AMC."
  > "with built-in aggregation thresholds ensuring user privacy"
- 요지: "Built on AWS Clean Rooms"라고 명시된다.
- ⚠️ **AMC의 구체적 집계 임계값 수치는 이 페이지에 없다. 확인 불가 (미조회).** Ads Data Hub의 20/50/10 숫자를 AMC에 전용하지 마라.

### E-5-4. Snowflake Data Clean Rooms

- 출처: <https://docs.snowflake.com/en/user-guide/cleanrooms/introduction> | 신뢰성 **최상** | 검색 시점 2026-07-25
- 요지: collaboration이 resources(data offerings, templates, code specs)를 담고, "All resources, and the collaboration itself, are defined by YAML specifications."
- **데이터를 복사하지 않는 방식 (원문 인용):**
  > "A live view of the source data, not a snapshot, and its specification controls which columns are exposed and what policies apply."
- 명시된 프라이버시 통제: **differential privacy**만 이 개요 페이지에서 확인됨.
- ⚠️ 집계 임계값, join policy, projection policy는 이 개요 페이지에 **명시되지 않았다 — 확인 불가 (미조회)**.

### E-5-5. 기술 기반 정리 (교차 확인 결과)

| 기법 | 공식 문서에서 명시적으로 확인된 곳 |
|---|---|
| **차등 프라이버시 (Differential Privacy)** | AWS Clean Rooms ✅ (원문 인용 확보), Snowflake ✅ |
| **집계 임계값 (aggregation threshold)** | Ads Data Hub ✅ (20/50/10 명시), AMC ✅ (수치 없이 존재만 명시) |
| **노이즈 주입 (noise injection)** | Ads Data Hub ✅ |
| **difference check** | Ads Data Hub ✅ |
| **암호화 상태 연산** | AWS Clean Rooms ✅ ("Cryptographic Computing for Clean Rooms") |
| **PSI (Private Set Intersection)** | ❌ **어느 벤더 공식 문서에서도 그 이름으로 확인하지 못했다 — 확인 불가 (미조회)** |
| **k-anonymity** | ❌ **어느 벤더 공식 문서에서도 그 용어를 확인하지 못했다.** "집계 임계값"과 k-익명성을 등치시켜 쓰려면 저자 해석임을 명시하라 |

⚠️ **fact-checker 주의:** 클린룸을 설명할 때 "PSI와 k-익명성을 쓴다"는 문장은 이번 리서치에서 **1차 출처로 뒷받침되지 않는다.** 학술 개념으로 소개하는 건 가능하나, 특정 벤더 제품이 그걸 쓴다고 쓰지 마라.

---

## E-6. 규제 (한국 / EU / 미국)

### E-6-1. 한국 개인정보 보호법 [조문 확인 여부: **부분 확인**]

**법령 메타 (law.go.kr 원문 확인 ✅)**
- 출처: <https://www.law.go.kr/LSW/lsInfoP.do?lsId=011357&ancYnChk=0> | 신뢰성 **최상** (법제처 국가법령정보센터) | 검색 시점 2026-07-25
- **시행일: 2025. 10. 2.**
- **법률 제20897호, 2025. 4. 1., 일부개정**

**조문 원문 확인 ✅ (law.go.kr에서 실제로 본문을 읽은 조문)**

| 조 | 제목 | 확인된 내용 |
|---|---|---|
| **제15조** | 개인정보의 수집ㆍ이용 | "개인정보처리자는 다음 각 호의 어느 하나에 해당하는 경우에는 개인정보를 수집할 수 있으며 그 수집 목적의 범위에서 이용할 수 있다." — 각 호 요지: 정보주체 동의 / 법률상 특별 규정·법령상 의무 / 공공기관 소관 업무 / 계약 이행·계약 체결 전 요청 조치 / 급박한 생명·신체·재산 이익 / 개인정보처리자의 정당한 이익 / 공중위생 등 공공의 안전 |
| **제16조** | 개인정보의 수집 제한 | "개인정보처리자는 그 목적에 필요한 최소한의 개인정보를 수집하여야 한다." + 최소 수집이라는 입증책임은 개인정보처리자가 부담 |
| **제24조** | 고유식별정보의 처리 제한 | "개인정보처리자는 다음 각 호의 경우를 제외하고는 고유식별정보를 처리할 수 없다." — 정보주체의 **별도 동의** 또는 법령의 명시적 요구 |
| **제30조** | 개인정보 처리방침의 수립 및 공개 | 제1항 각 호(아래 별도 인용), 제2항 공개 의무, 제3항 "개인정보 처리방침의 내용과 개인정보처리자와 정보주체 간에 체결한 계약의 내용이 다른 경우에는 정보주체에게 유리한 것을 적용한다.", 제4항 보호위원회 작성지침 |
| **제37조의2** | 자동화된 결정에 대한 정보주체의 권리 등 | 아래 별도 인용 |
| **제75조** | 과태료 | 아래 별도 인용 |

**제30조 제1항 각 호 (law.go.kr 원문 인용) — 개인정보 처리방침에 반드시 들어가는 것:**
> 1. 개인정보의 처리 목적
> 2. 개인정보의 처리 및 보유 기간
> 3. 개인정보의 제3자 제공에 관한 사항(해당되는 경우에만 정한다)
> 3의2. 개인정보의 파기절차 및 파기방법
> 3의3. 민감정보의 공개 가능성 및 비공개를 선택하는 방법(해당되는 경우에만 정한다)
> 4. 개인정보처리의 위탁에 관한 사항(해당되는 경우에만 정한다)
> 4의2. 가명정보의 처리 등에 관한 사항(해당되는 경우에만 정한다)
> 5. 정보주체와 법정대리인의 권리·의무 및 그 행사방법에 관한 사항
> 6. 개인정보 보호책임자의 성명 또는 연락처
> 7. 인터넷 접속정보파일 등 자동수집 장치에 관한 사항(해당하는 경우에만 정한다)
> 8. 그 밖에 대통령령으로 정한 사항

- **개발자 함의:** 7호 "인터넷 접속정보파일 등 자동수집 장치" — **쿠키·픽셀·SDK가 법령 문언에 직접 등장하는 지점**이다. 태그 하나 붙일 때마다 처리방침을 고쳐야 하는 법적 근거가 여기다.

**제37조의2(자동화된 결정에 대한 정보주체의 권리 등) — law.go.kr 원문 확인 ✅**
- 출처: <https://law.go.kr/LSW/lsLinkCommonInfo.do?ancYnChk=&chrClsCd=010202&lsJoLnkSeq=1029334889> | 신뢰성 **최상**
- 제1항 요지: 정보주체는 "완전히 자동화된 시스템으로 개인정보를 처리하여 이루어지는 결정"이 자신의 권리에 중대한 영향을 미치는 경우 **그 결정을 거부**할 수 있다.
- 제2항 (원문 인용): "정보주체는 개인정보처리자가 자동화된 결정을 한 경우에는 그 결정에 대하여 설명 등을 요구할 수 있다."
- 제3항 요지: 개인정보처리자는 정당한 사유가 없는 한 자동화된 결정을 적용하지 않거나 "인적 개입에 의한 재처리ㆍ설명 등 필요한 조치"를 해야 한다.
- 제4항 (원문 인용): "개인정보처리자는 자동화된 결정의 기준과 절차, 개인정보가 처리되는 방식 등을 정보주체가 쉽게 확인할 수 있도록 공개하여야 한다."
- **시행일: ⚠️ 검색 결과는 2024-03-15 시행이라고 나오나, law.go.kr 원문의 부칙으로 확인하지 못했다 — `조문 원문 미확인 (시행일)`.** 챕터에 시행일을 쓰려면 별도 확인 필요.
- **개발자 함의 — 이게 martech에 걸리는 지점:** 추천 알고리즘, 자동 등급 산정, 알고리즘 기반 가격 차등, 자동 심사 거절. 제4항의 "기준과 절차, 처리 방식 공개" 의무는 곧 **모델 카드/설명 문서를 제품 안에 넣으라는 요구**다.

**개인정보 보호법 시행령 제17조(동의를 받는 방법) — law.go.kr 원문 확인 ✅**
- 출처: <https://www.law.go.kr/LSW/lsLawLinkInfo.do?lsJoLnkSeq=1000572094&chrClsCd=010202> | 신뢰성 **최상**
- ⚠️ **주의: 이건 법률 제17조가 아니라 시행령 제17조다. 혼동하지 마라.**
- 제1항 각 호 (원문 인용) — 동의가 유효하려면 **네 조건을 모두** 충족해야 한다:
  > 1. 정보주체가 자유로운 의사에 따라 동의 여부를 결정할 수 있을 것
  > 2. 동의를 받으려는 내용이 구체적이고 명확할 것
  > 3. 그 내용을 쉽게 읽고 이해할 수 있는 문구를 사용할 것
  > 4. 동의 여부를 명확하게 표시할 수 있는 방법을 정보주체에게 제공할 것
- **개발자 함의:** 이 네 조건이 **다크 패턴 금지의 법적 근거**다. "동의" 버튼만 크게 하고 "거부"를 흐리게 하면 1호·4호 위반이다. CMP UI 구현은 디자인 문제가 아니라 컴플라이언스 문제다.

**제75조(과태료) — law.go.kr 원문 확인 ✅**
- 출처: <https://law.go.kr/LSW/lsLinkCommonInfo.do?ancYnChk=&chrClsCd=010202&lsJoLnkSeq=1020398445> | 신뢰성 **최상**
- 과태료 구간 (원문 확인): **제1항 5천만원 이하** (고정형/이동형 영상정보처리기기 위반) / **제2항 3천만원 이하** (27개 호) / **제3항 2천만원 이하** (국내대리인 지정 관련 4개 호) / **제4항 1천만원 이하** (자료 제출·동의·정책 공개 관련 12개 호)
- 제5항 (원문 인용): "제1항부터 제4항까지에 따른 과태료는 대통령령으로 정하는 바에 따라 보호위원회가 부과ㆍ징수한다"
- **제2항 각 호 중 martech 직결 항목 (원문 인용) — 이 한 줄이 동의 UX 설계를 규정한다:**
  > "제16조제3항ㆍ제22조제5항을 위반하여 재화 또는 서비스의 제공을 거부한 자"
  - 요지: **선택적 동의를 거부했다는 이유로 서비스 제공을 거부하면 과태료 대상**이다. 즉 "마케팅 수신 동의 안 하면 가입 불가"는 위법이다. 이건 CMP·회원가입 폼 구현에 직접 걸린다.
  - ⚠️ 제16조 제3항과 제22조 제5항의 **조문 원문 자체는 미확인**. 제75조 제2항에서 그 존재와 취지만 확인했다.

**개인정보 보호법 시행령 제31조(개인정보 처리방침의 내용 및 공개방법 등) — law.go.kr 원문 확인 ✅**
- 출처: <https://www.law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=900079801&chrClsCd=010202> | 신뢰성 **최상**
- 제1항 각 호 (원문 인용) — 법 제30조 제1항 8호의 "대통령령으로 정한 사항":
  > 1. 처리하는 개인정보의 항목
  > 2. 법 제28조의8제1항 각 호에 따라 개인정보를 국외로 이전하는 경우 국외 이전의 근거와 같은 조 제2항 각 호의 사항
  > 3. 제30조에 따른 개인정보의 안전성 확보 조치에 관한 사항
  > 4. 국외에서 국내 정보주체의 개인정보를 직접 수집하여 처리하는 경우 개인정보를 처리하는 국가명
- **여기서 얻는 두 가지:**
  1. **제28조의8이 국외 이전 조문임을 법령 원문(시행령 인용)으로 간접 확인했다.** 다만 제28조의8 본문 자체는 여전히 미확인.
  2. **4호는 역외 적용이다** — 해외 서비스가 한국 정보주체의 개인정보를 직접 수집하면 처리 국가명을 처리방침에 밝혀야 한다. Martech SaaS를 해외에서 쓰는 한국 기업, 또는 한국 사용자를 받는 해외 서비스 양쪽에 걸린다.
- 제2항 (원문 인용): "개인정보처리자는 법 제30조제2항에 따라 수립하거나 변경한 개인정보 처리방침을 개인정보처리자의 인터넷 홈페이지에 지속적으로 게재하여야 한다."
- 제3항 요지: 홈페이지 게재가 불가능하면 사업장 게시 / 관보·신문·인터넷신문 게재 / 연 2회 이상 발행 간행물 게재 / 계약서 등에 실어 발급 — 넷 중 하나 이상.

**조문 원문 미확인 항목 (⚠️ 챕터에 조문 번호를 쓰기 전 반드시 재확인)**

아래는 law.go.kr 본문을 열지 못해 **조문 원문 미확인**이다. 검색 결과·2차 자료에서 나온 내용이며, 조문 번호가 맞는지 별도 검증이 필요하다.

| 추정 조 | 주제 | 확인 수준 | 비고 |
|---|---|---|---|
| 제17조 | 개인정보의 제공 (제3자 제공) | 조문 원문 미확인 | 검색 요지: 제3자 제공 시 고지 후 동의, 고지 사항 변경 시 재동의 |
| 제22조 | 동의를 받는 방법 | 조문 원문 미확인 | 검색 요지: 동의 사항을 구분해 명확히 인지하도록 알리고 각각 동의를 받아야 함 |
| 제28조의2~제28조의7 | 가명정보 처리 특례 (제3절) | 조문 원문 미확인 | 검색 요지: 제28조의2 통계작성·과학적 연구·공익적 기록보존 목적 시 **동의 없이** 가명정보 처리 가능 / 제28조의3 서로 다른 처리자 간 가명정보 결합은 보호위원회 지정 **전문기관**이 수행 / 제28조의4 추가정보 분리 보관 등 안전조치 / 제28조의5 특정 개인 식별 목적 처리 금지. 2020-02-04 개정 도입 |
| 제28조의8, 제28조의9 | 개인정보의 국외 이전 / 국외 이전 중지 명령 | 조문 원문 미확인 (조문 번호는 **시행령 제31조 제1항 2호 인용으로 간접 확인 ✅**) | 검색 요지: 원칙적으로 국외 이전 금지, 예외로 ① 정보주체의 **별도 동의** ② 법률·조약·국제협정의 특별 규정 ③ 계약 체결·이행에 필요한 처리위탁·보관으로서 일정 요건 충족. 개정으로 보호위원회가 **본법과 실질적으로 동등한 수준**의 보호를 한다고 인정한 국가·국제기구로의 이전이 추가됨. 위반 시 국외 이전 중지 명령 |
| 제35조 / 제36조 / 제37조 | 열람 / 정정·삭제 / 처리정지 | 조문 원문 미확인 | 조문 번호 자체를 확인하지 못했다 |
| 제35조의2 | 개인정보 전송요구권 (마이데이터) | 조문 원문 미확인 | 검색 요지: 2025-03-13 시행, 에너지정보는 2026-06-01까지 유예. 시행령이 전송자를 보건의료·통신·에너지 정보전송자로 구분 |
| 제64조의2 | 과징금의 부과 | 조문 원문 미확인 | 검색 요지: **전체 매출액의 3% 이하**, 매출액 산정이 곤란하면 **20억원 이하**. 위반행위와 무관한 매출은 제외. ⚠️ "중대 위반 시 10%" 언급도 별개 검색에서 나왔으나 상충 — 아래 상충 섹션 참조. **과태료(제75조)와는 별개의 제재다** |

**PIPC 공식 안내서 (2026년 최신 목록 — pipc.go.kr 확인 ✅)**
- 출처: <https://www.pipc.go.kr/np/cop/bbs/selectBoardList.do?bbsId=BS217&mCode=D010030000> | 신뢰성 **최상** (개인정보보호위원회 공식) | 검색 시점 2026-07-25

| 안내서 | 발행 |
|---|---|
| **개인정보 전송요구권 제도 안내서 (전 분야 마이데이터)** | **2026-06-25** ← 가장 최신, martech 직결 |
| 개인정보 처리방침 작성지침 | 2026-04 |
| **가명정보 처리 가이드라인** | **2026-03** ← martech 직결 |
| 개인정보 처리방침 표준(안) | 2026-02 |
| 보건의료데이터 활용 가이드라인 | 2025-12 |
| 개인정보 질의응답 모음집 | 2025-12 |
| 개인정보의 안전성 확보조치 기준 안내서 | 2025-11 |
| 개인정보 영향평가 수행안내서 | 2025-10 |
| 생성형 인공지능(AI) 개발·활용을 위한 개인정보 처리 안내서 | 2025-08 |
| 개인정보 안내서 전체 목록 | 2025-08-19 |

- ⚠️ **"온라인 맞춤형 광고" 또는 "행태정보" 라는 제목의 독립 안내서는 이 목록에서 확인되지 않았다.** 과거에 그런 가이드라인이 있었다고 기억하더라도, 2026-07-25 기준 PIPC 안내서 목록에서는 확인 불가다. 챕터에서 언급하려면 별도 확인 필요.
- ⚠️ 위 안내서들의 **본문은 미조회**. 제목과 발행 시점만 확인했다.

### E-6-2. 정보통신망법 — 영리목적 광고성 정보 전송 [조문 확인 여부: **원문 확인 ✅**]

**법령 메타 (law.go.kr 원문 확인 ✅)**
- 출처: <https://www.law.go.kr/LSW/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000688185&lsId=000030&print=print> | 신뢰성 **최상** (법제처) | 검색 시점 2026-07-25
- **시행일: 2026. 7. 7.** ← 검색 시점 기준 **18일 전 시행된 따끈한 개정법**
- **법률 제21305호, 2026. 1. 6., 일부개정**

**제50조(영리목적의 광고성 정보 전송 제한) — law.go.kr 원문 인용 ✅**

> **제1항** "누구든지 전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려면 그 수신자의 명시적인 사전 동의를 받아야 한다."

> **제2항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 제1항에도 불구하고 수신자가 수신거부의사를 표시하거나 사전 동의를 철회한 경우에는 영리목적의 광고성 정보를 전송하여서는 아니 된다."

> **제3항 (야간 시간대 제한 — 단서 포함 전문, law.go.kr 원문 확인 ✅)** "오후 9시부터 그 다음 날 오전 8시까지의 시간에 전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 제1항에도 불구하고 그 수신자로부터 별도의 사전 동의를 받아야 한다. **다만, 대통령령으로 정하는 매체의 경우에는 그러하지 아니하다.**"

> **제4항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하는 자는 대통령령으로 정하는 바에 따라 다음 각 호의 사항 등을 광고성 정보에 구체적으로 밝혀야 한다. 1. 전송자의 명칭 및 연락처 2. 수신의 거부 또는 수신동의의 철회 의사표시를 쉽게 할 수 있는 조치"

> **제5항 (요지)** 수신거부 회피·방해 조치, 자동 번호생성, 기망을 통한 수신동의 취득 등 금지 행위 열거

> **제6항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하는 자는 수신자가 수신거부나 수신동의의 철회를 할 때 발생하는 전화요금 등의 금전적 비용을 수신자가 부담하지 아니하도록 대통령령으로 정하는 바에 따라 필요한 조치를 하여야 한다."

> **제7항** "전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 수신자가 제1항 및 제3항에 따른 수신동의, 제2항에 따른 수신거부 또는 수신동의 철회에 관한 의사를 표시할 때에는 해당 수신자에게 대통령령으로 정하는 바에 따라 처리 결과를 알려야 한다."

> **제8항** "제1항 또는 제3항에 따라 수신동의를 받은 자는 대통령령으로 정하는 바에 따라 정기적으로 광고성 정보 수신자의 수신동의 여부를 확인하여야 한다."

**야간 시간대: 오후 9시 ~ 다음 날 오전 8시 — law.go.kr 원문으로 확인했다. ✅** (**11시간 창**)

⚠️ **단서를 빼먹지 마라 — 이게 개발자에게 결정적이다.**
제3항에는 "다만, 대통령령으로 정하는 매체의 경우에는 그러하지 아니하다"는 단서가 **있다**(원문 확인 ✅). 즉 **모든 채널에 11시간 창이 똑같이 적용되는 게 아니다.**
- **어느 매체가 면제되는지는 시행령 원문으로 확인하지 못했다 — `시행령 원문 미확인`.** (`lspttninfSeq=81509` 시도했으나 시행령 제62조의3만 반환)
- 2차 자료(신뢰성 **중**)는 면제 매체가 **전자우편**이라고 한다. 즉 문자·전화·팩스에는 야간 별도 동의가 필요하고 이메일에는 필요 없다는 취지.
- **챕터에서 "밤 9시 이후엔 아무것도 보내면 안 된다"고 쓰지 마라.** 푸시·문자·이메일을 한 규칙으로 묶지 말고, "채널마다 다르며 면제 매체는 시행령이 정한다"까지만 쓴 뒤 `(사실 확인 필요)`를 붙여라. 앱 푸시가 어디에 속하는지는 **확인 불가**.

**2026-07-07 시행 개정의 martech 관련 변경 (⚠️ 신뢰성 중 — 법무법인 뉴스레터·업계 매체 기준, law.go.kr 원문 미확인)**
- 출처: <https://www.bkl.co.kr/law/insight/newsletter/6642>, <https://www.lexology.com/library/detail.aspx?g=def8b7ab-62c2-4807-93aa-fad326ef4612> | 검색 시점 2026-07-25
- 요지 ①: **과징금 도입** — 제50조 등 광고성 정보 전송 규정 위반 시 시행령으로 정하는 **매출액의 6% 이하** 범위에서 과징금 부과 가능
- 요지 ②: **전송 위탁 제한** — 광고성 정보 전송을 위탁할 때는 전기통신사업법 제22조의11 제1항에 따라 방송미디어통신위원회의 **전송자격인증**을 받은 자에게만 위탁 가능
- ⚠️ **6% 수치와 위탁 조문 번호는 law.go.kr 원문으로 확인하지 못했다.** 챕터에 쓸 경우 `(사실 확인 필요)` 마커를 붙이고 fact-checker가 재확인하게 하라. **이 개정은 시행 18일차라 2차 자료 자체가 아직 얇다.**

**챕터에 쓸 개발자 서사:**
> 마케팅팀이 "오후 10시에 푸시 보내면 열람률이 두 배"라고 한다. 개발자는 그때 스케줄러에 시간을 넣는 사람이다. 정보통신망법 제50조 제3항은 오후 9시부터 다음 날 오전 8시까지 광고성 정보를 보내려면 **별도의 사전 동의**를 받으라고 한다. 일반 수신동의로는 안 되고, 야간 전송에 대한 동의를 따로 받아야 한다. 즉 동의 테이블에 컬럼이 하나가 아니라 둘이다.
> 그런데 같은 조항에 단서가 붙어 있다 — 대통령령이 정하는 매체는 예외다. 그래서 "밤 9시 이후 금지"는 채널마다 다르다. 스케줄러 하나에 시간 조건 하나를 박는 순간 틀린다. 채널별 정책 테이블이 필요하다. (어떤 매체가 면제인지는 시행령 소관 — 구현 전에 반드시 확인할 것)
> 그리고 제8항 — 정기적으로 수신동의 여부를 재확인해야 한다. 동의는 한 번 받고 끝나는 boolean이 아니라 **만료되는 상태**다.

### E-6-3. GDPR [조문 확인: **EUR-Lex 원문 기준 ✅, 다만 축약 인용**]

- 출처: <https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng> | 신뢰성 **최상** (EU 공식 관보) | 검색 시점 2026-07-25
- ⚠️ 수집 도구의 인용 길이 제한으로 조문 전문을 그대로 확보하지 못했다. 아래는 규정 자체의 문구를 조각으로 확인한 것이다. 챕터에서 긴 인용이 필요하면 EUR-Lex를 직접 다시 열어라.

**Article 6(1) — 처리의 적법 근거 6가지 (규정 문언 기준)**

| 근거 | 문언 |
|---|---|
| (a) 동의 | "the data subject has given consent to the processing of his or her personal data" |
| (b) 계약 | "processing is necessary for the performance of a contract to which the data subject is party" |
| (c) 법적 의무 | "processing is necessary for compliance with a legal obligation to which the controller is subject" |
| (d) 중대한 이익 | "processing is necessary in order to protect the vital interests of the data subject or of another natural person" |
| (e) 공익 임무 | "processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority" |
| (f) **정당한 이익** | "processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party" |

- **martech의 핵심 쟁점: (a) 동의 vs (f) 정당한 이익.** 광고 타겟팅을 정당한 이익으로 처리할 수 있느냐가 오랜 논쟁이고, IAB TCF v2.2가 Purpose 3·4·5·6에서 LI를 아예 뺀 것(E-3-1)이 그 논쟁의 실무적 결론이다. 이 두 사실을 챕터에서 연결하면 강한 대목이 된다.

**Article 22 — 자동화된 개별 의사결정 (프로파일링 포함)**
- 제1항 요지: 개인은 "a decision based solely on automated processing...which produces legal effects concerning him or her or similarly significantly affects him or her"의 대상이 되지 않을 권리를 갖는다.
- 제2항 예외 3가지 (문언 조각):
  1. "necessary for entering into, or performance of, a contract between the data subject and a controller"
  2. "authorised by Union or Member State law to which the controller is subject"
  3. "the data subject has given his or her explicit consent"
- **한국 개인정보 보호법 제37조의2와 대응 관계**다. 챕터에서 나란히 놓으면 "한국법이 GDPR을 어떻게 참조했나"가 보인다.

**정보주체 권리 조문 번호 (EUR-Lex 확인 ✅)**

| 권리 | 조 |
|---|---|
| 열람 (Right of access) | Article 15 |
| 삭제 (Right to erasure) | Article 17 |
| 처리 제한 (Right to restriction) | Article 18 |
| 데이터 이동권 (Data portability) | Article 20 |
| 반대권 (Right to object) | Article 21 |
| 국외 이전 | **Chapter V (Articles 44–50)** |

### E-6-4. CCPA / CPRA [조문 확인: **부분 — 캘리포니아 법무장관실 페이지 기준**]

- 출처: <https://oag.ca.gov/privacy/ccpa> | 신뢰성 **최상** (California Attorney General 공식) | 발행일 표기 없음 | 검색 시점 2026-07-25
- **"sharing" 정의 (원문 인용):**
  > "sharing for cross-context behavioral advertising, which is the targeting of advertising to a consumer based on the consumer's personal information obtained from the consumer's online activity across numerous websites"
- **opt-out 권리 (원문 인용):**
  > "may request that businesses stop selling or sharing your personal information"
  > businesses "cannot sell or share your personal information after they receive your opt-out request unless you later provide authorization allowing them to do so again"
- **GPC 존중 의무 (원문 인용) — 이게 개발자에게 중요한 문장이다:**
  > "Under law, it must be honored by covered businesses as a valid consumer request to stop the sale or sharing of personal information."
- 요지: 온라인 요청을 받는 사업자는 최소 두 가지 제출 방법을 제공해야 하며, 그중 하나로 "via a user-enabled global privacy control, like the GPC"가 인정된다.
- ⚠️ **"sale"의 법문 정의와 Civil Code 조문 번호(1798.120, 1798.135 등)는 이 페이지에서 확인하지 못했다 — `조문 원문 미확인`.** cppa.ca.gov 규정 페이지는 규칙제정 문서 링크만 있고 조문 전문이 없었다.
- **EU vs 미국 모델 대비 (챕터 핵심 프레임):**
  - GDPR/한국: **opt-in** — 동의를 받아야 처리 가능
  - CCPA/CPRA: **opt-out** — 처리하다가 소비자가 거부하면 중단
  - 그래서 같은 코드베이스로 두 지역을 서비스하려면 **동의 모델 자체가 지역별로 분기**된다. 이게 E-7의 데이터 레지던시 논의로 이어진다.

### E-6-5. EU AI Act [적용 일정: **EU 공식 서비스데스크 확인 ✅**]

- 출처: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act> | 신뢰성 **최상** (European Commission 공식) | 페이지 최종 갱신일 표기 없음 | 검색 시점 2026-07-25

⚠️ **아래 표 전체에 대한 경고:** 이 페이지에는 최종 갱신일 표기가 없다. 2026년 7월 발효된 AI Omnibus가 이 표에 반영됐는지 **확인하지 못했다.** 챕터에 날짜를 옮길 때는 반드시 "2026-07-25 조회 기준"을 병기하라.

| 날짜 | 적용 내용 |
|---|---|
| 2024-08-01 | 발효 (entry into force) |
| 2025-02-02 | "General provisions (definitions & AI literacy) and prohibitions apply" — **금지 관행(Article 5)과 AI 리터러시 의무 적용 시작** |
| 2025-08-02 | 범용 AI(GPAI) 제공자 의무 개시. 회원국의 관할당국 지정·제재 체계 도입, EU 차원 거버넌스(AI Board, Scientific Panel, Advisory Forum) 설치 |
| **2026-08-02** | 투명성 규칙 적용 개시, 혁신 지원 조치 발효. GPAI 모델·금지 관행·투명성 요건·AI 리터러시에 대한 **집행 개시** |
| 2026-12-02 | 비동의 성적 딥페이크·아동 착취물 관련 신규 금지 발효. 2026-08-02 이전 시장 출시된 일부 합성 콘텐츠 제공자에 대한 경과 준수 기한 |
| 2027-08-02 | 회원국은 최소 1개 AI 규제 샌드박스를 운영해야 함 |
| **2027-12-02** | "Rules for high-risk AI systems in Annex III apply" |
| **2028-08-02** | "Rules for high-risk AI embedded in regulated products covered by Annex I apply" |

- **AI Omnibus로 인한 연기 ⚠️ (신뢰성 중 — EU 공식 페이지에서 직접 확인 못 함, 검색 결과 기준):**
  - 요지: 'AI omnibus' 간소화 제안이 2025-11-19 채택, 2026-05-07 정치적 합의, 최종 규정이 **2026년 7월 발효**. 그 결과 Annex I 규제 제품 내장 고위험 AI 규정의 전환기간이 **2028-08-02까지 연장**됐다.
  - 챕터에 쓸 때는 "2026년 중 AI Omnibus로 일정이 완화됐다"는 수준으로 쓰고, 구체 날짜에는 `(사실 확인 필요)` 마커를 붙여라. **이 항목은 검색 시점 기준으로도 진행 중이다.**
- **마케팅 AI에 걸리는 지점 (⚠️ Article 5 원문 미조회 — artificialintelligenceact.eu 요약 기준, 신뢰성 중):**
  - Article 5는 조작적(manipulative)·착취적(exploitative) 관행과 사회적 점수화(social scoring)를 목적으로 하는 AI 시스템의 출시·서비스·사용을 금지한다. 감정 인식과 생체 분류도 포함된다.
  - **마케팅과의 접점:** 취약 집단을 겨냥한 조작적 개인화, 감정 인식 기반 광고 타겟팅. 다만 **일반적인 광고 개인화·리타겟팅이 Article 5에 걸린다는 근거는 이번 리서치에서 확인하지 못했다 — `확인 불가`.**
  - **Article 50(투명성 규칙)이 마케팅에 더 직접적일 가능성이 있으나, 원문 미조회 — `확인 불가 (미조회)`.**
- ⚠️ **챕터에서 "AI Act가 마케팅 타겟팅을 규제한다"고 단정하지 마라.** 확인된 건 일정표와 Article 5의 금지 범주 개요뿐이다.

---

## E-7. 규제가 코드·데이터 모델에 남기는 흔적

⚠️ **이 섹션은 위 1차 출처들에서 도출한 저자 정리다. 개별 문장에 1차 출처가 붙지 않는다.** 챕터에서 수치나 "반드시 이래야 한다"는 단정 없이 설계 서술로 써라. 각 항목이 어느 법조문·문서에서 파생됐는지만 표기했다.

| 코드·데이터 모델에 남는 것 | 파생 근거 (이 문서 안에서 확인된 것) |
|---|---|
| **동의 필드가 boolean 하나가 아니다** | Consent Mode 파라미터 7종(E-3-2) + 정보통신망법 제50조 제1항/제3항이 요구하는 **두 개의 별도 동의**(E-6-2). 최소한 `{목적, 지역, 채널, 시간대}` 축으로 쪼개진다 |
| **동의가 만료된다** | 정보통신망법 제50조 제8항 "정기적으로 광고성 정보 수신자의 수신동의 여부를 확인하여야 한다"(E-6-2). → 동의 레코드에 `verified_at`이 필요하고, 만료 재확인 배치가 필요하다 |
| **동의에 이력이 필요하다** | 제50조 제2항 철회 시 전송 금지 + 제7항 처리 결과 통지 의무. → 현재 상태만이 아니라 **append-only 동의 이벤트 로그** |
| **다크 패턴 금지가 UI 코드 제약이 된다** | 개인정보 보호법 시행령 제17조 제1항 4개 조건(E-6-1). TCF v2.2의 "모두 동의 버튼이 있으면 모두 철회 버튼도"(E-3-1) |
| **"동의 안 하면 가입 불가"를 못 짠다** | 개인정보 보호법 제75조 제2항 — "제16조제3항ㆍ제22조제5항을 위반하여 재화 또는 서비스의 제공을 거부한 자"에 과태료(E-6-1). → 선택 동의 체크박스는 **미체크 상태로도 가입 플로우가 끝까지 통과해야** 한다 |
| **처리방침에 데이터가 어느 나라에 있는지 써야 한다** | 개인정보 보호법 시행령 제31조 제1항 2호·4호(E-6-1). → 벤더 리전을 바꾸면 처리방침을 고쳐야 한다. 인프라 결정이 법무 문서에 물려 있다 |
| **처리방침이 코드 배포와 연동된다** | 개인정보 보호법 제30조 제1항 7호 "인터넷 접속정보파일 등 자동수집 장치"(E-6-1). → 태그 하나 추가 = 처리방침 개정 |
| **보존 기간(TTL)이 스키마의 일부다** | 개인정보 보호법 제30조 제1항 2호 "개인정보의 처리 및 보유 기간", 제16조 최소 수집 원칙(E-6-1) |
| **삭제 요청이 파이프라인 전체를 관통한다** | GDPR Article 17 삭제권(E-6-3) + 한국법 삭제권. 지워야 할 곳: OLTP DB, 이벤트 스트림의 리텐션 구간, 웨어하우스 파티션, 컬럼 지향 포맷(Parquet/Iceberg — 행 단위 삭제가 비싸다), 백업 스냅샷, 검색 인덱스, **그리고 이미 벤더에 싱크된 오디언스** |
| **가명화는 삭제가 아니다** | 개인정보 보호법 제28조의4 요지 — 추가정보를 분리 보관해야 가명정보다(⚠️ 조문 원문 미확인). SHA-256 이메일 해시는 여전히 조인 키다(E-4-3) |
| **감사 로그가 제품 기능이다** | AWS Clean Rooms "Analysis logs ... help support audits"(E-5-1) + 개인정보 보호법 제37조의2 제4항 자동화 결정 공개 의무(E-6-1) |
| **지역별 분기가 런타임에 존재한다** | opt-in(EU/한국) vs opt-out(캘리포니아)(E-6-4) + GDPR Chapter V 국외 이전 + 한국법 제28조의8 국외 이전(⚠️ 조문 원문 미확인). → 요청 지역에 따라 **다른 동의 모델, 다른 저장 리전** |
| **GPC는 헤더 한 줄인데 법적 구속력이 있다** | W3C `Sec-GPC: 1`(E-3-3) + 캘리포니아 AG "it must be honored"(E-6-4) |
| **널·플레이스홀더 ID가 프라이버시 사고를 만든다** | ATT 거부 시 all-zero IDFA(E-1-4) + Ads Data Hub "events with zeroed or null user IDs don't count toward the aggregation threshold"(E-5-2) + ID 그래프 over-merge(E-4-2) |
| **48시간 dedup 창이 배치 잡 설계를 제약한다** | Meta CAPI dedup 48시간(E-2-3) |
| **7일 스토리지 캡이 익명 식별을 무너뜨린다** | Safari ITP 7일 script-writable storage 삭제(E-1-2), CNAME 쿠키 7일 캡(E-1-3) |

---

## 상충·불확실 항목 (스스로 결론 내지 않고 병기)

1. **서버사이드 태깅은 프라이버시 강화인가 회피인가**
   - Google 공식: 서버사이드 태깅이 "Unlock more detailed user privacy controls"를 제공한다 (E-2-1)
   - WebKit 공식: CNAME 클로킹은 추적 방지를 우회하는 수법이며, 쿠키 수명을 7일로 캡한다 (E-1-3)
   - → 병기하라. 같은 아키텍처가 두 진영에서 정반대로 불린다.

2. **개인정보 보호법 과징금 상한 — 3%인가 10%인가**
   - 검색 결과 A: 제64조의2, **전체 매출액의 3% 이하** (위반과 무관한 매출 제외), 매출액 산정 곤란 시 **20억원 이하**
   - 검색 결과 B: 반복·중대 위반(고의·중과실) 시 **10%까지** 가능
   - → **둘 다 law.go.kr 조문 원문으로 확인하지 못했다.** A가 여러 2차 자료에서 더 일관되게 나오지만, 확정하지 마라. 챕터에 수치를 쓰지 말거나, 쓴다면 `(사실 확인 필요)`를 붙여라.
   - **부수 주의: 과징금(제64조의2)과 과태료(제75조)는 다른 제재다.** 제75조는 원문으로 확인했다(5천만/3천만/2천만/1천만원 이하 4구간). 둘을 섞어 쓰지 마라. 정보통신망법의 6% 과징금(E-6-2)과도 별개다.

3. **Privacy Sandbox status 페이지 vs Chrome 144 릴리스 노트**
   - status 페이지(2025-10-17): Topics·Attribution Reporting·Related Website Sets 포함 7개가 "Deprecate and Remove"
   - Chrome 144 릴리스 노트(2026-01-13): deprecation 섹션에 Private Aggregation, Shared Storage, Protected Audience 세 개만 명시
   - blink-dev(2025-11-08, 2026-06-12 갱신): Topics는 M144 deprecate, M150 remove
   - → 세 소스가 서로 다른 커버리지를 보인다. **"Chrome 144에서 무엇이 deprecate됐다"를 단정하지 말고 API별로 소스를 달리 인용하라.**

4. **IP Protection의 운명**
   - 2025-04-22 Google 블로그: 2025년 3분기 런칭 예정
   - 2025-10-17 status 페이지: Discontinue (Do Not Launch)
   - → 이건 상충이 아니라 **번복**이다. 궤적으로 서술하면 챕터의 가장 좋은 사례가 된다.

5. **EU AI Act의 최종 일정**
   - EU 공식 서비스데스크 타임라인은 확인했으나, AI Omnibus의 최종 변경 내역이 그 페이지에 반영됐는지 확인하지 못했다. 페이지 자체에 최종 갱신일이 없다.
   - → 챕터에 AI Act 일정을 쓸 때는 "2026년 7월 기준"임을 명시하라.

6. **정보통신망법 제50조 제3항 야간 제한의 적용 범위**
   - 법 원문: 오후 9시~오전 8시 별도 동의 필요 **+ 대통령령이 정하는 매체는 예외** (둘 다 원문 확인 ✅)
   - 2차 자료: 예외 매체 = 전자우편 (신뢰성 중, 시행령 원문 미확인)
   - → **"11시간 창"만 떼어 쓰면 절반만 맞는 서술이 된다.** 반드시 단서와 함께 서술하라.

7. **PIPC의 온라인 맞춤형 광고 가이드라인 존재 여부**
   - 2026-07-25 기준 PIPC 안내서 목록에서 해당 제목의 문서를 확인하지 못했다.
   - → 있었다가 통합·폐지됐을 수 있고, 다른 게시판에 있을 수도 있다. **존재를 단정하지 마라.**

---

## 확인 불가 목록 (챕터에 쓰지 말 것 / 별도 확인 필요)

**E-1**
- Chrome M150의 실제 stable 릴리스 날짜 (chromiumdash JS 렌더링 실패)
- Privacy Sandbox status 페이지의 2026년 갱신본 존재 여부
- Firefox Total Cookie Protection이 기본값이 된 정확한 Firefox 버전 번호 (support.mozilla.org 로드 실패)
- SKAdNetwork의 deprecation 여부, 버전, conversion value 스펙 (Apple 문서 SPA 추출 실패)
- AdAttributionKit ↔ SKAdNetwork 상호운용의 정확한 문언 및 iOS 버전 요건
- CMA 결정문 PDF 본문 (요약만 확보)

**E-2**
- Meta가 CAPI를 만든 이유로 브라우저 제약·광고 차단기를 공식적으로 언급했는지 (공식 페이지에는 없음)
- GTM 서버사이드의 CNAME/서브도메인 설정에 대한 Google 공식 권고 문언

**E-4**
- raw UID2의 파생 절차 (해싱·솔팅), 토큰 정의·회전 주기
- RampID의 현재 상태
- 이메일 SHA-256 해시가 업계 표준 식별자인지에 대한 1차 근거
- LiveRamp/Adobe/Salesforce의 deterministic·probabilistic 정의 **원문** (검색 요약만 확보 — 따옴표 인용 금지)

**E-5**
- Snowflake Data Clean Rooms의 집계 임계값·join policy·projection policy
- Amazon Marketing Cloud의 구체적 집계 임계값 수치
- **어느 벤더도 PSI(Private Set Intersection)나 k-anonymity를 그 이름으로 명시하지 않았다**

**E-6**
- 개인정보 보호법 제16조제3항·제17조·제22조·제22조제5항·제28조의2~제28조의9·제35조·제35조의2·제36조·제37조·제64조의2 **조문 원문** (law.go.kr 본문 프레임 접근 실패). 제28조의8과 제16조제3항·제22조제5항은 **다른 조문의 인용을 통해 존재와 취지만 간접 확인**했다
- 제37조의2의 시행일 (부칙 미확인)
- 정보통신망법 2026-07-07 개정의 과징금 6% 수치 및 전송 위탁 조문 (law.go.kr 원문 미확인)
- **정보통신망법 제50조 제3항 단서의 "대통령령으로 정하는 매체"가 무엇인지** — 단서의 존재는 원문 확인했으나 시행령 원문 미확인. 2차 자료는 **전자우편**이라고 하나 미검증. **앱 푸시가 면제 대상인지는 확인 불가** (martech 구현에 가장 중요한 미결 항목)
- 개인정보 보호법 제16조 제3항·제22조 제5항 원문 (제75조 제2항의 인용으로 취지만 확인)
- CCPA "sale"의 법문 정의 및 Civil Code 조문 번호
- EU AI Act Article 5·Article 50 원문
- AI Omnibus 최종 규정의 공식 텍스트
- PIPC 안내서 각 문서의 **본문** (제목·발행 시점만 확보)

---

## 신선도 원장

| 소스 | URL | 발행일 / 갱신일 | 검색 시점 | 관련 항목 | 신뢰성 |
|---|---|---|---|---|---|
| Google Privacy Sandbox — 3PC 유지 결정 | privacysandbox.google.com/blog/privacy-sandbox-next-steps | 2025-04-22 | 2026-07-25 | E-1-1 | 최상 |
| Google Privacy Sandbox — 기술 은퇴 | privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies | 2025-10-17 | 2026-07-25 | E-1-1 | 최상 |
| Privacy Sandbox feature status | privacysandbox.google.com/overview/status | 2025-10-17 (페이지 최종 갱신) | 2026-07-25 | E-1-1 | 최상 ⚠️ 2026 갱신 미확인 |
| Chrome 144 릴리스 노트 | developer.chrome.com/release-notes/144 | stable 2026-01-13 | 2026-07-25 | E-1-1 | 최상 |
| blink-dev — Intent to Deprecate/Remove Topics | groups.google.com/a/chromium.org/g/blink-dev/c/_R85yctz4Rs | 2025-11-08, 갱신 2026-06-12 | 2026-07-25 | E-1-1 | 최상 |
| topics-api-announce PSA | groups.google.com/a/chromium.org/g/topics-api-announce/c/iQX7PC3S0Ds | 2025-12-05 | 2026-07-25 | E-1-1 | 최상 |
| UK CMA — Privacy Sandbox 사건 | gov.uk/cma-cases/investigation-into-googles-privacy-sandbox-browser-changes | 결정 2025-10-17 | 2026-07-25 | E-1-1 | 최상 ⚠️ PDF 본문 미조회 |
| WebKit — ITP 최초 도입 | webkit.org/blog/7675/ | 2017-06-05 | 2026-07-25 | E-1-2 | 최상 ⚠️ 구버전 정보 |
| WebKit — Full 3rd-Party Cookie Blocking | webkit.org/blog/10218/ | 2020-03-24 | 2026-07-25 | E-1-2 | 최상 |
| WebKit — CNAME Cloaking Defense | webkit.org/blog/11338/ | 2020-11-12 | 2026-07-25 | E-1-3, E-2 | 최상 |
| Mozilla — Total Cookie Protection | blog.mozilla.org/en/products/firefox/firefox-rolls-out-total-cookie-protection... | 2022-06-14 (업데이트 2024-08-28) | 2026-07-25 | E-1-3 | 최상 |
| Apple — User Privacy and Data Use | developer.apple.com/app-store/user-privacy-and-data-use/ | 표기 없음 | 2026-07-25 | E-1-4 | 최상 |
| Apple — AppTrackingTransparency | developer.apple.com/documentation/apptrackingtransparency | 표기 없음 | 2026-07-25 | E-1-4 | 최상 |
| Google — Server-side tagging | developers.google.com/tag-platform/tag-manager/server-side | 표기 없음 | 2026-07-25 | E-2-1 | 최상 |
| Google — Send data to server container | developers.google.com/tag-platform/tag-manager/server-side/send-data | 표기 없음 | 2026-07-25 | E-2-1 | 최상 |
| Meta — Conversions API | developers.facebook.com/docs/marketing-api/conversions-api | 표기 없음 | 2026-07-25 | E-2-2 | 최상 |
| Meta — Deduplicate Pixel & Server Events | developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events | 표기 없음 | 2026-07-25 | E-2-3 | 최상 |
| IAB Europe — TCF v2.3 전환 | iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/ | 2025-06-19 | 2026-07-25 | E-3-1 | 최상 |
| IAB Europe — TCF v2.2 | iabeurope.eu/tcf/, iabeurope.eu/tcf-2-2-launches-all-you-need-to-know/ | 2023 (v2.2 출시 2023-05-16) | 2026-07-25 | E-3-1 | 최상 |
| Google — Consent mode overview | developers.google.com/tag-platform/security/concepts/consent-mode | 표기 없음 | 2026-07-25 | E-3-2 | 최상 |
| W3C — Global Privacy Control | w3.org/TR/gpc/ | **2026-06-11 (Working Draft)** | 2026-07-25 | E-3-3 | 최상 |
| LiveRamp / Segment — identity resolution | liveramp.com/uk/blog/probabilistic-vs-deterministic-matching, segment.com/blog/identity-resolution/ | 표기 없음 | 2026-07-25 | E-4-1 | 중 ⚠️ 본문 미조회 |
| Unified ID 2.0 문서 | unifiedid.com/docs/intro | **최종 갱신 2026-07-23** | 2026-07-25 | E-4-3 | 최상 |
| AWS Clean Rooms — What is | docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html | 표기 없음 | 2026-07-25 | E-5-1 | 최상 |
| Google Ads Data Hub — Intro | developers.google.com/ads-data-hub/guides/intro | 표기 없음 | 2026-07-25 | E-5-2 | 최상 |
| Google Ads Data Hub — Privacy checks | developers.google.com/ads-data-hub/guides/privacy-checks | 표기 없음 | 2026-07-25 | E-5-2 | 최상 |
| Amazon Marketing Cloud | advertising.amazon.com/solutions/products/amazon-marketing-cloud | 표기 없음 | 2026-07-25 | E-5-3 | 최상 |
| Snowflake Data Clean Rooms | docs.snowflake.com/en/user-guide/cleanrooms/introduction | 표기 없음 | 2026-07-25 | E-5-4 | 최상 |
| **법제처 — 개인정보 보호법** | law.go.kr/LSW/lsInfoP.do?lsId=011357 | **시행 2025-10-02, 법률 제20897호 (2025-04-01 일부개정)** | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 조문 (제15·16·24·30조) | law.go.kr/LSW//lsLawLinkInfo.do?...lsJoLnkSeq=900078586..., ...lsJoLnkSeq=1020398697 | 상동 | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 제37조의2 | law.go.kr/LSW/lsLinkCommonInfo.do?...lsJoLnkSeq=1029334889 | 상동 | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 제75조 (과태료) | law.go.kr/LSW/lsLinkCommonInfo.do?...lsJoLnkSeq=1020398445 | 상동 | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 시행령 제17조 | law.go.kr/LSW/lsLawLinkInfo.do?lsJoLnkSeq=1000572094 | — | 2026-07-25 | E-6-1 | 최상 |
| 법제처 — PIPA 시행령 제31조 (처리방침·국외이전 고지) | law.go.kr/LSW//lsLawLinkInfo.do?lsJoLnkSeq=900079801 | — | 2026-07-25 | E-6-1, E-7 | 최상 |
| **법제처 — 정보통신망법 제50조** | law.go.kr/LSW/lsLawLinkInfo.do?...lsJoLnkSeq=1000688185...&print=print | **시행 2026-07-07, 법률 제21305호 (2026-01-06 일부개정)** | 2026-07-25 | E-6-2 | 최상 |
| 정보통신망법 2026 개정 해설 (법무법인) | bkl.co.kr/law/insight/newsletter/6642 | 2026 | 2026-07-25 | E-6-2 | 중 |
| **PIPC 안내서 목록** | pipc.go.kr/np/cop/bbs/selectBoardList.do?bbsId=BS217&mCode=D010030000 | 최신 항목 **2026-06-25** | 2026-07-25 | E-6-1 | 최상 |
| EUR-Lex — GDPR | eur-lex.europa.eu/eli/reg/2016/679/oj/eng | 2016-04-27 | 2026-07-25 | E-6-3 | 최상 |
| California AG — CCPA | oag.ca.gov/privacy/ccpa | 표기 없음 | 2026-07-25 | E-6-4 | 최상 |
| EU — AI Act 이행 타임라인 | ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act | 표기 없음 | 2026-07-25 | E-6-5 | 최상 |

---

## 참고문헌

**브라우저·플랫폼 정책 (1차)**
1. Anthony Chavez, "Next steps for Privacy Sandbox and tracking protections in Chrome", Google, 2025-04-22. https://privacysandbox.google.com/blog/privacy-sandbox-next-steps
2. Anthony Chavez, "Update on Plans for Privacy Sandbox Technologies", Google, 2025-10-17. https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies
3. "Privacy Sandbox feature status", Google, 2025-10-17. https://privacysandbox.google.com/overview/status
4. "Chrome 144 release notes", Chrome for Developers, stable 2026-01-13. https://developer.chrome.com/release-notes/144
5. Yao Xiao, "Intent to Deprecate and Remove: Topics API", blink-dev, 2025-11-08 (갱신 2026-06-12). https://groups.google.com/a/chromium.org/g/blink-dev/c/_R85yctz4Rs
6. Sam Dutton, "PSA: Topics API deprecation and removal", topics-api-announce, 2025-12-05. https://groups.google.com/a/chromium.org/g/topics-api-announce/c/iQX7PC3S0Ds
7. Competition and Markets Authority, "Investigation into Google's 'Privacy Sandbox' browser changes" (결정 2025-10-17). https://www.gov.uk/cma-cases/investigation-into-googles-privacy-sandbox-browser-changes
8. John Wilander, "Intelligent Tracking Prevention", WebKit, 2017-06-05. https://webkit.org/blog/7675/intelligent-tracking-prevention/
9. John Wilander, "Full Third-Party Cookie Blocking and More", WebKit, 2020-03-24. https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/
10. John Wilander, "CNAME Cloaking and Bounce Tracking Defense", WebKit, 2020-11-12. https://webkit.org/blog/11338/cname-cloaking-and-bounce-tracking-defense/
11. Mozilla, "Firefox rolls out Total Cookie Protection by default to all users worldwide", 2022-06-14 (업데이트 2024-08-28). https://blog.mozilla.org/en/products/firefox/firefox-rolls-out-total-cookie-protection-by-default-to-all-users-worldwide/
12. Apple, "User Privacy and Data Use". https://developer.apple.com/app-store/user-privacy-and-data-use/
13. Apple, "AppTrackingTransparency". https://developer.apple.com/documentation/apptrackingtransparency

**수집 아키텍처 (1차)**
14. Google, "Server-side tagging". https://developers.google.com/tag-platform/tag-manager/server-side
15. Google, "Send data to a server container". https://developers.google.com/tag-platform/tag-manager/server-side/send-data
16. Meta, "Conversions API". https://developers.facebook.com/docs/marketing-api/conversions-api
17. Meta, "Deduplicate Pixel and Server Events". https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events

**동의 (1차)**
18. IAB Europe, "All You Need to Know About the Transition to TCF v2.3", 2025-06-19. https://iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/
19. IAB Europe, "The Transparency & Consent Framework (TCF) v2.2". https://iabeurope.eu/tcf/
20. Google, "Consent mode overview". https://developers.google.com/tag-platform/security/concepts/consent-mode
21. W3C, "Global Privacy Control (GPC)", Working Draft, 2026-06-11. https://www.w3.org/TR/gpc/

**아이덴티티 (1차·2차)**
22. Unified ID 2.0 documentation (최종 갱신 2026-07-23). https://unifiedid.com/docs/intro
23. LiveRamp, "Probabilistic vs Deterministic Matching". https://liveramp.com/uk/blog/probabilistic-vs-deterministic-matching ⚠️ 본문 미조회
24. Twilio Segment, "Identity resolution: what it is and how it works". https://segment.com/blog/identity-resolution/ ⚠️ 본문 미조회

**클린룸 (1차)**
25. AWS, "What is AWS Clean Rooms?". https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html
26. Google, "Ads Data Hub introduction". https://developers.google.com/ads-data-hub/guides/intro
27. Google, "Privacy checks in Ads Data Hub". https://developers.google.com/ads-data-hub/guides/privacy-checks
28. Amazon Ads, "Amazon Marketing Cloud". https://advertising.amazon.com/solutions/products/amazon-marketing-cloud
29. Snowflake, "Snowflake Data Clean Rooms introduction". https://docs.snowflake.com/en/user-guide/cleanrooms/introduction

**규제 (1차)**
30. 법제처 국가법령정보센터, 「개인정보 보호법」 (시행 2025-10-02, 법률 제20897호). https://www.law.go.kr/LSW/lsInfoP.do?lsId=011357&ancYnChk=0
31. 법제처 국가법령정보센터, 「정보통신망 이용촉진 및 정보보호 등에 관한 법률」 제50조 (시행 2026-07-07, 법률 제21305호). https://www.law.go.kr/LSW/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000688185&lsId=000030&print=print
32. 개인정보보호위원회, 안내서 목록. https://www.pipc.go.kr/np/cop/bbs/selectBoardList.do?bbsId=BS217&mCode=D010030000
33. EUR-Lex, Regulation (EU) 2016/679 (GDPR). https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
34. California Attorney General, "California Consumer Privacy Act (CCPA)". https://oag.ca.gov/privacy/ccpa
35. European Commission AI Act Service Desk, "Timeline for the Implementation of the EU AI Act". https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act

**규제 (2차 — 신뢰성 중, 교차 확인 필요)**
36. 법무법인(유) 태평양, "정보통신망법 시행령 일부개정: 주요 내용과 시사점". https://www.bkl.co.kr/law/insight/newsletter/6642

---

## 수집 한계

- **law.go.kr 프레임 구조**: 국가법령정보센터는 프레임/SPA 기반이라 `법령/{법령명}` 경로로는 본문이 추출되지 않았다. `lsLawLinkInfo.do?...&print=print`와 `lsLinkCommonInfo.do?lsJoLnkSeq=` 패턴만 본문을 반환했다. 이 패턴은 조문별 `lsJoLnkSeq` 값을 알아야 해서, 검색으로 발견한 조문만 원문 확인이 가능했다. **후속 리서치자를 위한 팁: 이 두 URL 패턴을 쓰라.**
- **Apple 개발자 문서**: SPA라 일반 URL로는 추출 실패. `developer.apple.com/tutorials/data/documentation/{path}.json` 엔드포인트는 성공했다. 상시 HTML인 `developer.apple.com/app-store/...` 경로도 성공.
- **chromestatus.com, chromiumdash.appspot.com**: JS 렌더링 의존으로 추출 실패.
- **EUR-Lex 장문 인용**: 수집 도구의 인용 길이 제한으로 GDPR 조문 전문 확보 실패. 조각 문언과 조문 번호만 확보.
- **의도적 제외**: 커뮤니티(Reddit/HN/OKKY), 논문, 벤더 마케팅 블로그의 수치 주장. 다른 에이전트 담당이거나 신뢰성이 낮다.
- **날짜 없는 공식 문서**: 다수 벤더 문서(Google/Meta/AWS/Apple)에 발행일 표기가 없다. "표기 없음 / 검색 시점 2026-07-25"로 기록했다. **이 항목들은 6개월 뒤 재확인이 필요하다.**

<!-- ===== web_gaps.md ===== -->

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
