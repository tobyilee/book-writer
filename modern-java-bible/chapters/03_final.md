# 3장. 람다와 함수형 인터페이스 — 그 익숙함의 진짜 의미

PR 리뷰에서 이런 코드를 만났다고 상상해보자. 상품 카탈로그를 정렬하는 코드인데, 람다가 여섯 단계로 중첩되어 있다. 바깥의 `Comparator.comparing(...)` 안에서 또 다른 `Function`이 호출되고, 그 안에서 `Predicate.and(...)`가 짜이고, 그 안에서 다시 람다가 `map`을 받아 람다를 반환한다. 코드는 분명 컴파일되고 테스트도 통과한다. 그런데 리뷰어 입장에서는 화면을 한참 들여다봐도 "이 람다의 `this`는 무엇이고, 어느 변수가 캡처됐고, 만약 null이 들어오면 어디서 깨질까"가 한눈에 들어오지 않는다. 난감하다.

람다를 처음 만난 게 2014년 봄이다. 그때 우리는 "익명 클래스를 짧게 적는 문법"이라고 배웠고, 한동안 그렇게 써먹어도 별 탈은 없었다. 그런데 람다는 정말 익명 클래스의 문법 설탕일까? 아니면 그 익숙한 화살표 뒤에 우리가 11년 동안 한 번도 제대로 들여다보지 않은 무엇인가가 숨어 있었던 걸까? 이 장에서 그 안을 한번 열어보자.

## 람다는 익명 클래스의 설탕인가

가장 흔한 오해부터 정리하자. Java 8 출시 직후 많은 입문서는 다음 두 코드가 "동등하다"고 적었다.

```java
// 익명 클래스
Runnable r1 = new Runnable() {
    @Override public void run() { System.out.println("hi"); }
};

// 람다
Runnable r2 = () -> System.out.println("hi");
```

두 코드는 *의미적으로는* 같은 일을 한다. `r1.run()`과 `r2.run()`은 동일한 출력을 낸다. 하지만 *어떻게 같은 일을 하는지*를 들여다보면 둘은 완전히 다른 메커니즘 위에 서 있다.

익명 클래스는 컴파일 시점에 새 `.class` 파일이 하나 더 만들어진다. `Outer$1.class`라는 익숙한 이름의 파일이다. 클래스로더가 그 파일을 읽고, 메모리에 클래스를 올리고, `new`로 인스턴스를 만든다. 람다는 그렇지 않다. 람다 표현식은 `invokedynamic` 바이트코드 한 줄로 컴파일되고, 첫 호출 시점에 `LambdaMetafactory`가 클래스를 *동적으로* 생성해 캐싱한다. 다음 호출부터는 그 캐시된 클래스의 인스턴스를 재사용한다. 다시 말해, 같은 람다를 천 번 호출해도 클래스로딩 비용은 한 번뿐이고, 인스턴스 생성 비용도 거의 들지 않는다.

이게 단순히 성능 최적화 이야기로 들릴 수도 있는데, 더 중요한 함의가 있다. **람다는 클래스가 아니다.** JVM은 람다를 "특정 함수형 인터페이스의 인스턴스를 어떻게 만들지에 대한 늦은 결정"으로 본다. 익명 클래스는 정적이고 람다는 동적이다. 그래서 두 코드의 `this`도, 직렬화 동작도, 디버거에서 보이는 스택프레임도, 전부 다르다.

기억해두자. 람다와 익명 클래스는 *문법 설탕* 관계가 아니라 *서로 다른 메커니즘으로 같은 인터페이스 약속을 이행하는 두 가지 방식*이다. 익숙해 보인다고 같은 것으로 묶지 말자.

### `this`의 정체

이 차이는 `this` 키워드에서 가장 극적으로 드러난다. 다음 코드를 보자.

```java
class CatalogService {
    private final String name = "main";

    void run() {
        Runnable anon = new Runnable() {
            @Override public void run() { System.out.println(this); }
        };
        Runnable lambda = () -> System.out.println(this);

        anon.run();    // CatalogService$1@... (익명 인스턴스)
        lambda.run();  // CatalogService@... (바깥 인스턴스)
    }
}
```

익명 클래스 안의 `this`는 그 익명 객체 자신이다. 그래서 바깥 필드에 접근하려면 `CatalogService.this.name`처럼 한정자를 붙여야 했다. 람다는 다르다. 람다 안의 `this`는 람다를 *둘러싼 메서드의 `this`*다. 람다는 자신만의 인스턴스 정체성을 갖지 않는다. 바깥의 `name`을 그냥 `name`이라고 적으면 된다.

이건 단지 편의의 문제가 아니다. 람다는 *콜백을 적는 문법*이 아니라 *바깥 컨텍스트를 그대로 들고 다니는 동작 조각*이라는 사실의 직접적 증거다. 우리가 람다를 자연스럽게 쓸 수 있는 이유의 절반은 여기서 온다.

## effectively final — 11년 묵은 오해

람다와 익명 클래스가 공유하는 제약이 하나 있다. 바깥의 지역 변수를 캡처할 때, 그 변수는 *final이거나 effectively final*이어야 한다. Java 7까지는 명시적으로 `final` 키워드를 붙여야 했다. Java 8부터는 키워드 없이도 "다시 대입되지 않는" 변수라면 컴파일러가 알아서 동등하게 취급해준다.

문제는 많은 개발자가 effectively final을 "그냥 컴파일러가 봐주는 편의 기능"으로 가볍게 여긴다는 점이다. 그렇지 않다. JLS의 정의를 직접 보자.

> **JLS §15.27.2 — Lambda Body**
> "Any local variable, formal parameter, or exception parameter used but not declared in a lambda expression must either be declared final or be effectively final, or a compile-time error occurs where the use is attempted."
>
> **JLS §4.12.4 — final Variables**
> "A local variable... is effectively final if it is not declared final but it never occurs as the left-hand operand of an assignment operator... or as the operand of a prefix or postfix increment or decrement operator."

핵심 문장은 "never occurs as the left-hand operand of an assignment"다. 한 번이라도 재대입되면 effectively final이 아니고, 그 변수는 람다 안에서 쓸 수 없다.

왜 이렇게 까다로울까? 자바의 람다는 *값을 캡처*한다. 참조 캡처가 아니라 값 캡처다. 람다가 만들어지는 순간 바깥 변수의 *현재 값*이 람다 객체 안으로 복사된다. 그 뒤로 바깥에서 변수가 바뀌어도 람다 안의 복사본은 옛 값을 그대로 가진다. 이게 멀티스레드 환경에서 람다를 안전하게 쓸 수 있게 해주는 보증이다. 만약 자바가 클로저 변수의 재대입을 허용했다면, 람다는 *어느 시점의 값을 봐야 하는지* 끝없이 헷갈리는 동시성 시한폭탄이 되었을 것이다.

다음 코드는 컴파일되지 않는다.

```java
int total = 0;
products.forEach(p -> total += p.price()); //  total은 effectively final이 아니다
```

이 코드를 처음 본 사람은 거의 예외 없이 *왜 안 되지*라고 짜증을 낸다. 컴파일러가 시키는 대로 `int[] total = {0}`처럼 배열로 우회하기도 한다. 그런데 그 우회는 동작은 하지만 *왜 그런 우회가 필요한지*에 대한 답은 못 된다. 답은 위에 적었다. 람다는 값을 캡처한다. 합계가 필요하다면 합계를 표현할 도구를 따로 써야 한다. 5장에서 다룰 `reduce`나 `Collectors.summingInt`가 그 도구다.

## 함수형 인터페이스 — 다섯 식구를 외우는 일

`java.util.function` 패키지에는 40개가 넘는 인터페이스가 있다. 처음 보는 사람은 그 양에 압도되는데, 실제로 매일 만나게 되는 건 다섯 식구뿐이다.

| 인터페이스 | 시그니처 | 의미 |
|-----------|----------|------|
| `Function<T, R>` | `R apply(T t)` | "T를 받아 R로 변환" |
| `Predicate<T>` | `boolean test(T t)` | "T가 조건을 만족하는가" |
| `Consumer<T>` | `void accept(T t)` | "T를 받아 어떤 동작을 수행" |
| `Supplier<T>` | `T get()` | "인자 없이 T를 만들어 반환" |
| `BiFunction<T, U, R>` | `R apply(T, U)` | "두 개를 받아 하나로 변환" |

여기에 `UnaryOperator<T>`(= `Function<T, T>`)와 `BinaryOperator<T>`(= `BiFunction<T, T, T>`)가 특수 케이스로 얹힌다. 그리고 `int`/`long`/`double` 같은 원시 타입 전용 변종이 박싱 비용을 줄이기 위해 추가로 정의되어 있다 — `IntPredicate`, `ToDoubleFunction`, `LongSupplier` 같은 것들이다.

처음에는 이 다섯만 익혀도 충분하다. 상품 카탈로그 도메인으로 옮겨와 보자.

```java
Function<Product, BigDecimal> price = Product::price;
Predicate<Product> inStock = p -> p.stock() > 0;
Consumer<Product> printName = p -> System.out.println(p.name());
Supplier<Product> empty = () -> new Product("", BigDecimal.ZERO, 0);
BiFunction<Product, BigDecimal, Product> discount =
    (p, rate) -> p.withPrice(p.price().multiply(BigDecimal.ONE.subtract(rate)));
```

다섯 가지 모양 안에 거의 모든 콜백이 들어간다.

### `@FunctionalInterface`의 진짜 역할

`@FunctionalInterface` 어노테이션을 처음 본 사람은 자주 묻는다. "이거 꼭 붙여야 하나요?" 결론부터 적으면, *기능 동작에는* 필수가 아니다. 추상 메서드 하나만 가진 인터페이스라면 어노테이션이 없어도 람다를 받을 수 있다. 그러면 왜 붙일까?

`@FunctionalInterface`는 *의도의 표명*이자 *컴파일 시점의 안전 장치*다. 누군가 "이 인터페이스에 추상 메서드 하나만 두겠다"는 약속을 어기고 두 번째 추상 메서드를 추가하면, 컴파일러가 즉시 에러를 내준다. 그 안전 장치가 없으면 6개월 뒤 후배가 메서드 하나 더 추가했을 때, 그 인터페이스를 람다로 받던 모든 코드가 *훨씬 멀리 떨어진 호출 지점*에서 의미 불명의 컴파일 에러를 토해낸다. 끔찍한 일이다.

Spring 코드베이스가 이걸 어떻게 쓰는지 살펴보자. `JdbcTemplate.query(...)`가 받는 `RowMapper<T>`는 `@FunctionalInterface`다. 한 메서드 — `mapRow(ResultSet, int)` — 만 추상이다. `WebClient`의 `ExchangeFunction`도 그렇다. Spring 팀이 이 어노테이션을 의도적으로 붙인 이유는, *프레임워크 사용자에게 "이건 람다로 쓰셔도 됩니다"라는 약속*을 코드로 박아 두기 위해서다. 우리가 직접 만드는 콜백 인터페이스에도 이 어노테이션을 붙이는 편이 낫다. 의도가 명시되고, 안전이 확보된다.

### default 메서드 — 같은 인터페이스에 살이 붙다

여기서 한 가지 짚고 갈 게 있다. 함수형 인터페이스는 *추상 메서드가 하나*여야 한다는 규칙은 변하지 않았다. 그러나 Java 8부터는 인터페이스에 `default` 메서드와 `static` 메서드를 적을 수 있다. 추상 메서드가 아니므로 함수형 인터페이스 자격을 깨지 않는다.

`Function<T, R>`을 한번 보자.

```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);  // 유일한 추상 메서드

    default <V> Function<V, R> compose(Function<? super V, ? extends T> before) { ... }
    default <V> Function<T, V> andThen(Function<? super R, ? extends V> after) { ... }
    static <T> Function<T, T> identity() { ... }
}
```

`compose`와 `andThen`은 default 메서드다. 함수형 인터페이스 약속을 깨지 않으면서도, *모든 `Function` 인스턴스가 합성 기능을 가지게* 만든 우아한 설계다. JDK 라이브러리 진화의 핵심 도구가 바로 이 default 메서드다. 우리가 람다 두 개를 받아 `.andThen()`으로 잇는 코드를 짤 수 있는 이유가 여기 있다.

## 함수 합성 — 람다끼리 잇기

지금부터가 람다의 *진짜 표현력*이 드러나는 자리다. 합성을 모르면 람다는 그냥 "짧게 적는 콜백"에 머문다. 합성을 알면 람다는 *재사용 가능한 도메인 어휘*가 된다.

```java
Function<Product, BigDecimal> price = Product::price;
Function<BigDecimal, BigDecimal> applyVat = p -> p.multiply(new BigDecimal("1.1"));
Function<BigDecimal, String> format = bd -> "₩" + bd.toPlainString();

Function<Product, String> displayPrice = price.andThen(applyVat).andThen(format);

displayPrice.apply(product); // "₩11000"
```

`andThen(g)`은 "이 함수를 먼저 적용하고, 결과에 `g`를 적용하라"는 뜻이다. `compose(g)`는 반대다 — "`g`를 먼저 적용하고, 결과에 이 함수를 적용하라". 두 메서드는 같은 일을 방향만 바꿔서 한다. 한번 합성해보자, 라고 권하고 싶다. 처음에는 어색해도, 도메인 함수 몇 개를 합성으로 잇는 순간 코드의 표현력이 달라진다.

`Predicate`는 더 풍성하다.

```java
Predicate<Product> inStock = p -> p.stock() > 0;
Predicate<Product> affordable = p -> p.price().compareTo(new BigDecimal("50000")) < 0;
Predicate<Product> onSale = p -> p.discount() > 0;

Predicate<Product> recommendable = inStock.and(affordable).or(onSale);
Predicate<Product> notRecommendable = recommendable.negate();
```

`and`, `or`, `negate` 세 default 메서드로 부울 대수가 그대로 코드에 들어온다. 도메인 규칙을 *말로 적은 대로* 읽힌다. 이 표현력 때문에 우리는 `if (p.stock() > 0 && (p.price().compareTo(...) < 0 || p.discount() > 0))` 같은 한 줄짜리 거대한 조건문에서 벗어날 수 있다.

`Consumer`에도 `andThen`이 있다. 여러 부수 효과를 한 줄로 잇고 싶을 때 쓴다.

```java
Consumer<Product> log = p -> logger.info("processing {}", p.id());
Consumer<Product> audit = p -> auditTrail.record(p);
Consumer<Product> process = log.andThen(audit).andThen(this::doProcess);
```

## 메서드 참조 — 람다의 다섯 번째 단축형

람다에 익숙해질수록 다음 패턴이 자주 나온다.

```java
products.stream().map(p -> p.name()).forEach(s -> System.out.println(s));
```

`p -> p.name()`은 그저 *이미 존재하는 메서드를 호출*하는 람다다. 자바는 이런 경우를 위해 메서드 참조 문법 `::`을 제공한다.

```java
products.stream().map(Product::name).forEach(System.out::println);
```

같은 동작이고, 더 짧고, *의도가 더 명확*하다. 메서드 참조는 네 가지 모양이 있다.

| 종류 | 문법 | 예시 |
|------|------|------|
| 정적 메서드 참조 | `ClassName::staticMethod` | `Integer::parseInt` |
| 한정된 인스턴스 메서드 참조 | `instance::method` | `System.out::println` |
| 한정되지 않은 인스턴스 메서드 참조 | `ClassName::instanceMethod` | `Product::name` |
| 생성자 참조 | `ClassName::new` | `ArrayList::new` |

세 번째 — 한정되지 않은 인스턴스 메서드 참조 — 가 가장 헷갈린다. `Product::name`은 "어떤 `Product` 인스턴스를 받아서 그 인스턴스의 `name()`을 호출하라"는 뜻이다. 즉 `Function<Product, String>`이다. 첫 인자가 *암묵적인 수신자*가 된다. 처음에는 찜찜하게 느껴지는데, 익숙해지면 `p -> p.name()`보다 훨씬 깔끔하다.

생성자 참조도 강력하다. `ArrayList::new`는 `Supplier<ArrayList>`고, `ArrayList::new`가 `int`를 받는 자리에 있으면 `IntFunction<ArrayList>`다. 컴파일러가 target type에 맞춰 알아서 골라준다.

```java
List<String> names = products.stream()
    .map(Product::name)
    .collect(Collectors.toCollection(LinkedList::new));
```

## 함정들 — 람다가 우리를 배신하는 자리

람다가 우아하다고 해서 모든 코드를 람다로 옮기면 안 된다. 11년을 써온 입장에서 자주 데이는 함정 몇 가지를 짚어두자.

**첫째, 캡처 비용.** 람다가 바깥 변수를 캡처하면, 그 람다는 더 이상 stateless가 아니다. JVM은 같은 람다를 호출할 때마다 *캡처값을 들고 있는 새 인스턴스*를 만든다. 캡처가 없는 람다는 싱글톤처럼 재사용되지만, 캡처가 있으면 그렇지 않다. tight loop 안에서 캡처 람다를 매번 새로 만드는 코드는 *조용히* GC 압력을 만든다.

**둘째, `null` 처리.** `Function<T, R>`이 `null`을 반환하면 그다음 `.andThen(...)` 단계로 그대로 흘러간다. Stream의 `.map(...).filter(...)` 체인 한가운데서 NPE가 터지면 스택 트레이스만 보고 어느 람다가 범인인지 알기 어렵다. JEP 358의 Helpful NPE가 Java 14부터 도와주긴 하지만, 람다 안에서는 여전히 추적이 까다롭다. null이 흘러갈 수 있는 자리에는 7장에서 다룰 `Optional`이나 명시적 가드를 두는 편이 낫다.

**셋째, 직렬화.** 람다는 기본적으로 직렬화되지 않는다. `Serializable`을 캐스트로 강제할 수는 있지만, 그 길로 가면 람다의 *동적 생성* 특성과 직렬화의 *정적 형태* 사이에서 끝없이 깨진다. Redis 캐시에 람다를 넣으려는 시도는 처음부터 포기하자.

**넷째, 디버깅.** 람다에 중단점(breakpoint)을 거는 일은 IDE가 많이 도와주긴 하지만, 익명 클래스만큼 직관적이지는 않다. 6중 중첩 람다의 4번째 단계에서 NPE가 나면, 람다 표현식을 명명된 메서드 참조나 `private` 메서드로 *풀어두는* 것이 디버깅 친화적이다. 람다는 짧을 때 가장 빛난다. 길어지면 *다시 메서드로 풀자*.

**다섯째, this 캡처와 메모리 누수.** 람다 안에서 `this`를 쓰면 바깥 인스턴스 전체가 캡처된다. UI 컴포넌트의 콜백, 이벤트 리스너 등에서 이게 누수의 원흉이 된다. 짧은 수명의 객체를 만들고 콜백을 길게 등록할 때는 람다 캡처 범위를 한 번 점검하자.

## Java 8과 Java 21 — 같은 람다, 다른 어휘

같은 일을 하는 코드를 두 시대에 적어 보자. 상품 카탈로그에서 재고가 있고 가격이 5만 원 미만인 상품의 이름 목록을 추출한다.

**Java 8 (2014)**

```java
List<String> result = new ArrayList<>();
for (Product p : products) {
    if (p.getStock() > 0 && p.getPrice().compareTo(new BigDecimal("50000")) < 0) {
        result.add(p.getName());
    }
}
Collections.sort(result);
```

**Java 21 (2023)**

```java
List<String> result = products.stream()
    .filter(inStock.and(affordable))
    .map(Product::name)
    .sorted()
    .toList();
```

람다와 함수형 인터페이스 덕분에 *무엇을 하는지*가 코드 자체로 읽힌다. 정렬 비교자도 마찬가지다.

```java
// Java 8 이전
Collections.sort(products, new Comparator<Product>() {
    @Override public int compare(Product a, Product b) {
        int cmp = a.getCategory().compareTo(b.getCategory());
        return cmp != 0 ? cmp : a.getName().compareTo(b.getName());
    }
});

// Java 8 이후
products.sort(comparing(Product::category).thenComparing(Product::name));
```

`Comparator.comparing(...).thenComparing(...)`은 default 메서드 합성의 가장 아름다운 예시 중 하나다. 도메인을 *말한 대로* 적게 해준다.

## Spring의 자리 — 프레임워크가 람다를 어떻게 받아들였나

Spring Framework 4.x와 Spring Boot 1.x는 Java 8과 거의 동시에 출시됐다. 그때부터 Spring 코드베이스는 람다를 적극 받아들였다. 몇 가지 대표 사례를 살펴보자.

`JdbcTemplate`의 `RowMapper`는 람다 친화적이다.

```java
List<Product> products = jdbcTemplate.query(
    "SELECT id, name, price FROM products WHERE category = ?",
    (rs, rowNum) -> new Product(rs.getLong("id"), rs.getString("name"), rs.getBigDecimal("price")),
    "electronics"
);
```

`RestTemplate`/`WebClient`의 콜백도 람다다. `WebClient.exchangeToMono(response -> ...)`, `RestClient`의 `onStatus(status -> status.is4xxClientError(), (req, res) -> ...)` 같은 패턴이 그대로 람다로 표현된다.

Spring의 `@Bean`으로 등록되는 함수형 빈도 람다로 정의된다.

```java
@Bean
public Function<OrderRequest, OrderResponse> orderProcessor(OrderService service) {
    return request -> service.process(request);
}
```

이 패턴은 Spring Cloud Function에서 더욱 빛난다. 한 람다가 AWS Lambda, Azure Functions, Spring Boot 컨트롤러 모두에서 *같은 함수*로 동작한다. 람다라는 언어 기능이 분산 시스템 아키텍처의 *배포 단위*가 된 셈이다.

람다가 단지 "짧게 적는 콜백"이 아니라 *Spring 같은 거대 프레임워크의 진화 방향을 바꿔놓은 도구*였다는 점을 기억해두자.

## 마무리

람다는 11년이 지난 지금도 여전히 *완전히 이해됐다*고 말하기 어려운 기능이다. 화살표 문법만 익히고 11년을 써온 우리에게, 이 장은 그 익숙함의 뒷면을 한 번 들여다보는 자리였다.

정리하자면 람다는 익명 클래스의 설탕이 아니라, `invokedynamic`과 `LambdaMetafactory`가 뒷받침하는 *완전히 다른 메커니즘*이다. effectively final은 컴파일러의 친절이 아니라 값 캡처라는 설계 결정의 직접적 결과다. `@FunctionalInterface`는 의도 표명이고, default 메서드는 라이브러리 진화의 열쇠다. 메서드 참조는 람다의 다섯 번째 단축형이고, 함수 합성은 도메인 어휘를 만드는 도구다.

다음 4장에서는 람다와 함께 Java 8이 가져온 또 다른 *조용한 혁명*을 살펴보자. 우리가 `java.util.Date`와 `Calendar`에서 정말로 벗어났는지, `java.time`이 그동안 풀어낸 문제가 정확히 무엇인지 — 결제 정산이 시간대 때문에 새벽에 깨졌던 그날을 떠올리며 함께 들여다보자.
