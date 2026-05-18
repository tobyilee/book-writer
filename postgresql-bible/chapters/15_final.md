# 15장. 분석·OLAP·시계열 — Citus·TimescaleDB·DuckDB

분석은 빠른 DB로, 운영은 정확한 DB로 — 그렇게 둘로 갈라야 한다고 누가 정했을까. 한 쪽에서는 결제와 주문이 한 줄씩 들어오고, 다른 쪽에서는 매일 밤 ETL이 수억 줄을 빨아다 컬럼 스토어에 쌓는다. 분석가는 ClickHouse를 보고 개발자는 PostgreSQL을 본다. 두 데이터가 서로 다른 시점에 살아 있고, 누군가는 늘 "어제 데이터까지만 보입니다"라는 답을 듣는다. 익숙한 풍경이다. 그리고 한참 동안은 그게 정답이었다.

그런데 2026년의 PostgreSQL은 같은 답을 그대로 받아들이지 않는다. 윈도우 함수와 머티리얼라이즈드 뷰의 기본기 위에, Citus가 분산을 얹고, TimescaleDB가 시계열을 얹고, Hydra와 AlloyDB가 컬럼 엔진을 얹고, pg_duckdb가 DuckDB 벡터화 엔진을 통째로 끌어들인다. 한 클러스터 안에서 OLTP 한 줄과 OLAP 한 페이지가 같이 살 수 있는 시대가 열리고 있다는 뜻이다.

그 선이 어디까지 그어졌는지, 그리고 어떤 워크로드까지는 PostgreSQL 한 쪽으로 합쳐도 되는지 같이 따져보자. 처음에는 SQL 표준이 이미 준 기본 도구로 시작하고, 그다음에는 익스텐션 한 겹씩을 더해가며 분석 한계를 어디까지 밀 수 있는지 살펴본다. 마지막에는 ClickBench의 숫자 한 장을 함께 해석하면서, "익스텐션 composability가 진짜 moat"라는 말이 무슨 뜻인지 정직하게 따져볼 것이다.

## 15.1 윈도우·CUBE·머티리얼라이즈드 뷰 — 익스텐션 없이도 갈 수 있는 곳

월별 매출 누적 추이를 뽑아 달라는 요청을 받았다고 해보자. 머릿속에 두 가지 답이 떠오를 것이다. 하나는 "분석 DB로 던지자"이고, 다른 하나는 "윈도우 함수 한 줄이면 끝난다"이다. 둘 다 옳다. 그런데 두 번째 답을 PostgreSQL 위에서 가볍게 시도해 보지 않으면, 첫 번째 답으로 너무 빨리 도망가게 된다.

PostgreSQL의 분석 기본기는 ANSI SQL 표준을 충실히 지킨다는 데서 시작한다. 그리고 그 표준에는 우리가 평소에 잘 안 쓰는 무기들이 꽤 많다. 윈도우 함수, CUBE·ROLLUP·GROUPING SETS, 머티리얼라이즈드 뷰, 그리고 v17에서 들어온 JSON_TABLE까지. 익스텐션을 한 줄도 깔지 않은 순정 PostgreSQL에서 이미 작은 OLAP 워크로드의 70% 정도는 처리할 수 있다.

### 윈도우 함수 — 행을 잃지 않고 집계하기

GROUP BY를 쓰면 원본 행이 사라진다. 매출 합계는 나오는데, 어떤 주문이 그 합계에 기여했는지를 같이 보고 싶을 때는 곤란하다. 윈도우 함수는 그 곤란을 풀어준다.

```sql
SELECT
    order_date,
    customer_id,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,
    AVG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg,
    RANK() OVER (
        PARTITION BY DATE_TRUNC('month', order_date)
        ORDER BY amount DESC
    ) AS monthly_rank
FROM orders
WHERE order_date >= '2026-01-01';
```

행 하나하나에 그 행의 맥락(누적 합계, 7일 이동평균, 월별 순위)이 같이 붙어 나온다. 애플리케이션 코드에서 따로 계산하지 않아도, 쿼리 한 번이면 끝난다. ClickHouse를 따로 세우는 결정을 너무 빨리 내리지 말자는 첫 번째 신호가 여기서 나온다.

윈도우 함수의 진짜 힘은 `PARTITION BY`, `ORDER BY`, `ROWS/RANGE` 프레임이 합쳐졌을 때 드러난다. `LAG`와 `LEAD`로 이전·다음 행을 끌어오고, `FIRST_VALUE`·`LAST_VALUE`로 윈도우의 양 끝을 잡고, `PERCENTILE_CONT`로 분위수를 구한다. 이 정도면 "이 사용자의 어제 거래 대비 오늘 거래 증감률" 같은 코호트 분석을 SQL 한 장에서 끝낼 수 있다.

### CUBE·ROLLUP·GROUPING SETS — 다차원 집계의 표준

대시보드를 만들다 보면 "총합, 월별 합, 카테고리별 합, 월×카테고리 교차 합 — 다 한 번에 보여 달라"는 요구가 들어온다. 네 번 GROUP BY를 돌려서 UNION ALL로 붙이는 답도 가능하다. 그런데 번거롭다. 그리고 표가 깔끔하게 떨어지지 않는다.

ROLLUP과 CUBE는 이 번거로움을 깎는다.

```sql
SELECT
    DATE_TRUNC('month', order_date) AS month,
    category,
    region,
    SUM(amount) AS total,
    GROUPING(month, category, region) AS grouping_id
FROM orders
GROUP BY ROLLUP(DATE_TRUNC('month', order_date), category, region)
ORDER BY month NULLS LAST, category NULLS LAST, region NULLS LAST;
```

`ROLLUP(a, b, c)`는 `(a, b, c)`, `(a, b)`, `(a)`, `()` — 즉 점점 더 큰 묶음으로 집계한 결과를 한 번에 돌려준다. `CUBE`는 모든 가능한 조합을 다 만들어내고, `GROUPING SETS`는 우리가 직접 어떤 조합을 뽑을지 명시한다. 한 쿼리에서 여러 깊이의 소계와 총계가 나오니, BI 도구에 던지기 전에 한 번 처리해 두면 트래픽도 줄어든다.

`GROUPING()` 함수는 보너스다. 결과의 어떤 컬럼이 "소계 행"인지 표시해 주는 비트마스크라, 프런트엔드에서 합계 행을 굵게 표시할 때 쓴다. 익숙해지면 GROUP BY를 네 번 돌려서 UNION ALL로 붙이던 시절이 찜찜하게 느껴진다.

### 머티리얼라이즈드 뷰 — 한 번 계산해 두고 다시 안 쓴다

복잡한 집계 쿼리를 매번 새로 계산하면 비용이 누적된다. 매출 대시보드가 5초 걸리는데 그 페이지에 10명이 동시 접속한다고 해 보자. CPU가 끓는다. 그리고 대시보드 데이터는 1시간 단위로만 갱신해도 충분한 경우가 많다.

머티리얼라이즈드 뷰는 이 시나리오의 정공법이다.

```sql
CREATE MATERIALIZED VIEW monthly_revenue_summary AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    category,
    region,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_amount
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY DATE_TRUNC('month', order_date), category, region
WITH DATA;

CREATE UNIQUE INDEX ON monthly_revenue_summary (month, category, region);
```

조회는 일반 테이블처럼 빠르고, 갱신은 명시적으로 결정한다.

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue_summary;
```

`CONCURRENTLY` 옵션이 핵심이다. 이게 없으면 갱신 동안 뷰에 대한 모든 조회가 막힌다. 끔찍한 일이다. `CONCURRENTLY`는 유니크 인덱스를 요구하는 대신 조회를 막지 않고 새 데이터로 교체한다. pg_cron으로 1시간마다 호출하도록 걸어두면, 대시보드는 거의 무공짜로 빠르게 뜬다.

물론 한계도 있다. PostgreSQL의 머티리얼라이즈드 뷰는 **증분 갱신을 지원하지 않는다**. 전체를 다시 계산한다. 매출 테이블이 10억 행이라면 매시간 10억 행을 다시 훑어야 한다는 뜻이다. 그래서 시계열 워크로드에서는 TimescaleDB의 continuous aggregate가 답이 된다. 그 이야기는 15.3에서 본격적으로 하자.

### LATERAL과 윈도우의 결합 — 표준 SQL의 숨은 무기

윈도우 함수에 한 가지를 더 얹으면 표현력이 한 단계 더 올라간다. 바로 LATERAL이다. LATERAL은 FROM 절에서 앞쪽 행마다 서브쿼리를 따로 돌리는 표준 SQL 구문이다. 각 사용자별로 "가장 최근 주문 3건"을 한 줄에 펼쳐서 보고 싶다면, LATERAL 없이는 꽤 번거롭다.

```sql
SELECT
    u.user_id,
    u.email,
    recent.order_id,
    recent.amount,
    recent.created_at,
    recent.rn
FROM users u
CROSS JOIN LATERAL (
    SELECT
        o.order_id,
        o.amount,
        o.created_at,
        ROW_NUMBER() OVER (ORDER BY o.created_at DESC) AS rn
    FROM orders o
    WHERE o.user_id = u.user_id
    ORDER BY o.created_at DESC
    LIMIT 3
) recent
WHERE u.created_at >= NOW() - INTERVAL '30 days';
```

각 사용자 행마다 서브쿼리가 한 번씩 돌면서 최근 주문 3건을 끌어온다. ROW_NUMBER가 그 안에서 순위를 매긴다. 결과는 사용자 × 주문3건이 평평한 표로 펼쳐진다. 한 쿼리에서 "Top-N per group" 패턴이 깔끔하게 풀린다.

이 정도 표현력은 ClickHouse나 BigQuery에도 다 있다. 그런데 그 표현력이 익스텐션 한 줄 없이 순정 PostgreSQL에 처음부터 들어 있다는 점이 PostgreSQL의 정직한 강점이다. ANSI SQL 표준에 충실하다는 게 단순한 마케팅 문구가 아니다. 표현력의 출발점이 한참 위에 있다는 뜻이다.

### JSON_TABLE — JSON을 분석 컬럼으로 펼치기

v17에서 들어온 JSON_TABLE은 분석 쿼리의 표면적을 한층 넓혔다. JSONB 컬럼에 박혀 있는 이벤트 페이로드를 SQL FROM 절에서 평평한 표로 펼쳐서 윈도우·집계·조인에 그대로 끌어쓸 수 있다.

```sql
SELECT
    e.event_id,
    e.created_at,
    j.path AS click_path,
    j.duration_ms,
    SUM(j.duration_ms) OVER (PARTITION BY e.user_id ORDER BY e.created_at) AS cumulative_time
FROM events e,
     JSON_TABLE(e.payload, '$.clicks[*]'
         COLUMNS (
             path TEXT PATH '$.path',
             duration_ms INTEGER PATH '$.duration_ms'
         )) AS j
WHERE e.created_at >= NOW() - INTERVAL '1 day';
```

이전에는 `jsonb_array_elements`로 풀어내고 별칭과 캐스트를 줄줄이 붙여야 했던 일이 한 번에 정돈된다. JSON 페이로드를 분석 자산으로 다루는 워크로드라면, 17 업그레이드의 가장 큰 보상 중 하나가 이 함수일 것이다.

### 기본기의 한계는 어디서 오는가

여기까지가 익스텐션을 한 줄도 깔지 않은 PostgreSQL이다. 작은 분석 워크로드, 그러니까 수천만 행에서 수억 행 사이의 데이터를 다루는 대시보드라면 이 기본기만으로도 ClickHouse를 안 세워도 된다. 그런데 행이 100억을 넘기 시작하면 신호가 온다. 시퀀셜 스캔이 디스크 IO를 다 잡아먹고, 머티리얼라이즈드 뷰의 풀 리프레시가 끝나지 않고, 단일 노드의 CPU와 메모리가 천장에 부딪힌다.

그렇다면 다음 단계는 어디일까. 두 갈래다. **분산**으로 가거나, **컬럼**으로 가거나. PostgreSQL 진영의 익스텐션들은 이 두 갈래를 각자 다른 각도에서 푼다. Citus가 분산을, TimescaleDB·Hydra·AlloyDB가 컬럼을, pg_duckdb는 둘 다를 묶어버린다. 하나씩 살펴보자.

## 15.2 Citus — PostgreSQL을 분산 데이터베이스로 바꾸는 익스텐션

10년 전쯤이라면 "PostgreSQL을 샤딩한다"는 말은 자체적으로 라우팅을 짜고, 글로벌 시퀀스를 따로 관리하고, 노드 간 조인을 애플리케이션에서 풀어야 한다는 뜻이었다. 끔찍한 일이다. 분산 트랜잭션이 깨질까 봐 두렵고, 노드 추가 시 리밸런싱이 무서워서 처음부터 노드 수를 과하게 잡았다. 그러다 보면 결국 "그냥 ClickHouse로 갈까" 같은 결론이 자주 나왔다.

Citus는 이 풍경을 바꿨다. PostgreSQL의 정체성을 그대로 유지하면서, 단일 익스텐션 설치만으로 클러스터 전체를 분산 쿼리 엔진처럼 쓰게 만든다. Microsoft가 인수한 뒤에도 오픈소스로 유지하고 있고, 2026년 현재 분산 PostgreSQL의 사실상 표준 위치에 있다.

### 샤딩의 기본 — 데이터를 어떻게 자를 것인가

샤딩 일반론을 잠깐 짚고 가자. 분산 DB의 첫 번째 결정은 "데이터를 어떤 키로 자를 것인가"다. postgresql.kr에서 정리한 샤딩 자료가 깔끔하게 짚는데, 크게 세 가지 전략이 있다.

- **Range sharding** — 시간이나 ID 범위로 자른다. "1월 데이터는 노드 A, 2월은 노드 B" 식. 직관적이지만 핫스팟이 잘 생긴다. 최신 데이터가 늘 마지막 노드에 몰리기 때문이다.
- **Hash sharding** — 키 값에 해시 함수를 돌려서 어떤 노드에 갈지 결정한다. 분포가 고르고 핫스팟이 잘 안 생기지만, 범위 쿼리(`WHERE date BETWEEN ...`)에서는 모든 노드를 다 훑어야 한다.
- **Directory(lookup) sharding** — 어떤 키가 어떤 노드에 있는지 별도 디렉토리 테이블에 적어둔다. 유연하지만 디렉토리가 단일 장애점이 된다.

대부분의 OLTP 워크로드에서는 **hash sharding**이 정답에 가깝다. Citus가 기본으로 채택한 전략도 이쪽이다. 멀티테넌트 SaaS라면 `tenant_id`로 해시, 이벤트 로그라면 `user_id`로 해시 — 거의 모든 쿼리가 자연스럽게 한 노드 안에서 끝나도록 설계할 수 있다면 그 시스템은 잘 샤딩된 시스템이다.

### Citus의 핵심 기법 — 분산 테이블과 co-located join

Citus의 설치는 단순하다.

```sql
CREATE EXTENSION citus;
SELECT citus_add_node('worker-1', 5432);
SELECT citus_add_node('worker-2', 5432);
SELECT citus_add_node('worker-3', 5432);
```

이제 일반 테이블을 분산 테이블로 바꾼다.

```sql
CREATE TABLE events (
    event_id BIGSERIAL,
    tenant_id UUID NOT NULL,
    user_id BIGINT NOT NULL,
    event_type TEXT,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_distributed_table('events', 'tenant_id');
```

`create_distributed_table`을 호출하는 순간, 기본 32개(설정 가능) 샤드로 쪼개진다. 각 샤드는 해시값에 따라 worker 노드에 분배된다. 코디네이터 노드는 어떤 샤드가 어디 있는지를 관리하고, 쿼리가 들어오면 해당 샤드가 있는 노드로 라우팅한다. 애플리케이션은 평소처럼 `SELECT ... FROM events WHERE tenant_id = ?`를 던지면 끝이다. PostgreSQL 드라이버도 그대로, 트랜잭션도 그대로, ORM도 그대로 쓴다.

진짜 마법은 **co-located join**에서 일어난다. 두 테이블을 같은 분산 키로 자르면, 같은 키 값을 가진 행들은 항상 같은 노드에 모인다.

```sql
CREATE TABLE users (
    user_id BIGINT,
    tenant_id UUID NOT NULL,
    email TEXT,
    created_at TIMESTAMPTZ
);

SELECT create_distributed_table('users', 'tenant_id', colocate_with => 'events');
```

이제 `events`와 `users`를 `tenant_id`로 조인하면 — 네트워크 셔플 없이 각 노드에서 로컬 조인이 끝난다. 노드 간 데이터 이동이 거의 없으니 분산 환경이 마치 단일 노드처럼 빠르다. 잘 설계한 멀티테넌트 SaaS에서는 노드를 추가할수록 처리량이 거의 선형으로 늘어나는 풍경을 본다.

### 참조 테이블과 분산 함수

모든 테이블이 분산되어야 하는 건 아니다. 작은 마스터 데이터 — 국가 코드, 카테고리 목록, 설정 같은 — 는 모든 노드에 동일하게 복제해 두는 게 낫다.

```sql
CREATE TABLE countries (code CHAR(2) PRIMARY KEY, name TEXT, region TEXT);
SELECT create_reference_table('countries');
```

`create_reference_table`로 지정하면, 모든 worker 노드에 똑같은 사본이 유지된다. 분산 테이블과 조인할 때 셔플 없이 로컬에서 처리된다. 변경은 코디네이터가 모든 노드에 분산 트랜잭션으로 적용한다.

또 하나 — Citus는 분산 함수(`create_distributed_function`)도 제공한다. 자주 호출되는 procedure를 분산 키와 함께 등록하면, 코디네이터를 거치지 않고 해당 데이터가 있는 노드로 직접 라우팅된다. 코디네이터 병목을 풀고 latency를 한 자릿수 밀리초로 떨어뜨리는 패턴이다.

### Citus가 잘 맞는 워크로드와 안 맞는 워크로드

Citus는 다음과 같은 워크로드에서 빛난다.

- **멀티테넌트 SaaS** — `tenant_id` 분산 키로 자르면 거의 모든 쿼리가 한 노드에서 끝난다. 노드 수가 늘어도 한 테넌트의 latency는 안 변한다. Citus의 가장 자랑할 만한 시나리오.
- **실시간 분석** — 이벤트를 쪼개서 받고, 집계 쿼리를 분산해서 돌린다. 행 수가 수십억을 넘어가는 대시보드에서 효과가 크다.
- **시계열 메트릭** — 시간 범위로 자르거나, 디바이스 ID로 자르거나. 다만 시계열에 특화된 도구가 따로 있으니(15.3) 선택지를 비교해 보는 게 낫다.

반대로 Citus가 안 맞는 워크로드도 있다.

- **분산 키를 찾을 수 없는 워크로드** — 모든 쿼리가 cross-shard 조인을 강요한다면 Citus가 오히려 느리다. 네트워크 셔플 비용이 단일 노드의 IO를 넘어선다.
- **글로벌 트랜잭션이 빈번한 워크로드** — 2PC 비용이 누적되어 응답시간이 늘어진다. 단일 노드 PostgreSQL이 더 빠를 수 있다.
- **단일 노드로도 충분한 워크로드** — 데이터가 1TB 이하, 쿼리가 수백 QPS 수준이라면 Citus의 운영 복잡도가 이득보다 크다. 분산 시스템은 분산이 필요할 때 도입하는 게 좋다.

### 노드 확장과 리밸런싱 — 운영의 결정적 순간

Citus를 운영하다 보면 어느 시점에 노드를 추가해야 하는 순간이 온다. 디스크가 차거나, CPU가 끓거나, 한 노드에 데이터가 몰려 있거나. 이 순간이 분산 DB 운영의 진짜 시험대다. 다행히 Citus는 이 절차를 비교적 매끄럽게 만들어 둔다.

```sql
-- 새 워커 노드 추가
SELECT citus_add_node('worker-4', 5432);

-- 샤드를 새 노드로 재분배 (온라인)
SELECT rebalance_table_shards('events');
```

`rebalance_table_shards`는 기본적으로 온라인 리밸런싱이다. 데이터를 옮기는 동안에도 쿼리가 들어온다. 내부에서 logical replication을 써서 백그라운드로 샤드를 복제하고, 컷오버 순간만 짧게 락을 잡는다. 수십 GB짜리 샤드를 옮길 때도 서비스 중단 없이 끝낼 수 있다.

다만 함정이 있다. 리밸런싱이 끝날 때까지 양쪽 노드 모두에 같은 데이터가 있게 되니, 디스크 사용량이 일시적으로 늘어난다. 디스크가 빠듯한 상태에서 리밸런싱을 시작하면 끔찍한 일이 일어난다. 노드 추가는 디스크 여유가 30% 이상 남았을 때 시작하는 게 안전하다. "디스크가 다 차서 노드를 추가하려는데 추가하려고 보니 디스크가 모자라서 리밸런싱이 안 되는" 상황은 생각보다 흔하다.

### Citus 운영의 함정 모음

Citus를 도입한 팀이 자주 만나는 함정도 같이 정리해 두자.

- **잘못된 분산 키 선택** — 한 번 정한 분산 키는 바꾸기 매우 어렵다. 테이블을 새로 만들고 데이터를 옮겨야 한다. 처음에 신중하게 골라야 한다. 분산 키 선택의 기준은 "거의 모든 쿼리의 WHERE 절에 이 컬럼이 들어가는가"다. 들어간다면 단일 노드로 라우팅되어 빠르다. 안 들어간다면 모든 노드를 다 훑게 된다.
- **참조 테이블의 비대화** — `create_reference_table`은 모든 노드에 사본을 둔다는 뜻이다. 행이 수천만을 넘기 시작하면 동기화 비용이 만만치 않다. 참조 테이블은 작게(보통 수만~수십만 행) 유지하는 게 좋다.
- **글로벌 시퀀스의 비용** — `BIGSERIAL`은 코디네이터를 거쳐 시퀀스를 받아온다. INSERT가 많은 워크로드에서는 코디네이터 병목이 된다. UUIDv7(v18) 같은 분산 친화 ID를 쓰거나, 각 노드별 시퀀스를 따로 두는 패턴이 낫다.
- **분산 DDL의 단일 트랜잭션 비용** — `ALTER TABLE`은 코디네이터가 모든 워커에 분산 트랜잭션으로 적용한다. 노드 수가 많고 한 번에 큰 DDL을 돌리면 한참 멈춘다. 큰 DDL은 새벽에 돌리고, 가능하면 작은 단위로 쪼갠다.

### Production 사례 — Citus가 빛났던 자리

Microsoft가 인수하기 전 Citus의 가장 유명한 production 케이스 중 하나는 Heap이라는 분석 서비스다. 수천 개 고객의 이벤트를 한 클러스터에 담아 실시간 분석을 제공했다. tenant 단위 hash sharding이 거의 모든 쿼리를 한 노드로 라우팅되도록 만들었고, 수십 노드로 선형 확장됐다.

한국 사례로는 medium에 정리된 Rate Labs의 Citus 도입기가 참고할 만하다. PostgreSQL 단일 노드의 한계가 보이기 시작한 자리에서 Citus를 선택했고, 멀티테넌트 구조에서 노드 확장으로 풀어낸 결정이다. 분산 DB를 처음 도입하는 팀이라면 한 번 읽어볼 가치가 있다.

Citus의 가장 큰 미덕은 "PostgreSQL이 PostgreSQL인 상태로" 분산이 된다는 점이다. 마이그레이션 비용이 ClickHouse나 Cassandra로 가는 결정과는 비교가 안 된다. 그리고 분산 키를 잘 골랐다면 — 그게 잘 골라진다면 — 단일 노드 PostgreSQL의 한계를 한참 미룰 수 있다.

## 15.3 TimescaleDB — 시계열이라는 워크로드의 정답

시계열 데이터는 모양이 단순하다. 시간 컬럼이 있고, 그 시간을 따라 측정값들이 쌓인다. 메트릭, 로그, 이벤트, 센서 — 다 같은 모양이다. 그런데 단순한 모양이 거대해지면 운영이 어려워진다. 1년치 데이터를 인덱스 하나로 묶으면 인덱스가 RAM에 안 들어가고, 한 테이블에 쌓아두면 VACUUM이 끝나지 않고, 오래된 데이터를 지우려면 DELETE가 며칠 걸린다. 시계열 데이터의 운영에서 자주 듣는 한숨들이다.

TimescaleDB는 이 풍경의 정공법이다. PostgreSQL 익스텐션으로 동작하면서, 시간 기반 자동 파티셔닝(hypertable), 점진적 집계(continuous aggregate), 압축된 컬럼 스토어(native columnstore)를 한 묶음으로 제공한다.

### Hypertable — 자동으로 시간 파티션을 자른다

PostgreSQL에는 declarative partitioning이 이미 있다. 그러면 왜 TimescaleDB가 필요할까? 답은 "운영의 결"에 있다. 순정 파티셔닝은 우리가 직접 파티션을 만들어야 한다. 매월 새 파티션을 생성하는 cron job을 짜고, 오래된 파티션을 detach하는 로직을 따로 관리해야 한다. pg_partman이 그 일을 자동화해 주긴 한다.

TimescaleDB의 hypertable은 한 단계 더 간다. 테이블을 만들고 한 줄 추가하면, 시간이 흐를수록 자동으로 chunk(파티션의 다른 이름)가 만들어진다.

```sql
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id TEXT NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    cpu_pct DOUBLE PRECISION
);

SELECT create_hypertable('metrics', 'time', chunk_time_interval => INTERVAL '1 day');
```

이제 매일 자동으로 새 chunk가 만들어진다. 쿼리에 `WHERE time BETWEEN ...` 조건을 넣으면 해당 시간에 걸치는 chunk만 스캔한다(chunk pruning). 인덱스도 chunk별로 관리되니, 1년치 데이터가 쌓여도 단일 인덱스가 비대해지지 않는다. 오래된 데이터를 지울 때도 `DROP TABLE`처럼 빠르다 — chunk 자체를 통째로 drop하기 때문이다.

`chunk_time_interval`은 데이터 양에 맞춰 조정한다. 인덱스 하나가 RAM에 들어가는 크기가 되도록 잡는 게 정석이다. 일 단위로 1억 행이 들어오면 1일 chunk가 적당하고, 시 단위로 1억 행이라면 1시간 chunk를 쓴다.

### Continuous Aggregate — 미리 집계해 두는 진짜 머티리얼라이즈드 뷰

15.1에서 PostgreSQL 머티리얼라이즈드 뷰의 한계를 짚었다. 증분 갱신을 지원하지 않는다는 것. 시계열 워크로드에서는 이게 치명적이다. 10억 행이 쌓인 메트릭 테이블에서 매시간 풀 리프레시를 돌릴 수는 없다.

TimescaleDB의 continuous aggregate는 이걸 정면으로 푼다.

```sql
CREATE MATERIALIZED VIEW metrics_1h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    device_id,
    AVG(temperature) AS avg_temp,
    MAX(temperature) AS max_temp,
    MIN(temperature) AS min_temp,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS sample_count
FROM metrics
GROUP BY bucket, device_id;

SELECT add_continuous_aggregate_policy('metrics_1h',
    start_offset => INTERVAL '3 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
```

`time_bucket`이 핵심 함수다. 시간을 균등 간격(1시간, 5분, 1일 등)으로 자른 뒤 그 안에서 집계한다. 그 결과를 continuous aggregate라는 특별한 뷰에 저장한다.

여기서 진짜 차이가 나온다. TimescaleDB는 어떤 chunk가 변경됐는지를 추적하다가, 정책에 따라 **변경된 부분만** 다시 계산한다. 10억 행 중 어제 들어온 1억 행만 갱신되면, 그 1억 행에 해당하는 시간 bucket만 다시 계산한다. 풀 리프레시가 아니다. 운영 비용이 데이터 양에 비례하는 게 아니라 변경량에 비례한다는 뜻이다.

그리고 실시간 보정도 자동으로 된다. 가장 최근 1시간(`end_offset` 이내)의 데이터는 아직 집계 뷰에 들어가지 않았지만, 쿼리할 때 즉석에서 원본 hypertable과 합쳐서 보여준다. 사용자는 "거의 실시간 + 과거 미리 집계"의 매끄러운 뷰를 본다.

### Native Columnstore — TimescaleDB 2.22의 큰 변화

오래된 시계열 데이터는 보통 분석에만 쓰이고 수정되지 않는다. 그러면 행 기반 저장은 낭비다. 컬럼 단위로 압축하고 컬럼 단위로 스캔하면, 같은 데이터를 1/10, 1/20 크기로 들고 있을 수 있고 집계 쿼리도 훨씬 빠르다.

TimescaleDB는 이 자리에 한동안 "Hypercore TAM(Table Access Method)"이라는 하이브리드 엔진을 두고 행 영역과 압축 영역을 함께 운영했다. 그런데 2025년 9월, 버전 2.22에서 Hypercore TAM이 sunset됐다. 2.21에서 Hypercore가 폐기되고, 2.22부터는 **native columnstore**로 통일됐다. 한동안 두 엔진을 같이 관리해야 했던 운영의 결이 한층 단순해졌다.

```sql
ALTER TABLE metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'device_id',
    timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('metrics', INTERVAL '7 days');
```

7일 이상 된 chunk는 자동으로 컬럼 압축된다. `segmentby`는 같은 디바이스의 데이터끼리 묶고, `orderby`는 그 안에서 시간 역순으로 정렬한다. 시계열 데이터의 특성상 같은 디바이스의 연속 측정값은 비슷한 값이 많으니, 압축률이 5~20배까지 나온다.

압축된 chunk도 SELECT는 그대로 된다. 쿼리 옵티마이저가 컬럼 영역과 행 영역을 합쳐서 실행 계획을 짠다. 압축된 chunk에 INSERT를 하려면 약간의 추가 비용이 들지만(decompress 후 다시 compress), 시계열 워크로드는 거의 append-only이니 실무에서는 잘 안 부딪힌다.

### 데이터 보관 정책 — 오래된 chunk를 자동으로 처리

시계열 데이터의 운영에서 또 하나 중요한 결정이 "오래된 데이터를 언제까지 들고 있을 것인가"다. 무한정 쌓아두면 디스크가 폭발하고, 너무 빨리 지우면 분석 가치를 잃는다. TimescaleDB는 이 결정을 정책으로 표현하게 해 준다.

```sql
-- 90일 이상 된 chunk는 자동 삭제
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- 30일 이상 된 chunk는 자동 압축
SELECT add_compression_policy('metrics', INTERVAL '30 days');
```

이 두 줄을 같이 걸면 운영 패턴이 자연스럽게 만들어진다. 최근 30일은 행 기반으로 빠르게 INSERT를 받고, 30~90일은 컬럼으로 압축해 디스크를 아끼며 분석에 쓰고, 90일이 지난 chunk는 통째로 drop된다. 한 번 걸어두면 사람이 손댈 일이 거의 없다.

Cloudflare가 자사 블로그에서 공유한 TimescaleDB 운영기가 이 패턴을 잘 보여준다. 트래픽 분석 워크로드를 TimescaleDB에 담고, 압축으로 90% 이상의 디스크를 절약하며, 보관 정책으로 운영 부담을 일정하게 유지한다. "시계열 데이터를 PostgreSQL에 담을 수 있는가"라는 질문에 한 회사가 production 규모로 답한 사례다.

### TimescaleDB의 자리 — Citus와 무엇이 다른가

Citus가 "OLTP 쪽 분산"이라면, TimescaleDB는 "시계열 쪽 수직 최적화"다. 둘 다 익스텐션이지만 결이 다르다.

- TimescaleDB는 **단일 노드**에서도 큰 효과를 낸다. 분산 클러스터 운영의 복잡도 없이, 시계열 워크로드의 운영 비용을 한 자릿수 배수로 떨어뜨린다.
- Citus는 **분산**이 필요한 시점부터 효과를 낸다. 단일 노드의 한계 — 디스크, CPU, 메모리 — 를 넘기 위한 도구다.

시계열 데이터가 단일 노드에 들어가는 한, TimescaleDB가 먼저 답이다. 단일 노드의 한계를 넘으면 Citus와 TimescaleDB를 합치는 방안도 있다 — 코어 Citus 위에 TimescaleDB를 얹는 패턴은 공식적으로 지원되지는 않지만 일부 시도가 있다. 다만 운영의 복잡도가 급격히 늘어나니, 그 단계까지 가기 전에 데이터 보존 기간을 줄이거나 cold data를 S3로 빼는 게 보통은 답이다.

## 15.4 Hydra — Citus columnar를 OLAP에 맞춰 갈아 만든 fork

여기서 흥미로운 분기가 하나 등장한다. Citus는 분산을 위한 익스텐션이지만, 그 안에는 컬럼 스토어 기능도 들어 있었다. 그런데 Microsoft가 Citus를 인수한 뒤로 컬럼 부분은 상대적으로 우선순위가 낮아졌다. 분산 쪽에 집중한 결과다.

이 자리에 Hydra가 들어왔다. Hydra는 Citus의 columnar 코드를 fork해서, OLAP 워크로드에 특화된 PostgreSQL 익스텐션으로 갈아 만들었다. ClickBench 같은 분석 벤치마크에서 순수 PostgreSQL이 ClickHouse 대비 1050배 느리다는 결과가 나오는 자리 — 그 격차를 좁히는 게 Hydra의 목표다. 결과적으로 PostgreSQL 진영의 분석 익스텐션 중 ClickBench 상위권에 자주 이름을 올린다.

### 컬럼 스토어가 왜 OLAP에서 빠른가

행 기반 저장은 "한 행의 모든 컬럼을 함께 디스크에 적는다". 컬럼 기반은 "한 컬럼의 모든 행을 함께 디스크에 적는다". OLTP에서는 한 행을 통째로 가져오는 일이 흔하니 행 저장이 낫다. OLAP에서는 한 컬럼을 통째로 집계하는 일이 흔하니 컬럼 저장이 낫다. 그래서 같은 데이터를 두 가지 모양으로 쥐고 있는 시스템이 가장 강하다.

컬럼 스토어의 장점은 세 가지다.

- **IO 절감** — `SELECT AVG(amount) FROM orders`를 돌릴 때 행 저장은 모든 컬럼을 읽어야 한다(`amount` 외의 컬럼도 같은 페이지에 있으니까). 컬럼 저장은 `amount` 컬럼만 읽는다. 디스크 IO가 컬럼 수만큼 줄어든다.
- **압축률** — 같은 컬럼 안의 값들은 분포가 비슷하다. dictionary encoding, RLE, delta encoding 같은 컬럼 단위 압축이 효과가 크다. 행 저장 대비 5~50배 압축이 흔하다.
- **벡터화 실행** — 한 컬럼의 값들이 메모리에 연속으로 놓이니, SIMD 명령어로 한 번에 여러 값을 처리할 수 있다. CPU 사이클 효율이 한참 올라간다.

### Hydra의 사용법

```sql
CREATE EXTENSION hydra;

CREATE TABLE orders_columnar (
    order_id BIGINT,
    customer_id BIGINT,
    product_id INT,
    amount NUMERIC,
    created_at TIMESTAMPTZ
) USING columnar;
```

`USING columnar`가 키 포인트다. PostgreSQL의 table access method API를 통해 컬럼 스토어를 그대로 PostgreSQL 안에 박아넣는다. 일반 SQL이 그대로 통한다. 인덱스, 트랜잭션, 트리거, FDW — 다 평소처럼 쓴다. 다만 INSERT는 batch가 효율적이고, UPDATE/DELETE는 비싸다. OLAP 워크로드에 맞는 패턴이다.

Hydra의 진짜 가치는 **PostgreSQL의 다른 모든 것과 그대로 같이 쓸 수 있다**는 점에서 나온다. JSONB 컬럼을 컬럼 스토어 테이블에 넣을 수 있고, GIN 인덱스도 같이 걸 수 있다. 행 기반 테이블과 컬럼 기반 테이블을 같은 트랜잭션에서 조인할 수도 있다. ClickHouse를 따로 세웠을 때는 못하는 일들이다.

### Hydra가 안 맞는 자리

물론 만능은 아니다. Hydra가 강한 자리는 "한 번 쓰고 자주 읽는 큰 테이블"이다. 잦은 UPDATE, 짧은 트랜잭션, 단일 행 조회가 많은 워크로드에서는 행 저장이 여전히 낫다. 그리고 ClickHouse만큼 압도적으로 빠르지도 않다(ClickBench에서 ClickHouse 대비 약 3~4배 느린 정도). 다만 운영 단순성과 트랜잭션 일관성을 같이 따지면, PostgreSQL 한 클러스터로 가는 게 더 합리적인 경우가 많다.

Hydra는 "ClickHouse가 필요할까? 아닐 수도 있다"는 질문에 PostgreSQL 진영이 내놓는 답 중 하나다. 시도해 보고 ClickBench 식의 워크로드에서 자기 워크로드가 어디 위치하는지 한 번 측정해 보는 게 좋다.

## 15.5 AlloyDB columnar engine — Google이 만든 자동 row↔column 변환

같은 문제를 Google이 다른 각도에서 푼다. AlloyDB는 Google Cloud의 매니지드 PostgreSQL이다. PostgreSQL과 wire-compatible하고 SQL은 같은데, 내부에는 disaggregated storage와 columnar engine이 들어 있다. 그중에서도 OLAP 측면에서 가장 도드라지는 부품이 columnar engine이다.

### "자동"이라는 차별점

Hydra가 "테이블을 만들 때 컬럼 저장이라고 명시하라"는 모델이라면, AlloyDB의 columnar engine은 "메모리에 column 사본을 자동으로 만든다"는 모델이다.

AlloyDB의 columnar engine은 별도의 컬럼 인메모리 캐시를 운영한다. 자주 분석 쿼리가 가는 테이블·컬럼을 ML 기반 추천으로 골라내고, 그 부분을 컬럼 형식으로 메모리에 복제한다. 원본 테이블은 그대로 행 기반 저장이다. OLTP 쿼리는 원본을 보고, OLAP 쿼리는 컬럼 캐시를 본다. 둘 다 같은 트랜잭션 안에서 일관성이 유지된다.

```sql
SELECT google_columnar_engine_recommend();
```

위 함수를 호출하면 워크로드를 분석해서 "이 컬럼들을 컬럼 캐시에 올리면 좋겠다"는 추천이 나온다. 그 추천을 받아들이거나 직접 지정한다.

```sql
SELECT google_columnar_engine_add(
    relation => 'orders',
    columns  => 'amount,created_at,category'
);
```

Google의 마케팅 수치로는 분석 쿼리 최대 100배 가속이라고 한다. 실측에서는 워크로드에 따라 다르지만, 분석 쿼리가 워크로드의 일부인 환경에서 30~50배는 어렵지 않게 나온다는 보고가 흔하다.

### AlloyDB의 자리 — 매니지드 HTAP

AlloyDB의 진짜 가치는 columnar engine 자체보다 **HTAP를 매니지드로 받을 수 있다**는 운영의 결에서 나온다.

- PostgreSQL 호환성이 유지된다. 익스텐션은 일부 제약이 있지만 PostGIS·pgvector·pg_stat_statements 같은 핵심은 다 된다.
- 백업·HA·페일오버는 Google이 매니지드로 처리한다.
- columnar engine 추천과 운영은 SQL 함수 호출 몇 개로 끝난다.

물론 비용 모델이 다르다. Cloud SQL Enterprise Plus 대비 +39% 정도라고 보고된다. 자체 운영 PostgreSQL과 비교하면 한참 비싸다. 그래서 의사결정은 단순하다 — "OLTP에 OLAP가 섞여 있고, 두 워크로드를 분리하지 않고 매니지드로 받고 싶다"면 AlloyDB가 답이다. 그게 아니라면 RDS PostgreSQL + 컬럼 익스텐션 조합이 비용 면에서 낫다.

### AlloyDB Omni — 자체 호스팅 옵션

Google은 AlloyDB의 코어 엔진을 별도 바이너리로 묶은 AlloyDB Omni도 제공한다. 자체 서버에서 돌리거나 다른 클라우드에서 돌릴 수 있다. columnar engine과 PostgreSQL 호환성을 lock-in 없이 가져갈 수 있는 옵션이다. 매니지드는 아니지만 GCP에 묶이지 않아도 된다는 점에서 일부 회사들에 매력적이다.

## 15.6 pg_duckdb·pg_analytics — DuckDB 엔진을 PostgreSQL 안에서

여기까지는 PostgreSQL을 안에서 키우는 길이었다. 마지막으로 살펴볼 길은 다르다. 다른 분석 엔진을 PostgreSQL 안으로 끌어들이는 길이다.

DuckDB가 들어온다. DuckDB는 "분석을 위한 SQLite"라는 별명으로 불리는 임베디드 OLAP DB다. 단일 파일, 단일 프로세스, 벡터화 실행, 컬럼 저장. ClickBench에서 ClickHouse와 어깨를 나란히 하는 수준으로 빠르다. 그리고 그 엔진을 PostgreSQL 안에 통째로 박아넣는 익스텐션이 두 개 있다.

### pg_duckdb — MotherDuck과 DuckDB Labs의 공식 작품

pg_duckdb는 DuckDB Labs와 MotherDuck이 공동 개발한 PostgreSQL 익스텐션이다. 2025년 5월에 1.0이 나왔다. PostgreSQL 안에서 DuckDB 엔진으로 쿼리를 실행할 수 있게 만든다.

```sql
CREATE EXTENSION pg_duckdb;

-- PostgreSQL 테이블을 DuckDB 엔진으로 쿼리
SET duckdb.force_execution = true;
SELECT category, SUM(amount), COUNT(*)
FROM orders
WHERE created_at >= '2026-01-01'
GROUP BY category
ORDER BY 2 DESC;
```

위 쿼리는 일반 PostgreSQL 테이블 `orders`를 대상으로 하지만, 실행은 DuckDB 엔진이 한다. 벡터화 실행과 병렬 처리가 들어가니, 같은 쿼리가 순정 PostgreSQL 대비 한 자릿수~두 자릿수 배 빨라진다.

pg_duckdb의 진짜 매력은 **외부 데이터를 PostgreSQL SQL로 쿼리할 수 있다**는 점이다.

```sql
-- S3의 Parquet 파일을 직접 쿼리
SELECT date_trunc('day', event_time) AS day,
       count(*) AS events
FROM read_parquet('s3://my-bucket/events/2026/*.parquet')
GROUP BY 1
ORDER BY 1;

-- Iceberg 테이블 쿼리
SELECT *
FROM iceberg_scan('s3://my-warehouse/orders');

-- PostgreSQL 테이블과 Parquet 파일을 조인
SELECT u.email, e.event_type, e.event_time
FROM users u
JOIN read_parquet('s3://logs/events.parquet') e ON e.user_id = u.id
WHERE e.event_time >= NOW() - INTERVAL '1 day';
```

PostgreSQL 안에 있는 트랜잭션 데이터와, S3에 쌓인 분석 데이터를 한 쿼리에서 조인할 수 있다는 뜻이다. Parquet, Iceberg, Delta Lake — Lakehouse 진영의 포맷들이 다 통한다. ETL 파이프라인을 따로 짜지 않고, "DB 위에 데이터 레이크가 같이 보이는" 풍경을 만든다.

TPC-DS의 한 쿼리에서는 pg_duckdb가 순정 PostgreSQL 대비 1500배 빨라졌다는 보고도 있다. 모든 쿼리가 그 정도는 아니지만, 분석 워크로드의 상당수가 두 자릿수~세 자릿수 배 가속을 받는다.

### pg_analytics(ParadeDB) — Lakehouse 통합에 집중한 길

ParadeDB 진영이 만든 pg_analytics도 비슷한 발상이다. DuckDB 엔진과 Lakehouse 포맷을 PostgreSQL에 끌어들이지만, 강조점이 다르다. pg_analytics는 분석 워크로드의 가속과 외부 테이블 쿼리에 집중하고, 특히 S3·MinIO 같은 object storage 위의 Parquet·Iceberg를 1급 시민으로 다룬다.

```sql
CREATE EXTENSION pg_analytics;

CREATE FOREIGN TABLE clicks ()
    SERVER analytics_server
    OPTIONS (files 's3://logs/clicks/*.parquet', format 'parquet');

SELECT date_trunc('hour', event_time) AS hour, count(*)
FROM clicks
WHERE event_time >= '2026-05-01'
GROUP BY 1
ORDER BY 1;
```

ClickBench에서 ParadeDB의 pg_analytics는 ClickHouse 대비 약 10배 느린 자리에 있다. 순정 PostgreSQL의 1050배에 비하면 격차가 100배 줄어든 셈이다. PostgreSQL 한 클러스터로 분석 워크로드의 80~90%를 처리하는 게 가능해진다.

### MotherDuck 연동 — 로컬 PostgreSQL이 클라우드 DuckDB에 닿는다

pg_duckdb의 또 하나 흥미로운 길은 MotherDuck 클라우드와의 연동이다. MotherDuck은 DuckDB 진영이 만든 매니지드 클라우드 분석 서비스다. pg_duckdb를 깐 PostgreSQL에서 MotherDuck의 데이터셋을 직접 쿼리할 수 있다.

```sql
-- MotherDuck 토큰 등록
SELECT duckdb.create_secret('motherduck', '...');

-- MotherDuck 데이터셋을 PostgreSQL에서 직접 쿼리
SELECT category, sum(amount)
FROM duckdb_query('SELECT * FROM md:analytics.orders')
GROUP BY category;
```

로컬 OLTP PostgreSQL + 클라우드 OLAP MotherDuck이라는 하이브리드 구성이 가능해진다. 분석 데이터는 클라우드 컬럼 스토어에 두고, 트랜잭션 데이터는 자체 PostgreSQL에 두면서, 둘을 한 SQL 인터페이스로 합친다. 데이터 레이크 시대에 어울리는 구성이다.

### pg_duckdb의 한계와 함정

pg_duckdb가 만능은 아니다. 도입 전에 알아둘 한계도 있다.

- **트랜잭션 격리** — pg_duckdb로 실행되는 쿼리는 PostgreSQL의 MVCC와 완전히 같은 일관성을 제공하지는 않는다. 실행 중에 다른 트랜잭션의 변경이 보일 수 있다. OLAP 워크로드에서는 보통 문제가 안 되지만, 결제 같은 엄격한 일관성이 필요한 쿼리는 pg_duckdb로 돌리지 않는 게 좋다.
- **메모리 사용량** — DuckDB는 분석 쿼리를 빠르게 만들기 위해 메모리를 적극 사용한다. 큰 집계 쿼리를 돌리면 PostgreSQL 서버의 RAM이 갑자기 압박을 받을 수 있다. `duckdb.memory_limit` 설정으로 상한을 두는 게 좋다.
- **함수 호환성** — PostgreSQL의 모든 함수가 DuckDB로 통하는 건 아니다. 일부 함수는 DuckDB에 동등한 게 없어서 fallback이 일어나거나 실패한다. `duckdb.force_execution = true`로 강제하기 전에, 워크로드의 주요 쿼리를 미리 테스트하자.
- **버전이 빠르게 움직인다** — pg_duckdb는 1.0이 2025년에 나온 비교적 새 익스텐션이다. API가 바뀌거나 동작이 바뀔 가능성이 있다. production에 적용할 때는 버전 고정과 회귀 테스트가 필수다.

이런 한계들에도 불구하고 pg_duckdb의 가속 폭은 매력적이다. 자기 워크로드의 분석 쿼리를 가져다 한 번 측정해 보자. 두 자릿수 배 이상 빨라진다면, 운영 복잡도를 늘리고 도입할 만하다.

### pg_duckdb와 pg_analytics — 어떤 걸 고를까

두 익스텐션이 겹치는 영역이 크다. 정리하자면 이렇다.

- **트랜잭션 데이터에 분석 가속을 얹고 싶다면 pg_duckdb** — PostgreSQL 테이블 자체에 DuckDB 엔진을 적용하는 사용법이 매끄럽다.
- **데이터 레이크를 PostgreSQL 인터페이스로 노출하고 싶다면 pg_analytics** — Iceberg·Parquet·MinIO 통합과 LSP·BI 친화 기능이 더 두텁다.
- **둘 다 보고 정하자** — 둘 다 비교적 새 익스텐션이라 자기 워크로드에서 직접 측정해 보는 게 가장 빠른 답이다.

공통점이 하나 있다. 둘 다 "PostgreSQL을 떠나지 않고도 ClickHouse급 분석 성능에 가깝게 가는 길"을 연다는 것이다. 운영의 단순성과 트랜잭션 일관성을 같이 가져갈 수 있다는 게 결정적인 매력이다.

## 15.7 ClickBench와 그 해석 — 익스텐션 composability가 진짜 moat

여기까지 다섯 가지 익스텐션 군을 봤다. 이제 숫자 한 장을 같이 보자. Pigsty가 정리한 ClickBench 비교다.

| 솔루션 | ClickHouse 대비 상대 속도 |
|--------|--------------------------|
| 순수 PostgreSQL | x1050 (1050배 느림) |
| 튜닝된 PostgreSQL | x47 |
| ParadeDB(pg_analytics) | x10 |
| ClickHouse·DuckDB | x3~4 |
| MySQL·MariaDB | x3000~19700 |

여러 가지가 보인다. 하나씩 짚어보자.

### 숫자가 말하는 것

먼저 순수 PostgreSQL은 ClickHouse 대비 1050배 느리다. 1000배가 넘는 격차다. "PostgreSQL로 OLAP 다 된다"는 단순한 주장이 실측에서는 흔들리는 자리가 여기다. 인덱스도 안 갈고, 파티션도 안 한, 그냥 깡통 PostgreSQL은 ClickBench 같은 컬럼 분석 워크로드에서 ClickHouse를 절대 따라잡지 못한다.

다음으로 튜닝된 PostgreSQL은 47배다. 인덱스를 정성스럽게 깔고, 파티션을 자르고, 메모리 파라미터를 조정한 결과다. 1050배에서 47배로 줄었으니 22배 개선이다. 노력에 보답하는 격차다. 그런데 여전히 ClickHouse가 47배 빠르다.

ParadeDB의 pg_analytics를 깔면 10배까지 좁혀진다. DuckDB 엔진과 Lakehouse 포맷이 들어온 결과다. 47배에서 10배는 약 5배 개선이다.

ClickHouse와 DuckDB는 x3~4. 두 컬럼 분석 엔진은 비슷한 자리에 있다. 그리고 마지막으로 MySQL/MariaDB는 x3000~19700. 분석 워크로드에서는 MySQL이 PostgreSQL의 한참 뒤에 있다는 비교 기준점이 같이 잡힌다.

### 숫자를 해석하는 두 관점

이 숫자를 두고 두 관점이 부딪힌다.

**관점 A — "순수 컬럼 분석은 ClickHouse가 빠르다. PostgreSQL은 그쪽을 따라잡지 못한다."**

맞는 말이다. 분석만 한다면, 그것도 컬럼 단위 집계를 수십억 행에 돌린다면, ClickHouse 같은 dedicated OLAP DB가 항상 빠르다. 벤치마크 숫자가 일관되게 말해준다.

**관점 B — "OLTP + OLAP 혼합과 운영 단순성이라면 PostgreSQL이 압도. ClickHouse를 별도 운영하지 않아도 80% 케이스 해결."**

이쪽도 맞는 말이다. 그리고 더 정직한 말일 수 있다. 실제 서비스의 분석 워크로드 대부분은 ClickBench가 측정하는 극단적인 컬럼 집계가 아니다. 일별·시간별 대시보드, 코호트 분석, 간단한 BI 쿼리 — 이 정도는 튜닝된 PostgreSQL + pg_analytics면 충분히 빠르다. 그리고 별도 ETL 파이프라인이 없고, 데이터가 분 단위로 최신이고, 같은 트랜잭션 안에서 일관성이 유지된다는 운영의 결을 같이 얻는다.

### 진짜 moat는 composability에 있다

이 두 관점이 만나는 공통 합의가 하나 있다. PostgreSQL 진영이 가진 진짜 무기는 **익스텐션 composability**라는 것이다. 한 엔진의 성능 절대치가 아니라, 여러 익스텐션을 한 클러스터에서 조합할 수 있다는 사실이 moat다.

같은 PostgreSQL 클러스터 한 대 위에 다음을 모두 얹을 수 있다.

- 결제 트랜잭션을 처리하는 OLTP 워크로드(순정 PostgreSQL)
- 멀티테넌트 분산(Citus)
- 시계열 메트릭(TimescaleDB)
- 분석 쿼리 가속(pg_duckdb 또는 Hydra)
- 벡터 검색(pgvector, 12장)
- 전문 검색(PGroonga 또는 pg_search, 10장)
- 공간 데이터(PostGIS, 11장)
- API 자동 노출(PostgREST, 16장)

ClickHouse가 OLAP에서 PostgreSQL보다 빠른 건 사실이다. 그런데 ClickHouse 위에 pgvector를 얹을 수 있는가? PostGIS를 얹을 수 있는가? RLS 멀티테넌트 정책을 같은 클러스터에서 적용할 수 있는가? 답은 모두 "아니다"다. 한 시스템에서 OLTP·OLAP·검색·벡터·공간·실시간을 모두 합치는 능력은 PostgreSQL 진영에만 있다.

이 합산 가치가 ClickBench의 한 숫자보다 훨씬 크다. 그리고 그게 2026년의 PostgreSQL이 "메인 DB"로 점점 더 많이 선택되는 진짜 이유다.

### 의사결정 매트릭스 — 우리 시스템은 어디에 있는가

자기 시스템에 어떤 익스텐션 조합이 맞는지를 정리해 보자. 다음 표를 작은 의사결정 가이드로 들고 다닐 만하다.

| 워크로드 모양 | 첫 번째 선택 | 두 번째 선택 |
|--------------|------------|------------|
| 단일 노드, 수억 행 이하 분석 | 순정 PostgreSQL + 윈도우/MV | pg_duckdb |
| 멀티테넌트 SaaS, 노드 확장 필요 | Citus | AlloyDB |
| 시계열 메트릭/로그/이벤트 | TimescaleDB | Citus + TimescaleDB(고급) |
| 컬럼 분석 가속, 자체 운영 | Hydra | pg_analytics |
| 컬럼 분석 가속, 매니지드 | AlloyDB | RDS + pg_duckdb |
| Lakehouse(S3/Parquet/Iceberg) 통합 | pg_analytics | pg_duckdb |
| OLTP + OLAP 한 클러스터, 비용 최소 | RDS PostgreSQL + pg_duckdb | TimescaleDB(시계열일 때) |
| OLTP + OLAP 한 클러스터, 운영 최소 | AlloyDB | Hydra on RDS |

이 표를 절대 기준으로 받지 말자. 실제 답은 자기 워크로드를 갖고 직접 측정해 봐야 나온다. 다만 출발점으로는 쓸 만하다.

### 한국 현장에서 어떻게 쓰이고 있는가

한국 회사들도 비슷한 결정을 내리고 있다. 25장에서 자세히 다룰 사례들의 미리보기를 짧게 적어두자.

- 당근페이의 BroQuery는 데이터 분석 자가서비스 시스템이다. 자연어 질문을 SQL로 바꿔 PostgreSQL에 던지고, 분석 결과를 직원이 직접 받는다. 분석 워크로드를 PostgreSQL 한 클러스터에 집중시킨 결정이다. 별도 OLAP DB를 세우지 않고도 회사의 분석 수요를 받아내는 모델이다.
- 카카오스타일은 Amazon Bedrock과 PostgreSQL을 묶어서 RAG 시스템을 만든다. 벡터(pgvector)와 분석(SQL)이 한 DB 안에 있어서, LLM이 데이터를 끌어쓸 때 단일 인터페이스로 끝난다.

두 사례의 공통점은 "분석 전용 DB를 따로 세우지 않았다"는 것이다. PostgreSQL의 익스텐션 composability를 신뢰한 결과다. 그리고 그 신뢰가 깨지지 않았다.

### 그래서 어떻게 시작할까 — 단계적 도입 가이드

이론과 카탈로그를 다 봤으니, 마지막으로 실천의 결을 같이 정리해 보자. "내일 출근해서 무엇부터 해 볼 것인가"의 답을 찾기 위한 단계다.

**1단계 — 기본기부터.** 익스텐션을 깔기 전에, 자기 시스템에서 윈도우 함수·CUBE·머티리얼라이즈드 뷰가 얼마나 활용되고 있는지부터 점검한다. 분석 쿼리 절반은 사실 표준 SQL의 무기들을 제대로 쓰지 않아서 느린 경우가 많다. `pg_stat_statements`에서 가장 느린 분석 쿼리 10개를 뽑고, 그중 몇 개가 윈도우/MV로 풀리는지 본다. 풀리는 게 절반이면, 익스텐션을 깔기 전에 그것부터 챙긴다.

**2단계 — 정확한 통증을 진단한다.** 익스텐션은 통증에 따라 다른 답이다. 자기 시스템의 통증을 다음 네 카테고리로 분류해 보자.

- **데이터가 많아서 느리다** (단일 노드 한계) → Citus 또는 AlloyDB
- **시간 컬럼이 핵심인데 운영이 무겁다** → TimescaleDB
- **분석 쿼리가 OLTP 옆에서 느리다** → Hydra 또는 pg_duckdb
- **외부 데이터 레이크와 연결해야 한다** → pg_analytics 또는 pg_duckdb

자기 통증이 어디인지 정직하게 답하지 않으면, 익스텐션을 잘못 골라서 운영만 복잡해진다.

**3단계 — 한 익스텐션부터 작게 시도한다.** 한꺼번에 여러 익스텐션을 깔지 말자. 가장 큰 통증 하나에 해당하는 익스텐션 하나만 골라서, dev/staging에서 충분히 측정한다. 자기 워크로드의 핵심 쿼리 10~20개를 가져다, 익스텐션 적용 전후의 응답시간을 비교한다. 두 자릿수 배 이상 개선되면 production 도입을 고민한다. 한 자릿수 배 정도면 운영 복잡도와 견줘서 결정한다.

**4단계 — 운영 자산을 같이 갖춘다.** 익스텐션을 production에 깔면 모니터링이 같이 따라가야 한다. Citus라면 노드별 디스크·CPU·쿼리 분포. TimescaleDB라면 chunk 크기·압축률·continuous aggregate 지연. pg_duckdb라면 DuckDB 메모리 사용량과 fallback 빈도. 익스텐션마다 자기만의 가시성 지점이 있다. Grafana 대시보드에 그 지표를 같이 띄워두지 않으면, 어느 날 갑자기 무너졌을 때 원인을 찾기까지 한참 헤매게 된다. 끔찍한 일이다.

**5단계 — 정기적인 재평가.** 익스텐션 생태계는 빠르게 움직인다. TimescaleDB의 Hypercore가 1년 만에 sunset된 것처럼, 작년의 최적해가 올해는 다른 답일 수 있다. 분기에 한 번 정도는 자기 클러스터의 익스텐션 구성을 재평가하는 시간을 갖자. 새 버전이 나왔는지, 더 가벼운 대안이 등장했는지, 기존 익스텐션이 EOL을 향해 가는지를 점검한다.

이 다섯 단계를 충실히 밟으면, 익스텐션 한 겹씩의 도입이 운영의 복잡도가 아니라 능력의 확장으로 이어진다. 그게 PostgreSQL을 "그냥 DB"가 아니라 "메인 DB"로 쓰는 풍경이다.

## 마무리 — 한 쪽으로 합칠 수 있는 길

긴 길을 걸었다. 윈도우 함수의 기본기에서 시작해서, Citus의 분산과 TimescaleDB의 시계열 최적화를 지나, Hydra와 AlloyDB의 컬럼 엔진을 거쳐, pg_duckdb의 DuckDB 통합까지. 어디까지 PostgreSQL 한 쪽으로 합칠 수 있는지가 윤곽으로 잡혔을 것이다.

기억해 두자. "PostgreSQL은 OLAP가 느리다"는 명제는 절반만 참이다. **순정 PostgreSQL은 ClickHouse만큼 빠르지 않다.** 그러나 익스텐션 한 겹을 얹는 순간 격차가 두 자릿수 배로 줄어들고, 두 겹을 얹으면 한 자릿수 배까지 좁아진다. 그리고 이 격차를 좁히는 동안 우리는 트랜잭션 일관성, 운영 단순성, 단일 SQL 인터페이스, 멀티테넌트 정책, 벡터·공간·검색 같은 다른 모든 능력을 잃지 않는다.

분석은 빠른 DB로, 운영은 정확한 DB로 — 그렇게 둘로 갈라야 한다고 누가 정했을까. 2026년의 PostgreSQL은 그 결정을 다시 묻게 한다. 한 쪽으로 합칠 수 있는 길이 여러 갈래로 열려 있고, 그 길은 점점 더 넓어지고 있다. 5년 전이라면 "PostgreSQL로 OLAP까지 하자"는 제안에 데이터 엔지니어 절반이 손사래를 쳤을 것이다. 그런데 2026년에는 같은 제안에 "어느 익스텐션 조합으로?"라는 질문이 먼저 돌아온다. 풍경이 바뀌었다.

다만 한 가지 당부할 게 있다. 익스텐션을 무조건 많이 깔수록 좋은 것은 아니다. 익스텐션이 하나 늘 때마다 운영의 표면적도 함께 늘어난다. 자기 워크로드에 진짜로 필요한 익스텐션만 골라 쓰는 결정이 가장 어렵고, 가장 중요하다. ClickBench의 숫자 한 장은 참고일 뿐, 자기 시스템의 답은 자기 워크로드에서 직접 측정해야 나온다. 누군가의 벤치마크에서 100배 가속이 났다고 해서 우리 시스템에서도 같은 숫자가 나오는 건 아니다. 자기 데이터, 자기 쿼리, 자기 인프라에서 측정한 숫자만이 진짜 의사결정의 근거가 된다.

또 하나 — 익스텐션은 "한 번 깔면 영원히 쓴다"는 자세로 도입하지 말자. TimescaleDB의 Hypercore가 1년 만에 sunset된 사례를 잊지 말자. 익스텐션 생태계는 살아 움직이고, 어제의 최선이 오늘의 함정일 수 있다. 도입한 익스텐션의 release note를 분기마다 한 번씩 챙기고, EOL 신호가 보이면 마이그레이션 계획을 미리 세우는 운영의 결을 갖추자. 그게 익스텐션 composability를 안전하게 누리는 방식이다.

마지막으로, "PostgreSQL로 모든 걸 하자"는 단순화에 너무 빨리 빠지지도 말자. 하루 100MB/s가 흘러가는 메시지 버스, 1초에 100만 행이 들어오는 컬럼 분석, 검색 품질이 BM25 수준을 넘어 학습된 ranking이 필요한 워크로드 — 이런 자리에는 여전히 dedicated 도구가 더 좋은 답이다. PostgreSQL의 강점은 "80%를 한 데 묶을 수 있다"는 데 있지, "100%를 다 받는다"는 데 있지 않다. 정직하게 80%와 20%의 경계를 그을 줄 아는 사람이 결국 좋은 의사결정을 내린다.

다음 16장에서는 시야를 다시 옮겨, "DB가 백엔드다"라는 새로운 패턴 — PostgREST·pg_graphql·Supabase가 만들어낸 풀스택 의사결정의 자리로 가보자. SQL 표준과 익스텐션이 만들어낸 표현력이 어디까지 애플리케이션 계층을 줄일 수 있는지, 그리고 그 결정이 어떤 lock-in을 함께 가져오는지를 같이 따져볼 것이다.
