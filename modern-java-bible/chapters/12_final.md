# 12장. Sealed Classes — 합 타입(Sum Type)이 자바에 들어온 날

결제 시스템의 한 팀이 enum 하나를 두고 회의를 하고 있다고 해보자. `PaymentResult`라는 이름의 enum이다. 처음 만들어졌을 때는 `APPROVED`와 `DECLINED` 둘뿐이었다. 깔끔했다. 하지만 사업이 자라면서 상태가 늘었다. `PENDING`이 추가됐고(3D Secure 인증 대기), `CANCELLED_BY_USER`가 붙었고, `PARTIAL_REFUND`가 들어왔고, 어제는 `FRAUD_HOLD`가 추가됐다.

그리고 오늘 PM이 새 요구를 들고 왔다. "*승인된 결제에는 승인 시각과 카드 발급사 코드*가 같이 보관돼야 하고, *거절된 결제에는 거절 사유와 retry 가능 여부*가 있어야 한다. *Pending에는 인증 URL과 만료 시각*이 필요하다." 한 자리에 있던 enum이 갑자기 각자 다른 데이터를 요구하기 시작한 것이다.

이쯤 되면 enum 옆에 `Map<PaymentResult, Object>`를 두거나, `if (result == APPROVED) { ... } else if (result == DECLINED) { ... }` 식의 분기 안에서 캐스팅을 시작한다. 둘 다 *찜찜한 코드*다. 컴파일러가 더 이상 우리를 도와주지 않는다 — "Pending 상태일 때 인증 URL이 반드시 있다"는 약속이 *주석으로만 존재*하기 때문이다. 한 줄을 빠뜨리면 production에서 NPE가 난다.

다른 회사의 비슷한 자리에서는 어떻게 했을까? Scala라면 `sealed trait PaymentResult` 한 줄로, Kotlin이라면 `sealed class PaymentResult`로, Rust라면 `enum PaymentResult { Approved { ... }, Declined { ... } }`로 풀었을 자리다. 함수형 계열 언어들이 30년 동안 *합 타입(sum type)*이라 부르며 다뤄온 그 도구가 자바에 왔다. Java 17부터다.

이 장에서는 sealed classes가 무엇이고, *enum으로는 안 됐던 무엇*을 풀어주는지를 함께 살펴보자. 결제 상태 모델을 enum에서 sealed로 옮기면서, 그동안 Visitor 패턴이 6번째로 같은 코드를 적게 만들던 *지긋지긋함*도 같이 정리해보자.

## sealed가 도입되기 전, 우리는 무엇을 못 했나

**enum으로 충분했을까?** 짧게 답하면, enum은 *고정된 상수 집합*에만 충분하다. 각 상수가 *서로 다른 모양의 데이터*를 요구하는 순간 enum은 한계를 드러낸다. 위의 `PaymentResult`가 정확히 그 한계다.

물론 enum에 필드와 메서드를 붙일 수는 있다. 그러나 그것은 *모든 상수가 같은 필드를 가져야* 한다는 의미다. `APPROVED`에는 카드 발급사 코드가 필요하지만 `PENDING`에는 인증 URL이 필요할 때, enum은 두 필드를 *모두* 가지게 된다. 그리고 `PENDING` 인스턴스의 카드 발급사 코드는 null로 남는다. 다시 *찜찜한 코드*다.

그래서 자바 개발자들은 두 가지 우회를 만들어왔다. 하나는 **클래스 계층 + 추상 클래스**. `abstract class PaymentResult`를 만들고 `Approved`, `Declined`, `Pending`이 `extends`하는 식이다. 각 sub-class가 자기 필드를 가진다. 이렇게 하면 데이터 모양은 풀린다. 그러나 새로운 문제가 등장한다 — *누구나 그 추상 클래스를 상속할 수 있다*. 라이브러리를 사용하는 외부 코드가 `class HackedResult extends PaymentResult` 한 줄로 우리 도메인을 *오염*시킬 수 있다.

다른 하나는 **Visitor 패턴**이다. 1990년대에 GoF가 제안한 그 패턴이다. *분기를 객체화*해서 컴파일러에 분기의 완전성을 위탁하는 기법. 일단 코드 한 덩이를 보자.

```java
public abstract class PaymentResult {
    public abstract <R> R accept(Visitor<R> visitor);

    public interface Visitor<R> {
        R visitApproved(Approved a);
        R visitDeclined(Declined d);
        R visitPending(Pending p);
    }

    public static final class Approved extends PaymentResult {
        private final Instant approvedAt;
        private final String issuerCode;
        public Approved(Instant approvedAt, String issuerCode) {
            this.approvedAt = approvedAt;
            this.issuerCode = issuerCode;
        }
        public Instant approvedAt() { return approvedAt; }
        public String issuerCode() { return issuerCode; }
        @Override
        public <R> R accept(Visitor<R> visitor) { return visitor.visitApproved(this); }
    }

    public static final class Declined extends PaymentResult {
        private final String reasonCode;
        private final boolean retryable;
        public Declined(String reasonCode, boolean retryable) {
            this.reasonCode = reasonCode;
            this.retryable = retryable;
        }
        public String reasonCode() { return reasonCode; }
        public boolean retryable() { return retryable; }
        @Override
        public <R> R accept(Visitor<R> visitor) { return visitor.visitDeclined(this); }
    }

    public static final class Pending extends PaymentResult {
        private final URI authenticationUrl;
        private final Instant expiresAt;
        public Pending(URI authenticationUrl, Instant expiresAt) {
            this.authenticationUrl = authenticationUrl;
            this.expiresAt = expiresAt;
        }
        public URI authenticationUrl() { return authenticationUrl; }
        public Instant expiresAt() { return expiresAt; }
        @Override
        public <R> R accept(Visitor<R> visitor) { return visitor.visitPending(this); }
    }
}
```

50줄 가까이 됐다. 그리고 사용 측은 이렇게 적는다.

```java
String message = result.accept(new PaymentResult.Visitor<String>() {
    @Override public String visitApproved(Approved a) {
        return "결제 완료: " + a.issuerCode();
    }
    @Override public String visitDeclined(Declined d) {
        return d.retryable() ? "재시도 가능" : "재시도 불가";
    }
    @Override public String visitPending(Pending p) {
        return "인증 필요: " + p.authenticationUrl();
    }
});
```

호출 한 번을 위해 익명 클래스 한 덩어리가 매번 등장한다. 새 상태가 추가될 때마다 — `FraudHold`를 더한다고 해보자 — Visitor 인터페이스에 `visitFraudHold`를 추가하고, *모든 호출 사이트*가 컴파일 에러를 통해 갱신을 요구한다. 컴파일러가 완전성을 보장해주긴 한다. 그 점은 좋다. 하지만 *대가가 너무 크다*.

이 코드를 6번째로 적던 어느 날, 자바 개발자라면 모두 한 번쯤 한숨을 쉬어봤을 것이다. "왜 자바는 *닫힌 계층*을 일등 시민으로 받아주지 않는가?" 그 질문에 대한 OpenJDK의 답이 sealed classes다.

## JEP 360에서 409까지 — 자바의 답

연표를 짧게 짚자.

> **진화 박스 — Sealed Classes 표준화**
>
> - **Java 15 (2020-09)** — JEP 360 First Preview. `sealed`·`permits`·`non-sealed` 키워드의 골격 등장.
> - **Java 16 (2021-03)** — JEP 397 Second Preview. 같은 컴파일 단위면 `permits` 생략 가능 등의 미세 조정.
> - **Java 17 (2021-09)** — JEP 409 Standard. 첫 post-Java 8 LTS와 함께 표준화. records(JEP 395)는 16에 먼저 표준이 됐는데, sealed가 17에서 합류하며 *records + sealed*의 짝패가 동시에 성숙해진다.

이 흐름이 뜻하는 바가 있다. records는 *product type*, sealed는 *sum type*. 둘이 *같은 LTS 사이클에서 표준에 들어왔다*. 자바 17이라는 LTS의 정체성을 단 한 단어로 정리해야 한다면 **"데이터지향(data-oriented)"** 이다. records와 sealed가 *짝패로 들어왔기 때문에* 그 명명이 가능해졌다.

## sealed의 문법 — 세 단어로 충분하다

자, 결제 상태 모델을 sealed로 다시 적자. records와 짝지어서.

```java
public sealed interface PaymentResult
    permits PaymentResult.Approved,
            PaymentResult.Declined,
            PaymentResult.Pending {

    record Approved(Instant approvedAt, String issuerCode) implements PaymentResult {}
    record Declined(String reasonCode, boolean retryable) implements PaymentResult {}
    record Pending(URI authenticationUrl, Instant expiresAt) implements PaymentResult {}
}
```

위 Visitor 패턴의 50줄이 이 코드 9줄로 압축됐다. 그리고 같은 보증을 *언어 차원에서* 받는다.

세 단어를 짚자. `sealed`, `permits`, `non-sealed`. 그리고 `sealed`의 sub-type이 가져야 하는 세 선택지 — `final`, `sealed`, `non-sealed`.

**`sealed`** — 이 타입을 *상속·구현할 수 있는 후보를 제한*한다는 선언이다. 인터페이스에도 클래스에도 붙는다.

**`permits`** — 그 후보들을 *이름으로 명시*한다. 위 코드에서는 `Approved`, `Declined`, `Pending` 세 record가 후보다.

**`permits` 생략 가능 조건** — 같은 컴파일 단위(같은 `.java` 파일) 안에 sub-type이 모두 있으면 `permits` 절을 생략할 수 있다. 컴파일러가 같은 파일 안의 sub-type을 찾아 자동으로 채운다. 위 코드는 한 파일에 다 들어 있으므로 사실 `permits` 절을 지워도 동작한다. 다만 *명시성*을 위해 적어두는 편이 낫다 — sealed의 가치가 "닫힘이 명시적이다"라는 점에 있으므로, `permits`를 적는 것이 그 명시성을 살린다.

**sub-type의 세 선택지** — `permits`된 sub-type은 *반드시* 세 키워드 중 하나로 자신의 *연속·종결*을 선언해야 한다.

- `final` — 더 이상 상속되지 않는다. records는 자동으로 final이다.
- `sealed` — 이 sub-type도 다시 sealed. 자신의 `permits`를 다시 가진다.
- `non-sealed` — 이 sub-type부터는 *상속이 다시 열린다*. 봉인이 한 번 깨진다.

`non-sealed`의 의미를 한 번 더 짚자. sealed 계층의 끝에서 *기존 코드와의 호환*을 위해 봉인을 풀어야 할 자리가 종종 있다. 예를 들어 외부 라이브러리가 우리의 어떤 인터페이스를 자유롭게 구현하도록 허용하고 싶을 때. `non-sealed`는 그 *명시적 출구*다. 봉인의 닫힘이 *전체 다*는 아니라는 표현이다.

**같은 모듈, 같은 패키지 제약** — 자바 17의 sealed는 sub-type이 *같은 모듈 안*에 있어야 한다. 모듈을 쓰지 않는 경우(unnamed module)에는 *같은 패키지 안*. 이 제약이 뜻하는 바는 분명하다. "*우리 도메인의 경계 안에서만* 닫힘이 유효하다." 외부 코드가 `permits` 목록에 끼어드는 일은 컴파일러가 막아준다. 도입부에서 우려한 *외부 오염*의 가능성이 닫혔다.

> **JLS 인용 박스 — §8.1.1.2 sealed, permits**
>
> *원문* — "A `sealed` class restricts which other classes or interfaces may directly extend it. ... A class which is declared `sealed` must have either a `permits` clause or have all of its permitted direct subclasses declared in the same compilation unit."
>
> *번역* — "`sealed` 클래스는 *어떤 다른 클래스나 인터페이스가 자신을 직접 확장할 수 있는지를 제한한다*. (…) `sealed`로 선언된 클래스는 `permits` 절을 가지거나, *허용된 모든 직접 sub-class가 같은 컴파일 단위 안에서 선언되어야* 한다."
>
> *해설* — 핵심 단어는 *directly extend*. sealed의 닫힘은 *직접 sub-type 수준*에서 강제되는 닫힘이다. 그리고 `permits`된 sub-type이 다시 `non-sealed`라면, 그 아래로는 닫힘이 풀린다. 즉 sealed는 *완전한 잠금*이 아니라 *명시된 닫힘*이다. 닫힘과 열림을 *각 레이어에서 선언하는* 도구로 이해하자.
>
> *본문 연결* — `PaymentResult`가 `Approved`, `Declined`, `Pending` 셋만 허용한다는 보증이 이 문장에서 나온다. 새로운 결제 상태가 사업적으로 등장한다면, 그 추가는 *우리 도메인 내부의 명시적 결정*으로만 일어난다. 외부 라이브러리가 우리 모르게 새 sub-type을 끼워 넣을 길이 없다.

## 이것은 *합 타입*이다 — 다른 언어에서는 어떻게 부르나

sealed classes의 자바스러운 이름은 그렇게 정해졌다. 하지만 이 개념의 본명은 다른 곳에 있다. *합 타입(sum type)*. 함수형 언어들이 30년 동안 다뤄온 그 개념이다. 짧게 옆 언어들을 둘러보자.

**Haskell:**

```haskell
data PaymentResult
    = Approved UTCTime String
    | Declined String Bool
    | Pending URI UTCTime
```

`|`를 *또는*으로 읽자. `PaymentResult`는 *Approved이거나, Declined이거나, Pending이다*. 정확히 셋 중 하나다. 새 sub-type을 끼워 넣으려면 `data` 선언을 *명시적으로 수정*해야 한다. 자바의 sealed가 받아온 그 보증이다.

**Scala:**

```scala
sealed trait PaymentResult
final case class Approved(approvedAt: Instant, issuerCode: String) extends PaymentResult
final case class Declined(reasonCode: String, retryable: Boolean) extends PaymentResult
final case class Pending(authenticationUrl: URI, expiresAt: Instant) extends PaymentResult
```

문법이 자바의 sealed + record와 거의 같다. 그렇다 — *자바가 Scala를 따른 것이다*. 정확히는 ML·Haskell 계보를 Scala가 JVM 위에 올렸고, 자바가 다시 그 계보를 자기 어휘로 받아들였다.

**Kotlin:**

```kotlin
sealed class PaymentResult {
    data class Approved(val approvedAt: Instant, val issuerCode: String) : PaymentResult()
    data class Declined(val reasonCode: String, val retryable: Boolean) : PaymentResult()
    data class Pending(val authenticationUrl: URI, val expiresAt: Instant) : PaymentResult()
}
```

마찬가지다. Kotlin은 같은 도구를 자바보다 먼저(2017) 가졌고, 안드로이드 진영에서는 *데이터 클래스 + 봉인 클래스*가 사실상의 표준 도메인 모델링 도구다.

**Rust:**

```rust
enum PaymentResult {
    Approved { approved_at: Instant, issuer_code: String },
    Declined { reason_code: String, retryable: bool },
    Pending { authentication_url: Url, expires_at: Instant },
}
```

Rust는 자기 `enum` 키워드 안에 합 타입을 그대로 욱여넣었다. 자바의 enum과 *이름이 같을 뿐 다른 개념*이다 — Rust의 enum이 자바의 sealed에 해당한다. 이 점이 처음 두 언어를 오갈 때 가장 혼란스러운 자리다.

자, 다섯 언어를 둘러봤다. 모두 같은 한 가지를 표현한다. **합 타입은 닫힌 대안의 집합이다.** 그리고 그 닫힘이 *컴파일러에 의해 강제*된다. 자바가 마침내 그 문법을 자기 어휘로 받아들였다는 사실이 데이터지향 자바의 정체성을 결정짓는다.

Brian Goetz가 *Data-Oriented Programming in Java*에서 한 표현이 이 자리를 잘 정리한다. "We need products (records) and we need sums (sealed)." 곱과 합. *records는 컴포넌트의 곱, sealed는 sub-type의 합*. 두 도구가 함께 와야 ADT(algebraic data types)가 완성된다. 그래서 두 도구는 *짝패*다 — 한쪽만 들이는 일은 절반의 도입이다.

## Visitor와 sealed의 코드 길이 — 실측 비교

말로만 비교하지 말고, 같은 한 가지 일을 두 방식으로 적어 길이를 재보자. 결제 결과를 받아 *사용자에게 보여줄 메시지*와 *감사 로그에 기록할 한 줄*과 *후속 액션이 자동 재시도인지*를 각각 결정하는 일이다.

**Visitor 패턴으로 적은 코드:**

```java
public abstract class PaymentResult {
    public abstract <R> R accept(Visitor<R> visitor);
    public interface Visitor<R> {
        R visitApproved(Approved a);
        R visitDeclined(Declined d);
        R visitPending(Pending p);
    }
    public static final class Approved extends PaymentResult { /* ... 12줄 ... */ }
    public static final class Declined extends PaymentResult { /* ... 12줄 ... */ }
    public static final class Pending extends PaymentResult { /* ... 12줄 ... */ }
}

// 세 가지 결정을 위해 Visitor 인스턴스를 세 개 만들어야 한다
String userMessage = result.accept(new PaymentResult.Visitor<String>() {
    @Override public String visitApproved(Approved a) { return "결제 완료"; }
    @Override public String visitDeclined(Declined d) {
        return d.retryable() ? "재시도 가능한 실패" : "재시도 불가";
    }
    @Override public String visitPending(Pending p) { return "인증이 필요합니다"; }
});

String auditLog = result.accept(new PaymentResult.Visitor<String>() {
    @Override public String visitApproved(Approved a) { return "APPROVED " + a.issuerCode(); }
    @Override public String visitDeclined(Declined d) { return "DECLINED " + d.reasonCode(); }
    @Override public String visitPending(Pending p) { return "PENDING " + p.expiresAt(); }
});

boolean autoRetry = result.accept(new PaymentResult.Visitor<Boolean>() {
    @Override public Boolean visitApproved(Approved a) { return false; }
    @Override public Boolean visitDeclined(Declined d) { return d.retryable(); }
    @Override public Boolean visitPending(Pending p) { return false; }
});
```

타입 선언과 세 호출을 모두 합치면 *80줄 가까이* 된다. 매 호출마다 익명 클래스 한 덩어리가 등장하는 *지긋지긋함*이 본문에 그대로 드러난다.

**sealed + record + pattern matching으로 적은 코드:**

```java
public sealed interface PaymentResult {
    record Approved(Instant approvedAt, String issuerCode) implements PaymentResult {}
    record Declined(String reasonCode, boolean retryable) implements PaymentResult {}
    record Pending(URI authenticationUrl, Instant expiresAt) implements PaymentResult {}
}

String userMessage = switch (result) {
    case Approved a -> "결제 완료";
    case Declined(var reason, var retryable) -> retryable ? "재시도 가능한 실패" : "재시도 불가";
    case Pending p -> "인증이 필요합니다";
};

String auditLog = switch (result) {
    case Approved(var at, var issuer) -> "APPROVED " + issuer;
    case Declined(var reason, var retry) -> "DECLINED " + reason;
    case Pending(var url, var expires) -> "PENDING " + expires;
};

boolean autoRetry = switch (result) {
    case Approved a -> false;
    case Declined d -> d.retryable();
    case Pending p -> false;
};
```

*25줄 안쪽*이다. 그러면서 컴파일러의 완전성 검사는 정확히 같다 — 새 sub-type을 추가하면 *세 switch 모두*가 컴파일 에러로 갱신을 요구한다. Visitor가 100% 같은 보증을 *80줄로* 사주던 일을, sealed + pattern은 *25줄로* 사준다.

이 차이가 어디서 오는가? 본질적으로는 *분기를 객체화할 필요가 없어졌다*는 데서 온다. Visitor의 정체는 "switch가 없으니 그것을 객체로 모사한다"였다. 자바에 *데이터 분해를 아는 switch*가 들어오자, 그 모사가 불필요해진 것이다. 다음 장의 주인공이 바로 그 *데이터 분해를 아는 switch* — pattern matching이다.

## enum + sealed — 함께 쓰면 더 좋은 자리

여기까지 보면 "enum은 사망 선고인가?"라는 인상을 받을 수 있다. 그렇지 않다. enum은 *상태가 고정 상수이고, 각 상수가 같은 모양의 데이터를 가진다*는 *그* 자리에서는 여전히 가장 자연스럽다. 결제 *방법*(`CREDIT_CARD`, `BANK_TRANSFER`, `KAKAO_PAY`)은 enum이 어울린다. 결제 *결과*(`Approved`, `Declined`, `Pending`)는 sealed가 어울린다. 자리가 다르다.

오히려 두 도구를 *함께 쓰면* 더 좋아진다.

```java
public sealed interface PaymentResult {
    record Approved(Instant approvedAt, String issuerCode, PaymentMethod method)
        implements PaymentResult {}
    record Declined(String reasonCode, boolean retryable, PaymentMethod method)
        implements PaymentResult {}
    record Pending(URI authenticationUrl, Instant expiresAt, PaymentMethod method)
        implements PaymentResult {}
}

public enum PaymentMethod {
    CREDIT_CARD, BANK_TRANSFER, KAKAO_PAY, TOSS_PAY
}
```

각 결과 안에 *어떤 결제 방법으로 처리됐는지*를 enum으로 끼워 넣는다. 합 타입 안에 *고정 상수의 곱*이 들어간 모양이다. 두 도구가 서로의 자리를 잠식하지 않는다는 것이 보인다.

## Spring 도메인 이벤트에서의 sealed

sealed가 빛나는 또 하나의 자리가 Spring의 도메인 이벤트다. `ApplicationEventPublisher`로 이벤트를 발행할 때, 이벤트 타입을 sealed로 닫아두면 *수신자 측이 exhaustive 분기*를 쓸 수 있다.

```java
public sealed interface UserEvent {
    record Created(String userId, Instant createdAt) implements UserEvent {}
    record Updated(String userId, Set<String> changedFields, Instant updatedAt) implements UserEvent {}
    record Deleted(String userId, Instant deletedAt) implements UserEvent {}
}

@Component
public class UserEventListener {
    @EventListener
    public void on(UserEvent event) {
        switch (event) {
            case UserEvent.Created c -> handleCreated(c);
            case UserEvent.Updated u -> handleUpdated(u);
            case UserEvent.Deleted d -> handleDeleted(d);
        }
    }
}
```

새 이벤트 타입 — 예를 들어 `Suspended` — 가 sealed에 추가되는 순간, 위 listener의 switch가 *컴파일 에러*로 갱신을 요구한다. 도메인이 자라면서 "어떤 이벤트 핸들러가 갱신을 빠뜨렸는지"를 *컴파일 시점에 잡아주는* 안전망이다. enum + `if`/`else` 분기로는 결코 받을 수 없었던 *컴파일러의 보증*이다.

Spring Cloud Stream이나 Kafka로 이벤트를 *직렬화*해 전송할 때도 sealed가 유용하다. Jackson의 `@JsonTypeInfo` + `@JsonSubTypes`로 polymorphic 직렬화를 적던 자리에, sealed의 `permits` 목록이 *그 SubTypes 목록을 코드로* 갈음한다. Jackson 2.16부터는 sealed 인터페이스에 대해 polymorphic deserialization을 자동 추론해주는 기능이 들어왔다 — `permits` 목록을 그대로 SubTypes로 본다. *언어와 라이브러리의 합의*가 자라고 있다는 신호다.

## 13장으로 가는 다리

여기까지 정리하면 sealed가 무엇이고 왜 들어왔는지가 손에 잡힌다. 그런데 한 가지 어색한 점이 남는다. 위 코드의 switch가 *어떻게 records를 분해하는지*를 우리는 아직 설명하지 않았다.

```java
case Declined(var reason, var retryable) -> retryable ? "재시도 가능" : "재시도 불가";
```

이 한 줄에서 `Declined`라는 sub-type을 *매칭*하고, 동시에 그 컴포넌트 두 개를 `reason`과 `retryable`이라는 이름으로 *분해*했다. 두 가지 일이 동시에 일어났다. *타입 매칭 + 컴포넌트 분해*가 한 줄에 담긴 이 능력이 13장의 주인공 — *pattern matching* 이다.

records가 product, sealed가 sum, pattern matching이 분해기. 이 셋이 함께 와야 비로소 ADT가 *언어 차원에서* 완성된다. 다음 장에서 캐스트 사다리 9단을 한 화면에 펼쳐놓고, 그 사다리가 pattern matching으로 어떻게 *한 줄로 무너지는지*를 함께 보자. 그리고 Brian Goetz가 *Data-Oriented Programming*이라는 단어로 한 묶음으로 부른 이 셋이 *현실 도메인에서* 어떻게 풀려 들어오는지를 — 표현식 평가기, HTTP Result, Workflow 상태기계 세 가지 본격 예제로 — 한 자리에 모아보자.

기억해두자. sealed는 *닫힘을 명시적으로 선언하는 도구*다. 닫힘이 명시적이라는 것은, *언어가 우리 도메인의 경계를 알게 됐다*는 뜻이다. 컴파일러가 그 경계를 들고 있는 한, 우리는 분기를 빠뜨릴 수 없다. 그 작은 보증이 큰 자유를 준다.
