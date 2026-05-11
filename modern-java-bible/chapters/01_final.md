# 1장. 11년의 자바, 한 장의 지도

당신의 회사 코드베이스가 Java 8에 멈춰 있다고 해보자.

빌드 스크립트 어딘가에 `sourceCompatibility = 1.8`이라고 적혀 있고, 운영 서버에는 Oracle JDK 8u201이 깔려 있다. 누군가 한 번 Java 11로 올리려다가 Java EE 모듈 제거(JEP 320) 충격을 본 뒤 조용히 손을 뗀 흔적이 git log에 남아 있다. PR 리뷰에는 여전히 `Optional<List<T>>`가 올라오고, DTO 옆에는 Lombok이 친절하게 붙어 있다. 매주 월요일 회의에서 누군가 "그래서 우리도 records 좀 써야 하는 거 아닙니까?"라고 물으면, 시니어는 "JPA Entity는 안 돼"라고만 답하고 회의는 다음 안건으로 넘어간다. 어딘가 *난감하다*. 어딘가 안 풀린다. 그런데 새 LTS인 25가 나왔다고 한다. *또 새 버전이라니.*

자, 그렇다면 지금 우리는 자바의 어디쯤에 와 있을까? 한 장의 지도를 펼쳐보자.

## 두 개의 변화가 한꺼번에 일어났다

"Modern Java"라는 말을 들으면 보통 두 가지가 떠오른다. 람다와 스트림이 들어왔다는 것. 그리고 매년 두 번씩 새 버전이 나온다는 것. 둘은 별개의 사건처럼 보이지만, 실제로는 한 몸이다.

첫 번째 변화는 *언어 패러다임의 확장*이다. Java 8(2014년 3월)이 람다·스트림·`Optional`·`java.time`을 묶어 출시하면서, 자바는 객체지향 단일 노선의 언어에서 함수형·데이터지향·동시성 친화적 언어로 확장됐다. 람다는 `java.util.function`의 함수형 인터페이스 묶음과 결합해 코드에 새로운 어휘를 줬고, 스트림은 컬렉션 위의 선언적 파이프라인을 만들었으며, `Optional`은 null의 명시화를 시도했다. 한편 `java.time`은 `Date`와 `Calendar`의 사실상 종말을 선언했다. 한 번에 너무 많은 게 들어왔다고? 맞다. 그리고 바로 그 점이 이후 11년의 자바를 결정했다.

두 번째 변화는 *릴리스 모델의 전환*이다. Java 9가 JPMS(Project Jigsaw) 때문에 3년 가까이 지연되면서 OpenJDK는 결단을 내렸다. "한 거대한 기능이 전체 릴리스를 인질로 잡는 구조를 깨자." Java Chief Architect인 Mark Reinhold가 2017년 9월에 *Moving Java Forward Faster*라는 글로 이 새 모델을 공식화했다. 매년 3월과 9월에 새 버전을 내고, 그 시점에 준비된 JEP만 합류한다. 준비 안 된 기능은 다음 6개월을 기다린다. 마치 화물 열차처럼 — 시간에 맞춰 출발하고, 짐을 못 실은 화물은 다음 열차를 탄다. 이것이 *train model*이다.

이 두 변화가 결합되면 무엇이 보이는가? 람다·스트림이 한 번에 다 들어왔다는 사실보다, 그것이 6개월마다 다듬어지며 records·sealed·pattern matching·virtual thread로 *이어지는 연속체*라는 사실이 더 중요해진다. 그러니까 "자바를 따라간다"는 일은 더 이상 5년에 한 번씩 큰 점프를 하는 일이 아니다. 매년 두 번씩 누적되는 변화를 천천히 흡수하거나, LTS마다 한 번씩 모아서 따라잡는 일이 됐다.

## LTS 모델 — 8 / 11 / 17 / 21 / 25

엔터프라이즈 입장에서 진짜 의미 있는 라인은 LTS(Long-Term Support) 라인이다. 처음에는 3년에 한 번이었다 — 8(2014) → 11(2018) → 17(2021). 그러다 2021년 9월에 OpenJDK가 다시 결단했다. "LTS 간격을 2년으로 줄이자." 그렇게 17(2021) → 21(2023) → 25(2025) → 29(2027 예정)의 라인이 그려졌다.

LTS가 무엇을 의미하는지는 한 줄로 정리할 수 있다. *Oracle·Amazon Corretto·Azul Zulu·Eclipse Temurin·BellSoft Liberica*가 수년에 걸쳐 보안 패치를 약속하는 버전. 비-LTS는 다음 릴리스가 나오면 공식 패치가 끝난다. Java 18·19·20을 production에 올린 회사가 거의 없는 이유는 단순하다 — 6개월 뒤에는 패치를 못 받기 때문이다. 그러니 엔터프라이즈는 LTS만 추적하면 충분하다는 합리적 선택을 한다.

다만 그렇다고 비-LTS를 무시해도 되는가? 그건 아니다. records가 Java 14에서 preview로 처음 나와 16에서 표준화되기까지 두 차례 preview를 거치며 캐노니컬 생성자, compact constructor, JPA와의 충돌 같은 사실들이 다듬어졌다. virtual thread도 19에서 처음 preview로 나와 20에서 두 번째 preview, 21에서 표준화됐다. pattern matching for switch는 *네 번* preview를 거쳤다. LTS에 features가 안착한 시점에는 이미 비-LTS 단계에서 검증된 셈이다. 그러니 비-LTS를 production에 안 올리더라도 *읽어두는* 편이 낫다. LTS가 도착했을 때 놀라지 않으려면 말이다.

## 11년의 압축 연대기

11년의 변화를 한 페이지로 압축해보자. 각 LTS에 무엇이 들어왔는지, 그리고 그 사이 비-LTS들이 어떻게 다리를 놓았는지.

**Java 8 (2014, LTS) — 함수형의 도입.** 람다 표현식(JSR 335), Stream API, `Optional<T>`, `java.time`(JSR-310), `CompletableFuture`, 인터페이스 default·static 메서드, PermGen 제거와 Metaspace 도입. 11년이 지난 지금까지도 가장 오래 살아남은 베이스라인이다. 한국 엔터프라이즈, 특히 SI·금융권에서는 2025년에도 잔존 코드가 적지 않다.

**Java 9 (2017) — 모듈과 정리.** JPMS(`module-info.java`), JShell(REPL), `List.of/Set.of/Map.of`, `takeWhile/dropWhile`, `Optional.ifPresentOrElse`, `java.util.concurrent.Flow`(Reactive Streams 표준화), HTTP/2 client incubator. JPMS는 가장 야심찼고 가장 논쟁적이었다. (왜 그랬는지는 9장에서 따로 다룬다.)

**Java 10 (2018) — `var`.** 지역 변수 타입 추론. AppCDS도 이때 들어왔다. 6개월 케이던스의 첫 비-LTS.

**Java 11 (2018, LTS) — "포스트 8" 첫 LTS.** HttpClient 표준화(JEP 321), String 메서드 확장(`isBlank`, `lines`, `strip`, `repeat`), `Files.readString/writeString`, ZGC 실험 도입, Flight Recorder·Mission Control 오픈소스화. 그리고 *충격원*이 두 개. 첫째, JEP 320으로 Java EE / CORBA 모듈(JAXB, JAX-WS, JTA 등)이 JDK에서 제거됐다. 둘째, Oracle JDK가 유료화되면서 한국을 포함한 전 세계 기업이 OpenJDK·Corretto·Temurin으로 *대이주*했다.

**Java 12·13 (2019) — preview의 시대 시작.** Switch Expressions 미리보기(JEP 325), Text Blocks 미리보기(JEP 355), Shenandoah GC 실험. preview 키워드가 자바에 본격적으로 자리 잡은 시기다.

**Java 14 (2020) — records와 pattern matching for instanceof의 첫 등장.** Records preview(JEP 359), Pattern Matching for `instanceof` preview(JEP 305), Switch Expressions 표준화(JEP 361), `jpackage` incubator. Helpful NullPointerExceptions(JEP 358)는 의외로 실무에 즉시 효과를 줬다 — NPE 메시지가 "*어떤 표현식이* null이었는지" 알려주기 시작했다.

**Java 15 (2020) — Sealed Classes preview.** Sealed(JEP 360), Text Blocks 표준화(JEP 378), Nashorn 제거, ZGC·Shenandoah production-ready.

**Java 16 (2021) — Records 표준화, Pattern instanceof 표준화.** JEP 395·394. 그리고 JEP 396 — *Strongly Encapsulate JDK Internals by Default*. `sun.misc.Unsafe`처럼 internal API를 쓰면 경고가 뜨거나 실패하기 시작했다. 라이브러리들에게 큰 충격원이 됐다.

**Java 17 (2021, LTS) — Sealed 표준, Pattern Matching for switch preview.** JEP 409로 sealed가 표준이 됐고, JEP 406으로 switch pattern matching이 시작됐다. FFM 첫 incubator(JEP 412), Vector API 두 번째 incubator(JEP 414). 그리고 무엇보다 — *Spring Boot 3.0의 베이스라인이 됐다*. 2022년 11월에 Spring Boot 3.0이 나오면서 Java 17이 사실상 엔터프라이즈의 "Java 8 다음 정착지"가 됐다.

**Java 18·19·20 (2022~2023) — Loom의 첫 표면화.** UTF-8 default(JEP 400), Simple Web Server(`jwebserver`), Code Snippets(`{@snippet}`), Virtual Threads preview(JEP 425), Structured Concurrency incubator(JEP 428), Record Patterns preview(JEP 405), Scoped Values incubator(JEP 429). 비-LTS 세 개가 *모두 Loom으로 향하는 길*이었다.

**Java 21 (2023, LTS) — 동시성 모델의 전환점.** Virtual Threads 표준(JEP 444), Pattern Matching for switch 표준(JEP 441), Record Patterns 표준(JEP 440), Sequenced Collections(JEP 431), Generational ZGC(JEP 439), KEM API(JEP 452), Structured Concurrency preview(JEP 453), Scoped Values preview(JEP 446). 한국 엔터프라이즈가 17 다음 정착지로 21을 본격 검토하기 시작한 시점이다.

**Java 22·23·24 (2024~2025) — FFM 표준, Gatherers, AOT.** FFM 표준화(JEP 454) — JNI 시대의 종료 시작. Unnamed Variables(`_`), Stream Gatherers preview→standard(JEP 461→473→485), Markdown javadoc(JEP 467, `///`), JEP 491 — `synchronized` 블록의 virtual thread pinning 해결, JEP 483 — AOT Class Loading & Linking(Project Leyden의 첫 결실), Flexible Constructor Bodies preview, Class-File API 표준화.

**Java 25 (2025, LTS) — Compact Object Headers, AOT Cache 확장, Scoped Values 표준.** Compact Object Headers(JEP 519) — 64비트 JVM의 object header를 64비트로 압축, 메모리·캐시 효율 ~22% 개선 사례. Generational Shenandoah(JEP 521), AOT CLI ergonomics(JEP 514), AOT method profiling(JEP 515), Structured Concurrency 다섯 번째 preview(JEP 505), Scoped Values 표준(JEP 506), Module Import Declarations 표준(JEP 511) — `import module java.base;`가 가능, Compact Source Files + Instance Main(JEP 512) — `void main()` 단독 실행 가능, KDF API 표준(JEP 510), Flexible Constructor Bodies 표준(JEP 513).

11년이 한 단락에 다 들어간다. 그런데 한 가지 짚을 게 있다. 람다·스트림이 한 LTS(8)에 묶여서 들어왔고, records·sealed가 다른 LTS(17)에 묶여서 들어왔고, virtual thread가 또 다른 LTS(21)에 묶여서 들어왔다. 5년 단위로 보면 — 함수형 → 데이터지향 → 동시성. 세 번의 큰 파도가 LTS마다 한 번씩 친 셈이다. *왜 그 순서였는지*는 다음 장에서 본격적으로 다룬다.

## 한국 엔터프라이즈는 지금 어디 와 있는가

이 책의 독자가 가장 궁금해할 질문일 것이다. "그래서 우리만 뒤처진 건 아니지?" 답을 미리 말하자면, 그런 건 아니다.

대략의 분포는 이렇다. 첫째, *Java 8 잔존층*. 제조업·금융권·공공 SI의 레거시 시스템 다수, 그리고 한 번 11로 가려다 JEP 320 충격을 본 뒤 멈춘 코드베이스들. WebSphere·WebLogic 기반 J2EE 애플리케이션이 여기에 많다. 둘째, *Java 11/17 정착층*. 2020년 전후로 한 차례 이주를 단행한 모던 SaaS·핀테크·쇼핑몰 백엔드. Spring Boot 2.x → 3.x 전환과 함께 17로 올라간 사례가 다수다. 셋째, *Java 21 도입층*. 2024년부터 가시화. 우아한형제들, 카카오, 카카오페이의 기술 블로그에 virtual thread 도입 사례가 본격적으로 올라오기 시작한 게 이 시점이다. 우아한형제들의 *Java의 미래, Virtual Thread* 세미나(techblog.woowahan.com), 카카오의 제4회 Tech Meet *JDK 21의 Virtual Thread*(tech.kakao.com), 카카오페이의 *Virtual Thread에 봄(Spring)은 왔는가*(tech.kakaopay.com)가 한국 엔터프라이즈 입장에서 21이 *추상적 약속*에서 *실측 가능한 도구*로 옮겨가는 분기점이었다.

흥미로운 점은, 21이 정착되기 전에 25가 이미 도착했다는 것이다. 8→17→21→25의 LTS 라인을 보면, 한국 기업 대부분은 8→17 점프의 한가운데에 있거나, 17에 막 정착했거나, 21을 검토 중이다. 이 책은 그 상황을 정직하게 받아들인다. 모두가 25로 한 번에 가야 한다고 말하지 않는다. *자기 코드베이스가 어느 지층에 있는지 진단하고, 다음 한 발을 어디로 옮길지 결정하는 데 도움이 되는 책*을 목표로 한다.

## 가상의 회사 — PayBridge

추상적인 이야기로만 끝내지 말자. 책 전체를 관통할 가상의 회사를 한번 그려보자. 이름은 *PayBridge*다. 결제 SaaS 회사로, 2014년에 작은 스타트업으로 출발해 11년이 지난 지금은 한국·미국·동남아의 가맹점 수만 개를 처리하는 미들레이어 결제 플랫폼이 됐다. 책 곳곳에서 PayBridge의 코드와 인프라가 사례로 등장하고, 22장 결말에서는 PayBridge의 5년 뒤 코드를 함께 상상한다.

PayBridge의 코드베이스 변천을 한 페이지로 보자.

**2014년, 창업.** Java 7로 시작. Spring Framework 3.2, Tomcat 7, MySQL 5.5. 6개월 뒤 Java 8이 GA되자 람다와 스트림에 끌려 *조심스럽게* 8로 올린다. 처음에는 `for-each`를 `forEach(...)`로 바꾸는 수준. `Optional`은 *반환값에만* 쓰자는 가이드라인이 그때 정해진다.

**2016년, 성장기.** 트랜잭션 처리량이 늘면서 `CompletableFuture`로 외부 결제 게이트웨이 호출을 병렬화한다. `parallelStream()`을 결제 정산 배치에 무심코 썼다가 한 번 *p99 latency spike*를 본 뒤, *blocking I/O는 절대 parallelStream에 안 태운다*는 원칙이 사내 위키에 박힌다. (이 함정은 5장과 8B장에서 다시 만난다.)

**2018년, 첫 마이그레이션 시도.** Java 11이 LTS로 출시되자 마이그레이션을 검토한다. 그러나 PayBridge가 쓰던 JAX-WS 기반 외부 시스템 어댑터 두 개가 JEP 320 충격을 받는다. 일단 8에 머무르기로 결정. 대신 Oracle JDK 라이선스 변화로 *전사 OpenJDK(Eclipse Temurin) 이주*만 단행. 이때 처음으로 *런타임 벤더와 언어 버전이 분리된* 결정을 내린다.

**2021년, Spring Boot 3 예고.** Spring 측이 "Boot 3은 Java 17이 베이스라인"이라고 못 박자 PayBridge도 17 이주 계획을 짠다. 첫 시도는 2022년 봄. 코드 컴파일 에러 700개. 대부분은 `javax.*` → `jakarta.*` namespace 변환, 일부는 deprecated API 정리. 두 분기에 걸쳐 안착. 동시에 DTO 일부를 records로 옮긴다. JPA Entity로 records를 시도한 신입 개발자가 *좌절*하는 사건이 한 번 있고, 그 사건이 "Entity는 클래스, DTO·Projection·Command는 records"라는 사내 가이드라인의 출발점이 된다.

**2024년, virtual thread 검토.** Spring Boot 3.2가 `spring.threads.virtual.enabled` 설정을 추가하자, PayBridge의 결제 API 게이트웨이가 *thread-per-request 부활*의 가능성을 본다. 한 분기 PoC. p99 800ms → 250ms. 다만 한 차례 *덜컥*. HikariCP의 옛 버전을 쓰던 인스턴스 한 곳에서 `synchronized` 블록의 pinning으로 *deadlock*이 발생. JFR의 `jdk.VirtualThreadPinned` 이벤트로 진단하고, HikariCP 신 버전 + JEP 491(Java 24)을 기다리면서 일단 일부 트래픽만 VT로 전환.

**2025년 가을, 25 LTS.** PayBridge는 두 갈래로 간다. 결제 API 게이트웨이는 21에 머무르되 virtual thread 확장. 정산 배치는 25로 올려 Compact Object Headers로 메모리 ~20% 절감 + AOT Cache로 콜드 스타트 단축. records DTO, sealed `PaymentResult`, pattern matching `switch`로 도메인을 다시 그리는 작업이 진행 중. ScopedValue로 ThreadLocal 청소 누락이라는 옛 *찜찜함*을 정리하고, FFM으로 옛 native 어댑터 한 개를 JNI에서 옮긴다.

이 11년의 PayBridge 이야기가 익숙하게 들리는가? 그렇다면 좋은 신호다. 이 책 곳곳에서 PayBridge의 결제 처리, 정산 배치, 외부 API 통합 코드가 사례로 등장한다. 추상적인 *언어 기능*이 *어떤 코드를 어떻게 바꾸는지* 한 도메인의 11년을 통해 일관되게 보여주는 게 목표다.

## Spring Boot 시계열 — 자바 LTS의 거울

PayBridge 이야기에서 Spring Boot가 계속 등장한 데에는 이유가 있다. 엔터프라이즈 자바 개발자에게 *언어 LTS의 의미를 실무로 옮기는 통역사*가 Spring이다. Spring Boot의 메이저 버전이 어떤 자바 LTS를 베이스라인으로 잡았는지를 보면, *실무가 어느 LTS에 정착했는지*가 한 줄로 읽힌다.

- **Spring Boot 2.x (2018~2022)** — Java 8 베이스라인. 8년의 긴 수명. 한국 엔터프라이즈 대부분이 이 시기에 머물렀다.
- **Spring Boot 3.0 (2022.11)** — Java 17 베이스라인. `javax.*` → `jakarta.*` namespace 대변환. records DTO를 Spring이 일급으로 인식하기 시작.
- **Spring Boot 3.2 (2023.11)** — Java 21 지원 + `spring.threads.virtual.enabled` 한 줄 설정으로 virtual thread를 Tomcat·Jetty의 request handler에 켤 수 있게 됨. 동시에 Spring AOT가 GraalVM native image와 짝을 이뤄 cold-start 문제를 풀기 시작.
- **Spring Boot 3.3+ (2024~)** — JDK CDS 통합 + Project Leyden 대비. training run으로 AOT cache를 만들어 다음 실행부터 ~40% startup 단축.

엔터프라이즈에서 자바 LTS를 따라가는 일은 결국 Spring Boot의 메이저 마이그레이션을 따라가는 일이기도 하다. 둘은 한 몸이다. (Spring 시너지는 21장에서 본격적으로 다룬다.)

## 이 책의 범위와 읽는 방법

이쯤 와서 한 가지 약속을 명확히 하자. 이 책이 *다루는* 범위와 *다루지 않는* 범위.

다룬다: Java 8부터 25까지 60개+의 JEP, 그 중 엔터프라이즈에 의미 있는 ~40개. JLS의 핵심 인용(§15.27 람다, §17.4 JMM, §8.10 records, §8.1.1.2 sealed, §14.30 patterns, §7.7 modules 등). 함수형·데이터지향·동시성 세 축의 *왜*. Spring Framework / Boot의 통합 지점. 한국 엔터프라이즈의 마이그레이션 현실. 미래의 자바(Valhalla·Amber·Babylon·Leyden).

다루지 않는다: 자바 입문(람다 문법을 처음 배우는 단계는 가볍게 복습만). Kotlin·Scala·Groovy 비교(필요할 때 한 줄씩만). 안드로이드 개발(Android의 Java는 별개의 생태계). Quarkus·Helidon·Micronaut의 비교 분석(주로 Spring 베이스).

읽는 방법은 네 가지다. 첫째, *처음부터 끝까지 — 통사 독해.* 자바의 11년을 한 줄의 이야기로 읽고 싶다면. 둘째, *주제별 심층 독해.* Part II~III(함수형) → Part VI(데이터지향) → Part VII(동시성). 셋째, *실무 적용 우선.* Part IX(마이그레이션) → Part I(지형도) → 필요한 주제만. 넷째, *레퍼런스 사용.* 13장(Pattern Matching), 14장(Virtual Threads), 17장(GC), 19A장(도구) 같은 챕터는 그 자체로 펴 보는 레퍼런스로 쓸 수 있다. 각 챕터 헤더에 "이 챕터를 읽기 전 권장: 챕터 N" 미니 박스를 둬서, 어느 길로 들어와도 길을 잃지 않게 했다.

## 마무리

여기까지가 지도다. 11년의 자바, 한 장의 지도. 이 한 장에 다 담을 수 없는 깊이가 25개 챕터에 펼쳐진다.

다만 한 가지 더 짚자. 우리는 아직 *왜 이 순서였는지*를 묻지 않았다. 람다가 8에 먼저, records가 17에 먼저, virtual thread가 21에 먼저. 이 순서는 우연이 아니다. 그 안에는 자바를 끌고 온 다섯 가지 *동력*이 있다. 함수형 패러다임. 데이터지향. 동시성. 메모리·성능. 그리고 도구. 다음 장에서는 그 다섯 동력을 살펴보자. 그 다섯이 책 전체의 부(Part) 구조를 어떻게 만들었는지, 그리고 PayBridge의 11년이 어떻게 그 다섯을 따라 흘러왔는지 — 함께 들여다보자.
