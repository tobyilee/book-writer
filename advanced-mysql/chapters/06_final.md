# 6장. SQL의 표현력을 다시 끌어올리자 — 윈도우와 CTE

어느 날 기획팀에서 요청이 들어왔다. "상품별로 일별 매출과, 그 상품의 최근 7일 누적 매출을 같이 보여주는 화면이 필요해요." 개발자가 쿼리를 짜기 시작한다. 일별 집계는 GROUP BY로 하면 되는데, 7일 누적 합계는 어떻게 하지? 결국 Java 코드에서 결과를 받아다가 날짜 순서대로 반복문을 돌리면서 누적 합계를 계산한다. 쿼리 한 번, 자바 로직 한 번. 일단 동작은 한다.

그런데 이 방식에 찜찜함이 있다. 데이터가 늘어나면 자바 메모리에 얼마나 올라오는지 알 수 없고, 비슷한 집계 요청이 올 때마다 로직이 서비스 레이어에 쌓인다. 데이터를 가장 잘 아는 MySQL이 처리하면 될 일을 어플리케이션이 떠맡는 구조다.

MySQL 8.0은 이 상황을 바꿨다. 윈도우 함수와 CTE가 들어오면서, 애플리케이션에서 반복문으로 쌓던 집계 로직을 SQL 한 쿼리 안에서 표현할 수 있게 됐다. 어디까지 SQL로 할 수 있는지, 어디서 멈추는 게 맞는지를 같이 살펴보자.

## 윈도우 함수 — GROUP BY 없이 집계하기

윈도우 함수를 처음 접하면 개념이 낯설게 느껴진다. `GROUP BY`와 비슷한데 왜 따로 있는 걸까? 차이는 명확하다. `GROUP BY`는 행을 합쳐서 하나로 만드는 반면, 윈도우 함수는 행을 합치지 않고 원본 행을 유지하면서 집계 값을 곁에 붙여준다.

일별 주문 데이터에서 각 행 옆에 그 날의 주문 건수 합계를 붙이는 예를 보자.

```sql
-- GROUP BY는 날짜별로 행을 묶어버린다
SELECT order_date, COUNT(*) AS daily_count
FROM orders
GROUP BY order_date;

-- OVER()를 쓰면 원본 행을 유지하면서 집계 값을 옆에 붙인다
SELECT id, order_date, amount,
       COUNT(*) OVER (PARTITION BY order_date) AS daily_count
FROM orders;
```

`OVER (PARTITION BY order_date)`가 핵심이다. `PARTITION BY`는 GROUP BY처럼 그룹을 나누지만, 그룹으로 묶어버리지 않고 "이 그룹 안에서 집계 계산을 한다"는 의미다.

### ROW_NUMBER, RANK, DENSE_RANK

보고서에서 가장 자주 쓰이는 것들이다. 순위를 매길 때 쓴다.

```sql
-- 사용자별 최근 주문 1건씩 가져오기
SELECT *
FROM (
    SELECT id, user_id, amount, created_at,
           ROW_NUMBER() OVER (
               PARTITION BY user_id
               ORDER BY created_at DESC
           ) AS rn
    FROM orders
    WHERE status = 'COMPLETED'
) ranked
WHERE rn = 1;
```

`ROW_NUMBER()`는 같은 값이 있어도 무조건 다른 번호를 매긴다. 반면 `RANK()`는 같은 값에 같은 순위를 주고 다음 순위를 건너뛰고, `DENSE_RANK()`는 같은 값에 같은 순위를 주되 번호를 건너뛰지 않는다. 상황에 따라 골라 쓰자.

### LAG, LEAD — 앞뒤 행 참조

전일 대비 매출 증감을 구하려면 각 행에서 바로 이전 날의 값이 필요하다. 자바에서 처리하면 리스트를 정렬한 뒤 인덱스로 앞뒤를 참조해야 하는데, SQL에서는 `LAG`와 `LEAD`로 해결한다.

```sql
-- 일별 매출과 전일 대비 증감
SELECT
    order_date,
    daily_revenue,
    LAG(daily_revenue, 1) OVER (ORDER BY order_date) AS prev_day_revenue,
    daily_revenue - LAG(daily_revenue, 1, 0) OVER (ORDER BY order_date) AS revenue_diff
FROM (
    SELECT DATE(created_at) AS order_date,
           SUM(amount) AS daily_revenue
    FROM orders
    WHERE status = 'COMPLETED'
    GROUP BY DATE(created_at)
) daily
ORDER BY order_date;
```

`LAG(daily_revenue, 1, 0)` — 1행 앞의 값을 가져오되 앞이 없으면 0을 쓴다. `LEAD`는 반대로 뒤 행을 참조한다.

### SUM OVER — 누적 합계와 이동 평균

처음 예시에서 나온 7일 누적 매출이다. `ROWS BETWEEN` 구문으로 창(window) 범위를 정의한다.

```sql
-- 일별 매출과 7일 이동 합계
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg
FROM (
    SELECT DATE(created_at) AS order_date,
           SUM(amount) AS daily_revenue
    FROM orders
    WHERE status = 'COMPLETED'
    GROUP BY DATE(created_at)
) daily
ORDER BY order_date;
```

`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`는 현재 행을 포함해 앞 6개, 합쳐서 7개 행을 창으로 잡는다는 의미다. 누적 합계가 필요하면 `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`를 쓴다.

이 쿼리를 자바로 구현한다면? 결과 리스트를 받아 날짜 순서로 정렬, 인덱스 i에서 max(0, i-6)부터 i까지의 합계를 구하는 반복문. 쿼리에서 처리하면 MySQL이 최적화된 방식으로 처리하고 자바 메모리에는 최종 결과만 들어온다.

## CTE — 비재귀부터 시작하자

CTE(Common Table Expression)는 쿼리 안에 이름을 붙인 임시 결과 집합을 만드는 문법이다. `WITH` 절로 시작한다. 비재귀 CTE는 서브쿼리를 읽기 좋게 이름을 붙여 쓰는 것과 비슷한데, 실제로 얻는 이점이 있다.

```sql
-- 서브쿼리 방식 — 같은 서브쿼리가 두 번 나타나야 할 때 번거롭다
SELECT a.user_id, a.total, b.avg_amount
FROM (
    SELECT user_id, SUM(amount) AS total
    FROM orders WHERE status = 'COMPLETED'
    GROUP BY user_id
) a
JOIN (
    SELECT AVG(amount) AS avg_amount
    FROM orders WHERE status = 'COMPLETED'
) b;

-- CTE 방식 — 중간 결과에 이름을 붙여 재사용
WITH completed_orders AS (
    SELECT user_id, amount
    FROM orders
    WHERE status = 'COMPLETED'
),
user_totals AS (
    SELECT user_id, SUM(amount) AS total
    FROM completed_orders
    GROUP BY user_id
),
overall_avg AS (
    SELECT AVG(amount) AS avg_amount
    FROM completed_orders
)
SELECT t.user_id, t.total, a.avg_amount
FROM user_totals t
CROSS JOIN overall_avg a;
```

`completed_orders`를 한 번 정의하고 `user_totals`와 `overall_avg` 양쪽에서 참조했다. 서브쿼리라면 같은 내용을 두 번 써야 했을 것이다. 가독성이 높아지는 건 덤이고, 복잡한 쿼리를 단계별로 나눠 이해하고 검증할 수 있다는 것이 실용적인 이점이다.

MySQL의 비재귀 CTE는 옵티마이저가 내부적으로 뷰나 임시 테이블처럼 처리하는 경우가 있다. 같은 CTE를 여러 번 참조하면 결과를 임시 테이블에 저장해 재사용할 수 있다. 서브쿼리로는 이 재사용이 불가능하다.

## 재귀 CTE — 계층 데이터 탐색

재귀 CTE는 자기 자신을 참조하는 CTE다. 계층 구조 데이터(카테고리 트리, 조직도, 댓글 답글 구조)를 한 쿼리로 탐색할 수 있다.

```sql
-- 카테고리 테이블 (자기 참조)
-- categories: id, parent_id, name

-- 특정 카테고리의 모든 하위 카테고리를 재귀적으로 가져오기
WITH RECURSIVE category_tree AS (
    -- 앵커 부분: 시작점
    SELECT id, parent_id, name, 0 AS depth
    FROM categories
    WHERE id = 1  -- 루트 카테고리

    UNION ALL

    -- 재귀 부분: 앞에서 찾은 결과의 자식을 찾음
    SELECT c.id, c.parent_id, c.name, ct.depth + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT id, parent_id, name, depth
FROM category_tree
ORDER BY depth, id;
```

앵커 부분이 먼저 실행되어 id=1인 행이 들어오고, 재귀 부분이 그 행의 자식들을 찾고, 또 그 자식들의 자식을 찾는 과정을 반복한다. `depth`로 각 항목이 몇 단계 아래에 있는지 알 수 있다.

경로를 문자열로 누적하면 계층 구조의 전체 경로를 표현할 수도 있다.

```sql
WITH RECURSIVE category_path AS (
    SELECT id, name, CAST(name AS CHAR(1000)) AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name,
           CONCAT(cp.path, ' > ', c.name)
    FROM categories c
    INNER JOIN category_path cp ON c.parent_id = cp.id
)
SELECT id, name, path
FROM category_path;
```

### 재귀 CTE의 한계

재귀 CTE는 강력하다. 다만 조심해야 할 곳이 있다. 종료 조건이 없으면 무한 루프가 된다. MySQL은 `cte_max_recursion_depth` 변수로 기본 1000회로 제한하지만, 1000단계 깊이의 계층 트리가 있다면 이 제한에 걸린다.

더 중요한 것은 규모다. Egnyte의 사례를 보면 수십만 노드의 파일 시스템 트리를 재귀 CTE로 탐색했을 때 성능이 크게 떨어졌다. 깊이는 적당해도 너무 넓은 트리나, 수백만 건이 얽힌 그래프는 재귀 CTE로 처리하기 어렵다.

재귀 CTE가 잘 맞는 경우: 계층 깊이가 10~20단계 이하, 노드 수가 수만 이하. 그 이상이라면 계층 경로를 materialized path 패턴(`/1/2/5/` 같은 경로 문자열을 컬럼으로 저장)으로 저장하거나, 별도 계층 테이블을 관리하는 편이 낫다.

## 윈도우 함수 + CTE로 복합 보고서 작성하기

윈도우 함수와 CTE를 같이 쓰면 어떤 그림이 나올까. 보고서 쿼리에서 자주 보이는 패턴 하나를 따라가보자. 상품 카테고리별로 일별 매출을 집계하고, 각 카테고리 안에서 매출 순위를 매기는 쿼리다.

```sql
WITH daily_sales AS (
    SELECT
        p.category_id,
        DATE(o.created_at) AS order_date,
        SUM(oi.amount) AS daily_revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    WHERE o.status = 'COMPLETED'
      AND o.created_at >= '2024-01-01'
    GROUP BY p.category_id, DATE(o.created_at)
),
ranked_sales AS (
    SELECT
        category_id,
        order_date,
        daily_revenue,
        RANK() OVER (
            PARTITION BY category_id
            ORDER BY daily_revenue DESC
        ) AS revenue_rank,
        SUM(daily_revenue) OVER (
            PARTITION BY category_id
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue
    FROM daily_sales
)
SELECT *
FROM ranked_sales
WHERE revenue_rank <= 10  -- 카테고리별 매출 상위 10일
ORDER BY category_id, revenue_rank;
```

`daily_sales`에서 집계하고, `ranked_sales`에서 윈도우 함수를 적용해 순위와 누적 합계를 구한다. 마지막에 `WHERE revenue_rank <= 10`으로 각 카테고리에서 매출 상위 10일만 필터링한다.

윈도우 함수는 WHERE 절보다 나중에 실행된다는 점을 기억해두자. 그래서 윈도우 함수 결과로 필터링하려면 CTE나 서브쿼리로 한 번 감싸야 한다. `WHERE revenue_rank <= 10`을 직접 윈도우 함수와 같은 SELECT 수준에 쓰면 오류가 난다.

## 어디서 SQL로, 어디서 애플리케이션으로

윈도우 함수와 CTE로 꽤 많은 것을 SQL 안에서 처리할 수 있다는 걸 알았다. 그렇다면 항상 SQL에서 처리하는 것이 좋을까? 꼭 그렇지는 않다.

SQL에서 처리하는 편이 자연스러운 경우는 이렇다. 집계, 순위, 누적 합계처럼 데이터 전체나 그룹을 한 번에 봐야 하는 연산. 결과를 필터링하기 전에 계산이 먼저 필요한 경우(윈도우 함수는 WHERE보다 나중에 실행되니까). 정렬된 순서에 의존하는 연산(LAG/LEAD, 이동 평균). 네트워크를 통해 수십만 행을 옮기지 않아도 되는 경우.

그렇다면 반대편은 어떤 경우일까. 도메인 로직이 복잡하고 단위 테스트가 필요한 경우라면 애플리케이션 쪽이 더 명료하다. 여러 마이크로서비스의 데이터를 합쳐야 한다면 SQL 한쪽으로 몰 수 없다. SQL로 표현했을 때 지나치게 복잡해져 유지보수가 어려워진다면 애플리케이션이 떠맡는 편이 낫다.

기준은 결국 "DB가 더 잘 아는 일인가, 아니면 애플리케이션이 더 잘 아는 일인가"다. 집계와 순위는 DB가 잘 안다. 비즈니스 규칙 기반의 복잡한 계산은 애플리케이션이 자기 영역이다. 어느 한쪽이 항상 옳은 것이 아니라, 구조를 보고 판단해보자.

## 마무리

윈도우 함수(`ROW_NUMBER`, `LAG/LEAD`, `SUM OVER`)와 CTE(`WITH`, `WITH RECURSIVE`)는 8.0 이후 MySQL이 내놓은 가장 실용적인 기능들이다. 이걸 모르면 자바 코드에 쌓아두게 되는 집계 로직이, 이걸 알면 SQL 한 쿼리 안으로 들어온다.

다음 7장에서는 JSON 타입으로 넘어간다. 관계형 스키마로 표현하기 어려운 데이터를 JSON 컬럼에 넣었을 때 어떻게 인덱싱하고 조회하는지, 그리고 언제 JSON을 쓰고 언제 정규화 테이블을 쓰는지의 경계선을 같이 그어보자.

## 참고 자료

- MySQL :: 15.2.20 WITH (Common Table Expressions) — https://dev.mysql.com/doc/refman/8.0/en/with.html
- Percona — Introduction to MySQL 8.0 Recursive CTE (Part 2) — https://www.percona.com/blog/introduction-to-mysql-8-0-recursive-common-table-expression-part-2/
- Egnyte — Evaluating MySQL Recursive CTE at scale — https://www.egnyte.com/blog/post/12780evaluating-mysql-recursive-cte-at-scale/
