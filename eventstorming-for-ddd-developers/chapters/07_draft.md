# 7장. Domain Event를 Spring에 꽂기 — `@DomainEvents`·Outbox·Kafka

6장에서 만든 `Order` Aggregate에는 `registerEvent(new OrderPlaced(...))`라는 한 줄이 들어 있었다. 이 한 줄이 무엇을 약속하는가? "주문이 접수됐다는 사실을, *나 자신*이 아닌 *시스템 전체*가 알아야 한다"는 약속이다. 그 약속을 지키려면, 누군가가 그 이벤트를 *꺼내서*, *발행하고*, *듣고*, *실패하면 다시 보내야* 한다.

이 챕터는 그 흐름을 한 줄로 잇는다. 워크숍에서 본 주황색 sticky가, 정말로 다음 모듈(또는 다음 서비스, 다음 시스템)까지 *안전하게* 도착하기까지의 다리다. 이번 장이 책에서 가장 무거운 장이고, 가장 많은 코드가 들어간다.

## 7.1 Spring `ApplicationEventPublisher`의 기본기

먼저 가장 기본을 짚고 가자. Spring에는 *내장된* 이벤트 시스템이 있다. `ApplicationEventPublisher`를 inject받아서 `publishEvent(...)`를 호출하면, 같은 application context 안에 있는 `@EventListener`가 그 이벤트를 받는다. 한번 가장 단순한 모양을 살펴보자.

```java
@Service
@RequiredArgsConstructor
class SimplePublisher {
    private final ApplicationEventPublisher publisher;

    public void doSomething() {
        publisher.publishEvent(new SomethingHappened("foo"));
    }
}

@Component
class SimpleListener {
    @EventListener
    void on(SomethingHappened event) {
        // 처리
    }
}
```

이 모양이 *기본*이다. 그러나 이 기본 그대로는 *프로덕션에서 쓸 수 없다*. 두 가지 이유가 있다.

첫째, `@EventListener`는 **기본적으로 동기**다. `publishEvent()`를 호출한 스레드가 *그대로* 리스너를 실행한다. 리스너에서 예외가 터지면, 발행한 트랜잭션이 통째로 롤백된다. `Order` 저장은 성공시키고 싶은데, "고객에게 이메일을 보내려다 실패한" 일 때문에 `Order`까지 사라지는 일은 *말이 안 된다*.

둘째, `@EventListener`는 **트랜잭션 시점에 무지하다**. 트랜잭션이 *커밋되기 전에* 리스너가 실행된다. 그래서 "OrderPlaced 이벤트를 받은 뒤 그 Order를 DB에서 조회하려는" 리스너가 `EmptyResultDataAccessException`을 만나는 *황당한 풍경*이 펼쳐진다. 이미 commit 됐을 거라고 기대했는데, 실은 commit 전이었다.

이 두 가지 문제를 해결하는 첫 번째 도구가 `@TransactionalEventListener`다.

## 7.2 `@TransactionalEventListener` — 시점을 다스리기

Spring 4.2부터 들어온 어노테이션이다. 한번 모양을 보자.

```java
@Component
class OrderPlacedHandler {

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void on(OrderPlaced event) {
        // 트랜잭션이 commit된 *후에* 실행된다
    }
}
```

`phase`의 선택지는 네 가지다.

- `BEFORE_COMMIT` — commit 직전. 보통 추천하지 않는다.
- `AFTER_COMMIT` — commit 성공 직후. *대부분의 경우 우리가 원하는 시점*이다.
- `AFTER_ROLLBACK` — 롤백 직후. 보상 로직.
- `AFTER_COMPLETION` — commit이든 rollback이든 끝나면.

`AFTER_COMMIT`이 가장 자주 쓰는 시점이다. 이 시점에 리스너가 실행되면, 발행한 Aggregate의 변경은 *이미 DB에 반영*되어 있다. 리스너가 그 Aggregate를 조회해도 정상적으로 보이고, 리스너에서 예외가 터져도 *발행자의 트랜잭션은 안전*하다.

다만 한 가지 함정이 따라온다. `AFTER_COMMIT`이라는 시점이 무엇을 *약속하지 않는가*? **이벤트 전달의 신뢰성**이다. 만약 commit이 성공한 직후 JVM이 *죽으면*, 그 이벤트는 *영원히 사라진다*. 메모리에만 있던 이벤트였기 때문이다.

이 풍경이 위험한 이유를 한번 떠올려보자. `Order`는 DB에 *영구히* 기록됐다. 그러나 그 사건을 받기로 한 `warehouse` 모듈은 *영영 알지 못한다*. 두 모듈의 세상이 *영구적으로* 어긋난다. 다음 주에 그 사실을 발견했을 때는, *이미 늦었다*. 이게 dual-write 문제의 본질이다.

## 7.3 Dual-Write 문제와 Transactional Outbox

조금 더 풀어 설명해보자. Dual-write가 왜 어려운가? 우리는 한 동작 안에서 *두 곳에 쓰려고* 한다. 하나는 DB(주문 테이블), 다른 하나는 메시지 브로커(Kafka의 orders 토픽). 둘이 *모두 성공*해야 일관성이 유지된다.

- DB 성공 + Kafka 성공 → ✓ 일관적
- DB 실패 + Kafka 실패 → ✓ 일관적 (아무것도 안 일어남)
- DB 성공 + Kafka 실패 → ✗ Order는 있지만 아무도 모름
- DB 실패 + Kafka 성공 → ✗ 발행은 됐는데 Order가 없음

세 번째와 네 번째가 *재앙*이다. 2PC(2-phase commit)로 묶을 수 있을까? 이론적으로 가능하지만, Kafka가 *실용적인* XA 트랜잭션을 지원하지 않고, 설사 지원해도 운영 비용이 끔찍하다.

해법은 단순하면서 우아하다 — **두 곳에 동시에 쓰지 않는다**. 한 곳(DB)에만 쓰고, 그 한 곳에 *이벤트도 같이 쓴다*. 그리고 나중에 별도 프로세스가 DB의 이벤트를 *읽어서* Kafka로 흘려보낸다. 이 패턴이 **Transactional Outbox**다.

흐름은 이렇게 흐른다.

1. 비즈니스 트랜잭션 안에서 `Order`를 저장하면서, *같은 트랜잭션 안에서* `outbox` 테이블에 이벤트 row를 INSERT한다.
2. 두 쓰기가 같은 트랜잭션이므로 *원자적*이다. 둘 다 성공하거나 둘 다 실패한다.
3. 별도 *relay* 프로세스가 outbox 테이블을 polling(또는 CDC로 watch)하면서, 새 row를 Kafka로 발행한다.
4. 발행 성공한 row는 *지운다*(또는 `published_at`을 채운다).

Kafka 발행이 *몇 번 실패해도* 괜찮다. relay가 다시 시도하면 된다. 다만 한 가지 비용이 있다 — **at-least-once**. 같은 이벤트가 *두 번 이상* 발행될 수 있다(발행은 성공했는데 row 정리 전에 죽으면). 그래서 *consumer 쪽이 idempotent해야 한다*. 이 책임을 어떻게 지는지는 잠시 뒤에 본다.

## 7.4 Spring Modulith의 Event Publication Registry

Outbox 패턴을 *직접 손으로* 구현할 수도 있다. 그러나 한국 Spring 팀이 처음 출발할 때, 이걸 직접 만들 필요는 없다. Spring Modulith가 *in-process 버전*을 이미 가지고 있다 — **Event Publication Registry**다.

원리는 이렇다. Modulith가 `@ApplicationModuleListener`로 받기로 한 이벤트를, *발행자의 트랜잭션 안에서* DB에 row로 기록한다. 그리고 commit이 끝나면 *별도 스레드*에서 리스너를 호출하고, 성공하면 그 row의 `completion_date`를 채운다. 실패하면 row가 *미완료 상태로 남는다*. JVM이 재시작되면 미완료 row를 다시 시도한다.

설정을 살펴보자. `pom.xml`에 의존성 하나 추가한다.

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-events-jpa</artifactId>
</dependency>
```

이 의존성 하나로 `event_publication` 테이블이 자동 생성되고(또는 Liquibase/Flyway로 명시적으로 생성), 리스너 호출이 자동으로 그 테이블을 통해 흐른다. 우리가 코드에 추가로 쓸 것은 *없다*. 6장에서 본 `registerEvent(...)`와 7.2에서 본 `@ApplicationModuleListener` 한 묶음이면 끝이다.

```java
// orders 모듈 — 발행
public class Order extends AbstractAggregateRoot<Order> {
    public static Order place(...) {
        // ...
        order.registerEvent(new OrderPlaced(...));
        return order;
    }
}

// payments 모듈 — 수신
@Component
@RequiredArgsConstructor
class PaymentOrchestrator {

    private final InitiatePaymentUseCase initiatePayment;

    @ApplicationModuleListener
    void on(OrderPlaced event) {
        initiatePayment.start(new InitiatePaymentCommand(
            event.orderId(), event.totalAmount()
        ));
    }
}
```

이 한 흐름이 완성된 사이클이다. orders가 `Order`를 저장 → registry에 이벤트 row가 *함께* 기록 → commit → 별도 스레드에서 `PaymentOrchestrator.on()` 호출 → 성공하면 row 종결. 만약 `on()`이 실패하면? row는 남는다. JVM 재시작 시 다시 시도된다. **모듈 사이의 dual-write 문제가 *모듈러 모놀리스 수준*에서는 풀린 셈**이다.

## 7.5 Polling vs CDC — Relay 전략 두 갈래

이제 한 걸음 더 나가서, *외부 시스템*(다른 마이크로서비스, 분석 파이프라인)으로 이벤트를 흘리는 경우를 살펴보자. 한 JVM 안에서 끝나지 않으면 별도 relay가 필요하다. relay 전략은 크게 두 가지다.

**Polling**: 일정 주기로 outbox 테이블의 미발행 row를 SELECT한 뒤 Kafka로 발행한다.

- 장점: 단순하다. 추가 인프라가 없다.
- 단점: latency가 polling 주기에 의존한다. DB에 부하가 간다.

**CDC (Change Data Capture)**: Debezium 같은 도구가 DB의 WAL(write-ahead log)을 *직접* 따라가면서 변경을 감지하고 Kafka에 흘린다.

- 장점: 실시간성. DB에 추가 부하가 거의 없다.
- 단점: Debezium·Kafka Connect 인프라가 필요하다. 운영 학습 곡선이 가파르다.

선택의 가이드라인은 단순하다.

- **처음 외부 발행을 시작하는 팀**: Polling으로 출발하자. 1초 latency를 견딜 수 없는 도메인은 *생각보다 적다*.
- **대량 트래픽 / 마이크로서비스가 본격화된 팀**: CDC를 도입하자. 단 Debezium 운영 경험이 있는 SRE/플랫폼 팀이 받쳐줘야 한다.

Spring Modulith 2.0부터는 Event Publication Registry의 결과를 *외부로 흘리는* externalization 기능이 더 단단해진다 [Spring Modulith 2.0 M1, 2025]. 메서드 한 줄로 모듈 이벤트를 Kafka topic에 매핑할 수 있다. ZenWave 360의 글이 이 영역을 잘 정리하고 있다.

## 7.6 Kafka로 흘려보내기 — Spring Cloud Stream

Kafka로 직접 흘리는 가장 깔끔한 방식은 Spring Cloud Stream의 함수형 binding이다. Kafka의 구체적인 producer API를 *건드리지 않고*, `Supplier<>` / `Consumer<>` / `Function<>` 인터페이스로 추상화한다.

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
          brokers: kafka:9092
```

```java
@Configuration
class OrderEventBinding {

    private final Sinks.Many<OrderPlaced> sink =
        Sinks.many().multicast().onBackpressureBuffer();

    @Bean
    public Supplier<Flux<OrderPlaced>> orderPlacedEvents() {
        return sink::asFlux;
    }

    void publish(OrderPlaced event) {
        sink.tryEmitNext(event);
    }
}
```

이 코드가 어떻게 흐르는가? `Supplier<Flux<OrderPlaced>>` 빈을 등록하면, Spring Cloud Stream이 자동으로 그 stream을 `orderPlacedEvents-out-0` binding에 연결한다. binding은 `application.yml`의 매핑대로 `orders.events` Kafka topic에 발행된다.

이 sink를 outbox relay가 호출한다. Modulith Event Publication Registry의 미발행 row를 polling으로 읽어서, `OrderEventBinding.publish()`로 흘리는 작은 컴포넌트 하나만 만들면 된다.

```java
@Component
@RequiredArgsConstructor
@Slf4j
class OutboxRelay {

    private final EventPublicationRegistry registry;
    private final OrderEventBinding binding;

    @Scheduled(fixedDelay = 1000)
    @Transactional
    void relay() {
        registry.findIncompletePublications().forEach(publication -> {
            if (publication.getEvent() instanceof OrderPlaced e) {
                try {
                    binding.publish(e);
                    registry.markCompleted(publication.getIdentifier());
                } catch (Exception ex) {
                    log.warn("OrderPlaced 발행 실패, 다음 polling에서 재시도", ex);
                }
            }
        });
    }
}
```

처음에는 *과해 보일 수 있다*. 하지만 도메인 이벤트가 외부 시스템으로 흐르기 시작하는 순간, 이 한 클래스가 *시스템의 동맥*이 된다. 발행 실패는 *조용히* 일어나지 *않는다* — row가 남아 있으므로. JVM이 죽었다 살아나도 *복구된다*.

## 7.7 이벤트 스키마 관리 — JSON Schema 또는 Avro

이쯤에서 한 가지 자문해보자. 이벤트가 JSON으로 흐르는 건 좋다. 그런데 *스키마*는 어떻게 관리하나? `OrderPlaced` record에 필드를 하나 추가하면, 그걸 받는 다른 서비스는 어떻게 되나?

이 질문은 *마이크로서비스에 도달한 팀*이 처음으로 마주하는 차원이다. 답은 **스키마 레지스트리**다. Confluent Schema Registry, Apicurio, AWS Glue Schema Registry 같은 도구가 이 역할을 한다.

선택지는 두 가지가 입에 잘 붙는다.

**JSON Schema** — 사람이 읽기 좋고, JSON 그대로 흐른다. 한국 팀 대부분에게 이게 *충분한 첫 단계*다. Confluent의 JSON Schema 지원을 그대로 쓰면 된다.

**Avro / Protobuf** — 바이너리. 더 작고, 더 엄격한 호환성 룰. 트래픽이 크고, 스키마 진화가 자주 일어나는 도메인에 어울린다.

스키마 호환성은 *backward / forward / full* 세 모드 중 하나로 정한다. 가장 자주 쓰는 *backward compatible*은 — "새 스키마로 발행하면, *옛 consumer가 그대로 읽을 수 있어야 한다*"이다. 새 필드는 추가 OK, 기존 필드 제거는 금지, 타입 변경은 금지. 이 한 규칙만 지켜도 95%의 호환성 사고는 막힌다.

## 7.8 Consumer의 책임 — Idempotency

At-least-once 환경에서 같은 이벤트가 두 번 도착하면 어떻게 될까? "주문 하나에 결제 두 번"이 벌어진다. 그러면 *재앙*이다.

해법은 단순하다 — **consumer가 이미 처리한 이벤트의 ID를 기억한다**. 그리고 같은 ID가 또 오면 *조용히 무시*한다. 이게 idempotency다.

```java
@Component
@RequiredArgsConstructor
class PaymentOrchestrator {

    private final ProcessedEventRepository processed;
    private final InitiatePaymentUseCase initiatePayment;

    @ApplicationModuleListener
    @Transactional
    void on(OrderPlaced event) {
        if (processed.exists(event.eventId())) {
            return;   // 이미 처리됨, 조용히 종료
        }

        initiatePayment.start(new InitiatePaymentCommand(
            event.orderId(), event.totalAmount()
        ));

        processed.save(new ProcessedEvent(event.eventId(), Instant.now()));
    }
}
```

이벤트마다 *고유한 ID*가 있어야 idempotency가 성립한다. 그래서 `OrderPlaced` record를 정의할 때 `UUID eventId`를 *항상* 포함시키는 게 좋다.

```java
public record OrderPlaced(
    UUID eventId,
    OrderId orderId,
    CustomerId customerId,
    Money totalAmount,
    Instant occurredAt
) {
    public OrderPlaced {
        Objects.requireNonNull(eventId);
    }
}
```

`processed_event` 테이블 자체는 시간이 지나면 *부풀어 오른다*. 30일 정도 보존하고 그 이후는 정리하는 정책을 함께 두는 편이 낫다. 30일이면 대부분의 재시도/장애 복구 시나리오를 커버한다.

## 7.9 한 흐름으로 다시 보기 — OrderPlaced의 여정

7장이 다룬 모든 조각을 한 흐름으로 이어보자. 워크숍 벽에 붙어 있던 주황색 sticky `주문 접수됨` 한 장이, 시스템에서 어떤 여정을 거치는가?

```
[고객 요청]
     ↓
[OrderController]                                    ← inbound adapter
     ↓
[PlaceOrderUseCase.place(command)]                   ← inbound port
     ↓
[PlaceOrderService] @Transactional 시작
     ↓
[Order.place(...)]                                   ← domain
     │
     ├── 비즈니스 규칙 검증 (총액 계산, 상태 PLACED)
     └── registerEvent(new OrderPlaced(uuid, ...))   ← 이벤트 등록
     ↓
[OrderRepository.save(order)]                        ← outbound port
     ↓
[OrderPersistenceAdapter] → JPA → DB                 ← outbound adapter
     │
     └── 같은 트랜잭션에서 event_publication 테이블에도 INSERT
     ↓
[COMMIT]
     ↓
[Spring Modulith] 별도 스레드에서 리스너 호출
     ↓
[PaymentOrchestrator.on(OrderPlaced)]                ← payments 모듈
     │
     ├── idempotency 체크
     └── 결제 트리거
     ↓
[성공 시 event_publication row 완료 처리]

별도로 — 외부 발행 경로
[OutboxRelay] @Scheduled polling
     ↓
[event_publication 테이블의 미완료 row 조회]
     ↓
[Spring Cloud Stream Sink]
     ↓
[Kafka: orders.events topic]
     ↓
[외부 consumer들] (분석 파이프라인, 알림 서비스 등)
```

이 한 흐름이 7장의 성취다. 워크숍에서 떠올린 *한 사건*이, **트랜잭션 안에서 발행되고**, **registry에 보존되고**, **모듈 사이에서 안전하게 전달되고**, **외부 시스템으로 흘러나가고**, **중복 도착해도 안전하게 처리되는** 시스템이 완성됐다.

## 7.10 자주 마주치는 함정 셋

7장의 코드들이 첫눈에는 깔끔해 보이지만, 실제로 운영하면서 자주 마주치는 함정이 셋 있다. 미리 짚어두자.

**함정 1. `@TransactionalEventListener`인 줄 알았는데 `@EventListener`였다.** 두 어노테이션이 *겉모양*이 비슷해서, import만 잘못해도 시점이 통째로 바뀐다. PR 리뷰에서 가장 자주 놓치는 자리다. *체크리스트로 못 박자*.

**함정 2. 리스너 안에서 *다시* `@Transactional`을 잡지 않았다.** `AFTER_COMMIT` 시점에 리스너가 실행되면, *그 시점에는 트랜잭션이 끝나 있다*. 리스너 내부에서 DB를 또 쓰려면 *새로운* 트랜잭션을 시작해야 한다. `@Transactional`을 명시적으로 붙이자.

**함정 3. 이벤트에 *너무 많이* 담는다.** `OrderPlaced` record에 고객 이름, 주소, 모든 라인 아이템 상세, 결제 카드 끝 4자리까지 넣고 싶은 충동이 든다. 이 충동을 *경계*하자. 이벤트는 *"무엇이 일어났는가"*의 *최소한*만 담는다. 받는 쪽이 자기 read model을 만들 때 필요한 추가 정보가 있다면, ID로 *조회*해서 가져온다. 이벤트가 *데이터 동기화 채널*이 되기 시작하면, 결국 강결합이 돌아온다.

## 마무리 — 이벤트는 시스템의 동맥이다

7장이 한 일을 정리하자. Spring의 기본 `ApplicationEventPublisher`에서 시작해, `@TransactionalEventListener`로 시점을 다스리고, dual-write 문제를 Transactional Outbox로 풀었다. Spring Modulith의 Event Publication Registry로 *코드 한 줄 늘리지 않고* in-process outbox를 얻었다. Spring Cloud Stream으로 Kafka 발행을 추상화하고, Polling vs CDC의 선택지를 따져봤다. Schema Registry와 idempotency로 consumer 쪽의 책임까지 정리했다.

이쯤에서 한 가지 자문해보자. 우리는 도메인의 *쓰기* 쪽 흐름을 끝까지 따라왔다. command가 들어와 Aggregate가 변하고 이벤트가 흘러나간다. 그렇다면 *읽기* 쪽은? 사용자가 자기 주문을 확인하려고 화면을 여는 그 순간, 어떤 데이터가 어디서 어떻게 만들어져 화면에 도달하는가?

답은 8장에서 본격적으로 한다. 워크숍의 *초록색* sticky가 React Query 캐시와 Next.js Server Component로 환생하는 풍경을 보자.
