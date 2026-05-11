# 22장. Valhalla · Amber · Babylon · Leyden — 26 이후의 자바

PayBridge의 5년 뒤 코드를 상상해 보자.

2030년의 어느 평범한 화요일이다. PayBridge는 이제 가맹점 수십만 개를 처리하는 동남아 최대 결제 미들레이어가 됐다. 사내 LTS는 *Java 30*이다. 결제 컨트롤러는 21장에서 본 그 코드의 *5년 뒤 버전*이다. 도메인 모델은 여전히 record와 sealed로 적혀 있는데, 자세히 들여다보면 한 가지가 달라졌다. record 앞에 `value`라는 키워드가 붙어 있다. `Optional<T>`도 value class가 됐다. 정산 배치는 GPU에서 도는데, 그 코드를 자바로 직접 적었다. JNI도, CUDA도, Python bridge도 없다. 그리고 콜드 스타트가 *400ms*다.

이 풍경이 *그럴듯해* 보이는가? 그렇다면 좋은 신호다. 1장에서 그린 PayBridge의 11년 코드 변천 이야기를 *5년 뒤*로 연장해 보자. 그 5년 동안 자바는 무엇을 했을까. *자바는 어디까지 갈까?* 이 책의 마지막 장에서, 26 이후의 자바가 어떤 모양으로 만들어지고 있는지 함께 살펴보자.

> **이 장의 disclaimer — 시점 명시**
>
> 이 책이 인쇄되는 시점(2026년 5월)을 기준으로 *알려진* 26 이후의 모습을 정리한다. **JEP 401 (Value Classes and Objects)**, Project Valhalla, Project Amber, Project Babylon, Project Leyden 모두 *진행 중*이다. 이 글에 적힌 어휘, 키워드, 일정은 변할 수 있다. 특히 String Templates가 21·22 preview를 거쳐 23에서 *철회*되고 재설계 중인 사례에서 보듯이, OpenJDK의 *preview 단계 자정*은 자주 일어난다. 이 장은 *방향*을 읽는 자료이지, *확정된 스펙*이 아니다. 인쇄 이후의 최신 상태는 OpenJDK 공식 페이지(`openjdk.org/projects/valhalla`, `openjdk.org/projects/amber`, `openjdk.org/projects/babylon`, `openjdk.org/projects/leyden`)에서 확인하자.

## Project Valhalla — primitive와 reference의 *통합*

먼저 가장 오래 기다린 프로젝트부터 살펴보자. Project Valhalla는 2014년 *책의 출발점인 Java 8과 같은 해*에 시작됐다. 그동안 자바 진영의 거의 모든 발표에서 한 번씩은 언급됐고, 그때마다 *조금만 더*라는 말이 따라왔다. 11년이 지난 지금, Valhalla는 마침내 가시 거리에 들어왔다. **JEP 401: Value Classes and Objects** — Java 26 preview 타깃으로 예고되어 있다.

Valhalla가 풀려는 문제가 무엇인가? *primitive와 reference의 분리*다. Java 8에서 `int`와 `Integer`의 차이를 처음 만난 신입 개발자가 *난감해했던* 그 자리다. `int`는 메모리에 4바이트로 *납작하게* 박혀 있다. `Integer`는 객체라 헤더 16바이트 + 값 4바이트 + 정렬 패딩까지, 한 개당 *수십 배 무거운* 신원을 갖는다. 그래서 `List<Integer>` 천만 개는 *수백 메가바이트의 heap*을 먹는다. `int[]` 천만 개는 40MB짜리 *연속 메모리*다.

11년 동안 이 *찜찜함*을 우회로 살아왔다. Stream API에 `IntStream`이 따로 있는 이유, `Optional`이 `OptionalInt`·`OptionalLong`을 따로 가진 이유, generics에 primitive를 못 쓰는 이유 — 전부 같은 한 가지 *분리*에서 나온 비용이다.

### value class — 객체이되 신원이 없다

Valhalla의 답은 **value class**다. 객체처럼 메서드를 갖고, 다형성에 참여하고, generics에 쓸 수 있다. 그런데 *신원(identity)*이 없다. 신원이 없다는 게 무슨 뜻인가?

```java
// JEP 401 — 가상의 미래 자바 코드
value class Point {
    private final double x;
    private final double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double distance(Point other) {
        double dx = x - other.x;
        double dy = y - other.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}
```

`value` 키워드 하나가 붙었다. 이 한 키워드가 무엇을 약속하는가?

- **immutable.** 모든 필드가 final.
- **identity 없음.** `==` 비교가 *값 비교*다. `new Point(1, 2) == new Point(1, 2)`가 *true*다.
- **`synchronized` 불가능.** 신원이 없으니 모니터 락을 걸 곳이 없다.
- **null-restricted 가능.** `Point!` 같은 타입으로 *null이 들어올 수 없음*을 표현.
- **flat memory layout 가능.** JVM이 객체 헤더를 *제거*하고 필드를 *납작하게* 박을 수 있다.

이 네 번째와 다섯 번째가 결정적이다. JVM은 value class를 *primitive처럼* 다룰 권리를 얻는다. 호출 스택에 박을 수도 있고, `Point[]`를 *연속 메모리*로 둘 수도 있고, `Optional<Point>`를 *value class끼리의 flat 객체*로 둘 수도 있다.

PayBridge의 결제 코드를 떠올려 보자. `Money` 타입을 record로 만들었던 적이 있다.

```java
public record Money(BigDecimal amount, String currency) {}
```

평범한 record다. 그러나 결제 시스템에서 `Money`는 *수십억 개* 만들어진다. 거래 한 건이 끝나면 garbage collected되지만, 그 사이 GC가 *지긋지긋하게* 돌아간다. value class가 들어오면 — 그리고 BigDecimal이 언젠가 value class로 옮겨가면 — 같은 코드가 *primitive 수준의 효율*로 돈다. 코드를 *한 글자도 바꾸지 않고* 그렇게 된다 (혹은 `value record Money(...)` 한 줄 변경으로).

### null-restricted types

여기서 한 걸음 더 나간 카드가 있다. **null-restricted types**다.

```java
// 가상의 미래 자바
value class Point {
    private final double x;
    private final double y;
    // ...
}

void plot(Point! p) {        // null이 들어올 수 없음
    System.out.println(p.x() + "," + p.y());
}

void maybePlot(Point? p) {    // null 들어올 수 있음
    if (p != null) plot(p);
}
```

`!`와 `?`는 *예고된 어휘*다. 확정 문법은 아니다. 그러나 방향은 분명하다 — *NullPointerException이 컴파일 시점에 거의 사라진다*. 7장에서 `Optional<T>`로 우회했던 그 모든 *난감한* 자리가, 언어 차원에서 정리된다.

Kotlin과 비교하지 않을 수 없다. Kotlin은 처음부터 `String`과 `String?`을 구분했다. 자바가 11년 늦었지만, *호환성을 깨지 않고* 같은 일을 해낸다 — 이게 자바답다. 옛 코드는 그대로 돌고, 새 코드는 새 약속을 얻는다.

### frozen arrays

또 하나 짚어야 할 카드가 있다. **frozen array**다. 자바의 array는 mutable이다. `int[] arr`을 받은 메서드가 안에서 값을 바꿔 버릴 수 있다. 그래서 immutable한 데이터를 표현하려고 `List.copyOf(...)`로 한 번 더 감싸는 *번거로움*이 따라왔다.

```java
// 가상의 미래 자바
int[] data = {1, 2, 3, 4, 5};
int!frozen[] view = data.freeze();
// view[0] = 99; // 컴파일 에러
```

frozen array는 *읽기 전용* 약속을 array 자체에 박는다. value class array와 결합하면 — `Money!frozen[]` 같은 표현이 — *완벽한 immutable + flat memory*의 자리를 만든다. 함수형 자바의 가장 *번거롭던* 자리가 정리된다.

### Valhalla가 흔드는 표면들

Valhalla가 정식화되면 자바 전반이 흔들린다. 흔들리는 자리를 헤아려 보자.

- **`Optional<T>`이 value class로 옮겨감.** 박싱 비용이 사라진다. `OptionalInt`·`OptionalLong`이 *불필요해진다*.
- **`Integer`·`Long`·`Double` 등 wrapper가 value class로 재정의됨.** 호환성을 유지하면서 박싱 비용 소멸.
- **`Stream<Integer>`와 `IntStream`의 *분리 이유 자체가 사라짐*.** 11년 동안 두 길로 갈라져 있던 API가 자연 통합.
- **Vector API가 정식 표준화됨.** Valhalla를 기다리느라 9차 incubator에 머물던 JEP 489가 마침내 표준이 된다.
- **`@ValueBased` 어노테이션이 *진짜 약속*이 됨.** Java 16에서 hint로 도입됐던 어노테이션이, 언어 차원의 키워드로 정식화.

이 다섯 자리는 *우리가 매일 적던 코드*다. 그 자리에서 *동일한 의도가 더 효율적인 표현*으로 바뀐다. Valhalla가 정착하면, *Java 30의 코드를 Java 25 개발자가 봐도 거의 똑같이 읽힌다*. 그러나 그 코드가 도는 효율은 *수 배 차이*가 난다. 이게 호환성을 지키며 진화하는 자바의 *고유한* 방식이다.

## Project Amber의 다음 카드

다음으로 Amber를 들여다보자. Amber는 자바의 *언어 표면*을 다듬는 우산 프로젝트다. records, sealed classes, pattern matching, text blocks, `var` — 11장부터 13장까지 살펴본 카드들이 전부 Amber에서 나왔다. 다음 카드는 무엇인가?

### primitive type patterns

13장에서 다룬 pattern matching for switch를 떠올려 보자. 객체 타입에서는 자연스러웠다.

```java
return switch (result) {
    case Approved(var code, var at) -> /*...*/;
    case Declined(var reason, var msg) -> /*...*/;
    case Failed(var code, var __) -> /*...*/;
};
```

그런데 *primitive*에는 어색했다. `int`를 switch에 넣는 옛 자바 문법은 *값 비교*뿐이고, `instanceof int`는 문법적으로 *말이 안 되는* 일이었다. 그래서 primitive를 wrapper로 boxing한 뒤 pattern matching에 넣어야 했다 — *번거로웠다*.

**JEP 488: Primitive Types in Patterns, instanceof, and switch** (preview)가 그 자리를 정리한다.

```java
// 가상의 미래 자바
Object o = 42;
if (o instanceof int i) {     // 가능!
    System.out.println(i + 1);
}

return switch (value) {
    case int i when i > 0  -> "positive";
    case int i when i < 0  -> "negative";
    case int __            -> "zero";
    case double d          -> "float " + d;
    case String s          -> "string " + s;
};
```

`instanceof int`가 컴파일된다. `switch`의 case에 `int i`, `double d`가 들어간다. 그 자체로는 작은 변화 같지만 — 더 큰 그림에서 보면 *primitive와 reference가 pattern matching 안에서 통합*된다. Valhalla의 value class와 함께 가면, *모든 값이 같은 pattern 어휘로 표현*된다.

### array patterns

다음 카드는 array다.

```java
// 가상의 미래 자바
Object o = new int[]{1, 2, 3};

return switch (o) {
    case int[] {var first, var second, var third} -> first + second + third;
    case int[] {var first, var ... rest}          -> first;
    case int[] {}                                  -> 0;
    default                                        -> -1;
};
```

array를 *deconstruct*한다. record pattern과 같은 어휘다. 첫 원소, 마지막 원소, 비어 있음 — 한 줄에 표현된다. Stream API로 `arr[0]`, `arr.length`를 따로 검사하던 코드가 정리된다.

### with-expressions — record의 *부분 복사*

마지막 카드를 살펴보자. record가 immutable이다. 한 컴포넌트만 바꾸려면 어떻게 하나?

```java
// 현재 (Java 25)
record Money(BigDecimal amount, String currency) {}

var krw = new Money(BigDecimal.ZERO, "KRW");
var updated = new Money(BigDecimal.valueOf(1000), krw.currency()); // *번거롭다*
```

Kotlin의 `data class`는 `copy(amount = 1000)` 한 줄로 끝낸다. Scala도, Rust도 비슷한 어휘를 갖는다. 자바에는 *없었다*. record가 컴포넌트가 5개를 넘어가면 *지긋지긋해진다*.

**with-expression**이 그 자리에 들어온다.

```java
// 가상의 미래 자바
var updated = krw with { amount = BigDecimal.valueOf(1000); };
```

또는 표현식 형태로:

```java
var updated = krw with (amount: BigDecimal.valueOf(1000));
```

*확정 문법은 아니다*. JEP draft 단계다. 그러나 방향은 분명하다 — record의 immutable한 신원을 지키면서, *부분 복사*가 언어 차원의 어휘가 된다. 11장에서 다룬 record가 그동안 *부족했던* 한 자리가 정리된다.

## String Templates의 좌초와 재설계 — 사후 추적

여기서 한 자리를 *솔직하게* 짚자. 10장에서 다뤘던 String Templates 이야기다. JEP 430 (21 preview), JEP 459 (22 preview)로 등장했던 문법이다.

```java
// JEP 459 — Java 22까지의 preview
String name = "PayBridge";
String greeting = STR."Hello \{name}!";
```

`STR."..."` 어휘가 *어색하다*고 느낀 사람이 많았다. prefix 처리, null 의미론, 이스케이프 규칙이 다른 언어의 익숙한 string interpolation과 *미묘하게* 달랐다. 그리고 Java 23에서 **철회**됐다.

이 철회는 *실패*인가, *자정*인가? OpenJDK의 입장은 후자다. preview의 의미가 바로 이것 — *산업 피드백을 받아 다듬을 수 있고, 필요하면 되돌릴 수 있다*. records가 14에서 preview로 등장해 16에서 표준이 되기까지 2년이 걸렸고, 표준 이후에는 거의 부작용 없이 정착했다. String Templates는 그 *2년 검증*의 단계에서 자정됐다. *허망함*은 있지만, *잘못된 어휘를 21·22의 LTS에 그대로 박는 것보다* 나은 결정이다.

재설계의 방향은 (이 책이 인쇄되는 시점 기준으로) 아직 *명시적 JEP*로 나와 있지 않다. 알려진 의견은 두 가지다.

첫째, `StringTemplate.Processor`라는 *별도 타입*을 두지 말고, 결과 타입이 *바로 그 자리의 expected type*에 맞춰지게 하자. 즉, `String x = "Hello \{name}!"`이 그대로 `String`을 반환하고, `Document x = HTML."<p>\{name}</p>"`이 `Document`를 반환하도록.

둘째, prefix(`STR.`, `HTML.` 등) 어휘를 *생략*하고 컨텍스트에서 추론하자. 또는 더 가벼운 어휘로 표현하자.

이 방향이 확정되면, 10장에서 살펴본 그 *번거로움*이 마침내 정리된다. 그러나 *언제 올지는 모른다*. 자바답게, *서두르지 않는다*. 잘못된 어휘를 LTS에 박는 것보다, 한 LTS를 더 기다리는 편이 *낫다*는 결정이다.

## Project Babylon — Java가 GPU·자동미분에 닿는다

다음으로 살펴볼 프로젝트는 *외관*에서 가장 놀라운 카드다. **Project Babylon**이다.

Babylon이 풀려는 문제가 무엇인가? *Java가 자기 영역 밖의 컴퓨팅을 표현할 수 있어야 한다*는 것이다. GPU, 자동미분(autodiff), SQL DSL, SPIR-V 같은 GPU bytecode — 이 모든 것이 *Java 코드*로 적힐 수 있어야 한다는 야망이다.

지금까지는 어땠나? GPU에 코드를 보내려면 CUDA C++ 또는 OpenCL을 적었다. Java에서는 JNI로 호출하거나, GraalVM의 polyglot으로 우회했다. *번거로웠다.* 결제 시스템에서 머신러닝 inference를 자바로 적으려면, 모델 로딩과 데이터 전처리는 자바로, 실제 inference는 Python으로 — 두 언어를 *오가는* 끔찍한 일이 일상이었다.

Babylon의 핵심 발상은 **code reflection**이다. 자바 메서드의 *람다 표현식*을 컴파일러가 *그 안의 코드 구조 자체*로 보존한다. 보통은 람다가 bytecode로 컴파일되면 *그 안의 의미*는 사라진다 — 그저 실행 가능한 함수일 뿐이다. Babylon은 람다의 AST(혹은 그와 동등한 IR)를 *런타임에 들여다볼 수 있게* 만든다.

```java
// 가상의 미래 자바 — Babylon HAT 예시
GpuKernel kernel = Gpu.compile((float[] a, float[] b, float[] out) -> {
    int i = Gpu.threadIdx();
    out[i] = a[i] + b[i];
});

float[] a = /* ... */, b = /* ... */, out = new float[1024];
kernel.launch(a, b, out, 1024);
```

`Gpu.compile`에 *람다*가 들어간다. 그 람다의 *코드 구조 자체*가 Babylon의 IR로 보존되고, GPU bytecode(예: SPIR-V, PTX)로 변환돼 GPU에서 실행된다. *자바 코드가 GPU에서 돈다*. JNI도, CUDA C++도, Python bridge도 없다.

이게 단순한 GPU 시나리오에서 그치지 않는다.

### 자동미분 (autodiff)

```java
// 가상의 미래 자바
Function<Double, Double> f = x -> x * x + 3 * x + 1;
Function<Double, Double> dfdx = Autodiff.derivative(f);
double slope = dfdx.apply(2.0);  // = 2*2 + 3 = 7
```

람다의 *구조*를 들여다보고, 미분 규칙을 적용해 *새 람다*를 만든다. ML 학습 코드를 자바로 적을 수 있다.

### SQL DSL

```java
// 가상의 미래 자바
Stream<Payment> result = sql.from(Payment.class)
    .where(p -> p.amount().compareTo(BigDecimal.valueOf(1000)) > 0)
    .where(p -> p.status() == PaymentStatus.APPROVED)
    .stream();
// 람다가 *컴파일러 차원*에서 SQL where 절로 변환됨
```

JOOQ, QueryDSL, Criteria API가 지금까지 *문자열 빌더*나 *메타모델 + builder*로 우회했던 자리를, Babylon이 *언어 차원에서* 풀어낸다.

### HAT (Heterogeneous Accelerator Toolkit)

Babylon의 첫 가시적 결실이 **HAT**다. CPU·GPU·FPGA 같은 이질 가속기에 *동일한 자바 코드*가 매핑되는 toolkit이다. 머신러닝, 행렬 연산, 신호 처리 — 그동안 Python이나 C++로 적던 자리가 자바로 옮겨질 수 있다.

PayBridge의 5년 뒤를 다시 떠올려 보자. 정산 배치가 GPU에서 돈다고 했다. 그 코드가 *자바*다. 11장에서 적은 record DTO, 13장에서 적은 sealed result, 14장에서 적은 virtual thread — 같은 어휘로 GPU·CPU·FPGA가 매핑된다. *한 언어로 끝나는* 자바의 야망이다.

언제 오는가? *모른다*. Babylon은 가장 야심차고 가장 *느린* 프로젝트다. 그러나 방향은 분명하다 — 자바는 *자기 영역 밖*까지 자기 어휘를 확장한다.

## Project Leyden의 종착점 — *static image + AOT code cache*의 일반화

마지막 프로젝트를 살펴보자. **Project Leyden**이다. 19장에서 AOT class loading & linking (JEP 483), CDS, compact object headers를 살펴봤다. Leyden의 종착점은 그보다 한 걸음 더 멀다.

Leyden이 풀려는 문제가 무엇인가? *콜드 스타트와 메모리 풋프린트*다. GraalVM Native Image가 풀던 그 문제를, *JVM의 호환성을 깨지 않고* 푸는 길이다.

진행 상태를 한 줄로 정리하자면:

| 단계 | JEP | Java | 효과 |
|------|-----|------|------|
| AppCDS | (옛) | 10 | class metadata 캐시 |
| Dynamic CDS | JEP 350 | 13 | 단일 run으로 archive 생성 |
| AOT Class Loading & Linking | JEP 483 | 24 | class를 init·link해서 캐시 |
| AOT CLI ergonomics | JEP 514 | 25 | training run 한 줄 |
| AOT Method Profiling | JEP 515 | 25 | JIT 프로파일까지 캐시 |
| AOT Code Cache | (premain branch) | 미래 | *컴파일된 머신 코드*까지 캐시 |

마지막 행이 종착점이다. 지금까지의 AOT는 *class를 init·link*까지만 했다. 실제 머신 코드 컴파일은 런타임 JIT에 맡겼다. Leyden의 *premain branch*가 가는 길은 — *컴파일된 머신 코드 자체*를 빌드 타임에 만들어 캐시에 박는 것이다. 그러면 JVM이 부팅해서 첫 요청을 받기까지의 시간이 *수백 밀리초* 수준으로 떨어진다.

Spring Petclinic 기준으로 보면, AOT class loading만 켜도 startup이 36~42% 단축된다. Spring AOT + JDK AOT 조합으로 *4배* 개선 보고가 있다. AOT code cache까지 일반화되면 — *GraalVM Native Image 없이도* 콜드 스타트가 수백 밀리초 수준으로 떨어진다.

이게 왜 중요한가? *serverless와 short-lifecycle 컨테이너*가 자바의 영역이 된다. AWS Lambda, Cloud Run, Knative — 그동안 *콜드 스타트 8초의 난감함* 때문에 Go·Node.js·Python에 밀렸던 자리가, 자바로 돌아온다. PayBridge의 5년 뒤 풍경에서 *콜드 스타트 400ms*라고 적은 이유다.

GraalVM Native Image와의 차이는 분명하다. Native Image는 *closed-world*를 가정한다 — reflection, dynamic class loading, JNI 같은 dynamic 기능에 제약이 따른다. 그래서 Spring AOT가 reachability metadata를 빌드 타임에 생성해 줘야 했고, 그래도 어떤 라이브러리는 *못 돌았다*. Leyden은 *open-world*다. 기존 JVM의 모든 dynamic 기능을 그대로 누리면서, 시작 시간만 줄인다. *호환성을 깨지 않는다*. 이게 OpenJDK의 길이다.

## 호환성 — 자바의 *가장 큰 자산*

여기서 한 발 물러서 보자. Valhalla, Amber, Babylon, Leyden — 네 프로젝트를 관통하는 *공통점*이 무엇인가? **호환성을 깨지 않으면서** 진화한다는 점이다.

- **Valhalla.** value class는 기존 class와 호환된다. `Optional`이 value class로 옮겨가도, 옛 코드는 한 글자도 안 바꿔도 돈다.
- **Amber.** primitive patterns, array patterns, with-expressions — 모두 옛 문법을 *대체*하지 않고 *추가*한다. records, sealed, pattern matching이 그랬듯이.
- **Babylon.** code reflection은 *기존 람다 위에 얹는* 도구다. 옛 람다는 그대로 돈다. Babylon이 들여다보고 싶을 때만 들여다본다.
- **Leyden.** AOT cache는 *training run*의 결과를 *선택적으로* 적용한다. 기존 부팅 경로는 그대로 살아 있다.

이게 자바의 *가장 큰 자산*이다. 11년 동안 Java 8에서 Java 25까지 오면서, 거의 모든 옛 코드가 *컴파일러 한 줄 옵션*만으로 새 JVM에서 돈다. 다른 언어 진영의 *깨는 변경*과 비교해 보자. Python 2 → 3는 *10년의 고통*이었다. Scala 2 → 3는 *대대적 재작성*이었다. 자바는 같은 11년에 *람다·records·virtual thread·AOT·pattern matching*을 가져왔는데, 그 사이 *깨는 변경은 거의 없었다*.

이게 *지루함*인가? 아니다. *신뢰*다. 어제의 코드가 내일도 도는 것 — 엔터프라이즈가 자바를 떠나지 못하는 진짜 이유다. 11년 전 Java 8로 적은 PayBridge의 첫 마이크로서비스가 *지금도 그대로 도는* 자리를 만들어 준 것은, 컴파일러 팀의 *고집스러운* 호환성 약속이었다.

## 수미상관 — PayBridge의 가상 Java 30 코드

이제 1장에서 시작한 PayBridge 이야기를 닫아 보자. 11년 전 2014년에 작은 스타트업으로 출발해, 책의 곳곳에서 11년의 코드 변천을 함께 따라온 그 회사다. 21장에서 본 *지금의 컨트롤러*를, 5년 뒤로 옮겨 보자.

```java
// PayBridge — 가상 Java 30 결제 컨트롤러 (2030년)

// 도메인 모델 — value record + null-restricted types
public value record PaymentRequest(
    String! merchantId,
    Money! amount,
    Card! card
) {
    public value record Card(
        String! number,
        String! expiry
    ) {}
}

public value record Money(BigDecimal! amount, Currency! currency) {}

public sealed interface PaymentResult permits Approved, Declined, Failed {
    value record Approved(String authCode, Instant capturedAt) implements PaymentResult {}
    value record Declined(String reason, String issuerMessage) implements PaymentResult {}
    value record Failed(String errorCode, Throwable cause) implements PaymentResult {}
}

@RestController
public class PaymentController {
    private final RestClient fraudClient;
    private final RestClient cardClient;
    private final FraudModel fraudModel;  // Babylon HAT로 GPU 추론

    @PostMapping("/payments/authorize")
    public PaymentResponse authorize(@Valid PaymentRequest req) throws InterruptedException {
        try (var scope = StructuredTaskScope.open()) {
            var fraudScore = scope.fork(() -> fraudModel.scoreOnGpu(req));
            var auth = scope.fork(() ->
                cardClient.post().uri("/authorize").body(req).retrieve().body(AuthResult.class));
            scope.join();

            var result = switch (auth.get()) {
                case AuthResult.Ok(var code) when fraudScore.get() < 0.3 ->
                    new PaymentResult.Approved(code, Instant.now());
                case AuthResult.Ok(_) ->
                    new PaymentResult.Declined("FRAUD_SUSPECTED", "blocked by risk engine");
                case AuthResult.Rejected(var msg) ->
                    new PaymentResult.Declined("ISSUER_REJECTED", msg);
            };

            return toResponse(result);
        }
    }
}
```

21장의 컨트롤러와 *얼마나 다른가?* 본질은 같다. 비즈니스 로직만 보인다. 다른 점이 무엇인가?

- **`value record`**: 모든 도메인 모델이 value class가 됐다. `Money` 수십억 개가 *primitive 효율*로 돈다.
- **`String!`, `Money!`, `Card!`**: null-restricted types. NPE가 *컴파일 시점에 사라진다*.
- **`fraudModel.scoreOnGpu(req)`**: 사기 탐지 ML 모델이 Babylon HAT로 GPU에서 돈다. 같은 자바 어휘로 적혀 있다.
- **`case AuthResult.Ok(_)`**: 안 쓰는 컴포넌트를 `_`로. 이건 이미 Java 21에서 가능했다.

11년 동안 PayBridge가 거쳐 온 길을 한 페이지로 정리하면:

- **2014년 Java 8**: 람다, Stream, `java.time`. 함수형 자바의 시작.
- **2017년 Java 9**: JPMS 시도. *난감했다*. 결국 안 썼다.
- **2018년 OpenJDK 이주**: Oracle 라이선스 변화. 처음으로 *벤더와 버전을 분리*.
- **2022년 Java 17 + Spring Boot 3**: `jakarta` namespace 전환. DTO를 records로 옮김. JPA Entity로 records 시도하다 *좌절*한 사건.
- **2024년 Java 21 + virtual thread**: thread-per-request 부활. HikariCP 옛 버전에서 deadlock 발생. JFR로 진단, 신 버전으로 해결.
- **2025년 Java 25**: 정산 배치에 Compact Object Headers + AOT cache. 콜드 스타트 단축. ScopedValue로 ThreadLocal 정리.
- **2030년 Java 30 (가상)**: value class로 메모리 효율, Babylon HAT로 GPU 추론, Leyden AOT code cache로 콜드 스타트 400ms.

이 *16년의 호*가 자바 한 언어로 그려진다. 어떤 라이브러리, 어떤 프레임워크, 어떤 패러다임이 옮겨가도 — 자바라는 *연속체* 위에서 이어진다. 이게 PayBridge 같은 엔터프라이즈가 자바를 떠나지 않는 이유다. 어제의 코드가 내일도 돌고, 5년 뒤의 도구를 받아들이는 데 *재작성이 필요 없다*.

## 마무리 — 11년의 자바를 견뎌낸 자바 개발자에게

이 책을 여기까지 따라온 자바 개발자에게 한 페이지의 헌사를 남기자.

11년이라는 시간을 한 줄로 정리하기는 어렵다. 람다를 처음 만났을 때의 *어색함*, Stream의 `peek`을 두고 배포한 *찜찜함*, Optional을 처음 잘못 쓴 *당혹감*, NullPointerException의 *지긋지긋함*, 30자 타입 선언의 *번거로움*, jakarta namespace 전환 첫날의 *막막함*, virtual thread 켰는데 deadlock이 난 *끔찍한* 새벽, 콜드 스타트 8초의 *난감함*, String Templates 좌초의 *허망함*, 600줄짜리 `if-else` 분기를 패턴 매칭으로 옮긴 *후련함*, 그리고 한 컨트롤러에 11년의 도구가 모이는 그 *깊은 만족감*.

이 모든 감정을 함께 겪으며 코드를 다듬어 온 11년이다. 그 코드는 지금도 어딘가에서 돌고 있고, 누군가의 결제 거래를 처리하고 있고, 누군가의 메시지를 전달하고 있다. *어제의 자바가 오늘도 돈다.* 그게 자바라는 언어의 *가장 큰 약속*이고, 그 약속을 *지키는 일*이 컴파일러 팀의 *고집스러운 일관성* 위에서만 가능했다.

자바는 *완벽한 언어*가 아니다. Kotlin·Scala·Rust가 자바보다 표현력에서 앞선 자리가 여럿 있다. 자바는 그 자리를 *서두르지 않고* 한 LTS, 한 preview, 한 자정을 거쳐 받아들인다. records가 14에서 16까지 2년, virtual thread가 19에서 21까지 2년, AOT가 10에서 25까지 15년 — 자바의 시간 단위는 다른 언어보다 길다. 그 *느림*이 호환성을 만들고, 그 호환성이 PayBridge 같은 회사가 16년의 코드를 *한 언어로* 이어 쓸 수 있는 자산이 된다.

이 책의 마지막 한 페이지에서, 한 가지를 *기억해두자*. *Modern Java는 끝나지 않았다.* Valhalla가 들어오고, Babylon이 GPU에 닿고, Leyden이 콜드 스타트를 풀고, Amber가 with-expression을 가져오는 그 *다음 11년*이 우리를 기다리고 있다. 그리고 그 11년의 코드는 지금 우리가 쓰는 자바와 *같은 자바*다 — 더 빠르고, 더 안전하고, 더 표현력이 풍부하지만, 한 줄을 *대대적으로 재작성*하지 않아도 되는 자바.

이제 우리가 할 일은 한 가지다. 다음 자바를 *함께 기다려보자*. JEP를 읽고, preview를 켜 보고, 우리 코드에 *맞는 자리*를 찾아 천천히 옮겨가 보자. 11년 전 람다를 처음 손에 잡았을 때 그랬듯이 — *어색함*에서 시작해 *익숙함*을 거쳐 *후련함*에 도달해 보자.

자바 개발자로서의 11년을 견뎌낸 당신에게, 그리고 다음 11년을 함께 걸어갈 당신에게, 이 책을 바친다.

*함께 다음 자바를 기다려보자.*
