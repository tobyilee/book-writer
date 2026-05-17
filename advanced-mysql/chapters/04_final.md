# 4장. 인덱스 설계는 데이터 구조 설계다

velog의 한 개발자가 남긴 후기를 보자. `promotion_option` 테이블의 `promotion_id` 컬럼에 인덱스가 없었다. LEFT JOIN을 할 때마다 그 테이블을 풀 스캔했다. 쿼리 실행 시간: 6초. 인덱스 하나 추가했다. 실행 시간: 0.02초. 300배 차이다.

OKKY에도 비슷한 이야기가 있다. 이번엔 인덱스가 아예 없었던 게 아니라 복합 인덱스의 컬럼 순서가 문제였다. 순서를 바꿨더니 11초에서 0.1초로 줄었다.

인덱스 하나, 컬럼 순서 하나. 그런데 그 차이가 300배, 110배다. 왜 그럴까. 인덱스가 어떤 자료 구조이고, 어떤 원리로 쿼리를 빠르게 만드는지를 이해하면 이 질문에 답할 수 있다. 그리고 "이 쿼리에는 어떤 인덱스를 걸어야 하는가"를 직관으로 판단할 수 있게 된다.

## 클러스터링 인덱스: 테이블 자체가 인덱스다

2장에서 봤던 그림을 다시 꺼내자. InnoDB에서 테이블은 PK 기준으로 정렬된 B+Tree 그 자체다. 테이블을 저장하는 방식이 클러스터링 인덱스다. 테이블과 클러스터링 인덱스는 별개가 아니다 — 하나다.

이것이 왜 중요한가. PK로 row를 찾는 것은 B+Tree를 딱 한 번 타고 내려가는 것이다. 루트에서 리프까지. 리프 노드에 실제 row 데이터가 있다. 그 이상의 비용이 없다.

```
PK 조회:
  클러스터링 인덱스 B+Tree
  루트 → 내부 노드 → 내부 노드 → 리프 노드(row 데이터 있음)
  = 1회 B+Tree 탐색으로 데이터 획득
```

PK가 없는 테이블은 어떻게 되는가. InnoDB는 PK가 없으면 NOT NULL인 unique 인덱스를 클러스터링 인덱스로 쓴다. 그것도 없으면 내부적으로 숨겨진 6바이트 row ID를 생성해 클러스터링 인덱스로 사용한다. 이 숨겨진 row ID는 개발자가 접근할 수 없어 JOIN 조건 등에 쓸 수 없다. 그래서 **모든 InnoDB 테이블에는 PK를 명시적으로 정의하는 것이 좋다.**

### PK 선택이 쓰기 성능을 결정한다

PK 값이 무작위(UUID 같은)이면 새 row를 삽입할 때마다 B+Tree의 임의의 위치에 넣어야 한다. 그 위치의 리프 페이지가 꽉 찼다면 페이지를 두 개로 나눈다 — 이게 **page split**이다. 페이지 분열은 새 페이지 할당, 기존 페이지 이동, 상위 노드 업데이트를 포함하는 비용 있는 작업이다. UUID를 PK로 쓰면 이 page split이 빈번하게 일어난다.

auto_increment PK는 항상 맨 끝에 추가된다. B+Tree의 오른쪽 끝 리프 노드에만 삽입된다. page split이 거의 없다. 순차 쓰기는 InnoDB에게 가장 효율적인 패턴이다.

그렇다면 UUID를 전혀 쓰면 안 되는가. 그건 아니다. UUID를 애플리케이션에서 외부 식별자로 쓰되, 실제 PK는 auto_increment로 하고 UUID는 별도 unique 컬럼으로 두는 방식도 많이 쓰인다. ULID나 UUIDv7처럼 시간 순서로 정렬되는 UUID 변형을 쓰면 page split을 상당히 줄일 수 있다. 8장에서 PK 전략을 더 깊이 다룰 것이다.

JPA 엔티티에서는 PK 전략을 어노테이션 한 줄로 표현한다. 어느 쪽을 고르는지가 쓰기 성능을 정한다는 점을 기억해두자.

```java
@Entity
public class Order {
    // 권장: auto_increment 기반 — 순차 삽입으로 page split 최소화
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 외부 식별자가 필요하다면 별도 unique 컬럼으로
    @Column(unique = true, updatable = false, nullable = false)
    private String publicId; // UUID 또는 ULID
}
```

## 세컨더리 인덱스: back-to-table과 그 비용

PK 외의 모든 인덱스가 세컨더리 인덱스다. 세컨더리 인덱스의 리프 노드에는 (인덱스 키, PK) 쌍이 저장된다. PK가 포함되는 이유는 클러스터링 인덱스로 가는 포인터가 필요하기 때문이다.

`SELECT * FROM orders WHERE email = 'user@example.com'`을 실행한다고 해보자. `email` 컬럼에 세컨더리 인덱스가 있다면:

1. 세컨더리 인덱스 B+Tree에서 `email = 'user@example.com'`을 찾는다
2. 거기서 PK 값을 꺼낸다 (예: id = 42)
3. 클러스터링 인덱스 B+Tree에서 id = 42를 찾는다
4. 리프 노드에서 전체 row 데이터를 읽는다

```
세컨더리 인덱스 조회:
  세컨더리 인덱스 B+Tree: email → PK 획득
                           ↓
  클러스터링 인덱스 B+Tree: PK → row 데이터
  = 2회 B+Tree 탐색
```

3번 단계가 **back-to-table**(테이블로 돌아가기, 또는 PK 룩업)이다. 세컨더리 인덱스 조회에는 항상 이 추가 비용이 따른다. `EXPLAIN`의 `type` 컬럼이 `ref`나 `range`로 나오지만 Extra에 `Using index`가 없다면, back-to-table이 일어나고 있다는 뜻이다.

back-to-table 비용이 큰 경우는 주로 range scan으로 많은 row를 읽을 때다. row 수가 많을수록 클러스터링 인덱스를 그만큼 더 많이 찌른다. 이 때문에 옵티마이저가 세컨더리 인덱스 대신 풀 테이블 스캔을 선택하는 경우도 있다 — "인덱스를 쓰나 테이블을 다 뒤지나 비용이 비슷하거나, 어차피 많이 읽어야 하면 순차 스캔이 더 빠를 수 있다"고 판단할 때다.

이 back-to-table을 없애는 방법이 커버링 인덱스다.

## 복합 인덱스: 순서가 운명이다

OKKY 사례의 핵심이 여기서 풀린다. 같은 컬럼으로 복합 인덱스를 만들었는데, 컬럼 순서를 바꿨더니 11초가 0.1초가 됐다.

복합 인덱스(Composite Index)는 여러 컬럼을 하나의 인덱스로 묶은 것이다. `(a, b, c)` 복합 인덱스라고 하면 이 인덱스의 B+Tree는 (a, b, c) 값의 조합을 키로 정렬되어 있다.

### Leftmost Prefix Rule

복합 인덱스 `(a, b, c)`가 활용되는 조건은 **leftmost prefix**다.

```
(a, b, c) 복합 인덱스가 사용되는 쿼리:
  WHERE a = ?                    → 사용 가능
  WHERE a = ? AND b = ?          → 사용 가능
  WHERE a = ? AND b = ? AND c = ? → 사용 가능
  WHERE a = ? AND c = ?          → a 부분만 사용, c는 인덱스 미사용
  WHERE b = ?                    → 사용 불가
  WHERE b = ? AND c = ?          → 사용 불가
```

왜 그런가. 인덱스 B+Tree는 (a, b, c) 순서로 정렬되어 있다. `a`로 먼저 정렬되고, 같은 `a` 값 안에서 `b`로 정렬되고, 같은 `(a, b)` 값 안에서 `c`로 정렬된다. `WHERE b = ?` 조건은 첫 번째 정렬 키 `a`를 건너뛰기 때문에 이 정렬된 구조를 활용할 수 없다.

```
[ (a, b, c) 인덱스의 정렬 ]

a=1, b=2, c=10
a=1, b=2, c=20
a=1, b=3, c=5
a=2, b=1, c=8
a=2, b=2, c=15
...

WHERE b = 2: b가 2인 것이 연속하지 않아서 B+Tree 탐색 불가
WHERE a = 1: a=1인 부분이 연속해 있어서 B+Tree 탐색 가능
```

### Equality → Range → Sort 순서 휴리스틱

복합 인덱스를 설계할 때 컬럼 순서는 어떻게 정해야 하는가. 기본 원칙은 **equality 조건 먼저, range 조건은 그다음, sort 컬럼은 마지막**이다.

쿼리가 `WHERE status = 'PAID' AND created_at > '2024-01-01' ORDER BY created_at`라면:

- `status`: equality (`=`)
- `created_at`: range (`>`) + sort

인덱스 순서는 `(status, created_at)`이 좋다. `status`로 좁힌 다음, `created_at`으로 range scan하면서 정렬까지 처리할 수 있다.

`(created_at, status)`로 하면 어떻게 되는가. `created_at > '2024-01-01'` range로 먼저 좁힌 뒤, 그 안에서 `status = 'PAID'`를 필터링해야 한다. range 이후의 컬럼은 인덱스 탐색이 아니라 필터링이 되므로, 더 많은 레코드를 읽고 버린다.

equality가 여러 개라면 **카디널리티(cardinality, 값의 종류 수)가 높은 것을 앞에** 두는 것이 좋다. `gender (M/F, 카디널리티 2)`보다 `user_id (카디널리티 수천만)`이 먼저 오면 더 잘 좁혀진다.

```
[ Leftmost Prefix와 인덱스 활용 시각화 ]

인덱스: (status, created_at)

쿼리: WHERE status = 'PAID' AND created_at > '2024-01-01'

B+Tree 탐색:
  └─ status = 'PAID' 구간으로 이동
       └─ created_at > '2024-01-01' 범위 스캔
          (인덱스 순방향 스캔 → Using index range)

쿼리: WHERE created_at > '2024-01-01'
  → status 없이 created_at만으로는 위 인덱스 활용 불가
  → 인덱스가 있다면 (created_at) 단독 인덱스가 필요
```

이것이 OKKY 사례의 핵심이었다. 조건 컬럼의 순서가 맞지 않은 복합 인덱스는 효과를 낼 수 없다.

## 커버링 인덱스: back-to-table을 없애자

**커버링 인덱스(Covering Index)**는 쿼리가 필요로 하는 모든 컬럼이 인덱스 안에 들어 있어서, 클러스터링 인덱스(테이블)로 돌아갈 필요가 없는 인덱스다.

```sql
-- users 테이블에 (email) 인덱스가 있다
-- 이 쿼리는 back-to-table 발생
SELECT id, name, email FROM users WHERE email = 'user@example.com';
-- → 세컨더리 인덱스에서 email → PK, 다시 클러스터링 인덱스에서 name 읽기

-- (email, name) 복합 인덱스가 있다
-- 이 쿼리는 커버링 인덱스
SELECT id, name FROM users WHERE email = 'user@example.com';
-- → 세컨더리 인덱스에서 email → (name, PK) 모두 읽기 가능
-- → 클러스터링 인덱스로 돌아갈 필요 없음
```

`EXPLAIN`의 Extra 컬럼에 `Using index`가 나오면 커버링 인덱스가 작동하고 있다는 뜻이다.

커버링 인덱스는 특히 range scan이나 집계 쿼리에서 효과가 크다. 수만 건을 읽어야 하는 range scan에서 back-to-table이 없다는 것은, 수만 번의 클러스터링 인덱스 조회를 하지 않아도 된다는 뜻이다.

커버링 인덱스를 설계할 때는 SELECT 컬럼 목록도 같이 고려해야 한다. "이 쿼리에서 어떤 컬럼이 필요한가"를 확인한 뒤, 그 컬럼들을 모두 인덱스에 포함시킨다.

주의할 점: 인덱스에 포함하는 컬럼이 많아질수록 인덱스 크기가 커지고, INSERT/UPDATE 시 인덱스 업데이트 비용도 증가한다. 트레이드오프를 고려해야 한다.

## 프리픽스·Descending·Functional 인덱스

### 프리픽스 인덱스

VARCHAR나 TEXT 컬럼 전체를 인덱스로 만들면 인덱스 크기가 커진다. 앞 N바이트만 인덱스로 만드는 것이 **프리픽스 인덱스**다.

```sql
CREATE INDEX idx_email_prefix ON users (email(20));
```

장점은 인덱스 크기가 줄어들고, 쓰기 비용이 낮아진다는 것이다. 단점은 카디널리티가 낮아진다는 것이다. 이메일 앞 20자만 인덱스에 있으면, 앞 20자가 같은 이메일들이 인덱스에서 같아 보인다. 커버링 인덱스로 쓸 수 없다 — 실제 값이 인덱스에 완전히 없기 때문에 항상 back-to-table이 필요하다.

긴 텍스트 컬럼에 인덱스가 필요할 때는 적절한 prefix 길이를 찾는 것이 중요하다. `COUNT(DISTINCT LEFT(email, N))` / `COUNT(DISTINCT email)`로 N별 카디널리티 비율을 확인하고, 적절한 N을 찾자.

### Descending 인덱스

8.0부터 지원한다. `ORDER BY a ASC, b DESC` 같이 혼합 정렬을 인덱스로 처리할 수 있다.

```sql
-- (created_at DESC, id DESC) 인덱스 생성
CREATE INDEX idx_created_desc ON orders (created_at DESC, id DESC);

-- 이 쿼리는 Using filesort 없이 인덱스 스캔으로 처리
SELECT * FROM orders ORDER BY created_at DESC, id DESC LIMIT 10;
```

5.7에서는 이런 혼합 정렬을 인덱스로 처리할 수 없어 `Using filesort`가 발생했다. 8.0부터 가능해졌다. 카카오 기술 블로그가 오름차순/내림차순 인덱스 차이를 정리한 글이 이 내용을 잘 설명한다.

### Functional 인덱스

표현식 결과에 인덱스를 걸 수 있게 됐다 — 8.0.13부터다.

```sql
-- LOWER(name)에 인덱스
CREATE INDEX idx_name_lower ON users ((LOWER(name)));

-- 이 쿼리가 인덱스를 쓸 수 있다
SELECT * FROM users WHERE LOWER(name) = 'john';
```

함수를 컬럼에 적용하면 인덱스를 못 쓰는 것이 기본이다. `WHERE LOWER(name) = 'john'`은 `name` 컬럼 인덱스를 쓸 수 없다. Functional 인덱스를 만들어두면 표현식 자체를 인덱스로 쓸 수 있다.

JSON 컬럼의 특정 경로에 인덱스를 걸 때도 쓸 수 있다. 단, JSON 데이터 모델링과 JSON functional 인덱스의 본격적인 풀이는 7장에서 한다. 여기서는 "인덱스 도구함에 JSON functional 인덱스가 있다"는 사실만 기억해두자.

## Invisible 인덱스: 안전하게 인덱스를 제거하자

인덱스가 실제로 사용되고 있는지 확인하지 않고 삭제했다가 갑자기 쿼리가 느려지는 경우가 있다. 난감한 상황이다. 되돌리려면 인덱스를 다시 만들어야 하는데, 대용량 테이블에서 그건 또 시간이 걸린다.

**Invisible 인덱스**를 쓰면 이 위험을 줄일 수 있다. 옵티마이저가 특정 인덱스를 무시하도록 설정하는 기능이다. 인덱스를 실제로 삭제하지 않고, 옵티마이저 입장에서 없는 것처럼 처리한다.

```sql
-- 인덱스를 invisible로 설정 (옵티마이저가 무시)
ALTER TABLE orders ALTER INDEX idx_status INVISIBLE;

-- 이후 서비스를 관찰한다. 느려진다면?
ALTER TABLE orders ALTER INDEX idx_status VISIBLE;  -- 즉시 복구

-- 이상 없으면 진짜로 삭제
ALTER TABLE orders DROP INDEX idx_status;
```

Invisible로 설정해두고 모니터링하는 기간 동안 슬로우 쿼리가 생기지 않는다면, 그 인덱스는 실제로 쓰이지 않는다고 확신할 수 있다. 그때 삭제한다.

인덱스가 invisible 상태여도 인덱스 자체는 유지되므로, INSERT/UPDATE 시 여전히 인덱스를 업데이트한다. 조회 성능 개선이 없는데 쓰기 비용만 내는 상태가 된다. 그러므로 invisible 기간을 너무 길게 유지하는 것은 좋지 않다.

## 인덱스 개수: 3~5개 휴리스틱

인덱스가 많을수록 좋은 것 아닌가. 그렇지 않다.

인덱스는 조회를 빠르게 하지만, 모든 쓰기(INSERT/UPDATE/DELETE)를 느리게 한다. 테이블에 row를 추가하거나 인덱스 컬럼을 수정하면, 관련된 모든 인덱스 B+Tree를 업데이트해야 하기 때문이다. 인덱스가 5개면 쓰기 1번에 B+Tree를 5번 업데이트한다.

또한 인덱스는 디스크 공간과 버퍼풀 공간을 차지한다. 인덱스가 많을수록 버퍼풀에서 인덱스 페이지가 데이터 페이지를 밀어내 버퍼풀 히트율에도 영향을 준다.

실무 휴리스틱: **테이블당 인덱스는 3~5개 수준으로 유지**하는 것이 좋다. 물론 조회 패턴에 따라 달라지지만, 10개가 넘어가면 한 번 검토해볼 필요가 있다. 쓰기가 많은 테이블일수록 인덱스 수를 줄이는 것이 유리하다.

중복 인덱스나 쓰이지 않는 인덱스는 제거하는 편이 낫다. `sys.schema_unused_indexes` 뷰나 `performance_schema.table_io_waits_summary_by_index_usage`로 인덱스별 사용 빈도를 확인할 수 있다.

```sql
-- 사용되지 않는 인덱스 확인
SELECT *
FROM sys.schema_unused_indexes
WHERE object_schema = 'mydb';

-- 인덱스별 조회 횟수
SELECT
  object_schema, object_name, index_name,
  count_read, count_write
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'mydb'
  AND index_name IS NOT NULL
ORDER BY count_read;
```

## INSERT/UPDATE 비용: 쓰기가 많다면 인덱스는 신중하게

쓰기가 많은 테이블에 인덱스를 추가하는 결정은 신중하게 해야 한다. 주문 상태 업데이트가 초당 수천 번 일어나는 테이블이라면, 인덱스 하나를 추가하는 것이 초당 수천 번의 추가 B+Tree 업데이트를 의미한다.

버퍼풀에 인덱스 페이지가 올라와 있다면 메모리에서 처리되지만, 이것도 버퍼풀 경합을 증가시킨다. 2장에서 Change Buffer의 역할을 기억하는가. Change Buffer는 세컨더리 인덱스 업데이트를 나중으로 미뤄 이 비용을 완화해준다. 그런데 8.4에서 기본 OFF가 됐으므로, 8.4에서는 이 완충이 없다.

실제로 인덱스 추가가 쓰기 성능에 얼마나 영향을 주는지는 측정해봐야 안다. 테스트 환경에서 인덱스 추가 전후 INSERT 성능을 비교해보는 것이 가장 확실하다.

## 실제 사례로 돌아가서

velog 사례를 다시 보자. `promotion_option.promotion_id`에 인덱스가 없었다. LEFT JOIN에서 매번 promotion_option 테이블을 풀 스캔했다. 결과 집합이 작아도 promotion_option 테이블이 크다면 전체를 읽어야 했다. 인덱스 하나 추가로 B+Tree 탐색 → 매칭 레코드만 접근으로 바뀌었다. 6초 → 0.02초.

그런데 이야기가 거기서 끝나지 않았다. 인덱스를 추가했더니 이번엔 옵티마이저가 JOIN 컬럼 인덱스를 "너무 우선"해서 다른 인덱스를 무시하는 현상이 생겼다. 이것이 인덱스 추가로 끝이 아닌 이유다. 인덱스를 추가한 뒤 `EXPLAIN`으로 옵티마이저가 어떤 인덱스를 선택했는지, 예상대로 움직이는지를 확인해야 한다. 5장이 이 확인 절차를 다룬다.

OKKY 사례는 복합 인덱스 컬럼 순서의 문제였다. 세부 내용은 공개되어 있지 않지만, equality 조건 컬럼을 앞에, range 조건 컬럼을 뒤에 두는 leftmost prefix 원칙을 지키지 않은 것이 원인이었을 가능성이 높다.

## 마무리

인덱스 설계는 데이터 구조 설계다. B+Tree라는 자료 구조의 정렬 속성을 얼마나 잘 활용하느냐가 핵심이다. 이 장에서 다룬 것들을 요약하자.

- 클러스터링 인덱스 = PK = 테이블. InnoDB에서 테이블은 PK 기준 B+Tree 그 자체다.
- 세컨더리 인덱스 조회는 back-to-table 비용이 포함된다. 커버링 인덱스로 없앨 수 있다.
- 복합 인덱스는 leftmost prefix 규칙을 따른다. equality → range → sort 순서로 컬럼을 배치한다.
- 인덱스는 조회를 빠르게 하지만 쓰기를 느리게 한다. 3~5개 휴리스틱을 기억하자.
- Invisible 인덱스로 안전하게 인덱스 제거를 검증할 수 있다.

다음 장에서는 이 인덱스들이 실제로 어떻게 사용되는지를 `EXPLAIN ANALYZE`로 확인하는 법을 배운다. 인덱스를 만들었다고 해서 항상 쓰이는 것은 아니다. 5장이 그 이유를 파헤친다.

## 참고 자료

- MySQL :: 17.7.1 InnoDB Locking — https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- DEV.to — Understanding Composite Indexes: https://dohost.us/index.php/2025/08/01/the-leftmost-prefix-rule-optimizing-composite-index-usage/
- Red-Gate — Composite B-tree indexes: https://www.red-gate.com/simple-talk/databases/mysql/mysql-index-overviews-composite-b-tree-indexes/
- velog "MySQL 인덱스 성능 개선하기 - 커버링 인덱스": https://velog.io/@rnjsrntkd95/MySQL-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-%EC%BB%A4%EB%B2%84%EB%A7%81-%EC%9D%B8%EB%8D%B1%EC%8A%A4
- velog "슬로우 쿼리 개선기": https://velog.io/@bruni_23yong/%EC%8A%AC%EB%A1%9C%EC%9A%B0-%EC%BF%BC%EB%A6%AC-%EA%B0%9C%EC%84%A0%EA%B8%B0
- velog "쿼리 속도 개선기": https://velog.io/@gkh4302/%EC%BF%BC%EB%A6%AC-%EC%86%8D%EB%8F%84-%EA%B0%9C%EC%84%A0%EA%B8%B0
- 카카오 — Ascending vs Descending index: https://tech.kakao.com/posts/351
