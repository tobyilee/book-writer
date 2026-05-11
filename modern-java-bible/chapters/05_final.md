# 5장. Stream API — 선언적 데이터 파이프라인의 해부

팀 리뷰에서 동료가 `orders.parallelStream().filter(...).collect(toList())`라는 한 줄을 무심코 던졌다고 해보자. 누구도 그 한 줄을 깊이 들여다보지 않는다. 리뷰는 통과되고, 그 코드는 다음 날 운영에 올라간다. 그리고 한 달쯤 뒤 어느 한가한 평일 오후, 결제 서비스의 p99가 갑자기 800ms를 넘기 시작한다. 로그를 뒤지면 단서가 부족하고, 스레드 덤프를 떠 보면 어딘가 익숙한 이름이 자꾸 보인다 — `ForkJoinPool.commonPool-worker-3`, `ForkJoinPool.commonPool-worker-5`. 그제야 누군가가 묻는다. "그 `parallelStream()`, 그게 정말 우리가 의도한 거였나?"

이게 Stream을 둘러싼 가장 흔한 *난감함*이다. 우리는 Stream을 "컬렉션을 함수형으로 다루는 새 API" 정도로 안다. `filter` 다음에 `map`, 그 다음에 `collect`. 한 줄로 우아하게 풀린다. 그런데 그 "우아함"이 정확히 무엇을 뜻하는지, 안쪽에서 무엇이 벌어지는지를 한 문장으로 말해보라면 갑자기 말문이 막힌다. Stream은 컬렉션인가? 아니면 컬렉션 위에 얹힌 뷰인가? 그것도 아니면 따로 존재하는 새 자료구조인가? 답이 모두 어긋난다.

Stream을 정확히 이해하지 않으면 그것을 *오용*하는 모든 패턴이 자연스러워 보인다. `peek` 안에서 외부 변수에 값을 쓰고, `forEach`로 상태를 변경하고, 멀티 스레드 환경에서 `Collectors.toMap`이 던지는 `IllegalStateException`에 당황한다. 이번 장에서는 한 발 물러서서, Stream이 *무엇이고 무엇이 아닌지*부터 차분하게 짚어보자. 그 다음에야 중간 연산과 종단 연산의 카탈로그가 의미를 갖는다.

## Stream은 컬렉션이 아니다

먼저 한 가지 오해를 깨자. Stream은 데이터를 *저장*하지 않는다. `List`나 `Set`처럼 원소를 담는 자료구조가 아니라, 데이터가 *흘러 지나가도록* 만든 파이프라인이다. 자바 공식 문서의 표현을 한 번 그대로 옮겨보자.

> A sequence of elements supporting sequential and parallel aggregate operations. ... Streams differ from collections in several ways: **No storage. A stream is not a data structure that stores elements; instead, it conveys elements from a source through a pipeline of computational operations.**
> — `java.util.stream` package summary

"No storage." 이 한 줄이 Stream의 정체를 가장 정확하게 드러낸다. Stream은 *원본*(컬렉션, I/O 채널, 제너레이터 함수 등)에서 원소를 꺼내, 일련의 연산을 거쳐, 마지막 종단 연산까지 흘려보내는 *데이터 흐름의 추상*이다. 그래서 Stream에는 인덱스가 없고, 같은 Stream을 두 번 소비할 수도 없다.

```java
Stream<Order> s = orders.stream();
s.count();              // OK
s.filter(...).count();  // IllegalStateException: stream has already been operated upon
```

처음 만나면 "이게 왜 안 되지?" 싶다. 하지만 Stream이 "흐르는 것"이라는 정의를 받아들이면 당연해진다. 강물에 손을 두 번 담그면 같은 물이 아니지 않나. Stream도 마찬가지다.

또 하나, Stream은 *lazy*하다. `filter`·`map`·`flatMap` 같은 중간 연산은 호출 시점에는 아무 일도 하지 않는다. 종단 연산이 도착해야 비로소 데이터가 흐르기 시작한다. 다음 코드를 한번 머릿속으로 돌려보자.

```java
List<Order> orders = ...;
Stream<Order> pipeline = orders.stream()
    .filter(o -> {
        System.out.println("filter: " + o.id());
        return o.amount() > 1000;
    })
    .map(o -> {
        System.out.println("map: " + o.id());
        return o.toDto();
    });
// 여기까지 어떤 출력도 나오지 않는다.

pipeline.findFirst(); // 이 시점에 첫 원소부터 filter·map이 차례로 실행된다.
```

`filter`·`map`이 줄지어 있어도, 그것들은 "지시서"일 뿐이지 실행되는 코드가 아니다. 종단 연산이 트리거되는 순간 Stream은 원소를 하나씩 길어 올려, 그 원소에 대해 `filter` → `map`을 *수직으로* 적용한다. 모든 원소를 `filter` 끝낸 다음 모든 원소를 `map`하는 *수평* 방식이 아니다. 이 차이가 short-circuit과 무한 Stream을 가능하게 만든다.

short-circuit이란 종단 연산이 "필요한 만큼만" 원소를 끌어다 쓰고 멈출 수 있다는 뜻이다. `findFirst`·`findAny`·`anyMatch`·`allMatch`·`noneMatch`·`limit`는 모두 short-circuit 연산이다. 다음을 보자.

```java
long count = Stream.iterate(1L, i -> i + 1)  // 1, 2, 3, ... 무한
    .filter(i -> i % 7 == 0)
    .limit(5)
    .count();
// 35
```

`Stream.iterate`는 무한 시퀀스다. 평범한 컬렉션이라면 절대 끝나지 않는다. 그러나 `limit(5)`가 short-circuit으로 작동하기 때문에 Stream은 7의 배수 다섯 개를 길어 올린 뒤 깔끔하게 멈춘다. 이게 "lazy + short-circuit"의 힘이다.

여기서 한 가지 *주의해야 한다*. `filter` 안에서 외부 상태를 건드리거나, `peek`으로 부수 효과를 넣고 그 효과가 일어났을 거라고 가정하면 안 된다. lazy 평가는 곧 *언제, 몇 번, 어떤 순서로* 실행될지 확정되지 않는다는 뜻이다. 종단 연산이 무엇이냐에 따라 호출 횟수가 달라지고, 병렬화 여부에 따라 순서도 달라진다. Stream 문서가 그렇게 강조하는 *non-interference*와 *statelessness* 원칙이 바로 이 지점에서 나온다.

## non-interference와 statelessness — Stream이 우리에게 요구하는 두 가지

`java.util.stream` 패키지 문서를 보면 "Non-interference" 절이 따로 마련돼 있다. 한 단락만 옮겨두자.

> For most data sources, preventing interference means ensuring that the data source is not modified at all during the execution of the stream pipeline. The notable exception to this are streams whose sources are concurrent collections, which are specifically designed to handle concurrent modification. ... The behavioral parameters of stream operations, such as the predicate to filter or the function passed to map, should be **stateless** in most cases.
> — `java.util.stream` package summary, "Non-interference" / "Stateless behaviors"

해석하면 이렇다. 첫째, Stream이 흐르는 동안 *원본*을 건드리지 마라. 둘째, `filter`·`map`에 넘기는 람다는 *상태 없이* 작동해야 한다. 이 두 조건이 깨지면 Stream은 정의되지 않은 동작을 한다.

상태 없음이 왜 중요할까? Stream은 sequential로 도는지 parallel로 도는지를 *마지막 순간*까지 결정하지 않는다. `parallel()` 한 번이 끼어드는 순간 같은 람다가 여러 스레드에서 동시에 호출될 수 있다. 람다가 자체 상태(필드, 외부 변수)를 만지면 race condition이다. sequential에서는 "어쩌다 잘 돌던" 코드가 parallel에서 갑자기 결과가 흔들린다. 다음은 자주 보는 *찜찜한* 패턴이다.

```java
List<Order> filtered = new ArrayList<>();
orders.stream()
      .filter(o -> o.amount() > 1000)
      .forEach(filtered::add);   // forEach에서 외부 리스트에 add
```

한눈에 보면 무해해 보인다. sequential에서는 잘 돈다. 그러나 누가 `stream()` 자리에 `parallelStream()`을 넣으면 `ArrayList`는 thread-safe가 아니기 때문에 결과가 깨지기 시작한다. 게다가 위 코드는 의도부터가 잘못됐다. Stream의 정확한 용법은 외부 리스트에 `add`하는 것이 아니라, `collect`로 새 리스트를 *얻는* 것이다. 다음처럼 다듬는 편이 낫다.

```java
List<Order> filtered = orders.stream()
    .filter(o -> o.amount() > 1000)
    .collect(Collectors.toList());        // Java 8
// 또는
List<Order> filtered = orders.stream()
    .filter(o -> o.amount() > 1000)
    .toList();                            // Java 16+, 불변 리스트
```

위 두 줄이 같은 결과를 주는 것 같지만 정확히는 다르다. `Collectors.toList()`는 *구현 비지정* 가변 리스트(현재 JDK는 `ArrayList`)를 돌려주고, Stream 16에 추가된 `Stream::toList`는 *불변* 리스트를 돌려준다. 의도가 "이 리스트를 더는 안 건드린다"라면 후자가 더 명확하다. Java 16 이상을 쓴다면 새 코드는 `.toList()`로 가는 편이 바람직하다.

`peek`을 디버깅 용도로 끼워 넣고 그대로 운영에 올린 경험이 있다면, 그 *찜찜함*을 기억해두자. 공식 문서가 명시한다: "The action specified by this method should not modify the stream's source or have other observable side-effects." `peek`은 어디까지나 *관찰용*이고, 종단 연산이 모든 원소를 끌어다 쓰지 않으면 `peek`도 그만큼 호출되지 않는다. `findFirst`로 끝나는 파이프라인에 `peek`을 걸어두면, 원소 하나만 보고 종료한다. 디버깅 의도와 어긋난다. 디버깅 자리에는 `peek`보다 `forEach`나 별도 로그 줄을 쓰는 편이 안전하다.

## 중간 연산의 카탈로그 — 익숙한 것부터 덜 익숙한 것까지

중간 연산은 Stream을 받아 Stream을 돌려준다. 그래서 체인이 가능하다. 주요 연산을 카탈로그처럼 한 번 정리해보자.

| 연산 | 의미 | 비고 |
|------|------|------|
| `filter` | 술어가 참인 원소만 통과 | stateless |
| `map` | 1:1 변환 | stateless |
| `flatMap` | 1:N 변환 후 평탄화 | stateless, 6장 다시 회수 |
| `mapMulti` (Java 16) | 1:N을 콜백으로 표현 | flatMap보다 가벼움 |
| `distinct` | 중복 제거 | *stateful* — 본 원소 기억 필요 |
| `sorted` | 정렬 | *stateful* — 전체를 봐야 함 |
| `peek` | 관찰용 부수 효과 | 디버깅 한정 |
| `limit(n)` | 앞 n개만 통과 | short-circuit |
| `skip(n)` | 앞 n개 건너뜀 | stateful |
| `takeWhile` (Java 9) | 조건 참인 동안만 통과 | short-circuit |
| `dropWhile` (Java 9) | 조건 거짓이 될 때까지 버림 | stateful |

여기서 stateless / stateful의 구분을 *기억해두자*. stateless 연산(`filter`·`map`·`flatMap`)은 원소 하나만 보면 결정이 끝난다. 그래서 병렬화에 거의 비용 없이 따라간다. stateful 연산(`distinct`·`sorted`·`skip`)은 원소들 간의 상호 관계를 기억해야 한다. 병렬에서는 그 "기억"을 합치는 추가 비용이 든다. `parallel()` 뒤에 `sorted()`를 두면 부분별로 정렬한 뒤 머지가 따라온다.

`takeWhile`·`dropWhile`은 Java 9에 들어왔다. for-loop의 `break` / 조건부 `continue`를 Stream 한 줄로 옮기는 자리에 잘 맞는다.

```java
List<LogLine> head = lines.stream()
    .takeWhile(l -> l.level() != Level.ERROR)
    .collect(Collectors.toList());
```

ERROR가 나오기 *전까지*의 로그만 남긴다. 한때 이 패턴을 if-break로 적던 시절을 떠올려보면, takeWhile 한 줄이 얼마나 깔끔한지 *체감*된다. dropWhile은 그 반대 — ERROR가 나올 때까지 *버리고*, 그 이후부터 받는다.

`mapMulti`는 Java 16에 들어온 비교적 새 연산이다. 1:N 변환이 필요하지만 `flatMap`처럼 매번 새 Stream 객체를 만들기 부담스러울 때를 위한 도구다. 작은 람다 안에서 `Consumer::accept`를 직접 호출해 원소를 *내보낸다*.

```java
list.stream()
    .<String>mapMulti((o, downstream) -> {
        downstream.accept(o.firstName());
        if (o.middleName() != null) downstream.accept(o.middleName());
        downstream.accept(o.lastName());
    })
    .forEach(System.out::println);
```

같은 일을 `flatMap`으로 적으면 매번 임시 Stream을 만들어야 한다. `mapMulti`는 그 비용을 줄인다. 모든 자리에 어울리지는 않으니, 가벼운 1:N이라면 여전히 `flatMap`이 읽기 좋다는 점은 *잊지 말자*.

## 종단 연산의 카탈로그

종단 연산은 Stream을 *소비*하고 결과를 돌려준다. 종단이 호출되는 그 순간이 lazy 파이프라인의 트리거 지점이다. 주요 연산을 묶어 살펴보자.

| 종단 연산 | 결과 | short-circuit |
|----------|------|---------------|
| `forEach` / `forEachOrdered` | `void`, 부수 효과 | 아니오 |
| `collect(Collector)` | 임의 누적 결과 | 아니오 |
| `toArray` / `toList` (Java 16) | 배열 / 리스트 | 아니오 |
| `reduce` | 단일 값 누적 | 아니오 |
| `count` | 원소 수 | 아니오 |
| `min` / `max` | `Optional<T>` | 아니오 |
| `findFirst` / `findAny` | `Optional<T>` | **예** |
| `anyMatch` / `allMatch` / `noneMatch` | `boolean` | **예** |

종단 연산 중 가장 자주 쓰는 것이 `collect`다. 6장이 통째로 `collect`와 그 친구 `Gatherer`에 할애돼 있으니 자세한 이야기는 거기로 미루고, 여기서는 `reduce`를 한 번 짚어두자.

`reduce`는 누적을 일반화한 연산이다. 시그니처가 세 가지인데, 각각 다음 자리에 맞는다.

```java
// 1. identity 있고 결합 결과가 원소와 같은 타입
int sum = orders.stream().mapToInt(Order::amount).reduce(0, Integer::sum);

// 2. identity 없음 — Optional 반환
Optional<Order> biggest = orders.stream()
    .reduce((a, b) -> a.amount() > b.amount() ? a : b);

// 3. identity 있고 누적 타입이 원소와 다름
int totalChars = words.stream()
    .reduce(0, (acc, w) -> acc + w.length(), Integer::sum);
```

세 번째 시그니처가 가장 헷갈린다. accumulator와 combiner가 따로 들어간다. 왜 그럴까? 병렬에서 부분 결과를 합칠 때 *어떻게* 합칠지를 따로 알려줘야 하기 때문이다. accumulator는 "부분 결과 + 원소 → 부분 결과", combiner는 "부분 결과 + 부분 결과 → 부분 결과". sequential에서는 combiner가 호출되지 않을 수도 있지만, parallel에서는 필수다.

`reduce`가 제대로 돌려면 두 가지 수학적 조건이 필요하다. *identity*가 누적에 영향을 주지 않을 것(`combiner.apply(id, x) == x`), 그리고 *associativity*가 성립할 것(`combiner.apply(combiner.apply(a, b), c) == combiner.apply(a, combiner.apply(b, c))`). 덧셈·문자열 연결·집합 합집합은 모두 이 조건을 만족한다. 그러나 뺄셈은 결합 법칙이 깨진다. `reduce`에 뺄셈을 넣으면 sequential에서는 잘 돌다가 parallel에서 결과가 흔들린다. 이 *찜찜함*은 6장에서 monoid 이야기로 다시 회수한다.

`findFirst`와 `findAny`의 차이도 한 번 짚자. `findFirst`는 *encounter order*가 정의된 Stream에서 진짜로 첫 원소를 보장한다. `findAny`는 *어떤 원소든* 하나 — 병렬에서 가장 먼저 발견된 것이다. 순서가 의미 없는 자리(예: `Set` 기반 Stream)라면 `findAny`가 병렬에서 더 빠르다. 순서가 의미 있다면 `findFirst`를 골라야 한다.

## 박싱 함정과 primitive Stream

Stream의 우아함을 만끽하다가 한 번씩 부딪치는 *찜찜한* 자리가 박싱이다. `Stream<Integer>`로 1억 개를 더하면 모든 원소가 `int`에서 `Integer`로 박싱된다. 힙 위에 객체가 하나씩 만들어지고, GC가 그것을 청소한다. 측정해보면 같은 일을 primitive 배열로 하는 것보다 5~10배 느린 일이 흔하다.

그래서 자바는 `IntStream`·`LongStream`·`DoubleStream`이라는 별도 인터페이스를 둔다. boxing 없이 primitive를 그대로 흘려보내는 Stream이다.

```java
// 박싱 발생 — 느리고 GC 부담
int total = orders.stream()
    .map(Order::amount)        // Stream<Integer>
    .reduce(0, Integer::sum);

// 박싱 없음 — 빠르고 가벼움
int total = orders.stream()
    .mapToInt(Order::amount)   // IntStream
    .sum();
```

`mapToInt`·`mapToLong`·`mapToDouble`로 primitive Stream으로 옮기면, `sum`·`average`·`min`·`max`·`summaryStatistics` 같은 편의 메서드도 같이 따라온다. 다시 객체 Stream으로 가야 한다면 `mapToObj`·`boxed`로 돌아온다. 큰 컬렉션의 수치 집계에서는 *반드시* primitive Stream을 떠올리자.

## `parallelStream()`의 진실

이제 이 장의 핵심으로 돌아오자. `parallelStream()` 한 줄이다.

겉으로 보면 마법 같다. `stream()`을 `parallelStream()`으로 바꾸기만 하면 멀티 코어가 알아서 일을 나눠 받는다. 첫 인상에 끌려 곳곳에 뿌리고 싶은 욕구가 생긴다. 그러나 그 욕구는 *찜찜함*으로 돌아온다. 정확히 무엇이 벌어지는지 보자.

`parallelStream()`은 데이터를 `Spliterator`로 잘라, 작업을 *공용* `ForkJoinPool.commonPool()`에 제출한다. 그 풀은 JVM 한 프로세스 안에서 *전역으로 공유*된다. 우리가 쓴 `parallelStream` 한 줄 옆에서, 다른 라이브러리도, 다른 스레드도 같은 풀을 쓴다. 풀 크기는 기본으로 `Runtime.getRuntime().availableProcessors() - 1`. 8코어 머신이면 7. 풀이 7개라는 뜻은, 동시에 7개 이상의 *큰* 작업을 던지면 컨텐션이 발생한다는 뜻이다.

더 무서운 자리가 따로 있다. blocking I/O다. 다음 코드는 *끔찍한 일*이다.

```java
List<Result> results = userIds.parallelStream()
    .map(id -> restClient.callUserService(id))   // 블로킹 호출
    .collect(Collectors.toList());
```

겉으로는 "여러 사용자를 병렬로 조회한다"는 의도가 보인다. 그러나 안쪽에서는 commonPool worker 7개가 모두 외부 호출에 막혀 멈춘다. 그 사이 같은 JVM의 다른 `parallelStream`·`CompletableFuture`(executor 미지정)·`Files.lines` 같은 자리까지 모두 멈춘다. 운영에서 이 패턴이 한 번 들어가면 *완벽하게 예측 불가한 latency spike*가 따라온다. 이걸 한 번 겪고 나면 `parallelStream`이라는 이름을 보는 것만으로 등이 시리다.

권장은 단순하다. **blocking I/O는 절대 `parallelStream`에 태우지 말자.** 외부 호출의 병렬화는 `CompletableFuture` + 전용 executor, 또는 14장에서 다룰 virtual thread + structured concurrency가 답이다. `parallelStream`은 *CPU-bound* 작업에, 그것도 *데이터 크기가 충분히 클 때만* 골라 쓰는 편이 바람직하다. 일반적으로 원소 10만 개 이하라면 sequential이 더 빠른 경우가 많다. 작업 단위 비용이 너무 작으면 split·merge 비용이 더 크다.

`parallelStream`을 쓸 자리라면 한 가지를 *반드시* 기억해두자. 결과를 모으는 자리가 thread-safe해야 한다. `Collectors.toList`·`toUnmodifiableList`·`toConcurrentMap`은 안전하게 합쳐진다. 그러나 외부 `ArrayList`에 `forEach::add` 같은 패턴은 깨진다. `forEach`도 `forEachOrdered`도 병렬에서는 결정적 순서를 다르게 다룬다 — `forEachOrdered`는 encounter order를 강제하느라 병렬화 이득을 깎아 먹는다. 정말로 순서가 중요하다면 sequential을 쓰는 편이 맞다.

## Spring과의 접점 — JPA Stream return의 함정

마지막으로 실무에서 자주 마주치는 한 자리를 짚자. Spring Data JPA의 Repository가 `Stream<T>`를 반환할 수 있다는 사실은 잘 알려져 있다.

```java
@QueryHints({@QueryHint(name = HINT_FETCH_SIZE, value = "100")})
@Query("select o from Order o where o.status = :status")
Stream<Order> streamByStatus(@Param("status") OrderStatus status);
```

큰 결과 집합을 메모리에 다 올리지 않고 *흘려* 처리하겠다는 의도다. 좋은 설계다. 그러나 함정이 둘 있다.

첫째, 이 Stream은 *반드시* 트랜잭션 안에서 소비돼야 한다. 트랜잭션이 끝나면 underlying ResultSet과 Connection이 닫힌다. 그 뒤에 Stream을 쓰면 `LazyInitializationException`이 떨어진다. 그래서 호출하는 메서드는 `@Transactional(readOnly = true)`로 감싸야 하고, 그 메서드 *안에서* 종단 연산까지 끝내야 한다.

```java
@Transactional(readOnly = true)
public BigDecimal sumPending() {
    try (Stream<Order> s = repo.streamByStatus(OrderStatus.PENDING)) {
        return s.map(Order::amount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

`try-with-resources`도 *잊지 말자*. Stream은 `AutoCloseable`이고, JPA Stream을 닫지 않으면 커서가 남는다. 매번 try 블록으로 감싸 닫는 편이 안전하다.

둘째, fetch size 힌트다. `HINT_FETCH_SIZE`를 명시하지 않으면 JDBC 드라이버 기본값(MySQL은 한 번에 전부, PostgreSQL은 명시 필요 등)이 적용된다. 그러면 "Stream으로 흘려 받는다"는 의도가 무색해진다 — 결국 ResultSet이 한 번에 다 올라온다. 큰 결과를 정말로 *흘려* 받고 싶다면 fetch size를 명시하고, 트랜잭션 안에서 소비하자.

## 마무리

Stream은 컬렉션이 아니다. 데이터가 *흘러* 지나가는 lazy 파이프라인이고, 종단 연산이 트리거되기 전까지 아무 일도 일어나지 않는다. non-interference와 statelessness가 그 위에서 약속처럼 따라온다. 이 두 약속을 깨면 sequential에서는 어쩌다 잘 돌다가 parallel에서 결과가 흔들린다.

중간 연산은 stateless가 기본이지만 `distinct`·`sorted`처럼 stateful한 것도 있다. 종단 연산은 lazy 파이프라인의 트리거이며, `reduce`는 identity와 associativity 위에서만 정확하다. primitive Stream은 박싱 비용을 깎아주는 도구로 *반드시* 떠올리는 편이 좋다. 그리고 `parallelStream`은 그 한 줄로 commonPool 전체를 흔들 수 있는 강력하고 *위험한* 도구다 — blocking I/O에 태우지 말고, CPU-bound 작업에서도 크기가 충분할 때만 신중히 쓰자.

여기까지가 Stream의 "표면"이다. 그러나 한 가지 자리가 여전히 남는다. `collect`. Stream의 종단 연산 중 가장 자주 쓰면서도 가장 깊은 자리다. `Collectors.groupingBy`로 한 줄에 마법을 부린 적이 있는가? 그 마법의 안쪽을 들여다보지 않으면, 어느 날 "왜 이게 안 되지?" 하고 *난감해질* 때가 반드시 온다. 게다가 Java 22~24에 등장한 새 도구 `Stream::gather`는 그동안 "Stream에서는 어색했다"고 여겼던 패턴들 — 슬라이딩 윈도우, 누적합, rate-limited 매핑 — 을 한 줄로 풀어준다. 다음 장에서는 `Collector`의 5요소를 직접 분해해 만들어보고, `Gatherer`로 자바 함수형의 *봉우리*를 한 번 올라가보자.
