# 6장. Aggregate를 발견해 코드로 내려보내기 — JPA와 Hexagonal Architecture

5장에서 우리는 `orders` 모듈의 칸막이를 세웠다. 이제 그 칸막이를 *열고 들어가보자*. 모듈 안에 사는 그 `Order`는 정확히 어떤 클래스이며, 누가 그것의 일관성을 책임지는가? 워크숍에서 노란 sticky로 흐릿하게 적어놓았던 "Aggregate 후보"가 어떻게 Spring Data JPA의 `@Entity`로 환생하는가? 그리고 그 환생을 단정하게 정리해주는 Hexagonal Architecture는 우리 팀의 폴더 구조에 어떻게 박히는가?

> *Reading guide* — 이 장의 6.3절은 Vaughn Vernon의 "Effective Aggregate Design" 3부작을 EventStorming 어휘로 번역한 부분이다. 이미 Vernon의 *Implementing DDD*를 정독한 시니어 독자는 6.3절은 건너뛰어도 좋다. 다만 6.5절(Hexagonal)과 6.6절(코드 스니펫)은 Vernon 원전에 없는 *Spring 매핑*을 다루니 그쪽은 꼭 통과해 가자.

## 6.1 Aggregate를 너무 일찍 부르지 말 것

워크숍 벽으로 다시 돌아가보자. 노란 sticky 한 장에 "Order"라고 적혀 있다. 옆에 또 한 장 — "Cart". 그 옆에 — "Payment". 어떤 sticky는 동사형으로 쓰여 있고, 어떤 것은 한 단어로만 적혀 있다. 그리고 우리는 직감적으로 *이게 Aggregate인가* 자문하기 시작한다.

여기서 가장 흔한 실수가 시작된다. **Aggregate를 너무 일찍 이름 짓는 것**이다. Brandolini가 design-level EventStorming에서 거듭 경계하는 지점이다 — *postpone aggregate naming*. 노란 sticky는 "Aggregate 후보"이지 "Aggregate"가 아니다. 이름을 빨리 박는 순간, 그 이름이 *데이터의 컨테이너*로 굳어버린다. 그리고 그 컨테이너에 점점 더 많은 필드가 붙기 시작한다.

Brandolini의 경고를 그대로 옮겨와보자. "Looking at the *data* to be *contained* in the aggregate isn't the best way to go. We've seen how data and the static structure of a class would drive software stakeholders into *misleading agreements*" [B §4819]. 데이터로 자르면 모두가 동의하는 척하지만, 진짜 일관성 경계는 거기에 없다.

자, 그렇다면 진짜로 봐야 할 것은 무엇인가?

## 6.2 Aggregate는 상태 머신이다

Brandolini의 답은 명확하다 — "Aggregates as state machines" [B §4835]. Aggregate는 데이터의 모임이 아니라, *상태 전이를 책임지는 행위의 단위*다.

워크숍 벽 위에서 이 관점이 어떻게 보이는지 한번 그려보자. 노란 sticky `Order` 주변에 모인 sticky들을 보면, 항상 **command(파란색)와 event(주황색)의 짝**으로 흐른다.

- `주문 등록하기` (command) → `주문 접수됨` (event)
- `결제 완료 통보` (command) → `결제 확정됨` (event)
- `배송 시작 통보` (command) → `상품 출고됨` (event)

이 흐름이 무엇을 말하는가? `Order`라는 sticky가 **세 가지 상태**를 차례로 통과한다는 것이다 — *접수됨* → *결제 확정됨* → *출고됨*. 각 화살표가 상태 전이이고, 각 화살표 끝의 event가 *전이의 가시화*다. Aggregate를 발견했다는 말은, 이 상태 머신의 *경계*를 찾아냈다는 뜻이다. 그 머신 안에서 변하는 모든 상태가 *함께 일관성을 지켜야* 하고, 그 머신 밖의 상태는 *나중에 따라와도 된다*.

이 시점에서 한 가지 자문해보자. "주문 상품이 어떤 창고에서 출고될지를 결정하는 일은 `Order` Aggregate가 책임지나?" 답이 *명확하게 아니라*고 느껴진다면, 그건 행위의 결이 다르기 때문이다. 출고 창고 결정은 `Shipping`의 일이고, `Order`는 그 결정의 *결과*만 알면 된다. 두 머신은 서로 다른 부서에서 돌아가는 두 대의 기계다. 둘이 같은 트랜잭션에 묶일 이유가 없다.

## 6.3 Vernon의 4규칙을 sticky 위에서 검증하기

Vaughn Vernon의 *Effective Aggregate Design* 3부작에 압축된 4규칙이 있다. EventStorming 어휘로 번역해보자.

**규칙 1. Aggregate = transaction boundary**. 한 트랜잭션이 변경할 수 있는 Aggregate 인스턴스는 *하나*다. 벽에서 어떻게 검증하나? 한 command sticky가 *두 개의 노란 sticky*를 동시에 바꾸려고 하면 의심하자. 둘 중 하나가 가짜 Aggregate이거나, 둘 사이가 *eventually consistent*여야 한다.

**규칙 2. Aggregate는 작게**. Vernon이 *Implementing DDD*에서 "Customer가 모든 Order를 컬렉션으로 들고 있으면 안 된다"고 길게 설명하는 그 이유다. 큰 Aggregate는 동시성 충돌, 메모리 부하, 그리고 *학습의 부담*을 동시에 키운다. 벽에서 어떻게 검증하나? Aggregate sticky 옆에 줄줄이 매달린 *부속 sticky*가 5~6개를 넘기 시작하면 빨간불이다. 잘라낼 수 있는 단위가 그 안에 숨어 있다.

**규칙 3. Aggregate 간 참조는 ID로만**. Vernon이 두 번째 글에서 강조한다 — Aggregate A가 Aggregate B를 참조해야 한다면, B의 인스턴스를 가지지 말고 B의 `Id`만 가져라. 벽에서 어떻게 검증하나? `Order` 노란 sticky가 `Customer` 노란 sticky를 *직접 끌어안고* 있다면 의심하자. `Order`는 `CustomerId`만 안다. 고객의 상세 정보가 필요해지면 그건 *read model*의 일이다.

**규칙 4. Aggregate 간 일관성은 eventual**. 두 Aggregate가 같은 사건에 반응해야 한다면, *Domain Event*로 전파하자. 벽에서 어떻게 검증하나? `Order` 변경이 `Inventory` 변경을 *즉시* 요구한다고 느껴진다면, 정말 그러한지 도메인 전문가에게 다시 물어보자. 대부분의 경우 답은 "*몇 초 정도 늦어도 괜찮다*"이다. 그리고 그 *몇 초의 여유*가 시스템의 가용성과 단순성을 통째로 살린다.

이 4규칙을 알면서도 우리는 자주 어긴다. 익숙한 ER 다이어그램의 관성이, JPA `@OneToMany` 어노테이션의 편의가, 그리고 "한 번에 조회해야 화면이 빠르다"는 잘못된 통념이 등을 떠민다. 그래서 워크숍 벽 위에서 *명시적으로* 4규칙을 통과시키는 작업이 필요하다. sticky 한 장 한 장에 4개의 체크박스를 그리고 다음 자리로 넘어가는 식으로.

## 6.4 Servienti의 도발 — "All our aggregates are wrong"

이쯤에서 Mauro Servienti의 유명한 강연 한 편을 짚자. 제목 자체가 도발적이다 — *"All our aggregates are wrong"*. Servienti는 무엇을 wrong이라고 부르나?

답은 5장에서 이미 한 번 봤다. 데이터 관계로 자른 Aggregate가 wrong이다. 같은 "Customer"라도 Sales 컨텍스트와 Shipping 컨텍스트에서 *완전히 다른 Aggregate*여야 한다는 것이다. Sales의 Customer는 *어떤 가격대를 보여줄지*를 결정하는 데 쓰이고, Shipping의 Customer는 *어떤 주소로 보낼지*를 결정하는 데 쓰인다. 두 머신은 같은 일을 하지 않는다. 같은 클래스에 두 머신을 욱여넣으면, 결국 *둘 다 어색해진다*.

EventStorming의 swimlane 그리기와 이 통찰이 정확히 맞물린다. 워크숍에서 우리는 `Order` 한 줄을 *시간 축으로* 쭉 늘어놓는다. 그 안에서 `OrderPlacement`, `OrderFulfillment`, `OrderBilling` 같은 *행위의 단계*가 보이기 시작한다. 그 단계가 곧 *서로 다른 Aggregate*의 후보다. 같은 이름을 공유하는 *형제 머신*들이다.

이 통찰을 코드로 옮길 때, 두 가지 길이 있다.

**보수적인 길**: 같은 모듈 안에 한 `Order` Aggregate를 두되, 메서드를 *상태별로* 명확히 분리한다. `placeOrder()`, `confirmPayment()`, `markShipped()`. 한 클래스가 세 머신을 *순차적으로* 책임진다. 처음 시작하는 팀이 안전하게 갈 수 있는 길이다.

**과감한 길**: Servienti가 말하는 그대로, 서로 다른 Aggregate(`OrderPlacement`, `OrderFulfillment`)로 *물리적으로 분리*한다. 같은 데이터베이스 행을 공유하더라도, 코드 차원에서는 *다른 클래스*다. 모듈도 다를 수 있다.

어느 길이 옳다고 단정하기는 어렵다. 도메인의 복잡도와 팀의 성숙도에 따라 다르다. 다만 *둘 사이를 자유롭게 오가는 능력*은 가지고 있어야 한다. 그래서 처음에는 보수적인 길에서 출발하고, 한 Aggregate 안에 너무 많은 메서드가 모여 *어색해지기 시작하면* 과감한 길로 갈라치기를 시도하자.

## 6.5 Hexagonal Architecture — 도메인을 *가운데*에 두기

이쯤에서 한 걸음 물러서서 폴더 구조를 다시 보자. 우리는 `orders` 모듈 안에 사는 `Order` 클래스를 잘 만들었다고 치자. 그 클래스는 어디에 놓여 있는가? `OrderService`는? JPA repository는? REST controller는? Kafka listener는?

이 다섯 가지가 *같은 패키지에 모여 있으면* 한 모듈 안이 곧 진흙탕이 된다. 도메인 객체에 `@Entity`, `@RestController`, `@KafkaListener`가 모조리 붙는다. 어느 시점부터 도메인 로직과 인프라 코드를 *시각적으로 분리할 수 없게* 된다. 그러면 우리는 다시 그 코드를 "레거시"라고 부르기 시작한다.

여기서 등장하는 도구가 Hexagonal Architecture (Ports & Adapters)다. Alistair Cockburn의 1990년대 발상을, Tom Hombergs가 *Get Your Hands Dirty on Clean Architecture*에서 Spring Boot 실전으로 옮겨놓은 정전(正典)이 있다.

핵심 어휘는 셋이다.

- **Domain**: 비즈니스 규칙이 사는 곳. Spring annotation이 *거의 없는* plain POJO. 외부 세계를 모른다.
- **Port**: "시스템이 *무엇*을 할 수 있는가"를 표현하는 *인터페이스*. domain 패키지에 둔다.
  - *Inbound port* — 외부가 domain을 호출하는 진입점. *use case*라고도 부른다.
  - *Outbound port* — domain이 외부에게 부탁하는 *나가는 호출*. *driven port*라고도 부른다.
- **Adapter**: port의 *구체적인 구현*. 외부 세계와의 접점.
  - *Inbound adapter* — REST controller, message listener.
  - *Outbound adapter* — JPA repository 구현, Kafka publisher 구현, 외부 API 클라이언트.

EventStorming의 색상 grammar가 정확히 이 어휘에 매핑된다.

- **Blue Command → Inbound port (use case interface)**
- **Orange Domain Event → 도메인이 발행하는 사건** (그리고 외부 발행이 필요하면 *outbound port*로 한 번 더 추상화)
- **Pink External System → Outbound adapter** (Stripe SDK, SendGrid 등)
- **Green Read Model → Inbound port (query)** — write 쪽과는 별도 인터페이스

이 매핑이 6장의 약속이다. 워크숍 sticky의 색이 *그대로* 패키지 구조에 박힌다.

폴더 구조로 그려보자.

```
com.example.shop.orders
├── package-info.java              (@ApplicationModule "주문")
├── domain
│   ├── Order.java                  ← Aggregate Root
│   ├── OrderId.java
│   ├── OrderStatus.java
│   ├── OrderPlaced.java            ← Domain Event (named interface)
│   └── port
│       ├── in
│       │   ├── PlaceOrderUseCase.java     ← Blue Command
│       │   └── FindOrderQuery.java        ← Green Read Model
│       └── out
│           ├── OrderRepository.java       ← outbound (저장)
│           └── NotifyCustomerPort.java    ← Pink External
├── application
│   └── PlaceOrderService.java      ← use case 구현 (Application Service)
└── adapter
    ├── in
    │   └── web
    │       └── OrderController.java       ← REST
    └── out
        ├── persistence
        │   ├── OrderJpaEntity.java
        │   ├── OrderJpaRepository.java    ← Spring Data JPA
        │   └── OrderPersistenceAdapter.java
        └── notify
            └── EmailNotifyAdapter.java    ← SendGrid 호출
```

처음 이 구조를 보면 *과하지 않나* 싶을 수 있다. 작은 도메인에 폴더가 다섯 단계나 들어가는 게 부담스럽다. 하지만 한번 도메인이 충분히 자라고 나면, 이 구조가 *없을 때* 코드가 어떻게 진흙탕이 되는지가 보이기 시작한다. 작은 도메인일 때는 `application`과 `domain`을 한 패키지로 합치는 식으로 *부담을 덜어두자*. 다만 *방향성*은 처음부터 지키는 편이 낫다.

방향성이란 단 하나다 — **의존성은 *바깥에서 안으로* 흐른다**. `adapter`는 `application`과 `domain`을 안다. `application`은 `domain`을 안다. `domain`은 *아무도 모른다*. JPA를 모르고, Spring을 거의 모르고, 외부 세계의 존재를 모른다. 이 방향성이 깨지지 않는 한, 도메인은 *순수한 상태*로 살아남는다.

## 6.6 Order Aggregate를 JPA로 박기

이제 본격적인 코드를 살펴보자. 5장에서 만든 `orders` 모듈 안에, Hexagonal 컨벤션을 따라 클래스를 배치한 모습이다.

### Aggregate Root

```java
// orders/domain/Order.java
@Entity
@Table(name = "orders")
@Getter
public class Order extends AbstractAggregateRoot<Order> {

    @EmbeddedId
    private OrderId id;

    @Embedded
    private CustomerId customerId;

    @ElementCollection
    @CollectionTable(name = "order_lines")
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
            order.id, order.customerId, order.totalAmount, Instant.now()
        ));
        return order;
    }

    public void confirmPayment(PaymentId paymentId) {
        if (status != OrderStatus.PLACED) {
            throw new IllegalOrderStateException(
                "결제 확정은 PLACED 상태에서만 가능하다. 현재 상태: " + status
            );
        }
        this.status = OrderStatus.PAID;
        registerEvent(new OrderPaid(id, paymentId, Instant.now()));
    }
}
```

코드 위에 잠깐 멈춰 자문해보자. 이 클래스가 잘 잡혔는지 *4규칙*으로 검증해보자.

1. **Transaction boundary?** — `place()`와 `confirmPayment()`가 한 트랜잭션 안에서 *이 인스턴스만* 바꾼다. ✓
2. **작은 Aggregate?** — `OrderLine`만 컬렉션으로 들고 있다. `Customer`는 ID만. ✓
3. **ID 참조?** — `CustomerId`, `PaymentId`. ✓
4. **Eventually consistent?** — 결제와 출고는 *별도 Aggregate*가 책임진다. ✓

그리고 한 가지 더 살펴볼 디테일이 있다. `AbstractAggregateRoot<Order>`를 상속받았고, `registerEvent()`로 도메인 이벤트를 *등록*만 했다. 이게 무슨 뜻일까? Spring Data JPA가 이 Aggregate를 저장할 때 *자동으로* 등록된 이벤트를 발행해준다는 약속이다. `@DomainEvents` 어노테이션을 직접 쓰는 대신, 상속만으로 같은 효과를 얻는 방식이다. 자세한 발행 메커니즘은 7장에서 본다.

`@Version` 필드도 짚어두자. 낙관적 잠금이다. 두 개의 트랜잭션이 *같은 Order*를 동시에 수정하려 들면, 늦게 도착한 쪽이 `OptimisticLockingFailureException`을 받는다. 이게 *비즈니스 충돌*의 표현이다. 5분 동안 카트에 담아둔 상품을 다른 창에서 동시에 결제하려 했다면, 한쪽은 실패해야 한다. 그 실패가 *예외*로 명확히 드러나는 편이 낫다.

### Inbound Port (Use Case)

```java
// orders/domain/port/in/PlaceOrderUseCase.java
public interface PlaceOrderUseCase {
    OrderId place(PlaceOrderCommand command);

    record PlaceOrderCommand(
        CustomerId customerId,
        List<OrderLineRequest> lines
    ) {}

    record OrderLineRequest(ProductId productId, int quantity, Money unitPrice) {}
}
```

워크숍에서 본 파란 Command sticky가 그대로 인터페이스 한 줄이 됐다. *명령형 메서드 하나*. command 객체는 `record`로 immutable. 이게 외부가 도메인을 *부르는* 유일한 통로다.

### Application Service (use case 구현)

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
            .map(req -> new OrderLine(req.productId(), req.quantity(), req.unitPrice()))
            .toList();

        OrderId newId = OrderId.generate();
        Order order = Order.place(newId, command.customerId(), lines);
        orderRepository.save(order);

        return newId;
    }
}
```

이 클래스가 *얇다*는 점에 주목하자. 비즈니스 규칙은 한 줄도 없다. 모든 규칙은 `Order.place()` 안에 있다. Application Service의 책임은 *조립*이다 — 외부에서 들어온 command를 도메인 객체로 변환하고, repository를 통해 저장하고, 트랜잭션을 책임진다. 그게 전부다.

여기서 한 가지 자주 보이는 안티패턴을 짚자. 비즈니스 규칙이 Application Service로 *흘러나오는* 경우다. 가격 계산, 상태 전이 검증, 정책 적용 같은 것들이 `@Service` 클래스에 줄줄이 적혀 있는 모습. 이게 굳어지면 도메인 객체는 *getter/setter 덩어리*가 되고, 진짜 로직은 service에 있다. 이른바 *anemic domain model*이다. 이 안티패턴이 슬그머니 들어오기 시작하면 *찜찜한 신호*다. 그 시점에 멈춰서 도메인 객체로 로직을 *밀어 넣자*.

### Outbound Port와 Adapter

```java
// orders/domain/port/out/OrderRepository.java
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
}
```

도메인이 보는 repository는 *추상적인 collection*이다. JPA의 존재를 모른다. Spring Data의 존재를 모른다.

```java
// orders/adapter/out/persistence/OrderPersistenceAdapter.java
@Component
@RequiredArgsConstructor
class OrderPersistenceAdapter implements OrderRepository {

    private final OrderJpaRepository jpa;

    @Override
    public void save(Order order) {
        jpa.save(order);   // Order가 곧 @Entity이므로 그대로
    }

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpa.findById(id);
    }
}

interface OrderJpaRepository extends JpaRepository<Order, OrderId> {}
```

Spring Data가 직접 보는 `OrderJpaRepository`는 *내부 인터페이스*다. 도메인 코드는 `OrderRepository`만 안다. 어느 날 이 도메인을 MongoDB로 옮기게 된다면? `MongoOrderPersistenceAdapter`만 새로 쓰면 된다. 도메인은 한 줄도 안 건드린다. *port가 살아 있는 한* 도메인은 인프라의 변화에 면역이다.

## 6.7 Order와 OrderJpaEntity를 분리해야 할까?

코드를 한참 보다 보면 한 가지 결정이 또 등장한다. **도메인 객체와 JPA Entity를 같은 클래스로 둘 것인가, 분리할 것인가?**

위 코드는 *같은 클래스*다. `Order`가 곧 `@Entity`다. Hombergs의 책은 이를 *완전한 Hexagonal*이 아니라고 본다 — 도메인이 JPA 어노테이션을 *알게* 되기 때문이다. *순도*를 끝까지 지키려면 둘을 분리해야 한다.

```
domain
├── Order.java           ← 순수 POJO
└── ...
adapter/out/persistence
├── OrderJpaEntity.java  ← @Entity, JPA 매핑
├── OrderMapper.java     ← Order ↔ OrderJpaEntity
└── OrderPersistenceAdapter.java
```

이 방식의 장점은 명확하다. 도메인은 *완전히 순수*하다. 어떤 영속화 기술도 모른다. 단점도 명확하다 — 매핑 코드가 늘어난다. `OrderMapper`가 두 모델 사이를 *수동으로* 매번 옮긴다. 그리고 일관성 유지가 까다로워진다.

어느 길을 택할지는 팀의 상황에 따라 다르다. 다음의 가이드라인이 입에 잘 붙는다.

- **소규모 / 빠르게 출발하는 팀**: 같은 클래스로 두자. JPA 어노테이션이 도메인에 *조금* 끼는 비용이, 매핑 코드의 *상시적인* 비용보다 작다.
- **장기 운영 / 영속화 기술 교체 가능성이 있는 팀**: 분리하자. 순도가 미래의 자유를 산다.
- **하이브리드**: 도메인 객체에 JPA 어노테이션은 두되, *비즈니스 로직과 JPA 콜백을 섞지 않는* 컨벤션만 지킨다. Spring Modulith의 일반적 권장 라인이다.

선택의 옳고 그름보다, *팀이 그 선택을 의식하고 있는가*가 중요하다. 잘못된 길이 아니라 *고민 없이 들어선 길*이 위험하다.

## 6.8 sticky 색깔별 자기 자리 — 한 번 더 정리

이번 장에서 배운 매핑을 한 표로 압축해두자. 책의 후반부에서 계속 참조하게 될 척추다.

| 워크숍 sticky | 색깔 | Hexagonal의 자기 자리 | Spring 표현 |
|---|---|---|---|
| Domain Event | 주황 | domain (그리고 외부 발행 시 outbound port) | `record OrderPlaced(...)`, `registerEvent()` |
| Command | 파랑 | inbound port (use case interface) | `interface PlaceOrderUseCase` |
| Aggregate | 노랑 | domain | `@Entity` Aggregate Root |
| Policy | 라일락 | application service의 `@ApplicationModuleListener` | 7장에서 본격적으로 |
| Read Model | 초록 | inbound port (query) | `interface FindOrderQuery` + adapter |
| External System | 분홍 | outbound port + outbound adapter | `interface NotifyCustomerPort` + 구현 |
| Hotspot | 핫핑크 | (코드 위치가 아닌, 토론 trigger) | 9장에서 본격적으로 |

이 표가 6장이 책의 척추에 새겨놓는 약속이다. 워크숍 벽에서 본 sticky 한 장 한 장이, IDE 안의 *정확한 자리*를 갖는다. 그 자리가 일관되게 지켜지면, 6개월 뒤 신규 입사자가 코드를 열었을 때 *워크숍 사진을 보고 코드 위치를 찾을 수 있다*. 그게 살아 있는 모델의 모습이다.

## 마무리 — Aggregate는 발견하고, 폴더는 결정한다

6장이 한 일을 정리하자. 워크숍의 노란 sticky가 *너무 일찍 이름 붙으면* 데이터 컨테이너가 된다는 함정을 짚었다. Aggregate를 *상태 머신*으로 다시 보고, Vernon의 4규칙을 sticky 위에서 검증하는 방법을 손에 익혔다. Servienti의 도발("All our aggregates are wrong")을 통해 *행위로 자르기*의 감각을 잡았다. Hexagonal Architecture로 폴더 구조를 잡고, 색상 grammar가 폴더 위치에 그대로 박히는 매핑을 봤다. JPA + `@Version` + `registerEvent()`로 `Order` Aggregate를 실제 코드로 내려놨고, *도메인과 JPA Entity의 분리/통합* 결정을 의식적으로 내리는 자세를 익혔다.

다만 여기까지의 그림에는 한 가지 빈자리가 있다. `registerEvent()`로 등록만 해두었던 그 `OrderPlaced` 이벤트는 **실제로 누가 발행하고**, **누가 받고**, **트랜잭션 안에서 어디쯤 흘러가나**? 외부 시스템(다른 마이크로서비스, 분석 파이프라인, 알림 서비스)으로 *안전하게* 내보내려면 무엇이 필요한가?

이 질문에 답하려면 Spring의 이벤트 인프라 안으로 들어가야 한다. 다음 장에서 `@DomainEvents`, Transactional Outbox, Kafka 발행까지 한 흐름으로 살펴보자.
