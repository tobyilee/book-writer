# 5장. EXPLAIN ANALYZE를 안에서 바깥으로 읽기

슬랙 알람이 울렸다. "결제 목록 API가 10초 넘게 걸려요." 담당 개발자가 열어보니 쿼리가 하나 있고, 그 쿼리는 지난 6개월 동안 아무도 건드리지 않았다. 데이터가 쌓인 것 외에 달라진 건 없다. 그런데 갑자기 10초다.

EXPLAIN을 실행해 본다. 뭔가 줄줄이 나오는데, 솔직히 어디서부터 읽어야 할지 모르겠다. `rows`가 크면 나쁜 건지, `key`가 NULL이면 다 느린 건지, `Extra`에 `Using filesort`가 보이면 무조건 인덱스를 추가해야 하는 건지. 아는 것 같으면서도 막상 실제 쿼리 앞에서는 손이 멈춘다. 이 찜찜함은 꽤 보편적이다.

EXPLAIN과 EXPLAIN ANALYZE의 차이부터 시작해 실제 슬로우 쿼리 한 건을 처음부터 끝까지 분해해 보자. 목표는 하나다 — 다음번에 슬랙 알람이 울렸을 때 혼자 손을 댈 수 있는 절차를 손에 쥐는 것.

## EXPLAIN과 EXPLAIN ANALYZE — 추정과 현실 사이

MySQL의 EXPLAIN은 오래전부터 있었다. 쿼리 앞에 `EXPLAIN`을 붙이면 옵티마이저가 어떤 실행 계획을 선택했는지를 보여주는데, 여기서 나오는 숫자들 — `rows`, `filtered`, `key_len` 같은 것들 — 은 모두 *추정값*이다. 옵티마이저가 통계 정보를 보고 계산한 예측이지, 실제로 쿼리를 실행해서 나온 측정값이 아니다.

EXPLAIN ANALYZE는 다르다. 8.0.18부터 추가된 이 명령은 쿼리를 *실제로 실행*하면서 각 노드의 소요 시간과 실제 처리 행 수를 함께 수집한다. 출력 형태도 달라진다. EXPLAIN FORMAT=TREE처럼 들여쓰기 된 트리 구조로 나오고, 각 노드마다 두 쌍의 숫자가 붙는다.

```sql
-- EXPLAIN ANALYZE 기본 사용법
EXPLAIN ANALYZE
SELECT o.id, o.amount, u.name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'COMPLETED'
  AND o.created_at >= '2024-01-01'
ORDER BY o.created_at DESC
LIMIT 50;
```

출력에서 각 노드 옆에 붙는 숫자 패턴은 이렇게 생겼다.

```
-> Nested loop inner join  (cost=1234.56 rows=500)
                           (actual time=0.123..45.678 rows=48 loops=1)
```

괄호 두 개가 핵심이다. 첫 번째 괄호 `(cost=... rows=...)` 는 옵티마이저의 추정치고, 두 번째 괄호 `(actual time=0.123..45.678 rows=48 loops=1)` 는 실제 측정값이다. `actual time`의 두 숫자는 '첫 번째 행을 꺼내기까지 걸린 시간'과 '마지막 행까지 전부 처리한 시간'이다. 이 두 값의 차이가 크다면 그 노드가 스트리밍으로 처리되지 않고 중간 어딘가에서 전체 결과를 모아야 했다는 신호다.

## 트리를 안에서 바깥으로 읽는 법

EXPLAIN ANALYZE 트리를 처음 보면 흔히 빠지는 실수가 있다. 위에서 아래로, 즉 바깥 노드부터 읽는 것이다. 이렇게 읽으면 전체적인 실행 흐름은 이해할 수 있지만 "어디서 시간이 가장 많이 쓰였는가"를 파악하기 어렵다.

MySQL의 실행 트리는 안쪽 노드가 먼저 실행된다. 가장 깊이 들여쓰인 노드가 가장 먼저 데이터를 가져오고, 그 결과가 바깥 노드로 올라간다. 마치 함수 호출 스택처럼 — 안쪽이 호출되고, 그 결과가 바깥으로 돌아온다. 그래서 슬로우 쿼리의 원인을 찾으려면 가장 안쪽(들여쓰기가 가장 깊은) 노드부터 읽어야 한다.

예를 들어 이런 트리가 있다고 해보자.

```
-> Limit: 50 row(s)
   (actual time=234.56..234.67 rows=50 loops=1)
    -> Sort: orders.created_at DESC
       (actual time=234.44..234.52 rows=50 loops=1)
        -> Filter: (orders.status = 'COMPLETED')
           (actual time=0.08..233.91 rows=50 loops=1)
            -> Table scan on orders
               (actual time=0.07..180.23 rows=1000000 loops=1)
```

바깥에서 읽으면 `Limit → Sort → Filter → Table scan` 순서처럼 보이지만, 실제 실행은 반대다. `Table scan on orders`가 먼저 실행되어 100만 개 행을 하나씩 꺼내고, 그게 올라와서 `Filter`를 통과하고, 그 다음 `Sort`로 정렬되고, 마지막에 50개를 잘라낸다.

`actual time`을 보면 더 명확하다. `Table scan on orders`에서 이미 180.23ms를 쓰고 있다. 100만 행을 풀스캔하고 있는 것이다. 여기에 인덱스를 추가하거나, 필터 조건을 인덱스가 담당하게 만들어보자.

이 읽는 순서를 몸에 익히는 가장 쉬운 방법은 "들여쓰기가 가장 깊은 곳의 actual time을 먼저 확인하고, 거기서 위로 올라오면서 숫자가 어디서 커지는지 따라가는 것"이다. 시간이 크게 늘어나는 전환점이 병목이다.

## 추정치와 실측치의 괴리 — 통계가 오래됐을 때

EXPLAIN과 EXPLAIN ANALYZE의 숫자가 크게 다를 때가 있다. 추정은 500행인데 실제로는 50만 행을 처리한다든가. 이런 괴리가 생기는 원인은 대부분 *통계 정보가 오래됐거나 부정확*하기 때문이다.

MySQL의 옵티마이저는 테이블의 행 수 분포, 각 컬럼의 값 분포 같은 통계 정보를 보고 cost를 추정한다. 그런데 데이터가 빠르게 쌓이는 테이블은 통계가 실제 분포를 따라잡지 못할 때가 있다. 예를 들어 한 달 전 데이터로 통계를 만들었는데 그 이후 1000만 행이 들어온 경우다.

이때 시도해볼 첫 번째 수단이 `ANALYZE TABLE`이다.

```sql
-- 통계 갱신
ANALYZE TABLE orders;

-- 특정 컬럼에 히스토그램 생성 (8.0 이상)
ANALYZE TABLE orders UPDATE HISTOGRAM ON status, created_at;
```

8.0부터는 히스토그램 통계가 추가됐다. 인덱스가 없는 컬럼에 대해서도 값의 분포를 별도 통계로 관리할 수 있어, 옵티마이저가 더 정확한 cost 추정을 할 수 있게 됐다. `status` 컬럼처럼 카디널리티가 낮지만 특정 값이 압도적으로 많은 경우 — 예를 들어 전체 주문의 95%가 `COMPLETED`인 상황 — 에 히스토그램이 빛을 발한다.

히스토그램을 만들어도 여전히 추정치와 실측치 사이의 차이가 크다면, 더 깊은 곳을 봐야 한다. `optimizer_trace`를 켜면 옵티마이저가 어떤 플랜을 고려했고, 각각의 cost를 어떻게 계산했는지를 JSON 형태로 볼 수 있다.

```sql
-- optimizer_trace 켜기
SET SESSION optimizer_trace = 'enabled=on';
SET SESSION optimizer_trace_max_mem_size = 1000000;

-- 분석할 쿼리 실행
SELECT o.id, o.amount
FROM orders o
WHERE o.status = 'COMPLETED'
  AND o.created_at >= '2024-01-01';

-- 트레이스 확인
SELECT * FROM INFORMATION_SCHEMA.OPTIMIZER_TRACE\G

-- 끄기
SET SESSION optimizer_trace = 'enabled=off';
```

optimizer_trace 출력은 길고 복잡하지만, 핵심은 `considered_execution_plans` 섹션이다. 옵티마이저가 검토한 플랜과 각각의 `cost_info`를 보면 왜 특정 인덱스를 택했는지, 혹은 왜 인덱스를 버리고 풀스캔을 선택했는지를 알 수 있다.

## 인덱스가 안 쓰이는 세 가지 원인

EXPLAIN을 봤더니 `key: NULL`이다. 인덱스가 분명히 존재하는데 쓰이지 않는다. 난감한 상황이다. 원인은 크게 세 가지다.

**첫째, leftmost prefix rule 위반.** 복합 인덱스 `(status, created_at, amount)` 가 있다고 할 때, `WHERE created_at >= '2024-01-01'`만으로는 이 인덱스를 쓸 수 없다. 인덱스는 왼쪽 컬럼부터 순서대로 써야 한다. `status`를 먼저 걸어야 `created_at`을 이어서 쓸 수 있다. 4장에서 다뤘지만 인덱스 설계 실수 중 가장 흔한 패턴이라 여기서도 마주친다.

```sql
-- 인덱스 (status, created_at)가 있을 때

-- 이 쿼리는 인덱스를 쓴다 (leftmost prefix OK)
SELECT * FROM orders WHERE status = 'COMPLETED' AND created_at >= '2024-01-01';

-- 이 쿼리는 인덱스를 못 쓴다 (created_at만 조건에 있음)
SELECT * FROM orders WHERE created_at >= '2024-01-01';
```

**둘째, 컬럼에 함수를 적용한 경우.** 인덱스는 컬럼의 원래 값을 기준으로 만들어진다. 컬럼을 변환하면 인덱스를 쓸 수 없다.

```sql
-- 인덱스를 쓰지 못하는 패턴들
SELECT * FROM orders WHERE YEAR(created_at) = 2024;
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
SELECT * FROM orders WHERE LOWER(user_email) = 'user@example.com';

-- 대신 이렇게 — 컬럼에 함수 없이 범위 조건으로
SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

JPA를 쓰면서 JPQL에 `FUNCTION('YEAR', o.createdAt) = :year` 같은 표현을 넣는 경우를 종종 본다. 그럴 때 실제로 생성되는 SQL이 인덱스를 날리고 있는지 확인하는 편이 낫다.

**셋째, 옵티마이저의 cost 오추정.** 인덱스가 있고, leftmost prefix도 맞고, 함수도 없는데 여전히 인덱스를 안 쓰는 경우다. 옵티마이저가 "인덱스를 쓰는 것보다 풀스캔이 더 빠를 것"이라고 추정하는 상황이다. 이건 틀린 추정일 때도 있다. 통계가 부정확하거나, 인덱스 선택성(selectivity)을 옵티마이저가 잘못 파악할 때 발생한다. 앞서 말한 히스토그램 갱신을 먼저 시도하고, 그래도 나아지지 않으면 `USE INDEX`, `FORCE INDEX` 힌트를 단기 우회책으로 쓸 수 있다. 다만 이건 통계 문제를 근본적으로 해결하지 않는다는 점을 기억해두자.

```sql
-- 인덱스 힌트 (통계 문제가 해결되면 제거하는 편이 좋다)
SELECT * FROM orders USE INDEX (idx_status_created)
WHERE status = 'COMPLETED' AND created_at >= '2024-01-01';
```

## `Using filesort`와 `Using temporary` — 이 신호가 보이면

EXPLAIN의 Extra 컬럼에 `Using filesort`가 나왔다고 해서 무조건 성능이 나쁜 것은 아니다. 단지 MySQL이 결과를 정렬할 때 인덱스의 순서를 그대로 활용하지 못하고 별도의 정렬 작업을 했다는 뜻이다. 정렬 대상이 몇 천 건이라면 `Using filesort`가 있어도 빠를 수 있다.

`Using temporary`는 조금 더 주의를 기울여야 한다. 내부 임시 테이블을 만들어서 중간 결과를 쌓았다는 의미다. `GROUP BY`나 `DISTINCT`, 또는 `ORDER BY`가 들어간 쿼리에서 자주 나온다. 임시 테이블이 메모리 안에 들어가면 그나마 빠르지만, 결과가 커서 디스크 임시 테이블이 만들어지면 갑자기 느려진다.

이 둘이 함께 보이고 `actual time`이 크다면 어떻게 볼까. 대부분의 경우 두 가지를 점검한다.

하나, ORDER BY 컬럼이 인덱스 안에 있는가. ORDER BY에 사용되는 컬럼이 인덱스에 포함되어 있고, WHERE 조건이 그 인덱스를 통해 접근한다면 `Using filesort` 없이 정렬 결과를 낼 수 있다.

```sql
-- 인덱스 (status, created_at)가 있을 때
-- 이 쿼리는 정렬도 인덱스로 처리 가능 (extra: Using index condition)
SELECT id, amount FROM orders
WHERE status = 'COMPLETED'
ORDER BY created_at DESC
LIMIT 50;

-- 반면 이 쿼리는 정렬을 인덱스로 처리 못 함 (status로 걸러낸 뒤 amount로 정렬)
SELECT id, amount FROM orders
WHERE status = 'COMPLETED'
ORDER BY amount DESC
LIMIT 50;
```

둘, GROUP BY 컬럼이 인덱스에 있는가. MySQL은 GROUP BY 컬럼이 인덱스 순서와 일치하면 임시 테이블 없이 처리할 수 있다.

EXPLAIN ANALYZE의 트리에서 `Sort` 노드나 `Aggregate using temporary table` 노드가 안쪽에서 가장 시간을 많이 잡아먹고 있다면, 인덱스 재설계나 커버링 인덱스를 고민할 차례다.

## 커버링 인덱스로 back-to-table을 없애자

`Using index`가 EXPLAIN Extra에 보이면 기뻐할 일이다. 이것은 쿼리가 인덱스만으로 결과를 낼 수 있어서 테이블을 건드리지 않았다는 뜻, 즉 커버링 인덱스가 작동한 것이다.

세컨더리 인덱스는 PK 값을 포인터로 가지고 있다. 인덱스에서 조건에 맞는 PK를 찾고, 다시 그 PK로 테이블(클러스터링 인덱스)을 조회하는 것이 일반적인 흐름이다. 이것이 'back-to-table(또는 double lookup)'이라고도 부르는 과정이다. 조건에 맞는 행이 수백만 개라면 이 왕복 조회가 큰 부담이 된다.

SELECT하는 컬럼들이 인덱스 안에 모두 들어있다면 back-to-table이 필요 없다. 인덱스에서 조건 검색, 거기서 바로 값을 꺼내 반환.

```sql
-- 인덱스 (status, created_at, id) 가 있다면
-- id, created_at만 SELECT하는 이 쿼리는 커버링 인덱스로 처리 가능
-- Extra: Using index
SELECT id, created_at
FROM orders
WHERE status = 'COMPLETED'
  AND created_at >= '2024-01-01'
ORDER BY created_at DESC
LIMIT 50;

-- amount를 추가하면 인덱스에 없으므로 back-to-table 발생
SELECT id, created_at, amount
FROM orders
WHERE status = 'COMPLETED'
  AND created_at >= '2024-01-01'
ORDER BY created_at DESC
LIMIT 50;
```

페이지네이션을 구현할 때는 커버링 인덱스 + 지연 조인(deferred join) 기법을 시도해보자. 커버링 인덱스로 PK만 빠르게 찾은 뒤, 그 PK들에 대해서만 전체 컬럼 조회를 하는 방식이다.

```sql
-- 지연 조인으로 페이지네이션 최적화
SELECT o.id, o.amount, o.user_id, o.created_at
FROM orders o
INNER JOIN (
    SELECT id FROM orders
    WHERE status = 'COMPLETED'
      AND created_at >= '2024-01-01'
    ORDER BY created_at DESC
    LIMIT 50 OFFSET 10000  -- 깊은 페이지
) sub ON o.id = sub.id;
```

서브쿼리 부분은 커버링 인덱스로 빠르게 50개 ID를 찾고, 바깥 조인에서 그 50개에 대해서만 전체 컬럼 조회를 한다. OFFSET 페이지네이션 자체의 한계(깊어질수록 느려지는)는 9장에서 keyset pagination으로 더 근본적인 해법을 본다.

## 실제 슬로우 쿼리 분해 — 처음부터 끝까지

이제 실전 시나리오를 하나 따라가보자. velog에 올라온 슬로우 쿼리 개선 사례를 재구성해 본 것이다.

**상황:** 이벤트 목록 페이지가 갑자기 느려졌다. 쿼리는 이렇게 생겼다.

```sql
-- 문제의 쿼리 (실행 시간 약 6초)
SELECT p.id, p.title, p.discount_rate, po.option_name
FROM promotions p
LEFT JOIN promotion_options po ON p.id = po.promotion_id
WHERE p.is_active = 1
  AND p.end_date >= NOW()
ORDER BY p.created_at DESC
LIMIT 20;
```

**1단계: EXPLAIN ANALYZE 실행**

```sql
EXPLAIN ANALYZE
SELECT p.id, p.title, p.discount_rate, po.option_name
FROM promotions p
LEFT JOIN promotion_options po ON p.id = po.promotion_id
WHERE p.is_active = 1
  AND p.end_date >= NOW()
ORDER BY p.created_at DESC
LIMIT 20\G
```

결과(재구성):

```
-> Limit: 20 row(s)
   (actual time=6123.45..6123.52 rows=20 loops=1)
    -> Sort: p.created_at DESC
       (actual time=6123.23..6123.38 rows=20 loops=1)
        -> Filter: ((p.is_active = 1) and (p.end_date >= now()))
           (actual time=0.15..6120.78 rows=2340 loops=1)
            -> Left hash join (po.promotion_id = p.id)
               (actual time=0.14..5890.34 rows=125000 loops=1)
                -> Table scan on p
                   (cost=2345 rows=45000) (actual time=0.09..23.45 rows=45000 loops=1)
                -> Hash
                    -> Table scan on po
                       (cost=12340 rows=890000) (actual time=0.07..987.23 rows=890000 loops=1)
```

**2단계: 안쪽부터 읽기**

가장 안쪽 노드 두 개를 본다.

- `Table scan on p` — promotions 테이블 풀스캔, 45,000행, 23ms
- `Table scan on po` — promotion_options 테이블 풀스캔, 89만 행, 987ms

promotion_options가 89만 행 풀스캔이다. 여기서 시간이 상당히 간다. 그다음 `Left hash join`에서 두 테이블을 합치면서 125,000행이 되고, 이 처리에 5.8초를 쓴다.

**3단계: 인덱스 확인**

```sql
SHOW INDEX FROM promotion_options;
```

결과를 보니 promotion_options 테이블에는 `id`(PK) 인덱스만 있고 `promotion_id`에는 인덱스가 없다. JOIN 조건 `po.promotion_id = p.id`에서 `po.promotion_id`를 검색해야 하는데 인덱스가 없으니 매번 풀스캔이 일어난다.

**4단계: 인덱스 추가**

```sql
ALTER TABLE promotion_options
ADD INDEX idx_promotion_id (promotion_id);
```

**5단계: 다시 EXPLAIN ANALYZE**

```
-> Limit: 20 row(s)
   (actual time=0.45..0.52 rows=20 loops=1)
    -> Nested loop left join
       (actual time=0.43..0.50 rows=20 loops=1)
        -> Filter: ...
           (actual time=0.12..0.31 rows=20 loops=1)
            -> Index range scan on p using idx_active_enddate
               (actual time=0.09..0.24 rows=20 loops=1)
        -> Index lookup on po using idx_promotion_id (promotion_id=p.id)
           (actual time=0.008..0.009 rows=3 loops=20)
```

6초에서 0.5초로 줄었다. `Table scan on po`가 `Index lookup on po`로 바뀌었고, `Left hash join`이 `Nested loop left join`으로 바뀌었다.

**6단계: promotions 테이블의 인덱스도 확인**

0.5초도 여전히 빠르지는 않다. promotions 테이블의 `is_active`, `end_date`, `created_at` 컬럼에 인덱스가 있는지 확인해보자. `WHERE is_active = 1 AND end_date >= NOW()`로 걸러지는 비율이 높다면 복합 인덱스를 추가할 수 있다.

```sql
-- 복합 인덱스 추가
ALTER TABLE promotions
ADD INDEX idx_active_end_created (is_active, end_date, created_at);
```

이렇게 하면 `is_active = 1 AND end_date >= NOW()`를 인덱스로 처리하고, `ORDER BY created_at DESC`도 인덱스 순서를 따라갈 수 있다. 다시 EXPLAIN ANALYZE를 실행해서 `Using filesort`가 없어졌는지, actual time이 줄었는지 확인하자.

이 사이클 — **슬로우 쿼리 발견 → EXPLAIN ANALYZE로 분해 → 안쪽 노드부터 병목 찾기 → 인덱스/통계 수정 → 재검증** — 이 기본 패턴이다. 한 번 손에 익히면 어떤 쿼리 앞에서도 막히지 않는다.

## estimate와 actual이 크게 다를 때 — 다시 히스토그램으로

한 가지 더 보고 가자. 인덱스를 추가했는데도 여전히 느리고, EXPLAIN ANALYZE를 보니 `rows=500`으로 추정했는데 actual은 `rows=500000`이다. 이렇게 10배, 100배 차이가 나면 통계 문제다.

`status` 같은 컬럼이 이런 상황을 만들기 쉽다. `COMPLETED`, `PENDING`, `CANCELLED` 세 값이 있는데, 데이터의 99%가 `COMPLETED`다. 인덱스 통계만으로는 이 분포를 잘 담지 못할 수 있다.

```sql
-- 히스토그램 생성
ANALYZE TABLE orders UPDATE HISTOGRAM ON status WITH 3 BUCKETS;

-- 히스토그램 확인
SELECT * FROM INFORMATION_SCHEMA.COLUMN_STATISTICS
WHERE TABLE_NAME = 'orders' AND COLUMN_NAME = 'status'\G
```

히스토그램을 만들고 나면 옵티마이저가 `status = 'COMPLETED'`가 99%에 해당한다는 것을 알게 되어, 그 인덱스를 쓰는 것보다 풀스캔이 낫다고 판단하거나 반대로 더 적합한 인덱스를 선택하게 된다.

히스토그램은 인덱스와 달리 DML 성능에 영향을 주지 않는다. 읽기 전용 통계 테이블이기 때문에 자주 갱신해도 부담이 없다. 분포가 치우친 컬럼, 또는 카디널리티가 낮지만 특정 값이 집중된 컬럼에 히스토그램을 추가해두는 편이 낫다.

## 마무리

EXPLAIN ANALYZE는 쿼리 성능 문제의 진단 도구다. 핵심 절차를 정리해두자.

안쪽 노드부터 actual time과 actual rows를 확인하자. estimate와 actual의 차이가 크면 통계를 다시 갱신하거나 히스토그램을 만들어보자. 인덱스가 안 쓰인다면 leftmost prefix 위반, 함수 적용, cost 오추정 세 가지를 순서대로 의심한다. `Using filesort`나 `Using temporary`가 있고 실행 시간이 크다면 ORDER BY와 GROUP BY에 인덱스가 어떻게 걸려 있는지 다시 들여다보자.

진단 도구를 쓸 줄 아는 것과 실제로 쓰는 것 사이에는 습관의 차이가 있다. 슬로우 쿼리가 발생했을 때 바로 EXPLAIN ANALYZE를 실행하는 것을 팀의 기본 절차로 만들어두는 편이 낫다.

6장에서는 이렇게 진단하고 최적화한 쿼리를 SQL 자체의 표현력을 높이는 방향으로 가져가 본다. 윈도우 함수와 CTE로 애플리케이션 레이어에서 처리하던 집계 로직을 SQL 안으로 끌어올리는 방법을 같이 살펴보자.

## 참고 자료

- MySQL :: EXPLAIN ANALYZE 블로그 아카이브 — https://dev.mysql.com/blog-archive/mysql-explain-analyze/
- MySQL :: Histogram statistics in MySQL — https://dev.mysql.com/blog-archive/histogram-statistics-in-mysql/
- MySQL :: 10.9.6 Optimizer Statistics — https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html
- velog "EXPLAIN ANALYZE 해석법" — https://velog.io/@wisepine/MySQL-%EC%8A%AC%EB%A1%9C%EC%9A%B0%EC%BF%BC%EB%A6%AC-%EC%9E%A1%EB%8A%94-%EB%AA%85%EB%A0%B9%EC%96%B4-EXPLAIN-ANALIZE-%ED%95%B4%EC%84%9D%EB%B2%95
- velog "슬로우 쿼리 개선기" — https://velog.io/@bruni_23yong/%EC%8A%AC%EB%A1%9C%EC%9A%B0-%EC%BF%BC%EB%A6%AC-%EA%B0%9C%EC%84%A0%EA%B8%B0
- Alibaba Cloud — Analysis of MySQL Cost Estimator — https://www.alibabacloud.com/blog/analysis-of-mysql-cost-estimator_601201
