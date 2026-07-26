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
