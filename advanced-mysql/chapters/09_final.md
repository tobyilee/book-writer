# 9장. JPA로 MySQL 다루기 — 영속성 기본기와 함정

JPA를 처음 배울 때 느끼는 매력은 명확하다. SQL을 직접 쓰지 않아도 된다. 엔티티를 저장하고 꺼내는 것이 자바 코드처럼 느껴진다. 복잡한 JOIN도 연관 관계 설정으로 해결되는 것 같다. 그런데 실제 서비스를 운영하다 보면 이 편안함의 이면을 하나씩 마주하게 된다.

"N+1이 왜 이렇게 많이 나와요?" "페이지네이션이 갑자기 메모리를 1GB 잡아먹어요." "배치 처리가 왜 이렇게 느리죠?" 각각의 문제는 JPA가 만들어주는 추상과 MySQL이 실제로 실행하는 SQL 사이의 거리에서 나온다.

JPA의 일상 함정을 함께 풀어보자. 배치·동시성·락 패턴은 다음 장의 몫이다.

## JPA + native SQL 하이브리드 — 어디서 무엇을 쓸 것인가

JPA를 쓰면 모든 DB 접근을 JPA로 해야 한다는 의무는 없다. Vlad Mihalcea, Thorben Janssen 같은 JPA 전문가들이 공통으로 권고하는 접근이 있다.

**CRUD와 단일 애그리거트 영속화 → JPA**
엔티티 하나를 저장하고, 수정하고, 삭제하는 것. 또는 단일 애그리거트 루트를 통해 하위 항목들을 같이 다루는 것. JPA의 영속성 컨텍스트와 변경 감지가 여기서 빛을 발한다.

**N개 테이블 조인 + 집계 보고서 → JdbcTemplate 또는 MyBatis**
5개 테이블을 JOIN하고 GROUP BY로 집계하는 보고서 쿼리를 JPA JPQL로 작성하면 어떻게 될까. 가능은 하지만 SQL로 쓰는 것보다 복잡하고, 옵티마이저에 의도를 정확히 전달하기 어려울 때도 있다. 이런 쿼리는 JdbcTemplate로 native SQL을 쓰는 편이 낫다.

**bulk UPDATE/DELETE → JdbcTemplate batchUpdate 또는 native**
JPA로 100만 건을 UPDATE하려면 100만 개 엔티티를 메모리에 올려 각각 변경하고 flush해야 한다. native `UPDATE orders SET status = 'CLOSED' WHERE created_at < ?`가 100배 빠르다.

이 세 가지 구분을 팀 안에서 명시적으로 합의해두면 "JPA로 해야 하나 SQL로 해야 하나"라는 논쟁이 줄어든다.

```java
// CRUD는 JPA Repository
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    // Spring Data JPA 기본 메서드들
    Optional<Order> findByIdAndUserId(Long id, Long userId);
}

// 보고서 쿼리는 JdbcTemplate
@Repository
public class OrderReportRepository {

    private final JdbcTemplate jdbcTemplate;

    public List<DailySalesSummary> findDailySalesSummary(LocalDate from, LocalDate to) {
        String sql = """
            SELECT DATE(created_at) AS order_date,
                   COUNT(*) AS order_count,
                   SUM(total_amount) AS total_revenue
            FROM orders
            WHERE status = 'COMPLETED'
              AND created_at >= ? AND created_at < ?
            GROUP BY DATE(created_at)
            ORDER BY order_date
            """;

        return jdbcTemplate.query(sql,
            (rs, rowNum) -> new DailySalesSummary(
                rs.getDate("order_date").toLocalDate(),
                rs.getInt("order_count"),
                rs.getBigDecimal("total_revenue")
            ),
            from, to.plusDays(1)
        );
    }
}
```

한 트랜잭션에서 JPA와 JdbcTemplate을 함께 쓸 때 주의할 점이 있다. JPA는 영속성 컨텍스트에 변경 사항을 모아두다가 flush 시점에 SQL을 실행한다. JdbcTemplate은 바로 실행한다. 그래서 JPA로 뭔가를 수정하고 JdbcTemplate으로 그 결과를 읽으면 아직 flush가 안 된 변경을 보지 못할 수 있다. 이럴 때는 JdbcTemplate 호출 전에 `entityManager.flush()`를 호출해 JPA pending 쓰기를 먼저 동기화해두는 편이 낫다.

```java
@Service
@Transactional
public class OrderService {

    private final EntityManager entityManager;
    private final OrderRepository orderRepository;
    private final JdbcTemplate jdbcTemplate;

    public void processAndReport(Long orderId) {
        // JPA로 상태 변경
        Order order = orderRepository.findById(orderId).orElseThrow();
        order.complete();  // 상태 변경 — 아직 DB에 안 쓰임

        // JPA pending 쓰기를 DB에 반영
        entityManager.flush();

        // 이제 JdbcTemplate으로 최신 상태 조회 가능
        Long completedCount = jdbcTemplate.queryForObject(
            "SELECT COUNT(*) FROM orders WHERE status = 'COMPLETED' AND user_id = ?",
            Long.class, order.getUserId()
        );
    }
}
```

## N+1 문제 — 진단과 세 가지 도구

N+1 문제. JPA에서 가장 유명한 함정이다. 연관 관계를 LAZY 로딩으로 설정하고 목록을 조회하면, 목록 1번 쿼리 + 각 항목별 연관 엔티티 N번 쿼리, 합쳐서 N+1번 쿼리가 실행된다.

```java
// 이 코드가 N+1을 만드는 전형적인 패턴
@Entity
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)  // 기본 LAZY
    @JoinColumn(name = "user_id")
    private User user;

    // 필드들...
}

// 서비스
@Transactional(readOnly = true)
public List<OrderDto> getRecentOrders() {
    List<Order> orders = orderRepository.findTop50ByOrderByCreatedAtDesc();
    // 여기까지는 쿼리 1번

    return orders.stream()
        .map(order -> new OrderDto(
            order.getId(),
            order.getUser().getName()  // 여기서 각 order마다 user 조회 — 50번 추가 쿼리!
        ))
        .collect(toList());
}
```

50개 주문을 조회하면 주문 목록 1번 + 각 주문의 user 조회 50번 = 51번 쿼리가 된다. 슬로우 쿼리 로그에는 안 잡히는 경우가 많다(개별 쿼리가 빠르기 때문에). Hibernate의 쿼리 로그를 켜거나 APM 도구로 들여다보자.

N+1을 해결하는 도구는 크게 세 가지다.

### 1. Fetch Join

JPQL에서 INNER JOIN FETCH나 LEFT JOIN FETCH로 연관 엔티티를 한 번에 가져온다.

```java
// Repository에서 JPQL fetch join 사용
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o JOIN FETCH o.user ORDER BY o.createdAt DESC")
    List<Order> findRecentOrdersWithUser(Pageable pageable);
}
```

```sql
-- 생성되는 SQL (대략)
SELECT o.*, u.*
FROM orders o
INNER JOIN users u ON o.user_id = u.id
ORDER BY o.created_at DESC
LIMIT 50;
```

쿼리 1번으로 주문과 유저를 같이 가져온다. 단점이 있다. 컬렉션(일대다 관계)을 fetch join하면 중복 행이 생길 수 있어 DISTINCT가 필요하고, Pageable(페이지네이션)과 함께 컬렉션 fetch join은 쓰지 말자 — 이 부분은 뒤에서 자세히 본다.

### 2. EntityGraph

Spring Data JPA 애노테이션으로 fetch join을 선언적으로 지정한다.

```java
// 엔티티에 NamedEntityGraph 정의
@Entity
@NamedEntityGraph(
    name = "Order.withUser",
    attributeNodes = @NamedAttributeNode("user")
)
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    // ...
}

// Repository에서 EntityGraph 적용
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph("Order.withUser")
    List<Order> findTop50ByOrderByCreatedAtDesc();

    // 또는 ad-hoc EntityGraph
    @EntityGraph(attributePaths = {"user", "items"})
    Optional<Order> findByIdWithDetails(Long id);
}
```

EntityGraph는 fetch join과 내부적으로 비슷하게 LEFT OUTER JOIN을 발생시킨다. 인터페이스가 더 선언적이라 읽기 편하다는 장점이 있다.

### 3. @BatchSize

연관 엔티티를 한 번에 N개씩 묶어서 IN 쿼리로 조회한다. fetch join과 달리 컬렉션에도 자연스럽게 쓸 수 있다.

```java
// 전역 설정 (application.yml)
// spring.jpa.properties.hibernate.default_batch_fetch_size: 100

// 또는 엔티티에 직접 설정
@Entity
public class Order {
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    @BatchSize(size = 100)  // 100개씩 IN 쿼리로 묶어 조회
    private List<OrderItem> items;
}
```

```sql
-- @BatchSize(100) 적용 시 생성되는 쿼리
SELECT * FROM order_items WHERE order_id IN (1, 2, 3, ..., 100);
-- N+1이 아니라 N/100+1번으로 줄어든다
```

세 도구 중 무엇을 고를지는 상황 나름이다.

- **단순 다대일(ManyToOne) 조회** → fetch join 또는 EntityGraph
- **컬렉션(일대다) 조회, 페이지네이션 없음** → fetch join 또는 EntityGraph
- **컬렉션 조회 + 페이지네이션** → @BatchSize (이유는 다음 절에서)
- **여러 연관 관계가 복잡하게 얽힌 경우** → JdbcTemplate으로 native SQL이 더 명료할 때도 있다

## 페이지네이션 — OFFSET의 함정과 keyset

페이지네이션은 대부분의 목록 API에 들어간다. Spring Data JPA의 `Pageable`을 쓰면 간단하게 구현할 수 있다.

```java
// 페이지네이션 API 예시
@GetMapping("/orders")
public Page<OrderDto> getOrders(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size
) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
    return orderRepository.findAll(pageable).map(OrderDto::from);
}
```

```sql
-- 생성되는 SQL
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 0;   -- 1페이지
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 20;  -- 2페이지
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 10000;  -- 501페이지
```

1~2페이지는 빠르다. 그런데 501페이지(OFFSET 10000)는? MySQL은 `OFFSET 10000`을 처리하기 위해 10000개 행을 건너뛰고 그다음 20개를 반환한다. "건너뛰기"가 실제로는 처음 10020개 행을 읽고 앞의 10000개를 버리는 것이다. 페이지가 깊어질수록 느려진다. 100페이지가 10페이지보다 10배 느리지 않고, 실제로는 훨씬 더 느려질 수 있다.

무한 스크롤이나 관리자 화면처럼 깊은 페이지가 실제로 사용되는 경우라면 keyset pagination(seek 방식)이 답이다.

```java
// Keyset pagination — JPA JPQL
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // 마지막으로 본 created_at과 id를 기준으로 다음 페이지 조회
    @Query("""
        SELECT o FROM Order o
        WHERE o.status = 'COMPLETED'
          AND (o.createdAt < :lastCreatedAt
               OR (o.createdAt = :lastCreatedAt AND o.id < :lastId))
        ORDER BY o.createdAt DESC, o.id DESC
        """)
    List<Order> findNextPage(
        @Param("lastCreatedAt") LocalDateTime lastCreatedAt,
        @Param("lastId") Long lastId,
        Pageable pageable  // LIMIT만 적용됨, OFFSET은 0
    );
}
```

```sql
-- 생성되는 SQL
SELECT * FROM orders
WHERE status = 'COMPLETED'
  AND (created_at < '2024-01-15 10:30:00'
       OR (created_at = '2024-01-15 10:30:00' AND id < 12345))
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

OFFSET이 없다. 인덱스 `(status, created_at, id)`를 타고 바로 해당 위치로 이동해서 20개를 읽는다. 1페이지든 10000페이지든 속도가 같다.

keyset의 제약도 있다. 이전 페이지로 돌아가기가 어렵고(커서가 단방향이라), 특정 페이지 번호로 직접 이동하는 것이 불가능하다. "다음 페이지", "이전 페이지" 버튼만 있는 무한 스크롤이나 단방향 커서 방식에 어울린다.

Vlad Mihalcea와 Thorben Janssen 모두 깊은 페이지네이션에서 keyset이 절대적으로 유리하다고 강조한다. OFFSET 방식이 편리하지만 데이터가 쌓일수록 내재된 성능 문제가 드러난다.

## `findAll(Pageable)` + 컬렉션 JOIN FETCH의 메모리 페이징 경고

이 조합은 피해야 할 안티패턴이다. 왜 그런지 이해하면 다시는 빠지지 않는다.

```java
// 이것은 위험한 코드다
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.items WHERE o.status = 'COMPLETED'")
    Page<Order> findCompletedOrdersWithItems(Pageable pageable);
    // ← HibernateJpaDialect가 경고를 낸다
}
```

Hibernate는 이 쿼리에서 경고를 발생시킨다.

```
HHH90003004: firstResult/maxResults specified with collection fetch; 
applying in memory
```

무슨 뜻이냐면 — MySQL에 `LIMIT/OFFSET`을 보내지 않고, **전체 결과를 메모리로 올린 다음 Java에서 페이지를 자른다**는 것이다. 테이블에 1000만 건이 있다면 1000만 건을 Java 힙으로 올린 뒤 필요한 20건만 남기고 나머지를 버린다. 메모리 부족 오류(OOM)가 날 수 있고, 났다 하면 새벽에 서버가 다운된다.

왜 이런 동작을 하느냐면, 컬렉션 fetch join은 SQL 수준에서 행 수가 늘어나기 때문이다. 주문 1개에 아이템 3개가 있으면 JOIN 결과는 3행이다. 주문 10개에 각각 3개 아이템이 있으면 30행. MySQL에 `LIMIT 10`을 주면 30행 중 10행만 오는데, 이는 주문 기준 10개가 아닐 수 있다. 그래서 Hibernate는 아예 제한 없이 다 가져온 다음 자바에서 주문 기준으로 페이지를 나누는 것이다.

해결책은 두 가지다.

**1. Pageable은 페이징에, 컬렉션은 별도 BatchSize로**

```java
// OrderRepository — 페이지네이션만
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    Page<Order> findByStatus(String status, Pageable pageable);  // 일반 페이지네이션
}

// Order 엔티티
@Entity
public class Order {
    @OneToMany(mappedBy = "order")
    @BatchSize(size = 100)  // 페이지 안의 주문들의 아이템을 IN 쿼리로 한 번에
    private List<OrderItem> items;
}
```

이렇게 하면 페이지네이션 쿼리는 `LIMIT/OFFSET`으로 실제 DB에서 페이지를 자르고, 그 페이지 안의 주문들의 아이템은 `@BatchSize`로 IN 쿼리 한 번에 가져온다.

**2. EntityGraph로 대체 (단, Pageable 없이)**

Pageable 없이 특정 주문 하나를 조회할 때는 EntityGraph가 깔끔하다.

```java
@EntityGraph(attributePaths = {"items", "items.product"})
Optional<Order> findByIdWithDetails(Long id);
```

## 영속성 컨텍스트와 1차 캐시 — 만 단위 엔티티를 들고 있을 때

영속성 컨텍스트는 JPA가 관리하는 엔티티들의 저장소다. 같은 트랜잭션 안에서 같은 PK로 엔티티를 두 번 조회하면 두 번째는 DB를 가지 않고 영속성 컨텍스트(1차 캐시)에서 반환한다.

이 1차 캐시가 문제가 될 때가 있다. 배치 처리에서 대량의 엔티티를 처리할 때다.

```java
// 이 코드는 OOM을 일으킬 수 있다
@Transactional
public void processAllOrders() {
    List<Order> orders = orderRepository.findAll();  // 100만 건 모두 조회 + 1차 캐시에 저장
    for (Order order : orders) {
        order.markAsProcessed();  // 변경 감지 대상이 됨
        // 100만 건이 전부 1차 캐시에 쌓이고 변경 감지 대상으로 남아 있음
    }
    // flush 시점에 100만 건 UPDATE
}
```

100만 개 엔티티가 영속성 컨텍스트 안에 들어차면 Java 힙을 가득 채우고, 변경 감지를 위한 dirty checking도 100만 번 일어난다. 이렇게 쓰면 끔찍한 일이 벌어진다.

배치 처리에서는 주기적으로 `flush()`와 `clear()`를 호출해 영속성 컨텍스트를 비우자.

```java
// 올바른 배치 처리 패턴
@Transactional
public void processOrdersInBatch() {
    final int BATCH_SIZE = 1000;
    long lastId = 0;

    while (true) {
        List<Order> batch = orderRepository.findNextBatch(lastId, BATCH_SIZE);
        if (batch.isEmpty()) break;

        for (Order order : batch) {
            order.markAsProcessed();
        }

        entityManager.flush();   // 변경 사항 DB에 반영
        entityManager.clear();   // 영속성 컨텍스트 비우기

        lastId = batch.get(batch.size() - 1).getId();
    }
}
```

`flush()` 후 `clear()`를 하면 영속성 컨텍스트가 비워진다. 다음 배치 조회는 DB에서 다시 가져오지만 그 양이 1000건이라 관리 가능하다.

이 패턴에서 쿼리 메서드도 중요하다. `findAll()`로 전체를 한 번에 가져오지 말고, 커서 기반(lastId를 기준으로 다음 1000건)으로 청크를 가져오는 편이 낫다.

```java
// 청크 기반 조회
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o WHERE o.id > :lastId ORDER BY o.id ASC")
    List<Order> findNextBatch(@Param("lastId") Long lastId, Pageable pageable);
}

// 호출 시
List<Order> batch = orderRepository.findNextBatch(lastId,
    PageRequest.of(0, BATCH_SIZE));
```

## 영속성 컨텍스트의 변경 감지(dirty checking) 이해하기

JPA의 변경 감지는 편리하지만 예상치 못한 쿼리를 만들기도 한다. 엔티티를 조회하고 setter를 호출하면 트랜잭션이 끝날 때 자동으로 UPDATE 쿼리가 나간다. `save()`를 명시적으로 호출하지 않아도.

```java
@Transactional
public void updateOrderStatus(Long orderId, String newStatus) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    order.setStatus(newStatus);
    // save() 없어도 트랜잭션 종료 시 UPDATE 실행
    // 이 동작을 알아야 의도치 않은 UPDATE를 막을 수 있다
}
```

이 변경 감지는 스냅샷 비교로 작동한다. 엔티티를 조회할 때 Hibernate가 원본 상태의 복사본(스냅샷)을 만들어두고, flush 시점에 현재 상태와 비교해 다른 필드가 있으면 UPDATE를 생성한다. 이 스냅샷이 1차 캐시에 함께 저장되므로, 대량의 엔티티를 들고 있으면 그만큼 메모리를 더 쓴다.

읽기 전용 트랜잭션(`@Transactional(readOnly = true)`)을 쓰면 Hibernate가 스냅샷을 만들지 않아 메모리를 아낄 수 있고 성능도 약간 개선된다. 수정이 필요 없는 조회 서비스 메서드에는 `readOnly = true`를 붙여두는 편이 낫다.

```java
// 읽기 전용 트랜잭션 — 스냅샷 없음, dirty checking 없음
@Transactional(readOnly = true)
public List<OrderDto> getOrderList(Long userId, Pageable pageable) {
    return orderRepository.findByUserId(userId, pageable)
        .map(OrderDto::from)
        .getContent();
}
```

## JPQL과 QueryDSL에서 인덱스·옵티마이저 친화적으로 쓰기

> **사이드바:** QueryDSL은 타입 안전 쿼리 빌더다. JPQL의 문자열 기반 쿼리 대신 컴파일 타임에 오류를 잡을 수 있고, 동적 조건 쿼리를 체인 방식으로 작성할 수 있다. 이 책에서 깊이 다루지는 않지만, QueryDSL을 쓸 때 인덱스를 고려해야 하는 포인트들을 짚어보자.

첫째, JPQL이나 QueryDSL에서 컬럼에 함수를 적용하지 말자. 5장에서 본 내용이다.

```java
// 인덱스를 타지 못하는 JPQL
@Query("SELECT o FROM Order o WHERE YEAR(o.createdAt) = :year")
List<Order> findByYear(@Param("year") int year);

// 인덱스를 타는 방식으로 — 범위 조건으로 변환
@Query("SELECT o FROM Order o WHERE o.createdAt >= :from AND o.createdAt < :to")
List<Order> findByDateRange(
    @Param("from") LocalDateTime from,
    @Param("to") LocalDateTime to
);
```

둘째, QueryDSL로 동적 조건을 만들 때 `BooleanExpression`이 null이면 조건에서 빠진다는 점을 활용하되, 결과적으로 생성되는 SQL에 인덱스가 잘 쓰이는지 확인해두는 편이 낫다.

```java
// QueryDSL 동적 쿼리 예시
public List<Order> findOrders(OrderSearchCondition cond) {
    QOrder o = QOrder.order;

    return queryFactory
        .selectFrom(o)
        .where(
            statusEq(o, cond.getStatus()),         // null이면 조건 무시
            userIdEq(o, cond.getUserId()),
            createdAtBetween(o, cond.getFrom(), cond.getTo())
        )
        .orderBy(o.createdAt.desc())
        .limit(cond.getSize())
        .fetch();
}

private BooleanExpression statusEq(QOrder o, String status) {
    return status != null ? o.status.eq(status) : null;
}

private BooleanExpression createdAtBetween(QOrder o,
    LocalDateTime from, LocalDateTime to) {
    if (from == null && to == null) return null;
    if (from == null) return o.createdAt.loe(to);
    if (to == null) return o.createdAt.goe(from);
    return o.createdAt.between(from, to);
}
```

셋째, `fetchJoin()`과 `limit()`을 함께 쓸 때 컬렉션 join이 있으면 앞에서 본 메모리 페이징 경고와 동일한 문제가 생긴다. QueryDSL에서도 컬렉션 join + 페이지네이션 조합은 피하자.

## Spring Data JPA 리포지토리 설계 — 실전 패턴

리포지토리가 왜 이렇게 복잡해질까. 엔티티가 여러 개이고, 각각에 대한 조회 조건이 다양해지면 메서드가 줄줄이 늘어난다. 몇 가지 실전 패턴을 같이 살펴보자.

```java
// 기본 리포지토리 — JpaRepository 상속
@Repository
public interface OrderRepository
        extends JpaRepository<Order, Long>, OrderRepositoryCustom {

    // Spring Data JPA 쿼리 메서드
    Page<Order> findByUserId(Long userId, Pageable pageable);

    @EntityGraph(attributePaths = {"items"})
    Optional<Order> findWithItemsById(Long id);

    // 카운트 최적화 — countQuery를 별도로
    @Query(value = "SELECT o FROM Order o WHERE o.status = :status",
           countQuery = "SELECT COUNT(o) FROM Order o WHERE o.status = :status")
    Page<Order> findByStatus(@Param("status") String status, Pageable pageable);
}

// 커스텀 리포지토리 인터페이스
public interface OrderRepositoryCustom {
    List<Order> searchOrders(OrderSearchCondition cond);
}

// QueryDSL 구현
@Repository
@RequiredArgsConstructor
public class OrderRepositoryImpl implements OrderRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    @Override
    public List<Order> searchOrders(OrderSearchCondition cond) {
        // QueryDSL 구현
    }
}
```

`countQuery`를 별도로 지정하는 것이 중요한 포인트다. `Page<T>` 반환 시 Spring Data JPA는 전체 카운트 쿼리를 자동으로 만든다. 이때 원본 쿼리에 JOIN이 있으면 카운트 쿼리에도 JOIN이 붙어 불필요하게 느려질 수 있다. `countQuery`를 명시하면 JOIN 없는 단순한 COUNT 쿼리를 쓸 수 있다.

## 지연 로딩과 트랜잭션 범위의 함정

JPA의 LAZY 로딩은 트랜잭션 안에서만 작동한다. 트랜잭션이 끝난 뒤 연관 엔티티에 접근하면 `LazyInitializationException`이 발생한다. 스프링에서 자주 보는 패턴이 트랜잭션 서비스에서 엔티티를 반환하고, 컨트롤러나 뷰에서 연관 관계에 접근하려다 예외가 터지는 것이다.

```java
// 서비스 — 트랜잭션 안에서 Order를 반환
@Transactional
public Order getOrder(Long id) {
    return orderRepository.findById(id).orElseThrow();
    // 트랜잭션 종료
}

// 컨트롤러 — 트랜잭션 밖에서 연관 관계 접근
@GetMapping("/orders/{id}")
public OrderResponse getOrder(@PathVariable Long id) {
    Order order = orderService.getOrder(id);
    // 여기서 order.getUser().getName() 호출 시 LazyInitializationException!
    // 트랜잭션이 이미 끝났으므로 LAZY 로딩 불가
}
```

해결책은 두 가지다.

하나, 서비스 레이어에서 DTO로 변환해 반환한다. 엔티티가 아닌 DTO를 컨트롤러로 보내면 연관 엔티티 접근이 트랜잭션 안에서 이루어진다.

```java
@Transactional(readOnly = true)
public OrderDto getOrder(Long id) {
    Order order = orderRepository.findByIdWithDetails(id).orElseThrow();
    return OrderDto.from(order);  // 트랜잭션 안에서 DTO 변환
}
```

둘, OSIV(Open Session In View) 패턴을 쓴다. `spring.jpa.open-in-view=true`로 설정하면 HTTP 요청 전체에 걸쳐 세션을 유지해서 컨트롤러에서도 LAZY 로딩이 가능하다. 기본값이 `true`인데, 이 설정이 있으면 커넥션 풀에서 커넥션을 HTTP 요청 내내 점유해 성능에 부정적일 수 있다. 트래픽이 많다면 `false`로 바꾸고 DTO 변환 패턴을 쓰는 편이 낫다.

```yaml
# application.yml — 비권장 (기본 true)
spring:
  jpa:
    open-in-view: false  # 권장 설정 — 커넥션 점유 최소화
```

## 엔티티 설계 실전 — 양방향 연관 관계의 주의점

양방향 연관 관계는 편리하지만 함정도 같이 따라온다. 어떤 함정일까. 코드부터 같이 살펴보자.

```java
// Order 엔티티
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @OneToMany(mappedBy = "order",
               cascade = CascadeType.ALL,
               orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    // 연관 관계 편의 메서드
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);  // 양방향 동기화
    }

    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }
}

// OrderItem 엔티티
@Entity
@Table(name = "order_items")
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @Column(nullable = false)
    private Integer quantity;

    @Column(nullable = false)
    private BigDecimal unitPrice;
}
```

양방향 연관 관계를 쓸 때 주의할 점들이 있다.

`CascadeType.ALL`과 `orphanRemoval = true`를 동시에 쓰면 Order를 삭제할 때 OrderItem도 자동으로 삭제된다. 이것이 의도한 동작인지 확인하고 쓰자. 의도치 않게 연쇄 삭제가 일어나면 난감하다.

양방향에서 "연관 관계의 주인"은 FK를 가진 쪽이다. `OrderItem.order`에 `@JoinColumn`이 있으므로 OrderItem이 주인이다. `Order.items`의 `mappedBy = "order"`는 읽기 전용이라는 의미다. DB 반영은 `OrderItem.order`를 통해 일어난다. 그래서 `addItem()` 편의 메서드에서 `item.setOrder(this)`를 호출하는 것이 중요하다.

## 영속성 전환 상태와 merge

JPA 엔티티는 네 가지 상태를 가진다.

- **비영속(Transient)**: `new Order()`로 만들었지만 아직 영속성 컨텍스트에 없음
- **영속(Persistent)**: 영속성 컨텍스트가 관리 중. 변경 감지 대상
- **준영속(Detached)**: 영속성 컨텍스트에서 분리됨. 더 이상 변경 감지 안 됨
- **삭제(Removed)**: 삭제 표시됨, flush 시 DELETE

`save()` 메서드의 동작을 이해하면 의도치 않은 merge를 막을 수 있다.

```java
// SimpleJpaRepository의 save() 내부 (개념)
public <S extends T> S save(S entity) {
    if (entityInformation.isNew(entity)) {
        em.persist(entity);  // 새 엔티티 → persist
        return entity;
    } else {
        return em.merge(entity);  // 기존 엔티티 → merge
    }
}
```

ID가 null이면 새 엔티티로 판단해 `persist`를 호출하고, ID가 있으면 기존 엔티티로 판단해 `merge`를 호출한다. `merge`는 준영속 엔티티를 영속성 컨텍스트로 다시 붙이는 것인데, 이때 **모든 필드를 DB 값으로 덮어쓴 새 영속 객체를 반환**한다. 원본 객체는 여전히 준영속 상태다.

```java
// merge의 함정
Order detachedOrder = ...; // 준영속 상태 엔티티
detachedOrder.setStatus("COMPLETED");

Order merged = orderRepository.save(detachedOrder);
// detachedOrder와 merged는 다른 객체!
// detachedOrder는 여전히 준영속
// merged가 영속성 컨텍스트에서 관리되는 새 객체

// 이후 detachedOrder를 수정해도 DB에 반영 안 됨
detachedOrder.setNote("note");  // 이 변경은 DB에 안 감
merged.setNote("note");         // 이래야 DB에 반영됨
```

이런 혼란을 피하려면 준영속 객체를 서비스 레이어 경계 바깥으로 넘기지 않는 편이 낫다. 트랜잭션 안에서 조회하고, 수정하고, DTO로 변환해 반환하자.

## 9장과 10장, 5장 사이의 다리

여기서 한 발 뒤로 물러서서 전체 그림을 보자.

5장에서 EXPLAIN ANALYZE로 쿼리를 진단하는 법을 배웠다. 지금 이 장에서 JPA가 만들어내는 쿼리들이 어떤 함정을 가지는지를 봤다. 그런데 JPA 코드를 작성하다 N+1이 의심되거나 페이지네이션이 느려진다면, 5장의 도구를 다시 꺼내자. `spring.jpa.show_sql=true` 또는 Hibernate 쿼리 로그로 실제 SQL을 확인하고, 그것을 EXPLAIN ANALYZE로 분석한다. JPA 레벨의 진단과 MySQL 레벨의 진단이 항상 함께 가야 한다.

10장에서는 JPA의 다음 단계로 넘어간다. 배치 처리 100배 개선, 수백만 건 UPDATE 청크 분할, `@Version`으로 낙관적 락, `@Lock(PESSIMISTIC_WRITE)`로 비관적 락, MySQL named lock 분산락까지. 영속성 기본기 위에 성능과 동시성의 무기들을 올리는 것이 10장의 주제다. 12장의 운영 관측 도구(슬로우 쿼리 로그, performance_schema)와 연결하면 JPA 코드의 영향이 실제로 DB에서 어떻게 보이는지 전체 그림이 잡힌다.

## 마무리

JPA의 편안함은 진짜다. 하지만 그 편안함 뒤에서 MySQL이 무슨 쿼리를 실행하는지 모르고 쓰는 것은 찜찜하다. 이 장에서 다룬 함정들을 정리해두자.

**N+1**: 기본 LAZY로 인한 연쇄 쿼리. fetch join, EntityGraph, BatchSize로 상황에 맞게 풀어내자.

**컬렉션 fetch join + Pageable**: 메모리 페이징 경고. 컬렉션 fetch join과 Pageable을 함께 쓰지 말자.

**깊은 OFFSET 페이지네이션**: 데이터가 쌓일수록 점점 느려진다. 무한 스크롤이나 깊은 페이지네이션에는 keyset pagination이 답이다.

**영속성 컨텍스트에 만 단위 엔티티**: 배치 처리에서 flush+clear를 주기적으로 호출하자.

**OSIV**: `open-in-view=false`로 설정하고 트랜잭션 안에서 DTO 변환을 완료하는 편이 낫다.

**readOnly 트랜잭션**: 수정이 없는 조회는 `@Transactional(readOnly = true)` — 스냅샷을 만들지 않아 메모리를 아낀다.

이것들을 알고 쓰는 것과 모르고 쓰는 것의 차이는 처음엔 작아 보이지만, 서비스가 커지면서 점점 벌어진다.

## 참고 자료

- Vlad Mihalcea — Keyset Pagination with JPA and Hibernate — https://vladmihalcea.com/keyset-pagination-jpa-hibernate/
- Vlad Mihalcea — SQL Seek/Keyset pagination — https://vladmihalcea.com/sql-seek-keyset-pagination/
- Vlad Mihalcea — JPA First-Level Cache — https://vladmihalcea.com/jpa-hibernate-first-level-cache/
- Vlad Mihalcea — High-Performance Java Persistence, Chapter 13 Flushing — https://vladmihalcea.com/high-performance-java-persistence-chapter-13-flushing/
- Vlad Mihalcea — Java data access technology survey — https://vladmihalcea.com/java-data-access-technology/
- Thorben Janssen — Offset vs Keyset Pagination with Spring Data JPA — https://thorben-janssen.com/offset-and-keyset-pagination-with-spring-data-jpa/
- Baeldung — Optimistic Locking in JPA — https://www.baeldung.com/jpa-optimistic-locking
- DEV.to — Understanding and Solving the N+1 Problem in Spring Data JPA — https://dev.to/sadiul_hakim/understanding-and-solving-the-n1-problem-in-spring-data-jpa-2b6f
- SharpSkill — Spring Data JPA N+1: Fetch Join and EntityGraph — https://sharpskill.dev/en/blog/spring-boot/spring-data-jpa-n-plus-1-fetch-join-entitygraph
