# 3장. 트랜잭션, 격리수준, 그리고 락의 메커니즘

> **이 챕터는 락의 메커니즘을 다룬다.** InnoDB가 어떤 락을 언제 어디에 거는가. 낙관적 락, 비관적 락, 분산락을 코드에서 어떻게 거는지(애플리케이션 패턴)는 10장에서 본다.

새벽 두 시에 슬랙 알람이 온다. "결제 처리가 안 돼요." 로그를 열면 이런 메시지가 있다.

```
ERROR 1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```

이 메시지를 받았을 때 "재시도하면 되겠지"로 끝내는 개발자와, `SHOW ENGINE INNODB STATUS`를 열어 어떤 트랜잭션이 어떤 레코드에서 서로를 기다리고 있는지를 읽어내는 개발자의 차이는 크다.

그 차이를 만드는 것이 이 장이다.

## 격리수준: 어디까지 보여줄 것인가

트랜잭션 격리수준은 "동시에 실행되는 다른 트랜잭션의 변경이 내 트랜잭션에 어디까지 보이는가"를 정한다. SQL 표준은 네 단계를 정의한다.

| 격리수준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|---------|-----------|---------------------|-------------|
| READ UNCOMMITTED | 허용 | 허용 | 허용 |
| READ COMMITTED | 차단 | 허용 | 허용 |
| REPEATABLE READ | 차단 | 차단 | 허용* |
| SERIALIZABLE | 차단 | 차단 | 차단 |

*InnoDB의 RR은 next-key lock으로 phantom을 추가 차단한다.

세 가지 이상 현상이 무엇인지 짚고 가자.

**Dirty Read**: 아직 커밋되지 않은 변경을 읽는 것. 트랜잭션 A가 row를 수정했는데 아직 커밋하지 않았다. 트랜잭션 B가 그 수정된 값을 읽는다. 이후 A가 롤백하면, B는 존재하지 않는 데이터를 읽었던 것이 된다. 끔찍한 일이다.

**Non-Repeatable Read**: 같은 쿼리를 두 번 실행했는데 결과가 다른 것. 트랜잭션 A가 row를 읽었다. 그 사이에 트랜잭션 B가 그 row를 수정하고 커밋했다. A가 같은 row를 다시 읽으면 값이 달라져 있다. "아까 읽었을 때는 10000원이었는데 지금은 9000원이 됐다"는 상황이다.

**Phantom Read**: 같은 범위 쿼리를 두 번 실행했는데 row 수가 달라지는 것. 트랜잭션 A가 `WHERE age > 20`으로 읽었다. 그 사이에 B가 age=25인 row를 추가하고 커밋했다. A가 다시 같은 조건으로 읽으면 row가 하나 더 있다.

### InnoDB의 기본: REPEATABLE READ

MySQL InnoDB의 기본 격리수준은 REPEATABLE READ(RR)다. 2장에서 설명한 MVCC가 이것을 가능하게 한다. 트랜잭션 시작 시 read view를 만들고, 트랜잭션이 끝날 때까지 같은 read view를 유지한다. 그래서 트랜잭션 중에 아무리 다른 트랜잭션이 row를 수정하고 커밋해도, 내 read view 기준의 일관된 스냅샷을 본다.

그런데 MVCC만으로는 phantom을 막을 수 없다. range 조회로 존재하지 않는 row에 대한 INSERT를 막을 방법이 없기 때문이다. InnoDB는 next-key lock으로 이 문제를 추가 해결한다. 이것은 잠시 후 락 메커니즘을 다루면서 본다.

```sql
-- 세션 1: 트랜잭션 시작
START TRANSACTION;
SELECT * FROM orders WHERE amount > 10000;
-- 결과: 3건

-- 세션 2: 이 사이에 실행 (커밋 완료)
INSERT INTO orders (amount) VALUES (15000);
COMMIT;

-- 세션 1: 같은 쿼리 다시 실행
SELECT * FROM orders WHERE amount > 10000;
-- RR: 여전히 3건 (read view가 유지되므로)
-- RC라면: 4건 (새 read view를 만들기 때문에)
```

### READ COMMITTED를 선택하면

RC를 선택하면 무엇을 잃고 무엇을 얻는가.

잃는 것: 같은 트랜잭션 안에서 동일 row를 두 번 읽으면 값이 달라질 수 있다. 트랜잭션 중간에 다른 트랜잭션이 커밋한 변경이 보인다. 데이터의 일관성 스냅샷이 보장되지 않는다.

얻는 것: 갭 락이 거의 없어진다. 갭 락이 줄어들면 동시에 여러 트랜잭션이 삽입할 때 서로 막히는 일이 줄어든다. 데드락도 감소하는 경향이 있다.

실무에서 RC를 선택하는 경우는 주로 두 가지다. 높은 INSERT 동시성이 필요해서 갭 락 경합을 줄여야 할 때, 또는 각 쿼리가 항상 최신 데이터를 봐야 할 때. 많은 OLTP 시스템에서 RC가 충분하고, 오히려 RR보다 더 자연스럽게 동작하는 경우도 있다.

한 가지 주의할 점이 있다. RC에서는 binlog가 반드시 row 포맷이어야 한다. statement 포맷에서 RC를 쓰면 복제 안전성이 보장되지 않는다. 최신 MySQL은 row 포맷이 기본이므로 실제로 문제가 되는 경우는 드물지만, 알고 있는 것이 좋다.

## InnoDB가 거는 락의 종류

이제 락 메커니즘을 본격적으로 살펴보자. InnoDB는 여러 종류의 락을 거는데, 각각이 다른 목적을 가지고 있다.

### 레코드 락: 인덱스 레코드를 잠근다

레코드 락(Record Lock)은 가장 기본적인 락이다. 인덱스 레코드 자체에 거는 잠금이다. 중요한 점은, InnoDB의 레코드 락은 **테이블의 row가 아니라 인덱스 레코드에** 건다는 것이다.

```sql
-- id=1 인 레코드에 대한 레코드 락
SELECT * FROM orders WHERE id = 1 FOR UPDATE;
```

이 쿼리가 실행되면 id=1 인덱스 레코드에 배타적 락(X lock)이 걸린다. 다른 트랜잭션이 같은 레코드를 수정하거나 배타적 락을 걸려고 하면 대기한다.

인덱스가 없는 컬럼으로 조건을 걸면 어떻게 될까. InnoDB는 모든 레코드를 인덱스를 통해 접근한다. 인덱스가 없는 컬럼으로 `FOR UPDATE`를 하면 클러스터링 인덱스의 전체 레코드에 락이 걸릴 수 있다. 이것이 락 범위를 예상보다 훨씬 크게 만드는 흔한 함정이다.

### 갭 락: 없는 곳을 잠근다

갭 락(Gap Lock)은 인덱스 레코드들 사이의 간격(gap)에 거는 잠금이다. 정확히 말하면, 인덱스의 두 레코드 사이, 첫 레코드 이전, 마지막 레코드 이후의 공간이다.

갭 락의 목적은 그 gap에 새 row가 INSERT되는 것을 막는 것이다. phantom을 방지하기 위한 메커니즘이다.

```sql
-- RR에서 이 쿼리는 id가 (10, 20) 사이의 gap에 갭 락을 건다
SELECT * FROM orders WHERE id > 10 AND id < 20 FOR UPDATE;

-- 다른 트랜잭션에서 이 INSERT는 위 갭 락 때문에 대기한다
INSERT INTO orders (id, ...) VALUES (15, ...);
```

갭 락의 중요한 특성이 있다. **갭 락끼리는 서로 호환된다.** 두 트랜잭션이 같은 gap에 각각 갭 락을 걸 수 있다. 갭 락은 INSERT를 막는 것이 목적이지, 다른 트랜잭션의 갭 락 진입을 막는 것이 아니다. 그러나 갭 락을 가진 트랜잭션 두 개가 서로 INSERT를 시도하면 데드락이 생길 수 있다.

RC 격리수준에서는 갭 락이 거의 사용되지 않는다. 이것이 RC에서 INSERT 동시성이 높아지는 이유다.

### 넥스트키 락: 레코드 락 + 갭 락

넥스트키 락(Next-Key Lock)은 레코드 락과 갭 락을 합친 것이다. 레코드 자체와 그 레코드 앞의 gap까지 같이 잠근다. RR 격리수준에서 InnoDB가 range 조회 시 기본적으로 사용하는 락이다.

```
인덱스: [1] [5] [10] [20]
넥스트키 락 범위:
  (-∞, 1]  →  id=1에 대한 넥스트키 락
  (1, 5]   →  id=5에 대한 넥스트키 락
  (5, 10]  →  id=10에 대한 넥스트키 락
  (10, 20] →  id=20에 대한 넥스트키 락
  (20, ∞)  →  마지막 gap(supremum)에 대한 갭 락
```

`SELECT * FROM orders WHERE id > 5 AND id <= 15 FOR UPDATE`를 실행하면 `(5, 10]`과 `(10, 20]` 범위에 넥스트키 락이 걸린다. 즉 id=10, id=20에 레코드 락이, (5,10)과 (10,20) gap에 갭 락이 각각 걸린다.

이것이 RR에서 phantom이 막히는 이유다. 새로운 row가 이 범위 안에 INSERT되려면 갭 락에 막힌다.

그런데 이 넥스트키 락이 때로는 필요 이상으로 넓은 범위에 걸리는 것이 데드락의 원인이 되기도 한다.

### 인텐션 락: 테이블과 행 락의 공존

인텐션 락(Intention Lock)은 테이블 단위 잠금과 행 단위 잠금이 공존할 수 있게 해주는 테이블 수준의 잠금이다. "이 테이블 안에 행 잠금이 있다"는 신호를 테이블 레벨에서 표시한다.

IS(Intention Shared)와 IX(Intention Exclusive) 두 종류가 있다. 행에 공유 락을 걸기 전에 테이블에 IS를, 행에 배타 락을 걸기 전에 테이블에 IX를 건다.

인텐션 락은 테이블 전체에 대한 락(LOCK TABLE ... WRITE 같은)과 행 락이 충돌하지 않도록 조율하는 역할을 한다. 일반 OLTP 쿼리에서 개발자가 직접 신경 쓸 일은 거의 없지만, `SHOW ENGINE INNODB STATUS`의 락 정보를 읽을 때 이 락이 등장하면 혼란스러울 수 있으므로 개념을 알아두자.

### 락 호환성 매트릭스

어떤 락이 어떤 락과 공존할 수 있는지를 정리한 것이 호환성 매트릭스다.

| | IS | IX | S | X |
|--|---|---|---|---|
| **IS** | 호환 | 호환 | 호환 | 충돌 |
| **IX** | 호환 | 호환 | 충돌 | 충돌 |
| **S** | 호환 | 충돌 | 호환 | 충돌 |
| **X** | 충돌 | 충돌 | 충돌 | 충돌 |

(IS: Intention Shared, IX: Intention Exclusive, S: Shared(행), X: Exclusive(행))

핵심을 정리하면:
- 공유 락(S)끼리는 호환된다. 여러 트랜잭션이 같은 row를 읽을 수 있다.
- 배타 락(X)은 모든 것과 충돌한다. X락을 잡은 트랜잭션이 있으면 다른 트랜잭션은 S도 X도 모두 대기해야 한다.
- IX끼리는 호환된다. 여러 트랜잭션이 테이블의 다른 행들을 각각 배타 락으로 잡을 수 있다.

## 어떤 SQL이 어떤 락을 거는가

이제 구체적인 SQL 문장들이 어떤 락을 거는지를 살펴보자. 이 부분이 실무에서 가장 중요하다.

### SELECT: 잠금이 없다(기본)

일반 `SELECT`는 잠금을 걸지 않는다. MVCC로 일관된 스냅샷을 읽기 때문에 락 없이도 동시성을 보장한다. 이것이 InnoDB의 강점 중 하나다.

```sql
-- 락 없음 (스냅샷 읽기)
SELECT * FROM orders WHERE customer_id = 1;
```

### SELECT ... FOR SHARE / FOR UPDATE: 잠금 읽기

명시적으로 락을 걸어야 할 때는 `FOR SHARE`(S락)나 `FOR UPDATE`(X락)를 사용한다.

```sql
-- 공유 락 (FOR SHARE = LOCK IN SHARE MODE)
SELECT * FROM orders WHERE id = 1 FOR SHARE;

-- 배타 락
SELECT * FROM orders WHERE id = 1 FOR UPDATE;
```

`FOR UPDATE`는 읽은 row에 X락을 건다. 이 row를 UPDATE나 DELETE하려는 다른 트랜잭션은 대기해야 한다. 재고 차감이나 포인트 사용 같이 "읽고 즉시 수정"하는 패턴에서 쓴다.

조건에 인덱스가 없거나, range 조건이면 락 범위가 커진다는 점을 기억해두자.

### INSERT: 삽입 의도 락

INSERT는 삽입할 위치의 gap에 "삽입 의도 락(Insert Intention Lock)"을 건다. 삽입 의도 락끼리는 호환된다 — 같은 gap에 여러 INSERT가 동시에 들어와도 서로 다른 위치라면 기다리지 않아도 된다.

그런데 그 gap에 이미 갭 락이 있다면? 다른 트랜잭션의 갭 락이 그 위치를 막고 있으면, INSERT는 대기해야 한다.

```sql
-- RR에서 트랜잭션 A가 이 쿼리로 gap 락을 잡으면
SELECT * FROM orders WHERE id BETWEEN 10 AND 20 FOR UPDATE;

-- 트랜잭션 B의 이 INSERT는 대기한다
INSERT INTO orders (id, ...) VALUES (15, ...);
```

### UPDATE와 DELETE

조건에 맞는 row들에 X락을 건다. range 조건이면 넥스트키 락이 걸릴 수 있다.

```sql
-- id=5인 row에 X락
UPDATE orders SET status = 'PAID' WHERE id = 5;

-- id > 100 이면서 status='PENDING'인 모든 row와 그 gap에 락
-- (조건에 따라 락 범위가 달라질 수 있다)
UPDATE orders SET status = 'EXPIRED' WHERE id > 100 AND status = 'PENDING';
```

### 외래키 검증

외래키가 있을 때 INSERT나 UPDATE는 추가 락을 유발한다. 자식 테이블에 INSERT할 때 부모 테이블의 해당 row에 S락을 건다. 이것은 부모 row가 외래키 검증 중에 삭제되는 것을 막기 위해서다.

```sql
-- order_items에 INSERT할 때 orders.id에 S락이 걸린다
INSERT INTO order_items (order_id, product_id, quantity)
VALUES (1, 100, 2);
```

이 동작이 때로는 예상치 못한 락 경합을 만든다. 부모 테이블을 DELETE하려는 트랜잭션과 자식 테이블에 INSERT하려는 트랜잭션이 서로 대기하는 상황이 생길 수 있다.

## 데드락: 사이클을 읽어내는 법

데드락은 두 트랜잭션이 서로의 락을 기다리는 순환 대기다. InnoDB는 이 순환을 감지해 한쪽 트랜잭션을 강제로 롤백한다.

### 전형적인 데드락 패턴

```sql
-- 트랜잭션 A
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- A가 row1에 X락
-- 이 시점에 트랜잭션 B가 실행됨

-- 트랜잭션 B
START TRANSACTION;
UPDATE accounts SET balance = balance - 200 WHERE id = 2;  -- B가 row2에 X락
UPDATE accounts SET balance = balance + 200 WHERE id = 1;  -- B가 row1 X락 시도 → A 대기

-- 트랜잭션 A (계속)
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- A가 row2 X락 시도 → B 대기
-- A는 B를 기다리고, B는 A를 기다린다 → 데드락
```

### SHOW ENGINE INNODB STATUS로 읽기

데드락이 발생하면 InnoDB는 마지막 데드락 정보를 내부에 보관한다. `SHOW ENGINE INNODB STATUS`의 LATEST DETECTED DEADLOCK 섹션에서 볼 수 있다.

```sql
SHOW ENGINE INNODB STATUS\G
```

출력의 LATEST DETECTED DEADLOCK 부분에는 두 트랜잭션이 각각 어떤 락을 보유하고 어떤 락을 대기하고 있었는지가 나온다. 읽는 법을 배우자.

```
TRANSACTION 1, ACTIVE 2 sec starting index read
MySQL thread id 15, OS thread handle ...
...
HOLDS THE LOCK(S):
RECORD LOCKS space id 5 page no 4 n bits 72 index PRIMARY
of table `shop`.`orders` trx id 421 lock_mode X locks rec but not gap
Record lock, heap no 2 PHYSICAL RECORD: ...

WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 5 page no 4 n bits 72 index PRIMARY
of table `shop`.`orders` trx id 421 lock_mode X locks rec but not gap
```

중요한 키워드는 `HOLDS THE LOCK(S)`와 `WAITING FOR THIS LOCK TO BE GRANTED`다. 트랜잭션 1이 어떤 락을 잡고 있으면서 어떤 락을 기다리는지, 트랜잭션 2가 어떤 락을 잡고 있으면서 어떤 락을 기다리는지를 읽으면, 두 트랜잭션이 서로를 기다리는 사이클이 보인다.

`lock_mode X locks rec but not gap`은 갭 없는 레코드 락(넥스트키 락이 아닌 순수 레코드 락)이고, `lock_mode X`는 넥스트키 락, `lock_mode X locks gap before rec`는 갭 락이다.

### information_schema로 현재 락 상태 보기

데드락이 아니라 현재 대기 중인 락 상태를 보려면 `performance_schema.data_locks`와 `data_lock_waits`를 쓴다.

```sql
-- 현재 잡혀 있는 락 목록
SELECT
  ENGINE_TRANSACTION_ID,
  OBJECT_SCHEMA,
  OBJECT_NAME,
  INDEX_NAME,
  LOCK_TYPE,
  LOCK_MODE,
  LOCK_STATUS,
  LOCK_DATA
FROM performance_schema.data_locks
WHERE LOCK_STATUS = 'WAITING';

-- 어떤 트랜잭션이 어떤 트랜잭션을 기다리는지
SELECT
  r.REQUESTING_ENGINE_TRANSACTION_ID AS waiting_trx,
  b.BLOCKING_ENGINE_TRANSACTION_ID AS blocking_trx,
  bl.OBJECT_NAME AS table_name,
  bl.LOCK_TYPE,
  bl.LOCK_MODE
FROM performance_schema.data_lock_waits r
JOIN performance_schema.data_locks bl
  ON bl.ENGINE_LOCK_ID = r.BLOCKING_ENGINE_LOCK_ID;
```

이 쿼리들로 락 대기가 왜 생기고 있는지를 실시간으로 볼 수 있다.

### 데드락은 버그가 아니라 신호다

데드락이 발생했다는 것은 버그가 아니다. 동시성 높은 시스템에서는 피하기 어렵다. 중요한 것은 두 가지다.

첫째, **재시도 가능한 구조**. 데드락을 만난 트랜잭션은 처음부터 다시 시도해야 한다. 스프링의 `@Transactional` + `@Retryable` 조합으로 재시도 로직을 만들 수 있다. 재시도할 때 같은 연산을 해도 되는 멱등성이 보장돼야 한다.

둘째, **락 순서 일관성**. 여러 row에 락을 거는 순서가 트랜잭션마다 다르면 순환이 생기기 쉽다. 항상 같은 순서로 잠그면 사이클이 만들어지기 어렵다. 위의 예에서 두 트랜잭션이 모두 "id가 작은 것부터 먼저 잠근다"는 규칙을 지킨다면 데드락이 발생하지 않는다.

## 낙관적·비관적 락: 개념만 짚고 가자

낙관적 락과 비관적 락은 코드 패턴의 이야기다. 10장에서 JPA와 함께 자세히 다룬다. 여기서는 개념만 빠르게 정리하자.

**낙관적 락**: 충돌이 드물다고 가정한다. 잠금 없이 읽고 수정한다. 커밋 시점에 다른 트랜잭션이 먼저 수정했는지를 version 컬럼으로 확인한다. 충돌이 났으면 재시도한다. JPA의 `@Version` 어노테이션이 이를 구현한다.

**비관적 락**: 충돌이 잦다고 가정하거나, 충돌 시 재시도 비용이 크다고 판단할 때 쓴다. 읽는 시점부터 `FOR UPDATE`로 잠근다. JPA의 `@Lock(PESSIMISTIC_WRITE)` 또는 직접 `SELECT ... FOR UPDATE`다.

선택 기준은 간단하다. 충돌 빈도가 낮고 재시도 비용이 크지 않으면 낙관적 락, 그 반대면 비관적 락이 적합하다. 코드 패턴과 스프링 통합은 10장에서 본다.

## 심화: Jepsen과 PostgreSQL 진영의 다른 시각

이 절은 심화 내용이다. 락 메커니즘의 기본이 잡혔다면 읽어보자. 나중에 돌아와도 된다.

Jepsen은 분산 시스템과 데이터베이스의 정합성을 테스트하는 프레임워크다. MySQL 8.0.34 분석(jepsen.io)에서, RR 격리수준 하에서도 여전히 일부 이상 현상 — fractured read, lost update — 이 발생할 수 있음을 보였다.

이게 왜 가능한가. InnoDB의 RR은 MVCC 스냅샷으로 비잠금 읽기를 보호하지만, 잠금 읽기(`FOR UPDATE`)와 비잠금 읽기가 섞이면 일관성이 깨질 수 있다. 트랜잭션 중에 두 번의 읽기를 각각 잠금 없이, 잠금 있이 섞어서 하면 서로 다른 버전을 볼 수 있다.

Jepsen 분석의 결론은: **금전 트랜잭션같이 엄격한 일관성이 필요한 경우라면 RR + 명시적 비관적 락을 조합하거나, SERIALIZABLE을 고려하라**는 것이다.

PostgreSQL 진영의 접근 방식은 다르다. PostgreSQL은 RC를 기본 격리수준으로 쓰면서, 필요할 때 SSI(Serializable Snapshot Isolation)를 통해 완전한 직렬성을 보장한다. MySQL의 RR + 갭 락 방식보다 더 정교한 충돌 감지를 제공하지만, 오버헤드도 있다.

MySQL 진영은 기본 RR을 유지하면서 명시적 락으로 보완하는 방식을 취한다. 어느 쪽이 더 낫다고 단정할 수 없다. 워크로드와 팀의 방식에 따라 맞는 선택이 다르다. Cahill(2009)의 논문이 스냅샷 격리와 직렬성 격리의 관계를 이론적으로 정리한 참고 자료다 — 종장의 참고 문헌 절에서 안내한다.

실무 조언을 하자면: 대부분의 일반 OLTP는 RR 기본값으로 충분하다. 금전 이동, 재고 차감처럼 정합성이 핵심인 로직에서는 명시적 비관적 락(`FOR UPDATE`)을 쓰는 것이 가장 확실하다.

## 마무리

이 장에서 InnoDB의 락 메커니즘을 처음부터 끝까지 살펴봤다. 격리수준 네 단계와 각각이 허용·차단하는 이상 현상, 레코드·갭·넥스트키·인텐션 락의 역할과 호환성, 구체적인 SQL이 어떤 락을 유발하는지, 그리고 데드락 로그를 읽는 방법까지.

기억해두자: 데드락 로그가 찜찜하게 느껴졌던 것은 락 메커니즘의 그림이 없어서였다. 이 그림이 잡히면 그 로그가 전혀 다르게 보인다.

다음 장에서는 인덱스 설계로 넘어간다. B+Tree의 구조와 클러스터링 인덱스의 본질을 알고 있는 지금, 인덱스 이야기가 훨씬 자연스럽게 들릴 것이다.

## 참고 자료

- MySQL :: 17.7.1 InnoDB Locking — https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- MySQL :: 17.7.2.1 Transaction Isolation Levels — https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html
- MySQL :: 17.7.4 Phantom Rows / Next-Key Locking — https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html
- MySQL :: 17.7.5 Deadlocks in InnoDB — https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html
- MySQL :: InnoDB Data Locking Part 3 "Deadlocks" — https://dev.mysql.com/blog-archive/innodb-data-locking-part-3-deadlocks/
- Percona — InnoDB's Gap Locks — https://www.percona.com/blog/innodbs-gap-locks/
- Jepsen — MySQL 8.0.34 분석 — https://jepsen.io/analyses/mysql-8.0.34
- letmecompile.com — MySQL InnoDB lock & deadlock 이해하기 — https://www.letmecompile.com/mysql-innodb-lock-deadlock/
- Bytebase — How to show MySQL locks — https://www.bytebase.com/reference/mysql/how-to/how-to-show-mysql-locks/
