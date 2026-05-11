# 7장. `Optional<T>` — 약속과 함정

`user.getAddress().getCity().getZip()`의 NPE를 처음 만난 그날을 기억하는가.

테스트 환경에서는 멀쩡히 돌던 한 줄이다. 정산 페이지를 띄우면 사용자의 우편번호가 나와야 한다. 동료가 한 줄로 깔끔하게 적었다. 검토하는 우리도 자연스러워 보였다. 한 달 뒤 운영에서 `NullPointerException`이 떨어진다. 스택 트레이스가 가리키는 줄은 그 한 줄이고, 메시지는 단순하다. 어디서 `null`이 됐는지는 정확히 안 적혀 있다. 주소가 없는 사용자였나? 주소는 있는데 도시가 없었나? 도시까지 있는데 zip이 빠진 건가? 셋 다 가능하다. 그날 누구나 한 번씩 결심한다 — "다시는 이 패턴을 안 쓰겠다."

그래서 우리는 Java 8과 함께 들어온 `Optional<T>`를 반갑게 맞이했다. *Optional은 NPE의 명시화*다. 함수가 "값이 *있을 수도 있고 없을 수도 있는* 결과"를 돌려준다는 사실을 타입 시그니처에 박아 넣는다. 호출자는 `Optional`을 받는 순간 "이건 비어 있을 수 있구나"를 *반드시* 의식하게 된다. 깔끔한 약속이다.

그러나 이 약속을 우리는 *제대로* 쓰고 있는가?

10년이 지난 지금, 코드베이스를 한 번 훑어보면 *찜찜한* 자리가 곳곳에 보인다. `Optional<List<Order>>`를 반환하는 메서드, `Optional`을 클래스 *필드*로 들고 다니는 DTO, `optional.get()`을 일단 부르고 보는 패턴, `if (opt.isPresent()) opt.get()`이라는 `null != x ? x : null` 수준의 코드. Brian Goetz가 *반환 타입 전용*이라고 못 박았던 의도가 무색해진 자리가 한둘이 아니다. Optional을 둘러싼 가장 큰 *당혹감*은 NPE가 아니라, *Optional을 어디까지 어떻게 쓸지에 대한 합의 부재*다.

이번 장에서는 Optional의 *정확한 의도*를 다시 짚고, 거기서 자주 어긋나는 안티패턴을 짚어보자. 그리고 6장에서 미리 약속한 *monad-ish 색채*를 회수한다. `Optional::flatMap`이 왜 `Stream::flatMap`, `CompletableFuture::thenCompose`와 같은 모양인지를 한 자리에서 정리하자.

## Optional은 무엇이고 무엇이 아닌가

먼저 한 가지 인용을 박아두자. `Optional`의 설계자인 Brian Goetz가 2014년 Stack Overflow에 직접 남긴 답변이다.

> Of course, people will do what they want. But we did have a clear intention when adding this feature, and it was not to be a general purpose `Maybe` or `Some` type, as much as many people would have liked us to do so. Our intention was to provide a limited mechanism for library method return types where there needed to be a clear way to represent "no result."

번역하면 — "사람들이야 자기 마음대로 쓸 것이다. 그러나 우리는 분명한 의도를 갖고 이 기능을 추가했다. *범용* Maybe/Some 타입이 되라는 의도가 아니었다. 라이브러리의 *메서드 반환 타입*에서 '결과 없음'을 명확히 표현하기 위한 *제한적* 도구가 우리의 의도였다." 한 줄로 정리하면 — **Optional은 return type 한정**이다.

이게 왜 중요할까? 다른 자리에서 쓰면 무엇이 어긋나는지 하나씩 따라가보자.

### 필드 자리

```java
public class User {
    private Optional<Address> address;  // 찜찜한 자리
    ...
}
```

이 자리가 *찜찜한* 이유는 셋이다.

첫째, `Optional`은 직렬화 친화적이지 않다. `Optional`은 `Serializable`을 구현하지 않는다. Jackson 같은 JSON 직렬화는 별도 모듈이 있어야 다룬다. RPC, Kryo, 세션 직렬화에서 모두 *난감해진다*.

둘째, `Optional` 필드는 한 번 더 *간접 참조*를 만든다. `User` 100만 개가 있으면 `Optional` wrapper 객체도 100만 개다. 메모리도, 캐시 라인 효율도 손해다. 그 정도는 무시할 수 있다 쳐도, `address` 필드를 매번 `unwrap`해야 하는 *번거로움*은 매 줄에 묻어난다.

셋째, 의도가 어긋난다. 필드가 "있을 수도 있고 없을 수도 있다"는 의미는 `null` 가능성으로 표현하거나, 더 명시적으로는 별도 타입(예: `Address.NONE`, `sealed Address`)으로 표현하는 편이 *바람직하다*. `Optional`로 감싸는 것은 "이 값을 한 번만 길게 다루겠다"는 *반환 타입의 일회성* 의도와 어긋난다.

### 매개변수 자리

```java
public Order createOrder(Optional<Long> couponId, Optional<String> note) { ... }
```

이 자리는 *번거롭다*. 호출자가 매번 `Optional.empty()`나 `Optional.of(...)`로 감싸야 한다. 게다가 의미상 "쿠폰을 안 쓸 수도 있다"는 정보는 `null`을 허용하거나, 메서드 오버로딩으로 표현하거나, builder 패턴으로 푸는 편이 더 자연스럽다. 매개변수는 호출자가 *직접* 채우는 자리이므로, 거기에 `Optional`을 강요하는 것은 호출 코드를 *지저분하게* 만든다. IDE가 자동으로 `Optional.of`를 채워주지도 않는다.

### `Optional<List<T>>`

이게 가장 자주 마주치는 *당혹스러운* 자리다.

```java
public Optional<List<Order>> findRecentOrders(Long userId) { ... }
```

문제가 무엇인가? `List`는 이미 *비어 있을 수* 있다. 빈 List는 그 자체로 "결과 없음"을 표현한다. 거기에 `Optional`을 한 번 더 감싸면 *비어 있음의 의미가 둘로 갈라진다*. `Optional.empty()`인 경우와 `Optional.of(emptyList())`인 경우, 호출자는 무엇을 어떻게 다뤄야 하나? API 문서를 한 번 더 읽어야 한다. *지긋지긋하다*.

권장은 단순하다 — *컬렉션 타입은 절대 `Optional`로 감싸지 말자*. 그냥 빈 List를 돌려주는 편이 *바람직하다*. `Collections.emptyList()`나 `List.of()`로.

```java
public List<Order> findRecentOrders(Long userId) {
    // ... 없으면 List.of() 반환
}
```

`Map`도 마찬가지다. 빈 `Map`이 "결과 없음"을 그대로 표현한다. `Stream`도 그렇다. `Optional<Stream<T>>`는 처음 만나는 사람을 한참 *난감하게* 만든다. 그러니 다음을 *기억해두자*. **컨테이너 타입은 자기 자신이 비어 있는 상태를 표현할 수 있다. `Optional`로 한 번 더 감싸지 말자.**

### `Optional.of(null)`이라는 오해

이건 흔한 함정이다. 첫 입문자가 자주 한다.

```java
return Optional.of(user.getAddress());   // user.getAddress()가 null일 수도 있다면 NPE
```

`Optional.of(x)`는 `x`가 `null`이면 *즉시* `NullPointerException`을 던진다. `null`이 가능한 값이라면 `Optional.ofNullable(x)`를 써야 한다.

```java
return Optional.ofNullable(user.getAddress());
```

세 정적 팩토리를 한 번 *기억해두자*.

- `Optional.of(x)` — `x`가 `null`이면 NPE. 절대 `null`이 아닌 값에 쓴다.
- `Optional.ofNullable(x)` — `x`가 `null`이면 `empty()`. `null` 가능성이 있을 때.
- `Optional.empty()` — 비어 있음을 명시.

### `optional.get()`의 남발

이건 *끔찍한* 자리다.

```java
Optional<User> user = repo.findById(id);
return user.get();   // 비어 있으면 NoSuchElementException
```

`Optional`을 받아놓고 곧바로 `.get()`을 호출하면, 정확히 `Optional`이 막으려 했던 *그* 자리로 돌아간다. NPE 대신 `NoSuchElementException`이 떨어질 뿐, 본질은 같다. 게다가 stack trace는 더 *어색하다*. NPE는 무엇이 null인지 적어도 줄 번호로 가리키는데, `NoSuchElementException: No value present`는 그것도 없다.

권장은 단순하다. `.get()`을 보면 한 번 더 들여다보자. 거의 모든 자리에서 `.orElse(...)`, `.orElseGet(...)`, `.orElseThrow(...)`, `.ifPresent(...)` 중 하나가 더 정확한 의도를 표현한다.

```java
// 기본값으로 대체
User user = repo.findById(id).orElse(User.GUEST);

// 기본값을 비싸게 만들어야 한다면 lazy
User user = repo.findById(id).orElseGet(() -> userFactory.newGuest());

// 없으면 예외 — 비즈니스 의미 있는 예외로
User user = repo.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));
```

`orElse`와 `orElseGet`의 차이를 *반드시* 기억해두자. `orElse(fallback)`은 *항상* fallback 표현식을 평가한다. `orElseGet(supplier)`는 *비어 있을 때만* supplier를 호출한다. 비용이 큰 기본값이라면 `orElseGet`을 골라야 한다.

```java
// 매번 newGuest()를 호출한다 — 비어 있지 않아도
repo.findById(id).orElse(userFactory.newGuest());

// 비어 있을 때만 newGuest()를 호출한다
repo.findById(id).orElseGet(() -> userFactory.newGuest());
```

이 차이로 잘 돌던 서비스가 갑자기 *느려지는* 자리가 흔하다. 인지하면 한 줄 차이지만, 인지하지 못하면 한참을 끙끙대게 된다.

## Optional의 핵심 메서드 — `map`·`flatMap`·`filter`

이제 도입의 그 자리, `user.getAddress().getCity().getZip()`을 정확히 다듬어보자. 다음을 보자.

```java
// null-check 사다리
public Optional<String> zipOf(User user) {
    if (user == null) return Optional.empty();
    Address a = user.getAddress();
    if (a == null) return Optional.empty();
    City c = a.getCity();
    if (c == null) return Optional.empty();
    String z = c.getZip();
    return Optional.ofNullable(z);
}
```

여섯 줄이다. 같은 일이 Optional의 `map`·`flatMap`으로는 어떻게 표현되는가?

```java
public Optional<String> zipOf(User user) {
    return Optional.ofNullable(user)
        .map(User::getAddress)       // address가 null이면 empty
        .map(Address::getCity)        // city가 null이면 empty
        .map(City::getZip);           // zip이 null이면 empty
}
```

세 줄이다. 그리고 각 단계가 자명하다 — "user의 address의 city의 zip을 꺼낸다." `map`의 정확한 의미를 한 번 짚자. `Optional<A>::map(A -> B)`은 다음과 같이 작동한다.

- Optional이 비어 있으면, 그대로 `empty()`를 돌려준다.
- 비어 있지 않으면, 함수를 적용해 결과를 새 Optional로 감싼다. 함수가 `null`을 돌려주면 자동으로 `empty()`.

이 마지막 부분이 미묘하다. `map`에 넘긴 함수의 반환 타입이 *이미* `Optional`이라면? 그러면 `Optional<Optional<X>>`가 된다. 그게 우리가 원하는 자리가 아니다. 이런 자리를 위해 `flatMap`이 있다.

```java
// repo.findAddress가 Optional<Address>를 돌려준다고 해보자
public Optional<String> zipOf(Long userId) {
    return repo.findUser(userId)              // Optional<User>
        .flatMap(this::findAddressOf)         // Optional<Address> (map이면 Optional<Optional<Address>>)
        .map(Address::getCity)                 // Optional<City>
        .map(City::getZip);                    // Optional<String>
}
```

`flatMap`의 정확한 시그니처는 `Optional<A>::flatMap(A -> Optional<B>) -> Optional<B>`다. 함수의 반환이 이미 Optional이라 한 번 더 감싸지 않는다. 6장에서 본 monad-ish 형식 그대로다 — `M<A> + (A -> M<B>) -> M<B>`. `Optional`도 `Stream`도 `CompletableFuture`도 모두 이 형식의 친척이다.

`filter`는 술어로 걸러낸다. 술어가 거짓이면 `empty()`로 바뀐다.

```java
Optional<User> activeUser = repo.findById(id)
    .filter(User::isActive);   // 비활성이면 empty
```

이 셋 — `map`·`flatMap`·`filter` — 이 Optional의 *체인* 표현 방식이다. null-check 사다리를 명령형으로 짜는 자리에서, *흐름*으로 바꿔준다. 도입의 그날의 결심을 진짜로 실현하는 도구다.

## Java 9에서 더해진 자리들

Java 9가 Optional에 몇 가지를 더 추가했다. 자주 쓰는 셋만 짚자.

### `ifPresentOrElse`

값이 있으면 한 액션, 없으면 다른 액션. 그동안 두 줄로 적던 자리를 한 줄로 줄여준다.

```java
repo.findById(id).ifPresentOrElse(
    user -> log.info("found: {}", user.email()),
    () -> log.warn("missing: id={}", id)
);
```

### `or` — 비어 있을 때 다른 Optional로 fallback

```java
Optional<User> u = primaryRepo.findById(id)
    .or(() -> backupRepo.findById(id))
    .or(() -> Optional.of(User.GUEST));
```

여러 소스를 차례로 시도하는 자리에 잘 맞는다. `orElse`와 비슷해 보이지만 다르다. `orElse`는 *값*을 돌려주고 체인이 끝난다. `or`은 *Optional*을 돌려주고 체인이 계속된다.

### `stream` — Optional을 Stream에 흘리기

Java 9의 `Optional::stream`은 작아 보이지만 강력하다. `Optional<T>`를 0개 또는 1개 원소의 `Stream<T>`로 바꾼다. `Stream`의 `flatMap`과 결합하면 "Optional들의 시퀀스에서 비어 있는 자리를 제거하면서 펼친다"가 한 줄에 풀린다.

```java
// Java 8까지 — 어색했다
List<User> users = ids.stream()
    .map(repo::findById)             // Stream<Optional<User>>
    .filter(Optional::isPresent)
    .map(Optional::get)              // 찜찜한 .get()
    .collect(Collectors.toList());

// Java 9+ — 깔끔하다
List<User> users = ids.stream()
    .map(repo::findById)             // Stream<Optional<User>>
    .flatMap(Optional::stream)       // Stream<User>, 비어 있는 자리는 그냥 사라짐
    .toList();
```

`filter` + `get`이라는 *지긋지긋한* 패턴이 `flatMap(Optional::stream)` 한 줄로 정리된다. *기억해두자*. ids → repo lookup → 결과 모음 패턴이라면 이 형식이 거의 항상 들어맞는다.

## Optional의 monad 색채

이쯤에서 6장의 약속을 회수하자. `Optional::flatMap`이 `Stream::flatMap`, `CompletableFuture::thenCompose`와 같은 형식이라는 사실. 한 번 나란히 늘어놓자.

```java
// Stream
<R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper);

// Optional
<U> Optional<U> flatMap(Function<? super T, ? extends Optional<? extends U>> mapper);

// CompletableFuture
<U> CompletableFuture<U> thenCompose(Function<? super T, ? extends CompletionStage<U>> fn);
```

같은 모양이다. *컨텍스트 안의 값* + *컨텍스트로 가는 함수* → *컨텍스트 안의 결과*. 카테고리 이론에서는 이 형식을 monad의 bind라고 부른다. 자바가 이 셋을 *우연히* 같은 모양으로 만든 건 아니다 — Java 8 함수형 그룹의 설계 의도였다.

이걸 알면 무엇이 좋은가?

첫째, *새 컨테이너*를 만나도 패턴이 같다. `Result<T>`(rust-style success/failure), `Try<T>`(vavr), `Either<L, R>` — 모두 `flatMap`이 있다면 같은 형식으로 체인한다.

둘째, *코드의 의도*가 한 패턴으로 통일된다. "값이 있을 수도 있고 없을 수도 있다"는 컨텍스트, "비동기 미래 시점에 결과가 올 것이다"는 컨텍스트, "여러 원소가 펼쳐진다"는 컨텍스트 — 모두 같은 *체인의 모양*으로 표현된다. 그래서 한 패턴을 익혀두면 다른 자리에 그대로 옮긴다.

다만 Brian Goetz가 한 발 물러나 한 말도 *기억해두자*. "Optional은 모나드가 아니다. 그러나 모나드처럼 쓸 수 있는 자리들이 있다." 정확하게는 자바 타입 시스템이 모나드 법칙을 *강제하지 못한다*. 사용자가 `flatMap`에 부수 효과를 섞거나 `null`을 돌려주거나 하면 형식이 깨진다. 그래서 자바의 Optional은 "monad-ish"이지 monad가 아니다. 그러나 *형식이 같아서 같은 사고법을 쓸 수 있다*는 사실은 그대로 남는다. 그것만으로도 우리에게 충분한 가치다.

## `null` vs `Optional.empty()` vs sentinel

API를 설계할 때 한 번씩 고민이 된다. "결과 없음"을 어떻게 표현할까. 세 가지 선택지가 있다.

1. `null`을 돌려준다. 호출자가 `null`-check를 한다.
2. `Optional.empty()`를 돌려준다. 호출자가 `map`·`flatMap`·`orElse` 체인을 쓴다.
3. *sentinel* 값(예: `User.GUEST`, `Money.ZERO`)을 돌려준다. 호출자가 그것을 정상값처럼 다룬다.

각각의 자리가 다르다.

**`null`을 권장하는 자리** — 명확히 *없음*이 정상 흐름이 아닐 때. 가령 내부 헬퍼 메서드, private 메서드, 컬렉션의 `get(key)`(있는지 사전에 보는 게 일반적). Brian Goetz도 인터뷰에서 "Optional이 null을 *대체*하는 게 아니다, 그저 *반환 타입에서* null을 명시화하는 자리에 좋다"라고 말한다.

**`Optional.empty()`를 권장하는 자리** — public API의 반환 타입. 호출자가 "결과 없음"을 인지하고 처리해야 하는 자리. `Stream::findFirst`, `Repository::findById`, `Map::get`을 감싸는 wrapper 등.

**sentinel을 권장하는 자리** — "없음"이 자주 일어나고, 도메인적으로 *기본값*이 명확할 때. 가령 잔액이 없으면 `Money.ZERO`, 사용자가 비로그인이면 `User.GUEST`. sentinel은 null-check도 Optional unwrap도 필요 없어 호출 코드가 가장 *깔끔*하다.

세 가지를 *반드시* 구분해두자. 한 가지 만능 패턴이 아니다.

## JPA·Spring Data와 Optional

실무의 자리로 가보자. Spring Data Repository는 다음과 같이 Optional을 돌려준다.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
```

이건 거의 모범적인 자리다. ID·email로 단일 결과를 찾는 자리에서 *없음*이 가능하다는 것을 명시적으로 표현한다. 호출 코드는 다음과 같이 깔끔하게 흐른다.

```java
@Transactional(readOnly = true)
public UserSummary summaryOf(String email) {
    return userRepo.findByEmail(email)
        .map(UserSummary::from)
        .orElseThrow(() -> new UserNotFoundException(email));
}
```

여기에 *함정*이 하나 있다. Optional 안의 JPA 엔티티는 *영속성 컨텍스트*에 묶여 있다. `@Transactional` 범위를 벗어나면 그 엔티티의 lazy 연관 관계를 건드릴 때 `LazyInitializationException`이 떨어진다. 그래서 Optional의 `map` 단계에서 즉시 DTO로 변환해 *분리*해두는 편이 *바람직하다*. 위 코드의 `.map(UserSummary::from)`이 정확히 그 자리다.

또 한 자리 — `@RequestParam(required = false)`와 Optional.

```java
@GetMapping("/search")
public List<Order> search(@RequestParam Optional<String> q,
                          @RequestParam(defaultValue = "10") int size) { ... }
```

Spring은 `@RequestParam`을 Optional로 받는 패턴을 지원한다. 하지만 권장이 갈린다. 한쪽에서는 "Optional을 매개변수 자리에 두는 안티패턴"이라고 한다. 다른 쪽에서는 "Spring MVC는 컨트롤러 시그니처를 직접 호출하지 않으므로, 그 자리는 일반적인 메서드 매개변수와 다르다"고 한다. 정착된 권장은 *팀의 컨벤션*을 따르되, 일관성을 깨지 말자는 정도다. 어느 쪽이든 한 컨트롤러 안에서는 같은 스타일로 가는 편이 *바람직하다*.

## 안티패턴 6가지 — 정리

지금까지 짚은 자리를 한 번 묶어두자. *반드시* 피해야 할 여섯 자리다.

1. **`Optional`을 필드로 들고 다닌다** — 직렬화·메모리·간접 참조 모두 *번거롭다*. null 가능 필드, sealed 타입, 별도 plain field로 푸는 편이 낫다.
2. **`Optional`을 매개변수로 받는다** — 호출자에게 `Optional.of` 감싸기를 강요한다. 메서드 오버로딩이나 builder가 *바람직하다*.
3. **`Optional<List<T>>`/`Optional<Map<K,V>>`** — 빈 컬렉션이 이미 "없음"을 표현한다. 한 번 더 감싸지 말자.
4. **`Optional.of(x)`로 nullable x를 감싼다** — NPE. `Optional.ofNullable`을 쓰자.
5. **`optional.get()` 남발** — `Optional`의 의미를 무효화한다. `orElse`·`orElseGet`·`orElseThrow`·`ifPresent`를 골라 쓰자.
6. **`if (opt.isPresent()) opt.get()` 패턴** — null-check를 *흉내*낸 코드다. `ifPresent`·`map`·`flatMap`으로 다시 적자.

이 여섯을 *잊지 말자*. Optional을 *제대로* 쓰는 것은 NPE를 줄이는 일이 아니라, *체인의 흐름*으로 사고하는 일이다.

## 미래 — null-restricted types와 JSpecify

마지막으로 한 발 앞을 내다보자. 자바의 null 문제는 Optional로 *완전히* 해결되지 않았다. 컬렉션 원소의 null, 메서드 매개변수의 null, 필드의 null — 모든 자리가 Optional로 감싸기에는 너무 *번거롭다*. 그래서 코틀린은 `String?` vs `String`을 *언어 차원*에서 구분했고, Swift는 `Optional<T>` 위에 `?` 문법 설탕을 얹었다. 자바는 어디로 갈까?

두 가지 흐름이 있다.

**JSpecify** — 자바 커뮤니티의 합의 노력이다. `@Nullable`, `@NonNull` 어노테이션의 *표준화*를 추진한다. IntelliJ·NullAway·CheckerFramework 등 도구가 같은 어노테이션 어휘를 공유해 정적 분석을 일관되게 한다. 이미 상당히 정착했다.

**Project Valhalla & null-restricted types** — OpenJDK의 더 야심 찬 방향. JEP draft 단계에서 `String!`(non-null) vs `String?`(nullable)을 타입 시스템에 *직접* 박아 넣자는 제안이 논의 중이다. value type과 결합해 메모리 표현까지 최적화한다. 시점은 아직 불확실하다. Valhalla 자체가 10년째 진행 중인 거대 프로젝트라, null-restricted types는 그 한 갈래로 따라온다.

이 두 흐름이 합쳐지면 `Optional`의 *역할*도 조금 달라질 수 있다. 메서드 반환의 "없음 가능성"을 타입으로 표현하는 자리는 여전히 `Optional`이지만, 컬렉션 원소나 필드의 null 표현은 어노테이션·언어 문법으로 옮겨갈 가능성이 크다. 그날이 오면 우리는 다시 한 번 *Optional을 어디까지 쓸지*를 다듬게 될 것이다. 그러나 그 다듬음은 *Optional을 더 정확하게* 쓰는 방향이지, *없애는* 방향은 아닐 것이다.

## 마무리

Optional은 *반환 타입*에서 "결과 없음"을 명시화하는 *제한적* 도구다. 필드·매개변수·컬렉션 감싸기에는 어울리지 않는다. `get()`은 남발하지 말고 `map`·`flatMap`·`filter`로 체인하자. `orElse`와 `orElseGet`의 평가 시점 차이를 *반드시* 기억해두자. Java 9의 `ifPresentOrElse`·`or`·`stream`은 작지만 코드의 *답답함*을 정확하게 풀어준다.

`Optional::flatMap`이 `Stream::flatMap`·`CompletableFuture::thenCompose`와 같은 형식이라는 사실, 그 형식이 monad-ish 패턴의 한 모습이라는 사실 — 이 시야를 한 번 *기억해두자*. 자바 안에 *함수형 자바*라는 부분 언어가 자리 잡았고, Optional은 그 부분 언어의 한 시민이다. 도입의 그날 결심한 *"다시는 이 패턴을 안 쓰겠다"*가 실현되는 자리는, `null`-check를 줄이는 자리가 아니라 *체인의 흐름*으로 사고하는 자리다.

여기까지가 Part III의 끝이다. 함수형 자바의 기초(3·4장)에서 출발해, Stream의 해부(5장), Collector·Gatherer의 봉우리(6장), Optional의 약속과 함정(7장)까지 한 호흡으로 왔다. 다음 부에서는 결이 크게 바뀐다. *동시성*이다. `synchronized`와 `volatile`이 정확히 무엇을 보장하는가? `java.util.concurrent`의 지형은 어떻게 생겼는가? 그리고 우리가 5장 끝에서 *끔찍한 일*이라 부른 `parallelStream`의 commonPool 사건은, 왜 그렇게 자주 일어났는가? 8A장에서 Java Memory Model을 정확히 들여다보고, 8B장에서 `CompletableFuture`와 `Flow`로 비동기 조합의 두 갈래를 살펴보자. Loom 이전 시대의 자바 동시성을 한 번 차분히 정리하고 나면, 14장의 virtual thread가 왜 *대전환*이라 불리는지가 비로소 *체감*된다.
