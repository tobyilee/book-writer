# 9장. 한꺼번에 처리한다 — 배치와 대량 write

한 상황을 그려보자. 새벽 두 시. 야간 정산 배치가 돈다. 어제 들어온 주문 30만 건을 정산 테이블로 옮겨 적는 일이다. 평소처럼 `for` 루프 한 번 돌리고 자러 들어가면 그만이라고 생각했는데, 새벽 다섯 시에 알람이 울린다. 배치가 아직 끝나지 않았다. 게다가 곧 아침 트래픽이 들어올 시간이다. 부랴부랴 슬랙을 켜고 로그를 보니, INSERT 문이 한 줄씩, 한 줄씩, 한 줄씩 끝없이 흘러가고 있다. 30만 줄이다. 한 줄에 0.1초면 30,000초, 다시 말해 여덟 시간이 넘는다. 끔찍한 일이다.

그래서 어디서 들었던 게 떠오른다. "Hibernate에 batch_size를 켜면 된다." 황급히 `application.yml`을 열어 `hibernate.jdbc.batch_size=25`를 추가하고 재배포한다. 그런데 다음 날 새벽, 로그가 똑같다. INSERT이 여전히 한 줄씩 나간다. 분명히 켰는데 왜 동작하지 않을까. 난감하다.

이 장은 그 난감함을 풀어가는 길이다. 30만 건을 한 시간이 아니라 1분 안에 끝내려면 어떤 스위치들이 함께 켜져 있어야 하는지, 왜 `batch_size`만 켜서는 부족한지, 그리고 대량 write라는 워크로드가 JPA에게 무엇을 요구하는지를 같이 짚어보자.

## INSERT은 왜 한 줄씩 나갈까

먼저 가장 자주 발이 걸리는 자리부터 보자. `batch_size`를 분명히 설정했는데도 INSERT이 한 줄씩 나가는 현상이다. 이 한 가지를 이해하면, 그 다음에 나오는 모든 튜닝이 자연스럽게 자리를 잡는다.

JDBC에는 `executeBatch()`라는 메서드가 있다. INSERT 문 여러 개를 모아두었다가, 한 번의 네트워크 호출로 DB에 보내는 기능이다. 1장에서 우리는 라운드트립이 진짜 비용이라고 했다. 그 라운드트립을 30만 번이 아니라 12,000번(=300,000 ÷ 25)으로 줄여주는 도구가 바로 JDBC batch다. Hibernate는 그 위에 살짝 얇은 막을 두른다. `persist`나 dirty checking이 만들어낸 INSERT/UPDATE 문을 모아두었다가, 25개가 차면 한꺼번에 `executeBatch()`로 흘려보낸다. 이론은 깔끔하다.

그런데 한 줄씩 나간다. 왜 그럴까. 가장 흔한 원인은 한 가지다. **엔티티의 식별자 생성 전략이 `IDENTITY`로 되어 있기 때문**이다.

```java
@Entity
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    // ...
}
```

이 한 줄이 batch를 죽인다. 3장에서 식별자 이야기를 했을 때 우리는 이걸 한 번 짚고 넘어갔지만, 그때는 "IDENTITY는 batch를 죽인다"는 결론만 받고 지나갔다. 이제 그 메커니즘을 다시 펼쳐 보자.

`IDENTITY` 전략은 DB에게 PK 생성을 맡긴다. PostgreSQL의 `BIGSERIAL`, MySQL의 `AUTO_INCREMENT`가 그것이다. 우리가 `persist(order)`를 호출하면 Hibernate는 어떻게 동작해야 할까. 그 자리에서 즉시 INSERT을 DB로 보내야 한다. 왜냐하면 *그 INSERT의 결과로 비로소 PK가 생기기 때문이다*. PK가 없으면 PersistenceContext가 그 엔티티를 식별해 보관할 수도 없다. 다음 줄에서 누가 그 엔티티를 참조하려고 해도 식별자가 없다. 그래서 Hibernate는 `IDENTITY` 엔티티의 INSERT만큼은 *write-behind*를 포기한다. write-behind, 즉 "쌓아두었다가 한꺼번에 flush" 라는 정책 자체가 무너지는 자리다.

쌓아두지 않으니 모을 것도 없다. 모을 게 없으니 `executeBatch()`가 불릴 일도 없다. 그렇게 INSERT은 한 줄씩, 30만 번의 라운드트립으로 흘러간다. `batch_size=25`를 켜둔 채로도.

물론 Vlad Mihalcea의 블로그를 한 줄로 옮기면 "5건이라도 5번의 INSERT이 나간다"가 된다. 한국어로 옮기면 더 살갗에 와닿는다. *batch를 켜둔 채로도 batch가 일어나지 않는다.* 이 말의 의미를 잠시 곱씹어 보자. `application.yml`의 `batch_size`만 보고 "우리는 배치 켜뒀어요"라고 안심해 온 시스템이 얼마나 많을지 생각해 보면 아찔하다.

그렇다면 어떻게 해야 할까. 답은 단순하다. 식별자 생성 전략을 바꾸는 것이다.

## SEQUENCE pooled-lo가 정답인 이유

PostgreSQL과 Oracle, SQL Server, H2에는 SEQUENCE 객체가 있다. SEQUENCE는 DB가 관리하는 단조 증가 카운터다. "다음 번호 줘"라고 부르면 다음 정수를 돌려준다. 이게 IDENTITY와 무엇이 다를까. 결정적으로 다른 점이 하나 있다. *INSERT 전에 호출할 수 있다*는 점이다.

```sql
SELECT nextval('order_seq');
-- 결과: 1001

INSERT INTO orders (id, ...) VALUES (1001, ...);
```

PK가 INSERT 결과가 아니라 INSERT 입력이 된다. 그래서 Hibernate는 `persist(order)` 시점에 SEQUENCE를 한 번 호출해 PK를 미리 확보한 뒤, INSERT 자체는 PersistenceContext에 쌓아 두었다가 나중에 한꺼번에 보낼 수 있다. write-behind가 살아난다. batch가 동작한다.

자, 여기서 한 가지 의문이 생긴다. "그러면 SEQUENCE를 30만 번 호출해야 하는 거 아닌가? 그 자체도 라운드트립 아닌가?" 정확한 지적이다. 단순한 SEQUENCE는 그 자체가 라운드트립을 만든다. 그래서 Hibernate에는 SEQUENCE optimizer라는 게 있다. 그중 가장 권장되는 게 *pooled-lo* 전략이다.

```java
@Entity
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "order_seq")
    @SequenceGenerator(
        name = "order_seq",
        sequenceName = "order_seq",
        allocationSize = 50
    )
    private Long id;
    // ...
}
```

`allocationSize=50`이 핵심이다. SEQUENCE를 한 번 호출해서 1000을 받아오면, Hibernate는 *그게 1000~1049의 시작점*이라고 해석한다. 그 50개 슬롯은 메모리 안에서 채워나간다. 50개를 다 쓰면 그제야 SEQUENCE를 다시 호출한다. 30만 건을 만들면서 SEQUENCE를 호출하는 횟수는 6,000번이다. 라운드트립이 두 자리 자리수 단위로 줄어든다.

여기서 어떤 분은 한 번 더 의심할 수 있다. "메모리 안에서 채운다는데, 그 사이에 누가 같은 SEQUENCE를 호출하면 충돌하지 않을까?" 좋은 질문이다. pooled-lo가 영리한 게 그 자리다. 50을 받았을 때 *시작이 1000인지, 끝이 1000인지*가 strategy마다 다른데, pooled-lo는 *시작*으로 해석한다. 그래서 다음 SEQUENCE 호출자가 1050을 받든 1100을 받든, 우리가 쓰는 1000~1049와 겹치지 않는다. PostgreSQL의 SEQUENCE는 트랜잭션 격리와 무관하게 atomic하게 증가하니, 한 클라이언트의 1000과 다른 클라이언트의 1050은 안전하게 분리된다.

Vlad의 30만 건 PostgreSQL 벤치를 다시 보자. SEQUENCE + batch 4종 세트를 모두 켜둔 상태에서 측정한 결과다.

| 행 수 | no batch | batch_size=25 | speedup |
|-------|----------|---------------|---------|
| 30,000 | 5,889 ms | 2,640 ms | 2.2x |
| 300,000 | 51,785 ms | 16,052 ms | 3.2x |

30만 건에서 51초가 16초로 줄어든다. 3.2배다. 더 흥미로운 건, 행 수가 늘수록 speedup이 더 커진다는 점이다. 30,000건에선 2.2배, 300,000건에선 3.2배. 라운드트립이 절약되는 절대량이 커지기 때문이다. 우리가 정말 batch를 필요로 하는 자리는 데이터가 많아지는 자리니, 이 경향은 든든하다.

그러니 식별자 결정은 이렇게 정리하고 가자. 새 엔티티에는 가능한 한 SEQUENCE + pooled-lo를 쓰자. PostgreSQL을 쓰는 우리에게는 굳이 IDENTITY를 고집할 이유가 없다. 기억해두자.

MySQL을 쓰는 분들의 처지는 다르다. MySQL은 8.0 기준으로도 표준 SEQUENCE 객체가 없다. `AUTO_INCREMENT`(즉 IDENTITY)가 거의 유일한 자동 PK 선택지다. 그러면 batch를 영영 포기해야 하는가. 그렇지 않다. 두 가지 우회로가 있다. 첫째는 *수동 ID 할당*이다. 별도 ID 발급 테이블이나 어플리케이션 단에서 만든 분산 ID(snowflake 등)를 직접 부여하고, 엔티티의 ID는 `@GeneratedValue` 없이 둔다. 둘째는 잠시 후에 만날 `StatelessSession`을 활용한 직접 batching이다. MySQL이라고 해서 길이 막혀 있지는 않다.

## batch 4종 세트 — 한 묶음으로 켠다

`batch_size`만 켜는 걸로는 부족하다는 게 이 장의 출발점이었다. 그러면 무엇을 더 켜야 하는가. Vlad가 "정식 batch 세트"라고 부르는 네 개의 스위치를 보자.

```properties
hibernate.jdbc.batch_size=25
hibernate.order_inserts=true
hibernate.order_updates=true
hibernate.batch_versioned_data=true
```

하나씩 풀어보자.

**`hibernate.jdbc.batch_size=25`.** JDBC `executeBatch()`에 한 번에 보낼 statement의 개수다. 5에서 50 사이를 권장하고, 25가 가장 자주 쓰는 값이다. 너무 작으면 라운드트립이 그대로 남고, 너무 크면 batch 자체가 채워질 때까지 메모리에 쌓이는 양이 늘어난다. 또한 JDBC 드라이버나 DB 쪽에 한 batch가 너무 커서 거부되는 자리도 있다. 25는 보수적이면서도 효과적인 값이다.

**`hibernate.order_inserts=true`.** 이 스위치가 왜 필요한지를 알려면 한 시나리오를 더 그려보자. 우리가 `Order`와 `OrderItem`을 둘 다 한 번에 INSERT한다고 해보자. 코드에서는 이런 식으로 만들어진다.

```java
for (int i = 0; i < 100; i++) {
    Order order = new Order(...);
    em.persist(order);
    for (int j = 0; j < 5; j++) {
        OrderItem item = new OrderItem(order, ...);
        em.persist(item);
    }
}
```

`persist`가 호출된 순서대로 PersistenceContext에 쌓이면 어떻게 될까. `Order1, Item1, Item2, ..., Order2, Item6, ...` 식으로 뒤섞인다. JDBC batch는 *같은 PreparedStatement*에만 모인다. 즉 `Order` INSERT 문과 `OrderItem` INSERT 문이 번갈아 나오면, batch가 모이지 못한 채 자꾸 닫혔다 다시 열리기를 반복한다. 결과적으로 batch 사이즈가 1에 가깝게 떨어진다.

`order_inserts=true`를 켜면 Hibernate가 flush 시점에 INSERT을 *테이블별로 정렬한다*. `Order` 100건을 먼저, 그다음 `OrderItem` 500건을 다음에 보낸다. 같은 테이블의 INSERT이 연속해서 흘러가니 25개씩 깔끔하게 묶인다. 두 테이블만 있어도 효과가 크고, 테이블이 늘어날수록 효과가 더 커진다.

**`hibernate.order_updates=true`.** UPDATE에 대해 같은 효과를 낸다. dirty checking으로 여러 엔티티가 함께 변경되는 상황에서 UPDATE이 섞여 나가는 걸 막아준다. INSERT보다 효과의 폭은 작지만, 같이 켜두는 게 정석이다.

**`hibernate.batch_versioned_data=true`.** 이게 좀 특별하다. `@Version`이 붙은 엔티티의 UPDATE batching에 관한 스위치다. 8장에서 우리는 낙관락을 이야기했다. `@Version`이 붙으면 UPDATE 문에 `WHERE version=?` 조건이 들어가고, 영향받은 row 개수가 0이면 `OptimisticLockException`이 던져진다. 그런데 batch에서는 한 가지 미묘한 문제가 생긴다. *JDBC `executeBatch()`가 각 statement의 영향받은 row 개수를 정확히 돌려주는가?* 모든 드라이버가 그렇진 않다. 어떤 드라이버는 `Statement.SUCCESS_NO_INFO`(=-2)를 돌려준다. 그러면 Hibernate는 어느 row가 stale했는지 알 수 없다.

오래 전엔 이 안전장치 때문에 Hibernate는 `@Version` 엔티티의 UPDATE batching을 디폴트로 꺼두었다. 즉 versioned entity의 UPDATE은 batch에서 빠진다. write 중심 워크로드에서 이게 batching이 잘 안 되는 또 다른 원인이 되곤 했다. PostgreSQL pgjdbc, MySQL Connector/J 같은 모던 드라이버는 row count를 정확히 돌려준다. 이 환경이라면 `batch_versioned_data=true`를 켜서 versioned entity의 UPDATE도 batching에 참여시킬 수 있다. 우리가 PostgreSQL이나 MySQL을 쓰고 있다면 이걸 켜두는 편이 낫다.

네 개를 한 묶음으로 기억해두자. *batch_size + order_inserts + order_updates + batch_versioned_data.* `application.yml`에 이 네 줄이 함께 있는지가 첫 번째 체크리스트다. 하나만 빠져도 효과가 절반으로 떨어지는 자리가 흔하다.

## PostgreSQL의 비장의 카드 — reWriteBatchedInserts

여기까지 했어도 끝이 아니다. PostgreSQL을 쓰고 있다면, JDBC URL에 한 줄을 더 추가해서 *추가로 2~3배*를 받을 수 있다.

```
jdbc:postgresql://host:5432/db?reWriteBatchedInserts=true
```

이게 무엇을 하는가. JDBC `executeBatch()`는 기본적으로 *25개의 단일 INSERT 문*을 한 번에 보낸다. 라운드트립은 한 번이지만, DB는 여전히 25개의 INSERT을 각각 파싱하고 각각 실행해야 한다. `reWriteBatchedInserts=true`를 켜면, pgjdbc 드라이버가 그 25개를 *multi-VALUES 단일 INSERT*으로 재작성한다.

```sql
-- 켜기 전 (25개 statement 묶음)
INSERT INTO orders (id, ...) VALUES (?, ...);
INSERT INTO orders (id, ...) VALUES (?, ...);
-- ... 25번

-- 켠 뒤 (1개 statement)
INSERT INTO orders (id, ...) VALUES
  (?, ...),
  (?, ...),
  -- ... 25개의 VALUES 튜플
  (?, ...);
```

파싱 비용이 1/25로 줄고, planner 호출도 한 번이고, log 출력도 한 줄이다. Vlad의 측정에서는 batch 효과 위에 추가로 2~3배가 더 붙는다. 즉 30만 건 INSERT이 16초에서 다시 5~8초 수준으로 떨어진다. PostgreSQL 환경의 대량 INSERT에는 거의 무조건 켜두는 게 맞는 옵션이다.

여기에는 작은 주의사항이 있다. `RETURNING` 절이 포함된 INSERT, 즉 INSERT 후 무언가를 돌려받는 경우에는 multi-VALUES로 재작성되지 않는다. 일반적인 batch INSERT 경로에는 영향이 없으니, 안심하고 켜두자.

MySQL에도 비슷한 효과를 내는 옵션이 있다. `rewriteBatchedStatements=true`를 JDBC URL에 추가하면 Connector/J가 batch INSERT을 multi-VALUES로 재작성한다. MySQL 환경이라면 이 옵션을 켜두는 편이 낫다. 이름이 `re*W*riteBatchedInserts` (PostgreSQL)와 `rewriteBatchedStatements` (MySQL)로 묘하게 다른데, 두 줄로 같이 외워두자.

## 정식 batch 처리 패턴 — flush와 clear의 짝

설정은 끝났다. 이제 코드 차례다. 30만 건을 처음부터 끝까지 한 트랜잭션, 한 PersistenceContext에 쌓아 두고 끝에 `flush()`를 한 번 부르는 식으로 만들면 어떻게 될까. 라운드트립은 줄지만, 7장에서 우리가 본 그 문제가 다시 찾아온다. *PersistenceContext OOM*이다.

PersistenceContext는 자기에게 관리되는 모든 엔티티의 스냅샷을 들고 있다. 엔티티 하나가 평균 1KB라고 치면 30만 건은 300MB다. JVM 옵션을 충분히 잡아두지 않은 환경에서는 그냥 죽는다. 죽지 않더라도, dirty checking이 매 flush마다 30만 개의 스냅샷을 다시 검사한다. 단순 INSERT 시나리오에서도 부담이 점점 커진다.

그래서 우리는 batch 사이즈마다 두 가지를 한다. 하나는 `flush()`로 그동안 쌓인 INSERT을 DB로 흘려보내는 것. 다른 하나는 `clear()`로 PersistenceContext를 비우는 것. Vlad가 "정식 batch 처리 패턴"이라 부르는 코드를 보자.

```java
EntityManager em = emf.createEntityManager();
EntityTransaction tx = em.getTransaction();
int batchSize = 25;

try {
    tx.begin();
    for (int i = 0; i < entityCount; i++) {
        if (i > 0 && i % batchSize == 0) {
            tx.commit();
            tx.begin();
            em.clear();
        }
        em.persist(new Post("Post " + (i + 1)));
    }
    tx.commit();
} catch (RuntimeException e) {
    if (tx.isActive()) tx.rollback();
    throw e;
} finally {
    em.close();
}
```

작은 코드인데 짚어둘 게 많다.

첫째, 25개마다 `tx.commit()`이 일어난다. 30만 건을 한 트랜잭션으로 묶지 않는다는 뜻이다. 이게 의외라고 느낄 수 있다. "트랜잭션은 길수록 안전한 거 아닌가?" 일반적인 OLTP에서는 그렇다. 하지만 batch 처리는 다르다. 한 트랜잭션이 길어지면 그 사이에 쌓이는 undo log(PostgreSQL이라면 dead tuple)가 폭증한다. 도중에 한 번이라도 실패하면 30만 건이 모두 롤백된다. 진척이 사라진다. batch 처리에서는 "*작은 단위로 진척을 만들어가는 것*"이 안전과 같은 의미가 된다. 다만 비즈니스 의미가 "all-or-nothing"이라면 한 트랜잭션을 유지해야 한다. 그 경우엔 외부에 진척 테이블을 별도로 두거나, `SAVEPOINT`를 적극 활용한다.

둘째, `em.clear()`가 들어간다. 만약 이걸 빼면 어떻게 될까. commit으로 flush는 됐지만 PersistenceContext에는 25개의 엔티티가 그대로 남는다. 다음 루프에서 또 25개가 쌓이고, 그다음에 또 25개가 쌓이고… 30만 건이 끝날 즈음에는 결국 30만 개가 PersistenceContext에 들어 있다. OOM이다. `clear()`는 PersistenceContext에서 모든 엔티티를 분리한다. 메모리가 일정하게 유지된다.

셋째, `clear()` 위치가 *commit 뒤, 다음 begin 뒤*에 있다. 순서가 묘하다. 사실 미묘한 자리다. `commit()`이 일어나면 Hibernate가 자동으로 flush를 부르는데, 그 flush가 PersistenceContext의 dirty checking을 통해 INSERT을 토해낸다. 그러니 `clear()`를 commit 전에 부르면 *아직 INSERT되지 않은 엔티티들이 사라진다*. 반드시 commit 다음이어야 한다. 순서를 한 번 잘못 두면 데이터가 통째로 증발한다. 끔찍한 일이다. 코드에 주석으로 "*clear는 반드시 commit 다음에*"를 박아 두자.

여기서 7장의 결론과 다시 만나게 된다. 7장에서 우리는 1차 캐시가 무한히 크지 않다는 점, PersistenceContext가 작아야 한다는 점을 강조했다. 그 결론이 가장 살갗에 닿는 자리가 batch다. *batch는 7장의 직접적인 응용 시험장*이라고 생각해도 좋다.

Spring 환경에서 이걸 어떻게 구현하느냐는 또 약간 다르다. `@Transactional`을 메서드 단위로 잡으면 트랜잭션이 메서드 끝에 한 번 commit된다. batch에서는 메서드 안에서 여러 번 commit이 필요하니, 패턴이 바뀐다. 한 가지는 `TransactionTemplate` 또는 `PlatformTransactionManager`를 직접 주입받아 batch 사이즈마다 새 트랜잭션을 시작하고 끝내는 것이다. 다른 한 가지는 한 트랜잭션 안에서 `entityManager.flush()` + `entityManager.clear()`만 부르고, commit은 마지막에 한 번만 하는 것이다(이 경우는 위에서 말한 OLTP-safe 트레이드오프를 안고 간다).

```java
@Service
public class OrderBatchService {

    @PersistenceContext
    private EntityManager em;

    @Transactional
    public void importOrders(List<OrderDto> dtos) {
        int batchSize = 25;
        for (int i = 0; i < dtos.size(); i++) {
            Order order = toEntity(dtos.get(i));
            em.persist(order);
            if (i > 0 && i % batchSize == 0) {
                em.flush();
                em.clear();
            }
        }
        em.flush();
        em.clear();
    }
}
```

이 한 메서드 안에서 트랜잭션은 하나지만, *PersistenceContext만 25개마다 비워주는* 패턴이다. 안전하다고 느껴지는 만큼 OOM 위험도 낮다. 다만 진척의 의미가 작아질 뿐이다. 30만 건을 안전하게 OLTP 패턴으로 돌리고 싶으면 첫 번째 패턴, 트랜잭션이 비즈니스 의미를 가져야 하면 두 번째 패턴. 둘 사이의 선택은 도메인이 결정한다.

## StatelessSession이 부활했다

이쯤 되면 마음 한구석에 묘한 생각이 든다. *PersistenceContext, dirty checking, 1차 캐시 같은 게 batch에서는 다 짐 아닌가?* 단순 INSERT 30만 건을 흘려넣는데 우리는 무엇 때문에 스냅샷을 두 배로 들고, dirty 비교를 돌리고, 1차 캐시를 신경 써야 하는가. 이 질문에 정직하게 답하면 그렇다. *batch 처리에서는 그 모든 게 필요 없다.* 우리는 그저 SQL을 빠르게 흘려보내고 싶을 뿐이다.

Hibernate에는 그 자리를 위한 도구가 따로 있다. `StatelessSession`이다. 이름 그대로 "상태가 없는 세션"이라는 뜻인데, 더 정확히는 *PersistenceContext가 없는 세션*이다. dirty checking이 없다. 1차 캐시가 없다. cascade도 없다. 그래서 우리가 `insert(entity)`나 `update(entity)`를 부르면, Hibernate는 그 자리에서 SQL을 만들어 보낸다. 메모리에 스냅샷도 안 들고, dirty 비교도 안 한다.

그런데 왜 우리가 평소에 `StatelessSession`을 별로 못 들어봤을까. 이유가 있다. Hibernate 6 이전에는 `StatelessSession`이 JDBC batching을 *지원하지 않았다*. 한 줄씩 즉시 INSERT을 흘려보낸다는 의미였다. 빠르긴 했지만, 결정적인 batch 효과를 못 받았다. 또 UPSERT 같은 고급 동작도 빠져 있었다. 그래서 "이론적으로는 좋은데 실제로는 활용도가 낮은 도구"였다.

이 그림이 Hibernate 6.3에서 바뀌었다. **StatelessSession에 batch 지원이 들어왔다.** 6.4에서는 **UPSERT 메서드까지 추가됐다.** 진정한 의미의 high-volume ingest 도구로 부활한 것이다.

```java
SessionFactory sf = em.getEntityManagerFactory().unwrap(SessionFactory.class);
try (StatelessSession session = sf.openStatelessSession()) {
    Transaction tx = session.beginTransaction();
    int batchSize = 50;
    for (int i = 0; i < orders.size(); i++) {
        session.insert(orders.get(i));
        if (i > 0 && i % batchSize == 0) {
            session.flush();
        }
    }
    tx.commit();
}
```

코드를 보면 거의 비슷해 보이지만, 중요한 차이가 있다. `clear()`가 없다. 비울 PersistenceContext 자체가 없기 때문이다. 메모리 사용량이 평탄하다. 한 가지 위안이 늘었다.

언제 StatelessSession을 써야 할까. 기준은 의외로 단순하다. *대량 ingest 경로이고, 엔티티 그래프 cascade가 필요 없고, 1차 캐시 안에서 같은 엔티티를 두 번 참조하지 않을 때*. 야간 ETL, CSV 임포트, 외부 API에서 받은 데이터의 대량 적재. 이런 자리가 정확히 StatelessSession의 자리다. 반대로 도메인 로직이 엔티티 그래프를 따라 들어가서 `OrderItem`을 추가하고 `Customer`의 `lastOrderedAt`을 업데이트하는 식의 시나리오에는 부적합하다. 그 자리에는 일반 `EntityManager` + flush/clear 패턴이 적합하다.

UPSERT 메서드 한 가지도 짚어두자. Hibernate 6.4의 `session.upsert(entity)`는 PK가 이미 존재하면 UPDATE, 없으면 INSERT을 하는 메서드다. PostgreSQL의 `ON CONFLICT ... DO UPDATE`, MySQL의 `ON DUPLICATE KEY UPDATE`, SQL Server의 `MERGE`로 dialect별로 재작성된다. 데이터 sync 경로(외부에서 들어오는 데이터로 우리 테이블을 최신화)에 정석적인 도구다. 이전엔 직접 native SQL을 짜야 했던 자리가 어노테이션과 메서드 한 줄로 정리된다.

요약하자면 이렇다. PersistenceContext가 필요한 도메인 로직은 일반 EntityManager로, PersistenceContext가 짐만 되는 ingest 경로는 StatelessSession으로. 이 분리만 잘 해도 batch의 성능과 단순함이 동시에 따라온다. *대량 ingest 경로에 StatelessSession을 검토해 봤는지*가 두 번째 체크리스트다.

## 벌크 UPDATE/DELETE — JPQL 한 줄의 힘과 함정

지금까지는 *한 row씩 만들거나 고치는* 일을 batch로 묶는 이야기였다. 그런데 어떤 경우는 한 발 더 나아갈 수 있다. *한 SQL로 여러 row를 한 번에 갱신하는* 경우다.

"1년 이상 된 게시글의 status를 ARCHIVED로 바꿔라"는 요구를 받았다고 해보자. 보통 우리는 이렇게 짠다.

```java
List<Post> oldPosts = em.createQuery(
    "select p from Post p where p.createdOn < :d", Post.class)
    .setParameter("d", oneYearAgo)
    .getResultList();

for (Post p : oldPosts) {
    p.setStatus(Status.ARCHIVED);
}
```

JPA 진영의 클래식 코드다. 10건이면 멀쩡하게 동작한다. 그런데 만약 1년 이상 된 게시글이 50만 건이라면? 50만 건을 SELECT해서 메모리에 올리고, dirty checking을 통해 UPDATE 50만 번을 만든다. batch를 잘 묶었다 해도 50만 건의 데이터가 메모리를 왔다 갔다 하는 자리는 그 자체로 부담이다. 그런데 우리가 정말 원한 건 SQL 한 줄이다.

```sql
UPDATE post SET status = 'ARCHIVED' WHERE created_on < ?
```

JPA에도 이 자리를 위한 도구가 있다. *Bulk UPDATE/DELETE*다.

```java
int updated = em.createQuery("""
    update Post p
    set p.status = :s
    where p.createdOn < :d""")
    .setParameter("s", Status.ARCHIVED)
    .setParameter("d", oneYearAgo)
    .executeUpdate();
```

`executeUpdate()`는 SELECT 대신 UPDATE/DELETE를 실행하고 영향받은 row 수를 돌려준다. SQL은 정확히 우리가 원한 한 줄로 나간다. 50만 건이든 5,000만 건이든 메모리에 row를 올리지 않는다. DB가 자기 할 일을 자기 안에서 한다. 이게 정답이다.

Spring Data JPA에서는 `@Query`와 `@Modifying`을 함께 쓴다.

```java
public interface PostRepository extends JpaRepository<Post, Long> {

    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query("update Post p set p.status = :s where p.createdOn < :d")
    int archiveOlderThan(@Param("s") Status s, @Param("d") LocalDateTime d);
}
```

여기 두 개의 옵션이 보인다. `clearAutomatically`와 `flushAutomatically`. 이게 무엇을 하는지 짚어두자. 그러지 않으면 한 가지 함정에 빠진다.

벌크 UPDATE은 *PersistenceContext를 우회한다*. SQL이 DB에 바로 나간다. 그러니 PersistenceContext에 이미 들어 있던 같은 row의 엔티티는 DB의 새 상태와 동기화되지 않은 채 남아 있다. 만약 그 메서드 직전에 같은 엔티티의 다른 필드를 변경해 두었는데(아직 flush 전), bulk UPDATE이 먼저 나가면, dirty checking이 다음에 flush할 때 *원래 우리 변경*을 덮어쓰면서 다른 필드까지 stale한 값으로 돌려놓을 위험이 있다.

`flushAutomatically=true`는 bulk 실행 전에 PersistenceContext의 변경분을 먼저 flush한다. `clearAutomatically=true`는 bulk 실행 후에 PersistenceContext를 clear한다. 즉 *bulk가 DB를 휘젓고 나면, 우리 메모리의 그림자는 더 이상 신뢰할 수 없으니 비우자*는 뜻이다. 두 옵션 모두 디폴트는 `false`다. 디폴트로 두면 위의 위험을 안고 가게 된다. bulk에는 두 옵션을 *함께 켜두는 게 정석*이라고 기억해두자.

자, 여기에 한 가지 더 깊은 함정이 있다. cascade다.

JPA에서 우리는 자주 이런 매핑을 본다.

```java
@OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
private List<Comment> comments = new ArrayList<>();
```

`Post`를 지우면 cascade에 의해 그 자식 `Comment`들도 자동으로 지워진다. JPA 라이프사이클의 우아한 부분이다. 그런데 이걸 *bulk delete에 기대하면 안 된다*.

```java
em.createQuery("delete from Post p where p.createdOn < :d")
  .setParameter("d", oneYearAgo)
  .executeUpdate();
```

이 한 줄로 50만 건의 Post를 지웠다고 해보자. 그런데 그 Post들의 자식 Comment는 어떻게 됐을까. **그대로 남는다.** cascade는 *엔티티 라이프사이클*을 통해 일어나는 동작이다. JPA가 자식들을 메모리에 올려서, 각각 `remove`를 부르고, 그 결과로 DELETE이 나가는 식이다. bulk delete은 그 과정을 통째로 건너뛴다. SQL 한 줄로 DB에 가서, 부모 row만 지운다. 자식은 모른 채.

Vlad의 한 줄이 정곡을 찌른다. *"Using CascadeType.REMOVE and orphanRemoval is pointless for bulk operations."* 불행히도 우리는 이 사실을 모른 채 bulk를 쓰는 자리가 많다. 외래키 제약이 있으면 그나마 DB가 거절해 줘서 알게 되는데, 외래키가 없거나 NULLABLE이면 *자식이 부모를 잃고 고아로 남는다*. 데이터 정합성이 조용히 무너진다. 시간이 한참 지난 뒤에야 발견된다. 끔찍한 일이다.

그렇다면 어떻게 해야 할까. 두 가지 길이 있다.

첫째, 자식부터 명시적으로 지운다. 부모를 지우기 전에 자식의 bulk delete을 먼저 실행한다.

```java
em.createQuery("""
    delete from Comment c
    where c.post.id in (
        select p.id from Post p where p.createdOn < :d
    )""")
  .setParameter("d", oneYearAgo)
  .executeUpdate();

em.createQuery("delete from Post p where p.createdOn < :d")
  .setParameter("d", oneYearAgo)
  .executeUpdate();
```

두 줄이지만 명확하다. 자식의 cascade를 *JPA가 아니라 우리가 손으로* 표현한 셈이다.

둘째, *DB 외래키에 `ON DELETE CASCADE`를 위임한다*. DDL에서 외래키 제약에 `ON DELETE CASCADE`를 걸어두면, 부모 row가 삭제될 때 DB가 자식 row를 자동으로 지운다. JPA의 cascade와 거의 같은 역할을 DB 레벨에서 하는 셈이다. bulk delete이든 단건 delete이든, DB가 자기 책임으로 자식까지 함께 처리해준다. 정합성이 SQL 표준 위에서 보장된다는 이점이 크다.

```sql
ALTER TABLE comment
    ADD CONSTRAINT fk_comment_post
    FOREIGN KEY (post_id) REFERENCES post(id)
    ON DELETE CASCADE;
```

대량 삭제가 빈번한 도메인에서는 두 번째 방식을 강하게 추천한다. JPA cascade는 우아하지만, bulk와는 궁합이 맞지 않는다. 이걸 인정하고 책임의 한 부분을 DB에 넘기는 편이 깔끔하다.

## 동적인 벌크가 필요할 때 — Criteria와 Blaze

지금까지의 bulk JPQL은 *문자열로* 짜는 방식이었다. 컴파일 타임에 SQL 형태가 정해진다. 그런데 어떤 자리는 조건이 런타임에 결정된다. 검색 화면에서 한꺼번에 status 변경 같은 기능이 그렇다. 사용자가 어떤 필터를 걸었느냐에 따라 WHERE 절이 달라진다. 이럴 때 JPQL 문자열을 손으로 짜 붙이면, 보안과 가독성이 모두 흔들린다.

JPA 2.1부터 표준에 `CriteriaUpdate`와 `CriteriaDelete`가 들어왔다. 타입 안전한 동적 bulk다.

```java
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaUpdate<Post> update = cb.createCriteriaUpdate(Post.class);
Root<Post> root = update.from(Post.class);

update.set(root.get("status"), Status.ARCHIVED);
if (oneYearAgo != null) {
    update.where(cb.lessThan(root.get("createdOn"), oneYearAgo));
}

int affected = em.createQuery(update).executeUpdate();
```

문자열 concatenation 없이 동적으로 WHERE을 조립할 수 있다. 다만 익숙해지기 전엔 코드가 좀 장황하게 느껴진다. *진짜로 동적인* bulk 경로에만 활용하자.

여기서 한 발 더 나가는 라이브러리가 Blaze-Persistence Bulk다. PostgreSQL의 `RETURNING`, SQL Server의 `OUTPUT` 같은 dialect 기능과 함께 *bulk UPDATE/DELETE이 영향을 준 row들을 그대로 회수*할 수 있다. 한 번에 UPDATE하면서 그 결과 set을 받아 다음 단계에 쓰는 패턴이 가능해진다. dialect별로 따로 native SQL을 짜야 했던 자리가 한 API로 정리된다. 5장에서 projection을 다룰 때 Blaze-Persistence가 한 번 등장했는데, bulk에서도 그 자리는 유효하다. 표준 JPA가 닫아둔 문을 여는 라이브러리라고 생각해두자.

## 단일 노드 batch의 한계 — 그 너머로 가는 첫걸음

여기까지 우리가 한 모든 일은 *한 대의 DB에서, 한 application 인스턴스가, 정해진 시간 안에 30만 건을 빠르게 끝내는* 그림이었다. SEQUENCE pooled-lo, batch 4종 세트, reWriteBatchedInserts, StatelessSession, bulk JPQL. 이 도구들을 다 적용하면 30만 건 INSERT은 분 단위에서 초 단위로 떨어진다. 보통의 야간 배치, 평균적인 데이터 임포트는 이 자리에서 충분히 해결된다.

그런데 어떤 시스템은 그 너머로 간다. 30만 건이 아니라 매일 3,000만 건의 이벤트가 쌓인다. 한 application 인스턴스가 batching을 잘해도, 단일 DB 노드의 디스크 IO 한계, WAL 처리량 한계, 인덱스 업데이트 한계에 닿는다. 라운드트립을 줄이는 도구로는 더 이상 풀리지 않는 자리가 시작된다.

그 너머의 첫걸음 두 가지를 짧게 짚어두자. 자세한 그림은 이 책의 범위를 넘는다. 다만 *어디로 발을 디뎌야 할지*는 알고 있는 게 좋다.

첫째, **읽기/쓰기 분리**다. read-only 쿼리를 read replica로 라우팅해서, primary DB의 부담을 write에 집중시킨다. 1장에서 우리는 라운드트립을 줄이라고 했지만, primary의 CPU·IO 자체가 제한이라면 라운드트립을 줄여도 답이 안 나온다. application에서 `AbstractRoutingDataSource`나 Spring의 `@Transactional(readOnly=true)` 힌트로 라우팅을 분리하는 게 첫걸음이다.

둘째, **샤딩**이다. 데이터를 키 기준으로 여러 DB 노드에 분산한다. tenant별, 지역별, hash 분포로 row를 나눈다. application은 어느 노드를 봐야 하는지 판단하고 라우팅한다. 한 application 인스턴스가 어떤 트랜잭션에서는 노드 A를, 다른 트랜잭션에서는 노드 B를 본다. Hibernate에는 `MultiTenantConnectionProvider`로 schema-per-tenant나 database-per-tenant를 비교적 자연스럽게 받쳐줄 수 있는 자리가 있다.

이 두 가지가 시작되는 자리에서, 우리가 이 책에서 다뤄온 *단일 노드 안의 라운드트립 최적화*는 여전히 베이스 라인이다. 라운드트립을 잘 줄여둔 application은, 노드를 늘렸을 때 그 효과를 그대로 곱하기로 받는다. 라운드트립이 헐거운 application은, 노드를 늘려도 노드마다 같은 비효율을 똑같이 곱한다. 그러니 batch와 단일 노드 최적화는 스케일의 *대체재가 아니라 전제 조건*이라고 생각해두자.

Vlad의 14 tips 중 마지막 자리에 "수평·수직 스케일"이 들어가 있다. 그 자리는 한 책의 끝이라기보다는 *다음 여정의 시작점*이다. 이 장은 그 시작점 앞까지 우리를 데려다주는 마지막 도구 모음이다.

## 마무리 — 자기 코드를 확인하는 세 가지

이번 장은 무겁기보다 실용적이었다. 마지막으로 자기 코드에 대고 던질 세 가지 질문을 정리해두자. 다음 PR 리뷰나 `application.yml` 점검 때 그대로 쓸 수 있도록 짧게 두자.

**첫째, `hibernate.jdbc.batch_size`만 켜두고 만족하고 있지는 않은가.** `order_inserts`, `order_updates`, `batch_versioned_data`까지 네 개가 *함께 켜져 있어야* 정상이다. 한 줄만 켜둔 채 "우리는 batch 켰어요"라고 안심해온 시스템이 의외로 많다. `application.yml`을 다시 열어보자. PostgreSQL이라면 JDBC URL의 `reWriteBatchedInserts=true`까지 함께. MySQL이라면 `rewriteBatchedStatements=true`까지 함께.

**둘째, 대량 INSERT 경로에 `flush()` + `clear()` 루프가 있는가.** 한 트랜잭션 안에 수천 건을 `persist`만 하고 끝에 commit으로 몰아 flush를 부르는 코드는, PersistenceContext가 자꾸 무거워지면서 결국 OOM과 dirty checking 비대화로 이어진다. 25개나 50개마다 flush/clear을 끼워두자. 메모리가 평탄해진다.

**셋째, 대량 ingest 경로에 StatelessSession을 검토해 봤는가.** ETL, CSV 임포트, 외부 데이터 적재처럼 *엔티티 그래프 cascade가 필요 없는* 자리는 StatelessSession이 정답에 가깝다. Hibernate 6.3 이후로 batch도 지원되고, 6.4에서는 UPSERT도 들어왔다. 한 번 검토만 해봐도 의외로 많은 ingest 경로가 이 도구로 단순해진다.

이 세 가지를 점검하고 나면, 30만 건 INSERT이 30분이 아니라 1분에 끝나는 환경의 *베이스 라인*은 갖춰진 셈이다. 그 위에서 어떤 시스템은 1분도 너무 길다고 느껴 노드를 늘리는 길로 가고, 어떤 시스템은 1분이면 충분하다고 끄덕이며 다른 자리를 살핀다. 어느 길을 가든, 라운드트립을 줄이는 이 도구들은 다음 자리에서 다시 만난다.

자, 그러면 다음 장으로 넘어가보자. write의 batch가 끝났으니 이번엔 read의 batch — 라기보다는, read의 *깊이*에 관한 이야기다. 페이지네이션. 첫 페이지는 빠른데 500페이지로 가면 응답이 무너지는 그 자리, OFFSET 10,000을 넘기는 순간 왜 시간이 폭발하는지, 그리고 무한 스크롤을 *깊이와 무관하게* 만들 수 있는 keyset이라는 도구를 살펴보자.
