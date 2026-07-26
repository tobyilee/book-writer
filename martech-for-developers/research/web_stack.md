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
