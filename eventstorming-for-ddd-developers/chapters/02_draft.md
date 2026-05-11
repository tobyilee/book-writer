# 2장. 색상 grammar — 처음 만난 sticky note를 이해하기

문법을 모르고 문장을 짓는 건 어렵다고 말하며 1장을 닫았다. 이제 그 문법을 살펴볼 차례다. 처음 EventStorming 워크숍에 들어간 사람은 회의실 벽 앞에서 잠시 멈칫한다. 종이 롤은 8미터쯤 펼쳐져 있고, 오렌지·블루·라일락·핫핑크·노랑·초록·핑크 sticky note 묶음이 책상 위에 쌓여 있다. 누군가 묻는다. *"이건 무슨 색에 적어야 하나요?"* facilitator가 답을 하기 전에, 이 책에서 한 번 정리해두자. 색은 일곱 가지(엄밀히는 아홉 가지)지만, 머릿속에 들어와야 할 큰 그림은 단순하다.

## 색상 grammar 한 줄 요약 — alpha이자 omega

Brandolini가 *Introducing EventStorming*의 ch.13에서 던지는 한 문장이 있다. 색상 grammar의 alpha이자 omega다.

> *"There has to be a **Pink System** between a **Blue Command** and an **Orange Event**, there has to be a **Lilac Policy** between an **Orange Event** and a **Blue Command**."*

해석하면 이렇다. *파란 명령*과 *오렌지색 사건* 사이에는 항상 *분홍 시스템*이 있어야 하고, *오렌지색 사건*과 *파란 명령* 사이에는 항상 *라일락 정책*이 있어야 한다. 그림으로 그리면 작은 사슬이 된다.

```
[Blue Command] → [Pink System] → [Orange Event]
                                        ↓
                                  [Lilac Policy]
                                        ↓
                                  [Blue Command] → ...
```

이 사슬이 도메인의 한 호흡이다. 누군가가 *명령*을 던지면, *시스템*이 그 명령을 처리하고, 그 결과 *사건*이 발생한다. 그 사건은 그냥 사라지지 않는다. 어딘가에 있던 *정책*("X가 일어나면 Y를 한다")이 그 사건을 감지하고, 다음 *명령*을 만들어낸다. 명령 → 시스템 → 사건 → 정책 → 명령 → 시스템 → 사건 ... 이 작은 고리가 끝없이 이어지면서 도메인 전체의 흐름이 만들어진다.

여기에 두 가지 곁가지가 붙는다. 첫째, 명령은 누군가가 던지는데 그 *누군가*가 작은 노란색 sticky로 표현되는 **Actor**다. 둘째, 정책이 다음 명령을 만들 때 *어떤 정보*를 보고 결정한다. 그 정보가 초록색 sticky인 **Read Model**이다. 그리고 흐름 안에서 풀리지 않는 의문이 생기면 핫핑크 sticky로 **Hotspot**을 표시한다. 비즈니스에 중요한 갈림길이 되는 사건은 보라색 테이프를 더해 **Pivotal Event**로 강조한다.

이게 전부다. 일곱 색깔, 그 이상도 이하도 아니다. 그런데 막상 실전에서는 sticky note 하나하나가 "이건 무슨 색이지?"라는 의문을 부른다. 색 하나씩 짚어가며 정의와 Java 비유를 함께 살펴보자. Java 비유를 끼워넣는 이유는 분명하다. 우리 머릿속에는 이미 *타입 시스템*이라는 강력한 분류 도구가 있다. 그 도구를 sticky note 위에 올려놓으면 색상 grammar가 갑자기 친숙해진다.

## 색상 정의 표

본격적으로 들어가기 전에 일곱 색을 한 표로 모아두자. 워크숍 벽에 늘 붙여둘 "Visible Legend"의 축약본이라고 보면 된다.

| 색상 | 역할 | 표기 형태 | Java 비유 |
|------|------|----------|-----------|
| **Orange** | Domain Event — 도메인에서 일어난 사실 | 과거 시제 동사구 | `record OrderPlaced(...) implements DomainEvent` |
| **Blue** | Command — 의도, 결정 | 명령형 동사구 | `record PlaceOrder(...) implements Command` |
| **Pink (large)** | External System — 우리 통제 밖의 시스템 | 시스템 이름 | 외부 어댑터(Stripe SDK, SendGrid 등) |
| **Lilac (purple)** | Policy — "X가 일어나면 Y를 한다" 반응 규칙 | "Whenever ... then ..." | `@TransactionalEventListener` 메서드 |
| **Yellow (rectangle)** | Aggregate — 일관성 경계, 상태 머신 | 명사 | `@AggregateRoot`가 붙은 JPA 엔티티 |
| **Small Yellow (person)** | Actor / Persona — 명령을 내리는 사람 | 사람 이름 또는 역할 | API 호출자, 인증된 `Principal` |
| **Green (rectangle)** | Read Model — 결정의 근거가 되는 정보 | 화면·데이터 이름 | CQRS read projection, React Query 캐시 |
| **Hot Pink (red)** | Hotspot — 의문·갈등·미해결 이슈 | 자유로운 메모 | 코드의 `// FIXME`, PR 코멘트 |
| **Pivotal Event** | 비즈니스 흐름의 분기점 | 오렌지 + 색 테이프 | Bounded Context의 경계 사건 |

이 표를 처음 보는 사람에게는 단순한 chart로 보이겠지만, 사실은 *합의서*에 가깝다. 각 색의 의미가 워크숍 참가자 사이에 합의돼 있어야 같은 그림이 그려진다. 그래서 Brandolini가 ch.8에서 "Visible Legend"라는 짧은 절을 특별히 두는 것이다. 이 표를 벽에 항상 보이게 붙여두는 것이 색깔 자체보다 중요하다. 한국 팀에서 자주 빠지는 함정 중 하나는, legend는 안 붙이고 sticky만 잔뜩 사다가 워크숍 30분쯤 지난 시점에 "이건 라일락인가 핑크인가" 같은 토론으로 시간을 날리는 경우다. 끔찍한 일이다. legend 한 장이면 막을 수 있는 손실이다.

이제 색깔 하나씩 들어가보자. 가장 먼저 깔리는 sticky, 오렌지부터다.

## Orange — Domain Event: 과거 시제로 적힌 사실

오렌지색 sticky note 한 장을 손에 들고 회의실 벽 앞에 섰다고 해보자. 위에 무엇을 적어야 할까? Brandolini의 규칙은 단순하다. *과거 시제로 적힌, 도메인에서 일어난 사실*이다. "Order Placed", "Payment Received", "Item Shipped". 한국어로 하면 "주문이 접수됐다", "결제가 완료됐다", "상품이 출고됐다". 동사는 *과거형*이어야 한다. 미래도 아니고, 현재 진행도 아니고, 가정도 아니다. *이미 일어난 일*만 적는다.

왜 과거 시제일까? 과거 시제는 거짓말을 하기 어렵다. "주문이 접수됐다"는 사실은 누군가의 의도가 아니라 *현실*이다. 의도는 명령(Command)으로 표현하고, 현실은 사건(Event)으로 표현한다. 이 구분이 도메인의 *지나간 흔적*과 *앞으로의 의지*를 깔끔하게 가른다.

Java 개발자가 이 정의를 들으면 자연스럽게 떠오르는 게 있다. *불변 값 객체*다. 도메인 이벤트는 한 번 발생하면 바꿀 수 없다. 시점도 박혀 있고, 참여한 데이터도 박혀 있다. 그래서 도메인 이벤트는 Java record로 표현하는 편이 가장 자연스럽다. 그 자체로 불변이고, 동등성은 값 기반이고, 시그니처가 단순하다.

```java
public record OrderPlaced(
        OrderId orderId,
        CustomerId customerId,
        Money total,
        Instant occurredAt
) implements DomainEvent {}
```

이 record 한 줄이 sticky note 한 장에 정확히 대응한다. sticky 위에는 "Order Placed"라고 쓰여 있고, 코드에서는 `OrderPlaced`라는 record가 그 사실을 담는다. 시점은 `occurredAt`으로 분명히 박혔고, 누구의 주문이고 얼마짜리인지가 record 필드로 남는다. 이 매핑이 책 후반부 7장에서 본격적으로 풀린다. 지금은 *오렌지색 sticky 한 장 = Java record 한 개*라는 직관만 가져가자.

이벤트 이름을 짓는 일은 의외로 어렵다. "Order Placed"인가 "Order Created"인가? "Payment Received"인가 "Payment Captured"인가? 도메인 전문가가 실제로 쓰는 단어를 따르자. 회의에서 누군가가 "주문 접수"라는 단어를 자연스럽게 던졌다면 그것이 ubiquitous language의 단서다. 그 단어를 sticky에 적고, 코드에도 그대로 옮기자. 회계 팀이 "정산 마감"이라는 단어를 쓴다면 `SettlementClosed`가 코드에 등장해야 한다.

## Blue — Command: 의도와 결정

파란색 sticky는 *의도*다. "주문을 접수하라(Place Order)", "결제를 승인하라(Authorize Payment)", "재고를 차감하라(Decrease Stock)". 동사는 명령형이고, 누군가의 결정을 담는다. 그 누군가는 사람일 수도 있고(고객이 결제 버튼을 누르는 순간), 다른 시스템일 수도 있다(스케줄러가 정산 명령을 던지는 순간). 그래서 파란색 sticky 옆에는 보통 작은 노란색 sticky로 *Actor*가 따라붙는다.

Command와 Event를 구분하는 일이 처음에는 헷갈린다. *주문을 접수하라*와 *주문이 접수됐다*는 같은 도메인 사실의 두 얼굴 아닌가? 비슷하지만 다르다. Command는 *시도*다. 실패할 수 있다. 재고가 모자라서 거부될 수도 있고, 결제 카드가 한도 초과여서 막힐 수도 있다. Event는 *결과*다. 성공한 시도만 Event가 된다. 명령 → 시스템 → 사건의 사슬에서 시스템이 거부하면 Event는 발생하지 않거나, 거부 자체가 별도의 Event(`OrderRejected`)로 기록된다.

Java로 옮기면 Command 역시 record다. 다만 의미는 다르다.

```java
public record PlaceOrder(
        CustomerId customerId,
        List<LineItem> items,
        PaymentMethod paymentMethod
) implements Command {}
```

이 record는 *시도되기 전*의 상태를 담는다. Spring 백엔드라면 REST 컨트롤러가 받은 요청을 Command로 변환해 use case 함수로 넘기고, 그 함수가 도메인 모델을 변경한 다음 결과로 `OrderPlaced` Event를 발행한다. Command record와 Event record는 시그니처가 닮았지만, 책임이 다르다. 6장에서 hexagonal architecture를 그릴 때 Command는 *inbound port*의 입력으로 등장하고, Event는 *outbound port*의 출력으로 등장한다.

여기서 한 가지 짚어두자. Command와 Event를 같은 클래스로 합치고 싶은 유혹이 있다. "어차피 같은 필드인데 왜 두 번 정의하지?" 그 유혹을 견디는 편이 낫다. 같은 필드라도 의미가 다르고, 미래에 분기하기 때문이다. Command는 검증을 받고, Event는 보관·전파된다. 두 record를 두는 것이 *typesystem 위의 분리된 책임*이다. 한 클래스로 합치면 코드 단계에서 그 구분이 흐려지고, 결국 같은 함정으로 떨어진다.

## Pink — External System: 우리 통제 밖의 세계

분홍색(엄밀히는 핫핑크보다 약간 큰 큰 핑크) sticky는 *우리가 통제하지 못하는 시스템*이다. Stripe, SendGrid, 카카오페이, 토스페이먼츠, 카페24 ERP, 사내 다른 팀의 인증 서버 — 우리 코드 베이스 밖에서 우리에게 영향을 주는 모든 것. 결제 게이트웨이가 응답을 늦게 주면 우리 주문 흐름이 막힌다. 외부 ERP가 한 번 멈추면 우리 정산이 한 시간 늦어진다. 이런 시스템은 *우리가 어떻게 잘 만들든* 통제할 수 없다.

Brandolini가 이 색을 따로 두는 이유는 단순하다. *책임의 경계*를 시각화하기 위해서다. 워크숍에서 "결제 승인" sticky 옆에 분홍색 "PG사" sticky가 붙으면, 그 자리에서 "이 사건의 실패는 우리 책임이 아니다"가 모두에게 분명해진다. 사람 사이의 finger-pointing이 sticky 위에서 일어난다. 회의실 분위기가 부드러워진다.

Java로 옮기면, 외부 시스템은 *outbound adapter*가 된다. Hexagonal Architecture의 용어로 외부 port 뒤의 구체 구현이다.

```java
public interface PaymentGateway {  // outbound port
    PaymentResult charge(Money amount, PaymentMethod method);
}

@Component
class StripePaymentGateway implements PaymentGateway {  // outbound adapter
    // Stripe SDK 호출
}
```

분홍색 sticky 하나가 *인터페이스 하나 + adapter 하나*의 쌍으로 떨어진다. 6장에서 본격적으로 다룬다. 지금은 *분홍색 = 외부 세계*만 기억해두자.

## Lilac — Policy: 반응의 규칙

라일락(연보라) sticky는 *규칙*이다. 형식은 항상 "Whenever X happens, then do Y" — *X가 일어나면 Y를 한다*. 가장 흔한 예시. *Whenever an order is placed, then notify the warehouse to ship.* 주문이 접수되면 창고에 출고 요청을 보낸다. 이 한 줄이 라일락 sticky 한 장이다.

Policy는 EventStorming 문법의 hinge(경첩)다. 오렌지 Event를 받아 파란 Command를 만든다. Event가 *과거*고 Command가 *미래*라면, Policy는 그 사이를 잇는 *반응*이다. 도메인 안의 모든 자동화는 Policy로 표현된다. 사람이 직접 결제 승인 후에 출고 요청을 누르는 경우라면 actor가 들어가지만, 시스템이 자동으로 처리하는 경우는 라일락 sticky 한 장으로 표현된다.

Java/Spring으로 옮기면 Policy는 가장 자연스럽게 `@TransactionalEventListener` 메서드가 된다.

```java
@Component
public class OrderPlacedShippingPolicy {

    private final ShippingService shippingService;

    // "주문이 접수되면 → 출고 요청을 보낸다"
    @TransactionalEventListener
    public void on(OrderPlaced event) {
        shippingService.requestShipment(event.orderId());
    }
}
```

이 코드 한 덩어리가 sticky 한 장이다. 클래스 이름이 sticky 위의 문장이고(`OrderPlacedShippingPolicy` ≈ "주문 접수 시 출고 정책"), 메서드 시그니처가 Event ↔ Command의 다리다. Spring Modulith를 쓰면 `@ApplicationModuleListener` 한 줄로 비동기·트랜잭션·재시도까지 챙겨준다. 7장에서 본격적으로 다룬다.

Policy를 Java record로 표현해도 좋다. 워크숍 단계에서 Policy를 *데이터*로 모델링하면 추후 자동화의 청사진이 된다.

```java
public record OnOrderPlacedNotifyShipping(
        String name,
        String triggerEvent,    // "OrderPlaced"
        String issuedCommand    // "RequestShipment"
) implements Policy {}
```

record로 표현하면 Policy 카탈로그를 코드에 박을 수 있다. 어떤 도메인 이벤트에 어떤 Policy가 걸려 있는지를 한 군데서 볼 수 있다. 다만 실전에서는 record는 워크숍 단계의 *기록*으로 두고, 실제 구현은 위의 `@TransactionalEventListener` 메서드 쪽으로 가는 편이 자연스럽다.

## Yellow — Aggregate와 Actor

노란색은 두 종류다. *큰 노란색 사각형*은 **Aggregate**고, *작은 노란색 사람 모양*은 **Actor**다. 모양만 다르고 색은 같다. 처음에는 헷갈리지만 워크숍 벽에서는 모양 차이가 분명해서 금방 익숙해진다.

**Aggregate**는 명령을 받아 일관성을 보장하는 상태 머신이다. 노란색 sticky 위에는 명사만 적힌다 — `Order`, `Cart`, `Customer`. 의도(파란색)와 사실(오렌지) 사이에서 *비즈니스 규칙을 검증하는 자리*가 Aggregate다. 누가 "주문을 접수하라"(파란색 Command)고 던지면, `Order` Aggregate가 그 명령을 받아 재고가 충분한지, 결제 한도가 남았는지를 검증한 다음, 검증을 통과하면 `OrderPlaced`(오렌지색 Event)를 발행한다. 이 검증의 자리에 *불변식*(invariant)이 박힌다.

Java로 옮기면 Aggregate Root는 보통 JPA `@Entity`로 표현되고, `@Version` 어노테이션으로 낙관적 잠금을 건다. 그리고 `@DomainEvents` 메서드로 저장 시 자동으로 이벤트를 발행한다.

```java
@Entity
public class Order {
    @Id private OrderId id;
    @Version private long version;
    private OrderStatus status;
    private List<OrderLine> lines;

    // 비즈니스 규칙은 여기로 모인다
    public void place(StockChecker stockChecker) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("이미 접수된 주문입니다");
        }
        stockChecker.assertAvailable(lines);
        status = OrderStatus.PLACED;
        registerEvent(new OrderPlaced(id, totalAmount(), Instant.now()));
    }

    @DomainEvents
    Collection<DomainEvent> domainEvents() { /* ... */ }
}
```

이 매핑은 6장에서 본격적으로 풀어낸다. 지금은 *큰 노란색 sticky = 코드 안의 상태 머신*이라는 것만 가져가자. Brandolini가 ch.20에서 "Aggregate as state machine"이라는 표현을 쓰는데, 이게 핵심이다. Aggregate는 데이터 컨테이너가 아니라 *상태 전이의 규칙 묶음*이다.

**Actor**(작은 노란색 사람 모양)는 명령을 던지는 주체다. 고객, 관리자, 운영자, 다른 시스템의 어떤 모듈. 워크숍에서는 actor를 명령 옆에 작게 붙여 *누구의 의도인지*를 분명히 한다. Java/Spring 코드로는 보통 인증된 `Principal`, JWT 클레임, API 호출자의 client ID로 등장한다. 컨트롤러에서 `@AuthenticationPrincipal`로 받아 Command record에 함께 담는 패턴이 흔하다.

## Green — Read Model: 결정의 근거

초록색 sticky는 *결정을 내리기 위해 읽는 정보*다. 화면, 보고서, API 응답, 캐시 — 사용자가 다음 행동을 결정하기 위해 *보는* 모든 것. 워크숍에서 "주문 목록"(고객이 자기 주문을 확인하는 화면), "출고 대기 리스트"(창고 담당자가 무엇을 출고할지 보는 화면), "정산 요약"(회계 담당자가 정산 상태를 보는 화면) 같은 sticky가 초록색으로 붙는다.

여기서 사소해 보이지만 결정적인 *관점 전환*이 일어난다. 한국 개발자는 "조회 데이터"라는 표현에 익숙하다. ERD를 먼저 그리고, 그 위에 JPQL이나 native query로 데이터를 뽑아내는 패턴. 그런데 Brandolini는 초록색 sticky를 단순한 조회 데이터가 아니라 *결정의 근거*로 정의한다. *무엇을 조회하는가*가 아니라 *어떤 결정을 위해 무엇을 보는가*가 핵심이다.

이 관점이 코드 구조를 바꾼다. CQRS의 read side projection이 바로 이 자리에 들어선다. Write 모델은 도메인 일관성을 위해 정규화된 JPA 엔티티지만, Read 모델은 *결정에 필요한 모양*으로 미리 가공된 별도의 view다. 그리고 프론트엔드의 React Query 캐시 키 한 개가 정확히 초록색 sticky 한 장에 대응한다. 8장에서 본격적으로 다룬다.

```typescript
// 8장 미리보기 — 초록색 sticky가 React Query 캐시 키로 환생한다
const { data: orders } = useQuery({
  queryKey: ['orders', customerId],
  queryFn: () => api.getOrders(customerId),
});
```

`['orders', customerId]`라는 캐시 키가 워크숍 벽의 "내 주문 목록" 초록색 sticky와 정확히 1:1로 떨어진다. 이 매핑이 EventStorming과 모던 프론트엔드의 자연스러운 다리다.

## Hot Pink — Hotspot: 미해결의 안전한 표식

핫핑크(또는 빨간색) sticky는 *의문, 갈등, 미해결 이슈*다. 워크숍에서 "이거 어떻게 처리하지?" "여기서 자주 문제가 생기는데..." "이게 정확히 누구 책임이지?" 같은 발화가 나오는 순간 facilitator가 핫핑크 sticky 한 장에 그 말을 적어 흐름 옆에 붙인다.

Hotspot은 Brandolini가 책에서 짧지만 강하게 짚는 개념이다. 표현이 인상적이다 — *"a safer target for finger-pointing"*. 안전한 finger-pointing 표적. 한국 조직 회의에서 가장 두려운 게 *누가 잘못했나*로 흐르는 분위기다. EventStorming은 그 finger-pointing을 *사람*에서 *벽 위의 sticky*로 옮긴다. "결제와 정산 사이가 자주 깨진다"라는 핫핑크 sticky가 벽에 붙으면, 회의실 안의 누구도 비난받지 않는다. 문제는 모델 위에 있고, 모두가 그 sticky를 함께 본다. 회의 분위기가 부드러워진다.

이건 사소해 보이지만 워크숍의 *심리적 안전*을 만드는 결정적 장치다. 한국 팀이 EventStorming을 도입할 때 가장 큰 효과를 보는 부분이기도 하다. 오토피디아 회고에서 "워크숍은 실패했다"라고 적었지만, 그 회고 자체가 핫핑크 sticky의 정신과 닿아 있다 — *사람을 비난하지 않고 도구·과정을 들여다본다*.

Java 코드로 직접 옮기는 건 어렵다. 비유하자면 `// FIXME` 주석이거나 GitHub Issue 또는 Linear ticket이다. 9장에서 이 핫핑크 sticky가 어떻게 PR 백로그로 흘러가는지를 짧게 다룬다.

## Pivotal Event — 비즈니스 흐름의 분기점

마지막 한 색깔. 정확히는 새 색이 아니라 *기존 오렌지색 sticky에 색 테이프나 강조를 더한 것*이다. **Pivotal Event**는 비즈니스 흐름에서 가장 의미 있는 사건이다. Brandolini의 정의를 그대로 가져오면: 이커머스 도메인이라면 `Article Added to Catalogue`, `Order Placed`, `Order Shipped`, `Payment Received`, `Order Delivered` 같은 5개 안팎의 사건. *여러 부서가 동시에 반응하는 사건*이거나 *돈이 움직이는 사건*이 보통 pivotal이다.

이 개념이 결정적인 이유는 5장에서 본격적으로 풀린다. *Pivotal Event 사이의 구간이 Bounded Context 후보가 된다.* 워크숍 벽에 보라색 테이프로 강조된 오렌지 sticky 5개가 한 줄로 늘어선다면, 그 사이의 4~5개 구간이 우리 Spring Modulith의 모듈 후보다. 즉, sticky 한 장이 *모듈 경계의 칼날*이 된다. 한국 Spring 팀이 모놀리스를 자르는 가장 자연스러운 출발점이다.

지금은 *오렌지 + 색 테이프 = 도메인의 큰 분기점*이라는 직관만 가져가자.

## Visible Legend — 벽에 항상 붙여두자

색을 다 살펴봤다. 머리에 그림이 그려졌을 것이다. 그러나 워크숍 현장에서는 머릿속 그림으로 부족하다. *눈에 보여야* 한다.

Brandolini가 ch.8에 "Visible Legend"라는 짧지만 중요한 절을 둔다. 핵심은 단순하다. 회의실 벽 한쪽에 색별 의미가 적힌 작은 표를 *항상 보이게* 붙여두자. 워크숍 참가자 대부분은 *처음* EventStorming을 한다. 그들은 안 그래도 익숙하지 않은 표기법에 떠밀려 있는 상태다. 거기에 "이 분홍색이 뭐였더라?"라는 사소한 의문 하나만 더해져도 흐름이 끊긴다. 그 작은 끊김이 누적되면 워크숍이 죽는다.

legend 한 장이 그 작은 끊김을 다 막는다. 5분이면 만들고 한 번 붙이면 끝이다. 이렇게 사소한 디테일을 책에 한 절씩 두는 이유가 있다. EventStorming은 *학습이 멈추지 않게 하는 작은 안전장치들의 묶음*이다. legend, 풍족한 sticky, 풍족한 마커, 의자 없는 회의실 — 하나하나 사소하지만 빠지면 전체가 흔들린다.

## 색상 강박 — 한 줄 경고

한 가지만 짚고 넘어가자. 색깔을 정확히 분류하는 *강박*에 빠지는 일이 흔하다. "이건 yellow야 orange야?", "이건 lilac이야 pink야?" 같은 토론으로 30분을 쓴다. 끔찍한 일이다. facilitator의 답은 단순하다. *둘 다 붙이고 넘어가자.* 색깔은 grammar지 규칙이 아니다. 11장에서 본격적으로 다룬다. 지금은 *grammar로서의 color*만 잡아두면 충분하다.

## Java record 한 세트로 마무리

마지막으로, 이 챕터에서 본 색깔의 핵심을 Java record 한 세트로 압축해보자. 워크숍 벽의 색상 grammar가 우리 IDE에서 어떻게 보일지의 *예고편*이다.

```java
// 도메인 이벤트(오렌지)와 명령(블루)을 같은 sealed interface 아래 묶는다
public sealed interface DomainEvent permits OrderPlaced, PaymentReceived, OrderShipped {}
public sealed interface Command      permits PlaceOrder, AuthorizePayment, RequestShipment {}
public sealed interface Policy       permits OnOrderPlacedNotifyShipping {}

// 오렌지: 과거 시제 사실
public record OrderPlaced(OrderId orderId, Money total, Instant occurredAt) implements DomainEvent {}

// 블루: 의도, 결정
public record PlaceOrder(CustomerId customerId, List<LineItem> items) implements Command {}

// 라일락: 반응 규칙
public record OnOrderPlacedNotifyShipping(String name) implements Policy {}
```

`sealed interface`를 쓰는 이유는 *문법을 코드 단계에서 강제*하기 위함이다. Domain Event가 될 수 있는 record는 명시적으로 허용된 것들뿐이다. Command도, Policy도 마찬가지다. typesystem이 색상 grammar를 떠받친다. 이 작은 코드 한 덩어리가 워크숍 벽의 sticky 색깔과 정확히 1:1로 떨어진다.

내 Spring 프로젝트의 `OrderService`에서는 이게 어떻게 보일까? 7장에서 본격적으로 펼친다. 그 때까지는 *색깔 = 타입 시스템의 분류*라는 직관을 잡고 가자.

## 마무리 — 다음 챕터로

색상 grammar 한 바퀴를 돌았다. 일곱 색깔의 의미와 Java 타입 시스템 비유, 그리고 워크숍 벽 위에서 그것들이 어떻게 결합되는지를 살펴봤다. 그런데 색깔만 알아서는 워크숍이 굴러가지 않는다. *언제, 어떤 순서로, 어떻게* 그 색깔들이 벽에 올라가는지의 절차가 필요하다.

다음 챕터에서는 가장 큰 격(格)의 EventStorming — Big Picture 워크숍의 6단계 절차를 한국 이커머스 도메인을 회의실 벽에 펼친다는 가정 아래 함께 시뮬레이션해보자. 종이가 펼쳐지고, 첫 오렌지 sticky가 붙고, hotspot이 등장하고, pivotal event가 보라색 테이프로 강조되고, 마지막에 arrow voting으로 다음 문제가 선택된다. 그 흐름을 따라가다 보면 우리 회사 다음 워크숍의 윤곽이 머릿속에 그려질 것이다.
