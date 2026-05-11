# 6장. Collector·Reducer·Gatherer — Stream의 종착과 새 중간 정거장

"5분 이동 평균을 Stream으로 한 번 구해보세요."

기획에서 데이터 분석 요건이 떨어졌다고 해보자. 결제 트랜잭션이 초당 수백 건씩 쌓이는데, *최근 5분간* 평균 결제 금액을 실시간으로 내고 싶다는 요구다. Stream에 익숙한 우리는 자신 있게 IDE를 연다. `filter` → `map` → `collect`. 그런데 손가락이 멈춘다. *슬라이딩 윈도우*. Stream에서 이걸 어떻게 표현하지?

`Collectors`를 한참 뒤져도 그런 자리는 없다. `groupingBy(timeBucket)`로 5분 단위 *고정* 버킷은 만들 수 있지만, "지금 시각 기준 직전 5분"이라는 *움직이는* 창은 만들 수 없다. for-loop으로 돌아가면 인덱스 두 개를 굴리면 된다. 그런데 Stream 한 줄로는 안 된다. 답답하다. *번거롭다*. 한참 끙끙대다가 결국 `IntStream.range(0, list.size() - 4).mapToObj(i -> list.subList(i, i + 5))` 같은 *어색한* 우회를 짜놓고 PR을 올린다. 리뷰어가 묻는다 — "이게 자연스러워 보이세요?" 답이 없다.

Stream API가 출시된 지 11년이 흘렀는데, *슬라이딩 윈도우*가 그동안 그렇게 *번거로웠던 이유*는 무엇일까. 정답은 단순하다. Stream의 중간 연산 자리가 닫혀 있었기 때문이다. `filter`·`map`·`flatMap`·`distinct`·`sorted` — 우리가 새 중간 연산을 직접 만들 수단이 없었다. `Collector`로 마지막 자리는 열려 있는데, 중간 자리는 막혀 있었다. 그래서 1:N, N:1, N:N 변환이 필요한 모든 패턴이 어색하게 우회해야 했다. 슬라이딩 윈도우, 누적합, rate-limited 매핑, 중복 제거의 변형 — 모두 이 막힘에 부딪쳐 *지긋지긋함*을 남겼다.

이 닫혀 있던 자리가 Java 22에서 preview로 열리고, Java 24에서 표준화됐다. 이름은 *Stream Gatherers* (JEP 461 → 473 → 485). 그 이야기에 도달하기 전에, 먼저 Stream의 종착인 `Collector`부터 깊이 들여다보자. `Collector`를 정확히 이해하지 않으면 `Gatherer`의 의미가 반쪽으로 들어온다. 이 두 도구는 형제다.

## `Collectors`의 표면 — 익숙한 자리부터

`Stream::collect`에 가장 자주 넘기는 인자는 `Collectors`의 정적 팩토리다. 거의 모든 자리에서 다음 셋만 알면 80%는 처리된다 — `toList`·`toMap`·`groupingBy`. 그러나 그 셋만 알면 나머지 20%의 자리에서 *난감*해진다. 카탈로그를 한 번 죽 늘어놓고 시작하자.

| Collector | 의미 |
|-----------|------|
| `toList()` | 가변 List로 모음 (구현 비지정) |
| `toUnmodifiableList()` (Java 10) | 불변 List로 모음 |
| `toSet()` / `toUnmodifiableSet()` | Set으로 모음 |
| `toMap(keyFn, valueFn)` | Map으로 모음, 키 충돌 시 예외 |
| `toMap(keyFn, valueFn, mergeFn)` | 키 충돌 시 mergeFn으로 합침 |
| `toMap(keyFn, valueFn, mergeFn, mapFactory)` | Map 구현을 직접 지정 |
| `groupingBy(classifier)` | 분류기로 Map<K, List<V>> |
| `groupingBy(classifier, downstream)` | 그룹별로 downstream collector 적용 |
| `partitioningBy(predicate)` | true/false 두 그룹으로 분할 |
| `joining()` / `joining(", ", "[", "]")` | 문자열 연결 |
| `counting()` | 원소 수 |
| `summingInt` / `summingLong` / `summingDouble` | 합 |
| `averagingInt` / `averagingLong` / `averagingDouble` | 평균 |
| `minBy(Comparator)` / `maxBy(Comparator)` | 최소/최대 |
| `summarizingInt` 등 | sum·avg·min·max·count 한 번에 |
| `reducing(...)` | 임의 누적 |
| `mapping(mapper, downstream)` | downstream 앞에 map |
| `flatMapping(mapper, downstream)` (Java 9) | downstream 앞에 flatMap |
| `filtering(predicate, downstream)` (Java 9) | downstream 앞에 filter |
| `teeing(c1, c2, merger)` (Java 12) | 같은 Stream을 두 Collector에 흘려 merger로 합침 |
| `collectingAndThen(downstream, finisher)` | downstream 결과를 한 번 더 변환 |

이 카탈로그를 한 줄씩 외울 필요는 없다. 그러나 *합성* 가능성은 *기억해두자*. `Collector`는 다른 `Collector`를 받아 새 `Collector`를 만든다. `groupingBy(classifier, downstream)`의 두 번째 인자가 또 `Collector`다. 이 합성성이 `Collector`의 진짜 힘이다. 익숙한 자리부터 합성을 한 번 따라가보자.

```java
// 1) 단순 그룹화: 상태별로 주문 목록
Map<OrderStatus, List<Order>> byStatus = orders.stream()
    .collect(groupingBy(Order::status));

// 2) 그룹화 + downstream: 상태별 주문 수
Map<OrderStatus, Long> countByStatus = orders.stream()
    .collect(groupingBy(Order::status, counting()));

// 3) 그룹화 + downstream + 매핑: 상태별 주문 ID 목록
Map<OrderStatus, List<Long>> idsByStatus = orders.stream()
    .collect(groupingBy(Order::status, mapping(Order::id, toList())));

// 4) 그룹화 + downstream + 필터링 + 매핑: 상태별 1000원 이상 주문의 합계
Map<OrderStatus, Integer> bigSumByStatus = orders.stream()
    .collect(groupingBy(
        Order::status,
        filtering(o -> o.amount() > 1000,
            summingInt(Order::amount))));
```

(2)~(4)의 두 번째 인자를 빼면 그냥 `groupingBy(classifier)` — 한 줄짜리 그룹화다. 거기에 downstream을 끼우면 그룹별로 다른 *집계*를 한다. 그 downstream 안에 또 `mapping`·`filtering`을 끼우면 그룹 안에서 또 다른 변환을 한다. *합성*된다. 이렇게 *작은 도구의 합성*으로 복잡한 집계를 표현하는 패턴은 함수형의 핵심 정신이다. 6장 끝에서 이 정신을 한 번 더 회수할 것이니 *잊지 말자*.

`teeing`은 Java 12에 들어온 흥미로운 도구다. 같은 Stream을 두 Collector에 *동시에* 흘려 결과를 하나로 합친다. 예전에는 Stream을 두 번 만들거나 한 번에 두 가지를 누적할 수단이 마땅치 않았다.

```java
// 평균과 합계를 한 번에
record SumAvg(int sum, double avg) {}

SumAvg result = orders.stream()
    .collect(teeing(
        summingInt(Order::amount),
        averagingInt(Order::amount),
        SumAvg::new));
```

같은 일을 `summarizingInt`로 한 번에 받을 수도 있지만, `teeing`은 *임의의* 두 Collector를 합칠 수 있다는 점에서 더 일반적이다. "그룹화 + 전체 합계"처럼 분류와 비분류가 섞이는 자리에서 자주 빛난다.

여기까지가 `Collectors`의 표면이다. 카탈로그가 풍부하다. 그러나 우리가 이 도구를 *직접 만들 수 있는가*는 다른 질문이다.

## `Collector`를 직접 만들어보자

`Collectors`의 정적 팩토리는 결국 `Collector` 인터페이스를 구현한 객체를 돌려준다. 그 인터페이스의 모양을 한 번 들여다보자.

```java
public interface Collector<T, A, R> {
    Supplier<A> supplier();
    BiConsumer<A, T> accumulator();
    BinaryOperator<A> combiner();
    Function<A, R> finisher();
    Set<Characteristics> characteristics();
}
```

다섯 가지 부품이다. *5요소*라고 부르자. 의미를 하나씩 따라가보면 의외로 단순하다.

- **`supplier`**: 누적할 *컨테이너*를 새로 만든다. `() -> new ArrayList<>()` 같은 것이다.
- **`accumulator`**: 컨테이너에 원소 하나를 더한다. `(list, elem) -> list.add(elem)` 같은 것이다.
- **`combiner`**: 두 부분 컨테이너를 *합친다*. 병렬 처리에서 분할된 결과를 모을 때 쓴다.
- **`finisher`**: 최종 컨테이너를 *결과*로 변환한다. 변환이 없으면 항등 함수.
- **`characteristics`**: `CONCURRENT`, `UNORDERED`, `IDENTITY_FINISH` 같은 힌트.

직접 `toList`를 만들어보자. 간단한 손맛이다.

```java
Collector<Order, List<Order>, List<Order>> toListManual = Collector.of(
    ArrayList::new,                         // supplier
    List::add,                              // accumulator
    (left, right) -> { left.addAll(right); return left; },  // combiner
    Collector.Characteristics.IDENTITY_FINISH
);

List<Order> result = orders.stream().collect(toListManual);
```

`Collector.of(...)`는 5요소 중 `finisher`가 항등이면 생략할 수 있는 편의 메서드다. 위 코드의 `IDENTITY_FINISH` 힌트는 "최종 변환이 필요 없다, 누적 컨테이너가 곧 결과다"를 알려주는 것이다. 그 힌트를 본 Stream 구현은 마지막 단계를 건너뛴다.

조금 더 흥미로운 예를 만들어보자. *주문 금액의 중앙값*을 구하는 Collector. 표준 `Collectors`에 없는 자리다.

```java
public static Collector<Order, ?, OptionalInt> medianAmount() {
    return Collector.of(
        ArrayList<Integer>::new,
        (list, order) -> list.add(order.amount()),
        (a, b) -> { a.addAll(b); return a; },
        amounts -> {
            if (amounts.isEmpty()) return OptionalInt.empty();
            Collections.sort(amounts);
            int n = amounts.size();
            return OptionalInt.of(n % 2 == 1
                ? amounts.get(n / 2)
                : (amounts.get(n / 2 - 1) + amounts.get(n / 2)) / 2);
        }
    );
}

OptionalInt median = orders.stream().collect(medianAmount());
```

`finisher`가 비어 있지 않다. 누적은 ArrayList로 모으되, *마지막에* 정렬해 중앙값을 뽑는다. 이 자리에는 `IDENTITY_FINISH`를 주면 안 된다. 누적 타입(`List<Integer>`)과 결과 타입(`OptionalInt`)이 다르기 때문이다.

`combiner`가 왜 필요한지도 이 자리에서 *체감*해보자. sequential에서는 `combiner`가 호출되지 않을 수도 있다. 그러나 같은 코드를 `parallelStream`으로 돌리면 Stream은 데이터를 잘라 부분별로 누적한 뒤 `combiner`로 합친다. 그래서 `combiner`가 비어 있거나 결합 법칙을 깨면 parallel에서 결과가 흔들린다. *반드시* 두 부분 컨테이너의 합치는 의미가 "전체에 차례로 누적한 것"과 같아야 한다.

여기까지 오면 `Collectors`의 정적 팩토리들이 그렇게 마법이 아니라는 것을 알게 된다. 사람이 만들 수 있는 5요소의 조합이다. 우리에게 *합성* 가능한 작은 부품을 손에 쥐어준 것이다.

## `reduce`의 세 가지 시그니처 — 다시

5장에서 `reduce`의 세 시그니처를 잠깐 봤다. 6장에서 한 번 더 들여다보자. 이번에는 *수학적* 자리에 집중해서.

```java
// (1) Optional<T> reduce(BinaryOperator<T> op)
// (2) T reduce(T identity, BinaryOperator<T> op)
// (3) <U> U reduce(U identity, BiFunction<U, ? super T, U> accumulator, BinaryOperator<U> combiner)
```

(1)은 identity가 없다. 원소가 0개일 때 누적의 "기본값"이 없으므로 `Optional`을 돌려준다. (2)는 identity가 있다. 그래서 원소가 0개라도 결과는 identity. (3)은 누적 타입과 원소 타입이 다르다. 그래서 accumulator와 combiner가 분리된다.

이 세 시그니처의 등 뒤에 *monoid*라는 추상이 있다. monoid란 다음 두 조건을 만족하는 (T, ⊕, id)의 묶음이다.

- **identity**: 모든 `x`에 대해 `x ⊕ id == x` 이며 `id ⊕ x == x`
- **associativity**: 모든 `a`, `b`, `c`에 대해 `(a ⊕ b) ⊕ c == a ⊕ (b ⊕ c)`

(정수, +, 0)은 monoid다. (문자열, concat, "")도 monoid다. (집합, ∪, ∅)도 monoid다. (정수, *, 1)도 monoid다. 이 셋은 `reduce`에 그대로 넣어 sequential·parallel 모두에서 정확히 같은 결과를 준다. 그러나 (정수, -, 0)은 monoid가 *아니다*. 뺄셈은 결합 법칙이 깨진다. `(5 - 3) - 1 = 1`이지만 `5 - (3 - 1) = 3`. parallel에서 이걸 `reduce`에 넣으면 분할 위치에 따라 결과가 달라진다.

왜 이 추상이 중요할까? **monoid는 parallel safety의 수학적 기반이다.** 데이터를 어떻게 자르든 부분 결과를 어떤 순서로 합치든, 결과가 같으려면 결합 법칙이 필요하다. 빈 조각이 결과를 바꾸지 않으려면 identity가 필요하다. 그래서 `reduce`의 시그니처가 우리에게 identity와 combiner를 요구하는 것이다. JLS도 비슷한 톤으로 말한다 — `java.util.stream` 패키지 문서의 "Associativity" 절은 한 페이지를 통째로 이 요구사항에 쓴다.

여기서 한 발 더 나가면 `Collector`의 5요소가 *fold의 일반화*임을 보게 된다. fold란 함수형 세계의 가장 근본 도구로, "초기값 + 결합 함수로 컬렉션을 단일 값으로 접는 일"이다. Haskell의 `foldr`·`foldl`, Scala의 `foldLeft`·`foldRight`, JavaScript의 `reduce` — 모두 같은 모양이다. 자바의 `reduce`도 그 한 종이다.

그러면 `Collector`는? `Collector`도 *fold다*. 단지 누적 컨테이너를 *가변*으로 두고, `combiner`로 부분 컨테이너를 합치며, 마지막에 `finisher`로 변환을 허락한다. 가변 누적을 허용하면 `ArrayList::add` 같은 *효율적인* 누적이 가능해진다. 매번 새 리스트를 만들지 않아도 된다. 이게 자바가 함수형의 추상을 *JVM 위에서* 실용적으로 옮긴 자리다. 순수 함수형 언어가 immutable 누적을 고집한다면, 자바는 mutable container를 인정하되 "thread-safe하게 합치는 의무"를 `combiner`에 요구한다. 깔끔한 절충이다.

## Gatherer — 닫혀 있던 중간 자리가 열리다

이제 이 장의 봉우리다. Java 22에서 preview로 들어와 Java 24에서 표준화된 `Stream::gather`다.

`Collector`가 *종단*의 일반화였다면, `Gatherer`는 *중간 연산*의 일반화다. 그동안 우리가 `filter`·`map`·`flatMap`만으로는 표현할 수 없었던 모든 패턴 — 1:1, 1:N, N:1, N:N 변환 — 을 사용자가 직접 만들 수 있게 됐다.

`Gatherer` 인터페이스의 모양을 한 번 보자.

```java
public interface Gatherer<T, A, R> {
    Supplier<A> initializer();
    Integrator<A, T, R> integrator();
    BinaryOperator<A> combiner();
    BiConsumer<A, Downstream<? super R>> finisher();
}

@FunctionalInterface
public interface Integrator<A, T, R> {
    boolean integrate(A state, T element, Downstream<? super R> downstream);
}
```

`Collector`와 비슷하면서도 다르다. 비교해두자.

| | `Collector` | `Gatherer` |
|---|---|---|
| 입력 | Stream의 원소 `T` | 같음 |
| 누적 상태 | `A` (가변 컨테이너) | `A` (필요 시 상태) |
| 출력 | 단일 결과 `R` | downstream으로 *여러* `R` 흘리기 |
| 합치기 | `combiner` (parallel) | `combiner` (parallel) |
| 마무리 | `finisher: A → R` | `finisher: A, downstream → void` |

핵심 차이는 `integrator`다. `Collector`의 `accumulator`는 컨테이너에 원소를 *담는다*. `Gatherer`의 `integrator`는 원소를 받아 downstream에 *0개부터 N개까지* 내보낸다. 1:1이면 `map`처럼, 0:1이면 `filter`처럼, 1:N이면 `flatMap`처럼 동작한다. 게다가 상태를 들고 있을 수 있어 *N:1*도 *N:N*도 자연스럽다. 슬라이딩 윈도우가 마침내 한 줄로 풀린다.

또 한 가지, `integrator`는 `boolean`을 돌려준다. `false`를 돌려주면 *short-circuit*. Stream이 그 자리에서 멈춘다. `takeWhile`·`limit`의 일반화다.

## 내장 Gatherer 4종

먼저 자바가 기본으로 제공하는 Gatherer를 한 바퀴 돌자. `java.util.stream.Gatherers` 정적 팩토리에 다음 넷이 들어 있다(JDK 24 기준).

| Gatherer | 용도 |
|----------|------|
| `windowFixed(size)` | 고정 크기로 잘라 List 시퀀스로 |
| `windowSliding(size)` | 슬라이딩 윈도우 List 시퀀스로 |
| `fold(init, fn)` | 누적합 *단일* 결과 |
| `scan(init, fn)` | 누적합 *각 단계* 결과 |
| `mapConcurrent(max, fn)` | 동시성 제한 매핑 |

(JEP 461·473·485의 진화를 따라가면 이름이 살짝씩 다듬어졌다. 일부 자료는 `mapConcurrent`를 다섯 번째로 별도 분류하기도 한다. 본문에서는 활용 자리 위주로 다섯을 같이 다룬다.)

먼저 `windowFixed`부터 보자.

```java
List<List<Order>> batches = orders.stream()
    .gather(Gatherers.windowFixed(100))
    .toList();
```

원소를 100개씩 잘라 List들의 List로 만든다. 마지막 배치가 100개에 못 미치면 그대로 짧은 List로 들어온다. 한때 이 일을 IntStream과 subList로 우회하던 *번거로움*을 생각하면 한 줄이 *후련하다*.

`windowSliding`은 5분 이동 평균의 자리다.

```java
List<Double> movingAvg = txns.stream()
    .gather(Gatherers.windowSliding(5))
    .map(window -> window.stream().mapToInt(Txn::amount).average().orElse(0))
    .toList();
```

`windowSliding(5)`는 슬라이딩 윈도우다. `[t1, t2, t3, t4, t5]`, `[t2, t3, t4, t5, t6]`, `[t3, t4, t5, t6, t7]` ... 이렇게 한 칸씩 이동한다. 그 위에 평균 계산을 `map`으로 얹는다. 도입에서 *번거로워하던* 자리가 두 줄에 풀린다. 11년 동안 우회해야 했던 자리다.

`fold`와 `scan`의 차이를 한 번 짚자. 둘 다 누적이지만, `fold`는 마지막 *단일* 결과를 흘리고, `scan`은 *매 단계*의 누적값을 흘린다.

```java
// fold: 총 잔액의 최종값 하나
Optional<Long> total = transactions.stream()
    .gather(Gatherers.fold(() -> 0L, (acc, t) -> acc + t.amount()))
    .findFirst();

// scan: 매 거래 후의 잔액 시퀀스
List<Long> balances = transactions.stream()
    .gather(Gatherers.scan(() -> 0L, (acc, t) -> acc + t.amount()))
    .toList();
```

`scan`은 prefix sum, 누적 카운터, 누적 잔액에 정확히 들어맞는다. 그동안 이 패턴을 `for-loop`이나 `IntStream.range` 우회로 풀던 자리다. 이제 한 줄로 표현된다.

`mapConcurrent`는 *rate-limited* 매핑이다.

```java
List<Result> results = userIds.stream()
    .gather(Gatherers.mapConcurrent(10, id -> restClient.callUserService(id)))
    .toList();
```

최대 10개의 호출만 동시에 진행하면서, 외부 서비스를 비동기로 호출한다. 5장에서 *끔찍한 일*이라고 했던 `parallelStream`의 blocking I/O 자리를, `mapConcurrent`는 *통제 가능한* 동시성으로 바꿔준다. JDK 21+의 virtual thread 위에서 도는 구현이라, 블로킹 호출을 비교적 안전하게 흘릴 수 있다. (다만 production에서는 별도 executor·timeout·circuit breaker를 결합하는 편이 안전하다.)

## Gatherer를 직접 만들어보자

내장 Gatherer로 안 풀리는 자리가 한 번씩 있다. 한 가지 예를 손으로 짜보자 — *키 기준 중복 제거*. `distinct`는 원소 자체의 equality로 중복을 본다. 우리는 "같은 user_id가 처음 등장하는 원소만 통과"시키고 싶다.

```java
public static <T, K> Gatherer<T, ?, T> distinctBy(Function<T, K> keyFn) {
    return Gatherer.ofSequential(
        HashSet<K>::new,                              // initializer
        (set, element, downstream) -> {               // integrator
            if (set.add(keyFn.apply(element))) {
                return downstream.push(element);      // 처음 본 키만 흘림
            }
            return true;                              // 계속 진행
        }
    );
}

List<Order> uniqueByUser = orders.stream()
    .gather(distinctBy(Order::userId))
    .toList();
```

상태로 `HashSet<K>`를 들고 다닌다. `integrator`가 원소를 받을 때마다 키를 추출해 set에 추가를 *시도*한다. 새 키면 set이 `true`를 돌려주고, 그 원소를 downstream에 push한다. 이미 본 키면 push하지 않고 그냥 `true`를 반환해 다음 원소를 받는다.

`Gatherer.ofSequential`을 쓴 이유는 이 Gatherer가 *순서에 의존*하기 때문이다 — "처음 본 키"라는 개념은 순서 없이는 정의되지 않는다. 그래서 parallel에서 안전하지 않다. parallel-safe하려면 `Gatherer.of`로 `combiner`를 같이 넘겨야 한다.

조금 더 어려운 예를 가보자 — *N:1로 묶기*. 같은 user_id가 연속으로 나오면 한 묶음으로 만든다.

```java
public static <T, K> Gatherer<T, ?, List<T>> groupConsecutiveBy(Function<T, K> keyFn) {
    record State<T, K>(List<T> buffer, K currentKey) {}

    return Gatherer.ofSequential(
        () -> new Object[] { new ArrayList<T>(), null },
        (state, elem, downstream) -> {
            @SuppressWarnings("unchecked")
            List<T> buf = (List<T>) state[0];
            Object prevKey = state[1];
            K key = keyFn.apply(elem);

            if (buf.isEmpty() || Objects.equals(prevKey, key)) {
                buf.add(elem);
                state[1] = key;
                return true;
            }
            // 키가 바뀌었다: 지금까지의 묶음을 흘리고 새 묶음 시작
            List<T> flushed = List.copyOf(buf);
            buf.clear();
            buf.add(elem);
            state[1] = key;
            return downstream.push(flushed);
        },
        (state, downstream) -> {                       // finisher
            @SuppressWarnings("unchecked")
            List<T> buf = (List<T>) state[0];
            if (!buf.isEmpty()) downstream.push(List.copyOf(buf));
        }
    );
}
```

`finisher`까지 쓴다. 스트림이 끝났는데도 버퍼에 남아 있는 묶음이 있다면 마지막에 한 번 더 흘려야 하기 때문이다. 이 자리가 `Collector`의 `finisher`와는 미묘하게 다르다 — Gatherer의 `finisher`는 결과를 *돌려주는* 것이 아니라 downstream에 *흘리는* 것이다. 흘릴 수도 있고 안 흘릴 수도 있다. 0개부터 N개까지 자유롭다.

코드가 좀 답답하다고 느꼈을 것이다. `Object[]`로 상태를 들고 다니는 자리가 *찜찜하다*. 이건 자바가 mutable lambda capture를 못 하는 데서 오는 한계다 — 람다는 effectively final만 캡처할 수 있어서 상태를 갱신하려면 컨테이너에 담아야 한다. 5장에서 람다와 함께 짚었던 자리다. JDK 25 시점에서는 이게 여전히 일반적인 패턴이다. record로 만들어 atomic update를 쓰면 조금 더 깔끔해지지만, 본질적 *번거로움*은 남는다.

## 함수형 관점 — fold, composition, monad-ish patterns

여기까지 5요소의 `Collector`와 4요소의 `Gatherer`를 봤다. 두 도구가 비슷한 모양을 한 이유, 그리고 `reduce`까지 다 같은 가족이라는 사실 — 이것을 *함수형의 큰 그림*에서 한 번 정리하자.

### 모든 것은 fold다

먼저 `reduce`. 시그니처 (2) `T reduce(T identity, BinaryOperator<T> op)`는 정확히 monoid 위의 fold다. monoid가 보장되면 sequential·parallel 결과가 같다.

다음 `collect`. `Collector`의 5요소는 *가변 누적 fold*다. 누적 컨테이너에 `accumulator`로 원소를 담고, `combiner`로 부분 컨테이너를 합치며, 마지막에 `finisher`로 결과를 변환한다. fold의 일반화에 불과하다.

마지막 `gather`. `Gatherer`의 `integrator`는 fold의 step function인데, downstream에 *여러 개*를 흘릴 수 있도록 일반화된 것이다. 0개를 흘리면 filter, 1개를 흘리면 map, N개를 흘리면 flatMap, 누적해서 모았다가 한 번에 흘리면 windowing. 모두 *같은* 추상의 다른 모습이다.

그래서 자바 함수형의 자리에 도구가 셋이라는 사실이 아니라, *같은 fold가 세 가지 자리에 자기 모양을 잡았다*고 보는 편이 정확하다. 이 시야를 한 번 갖고 나면, 새 도구를 마주칠 때마다 "이건 fold의 어느 모습인가"를 묻게 된다. 다음 자바가 또 새 추상을 들고 오면, 그것도 fold의 모습으로 들어올 가능성이 높다.

### composition — 작은 부품의 결합

함수형의 두 번째 정신은 *합성*이다. `Collector`는 이미 그것을 보여줬다. `groupingBy(classifier, mapping(mapper, filtering(predicate, summingInt(toInt))))` — 작은 도구가 차례로 *합성*된 것이다. 각각은 단순하다. 그러나 결합된 의미는 풍부하다.

`Gatherer`도 같은 정신을 따른다. `gatherer.andThen(another)`로 두 Gatherer를 합칠 수 있다. Java 24 기준 시그니처는 다음과 같다.

```java
default <RR> Gatherer<T, ?, RR> andThen(Gatherer<? super R, ?, RR> that) { ... }
```

앞 Gatherer가 흘린 원소를 뒷 Gatherer가 받아 다시 처리한다. *파이프라인*이 한 줄로 합성된다.

```java
Gatherer<Txn, ?, Double> movingAvg5 =
    Gatherers.<Txn>windowSliding(5)
        .andThen(Gatherer.ofSequential(
            () -> null,
            (state, window, downstream) ->
                downstream.push(window.stream().mapToInt(Txn::amount).average().orElse(0))
        ));

List<Double> result = txns.stream().gather(movingAvg5).toList();
```

`windowSliding`이 List를 흘리고, 그 List를 받아 평균을 계산해 다시 흘린다. 이 합성된 Gatherer는 *재사용 가능한* 부품이 된다. 결제 분석, 모니터링, 트래픽 통계 — 5분 이동 평균이 필요한 모든 자리에 한 줄로 들어간다.

`Function::andThen`·`Function::compose`도 같은 정신이다. 3장에서 람다 합성을 짚었다. 모든 합성이 동일한 모양을 한다는 사실이 *기억해둘* 자리다.

### monad-ish patterns — flatMap의 형식

세 번째 정신은 *monad*다. 정확한 정의는 카테고리 이론의 영역이라 책 한 권으로도 부족하지만, 우리가 마주치는 자바의 자리에서는 한 가지 *형식*으로 충분하다.

```
M<A> + (A -> M<B>) -> M<B>
```

이 형식은 어디서 본 적이 있는가? `Stream::flatMap`이 정확히 이 모양이다.

```java
Stream<A> + (A -> Stream<B>) -> Stream<B>
```

7장에서 자세히 볼 `Optional::flatMap`도 같은 모양이다.

```java
Optional<A> + (A -> Optional<B>) -> Optional<B>
```

`CompletableFuture::thenCompose`도 같다.

```java
CompletableFuture<A> + (A -> CompletableFuture<B>) -> CompletableFuture<B>
```

그래서 이 셋을 *대충* monad라고 부른다. 정확하게는 모나드 법칙(left identity, right identity, associativity)을 자바 타입 시스템이 강제하지 못하고, 사용자가 그것을 깨도 컴파일러가 막지 못한다. 그러나 의도와 형식은 monad다. 7장에서 Brian Goetz가 "Optional은 모나드가 아니다, 그러나 모나드처럼 쓸 수 있는 자리들이 있다"라고 한 발 물러난 말을 다시 만나게 될 텐데, 그 말의 정확한 결이 이것이다.

이 형식을 알아두면 무엇이 좋은가? *체인*이 자연스럽게 보인다. null-check 사다리, exception-catch 사다리, callback 사다리 — 모두 같은 자리에 들어가는 같은 패턴이라는 시야가 생긴다. 어떤 컨텍스트(`Optional`, `Stream`, `Future`) 안에 값이 있고, 그 값을 다른 컨텍스트로 변환하는 함수가 있다면, `flatMap`이 답이다. 7장의 핵심이 거기 있다.

## Java 8 collector 지옥 vs Java 24 gatherer

이 장의 도입을 다시 떠올리자. 5분 이동 평균을 Stream으로 구하는 자리. Java 8에서 같은 일을 어떻게 했는지 한 번 비교해보자.

```java
// Java 8 — 슬라이딩 윈도우를 IntStream.range로 우회
List<Double> movingAvg = IntStream.range(0, txns.size() - 4)
    .mapToObj(i -> txns.subList(i, i + 5))
    .map(window -> window.stream().mapToInt(Txn::amount).average().orElse(0))
    .collect(Collectors.toList());

// Java 24 — windowSliding 한 줄
List<Double> movingAvg = txns.stream()
    .gather(Gatherers.windowSliding(5))
    .map(window -> window.stream().mapToInt(Txn::amount).average().orElse(0))
    .toList();
```

겉으로 보면 코드 줄 수가 비슷하다. 그러나 *의도*의 거리는 멀다. Java 8 버전은 "인덱스를 굴려 부분 리스트를 만든다"는 *명령*이다. Java 24 버전은 "슬라이딩 윈도우를 만든다"는 *선언*이다. 어느 쪽이 자명한지 한 번 동료에게 보여보자. PR 리뷰에서 "이게 정확히 뭐 하는 코드죠?"라는 질문이 나오는 빈도가 정확히 절반이 된다.

게다가 Java 8 버전은 Stream의 원본이 List가 *아니면* 그대로 깨진다. `txns`가 `Stream<Txn>`이거나 `Iterable<Txn>`이라면 `subList`가 없다. Java 24 버전은 그것을 신경 쓰지 않는다 — Gatherer가 *상태*로 윈도우를 관리한다.

또 다른 예 — *prefix sum*도 비교해보자.

```java
// Java 8 — 외부 변수 캡처로 우회
AtomicLong acc = new AtomicLong();
List<Long> cumulative = transactions.stream()
    .map(t -> acc.addAndGet(t.amount()))
    .collect(Collectors.toList());

// Java 24 — scan 한 줄
List<Long> cumulative = transactions.stream()
    .gather(Gatherers.scan(() -> 0L, (acc, t) -> acc + t.amount()))
    .toList();
```

Java 8 버전은 *지긋지긋한* 패턴이다. `AtomicLong`을 외부에 두고 람다에서 그것을 *변경*한다. 5장의 non-interference 원칙을 정확히 어긴다. sequential에서는 어쩌다 돌지만, parallel에서는 결과가 깨진다. 함수형 코드의 *옷*을 입었지만 정신은 명령형이다. *찜찜하다*. Java 24 버전은 상태를 Gatherer 내부에 *캡슐화*한다. 외부에는 효과가 새지 않는다. 같은 코드를 `parallelStream`에 태우는 것도 가능하다(scan은 sequential 의미가 강해 실효는 따로 따져야 하지만, 적어도 형식적 안전은 다르다).

이 비교가 11년의 자바 함수형 진화를 한 자리에 응축한다. 람다 → Stream → Collector → Gatherer. 한 발씩 더 *추상*으로 옮겨가면서, 사용자 정의의 자리를 점점 더 *문법적으로* 열어줬다. 그 끝이 어디인지는 아직 모른다. 그러나 한 가지는 분명하다. 자바는 더 이상 "함수형이 아닌 언어"가 아니다. *함수형 자바*라는 별도의 부분 언어가 자바 안에 자리 잡았다.

## Spring 맥락 — 배치 인서트와 윈도우 집계

마지막으로 실무 자리를 한 번 짚자. JDBC batch insert다. JPA·MyBatis·JDBC Template 모두 한 번의 트랜잭션에 묶을 배치 크기를 적당히 둬야 한다. 너무 작으면 round-trip이 많아 느리고, 너무 크면 메모리 폭증과 oracle/MySQL의 packet 크기 한계에 부딪친다. 보통 100~1000 사이다.

전통적 패턴은 다음과 같았다.

```java
int batchSize = 1000;
int i = 0;
for (Order order : orders) {
    em.persist(order);
    if (++i % batchSize == 0) {
        em.flush();
        em.clear();
    }
}
em.flush();
em.clear();
```

명령형이다. 인덱스를 굴리고, 모듈로 연산을 하고, 마지막에 잊지 않고 flush·clear를 한 번 더 한다. 이 마지막 한 줄을 *잊어버리면* 마지막 999개가 안 들어간다. *번거롭다*. 이걸 Gatherer로 다듬으면 다음과 같이 된다.

```java
orders.stream()
    .gather(Gatherers.windowFixed(1000))
    .forEach(batch -> {
        batch.forEach(em::persist);
        em.flush();
        em.clear();
    });
```

`windowFixed(1000)`이 1000개씩 알아서 묶어주고, 마지막 batch가 1000개 미만이면 그것대로 흘려준다. *반드시 마지막 flush를 잊지 말자*는 잔소리가 사라진다. JDBC batch size 설정과 정확히 정합되도록 윈도우 크기를 맞추면, ORM 레이어와 드라이버 레이어가 한 박자로 움직인다.

또 다른 자리 — 결제 트랜잭션의 시간 윈도우 집계. 모니터링 대시보드에서 "최근 5분간 결제 실패율"을 실시간으로 내고 싶다고 해보자.

```java
Map<Boolean, Long> failureRate = paymentEvents.stream()
    .gather(Gatherers.windowSliding(300))  // 5분 = 300초 가정
    .map(window -> window.stream()
        .collect(Collectors.partitioningBy(PaymentEvent::isFailed, Collectors.counting())))
    .reduce((a, b) -> b)  // 마지막 윈도우
    .orElse(Map.of(true, 0L, false, 0L));
```

`windowSliding`이 윈도우를 흘리고, 각 윈도우에서 `partitioningBy`로 성공/실패를 분리해 count한다. 마지막 윈도우의 결과가 *현재 시점*의 성공·실패율이다. 한때 이 코드를 손으로 짜면 한 페이지가 넘던 자리다. 이제 다섯 줄에 들어온다.

물론 production에서는 시간 정확도(이벤트 시간 vs 처리 시간), 늦게 도착하는 이벤트, 윈도우 경계 정렬 같은 정밀한 자리를 더 신경 써야 한다. Flink·Kafka Streams 같은 진짜 스트림 프로세서가 그 자리에 있다. Gatherer는 *프로세스 내부의* 배치/스트림 처리에 어울리는 도구이고, *분산 스트림 처리*의 대체는 아니다. 그러나 사내 분석 도구, 모니터링 보고서, 정기 배치 — 그런 자리에서는 Gatherer 한 줄이 한때 짊어졌던 *지긋지긋한* 코드의 무게를 완전히 덜어준다.

## 마무리

`Collector`는 종단 연산의 일반화고, `Gatherer`는 중간 연산의 일반화다. 5요소의 `Collector`와 4요소의 `Gatherer`는 *fold라는 같은 추상*의 다른 모습이다. 합성 가능하고, 재사용 가능하고, 사용자 정의가 자유롭다. 11년 동안 *지긋지긋했던* 슬라이딩 윈도우·prefix sum·rate-limited 매핑이 한 줄로 풀린다.

monoid를 한 번 *기억해두자*. identity와 associativity가 parallel safety의 수학적 기반이다. monad-ish 형식 `M<A> + (A -> M<B>) -> M<B>`도 *기억해두자*. 그 형식이 `Stream`, `Optional`, `CompletableFuture`에서 모두 같은 자리에 등장한다.

이제 그 형식이 다음 장의 무대로 그대로 옮겨간다. `Optional<T>`다. NPE의 명시화로 출발한 이 작은 컨테이너가 어떻게 monad-ish 패턴의 한 자리를 차지하게 됐는지, 그리고 그 자리에서 우리가 어떤 *함정*에 자주 빠지는지를 다음 장에서 살펴보자. `user.getAddress().getCity().getZip()`의 NPE를 처음 만난 그날을 한 번 떠올리며.
