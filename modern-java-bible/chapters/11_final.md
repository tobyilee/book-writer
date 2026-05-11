# 11장. Records — 자바가 마침내 인정한 "데이터의 신원"

옆자리 동료가 한숨을 쉬며 IDE를 노려보고 있다고 해보자. 어제는 신이 나서 자랑하던 사람이었다. "이번에 Spring Boot 3.4로 올리면서 DTO를 전부 record로 옮겼다"고. `OrderRequest`, `OrderResponse`, `OrderEvent` 세 개를 한 시간 만에 갈아치우면서 코드 줄 수가 70%로 줄었다고. 그런데 오늘은 표정이 영 좋지 않다. 무슨 일이냐고 물으니, "JPA Entity도 record로 옮기려다가 두 시간을 날렸다"고 답한다.

`Order` 엔티티에 `@Entity` 어노테이션을 붙이고 `record Order(Long id, String status, ...)` 라고 적어보았더니, Hibernate가 `InstantiationException`을 던지더라는 것이다. no-args constructor가 없다고. 그래서 canonical constructor를 비워서 시도해봤더니, 이번엔 `final field`라서 proxy를 못 만든다고 한다. lazy loading은 어떻게 하느냐고 묻기 시작했을 때, 동료는 결국 record 선언을 지우고 클래스로 되돌리고 있었다.

이쯤 되면 한 번쯤 고민하게 된다. **Records는 도대체 Lombok의 *대체*인가, 아니면 다른 무엇인가?** 같은 것을 더 짧게 적을 수 있다면 그건 그저 문법 설탕에 불과할 텐데, 어떤 자리에서는 되고 어떤 자리에서는 안 된다면 그건 단순한 설탕이 아니다. 의도가 따로 있다는 뜻이다. 그 의도를 짚어보지 않고 코드만 옮기면, 위 동료처럼 두 시간을 날린다.

이 장에서는 record라는 작은 문법 뒤에 숨어 있는 "데이터의 신원(identity)"이라는 큰 이야기를 풀어보자. Brian Goetz가 records를 두고 했던 표현을 빌리면, 이것은 Lombok이라는 "패치"가 아니라 자바가 마침내 "데이터 캐리어를 언어 차원에서 인정한 선언"이다. 무슨 뜻인지, 그리고 그것이 우리 실무 코드에 어떻게 풀려 들어오는지를 함께 살펴보자.

## records가 14에서 preview, 16에서 표준이 된 이유

먼저 작은 진화 박스 하나로 시작하자. Records는 Java 14에 preview로 도입(JEP 359)되어, 15에서 second preview(JEP 384)를 거쳐, 16에서 표준(JEP 395)이 됐다. 이 짧은 흐름이 뜻하는 바를 생각해보자.

> **진화 박스 — Records 표준화 연표**
>
> - **Java 14 (2020-03)** — JEP 359 First Preview. 컴포넌트, canonical constructor, accessor 자동 생성, `equals`/`hashCode`/`toString` 자동의 골격이 처음 모습을 드러낸다.
> - **Java 15 (2020-09)** — JEP 384 Second Preview. 컴팩트 생성자에서 instance 필드 직접 대입 금지가 명확해진다. 로컬 record 허용. 어노테이션 처리에 미세 조정.
> - **Java 16 (2021-03)** — JEP 395 Standard. 1년 만에 표준화. inner class에서의 static member 허용 같은 부수 조항까지 정리.

자바답지 않게 빠르다. 그 자바답지 않은 속도가 무엇을 말하는가? 두 가지를 말한다. 하나는, OpenJDK가 preview라는 단계를 가지면서 *산업 피드백을 받아 다듬는 절차*를 본격적으로 가동하기 시작했다는 점이다. 또 하나는, records가 "데이터 캐리어"라는 *해묵은 요구*에 대한 응답이었다는 점이다. 자바 8 이래 Lombok이 압도적인 점유율로 답하고 있던 그 자리를, 자바가 마침내 언어 차원에서 받아내기 시작한 것이다.

물론 일부 비판도 있다. "5개 LTS를 가로지르며 preview가 돌았다, 너무 빠르다"는 시각이다. 하지만 records의 도입 후 부작용을 보면 그 빠름이 *경솔함*은 아니었다는 사실을 인정하게 된다. preview의 의미가 바로 그것이다 — 산업이 직접 만져보고 흠을 찾아낸 뒤에 표준에 들이는 일. 잊지 말자, 자바는 preview를 단계로 갖춘 첫 메이저 언어다.

## OrderRequest를 record로 옮겨보자

말로만 하면 추상적이니, 손에 잡히는 코드로 옮기자. 주문 시스템의 DTO 세 개 — `OrderRequest`, `OrderResponse`, `OrderEvent` — 를 record로 적어보자.

Lombok 시절의 코드는 이랬다.

```java
@Value
@Builder
public class OrderRequest {
    String customerId;
    List<OrderLine> lines;
    String couponCode;
}
```

`@Value`가 final 클래스 + final 필드 + getter + `equals`/`hashCode`/`toString`을 모두 만들어주었다. `@Builder`가 builder 패턴을 만들어주었다. 코드 다섯 줄로 의도를 압축했고, 그 의도는 "불변 데이터 캐리어"였다.

같은 의도를 record로 옮기면 이렇게 된다.

```java
public record OrderRequest(
    String customerId,
    List<OrderLine> lines,
    String couponCode
) {}
```

한 줄로 본문이 끝났다. record header에 적힌 세 개의 컴포넌트가 곧 필드이자 accessor의 시그니처다. `customerId()`, `lines()`, `couponCode()`가 자동으로 만들어지고, `equals`·`hashCode`·`toString` 세 메서드도 자동이다. `@Value`가 어노테이션 프로세서로 *외부에서* 메우던 일을, 컴파일러가 *언어 차원에서* 해준다.

그 차이가 정말 크다. 어노테이션 프로세서는 IDE마다 인지 정도가 달라서, IntelliJ가 잠시 캐시를 잃으면 빨간 줄이 가득 차는 일이 흔했다. records는 그 자체로 언어다. 컴파일러가 알고, IDE가 알고, 리플렉션·직렬화 라이브러리가 모두 안다. "외부 어노테이션 프로세서에 의존하지 않는다"는 한 줄이 실무에서 얼마나 후련한지, Lombok과 한 번이라도 씨름해본 사람은 안다.

응답과 이벤트도 같은 방식으로 적자.

```java
public record OrderResponse(
    String orderId,
    String status,
    BigDecimal totalAmount,
    Instant createdAt
) {}

public record OrderEvent(
    String orderId,
    OrderEventType type,
    Instant occurredAt
) {}
```

세 DTO를 한 화면에 담아도 모자라지 않다. 코드의 의도가 *데이터*임을 한눈에 알 수 있다. 그리고 더 중요한 사실은, 이제 *이 의도를 컴파일러가 보증한다*는 점이다. 누군가 실수로 `record`에 mutable field나 setter를 넣으려고 하면 컴파일이 막힌다. Lombok 시절에는 `@Value` 옆에 `@Setter`를 같이 붙이는 *찜찜한 코드*를 종종 보았지만, record는 그 경로 자체가 닫혀 있다.

## 자동 생성되는 네 가지, 그리고 직접 손대고 싶을 때

record가 자동으로 만들어주는 것은 정확히 네 가지다.

첫째, **컴포넌트마다 private final 필드와 그에 대응하는 accessor 메서드** — `customerId` 컴포넌트가 있다면 `customerId()`라는 메서드가 자동이다. getter가 아니라 *accessor*다. `get` 접두사가 붙지 않는다는 점에 주의하자. JavaBean 규약을 따르지 않는 작은 선언인데, 그 선언이 뜻하는 바가 작지 않다. record는 "캡슐화된 객체"가 아니라 "*투명한* 데이터 캐리어"라는 입장 표명이다. Jackson과 Spring이 이를 인지해서, 굳이 `@JsonProperty`를 일일이 붙이지 않아도 직렬화가 자연스럽다.

둘째, **canonical constructor** — 컴포넌트 순서대로 받는 생성자. `new OrderRequest("cust-1", lines, "SUMMER10")` 식으로 호출된다.

셋째, **`equals`와 `hashCode`** — 컴포넌트 기반으로 계산된다. 두 record 인스턴스가 *값으로* 같으면 같다고 판단한다. 이 점이 record의 신원을 단적으로 드러낸다. 객체의 신원은 *주소*가 아니라 *값*에 있다.

넷째, **`toString`** — `OrderRequest[customerId=cust-1, lines=..., couponCode=SUMMER10]` 형식. 디버깅에 그대로 쓸 만하다.

이 자동 생성이 마음에 안 들 때는 어떻게 해야 할까? 두 가지 길이 있다.

하나는 **compact constructor**다. canonical constructor의 본문만 적되, 파라미터 목록은 생략하는 형태다. 보통 validation에 쓴다.

```java
public record OrderRequest(
    String customerId,
    List<OrderLine> lines,
    String couponCode
) {
    public OrderRequest {
        if (customerId == null || customerId.isBlank()) {
            throw new IllegalArgumentException("customerId required");
        }
        if (lines == null || lines.isEmpty()) {
            throw new IllegalArgumentException("at least one line required");
        }
        lines = List.copyOf(lines);  // 방어적 복사
    }
}
```

여기서 한 가지 놓치지 말아야 할 점이 있다. compact constructor 안에서 `this.lines = lines` 식으로 *명시적 대입을 할 수 없다*. 컴파일러가 그 일을 마지막에 자동으로 해준다. 다만 *파라미터를 재할당*하는 것은 가능하다. 위 코드에서 `lines = List.copyOf(lines)`를 하면, 컴파일러가 마지막에 그 재할당된 값을 필드에 넣어준다. 작은 차이 같지만, 방어적 복사를 단 한 줄로 끝낼 수 있다는 점에서 실무적으로 큰 차이다.

또 하나는 **explicit canonical constructor**다. 컴팩트 형식 대신 파라미터 목록을 모두 다 적은 정통 생성자. 이 경우는 마지막에 모든 필드를 자기 손으로 대입해야 한다. 컴팩트가 자연스럽지 않은 경우에만 쓰자.

## Records가 안 되는 것

이 자리에서 솔직히 말하자. record로 *모든 것을 옮기려*는 시도는 거의 항상 좌절로 끝난다. record가 안 되는 것들을 분명히 짚어두자.

**상속이 안 된다.** record는 암묵적으로 `final`이며, 자동으로 `java.lang.Record`를 상속한다. 그 외의 클래스를 `extends` 할 수 없다. 다른 클래스가 record를 `extends`할 수도 없다. 인터페이스 `implements`는 가능하다 — `OrderEvent implements DomainEvent` 같은 식. 이 점이 13장에서 다룰 sealed 패턴과 만나면 강력해진다.

**가변 상태가 안 된다.** 모든 컴포넌트는 `private final` 필드로 고정된다. setter가 없고, 추가 instance 필드를 선언할 수도 없다. 컴팩트 생성자에서 방어적 복사를 해도, 컴포넌트가 가리키는 *대상*까지 불변이 되는 것은 아니다. 그래서 `List<OrderLine>` 같은 컴포넌트는 `List.copyOf`로 막는 편이 안전하다.

**그리고 JPA Entity가 안 된다.** 도입부 동료가 겪은 바로 그 좌절이다. JPA의 `@Entity`는 (1) no-args constructor를 요구하고, (2) `final` 클래스를 받아주지 않으며, (3) lazy loading을 위해 proxy로 감싸는데 final field로는 그 proxy가 만들어지지 않는다. record의 모든 자동화가 정확히 JPA의 요구를 거부한다. 같은 단어를 두 개의 패러다임이 정반대 방향으로 쓰는 셈이다.

여기서 *난감해*하지 않으려면, record와 Entity를 *동의어로 보지 않는 정신적 습관*이 필요하다. record는 "투명한 데이터 캐리어"이고 Entity는 "JPA 영속성 컨텍스트가 관리하는 식별자 보유체"다. 의도가 다르다.

> **JLS 인용 박스 — §8.10 Record Classes**
>
> *원문* — "A record class is a special kind of class that acts as a transparent carrier for shallowly immutable data. The components of a record class declaration are the variables that comprise its state."
>
> *번역* — "record 클래스는 *얕은 불변* 데이터를 위한 *투명한 캐리어*로 동작하는, 특수한 종류의 클래스다. record 클래스 선언의 컴포넌트들이 그 상태를 구성하는 변수다."
>
> *해설* — 핵심 단어 두 개를 음미하자. 하나는 *transparent*. record는 자신이 가진 데이터를 *숨기지 않는다*. accessor가 자동이고, `toString`이 자동이고, 외부에서 컴포넌트의 신원을 완전히 들여다볼 수 있다. 객체지향이 줄곧 강조해온 "캡슐화"의 반대편 입장이다. 다른 하나는 *shallowly immutable*. 컴포넌트 자체는 final이지만, 컴포넌트가 가리키는 *내부 객체*까지 강제로 불변이 되지는 않는다. 그래서 `List<OrderLine>`을 컴포넌트로 가지면, 그 리스트의 내용은 변경 가능할 수 있다는 점을 의식해두자.
>
> *본문 연결* — 위 compact constructor에서 `List.copyOf`로 방어적 복사를 한 이유가 여기에 있다. JLS가 "얕은 불변"이라고 명시한 그 한계를 우리가 본문에서 보강하는 것이다.

## Java 23이 풀어준 한 가지 — Flexible Constructor Bodies

records를 본격적으로 쓰다 보면, 또 하나의 작은 답답함을 만난다. 생성자에서 `super()`나 `this()` 호출은 *반드시 첫 줄*이어야 한다는 30년 묵은 규칙이다. records 자체는 `Record`를 자동으로 상속하니 큰 문제 없어 보이지만, 일반 클래스나 record의 컴팩트 생성자에서 *유도된 값으로 super를 호출하고 싶을 때* 그 규칙이 발목을 잡았다.

이 답답함을 푸는 것이 **JEP 482 (Java 23 preview)** → **JEP 513 (Java 25 표준)** Flexible Constructor Bodies다. 이제는 `super()` 또는 `this()` 호출 이전에도 *검증·계산·로깅* 같은 코드가 들어갈 수 있다. 단, 그 prologue 안에서는 *해당 인스턴스의 필드나 메서드에 접근할 수 없다*. 아직 객체가 만들어지기 전이므로.

```java
public class ValidatedAmount {
    private final BigDecimal value;

    public ValidatedAmount(BigDecimal raw) {
        if (raw == null || raw.signum() < 0) {
            throw new IllegalArgumentException("non-negative required");
        }
        var normalized = raw.setScale(2, RoundingMode.HALF_UP);
        super();   // ← 이제 첫 줄이 아니어도 된다
        this.value = normalized;
    }
}
```

작은 변화로 보이지만, records의 compact constructor와 결합되면 더 자연스러워진다. compact constructor 안에서 *파라미터를 정규화한 후*에 super-like 호출을 끼울 일은 record에서는 거의 없지만, 이 룰의 종말은 자바 전체 코드 스타일에 천천히 스며들 변화다. *언어가 자기 안의 묵은 제약을 풀어주는 신호*로 기억해두자.

## Records vs Lombok — 신원의 문제

자, 이제 본격적인 논쟁으로 들어가자. records가 Lombok을 대체하는가? Brian Goetz가 한 인터뷰에서 이 질문을 받았을 때 그가 한 답이 인상적이다.

> "Records aren't there to replace Lombok. Records are there because Java has finally decided that data carriers deserve to be a first-class concept in the language."
>
> "Records가 Lombok을 대체하려고 등장한 것이 아니다. Records는 *데이터 캐리어가 언어의 일급 개념으로 인정받을 자격이 있다*고 자바가 마침내 결정했기 때문에 등장한 것이다."

이 문장을 두 번 읽자. Goetz의 입장은 명료하다. Lombok은 "자바가 부족해서 외부 어노테이션 프로세서로 메우던 *패치*"였다. records는 "자바가 자신의 어휘로 데이터 캐리어를 인정한 *신원* 표명"이다. 둘은 의도가 다르고, 그 결과 잘 맞는 자리가 다르다.

실무 정착의 방향을 정리하면 이렇다.

**records가 잘 맞는 자리:** DTO, command, event, value object, projection 결과, `@ConfigurationProperties` 바인딩 대상. 한마디로 *불변, 캡슐화 없음, 컴포넌트 동등성으로 의미가 결정되는 모든 자리*다.

**Lombok이 여전히 자기 자리를 지키는 곳:**

- **`@Slf4j`** — record에는 logger를 둘 instance 필드를 추가할 수 없다. 정적 logger 도입을 위한 한 줄짜리 어노테이션은 record와 무관하게 계속 유용하다.
- **`@SneakyThrows`** — checked exception을 unchecked로 감춰주는 도구. 미학적 호불호는 있지만, 인프라성 코드에서는 여전히 쓰임이 있다.
- **`@Accessors(chain = true)` / `@Builder`** — mutable POJO에서 fluent setter나 builder가 필요한 경우. record는 builder를 자동으로 만들어주지 않는다(요청은 끊임없이 올라오지만, OpenJDK 측은 신중하다).
- **JPA Entity** — 위에서 짚었다. record가 안 되는 자리.

그래서 실무 합의는 명확하다. **"DTO와 Value Object는 records, Entity와 mutable 도메인 객체는 Lombok 클래스"**. 이 두 영역이 서로 자리를 다투지 않는다는 점을 기억해두면, "record로 모든 것을 옮기려다 좌절하는 일"을 피할 수 있다.

물론 *Lombok을 점점 줄여가는 것*은 바람직하다. 어노테이션 프로세서에 의존하는 것은 그 자체로 외부 의존성이고, JDK가 진화할 때마다 호환성 이슈를 일으킨다(Lombok 1.18.22 미만은 Java 17과 잘 맞지 않았던 경험을 다들 기억할 것이다). 그러나 "Lombok을 한순간에 걷어내자"는 시도는 *지긋지긋한 작업*이 될 가능성이 높다. records가 잘 맞는 자리부터 차근히 옮기는 편이 낫다.

## 직렬화 — Jackson, JPA AttributeConverter, ConfigurationProperties

records를 DTO로 쓰겠다고 마음먹는 순간, 가장 먼저 마주치는 실무 질문은 직렬화다. JSON으로 어떻게 변환되는가? Spring `@ConfigurationProperties`에 어떻게 바인딩되는가? JPA 컨버터와 어떻게 어울리는가?

**Jackson은 records를 잘 안다.** Jackson 2.12 이상부터 records가 일급 시민이다. 별도 모듈 없이 직렬화·역직렬화가 동작한다. 다만 한 가지 작은 *주의*가 있다 — record의 accessor는 `get` 접두사가 없으므로, Jackson의 기본 introspection이 컴포넌트 이름을 직접 본다. 그래서 JSON 필드명을 컴포넌트 이름과 다르게 쓰고 싶다면 `@JsonProperty`를 컴포넌트 위에 직접 붙이거나, record header에 어노테이션을 적어야 한다.

```java
public record OrderRequest(
    @JsonProperty("customer_id") String customerId,
    List<OrderLine> lines,
    @JsonProperty("coupon_code") String couponCode
) {}
```

snake_case 컨벤션과 camelCase 자바 컴포넌트를 잇는 정도면 이 정도 표시로 충분하다. 더 큰 변환이 필요하다면 `@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)`를 클래스 레벨로 한 번 적어두자.

**Spring `@ConfigurationProperties`도 records와 자연스럽다.** 정확히는 Spring Boot 2.4 이후 *constructor binding*이 도입되면서부터다. `@ConstructorBinding`을 record header에 붙이지 않아도 된다 — Spring이 자동으로 canonical constructor를 통해 바인딩한다.

```java
@ConfigurationProperties(prefix = "order")
public record OrderProperties(
    Duration timeout,
    int retryCount,
    List<String> allowedChannels
) {}
```

`application.yml`의 `order.timeout=PT5S`, `order.retry-count=3` 같은 설정이 그대로 들어온다. 컴포넌트가 final이고 setter가 없으므로, 누구도 런타임에 설정을 *몰래 바꿀 수* 없다. 설정은 불변이라는 원칙을 *언어가 보증해주는* 셈이다. 이것이 records를 설정에 쓰는 가장 큰 이유다.

**JPA `AttributeConverter`에 record를 쓰는 일.** record를 column 한 칸에 JSON으로 넣어두는 패턴이다. `@Convert(converter = OrderMetadataConverter.class)`를 Entity 필드에 붙이고, `AttributeConverter<OrderMetadata, String>`이 Jackson을 통해 직렬화·역직렬화하는 식이다. 이때 record는 *값 자체로* 다뤄지고, JPA의 영속성 컨텍스트가 그 컴포넌트 단위로 dirty checking을 하지는 않는다. 그래서 *불변 값 묶음*에는 자연스럽고, 부분 수정이 잦은 데이터에는 부적합하다. 잊지 말자.

**Spring Data의 projection.** 인터페이스 기반 projection을 써본 사람이라면 "동적 proxy로 만들어지는 그 객체가 어색하다"는 인상을 받았을 것이다. record projection은 그 어색함을 깔끔히 푼다.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("""
        SELECT new com.example.OrderSummary(o.id, o.status, o.totalAmount)
        FROM Order o
        WHERE o.customerId = :customerId
    """)
    List<OrderSummary> findSummariesByCustomer(String customerId);
}

public record OrderSummary(Long id, String status, BigDecimal totalAmount) {}
```

JPQL의 `new` 절이 record의 canonical constructor를 그대로 호출한다. 결과는 *값으로 결정되는* record 인스턴스의 리스트다. 인터페이스 proxy의 어색함이 사라지고, 콜링 사이트에서는 그저 record를 쓰듯이 다루면 된다.

## Java 8과 Java 21 — DTO 한 개의 변천사

이 장의 마지막에, 같은 의도를 가진 *한 개의 DTO가* 11년 사이에 어떻게 변했는지를 한 화면에 담아보자. 이 비교가 records의 가치를 가장 정직하게 보여준다.

**Java 8 시절, Lombok 없이 적은 코드:**

```java
public final class OrderRequest {
    private final String customerId;
    private final List<OrderLine> lines;
    private final String couponCode;

    public OrderRequest(String customerId, List<OrderLine> lines, String couponCode) {
        this.customerId = customerId;
        this.lines = lines == null ? List.of() : List.copyOf(lines);
        this.couponCode = couponCode;
    }

    public String getCustomerId() { return customerId; }
    public List<OrderLine> getLines() { return lines; }
    public String getCouponCode() { return couponCode; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderRequest other)) return false;
        return Objects.equals(customerId, other.customerId)
            && Objects.equals(lines, other.lines)
            && Objects.equals(couponCode, other.couponCode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(customerId, lines, couponCode);
    }

    @Override
    public String toString() {
        return "OrderRequest{customerId=" + customerId
            + ", lines=" + lines + ", couponCode=" + couponCode + "}";
    }
}
```

35줄에 가까운 boilerplate. 사람이 손으로 적기에 *번거롭다*. 컴포넌트가 추가될 때마다 4군데를 빠짐없이 수정해야 한다. 한 군데라도 빠뜨리면 `equals`가 조용히 잘못 동작하는 *끔찍한 일*이 생긴다.

**Java 8 + Lombok 시절:**

```java
@Value
@Builder
public class OrderRequest {
    String customerId;
    List<OrderLine> lines;
    String couponCode;
}
```

5줄로 압축됐다. 그러나 이 코드를 읽기 위해서는 Lombok의 어노테이션 의미를 알아야 한다. `@Value`가 정확히 무엇을 만들어주는지, `@Builder`가 어떤 패턴을 따르는지. 그리고 IDE가 그 의미를 *제대로 인지하고 있어야* 빨간 줄이 없다. 외부 도구에 의존하는 코드.

**Java 21, records:**

```java
public record OrderRequest(
    String customerId,
    List<OrderLine> lines,
    String couponCode
) {}
```

5줄. 외부 의존성 없이 언어 차원에서 보증된 5줄. 컴파일러가 직접 알고, IDE가 직접 알고, 리플렉션이 직접 안다. *언어가 데이터 캐리어를 인정한 코드*다.

차이는 단순한 줄 수가 아니다. 의도가 *밖으로 드러나는* 정도가 다르다. Java 8 코드는 "불변 데이터 클래스를 만들고 싶어요"라는 의도를 *35줄의 boilerplate로 표현*했다. Lombok 코드는 그 의도를 *어노테이션의 의미를 빌려* 표현했다. records 코드는 그 의도를 *문법 그 자체로* 표현한다. 코드를 읽는 사람이 별도의 지식 없이도 "아, 이건 데이터 캐리어"라고 즉각 안다.

## 마무리

이 장에서 우리가 정리한 것을 한 번 거두어보자.

records는 *Lombok의 대체*가 아니다. 자바가 데이터 캐리어를 *언어 차원에서 인정한 신원 선언*이다. 그래서 records는 *DTO·VO·command·event·projection 결과·configuration*과 잘 맞고, JPA Entity·mutable 도메인 객체·logger를 품은 인프라 클래스와는 맞지 않는다. 두 영역이 자리를 다투지 않는다는 사실을 기억하자.

문법은 단순하다. record header에 컴포넌트를 나열하면 `private final` 필드, accessor, canonical constructor, `equals`/`hashCode`/`toString`이 자동으로 만들어진다. validation은 compact constructor로, 방어적 복사는 그 안에서 파라미터 재할당으로. 더 풀어 적고 싶다면 explicit canonical constructor도 가능하다.

Jackson은 records를 직접 안다. Spring `@ConfigurationProperties`도 records의 canonical constructor로 직접 바인딩한다. JPQL의 `new` 절이 record를 받아 projection을 돌려준다. *언어와 프레임워크의 합의가 자연스럽다*는 것이 records의 진짜 힘이다.

다음 장에서는 records의 *짝패*인 sealed classes를 살펴보자. records가 *product type*이라면 sealed는 *sum type*이다. 결제 상태 모델을 enum이 더 이상 표현하지 못하는 자리에서 시작해, 합 타입이 자바에 마침내 들어온 의미를 짚어보겠다. 그리고 13장에서 두 도구를 패턴 매칭으로 분해하는 *데이터지향 자바의 삼위일체*가 완성된다. record를 product, sealed를 sum, pattern을 분해기로 — 이 셋이 함께 만들어내는 표현력이 어디까지 가는지를 함께 보자.
