# 10장. `var`·switch·text blocks·Sequenced Collections — 작지만 결정적인 변화

사내 코드 리뷰에서 30자짜리 타입 선언을 매일 적던 동료가 어느 날 한 줄을 이렇게 적었다고 해보자.

```java
var orders = orderRepository.findRecentByCustomer(customerId, since);
```

옆자리 시니어가 어깨를 두드린다. "그 `var`, 가독성 떨어지지 않아? 반환 타입이 뭔지 안 보이잖아." 동료는 잠시 머뭇거리다 IDE의 hover로 타입을 보여준다. "`List<Order>`예요. 메서드 이름에 `findRecentByCustomer`라고 적혀 있고, 변수 이름도 `orders`잖아요."

이 1분짜리 코드 리뷰 안에 *언어 표면 진화의 모든 것*이 들어 있다. 자바는 30년간 *explicit*을 사랑해 온 언어다. 그 언어에 `var`가 들어왔을 때 우리가 느낀 *찜찜함*은 무엇이었나? 한편 같은 시기에 들어온 switch expression, text blocks, sequenced collections는 거의 *논쟁 없이* 받아들여졌다. 왜 같은 시기의 변화인데 환영의 폭이 달랐을까?

이 장에서는 8가지를 함께 살펴본다. `var`, switch expression, text blocks, Sequenced Collections, Markdown Javadoc, String Templates의 좌초, Compact Source / Instance Main, 그리고 마지막으로 — 이 모든 변화의 합주가 만들어내는 *코드의 색깔*까지. 14년치 일상 코드의 피로감을 덜어주는 작은 도구들이다. 하나씩 음미해보자.

## §10.1 `var` — 작아 보이는 변화의 진짜 크기

Java 10(2018, JEP 286)에서 `var`가 들어왔다. **LVTI**(Local Variable Type Inference)라는 이름이 붙은 이 기능은 *지역 변수*의 타입을 우변에서 추론하는 것이다.

```java
// Before
Map<String, List<Order>> ordersByStatus = new HashMap<>();

// After
var ordersByStatus = new HashMap<String, List<Order>>();
```

문법은 단순하다. 그러나 *어디에 쓸 수 있고, 어디에는 못 쓰는가*를 먼저 정확히 알아두자. `var`는 의도적으로 *좁게* 한정됐다. JLS의 표현을 정확히 보자.

> **JLS §14.4 (Local Variable Declaration)**
>
> *The `var` reserved type name appears only in local variable declarations with initializers, and in the formal parameters of implicitly typed lambda expressions.*
>
> 한국어 번역: "`var` 예약 타입 이름은 *초기화자가 있는 지역 변수 선언*과 *implicitly typed 람다 식의 formal parameter*에서만 사용한다."
>
> 의미 해설: `var`는 *지역*이라는 자리에 명시적으로 묶여 있다. 필드·메서드 시그니처·반환 타입에는 쓸 수 없다. 이는 우연한 제약이 아니라 의도적 한정이다 — *공개 API의 모양*은 컴파일러 추론에 맡겨선 안 된다는 자바 설계자들의 신중함이다.
>
> 본문 연결: 다음 문단에서 다룰 *어울리는 자리 / 어울리지 않는 자리*의 분기점이 바로 이 정의에서 흘러나온다.

쓸 수 있는 자리는 네 군데다. 지역 변수 선언, `for` 루프의 인덱스, `for-each` 루프의 변수, `try-with-resources`의 리소스 선언. 쓸 수 없는 자리는 그 외 전부 — 필드, 메서드 파라미터, 반환 타입, catch 변수, lambda parameter(단, Java 11부터 `(var x) -> ...`는 가능)다.

### `var`가 어울리는 자리

OpenJDK Amber 팀이 직접 만든 *LVTI Style Guide*가 있다. 거기서 권장하는 다섯 가지 자리를 살펴보자.

**첫째, 우변이 자명할 때.** `new HashMap<...>()` 같은 *생성자 호출*은 타입을 자기 안에 다 담고 있다. 좌변에 같은 정보를 한 번 더 적는 것은 *번거롭다*.

```java
var users = new ArrayList<User>();
var connection = DriverManager.getConnection(url);
```

**둘째, 변수 이름이 의도를 충분히 전달할 때.** `orders`라는 이름은 `List<Order>`임을 추론할 수 있는 충분한 단서다. `userMap`은 `Map<UserId, User>`다. 변수 이름이 타입을 노출하면 `var`로 충분하다.

**셋째, 스트림 파이프라인의 중간 변수.** Stream의 중간 결과 타입은 매우 길어진다(`Map<Integer, List<Order>>`처럼). 이걸 풀어 쓰면 한 줄이 80자를 넘는다.

```java
var ordersByYear = orders.stream()
    .collect(Collectors.groupingBy(o -> o.createdAt().getYear()));
```

**넷째, 익명 클래스를 받을 때.** 익명 클래스의 *실제* 타입은 익명이라 적을 수가 없다. `var`만이 그 타입을 보존한다.

```java
var counter = new Object() {
    int count = 0;
    void inc() { count++; }
};
counter.inc();  // 컴파일 OK. Object로 받았다면 불가능.
```

**다섯째, try-with-resources의 자원 변수.** 자원 변수의 타입은 거의 *open한 그 자리* 한 번만 쓴다.

```java
try (var conn = dataSource.getConnection();
     var stmt = conn.prepareStatement(sql)) {
    // ...
}
```

### `var`가 어울리지 않는 자리

반대로 *피해야 할* 자리도 분명하다.

**첫째, 우변이 모호할 때.** `var result = compute();`는 *끔찍하다*. `compute()`의 반환 타입을 IDE 없이는 알 수 없다. PR diff를 보는 동료도, 1년 뒤 같은 코드를 다시 보는 우리 자신도 — 그 자리에서 막힌다.

**둘째, 다이아몬드 연산자와 결합할 때.** `var list = new ArrayList<>();`는 컴파일은 되지만 *추론 결과가 `ArrayList<Object>`*다. 우리가 원한 건 아닐 것이다. 명시적으로 `new ArrayList<User>()`라고 적거나, 좌변에 타입을 적자.

**셋째, 숫자 리터럴.** `var x = 0;`은 `int`다. 그러나 `long`이나 `byte`를 원했다면 명시적으로 적는 편이 낫다.

**넷째, 다이아몬드와 익명 함수가 섞일 때.** `var f = (String s) -> s.length();`는 컴파일 에러다. 람다는 *target type*이 필요한데, `var`는 그걸 줄 수 없다.

**다섯째, 함수형 인터페이스 변환.** `var supplier = () -> 42;`도 같은 이유로 에러다. `Supplier<Integer> supplier = () -> 42;`처럼 명시해야 한다.

### Java 11의 람다 파라미터 `var`

Java 11에서 한 가지 작은 보완이 들어왔다. 람다 파라미터에도 `var`를 적을 수 있게 됐다(JEP 323).

```java
list.stream()
    .filter((var s) -> s.length() > 5)
    .toList();
```

왜 필요했을까. *애노테이션을 람다 파라미터에 붙이려면 타입이 있어야* 하기 때문이다. `@NonNull String s`처럼 적으려면 타입이 필요하다. 그런데 `var`도 타입의 자리에 올 수 있으므로, `(@NonNull var s) -> ...`가 가능해진 것이다. 자주 쓰는 기능은 아니지만, *문법의 일관성*을 위한 정리다.

### 가독성 — 도구의 문제인가, 문화의 문제인가

가독성 논쟁의 한가운데로 들어가보자. Java는 30년간 explicit 문화였다. 그 문화 안에서 자란 우리는 `var` 앞에서 *찜찜함*을 느낀다. 이 찜찜함은 정당한가?

JetBrains의 통계(IntelliJ IDEA 사용자 데이터)에 따르면, `var` 사용 비율은 매년 가파르게 늘고 있다. 신규 코드의 30~40% 가까이가 `var`로 작성된다는 조사도 있다. 한편 Java 공식 LVTI Style Guide는 다음을 강조한다.

> *Code is read much more often than it is written. Moreover, it is often read in contexts where the reader does not have ready access to an IDE.* (코드는 작성보다 훨씬 더 자주 읽힌다. 게다가 IDE 없이 읽히는 경우가 많다.)

이 문장의 무게가 크다. PR diff, GitHub 검색 결과, 콘솔 출력, 책에 실린 코드 스니펫 — 이 모든 자리에서 IDE는 없다. 코드는 *그 자체로 자명*해야 한다.

그러니 정리해보자. `var`는 *문법 설탕*이 아니라 *문화적 선택*이다. 팀이 코드 리뷰에서 매번 hover로 타입을 확인하는 일을 *번거롭다*고 느끼지 않는다면 — IDE가 충실히 깔려 있고, 변수 이름이 잘 쓰여 있다면 — `var`를 적극 활용하는 편이 낫다. 반대로 콘솔과 git blame에서 코드를 자주 읽는 팀이라면 explicit 타입이 *친절하다*. 어느 쪽이든, *왜 그렇게 쓰는지*에 대한 팀의 공통 이해가 있는 편이 좋다.

## §10.2 Switch Expression — 한 줄 안에 들어온 결정

Java 14(JEP 361)에서 switch가 *expression*이 됐다. 이전까지 switch는 *문장*(statement)이었다 — 값을 반환하지 못하고, 부수효과로만 동작했다. 이제 switch는 값을 *반환*한다.

```java
// Before — statement 형식
String name;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        name = "6 letters";
        break;
    case TUESDAY:
        name = "7 letters";
        break;
    default:
        name = "unknown";
}

// After — expression 형식
String name = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> "6 letters";
    case TUESDAY -> "7 letters";
    default -> "unknown";
};
```

차이가 보이는가. *세 가지*가 한꺼번에 바뀌었다.

**첫째, `case L ->` 화살표 문법.** 콜론(`:`) 대신 화살표(`->`)를 쓰면 fall-through가 사라진다. break를 쓸 필요가 없다. 자바 switch의 가장 끔찍한 버그 원천 중 하나가 *깜빡한 break*였는데, 그게 깔끔히 사라졌다.

**둘째, 다중 라벨.** `case MONDAY, FRIDAY, SUNDAY`처럼 라벨을 콤마로 묶을 수 있다. 옛 시절 빈 case를 줄줄이 쌓던 *번거로움*이 끝났다.

**셋째, expression.** 전체 switch가 *값*이다. `String name = switch (...) {...};`처럼 결과를 변수에 바로 담는다. 함수 인자로 넘기는 것도 자연스럽다.

복잡한 case에서 값을 계산해야 할 때는 블록 + `yield`를 쓴다.

```java
int days = switch (month) {
    case FEB -> {
        int d = year % 4 == 0 ? 29 : 28;
        yield d;
    }
    case APR, JUN, SEP, NOV -> 30;
    default -> 31;
};
```

`yield`는 *블록의 결과값*을 표현하는 키워드다. `return`이 아니라 `yield`인 이유 — `return`은 *메서드*에서 빠져나오는 것이고, `yield`는 *블록의 값*을 산출하는 것이다. 둘은 의미가 다르다.

JLS의 정의를 한 번 보자.

> **JLS §15.28 (Switch Expressions)**
>
> *A switch expression is a poly expression; if it appears in an assignment context or an invocation context, then the target type is used to determine the result type of the switch expression. ... A switch expression must be exhaustive.*
>
> 한국어 번역: "switch expression은 *poly expression*이다. 만약 그것이 *대입 컨텍스트*나 *호출 컨텍스트*에 나타난다면, target type이 switch expression의 결과 타입을 결정하는 데 사용된다. ... switch expression은 *exhaustive*해야 한다."
>
> 의미 해설: switch expression이 *값을 산출하는 식*이므로, 그것의 *결과 타입*은 문맥에 따라 다르게 결정된다. 더 중요한 것은 *exhaustive 요구*다 — 모든 가능한 입력 값이 어떤 case에 의해 매칭되어야 한다. enum이나 sealed type처럼 가능 값의 집합이 컴파일 타임에 알려진 경우, 컴파일러가 *빠진 case*를 잡아준다.
>
> 본문 연결: exhaustiveness는 다음 절의 디딤돌이다. 12장(sealed)과 13장(pattern matching)에서 본격적으로 다룰 *데이터 지향 프로그래밍*의 핵심 메커니즘이 바로 이 exhaustive switch다.

### 13장의 디딤돌

switch expression은 *그 자체로도 유용*하지만, 진짜 가치는 13장에서 드러난다. Java 21(JEP 441)에서 switch는 *pattern matching*까지 결합한다.

```java
String describe(Shape s) {
    return switch (s) {
        case Circle c -> "circle with radius " + c.radius();
        case Square sq when sq.side() > 100 -> "big square";
        case Square sq -> "small square";
        case Triangle t -> "triangle";
    };
}
```

`Shape`가 `sealed`라면 컴파일러가 *모든 sub-type을 다뤘는지*를 강제한다. enum의 exhaustiveness가 *유한한 값 집합*에 적용되던 것을, sealed type으로 일반화한 것이다. switch expression은 이 일반화의 *문법 기반*이다.

10장 단계에서 우리는 switch expression의 *형식*만 익혀도 충분하다. 그러나 그 형식이 *왜 그렇게 설계됐는지*는 13장에서 본격적으로 풀린다. 함께 기억해두자.

> **JLS §14.11 (The switch Statement)** 도 마지막에 짚어두자. switch *statement* 역시 화살표 문법을 쓸 수 있게 정리됐다. 즉, 자바의 switch는 이제 *네 가지 조합*이 있다 — statement 콜론, statement 화살표, expression 콜론(거의 안 씀), expression 화살표. 새 코드를 적을 때는 *expression 화살표*를 default로 두자. 옛 형식은 *옛 코드 유지보수*에서만 만나면 충분하다.

## §10.3 Text Blocks — 삼중 따옴표의 평화

Java 15(JEP 378)에서 text blocks가 표준화됐다. 멀티라인 문자열 리터럴이다.

```java
// Before
String sql = "SELECT id, name, email\n" +
             "FROM users\n" +
             "WHERE created_at > ?\n" +
             "  AND status = 'ACTIVE'\n" +
             "ORDER BY name";

// After
String sql = """
        SELECT id, name, email
        FROM users
        WHERE created_at > ?
          AND status = 'ACTIVE'
        ORDER BY name
        """;
```

훨씬 *읽기 좋다*. SQL을 SQL답게, JSON을 JSON답게, HTML을 HTML답게 적을 수 있다. 자바 코드 안에 *다른 언어*가 들어올 때마다 우리가 겪던 그 *번거로움*이 끝났다.

문법은 단순하다. `"""`로 열고 `"""`로 닫는다. 단, 열린 `"""` 다음에는 *반드시 줄바꿈*이 와야 한다. 닫는 `"""`의 위치가 *들여쓰기 기준*이 된다.

### incidental whitespace — 들여쓰기의 마법

text blocks의 진짜 묘미는 *들여쓰기 정규화*다. 위의 SQL 예제를 보자. `SELECT`, `FROM`, `WHERE`가 각각 *몇 칸 들여쓰기*되어 있는가? 8칸이다. 그런데 결과 문자열에는 그 8칸이 *없다*. 컴파일러가 알아서 제거했기 때문이다.

이게 *incidental whitespace 제거 알고리즘*이다. 정확한 규칙은 JLS에 있다.

> **JLS §3.10.6 (Text Blocks — Incidental White Space)**
>
> *The algorithm computes the minimum number of leading white space characters in each non-blank line of the content. The closing delimiter line, if non-empty, is also counted. The minimum is then stripped from every line.*
>
> 한국어 번역: "알고리즘은 컨텐츠의 *각 non-blank 줄에서 leading white space의 개수*를 센다. 닫는 delimiter 줄이 비어 있지 않다면 그것도 함께 센다. 그렇게 구한 *최솟값*을 모든 줄에서 제거한다."
>
> 의미 해설: 즉, 컴파일러는 모든 줄의 *공통 들여쓰기*를 찾아 떼어낸다. 닫는 `"""`의 들여쓰기가 *기준선*이 된다. 우리가 자바 코드 안에서 깔끔한 들여쓰기를 유지하면서도, 결과 문자열에는 그 들여쓰기가 묻지 않게 하기 위한 설계다.
>
> 본문 연결: 닫는 `"""`의 위치를 *얼마나 들여 쓸지*가 곧 *결과 들여쓰기의 기준*이다. 닫는 `"""`를 줄 맨 앞에 두면, 결과 문자열의 모든 줄이 그대로 들여쓰기를 보존한다. 닫는 `"""`를 컨텐츠보다 *더 들여쓰기*하면 컴파일 에러다.

직관적이지 않은 이 규칙을 머리에 그림으로 새겨두자. 닫는 `"""`의 자리가 *수직선*이고, 그 선 왼쪽의 공백은 *전부 제거*된다. 그 선 오른쪽의 공백은 *결과에 그대로 들어간다*.

### `\s`와 `\<newline>` — 두 가지 이스케이프

text blocks에는 두 가지 새 이스케이프가 들어왔다.

**`\s`** — 줄 끝의 공백을 *보존*한다. text blocks는 줄 끝의 trailing whitespace를 자동으로 제거하는데, 그게 의도가 아닐 때(예: 패딩 문자열) 마지막에 `\s`를 적어 공백을 보존한다.

**`\<newline>`** (줄바꿈 이스케이프) — 줄을 *합친다*. 긴 한 줄을 시각적으로 끊어 적되 결과 문자열에는 줄바꿈을 넣지 않고 싶을 때 쓴다.

```java
String url = """
        https://example.com/api/v1/users\
        ?page=1\
        &size=20\
        """;
// 결과: "https://example.com/api/v1/users?page=1&size=20"
```

### Spring 맥락 — `@Query`와 JdbcTemplate

text blocks가 *가장 빛나는 자리*가 어디일까. Spring Data JPA의 `@Query` 안 JPQL이다.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("""
        SELECT o FROM Order o
        JOIN FETCH o.items i
        WHERE o.customer.id = :customerId
          AND o.status = 'PAID'
          AND o.createdAt > :since
        ORDER BY o.createdAt DESC
        """)
    List<Order> findRecentPaidOrders(
        @Param("customerId") Long customerId,
        @Param("since") LocalDateTime since);
}
```

이게 Java 8 시절이면 `"SELECT o FROM Order o " + "JOIN FETCH o.items i " + ...` 같이 가독성이 떨어지는 *접합 표현*이었다. text blocks 한 번이면 *진짜 SQL처럼 보이는 JPQL*이 된다. JdbcTemplate의 native SQL도 마찬가지다. JPA를 쓰든 JdbcTemplate을 쓰든, text blocks가 *번거로움*을 덜어준다.

## §10.4 Sequenced Collections — 27년 묵은 누락의 마무리

자바 컬렉션 프레임워크는 1.2(1998)에 들어왔다. 그로부터 25년이 지나도록 *기본기 중 하나*가 빠져 있었다. 무엇인가?

`List<String>`의 *첫 원소*를 어떻게 가져왔는지 떠올려보자.

```java
String first = list.get(0);
String last = list.get(list.size() - 1);
```

`Deque`라면 `getFirst()`·`getLast()`가 있다. `SortedSet`이라면 `first()`·`last()`다. 그런데 `LinkedHashSet`이라면? `LinkedHashSet`은 *삽입 순서*를 보존하는데, 그 첫 원소를 가져오려면 — *iterator를 돌려야* 한다.

```java
String first = linkedHashSet.iterator().next();
```

*끝 원소*는 더 끔찍하다. iterator를 끝까지 돌리거나, `new ArrayList<>(set).get(set.size() - 1)`처럼 *임시 리스트로 변환*해야 한다. `LinkedHashMap`도 마찬가지다. 27년간 이렇게 살았다. 무언가 *찜찜한* 일이었다.

Java 21(JEP 431)에서 이 누락이 정리됐다. **Sequenced Collections**다. 세 개의 새 인터페이스가 들어왔다.

```java
public interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();
    void addFirst(E e);
    void addLast(E e);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}

public interface SequencedSet<E> extends Set<E>, SequencedCollection<E> { ... }
public interface SequencedMap<K, V> extends Map<K, V> { ... }
```

그리고 기존 구현 클래스들이 이 인터페이스를 *retrofit*했다. `ArrayList`, `LinkedList`, `ArrayDeque`, `LinkedHashSet`, `LinkedHashMap` — 모두가 `SequencedCollection`(또는 `SequencedSet`/`SequencedMap`)이 됐다.

```java
var list = new ArrayList<>(List.of("a", "b", "c"));
list.getFirst();    // "a"
list.getLast();     // "c"
list.addFirst("z"); // [z, a, b, c]
list.reversed();    // [c, b, a, z] — 새 뷰

var linkedSet = new LinkedHashSet<>(List.of("x", "y", "z"));
linkedSet.getFirst();  // "x"
linkedSet.getLast();   // "z"

var linkedMap = new LinkedHashMap<String, Integer>();
linkedMap.put("a", 1);
linkedMap.put("b", 2);
linkedMap.firstEntry();  // a=1
linkedMap.lastEntry();   // b=2
```

`reversed()`도 흥미롭다. *역순 뷰*를 돌려준다 — 새 컬렉션이 아니라, 원본의 *역순 시점*이다. 메모리를 새로 안 쓴다.

```java
for (var x : list.reversed()) {
    // 마지막 원소부터 순회
}
```

작은 변화지만, *27년 묵은 어색함*이 사라졌다는 사실이 의미 있다. 이 작은 정리가 27년이 걸린 이유는 — *기존 구현의 호환성을 깨지 않으면서 인터페이스 계층을 다시 짜는 일*이 매우 어렵기 때문이다. JPMS의 strong encapsulation 덕분에 JDK 내부 재설계가 자유로워졌다는 9장의 이야기와 연결된다. 함께 기억해두자.

## §10.5 Markdown Javadoc — `///`의 등장

Java 23(JEP 467)에서 작은 도구 변화가 들어왔다. Markdown Javadoc이다. 기존 `/** ... */` 형식의 HTML Javadoc 대신, `///` 세 줄 슬래시로 *Markdown* 주석을 쓸 수 있다.

```java
/// Calculates the area of a circle.
///
/// **Formula:** `π × r²`
///
/// Example:
/// ```java
/// double area = circle(5);  // 78.539...
/// ```
///
/// @param radius radius of the circle, must be non-negative
/// @return the area
public static double circle(double radius) {
    return Math.PI * radius * radius;
}
```

기존 HTML 형식과 비교해보자.

```java
/**
 * Calculates the area of a circle.
 *
 * <p><b>Formula:</b> <code>π × r²</code></p>
 *
 * <p>Example:</p>
 * <pre>{@code
 * double area = circle(5);  // 78.539...
 * }</pre>
 *
 * @param radius radius of the circle, must be non-negative
 * @return the area
 */
```

훨씬 *친근하다*. GitHub, README, 블로그에서 우리가 매일 쓰는 Markdown 문법 그대로다. `<p>`, `<b>`, `<code>`, `<pre>{@code ...}`를 일일이 적던 *번거로움*이 사라졌다.

두 형식은 *공존*한다. 기존 HTML Javadoc은 그대로 동작하고, 새 Markdown 주석은 javadoc 도구가 자동으로 파싱한다. 옛 코드를 강제로 옮길 필요는 없다. 다만 새로 적는 주석은 Markdown 형식이 *편하다*고 느껴진다면 그쪽으로 옮겨가는 편이 낫다.

IDE 도구도 따라오는 중이다. IntelliJ IDEA 2025.1부터, Eclipse 2025-09부터 Markdown Javadoc을 정식 지원한다. 한 가지 *잊지 말자* — `///`는 *세 줄*이다. `//`(주석)나 `////`(잘못된 형식)와 헷갈리지 말자.

## §10.6 String Templates의 좌초사

조심히 다룰 주제다. 한 번 들어왔다가 *철회*된 기능이다. String Templates는 JEP 430(Java 21 preview), 459(Java 22 preview)로 등장했다가, Java 23에서 *철회*됐다.

원래 의도는 좋았다.

```java
// 의도된 문법 (좌초된 디자인)
String name = "Toby";
int age = 41;
String message = STR."Hello, \{name}, you are \{age} years old.";
```

`STR.` prefix를 붙여 *문자열 안의 표현식*을 평가하는 디자인이었다. JavaScript의 template literal, Python의 f-string, Kotlin의 `${}`와 비슷한 아이디어다.

그런데 왜 좌초했을까. 두 가지 큰 이유가 있다.

**첫째, prefix 문법의 어색함.** `STR.` 같은 *템플릿 프로세서 prefix*가 직관적이지 않다. 다른 언어들은 `f"..."`(파이썬)이나 `${}`(Kotlin)처럼 *문법 한 줄*로 표현하는데, 자바는 *메서드 호출처럼* 보이는 prefix를 두었다. "이게 왜 필요한가?"라는 물음에 충분히 답하지 못했다.

**둘째, 보안 디자인의 충돌.** 자바 설계자들은 String Templates를 *SQL injection 안전한 문자열 조립*의 도구로 쓰고 싶었다. `STR` 외에 `RAW`, `FMT` 같은 다른 프로세서를 두고, 사용자가 *직접 안전한 프로세서를 만들 수 있게* 했다. 그러나 그 일반성 때문에 *기본 사용법*이 복잡해졌다. "그냥 문자열 보간을 쓰고 싶었을 뿐인데, 왜 ProcessorFactory를 이해해야 하지?"라는 불만이 쌓였다.

Java 23 시점에서 Brian Goetz는 String Templates를 *원점에서 재설계*하기로 결정했다. 향후 새 디자인이 나올 때까지, 자바는 *문자열 보간이 없는 언어*로 남는다. `String.format`, text blocks, `+` 연산자가 여전히 우리의 도구다.

> **메타 메시지로서의 String Templates의 좌초사:** preview 단계가 *왜* 있는지를 보여주는 정직한 사례다. preview는 *피드백을 받기 위한 단계*이고, 받은 피드백이 부정적이면 *철회*가 가능하다. 자바 설계자들이 이런 결단을 내릴 수 있다는 사실 자체가 자바 생태계의 건강함을 보여준다. records가 14에서 16으로 *순항*했고, switch가 12에서 14로 *순항*했지만, String Templates는 21·22를 거쳐 *물러섰다*. 모든 preview가 표준화되지는 않는다. 22장에서 향후 재설계 동향을 더 추적한다.

## §10.7 Compact Source Files — 자바의 진입 장벽 낮추기

Java 25(JEP 512)에서 *Compact Source Files and Instance Main Methods*가 표준화됐다. 입문자 친화 개선이다.

전통적인 Hello World는 이렇다.

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

이걸 자바를 처음 배우는 사람에게 한 줄씩 설명하려면 — `public`이 뭔지, `class`가 뭔지, `static`이 뭔지, `void`가 뭔지, `String[] args`가 뭔지를 다 알려야 한다. 자바에 *처음 발 디딘* 사람이 첫 줄을 적기까지 *5개의 개념*을 미리 알아야 했다. *난감한 일*이다.

JEP 512가 이걸 풀었다.

```java
void main() {
    println("Hello, World!");
}
```

이게 *유효한 자바 프로그램*이다. `java HelloWorld.java` 한 줄로 실행된다. 클래스 선언도, `public static`도, `String[] args`도 없다. `println`은 *implicitly imported* — `java.lang.IO.println`이 자동으로 임포트된다.

JEP 511(Module Import Declarations)과 결합하면 *스크립트 같은 자바*가 가능하다.

```java
import module java.base;

void main() {
    var list = List.of("a", "b", "c");
    var map = Map.of("a", 1, "b", 2);
    println(list);
    println(map);
}
```

엔터프라이즈에서는 거의 안 쓴다. 그러나 *자바를 처음 배우는 학생*, *작은 스크립트를 자바로 적고 싶은 개발자*에게 이 변화의 의미는 크다. Python·Ruby·JavaScript가 매력적이었던 이유 중 하나가 *진입 장벽이 낮음*이었는데, 자바도 그 자리에 발을 들였다.

엔터프라이즈 개발자라면 *동료에게 자바를 가르칠 때*만 만나는 도구로 두자. 그래도 *그 자리가 있다*는 것을 기억해두자.

## §10.8 같은 함수의 변천사 — Java 8 vs Java 21

이 장의 마무리는 *같은 함수*를 Java 8과 Java 21로 두 번 적어 비교해보는 일이다. 한 컨트롤러 메서드를 가정해보자. 사용자의 최근 주문을 받아 상태별로 그룹핑하고, JSON으로 직렬화해 응답을 만든다.

**Java 8 시절의 코드:**

```java
@GetMapping("/users/{userId}/orders")
public ResponseEntity<String> getOrders(@PathVariable Long userId) {
    Map<OrderStatus, List<Order>> ordersByStatus =
        orderService.findRecentOrders(userId).stream()
            .collect(Collectors.groupingBy(Order::getStatus));

    String json = "{\n" +
                  "  \"userId\": " + userId + ",\n" +
                  "  \"groups\": [\n";
    for (Map.Entry<OrderStatus, List<Order>> entry : ordersByStatus.entrySet()) {
        OrderStatus status = entry.getKey();
        List<Order> orders = entry.getValue();
        String statusLabel;
        switch (status) {
            case PAID:
                statusLabel = "결제완료";
                break;
            case SHIPPED:
                statusLabel = "배송중";
                break;
            case DELIVERED:
                statusLabel = "배송완료";
                break;
            default:
                statusLabel = "기타";
        }
        json += "    { \"status\": \"" + statusLabel +
                "\", \"count\": " + orders.size() + " },\n";
    }
    json += "  ]\n}";
    return ResponseEntity.ok(json);
}
```

`Map.Entry<OrderStatus, List<Order>>`라는 *26자짜리 타입*을 매번 적는다. switch는 *6줄*에 걸쳐 4개의 case를 처리한다. JSON은 `+ "\n" +`로 한 줄씩 접합한다. *번거롭고*, *읽기 어렵고*, *수정하기 끔찍하다*.

**Java 21 스타일로 옮기면:**

```java
@GetMapping("/users/{userId}/orders")
public ResponseEntity<String> getOrders(@PathVariable Long userId) {
    var ordersByStatus = orderService.findRecentOrders(userId).stream()
        .collect(Collectors.groupingBy(Order::status));

    var groups = ordersByStatus.entrySet().stream()
        .map(entry -> {
            var statusLabel = switch (entry.getKey()) {
                case PAID -> "결제완료";
                case SHIPPED -> "배송중";
                case DELIVERED -> "배송완료";
                default -> "기타";
            };
            return """
                    { "status": "%s", "count": %d }""".formatted(statusLabel, entry.getValue().size());
        })
        .collect(Collectors.joining(",\n    "));

    var json = """
            {
              "userId": %d,
              "groups": [
                %s
              ]
            }""".formatted(userId, groups);

    return ResponseEntity.ok(json);
}
```

같은 일을 하는데 *길이가 줄고, 들여쓰기 결이 살고, switch가 결정 식으로 깔끔해졌다*. `var`가 타입 노이즈를 줄였고, switch expression이 분기를 한 식으로 압축했고, text blocks가 JSON을 진짜 JSON처럼 보이게 했다. 14년치 코드의 피로감이 *조금* 덜어진다.

여기에 13장에서 다룰 *pattern matching*까지 결합하면, switch 부분이 다시 한 번 더 깔끔해진다. 그건 다음 호로 미루자.

## 정리 — 작은 변화가 만드는 색깔

이 장에서 살펴본 도구들을 한자리에 모아보자.

- **`var` (Java 10):** 지역 변수 타입 추론. 우변이 자명할 때 *번거로움*을 덜어준다. *문화적 선택*이므로 팀의 공통 이해가 중요하다.
- **switch expression (Java 14):** 화살표 문법 + 다중 라벨 + expression 형태. fall-through 버그가 사라지고, 결정을 *한 식*으로 표현할 수 있게 됐다. 13장 pattern matching의 디딤돌.
- **text blocks (Java 15):** 삼중 따옴표 멀티라인 문자열. SQL·JSON·HTML이 *진짜 그 모양으로* 보인다. JLS §3.10.6의 incidental whitespace 알고리즘이 들여쓰기를 자동 정규화한다.
- **Sequenced Collections (Java 21):** 27년 묵은 누락이 마무리됐다. `getFirst`·`getLast`·`addFirst`·`addLast`·`reversed`가 모든 *순서 있는 컬렉션*에 자연스럽게 들어왔다.
- **Markdown Javadoc (Java 23):** `///` 세 줄 슬래시로 Markdown 주석. HTML Javadoc과 *공존*한다.
- **String Templates (좌초):** preview 단계의 자정 사례. 한 번 들어왔다가 철회된 보기 드문 경우다. 22장에서 향후 동향 추적.
- **Compact Source / Instance Main (Java 25):** `void main()` 한 줄로 자바 프로그램. 입문자 친화. 엔터프라이즈에서는 거의 안 쓰지만 자바의 진입 장벽 낮추기.

이 도구들의 공통점은 — *각각 하나만 보면 작다*. `var` 하나, switch expression 하나, text blocks 하나 — 어느 것도 자바의 패러다임을 바꾸지는 않는다. 그러나 *모이면 코드의 색깔이 달라진다*. 같은 일을 하는 함수가 30% 짧아지고, 들여쓰기가 살아나고, 결정이 식으로 압축된다. 14년치 일상 코드의 *피로감*이 줄어든다.

그리고 이 색깔의 변화가 — 11장에서 본격적으로 만날 *records*와, 12장의 *sealed*, 13장의 *pattern matching*과 결합하면 — 자바가 *데이터지향 언어*로 다시 태어난다. 표면의 진화는 *깊이의 진화*로 가는 다리다. 함께 다음 장으로 넘어가보자. Records가 우리를 기다리고 있다.
