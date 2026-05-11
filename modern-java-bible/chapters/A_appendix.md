# 부록 A. JEP 일람

이 부록은 본문에서 다룬 JEP(JDK Enhancement Proposal)를 한자리에 모아둔 *지도*다. 본문이 진화의 *흐름*을 따라갔다면, 이 부록은 진화의 *낱장*을 빠르게 찾아보는 인덱스 구실을 한다. JEP가 처음 등장한 버전, preview에서 표준으로 안착한 경로, 한 줄로 압축한 의의, 그리고 본문에서 어디에 등장하는지를 한눈에 보여준다.

분류 기준은 책의 구성과 맞추었다. 함수형, 데이터지향, 동시성, 모듈·언어 표면, 메모리·네이티브, GC, AOT·CDS, 보안, 도구 — 9개 묶음이다. JEP 번호 순이 아니라 *주제 안에서 시간 순*으로 정렬해 흐름을 함께 읽을 수 있도록 했다. 본문 챕터 참조 열은 한 권을 들고 다닐 때 가장 쓸모 있는 정보다.

JEP는 한 건이 여러 preview를 거치며 번호가 바뀌는 경우가 흔하다. 표에서는 *최종 표준화 JEP 번호*를 굵게 표시했다. preview 단계의 번호는 화살표(→)로 이어 적었다.

---

## A.1 함수형 자바

람다와 Stream으로 시작한 함수형 흐름은 Java 9의 `takeWhile`·`dropWhile`을 거쳐, 마침내 Java 24의 Stream Gatherers 표준화에서 *중간 연산을 사용자가 정의할 수 있는* 단계까지 왔다. 11년에 걸친 함수형의 안착이다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 8 (JSR 335) | Lambda Expressions | 8 (2014) | 표준 | 함수를 1급 값으로. Java 11년 전체 변화의 출발점 | 3장 |
| 269 | Convenience Factory Methods for Collections | 9 | 표준 | `List.of`·`Map.of` — immutable 컬렉션 한 줄 생성 | 5장 |
| 461 → 473 → **485** | Stream Gatherers | 22 preview → 24 표준 | 22→24 | 사용자 정의 intermediate 연산 — Stream 11년의 가장 큰 확장 | 6장 |

람다(JEP 8)는 그 자체로 JEP가 아니라 JSR 335였지만, 변화의 무게를 생각하면 같은 줄에 놓는 게 정직하다. Stream Gatherers는 본문 6장에서 가장 깊이 다룬 변화다 — *왜 `mapConcurrent`가 `parallelStream`보다 안전한가*의 답이 거기 있다.

---

## A.2 데이터지향 자바

records, sealed, pattern matching — 세 가지가 모여 *대수적 데이터 타입(ADT)*을 만든다. Java 14의 첫 preview에서 시작해 Java 21에서 모두 표준이 됐다. 13장은 이 셋이 한 무대에서 만나는 자리였다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 305 | Pattern Matching for `instanceof` (Preview) | 14 (2020) | 14→**394**(16) | "캐스트 사다리"의 종식 | 13장 |
| 359 → 384 → **395** | Records | 14 preview → 16 표준 | 14→15→16 | 데이터의 신원을 자바가 인정한 자리 | 11장 |
| 360 → 397 → **409** | Sealed Classes | 15 preview → 17 표준 | 15→16→17 | 합 타입(sum type) — 컴파일러가 분기의 누락을 잡는다 | 12장 |
| **394** | Pattern Matching for `instanceof` (Standard) | 16 (2021) | 표준 | type test와 binding의 융합 | 13장 |
| 406 → 420 → 427 → 433 → **441** | Pattern Matching for `switch` | 17 preview → 21 표준 | 17→18→19→20→21 | exhaustive switch — sealed의 합 타입을 활용 | 13장 |
| **395** | Records (Standard) | 16 | 표준 | 14의 preview에서 16의 표준까지 18개월 | 11장 |
| 405 → 432 → **440** | Record Patterns | 19 preview → 21 표준 | 19→20→21 | record를 분해해서 매칭 — deconstruction의 정식 도입 | 13장 |
| **409** | Sealed Classes (Standard) | 17 | 표준 | "post-Java 8 첫 LTS"의 데이터지향 척추 | 12장 |
| **431** | Sequenced Collections | 21 | 표준 | `addFirst`·`getLast`·`reversed` — 21년 만의 List 보강 | 10장 |
| **440** | Record Patterns (Standard) | 21 | 표준 | ADT의 분해 | 13장 |
| **441** | Pattern Matching for `switch` (Standard) | 21 | 표준 | exhaustiveness check가 컴파일러로 | 13장 |
| 443 → 456 | Unnamed Patterns and Variables | 21 preview → 22 표준 | 21→22 | `_`로 무관심 표현 | 13장 |
| **456** | Unnamed Variables & Patterns (Standard) | 22 | 표준 | 패턴 매칭의 가독성 보강 | 13장 |
| 482 → **513** | Flexible Constructor Bodies | 23 preview → 25 표준 | 22→23→25 | `super(...)` 전에 statement 허용 — record/sealed와의 시너지 | 11장 |
| **397** | Sealed Classes (Second Preview) | 16 | preview | 17 표준화의 마지막 디딤돌 | 12장 |
| 430 | String Templates (Preview, 좌초) | 21 preview | 좌초 | 23에서 철회 — *모든 preview가 표준이 되지는 않는다*는 산 증거 | 10·22장 |

JEP 430(String Templates)의 좌초는 22장의 중요한 소재다. Brian Goetz가 "다시 그리겠다"고 말한 한 사례 — preview의 자유로움이 표준의 신중함과 만나는 자리다.

---

## A.3 동시성 — Loom 시대

동시성은 Java 5의 `java.util.concurrent`로 시작해 Java 8의 `CompletableFuture`까지 한 시대를 보냈고, Java 19의 Virtual Threads 첫 preview로 다음 시대가 열렸다. JEP 491이 21~23의 `synchronized` pinning 문제를 마침내 끊은 자리가 동시성 11년의 *결정적 매듭*이다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 266 | More Concurrency Updates | 9 | 표준 | Reactive Streams `Flow` 표준화 | 8B장 |
| 321 | HTTP Client (Standard) | 11 | 표준 | `java.net.http` — 비동기 조합의 표준 진입점 | 20·21장 |
| 425 → 436 → **444** | Virtual Threads | 19 preview → 21 표준 | 19→20→21 | thread-per-request의 부활 | 14장 |
| 428 → 437 → 453 → 462 → 480 → 499 → 505 | Structured Concurrency | 19 incubator → 5차 preview | 7차 preview까지 | concurrent code의 *구조* — Dijkstra의 재해석 | 16장 |
| 429 → 446 → 464 → 481 → 487 → **506** | Scoped Values | 20 incubator → 25 표준 | 20→21→22→23→24→25 | ThreadLocal의 후임 — immutable·bounded | 16장 |
| **444** | Virtual Threads (Standard) | 21 | 표준 | M:N 스케줄링·자동 unmount | 14장 |
| **453** | Structured Concurrency (Preview) | 21 | preview | `StructuredTaskScope` 첫 등장 | 16장 |
| **446** | Scoped Values (Preview) | 21 | preview | ThreadLocal 대안의 첫 가시화 | 15·16장 |
| 423 | Region Pinning for G1 | 22 | 표준 | virtual thread + G1의 안정화 | 17장 |
| **491** | Synchronize Virtual Threads without Pinning | 24 | 표준 | `synchronized`의 pinning 문제 해결 — Loom의 마지막 큰 매듭 | 15장 |
| **487** | Scoped Values (Fourth Preview) | 24 | preview | 25 표준화 직전 단계 | 16장 |
| **499** | Structured Concurrency (Fourth Preview) | 24 | preview | API 안정화 작업 | 16장 |
| **505** | Structured Concurrency (Fifth Preview) | 25 | preview | 표준화 직전 — JDK 26 표준 예정 | 16장 |
| **506** | Scoped Values (Standard) | 25 | 표준 | 마침내 표준 — virtual thread 시대의 ThreadLocal 후임 | 15·16장 |
| 533 | Structured Concurrency (계속) | 26+ | preview | 7차 preview 진행 | 22장 |

JEP 491(Java 24)은 Loom 시대의 *조용한 결정타*다. 21~23에서 우리가 "virtual thread 좋은데 `synchronized` 때문에 못 쓰겠다"고 했던 그 문제를, JVM 모니터의 30년 묵은 구현을 뜯어고쳐 해결했다. 15장의 후반부가 이 한 줄에 걸린다.

---

## A.4 모듈·언어 표면

JPMS는 9장의 주제고, `var`·switch·text blocks는 10장의 주제다. JEP 286(`var`)에서 시작해 JEP 512(`void main()`)까지 — *언어가 입문자와 스크립트 사용자에게 마침내 친절해진* 흐름이다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 200·201·220·261 | Project Jigsaw (JPMS) | 9 | 표준 | `module-info.java` — 야망과 좌절의 9년 | 9장 |
| 286 | Local Variable Type Inference (`var`) | 10 | 표준 | 6개월 케이던스의 첫 비-LTS 결실 | 10장 |
| 323 | Local-Variable Syntax for Lambda Parameters | 11 | 표준 | `(var x, var y) -> ...` — 람다에 annotation 부착 가능 | 10장 |
| 325 → 354 → **361** | Switch Expressions | 12 preview → 14 표준 | 12→13→14 | `case L ->`·`yield` — fall-through 시대의 종식 | 10장 |
| 355 → **378** | Text Blocks | 13 preview → 15 표준 | 13→14→15 | `"""` 삼중 따옴표 — incidental whitespace 알고리즘 | 10장 |
| 374 | Deprecate and Disable Biased Locking | 15 | 표준 | virtual thread의 길을 닦는 사전 작업 | 17장 |
| 408 | Simple Web Server (`jwebserver`) | 18 | 표준 | 한 줄짜리 HTTP 서버 — 학습·디버깅용 | 19A장 |
| **458** | Launch Multi-File Source-Code Programs | 22 | 표준 | `java App.java`로 여러 파일 실행 | 19A장 |
| **467** | Markdown Documentation Comments | 23 | 표준 | `///` 세 줄 슬래시 — Markdown javadoc | 10·19A장 |
| 459 → 476 → 494 → **511** | Module Import Declarations | 22 preview → 25 표준 | 22→23→24→25 | `import module java.base;` — 학습용 진입 장벽 완화 | 9·10장 |
| **512** | Compact Source Files and Instance Main Methods | 25 | 표준 | `void main()` 단독 실행 — 입문자 친화 | 10·19A장 |

JEP 512는 작은 변화 같지만 *철학의 변화*다. Brian Goetz의 표현으로 "자바의 첫 줄을 한 페이지에 다 설명할 수 있게 됐다". `public static void main(String[] args)`를 외우라고 한 30년의 관행이 25에서 끝났다.

---

## A.5 메모리·네이티브

Foreign Function & Memory API는 JNI 시대를 끝내는 중이다. Java 17의 첫 incubator(JEP 412)에서 Java 22의 표준(JEP 454)까지 5년 — *비교적 빠른 안착*이다. Vector API는 아직 Valhalla를 기다리고 있다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 338 | Vector API (First Incubator) | 16 | incubator | SIMD를 자바가 표현하기 시작 | 18장 |
| 412 → 419 → 424 → 434 → 442 → **454** | Foreign Function & Memory API | 17 incubator → 22 표준 | 17→18→19→20→21→22 | JNI를 점진적으로 대체 | 18장 |
| 414 | Vector API (Second Incubator) | 17 | incubator | Vector API 진행 | 18장 |
| **454** | Foreign Function & Memory API (Standard) | 22 | 표준 | `Arena`·`MemorySegment`·`Linker` — 자원 안전성 회복 | 18장 |
| 466 → **484** | Class-File API | 23 preview → 24 표준 | 22→23→24 | ASM·ByteBuddy의 OpenJDK 표준 대안 | 18장 |
| **489** | Vector API (Ninth Incubator) | 24 | incubator | Valhalla value types 대기 중 | 18·22장 |

JEP 454의 표준화 이후 `sun.misc.Unsafe`의 메모리 접근 메서드는 deprecation 강화 단계에 들어갔다. JNI를 쓰는 라이브러리들이 점진적으로 FFM으로 이주하는 시기다.

---

## A.6 GC

Serial부터 Generational Shenandoah까지 — GC의 11년은 *pause time*과 *throughput*의 줄다리기였다. Java 25의 Compact Object Headers(JEP 519)는 GC 자체가 아니라 객체 헤더의 압축이지만, GC 압력에 직접 영향을 미치니 같은 자리에 둔다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 248 | Make G1 the Default Garbage Collector | 9 | 표준 | G1이 default — Java enterprise의 GC 표준 | 17장 |
| 318 | Epsilon: A No-Op GC | 11 | 표준 | 측정·테스트 전용 GC — heap 사용량 *원형*을 본다 | 17장 |
| 333 | ZGC: A Scalable Low-Latency GC (Experimental) | 11 | experimental | colored pointer — multi-TB heap에서 sub-ms pause | 17장 |
| 376 | ZGC: Concurrent Thread-Stack Processing | 16 | 표준 | ZGC의 pause time 추가 단축 | 17장 |
| 377 | ZGC: Production-Ready | 15 | 표준 | experimental에서 production으로 | 17장 |
| 379 | Shenandoah: Production-Ready | 15 | 표준 | Red Hat의 concurrent compaction GC | 17장 |
| 423 | Region Pinning for G1 | 22 | 표준 | G1이 virtual thread와 함께 안정적으로 동작 | 17장 |
| **439** | Generational ZGC | 21 | 표준 | ZGC + 세대 분리 — throughput ~10% 향상 | 17장 |
| **474** | ZGC: Generational Mode by Default | 23 | 표준 | Generational ZGC가 ZGC의 default | 17장 |
| **519** | Compact Object Headers | 25 | 표준 | 객체 헤더를 96~128비트에서 64비트로 — heap ~22% 절감 | 17·19장 |
| **521** | Generational Shenandoah | 25 | 표준 | Shenandoah에도 세대 — Red Hat ecosystem의 결실 | 17장 |

JEP 519는 "Compact Object Headers를 켤지 말지"가 책 출간 시점의 가장 자주 받는 질문 중 하나다. 17·19장에서 답이 있다 — 짧게 말하면 *25 LTS의 default가 되기 전까지는 측정 후 결정*.

---

## A.7 AOT · CDS · Leyden

GraalVM이 가진 자리를 OpenJDK가 *다른 방식으로* 회수하는 중이다. AppCDS(JEP 310)부터 시작해 JEP 483의 AOT Class Loading & Linking까지 — Spring Petclinic 기준 startup이 36~42% 단축됐다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 310 | Application Class-Data Sharing (AppCDS) | 10 | 표준 | class metadata를 archive로 캐시 | 19장 |
| 350 | Dynamic CDS Archives | 13 | 표준 | 단일 run으로 archive 생성 — workflow 간소화 | 19장 |
| **483** | Ahead-of-Time Class Loading & Linking | 24 | 표준 | class를 init·link해서 캐시 — Leyden의 첫 결실 | 19장 |
| **514** | Ahead-of-Time Command-Line Ergonomics | 25 | 표준 | AOT 사용 UX 정리 — 한 줄 명령으로 cache 생성 | 19장 |
| **515** | Ahead-of-Time Method Profiling | 25 | 표준 | JIT profile을 AOT cache에 포함 | 19장 |

Project Leyden의 *premain branch*는 아직 표준 JEP는 아니지만, AOT code compilation·AOT proxy generation 같은 더 깊은 수준의 변화를 예고한다. 22장 후반에서 그 풍경을 그렸다.

---

## A.8 보안

Java의 보안은 *조용한 진화*다. JEP 411(SecurityManager deprecation)이 가장 큰 정책 변화고, post-quantum 대응(JEP 478·510)이 가장 최신 흐름이다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 339 | Edwards-Curve Digital Signature Algorithm (EdDSA) | 15 | 표준 | Ed25519·Ed448 — 현대 암호 정식 진입 | 20A장 |
| **411** | Deprecate the Security Manager for Removal | 17 | 표준 | 25년간 자바의 보안 모델이었던 SecurityManager의 퇴장 시작 | 20A장 |
| **452** | Key Encapsulation Mechanism API | 21 | 표준 | KEM — post-quantum 대비 첫 표면 | 20A장 |
| 478 → **510** | Key Derivation Function API | 24 preview → 25 표준 | 24→25 | HKDF·PBKDF — Argon2·KDF 표준 진입 | 20A장 |
| 486 | Permanently Disable the Security Manager | 25+ | preview | SecurityManager의 완전 퇴장 — 마이그레이션 마지노선 | 20A장 |

SecurityManager의 deprecation은 단순한 API 변화가 아니다. *프로세스 격리·컨테이너·OS 권한*으로 보안 책임이 옮겨갔다는 의미다. 20A장이 그 이야기다.

---

## A.9 도구

JShell(JEP 222)부터 jextract(Panama 도구)까지 — Java의 *주변 도구*가 11년간 가장 많이 바뀐 영역이다. 19A장이 이 모두를 한 권에 모은 자리다.

| JEP | 제목 | 도입 버전 | preview → stable | 한 줄 의의 | 본문 |
|---|---|---|---|---|---|
| 222 | JShell: The Java Shell | 9 | 표준 | REPL — 학습과 실험의 진입점 | 19A장 |
| 328 | Flight Recorder | 11 | 표준 | production-grade profiling, 오버헤드 1% 미만 | 19A장 |
| 343 | Packaging Tool (`jpackage`) | 16 | 표준 | native installer 생성 (.msi·.dmg·.deb) | 19A장 |
| 349 | JFR Event Streaming | 14 | 표준 | JFR 이벤트를 실시간 스트림으로 | 19A장 |

`jextract`는 정식 JEP는 아니지만 Panama 도구 묶음의 일원으로 18·19A장에서 다룬다. C header를 자바 바인딩으로 자동 변환하는 도구다.

---

## A.10 부 도입 — *번호가 없는 JEP들*

JEP 번호로 표현되지 않은 변화들도 있다. 라이선스, 호스팅, 도구 생태계 — *세상의 변화*가 자바의 모습을 함께 바꿔놓았다.

- **Oracle JDK 라이선스 유료화 (2018)**: Java 11과 함께 시작. OpenJDK·Corretto·Temurin·Zulu·Liberica로의 대이주를 촉발. 20장의 출발점이기도 하다.
- **Mercurial → Git, GitHub로 호스팅 이전 (Java 16)**: OpenJDK 소스가 GitHub로 옮긴 시점. 외부 기여의 진입 장벽이 크게 낮아졌다.
- **6개월 케이던스 (2017~)**: Java 10부터 시작된 짧은 릴리스 주기. LTS 모델과 함께 *preview의 자유*와 *표준의 신중함*을 분리하는 운영 방식이 됐다.
- **JCP의 후퇴, JEP의 부상**: JSR-376(JPMS) 부결 사건 이후, 실질적인 변화 채널은 JCP가 아니라 JEP 프로세스가 됐다. 22장에서 다룬 변화의 의미다.

JEP 번호로 잡히지 않는 이 변화들이 자바 11년의 풍경을 만들어왔다. 표 안에는 들어갈 수 없었지만, 본문 전체가 이 배경을 전제하고 있다.

---

## A.11 사용 안내

이 부록의 활용법을 짧게 적어둔다.

특정 JEP를 검색해서 들어왔다면, *본문* 열의 챕터 번호로 가서 그 JEP가 *어떤 맥락에서 무슨 문제에 답하는가*를 읽는 게 좋다. JEP 자체의 정의는 OpenJDK 공식 페이지(`openjdk.org/jeps/{번호}`)가 더 정확하지만, *왜 그 JEP가 그 시점에 그 모습으로 등장했는가*는 본문에서 더 잘 읽힌다.

마이그레이션 계획을 세우는 자리라면, 부록 C(체크리스트)와 함께 보는 편이 낫다. JEP 일람은 *무엇이 바뀌었나*를 알려주고, 체크리스트는 *우리 코드가 그 변화에 어떻게 대응해야 하나*를 알려준다.

코드 패턴이 궁금하다면 부록 D(8 vs 25 비교 30선)로 가자. 한 JEP가 실제 코드에서 어떻게 표현되는지를 30개의 짝으로 묶어두었다.

마지막으로 — JEP 번호는 *시간의 좌표*가 아니라 *변화의 좌표*다. 같은 변화가 여러 JEP를 거치며 번호가 바뀌는 일이 많으니, 본문에서 만난 JEP 번호와 표의 번호가 다르더라도 당황하지 말자. 화살표(→)로 이어진 흐름이 그 답이다.
