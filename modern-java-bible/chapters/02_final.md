# 2장. 11년 변화의 다섯 가지 동력

기획 회의에서 "왜 굳이 21로?"라는 질문이 나왔다고 해보자.

화면에는 마이그레이션 일정과 인력 산정이 띄워져 있고, 회의실 끝에서 누군가가 손을 든다. "Java 17은 작년에 막 올렸잖아요. 잘 돌고 있어요. 왜 *지금* 또 21이에요? 그것도 records·virtual thread 같은 큰 변화가 있다면서요. 8에서 17로 올 때도 컴파일 에러 700개를 봤는데, 또 그런 거 보자고요?" 회의실은 잠시 조용해진다. 답을 못 하면 새 LTS 마이그레이션 첫날의 *난감함*이 모두에게 옮겨붙는다. 그 답은 의외로 간단하지만, 단순하지는 않다. 자바의 변화는 *무작위*가 아니라 다섯 갈래의 *동력*이 시기별로 결과를 낸 것이고, 21은 그 다섯 중 셋째가 임계점을 넘은 LTS이기 때문이다.

자, 그렇다면 그 다섯 동력을 함께 살펴보자.

## 왜 이 순서였을까

자바의 11년을 가만히 들여다보면 한 가지가 보인다. 람다·records·virtual thread가 *이 순서로* 들어왔다는 사실. 무작위로 보이지 않는다. 람다(8) → records(17) → virtual thread(21)에 정확히 4년 간격이 있고, 그 사이에 비-LTS들이 다리를 놓는다. 더 흥미로운 점은 — 비-LTS의 변화도 *셋 중 하나의 동력*에 속한다는 것이다.

이 책은 11년의 자바를 다섯 동력으로 묶어 본다. 다섯 동력에는 OpenJDK 내부에서 부르는 *프로젝트 이름*이 붙어 있다. 그리고 각 프로젝트는 책의 한 부(Part)에 대응된다. 그러니까 이 장은 *책 전체의 미리보기*이기도 하다.

다섯 동력은 다음과 같다.

1. **함수형 패러다임** — *Project Lambda*에서 시작해 *Stream Gatherers*까지.
2. **데이터지향** — *Project Amber*가 그린 records·sealed·pattern matching.
3. **동시성** — *Project Loom*의 virtual thread·structured concurrency·scoped values.
4. **메모리·네이티브·성능** — *Project Panama*(FFM·Vector)와 *Project Leyden*(AOT·startup), 그리고 GC 진화.
5. **도구와 언어 표면의 정리** — JPMS·`var`·switch·text blocks·markdown javadoc·module import 같은 *작지만 결정적인* 변화들.

각각을 차례로 들여다보자. 그리고 각 동력의 끝에는 *그 동력이 책의 어느 부에서 본격적으로 다뤄지는지* 표시해두겠다.

## 첫째 동력 — 함수형 패러다임 (Project Lambda → Gatherers)

자바가 함수형으로 옮겨가는 일은 한 LTS의 사건이 아니라 *11년에 걸친 점진적 흡수*다.

시작은 분명하다. 2014년 Java 8, JSR 335. 람다 표현식과 함수형 인터페이스, 그리고 그 위에 얹힌 Stream API. 그날부터 자바 개발자는 `Function`, `Predicate`, `Supplier`, `Consumer`, `BiFunction`이라는 새 어휘를 손에 쥐었다. `for-each` 루프가 `forEach(...)`로 바뀌고, `Comparator` 익명 클래스가 `Comparator.comparing(User::getName)`이 됐다. Stephen Colebourne의 `java.time`(JSR-310)이 함께 들어와 `Date`와 `Calendar`의 종말을 선언했다.

그러나 *진짜 함수형*은 8에 다 들어오지 못했다. `Optional<T>`는 8에 있었지만 `ifPresentOrElse`·`or`·`stream`은 9에서야 추가됐다. `Stream::toList`는 16에서야 들어왔다 — 그 전까지 `collect(Collectors.toUnmodifiableList())`라는 *번거로움*을 견뎌야 했다. `takeWhile`·`dropWhile`·`iterate(seed, hasNext, next)` 같은 자연스러운 연산이 9에서 추가됐다. 가장 결정적인 진화는 한참 뒤에 왔다. **Stream Gatherers** — JEP 461(22 preview) → 473(23 second preview) → 485(24 standard). 그동안 *Stream에선 자연스럽지 않다*고 여겨졌던 슬라이딩 윈도우, prefix sum, 병렬 매핑이 한 줄로 표현 가능해진 것이다. 5분 이동 평균을 구하는 데 `Collectors.toMap`을 1000번 쓰던 *지긋지긋함*은 이제 옛이야기가 됐다.

함수형 패러다임의 진짜 의미는 *문법*이 아니다. `reduce`의 monoid 속성(identity·associativity), `flatMap`의 monad 의미, Collector의 5요소(supplier·accumulator·combiner·finisher·characteristics)가 fold의 일반화임을 인지하는 *시야*다. 그 시야는 한 번 들어오면 Optional, Stream, CompletableFuture, Mono/Flux를 *같은 형식의 다른 표현*으로 보게 만든다. 그게 함수형이 자바에 가져온 진짜 변화다.

> *책 안에서:* Part II(3·4장), Part III(5·6·7장)에서 본격. 특히 6장의 *fold·monad·composition* 절이 이 동력의 깊이를 보여준다.

## 둘째 동력 — 데이터지향 (Project Amber)

함수형이 자바의 *행위*를 바꿨다면, 데이터지향은 *데이터의 모양*을 바꿨다.

Brian Goetz가 InfoQ에 쓴 *Data-Oriented Programming in Java*는 명시적이다. **데이터는 불변으로, 행위는 분리하라.** 객체지향이 캡슐화로 데이터와 행위를 묶었다면, DOP는 그 반대편을 표현한다. 그리고 그 반대편을 표현하는 도구가 세 개 — records, sealed, pattern matching.

세 도구의 발원지는 *Project Amber*다. 진행은 다음과 같다.

- **Records (JEP 359 preview → 395 standard, Java 14→16)** — *product type*. 컴포넌트의 카르티시안 곱. `final` 클래스, `private final` 필드, 자동 accessor·`equals`·`hashCode`·`toString`, canonical constructor.
- **Sealed Classes (JEP 360 preview → 397 second preview → 409 standard, Java 15→17)** — *sum type*. `sealed interface Expr permits Num, Add, Mul`. 허용된 sub-type의 닫힌 합집합.
- **Pattern Matching for instanceof (JEP 305 preview → 394 standard, Java 14→16)** + **Record Patterns (JEP 405→440, Java 19→21)** + **Pattern Matching for switch (JEP 406→441, Java 17→21)** + **Unnamed Patterns (JEP 443→456, Java 21 preview→22 standard)** — ADT의 분해와 분기.

Records + Sealed = **대수적 데이터 타입(ADT)**. Pattern matching은 그 분해 도구다. Haskell·Scala·OCaml·Kotlin·Rust가 가진 표현력을 자바가 마침내 갖춘 것이다. `instanceof` 캐스트 사다리가 9단까지 늘어난 컨트롤러를 받았을 때의 *끔찍함*을 기억하는가? `if (x instanceof A) { A a = (A)x; ... } else if (x instanceof B) { ... }` 이 사다리가 switch pattern 한 블록으로 정리되는 순간, 그 *후련함*은 한 번 본 사람은 잊지 못한다.

다만 정직하게 짚자. records는 Lombok의 *대체*가 아니다. Brian Goetz의 표현을 빌리자면, Lombok이 "자바가 부족해서 메우는 패치"라면 records는 "자바가 데이터 캐리어를 인정한 신원"이다. *의도가 다르다.* 그래서 JPA Entity로 records를 시도한 신입이 *좌절*하는 일이 생긴다. records는 final + 불변이고, JPA Entity는 mutable + no-args constructor + non-final을 요구한다. 그래서 실무에서 자리 잡은 가이드라인은 단순하다 — **Entity는 클래스(또는 Lombok), DTO·Projection·Command는 records**.

> *책 안에서:* Part VI(11·12·13장)에서 본격. 13장에서 PayBridge의 결제 표현식 평가기를 records·sealed·pattern matching으로 재구성한다.

## 셋째 동력 — 동시성 (Project Loom)

자바의 동시성 모델이 *근본부터* 바뀐 사건이 21에서 일어났다. 그 사건의 이름이 *virtual thread*다.

이걸 이해하려면 잠시 옛 모델을 떠올려야 한다. Java의 전통적 thread는 OS thread = `java.lang.Thread`였다. Linux x64 기준 스택 ~1MB 예약, 컨텍스트 스위치 비용 크고, 수천 개까지가 한계. I/O-bound 웹 애플리케이션은 대부분의 시간을 DB·외부 API 대기에 쓰는데, 그동안 OS thread는 idle인 채 자원만 점유했다. 그래서 Tomcat 200 thread 풀로 한 달을 버틴 끝에 p99가 800ms였다 — *답답한* 일이다. *thread-per-request 모델은 사실상 죽었다*는 게 2010년대 후반의 분위기였다.

대안은 *비동기*였다. `CompletableFuture`의 50개+ 메서드 체인, Reactor의 `Mono`/`Flux`, RxJava의 `Observable`. 그러나 이쪽은 *비싸다*. 콜백·체인 사이에 컨텍스트를 옮기는 게 번거롭고, 스택 트레이스가 산산이 흩어지며, `synchronized`·`ThreadLocal` 같은 옛 도구가 작동을 멈춘다. backpressure를 이해해야 하고, exception 흐름을 따로 설계해야 한다. 새 프로젝트라면 모르되, 30년 묵은 자바 코드를 reactive로 옮기는 일은 *지옥*에 가까웠다.

Project Loom의 답은 우회였다. *OS thread 위에 lightweight thread를 얹자.* `Thread.ofVirtual().start(...)` 또는 `Executors.newVirtualThreadPerTaskExecutor()`로 만드는 **virtual thread**는 JVM이 관리한다. 스택은 heap에 작게 시작해서 필요 시 grow한다. M:N 스케줄링 — 다수 virtual thread가 소수의 carrier(platform) thread에 multiplex. blocking 호출이 들어오면 자동 unmount → 다른 virtual thread가 그 carrier를 점유. 결과적으로 *수백만 개* 생성 가능하다. Brian Goetz의 표현으로는 "virtual memory의 비유" — 물리 메모리보다 큰 환상의 메모리를 주듯, 물리 thread보다 많은 환상의 thread를 주는 것이다.

JEP 425(19 preview) → 436(20 second preview) → **444(21 standard)**. 21이 동시성 모델의 전환점이 된 이유다.

그러나 virtual thread는 *마법*이 아니다. *pinning*이라는 새 함정이 있다. Java 21~23에서는 `synchronized` 블록 내부 I/O가 pinning을 일으켰다 — virtual thread가 unmount 못 하고 carrier thread를 점유한 채 굳어버리는 현상. HikariCP, Caffeine, MySQL Connector/J 같은 라이브러리가 `synchronized` → `ReentrantLock` 이주로 대응했고, Netflix는 production deadlock을 경험했다. *덜컥*한 사건이었다. JDK 24의 JEP 491이 *그 30년 묵은 JVM 모니터 구현*을 손봐서 `synchronized`도 unmount 가능하게 만들었지만, 그 전까지 한국·해외 가릴 것 없이 많은 회사가 VT 도입 첫 분기에 새벽 알람을 받았다.

Loom의 동반자는 두 개 더 있다. **Structured Concurrency** (JEP 453 preview → 533 다섯 번째 preview까지 진행 중) — `StructuredTaskScope`로 자식 task들을 단일 단위로 묶고, 모두 성공/모두 실패/모두 취소를 보장한다. Dijkstra의 structured programming을 *concurrent 코드*에 재해석한 것이다. 그리고 **Scoped Values** (JEP 506 standard, Java 25) — virtual thread가 cheap·short-lived해서 ThreadLocal에 connection·SimpleDateFormat을 캐싱하던 옛 패턴이 *수백만 thread × 수백만 캐시 인스턴스*를 만들 위험이 생겼다. ScopedValue가 그 답이다. 부모/자식 binding, immutable, 자동 cleanup. ThreadLocal 청소를 안 해 메모리가 새던 옛 *찜찜함*을 정리하는 도구다.

한국에서 virtual thread를 production에 본격적으로 도입한 사례는 이미 적지 않다. 우아한형제들이 *Java의 미래, Virtual Thread*라는 제목으로 두 차례 기술 블로그 글을 냈고(techblog.woowahan.com/15398/와 /17163/), 카카오는 제4회 Kakao Tech Meet에서 *JDK 21의 Virtual Thread*를 다뤘으며, 카카오페이는 *Virtual Thread에 봄(Spring)은 왔는가*에서 platform thread → virtual thread 전환의 자원 소모를 실측해서 공개했다(tech.kakaopay.com).

> *책 안에서:* Part IV(8A·8B장)에서 Loom *이전*의 동시성 — JMM, j.u.c, `CompletableFuture`, Flow를 다지고, Part VII(14·15·16장)에서 Loom *이후*를 본격. Spring Boot 3.2의 `spring.threads.virtual.enabled` 한 줄 설정과 그 한 줄 뒤에 숨은 의미가 14·21장에서 만난다.

## 넷째 동력 — 메모리·네이티브·성능 (Project Panama + Project Leyden + GC)

이 동력은 사실 *세 개의 작은 동력*이 한 묶음이 된 것이다. 끝까지 따라가면 결국 "자바를 *빠르게*, *가볍게*, *외부 세계와 잘 통하게* 만든다"는 한 문장으로 수렴한다.

### Project Panama — 네이티브와 SIMD

JNI의 시대가 끝나고 있다. JNI는 거대한 boilerplate를 요구했다 — `*.h` 작성, header 추출, C 코드, `System.loadLibrary`. GC와 충돌이 잦고, 한 번 native crash가 나면 JVM 전체가 죽었다. *끔찍한* 기억을 가진 자바 개발자가 적지 않다. Project Panama는 그 자리를 메우러 왔다.

- **Foreign Function & Memory API (FFM)** — JEP 412(17 incubator) → 442(21 third preview) → **454(22 standard)**. `Arena`로 lifetime을 관리하고, `MemorySegment`로 명시적·범위 한정된 native memory를 다루며, `Linker`로 함수 시그니처를 method handle로 옮긴다. `jextract`가 C header → Java 바인딩을 자동 생성한다. `try (Arena arena = Arena.ofConfined()) { MemorySegment seg = arena.allocate(100); ... }` — 메모리 해제가 try-with-resources로 자연스럽게 된다.
- **Vector API** — JEP 338(16 first incubator) → 489(24 ninth incubator). 아직 표준화 안 됐다. *Project Valhalla*의 value types를 기다리는 중이다. 표준화되면 AVX2·AVX-512·NEON·SVE에 자동 매핑된다. 행렬 연산, 벡터화 가능한 numeric loop, ML inference를 위한 도구다.

### Project Leyden — 시작 시간

Java가 클라우드 시대에 받은 가장 큰 *난감함*은 cold start였다. AWS Lambda에 8초짜리 콜드 스타트가 떠서 SLA를 깬 사례, 한국 핀테크에서도 적지 않게 봤다. 옛 답은 GraalVM Native Image 하나뿐이었다 — closed-world 가정, reachability metadata, reflection 제약. 강력하지만 *비싼* 답이었다.

OpenJDK의 답은 다른 방향에서 왔다.

- **AppCDS** (Java 10) — class metadata 캐시.
- **Dynamic CDS Archives** (Java 13) — 단일 run으로 archive 생성.
- **JEP 483 (Java 24)** — Ahead-of-Time **Class Loading & Linking**. class를 init·link해서 캐시. Project Leyden의 첫 가시적 결실이다.
- **JEP 514 / 515 (Java 25)** — AOT CLI ergonomics, AOT method profiling.

Spring Boot 3.3+는 이걸 통합했다. training run으로 AOT cache를 만들고, 다음 실행부터 적용한다. Spring Petclinic 기준 startup 36~42% 단축. Spring AOT(빌드 타임 BeanFactory 사전 계산) + JDK AOT(JVM 캐시)를 조합하면 ~4배 startup 개선이 보고됐다. *GraalVM 없이도 빠른 startup*이 가능해진 것이다.

### GC의 진화

마지막은 GC다. CMS의 시대(1.4)를 거쳐, G1이 9에서 default가 됐고, ZGC가 11에 실험적으로 들어와 15에서 production-ready가 됐다. Generational ZGC가 21(JEP 439)에서 들어와 23(JEP 474)에서 default가 됐다. Java 25에서는 Generational Shenandoah(JEP 521)가 도착했고, **Compact Object Headers (JEP 519)**가 들어왔다. 64비트 JVM의 모든 객체에 붙던 96~128비트 헤더를 64비트로 압축한 것이다. 작은 객체가 많은 워크로드(캐시, JSON 파싱)에서 heap 사용량 ~10~22% 감소가 보고됐다. 일부 측정에서 CPU 절감 30% 보고도 있다. *Java 8 PermGen OOM*에 시달려본 사람이라면, GC 진화의 11년을 보고 *묘하게 안도하는* 감각을 느낄 것이다.

> *책 안에서:* Part VIII(17·18·19·19A장)에서 본격. 17장에서 GC 선택, 18장에서 FFM, 19장에서 AOT/Leyden, 19A장에서 도구 일습.

## 다섯째 동력 — 도구와 언어 표면의 정리

다섯째는 이름이 붙은 *프로젝트*가 아니다. 그래서 더 흥미롭다. 11년에 걸쳐 *작지만 결정적인* 변화들이 누적된 영역이다.

- **JPMS (Java 9)** — 가장 야심찼고 가장 논쟁적이었다. 결론적으로는 *애플리케이션 레벨에서는 사실상 안 쓰이지만 JDK 내부 도구로는 필수*가 됐다. 9장에서 따로 다룬다.
- **`var` (Java 10)** — 사내 코드 리뷰에서 30자짜리 타입 선언을 매일 적던 동료가 *번거로움*에서 해방됐다. 다만 *가독성 논쟁*도 같이 왔다.
- **Switch Expressions (Java 12 preview → 14 standard)** + **Pattern Matching for switch (Java 17 preview → 21 standard)** — `case L ->` 화살표 form과 `yield` 키워드. 이건 단순한 문법 설탕이 아니라, 다섯째 동력이 둘째 동력(데이터지향)과 만나는 자리다.
- **Text Blocks (Java 13 preview → 15 standard)** — 삼중 따옴표 멀티라인. SQL·JSON·HTML 리터럴이 깔끔해졌다.
- **Sequenced Collections (Java 21, JEP 431)** — `SequencedCollection`·`SequencedSet`·`SequencedMap` 인터페이스로 첫·끝 원소 접근을 통일. `addFirst`·`addLast`·`reversed()`.
- **Markdown Javadoc (Java 23, JEP 467)** — `///` 세 줄 슬래시로 Markdown javadoc.
- **Module Import Declarations (Java 25, JEP 511)** — `import module java.base;` 한 줄로 모듈 전체 import.
- **Compact Source Files + Instance Main (Java 25, JEP 512)** — `void main()` 단독 실행. 입문자 친화 + 스크립트 활용도.
- **String Templates의 좌초** — JEP 430(21 preview)로 시작했다가 22에서 *철회*. Brian Goetz가 직접 "현재 설계가 만족스럽지 않다"고 밝혔다. 새 설계를 기다리는 중이다. *허망한* 사건이지만, 이런 일이 자바에 일어났다는 것 자체가 *변화에 정직해진* 신호로 읽을 만하다.

도구 쪽도 11년에 걸쳐 두꺼워졌다. **JShell** (9), **jpackage** (16), **jwebserver** (18), **jextract** (Panama 함께), **JFR + JMC**(11+, 오픈소스화). 19A장에서 이 도구들을 따로 모아 다룬다. CI 파이프라인이 Java 17을 인식 못 해 빌드가 깨졌을 때의 *피곤함*을 한 번이라도 겪어본 사람이라면, 도구 일습을 한 번 정리해두는 일이 얼마나 *후련한지* 알 것이다.

> *책 안에서:* Part V(9·10장)에서 언어 표면, Part VIII의 19A장에서 도구 일습.

## 한 도메인을 두 번 — Java 8 vs Java 25 미리보기

다섯 동력을 따로따로 보면 추상적이다. 그러니 한 도메인을 두 번 보자. PayBridge의 *주문 처리* 코드를 Java 8 스타일과 Java 25 스타일로 한 페이지씩.

### Java 8 스타일

```java
// 도메인 클래스 (Lombok 가정)
public class Order {
    private Long id;
    private String status;          // "PENDING", "PAID", "FAILED", "REFUNDED"
    private List<OrderItem> items;
    private Long customerId;
    // getter/setter/equals/hashCode (Lombok @Data)
}

public class OrderItem {
    private Long productId;
    private int quantity;
    private BigDecimal unitPrice;
}

// 처리 서비스
public class OrderService {
    private final ExecutorService executor =
        Executors.newFixedThreadPool(200);

    public CompletableFuture<List<OrderSummary>> processOrders(List<Order> orders) {
        List<CompletableFuture<OrderSummary>> futures = new ArrayList<>();
        for (Order order : orders) {
            CompletableFuture<OrderSummary> f =
                CompletableFuture.supplyAsync(() -> processOne(order), executor)
                    .exceptionally(ex -> {
                        log.error("failed: " + order.getId(), ex);
                        return null;
                    });
            futures.add(f);
        }
        return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
            .thenApply(v -> futures.stream()
                .map(CompletableFuture::join)
                .filter(Objects::nonNull)
                .collect(Collectors.toList()));
    }

    private OrderSummary processOne(Order order) {
        if (order == null || order.getStatus() == null) {
            throw new IllegalArgumentException("invalid order");
        }
        String status = order.getStatus();
        OrderSummary summary;
        if ("PAID".equals(status)) {
            summary = createPaidSummary(order);
        } else if ("FAILED".equals(status)) {
            summary = createFailedSummary(order);
        } else if ("REFUNDED".equals(status)) {
            summary = createRefundedSummary(order);
        } else if ("PENDING".equals(status)) {
            summary = createPendingSummary(order);
        } else {
            throw new IllegalStateException("unknown: " + status);
        }
        return summary;
    }
}
```

이 코드의 *찜찜한* 자리를 꼽아보자. 첫째, `status`가 `String`이다. 오타가 컴파일 타임에 안 잡힌다. 둘째, `if-else if` 사다리가 길고, 새 상태가 추가됐을 때 컴파일러가 안 알려준다. 셋째, `Lombok @Data`로 mutable getter/setter가 자동 생성된다 — DTO인데 mutable이다. 넷째, `ExecutorService.newFixedThreadPool(200)`이 *답답하다*. 200개로 어떻게 수만 건 트래픽을 받을까. 다섯째, `CompletableFuture.allOf(...)` + `join` + `filter(Objects::nonNull)`이 *번거롭다*. 부분 실패가 발생했을 때의 처리도 직관적이지 않다. 여섯째, `exceptionally(ex -> { log.error(...); return null; })`이 *조용한 실패*를 만든다. 일곱째, `Collectors.toList()`가 mutable list를 만든다 — Java 16 이전이라 `Stream::toList`가 없다.

### Java 25 스타일

```java
// 도메인: records + sealed
public sealed interface OrderStatus permits Pending, Paid, Failed, Refunded {}
public record Pending(Instant placedAt) implements OrderStatus {}
public record Paid(Instant paidAt, String txId) implements OrderStatus {}
public record Failed(Instant failedAt, String reason) implements OrderStatus {}
public record Refunded(Instant refundedAt, BigDecimal amount) implements OrderStatus {}

public record Order(
    long id,
    OrderStatus status,
    List<OrderItem> items,
    long customerId
) {}

public record OrderItem(long productId, int quantity, BigDecimal unitPrice) {}

// 처리 서비스
public class OrderService {
    private static final ScopedValue<Tenant> TENANT = ScopedValue.newInstance();

    public List<OrderSummary> processOrders(List<Order> orders, Tenant tenant)
            throws InterruptedException {
        return ScopedValue.callWhere(TENANT, tenant, () -> {
            try (var scope = StructuredTaskScope.open(
                    StructuredTaskScope.Joiner.<OrderSummary>allSuccessfulOrThrow())) {
                List<Subtask<OrderSummary>> tasks = orders.stream()
                    .map(o -> scope.fork(() -> processOne(o)))
                    .toList();
                scope.join();
                return tasks.stream().map(Subtask::get).toList();
            }
        });
    }

    private OrderSummary processOne(Order order) {
        return switch (order.status()) {
            case Paid(var paidAt, var txId) ->
                new OrderSummary(order.id(), "OK", "paid at " + paidAt + " (" + txId + ")");
            case Failed(var failedAt, var reason) ->
                new OrderSummary(order.id(), "ERR", "failed: " + reason);
            case Refunded(var refundedAt, var amount) ->
                new OrderSummary(order.id(), "REFUND", "refunded " + amount);
            case Pending(var placedAt) ->
                new OrderSummary(order.id(), "WAIT", "pending since " + placedAt);
        };
    }
}
```

같은 비즈니스 로직이지만 다섯 동력이 *모두* 한 자리에 모인다. 첫째 동력(함수형) — `Stream`·`map`·`toList()`·`record`의 deconstruction. 둘째 동력(데이터지향) — `sealed interface`·`record`·`switch` pattern matching의 exhaustiveness. 컴파일러가 새 상태가 추가됐을 때 자동으로 모든 switch를 *깨준다*. `default`가 *필요 없다*. 셋째 동력(동시성) — `StructuredTaskScope`로 자식 task의 lifecycle을 묶고, `ScopedValue`로 tenant 컨텍스트를 자식에게 안전하게 전달. 그 뒤에서 virtual thread가 *알아서* 수만 건을 처리. `newFixedThreadPool(200)`의 *답답함*이 사라진다. 넷째 동력(메모리·성능) — record + sealed의 작은 객체들이 Compact Object Headers 위에서 ~20% 가벼워지고, AOT cache로 startup이 빨라진다. 다섯째 동력(도구·언어 표면) — `var`로 타입 선언이 줄고, `switch expression`이 값을 돌려주며, deconstruction pattern으로 `Paid(var paidAt, var txId)`가 가능해진다.

물론 정직하게 짚자. 이 두 페이지는 *문법 비교*가 아니다. Java 25 스타일이 *왜* 더 나은지 — 왜 mutable getter/setter가 *찜찜한* 일인지, 왜 `String status`보다 sealed가 *안심되는*지, 왜 `newFixedThreadPool(200)`이 *답답한*지 — 그 *왜*를 채워주는 게 이 책의 본문이다. 5분 만에 옮길 수 있는 코드 변환표가 아니라, 11년의 자바 진화가 한 페이지의 코드 안에서 어떻게 만나는지 보여주는 *프리뷰*다.

## 다섯 동력은 책의 부 구조다

이제 책의 부 구조와 다섯 동력의 대응을 정리하자.

| 동력 | 책의 부 | 대표 챕터 |
|------|---------|----------|
| 함수형 | Part II, Part III | 3·4·5·6·7장 |
| 데이터지향 | Part VI | 11·12·13장 |
| 동시성 | Part IV(Loom 이전), Part VII(Loom 이후) | 8A·8B·14·15·16장 |
| 메모리·네이티브·성능 | Part VIII | 17·18·19·19A장 |
| 도구·언어 표면 | Part V | 9·10장 |

여기에 Part IX(마이그레이션·보안·Spring 시너지, 20·20A·21장), Part X(다음 자바, 22장), 그리고 처음의 Part I(지형도, 1·2장)이 더해진다. 다섯 동력이 책의 척추이고, 마이그레이션·미래·지형도가 그 척추를 둘러싼 *살*이다.

## 마무리 — 22장과의 약속

PayBridge의 11년을 함수형·데이터지향·동시성·성능·도구라는 다섯 갈래로 다시 읽으면, 무작위 사건의 나열이 *한 줄의 이야기*가 된다. Java 8의 람다가 PayBridge의 결제 정산 배치를 함수형 스타일로 옮겼고, Java 17의 records가 DTO를 다듬었으며, Java 21의 virtual thread가 thread-per-request를 부활시켰고, Java 25의 Compact Object Headers가 메모리 ~20%를 돌려줬고, 11년의 도구 진화가 빌드·프로파일링·배포 파이프라인의 모양을 바꿨다. 다섯 동력이 한 회사의 코드베이스 안에서 어떻게 결합되는지가 이 책의 핵심 줄거리다.

그리고 약속 하나. 22장 결말에서 다시 PayBridge로 돌아온다. 그때는 5년 뒤를 상상한다. *Project Valhalla*의 value types가 도착했을 때 records가 어떻게 바뀔지, *Project Amber*의 with-expressions·primitive type patterns이 ADT를 어떻게 더 풍부하게 만들지, *Project Babylon*의 code reflection이 metaprogramming을 어떻게 다시 그릴지, *Project Leyden*의 condensers가 startup을 어디까지 줄일지. 다섯 동력의 *다음 5년*을 PayBridge의 5년 뒤 코드 한 페이지로 함께 그려본다. 1장의 지도, 2장의 다섯 동력, 22장의 미래 — 이 셋이 책의 처음과 끝을 잇는 *수미상관*이다.

자, 다섯 동력의 지도를 손에 쥐었다. 다음 장에서는 첫째 동력의 가장 안쪽으로 들어가보자. 람다 — 그 익숙함의 진짜 의미를. PR 리뷰에서 6중 중첩 람다를 만났을 때의 *난감함*을 한번 들여다보자.
