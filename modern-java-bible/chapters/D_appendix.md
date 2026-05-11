# 부록 D. Java 8 vs 25 코드 패턴 30선

같은 일을 하는 코드가 11년 사이에 어떻게 바뀌었는가. 30개의 짝을 모아두었다. 본문이 *왜*와 *어떻게*를 다뤘다면, 이 부록은 *눈으로 직접 보는 변화*다. 한 페이지에 두 코드를 나란히 두고, 짧은 메모로 *무엇이 달라졌는가*만 짚었다.

읽는 법은 자유롭다. 처음부터 30개를 훑어도 되고, 본문 어느 챕터를 읽다가 *오, 이게 8 시절엔 어떻게 썼지?* 싶을 때 인덱스로 와도 된다. 패턴마다 본문 챕터 참조를 달아두었다.

코드는 *최소한*으로 줄였다. import문·boilerplate는 생략했고, 변화의 *핵심*만 보이도록 잘랐다. 실제 production 코드는 더 길지만, 짧은 짝이 11년의 차이를 더 잘 드러낸다.

---

## D.1 함수형의 기본

### 1. 즉시 함수 표현 — anonymous → lambda (3장)

```java
// Java 8 이전
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        System.out.println("clicked");
    }
});

// Java 8+
button.addActionListener(e -> System.out.println("clicked"));
```

5줄이 한 줄로. *function as value*가 자바에 들어온 순간이다.

---

### 2. 컬렉션 필터링 — for-loop → Stream.filter (5장)

```java
// Java 8 이전
List<Order> result = new ArrayList<>();
for (Order o : orders) {
    if (o.amount() > 1000) {
        result.add(o);
    }
}

// Java 25
List<Order> result = orders.stream()
    .filter(o -> o.amount() > 1000)
    .toList();
```

명령형(*어떻게*)에서 선언형(*무엇*)으로. `.toList()`(Java 16+)가 `Collectors.toList()`를 대체한 부분도 챙겨두자.

---

## D.2 데이터 모델

### 3. DTO 정의 — class → record (11장)

```java
// Java 8 (Lombok 없이)
public final class OrderRequest {
    private final String customerId;
    private final BigDecimal amount;
    private final Instant orderedAt;

    public OrderRequest(String customerId, BigDecimal amount, Instant orderedAt) {
        this.customerId = customerId;
        this.amount = amount;
        this.orderedAt = orderedAt;
    }

    public String getCustomerId() { return customerId; }
    public BigDecimal getAmount() { return amount; }
    public Instant getOrderedAt() { return orderedAt; }

    @Override public boolean equals(Object o) { /* ... */ }
    @Override public int hashCode() { /* ... */ }
    @Override public String toString() { /* ... */ }
}

// Java 25
public record OrderRequest(
    String customerId,
    BigDecimal amount,
    Instant orderedAt
) {}
```

30줄이 한 줄로. record는 *Lombok 없이도* equals·hashCode·toString·accessor를 모두 자동 생성한다.

---

### 4. 다중 결과 — Pair 클래스 → record (11장)

```java
// Java 8 (Pair는 표준 라이브러리에 없음)
public class MinMax {
    public final int min;
    public final int max;
    public MinMax(int min, int max) { this.min = min; this.max = max; }
}
return new MinMax(min, max);

// Java 25
record MinMax(int min, int max) {}
return new MinMax(min, max);
```

매번 Pair 클래스를 새로 만들 필요가 없다. local record(메서드 안에서 선언 가능)는 *이름 있는 튜플*로 쓰면 가독성이 크게 올라간다.

---

### 5. 도메인 합 타입 — Visitor 패턴 → sealed + pattern (12·13장)

```java
// Java 8 — Visitor 패턴
interface Expr {
    <R> R accept(Visitor<R> v);
    interface Visitor<R> {
        R visit(Num n);
        R visit(Add a);
    }
}
class Num implements Expr { /* ... */ }
class Add implements Expr { /* ... */ }

// Java 25
sealed interface Expr permits Num, Add {}
record Num(int v) implements Expr {}
record Add(Expr l, Expr r) implements Expr {}

int eval(Expr e) {
    return switch (e) {
        case Num(int v) -> v;
        case Add(Expr l, Expr r) -> eval(l) + eval(r);
    };
}
```

Visitor 패턴의 *boilerplate*가 통째로 사라진다. 새 케이스 추가 시 컴파일러가 *누락된 분기*를 알려주니, double dispatch가 필요 없다.

---

## D.3 null 안전성

### 6. NPE 안전 체인 — null 체크 → Optional (7장)

```java
// Java 8 이전
String city = null;
if (order != null) {
    Address a = order.getAddress();
    if (a != null) {
        city = a.getCity();
    }
}

// Java 25
String city = Optional.ofNullable(order)
    .map(Order::address)
    .map(Address::city)
    .orElse(null);
```

`if-null-then` 사다리가 한 줄 체인으로. 단, 7장에서 짚었듯이 *과사용*은 오히려 가독성을 해친다 — *반환값 표현*에 한정하는 게 권장이다.

---

### 7. 옵셔널 풀기 — if not null → Optional.ifPresent (7장)

```java
// Java 8 이전
User u = repo.find(id);
if (u != null) {
    notify(u);
}

// Java 9+
repo.findById(id).ifPresent(this::notify);
```

`ifPresent`·`ifPresentOrElse`(Java 9+)로 *값이 있을 때만* 동작을 한 줄로 표현.

---

## D.4 시간·문자열

### 8. 시간 처리 — Date + SimpleDateFormat → java.time (4장)

```java
// Java 8 이전
Date now = new Date();
SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");
String s = fmt.format(now);

// Java 25
LocalDate today = LocalDate.now();
String s = today.format(DateTimeFormatter.ISO_LOCAL_DATE);
```

`SimpleDateFormat`은 thread-safe가 아니다. `DateTimeFormatter`는 immutable·thread-safe. `java.time`(JSR-310)은 Java 8의 *가장 큰 보석* 중 하나다.

---

### 9. 다중 라인 문자열 — String 연결 → text block (10장)

```java
// Java 8
String json =
    "{\n" +
    "  \"name\": \"Toby\",\n" +
    "  \"age\": 42\n" +
    "}";

// Java 15+
String json = """
    {
      "name": "Toby",
      "age": 42
    }
    """;
```

JSON·SQL·HTML 리터럴이 *읽기 좋아진다*. incidental whitespace는 자동 제거(JLS §3.10.6) — 인용 박스 한 페이지가 10장에 있다.

---

### 10. 로컬 타입 선언 — 정식 타입 → var (10장)

```java
// Java 8
Map<String, List<Order>> ordersByCustomer = new HashMap<>();

// Java 10+
var ordersByCustomer = new HashMap<String, List<Order>>();
```

타입 추론(LVTI, JEP 286)으로 좌변 반복을 줄인다. 단, *읽는 사람이 추론 가능할 때*만 권장한다.

---

## D.5 컬렉션 · Stream

### 11. 컬렉션 생성 — Arrays.asList → List.of (5장)

```java
// Java 8
List<String> names = Arrays.asList("Alice", "Bob");
// 또는
List<String> names = Collections.unmodifiableList(
    Arrays.asList("Alice", "Bob"));

// Java 9+
List<String> names = List.of("Alice", "Bob");
```

`List.of`는 *처음부터 immutable*. `Arrays.asList`는 *고정 크기지만 mutable*(`set`은 가능, `add`는 불가). 의미가 다르다.

---

### 12. Stream collect — Collectors.toList → toList() (5장)

```java
// Java 8
List<String> upper = words.stream()
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// Java 16+
List<String> upper = words.stream()
    .map(String::toUpperCase)
    .toList();
```

`.toList()`는 *unmodifiable* 결과를 돌려준다. mutable이 필요하면 여전히 `Collectors.toList()`를 쓴다.

---

### 13. groupingBy — 수동 코드 → Collectors.groupingBy (5·6장)

```java
// Java 8 이전
Map<String, List<Order>> byCustomer = new HashMap<>();
for (Order o : orders) {
    byCustomer.computeIfAbsent(o.customerId(), k -> new ArrayList<>()).add(o);
}

// Java 25
Map<String, List<Order>> byCustomer = orders.stream()
    .collect(Collectors.groupingBy(Order::customerId));
```

선언적인 표현이 *의도*를 더 빨리 드러낸다. `groupingBy`는 downstream collector와 조합해 *합계·평균·세는* 작업도 자연스럽다.

---

### 14. 슬라이딩 윈도우 — 수동 loop → Stream Gatherer (6장)

```java
// Java 8
List<List<Integer>> windows = new ArrayList<>();
for (int i = 0; i + 3 <= numbers.size(); i++) {
    windows.add(new ArrayList<>(numbers.subList(i, i + 3)));
}

// Java 24+
List<List<Integer>> windows = numbers.stream()
    .gather(Gatherers.windowSliding(3))
    .toList();
```

Stream Gatherer(JEP 485)가 마침내 자바에서 슬라이딩 윈도우를 *한 줄로* 표현하게 했다. `windowFixed`·`fold`·`scan`·`mapConcurrent`도 같은 패키지에 있다.

---

### 15. teeing — 두 Collector 결합 (6장)

```java
// Java 8
double sum = orders.stream().mapToDouble(Order::amount).sum();
long count = orders.stream().count();
double average = count == 0 ? 0 : sum / count;

// Java 12+
double average = orders.stream().collect(
    Collectors.teeing(
        Collectors.summingDouble(Order::amount),
        Collectors.counting(),
        (s, c) -> c == 0 ? 0 : s / c
    ));
```

스트림을 두 번 돌지 않고 *한 번에* 두 reduce를 동시에. 메모리도 한 번 만에 끝난다.

---

### 16. 컬렉션 마지막 요소 — size-1 → getLast (10장)

```java
// Java 8
String last = list.get(list.size() - 1);

// Java 21+
String last = list.getLast();
```

Sequenced Collections(JEP 431) — 21년 만의 List 보강. `getFirst`·`getLast`·`addFirst`·`addLast`·`reversed()` 모두 사용 가능.

---

## D.6 분기 · 패턴 매칭

### 17. 분기 — switch statement → switch expression (10장)

```java
// Java 8 — fall-through 위험
String label;
switch (status) {
    case ACTIVE:
        label = "활성";
        break;
    case INACTIVE:
        label = "비활성";
        break;
    default:
        label = "알 수 없음";
}

// Java 14+
String label = switch (status) {
    case ACTIVE -> "활성";
    case INACTIVE -> "비활성";
    default -> "알 수 없음";
};
```

`break` 누락으로 인한 *fall-through 버그*가 원천 차단. switch가 *값을 돌려주는 표현*이 됐다.

---

### 18. 캐스트 사다리 — instanceof + cast → instanceof pattern (13장)

```java
// Java 8
if (obj instanceof String) {
    String s = (String) obj;
    return s.length();
}

// Java 16+
if (obj instanceof String s) {
    return s.length();
}
```

type test와 binding을 융합. 캐스트가 사라지면서 *변수가 한 자리*에 정의된다.

---

### 19. exhaustive 분기 — default + throw → sealed exhaustive switch (12·13장)

```java
// Java 8
public String describe(Shape s) {
    if (s instanceof Circle) return "circle";
    if (s instanceof Square) return "square";
    throw new IllegalStateException("unknown: " + s);
}

// Java 21+
sealed interface Shape permits Circle, Square {}

public String describe(Shape s) {
    return switch (s) {
        case Circle c -> "circle";
        case Square q -> "square";
    };
}
```

sealed + exhaustive switch는 *새 케이스를 빠뜨리면 컴파일 에러*. throw 폴백이 필요 없다.

---

### 20. 도메인 이벤트 — Object 상속 → sealed interface (12장)

```java
// Java 8
public abstract class DomainEvent { }
public class OrderPlaced extends DomainEvent { /* ... */ }
public class OrderCancelled extends DomainEvent { /* ... */ }

// Java 25
public sealed interface DomainEvent
    permits OrderPlaced, OrderCancelled {}
public record OrderPlaced(String orderId) implements DomainEvent {}
public record OrderCancelled(String orderId, String reason) implements DomainEvent {}
```

*어떤 이벤트가 올 수 있는지* 컴파일러가 안다. pattern matching에서 exhaustiveness 보장.

---

## D.7 동시성

### 21. 비동기 조합 — Future.get → CompletableFuture chain (8B장)

```java
// Java 7
Future<String> f1 = exec.submit(() -> fetchUser(id));
Future<List<Order>> f2 = exec.submit(() -> fetchOrders(id));
String user = f1.get();  // blocking
List<Order> orders = f2.get();  // blocking
return new Profile(user, orders);

// Java 8+
CompletableFuture<String> u = CompletableFuture.supplyAsync(() -> fetchUser(id));
CompletableFuture<List<Order>> o = CompletableFuture.supplyAsync(() -> fetchOrders(id));
return u.thenCombine(o, Profile::new);
```

콜백 지옥 없이 비동기 결과를 *조합*한다.

---

### 22. 동시성 fan-out — CompletableFuture.allOf → Virtual Thread + StructuredTaskScope (14·16장)

```java
// Java 8
List<CompletableFuture<Result>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetch(id), executor))
    .toList();
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
List<Result> results = futures.stream().map(CompletableFuture::join).toList();

// Java 25 (StructuredTaskScope는 preview)
try (var scope = StructuredTaskScope.open()) {
    List<StructuredTaskScope.Subtask<Result>> tasks = ids.stream()
        .map(id -> scope.fork(() -> fetch(id)))
        .toList();
    scope.join();
    return tasks.stream().map(StructuredTaskScope.Subtask::get).toList();
}
```

자식 작업들의 *생명주기가 부모와 묶인다*. 부모가 종료되면 자식도 모두 정리. 16장 참조.

---

### 23. context 전달 — ThreadLocal → ScopedValue (15·16장)

```java
// Java 8
private static final ThreadLocal<String> USER_ID = new ThreadLocal<>();
USER_ID.set(userId);
try {
    processRequest();
} finally {
    USER_ID.remove();  // 깜빡하면 메모리 누수
}

// Java 25
private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();
ScopedValue.where(USER_ID, userId).run(() -> processRequest());
// 자동으로 unmount
```

ScopedValue(JEP 506)는 *bounded*·*immutable*. virtual thread 시대의 ThreadLocal 후임이다.

---

### 24. Virtual Thread 도입 — platform → virtual (14장)

```java
// Java 8
ExecutorService exec = Executors.newFixedThreadPool(200);
// platform thread 200개, 더 많은 동시 요청은 큐 대기

// Java 21+
ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor();
// 요청마다 virtual thread, 수백만 개 동시 가능
```

I/O-bound 워크로드에서 *thread-per-request*가 다시 합리적이 됐다.

---

## D.8 모듈 · 네트워킹

### 25. 모듈 의존성 — classpath → module-info (9장)

```java
// Java 8 — classpath 한 줄
// (별도 선언 없음, JAR 모두 visible)

// Java 9+
// module-info.java
module com.example.order {
    requires com.example.common;
    requires transitive java.sql;
    exports com.example.order.api;
}
```

전제 — 9장에서 짚었듯, JPMS는 *대부분의 애플리케이션이 도입하지 않은* 변화다. 라이브러리·도구 영역에서 부분적으로 사용된다.

---

### 26. HTTP 호출 — URLConnection → HttpClient (20·21장)

```java
// Java 8
URL url = new URL("https://api.example.com/order/42");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");
try (BufferedReader r = new BufferedReader(
        new InputStreamReader(conn.getInputStream()))) {
    String body = r.lines().collect(Collectors.joining("\n"));
    return body;
}

// Java 11+
HttpClient client = HttpClient.newHttpClient();
HttpRequest req = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/order/42"))
    .build();
HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
return res.body();
```

표준 API로 HTTP/2·WebSocket·동기/비동기 모두 지원. Apache HttpClient·OkHttp 의존성을 줄일 수 있다.

---

## D.9 직렬화 · 빌더

### 27. 직렬화 — Serializable → record + Jackson (11·20A장)

```java
// Java 8
public class OrderDto implements Serializable {
    private static final long serialVersionUID = 1L;
    private String id;
    private BigDecimal amount;
    /* getter/setter/equals/hashCode */
}

// Java 25
public record OrderDto(String id, BigDecimal amount) {}
// Jackson이 record를 native로 인식 (2.12+)
```

`Serializable`의 함정(보안 취약점·버전 호환성·hidden 의존성)을 피하고, JSON·CBOR 같은 *명시적* 직렬화로 이행하는 게 권장이다. 20A장 보안 절 참조.

---

### 28. 빌더 — Lombok @Builder → record + with-method (11장)

```java
// Java 8 (Lombok)
@Builder
public class OrderRequest {
    private String customerId;
    private BigDecimal amount;
}
OrderRequest req = OrderRequest.builder()
    .customerId("C1")
    .amount(BigDecimal.TEN)
    .build();

// Java 25 (without Lombok)
public record OrderRequest(String customerId, BigDecimal amount) {
    public OrderRequest withAmount(BigDecimal v) {
        return new OrderRequest(customerId, v);
    }
}
OrderRequest req = new OrderRequest("C1", BigDecimal.TEN);
OrderRequest updated = req.withAmount(BigDecimal.valueOf(100));
```

Lombok 의존을 줄이면서도 *immutable update*를 표현. with-method 패턴(record의 관용구)을 손수 또는 코드 생성 도구로 만들자.

---

## D.10 시작 시간 · 네이티브 · 도구

### 29. 시작 시간 단축 — 없음 → CDS + AOT (19장)

```java
// Java 8 — 별다른 옵션 없음
// $ java -jar app.jar
// (startup time: ~6초)

// Java 25 — AOT Class Loading
// $ java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -jar app.jar
// $ java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf -XX:AOTCache=app.aot -jar app.jar
// $ java -XX:AOTCache=app.aot -jar app.jar
// (startup time: ~3초, Spring Petclinic 기준 36~42% 단축)
```

JEP 483·514·515의 결실. GraalVM Native Image 없이도 *cold start* 문제를 완화한다.

---

### 30. 네이티브 호출 — JNI → FFM + jextract (18장)

```java
// Java 8 — JNI
// 1) Native.java
public native int add(int a, int b);
// 2) javac → javah → C 헤더 생성
// 3) C로 구현 → libnative.so
// 4) System.loadLibrary("native")

// Java 22+ — FFM
try (Arena arena = Arena.ofConfined()) {
    Linker linker = Linker.nativeLinker();
    SymbolLookup stdlib = linker.defaultLookup();
    MethodHandle strlen = linker.downcallHandle(
        stdlib.find("strlen").orElseThrow(),
        FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS));
    MemorySegment cString = arena.allocateUtf8String("Hello");
    long len = (long) strlen.invoke(cString);
}
```

JNI의 boilerplate·crash 위험·GC 충돌이 사라진다. `jextract`로 C 헤더 → 자바 바인딩 자동 생성도 가능. JNI 시대의 종료가 시작된 자리(JEP 454).

---

## D.11 *번외* — 한 줄짜리 자바 (10·19A장)

본 30선 밖이지만 *철학의 변화*를 보여주는 한 짝을 더 둔다.

```java
// Java 8 — 첫 줄에 30년 묵은 의례
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// Java 25 (JEP 512: Compact Source Files and Instance Main Methods)
void main() {
    IO.println("Hello, World!");
}
```

`public static void main(String[] args)`를 외우라고 한 30년이 25에서 끝났다. *입문자에게 자바가 마침내 친절해진* 자리다. 학습용·스크립트용으로 한정된 변화지만, 그 의미는 작지 않다.

---

## D.12 표 — 30선 한눈에

| # | 패턴 | 본문 |
|---|---|---|
| 1 | anonymous → lambda | 3장 |
| 2 | for-loop → Stream.filter | 5장 |
| 3 | class → record | 11장 |
| 4 | Pair → record | 11장 |
| 5 | Visitor → sealed + pattern | 12·13장 |
| 6 | null 체크 → Optional | 7장 |
| 7 | if not null → ifPresent | 7장 |
| 8 | Date → java.time | 4장 |
| 9 | String 연결 → text block | 10장 |
| 10 | 정식 타입 → var | 10장 |
| 11 | Arrays.asList → List.of | 5장 |
| 12 | Collectors.toList → toList() | 5장 |
| 13 | 수동 그룹 → groupingBy | 5·6장 |
| 14 | 수동 윈도우 → Gatherer | 6장 |
| 15 | 두 번 stream → teeing | 6장 |
| 16 | size-1 → getLast | 10장 |
| 17 | switch statement → expression | 10장 |
| 18 | instanceof + cast → pattern | 13장 |
| 19 | default + throw → sealed exhaustive | 12·13장 |
| 20 | Object 상속 → sealed interface | 12장 |
| 21 | Future.get → CompletableFuture | 8B장 |
| 22 | allOf → StructuredTaskScope | 14·16장 |
| 23 | ThreadLocal → ScopedValue | 15·16장 |
| 24 | platform thread → virtual | 14장 |
| 25 | classpath → module-info | 9장 |
| 26 | URLConnection → HttpClient | 20·21장 |
| 27 | Serializable → record + Jackson | 11·20A장 |
| 28 | @Builder → record + with | 11장 |
| 29 | 없음 → CDS + AOT | 19장 |
| 30 | JNI → FFM + jextract | 18장 |

---

## D.13 사용 안내

이 30선은 *마이그레이션 체크리스트*(부록 C)와 짝을 이룬다. 체크리스트가 *언제·어떤 순서로*를 알려준다면, 이 부록은 *코드가 어떻게 생기는가*를 보여준다. 둘을 함께 보자.

또 한 가지 — 모든 짝이 *바로 적용 가능*한 건 아니다. 8 → 25를 한 번에 점프하면 의존성·테스트·문화가 따라가지 못한다. 부록 C의 4단계(8 → 11 → 17 → 21 → 25)를 함께 보면서 *점진적*으로 옮기는 편이 낫다.

마지막으로 — *옛 코드가 무조건 나쁜 건 아니다*. 8 시절의 코드는 *그 시점에 합리적*이었다. 우리가 다시 쓴다면 25의 도구를 쓰는 게 자연스럽지만, *지금 잘 돌아가는 8 코드*를 무리해서 갈아엎을 필요는 없다. 새 기능을 *25 스타일로* 추가하고, 손이 갈 때마다 옛 자리를 *조금씩 정리*하는 게 11년의 변화를 *지속 가능하게* 흡수하는 방법이다.

11년의 변화를 한 권에 담아 보자고 시작한 책이, 마지막 부록까지 와서야 한 번에 30짝으로 압축됐다. 책을 덮고 코드 앞으로 돌아가, 이 30짝 중 하나라도 *오늘 한 줄* 옮겨보는 것 — 그게 이 책의 가장 좋은 마무리일 것이다.
