# 10장. JPA를 넘어 — 성능·동시성·락 패턴·배치

이 챕터는 락의 **애플리케이션 패턴**을 다룬다. 락 메커니즘은 3장에서 보았다.

어느 날 갑자기 배포 슬랙 채널에 메시지가 올라온다. "오늘 오후 정산 배치 돌렸는데 왜 이렇게 오래 걸리죠?" 담당자를 찾아보니 기존엔 3분이면 끝나던 INSERT가 갑자기 37분을 넘겼다. 코드는 어제와 똑같다. DB 서버 CPU는 10%대. 그런데 느리다.

원인을 파고들어 보면 `@GeneratedValue(strategy = GenerationType.IDENTITY)` 한 줄이 문제다. 9장에서 JPA의 일상 함정들을 살펴봤다면, 이 장에서는 그 함정을 넘어 성능을 진짜로 뽑아내는 방법을 알아보자. 배치 성능, 수백만 row를 건드리는 UPDATE/DELETE, 트랜잭션 경계 설계, 그리고 named lock을 이용한 분산락 패턴까지 — JPA가 버거워지는 지점에서 우리는 어디로 내려가야 하는지를 함께 따라가보자.

---

## 배치 INSERT 100배 — 세 가지 설정의 합주

배치 INSERT 성능 문제를 한 번이라도 겪어본 사람은 안다. `saveAll()` 한 줄로 리스트를 던졌는데 개별 INSERT가 낱개로 나간다. 1,000건이면 1,000번의 왕복. 찜찜하지 않은가?

우아한형제들 기술블로그에 기록된 사례를 보자. 배치 INSERT 성능을 100배 끌어올린 핵심은 세 가지 설정이었다.

```yaml
# application.yml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
```

```properties
# JDBC URL에 반드시 추가
spring.datasource.url=jdbc:mysql://localhost:3306/mydb?rewriteBatchedStatements=true
```

이 세 가지가 **모두** 켜져야 진짜 배치 INSERT가 일어난다. 하나라도 빠지면 겉보기에는 배치처럼 보여도 실제로는 낱개 INSERT가 나간다. 특히 `rewriteBatchedStatements=true`가 빠지면 JDBC 드라이버가 배치 요청을 개별 `INSERT`로 펼쳐서 보내기 때문에 DB 왕복 횟수가 줄지 않는다.

그런데 여기서 한 가지 난감한 지점이 생긴다. `@GeneratedValue(strategy = GenerationType.IDENTITY)` 전략은 배치와 함께 쓸 수 없다.

### IDENTITY 전략이 배치를 막는 이유

IDENTITY 전략은 INSERT 직후 DB가 생성한 PK를 바로 가져와야 한다. Hibernate는 이 PK를 영속성 컨텍스트에서 즉시 추적해야 하므로, INSERT 직후 `LAST_INSERT_ID()`를 호출해 PK를 알아낸다. 이 흐름 자체가 배치를 불가능하게 만든다 — 배치는 여러 INSERT를 묶어서 한 번에 보내는 것인데, 각 INSERT가 끝날 때마다 PK를 받아야 하니 묶을 수가 없다.

해결책은 SEQUENCE 또는 TABLE 전략으로 바꾸는 것이다. MySQL은 기본 SEQUENCE를 지원하지 않으므로 `TABLE` 전략을 쓰거나, Hibernate의 `pooled` 시퀀스 알로케이터를 직접 구성한다.

```java
// IDENTITY에서 TABLE 전략으로 변경
@Entity
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.TABLE,
                    generator = "order_item_seq")
    @TableGenerator(
        name = "order_item_seq",
        table = "hibernate_sequences",
        pkColumnName = "sequence_name",
        valueColumnName = "next_val",
        allocationSize = 50  // 50개씩 미리 채번
    )
    private Long id;

    // ...
}
```

allocationSize를 50으로 잡으면 DB에 한 번 접근할 때마다 50개의 ID를 미리 채번해 메모리에 들고 있는다. DB 채번 빈도를 줄이면서도 유일성을 보장한다.

### JdbcTemplate으로 더 깔끔하게

JPA 엔티티 매핑이 복잡한 상황이라면 JdbcTemplate의 `batchUpdate()`를 직접 쓰는 편이 낫다.

```java
@Repository
@RequiredArgsConstructor
public class OrderItemBatchRepository {

    private final JdbcTemplate jdbcTemplate;

    // 1,000건씩 청크로 나눠 배치 INSERT
    public void batchInsert(List<OrderItem> items) {
        String sql = "INSERT INTO order_item (order_id, product_id, quantity, price) "
                   + "VALUES (?, ?, ?, ?)";

        List<List<OrderItem>> chunks = partition(items, 1_000);

        for (List<OrderItem> chunk : chunks) {
            jdbcTemplate.batchUpdate(sql,
                new BatchPreparedStatementSetter() {
                    @Override
                    public void setValues(PreparedStatement ps, int i)
                            throws SQLException {
                        OrderItem item = chunk.get(i);
                        ps.setLong(1, item.getOrderId());
                        ps.setLong(2, item.getProductId());
                        ps.setInt(3, item.getQuantity());
                        ps.setBigDecimal(4, item.getPrice());
                    }

                    @Override
                    public int getBatchSize() {
                        return chunk.size();
                    }
                });
        }
    }

    private <T> List<List<T>> partition(List<T> list, int size) {
        List<List<T>> partitions = new ArrayList<>();
        for (int i = 0; i < list.size(); i += size) {
            partitions.add(list.subList(i, Math.min(i + size, list.size())));
        }
        return partitions;
    }
}
```

1,000건 청크로 나누고 각 청크를 하나의 배치 요청으로 보낸다. `rewriteBatchedStatements=true`와 조합하면 1,000개의 INSERT 값이 하나의 멀티-row INSERT SQL로 합쳐져 나간다.

---

## 수백만 row UPDATE/DELETE — 청크 분할의 기술

"어제 배포에서 `status = 'EXPIRED'`인 주문 데이터를 정리해야 한다"는 요구가 왔다. 테이블에는 4,500만 건이 있고, 그중 만료된 것이 800만 건쯤 된다. 한 트랜잭션에서 `DELETE FROM order WHERE status = 'EXPIRED'`를 날린다고 생각해보자. 끔찍한 일이다.

왜 끔찍할까? 세 가지 이유가 있다.

첫째, 트랜잭션이 종료되기 전까지 삭제 대상 행 전체에 락이 걸린다. 800만 건에 걸린 레코드 락은 다른 트랜잭션들을 한없이 기다리게 만든다.

둘째, binlog에 800만 건의 DELETE row가 쌓이면 리플리카가 그것을 받아 처리하는 동안 복제 lag이 폭발한다. 운영 중에 리플리카가 수 분씩 뒤처지기 시작하면 읽기 요청을 리플리카로 분산시키는 구조 전체가 흔들린다.

셋째, InnoDB의 undo 로그가 급격히 불어나 버퍼풀을 압박한다.

해결책은 간단하다. 작게 잘라서, 짧은 트랜잭션으로, 천천히.

```java
@Service
@RequiredArgsConstructor
public class OrderCleanupService {

    private final JdbcTemplate jdbcTemplate;

    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    public void deleteExpiredOrdersInChunks() {
        long lastId = 0;
        int chunkSize = 1_000;
        int totalDeleted = 0;

        while (true) {
            // 각 청크는 별도 트랜잭션으로 처리
            int deleted = deleteChunk(lastId, chunkSize);
            totalDeleted += deleted;

            if (deleted < chunkSize) {
                break; // 더 삭제할 것 없음
            }

            // 다음 청크의 시작 ID 계산
            lastId = getLastDeletedId(lastId, chunkSize);

            // 리플리카 lag 완화를 위한 짧은 대기
            sleepQuietly(50); // 50ms
        }

        log.info("총 {}건 삭제 완료", totalDeleted);
    }

    @Transactional
    public int deleteChunk(long fromId, int limit) {
        return jdbcTemplate.update(
            "DELETE FROM orders WHERE id > ? AND status = 'EXPIRED' "
          + "ORDER BY id LIMIT ?",
            fromId, limit
        );
    }
}
```

`ORDER BY id LIMIT ?` 패턴이 핵심이다. id 순서로 정렬해 앞에서부터 잘라내면 각 DELETE 트랜잭션의 크기가 예측 가능해지고, 락 유지 시간도 짧아진다. 청크 사이 50ms 대기는 리플리카가 따라잡을 시간을 주는 일종의 배려다.

물론 이 방식은 전체 작업 시간이 길어진다. 하지만 운영 중인 서비스를 멈추지 않고 진행할 수 있다는 장점이 그것을 훨씬 압도한다.

---

## 트랜잭션 경계 설계 — 외부 IO를 트랜잭션 밖으로

결제 처리 코드를 보면 이런 패턴이 자주 등장한다.

```java
// 찜찜한 패턴: 외부 API 호출이 트랜잭션 안에 있다
@Transactional
public void processPayment(PaymentRequest request) {
    Order order = orderRepository.findById(request.getOrderId())
        .orElseThrow();
    
    // DB 락을 잡고 있는 상태에서 외부 API 호출!
    PaymentResult result = pgClient.charge(request); // 이게 2초 걸리면?
    
    Payment payment = Payment.of(order, result);
    paymentRepository.save(payment);
    order.complete();
}
```

외부 결제 PG API 호출이 트랜잭션 안에 있다. 만약 PG사 API가 일시적으로 느려져 2초 걸린다면, 그 2초 동안 해당 주문에 대한 DB 락이 유지된다. 동시에 같은 주문에 접근하려는 다른 요청은 2초를 기다려야 한다. 트래픽이 몰리면 대기 중인 트랜잭션이 쌓이고, 커넥션 풀이 고갈된다.

올바른 패턴은 외부 IO를 트랜잭션 바깥으로 빼는 것이다.

```java
// 개선된 패턴: 외부 IO를 트랜잭션 밖으로
@Service
@RequiredArgsConstructor
public class PaymentService {

    private final OrderRepository orderRepository;
    private final PaymentRepository paymentRepository;
    private final PgClient pgClient;

    // 트랜잭션 없이: 외부 API 먼저 호출
    public PaymentResult processPayment(PaymentRequest request) {
        // 1단계: 트랜잭션 없이 외부 API 호출
        PaymentResult result = pgClient.charge(request);
        
        // 2단계: 짧은 트랜잭션으로 DB 처리
        return savePaymentResult(request.getOrderId(), result);
    }

    @Transactional
    protected PaymentResult savePaymentResult(Long orderId, PaymentResult result) {
        Order order = orderRepository.findById(orderId).orElseThrow();
        Payment payment = Payment.of(order, result);
        paymentRepository.save(payment);
        order.complete();
        return result;
    }
}
```

외부 API 호출이 얼마나 걸리든 그것은 DB 트랜잭션과 무관하다. DB 트랜잭션은 결과를 저장하는 짧은 순간만 유지된다.

### JPA와 JdbcTemplate을 한 트랜잭션에서 손잡기

가끔 JPA로 엔티티를 저장하고 같은 트랜잭션 안에서 JdbcTemplate으로 네이티브 SQL을 쓰고 싶을 때가 있다. 이 경우 주의할 점이 있다. JPA의 변경 감지는 flush 시점에 SQL을 생성하는데, 그 전에 JdbcTemplate으로 같은 테이블을 조회하면 아직 반영되지 않은 상태를 읽을 수 있다.

```java
@Transactional
public void hybridOperation(Long orderId) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    order.updateStatus(OrderStatus.PROCESSING);
    
    // JPA 변경을 DB에 먼저 반영
    entityManager.flush();
    
    // 이제 JdbcTemplate으로 같은 데이터를 정확히 읽을 수 있다
    int relatedCount = jdbcTemplate.queryForObject(
        "SELECT COUNT(*) FROM order_item WHERE order_id = ? AND status = 'ACTIVE'",
        Integer.class, orderId
    );
    
    // relatedCount를 기반으로 추가 처리
    if (relatedCount > 0) {
        jdbcTemplate.update(
            "UPDATE order_item SET status = 'PROCESSING' WHERE order_id = ?",
            orderId
        );
    }
}
```

`entityManager.flush()` 호출이 핵심이다. JPA pending 쓰기를 DB에 반영한 뒤 JdbcTemplate으로 조회하면 최신 상태를 정확히 읽는다. 이 패턴은 JPA와 native SQL이 같은 트랜잭션에서 공존할 수 있게 하는 다리다.

---

## 낙관적 락 — `@Version`과 재시도

충돌이 드문 상황에서는 낙관적 락이 좋은 선택이다. 잠금을 걸지 않으니 대기가 없고, 처리량도 높다. 대신 충돌이 발생하면 예외를 던지므로 재시도 로직이 필요하다.

```java
@Entity
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private int stockQuantity;

    @Version
    private Long version; // 낙관적 락의 버전 컬럼

    public void decreaseStock(int quantity) {
        if (this.stockQuantity < quantity) {
            throw new InsufficientStockException();
        }
        this.stockQuantity -= quantity;
    }
}
```

```java
// 재시도 로직을 @Retryable로 선언
@Service
@RequiredArgsConstructor
public class StockService {

    private final ProductRepository productRepository;

    @Retryable(
        retryFor = OptimisticLockingFailureException.class,
        maxAttempts = 3,
        backoff = @Backoff(delay = 100, multiplier = 2)
    )
    @Transactional
    public void decreaseStock(Long productId, int quantity) {
        Product product = productRepository.findById(productId)
            .orElseThrow();
        product.decreaseStock(quantity); // version 불일치 시 예외
    }

    @Recover
    public void handleOptimisticLockFailure(
            OptimisticLockingFailureException e, Long productId, int quantity) {
        log.error("재고 감소 최종 실패: productId={}, quantity={}", productId, quantity);
        throw new StockUpdateFailedException("재고 업데이트에 실패했습니다. 잠시 후 다시 시도해주세요.");
    }
}
```

낙관적 락의 재시도 페이로드는 **멱등(idempotent)** 이어야 한다. 같은 요청을 세 번 재시도해도 결과가 하나여야 한다는 뜻이다. 재시도마다 새 엔티티를 만들거나 중복 처리를 허용하는 설계라면 낙관적 락과 재시도의 조합이 오히려 위험하다.

버전 컬럼은 INSERT 시 0으로 시작해 UPDATE마다 1씩 증가한다. 두 트랜잭션이 같은 버전으로 UPDATE를 시도하면 하나만 성공하고 나머지는 `OptimisticLockingFailureException`을 받는다. 이것이 낙관적 락의 전부다.

---

## 비관적 락 — `@Lock(PESSIMISTIC_WRITE)`

충돌이 잦고 재시도 비용이 높다면 비관적 락이 낫다. 읽는 시점부터 독점 락을 걸어 다른 트랜잭션이 기다리게 만든다.

```java
// 레포지토리: 비관적 락으로 조회
public interface ProductRepository extends JpaRepository<Product, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithLock(@Param("id") Long id);

    // 타임아웃 설정 (10초)
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints({
        @QueryHint(name = "jakarta.persistence.lock.timeout", value = "10000")
    })
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdWithLockAndTimeout(@Param("id") Long id);
}
```

```java
@Service
@RequiredArgsConstructor
public class FlashSaleService {

    private final ProductRepository productRepository;

    @Transactional
    public void processPurchase(Long productId, int quantity) {
        // SELECT ... FOR UPDATE
        Product product = productRepository.findByIdWithLock(productId)
            .orElseThrow(() -> new ProductNotFoundException(productId));

        product.decreaseStock(quantity);
        // 트랜잭션 종료 시 락 해제
    }
}
```

`@Lock(LockModeType.PESSIMISTIC_WRITE)`은 `SELECT ... FOR UPDATE`를 생성한다. 이 트랜잭션이 종료될 때까지 같은 row를 건드리려는 다른 트랜잭션은 기다린다.

비관적 락의 주의점은 **락 획득 대기 시간**이다. 기다리다가 `LockTimeoutException`이 발생할 수 있으므로 타임아웃을 명시하는 편이 낫다. 타임아웃 없이 쓰면 무한 대기가 될 수 있다 — 그것도 꽤 난감한 상황이다.

또 한 가지. 비관적 락은 레코드 단위다. 같은 상품을 여러 트랜잭션이 동시에 구매하려면 이들이 줄 서서 기다린다. 이 대기 시간이 너무 길어지면 커넥션 풀이 고갈된다. 순간 트래픽 집중이 예상된다면 named lock 분산락 패턴을 고려해볼 필요가 있다.

---

## MySQL Named Lock — 분산락의 실용 패턴

여러 애플리케이션 인스턴스가 같은 리소스를 동시에 처리하지 않아야 할 때, 가장 간단한 분산락 매개체는 MySQL named lock이다.

`GET_LOCK("ad:campaign:42", 10)`은 "ad:campaign:42"라는 이름의 락을 최대 10초 기다려서 획득한다. 성공하면 1, 실패하면 0을 반환한다. `RELEASE_LOCK("ad:campaign:42")`로 해제한다.

우아한형제들은 광고 시스템에서 이 패턴을 실제로 운영했다. 핵심 인사이트는 두 가지다.

첫째, **락 획득용 커넥션 풀을 비즈니스 로직 풀과 반드시 분리**해야 한다. named lock은 커넥션에 묶인다. 비즈니스 커넥션 풀로 락을 잡으면 락을 들고 있는 커넥션이 풀을 점유해 다른 비즈니스 처리가 커넥션을 못 얻는 상황이 생긴다.

둘째, MySQL 5.7.5 미만에서는 한 세션에서 하나의 named lock만 유지된다. `GET_LOCK("lock_b")`를 다시 호출하면 이전에 잡은 `lock_a`가 자동으로 해제된다 — 모르고 쓰면 대형 사고다.

```java
// 별도 커넥션 풀 설정
@Configuration
public class LockDataSourceConfig {

    @Bean(name = "lockDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.lock")
    public DataSource lockDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name = "lockJdbcTemplate")
    public JdbcTemplate lockJdbcTemplate(
            @Qualifier("lockDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```

```yaml
# application.yml: 락 전용 커넥션 풀
spring:
  datasource:
    lock:
      url: jdbc:mysql://localhost:3306/mydb?rewriteBatchedStatements=true
      username: app_user
      password: secret
      hikari:
        pool-name: lock-pool
        maximum-pool-size: 10  # 비즈니스 풀보다 훨씬 작게
        minimum-idle: 2
```

```java
@Component
@RequiredArgsConstructor
public class MysqlNamedLockManager {

    @Qualifier("lockJdbcTemplate")
    private final JdbcTemplate lockJdbcTemplate;

    private static final int DEFAULT_TIMEOUT_SECONDS = 10;

    // 락 획득 후 작업 실행, 반드시 해제
    public <T> T executeWithLock(String lockName, Supplier<T> task) {
        return executeWithLock(lockName, DEFAULT_TIMEOUT_SECONDS, task);
    }

    public <T> T executeWithLock(String lockName, int timeoutSeconds, Supplier<T> task) {
        boolean acquired = acquireLock(lockName, timeoutSeconds);
        if (!acquired) {
            throw new LockAcquisitionException("락 획득 실패: " + lockName);
        }
        try {
            return task.get();
        } finally {
            releaseLock(lockName); // 예외가 나도 반드시 해제
        }
    }

    private boolean acquireLock(String lockName, int timeoutSeconds) {
        Integer result = lockJdbcTemplate.queryForObject(
            "SELECT GET_LOCK(?, ?)",
            Integer.class, lockName, timeoutSeconds
        );
        return Integer.valueOf(1).equals(result);
    }

    private void releaseLock(String lockName) {
        lockJdbcTemplate.queryForObject(
            "SELECT RELEASE_LOCK(?)",
            Integer.class, lockName
        );
    }
}
```

```java
// 사용 예시: 광고 캠페인 예산 차감
@Service
@RequiredArgsConstructor
public class AdBudgetService {

    private final MysqlNamedLockManager lockManager;
    private final CampaignRepository campaignRepository;

    public void deductBudget(Long campaignId, BigDecimal amount) {
        String lockName = "ad:campaign:" + campaignId;

        lockManager.executeWithLock(lockName, () -> {
            Campaign campaign = campaignRepository.findById(campaignId)
                .orElseThrow();
            campaign.deductBudget(amount);
            campaignRepository.save(campaign);
            return null;
        });
    }
}
```

`Supplier<T>` 콜백으로 작업을 감싸면 락 획득/해제 책임이 `MysqlNamedLockManager`에 집중된다. 비즈니스 코드는 락이 어떻게 구현됐는지 신경 쓸 필요 없이 콜백만 건네면 된다.

락 이름은 리소스를 고유하게 식별해야 한다. `"ad:campaign:42"`처럼 도메인 + 구분자 + ID 조합이 좋다. 락 이름이 너무 짧거나 범용적이면 의도하지 않은 충돌이 생긴다.

### Named Lock vs Redis Redlock

MySQL named lock과 Redis Redlock은 둘 다 분산락이지만 성격이 다르다.

| 관점 | MySQL Named Lock | Redis Redlock |
|------|-----------------|---------------|
| 일관성 | DB 트랜잭션과 묶임 → 보수적 | 분리된 저장소 → 별도 관리 |
| 속도 | DB 왕복 비용 있음 | 메모리 기반 → 빠름 |
| 운영 복잡도 | 이미 MySQL 있으면 추가 인프라 없음 | Redis 별도 운영 필요 |
| 락 만료 | 세션 종료 시 자동 해제 | TTL 기반 자동 만료 |
| 장애 내성 | MySQL이 단일 장애점 | Redis 클러스터로 HA 가능 |

이미 MySQL을 쓰고 있고, 락 빈도가 높지 않으며, 일관성을 더 중요하게 여긴다면 MySQL named lock이 간단하고 안전한 선택이다. 반면 락 빈도가 높고 성능이 중요하다면 Redis Redlock을 고려해볼 수 있다. 어느 쪽이 "더 낫다"고 단정하기보다, 우리 워크로드의 특성을 먼저 파악하는 편이 낫다.

---

## 락 순서 일관성 — 데드락 사이클 차단

코드에 비관적 락을 쓰는 곳이 여러 군데 있다면 락 순서를 일관되게 유지해야 한다. 3장에서 데드락 메커니즘을 보았듯이, 두 트랜잭션이 서로 다른 순서로 락을 획득하려 하면 사이클이 생긴다.

고전적인 예시다. 트랜잭션 A는 먼저 계좌 1을 잠그고 그다음 계좌 2를 잠그려 한다. 트랜잭션 B는 먼저 계좌 2를 잠그고 그다음 계좌 1을 잠그려 한다. 이들이 동시에 실행되면 사이클이 생긴다.

```java
// 데드락 위험: 락 순서가 보장되지 않음
@Transactional
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    Account from = accountRepository.findByIdWithLock(fromId).orElseThrow();
    Account to = accountRepository.findByIdWithLock(toId).orElseThrow();
    from.withdraw(amount);
    to.deposit(amount);
}

// 개선: 정렬된 순서로 락 획득
@Transactional
public void transferSafe(Long fromId, Long toId, BigDecimal amount) {
    // ID가 작은 쪽을 먼저 잠근다
    Long firstId = Math.min(fromId, toId);
    Long secondId = Math.max(fromId, toId);

    Account first = accountRepository.findByIdWithLock(firstId).orElseThrow();
    Account second = accountRepository.findByIdWithLock(secondId).orElseThrow();

    Account from = fromId.equals(firstId) ? first : second;
    Account to = toId.equals(firstId) ? first : second;

    from.withdraw(amount);
    to.deposit(amount);
}
```

항상 id가 작은 계좌를 먼저 잠그면, 어떤 두 트랜잭션이 같은 두 계좌를 건드리더라도 같은 순서로 락을 획득한다. 데드락 사이클 자체가 생기지 않는다.

이 원칙을 더 넓게 적용하면 "여러 리소스를 동시에 잠가야 할 때는 항상 정렬된 순서로"가 된다. 주문 → 재고 → 계좌 순서를 애플리케이션 전체에서 일관되게 유지하면 이 종류의 데드락은 원천 차단된다.

---

## 영속성 컨텍스트와 배치 처리 — flush/clear의 타이밍

배치 처리 중 만 단위 엔티티가 영속성 컨텍스트에 쌓이면 어떻게 될까? 힙 메모리가 폭발하거나, 1차 캐시에서 같은 엔티티를 계속 찾느라 처리 속도가 떨어진다.

```java
@Service
@RequiredArgsConstructor
public class ProductSyncService {

    private final EntityManager entityManager;
    private final ProductRepository productRepository;

    @Transactional
    public void syncProducts(List<ProductData> dataList) {
        int batchSize = 100;

        for (int i = 0; i < dataList.size(); i++) {
            ProductData data = dataList.get(i);
            Product product = Product.from(data);
            entityManager.persist(product);

            // 100건마다 flush + clear
            if (i % batchSize == 0) {
                entityManager.flush();  // DB에 반영
                entityManager.clear();  // 1차 캐시 비움
            }
        }

        // 남은 것 처리
        entityManager.flush();
    }
}
```

`flush()`와 `clear()`를 100건 단위로 주기적으로 호출하면 영속성 컨텍스트에 쌓이는 엔티티 수를 통제할 수 있다. `flush()`는 변경을 DB에 반영하고, `clear()`는 1차 캐시를 비운다. 이 둘이 한 쌍이다. `clear()` 없이 `flush()`만 하면 엔티티가 메모리에서 계속 쌓인다.

기억해두자. 배치 처리 중 `OutOfMemoryError`가 난다면 십중팔구 주기적인 `flush()`와 `clear()`가 빠졌기 때문이다.

---

## 마무리

JPA는 편리하다. 하지만 그 편리함의 이면을 알아야 한계를 현명하게 넘을 수 있다.

배치 INSERT 100배 개선은 세 가지 설정의 합주였다. `jdbc.batch_size`, `order_inserts`, `rewriteBatchedStatements`가 모두 켜져야 한다. IDENTITY 전략은 배치의 적이다. 수백만 row를 지워야 한다면 한 방에 날리지 말고 청크로 나눠야 한다. 외부 IO는 트랜잭션 밖으로 빼야 한다.

낙관적 락은 충돌이 드물 때, 비관적 락은 충돌이 잦을 때. 두 인스턴스 이상에서 같은 리소스를 건드린다면 named lock을 고려해보자. 그때 커넥션 풀 분리를 빠뜨리면 락이 비즈니스 커넥션을 잡아먹는다.

락 순서는 애플리케이션 전체에서 일관되게 유지해야 데드락 사이클이 생기지 않는다. 배치 중 영속성 컨텍스트가 폭발하지 않으려면 `flush()`와 `clear()`를 주기적으로 호출하자.

다음 장에서는 데이터베이스 인프라로 시야를 넓힌다. AWS RDS와 Aurora 사이의 분기점 — 어떤 워크로드에서 어떤 선택이 맞는지를 함께 따져보자.

---

## 참고 자료

- 우아한형제들 — 하이버네이트 배치 설정: https://techblog.woowahan.com/2695/
- 우아한형제들 — MySQL을 이용한 분산락: https://techblog.woowahan.com/2631/
- 권남이 위키 — MySQL User Lock: https://kwonnam.pe.kr/wiki/database/mysql/user_lock
- haon.blog — MySQL 네임드 락으로 분산 환경에서의 동시성 이슈 해결: https://haon.blog/database/named-lock/
- Baeldung — Optimistic Locking in JPA: https://www.baeldung.com/jpa-optimistic-locking
- CodeWiz — Locking strategies in Spring Boot: https://codewiz.info/blog/locking-strategies-spring-boot/
- Medium — Spring Boot JPA Bulk Insert Performance by 100 times: https://dev.to/amrutprabhu/spring-boot-jpa-bulk-insert-performance-by-100-times-fn4
