# 8장. SQL 표준과 트랜잭션 — RDB 정통의 깊이

애플리케이션 코드를 들여다보면, 절반 가까이가 데이터 가공이다. 어디서 가져오고, 어떻게 추리고, 무엇과 합치고, 어떤 모양으로 내보낼 것인가. 이 일을 누가 할 것인가에 대한 답이 두 가지로 갈린다. 한쪽은 "DB는 저장만 해주고 가공은 애플리케이션에서 한다"고 말한다. 다른 한쪽은 "DB가 SQL로 풀어줄 수 있다면 거기서 풀자"고 답한다. 어느 쪽이 옳은가에 대한 답은 사실 한 가지로 정해져 있지 않다. 답은 **그 DB가 SQL을 얼마나 풍부하게 표현할 수 있는가**에 달려 있다.

SQL이 빈약하면 가공을 애플리케이션으로 끌어올릴 수밖에 없다. 그러면 네트워크 왕복이 늘고, 트랜잭션 경계가 흐려지고, 코드는 점점 데이터 가공기에 가까워진다. 반대로 SQL이 풍부하면, 한 번의 쿼리로 끝낼 일을 굳이 코드로 펼치지 않아도 된다. 트랜잭션 안에서 원자적으로 일이 마무리되고, 애플리케이션은 비즈니스 결정에만 집중할 수 있다.

PostgreSQL이 "SQL 표준 준수"를 모토로 내세우는 것은 단순히 자랑이 아니다. 그 말의 뜻은 **표현력의 깊이를 무기로 가져왔다**는 선언이다. 그 깊이를 한 번 들여다보자. 윈도우 함수와 재귀 CTE에서 시작해, MERGE와 RETURNING의 진화, JSON_TABLE이 여는 새로운 가능성, 그리고 v18이 들고 온 RETURNING OLD/NEW와 temporal constraint까지. 끝에는 트랜잭션 DDL과 SAVEPOINT라는, 마이그레이션을 살리는 안전망까지 살펴보자.

3장에서 v17/v18 release note를 훑었을 때와는 톤이 다르다. 그때는 "올려야 하는가"를 따졌다면, 이번 장은 "그 기능으로 무엇이 가능해지는가"를 본다. 같은 기능이라도 어떻게 풀어 쓰는가에 따라 그 가치는 완전히 달라진다.

## 8.1 윈도우 함수·CTE·WITH RECURSIVE — SQL이 절차형을 흡수하는 지점

SQL이 풍부해진다는 말은 사실 추상적이다. 구체적으로 어디가 어떻게 풍부한가? 윈도우 함수와 CTE, 그리고 재귀 CTE가 그 답의 큰 부분을 차지한다. 이 셋이 없던 시절의 SQL은 집계와 조인 정도가 한계였고, 나머지는 애플리케이션 코드로 풀어야 했다. 셋이 들어오고 난 다음, SQL은 절차형 코드의 영역까지 흡수하기 시작한다.

### 8.1.1 윈도우 함수 — 집계의 패러다임을 바꾼 도구

집계 함수와 윈도우 함수의 차이를 한 줄로 말하면 이렇다. `GROUP BY`는 여러 행을 하나로 줄이지만, 윈도우 함수는 **행 수를 유지한 채로** 각 행 옆에 집계 결과를 붙여 준다. 이 작은 차이가 만들어내는 표현력의 폭이 엄청나다.

주문 데이터에서 "각 고객의 주문 옆에, 그 고객의 누적 결제 금액을 같이 보고 싶다"는 요구를 생각해보자. `GROUP BY customer_id`로는 절대 안 된다. 누적이라는 개념이 들어오면 자기 행과 이전 행들의 관계가 필요하기 때문이다. 윈도우 함수는 이 일을 한 줄로 끝낸다.

```sql
SELECT
  order_id,
  customer_id,
  ordered_at,
  amount,
  SUM(amount) OVER (
    PARTITION BY customer_id
    ORDER BY ordered_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS cumulative_amount
FROM orders
ORDER BY customer_id, ordered_at;
```

`PARTITION BY`는 어떤 그룹 안에서 집계할지 정한다. `ORDER BY`는 그 안의 순서를 정하고, `ROWS BETWEEN ...`은 자기 행을 기준으로 어디까지를 윈도우에 포함할지를 정한다. 이 세 가지의 조합으로 누적합, 이동평균, 직전 행과의 비교, N번째 행 가져오기 같은 거의 모든 시계열적 계산을 풀 수 있다.

랭킹은 또 다른 큰 쓰임새다. "각 카테고리에서 매출 상위 3개 상품을 뽑자"를 SQL로 풀려고 한다고 해보자. 윈도우 함수 없이 풀면 서브쿼리와 조인이 얽혀 끔찍한 모양이 된다. 그런데 `ROW_NUMBER()`와 `RANK()`, `DENSE_RANK()` 같은 함수가 들어오면 이렇게 풀린다.

```sql
WITH ranked AS (
  SELECT
    category_id,
    product_id,
    revenue,
    DENSE_RANK() OVER (
      PARTITION BY category_id
      ORDER BY revenue DESC
    ) AS rnk
  FROM product_sales
)
SELECT category_id, product_id, revenue
FROM ranked
WHERE rnk <= 3;
```

`ROW_NUMBER()`는 동률을 끊어 1, 2, 3을 주고, `RANK()`는 동률에 같은 순위를 주되 다음 순위를 건너뛰고(1, 1, 3), `DENSE_RANK()`는 동률에 같은 순위를 주되 다음 순위를 건너뛰지 않는다(1, 1, 2). 세 함수의 미묘한 차이를 잊지 말자. "Top-N per group" 패턴의 표준 답안이다.

`LAG()`와 `LEAD()`는 이전 행, 다음 행의 값을 가져오는 도구다. "직전 주문과의 시간 간격"이나 "전월 대비 매출 증감"을 SQL 한 줄로 표현할 수 있다.

```sql
SELECT
  customer_id,
  ordered_at,
  amount,
  amount - LAG(amount, 1, 0) OVER (
    PARTITION BY customer_id ORDER BY ordered_at
  ) AS delta_from_prev,
  EXTRACT(EPOCH FROM (
    ordered_at - LAG(ordered_at) OVER (
      PARTITION BY customer_id ORDER BY ordered_at
    )
  )) AS seconds_since_prev_order
FROM orders;
```

이 한 쿼리를 애플리케이션 코드로 풀려면 어떻게 될까? 전체 주문을 가져와 메모리에 정렬하고, 고객별로 묶고, 한 행씩 순회하면서 직전 값을 기억하고 차이를 계산해야 한다. 코드는 길어지고, 메모리는 부풀고, 트랜잭션 경계는 모호해진다. 윈도우 함수 한 줄과 비교하면, 어느 쪽이 더 우아한지는 굳이 따져볼 필요도 없다.

윈도우 프레임을 조금만 더 응용하면 이동평균도 자연스럽게 풀린다.

```sql
SELECT
  bucket_at,
  metric_value,
  AVG(metric_value) OVER (
    ORDER BY bucket_at
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7
FROM metrics_minutely;
```

직전 6개 행과 현재 행을 묶어 평균을 내면 곧 7행 이동평균이다. `ROWS` 대신 `RANGE`를 쓰면 행 개수가 아니라 시간 범위로 윈도우를 잡을 수도 있다. 14장의 시계열 분석에서 다시 만날 도구다.

랭킹과 LAG/LEAD 외에도 손에 익혀두면 좋은 함수가 몇 개 더 있다. `NTILE(n)`은 윈도우를 N등분해서 각 행이 몇 번째 분위에 속하는지를 돌려준다. "고객을 매출 4분위로 나누자"는 흔한 요구를 한 줄로 푼다.

```sql
SELECT
  customer_id,
  total_amount,
  NTILE(4) OVER (ORDER BY total_amount DESC) AS revenue_quartile
FROM customer_yearly_revenue;
```

`FIRST_VALUE()`와 `LAST_VALUE()`는 윈도우의 첫 번째·마지막 행의 값을 가져온다. "각 고객의 첫 주문 금액과 가장 최근 주문 금액을 같이 보고 싶다"는 요구를 그대로 표현할 수 있다.

```sql
SELECT DISTINCT
  customer_id,
  FIRST_VALUE(amount) OVER w AS first_amount,
  LAST_VALUE(amount)  OVER w AS latest_amount
FROM orders
WINDOW w AS (
  PARTITION BY customer_id
  ORDER BY ordered_at
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
);
```

여기서 한 가지 주의할 점이 있다. `LAST_VALUE()`의 기본 프레임은 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`다. 즉 현재 행까지만 보는 윈도우가 기본이라, 명시적으로 `UNBOUNDED FOLLOWING`까지 늘려주지 않으면 `LAST_VALUE`가 사실상 자기 자신을 돌려준다. 처음 보는 사람이 가장 잘 빠지는 함정이라 한 번쯤 헷갈리고 나면 잊을 수가 없다. 잊지 말자.

또 한 가지, `WINDOW w AS (...)` 절은 같은 윈도우 정의를 여러 함수에서 공유할 때 유용하다. 같은 PARTITION/ORDER를 반복해 적느니, 한 번 정의해 이름으로 부르는 편이 깔끔하다.

### 8.1.2 CTE — 가독성 한 단계, 그러나 함정도

CTE(Common Table Expression)는 `WITH` 절로 시작하는 일종의 "이름 붙은 서브쿼리"다. 복잡한 쿼리를 단계별로 풀어 읽기 좋게 만들어준다. 가독성이 첫 번째 효용이고, 같은 서브쿼리를 여러 번 참조할 때 한 번만 적어도 된다는 것이 두 번째 효용이다.

```sql
WITH recent_orders AS (
  SELECT * FROM orders
  WHERE ordered_at >= NOW() - INTERVAL '7 days'
),
customer_summary AS (
  SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(amount) AS total_amount
  FROM recent_orders
  GROUP BY customer_id
)
SELECT
  c.customer_id,
  c.order_count,
  c.total_amount,
  cu.tier
FROM customer_summary c
JOIN customers cu USING (customer_id)
WHERE c.total_amount > 1000000;
```

서브쿼리를 깊이 중첩한 버전과 비교해보면 가독성 차이가 한눈에 보인다.

CTE에는 한 가지 주의할 점이 있다. PostgreSQL 11까지 CTE는 **optimizer fence**처럼 동작했다. 즉, CTE가 일단 따로 계산되어 임시 결과로 떨어진 다음, 그 결과를 본 쿼리가 사용했다. 그래서 큰 테이블을 CTE로 감싸면 plan이 망가지는 경우가 있었다. PostgreSQL 12부터는 기본 동작이 `inline`으로 바뀌었다. 옵티마이저가 CTE를 본 쿼리 안으로 펼쳐 같이 최적화한다. 한 번만 참조되고 부작용(`INSERT/UPDATE/DELETE`)이 없는 CTE는 자동으로 인라인된다.

그렇다면 옛 동작을 유지하고 싶을 때는 어떻게 하느냐? `MATERIALIZED` 키워드를 명시한다.

```sql
WITH expensive_calc AS MATERIALIZED (
  SELECT ... FROM huge_table WHERE ...
)
SELECT ...
FROM expensive_calc
JOIN ...
```

반대로 명시적으로 인라인을 강제하려면 `NOT MATERIALIZED`다. PG 12 이후로 옮긴 팀이라면 한 번쯤 점검할 만한 지점이다. "CTE를 썼더니 갑자기 빨라졌어요" 또는 "CTE를 썼더니 갑자기 느려졌어요" 같은 보고가 들어오면 십중팔구 이 동작 변경이 원인이다.

### 8.1.3 WITH RECURSIVE — 절차형의 마지막 영역까지

윈도우 함수와 CTE가 SQL의 표현력을 한 차원 끌어올렸다면, `WITH RECURSIVE`는 그 다음 차원까지 간다. 트리·그래프·계층 구조처럼 "정해진 깊이 없이 따라가야 하는" 데이터를 SQL 안에서 한 번에 풀어낸다. 이런 일은 전통적으로 애플리케이션 코드로 처리하는 영역이었는데, 재귀 CTE가 그 경계를 허물었다.

조직도가 대표적인 예다. 사원 한 명의 모든 상위 관리자를 찾고 싶다고 해보자.

```sql
WITH RECURSIVE manager_chain AS (
  -- 앵커: 출발점
  SELECT employee_id, name, manager_id, 1 AS depth
  FROM employees
  WHERE employee_id = 12345

  UNION ALL

  -- 재귀: 한 단계씩 위로
  SELECT e.employee_id, e.name, e.manager_id, mc.depth + 1
  FROM employees e
  JOIN manager_chain mc ON e.employee_id = mc.manager_id
)
SELECT employee_id, name, depth
FROM manager_chain
ORDER BY depth;
```

핵심은 두 부분이 `UNION ALL`로 연결된 모양이다. 앵커는 출발점(직원 본인)을 잡고, 재귀 절은 직전 단계의 결과를 받아 한 단계씩 거슬러 올라간다. PostgreSQL은 결과 집합이 비어질 때까지 자동으로 반복한다.

반대로 어떤 관리자의 모든 부하 직원을 찾는 것도 같은 패턴이다. 조인 방향만 뒤집으면 된다.

```sql
WITH RECURSIVE subordinates AS (
  SELECT employee_id, name, manager_id, 1 AS depth
  FROM employees
  WHERE employee_id = 100  -- 최상위

  UNION ALL

  SELECT e.employee_id, e.name, e.manager_id, s.depth + 1
  FROM employees e
  JOIN subordinates s ON e.manager_id = s.employee_id
)
SELECT * FROM subordinates;
```

카테고리 트리, 댓글 스레드, 의존성 그래프, 모두 같은 모양으로 풀린다. 한 가지 잊지 말자. 사이클이 있는 그래프를 다룰 때는 무한 루프에 빠진다. PostgreSQL 14부터 `CYCLE` 절이 표준 SQL로 들어왔다.

```sql
WITH RECURSIVE graph AS (
  SELECT node, parent, ARRAY[node] AS path
  FROM nodes
  WHERE node = 'A'

  UNION ALL

  SELECT n.node, n.parent, g.path || n.node
  FROM nodes n
  JOIN graph g ON n.parent = g.node
)
CYCLE node SET is_cycle USING cycle_path
SELECT * FROM graph;
```

`CYCLE node SET is_cycle USING cycle_path`는 "`node` 컬럼을 기준으로 사이클을 감지해서, 감지되면 `is_cycle`을 `true`로 표시하고 경로는 `cycle_path`에 저장하라"는 뜻이다. 그래프 데이터를 다룬다면 이 절은 반드시 기억해두자. 무한 루프로 서버가 멈춰버리면 끔찍한 일이다.

`WITH RECURSIVE`는 트랜잭션 안에서 한 번에 끝나는 표현이라는 점이 중요하다. 애플리케이션이 N번 왕복하면서 트리를 따라가는 코드를 떠올려보자. 그 사이 누군가 트리를 수정하면? 일관성이 어디서 깨질지 모른다. 재귀 CTE는 그 모든 일을 한 스냅샷 위에서 처리한다. **SQL의 표현력이 동시성 안전성까지 자동으로 가져온다**는 사실은 자주 잊히는 효용이다.

## 8.2 MERGE와 RETURNING — UPSERT의 진짜 문법

이제 데이터를 쓰는 영역으로 넘어가자. "있으면 갱신, 없으면 삽입"이라는 패턴, 흔히 UPSERT라고 부르는 그것은 운영 시스템에서 가장 자주 나타나는 요구 중 하나다. 동기화 작업, 카운터 갱신, 외부 데이터 머지, 일배치 적재까지. 이 패턴을 어떻게 표현하느냐가 SQL의 격을 결정한다.

PostgreSQL이 오래전부터 가진 도구는 `INSERT ... ON CONFLICT`다.

```sql
INSERT INTO user_stats (user_id, login_count, last_login_at)
VALUES (42, 1, NOW())
ON CONFLICT (user_id) DO UPDATE
SET login_count = user_stats.login_count + 1,
    last_login_at = EXCLUDED.last_login_at;
```

`ON CONFLICT`는 어떤 제약(보통 unique index)을 기준으로 충돌을 감지할지 정한다. `EXCLUDED` 가상 테이블은 "삽입하려 했던 그 행"을 가리킨다. 갱신 식에서 `user_stats.login_count`(현재 행)와 `EXCLUDED.last_login_at`(들어오려 했던 행)을 동시에 참조할 수 있다는 점이 강력하다. 충돌이 났을 때 아무것도 하지 않으려면 `DO NOTHING`을 쓰면 된다.

이 구문은 PG-native, 표현력 좋고 빠르다. 그러나 한 가지 한계가 있다. 한 번에 INSERT, UPDATE, DELETE를 섞어 처리하지는 못한다. "조건에 따라 어떤 행은 새로 넣고, 어떤 행은 갱신하고, 어떤 행은 지워야" 하는 진짜 동기화 작업에서는 답이 모자랐다.

### 8.2.1 MERGE — SQL 표준의 UPSERT

PostgreSQL 15부터 `MERGE`가 들어왔다. SQL:2003 표준의 정통 문법이다. 소스와 타깃을 매칭한 다음, 매칭된 행에는 갱신·삭제를, 매칭되지 않은 행에는 삽입을 한다.

상품 마스터 데이터를 외부 시스템으로부터 받아 동기화한다고 해보자.

```sql
MERGE INTO products AS p
USING staging_products AS s
  ON p.sku = s.sku
WHEN MATCHED AND s.is_deleted THEN
  DELETE
WHEN MATCHED AND s.updated_at > p.updated_at THEN
  UPDATE SET
    name = s.name,
    price = s.price,
    updated_at = s.updated_at
WHEN NOT MATCHED THEN
  INSERT (sku, name, price, updated_at)
  VALUES (s.sku, s.name, s.price, s.updated_at);
```

한 문장 안에 세 가지 동작이 다 들어 있다. `ON` 절로 매칭 조건을 잡고, `WHEN MATCHED`와 `WHEN NOT MATCHED` 절로 어떤 경우에 무엇을 할지 정한다. `AND` 조건을 덧붙여 같은 매칭 안에서도 분기할 수 있다.

이 정도면 표현력이 충분해 보이는데, MERGE에는 더 깊은 효용이 있다. 트랜잭션 안에서 한 번의 스캔으로 모든 분기를 처리한다는 점이다. `ON CONFLICT`로 풀면 INSERT 한 번, UPDATE 한 번, DELETE 한 번 — 세 번의 문장으로 갈라 써야 하고, 각각이 독립적으로 락을 잡고 인덱스를 탄다. MERGE는 한 번에 끝낸다.

한 가지 주의할 점도 같이 짚어두자. MERGE는 동시성 시나리오에서 `ON CONFLICT`만큼 친절하지 않다. `ON CONFLICT`는 unique 제약 충돌을 자동으로 잡아 갱신 경로로 넘기지만, MERGE는 그런 자동 처리가 없다. 두 트랜잭션이 동시에 같은 키에 대해 `WHEN NOT MATCHED THEN INSERT`를 수행하면, unique 제약 위반으로 한쪽이 실패할 수 있다. 그래서 MERGE는 **싱글 라이터**가 동기화 배치를 처리하는 패턴에 잘 맞고, 다수 클라이언트가 동시에 같은 키를 갱신하는 OLTP 패턴에는 `ON CONFLICT`가 여전히 더 안전하다. 두 도구의 결을 구분해서 쓰는 편이 낫다.

### 8.2.2 PG 17의 진화 — MERGE에 RETURNING이 붙다

PostgreSQL 15의 MERGE에는 한 가지 답답한 점이 있었다. **무슨 행이 INSERT됐는지, UPDATE됐는지, DELETE됐는지를 알 길이 없었다.** 애플리케이션은 "몇 행이 영향을 받았다"는 카운트만 받았다. 동기화 후 후속 처리(예: 인덱스 재생성, 이벤트 발행, 캐시 무효화)가 필요한 경우, 어떤 행이 어떻게 바뀌었는지 모르면 난감하다.

PG 17이 이 구멍을 메웠다. `MERGE`에 `RETURNING` 절이 붙었고, **`merge_action()`** 이라는 함수로 각 행에 어떤 동작이 일어났는지를 식별할 수 있게 됐다.

```sql
MERGE INTO products AS p
USING staging_products AS s
  ON p.sku = s.sku
WHEN MATCHED AND s.is_deleted THEN
  DELETE
WHEN MATCHED AND s.updated_at > p.updated_at THEN
  UPDATE SET
    name = s.name,
    price = s.price,
    updated_at = s.updated_at
WHEN NOT MATCHED THEN
  INSERT (sku, name, price, updated_at)
  VALUES (s.sku, s.name, s.price, s.updated_at)
RETURNING
  merge_action() AS action,
  p.sku,
  p.name,
  p.price;
```

결과는 이런 모양이 된다.

```
 action  |  sku  |   name    |  price
---------+-------+-----------+--------
 INSERT  | A-001 | 새 상품 A  | 10000
 UPDATE  | A-002 | 갱신 상품  | 12000
 DELETE  | A-003 | 폐기 상품  |  8000
```

이 결과를 한 번의 트랜잭션 안에서 받아 후속 처리(이벤트 발행, 캐시 키 무효화)로 흘려보낼 수 있다. 동기화 → 카운트만 보고 끝났던 시절과 비교하면 큰 진보다.

`RETURNING`은 MERGE에만 붙는 게 아니다. INSERT, UPDATE, DELETE 모두에서 오래전부터 쓸 수 있었다.

```sql
-- 삽입 후 생성된 ID 즉시 반환
INSERT INTO orders (customer_id, amount)
VALUES (42, 100000)
RETURNING order_id, created_at;

-- 갱신 후 새 값 확인
UPDATE accounts
SET balance = balance - 50000
WHERE account_id = 7
RETURNING balance AS new_balance;

-- 삭제된 행을 감사 로그로
DELETE FROM sessions
WHERE expired_at < NOW()
RETURNING user_id, session_id;
```

이 패턴 하나만 잘 써도 애플리케이션 코드가 눈에 띄게 줄어든다. "INSERT 후에 SELECT로 다시 조회해서 ID를 알아내는" 두 번 왕복 코드는 이제 옛 패턴이다. 한 번에 끝낼 수 있는 일을 두 번 가는 것은 번거롭다.

## 8.3 JSON_TABLE — JSON을 FROM 절에 펼치다

PostgreSQL은 일찍부터 JSONB를 받아들였다. 이 이야기는 9장에서 깊이 다루지만, 이번 장에서는 SQL 표현력의 관점에서 한 가지 도구만 짚자. **JSON_TABLE**이다. SQL:2016 표준이고, PG 17부터 정식으로 들어왔다.

문제 상황을 먼저 그려보자. JSON 컬럼에 다음과 같은 데이터가 있다고 해보자.

```json
{
  "order_id": "ORD-9981",
  "customer": {"id": 42, "name": "홍길동"},
  "items": [
    {"sku": "A-001", "qty": 2, "price": 10000},
    {"sku": "B-007", "qty": 1, "price": 25000},
    {"sku": "C-013", "qty": 5, "price":  3000}
  ]
}
```

여기서 "각 주문의 라인 아이템을 평탄화해서 행으로 펼치고 싶다"는 요구가 들어왔다고 해보자. PG 17 이전이라면 `jsonb_array_elements`와 `->>` 연산자를 동원해 풀어야 했다.

```sql
SELECT
  o.order_id,
  (item->>'sku')                AS sku,
  (item->>'qty')::int           AS qty,
  (item->>'price')::numeric     AS price
FROM orders_json o,
     LATERAL jsonb_array_elements(o.payload->'items') AS item;
```

읽을 수는 있지만, 컬럼이 늘어날수록 캐스팅이 빽빽해진다. 5~6개만 넘어가도 한눈에 들어오지 않는다. JSON_TABLE은 같은 일을 훨씬 깔끔하게 풀어낸다.

```sql
SELECT jt.*
FROM orders_json o,
     JSON_TABLE(
       o.payload,
       '$'
       COLUMNS (
         order_id    text     PATH '$.order_id',
         customer_id int      PATH '$.customer.id',
         NESTED PATH '$.items[*]' COLUMNS (
           sku   text    PATH '$.sku',
           qty   int     PATH '$.qty',
           price numeric PATH '$.price'
         )
       )
     ) AS jt;
```

핵심은 세 가지다. 첫째, `JSON_TABLE`은 FROM 절 안에 들어가는 **테이블 함수**다. JSON을 통째로 받아 행과 컬럼으로 펼친다. 둘째, JSONPath(`$.order_id`)로 어떤 경로의 값을 어떤 컬럼으로 매핑할지 선언적으로 적는다. 셋째, `NESTED PATH`로 배열을 한 번에 평탄화한다. 위 쿼리는 한 주문에 3개 아이템이 있으면 3행으로 펼쳐진다.

이 한 번의 변환으로 무엇이 바뀌는가? 그 결과를 그대로 JOIN, GROUP BY, 윈도우 함수, MERGE에 넘길 수 있다. 즉 **JSON을 SQL의 1급 시민으로 취급할 수 있게 된다**.

집계도 자연스럽다.

```sql
SELECT
  jt.sku,
  SUM(jt.qty * jt.price) AS total_revenue
FROM orders_json o,
     JSON_TABLE(
       o.payload,
       '$'
       COLUMNS (
         NESTED PATH '$.items[*]' COLUMNS (
           sku   text    PATH '$.sku',
           qty   int     PATH '$.qty',
           price numeric PATH '$.price'
         )
       )
     ) AS jt
GROUP BY jt.sku
ORDER BY total_revenue DESC
LIMIT 10;
```

JSON 형태로 들어온 주문 데이터에서 SKU별 매출 상위 10개를 뽑는 일이 한 쿼리로 끝났다. 같은 일을 애플리케이션 코드로 풀려면 어떻게 될까? 전체 JSON 행을 가져와 파싱하고, 배열을 순회하면서 SKU별 누적 매출을 집계해 정렬하는 코드를 짜야 한다. 코드 양도, 메모리도, 네트워크도 부담이 커진다.

또 한 가지 효용은 **타입 안전성**이다. `JSON_TABLE` COLUMNS 절에 적은 `int`, `numeric`, `text` 같은 타입은 자동 캐스팅된다. 한 컬럼이 정의된 타입과 맞지 않으면 어떻게 처리할지 `ON ERROR` 절로 지정할 수 있다.

```sql
... PATH '$.qty' DEFAULT 0 ON EMPTY DEFAULT -1 ON ERROR
```

값이 비어 있으면 0, 캐스팅 에러면 -1로 대체한다. 외부에서 받은 JSON처럼 스키마가 들쭉날쭉한 데이터를 처리할 때 이 절은 큰 효자다. 캐스팅 에러로 쿼리가 통째로 죽어버리는 일은 정말 끔찍한 일이다.

이벤트 로그를 행으로 펼치는 작업, 외부 API 응답을 보고용 테이블로 평탄화하는 작업, 설정 JSON에서 특정 키만 뽑아 검증 쿼리에 거는 작업 — JSON_TABLE이 가는 영역은 생각보다 넓다. 9장에서 다시 만나겠지만, "JSONB를 쓴다 = SQL을 포기한다"는 옛 생각은 이제 안 해도 된다.

## 8.4 RETURNING OLD/NEW와 트리거의 단순화 — v18의 작은 혁명

INSERT/UPDATE/DELETE에 붙는 `RETURNING`은 오래된 도구다. 그런데 한 가지 답답한 점이 있었다. **UPDATE의 RETURNING은 갱신 후 값만 돌려준다.** 갱신 전 값을 같이 보고 싶으면 SELECT를 따로 날리든지, 트리거 안에서 OLD/NEW를 직접 만져 별도 테이블로 옮겨 적어야 했다.

PostgreSQL 18에서 이 답답함이 풀렸다. `RETURNING OLD.*`와 `RETURNING NEW.*`가 정식 문법으로 들어왔다.

```sql
UPDATE accounts
SET balance = balance - 50000
WHERE account_id = 7
RETURNING
  OLD.balance AS prev_balance,
  NEW.balance AS new_balance,
  NEW.balance - OLD.balance AS delta;
```

이 한 줄로 끝나는 일이, v17까지는 트리거 한 벌이 필요했다. 감사 로그(audit log)를 적는 흔한 패턴을 v17 이전 방식으로 풀어보자.

```sql
-- v17 이전: 트리거 함수
CREATE OR REPLACE FUNCTION audit_account_changes()
RETURNS trigger AS $$
BEGIN
  INSERT INTO account_audit (
    account_id, prev_balance, new_balance,
    changed_at, changed_by
  )
  VALUES (
    NEW.account_id, OLD.balance, NEW.balance,
    NOW(), current_user
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_account
AFTER UPDATE ON accounts
FOR EACH ROW EXECUTE FUNCTION audit_account_changes();
```

트리거 함수를 PL/pgSQL로 작성하고, 트리거를 따로 걸어야 한다. 트리거가 늘어나면 어떤 트리거가 어떤 순서로 발화하는지 추적이 점점 어려워진다. 트리거 디버깅이 시작되면 정말 찜찜하다.

v18에서는 같은 일을 단일 SQL 한 줄로 풀 수 있다.

```sql
-- v18: CTE + RETURNING OLD/NEW로 트리거 없이
WITH changed AS (
  UPDATE accounts
  SET balance = balance - 50000
  WHERE account_id = 7
  RETURNING
    NEW.account_id,
    OLD.balance AS prev_balance,
    NEW.balance AS new_balance
)
INSERT INTO account_audit (
  account_id, prev_balance, new_balance, changed_at, changed_by
)
SELECT
  account_id, prev_balance, new_balance, NOW(), current_user
FROM changed;
```

CTE 안에서 UPDATE를 실행하고, 그 결과의 OLD/NEW를 받아 INSERT로 흘린다. 트리거 정의도 없고, 트리거 함수도 없다. 한 트랜잭션 안에서 원자적으로 끝난다.

트리거가 무의미하다는 말은 아니다. 모든 경로의 갱신을 빠짐없이 잡아야 할 때, 트리거는 여전히 강력하다. 그러나 **명시적 SQL이 잡을 수 있는 케이스를 굳이 트리거로 숨길 이유는 줄어들었다**. 코드 읽기에서 "어디서 무엇이 벌어지는가"를 추적하기 쉬워진다. 트리거는 마법을 부리지만, 마법이 너무 많으면 운영이 힘들어진다.

DELETE에서도 OLD를 받아 감사 테이블로 보내는 같은 패턴이 자연스럽다.

```sql
WITH deleted AS (
  DELETE FROM sessions
  WHERE expired_at < NOW()
  RETURNING OLD.*
)
INSERT INTO session_history
SELECT *, NOW() AS archived_at FROM deleted;
```

세션 만료 처리와 이력 보존을 한 트랜잭션, 한 문장에 묶었다. CTE로 INSERT/UPDATE/DELETE를 엮어 한 번에 데이터를 옮기는 패턴, 잊지 말고 손에 익혀두자.

3장에서 v18의 `RETURNING OLD/NEW`를 두고 "올려야 하는가"를 따졌다면, 여기서는 "그것으로 트리거 한 벌을 지울 수 있다"는 결말까지 봤다. 같은 기능을 어느 톤으로 보느냐의 차이다.

## 8.5 Temporal Constraint — 이력 테이블 설계의 새 기준

이력 관리는 모든 시스템의 숙제다. 가격이 어느 시점에 어떻게 바뀌었는지, 계약이 어느 기간에 유효했는지, 사용자가 어느 기간에 어떤 권한을 가졌는지. 이런 질문에 답하려면 시점 정보를 가진 테이블이 필요하다.

전통적인 모델은 `valid_from`, `valid_to` 두 컬럼을 두는 것이다.

```sql
CREATE TABLE product_prices (
  product_id  bigint  NOT NULL,
  price       numeric NOT NULL,
  valid_from  timestamptz NOT NULL,
  valid_to    timestamptz,  -- NULL이면 현재 유효
  PRIMARY KEY (product_id, valid_from)
);
```

이 모델에는 두 가지 골치 아픈 문제가 있다. 첫째, **같은 상품에 대해 기간이 겹치는 행이 들어가는 것을 막을 방법이 마땅찮다**. 평범한 UNIQUE 제약으로는 "기간 겹침"을 표현할 수 없기 때문이다. 둘째, **현재 시점의 행을 어떻게 표현할지가 애매하다**. `valid_to = NULL`로 두면 SQL의 NULL 처리가 골치 아프고, `9999-12-31` 같은 매직 값을 쓰면 또 다른 의미상 부담이 생긴다.

PostgreSQL에는 오래전부터 `range` 타입과 GiST `EXCLUDE` 제약이 있었다. 이걸로 기간 겹침은 막을 수 있었다.

```sql
CREATE TABLE product_prices (
  product_id  bigint  NOT NULL,
  price       numeric NOT NULL,
  valid_period tstzrange NOT NULL,
  EXCLUDE USING gist (
    product_id WITH =,
    valid_period WITH &&
  )
);
```

`&&`는 range 타입의 겹침 연산자다. 같은 `product_id`에 대해 `valid_period`가 겹치는 두 행이 동시에 존재할 수 없도록 한다. 강력한 도구지만, 문법이 익숙하지 않아 신규 개발자에게 설명하기가 만만치 않았다.

### 8.5.1 v18의 temporal constraint — SQL 표준의 정통 문법

PostgreSQL 18에서 SQL:2011이 정의한 **temporal table** 문법이 들어왔다. `PRIMARY KEY ... WITHOUT OVERLAPS`와 `FOREIGN KEY ... PERIOD`가 그 핵심이다.

```sql
CREATE TABLE product_prices (
  product_id   bigint NOT NULL,
  price        numeric NOT NULL,
  valid_period tstzrange NOT NULL,
  PRIMARY KEY (product_id, valid_period WITHOUT OVERLAPS)
);
```

`WITHOUT OVERLAPS`가 들어가면 자동으로 GiST 인덱스가 생기고, 같은 `product_id`에 `valid_period`가 겹치는 행은 거부된다. 의도가 문법에 그대로 드러나기 때문에 읽기도 좋다.

외래키 쪽이 더 멋지다. "어떤 계약이 유효한 기간 안에서만 그 계약의 결제 이력이 있을 수 있다"는 무결성을 SQL로 표현하려고 한다고 해보자.

```sql
CREATE TABLE contracts (
  contract_id  bigint NOT NULL,
  party_id     bigint NOT NULL,
  active_period tstzrange NOT NULL,
  PRIMARY KEY (contract_id, active_period WITHOUT OVERLAPS)
);

CREATE TABLE contract_payments (
  payment_id    bigint PRIMARY KEY,
  contract_id   bigint NOT NULL,
  paid_period   tstzrange NOT NULL,
  amount        numeric NOT NULL,
  FOREIGN KEY (contract_id, PERIOD paid_period)
    REFERENCES contracts (contract_id, PERIOD active_period)
);
```

`FOREIGN KEY (contract_id, PERIOD paid_period) REFERENCES contracts (contract_id, PERIOD active_period)` — 이 한 줄이 "이 결제는 계약이 유효한 기간 안에 속해야 한다"는 무결성을 자동으로 보장한다. 이전에는 트리거나 애플리케이션 코드로 짜야 했던 검증이 제약으로 들어왔다.

이력 데이터를 다루는 모든 시스템에서 한 번쯤 검토할 만한 새 무기다. 계약·가격·환율·권한 같은 시간 의존적 마스터 데이터, 그리고 그것을 참조하는 트랜잭션 데이터가 있다면, 무결성을 데이터 계층에 박을 수 있다는 의미가 크다. 무결성을 애플리케이션이 책임지면 어딘가 한 곳에서 뚫린다. 데이터베이스가 책임지면 뚫릴 곳이 없다.

### 8.5.2 시점 조회 패턴 — 이력 테이블에서 한 시점의 모습 보기

이력 테이블을 만들었으면, 자주 마주칠 질문이 있다. **"어느 시점의 상태가 어땠는가?"** 이걸 SQL로 풀어보자.

```sql
-- 2026-01-15 10:00 시점의 상품 가격
SELECT product_id, price
FROM product_prices
WHERE valid_period @> '2026-01-15 10:00:00'::timestamptz;
```

`@>`는 range가 특정 값을 포함하는지 검사하는 연산자다. GiST 인덱스가 걸려 있으면 빠르게 답이 나온다. 윈도우 함수와 결합하면 시점별 가격 추이도 한 쿼리로 풀린다.

```sql
SELECT
  product_id,
  lower(valid_period) AS effective_from,
  price,
  LAG(price) OVER (
    PARTITION BY product_id ORDER BY lower(valid_period)
  ) AS prev_price,
  price - LAG(price) OVER (
    PARTITION BY product_id ORDER BY lower(valid_period)
  ) AS price_delta
FROM product_prices
WHERE product_id = 1234
ORDER BY lower(valid_period);
```

윈도우 함수, range 타입, temporal constraint — 8장에서 본 도구들이 한 쿼리에서 자연스럽게 합쳐진다. SQL의 표현력이 깊다는 말의 진짜 뜻이 여기 있다. **하나하나의 도구가 따로 따로가 아니라, 같은 SQL 문법 안에서 조립된다**는 것.

## 8.6 트랜잭션 DDL과 SAVEPOINT — 마이그레이션의 안전망

마지막으로 가장 자주 잊히는 PG의 무기 하나를 보자. **트랜잭션 DDL**이다. CREATE TABLE, ALTER TABLE, CREATE INDEX, DROP TABLE 같은 스키마 변경이 트랜잭션 안에서 동작하고, 실패하면 깔끔하게 롤백된다는 사실. 너무 당연해 보이지만, MySQL이나 Oracle을 오래 쓴 사람에겐 전혀 당연하지 않다.

MySQL에서 마이그레이션 도중 ALTER TABLE이 중간에 실패하면 어떻게 되는가? 일부 변경이 그대로 남는다. 롤백되지 않는다. 그래서 마이그레이션 도구는 "변경을 작은 단위로 쪼개서, 실패하면 어디까지 됐는지를 사람이 추적"하는 방식으로 동작한다. 운영 중에 마이그레이션이 깨지면 정말 끔찍한 일이다.

PostgreSQL에서는 다음 한 덩어리가 통째로 원자적이다.

```sql
BEGIN;

CREATE TABLE new_orders (
  order_id    bigint PRIMARY KEY,
  customer_id bigint NOT NULL,
  amount      numeric NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT NOW()
);

INSERT INTO new_orders (order_id, customer_id, amount, created_at)
SELECT order_id, customer_id, amount, created_at
FROM orders;

ALTER TABLE orders RENAME TO old_orders;
ALTER TABLE new_orders RENAME TO orders;

CREATE INDEX idx_orders_customer ON orders (customer_id);

COMMIT;
```

이 트랜잭션 안에서 무엇이 실패하든 — 인덱스 생성에서 디스크가 부족하든, 외부 락 충돌이 나든 — 트랜잭션 전체가 되돌려진다. 절반만 적용된 상태로 멈추는 일이 없다. 이 안전성 위에서 Flyway, Liquibase, Alembic 같은 마이그레이션 도구가 진짜로 안전하게 동작한다.

한 가지 예외만 기억해두자. `CREATE INDEX CONCURRENTLY`는 트랜잭션 안에서 못 쓴다. 락을 잡지 않고 인덱스를 만드는 특수 명령이라 트랜잭션 외부에서만 실행할 수 있다. 이 한 가지는 별도 단계로 빼야 한다.

```sql
-- 한 트랜잭션 안 (DDL 묶음)
BEGIN;
ALTER TABLE orders ADD COLUMN tier text;
UPDATE orders SET tier = 'standard';
ALTER TABLE orders ALTER COLUMN tier SET NOT NULL;
COMMIT;

-- 별도 단계 (운영 락 회피)
CREATE INDEX CONCURRENTLY idx_orders_tier ON orders (tier);
```

### 8.6.1 SAVEPOINT — 한 트랜잭션 안의 부분 롤백

트랜잭션 안에서 일부만 되돌리고 싶을 때가 있다. 예를 들어 대량 데이터를 한 트랜잭션으로 적재하면서, 한 행에서 에러가 나도 그 행만 건너뛰고 나머지는 살리고 싶다고 해보자. SAVEPOINT가 그 일을 해준다.

```sql
BEGIN;

SAVEPOINT before_batch;
INSERT INTO target_table SELECT ... FROM source_a;
-- 성공: 그대로 진행
RELEASE SAVEPOINT before_batch;

SAVEPOINT before_risky;
INSERT INTO target_table SELECT ... FROM source_b;
-- 실패: 이 부분만 되돌리고 트랜잭션은 살린다
ROLLBACK TO SAVEPOINT before_risky;

INSERT INTO target_table SELECT ... FROM source_c;

COMMIT;
```

SAVEPOINT는 일종의 트랜잭션 안의 체크포인트다. 부분 롤백을 명시적으로 표현할 수 있다. 한 가지 주의할 점은 SAVEPOINT가 많아지면 메모리와 성능에 부담을 준다는 사실이다. 일반적인 OLTP 트랜잭션에서 SAVEPOINT를 수십, 수백 개씩 만드는 것은 권장되지 않는다. 큰 ETL 잡이나 마이그레이션처럼 묶음 단위로 제어할 때 쓰는 도구다.

JDBC, psycopg, asyncpg 같은 클라이언트 라이브러리도 PostgreSQL의 SAVEPOINT를 활용한다. 예를 들어 Spring의 `@Transactional`에서 자식 트랜잭션처럼 보이는 `Propagation.NESTED`는 내부적으로 SAVEPOINT로 구현된다. 21장에서 PgBouncer의 transaction pooling 모드를 다룰 때 이 SAVEPOINT 동작이 어떻게 어긋날 수 있는지 다시 만나게 된다.

### 8.6.2 PostgreSQL의 트랜잭션 격리 수준 — Read Committed에서 Serializable까지

트랜잭션 이야기를 했으면 격리 수준(isolation level)을 빼놓고 갈 수 없다. PostgreSQL은 SQL 표준의 네 가지 격리 수준 중 세 가지를 제공한다. **Read Committed**(기본), **Repeatable Read**, **Serializable**. Read Uncommitted는 받아들이긴 하지만 내부적으로 Read Committed로 처리된다.

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- 작업
COMMIT;
```

Read Committed는 가장 가벼운 수준이다. 각 SELECT가 자신이 시작하는 시점의 스냅샷을 본다. 같은 트랜잭션 안에서 같은 쿼리를 두 번 날리면, 두 번째 SELECT 사이에 누군가 다른 트랜잭션이 COMMIT했다면, 두 번째 결과가 달라질 수 있다. 흔히 "non-repeatable read"라고 부르는 현상이다.

Repeatable Read는 트랜잭션 시작 시점의 스냅샷으로 모든 SELECT가 답한다. 같은 쿼리를 몇 번 날려도 결과가 같다. PG의 Repeatable Read는 실제로는 표준 정의보다 한 단계 더 강한, **snapshot isolation**이라는 모델이다.

Serializable은 가장 강한 수준이다. 7장에서 본 SSI(Serializable Snapshot Isolation)가 여기서 동작한다. 여러 트랜잭션이 동시에 돌아도, 마치 한 줄로 차례차례 실행한 것 같은 결과를 보장한다. 직렬화 가능성이 깨질 위험이 감지되면 한쪽 트랜잭션을 abort시킨다. 그래서 Serializable 트랜잭션을 쓰는 코드는 **abort에 대비해 재시도 로직을 가져야 한다**.

```python
# 의사 코드: 재시도 패턴
import time

def transactional_work():
    for attempt in range(MAX_RETRIES):
        try:
            with conn.transaction(isolation="serializable"):
                do_critical_work()
            return
        except SerializationFailure:
            time.sleep(2 ** attempt * 0.01)  # 지수 백오프
    raise RuntimeError("max retries exceeded")
```

금융·결제·재고처럼 일관성에 한 치의 양보가 없는 시스템에서 Serializable은 든든한 방패다. 비용은 abort 가능성과 재시도 처리지만, 락 기반 직렬화에 비하면 throughput은 훨씬 좋다. SSI의 이론적 배경은 7장에서 자세히 다뤘으니 한 번 더 펼쳐 보면 좋다.

## 마무리 — SQL이 풍부할수록 코드가 가벼워진다

이번 장에서 본 도구들을 한 자리에 모아보자. 윈도우 함수와 CTE, 재귀 CTE, MERGE와 RETURNING(v15·v17), JSON_TABLE(v17), RETURNING OLD/NEW(v18), temporal constraint(v18), 트랜잭션 DDL과 SAVEPOINT. 이 도구들의 공통점은 무엇인가? **SQL 한 문장 안에서 끝내는 영역을 점점 넓혀준다**는 점이다.

이 사실이 왜 중요한지 다시 짚어보자. 한 SQL로 끝나는 일은 한 트랜잭션 안에서 원자적이다. 한 스냅샷 위에서 일관성이 보장된다. 네트워크 왕복이 한 번이다. 옵티마이저가 전체를 보고 최적화한다. 같은 일을 애플리케이션 코드로 풀어 헤치면 이 모든 효용이 사라진다. 일관성 보장은 락이나 분산 트랜잭션으로 다시 만들어야 하고, 네트워크는 여러 번 오가고, 옵티마이저는 부분만 보게 된다.

"SQL 표준 준수"라는 PostgreSQL의 모토는 마케팅 문구가 아니다. **표준에 정의된 풍부한 표현력을 받아들였다는 약속**이다. 그 약속이 v15, v17, v18을 거치며 차근차근 채워지고 있다. MERGE가 들어왔고, JSON_TABLE이 들어왔고, RETURNING OLD/NEW가 들어왔고, temporal constraint가 들어왔다. 이 흐름은 v19, v20에서도 이어질 것이다.

마지막으로 한 가지 당부하자. 이 도구들을 다 외울 필요는 없다. 그러나 **"이건 SQL로 풀 수 있는 일인가?"라는 질문을 먼저 던지는 습관**은 가질 만하다. 애플리케이션 코드가 데이터를 길게 가공하기 시작하면, 그 자리에 윈도우 함수나 MERGE나 JSON_TABLE이 들어갈 자리가 있지 않은지 의심해보자. 절반은 들어간다.

물론 모든 일을 SQL로 풀자는 말은 아니다. 비즈니스 로직, 외부 시스템 호출, 복잡한 분기 처리는 애플리케이션의 일이다. 하지만 데이터 가공의 영역에서는, PostgreSQL의 표현력을 한 번 더 믿어볼 만하다.

그리고 이 표현력의 그림자도 같이 봐 두자. SQL이 풍부할수록 한 쿼리에 담기는 일이 많아지고, 한 쿼리가 깨질 때의 영향 범위도 같이 커진다. EXPLAIN으로 plan을 읽는 습관, pg_stat_statements로 느린 쿼리를 추적하는 습관, MERGE처럼 한 번에 많은 일을 하는 문장에 대해서는 lock 행동까지 추적하는 습관 — 이 운영의 기본기는 함께 가져가야 한다. 21장과 23장에서 이 도구들과 다시 만난다. 표현력은 무기지만, 무기를 안전하게 다루는 손도 같이 만들어야 한다는 사실은 잊지 말자.

다음 장에서는 같은 표현력의 한 갈래, JSONB와 문서 DB 영역으로 더 깊이 들어간다. 8장에서 잠깐 본 JSON_TABLE이 어떤 더 큰 그림의 한 조각이었는지가 거기서 드러난다. MongoDB를 대체할 수 있는가, 어디까지 대체 가능한가에 대한 답을 같이 찾아보자.
