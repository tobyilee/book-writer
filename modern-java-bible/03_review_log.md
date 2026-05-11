# Modern Java Bible — 저술 계획 리뷰 (라운드 1)

> 리뷰 대상: `02_plan.md` (22장, 약 271,500자 예상)
> 비교 기준: `01_reference.md` (8개 절, JEP 60+)
> 대상 독자: Spring Framework로 엔터프라이즈 앱을 만드는 자바 개발자
> 리뷰 일자: 2026-05-11

---

## A. 잘된 점 (간단히)

1. **더블 헬릭스 구조**가 영리하다 — 1·9·13·22장이 시간 축의 마디를 짚고, 나머지가 주제 축을 판다. "버전별이냐 주제별이냐"의 오래된 딜레마를 정직하게 우회했다.
2. **호 ②의 동선**(8장 Loom 이전 → 11·12·13 데이터지향 → 14·15·16 Loom 시대)이 강력하다. Pattern matching의 데이터지향 도구를 손에 쥔 채 동시성 새 모델로 넘어가는 순서가 직관적이다.
3. **Toby 스타일 적용 지점 표**(§6)가 챕터마다 적시돼 있어, 챕터 저술가가 "어디서 청유형을, 어디서 공감 표현을" 쓸지 미리 자리를 잡았다. 다른 책 계획에서 보기 드문 강점.
4. **5장 Stream의 함정 챕터, 6장 Gatherer 정점, 13장 ADT 클라이맥스**의 봉우리 배치가 명확하다. 책의 미학적 정점이 어디인지 의도가 보인다.
5. **20·21장이 마이그레이션과 Spring 시너지를 분리한 결정** — 한 챕터로 뭉뚱그리지 않은 점이 좋다.

---

## B. 보강/수정 요구사항

### 【Must Fix 1】 동시성 비중이 약속(28%)에 못 미친다 — 6~7%포인트 부족

§7 분량 검증표 본인이 인정하듯 동시성(8+14+15+16)이 21%(56,500자)로, 책의 무게 중심 §2가 약속한 **28%**에 7%포인트 모자란다. 이건 **Bible 약속의 정직성 문제**다 — §2에서 "동시성이 책의 최대 무게"라고 못 박은 약속을 분량이 배신한다.

**근거:** 레퍼런스 §3.3(Virtual Threads)이 단일 절로 가장 길고, §3.1 함수형(58,500자=22%)보다 동시성 깊이 요구가 크다. JMM·happens-before·pinning·structured concurrency·scoped values는 함수형보다 *더 어렵고 더 새롭다*.

**제안:**
- 8장 17,000 → **20,000자**로 확장. JMM·happens-before·out-of-thin-air 절을 별도 소절로 분리하고, `final` field semantics·`volatile` memory effect의 JLS §17.4 정확 인용을 본문에 한 페이지 박스로 삽입.
- 14장 15,000 → **18,000자**. M:N 스케줄링 internals(continuation, ForkJoinPool carrier, mount/unmount의 실제 바이트코드 흐름)을 추가. 현재 계획은 "M:N 스케줄링과 carrier" 한 줄로 처리됐다.
- 16장 12,500 → **15,000자**. StructuredTaskScope의 정책 3종을 코드 예제로 모두 보여주고, ScopedValue rebinding semantics를 깊이 다루기.
- 합산 → 약 65,000자 ≈ 24%. 여전히 28% 약속에는 모자라지만, 합리적 절충.

**대안:** §2의 가중치 명세를 24%로 솔직히 수정한다. 약속과 산출을 일치시키는 게 우선.

---

### 【Must Fix 2】 데이터지향(18% 약속) 분량 14%로 미달 — 4%포인트 부족

11·12·13장 합계 37,000자 = 14%. §2 약속 18%에 모자란다. 13장은 책 미학의 클라이맥스라며 14,500자만 할당하는 건 자기모순이다.

**제안:**
- 13장 14,500 → **17,000자**. 이유:
  - "Visitor 패턴의 사망 신고서"라는 강한 메시지가 한 절로 다뤄지려면 *Visitor의 한 줄 한 줄을 ADT로 옮기는 4페이지 대비 예제*가 필요.
  - JEP 305→394→406→420→427→432→433→440→441→456의 10개 JEP를 14,500자로 다루면 한 JEP당 1,450자 — Bible의 깊이가 아니라 *카탈로그*가 된다.
  - 레퍼런스 §3.2의 "Records + Sealed = ADT" 철학(Philip Schwarz의 Speaker Deck 인용)을 책 한 챕터로 다지려면 표현식 평가기 외에 *현실 도메인 예제*(예: HTTP `Result<T,E>`, Workflow state machine) 두 개가 더 필요.
- 12장 10,500 → **12,000자**. Sealed의 표현력과 Visitor 비교를 *코드 길이 측정*까지 보여주기.

---

### 【Must Fix 3】 JLS 인용 약속이 본문 챕터에 흩어져 있을 뿐 *체계*가 없다

요구사항에 "JLS 인용 디테일"이 명시되어 있다. 현재 계획은 다음만 명시한다:
- 3장: JLS §15.27 (effectively final)
- 8장: JLS §17.4 (Memory Model, out-of-thin-air)
- 11장: JLS §8.10 (records)
- 12장: JLS §8.1.1.2 (sealed)
- 13장: JLS §14.30 (switch exhaustiveness)

레퍼런스 §4.4(Text Blocks JLS §3.10.6), §4.5(JEP 286 var)는 본문 챕터에 어디에 들어가는지 모호하다. 또한 JLS §15.25(switch expression), §15.28(constant expressions와 case label), §6.8(naming convention)도 다뤄야 할 자리들이 비어 있다.

**제안:**
- 부록 A "JLS 인용 인덱스"를 *명시적 챕터*로 약속 (§2에서 "부록은 후속 자동 생성"으로 흘리는 대신, 부록 자체를 분량 합산에 포함 — 약 8,000자).
- 각 챕터의 "JLS 인용 박스"를 명시적 디자인 요소로 약속한다. §6의 Toby 스타일 표와 같은 형식으로 "JLS 인용 자리" 표를 추가.
- 10장에서 text blocks를 다룰 때 JLS §3.10.6의 incidental whitespace 알고리즘을 *원전 인용으로* 박스에 넣는 약속을 명시.

---

### 【Must Fix 4】 누락된 JEP / 주제

레퍼런스를 훑어 가며 계획에서 사라진 항목을 모두 찾아냈다:

| 누락 JEP/주제 | 레퍼런스 위치 | 제안 |
|---|---|---|
| **JEP 431 Sequenced Collections** | §4.8, Java 21 | 10장 또는 11장에 한 절(2,000자). "들어왔는데 잘 모르는" 것의 대표 사례 — 책의 정체성에 맞음 |
| **JEP 467 Markdown Documentation Comments** | §3.10, Java 23 | 10장에 한 절 추가. 도구 챕터가 없으니 10장이 가장 자연스러움 |
| **JEP 482 Flexible Constructor Bodies (Java 23 → 25 표준 JEP 513)** | §2 Java 23, Java 25 | 11장(records) 또는 14장 옆 절에 박스로. 30년 묵은 `this()/super()` first-statement 룰의 종말 |
| **JEP 484 Class-File API (Standard, Java 24)** | §2 Java 24 | 누락. 어디든 새 절 필요 — 18장의 FFM 다음 또는 별도 미니챕터. ASM·BCEL을 대체하는 1급 API, Spring AOT·Hibernate가 직접 영향받음 |
| **JEP 458 Launch Multi-File Source Programs** + **JEP 512 Compact Source Files + Instance Main** | §2 Java 22, Java 25 | 10장 또는 22장 끝에 "자바의 입문 친화 진화" 절. 엔터프라이즈 독자에게도 스크립트·CI 도구 작성에 의미 큼 |
| **JEP 408 Simple Web Server / jwebserver** | §3.10 | 22장의 도구 절에 한 줄, 또는 새 도구 챕터 |
| **JEP 478 Key Derivation Function API → JEP 510 표준** | §2 Java 24/25 | **완전 누락**. 보안 챕터가 없는 게 약점 — post-quantum 대응 준비, Spring Security 시너지 |
| **JEP 452 Key Encapsulation Mechanism API (Java 21)** | §2 Java 21 | 위와 같이 보안 절 누락 |
| **JSR 133 happens-before 정확한 원문 인용** | §4.7 | 8장에서 *원문*을 박스에 넣겠다고 약속해야 — 현재는 "JLS §17.4에서 인용" 한 줄로 흐림 |
| **deprecated `SecurityManager` (Java 17 JEP 411 → 24 종료)** | 없음 | 20장 마이그레이션에 *반드시* 들어가야 — 엔터프라이즈 마이그레이션의 큰 함정 |
| **String Templates의 좌초 (§6.6)** | §6.6 | **계획에 *완전히* 없다**. 22장에 한 절 또는 10장 끝에 "preview 자정 사례"로 4,000자. Bible의 메타 메시지(언어 진화의 자기교정)에 매우 중요 |
| **Lombok 다중 어노테이션의 미래 (`@Slf4j`, `@SneakyThrows`, `@Accessors`)** | §3.2 (records vs Lombok) | 11장이 "DTO는 records"만 다루면 부족. `@Slf4j`는 records로 대체 불가 — 명시 필요 |
| **JFR/JMC, JShell, jpackage, jlink, jextract** | §3.10 | **도구 챕터가 통째로 없다.** 17·18·19 사이에 끼울 한 챕터 또는 부록 |
| **Maven/Gradle의 자바 버전 호환성** | §5.1 | 20장에 "빌드 도구 — Maven 3.6.3+/Gradle 7.3+" 한 줄만. 실무자에겐 *한 절*이 필요 (toolchain, foojay-resolver, Maven Wrapper) |
| **JUnit 5의 자바 17 활용 (records 친화, sealed exhaustiveness 테스트)** | 없음 | 21장 또는 새 테스트 절 |
| **GraalVM Native Image의 *깊이*** | §3.8, 19장 | 19장에서 한 줄로 처리되는데, "GraalVM 없이도 빠른" 메시지를 위해서라도 GraalVM이 정확히 무엇이고 한계가 무엇인지 *비교 절* 필요 |
| **`HttpClient` 표준화 (Java 11, JEP 321)** | §2 Java 11 | **계획에서 누락**. WebClient·RestTemplate과의 비교, virtual thread + HttpClient의 시너지는 21장에 한 절로 들어갈 자리 |
| **PermGen → Metaspace 전환의 영향** | §2 Java 8 | 17장 GC 챕터 또는 20장 마이그레이션에 한 절. CleverTap 사례에서 Docker OOM의 직접 원인 |

---

### 【Should Fix 1】 13장의 JEP 폭격 — 한 챕터에 10개 JEP는 카탈로그형 위험

13장 "다룰 JEP: JEP 305, 394, 406, 420, 427, 432, 433, 440, 441, 456" — 10개. 14,500자에 10개 JEP를 다루면 JEP당 1,450자, 거의 인덱스 카드 수준이다.

**제안:** 13장을 "Pattern Matching 본론"과 "Records Pattern + 중첩 + Unnamed"로 *분할*하거나, 13장을 17,000자로 늘리고 preview 진화사(305→394, 406→420→427→432→433→441)는 *연표 박스*로 압축하고 본문은 21 표준 + 22 unnamed에 집중.

---

### 【Should Fix 2】 6장 Gatherer 챕터의 함수형 깊이 부족

6장 16,000자에 Collectors 표면, 내장 Gatherer 5종, 직접 Gatherer 구현, 8 vs 24 비교까지. 좋은데 — **함수형 패러다임의 깊이**가 약하다.

요구사항: "Stream/Optional/Collector/Gatherer가 단순 사용법을 넘어 함수형 패러다임(immutability, ADT, monad-ish patterns)을 충분히 다루나?"

현재 6장은 *Gatherer 카탈로그*다. 다음이 빠졌다:
- `reduce`의 monoid 속성 (identity, associativity)을 *왜 강조해야 하는지* — parallel safety의 수학적 기반.
- Collector의 5개 함수 (`supplier/accumulator/combiner/finisher/characteristics`)가 사실은 *fold 일반화*임을 짚는 절.
- `flatMap`의 monad 의미 — Optional·Stream·CompletableFuture에서 모두 같은 형식인 이유.
- Gatherer의 `Stream<T> → Stream<R>` 변환이 *함수형 transformer*로 합성 가능함 (코드 한 페이지로 보여줄 만함).

**제안:** 6장에 "함수형 관점 — fold·monad·composition" 절 하나(2,500자)를 추가하고 분량 18,500자로. 또는 7장 Optional 챕터를 9,500 → 11,500자로 늘리고 monad 색채를 7장에 몰아주기.

---

### 【Should Fix 3】 8장의 비대화와 분할 가능성

8장 17,000자 — JMM, j.u.c, ExecutorService, Future, BlockingQueue, Phaser, ForkJoin, parallelStream 함정, CompletableFuture 50+ 메서드, exception 전파, Flow, Reactor 비교. **너무 많다.**

읽다가 맥이 끊긴다. JMM은 그 자체로 한 챕터다.

**제안:** 8장을 **8A. j.u.c와 JMM**(11,000자) + **8B. CompletableFuture와 Reactive Streams**(10,000자)로 분할. 총 21,000자로 동시성 1축의 무게를 늘리는 효과 + 가독성 개선. 챕터 번호가 1씩 밀리지만, 책의 두께 약속(Bible)을 지키는 데 더 정직하다.

---

### 【Should Fix 4】 17장 GC의 실측 데이터 부족 — Bible답지 않은 약속

17장 12,000자에 9종 GC + 옵션 + k8s 함정 + 워크로드별 가이드. 좋은데 **벤치마크 표가 없다**.

레퍼런스 §8.6이 인정하듯 "실측 데이터는 발표 자료 추가 조사 권장". 현재 계획은 그 약속이 본문에 어떻게 반영되는지 모호.

**제안:** 17장에 "*벤치마크 박스 3종* — JFokus·Devoxx·JavaOne 발표 슬라이드에서 추출한 실측 표"를 명시적으로 약속. JEP 519 Compact Object Headers는 19장에서 따로 다루므로 17장은 GC 자체에 집중.

---

### 【Should Fix 5】 21장이 "다시 한 번의 종합" 이상이 되어야 — Spring 시너지의 *고유성*

21장 13,000자에 "한 챕터에 records, sealed, pattern, virtual thread, AOT가 한 줄씩". 이건 위험하다 — *재탕*이다.

**제안:** 21장은 *Spring이 Modern Java를 받아들이며 *나름의 패턴*을 만든 자리*에 집중. 다음을 챕터의 척추로:
- Spring Data Repositories의 records projection 미세 동작 (interface projection과 다른 점, Spring Data AOT Repositories의 빌드 타임 코드 생성)
- `@ConfigurationProperties` + records의 immutable config 패턴과 `@RefreshScope`의 충돌
- Spring 6의 `RestClient` (5.1 신규)가 RestTemplate·WebClient·HttpClient와 어떻게 다른지
- Spring Boot 3.4의 SSL bundle, Docker Compose support 등 Java 21·25 베이스에서의 신기능
- WebFlux를 *유지해야 하는* 시나리오 4가지 (backpressure, SSE, server-sent stream, kafka consumer fan-out)

레퍼런스 §6.3(VT vs Reactive 논쟁)을 21장 결론으로 가져오기.

---

### 【Should Fix 6】 호 ②와 호 ③ 사이 — 13장(데이터지향 끝)에서 14장(Loom)으로의 점프가 가파르다

13장은 책의 미학적 클라이맥스인데, 그 다음 페이지가 곧장 14장 Virtual Thread다. 독자가 호흡을 고를 자리가 없다.

**제안:** 13장 마지막 1페이지를 *13장과 14장의 다리*로 활용 — "이제 ADT로 도메인을 모델링했으니, 그 도메인 위에서 동시성을 다시 생각해보자"의 문단을 명시.

또는 14장 도입 1페이지를 *13장 회수*로 — sealed `Result<T,E>`를 virtual thread 결과 처리에 쓰는 한 페이지 예제.

---

### 【Should Fix 7】 1장의 한국 사례가 1장에만 나오고 마는 위험

1장에 "한국 엔터프라이즈의 실제 분포 (8 잔존 → 17 정착 → 21 도입의 흐름)"가 있다. 좋다. 그러나 이게 *통계 한 줄*로 끝나고 책 전체에서 사라지면 *그저 한국어 책*이라는 정체성을 잃는다.

**제안:** §6 Toby 스타일 표 옆에 "한국 사례 인용 자리" 열을 추가하고, 다음을 분배:
- 14장: 우아한형제들·카카오의 Virtual Thread 세미나 인용
- 15장: 카카오페이의 platform → virtual 전환 측정 인용
- 20장: 한국 SI/금융권의 8 → 17 이주 사례 1~2건 인용 (리서치 보강 필요)
- 21장: velog·findstar.pe.kr 등 한국 개발자 블로그 1~2건 인용

레퍼런스 §3.3 끝에 한국 사례가 정리돼 있는데, 계획에는 14·15장에 한 번씩만 나타난다. 더 자주.

---

### 【Should Fix 8】 22장의 Valhalla 약속 — preview 도달 가정의 위험

22장: "Project Valhalla: value class (JEP 401, 26 preview 타깃)". 레퍼런스 §8.1이 인정하듯 *진행 상황이 출판 시점에 바뀔 수 있다*. 책이 인쇄됐는데 26 preview가 또 밀리면 22장이 우스워진다.

**제안:** 22장의 어조를 *예측*이 아니라 *현재 시점의 약속*으로 — "이 책이 인쇄될 때까지 알려진 26의 모습"이라는 명시적 disclaimer 박스. JEP 401·Babylon·Leyden의 *최신 상태*를 챕터 도입에 박스로 못 박는다.

---

### 【Nice to Have 1】 부 도입 페이지의 약속

§3은 부(Part) 구조를 보여주는데, *부 도입 페이지*가 명시되지 않았다. Bible급 책은 부마다 1~2페이지 도입이 관례. 약 10부 × 1,500자 = 15,000자 추가.

§7 합산에 "전문·각 부 도입·부록을 더하면 28만~30만 자"라고만 적혀 있다 — 구체적 분량 약속이 모호. *부 도입 분량을 §7 표에 명시*.

---

### 【Nice to Have 2】 책 시작의 "이 책을 읽는 4가지 길" 약속을 실제로 디자인

§5 끝에 "이 책을 읽는 4가지 길"이 약속됐다. 좋다. 그러나 실제 어떻게 표시할지 — 챕터 첫 페이지에 의존성 아이콘이 있을지, 부 도입에 길 안내가 있을지 — 가 미정.

**제안:** 챕터 헤더에 "이 챕터를 읽기 전 권장: 챕터 N" 미니 박스를 디자인. 의존성 그래프(§5)를 챕터 헤더 메타데이터로 분산.

---

### 【Nice to Have 3】 코드 비율의 약속

Bible급 책은 코드 분량이 본문의 30~40%다. 현재 계획은 *글자 수*만 약속하고 코드 비중은 모호.

**제안:** §2에 "본문 28만 자 + 코드 약 4만 줄(LOC)"의 약속을 추가. 또는 "본문 :코드 = 7:3"의 비율을 명시.

---

### 【Nice to Have 4】 부록 명시화

§2가 "부록(JEP 일람, JLS 인용 인덱스)"을 언급하지만 §4의 22장에는 부록이 없다. 부록도 책의 일부 — *부록 A·B·C*를 명시적으로 챕터처럼 설계해야 Bible의 약속에 부합:

- **부록 A. JEP 일람** — 60+ JEP를 버전·Project·표준화 시점으로 정렬 (8,000자)
- **부록 B. JLS 인용 인덱스** — 본문에 나온 JLS 인용을 §·페이지·챕터 번호로 색인 (4,000자)
- **부록 C. 마이그레이션 체크리스트** — 20장의 핵심을 1페이지로 (2,000자)
- **부록 D. 한 줄 요약 — 8 vs 25 코드 패턴 30선** — 책의 정체성을 압축 (6,000자)

부록 합계 20,000자 추가 → 본문 271,500 + 부록 20,000 + 부 도입 15,000 = **약 306,500자**. Bible 약속(28~30만 자, 600~720p)에 정확히 맞는다.

---

## C. 신설 챕터/주제 제안

다음 셋은 *반드시* 챕터 또는 절로 들어가야 한다고 본다.

### 신설 제안 1: 도구 챕터 — 17·18·19 사이에 끼울 한 챕터

**가칭 19A. Modern Java의 도구들 — JShell부터 jextract까지** (8,000자)
- JShell의 실무 활용 (Spring REPL, JPA 쿼리 디버깅)
- jpackage·jlink로 만드는 native installer / slim JRE
- jwebserver의 로컬 개발 활용
- JFR + JMC로 production-grade profiling — virtual thread pinning 진단의 *실전 시연*
- jextract 워크플로 (FFM 챕터의 전제)

도구가 통째로 빠진 건 Bible의 망라성 약속에 명백한 구멍이다.

### 신설 제안 2: 보안과 암호 챕터 또는 절

**가칭 20A. 자바 보안의 11년 변화** (6,000자)
- `SecurityManager`의 deprecation (JEP 411, Java 17) → 제거 (JEP 486, Java 24)
- KEM API (JEP 452 Java 21, JEP 478/510 Java 24/25) — post-quantum 대응
- TLS 1.3, EdDSA (JEP 339), 인증서 처리의 변화
- Spring Security의 Modern Java 패턴

레퍼런스 §2 Java 21·24·25에 명시된 보안 JEP들이 *통째로* 빠져 있다. Spring 개발자 독자에게 *반드시* 필요.

### 신설 제안 3: 1장 앞에 "서론" 또는 1장 자체를 더 두껍게

현재 1장 10,000자에 11년 연대기 + LTS 모델 + 한국 분포 + 책 읽는 방법. 너무 많다.

**제안:** 1장 12,000자, 또는 *서론*(2,000자) + 1장(10,000자)로 분리. 서론은 Toby 스타일 책에서 *책 전체의 톤을 결정*하는 자리 — 이 책이 왜 필요한가, 왜 지금인가, 왜 Bible인가.

---

## D. 분량 재배분 권고 (요약 표)

| 챕터 | 현재 | 권고 | 사유 |
|---|---:|---:|---|
| 서론 (신설) | — | 2,000 | 책 전체의 톤 결정 |
| 1장 | 10,000 | 11,000 | Sequenced Collections 등 추가 |
| 6장 | 16,000 | 18,500 | 함수형 깊이 절 추가 |
| 7장 | 9,500 | 11,500 | Optional의 monad 색채 |
| 8장 | 17,000 | 21,000 (또는 분할 11,000+10,000) | JMM 독립 + CompletableFuture 분리 |
| 10장 | 12,500 | 14,500 | Sequenced Collections, JEP 467, JEP 458/512, String Templates 자정 |
| 11장 | 12,000 | 12,000 | 유지 |
| 12장 | 10,500 | 12,000 | Sealed의 Visitor 코드 길이 비교 |
| 13장 | 14,500 | 17,000 | Bible의 미학적 클라이맥스 |
| 14장 | 15,000 | 18,000 | M:N internals 추가 |
| 16장 | 12,500 | 15,000 | StructuredTaskScope 정책 3종 |
| 19A장 (신설) | — | 8,000 | 도구 챕터 |
| 20장 | 12,500 | 14,500 | SecurityManager·HttpClient·빌드 도구 |
| 20A장 (신설) | — | 6,000 | 보안·암호 |
| 21장 | 13,000 | 15,000 | Spring 시너지의 고유성 |
| 22장 | 10,000 | 12,000 | 도구 마무리 + String Templates 사후 |
| 부 도입 (10개) | — | 15,000 | Bible 관례 |
| 부록 A·B·C·D | — | 20,000 | 명시적 부록 |

**재배분 후 합계:** 본문 약 306,500자 → 국판 약 720~780p. Bible 약속의 상한에 정확히 도달. 동시성 비중도 약 25%로 개선.

---

## E. 중복·공백 점검

### 중복 위험

1. **records가 11장·13장·21장**에서 모두 나옴 — 의도된 반복(데이터지향 삼위일체)이지만, *각 챕터에서 records의 어떤 면을 다루는지* 명시 필요. 현재는 11장이 records 전체, 13장이 records pattern, 21장이 Spring과의 records — *겹치는 자리*가 안 보이지만 챕터 저술가가 같은 예제를 반복할 위험이 있다.
   - **제안:** 11장 표준 DTO 예제, 13장 표현식 평가기, 21장 `@ConfigurationProperties` — *서로 다른 도메인*으로 고정.
2. **virtual thread가 14·15·16·21장**에서 반복 — 같은 패턴.
   - **제안:** 14장 도입, 15장 함정, 16장 구조화, 21장 Spring 통합 — 챕터별 도메인 예제를 분리.
3. **Spring Boot 3.2의 `spring.threads.virtual.enabled`가 14·21장**에서 두 번 — 한 곳을 *간략 호명*으로 줄여야 함.

### 공백

1. **GC와 JMM 사이의 다리 없음** — 17장 GC 챕터가 메모리를 다루지만 JMM·happens-before는 8장에 있다. 두 메모리 이야기가 책 안에서 *완전히 분리*돼 있다. 17장 끝 또는 별도 1페이지로 "메모리의 두 얼굴" 다리 필요.
2. **Reactive Streams Flow가 8장 한 챕터에만** — 21장에서 WebFlux 유지 시나리오를 다루기로 했으니, 8장 → 21장의 Reactive 연결고리 명시 필요.
3. **JEP가 *왜 그 순서로* 들어왔는가**의 메타 — 2장이 다루지만, 책 중반에 다시 회수되지 않는다. 11장 records 도입부에 "왜 records가 14에 preview, 16에 표준이었는가"의 *진화 박스* 같은 게 챕터마다 있으면 책의 정체성이 살아난다.

---

## F. Toby 스타일 강점 점검

§6 표가 챕터마다 Toby 스타일 자리를 명시한 건 강점이다. 그러나:

1. **공감 표현이 17·18장에서 약하다.** GC·FFM·SIMD는 학술적 주제라 *공감 단어를 어디 넣을지* 보이지 않는다. §6의 "OOM kill로 새벽에 깨는 *끔찍함*"은 좋은데, FFM 챕터의 "`*.h` 추출에 하루를 쓴 *번거로움*"은 *너무 캐주얼*해 보일 수 있다. 학술적 주제에서 Toby 스타일이 살아나려면 *실측·실험*의 권유형이 더 적합 — "한 번 측정해보자", "벤치마크를 직접 돌려보자".
2. **수사적 질문이 너무 동일 패턴.** 22개 챕터에 "정말 ~인가?" 형식이 7번. 변주가 필요. *지금 우리는 어디 와 있는가*, *그래서 결국 어떻게 쓰는가*, *이게 정말 끝일까* 같은 다양한 형식.
3. **구체적 상황 가정**(~라고 해보자)이 §6에 명시되어 있지 않다. 챕터 도입부 1~2 문단을 *상황 가정*으로 시작한다는 §6의 원칙은 좋은데, 챕터마다 *어떤 상황*인지 미정. 챕터 저술 단계에서 임의로 정해지는 위험.
   - **제안:** §6 표에 "도입부 상황 가정" 열을 추가하고, 챕터마다 구체적 가정을 한 줄로 미리 적시.

---

## G. 한 줄 종합 평가

**Bible의 골격과 더블 헬릭스 구조는 정직하고 강력하지만, "Bible의 두께·동시성·데이터지향" 세 약속의 분량이 자기 약속을 못 지킨다. 동시성 +7%pt, 데이터지향 +4%pt, 누락 JEP 15+개와 보안·도구 챕터 신설, 부록 명시화로 본문 30만 자에 도달해야 Bible의 무게값을 정직하게 받을 수 있다.**

---

*리뷰: plan-reviewer @ 2026-05-11, 하네스 v1.2.0*
