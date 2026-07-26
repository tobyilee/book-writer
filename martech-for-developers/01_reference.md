<!-- genre: tech-book / slug: martech-for-developers -->
<!-- 리서치 수행일: 2026-07-25 / 합성: research-lead -->

# Martech (CDP / CEP / AI 마케팅 도구) 레퍼런스

**대상 독자:** 웹·앱 개발 경험은 풍부하지만 마케팅 도메인 지식은 거의 없는 개발자. Martech 제품을 만들거나 운영하는 회사에 입사할 준비를 하고 있다.

**리서치 수행일:** 2026-07-25 (모든 "검색 시점"은 이 날짜다)

---

## 이 문서를 읽는 규칙 (Phase 4 fact-checker 필독)

이 문서는 5개 리서치 산출물의 합성이다. 원본은 보존되어 있고, **fact-checker의 1차 대조 근거는 원본 파일**이다.

| 원본 | 담당 축 |
|---|---|
| **`research/web.md`** | **위 4개 웹 리서치 파일의 병합본** (하네스 계약 경로 — fact-checker의 1차 대조 대상) |
| `research/web_products.md` | 제품 카테고리 분류학 · Insider · 벤더 개발자 표면 · Segment Spec |
| `research/web_stack.md` | 오픈소스 데이터 스택 · 근사 자료구조 · 아키텍처 사례 |
| `research/web_privacy.md` | 브라우저 정책 · 동의 · 아이덴티티 · 클린룸 · 규제 |
| `research/web_gaps.md` | 카테고리 정의 갭 필러 (DMP/CRM/MA/CEM, Identity Resolution) |
| `research/papers.md` | 마케팅 원리·기반 기술의 학술 근거 |
| `research/community.md` | 채용 공고 · 현장 pain point · 한국 시장 |

> 웹 리서치는 커버리지 부담이 커서 **3개 축 + 갭 필러 1개로 분할 실행**했다. `web.md`는 그 넷을 순서대로 이어붙인 병합본이며, **원본 4개도 함께 보존**된다.

**라벨 규약 — 이 문서 전체에 적용된다:**

- `1차 확인` — 해당 리서처가 이 세션에서 실제로 페이지를 열어 확인한 것.
- `벤더 자체 주장` — 벤더가 자기 제품에 대해 한 말. 사실로 격상하지 않았다.
- `(2차 인용)` — 다른 매체·요약을 거친 것. 1차 확인이 아니다.
- `커뮤니티 주장 (검증 필요)` — 익명 개인의 진술.
- `관찰` — 리서처가 여러 문서를 대조해 도출한 것. 어느 출처의 인용도 아니다.
- `확인 불가` — 조회 실패 또는 미조회. **추측으로 메우지 않았다.**

> **가장 중요한 규율:** 이 문서에 없는 수치·버전·조문은 **저술 시점에 새로 확인해야 한다.** 기억으로 채우면 거의 틀린다. 이 리서치가 그것을 반복해서 실증했다(§9 참조).

---

## 1. 개념과 정의

### 1-1. Martech이란 무엇인가 — 개발자에게 통하는 정의

가장 명료한 1차 정의는 벤더의 마케팅 문구가 아니라 **한 실무 리드의 인터뷰**에서 나왔다.

> "마케팅 성과 분석이란 어떤 광고를 사용자가 봤다는 것에 대한 기록, 이를 통해 설치나 구매 등의 전환을 일으켰다는 기록을 놓치지 않고 수집해서 인과관계 분석을 돕는 것인데요, Mar-Tech는 이 과정을 기술적으로 풀어 가는 비즈니스 분야라고 생각해 주시면 됩니다."
>
> — AB180 Data Pipeline Team Lead 김재원 [engineering.ab180.co/stories/data-pipeline-team-interview | **게시일 미상** | 검색 시점 2026-07-25] `1차 확인` `[community]`

⚠️ 이 블로그 글은 **페이지에 게시일이 없다.** 인용은 가능하나 시점을 특정하지 마라.

### 1-2. CDP의 핵심 스키마는 사실상 두 테이블이다

이 리서치에서 가장 강한 발견 중 하나다. **여러 벤더의 개발자 문서를 나란히 놓으면, 이름만 다르고 구조가 같다.** Adobe가 이걸 가장 명시적인 언어로 표현한다.

> **XDM Individual Profile**: "A record-based class that forms a singular representation of the attributes of both identified and partially identified subjects."
>
> **XDM ExperienceEvent**: "A time-series-based class used to capture the state of the system when an event (or set of events) occurred, including the point in time and identity of the subject involved."
>
> [experienceleague.adobe.com/en/docs/experience-platform/xdm/home | 문서 표기 "Last update May 23, 2026" | 검색 시점 2026-07-25] `1차 확인` `[web-products]`

**즉 레코드 하나 + 시계열 로그 하나.** 같은 축이 전 벤더에서 반복된다:

| 개념 | Segment Spec | RudderStack | Insider One (UCD) | Adobe (XDM) | Bloomreach | Klaviyo |
|---|---|---|---|---|---|---|
| 사용자 식별 | `identify` + `userId`/`anonymousId` | `Identify` | `identifiers` (`email`/`phone_number`/`uuid`) 또는 `insider_id` | (identity graph 언급만) | **hard IDs / soft IDs** | `Profiles` |
| 사용자 속성 | `traits` (예약 17종) | (Identify의 traits) | `attributes` + `custom` | **XDM Individual Profile** | Customers | `Profiles` |
| 행동 이벤트 | `track` + `event` + `properties` | `Track` | `events[]` + `event_name` + `event_params` | **XDM ExperienceEvent** | Events | `Events` |
| 화면/페이지 | `page` / `screen` | `Page` / `Screen` | `type: 'home'/'category'/'product'/'cart'/'purchase'/'other'` | 확인 불가 | 확인 불가 | 확인 불가 |
| 조직/계정 | `group` | `Group` | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 |
| 신원 병합 | `alias` | `Alias` | Update Identifiers API | 확인 불가 | (hard/soft ID 병합) | 확인 불가 |
| 세션 리셋 | (스펙에 없음) | `Reset` | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 |

`[web-products]` — 표의 각 항목은 해당 벤더 공식 문서를 실제로 열어 확인한 것. "확인 불가"는 **이 세션에서 조회한 페이지 범위 안에서** 못 찾았다는 뜻이지, 그 기능이 없다는 뜻이 아니다.

> **개발자에게 전할 한 문장:** CDP의 핵심 스키마는 두 테이블이다 — 사용자 테이블 하나, 이벤트 로그 하나. 나머지는 전부 그 위의 뷰·조인·인덱스다.

**식별자 이원화도 전 벤더 공통이다.** Segment의 `userId` vs `anonymousId`, Bloomreach의 hard ID vs soft ID, Insider의 `identifiers` vs `insider_id`. 같은 문제(로그인 전/후)를 각자 다른 이름으로 푼 것. `관찰`

### 1-3. Segment Spec — 마테크 데이터 수집의 전부가 6개 질문이다

Segment가 정의한 6개 API 콜과 각각의 한 줄 정의 (원문):

| 콜 | 원문 정의 |
|---|---|
| **Identify** | "who is the customer?" |
| **Track** | "what are they doing?" |
| **Page** | "what web page are they on?" |
| **Screen** | "what app screen are they on?" |
| **Group** | "what account or organization are they part of?" |
| **Alias** | "what was their past identity?" |

[raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/index.md | 발행일 미표기 (develop 브랜치 / 2026-07-25 조회) | 검색 시점 2026-07-25] `1차 확인` `[web-products]`

> ⚠️ **조회 경로 주의:** `segment.com/docs/`는 **403 Forbidden**이었다. 위 인용은 Segment가 공개한 **문서 소스 리포지터리의 raw 마크다운**에서 가져온 것 — 1차 소스이되 렌더된 문서 사이트가 아니다.

**`identify` 예약 traits (원문 표):** `address`(Object), `age`(Number), `avatar`(String), `birthday`(Date), `company`(Object), `createdAt`(Date), `description`(String), `email`(String), `firstName`(String), `gender`(String), `id`(String), `lastName`(String), `name`(String), `phone`(String), `title`(String), `username`(String), `website`(String)

**`track` 예약 properties (원문):** `revenue`(Number, "Amount of revenue an event resulted in"), `currency`(String), `value`(Number, "An abstract 'value' to associate with an event")

**`alias` — 개발자가 가장 자주 틀리는 지점:**

> "an advanced method used to merge 2 unassociated user identities, effectively connecting 2 sets of user data in one profile."

문서는 이것이 **고급 유스케이스 전용**이며, Segment의 Unify 제품 안에서 프로필을 병합하는 용도로는 **쓸 수 없다**고 명시한다 — 그건 Identity Resolution이 한다.

> **관찰:** "익명 사용자가 로그인했다"를 `alias`로 처리하려는 시도가 흔하지만, 문서는 그게 Identity Resolution의 일이라고 못박는다. 익명→식별 전환은 **모든 CDP에서 가장 어려운 문제**이며, Bloomreach의 hard/soft ID, Adobe의 identity graph, Insider의 Update Identifiers API가 전부 같은 문제를 각자 다르게 푼 결과다. `[web-products]`

**`context` 객체 — 모든 콜에 붙는 환경 정보 (18개 필드).** 그중 개발자에게 결정적인 하나:

> `channel` (String): "Where the request originated from: server, browser, or mobile."

**서버사이드 / 클라이언트사이드 구분이 스펙의 일급 필드로 박혀 있다.** "어디서 이벤트를 쏘느냐"가 왜 설계 문제인지의 근거다. `[web-products]`

### 1-4. E-commerce Spec — 커머스 이벤트 이름은 이미 표준화되어 있다

Segment는 커머스 이벤트 이름을 예약해 두었다. 그대로 쓰면 다운스트림 도구가 별도 매핑 없이 해석한다. (v2 스펙)

| 그룹 | 예약 이벤트 이름 |
|---|---|
| **Browsing** | `Products Searched`, `Product List Viewed`, `Product List Filtered` |
| **Promotions** | `Promotion Viewed`, `Promotion Clicked` |
| **Core Ordering** | `Product Clicked`, `Product Viewed`, `Product Added`, `Product Removed`, `Cart Viewed`, `Checkout Started`, `Checkout Step Viewed`, `Checkout Step Completed`, `Payment Info Entered`, `Order Completed`, `Order Updated`, `Order Refunded`, `Order Cancelled` |
| **Coupons** | `Coupon Entered`, `Coupon Applied`, `Coupon Denied`, `Coupon Removed` |
| **Wishlisting** | `Product Added to Wishlist`, `Product Removed from Wishlist`, `Wishlist Product Added to Cart` |
| **Sharing** | `Product Shared`, `Cart Shared` |
| **Reviewing** | `Product Reviewed` |

[raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/ecommerce/v2.md | v2 스펙 / 2026-07 조회 기준 | 검색 시점 2026-07-25] `1차 확인` `[web-products]`

> **관찰 — 같은 도메인 지식을 두 방식으로 인코딩한다.** Insider는 커머스 이벤트를 **SDK 메서드 타입**으로 못박았다(`type: 'product'` → `product_detail_page_view`). Segment는 **이벤트 이름 문자열 규약**으로 풀었다(`track('Product Viewed')`). 강한 타입 vs 유연한 컨벤션 — 개발자에게 익숙한 트레이드오프다. ⚠️ 이 대조는 리서처의 관찰이며 두 벤더 모두 서로를 언급하지 않았다. `[web-products]`

### 1-5. 스택 전체 지도 — 다섯 개 층

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
     Reverse ETL, 저니 엔진, 캠페인 트리거
```

`[web-stack]`

**개발자가 잡아야 할 축 세 개** — 이후 모든 도구 선택이 "이 축의 어디에 있느냐"로 설명된다:

- **지연(latency) 축** — 이 이벤트가 세그먼트에 반영되기까지 몇 초/몇 시간이 허용되나? → Flink냐 dbt냐를 가른다.
- **기수(cardinality) 축** — 유니크 카운트를 정확히 세야 하나, 근사해도 되나? → `uniqExact` vs HyperLogLog를 가른다.
- **조회 패턴 축** — 집계 스캔(OLAP)인가, 단건 프로필 조회(KV)인가? → 같은 고객 데이터가 두 벌 존재하는 이유.

---

## 2. 제품 카테고리 분류학

### 2-0. ✅ 앵커 — "CDP"라는 말을 만든 사람의 원문 (David Raab, 2013-04-25)

`cdpinstitute.org`는 **사이트 전역 403**이라 기관 공식 정의문을 얻지 못했다(§2-0-2). 대신 **그 카테고리를 처음 명명한 David Raab 본인의 블로그 원문 3건**을 확보했다. 저자가 확인되는 1차 소스다. `[web-products]`

**① 최초 명명 (2013-04-25)** — 글 제목: "I've Discovered a New Class of System: the Customer Data Platform. Causata Is An Example."

시스템이 하는 일 (원문):
> "These systems that gather customer data from multiple sources, combine information related to the same individuals, perform predictive analytics on the resulting database, and use the results to guide marketing treatments across multiple channels."

이름을 붙이는 대목 (원문) — **세 단어가 각각 무엇을 주장하는지 작명자 본인이 밝힌다**:
> "I'll step in myself, and hereby christen the concept as 'Customer Data Platform'. ... the merits of this name include:
> - "Customer" shows the scope extends to all customer-related functions, not just marketing;
> - "Data" shows the primary focus is on data, not execution; and
> - "Platform" shows it does more than data management while supporting other systems"

[customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html | **2013-04-25** | 검색 시점 2026-07-25] `1차 확인` ⚠️ **13년 경과 — 카테고리의 *기원*을 말할 때만 쓰고 현재 제품의 정의로 쓰지 마라.**

**② 다듬어진 정의 (2015-01-18)** — 같은 저자, 원문:
> "a marketer-controlled system that builds a multi-source customer database and exposes it to external execution systems"

[customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html | **2015-01-18** | 검색 시점 2026-07-25] `1차 확인` ⚠️ 11년 경과
⚠️ 이 글에서 DMP·CRM·MA·데이터 웨어하우스와의 명시적 대비 → **NOT FOUND**

> **2013 → 2015 정의 변화가 흥미롭다** (`관찰`, 두 정의문만 사실): 2013년 정의에 있던 "perform predictive analytics"가 2015년에는 빠지고, **"marketer-controlled"**(소유권)와 **"exposes it to external execution systems"**(개방성)가 핵심으로 올라왔다.
> 개발자 독자에게: **"CDP는 왜 데이터를 자기 안에 가둬두지 않고 밖으로 내보내는가"의 답이 정의 자체에 박혀 있다.**

**③ 유형 분류 (2018-11-03)** — 글 제목: "Why Are There So Many Types of Customer Data Platforms? It's Complicated."

| 유형 | 원문 |
|---|---|
| **Data CDP** | "CDPs with a customer database" |
| **Analytics CDP** | "CDPs with a customer database plus customer analytics" |
| **Personalization CDP** | "a customer Database, analytics, and personalization" |

추가 언급: **Marketing Suite CDPs** — 실행(delivery) 시스템이 거꾸로 확장해 데이터베이스·분석·개인화를 흡수한 형태. Raab은 이런 것들이 CDP 정의를 의미 없을 정도로 늘린다고 지적한다. (요지)

카테고리 혼란에 대한 Raab 본인의 진술 (원문):
> "CDPs are not simple: the industry has rapidly evolved numerous subspecies of CDPs that are as different from each other as the different kinds of dinosaurs."
>
> "For CDP to have any meaning, it must describe a system whose primary purpose is to build a persistent, sharable customer database."

[customerexperiencematrix.blogspot.com/2018/11/why-are-there-so-many-types-of-customer.html | **2018-11-03** | 검색 시점 2026-07-25] `1차 확인`

> 🚨 **정정 — 널리 쓰이는 "4분류"는 이 원문에 없다.**
> "Data / Analytics / **Campaign** / **Delivery** CDP"라는 4분류가 흔히 인용되지만, **Raab 2018 원문의 세 번째 유형은 "Personalization CDP"이고 "Campaign CDP"·"Delivery CDP"라는 용어는 그 글에 등장하지 않는다.**
> - `Data CDP` / `Analytics CDP` / `Personalization CDP` → ✅ Raab 2018 원문 확인
> - `Campaign CDP` / `Delivery CDP` → **확인 불가.** CDP Institute가 별도로 쓰는 용어일 가능성은 있으나 403으로 검증 실패.
>
> **책에 4분류로 쓰지 마라.** "Data / Analytics / Personalization" 3분류를 **"2018년 Raab 기준"을 병기해서** 쓰라. ⚠️ 8년 전 분류이므로 현재 기관 분류와 다를 수 있다.

> **개발자에게 이 3분류가 유용한 이유:** 데이터베이스만 있는가(Data) / 그 위에 분석이 있는가(Analytics) / 그 위에 실행까지 있는가(Personalization) — **레이어가 쌓이는 순서**다. Hightouch(데이터를 저장조차 안 하는 액티베이션 레이어)와 Insider One(UCD + 세그먼트 + 채널 실행 전부)을 이 축에 놓으면 시장 지도가 바로 그려진다.

### 2-0-2. ⚠️ 남은 결손 — CDP Institute 기관 공식 정의문

`cdpinstitute.org` 6개 URL(www 유무·하위 경로 4개·지역 서브도메인) 전부 **403**, web.archive.org 우회도 도구 접근 불가. Gartner 용어집도 **403**. `[web-products]`

> **저술 시 규율:** "CDP Institute는 CDP를 ~라고 정의한다"를 쓰려면 별도 확인이 필요하다. **"persistent, unified customer database that is accessible to other systems" 계열 문장은 널리 회자되지만 이 세션에서 원문 대조를 하지 못했다. 기억으로 복원해 넣지 마라.**
> 대신 **"CDP라는 용어를 만든 David Raab은 ~라고 썼다"**로 쓰면 §2-0의 원문으로 뒷받침된다. **둘을 섞어 쓰지 마라.**

- ✅ **"CDP"라는 용어의 최초 명명 시점: 2013년 4월 25일** — 1차 확인 완료
- David Raab이 CDP Institute의 **창립자**라는 사실 → `확인 불가 (1차 소스 미확보)`. 그가 CDP를 **명명한** 인물이라는 것만 확인됨.
- CDP Institute가 "Customer Data Alliance"를 병기하고 있을 가능성 → `확인 불가`

### 2-0-3. DMP / CRM / MA / CEM — 카테고리 비교축

> ⚠️ **이 표는 합성물이다.** 각 셀의 근거 등급이 다르다. **표 전체를 하나의 출처에서 온 것처럼 인용하지 마라.** `[web-gaps]`

| 축 | **CRM** | **DMP** | **CDP** | **MA** | **CEM/CXM** |
|----|---------|---------|---------|--------|-------------|
| **누구의 데이터인가** | 퍼스트파티 (자사가 입력) `[Trailhead 1차]` | 퍼스트파티 + **세컨드·서드파티 보강** `[Adobe AAM 1차]` | 퍼스트파티 `[Wikipedia — 신뢰성 중]` | 퍼스트파티 (방문자→prospect) `[Trailhead 1차]` | **확인 불가** |
| **식별 수준** | **식별된 개인/회사** (Account·Contact) `[Trailhead 1차]` | **확인 불가** — Adobe 문서에 익명/쿠키 언급 없음 | 확인 불가 (1차 미확보) | **익명 방문자 → 전환 시 식별된 prospect** `[Trailhead 1차]` | **확인 불가** |
| **주 용도** | **영업 파이프라인 관리** (Lead→Opportunity) `[Trailhead 1차]` | **광고 타겟팅·오디언스·look-alike** `[Adobe AAM 1차]` | 데이터 통합 + 외부 시스템에 노출 `[Raab 1차]` | **B2B 리드 너처링 + 스코어링 → 영업 인계** `[Trailhead 1차]` | **확인 불가** |
| **데이터를 남에게 열어 주는가** | ❌ `[Raab 2017 1차]` | ❌ `[Raab 2017 1차]` ⚠️벤더 자기규정과 충돌 | **✅ 이것이 CDP의 정의적 특징** `[Raab 1차]` | ❌ `[Raab 2017 1차]` | **확인 불가** |
| **메시지를 고르는가** | ✅ (영업 중심) | ✅ | ❌ | ✅ **행동·시간 간격으로 이메일 트리거** `[Trailhead 1차]` | **확인 불가** |
| **고유한 점수 체계** | — | — | — | **score(행동, 숫자) + grade(적합도, 문자)** `[Trailhead 1차]` | — |
| **등장 시점** | 확인 불가 | 확인 불가 | **2013년 4월 명명** `[Raab 원문 + Wikipedia 교차 확인]` ✅ | 확인 불가 | 확인 불가 |

> 🚨 **두 가지 금지:**
> 1. **CEM/CXM 열은 통째로 비어 있다** (Gartner 403). **이 카테고리를 책의 비교표에 넣지 마라.** 검색 요약이 제시한 Gartner 정의를 **Gartner에 귀속시켜 인용하지 마라.**
> 2. **"DMP = 서드파티 쿠키 기반, CDP = 퍼스트파티"라는 통설은 어떤 1차 소스로도 확인하지 못했다.** 검증 없이 쓰면 안 된다. Adobe Audience Manager 문서에는 익명/쿠키 언급이 없었다.
>
> ⚠️ **"등장 시점" 행은 CDP를 빼면 전부 확인 불가**다. 카테고리 연대기를 서술하려면 추가 리서치가 필요하다.

### 2-0-4. 🇰🇷 "CRM"이라는 세 글자가 한국과 영미권에서 다른 것을 가리킨다

**대상 독자(한국 개발자)에게 이번 리서치에서 가장 중요한 발견 중 하나다.** `[web-gaps]`

| | **영미권 "CRM"** [Salesforce Trailhead 1차] | **한국 "CRM 마케팅"** [노티플라이·FlareLane] |
|---|---|---|
| 핵심 대상 | **영업(sales)** — Lead → Opportunity 파이프라인 | **리텐션** — 기존 고객 재구매·재방문 |
| 주 사용자 | 영업사원 | 마케터(그로스) |
| 대표 행위 | 레코드 관리·상담 이력·딜 관리 | **메시지 발송** (푸시·알림톡·문자·이메일) |
| 핵심 객체 | Account / Contact / Lead / Opportunity | 세그먼트 / 캠페인 / 메시지 |
| 서구 대응 카테고리 | CRM | **오히려 MA·CEP에 가깝다** |

한국 벤더의 정의 (원문):
> CRM 마케팅이란 "고객이 자사 플랫폼(서비스)에 유입되었을때, 말을 걸고, 구매를 유도하고, 구매한 이후 재탐색을 유도하는 등, **리텐션을 높이는 모든 고객대상 마케팅**"
>
> 채널: "푸시, 모달(IAM), 카카오 알림톡, 카카오 친구톡, 문자 메시지, 이메일 - 총 6가지가 대표적인 매체"
>
> [blog.notifly.tech/crm-marketing-introduction/ | **2023-10-24** | 검색 시점 2026-07-25] · [blog.flarelane.co.kr/what-is-crm-marketing-concepts-strategies-and-common-mistakes/ | **2025-04-22**] `1차 확인`

> 🎯 **개발자 독자에게 이건 함정이다.** 한국 회사에서 "CRM 팀"이 요구사항을 들고 오면, 그들이 원하는 건 Salesforce가 아니라 **푸시·알림톡 발송 시스템**일 가능성이 높다. 같은 세 글자가 태평양을 건너면서 뜻이 바뀌었다. **카카오 알림톡이 채널 목록 상위에 오는 것 자체가 한국 시장 고유성의 증거다.**
>
> ⚠️ **신뢰성 등급 주의:** 두 출처 모두 **한국 martech 벤더의 자사 블로그**다. 업계에서 그 말이 그렇게 쓰인다는 *용법의 증거*로는 충분하지만 **중립적 정의로 인용하면 안 된다.** 책에는 **"국내 CDP/메시징 벤더들은 이 말을 …라는 뜻으로 쓴다"**는 형태로 쓸 것.

### 2-0-5. Martech 랜드스케이프 규모 — 2026년판

**15,505개** (전년 대비 +0.79%, 추가 1,488 / 제거 1,367)
[chiefmartec — 2026 Marketing Technology Landscape Supergraphic, Scott Brinker | **2026-05-05** | 검색 시점 2026-07-25] `1차 확인` `[web-gaps]`

> 🚨 **유사 수치 함정:** **15,384**라는 미검증 숫자가 함께 돌아다닌다. **fetch 확인된 15,505(2026년판)만 써라.**

### 2-1. 대신 확보한 것 — 벤더가 스스로 "CDP"라고 쓴 1차 문장 3건

정의 대신 "업계가 CDP라는 말을 어떻게 쓰는가"의 근거로는 쓸 수 있다.

| 벤더 | 원문 | 출처 |
|---|---|---|
| Adobe | "Use Adobe Real-Time Customer Data Platform (Real-Time CDP) to bring together known and anonymous data from multiple enterprise sources in order to create customer profiles that can be used to provide personalized customer experiences across all channels and devices in real time." | experienceleague.adobe.com/.../rtcdp/home (문서 표기 2026-06-18) |
| mParticle | "a customer data platform (CDP) that simplifies how you collect and connect your user data to hundreds of vendors without needing to manage multiple integrations." | docs.mparticle.com (문서 표기 "Last Updated: 7/16/2026") |
| Insider One | "the core Customer Data Platform (CDP) that powers all Insider One products" | academy.insiderone.com/docs/unified-customer-database-ucd (페이지 표기 2026-04-22) |

`1차 확인` `벤더 자체 주장` `[web-products]`

**세 문장의 공통 요소** (`관찰`, 인용 아님): ① 여러 소스의 데이터를 모은다 ② 고객 프로필/식별을 만든다 ③ 다른 시스템이 그걸 쓸 수 있게 한다. 세 벤더가 독립적으로 같은 세 가지를 말한다.

⚠️ 이건 **정의가 아니라 관찰**이다. "CDP의 정의는 다음과 같다"고 쓰려면 여전히 1차 정의 소스가 필요하다.

### 2-2. 패키지형 CDP vs 컴포저블/웨어하우스 네이티브 CDP

**이 대비가 개발자 독자에게 가장 중요한 개념 축이다.**

**Hightouch의 Composable CDP 정의** (`벤더 자체 주장`, 1차):

> "A Composable CDP is a customer data platform that enables you to use any data in your organization to power marketing use cases like audience management, journey orchestration, personalization, and data activation directly from your existing data infrastructure."
>
> [hightouch.com/blog/composable-cdp | 저자 Luke Kline, 발행 **2023-06-20** | 검색 시점 2026-07-25] ⚠️ **3년 경과 — 구버전 정보일 수 있음**

**제품 페이지의 더 날 선 주장** (`벤더 자체 주장`, 1차):

> "Don't copy your data to an incompatible and less secure data silo. Turn your existing data into a CDP instead."
> "Hightouch doesn't store your data. Instead we simply read from your data warehouse where it stays safe and sound."
>
> [hightouch.com/platform/composable-cdp | 발행일 미표기 | 검색 시점 2026-07-25]

> **개발자 관점 핵심 문장:** "패키지형 CDP는 데이터를 복사해 자기 저장소에 넣고, 컴포저블 CDP는 웨어하우스를 그대로 읽는다." — 이 한 문장이 두 갈래를 가른다.

⚠️ **온도 차 기록:** 위 강한 아키텍처 주장은 **마케팅 페이지에만** 있다. Hightouch 개발자 문서(`/docs/getting-started/concepts`)에는 해당 문장이 **없었다**. `[web-products]`

**컴포저블 CDP의 코어 개념 4종** (Hightouch 개발자 문서, 1차) — reverse ETL의 표준 멘탈 모델로 그대로 쓸 수 있다:

> **Source**: "A source is any system where your data resides. Common examples include Snowflake, BigQuery, Databricks, and PostgreSQL."
> **Model**: "A model defines what data to query from a source. Models can represent users, events, products, or any other entity."
> **Sync**: "A sync defines how data appears in the destination and when. Syncs specify: Type: object, event, audience, etc. Mode: insert, update, upsert, or archive Mapping: how source columns map to destination fields Schedule: interval, cron, or triggered by tools like dbt Cloud or Airflow"
> **Destination**: "A destination is any system where data is consumed — CRMs, ad platforms, support tools, analytics, or custom APIs."
>
> [hightouch.com/docs/getting-started/concepts | 페이지 표기 "Last updated Jul 17, 2026" | 검색 시점 2026-07-25] `1차 확인`

### 2-3. ⚠️ 시장 통합 — "Hightouch / Census / RudderStack 3강" 서술은 낡았다

**Fivetran → Census 인수** `1차 확인`:
- 발표일 **2025-05-01**
- Census 설명 (원문): "the leader in Reverse ETL, data activation, and operational analytics"
- 거래 조건: "Terms of the deal were not disclosed."
- [fivetran.com/press/fivetran-signs-agreement-to-acquire-census-... | 2025-05-01 | 검색 시점 2026-07-25]
- **`getcensus.com` 도메인이 `fivetran.com`으로 301 리다이렉트**되는 것을 2026-07-25에 확인했다.
- ⚠️ **다만 Census 브랜드·제품의 완전 소멸 여부는 `확인 불가`** — 리다이렉트만으로 단종을 단정할 수 없다.

**Rokt × mParticle 합병** `1차 확인` (부분):
- 금액 **"$300 million merger"** (원문 표기) — 1차 확인
- **발표일은 이 페이지에서 NOT FOUND.** 검색 요약은 2025년 1월이라 하나 **1차 미확인** → 날짜를 쓰려면 재확인
- `developer.mparticle.com` → **DNS ENOTFOUND** (구 개발자 도메인 소멸). 단 `docs.mparticle.com`은 살아 있고 2026-07-16 갱신 표기
- [mparticle.com/news/rokt-and-mparticle-merge/ | 발행일 미표기 | 검색 시점 2026-07-25]

> **관찰:** 두 인수의 결과가 다르다. Census는 브랜드가 흡수된 것으로 보이고, mParticle은 브랜드·문서를 유지하며 여전히 자기를 "a customer data platform (CDP)"로 규정한다. `[web-products]`

### 2-4. 카테고리 경계가 왜 흐릿한가 — 문서 대조로 직접 관찰된 5가지

애널리스트·벤더의 공개 논평 텍스트는 확보하지 못했다(`확인 불가`). 대신 **20개 벤더 문서를 열어 직접 관찰한 것**을 기록한다. 책에서는 "문서를 열어보면 이렇다"는 형태로 써야 한다. `관찰` `[web-products]`

1. **한 회사가 두 카테고리를 동시에 주장한다.** Insider One은 회사 차원에서 "Agentic Customer Engagement Platform"(insiderone.com), 제품 문서에서는 자사 UCD를 "the core Customer Data Platform (CDP)"라 부른다. → CEP 안에 CDP가 모듈로 들어있는 구조.
2. **CDP라는 이름이 서로 다른 아키텍처를 가리킨다.** Hightouch는 "never copies your data"를 차별점으로 내세우고, Insider UCD는 이벤트·속성을 자기 DB에 저장한다. 둘 다 CDP라 불린다.
3. **인접 카테고리가 CDP 쪽으로 이동한다.** ETL 회사(Fivetran)가 Reverse ETL 회사(Census)를 인수했고(2025-05-01), 커머스 광고 회사(Rokt)가 CDP(mParticle)를 $300M에 합쳤다.
4. **같은 일에 다른 라벨을 붙인다.** 확인된 자기 라벨: "Customer Data Platform"(Adobe·mParticle·Insider UCD), "Customer Engagement Platform"(Insider 회사 차원), **"Customer retention platform"(CleverTap)**, **"omnichannel messaging"(OneSignal)**, "마테크 솔루션"(그루비), "CRM 자동화"(빅인).
5. **CDP는 CEP의 부품이기도 하고 경쟁자이기도 하다.** Airship은 CDP를 "파트너 연동" 목록(analytics, CRMs, **CDPs**, marketing tools)에 넣는다 — 데이터 공급자로 본다. 반면 Insider·Adobe는 CDP를 자기 안에 내장한다.

> **가장 인상적인 통계 (`관찰`):** 문서를 연 **20개 벤더 중 자기 카테고리를 문서 첫 페이지에 명시한 것은 4개뿐**(Insider·Adobe RTCDP·mParticle·CleverTap). **카테고리는 개발자 문서가 아니라 세일즈 자료에 산다.**

### 2-5. CDP/CEP vs 어트리뷰션(MMP) — API 카탈로그가 카테고리를 가른다

마케팅 문구 없이 카테고리를 구분하는 가장 좋은 방법. `관찰` `[web-products]`

| | CDP/CEP (Insider·Braze·mParticle) | 어트리뷰션 (AppsFlyer·Adjust·Airbridge) |
|---|---|---|
| 핵심 API | Upsert User / Track Users / Events API | **Attribution Result**, Tracking Link, SKAdNetwork Config |
| 리포트 API | 캠페인 분석 | **Actuals / Revenue / Retention / ROAS Report** |
| 존재 이유 | 프로필을 만들고 메시지를 보낸다 | **어느 광고가 이 설치·전환을 만들었는지 귀속(attribute)한다** |

Airbridge에만 `Attribution Result` API가 있고 Insider에는 없다. Insider에만 `Send Transactional Emails`가 있고 Airbridge에는 없다.

⚠️ **"어트리뷰션 제품은 CDP/CEP와 다르다"를 벤더가 스스로 선언한 문장으로는 확보하지 못했다.** 위 표는 각 벤더 문서에서 확인한 API 이름을 재배열한 것이다. 각 항목의 **존재**는 사실이지만, **"없다"는 진술은 이 세션에서 조회한 페이지 범위 안에서만** 유효하다.

### 2-6. Adobe 사례 — CDP와 CEP의 관계가 가장 명료하게 드러난다

> **Adobe Journey Optimizer** 정의: "An enterprise application for creating and delivering connected, contextual, and personalized customer experiences across all channels and touchpoints."
>
> AEP와의 관계 (원문): "is built natively on Adobe Experience Platform, sharing its data foundation, identity graph, and governance services."
>
> [experienceleague.adobe.com/en/docs/journey-optimizer/using/get-started/get-started | 문서 표기 "Last updated July 1, 2026" | 검색 시점 2026-07-25] `1차 확인`

**Real-Time CDP = 데이터 기반(프로필·아이덴티티 그래프), Journey Optimizer = 그 위에서 저니를 실행하는 애플리케이션. 둘이 같은 데이터 기반을 공유한다.** 이 분리가 Insider(UCD + Architect), Braze(users + Canvas)에서도 같은 형태로 반복된다. `관찰`

### 2-7. 20개 벤더 대조표 (요약)

| 벤더 | 문서에서 확인한 자기 규정 | 개발자 표면 | 문서 URL |
|---|---|---|---|
| Insider One | "Agentic Customer Engagement Platform" / UCD는 "the core CDP" | ins.js 태그, `InsiderQueue`, Upsert/Get/Export/Delete API, iOS·Android·Flutter SDK | academy.insiderone.com |
| Adobe Real-Time CDP | "bring together known and anonymous data ... in real time" | XDM 스키마, Individual Profile / ExperienceEvent | experienceleague.adobe.com |
| Adobe Journey Optimizer | "An enterprise application for creating and delivering..." | AEP 위에 네이티브 | experienceleague.adobe.com |
| mParticle (by Rokt) | "a customer data platform (CDP)" | Events API(HTTP/Node/Python/Ruby), Profile API, Firehose API, **IDSync** | docs.mparticle.com |
| Twilio Segment | NOT FOUND | Spec(identify/track/page/screen/group/alias) | segment.com/docs (**403**) |
| Bloomreach Engagement | NOT FOUND | Customers/Events/Catalogs, hard/soft ID, REST + Webhook + **Kafka** | documentation.bloomreach.com |
| Braze | NOT FOUND | "high-performance REST API", Track users endpoint, User attributes object | braze.com/docs |
| MoEngage | "Engage your users with intelligent, cross-channel experiences" | ingestion/campaigns/segments/templates 엔드포인트, SDK 6종 | moengage.com/docs |
| CleverTap | **"Customer retention platform"** | Upload Events, Upload User Profiles / SDK 9종(**KaiOS·Unreal 포함**) | developer.clevertap.com |
| OneSignal | **"omnichannel messaging"** | REST API, Webhooks / Push·Email·SMS&RCS·In-app·Live Activities | documentation.onesignal.com |
| Airship | NOT FOUND | REST(messaging/audience/**event streaming**/wallet), Open Channel API | airship.com/docs |
| Klaviyo | NOT FOUND | **JSON:API**, 날짜 버저닝(v2026-07-15), Profiles/Events/Lists/Segments/Campaigns/Flows | developers.klaviyo.com |
| AppsFlyer | (카테고리 라벨 아님) | "attribution out-of-the-box", S2S events API, Click Signing API | dev.appsflyer.com |
| Adjust | NOT FOUND | Attribution info, ad revenue, subscription, uninstall/reinstall 측정 / SDK 14종 | dev.adjust.com |
| Airbridge (AB180) | NOT FOUND (제품: "Web + app attribution", "ROAS measurement") | Tracking Link, S2S Event, **Attribution Result**, SKAdNetwork Config, Raw Data Export | help.airbridge.io |
| 채널톡 | NOT FOUND | Open API, Webhook, Snippet, TTS / JS·iOS·Android·RN SDK | developers.channel.io |
| 그루비 (Plateer) | **"비즈니스 성공을 위한 필수 마테크 솔루션"** | 스크립트·SDK 설치, "그루비 API" (상세는 어드민 내부) | groobee.net (저작권 표기 2023) |
| 빅인 (biginsight) | NOT FOUND ("개인화된 CRM 자동화") | **카페24 API 연동** (공개 개발자 문서 확인 불가) | bigin.io |
| 다이티 (NHN DATA) | **확인 불가** | 확인 불가 | dighty.com (**TLS 인증서 불일치**) |
| Salesforce Data Cloud / Iterable | **확인 불가** (404 / 403) | 확인 불가 | — |

`1차 확인` `[web-products]`

> **한국 독자에게 중요한 관찰:** **한국 벤더 3곳(그루비·빅인·다이티) 모두 공개 개발자 문서를 확인하지 못했다.** 글로벌 벤더는 문서를 공개 자산으로 운영하고, 한국 벤더는 계약·어드민 뒤에 둔다. **이 차이가 개발자로 입사할 때 체감하는 첫 문화 차이일 가능성이 높다.** `관찰`

### 2-8. Klaviyo — API 진화 방식의 대조 사례

- **날짜 기반 버저닝.** 문서에 노출된 버전: `v2022-10-17`, `v2023-01-24`, `v2023-06-15`, `v2024-02-15`, `v2024-10-15`, `v2025-01-15`, **`v2026-07-15`(조회 시점 최신)**
- **레이트 리밋 (원문):** "fixed-window rate limiting algorithm with two distinct windows: burst (short) and steady (long)" — 초과 시 HTTP 429
- API 스타일: **JSON:API** 규약, `relationships` 객체 사용
- [developers.klaviyo.com/en/reference/api_overview | **API 버전 v2026-07-15 기준** | 검색 시점 2026-07-25] `1차 확인`

> Klaviyo의 날짜 버저닝 + burst/steady 이중 리밋 창은 Insider(단일 분당 리밋, §6-4)와 대조하기 좋은 1차 사례다.

---

## 3. 마케팅 원리 (학술·업계 근거)

> **확인 수준 규약** (`research/papers.md` 기준 — fact-checker 필독):
> - `초록 확인` — 초록 전문을 실제로 읽었다. **직접 인용 가능.**
> - `메타데이터 확인` — Crossref/Semantic Scholar/arXiv의 권위 있는 서지 레코드(제목·저자·연도·발표처·DOI)를 확인했으나 **초록 본문은 못 봤다. 구체 수치를 이 논문에 귀속시키지 마라.**
> - `학술 근거 확인 불가` — **업계 관행이다. 그렇게 표기하라.**
>
> 조회 경로: Crossref API, arXiv API, Semantic Scholar Graph API, 개별 랜딩 페이지. **저자·연도·DOI·arXiv ID는 전부 2026-07-25 세션에서 실제 조회한 응답에서 복사했다.**

### 3-A. 🎯 이 책의 차별점 — "학술 근거 없음 / 업계 관행" 12건

> **이 목록 자체가 이 책의 가치다.** 업계가 학술적 권위인 양 쓰는 것들이 실제로 어디서 끊기는지 보여준다. `papers.md` 최종 판정.

| # | 항목 | 실제 출처 |
|---|---|---|
| 1 | **LTV:CAC 3:1** | SaaS 투자자 경험칙. **이 값이 최적이라는 실증 연구 없음** |
| 2 | **Gamma-Gamma 지출 모델** | brucehardie.com **미간행 노트** (`lifetimes` 라이브러리가 구현하는 대상) |
| 3 | **Send-time optimization** | 최상위 저널 검증 없음. ⚠️ **단 발송 빈도/피로도에는 근거 있음**(§3-J) |
| 4 | **Lambda 아키텍처** | Marz & Warren, *Big Data* (Manning, 2015) — **책** |
| 5 | **Kappa 아키텍처** | Jay Kreps, O'Reilly Radar **2014 블로그 글** |
| 6 | **Feature store** | 학술 정전 부재. 가장 가까운 대응물은 TFX + Sculley 기술부채 논문 |
| 7 | **Meridian / Robyn의 학술 계보** | Google 사내 기술보고서 + 베이지안 교과서 |
| 8 | **Google 지오 실험 방법론** | Google 기술보고서 |
| 9 | **상시 홀드아웃 / universal control** | 독립 정전 논문 미확인 |
| 10 | **Kafka 원 논문** | NetDB'11 **워크숍**, **DOI 없음, Crossref 레코드 부재** |
| 11 | **RFM의 기원** | 1차 학술 문헌 확인 불가 — **"19XX년 누가 만들었다" 단정 금지** |
| 12 | **DMARC를 "표준"이라 부르는 것** | RFC 7489는 **Informational** (§3-J) |

> 🚨 **서지 함정 2건 (검증 파이프라인이 실제로 잡아낸 것):**
> - **Theta Sketch 저자** — 널리 도는 "Dasgupta, Lang, **Stokes, Tirthapura**"는 **틀렸다.** 실제는 Dasgupta, Lang, **Rhodes, Thaler** (§4-5)
> - **C-Store 원본 DOI 부재** — 검색으로 나오는 `10.1145/3226595.3226638`은 **2018년 기념 논문집 재수록본**이다. 원본인 것처럼 쓰지 마라.

#### 아래 셋은 챕터 소재로 특히 강하다

> **이 구분 자체가 이 책의 가치다.** 업계가 학술적 권위인 양 쓰는 것들이 실제로 어디서 끊기는지 보여준다.

**① LTV/CAC 3:1 — 학술 근거 없음** ⭐
> 이번 세션에서 **3:1 비율을 지지하는 peer-reviewed 연구를 찾지 못했다.** 이 규칙은 SaaS 투자자·운영자 커뮤니티(특히 David Skok 계열 SaaS 메트릭 글)에서 확산된 rule of thumb으로 반복 서술된다.
>
> **저술 권고:** "LTV:CAC 3:1은 **학술적으로 검증된 임계값이 아니라 VC/SaaS 업계의 경험칙**이다. 정당화 논리(생애가치의 1/3까지 획득에 써도 마진과 성장 여력이 남는다)는 있지만, **이 숫자가 최적이라는 실증 연구는 확인되지 않는다**"고 명시하라.

**② Gamma-Gamma 지출 모델 — peer-review 논문이 아니다** ⭐
> Bruce Hardie, "The Gamma-Gamma Model of Monetary Value," **미간행 기술 노트**, brucehardie.com Note #25, 최종 갱신 2013-02-25.
> [brucehardie.com/notes/025/ | 검색 시점 2026-07-25] `초록 확인 (랜딩 페이지 조회 — 저널 게재 논문이 아님을 확인)`
>
> 🎯 **정직성 포인트:** `lifetimes.GammaGammaFitter`가 구현하는 대상이 저널 논문이 아니라 **저자 개인 웹사이트의 PDF 노트**다. **마테크 스택의 "학술적 권위"가 어디쯤에서 끊기는지 보여주는 최고의 사례.**

**③ 홀드아웃 그룹 설계 / 코호트 리텐션 커브 형태 — 정전 논문 미특정**
> 상시 홀드아웃(global holdout / universal control)은 실무에서 널리 쓰이지만 **정식화한 독립 학술 논문을 특정하지 못했다.** 통제 실험 일반론(Kohavi 계열)에서 정당화해야 한다.
> "코호트 리텐션 커브가 멱법칙/로그 형태로 안정화된다"는 실무 서술도 **정전 논문 미특정 — `확인 불가`.**

> ⚠️ **RFM 기원 경고:** RFM 용어가 1960~70년대 미국 다이렉트 마케팅 업계에서 나왔다는 서술이 널리 퍼져 있으나 **기원을 확정하는 1차 문헌을 확인하지 못했다. "RFM은 19XX년 누가 만들었다"고 단정하지 마라.**

### 3-B. RFM과 CLV/LTV

**RFM은 이론이 아니라 실무 휴리스틱이다.**
- **Bult & Wansbeek (1995)**, "Optimal Selection for Direct Mail," *Marketing Science* 14(4), 378–394. DOI `10.1287/mksc.14.4.378` `메타데이터 확인`
  → RFM류 휴리스틱 대신 응답 확률 모형 기반 선택 규칙을 제시한 초기 정전. **학계는 애초부터 RFM을 최적화 문제로 대체하려 했다.**
- **Fader, Hardie & Lee (2005)**, "RFM and CLV: Using Iso-Value Curves for Customer Base Analysis," *JMR* 42(4), 415–430. DOI `10.1509/jmkr.2005.42.4.415` `메타데이터 확인`
  → 서로 다른 RFM 조합이 같은 CLV를 갖는 **등가치 곡선(iso-value curve)**. **"RFM은 CLV의 저차원 프록시"**라는 서술의 근거.

> 🎯 **개발자에게:** RFM 세그먼트를 구현할 때 **"최적이라서 쓰는 게 아니라 싸고 설명 가능해서 쓴다"**는 걸 알고 써야 한다. (§3-N의 Insider가 2026년에도 RFM Segments 문서를 별도로 두고 있다는 사실과 연결하면 강한 대목이 된다.)

**CLV 확률 모형 계열:**
- **Schmittlein, Morrison & Colombo (1987)** — Pareto/NBD 원 논문 ⭐. "Counting Your Customers: Who-Are They and What Will They Do Next?," *Management Science* 33(1), 1–24. DOI `10.1287/mnsc.33.1.1` · 피인용 687 (Semantic Scholar) `메타데이터 확인`
  > 🎯 **비계약형 관계에서 고객은 "탈퇴 버튼"을 누르지 않는다 — 그냥 조용히 안 온다.** 그래서 이탈을 **관측 라벨이 아니라 잠재 변수**로 다뤄야 한다. **CDP에서 "휴면 고객" 플래그를 만들 때 무엇을 가정하는지 정확히 설명해준다.**
- **Fader, Hardie & Lee (2005)** — BG/NBD. *Marketing Science* 24(2), 275–284. DOI `10.1287/mksc.1040.0098` · 피인용 501 `메타데이터 확인`
  > **`lifetimes`·`PyMC-Marketing`의 `BetaGeoFitter`가 바로 이 모델이다.** 라이브러리를 쓰기 전에 **"이탈은 구매 직후에만 발생한다"는 가정**을 알아야 한다 — 이 가정이 깨지는 도메인에서 결과가 이상해진다.
- **Fader, Hardie & Shang (2010)** — BG/BB(이산 시간). *Marketing Science* 29(6), 1086–1108. DOI `10.1287/mksc.1100.0580` `메타데이터 확인`
  > 데이터 그레인에 따라 **다른 모델을 골라야 한다**는 반례. 하나의 LTV 모델을 전 제품에 붙이려는 유혹을 깬다.
- **Gupta et al. (2006)** — CLV 서베이. *Journal of Service Research* 9(2), 139–155. DOI `10.1177/1094670506293810` `메타데이터 확인`
  > **"LTV 계산식 알려줘"에 단일 답이 없는 이유**를 권위 있게 설명한다. CLV는 하나의 공식이 아니라 **문제 설정에 따라 갈리는 모델 패밀리**다.
- **Braun & Schweidel (2011)** — 경쟁 위험(competing risks). *Marketing Science* 30(5), 881–902. DOI `10.1287/mksc.1110.0665` `메타데이터 확인`
  > 🎯 **`churn = 1` 이진 라벨로 뭉개는 관행의 한계.** 자발적 해지 / 결제 실패 / 이사는 원인이 다르면 대응도 달라야 한다. **결제 실패 이탈에 리텐션 캠페인을 쏘는 건 무의미하다 — 카드 갱신 플로우가 답이다.**

> **코호트·리텐션·생존 분석의 학술적 뿌리는 위 확률 모형 계열과 사실상 같다.** 비계약형에서는 Pareto/NBD·BG/NBD가 곧 생존 모형 역할을 한다(잠재 생존 시간).

### 3-C. 개인화 — 효과와 역효과

> 🎯 **이 소절이 §4-9(AI/ML)와 §8(논쟁)을 잇는 핵심이다. "개인화를 세게 할수록 좋아진다"는 선형 가정이 실증적으로 깨진다.**

**Goldfarb & Tucker (2011)** — 개인화 역효과의 대표 실증 ⭐
*Marketing Science* 30(3), 389–404. DOI `10.1287/mksc.1100.0583` · 피인용 814 `초록 확인`

> "Ads that match both website content and are obtrusive do worse at increasing purchase intent than ads that do only one or the other. This failure appears to be related to privacy concerns: the negative effect of combining targeting with obtrusiveness is strongest for people who refuse to give their income and for categories where privacy matters most."

> 🚨 **범위 한정 — 반드시 함께 쓸 것:** 종속변수는 **구매 의향(purchase intent)**이지 실제 매출이 아니다. 매체는 **온라인 디스플레이 광고**다. **"개인화는 역효과다"로 일반화하지 마라.**

- **White et al. (2007/2008)** — 개인화 리액턴스. "Getting too personal: Reactance to highly personalized email solicitations," *Marketing Letters* 19, 39–50. DOI `10.1007/s11002-007-9027-9` `메타데이터 확인`
  ⚠️ **연도 주의:** Crossref는 issued를 **2007**로 반환했으나 해당 권은 통상 2008로 인용된다. **`(2007/2008)`로 쓰고 단정 표기를 피하라.**
  > **왜 "어제 보신 그 상품, 아직 고민 중이시죠?" 같은 카피가 역효과를 내는지**를 설명하는 학술 언어.
- **Tucker (2013/2014)** — 프라이버시 통제권과 개인화 광고. *JMR*. DOI `10.1509/jmr.10.0355` `메타데이터 확인` ⚠️ **서지 상충**
  ⚠️ Crossref에 상충하는 두 레코드가 존재한다(Vol.51 vs Vol.50, 둘 다 issued 2013). **DOI `10.1509/jmr.10.0355`를 쓰고 권/연도는 fact-checker가 출판사 페이지로 재확인할 것.**
  > 🎯 **소셜 네트워크가 이용자에게 프라이버시 통제권을 더 준 이후 개인화 광고의 성과가 오히려 올라갔다.** **"동의·통제 UI는 마케팅 성과의 비용"이라는 가정에 대한 반례** — §5의 동의 설계 논의와 직결된다.
- **Awad & Krishnan (2006)** — 개인화-프라이버시 역설. *MIS Quarterly* 30(1), 13–28. DOI `10.2307/25148715` `메타데이터 확인`
  > **CDP를 만들며 "동의를 받으면 되지 않나"라고 생각하는 개발자에게 선언된 선호와 실제 행동이 어긋난다는 걸 보여준다.**
- **Ansari & Mela (2003)** — 이메일 콘텐츠 개인화의 초기 실증. (상세는 `papers.md` D-5-1)

### 3-D. 추천 시스템 — 가장 중요한 논문은 회의론이다

**Ferrari Dacrema, Cremonesi & Jannach (2019)** — "정말 진전이 있었나?" ⭐⭐
*RecSys 2019*. arXiv:**1907.06902** (v3). DOI `10.1145/3298689.3347058` · 피인용 686 `초록 확인`

> "Specifically, we considered 18 algorithms that were presented at top-level research conferences in the last years. Only 7 of them could be reproduced with reasonable effort. For these methods, it however turned out that 6 of them can often be outperformed with comparably simple heuristic methods, e.g., based on nearest-neighbor or graph-based techniques."

**핵심 수치:** 최상위 학회 신경망 추천 알고리즘 **18개** 중 재현 가능한 것은 **7개**뿐, 그 7개 중 **6개는 최근접 이웃·그래프 기반 단순 휴리스틱에 자주 능가당했다.**
코드 공개: `github.com/MaurizioFD/RecSys2019_DeepLearning_Evaluation`

> 🎯 **이 책에서 가장 중요한 논문 중 하나.** **"우리도 딥러닝 추천을 도입해야 하나?"에 대해 "잘 튜닝된 단순 베이스라인부터 세우라"는 답을 학술적 권위로 뒷받침한다.** §4-9의 "Martech의 AI는 대부분 LLM이 아니다"와 짝을 이룬다.

- **Rendle et al. (2020)** — "Neural Collaborative Filtering vs. Matrix Factorization Revisited," arXiv:**2005.09683** `메타데이터 확인`
  > D-6-7과 함께 **베이스라인 튜닝의 중요성**을 보여준다. **제1저자 Steffen Rendle은 Factorization Machines 창시자라 반박의 무게가 다르다.**
- **Covington, Adams & Sargin (2016)** — YouTube 2단계 아키텍처. *RecSys 2016*, 191–198. DOI `10.1145/2959100.2959190` `메타데이터 확인`
  > 🎯 **후보 생성(candidate generation) → 랭킹(ranking)** 2단계 산업 표준. **§4-9의 토스 3단 파이프라인(Targeting → Filtering → Ranking)이 정확히 이 구조다** — 학술 정전과 국내 실무 사례가 만나는 지점.
- 계보: **Linden, Smith & York (2003)** 아이템 기반 CF / **Koren, Bell & Volinsky (2009)** 행렬 분해 / **He et al. (2017)** NCF / **Hidasi et al. (2015)** GRU4Rec / **Kang & McAuley (2018)** SASRec / **Sun et al. (2019)** BERT4Rec — 상세 서지는 `papers.md` D-6.

### 3-E. CTR / 전환 예측

- **McMahan et al. (2013)** — FTRL, "Ad Click Prediction: a View from the Trenches" ⭐ `papers.md` D-7-1
- **He et al. (2014)** — GBDT 피처 + 로지스틱 회귀 (Facebook)
- **Juan et al. (2016)** — Field-aware Factorization Machines
- **Cheng et al. (2016)** — Wide & Deep ⭐
- **Guo et al. (2017)** — DeepFM / **Zhou et al. (2017)** DIN / **Zhou et al. (2018)** DIEN

> 🎯 **§4-9의 토스 사례가 "FM, DeepFM, DCN 구조로 eCPM 산출"이라고 밝힌 것**과 이 계보가 정확히 대응한다. **학술 논문 → 국내 프로덕션이라는 경로를 개발자에게 보여줄 수 있다.**

### 3-F. A/B 테스트와 온라인 실험 — 마테크 대시보드가 조장하는 오류

**Kohavi et al. (2009)** — 이 축의 첫 인용으로 쓰라 ⭐
"Controlled experiments on the web: survey and practical guide," *Data Mining and Knowledge Discovery* 18, 140–181. DOI `10.1007/s10618-008-0114-1` `메타데이터 확인`
(선행 학회 버전: *KDD 2007*, 959–967. DOI `10.1145/1281192.1281295`)
⚠️ Crossref issued는 **2008**, 통상 `(2009), DMKD 18: 140–181`로 인용된다.
> 통계적 기초 + 흔한 함정(SRM, 계측 오류, Simpson's paradox) + 조직 운영 원칙. **마테크 툴의 "실험" 탭이 무엇을 계산하는지, 왜 결과를 믿으면 안 되는 경우가 많은지의 표준 레퍼런스.**

**Johari et al. (2017/2022)** — 피킹(peeking) 문제 ⭐
*KDD 2017*, 1517–1525. DOI `10.1145/3097983.3097992` / 저널 확장판 "Always Valid Inference: Continuous Monitoring of A/B Tests," *Operations Research* 70(3), 1806–1821, 2022. DOI `10.1287/opre.2021.2135` `메타데이터 확인`

> 고정 표본 크기를 전제한 p-값을 **실험 진행 중 반복해서 들여다보고 유의해지면 멈추는** 관행은 1종 오류율을 크게 부풀린다.

> 🚨 **이 책에 가장 실용적인 대목:** **마테크 대시보드는 실시간으로 유의성을 보여준다. 그 UI가 조장하는 행동이 바로 피킹이다.** 실험 플랫폼을 만든다면 **순차 검정(always valid inference)을 기본값으로 삼으라**는 근거.

- **Benjamini & Hochberg (1995)** — FDR 다중 검정 보정. *JRSS-B* 57(1), 289–300. DOI `10.1111/j.2517-6161.1995.tb02031.x` `메타데이터 확인`
  > 🎯 **캠페인 하나에 지표 20개를 붙이고 "뭐라도 유의하면 성공"이라 보고하는 관행**이 왜 위험한지의 표준 레퍼런스.
- **Deng et al. (2013)** — CUPED(분산 축소). *WSDM 2013*, 123–132. DOI `10.1145/2433396.2433413` `메타데이터 확인`
  > **"표본이 부족해서 실험을 못 한다"**는 제약에 대한 구체적 해법. **캠페인 대상 수가 원래 적은 마테크 실험에서 특히 중요하다.**
- **Eckles, Karrer & Ugander (2016/2017)** — 네트워크 간섭(SUTVA 위반). *Journal of Causal Inference* 5. DOI `10.1515/jci-2015-0021` `메타데이터 확인`
  > **A그룹의 변화가 B그룹으로 새어나간다.** 마테크에서는 **"친구 초대", "공유 쿠폰", 재고 공유 마켓플레이스**에서 실제 문제가 된다.
- **Saveski et al. (2017)** — 네트워크 효과 탐지. *KDD 2017*, 1027–1035. DOI `10.1145/3097983.3098192` `메타데이터 확인`
  > **간섭이 있는지 없는지를 가정하지 말고 측정하라**는 실용적 처방.
- **Kohavi et al. (2012)** "Trustworthy online controlled experiments" (*KDD 2012*, DOI `10.1145/2339530.2339653`) — **실험 결과가 틀리는 방식을 카탈로그화한 논문. "숫자가 나왔으니 맞겠지"를 깨는 데 쓴다.**
- **Kohavi et al. (2013)** "Online controlled experiments at large scale" (*KDD 2013*, DOI `10.1145/2487575.2488217`) — 사내 실험 플랫폼 설계의 근거.

### 3-G. 저니 오케스트레이션

- **Lemon & Verhoef (2016)** — 고객 여정의 학술적 정의 ⭐ (`papers.md` D-4-1)
- **Anderl et al. (2016)** — 그래프/마르코프 기반 저니 어트리뷰션 (`papers.md` D-4-2)

### 3-H. 어트리뷰션 — "라스트터치는 안 쓰느니만 못하다"

**Berman (2018)** — 라스트터치는 광고주 이익을 **깎는다** ⭐⭐
"Beyond the Last Touch: Attribution in Online Advertising," *Marketing Science* 37(5), 771–792. DOI `10.1287/mksc.2018.1104` · 피인용 135 `초록 확인`

> "Our analysis of a common attribution method known as last-touch shows that it reduces advertiser profits compared to not using attribution at all, and that stronger advertisers suffer from a misallocation of consumer impressions due to overbidding for ads resulting from the attribution process. Our analysis of an attribution scheme based on the Shapley value shows that it will improve the profits of advertisers when conversion rates in the market are not too high."

> 🎯 **"라스트터치는 부정확하다" 정도가 아니라 "라스트터치를 쓰면 아예 안 쓰느니만 못하다"는 훨씬 강한 주장이다.** Shapley value가 왜 마테크 어트리뷰션 문서에 계속 등장하는지의 근거이기도 하다.
>
> 🚨 **범위 한정:** 이론 모델 + 분석적 결과다(대규모 관측 데이터 실증이 아니다). Shapley의 개선 효과에는 **"시장 전환율이 너무 높지 않을 때"**라는 조건이 붙는다 — **이 조건을 빼고 인용하지 마라.**

**MMM (미디어 믹스 모델링):**
- **Jin, Wang, Sun, Chan & Koehler (2017)** — 베이지안 MMM ⭐ `초록 확인` **(단, peer-reviewed 아님 — Google 기술 보고서)**
  > **초록이 밝힌 한계가 이 논문의 진짜 가치다:** 데이터가 클 때는 잘 추정되지만 **표본이 작으면 사전분포가 사후에 큰 영향을 주고 편향된 추정으로 이어진다.** 실제 광고주 데이터에서 **모델 기반 최적 미디어 믹스는 파라미터 추정의 분산 때문에 그 자체의 분산이 크다.**
- **Chen et al. (2018)** — 유료 검색의 MMM 편향 보정
- **Google Meridian** — 오픈소스 MMM의 방법론 계보 `초록 확인 (문서 페이지)`. ⚠️ 개별 Google 보고서는 **제목·저자·연도만 확인, 원문 미조회**
- **Runge, Skokan, Zhou & Pauwels (2024)** — Meta Robyn의 학술적 소개
- **Vaver & Koehler (2011)** — 지오 실험 `초록 확인` **(기업 기술 보고서)**
- **Anderl et al. (2016)** — 마르코프 제거 효과

### 3-I. 🎯 증분성 — 이 책에서 가장 강력한 정량 근거

**Blake, Nosko & Tadelis (2015)** — eBay 검색광고 실험 ⭐⭐
*Econometrica* 83(1), 155–174. DOI `10.3982/ecta12423` (NBER WP No. 20171, 2014. DOI `10.3386/w20171`) `초록 확인 (NBER 페이지)`

- **브랜드 키워드 광고는 측정 가능한 단기 효익이 없었다** ("brand-keyword ads have no measurable short-term benefits") — 이미 eBay를 찾아온 사람이 광고를 클릭했을 뿐이다.
- **비브랜드 키워드**에서는 **신규·저빈도 고객이 광고에 긍정적으로 반응**했다.
- 그러나 광고비 대부분이 **광고가 없어도 구매했을 기존·상시 이용자**에게 지출되어 **전체 평균 수익률은 마이너스**였다.

> 🚨 **오인용 경고 — 반드시 지킬 것:** 이 연구는 **"온라인 광고는 효과 없다"가 아니다.** 정확히는 ①브랜드 키워드 검색광고에 단기 효과가 없었고 ②비브랜드에서는 신규·저빈도 고객에게 효과가 있었으나 ③지출이 효과 없는 기존 고객 쪽에 몰려 평균 수익률이 음수였다는 것이다. **"eBay라는 이미 강한 브랜드의 검색광고"라는 맥락도 함께 말해야 한다.**

**Gordon, Moakler & Zettelmeyer (2023)** — "Close Enough?" ⭐⭐ **이 책에서 가장 강력한 정량 근거**
*Marketing Science* 42(4), 768–793. DOI `10.1287/mksc.2022.1413` · arXiv:**2201.07055** · 피인용 65 `초록 확인 (arXiv 초록 전문)`

Facebook **대규모 실험 663건** + **5,000개 이상의 사용자 수준 피처**로 두 비실험 방법(DML, SPSM)을 평가:

| 퍼널 | **RCT 실제 리프트** | DML 추정 | SPSM 추정 |
|---|---|---|---|
| 상단 | **29%** | 83% | 173% |
| 중단 | **18%** | 58% | 176% |
| 하단 | **5%** | 24% | 64% |

> "The median RCT lifts are 29%, 18%, and 5% for the upper, middle, and lower funnel outcomes, respectively. Using DML (SPSM), the median lift by funnel is 83% (173%), 58% (176%), and 24% (64%), respectively, indicating significant relative measurement errors."
>
> "Overall, despite having access to large-scale experiments and rich user-level data, **we are unable to reliably estimate an ad campaign's causal effect.**"

> 🎯 **하단 퍼널 실제 리프트가 5%인데 관측 기반 방법은 24~64%로 보고했다 — 5배에서 13배 과대추정이다.**
> **"그냥 데이터가 더 많으면 되지 않나?"라는 개발자의 직관을, 5,000개 피처와 663개 실험을 쓰고도 안 됐다는 사실로 반박한다.** §7-4의 커뮤니티 인용("각 광고 채널이 같은 전환을 각자 자기 것이라 주장한다")에 대한 **학술적 정량 뒷받침**이다.

- **Gordon, Zettelmeyer, Bhargava & Chapsky (2019)** — *Marketing Science* 38(2), 193–225. DOI `10.1287/mksc.2018.1135` · 피인용 291 `초록 확인 (요약본만)`
  > "Observational methods often fail to accurately recover the treatment effects generated from randomized advertising experiments on Facebook."
  > 🚨 **인용 주의:** 위 문장은 저널이 제공하는 **한 줄 요약**이며 초록 전문이 아니다. **이 논문에 구체적 수치를 귀속시키지 마라.** 수치가 필요하면 위 D-10-3(2023)을 쓰라.
- **Johnson, Lewis & Nubbemeyer (2017)** — 고스트 광고(Ghost Ads). §3-A의 홀드아웃 설계 근거로 연결된다.

> 🎯 **§8 논쟁 2(어트리뷰션은 유용한가 자기기만인가)의 학술적 판정은 여기서 온다.** 커뮤니티의 "85%를 목표로 하라"는 휴리스틱과 이 정량 근거를 나란히 놓으면, **"어트리뷰션 숫자는 방향 지시등이지 계기판이 아니다"**라는 챕터 결론을 근거 있게 쓸 수 있다.

### 3-J. 발송 빈도·피로도와 딜리버러빌리티 — 두 개의 정확성 포인트

**① 발송 빈도에는 학술 근거가 있다 (send-time optimization과 구분하라)** 🎯

§7-4의 "채널 피로도" pain point는 지금까지 **커뮤니티 증언만** 있었다. 이제 학술 뒷받침이 붙는다:

- **Godfrey, Seiders & Voss (2011)** — "Enough Is Enough! The Fine Line in Executing Multichannel Relational Communication," *Journal of Marketing* 75(4), 94–109. DOI `10.1509/jmkg.75.4.94` ⭐ `메타데이터 확인`
  > **빈도의 역U자** — 커뮤니케이션 빈도에 최적점이 있고, 넘으면 성과가 꺾인다.
- **Zhang, Kumar & Cosguner (2017)** — "Dynamically Managing a Profitable Email Marketing Program," *JMR* 54(6), 851–866. DOI `10.1509/jmr.16.0210` ⭐ `메타데이터 확인`

> 🚨 **단, 구분이 중요하다:** **Send-time optimization(사용자별 최적 발송 시각 예측)은 최상위 저널 검증이 없다** — 업계 관행이다. 반면 **발송 빈도/피로도에는 근거가 있다.** 벤더가 "AI 발송 시각 최적화"를 팔 때와 "빈도 상한"을 말할 때의 근거 강도가 다르다는 걸 챕터에서 구분해서 쓰라.
> ⚠️ 두 논문 모두 `메타데이터 확인`이다 — **구체 수치·결론 방향을 귀속시키지 마라.**

**② 🚨 DMARC는 "표준"이 아니다 — 분류 정정** `문서 확인 (RFC 직접 조회)`

| RFC | 문서 | 발행 | **IETF 카테고리** |
|---|---|---|---|
| **RFC 7208** | SPF (Sender Policy Framework) v1, S. Kitterman | **2014-04** | ✅ **Standards Track** |
| **RFC 6376** | DKIM Signatures, Crocker·Hansen·Kucherawy (Eds.) | **2011-09** | ✅ **Standards Track** |
| **RFC 7489** | DMARC, Kucherawy·Zwicky (Eds.) | **2015-03** | 🚨 **Informational** |

> 🎯 **업계에서 DMARC를 "표준"이라 부르지만 IETF 분류상으로는 Informational이다.** SPF·DKIM만 Standards Track이다. **이 구분을 정확히 쓰면 신뢰가 올라간다** — §7-4의 딜리버러빌리티 챕터에서 쓸 디테일.

**③ 그 외**
- **D-11. 업리프트 모델링 / CATE** — "누구에게 캠페인을 보내야 이득인가" (`papers.md` D-11)
- **D-12. 멀티암드 밴딧 / 컨텍스추얼 밴딧** (`papers.md` D-12)
- **D-15. 가격·프로모션·쿠폰 타겟팅의 인과 효과** — ❌ **미확보**

### 3-K. ✅ 기반 기술의 학술적 뿌리 (C축 — 확보 완료)

> `papers.md` C-16~C-22. **전 항목 `메타데이터 확인` 이상** (Crossref/arXiv API 직접 조회).

**C-16. 근사 자료구조** (§4-5가 이 서지를 쓴다)
- **Bloom (1970)**, "Space/time trade-offs in hash coding with allowable errors," *CACM* 13(7), 422–426. DOI `10.1145/362686.362692` ⭐
- **Flajolet, Fusy, Gandouet & Meunier (2007)**, "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm," *DMTCS Proceedings* vol. AH (AofA 2007). DOI `10.46298/dmtcs.3545` ⭐
- **Heule, Nunkesser & Hall (2013)**, "HyperLogLog in practice," *EDBT 2013*, 683–692. DOI `10.1145/2452376.2452456` — **프로덕션이 실제로 쓰는 개선판**
- **Cormode & Muthukrishnan (2005)**, "An improved data stream summary: the count-min sketch and its applications," *Journal of Algorithms* 55(1), 58–75. DOI `10.1016/j.jalgor.2003.12.001`
- **Dunning & Ertl (2019)**, "Computing Extremely Accurate Quantiles Using t-Digests," arXiv:**1902.04023**
- **Dasgupta, Lang, Rhodes & Thaler (2016)** — Theta Sketch, arXiv:**1510.01455**, *ICDT 2016* ⚠️ **저자 오인용 주의(§4-5)**

**C-17. 스트림 처리 이론**
- **Akidau et al. (2015)** — Dataflow Model ⭐⭐ (§4-3 워터마크·이벤트 타임의 이론적 출처)
- **Kreps, Narkhede & Rao (2011)** — Kafka 원 논문 ⚠️ **위상 주의** (peer-review 위상은 `papers.md` 확인)
- **Carbone et al. (2017)** — Flink의 상태 관리, **exactly-once의 실체**
- 🚨 **Lambda / Kappa 아키텍처 — peer-reviewed 논문이 아니다** ⭐ → §4-8의 `확인 불가`가 **확정 판정으로 바뀌었다.** 블로그 글이 출처임을 명시하고 쓰라.

**C-18. 컬럼 지향 저장·OLAP**
- **Stonebraker et al. (2005)** — C-Store ⚠️ DOI 주의 / **Abadi et al. (2013)** — 컬럼 스토어 서베이 ⭐ / **Melnik et al. (2010/2011/2020)** — Dremel / **Yang et al. (2014)** — Druid / **Im et al. (2018)** — Pinot
> §4-4의 ClickHouse·Druid·Pinot 설명에 학술 계보를 붙일 수 있다.

**C-19. 엔티티 해석 — §4-6·§5-4 ID 그래프의 학술적 대응물**
- **Fellegi & Sunter (1969)** — 확률적 레코드 링키지의 이론 ⭐⭐ (**결정적/확률적 매칭의 학술 원류**)
- **Mudgal et al. (2018)** 딥러닝 엔티티 매칭 설계 공간 / **Li et al. (2020)** Ditto / **Papadakis et al. (2020)** 블로킹·필터링 서베이 ⭐ / **Thirumuruganathan et al. (2021)**

**C-20. 프라이버시 기술 — §5-5의 negative finding을 학술 개념으로 보완한다**
- **Dwork, McSherry, Nissim & Smith (2006)** — 차등 프라이버시 ⭐⭐ / **Sweeney (2002)** — k-익명성 / **McMahan et al. (2017)** — 연합 학습(FedAvg) ⭐ / **Erlingsson, Pihur & Korolova (2014)** — RAPPOR(로컬 DP) / **Pinkas, Schneider & Zohner (2018)** — **PSI**
> 🎯 **이제 PSI·k-익명성을 학술 개념으로는 소개할 수 있다.** 단 **§5-5의 규율은 그대로다 — "특정 벤더 제품이 그걸 쓴다"고는 쓰지 마라.** 어느 벤더 문서에서도 그 이름으로 확인되지 않았다.
- **Ghazi et al. (2024/2025)** — Privacy Sandbox 리포트의 차등 프라이버시 분석 ⭐
- 🎯 **Grib et al. (2026)** — **"Privacy Sandbox의 흥망"** ⭐ **최신.** §5-1의 정책 궤적(2025-04 철회 → 2025-10 은퇴)에 **학술적 사후 분석**을 붙일 수 있다. 이 책의 프라이버시 챕터에 매우 유용.
- **Tholoniat et al. (2024)** — Cookie Monster(온디바이스 프라이버시 예산)

**C-21. LLM의 마케팅 적용 — §4-9의 "확인 불가" 항목을 부분 보완**
- **Yu et al. (2018)** — Spider ⭐ / **Li et al. (2023)** — BIRD ⭐ (text-to-SQL 벤치마크 = "자연어 세그먼트 질의"의 학술 대응물)
- **Hong et al. (2024/2025)** — LLM text-to-SQL 서베이 ⭐ / **Liu et al. (2025)**·**Zhang et al. (2024)** — 개인화 LLM 서베이
- **Aghaei et al. (2025)** — 마케팅 관리에서의 LLM ⚠️ **프리프린트**
- ❌ **LLM 생성 카피의 효과 크기 연구 — 미확보.** "LLM 카피가 성과를 X% 올린다"는 주장의 근거는 **없다.**

**C-22. Sculley et al. (2015)** — ML 시스템의 숨겨진 기술 부채 ⭐⭐ → §4-9의 학습-서빙 스큐·피처 스토어 논의의 학술 근거.

### 3-L. ⏳ 남은 학술 공백

| 축 | 상태 |
|---|---|
| **LLM 생성 마케팅 카피의 효과 크기** | ❌ **미확보 (C-21-7 명시적 실패 판정)** — 수치 주장 금지 |
| **가격·프로모션·쿠폰 타겟팅 인과 효과** | ❌ **미확보 (D-15 명시적 실패 판정)** |
| **홀드아웃 그룹 설계 / 코호트 리텐션 커브 형태** | ❌ 정전 논문 미특정 (§3-A) |
| **RFM 용어의 기원** | ❌ 1차 문헌 미확인 (§3-A) |

🚨 **저술 규율:** 위 축의 논문을 챕터에서 인용해야 한다면 **`papers.md`를 먼저 열어 실제로 기록됐는지 확인하라. 없으면 새로 조회하라. 기억으로 인용을 만들면 존재하지 않는 논문을 지어내게 된다.**

**다만 이 섹션이 비어 있어도 이미 확보된 마케팅 원리 근거가 있다** — 아래는 웹·커뮤니티 축에서 나온 것으로, 학술 근거와 별개로 유효하다.

### 3-M. 어트리뷰션이 원리적으로 안 맞는 기술적 이유 (커뮤니티 1차)

**가장 흔한 원인:** 각 광고 플랫폼이 **같은 전환을 각자 자기 것이라고 주장**한다.

> "The most common source of inflation in Google/FB self reported performance numbers is multiple ad channels taking credit for the same order. If a customer clicks a Google ad then clicks a Facebook Ad then makes a purchase, each ad channel will claim credit for that purchase."
>
> — HN 28855010 / fourseventy / 2021-10-13 (어트리뷰션 회사 ThoughtMetric 운영자의 자기 진술) `커뮤니티 주장 (검증 필요)` `[community]`

그래서 **플랫폼 합계 > 실제 매출**이 된다. 개발자가 마케터에게 설명해야 하는 첫 번째 개념.

**실무 휴리스틱 H1 — 85%를 목표로 하라:**

> "Your best bet is to sit down, figure out what your channel KPIs are, and then try to do 85% attribution with your different activities. **Going for 100%, with GA or any other tool, is just going to drive you mad.**"
>
> — HN 9258007 / bduerst / 2015-03-24 `커뮤니티 주장 (검증 필요)`

⚠️ 85%는 근거 없는 어림수다. 다만 **"완전성을 포기하고 KPI를 먼저 정하라"는 순서**는 여러 소스가 공유한다.

### 3-N. Predictive Segments — 벤더가 실제로 파는 예측 기능 (1차)

Insider One의 **Predictive Segments 5종** (문서 확인):
1. Likelihood to Purchase
2. User Engagement
3. Customer Lifecycle Status
4. Discount Affinity
5. Attribute Affinity

작동 설명 (원문 조각): "leverage algorithms that predict users' likelihood to purchase and segment users based on their interests and purchase behaviors"

⚠️ **사용하는 ML 모델에 대한 서술 → NOT FOUND. 어떤 모델·피처를 쓰는지 공개 자료 없음. 추정 금지.**

[academy.insiderone.com/docs/audience-predictive-segments | 페이지 표기 2026-04-12 | 검색 시점 2026-07-25] `1차 확인` `[web-products]`

**RFM 세그먼트가 별도 문서로 존재한다** (`academy.insiderone.com/docs/rfm-segments.md`가 문서 인덱스에서 확인됨). ⚠️ 문서 본문은 미조회 → 내용 `확인 불가`.

> **관찰:** RFM(Recency/Frequency/Monetary)이라는 1960년대 다이렉트 메일 시대의 기법이 2026년 CDP 제품 문서에 별도 페이지로 살아 있다. 마케팅 원리의 수명이 기술의 수명보다 길다는 증거.

---

## 4. 기술 스택 — 수집·처리·저장·아이덴티티·AI

> **버전 표기 규율 (BLOCKING):** 아래 버전은 **2026-07-25에 공식 릴리스 페이지를 실제로 열어 확인한 것**이다. `확정`은 페이지에 연도까지 명시된 것, `연도 추정`은 GitHub Releases가 연도를 생략해 추정한 것이다. **`연도 추정` 항목을 챕터에 연도까지 박아 쓰지 마라.**
>
> 🚨 **이 리서치가 실증한 함정:** "GitHub이 연도를 생략하면 당해 연도"라는 추론은 **반례가 존재한다.** Snowplow의 `22.01 Western Ghats – 31 Jan`은 CalVer상 2022년인데도 연도 없이 렌더링됐다. Iceberg·Pinot·Druid는 태그 페이지를 다시 열어도 `YEAR NOT ON PAGE`였고, 결국 **Apache 배포 아카이브(전체 타임스탬프 출력)로 재확인**했다. `[web-stack]`

### 4-1. Tier 1 — 확인된 버전 일람

| 컴포넌트 | 버전 | 날짜 | 확정 수준 | 출처 |
|---|---|---|---|---|
| **Apache Kafka** | 4.3.1 | 2026-06-23 | ✅ 확정 | archive.apache.org/dist/kafka/ |
| **Apache Flink** | 2.3.0 (LTS 1.20.5 / 2026-06-03) | 2026-06-25 | ✅ 확정 | flink.apache.org/downloads/ |
| **Apache Iceberg** | 1.11.0 | 2026-05-19 | ✅ 확정 | archive.apache.org/dist/iceberg/ |
| **Apache Pinot** | 1.5.1 | 2026-06-30 | ✅ 확정 | archive.apache.org/dist/pinot/ |
| **Apache Druid** | 37.0.0 | 2026-05-06 | ✅ 확정 | archive.apache.org/dist/druid/ |
| **Trino** | 483 | 2026-07-17 | ✅ 확정 | trino.io/docs/current/release.html |
| **DuckDB** | 1.5.5 (LTS 1.4.5 / 2026-06-17) | 2026-07-22 | ✅ 확정 | duckdb.org/news/ |
| **dbt-core** | 1.12.0 (2.0은 **alpha**) | 2026-07-16 | ✅ 확정 | github.com/dbt-labs/dbt-core/releases |
| **Snowplow SLULA** | v1.1 (v1.0은 2024-01) | 2024-12 | ✅ 확정 | docs.snowplow.io/docs/licensing/... |
| **ClickHouse** | **26.x 계열** (v26.7.1.1315-stable) | 2026 | ⚠️ 연도 추정 | github.com/ClickHouse/ClickHouse/releases |
| **Redis** | 8.8.1 (8.10은 RC) | 2026 | ⚠️ 연도 추정 | github.com/redis/redis/releases |
| **Feast** | 0.65.0 | 2026 | ⚠️ 연도 추정 | github.com/feast-dev/feast/releases |
| **rudder-server** | 1.81.1 | 2026 | ⚠️ 연도 추정 | github.com/rudderlabs/rudder-server/releases |

`[web-stack]` · 전 항목 검색 시점 2026-07-25

> ⚠️ **ClickHouse는 특히 조심하라.** 여러 유지보수 라인이 병행 패치되므로 **"최신 = 가장 높은 버전"이 아니다** (v26.7.1은 22 Jul, v26.5.6은 23 Jul — 버전은 낮은데 릴리스가 늦다). 책에 "최신 버전은 X"라고 쓰면 거의 확실히 틀린다. **"26.x 계열 / 2026 기준"으로 써라.**
>
> ⚠️ **Flink·DuckDB는 2.x/1.x, 1.5.x/1.4.x LTS 두 라인이 병행 중**이다. 코드를 넣을 때 어느 계열 기준인지 반드시 명시하라.

### 4-2. 수집·전송 — Kafka가 대체 불가인 이유

**핵심 성질:** 큐는 읽으면 사라지지만 **Kafka는 읽어도 남는다.** 같은 클릭스트림을 실시간 세그먼트 엔진도, 웨어하우스 적재기도, 6개월 뒤 새 모델 학습용 백필도 읽는다.

**파티션과 순서 보장** (Confluent 공식 문서 원문):
> "messages in each partition log are then read sequentially"
> "Each partition is consumed by exactly one consumer within each consumer group at any given time."
> "A consumer offset is used to track the progress of a consumer group. An offset is a unique identifier, an integer, which marks the next record that should be read by the consumer in a partition."
>
> [docs.confluent.io/kafka/design/consumer-design.html | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

> **Martech에서 파티션 키는 성능 튜닝이 아니라 데이터 모델링 결정이다.** `user_id`로 파티셔닝하면 한 사용자의 이벤트가 한 파티션에 들어가 "장바구니 담기 → 결제 → 환불" 순서가 뒤집히지 않는다. `event_type`으로 파티셔닝하면 한 사용자의 이벤트가 흩어지고, 저니 상태 머신이 "결제를 먼저 보고 장바구니를 나중에 보는" 사고가 난다. `관찰` `[web-stack]`

**Exactly-once — 면접 단골이자 가장 많이 오해되는 지점** (KIP-98 원문):
> "Every new producer will be assigned a unique PID during initialization."
> "For a given PID, sequence numbers will start from zero and be monotonically increasing"
> "Every message write will be persisted exactly once, without duplicates and without data loss"

**그런데 KIP-98은 보장하지 않는 것도 명시한다** — 이게 결정적이다:
> "We cannot guarantee that all the messages of a committed transaction will be consumed all together"

이유 4가지: 컴팩션된 토픽이 트랜잭션 메시지를 덮어쓸 수 있고, 로그 세그먼트를 넘나드는 트랜잭션은 세그먼트 삭제 시 일부를 잃고, 컨슈머가 임의 지점으로 seek하면 앞부분을 놓치고, 컨슈머가 트랜잭션에 참여한 모든 파티션을 읽지 않을 수 있다.

[cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

**운영 함정** (`관찰`, `[web-stack]`):
- **파티션 수는 되돌리기 어렵다.** 늘리는 순간 `hash(key) % partition_count`가 바뀌어 기존 키의 배치가 깨진다 → "저니가 한 번 꼬였다"로 나타난다.
- **핫 파티션.** `user_id` 해시의 균등성은 봇·크롤러·내부 테스트 계정 앞에서 깨진다.
- **컨슈머 랙이 Martech의 진짜 SLA다.** "실시간 세그먼트"라고 팔았는데 랙이 20분이면 실시간이 아니다.
- **exactly-once는 공짜가 아니다.** 대부분의 Martech 파이프라인은 **at-least-once + 다운스트림 멱등 처리**(이벤트 ID 기준 중복 제거)가 더 현실적이다.

**Snowplow — 스키마 검증을 1급 시민으로** (공식 문서 원문):
> "The **Enrich** application cleanses the data and validates each event against its schema to ensure it meets the criteria you have designed and set."
> "failed events can be reprocessed"
>
> [docs.snowplow.io/docs/fundamentals/ | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

**두 문장이 함께 중요하다.** 검증만 하고 실패 이벤트를 버리면 데이터 손실이다. 검증하고 **격리 보관하고 재처리 가능하게** 만드는 게 완성형이다.

> 🚨 **책에 반드시 넣을 것 — Snowplow는 더 이상 OSI 오픈소스가 아니다.** 공식 FAQ 원문:
> > "Licensee is not granted the right to, and Licensee shall not, exercise the License for any Competing Use, and Licensee may exercise the License only for Non-Production Use or Non-Commercial Use."
>
> SLULA v1.0(2024-01) → **v1.1(2024-12)**에서 "Highly Available" 조항이 제거되어, **고가용성 여부와 무관하게 모든 프로덕션 사용이 상용 라이선스를 요구**하게 정리됐다.
> [docs.snowplow.io/docs/licensing/limited-use-license-faq/ | v1.1 = 2024-12 (문서 표기) | 검색 시점 2026-07-25] `1차 확인`
>
> **"오픈소스 CDP 스택"이라며 Snowplow를 골랐다가 프로덕션 배포 직전에 라이선스 문제를 발견하는 사고가 실제로 일어난다.** Apache 2.0 포크(OpenSnowcat) 존재 언급은 확인했으나 **포크 현황은 `확인 불가`**.
>
> ⚠️ 같은 이유로 **RudderStack·Redis의 라이선스는 `확인 불가`**다. 조회에 실패했다. **"오픈소스"라고 단정 서술하지 말고 저술 시 재확인하라.** 이 카테고리의 라이선스는 변동이 잦다.

### 4-3. 처리 — Flink와 "실시간"의 진짜 의미

**이벤트 타임 vs 처리 타임** (공식 문서 원문):
> "Event time is the time that each individual event occurred on its producing device."

**워터마크 정의 — 그대로 외울 가치가 있다:**
> "A Watermark(t) declares that event time has reached time t in that stream, meaning that there should be no more elements from the stream with a timestamp t' <= t."

[nightlies.apache.org/flink/flink-docs-release-2.0/docs/concepts/time/ | 발행일 확인 불가 (2.0 문서 브랜치) | 검색 시점 2026-07-25] `1차 확인`

> **Martech에서 왜 결정적인가** (`관찰`): 지하철에서 앱을 쓴 사용자의 이벤트는 지상에 올라온 20분 뒤 서버에 도착한다. 처리 타임 기준이면 그 사용자는 "20분 뒤에 장바구니를 담은 사람"이 되고, "장바구니 담고 30분 내 미결제 → 쿠폰 발송" 룰이 엉뚱한 시점에 발동한다.

**운영 함정** (`관찰`, `[web-stack]`):
- **워터마크 지연 설정이 곧 비즈니스 결정이다.** 5초면 모바일 오프라인 이벤트를 대량으로 놓치고, 30분이면 "실시간"이 30분 지연 시스템이 된다. **마케터에게 "실시간"이라 말하기 전에 워터마크 값을 먼저 합의해야 한다.**
- **상태가 무한히 큰다.** 사용자별 상태를 TTL 없이 두면 사용자 수에 비례해 무한 증가. Martech는 사용자가 수천만인 도메인이라 즉시 문제가 된다.
- **부재(absence) 조건이 어렵다.** "최근 7일 미방문"은 **아무 이벤트도 오지 않는** 사용자를 감지해야 하므로 타이머가 필수다.
- **운영 난이도가 스택에서 가장 높다.** 소규모 팀이 도입했다가 유지 못 하고 배치로 회귀하는 사례가 흔하다.

**dbt — 세그먼트를 코드로 관리하는 패턴** (공식 문서 원문):
> "Models are primarily written as a `select` statement and saved as a `.sql` file."
> "When you execute `dbt run`, you are running a model that will transform your data without that data ever leaving your warehouse."
>
> [docs.getdbt.com/docs/build/models | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

전형적 계층 구조 (`관찰`):
```
staging/       원본 이벤트 정규화 (stg_events, stg_orders, stg_users)
    ↓ ref()
intermediate/  아이덴티티 해석, 세션화 (int_identity_graph, int_sessions)
    ↓ ref()
marts/         고객 360 (dim_customer)
               세그먼트 (seg_high_value, seg_churn_risk, seg_cart_abandoners)
```

**여기서 나오는 실무적 미덕:** 세그먼트가 코드가 되어 PR로 리뷰되고 git blame으로 추적된다 → **"VIP 세그먼트 기준이 언제 바뀐 거야?"라는 흔한 사고가 사라진다.** 테스트가 붙는다("세그먼트 크기가 전일 대비 50% 이상 변하면 실패"). DAG가 영향 범위를 알려준다.

**함정:** dbt는 배치다. 증분 모델은 **늦게 도착한 데이터**를 놓치기 쉬운데, Martech의 모바일 이벤트는 늦게 오는 게 정상이라 상시 발생한다. 그리고 **웨어하우스 비용이 실행 빈도에 비례**해 "1시간마다 갱신" 요구와 정면 충돌한다.

### 4-4. 저장 — 왜 같은 고객 데이터가 두 벌 존재하나

**ClickHouse MergeTree — 희소 인덱스가 전부를 설명한다** (공식 문서 원문):
> "The primary key also does not reference individual rows but blocks of 8192 rows called granules."
>
> [clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

> B-tree는 행 하나하나를 가리키니 인덱스가 데이터만큼 커진다. MergeTree는 **8192행짜리 그래뉼 단위**로만 가리키니 인덱스가 RAM에 통째로 들어간다. 대신 "이 사용자 한 명의 행"을 찍어 가져오는 건 못 한다. **OLAP에 강하고 OLTP에 약한 이유가 이 한 줄에 있다.**

**Trino는 아예 못박는다** (공식 문서 원문):
> "Do not mistake the fact that Trino understands SQL with it providing the features of a standard database."
> "Trino is not a replacement for databases like MySQL, PostgreSQL or Oracle."
> "Trino was not designed to handle Online Transaction Processing (OLTP)."
>
> [trino.io/docs/current/overview/use-cases.html | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

**그래서 분석 경로와 서빙 경로가 갈린다** (`관찰`, `[web-stack]`):

| | 분석 경로 | 서빙 경로 |
|---|---|---|
| 질문 | "지난달 VIP 세그먼트는 몇 명?" | "이 사람은 VIP인가?" |
| 접근 | 수억 행 스캔·집계 | 키 하나 조회 |
| 지연 | 초~분 | 밀리초 |
| 동시성 | 수십 | 수만 |
| 스토어 | ClickHouse / Iceberg+Trino | Redis / Aerospike / Cassandra |

> **개발자가 Martech 아키텍처 다이어그램을 처음 볼 때 "왜 이렇게 중복이 많지?"라고 느끼는 이유가 이것이다.** 조회 패턴이 근본적으로 다르다.

**ClickHouse vs Pinot — 자리가 다르다** (`관찰`):
- **ClickHouse** — 분석가·마케터가 대시보드에서 던지는 무거운 애드혹 쿼리. 동시성 낮음(수십), 쿼리 복잡, 데이터 큼.
- **Pinot** — **최종 사용자에게 직접 노출되는** 분석. 광고주 콘솔("내 캠페인 지금 성과"), 판매자 대시보드. 동시성 높음(수천~수만), 쿼리 정형화, 지연 밀리초.

Pinot 프로젝트 문서의 성능 표방:
> "Ultra low-latency queries (as low as 10ms P95)" / "High query concurrency (as many as 100,000 queries per second)"
>
> [docs.pinot.apache.org/architecture-and-concepts/concepts/architecture.md | 검색 시점 2026-07-25]
>
> 🚨 **인용 시 필수 표기: 이는 Apache Pinot 프로젝트 자체 문서의 표방 수치이며 독립 검증된 벤치마크가 아니다.**

> 🚨 **ClickBench도 마찬가지다.** 제3자 중립 벤치마크처럼 인용되는 경우가 많으나 **운영 주체가 ClickHouse다.** 방법론 문서는 미조회. **구체 수치는 `확인 불가` — 인용 금지.** `[web-stack]`

**Apache Iceberg — 왜 고객 데이터 레이크하우스의 기본값이 되었나**

스펙 원문:
> "Table metadata file tracks the table schema, partitioning config, custom properties, and snapshots of the table contents."
> "Valid primitive type promotions are: `int` to `long`, `float` to `double`, and `decimal(P, S)` to `decimal(P', S)` if P' > P."

포맷 버전별 차이: **v1** 불변 파일 관리 / **v2** 행 수준 삭제("delete files to encode rows that are deleted in existing data files") / **v3** 타입 확장(nanosecond timestamp, variant, geometry, geography) + 기본값 + **행 계보(row lineage)**

[raw.githubusercontent.com/apache/iceberg/main/format/spec.md | main 브랜치 시점 | 검색 시점 2026-07-25] `1차 확인`

**Martech에서 결정적인 네 가지** (`관찰`):
1. **삭제할 수 있어야 한다.** 고객 데이터는 삭제 요청이 법적으로 강제된다. v2의 행 수준 delete가 없으면 "사용자 한 명 지우기"가 **수 TB 재작성**이 된다. **테이블 포맷 선택이 규제 대응 능력을 결정한다.**
2. **스키마가 계속 변한다.** 이벤트 스키마는 제품이 바뀔 때마다 필드가 붙는다.
3. **타임 트래블이 감사·재현의 근거다.** "3월 캠페인 때 이 사용자가 정말 VIP였나?"를 그 시점 스냅샷으로 증명한다. 마케팅·정산 분쟁에서 실제로 쓰인다.
4. **엔진 중립.** 벤더 락인을 피하는 유일한 실용적 경로.

**함정:** 스트리밍 적재는 작은 파일을 대량 생산해 **컴팩션이 상시 운영 업무**가 된다. 스냅샷 만료 정책을 안 걸면 비용이 계속 늘고, **너무 짧게 걸면 타임 트래블·삭제 감사 능력을 잃는다 — 규제 요구와 비용이 여기서 정면충돌한다.**

**ClickHouse의 삭제 함정:** mutation은 파트를 다시 쓴다. GDPR 삭제 요청이 들어올 때 "사용자 한 명 지우기"가 테이블 전체 재작성으로 번질 수 있다. `ReplacingMergeTree`·파티션 단위 DROP 설계를 미리 해둬야 한다.

**DuckDB — 이 책의 실습 환경으로 최적** (공식 문서 원문):
> "DuckDB does not run as a separate process, but completely **embedded within a host process**."
> "DuckDB uses a **columnar-vectorized query execution engine**, where queries are still interpreted, but a large batch of values (a 'vector') are processed in one operation."
> "the DuckDB Python package can run queries directly on Pandas data without ever importing or copying any data."
>
> [duckdb.org/why_duckdb | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

> **개발자 독자가 오늘 당장 써볼 수 있는 유일한 항목이다.** `pip install duckdb` 한 줄로 이벤트 분석·퍼널 쿼리를 따라 할 수 있다. **책에 실습을 넣는다면 DuckDB가 최선의 선택이다.** `[web-stack]`

### 4-5. 근사 자료구조 — 이 책에서 가장 "새로운 지식"이 될 부분

**핵심 서사:** 마케팅 지표는 대부분 정확할 필요가 없고, 그 사실을 이용하면 메모리를 수천 배 아낀다.

| 마케팅 질문 | 자료구조 | 정확도 | 메모리 |
|---|---|---|---|
| "이번 캠페인 고유 도달 수는?" | HyperLogLog | 표준 오차 **0.81%** | 최대 **12KB** (고정) |
| "이 사용자가 이 광고를 이미 봤나?" | Bloom filter | 거짓 양성만, 거짓 음성 없음 | 0.1% 오류율 시 항목당 **14.378비트** |
| 위 + 삭제 필요 | Cuckoo filter | 삭제 가능 | — |
| "이 캠페인의 노출 빈도는?" | Count-Min Sketch | **임계값 이상만 신뢰** | 폭 w = 2/error |
| "세션 길이 p50/p90/p99는?" | t-digest | compression 파라미터로 조절 | 압축된 센트로이드 |

**HyperLogLog** (Redis 공식 문서 원문):
> "The Redis implementation uses up to 12 KB of memory and provides a standard error rate of 0.81%."
> "The HyperLogLog can estimate the cardinality of sets with up to 18,446,744,073,709,551,616 (2^64) members."
>
> 문서가 직접 드는 사용 사례가 그대로 Martech다: "How many unique visits has this page had on this day?"
>
> [redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

명령: `PFADD` O(1), `PFCOUNT` O(1), `PFMERGE` O(N).

> **대비를 만드는 계산 (`관찰`):** 1,000만 명의 고유 방문자를 Set으로 세면 사용자 ID를 전부 저장해야 한다. **HLL은 12KB다.** 이 대비가 이 절 전체의 훅이다.
>
> 🚨 **HLL의 결정적 한계 — 합집합만 된다.** `PFMERGE`는 합집합이고 **교집합은 없다.** "세그먼트 A와 B 둘 다 속한 고유 사용자 수"는 HLL로 직접 못 구한다. 포함배제 원리로 근사하면 오차가 증폭된다. **실무에서 자주 걸리는 함정이다.**

**ClickHouse의 같은 선택** — `uniqCombined`는 적응형 3단(작은 기수는 배열 → 중간은 해시테이블 → 큰 기수는 HyperLogLog). 한계 (원문): "the error will raise quickly after a few tens of billions of distinct values". `uniqExact`는 "the size of the state has unbounded growth".

> **Martech 번역 (`관찰`):**
> - "캠페인 도달 유니크 사용자 수" → `uniqCombined`로 충분. 대시보드 숫자가 0.5% 틀려도 아무도 안 죽는다.
> - "이 쿠폰을 실제로 받은 사용자 수(정산 대상)" → `uniqExact`. **돈이 걸리면 근사는 안 된다.**
> - **이 구분을 못 하는 팀이 겪는 사고:** 마케팅 대시보드와 정산 리포트의 유니크 수가 안 맞아 며칠간 원인 추적. 원인은 버그가 아니라 **함수 선택**이었다.

**Bloom filter — Redis 공식 문서가 광고 사용 사례를 직접 든다** (그대로 인용 가능):
> "Ad placement (retail, advertising) — This application answers these questions: Has the user already seen this ad? Has the user already bought this product?"
>
> 보장의 비대칭성: "A Bloom filter can guarantee the absence of an item from a set, but it can only give an estimation about its presence. So when it responds that an item is not present in a set (a negative answer), you can be sure that indeed is the case. But one out of every N positive answers will be wrong."
>
> 메모리: "1% error rate requires 7 hash functions and 9.585 bits per item." / "0.1% error rate requires 10 hash functions and 14.378 bits per item." / "0.01% error rate requires 14 hash functions and 19.170 bits per item."
>
> [redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/ | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

> **Martech 번역 (`관찰`) — 이 방향성 분석이 "아, 이래서 쓰는구나"를 준다:** "안 봤다"는 확실하고 "봤다"는 틀릴 수 있다. 즉 **광고를 안 본 사람에게 안 보여주는 실수는 없고, 본 적 없는데 "봤다"고 판정해 노출을 건너뛰는 실수만 있다.** 광고 기회를 약간 잃을 뿐 사용자를 괴롭히지 않는다 — **보수적으로 안전한 방향이다.**

**Count-Min Sketch — 가장 중요한 경고** (원문 그대로 인용할 것):
> "It is very important to know that the results coming from a Count-Min sketch lower than a certain threshold (determined by the error_rate) should be ignored and often even approximated to zero. So Count-Min sketch is indeed a data-structure for counting frequencies of elements in a stream, but it's only useful for higher counts. Very low counts should be ignored as noise."
>
> 임계값 공식: `threshold = error * total_count`
>
> 문서 스스로의 결론: "This shows that a CMS is maybe not the best data structure to count frequency of a uniformly distributed stream."
>
> [redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/ | 검색 시점 2026-07-25] `1차 확인`

> **Martech 번역:** CMS는 **롱테일이 아니라 헤비히터를 찾는 도구**다. "가장 많이 노출된 광고 TOP N"에는 맞고, "이 사용자가 이 상품을 몇 번 봤나"(개별 저빈도)에는 안 맞는다. **이 구분을 못 하면 조용히 틀린 숫자를 보고 있게 된다.**

**t-digest** (원문): "The `COMPRESSION` argument is used to specify the tradeoff between accuracy and memory consumption. The default value is 100." / trimmed mean은 "the mean value from the sketch, excluding observation values outside the low and high cutoff percentiles."

> **Martech 번역:** "VIP 세그먼트의 임계값을 데이터로 정한다" → `TDIGEST.QUANTILE 0.9`. **trimmed mean이 특히 유용하다** — "이상치를 뺀 평균 객단가"는 마케팅 리포트가 실제로 원하는 숫자다.

> **이 절의 챕터 프레임:** **"마케터가 요구하는 정확도와 시스템이 지불하는 비용은 협상 가능하다."** MAU가 2,847,193이든 2,847,900이든 어떤 마케팅 의사결정도 바뀌지 않는다. 그 0.81%를 받아들이는 대가로 메모리를 수천 배 아낀다. 반대로 쿠폰 정산 대상자 수는 한 명도 틀리면 안 된다. **어느 숫자가 어느 쪽인지 판별하는 능력이 Martech 개발자의 핵심 역량이다.**

> ✅ **원 논문 서지는 §3-K에서 확보됐다** (Bloom 1970 / Flajolet et al. 2007 / Cormode & Muthukrishnan 2005 / Dunning & Ertl 2019). **학술 귀속이 가능하다.**
> ⚠️ 단, 전부 `메타데이터 확인` 수준이다 — **위의 구체 수치(0.81%, 12KB, 14.378비트)는 여전히 Redis 공식 문서의 값이지 원 논문의 값이 아니다. 수치를 원 논문에 귀속시키지 마라.**

#### 🎯 HLL의 교집합 한계를 푸는 자료구조가 따로 있다 — Theta Sketch

위에서 "HLL은 합집합만 되고 교집합은 없다"고 했다. **그런데 마테크 세그먼테이션이 요구하는 건 정확히 그 연산이다** — "A 세그먼트 AND B 세그먼트 NOT C 세그먼트가 몇 명인가".

**Dasgupta, Lang, Rhodes & Thaler (2016)** — "A Framework for Estimating Stream Expression Cardinalities," arXiv:**1510.01455**, *ICDT 2016*, LIPIcs Vol. 48. `메타데이터 확인`
> 각 스트림의 샘플을 **보편적(universal)으로 결합**해 합집합·교집합·차집합 같은 **집합 연산의 카디널리티**를 추정하는 프레임워크.
> **Apache DataSketches의 Theta Sketch가 이 논문의 구현이고, 이게 CDP 세그먼트 빌더의 실시간 카운트를 떠받친다.** `[papers C-16-6]`

> 🚨 **저자 정정 — 책에 쓸 만한 실물 사례:** 이 논문의 저자를 **"Dasgupta, Lang, Stokes, Tirthapura"로 적는 자료가 돌아다니는데 틀렸다.** arXiv API가 반환한 실제 저자는 **Dasgupta, Lang, Rhodes, Thaler**다. (Gibbons & Tirthapura는 관련된 다른 논문의 저자다.)
> **이 항목 자체가 "인용을 기억으로 만들면 안 되는 이유"의 실물 증거다** — 챕터에서 그렇게 쓸 수 있다.

> 🎯 **또 하나의 좋은 대목 — 논문과 프로덕션 구현은 다르다:** **Heule, Nunkesser & Hall (2013)**, "HyperLogLog in practice," *EDBT 2013*, 683–692. DOI `10.1145/2452376.2452456`
> BigQuery의 `APPROX_COUNT_DISTINCT`, Redis의 `PFCOUNT`가 실제로 구현하는 건 **원 논문이 아니라 이 개선판 계열**이다(작은 카디널리티 편향 보정, 64비트 해시, 희소 표현). **"논문을 읽었으니 구현을 안다"가 틀리는 지점.**

### 4-6. 아이덴티티 스토어와 ID 그래프

**개발자에게 익숙한 자료구조로:** ID 그래프는 **union-find(disjoint set)** 문제다. 식별자가 노드, "같은 사람" 관찰이 간선, 연결 요소가 한 사람. `관찰` `[web-stack]`

저장 전략 세 갈래:
1. **정규 ID 매핑 테이블** — `identifier → canonical_person_id`를 KV에 평탄화. 조회 O(1). 단점: 병합 시 한쪽의 모든 식별자를 다시 써야 한다.
2. **간선 저장 + 배치 해석** — 관찰된 간선만 저장하고 배치로 연결 요소를 계산. 정확하지만 지연이 있다.
3. **그래프 DB** — 유연하지만 밀리초 조회와 궁합이 나쁠 수 있다.

**실무에서 흔한 구조는 1+2 하이브리드** — 배치로 정확히 계산해 KV에 물질화하고, 스트림에서는 새 간선을 즉시 반영하되 완전 해석은 다음 배치로 미룬다.

**Martech 특유의 함정** (`관찰`):
- 🚨 **과병합(over-merge)이 프라이버시 사고다.** 공용 PC의 쿠키를 두 사람의 계정에 잘못 연결하면 **A의 구매 이력이 B에게 개인화되어 노출된다. 이건 버그가 아니라 사고다.**
- **병합은 되돌리기 어렵다.** 잘못 합친 두 프로필을 다시 가르려면 원본 간선 이력이 보존돼 있어야 한다 → **간선 원장을 append-only로 남겨야 하는 이유.**
- **삭제 요청이 그래프를 관통한다.** "내 데이터 지워줘"는 그 사람의 **모든 식별자**에 연결된 데이터를 지우라는 뜻이고, 그러려면 ID 그래프가 정확해야 한다.
- **과병합의 대표 트리거:** 공용 기기, **널·플레이스홀더 식별자**(ATT 거부 시 all-zero IDFA — §5-1 참조), 역할 계정(`info@`, `noreply@`), 기기 초기화 후 광고 ID 재발급.
- **미병합의 대표 트리거:** 익명 세션에서 장바구니에 담고 로그인 후 결제 → 잇지 못하면 "첫 구매 고객"으로 오분류.

> ⚠️ 이 소절의 저장 전략 서술은 **공개 1차 문서를 직접 조회한 것이 아니라 스택 문서들에서 추론한 아키텍처 정리**다. "일반적 패턴" 수준으로 서술하고 특정 제품의 구현이라고 단정하지 마라. 벤더 문서 근거는 `web_gaps.md`(§9 참조).

**Redis 자료구조 ↔ 마케팅 질문 매핑** (`관찰`, `[web-stack]`):

| Redis 자료구조 | 마케팅 질문 | 왜 이게 맞나 |
|---|---|---|
| **Hash** | "이 사용자의 프로필 속성은?" | 프로필 필드를 한 키에 모아 O(1) |
| **Set / Sorted Set** | "이 사용자가 속한 세그먼트는?" / "실시간 인기 TOP 10" | 집합 연산(교집합=세그먼트 AND), 점수 랭킹 |
| **HyperLogLog** | "오늘 이 캠페인의 고유 도달 수는?" | 12KB 고정 메모리 |
| **Bitmap** | "이 사용자가 오늘 방문했나?" | 사용자당 1비트 — 1천만 명 ≈ 1.25MB |
| **String + TTL** | "오늘 푸시를 몇 번 보냈나?" (frequency capping) | INCR + EXPIRE로 원자적 카운터 + 자동 만료 |
| **Bloom filter** | "이 광고를 이미 봤나?" | 사용자당 작은 필터로 재노출 방지 |

**함정:** TTL 없는 키는 영원히 남는다. **사용자 수 × 캠페인 수만큼 키가 생기는 설계는 순식간에 터진다.** 내구성 모델(RDB/AOF)에 따라 "frequency cap 카운터가 리셋되어 같은 광고가 10번 나갔다"는 실제 사고가 발생한다.

**Aerospike가 이 자리에서 반복 등장한다** — 인덱스는 메모리, 데이터는 SSD. 두 독립 신호가 같은 방향을 가리킨다: **토스 피처 스토어의 온라인 스토어가 Aerospike이고**(§4-9), **Feast 0.65.0이 Aerospike·ScyllaDB를 온라인 스토어로 추가**했다. `관찰`

### 4-7. 배치 vs 스트리밍 세그먼트 — 개발자가 가장 자주 마주칠 설계 결정

**예시 세그먼트:** "최근 30일 내 3회 이상 구매했고, 최근 7일간 앱을 열지 않은 사용자"

| | 배치 경로 | 스트리밍 경로 |
|---|---|---|
| 파이프라인 | Kafka → Iceberg/웨어하우스 → dbt(매일 새벽) → Reverse ETL | Kafka → Flink(사용자별 상태 + 타이머) → Redis/Pinot |
| 지연 | 최대 24시간 | 초 단위 |
| 비용 | 하루 한 번 전체 스캔 (**계산량에 비례**) | 24시간 상시 가동 (**시간에 비례**) |
| 복잡도 | SQL 한 파일. 신규 입사자도 읽는다 | 상태 관리·워터마크·체크포인트·상태 스키마 진화 |
| 정정 | 로직 바꾸면 다음 실행에 자동 반영. **쉽다** | 상태를 어떻게 할 것인가가 문제. **어렵다** |
| 정확도 | 매번 원본에서 재계산 → 드리프트 없음 | "30일 윈도우"를 상태로 들거나 근사해야 함 |

`관찰` `[web-stack]`

**비용 구조의 차이 (개발자가 놓치는 지점):**
- 배치: 세그먼트 100개를 하루 한 번 = 하루 100번의 스캔 비용
- 스트리밍: 세그먼트 100개 = 100개 Flink 잡이 24시간 가동. **사용자가 조용한 새벽에도 클러스터는 켜져 있다.**

**결정 규칙:** 세그먼트가 많고 지연 요구가 느슨하면 배치가 압도적으로 싸다. 세그먼트가 소수인데 지연이 결정적이면 스트리밍이 정당하다.

> 🎯 **개발자가 마케터에게 물어야 할 단 하나의 질문:**
> ***"이 세그먼트가 5분 늦으면 무슨 일이 일어나나요?"***
> - "아무 일도 안 일어나요" → 배치
> - "고객이 이미 경쟁사에서 샀어요" → 스트리밍
>
> 이 질문 하나가 아키텍처 비용을 몇 배 가른다. **책의 실용적 하이라이트로 쓸 만한 문장이다.**

**실무의 답은 대개 "둘 다"** — 대부분의 세그먼트는 배치, **전환에 직결되는 소수**(장바구니 이탈, 결제 실패, 첫 구매 축하)만 스트리밍.

### 4-8. Lambda / Kappa 아키텍처의 CDP 버전

**Lambda의 CDP 형태:** 배치 층(dbt가 밤새 고객 360·세그먼트를 정확히 재계산) + 속도 층(Flink가 오늘 이벤트로 델타 유지) + 서빙 층(둘을 합쳐 응답).

**Pinterest 사례가 정확히 이 구조다** (2026-05-21, 이 리서치에서 가장 최신이자 값진 사례):
> "Streaming Path... Batch Path... **This lambda-style architecture balances freshness (streaming updates) with completeness (batch corrections), eliminating the historical problem where training and serving systems diverged.**"
>
> - 스트리밍 경로: 실시간 인덱서가 "filters incoming events, converts them into a normalized representation, applies enrichments, and writes incremental updates."
> - 배치 경로: "read historical raw events, apply the same filter and enrichment definitions, and produce longer sequences."
> - 저장·서빙: "Sequence data is stored in a columnar layout so models can read exactly the fields they need"
>
> [medium.com/pinterest-engineering/making-user-sequence-data-more-cost-efficient-faster-and-easier-to-use-2a56a928cae1 | **2026-05-21** | 검색 시점 2026-07-25] `1차 확인` `[web-stack]`

> **Lambda의 고질병:** 같은 세그먼트 로직을 SQL(배치)과 Java/Flink(스트림)로 **두 번 구현**해야 한다. 두 구현이 갈라지면 "배치 대시보드와 실시간 개인화가 다른 답을 준다"는 사고가 나고, **Martech에서는 이게 마케터의 신뢰를 무너뜨린다.**
>
> 🎯 **Pinterest의 답이 인상적이다 — "one definition, many runtimes".** 정의를 한 번 쓰고 스트리밍/배치 런타임이 각각 실행한다. **이 하나의 사례가 §4-7(배치 vs 스트리밍), §4-8(Lambda), §4-9(학습-서빙 스큐)를 전부 관통한다. 챕터 하나의 앵커로 쓸 만하다.**

**Kappa가 Martech에서 잘 성립하지 않는 이유** (`관찰`): 이벤트 로그가 완전한 진실이어야 하는데, **Martech는 안 그렇다** — CRM의 회원 등급, 결제 시스템의 환불, 오프라인 매장 구매는 이벤트 스트림 밖에서 온다. 다만 "이벤트 로그를 진실의 원천으로 두고 파생을 재계산 가능하게 만든다"는 Kappa의 **철학**은 거의 모든 현대 CDP가 채택했다.

> ✅ **판정 확정 (§3-K, C-17-4): Lambda / Kappa 아키텍처는 peer-reviewed 논문이 아니다.**
> - **Lambda** — Nathan Marz의 블로그 글("How to beat the CAP theorem")에서 시작해 **Marz & Warren, *Big Data: Principles and Best Practices of Scalable Realtime Data Systems* (Manning, 2015)**로 정식화. **책이지 논문이 아니다.**
> - **Kappa** — Kafka 공동 창시자 **Jay Kreps**가 **2014년 O'Reilly Radar**에 쓴 블로그 글 **"Questioning the Lambda Architecture"**. **블로그 글이지 논문이 아니다.**
> → **"논문에 따르면"이라고 쓰지 마라.** "이 용어는 블로그에서 나와 업계 어휘가 됐다"고 정직하게 쓰면 오히려 좋은 대목이 된다 — §3-A의 Gamma-Gamma(개인 웹사이트 노트)와 함께 **마테크 어휘의 권위가 어디서 오는가**를 보여주는 사례다.
> 위 서술 중 Pinterest 부분만 1차 조회 근거가 있다.

> **개발자에게 전달할 핵심:** **"두 층이 존재하는 건 게으름이 아니라 물리다."** 정확성과 신선도는 동시에 최대화할 수 없다.

### 4-9. AI/ML 층 — "Martech의 AI는 대부분 LLM이 아니다"

> **주의:** 이 절은 **공개 문서·공개 기술블로그에서 확인된 것만** 기록한다. 벤더의 "AI로 무엇을 한다"는 마케팅 주장은 담지 않았다.

**토스 광고 ML 스택 — 한국 독자에게 가장 값진 사례** (국내 서비스가 실제 모델 구조를 공개한 드문 글):

3단 구조:
1. **Targeting — Lookalike**: > "유저의 행동 로그를 학습하거나 Two-tower 모델을 통해 유저와 광고 간의 상호작용을 학습하여 유저 임베딩을 생성"
2. **Filtering — 후보군 선정**: Two-tower 임베딩으로 수백만 광고 중 관련성 높은 후보를 빠르게 검색
3. **Ranking — CTR 예측**: > "CTR 예측 모델은 광고 ID, 유저 속성 등 고차원의 희소 특징 간의 상호작용을 효과적으로 학습" — FM, DeepFM, DCN 구조로 eCPM 산출

[toss.tech/article/ads-ml | **2025-04-21** | 저자 김영호 | 검색 시점 2026-07-25] `1차 확인` `[web-stack]`

> **이 사례가 좋은 이유:** "추천 시스템"이라는 뭉뚱그린 말 대신 **후보 생성 → 필터링 → 랭킹** 3단 파이프라인을 보여주고, 각 단계에 다른 모델이 들어간다는 걸 명확히 한다. **§4-6의 벡터 DB가 필요해지는 지점이 정확히 여기다** — 임베딩 최근접 이웃 검색.

**토스 피처 스토어 — 학습-서빙 일관성**:
- 오프라인 스토어: Hive 테이블 / **온라인 스토어: Aerospike**
- 데이터 누수 방지 (원문): > "Target 데이터를 기준으로 시간 파티션을 Shift 할 수 있어요. 예를들어, 01시에 발생한 피드백 데이터라도 Shift 기능을 사용하여 00시에 발생한 Feature들과 조인하여 데이터 누수를 방지할 수 있습니다."

[toss.tech/article/feature-store-trainkit | **2025-08-14** | 저자 우종호·송석현 | 검색 시점 2026-07-25] `1차 확인`

**Feast의 같은 문제 정의** (공식 문서 원문):
> "Feast is able to join features from one or more feature views onto an entity dataframe in a **point-in-time correct** way."
> "Feast is able to reproduce the state of features at a specific point in the past."
> "the TTL time is relative to each timestamp within the entity dataframe. TTL is not relative to the current point in time (when you run the query)."
>
> [docs.feast.dev/getting-started/concepts/point-in-time-joins | 발행일 확인 불가 | 검색 시점 2026-07-25] `1차 확인`

> **학습-서빙 스큐를 Martech 예시로 설명하기 (`관찰`) — 이 책에 가장 좋은 설명:**
> 이탈 예측 모델의 피처 중 하나가 "지난 30일 구매 횟수"다.
> - **학습 시점** — 분석가가 웨어하우스에서 `SELECT COUNT(*) ... WHERE date BETWEEN ...`으로 뽑는다. 배치 SQL.
> - **서빙 시점** — 실시간 예측이 필요하니 백엔드 개발자가 Redis에서 카운터를 읽는다. 완전히 다른 코드.
>
> 두 계산이 **미묘하게 다르다.** 학습 쪽은 환불 건을 제외했는데 서빙 쪽은 포함한다. 학습은 UTC, 서빙은 KST. 모델은 오프라인 AUC 0.85인데 프로덕션에서는 형편없다. **이게 학습-서빙 스큐다.**
>
> **데이터 누수는 더 무섭다.** "2026-03-01에 이탈했는가"를 라벨로 쓰면서 피처는 오늘 기준 "지난 30일 구매 횟수"를 쓰면, 모델은 **이탈 이후의 행동까지 보고 학습한다.** 오프라인 성능은 환상적이고 프로덕션은 무너진다. **Martech의 이탈·전환 예측 모델이 실패하는 가장 흔한 이유다.**

**토스 TUES — 배치 세그먼테이션의 실증**:
- TUES = Toss User Engagement Segment. > "각 유저의 서비스 이용 패턴을 기준으로 비슷한 유저들끼리 묶어둔 세그먼트"
- **V1:** K-Means (하드 클러스터링) → **V2:** NMF (소프트 클러스터링) → **확률적 세그먼트 멤버십**
- **처리 모델: 배치 — 월 단위로 계산.** 실시간이 아니다.

[toss.tech/article/tues | **2026-06-16** | 저자 우찬희 | 검색 시점 2026-07-25] `1차 확인`

> 🎯 **이 사례가 §4-7의 완벽한 실증이다.** 대규모 플랫폼의 사용자 세그먼테이션이 **월 배치**로 돈다. **"모든 게 실시간이어야 한다"는 개발자의 직관이 틀렸다는 증거.** 그리고 V1→V2의 하드→소프트 클러스터링 전환도 흥미롭다 — **사람은 하나의 세그먼트에 딱 떨어지지 않는다.**

**AI/ML 층 지형 — 확인 상태를 반드시 구분하라:**

| 과제 | 접근 | 확인 상태 |
|---|---|---|
| 룩얼라이크 오디언스 | Two-tower 임베딩 + ANN 검색 | ✅ 토스 사례 확인 |
| CTR/전환 예측 | FM / DeepFM / DCN | ✅ 토스 사례 확인 |
| 세그먼테이션 | K-Means → NMF | ✅ 토스 사례 확인 |
| 이탈 예측 | 지도학습 분류 | ⚠️ **확인 불가 (미조회)** |
| Send-time optimization | 사용자별 최적 발송 시각 예측 | ⚠️ **확인 불가 (미조회)** |
| LLM 카피 생성 | 생성 모델 | ⚠️ **확인 불가 (미조회)** |
| 자연어 세그먼트 질의 (text-to-SQL) | LLM + 스키마 컨텍스트 | ⚠️ **확인 불가 (미조회)** |

> 🚨 **확인 불가 항목 처리 지침:** 아래 넷은 이 세션에서 **공개 1차 문서를 조회하지 못했다.** 업계에서 널리 언급되는 카테고리이지만 **어느 제품이 실제로 무엇을 쓰는지는 확인하지 않았다.** "이런 과제 영역이 있다" 수준으로 제한하거나 저술 시점에 별도 리서치를 요청하라. **특정 벤더가 이 기능을 제공한다는 서술은 이 리서치를 근거로 쓸 수 없다.**

> **이 절의 챕터 프레임:** **"Martech의 AI는 대부분 LLM이 아니다."** 2026년의 독자는 "AI"를 들으면 LLM을 떠올리지만, Martech에서 실제로 돈을 버는 ML은 **임베딩·랭킹·클러스터링**이다. 토스 사례 셋이 이걸 증명한다. LLM은 그 위에 얹히는 인터페이스 계층(카피 생성, 자연어 질의)이지 코어가 아니다.

### 4-10. 스키마·데이터 계약 — Martech에서 특히 치명적인 이유

**일반 백엔드에서 잘못된 데이터는 에러 로그를 남기고 알림이 울린다. Martech에서 잘못된 이벤트는 조용히 잘못된 캠페인을 발송한다.** `관찰` `[web-stack]`

구체적 사고 시나리오 — 책에 쓸 만한 것들:

1. **필드 이름이 바뀌었다.** 앱 릴리스에서 `purchase_amount` → `amount`. 세그먼트 SQL은 `purchase_amount`를 참조한다. NULL이 되고 **"고액 구매자" 세그먼트가 0명이 된다.** 아무도 에러를 안 본다 — 쿼리는 성공했다. 마케터는 3주 뒤에 "이번 달 VIP 캠페인 성과가 왜 없지?"라고 묻는다.
2. **타입이 바뀌었다.** `amount`가 숫자에서 문자열 `"39,900"`으로. 합계가 이상해지거나 조용히 0이 된다.
3. **단위가 바뀌었다.** 원 → 센트. "10만원 이상 구매자" 세그먼트가 **전 사용자**가 된다. 그리고 전 사용자에게 VIP 쿠폰이 나간다. **돈이 나가는 사고다.**
4. **이벤트가 중복 발송된다.** SDK 버그로 `purchase`가 두 번 찍히면 구매 횟수 기반 세그먼트가 전부 부풀려진다.

**공통점: 시스템은 아무 에러도 내지 않는다.** 파이프라인은 성공했고, SQL은 실행됐고, 캠페인은 발송됐다. **틀린 대상에게.**

> **개발자에게 통하는 프레임:** **이벤트 스키마 = API 스펙.** 백엔드 개발자는 API 응답 형식을 바꿀 때 버저닝하고, 컨슈머에게 알리고, 마이그레이션 기간을 둔다. 그런데 **같은 개발자가 프론트엔드 이벤트는 아무 협의 없이 바꾼다.** 왜? **이벤트에는 컴파일러도, 타입 체커도, 통합 테스트도 없기 때문이다.**
>
> **데이터 계약(data contract)은 그 빈자리를 메우려는 시도다:** 스키마를 저장소에 두고 PR 리뷰 → CI에서 호환성 검사 → 프로듀서 SDK가 스키마에서 타입 생성 → 런타임 검증 후 실패 스트림 격리 → 소비자 계보 추적.
>
> **Iceberg의 스키마 진화 규칙이 저장 계층에서 같은 문제를 다룬다** — 허용되는 변경을 **명시적으로 열거**한다는 점이 핵심이다. 이건 곧 "이 변경은 안전하고 저 변경은 안전하지 않다"는 계약이다.

> ⚠️ Iglu·Confluent Schema Registry의 스펙 세부(SchemaVer, 호환성 모드)는 **미조회 — `확인 불가`**.

### 4-11. 실제 회사 아키텍처 사례 (전부 발행일 확인)

**우아한형제들 — Transactional Outbox** [techblog.woowahan.com/17386/ | **2024-05-30** | 저자 김나은] `1차 확인`
> "데이터와 메시지 발행의 트랜잭션을 하나로 관리하여 데이터 정합성을 확보할 필요가 있었습니다."

Debezium MySQL 커넥터 기반 Transactional Outbox Pattern + Kafka Streams 실시간 집계.
> **§4-2와 직결:** "Kafka가 exactly-once를 지원한다"와 "DB 트랜잭션과 이벤트 발행의 원자성"은 **다른 문제**이고, 후자를 푸는 게 Outbox 패턴이다. Martech에서 "주문은 됐는데 이벤트가 안 갔다"(또는 반대)는 세그먼트를 조용히 망가뜨린다.

**LINE — userId를 파티션 키로** [engineering.linecorp.com/ko/blog/applying-kafka-streams-for-internal-message-delivery-pipeline | **2016-08-18** | 저자 Kawamura Yuto] `1차 확인`
> "Kafka Streams는 '라이브러리'입니다. 실행 프레임워크가 아니기 때문에 사용자가 수동으로 구동해야 합니다."

⚠️ **2016년 글 — 구버전 정보.** Kafka Streams API는 이후 크게 변했다. **고전 레퍼런스로만 인용하고 현재 API 서술의 근거로 쓰지 마라.** 다만 "userId를 파티션 키로"는 §4-2 순서 보장 원리의 실제 적용 사례로 여전히 유효하다.

**쿠팡 — 데이터 플랫폼 진화 4단계** [medium.com/coupang-engineering/big-data-platform-evolving-from-start-up-to-big-tech-company-... | **2022-08-03**] `1차 확인`
- Phase I (2010–2013): 관계형 DB / Phase II (2014–2016): Hadoop + MPP / Phase III (2016–2017): 클라우드 전면 이전 / Phase IV (2019–): 서비스 기반 모델

⚠️ **2022년 글 — 현행 아키텍처와 다를 수 있다. "진화 서사"로만 인용할 것.**

> 🎯 **책에서의 활용:** **"처음부터 이 스택을 다 짓지 않는다"**는 메시지의 근거. 독자가 §1-5의 스택 지도를 보고 압도되지 않게 하려면 **"쿠팡도 관계형 DB에서 시작했다"**는 사실이 필요하다. **책 초반이나 마무리 챕터의 안심 장치로 배치할 것.**

**미조회:** Netflix 실시간 분산 그래프(Medium 307 리다이렉트), 카카오 데이터정보플랫폼팀, 당근, Uber RAMEN — 전부 `확인 불가`.

---

## 5. 프라이버시 · 동의 · 아이덴티티 · 규제

> 🚨 **이 축은 2025~2026년에 여러 번 뒤집혔다. 기억으로 쓰면 거의 틀린다.** 아래 표를 먼저 읽어라.

### 5-0. ⚠️ 먼저 읽을 것 — 2026-07-25 기준 "기억과 다른" 핵심 5가지

| # | 흔한 오해 (2024년까지의 상식) | 2026-07-25 기준 실제 |
|---|---|---|
| 1 | "Chrome이 서드파티 쿠키를 없앤다" | **폐지 계획 자체가 철회됐다.** 2025-04-22 Google이 "현재 방식 유지" 발표, 별도 프롬프트도 안 띄운다 |
| 2 | "Privacy Sandbox가 쿠키를 대체한다" | **광고 API 대부분이 폐기됐다.** 2025-10-17 Topics·Protected Audience·Attribution Reporting 등 은퇴 발표, Chrome 144(2026-01-13)에서 deprecate, M150에서 제거 예정 |
| 3 | "IAB TCF는 v2.2가 최신" | **v2.3.** 2026-03-01부터 `disclosedVendors` 세그먼트 없는 TC String은 무효 |
| 4 | "정보통신망법 스팸 위반은 과태료" | **2026-07-07 시행 개정법(법률 제21305호)으로 과징금 도입** — 매출액 6% 이하 ⚠️수치 미검증 |
| 5 | "EU AI Act는 2026-08-02에 전면 적용" | AI Omnibus로 일부 고위험 규정이 **2027-12-02 / 2028-08-02로 연기**됐다 |

`[web-privacy]`

### 5-1. 브라우저 정책 — 변화 궤적

```
2020~2023  Privacy Sandbox 제안, 서드파티 쿠키 단계적 폐지 로드맵
2024-01    Chrome 사용자 1%에 서드파티 쿠키 기본 차단 테스트
   ↓
2025-04-22 반전 ①: "폐지 안 한다" — 현재 선택 방식 유지, 별도 프롬프트 없음
   ↓
2025-10-17 반전 ②: Privacy Sandbox 광고 API 대부분 은퇴 (같은 날 영국 CMA도 규제 약속 해제)
   ↓
2026-01-13 Chrome 144 stable — Protected Audience / Private Aggregation / Shared Storage deprecate
   ↓
2026-06-12 Topics API 사용률 4.9% of page loads (blink-dev 스레드 갱신)
   ↓
M150       제거 예정 (M150의 실제 stable 날짜는 확인 불가)
```

**① 폐지 철회 (2025-04-22)** — 저자 Anthony Chavez (VP, Privacy Sandbox), 원문:
> "not be rolling out a new standalone prompt for third-party cookies"
> "made the decision to maintain our current approach to offering users third-party cookie choice in Chrome"
>
> [privacysandbox.google.com/blog/privacy-sandbox-next-steps | **2025-04-22** | 검색 시점 2026-07-25] `1차 확인`

**② 기술 은퇴 (2025-10-17)** — 원문:
> "After evaluating ecosystem feedback about their expected value and in light of their low levels of adoption, we've decided to retire the following Privacy Sandbox technologies."

**은퇴 목록 (원문 열거):** Attribution Reporting API, IP Protection, On-Device Personalization, Private Aggregation, Shared Storage, Protected Audience, Protected App Signals, Related Website Sets, SelectURL, SDK Runtime, Topics
**계속 지원:** CHIPS, FedCM, Private State Tokens

[privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies | **2025-10-17** | 검색 시점 2026-07-25] `1차 확인`

**③ IP Protection의 번복 — 이 축을 기억으로 쓰면 안 되는 교과서적 사례:**
2025-04-22 글은 "IP Protection을 2025년 3분기에 런칭하겠다"고 했으나, 2025-10-17 status 페이지에서는 **Discontinue (Do Not Launch)**로 뒤집혔다. **6개월 만의 번복.** `[web-privacy]`

**④ 영국 CMA가 같은 날 규제 약속을 해제했다 (2025-10-17)** — Google이 서드파티 쿠키 제한 계획을 철회하면서 원래의 경쟁 우려가 성립하지 않는다고 판단.
> **개발자용 서사 포인트:** Privacy Sandbox는 "프라이버시 프로젝트"였던 동시에 "경쟁법 감시 대상"이었다. **규제가 풀린 날과 API가 죽은 날이 같은 날이다.**

**Safari ITP** [webkit.org/blog/10218/ | **2020-03-24** | 저자 John Wilander] `1차 확인`:
> "Cookies for cross-site resources are now blocked by default across the board."
> "ITP has aligned the remaining script-writable storage forms with the existing client-side cookie restriction, deleting all of a website's script-writable storage after **seven days** of Safari use without user interaction on the site."

7일 삭제 대상: IndexedDB, LocalStorage, Media keys, SessionStorage, Service Worker registrations and cache

> 🎯 **개발자 함의:** `localStorage`에 넣은 익명 방문자 ID가 **7일 뒤 사라진다.** 이게 "왜 우리 재방문 식별률이 계속 떨어지나"의 기술적 정답이다.

**CNAME 클로킹 방어** [webkit.org/blog/11338/ | **2020-11-12**] `1차 확인`:
> "ITP now detects third-party CNAME cloaking requests and caps the expiry of any cookies set in the HTTP response to 7 days."

**Firefox Total Cookie Protection** [blog.mozilla.org/.../firefox-rolls-out-total-cookie-protection... | **2022-06-14** (업데이트 2024-08-28)] `1차 확인`:
> "creating a separate 'cookie jar' for each website you visit"

차단이 아니라 **파티셔닝**이다. ⚠️ 기본값이 된 정확한 Firefox 버전 번호는 **확인 불가**.

**Apple ATT** — Apple의 "tracking" 정의 (원문, **이 정의가 챕터의 핵심 인용이다**):
> "Tracking refers to the act of linking user or device data collected from your app with user or device data collected from other companies' apps, websites, or offline properties for targeted advertising or advertising measurement purposes. Tracking also refers to sharing user or device data with data brokers."
>
> "Unless you receive permission from the user to enable tracking, the device's advertising identifier value will be all zeros and you may not track them as described above."
>
> [developer.apple.com/app-store/user-privacy-and-data-use/ | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

API: `requestTrackingAuthorization(completionHandler:)`, `trackingAuthorizationStatus`, Info.plist 키 `NSUserTrackingUsageDescription`. 가용성: iOS/iPadOS/tvOS 14.0, macOS 11.0, visionOS 1.0.

> 🚨 **개발자 함의 — 이게 §4-6 과병합과 직결된다:** 거부 시 IDFA가 `00000000-0000-0000-0000-000000000000`. **null이 아니라 0으로 채워진 유효한 형태의 UUID**다. 이걸 그대로 ID 그래프에 넣으면 **전 세계 거부 사용자가 한 사람으로 병합된다.**

⚠️ **SKAdNetwork의 deprecation 여부·버전·conversion value 비트 수는 전부 `확인 불가`** (Apple 문서 SPA 추출 실패). **챕터에 쓰지 마라.**

> 🎯 **가장 중요한 오독 방지:** Privacy Sandbox가 죽었다고 **서드파티 쿠키가 정상으로 돌아온 게 아니다.** 2026-07-25 기준: Safari는 **기본 전면 차단**(2020년부터), Firefox는 **사이트별 파티셔닝**(2022년부터), Chrome은 폐지는 안 하지만 CHIPS로 파티션 쿠키를 표준화. **즉 문제는 그대로인데 표준 해법만 없어졌다.** 그래서 압력은 오히려 커졌다 — 퍼스트파티 데이터, 로그인 기반 식별, 서버사이드 수집, 벤더 종속적 클린룸으로. **이게 §5-2~§5-5가 존재하는 이유다.**

### 5-2. 서버사이드 태깅과 중복 제거

**GTM 서버사이드** (공식 문서 원문):
> "Server-side tagging is a way to instrument your tags to measure user activity wherever it happens."
> **client 정의:** "Clients are adapters between the software running on a user's device and your server-side Tag Manager container. They receive measurement data from a device, transform that data into one or more events, process the data in the container, and package the results to be sent back to the device."
> "To send data in a true first-party context, you need to serve Google scripts, such as the Google Analytics library, from your own servers."
>
> [developers.google.com/tag-platform/tag-manager/server-side | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

**Meta CAPI 중복 제거 — 개발자가 실제로 짜는 부분** (원문):
> "We determine if events are identical based on their **ID** and **name**. So, for an event to be deduplicated:
> 1. In corresponding events, a Meta Pixel's `eventID` must match the Conversion API's `event_id`.
> 2. In corresponding events, a Meta Pixel's `event` must match the Conversion API's `event_name`."
>
> **시간 창 — 이 48시간이 챕터에 쓸 구체 수치다:**
> "If we find the same server key combination (`event_id` and `event_name`) **and** browser key combination (`eventID` and `event`) sent to the same Pixel ID within **48 hours**, we discard the subsequent events."
>
> [developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

> 🎯 **챕터에 쓸 개발자 서사:** 브라우저에서도 보내고 서버에서도 보낸다. 둘 다 보내면 같은 구매가 두 번 카운트된다. 그래서 주문 ID 같은 걸로 `event_id`를 만들어 양쪽에 똑같이 실어 보낸다 — **이게 martech 백엔드 개발자가 입사 첫 주에 만나는 코드다. 48시간 창을 넘기는 지연 배치 잡을 짜면 중복이 그대로 통과한다.**
>
> ⚠️ **정직한 표기:** Meta 공식 문서에는 **"광고 차단기 때문에 만들었다"는 문장이 없다.** 브라우저 제약을 CAPI의 존재 이유로 쓸 때는 Meta 공식 진술이 아니라 **업계 통설**로 표기하라.

**Segment 공식 가이드 — 무엇을 어디서 보내나** (원문 기반) `[web-gaps]`:
- **클라이언트사이드로:** page view·click·scroll, **UTM 파라미터·디바이스 정보·재방문자 쿠키 데이터**. 그리고 **"일부 분석 목적지는 쿠키에 의존하기 때문에 브라우저에서 보낸 이벤트만 받을 수 있다"** ← 개발자가 "다 서버에서 보내면 되지"라고 생각할 때 부딪히는 벽
- **서버사이드로:** **결제 이벤트**("accuracy for payments is so important"), 파생 지표. 원문: **"client-side data is fine for watching general trending, but it's never going to be perfect."** / **"sensitive information is also best kept out of browsers."**
- [raw.githubusercontent.com/segmentio/segment-docs/develop/src/guides/how-to-guides/collect-on-client-or-server.md | 발행일 미표기 (develop 브랜치) | 검색 시점 2026-07-25] `1차 확인`

> 🚨 **상충 — 병기하고 결론 내지 마라:** Google 공식 문서는 서버사이드 태깅의 이점으로 **"Unlock more detailed user privacy controls"**를 든다. WebKit은 CNAME 클로킹을 **추적 회피 수법**으로 규정하고 쿠키 수명을 7일로 캡한다. **같은 아키텍처가 벤더 문서에서는 프라이버시 강화로, 브라우저 벤더 블로그에서는 회피 수법으로 불린다.** 이 긴장 자체를 보여주는 게 정직하다.

### 5-3. 동의 관리 (CMP)

**IAB Europe TCF — 현재 v2.3** (기억이 흔히 "v2.2"라고 답하는 지점):
> "Starting 1st March, 2026: Any TC String created without the disclosedVendor segment will be deemed invalid."
>
> [iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/ | **2025-06-19** | 검색 시점 2026-07-25] `1차 확인`

v2.2 배경 (2023-05-16 출시): Purpose 3·4·5·6(개인화 광고/콘텐츠 프로필 생성·이용)에 대해 **Legitimate Interest를 법적 근거로 선택할 수 없게** 하고 consent만 허용. **"모두 동의" 원클릭 버튼이 있으면 재방문 시 "모두 철회" 원클릭도 동등하게 제공해야 함.**

**Google Consent Mode — 파라미터 전체** (공식 문서 원문 정의):

| 파라미터 | 원문 정의 |
|---|---|
| `ad_storage` | "Enables storage, such as cookies (web) or device identifiers (apps), related to advertising." |
| `ad_user_data` | "Sets consent for sending user data to Google for online advertising purposes." |
| `ad_personalization` | "Sets consent for personalized advertising." |
| `analytics_storage` | "Enables storage... related to analytics, for example, visit duration." |
| `functionality_storage` | "Enables storage that supports the functionality of the website or app, for example, language settings" |
| `personalization_storage` | "Enables storage related to personalization, for example, video recommendations" |
| `security_storage` | "Enables storage related to security such as authentication functionality, fraud prevention..." |

[developers.google.com/tag-platform/security/concepts/consent-mode | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

⚠️ **버전 표기 주의:** 이 공식 개요 문서는 **문서 제목에서 "v2"라는 라벨을 쓰지 않는다.** "Consent Mode v2"라고 쓸 거면 "2023년 11월에 `ad_user_data`·`ad_personalization` 두 파라미터가 추가된 개정"이라는 **사실 기준**으로 쓰는 게 안전하다.

**Basic vs Advanced — 개발자가 코드 한 줄로 정하는 갈림길** (원문):
- Basic: "Prevent Google tags from loading until a user interacts with a consent banner", "no data transferred to Google prior to user interaction" → "general model (less detailed modeling)"
- Advanced: "Google tags load when a user opens the website or app", 동의 전에도 "measurements without cookies" 전송 → "advertiser-specific model (more detailed modeling)"

> **Advanced 모드는 "동의 안 했는데도 뭔가 보낸다"이고, 그 대가로 더 정교한 전환 모델링을 받는다.** 이 트레이드오프를 개발자가 코드 한 줄로 정하게 되는 게 martech의 특징적 긴장이다.

**Global Privacy Control (GPC)** — **W3C Working Draft, 2026-06-11** (Recommendation 아님):
> "The `Sec-GPC` header field is a mechanism for expressing a person's general universal preference for a do-not-sell-or-share interaction in HTTP requests (for any request method)."
> ```
> Sec-GPC-field-value = "1"
> ```
> `Navigator`와 `WorkerNavigator`에 `globalPrivacyControl` readonly boolean으로 노출.
>
> [w3.org/TR/gpc/ | **2026-06-11 (Working Draft)** | 검색 시점 2026-07-25] `1차 확인`

> 🎯 **개발자 함의:** DNT(Do Not Track)와 달리 GPC는 **법적 구속력이 있다** — 캘리포니아에서는 반드시 존중해야 한다(§5-6). 즉 **`req.headers['sec-gpc'] === '1'` 한 줄이 법적 의미를 갖는 첫 헤더다.** DNT의 실패와 대비시키면 좋다.

### 5-4. 아이덴티티 레졸루션 — 벤더 4곳 대조 (1차 문서)

`[web-gaps]` — 각 셀은 해당 벤더 문서에서 fetch됨

| | **Segment** | **Adobe AEP** | **mParticle** | **Bloomreach** |
|---|---|---|---|---|
| **기능 이름** | Identity Resolution / Unify | Identity Service | IDSync | Customer identification / Merging |
| **식별자 구분** | identifiers (user_id, email, 기타) | identity namespace + value | identity priority 목록 | **hard ID / soft ID** |
| **우선순위 장치** | priority (user_id 1위, email 2위, 나머지 알파벳순) | **namespace priority** | **identity priority** (오름차순 순회) | hard ID > soft ID |
| **개수 제한** | user_id: 1, 그 외: 5 (기본값) | unique namespace = 그래프당 1개 | 확인 불가 | **soft ID 타입당 64개 (초과 시 LRU 제거)** |
| **오병합 방지 명칭** | blocked values | **"graph collapse" 방지** | (명칭 미확인) | hard ID 지정 권고 |
| **차단 대상 값** | `-1`, `null`, `anonymous`, 0/대시 패턴 | `user_null`, `not-specified` 등 | 확인 불가 | 확인 불가 |
| **익명→식별 전환** | child session → parent session 병합 | 확인 불가 | **profile conversion strategy** | 로그인/구매 시 자동 병합 |
| **문서 최신성** | 리포 최신 (날짜 미표기) | 2026-06-18 | 2026-07-16 | "9 days ago" |

> **이 표에서 나오는 서술 포인트 3개:**
> 1. **네 벤더 모두 "우선순위 + 개수 제한"이라는 같은 두 손잡이를 준다.** 이름만 다르다.
> 2. **오병합은 벤더가 인정하는 알려진 실패 모드다.** Adobe는 아예 **"graph collapse"**라는 고유 명칭까지 붙였다.
> 3. **구체적 그래프 크기 제한을 숫자로 명시한 건 Bloomreach(64)뿐이다.**
>
> 🎯 **차단 대상 값 목록(`-1`, `null`, `anonymous`)이 §5-1의 all-zero IDFA, §4-6의 과병합과 정확히 같은 문제다.** 세 축이 한 지점에서 만난다 — 챕터 구성에 유용.

**결정적 vs 확률적 매칭:**
- **결정적** = "이 사용자가 그걸 했다"(확실). 조인 키가 있는 `JOIN`.
- **확률적** = "이 사용자가 그걸 할 것이다"(신뢰구간). 유사도 임계값이 있는 `fuzzy match` — **임계값 하나 잘못 잡으면 서로 다른 사람이 한 프로필로 합쳐진다.**
- ⚠️ **LiveRamp/Adobe/Salesforce의 정의 원문은 본문 미조회 — 따옴표 인용 금지.** 위는 검색 요약 기반 요지 + 리서처 정리다.

**UID2** [unifiedid.com/docs/intro | **문서 최종 갱신 2026-07-23** — 검색 시점 이틀 전, 매우 신선] `1차 확인`:
> "UID2 is a framework that enables deterministic identity for advertising opportunities on the open internet"
> 라이선스: "All work and artifacts are licensed under the Apache License, Version 2.0"

⚠️ **미확인 — 챕터에 쓰지 마라:** raw UID2의 파생 절차(해싱·솔팅), 토큰 정의·회전 주기, RampID의 현재 상태. **"SHA-256 이메일 해시가 업계 표준 식별자다"라고 단정하지 마라 — 1차 근거를 확보하지 못했다.**

> **개발자용 논점 (`관찰`):** 이메일을 SHA-256으로 해싱해도 그건 익명화가 아니라 **가명화**다. 같은 이메일은 항상 같은 해시가 되므로 **여전히 조인 키다.** 이 구분이 §5-6의 가명정보 논의와 바로 연결된다.

### 5-5. 데이터 클린룸

**Google Ads Data Hub — 유일하게 구체 임계값이 공개된 소스** (원문):
> "Noise injection requires approximately **20 unique users** per result row. Difference checks require approximately **50 unique users** per result row. Queries of only click and conversion data require approximately **10 unique users** per result row."
>
> "events with zeroed or null user IDs don't count toward the aggregation threshold"
>
> [developers.google.com/ads-data-hub/guides/privacy-checks | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

> 🎯 **개발자 서사:** "SQL은 쓸 수 있는데 `SELECT` 결과가 20명 미만이면 행이 그냥 사라진다." **쿼리 결과가 조용히 비어 있는 걸 디버깅하는 게 클린룸 엔지니어링의 일상이다.** 그리고 `events with zeroed or null user IDs don't count` — **§5-1의 all-zero IDFA가 여기서 다시 등장한다.**

**AWS Clean Rooms** (원문):
> "AWS Clean Rooms helps you and your partners analyze and collaborate on your collective datasets to gain new insights without revealing underlying data to one another."
>
> 내장 통제: Analysis rules / **Cryptographic Computing for Clean Rooms** / Analysis logs / **Differential privacy** / AWS Clean Rooms ML
>
> 주목: "**ID namespaces for entity resolution**" — 클린룸과 아이덴티티 레졸루션이 같은 제품 안에서 만난다.
>
> [docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

**기술 기반 — 교차 확인 결과:**

| 기법 | 공식 문서에서 명시적으로 확인된 곳 |
|---|---|
| **차등 프라이버시** | AWS Clean Rooms ✅, Snowflake ✅ |
| **집계 임계값** | Ads Data Hub ✅ (20/50/10 명시), AMC ✅ (수치 없이 존재만) |
| **노이즈 주입 / difference check** | Ads Data Hub ✅ |
| **암호화 상태 연산** | AWS Clean Rooms ✅ |
| **PSI (Private Set Intersection)** | ❌ **어느 벤더 공식 문서에서도 그 이름으로 확인하지 못했다** |
| **k-anonymity** | ❌ **어느 벤더 공식 문서에서도 그 용어를 확인하지 못했다** |

> 🚨 **fact-checker 주의:** 클린룸을 설명할 때 **"PSI와 k-익명성을 쓴다"는 문장은 1차 출처로 뒷받침되지 않는다.** **특정 벤더 제품이 그걸 쓴다고 쓰지 마라.** "집계 임계값"과 k-익명성을 등치시키려면 **저자 해석임을 명시**하라.
> ✅ **다만 학술 개념으로 소개하는 건 가능하다** — §3-K(C-20)에 원 논문 서지가 있다: 차등 프라이버시(Dwork et al. 2006), k-익명성(Sweeney 2002), PSI(Pinkas et al. 2018), 로컬 DP(RAPPOR), 연합 학습(McMahan et al. 2017). **"이런 기법이 존재한다"와 "이 제품이 그걸 쓴다"를 분리해서 쓰라.**
>
> ⚠️ **Ads Data Hub의 20/50/10을 AMC나 Snowflake에 전용하지 마라.** 그쪽 수치는 `확인 불가`.

### 5-6. 규제 — 한국 기준이 특히 중요하다

#### 5-6-1. 개인정보 보호법 [조문 확인: **부분**]

**법령 메타:** **시행 2025-10-02, 법률 제20897호 (2025-04-01 일부개정)**
[law.go.kr/LSW/lsInfoP.do?lsId=011357 | 검색 시점 2026-07-25] `1차 확인 (법제처 원문)`

**law.go.kr 본문을 실제로 읽은 조문:**

| 조 | 제목 | 확인된 내용 |
|---|---|---|
| **제15조** | 개인정보의 수집·이용 | 수집 가능 사유 7가지 (동의 / 법률 특별규정 / 공공기관 소관업무 / **계약 이행** / 급박한 이익 / **정당한 이익** / 공공의 안전) |
| **제16조** | 수집 제한 | "개인정보처리자는 그 목적에 필요한 최소한의 개인정보를 수집하여야 한다." + **입증책임은 개인정보처리자 부담** |
| **제24조** | 고유식별정보 처리 제한 | **별도 동의** 또는 법령의 명시적 요구 |
| **제30조** | 처리방침 수립·공개 | 아래 각 호 |
| **제37조의2** | **자동화된 결정에 대한 정보주체의 권리** | 아래 |
| **제75조** | 과태료 | 아래 |

**제30조 제1항 각 호 (원문 인용) — 개발자에게 결정적인 7호:**
> 1. 개인정보의 처리 목적 / 2. 처리 및 보유 기간 / 3. 제3자 제공 / 3의2. 파기절차·방법 / 3의3. 민감정보 공개 가능성 / 4. 처리 위탁 / 4의2. 가명정보 처리 / 5. 정보주체 권리·행사방법 / 6. 개인정보 보호책임자 / **7. 인터넷 접속정보파일 등 자동수집 장치에 관한 사항** / 8. 대통령령으로 정한 사항

> 🎯 **7호가 쿠키·픽셀·SDK가 법령 문언에 직접 등장하는 지점이다.** **태그 하나 붙일 때마다 처리방침을 고쳐야 하는 법적 근거가 여기다.**

**제37조의2 (자동화된 결정)** — Martech에 직접 걸린다:
> 제2항 (원문): "정보주체는 개인정보처리자가 자동화된 결정을 한 경우에는 그 결정에 대하여 설명 등을 요구할 수 있다."
> 제4항 (원문): "개인정보처리자는 자동화된 결정의 기준과 절차, 개인정보가 처리되는 방식 등을 정보주체가 쉽게 확인할 수 있도록 공개하여야 한다."

⚠️ **시행일은 `조문 원문 미확인`** (부칙 미확인). 검색 결과는 2024-03-15이라 하나 검증 실패.

> 🎯 **Martech에 걸리는 지점:** 추천 알고리즘, 자동 등급 산정, 알고리즘 기반 가격 차등, 자동 심사 거절. **제4항의 "기준과 절차 공개" 의무는 곧 모델 카드/설명 문서를 제품 안에 넣으라는 요구다.**

**시행령 제17조 (동의를 받는 방법)** — ⚠️ **법률 제17조가 아니라 시행령 제17조다. 혼동하지 마라.** 동의가 유효하려면 **네 조건을 모두** 충족 (원문):
> 1. 정보주체가 자유로운 의사에 따라 동의 여부를 결정할 수 있을 것
> 2. 동의를 받으려는 내용이 구체적이고 명확할 것
> 3. 그 내용을 쉽게 읽고 이해할 수 있는 문구를 사용할 것
> 4. 동의 여부를 명확하게 표시할 수 있는 방법을 정보주체에게 제공할 것

> 🎯 **이 네 조건이 다크 패턴 금지의 법적 근거다.** "동의" 버튼만 크게 하고 "거부"를 흐리게 하면 1호·4호 위반이다. **CMP UI 구현은 디자인 문제가 아니라 컴플라이언스 문제다.**

**제75조 (과태료)** — 구간: 제1항 5천만원 / 제2항 3천만원(27개 호) / 제3항 2천만원 / 제4항 1천만원 이하.

**제2항 중 martech 직결 항목 (원문 인용):**
> "제16조제3항ㆍ제22조제5항을 위반하여 재화 또는 서비스의 제공을 거부한 자"

> 🎯 **선택적 동의를 거부했다는 이유로 서비스 제공을 거부하면 과태료 대상이다.** 즉 **"마케팅 수신 동의 안 하면 가입 불가"는 위법이다.** 선택 동의 체크박스는 **미체크 상태로도 가입 플로우가 끝까지 통과해야** 한다.
> ⚠️ 제16조 제3항·제22조 제5항의 **조문 원문 자체는 미확인.** 제75조 제2항에서 존재와 취지만 확인했다.

**시행령 제31조** — 처리방침에 들어갈 대통령령 사항 (원문): 1. 처리하는 개인정보 항목 / 2. **국외 이전 근거**(법 제28조의8) / 3. 안전성 확보 조치 / 4. **국외에서 국내 정보주체의 개인정보를 직접 수집·처리하는 경우 처리 국가명**

> 🎯 **4호는 역외 적용이다.** Martech SaaS를 해외에서 쓰는 한국 기업, 또는 한국 사용자를 받는 해외 서비스 양쪽에 걸린다. **벤더 리전을 바꾸면 처리방침을 고쳐야 한다 — 인프라 결정이 법무 문서에 물려 있다.**

#### 5-6-2. 정보통신망법 제50조 — **원문 확인 ✅**

**법령 메타:** **시행 2026-07-07, 법률 제21305호 (2026-01-06 일부개정)** — 검색 시점 기준 **18일 전 시행된 개정법**
[law.go.kr/LSW/lsLawLinkInfo.do?...lsJoLnkSeq=1000688185...&print=print | 검색 시점 2026-07-25] `1차 확인 (법제처 원문)`

> **제1항** "누구든지 전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려면 그 수신자의 명시적인 사전 동의를 받아야 한다."
>
> **제3항 (야간 제한 — 단서 포함 전문)** "**오후 9시부터 그 다음 날 오전 8시까지**의 시간에 전자적 전송매체를 이용하여 영리목적의 광고성 정보를 전송하려는 자는 제1항에도 불구하고 그 수신자로부터 **별도의 사전 동의**를 받아야 한다. **다만, 대통령령으로 정하는 매체의 경우에는 그러하지 아니하다.**"
>
> **제7항** 수신동의·수신거부·철회 의사표시 시 **처리 결과를 알려야 한다**
>
> **제8항** "제1항 또는 제3항에 따라 수신동의를 받은 자는 대통령령으로 정하는 바에 따라 **정기적으로** 광고성 정보 수신자의 수신동의 여부를 확인하여야 한다."

> 🚨 **가장 중요한 정정 — "밤 9시 이후 전면 금지"는 틀린 서술이다.**
> ① 금지가 아니라 **별도의 사전 동의** 요구다. ② 그리고 **단서가 있다** — "대통령령으로 정하는 매체의 경우에는 그러하지 아니하다."
> ⚠️ **면제 매체가 무엇인지, 앱 푸시가 어디에 속하는지는 시행령 원문 미확인 — `확인 불가`.** 2차 자료는 전자우편이라고 하나 검증되지 않았다. **이 리서치의 최우선 미결 항목이다.**

> 🎯 **챕터에 쓸 개발자 서사:** 마케팅팀이 "오후 10시에 푸시 보내면 열람률이 두 배"라고 한다. 개발자는 그때 스케줄러에 시간을 넣는 사람이다. 제50조 제3항은 **오후 9시~다음 날 오전 8시(11시간 창)**에 보내려면 **별도의 사전 동의**를 받으라고 한다. 일반 수신동의로는 안 된다. **즉 동의 테이블에 컬럼이 하나가 아니라 둘이다.**
> 그리고 제8항 — 정기적으로 재확인해야 한다. **동의는 한 번 받고 끝나는 boolean이 아니라 만료되는 상태다.**

⚠️ **2026-07-07 개정의 과징금 "매출액 6% 이하"와 전송 위탁 조문은 law.go.kr 원문으로 확인하지 못했다** (법무법인 뉴스레터 기준). **`(사실 확인 필요)` 마커를 붙이고 fact-checker가 재확인하게 하라.** 시행 18일차라 2차 자료 자체가 얇다.

#### 5-6-3. GDPR / CCPA / EU AI Act

**GDPR Article 6(1) 적법 근거 6가지** (EUR-Lex 원문 조각): (a) 동의 / (b) 계약 / (c) 법적 의무 / (d) 중대한 이익 / (e) 공익 임무 / **(f) 정당한 이익**

> 🎯 **martech의 핵심 쟁점은 (a) 동의 vs (f) 정당한 이익이다.** 광고 타겟팅을 정당한 이익으로 처리할 수 있느냐가 오랜 논쟁이고, **IAB TCF v2.2가 Purpose 3·4·5·6에서 LI를 아예 뺀 것(§5-3)이 그 논쟁의 실무적 결론이다.** 이 두 사실을 연결하면 강한 대목이 된다.

**Article 22 (자동화된 개별 의사결정)** — 개인은 "a decision based solely on automated processing...which produces legal effects concerning him or her or similarly significantly affects him or her"의 대상이 되지 않을 권리. 예외 3가지: 계약 필요 / 법률 허용 / **명시적 동의**.
> **한국 개인정보 보호법 제37조의2와 대응 관계다.** 나란히 놓으면 "한국법이 GDPR을 어떻게 참조했나"가 보인다.

**정보주체 권리 조문:** 열람 Art.15 / 삭제 Art.17 / 처리 제한 Art.18 / 이동권 Art.20 / 반대권 Art.21 / 국외 이전 **Chapter V (Art.44–50)**

⚠️ 수집 도구의 인용 길이 제한으로 **조문 전문은 확보하지 못했다.** 긴 인용이 필요하면 EUR-Lex를 직접 다시 열어라.

**CCPA/CPRA** (California AG 공식):
> "sharing for cross-context behavioral advertising, which is the targeting of advertising to a consumer based on the consumer's personal information obtained from the consumer's online activity across numerous websites"
>
> **GPC 존중 의무 (원문):** "Under law, it must be honored by covered businesses as a valid consumer request to stop the sale or sharing of personal information."
>
> [oag.ca.gov/privacy/ccpa | 발행일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

⚠️ "sale"의 법문 정의와 Civil Code 조문 번호(1798.120 등)는 **`조문 원문 미확인`**.

> 🎯 **EU vs 미국 모델 대비 (챕터 핵심 프레임):** GDPR/한국은 **opt-in**(동의를 받아야 처리 가능), CCPA/CPRA는 **opt-out**(처리하다가 소비자가 거부하면 중단). **그래서 같은 코드베이스로 두 지역을 서비스하려면 동의 모델 자체가 지역별로 분기된다.**

**EU AI Act 적용 일정** (European Commission 공식):

| 날짜 | 적용 내용 |
|---|---|
| 2024-08-01 | 발효 |
| 2025-02-02 | 금지 관행(Article 5) + AI 리터러시 의무 적용 |
| 2025-08-02 | GPAI 제공자 의무 개시 |
| **2026-08-02** | 투명성 규칙 적용 개시, 집행 개시 |
| 2026-12-02 | 비동의 성적 딥페이크·아동 착취물 관련 신규 금지 |
| **2027-12-02** | "Rules for high-risk AI systems in Annex III apply" |
| **2028-08-02** | "Rules for high-risk AI embedded in regulated products covered by Annex I apply" |

[ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act | 페이지 최종 갱신일 표기 없음 | 검색 시점 2026-07-25] `1차 확인`

> 🚨 **"AI Act가 마케팅 타겟팅을 규제한다"고 단정하지 마라.** 확인된 건 일정표와 Article 5의 금지 범주 개요뿐이다. **일반적인 광고 개인화·리타겟팅이 Article 5에 걸린다는 근거는 확인하지 못했다.** Article 5·Article 50 원문은 **미조회**. AI Omnibus 최종 변경 내역도 EU 공식 페이지에서 직접 확인하지 못했다 — **"2026년 7월 기준"임을 명시하라.**

### 5-7. 🎯 규제가 코드·데이터 모델에 남기는 흔적

> ⚠️ **이 표는 위 1차 출처들에서 도출한 저자 정리다.** 개별 문장에 1차 출처가 붙지 않는다. **수치나 "반드시 이래야 한다"는 단정 없이 설계 서술로 써라.**

| 코드·데이터 모델에 남는 것 | 파생 근거 |
|---|---|
| **동의 필드가 boolean 하나가 아니다** | Consent Mode 7종 + 정보통신망법 제50조 제1항/제3항이 요구하는 **두 개의 별도 동의**. 최소 `{목적, 지역, 채널, 시간대}` 축으로 쪼개진다 |
| **동의가 만료된다** | 제50조 제8항 "정기적으로 확인하여야 한다" → 동의 레코드에 `verified_at`이 필요하고 만료 재확인 배치가 필요하다 |
| **동의에 이력이 필요하다** | 제50조 제2항 철회 + 제7항 처리 결과 통지 → 현재 상태만이 아니라 **append-only 동의 이벤트 로그** |
| **다크 패턴 금지가 UI 코드 제약이 된다** | 시행령 제17조 4개 조건 + TCF의 "모두 동의 버튼이 있으면 모두 철회 버튼도" |
| **"동의 안 하면 가입 불가"를 못 짠다** | 제75조 제2항 → 선택 동의는 **미체크로도 가입이 끝까지 통과해야** 한다 |
| **처리방침에 데이터가 어느 나라에 있는지 써야 한다** | 시행령 제31조 제1항 2호·4호 → **인프라 결정이 법무 문서에 물려 있다** |
| **처리방침이 코드 배포와 연동된다** | 법 제30조 제1항 7호 → **태그 하나 추가 = 처리방침 개정** |
| **보존 기간(TTL)이 스키마의 일부다** | 제30조 제1항 2호, 제16조 최소 수집 원칙 |
| **삭제 요청이 파이프라인 전체를 관통한다** | GDPR Art.17 + 한국법 삭제권. 지워야 할 곳: OLTP DB, 이벤트 스트림 리텐션 구간, 웨어하우스 파티션, **컬럼 지향 포맷(행 단위 삭제가 비싸다 — §4-4)**, 백업 스냅샷, 검색 인덱스, **그리고 이미 벤더에 싱크된 오디언스** |
| **가명화는 삭제가 아니다** | SHA-256 이메일 해시는 여전히 조인 키다(§5-4) |
| **감사 로그가 제품 기능이다** | AWS Clean Rooms "Analysis logs ... help support audits" + 법 제37조의2 제4항 |
| **지역별 분기가 런타임에 존재한다** | opt-in(EU/한국) vs opt-out(캘리포니아) + 국외 이전 규정 → **다른 동의 모델, 다른 저장 리전** |
| **GPC는 헤더 한 줄인데 법적 구속력이 있다** | W3C `Sec-GPC: 1` + 캘리포니아 AG "it must be honored" |
| **널·플레이스홀더 ID가 프라이버시 사고를 만든다** | ATT all-zero IDFA + Ads Data Hub "zeroed or null user IDs don't count" + ID 그래프 과병합(§4-6, §5-4) |
| **48시간 dedup 창이 배치 잡 설계를 제약한다** | Meta CAPI 48시간(§5-2) |
| **7일 스토리지 캡이 익명 식별을 무너뜨린다** | Safari ITP 7일 + CNAME 쿠키 7일 캡 |

**커뮤니티가 제시한 실무 해법 2가지** `[community]`:

**크립토 셰레딩(crypto shredding)** — HN 30684445 / tybit / 2022-03-15:
> "At big tech companies I've seen and heard about, the answer is **crypto shredding. Encrypt all PII at rest with a per user data key. GDPR deletion requests can then delete the data key.** This isn't perfect, but it's a step in the right direction IMO. **Unfortunately I don't see it being feasible for a typical company anytime soon.**"

`커뮤니티 주장 (검증 필요)` — 다만 구체적이고 챕터에 쓸 만하다. 백업·로그·파이프라인 곳곳에 흩어진 데이터를 물리적으로 지우는 게 불가능에 가깝다는 문제를 **키만 지워서** 우회한다.

**소프트 삭제를 기본값으로 두지 마라** — HN 32158458 / jacksnipe / 2022-07-19:
> "The ONLY reason that you should avoid soft deletion is that **deleting things permanently in a soft-deletion-based system is hard and error prone. GDPR, among other regulations, requires that you be able to do this sometimes; and it requires that the data REALLY BE GONE.**"

> 🎯 **소프트 삭제가 기본값인 웹 백엔드 습관이 Martech에서는 규제 위반이 된다.** 독자(웹 개발 경험자)의 **기존 습관이 깨지는 지점** — 좋은 챕터 재료다.

**"수집과 처리는 다른 것"** — Deliveroo–Braze 논쟁 (HN 18989137 / scrollaway / 2019-01-24):
> "**So the question is, is the data sent to Braze exclusively for marketing? More critically: If it is collected regardless of consent, does processing still follow consent? (Collecting and processing of data are two different things)**"

> 🎯 이 구분이 **동의 신호를 이벤트 파이프라인 어디까지 전파해야 하는지**를 결정하는 기준이다. 그리고 이 논쟁의 대상이 **Braze**라는 점이 의미 있다 — **독자가 입사할 수도 있는 회사가 프라이버시 논쟁의 한복판에 있다.**
> ⚠️ 세 명 모두 **법률 비전문가의 GDPR 해석**이다. `커뮤니티 주장 (검증 필요)`

---

## 6. 대표 사례 — Insider One (공개 문서로 읽는 카테고리의 대표)

> **이 책은 Insider를 "공개 문서로 읽는 카테고리의 대표 사례"로 다룬다.** 아래는 전부 Insider 자사 공개 자료 1차 확인이며, **내부 아키텍처에 대한 주장은 Insider가 스스로 공개한 것이 아니면 "공개 자료 없음"으로 기록했다.**

### 6-1. ✅ 확인된 사실 vs ❌ 확인 불가

| 항목 | 확인 내용 | 출처 |
|---|---|---|
| 현재 브랜드명 | **"Insider One"** — 공식 도메인 `insiderone.com`, 문서 `academy.insiderone.com` | insiderone.com |
| 자기 규정 | "#1 Platform for AI-Powered Customer Engagement", "the leading Agentic Customer Engagement Platform" `벤더 자체 주장` | insiderone.com |
| 제품 모듈 | Insider One AI™, Customer Data Management, Personalization, Journey Orchestration, Reporting & Data, Behavioral Analytics | insiderone.com |
| AI 제품명 | **"Insider One AI™"**(우산 브랜드), **"Agent One™"**(에이전틱 AI) | insiderone.com |
| 채널 | Web, Email, Site Search, Conversational CX, WhatsApp, Web Push, InStory, App, SMS & RCS | insiderone.com |
| CDP 모듈 | **Unified Customer Database (UCD)** — "the core Customer Data Platform (CDP) that powers all Insider One products" | academy (2026-04-22) |
| Series E | $500M, 리드 General Atlantic, 발표 **2024-11-01**, "28 countries across five continents" | insiderone.com/news |
| 고객 규모 주장 | "1,500+ customers across the globe, including Nike, Samsung, L'Oreal, Unilever, Allianz, Walt Disney, ING Group, Toyota, Singapore Airlines, and GAP..." `벤더 자체 주장` | insiderone.com/news |

**❌ 확인 불가 (조회했으나 1차 근거 못 찾음):**

| 항목 | 상태 |
|---|---|
| 설립 연도 | **확인 불가** — `insiderone.com/about/`은 채용 페이지였고 창업 정보 없음. 보도자료 boilerplate에도 없음 |
| 본사 소재지 | **확인 불가** — 보도자료 발신지가 New York으로 표기됐을 뿐 "headquarters" 명시 없음 |
| 총 누적 투자액 / 기업 가치 / 유니콘 등극 시점 | **확인 불가** (1차 소스에서 NOT FOUND) |
| 한국 법인/오피스 유무 | **확인 불가 (미조회)** |
| **내부 아키텍처 (DB 종류, 스트리밍 엔진 등)** | **공개 자료 없음 — 추정 금지** |

> 🚨 **중요:** 설립연도 2012 / 이스탄불 본사 / 2022년 유니콘 / 누적 $772M 같은 숫자는 **검색 결과 요약(Tracxn·PitchBook·Tech.eu 등)에만 있었고 1차 페이지에서 확인하지 못했다.** 책에 쓰려면 재확인이 필요하다. 지금 상태로는 `(2차 인용, 미검증)`.

### 6-2. UCD — Insider의 CDP 레이어 (핵심 개념 3종, 문서 원문)

- **Identifiers** — "anything specific to the user" (이메일, 전화번호, user ID 등). 여러 소스의 데이터를 하나로 묶는 열쇠.
- **Events** — "User actions across all online and offline channels, including add-to-carts, purchases, visits, and logins." 이벤트는 파라미터를 가질 수 있다.
- **Attributes** — "enable you to collect users' information, such as age, gender, birthday, and singular items for each user"

[academy.insiderone.com/docs/unified-customer-database-ucd | 페이지 표기 2026-04-22 (문서 사이트 표기 — 최초 발행일/갱신일 구분 불가) | 검색 시점 2026-07-25] `1차 확인`

> **개발자용 멘탈 모델:** identifiers = 조인 키 / events = append-only 시계열 / attributes = 사용자 행의 컬럼. **Segment의 `userId`+`traits`+`track` 3분할과 거의 같은 구조다**(§1-2 대조표).

### 6-3. 웹 SDK — 개발자가 실제로 만지는 표면

```html
<script async src="//{partnerName}.api.useinsider.com/ins.js?id={partnerId}"></script>
```

```javascript
window.InsiderQueue = window.InsiderQueue || [];
// 푸시 패턴: window.InsiderQueue.push({type: 'method_type', value: {...}})
```
큐는 Insider 태그가 로드되기 **전에** 정의되어야 한다.

**사용자 속성 스키마 (`type: 'user'`)** — 필수 식별자 최소 1개: `uuid`, `email`, `phone_number`

| Field | Type | Sample |
|-------|------|--------|
| `uuid` | String | "INS123" |
| `email` | String | "jdoe@useinsider.com" |
| `phone_number` | String (E.164) | "+120394879878" |
| `birthday` | Datetime | "2000-01-20T00:00:00Z" |
| `country` | String (ISO-3166 alpha-2) | "ID" |
| `email_optin` / `sms_optin` / `whatsapp_optin` | Boolean | true |
| `gdpr_optin` | Boolean (GDPR 준수 시 필요) | true |
| `custom` | Object | {"membership": "Silver"} |

**페이지 타입 메서드:** `home` → `home_page_view` / `category` → `listing_page_view` (`breadcrumb` 배열 필요) / `product` → `product_detail_page_view` / `cart` → `cart_page_view` / `purchase` → `confirmation_page_view` / `other` → `other_page_view`

**이벤트 메서드:** `add_to_cart` / `remove_from_cart` / `custom_event`(`event_name` 필수) / `init`("Critical initialization trigger (must fire once per page after user/page data)") / `currency`

[academy.insiderone.com/docs/insider-web-sdk-integration-guide | 페이지 표기 2026-07-23 | 검색 시점 2026-07-25] `1차 확인`

> 🎯 **책에 쓸 만한 관찰 — 브랜드는 바뀌었지만 API는 안 바뀌었다.**
> 브랜드·문서 도메인은 `insiderone.com`인데 **태그 스크립트 호스트는 여전히 `useinsider.com`**이고, 샘플 이메일도 `jdoe@useinsider.com`, API 호스트도 `unification.useinsider.com`, GitHub 조직 slug도 `useinsider`(표시명만 InsiderOne)다. **리브랜딩이 프레젠테이션 레이어에만 적용되고 데이터 평면은 레거시 도메인을 유지하는, 실무에서 아주 흔한 패턴.** (2026-07-25 시점 관찰) `관찰`

### 6-4. Upsert User Data API — 데이터 인입의 핵심

- **엔드포인트:** `POST https://unification.useinsider.com/api/user/v1/upsert`
- **헤더:** `X-PARTNER-NAME`, `X-REQUEST-TOKEN`, `Content-Type: application/json`

**요청 바디:**
- 최상위: `skip_hook`(boolean — 임포트 데이터가 Architect 저니를 트리거할지 제어), `error_callback_endpoint`, `users`(array, **required**)
- user 객체: `insider_id` **또는** `identifiers` (둘 중 하나 필수), `attributes`, `events`, `not_append`/`append`
- event 필드: `event_name`(**required**), `timestamp`(**RFC 3339**, **required**), `event_params`, `event_group_id`(purchase/cart_page_view에 required)

**배치·레이트 제한:** 요청당 최대 **1,000 users** / **25,000 requests/minute** / 요청 크기 **최대 5 MB**

[academy.insiderone.com/docs/upsert-user-data-api | 페이지 내 참조 날짜 2026-07-24 | 검색 시점 2026-07-25] `1차 확인`

**API 레이트 리밋 — 개발자가 가장 먼저 부딪히는 벽** (2026-07-12 문서 표기 기준):

| API | 리밋 |
|---|---|
| Upsert User Data | 25,000 req/min |
| **Export Raw User Data** | **1 request per day** |
| Delete User Profiles | 10,000 req/min |
| Delete User's PII Data | 500 req/min |
| Update Identifiers | 2,000 req/min |
| **Send Transactional Emails** | **9,000 requests per second** |
| **Create Email Campaigns** | **1 request per second** |
| Launch Single Web Pushes V2 | 6,000 req/min |
| Send Targeted App Pushes | 10,000 req/min |
| WhatsApp Transactional | 1,000 req/sec |
| SMS Transactional Bulk | 5 req/sec |
| Recommendation APIs | 1,000 calls/min |

[academy.insiderone.com/docs/api-rate-limits | 페이지 표기 **2026-07-12** | 검색 시점 2026-07-25] `1차 확인`

⚠️ **버전·수치 규율:** 위 숫자는 전부 **2026-07-12 문서 표기 기준**이다. 레이트 리밋은 벤더가 예고 없이 바꾼다. **책에 넣을 때 "2026년 7월 문서 기준"을 반드시 병기하라.**

> 🎯 **이 비대칭이 마테크 아키텍처의 본질을 드러낸다** (`관찰`, 수치만 사실):
> - **인입은 크게 열려 있다:** Upsert 25,000 req/min, 요청당 1,000 users, 5MB
> - **추출은 극단적으로 좁다:** Export Raw User Data **1 request per day**
> - **트랜잭셔널이 캠페인보다 훨씬 넓다:** Transactional Email 9,000 req/sec vs Create Email Campaign 1 req/sec
>
> **데이터는 들어오기 쉽고 나가기 어렵다(=락인). 그리고 "한 명에게 즉시 보내는 것"과 "모두에게 한 번에 보내는 것"은 완전히 다른 시스템이다.**

### 6-5. 규제가 API 표면의 절반을 차지한다

User Data API 6종: Upsert / Get User Profiles / Export Raw User Data / **Delete User Attribute** / **Update Identifiers** / **Delete Identifiers** (+ 별도 Delete User Profiles, Delete PII)

> 🎯 **관찰:** 6개 중 **4개가 삭제/수정 계열**이다. **CDP API 표면의 절반이 GDPR·개인정보 삭제 요구를 처리하기 위한 것** — 개발자 독자에게 **"마테크에서 규제는 부가 기능이 아니라 API 설계의 절반"**이라는 점을 보여주는 근거다. `관찰`

### 6-6. 기타 확인 사항

- **모바일 SDK:** iOS 모듈 버전 InsiderMobile **v15.1.1**, InsiderGeofence v1.2.4, InsiderMobileAdvancedNotification v2.4.0. ⚠️ **상충:** 리포 릴리스 태그는 **v1.9.1**로 모듈 버전과 다른 체계다 — 인용 시 어느 쪽인지 명시할 것. [github.com/useinsider/Insider-iOS-SDK]
- **문서 사이트가 `/llms.txt` 인덱스를 제공한다** — AI 에이전트용 문서 색인을 갖춘 최신 문서 사이트 패턴.
- **Architect** = 저니 오케스트레이션 제품명 (Upsert API의 `skip_hook` 설명에 "Architect journeys"가 등장해 **간접 확인**). ⚠️ `architect-overview` 문서는 **404** — 세부 기능 `확인 불가`.
- **Eureka** — 제품명만 확인, 기능 `확인 불가` (미조회).

> ⚠️ **문서 사이트 타임스탬프의 의미:** Insider Academy는 다수 페이지가 Published와 Updated가 **동일 초 단위 타임스탬프**를 갖는다(예: 양쪽 다 2026-04-22T09:21:05Z) → **빌드/렌더 시각일 가능성이 높다. 문서 사이트 날짜를 "발행일"로 인용하지 마라.** 이 레퍼런스는 전부 `페이지 표기`로만 기록했다.

---

## 7. 한국 시장 · 커리어

> ⚠️ **표본 편향을 먼저 밝힌다** `[community]`: pain point는 **영어권 HN 비중이 크다**(Reddit 전면 차단이 주원인). **한국 현장 목소리는 개인 커뮤니티 글이 아니라 벤더 기술블로그·채용 공고에서 주로 확보됐고, 이건 이해관계가 있는 소스다. 챕터에서 이 편향을 감춰서는 안 된다.**

### 7-1. 🎯 가장 중요한 발견 — Martech 벤더사에서 "기술을 아는 사람"의 자리는 개발자 자리보다 넓다

**AB180 채용 공고 분석 — 반드시 스냅샷 시점과 함께 인용하라:**

> **2026-07-25 원티드 active 공고 24건 기준**, 순수 소프트웨어 엔지니어 공고는 **3건**(Backend Engineer - Data Pipeline, DevOps Engineer, Endpoint Security Engineer), 기술을 쓰지만 개발자가 아닌 직무는 **7건**(Solution Architect, Technical Support Manager ×2, CSM-Onboarding, CSM-Amplitude & Braze, QA, Technical Writer)이다.

`관찰 사실` — **이 비율 자체가 이 책의 핵심 논지 중 하나다.**

> 🚨 **인용 규율:** 이 문서에서 가장 자주 인용될 숫자다. **채용 공고는 마감되면 사라진다.** "24건 중 3건"을 쓸 때는 **반드시 "2026년 7월 원티드 active 공고 기준"을 문장 안에 넣어라.** 시점을 뗀 채로 옮기면 검증 불가능한 주장이 된다.

**해외에서도 같은 패턴이 대량 반복된다** (Greenhouse API, 2026-07-25 조회 — Braze 236건 / Klaviyo 152건 / Twilio 183건 / Hightouch 70건):

| 직무군 | 실제 공고 타이틀 |
|---|---|
| **Solutions Engineer / Consultant (프리세일즈)** | Hightouch 7건(Enterprise East/West, Mid-Market, EMEA, Senior, Manager ×2), Braze `Solutions Consultant` ×5(도시별)·`Solutions Engineer, Security & Privacy` ×4·`Solutions Architect`·`Technical Architect`·`Senior Lead Field Architect` ×4, Twilio `Presales Engineer/Architect` 6건, Klaviyo 3건 |
| **Technical Account Manager (TAM)** | Braze ×5(Chicago/SF/Toronto/NYC/Austin), Hightouch ×4, Twilio ×6 |
| **Forward Deployed 계열 — 2026년 현재 확산 중** | Hightouch `Forward Deployed Analytics Engineer`(2026-07-21 갱신)·`Forward Deployed Marketing Data Scientist`, Twilio ×2, Braze `Forward-Deployed Data Scientist`(Tokyo/Paris/London), **채널톡(국내)** `Forward Deployed Engineer` |
| **Deliverability 전담 — 별도 커리어 트랙** | Braze `Senior Email Deliverability Consultant` ×4(2026-07-17 갱신)·`Team Lead, Email Deliverability` ×4, Klaviyo `Deliverability Strategist`, Hightouch `Deliverability Specialist` |
| **Analytics Engineer** | Klaviyo(Boston, 2026-07-23 갱신), Twilio `Staff, Analytics Engineer`, Hightouch |

**제품 도메인이 그대로 팀 이름인 엔지니어 직무 (Martech 특유):**
- Twilio: **`Principal Software Engineer - Identity Graph`**, **`Software Engineer, (L2) CDP`**, `Software Engineer, Identity`, `Software Engineer (L3) Data Substrate`, `Staff Software Engineer (L4) Data Platform`
- Klaviyo: **`Senior Software Engineer - Profiles, Lists and Segments`**, `Lead Software Engineer, Messaging Infrastructure`, `Lead Product Manager, Core Data`
- Braze: `Engineering Manager, Data Streaming`, `Engineering Manager, Email` ×5, `Senior Software Engineer, Content Cards`
- Hightouch: `Software Engineer, Streaming Systems`, `Principal Engineer, Streaming Systems`, `Software Engineer, Destinations`, `Software Engineer, Control Plane`

> 🎯 **이 세 타이틀만 봐도 Martech 백엔드의 핵심 문제가 드러난다:** `Identity Graph`, `CDP`, `Profiles, Lists and Segments` — **아이덴티티 해석과 프로필/세그먼트 저장·조회. 일반 웹 백엔드에는 없는 도메인이다.**

### 7-2. 국내 채용 공고 원문 — 스택의 구체적 표본

**빅인사이트 Data Platform Engineer** (원티드 ID 359453, active) — **국내 Martech 데이터 플랫폼 스택의 가장 구체적인 표본:**

주요업무 (원문 발췌):
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
• AWS 비용 구조를 고려한 리소스 최적화
```

**"What Makes A Strong Fit" (원문 — 그대로 챕터에 쓸 만하다):**
```
• 데이터 파이프라인과 Kubernetes 운영을 함께 볼 수 있는 분
• 실패한 워크플로우를 단순 재실행하지 않고 원인과 재발 방지까지 보는 분
• DB, 스토리지, 워크플로우, 인프라를 분리해서 보지 않고 전체 병목을 추적할 수 있는 분
• 배치 처리의 idempotency, backfill, retry, 중복 처리 문제를 중요하게 생각하는 분
• 비용과 안정성 사이의 트레이드오프를 숫자로 판단할 수 있는 분
```

> 🎯 **"실패한 워크플로우를 단순 재실행하지 않고 원인과 재발 방지까지 보는 분"** — 이 한 줄이 Martech 데이터 엔지니어의 일상을 요약한다. **재실행으로 때우고 싶은 유혹이 상시 존재한다는 뜻이기 때문이다.**
>
> 📌 **이 JD 하나가 §4의 스택 지도를 실증한다:** MongoDB(프로필은 스키마리스) + ClickHouse(분석은 OLAP) + Vitess/MySQL(트랜잭션은 샤딩된 RDBMS) + Iceberg(레이크) + Flink(스트리밍). **왜 저장소가 네 벌인지**를 §4-4의 조회 패턴 축으로 설명할 수 있다.

**AB180 Backend Engineer - Data Pipeline** (원티드 ID 330977, active) — 우대사항 원문:
```
• Kafka 또는 Queue를 활용한 분산 처리 개발 경험이 있으신 분
• Grafana, New Relic, Sentry와 같은 모니터링 도구 사용 경험이 있으신 분
• 더 적은 비용으로 시스템을 운영하는 비용 관리 경험이 있으신 분
• 시스템이 휴먼 에러를 잡아줄 수 있는 환경을 구축해 보신 분
```
자격요건: 3년 이상 웹 백엔드, **Kotlin 또는 Golang**, 클라우드(AWS/GCP/Azure), 테스트 코드

**AB180 DevOps Engineer** (ID 365460) — 4대 업무 중 하나가 **"비용 가시성을 높이고 효율을 개선하는 FinOps"**.
> 📌 **FinOps가 DevOps JD의 4대 업무로 명문화돼 있다. Martech에서 비용은 곁가지가 아니라 직무 정의다.**

**마티니아이오 솔루션 컨설턴트** (ID 349957) — 주요업무 원문 발췌:
```
이벤트 택소노미(Event Naming, Property 구조) 설계
SDK / Server-side / Hybrid 트래킹 전략 수립
데이터 불일치, Attribution 오류, 이벤트 누락 등 트러블슈팅
```
> 🎯 **이 JD는 §7-4의 pain point 목록을 그대로 업무 정의로 옮겨놓은 문서다.** "데이터 불일치, Attribution 오류, 이벤트 누락 트러블슈팅"이 **직무기술서에 명시**돼 있다는 건, 그게 예외 상황이 아니라 **상시 업무**라는 뜻이다. **챕터 오프닝으로 강력하다.**

**채널톡 Forward Deployed Engineer** (ID 324639) — 자격요건 **첫 항목이 기술이 아니다**:
```
• 회복 탄력성 : 복잡한 이해관계와 반복되는 실패 속에서도 빠르게 회복하고,
  새로운 해결책을 집요하게 탐색하는 분
```
> 📌 자격요건 5개 중 **기술 스택 언급이 0개**이고, 전부 태도·커뮤니케이션·학습 민첩성이다.

### 7-3. 팀 구성과 역할 — AB180 엔지니어링 블로그 (1차)

> ⚠️ **게시일이 페이지에 없다 (`확인 불가`).** 본문에 "백엔드 엔지니어링 그룹 총 19명, Data Pipeline 팀 7명" 같은 조직 수치가 있는데 **시점 미상**이므로 쓸 거면 "인터뷰 당시"라고 명시할 것.

**역할 경계가 흐리다 — 이 책의 중요한 논지** (원문):
> "저를 포함한 **AB180 백엔드 그룹의 엔지니어 분들은 흔히 말하는 백엔드, 데브옵스, 데이터 엔지니어가 하는 일을 복합적으로 하고 있습니다.** Data Pipline팀도 마찬가지인데요, 데이터 수집부터 처리, 적재 관리 등 흔히 데이터 엔지니어가 하는 영역까지 담당하고 있습니다."

> 🎯 독자(웹/앱 개발 경험자)가 가장 궁금해할 **"나는 어느 직무로 가야 하나"**에 대한 현실적 답: **경계가 생각보다 흐리다.**

**무엇이 중요한 일인가 — 안정성과 비용** (원문):
> "많은 고객사가 월 수억 원에 달하는 마케팅 예산을 집행하고 비용을 정산할 때 사용하는 데이터를 다루기 때문에, **저희 팀에게는 안정성과 효율성이 가장 중요한 키워드입니다.** ... **보통 최적화나 안정화 작업은 잘 보이지도 않고, 설명하기도 쉽지 않아 외부에서는 잘 몰라줄 때가 많지만**, 정말 중요한 작업이고 나름의 성취감도 커서 보람을 많이 느낍니다. 특히 큰 장애를 잘 방지했거나 큰 비용 절감을 이뤄낸 작업을 했을 땐 **"오늘 밥값 했다" 하며 자랑할 때가 많아요.**"

> 🥇 **"오늘 밥값 했다" — 챕터 오프닝 후보 1순위.** 한국어 원문의 생활감이 살아 있고, **"Martech 개발자의 성취는 눈에 안 보이는 곳에 있다"**는 이 책의 주제를 한 문장으로 압축한다.

**신입의 첫 벽** (원문):
> "제가 처음 입사했을 때 **비즈니스 로직이 어렵다고 느꼈고, 동시에 이해가 되지 않는 로직이 많았습니다.** 그래서 당시 CTO, CPO님 자리에 찾아가 옆에 앉아서 로직에 대해 토론하는 시간을 자주 가졌는데..."

> 🎯 **대상 독자에게 직접 꽂히는 대목: "기술이 어려운 게 아니라 비즈니스 로직이 어렵다"**가 Martech 신입의 첫 벽이다.

**개발자와 마케터의 협업 마찰 — 프로세스 문서로 확인** [blog.martinee.io/post/designing-perfect-event-taxonomy-naver-series | **2024-05-30** | 저자 문소윤] `1차 확인`:

이벤트 택소노미 구축 8단계: ①목적·방향성 → ②주요 지표 → ③사용자 여정 스케치 → ④이벤트·프로퍼티 설계 → **⑤마케터 협의** → **⑥개발자 협의** → ⑦QA 테스트 → ⑧최종 수정

> "**5-6번 프로세스의 경우 수차례 반복될 수 있습니다.** 모든 담당자들과의 합의점이 반영된 택소노미를 설계하기까지란 많은 소통과 협의가 필요한 데다, **마케터의 요구사항을 운 좋게 완벽히 반영했다고 하더라도 기능상 점검과 동작 검증이 불가피하기 때문입니다.**"

> 📌 벤더의 자사 방법론 홍보 글이라는 점은 감안해야 한다 `이해관계 있음`. 다만 **"마케터 협의 ↔ 개발자 협의가 수차례 반복된다"를 벤더 스스로 프로세스 문서에 적어놓은 것**은, 그 반복이 예외가 아니라 **표준**이라는 방증이다.

### 7-4. 현장 pain point — 반복 관찰 순위

> ⚠️ 건수는 **이 세션에서 실제로 열어본 소스 중** 해당 불만이 등장한 독립 소스 수다. **"업계 순위"가 아니라 "이 표본에서의 빈도"다.**

**🥇 최고 오프닝 재료** — HN 39103276 / shkan / **2024-01-23** (⚠️ **댓글 0개 — 커뮤니티 합의가 아니라 한 실무자의 토로**):
> "It's a loop of integration, testing, fixing, and doing it all over again."
> "**It's not a job; it's a tech Groundhog Day where you wake up to the same problems, over and over. Bugs become your alarm clock, and every integration feels like déjà vu.**"
> "Imagine your data as a puzzle, but here's the catch: **the pieces keep changing shapes.**"

> 📌 이 글은 **책 전체의 테제를 한 실무자가 먼저 말해버린 문서**다. 오프닝으로 쓰되 **"댓글 0개인 개인 토로"임을 밝히는 게 정직하다.**

**1위. 어트리뷰션은 원리적으로 안 맞는다** — HN 5개 스레드 / 6명 (+ 채용공고 2건). §3-M 참조.

**2위. 이벤트 택소노미가 망가진다** — HN 1 + 벤더 문서 1 + 채용공고 1 + GitHub 이슈 계보 1
> `관찰 사실`: Snowplow 레포에서 스키마 검증 관련 이슈가 **2014년부터** 확인된다(#611 "Add JSON Schema-based validation for incoming unstructured events", 2014-04-01 등 9건). **"스키마를 강제하지 않으면 이벤트 데이터가 썩는다"는 문제의식이 10년 넘은 것.** ⚠️ 이슈 본문은 미조회(rate limit) — 제목·번호·날짜만 확인.

**3위. reverse ETL의 운영 고통과 사업적 취약성** — HN 3개 스레드 / 5명
> "Ultimately reverse ETL is just a technology (basically from SQL to APIs). **The quality/correctness of data is someone else's headache.** I've been there and done that, and **reverse ETL is a feature-product with huge churn. See how Hightouch pivoted hard from that into CDP.**"
> — HN 43861360 / throwaway7783 / **2025-05-01** `커뮤니티 주장 (검증 필요)`
>
> 📌 이 2025년 관측은 **사후적으로 맞았다** — Hightouch의 2026년 자사 소개가 "Agentic Marketing Platform powered by the industry-leading Composable CDP"임을 이 세션에서 확인했다.

**3-C위. SDK가 계속 늘어난다 — 앱이 느려지는 조직적 이유** — HN 43668825 / Swizec / **2025-04-12**:
> "In my experience of building consumer web applications, they all start fast.
> Then someone says **"We need to track every interaction in mixpanel. What's even the point if we don't know it happened"**.
> Then the sales team says **"We need to track in Salesforce, nobody on our team looks at mixpanel"**
> Then the marketing team goes **"We must consolidate in google analytics, nothing else fits our usecase"**
> Then the other product team says **"We need Amplitude"**
> Then the re-engagement marketing team goes **"Braze for us please..."**"

> 🥉 **챕터 오프닝 후보 3순위 — 그리고 이 책 독자에게 가장 직접적이다.** "왜 우리 앱에는 추적 SDK가 다섯 개나 붙어 있는가"에 대한 답이 **기술이 아니라 조직**이라는 것.
>
> **호응하는 1차 근거** — HN 20299880 / dlevine / 2019-06-27 (story: "Building Lyft's Marketing Automation Platform"):
> > "**most companies buy 2-4 products for their marketing stack (CDP, Marketing Automation, attribution, and analytics).** ... **Each company does marketing enough differently that there isn't a single product that could solve the problem end-to-end for everyone.**"
> → **"왜 Martech 스택은 항상 여러 제품의 조합인가"에 대한 실무자 설명. 연동 지옥의 구조적 원인이다.**

**4위. 푸시/메시지 opt-out과 "거래성 vs 광고성" 분리 실패** — HN 5개 스레드 / 6명. **개발자가 직접 설계로 해결해야 하는 문제**라 이 책에 특히 중요하다.

> "The thing I have a problem with in this method is **you're blanket opting in or out of notifications. I'd much rather have notifications bucketed into two systems. Transactional and marketing, just like email. I should be able to opt out of Amazon's marketing push notifications without ALSO opting out of getting delivery alerts.**"
> — HN 38842663 / joshmanders / 2024-01-02

> 🥈 **챕터 오프닝 후보 2순위.** 개발자 독자가 "아 이건 내가 만드는 쪽 얘기구나" 하고 즉시 감정 이입할 수 있는 요구사항이고, 실제로 이게 **동의 모델 설계의 핵심**이다.

세그먼트 suppression 실패의 구체적 사례 — HN 38840135 / winkelwagen / 2024-01-02:
> "I recently unsubscribed to a services that kept spamming me their "lifetime subscription" product, while **I already was on their yearly premium plan.** Over the course of 2 weeks, I received **4 push notifications, 4 emails and 2 times when I opened the app it had a full screen ad.** I'll never use this product again. Ironically, this app focuses on sleep quality, focus and meditation."

> 📌 **"이미 연간 프리미엄 결제한 사람에게 평생 구독권을 광고했다"** — 기존 구매자를 **제외(suppression)**하지 못한 전형적 실패. 2주간 푸시 4 + 이메일 4 + 전면광고 2라는 구체 숫자까지 있어 오프닝으로 좋다.

> `관찰 사실`: **2012년(dirtae) → 2026년(PurestGuava)까지 14년간 동일한 불만이 반복된다.** "채널 피로도는 해결된 적 없는 문제"라는 서술의 근거.
>
> ✅ **그리고 이 축에는 학술 근거가 붙는다 (§3-J):** **Godfrey, Seiders & Voss (2011)**의 **빈도 역U자** — 커뮤니케이션 빈도에 최적점이 있고 넘으면 성과가 꺾인다. **커뮤니티 증언 + 학술 근거가 같은 방향을 가리키는 드문 축이다.** 챕터에서 이 둘을 겹치면 강하다.

**5위. 이메일 딜리버러빌리티는 별도의 전문 영역** — HN 5개 스레드 / 5명
> "**Email, deliverability in particular, is a rabbit hole.** Its easy enough to get it set up and "basically" working, but not. ... **Beyond that, once you hit enough volume, there's best practices should have always been doing but you learn from experience and need to abide by or else you're not getting anything through**"
> — HN 9115955 / sbov / 2015-02-26

> 📌 `관찰 사실`: **Braze·Klaviyo·Hightouch 세 회사 모두 Deliverability 전담 직무를 별도로 채용 중**(§7-1)이라는 사실과 위 증언들이 서로를 보강한다. **"왜 딜리버러빌리티 전담자가 따로 있는가"에 대한 답이 된다.**

**6위. CDP는 무엇을 하는 회사인지 설명하기 어렵다** — HN 3개 스레드 / 4명
> "**So nobody feels comfortable talking about what they do.**" — HN 24737006 / m463 / 2020-10-10
>
> "CDP (Customer Data Platform) is a more widely known space but it's too broad. **CDI (Customer Data Infrastructure) is more relevant but very few people know about it**" — HN 27553257 / soumyadeb (RudderStack) / 2021-06-18

> 🎯 **책에 반드시 다뤄야 할 정서:** 개발자 커뮤니티에는 Martech에 대한 **윤리적 불편감**이 깔려 있다. **"내가 만드는 게 감시 도구 아닌가"**라는 질문. **이 책이 이걸 피하면 독자에게 정직하지 않다. 최소 한 챕터 또는 한 절이 필요하다.**

**8위. 격리 실패** — RudderStack GitHub 이슈 **#4953 "Rudderstack becomes extremely slow when you have one destination down"** (2024-07-31 생성, **조회 시점 여전히 open**, 댓글 16). 이벤트 라우팅 시스템의 **격리(isolation) 실패**라는 전형적 아키텍처 문제.
⚠️ **이슈 본문·댓글 원문은 미조회** (GitHub rate limit). **제목·상태·날짜·댓글 수만 확인.** 인용문으로 쓰려면 재조회 필요.

### 7-5. 한국 특유의 채널 — 카카오 알림톡

> ⚠️ **카카오 공식 개발 문서는 3개 URL 전부 조회 실패했다.** 아래는 **벤더가 정리한 2차 자료**다. [blog.notifly.tech/alimtalk-screening-guide/ | **2025-08-26**] `이해관계 있음`

**구조적 사실 (원문 인용):**
> "알림톡은 고객의 휴대폰 번호만 있으면 카카오톡 채널 추가 여부와 관계없이 발송이 가능하며, 문자 메시지(SMS, LMS)보다 비용이 합리적인 장점이 있습니다. **하지만 광고성 문구는 허용되지 않으며, 사전에 카카오톡 심사를 통과해야지만 발송할 수 있습니다.**"

> 🎯 **이게 한국 Martech의 가장 큰 구조적 차이다.** 서구권 CRM(Braze·Klaviyo)은 이메일/푸시/SMS를 "동의만 있으면 원하는 내용을 보낼 수 있는" 채널로 다룬다. **한국의 알림톡은 템플릿 단위로 플랫폼 사전 심사를 받아야 한다. 즉 메시지 내용이 배포 파이프라인의 심사 대상이 된다.** 개발자 입장에서는 **"템플릿 등록 → 심사 요청 → 상태 조회"라는 비동기 승인 워크플로우를 시스템에 넣어야 한다**는 뜻이다.

**블랙리스트 (발송 불가 유형) — 원문:**
> "1) 특가 상품 알림 안내(친구톡 권장)
> 2) **장바구니 등록 상품 안내(친구톡 권장)**
> 3) 포인트 지급에 명시적으로 동의하지 않은 수신자에게 발송하는 포인트 적립/소멸 메시지
> 4) 쿠폰 발급 후 빠른 시일 내 소멸하는 쿠폰의 메시지
> 5) **변수만으로 구성된 메시지 불가 ex) #{상품명} #{송장정보}**"

> 🎯 **"장바구니 등록 상품 안내는 알림톡 불가, 친구톡 권장"** — 서구권 CRM에서 가장 기본적인 자동화인 **장바구니 이탈(cart abandonment) 캠페인이 한국에서는 채널을 바꿔야 한다.** 이건 개발자가 캠페인 엔진을 설계할 때 **채널 라우팅 규칙**으로 구현해야 하는 도메인 지식이다.
>
> 🎯 **"변수만으로 구성된 메시지 불가"** — 템플릿 엔진 설계에 직접 영향을 주는 제약. **모르면 심사에서 반려당한다.**
>
> 🎯 **"템플릿이 승인된 이후에도 모니터링을 통해 가이드 위반이 확인될 경우 해당 템플릿에 대해 차단 조치가 취해질 수 있습니다."** → **승인 후에도 사후 차단이 가능하다. 프로덕션에서 갑자기 특정 템플릿이 죽을 수 있다 — 장애 대응 시나리오에 넣어야 한다.**

쿠폰·포인트 알림톡 필수 기재 요건(업체명 / 포인트 금액 / 유효기간 / 발송 근거)은 **템플릿 변수 스키마 설계로 직결된다.**

⚠️ 심사 리드타임("4-5일") 수치는 **`확인 불가`** — 검색 스니펫에서만 봤다.

### 7-6. 한국 Martech 시장 지형

> ⚠️ **이 절은 이 리서치에서 가장 약한 부분이다.** 회사 규모·투자·고객사 수치의 1차 소스를 거의 조회하지 못했다. 아래는 대부분 **채용 공고·자사 블로그에서 회사가 스스로 말한 내용**이다.

| 회사 | 확인한 것 | 확인 못한 것 |
|---|---|---|
| **AB180** | 원티드 active 24건. 자사 제품 **Airbridge** = 어트리뷰션. **Braze·Amplitude를 국내에 함께 공급**(CSM 공고 타이틀 + JD 본문 2건에서 교차 확인) | 투자·매출·고객사 수 1차 미확인. "국내 1위 MMP" 등은 **검색 요약의 벤더 마케팅 문구** → `확인 불가` |
| **채널톡** | 원티드 active 40건. FDE·Applied AI Engineer·AX Consultant 채용 중 | **DAU 수치 상충**(800만 vs 3M) → `확인 불가` |
| **빅인사이트** | active 1건(Data Platform Engineer). 자사 소개 "Bigin Ads와 Bigin CRM" `(2차 인용)` | 규모·투자·고객사 전부 미조회 |
| **마티니아이오** | active 12건(솔루션 컨설턴트 1, CRM 마케터 3, CSM, BA, 세일즈). 자사 블로그 운영 | 규모·투자 미조회 |
| **노티플라이** | 자사 블로그 운영, 카카오 알림톡 실무 가이드(2025-08-26) | 회사 규모·제품 상세 미조회 |
| **인사이더 한국** | 원티드 기업 ID 813 존재만 확인 | **공고·JD 미조회** |
| **그루비 / 다이티** | 그루비: 원티드에 `그루비엑스` 검색됨(**동일 회사 확인 불가**) / 다이티: 원티드 검색 **0건** | 전부 `조회 불가` |

> 🎯 **AB180이 Airbridge(자사 제품)와 Braze·Amplitude(해외 제품 국내 공급)를 동시에 다룬다**는 구조는 JD 두 건으로 교차 확인됐다. **한국 Martech 시장의 중요한 특징 — 국내 벤더가 동시에 해외 솔루션의 리셀러/파트너**이고, 그래서 CSM·Solution Architect 직무가 "여러 제품의 연동"을 다룬다.

> `관찰 사실`: **한국어 Martech 콘텐츠 생태계는 개발자 커뮤니티가 아니라 벤더 블로그가 주도한다.** 한국어 검색 상위에 뜬 것은 전부 martinee.io / notifly.tech / bizgo.io / solapi.com 같은 **솔루션 벤더의 콘텐츠 마케팅**이었다. ⚠️ 단, 이건 **검색 결과 상위 노출 기준의 인상**이며 체계적 조사가 아니다.

### 7-7. 개발자가 준비해야 할 것 — 근거 강도 순위

**근거 강도:** ⭐⭐⭐ = 채용 공고 다수 + 커뮤니티 교차 / ⭐⭐ = 한쪽 / ⭐ = 단일 소스

| 순위 | 역량 | 강도 |
|-----|------|-----|
| 1 | **대용량 이벤트 스트림 처리** (Kafka/Queue, 실시간+배치) | ⭐⭐⭐ |
| 2 | **클라우드 + Kubernetes 운영** | ⭐⭐⭐ |
| 3 | **비용을 숫자로 판단하는 감각 (FinOps)** | ⭐⭐⭐ |
| 4 | **개발자·비개발자 양쪽과 소통** | ⭐⭐⭐ |
| 5 | **데이터 흐름을 End-to-End로 설명하는 능력** | ⭐⭐⭐ |
| 6 | 멱등성·backfill·retry·중복 처리 | ⭐⭐ |
| 7 | SQL + 데이터 웨어하우스 | ⭐⭐ |
| 8 | 모니터링·옵저버빌리티 | ⭐⭐ |
| 9 | SDK 통합 경험 (iOS/Android/Web) | ⭐⭐ |
| 10 | **비즈니스 영어** (AB180 SA·CSM 둘 다 **필수**, 우대 아님) | ⭐⭐ |
| 11 | Go 또는 Kotlin | ⭐⭐ |
| 12 | 실패 내성·회복 탄력성 | ⭐⭐ |

> 🎯 **주목: 3위(비용)와 4위(소통)가 순수 코딩 역량보다 위에 온다.** 표본이 작아서가 아니라 **여러 공고가 반복해서 명시**하기 때문이다.
> **대상 독자에게 전할 메시지: 부족한 건 코딩이 아니라 도메인과 비용 감각이다.**

**개발자가 반드시 알아야 할 도메인 용어** (공고/문서에 실제 등장한 것만): `Attribution` · `MMP(Mobile Measurement Partner)` · `CDP` · `CDI` · `이벤트 택소노미(Category/Event/Property 3층)` · `PA(Product Analytics)` · `Identity Graph / Identity Resolution` · `Reverse ETL` · `Deliverability` · `Segment` · `알림톡/친구톡`
직무 용어: `Solutions Engineer(SE)` · `TAM` · `Forward Deployed Engineer(FDE)` · `Analytics Engineer(AE)` · `Growth Engineer` · `Pre-Sales` · `GTM`

> ⚠️ **면접 질문·과제 유형은 수집 실패했다.** 잡플래닛·블라인드·면접 후기를 조회하지 못했다. **"이런 질문이 나온다"고 쓸 근거가 이 리서치에는 없다. "공고가 요구한다"로만 써라.**

---

## 8. 논쟁점 — 관점 A / 관점 B 병기

> **이 섹션은 통합하지 않았다.** 상충하는 자료는 나란히 제시하고, 어느 쪽이 옳은지 결론 내지 않았다. 챕터에서 한쪽으로 정리하려면 저술 시 판단 근거를 명시해야 한다.

### 논쟁 1. 패키지형 CDP vs 컴포저블/웨어하우스 네이티브 CDP

**관점 A — 웨어하우스가 진실의 원천이어야 한다** (비(非)벤더 실무자 발언, HN 29188544 스레드 2021-11):

> "**once you get into complex workflows that merge data across your product and CRMs it all moves to the warehouse first.** Typical flow is a Fivetran or Stitch into the warehouse, lots of dbt models... **Once in the warehouse, it needs to get back into those operational systems again, which is the tricky part. I've done these one off integrations from the warehouse into Salesforce**... **Being able to feed tools directly off the warehouse instead of writing one off integrations is t[he value]**"
> — HN 29190721 / pinkbeanz `커뮤니티 주장 (검증 필요)`

> "**The Salesforce data is in Salesforce, and the HubSpot data is in HubSpot, and the Mixpanel data is in Mixpanel, but those applications don't have each others data**"
> — HN 29190740 / gurubavan

> 📌 **관점 A의 가장 좋은 근거**: 벤더가 아니라 **"일회성 연동을 직접 짜본 사람"**이 왜 웨어하우스 우선인지 설명한다. **이 책 독자가 정확히 겪게 될 일이다.**

**관점 B-1 — 추상화가 새어나온다** (실무자 비판):

> "Implicit mapping between SQL to target is great, but **how does the SQL author know what SQL to write in the first place? I've done no shortage of integrations like this, and there is no avoiding reading the target SaaS documentation to know what their schema looks like so I can shape data accordingly. Without that step, I can't even start writing SQL.**"
> — HN 29191935 / tomnipotent

> 🎯 **"결국 목적지 API 문서를 읽어야 한다"** — 컴포저블 CDP가 약속하는 "SQL만 알면 된다"의 한계를 실무자가 지적한 대목. **이 책 독자에게 매우 실용적인 경고다.**
> 📌 **벤더(tejasmanohar)의 답변이 "declarative이고 docs·autocomplete·schema discovery로 돕는다, still early days there"였다 — 즉 완전히 해결되지 않았음을 인정했다.**

**관점 B-2 — reverse ETL/컴포저블은 제품으로서 취약하다:** §7-4의 throwaway7783(2025-05-01), r1290("You just need dagster or temporal - and a few lines of python", 2025-05-02), knes("**The whole Modern Data Stack has either died, acquired or merged by now.**", 2025-10-13).

**참고 — 경쟁사 창업자들끼리의 공개 대화** (양쪽 다 벤더지만, **이 시장의 축을 당사자들이 정의한 대목**):
> **soumyadeb (RudderStack 창업자, 2021-11-12):** "Our positioning, go-to-market, pricing, use cases etc are centered around **building the end to end customer data infrastructure.**"
> **tejasmanohar (Hightouch 창업자, 2021-11-12):** "**Agree RE: focus. Rudderstack is a bundle and there is a place for that.** Hightouch is 100% focused on activating data from the warehouse"

> 🎯 **"번들이냐 단일 기능이냐"가 이 시장의 실제 축이다.** 그리고 2021년의 이 대화와 2025년 throwaway7783의 진단을 나란히 놓으면 **4년에 걸친 시장 서사**가 만들어진다.

> 🚨 **이 리서치의 정직한 결론 — 저술 시 반드시 반영할 것:**
> - **양쪽 다 비(非)벤더 실무자 발언을 확보했다.** 다만 **모두 같은 하나의 스레드(2021-11)**에서 나왔고 **2021년 시점**이다. 🕒
> - `관찰 사실`: **"패키지형 vs 컴포저블"이라는 프레이밍 자체로 HN에서 큰 논쟁이 붙은 적은 이 조사 범위에서 발견되지 않았다.** 컴포저블을 주장하는 글은 거의 전부 벤더가 올렸고 **HN에서 1~2점으로 묻혔다.**
> - **책에서 "업계가 둘로 갈렸다"는 식으로 쓰면 벤더 마케팅을 그대로 옮기는 것이 된다.** 대신 **"실무자는 진영이 아니라 구체적 마찰(목적지 API 문서, 지연, 상태 추적)로 말한다"**는 각도가 이 자료에 충실하다.

### 논쟁 2. 어트리뷰션은 유용한가, 자기기만인가

**A — 불완전해도 쓸모 있다:**
> "complaining that GA doesn't know that a person saw a Facebook ad at some point before ultimately subscribing... is a bit like complaining that your car isn't also a boat and plane. **If you want comprehensive analytics, you need to spend time developing a comprehensive measurement plan.**" — HN 9257502 / ssharp / 2015-03-24
>
> "It's well known that the self reported performance numbers from Google Ads and Facebook Ads are inflated, **however those ad channels still do drive real value.**" — HN 28855010 / fourseventy / 2021-10-13

**B — 근본적으로 가정에 기댄 숫자다:**
> "**The answer is you really don't[;] do you come up with some kind of formula based [on] a few assumptions.** Ultimately I am highly skeptical. **Ad tech is almost always a repackaging of the same product with a new name.**" — HN 48180365 / etempleton / **2026-05-18** (가장 최신)

> 🎯 **이 논쟁의 학술적 판정은 §3-H·§3-I에 있다 — 커뮤니티 발언만으로 결론 내지 마라.**
> **Berman (2018):** 라스트터치는 **안 쓰느니만 못하다**(광고주 이익 감소). → B에 힘을 싣는다.
> **Gordon et al. (2023):** 관측 기반 방법이 실제 리프트를 **5~13배 과대추정**했다. → B에 힘을 싣는다.
> **Blake et al. (2015):** 그러나 **비브랜드 키워드에서 신규·저빈도 고객에게는 실제 효과가 있었다.** → A를 완전히 기각할 수 없다.
>
> **종합 서술 권고:** "어트리뷰션 숫자는 **계기판이 아니라 방향 지시등**이다. 그리고 그 방향조차 실험으로 교정하지 않으면 몇 배씩 틀린다." — 이 결론은 위 세 논문으로 근거화된다.

### 논쟁 3. 딜리버러빌리티/메시징 인프라는 사야 하나 만들어야 하나

**A — 사라:** "Do you want to become an expert in email deliverability, DNS, bounces, white listing, DKIM, SPF? Or do you want to sell your product?"(HN 5648393 / 13rules / 2013-05-03) / "**Don't run your own mailer as a startup.**"(HN 8532692 / shizcakes / 2014-10-30)

**B — 볼륨이 커지면 자체 운영이 경제적이다:** "you don't pay per-message fees, so for higher volume it's really economical compared to a service like SendGrid."(HN 9471320 / davideous / 2015-05-01 — **MTA 제품 벤더의 발언**, `이해관계 있음`)

> 🎯 **이 책에 중요한 재구성:** **이 논쟁은 독자가 어느 쪽 회사에 가느냐로 답이 갈린다.** 인하우스라면 A. **Martech 벤더라면 이게 곧 제품이므로 "그게 우리 일"이다.** Braze가 `Team Lead, Email Deliverability`를 4개 도시에서 뽑고 있다는 사실(§7-1)이 이를 뒷받침한다. **벤더/인하우스에 따라 정반대의 조언이 된다는 점이 이 책에서 짚을 지점.**

### 논쟁 4. Martech를 만드는 일은 윤리적으로 편한가

**A — 정상적인 비즈니스 인프라다:** "**Shopping Cart abandonment email campaigns are pretty benign.**"(HN 45106650 / jacobr1 / 2025-09-02) / "there are numerous services that provide analytics and have no part in tracking you elsewhere... **To my knowledge, no**"(HN 11267213 / robbiemitchell / 2016-03-11)

**B — 설명하기 불편하다는 것 자체가 신호다:** "**So nobody feels comfortable talking about what they do.**"(m463) / "However well done this may be, **it is more comfortable not to be too aware about it.**"(salicideblock)

**같은 사람이 A와 B를 동시에 말한다** — HN 45106650 / jacobr1:
> "**But the outrage around the targeted ad for baby/pregnancy products that made the news from Target a few years ago is just the start** for what more insightful data signals can give you. I don't really care about most retailers knowing what I buy. **I do care about them reselling that data to big aggregators that know everything I buy, where I go and when**"

> 🎯 **이 마지막 인용이 이 논쟁의 가장 정직한 형태다** — 경계는 "데이터를 모으느냐"가 아니라 **"모은 데이터가 어디까지 흘러가느냐"**에 있다.

### 논쟁 5. 마케팅 알림은 채널 자체를 망치는가

**A — 남용이 채널을 죽인다:** "**Rampant abuse of push notifications in this way is ruining the push notification mechanism for developers that use them appropriately**"(HN 4210820 / dirtae / **2012-07-07**) / "**The entire purpose of getting you to install a mobile phone app is to push marketing notifications at you**"(HN 37735717 / tsukikage / 2023-10-02)

**B — 도구 문제가 아니라 분리·통제 설계 문제다:** joshmanders의 거래성/마케팅성 버킷 분리 요구(§7-4)

⚠️ 마케터 자기 진술(HN 24630925 / NicolasGorden, 2020-09-29)의 **"75~80% 오픈율"은 검증되지 않은 개인 주장이며 업계 평균과 크게 다르다. 수치는 인용하지 마라.**

### 논쟁 6. CDP 정의가 두 갈래다 — 해소하지 말고 서술하라

- **Raab 계열 정의:** "a marketer-controlled system that builds a multi-source customer database and **exposes it to external execution systems**" — 개방성이 정의적 특징
- **CDPI에 귀속된 유명 문장:** "packaged software..." 계열 — **영속 DB 구축**이 핵심 `(2차 인용, Informatica 경유)`

⚠️ 후자는 **1차 확보 실패**다. 둘을 섞어 쓰지 마라. `[web-gaps]`

### 논쟁 7. DMP는 데이터를 통합하는가

- **애널리스트/Raab 2017 벤 다이어그램:** DMP는 데이터를 **남에게 열어주지 않는다** ❌
- **벤더(Adobe Audience Manager) 자기 규정:** 오디언스를 여러 소스에서 통합·활성화한다

⚠️ **벤더 자기규정과 애널리스트 분류가 충돌한다. 병기하라.** `[web-gaps]`

---

## 9. 리서치 공백 — 확인 불가 목록

> **이 목록은 실패의 기록이자 후속 리서치 지시서다. 책에서 이 항목들을 아는 척하면 안 된다.**
> **저술 중 아래 항목이 필요해지면 반드시 새로 조회하라. 기억으로 채우면 거의 틀린다.**

### 9-1. 🔴 최우선 미결 (책의 뼈대에 영향)

| 항목 | 상태 | 영향 |
|---|---|---|
| **§3 학술 근거** | ✅ **완료.** 마케팅 원리 D-1~D-15 + 기반 기술 C-16~C-22 전부 확보 (`papers.md` 1,054줄) | 남은 공백은 §3-L의 4건뿐 |
| **LLM 생성 카피의 효과 크기** | ❌ **미확보 (명시적 실패 판정)** | **"LLM 카피가 성과를 X% 올린다"는 수치 주장 금지** |
| **정보통신망법 제50조 제3항 단서의 "대통령령으로 정하는 매체"** | 시행령 원문 미확인 | **앱 푸시가 야간 제한 대상인지 판정 불가.** 2차 자료는 전자우편이라 하나 미검증 |
| **CDP Institute 기관 공식 정의문** | cdpinstitute.org 전역 403 (PDF 포함, 우회 없음) | Raab 개인 정의로 대체 가능하나 **둘을 섞어 쓰면 안 됨** |
| **CEM/CXM 카테고리 정의** | Gartner 403 | **비교표에서 제외 권장** |
| **"DMP=서드파티 쿠키, CDP=퍼스트파티" 통설** | **어떤 1차 소스로도 미확인** | **검증 없이 쓰면 안 됨** |
| **CDP 4분류(Data/Analytics/Campaign/Delivery)** | ❌ **확인 불가 — 이 분류를 쓰지 마라** | Raab 원문은 **3분류(Data/Analytics/Personalization)** |

### 9-2. 기술 스택

- **Tier 2 전 항목의 버전·수치** — Redpanda, Pulsar, Jitsu, OpenTelemetry, Spark Structured Streaming, Kafka Streams, Materialize, Arroyo, StarRocks, Delta Lake, Hudi, Parquet, Snowflake·BigQuery·Redshift, Airflow, Dagster, Airbyte, Cassandra/ScyllaDB, Aerospike, RocksDB, pgvector/Qdrant/Milvus. **의도적 미조회 — 챕터에 버전·수치로 옮기면 안 된다.**
- **RudderStack·Redis 라이선스** — 조회 실패. **"오픈소스"로 단정 서술 금지**
- **ClickBench 방법론·구체 수치** — 미조회. **인용 금지**
- **Druid 아키텍처 문서** — 미조회 (버전만 확정). 성격 규정은 통념 수준
- **이탈 예측 / send-time optimization / LLM 카피 생성 / text-to-SQL** — **어느 제품이 실제로 무엇을 쓰는지 공개 1차 문서 미확보.** 특정 벤더가 이 기능을 제공한다는 서술은 이 리서치를 근거로 쓸 수 없다
- **Lambda/Kappa 원전** (Nathan Marz / Jay Kreps) — 미조회
- **Iglu / Confluent Schema Registry 스펙 세부** — 미조회
- **dbt 머티리얼라이제이션·`ref()`·테스트 상세** — 미조회
- **Pinot 인덱스 종류·업서트 상세** — 미조회
- **Netflix 실시간 분산 그래프 / 카카오·당근 CDP 아키텍처 / Uber RAMEN** — 본문 미조회

### 9-3. 제품·벤더

- **Insider:** 설립연도·본사·누적투자액·기업가치·한국 오피스 (전부 1차 미확인) / **내부 아키텍처는 공개 자료 없음 — 추정 금지** / Architect 상세(404), Eureka 정체, RFM Segments 본문
- **Iterable**(403), **Salesforce Marketing Cloud**(미조회), **Branch**(미조회)
- **Salesforce Data Cloud** → ✅ 확보. **다만 제품명이 "Data 360"으로 표기 중** (404의 원인)
- **한국 벤더 3곳(그루비·빅인·다이티) 공개 개발자 문서 없음** — 계약·어드민 뒤. 다이티는 사이트 자체가 **TLS 인증서 불일치**로 조회 불가
- **mParticle 합병 발표일** — 1차 미확인(금액 $300M만 확인)
- **Census 브랜드·제품의 완전 소멸 여부** — 리다이렉트만으로 단정 불가

### 9-4. 프라이버시·규제

- **Chrome M150의 실제 stable 릴리스 날짜** (chromiumdash JS 렌더링 실패)
- **Firefox Total Cookie Protection 기본값 버전 번호**
- **SKAdNetwork deprecation 여부·버전·conversion value 스펙** / AdAttributionKit 상호운용 문언 — **챕터에 쓰지 마라**
- **PIPA 조문 원문 미확인:** 제16조제3항·제17조·제22조·제22조제5항·제28조의2~제28조의9·제35조·제35조의2·제36조·제37조·제64조의2 / **제37조의2의 시행일**
- 🚨 **PIPA 과징금 상한 3% vs 10% — 상충 상태로 병기됨. 둘 다 law.go.kr 원문 미확인.** 챕터에 수치를 쓰지 말거나 `(사실 확인 필요)`를 붙여라. **과징금(제64조의2)과 과태료(제75조)는 다른 제재다 — 섞어 쓰지 마라.**
- **정보통신망법 2026-07-07 개정의 과징금 6% 수치·전송 위탁 조문** — 원문 미확인
- **CCPA "sale" 법문 정의 및 Civil Code 조문 번호**
- **EU AI Act Article 5·Article 50 원문** / AI Omnibus 최종 규정 텍스트
- **PIPC 안내서 본문** (제목·발행 시점만 확보). ⚠️ **"온라인 맞춤형 광고"·"행태정보" 제목의 독립 안내서는 2026-07-25 기준 PIPC 목록에서 확인되지 않았다. 존재를 단정하지 마라.**
- **어느 벤더도 PSI·k-anonymity를 그 이름으로 명시하지 않았다** (negative finding)
- **UID2 파생 절차(해싱·솔팅)·토큰 회전 주기 / RampID 현재 상태 / 이메일 SHA-256이 업계 표준인지의 1차 근거**
- **LiveRamp/Adobe/Salesforce의 deterministic·probabilistic 정의 원문** — 검색 요약만 확보, **따옴표 인용 금지**

### 9-5. 커뮤니티·커리어

- 🔴 **면접 질문·과제 유형 전체 공백** — 잡플래닛·블라인드 미조회. **"면접에서 나온다"고 쓸 근거 없음**
- **Reddit 전면 차단** — r/dataengineering 등. **표본이 HN으로 심하게 기울어진 주원인**
- **GeekNews·OKKY·velog·커리어리** — JS 렌더링/검색 실패. **한국 개발자 커뮤니티 목소리 사실상 미확보**
- **카카오 비즈메시지 공식 개발 문서 3개 URL 전부 실패** — 알림톡 내용은 전부 벤더 2차 자료
- **인하우스 직무 표본 전무** — 당근·토스·무신사·컬리·배민의 그로스/마케팅 플랫폼 JD 미조회
- **GitHub 이슈 본문·댓글** — rate limit 소진. 제목·날짜·댓글수만
- **미확보 주제:** MTU·볼륨 과금 불만(0건), CDP 도입 후회담(0건), **AI/LLM 기능 현장 후기(0건 — 공고에는 AI 직무가 폭증 중인데 후기가 없다는 비대칭 자체는 기록할 가치가 있다)**

### 9-6. 수치 충돌 — 책에 쓰기 전 재확인 필수

| 항목 | 문제 |
|---|---|
| **채널톡 DAU** | "하루 800만명" vs "3 million daily" — **둘 다 1차 미확인** |
| **AB180 트래픽** | 블로그 **제목 "하루 100억 트래픽" vs 본문 "하루 10억건"** 불일치 + **게시일 미상** |
| **Martech 총량** | ✅ **15,505(2026년판)만 사용.** 15,384는 미검증 |
| **PIPA 과징금** | 3% vs 10% 상충 |
| **Insider iOS SDK 버전** | 모듈 v15.1.1 vs 리포 태그 v1.9.1 — 다른 체계 |
| **Iceberg/Pinot 릴리스 일자** | GitHub vs Apache 아카이브 하루~수주 차이 |
| **Salesforce 제품명** | Data Cloud / Data 360 혼재 |

### 9-7. 후속 리서처를 위한 접근 가능 도메인 지도

이 리서치가 실증한 우회 경로다. **다음 라운드에서 시간을 아낄 수 있다.**

| 막힌 곳 | 뚫린 경로 |
|---|---|
| `segment.com` 403 | ✅ `raw.githubusercontent.com/segmentio/segment-docs/develop/src/...` |
| `salesforce.com` 403 | ✅ `trailhead.salesforce.com` (MA 갭을 이걸로 뚫음) |
| `architect.salesforce.com` 403 | ✅ `developer.salesforce.com/docs/...` |
| `iceberg.apache.org` 내비게이션만 | ✅ `raw.githubusercontent.com/apache/iceberg/main/format/spec.md` |
| GitHub Releases **연도 미표기** | ✅ `archive.apache.org/dist/{project}/` (전체 타임스탬프) |
| `law.go.kr` 프레임 SPA | ✅ `lsLawLinkInfo.do?...&print=print` 와 `lsLinkCommonInfo.do?lsJoLnkSeq=` 패턴만 본문 반환 |
| Apple 개발자 문서 SPA | ✅ `developer.apple.com/tutorials/data/documentation/{path}.json` |
| `docs.pinot.apache.org` 404 | ✅ 404 페이지가 안내하는 `.md` 경로 |
| `cdpinstitute.org` | ❌ **PDF 포함 전역 차단, 우회 없음** (확정적 부정 결과) |
| Reddit / chromestatus / chromiumdash / web.archive.org | ❌ 차단 또는 JS 렌더링 |

---

## 10. 참고문헌

> 전체 URL 목록은 각 원본 파일의 "참고문헌" 절에 있다. 여기서는 **저술 시 가장 자주 인용할 핵심 소스**만 정리한다.

### 카테고리·정의 (1차)
1. Raab, David. "I've Discovered a New Class of System: the Customer Data Platform." *Customer Experience Matrix*, 2013-04-25. http://customerexperiencematrix.blogspot.com/2013/04/ive-discovered-new-class-of-system.html
2. Raab, David. "Customer Data Platforms Revisited: The Future of Marketing Data." 2015-01-18. http://customerexperiencematrix.blogspot.com/2015/01/customer-data-platforms-revisited.html
3. Raab, David. "Why Are There So Many Types of Customer Data Platforms? It's Complicated." 2018-11-03. http://customerexperiencematrix.blogspot.com/2018/11/why-are-there-so-many-types-of-customer.html
4. Brinker, Scott. "2026 Marketing Technology Landscape Supergraphic." *chiefmartec*, 2026-05-05. (15,505개)
5. Adobe. "Adobe Real-Time Customer Data Platform." 문서 표기 2026-06-18. https://experienceleague.adobe.com/en/docs/experience-platform/rtcdp/home
6. Adobe. "XDM System Overview." 문서 표기 2026-05-23. https://experienceleague.adobe.com/en/docs/experience-platform/xdm/home
7. Kline, Luke. "What is a Composable CDP?" *Hightouch*, 2023-06-20. https://hightouch.com/blog/composable-cdp
8. Fivetran. "Fivetran Signs Agreement to Acquire Census." 보도자료, 2025-05-01.

### 개발자 표면 스펙 (1차)
9. Segment. Spec — index / identify / track / page / screen / group / alias / common / ecommerce v2. https://raw.githubusercontent.com/segmentio/segment-docs/develop/src/connections/spec/
10. Segment. "Collecting Data on the Client or Server." (develop 브랜치)
11. Insider One. Web SDK Integration Guide (2026-07-23) / UCD (2026-04-22) / Upsert User Data API (2026-07-24) / API Rate Limits (**2026-07-12**). https://academy.insiderone.com/
12. Klaviyo. API Overview. **API 버전 v2026-07-15**. https://developers.klaviyo.com/en/reference/api_overview

### 기술 스택 (1차 — 버전 확정)
13. Apache Kafka Archive (**4.3.1 / 2026-06-23**) / KIP-98 Exactly Once / Confluent Consumer Design
14. Apache Flink Downloads (**2.3.0 / 2026-06-25**) / Timely Stream Processing
15. Apache Iceberg — Table Spec + Archive (**1.11.0 / 2026-05-19**)
16. Apache Pinot Archive (**1.5.1 / 2026-06-30**) / Architecture
17. Trino Release Notes (**483 / 2026-07-17**) / Use Cases
18. DuckDB News (**1.5.5 / 2026-07-22**) / Why DuckDB
19. dbt-core Releases (**1.12.0 / 2026-07-16**) / About dbt models
20. ClickHouse — MergeTree / uniqCombined / uniqExact (**26.x 계열 / 2026**)
21. Redis — HyperLogLog / Bloom filter / Count-Min Sketch / t-digest
22. Feast — Architecture Overview / Point-in-time joins (**0.65.0 / 2026**)
23. Snowplow — Fundamentals / **Limited Use License FAQ (SLULA v1.1 / 2024-12)**

### 아키텍처 사례 (1차, 발행일 확인)
24. Pinterest Engineering. "Making user sequence data more cost-efficient, faster, and easier to use." **2026-05-21**
25. 토스. "광고 ML" (**2025-04-21**, 김영호) / "Feature Store & Trainkit" (**2025-08-14**, 우종호·송석현) / "TUES" (**2026-06-16**, 우찬희)
26. 우아한형제들. "카프카 활용" (**2024-05-30**, 김나은)
27. LINE. "Kafka Streams 적용" (**2016-08-18**, Kawamura Yuto) ⚠️ 구버전
28. 쿠팡. "Big data platform evolving..." (**2022-08-03**) ⚠️ 구버전

### 프라이버시·규제 (1차)
29. Chavez, Anthony. "Next steps for Privacy Sandbox..." Google, **2025-04-22** / "Update on Plans for Privacy Sandbox Technologies," **2025-10-17**
30. Chrome 144 release notes (stable **2026-01-13**) / blink-dev "Intent to Deprecate and Remove: Topics API" (2025-11-08, 갱신 **2026-06-12**)
31. Wilander, John. WebKit — ITP (2017-06-05) / Full Third-Party Cookie Blocking (**2020-03-24**) / CNAME Cloaking Defense (**2020-11-12**)
32. Mozilla. Total Cookie Protection (**2022-06-14**, 업데이트 2024-08-28)
33. Apple. User Privacy and Data Use / AppTrackingTransparency
34. Google. Server-side tagging / Consent mode overview / **Ads Data Hub Privacy checks (20/50/10)**
35. Meta. Conversions API / **Deduplicate Pixel and Server Events (48시간)**
36. IAB Europe. "Transition to TCF v2.3," **2025-06-19**
37. W3C. "Global Privacy Control," Working Draft, **2026-06-11**
38. AWS. "What is AWS Clean Rooms?" / Snowflake Data Clean Rooms / Amazon Marketing Cloud
39. 법제처 국가법령정보센터. 「개인정보 보호법」 **(시행 2025-10-02, 법률 제20897호)** — 제15·16·24·30·37조의2·75조, 시행령 제17·31조
40. 법제처 국가법령정보센터. 「정보통신망 이용촉진 및 정보보호 등에 관한 법률」 제50조 **(시행 2026-07-07, 법률 제21305호)**
41. 개인정보보호위원회. 안내서 목록 (최신 항목 **2026-06-25** 전송요구권 안내서)
42. EUR-Lex. Regulation (EU) 2016/679 (GDPR) / California AG, CCPA / EC AI Act Service Desk 타임라인

### 학술 (전부 2026-07-25 Crossref/arXiv/Semantic Scholar 조회 — 확인 수준은 신선도 원장 E절 참조)
43a. Schmittlein, D. C., Morrison, D. G., & Colombo, R. (1987). "Counting Your Customers: Who-Are They and What Will They Do Next?" *Management Science*, 33(1), 1–24. DOI: 10.1287/mnsc.33.1.1
43b. Fader, P. S., Hardie, B. G. S., & Lee, K. L. (2005). "'Counting Your Customers' the Easy Way: An Alternative to the Pareto/NBD Model." *Marketing Science*, 24(2), 275–284. DOI: 10.1287/mksc.1040.0098
43c. Gupta, S., et al. (2006). "Modeling Customer Lifetime Value." *Journal of Service Research*, 9(2), 139–155. DOI: 10.1177/1094670506293810
43d. Goldfarb, A., & Tucker, C. (2011). "Online Display Advertising: Targeting and Obtrusiveness." *Marketing Science*, 30(3), 389–404. DOI: 10.1287/mksc.1100.0583 **[직접 인용 가능]**
43e. Ferrari Dacrema, M., Cremonesi, P., & Jannach, D. (2019). "Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches." *RecSys 2019*. arXiv:1907.06902. DOI: 10.1145/3298689.3347058 **[직접 인용 가능]**
43f. Kohavi, R., Longbotham, R., Sommerfield, D., & Henne, R. M. "Controlled experiments on the web: survey and practical guide." *Data Mining and Knowledge Discovery*, 18, 140–181. DOI: 10.1007/s10618-008-0114-1
43g. Johari, R., Koomen, P., Pekelis, L., & Walsh, D. (2017). "Peeking at A/B Tests." *KDD 2017*, 1517–1525. DOI: 10.1145/3097983.3097992 / (2022) *Operations Research*, 70(3), 1806–1821. DOI: 10.1287/opre.2021.2135
43h. Benjamini, Y., & Hochberg, Y. (1995). "Controlling the False Discovery Rate." *JRSS-B*, 57(1), 289–300. DOI: 10.1111/j.2517-6161.1995.tb02031.x
43i. Covington, P., Adams, J., & Sargin, E. (2016). "Deep Neural Networks for YouTube Recommendations." *RecSys 2016*, 191–198. DOI: 10.1145/2959100.2959190
43j. 전체 목록(D-1~D-8, 40여 편)은 `research/papers.md` 참조.

### 커리어·커뮤니티 (1차)
43. 원티드 채용 공고 (조회일 **2026-07-25**) — AB180 ID 330977·370636·370582·365460 / 빅인사이트 ID 359453 / 마티니아이오 ID 349957 / 채널톡 ID 324639
44. Greenhouse Job Board API (조회일 **2026-07-25**) — Braze(236) / Klaviyo(152) / Twilio(183) / Hightouch(70)
45. AB180 엔지니어링. "Data Pipeline Team 인터뷰" ⚠️ **게시일 미상**
46. 마티니. 문소윤, "이벤트 택소노미 완벽 설계하기(1)", **2024-05-30**
47. 노티플라이. "카카오 알림톡 심사 한번에 통과하기", **2025-08-26** / "CRM 마케팅이란?", **2023-10-24**
48. FlareLane. "CRM 마케팅이란 무엇일까?", **2025-04-22**
49. Hacker News 댓글 50여 건 — 개별 objectID·게시일은 `research/community.md` 신선도 원장 참조

---

## 신선도 원장 (소스별 발행일·버전 시점)

> **이 표가 `research/*.md`가 정리되더라도 남는 그라운딩이다.** Phase 4 fact-checker는 본문의 버전·수치 주장을 이 표와 대조한다.
> **전 항목 검색 시점: 2026-07-25**

### A. 버전·릴리스 (기술 스택)

| 소스 | URL | 버전/연도 기준 | 확정 수준 | 관련 축 |
|---|---|---|---|---|
| Apache Kafka | archive.apache.org/dist/kafka/ | **4.3.1 / 2026-06-23** | ✅ 확정 (전체 타임스탬프) | §4-2 |
| Apache Flink | flink.apache.org/downloads/ | **2.3.0 / 2026-06-25** (LTS 1.20.5 / 2026-06-03) | ✅ 확정 (페이지 표기) | §4-3 |
| Apache Iceberg | archive.apache.org/dist/iceberg/ | **1.11.0 / 2026-05-19** | ✅ 확정 | §4-4 |
| Apache Pinot | archive.apache.org/dist/pinot/ | **1.5.1 / 2026-06-30** | ✅ 확정 | §4-4 |
| Apache Druid | archive.apache.org/dist/druid/ | **37.0.0 / 2026-05-06** | ✅ 확정 | §4-4 |
| Trino | trino.io/docs/current/release.html | **483 / 2026-07-17** | ✅ 확정 | §4-4 |
| DuckDB | duckdb.org/news/ | **1.5.5 / 2026-07-22** (LTS 1.4.5 / 2026-06-17) | ✅ 확정 | §4-4 |
| dbt-core | github.com/dbt-labs/dbt-core/releases | **1.12.0 / 2026-07-16** (2.0은 alpha) | ✅ 확정 | §4-3 |
| Snowplow SLULA | docs.snowplow.io/docs/licensing/limited-use-license-faq/ | **v1.1 / 2024-12** (v1.0 / 2024-01) | ✅ 확정 | §4-2 |
| ClickHouse | github.com/ClickHouse/ClickHouse/releases | **26.x 계열 / 2026** | ⚠️ 연도 추정 | §4-4 |
| Redis | github.com/redis/redis/releases | **8.8.1 / 2026** | ⚠️ 연도 추정 | §4-5 |
| Feast | github.com/feast-dev/feast/releases | **0.65.0 / 2026** | ⚠️ 연도 추정 | §4-9 |
| rudder-server | github.com/rudderlabs/rudder-server/releases | **1.81.1 / 2026** | ⚠️ 연도 추정 | §4-2 |
| Snowplow (모노레포) | github.com/snowplow/snowplow/releases | **비활성 릴리스 라인 — 현행 버전 확인 불가** | ❌ | §4-2 |

### B. 벤더 문서 (제품·API)

| 소스 | URL | 발행일/버전 시점 | 관련 축 |
|---|---|---|---|
| Insider Web SDK | academy.insiderone.com/docs/insider-web-sdk-integration-guide | 페이지 표기 2026-07-23 | §6-3 |
| Insider UCD | academy.insiderone.com/docs/unified-customer-database-ucd | 페이지 표기 2026-04-22 | §6-2 |
| **Insider API Rate Limits** | academy.insiderone.com/docs/api-rate-limits | **페이지 표기 2026-07-12 — 인용 시 병기 필수** | §6-4 |
| Insider Upsert API | academy.insiderone.com/docs/upsert-user-data-api | 페이지 참조일 2026-07-24 | §6-4 |
| Insider Predictive Segments | academy.insiderone.com/docs/audience-predictive-segments | 페이지 표기 2026-04-12 | §3-N |
| Insider Series E | insiderone.com/news/... | **2024-11-01** | §6-1 |
| Insider iOS SDK | github.com/useinsider/Insider-iOS-SDK | InsiderMobile **v15.1.1** (리포 태그 v1.9.1 — 상충) | §6-6 |
| Segment Spec (전 문서) | raw.githubusercontent.com/segmentio/segment-docs/develop/... | 발행일 미표기 (develop 브랜치 / 2026-07 조회) | §1-3, §1-4 |
| **Klaviyo API** | developers.klaviyo.com/en/reference/api_overview | **API 버전 v2026-07-15** | §2-8 |
| Adobe RTCDP | experienceleague.adobe.com/.../rtcdp/home | 문서 표기 2026-06-18 | §2-1 |
| Adobe XDM | experienceleague.adobe.com/.../xdm/home | 문서 표기 2026-05-23 | §1-2 |
| Adobe Journey Optimizer | experienceleague.adobe.com/.../journey-optimizer/... | 문서 표기 2026-07-01 | §2-6 |
| Adobe Identity Service | experienceleague.adobe.com/.../identity-service | 2026-06-18 | §5-4 |
| mParticle 문서 / IDSync | docs.mparticle.com | 문서 표기 2026-07-16 | §2-7, §5-4 |
| Bloomreach Engagement | documentation.bloomreach.com/engagement/docs | 상대 시각만 ("9 days ago") — 절대 날짜 미확인 | §1-2, §5-4 |
| Airship | www.airship.com/docs/ | 문서 내 최신 항목 2026-07-23 | §2-7 |
| Hightouch 문서 | hightouch.com/docs/getting-started/concepts | "Last updated Jul 17, 2026" | §2-2 |
| Hightouch composable CDP 블로그 | hightouch.com/blog/composable-cdp | **2023-06-20** ⚠️ 3년 경과 | §2-2 |
| Airbridge | help.airbridge.io/en/references/introduction | "Last updated April 8, 2026" | §2-5 |
| 그루비 | groobee.net/tech/data/ | 저작권 표기 **2023** ⚠️ 갱신 안 된 가능성 | §2-7 |
| 빅인 | bigin.io | 페이지 내 최신 날짜 2025-12-03 | §2-7 |
| chiefmartec 랜드스케이프 | chiefmartec.com | **2026-05-05 (15,505개)** | §2-0-5 |

### C. 카테고리 정의 (Raab)

| 소스 | 발행일 | 경과 | 사용 규율 |
|---|---|---|---|
| Raab — CDP 최초 명명 | **2013-04-25** | ⚠️ 13년 | **기원 서술 전용.** 현재 제품 정의로 쓰지 마라 |
| Raab — 정의 개정 | **2015-01-18** | ⚠️ 11년 | 정의 인용 시 연도 병기 |
| Raab — 유형 분류 | **2018-11-03** | ⚠️ 8년 | **"2018년 Raab 기준" 병기 필수.** 3분류(Data/Analytics/Personalization) |

### D. 프라이버시·규제 (변동이 가장 심한 축)

| 소스 | 발행일/시행일 | 관련 축 | 비고 |
|---|---|---|---|
| Google — 3PC 유지 결정 | **2025-04-22** | §5-1 | 폐지 철회 |
| Google — Privacy Sandbox 기술 은퇴 | **2025-10-17** | §5-1 | 11개 API 은퇴 |
| Privacy Sandbox status 페이지 | 페이지 최종 갱신 **2025-10-17** | §5-1 | ⚠️ 2026 갱신본 미확인 |
| Chrome 144 릴리스 노트 | stable **2026-01-13** | §5-1 | |
| blink-dev Topics deprecate | 2025-11-08, 갱신 **2026-06-12** | §5-1 | 사용률 4.9% |
| UK CMA 약속 해제 | 결정 **2025-10-17** | §5-1 | ⚠️ PDF 본문 미조회 |
| WebKit ITP 전면 차단 | **2020-03-24** | §5-1 | 7일 스토리지 캡 |
| WebKit CNAME 방어 | **2020-11-12** | §5-1, §5-2 | |
| Mozilla TCP | **2022-06-14** (업데이트 2024-08-28) | §5-1 | ⚠️ 버전 번호 미확인 |
| Apple ATT / 정책 | 발행일 표기 없음 (상시 갱신) | §5-1 | |
| Meta CAPI dedup | 발행일 표기 없음 | §5-2 | **48시간 창** |
| **IAB TCF v2.3** | **2025-06-19** | §5-3 | **2026-03-01부터 강제** |
| Google Consent Mode | 발행일 표기 없음 | §5-3 | ⚠️ 문서가 "v2" 라벨 미사용 |
| **W3C GPC** | **2026-06-11 (Working Draft)** | §5-3 | Recommendation 아님 |
| UID2 | **문서 최종 갱신 2026-07-23** | §5-4 | 매우 신선 |
| Google Ads Data Hub | 발행일 표기 없음 | §5-5 | **20/50/10 임계값** |
| **개인정보 보호법** | **시행 2025-10-02, 법률 제20897호** | §5-6-1 | law.go.kr 원문 |
| **정보통신망법 제50조** | **시행 2026-07-07, 법률 제21305호** | §5-6-2 | **야간 오후 9시~오전 8시 + 단서** |
| PIPC 안내서 목록 | 최신 항목 **2026-06-25** | §5-6-1 | 본문 미조회 |
| GDPR (EUR-Lex) | 2016-04-27 | §5-6-3 | 조문 전문 미확보 |
| EU AI Act 타임라인 | 페이지 갱신일 표기 없음 | §5-6-3 | **"2026년 7월 기준" 명시 필수** |

### E. 학술 논문 (전부 2026-07-25 Crossref/arXiv/Semantic Scholar API 조회)

> **확인 수준이 곧 인용 권한이다.** `초록 확인`만 직접 인용 가능. `메타데이터 확인`은 **구체 수치를 그 논문에 귀속시키지 마라.**
>
> **`papers.md` 최종 집계 (총 100건 서지 확정, 1,419줄):**
>
> | 확인 수준 | 건수 | 인용 권한 |
> |---|---|---|
> | **초록 확인** (초록 전문 조회) | **8** | ✅ 직접 인용 가능 |
> | **문서 확인** (RFC·기업 기술보고서·제품문서·저자 노트) | **7** | ✅ 인용 가능, **peer-review 아님을 병기** |
> | 초록 확인 (요약본만) ⚠️ | 1 | **수치 귀속 금지** (Gordon 2019) |
> | **메타데이터 확인** (서지만 확정, 초록 미조회) | **84** | **수치·결론 방향 귀속 금지** |
> | 확인 불가 / 미조회 | 12 | 인용 금지 |
> | **학술 근거 없음 / 업계 관행** | **12** | 그렇게 표기할 것 |
>
> 🚨 **본문(full text) 확인은 0건이다.** 논문 본문 표·그림의 수치가 필요하면 **fact-checker가 PDF를 직접 열어야 한다.**

| 논문 | 연도 | DOI / arXiv ID | 확인 수준 | 관련 축 |
|---|---|---|---|---|
| Schmittlein, Morrison & Colombo — Pareto/NBD | 1987 | `10.1287/mnsc.33.1.1` | 메타데이터 확인 (피인용 687) | §3-B |
| Bult & Wansbeek — Optimal Selection for Direct Mail | 1995 | `10.1287/mksc.14.4.378` | 메타데이터 확인 | §3-B |
| Benjamini & Hochberg — FDR | 1995 | `10.1111/j.2517-6161.1995.tb02031.x` | 메타데이터 확인 | §3-F |
| Linden, Smith & York — 아이템 기반 CF | 2003 | (papers.md D-6-1) | 메타데이터 확인 | §3-D |
| Fader, Hardie & Lee — RFM/CLV iso-value | 2005 | `10.1509/jmkr.2005.42.4.415` | 메타데이터 확인 | §3-B |
| Fader, Hardie & Lee — BG/NBD | 2005 | `10.1287/mksc.1040.0098` | 메타데이터 확인 (피인용 501) | §3-B |
| Awad & Krishnan — 개인화-프라이버시 역설 | 2006 | `10.2307/25148715` | 메타데이터 확인 | §3-C |
| Gupta et al. — CLV 서베이 | 2006 | `10.1177/1094670506293810` | 메타데이터 확인 | §3-B |
| White et al. — 개인화 리액턴스 | **2007/2008** ⚠️연도 상충 | `10.1007/s11002-007-9027-9` | 메타데이터 확인 | §3-C |
| Kohavi et al. — Controlled experiments on the web | **2008/2009** ⚠️ | `10.1007/s10618-008-0114-1` | 메타데이터 확인 | §3-F |
| Koren, Bell & Volinsky — 행렬 분해 | 2009 | (papers.md D-6-2) | 메타데이터 확인 | §3-D |
| Fader, Hardie & Shang — BG/BB | 2010 | `10.1287/mksc.1100.0580` | 메타데이터 확인 | §3-B |
| **Goldfarb & Tucker — 개인화 역효과** | 2011 | `10.1287/mksc.1100.0583` | **초록 확인 (직접 인용 가능)** · 피인용 814 | §3-C |
| Braun & Schweidel — 경쟁 위험 이탈 | 2011 | `10.1287/mksc.1110.0665` | 메타데이터 확인 | §3-B |
| Kohavi et al. — Trustworthy OCE | 2012 | `10.1145/2339530.2339653` | 메타데이터 확인 | §3-F |
| Deng et al. — CUPED | 2013 | `10.1145/2433396.2433413` | 메타데이터 확인 | §3-F |
| Kohavi et al. — OCE at large scale | 2013 | `10.1145/2487575.2488217` | 메타데이터 확인 | §3-F |
| Tucker — 프라이버시 통제권 | **2013/2014** 🚨서지 상충 | `10.1509/jmr.10.0355` | 메타데이터 확인 | §3-C |
| McMahan et al. — FTRL | 2013 | (papers.md D-7-1) | 메타데이터 확인 | §3-E |
| Covington et al. — YouTube 2단계 | 2016 | `10.1145/2959100.2959190` | 메타데이터 확인 | §3-D |
| Eckles, Karrer & Ugander — 네트워크 간섭 | 2016 | `10.1515/jci-2015-0021` | 메타데이터 확인 | §3-F |
| Cheng et al. — Wide & Deep | 2016 | (papers.md D-7-4) | 메타데이터 확인 | §3-E |
| Johari et al. — Peeking at A/B Tests | 2017 | `10.1145/3097983.3097992` | 메타데이터 확인 | §3-F |
| Johari et al. — Always Valid Inference | 2022 | `10.1287/opre.2021.2135` | 메타데이터 확인 | §3-F |
| Saveski et al. — Detecting Network Effects | 2017 | `10.1145/3097983.3098192` | 메타데이터 확인 | §3-F |
| **Ferrari Dacrema et al. — 추천 재현성** | 2019 | arXiv **1907.06902** / `10.1145/3298689.3347058` | **초록 확인 (직접 인용 가능)** · 피인용 686 | §3-D |
| Rendle et al. — NCF vs MF Revisited | 2020 | arXiv **2005.09683** | 메타데이터 확인 | §3-D |
| **Blake, Nosko & Tadelis — eBay 검색광고 실험** | 2015 | `10.3982/ecta12423` / NBER `10.3386/w20171` | **초록 확인 (NBER 페이지)** | §3-I |
| **Berman — Beyond the Last Touch** | 2018 | `10.1287/mksc.2018.1104` | **초록 확인 (직접 인용 가능)** · 피인용 135 | §3-H |
| Gordon, Zettelmeyer et al. — Facebook 실험 비교 | 2019 | `10.1287/mksc.2018.1135` | 초록 확인 **(요약본만 — 수치 귀속 금지)** · 피인용 291 | §3-I |
| **Gordon, Moakler & Zettelmeyer — "Close Enough?"** | 2023 | `10.1287/mksc.2022.1413` / arXiv **2201.07055** | **초록 확인 (전문) — 29/18/5 vs 83/58/24 vs 173/176/64** · 피인용 65 | §3-I |
| Johnson, Lewis & Nubbemeyer — Ghost Ads | 2017 | (papers.md D-10-4) | (papers.md 참조) | §3-I |
| Jin, Wang, Sun, Chan & Koehler — 베이지안 MMM | 2017 | (Google 기술 보고서) | 초록 확인 **(peer-reviewed 아님)** | §3-H |
| Vaver & Koehler — 지오 실험 | 2011 | (Google 기술 보고서) | 초록 확인 **(기업 기술 보고서)** | §3-H |
| Anderl et al. — 마르코프 어트리뷰션 | 2016 | (papers.md D-4-2 / D-9-2) | 메타데이터 확인 | §3-G, §3-H |
| Lemon & Verhoef — 고객 여정 | 2016 | (papers.md D-4-1) | (papers.md 참조) | §3-G |
| **Hardie — Gamma-Gamma** | note 갱신 2013 | ❌ **DOI 없음 — 미간행 기술 노트** | 초록 확인 (랜딩 페이지) | §3-A |
| **가격·프로모션·쿠폰 인과 효과** | — | ❌ **미확보** | — | §3-J |
| **LTV/CAC 3:1** | — | ❌ **학술 근거 확인 불가 — 업계 관행** | — | §3-A |
| **홀드아웃 그룹 설계 / 리텐션 커브 형태** | — | ❌ **정전 논문 미특정** | — | §3-A |

**기반 기술 C축 (C-16~C-22) — 전부 `메타데이터 확인` 이상, 상세 서지는 §3-K:**

| 논문 | 연도 | DOI / arXiv ID | 관련 축 |
|---|---|---|---|
| Bloom — 블룸 필터 | 1970 | `10.1145/362686.362692` | §4-5 |
| Flajolet et al. — HyperLogLog | 2007 | `10.46298/dmtcs.3545` | §4-5 |
| Heule, Nunkesser & Hall — HLL in practice | 2013 | `10.1145/2452376.2452456` | §4-5 |
| Cormode & Muthukrishnan — Count-Min Sketch | 2005 | `10.1016/j.jalgor.2003.12.001` | §4-5 |
| Dunning & Ertl — t-digest | 2019 | arXiv **1902.04023** | §4-5 |
| **Dasgupta, Lang, Rhodes & Thaler — Theta Sketch** | 2016 | arXiv **1510.01455** / ICDT 2016 | §4-5 ⚠️**저자 오인용 주의** |
| Akidau et al. — Dataflow Model | 2015 | (papers.md C-17-1) | §4-3 |
| Kreps, Narkhede & Rao — Kafka | 2011 | (papers.md C-17-2) ⚠️위상 주의 | §4-2 |
| Carbone et al. — Flink 상태 관리 | 2017 | (papers.md C-17-3) | §4-3 |
| **Lambda / Kappa** | — | ❌ **peer-reviewed 아님 — 블로그 출처** | §4-8 |
| Abadi et al. — 컬럼 스토어 서베이 | 2013 | (papers.md C-18-2) | §4-4 |
| Yang et al. — Druid / Im et al. — Pinot | 2014 / 2018 | (papers.md C-18-4·5) | §4-4 |
| **Fellegi & Sunter — 확률적 레코드 링키지** | 1969 | (papers.md C-19-1) | §4-6, §5-4 |
| Papadakis et al. — 블로킹 서베이 | 2020 | (papers.md C-19-4) | §4-6 |
| **Dwork et al. — 차등 프라이버시** | 2006 | (papers.md C-20-1) | §5-5 |
| Sweeney — k-익명성 | 2002 | (papers.md C-20-2) | §5-5 |
| Pinkas, Schneider & Zohner — PSI | 2018 | (papers.md C-20-5) | §5-5 |
| McMahan et al. — 연합 학습 | 2017 | (papers.md C-20-3) | §5-5 |
| **Grib et al. — Privacy Sandbox의 흥망** | **2026** | (papers.md C-20-8) | §5-1 ⭐최신 |
| Yu et al. — Spider / Li et al. — BIRD | 2018 / 2023 | (papers.md C-21-1·2) | §4-9 |
| **Sculley et al. — ML 기술 부채** | 2015 | (papers.md C-22-1) | §4-9 |
| **LLM 카피 효과 크기** | — | ❌ **미확보** | §4-9 |

### F. 커뮤니티·커리어 (조회 스냅샷)

| 소스 | 시점 | 비고 |
|---|---|---|
| 원티드 공고 7건 본문 | **active 스냅샷 2026-07-25** | 공고는 마감되면 사라진다 — 조회일 병기 필수 |
| 채널톡 백엔드 공고 ID 34197 | **마감 2022-12-14** | ⚠️ 구자료. 현재 스택 근거로 쓰지 마라 |
| Greenhouse 4사 641건 | **2026-06-16~07-25 갱신** | |
| AB180 엔지니어링 블로그 | ❌ **게시일 미상** | 조직 수치·트래픽 수치 전부 시점 미상 |
| 마티니 택소노미 | **2024-05-30** | |
| 노티플라이 알림톡 가이드 | **2025-08-26** | 카카오 공식 문서 미조회 → 2차 자료 |
| 노티플라이 CRM 마케팅 | **2023-10-24** | 벤더 블로그 |
| FlareLane CRM 마케팅 | **2025-04-22** | 벤더 블로그 |
| HN 댓글 50여 건 | 2012-07-07 ~ **2026-05-18** | 개별 objectID는 community.md 참조 |
| GitHub 이슈 (RudderStack/Snowplow) | 2014 ~ 2026-01 | 제목·날짜만 (rate limit) |

---

<!-- 합성 완료: 2026-07-25 / research-lead -->
<!-- 리서치 실행: web-researcher ×4(제품·스택·프라이버시·갭필러) + paper-researcher + community-researcher -->
<!-- 보존 산출물: 01_reference.md + research/{web,web_products,web_stack,web_privacy,web_gaps,papers,community}.md -->
<!-- 미결: §3-H의 학술 축(어트리뷰션·증분성·업리프트·밴딧·근사자료구조 원논문 등)은 papers.md D-9 이후 미기록 -->
<!-- 저술 전 필독: §9 리서치 공백 / 인용 금지 목록 -->

