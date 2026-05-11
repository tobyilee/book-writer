# 부록 A. Spring Modulith·Outbox 코드 템플릿

5~8장에서 흩어져 있던 코드 조각을 *복붙 가능한 형태*로 한 군데에 모았다. 새 프로젝트를 시작하거나, 기존 프로젝트에 Spring Modulith를 처음 도입할 때 *최소 출발점*으로 쓰자. 본문은 거의 없다 — 코드 위에 한두 줄 해설만 둔다.

## A.1 `pom.xml` 의존성

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.modulith</groupId>
      <artifactId>spring-modulith-bom</artifactId>
      <version>1.3.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <!-- 기본 -->
  <dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-starter-core</artifactId>
  </dependency>

  <!-- JPA 기반 Event Publication Registry -->
  <dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-starter-jpa</artifactId>
  </dependency>

  <!-- 모듈 검증 테스트 -->
  <dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-starter-test</artifactId>
    <scope>test</scope>
  </dependency>

  <!-- 외부 발행: Kafka -->
  <dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-events-kafka</artifactId>
  </dependency>
</dependencies>
```

`spring-modulith-bom`이 모든 하위 모듈의 버전을 한 줄로 관리해준다. Spring Boot 버전과 호환되는 Modulith 버전은 공식 문서의 호환 표를 참조하자.

## A.2 패키지 구조 — 모듈러 모놀리스 출발점

```text
com.example.shop
├── ShopApplication.java
│
├── orders/                          ← 모듈 (Bounded Context)
│   ├── package-info.java
│   ├── api/                          ← 외부 공개 패키지 (named interface)
│   │   ├── package-info.java
│   │   └── OrderPlaced.java
│   ├── domain/                       ← 도메인 (port + Aggregate)
│   │   ├── Order.java
│   │   ├── OrderId.java
│   │   └── port/
│   │       ├── in/
│   │       │   ├── PlaceOrderUseCase.java
│   │       │   └── FindOrderQuery.java
│   │       └── out/
│   │           └── OrderRepository.java
│   ├── application/                  ← use case 구현
│   │   ├── PlaceOrderService.java
│   │   └── OrderQueryService.java
│   └── adapter/                      ← 인프라
│       ├── in/web/OrderController.java
│       └── out/persistence/
│           ├── OrderJpaRepository.java
│           └── OrderPersistenceAdapter.java
│
├── payments/
│   └── ... (orders와 동일 구조)
│
└── shipping/
    └── ...
```

각 모듈이 *형제*로 나란히 서고, 안에서는 *Hexagonal*을 따른다. 새 모듈을 추가할 때마다 이 골격을 그대로 복제하자.

## A.3 `@ApplicationModule` 선언과 named interface

```java
// orders/package-info.java
@ApplicationModule(
    displayName = "주문",
    allowedDependencies = {"payments :: api"}
)
package com.example.shop.orders;

import org.springframework.modulith.ApplicationModule;
```

```java
// orders/api/package-info.java
@NamedInterface("api")
package com.example.shop.orders.api;

import org.springframework.modulith.NamedInterface;
```

`api` named interface 안에 둔 타입만 외부 모듈이 import 할 수 있다. 그 외 패키지(`domain`, `application`, `adapter`)는 *모듈 내부*다.

## A.4 Aggregate Root 템플릿

```java
// orders/domain/Order.java
package com.example.shop.orders.domain;

import com.example.shop.orders.api.OrderPlaced;
import jakarta.persistence.*;
import org.springframework.data.domain.AbstractAggregateRoot;
import java.time.Instant;
import java.util.*;

@Entity
@Table(name = "orders")
public class Order extends AbstractAggregateRoot<Order> {

    @EmbeddedId
    private OrderId id;

    @Embedded
    private CustomerId customerId;

    @ElementCollection
    @CollectionTable(name = "order_lines", joinColumns = @JoinColumn(name = "order_id"))
    private List<OrderLine> lines = new ArrayList<>();

    @Embedded
    private Money totalAmount;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @Version
    private Long version;

    protected Order() {}

    public static Order place(OrderId id, CustomerId customerId, List<OrderLine> lines) {
        Order order = new Order();
        order.id = id;
        order.customerId = customerId;
        order.lines = new ArrayList<>(lines);
        order.totalAmount = lines.stream()
            .map(OrderLine::lineTotal)
            .reduce(Money.ZERO, Money::plus);
        order.status = OrderStatus.PLACED;

        order.registerEvent(new OrderPlaced(
            UUID.randomUUID(),
            id.value(),
            customerId.value(),
            order.totalAmount.amount(),
            Instant.now()
        ));
        return order;
    }

    // getter, 비즈니스 메서드 ...
    public OrderId getId() { return id; }
    public OrderStatus getStatus() { return status; }
}
```

`AbstractAggregateRoot<Order>`를 상속받으면 `registerEvent()` 메서드가 자동으로 들어온다. Spring Data가 save 시점에 등록된 이벤트를 *자동 발행*한다.

## A.5 Domain Event record

```java
// orders/api/OrderPlaced.java
package com.example.shop.orders.api;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

public record OrderPlaced(
    UUID eventId,
    UUID orderId,
    UUID customerId,
    BigDecimal totalAmount,
    Instant occurredAt
) {
    public OrderPlaced {
        Objects.requireNonNull(eventId, "eventId는 필수");
        Objects.requireNonNull(orderId);
        Objects.requireNonNull(customerId);
        Objects.requireNonNull(totalAmount);
        Objects.requireNonNull(occurredAt);
    }
}
```

`eventId`는 idempotency를 위한 *고유 ID*. record라서 immutable. `api` 패키지에 두어 외부 모듈이 import 할 수 있다.

## A.6 use case 인터페이스와 구현

```java
// orders/domain/port/in/PlaceOrderUseCase.java
public interface PlaceOrderUseCase {
    OrderId place(PlaceOrderCommand command);

    record PlaceOrderCommand(
        UUID customerId,
        List<OrderLineRequest> lines
    ) {}

    record OrderLineRequest(UUID productId, int quantity, BigDecimal unitPrice) {}
}
```

```java
// orders/application/PlaceOrderService.java
@Service
@Transactional
@RequiredArgsConstructor
class PlaceOrderService implements PlaceOrderUseCase {

    private final OrderRepository orderRepository;

    @Override
    public OrderId place(PlaceOrderCommand command) {
        List<OrderLine> lines = command.lines().stream()
            .map(req -> new OrderLine(
                new ProductId(req.productId()), req.quantity(),
                new Money(req.unitPrice())))
            .toList();

        OrderId id = OrderId.generate();
        Order order = Order.place(id, new CustomerId(command.customerId()), lines);
        orderRepository.save(order);
        return id;
    }
}
```

## A.7 Outbound port와 persistence adapter

```java
// orders/domain/port/out/OrderRepository.java
public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(OrderId id);
}
```

```java
// orders/adapter/out/persistence/OrderPersistenceAdapter.java
@Component
@RequiredArgsConstructor
class OrderPersistenceAdapter implements OrderRepository {

    private final OrderJpaRepository jpa;

    @Override
    public Order save(Order order) { return jpa.save(order); }

    @Override
    public Optional<Order> findById(OrderId id) { return jpa.findById(id); }
}

interface OrderJpaRepository extends JpaRepository<Order, OrderId> {}
```

도메인은 `OrderRepository`만 안다. JPA는 *adapter 안*에 갇혀 있다.

## A.8 모듈 사이 리스너 (`@ApplicationModuleListener`)

```java
// payments/application/PaymentOrchestrator.java
package com.example.shop.payments.application;

import com.example.shop.orders.api.OrderPlaced;
import org.springframework.modulith.events.ApplicationModuleListener;
import org.springframework.transaction.annotation.Transactional;

@Component
@RequiredArgsConstructor
class PaymentOrchestrator {

    private final InitiatePaymentUseCase initiatePayment;
    private final ProcessedEventRepository processed;

    @ApplicationModuleListener
    void on(OrderPlaced event) {
        if (processed.exists(event.eventId())) return;

        initiatePayment.start(new InitiatePaymentCommand(
            event.orderId(), event.totalAmount()
        ));

        processed.save(new ProcessedEvent(event.eventId(), Instant.now()));
    }
}
```

`@ApplicationModuleListener` = `@Async + @TransactionalEventListener(phase = AFTER_COMMIT)`. idempotency를 위해 *처리된 이벤트 ID*를 별도 테이블에 보존한다.

## A.9 Event Publication Registry 테이블 DDL

```sql
CREATE TABLE event_publication (
    id              UUID PRIMARY KEY,
    listener_id     VARCHAR(512) NOT NULL,
    event_type      VARCHAR(512) NOT NULL,
    serialized_event TEXT NOT NULL,
    publication_date TIMESTAMP NOT NULL,
    completion_date  TIMESTAMP
);

CREATE INDEX idx_event_publication_incomplete
    ON event_publication (completion_date)
    WHERE completion_date IS NULL;
```

`completion_date IS NULL`인 row가 *미발행 이벤트*다. 부분 인덱스로 polling 비용을 줄인다.

## A.10 Idempotency용 보조 테이블 DDL

```sql
CREATE TABLE processed_event (
    event_id      UUID PRIMARY KEY,
    processed_at  TIMESTAMP NOT NULL
);

-- 30일 이상 지난 row 정리
DELETE FROM processed_event
WHERE processed_at < NOW() - INTERVAL '30 days';
```

DELETE 쿼리는 cron job 또는 Spring `@Scheduled`로 매일 한 번 돌리자.

## A.11 모듈 검증 테스트

```java
// src/test/java/com/example/shop/ModularityTests.java
@SpringBootTest
class ModularityTests {

    ApplicationModules modules = ApplicationModules.of(ShopApplication.class);

    @Test
    void shouldBeCompliant() {
        modules.verify();
    }

    @Test
    void writeDocumentation() {
        new Documenter(modules)
            .writeDocumentation()
            .writeIndividualModulesAsPlantUml()
            .writeModuleCanvases();
    }
}
```

첫 테스트는 모듈 경계 침범을 잡고, 둘째 테스트는 `target/spring-modulith-docs/` 아래에 PlantUML/AsciiDoc 문서를 생성한다. CI에 두 테스트를 모두 포함시키자.

## A.12 Spring Cloud Stream Kafka 외부 발행 설정

```yaml
# application.yml
spring:
  cloud:
    function:
      definition: orderPlacedEvents
    stream:
      bindings:
        orderPlacedEvents-out-0:
          destination: orders.events
          content-type: application/json
      kafka:
        binder:
          brokers: ${KAFKA_BROKERS:localhost:9092}
        bindings:
          orderPlacedEvents-out-0:
            producer:
              configuration:
                acks: all                  # 모든 replica 확인
                enable.idempotence: true   # Kafka 쪽 idempotency
```

## A.13 Outbox Relay 컴포넌트

```java
@Component
@RequiredArgsConstructor
@Slf4j
class OrderOutboxRelay {

    private final IncompleteEventPublications registry;
    private final Sinks.Many<OrderPlaced> orderPlacedSink;

    @Scheduled(fixedDelay = 1000)
    void relay() {
        registry.findIncompletePublicationsOlderThan(Duration.ofMillis(500))
            .forEach(publication -> {
                if (publication.getEvent() instanceof OrderPlaced e) {
                    try {
                        orderPlacedSink.tryEmitNext(e);
                        registry.markCompleted(publication.getIdentifier());
                    } catch (Exception ex) {
                        log.warn("OrderPlaced 외부 발행 실패: {}", e.eventId(), ex);
                    }
                }
            });
    }

    @Bean
    Supplier<Flux<OrderPlaced>> orderPlacedEvents() {
        return orderPlacedSink::asFlux;
    }
}
```

`Sinks.Many` + `Supplier<Flux>` 조합으로 Spring Cloud Stream 함수형 binding을 만든다. `@Scheduled` polling이 미완료 이벤트를 sink에 흘려넣으면, binding이 Kafka topic으로 발행한다.

## A.14 미니멀 Outbox만 쓰는 경우 (Modulith 없이)

Modulith를 도입하기 어려운 기존 코드베이스에서 *최소한의 outbox만* 얹고 싶다면, 다음 두 테이블과 한 컴포넌트가 출발점이다.

```sql
CREATE TABLE outbox (
    id            UUID PRIMARY KEY,
    aggregate_id  VARCHAR(255) NOT NULL,
    event_type    VARCHAR(255) NOT NULL,
    payload       JSONB NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    published_at  TIMESTAMP
);

CREATE INDEX idx_outbox_unpublished ON outbox (created_at)
    WHERE published_at IS NULL;
```

```java
@Service
@RequiredArgsConstructor
@Transactional
class OutboxWriter {

    private final OutboxJpaRepository repo;
    private final ObjectMapper mapper;

    public void write(String aggregateId, Object event) {
        try {
            OutboxEntry entry = new OutboxEntry();
            entry.setId(UUID.randomUUID());
            entry.setAggregateId(aggregateId);
            entry.setEventType(event.getClass().getSimpleName());
            entry.setPayload(mapper.writeValueAsString(event));
            repo.save(entry);
        } catch (Exception e) {
            throw new RuntimeException("outbox 쓰기 실패", e);
        }
    }
}
```

`@Transactional` 안에서 `outbox` 테이블에 쓰는 동안, 같은 트랜잭션의 비즈니스 변경이 *함께* 커밋된다. 별도 polling 컴포넌트(A.13과 같은 형태)가 `published_at IS NULL` row를 읽어 발행한다.

---

이 부록의 코드는 *출발점*이지 *완성형*이 아니다. 도메인이 자라면서 *맞춰서 늘리자*. 다만 *방향성*은 처음부터 지키자 — 의존성은 바깥에서 안으로, 이벤트는 트랜잭션이 commit된 후에, 발행은 *반드시* DB에 자취를 남긴다.
