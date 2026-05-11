# 5장. Pivotal Event는 Bounded Context의 칼이다 — Spring Modulith로 잘라보기

벽 앞에 다시 서보자. 4장에서 Process Modeling을 통과한 우리 손에는 두 가지가 남았다. 하나는 색깔이 가지런히 정돈된 sticky의 풍경이고, 다른 하나는 그 풍경 위에 띄엄띄엄 놓인 보라색(라일락보다 한 톤 더 진한) **Pivotal Event** 몇 장이다. `주문 접수됨`, `결제 승인됨`, `상품 출고됨`, `배송 완료됨`. 네 장이 거의 등간격으로 벽을 가르고 있다.

이쯤에서 한 가지 짚고 가자. **Big Picture는 발견이고, Software Design은 결정이다.** 발견은 누가 옳다는 판정 없이 풍경을 그리는 행위지만, 결정은 책임을 진다. 벽에서 본 그 풍경을 가지고 IDE 앞으로 돌아왔을 때, 우리가 가장 먼저 마주하는 결정이 바로 **Bounded Context를 어디서 자를 것인가**이다. 그리고 이번 장의 약속은 단순하다 — 그 칼을 손에 쥐는 법, 그리고 그 칼을 Spring 프로젝트의 패키지 구조에 실제로 내려놓는 법까지.

## Pivotal Event가 왜 칼이 되는가

벽에 붙은 sticky가 수십 장이라고 해보자. 그 모든 sticky 사이에 균등하게 선을 그을 수는 없다. 도메인은 시간 축 위에서 *고르지 않게* 흐르기 때문이다. 어떤 구간은 한 부서가 1분 안에 끝내는 작은 처리이고, 어떤 구간은 결제·물류·CS가 동시에 반응하는 큰 사건이다. 후자가 Pivotal Event다.

Brandolini가 든 예시는 정확하다 — "An e-commerce website, they might look like `Article Added to Catalogue`, `Order Placed`, `Order Shipped`, `Payment Received` and `Order Delivered`." [B §1506]. 네다섯 개. 그 이상도 그 이하도 아니다. 너무 많으면 의미가 없고, 너무 적으면 도메인을 한 덩어리로 본 것이다.

Pivotal Event를 찾는 휴리스틱은 세 가지가 입에 잘 붙는다.

첫째, **follow the money**. 돈이 움직이는 순간을 따라가보자. `결제 승인됨` 앞과 뒤에서 회사가 책임지는 의무가 달라진다. 그 전이라면 사용자는 마음을 바꿀 수 있고, 그 후라면 회사가 환불을 책임진다. 회계 처리도, 세금 신고도, 정산 사이클도 모두 그 한 sticky를 기준으로 뒤바뀐다. 이 sticky가 작은 사건일 리 없다.

둘째, **여러 부서가 동시에 반응하는 이벤트**. `주문 접수됨` 하나가 발생하면 창고는 "픽업 준비"를 시작하고, 마케팅은 "추천 모델 업데이트"를 트리거하고, CS는 "예상 문의 패턴"을 만든다. *high fan-out* 이라고 Brandolini가 부르는 그것이다 [B §4849]. 한 sticky 뒤에 여러 부서가 줄을 서면, 그 sticky는 *경계*다. 안과 밖을 가르는 칼끝이다.

셋째, **business phases**. 사람의 일상으로 환원해보자. 우리가 "오늘 점심 뭐 먹지"를 결정하기 전과 후, "결제했다"의 전과 후, "음식을 받았다"의 전과 후는 *심리적으로* 다른 단계다. 시간 축에서 모드가 바뀌는 지점, 그게 phase의 끝이고 다음 phase의 시작이다. 도메인도 똑같다. 모드가 달라지는 자리가 Pivotal Event다.

이 세 휴리스틱을 워크숍 벽 앞에서 동시에 굴려보자. 한 sticky가 셋 중 둘 이상에 걸린다면, 그건 Pivotal Event 후보다. 그 후보들을 시간 축에 띄엄띄엄 배치하고, **그 사이 구간**이 Bounded Context 후보가 된다.

## "Order"라는 단어의 함정

여기서 한 번 멈춰서 자문해보자. 그렇다면 우리가 흔히 쓰는 `Order`라는 단어는 하나의 Bounded Context인가? 답은 슬프게도 *아니다*.

Brandolini가 6장 도입부에서 길게 묘사한 풍경을 떠올려보자 — "A common concept (like the `Order` in an e-commerce web shop) becomes vital for several business capabilities, raising the need for reliability and availability... up to the unexplored limits of the CAP theorem" [B §2136]. 모두가 같은 `Order` 테이블을 바라보기 시작하면, 그 순간부터 어떤 변경도 위험해진다. 보안팀이 요구하는 컬럼 마스킹, 마케팅이 요구하는 추천 플래그, 회계가 요구하는 정산 코드. 한 테이블이 *모든 부서의 백본*이 되어버린다. 그러고는 어느 순간 개발자가 그 코드를 "레거시"라고 부르기 시작한다.

이 풍경, 익숙하지 않은가? 한국 이커머스 팀에서 `tb_order`가 컬럼 300개를 짊어진 채 살아가는 모습. 컬리 회고가 자조적으로 짚은 "Database Driven Development의 그늘"이 바로 이 풍경이다. 그래서 *같은* `Order`라도 워크숍 벽에서는 여러 곳에서 등장할 수 있고, *그래야 한다*. 결제가 보는 Order, 물류가 보는 Order, CS가 보는 Order는 서로 다른 모델이다. 같은 단어가 여러 Bounded Context에 *분리되어* 살 수 있다는 사실이, Pivotal Event 휴리스틱의 결론이다.

Mauro Servienti의 표현을 빌리자면 — "All our aggregates are wrong" [Servienti, NDC]. 데이터의 관계로 한 덩어리를 잘랐기 때문이다. 행동(behavior)으로 자르면 그 거대한 `Order`는 `OrderPlacement`, `OrderFulfillment`, `OrderBilling` 같은 더 작은, 그러나 *각자 옳은* 모델로 쪼개진다. 이 통찰이 5장의 핵심 약속이다.

> **다른 시각** — 모든 사람이 이 분할에 동의하진 않는다. Nicolas Frankel은 "modular monolith first"를 주장한다 [Frankel, "Modular Monolith"]. 마이크로서비스의 분산 비용을 짊어지기 전에, 같은 JVM 안에서 모듈만 잘 잘라도 충분히 멀리 갈 수 있다는 입장이다. Servienti가 *모델* 수준에서 잘라야 한다고 말한다면, Frankel은 *배포* 수준에서는 아직 자르지 말라고 말한다. 둘은 충돌하지 않는다. 우리가 처음 마주할 결정은 *모델은 자르되 배포는 함께*인 모듈러 모놀리스이고, 그 자리가 Spring Modulith가 자리 잡는 곳이다.

## Spring Modulith — 모놀리스 안에서 경계를 살아 숨쉬게 하기

벽에서 잘라낸 경계를 IDE로 옮기자. 한국 Spring 팀의 일상에서 가장 먼저 부딪히는 질문은 이거다 — "그래서 그 경계를 *어디에* 표현하나?"

Maven multi-module로 갈라야 할까? 별도 git repo로 분리해야 할까? 처음부터 마이크로서비스로 가야 할까? 셋 다 답이 될 수 있지만, 셋 다 비용이 크다. 그리고 셋 다 *되돌리기 어렵다*. 한번 갈라놓은 repo를 다시 합치는 일은 *번거롭다 못해 끔찍하다*. 워크숍에서 발견한 경계는 한 번에 옳을 수가 없다. 시간이 지나면서 다듬어진다. 그렇다면 처음에는 *되돌리기 쉬운* 형태로 표현하는 편이 낫다.

여기서 등장하는 도구가 Spring Modulith다. Oliver Drotbohm이 주도하는 Spring 공식 toolkit으로, 한 줄로 요약하자면 — **"패키지 단위로 모듈을 선언하고, 모듈 간 직접 의존을 ArchUnit으로 막아주는 그릇"**이다.

Modulith가 약속하는 세 가지를 살펴보자.

첫째, **Module = Bounded Context 후보**. 최상위 패키지 하나가 하나의 모듈이고, 그 모듈은 자기 하위 패키지를 자유롭게 가지되 *다른 모듈의 내부 패키지*에는 접근할 수 없다.

둘째, **Application Event 우선**. 모듈 사이의 호출은 다른 모듈의 빈을 직접 inject하지 않는다. 대신 `ApplicationEventPublisher`로 도메인 이벤트를 던지고, 듣는 쪽이 `@ApplicationModuleListener`로 받는다. 워크숍에서 그린 lilac Policy("whenever Order Placed → notify warehouse")가 코드로 *직역*되는 모양이다.

셋째, **모듈 검증의 코드화**. `ApplicationModules.of(MyApplication.class).verify()` 한 줄로 모듈 경계 침범을 JUnit 테스트로 잡는다. PR이 올라올 때마다 CI가 경계를 지킨다.

이쯤에서 코드를 한번 살펴보자. 4장 끝에서 발견한 Pivotal Event 네 장(`주문 접수됨`, `결제 승인됨`, `상품 출고됨`, `배송 완료됨`)을 가지고 세 구간으로 자른 다음, 각 구간을 Spring Modulith 모듈로 옮긴 모습이다.

```
com.example.shop
├── ShopApplication.java
├── orders            ← @ApplicationModule
│   ├── package-info.java
│   ├── Order.java
│   ├── OrderPlaced.java         (named interface)
│   └── internal
│       ├── OrderRepository.java
│       └── OrderJpaEntity.java
├── payments          ← @ApplicationModule
│   ├── package-info.java
│   ├── PaymentApproved.java     (named interface)
│   └── internal
│       └── ...
└── shipping          ← @ApplicationModule
    ├── package-info.java
    └── internal
        └── ...
```

세 모듈이 형제처럼 나란히 서 있다. 각 모듈은 자기 `internal` 하위 패키지를 가지고, 거기에 다른 모듈이 *건드리면 안 되는* 내부 구현을 둔다. 외부에 노출할 타입(이벤트 record, 공개 인터페이스)은 모듈의 최상위 패키지에만 둔다.

`package-info.java`를 어떻게 쓰는지가 처음에는 어색할 수 있다. 한번 들여다보자.

```java
// orders/package-info.java
@ApplicationModule(
    displayName = "주문",
    allowedDependencies = {"payments :: api"}
)
package com.example.shop.orders;

import org.springframework.modulith.ApplicationModule;
```

`displayName`은 Modulith가 자동 생성하는 모듈 다이어그램에 표시될 이름이다. `allowedDependencies`가 핵심이다 — 이 모듈은 `payments` 모듈의 *named interface 중 `api`*에만 의존할 수 있다고 선언한 것이다. 그 외 모듈은 호출하면 컴파일은 통과하지만 `verify()` 테스트에서 잡힌다.

named interface는 또 어떻게 표현하나?

```java
// payments/api/package-info.java
@NamedInterface("api")
package com.example.shop.payments.api;

import org.springframework.modulith.NamedInterface;
```

이 패키지 안에 둔 타입만 외부에 공개된다. 나머지(`payments.internal.*`)는 안에서만 쓴다. 자바 자체의 가시성(public/protected)을 넘어선, *아키텍처 수준의 가시성*을 Modulith가 보강해주는 셈이다.

## 모듈 의존을 ArchUnit으로 못 박기

이쯤에서 자문해보자. 그래서 누가 이걸 지키나? 사람의 양심에 맡길 일이 아니다. 다음 분기 다른 팀원이 PR을 올릴 때 `OrderService` 안에서 `ShippingInternalService`를 inject하는 일은 *반드시* 일어난다. 그것을 막아주는 것이 검증 코드다.

```java
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
            .writeIndividualModulesAsPlantUml();
    }
}
```

테스트 한 개에 모듈 경계가 통째로 걸린다. 첫 번째 테스트는 *침범이 있으면 빨갛게* 떨어진다. 두 번째 테스트는 *부수 효과*로 `target/spring-modulith-docs/` 아래에 PlantUML 다이어그램을 떨군다. 이 파일을 README에 임베드하거나 Confluence에 붙여두면, 워크숍 벽에서 잘라낸 경계가 *살아 있는 문서*가 된다. 6개월 뒤 신규 입사자가 "우리 시스템 어떻게 생겼어요?"라고 물으면, 누구도 PPT를 뒤지지 않고 그 다이어그램을 펼친다.

ArchUnit 기반 검증을 더 세밀하게 쓰고 싶다면 직접 룰을 쓸 수도 있다. 하지만 대부분의 팀에서 첫 단계는 `verify()` 하나로 충분하다. 일단 경계가 *깨지면 빨갛게 떨어진다*는 것만 확보해도, 팀 문화가 달라진다.

## Pivotal Event를 모듈 사이의 *계약*으로 옮기기

그렇다면 모듈 사이의 *대화*는 어떻게 표현하나? 워크숍에서 본 lilac Policy를 떠올려보자. "주문 접수됨 → 결제 모듈이 결제를 시도한다". 이 화살표 하나가 코드에서는 어떻게 표현될까?

```java
// orders 모듈 — Pivotal Event를 record로 노출
public record OrderPlaced(
    OrderId orderId,
    CustomerId customerId,
    Money totalAmount,
    Instant occurredAt
) {}
```

`OrderPlaced`는 `orders` 모듈의 최상위 패키지에 둔다. 이게 모듈의 *공개 어휘*다. 워크숍의 보라색 sticky가 그대로 Java record가 된 모양새다.

이 이벤트를 발행하는 자리는 `Order` Aggregate 내부다(자세한 발행 메커니즘은 7장에서 본격적으로 다룬다). 듣는 쪽은 이렇게 생겼다.

```java
// payments 모듈
@Component
class PaymentOrchestrator {

    @ApplicationModuleListener
    void on(OrderPlaced event) {
        // 결제 시도, 결과를 PaymentApproved/PaymentDeclined로 발행
    }
}
```

`@ApplicationModuleListener`는 Modulith가 제공하는 어노테이션으로, 내부적으로 `@Async`와 `@TransactionalEventListener(phase = AFTER_COMMIT)` 두 가지를 합쳐놓은 것이다. 무슨 뜻인가? **이벤트는 트랜잭션이 커밋된 *후에*, 별도 스레드에서 수신된다**. 발행자(orders)와 수신자(payments)가 *시간적으로*도, *트랜잭션적으로*도 분리된다는 약속이다.

여기서 한 가지 주의해야 한다. 동기적 메서드 호출에 익숙한 개발자라면 *비동기에서 실패가 나면 어떻게 되나*가 즉시 떠오를 것이다. 정당한 걱정이다. Spring Modulith는 그 답을 *Event Publication Registry*로 준비해두었는데, 7장에서 자세히 본다.

## modular monolith냐 microservice냐 — 결정을 미루는 법

벽에서 잘라낸 경계를 모듈로 옮기고 나면, 다음 질문이 따라온다. "그러면 우리는 이걸 결국 마이크로서비스로 갈라야 하나?"

대답은 *조급해질 필요 없다*이다. 이쯤에서 다른 시각 박스를 다시 펼쳐보자.

> **다른 시각** — Frankel은 *modular monolith first*를 권한다. 한 JVM 안에서 모듈만 잘 잘라도, 트랜잭션·관측·배포 비용을 떠안지 않고 도메인 경계를 학습할 수 있다는 것이다. Servienti는 *모델*은 처음부터 작게 자르라고 한다. 둘은 모순이 아니라 *축이 다르다*. 모델은 작게 잘라도 좋다. 배포는 함께 가져가도 좋다. Spring Modulith가 정확히 그 자리를 잡는다.

이 말이 한국 팀에 특히 와닿는 이유가 있다. 우리는 마이크로서비스의 운영 비용을 단행본 한 권으로 학습했지만, 막상 부딪히는 현실은 다르다. 분산 트랜잭션의 모호함, observability 도구의 도입과 학습 비용, 배포 파이프라인 자체의 복잡도, 그리고 *각 팀의 운영 책임 분할*. 처음 워크숍을 돌린 팀이 워크숍 결과를 마이크로서비스로 직역하면, 도메인의 학습 곡선과 운영의 학습 곡선이 *동시에* 올라오면서 둘 다 실패한다.

그래서 출발선은 *modular monolith*가 자연스럽다. 모듈 경계는 ArchUnit으로 못 박혀 있고, 이벤트 발행은 이미 `ApplicationEventPublisher` 기반이다. 어느 날 한 모듈의 부하가 다른 모듈의 5배가 되어 *분리*가 정당해지면, 그 모듈만 떼어내면 된다. 이미 이벤트로 대화하던 모듈은, 그 이벤트를 Kafka에 흘리도록 *binding*만 바꾸면 된다(7장에서 본다). 모듈러 모놀리스가 마이크로서비스의 *대안*이 아니라 *진입로*인 이유가 여기 있다.

## 4장에서 미뤄둔 read model 박스

5장을 마무리하기 전에 한 가지 빚을 청산하자. 4장에서 "Read Model은 단순한 조회 데이터가 아니라 결정의 근거"라고 잠시 짚고 미뤄둔 박스가 있었다. 그 박스는 어디로 가나? Bounded Context 안에서 어떻게 자리 잡나?

답은 8장에서 본격적으로 마저 한다. 미리 그림만 그려두자면 — read model은 *write 쪽의 Aggregate와는 다른 모델*이다. 같은 모듈 안에 있을 수도 있고, *별도 read 모듈*로 분리될 수도 있다. CQRS의 read side projection이 RSC와 React Query 캐시로 어떻게 환생하는지는 그 자리에서 자세히 본다.

## 마무리 — Pivotal Event는 단호한 칼이다

5장이 한 일을 다시 정리하자. 워크숍 벽 위에 보라색으로 띄엄띄엄 놓였던 Pivotal Event를 손에 쥐었다. *follow the money*, *high fan-out*, *business phase shift* 세 휴리스틱으로 그 후보들을 검증했다. 그 사이 구간을 Bounded Context 후보로 삼았고, Spring Modulith의 `@ApplicationModule`과 named interface로 IDE 안에 패키지 구조를 만들었다. `verify()` 테스트 하나로 그 경계를 *살아 있는 문서*로 박았다. 모듈 사이의 대화는 `ApplicationEventPublisher`로 흐르도록 설계했고, "modular monolith first → 필요 시 분리"라는 결정 보류의 자세를 익혔다.

다만 우리는 아직 *모듈의 내부*는 들여다보지 않았다. orders 모듈 안에 사는 그 `Order`는 정확히 어떤 클래스인가? `@Entity`로 잡힐 것인가? 그 안의 invariant는 누가 지키나? 그 클래스가 `OrderPlaced` 이벤트를 *어떻게* 발행하는가?

이 질문에 답하려면 모듈의 칸막이를 열고 안으로 들어가야 한다. 다음 장에서 Aggregate 발견의 절차와, JPA + Hexagonal Architecture로 그것을 코드에 박는 법을 살펴보자.
