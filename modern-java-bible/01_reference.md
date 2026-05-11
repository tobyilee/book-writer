# Modern Java Bible — 레퍼런스 문서

본 문서는 Java 8부터 Java 25까지의 언어·API·런타임 진화 전반을 다루는 "Modern Java Bible" 저술의 1차 참조 자료다. 대상 독자는 **Spring Framework로 엔터프라이즈 애플리케이션을 만드는 자바 개발자**이며, 따라서 단순한 스펙 나열보다 *어떤 변화가 실무에 어떻게 영향을 미치는가*를 기준으로 정리했다.

세 갈래(공식 자료·학술/스펙·실무 커뮤니티)의 자료를 통합했으며, 출처는 각 항목 옆에 URL로 명시하거나 6절(참고문헌)에 일괄 정리했다.

---

## 1. 개념과 정의

### 1.1 "Modern Java"란 무엇인가

"Modern Java"는 보통 두 가지를 의미한다.

1. **언어 패러다임의 확장:** Java 8(2014)의 람다·스트림·Optional·`java.time`을 기점으로, Java가 객체지향만의 언어에서 **함수형·데이터지향·동시성 친화적** 언어로 확장된 것을 가리킨다.
2. **릴리스 모델의 전환:** Java 9(2017) 이후 OpenJDK가 6개월 케이던스로 전환하면서, Java는 "한 번에 거대한 변화를 묶어 출시하는 언어"에서 "매년 두 차례 작은 변화를 누적하는 언어"가 됐다.

엔터프라이즈 자바 개발자에게 두 변화는 결합돼 있다. 람다와 스트림이 도입됐다는 사실보다, 그것이 6개월마다 다듬어지며 records·sealed·pattern matching·virtual threads로 이어지는 **연속체**라는 사실이 더 중요하다.

### 1.2 LTS 모델과 6개월 케이던스

Mark Reinhold(Java Chief Architect)가 2017년 9월에 제안한 모델은 다음과 같다 ([Moving Java Forward Faster](https://mreinhold.org/blog/forward-faster), [InfoQ 보도](https://www.infoq.com/news/2017/09/Java6Month/)).

- **Feature release**: 매년 3월·9월 (예: 9, 10, 11, …, 25). 누가 무엇을 가져갈지 미리 못 박지 않고 "준비된 JEP가 그 시점 릴리스에 합류"하는 **train model**.
- **LTS(Long-Term Support) release**: 처음에는 3년에 한 번(8, 11, 17)이었다가, 2021년부터 **2년에 한 번**(17, 21, 25, 29…)으로 단축됐다.
- **비-LTS는 6개월짜리**: 다음 릴리스가 나오면 공식 패치 지원이 끝난다.

Reinhold의 핵심 논거는 "Java 9가 JPMS 때문에 3년 가까이 지연됐다. 한 거대한 기능이 전체 릴리스를 인질로 잡는 구조를 깨야 한다"는 것이다. 이후 records·sealed·pattern matching이 여러 차례 preview를 거치며 6개월 단위로 다듬어진 사실이 이 모델의 효용을 증명한다.

엔터프라이즈 입장에서 의미는 단순하다.

- **LTS만 본다**: Java 8 → 11 → 17 → 21 → 25 라인을 따라가면 된다.
- **그러나 매년 릴리스를 추적할 가치**: preview 단계에서 피드백이 반영되므로, LTS에 features가 안착한 시점에는 이미 검증돼 있다.

JDK 17 이후로 OpenJDK 빌드 자체가 production-grade이며, Oracle·Amazon Corretto·Azul Zulu·Eclipse Temurin·BellSoft Liberica 등 여러 벤더가 LTS 패치를 제공한다.

### 1.3 책에서의 "Modern Java" 기준선

이 책은 **Java 8을 출발점, Java 25를 종착점**으로 잡되, Spring Boot 3.x 베이스라인(Java 17 이상)을 실무 적용의 기준선으로 본다 ([InfoQ: Spring Boot 3.2 / Spring 6.1](https://www.infoq.com/articles/spring-boot-3-2-spring-6-1/)).

---

## 2. 버전별 변화 매트릭스

각 버전의 굵직한 JEP만 정리했다. 자세한 의미론은 3절(횡단 주제)에서 다룬다.

### Java 8 (2014, LTS) — 함수형 패러다임의 도입

- **JSR 335 람다 표현식 + functional interface**: `Runnable`, `Function`, `Predicate`, `Supplier`, `Consumer`, `BiFunction`.
- **Stream API**: 컬렉션 위의 선언적 데이터 파이프라인. `parallelStream()`으로 ForkJoinPool 활용.
- **`Optional<T>`**: null 명시화 (단, 반환값 한정 사용이 권장).
- **`java.time`** (JSR-310, Stephen Colebourne): `Instant`, `LocalDate`, `ZonedDateTime`, `Duration`. `java.util.Date`/`Calendar`의 사실상 종말.
- **`CompletableFuture`**: 콜백 지옥을 푸는 비동기 조합기.
- **인터페이스 default·static 메서드**: 라이브러리 진화의 핵심 도구.
- **PermGen 제거 → Metaspace 도입**.

엔터프라이즈에서 가장 오래 살아남은 버전이다. 2025년 현재도 잔존 코드 베이스가 많다 ([Baeldung Java 8](https://www.baeldung.com/java-8-features)).

### Java 9 (2017) — 모듈과 정리

- **JEP 200/201/220/261: JPMS(Project Jigsaw)** — `module-info.java`, `requires`, `exports`, `opens`. ([JPMS Wikipedia](https://en.wikipedia.org/wiki/Java_Platform_Module_System))
- **JShell** (JEP 222): REPL.
- **Stream API 확장**: `takeWhile`, `dropWhile`, `iterate(seed, hasNext, next)`.
- **Collection factory**: `List.of(...)`, `Set.of(...)`, `Map.of(...)` (immutable).
- **`Optional.ifPresentOrElse`, `or`, `stream`**.
- **Reactive Streams 인터페이스** (`java.util.concurrent.Flow`) 표준화.
- **HTTP/2 Client API**: incubating (`jdk.incubator.http`).
- **Multi-release JAR** (JEP 238).

JPMS는 가장 야심차고 가장 논쟁적인 변경이다. 6절·논쟁점에서 다룬다.

### Java 10 (2018) — `var`

- **JEP 286: 지역 변수 타입 추론 (`var`)**. ([JEP 286](https://openjdk.org/jeps/286), [LVTI Style Guide](https://openjdk.org/projects/amber/guides/lvti-style-guide))
- **Application Class-Data Sharing(AppCDS)** (JEP 310).
- **G1 Parallel Full GC** (JEP 307).
- 6개월 케이던스의 첫 비-LTS.

### Java 11 (2018, LTS) — JDK 9·10의 안착과 Oracle 라이선스 변화

- **HttpClient 표준화** (JEP 321): `java.net.http`. HTTP/1.1·HTTP/2·WebSocket·HTTP/2 server push·동기/비동기 모두 지원. ([HttpClient Docs](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html))
- **String 메서드 확장**: `isBlank`, `lines`, `strip/stripLeading/stripTrailing`, `repeat`.
- **`Files.readString`/`writeString`**.
- **람다에서 `var`** (JEP 323): `(var x, var y) -> ...`.
- **JEP 320**: Java EE / CORBA 모듈 제거 — JAXB, JAX-WS, JTA, Activation 등. 마이그레이션 시 가장 큰 충격원.
- **ZGC 실험적 도입** (JEP 333), **Epsilon No-Op GC** (JEP 318).
- **Flight Recorder & Mission Control 오픈소스화** (JEP 328, 349).
- Oracle JDK 라이선스가 유료화되면서 OpenJDK·Corretto·Temurin로의 대이주가 발생.

### Java 12 (2019) — Switch Expressions(Preview)

- **JEP 325: Switch Expressions (Preview)** — `case L ->` arrow form, `yield`. ([JEP 361](https://openjdk.org/jeps/361))
- **JEP 189: Shenandoah GC (Experimental)**.
- **JEP 230: Microbenchmark Suite (JMH)**.

### Java 13 (2019) — Text Blocks(Preview)

- **JEP 355: Text Blocks (Preview)** — 삼중 따옴표 멀티라인 문자열.
- **JEP 354: Switch Expressions (Second Preview)** — `yield` 키워드 도입.
- **JEP 350: Dynamic CDS Archives**.

### Java 14 (2020) — Records(Preview), Pattern matching for instanceof(Preview)

- **JEP 359: Records (Preview)**.
- **JEP 305: Pattern Matching for `instanceof` (Preview)**.
- **JEP 361: Switch Expressions (Standard)** — 표준화.
- **JEP 343: Packaging Tool (`jpackage`)** (Incubator).
- **JEP 358: Helpful NullPointerExceptions** — NPE에 어떤 표현식이 null이었는지 자세히 표기.

### Java 15 (2020) — Sealed Classes(Preview), Text Blocks(Standard)

- **JEP 360: Sealed Classes (Preview)**.
- **JEP 378: Text Blocks (Standard)**.
- **JEP 339: Edwards-Curve Digital Signature Algorithm (EdDSA)**.
- **JEP 372: Nashorn 제거**.
- **JEP 379: Shenandoah Production-Ready**, **JEP 377: ZGC Production-Ready**.

### Java 16 (2021) — Records(Standard), Pattern matching for instanceof(Standard)

- **JEP 395: Records (Standard)**. ([JEP 395](https://openjdk.org/jeps/395))
- **JEP 394: Pattern Matching for `instanceof` (Standard)**.
- **JEP 397: Sealed Classes (Second Preview)**.
- **JEP 376: ZGC Concurrent Thread-Stack Processing**.
- **JEP 396: Strongly Encapsulate JDK Internals by Default** — `sun.misc.Unsafe` 등 내부 API 사용 시 경고/실패. 라이브러리 충격원.
- Mercurial → Git 이주, GitHub로 OpenJDK 코드 호스팅 이전.

### Java 17 (2021, LTS) — Sealed Classes 표준화, "post-Java 8 첫 LTS"

- **JEP 409: Sealed Classes (Standard)**. ([JEP 409](https://openjdk.org/jeps/409))
- **JEP 406: Pattern Matching for `switch` (Preview)**.
- **JEP 356: Enhanced Pseudo-Random Number Generators**.
- **JEP 412: Foreign Function & Memory API (Incubator)**.
- **JEP 414: Vector API (Second Incubator)**.
- **JEP 403: Strongly Encapsulate JDK Internals** — Java 16의 경고가 default로 강제.
- Spring Boot 3.0 (2022.11)의 베이스라인이 됨 — 사실상 엔터프라이즈의 "Java 8 다음 정착지".

### Java 18 (2022) — UTF-8 as default

- **JEP 400: UTF-8 by Default** — 파일 I/O의 기본 charset이 UTF-8로 통일. Windows에서 인코딩 깨짐 줄어듦.
- **JEP 408: Simple Web Server** (`jwebserver`).
- **JEP 413: Code Snippets in Java API Documentation** (`{@snippet}`).
- **JEP 416: Reimplement Core Reflection with Method Handles**.

### Java 19 (2022) — Virtual Threads(Preview)

- **JEP 425: Virtual Threads (Preview)** — Project Loom의 첫 표면화.
- **JEP 428: Structured Concurrency (Incubator)**.
- **JEP 405: Record Patterns (Preview)**.
- **JEP 422: Linux/RISC-V Port**.

### Java 20 (2023) — Virtual Threads(Second Preview)

- **JEP 436: Virtual Threads (Second Preview)**.
- **JEP 432: Record Patterns (Second Preview)**.
- **JEP 433: Pattern Matching for `switch` (Fourth Preview)**.
- **JEP 437: Structured Concurrency (Second Incubator)**.
- **JEP 429: Scoped Values (Incubator)**.

### Java 21 (2023, LTS) — Virtual Threads·Pattern Matching 표준화

- **JEP 444: Virtual Threads (Standard)**. ([JEP 444](https://openjdk.org/jeps/444))
- **JEP 441: Pattern Matching for `switch` (Standard)**. ([JEP 441](https://openjdk.org/jeps/441))
- **JEP 440: Record Patterns (Standard)**.
- **JEP 431: Sequenced Collections** — `SequencedCollection`, `SequencedSet`, `SequencedMap` 인터페이스로 "순서가 있는 컬렉션"의 첫·끝 원소 접근을 통일. `addFirst`, `addLast`, `reversed()`.
- **JEP 439: Generational ZGC**.
- **JEP 452: Key Encapsulation Mechanism API**.
- **JEP 453: Structured Concurrency (Preview)**. ([JEP 453](https://openjdk.org/jeps/453))
- **JEP 446: Scoped Values (Preview)**. ([JEP 446](https://openjdk.org/jeps/446))
- **JEP 442: Foreign Function & Memory API (Third Preview)**.
- **JEP 448: Unnamed Patterns and Variables (Preview)**.
- **JEP 430: String Templates (Preview)** — 이후 21에서 미리보기, 향후 재설계.

엔터프라이즈에서 **Java 8 → 17 → 21** 흐름이 표준이 됐다 ([InfoQ Java 21 release](https://www.infoq.com/news/2023/09/java21-released/), [Azul JDK 21](https://www.azul.com/blog/jdk-21-delivers-virtual-threads-other-new-features-and-long-term-support/)).

### Java 22 (2024) — FFM 표준화, Unnamed Variables 표준화

- **JEP 454: Foreign Function & Memory API (Standard)** — JNI 시대 종료의 시작. ([InfoQ Java 22](https://www.infoq.com/news/2024/03/java22-released/))
- **JEP 456: Unnamed Variables & Patterns** — `_` 사용.
- **JEP 461: Stream Gatherers (Preview)**. ([JEP 461](https://openjdk.org/jeps/461))
- **JEP 462: Structured Concurrency (Second Preview)**.
- **JEP 458: Launch Multi-File Source-Code Programs** — `java App.java` 하나로 여러 파일 실행.
- **JEP 423: Region Pinning for G1**.

### Java 23 (2024) — Markdown Javadoc, ZGC 세대화 default

- **JEP 467: Markdown Documentation Comments** — `///` 세 줄 슬래시로 Markdown javadoc. ([Java 23 release](https://www.infoq.com/news/2024/09/java23-released/))
- **JEP 473: Stream Gatherers (Second Preview)**.
- **JEP 474: ZGC: Generational Mode by Default**.
- **JEP 482: Flexible Constructor Bodies (Second Preview)** — `super(...)` 호출 전 statement 허용.
- **JEP 466: Class-File API (Second Preview)**.
- `sun.misc.Unsafe`의 메모리 접근 메서드 deprecation 강화 — MemorySegment(FFM)로 이주 권장.

### Java 24 (2025) — Stream Gatherers 표준화, AOT Class Loading

- **JEP 485: Stream Gatherers (Standard)** — 커스텀 intermediate operation. ([JEP 485](https://openjdk.org/jeps/485))
- **JEP 491: Synchronize Virtual Threads without Pinning** — `synchronized` 블록의 pinning 문제 해결. ([JEP 491](https://openjdk.org/jeps/491))
- **JEP 483: Ahead-of-Time Class Loading & Linking** — Project Leyden의 첫 가시적 결실. ([JEP 483 분석](https://www.morling.dev/blog/jep-483-aot-class-loading-linking/))
- **JEP 478: Key Derivation Function API (Preview)** — post-quantum 대응 준비.
- **JEP 484: Class-File API (Standard)**.
- **JEP 494: Module Import Declarations (Second Preview)** — `import module M;`.
- **JEP 489: Vector API (Ninth Incubator)** — Valhalla 대기 중.
- **JEP 487: Scoped Values (Fourth Preview)**.
- **JEP 499: Structured Concurrency (Fourth Preview)**.

### Java 25 (2025, LTS) — Compact Object Headers, AOT Cache 확장

- **JEP 519: Compact Object Headers** — 64-bit JVM의 object header를 96~128 비트에서 64 비트로 압축. 메모리·캐시 효율 ~22%, CPU 절감 사례 30% 보고. ([InfoQ Compact Object Headers](https://www.infoq.com/news/2025/06/java-25-compact-object-headers/), [Baeldung 해설](https://www.baeldung.com/java-object-header-reduced-size-save-memory))
- **JEP 521: Generational Shenandoah** — Shenandoah에도 세대형 GC.
- **JEP 514: Ahead-of-Time Command-Line Ergonomics** — AOT 사용 UX 정리.
- **JEP 515: Ahead-of-Time Method Profiling**.
- **JEP 505: Structured Concurrency (Fifth Preview)**.
- **JEP 506: Scoped Values (Standard)** — 마침내 표준화.
- **JEP 511: Module Import Declarations (Standard)**.
- **JEP 512: Compact Source Files and Instance Main Methods** — `void main()` 단독 실행 가능. 입문자 친화 + 스크립트 활용도.
- **JEP 510: Key Derivation Function API (Standard)**.
- **JEP 513: Flexible Constructor Bodies (Standard)**.

2025-09-16 GA ([Oracle: The Arrival of Java 25](https://blogs.oracle.com/java/the-arrival-of-java-25), [Inside.java 정리](https://inside.java/2025/10/17/new-in-jdk-25-2-mins/)).

### LTS 흐름 압축 요약

| LTS | 출시 | 사실상 의의 |
|---|---|---|
| 8 | 2014 | 함수형의 도입, 가장 오래 살아남은 베이스라인 |
| 11 | 2018 | "포스트 8" 첫 LTS, HttpClient·`var`·JEP 320(EE 제거) |
| 17 | 2021 | records·sealed·text blocks·pattern instanceof 표준화, Spring Boot 3 베이스라인 |
| 21 | 2023 | Virtual Threads·Pattern Matching for switch·Generational ZGC 표준화, 동시성 모델 전환점 |
| 25 | 2025 | Compact Object Headers·AOT Cache·Scoped Values 표준, 성능/시작시간 최적화의 LTS |

---

## 3. 횡단 주제

버전 간 시각이 아니라 *주제*별 시각이 책에 더 유용하다. 각 주제를 책의 한 챕터 단위로 다룰 만한 깊이로 정리했다.

### 3.1 함수형 패러다임의 도입과 진화

**핵심 흐름**

- Java 8: 람다 + `@FunctionalInterface` + `java.util.function`.
- Java 8: Stream API — `filter/map/reduce/collect`.
- Java 9: `takeWhile/dropWhile/iterate`.
- Java 16: `Stream::toList` — `collect(Collectors.toUnmodifiableList())` 대체.
- Java 22-24: **Stream Gatherers** (JEP 461 → 473 → 485) — 사용자 정의 intermediate 연산.

**Stream Gatherers의 의미**

기존 Stream은 `collect`(terminal)에서만 임의 확장이 가능했고, `map/filter/flatMap` 이외의 중간 변환은 불가능했다. Gatherer는 1:1, 1:N, N:1, N:N 변환을 표현하며, 내장 gatherer 5종 — `fold`, `scan`, `windowFixed`, `windowSliding`, `mapConcurrent` — 만으로도 그동안 "Stream에선 자연스럽지 않다"고 여겨졌던 패턴(슬라이딩 윈도우, prefix sum, 병렬 매핑)이 한 줄로 표현된다 ([Stream Gatherers Deep Dive](https://inside.java/2025/04/03/javaone-stream-gatherers/)).

**함정**: `parallelStream()`은 공용 `ForkJoinPool.commonPool()`을 사용한다. CPU-bound 작업의 컨텐션, blocking I/O로 인한 풀 고갈, 예측 불가한 latency spike가 흔하다 ([Baeldung: Custom Thread Pools in Parallel Streams](https://www.baeldung.com/java-8-parallel-streams-custom-threadpool), [JRebel: Take Caution Using Java Parallel Streams](https://www.jrebel.com/blog/parallel-java-streams)). 실무 권장: blocking I/O는 절대 `parallelStream`에 태우지 말 것, CPU-bound 작업에서도 작업 크기가 클 때만 사용.

### 3.2 데이터 지향 프로그래밍: Records + Sealed + Pattern Matching

**철학**

Brian Goetz의 "Data-Oriented Programming in Java" ([InfoQ](https://www.infoq.com/articles/data-oriented-programming-java/))는 명시적이다. **데이터는 불변으로, 행위는 분리하라.** 객체지향이 캡슐화로 데이터와 행위를 묶었다면, DOP는 다음 셋의 결합으로 그 반대편을 표현한다.

- **Records (JEP 395)** = **product type** — 컴포넌트의 카르티시안 곱.
- **Sealed classes (JEP 409)** = **sum type** — 허용된 대안의 합집합.
- **Pattern matching (JEP 394, 440, 441)** = ADT의 분해와 분기.

Records + Sealed = **대수적 데이터 타입(ADT)**. Pattern matching은 그 분해 도구다. Haskell·Scala·OCaml·Kotlin·Rust가 가진 표현력을 자바가 마침내 갖춘 것이다 ([Speaker Deck: ADTs for DOP — From Haskell and Scala to Java](https://speakerdeck.com/philipschwarz/algebraic-data-types-for-data-oriented-programming-from-haskell-and-scala-to-java)).

**예시: 표현식 평가기**

```java
sealed interface Expr permits Num, Add, Mul {}
record Num(int v) implements Expr {}
record Add(Expr l, Expr r) implements Expr {}
record Mul(Expr l, Expr r) implements Expr {}

int eval(Expr e) {
    return switch (e) {
        case Num(int v) -> v;
        case Add(Expr l, Expr r) -> eval(l) + eval(r);
        case Mul(Expr l, Expr r) -> eval(l) * eval(r);
    };
}
```

`default`가 필요 없는 이유: sealed가 `permits`로 닫혀 있고, 컴파일러가 exhaustiveness를 검증한다. 새 sub-type을 sealed에 추가하면 모든 switch가 컴파일 에러로 갱신을 요구한다 — Visitor 패턴이 그동안 해결하려 애썼지만 코드량 측면에서 실패했던 바로 그 일이다 ([JavaPro: Writing Readable Code with ADTs and Pattern Matching](https://javapro.io/2025/11/11/writing-readable-code-with-algebraic-data-types-and-pattern-matching-in-java/)).

**Records의 한계 (JPA)**

- Records는 `final` + 불변. JPA Entity는 mutable + no-args constructor + non-final 요구 → **Entity로 Records 사용 불가**.
- DTO·Value Object로는 이상적.
- 따라서 실무: **Entity는 Lombok / 클래식 클래스, DTO·Projection·Command는 Records** ([Baeldung: Java Record vs Lombok](https://www.baeldung.com/java-record-vs-lombok)).

**Lombok vs Records 논쟁**

- Records 우위: 언어 차원 보증, 컴파일러 인지, IDE/리플렉션 호환, 외부 어노테이션 프로세서 의존 없음.
- Lombok 우위: mutable, builder, `@Slf4j`·`@SneakyThrows`·`@Accessors` 등 다양성, JPA Entity 친화.
- Brian Goetz의 입장: Records는 Lombok의 *대체*가 아니다. Lombok이 "Java가 부족해서 메우는 패치"라면, Records는 "Java가 데이터 캐리어를 인정한 신원". 의도가 다르다 ([nipafx: Why Java's Records Are Better Than Lombok's @Data](https://nipafx.dev/java-record-semantics/)).

### 3.3 동시성 모델의 대전환: Virtual Threads (Project Loom)

**문제**

Java의 전통적 thread-per-request 모델은 OS thread = `java.lang.Thread`였다. Linux x64 기준 스택 ~1MB 예약, 컨텍스트 스위치 비용 크고, 수천 개까지가 한계. I/O-bound 웹앱은 대부분의 시간을 DB·외부 호출 대기에 쓰는데, 그 동안 OS thread는 idle인 채 자원만 점유했다 ([Oracle Java Magazine: Exploring the design of Java's new virtual threads](https://blogs.oracle.com/javamagazine/java-virtual-threads/)).

**해법: Virtual Threads (JEP 444)**

- `Thread.ofVirtual().start(...)` 또는 `Executors.newVirtualThreadPerTaskExecutor()`.
- JVM이 관리하는 lightweight thread. 스택은 heap에 작게 시작해 필요 시 grow.
- M:N 스케줄링: 다수 virtual thread가 소수의 **carrier(platform) thread**에 multiplex.
- Blocking 호출 시 자동 unmount → 다른 virtual thread가 carrier 점유.
- 수백만 개 생성 가능. "thread per request"를 다시 합리적으로 만든다.

Brian Goetz는 명명에 대해 "virtual memory의 비유"라고 설명했다: 물리 메모리보다 큰 환상의 메모리를 주듯, 물리 thread보다 많은 환상의 thread를 준다 ([Inside.java: Virtual Threads Explained](https://inside.java/2023/10/30/sip086/)).

**Go goroutine과의 비교**

| | Virtual Threads | Goroutines |
|---|---|---|
| 통신 모델 | 공유 메모리 + lock·CAS | 채널 (CSP) |
| 호환성 | 기존 `Thread` API 그대로 | 새 언어 차원 키워드(`go`) |
| 스케줄링 | M:N work-stealing carrier pool | M:N work-stealing |
| 도입 시점 | 2023 (JDK 21) | 2009 (Go 1.0) |

[Limits of Loom's Performance — SoftwareMill](https://softwaremill.com/limits-of-looms-performance/)에 따르면 Loom은 Go에 비교적 가까운 throughput을 달성한다. 결정적 차이는 "수십 년 묵은 Java 코드가 그대로 돈다"는 것이다.

**Pinning 문제와 JEP 491**

Virtual thread가 unmount 못 하는 상황을 **pinning**이라 한다.

- Java 21~23: `synchronized` 블록 내부 I/O는 pinning. 이유는 30년 묵은 JVM 모니터 구현(OS thread 신원 추적). HikariCP·Caffeine·Apache HttpClient·MySQL Connector/J 등 라이브러리들이 `synchronized` → `ReentrantLock` 이주로 대응. Netflix의 production deadlock 사례가 유명 ([Netflix Tech Blog post-mortem](https://netflixtechblog.com/), [TheServerSide: pinning problem](https://www.theserverside.com/tip/How-to-solve-the-pinning-problem-in-Java-virtual-threads)).
- Java 24 / JEP 491: JVM 모니터가 virtual thread 신원을 추적하도록 변경 → **`synchronized`도 unmount 가능**. JNI native call·class initializer 등 극히 일부만 pinning ([JEP 491](https://openjdk.org/jeps/491), [Mike My Bytes: Java 24 Thread Pinning Revisited](https://mikemybytes.com/2025/04/09/java24-thread-pinning-revisited/)).

**ThreadLocal 함정**

Virtual thread는 cheap하고 short-lived다. 따라서 ThreadLocal에 connection·SimpleDateFormat을 캐싱하는 옛 패턴은 "수백만 thread × 수백만 캐시 인스턴스"를 만든다. 답: **Scoped Values (JEP 506)** — JDK 25에서 표준화. 부모/자식 binding, immutable, 자동 cleanup.

**Structured Concurrency (JEP 453 → 533, 7차 preview까지 진행)**

`StructuredTaskScope`로 자식 task들을 단일 단위로 묶는다. 모두 성공/모두 실패/모두 취소가 보장. 부모 함수가 반환되기 전 자식이 모두 끝남 — "concurrent code도 sequential code처럼 구조를 갖춘다"는 Dijkstra의 structured programming을 재해석한 것 ([JEP 453](https://openjdk.org/jeps/453)).

**Spring Boot 3.2의 통합**

- `spring.threads.virtual.enabled=true` 한 줄로 Tomcat·Jetty의 request handler가 virtual thread로 ([Baeldung: Spring 6 Virtual Threads](https://www.baeldung.com/spring-6-virtual-threads), [Spring Blog: All Together Now](https://spring.io/blog/2023/09/09/all-together-now-spring-boot-3-2-graalvm-native-images-java-21-and-virtual/)).
- `@Async`·`@Scheduled`의 TaskExecutor도 virtual thread로 교체 가능.
- 다수 JDBC 드라이버(Postgres, Oracle, MySQL)가 Loom-ready로 갱신.

**실무 마이그레이션 경험들** (Reddit r/java, dev.to, Medium 등 집계)

- Cashfree Payments: "7 Key Lessons" — heap 설정 미흡으로 OOM, ThreadLocal 캐싱 폭증, pinning으로 deadlock ([Cashfree Blog](https://www.cashfree.com/blog/java-21-virtual-threads-lessons-production/)).
- "I/O-heavy 신규 프로젝트에는 즉시 도입. 기존 시스템은 audit이 우선."
- 모니터링: Java Flight Recorder의 `jdk.VirtualThreadPinned` 이벤트로 pinning을 추적할 것.

**한국 커뮤니티 사례**

- 우아한형제들: "Java의 미래, Virtual Thread" 기술 세미나 + 블로그 ([techblog.woowahan.com/15398/](https://techblog.woowahan.com/15398/), [/17163/](https://techblog.woowahan.com/17163/)).
- 카카오: 제4회 Kakao Tech Meet "JDK 21의 Virtual Thread" ([tech.kakao.com](https://tech.kakao.com/2023/12/22/techmeet-virtualthread/)).
- 카카오페이: "Virtual Thread에 봄(Spring)은 왔는가" — 실제 platform → virtual 전환 + 자원 소모 측정 ([tech.kakaopay.com](https://tech.kakaopay.com/post/ro-spring-virtual-thread/)).
- velog·findstar.pe.kr 등 개발자 블로그 다수.

### 3.4 모듈 시스템 (JPMS)

**의도**

- JAR Hell 해결 (classpath 충돌, split package, version 다중성).
- JDK의 strong encapsulation: `sun.misc.Unsafe`, internal API 비공개화.
- `jlink`로 runtime image 슬림화.

**실패한 이유** ([Java Code Geeks: Java Module System in 2026: Still Ignored, Still Relevant](https://www.javacodegeeks.com/2026/04/java-module-system-in-2026-still-ignored-still-relevant.html), [The ServerSide: JCP EC Votes against JPMS](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Java-modularitys-future-takes-a-hit-a-Project-Jigsaw-JPMS-is-voted-down), [InfoQ: JCP EC Rejected JPMS](https://www.infoq.com/news/2017/05/jpms-rejected/))

1. **너무 늦었다.** 2011년 약속이 2017년에야 도착. 그 사이 Maven/Gradle/OSGi가 dependency·encapsulation 문제를 충분히 해결.
2. **자동 모듈의 인지 부담.** explicit module + automatic module + classpath 혼합 시 가시성 규칙이 복잡.
3. **에러 메시지가 불친절.** "split package" 같은 상황의 진단이 어려움.
4. **IBM·Red Hat의 OSGi 진영 반대표.** JCP EC에서 한 차례 부결.
5. **Spring의 우회.** GraalVM native image + Spring AOT가 JPMS 없이도 runtime trimming을 달성.

**현재 상태**

JDK 자체는 모듈화되어 있지만, 애플리케이션 레벨에서 `module-info.java`를 도입한 라이브러리·프레임워크는 소수. Spring 6도 modular jar 형태로 제공하지 않는다. JPMS는 "JDK 내부의 도구"로 남았다.

### 3.5 GC의 진화

| GC | 도입 | 특징 | 권장 사례 |
|---|---|---|---|
| Serial | 초기 | single-threaded, stop-the-world | embedded, single CPU |
| Parallel | 1.4 | throughput 우선 | batch |
| CMS | 1.4 (deprecated 9, removed 14) | concurrent old-gen | 옛 latency-sensitive |
| **G1** | 7 (default 9+) | region-based, predictable pause | 일반 enterprise default |
| **ZGC** | 11 experimental, 15 production | colored pointers, sub-ms pause, multi-TB | 대용량 heap, low-latency |
| **Generational ZGC** | 21 (JEP 439), default 23 (JEP 474) | ZGC + 세대 분리, throughput ~10% 향상 | 21+ default for low-latency |
| **Shenandoah** | 12 experimental, 15 production | Red Hat, concurrent compaction | Red Hat ecosystem |
| **Generational Shenandoah** | 25 (JEP 521) | Shenandoah + 세대 | 25+ |
| Epsilon | 11 | no-op | 테스트 |

**선택 가이드** ([IBM Community: G1/Shenandoah/ZGC](https://community.ibm.com/community/user/blogs/theo-ezell/2025/09/03/g1-shenandoah-and-zgc-garbage-collectors), [foojay: 10-year GC guide](https://foojay.io/today/the-ultimate-10-years-java-garbage-collection-guide-2016-2026-choosing-the-right-gc-for-every-workload/))

- 1~4GB heap, 일반 throughput → **G1** (default).
- ≥8GB heap + p99 latency 민감 → **Generational ZGC** (sub-ms pause).
- Red Hat 환경 / OpenJDK distro → **Generational Shenandoah**.
- Kubernetes pod 메모리 limit이 빠듯 → 주의. ZGC/Shenandoah는 off-heap 메타데이터가 필요해 G1보다 OOM risk가 높다.

**Compact Object Headers (JEP 519, Java 25)**

64비트 JVM의 모든 객체에는 96~128비트의 헤더(mark word + klass pointer)가 붙는다. JEP 519는 이를 64비트로 압축. 효과:

- 작은 객체가 많은 워크로드(예: 캐시, JSON 파싱)에서 heap 사용량 ~10~22% 감소.
- 캐시 라인 효율 향상, GC 압력 감소.
- 일부 측정에서 CPU 절감 30% 보고 ([InfoQ JEP 519](https://www.infoq.com/news/2025/06/java-25-compact-object-headers/), [Coding Steve: Should I Use Compact Object Headers?](https://stevenpg.com/posts/should-i-use-java-25-compact-object-headers/)).

### 3.6 네이티브 인터페이스: Foreign Function & Memory API

**JNI의 한계**

- 거대한 boilerplate (`*.h` 작성 → header 추출 → C 코드 → `System.loadLibrary`).
- GC와 충돌 (`Get*Critical` 등).
- 자원 누수·crash가 JVM 전체 다운.

**FFM (JEP 442 → 454, Java 22 표준화)**

- `MemorySegment`: 명시적·범위 한정된 native memory.
- `Arena`: lifetime 관리 (try-with-resources).
- `Linker`: 함수 시그니처 → method handle.
- `jextract`: C header → Java 바인딩 자동 생성.

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
    // ... use ...
} // 메모리 자동 해제
```

**Project Panama의 야망**: JNI를 점진적으로 대체, GPU·SIMD·DPDK 같은 native ecosystem과 자바를 잇는다 ([dzone: Java's Future-Looking Projects](https://dzone.com/articles/javas-future-looking-projects-panama-loom-amber-an)).

### 3.7 Vector API (SIMD)

**JEP 338(Java 16 첫 incubator) → JEP 489(Java 24 9th incubator)** — 아직 표준화 안 됨. Valhalla의 value types를 기다리는 중.

용도: 행렬 연산, 벡터화 가능한 numeric loop, ML inference. AVX2·AVX-512·NEON·SVE 자동 매핑. Stuart Marks의 표현으로 "Java가 마침내 SIMD를 표현할 수 있게 됐다".

### 3.8 시작 시간과 메모리: AOT/CDS/Leyden

**옛 답**: GraalVM Native Image. Reflection·dynamic class loading의 closed-world 가정 + 별도 메타데이터(reachability metadata).

**OpenJDK 답** ([Spring Blog: CDS support and Leyden anticipation](https://spring.io/blog/2024/08/29/spring-boot-cds-support-and-project-leyden-anticipation/), [Java Code Geeks: Leyden's AOT Code Cache](https://www.javacodegeeks.com/2026/03/project-leydens-aot-code-cache-how-java-is-solving-its-cold-start-problem-without-graalvm.html))

- **AppCDS** (10): class metadata 캐시.
- **Dynamic CDS** (13): 단일 run으로 archive 생성.
- **JEP 483 (24)**: Ahead-of-Time **Class Loading & Linking** — class를 init·link해서 캐시.
- **JEP 514·515 (25)**: AOT CLI ergonomics, AOT method profiling.
- **Leyden premain branch**: AOT code compilation, AOT proxy generation.

**Spring Boot 3.3+의 통합**

- training run으로 AOT cache 생성 → 다음 실행부터 적용.
- Spring Petclinic 기준 startup 36~42% 단축.
- Spring AOT(빌드 타임 BeanFactory 사전 계산) + JDK AOT(JVM 캐시) 조합으로 ~4배 startup 개선 보고.

엔터프라이즈 의미: serverless·짧은 lifecycle·rolling deploy에서 JVM이 부담이 아니게 됐다. "GraalVM 없이도 빠른 startup."

### 3.9 패턴 매칭과 type system

진행:

- Java 16 (JEP 394): `instanceof` 패턴.
- Java 21 (JEP 440): record 패턴 (deconstruction).
- Java 21 (JEP 441): switch 패턴 + sealed exhaustiveness.
- Java 22 (JEP 456): unnamed pattern·variable (`_`).
- Future: primitive type patterns, array patterns, with-expressions (Project Amber).

이 진화는 **type theory의 ADT**가 자바로 들어오는 과정 그 자체다.

### 3.10 도구 생태계의 변화

- **JShell** (9): REPL.
- **jpackage** (16): native installer 생성.
- **jwebserver** (18): 간단 HTTP 서버.
- **jextract** (Panama): C header → Java binding.
- **JFR + JMC** (11+, open-source): production-grade profiling.
- **Markdown javadoc** (23, JEP 467): `///` 코멘트.
- **Module Import Declarations** (25, JEP 511): `import module java.base;`.
- **Compact Source Files + Instance Main** (25, JEP 512): `void main()` 단독 실행 → 입문/스크립트.

---

## 4. JLS·스펙 인용 풀 (책에서 쓸 만한 발췌)

이 절은 책에서 정확성을 살려 인용할 수 있도록, 가급적 원전(JLS, JEP)을 기준으로 정리한다. 페이지·섹션 번호는 JLS 17(JSR 392), JLS 21(JSR 396), JLS 25 기준이다.

### 4.1 Records (JLS §8.10, JEP 395)

> A record class is a special kind of class that acts as a transparent carrier for shallowly immutable data. The components of a record class declaration are the variables that comprise its state. — *JEP 395*

핵심 속성:

- `final` class. `extends Record` 자동 부여.
- 컴포넌트마다 `private final` field + accessor (`name()`) + canonical constructor.
- `equals`/`hashCode`/`toString` 자동 — 컴포넌트 기반.
- compact constructor로 validation 가능: `public Point { if (x < 0) throw ...; }`.

### 4.2 Sealed Classes (JLS §8.1.1.2, JEP 409)

> A sealed class or interface restricts which other classes or interfaces may extend or implement it. — *JEP 409*

- `sealed` + `permits A, B, C`.
- 허용된 sub-type은 같은 모듈(or unnamed module이면 같은 패키지) 안에 있어야 함.
- Sub-type은 정확히 `final`, `sealed`, 또는 `non-sealed` 중 하나여야 함.
- `instanceof` switch에서 exhaustiveness 결정에 활용.

### 4.3 Pattern Matching for switch (JLS §14.30, JEP 441)

> A `switch` block is exhaustive if it has no `default` clause and the set of patterns in its case labels covers all possible values of the selector expression. — *JEP 441*

- `null`을 case로 적을 수 있다: `case null -> ...`.
- guard: `case Point p when p.x() > 0 -> ...`.
- synthetic default: sealed type이라도, separate compilation 때문에 매칭되지 않을 수 있는 런타임 상황을 위해 컴파일러가 `MatchException`을 던지는 default를 삽입.

### 4.4 Text Blocks (JLS §3.10.6, JEP 378)

> A text block is a multi-line string literal that avoids the need for most escape sequences. — *JEP 378*

- `"""` opening delimiter는 새 줄로 끝나야 함.
- incidental whitespace는 자동 제거 (closing `"""`의 들여쓰기를 기준).
- `\` line continuation으로 줄바꿈 제거 가능.

### 4.5 Local Variable Type Inference (JEP 286)

> The `var` reserved type name appears only in local variable declarations with initializers, and in the formal parameters of implicitly typed lambda expressions. — *JEP 286*

- 필드·메서드 시그니처에는 사용 불가. 의도적으로 좁게 한정.
- LVTI Style Guide ([OpenJDK Amber LVTI Style Guide](https://openjdk.org/projects/amber/guides/lvti-style-guide)): "코드는 self-revealing해야 한다. 타입이 RHS에서 명확할 때만 var."

### 4.6 Virtual Threads (JEP 444)

> A virtual thread is an instance of `java.lang.Thread` that is not tied to a particular OS thread. A platform thread, by contrast, is a `Thread` implemented in the traditional way, as a thin wrapper around an OS thread. — *JEP 444*

- 모든 virtual thread는 daemon. `setDaemon(false)`는 `IllegalArgumentException`.
- priority 무시.
- thread group은 single shared "VirtualThreads" group.

### 4.7 Memory Model (JSR 133, JLS §17.4)

JSR 133 (Manson·Pugh, 2004)는 Java 5에 도입돼 현재까지 변경 없다. 핵심 개념:

- **happens-before**: 두 액션 A·B에 대해 A가 B보다 먼저 발생함을 보장.
- volatile read/write, monitor enter/exit, `Thread.start`/`join`, final field 등이 happens-before 관계를 생성.
- causality model: pure happens-before로는 "out-of-thin-air" 값을 허용해 버리므로, JLS는 well-formed execution 정의를 통해 이를 보강.

원전: [JSR-133 PDF](https://www.cs.umd.edu/~pugh/java/memoryModel/jsr133.pdf), [JSR 133 FAQ](https://www.cs.umd.edu/~pugh/java/memoryModel/jsr-133-faq.html), [JSR-133 Cookbook](https://gee.cs.oswego.edu/dl/jmm/cookbook.html).

### 4.8 Sequenced Collections (JEP 431)

> A sequenced collection is a collection whose elements have a defined encounter order. It has a well-defined first element, a well-defined last element, and the elements between them have well-defined successors and predecessors.

- 새 인터페이스: `SequencedCollection<E>`, `SequencedSet<E>`, `SequencedMap<K,V>`.
- 새 메서드: `addFirst`, `addLast`, `getFirst`, `getLast`, `removeFirst`, `removeLast`, `reversed()`.

---

## 5. 실무 시나리오·사례

### 5.1 Spring Boot 3.x로의 이주 — Java 8 → 17

Spring Boot 3.0(2022.11)이 Java 17을 baseline으로 정한 것은 산업적 사건이었다. 이전까지 "Java 11도 안 쓰고 8에 머물던" 다수의 엔터프라이즈가 강제 이주를 시작.

**대표 함정** ([Aviator: Java Version Upgrade](https://www.aviator.co/blog/java-version-upgrade/), [Bell-SW: Migration from Java 8 to 17](https://bell-sw.com/blog/migration-from-java-8-to-java-17/), [CleverTap Tech Blog: Pitfalls When Upgrading from Java 8 to Java 17](https://tech.clevertap.com/pitfalls-when-upgrading-from-java-8-to-java-17/))

1. **JEP 320(11)의 흔적**: JAXB·JAX-WS·CORBA·`javax.annotation` 사용 코드는 별도 의존성으로 분리. `jakarta.*`로 패키지 rename(Spring 6).
2. **strong encapsulation**: `sun.misc.Unsafe`, `--add-opens`, `--add-exports` 필요한 라이브러리 (예: 옛 Mockito, ByteBuddy 옛 버전).
3. **Nashorn 제거(15)**: JS 스크립트 평가에 Nashorn 의존한 코드는 GraalVM JS로 이주.
4. **Docker RSS 증가**: G1 + JFR + Metaspace 합산으로 컨테이너 메모리 limit 상향 필요. CleverTap 사례에서 Docker OOM kill 빈발.
5. **빌드 도구 업그레이드**: Maven 3.6.3 미만, Gradle 7.3 미만은 17 미지원. Lombok도 1.18.22+ 필요.
6. **Spring 5 → 6**: `javax.servlet` → `jakarta.servlet`, `javax.persistence` → `jakarta.persistence`. Tomcat 10+, Jetty 11+ 필수.

**경험적 권장 순서**

1. JDK만 17로 올린 채 코드 빌드 — 경고/오류 식별.
2. JEP 320 잔재 의존성 외부화.
3. Lombok·Mockito·Hibernate·DB driver 등 핵심 라이브러리 버전 정렬.
4. Spring Boot 2.7 → 3.0(jakarta namespace 변환).
5. 단계적으로 `records`, `var`, `switch expression` 도입.
6. 그 다음 Spring Boot 3.2 + Java 21 + virtual threads.

### 5.2 Virtual Threads 도입 시나리오

**적합한 곳**

- I/O bound HTTP API server. JDBC·외부 API 호출 비중이 높은 서비스.
- Webhook receiver / fanout — 수만 동시 작업.
- Long-polling, SSE.

**부적합/주의**

- CPU bound 작업 — 효과 없음. `ForkJoinPool` 또는 GPU.
- `synchronized` 무거운 라이브러리 사용 (Java 21~23). JEP 491(24)로 해결되지만, 이중 LTS인 21에 머문다면 대안 검토 — HikariCP 5.x, Apache HttpClient 5.x 최신 등.
- ThreadLocal heavy 패턴 — Scoped Values로 이주 권장.
- pinning 모니터링: `-Djdk.tracePinnedThreads=full`, JFR `jdk.VirtualThreadPinned` 이벤트.

**Spring Boot 적용**

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

이 한 줄로 Tomcat의 `TaskExecutor`가 virtual thread per request로. WebFlux는 다른 모델(Reactor)이라 직접 영향 없음.

**예시 워크로드**

기존: Tomcat 200 thread pool, p99 800ms.
Virtual thread 적용: 동일 부하에서 p99 200ms, throughput 3~5x. 단 heap 사용량 ~30% 증가 (stack이 heap에 살기 때문).

### 5.3 Records의 실전 사용처

- **DTO**: API request/response. Jackson은 records 직접 지원.
- **Projection/Query result**: Spring Data JPA의 interface-based projection 대안.
- **Command·Event**: CQRS·event-sourced 시스템.
- **Value Object**: DDD의 VO 자연스럽게.
- **불변 configuration**: `@ConfigurationProperties`와 records 호환.

**금기**: JPA `@Entity`. 위에서 설명한 이유로.

### 5.4 Pattern Matching의 실전

- API 응답 매핑: sealed result type + switch.
- domain event 처리: `sealed interface UserEvent permits Created, Updated, Deleted`.
- ANTLR/parser 트리 traversal — Visitor 대체.
- error handling: `sealed interface Result<T,E> permits Ok, Err`.

### 5.5 Stream Gatherers의 실전

- **Rate limiting**: `mapConcurrent(maxInFlight, async)`로 동시성 제한 매핑.
- **Sliding window 통계**: 시계열의 5분 이동 평균.
- **Prefix sum**: 누적 잔액·누적 카운터.
- **Batch grouping**: `windowFixed(100)`으로 bulk insert 묶기.

### 5.6 GC 선택 시나리오

- Spring Boot REST API, heap 2~4GB, k8s → **G1 default**, `-XX:+UseG1GC`, `-XX:MaxGCPauseMillis=200`.
- 대용량 캐시(50GB+), p99 latency 민감 → **Generational ZGC** (Java 21+), `-XX:+UseZGC -XX:+ZGenerational`.
- 짧은 lifecycle batch → **Parallel GC** (throughput).
- 정말 짧은 lifecycle, GC 자체가 부담 → **Epsilon** + 충분한 heap.

### 5.7 AOT/Leyden 시나리오

- Lambda/Cloud Run/Knative 콜드 스타트 — Spring Boot 3.3 + CDS + JEP 483(24).
- training run을 CI에서 한 번 → cache 아티팩트 배포.
- GraalVM native image와의 트레이드오프: native는 더 빠르지만 reflection·dynamic class loading 제약. AOT cache는 동일 JVM이라 기존 코드 그대로.

---

## 6. 논쟁점·상충 관점

### 6.1 JPMS — 실패인가 미완인가

**관점 A (실패론)**: 12년 늦었고, 자동 모듈 매트릭스가 복잡하고, 에러 메시지가 불친절. 엔터프라이즈 코드 중 `module-info.java` 작성한 곳을 거의 본 적 없다.

**관점 B (잠재 가치론)**: JDK 자체가 모듈화돼 `jlink`로 슬림 JRE를 만든다. strong encapsulation이 `sun.misc.Unsafe`를 제거하는 동력. 라이브러리들은 일부라도 modular jar로 진화 중.

[Java Code Geeks: Module System in 2026 Still Ignored, Still Relevant](https://www.javacodegeeks.com/2026/04/java-module-system-in-2026-still-ignored-still-relevant.html)는 두 관점을 병기한다 — "ignored at app level, but still essential at JDK level."

### 6.2 `var` — 가독성 향상인가 후퇴인가

**관점 A**: `Map<String, List<Pair<Integer, Customer>>> data = new HashMap<>();` 보다 `var data = new HashMap<String, List<Pair<Integer, Customer>>>();` 가 낫다. Boilerplate를 줄인다.

**관점 B**: 함수 호출의 반환 타입이 IDE 없이 안 보인다. PR diff가 어려워진다. C#·Kotlin과 달리 Java는 30년간 explicit 문화였다.

OpenJDK 공식 [LVTI Style Guide](https://openjdk.org/projects/amber/guides/lvti-style-guide)는 후자에 가깝게 균형을 잡는다: "코드는 도구 없이도 자명해야 한다."

### 6.3 Virtual Threads — 모든 reactive를 대체할까

**관점 A (대체론)**: WebFlux/Reactor의 복잡성(operators 학습, debugging 난해, stack trace 불친절)을 virtual thread가 해소. blocking I/O를 다시 쓸 수 있다.

**관점 B (보완론)**: backpressure, hot/cold stream, 명시적 cancel/replay 같은 reactive의 도구는 virtual thread가 못 준다. 진정한 streaming(예: server-sent events, kafka consumer fan-out)은 여전히 Reactor·RxJava가 자연스럽다.

[SoftwareMill: Limits of Loom's Performance](https://softwaremill.com/limits-of-looms-performance/)도 양면 모두 인정.

### 6.4 Records vs Lombok

**관점 A (Records 우위)**: 언어 차원 + 컴파일러 인지 + 외부 의존성 없음 + IDE 호환.

**관점 B (Lombok 잔존)**: mutable, builder, JPA Entity. 거대 codebase의 `@Data`·`@Slf4j` 등 변경 비용 크다.

실무 정착: **DTO는 records, Entity는 Lombok, 신규 코드는 records 우선**.

### 6.5 Project Amber의 속도 — 빠른가 신중한가

**관점 A (빠르다)**: 6개월 케이던스 + preview 다라운드 — records가 14에 등장해 16에 표준, 5개 LTS를 가로지름. 자바답지 않다.

**관점 B (신중하다)**: 같은 records가 표준화까지 2년. preview의 의미가 바로 그것 — 산업 피드백을 받아 다듬을 수 있다. 그 결과 records는 도입 후에도 거의 부작용 없이 정착.

### 6.6 String Templates의 좌초

JEP 430(21 preview), 459(22 preview)로 등장한 후 **Java 23에서 철회**. STR\."Hello \{name}" 문법이 prefix 처리·null·이스케이프 의미론에서 충분히 일관되지 않다는 판단. 향후 새 디자인으로 재시도 예정. 이는 "preview 단계의 자정" 사례로 자주 인용된다.

### 6.7 Generational ZGC 기본화 — 적절한가

**관점 A**: 23에서 generational mode가 default. 대부분의 워크로드(young die fast)에 유리.

**관점 B**: small heap·short lifecycle batch에서는 단일 세대 ZGC가 단순. 또한 generational mode의 메모리 오버헤드.

기본값 변경의 자세한 의도는 [JEP 474](https://openjdk.org/jeps/474)에 명시. "대다수에 더 나으므로 default."

---

## 7. 참고문헌

### OpenJDK 공식 JEP

- [JEP 286: Local-Variable Type Inference](https://openjdk.org/jeps/286)
- [JEP 361: Switch Expressions](https://openjdk.org/jeps/361)
- [JEP 378: Text Blocks](https://openjdk.org/jeps/378)
- [JEP 395: Records](https://openjdk.org/jeps/395)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409)
- [JEP 431: Sequenced Collections](https://openjdk.org/jeps/431)
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 442: Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 446: Scoped Values (Preview)](https://openjdk.org/jeps/446)
- [JEP 453: Structured Concurrency (Preview)](https://openjdk.org/jeps/453)
- [JEP 454: Foreign Function & Memory API](https://openjdk.org/jeps/454)
- [JEP 456: Unnamed Variables & Patterns](https://openjdk.org/jeps/456)
- [JEP 461: Stream Gatherers (Preview)](https://openjdk.org/jeps/461)
- [JEP 462: Structured Concurrency (Second Preview)](https://openjdk.org/jeps/462)
- [JEP 467: Markdown Documentation Comments](https://openjdk.org/jeps/467)
- [JEP 474: ZGC: Generational Mode by Default](https://openjdk.org/jeps/474)
- [JEP 483: Ahead-of-Time Class Loading & Linking](https://openjdk.org/jeps/483)
- [JEP 485: Stream Gatherers](https://openjdk.org/jeps/485)
- [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491)
- [JEP 494: Module Import Declarations (Second Preview)](https://openjdk.org/jeps/494)
- [JEP 506: Scoped Values (Standard)](https://openjdk.org/jeps/506)
- [JEP 511: Module Import Declarations (Standard)](https://openjdk.org/jeps/511)
- [JEP 512: Compact Source Files and Instance Main Methods](https://openjdk.org/jeps/512)
- [JEP 519: Compact Object Headers](https://openjdk.org/jeps/519)
- [JEP 521: Generational Shenandoah](https://openjdk.org/jeps/521)
- [OpenJDK Project Amber](https://openjdk.org/projects/amber/)
- [OpenJDK Amber LVTI Style Guide](https://openjdk.org/projects/amber/guides/lvti-style-guide)
- [OpenJDK Amber LVTI FAQ](https://openjdk.org/projects/amber/guides/lvti-faq)

### Oracle 공식 문서

- [Oracle: Significant Changes in JDK 21](https://docs.oracle.com/en/java/javase/24/migrate/significant-changes-jdk-21.html)
- [Oracle: Significant Changes in JDK 22](https://docs.oracle.com/en/java/javase/24/migrate/significant-changes-jdk-22.html)
- [Oracle: Significant Changes in JDK 23](https://docs.oracle.com/en/java/javase/24/migrate/significant-changes-jdk-23.html)
- [Oracle: Significant Changes in JDK 24](https://docs.oracle.com/en/java/javase/24/migrate/significant-changes-jdk-24.html)
- [Oracle: Migrating from JDK 8](https://docs.oracle.com/en/java/javase/17/migrate/migrating-jdk-8-later-jdk-releases.html)
- [Oracle: Virtual Threads](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html)
- [Oracle: Pattern Matching for switch (Java 21)](https://docs.oracle.com/en/java/javase/21/language/pattern-matching-switch.html)
- [Oracle: Java SE 21 Language Updates PDF](https://docs.oracle.com/en/java/javase/21/language/java-se-language-updates.pdf)
- [Oracle: Java SE 25 Language Updates PDF](https://docs.oracle.com/en/java/javase/25/language/java-se-language-updates.pdf)
- [Oracle: Stream Gatherers (Java 24)](https://docs.oracle.com/en/java/javase/24/core/stream-gatherers.html)
- [Oracle: HttpClient (Java 11)](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html)
- [Oracle Releases Java 24](https://www.oracle.com/europe/news/announcement/oracle-releases-java-24-2025-03-18/)
- [Oracle Blog: The Arrival of Java 25](https://blogs.oracle.com/java/the-arrival-of-java-25)

### Inside.java & Java Magazine

- [Inside.java: Virtual Threads Explained](https://inside.java/2023/10/30/sip086/)
- [Inside.java: Pattern Matching for switch](https://inside.java/2023/11/13/sip088/)
- [Inside.java: What's New in JDK 25 in 2 mins](https://inside.java/2025/10/17/new-in-jdk-25-2-mins/)
- [Inside.java: Stream Gatherers Deep Dive](https://inside.java/2025/04/03/javaone-stream-gatherers/)
- [Inside.java: Java's Plans for 2025](https://inside.java/2025/01/16/newscast-83/)
- [Inside.java: 2025 in Review (Newscast 103)](https://inside.java/2025/12/18/newscast-103/)
- [Inside.java: Brian Goetz posts](https://inside.java/u/BrianGoetz/)
- [Inside.java: Loom tag](https://inside.java/tag/loom)
- [Java Magazine: Exploring the Design of Java's New Virtual Threads](https://blogs.oracle.com/javamagazine/java-virtual-threads/)

### 학술 / 스펙

- [JSR-133 PDF (Java Memory Model)](https://www.cs.umd.edu/~pugh/java/memoryModel/jsr133.pdf)
- [JSR-133 FAQ](https://www.cs.umd.edu/~pugh/java/memoryModel/jsr-133-faq.html)
- [JSR-133 Cookbook (Doug Lea)](https://gee.cs.oswego.edu/dl/jmm/cookbook.html)
- [JSR-133 Semantic Scholar entry](https://www.semanticscholar.org/paper/JSR-133:-Java-Memory-Model-and-Thread-Specification-Manson-Pugh/a919d184b170eb514d3871afb1ff42688f4642e1)
- [Speaker Deck: Algebraic Data Types for Data-Oriented Programming (Philip Schwarz)](https://speakerdeck.com/philipschwarz/algebraic-data-types-for-data-oriented-programming-from-haskell-and-scala-to-java)

### Brian Goetz, Stuart Marks 등 권위 있는 블로그·아티클

- [Mark Reinhold: Moving Java Forward Faster](https://mreinhold.org/blog/forward-faster)
- [InfoQ: Java to Move to 6-Monthly Release Cadence](https://www.infoq.com/news/2017/09/Java6Month/)
- [InfoQ: Data-Oriented Programming in Java (Brian Goetz)](https://www.infoq.com/articles/data-oriented-programming-java/)
- [InfoQ: Brian Goetz on Data Classes for Java](https://www.infoq.com/news/2018/02/data-classes-for-java/)
- [InfoQ: Java 21 Released](https://www.infoq.com/news/2023/09/java21-released/)
- [InfoQ: Java 22 Released](https://www.infoq.com/news/2024/03/java22-released/)
- [InfoQ: Java 23 Released](https://www.infoq.com/news/2024/09/java23-released/)
- [InfoQ: JEP 519 Compact Object Headers](https://www.infoq.com/news/2025/06/java-25-compact-object-headers/)
- [InfoQ: Spring Boot 3.2 / Spring 6.1](https://www.infoq.com/articles/spring-boot-3-2-spring-6-1/)
- [InfoQ: JCP EC Votes against JPMS](https://www.infoq.com/news/2017/05/jpms-rejected/)
- [InfoQ: Oracle Defends the Java Module System](https://www.infoq.com/news/2017/06/oracle-defends-jpms/)
- [InfoQ: Virtual Threads Arrive in JDK 21](https://www.infoq.com/news/2023/04/virtual-threads-arrives-jdk21/)
- [InfoQ: JEP 441 Pattern Matching for switch](https://www.infoq.com/news/2023/07/tranforming-java-pattern/)
- [InfoQ: Project Loom presentation](https://www.infoq.com/presentations/loom-java-concurrency/)
- [nipafx: Inside Java Newscast 83 — Plans for 2025](https://nipafx.dev/inside-java-newscast-83/)
- [nipafx: Inside Java Newscast 61 — Plans for 2024](https://nipafx.dev/inside-java-newscast-61/)
- [nipafx: Newscast 40 — Plans for 2023](https://nipafx.dev/inside-java-newscast-40/)
- [nipafx: Newscast 29 — Data-Oriented Programming](https://nipafx.dev/inside-java-newscast-29/)
- [nipafx: project-amber overview](https://nipafx.dev/project-amber/)
- [nipafx: project-valhalla overview](https://nipafx.dev/project-valhalla/)
- [nipafx: Why Java's Records Are Better Than Lombok's @Data](https://nipafx.dev/java-record-semantics/)
- [nipafx: First Contact with var in Java 10](https://nipafx.dev/java-10-var-type-inference/)
- [Gunnar Morling: JEP 483 AOT Class Loading & Linking](https://www.morling.dev/blog/jep-483-aot-class-loading-linking/)
- [Mike My Bytes: Java 24 Thread Pinning Revisited](https://mikemybytes.com/2025/04/09/java24-thread-pinning-revisited/)

### Spring / 프레임워크

- [Spring Blog: All Together Now — Spring Boot 3.2, GraalVM, Java 21, Virtual Threads](https://spring.io/blog/2023/09/09/all-together-now-spring-boot-3-2-graalvm-native-images-java-21-and-virtual/)
- [Spring Blog: CDS with Spring Framework 6.1](https://spring.io/blog/2023/12/04/cds-with-spring-framework-6-1/)
- [Spring Blog: Spring Boot CDS Support and Project Leyden Anticipation](https://spring.io/blog/2024/08/29/spring-boot-cds-support-and-project-leyden-anticipation/)
- [Spring Blog: Spring Data Ahead of Time Repositories](https://spring.io/blog/2025/05/22/spring-data-ahead-of-time-repositories/)
- [Baeldung: Spring 6 Virtual Threads](https://www.baeldung.com/spring-6-virtual-threads)
- [Bell-SW: A Guide to Using Virtual Threads with Spring Boot](https://bell-sw.com/blog/a-guide-to-using-virtual-threads-with-spring-boot/)
- [Bell-SW: How to Use CDS with Spring Boot](https://bell-sw.com/blog/how-to-use-cds-with-spring-boot-applications/)
- [Bell-SW: Migration from Java 8 to Java 17](https://bell-sw.com/blog/migration-from-java-8-to-java-17/)
- [Piotr Minkowski: Speed up Java Startup with Spring Boot and Project Leyden](https://piotrminkowski.com/2026/03/19/speed-up-java-startup-with-spring-boot-and-project-leyden/)
- [Dan Vega: Virtual Threads in Spring Boot](https://www.danvega.dev/blog/virtual-threads-spring-boot)
- [Dan Vega: Stream Gatherers in JDK 24](https://www.danvega.dev/blog/stream-gatherers)

### Baeldung / Java Code Geeks / 권위 튜토리얼

- [Baeldung: New Features in Java 11](https://www.baeldung.com/java-11-new-features)
- [Baeldung: New Features in Java 21](https://www.baeldung.com/java-lts-21-new-features)
- [Baeldung: Guide to CompletableFuture](https://www.baeldung.com/java-completablefuture)
- [Baeldung: Java Record vs Lombok](https://www.baeldung.com/java-record-vs-lombok)
- [Baeldung: Reduce Object Header Size with Java 25](https://www.baeldung.com/java-object-header-reduced-size-save-memory)
- [Baeldung: Custom Thread Pools for Parallel Streams](https://www.baeldung.com/java-8-parallel-streams-custom-threadpool)
- [Baeldung: When to Use a Parallel Stream](https://www.baeldung.com/java-when-to-use-parallel-stream)
- [Java Code Geeks: Modern Java Language Features](https://www.javacodegeeks.com/2025/12/modern-java-language-features-records-sealed-classes-pattern-matching.html)
- [Java Code Geeks: Java's Multi-Project Evolution — Valhalla, Panama, Amber](https://www.javacodegeeks.com/2026/03/javas-multi-project-evolution-valhalla-panama-amberreach-maturity.html)
- [Java Code Geeks: Module System in 2026, Still Ignored, Still Relevant](https://www.javacodegeeks.com/2026/04/java-module-system-in-2026-still-ignored-still-relevant.html)
- [Java Code Geeks: Project Leyden's AOT Code Cache](https://www.javacodegeeks.com/2026/03/project-leydens-aot-code-cache-how-java-is-solving-its-cold-start-problem-without-graalvm.html)
- [Java Code Geeks: Virtual Threads Two Years In — Production War Stories](https://www.javacodegeeks.com/2026/05/virtual-threads-two-years-in-production-war-stories-the-pinning-edge-cases-and-what-jdk-25-fixed.html)
- [Java Code Geeks: GC Decision in 2026 — G1 vs ZGC vs Shenandoah](https://www.javacodegeeks.com/2026/04/the-jvm-garbage-collector-decision-in-2026-g1-vs-zgc-vs-shenandoah-for-real-workloads.html)
- [Java Code Geeks: Java's Memory Model Is Not What You Think](https://www.javacodegeeks.com/2026/04/javas-memory-model-is-not-what-you-think-the-gap-between-the-jmm-spec-and-the-jits-actual-guarantees.html)
- [Java Code Geeks: GC Performance G1 vs ZGC vs Shenandoah](https://www.javacodegeeks.com/2025/08/java-gc-performance-g1-vs-zgc-vs-shenandoah.html)
- [foojay: 10-year GC guide](https://foojay.io/today/the-ultimate-10-years-java-garbage-collection-guide-2016-2026-choosing-the-right-gc-for-every-workload/)
- [IBM Community: G1, Shenandoah, ZGC](https://community.ibm.com/community/user/blogs/theo-ezell/2025/09/03/g1-shenandoah-and-zgc-garbage-collectors)
- [Red Hat Developer: Beginner's Guide to Shenandoah](https://developers.redhat.com/articles/2024/05/28/beginners-guide-shenandoah-garbage-collector)
- [Datadog: A Deep Dive into Java Garbage Collectors](https://www.datadoghq.com/blog/understanding-java-gc/)
- [Azul: A Java Champion's Guide to JDK 25 Features](https://www.azul.com/blog/a-java-champions-guide-to-jdk-25-features/)
- [Azul: JDK 21 Delivers Virtual Threads](https://www.azul.com/blog/jdk-21-delivers-virtual-threads-other-new-features-and-long-term-support/)
- [JRebel: What's New With Java 25](https://www.jrebel.com/blog/java-25)
- [JRebel: Uncover New Features in Java 21](https://www.jrebel.com/blog/java-21)
- [JRebel: Take Caution Using Java Parallel Streams](https://www.jrebel.com/blog/parallel-java-streams)
- [javaalmanac: var keyword (JEP 286)](https://javaalmanac.io/features/var/)
- [javaalmanac: Virtual Threads (JEP 444)](https://javaalmanac.io/features/virtual-threads/)
- [javaalmanac: Switch Expressions (JEP 361)](https://javaalmanac.io/features/switch/)
- [javaalmanac: Pattern Matching for switch (JEP 441)](https://javaalmanac.io/features/typepatterns/)

### 실무 경험 / 마이그레이션

- [Aviator: Java Version Upgrade — From Java 8 to 17](https://www.aviator.co/blog/java-version-upgrade/)
- [CleverTap Tech Blog: Pitfalls When Upgrading from Java 8 to 17](https://tech.clevertap.com/pitfalls-when-upgrading-from-java-8-to-java-17/)
- [Hashnode: Migrating from Java 8 to 17 and Spring Boot 2 to 3](https://ahrooran.hashnode.dev/technical-challenges-migrating-from-jdk-8-to-17-and-spring-boot-2x-to-3x)
- [Systematic: Java Migration Journey, Java 8 to 17](https://systematic.com/int/careers/meet-us/tech-bytes/systematic-s-java-migration-journey-from-java8-to-java17/)
- [Cashfree: 7 Key Lessons from Java 21 Virtual Threads in Production](https://www.cashfree.com/blog/java-21-virtual-threads-lessons-production/)
- [TheServerSide: How to Solve the Pinning Problem](https://www.theserverside.com/tip/How-to-solve-the-pinning-problem-in-Java-virtual-threads)
- [TheServerSide: Java Modularity's Future — JPMS Voted Down](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Java-modularitys-future-takes-a-hit-a-Project-Jigsaw-JPMS-is-voted-down)
- [Fast Thread: Pitfalls to Avoid When Switching to Virtual Threads](https://blog.fastthread.io/pitfalls-to-avoid-when-switching-to-virtual-threads/)
- [SoftwareMill: Limits of Loom's Performance](https://softwaremill.com/limits-of-looms-performance/)
- [Coding Steve: Should I Use Java 25 Compact Object Headers?](https://stevenpg.com/posts/should-i-use-java-25-compact-object-headers/)
- [Hacker News: Migrating from Java 8 to Java 17 discussion](https://news.ycombinator.com/item?id=40752546)
- [Hacker News: Goroutines vs Project Loom](https://news.ycombinator.com/item?id=27884392)
- [Hacker News: JEP 461 Stream Gatherers discussion](https://news.ycombinator.com/item?id=38126150)

### 한국 커뮤니티

- [우아한형제들: Java의 미래, Virtual Thread](https://techblog.woowahan.com/15398/)
- [우아한형제들: 4월 우아한테크세미나 다시 보기](https://techblog.woowahan.com/17163/)
- [카카오: 제4회 Kakao Tech Meet — JDK 21 Virtual Thread](https://tech.kakao.com/2023/12/22/techmeet-virtualthread/)
- [카카오페이: Virtual Thread에 봄(Spring)은 왔는가](https://tech.kakaopay.com/post/ro-spring-virtual-thread/)
- [findstar.pe.kr: Virtual Thread란 무엇일까](https://findstar.pe.kr/2023/04/17/java-virtual-threads-1/)
- [velog: JDK 21, Spring Boot 3.4 버전업 가이드](https://velog.io/@dongvelop/JDK-21-Spring-Boot-3.4)
- [에스코어: 고성능 Java 애플리케이션과 Virtual Threads](https://s-core.co.kr/insight/view/%EA%B3%A0%EC%84%B1%EB%8A%A5-java-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EA%B0%9C%EB%B0%9C%EC%9D%84-%EC%9C%84%ED%95%9C-%ED%95%84%EC%88%98-%EA%B8%B0%EC%88%A0-virtual-threads/)

### 기타 권위 자료

- [Wikipedia: Java version history](https://en.wikipedia.org/wiki/Java_version_history)
- [Wikipedia: Java Platform Module System](https://en.wikipedia.org/wiki/Java_Platform_Module_System)
- [Wikipedia: Java memory model](https://en.wikipedia.org/wiki/Java_memory_model)
- [Wikipedia: Virtual thread](https://en.wikipedia.org/wiki/Virtual_thread)
- [Stephen Colebourne's blog: JPMS basics](https://blog.joda.org/2017/04/java-9-modules-jpms-basics.html)
- [ChrisWhoCodes: OpenJDK Project JEPs map](https://chriswhocodes.com/jepmap.html)
- [Manning: Java 8 in Action (Urma, Fusco, Mycroft)](https://www.manning.com/books/java-8-in-action)
- [Manning: Interview with Brian Goetz](https://freecontent.manning.com/interview-with-brian-goetz/)

---

## 8. 리서치 한계 (커버하지 못한 영역)

1. **Project Valhalla의 구체 디테일**: value classes (JEP 401)는 JDK 26 preview 타깃이라 본 책 범위(25)에서는 "다가오는 변화"로만 언급. 실측 데이터·실 사용 사례는 부족.
2. **Vector API의 실제 ML 워크로드 벤치마크**: incubator 단계라 production 사례 적음. Brian Goetz의 발표 슬라이드 인용 의존.
3. **OKKY·국내 포럼의 깊은 실무 후기**: 키워드 검색으로는 단편적 글 발견에 그침. 직접 OKKY/velog/네이버 카페에 들어가 상세 글 큐레이션 필요 시 챕터별 보강 필요.
4. **Quarkus·Micronaut 등 Spring 외 프레임워크의 Java 21·25 활용**: 본 책이 Spring 중심 독자를 가정하므로 본문에 깊이 다루지 않지만, 비교 챕터에서 보강 가능.
5. **JLS 정확한 섹션 번호**: 본 문서에서 §8.10(records), §8.1.1.2(sealed), §14.30(switch), §3.10.6(text block), §17.4(memory model)로 표기했으나, 인용 시 JLS 23/JLS 25 페이지·줄 위치 재확인 필요.
6. **GC 운영 실측 데이터**: 본 문서는 벤더·블로그 인용 수준. 실제 production 측정치(예: Netflix·Pinterest·LinkedIn의 ZGC 사례)는 책 단계에서 발표 자료(JFokus, Devoxx, JavaOne) 추가 조사 권장.
7. **String Templates**: 23 시점 철회됐고 향후 재설계 계획이 공식 발표 전. 진행 상황은 책 본문 시점에 재확인 필요.

---
