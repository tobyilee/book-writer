# Modern Java Bible
## Java 8에서 25까지, 그리고 그 너머

**저자**: Toby-AI
**판본**: v1.0.0 · 2026-05-11

---

## 차례

- 서론. 왜 이 책인가
- **Part I. 11년의 자바, 한 장의 지도**
  - 1장. 11년의 자바, 한 장의 지도
  - 2장. 11년 변화의 다섯 가지 동력
- **Part II. 함수형 자바의 어휘**
  - 3장. 람다와 함수형 인터페이스 — 그 익숙함의 진짜 의미
  - 4장. `java.time`과 종종 잊히는 Java 8의 보석들
- **Part III. 스트림과 Optional의 모든 것**
  - 5장. Stream API — 선언적 데이터 파이프라인의 해부
  - 6장. Collector · Reducer · Gatherer — Stream의 종착과 새 중간 정거장
  - 7장. `Optional<T>` — 약속과 함정
- **Part IV. 동시성 I — Loom 이전의 모든 것**
  - 8A장. j.u.c와 Java Memory Model — 동시성의 토대
  - 8B장. CompletableFuture와 Reactive Streams Flow — 비동기 조합의 두 갈래
- **Part V. 언어 표면의 진화 (Java 9 ~ Java 23)**
  - 9장. JPMS — 실패인가 미완인가
  - 10장. `var` · switch · text blocks · Sequenced Collections — 작지만 결정적인 변화
- **Part VI. 데이터지향 자바 — Records · Sealed · Pattern**
  - 11장. Records — 자바가 마침내 인정한 "데이터의 신원"
  - 12장. Sealed Classes — 합 타입(Sum Type)이 자바에 들어온 날
  - 13장. Pattern Matching — ADT를 풀어내는 도구
- **Part VII. 동시성 II — Loom 시대**
  - 14장. Virtual Threads — thread-per-request의 부활
  - 15장. Pinning · ThreadLocal · 함정들 — Virtual Thread가 우리를 실망시키는 자리
  - 16장. Structured Concurrency와 Scoped Values — concurrent 코드의 문법
- **Part VIII. 메모리 · 네이티브 · 성능 · 도구**
  - 17장. GC 11년의 진화 — Serial부터 Generational Shenandoah까지
  - 18장. Foreign Function & Memory API · Vector API · Class-File API
  - 19장. AOT · Leyden · Compact Object Headers — 시작 시간과 메모리의 새 풍경
  - 19A장. 모던 자바의 도구들 — JShell부터 jextract까지
- **Part IX. 마이그레이션 · 보안 · Spring 시너지**
  - 20장. Java 8 → 17 마이그레이션 — 현장의 함정과 권장 순서
  - 20A장. 자바 보안의 11년 변화 — SecurityManager의 종말부터 KEM·KDF까지
  - 21장. Spring Boot 3.x × Java 21/25 — 시너지의 *고유성*
- **Part X. 다음 자바**
  - 22장. Valhalla · Amber · Babylon · Leyden — 26 이후의 자바
- **부록**
  - 부록 A. JEP 일람
  - 부록 B. JLS 인용 인덱스
  - 부록 C. 마이그레이션 체크리스트
  - 부록 D. Java 8 vs 25 코드 패턴 30선
- 판권

---

# 서론. 왜 이 책인가

11년 전, 람다를 처음 만났던 날을 기억하는가.

`Collections.sort()`에 `Comparator` 익명 클래스 다섯 줄을 적던 손이 갑자기 한 줄로 줄어든 그 순간 말이다. `list.sort(Comparator.comparing(User::getName))`. 그날의 가벼운 흥분은 곧 의심으로 바뀌었다. "이게 정말 자바인가?" "익명 클래스의 문법 설탕에 불과한 거 아닌가?" "어차피 안쪽은 `invokedynamic`이라던데, 성능은 괜찮은가?" 우리는 그렇게 자바와의 새로운 관계를 시작했다.

그리고 11년이 지났다. 그사이 자바는 람다와 스트림을 넘어 records, sealed, pattern matching, virtual thread, foreign function & memory, structured concurrency, scoped values까지 굵직한 도구를 줄줄이 출시했다. LTS 모델이 바뀌었고, 6개월 케이던스가 정착했으며, Spring은 Boot 3.x로 Java 17을 베이스라인으로 못 박았다. Oracle JDK의 라이선스 변화로 한 차례 대이주가 있었고, OpenJDK 빌드는 production-grade가 됐다. *Project Loom*이라는 이름은 *Project Valhalla*만큼이나 익숙해졌다.

그런데 — 솔직해지자. 우리 코드베이스는 거기까지 따라왔는가?

여전히 `Date`와 `Calendar`가 살아 있는 모듈이 있고, `instanceof` 캐스트 사다리가 9단까지 늘어난 컨트롤러가 있다. DTO에 Lombok이 잔뜩 붙어 있고, 결제 처리 컨트롤러는 200개짜리 Tomcat 스레드 풀로 p99를 800ms에 맞춰 버티고 있다. 옆 팀은 records를 도입했다지만, 우리 팀은 JPA Entity에 records를 시도했다가 좌절한 사람이 둘이나 있다. 그 사이 신입은 입사 첫날 `switch expression`을 쓰는 코드를 자연스럽게 짜고, 시니어는 그 코드를 봐도 *왜 그게 더 나은지* 한 문장으로 설명하지 못한다. 어딘가 *찜찜하다*.

이 책은 그 찜찜함에서 출발한다.

11년의 자바 진화를 한 권으로 묶어 읽는 일은 단순한 회고가 아니다. 람다·records·virtual thread가 *왜 이 순서로* 들어왔는지 이해하는 일이고, 그 순서가 다음 5년의 자바를 어떻게 결정할지 가늠하는 일이다. 자바가 "변하지 않는 언어"라는 통념은 이미 깨졌다. 그러나 그 자리에 들어선 "변하는 자바"의 정체를 우리는 충분히 알고 있는가? 매년 두 번의 릴리스가 나오는데, 그 변화를 한 문장으로 설명할 수 있는 동료가 팀에 몇이나 있는가? 8년째 같은 코드베이스를 만지면서 새 릴리스 노트가 나올 때마다 *피로감*을 먼저 느끼는 사람이 우리 자신은 아닌가?

그렇기에 *지금* 이 책이 필요하다.

이 책은 "Bible"이라는 이름의 무게를 정직하게 받아들인다. 책장에 꽂아두고 11년 치 자바 진화를 한 권으로 추적하는 항해 지도가 되겠다는 약속이다. 망라성과 깊이 둘 다 — 가볍게 훑고 끝낼 책이라면 굳이 Bible이라 부를 이유가 없다. 그러나 동시에 약속은 정직해야 한다. 이 책은 모든 자바 입문서가 아니다. Spring Framework로 엔터프라이즈 앱을 만들면서 Java 8~11에 머물러 있고, records·sealed·virtual thread를 "들어는 봤다" 수준에 있는 *중급 이상의 자바 개발자*를 위한 책이다. JLS의 happens-before가 무엇을 말하는지, `effectively final`의 정확한 정의가 무엇인지, Stream Gatherer가 fold의 일반화임을 코드로 보여달라 — 그런 깊이를 원하는 사람을 위한 책이다.

본문은 25개 장과 4개의 부록으로 구성됐다. 1·2장은 11년 전체를 한눈에 보는 지형도다. 이어 함수형(3~7장), Loom 이전 동시성(8A·8B), 언어 표면의 진화(9·10), 데이터지향(11~13), Loom 시대 동시성(14~16), 성능·네이티브·도구(17~19A), 마이그레이션·보안·Spring 시너지(20~21), 그리고 다음 자바(22)로 이어진다. 부록에는 JEP 일람, JLS 인용 색인, 마이그레이션 체크리스트, "Java 8 vs Java 25 코드 패턴 30선"이 들어 있다. 처음부터 끝까지 통사로 읽어도 되고, Part II→VI→VII로 주제별 심층 독해도 가능하며, Part IX 마이그레이션을 먼저 본 뒤 필요한 장으로 가지를 뻗어도 된다. 각 장 첫머리에는 "이 챕터를 읽기 전 권장: 챕터 N"이라는 안내 박스가 있어, 어느 길로 들어와도 길을 잃지 않게 했다.

한 가지 더 약속하자. 이 책은 "이렇게 써야 한다"고 강요하지 않는다. *왜 그렇게 쓰는 편이 나은지* 보여주고, 그 판단을 독자에게 넘긴다. JLS 인용은 그 판단의 근거를 정확하게 깔아주기 위한 장치다. 코드 비판은 "이건 틀렸다" 대신 "이건 *찜찜하다*", "*번거롭다*"라는 감각의 언어로 한다. 함께 코드를 다듬어 나가는 동반자의 자리에 책을 두고 싶다. 11년의 자바를 견뎌낸 우리의 동료로서.

자, 함께 11년을 거슬러보자. 첫 장에서는 지도를 펼쳐 우리가 *지금 어디 와 있는지* 짚어볼 차례다.

---

# Part I. 11년의 자바, 한 장의 지도

자바를 11년 단위로 들여다본다는 일은 어딘가 위태롭다. 11년이면 두 번의 LTS 사이클이 끼고, 람다와 records와 virtual thread가 모두 들어왔다. 그 안에서 "Modern Java"가 무엇인지 한 줄로 답하기란 쉽지 않다. 그래서 우리는 본격적인 챕터에 들어가기 전에 *지도부터 펼친다*.

Part I의 두 장은 책 전체를 떠받치는 *지형도*다. 1장은 시간 축을 따라 Java 8부터 Java 25까지 11년의 압축 연대기를 그린다. LTS 모델, 6개월 케이던스, 그 사이를 흘러간 60여 개의 JEP를 한 장에 압축한다. 한국 엔터프라이즈의 분포 — Java 8 잔존, 17 정착, 21 도입 — 가 이 지도 위에 어디쯤 점을 찍는지도 짚어둔다. 책 전체를 관통할 가상의 회사 *PayBridge*가 등장하는 자리이기도 하다. 11년의 결제 SaaS 코드베이스가 어떻게 자바와 함께 변해왔는지, PayBridge의 이야기로 추상적 변화에 살을 붙인다.

2장은 시간 축이 아니라 *동력*의 축이다. 람다·records·virtual thread가 왜 *이 순서로* 들어왔는지를 묻는다. 그 답은 자바를 끌어온 다섯 가지 동력 — *함수형 패러다임*, *데이터지향*, *Loom(동시성)*, *Panama(네이티브)*, *Leyden(시작 시간)* — 으로 풀어낸다. 각 동력은 OpenJDK의 한 *Project*에 대응하고, 그 Project들이 책의 부(Part) 구조로 그대로 이어진다. Brian Goetz의 *Data-Oriented Programming in Java*가 그리는 큰 그림이 이 장의 등뼈다.

두 장을 다 읽고 나면, 우리는 *자바의 어디쯤에 와 있는지*, 그리고 *왜 그 순서로 와 있는지*를 동시에 알게 된다. 이 두 축이 책 나머지의 좌표계를 만든다. Part II부터는 그 좌표계 위에서 함수형·데이터지향·동시성을 차례로 깊이 판다.

자, 지도를 펼치자.

---

## 1장. 11년의 자바, 한 장의 지도

당신의 회사 코드베이스가 Java 8에 멈춰 있다고 해보자.

빌드 스크립트 어딘가에 `sourceCompatibility = 1.8`이라고 적혀 있고, 운영 서버에는 Oracle JDK 8u201이 깔려 있다. 누군가 한 번 Java 11로 올리려다가 Java EE 모듈 제거(JEP 320) 충격을 본 뒤 조용히 손을 뗀 흔적이 git log에 남아 있다. PR 리뷰에는 여전히 `Optional<List<T>>`가 올라오고, DTO 옆에는 Lombok이 친절하게 붙어 있다. 매주 월요일 회의에서 누군가 "그래서 우리도 records 좀 써야 하는 거 아닙니까?"라고 물으면, 시니어는 "JPA Entity는 안 돼"라고만 답하고 회의는 다음 안건으로 넘어간다. 어딘가 *난감하다*. 어딘가 안 풀린다. 그런데 새 LTS인 25가 나왔다고 한다. *또 새 버전이라니.*

자, 그렇다면 지금 우리는 자바의 어디쯤에 와 있을까? 한 장의 지도를 펼쳐보자.

### 두 개의 변화가 한꺼번에 일어났다

"Modern Java"라는 말을 들으면 보통 두 가지가 떠오른다. 람다와 스트림이 들어왔다는 것. 그리고 매년 두 번씩 새 버전이 나온다는 것. 둘은 별개의 사건처럼 보이지만, 실제로는 한 몸이다.

첫 번째 변화는 *언어 패러다임의 확장*이다. Java 8(2014년 3월)이 람다·스트림·`Optional`·`java.time`을 묶어 출시하면서, 자바는 객체지향 단일 노선의 언어에서 함수형·데이터지향·동시성 친화적 언어로 확장됐다. 람다는 `java.util.function`의 함수형 인터페이스 묶음과 결합해 코드에 새로운 어휘를 줬고, 스트림은 컬렉션 위의 선언적 파이프라인을 만들었으며, `Optional`은 null의 명시화를 시도했다. 한편 `java.time`은 `Date`와 `Calendar`의 사실상 종말을 선언했다. 한 번에 너무 많은 게 들어왔다고? 맞다. 그리고 바로 그 점이 이후 11년의 자바를 결정했다.

두 번째 변화는 *릴리스 모델의 전환*이다. Java 9가 JPMS(Project Jigsaw) 때문에 3년 가까이 지연되면서 OpenJDK는 결단을 내렸다. "한 거대한 기능이 전체 릴리스를 인질로 잡는 구조를 깨자." Java Chief Architect인 Mark Reinhold가 2017년 9월에 *Moving Java Forward Faster*라는 글로 이 새 모델을 공식화했다. 매년 3월과 9월에 새 버전을 내고, 그 시점에 준비된 JEP만 합류한다. 준비 안 된 기능은 다음 6개월을 기다린다. 마치 화물 열차처럼 — 시간에 맞춰 출발하고, 짐을 못 실은 화물은 다음 열차를 탄다. 이것이 *train model*이다.

이 두 변화가 결합되면 무엇이 보이는가? 람다·스트림이 한 번에 다 들어왔다는 사실보다, 그것이 6개월마다 다듬어지며 records·sealed·pattern matching·virtual thread로 *이어지는 연속체*라는 사실이 더 중요해진다. 그러니까 "자바를 따라간다"는 일은 더 이상 5년에 한 번씩 큰 점프를 하는 일이 아니다. 매년 두 번씩 누적되는 변화를 천천히 흡수하거나, LTS마다 한 번씩 모아서 따라잡는 일이 됐다.

### LTS 모델 — 8 / 11 / 17 / 21 / 25

엔터프라이즈 입장에서 진짜 의미 있는 라인은 LTS(Long-Term Support) 라인이다. 처음에는 3년에 한 번이었다 — 8(2014) → 11(2018) → 17(2021). 그러다 2021년 9월에 OpenJDK가 다시 결단했다. "LTS 간격을 2년으로 줄이자." 그렇게 17(2021) → 21(2023) → 25(2025) → 29(2027 예정)의 라인이 그려졌다.

LTS가 무엇을 의미하는지는 한 줄로 정리할 수 있다. *Oracle·Amazon Corretto·Azul Zulu·Eclipse Temurin·BellSoft Liberica*가 수년에 걸쳐 보안 패치를 약속하는 버전. 비-LTS는 다음 릴리스가 나오면 공식 패치가 끝난다. Java 18·19·20을 production에 올린 회사가 거의 없는 이유는 단순하다 — 6개월 뒤에는 패치를 못 받기 때문이다. 그러니 엔터프라이즈는 LTS만 추적하면 충분하다는 합리적 선택을 한다.

다만 그렇다고 비-LTS를 무시해도 되는가? 그건 아니다. records가 Java 14에서 preview로 처음 나와 16에서 표준화되기까지 두 차례 preview를 거치며 캐노니컬 생성자, compact constructor, JPA와의 충돌 같은 사실들이 다듬어졌다. virtual thread도 19에서 처음 preview로 나와 20에서 두 번째 preview, 21에서 표준화됐다. pattern matching for switch는 *네 번* preview를 거쳤다. LTS에 features가 안착한 시점에는 이미 비-LTS 단계에서 검증된 셈이다. 그러니 비-LTS를 production에 안 올리더라도 *읽어두는* 편이 낫다. LTS가 도착했을 때 놀라지 않으려면 말이다.

### 11년의 압축 연대기

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

### 한국 엔터프라이즈는 지금 어디 와 있는가

이 책의 독자가 가장 궁금해할 질문일 것이다. "그래서 우리만 뒤처진 건 아니지?" 답을 미리 말하자면, 그런 건 아니다.

대략의 분포는 이렇다. 첫째, *Java 8 잔존층*. 제조업·금융권·공공 SI의 레거시 시스템 다수, 그리고 한 번 11로 가려다 JEP 320 충격을 본 뒤 멈춘 코드베이스들. WebSphere·WebLogic 기반 J2EE 애플리케이션이 여기에 많다. 둘째, *Java 11/17 정착층*. 2020년 전후로 한 차례 이주를 단행한 모던 SaaS·핀테크·쇼핑몰 백엔드. Spring Boot 2.x → 3.x 전환과 함께 17로 올라간 사례가 다수다. 셋째, *Java 21 도입층*. 2024년부터 가시화. 우아한형제들, 카카오, 카카오페이의 기술 블로그에 virtual thread 도입 사례가 본격적으로 올라오기 시작한 게 이 시점이다. 우아한형제들의 *Java의 미래, Virtual Thread* 세미나(techblog.woowahan.com), 카카오의 제4회 Tech Meet *JDK 21의 Virtual Thread*(tech.kakao.com), 카카오페이의 *Virtual Thread에 봄(Spring)은 왔는가*(tech.kakaopay.com)가 한국 엔터프라이즈 입장에서 21이 *추상적 약속*에서 *실측 가능한 도구*로 옮겨가는 분기점이었다.

흥미로운 점은, 21이 정착되기 전에 25가 이미 도착했다는 것이다. 8→17→21→25의 LTS 라인을 보면, 한국 기업 대부분은 8→17 점프의 한가운데에 있거나, 17에 막 정착했거나, 21을 검토 중이다. 이 책은 그 상황을 정직하게 받아들인다. 모두가 25로 한 번에 가야 한다고 말하지 않는다. *자기 코드베이스가 어느 지층에 있는지 진단하고, 다음 한 발을 어디로 옮길지 결정하는 데 도움이 되는 책*을 목표로 한다.

### 가상의 회사 — PayBridge

추상적인 이야기로만 끝내지 말자. 책 전체를 관통할 가상의 회사를 한번 그려보자. 이름은 *PayBridge*다. 결제 SaaS 회사로, 2014년에 작은 스타트업으로 출발해 11년이 지난 지금은 한국·미국·동남아의 가맹점 수만 개를 처리하는 미들레이어 결제 플랫폼이 됐다. 책 곳곳에서 PayBridge의 코드와 인프라가 사례로 등장하고, 22장 결말에서는 PayBridge의 5년 뒤 코드를 함께 상상한다.

PayBridge의 코드베이스 변천을 한 페이지로 보자.

**2014년, 창업.** Java 7로 시작. Spring Framework 3.2, Tomcat 7, MySQL 5.5. 6개월 뒤 Java 8이 GA되자 람다와 스트림에 끌려 *조심스럽게* 8로 올린다. 처음에는 `for-each`를 `forEach(...)`로 바꾸는 수준. `Optional`은 *반환값에만* 쓰자는 가이드라인이 그때 정해진다.

**2016년, 성장기.** 트랜잭션 처리량이 늘면서 `CompletableFuture`로 외부 결제 게이트웨이 호출을 병렬화한다. `parallelStream()`을 결제 정산 배치에 무심코 썼다가 한 번 *p99 latency spike*를 본 뒤, *blocking I/O는 절대 parallelStream에 안 태운다*는 원칙이 사내 위키에 박힌다. (이 함정은 5장과 8B장에서 다시 만난다.)

**2018년, 첫 마이그레이션 시도.** Java 11이 LTS로 출시되자 마이그레이션을 검토한다. 그러나 PayBridge가 쓰던 JAX-WS 기반 외부 시스템 어댑터 두 개가 JEP 320 충격을 받는다. 일단 8에 머무르기로 결정. 대신 Oracle JDK 라이선스 변화로 *전사 OpenJDK(Eclipse Temurin) 이주*만 단행. 이때 처음으로 *런타임 벤더와 언어 버전이 분리된* 결정을 내린다.

**2021년, Spring Boot 3 예고.** Spring 측이 "Boot 3은 Java 17이 베이스라인"이라고 못 박자 PayBridge도 17 이주 계획을 짠다. 첫 시도는 2022년 봄. 코드 컴파일 에러 700개. 대부분은 `javax.*` → `jakarta.*` namespace 변환, 일부는 deprecated API 정리. 두 분기에 걸쳐 안착. 동시에 DTO 일부를 records로 옮긴다. JPA Entity로 records를 시도한 신입 개발자가 *좌절*하는 사건이 한 번 있고, 그 사건이 "Entity는 클래스, DTO·Projection·Command는 records"라는 사내 가이드라인의 출발점이 된다.

**2024년, virtual thread 검토.** Spring Boot 3.2가 `spring.threads.virtual.enabled` 설정을 추가하자, PayBridge의 결제 API 게이트웨이가 *thread-per-request 부활*의 가능성을 본다. 한 분기 PoC. p99 800ms → 250ms. 다만 한 차례 *덜컥*. HikariCP의 옛 버전을 쓰던 인스턴스 한 곳에서 `synchronized` 블록의 pinning으로 *deadlock*이 발생. JFR의 `jdk.VirtualThreadPinned` 이벤트로 진단하고, HikariCP 신 버전 + JEP 491(Java 24)을 기다리면서 일단 일부 트래픽만 VT로 전환.

**2025년 가을, 25 LTS.** PayBridge는 두 갈래로 간다. 결제 API 게이트웨이는 21에 머무르되 virtual thread 확장. 정산 배치는 25로 올려 Compact Object Headers로 메모리 ~20% 절감 + AOT Cache로 콜드 스타트 단축. records DTO, sealed `PaymentResult`, pattern matching `switch`로 도메인을 다시 그리는 작업이 진행 중. ScopedValue로 ThreadLocal 청소 누락이라는 옛 *찜찜함*을 정리하고, FFM으로 옛 native 어댑터 한 개를 JNI에서 옮긴다.

이 11년의 PayBridge 이야기가 익숙하게 들리는가? 그렇다면 좋은 신호다. 이 책 곳곳에서 PayBridge의 결제 처리, 정산 배치, 외부 API 통합 코드가 사례로 등장한다. 추상적인 *언어 기능*이 *어떤 코드를 어떻게 바꾸는지* 한 도메인의 11년을 통해 일관되게 보여주는 게 목표다.

### Spring Boot 시계열 — 자바 LTS의 거울

PayBridge 이야기에서 Spring Boot가 계속 등장한 데에는 이유가 있다. 엔터프라이즈 자바 개발자에게 *언어 LTS의 의미를 실무로 옮기는 통역사*가 Spring이다. Spring Boot의 메이저 버전이 어떤 자바 LTS를 베이스라인으로 잡았는지를 보면, *실무가 어느 LTS에 정착했는지*가 한 줄로 읽힌다.

- **Spring Boot 2.x (2018~2022)** — Java 8 베이스라인. 8년의 긴 수명. 한국 엔터프라이즈 대부분이 이 시기에 머물렀다.
- **Spring Boot 3.0 (2022.11)** — Java 17 베이스라인. `javax.*` → `jakarta.*` namespace 대변환. records DTO를 Spring이 일급으로 인식하기 시작.
- **Spring Boot 3.2 (2023.11)** — Java 21 지원 + `spring.threads.virtual.enabled` 한 줄 설정으로 virtual thread를 Tomcat·Jetty의 request handler에 켤 수 있게 됨. 동시에 Spring AOT가 GraalVM native image와 짝을 이뤄 cold-start 문제를 풀기 시작.
- **Spring Boot 3.3+ (2024~)** — JDK CDS 통합 + Project Leyden 대비. training run으로 AOT cache를 만들어 다음 실행부터 ~40% startup 단축.

엔터프라이즈에서 자바 LTS를 따라가는 일은 결국 Spring Boot의 메이저 마이그레이션을 따라가는 일이기도 하다. 둘은 한 몸이다. (Spring 시너지는 21장에서 본격적으로 다룬다.)

### 이 책의 범위와 읽는 방법

이쯤 와서 한 가지 약속을 명확히 하자. 이 책이 *다루는* 범위와 *다루지 않는* 범위.

다룬다: Java 8부터 25까지 60개+의 JEP, 그 중 엔터프라이즈에 의미 있는 ~40개. JLS의 핵심 인용(§15.27 람다, §17.4 JMM, §8.10 records, §8.1.1.2 sealed, §14.30 patterns, §7.7 modules 등). 함수형·데이터지향·동시성 세 축의 *왜*. Spring Framework / Boot의 통합 지점. 한국 엔터프라이즈의 마이그레이션 현실. 미래의 자바(Valhalla·Amber·Babylon·Leyden).

다루지 않는다: 자바 입문(람다 문법을 처음 배우는 단계는 가볍게 복습만). Kotlin·Scala·Groovy 비교(필요할 때 한 줄씩만). 안드로이드 개발(Android의 Java는 별개의 생태계). Quarkus·Helidon·Micronaut의 비교 분석(주로 Spring 베이스).

읽는 방법은 네 가지다. 첫째, *처음부터 끝까지 — 통사 독해.* 자바의 11년을 한 줄의 이야기로 읽고 싶다면. 둘째, *주제별 심층 독해.* Part II~III(함수형) → Part VI(데이터지향) → Part VII(동시성). 셋째, *실무 적용 우선.* Part IX(마이그레이션) → Part I(지형도) → 필요한 주제만. 넷째, *레퍼런스 사용.* 13장(Pattern Matching), 14장(Virtual Threads), 17장(GC), 19A장(도구) 같은 챕터는 그 자체로 펴 보는 레퍼런스로 쓸 수 있다. 각 챕터 헤더에 "이 챕터를 읽기 전 권장: 챕터 N" 미니 박스를 둬서, 어느 길로 들어와도 길을 잃지 않게 했다.

### 마무리

여기까지가 지도다. 11년의 자바, 한 장의 지도. 이 한 장에 다 담을 수 없는 깊이가 25개 챕터에 펼쳐진다.

다만 한 가지 더 짚자. 우리는 아직 *왜 이 순서였는지*를 묻지 않았다. 람다가 8에 먼저, records가 17에 먼저, virtual thread가 21에 먼저. 이 순서는 우연이 아니다. 그 안에는 자바를 끌고 온 다섯 가지 *동력*이 있다. 함수형 패러다임. 데이터지향. 동시성. 메모리·성능. 그리고 도구. 다음 장에서는 그 다섯 동력을 살펴보자. 그 다섯이 책 전체의 부(Part) 구조를 어떻게 만들었는지, 그리고 PayBridge의 11년이 어떻게 그 다섯을 따라 흘러왔는지 — 함께 들여다보자.

---

## 2장. 11년 변화의 다섯 가지 동력

기획 회의에서 "왜 굳이 21로?"라는 질문이 나왔다고 해보자.

화면에는 마이그레이션 일정과 인력 산정이 띄워져 있고, 회의실 끝에서 누군가가 손을 든다. "Java 17은 작년에 막 올렸잖아요. 잘 돌고 있어요. 왜 *지금* 또 21이에요? 그것도 records·virtual thread 같은 큰 변화가 있다면서요. 8에서 17로 올 때도 컴파일 에러 700개를 봤는데, 또 그런 거 보자고요?" 회의실은 잠시 조용해진다. 답을 못 하면 새 LTS 마이그레이션 첫날의 *난감함*이 모두에게 옮겨붙는다. 그 답은 의외로 간단하지만, 단순하지는 않다. 자바의 변화는 *무작위*가 아니라 다섯 갈래의 *동력*이 시기별로 결과를 낸 것이고, 21은 그 다섯 중 셋째가 임계점을 넘은 LTS이기 때문이다.

자, 그렇다면 그 다섯 동력을 함께 살펴보자.

### 왜 이 순서였을까

자바의 11년을 가만히 들여다보면 한 가지가 보인다. 람다·records·virtual thread가 *이 순서로* 들어왔다는 사실. 무작위로 보이지 않는다. 람다(8) → records(17) → virtual thread(21)에 정확히 4년 간격이 있고, 그 사이에 비-LTS들이 다리를 놓는다. 더 흥미로운 점은 — 비-LTS의 변화도 *셋 중 하나의 동력*에 속한다는 것이다.

이 책은 11년의 자바를 다섯 동력으로 묶어 본다. 다섯 동력에는 OpenJDK 내부에서 부르는 *프로젝트 이름*이 붙어 있다. 그리고 각 프로젝트는 책의 한 부(Part)에 대응된다. 그러니까 이 장은 *책 전체의 미리보기*이기도 하다.

다섯 동력은 다음과 같다.

1. **함수형 패러다임** — *Project Lambda*에서 시작해 *Stream Gatherers*까지.
2. **데이터지향** — *Project Amber*가 그린 records·sealed·pattern matching.
3. **동시성** — *Project Loom*의 virtual thread·structured concurrency·scoped values.
4. **메모리·네이티브·성능** — *Project Panama*(FFM·Vector)와 *Project Leyden*(AOT·startup), 그리고 GC 진화.
5. **도구와 언어 표면의 정리** — JPMS·`var`·switch·text blocks·markdown javadoc·module import 같은 *작지만 결정적인* 변화들.

각각을 차례로 들여다보자. 그리고 각 동력의 끝에는 *그 동력이 책의 어느 부에서 본격적으로 다뤄지는지* 표시해두겠다.

### 첫째 동력 — 함수형 패러다임 (Project Lambda → Gatherers)

자바가 함수형으로 옮겨가는 일은 한 LTS의 사건이 아니라 *11년에 걸친 점진적 흡수*다.

시작은 분명하다. 2014년 Java 8, JSR 335. 람다 표현식과 함수형 인터페이스, 그리고 그 위에 얹힌 Stream API. 그날부터 자바 개발자는 `Function`, `Predicate`, `Supplier`, `Consumer`, `BiFunction`이라는 새 어휘를 손에 쥐었다. `for-each` 루프가 `forEach(...)`로 바뀌고, `Comparator` 익명 클래스가 `Comparator.comparing(User::getName)`이 됐다. Stephen Colebourne의 `java.time`(JSR-310)이 함께 들어와 `Date`와 `Calendar`의 종말을 선언했다.

그러나 *진짜 함수형*은 8에 다 들어오지 못했다. `Optional<T>`는 8에 있었지만 `ifPresentOrElse`·`or`·`stream`은 9에서야 추가됐다. `Stream::toList`는 16에서야 들어왔다 — 그 전까지 `collect(Collectors.toUnmodifiableList())`라는 *번거로움*을 견뎌야 했다. `takeWhile`·`dropWhile`·`iterate(seed, hasNext, next)` 같은 자연스러운 연산이 9에서 추가됐다. 가장 결정적인 진화는 한참 뒤에 왔다. **Stream Gatherers** — JEP 461(22 preview) → 473(23 second preview) → 485(24 standard). 그동안 *Stream에선 자연스럽지 않다*고 여겨졌던 슬라이딩 윈도우, prefix sum, 병렬 매핑이 한 줄로 표현 가능해진 것이다. 5분 이동 평균을 구하는 데 `Collectors.toMap`을 1000번 쓰던 *지긋지긋함*은 이제 옛이야기가 됐다.

함수형 패러다임의 진짜 의미는 *문법*이 아니다. `reduce`의 monoid 속성(identity·associativity), `flatMap`의 monad 의미, Collector의 5요소(supplier·accumulator·combiner·finisher·characteristics)가 fold의 일반화임을 인지하는 *시야*다. 그 시야는 한 번 들어오면 Optional, Stream, CompletableFuture, Mono/Flux를 *같은 형식의 다른 표현*으로 보게 만든다. 그게 함수형이 자바에 가져온 진짜 변화다.

> *책 안에서:* Part II(3·4장), Part III(5·6·7장)에서 본격. 특히 6장의 *fold·monad·composition* 절이 이 동력의 깊이를 보여준다.

### 둘째 동력 — 데이터지향 (Project Amber)

함수형이 자바의 *행위*를 바꿨다면, 데이터지향은 *데이터의 모양*을 바꿨다.

Brian Goetz가 InfoQ에 쓴 *Data-Oriented Programming in Java*는 명시적이다. **데이터는 불변으로, 행위는 분리하라.** 객체지향이 캡슐화로 데이터와 행위를 묶었다면, DOP는 그 반대편을 표현한다. 그리고 그 반대편을 표현하는 도구가 세 개 — records, sealed, pattern matching.

세 도구의 발원지는 *Project Amber*다. 진행은 다음과 같다.

- **Records (JEP 359 preview → 395 standard, Java 14→16)** — *product type*. 컴포넌트의 카르티시안 곱. `final` 클래스, `private final` 필드, 자동 accessor·`equals`·`hashCode`·`toString`, canonical constructor.
- **Sealed Classes (JEP 360 preview → 397 second preview → 409 standard, Java 15→17)** — *sum type*. `sealed interface Expr permits Num, Add, Mul`. 허용된 sub-type의 닫힌 합집합.
- **Pattern Matching for instanceof (JEP 305 preview → 394 standard, Java 14→16)** + **Record Patterns (JEP 405→440, Java 19→21)** + **Pattern Matching for switch (JEP 406→441, Java 17→21)** + **Unnamed Patterns (JEP 443→456, Java 21 preview→22 standard)** — ADT의 분해와 분기.

Records + Sealed = **대수적 데이터 타입(ADT)**. Pattern matching은 그 분해 도구다. Haskell·Scala·OCaml·Kotlin·Rust가 가진 표현력을 자바가 마침내 갖춘 것이다. `instanceof` 캐스트 사다리가 9단까지 늘어난 컨트롤러를 받았을 때의 *끔찍함*을 기억하는가? `if (x instanceof A) { A a = (A)x; ... } else if (x instanceof B) { ... }` 이 사다리가 switch pattern 한 블록으로 정리되는 순간, 그 *후련함*은 한 번 본 사람은 잊지 못한다.

다만 정직하게 짚자. records는 Lombok의 *대체*가 아니다. Brian Goetz의 표현을 빌리자면, Lombok이 "자바가 부족해서 메우는 패치"라면 records는 "자바가 데이터 캐리어를 인정한 신원"이다. *의도가 다르다.* 그래서 JPA Entity로 records를 시도한 신입이 *좌절*하는 일이 생긴다. records는 final + 불변이고, JPA Entity는 mutable + no-args constructor + non-final을 요구한다. 그래서 실무에서 자리 잡은 가이드라인은 단순하다 — **Entity는 클래스(또는 Lombok), DTO·Projection·Command는 records**.

> *책 안에서:* Part VI(11·12·13장)에서 본격. 13장에서 PayBridge의 결제 표현식 평가기를 records·sealed·pattern matching으로 재구성한다.

### 셋째 동력 — 동시성 (Project Loom)

자바의 동시성 모델이 *근본부터* 바뀐 사건이 21에서 일어났다. 그 사건의 이름이 *virtual thread*다.

이걸 이해하려면 잠시 옛 모델을 떠올려야 한다. Java의 전통적 thread는 OS thread = `java.lang.Thread`였다. Linux x64 기준 스택 ~1MB 예약, 컨텍스트 스위치 비용 크고, 수천 개까지가 한계. I/O-bound 웹 애플리케이션은 대부분의 시간을 DB·외부 API 대기에 쓰는데, 그동안 OS thread는 idle인 채 자원만 점유했다. 그래서 Tomcat 200 thread 풀로 한 달을 버틴 끝에 p99가 800ms였다 — *답답한* 일이다. *thread-per-request 모델은 사실상 죽었다*는 게 2010년대 후반의 분위기였다.

대안은 *비동기*였다. `CompletableFuture`의 50개+ 메서드 체인, Reactor의 `Mono`/`Flux`, RxJava의 `Observable`. 그러나 이쪽은 *비싸다*. 콜백·체인 사이에 컨텍스트를 옮기는 게 번거롭고, 스택 트레이스가 산산이 흩어지며, `synchronized`·`ThreadLocal` 같은 옛 도구가 작동을 멈춘다. backpressure를 이해해야 하고, exception 흐름을 따로 설계해야 한다. 새 프로젝트라면 모르되, 30년 묵은 자바 코드를 reactive로 옮기는 일은 *지옥*에 가까웠다.

Project Loom의 답은 우회였다. *OS thread 위에 lightweight thread를 얹자.* `Thread.ofVirtual().start(...)` 또는 `Executors.newVirtualThreadPerTaskExecutor()`로 만드는 **virtual thread**는 JVM이 관리한다. 스택은 heap에 작게 시작해서 필요 시 grow한다. M:N 스케줄링 — 다수 virtual thread가 소수의 carrier(platform) thread에 multiplex. blocking 호출이 들어오면 자동 unmount → 다른 virtual thread가 그 carrier를 점유. 결과적으로 *수백만 개* 생성 가능하다. Brian Goetz의 표현으로는 "virtual memory의 비유" — 물리 메모리보다 큰 환상의 메모리를 주듯, 물리 thread보다 많은 환상의 thread를 주는 것이다.

JEP 425(19 preview) → 436(20 second preview) → **444(21 standard)**. 21이 동시성 모델의 전환점이 된 이유다.

그러나 virtual thread는 *마법*이 아니다. *pinning*이라는 새 함정이 있다. Java 21~23에서는 `synchronized` 블록 내부 I/O가 pinning을 일으켰다 — virtual thread가 unmount 못 하고 carrier thread를 점유한 채 굳어버리는 현상. HikariCP, Caffeine, MySQL Connector/J 같은 라이브러리가 `synchronized` → `ReentrantLock` 이주로 대응했고, Netflix는 production deadlock을 경험했다. *덜컥*한 사건이었다. JDK 24의 JEP 491이 *그 30년 묵은 JVM 모니터 구현*을 손봐서 `synchronized`도 unmount 가능하게 만들었지만, 그 전까지 한국·해외 가릴 것 없이 많은 회사가 VT 도입 첫 분기에 새벽 알람을 받았다.

Loom의 동반자는 두 개 더 있다. **Structured Concurrency** (JEP 453 preview → 533 다섯 번째 preview까지 진행 중) — `StructuredTaskScope`로 자식 task들을 단일 단위로 묶고, 모두 성공/모두 실패/모두 취소를 보장한다. Dijkstra의 structured programming을 *concurrent 코드*에 재해석한 것이다. 그리고 **Scoped Values** (JEP 506 standard, Java 25) — virtual thread가 cheap·short-lived해서 ThreadLocal에 connection·SimpleDateFormat을 캐싱하던 옛 패턴이 *수백만 thread × 수백만 캐시 인스턴스*를 만들 위험이 생겼다. ScopedValue가 그 답이다. 부모/자식 binding, immutable, 자동 cleanup. ThreadLocal 청소를 안 해 메모리가 새던 옛 *찜찜함*을 정리하는 도구다.

한국에서 virtual thread를 production에 본격적으로 도입한 사례는 이미 적지 않다. 우아한형제들이 *Java의 미래, Virtual Thread*라는 제목으로 두 차례 기술 블로그 글을 냈고(techblog.woowahan.com/15398/와 /17163/), 카카오는 제4회 Kakao Tech Meet에서 *JDK 21의 Virtual Thread*를 다뤘으며, 카카오페이는 *Virtual Thread에 봄(Spring)은 왔는가*에서 platform thread → virtual thread 전환의 자원 소모를 실측해서 공개했다(tech.kakaopay.com).

> *책 안에서:* Part IV(8A·8B장)에서 Loom *이전*의 동시성 — JMM, j.u.c, `CompletableFuture`, Flow를 다지고, Part VII(14·15·16장)에서 Loom *이후*를 본격. Spring Boot 3.2의 `spring.threads.virtual.enabled` 한 줄 설정과 그 한 줄 뒤에 숨은 의미가 14·21장에서 만난다.

### 넷째 동력 — 메모리·네이티브·성능 (Project Panama + Project Leyden + GC)

이 동력은 사실 *세 개의 작은 동력*이 한 묶음이 된 것이다. 끝까지 따라가면 결국 "자바를 *빠르게*, *가볍게*, *외부 세계와 잘 통하게* 만든다"는 한 문장으로 수렴한다.

#### Project Panama — 네이티브와 SIMD

JNI의 시대가 끝나고 있다. JNI는 거대한 boilerplate를 요구했다 — `*.h` 작성, header 추출, C 코드, `System.loadLibrary`. GC와 충돌이 잦고, 한 번 native crash가 나면 JVM 전체가 죽었다. *끔찍한* 기억을 가진 자바 개발자가 적지 않다. Project Panama는 그 자리를 메우러 왔다.

- **Foreign Function & Memory API (FFM)** — JEP 412(17 incubator) → 442(21 third preview) → **454(22 standard)**. `Arena`로 lifetime을 관리하고, `MemorySegment`로 명시적·범위 한정된 native memory를 다루며, `Linker`로 함수 시그니처를 method handle로 옮긴다. `jextract`가 C header → Java 바인딩을 자동 생성한다. `try (Arena arena = Arena.ofConfined()) { MemorySegment seg = arena.allocate(100); ... }` — 메모리 해제가 try-with-resources로 자연스럽게 된다.
- **Vector API** — JEP 338(16 first incubator) → 489(24 ninth incubator). 아직 표준화 안 됐다. *Project Valhalla*의 value types를 기다리는 중이다. 표준화되면 AVX2·AVX-512·NEON·SVE에 자동 매핑된다. 행렬 연산, 벡터화 가능한 numeric loop, ML inference를 위한 도구다.

#### Project Leyden — 시작 시간

Java가 클라우드 시대에 받은 가장 큰 *난감함*은 cold start였다. AWS Lambda에 8초짜리 콜드 스타트가 떠서 SLA를 깬 사례, 한국 핀테크에서도 적지 않게 봤다. 옛 답은 GraalVM Native Image 하나뿐이었다 — closed-world 가정, reachability metadata, reflection 제약. 강력하지만 *비싼* 답이었다.

OpenJDK의 답은 다른 방향에서 왔다.

- **AppCDS** (Java 10) — class metadata 캐시.
- **Dynamic CDS Archives** (Java 13) — 단일 run으로 archive 생성.
- **JEP 483 (Java 24)** — Ahead-of-Time **Class Loading & Linking**. class를 init·link해서 캐시. Project Leyden의 첫 가시적 결실이다.
- **JEP 514 / 515 (Java 25)** — AOT CLI ergonomics, AOT method profiling.

Spring Boot 3.3+는 이걸 통합했다. training run으로 AOT cache를 만들고, 다음 실행부터 적용한다. Spring Petclinic 기준 startup 36~42% 단축. Spring AOT(빌드 타임 BeanFactory 사전 계산) + JDK AOT(JVM 캐시)를 조합하면 ~4배 startup 개선이 보고됐다. *GraalVM 없이도 빠른 startup*이 가능해진 것이다.

#### GC의 진화

마지막은 GC다. CMS의 시대(1.4)를 거쳐, G1이 9에서 default가 됐고, ZGC가 11에 실험적으로 들어와 15에서 production-ready가 됐다. Generational ZGC가 21(JEP 439)에서 들어와 23(JEP 474)에서 default가 됐다. Java 25에서는 Generational Shenandoah(JEP 521)가 도착했고, **Compact Object Headers (JEP 519)**가 들어왔다. 64비트 JVM의 모든 객체에 붙던 96~128비트 헤더를 64비트로 압축한 것이다. 작은 객체가 많은 워크로드(캐시, JSON 파싱)에서 heap 사용량 ~10~22% 감소가 보고됐다. 일부 측정에서 CPU 절감 30% 보고도 있다. *Java 8 PermGen OOM*에 시달려본 사람이라면, GC 진화의 11년을 보고 *묘하게 안도하는* 감각을 느낄 것이다.

> *책 안에서:* Part VIII(17·18·19·19A장)에서 본격. 17장에서 GC 선택, 18장에서 FFM, 19장에서 AOT/Leyden, 19A장에서 도구 일습.

### 다섯째 동력 — 도구와 언어 표면의 정리

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

### 한 도메인을 두 번 — Java 8 vs Java 25 미리보기

다섯 동력을 따로따로 보면 추상적이다. 그러니 한 도메인을 두 번 보자. PayBridge의 *주문 처리* 코드를 Java 8 스타일과 Java 25 스타일로 한 페이지씩.

#### Java 8 스타일

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

#### Java 25 스타일

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

### 다섯 동력은 책의 부 구조다

이제 책의 부 구조와 다섯 동력의 대응을 정리하자.

| 동력 | 책의 부 | 대표 챕터 |
|------|---------|----------|
| 함수형 | Part II, Part III | 3·4·5·6·7장 |
| 데이터지향 | Part VI | 11·12·13장 |
| 동시성 | Part IV(Loom 이전), Part VII(Loom 이후) | 8A·8B·14·15·16장 |
| 메모리·네이티브·성능 | Part VIII | 17·18·19·19A장 |
| 도구·언어 표면 | Part V | 9·10장 |

여기에 Part IX(마이그레이션·보안·Spring 시너지, 20·20A·21장), Part X(다음 자바, 22장), 그리고 처음의 Part I(지형도, 1·2장)이 더해진다. 다섯 동력이 책의 척추이고, 마이그레이션·미래·지형도가 그 척추를 둘러싼 *살*이다.

### 마무리 — 22장과의 약속

PayBridge의 11년을 함수형·데이터지향·동시성·성능·도구라는 다섯 갈래로 다시 읽으면, 무작위 사건의 나열이 *한 줄의 이야기*가 된다. Java 8의 람다가 PayBridge의 결제 정산 배치를 함수형 스타일로 옮겼고, Java 17의 records가 DTO를 다듬었으며, Java 21의 virtual thread가 thread-per-request를 부활시켰고, Java 25의 Compact Object Headers가 메모리 ~20%를 돌려줬고, 11년의 도구 진화가 빌드·프로파일링·배포 파이프라인의 모양을 바꿨다. 다섯 동력이 한 회사의 코드베이스 안에서 어떻게 결합되는지가 이 책의 핵심 줄거리다.

그리고 약속 하나. 22장 결말에서 다시 PayBridge로 돌아온다. 그때는 5년 뒤를 상상한다. *Project Valhalla*의 value types가 도착했을 때 records가 어떻게 바뀔지, *Project Amber*의 with-expressions·primitive type patterns이 ADT를 어떻게 더 풍부하게 만들지, *Project Babylon*의 code reflection이 metaprogramming을 어떻게 다시 그릴지, *Project Leyden*의 condensers가 startup을 어디까지 줄일지. 다섯 동력의 *다음 5년*을 PayBridge의 5년 뒤 코드 한 페이지로 함께 그려본다. 1장의 지도, 2장의 다섯 동력, 22장의 미래 — 이 셋이 책의 처음과 끝을 잇는 *수미상관*이다.

자, 다섯 동력의 지도를 손에 쥐었다. 다음 장에서는 첫째 동력의 가장 안쪽으로 들어가보자. 람다 — 그 익숙함의 진짜 의미를. PR 리뷰에서 6중 중첩 람다를 만났을 때의 *난감함*을 한번 들여다보자.

---

# Part II. 함수형 자바의 어휘

람다와 함수형 인터페이스. 11년 자바 진화의 *모든 것*이 사실 이 두 문법에서 시작됐다. 8장에서도, 11장에서도, 14장에서도, 그 뿌리는 Java 8의 람다와 `java.util.function`이다. 그래서 함수형 어휘를 다시 한 번 정확히 다지는 일은 단지 *기초 복습*이 아니다. 그것은 *책 전체의 단어집을 합의하는 일*이다.

3장은 람다를 *익명 클래스의 문법 설탕*으로 보는 통념을 정면으로 마주한다. JSR 335의 스펙, `invokedynamic`과 `LambdaMetafactory`의 내부, 캡처와 `effectively final`의 정확한 정의 — 이 작은 문법 뒤에 얼마나 두꺼운 설계가 깔려 있는지 본다. 메서드 참조 네 가지(static, instance-bound, unbound, constructor) 사이의 미세한 차이도 짚고, `Function`·`Predicate`·`Supplier`·`Consumer`·`BiFunction`의 합성 어휘가 어떻게 한 줄의 표현력을 폭발시키는지 본다.

4장은 종종 잊히는 Java 8의 *보석들*을 다시 꺼낸다. `java.time`(JSR-310)이 `Date`와 `Calendar`를 어떻게 *종결*했는지, `Instant`·`LocalDateTime`·`ZonedDateTime`·`Duration`·`Period`의 모델이 왜 그렇게 설계됐는지. `Stream` 같은 큰 도구에 가려 잘 들여다보지 않던 `Optional.ifPresentOrElse`, `Collectors.teeing`, `Stream.takeWhile/dropWhile`, `Files.readString/writeString`, `String.repeat/strip/lines`도 함께 정리한다. 11년 전에 들어왔지만 아직도 회사 코드베이스 어딘가에서 `Date`와 `SimpleDateFormat`이 살아 있는 이유는 단순하다 — 우리가 아직 *그 보석들을 다 줍지 못했다*.

이 두 장이 책 후반부의 *함수형 어휘*를 모두 깔아준다. Stream(Part III)도, CompletableFuture(8B)도, records의 함수형 합성(Part VI)도, 모두 이 두 장의 어휘 위에서 자란다. 가볍게 훑지 말고 천천히 다시 만나보자.

---

## 3장. 람다와 함수형 인터페이스 — 그 익숙함의 진짜 의미

PR 리뷰에서 이런 코드를 만났다고 상상해보자. 상품 카탈로그를 정렬하는 코드인데, 람다가 여섯 단계로 중첩되어 있다. 바깥의 `Comparator.comparing(...)` 안에서 또 다른 `Function`이 호출되고, 그 안에서 `Predicate.and(...)`가 짜이고, 그 안에서 다시 람다가 `map`을 받아 람다를 반환한다. 코드는 분명 컴파일되고 테스트도 통과한다. 그런데 리뷰어 입장에서는 화면을 한참 들여다봐도 "이 람다의 `this`는 무엇이고, 어느 변수가 캡처됐고, 만약 null이 들어오면 어디서 깨질까"가 한눈에 들어오지 않는다. 난감하다.

람다를 처음 만난 게 2014년 봄이다. 그때 우리는 "익명 클래스를 짧게 적는 문법"이라고 배웠고, 한동안 그렇게 써먹어도 별 탈은 없었다. 그런데 람다는 정말 익명 클래스의 문법 설탕일까? 아니면 그 익숙한 화살표 뒤에 우리가 11년 동안 한 번도 제대로 들여다보지 않은 무엇인가가 숨어 있었던 걸까? 이 장에서 그 안을 한번 열어보자.

### 람다는 익명 클래스의 설탕인가

가장 흔한 오해부터 정리하자. Java 8 출시 직후 많은 입문서는 다음 두 코드가 "동등하다"고 적었다.

```java
// 익명 클래스
Runnable r1 = new Runnable() {
    @Override public void run() { System.out.println("hi"); }
};

// 람다
Runnable r2 = () -> System.out.println("hi");
```

두 코드는 *의미적으로는* 같은 일을 한다. `r1.run()`과 `r2.run()`은 동일한 출력을 낸다. 하지만 *어떻게 같은 일을 하는지*를 들여다보면 둘은 완전히 다른 메커니즘 위에 서 있다.

익명 클래스는 컴파일 시점에 새 `.class` 파일이 하나 더 만들어진다. `Outer$1.class`라는 익숙한 이름의 파일이다. 클래스로더가 그 파일을 읽고, 메모리에 클래스를 올리고, `new`로 인스턴스를 만든다. 람다는 그렇지 않다. 람다 표현식은 `invokedynamic` 바이트코드 한 줄로 컴파일되고, 첫 호출 시점에 `LambdaMetafactory`가 클래스를 *동적으로* 생성해 캐싱한다. 다음 호출부터는 그 캐시된 클래스의 인스턴스를 재사용한다. 다시 말해, 같은 람다를 천 번 호출해도 클래스로딩 비용은 한 번뿐이고, 인스턴스 생성 비용도 거의 들지 않는다.

이게 단순히 성능 최적화 이야기로 들릴 수도 있는데, 더 중요한 함의가 있다. **람다는 클래스가 아니다.** JVM은 람다를 "특정 함수형 인터페이스의 인스턴스를 어떻게 만들지에 대한 늦은 결정"으로 본다. 익명 클래스는 정적이고 람다는 동적이다. 그래서 두 코드의 `this`도, 직렬화 동작도, 디버거에서 보이는 스택프레임도, 전부 다르다.

기억해두자. 람다와 익명 클래스는 *문법 설탕* 관계가 아니라 *서로 다른 메커니즘으로 같은 인터페이스 약속을 이행하는 두 가지 방식*이다. 익숙해 보인다고 같은 것으로 묶지 말자.

#### `this`의 정체

이 차이는 `this` 키워드에서 가장 극적으로 드러난다. 다음 코드를 보자.

```java
class CatalogService {
    private final String name = "main";

    void run() {
        Runnable anon = new Runnable() {
            @Override public void run() { System.out.println(this); }
        };
        Runnable lambda = () -> System.out.println(this);

        anon.run();    // CatalogService$1@... (익명 인스턴스)
        lambda.run();  // CatalogService@... (바깥 인스턴스)
    }
}
```

익명 클래스 안의 `this`는 그 익명 객체 자신이다. 그래서 바깥 필드에 접근하려면 `CatalogService.this.name`처럼 한정자를 붙여야 했다. 람다는 다르다. 람다 안의 `this`는 람다를 *둘러싼 메서드의 `this`*다. 람다는 자신만의 인스턴스 정체성을 갖지 않는다. 바깥의 `name`을 그냥 `name`이라고 적으면 된다.

이건 단지 편의의 문제가 아니다. 람다는 *콜백을 적는 문법*이 아니라 *바깥 컨텍스트를 그대로 들고 다니는 동작 조각*이라는 사실의 직접적 증거다. 우리가 람다를 자연스럽게 쓸 수 있는 이유의 절반은 여기서 온다.

### effectively final — 11년 묵은 오해

람다와 익명 클래스가 공유하는 제약이 하나 있다. 바깥의 지역 변수를 캡처할 때, 그 변수는 *final이거나 effectively final*이어야 한다. Java 7까지는 명시적으로 `final` 키워드를 붙여야 했다. Java 8부터는 키워드 없이도 "다시 대입되지 않는" 변수라면 컴파일러가 알아서 동등하게 취급해준다.

문제는 많은 개발자가 effectively final을 "그냥 컴파일러가 봐주는 편의 기능"으로 가볍게 여긴다는 점이다. 그렇지 않다. JLS의 정의를 직접 보자.

> **JLS §15.27.2 — Lambda Body**
> "Any local variable, formal parameter, or exception parameter used but not declared in a lambda expression must either be declared final or be effectively final, or a compile-time error occurs where the use is attempted."
>
> **JLS §4.12.4 — final Variables**
> "A local variable... is effectively final if it is not declared final but it never occurs as the left-hand operand of an assignment operator... or as the operand of a prefix or postfix increment or decrement operator."

핵심 문장은 "never occurs as the left-hand operand of an assignment"다. 한 번이라도 재대입되면 effectively final이 아니고, 그 변수는 람다 안에서 쓸 수 없다.

왜 이렇게 까다로울까? 자바의 람다는 *값을 캡처*한다. 참조 캡처가 아니라 값 캡처다. 람다가 만들어지는 순간 바깥 변수의 *현재 값*이 람다 객체 안으로 복사된다. 그 뒤로 바깥에서 변수가 바뀌어도 람다 안의 복사본은 옛 값을 그대로 가진다. 이게 멀티스레드 환경에서 람다를 안전하게 쓸 수 있게 해주는 보증이다. 만약 자바가 클로저 변수의 재대입을 허용했다면, 람다는 *어느 시점의 값을 봐야 하는지* 끝없이 헷갈리는 동시성 시한폭탄이 되었을 것이다.

다음 코드는 컴파일되지 않는다.

```java
int total = 0;
products.forEach(p -> total += p.price()); //  total은 effectively final이 아니다
```

이 코드를 처음 본 사람은 거의 예외 없이 *왜 안 되지*라고 짜증을 낸다. 컴파일러가 시키는 대로 `int[] total = {0}`처럼 배열로 우회하기도 한다. 그런데 그 우회는 동작은 하지만 *왜 그런 우회가 필요한지*에 대한 답은 못 된다. 답은 위에 적었다. 람다는 값을 캡처한다. 합계가 필요하다면 합계를 표현할 도구를 따로 써야 한다. 5장에서 다룰 `reduce`나 `Collectors.summingInt`가 그 도구다.

### 함수형 인터페이스 — 다섯 식구를 외우는 일

`java.util.function` 패키지에는 40개가 넘는 인터페이스가 있다. 처음 보는 사람은 그 양에 압도되는데, 실제로 매일 만나게 되는 건 다섯 식구뿐이다.

| 인터페이스 | 시그니처 | 의미 |
|-----------|----------|------|
| `Function<T, R>` | `R apply(T t)` | "T를 받아 R로 변환" |
| `Predicate<T>` | `boolean test(T t)` | "T가 조건을 만족하는가" |
| `Consumer<T>` | `void accept(T t)` | "T를 받아 어떤 동작을 수행" |
| `Supplier<T>` | `T get()` | "인자 없이 T를 만들어 반환" |
| `BiFunction<T, U, R>` | `R apply(T, U)` | "두 개를 받아 하나로 변환" |

여기에 `UnaryOperator<T>`(= `Function<T, T>`)와 `BinaryOperator<T>`(= `BiFunction<T, T, T>`)가 특수 케이스로 얹힌다. 그리고 `int`/`long`/`double` 같은 원시 타입 전용 변종이 박싱 비용을 줄이기 위해 추가로 정의되어 있다 — `IntPredicate`, `ToDoubleFunction`, `LongSupplier` 같은 것들이다.

처음에는 이 다섯만 익혀도 충분하다. 상품 카탈로그 도메인으로 옮겨와 보자.

```java
Function<Product, BigDecimal> price = Product::price;
Predicate<Product> inStock = p -> p.stock() > 0;
Consumer<Product> printName = p -> System.out.println(p.name());
Supplier<Product> empty = () -> new Product("", BigDecimal.ZERO, 0);
BiFunction<Product, BigDecimal, Product> discount =
    (p, rate) -> p.withPrice(p.price().multiply(BigDecimal.ONE.subtract(rate)));
```

다섯 가지 모양 안에 거의 모든 콜백이 들어간다.

#### `@FunctionalInterface`의 진짜 역할

`@FunctionalInterface` 어노테이션을 처음 본 사람은 자주 묻는다. "이거 꼭 붙여야 하나요?" 결론부터 적으면, *기능 동작에는* 필수가 아니다. 추상 메서드 하나만 가진 인터페이스라면 어노테이션이 없어도 람다를 받을 수 있다. 그러면 왜 붙일까?

`@FunctionalInterface`는 *의도의 표명*이자 *컴파일 시점의 안전 장치*다. 누군가 "이 인터페이스에 추상 메서드 하나만 두겠다"는 약속을 어기고 두 번째 추상 메서드를 추가하면, 컴파일러가 즉시 에러를 내준다. 그 안전 장치가 없으면 6개월 뒤 후배가 메서드 하나 더 추가했을 때, 그 인터페이스를 람다로 받던 모든 코드가 *훨씬 멀리 떨어진 호출 지점*에서 의미 불명의 컴파일 에러를 토해낸다. 끔찍한 일이다.

Spring 코드베이스가 이걸 어떻게 쓰는지 살펴보자. `JdbcTemplate.query(...)`가 받는 `RowMapper<T>`는 `@FunctionalInterface`다. 한 메서드 — `mapRow(ResultSet, int)` — 만 추상이다. `WebClient`의 `ExchangeFunction`도 그렇다. Spring 팀이 이 어노테이션을 의도적으로 붙인 이유는, *프레임워크 사용자에게 "이건 람다로 쓰셔도 됩니다"라는 약속*을 코드로 박아 두기 위해서다. 우리가 직접 만드는 콜백 인터페이스에도 이 어노테이션을 붙이는 편이 낫다. 의도가 명시되고, 안전이 확보된다.

#### default 메서드 — 같은 인터페이스에 살이 붙다

여기서 한 가지 짚고 갈 게 있다. 함수형 인터페이스는 *추상 메서드가 하나*여야 한다는 규칙은 변하지 않았다. 그러나 Java 8부터는 인터페이스에 `default` 메서드와 `static` 메서드를 적을 수 있다. 추상 메서드가 아니므로 함수형 인터페이스 자격을 깨지 않는다.

`Function<T, R>`을 한번 보자.

```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);  // 유일한 추상 메서드

    default <V> Function<V, R> compose(Function<? super V, ? extends T> before) { ... }
    default <V> Function<T, V> andThen(Function<? super R, ? extends V> after) { ... }
    static <T> Function<T, T> identity() { ... }
}
```

`compose`와 `andThen`은 default 메서드다. 함수형 인터페이스 약속을 깨지 않으면서도, *모든 `Function` 인스턴스가 합성 기능을 가지게* 만든 우아한 설계다. JDK 라이브러리 진화의 핵심 도구가 바로 이 default 메서드다. 우리가 람다 두 개를 받아 `.andThen()`으로 잇는 코드를 짤 수 있는 이유가 여기 있다.

### 함수 합성 — 람다끼리 잇기

지금부터가 람다의 *진짜 표현력*이 드러나는 자리다. 합성을 모르면 람다는 그냥 "짧게 적는 콜백"에 머문다. 합성을 알면 람다는 *재사용 가능한 도메인 어휘*가 된다.

```java
Function<Product, BigDecimal> price = Product::price;
Function<BigDecimal, BigDecimal> applyVat = p -> p.multiply(new BigDecimal("1.1"));
Function<BigDecimal, String> format = bd -> "₩" + bd.toPlainString();

Function<Product, String> displayPrice = price.andThen(applyVat).andThen(format);

displayPrice.apply(product); // "₩11000"
```

`andThen(g)`은 "이 함수를 먼저 적용하고, 결과에 `g`를 적용하라"는 뜻이다. `compose(g)`는 반대다 — "`g`를 먼저 적용하고, 결과에 이 함수를 적용하라". 두 메서드는 같은 일을 방향만 바꿔서 한다. 한번 합성해보자, 라고 권하고 싶다. 처음에는 어색해도, 도메인 함수 몇 개를 합성으로 잇는 순간 코드의 표현력이 달라진다.

`Predicate`는 더 풍성하다.

```java
Predicate<Product> inStock = p -> p.stock() > 0;
Predicate<Product> affordable = p -> p.price().compareTo(new BigDecimal("50000")) < 0;
Predicate<Product> onSale = p -> p.discount() > 0;

Predicate<Product> recommendable = inStock.and(affordable).or(onSale);
Predicate<Product> notRecommendable = recommendable.negate();
```

`and`, `or`, `negate` 세 default 메서드로 부울 대수가 그대로 코드에 들어온다. 도메인 규칙을 *말로 적은 대로* 읽힌다. 이 표현력 때문에 우리는 `if (p.stock() > 0 && (p.price().compareTo(...) < 0 || p.discount() > 0))` 같은 한 줄짜리 거대한 조건문에서 벗어날 수 있다.

`Consumer`에도 `andThen`이 있다. 여러 부수 효과를 한 줄로 잇고 싶을 때 쓴다.

```java
Consumer<Product> log = p -> logger.info("processing {}", p.id());
Consumer<Product> audit = p -> auditTrail.record(p);
Consumer<Product> process = log.andThen(audit).andThen(this::doProcess);
```

### 메서드 참조 — 람다의 다섯 번째 단축형

람다에 익숙해질수록 다음 패턴이 자주 나온다.

```java
products.stream().map(p -> p.name()).forEach(s -> System.out.println(s));
```

`p -> p.name()`은 그저 *이미 존재하는 메서드를 호출*하는 람다다. 자바는 이런 경우를 위해 메서드 참조 문법 `::`을 제공한다.

```java
products.stream().map(Product::name).forEach(System.out::println);
```

같은 동작이고, 더 짧고, *의도가 더 명확*하다. 메서드 참조는 네 가지 모양이 있다.

| 종류 | 문법 | 예시 |
|------|------|------|
| 정적 메서드 참조 | `ClassName::staticMethod` | `Integer::parseInt` |
| 한정된 인스턴스 메서드 참조 | `instance::method` | `System.out::println` |
| 한정되지 않은 인스턴스 메서드 참조 | `ClassName::instanceMethod` | `Product::name` |
| 생성자 참조 | `ClassName::new` | `ArrayList::new` |

세 번째 — 한정되지 않은 인스턴스 메서드 참조 — 가 가장 헷갈린다. `Product::name`은 "어떤 `Product` 인스턴스를 받아서 그 인스턴스의 `name()`을 호출하라"는 뜻이다. 즉 `Function<Product, String>`이다. 첫 인자가 *암묵적인 수신자*가 된다. 처음에는 찜찜하게 느껴지는데, 익숙해지면 `p -> p.name()`보다 훨씬 깔끔하다.

생성자 참조도 강력하다. `ArrayList::new`는 `Supplier<ArrayList>`고, `ArrayList::new`가 `int`를 받는 자리에 있으면 `IntFunction<ArrayList>`다. 컴파일러가 target type에 맞춰 알아서 골라준다.

```java
List<String> names = products.stream()
    .map(Product::name)
    .collect(Collectors.toCollection(LinkedList::new));
```

### 함정들 — 람다가 우리를 배신하는 자리

람다가 우아하다고 해서 모든 코드를 람다로 옮기면 안 된다. 11년을 써온 입장에서 자주 데이는 함정 몇 가지를 짚어두자.

**첫째, 캡처 비용.** 람다가 바깥 변수를 캡처하면, 그 람다는 더 이상 stateless가 아니다. JVM은 같은 람다를 호출할 때마다 *캡처값을 들고 있는 새 인스턴스*를 만든다. 캡처가 없는 람다는 싱글톤처럼 재사용되지만, 캡처가 있으면 그렇지 않다. tight loop 안에서 캡처 람다를 매번 새로 만드는 코드는 *조용히* GC 압력을 만든다.

**둘째, `null` 처리.** `Function<T, R>`이 `null`을 반환하면 그다음 `.andThen(...)` 단계로 그대로 흘러간다. Stream의 `.map(...).filter(...)` 체인 한가운데서 NPE가 터지면 스택 트레이스만 보고 어느 람다가 범인인지 알기 어렵다. JEP 358의 Helpful NPE가 Java 14부터 도와주긴 하지만, 람다 안에서는 여전히 추적이 까다롭다. null이 흘러갈 수 있는 자리에는 7장에서 다룰 `Optional`이나 명시적 가드를 두는 편이 낫다.

**셋째, 직렬화.** 람다는 기본적으로 직렬화되지 않는다. `Serializable`을 캐스트로 강제할 수는 있지만, 그 길로 가면 람다의 *동적 생성* 특성과 직렬화의 *정적 형태* 사이에서 끝없이 깨진다. Redis 캐시에 람다를 넣으려는 시도는 처음부터 포기하자.

**넷째, 디버깅.** 람다에 중단점(breakpoint)을 거는 일은 IDE가 많이 도와주긴 하지만, 익명 클래스만큼 직관적이지는 않다. 6중 중첩 람다의 4번째 단계에서 NPE가 나면, 람다 표현식을 명명된 메서드 참조나 `private` 메서드로 *풀어두는* 것이 디버깅 친화적이다. 람다는 짧을 때 가장 빛난다. 길어지면 *다시 메서드로 풀자*.

**다섯째, this 캡처와 메모리 누수.** 람다 안에서 `this`를 쓰면 바깥 인스턴스 전체가 캡처된다. UI 컴포넌트의 콜백, 이벤트 리스너 등에서 이게 누수의 원흉이 된다. 짧은 수명의 객체를 만들고 콜백을 길게 등록할 때는 람다 캡처 범위를 한 번 점검하자.

### Java 8과 Java 21 — 같은 람다, 다른 어휘

같은 일을 하는 코드를 두 시대에 적어 보자. 상품 카탈로그에서 재고가 있고 가격이 5만 원 미만인 상품의 이름 목록을 추출한다.

**Java 8 (2014)**

```java
List<String> result = new ArrayList<>();
for (Product p : products) {
    if (p.getStock() > 0 && p.getPrice().compareTo(new BigDecimal("50000")) < 0) {
        result.add(p.getName());
    }
}
Collections.sort(result);
```

**Java 21 (2023)**

```java
List<String> result = products.stream()
    .filter(inStock.and(affordable))
    .map(Product::name)
    .sorted()
    .toList();
```

람다와 함수형 인터페이스 덕분에 *무엇을 하는지*가 코드 자체로 읽힌다. 정렬 비교자도 마찬가지다.

```java
// Java 8 이전
Collections.sort(products, new Comparator<Product>() {
    @Override public int compare(Product a, Product b) {
        int cmp = a.getCategory().compareTo(b.getCategory());
        return cmp != 0 ? cmp : a.getName().compareTo(b.getName());
    }
});

// Java 8 이후
products.sort(comparing(Product::category).thenComparing(Product::name));
```

`Comparator.comparing(...).thenComparing(...)`은 default 메서드 합성의 가장 아름다운 예시 중 하나다. 도메인을 *말한 대로* 적게 해준다.

### Spring의 자리 — 프레임워크가 람다를 어떻게 받아들였나

Spring Framework 4.x와 Spring Boot 1.x는 Java 8과 거의 동시에 출시됐다. 그때부터 Spring 코드베이스는 람다를 적극 받아들였다. 몇 가지 대표 사례를 살펴보자.

`JdbcTemplate`의 `RowMapper`는 람다 친화적이다.

```java
List<Product> products = jdbcTemplate.query(
    "SELECT id, name, price FROM products WHERE category = ?",
    (rs, rowNum) -> new Product(rs.getLong("id"), rs.getString("name"), rs.getBigDecimal("price")),
    "electronics"
);
```

`RestTemplate`/`WebClient`의 콜백도 람다다. `WebClient.exchangeToMono(response -> ...)`, `RestClient`의 `onStatus(status -> status.is4xxClientError(), (req, res) -> ...)` 같은 패턴이 그대로 람다로 표현된다.

Spring의 `@Bean`으로 등록되는 함수형 빈도 람다로 정의된다.

```java
@Bean
public Function<OrderRequest, OrderResponse> orderProcessor(OrderService service) {
    return request -> service.process(request);
}
```

이 패턴은 Spring Cloud Function에서 더욱 빛난다. 한 람다가 AWS Lambda, Azure Functions, Spring Boot 컨트롤러 모두에서 *같은 함수*로 동작한다. 람다라는 언어 기능이 분산 시스템 아키텍처의 *배포 단위*가 된 셈이다.

람다가 단지 "짧게 적는 콜백"이 아니라 *Spring 같은 거대 프레임워크의 진화 방향을 바꿔놓은 도구*였다는 점을 기억해두자.

### 마무리

람다는 11년이 지난 지금도 여전히 *완전히 이해됐다*고 말하기 어려운 기능이다. 화살표 문법만 익히고 11년을 써온 우리에게, 이 장은 그 익숙함의 뒷면을 한 번 들여다보는 자리였다.

정리하자면 람다는 익명 클래스의 설탕이 아니라, `invokedynamic`과 `LambdaMetafactory`가 뒷받침하는 *완전히 다른 메커니즘*이다. effectively final은 컴파일러의 친절이 아니라 값 캡처라는 설계 결정의 직접적 결과다. `@FunctionalInterface`는 의도 표명이고, default 메서드는 라이브러리 진화의 열쇠다. 메서드 참조는 람다의 다섯 번째 단축형이고, 함수 합성은 도메인 어휘를 만드는 도구다.

다음 4장에서는 람다와 함께 Java 8이 가져온 또 다른 *조용한 혁명*을 살펴보자. 우리가 `java.util.Date`와 `Calendar`에서 정말로 벗어났는지, `java.time`이 그동안 풀어낸 문제가 정확히 무엇인지 — 결제 정산이 시간대 때문에 새벽에 깨졌던 그날을 떠올리며 함께 들여다보자.

---

## 4장. `java.time`과 종종 잊히는 Java 8의 보석들

결제 정산 시스템이 새벽에 깨졌다고 해보자. 한국 시간 자정에 마감되는 일일 정산 배치가 미국 동부의 결제 게이트웨이에서 받은 거래 시각을 잘못 해석한 탓이었다. 거래 시각은 `2026-05-04T22:30:00`이라는 *시간대 정보 없는 문자열*로 넘어왔고, 우리 코드는 그걸 한국 시간으로 가정해 처리했다. 실제로는 미국 동부 시간 — UTC-4 — 의 22:30이었으니, UTC로는 다음 날 02:30, 한국 시간으로는 같은 날 11:30이었다. 정산일이 하루씩 어긋났고, 그 차이만큼의 거래가 *어제와 오늘의 경계*에서 사라졌다.

이런 버그를 겪고 새벽에 깨본 사람이라면 안다. 시간대 처리는 *틀리면 조용히 틀린다*. 컴파일도 되고 단위 테스트도 통과하는데, 한 달 뒤 정산 보고서에서 5만 원짜리 거래 한 건이 두 번 잡혀 있거나 아예 빠져 있는 식이다. 끔찍한 일이다.

그래서 묻자. 우리는 정말 `java.util.Date`와 `Calendar`에서 벗어났을까? Java 8이 `java.time`을 들고 온 지 11년이 됐는데, 사내 코드베이스 어디엔가는 여전히 `new Date()`와 `Calendar.getInstance()`가 살아 있지 않을까. 그리고 더 중요하게, *벗어났다고 믿고 있는 우리*가 `java.time`을 정말 제대로 쓰고 있을까. 한번 들여다보자.

### `Date`와 `Calendar`의 *끔찍했던* 결함들

먼저 우리가 어디에서 출발했는지를 기억하자. Java 1.0의 `java.util.Date`는 *디자인의 거의 모든 차원에서* 실패한 클래스다. 그 결함을 하나씩 짚어두자.

**첫째, 의미의 혼란.** `Date`라는 이름이 무색하게도, 이 클래스는 *날짜*가 아니다. UTC 기준 epoch 밀리초를 담는 *시각(instant)*이다. "오늘이 며칠인가"를 표현하고 싶으면 다른 도구가 필요한데, JDK는 그걸 주지 않았다.

**둘째, mutable.** `Date`의 `setTime()`, `setYear()`, `setMonth()` 같은 메서드가 객체 내부 상태를 바꾼다. 한 `Date` 인스턴스를 여러 곳에서 공유하는 코드는 *어디에서 변형이 일어났는지* 추적하기가 사실상 불가능했다. 그래서 모든 getter가 *방어적 복사*를 해야 했고, 그 비용과 보일러플레이트는 11년 내내 자바 개발자의 *지긋지긋한* 동반자였다.

**셋째, thread-unsafe.** `SimpleDateFormat`이 가장 악명 높았다. 멀티스레드 환경에서 같은 포매터 인스턴스를 공유하면 *조용히 잘못된 문자열*을 뱉었다. 첫 번째 호출은 멀쩡한데 두 번째에서 갑자기 깨지는 식이라, 재현이 어렵고 디버깅이 끔찍했다.

**넷째, 0-based month.** `Calendar.set(2026, 4, 4)`가 5월 4일을 만든다. 4월이 아니다. C 언어의 `tm` 구조체에서 가져온 이 *유물*이 자바 1.0에 그대로 박혀 들어왔고, 11년 동안 수많은 off-by-one 버그를 양산했다.

**다섯째, `Calendar`의 거대함.** `Calendar`는 *모든 달력 시스템을 추상화*한다는 야심으로 만들어졌는데, 실제로는 그레고리력만 제대로 동작했고, API는 거대한 비밀번호 자판 같았다 — `add()`, `roll()`, `set()`, `get()` 사이의 차이를 직관으로 짐작할 수 없었다.

**여섯째, `TimeZone`과의 어색한 결합.** 시간대는 `Date`에 묶이지 않고 별도 `TimeZone` 객체를 통해 *간접적으로* 표현됐다. 같은 epoch 값을 가진 두 `Date`가 같은 시각인지 다른 시각인지는 코드 작성자만 알았다.

이 결함들 때문에 자바 개발자들은 *오랫동안 외부 라이브러리*에 의존했다. 그 이름이 **Joda-Time**이다.

### Joda-Time과 Stephen Colebourne의 유산

Joda-Time은 2002년부터 Stephen Colebourne이 만들고 발전시킨 시간 라이브러리다. 자바 1.0이 못한 일들을 하나씩 풀어냈다 — immutable 객체, 명확한 의미 분리(`LocalDate` vs `LocalDateTime` vs `DateTime`), thread-safe 포매터, 1-based month. 2010년대 초중반의 거의 모든 자바 프로젝트가 Joda-Time을 의존성에 추가했다.

흥미로운 점은 JDK가 결국 *Joda-Time의 저자에게 직접 표준 시간 API를 그려달라고 의뢰*했다는 사실이다. JSR-310은 Stephen Colebourne이 주도한 JEP이고, Java 8의 `java.time`은 사실상 *Joda-Time의 교훈을 흡수한 차세대*다. 단지 베끼지 않았다. Colebourne 본인도 Joda-Time에서 잘못 설계했다고 판단한 부분들 — 예를 들어 `DateTime`이라는 단일 클래스로 너무 많은 의미를 묶었던 점 — 을 새 API에서 *분리*했다. 그래서 `java.time`은 클래스가 많아 보이지만, 그 많음이 *의미의 명확함*에서 나온다.

기억해두자. `java.time`을 깊이 이해하려면 그것이 *Joda-Time의 후예*라는 사실을 알고 시작하는 편이 낫다. 두 라이브러리는 메서드명이 비슷한데 *의미가 다른 자리*가 꽤 있기 때문이다 — `getMonthOfYear()` vs `getMonthValue()`, `plusDays()` 동작의 미묘한 차이 같은 것들 말이다.

### 일곱 가지 시간 — `java.time`의 어휘

`java.time`이 처음에 거대해 보이는 이유는 시간을 *일곱 가지 다른 의미*로 나눠 표현하기 때문이다. 일단 이름을 외우고, 의미를 한 줄씩 붙여보자.

| 클래스 | 의미 | 시간대 정보 |
|--------|------|------------|
| `LocalDate` | "2026년 5월 4일" — 날짜만 | 없음 |
| `LocalTime` | "오후 11시 30분" — 시각만 | 없음 |
| `LocalDateTime` | "2026년 5월 4일 오후 11시 30분" | 없음 |
| `ZonedDateTime` | 위 + "Asia/Seoul" 시간대 | 있음 (지역) |
| `OffsetDateTime` | 위 + "+09:00" 오프셋 | 있음 (오프셋만) |
| `Instant` | UTC 기준 epoch 시각 | 항상 UTC |
| `Year`, `YearMonth`, `MonthDay` | 부분 정보 | 없음 |

이 표를 외우는 일은 *시간대 버그를 줄이는 첫걸음*이다. 각 클래스가 무엇을 표현하는지 *그리고 무엇을 표현하지 않는지*를 알면, "이 값에 시간대를 붙여야 하나 말아야 하나"가 코드 작성 시점에 결정된다.

가장 중요한 구분이 `LocalDateTime`과 `ZonedDateTime`의 차이다. `LocalDateTime`은 *시간대 정보가 없다*. "2026-05-04T23:30:00"이라는 정보만 있고, 이게 한국 시간인지 미국 시간인지 알 수 없다. 머리말의 정산 버그가 정확히 이 자리에서 터졌다. 외부 시스템에서 시각 정보를 받을 때, 그것이 `LocalDateTime`으로 표현되어 있다면 *시간대를 누가 어디서 결정하는지*를 반드시 짚어야 한다.

`Instant`는 정반대다. 시간대 따위가 없고, 그냥 *epoch 이후 몇 나노초가 지났는가*만 담는다. 기계 친화적이고, 데이터베이스 저장과 로그 기록과 분산 시스템 메시지에 적합하다. *기계가 읽는 시각은 `Instant`로, 사람이 읽는 시각은 `ZonedDateTime`으로* — 이 원칙을 한 줄로 외워두면 절반은 안전하다.

```java
// 1. 사람이 입력한 시각 — 시간대 명시
ZonedDateTime userTime = ZonedDateTime.of(2026, 5, 4, 23, 30, 0, 0, ZoneId.of("Asia/Seoul"));

// 2. UTC로 변환해 저장
Instant utc = userTime.toInstant();

// 3. 다시 사람에게 보여줄 때 — 다른 시간대로 표시
ZonedDateTime forUS = utc.atZone(ZoneId.of("America/New_York"));
```

이 세 단계를 *어디에서나 같은 패턴으로* 적용하면, 정산 버그의 절반은 사라진다.

### `Duration`과 `Period` — 시간의 두 가지 *기간*

자주 헷갈리는 두 클래스가 있다. `Duration`과 `Period`다. 둘 다 *기간*을 표현하는데, 의미가 다르다.

`Duration`은 *기계적 시간*이다. "5초", "3시간 27분"처럼 *정확한 양*을 담는다. 내부적으로 초와 나노초로 표현된다.

`Period`는 *달력 시간*이다. "1개월", "2년 3개월"처럼 *달력 단위*를 담는다. 1개월은 28일일 수도, 31일일 수도 있다.

이 차이가 왜 중요한가. *서머타임이 있는 자리*에서 둘이 다르게 동작하기 때문이다. 미국 동부에서 3월 둘째 주 일요일에 서머타임이 시작되면, 그날의 *달력상 24시간*은 *실제로는 23시간*이다. `Period.ofDays(1)`을 더하면 같은 시각이 되고, `Duration.ofHours(24)`를 더하면 한 시간 어긋난 시각이 된다.

```java
ZonedDateTime before = ZonedDateTime.of(2026, 3, 7, 12, 0, 0, 0, ZoneId.of("America/New_York"));
ZonedDateTime byPeriod = before.plus(Period.ofDays(1));        // 2026-03-08T12:00 (정상)
ZonedDateTime byDuration = before.plus(Duration.ofHours(24));  // 2026-03-08T13:00 (한 시간 어긋남)
```

기억해두자. *달력 의미가 중요한 곳*에는 `Period`, *기계적 시간 간격이 중요한 곳*에는 `Duration`. 멱등성 토큰의 만료, 캐시 TTL, 락 보유 시간 같은 자리는 `Duration`이다. 청구서 발행 주기, 구독 만료일 같은 자리는 `Period`다.

### `ChronoUnit`과 `TemporalAdjusters`

`ChronoUnit`은 시간 단위의 열거형이다. `ChronoUnit.DAYS`, `ChronoUnit.MINUTES`, `ChronoUnit.HALF_DAYS` 같은 식이다. 두 시각 사이의 거리를 계산할 때 유용하다.

```java
long days = ChronoUnit.DAYS.between(start, end);
long minutes = ChronoUnit.MINUTES.between(start, end);
```

`TemporalAdjusters`는 *시각을 어떤 규칙에 맞춰 옮기는* 도구다. "이번 달의 마지막 영업일", "다음 월요일", "이번 분기의 첫 날" 같은 도메인 규칙을 *함수형으로* 표현한다.

```java
LocalDate lastDayOfMonth = LocalDate.now().with(TemporalAdjusters.lastDayOfMonth());
LocalDate nextMonday = LocalDate.now().with(TemporalAdjusters.next(DayOfWeek.MONDAY));
```

3장에서 다룬 함수형 인터페이스의 자취가 여기서도 보인다 — `TemporalAdjuster` 자체가 `@FunctionalInterface`다. 사용자 정의 조정자도 람다로 짤 수 있다.

```java
TemporalAdjuster nextWorkday = temporal -> {
    DayOfWeek day = DayOfWeek.of(temporal.get(ChronoField.DAY_OF_WEEK));
    int daysToAdd = switch (day) {
        case FRIDAY -> 3;
        case SATURDAY -> 2;
        default -> 1;
    };
    return temporal.plus(daysToAdd, ChronoUnit.DAYS);
};

LocalDate nextBusinessDay = LocalDate.now().with(nextWorkday);
```

### 시간대 — `ZoneId`와 DST

`ZoneId`는 "Asia/Seoul", "America/New_York" 같은 *지역 식별자*를 담는다. 단순 오프셋(`+09:00`)이 아니라 *DST 규칙을 포함한 지역의 시간 운영 정책 전체*를 가리킨다. 한국은 DST가 없어서 항상 UTC+9지만, 미국은 봄·가을마다 한 시간씩 움직인다.

운영에서 가장 자주 데이는 자리가 *서버 기본 시간대 가정*이다. 같은 코드가 개발자 노트북에서는 잘 돌다가 UTC로 설정된 운영 컨테이너에서 다른 결과를 낸다. 그래서 권장은 단순하다.

**서버는 UTC, 입출력에서만 변환한다.**

```java
// 컨테이너 시작 시
TZ=UTC

// 사용자에게 보일 때만 변환
ZonedDateTime displayTime = instant.atZone(userZoneId);
```

이 한 줄짜리 운영 규칙이 *시간대 버그의 60%를 막아준다*고 봐도 좋다.

### 포매팅 — `DateTimeFormatter`

`SimpleDateFormat`이 thread-unsafe였던 *그 끔찍한 시절*은 끝났다. `DateTimeFormatter`는 *immutable이고 thread-safe*다. 마음껏 static 필드로 공유해도 된다.

```java
public class TimeFormats {
    public static final DateTimeFormatter ISO = DateTimeFormatter.ISO_OFFSET_DATE_TIME;
    public static final DateTimeFormatter KOREAN = DateTimeFormatter.ofPattern("yyyy년 M월 d일 HH시 mm분");
    public static final DateTimeFormatter LOG_TS = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSSXXX");
}
```

ISO-8601 표준 포맷은 *직접 만들지 말고* `DateTimeFormatter.ISO_*` 상수들을 쓰는 편이 낫다. `ISO_INSTANT`, `ISO_LOCAL_DATE`, `ISO_OFFSET_DATE_TIME` 등이 미리 정의되어 있다.

파싱할 때 한 가지 주의점. `LocalDateTime.parse()`는 *입력 문자열에 시간대 정보가 있어도 버린다*. 시간대를 살리고 싶으면 `ZonedDateTime.parse()`나 `OffsetDateTime.parse()`를 써야 한다. 머리말의 정산 버그가 사실 이 자리와도 관련이 있다.

### JSON·JPA 직렬화 — 라이브러리와의 만남

`java.time`을 도입할 때 가장 자주 막히는 자리가 직렬화다. Jackson과 JPA 둘 다 *기본 설정에서는* `java.time`을 곱게 다뤄주지 않는다. 짚어두자.

**Jackson + java.time.** `jackson-datatype-jsr310` 모듈이 필요하다. Spring Boot 2 이후로는 자동 설정되지만, 두 가지 옵션을 명시하는 편이 낫다.

```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());
mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);  // ISO 문자열로
mapper.setTimeZone(TimeZone.getTimeZone("UTC"));
```

`WRITE_DATES_AS_TIMESTAMPS`를 끄지 않으면 `Instant`가 *epoch 초의 숫자*로 직렬화된다. API 응답에서는 거의 항상 ISO-8601 문자열이 낫다.

**JPA + java.time.** Hibernate 6부터는 `LocalDate`, `LocalDateTime`, `Instant`, `ZonedDateTime`을 *기본 지원*한다. 이전 버전에서는 `AttributeConverter`를 직접 짜야 했다.

```java
@Converter(autoApply = true)
public class InstantConverter implements AttributeConverter<Instant, Timestamp> {
    @Override public Timestamp convertToDatabaseColumn(Instant attribute) {
        return attribute == null ? null : Timestamp.from(attribute);
    }
    @Override public Instant convertToEntityAttribute(Timestamp dbData) {
        return dbData == null ? null : dbData.toInstant();
    }
}
```

`autoApply = true`로 두면 해당 타입을 가진 모든 Entity 필드에 자동 적용된다.

운영에서 한 가지 권장. *Entity의 시각 필드는 가급적 `Instant`로 통일*하는 편이 낫다. `LocalDateTime`을 Entity에 두면 시간대 책임이 *코드 어딘가에 분산*된다. `Instant`로 통일하면 DB에는 UTC, 응답 직렬화 시점에 사용자 시간대로 변환 — 흐름이 단순해진다.

### Kafka·로그 — 메시지 타임스탬프의 자리

Kafka의 `ProducerRecord`에는 `timestamp` 필드가 있다. 이 값은 *epoch 밀리초의 `long`*이다. `Instant.toEpochMilli()`로 채우는 편이 일관성 있다. Kafka Streams의 `WindowedBy` 윈도잉도 `Duration`을 받는다.

```java
KStream<String, Event> stream = ...;
stream.groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .aggregate(...)
```

로그 타임스탬프는 *반드시 ISO-8601 with offset*으로 적는 편이 낫다. `2026-05-04T14:30:00.123+09:00` 같은 형식이다. Logback의 `%date{ISO8601}` 패턴이 이 형식을 지원한다. 시간대 정보 없는 타임스탬프는 *멀티 리전 운영에서 추적을 끔찍하게 만든다*.

### Spring 맥락 — `@DateTimeFormat`과 친구들

Spring MVC는 `@DateTimeFormat`으로 *컨트롤러 파라미터의 파싱 형식*을 지정한다.

```java
@GetMapping("/orders")
public List<Order> orders(
    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate from,
    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate to
) { ... }
```

`?from=2026-05-01&to=2026-05-31` 같은 쿼리 파라미터가 자동으로 `LocalDate`로 바인딩된다. 만약 시각까지 받고 싶으면 `ISO.DATE_TIME`을 쓴다.

Spring Boot의 properties에서도 `Duration`이 자연스럽다.

```yaml
app:
  cache-ttl: 30m
  request-timeout: 5s
  retention-period: 7d
```

```java
@ConfigurationProperties("app")
public record AppProperties(Duration cacheTtl, Duration requestTimeout, Duration retentionPeriod) {}
```

문자열 `"30m"`이 자동으로 `Duration.ofMinutes(30)`으로 파싱된다. `30s`, `1h`, `7d` 등이 모두 지원된다. Boot 2.3 이후로는 `Period`도 같은 방식으로 받는다 — `1y`, `3M`, `14d` 같은 식이다.

### 마이그레이션 — `Date`/`Calendar`에서 옮겨오기

레거시 코드를 *살려 둔 채로* 점진 마이그레이션하는 패턴을 정리해두자.

**1단계 — 경계에서 변환.** 외부 라이브러리(JDBC, 오래된 SDK)가 `Date`를 반환하면, *받자마자* `Instant`로 변환한다.

```java
Date legacy = stmt.executeQuery().getDate(1);
Instant modern = legacy.toInstant();
```

반대로 외부에 `Date`를 줘야 하면, *나갈 때만* 변환한다.

```java
Date toLegacy = Date.from(instant);
```

**2단계 — 도메인 클래스의 시각 필드 교체.** Entity·DTO·Value Object의 `Date`/`Calendar` 필드를 차례로 `Instant`/`LocalDate`로 바꾼다. JPA `AttributeConverter`로 DB 컬럼은 그대로 둘 수 있어서 *마이그레이션을 점진적으로* 끌고 갈 수 있다.

**3단계 — `SimpleDateFormat` 추방.** 코드베이스 전체에서 `SimpleDateFormat`을 grep으로 찾아 `DateTimeFormatter`로 옮긴다. 단위 테스트가 *멀티스레드에서 잘 도는지*를 함께 확인하는 편이 낫다.

**4단계 — `Calendar` 산수 추방.** `cal.add(Calendar.DAY_OF_MONTH, 7)` 같은 코드를 `date.plusDays(7)`로 바꾼다. 가독성이 즉시 좋아진다.

**5단계 — 시간대 가정 점검.** 마지막 단계가 가장 어렵다. 코드베이스 전체에서 *시간대를 어디서 어떻게 가정*하고 있는지를 한 번 훑는다. 머리말의 정산 버그가 여기서 잡힌다.

### 한국 시간대 운영의 미세한 함정들

한국은 *DST가 없어서* 시간대 운영이 비교적 단순하다. 그래도 몇 가지는 짚어둘 만하다.

**Asia/Seoul vs +09:00.** 둘 다 *현재로서는* 같은 결과를 낸다. 그러나 `ZoneId.of("Asia/Seoul")`은 *지역 시간대 데이터베이스*를 가리킨다 — 만약 한국이 DST를 도입하기로 결정하면(역사적으로 1948년, 1949년, 1987~88년에 짧게 시행한 적이 있다) `Asia/Seoul`은 자동으로 적응한다. `+09:00`은 고정 오프셋이라 그렇지 않다. *지역 운영* 관점에서는 `ZoneId.of("Asia/Seoul")`을 쓰는 편이 미래 대비에 낫다.

**`tzdata` 업데이트.** JDK는 IANA의 `tzdata`를 내장하고 있다. 이 데이터는 *세계 어디선가* 시간대 규칙이 바뀔 때마다 갱신된다. JDK 마이너 버전 업데이트에서 `tzdata`가 함께 갱신되니, 운영 환경의 JDK를 *너무 오래 안 올리면* 외국 거래 처리에서 미세한 어긋남이 발생할 수 있다.

**Excel·CSV 시간대.** 한국 사용자가 익숙한 Excel은 시간대 개념이 없다. CSV로 시각을 주고받을 때, *어떤 시간대 기준의 시각인지*를 컬럼 이름이나 별도 컬럼으로 명시하자. 그냥 `"2026-05-04 14:30"`이라고만 적으면 받는 쪽이 *알아서 추측*하게 된다 — 추측은 틀린다.

### 종종 잊히는 Java 8의 보석들

`java.time`만큼 화려하진 않지만 *조용히 도움 되는* Java 8 추가 기능들을 잠깐 살펴보자. Map에 추가된 네 가지 메서드가 그중 백미다.

```java
// getOrDefault — null 체크 없이 기본값
String name = userIdToName.getOrDefault(userId, "anonymous");

// computeIfAbsent — 캐시 패턴의 정석
Map<String, List<Product>> byCategory = new HashMap<>();
products.forEach(p -> byCategory.computeIfAbsent(p.category(), k -> new ArrayList<>()).add(p));

// merge — 카운터·합계 누적
Map<String, Integer> counts = new HashMap<>();
words.forEach(w -> counts.merge(w, 1, Integer::sum));

// replaceAll — 전체 값 변환
prices.replaceAll((k, v) -> v.multiply(new BigDecimal("1.1")));
```

특히 `computeIfAbsent`는 *그동안 우리가 적어왔던* 6줄짜리 *putIfAbsent + get* 패턴을 한 줄로 줄여준다. `merge`는 카운팅·합계 누적 코드의 보일러플레이트를 거의 없앤다. 한번 써보면 `containsKey` 검사로 분기하던 옛 코드가 새삼 *번거롭게* 느껴진다.

`Optional`도 Java 8의 보석이지만, 그건 7장에서 따로 다룬다. 여기서는 한 가지만 짚자 — `Map.get()`의 결과를 *`Optional.ofNullable`로 감싸는 습관*은 좋은 출발이지만, 그게 정말 어디까지 가야 하는지는 7장에서 깊이 보자.

### 마무리

`java.time`은 Java 8의 *가장 조용하지만 가장 깊은* 변화다. 람다나 Stream만큼 화려하지 않아서 적게 언급되지만, 이 라이브러리가 11년 동안 막아낸 *시간대 버그의 양*은 측정하기 어려울 만큼 많다. 그리고 동시에, 우리가 *제대로 쓰지 못해 여전히 만들고 있는 시간대 버그*도 적지 않다.

정리하자면 시각의 의미를 일곱 가지로 *분리해서* 외우자. 기계 시각은 `Instant`, 사람 시각은 `ZonedDateTime`. 기간은 달력이면 `Period`, 기계면 `Duration`. 서버는 UTC로 돌리고 입출력에서만 변환하자. `SimpleDateFormat`은 다시 보지 말자. JPA Entity의 시각 필드는 `Instant`로 통일하는 편이 낫고, Hibernate 6 이후로는 변환자도 필요 없다.

다음 5장에서는 람다와 함수형 인터페이스가 *컬렉션 처리*와 만나서 생긴 변화 — Stream API — 를 들여다보자. 동료가 무심코 던진 `stream.parallel()` 한 줄이 운영을 어떻게 흔들 수 있는지, 그리고 그걸 막으려면 무엇을 알아야 하는지를 함께 살펴보자.

---

# Part III. 스트림과 Optional의 모든 것

Stream API는 자바가 11년 동안 *가장 오래 다듬어온 도구*다. Java 8에 처음 들어와 매 릴리스마다 메서드가 추가됐고, Java 22에서 Gatherers라는 새 중간 정거장을 얻었으며, Java 25에서도 여전히 다듬어지고 있다. 그 도구를 *깊이* 이해하는 일은 곧 11년 자바의 함수형 사고를 이해하는 일이다.

Part III의 세 장은 Stream의 표면에서 심부까지 단계적으로 내려간다. 5장은 Stream의 *해부도*다. lazy evaluation과 short-circuiting의 실제 동작, `Spliterator`의 분할 정책, parallel stream의 `ForkJoinPool.commonPool()` 함정 — 표면의 한 줄 뒤에 무엇이 동작하는지 본다. 6장은 종착(Collector)과 새 중간 정거장(Gatherer)이다. `Collectors.toMap`의 1,000번째 호출과 `Stream.collect(toList())`의 미세한 차이부터, `Gatherer`가 fold의 일반화로서 슬라이딩 윈도우와 stateful 변환을 어떻게 *마침내* 자연스럽게 표현하게 됐는지까지 본다. 7장은 `Optional<T>`다. `Optional<List<T>>`라는 그 *당혹스러운* 시그니처를 어떻게 피하는지, monad의 색채가 자바에 어떻게 스며들었는지, 그리고 `Optional`을 잘못 써서 오히려 코드를 *더 찜찜하게* 만든 사례들을 정직하게 본다.

이 셋이 묶여 *함수형 데이터 파이프라인*이라는 한 도구가 완성된다. 5·6·7장의 어휘는 Part VI(데이터지향)와 Part VII(Loom 시대)에서 다시 쓰인다 — records를 Gatherer로 모으고, Optional을 virtual thread 안에서 흘리는 코드가 그 뒤에 나온다. 함수형 사고의 *정점*을 함께 올라가보자.

---

## 5장. Stream API — 선언적 데이터 파이프라인의 해부

팀 리뷰에서 동료가 `orders.parallelStream().filter(...).collect(toList())`라는 한 줄을 무심코 던졌다고 해보자. 누구도 그 한 줄을 깊이 들여다보지 않는다. 리뷰는 통과되고, 그 코드는 다음 날 운영에 올라간다. 그리고 한 달쯤 뒤 어느 한가한 평일 오후, 결제 서비스의 p99가 갑자기 800ms를 넘기 시작한다. 로그를 뒤지면 단서가 부족하고, 스레드 덤프를 떠 보면 어딘가 익숙한 이름이 자꾸 보인다 — `ForkJoinPool.commonPool-worker-3`, `ForkJoinPool.commonPool-worker-5`. 그제야 누군가가 묻는다. "그 `parallelStream()`, 그게 정말 우리가 의도한 거였나?"

이게 Stream을 둘러싼 가장 흔한 *난감함*이다. 우리는 Stream을 "컬렉션을 함수형으로 다루는 새 API" 정도로 안다. `filter` 다음에 `map`, 그 다음에 `collect`. 한 줄로 우아하게 풀린다. 그런데 그 "우아함"이 정확히 무엇을 뜻하는지, 안쪽에서 무엇이 벌어지는지를 한 문장으로 말해보라면 갑자기 말문이 막힌다. Stream은 컬렉션인가? 아니면 컬렉션 위에 얹힌 뷰인가? 그것도 아니면 따로 존재하는 새 자료구조인가? 답이 모두 어긋난다.

Stream을 정확히 이해하지 않으면 그것을 *오용*하는 모든 패턴이 자연스러워 보인다. `peek` 안에서 외부 변수에 값을 쓰고, `forEach`로 상태를 변경하고, 멀티 스레드 환경에서 `Collectors.toMap`이 던지는 `IllegalStateException`에 당황한다. 이번 장에서는 한 발 물러서서, Stream이 *무엇이고 무엇이 아닌지*부터 차분하게 짚어보자. 그 다음에야 중간 연산과 종단 연산의 카탈로그가 의미를 갖는다.

### Stream은 컬렉션이 아니다

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

### non-interference와 statelessness — Stream이 우리에게 요구하는 두 가지

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

### 중간 연산의 카탈로그 — 익숙한 것부터 덜 익숙한 것까지

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

### 종단 연산의 카탈로그

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

### 박싱 함정과 primitive Stream

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

### `parallelStream()`의 진실

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

### Spring과의 접점 — JPA Stream return의 함정

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

### 마무리

Stream은 컬렉션이 아니다. 데이터가 *흘러* 지나가는 lazy 파이프라인이고, 종단 연산이 트리거되기 전까지 아무 일도 일어나지 않는다. non-interference와 statelessness가 그 위에서 약속처럼 따라온다. 이 두 약속을 깨면 sequential에서는 어쩌다 잘 돌다가 parallel에서 결과가 흔들린다.

중간 연산은 stateless가 기본이지만 `distinct`·`sorted`처럼 stateful한 것도 있다. 종단 연산은 lazy 파이프라인의 트리거이며, `reduce`는 identity와 associativity 위에서만 정확하다. primitive Stream은 박싱 비용을 깎아주는 도구로 *반드시* 떠올리는 편이 좋다. 그리고 `parallelStream`은 그 한 줄로 commonPool 전체를 흔들 수 있는 강력하고 *위험한* 도구다 — blocking I/O에 태우지 말고, CPU-bound 작업에서도 크기가 충분할 때만 신중히 쓰자.

여기까지가 Stream의 "표면"이다. 그러나 한 가지 자리가 여전히 남는다. `collect`. Stream의 종단 연산 중 가장 자주 쓰면서도 가장 깊은 자리다. `Collectors.groupingBy`로 한 줄에 마법을 부린 적이 있는가? 그 마법의 안쪽을 들여다보지 않으면, 어느 날 "왜 이게 안 되지?" 하고 *난감해질* 때가 반드시 온다. 게다가 Java 22~24에 등장한 새 도구 `Stream::gather`는 그동안 "Stream에서는 어색했다"고 여겼던 패턴들 — 슬라이딩 윈도우, 누적합, rate-limited 매핑 — 을 한 줄로 풀어준다. 다음 장에서는 `Collector`의 5요소를 직접 분해해 만들어보고, `Gatherer`로 자바 함수형의 *봉우리*를 한 번 올라가보자.

---

## 6장. Collector·Reducer·Gatherer — Stream의 종착과 새 중간 정거장

"5분 이동 평균을 Stream으로 한 번 구해보세요."

기획에서 데이터 분석 요건이 떨어졌다고 해보자. 결제 트랜잭션이 초당 수백 건씩 쌓이는데, *최근 5분간* 평균 결제 금액을 실시간으로 내고 싶다는 요구다. Stream에 익숙한 우리는 자신 있게 IDE를 연다. `filter` → `map` → `collect`. 그런데 손가락이 멈춘다. *슬라이딩 윈도우*. Stream에서 이걸 어떻게 표현하지?

`Collectors`를 한참 뒤져도 그런 자리는 없다. `groupingBy(timeBucket)`로 5분 단위 *고정* 버킷은 만들 수 있지만, "지금 시각 기준 직전 5분"이라는 *움직이는* 창은 만들 수 없다. for-loop으로 돌아가면 인덱스 두 개를 굴리면 된다. 그런데 Stream 한 줄로는 안 된다. 답답하다. *번거롭다*. 한참 끙끙대다가 결국 `IntStream.range(0, list.size() - 4).mapToObj(i -> list.subList(i, i + 5))` 같은 *어색한* 우회를 짜놓고 PR을 올린다. 리뷰어가 묻는다 — "이게 자연스러워 보이세요?" 답이 없다.

Stream API가 출시된 지 11년이 흘렀는데, *슬라이딩 윈도우*가 그동안 그렇게 *번거로웠던 이유*는 무엇일까. 정답은 단순하다. Stream의 중간 연산 자리가 닫혀 있었기 때문이다. `filter`·`map`·`flatMap`·`distinct`·`sorted` — 우리가 새 중간 연산을 직접 만들 수단이 없었다. `Collector`로 마지막 자리는 열려 있는데, 중간 자리는 막혀 있었다. 그래서 1:N, N:1, N:N 변환이 필요한 모든 패턴이 어색하게 우회해야 했다. 슬라이딩 윈도우, 누적합, rate-limited 매핑, 중복 제거의 변형 — 모두 이 막힘에 부딪쳐 *지긋지긋함*을 남겼다.

이 닫혀 있던 자리가 Java 22에서 preview로 열리고, Java 24에서 표준화됐다. 이름은 *Stream Gatherers* (JEP 461 → 473 → 485). 그 이야기에 도달하기 전에, 먼저 Stream의 종착인 `Collector`부터 깊이 들여다보자. `Collector`를 정확히 이해하지 않으면 `Gatherer`의 의미가 반쪽으로 들어온다. 이 두 도구는 형제다.

### `Collectors`의 표면 — 익숙한 자리부터

`Stream::collect`에 가장 자주 넘기는 인자는 `Collectors`의 정적 팩토리다. 거의 모든 자리에서 다음 셋만 알면 80%는 처리된다 — `toList`·`toMap`·`groupingBy`. 그러나 그 셋만 알면 나머지 20%의 자리에서 *난감*해진다. 카탈로그를 한 번 죽 늘어놓고 시작하자.

| Collector | 의미 |
|-----------|------|
| `toList()` | 가변 List로 모음 (구현 비지정) |
| `toUnmodifiableList()` (Java 10) | 불변 List로 모음 |
| `toSet()` / `toUnmodifiableSet()` | Set으로 모음 |
| `toMap(keyFn, valueFn)` | Map으로 모음, 키 충돌 시 예외 |
| `toMap(keyFn, valueFn, mergeFn)` | 키 충돌 시 mergeFn으로 합침 |
| `toMap(keyFn, valueFn, mergeFn, mapFactory)` | Map 구현을 직접 지정 |
| `groupingBy(classifier)` | 분류기로 `Map<K, List<V>>` |
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

### `Collector`를 직접 만들어보자

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

### `reduce`의 세 가지 시그니처 — 다시

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

### Gatherer — 닫혀 있던 중간 자리가 열리다

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

### 내장 Gatherer 4종

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

### Gatherer를 직접 만들어보자

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

### 함수형 관점 — fold, composition, monad-ish patterns

여기까지 5요소의 `Collector`와 4요소의 `Gatherer`를 봤다. 두 도구가 비슷한 모양을 한 이유, 그리고 `reduce`까지 다 같은 가족이라는 사실 — 이것을 *함수형의 큰 그림*에서 한 번 정리하자.

#### 모든 것은 fold다

먼저 `reduce`. 시그니처 (2) `T reduce(T identity, BinaryOperator<T> op)`는 정확히 monoid 위의 fold다. monoid가 보장되면 sequential·parallel 결과가 같다.

다음 `collect`. `Collector`의 5요소는 *가변 누적 fold*다. 누적 컨테이너에 `accumulator`로 원소를 담고, `combiner`로 부분 컨테이너를 합치며, 마지막에 `finisher`로 결과를 변환한다. fold의 일반화에 불과하다.

마지막 `gather`. `Gatherer`의 `integrator`는 fold의 step function인데, downstream에 *여러 개*를 흘릴 수 있도록 일반화된 것이다. 0개를 흘리면 filter, 1개를 흘리면 map, N개를 흘리면 flatMap, 누적해서 모았다가 한 번에 흘리면 windowing. 모두 *같은* 추상의 다른 모습이다.

그래서 자바 함수형의 자리에 도구가 셋이라는 사실이 아니라, *같은 fold가 세 가지 자리에 자기 모양을 잡았다*고 보는 편이 정확하다. 이 시야를 한 번 갖고 나면, 새 도구를 마주칠 때마다 "이건 fold의 어느 모습인가"를 묻게 된다. 다음 자바가 또 새 추상을 들고 오면, 그것도 fold의 모습으로 들어올 가능성이 높다.

#### composition — 작은 부품의 결합

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

#### monad-ish patterns — flatMap의 형식

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

### Java 8 collector 지옥 vs Java 24 gatherer

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

### Spring 맥락 — 배치 인서트와 윈도우 집계

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

### 마무리

`Collector`는 종단 연산의 일반화고, `Gatherer`는 중간 연산의 일반화다. 5요소의 `Collector`와 4요소의 `Gatherer`는 *fold라는 같은 추상*의 다른 모습이다. 합성 가능하고, 재사용 가능하고, 사용자 정의가 자유롭다. 11년 동안 *지긋지긋했던* 슬라이딩 윈도우·prefix sum·rate-limited 매핑이 한 줄로 풀린다.

monoid를 한 번 *기억해두자*. identity와 associativity가 parallel safety의 수학적 기반이다. monad-ish 형식 `M<A> + (A -> M<B>) -> M<B>`도 *기억해두자*. 그 형식이 `Stream`, `Optional`, `CompletableFuture`에서 모두 같은 자리에 등장한다.

이제 그 형식이 다음 장의 무대로 그대로 옮겨간다. `Optional<T>`다. NPE의 명시화로 출발한 이 작은 컨테이너가 어떻게 monad-ish 패턴의 한 자리를 차지하게 됐는지, 그리고 그 자리에서 우리가 어떤 *함정*에 자주 빠지는지를 다음 장에서 살펴보자. `user.getAddress().getCity().getZip()`의 NPE를 처음 만난 그날을 한 번 떠올리며.

---

## 7장. `Optional<T>` — 약속과 함정 {#ch-07-optional}

`user.getAddress().getCity().getZip()`의 NPE를 처음 만난 그날을 기억하는가.

테스트 환경에서는 멀쩡히 돌던 한 줄이다. 정산 페이지를 띄우면 사용자의 우편번호가 나와야 한다. 동료가 한 줄로 깔끔하게 적었다. 검토하는 우리도 자연스러워 보였다. 한 달 뒤 운영에서 `NullPointerException`이 떨어진다. 스택 트레이스가 가리키는 줄은 그 한 줄이고, 메시지는 단순하다. 어디서 `null`이 됐는지는 정확히 안 적혀 있다. 주소가 없는 사용자였나? 주소는 있는데 도시가 없었나? 도시까지 있는데 zip이 빠진 건가? 셋 다 가능하다. 그날 누구나 한 번씩 결심한다 — "다시는 이 패턴을 안 쓰겠다."

그래서 우리는 Java 8과 함께 들어온 `Optional<T>`를 반갑게 맞이했다. *Optional은 NPE의 명시화*다. 함수가 "값이 *있을 수도 있고 없을 수도 있는* 결과"를 돌려준다는 사실을 타입 시그니처에 박아 넣는다. 호출자는 `Optional`을 받는 순간 "이건 비어 있을 수 있구나"를 *반드시* 의식하게 된다. 깔끔한 약속이다.

그러나 이 약속을 우리는 *제대로* 쓰고 있는가?

10년이 지난 지금, 코드베이스를 한 번 훑어보면 *찜찜한* 자리가 곳곳에 보인다. `Optional<List<Order>>`를 반환하는 메서드, `Optional`을 클래스 *필드*로 들고 다니는 DTO, `optional.get()`을 일단 부르고 보는 패턴, `if (opt.isPresent()) opt.get()`이라는 `null != x ? x : null` 수준의 코드. Brian Goetz가 *반환 타입 전용*이라고 못 박았던 의도가 무색해진 자리가 한둘이 아니다. Optional을 둘러싼 가장 큰 *당혹감*은 NPE가 아니라, *Optional을 어디까지 어떻게 쓸지에 대한 합의 부재*다.

이번 장에서는 Optional의 *정확한 의도*를 다시 짚고, 거기서 자주 어긋나는 안티패턴을 짚어보자. 그리고 6장에서 미리 약속한 *monad-ish 색채*를 회수한다. `Optional::flatMap`이 왜 `Stream::flatMap`, `CompletableFuture::thenCompose`와 같은 모양인지를 한 자리에서 정리하자.

### Optional은 무엇이고 무엇이 아닌가

먼저 한 가지 인용을 박아두자. `Optional`의 설계자인 Brian Goetz가 2014년 Stack Overflow에 직접 남긴 답변이다.

> Of course, people will do what they want. But we did have a clear intention when adding this feature, and it was not to be a general purpose `Maybe` or `Some` type, as much as many people would have liked us to do so. Our intention was to provide a limited mechanism for library method return types where there needed to be a clear way to represent "no result."

번역하면 — "사람들이야 자기 마음대로 쓸 것이다. 그러나 우리는 분명한 의도를 갖고 이 기능을 추가했다. *범용* Maybe/Some 타입이 되라는 의도가 아니었다. 라이브러리의 *메서드 반환 타입*에서 '결과 없음'을 명확히 표현하기 위한 *제한적* 도구가 우리의 의도였다." 한 줄로 정리하면 — **Optional은 return type 한정**이다.

이게 왜 중요할까? 다른 자리에서 쓰면 무엇이 어긋나는지 하나씩 따라가보자.

#### 필드 자리

```java
public class User {
    private Optional<Address> address;  // 찜찜한 자리
    ...
}
```

이 자리가 *찜찜한* 이유는 셋이다.

첫째, `Optional`은 직렬화 친화적이지 않다. `Optional`은 `Serializable`을 구현하지 않는다. Jackson 같은 JSON 직렬화는 별도 모듈이 있어야 다룬다. RPC, Kryo, 세션 직렬화에서 모두 *난감해진다*.

둘째, `Optional` 필드는 한 번 더 *간접 참조*를 만든다. `User` 100만 개가 있으면 `Optional` wrapper 객체도 100만 개다. 메모리도, 캐시 라인 효율도 손해다. 그 정도는 무시할 수 있다 쳐도, `address` 필드를 매번 `unwrap`해야 하는 *번거로움*은 매 줄에 묻어난다.

셋째, 의도가 어긋난다. 필드가 "있을 수도 있고 없을 수도 있다"는 의미는 `null` 가능성으로 표현하거나, 더 명시적으로는 별도 타입(예: `Address.NONE`, `sealed Address`)으로 표현하는 편이 *바람직하다*. `Optional`로 감싸는 것은 "이 값을 한 번만 길게 다루겠다"는 *반환 타입의 일회성* 의도와 어긋난다.

#### 매개변수 자리

```java
public Order createOrder(Optional<Long> couponId, Optional<String> note) { ... }
```

이 자리는 *번거롭다*. 호출자가 매번 `Optional.empty()`나 `Optional.of(...)`로 감싸야 한다. 게다가 의미상 "쿠폰을 안 쓸 수도 있다"는 정보는 `null`을 허용하거나, 메서드 오버로딩으로 표현하거나, builder 패턴으로 푸는 편이 더 자연스럽다. 매개변수는 호출자가 *직접* 채우는 자리이므로, 거기에 `Optional`을 강요하는 것은 호출 코드를 *지저분하게* 만든다. IDE가 자동으로 `Optional.of`를 채워주지도 않는다.

#### `Optional<List<T>>` {#sec-optional-list-t}

이게 가장 자주 마주치는 *당혹스러운* 자리다.

```java
public Optional<List<Order>> findRecentOrders(Long userId) { ... }
```

문제가 무엇인가? `List`는 이미 *비어 있을 수* 있다. 빈 List는 그 자체로 "결과 없음"을 표현한다. 거기에 `Optional`을 한 번 더 감싸면 *비어 있음의 의미가 둘로 갈라진다*. `Optional.empty()`인 경우와 `Optional.of(emptyList())`인 경우, 호출자는 무엇을 어떻게 다뤄야 하나? API 문서를 한 번 더 읽어야 한다. *지긋지긋하다*.

권장은 단순하다 — *컬렉션 타입은 절대 `Optional`로 감싸지 말자*. 그냥 빈 List를 돌려주는 편이 *바람직하다*. `Collections.emptyList()`나 `List.of()`로.

```java
public List<Order> findRecentOrders(Long userId) {
    // ... 없으면 List.of() 반환
}
```

`Map`도 마찬가지다. 빈 `Map`이 "결과 없음"을 그대로 표현한다. `Stream`도 그렇다. `Optional<Stream<T>>`는 처음 만나는 사람을 한참 *난감하게* 만든다. 그러니 다음을 *기억해두자*. **컨테이너 타입은 자기 자신이 비어 있는 상태를 표현할 수 있다. `Optional`로 한 번 더 감싸지 말자.**

#### `Optional.of(null)`이라는 오해

이건 흔한 함정이다. 첫 입문자가 자주 한다.

```java
return Optional.of(user.getAddress());   // user.getAddress()가 null일 수도 있다면 NPE
```

`Optional.of(x)`는 `x`가 `null`이면 *즉시* `NullPointerException`을 던진다. `null`이 가능한 값이라면 `Optional.ofNullable(x)`를 써야 한다.

```java
return Optional.ofNullable(user.getAddress());
```

세 정적 팩토리를 한 번 *기억해두자*.

- `Optional.of(x)` — `x`가 `null`이면 NPE. 절대 `null`이 아닌 값에 쓴다.
- `Optional.ofNullable(x)` — `x`가 `null`이면 `empty()`. `null` 가능성이 있을 때.
- `Optional.empty()` — 비어 있음을 명시.

#### `optional.get()`의 남발

이건 *끔찍한* 자리다.

```java
Optional<User> user = repo.findById(id);
return user.get();   // 비어 있으면 NoSuchElementException
```

`Optional`을 받아놓고 곧바로 `.get()`을 호출하면, 정확히 `Optional`이 막으려 했던 *그* 자리로 돌아간다. NPE 대신 `NoSuchElementException`이 떨어질 뿐, 본질은 같다. 게다가 stack trace는 더 *어색하다*. NPE는 무엇이 null인지 적어도 줄 번호로 가리키는데, `NoSuchElementException: No value present`는 그것도 없다.

권장은 단순하다. `.get()`을 보면 한 번 더 들여다보자. 거의 모든 자리에서 `.orElse(...)`, `.orElseGet(...)`, `.orElseThrow(...)`, `.ifPresent(...)` 중 하나가 더 정확한 의도를 표현한다.

```java
// 기본값으로 대체
User user = repo.findById(id).orElse(User.GUEST);

// 기본값을 비싸게 만들어야 한다면 lazy
User user = repo.findById(id).orElseGet(() -> userFactory.newGuest());

// 없으면 예외 — 비즈니스 의미 있는 예외로
User user = repo.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));
```

`orElse`와 `orElseGet`의 차이를 *반드시* 기억해두자. `orElse(fallback)`은 *항상* fallback 표현식을 평가한다. `orElseGet(supplier)`는 *비어 있을 때만* supplier를 호출한다. 비용이 큰 기본값이라면 `orElseGet`을 골라야 한다.

```java
// 매번 newGuest()를 호출한다 — 비어 있지 않아도
repo.findById(id).orElse(userFactory.newGuest());

// 비어 있을 때만 newGuest()를 호출한다
repo.findById(id).orElseGet(() -> userFactory.newGuest());
```

이 차이로 잘 돌던 서비스가 갑자기 *느려지는* 자리가 흔하다. 인지하면 한 줄 차이지만, 인지하지 못하면 한참을 끙끙대게 된다.

### Optional의 핵심 메서드 — `map`·`flatMap`·`filter`

이제 도입의 그 자리, `user.getAddress().getCity().getZip()`을 정확히 다듬어보자. 다음을 보자.

```java
// null-check 사다리
public Optional<String> zipOf(User user) {
    if (user == null) return Optional.empty();
    Address a = user.getAddress();
    if (a == null) return Optional.empty();
    City c = a.getCity();
    if (c == null) return Optional.empty();
    String z = c.getZip();
    return Optional.ofNullable(z);
}
```

여섯 줄이다. 같은 일이 Optional의 `map`·`flatMap`으로는 어떻게 표현되는가?

```java
public Optional<String> zipOf(User user) {
    return Optional.ofNullable(user)
        .map(User::getAddress)       // address가 null이면 empty
        .map(Address::getCity)        // city가 null이면 empty
        .map(City::getZip);           // zip이 null이면 empty
}
```

세 줄이다. 그리고 각 단계가 자명하다 — "user의 address의 city의 zip을 꺼낸다." `map`의 정확한 의미를 한 번 짚자. `Optional<A>::map(A -> B)`은 다음과 같이 작동한다.

- Optional이 비어 있으면, 그대로 `empty()`를 돌려준다.
- 비어 있지 않으면, 함수를 적용해 결과를 새 Optional로 감싼다. 함수가 `null`을 돌려주면 자동으로 `empty()`.

이 마지막 부분이 미묘하다. `map`에 넘긴 함수의 반환 타입이 *이미* `Optional`이라면? 그러면 `Optional<Optional<X>>`가 된다. 그게 우리가 원하는 자리가 아니다. 이런 자리를 위해 `flatMap`이 있다.

```java
// repo.findAddress가 Optional<Address>를 돌려준다고 해보자
public Optional<String> zipOf(Long userId) {
    return repo.findUser(userId)              // Optional<User>
        .flatMap(this::findAddressOf)         // Optional<Address> (map이면 Optional<Optional<Address>>)
        .map(Address::getCity)                 // Optional<City>
        .map(City::getZip);                    // Optional<String>
}
```

`flatMap`의 정확한 시그니처는 `Optional<A>::flatMap(A -> Optional<B>) -> Optional<B>`다. 함수의 반환이 이미 Optional이라 한 번 더 감싸지 않는다. 6장에서 본 monad-ish 형식 그대로다 — `M<A> + (A -> M<B>) -> M<B>`. `Optional`도 `Stream`도 `CompletableFuture`도 모두 이 형식의 친척이다.

`filter`는 술어로 걸러낸다. 술어가 거짓이면 `empty()`로 바뀐다.

```java
Optional<User> activeUser = repo.findById(id)
    .filter(User::isActive);   // 비활성이면 empty
```

이 셋 — `map`·`flatMap`·`filter` — 이 Optional의 *체인* 표현 방식이다. null-check 사다리를 명령형으로 짜는 자리에서, *흐름*으로 바꿔준다. 도입의 그날의 결심을 진짜로 실현하는 도구다.

### Java 9에서 더해진 자리들

Java 9가 Optional에 몇 가지를 더 추가했다. 자주 쓰는 셋만 짚자.

#### `ifPresentOrElse`

값이 있으면 한 액션, 없으면 다른 액션. 그동안 두 줄로 적던 자리를 한 줄로 줄여준다.

```java
repo.findById(id).ifPresentOrElse(
    user -> log.info("found: {}", user.email()),
    () -> log.warn("missing: id={}", id)
);
```

#### `or` — 비어 있을 때 다른 Optional로 fallback

```java
Optional<User> u = primaryRepo.findById(id)
    .or(() -> backupRepo.findById(id))
    .or(() -> Optional.of(User.GUEST));
```

여러 소스를 차례로 시도하는 자리에 잘 맞는다. `orElse`와 비슷해 보이지만 다르다. `orElse`는 *값*을 돌려주고 체인이 끝난다. `or`은 *Optional*을 돌려주고 체인이 계속된다.

#### `stream` — Optional을 Stream에 흘리기

Java 9의 `Optional::stream`은 작아 보이지만 강력하다. `Optional<T>`를 0개 또는 1개 원소의 `Stream<T>`로 바꾼다. `Stream`의 `flatMap`과 결합하면 "Optional들의 시퀀스에서 비어 있는 자리를 제거하면서 펼친다"가 한 줄에 풀린다.

```java
// Java 8까지 — 어색했다
List<User> users = ids.stream()
    .map(repo::findById)             // Stream<Optional<User>>
    .filter(Optional::isPresent)
    .map(Optional::get)              // 찜찜한 .get()
    .collect(Collectors.toList());

// Java 9+ — 깔끔하다
List<User> users = ids.stream()
    .map(repo::findById)             // Stream<Optional<User>>
    .flatMap(Optional::stream)       // Stream<User>, 비어 있는 자리는 그냥 사라짐
    .toList();
```

`filter` + `get`이라는 *지긋지긋한* 패턴이 `flatMap(Optional::stream)` 한 줄로 정리된다. *기억해두자*. ids → repo lookup → 결과 모음 패턴이라면 이 형식이 거의 항상 들어맞는다.

### Optional의 monad 색채

이쯤에서 6장의 약속을 회수하자. `Optional::flatMap`이 `Stream::flatMap`, `CompletableFuture::thenCompose`와 같은 형식이라는 사실. 한 번 나란히 늘어놓자.

```java
// Stream
<R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper);

// Optional
<U> Optional<U> flatMap(Function<? super T, ? extends Optional<? extends U>> mapper);

// CompletableFuture
<U> CompletableFuture<U> thenCompose(Function<? super T, ? extends CompletionStage<U>> fn);
```

같은 모양이다. *컨텍스트 안의 값* + *컨텍스트로 가는 함수* → *컨텍스트 안의 결과*. 카테고리 이론에서는 이 형식을 monad의 bind라고 부른다. 자바가 이 셋을 *우연히* 같은 모양으로 만든 건 아니다 — Java 8 함수형 그룹의 설계 의도였다.

이걸 알면 무엇이 좋은가?

첫째, *새 컨테이너*를 만나도 패턴이 같다. `Result<T>`(rust-style success/failure), `Try<T>`(vavr), `Either<L, R>` — 모두 `flatMap`이 있다면 같은 형식으로 체인한다.

둘째, *코드의 의도*가 한 패턴으로 통일된다. "값이 있을 수도 있고 없을 수도 있다"는 컨텍스트, "비동기 미래 시점에 결과가 올 것이다"는 컨텍스트, "여러 원소가 펼쳐진다"는 컨텍스트 — 모두 같은 *체인의 모양*으로 표현된다. 그래서 한 패턴을 익혀두면 다른 자리에 그대로 옮긴다.

다만 Brian Goetz가 한 발 물러나 한 말도 *기억해두자*. "Optional은 모나드가 아니다. 그러나 모나드처럼 쓸 수 있는 자리들이 있다." 정확하게는 자바 타입 시스템이 모나드 법칙을 *강제하지 못한다*. 사용자가 `flatMap`에 부수 효과를 섞거나 `null`을 돌려주거나 하면 형식이 깨진다. 그래서 자바의 Optional은 "monad-ish"이지 monad가 아니다. 그러나 *형식이 같아서 같은 사고법을 쓸 수 있다*는 사실은 그대로 남는다. 그것만으로도 우리에게 충분한 가치다.

### `null` vs `Optional.empty()` vs sentinel

API를 설계할 때 한 번씩 고민이 된다. "결과 없음"을 어떻게 표현할까. 세 가지 선택지가 있다.

1. `null`을 돌려준다. 호출자가 `null`-check를 한다.
2. `Optional.empty()`를 돌려준다. 호출자가 `map`·`flatMap`·`orElse` 체인을 쓴다.
3. *sentinel* 값(예: `User.GUEST`, `Money.ZERO`)을 돌려준다. 호출자가 그것을 정상값처럼 다룬다.

각각의 자리가 다르다.

**`null`을 권장하는 자리** — 명확히 *없음*이 정상 흐름이 아닐 때. 가령 내부 헬퍼 메서드, private 메서드, 컬렉션의 `get(key)`(있는지 사전에 보는 게 일반적). Brian Goetz도 인터뷰에서 "Optional이 null을 *대체*하는 게 아니다, 그저 *반환 타입에서* null을 명시화하는 자리에 좋다"라고 말한다.

**`Optional.empty()`를 권장하는 자리** — public API의 반환 타입. 호출자가 "결과 없음"을 인지하고 처리해야 하는 자리. `Stream::findFirst`, `Repository::findById`, `Map::get`을 감싸는 wrapper 등.

**sentinel을 권장하는 자리** — "없음"이 자주 일어나고, 도메인적으로 *기본값*이 명확할 때. 가령 잔액이 없으면 `Money.ZERO`, 사용자가 비로그인이면 `User.GUEST`. sentinel은 null-check도 Optional unwrap도 필요 없어 호출 코드가 가장 *깔끔*하다.

세 가지를 *반드시* 구분해두자. 한 가지 만능 패턴이 아니다.

### JPA·Spring Data와 Optional

실무의 자리로 가보자. Spring Data Repository는 다음과 같이 Optional을 돌려준다.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
```

이건 거의 모범적인 자리다. ID·email로 단일 결과를 찾는 자리에서 *없음*이 가능하다는 것을 명시적으로 표현한다. 호출 코드는 다음과 같이 깔끔하게 흐른다.

```java
@Transactional(readOnly = true)
public UserSummary summaryOf(String email) {
    return userRepo.findByEmail(email)
        .map(UserSummary::from)
        .orElseThrow(() -> new UserNotFoundException(email));
}
```

여기에 *함정*이 하나 있다. Optional 안의 JPA 엔티티는 *영속성 컨텍스트*에 묶여 있다. `@Transactional` 범위를 벗어나면 그 엔티티의 lazy 연관 관계를 건드릴 때 `LazyInitializationException`이 떨어진다. 그래서 Optional의 `map` 단계에서 즉시 DTO로 변환해 *분리*해두는 편이 *바람직하다*. 위 코드의 `.map(UserSummary::from)`이 정확히 그 자리다.

또 한 자리 — `@RequestParam(required = false)`와 Optional.

```java
@GetMapping("/search")
public List<Order> search(@RequestParam Optional<String> q,
                          @RequestParam(defaultValue = "10") int size) { ... }
```

Spring은 `@RequestParam`을 Optional로 받는 패턴을 지원한다. 하지만 권장이 갈린다. 한쪽에서는 "Optional을 매개변수 자리에 두는 안티패턴"이라고 한다. 다른 쪽에서는 "Spring MVC는 컨트롤러 시그니처를 직접 호출하지 않으므로, 그 자리는 일반적인 메서드 매개변수와 다르다"고 한다. 정착된 권장은 *팀의 컨벤션*을 따르되, 일관성을 깨지 말자는 정도다. 어느 쪽이든 한 컨트롤러 안에서는 같은 스타일로 가는 편이 *바람직하다*.

### 안티패턴 6가지 — 정리

지금까지 짚은 자리를 한 번 묶어두자. *반드시* 피해야 할 여섯 자리다.

1. **`Optional`을 필드로 들고 다닌다** — 직렬화·메모리·간접 참조 모두 *번거롭다*. null 가능 필드, sealed 타입, 별도 plain field로 푸는 편이 낫다.
2. **`Optional`을 매개변수로 받는다** — 호출자에게 `Optional.of` 감싸기를 강요한다. 메서드 오버로딩이나 builder가 *바람직하다*.
3. **`Optional<List<T>>`/`Optional<Map<K,V>>`** — 빈 컬렉션이 이미 "없음"을 표현한다. 한 번 더 감싸지 말자.
4. **`Optional.of(x)`로 nullable x를 감싼다** — NPE. `Optional.ofNullable`을 쓰자.
5. **`optional.get()` 남발** — `Optional`의 의미를 무효화한다. `orElse`·`orElseGet`·`orElseThrow`·`ifPresent`를 골라 쓰자.
6. **`if (opt.isPresent()) opt.get()` 패턴** — null-check를 *흉내*낸 코드다. `ifPresent`·`map`·`flatMap`으로 다시 적자.

이 여섯을 *잊지 말자*. Optional을 *제대로* 쓰는 것은 NPE를 줄이는 일이 아니라, *체인의 흐름*으로 사고하는 일이다.

### 미래 — null-restricted types와 JSpecify

마지막으로 한 발 앞을 내다보자. 자바의 null 문제는 Optional로 *완전히* 해결되지 않았다. 컬렉션 원소의 null, 메서드 매개변수의 null, 필드의 null — 모든 자리가 Optional로 감싸기에는 너무 *번거롭다*. 그래서 코틀린은 `String?` vs `String`을 *언어 차원*에서 구분했고, Swift는 `Optional<T>` 위에 `?` 문법 설탕을 얹었다. 자바는 어디로 갈까?

두 가지 흐름이 있다.

**JSpecify** — 자바 커뮤니티의 합의 노력이다. `@Nullable`, `@NonNull` 어노테이션의 *표준화*를 추진한다. IntelliJ·NullAway·CheckerFramework 등 도구가 같은 어노테이션 어휘를 공유해 정적 분석을 일관되게 한다. 이미 상당히 정착했다.

**Project Valhalla & null-restricted types** — OpenJDK의 더 야심 찬 방향. JEP draft 단계에서 `String!`(non-null) vs `String?`(nullable)을 타입 시스템에 *직접* 박아 넣자는 제안이 논의 중이다. value type과 결합해 메모리 표현까지 최적화한다. 시점은 아직 불확실하다. Valhalla 자체가 10년째 진행 중인 거대 프로젝트라, null-restricted types는 그 한 갈래로 따라온다.

이 두 흐름이 합쳐지면 `Optional`의 *역할*도 조금 달라질 수 있다. 메서드 반환의 "없음 가능성"을 타입으로 표현하는 자리는 여전히 `Optional`이지만, 컬렉션 원소나 필드의 null 표현은 어노테이션·언어 문법으로 옮겨갈 가능성이 크다. 그날이 오면 우리는 다시 한 번 *Optional을 어디까지 쓸지*를 다듬게 될 것이다. 그러나 그 다듬음은 *Optional을 더 정확하게* 쓰는 방향이지, *없애는* 방향은 아닐 것이다.

### 마무리

Optional은 *반환 타입*에서 "결과 없음"을 명시화하는 *제한적* 도구다. 필드·매개변수·컬렉션 감싸기에는 어울리지 않는다. `get()`은 남발하지 말고 `map`·`flatMap`·`filter`로 체인하자. `orElse`와 `orElseGet`의 평가 시점 차이를 *반드시* 기억해두자. Java 9의 `ifPresentOrElse`·`or`·`stream`은 작지만 코드의 *답답함*을 정확하게 풀어준다.

`Optional::flatMap`이 `Stream::flatMap`·`CompletableFuture::thenCompose`와 같은 형식이라는 사실, 그 형식이 monad-ish 패턴의 한 모습이라는 사실 — 이 시야를 한 번 *기억해두자*. 자바 안에 *함수형 자바*라는 부분 언어가 자리 잡았고, Optional은 그 부분 언어의 한 시민이다. 도입의 그날 결심한 *"다시는 이 패턴을 안 쓰겠다"*가 실현되는 자리는, `null`-check를 줄이는 자리가 아니라 *체인의 흐름*으로 사고하는 자리다.

여기까지가 Part III의 끝이다. 함수형 자바의 기초(3·4장)에서 출발해, Stream의 해부(5장), Collector·Gatherer의 봉우리(6장), Optional의 약속과 함정(7장)까지 한 호흡으로 왔다. 다음 부에서는 결이 크게 바뀐다. *동시성*이다. `synchronized`와 `volatile`이 정확히 무엇을 보장하는가? `java.util.concurrent`의 지형은 어떻게 생겼는가? 그리고 우리가 5장 끝에서 *끔찍한 일*이라 부른 `parallelStream`의 commonPool 사건은, 왜 그렇게 자주 일어났는가? 8A장에서 Java Memory Model을 정확히 들여다보고, 8B장에서 `CompletableFuture`와 `Flow`로 비동기 조합의 두 갈래를 살펴보자. Loom 이전 시대의 자바 동시성을 한 번 차분히 정리하고 나면, 14장의 virtual thread가 왜 *대전환*이라 불리는지가 비로소 *체감*된다.

---

# Part IV. 동시성 I — Loom 이전의 모든 것

Virtual Thread가 들어오기 전, 우리가 알던 동시성은 *thread를 아껴 쓰는* 모델이었다. Tomcat 200 thread 풀, `ExecutorService` 한 줄, `CompletableFuture` 체인, 그리고 — 답답함을 못 견딘 누군가가 도입한 Reactive Streams. 이 모든 도구는 *thread가 비싼 자원*이라는 한 줄의 전제 위에서 자랐다. 그 전제가 21에서 무너졌다는 사실은 14장에서 본격적으로 다룬다. 그러나 그 무너짐을 *제대로 이해하려면*, 먼저 무너진 그것이 *무엇이었는지* 정확히 알아야 한다.

8A장은 `java.util.concurrent`(Doug Lea의 위대한 유산)와 Java Memory Model의 토대다. `volatile`·`synchronized`·`final`이 정확히 무엇을 보장하는지, *happens-before*가 한국어로 *번역되기 전에 영문 표현 그대로 외워둬야 하는 이유*가 무엇인지, OOTA(out-of-thin-air)라는 단어가 왜 그렇게 두려운지를 본다. JLS §17.4와 §17.5의 핵심 문장을 직접 인용하며, 우리가 *얕게 알고 있던 것의 깊이*를 다시 잰다.

8B장은 그 토대 위에서 자란 두 갈래 — `CompletableFuture`와 `java.util.concurrent.Flow`(Reactive Streams의 표준화) — 를 본다. `CompletableFuture`의 `thenCompose`·`thenCombine`·`exceptionally`가 어떤 *사고의 형태*를 강요하는지, Reactive Streams가 backpressure로 풀려 한 *그 어렵던 문제*가 정확히 무엇이었는지, 그리고 두 모델이 모두 *thread가 비싸다*라는 한 줄의 전제 때문에 *그 모양이었음*을 본다.

8A·8B를 다 읽고 나면, Part VII(Loom 시대)에서 만나는 *thread-per-request의 부활*이 왜 그렇게 충격적인지 자연스럽게 이해된다. Loom은 동시성을 새로 만든 게 아니라, *전제 하나를 무너뜨려 모든 코드의 모양을 바꾼* 사건이다. 그 사건을 제대로 보려면, 옛 전제 위에 무엇이 자라 있었는지부터 봐야 한다.

---

## 8A장. j.u.c와 Java Memory Model — 동시성의 토대

단일 인스턴스에서 잘 돌던 코드가 멀티 코어에서 깨졌다고 해보자.

재고 차감 로직이다. 주문이 들어오면 `Stock.count`를 하나 깎고 DB에 반영한다. 통합 테스트는 통과했다. QA 환경에서도 문제없었다. 그런데 운영 단일 노드에 코어 16개짜리 머신을 박고 부하 테스트를 돌렸더니, 5만 건 주문에 재고가 0으로 떨어져야 할 자리에서 *마이너스 23*이 찍혀 있다. 로그를 봐도 예외는 없다. 트랜잭션 격리 수준은 `READ_COMMITTED`로 맞춰 뒀고, JPA의 1차 캐시도 의심해 봤다. 결국 문제는 자바 코드의 가장 평범해 보이던 한 줄이었다.

```java
public class Stock {
    private int count;
    public void decrement() { count--; }
}
```

`count--` 한 줄이 무엇이 문제일까? 그것은 *하나의 연산이 아니다.* 읽고, 빼고, 쓰는 세 단계다. 게다가 그 세 단계 사이에 다른 스레드가 끼어들 수 있다는 것보다 더 무서운 사실이 있다 — *내가 쓴 값이 다른 스레드의 시야에 영원히 도달하지 않을 수도 있다.* 메모리 모델이라는 단어를 처음 들어본 사람에게 이 문장은 거의 협박처럼 들린다. 그러나 자바 동시성의 모든 것은 정확히 이 한 문장에서 출발한다.

이 장에서는 우리가 매일 쓰던 `synchronized`와 `volatile`이 *정확히 무엇을 보장하는지*, 그리고 그 보장의 근거가 되는 Java Memory Model(JMM)이 어떤 모양인지를 들여다본다. JSR 133이라는 무거운 이름의 문서를 회피하지 말자. 이 문서를 한 번 정독한 개발자는 그렇지 않은 개발자와 동시성 코드를 짤 때 완전히 다른 사람이 된다. 그러고 나면 `java.util.concurrent`(이하 j.u.c) 패키지가 *왜 그 모양으로* 설계됐는지가 비로소 보이기 시작한다.

### 메모리 모델은 *왜* 필요한가

먼저 한 가지 오해부터 풀자. JMM은 "JVM이 메모리를 어떻게 배치하는가"에 대한 명세가 *아니다.* JMM은 **여러 스레드가 공유 변수에 행한 읽기·쓰기가 서로에게 어떤 순서로 보이는가**를 규정하는 명세다. 더 정확히 말하면, *어떤 순서로 보일 수 있는지*에 대한 *제약*이다.

왜 이런 제약이 필요한가? 두 가지 현실 때문이다.

첫째, **CPU는 명령어를 재정렬한다.** 현대 CPU는 파이프라인을 비우지 않으려고 의존성 없는 명령어 순서를 자유롭게 바꾼다. 같은 코어의 store buffer는 쓰기를 지연시킬 수 있고, 인접 코어의 캐시는 무효화 메시지를 받기 전까지 오래된 값을 들고 있을 수 있다.

둘째, **JIT 컴파일러도 재정렬한다.** HotSpot은 escape analysis, loop hoisting, dead store elimination 같은 최적화를 수행한다. 그 결과로 소스 코드의 순서와 실제 실행 순서는 별개가 된다.

그렇다면 어떻게 해야 할까? 두 가지 길이 있다. 하나는 *모든 재정렬을 금지*하는 것이다. 그러면 멀티 코어의 성능 이점이 거의 사라진다. 다른 하나는 *프로그래머가 명시한 곳에서만* 재정렬을 제한하는 것이다. 이쪽이 자바가 택한 길이다. JMM은 "프로그래머가 약속한 곳"의 모양을 happens-before라는 관계로 정의한다.

### happens-before — 동시성 코드의 단 하나의 문법

happens-before는 두 액션 A와 B 사이의 *관계*다. "A가 B보다 시간상 먼저 일어났다"가 아니다 — "A의 결과를 B가 *반드시* 볼 수 있다"는 *보증*이다. 시간이 아니라 *가시성*이다.

JLS §17.4.5는 이 관계를 다음과 같이 규정한다.

> **JLS §17.4.5 (Happens-before Order) — 원문 박스**
>
> *"Two actions can be ordered by a happens-before relationship. If one action happens-before another, then the first is visible to and ordered before the second."*
>
> **번역**: 두 액션은 happens-before 관계로 순서가 지어질 수 있다. 만약 한 액션이 다른 액션보다 happens-before 관계라면, 앞 액션은 뒤 액션에게 *가시적*이고 *순서가 보장된다*.
>
> **해설**: 핵심 단어는 *visible*이다. happens-before는 단순한 순서가 아니라 가시성을 약속한다. A가 쓴 값을 B가 반드시 *볼 수 있다*는 보증이며, A의 모든 쓰기(공유 변수든 아니든)가 B 시점에는 메모리에 반영돼 있다는 약속이다.
>
> **본문 연결**: 그러므로 우리가 `volatile`·`synchronized`·`Thread.join`을 쓰는 진짜 이유는 락이 아니라 *가시성을 만드는 일*이다. 락을 잡는 것은 부수 효과일 뿐이다.

happens-before 관계를 만들어 내는 *생성자*들은 정해져 있다. 일곱 가지다.

1. **Program order rule**: 같은 스레드 내에서, 소스 코드 순서대로 happens-before.
2. **Monitor lock rule**: 같은 락에 대한 `unlock`은 그 다음 `lock`보다 happens-before.
3. **Volatile variable rule**: 같은 volatile 변수에 대한 `write`는 그 다음 `read`보다 happens-before.
4. **Thread start rule**: `Thread.start()` 호출은 그 스레드 안의 모든 액션보다 happens-before.
5. **Thread termination rule**: 스레드 안의 모든 액션은 다른 스레드의 `Thread.join()` 반환보다 happens-before.
6. **Interruption rule**: `Thread.interrupt()` 호출은 인터럽트 감지보다 happens-before.
7. **Finalizer rule**: 객체의 생성자 종료는 finalizer 시작보다 happens-before.

그리고 마지막으로 **transitivity** — A → B이고 B → C이면 A → C다. 이 추이성이 실무에서 가장 중요하다. 한 스레드가 volatile 변수에 *플래그* 하나만 쓰면, 그 스레드가 그전에 일반 변수에 쓴 모든 값이 *동시에* 다른 스레드에 가시적이 된다. 플래그 하나에 *모든 쓰기*가 묶여 따라간다는 뜻이다. 이걸 모르고 동시성 코드를 짜면, 디버깅이 거의 불가능한 미스터리에 빠진다.

### volatile은 *정확히* 무엇을 보장하는가

`volatile`을 두고 "최신 값을 보장한다"라거나 "캐시를 무효화한다"라고 설명하는 글이 많다. 둘 다 잘못된 비유다. 정확한 정의는 위의 *volatile variable rule* 한 줄이다 — **같은 volatile 변수에 대한 write는 그 다음 read보다 happens-before**.

여기서 두 가지 함의가 따라온다. 첫째, volatile read는 동기화 진입(`acquire`)과 같은 효과를 낸다. 그 read 이후에 오는 모든 일반 read는 *이전 스레드의 모든 쓰기*를 본다. 둘째, volatile write는 동기화 종료(`release`)와 같은 효과를 낸다. 그 write 이전에 한 모든 일반 write는 *다음 스레드의 어떤 read*에서도 가시적이 된다.

그렇다면 `volatile`로 무엇이 가능하고 무엇이 *불가능*한가?

**가능한 것**: 상태 플래그, 더블 체크 아이디엄의 안전화, lock-free 카운터에 *최신 값 읽기*.

**불가능한 것**: `count++` 같은 *read-modify-write* 연산의 원자성. 왜냐하면 그것은 *세 액션*이지 하나의 액션이 아니기 때문이다. volatile은 *원자성*을 주지 않는다. 원자성은 다른 도구의 영역이다.

```java
private volatile int count;
public void inc() { count++; } // ❌ 여전히 race condition
```

이 코드가 *어떻게* 깨지는지는 자명하다. 두 스레드가 동시에 `count=5`를 읽고, 둘 다 6을 쓰면, 결과는 7이 아니라 6이다. volatile은 *가시성*만 주지 *원자성*은 주지 않는다는 사실을 잊지 말자.

### synchronized와 락의 두 얼굴

`synchronized`는 두 가지 일을 *동시에* 한다. 하나는 **상호 배제**(mutual exclusion) — 같은 락을 잡은 다른 스레드를 막는다. 다른 하나는 **가시성** — `unlock`은 그 다음 같은 락의 `lock`보다 happens-before다. 자바에서 *동시성 도구의 모든 보장*은 이 두 얼굴의 조합으로 만들어진다.

흔한 오해 하나. "단일 스레드만 들어가니까 가시성 문제는 자동으로 풀린다"고 생각하기 쉽다. 정반대다. *상호 배제가 가시성을 만드는 것이 아니라*, synchronized의 happens-before 효과가 가시성을 만든다. 같은 락이라는 점이 핵심이다 — *다른* 락이면 happens-before가 성립하지 않는다.

예제로 보자. 흔한 더블 체크 락킹(double-checked locking, DCL)이다.

```java
public class Holder {
    private static Holder instance;
    public static Holder getInstance() {
        if (instance == null) {              // (1)
            synchronized (Holder.class) {
                if (instance == null) {      // (2)
                    instance = new Holder(); // (3)
                }
            }
        }
        return instance;                     // (4)
    }
}
```

이 패턴은 Java 5 이전까지 *깨진 코드*였다. (3)에서의 객체 생성은 ① 메모리 할당, ② 생성자 실행, ③ 참조 대입의 세 단계로 나뉘는데, JVM이 ②와 ③의 순서를 바꿔도 무방한 시절이 있었다. 다른 스레드가 (1)에서 `instance != null`을 보고 (4)에서 *아직 생성자가 끝나지 않은* 객체를 들고 가는 사태가 가능했다. *끔찍한 일이다.*

Java 5에서 JSR 133이 도입되면서 해법이 생겼다. `instance`를 `volatile`로 선언하면 (3)의 모든 write가 다음 스레드의 (1) read에 가시적이 된다. happens-before가 *전이적으로* 생성자 안의 모든 필드까지 따라가 준다.

```java
private static volatile Holder instance; // Java 5+에서 이 한 줄로 해결
```

이 패턴은 지금도 동작한다. 그러나 더 명확한 대안이 있다 — *holder idiom*이다.

```java
public class Holder {
    private Holder() {}
    private static class Lazy { static final Holder INSTANCE = new Holder(); }
    public static Holder getInstance() { return Lazy.INSTANCE; }
}
```

내부 클래스의 `static final` 필드는 클래스 초기화 시점에 단 한 번 초기화되며, JVM이 그 초기화에 동기화를 보장한다. 더 단순하고, 더 빠르고, *읽는 사람이 즉시 이해한다.* DCL은 역사적으로 의미가 있지만, 실무에서는 이쪽을 *기억해두는 편이 낫다.*

### final 필드의 특별한 약속

JMM에는 *final 필드만을 위한* 별도의 보증이 있다. JLS §17.5다.

> **JLS §17.5 (final Field Semantics) — 원문 박스**
>
> *"The usage model for final fields is a simple one: Set the final fields for an object in that object's constructor; and do not write a reference to the object being constructed in a place where another thread can see it before the object's constructor is finished."*
>
> **번역**: final 필드의 사용 모델은 단순하다. 객체의 생성자 안에서 final 필드들을 초기화하라. 그리고 *생성자가 끝나기 전*에 그 객체의 참조를 다른 스레드가 볼 수 있는 곳에 *써넣지 말라.*
>
> **해설**: 이 약속을 지키면 JMM은 *동기화 없이도* final 필드의 초기값이 모든 스레드에 가시적임을 보장한다. 단, 약속을 지킨 객체에 한해서다.
>
> **본문 연결**: 우리가 `String`·`Integer`·records를 자유롭게 공유하는 이유가 여기에 있다. 그들의 모든 상태는 final이고, 생성자가 끝나기 전에 *this 참조가 새지 않으면* 가시성은 공짜로 따라온다.

여기서 *생성자가 끝나기 전에 this 참조가 새는 일*을 **safe publication 위반**이라 부른다. 흔한 예가 생성자 안에서 리스너에 자기 자신을 등록하는 경우다. 그 순간 *반쯤 초기화된 객체*가 외부에 노출된다. 이건 final 필드의 보증도 깨뜨린다. *난감하다.* 해결은 단순하다 — 등록은 생성자 밖에서, 별도의 초기화 메서드에서 하자.

이것이 records가 동시성에서 *그토록 편한* 이유이기도 하다. records의 컴포넌트는 모두 final이고 canonical constructor가 강제된다. safe publication만 지키면 멀티 스레드에서 공유해도 *동기화 없이도* 안전하다. 자바가 마침내 "값"이라는 신원을 인정한 그 결과다.

### out-of-thin-air — JMM이 *허용하지 않는* 한 가지

JMM의 행동 정의에는 한 가지 묘한 구멍이 있다. 순수 happens-before 모델은 *허공에서 솟아난 값(out-of-thin-air, OOTA)*을 허용해 버린다는 점이다. 예를 들어 두 스레드가 서로의 변수를 읽어 자기 변수에 쓴다고 해보자. 만약 둘 다 "상대가 42를 쓸 거니까 나도 42를 쓰자"고 *예측*해서 정합성 있게 끝맺는 실행이 존재한다면, happens-before만으로는 이를 금지하지 못한다.

물론 실제 JVM은 OOTA 값을 만들지 않는다. JMM 명세는 happens-before 위에 **causality requirements**라는 별도의 well-formed execution 정의를 얹어 이런 실행을 *명시적으로 배제*한다. 실무 개발자가 이 사실을 매일 의식할 필요는 없다 — 그러나 메모리 모델 명세가 그저 happens-before 한 줄로 끝나지 *않는다는* 사실은 기억해두자. 동시성은 직관보다 깊다.

### j.u.c — Doug Lea가 세운 도시

JMM이 *문법*이라면, `java.util.concurrent`는 그 문법으로 지어진 *도시*다. 2004년 Java 5에 JSR 166으로 도입된 이래, Doug Lea를 비롯한 EG는 모든 락·큐·실행자·atomic·sync 도구를 *JMM 위에서 안전한 형태로* 구현해 두었다. 우리가 더 이상 `wait/notify`를 직접 만질 일이 없는 이유다.

**Atomic 패키지** — `AtomicInteger`, `AtomicLong`, `AtomicReference`. CAS(compare-and-swap) 명령어 한 번으로 read-modify-write를 원자화한다. `count.incrementAndGet()`은 위에서 본 `count++`의 깨진 버전을 한 줄로 고친다. 내부적으로는 `Unsafe.compareAndSwapInt` 호출이며, 실패 시 spin retry한다. Java 8에서 `LongAdder`·`LongAccumulator`가 추가됐는데, *많은 스레드의 누적 합산*에서 `AtomicLong`을 한참 앞서는 성능을 보인다. 핵심 차이는 *셀 분산*이다 — 단일 변수가 아니라 스레드별 셀에 누적해 두고, 읽을 때만 합산한다. 카운터·통계·로깅 누적에는 `LongAdder`를 *기억해두자.*

**락 패키지** — `ReentrantLock`은 `synchronized`의 모든 보장을 그대로 주면서 `tryLock`, `lockInterruptibly`, fair 정책, 다중 `Condition`을 추가로 제공한다. Java 8 이전엔 성능 이점도 있었지만, HotSpot의 biased lock·thin lock 최적화로 `synchronized`도 충분히 빨라졌다. 지금은 *기능적 필요*가 있을 때 `ReentrantLock`을 쓰자.

`ReadWriteLock`은 *읽기 다수, 쓰기 소수*인 캐시류에서 빛난다. 그러나 read 락 자체가 cache line bouncing을 만들기에, 진짜 read-heavy 워크로드에서는 *immutable한 스냅샷 + AtomicReference 교체*가 더 빠를 때가 많다.

Java 8에 추가된 `StampedLock`은 *optimistic read*라는 새 모드를 추가했다 — 락을 잡지 *않고* 읽은 뒤, 끝에서 stamp가 여전히 유효한지만 검증한다. read 비용이 사실상 volatile read 수준이다. 다만 reentrant가 *아니고* `Condition`도 없다. 강력한 무기지만 잘못 쓰면 손가락을 자른다.

**BlockingQueue 계열** — `ArrayBlockingQueue`(고정 크기), `LinkedBlockingQueue`(가변), `SynchronousQueue`(0 용량 핸드오프), `PriorityBlockingQueue`(우선순위), `DelayQueue`(지연 발행), `LinkedTransferQueue`(transfer 시맨틱). Producer-consumer 패턴의 표준 도구다. `put`·`take`는 happens-before를 만든다 — 즉, 큐에 객체를 넣은 시점까지의 모든 쓰기가 꺼낸 쪽에 가시적이다.

**ConcurrentHashMap의 내부 진화** — Java 7까지는 segment lock(16개의 부분 락)이었다. Java 8에서 *완전히 다시 썼다.* 버킷 단위 CAS + `synchronized` block, 충돌이 8개를 넘으면 linked list가 *red-black tree*로 자동 승격(O(n) → O(log n)). `compute`·`merge`·`computeIfAbsent`가 추가됐고, `forEach`·`reduce`·`search`로 병렬 처리가 가능하다. `size()`도 `LongAdder` 스타일로 분산 셀에 누적한다. 옛 segment lock의 read-write 컨텐션 문제가 거의 사라졌다. *모던 자바의 가장 중요한 자료구조 한 가지*를 꼽으라면 이쪽이다.

**동기화 보조 — `CountDownLatch`, `CyclicBarrier`, `Semaphore`, `Phaser`**. 각각 일회용 카운트다운, 재사용 가능한 배리어, 카운팅 세마포어, 동적 단계 진행 도구다. `Phaser`는 다소 복잡하지만, 단계별로 *참가자가 동적으로 변하는* 시뮬레이션·테스트 시나리오에서 강력하다.

### ForkJoinPool과 work-stealing — 그리고 commonPool의 함정

Java 7에서 도입된 `ForkJoinPool`은 *분할 정복형 CPU-bound 작업*을 위한 풀이다. 각 워커 스레드가 자기 deque를 갖고, deque가 비면 *다른 워커의 deque 꼬리를 훔쳐* 일을 가져온다(work-stealing). idle 워커가 알아서 짐을 나누니, 작업 분배 로직을 짤 필요가 없다. `RecursiveTask`·`RecursiveAction`을 상속해서 `compute()`에 분할 로직을 적으면 끝이다.

그리고 Java 8에서 `ForkJoinPool.commonPool()`이라는 *전역 공용 풀*이 도입됐다. 기본 스레드 수는 `availableProcessors() - 1`. 이 풀은 다음 세 가지가 *모두* 공유한다.

- `parallelStream()`
- `CompletableFuture.supplyAsync(...)`의 *executor 인자 없는 호출*
- `ForkJoinPool.commonPool().submit(...)`

여기서 *끔찍한 일이* 시작된다. 가령 이런 코드를 보자.

```java
ordersStream.parallel()
    .map(order -> paymentClient.charge(order)) // HTTP 호출, blocking
    .toList();
```

이 코드는 *commonPool에 blocking I/O를 태운다.* 워커가 HTTP 응답을 기다리는 동안 풀은 비어 있고, 같은 JVM의 다른 모든 `parallelStream`·`CompletableFuture`가 *함께 굶는다.* p99 latency가 일정하지 않게 폭주하는 흔한 원인이다. 이 사실을 모르는 팀은 "왜 parallelStream을 켰는데 더 느려졌지?"를 반나절 헤매다 결국 `parallel()`을 떼는 것으로 끝난다.

해법은 단순하다. **commonPool에는 CPU-bound 작업만 태우자.** Blocking I/O는 별도의 풀 — `Executors.newFixedThreadPool` 또는 (Loom 시대라면) virtual thread per task executor — 로 보낸다. `CompletableFuture`라면 *항상 executor를 명시적으로 지정*하는 편이 낫다. 그게 안전하다.

여기서 한 가지 미리 짚어두자. 이 모든 풀과 락의 *진짜 가치*는 Part VII의 Loom 시대에 다시 따져봐야 한다. virtual thread가 *thread-per-request*를 다시 합리적으로 만든 순간, "thread pool은 비싸니까 재사용해야 한다"는 11년의 통념이 흔들리기 시작한다. 그러나 지금은 그 이전의 세계를 정직하게 마주하는 일이 먼저다.

### Spring 맥락 — 1차 캐시와 ThreadLocal

JPA의 `EntityManager`는 thread-safe하지 *않다.* 1차 캐시(영속 컨텍스트)는 단일 스레드에 *confined*된다는 전제다. Spring의 `OpenEntityManagerInView` 패턴은 요청 스레드에 `EntityManager`를 묶어두는 것으로 이 전제를 지킨다. `@Transactional` 메서드의 가시성 보장도 같은 토대 위에 있다 — 트랜잭션 진입과 종료가 JDBC connection의 commit/rollback에 묶이고, JDBC 드라이버가 그 시점에서 가시성을 만들어 준다.

`@Scope("prototype")`과 `singleton`의 차이도 이 맥락에서 다시 보자. singleton Bean이 *상태를 들고 있다면* 자동으로 멀티 스레드에 노출된다. 그 상태가 *가변*이라면 동기화가 필요하다. 가장 흔한 함정은 `private SimpleDateFormat sdf`를 singleton 서비스 Bean에 박아두는 일이다. `SimpleDateFormat`은 thread-safe하지 않다. `DateTimeFormatter`(Java 8, immutable)로 바꾸자 — 그게 *훨씬 낫다.*

ThreadLocal Bean도 한 번 들여다볼 만하다. ThreadLocal은 thread-confined를 강제해 가시성 문제를 회피하는 도구지만, 자체로 *위험한 도구*다. 풀에서 재사용되는 스레드에 ThreadLocal이 남아 있으면, *다음 요청이 이전 요청의 상태를 본다.* Spring Security의 `SecurityContextHolder`가 잘 알려진 사례 — request 끝에 반드시 `clear()`해야 한다. virtual thread 시대에는 이 패턴 자체가 흔들린다는 점도 *기억해두자.* Scoped Values라는 후속 도구가 16장에서 등장한다.

### 마무리

이 장에서 우리는 자바 동시성의 *문법책*을 펼쳤다. happens-before라는 단 하나의 관계가 volatile·synchronized·final·Thread.start·Thread.join을 한 줄로 묶고, j.u.c의 모든 도구가 그 문법 위에서 안전하게 작동한다는 사실을 확인했다. CAS·work-stealing·tree-bin 같은 구현 기법들도 결국 happens-before를 깨지 않으면서 성능을 회복하는 도구들이었다.

이제 문법은 갖춰졌다. 그러나 비동기 *조합*은 또 다른 이야기다. 외부 API 세 개를 *병렬로* 호출하고, 그중 하나가 실패했을 때 우아하게 복구하고, 그 결과를 다시 *순차적으로* 합쳐 클라이언트에 돌려주는 일 — `Future` 하나로는 어림없다. 다음 장에서는 `CompletableFuture`가 어떻게 콜백 지옥에서 우리를 꺼냈고, Java 9의 `Flow`가 어떻게 그 흐름을 또 한 번 일반화했는지 살펴보자. 그 끝에서 우리는 Reactive Streams라는 이름의 길고 험한 산을 만난다.

---

## 8B장. CompletableFuture와 Reactive Streams Flow — 비동기 조합의 두 갈래

외부 API 세 개를 합쳐야 하는 컨트롤러를 받았다고 해보자.

요구사항은 단순해 보였다. 결제 게이트웨이 A, 적립 포인트 시스템 B, 배송 추적 시스템 C에 각각 주문 정보를 보내고, 세 응답을 한 데 묶어 클라이언트에 돌려준다. 각각 평균 200ms씩 걸리니, 순차로 호출하면 p50이 600ms를 넘는다. 병렬로 돌리면 200ms대에 떨어질 텐데, 그 *병렬*을 어떻게 짤 것인가가 문제다. 일주일 전 같은 작업을 했던 동료의 코드를 열어보면, 이런 게 있다.

```java
ExecutorService es = Executors.newFixedThreadPool(3);
Future<PaymentResult> f1 = es.submit(() -> paymentClient.charge(order));
Future<PointResult> f2 = es.submit(() -> pointClient.accrue(order));
Future<ShippingResult> f3 = es.submit(() -> shipClient.track(order));
PaymentResult r1 = f1.get(2, TimeUnit.SECONDS);
PointResult r2 = f2.get(2, TimeUnit.SECONDS);
ShippingResult r3 = f3.get(2, TimeUnit.SECONDS);
return new OrderResponse(r1, r2, r3);
```

병렬은 됐다. 그러나 *찜찜하다.* 첫째, `Future.get()`이 줄줄이 blocking이다. 둘째, 셋 중 하나만 실패해도 나머지를 *우아하게* 취소하는 방법이 없다. 셋째, 결제 결과가 도착하자마자 *그것만 가지고* 적립 비율을 계산하는 식의 *조합*은 어림도 없다. 넷째, 타임아웃·재시도·fallback을 합쳐 짜다 보면 `try-catch`와 `Future`가 뒤엉켜 가독성이 무너진다.

`Future`가 잘못 설계된 건 아니다. Java 5에서 비동기의 *최소한*을 표현하기 위해 만든 도구일 뿐이다. 그러나 *조합*까지 가려면 다른 도구가 필요했다. Java 8의 `CompletableFuture`가 그 다음 단계였고, Java 9의 `Flow`가 또 한 번의 일반화였다. 이 장에서는 콜백 지옥에서 우리가 어떻게 빠져나왔고, *그 다음은 무엇이었는지*를 따라가 본다. 그리고 솔직히 인정하자 — Reactive Streams는 *왜 그렇게 어려웠을까?*

### Future의 한계와 CompletableFuture의 도착

`Future`의 결정적 한계는 두 가지다. **콜백을 등록할 수 없다** — 결과가 준비되면 무엇을 할지를 *미리 적어둘* 방법이 없다. **조합할 수 없다** — 여러 Future를 묶거나, 한 Future의 결과를 다음 Future의 입력으로 보낼 *언어 도구*가 없다. 결국 `get()`으로 막아서서 받는 수밖에 없는데, 그 순간 비동기의 가치가 절반은 사라진다.

Java 8에서 도입된 `CompletableFuture<T>`(이하 CF)는 이 두 한계를 정면으로 깬다. CF는 `Future`이면서 동시에 *`CompletionStage`* 다. 즉, 결과가 준비되면 *다음 단계*를 자동으로 트리거하는 비동기 파이프라인의 한 마디다. 메서드가 50개를 넘는다. 처음 보면 압도된다. 그러나 분류하면 의외로 단순하다 — 세 축이다. **무엇을** 할 것인가(consume·transform·combine), **어디서** 실행할 것인가(같은 스레드 vs 다른 스레드), **예외**가 났을 때 어떻게 할 것인가.

도입 코드를 위 시나리오로 다시 써보자.

```java
CompletableFuture<PaymentResult>  cf1 = CompletableFuture.supplyAsync(() -> paymentClient.charge(order), httpExecutor);
CompletableFuture<PointResult>    cf2 = CompletableFuture.supplyAsync(() -> pointClient.accrue(order),   httpExecutor);
CompletableFuture<ShippingResult> cf3 = CompletableFuture.supplyAsync(() -> shipClient.track(order),     httpExecutor);

CompletableFuture<OrderResponse> result =
    CompletableFuture.allOf(cf1, cf2, cf3)
        .thenApply(__ -> new OrderResponse(cf1.join(), cf2.join(), cf3.join()));
```

`allOf(...)`가 세 작업을 묶어준다. `thenApply(...)`로 결과 변환을 *콜백*으로 등록한다. `get`도 `try-catch`도 없다. *훨씬 낫다.*

### thenApply · thenCompose · thenCombine — 헷갈리는 세 친척

CF의 메서드 중 가장 자주 손에 잡는 세 가지를 정확히 구분해보자. 셋은 비슷해 보이지만 *완전히 다른 일*을 한다.

`thenApply(Function<T, U>)` — 결과 `T`를 받아 `U`로 변환한다. 동기 함수다. 입력 `Function`은 *값*을 반환한다.

`thenCompose(Function<T, CompletionStage<U>>)` — 결과 `T`로 *또 다른 CF*를 만들어 그것이 끝나기를 기다린다. 함수가 *CF*를 반환한다. *flat-map*에 해당하는 연산이다 — Optional·Stream의 `flatMap`과 *철학이 같다.* 비동기 호출의 *체인*을 짤 때 쓴다.

```java
fetchUserId(req).thenCompose(this::fetchUser).thenCompose(this::fetchUserOrders);
// fetchUser, fetchUserOrders가 각각 CompletableFuture를 반환
```

`thenCombine(CompletionStage<U>, BiFunction<T, U, R>)` — *두 CF의 결과*가 모두 도착하면 결합 함수를 실행한다. zip에 해당한다.

이 셋을 구분하지 못하면 `thenApply` 안에서 또 비동기 호출을 호출하다 *동기 블로킹*이 발생하거나, `thenCompose`를 써야 할 자리에 `thenApply(... -> someAsync())`를 두어 *CF가 한 겹 더 감싸진* 채로 흘러가 버린다. 후자는 `CompletableFuture<CompletableFuture<Result>>`라는 *난감한* 타입을 만든다. *기억해두자* — 단계 함수가 *값*을 반환하면 `thenApply`, *CF*를 반환하면 `thenCompose`다.

`thenAccept`(consume, 반환 없음), `thenRun`(인자도 없음, 단순 실행)도 같은 가족이다. 모두 `Async` 접미사 변형이 있다 — `thenApplyAsync`처럼. 접미사가 *있으면* 다음 단계를 별도 executor에서, *없으면* 직전 단계를 실행한 스레드에서 그대로 이어 실행한다.

### handle · exceptionally · whenComplete — 예외 전파의 세 모양

비동기 파이프라인에서 예외는 *다음 단계로 전파*된다. 마치 Stream의 short-circuit처럼 — 예외가 한 번 발생하면 그 뒤의 `thenApply`·`thenCompose`는 *모두 건너뛰고* 끝까지 흘러간다. 그 흐름의 어디서 예외를 *받아 처리*할지가 세 메서드의 차이다.

`exceptionally(Function<Throwable, T>)` — 예외가 났을 때만 호출돼 *대체 값*을 만든다. 정상 흐름은 통과시킨다. fallback에 가장 적합하다.

```java
fetchFromPrimary().exceptionally(ex -> fetchFromCache(ex)); // ex로 fallback
```

`handle(BiFunction<T, Throwable, R>)` — 정상이든 예외든 *둘 다*를 보고 결과를 만든다. 둘 중 하나는 null이다. 흐름을 *항상* 정상으로 되돌린다.

`whenComplete(BiConsumer<T, Throwable>)` — 정상/예외 *둘 다* 호출되지만 결과를 *바꾸지 못한다.* 로깅·메트릭·정리 작업용이다. 예외는 *그대로* 다음 단계로 흘러간다.

세 가지를 한 줄로 정리하자. **처리만** 하고 흐름은 그대로: `whenComplete`. **대체 값**으로 복구: `exceptionally`. **둘 다 보고 변환**: `handle`. 흔한 실수가 `whenComplete`로 예외를 *소비했다고 착각*하는 일이다. 소비된 게 아니다. 다음 `.thenApply`는 *여전히* 건너뛴다. *기억해두자.*

Java 12에서 `exceptionallyCompose`가 추가됐다. `exceptionally`의 *flat-map* 버전이다 — fallback이 또 다른 비동기 호출일 때 쓴다.

### Executor를 명시하는 일 — commonPool에 blocking I/O를 태운 *끔찍한 사건*

CF에는 `Async` 접미사 메서드들이 있다. `supplyAsync`·`thenApplyAsync`·`thenComposeAsync` 등이다. *executor 인자를 생략하면* 기본값은 `ForkJoinPool.commonPool()`이다. 8A장에서 본 그 commonPool 말이다.

여기서 *잊지 못할 사건*이 발생한다. 어느 팀의 결제 컨트롤러 — 외부 결제 게이트웨이 호출을 `CompletableFuture.supplyAsync(...)`로 감쌌다. 각 호출은 평균 300ms의 HTTP I/O. 동시 처리 30 RPS. 컨트롤러 자체는 *완벽하게* 동작했다. 그런데 같은 JVM의 *다른* 엔드포인트들이 이상하게 느려졌다. `parallelStream`을 쓰던 리포트 생성 API의 p99가 갑자기 8초를 넘었고, 캐시 갱신 잡이 *대기열에서 사라지지 않고* 쌓이기 시작했다.

원인은 단순했다. 결제 호출이 commonPool의 워커들을 *blocking으로 점유*했고, 그 풀을 함께 쓰는 다른 모든 작업이 *함께 굶었다.* commonPool의 기본 크기는 코어 수 - 1. 16코어 머신에서 15개의 워커가 모두 HTTP 응답을 기다리고 있으면, 새 작업은 무한히 대기한다. *끔찍한 일이다.*

해법은 *항상 executor를 명시하는 것*이다. 다음 코드 한 줄이 규율을 만든다.

```java
private static final ExecutorService HTTP_POOL =
    Executors.newFixedThreadPool(64, r -> Thread.ofPlatform().name("http-", 0).unstarted(r));
// ...
CompletableFuture.supplyAsync(() -> client.call(req), HTTP_POOL);
```

I/O bound 작업은 *I/O 전용 풀*에, CPU bound 작업은 *코어 수 기준 풀*에, 그리고 Loom 시대에는 *virtual thread per task executor*에 — 이 셋을 *기억해두는 편이 낫다.* commonPool은 짧은 CPU bound 작업, 그리고 명시적으로 안전한 곳에만 쓰자.

### allOf · anyOf — 다수 결합의 두 모양

`allOf(CompletableFuture... cfs)`는 *모두* 완료될 때 끝난다. 결과 타입은 `CompletableFuture<Void>`다 — 각 CF의 결과는 *따로 꺼내야* 한다. 위 도입 예제가 정확히 이 패턴이다.

`anyOf(CompletableFuture... cfs)`는 *하나라도* 완료되면 끝난다. 결과 타입은 `CompletableFuture<Object>`. 빠른 응답을 우선하는 미러링·캐시 hedging에 쓴다.

타임아웃은 Java 9에서 추가된 `orTimeout(duration, unit)`과 `completeOnTimeout(value, duration, unit)`로 깔끔해진다. 이전엔 `ScheduledExecutorService`로 손수 만들어야 했다.

```java
fetchUser(id)
    .orTimeout(1, TimeUnit.SECONDS)
    .exceptionally(ex -> User.guest()); // 1초 넘으면 guest로
```

### Executor·ExecutorService·ScheduledExecutorService — 실행자의 세 층

CF의 *어디서* 실행되는가에 대한 답은 결국 `Executor` 인터페이스다. 가장 얇은 상위 타입이 `Executor` — `execute(Runnable)` 하나뿐이다. 그 위에 라이프사이클과 결과 반환을 더한 것이 `ExecutorService`다. `submit`, `invokeAll`, `shutdown`이 여기서 등장한다. 그 위에 시간 기반 예약을 더한 것이 `ScheduledExecutorService` — `schedule`, `scheduleAtFixedRate`, `scheduleWithFixedDelay`다.

`Executors` 팩토리의 메서드들은 모두 한 번씩 정리해두자. `newFixedThreadPool(n)`, `newCachedThreadPool()`, `newSingleThreadExecutor()`, `newScheduledThreadPool(n)`, 그리고 Java 8의 `newWorkStealingPool()`(= `ForkJoinPool`), Java 21의 `newVirtualThreadPerTaskExecutor()`까지. 각각 *서로 다른 워크로드의 모양*을 가정한다. CPU bound인지, I/O bound인지, 짧은 작업의 폭주인지, 주기적 잡인지에 따라 고르자.

`Executors.newCachedThreadPool()`은 한 가지 *함정*이 있다. 큐가 `SynchronousQueue`라서 작업이 들어오면 *무조건 새 스레드를 만든다.* 폭주 시 *수만 개* 스레드를 만들어 OOM을 띄울 수 있다. 알 수 없는 입력 부하 앞에서 이건 무방비다. 운영에선 `newFixedThreadPool` 또는 *명시적 `ThreadPoolExecutor` 빌드*가 더 안전하다.

### ForkJoinPool과 work-stealing의 자리

8A장에서 한 번 짚었지만, 여기서 한 번 더 정리하자. `ForkJoinPool`은 *분할 정복형 CPU bound 작업*에 최적화된 풀이다. 워커마다 자기 deque를 갖고 idle 워커가 다른 워커의 꼬리를 *훔친다.* `RecursiveTask`를 상속해 `compute()`에 base case와 분할 로직을 적으면 끝이다.

`parallelStream()`이 commonPool 위에서 동작한다는 점은 이미 보았다. CF의 `*Async` 메서드 *executor 생략 시* 기본값도 commonPool이다. 한 JVM 안에서 *이 둘이 같은 풀을 공유한다는 사실*을 잊지 말자. 부하가 큰 두 도구를 한 풀에 동시에 풀어놓으면 *예측 불가의 대기*가 따라온다. 풀을 *분리*하는 편이 낫다.

### Java 9 — `Flow`라는 인터페이스 4종

Java 9는 `java.util.concurrent.Flow`라는 *클래스 한 개*를 새로 도입했다. 그 안에 *static 인터페이스 네 개*가 들어 있다. `Publisher`, `Subscriber`, `Subscription`, `Processor`다. JEP 266이다. 이게 자바판 **Reactive Streams**의 표준 인터페이스다.

왜 이게 *언어 표준*에 들어와야 했는가? 2010년대 중반, RxJava·Reactor·Akka Streams·Vert.x 등 여러 reactive 라이브러리가 각자 다른 인터페이스로 *호환되지 않는* 비동기 스트림을 표현하고 있었다. 라이브러리 사이를 *흐름 단위*로 연결하려면 표준이 필요했다. 2013년 시작된 *Reactive Streams Initiative*가 그 표준을 만들었고, Java 9가 그 인터페이스를 *언어 표준 라이브러리*로 끌어들였다. 이제 Reactor의 `Flux`, RxJava의 `Flowable`, MongoDB·Cassandra·R2DBC의 비동기 드라이버가 *모두 같은 인터페이스*로 서로를 받아들인다.

네 인터페이스의 모양은 단순하다.

```java
interface Publisher<T> { void subscribe(Subscriber<? super T> s); }
interface Subscriber<T> {
    void onSubscribe(Subscription s);
    void onNext(T item);
    void onError(Throwable t);
    void onComplete();
}
interface Subscription { void request(long n); void cancel(); }
interface Processor<T,R> extends Subscriber<T>, Publisher<R> {}
```

핵심은 **네 신호**다 — `onSubscribe`, `onNext`, `onError`, `onComplete`. 그리고 결정적으로 `Subscription.request(long n)` — *구독자가 발행자에게 N개를 요청*한다. 이것이 backpressure다.

### backpressure — Reactive가 *어려웠던* 진짜 이유

backpressure를 한 문장으로 설명하면 이렇다. **소비자가 감당할 수 있는 만큼만 생산자에게 요청한다.** 전통적 push 모델에서는 생산자가 무한히 토하면 소비자가 OOM으로 죽거나 큐가 폭주한다. pull 모델은 응답성을 잃는다. Reactive Streams는 그 중간 — *demand-driven push* — 을 택한다. 생산자는 *요청받은 만큼만* push한다. 적정량의 prefetch와 buffer는 구현 측의 자유로 남는다.

이게 *왜 그렇게 어려웠을까?* 세 가지가 겹쳤다.

첫째, *모든 단계*가 비동기·non-blocking이라는 약속을 지켜야 한다. 한 단계라도 blocking이면 전체가 무너진다. JPA의 동기 API, JDBC의 blocking 호출이 reactive 체인 안에 섞이는 순간 — *끔찍한 일이다.* 이게 reactive 도입의 가장 흔한 좌초점이었다.

둘째, *디버깅이 어렵다.* 스택 트레이스가 의미를 잃는다. 람다 체인 안에서 예외가 발생하면 어디서 났는지를 찾아 거슬러 올라가는 일이 가설을 동반한 추리가 된다. Reactor는 `Hooks.onOperatorDebug()` 같은 도구를 제공하지만, 그 자체가 *별도의 학습*이다.

셋째, *추상화의 거리가 멀다.* `map`·`filter`·`flatMap`까지는 익숙하지만, `concatMap`·`switchMap`·`mergeMap`·`window`·`groupBy`·`publishOn`·`subscribeOn`의 차이를 정확히 익히기까지 *몇 달*이 걸린다. 코드 한 줄을 잘못 고르면 *순서가 무너지거나*, *쓰레드가 이동하지 않거나*, *backpressure가 풀려버린다.*

그래서 우리는 자주 묻는다. "그래서 — 그 학습 곡선을 넘어설 만한 *고유한* 가치가 어디에 있는가?" 이 질문의 답은 *지금* 짧게 하기 어렵다. Loom이라는 새로운 패러다임이 등장한 이후 그 답이 *흔들리고 있다*는 사실까지 함께 보아야 정직한 답이 된다. 그 정리는 14장 이후, 그리고 21장의 "WebFlux 유지 시나리오"에서 본격적으로 따져본다. 이 장에서는 *도구의 모양*까지만 가져가자.

### Project Reactor·RxJava와 Flow의 관계

자바 표준의 `Flow`는 *인터페이스*만 정의한다. *연산자*는 없다. `map`·`filter`·`flatMap` 같은 *그 풍성한 컬렉션*은 모두 Reactor나 RxJava 같은 *라이브러리*가 제공한다. Flow는 그 라이브러리들이 *서로 호환되도록* 약속한 *호환 layer*다.

Reactor의 `Flux`·`Mono`는 0~N개·0~1개 비동기 시퀀스를 표현한다. Spring WebFlux의 토대다. `Mono`는 사실상 *single-element Flux*이며, `CompletableFuture`와 *형태가 비슷하지만* 본질적으로 *lazy*하다 — 누군가 `subscribe`하기 전에는 아무것도 실행되지 않는다. CF는 *eager*하다 — `supplyAsync` 호출 시점에 즉시 시작된다. *이 차이는 작지 않다.*

RxJava의 `Observable`·`Flowable`도 같은 자리에 있다. `Observable`은 backpressure 없는 흐름, `Flowable`은 backpressure 있는 흐름이다. 둘 다 Flow의 `Publisher`로 변환 가능하다 — `Flowable.toFlowable()`은 곧 reactive-streams `Publisher`이고, 그 인터페이스가 곧 `Flow.Publisher`다(JDK 9에서 어댑터 한 줄로 연결).

### HttpClient의 비동기 호출 — Java 11의 한 가지 점

Java 11에서 JEP 321로 표준화된 `java.net.http.HttpClient`는 *비동기 API를 처음부터* 갖춘 자바 표준의 HTTP 클라이언트다. `sendAsync(...)`는 `CompletableFuture<HttpResponse<T>>`를 반환한다. 더 나아가 body publisher·subscriber는 `Flow.Publisher`·`Flow.Subscriber`로 모델링된다 — *body를 reactive 스트림으로 받을 수 있다.*

```java
HttpClient client = HttpClient.newBuilder().version(Version.HTTP_2).build();
client.sendAsync(req, BodyHandlers.ofString())
      .thenApply(HttpResponse::body)
      .thenAccept(System.out::println);
```

Apache HttpClient·OkHttp에 대한 자바 표준의 답이다. 단, 풍성한 미들웨어·인터셉터 생태계는 여전히 별도 라이브러리가 채운다. 마이그레이션 맥락에서 이 클라이언트가 어떤 자리에 서는지, RestClient·WebClient와 어떻게 비교되는지는 20장과 21장에서 본격적으로 다시 따져본다. 이 장에서는 *Java 8 이후 동시성 API가 어떻게 진화했는가*의 한 점으로 짚어두자.

### Spring 맥락 — `@Async`·`Mono`/`Flux`·WebClient

Spring의 `@Async`는 가장 익숙한 비동기 도구다. 메서드에 붙이면 *기본 TaskExecutor*가 그 호출을 별도 스레드에서 실행한다. 반환 타입을 `CompletableFuture<T>`로 두면 호출자가 *조합 가능한* 비동기 결과를 받을 수 있다. 단, *Bean 외부에서 호출*해야 프록시가 적용된다는 함정 — 같은 클래스 내 메서드 호출은 `@Async`가 *동작하지 않는다.* AOP 기반 도구의 공통된 한계다.

Spring WebFlux는 `Mono<T>`·`Flux<T>`를 컨트롤러 반환 타입으로 받는다. Reactor 위에 세워진 서버 스택 — Netty 기반, non-blocking, demand-driven. 도구 자체는 강력하다. 그러나 *전체 스택이 non-blocking이어야* 비로소 의미가 있다. JDBC·JPA가 끼는 순간 그 약속은 깨진다(R2DBC가 그 빈자리를 메우려 했지만, JPA 생태계의 무게에 비해 *얇다*).

`WebClient`는 reactive HTTP 클라이언트다. `client.get().uri(...).retrieve().bodyToMono(User.class)` 같은 체인이 *지연 실행 reactive 흐름*을 만든다. CF와 다르게 *subscribe 전에는 실행되지 않는다.* `.block()`을 호출하면 동기처럼 변하지만, *그 순간 reactive의 모든 장점이 사라진다.* 그래서 우리는 *함부로 `.block()`을 부르지 않는다 —* 기억해두자.

`@Async` + `CompletableFuture`와 reactive + `Mono`/`Flux`는 *서로 다른 패러다임*이다. 둘 사이의 변환도 가능하지만(`Mono.fromFuture`, `Mono.toFuture`), 두 모델을 *한 컨트롤러 안에서 자유롭게 섞는 일*은 좋지 않은 결과를 낳는다. 일관성을 유지하자.

### 마무리

이 장에서 우리는 비동기 *조합*의 두 갈래를 함께 걸었다. `Future`의 단순한 약속에서 `CompletableFuture`의 풍성한 조합 연산자로, 그리고 다시 `Flow` 인터페이스가 표현하는 *demand-driven push*로. 한 갈래는 *값 중심*의 비동기다 — 작업 하나의 결과를 깔끔히 조합한다. 다른 한 갈래는 *흐름 중심*의 비동기다 — 0개에서 무한 개의 신호가 backpressure와 함께 흘러간다. 둘은 다른 도구가 아니라 *다른 추상화의 층*이다.

그리고 한 가지 정직하게 인정하고 가자. 이 장의 도구들은 모두 *Loom 이전*의 답이다. virtual thread가 *thread-per-request*를 다시 합리적으로 만든 이후, "왜 굳이 reactive로 짜야 하는가?"라는 질문은 *전제 자체가 흔들린* 자리에 서 있다. 14장에서 Loom을 만나고, 21장에서 WebFlux 유지 시나리오를 따져본 다음에 비로소 *이 모든 도구의 진짜 가치*를 다시 평가할 수 있다. 지금은 두 갈래의 풍경을 *기억해두는 편이 낫다.* 도구가 바뀌어도, 비동기 조합의 *어휘*는 같은 자리에 남아 있을 것이다.

이제 동시성의 첫 막은 닫힌다. 다음 Part는 언어 표면의 진화 — JPMS와 `var`·switch·text blocks가 우리 코드의 *색깔*을 어떻게 바꿔놓았는지부터 다시 시작하자.

---

# Part V. 언어 표면의 진화 (Java 9 ~ Java 23)

Java 9부터 23까지 — 14년이 아니라 *6년 반* — 사이에 자바의 *언어 표면*에는 작고 많은 변화가 쌓였다. JPMS, `var`, switch expressions, text blocks, Sequenced Collections, Markdown javadoc, String Templates의 좌초까지. 어느 하나도 람다나 records만큼의 "사건"은 아니다. 그러나 이 작은 변화들이 모이면, *코드 한 줄을 적을 때의 호흡*이 완전히 달라진다.

9장은 JPMS — 가장 야심찼고 가장 논쟁적이었던 변화 — 를 정면에서 본다. Java 9의 출시를 3년 지연시킨 그 거대한 기능이 *왜* 그렇게 설계됐는지, *왜* 우리가 결국 `module-info.java`를 잘 쓰지 않게 됐는지, 그리고 *그럼에도 불구하고* JPMS가 JDK 내부에서 어떤 일을 하고 있는지를 본다. 실패도 미완도 아닌, *이상한 중간 상태*에 자리 잡은 한 변화에 대한 정직한 평가다.

10장은 작지만 결정적인 변화들의 모음이다. `var`가 정말 가독성을 떨어뜨리는지, switch expressions가 *어떻게* statement에서 expression으로 옮겨가며 *값을 반환하는 것의 자연스러움*을 가져왔는지, text blocks가 SQL과 JSON을 적을 때의 *번거로움*을 어떻게 줄였는지, Sequenced Collections(Java 21)가 `LinkedHashMap`의 첫 키를 꺼내는 일에 11년 걸린 *이상한 빈자리*를 어떻게 메웠는지, 그리고 — String Templates가 왜 *좌초*했고 그 자리에 무엇이 들어올지를 함께 본다.

이 두 장은 책의 후반부에 깔리는 *코드의 호흡*을 결정한다. Part VI의 records와 Part VII의 virtual thread 코드 예제 모두 `var`와 switch expressions와 text blocks를 자연스럽게 사용한다. 작은 변화가 모여 큰 코드의 모양을 만든다는 사실을 함께 느껴보자.

---

## 9장. JPMS — 실패인가 미완인가

새 라이브러리를 의존성에 추가했더니 빌드는 통과하는데 런타임에 갑자기 `IllegalAccessError`가 떨어졌다고 해보자. 메시지는 친절하지 않다. "module java.base does not export sun.nio.ch to unnamed module" 같은 한 줄을 보고, 우리는 `--add-opens`라는 마법 주문을 검색창에 입력한다. 한참을 헤매다 `pom.xml`에 `<argLine>`을 한 줄 더 박고 나서야 빌드가 다시 살아난다. 누가 봐도 *번거롭다*.

그런데 그 에러 메시지의 출처가 어디인가? *모듈 시스템*이다. 정확히는 Java 9가 도입한 JPMS — Java Platform Module System. 우리는 `module-info.java`를 한 줄도 쓰지 않는데, 모듈 시스템은 우리 코드의 발목을 잡는다. 이 모순이 9장의 출발점이다.

왜 우리는 `module-info.java`를 쓰지 않게 됐을까? 그리고 안 쓰는데도 왜 모듈 시스템의 영향은 계속 받는 것일까? 함께 짚어보자.

### Project Jigsaw — 12년의 야망

JPMS는 2008년 Sun Microsystems가 *Project Jigsaw*라는 이름으로 시작한 작업이다. Java 7에 들어갈 예정이었다가 한 차례 미뤄지고, Java 8 때 또 미뤄지고, 결국 Java 9(2017)에서야 빛을 봤다. 9년이 걸렸다. 자바 역사에서 가장 오래 끌었고, 가장 많이 논쟁된 변경이다.

그 야망은 단순했다. 세 가지를 한꺼번에 해결하고 싶었다.

첫째, **JAR Hell의 종식**. 같은 클래스가 두 개의 JAR에 들어 있을 때 클래스로더가 무엇을 먼저 로드하느냐에 따라 동작이 달라지는 그 끔찍한 상황 말이다. classpath의 순서를 바꿔야 빌드가 통과되는 코드를 만져본 사람이라면 알 것이다. 그게 *split package*다.

둘째, **strong encapsulation**. `sun.misc.Unsafe`나 `com.sun.*` 패키지처럼 *공식이 아닌데도 모두가 쓰는* 내부 API를 막고 싶었다. Brian Goetz의 표현을 빌리자면, "공개 약속이 아닌 것을 공개 약속처럼 의존해 온 거대한 부채"를 청산하고 싶었다.

셋째, **JDK의 슬림화**. `rt.jar` 한 덩어리에 들어 있던 1만 개 넘는 클래스를, 필요한 모듈만 골라 `jlink`로 작은 런타임 이미지로 만들고 싶었다. 50MB짜리 도커 이미지에 자바 앱을 넣자는 꿈이었다.

이 야망을 한 문장으로 말하면 — *자바를 다시 정리하자*. 21년간 쌓인 의존성·캡슐화·배포의 부채를 한꺼번에 청산하자는 것이었다. 그렇게 모듈 시스템이 들어왔다.

### `module-info.java` — 다섯 개의 키워드

모듈을 선언하는 자리는 `module-info.java`라는 특별한 파일이다. 패키지 루트에 두는 한 장의 메타 파일이고, 거기에 다섯 개의 키워드가 들어간다. 살펴보자.

```java
module com.example.order {
    requires com.example.common;
    requires transitive java.sql;
    requires static lombok;

    exports com.example.order.api;
    exports com.example.order.internal to com.example.payment;

    opens com.example.order.entity to org.hibernate.orm.core;

    uses com.example.order.spi.PaymentGateway;
    provides com.example.order.spi.PaymentGateway
        with com.example.order.gateway.TossGateway;
}
```

다섯 가지를 차례로 보자.

**`requires`**는 의존성 선언이다. 다른 모듈을 *컴파일 타임 + 런타임* 둘 다 필요로 한다고 알린다. `transitive`를 붙이면 이 모듈을 의존하는 쪽도 자동으로 그 의존성을 받는다. Maven의 `compile` 스코프와 유사하다. `static`을 붙이면 컴파일 타임에만 필요하다 — Lombok 같은 annotation processor에 쓴다.

**`exports`**는 공개 약속이다. 이 패키지의 `public` 타입을 외부에서 쓸 수 있게 한다. `to`를 붙이면 *qualified export* — 지정한 모듈에만 공개한다. 우리가 친했던 그 표현 "공개 API"가 마침내 컴파일러가 강제하는 약속이 됐다.

**`opens`**는 reflection 허용이다. `exports`는 컴파일 타임 공개고, `opens`는 *런타임 reflection*까지 허용한다. Hibernate가 Entity의 private 필드를 setter 없이 채우려면 reflective access가 필요하니, `opens`를 열어준다. 이게 우리가 매일 마주치는 `--add-opens` 옵션의 정체다.

**`uses`**와 **`provides`**는 `ServiceLoader` 메커니즘을 모듈 시스템 위에 얹은 것이다. SPI 패턴을 언어 차원에서 표현한다고 보면 된다.

언뜻 보면 깔끔하다. *공개 약속*과 *내부 구현*이 컴파일러 수준에서 분리되고, *reflection 허용*은 명시적으로만 가능해진다. JLS의 표현을 빌려보자.

> **JLS §7.7 (Module Declarations)**
>
> *A module declaration specifies a new module, a uniquely named, reusable group of related packages, as well as resources and a module descriptor. A module is the unit of reuse in the modular Java platform.*
>
> 한국어 번역: "모듈 선언은 새 모듈을 명시한다. 모듈은 유일하게 명명된, 관련 패키지들의 재사용 가능한 묶음이며, 리소스와 모듈 기술자(module descriptor)를 포함한다. 모듈은 모듈식 Java 플랫폼에서 재사용의 단위다."
>
> 의미 해설: JLS는 모듈을 *재사용의 단위*로 명확하게 정의한다. 클래스나 패키지가 아닌, 모듈이 *plug-in 가능한 묶음*의 단위라는 선언이다. Java가 21년간 정의해 온 가시성의 단위(public/protected/package-private)에 *모듈 경계*가 한 층 더 얹힌다.
>
> 본문 연결: 이 정의는 다음 절에서 다룰 *strong encapsulation*의 법적 근거다. 모듈이 재사용의 단위라면, *모듈 경계 너머의 internal 코드에 의존하는 것은 약속 위반*이라는 논리가 성립한다.

### strong encapsulation — 우리가 모르는 사이 받은 영향

JPMS가 도입되자 JDK 내부 패키지가 외부에 닫혔다. 이 변화는 자동 모듈을 안 쓰는 사람에게도 직접적인 영향을 줬다. *우리 모두가 받은 영향*이다.

Java 8까지는 `sun.misc.Unsafe`를 그냥 import해서 쓸 수 있었다. 메모리를 직접 만지고, off-heap 버퍼를 직접 할당하고, `volatile` 없이도 메모리 배리어를 강제하고 — 자바답지 않은 어두운 마법을 부릴 수 있었다. Netty, Cassandra, Hadoop, JNA — 이름만 들어도 알 만한 라이브러리가 거의 다 `Unsafe`를 썼다.

Java 9부터 그게 닫혔다. 정확히는 *경고*가 떨어지기 시작했고, Java 16(JEP 396)에서 *기본값 실패*로 바뀌었고, Java 17(JEP 403)에서 *강제 캡슐화*가 default가 됐다. 우리가 라이브러리를 업그레이드하지 않은 채 Java 17로 이주하면, `Unsafe`를 쓰던 트랜시티브 라이브러리 중 하나가 런타임에 폭발한다. 흔한 일이다. *난감하다*.

그렇다면 어떻게 풀어야 할까? 두 가지 길이 있다.

첫째, `--add-opens java.base/sun.nio.ch=ALL-UNNAMED` 같은 JVM 옵션을 박아 캡슐화를 뚫는다. *우회로*다. 안전하지 않고, 다음 LTS에서는 막힐 수 있다고 JEP 문서들이 거듭 경고한다.

둘째, 라이브러리를 업그레이드해 `Unsafe` 의존을 끊은 버전으로 옮긴다. 시간이 걸리지만 *바른길*이다.

흥미로운 점은 — 우리가 `module-info.java`를 한 줄도 안 썼는데도, 모듈 시스템의 *경계 강제*는 그대로 받았다는 사실이다. 이게 JPMS의 정체다. 채택은 선택이지만, 영향은 강제다. 기억해두자.

### 자동 모듈과 unnamed module — 혼란의 자리

채택하지 않는 길을 택했다고 모듈 시스템이 사라지는 건 아니다. classpath에 그냥 던진 JAR도 모듈 시스템 안에서 *어떤 자리*에 배치된다. 그 자리가 두 가지다.

`module-info.java`가 없는 JAR가 **classpath**에 있으면, 그건 *unnamed module*에 속한다. 모든 unnamed module은 하나로 묶여 있고, 그 안에서는 캡슐화가 없다. classpath 옛 시절과 동일하게 동작한다.

같은 JAR가 **module path**(`--module-path`)에 있으면, 그건 *automatic module*이 된다. 모듈 이름은 JAR 파일명에서 추론한다(`spring-context-6.1.0.jar` → `spring.context`). automatic module은 모든 패키지를 자동으로 export하고, 다른 모든 모듈을 자동으로 requires하는 *느슨한* 모듈이다.

이 둘이 섞이면 가시성 규칙이 매우 복잡해진다. *explicit module*은 unnamed module을 requires할 수 없다(unnamed module은 이름이 없으니까). 그래서 *explicit module이 되려면 그 의존성 트리의 모든 라이브러리가 modular 또는 적어도 module path에 올라가 있어야 한다*. 한 줄로 말하면 — *우리 코드만 modular로 만들 수가 없다*. 의존성 트리 전체가 함께 움직여야 한다.

이게 JPMS 채택의 첫 번째 *난감함*이다.

### 2017년 — JCP EC 부결 사건

야망이 컸던 만큼 진통도 컸다. 2017년 5월, JPMS는 한 차례 *부결*됐다. Java Community Process(JCP)의 Executive Committee가 Public Review Ballot에서 13:10으로 반대했다(JSR 376). 자바 표준화 역사상 대단히 이례적인 사건이다.

부결의 주축은 IBM과 Red Hat이었다. 두 곳은 *OSGi*라는 또 다른 모듈 시스템을 십수 년간 운영해 온 진영이다. 그들의 비판은 다음과 같이 요약된다.

- *너무 늦었다.* OSGi가 이미 비슷한 일을 해 왔다. 같은 문제를 두 번 풀 필요가 없다.
- *너무 단순하다.* 버전 관리, 동적 모듈 로딩·언로딩, multi-version coexistence 같은 OSGi의 핵심 기능이 빠졌다.
- *반사(reflection) 모델이 깨졌다.* Hibernate·Spring·Jackson처럼 reflective access에 의존하는 거대 라이브러리가 모두 `opens`를 요구하게 된다.

부결 후 한 달간 추가 협상이 진행됐고, 6월에 수정안이 재투표를 통과해 결국 Java 9에 들어갔다. 그러나 그 한 달의 진통이 시그널이었다. *공동체가 이 변화를 충분히 환영하지는 않았다.* 그 그림자가 그 후 9년간 따라다닌다.

### 왜 안 쓰게 됐을까

Java 9 출시로부터 9년이 지난 지금, 솔직하게 짚어보자. 엔터프라이즈 자바 코드 중 `module-info.java`를 가진 곳을 본 적이 있는가? 거의 없다. Spring 6도 modular jar로 제공되지 않는다. Hibernate도 마찬가지다. Jackson도, Logback도, Apache Commons도 — 우리가 매일 쓰는 라이브러리 대부분이 *automatic module* 자리에 머물러 있다.

왜 그럴까. 네 가지 이유가 있다.

**첫째, 너무 늦었다.** 2008년 야망이 2017년에야 도착했다. 그 사이 Maven과 Gradle이 dependency 문제를 해결했고, OSGi가 캡슐화 문제를 해결했고, Docker가 *런타임 격리* 문제를 해결했다. JPMS가 풀려던 문제 대부분이 *이미 부분적으로 풀려 있었다*. "더 나은 길"을 만들어도 *기존 길에서 갈아탈 인센티브*가 충분히 크지 않다.

**둘째, 라이브러리 생태계의 마찰.** 우리가 modular로 가려면 의존성 트리 전체가 모듈화되어 있어야 한다. 하나라도 unnamed module로 남으면 explicit module이 못 된다. 이건 *치킨-에그* 문제다. 라이브러리들은 사용자가 안 쓰니까 modular로 안 만들고, 사용자는 라이브러리가 modular가 아니라서 못 쓴다.

**셋째, Spring·Hibernate의 깊은 reflection.** Spring의 핵심 메커니즘 중 하나가 *런타임 reflection을 통한 의존성 주입*이다. Hibernate는 *Entity의 private 필드를 setter 없이 채운다*. 두 라이브러리 모두 `opens`를 광범위하게 요구한다. modular 환경에서 이 둘을 쓰려면 거의 모든 도메인 패키지를 `opens`해야 하고, 그러면 *캡슐화의 이득이 거의 사라진다*. 그럴 거면 차라리 classpath 쓰는 게 깔끔하다.

**넷째, 학습 곡선과 에러 메시지.** 처음 `requires`·`exports`·`opens`를 마주친 개발자가 그 차이를 이해하기까지 며칠이 걸린다. 그 와중에 떨어지는 에러 메시지는 *split package*, *uses constraint violation* 같은 자바답지 않은 표현을 동원한다. 학습 비용이 ROI를 압도한다.

이게 *실패론*의 골격이다. 정직하게 인정하자. JPMS는 *애플리케이션 레벨에서는* 실패에 가깝다.

### 그러나 — JDK는 모듈화됐다

물론 실패라고만 부르긴 부당하다. JPMS의 가장 큰 *조용한 성공*은 JDK 자체에 있다.

Java 9 이전 JDK는 `rt.jar` 한 덩어리였다. Java 9 이후는 80개가 넘는 `java.*`·`jdk.*` 모듈로 쪼개졌다. 그 덕분에 다음과 같은 일이 가능해졌다.

`jlink`로 *우리 앱이 진짜 쓰는 모듈만 골라* slim runtime image를 만들 수 있다. 컨테이너 시대에 이게 얼마나 큰 자산인가. 표준 JDK가 300MB인데, `jlink`로 만든 이미지는 50MB까지 줄어든다. AWS Lambda나 GraalVM Native Image 같은 환경에서 이 차이는 *실제 비용*이다.

```bash
jlink --add-modules java.base,java.logging,java.net.http \
      --output myapp-runtime --strip-debug --compress=2
```

`jdeps`로 의존성을 정적으로 분석해 우리 앱이 어떤 JDK 내부 API를 건드리는지 진단할 수 있다.

```bash
jdeps --jdk-internals --multi-release 17 app.jar
```

`jpackage`로 OS-네이티브 인스톨러(Windows .msi, macOS .pkg, Linux .deb/.rpm)를 만들 때, jlink로 만든 runtime을 묶어 배포할 수 있다. 데스크톱 자바 앱이 이렇게 다시 가능해진 데에는 JPMS의 공이 크다.

그리고 무엇보다 — strong encapsulation 덕분에 *Project Loom*, *Project Panama*, *Project Leyden*이 JDK 내부를 자유롭게 재설계할 수 있게 됐다. `Thread`의 내부 구조를 바꾸고, `MemorySegment`로 native interop을 새로 쓰고, AOT 캐시로 클래스 로딩을 재구성하는 일이 — *공개 API를 깨지 않고도* 가능해진 것이다. JDK 내부의 자유는 외부 사용자의 부담을 늘렸지만, 그 부담만큼 JDK는 더 빠르게 진화하고 있다.

이게 *미완론*의 골격이다. JPMS는 *애플리케이션의 도구로는* 실패에 가깝지만, *JDK의 진화 기반으로는* 명백한 성공이다.

### Spring의 우회 — modular jar로 가지 않는 이유

Spring Framework 6과 Spring Boot 3은 Java 17을 베이스라인으로 정했다. 그렇다면 modular jar로 진화하지 않았을까? 답은 — *아니다*. Spring은 의도적으로 modular path를 택하지 않았다. 왜 그럴까.

Spring의 핵심 가치 중 하나는 *유연한 reflection 기반 DI*다. `@Autowired`, `@Configuration`, `@ConditionalOnProperty` — 이 모든 것이 *런타임에 클래스를 들여다보고 결정*하는 메커니즘이다. modular 환경에서 이걸 유지하려면 우리 도메인 패키지 거의 전부를 `opens`해야 하고, 그러면 캡슐화의 이득이 사라진다.

대신 Spring은 *다른 길*을 택했다. **Spring AOT**(Ahead-of-Time processing)다. 빌드 타임에 BeanFactory의 구조를 정적으로 계산해 `BeanDefinition`을 코드로 생성한다. 런타임에는 이미 만들어진 결정 트리를 *읽기만* 한다. reflection이 거의 필요 없어진다.

이걸 *GraalVM Native Image*와 결합하면 *closed-world 가정*에서 동작하는 네이티브 이미지를 만들 수 있다. 시작 시간은 50ms 수준으로 떨어지고, 메모리는 100MB 미만이 되고, JIT compilation 비용은 0이 된다. JPMS가 풀려던 문제 — *런타임 슬림화*와 *내부 캡슐화* — 를, Spring은 *전혀 다른 길*로 풀어버렸다.

이 우회는 우연이 아니다. 큰 프레임워크가 한 차례 다른 길로 갈아타면, 그 생태계 전체가 따라간다. Quarkus도, Micronaut도, Helidon도 — modular jar가 아니라 빌드 타임 처리 + 네이티브 이미지로 갔다. JPMS의 *애플리케이션 레벨 패배*는 이 시점에 결정됐다고 봐도 무방하다.

### JEP 511 — 작은 화해의 신호

그래도 JPMS가 사라지지는 않는다. 오히려 Java 25는 흥미로운 화해의 신호를 보냈다. **JEP 511: Module Import Declarations**(Java 25 표준)다.

기존에는 `import java.util.List; import java.util.Map; import java.util.ArrayList; ...` 같이 한 줄씩 import해야 했다. JEP 511은 *모듈 단위 import*를 가능하게 한다.

```java
import module java.base;

public class Demo {
    public static void main(String[] args) {
        List<String> names = List.of("Toby", "Alice");
        Map<String, Integer> ages = Map.of("Toby", 41);
        System.out.println(names);
    }
}
```

`import module java.base;` 한 줄이면 `java.util.*`, `java.io.*`, `java.lang.*` 등 `java.base` 모듈의 모든 export된 패키지의 public 타입을 쓸 수 있다. 작은 변화지만 의미가 크다. *모듈을 안 써도, 모듈의 존재는 utility로 활용할 수 있다*는 메시지다. JEP 458의 *compact source file*과 결합하면, 스크립트 같은 자바 코드를 더 짧게 적을 수 있다(10장에서 다룬다).

JPMS가 *내부 도구*에서 출발해, 천천히 *입문자의 친구*로 자리를 옮기는 중이라고 봐도 좋다. 12년의 야망이 처음과는 다른 모습으로 살아남고 있다.

### 정리 — 안 써도 부끄러워하지 말자

이 장의 핵심을 다시 정리해보자.

- JPMS는 2008년 시작해 2017년 도착한 *모듈 시스템*이다. JAR Hell·strong encapsulation·JDK 슬림화라는 세 가지를 한꺼번에 풀고자 했다.
- `module-info.java`의 다섯 키워드(`requires`, `exports`, `opens`, `uses`, `provides`)가 모듈 간 관계를 명시한다.
- *애플리케이션 레벨에서는* 거의 채택되지 않았다. 라이브러리 생태계 호환, Spring/Hibernate의 reflection 의존, 학습 곡선이 주요 이유다.
- *JDK 내부에서는* 명백히 성공했다. `jlink`·`jdeps`·`jpackage`로 슬림 배포가 가능해졌고, Loom·Panama·Leyden이 자유롭게 JDK를 재설계할 수 있게 됐다.
- strong encapsulation의 영향은 채택과 무관하게 *모든* 자바 개발자가 받는다. `sun.misc.Unsafe`가 닫히고, 라이브러리들이 그에 적응하는 비용은 우리 모두가 지불했다.
- Spring은 *Spring AOT + GraalVM Native Image* 조합으로 JPMS를 우회했다. 이 우회가 자바 생태계 전체의 방향을 결정했다.

그러니 — 우리 회사 코드에 `module-info.java`가 없다고 부끄러워할 일이 아니다. *대다수가 그렇게 살고 있고*, 그게 합리적인 선택이다. 다만 strong encapsulation의 영향은 외면할 수 없다. Java 17 이상으로 이주할 때 `--add-opens`를 만나면, *그 자리에서 우회로를 박는 대신 라이브러리 업그레이드를 우선 검토*하는 편이 낫다. 기억해두자.

다음 장은 같은 시기의 *훨씬 더 사용된* 변화들을 다룬다. `var`, switch expression, text blocks, sequenced collections — 우리 손가락이 매일 만나는 작은 문법 변화들이다. JPMS가 *못 박힌 야망*이라면, 이쪽은 *조용히 스민 진화*다. 함께 살펴보자.

---

## 10장. `var`·switch·text blocks·Sequenced Collections — 작지만 결정적인 변화

사내 코드 리뷰에서 30자짜리 타입 선언을 매일 적던 동료가 어느 날 한 줄을 이렇게 적었다고 해보자.

```java
var orders = orderRepository.findRecentByCustomer(customerId, since);
```

옆자리 시니어가 어깨를 두드린다. "그 `var`, 가독성 떨어지지 않아? 반환 타입이 뭔지 안 보이잖아." 동료는 잠시 머뭇거리다 IDE의 hover로 타입을 보여준다. "`List<Order>`예요. 메서드 이름에 `findRecentByCustomer`라고 적혀 있고, 변수 이름도 `orders`잖아요."

이 1분짜리 코드 리뷰 안에 *언어 표면 진화의 모든 것*이 들어 있다. 자바는 30년간 *explicit*을 사랑해 온 언어다. 그 언어에 `var`가 들어왔을 때 우리가 느낀 *찜찜함*은 무엇이었나? 한편 같은 시기에 들어온 switch expression, text blocks, sequenced collections는 거의 *논쟁 없이* 받아들여졌다. 왜 같은 시기의 변화인데 환영의 폭이 달랐을까?

이 장에서는 8가지를 함께 살펴본다. `var`, switch expression, text blocks, Sequenced Collections, Markdown Javadoc, String Templates의 좌초, Compact Source / Instance Main, 그리고 마지막으로 — 이 모든 변화의 합주가 만들어내는 *코드의 색깔*까지. 14년치 일상 코드의 피로감을 덜어주는 작은 도구들이다. 하나씩 음미해보자.

### §10.1 `var` — 작아 보이는 변화의 진짜 크기

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

#### `var`가 어울리는 자리

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

#### `var`가 어울리지 않는 자리

반대로 *피해야 할* 자리도 분명하다.

**첫째, 우변이 모호할 때.** `var result = compute();`는 *끔찍하다*. `compute()`의 반환 타입을 IDE 없이는 알 수 없다. PR diff를 보는 동료도, 1년 뒤 같은 코드를 다시 보는 우리 자신도 — 그 자리에서 막힌다.

**둘째, 다이아몬드 연산자와 결합할 때.** `var list = new ArrayList<>();`는 컴파일은 되지만 *추론 결과가 `ArrayList<Object>`*다. 우리가 원한 건 아닐 것이다. 명시적으로 `new ArrayList<User>()`라고 적거나, 좌변에 타입을 적자.

**셋째, 숫자 리터럴.** `var x = 0;`은 `int`다. 그러나 `long`이나 `byte`를 원했다면 명시적으로 적는 편이 낫다.

**넷째, 다이아몬드와 익명 함수가 섞일 때.** `var f = (String s) -> s.length();`는 컴파일 에러다. 람다는 *target type*이 필요한데, `var`는 그걸 줄 수 없다.

**다섯째, 함수형 인터페이스 변환.** `var supplier = () -> 42;`도 같은 이유로 에러다. `Supplier<Integer> supplier = () -> 42;`처럼 명시해야 한다.

#### Java 11의 람다 파라미터 `var`

Java 11에서 한 가지 작은 보완이 들어왔다. 람다 파라미터에도 `var`를 적을 수 있게 됐다(JEP 323).

```java
list.stream()
    .filter((var s) -> s.length() > 5)
    .toList();
```

왜 필요했을까. *애노테이션을 람다 파라미터에 붙이려면 타입이 있어야* 하기 때문이다. `@NonNull String s`처럼 적으려면 타입이 필요하다. 그런데 `var`도 타입의 자리에 올 수 있으므로, `(@NonNull var s) -> ...`가 가능해진 것이다. 자주 쓰는 기능은 아니지만, *문법의 일관성*을 위한 정리다.

#### 가독성 — 도구의 문제인가, 문화의 문제인가

가독성 논쟁의 한가운데로 들어가보자. Java는 30년간 explicit 문화였다. 그 문화 안에서 자란 우리는 `var` 앞에서 *찜찜함*을 느낀다. 이 찜찜함은 정당한가?

JetBrains의 통계(IntelliJ IDEA 사용자 데이터)에 따르면, `var` 사용 비율은 매년 가파르게 늘고 있다. 신규 코드의 30~40% 가까이가 `var`로 작성된다는 조사도 있다. 한편 Java 공식 LVTI Style Guide는 다음을 강조한다.

> *Code is read much more often than it is written. Moreover, it is often read in contexts where the reader does not have ready access to an IDE.* (코드는 작성보다 훨씬 더 자주 읽힌다. 게다가 IDE 없이 읽히는 경우가 많다.)

이 문장의 무게가 크다. PR diff, GitHub 검색 결과, 콘솔 출력, 책에 실린 코드 스니펫 — 이 모든 자리에서 IDE는 없다. 코드는 *그 자체로 자명*해야 한다.

그러니 정리해보자. `var`는 *문법 설탕*이 아니라 *문화적 선택*이다. 팀이 코드 리뷰에서 매번 hover로 타입을 확인하는 일을 *번거롭다*고 느끼지 않는다면 — IDE가 충실히 깔려 있고, 변수 이름이 잘 쓰여 있다면 — `var`를 적극 활용하는 편이 낫다. 반대로 콘솔과 git blame에서 코드를 자주 읽는 팀이라면 explicit 타입이 *친절하다*. 어느 쪽이든, *왜 그렇게 쓰는지*에 대한 팀의 공통 이해가 있는 편이 좋다.

### §10.2 Switch Expression — 한 줄 안에 들어온 결정

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

#### 13장의 디딤돌

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

### §10.3 Text Blocks — 삼중 따옴표의 평화

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

#### incidental whitespace — 들여쓰기의 마법

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

#### `\s`와 `\<newline>` — 두 가지 이스케이프

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

#### Spring 맥락 — `@Query`와 JdbcTemplate

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

### §10.4 Sequenced Collections — 27년 묵은 누락의 마무리

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

### §10.5 Markdown Javadoc — `///`의 등장

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

### §10.6 String Templates의 좌초사

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

### §10.7 Compact Source Files — 자바의 진입 장벽 낮추기

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

### §10.8 같은 함수의 변천사 — Java 8 vs Java 21

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

### 정리 — 작은 변화가 만드는 색깔

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

---

# Part VI. 데이터지향 자바 — Records · Sealed · Pattern

Java 17 LTS의 핵심은 records와 sealed 두 단어로 압축된다. 그리고 Java 21 LTS의 가장 *코드의 모양을 바꾼* 변화는 pattern matching이었다. 이 셋은 따로 떨어진 기능이 아니다. 셋이 묶여 *대수적 데이터 타입(ADT)* 이라는 한 개념을 자바에 들여왔다. Brian Goetz가 *Data-Oriented Programming in Java*에서 그린 그림이 바로 이 셋의 결합이다.

11장은 records로 시작한다. *데이터의 신원* — 같은 필드값을 가진 두 객체는 같은 객체다 — 이라는 단순한 원칙이 11년 자바에서 마침내 일급 시민이 된 사연이다. canonical constructor와 compact constructor의 미세한 문법, `equals`·`hashCode`·`toString`의 자동 생성, immutability, 그리고 — *JPA Entity로는 왜 records가 안 되는지*를 정직하게 짚는다. Lombok과 records의 비교, DTO·Command·Projection에 records를 어떻게 매핑하는지의 사내 가이드라인까지.

12장은 sealed classes — 합 타입(Sum Type)이 자바에 들어온 날이다. enum으로 표현하기에는 너무 풍부하고, interface로 표현하기에는 *닫혀 있다는 것을 표현할 수 없던* 그 회색 지대를 sealed가 정확히 메운다. `PaymentResult`가 `Approved`, `Declined`, `Pending`, `PartialRefund`로 *정확히 그만큼만* 존재한다는 사실을 컴파일러가 알게 되는 순간, 패턴 매칭의 *exhaustiveness 검사*가 가능해진다.

13장은 그 위에서 pattern matching이 ADT를 *풀어내는 도구*가 되는 자리다. `instanceof` 캐스트 사다리 9단을 `switch`의 패턴 한 표현식으로 정리하는 일, record pattern으로 *destructuring*이 가능해지는 일, *nested pattern*으로 도메인 객체를 한 줄에 분해하는 일. 이 셋이 묶여 자바의 코드 한 줄이 완전히 다른 호흡을 갖는다.

11·12·13장이 묶이는 자리에서 자바는 *객체지향과 함수형 사이*의 옛 이분법을 넘어선다. 그 다음 장(14)에서 우리는 이 ADT 위에서 *concurrent 코드를 다시 생각한다*. 데이터지향이 동시성과 만나는 자리가 책의 가장 두꺼운 중심이다.

---

## 11장. Records — 자바가 마침내 인정한 "데이터의 신원"

옆자리 동료가 한숨을 쉬며 IDE를 노려보고 있다고 해보자. 어제는 신이 나서 자랑하던 사람이었다. "이번에 Spring Boot 3.4로 올리면서 DTO를 전부 record로 옮겼다"고. `OrderRequest`, `OrderResponse`, `OrderEvent` 세 개를 한 시간 만에 갈아치우면서 코드 줄 수가 70%로 줄었다고. 그런데 오늘은 표정이 영 좋지 않다. 무슨 일이냐고 물으니, "JPA Entity도 record로 옮기려다가 두 시간을 날렸다"고 답한다.

`Order` 엔티티에 `@Entity` 어노테이션을 붙이고 `record Order(Long id, String status, ...)` 라고 적어보았더니, Hibernate가 `InstantiationException`을 던지더라는 것이다. no-args constructor가 없다고. 그래서 canonical constructor를 비워서 시도해봤더니, 이번엔 `final field`라서 proxy를 못 만든다고 한다. lazy loading은 어떻게 하느냐고 묻기 시작했을 때, 동료는 결국 record 선언을 지우고 클래스로 되돌리고 있었다.

이쯤 되면 한 번쯤 고민하게 된다. **Records는 도대체 Lombok의 *대체*인가, 아니면 다른 무엇인가?** 같은 것을 더 짧게 적을 수 있다면 그건 그저 문법 설탕에 불과할 텐데, 어떤 자리에서는 되고 어떤 자리에서는 안 된다면 그건 단순한 설탕이 아니다. 의도가 따로 있다는 뜻이다. 그 의도를 짚어보지 않고 코드만 옮기면, 위 동료처럼 두 시간을 날린다.

이 장에서는 record라는 작은 문법 뒤에 숨어 있는 "데이터의 신원(identity)"이라는 큰 이야기를 풀어보자. Brian Goetz가 records를 두고 했던 표현을 빌리면, 이것은 Lombok이라는 "패치"가 아니라 자바가 마침내 "데이터 캐리어를 언어 차원에서 인정한 선언"이다. 무슨 뜻인지, 그리고 그것이 우리 실무 코드에 어떻게 풀려 들어오는지를 함께 살펴보자.

### records가 14에서 preview, 16에서 표준이 된 이유

먼저 작은 진화 박스 하나로 시작하자. Records는 Java 14에 preview로 도입(JEP 359)되어, 15에서 second preview(JEP 384)를 거쳐, 16에서 표준(JEP 395)이 됐다. 이 짧은 흐름이 뜻하는 바를 생각해보자.

> **진화 박스 — Records 표준화 연표**
>
> - **Java 14 (2020-03)** — JEP 359 First Preview. 컴포넌트, canonical constructor, accessor 자동 생성, `equals`/`hashCode`/`toString` 자동의 골격이 처음 모습을 드러낸다.
> - **Java 15 (2020-09)** — JEP 384 Second Preview. 컴팩트 생성자에서 instance 필드 직접 대입 금지가 명확해진다. 로컬 record 허용. 어노테이션 처리에 미세 조정.
> - **Java 16 (2021-03)** — JEP 395 Standard. 1년 만에 표준화. inner class에서의 static member 허용 같은 부수 조항까지 정리.

자바답지 않게 빠르다. 그 자바답지 않은 속도가 무엇을 말하는가? 두 가지를 말한다. 하나는, OpenJDK가 preview라는 단계를 가지면서 *산업 피드백을 받아 다듬는 절차*를 본격적으로 가동하기 시작했다는 점이다. 또 하나는, records가 "데이터 캐리어"라는 *해묵은 요구*에 대한 응답이었다는 점이다. 자바 8 이래 Lombok이 압도적인 점유율로 답하고 있던 그 자리를, 자바가 마침내 언어 차원에서 받아내기 시작한 것이다.

물론 일부 비판도 있다. "5개 LTS를 가로지르며 preview가 돌았다, 너무 빠르다"는 시각이다. 하지만 records의 도입 후 부작용을 보면 그 빠름이 *경솔함*은 아니었다는 사실을 인정하게 된다. preview의 의미가 바로 그것이다 — 산업이 직접 만져보고 흠을 찾아낸 뒤에 표준에 들이는 일. 잊지 말자, 자바는 preview를 단계로 갖춘 첫 메이저 언어다.

### OrderRequest를 record로 옮겨보자

말로만 하면 추상적이니, 손에 잡히는 코드로 옮기자. 주문 시스템의 DTO 세 개 — `OrderRequest`, `OrderResponse`, `OrderEvent` — 를 record로 적어보자.

Lombok 시절의 코드는 이랬다.

```java
@Value
@Builder
public class OrderRequest {
    String customerId;
    List<OrderLine> lines;
    String couponCode;
}
```

`@Value`가 final 클래스 + final 필드 + getter + `equals`/`hashCode`/`toString`을 모두 만들어주었다. `@Builder`가 builder 패턴을 만들어주었다. 코드 다섯 줄로 의도를 압축했고, 그 의도는 "불변 데이터 캐리어"였다.

같은 의도를 record로 옮기면 이렇게 된다.

```java
public record OrderRequest(
    String customerId,
    List<OrderLine> lines,
    String couponCode
) {}
```

한 줄로 본문이 끝났다. record header에 적힌 세 개의 컴포넌트가 곧 필드이자 accessor의 시그니처다. `customerId()`, `lines()`, `couponCode()`가 자동으로 만들어지고, `equals`·`hashCode`·`toString` 세 메서드도 자동이다. `@Value`가 어노테이션 프로세서로 *외부에서* 메우던 일을, 컴파일러가 *언어 차원에서* 해준다.

그 차이가 정말 크다. 어노테이션 프로세서는 IDE마다 인지 정도가 달라서, IntelliJ가 잠시 캐시를 잃으면 빨간 줄이 가득 차는 일이 흔했다. records는 그 자체로 언어다. 컴파일러가 알고, IDE가 알고, 리플렉션·직렬화 라이브러리가 모두 안다. "외부 어노테이션 프로세서에 의존하지 않는다"는 한 줄이 실무에서 얼마나 후련한지, Lombok과 한 번이라도 씨름해본 사람은 안다.

응답과 이벤트도 같은 방식으로 적자.

```java
public record OrderResponse(
    String orderId,
    String status,
    BigDecimal totalAmount,
    Instant createdAt
) {}

public record OrderEvent(
    String orderId,
    OrderEventType type,
    Instant occurredAt
) {}
```

세 DTO를 한 화면에 담아도 모자라지 않다. 코드의 의도가 *데이터*임을 한눈에 알 수 있다. 그리고 더 중요한 사실은, 이제 *이 의도를 컴파일러가 보증한다*는 점이다. 누군가 실수로 `record`에 mutable field나 setter를 넣으려고 하면 컴파일이 막힌다. Lombok 시절에는 `@Value` 옆에 `@Setter`를 같이 붙이는 *찜찜한 코드*를 종종 보았지만, record는 그 경로 자체가 닫혀 있다.

### 자동 생성되는 네 가지, 그리고 직접 손대고 싶을 때

record가 자동으로 만들어주는 것은 정확히 네 가지다.

첫째, **컴포넌트마다 private final 필드와 그에 대응하는 accessor 메서드** — `customerId` 컴포넌트가 있다면 `customerId()`라는 메서드가 자동이다. getter가 아니라 *accessor*다. `get` 접두사가 붙지 않는다는 점에 주의하자. JavaBean 규약을 따르지 않는 작은 선언인데, 그 선언이 뜻하는 바가 작지 않다. record는 "캡슐화된 객체"가 아니라 "*투명한* 데이터 캐리어"라는 입장 표명이다. Jackson과 Spring이 이를 인지해서, 굳이 `@JsonProperty`를 일일이 붙이지 않아도 직렬화가 자연스럽다.

둘째, **canonical constructor** — 컴포넌트 순서대로 받는 생성자. `new OrderRequest("cust-1", lines, "SUMMER10")` 식으로 호출된다.

셋째, **`equals`와 `hashCode`** — 컴포넌트 기반으로 계산된다. 두 record 인스턴스가 *값으로* 같으면 같다고 판단한다. 이 점이 record의 신원을 단적으로 드러낸다. 객체의 신원은 *주소*가 아니라 *값*에 있다.

넷째, **`toString`** — `OrderRequest[customerId=cust-1, lines=..., couponCode=SUMMER10]` 형식. 디버깅에 그대로 쓸 만하다.

이 자동 생성이 마음에 안 들 때는 어떻게 해야 할까? 두 가지 길이 있다.

하나는 **compact constructor**다. canonical constructor의 본문만 적되, 파라미터 목록은 생략하는 형태다. 보통 validation에 쓴다.

```java
public record OrderRequest(
    String customerId,
    List<OrderLine> lines,
    String couponCode
) {
    public OrderRequest {
        if (customerId == null || customerId.isBlank()) {
            throw new IllegalArgumentException("customerId required");
        }
        if (lines == null || lines.isEmpty()) {
            throw new IllegalArgumentException("at least one line required");
        }
        lines = List.copyOf(lines);  // 방어적 복사
    }
}
```

여기서 한 가지 놓치지 말아야 할 점이 있다. compact constructor 안에서 `this.lines = lines` 식으로 *명시적 대입을 할 수 없다*. 컴파일러가 그 일을 마지막에 자동으로 해준다. 다만 *파라미터를 재할당*하는 것은 가능하다. 위 코드에서 `lines = List.copyOf(lines)`를 하면, 컴파일러가 마지막에 그 재할당된 값을 필드에 넣어준다. 작은 차이 같지만, 방어적 복사를 단 한 줄로 끝낼 수 있다는 점에서 실무적으로 큰 차이다.

또 하나는 **explicit canonical constructor**다. 컴팩트 형식 대신 파라미터 목록을 모두 다 적은 정통 생성자. 이 경우는 마지막에 모든 필드를 자기 손으로 대입해야 한다. 컴팩트가 자연스럽지 않은 경우에만 쓰자.

### Records가 안 되는 것

이 자리에서 솔직히 말하자. record로 *모든 것을 옮기려*는 시도는 거의 항상 좌절로 끝난다. record가 안 되는 것들을 분명히 짚어두자.

**상속이 안 된다.** record는 암묵적으로 `final`이며, 자동으로 `java.lang.Record`를 상속한다. 그 외의 클래스를 `extends` 할 수 없다. 다른 클래스가 record를 `extends`할 수도 없다. 인터페이스 `implements`는 가능하다 — `OrderEvent implements DomainEvent` 같은 식. 이 점이 13장에서 다룰 sealed 패턴과 만나면 강력해진다.

**가변 상태가 안 된다.** 모든 컴포넌트는 `private final` 필드로 고정된다. setter가 없고, 추가 instance 필드를 선언할 수도 없다. 컴팩트 생성자에서 방어적 복사를 해도, 컴포넌트가 가리키는 *대상*까지 불변이 되는 것은 아니다. 그래서 `List<OrderLine>` 같은 컴포넌트는 `List.copyOf`로 막는 편이 안전하다.

**그리고 JPA Entity가 안 된다.** 도입부 동료가 겪은 바로 그 좌절이다. JPA의 `@Entity`는 (1) no-args constructor를 요구하고, (2) `final` 클래스를 받아주지 않으며, (3) lazy loading을 위해 proxy로 감싸는데 final field로는 그 proxy가 만들어지지 않는다. record의 모든 자동화가 정확히 JPA의 요구를 거부한다. 같은 단어를 두 개의 패러다임이 정반대 방향으로 쓰는 셈이다.

여기서 *난감해*하지 않으려면, record와 Entity를 *동의어로 보지 않는 정신적 습관*이 필요하다. record는 "투명한 데이터 캐리어"이고 Entity는 "JPA 영속성 컨텍스트가 관리하는 식별자 보유체"다. 의도가 다르다.

> **JLS 인용 박스 — §8.10 Record Classes**
>
> *원문* — "A record class is a special kind of class that acts as a transparent carrier for shallowly immutable data. The components of a record class declaration are the variables that comprise its state."
>
> *번역* — "record 클래스는 *얕은 불변* 데이터를 위한 *투명한 캐리어*로 동작하는, 특수한 종류의 클래스다. record 클래스 선언의 컴포넌트들이 그 상태를 구성하는 변수다."
>
> *해설* — 핵심 단어 두 개를 음미하자. 하나는 *transparent*. record는 자신이 가진 데이터를 *숨기지 않는다*. accessor가 자동이고, `toString`이 자동이고, 외부에서 컴포넌트의 신원을 완전히 들여다볼 수 있다. 객체지향이 줄곧 강조해온 "캡슐화"의 반대편 입장이다. 다른 하나는 *shallowly immutable*. 컴포넌트 자체는 final이지만, 컴포넌트가 가리키는 *내부 객체*까지 강제로 불변이 되지는 않는다. 그래서 `List<OrderLine>`을 컴포넌트로 가지면, 그 리스트의 내용은 변경 가능할 수 있다는 점을 의식해두자.
>
> *본문 연결* — 위 compact constructor에서 `List.copyOf`로 방어적 복사를 한 이유가 여기에 있다. JLS가 "얕은 불변"이라고 명시한 그 한계를 우리가 본문에서 보강하는 것이다.

### Java 23이 풀어준 한 가지 — Flexible Constructor Bodies

records를 본격적으로 쓰다 보면, 또 하나의 작은 답답함을 만난다. 생성자에서 `super()`나 `this()` 호출은 *반드시 첫 줄*이어야 한다는 30년 묵은 규칙이다. records 자체는 `Record`를 자동으로 상속하니 큰 문제 없어 보이지만, 일반 클래스나 record의 컴팩트 생성자에서 *유도된 값으로 super를 호출하고 싶을 때* 그 규칙이 발목을 잡았다.

이 답답함을 푸는 것이 **JEP 482 (Java 23 preview)** → **JEP 513 (Java 25 표준)** Flexible Constructor Bodies다. 이제는 `super()` 또는 `this()` 호출 이전에도 *검증·계산·로깅* 같은 코드가 들어갈 수 있다. 단, 그 prologue 안에서는 *해당 인스턴스의 필드나 메서드에 접근할 수 없다*. 아직 객체가 만들어지기 전이므로.

```java
public class ValidatedAmount {
    private final BigDecimal value;

    public ValidatedAmount(BigDecimal raw) {
        if (raw == null || raw.signum() < 0) {
            throw new IllegalArgumentException("non-negative required");
        }
        var normalized = raw.setScale(2, RoundingMode.HALF_UP);
        super();   // ← 이제 첫 줄이 아니어도 된다
        this.value = normalized;
    }
}
```

작은 변화로 보이지만, records의 compact constructor와 결합되면 더 자연스러워진다. compact constructor 안에서 *파라미터를 정규화한 후*에 super-like 호출을 끼울 일은 record에서는 거의 없지만, 이 룰의 종말은 자바 전체 코드 스타일에 천천히 스며들 변화다. *언어가 자기 안의 묵은 제약을 풀어주는 신호*로 기억해두자.

### Records vs Lombok — 신원의 문제

자, 이제 본격적인 논쟁으로 들어가자. records가 Lombok을 대체하는가? Brian Goetz가 한 인터뷰에서 이 질문을 받았을 때 그가 한 답이 인상적이다.

> "Records aren't there to replace Lombok. Records are there because Java has finally decided that data carriers deserve to be a first-class concept in the language."
>
> "Records가 Lombok을 대체하려고 등장한 것이 아니다. Records는 *데이터 캐리어가 언어의 일급 개념으로 인정받을 자격이 있다*고 자바가 마침내 결정했기 때문에 등장한 것이다."

이 문장을 두 번 읽자. Goetz의 입장은 명료하다. Lombok은 "자바가 부족해서 외부 어노테이션 프로세서로 메우던 *패치*"였다. records는 "자바가 자신의 어휘로 데이터 캐리어를 인정한 *신원* 표명"이다. 둘은 의도가 다르고, 그 결과 잘 맞는 자리가 다르다.

실무 정착의 방향을 정리하면 이렇다.

**records가 잘 맞는 자리:** DTO, command, event, value object, projection 결과, `@ConfigurationProperties` 바인딩 대상. 한마디로 *불변, 캡슐화 없음, 컴포넌트 동등성으로 의미가 결정되는 모든 자리*다.

**Lombok이 여전히 자기 자리를 지키는 곳:**

- **`@Slf4j`** — record에는 logger를 둘 instance 필드를 추가할 수 없다. 정적 logger 도입을 위한 한 줄짜리 어노테이션은 record와 무관하게 계속 유용하다.
- **`@SneakyThrows`** — checked exception을 unchecked로 감춰주는 도구. 미학적 호불호는 있지만, 인프라성 코드에서는 여전히 쓰임이 있다.
- **`@Accessors(chain = true)` / `@Builder`** — mutable POJO에서 fluent setter나 builder가 필요한 경우. record는 builder를 자동으로 만들어주지 않는다(요청은 끊임없이 올라오지만, OpenJDK 측은 신중하다).
- **JPA Entity** — 위에서 짚었다. record가 안 되는 자리.

그래서 실무 합의는 명확하다. **"DTO와 Value Object는 records, Entity와 mutable 도메인 객체는 Lombok 클래스"**. 이 두 영역이 서로 자리를 다투지 않는다는 점을 기억해두면, "record로 모든 것을 옮기려다 좌절하는 일"을 피할 수 있다.

물론 *Lombok을 점점 줄여가는 것*은 바람직하다. 어노테이션 프로세서에 의존하는 것은 그 자체로 외부 의존성이고, JDK가 진화할 때마다 호환성 이슈를 일으킨다(Lombok 1.18.22 미만은 Java 17과 잘 맞지 않았던 경험을 다들 기억할 것이다). 그러나 "Lombok을 한순간에 걷어내자"는 시도는 *지긋지긋한 작업*이 될 가능성이 높다. records가 잘 맞는 자리부터 차근히 옮기는 편이 낫다.

### 직렬화 — Jackson, JPA AttributeConverter, ConfigurationProperties

records를 DTO로 쓰겠다고 마음먹는 순간, 가장 먼저 마주치는 실무 질문은 직렬화다. JSON으로 어떻게 변환되는가? Spring `@ConfigurationProperties`에 어떻게 바인딩되는가? JPA 컨버터와 어떻게 어울리는가?

**Jackson은 records를 잘 안다.** Jackson 2.12 이상부터 records가 일급 시민이다. 별도 모듈 없이 직렬화·역직렬화가 동작한다. 다만 한 가지 작은 *주의*가 있다 — record의 accessor는 `get` 접두사가 없으므로, Jackson의 기본 introspection이 컴포넌트 이름을 직접 본다. 그래서 JSON 필드명을 컴포넌트 이름과 다르게 쓰고 싶다면 `@JsonProperty`를 컴포넌트 위에 직접 붙이거나, record header에 어노테이션을 적어야 한다.

```java
public record OrderRequest(
    @JsonProperty("customer_id") String customerId,
    List<OrderLine> lines,
    @JsonProperty("coupon_code") String couponCode
) {}
```

snake_case 컨벤션과 camelCase 자바 컴포넌트를 잇는 정도면 이 정도 표시로 충분하다. 더 큰 변환이 필요하다면 `@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)`를 클래스 레벨로 한 번 적어두자.

**Spring `@ConfigurationProperties`도 records와 자연스럽다.** 정확히는 Spring Boot 2.4 이후 *constructor binding*이 도입되면서부터다. `@ConstructorBinding`을 record header에 붙이지 않아도 된다 — Spring이 자동으로 canonical constructor를 통해 바인딩한다.

```java
@ConfigurationProperties(prefix = "order")
public record OrderProperties(
    Duration timeout,
    int retryCount,
    List<String> allowedChannels
) {}
```

`application.yml`의 `order.timeout=PT5S`, `order.retry-count=3` 같은 설정이 그대로 들어온다. 컴포넌트가 final이고 setter가 없으므로, 누구도 런타임에 설정을 *몰래 바꿀 수* 없다. 설정은 불변이라는 원칙을 *언어가 보증해주는* 셈이다. 이것이 records를 설정에 쓰는 가장 큰 이유다.

**JPA `AttributeConverter`에 record를 쓰는 일.** record를 column 한 칸에 JSON으로 넣어두는 패턴이다. `@Convert(converter = OrderMetadataConverter.class)`를 Entity 필드에 붙이고, `AttributeConverter<OrderMetadata, String>`이 Jackson을 통해 직렬화·역직렬화하는 식이다. 이때 record는 *값 자체로* 다뤄지고, JPA의 영속성 컨텍스트가 그 컴포넌트 단위로 dirty checking을 하지는 않는다. 그래서 *불변 값 묶음*에는 자연스럽고, 부분 수정이 잦은 데이터에는 부적합하다. 잊지 말자.

**Spring Data의 projection.** 인터페이스 기반 projection을 써본 사람이라면 "동적 proxy로 만들어지는 그 객체가 어색하다"는 인상을 받았을 것이다. record projection은 그 어색함을 깔끔히 푼다.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("""
        SELECT new com.example.OrderSummary(o.id, o.status, o.totalAmount)
        FROM Order o
        WHERE o.customerId = :customerId
    """)
    List<OrderSummary> findSummariesByCustomer(String customerId);
}

public record OrderSummary(Long id, String status, BigDecimal totalAmount) {}
```

JPQL의 `new` 절이 record의 canonical constructor를 그대로 호출한다. 결과는 *값으로 결정되는* record 인스턴스의 리스트다. 인터페이스 proxy의 어색함이 사라지고, 콜링 사이트에서는 그저 record를 쓰듯이 다루면 된다.

### Java 8과 Java 21 — DTO 한 개의 변천사

이 장의 마지막에, 같은 의도를 가진 *한 개의 DTO가* 11년 사이에 어떻게 변했는지를 한 화면에 담아보자. 이 비교가 records의 가치를 가장 정직하게 보여준다.

**Java 8 시절, Lombok 없이 적은 코드:**

```java
public final class OrderRequest {
    private final String customerId;
    private final List<OrderLine> lines;
    private final String couponCode;

    public OrderRequest(String customerId, List<OrderLine> lines, String couponCode) {
        this.customerId = customerId;
        this.lines = lines == null ? List.of() : List.copyOf(lines);
        this.couponCode = couponCode;
    }

    public String getCustomerId() { return customerId; }
    public List<OrderLine> getLines() { return lines; }
    public String getCouponCode() { return couponCode; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderRequest other)) return false;
        return Objects.equals(customerId, other.customerId)
            && Objects.equals(lines, other.lines)
            && Objects.equals(couponCode, other.couponCode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(customerId, lines, couponCode);
    }

    @Override
    public String toString() {
        return "OrderRequest{customerId=" + customerId
            + ", lines=" + lines + ", couponCode=" + couponCode + "}";
    }
}
```

35줄에 가까운 boilerplate. 사람이 손으로 적기에 *번거롭다*. 컴포넌트가 추가될 때마다 4군데를 빠짐없이 수정해야 한다. 한 군데라도 빠뜨리면 `equals`가 조용히 잘못 동작하는 *끔찍한 일*이 생긴다.

**Java 8 + Lombok 시절:**

```java
@Value
@Builder
public class OrderRequest {
    String customerId;
    List<OrderLine> lines;
    String couponCode;
}
```

5줄로 압축됐다. 그러나 이 코드를 읽기 위해서는 Lombok의 어노테이션 의미를 알아야 한다. `@Value`가 정확히 무엇을 만들어주는지, `@Builder`가 어떤 패턴을 따르는지. 그리고 IDE가 그 의미를 *제대로 인지하고 있어야* 빨간 줄이 없다. 외부 도구에 의존하는 코드.

**Java 21, records:**

```java
public record OrderRequest(
    String customerId,
    List<OrderLine> lines,
    String couponCode
) {}
```

5줄. 외부 의존성 없이 언어 차원에서 보증된 5줄. 컴파일러가 직접 알고, IDE가 직접 알고, 리플렉션이 직접 안다. *언어가 데이터 캐리어를 인정한 코드*다.

차이는 단순한 줄 수가 아니다. 의도가 *밖으로 드러나는* 정도가 다르다. Java 8 코드는 "불변 데이터 클래스를 만들고 싶어요"라는 의도를 *35줄의 boilerplate로 표현*했다. Lombok 코드는 그 의도를 *어노테이션의 의미를 빌려* 표현했다. records 코드는 그 의도를 *문법 그 자체로* 표현한다. 코드를 읽는 사람이 별도의 지식 없이도 "아, 이건 데이터 캐리어"라고 즉각 안다.

### 마무리

이 장에서 우리가 정리한 것을 한 번 거두어보자.

records는 *Lombok의 대체*가 아니다. 자바가 데이터 캐리어를 *언어 차원에서 인정한 신원 선언*이다. 그래서 records는 *DTO·VO·command·event·projection 결과·configuration*과 잘 맞고, JPA Entity·mutable 도메인 객체·logger를 품은 인프라 클래스와는 맞지 않는다. 두 영역이 자리를 다투지 않는다는 사실을 기억하자.

문법은 단순하다. record header에 컴포넌트를 나열하면 `private final` 필드, accessor, canonical constructor, `equals`/`hashCode`/`toString`이 자동으로 만들어진다. validation은 compact constructor로, 방어적 복사는 그 안에서 파라미터 재할당으로. 더 풀어 적고 싶다면 explicit canonical constructor도 가능하다.

Jackson은 records를 직접 안다. Spring `@ConfigurationProperties`도 records의 canonical constructor로 직접 바인딩한다. JPQL의 `new` 절이 record를 받아 projection을 돌려준다. *언어와 프레임워크의 합의가 자연스럽다*는 것이 records의 진짜 힘이다.

다음 장에서는 records의 *짝패*인 sealed classes를 살펴보자. records가 *product type*이라면 sealed는 *sum type*이다. 결제 상태 모델을 enum이 더 이상 표현하지 못하는 자리에서 시작해, 합 타입이 자바에 마침내 들어온 의미를 짚어보겠다. 그리고 13장에서 두 도구를 패턴 매칭으로 분해하는 *데이터지향 자바의 삼위일체*가 완성된다. record를 product, sealed를 sum, pattern을 분해기로 — 이 셋이 함께 만들어내는 표현력이 어디까지 가는지를 함께 보자.

---

## 12장. Sealed Classes — 합 타입(Sum Type)이 자바에 들어온 날

결제 시스템의 한 팀이 enum 하나를 두고 회의를 하고 있다고 해보자. `PaymentResult`라는 이름의 enum이다. 처음 만들어졌을 때는 `APPROVED`와 `DECLINED` 둘뿐이었다. 깔끔했다. 하지만 사업이 자라면서 상태가 늘었다. `PENDING`이 추가됐고(3D Secure 인증 대기), `CANCELLED_BY_USER`가 붙었고, `PARTIAL_REFUND`가 들어왔고, 어제는 `FRAUD_HOLD`가 추가됐다.

그리고 오늘 PM이 새 요구를 들고 왔다. "*승인된 결제에는 승인 시각과 카드 발급사 코드*가 같이 보관돼야 하고, *거절된 결제에는 거절 사유와 retry 가능 여부*가 있어야 한다. *Pending에는 인증 URL과 만료 시각*이 필요하다." 한 자리에 있던 enum이 갑자기 각자 다른 데이터를 요구하기 시작한 것이다.

이쯤 되면 enum 옆에 `Map<PaymentResult, Object>`를 두거나, `if (result == APPROVED) { ... } else if (result == DECLINED) { ... }` 식의 분기 안에서 캐스팅을 시작한다. 둘 다 *찜찜한 코드*다. 컴파일러가 더 이상 우리를 도와주지 않는다 — "Pending 상태일 때 인증 URL이 반드시 있다"는 약속이 *주석으로만 존재*하기 때문이다. 한 줄을 빠뜨리면 production에서 NPE가 난다.

다른 회사의 비슷한 자리에서는 어떻게 했을까? Scala라면 `sealed trait PaymentResult` 한 줄로, Kotlin이라면 `sealed class PaymentResult`로, Rust라면 `enum PaymentResult { Approved { ... }, Declined { ... } }`로 풀었을 자리다. 함수형 계열 언어들이 30년 동안 *합 타입(sum type)*이라 부르며 다뤄온 그 도구가 자바에 왔다. Java 17부터다.

이 장에서는 sealed classes가 무엇이고, *enum으로는 안 됐던 무엇*을 풀어주는지를 함께 살펴보자. 결제 상태 모델을 enum에서 sealed로 옮기면서, 그동안 Visitor 패턴이 6번째로 같은 코드를 적게 만들던 *지긋지긋함*도 같이 정리해보자.

### sealed가 도입되기 전, 우리는 무엇을 못 했나

**enum으로 충분했을까?** 짧게 답하면, enum은 *고정된 상수 집합*에만 충분하다. 각 상수가 *서로 다른 모양의 데이터*를 요구하는 순간 enum은 한계를 드러낸다. 위의 `PaymentResult`가 정확히 그 한계다.

물론 enum에 필드와 메서드를 붙일 수는 있다. 그러나 그것은 *모든 상수가 같은 필드를 가져야* 한다는 의미다. `APPROVED`에는 카드 발급사 코드가 필요하지만 `PENDING`에는 인증 URL이 필요할 때, enum은 두 필드를 *모두* 가지게 된다. 그리고 `PENDING` 인스턴스의 카드 발급사 코드는 null로 남는다. 다시 *찜찜한 코드*다.

그래서 자바 개발자들은 두 가지 우회를 만들어왔다. 하나는 **클래스 계층 + 추상 클래스**. `abstract class PaymentResult`를 만들고 `Approved`, `Declined`, `Pending`이 `extends`하는 식이다. 각 sub-class가 자기 필드를 가진다. 이렇게 하면 데이터 모양은 풀린다. 그러나 새로운 문제가 등장한다 — *누구나 그 추상 클래스를 상속할 수 있다*. 라이브러리를 사용하는 외부 코드가 `class HackedResult extends PaymentResult` 한 줄로 우리 도메인을 *오염*시킬 수 있다.

다른 하나는 **Visitor 패턴**이다. 1990년대에 GoF가 제안한 그 패턴이다. *분기를 객체화*해서 컴파일러에 분기의 완전성을 위탁하는 기법. 일단 코드 한 덩이를 보자.

```java
public abstract class PaymentResult {
    public abstract <R> R accept(Visitor<R> visitor);

    public interface Visitor<R> {
        R visitApproved(Approved a);
        R visitDeclined(Declined d);
        R visitPending(Pending p);
    }

    public static final class Approved extends PaymentResult {
        private final Instant approvedAt;
        private final String issuerCode;
        public Approved(Instant approvedAt, String issuerCode) {
            this.approvedAt = approvedAt;
            this.issuerCode = issuerCode;
        }
        public Instant approvedAt() { return approvedAt; }
        public String issuerCode() { return issuerCode; }
        @Override
        public <R> R accept(Visitor<R> visitor) { return visitor.visitApproved(this); }
    }

    public static final class Declined extends PaymentResult {
        private final String reasonCode;
        private final boolean retryable;
        public Declined(String reasonCode, boolean retryable) {
            this.reasonCode = reasonCode;
            this.retryable = retryable;
        }
        public String reasonCode() { return reasonCode; }
        public boolean retryable() { return retryable; }
        @Override
        public <R> R accept(Visitor<R> visitor) { return visitor.visitDeclined(this); }
    }

    public static final class Pending extends PaymentResult {
        private final URI authenticationUrl;
        private final Instant expiresAt;
        public Pending(URI authenticationUrl, Instant expiresAt) {
            this.authenticationUrl = authenticationUrl;
            this.expiresAt = expiresAt;
        }
        public URI authenticationUrl() { return authenticationUrl; }
        public Instant expiresAt() { return expiresAt; }
        @Override
        public <R> R accept(Visitor<R> visitor) { return visitor.visitPending(this); }
    }
}
```

50줄 가까이 됐다. 그리고 사용 측은 이렇게 적는다.

```java
String message = result.accept(new PaymentResult.Visitor<String>() {
    @Override public String visitApproved(Approved a) {
        return "결제 완료: " + a.issuerCode();
    }
    @Override public String visitDeclined(Declined d) {
        return d.retryable() ? "재시도 가능" : "재시도 불가";
    }
    @Override public String visitPending(Pending p) {
        return "인증 필요: " + p.authenticationUrl();
    }
});
```

호출 한 번을 위해 익명 클래스 한 덩어리가 매번 등장한다. 새 상태가 추가될 때마다 — `FraudHold`를 더한다고 해보자 — Visitor 인터페이스에 `visitFraudHold`를 추가하고, *모든 호출 사이트*가 컴파일 에러를 통해 갱신을 요구한다. 컴파일러가 완전성을 보장해주긴 한다. 그 점은 좋다. 하지만 *대가가 너무 크다*.

이 코드를 6번째로 적던 어느 날, 자바 개발자라면 모두 한 번쯤 한숨을 쉬어봤을 것이다. "왜 자바는 *닫힌 계층*을 일등 시민으로 받아주지 않는가?" 그 질문에 대한 OpenJDK의 답이 sealed classes다.

### JEP 360에서 409까지 — 자바의 답

연표를 짧게 짚자.

> **진화 박스 — Sealed Classes 표준화**
>
> - **Java 15 (2020-09)** — JEP 360 First Preview. `sealed`·`permits`·`non-sealed` 키워드의 골격 등장.
> - **Java 16 (2021-03)** — JEP 397 Second Preview. 같은 컴파일 단위면 `permits` 생략 가능 등의 미세 조정.
> - **Java 17 (2021-09)** — JEP 409 Standard. 첫 post-Java 8 LTS와 함께 표준화. records(JEP 395)는 16에 먼저 표준이 됐는데, sealed가 17에서 합류하며 *records + sealed*의 짝패가 동시에 성숙해진다.

이 흐름이 뜻하는 바가 있다. records는 *product type*, sealed는 *sum type*. 둘이 *같은 LTS 사이클에서 표준에 들어왔다*. 자바 17이라는 LTS의 정체성을 단 한 단어로 정리해야 한다면 **"데이터지향(data-oriented)"** 이다. records와 sealed가 *짝패로 들어왔기 때문에* 그 명명이 가능해졌다.

### sealed의 문법 — 세 단어로 충분하다

자, 결제 상태 모델을 sealed로 다시 적자. records와 짝지어서.

```java
public sealed interface PaymentResult
    permits PaymentResult.Approved,
            PaymentResult.Declined,
            PaymentResult.Pending {

    record Approved(Instant approvedAt, String issuerCode) implements PaymentResult {}
    record Declined(String reasonCode, boolean retryable) implements PaymentResult {}
    record Pending(URI authenticationUrl, Instant expiresAt) implements PaymentResult {}
}
```

위 Visitor 패턴의 50줄이 이 코드 9줄로 압축됐다. 그리고 같은 보증을 *언어 차원에서* 받는다.

세 단어를 짚자. `sealed`, `permits`, `non-sealed`. 그리고 `sealed`의 sub-type이 가져야 하는 세 선택지 — `final`, `sealed`, `non-sealed`.

**`sealed`** — 이 타입을 *상속·구현할 수 있는 후보를 제한*한다는 선언이다. 인터페이스에도 클래스에도 붙는다.

**`permits`** — 그 후보들을 *이름으로 명시*한다. 위 코드에서는 `Approved`, `Declined`, `Pending` 세 record가 후보다.

**`permits` 생략 가능 조건** — 같은 컴파일 단위(같은 `.java` 파일) 안에 sub-type이 모두 있으면 `permits` 절을 생략할 수 있다. 컴파일러가 같은 파일 안의 sub-type을 찾아 자동으로 채운다. 위 코드는 한 파일에 다 들어 있으므로 사실 `permits` 절을 지워도 동작한다. 다만 *명시성*을 위해 적어두는 편이 낫다 — sealed의 가치가 "닫힘이 명시적이다"라는 점에 있으므로, `permits`를 적는 것이 그 명시성을 살린다.

**sub-type의 세 선택지** — `permits`된 sub-type은 *반드시* 세 키워드 중 하나로 자신의 *연속·종결*을 선언해야 한다.

- `final` — 더 이상 상속되지 않는다. records는 자동으로 final이다.
- `sealed` — 이 sub-type도 다시 sealed. 자신의 `permits`를 다시 가진다.
- `non-sealed` — 이 sub-type부터는 *상속이 다시 열린다*. 봉인이 한 번 깨진다.

`non-sealed`의 의미를 한 번 더 짚자. sealed 계층의 끝에서 *기존 코드와의 호환*을 위해 봉인을 풀어야 할 자리가 종종 있다. 예를 들어 외부 라이브러리가 우리의 어떤 인터페이스를 자유롭게 구현하도록 허용하고 싶을 때. `non-sealed`는 그 *명시적 출구*다. 봉인의 닫힘이 *전체 다*는 아니라는 표현이다.

**같은 모듈, 같은 패키지 제약** — 자바 17의 sealed는 sub-type이 *같은 모듈 안*에 있어야 한다. 모듈을 쓰지 않는 경우(unnamed module)에는 *같은 패키지 안*. 이 제약이 뜻하는 바는 분명하다. "*우리 도메인의 경계 안에서만* 닫힘이 유효하다." 외부 코드가 `permits` 목록에 끼어드는 일은 컴파일러가 막아준다. 도입부에서 우려한 *외부 오염*의 가능성이 닫혔다.

> **JLS 인용 박스 — §8.1.1.2 sealed, permits**
>
> *원문* — "A `sealed` class restricts which other classes or interfaces may directly extend it. ... A class which is declared `sealed` must have either a `permits` clause or have all of its permitted direct subclasses declared in the same compilation unit."
>
> *번역* — "`sealed` 클래스는 *어떤 다른 클래스나 인터페이스가 자신을 직접 확장할 수 있는지를 제한한다*. (…) `sealed`로 선언된 클래스는 `permits` 절을 가지거나, *허용된 모든 직접 sub-class가 같은 컴파일 단위 안에서 선언되어야* 한다."
>
> *해설* — 핵심 단어는 *directly extend*. sealed의 닫힘은 *직접 sub-type 수준*에서 강제되는 닫힘이다. 그리고 `permits`된 sub-type이 다시 `non-sealed`라면, 그 아래로는 닫힘이 풀린다. 즉 sealed는 *완전한 잠금*이 아니라 *명시된 닫힘*이다. 닫힘과 열림을 *각 레이어에서 선언하는* 도구로 이해하자.
>
> *본문 연결* — `PaymentResult`가 `Approved`, `Declined`, `Pending` 셋만 허용한다는 보증이 이 문장에서 나온다. 새로운 결제 상태가 사업적으로 등장한다면, 그 추가는 *우리 도메인 내부의 명시적 결정*으로만 일어난다. 외부 라이브러리가 우리 모르게 새 sub-type을 끼워 넣을 길이 없다.

### 이것은 *합 타입*이다 — 다른 언어에서는 어떻게 부르나

sealed classes의 자바스러운 이름은 그렇게 정해졌다. 하지만 이 개념의 본명은 다른 곳에 있다. *합 타입(sum type)*. 함수형 언어들이 30년 동안 다뤄온 그 개념이다. 짧게 옆 언어들을 둘러보자.

**Haskell:**

```haskell
data PaymentResult
    = Approved UTCTime String
    | Declined String Bool
    | Pending URI UTCTime
```

`|`를 *또는*으로 읽자. `PaymentResult`는 *Approved이거나, Declined이거나, Pending이다*. 정확히 셋 중 하나다. 새 sub-type을 끼워 넣으려면 `data` 선언을 *명시적으로 수정*해야 한다. 자바의 sealed가 받아온 그 보증이다.

**Scala:**

```scala
sealed trait PaymentResult
final case class Approved(approvedAt: Instant, issuerCode: String) extends PaymentResult
final case class Declined(reasonCode: String, retryable: Boolean) extends PaymentResult
final case class Pending(authenticationUrl: URI, expiresAt: Instant) extends PaymentResult
```

문법이 자바의 sealed + record와 거의 같다. 그렇다 — *자바가 Scala를 따른 것이다*. 정확히는 ML·Haskell 계보를 Scala가 JVM 위에 올렸고, 자바가 다시 그 계보를 자기 어휘로 받아들였다.

**Kotlin:**

```kotlin
sealed class PaymentResult {
    data class Approved(val approvedAt: Instant, val issuerCode: String) : PaymentResult()
    data class Declined(val reasonCode: String, val retryable: Boolean) : PaymentResult()
    data class Pending(val authenticationUrl: URI, val expiresAt: Instant) : PaymentResult()
}
```

마찬가지다. Kotlin은 같은 도구를 자바보다 먼저(2017) 가졌고, 안드로이드 진영에서는 *데이터 클래스 + 봉인 클래스*가 사실상의 표준 도메인 모델링 도구다.

**Rust:**

```rust
enum PaymentResult {
    Approved { approved_at: Instant, issuer_code: String },
    Declined { reason_code: String, retryable: bool },
    Pending { authentication_url: Url, expires_at: Instant },
}
```

Rust는 자기 `enum` 키워드 안에 합 타입을 그대로 욱여넣었다. 자바의 enum과 *이름이 같을 뿐 다른 개념*이다 — Rust의 enum이 자바의 sealed에 해당한다. 이 점이 처음 두 언어를 오갈 때 가장 혼란스러운 자리다.

자, 다섯 언어를 둘러봤다. 모두 같은 한 가지를 표현한다. **합 타입은 닫힌 대안의 집합이다.** 그리고 그 닫힘이 *컴파일러에 의해 강제*된다. 자바가 마침내 그 문법을 자기 어휘로 받아들였다는 사실이 데이터지향 자바의 정체성을 결정짓는다.

Brian Goetz가 *Data-Oriented Programming in Java*에서 한 표현이 이 자리를 잘 정리한다. "We need products (records) and we need sums (sealed)." 곱과 합. *records는 컴포넌트의 곱, sealed는 sub-type의 합*. 두 도구가 함께 와야 ADT(algebraic data types)가 완성된다. 그래서 두 도구는 *짝패*다 — 한쪽만 들이는 일은 절반의 도입이다.

### Visitor와 sealed의 코드 길이 — 실측 비교

말로만 비교하지 말고, 같은 한 가지 일을 두 방식으로 적어 길이를 재보자. 결제 결과를 받아 *사용자에게 보여줄 메시지*와 *감사 로그에 기록할 한 줄*과 *후속 액션이 자동 재시도인지*를 각각 결정하는 일이다.

**Visitor 패턴으로 적은 코드:**

```java
public abstract class PaymentResult {
    public abstract <R> R accept(Visitor<R> visitor);
    public interface Visitor<R> {
        R visitApproved(Approved a);
        R visitDeclined(Declined d);
        R visitPending(Pending p);
    }
    public static final class Approved extends PaymentResult { /* ... 12줄 ... */ }
    public static final class Declined extends PaymentResult { /* ... 12줄 ... */ }
    public static final class Pending extends PaymentResult { /* ... 12줄 ... */ }
}

// 세 가지 결정을 위해 Visitor 인스턴스를 세 개 만들어야 한다
String userMessage = result.accept(new PaymentResult.Visitor<String>() {
    @Override public String visitApproved(Approved a) { return "결제 완료"; }
    @Override public String visitDeclined(Declined d) {
        return d.retryable() ? "재시도 가능한 실패" : "재시도 불가";
    }
    @Override public String visitPending(Pending p) { return "인증이 필요합니다"; }
});

String auditLog = result.accept(new PaymentResult.Visitor<String>() {
    @Override public String visitApproved(Approved a) { return "APPROVED " + a.issuerCode(); }
    @Override public String visitDeclined(Declined d) { return "DECLINED " + d.reasonCode(); }
    @Override public String visitPending(Pending p) { return "PENDING " + p.expiresAt(); }
});

boolean autoRetry = result.accept(new PaymentResult.Visitor<Boolean>() {
    @Override public Boolean visitApproved(Approved a) { return false; }
    @Override public Boolean visitDeclined(Declined d) { return d.retryable(); }
    @Override public Boolean visitPending(Pending p) { return false; }
});
```

타입 선언과 세 호출을 모두 합치면 *80줄 가까이* 된다. 매 호출마다 익명 클래스 한 덩어리가 등장하는 *지긋지긋함*이 본문에 그대로 드러난다.

**sealed + record + pattern matching으로 적은 코드:**

```java
public sealed interface PaymentResult {
    record Approved(Instant approvedAt, String issuerCode) implements PaymentResult {}
    record Declined(String reasonCode, boolean retryable) implements PaymentResult {}
    record Pending(URI authenticationUrl, Instant expiresAt) implements PaymentResult {}
}

String userMessage = switch (result) {
    case Approved a -> "결제 완료";
    case Declined(var reason, var retryable) -> retryable ? "재시도 가능한 실패" : "재시도 불가";
    case Pending p -> "인증이 필요합니다";
};

String auditLog = switch (result) {
    case Approved(var at, var issuer) -> "APPROVED " + issuer;
    case Declined(var reason, var retry) -> "DECLINED " + reason;
    case Pending(var url, var expires) -> "PENDING " + expires;
};

boolean autoRetry = switch (result) {
    case Approved a -> false;
    case Declined d -> d.retryable();
    case Pending p -> false;
};
```

*25줄 안쪽*이다. 그러면서 컴파일러의 완전성 검사는 정확히 같다 — 새 sub-type을 추가하면 *세 switch 모두*가 컴파일 에러로 갱신을 요구한다. Visitor가 100% 같은 보증을 *80줄로* 사주던 일을, sealed + pattern은 *25줄로* 사준다.

이 차이가 어디서 오는가? 본질적으로는 *분기를 객체화할 필요가 없어졌다*는 데서 온다. Visitor의 정체는 "switch가 없으니 그것을 객체로 모사한다"였다. 자바에 *데이터 분해를 아는 switch*가 들어오자, 그 모사가 불필요해진 것이다. 다음 장의 주인공이 바로 그 *데이터 분해를 아는 switch* — pattern matching이다.

### enum + sealed — 함께 쓰면 더 좋은 자리

여기까지 보면 "enum은 사망 선고인가?"라는 인상을 받을 수 있다. 그렇지 않다. enum은 *상태가 고정 상수이고, 각 상수가 같은 모양의 데이터를 가진다*는 *그* 자리에서는 여전히 가장 자연스럽다. 결제 *방법*(`CREDIT_CARD`, `BANK_TRANSFER`, `KAKAO_PAY`)은 enum이 어울린다. 결제 *결과*(`Approved`, `Declined`, `Pending`)는 sealed가 어울린다. 자리가 다르다.

오히려 두 도구를 *함께 쓰면* 더 좋아진다.

```java
public sealed interface PaymentResult {
    record Approved(Instant approvedAt, String issuerCode, PaymentMethod method)
        implements PaymentResult {}
    record Declined(String reasonCode, boolean retryable, PaymentMethod method)
        implements PaymentResult {}
    record Pending(URI authenticationUrl, Instant expiresAt, PaymentMethod method)
        implements PaymentResult {}
}

public enum PaymentMethod {
    CREDIT_CARD, BANK_TRANSFER, KAKAO_PAY, TOSS_PAY
}
```

각 결과 안에 *어떤 결제 방법으로 처리됐는지*를 enum으로 끼워 넣는다. 합 타입 안에 *고정 상수의 곱*이 들어간 모양이다. 두 도구가 서로의 자리를 잠식하지 않는다는 것이 보인다.

### Spring 도메인 이벤트에서의 sealed

sealed가 빛나는 또 하나의 자리가 Spring의 도메인 이벤트다. `ApplicationEventPublisher`로 이벤트를 발행할 때, 이벤트 타입을 sealed로 닫아두면 *수신자 측이 exhaustive 분기*를 쓸 수 있다.

```java
public sealed interface UserEvent {
    record Created(String userId, Instant createdAt) implements UserEvent {}
    record Updated(String userId, Set<String> changedFields, Instant updatedAt) implements UserEvent {}
    record Deleted(String userId, Instant deletedAt) implements UserEvent {}
}

@Component
public class UserEventListener {
    @EventListener
    public void on(UserEvent event) {
        switch (event) {
            case UserEvent.Created c -> handleCreated(c);
            case UserEvent.Updated u -> handleUpdated(u);
            case UserEvent.Deleted d -> handleDeleted(d);
        }
    }
}
```

새 이벤트 타입 — 예를 들어 `Suspended` — 가 sealed에 추가되는 순간, 위 listener의 switch가 *컴파일 에러*로 갱신을 요구한다. 도메인이 자라면서 "어떤 이벤트 핸들러가 갱신을 빠뜨렸는지"를 *컴파일 시점에 잡아주는* 안전망이다. enum + `if`/`else` 분기로는 결코 받을 수 없었던 *컴파일러의 보증*이다.

Spring Cloud Stream이나 Kafka로 이벤트를 *직렬화*해 전송할 때도 sealed가 유용하다. Jackson의 `@JsonTypeInfo` + `@JsonSubTypes`로 polymorphic 직렬화를 적던 자리에, sealed의 `permits` 목록이 *그 SubTypes 목록을 코드로* 갈음한다. Jackson 2.16부터는 sealed 인터페이스에 대해 polymorphic deserialization을 자동 추론해주는 기능이 들어왔다 — `permits` 목록을 그대로 SubTypes로 본다. *언어와 라이브러리의 합의*가 자라고 있다는 신호다.

### 13장으로 가는 다리

여기까지 정리하면 sealed가 무엇이고 왜 들어왔는지가 손에 잡힌다. 그런데 한 가지 어색한 점이 남는다. 위 코드의 switch가 *어떻게 records를 분해하는지*를 우리는 아직 설명하지 않았다.

```java
case Declined(var reason, var retryable) -> retryable ? "재시도 가능" : "재시도 불가";
```

이 한 줄에서 `Declined`라는 sub-type을 *매칭*하고, 동시에 그 컴포넌트 두 개를 `reason`과 `retryable`이라는 이름으로 *분해*했다. 두 가지 일이 동시에 일어났다. *타입 매칭 + 컴포넌트 분해*가 한 줄에 담긴 이 능력이 13장의 주인공 — *pattern matching* 이다.

records가 product, sealed가 sum, pattern matching이 분해기. 이 셋이 함께 와야 비로소 ADT가 *언어 차원에서* 완성된다. 다음 장에서 캐스트 사다리 9단을 한 화면에 펼쳐놓고, 그 사다리가 pattern matching으로 어떻게 *한 줄로 무너지는지*를 함께 보자. 그리고 Brian Goetz가 *Data-Oriented Programming*이라는 단어로 한 묶음으로 부른 이 셋이 *현실 도메인에서* 어떻게 풀려 들어오는지를 — 표현식 평가기, HTTP Result, Workflow 상태기계 세 가지 본격 예제로 — 한 자리에 모아보자.

기억해두자. sealed는 *닫힘을 명시적으로 선언하는 도구*다. 닫힘이 명시적이라는 것은, *언어가 우리 도메인의 경계를 알게 됐다*는 뜻이다. 컴파일러가 그 경계를 들고 있는 한, 우리는 분기를 빠뜨릴 수 없다. 그 작은 보증이 큰 자유를 준다.

---

## 13장. Pattern Matching — ADT를 풀어내는 도구

PR 리뷰에서 한 컨트롤러를 받았다고 해보자. 새벽 두 시에 동료가 보낸 메시지에 "이상하게 동작합니다, 봐주세요"라고만 적혀 있다. 코드를 펼치니 이런 모양이다.

```java
public ResponseEntity<?> handle(Object response) {
    if (response instanceof SuccessResponse) {
        SuccessResponse s = (SuccessResponse) response;
        if (s.getPayload() instanceof OrderCreated) {
            OrderCreated created = (OrderCreated) s.getPayload();
            if (created.getCustomer() instanceof RegisteredCustomer) {
                RegisteredCustomer rc = (RegisteredCustomer) created.getCustomer();
                if (rc.getTier() instanceof PremiumTier) {
                    PremiumTier pt = (PremiumTier) rc.getTier();
                    return premiumHandler(pt, created);
                } else if (rc.getTier() instanceof StandardTier) {
                    // ...
                }
            } else if (created.getCustomer() instanceof GuestCustomer) {
                // ...
            }
        } else if (s.getPayload() instanceof PaymentApproved) {
            // ...
        }
    } else if (response instanceof ErrorResponse) {
        // ...
    }
    return ResponseEntity.badRequest().build();
}
```

캐스트 사다리가 9단까지 늘어났다. 같은 변수의 같은 타입을 *확인*하고 *캐스팅*하는 두 줄이 9번 반복된다. 한 줄 한 줄이 *끔찍한 일*은 아니지만, 한 화면에 모인 모습을 보면 그 누적이 *끔찍하다*. 사다리의 어느 한 칸이라도 잘못 적혀 있으면 `ClassCastException`이 production에서 새벽에 깨운다. 들여쓰기가 깊어지면서 가독성도 같이 떨어진다.

이쯤 되면 한 번쯤 묻게 된다. **캐스트 사다리, 이게 정말 최선이었을까?** 자바 이외의 거의 모든 현대 언어가 이 자리를 *pattern matching*으로 풀고 있다. Scala의 `match`, Kotlin의 `when`, Rust의 `match`, F#의 `match`, Swift의 `switch`. 같은 도구가 자바에 마침내 왔다 — Java 16의 `instanceof` 패턴(JEP 394)에서 시작해, Java 21의 switch 패턴(JEP 441)과 record 패턴(JEP 440)으로 완성되고, Java 22의 unnamed pattern(JEP 456)으로 다듬어진 그 도구.

이 장이 *Modern Java Bible의 미학적 클라이맥스*다. 앞 두 장에서 모은 records와 sealed가 이 장의 pattern matching과 만나면, Brian Goetz가 *Data-Oriented Programming in Java*라고 부른 한 묶음이 완성된다. *Records + Sealed + Pattern = 삼위일체*. 표현식 평가기, HTTP Result, Workflow 상태기계 — 세 본격 예제로 그 삼위일체가 현실 도메인에서 어떻게 풀려 들어오는지를 함께 살펴보자. 그리고 마지막에는 다음 장(14장 Virtual Threads)으로 가는 다리를 놓자. *도메인을 ADT로 모델링했으니, 그 도메인 위에서 동시성을 다시 생각해보자*는 다리다.

### preview의 8년 — 연표로 한 번에

자바의 pattern matching은 *6년에 걸쳐 7단계의 preview*를 거쳐 완성됐다. 그 흐름을 본문에서 한 단계씩 따라가는 일은 *지긋지긋*하다. 한 박스로 압축하자.

> **연표 박스 — Pattern Matching의 8년**
>
> - **JEP 305 (Java 14, 2020)** — pattern matching for `instanceof` 1차 preview. 자바 사상 처음으로 패턴이라는 어휘가 들어왔다.
> - **JEP 394 (Java 16, 2021)** — `instanceof` 패턴 표준. `if (x instanceof Point p)`의 그 형태.
> - **JEP 406 (Java 17, 2021)** — switch에 패턴이 1차 preview로 등장.
> - **JEP 420 (Java 18, 2022)** — switch 패턴 2차 preview. guard가 `&&`에서 `when`으로 바뀌는 굵직한 디자인 결정이 이 단계에서 내려진다.
> - **JEP 427 (Java 19, 2022)** — 3차. `case null` 처리, dominance 검사가 정착.
> - **JEP 432, 440 (Java 20, 2023)** — record pattern preview. `case Point(int x, int y)`라는 분해 문법이 등장.
> - **JEP 441 (Java 21, 2023)** — *switch 패턴 표준*. record pattern도 함께 표준화(JEP 440).
> - **JEP 456 (Java 22, 2024)** — *unnamed pattern* `_` 표준. 쓰지 않는 컴포넌트를 명시적으로 무시.

8년이다. 자바답다. records와 sealed가 2~3년에 표준에 도달한 데 비해, pattern matching은 *언어의 분기 의미론을 새로 짜는 일*이라 신중함이 곱절로 들어갔다. `case`의 의미가 fall-through 기반에서 arrow 기반으로, 그리고 *데이터 분해*까지 받아들이는 자리로 *바뀐 것*이다. 자바의 신중함이 가장 보수적으로 작동한 자리다.

본문에서는 *21 표준과 22 unnamed*에 집중하자. 그 둘이 우리가 매일 적을 코드의 99%다.

### 가장 작은 패턴 — `instanceof` 분해

도입부 캐스트 사다리의 한 칸을 떼어내자.

```java
if (response instanceof SuccessResponse) {
    SuccessResponse s = (SuccessResponse) response;
    // s 사용
}
```

`instanceof`로 확인하고, 같은 줄을 한 번 더 적어 캐스팅한다. 같은 의도를 두 번 적는다. *번거롭다*. 어디서 본 듯한 *지루함*이다.

Java 16의 JEP 394로 이 두 줄이 한 줄이 됐다.

```java
if (response instanceof SuccessResponse s) {
    // s 사용 — 이미 SuccessResponse 타입
}
```

`SuccessResponse s`. 이것이 *type pattern*의 가장 작은 형태다. 매칭이 성공하면 `s`라는 *binding 변수*가 자동으로 생기고, 그 변수의 타입은 `SuccessResponse`다. 캐스팅이 필요 없다. `if` 블록 안에서 `s`를 *그대로 쓰면 된다*.

흥미로운 자리가 한 군데 있다. `s`의 스코프는 *매칭이 성공하는 분기*에 자동으로 묶인다.

```java
if (!(response instanceof SuccessResponse s)) {
    return ResponseEntity.badRequest().build();
}
// 여기에서 s가 살아 있다 — 실패 분기에서 일찍 return했기 때문에
return ResponseEntity.ok(s.getPayload());
```

*flow scoping*이라 부르는 이 동작이다. early return으로 실패 분기를 끊어내면, 나머지 본문에서 `s`가 *살아남는다*. guard clause 스타일의 코드에 자연스럽다. 컴파일러가 *변수의 정의 가능 위치*를 흐름 분석으로 추적하기 때문에 가능한 일이다. 자바 14의 effectively final 추적과 같은 결의 일이 패턴에서 한 번 더 일어난 셈이다.

### switch가 패턴을 만나면 — Java 21의 본격

`instanceof` 패턴이 길어지면 결국 *분기의 나열*이 된다. 도입부 사다리가 정확히 그것이다. 그래서 분기의 나열은 switch가 가장 잘 다룬다. Java 21에 들어서면서 switch가 *type을 case 라벨로* 받는다.

같은 컨트롤러를 sealed `Response`와 switch 패턴으로 다시 적자.

```java
public sealed interface Response {
    record SuccessResponse(Payload payload) implements Response {}
    record ErrorResponse(String code, String message) implements Response {}
}

public ResponseEntity<?> handle(Response response) {
    return switch (response) {
        case SuccessResponse s -> ResponseEntity.ok(s.payload());
        case ErrorResponse e   -> ResponseEntity.status(400).body(e);
    };
}
```

9단 사다리가 4줄로 무너졌다. 그리고 *더 중요한 일이 일어났다* — 컴파일러가 이 switch의 *완전성을 검증*한다. `Response`가 sealed로 `SuccessResponse`와 `ErrorResponse` 둘만 허용하므로, 두 case가 모든 가능성을 덮는다. *default가 필요 없다*. 새 sub-type — 예를 들어 `PartialResponse` — 가 sealed에 추가되는 순간 이 switch는 컴파일 에러로 갱신을 요구한다.

화살표 `->`의 의미를 짚자. 전통적인 `case ... :` + `break;`의 fall-through 모델이 아니다. 화살표 case는 *해당 분기만 실행*한다. switch가 expression일 때(위처럼 값을 반환할 때) `yield`나 명시적 return으로 값을 내보낸다. fall-through의 그 묵은 *찜찜함*이 화살표 한 번으로 정리됐다.

### guard — `when`으로 조건을 잇는다

타입 매칭에 더해, 한 가지 추가 조건이 필요한 자리가 자주 있다. 예를 들어 "성공 응답이되 payload가 5MB를 넘으면 다른 처리"라는 식. 이걸 case 안에서 `if`로 다시 풀면 *흐름이 한 번 꺾인다*. switch 패턴은 그 자리를 `when`이라는 키워드로 받는다.

```java
return switch (response) {
    case SuccessResponse s when s.payload().sizeBytes() > 5_000_000
        -> ResponseEntity.status(413).body("Payload too large");
    case SuccessResponse s -> ResponseEntity.ok(s.payload());
    case ErrorResponse e   -> ResponseEntity.status(400).body(e);
};
```

`when` 절에는 *binding 변수를 자유롭게 활용한 boolean 표현식*이 들어간다. guard라 부른다. guard가 있는 case는 같은 타입의 *guard 없는 case*보다 *위에* 와야 한다 — 위에서부터 첫 매칭으로 분기하므로. 컴파일러가 이 순서까지 챙겨준다. *dominance check*라 부른다. 만약 guard 없는 case가 먼저 오면 그 아래의 guard case가 *영원히 도달 불가능*해진다는 에러를 컴파일러가 일으킨다.

설계 결정에 한 가지 흥미로운 점이 있다. 자바의 guard는 `when`이지 `&&`가 아니다. 첫 preview(JEP 406)에서는 `&&`였다. 그러나 산업 피드백을 받으며 `when`으로 바뀌었다(JEP 420). `&&`이면 일반 boolean과 *시각적으로 구별되지 않는다*는 비판이 있었다. `when`이라는 *영어 단어*가 들어가면서 "여기서부터는 guard"라는 의미가 *읽는 사람에게 명시적*이 된다. 작은 단어 하나의 결정이지만, 8년 preview의 신중함이 만든 결정이다.

> **JLS 인용 박스 — §14.30 Patterns**
>
> *원문* — "A pattern describes a structure that a value may match. Pattern matching is the process of testing whether a value matches a pattern, and if so, deconstructing it."
>
> *번역* — "패턴은 어떤 값이 매칭될 수 있는 *구조*를 기술한다. 패턴 매칭이란 *값이 그 패턴에 매칭되는지를 검사하고, 매칭되면 그 값을 분해하는* 과정이다."
>
> *해설* — 핵심 단어가 두 개다. *structure*, 그리고 *deconstructing*. 패턴은 단순한 타입 검사가 아니라 *값의 구조를 기술하는 어휘*다. 그 구조를 *분해*해서 컴포넌트에 이름을 붙이는 일이 패턴 매칭의 본질이다. 이 정의 한 줄이 자바를 *Java 8 시절의 캐스트 사다리 언어*에서 *함수형 분해를 아는 언어*로 옮긴 분기점이다.
>
> *본문 연결* — 다음 절에서 다룰 record 패턴이 이 *deconstructing*의 정확한 사례다. record header에 적힌 컴포넌트가 곧 *분해 가능한 구조*이고, 패턴 매칭은 그 구조를 *역방향으로 푸는* 어휘다.

### record pattern — 컴포넌트를 한 줄에 풀어내다

지금까지의 `case SuccessResponse s`는 *타입만 매칭*하고 컴포넌트는 분해하지 않았다. record pattern은 그 마지막 한 발을 더 간다.

```java
return switch (response) {
    case SuccessResponse(Payload p) -> ResponseEntity.ok(p);
    case ErrorResponse(String code, String message) -> ResponseEntity.status(400).body(code + ": " + message);
};
```

`SuccessResponse(Payload p)`. record header를 *그대로 패턴*으로 적었다. 매칭이 성공하면 `p`라는 binding이 컴포넌트의 값으로 채워진다. `ErrorResponse(String code, String message)`는 *두 컴포넌트를 한 번에* 분해했다. 분해된 변수가 case 본문에서 바로 쓰인다.

`var`로 받는 줄임도 있다.

```java
case ErrorResponse(var code, var message) -> ...
```

코드의 의도에 따라 타입을 명시할지, `var`로 줄일지 선택하면 된다. 컴포넌트가 한두 개일 때는 `var`가 자연스럽고, 컴포넌트가 많거나 의미가 모호할 때는 명시적 타입을 권한다.

### 중첩 분해 — 도메인이 깊어질 때

도메인 모델이 자라면 record가 다른 record를 컴포넌트로 가진다. 그 깊이까지 패턴이 *재귀적으로* 따라간다.

```java
public record Point(int x, int y) {}
public record Line(Point start, Point end) {}

double slope(Line line) {
    return switch (line) {
        case Line(Point(int x1, int y1), Point(int x2, int y2))
            when x1 != x2 -> (y2 - y1) / (double)(x2 - x1);
        case Line(Point p1, Point p2) -> Double.POSITIVE_INFINITY;  // 수직선
    };
}
```

`Line(Point(int x1, int y1), Point(int x2, int y2))`. record 안의 record를 한 번에 분해했다. 컴포넌트 네 개가 한 줄에 펼쳐진다. 도입부의 캐스트 사다리 9단이 *분해 한 줄*이 됐다.

이 자리에서 자바가 *Scala·Rust·Haskell과 같은 어휘*를 받아들였다는 사실을 다시 확인하자. 함수형 언어들은 30년 동안 데이터 구조를 *역방향으로 분해*하는 도구로 패턴을 다듬어왔다. 자바가 그 도구를 자기 어휘로 받았다. records가 product type을 *만드는* 어휘라면, record pattern은 그 product를 *분해하는* 어휘다. 둘은 *짝패*다.

### unnamed pattern `_` — 무시할 권리 (Java 22)

깊은 분해를 적다 보면 한 가지 *작은 불편*에 부딪힌다. 신경 쓰지 않는 컴포넌트까지 *이름을 지어야* 한다는 점이다. 위 `slope` 함수의 *수직선 분기*에서 `Line(Point p1, Point p2)`라고 적었는데, `p1`과 `p2`를 본문에서 쓰지 않는다. 안 쓰는 이름 두 개가 *어색하게* 남아 있다.

Java 22의 JEP 456이 이 자리를 풀어준다. *unnamed pattern* `_`이다.

```java
double slope(Line line) {
    return switch (line) {
        case Line(Point(int x1, int y1), Point(int x2, int y2))
            when x1 != x2 -> (y2 - y1) / (double)(x2 - x1);
        case Line(Point _, Point _) -> Double.POSITIVE_INFINITY;
    };
}
```

`Point _`. "Point 타입이긴 한데, 그 내부 값에는 *관심이 없다*"는 명시적 선언이다. 이름이 사라지지 않는다 — 그 자리에 *익명*이라는 *명시적 표시*가 들어간다. *읽는 사람에게 의도가 더 분명해진다*. 안 쓸 변수에 어색한 이름을 지어 *찜찜하게* 남기던 일이 끝났다.

`_`는 *binding이 일어나지 않는다*. 같은 case 안에 `_`가 여러 개 나와도 충돌하지 않는다. 그 점이 *변수 이름*과 달라 정신적 부담이 적다.

### sealed + pattern = 완전성 (exhaustiveness)

여기까지 도구를 모았으니, sealed의 짝패 효과를 다시 짚자. switch가 *모든 가능성을 덮는지*를 컴파일러가 검사하는 그 기능 — **exhaustiveness**.

```java
sealed interface Shape permits Circle, Square, Triangle {}
record Circle(double radius) implements Shape {}
record Square(double side) implements Shape {}
record Triangle(double base, double height) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle(double r)      -> Math.PI * r * r;
        case Square(double s)      -> s * s;
        case Triangle(double b, double h) -> 0.5 * b * h;
    };
}
```

`default`가 없다. 그런데 컴파일러가 에러를 내지 않는다. `Shape`가 sealed로 세 sub-type을 *permits*하고, 위 switch가 셋을 모두 *case*로 받았으므로 *완전*하다. 컴파일러가 *그 사실을 안다*.

이제 누군가가 `Shape`에 `Hexagon`을 추가한다고 해보자. `permits` 목록에 `Hexagon`이 들어가는 순간, 위 `area` 함수의 switch가 *컴파일 에러*가 된다. "Hexagon이 빠졌다"고. 도메인이 자라는 자리를 *컴파일러가 우리 손에 쥐어준다*. enum + if 분기로는 결코 받을 수 없었던 *언어 차원의 안전망*이다.

JLS는 이 자리를 한 번 더 분명히 한다.

> **JLS 인용 박스 — §14.30.3 switch exhaustiveness**
>
> *원문* — "A `switch` block is exhaustive if it has no `default` clause and the set of patterns in its case labels covers all possible values of the selector expression."
>
> *번역* — "어떤 `switch` 블록이 `default` 절 없이도, case 라벨들의 패턴 집합이 *selector 표현식의 가능한 모든 값을 덮는다*면 그 switch는 *exhaustive*하다."
>
> *해설* — 단순한 syntactic 검사가 아니다. *type system 차원의 검사*다. sealed 계층의 `permits` 목록을 컴파일러가 들고, switch의 case 패턴 집합이 그 목록을 *모두 덮는지*를 검사한다. 덮으면 *default 없이도 통과*. 덮지 못하면 컴파일 에러. JLS의 이 한 문장이 *records + sealed + pattern*이라는 삼위일체의 *마지막 못*을 박는다.
>
> **synthetic default의 작은 비밀** — 한 가지 *내부 사정*이 있다. 컴파일러는 위와 같은 exhaustive switch를 바이트코드로 내릴 때, *synthetic default*를 자동으로 끼워 넣는다. 이유는 *separate compilation*. 클래스 A가 컴파일된 후, 라이브러리 B의 sealed 계층에 새 sub-type이 추가되고 *B만 재컴파일*되면, A의 switch가 그 새 sub-type을 받을 때 *런타임에 매칭에 실패*할 수 있다. 그 경우를 위해 `MatchException`을 던지는 default가 살짝 들어간다. 우리는 코드에서 보이지 않지만, 클래스 파일을 열어보면 거기 있다.

### 예제 1 — 표현식 평가기 (교과서적)

자, 도구를 모두 모았다. 이제 본격 예제 셋으로 들어가자. 첫 번째는 함수형 언어 교과서에 반드시 등장하는 그 예제 — *표현식 평가기*다.

`Num(3) + Mul(Add(Num(2), Num(4)), Num(5))` 같은 수식 트리를 만들어 평가하는 일이다. 자바 8 시절이면 `interface Expr` + 추상 클래스 + Visitor 패턴으로 60줄을 적었을 것이다. records + sealed + pattern으로는 이렇게 된다.

```java
public sealed interface Expr {
    record Num(int value) implements Expr {}
    record Add(Expr left, Expr right) implements Expr {}
    record Mul(Expr left, Expr right) implements Expr {}
}

public class Evaluator {
    public static int eval(Expr expr) {
        return switch (expr) {
            case Expr.Num(int v) -> v;
            case Expr.Add(Expr l, Expr r) -> eval(l) + eval(r);
            case Expr.Mul(Expr l, Expr r) -> eval(l) * eval(r);
        };
    }

    public static void main(String[] args) {
        Expr e = new Expr.Mul(
            new Expr.Add(new Expr.Num(2), new Expr.Num(4)),
            new Expr.Num(5)
        );
        System.out.println(eval(e));  // 30
    }
}
```

20줄 안쪽. 그러면서 컴파일러가 *세 가지 case가 Expr의 sub-type을 모두 덮는다*는 사실을 안다. `default`가 없다. 새 연산 — 예를 들어 `Sub` — 을 sealed에 추가하면 `eval`이 컴파일 에러로 갱신을 요구한다.

이 예제가 교과서적인 이유가 있다. *재귀적 데이터 구조*와 *재귀적 분기*가 같은 형태로 짝지어진다. `Add(Expr l, Expr r)`라는 record 패턴이 *데이터 구조를 그대로 그려내고*, `eval(l) + eval(r)`이 *그 구조 위의 연산을 그대로 그려낸다*. 데이터의 모양과 코드의 모양이 *일치*한다. 함수형 프로그래밍이 30년 동안 자랑해온 그 *대응*이 자바에 들어왔다.

여기에 *덧셈에서 0 더하기 같은 사소한 경우를 미리 제거*하는 *상수 폴딩(constant folding)*을 한 줄 더 붙여보자. guard가 빛나는 자리다.

```java
public static Expr simplify(Expr expr) {
    return switch (expr) {
        case Expr.Add(Expr.Num(int v1), Expr.Num(int v2)) -> new Expr.Num(v1 + v2);
        case Expr.Mul(Expr.Num(int v1), Expr.Num(int v2)) -> new Expr.Num(v1 * v2);
        case Expr.Add(Expr l, Expr.Num(int v)) when v == 0 -> simplify(l);
        case Expr.Add(Expr.Num(int v), Expr r) when v == 0 -> simplify(r);
        case Expr.Mul(Expr l, Expr.Num(int v)) when v == 1 -> simplify(l);
        case Expr.Add(Expr l, Expr r) -> new Expr.Add(simplify(l), simplify(r));
        case Expr.Mul(Expr l, Expr r) -> new Expr.Mul(simplify(l), simplify(r));
        case Expr.Num n -> n;
    };
}
```

여덟 줄에 *컴파일 타임 폴딩 + 항등원 제거 + 일반 재귀*가 모두 들어갔다. Visitor 패턴으로 이걸 적었더라면 100줄을 넘었을 것이다. 그리고 컴파일러는 여전히 *모든 sub-type이 덮였는지*를 검사한다.

### 예제 2 — HTTP `Result<T, E>` (현실 도메인) {#sec-result-http}

교과서를 떠나 *현실 도메인*으로 옮기자. HTTP API 호출은 두 가지 결과 중 하나다 — *성공*이거나 *실패*. 자바 8 시절에는 이를 *checked exception*이나 *nullable 반환*으로 풀었다. 둘 다 *찜찜한 코드*를 만들었다.

함수형 진영의 답은 명확하다. `Result<T, E>`. 성공이거나 실패. 두 경우 각각이 *서로 다른 데이터*를 가진다. sealed가 정확히 받아낼 모양이다.

```java
public sealed interface Result<T, E> {
    record Ok<T, E>(T value) implements Result<T, E> {}
    record Err<T, E>(E error) implements Result<T, E> {}
}

public record HttpError(int status, String code, String message) {}

public Result<OrderResponse, HttpError> getOrder(String orderId) {
    try {
        var response = httpClient.send(buildRequest(orderId), JsonHandler.of(OrderResponse.class));
        return switch (response.statusCode()) {
            case 200 -> new Result.Ok<>(response.body());
            case 404 -> new Result.Err<>(new HttpError(404, "NOT_FOUND", "Order not found"));
            case int s when s >= 500 -> new Result.Err<>(new HttpError(s, "SERVER_ERROR", "Upstream failure"));
            default -> new Result.Err<>(new HttpError(response.statusCode(), "UNKNOWN", ""));
        };
    } catch (IOException | InterruptedException e) {
        return new Result.Err<>(new HttpError(0, "IO_ERROR", e.getMessage()));
    }
}
```

응답을 받아 *예외를 던지지 않고* `Result`로 감싼다. 호출 측은 어떻게 받는가?

```java
Result<OrderResponse, HttpError> result = client.getOrder("ord-42");

String userMessage = switch (result) {
    case Result.Ok<OrderResponse, HttpError>(OrderResponse order)
        -> "주문 " + order.orderId() + " 상태: " + order.status();
    case Result.Err<OrderResponse, HttpError>(HttpError(int status, String code, String _))
        when status == 404 -> "주문을 찾을 수 없습니다";
    case Result.Err<OrderResponse, HttpError>(HttpError(int status, var code, var msg))
        when status >= 500 -> "서버에 문제가 있습니다, 잠시 후 다시 시도해주세요";
    case Result.Err<OrderResponse, HttpError>(HttpError(var status, var code, var msg))
        -> "오류: " + code;
};
```

`HttpError` record를 *중첩 분해*하면서, *상태 코드별로 다른 메시지*를 만든다. guard가 *상태 코드 범위*를 받아내고, unnamed pattern이 *쓰지 않는 메시지*를 무시한다. 캐스트가 한 번도 등장하지 않고, `null`이 한 번도 등장하지 않고, 분기를 빠뜨릴 가능성이 0이다. *컴파일러가 그 모든 보증을 들고 있다*.

이 패턴이 Rust의 `Result<T, E>`와 거의 같은 모양이라는 점을 잠시 짚자. Rust 사용자라면 위 코드가 *문법만 다를 뿐 동일한 어휘*로 읽힌다. 자바가 함수형 진영의 *오랜 어휘*를 자기 것으로 받았다는 사실을 코드 한 덩이가 증명한다.

Spring의 `RestClient`나 `WebClient`를 사용하는 자리에서 이 `Result`가 자주 등장한다. 예외 기반 에러 처리와 결과 기반 에러 처리를 *섞지 않고*, 도메인 경계에서 한 번 변환한 뒤 *내부에서는 일관되게 Result*로 흐르게 하는 패턴이다.

### 예제 3 — Workflow 상태기계

세 번째 예제로 *주문 워크플로우의 상태기계*를 보자. 12장에서 잠시 짚은 결제 상태가 *단순한 결과*였다면, 워크플로우는 *상태 간의 *전이*를 모델링하는 일*이다. enum + flag 필드로 적던 그 자리다.

```java
public sealed interface OrderState {
    record Pending(Instant createdAt) implements OrderState {}
    record Paid(Instant createdAt, Instant paidAt, String paymentId) implements OrderState {}
    record Shipped(Instant createdAt, Instant paidAt, String paymentId,
                   Instant shippedAt, String trackingNumber) implements OrderState {}
    record Delivered(Instant createdAt, Instant paidAt, String paymentId,
                     Instant shippedAt, String trackingNumber, Instant deliveredAt) implements OrderState {}
    record Cancelled(Instant createdAt, Instant cancelledAt, String reason) implements OrderState {}
}
```

각 상태가 자기 정보를 *충분히 가진다*. `Pending`은 생성 시각만, `Paid`는 결제 시각과 ID, `Shipped`는 운송장 정보까지, `Delivered`는 도착 시각, `Cancelled`는 취소 사유. *상태에 따라 다른 데이터*라는 점이 자연스럽게 표현된다.

상태 전이도 switch 한 덩이에 담는다.

```java
public OrderState transition(OrderState current, OrderCommand command) {
    return switch (current) {
        case OrderState.Pending(var createdAt) -> switch (command) {
            case OrderCommand.Pay(var paymentId) ->
                new OrderState.Paid(createdAt, Instant.now(), paymentId);
            case OrderCommand.Cancel(var reason) ->
                new OrderState.Cancelled(createdAt, Instant.now(), reason);
            default -> throw new IllegalStateException("Pending에서 허용되지 않는 명령: " + command);
        };
        case OrderState.Paid(var createdAt, var paidAt, var paymentId) -> switch (command) {
            case OrderCommand.Ship(var trackingNumber) ->
                new OrderState.Shipped(createdAt, paidAt, paymentId, Instant.now(), trackingNumber);
            case OrderCommand.Cancel(var reason) ->
                new OrderState.Cancelled(createdAt, Instant.now(), reason);
            default -> throw new IllegalStateException("Paid에서 허용되지 않는 명령: " + command);
        };
        case OrderState.Shipped(var c, var p, var pid, var s, var t) -> switch (command) {
            case OrderCommand.Deliver _ ->
                new OrderState.Delivered(c, p, pid, s, t, Instant.now());
            default -> throw new IllegalStateException("Shipped에서 허용되지 않는 명령: " + command);
        };
        case OrderState.Delivered d ->
            throw new IllegalStateException("Delivered 상태에서는 전이 없음");
        case OrderState.Cancelled c ->
            throw new IllegalStateException("Cancelled 상태에서는 전이 없음");
    };
}
```

이중 switch — *외부는 상태, 내부는 명령*. 각 (상태, 명령) 조합에 대해 *허용되는 전이만* 코드에 적힌다. 허용되지 않는 조합은 명시적으로 거부한다. 상태와 데이터가 한 번 매칭되면, 그 데이터가 그대로 *다음 상태로 흘러 들어간다*. `Paid`의 `paymentId`가 `Shipped`로 그대로 옮겨가는 모습이 코드에 그려진다.

이런 모양을 *유한 상태기계(FSM)*라 부른다. 자바 8 시절에는 `Map<Pair<State, Command>, Transition>`이나 *Spring Statemachine* 같은 별도 라이브러리로 풀던 자리다. records + sealed + pattern으로 이 자리가 *언어 차원에서 표현 가능*해졌다. 별도 라이브러리 없이, 컴파일러의 보증을 받으면서.

여기에 한 가지 흥미로운 자리를 짚자. 위 코드에서 `default -> throw`가 등장하는데, 이 `default`가 *실제로는 도달하지 않을* 분기라면 어떨까? `OrderCommand`를 sealed로 만들어 *모든 명령을 명시적으로 분기*하면, `default` 자체가 사라진다. 그러면 새 명령이 추가될 때마다 *모든 상태의 switch*가 컴파일 에러로 갱신을 요구한다. 도메인이 자라는 자리를 *컴파일러가 우리 손에 쥐어준다*. 그 안전망이 production에서 *어느 새벽의 끔찍한 NPE*를 막아준다.

### Brian Goetz의 한 문단 — Data-Oriented Programming

이 자리에서 자바의 설계자 본인의 말을 한 번 인용하자. Brian Goetz가 2022년 InfoQ에 기고한 *Data-Oriented Programming in Java*의 핵심 문단이다.

> "Object-oriented programming says: combine code and data, and hide implementation details. Data-oriented programming says: separate code and data, make data immutable, and make illegal states unrepresentable.
>
> Records give us product types. Sealed classes give us sum types. Pattern matching gives us a way to take them apart. These three features together let us model data the way functional languages have for decades, but in idiomatic Java."

번역하자.

> "객체지향은 말한다 — *코드와 데이터를 묶고, 구현 세부를 감추라*. 데이터지향은 말한다 — *코드와 데이터를 분리하고, 데이터를 불변으로 만들고, 잘못된 상태가 표현되지 않도록 하라.*
>
> Records가 product type을 준다. Sealed가 sum type을 준다. Pattern matching이 그것들을 *분해할 도구*를 준다. 이 세 기능이 함께, 함수형 언어들이 *수십 년 동안* 해온 데이터 모델링을 *자바답게* 가능하게 해준다."

이 문단의 마지막 단어가 *idiomatic Java*다. 자바의 *문법답게*. 함수형 패러다임의 어휘를 자바로 *번역*해 들여온 것이 아니라, *자바답게 받아낸* 것이다. records의 `private final` 자동 부여, sealed의 `permits` 명시성, pattern의 `case`와 `when` — 모두 자바 사용자에게 *낯설지 않은 어휘*다. 자바답다.

*illegal states unrepresentable*이라는 표현도 음미하자. 잘못된 상태를 *표현할 수 없게* 만든다. enum + null이 표현했던 *"Pending인데 인증 URL이 null"* 같은 모양이 records + sealed에서는 *컴파일이 안 된다*. 잘못된 상태가 *코드로 적힐 수 없는* 자리에 못이 박힌다. 그것이 데이터지향 자바의 가장 큰 약속이다.

### Visitor 패턴의 사망 신고서

12장에서 Visitor 패턴의 *지긋지긋함*을 짚었다. 이 장의 도구를 모두 모은 자리에서, Visitor를 *한 줄 한 줄 ADT로 옮겨 보내자*. 4페이지 분량으로 한꺼번에.

같은 한 가지 도메인 — *식 표현식의 평가, 출력, 미분* — 을 Visitor와 ADT 두 방식으로.

**Visitor:**

```java
public abstract class Expr {
    public abstract <R> R accept(Visitor<R> v);
    public interface Visitor<R> {
        R visitNum(Num n);
        R visitAdd(Add a);
        R visitMul(Mul m);
    }
    // 세 sub-class 각각 약 10줄 — 생략
}

class Evaluator implements Expr.Visitor<Integer> {
    public Integer visitNum(Num n) { return n.value(); }
    public Integer visitAdd(Add a) { return a.left().accept(this) + a.right().accept(this); }
    public Integer visitMul(Mul m) { return m.left().accept(this) * m.right().accept(this); }
}

class Printer implements Expr.Visitor<String> {
    public String visitNum(Num n) { return String.valueOf(n.value()); }
    public String visitAdd(Add a) { return "(" + a.left().accept(this) + " + " + a.right().accept(this) + ")"; }
    public String visitMul(Mul m) { return "(" + a.left().accept(this) + " * " + a.right().accept(this) + ")"; }
}

class Differentiator implements Expr.Visitor<Expr> {
    private final String var;
    Differentiator(String var) { this.var = var; }
    public Expr visitNum(Num n) { return new Num(0); }
    public Expr visitAdd(Add a) { return new Add(a.left().accept(this), a.right().accept(this)); }
    public Expr visitMul(Mul m) {
        // 곱의 미분: (fg)' = f'g + fg'
        return new Add(
            new Mul(m.left().accept(this), m.right()),
            new Mul(m.left(), m.right().accept(this))
        );
    }
}
```

세 연산을 *세 개의 클래스*로 풀었다. 클래스마다 *세 visit 메서드*. 9개의 작은 메서드가 9개의 분기를 *객체로 모사*한다. 그리고 사용 측은 `expr.accept(new Evaluator())` 같은 호출을 적는다.

**ADT + Pattern matching:**

```java
public sealed interface Expr {
    record Num(int value) implements Expr {}
    record Add(Expr left, Expr right) implements Expr {}
    record Mul(Expr left, Expr right) implements Expr {}
}

public class Algebra {
    public static int eval(Expr e) {
        return switch (e) {
            case Expr.Num(int v) -> v;
            case Expr.Add(var l, var r) -> eval(l) + eval(r);
            case Expr.Mul(var l, var r) -> eval(l) * eval(r);
        };
    }

    public static String print(Expr e) {
        return switch (e) {
            case Expr.Num(int v) -> String.valueOf(v);
            case Expr.Add(var l, var r) -> "(" + print(l) + " + " + print(r) + ")";
            case Expr.Mul(var l, var r) -> "(" + print(l) + " * " + print(r) + ")";
        };
    }

    public static Expr differentiate(Expr e) {
        return switch (e) {
            case Expr.Num n -> new Expr.Num(0);
            case Expr.Add(var l, var r) -> new Expr.Add(differentiate(l), differentiate(r));
            case Expr.Mul(var l, var r) -> new Expr.Add(
                new Expr.Mul(differentiate(l), r),
                new Expr.Mul(l, differentiate(r))
            );
        };
    }
}
```

세 *함수*가 *한 클래스 안*에 모였다. 클래스를 따로 만들 필요 없고, accept-visit 왕복도 없다. 사용 측은 `Algebra.eval(expr)`을 그냥 호출한다.

Visitor 코드가 60줄 가까이 되는 데 비해, ADT 코드는 30줄. 그리고 컴파일러의 *완전성 보증*은 양쪽 다 같다. ADT 쪽은 *default가 필요 없으면서* 그 보증을 받는다.

Visitor 패턴은 *언어가 분기를 모르던 시절의 우회로*였다. 자바의 분기가 *데이터 분해를 알게* 된 순간, 그 우회로의 사용 이유가 사라졌다. *기존 Visitor 코드를 다 갈아치우자*는 말은 아니다. 그건 *지긋지긋한 작업*이 될 것이다. 그러나 *새로 적는 코드에 Visitor 패턴을 끌어들이지 말자*는 권유는 분명히 할 수 있다. 자바가 더 좋은 도구를 손에 쥐여줬으므로.

### Java 8 vs Java 21 — 한 도메인의 변천사

이 장의 마지막 비교로, 같은 한 가지 일 — *API 응답을 받아 사용자 메시지로 변환* — 을 11년 사이의 두 버전으로 적어보자.

**Java 8, 캐스트 사다리:**

```java
public String formatResponse(Object response) {
    if (response == null) {
        return "응답 없음";
    }
    if (response instanceof SuccessResponse) {
        SuccessResponse s = (SuccessResponse) response;
        if (s.getPayload() == null) {
            return "성공이지만 빈 응답";
        }
        if (s.getPayload() instanceof OrderCreated) {
            OrderCreated created = (OrderCreated) s.getPayload();
            return "주문 생성: " + created.getOrderId();
        }
        if (s.getPayload() instanceof PaymentApproved) {
            PaymentApproved approved = (PaymentApproved) s.getPayload();
            return "결제 승인: " + approved.getTransactionId();
        }
        return "알 수 없는 성공 응답";
    }
    if (response instanceof ErrorResponse) {
        ErrorResponse e = (ErrorResponse) response;
        if (e.getStatusCode() >= 500) {
            return "서버 오류: " + e.getMessage();
        }
        return "오류: " + e.getCode();
    }
    return "알 수 없는 응답 타입";
}
```

25줄. 들여쓰기 3단. instanceof + 캐스팅 6번. null 체크 2번. *알 수 없는*으로 끝나는 분기가 2개 — 이게 *진짜* 일어나야 하는 분기인지 *방어용*인지 코드를 읽어서는 알 수 없다. *찜찜한 코드*다.

**Java 21, sealed + pattern matching:**

```java
public sealed interface Response {
    record Success(Payload payload) implements Response {}
    record Error(int statusCode, String code, String message) implements Response {}
}

public sealed interface Payload {
    record OrderCreated(String orderId) implements Payload {}
    record PaymentApproved(String transactionId) implements Payload {}
}

public String formatResponse(Response response) {
    return switch (response) {
        case Response.Success(Payload.OrderCreated(var orderId))
            -> "주문 생성: " + orderId;
        case Response.Success(Payload.PaymentApproved(var txId))
            -> "결제 승인: " + txId;
        case Response.Error(int status, var code, var msg) when status >= 500
            -> "서버 오류: " + msg;
        case Response.Error(int status, var code, var _)
            -> "오류: " + code;
    };
}
```

15줄. 들여쓰기 1단. 캐스팅 0번. null 체크 0번. 그리고 *알 수 없는* 분기가 0개 — 모든 가능성이 sealed의 `permits`로 *명시적으로 닫혀 있기 때문*이다. 새 payload 타입이 추가되면 컴파일러가 그 사실을 *우리 손에 쥐어준다*.

11년이 두 코드 사이에 흘렀다. 그 11년 동안 자바는 *분기에 대한 자기 입장*을 *완전히 바꿔* 들었다. 이것이 modern Java의 미학이다.

### 14장으로 가는 다리 — 도메인을 ADT로 모델링했다면

여기까지가 데이터지향 자바의 *삼위일체*다. records로 *불변 데이터*를 정의하고, sealed로 *닫힌 대안*을 표명하고, pattern matching으로 *그것들을 분해*한다. 도메인이 코드에 *자연스럽게* 그려진다. 잘못된 상태는 *코드로 적힐 수 없다*.

자, 이 도메인 위에서 한 발 더 나가자. *동시성*이다.

생각해보자. 우리는 위 예제 2에서 HTTP API 호출을 `Result<OrderResponse, HttpError>`로 받았다. 만약 API 호출이 *세 개*라면? *외부 결제 게이트웨이 + 재고 시스템 + 회원 정보 시스템* — 세 API를 *병렬*로 호출하고, 세 결과가 모두 도착한 후에 결합해야 한다고 해보자.

Java 8 시절에는 `CompletableFuture.allOf`로 풀었다. 풀리긴 했다. 그러나 *Result로 감싼 결과 셋*을 합치는 코드는 *지긋지긋하게* 길었다. 그리고 `ForkJoinPool.commonPool()`에 blocking I/O를 태운 *끔찍한 사건*들도 동시에 일어났다.

Java 21의 *virtual threads*가 그 자리를 풀어준다. 다음과 같이 적힌다.

```java
public Result<OrderSummary, HttpError> compose(String orderId) {
    try (var scope = StructuredTaskScope.open()) {
        var paymentFuture = scope.fork(() -> paymentClient.get(orderId));
        var inventoryFuture = scope.fork(() -> inventoryClient.get(orderId));
        var memberFuture = scope.fork(() -> memberClient.get(orderId));

        scope.join();

        var payment = paymentFuture.get();
        var inventory = inventoryFuture.get();
        var member = memberFuture.get();

        return switch (payment) {
            case Result.Err<?, HttpError>(var err) -> new Result.Err<>(err);
            case Result.Ok<Payment, HttpError>(var p) -> switch (inventory) {
                case Result.Err<?, HttpError>(var err) -> new Result.Err<>(err);
                case Result.Ok<Inventory, HttpError>(var i) -> switch (member) {
                    case Result.Err<?, HttpError>(var err) -> new Result.Err<>(err);
                    case Result.Ok<Member, HttpError>(var m)
                        -> new Result.Ok<>(new OrderSummary(p, i, m));
                };
            };
        };
    }
}
```

`StructuredTaskScope`로 세 task를 *구조적으로* 묶고, 각 결과를 *pattern matching으로 분해*한다. virtual thread가 *세 호출의 blocking을 OS thread 없이* 견뎌낸다. 13장의 sealed `Result`가 14장의 virtual thread와 *그대로 만난다*.

다음 장에서는 *왜 이제야 thread-per-request가 가능해졌는지*를 시작점으로, virtual thread의 정체와 한계를 함께 살펴보자. 100 thread 풀로 버티던 *답답함*이 어떻게 풀려나는지, 그러나 켰는데 오히려 deadlock이 나는 *끔찍한 새벽*은 왜 일어나는지를. 도메인을 ADT로 모델링한 자리에서 *그 도메인 위의 동시성*을 다시 짜는 일이 시작된다.

기억해두자. records + sealed + pattern은 *언어가 데이터를 인정한 어휘*다. 그 어휘 위에 동시성과 메모리와 네이티브가 차곡차곡 쌓인다. 자바 11년의 변화가 *왜 이 자리에서 가장 아름다운지*를, 다음 장의 virtual thread에서 한 번 더 확인하자.

---

# Part VII. 동시성 II — Loom 시대

Project Loom — Virtual Thread, Structured Concurrency, Scoped Values — 가 자바에 들어왔다. 이 변화의 크기를 한 문장으로 말하자면, *thread-per-request 모델이 부활했다*는 것이다. Reactive Streams로 우회하던 그 길이 다시 *thread를 그냥 쓰면 되는* 길로 바뀌었다. 그러나 그 변화는 단순한 *되돌림*이 아니다. 옛 thread-per-request와는 *근본부터 다른* 모델이 그 자리에 들어왔다.

14장은 Virtual Thread의 *왜*와 *어떻게*를 본다. Tomcat 200 thread 풀로 p99 800ms를 버티던 그 답답함이 어떻게 풀리는지, `Thread.startVirtualThread()` 한 줄의 호출 뒤에 어떤 carrier thread의 mounting/unmounting이 벌어지는지, `Continuation`이라는 옛 OpenJDK 아이디어가 어떻게 표면 위로 올라왔는지를 본다. *thread가 더 이상 비싼 자원이 아니라는 사실*이 코드의 모양을 어떻게 바꾸는지가 이 장의 핵심이다.

15장은 *Pinning*과 *ThreadLocal* — Virtual Thread가 우리를 *실망시키는 자리*를 본다. `synchronized` 블록 안에서 blocking I/O를 부르면 어떤 일이 벌어지는지, JFR의 `jdk.VirtualThreadPinned` 이벤트로 그것을 어떻게 진단하는지, HikariCP의 옛 버전과 옛 JDBC 드라이버가 어떻게 함정이 되는지, 그리고 JEP 491(Java 24)이 `synchronized`의 pinning을 어떻게 *마침내* 해결했는지. Virtual Thread는 *그냥 켜면 빨라지는 도구*가 아니다. 옛 코드와의 *마찰*을 이해해야 비로소 그 힘을 쓸 수 있다.

16장은 Structured Concurrency와 Scoped Values다. `StructuredTaskScope`가 fork-join을 *구조*로 표현하는 일, `ScopedValue`가 ThreadLocal 청소를 잊는 그 *찜찜함*을 어떻게 정리하는지, 그리고 둘이 묶이면 concurrent 코드에도 *언어의 문법*이 생긴다는 사실을 본다. Doug Lea가 80년대부터 그려온 *structured programming for concurrency*가 자바에 *마침내* 들어왔다.

이 세 장을 다 읽고 나면, 8A·8B의 옛 동시성 모델이 어떻게 새 모델로 옮겨갔는지가 한 줄로 이어진다. 11년의 자바에서 *가장 무거운 한 변화*가 이 부에 묶여 있다.

---

## 14장. Virtual Threads — thread-per-request의 부활

Tomcat 200 thread 풀로 한 달을 버틴 끝에 p99가 800ms였다고 해보자. 새벽 트래픽이 몰리는 두 시간 동안 응답 시간 그래프는 진동했고, 그 진동을 가라앉히려고 풀 사이즈를 300으로 늘렸더니 메모리가 답답한 소리를 내며 컨테이너 limit에 부딪혔다. 이상하다. CPU 사용률은 30%를 넘지 않는다. 컨트롤러가 하는 일이라곤 외부 결제 API 하나, 회원 조회 API 하나, 쿠폰 검증 API 하나를 합치는 것뿐이다. 세 호출이 각 100ms씩 걸린다 치자. 한 요청이 300ms를 잡고 있는 동안 thread는 거의 100% idle이다. 그저 대기할 뿐이다. 그런데도 풀이 모자란다. 답답하지 않은가.

이 답답함을 해결하겠다고 등장했던 것이 reactive였다. WebFlux를 도입한 옆 팀의 코드를 본 적이 있을 것이다. `Mono`와 `Flux`가 메서드 시그니처마다 따라다니고, `subscribe`·`flatMap`·`zipWith`로 흐름을 다시 짜야 하고, `StackOverflowError`가 났을 때 stack trace는 어디서부터 봐야 할지 알 수 없는 추상의 사다리를 그리고 있다. 그런 코드를 짜고도 같은 팀의 절반은 *operator semantics*를 정확히 설명하지 못한다. 그렇다면, 묻고 싶어진다. 왜 이제야 thread-per-request가 가능해졌을까. 왜 자바는 30년 동안 OS thread에 묶인 채 살아왔을까. 그리고 지금 우리가 켤 수 있다는 그 *virtual thread*는, 정말 reactive 없이도 충분히 빠르다는 약속을 지킬 수 있을까.

### 회수: 13장의 `Result<T,E>`를 다시 꺼내자 {#sec-result-recall}

본격적으로 들어가기 전에, 13장에서 만들었던 sealed `Result<T,E>` 타입을 다시 꺼내 보자. virtual thread를 다루는 첫 코드에 이 타입이 등장하는 데는 이유가 있다. virtual thread가 하는 일은 본질적으로 *blocking 호출의 결과*를 받아 합치는 일이다. 그 결과는 성공일 수도, 실패일 수도 있다. 우리는 13장에서 이미 그 두 갈래를 한 자리에 묶는 방법을 익혔다.

```java
sealed interface Result<T, E> permits Ok, Err {
    record Ok<T, E>(T value) implements Result<T, E> {}
    record Err<T, E>(E error) implements Result<T, E> {}
}
```

가령 결제 API와 회원 조회와 쿠폰 검증을 동시에 호출하고, 세 결과를 모두 모은 뒤 하나라도 실패하면 사용자에게 명확한 도메인 에러를 돌려주고 싶다고 해보자. 이전이라면 `CompletableFuture<Result<...>>`를 줄줄이 엮어 `allOf`로 모으고 `get()`에서 예외를 잡았을 것이다. virtual thread를 쓰면 그 코드는 *그냥 synchronous하게* 적힌다.

```java
try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<Result<Payment, BillingError>> pay   = scope.submit(() -> billing.charge(orderId));
    Future<Result<Member, MemberError>>   mem   = scope.submit(() -> members.findById(userId));
    Future<Result<Coupon, CouponError>>   coup  = scope.submit(() -> coupons.validate(couponCode));

    return switch (pay.get()) {
        case Result.Ok<Payment, BillingError>(var p) -> switch (mem.get()) {
            case Result.Ok<Member, MemberError>(var m) -> switch (coup.get()) {
                case Result.Ok<Coupon, CouponError>(var c) -> CheckoutResponse.success(p, m, c);
                case Result.Err<Coupon, CouponError>(var e) -> CheckoutResponse.failed(e);
            };
            case Result.Err<Member, MemberError>(var e) -> CheckoutResponse.failed(e);
        };
        case Result.Err<Payment, BillingError>(var e) -> CheckoutResponse.failed(e);
    };
}
```

세 호출이 *동시에* 일어나고, 세 결과가 *순서 없이* 도착하지만, 코드 자체는 위에서 아래로 흐른다. 디버거를 걸면 평범한 stack trace가 한 줄로 보인다. 세 개의 외부 호출을 합치는 컨트롤러 — 이 장이 끝날 때까지 이 도메인을 들고 갈 것이다. 마음 한쪽에 결제·회원·쿠폰 세 API를 두고, virtual thread가 그것을 어떻게 *합리적인* 코드로 만들어주는지 추적해 가자.

(중첩 switch가 깊다고 느낀다면 — 그 감각이 옳다. 16장에서 `StructuredTaskScope`로 같은 코드를 한 단계 더 다듬을 것이다. 지금은 *virtual thread 자체*에만 집중하자.)

### 왜 이제야 가능해졌을까

자바가 등장한 1995년의 thread는 `green thread`였다. JVM이 user-level에서 스케줄링하는 가벼운 thread다. Solaris의 native thread 모델이 자리 잡으면서 1998년 무렵 Java 1.2는 green thread를 폐기하고 *OS thread = `java.lang.Thread`*라는 등식으로 옮겨갔다. 그 뒤로 27년이다. `Runnable`을 짜고 `new Thread(...).start()`를 호출하면 커널이 새 thread를 만들고, 스택을 1MB 예약하고, 스케줄러 큐에 올렸다. 이 등식이 자바의 모든 동시성 모델을 결정했다 — `ExecutorService`도, `ThreadPoolExecutor`도, Tomcat의 request handler도, 결국 같은 무거운 자원을 *재사용*하는 방식이었다.

OS thread는 비싸다. Linux x64에서 thread 하나당 약 1MB의 스택을 예약해 둔다. 1000개를 만들면 그것만으로 1GB다. 컨텍스트 스위치 비용도 무시할 수 없어서, 수만 개를 띄우면 스케줄러가 먼저 휘청거린다. 그래서 자바 개발자는 30년간 *thread pool*이라는 한 가지 답을 써왔다. 200개, 400개, 많아야 1000개. 그 풀 안에서 요청들이 줄을 서서 thread를 빌려 쓰고 돌려준다.

문제는 풀이 모자랄 때다. 한 요청이 외부 API 응답을 기다리는 동안 thread는 차지된 채 *아무 일도 하지 않는다*. CPU는 한가한데 풀은 비어 있는 모순이 일어난다. p99가 800ms로 솟구치는 새벽의 답답함이 바로 이 모순이다. CPU를 더 사면 해결되는 문제가 아니다. *thread 자체가 비싸기 때문*에 일어나는 문제다.

reactive는 이 모순을 다른 방향에서 풀려고 했다. "blocking I/O를 쓰지 말자. 모든 I/O를 non-blocking event로 모델링하고, callback이나 stream으로 결과를 받자." 똑똑한 답이다. 그러나 모든 외부 라이브러리가 non-blocking이 아니다. JDBC는 30년째 blocking이다. 한 자리에서 reactive를 쓰려면 *모든 자리*에서 reactive를 써야 한다. 함수 시그니처가 전염되고, 에러 핸들링이 새로운 어휘로 다시 짜인다. *기존 자바 코드가 그대로 돌지 않는다*는 결정적 비용이 따라붙는다.

Project Loom의 동기는 정확히 그 자리에서 출발했다. Ron Pressler를 비롯한 OpenJDK 팀의 답은 단순했다. "blocking I/O를 그대로 쓰자. 단, thread 자체를 싸게 만들자." OS thread를 그대로 둔 채, JVM이 관리하는 *가벼운 thread*를 새로 도입한다. blocking 호출이 들어오면 그 thread는 OS thread에서 *unmount*되고 다른 thread가 OS thread를 빌려 쓴다. 풀의 크기를 늘리는 대신, thread의 단가를 낮춘다.

### Virtual Thread란 무엇인가

JEP 444의 정의를 정직하게 인용하는 편이 낫다.

> A virtual thread is an instance of `java.lang.Thread` that is not tied to a particular OS thread. A platform thread, by contrast, is a `Thread` implemented in the traditional way, as a thin wrapper around an OS thread. — JEP 444

핵심은 *`java.lang.Thread`의 인스턴스*라는 점이다. 새로운 타입이 아니다. 같은 API다. `Thread.currentThread()`, `Thread.sleep()`, `InterruptedException`, `ThreadLocal` — 모두 그대로 동작한다. 30년 묵은 자바 코드가 *그대로* 돌아가야 한다는 호환성 제약을 OpenJDK 팀이 끝까지 지켜낸 결과다. 새 키워드도 없고, 새 동시성 어휘도 없다. 그저 thread의 *종류*가 둘이 됐을 뿐이다.

Brian Goetz는 이 명명에 대해 이런 비유를 했다. *virtual thread는 thread의 virtual memory*다. 물리 메모리보다 큰 환상의 메모리를 운영체제가 페이지로 매핑해주듯, 물리 thread보다 많은 환상의 thread를 JVM이 carrier thread로 매핑해준다. virtual memory를 처음 도입했을 때 개발자가 직접 페이지 in/out을 신경 쓸 필요가 없어진 것처럼, virtual thread를 도입한 지금 개발자가 thread pool 크기를 신경 쓸 필요가 없어진다. *thread는 자원이 아니라 표현 단위*가 된다. 30년 만에 자바가 그 자리에 도달했다.

API는 세 갈래다.

```java
// 1. 일회성
Thread.startVirtualThread(() -> System.out.println("hi"));

// 2. 빌더
Thread t = Thread.ofVirtual()
    .name("checkout-fanout-", 0)
    .uncaughtExceptionHandler((th, ex) -> log.error("uncaught", ex))
    .start(() -> doWork());

// 3. ExecutorService — 가장 흔히 쓰는 길
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> doWork());
}
```

`newVirtualThreadPerTaskExecutor()`라는 이름을 곱씹어 보자. *per task*다. task마다 새 virtual thread를 만든다. 이전 같으면 "thread를 한 번 쓰고 버린다고? 미친 짓이다"라고 답했을 일이지만, virtual thread에서는 그게 *합리적*이다. 만드는 비용이 거의 0에 가깝기 때문이다. 100만 개를 만들어도 OS는 모른다. JVM 안에서만 사는 객체이기 때문이다.

세 가지는 알아둘 만하다.

- **모든 virtual thread는 daemon이다.** `setDaemon(false)`를 호출하면 `IllegalArgumentException`이 난다. JVM 종료를 막을 권한이 없다는 뜻이다.
- **priority가 무시된다.** `setPriority(MAX_PRIORITY)`를 적어도 효과 없다. 스케줄링은 carrier pool이 알아서 한다.
- **thread group은 하나다.** 모든 virtual thread는 단일 공유 그룹 `"VirtualThreads"`에 속한다. thread group 기반의 옛 코드는 더 이상 의미가 없어진다.

이 세 가지는 thread가 *자원에서 표현 단위로* 옮겨갔다는 사실의 작은 증거다. daemon이냐 아니냐를 신경 쓸 필요가 없다. priority로 조정할 만큼 비싸지 않다. group으로 묶을 만큼 길게 살지 않는다.

### M:N 스케줄링: continuation으로 들여다보자

원리를 정확히 이해하고 싶다면 *continuation*이라는 추상부터 살펴보자. Project Loom의 진짜 코어는 virtual thread가 아니다. continuation이다. virtual thread는 continuation에 OS thread 비유를 입힌 *얼굴*일 뿐이다.

continuation은 "지금까지의 실행 상태를 통째로 들고 다닐 수 있는 일급 객체"다. 함수 호출의 한가운데서 일시 정지했다가, 나중에 *같은 자리에서* 재개할 수 있다. 자바의 내부 API로 `jdk.internal.vm.Continuation`이 존재하고, scope는 `jdk.internal.vm.ContinuationScope`로 묶인다. 일반 애플리케이션 개발자가 직접 만질 일은 없지만, virtual thread의 동작을 이해하려면 한 번은 들여다보는 편이 낫다.

virtual thread가 동작하는 흐름을 단순화하면 이렇다.

1. JVM은 `ForkJoinPool` 기반의 *carrier thread pool*을 유지한다. 기본 크기는 `Runtime.getRuntime().availableProcessors()`. CPU 코어 수만큼이다.
2. virtual thread가 `start()`되면 carrier 중 하나에 *mount*된다. 그 순간부터 virtual thread는 평범한 OS thread처럼 코드를 실행한다.
3. blocking 호출(예: `Socket.read()`, `Thread.sleep()`, `BlockingQueue.take()`)을 만나면 JVM은 continuation으로 현재 실행 상태를 캡처하고 virtual thread를 carrier에서 *unmount*한다. carrier는 자유로워져서 다른 virtual thread를 mount한다.
4. blocking이 풀리면 (소켓에 데이터가 도착하면) virtual thread는 *언젠가* 다시 carrier에 mount되어 같은 자리에서 재개한다.

핵심은 mount/unmount가 *코드 한 줄의 변경 없이* 일어난다는 점이다. JDK 내부의 `Socket`·`HttpClient`·`Files`·`BlockingQueue` 등 거의 모든 blocking 지점이 Loom-aware로 재작성됐다. `Socket.read()`를 호출하는 코드는 똑같이 보이지만, 그 안에서 JVM은 OS의 `epoll`을 쓰는 비동기 I/O로 변환해 처리한다. virtual thread가 unmount되어 있는 동안 carrier는 다른 일을 한다.

이게 곧 *M:N 스케줄링*이다. M개의 virtual thread가 N개의 carrier thread에 multiplex된다. M은 100만 수준까지 갈 수 있고, N은 CPU 코어 수다. Go의 goroutine과 똑같은 구조다. 다만 자바는 새 키워드(`go`) 없이, 기존 `Thread` API를 그대로 둔 채로 같은 결과를 얻는다.

조금 더 들여다보자. JVM은 carrier thread pool을 `ForkJoinPool`로 구현한다. 정확히는 `ForkJoinPool.commonPool()`이 아닌, virtual thread 전용 *별도* pool이다. `-Djdk.virtualThreadScheduler.parallelism`으로 크기를 조정할 수 있지만, 거의 모든 경우 기본값(코어 수)을 그대로 두는 편이 낫다. ForkJoinPool을 고른 이유는 work-stealing이다. carrier A가 한가해지면 carrier B의 큐에서 *대기 중인 virtual thread*를 가져와 mount한다. 그 결과 carrier들이 *균등하게* 일을 나눠 갖는다. 동시 요청이 들쭉날쭉해도 throughput이 안정적이다.

mount의 비용도 짚어두자. virtual thread를 새로 만드는 자체의 비용은 *수십 마이크로초*다. OS thread 생성이 *수 밀리초*인 것에 비하면 1000배 가까이 싸다. 100만 개를 만드는 일이 *합리적*이라는 말의 근거가 여기 있다. unmount/mount의 비용 — 한 carrier에서 다른 carrier로 옮겨가는 비용 — 도 마찬가지로 가볍다. continuation의 stack을 heap에 *통째로 옮기는 일*이 본질이지만, JVM이 그 일을 최적화해서 *대체로 자유롭게* 일어나도록 만들었다.

이 가벼움이 곧 *thread-per-request*의 부활을 가능하게 한 자리다. thread 자체가 비싸지 않으면 풀의 필요가 사라진다. 풀이 사라지면 큐가 사라지고, 큐가 사라지면 큐 대기 시간이 사라진다. p99의 답답함이 사라진다. 새벽의 800ms가 사라진다. *비싼 자원의 재사용*이라는 30년의 자바 모델이, 한 줄 — `newVirtualThreadPerTaskExecutor()` — 으로 무너진다.

### virtual thread vs goroutine vs async/await vs green thread

한국 개발자가 자주 묻는 질문이다. virtual thread는 결국 *옛 green thread*와 무엇이 다른가. goroutine을 흉내 낸 것 아닌가. C#의 `async/await`와는 어떻게 다른가. 표 하나로 정리해 두자.

| | virtual thread | goroutine | async/await | green thread (옛) |
|---|---|---|---|---|
| 통신 모델 | 공유 메모리 + lock·CAS | 채널 (CSP) | task/future + await | 공유 메모리 |
| 호환성 | 기존 `Thread` API 그대로 | 새 키워드 `go` | 시그니처 전염 (`async`) | 기존 API |
| blocking I/O | 자동 unmount (Loom-aware) | 자동 yield | 명시적 `await` | 협력적 yield |
| 스케줄링 | M:N work-stealing carrier pool | M:N work-stealing | 단일 event loop 다수 | user-level, OS 미연동 |
| 도입 시점 | 2023 (JDK 21) | 2009 (Go 1.0) | 2012 (C# 5) / 2017 (Python 3.6) | ~1998 (Java 1.1) |
| 사라진 이유 | — | — | — | OS thread 모델 채택 |

핵심을 짚자. virtual thread가 *함수 색깔(function color)* 문제에서 자유로운 점이 가장 큰 미덕이다. C#의 `async`는 `async` 함수에서만 `await`할 수 있고, `async` 함수를 호출한 함수는 자기도 `async`가 되어야 한다. 색깔이 전염된다. 그 결과 라이브러리는 `sync` 버전과 `async` 버전을 둘 다 제공해야 한다. virtual thread에는 색깔이 없다. `read()`는 `read()`다. blocking이면 unmount되고, non-blocking이면 그대로 진행한다. 함수 시그니처가 변하지 않는다.

green thread와의 차이도 정직하게 짚자. 1990년대 자바의 green thread는 *user-level*이었다. JVM 내부의 단일 OS thread 위에서 협력적으로 yield하는 모델이었다. 멀티 코어를 못 썼다. virtual thread는 다르다. carrier pool이 멀티 코어를 활용하고, JVM과 OS가 *함께* 비동기 I/O를 조율한다. 옛 green thread의 약점이었던 "한 thread가 OS-blocking syscall을 호출하면 모두가 멈춘다"는 문제가 *Loom-aware* 라이브러리 덕에 해소됐다. green thread의 이름은 같지만, 정체는 다른 도구다.

### 성능: 약속은 정직한가

OpenJDK가 약속한 것은 *throughput의 비약*이지 *latency의 비약*이 아니다. 이 차이를 정확히 짚어두자. virtual thread를 켜면 같은 요청 하나가 갑자기 빨라지지는 않는다. JDBC 호출 100ms는 그대로 100ms다. 빨라지는 것은 *동시에 처리할 수 있는 요청의 수*다. 800ms p99의 원인이 thread 풀이 모자라 큐에 쌓이는 것이었다면, 풀의 제약이 사라지면서 큐가 줄고 p99가 200ms로 떨어진다. 하지만 처음부터 큐가 짧았다면 p99는 거의 변하지 않는다.

이 약속이 production에서 어떻게 검증됐는지 보자. SoftwareMill의 벤치마크 *Limits of Loom's Performance*는 두 가지를 보여줬다. 첫째, virtual thread의 throughput은 Go의 goroutine과 비슷한 수준에 도달한다. 둘째, 결정적 차이는 자바 쪽에 있다 — *기존 자바 코드가 그대로 돌아간다*. Reactive Streams나 새 언어 키워드 없이, 11년 묵은 Spring MVC 코드가 그대로 throughput을 받는다. 이게 자바가 Loom에 11년을 투자한 가장 큰 회수다.

production 사례도 모이고 있다. Cashfree Payments는 *7 Key Lessons*라는 글에서 자기 인프라에 virtual thread를 도입한 경험을 정리했다. 결제 처리 서버 — 외부 은행 API와 카드사 게이트웨이를 합치는 fan-out 구조다. 도입 후 동일 부하에서 thread 풀이 사라지고, p99 latency가 의미 있게 떨어졌으며, container 메모리 사용량은 *늘었다*. 늘었다고? 그렇다, stack이 heap에 살기 때문이다. virtual thread는 OS 스택 1MB를 예약하지 않는 대신, 필요할 때 heap에서 작게 시작해 grow한다. heap 사용량이 ~30% 증가하는 것은 흔한 관찰이다. 컨테이너 limit을 그만큼 상향해 두는 편이 안전하다.

한국에서도 사례가 쌓이고 있다. 우아한형제들은 *"Java의 미래, Virtual Thread"* 기술 세미나와 후속 블로그에서 Loom 도입의 의미를 정리했다. 카카오는 제4회 Kakao Tech Meet *"JDK 21의 Virtual Thread"*에서 같은 주제를 다뤘다. 카카오페이는 *"Virtual Thread에 봄(Spring)은 왔는가"*에서 platform thread → virtual thread 전환을 실제로 측정한 결과를 공개했다. 자세한 수치는 15장에서 *함정과 한계*와 함께 짚을 테니, 지금은 *production에 들어가 있다*는 사실만 기억해 두자.

(SoftwareMill 벤치마크에서 한 가지 흥미로운 관찰이 있었다 — virtual thread는 *극단적인 throughput 한계*에서는 Go의 goroutine보다 약간 뒤처졌다. 그 차이는 work-stealing 스케줄러의 세부 구현, FFI 호출의 영향, 그리고 자바 객체의 메모리 footprint에서 온다고 분석됐다. 그러나 *production이 다루는 현실적인 throughput 영역*에서는 두 도구 모두 충분한 head room을 보여줬다. 실무자에게 의미 있는 결론은 — virtual thread를 도입하면서 *Go로 옮겨야 하는 이유*는 거의 사라졌다는 것이다. 자바의 ecosystem과 도구가 그대로 따라오기 때문이다.)

### 30년 자바 코드가 그대로 돈다는 약속

이 절을 한 번 더 정직하게 짚어두는 편이 낫다. *기존 자바 코드가 그대로 돈다*는 약속은 무엇을 뜻하는가. 무엇이 그대로이고 무엇이 새로워졌는가.

**그대로 돌아가는 것**

- `Thread.currentThread()`, `Thread.sleep()`, `Thread.interrupt()` 등 `Thread` 클래스의 거의 모든 API.
- `synchronized` 블록 — *진입과 종료*의 의미론은 같다. 단, Java 21~23에서는 unmount가 막힌다(15장에서 짚는다).
- `ThreadLocal` — *동작은* 같다. 다만 thread 수가 폭발하면 메모리 사용 양상이 달라진다(역시 15장).
- `ReentrantLock`, `Semaphore`, `CountDownLatch`, `BlockingQueue` 등 `java.util.concurrent`의 모든 도구. 모두 Loom-aware로 재작성됐다.
- `Socket`, `ServerSocket`, `HttpClient` 등 표준 I/O — JDK 내부에서 mount/unmount를 자동 처리한다.

**달라진 것**

- thread 생성 비용: 수 밀리초 → 수십 마이크로초.
- thread당 stack: OS 예약 1MB → heap 동적 grow.
- thread 수 한계: ~수천 → ~수백만.
- `setDaemon`, `setPriority`, thread group: 의미 없는 호출.
- `ThreadFactory` 기반의 *thread 재사용 풀*: virtual thread에는 의미 없다 — *재사용하지 않으니까*.

마지막 항목이 중요하다. `newFixedThreadPool(200)`을 `newVirtualThreadPerTaskExecutor()`로 *그대로* 바꾸면 안 된다. 두 도구는 *다른 모델*이다. 옛 코드가 풀의 크기에 *의존*하고 있었다면 — 가령 외부 API의 rate limit을 thread 수로 제한하고 있었다면 — virtual thread로 옮기는 순간 그 제한이 사라진다. rate limit은 *명시적*으로 `Semaphore`로 다시 두는 편이 낫다. 풀의 크기로 *암묵적*으로 다스리던 제약을 *드러내자*. 이 *드러냄*이 virtual thread 도입의 또 다른 부수 효과다.

### Java 8 ExecutorService vs Java 21 VirtualThreadPerTaskExecutor

코드 한 쌍으로 11년의 거리를 좁혀 보자. 같은 일을 Java 8 시대에는 어떻게 적었고, Java 21에서는 어떻게 적는가.

**Java 8 — bounded thread pool**

```java
private static final ExecutorService POOL =
    Executors.newFixedThreadPool(200,
        new ThreadFactoryBuilder().setNameFormat("checkout-%d").build());

public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    Future<Payment> pay  = POOL.submit(() -> billing.charge(orderId));
    Future<Member>  mem  = POOL.submit(() -> members.findById(userId));
    Future<Coupon>  cp   = POOL.submit(() -> coupons.validate(coupon));
    try {
        return new CheckoutResponse(pay.get(), mem.get(), cp.get());
    } catch (Exception e) {
        // pay·mem 결과 폐기, 보상 처리는 ... 어디서 ... ?
        throw new ServiceException(e);
    }
}
```

`POOL`은 *공유 자원*이다. 200개 thread가 컨트롤러 전체에서 돌고 있다. 어떤 요청이 외부 API의 응답을 30초간 기다리면, 그 30초 동안 thread 하나가 점유된다. 200개가 모두 그렇게 되면 다음 요청은 큐에 쌓인다. 800ms의 p99는 이 큐에서 태어난다. 그리고 한 자식이 실패했을 때 다른 자식을 깔끔하게 취소할 방법이 보이지 않는다. `pay.cancel(true)`를 호출해도 이미 보낸 결제 요청은 중단되지 않을 가능성이 크다. 보상 트랜잭션을 어디 적어야 할지조차 코드에서 안 보인다.

**Java 21 — virtual thread per task**

```java
public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<Payment> pay  = scope.submit(() -> billing.charge(orderId));
        Future<Member>  mem  = scope.submit(() -> members.findById(userId));
        Future<Coupon>  cp   = scope.submit(() -> coupons.validate(coupon));
        return new CheckoutResponse(pay.get(), mem.get(), cp.get());
    } // scope 종료 시 자식 task 정리
}
```

차이를 살피자. 첫째, `POOL`이 사라졌다. 매 요청마다 새 executor를 만든다. 둘째, 그 executor는 *thread를 빌려주지 않는다*. 자식 task마다 새 virtual thread를 만든다. 셋째, `try-with-resources`로 묶었기 때문에 컨트롤러가 반환되는 순간 executor도 닫히고 자식 task의 수명이 컨트롤러 scope에 묶인다.

이 코드는 *문법적으로* 거의 같다. Java 8 코드를 Java 21로 옮기면서 새로 배운 것은 `newVirtualThreadPerTaskExecutor()` 한 줄뿐이다. 그러나 *의미*는 달라졌다. thread는 자원이 아니고, 풀은 없으며, 외부 호출이 100ms든 30초든 다른 요청에 영향을 주지 않는다. 이게 thread-per-request가 *돌아왔다*는 말의 진짜 내용이다.

(취소·실패 전파의 정직한 답은 16장의 `StructuredTaskScope`에 있다. virtual thread는 그 자체로는 *수명 관리*까지 풀어주지 않는다. 그러나 일단 여기까지가 14장의 무게다.)

### Spring과의 만남은 21장에서

Spring Boot 3.2부터는 `application.yml`에 한 줄을 적으면 Tomcat의 request handler가 virtual thread per request로 바뀐다.

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

기억해 두자 — 이 한 줄의 의미는 21장에서 본격 다룬다. 한 결제 마이크로서비스에 records·sealed·virtual thread·AOT를 한 번에 끼워 넣는 자리에서, 이 한 줄이 어떤 도구들과 만나 *후련함*이 되는지 같이 본다. 지금은 *호명*만 해두자.

### reactive와의 대화: 무엇이 남고 무엇이 사라질까

§6.3의 두 관점을 한 번 정직하게 짚어두자. *virtual thread가 모든 reactive를 대체할까*. 한국 커뮤니티에서 가장 자주 마주치는 질문이다. 양면 모두 인정하는 편이 낫다.

**대체될 자리**

`Mono`·`Flux`로 짠 단순 fan-out 컨트롤러는 virtual thread로 *다시 평범한 동기 코드*가 된다. operator chain의 학습 비용, 디버깅의 *난감함*, stack trace에서 진짜 발생 지점을 찾지 못해 헤매던 시간 — 그 부담이 줄어든다. WebFlux를 도입한 이유의 *반*은 "thread 풀 한계를 우회하려고"였는데, 그 자리는 virtual thread가 더 단순한 답을 준다.

**남는 자리**

reactive가 *진짜로 제공*하던 것이 둘 있다. 첫째, *backpressure*. consumer가 늦으면 producer를 *멈춰 세우는* 신호 전달이다. Kafka 컨슈머·SSE·WebSocket 같은 streaming 자리에서는 backpressure가 본질이다. virtual thread가 backpressure를 *자동으로* 주지는 않는다. 둘째, *hot/cold stream과 명시적 cancel/replay*. Reactor의 `share()`·`replay()`·`retryWhen` 같은 operator는 virtual thread의 어휘에 없다. 진정한 *데이터 흐름*이 주제인 시스템 — 실시간 통계, event sourcing, 메시지 스트림 — 에서는 reactive가 여전히 더 자연스러운 도구다.

SoftwareMill의 *Limits of Loom's Performance*도 이 두 관점을 모두 인정했다. *대체*가 아니라 *역할의 재배치*다. 한국 사례를 한 줄 더 — 카카오페이가 platform → virtual로 옮긴 자리는 *fan-out 컨트롤러*였다. *결제 streaming*이나 *Kafka 컨슈머*는 다른 도구로 따로 짜고 있다. 우리도 그 방향으로 결정하는 편이 낫다.

### 진화의 자리: JEP 425 → 436 → 444

마지막으로 진화의 자리를 정리하자. virtual thread는 갑자기 생긴 도구가 아니다. Project Loom은 2017년에 시작됐고, OpenJDK에서 6년의 incubation을 거쳤다.

- **JEP 425 (Java 19, 2022 preview)** — virtual thread 첫 공개. API의 모양이 잡혔지만 아직 실험.
- **JEP 436 (Java 20, 2023 second preview)** — preview 라운드 2. 거의 변화 없음. 산업 피드백 수렴.
- **JEP 444 (Java 21, 2023 standard)** — LTS에 표준으로 안착. 이 자리가 우리가 본격적으로 쓸 수 있는 출발선이다.

이 흐름은 자바의 *preview 문화*를 잘 보여준다. records가 그랬듯, virtual thread도 두 라운드의 preview를 거쳐 다듬어졌다. 표준화된 21에서는 API가 바뀌지 않을 것이라는 *호환성 약속*이 따라붙는다. 11년의 자바를 견뎌낸 도구는 그렇게 만들어진다.

### 마무리

virtual thread는 자바에 *thread-per-request*를 돌려준 도구다. 30년간 OS thread에 묶여 thread pool로 버텨왔던 모델이, 마침내 *task마다 thread를 만든다*는 가장 자연스러운 표현으로 돌아왔다. continuation이라는 추상이 mount/unmount로 OS thread를 자유롭게 만들고, ForkJoinPool 기반의 carrier가 그 위에서 work-stealing을 한다. reactive 없이도 충분히 빠르다는 약속은 — *I/O bound*라는 단서 안에서 — 정직하게 지켜진다.

그러나 약속은 단서가 있어야 정직하다. virtual thread를 켜기만 하면 모든 게 빨라진다는 말은 사실이 아니다. `synchronized` 블록 안에서 외부 API를 호출하면 pinning이 일어나고, ThreadLocal에 caching을 들고 있던 코드는 수백만 thread 곱하기 수백만 캐시로 메모리를 *폭발*시킨다. CPU-bound 작업에 virtual thread를 쓰면 오히려 느려진다. 켰는데 *deadlock*이 난 새벽도 production에서는 드물지 않다.

다음 장에서는 그 *끔찍한 새벽*을 함께 들여다보자. VT를 켰는데 더 느려지는 자리, pinning을 JFR로 추적하는 절차, ThreadLocal의 폭발을 막는 안전한 패턴 — 이 장에서 약속한 것의 *반대편*에 정직하게 마주서 보자.

---

## 15장. Pinning · ThreadLocal · 함정들 — Virtual Thread가 우리를 실망시키는 자리

VT를 켰는데 오히려 deadlock이 났다고 해보자.

`spring.threads.virtual.enabled=true` 한 줄을 추가하고 운영에 올린 다음 날 새벽, 결제 컨트롤러가 멈췄다. p99가 떨어지기는커녕 *모든* 요청이 timeout으로 떨어졌다. JStack을 찍어 보면 thread 수십 개가 같은 `synchronized` 블록 앞에서 대기 중이다. 외부 결제 게이트웨이의 SDK가 내부적으로 `synchronized(connectionLock)`로 보호된 메서드 안에서 소켓 read를 하고 있는 것이다. 그 한 자리에서 carrier thread가 unmount되지 못하고 *못 박혔다*. 결제 쪽 carrier가 다 잠기자 다른 외부 호출도 줄을 잇지 못해 멈췄다. 정확히 14장에서 약속한 *비약*과 반대 방향이다.

켰는데 왜 더 느려졌을까. 왜 도구는 약속을 지키지 못했을까. 그렇다면 우리는 — 그 약속이 깨지는 자리를 미리 알고, JFR을 켜서 *조용히 막혀 가는 시그널*을 잡아내고, 라이브러리의 이주 상태를 확인할 수 있을까. 이 장에서 그 *끔찍한 새벽*을 정직하게 들여다보자. 결론을 먼저 짚자면 — virtual thread는 만능이 아니다. 그러나 함정을 알면 안전하다.

### Pinning이란 무엇인가

먼저 용어부터 정리하자. **pinning**은 virtual thread가 carrier thread에서 *unmount되지 못하는* 상황을 말한다. 14장에서 살펴봤듯, virtual thread의 마법은 blocking 호출을 만났을 때 자동으로 unmount되어 carrier를 자유롭게 풀어주는 데 있다. 그 unmount가 막히는 자리, 그 자리가 pinning이다.

pinning이 일어나면 virtual thread는 *그 carrier에 못 박힌 채로* blocking 호출을 마칠 때까지 자리를 차지한다. 그 동안 그 carrier에는 다른 virtual thread가 mount되지 못한다. carrier pool의 크기는 CPU 코어 수 — 보통 4~32개다. pinning이 그 절반에 일어나면 throughput은 절반이 된다. 두 자리 모두 일어나면 *14장에서 본 800ms*가 그대로 돌아온다. 더 나쁜 경우, carrier가 모두 잠긴 채로 외부 호출의 응답을 *서로 기다리면* deadlock이 된다. 새벽에 결제 컨트롤러가 멈춘 그 자리가 바로 그렇다.

이 함정의 뿌리를 정확히 들여다보려면 30년 묵은 JVM 모니터의 구현으로 들어가 봐야 한다.

### `synchronized`의 30년 묵은 짐

자바의 `synchronized` 블록은 1995년부터 지금까지 *intrinsic monitor*라는 JVM 내부 메커니즘으로 구현돼 왔다. monitor는 OS thread의 신원으로 lock을 추적한다. 같은 OS thread가 두 번 들어오면 reentrant로 허용하고, 다른 OS thread가 들어오려 하면 대기시킨다. 30년 동안 잘 동작했다. 자바 = OS thread라는 등식이 깨지기 전까지는.

virtual thread가 등장하자 문제가 생겼다. virtual thread는 OS thread를 *옮겨 다닌다*. carrier A에 mount됐다가 unmount된 뒤 다시 mount될 때 carrier B로 옮겨갈 수 있다. JVM 모니터가 OS thread 신원으로 lock을 추적하는데, 그 OS thread가 *바뀐다면* lock의 일관성이 깨진다. OpenJDK 팀의 선택은 보수적이었다. virtual thread가 `synchronized` 블록 안에 *진입*해 있을 때는 unmount를 *금지*한다. 그 시간 동안 그 virtual thread는 carrier에 *못 박힌 채로* 살아야 한다.

Java 21·22·23의 virtual thread가 산업에서 부딪힌 가장 큰 벽이 이것이다. 모든 라이브러리가 `synchronized`를 쓴다. JDBC 드라이버도, HTTP 클라이언트도, connection pool도. 그중 하나가 외부 I/O를 `synchronized` 블록 안에서 호출하면 그 자리가 pinning이 된다. 가장 흔한 예가 HikariCP의 5.0 미만 버전 — `synchronized(ConnectionState)` 안에서 JDBC 연결을 얻어내고 있었다. JDBC 연결을 얻는 일은 보통 빠르지만, pool이 비어 있으면 *기다린다*. 그 기다림이 virtual thread를 carrier에 *못 박는다*.

이 자리에서 라이브러리 생태계의 이주가 시작됐다. 2023~2024년에 걸쳐 주요 라이브러리들이 `synchronized` → `ReentrantLock`으로 *옮기는 PR*을 받았다. `ReentrantLock`은 monitor를 쓰지 않고 `java.util.concurrent`의 큐와 CAS로 구현돼 있어서 virtual thread를 carrier에 못 박지 않는다.

| 라이브러리 | 이주 상태 (2025 기준) | 메모 |
|---|---|---|
| HikariCP | 5.1.0+ (5.0은 부분) | `synchronized` 다수 제거. JDBC 드라이버의 pinning은 별개 |
| Caffeine | 3.1.0+ | 거의 모든 `synchronized`를 `ReentrantLock`으로 |
| Apache HttpClient | 5.3+ | 5.2는 connection lock에서 pinning 잔존 |
| MySQL Connector/J | 8.3+ | 8.2 이하는 statement 실행 자리에서 pinning |
| Postgres JDBC | 42.7+ | 거의 해소. driver 자체는 cleaner |
| Oracle JDBC | 23ai+ | 일부 잔존 보고. driver별 정밀 audit 필요 |

이주가 완벽하지는 않다. 직접 인용한 한국 기업의 사례에서도 *카카오페이*는 production 도입 과정에서 외부 SDK 일부가 `synchronized` 블록 안에서 소켓 I/O를 호출하는 자리를 발견했고, 그 자리들을 우회하거나 SDK를 교체해야 했다. *Cashfree Payments*도 비슷하다. *7 Key Lessons* 글의 핵심 중 하나는 "도입 전에 connection pool과 외부 SDK의 Loom-readiness를 audit해라"였다. 한 자리만 안 풀려도 carrier가 못 박힌다.

(Netflix의 production deadlock 사례는 한 차례 화제가 됐다. 공식 post-mortem은 핵심 정보가 정리된 형태로 공개되지 않았으나, *TheServerSide*의 정리에 따르면 큰 그림은 — `synchronized` 안의 외부 호출이 carrier를 다 잠그며 컨트롤러 전체가 멈춘 — 우리가 새벽에 만난 그 시나리오다. *사실 확인 필요*. 정확한 사정이 궁금하다면 Netflix Tech Blog의 후속 글을 추적하길 권한다.)

### JEP 491: Java 24가 가져온 해방

다행히도 이 함정은 *현재진행형 해소* 중이다. Java 24의 **JEP 491**은 JVM 모니터의 30년 묵은 구현을 바꿨다. 핵심 변화 한 줄이다 — *monitor가 OS thread 신원이 아니라 virtual thread 신원을 추적한다*. 그 결과 `synchronized` 블록 안에서도 virtual thread를 unmount할 수 있게 됐다.

JEP 491의 의미를 정직하게 짚자.

- Java 24 이후로, `synchronized` 안의 blocking I/O는 더 이상 pinning이 아니다.
- 라이브러리의 `synchronized` → `ReentrantLock` 이주는 *여전히 권장*되지만, 그 자리에서 운영을 막는 *blocker*는 아니게 됐다.
- Java 21 LTS에 머무는 한, 이 해방은 받지 못한다. 21 LTS 위에서 운영한다면 라이브러리 audit이 *여전히 필수*다.

여기서 결정의 자리가 생긴다. *21 LTS에 머물 것인가, 24·25로 갈 것인가*. 운영 안정성, 보안 패치 주기, 라이브러리 호환성 — 모든 결정 요소를 한 번에 저울에 올려야 한다. 일반적인 권장은 이렇다 — 신규 프로젝트라면 25 LTS를 노리고, 기존 시스템은 21에 머물되 라이브러리 audit과 pinning 모니터링을 *반드시* 설치해두자.

pinning이 *원천적으로* 사라지는 자리가 있느냐 하면, 그렇지는 않다. JEP 491 이후에도 두 자리는 여전히 pinning이다.

- **JNI/native call** 안의 코드. native 영역에서는 JVM이 unmount를 시킬 수 없다.
- **class initializer** 실행 중. JVM은 class 초기화의 원자성을 지키기 위해 그 동안 unmount를 금지한다.

이 둘은 *기억해두자*. 두 자리에서 외부 I/O를 호출하는 코드는 — 24·25에서도 — pinning을 만든다.

### ThreadLocal 함정: 수백만 thread × 캐시

pinning만 함정이 아니다. 더 *조용히* 메모리를 망치는 함정이 있다. **ThreadLocal**이다.

자바 코드에 ThreadLocal이 얼마나 깊이 박혀 있는지 한 번 짚어보자. `SimpleDateFormat`은 thread-safe하지 않아서 보통 ThreadLocal로 캐싱한다. Hibernate는 `Session`을 ThreadLocal에 묶는다. Spring의 `RequestContextHolder`는 `LocaleContextHolder`와 `SecurityContextHolder`까지 ThreadLocal 기반이다. SLF4J의 MDC도 ThreadLocal이다. JDBC 트랜잭션 동기화는 ThreadLocal로 connection을 묶는다.

이 패턴이 *thread pool*과 잘 맞물려 있었다. 200개 thread 풀이 있다면 ThreadLocal 캐시도 200개다. SimpleDateFormat 200개 — 큰 메모리는 아니다. Hibernate Session 200개 — 운영 가능한 크기다. ThreadLocal은 *thread의 lifetime*에 묶여 살고, thread는 *재사용*되므로 캐시도 재사용된다. 자바의 *thread 자원이 비싸다*는 전제 위에 ThreadLocal이라는 도구가 자연스럽게 자리 잡았다.

이제 virtual thread를 켜자. thread는 더 이상 *재사용*되지 않는다. *task마다 새로 만든다*. 동시에 100만 개의 virtual thread가 살 수 있다.

곱셈이 무서워진다. SimpleDateFormat × 100만 = 100만 개. 1KB짜리 객체라도 1GB다. Hibernate Session × 100만 — 가능한 시나리오가 아니지만, 이론적으로는 폭발이다. MDC가 user context를 들고 있다면 그것도 100만 벌. 우리 머릿속의 *thread pool 곱하기 캐시*라는 산수가 *task 수 곱하기 캐시*로 바뀌었다. 자원 계산의 단위가 통째로 달라진 것이다.

이 함정은 *조용하다*. pinning은 새벽에 한 번 일어나면 컨트롤러가 멈춰서 페이지를 친다. ThreadLocal 폭발은 그렇게 극적이지 않다. heap이 천천히 차오르고, GC가 점점 자주 일어나고, p99가 *서서히* 솟구친다. JFR을 켜서 heap profile을 보지 않으면 발견하기 어렵다. *찜찜한* 메모리 사용량 증가가 일어나면 가장 먼저 ThreadLocal을 의심하는 편이 낫다.

JDK가 준 길은 두 갈래다.

- **ThreadLocal을 줄여라**. 정말 필요한 자리만 남기고, 캐싱 대신 매번 새로 만들거나(예: `DateTimeFormatter.ISO_LOCAL_DATE`는 immutable이라 ThreadLocal이 필요 없다) thread-safe한 대안으로 옮긴다.
- **ScopedValue로 옮겨라**. JEP 506의 `ScopedValue`가 ThreadLocal의 후계자다. immutable이고, 부모→자식 binding이며, scope이 끝나면 *자동 cleanup*된다. 100만 virtual thread가 각자 `ScopedValue`로 user context를 들고 있어도 메모리는 폭발하지 않는다. 자세한 내용은 16장에서 다룬다.

`InheritableThreadLocal`도 함정에 들어가 있다는 점은 짚어 둘 만하다. 부모에서 자식으로 *복사*되는 패턴은 ThreadLocal보다 *더 위험*하다. virtual thread는 부모-자식 관계가 흔하기 때문에 한 컨트롤러가 fan-out한 자식 모두에 ThreadLocal이 복사된다. 16장의 ScopedValue가 정확히 이 자리를 노리고 만들어졌다.

### 모니터링: JFR과 `tracePinnedThreads`로 잡아내자

이제 *진단 절차*를 한 페이지로 정리하자. virtual thread를 도입한 시스템이라면 — 도입 첫날에 — 이 둘 중 하나는 반드시 설치해두는 편이 낫다.

**1. 가장 가벼운 길: `-Djdk.tracePinnedThreads=full`**

JVM 옵션 한 줄이다. virtual thread가 pinning되면 stack trace가 stderr로 찍힌다. 개발/스테이징 환경에서 *어디서 pinning이 나는지*를 빠르게 파악하기 좋다. 단, production에는 권장되지 않는다 — 모든 pinning 이벤트가 로그를 찍으면 부하가 크다.

```
-Djdk.tracePinnedThreads=full
```

`short` 옵션도 있다. trace의 일부만 찍어서 부하가 가볍다. 일단 *어디서 일어나는지*만 알면 되니 `short`로 시작하는 편이 낫다.

**2. production용 길: JFR `jdk.VirtualThreadPinned` 이벤트**

Java Flight Recorder의 `jdk.VirtualThreadPinned` 이벤트가 정확히 이 자리를 위해 추가됐다. JFR을 켜 두면 pinning이 일어난 자리, 시간, stack trace가 이벤트로 기록된다. 부하가 거의 없어서 production에 *상시*로 켜 둘 만하다.

```bash
jcmd <pid> JFR.start name=pinning duration=5m filename=pinning.jfr \
    settings=profile
```

또는 JVM 시작 시:

```
-XX:StartFlightRecording=name=pinning,settings=profile,filename=pinning.jfr
```

기본 profile은 무거우니 `-XX:StartFlightRecording=name=pinning,duration=5m,settings=profile,jdk.VirtualThreadPinned#enabled=true` 같이 *원하는 이벤트만* 켜는 편이 효율적이다. 생성된 `.jfr` 파일은 JDK Mission Control (JMC) 또는 IntelliJ의 JFR 분석기로 연다.

**3. ThreadLocal 폭발 진단**

heap dump (`jcmd <pid> GC.heap_dump`)를 떠서 `ThreadLocal$ThreadLocalMap` 인스턴스 수를 확인한다. virtual thread를 켠 시스템에서 그 수가 *수만~수십만*에 이르면 폭발 직전이다. 어떤 ThreadLocal이 가장 많은 메모리를 잡고 있는지는 dominator tree로 추적할 수 있다.

**진단 절차 한 페이지**

새벽에 깨서 *VT가 의심된다*면 순서는 이렇다.

1. JFR을 켜서 5분 기록한다 — `jdk.VirtualThreadPinned` 이벤트가 있는지 본다.
2. 이벤트가 있다면 stack trace를 본다 — 어느 라이브러리의 어느 메서드인가.
3. 그 라이브러리의 *Loom-ready* 버전을 확인한다. 위 표가 첫 출발이다.
4. 라이브러리 업그레이드가 어렵다면 — 그 자리만 platform thread로 격리한다. `Executors.newFixedThreadPool()`을 따로 두고, 문제의 호출만 그 풀에 위임한다.
5. 이벤트가 없는데 메모리가 새는 것 같으면 ThreadLocal을 의심한다 — heap dump를 본다.

### CPU-bound 작업에는 쓰지 말 것

virtual thread의 약속은 *I/O bound* 워크로드에 한정된다. CPU-bound 작업 — 행렬 곱셈, 이미지 인코딩, 암호 계산, JSON 파싱이 분 단위인 거대 페이로드 — 에는 virtual thread가 *효과 없다*. 오히려 *느려질* 수 있다. 이유는 단순하다.

CPU-bound 작업은 *unmount되지 않는다*. blocking I/O 호출이 없기 때문이다. virtual thread가 carrier에 mount되어 CPU를 잡고 계산을 한다. carrier 수가 CPU 코어 수와 같으니, 결국 *코어 수만큼*의 동시성으로 돌아간다. 100만 개를 만들어도 한 번에 *코어 수만큼*만 진행된다. 평범한 `ForkJoinPool` 또는 `newFixedThreadPool(코어 수)`과 결과가 같다 — 다른 점은 virtual thread를 만들고 스케줄링하는 *오버헤드*가 더해진다는 것이다.

원칙은 이렇다.

- **I/O bound** (외부 API·DB·디스크) → virtual thread 적합.
- **CPU bound** (계산·인코딩) → `ForkJoinPool` 또는 GPU.
- **혼합** → I/O 부분은 virtual thread, 계산 부분은 별도 풀로 *위임*한다.

세 번째 패턴은 자주 만난다. 결제 컨트롤러가 외부 API 세 개를 합치고(I/O), 응답을 받은 뒤 암호 서명을 검증한다(CPU). 둘을 같은 virtual thread에서 다 처리해도 동작은 한다 — 다만 *서명 검증*이 카운트당 50ms씩 걸리면 그 50ms 동안 carrier가 잠긴다. 100만 동시 요청이 그 자리를 동시에 통과하면 carrier 풀이 그 자리에서 사상자가 난다. 별도의 CPU pool로 위임하는 편이 낫다.

```java
// CPU 작업 분리
private static final ExecutorService cpu = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors());

public CheckoutResponse checkout(...) {
    try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<Payment> pay  = scope.submit(() -> billing.charge(orderId));
        // ...
        Payment p = pay.get();
        // 서명 검증은 별도 CPU 풀로
        boolean valid = cpu.submit(() -> verifySignature(p)).get();
        return new CheckoutResponse(p, valid);
    }
}
```

이 *나누는 감각*은 virtual thread를 production에서 안전하게 쓰는 첫걸음이다.

### 적합도 매트릭스

한 페이지에 정리하자. 어떤 워크로드에 virtual thread를 켤지, *우선* 표로 본다.

| 워크로드 | 적합도 | 메모 |
|---|---|---|
| Spring MVC REST API (외부 API·DB 호출 많음) | ★★★ | 14장의 그 자리. p99 즉시 개선 |
| Webhook receiver / fanout (수만 동시) | ★★★ | thread-per-request의 정수 |
| Long-polling / SSE | ★★★ | 수만 connection 유지에 적합 |
| 메시지 컨슈머 (Kafka, RabbitMQ) | ★★ | I/O bound면 적합. 컨슈머 그룹 관리 별도 |
| Reactive (WebFlux) 시스템 | — | 이미 non-blocking. 도입 의미 없음 |
| CPU-bound 배치 | ★ | 효과 없음. ForkJoinPool 사용 |
| 동기 트랜잭션 chain (다수 DB 호출) | ★★★ | thread 풀 한계 즉시 해소 |
| `synchronized` 많은 옛 라이브러리 사용 | ★ (Java 21) / ★★★ (Java 24+) | 라이브러리 audit 필수 |
| 작은 함수 다수 (GraalVM serverless) | — | startup·footprint가 우선. AOT 19장 |

★★★는 *지금 켜라*. ★★는 *audit 후 켜라*. ★는 *효과 미미하거나 위험*. —는 *부적합*.

### 한국 사례: 카카오페이의 정직한 측정

이쯤에서 한국 사례를 하나만 더 들여다보자. *카카오페이*는 *"Virtual Thread에 봄(Spring)은 왔는가"* 글에서 platform thread → virtual thread 전환을 실측한 결과를 공유했다. 핵심을 정리하면 이렇다.

- *외부 API 호출이 다수인 결제 컨트롤러*에서, virtual thread 도입 후 동일 부하에서 p99 latency가 의미 있게 떨어졌다.
- container 메모리 사용량은 *증가*했다. 14장에서 짚은 그 자리다 — stack이 heap에 살기 때문이다.
- 도입 과정에서 외부 SDK 일부의 `synchronized` 자리에서 pinning이 발견됐고, *해당 SDK 우회* 또는 *교체*가 필요했다.
- ThreadLocal 기반 컨텍스트 전달 코드는 *audit*이 필요했다.

이 정직한 정리가 한국 production에서 가장 신뢰할 만한 자료다. 글 자체에 정확한 수치와 그래프가 있으니, virtual thread 도입을 고민 중이라면 한 번 읽어 보는 편이 낫다.

### 마무리

virtual thread는 만능이 아니다. *켜기만 하면 모든 게 빨라진다*는 약속은 단서 없이는 거짓이다. `synchronized` 안의 외부 I/O는 carrier에 못 박히고, ThreadLocal에 무심코 들어 있는 캐시는 100만 곱하기로 폭발하며, CPU-bound 작업은 오히려 carrier를 잠근다. JEP 491이 Java 24에서 `synchronized` pinning을 해소했지만, 21 LTS에 머무는 한 라이브러리 audit은 여전히 필수다.

그러나 함정을 알면 안전하다. JFR의 `jdk.VirtualThreadPinned` 이벤트로 *조용한 시그널*을 잡고, 라이브러리의 Loom-readiness를 도입 전에 확인하고, ThreadLocal을 ScopedValue로 옮기고, CPU 작업을 별도 풀로 분리한다. 이 네 가지 습관이 virtual thread를 *약속의 자리*로 데려간다.

ThreadLocal을 ScopedValue로 옮긴다는 말이 자꾸 떠올랐을 것이다. 그 자리, 그리고 fan-out한 자식 task 전체를 *하나의 단위*로 묶어 *cancellation까지 전파*하는 자리. 다음 장에서는 그 도구 — `StructuredTaskScope`과 `ScopedValue` — 를 본격적으로 살펴보자. concurrent 코드에도 *구조*가 있다는 Dijkstra의 1968년 약속을 자바가 마침내 받아낸 자리다.

---

## 16장. Structured Concurrency와 Scoped Values — concurrent 코드의 문법

request-scoped 데이터를 자식 task에 넘기다 ThreadLocal 청소를 잊었다고 해보자.

컨트롤러가 fan-out한 자식 task 셋이 있다. 결제 호출, 회원 조회, 쿠폰 검증 — 14장에서 우리가 따라온 그 fan-out이다. 각 자식이 `userId`와 `tenantId`를 알아야 한다. 누구는 audit log를 남기고, 누구는 multi-tenant DB의 schema를 분기하기 때문이다. 이 컨텍스트를 어디에 둘까. `SecurityContextHolder`나 `RequestContextHolder` 같은 Spring의 자리는 *ThreadLocal*이다. 컨트롤러 thread에는 값이 들어 있지만 자식 thread는 새 thread다. 비어 있다. 그래서 `InheritableThreadLocal`로 복사하거나, 명시적으로 `try { set(...); ... } finally { remove(); }`로 다시 깔아준다.

여기서 일이 생긴다. 자식 task 중 하나가 예외를 던졌다. `try-finally`의 `finally` 블록이 자식 thread에서 잘 실행될까. 자식이 thread pool에서 *재사용*되는 thread라면, 청소를 잊은 ThreadLocal은 다음 요청의 자식에게 *유령처럼* 따라간다. 다른 사용자의 `userId`가 우리 자식 task에 흘러 들어가 DB의 *다른 tenant*에 audit log가 남는다. *찜찜한* 정도가 아니라 *끔찍한 일*이다.

게다가 자식 셋 중 결제 호출이 30초 timeout으로 늦어지는 동안 회원 조회와 쿠폰 검증은 *이미 끝나서 자원을 기다리고 있다*. 결제가 실패로 끝나도 나머지 두 자식의 자원은 누가 정리하는가. 컨트롤러는 그 셋의 수명을 *함께* 다스리고 싶은데, 코드 어디에도 *함께*라는 말이 보이지 않는다. concurrent 코드가 *흩어진* 채로 살아있다. 동기 코드라면 함수 호출의 stack이 곧 *함께*라는 약속을 받아냈다. 그렇다면 — concurrent 코드에도 그런 *구조*가 있을 수 있을까.

### Dijkstra의 1968년이 자바에 도착했다

Edsger Dijkstra가 1968년 *Notes on Structured Programming*을 쓰며 한 주장은 단순했다. *goto*를 버리고 함수 호출과 블록 구조로 프로그램을 짜자. 한 함수에 들어간 흐름은 *반드시* 그 함수에서 나온다. 시작과 끝이 *짝*을 이룬다. 그 짝 덕분에 우리는 프로그램을 *어휘적*으로 읽을 수 있다. 코드를 위에서 아래로 따라가면 흐름이 어디서 시작해 어디서 끝나는지 보인다.

자바의 동기 코드는 50년 동안 이 약속 위에 살아왔다. 한 메서드가 호출되면 그 메서드가 *반드시* 반환되고, 메서드 안의 모든 자원이 *호출자에게 돌아가기 전*에 정리된다. `try-with-resources`는 이 약속을 자원에까지 확장했다. 블록을 떠나는 순간 자원도 *함께 떠난다*. 시작과 끝이 짝을 이룬다는 단순한 규칙이 코드의 추리 가능성을 받쳐 왔다.

그런데 concurrent 코드는 이 약속을 *깨면서* 발전했다. `ExecutorService.submit()`로 자식 task를 던지면, 그 자식의 수명은 호출자의 수명과 *분리*된다. 호출자가 반환된 뒤에도 자식은 살아 있을 수 있다. 자식이 실패해도 호출자는 모를 수 있다. 호출자가 일찍 끝나도 자식은 *유령처럼* 자원을 잡고 있다. 30년 묵은 goto의 자리를 자바의 concurrent 코드가 *그대로* 물려받은 셈이다.

Project Loom의 두 번째 큰 도구가 정확히 이 자리를 노렸다. *Structured Concurrency*다. JEP 453의 한 줄로 약속이 분명해진다 — *부모 함수가 반환되기 전 자식이 모두 끝난다*. 호출자의 scope가 자식의 scope를 *감싼다*. 시작과 끝이 짝을 이룬다. concurrent 코드에도 *구조*가 돌아왔다.

### `StructuredTaskScope`: 자식을 하나의 단위로

핵심 API는 `StructuredTaskScope`다. 14장에서 만났던 `Executors.newVirtualThreadPerTaskExecutor()`와 모양이 비슷하다 — `try-with-resources` 블록에서 자식 task를 fork하고, 마지막에 join한다.

```java
try (var scope = StructuredTaskScope.open()) {
    StructuredTaskScope.Subtask<Payment> pay  = scope.fork(() -> billing.charge(orderId));
    StructuredTaskScope.Subtask<Member>  mem  = scope.fork(() -> members.findById(userId));
    StructuredTaskScope.Subtask<Coupon>  cp   = scope.fork(() -> coupons.validate(coupon));

    scope.join();  // 자식 셋 모두 끝날 때까지 대기

    return new CheckoutResponse(pay.get(), mem.get(), cp.get());
}
```

차이를 정리하자. `submit()`이 `Future`를 돌려주는 반면 `fork()`는 `Subtask`를 돌려준다. 그리고 `join()`이 *반드시* 호출돼야 한다. 호출자가 `join()` 없이 블록을 벗어나려고 하면 — scope의 `close()`가 자식들을 강제로 cancel한다. *자식이 살아 있는 채로 부모가 떠날 수 없다*. 이게 structured concurrency의 핵심 규칙이다.

Java 25에서 표준화된 시점의 API 모양을 짚어두자. 진화 과정에서 메서드 이름이 몇 차례 바뀌었다. 옛 글들에서 `scope.fork(...)` 다음에 `scope.joinUntil(deadline)`이나 `scope.joinAll()` 같은 변종을 볼 수 있는데, 25 finalize 기준은 `join()` 한 줄로 통일됐다. 책에서는 25 기준으로만 적는다.

### 정책 세 가지: ShutdownOnFailure · ShutdownOnSuccess · Joiner

자식 셋이 동시에 진행되다가 *하나가 실패*하면 어떻게 할까. 자식 셋 중 *가장 빠른 하나의 성공*만 필요한 fan-out도 있다. 또 *모두의 결과를 무조건 모아*야 하는 경우도 있다. 세 갈래의 정책을 코드로 보자.

**1. `ShutdownOnFailure`: 하나가 실패하면 모두 취소**

결제 컨트롤러의 가장 흔한 패턴이다. 세 자식 중 하나라도 실패하면 나머지를 *즉시 취소*하고 호출자에게 예외를 던진다. 자원 낭비도 막고, 일관성 없는 부분 성공도 막는다.

```java
try (var scope = StructuredTaskScope.open(
        Joiner.<Object>anySuccessfulResultOrThrow())) {
    // ... 가장 빠른 성공 한 자식의 결과만 필요할 때
}

// 또는 ShutdownOnFailure (사실 확인 필요: Java 25에서 Joiner.allSuccessfulOrThrow()로 통합됐을 가능성)
try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
    var pay  = scope.fork(() -> billing.charge(orderId));
    var mem  = scope.fork(() -> members.findById(userId));
    var cp   = scope.fork(() -> coupons.validate(coupon));
    scope.join();
    return new CheckoutResponse(pay.get(), mem.get(), cp.get());
}
```

(Java 21~24의 preview API에는 `StructuredTaskScope.ShutdownOnFailure`와 `ShutdownOnSuccess`라는 *서브 클래스*가 있었고, Java 25의 standard 시점에 `Joiner` 인터페이스 기반으로 통합된 형태로 다듬어졌다. 책에 적힌 정확한 메서드 이름은 25 GA 시점의 문서를 *반드시 확인*하길 권한다. 이주의 방향성은 분명하다 — *서브 클래스 상속*에서 *Joiner 조합*으로.)

**2. `ShutdownOnSuccess`: 가장 빠른 성공 하나만**

여러 백엔드에서 같은 답을 받아오는 *replicated read* 같은 패턴이다. 캐시 두 대와 DB 하나에 동시에 조회를 보내고 *가장 빠른 응답*만 받는다. 한 자식이 성공하면 나머지를 *즉시 취소*하고 호출자에게 그 결과를 돌려준다.

```java
try (var scope = StructuredTaskScope.open(Joiner.<String>anySuccessfulResultOrThrow())) {
    scope.fork(() -> readFromCacheA(key));
    scope.fork(() -> readFromCacheB(key));
    scope.fork(() -> readFromPrimary(key));
    scope.join();
    return scope.result();  // 가장 먼저 성공한 결과
}
```

이 패턴은 cache stampede 방지·hedged read·라우팅 최적화 같은 자리에서 유용하다. 단, 가장 빠른 *성공*이 정답이라는 단서가 있어야 한다 — 캐시가 stale일 가능성이 있다면 정책이 달라져야 한다.

**3. 커스텀 `Joiner`: 정책을 직접 짜자**

위 둘로 부족하면 `Joiner` 인터페이스를 직접 구현할 수 있다. 가령 *최소 2개 성공*이 정족수인 quorum read를 짜고 싶다고 해보자. 또는 *모든 자식의 결과를 모으되, 실패한 자식은 기본값으로 채우는* 관대한 정책이 필요할 수 있다.

```java
// 의사 코드 — 25 GA 시점의 정확한 시그니처는 문서 확인 권장
class QuorumJoiner<T> implements Joiner<T, List<T>> {
    private final int quorum;
    private final List<T> results = new CopyOnWriteArrayList<>();
    
    @Override public boolean onComplete(Subtask<? extends T> subtask) {
        if (subtask.state() == Subtask.State.SUCCESS) {
            results.add(subtask.get());
            return results.size() >= quorum;  // true면 scope shutdown
        }
        return false;
    }
    
    @Override public List<T> result() { return results; }
}
```

핵심 규칙은 두 가지다. `onComplete`에서 `true`를 돌려주면 scope이 *지금 shutdown*된다 — 나머지 자식이 모두 cancel된다. 그리고 `result()`가 `scope.result()` 호출에 돌려줄 값이다. 이 두 자리만 잡으면 어떤 정책도 짤 수 있다.

세 정책의 공통점은 *cancellation propagation*이다. shutdown이 호출되는 순간 살아있는 자식 모두에 `interrupt`가 전파된다. virtual thread 안에서 blocking 호출이 `InterruptedException`을 정직하게 받는다면, 자식은 곧 정리된다. 자식이 외부 API 호출 중이라면, JDBC 드라이버의 cancel 동작이나 HTTP 클라이언트의 interrupt 처리가 *Loom-aware* 한지가 그 자리에서 시험된다.

### Cancellation propagation: 부모가 반환되기 전 자식이 모두 끝난다

이 한 줄을 다시 한 번 정직하게 짚자. *부모 함수가 반환되기 전 자식이 모두 끝난다*. structured concurrency가 약속하는 단 하나의 규칙이다. 이 규칙으로부터 따라 나오는 모든 결과가 우리가 본격적으로 받는 *후련함*이다.

- 호출자가 timeout으로 일찍 끝나면 자식이 *모두* 취소된다. 살아남는 유령이 없다.
- 자식 하나가 실패하면 나머지가 *즉시* 취소된다. 자원 낭비가 없다.
- 호출자의 stack에 자식의 모든 stack이 *함께* 표시된다. JFR이나 thread dump가 컨트롤러 - 자식 - 자식의 자식을 *나무*로 보여준다.

마지막 항목이 특히 중요하다. 옛 `ExecutorService`로 짜인 fan-out 코드는 thread dump에서 *조각난* 채로 보였다. 자식 thread가 누구의 자식인지 정보가 없었다. structured concurrency는 *부모-자식 관계*를 thread 메타데이터에 박아 넣는다. JFR을 켜 두면 "이 자식 task가 이 컨트롤러의 자식이고, 그 컨트롤러는 이 사용자 요청의 자식이다"라는 *나무*가 보인다. production 디버깅이 *비교할 수 없을 만큼* 좋아진다.

### Scoped Values: ThreadLocal의 후계자

이제 도입부의 *끔찍한 일*로 돌아가자. `userId`와 `tenantId`를 자식 task에 넘기는 자리 — ThreadLocal로 풀어왔던 그 자리다. JEP 506이 Java 25에서 표준화된 **`ScopedValue`**가 이 자리의 정답이다.

ScopedValue가 ThreadLocal과 결정적으로 다른 점 셋을 짚자.

- **Immutable.** 한 번 binding되면 그 scope 안에서 *바꿀 수 없다*. `set()`이 없다. 이 *immutability* 덕에 race condition도, 청소 잊음도 원천적으로 사라진다.
- **부모→자식 자동 binding.** 부모 scope에서 binding된 값이 *자식 task로 자동 전파*된다. `InheritableThreadLocal`처럼 *복사*되는 게 아니다. 같은 immutable 값을 자식이 *읽는다*. 메모리 폭발이 일어나지 않는다.
- **자동 cleanup.** scope이 끝나면 binding이 *자동 해제*된다. `finally` 블록에 `remove()`를 적을 필요가 없다.

기본 사용법은 이렇다.

```java
public class AuthContext {
    public static final ScopedValue<UserPrincipal> PRINCIPAL = ScopedValue.newInstance();
    public static final ScopedValue<TenantId> TENANT = ScopedValue.newInstance();
}

// 컨트롤러 진입점에서 binding
public CheckoutResponse handle(HttpRequest req) {
    UserPrincipal user = authenticate(req);
    TenantId tenant = resolveTenant(req);

    return ScopedValue
        .where(AuthContext.PRINCIPAL, user)
        .where(AuthContext.TENANT, tenant)
        .call(() -> doCheckout(req));
}

// 자식 task에서 자동으로 읽힌다
private CheckoutResponse doCheckout(HttpRequest req) {
    try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
        var pay  = scope.fork(() -> billing.charge(...));
        var mem  = scope.fork(() -> members.findById(...));
        // ...
        scope.join();
        return new CheckoutResponse(pay.get(), mem.get());
    }
}

// billing 안 깊은 자리에서도 그냥 읽는다
public Payment charge(long orderId) {
    UserPrincipal user = AuthContext.PRINCIPAL.get();
    TenantId tenant = AuthContext.TENANT.get();
    // audit log에 user, tenant 박아 넣기
    ...
}
```

`where().call()` 또는 `where().run()`의 *동적 scope*가 핵심이다. `where(KEY, value)`로 binding을 *선언*하고, `call()`에 넘긴 람다가 실행되는 동안 그 binding이 살아있다. 람다가 반환되면 binding은 *자동으로* 해제된다. 람다 안에서 어떤 깊이의 자식 task를 만들어도, 그 자식들은 *같은 binding*을 본다. ScopedValue가 thread를 따라가는 게 아니라 *scope을 따라간다*는 점이 ThreadLocal과 가장 다른 자리다.

### Rebinding semantics: 동적 scope의 묘미

ScopedValue의 *동적 scope*가 가져오는 묘미가 하나 있다. **rebinding**이다.

이미 binding된 값을 *그 자리에서* 다른 값으로 갈아 끼울 수 있다. 단, 갈아 끼우는 *내부 scope*에서만 새 값이 보이고, *바깥 scope*에 영향을 주지 않는다.

```java
ScopedValue.where(AuthContext.PRINCIPAL, alice).call(() -> {
    var outerUser = AuthContext.PRINCIPAL.get();  // alice

    // 잠깐 시스템 권한으로 작업
    return ScopedValue.where(AuthContext.PRINCIPAL, systemUser).call(() -> {
        var innerUser = AuthContext.PRINCIPAL.get();  // systemUser
        return doPrivilegedTask();
    });
    // 여기로 돌아오면 PRINCIPAL은 다시 alice
});
```

이 *겹쳐 쓰기*가 안전한 이유는 binding이 *동적 scope*에 묶이기 때문이다. 정적 scope이라면 변수 가림(shadowing)을 적용해 컴파일러가 처리할 일이지만, ScopedValue는 *실행 시점*의 호출 chain이 scope를 결정한다. 람다가 끝나면 그 binding도 *함께 사라진다*.

ThreadLocal에서 이걸 시도하면 어떻게 될까. `try { set(systemUser); ... } finally { set(alice); }` 같은 식으로 *직접* 청소를 해야 했다. `finally`에서 예외가 나면 — 또는 비동기로 다른 thread로 넘어가면 — 청소가 깨질 가능성이 있었다. ScopedValue는 *언어 차원*에서 이 짝을 보장한다. 코드를 잘못 쓸 수 없다.

### ScopedValue vs ThreadLocal: 한 표로

| | ThreadLocal | ScopedValue |
|---|---|---|
| Mutability | mutable (set/remove) | immutable |
| 부모→자식 전파 | `InheritableThreadLocal`로 *복사* | 자동, *공유 참조* |
| 청소 책임 | 호출자 (`try-finally`) | 자동 (scope 종료 시) |
| 메모리 모델 | thread당 ThreadLocalMap | scope chain의 immutable bindings |
| Virtual thread 100만 개와 함께 | 폭발 위험 | 안전 |
| Rebinding | `set` 후 `set` (불안전) | `where().call()` 중첩 (안전) |
| Spring 통합 | `RequestContextHolder`·`SecurityContextHolder` | 25 이후 검토 중 |
| 도입 시점 | Java 1.2 (1998) | Java 25 (2025, JEP 506) |

마지막 행을 음미하자. ThreadLocal은 27년 동안 자바의 *컨텍스트 전달*을 책임져 왔다. 그 자리를 ScopedValue가 이어받는다. 다만 ThreadLocal이 사라지지는 않는다 — *Spring의 `RequestContextHolder`·`SecurityContextHolder`* 같은 위 layer가 ScopedValue로 이주하는 데 시간이 걸리기 때문이다. 그 이주가 끝날 때까지는 두 도구가 *공존*한다.

### Java 8 ExecutorService vs Java 25 StructuredTaskScope

14장과 같은 *세 외부 API* 예제를 두 시대로 비교하며 마무리하자.

**Java 8 — 흩어진 자식**

```java
private static final ExecutorService POOL = Executors.newFixedThreadPool(200);

public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    Future<Payment> pay  = POOL.submit(() -> billing.charge(orderId));
    Future<Member>  mem  = POOL.submit(() -> members.findById(userId));
    Future<Coupon>  cp   = POOL.submit(() -> coupons.validate(coupon));
    try {
        Payment p = pay.get(5, TimeUnit.SECONDS);
        Member  m = mem.get(5, TimeUnit.SECONDS);
        Coupon  c = cp.get(5, TimeUnit.SECONDS);
        return new CheckoutResponse(p, m, c);
    } catch (TimeoutException | ExecutionException | InterruptedException e) {
        pay.cancel(true); mem.cancel(true); cp.cancel(true);  // 정말 취소될까?
        throw new ServiceException(e);
    }
}
```

자식 셋은 *공유 POOL*에서 돈다. 호출자와 자식의 *부모-자식 관계*가 코드에 없다. `cancel(true)`는 *interrupt를 보낼 뿐* 자식이 *반드시* 취소된다는 보장이 없다. timeout 5초를 자식 셋 각각에 매기다 보니, 셋이 *전체적으로* 얼마나 걸렸는지 보장하기도 어렵다.

**Java 25 — 한 단위로 묶인 자식**

```java
public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    return ScopedValue
        .where(AuthContext.PRINCIPAL, SecurityContextHolder.getUser())
        .where(AuthContext.TENANT, TenantContext.current())
        .call(() -> doCheckout(orderId, userId, coupon));
}

private CheckoutResponse doCheckout(long orderId, long userId, String coupon)
        throws InterruptedException {
    try (var scope = StructuredTaskScope.open(
            Joiner.<Object>allSuccessfulOrThrow(),
            cfg -> cfg.withTimeout(Duration.ofSeconds(5)))) {
        var pay  = scope.fork(() -> billing.charge(orderId));
        var mem  = scope.fork(() -> members.findById(userId));
        var cp   = scope.fork(() -> coupons.validate(coupon));
        scope.join();
        return new CheckoutResponse(pay.get(), mem.get(), cp.get());
    }
}
```

차이를 한 번 정리하자.

- **컨텍스트 전달.** ThreadLocal 청소 코드가 사라지고 `ScopedValue.where().call()` 한 자리로 정리된다.
- **부모-자식 관계.** `StructuredTaskScope`가 그 관계를 *코드 구조*로 박았다. JFR thread dump에서 *나무*로 보인다.
- **Timeout.** scope의 `withTimeout`이 *전체*에 걸린다. 자식 셋 합쳐서 5초 — 자식 각자가 아니다.
- **취소 보장.** scope이 닫히는 순간 자식 셋이 *모두* interrupt된다. Loom-aware한 호출이라면 즉시 정리된다.
- **에러 일관성.** 자식 하나가 실패하면 나머지가 *즉시* 취소된다. 부분 성공으로 인한 inconsistent state가 사라진다.

11장에서 records, 12장에서 sealed, 13장에서 pattern matching, 14장에서 virtual thread, 16장의 이 자리에서 structured concurrency와 scoped values까지 — Modern Java가 *도구의 묶음*으로 자리 잡는 그림이 비로소 한 페이지에 모인다. 결제 컨트롤러 한 자리에 이 모든 도구가 들어간다.

### Spring과 ScopedValue: 이주의 자리

Spring의 `RequestContextHolder`·`SecurityContextHolder`·`LocaleContextHolder`는 모두 ThreadLocal 기반이다. 27년의 자바 컨벤션 위에 세워진 도구이니 당연하다. ScopedValue가 표준화된 지금, Spring 6/7이 ScopedValue 기반으로 *이주*할 가능성이 본격 검토 중이다. 정확한 시점과 API 모양은 *Spring 팀의 결정*에 달려 있다 — 이 책 시점에는 아직 ThreadLocal 기반이 안정적인 default다.

다만 우리 코드에서는 *지금부터* 새로 짜는 컨텍스트 전달은 ScopedValue로 옮기는 편이 낫다. 가령 사내 audit·tenant routing 같은 자리는 Spring을 거치지 않고 우리 손에 있는 자리다. 그 자리부터 ScopedValue로 익혀 두면, Spring의 이주가 들어왔을 때 자연스럽게 받아낼 수 있다. 21장에서 *한 결제 마이크로서비스에 모든 도구를 모으는* 자리에서 이 이주를 본격적으로 다룬다.

### 진화의 자리: JEP 428 → 533, 그리고 JEP 506

마지막으로 진화의 자리를 짚자. structured concurrency와 scoped values 둘 다 자바의 *preview 문화*를 가장 길게 통과한 도구다.

**Structured Concurrency**

- JEP 428 (Java 19, 2022 incubator) — 첫 등장. `java.util.concurrent` 외부 incubator로.
- JEP 437 (Java 20, second incubator)
- JEP 453 (Java 21, *preview*) — 표준 API 후보로 승격. 다만 *preview*.
- JEP 462 (Java 22, second preview)
- JEP 480 (Java 23, third preview)
- JEP 499 (Java 24, fourth preview)
- JEP 505 (Java 25, fifth preview... 또는 finalize)
- JEP 533 (가정 — Java 26 또는 25에서 finalize 시점). *사실 확인 필요: 정확한 finalize JEP 번호는 25 GA 노트 확인 권장.*

**Scoped Values**

- JEP 429 (Java 20, incubator)
- JEP 446 (Java 21, preview)
- JEP 464 (Java 22, second preview)
- JEP 481 (Java 23, third preview)
- JEP 487 (Java 24, fourth preview)
- **JEP 506 (Java 25, standard)** — 마침내 표준화.

두 도구가 5~7라운드의 preview를 거친 데에는 이유가 있다. *Joiner의 일반화*, *컨텍스트 전파 의미론*, *cancellation의 비동기성*, *기존 ExecutorService와의 호환* — 어느 하나도 가볍게 다듬을 수 없는 자리였다. preview 라운드마다 산업 피드백을 받아 *API의 모양*을 다듬었다. 5년의 다듬기를 거친 도구가 25 LTS에 안착했다. 11년의 자바를 *정직하게* 만들어 온 OpenJDK 문화의 본보기다.

### 마무리

structured concurrency와 scoped values는 자바의 동시성 모델에 *구조*를 돌려준 도구다. 호출자의 scope가 자식의 scope를 *감싸고*, 자식의 컨텍스트가 부모로부터 *immutable 참조*로 흘러내리며, scope이 끝나면 자식과 binding이 *함께* 정리된다. Dijkstra가 1968년에 그렸던 *구조*가 60년 만에 concurrent 코드의 자리까지 왔다.

자식 task의 fan-out, cancellation propagation, timeout, 컨텍스트 전달, 에러 일관성 — 옛 `ExecutorService`로 짜인 *흩어진* 자리가 한 블록으로 묶인다. ThreadLocal 청소를 잊어 다른 사용자의 audit log를 남기는 *끔찍한 일*은, 컨텍스트가 immutable binding이 되면서 *원천적으로* 사라진다. JFR thread dump가 *나무*로 보이는 production 디버깅의 후련함도 따라온다.

여기까지가 Part VII의 끝이다. 14·15·16장에서 *Loom 시대의 동시성*이 한 묶음으로 정리됐다. virtual thread가 *thread-per-request*를 돌려줬고, pinning과 ThreadLocal 함정의 자리를 정직하게 짚었으며, structured concurrency와 scoped values로 *구조*를 받아냈다. 이 묶음이 책의 *두 번째 봉우리*다.

다음 부에서는 그동안 미뤘던 *메모리·네이티브·성능*의 자리를 본격적으로 살펴보자. 17장에서 GC 11년의 진화를, 18장에서 Foreign Function & Memory API와 Vector API를, 19장에서 AOT와 Leyden을 차례로 펼친다. virtual thread가 *동시성의 단위 비용*을 낮췄듯이, 그쪽 도구들이 *시작 시간과 메모리의 단위 비용*을 어떻게 낮추는지 짚어보자.

---

# Part VIII. 메모리 · 네이티브 · 성능 · 도구

자바의 11년이 언어 표면에서만 일어난 게 아니다. JVM의 깊은 곳 — GC, 메모리 모델, 네이티브 호출, 시작 시간 — 에서도 11년 동안 거대한 변화가 일어났다. 람다와 records가 *눈에 보이는 변화*였다면, 이 부의 변화는 *알아채기는 어렵지만 코드의 성능을 결정짓는* 변화들이다.

17장은 GC의 11년이다. Java 8의 PermGen OOM 새벽 알람부터 시작해 G1의 안착, ZGC와 Shenandoah의 등장, Java 21의 Generational ZGC, Java 25의 Generational Shenandoah까지. 각 GC가 *어떤 메모리 모델*을 가정하는지, *어떤 워크로드*에 맞는지, JFR로 GC를 *어떻게 직접 측정하는지* — "우리 서비스는 G1로 두면 된다"는 한 줄의 통념을 정직하게 흔든다.

18장은 *Foreign Function & Memory API*(FFM)와 *Vector API*, *Class-File API*다. JNI의 `*.h` 추출에 하루를 통째로 쓴 그날의 그 *번거로움*이 어떻게 한 줄의 `Linker.downcallHandle()`로 바뀌는지, native crash로 JVM이 통째 죽던 그 *끔찍한 새벽*이 어떻게 `Arena`의 안전한 메모리 관리로 옮겨가는지를 본다. Project Panama의 결실이 이 자리에 모인다.

19장은 *AOT · Leyden · Compact Object Headers*다. AWS Lambda의 8초 콜드 스타트 알람이 어떻게 풀리는지, GraalVM 네이티브 이미지와 Project Leyden의 AOT Cache가 어떻게 *다른 답*을 내놓는지, Compact Object Headers(Java 25, JEP 519)가 64비트 JVM의 object header를 어떻게 64비트로 압축해 메모리 ~22%를 돌려주는지. 시작 시간과 메모리의 새 풍경이 이 장에 펼쳐진다.

19A장은 *모던 자바의 도구들*이다. JShell·jpackage·jlink·jdeps·JFR·jdeprscan·jextract — 11년의 자바가 만든 도구 일습을 한 자리에 모은다. 매일 IDE에 가려 안 보이던 도구들이 *우리 손에 있던 그것이었음*을 정직하게 짚는다. CI 파이프라인 한 줄에 하루를 쓰던 그 *피곤함*이 풀리는 자리이기도 하다.

이 네 장이 묶여 *눈에 안 보이는 자바*의 11년을 본다. 표면의 변화가 아무리 크더라도, 결국 production에서 우리의 코드를 떠받치는 건 JVM의 이 깊은 변화들이다.

---

## 17장. GC 11년의 진화 — Serial부터 Generational Shenandoah까지

Java 8의 `PermGen` OOM에 시달려본 사람이라면, 그 새벽의 알람 진동을 잊지 못할 것이다.

`java.lang.OutOfMemoryError: PermGen space`. 운영 중인 서비스가 갑자기 죽는다. heap은 멀쩡한데 PermGen이 꽉 찼다. `-XX:MaxPermSize=256m`을 올린다. 며칠 뒤 또 죽는다. ClassLoader 누수의 원인을 찾아 `Tomcat` 컨테이너의 webapp 재배포 로직을 헤매고, 결국 `-XX:MaxPermSize`를 512m으로 올리고 한숨을 쉰다. PermGen은 클래스 메타데이터를 담는 고정 영역이었고, 그 크기는 JVM 시작 시 못박혔다. 클래스가 늘어나면 죽었다. 무슨 일을 해도 *찜찜했다*.

Java 8이 PermGen을 없앤 건 그래서 사건이었다. 클래스 메타데이터를 native memory의 `Metaspace`로 옮겼다. heap이 아니다. JVM이 OS에서 직접 가져오는 메모리다. 기본값은 무제한 — `-XX:MaxMetaspaceSize`를 명시하지 않으면 시스템이 허락하는 만큼 늘어난다. PermGen OOM은 사라졌다. 그 자리에 다른 문제가 들어섰다. Docker 컨테이너의 `RSS`(Resident Set Size)가 슬금슬금 자라기 시작했다. CleverTap의 마이그레이션 회고가 짚어주듯, G1·JFR·Metaspace가 합산되면서 Docker OOM kill이 빈발했다([CleverTap Tech Blog](https://tech.clevertap.com/pitfalls-when-upgrading-from-java-8-to-java-17/)). heap 안의 OOM은 사라졌지만, 컨테이너 밖에서 *죽는* 새 패턴이 등장한 것이다.

11년이 지났다. 그사이 자바의 GC는 한 번 더, 그리고 또 한 번 더 옷을 갈아입었다. ZGC가 들어왔고, Shenandoah가 들어왔고, 둘 다 세대형으로 진화했다. Generational ZGC는 기본값이 됐고, 2025년 9월의 Java 25는 Shenandoah까지 세대형으로 만들어 냈다. 우리는 그동안 `-Xms`와 `-Xmx`만 만지면서 살아왔다. 그런데 — 솔직해지자. 우리 서비스는 어떤 GC를 써야 하는가? 그 질문에 한 문장으로 답할 수 있는 동료가 팀에 몇이나 있는가?

이 장은 그 질문에 답하기 위해 11년의 GC 지형을 한 장의 지도로 펼쳐 보이는 일이다. 9종의 GC가 차례로 들어왔다 사라졌고, 그 사이의 트레이드오프는 우리가 흔히 알고 있는 것보다 훨씬 정교하다. 함께 짚어보자.

### 9종의 GC 지형

먼저 한 번 정리하고 가자. 2026년 현재, OpenJDK가 손에 쥐고 있는 GC는 모두 아홉 종이다. 그중 하나(CMS)는 죽었고, 둘(Generational ZGC, Generational Shenandoah)은 새로 태어났다. 나머지는 그 사이에서 각자의 자리를 지키고 있다.

| GC | 첫 등장 | 메커니즘의 핵심 | 권장 사례 |
|---|---|---|---|
| Serial | 초기 | single-threaded, stop-the-world | embedded, 단일 CPU |
| Parallel | 1.4 | throughput 우선, 멀티스레드 STW | batch, throughput-bound |
| CMS | 1.4 (deprecated 9, removed 14) | concurrent old-gen mark-sweep | 옛 latency-sensitive — **사망** |
| **G1** | 7 (default 9+) | region-based, predictable pause | 일반 enterprise default |
| **ZGC** | 11 experimental, 15 production | colored pointers, sub-ms pause | 대용량 heap, low-latency |
| **Generational ZGC** | 21 (JEP 439), default 23 (JEP 474) | ZGC + 세대 분리 | 21+ default for low-latency |
| **Shenandoah** | 12 experimental, 15 production | concurrent compaction (Red Hat) | Red Hat ecosystem |
| **Generational Shenandoah** | 25 (JEP 521) | Shenandoah + 세대 | 25+ Red Hat 환경 |
| Epsilon | 11 (JEP 318) | no-op, 메모리 회수 안 함 | 테스트·short-lived |

표만 보면 단순하다. 그러나 이 한 줄짜리 칸들 안에는 11년의 설계 결정과 트레이드오프가 압축돼 있다. 하나씩 풀어보자.

**Serial과 Parallel은 여전히 살아 있다.** 우리가 자주 잊는 사실이다. Serial은 단일 CPU 환경, 작은 heap, 시작 시간이 짧아야 하는 짧은 lifecycle 프로세스에서 여전히 합리적이다. Parallel은 throughput을 최우선으로 둔 batch 작업에서 G1보다 나은 선택일 수 있다. STW pause가 길어도 상관없다면 — 그러니까 사용자 응답성을 신경 쓰지 않는 야간 ETL이라면 — Parallel의 throughput 우위가 빛난다. *잊지 말자*. 모든 워크로드가 sub-ms pause를 원하는 건 아니다.

**CMS는 죽었다.** JEP 363(Java 14)이 공식 사망 진단서다. concurrent mark-sweep으로 한때 latency-sensitive 자바의 사실상 표준이었지만, 단편화·복잡한 튜닝 노브·old-gen 단일화의 한계로 G1과 ZGC에 자리를 내줬다. 옛 코드베이스에서 `-XX:+UseConcMarkSweepGC` 플래그를 만나면 *반드시* 다른 GC로 갈아끼워야 한다. 14 이상에서는 그 플래그 자체가 인식되지 않거나 경고를 띄운다.

**G1은 사실상의 default다.** Java 9부터 server-class machine의 기본 GC가 됐고(JEP 248), 11년이 지난 지금도 압도적 다수의 Spring Boot 서비스가 G1 위에서 돌아간다. 핵심 아이디어는 *region-based*다. heap을 1~32MB 크기의 region으로 잘게 쪼개고, GC 사이클마다 *garbage가 가장 많은 region*을 우선 수집한다("Garbage First"). pause time을 직접 목표로 설정할 수 있다는 점이 매력이다 — `-XX:MaxGCPauseMillis=200`이라고 하면 G1은 그 목표를 향해 region 수집 개수와 cycle 빈도를 조절한다. *예측 가능한 pause*가 G1의 정체성이다.

**ZGC와 Shenandoah는 다른 방향에서 같은 문제를 풀었다.** "STW pause를 사실상 0에 가깝게 만들 수 없을까?" 둘 다 *concurrent compaction*을 답으로 내놨다. 객체 이동(compaction)을 애플리케이션 스레드와 동시에 수행한다. 그러나 *어떻게* 동시에 수행하느냐에서 갈렸다.

ZGC는 **colored pointers**(또는 load barriers)를 쓴다. 64비트 포인터에 GC 상태 비트를 박아 둔다. 객체에 접근할 때마다 그 비트를 읽고, 필요하면 forward — 즉, "이 객체는 이미 이사 갔다, 새 주소로 가라"라는 신호를 받아 새 주소로 redirect한다. 객체 이동 자체는 GC 스레드가 하고, 애플리케이션 스레드는 load 시점에 한 번 barrier 비용을 낼 뿐이다. pause는 mark 시작과 끝의 짧은 root scan뿐이고, 그것도 sub-millisecond 수준이다([ZGC: Production-Ready](https://openjdk.org/jeps/377)).

Shenandoah는 **Brooks pointer**(또는 forwarding pointer)를 쓴다. 모든 객체 헤더에 forwarding 슬롯을 하나씩 박아 놓는다. 객체 이동이 일어나면 그 슬롯에 새 주소를 적고, 접근하는 쪽이 forwarding을 따라간다. ZGC와 마찬가지로 sub-ms pause를 달성하지만, 메모리 오버헤드의 위치가 다르다 — ZGC는 포인터 자체에, Shenandoah는 객체 헤더에 비용을 둔다.

둘 다 결과는 비슷하다. heap이 1TB까지 늘어나도 pause는 millisecond 단위로 유지된다. G1이 약속한 "예측 가능한 pause"를 ZGC와 Shenandoah는 "거의 0인 pause"로 끌고 갔다.

**Epsilon은 농담이 아니다.** JEP 318(Java 11)으로 들어온 *no-op GC*다. 메모리를 회수하지 않는다. 할당만 하다가 heap이 차면 OOM으로 죽는다. 쓸모없는 것 같지만, GC 성능 측정의 baseline으로 매우 유용하다 — "GC가 없을 때의 처리량은 얼마인가?"를 측정하는 도구. 또 짧은 lifecycle batch 작업에서 *GC 자체의 비용*이 부담이라면, 충분한 heap을 주고 Epsilon으로 돌리는 선택도 있다. *기억해두자*. 자바는 GC가 없는 모드까지 갖고 있다.

여기까지가 지도다. 그러나 이 지도만으로는 "우리 서비스는 어떤 GC를 써야 하는가"에 답할 수 없다. 11년의 진화 *순서*를 따라 들어가 봐야 한다.

### ZGC의 11년 — experimental에서 default까지

ZGC의 여정은 자바 GC 진화의 척추다. 7년 만에 experimental에서 default로 올라온 이 GC의 궤적을 따라가면, 자바가 어떤 방향으로 가고 있는지가 보인다.

**JEP 248(Java 9)** — G1이 server-class 기본 GC가 됐다. 그전까지 Parallel이 default였다. 이 변경은 자바가 "throughput보다 predictable pause"로 무게중심을 옮긴 첫 신호다.

**JEP 333(Java 11)** — ZGC가 experimental로 들어왔다. "scalable, low-latency"라는 깃발을 들고. 당시 ZGC의 약속은 단순했다: heap 크기와 *무관하게* pause 10ms 이하. 그러나 experimental이었고, Linux/x64에서만 돌았고, JEP 333 원문이 명시하듯 "preliminary"라는 단어를 떼지 못한 상태였다.

**JEP 377(Java 15)** — ZGC가 production-ready 선언. 동시에 JEP 379로 Shenandoah도 production-ready. 두 GC가 같은 릴리스에서 정식 데뷔를 했다. 이때부터 *대용량 heap + low latency* 워크로드가 본격적으로 ZGC를 검토하기 시작했다.

**JEP 376(Java 16)** — Concurrent Thread-Stack Processing. ZGC가 thread stack을 stop-the-world 없이 처리할 수 있게 됐다. 이 변경으로 *사실상 모든* GC 작업이 concurrent가 됐다. STW pause는 sub-millisecond로 떨어졌다.

**JEP 439(Java 21)** — Generational ZGC. 가장 큰 진화다. 원래 ZGC는 단일 세대였다 — young/old 구분 없이 전체 heap을 한 번에 다뤘다. JEP 439는 ZGC에 *세대 분리*를 도입했다. 이유는 단순하다. "**대부분의 객체는 일찍 죽는다**"(generational hypothesis)는 30년 묵은 관찰을 ZGC도 활용하게 됐다. young region을 자주 청소하고 old region은 드물게 청소하면, 같은 throughput에 더 적은 메모리 오버헤드. JEP 439의 평가에 따르면 throughput이 ~10% 향상됐다.

**JEP 474(Java 23)** — Generational ZGC가 default. `-XX:+UseZGC`만 켜면 자동으로 generational이다. non-generational ZGC를 쓰려면 `-XX:-ZGenerational`을 명시해야 한다. JEP 474 원문은 default 변경의 의도를 "*대다수의 워크로드에서 더 낫기 때문*"이라고 표현한다([JEP 474](https://openjdk.org/jeps/474)). 11년 전 experimental로 들어온 GC가 default 자리로 올라온 것이다.

**JEP 521(Java 25)** — Generational Shenandoah. Red Hat 진영의 답이 한 박자 늦게 같은 방향으로 갔다. Shenandoah도 세대형이 됐다. ZGC가 23에 default를 차지한 상황에서 Shenandoah는 자기 진영의 사용자(Red Hat·OpenJDK distro)에게 같은 throughput 향상을 약속하면서 따라붙었다.

이 순서를 한 줄로 요약하면 이렇다. **GC는 "STW를 줄이는 경쟁"에서 "STW 없이 throughput까지 챙기는 경쟁"으로 옮겨 갔다.** sub-ms pause는 이제 기본 조건이고, 그 위에서 메모리 오버헤드를 어떻게 줄일지가 새 전장이다. 11년 전 PermGen OOM 알람에 새벽에 깨던 우리가 지금은 sub-ms pause를 "당연한 것"으로 다루는 시대에 와 있다.

### PermGen에서 Metaspace로 — 그리고 컨테이너의 함정

GC 9종의 지도를 살피기 전에, 우리가 한 번 멈춰 서서 정리해야 할 변화가 있다. 본문 첫 단락에서 잠깐 언급한 *PermGen 제거*다. 이 변경은 단순한 영역 이름 변경이 아니라, 자바 메모리 모델 전체와 컨테이너 환경의 상호작용을 바꿔놓은 사건이다.

Java 7까지의 PermGen은 클래스 메타데이터(클래스 구조, method bytecode, interned string)를 담는 *heap 안*의 고정 영역이었다. JVM 시작 시 `-XX:MaxPermSize`로 크기가 결정됐고, 그 한계를 넘으면 `OutOfMemoryError: PermGen space`로 죽었다.

Java 8(JEP 122)이 PermGen을 없애고 **Metaspace**를 도입했다. 클래스 메타데이터를 heap 밖, native memory로 옮겼다. `-XX:MaxMetaspaceSize`를 명시하지 않으면 기본값은 사실상 무제한이다. heap 안의 클래스 OOM은 사라졌다.

그런데 — 이 변화가 컨테이너 환경에서 *새로운 종류의 죽음*을 만들었다. *주의해야 한다*.

`docker stats`로 컨테이너의 메모리 사용량을 보면, 자바 프로세스의 RSS가 heap 크기보다 훨씬 크다. `-Xmx4g`로 설정한 컨테이너에서 RSS가 6GB를 찍는다. 어디로 갔는가? 답은 *off-heap 영역의 누적*이다.

- **Metaspace**: 클래스 메타데이터. 평범한 Spring Boot 앱이 200~400MB를 쓴다.
- **Direct memory**: `ByteBuffer.allocateDirect()`, Netty의 PooledByteBufAllocator.
- **JIT code cache**: `-XX:ReservedCodeCacheSize` 기본값이 240MB.
- **JFR buffer**: Java 11+의 Flight Recorder가 항상 켜져 있을 수 있다.
- **GC 메타데이터**: ZGC/Shenandoah의 remembered set, forwarding table.
- **Thread stack**: 스레드당 1MB, 200개면 200MB.

이 모두가 합쳐져 RSS가 된다. heap 4GB + 위의 합산 2GB → 6GB. 컨테이너 limit이 6GB라면, 트래픽 스파이크 한 번에 Docker OOM kill이 떨어진다. *컨테이너 밖에서* 죽는다. heap OOM 로그는 없다. JVM은 `SIGKILL`을 받고 그냥 사라진다.

CleverTap의 마이그레이션 회고가 이 패턴을 정확히 기록한다 — Java 8에서 17로 올린 뒤 G1 + JFR + Metaspace의 합산이 늘어나면서 Docker OOM kill이 빈발했고, 컨테이너 메모리 limit을 상향해야 했다([CleverTap Tech Blog](https://tech.clevertap.com/pitfalls-when-upgrading-from-java-8-to-java-17/)). PermGen은 사라졌지만, 그 자리에 *컨테이너의 OOM kill*이 들어선 것이다.

**해결의 원칙은 단순하다.** heap만 보지 말고, off-heap 합산을 보자. `-Xmx`만 정하지 말고 `-XX:MaxMetaspaceSize`, `-XX:MaxDirectMemorySize`, `-XX:ReservedCodeCacheSize`까지 명시하는 편이 낫다. 그리고 그 합산이 컨테이너 limit의 *80% 이하*에 들어오는지 확인하자. Java 10+부터는 `-XX:UseContainerSupport`가 기본으로 켜져 있어 cgroup limit을 인식하지만, 그것은 *heap 크기*를 컨테이너 limit에 맞춰 자동 조절할 뿐, off-heap까지 보호하지 않는다. *잊지 말자*.

> **벤치마크 박스 1: Netflix의 ZGC 도입** *(사실 확인 필요)*
>
> Netflix는 일부 streaming 워크로드에서 G1에서 ZGC로 전환한 사례를 공유했다. 핵심 지표는 *tail latency*다. G1 환경에서 p99의 GC pause가 200~400ms를 찍던 워크로드가, ZGC로 전환하면서 sub-10ms로 떨어졌다. 단 throughput은 약간 떨어졌고(ZGC의 barrier 비용), 메모리 footprint는 ~15% 증가했다. 적용 기준은 단순했다: "tail latency가 사용자 경험에 직접 영향을 주는 워크로드"에만 적용하고, throughput이 우선인 batch는 G1을 유지. *(구체 수치는 JFokus·Devoxx 발표 슬라이드 추가 확인 필요)*

> **벤치마크 박스 2: Pinterest·LinkedIn의 사례** *(사실 확인 필요)*
>
> Pinterest는 ad serving 인프라에서 ZGC 전환으로 p99 latency가 안정화됐다고 발표. LinkedIn은 large heap(>50GB) 워크로드에서 G1의 mixed collection cycle이 가끔 길어지는 문제를 ZGC로 해소. 두 사례 모두 *heap 크기 ≥ 16GB + latency-sensitive*가 적용 기준이었다. *(구체 수치 출처 확인 필요)*

> **벤치마크 박스 3: 일반 Spring Boot 서비스의 경험치**
>
> heap 2~4GB의 일반 REST API에서 G1 → ZGC로 갈아끼웠을 때 차이는 미미한 경우가 많다. ZGC의 강점이 "*대용량 heap에서 sub-ms pause*"인데, 작은 heap에서는 G1도 충분히 짧은 pause를 낸다. 오히려 ZGC의 native memory 오버헤드와 throughput 손실이 더 두드러진다. **8GB heap 미만이라면 G1을 유지하는 편이 낫다**는 권고가 IBM Community와 foojay의 GC 가이드에서 공통적으로 등장한다([IBM Community](https://community.ibm.com/community/user/blogs/theo-ezell/2025/09/03/g1-shenandoah-and-zgc-garbage-collectors), [foojay 10-year GC guide](https://foojay.io/today/the-ultimate-10-years-java-garbage-collection-guide-2016-2026-choosing-the-right-gc-for-every-workload/)).

### 어떤 GC를 골라야 하는가 — 세 워크로드 시나리오

자, 이제 가장 자주 묻는 질문에 답해보자. "우리 서비스는 어떤 GC를 써야 하는가?" 추상적으로 답하면 또 *찜찜한* 가이드가 된다. 세 가지 구체적인 워크로드를 놓고 따져보자.

**시나리오 A: Spring Boot REST API, heap 2GB, Kubernetes pod**

가장 흔한 케이스다. 결제 처리, 상품 조회, 사용자 인증 같은 OLTP 성격의 API 서버. 동시 요청 수백~수천, 응답시간 p99 200ms 이내. heap은 컨테이너 limit에 맞춰 2~4GB.

**선택: G1 (default 유지).** 별도 플래그를 줄 필요가 없다. Java 9 이상이라면 G1이 자동이다. 명시적으로 적자면 `-XX:+UseG1GC -XX:MaxGCPauseMillis=200` 정도. 이 워크로드에서 G1을 ZGC로 갈아끼우는 건 *대개 비용이 이득보다 크다*. heap이 작아서 ZGC의 강점이 드러나지 않고, off-heap 오버헤드는 컨테이너 limit 안에서 더 빠듯해진다.

추가로 챙길 것 — 컨테이너 limit을 정할 때 `-Xmx`의 1.5배 정도를 잡자. heap 2GB라면 컨테이너 3GB. 그 안에 Metaspace, direct memory, JIT cache, thread stack이 들어간다. `-XX:MaxRAMPercentage=60` 같은 옵션으로 heap을 cgroup limit의 비율로 자동 잡는 패턴도 안정적이다. *기억해두자*. 컨테이너의 OOM kill은 heap의 OOM과 다른 곳에서 온다.

**시나리오 B: 캐시 서버, heap 50GB**

Redis 대체로 in-memory cache를 자바로 구현한 서비스, 또는 Elasticsearch처럼 대용량 인덱스를 heap에 올려둔 서비스. heap이 50GB를 넘고, p99 latency 요구가 빡빡하다. 한 번의 GC pause가 100ms를 넘으면 사용자가 느낀다.

**선택: Generational ZGC.** `-XX:+UseZGC`(Java 23+에서는 자동으로 generational). 이 케이스가 ZGC가 만들어진 이유다. 50GB heap에서 G1의 mixed collection이 가끔 1초를 찍는 일이 있고, 그게 캐시 서버에서는 치명적이다. ZGC는 같은 heap에서 sub-10ms pause를 약속한다. throughput 손실은 있지만, latency 안정성이 우선이라면 받아들일 수 있다.

Red Hat 진영(RHEL의 OpenJDK)이라면 **Generational Shenandoah**(Java 25+)도 같은 자리에 들어온다. `-XX:+UseShenandoahGC`. 두 GC의 선택은 디스트리뷰션과 익숙함의 문제지, 성능 차이가 결정적이지 않다.

**시나리오 C: 야간 ETL 배치 잡**

매일 02:00에 도는 데이터 파이프라인. JDBC로 OLAP DB에서 수억 행을 읽어 가공해 다른 곳으로 적재. 응답시간은 무관 — 사용자가 보지 않는다. 단지 *전체 처리량*과 *총 실행 시간*이 중요하다.

**선택: Parallel GC.** `-XX:+UseParallelGC`. throughput을 최우선으로 두는 GC. pause가 100ms든 500ms든 상관없다. 같은 시간에 더 많은 행을 처리하는 게 이긴다. G1도 나쁘지 않지만, throughput으로만 비교하면 Parallel이 작은 차이로 앞선다.

극단으로 가면 **Epsilon**도 후보다. heap을 처리량의 *2배 이상*으로 넉넉히 잡고 `-XX:+UseEpsilonGC -XX:+UnlockExperimentalVMOptions`. GC가 아예 돌지 않으니 throughput이 최대다. 단 잡 끝나면 JVM이 OOM으로 죽거나 종료된다. 그 죽음을 *의도된 끝*으로 받아들일 수 있는 워크로드라면 — 짧은 lifecycle batch가 그렇다 — Epsilon은 거짓말 같은 throughput을 낸다.

이 세 시나리오만 익혀두자. 대부분의 결정이 이 셋의 변형이다. *권장형으로 말하자면* — 잘 모르겠으면 G1을 쓰는 편이 낫다. 그게 default인 데에는 이유가 있다. ZGC로 갈아끼우는 건 *latency 측정 데이터*가 손에 있을 때만 하자. 단순히 "최신 GC가 좋겠지"라는 직관으로 옮기면, throughput과 RSS 증가에 발목을 잡힌다.

### Spring Boot에서의 GC 튜닝과 진단

Spring Boot 컨테이너에서 GC를 다루는 일은 두 단계로 나뉜다. *측정*과 *튜닝*. 그런데 우리는 자주 측정 없이 튜닝부터 한다 — `-XX:+UseG1GC -XX:MaxGCPauseMillis=100`을 어디선가 베껴 와서 붙인다. 이건 *번거롭다*. 측정부터 짚어보자.

**JFR(Java Flight Recorder)로 GC pause 진단하기.** Java 11에서 오픈소스화된 JFR은 production-grade 프로파일러다. 항상 켜두는 비용이 낮다(~1% 미만 오버헤드). GC 이벤트를 빠짐없이 기록한다.

```bash
java -XX:StartFlightRecording=duration=60s,filename=app.jfr,settings=profile \
     -jar app.jar
```

또는 production에서는 continuous recording으로:

```bash
-XX:StartFlightRecording=disk=true,maxage=1h,maxsize=200M,filename=app.jfr
```

이렇게 두면 JFR이 항상 돌면서 최근 1시간 또는 200MB까지의 이벤트를 디스크에 보관한다. 사고가 터지면 그 시점 직전의 데이터를 갖고 있다. JMC(Java Mission Control)에서 열어 `GC Pause` 이벤트를 본다. p99의 pause 길이가 어디서 튀는지, mixed collection이 길어지는 시점이 있는지 — 한눈에 보인다.

**Spring Boot Actuator의 메트릭과 결합.** `management.endpoints.web.exposure.include=health,info,metrics`를 켜두면 `/actuator/metrics/jvm.gc.pause`로 GC pause 분포를 가져올 수 있다. Micrometer가 Prometheus·Datadog로 보내면 Grafana 대시보드가 된다. *반드시 메트릭을 먼저 보고, 그 다음에 GC 옵션을 만지자*. 측정 없는 튜닝은 미신이다.

**일반적인 Spring Boot 권장 옵션 패턴.** 한 가지 시작점을 깔자면 이렇다.

```bash
-XX:MaxRAMPercentage=60
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+UnlockDiagnosticVMOptions
-XX:+LogVMOutput
-XX:StartFlightRecording=disk=true,maxage=1h,maxsize=200M,filename=/tmp/app.jfr,settings=profile
-Xlog:gc*:file=/tmp/gc.log:time,uptime,level,tags:filecount=10,filesize=50M
```

이게 모든 케이스의 답은 아니다. 그러나 *side effect가 적고 진단이 잘 되는* 시작점이다. heap은 cgroup limit의 60%로 자동 조절, G1으로 default 유지, GC pause 목표 200ms, JFR과 GC log를 디스크에 회전 저장. 사고가 터지면 데이터가 있다.

*권장하지 않는 패턴.* "`-XX:+UseStringDeduplication`을 항상 켜라", "`-XX:+ParallelRefProcEnabled`를 꼭 켜라" 같은 인터넷 블로그의 마법 주문들. 케이스에 따라 도움이 될 수도 있고 해가 될 수도 있다. *측정 없이 켜지 말자*.

### 메모리의 두 얼굴 — GC와 JMM 사이의 다리

이 장의 끝에서 한 번 멈춰 서서, 우리가 놓치고 가는 것을 짚어야 한다. 자바의 "메모리"는 사실 *두 얼굴*을 갖고 있다.

하나는 우리가 이 장에서 본 얼굴이다. heap, region, generation, pause, footprint. *물리적 메모리의 관리* — 어떤 객체를 어떤 영역에 두고, 어떻게 회수할 것인가. GC가 답하는 영역이다. 11년 동안 우리는 이 얼굴을 ZGC와 Generational Shenandoah까지 끌고 왔다. sub-ms pause라는 결과를 손에 쥐었다.

다른 하나는 **Java Memory Model**(JMM)이 그리는 얼굴이다. happens-before, volatile, final field semantics, synchronization order. *동시성 의미론으로서의 메모리* — 한 스레드의 쓰기가 다른 스레드에 *언제, 어떤 순서로* 보이는가. 8A장에서 우리가 만났던 그 영역이다. JLS §17.4가 명시하는 그 모델이다. JSR-133이 2004년에 풀어낸 그 약속이다.

이 두 얼굴은 자주 따로 다뤄진다. GC 튜닝하는 사람은 JMM을 잘 모르고, JMM을 다루는 사람은 GC 옵션에 무관심하다. 그러나 *둘은 한 메모리의 두 얼굴*이다. ZGC가 colored pointer로 객체를 옮겨도, 그 이동이 다른 스레드에 일관되게 보이려면 JMM의 happens-before가 받쳐줘야 한다. G1의 region 압축이 일어나는 동안 volatile read는 여전히 정확한 값을 봐야 한다. GC와 JMM은 *같은 메모리*에 대해 서로 다른 층위의 약속을 한다. 한 층은 *얼마나 빨리 회수하느냐*를, 다른 층은 *어떤 순서로 보이느냐*를 보장한다.

우리가 ZGC의 sub-ms pause를 신뢰할 수 있는 이유는, 그 GC가 JMM의 약속을 깨지 않기 때문이다. 11년의 GC 진화는 *JMM의 약속을 지키면서* throughput과 latency를 동시에 끌어올린 과정이었다. 8A장의 JMM과 이 장의 GC는 *한 메모리 위에서 함께 움직인다*. 둘 중 하나만 알면 절반만 아는 것이다.

다음 장에서는 그 메모리의 한 단계 *더 바깥*으로 나가본다. heap 안의 객체가 아니라, *heap 밖의 native memory*를 자바가 어떻게 다루게 됐는지. JNI에 시달리던 우리가 FFM과 만나는 그 자리다. 자바가 SIMD를 *표현*할 수 있게 된 그 자리다. ASM이 더 이상 필요 없게 된 그 자리다.

함께 걸어보자.

---

## 18장. Foreign Function & Memory API · Vector API · Class-File API

JNI `*.h` 추출에 하루를 통째로 쓴 그날을 기억하는가.

`zlib`을 자바에서 호출하고 싶었을 뿐이다. 그런데 일은 그렇게 단순하지 않았다. 먼저 `native` 메서드를 자바 코드에 선언한다. 그 다음 `javac`로 컴파일하고, `javah`로(또는 Java 8 이후엔 `javac -h`로) `.h` 헤더를 추출한다. 헤더에 적힌 `JNIEXPORT void JNICALL Java_com_example_Zlib_compress(JNIEnv *, jobject, jbyteArray)` 같은 길고 추한 시그니처를 보고 잠시 한숨을 쉰다. `.c` 파일에서 그 시그니처를 구현하는데, `(*env)->GetByteArrayElements`로 자바 배열을 C 배열로 끌어내고, 다 쓰면 `ReleaseByteArrayElements`로 풀어줘야 한다. 잊으면? 메모리 누수다. 잘못 푸는 순서를 짜면? *JVM 전체가 죽는다*.

그러고도 끝이 아니다. `gcc -shared -fPIC`로 `.so`를 빌드하고(Windows라면 `.dll`, Mac이라면 `.dylib`), `System.loadLibrary("zlib_wrapper")`로 자바가 그걸 찾을 수 있게 해야 한다. CI에서 빌드할 때 native toolchain이 자동으로 깔려 있어야 하고, 배포 환경의 glibc 버전과 빌드 환경의 glibc 버전이 안 맞으면 또 죽는다. 컨테이너에 native shared library를 같이 패키징해야 하고, ARM과 x64 양쪽 빌드를 따로 굴려야 한다. *번거롭다*는 말로 부족하다. *끔찍한 일이다*.

이 모든 것이 — 우리는 그저 `zlib`의 `compress` 함수를 자바에서 부르고 싶었을 뿐이다.

JNI에 시달려본 사람이라면, JNI가 *왜 끝나야 했는지* 굳이 설명할 필요가 없다. 그러나 끝났다는 *증거*는 필요하다. 진짜로 끝났는가? 자바는 이제 `*.h` 없이 native를 부를 수 있는가? 그리고 — *그것만으로는 부족하다*. 우리는 또 두 가지 질문을 동시에 던지고 있다. "자바는 SIMD를 어떻게 표현하는가?", "ASM·BCEL로 바이트코드를 생성하던 그 *부족 비밀*은 이제 무엇으로 대체되는가?"

이 세 질문이 한 장에 모인 이유는 분명하다. 세 변화 모두 *Project Panama*의 깃발 아래에서 진행됐고, 셋 모두 자바를 "native ecosystem과 더 가깝게" 가져가려는 한 흐름의 다른 얼굴이다. 함께 살펴보자.

### §18.1 FFM — JNI 시대의 종료

**Foreign Function & Memory API**의 여정을 한 줄로 요약하면 이렇다. Java 14의 incubator에서 Java 22의 표준으로, 8년에 걸친 점진적 진화.

| JEP | Java | 단계 |
|---|---|---|
| 370 | 14 | Foreign-Memory Access API (Incubator) |
| 412 | 17 | Foreign Function & Memory API (Incubator) — 17 LTS에 들어옴 |
| 419 | 18 | Second Incubator |
| 424 | 19 | Preview |
| 434 | 20 | Second Preview |
| 442 | 21 | Third Preview — 21 LTS에 들어옴 |
| **454** | **22** | **Standard** — JNI 시대 종료의 시작 |

이 9개 릴리스에 걸친 점진성이 자바의 진화 방식을 잘 보여준다. *서두르지 않는다*. preview에서 incubator에서 standard로 가는 동안 API 표면이 다듬어지고, 8년 후에 표준이 된다. 그 결과로 우리 손에 들어온 추상은 깔끔하다. 핵심 다섯 개만 짚어보자.

#### MemorySegment — native memory의 일급 추상

`MemorySegment`는 *어딘가에 존재하는 메모리 영역*을 표현한다. heap일 수도 있고, native memory일 수도 있고, mapped file일 수도 있다. 어디에 있든 `MemorySegment` 하나로 다루는 것이 핵심이다.

```java
MemorySegment segment = arena.allocate(100); // native memory 100바이트
segment.set(ValueLayout.JAVA_INT, 0, 42);    // offset 0에 int 42 쓰기
int value = segment.get(ValueLayout.JAVA_INT, 0); // 읽기
```

`set`/`get`은 `ValueLayout`을 받는다 — `JAVA_INT`, `JAVA_LONG`, `JAVA_DOUBLE` 같은 primitive layout이거나, `ADDRESS`(포인터)이거나, 또는 우리가 직접 정의한 `StructLayout`이다. C의 `struct sockaddr_in` 같은 구조체를 자바에서 그대로 표현할 수 있다. *기억해두자*. JNI 시절에는 `Get*ArrayElements`로 자바 배열을 native 쪽에서 빌려와야 했지만, FFM은 그 경계 자체가 사라졌다.

#### Arena — lifetime 관리의 핵심

native memory의 가장 어려운 문제는 *언제 해제할 것인가*다. 너무 일찍 해제하면 use-after-free, 너무 늦으면 누수. C 프로그래머가 평생 씨름하는 그 문제. FFM은 `Arena`로 이 문제를 try-with-resources의 영역으로 끌어왔다.

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
    // segment 사용
} // arena가 닫히면서 segment 자동 해제
```

`Arena`에는 세 가지 종류가 있다.

- **`Arena.ofConfined()`**: 한 스레드 안에서만 쓸 수 있다. 다른 스레드가 접근하면 즉시 예외. 가장 빠르고 가장 안전하다. 대부분의 경우 이걸 쓰는 편이 낫다.
- **`Arena.ofShared()`**: 여러 스레드에서 공유한다. 그 대신 약간의 동기화 비용. 동일 native 리소스를 여러 worker에서 접근해야 할 때.
- **`Arena.ofAuto()`**: GC가 해제 시점을 결정한다. C의 `malloc`처럼 들고 다니다가, 더 이상 참조되지 않으면 자동 해제. 가장 자바스럽지만, *정확한 해제 시점이 보장되지 않는다*는 함정이 있다. 즉시성이 필요하면 confined나 shared를 쓰자.

이 세 가지 lifetime 모델은 단순한 API 디자인이 아니다. JNI에서 *완전히 빠져 있던* 안전망이다. JNI는 누가 언제 메모리를 풀어줄지 약속하지 않았다. FFM은 그 약속을 try-with-resources의 문법으로 못 박는다. 누수와 use-after-free는 *컴파일러가 아니라 런타임이 잡아준다*. confined arena에 다른 스레드가 접근하면 `WrongThreadException`이 즉시 떨어진다. 침묵하는 메모리 손상이 아니라 *시끄러운 실패*다.

#### Linker — C 함수의 호출

native 메모리만으로는 부족하다. C 함수를 *불러야* 한다. `Linker`가 그 일을 한다.

```java
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MemorySegment strlenAddr = stdlib.find("strlen").orElseThrow();

MethodHandle strlen = linker.downcallHandle(
    strlenAddr,
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment cStr = arena.allocateUtf8String("Hello, FFM");
    long len = (long) strlen.invoke(cStr);
    System.out.println(len); // 10
}
```

세 단계다. *어디에 있는지 찾고*(`SymbolLookup.find`), *시그니처를 적고*(`FunctionDescriptor`), *MethodHandle을 얻어서 부른다*. `FunctionDescriptor.of(returnType, argTypes...)`는 C 함수의 시그니처를 자바 쪽 표현으로 옮긴 것이다. `strlen`은 `size_t strlen(const char *)`이니 return은 `JAVA_LONG`, arg는 `ADDRESS`.

이게 JNI의 `Java_com_example_...` 시그니처를 직접 적던 시절과 비교가 되는가? 자바 코드 안에서 *자바 문법으로* C 함수의 시그니처를 표현한다. `.h` 헤더도, `.c` 구현도, `gcc` 빌드도, `loadLibrary`도 필요 없다. `defaultLookup()`이 libc의 함수를 찾아주고, 우리 라이브러리라면 `SymbolLookup.libraryLookup(path, arena)`로 `.so`를 직접 열 수 있다.

#### jextract — 헤더 자동 바인딩

그런데 — 정직하게 짚자. 위의 `Linker` 코드를 *모든 함수마다 손으로 적는 일*은 여전히 *번거롭다*. `zstd` 라이브러리에 함수가 100개라면? 100번을 적는가? 그건 JNI 시대와 다를 게 없다.

이 자리에 **jextract**가 들어선다. C 헤더 파일을 입력으로 받아 자바 바인딩을 자동 생성한다.

```bash
jextract --output src/main/java \
         -t com.example.zstd \
         /usr/include/zstd.h
```

이 한 줄로 `zstd.h`의 모든 함수·struct·constant가 자바 클래스로 풀린다. 우리가 손에 쥐는 건 `com.example.zstd.zstd_h.ZSTD_compress(...)` 같은 깔끔한 static 메서드들이다. C struct는 자바의 `StructLayout`으로 풀리고, constant는 자바 static 필드가 된다. `-l zstd` 옵션을 주면 `loadLibrary` 호출까지 코드에 묻혀 나온다.

JNI 시대의 하루치 작업이 *5분으로* 줄어든다. 과장이 아니다.

#### 예제 — JNI에서 FFM으로

이론은 충분하니, 실제 ZNI 코드가 FFM으로 어떻게 갈아끼워지는지 한 번 보자. 압축 라이브러리 `zstd`를 부르는 코드.

**JNI 시대 (~50줄의 native + 자바 양쪽 코드)**

```java
public class ZstdJni {
    static { System.loadLibrary("zstd_wrapper"); }
    public native byte[] compress(byte[] input);
}
```

```c
// ZstdJni.c
#include <jni.h>
#include <zstd.h>

JNIEXPORT jbyteArray JNICALL
Java_com_example_ZstdJni_compress(JNIEnv *env, jobject this, jbyteArray input) {
    jsize len = (*env)->GetArrayLength(env, input);
    jbyte *src = (*env)->GetByteArrayElements(env, input, NULL);
    size_t bound = ZSTD_compressBound(len);
    jbyteArray result = (*env)->NewByteArray(env, bound);
    jbyte *dst = (*env)->GetByteArrayElements(env, result, NULL);
    size_t actual = ZSTD_compress(dst, bound, src, len, 3);
    (*env)->ReleaseByteArrayElements(env, input, src, JNI_ABORT);
    (*env)->ReleaseByteArrayElements(env, result, dst, 0);
    // actual로 jbyteArray 크기를 자르는 추가 작업 필요...
    return result;
}
```

`.h` 추출, `.c` 컴파일, `.so` 빌드, 배포 패키징, 플랫폼별 빌드 — 그 모든 작업이 코드 *바깥*에서 따라붙는다.

**FFM 시대 (jextract로 만든 바인딩 사용)**

```bash
jextract -lzstd -t com.example.zstd /usr/include/zstd.h
```

```java
import static com.example.zstd.zstd_h.*;

public class ZstdFfm {
    public byte[] compress(byte[] input) {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment src = arena.allocate(input.length);
            MemorySegment.copy(input, 0, src, ValueLayout.JAVA_BYTE, 0, input.length);

            long bound = ZSTD_compressBound(input.length);
            MemorySegment dst = arena.allocate(bound);

            long actual = ZSTD_compress(dst, bound, src, input.length, 3);
            byte[] result = new byte[(int) actual];
            MemorySegment.copy(dst, ValueLayout.JAVA_BYTE, 0, result, 0, (int) actual);
            return result;
        }
    }
}
```

`.c`도, `.h`도, `gcc`도, `loadLibrary`도 없다. 자바 코드만 있다. lifetime은 `try-with-resources`로 명시. `WrongThreadException`이 잘못된 스레드 접근을 즉시 잡아준다. native가 crash해도 JVM 전체가 죽지 않는다 — FFM은 더 *안전한 경계*에서 호출한다.

**JNI는 정말 끝났는가?** 솔직히 답하자. *기존 코드는 여전히 JNI다*. 그리고 그 코드를 당장 갈아끼울 동기가 없을 수 있다. 그러나 *새로 짜는 native 호출은 더 이상 JNI를 쓸 이유가 없다*. Spring Boot 6 시대, Java 21 이상의 베이스라인에서 새 native 통합은 FFM이다. 암호화 라이브러리(libsodium, openssl), 압축(zstd, lz4), DB driver의 일부 hot path — 모두 FFM으로 옮겨 가고 있다. *권장형으로 말하자면*, JNI 코드를 새로 짤 생각이 든다면 한 번 멈춰 서서 FFM을 검토하는 편이 낫다.

### §18.2 Vector API — 자바가 SIMD를 표현하는 법

다음 질문으로 넘어가자. *자바는 SIMD를 어떻게 표현하는가?*

CPU에는 *SIMD*(Single Instruction Multiple Data) 명령이 있다. AVX2는 256비트 레지스터에 int 8개를 한 번에 곱하고, AVX-512는 512비트에 int 16개를 한 번에. ARM의 NEON·SVE도 같은 일을 한다. ML inference, 이미지 처리, 행렬 연산, 압축 — 모든 numeric loop가 SIMD로 *수 배에서 십수 배* 빨라진다.

그런데 — 자바에서 *어떻게* 표현하는가? 11년 전 답은 "*JNI로 C++ SIMD 라이브러리를 부른다*"였다. 또는 "*JIT의 auto-vectorization을 믿고 손은 안 댄다*". 둘 다 만족스러운 답이 아니다. JIT은 단순한 루프만 vectorize하고, JNI는 위에서 본 그 모든 비용을 짊어진다.

#### Vector API의 9년 incubator

| JEP | Java | 단계 |
|---|---|---|
| 338 | 16 | First Incubator |
| 414 | 17 | Second Incubator |
| 417 | 18 | Third Incubator |
| 426 | 19 | Fourth Incubator |
| 438 | 20 | Fifth Incubator |
| 448 | 21 | Sixth Incubator |
| 460 | 22 | Seventh Incubator |
| 469 | 23 | Eighth Incubator |
| **489** | **24** | **Ninth Incubator** — *아직 표준 아님* |

9년째 incubator다. *왜 표준이 안 되는가?* 답은 단순하지 않지만 한 단어로 요약하면 **Valhalla**다. Project Valhalla의 value class(이전 이름 "inline class", "primitive class")가 들어오면, Vector API의 핵심 타입(`Vector`, `IntVector`, `FloatVector`)이 value class로 다시 설계돼야 한다. 지금 표준으로 굳히면 Valhalla가 들어왔을 때 backward incompatibility가 생긴다. 그래서 *기다리는* 중이다. 자바의 *서두르지 않는 진화*가 가장 길게 적용된 사례다.

#### 핵심 API — VectorSpecies와 lane operation

Vector API의 코드 모양을 한 번 보자. 두 float 배열의 점곱(dot product).

```java
import jdk.incubator.vector.*;

public class DotProduct {
    static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

    public static float dot(float[] a, float[] b) {
        float sum = 0f;
        int i = 0;
        int upperBound = SPECIES.loopBound(a.length);
        FloatVector acc = FloatVector.zero(SPECIES);

        for (; i < upperBound; i += SPECIES.length()) {
            FloatVector va = FloatVector.fromArray(SPECIES, a, i);
            FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
            acc = acc.add(va.mul(vb));
        }
        sum = acc.reduceLanes(VectorOperators.ADD);

        // 꼬리 처리 (배열 길이가 lane 수의 배수가 아닐 때)
        for (; i < a.length; i++) sum += a[i] * b[i];
        return sum;
    }
}
```

`VectorSpecies`가 핵심이다. `SPECIES_PREFERRED`는 *현재 CPU에서 가장 효율적인 lane 수*를 자동으로 고른다. AVX-512가 있으면 16, AVX2면 8, NEON이면 4. 코드는 한 번 짜고, JVM이 알아서 매핑한다. 같은 자바 코드가 x64에서는 AVX-512로, ARM에서는 NEON으로 컴파일된다. *이 추상이 자바 SIMD의 정체성이다*.

`fromArray`로 배열을 vector로 끌어오고, `mul`·`add`로 lane별 연산을 한 번에 한다. 256비트 vector라면 float 8개의 곱셈이 *한 명령*으로 끝난다. 마지막에 `reduceLanes(ADD)`로 lane들을 합산해 스칼라 결과를 얻는다.

성능 차이는 *워크로드에 따라* 2배~10배. ML inference의 inner loop, 이미지 필터의 컨볼루션, 압축 알고리즘의 hash, 암호화의 round function — 이런 hot path에서 효과가 두드러진다.

#### 언제 쓰는가 — 그리고 언제 쓰지 말아야 하는가

Vector API는 *매력적이지만 만능이 아니다*. *주의해야 한다*. 몇 가지 함정.

**incubator라는 사실 자체.** `jdk.incubator.vector` 모듈에 들어 있고, 코드 빌드 시 `--add-modules jdk.incubator.vector --enable-preview`(릴리스에 따라) 같은 옵션이 필요하다. production에서 incubator API를 쓴다는 건 *다음 릴리스에서 API가 깨질 수 있다*는 약속을 받아들이는 일이다. 9년째 incubator이긴 하지만, 그 말은 9년째 *공식 안정성 보장이 없다*는 뜻이기도 하다.

**단순한 루프는 JIT이 알아서 한다.** `for (int i = 0; i < a.length; i++) c[i] = a[i] * b[i];`처럼 명백한 패턴은 HotSpot의 auto-vectorizer가 SIMD로 컴파일한다. Vector API를 직접 쓰는 이득이 없다. *측정해보고 쓰자*.

**Valhalla 이전의 박싱 비용.** 현재 Vector API의 vector 타입은 reference type이다. 자주 생성·소멸하면 allocation 비용이 따라붙는다. JIT의 escape analysis가 잘 박혀 들어가면 stack-allocated로 풀리지만, 그게 보장되지 않는다. *Valhalla의 value class가 들어와야 진정한 zero-cost*다.

**Spring에서의 자리.** 일반 Spring Boot 비즈니스 로직에는 Vector API의 자리가 거의 없다. 적합한 자리는 *극히 좁다* — 이미지 처리 마이크로서비스, ML inference 서버, 암호화 hot path, 압축 코덱. 만약 우리가 손으로 SIMD를 쓰고 싶을 만큼 numeric loop가 hot path에 있다면 그제야 검토하자. 그 외에는 *기다리는 편이 낫다*. Valhalla가 들어오면 그때 다시 살펴봐도 늦지 않다.

### §18.3 Class-File API — ASM 시대의 종료

세 번째 질문. *ASM은 무엇으로 대체되는가?*

자바의 *부족 비밀* 같은 도구가 있다. **ASM**. OW2 컨소시엄의 바이트코드 조작 라이브러리. Spring AOP의 dynamic proxy가 ASM 위에서 돌고, Hibernate의 lazy proxy도 ASM. Lombok이 컴파일 타임에 바이트코드를 변형하고, ByteBuddy가 ASM을 감싸 더 친절한 API를 제공한다. CGLib, Javassist, BCEL — 모두 같은 자리에서 싸워 온 라이브러리들.

ASM은 강력하지만 *사용자 경험이 끔찍하다*. visitor 패턴, magic number 가득한 opcode 상수, 매 JDK 릴리스마다 새 class file format을 따라잡아야 하는 maintenance 부담. ASM 9.x에서 10.x로 가는 사이 깨진 코드가 한둘이 아니다. JDK가 새 instruction을 추가하면 ASM이 follow-up을 해야 하고, 그 사이 모든 ASM 의존 라이브러리가 같이 멈춘다.

#### JEP 484 — 1급 API의 도입

| JEP | Java | 단계 |
|---|---|---|
| 457 | 22 | Class-File API (Preview) |
| 466 | 23 | Class-File API (Second Preview) |
| **484** | **24** | **Class-File API (Standard)** |

3년 만에 표준이 됐다. 모듈은 `java.lang.classfile` — `jdk.internal`이 아니라 *공식 java 네임스페이스 안*이다. 이 자리 자체가 의미한다. 바이트코드 조작이 더 이상 부족 비밀이 아니라 *언어 플랫폼의 일부*가 됐다는 선언.

기본 모양을 한 번 보자. "Hello"를 출력하는 클래스를 바이트코드로 생성하는 코드.

```java
import java.lang.classfile.*;
import java.lang.constant.*;
import static java.lang.constant.ConstantDescs.*;

byte[] bytes = ClassFile.of().build(
    ClassDesc.of("Hello"),
    cb -> cb.withFlags(ClassFile.ACC_PUBLIC)
        .withMethodBody("main",
            MethodTypeDesc.of(CD_void, CD_String.arrayType()),
            ClassFile.ACC_PUBLIC | ClassFile.ACC_STATIC,
            mb -> mb.getstatic(ClassDesc.of("java.lang.System"), "out",
                               ClassDesc.of("java.io.PrintStream"))
                    .ldc("Hello")
                    .invokevirtual(ClassDesc.of("java.io.PrintStream"), "println",
                                   MethodTypeDesc.of(CD_void, CD_String))
                    .return_())
);
```

ASM의 visitor 패턴이 *builder 패턴*으로 바뀌었다. `ClassFile.of().build(name, classBuilder -> ...)`가 시작점이고, 그 안에서 method를 추가하고, 그 안에서 instruction을 람다로 적는다. `ldc("Hello")`, `invokevirtual(...)`처럼 instruction이 *그 자체로 메서드 호출*이다. `ClassDesc`, `MethodTypeDesc`는 Java 12에서 들어온 `java.lang.constant` 패키지의 nominal descriptor — symbolic하게 클래스와 메서드를 가리키는 표준 표현.

ASM의 `ClassVisitor`, `MethodVisitor`, `visitMethodInsn(INVOKEVIRTUAL, ...)` 같은 모양과 비교가 되는가? *훨씬 자바스럽다*. 람다와 메서드 체이닝으로 자연스럽게 풀린다. *fluent*하다.

#### 더 중요한 약속 — JDK와 함께 진화한다

API 모양보다 더 중요한 변화가 있다. *Class-File API는 JDK 안에 산다*. 새 instruction이 추가되면 같은 릴리스에서 API가 자동으로 따라온다. ASM이 6개월씩 지각하는 일이 없다. permits, sealed, record component, varhandle — JDK가 새 class file feature를 추가할 때 Class-File API는 *그 자리에서* 지원한다.

이 약속이 Spring AOT·Hibernate·Lombok 같은 라이브러리들에 던지는 신호는 크다. ASM 의존을 점진적으로 걷어낼 수 있다는 뜻이다. 새 JDK 릴리스마다 깨지는 일이 줄어든다는 뜻이다. *플랫폼 위에서* 바이트코드를 다룰 수 있다는 뜻이다.

#### 예제 — ASM에서 Class-File API로

간단한 변환 예제. 모든 메서드에 진입 시 `System.out.println`을 끼워 넣는 instrumentation.

**ASM 시대 (개요만)**

```java
ClassReader reader = new ClassReader(originalBytes);
ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_FRAMES);
ClassVisitor visitor = new ClassVisitor(Opcodes.ASM9, writer) {
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc,
                                     String sig, String[] exc) {
        MethodVisitor mv = super.visitMethod(access, name, desc, sig, exc);
        return new MethodVisitor(Opcodes.ASM9, mv) {
            @Override
            public void visitCode() {
                mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
                mv.visitLdcInsn("entering " + name);
                mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println",
                                   "(Ljava/lang/String;)V", false);
                super.visitCode();
            }
        };
    }
};
reader.accept(visitor, 0);
byte[] result = writer.toByteArray();
```

`visit*` 메서드 다섯 개, internal name(`java/lang/System`), descriptor 문자열(`(Ljava/lang/String;)V`) — 모두 *낮은 층위*의 표현이다.

**Class-File API 시대**

```java
ClassFile cf = ClassFile.of();
ClassModel original = cf.parse(originalBytes);
byte[] result = cf.transform(original, ClassTransform.transformingMethodBodies(
    (codeBuilder, codeElement) -> {
        // 메서드 시작 시점에 println 삽입
        // (정확한 위치 분기는 첫 instruction 여부로 판단)
        codeBuilder.with(codeElement);
    }));
```

코드 분량이 줄어드는 건 부차적인 효과다. *진짜 차이*는 internal name이 아니라 `ClassDesc.of("java.lang.System")`을 쓴다는 것, descriptor 문자열이 아니라 `MethodTypeDesc`를 쓴다는 것이다. *자바의 정상 표현*으로 바이트코드를 다룬다.

Spring AOT가 받는 영향은 크다. Spring 6의 빌드 타임 BeanFactory 사전 계산은 결국 *바이트코드 생성*이다. Class-File API가 들어오면서 그 코드가 더 깔끔해지고, 새 JDK 릴리스마다 ASM upgrade에 발목 잡히는 일이 줄어든다. Hibernate의 lazy proxy 생성, Lombok의 컴파일 타임 변환 — 모두 같은 흐름이다. *11년 묵은 비밀이 표면으로 올라오고 있다*.

### §18.4 Project Panama의 야망 — 그리고 그 너머

세 절을 다 지나왔다. 한 번 멈춰 서서 *왜 이 셋이 한 장에 모였는지* 짚어보자.

**Project Panama**의 깃발 아래에 있다. Panama의 사명은 단순하다 — *자바와 native ecosystem 사이의 경계를 더 얇게 만들자*. JNI라는 두꺼운 벽을 얇은 막으로 바꾸자. FFM은 그 벽 자체를 허물었다. Vector API는 native CPU의 SIMD 명령을 *자바 코드로* 표현할 수 있게 했다. Class-File API는 JVM의 바이트코드를 *플랫폼의 일급 추상*으로 끌어올렸다. 셋 모두 "자바는 더 이상 native와 *분리된 섬*이 아니다"라는 같은 선언을 한다.

그 너머에는 무엇이 있는가? 22장에서 자세히 다루겠지만, 지도만 펼쳐 보자.

- **GPU 호출.** FFM + Vector API의 조합으로 CUDA·OpenCL·Metal을 자바에서 부르는 시도가 가능해진다. TornadoVM 같은 프로젝트가 그 길을 일찍 걷고 있다.
- **DPDK·io_uring.** 고성능 네트워킹 라이브러리를 자바가 직접 다룰 수 있다. JNI의 비용 없이.
- **ML inference.** ONNX Runtime, TensorRT 같은 ML 런타임을 자바에서 호출하면서, Vector API로 pre/post-processing을 같은 JVM에서 처리. *Java가 ML 추론 서버의 일급 후보가 된다*.
- **Cryptography.** libsodium·OpenSSL 같은 검증된 C 라이브러리를 직접. JCE provider의 무거운 추상 없이.

이 미래는 *이미 일부 도착해 있다*. Java 22 이상의 production 코드베이스에서 FFM은 정말로 JNI를 대체하고 있고, Vector API는 incubator임에도 ML 워크로드에서 진지하게 채택되고 있다. Class-File API는 Spring 7, Hibernate 7의 빌드 파이프라인을 새로 그리고 있다.

**Spring 맥락에서 정리하자.** FFM은 *암호화 라이브러리 호출*에서, Vector API는 *이미지 처리·ML 추론 마이크로서비스*에서, Class-File API는 *Spring AOT의 빌드 타임 코드 생성*에서 각자 자리를 잡는다. 셋 모두 *일반 비즈니스 로직*에는 직접 닿지 않는다. 그러나 *플랫폼 라이브러리*가 이 셋 위에서 다시 짜이면서, 그 위의 모든 Spring 앱이 *간접적으로* 영향을 받는다. JNI 의존 라이브러리가 FFM으로 갈아끼워지면 우리 컨테이너의 패키징이 단순해지고, Spring AOT가 Class-File API 위에서 빨라지면 우리 앱의 startup이 빨라진다. *우리가 직접 손대지 않아도, 발 아래의 흙이 바뀌고 있다*.

JNI `*.h` 추출에 하루를 쓰던 그날에서 11년이 흘렀다. 그 하루는 이제 5분이다. 이게 사실이라는 걸 우리가 받아들이는 데에는 시간이 좀 더 필요할지도 모른다. 그러나 *받아들이는 편이 낫다*. 다음 native 통합을 짤 때는 한 번 멈춰 서서, JNI 대신 FFM을 검토해보자. SIMD가 필요한 hot path를 만나면, JNI 우회 대신 Vector API를 살펴보자. 바이트코드 변환을 짜야 한다면, ASM 의존을 새로 들이기 전에 Class-File API를 먼저 펴 보자.

다음 장에서는 *시작 시간*의 영역으로 넘어간다. AOT, CDS, Leyden, Compact Object Headers — 자바가 GraalVM 없이도 빠른 startup을 손에 쥐는 새 풍경이다. 함께 가 보자.

---

## 19장. AOT · Leyden · Compact Object Headers — 시작 시간과 메모리의 새 풍경

새벽 두 시, AWS Lambda 알람이 울린다. p99 콜드 스타트가 8초를 찍고 SLA를 깼다는 통보다. PayBridge의 결제 검증 Lambda는 평소 200ms에 처리되던 일이라, 8초는 그냥 *사고*다. 우리는 익숙한 절차로 들어간다. 메모리를 1.5GB에서 3GB로 올려보고, Provisioned Concurrency를 켜고, JVM 옵션을 만지작거린다. 그러다 누군가 회의에서 한 마디 꺼낸다. "이쯤 되면 GraalVM 네이티브 이미지로 가야 하는 거 아닙니까?" 모두 잠시 말이 없다. 네이티브 이미지로 가면 Reflection 메타데이터를 한참 정리해야 하고, Hibernate proxy도 손봐야 하고, 그 검증을 누가 4주 안에 끝낼지 아무도 자신하지 못한다.

콜드 스타트, 정말 GraalVM만 답일까?

이 장은 그 질문에서 출발한다. *GraalVM 없이도 빠른 자바가 가능한가*. 결론부터 말하면, 가능해지는 중이다. AppCDS에서 Dynamic CDS로, 다시 JEP 483 AOT Class Loading & Linking으로, 그리고 Project Leyden의 더 큰 그림으로 — OpenJDK는 콜드 스타트 문제를 자기 영역 안에서 풀어내려 한다. 거기에 Java 25에서 도착한 Compact Object Headers가 메모리 풍경까지 바꾼다. JVM을 *떠나지 않고도* 시작 시간과 메모리를 동시에 개선할 수 있게 됐다는 뜻이다. 한 단계씩 따라가 보자.

### CDS의 십 년: AppCDS에서 Dynamic CDS로

먼저 잘못된 통념부터 정리하자. *Java의 콜드 스타트는 JIT 컴파일 때문에 느리다*는 말은 절반만 맞다. 실제로 JVM이 시작될 때 가장 오래 걸리는 일 중 하나는 *클래스 로딩*이다. `java.base`만 해도 수천 개의 클래스가 있고, Spring Boot 앱은 거기에 다시 수만 개의 클래스를 더 얹는다. 클래스 파일을 디스크에서 읽고, 파싱하고, 검증하고, 메타데이터를 메타스페이스에 올리는 그 과정이 매 실행마다 반복된다. 같은 클래스를 매번 다시 읽고 매번 다시 파싱하는 일 — 곰곰이 따져보면 *번거롭다*.

Class-Data Sharing(CDS)은 이 번거로움에 처음 손을 댄 도구다. 시작은 오래됐다. Java 5에서 부트클래스로더의 일부 클래스를 미리 메모리에 매핑해두던 기능이 그 뿌리다. 그러나 그건 JDK 내부에 박힌 클래스 한정의 좁은 기능이었다. 우리 애플리케이션 클래스에는 도움이 되지 않았다.

판도를 바꾼 것은 Java 10의 **JEP 310: Application Class-Data Sharing**, 흔히 AppCDS라 부르는 기능이다. 핵심 발상은 단순하다. 처음 한 번은 애플리케이션을 평소처럼 실행해 *어떤 클래스가 로드되는지* 목록을 뽑는다. 그 목록을 입력으로 다시 한 번 실행해 *클래스 메타데이터를 통째로 직렬화한 아카이브*를 만든다. 그다음부터는 JVM이 시작할 때 그 아카이브를 메모리에 mmap으로 매핑한다. 클래스 파일을 읽고 파싱하는 단계가 통째로 사라지는 것이다.

AppCDS는 효과가 분명했다. 그러나 *세 단계*로 나눠 실행해야 했다 — 클래스 목록 뽑기, 아카이브 만들기, 그리고 실제 실행. 운영팀 입장에서는 도입 비용이 만만치 않았다. CI에 단계 두 개를 끼워야 했고, 클래스 목록과 실제 실행이 어긋나면 효과가 사라졌다. 도입하는 회사보다 알면서도 미루는 회사가 더 많았던 이유다.

Java 13의 **JEP 350: Dynamic CDS Archives**가 그 마찰을 한 번에 줄였다. 한 줄로 바뀐다. `-XX:ArchiveClassesAtExit=app.jsa` 옵션을 붙여 한 번만 평소처럼 실행하면, JVM이 종료될 때 알아서 아카이브를 떨궈준다. 다음 실행부터는 `-XX:SharedArchiveFile=app.jsa`로 그 아카이브를 매핑해 띄운다. 세 단계가 두 단계로 — 그것도 자연스러운 *training run* 한 번으로 — 줄어든 것이다. Spring Boot 3.3부터 이 패턴을 공식적으로 지원한다. 컨테이너 빌드 단계에서 한 번 띄웠다 죽이는 *워밍업 실행*을 한 번 끼우는 것만으로 충분하다.

여기까지가 *클래스 메타데이터*의 캐시다. 그런데 메타데이터를 캐시했다고 해서, 클래스를 *초기화*하고 *링크*하는 비용까지 사라지는 것은 아니다. `<clinit>` 블록을 실행하고, 상수 풀을 해석하고, 메서드 디스패치 테이블을 준비하는 일은 여전히 매 실행마다 반복된다. 그 다음 카드가 필요한 자리다.

### JEP 483: AOT Class Loading & Linking — Leyden의 첫 카드

Project Leyden은 2020년 즈음부터 OpenJDK 내부에서 회자되던 *시작 시간 프로젝트*의 우산 이름이다. Mark Reinhold가 처음 제안할 때의 야망은 컸다 — *static image*, 즉 GraalVM 네이티브 이미지에 준하는 일체형 바이너리를 OpenJDK 안에서 만들겠다는 그림이었다. 그러나 OpenJDK의 일하는 방식은 야망을 한 번에 풀지 않는다. Leyden은 자신의 *premain branch*에서 콘덴서(condenser)라는 개념을 다듬으면서, *점진적으로* JEP를 끊어 본류에 흘려보내는 길을 골랐다. 그 첫 결실이 Java 24에 도착한 **JEP 483: Ahead-of-Time Class Loading & Linking**이다.

발상의 진전은 한 줄로 표현된다. *클래스 메타데이터만 캐시할 게 아니라, 로딩과 링킹까지 끝낸 상태를 캐시하자*. Dynamic CDS가 클래스의 *형태*를 저장했다면, JEP 483은 *이미 해석된 클래스*를 저장한다. 결과는 인상적이다. 비슷한 training run 한 번으로 만들어진 캐시를 매핑해 띄우면, JVM이 클래스 로딩과 링킹 단계 대부분을 건너뛴다. Spring Boot 표준 데모로 자주 인용되는 Petclinic에서 시작 시간이 36~42%까지 짧아진다는 측정이 공개돼 있다. (구체 수치는 측정 환경과 Spring Boot 버전에 따라 흔들린다.)

Java 25는 거기에 두 장을 더 얹는다. **JEP 514: Ahead-of-Time Command-Line Ergonomics**는 사용성 정리다. `-XX:AOTMode=record`로 training run을 돌리고, `-XX:AOTCacheOutput=app.aot`로 캐시를 떨구고, `-XX:AOTCache=app.aot`로 실제 실행에서 그 캐시를 쓴다는 일관된 옵션 체계를 깔았다. **JEP 515: Ahead-of-Time Method Profiling**은 한 발 더 들어간다. JIT 컴파일러가 평소 *런타임에 모으는* 메서드 호출 빈도·분기 확률 같은 프로파일 정보를 training run에서 미리 모아두면, 실제 실행에서 JIT가 그 정보를 *재사용*해 더 빠르게 핫 메서드를 최적화한다. 클래스 로딩의 차원을 넘어, *컴파일러 워밍업*의 일부까지 캐시로 이전하기 시작한 것이다.

여기까지 와도 캐시는 *코드 자체*는 담지 않는다. 컴파일된 네이티브 코드를 캐시에 박는 일 — *AOT 코드 캐시* — 은 Leyden의 premain branch에서 여전히 실험 중이고, 표준 본류에 흘러들 시점은 정해지지 않았다. 그래도 흐름은 분명하다. AppCDS가 *메타데이터*를, JEP 483이 *로딩·링킹*을, JEP 515가 *프로파일*을 캐시한다. 그 다음 단계로 *코드*와 *프록시 생성*까지 캐시되면, OpenJDK의 콜드 스타트는 GraalVM 네이티브 이미지와의 격차를 의미 있게 줄이게 될 것이다. *그날은 멀지 않다*고 Leyden 팀이 이야기한다.

### 그래서, GraalVM은 어디로 가는가

여기서 한 발 멈춰 서서 GraalVM 네이티브 이미지의 정체를 정확히 짚어두자. 막연히 "더 빠른 자바"라고 알고 도입했다가 *난감해진* 팀을 본 적이 있을 것이다.

GraalVM Native Image의 핵심 가정은 **closed-world hypothesis**다. 빌드 시점에 *모든 도달 가능한 코드*를 정적으로 알 수 있다고 가정하고, 그 정적 분석 결과를 토대로 통째로 네이티브 바이너리를 만든다. 결과물은 JVM 없이 OS 위에서 바로 도는 단일 실행 파일이다. 시작은 밀리초 단위, 메모리 풋프린트는 JVM의 일부 — 서버리스 워크로드에는 매력적이다.

그러나 closed-world의 *닫혀 있다*는 가정이 자바 생태계와 마찰을 일으킨다. 자바는 30년간 *open-world*에서 살아왔다. Reflection으로 임의의 클래스를 들춰보고, dynamic proxy로 인터페이스 구현체를 런타임에 찍어내고, ServiceLoader로 어떤 구현이 올라올지 실행 시점에야 결정한다. Spring·Hibernate·Jackson 같은 프레임워크는 이 동적 능력 위에 세워졌다. closed-world에 가두려면 *어떤 클래스가 reflection으로 접근될지, 어떤 인터페이스가 proxy 대상인지, 어떤 리소스가 로드될지*를 빌드 시점에 GraalVM에게 알려줘야 한다. 그 메타데이터를 **reachability metadata**라고 부른다. 다행히 Spring Boot 3가 빌드 타임에 이 메타데이터를 알아서 뽑아주지만, 마이너한 라이브러리를 쓰는 자리에선 우리가 직접 손으로 채워줘야 한다. 한두 번 해보면 *번거로운* 정도가 아니라 마음이 *찜찜해진다*.

게다가 동적 클래스 로딩, 임의의 바이트코드 생성, JVM 에이전트는 닫혀 있는 세계에선 원천적으로 못 쓴다. 모니터링 에이전트를 붙이려다 *어, 안 되네* 한 번 겪으면 그 기억이 오래 간다.

이쯤에서 JDK AOT(Leyden)와 GraalVM의 차이를 한 표로 정리하자.

| 축 | GraalVM Native Image | JDK AOT (Leyden) |
|---|---|---|
| 산출물 | 네이티브 실행 파일 (JVM 불필요) | JVM + AOT 캐시 (`.aot` 또는 `.jsa`) |
| 세계관 | closed-world (정적 분석) | open-world (기존 JVM과 동일) |
| Reflection·proxy | reachability metadata 필요 | 그대로 동작 |
| 빌드 시간 | 수 분 단위 (정적 분석이 무겁다) | 짧음 (training run 한 번) |
| 시작 시간 | 수십 ms 수준 | 수백 ms ~ 1초대 |
| 메모리 풋프린트 | 매우 낮음 | JVM 기본보다 약간 낮음 |
| 호환성 | 라이브러리 따라 위험 | 기존 코드 그대로 |
| 운영 도구 | JFR·JMC 일부 제한 | 그대로 사용 |

표만 봐도 어떻게 갈라야 할지 윤곽이 잡힌다. *극단의 콜드 스타트와 메모리가 최우선*이고, *라이브러리 호환성을 통제할 수 있는* 상황이면 GraalVM이 답이다. *기존 코드 그대로 두고 시작 시간을 합리적으로 줄이고 싶다*면 JDK AOT가 자연스러운 첫 카드다. 두 길은 경쟁이라기보다, *연속적인 선택지*에 가깝다. 우리는 둘 다 가질 권리가 있다.

### Spring Boot 3.3+의 CDS 통합 — training run으로 충분하다

말로만 효과를 이야기하면 와닿지 않으니, Spring Boot에서 실제로 어떻게 쓰는지 보자. Spring Boot 3.3은 *Class-Data Sharing*을 *Maven/Gradle 플러그인 한 줄*로 지원한다. 컨테이너 이미지를 빌드할 때 *워밍업 단계*가 한 번 들어간다는 차이뿐이다.

```bash
# 1) training run — 앱을 한 번 띄웠다 곧장 종료한다
java -Dspring.context.exit=onRefresh \
     -XX:ArchiveClassesAtExit=application.jsa \
     -jar app.jar

# 2) 실제 실행 — 만들어진 아카이브를 매핑해 띄운다
java -XX:SharedArchiveFile=application.jsa -jar app.jar
```

`spring.context.exit=onRefresh`는 Spring 6.1에 들어간 옵션이다. ApplicationContext가 `refresh()`까지 끝낸 순간 곧장 종료한다 — *컨트롤러는 한 번도 호출하지 않고*. 그 사이에 Spring은 BeanDefinition을 모두 로드하고 AutoConfiguration을 다 돌렸으니, 컨테이너에 자주 들어오는 클래스 목록은 이미 다 메타스페이스에 올라가 있다. JVM은 종료 직전에 그 상태를 통째로 아카이브로 떨군다. *컨테이너 이미지를 빌드하는 그 자리에서* 한 번이면 충분하다.

여기에 Spring Framework 6.1의 *Spring AOT*까지 얹으면 그림이 더 흥미로워진다. Spring AOT는 *빌드 타임에* BeanFactory의 초기화 코드를 미리 계산해 자바 코드로 생성해 둔다. 런타임의 BeanFactoryPostProcessor 단계 상당 부분이 *컴파일된 코드*로 치환된다는 의미다. Spring AOT + JDK AOT 캐시를 둘 다 켠 Petclinic 측정에서, *기본 실행 대비 startup이 4배 정도* 짧아진다는 보고가 Spring 블로그와 Piotr Minkowski의 글에 올라와 있다. (정확한 배수는 머신·버전·heap 크기에 따라 흔들리니, 우리 환경에서 직접 측정하는 편이 낫다.)

PayBridge의 Lambda로 돌아가 보자. 평소 cold start가 3.2초였다고 하면, Spring Boot 3.3의 CDS만으로 2초 안쪽으로 떨어진다. JDK 24의 JEP 483 AOT 캐시를 더하면 1.5초대. JDK 25의 JEP 515 method profiling이 합쳐지면 1초 안쪽이 시야에 들어온다. *GraalVM으로 가지 않고도* SLA를 다시 맞출 가능성이 생기는 것이다. 운영팀 입장에서는 *기존 코드 그대로* 라는 한 마디가 묵직하다.

### JEP 519: Compact Object Headers — 64비트로 줄어든 객체 머리

이번엔 시작 시간과 결이 다른 이야기다. 메모리.

자바의 모든 객체는 *헤더*를 가진다. 64비트 JVM 기준으로 평소 96~128비트, 즉 12~16바이트가 매 객체마다 붙어 다닌다. 이 헤더는 두 부분으로 나뉜다. **mark word**는 객체의 락 상태, identity hash code, GC 마크 비트 같은 메타데이터를 담는 64비트짜리 슬롯이다. **klass pointer**는 이 객체가 어떤 클래스의 인스턴스인지 가리키는 포인터로, compressed class pointer가 켜져 있으면 32비트, 아니면 64비트다.

작은 객체일수록 헤더 비율이 *부담스럽다*. `Integer` 박싱 객체 하나가 실제로 담는 데이터는 `int` 4바이트인데, 그 위에 헤더가 12~16바이트 붙는다. 캐시에 `Long`을 수십만 개 쌓아두는 워크로드, JSON 파서가 임시 객체를 양산하는 워크로드, ORM이 엔티티 그래프를 메모리에 펼치는 워크로드 — 이런 자리에선 헤더가 차지하는 비율이 만만치 않다.

Java 25의 **JEP 519: Compact Object Headers**는 이 헤더를 *64비트로 압축*한다. mark word의 자주 안 쓰는 필드를 줄이고, klass pointer를 mark word 안에 작은 인덱스로 끼워 넣는 설계다. 효과는 측정에 따라 다양하게 보고된다.

- 작은 객체가 많은 워크로드(캐시, JSON 파싱, 컬렉션 무거운 코드)에서 *힙 사용량 10~22% 감소*.
- 캐시 라인 효율이 좋아지면서 GC 압력이 줄어든다 — 같은 힙 안에 더 많은 객체가 들어가니까.
- 일부 측정에서 CPU 사용량이 *30%까지* 절감됐다는 보고가 있다. (Compact Headers 자체보다는, GC 사이클이 줄어든 부수 효과가 큰 것으로 보인다.)

켜는 방법은 단순하다.

```bash
java -XX:+UnlockExperimentalVMOptions \
     -XX:+UseCompactObjectHeaders \
     -jar app.jar
```

Java 25에서는 experimental 플래그 단계지만, Java 26~27에 기본 동작으로 승격될 가능성이 높다. 그렇다면 *지금 그냥 켜도 되는가*?

조심해야 할 자리가 있다. `Unsafe`로 객체 헤더 오프셋을 *손으로 계산*하는 라이브러리가 있다면 마음 *졸일 일*이다. 16바이트를 가정하고 코드 안에 상수가 박혀 있다면 헤더가 8바이트로 줄어든 순간 깨진다. Lucene이나 일부 고성능 직렬화 라이브러리가 이런 코드를 가졌다는 보고가 있었고, 대부분 빠르게 패치됐지만 *우리 의존성 트리에 어떤 게 있는지 한 번은 훑고 가는 편이 낫다*. JOL(Java Object Layout) 같은 도구로 실제 객체 레이아웃을 한 번 떠보면 마음이 편해진다.

또 하나, 작은 객체 비중이 낮은 워크로드 — *큰 byte 배열을 중심으로 도는* 동영상 처리나 머신러닝 추론 같은 자리 — 에서는 효과가 미미하다. 모든 워크로드를 다 살리는 마법은 아니다. *어디서 켜고 어디서 끌지*는 측정으로 결정하는 편이 낫다.

### 한 단계씩 쌓아보자 — Baseline에서 Compact Headers까지

도구가 늘어났으니 한 자리에 모아 보자. PayBridge의 결제 검증 서비스 — Spring Boot 3.3, Java 25, 평소 startup 3.2초, heap 사용량 380MB — 를 가정하고 단계별 효과를 누적해 보자. (수치는 환경에 따라 흔들리니, *비율의 감*만 잡자.)

| 단계 | 명령/옵션 | startup | heap | 비고 |
|---|---|---|---|---|
| Baseline | 평소 실행 | 3.2s | 380MB | 비교 기준 |
| + CDS | `-XX:ArchiveClassesAtExit=app.jsa` | ~2.1s | 360MB | training run 1회 |
| + JDK AOT (JEP 483) | `-XX:AOTCache=app.aot` | ~1.5s | 350MB | Java 24+ |
| + Method Profiling (JEP 515) | `-XX:AOTMode=record/use` | ~1.1s | 350MB | Java 25+ |
| + Spring AOT | `spring-aot` 플러그인 | ~0.8s | 340MB | 빌드 시간은 늘어남 |
| + Compact Headers | `-XX:+UseCompactObjectHeaders` | ~0.8s | 290MB | startup보다 heap 효과 |

표를 들여다보면 두 가지가 보인다. *startup에 가장 큰 영향을 주는 것은 CDS와 JDK AOT*다. Spring AOT를 더하면 한 번 더 떨어지지만, 빌드 시간이 길어진다는 트레이드오프가 따라온다. *heap에 가장 큰 영향을 주는 것은 Compact Headers*다. 둘은 *겹치지 않고 서로 다른 자리를 친다*. 그래서 함께 쓰는 의미가 있다.

PayBridge 팀의 결론은 이렇게 정해진다. Lambda·Cloud Run의 단명 워크로드에는 CDS + JDK AOT + Compact Headers를 *기본 세트*로 켠다. 매니페스트와 Dockerfile에 한 번 박아두면 그 다음부터는 잊고 살아도 된다. 더 극단적인 콜드 스타트가 필요한 *몇몇 핫스팟*만 GraalVM 네이티브 이미지를 검토한다. 운영팀이 길게 한숨을 돌리는 풍경이 그려진다.

### 마무리: GraalVM이 답이 아닐 자유

11년 전 자바는 *시작이 느린 언어*였다. JIT 워밍업과 무거운 클래스 로딩이 *어쩔 수 없는 자바의 운명*처럼 여겨졌다. 그 운명을 옆에서 깬 것이 GraalVM 네이티브 이미지였고, *자바는 못 한다*는 통념을 한 번 뒤집은 공로가 컸다. 그러나 모든 팀이 closed-world의 비용을 치르고 거기까지 갈 필요는 없다. OpenJDK는 자기 영역 안에서 그 비용을 점진적으로 깎아내고 있다 — AppCDS, Dynamic CDS, JEP 483, JEP 515, 그리고 Leyden이 가져올 그 다음 카드들로. 거기에 Compact Object Headers가 메모리 풍경까지 한 번 더 깎는다.

이번 장에서 기억해둘 것은 셋이다. *첫째, CDS와 JDK AOT는 한 번의 training run으로 켜진다.* 도입 비용이 GraalVM과 비교가 안 된다. *둘째, GraalVM과 JDK AOT는 경쟁이 아니라 연속적인 선택지다.* 우리의 코드와 운영 사정에 맞춰 어느 자리에 어떤 카드를 쓸지 결정하면 된다. *셋째, Compact Object Headers는 작은 객체 많은 워크로드에서 마음 편히 켤 만하다.* `Unsafe`로 헤더를 들춰보는 라이브러리만 한 번 점검해두자.

다음 장에서는 결이 다른 이야기로 넘어간다. 11년 사이 우리 손에 쥐어진 *도구들* — JShell부터 jpackage, jlink, jwebserver, jextract, JFR/JMC, 그리고 빌드 도구의 자바 호환까지 — 을 한 자리에 모아 본다. *우리 손에 있는 도구를 우리는 어디까지 알고 있는가*. 그 점검의 시간이다.

---

## 19A장. 모던 자바의 도구들 — JShell부터 jextract까지

CI 파이프라인이 Java 17을 인식 못 해 빌드가 깨졌다고 해보자.

월요일 아침이다. PayBridge의 결제 게이트웨이 서비스가 Jenkins에서 빌드 실패 알림을 보낸다. 로그를 들여다보면 `error: invalid target release: 17`이다. *어, 분명 Java 17 toolchain을 깔았는데?* 빌드 노드를 SSH로 들어가 `java -version`을 쳐보면 8이 답한다. 어떤 PATH가 어디서 가로채는지 추적하는 데 한나절이 간다. 누군가 Ansible 플레이북에서 `JAVA_HOME`을 *친절하게도* 8로 강제 세팅해 둔 자국이 발견된다. 우리는 toolchain 설정 한 줄에 *하루를 쓴 피곤함*을 안고 자리에 돌아온다.

이 풍경은 우연한 사고가 아니다. 11년 사이 자바 도구는 *조용히, 그러나 단단히* 늘어났다. JShell, jpackage, jlink, jwebserver, jextract, JFR/JMC — 각각 작은 도구 같지만 모이면 풍경이 달라진다. 빌드 도구는 자바 버전을 감지하는 방식이 두 번 바뀌었고, JUnit은 records와 sealed를 자연스럽게 안는 5세대로 진화했다. 우리 손에 있는 도구를 우리는 *어디까지* 알고 있을까?

이 장은 그 점검을 위한 자리다. 큰 진리를 펼치는 자리가 아니라, *책장에서 꺼내 펴 보는 레퍼런스*로 쓰여졌다. 도구 하나하나가 왜 들어왔는지, 어디서 어떻게 쓰면 가장 즐거운지를 차례로 보자.

### §19A.1 JShell — 자바에 도착한 REPL

자바 9가 가져온 도구 중 가장 *덜* 화제가 된 것이 JShell이다. JEP 222로 들어왔는데, 모듈 시스템(Jigsaw)의 그늘에 가려져 입에 잘 오르지 않았다. 그러나 일상 디버깅에서 JShell만큼 *손이 덜 가는* 도구가 드물다.

Python에 익숙한 사람은 REPL을 자연스럽게 여긴다. *코드 한 줄 적으면 한 줄의 결과*가 돌아오는 즉시성. 자바는 오랫동안 그게 없었다. 한 줄을 시험해보려고 `Main` 클래스에 `public static void main`을 둘러 짜고, IDE에서 컴파일하고, 실행하고 — 그 *번거로움*을 다들 한 번씩은 겪었을 것이다. JShell이 그 번거로움을 한 줄로 줄였다.

```bash
$ jshell
|  Welcome to JShell -- Version 25
|  For an introduction type: /help intro

jshell> var list = List.of(1, 2, 3, 4, 5);
list ==> [1, 2, 3, 4, 5]

jshell> list.stream().filter(n -> n % 2 == 1).toList();
$2 ==> [1, 3, 5]

jshell> import java.time.*
jshell> LocalDate.now().plusDays(30)
$3 ==> 2026-06-10
```

세미콜론은 선택이고, 결과는 자동으로 `$1`, `$2` 변수에 잡힌다. `var` 선언이 그대로 먹는다. 새로운 자바 문법을 한번 만져보고 싶을 때, *코드 짜기 전에 감을 잡고 싶을 때*, JShell만 한 도구가 없다.

Spring 개발자라면 더 흥미로운 사용처가 있다. JdbcTemplate이나 JPA 쿼리를 *즉석에서* 테스트하는 자리다. 운영 DB에 붙어 의심스러운 쿼리를 한 줄씩 시험해 보는 일이 흔한데, 매번 디버깅용 컨트롤러를 만들어 띄우는 것은 *찜찜하다*. JShell에 의존성을 통째로 클래스패스로 끼우면 그 자리에서 끝난다.

```bash
$ jshell --class-path "lib/*"

jshell> import com.paybridge.repo.*
jshell> var ds = ApplicationContextStarter.dataSource()
jshell> var jdbc = new JdbcTemplate(ds)
jshell> jdbc.queryForList("SELECT * FROM payment WHERE status = ?", "FAILED")
```

스크립트 파일로도 돌릴 수 있어, 운영 점검 절차를 `.jsh` 파일로 묶어두면 *반복 작업이 깨끗해진다*. CI에 끼워 헬스체크 용도로 쓰는 팀도 있다.

### §19A.2 jpackage — 데스크톱 자바의 부활

Java 16의 JEP 343이 도입한 jpackage는 *자바 앱을 OS 네이티브 인스톨러로 패키징*하는 도구다. macOS의 `.dmg`, Windows의 `.msi`, Linux의 `.deb`/`.rpm`까지 — 한 명령어로 빠진다.

오래된 자바 데스크톱 앱 배포가 어땠는지 잠시 떠올려보자. Java Web Start로 띄우거나, exe wrapper(Launch4j 같은)를 손으로 끼우거나, JNLP 파일을 사용자에게 설명하거나 — 한결같이 *피로한* 길이었다. 게다가 Oracle이 Java Web Start를 9에서 deprecate, 11에서 제거한 이후로는 그 길조차 막혔다. jpackage가 그 자리를 채운 것이다.

```bash
jpackage \
  --name PayBridgeAdmin \
  --input target/ \
  --main-jar admin-1.0.jar \
  --main-class com.paybridge.admin.Main \
  --type dmg \
  --runtime-image custom-jre
```

`--runtime-image`에 *jlink로 만든 슬림 JRE*를 끼우면 사용자는 자바 설치 없이 앱만 깔면 된다. 이 한 줄이 데스크톱 자바를 다시 *현실적인 선택지*로 만들었다. JavaFX·Swing 앱을 만지는 팀이라면 이미 한 번씩 만져봤을 것이다.

### §19A.3 jlink — 슬림 JRE를 만들자

jlink는 Java 9 모듈 시스템과 함께 들어왔다. 발상은 단순하다. *내가 안 쓰는 모듈은 빼고, 쓰는 모듈만 모아 작은 JRE를 만들자*.

전통적인 JRE는 200MB대다. 우리 앱이 `java.base`, `java.sql`, `java.net.http`, 그리고 약간의 logging만 쓴다면 — 나머지 198MB는 *우리에게 무의미한 무게*다. 컨테이너 이미지에 들어갈 때 이 무게가 직접 비용으로 잡힌다.

```bash
jlink \
  --module-path $JAVA_HOME/jmods \
  --add-modules java.base,java.sql,java.net.http \
  --strip-debug \
  --compress=2 \
  --no-header-files \
  --no-man-pages \
  --output custom-jre
```

이렇게 만든 JRE는 40~60MB 수준으로 떨어진다. 컨테이너 이미지 사이즈가 200MB대에서 90MB대로 줄어드는 경험은 *후련하다*. Spring Boot 컨테이너 패턴에서는 그래서 두 단계로 빌드한다. *빌드 스테이지*에서 jlink로 슬림 JRE를 만들고, *런타임 스테이지*에서 그 JRE 위에 fat jar를 얹는다. 베이스 이미지로 Alpine이나 distroless를 고르면 더 줄어든다.

물론 jlink가 만능은 아니다. *모듈로 잘 정의되지 않은 라이브러리*를 쓰면 어떤 모듈이 필요한지 찾기가 *번거롭다*. `jdeps` 명령으로 의존 모듈을 뽑아내는 절차를 한 번 익혀두면 마음이 편하다. classpath jar로만 쓰던 시절의 라이브러리는 *automatic module*로 추정돼 들어가는데, 이 추정이 *어긋날 때*가 가끔 있다. 그래도 한 번 셋업해두면 그 다음부터는 잊고 살 수 있는 도구다.

### §19A.4 jwebserver — 5초만에 띄우는 정적 서버

Java 18(JEP 408)이 가져온 `jwebserver`는 *민망할 정도로 단순한* 도구다. 현재 디렉토리를 정적으로 서빙하는 HTTP 서버를 한 줄로 띄운다.

```bash
$ cd target/classes
$ jwebserver -p 8080
Binding to loopback by default. For all interfaces use "-b 0.0.0.0" or "-b ::".
Serving /path/to/target/classes and subdirectories on 127.0.0.1 port 8080
URL http://127.0.0.1:8080/
```

Python의 `python -m http.server`를 자바가 11년 늦게 따라잡은 셈이다. 별것 아닌 도구 같지만, *별것 아니라서 자주 쓴다*. 프론트엔드 빌드 결과물을 잠깐 띄워 확인할 때, API 응답 JSON을 같은 머신의 다른 프로세스에 노출할 때, IDE 의존 없이 동료에게 *지금 이 폴더만 한 번 봐달라*고 보낼 때. 큰 도구는 아니지만, 손에 닿는 자리에 늘 있으면 좋은 도구다.

### §19A.5 jextract — C 헤더를 자바 바인딩으로

18장에서 다룬 FFM API를 손에 잡고 쓰려면 *C 함수 시그니처를 자바로 옮기는* 작업이 필요하다. 함수 하나하나를 `Linker`로 손수 묶는 일은 *번거로운* 정도가 아니라 *끔찍한 일*이 된다. 큰 헤더 파일을 가진 라이브러리(예: `libcurl`, `libsqlite3`)를 묶는다고 상상해 보자.

jextract는 그 자리를 자동화한다. C 헤더 파일을 입력으로 받아 *자바 바인딩 클래스*를 생성한다. Project Panama의 자식 도구이며, 별도 다운로드가 필요하다(JDK에 기본 동봉되지는 않는다).

```bash
jextract \
  --output src/main/java \
  --target-package com.paybridge.native.curl \
  --library curl \
  /usr/include/curl/curl.h
```

생성된 클래스에는 함수 매핑·구조체 레이아웃·상수까지 다 들어 있다. 우리는 `Curl.curl_easy_init()`처럼 *그냥 자바 함수처럼* 부르면 된다. JNI 시절에 한 라이브러리를 묶느라 며칠씩 쓰던 자리가 *몇 분*으로 줄어든 풍경 — FFM이 가진 가장 실질적인 약속이다.

### §19A.6 JFR + JMC — production-grade 프로파일링

도구 일습 중 *가장 늦게 빛을 본* 것이 JFR(Java Flight Recorder)과 JMC(JDK Mission Control)다. 둘 다 원래 Oracle JRockit JDK의 상용 도구였고, Hotspot에 흡수된 뒤로도 한참 상용으로 남아 있었다. Java 11에서 JEP 328로 *오픈소스화*되면서, *production에서 부담 없이 켜 둘 수 있는* 프로파일링 도구가 자바 생태계에 들어섰다.

JFR의 특징은 *항상 켜둘 수 있다는 점*이다. 오버헤드가 1~2% 수준으로 잡혀 있어 운영 환경에 부담을 주지 않는다. JVM 내부에서 일어나는 거의 모든 이벤트 — GC, 클래스 로딩, JIT 컴파일, 락 경합, IO, 그리고 14장에서 본 `jdk.VirtualThreadPinned` — 를 *낮은 비용으로* 기록한다.

가장 흔한 사용 패턴은 두 가지다. 운영 중 의심 구간만 일정 시간 *덤프*해 분석하거나, 24시간 *연속 기록*을 굴리면서 문제가 터졌을 때 그 직전 구간을 떠내는 방식이다.

```bash
# 60초 동안 측정해 파일로 떠내기
java -XX:StartFlightRecording=duration=60s,filename=app.jfr -jar app.jar

# 운영 중인 JVM에 jcmd로 붙어서 동적으로 시작
jcmd <pid> JFR.start name=app duration=60s filename=app.jfr

# 연속 기록 (Continuous) — 의심스러울 때 dump
jcmd <pid> JFR.dump name=app filename=snapshot.jfr
```

14장에서 *virtual thread가 deadlock이 났다고 해보자*는 시나리오를 던졌었다. JFR로 *pinning을 잡는 실전 시연*을 여기서 마저 끝내보자. 평소 켜둔 JFR 기록에서 의심 구간을 dump한 다음, `jfr` CLI나 JMC GUI로 연다.

```bash
# CLI로 pinning 이벤트만 추리기
jfr print --events jdk.VirtualThreadPinned snapshot.jfr
```

출력을 보면 *어느 스택*에서 *얼마나 자주* pinning이 났는지가 줄줄이 박혀 있다. 한 줄을 잡아 풀어보면 보통 `synchronized` 블록 안에서 IO 호출이 일어나고 있는 자리다. *어, 이 자리에서 막혔구나*. 그 자리만 `ReentrantLock`으로 바꾸면 문제가 풀린다. *JFR이 없었다면 그 자리를 어떻게 찾을 뻔했는가* — 한 번 겪고 나면 JFR은 *상시 켜두는 도구*로 자리 잡는다.

JMC는 JFR 파일을 *그림으로 보는* GUI 도구다. CPU·메모리·락 경합·IO를 시간축 위에서 한눈에 본다. 처음 익히는 비용은 조금 있지만, 한 번 익히면 CLI보다 빠르게 *어디부터 들여다볼지*가 보인다. AdoptOpenJDK·Adoptium 진영에서 별도 빌드를 배포하고 있어, JDK에서 분리돼 있다는 점만 기억해두자.

### §19A.7 빌드 도구의 자바 호환

이쯤 와서 *현장에서 실제로 가장 자주 막히는 자리*를 짚어보자. 빌드 도구다.

자바 LTS가 11에서 17, 다시 21·25로 빠르게 넘어오는 동안, Maven과 Gradle은 각자의 속도로 따라왔다. 한 가지는 기억해두는 편이 낫다.

- **Maven**: 3.6.3 이상이 Java 17과 안정적으로 동작한다. 3.9.x가 Java 21·25 호환의 *권장 라인*이다.
- **Gradle**: 7.3 이상이 Java 17, 8.5 이상이 Java 21을 안정 지원한다. Java 25는 Gradle 8.10+가 안전한 선이다.

낮은 버전을 쓰던 프로젝트에 새 자바를 끼우면 *알 수 없는 컴파일 오류*가 흩어져 나오는 풍경을 한 번씩 본다. *번거롭게* 한참을 들여다본 끝에 도착하는 결론이 빌드 도구 버전이라는 사실이 *허탈하다*. 새 자바를 도입하기 전, 빌드 도구 버전부터 한 번 올리고 가는 편이 낫다.

도구 호환의 다음 매듭은 *toolchain*이다. 빌드 시스템이 *어떤 JDK로 컴파일하고 실행할지*를 명시적으로 묶는 장치다. 머신에 깔린 PATH의 JDK에 끌려가지 않고, 프로젝트가 *원하는 JDK*를 골라 쓴다.

Maven의 toolchain 설정은 `~/.m2/toolchains.xml`에 JDK 경로를 등록하고, `pom.xml`에서 `maven-toolchains-plugin`으로 묶는다.

```xml
<plugin>
  <artifactId>maven-toolchains-plugin</artifactId>
  <configuration>
    <toolchains>
      <jdk>
        <version>21</version>
        <vendor>temurin</vendor>
      </jdk>
    </toolchains>
  </configuration>
</plugin>
```

Gradle은 *toolchain 자체를 자동으로 다운로드*해 주는 길까지 열어두었다. `build.gradle`에 한 블록만 적으면 된다.

```groovy
plugins {
    id 'java'
    id 'org.gradle.toolchains.foojay-resolver-convention' version '0.8.0'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
        vendor = JvmVendorSpec.ADOPTIUM
    }
}
```

`foojay-resolver-convention` 플러그인이 *foojay Disco API*에 붙어 우리가 요청한 JDK를 알아서 받아온다. 머신마다 손으로 JDK를 깔던 시절을 깨끗하게 정리한 길이다. CI 머신에 *JDK가 안 깔려 있어도* Gradle이 알아서 받아 쓰니, Jenkins 노드 셋업이 한결 가벼워진다. 모놀리식 빌드 머신에 11과 17과 21을 동시에 굴리는 *옛 풍경*을 끝내고 싶다면, 이 한 줄이 시작점이다.

여기에 **Maven Wrapper**(`mvnw`)와 **Gradle Wrapper**(`gradlew`)를 더하면 *Maven/Gradle 자체*도 머신에 깔 필요가 없어진다. 레포에 wrapper 스크립트만 들어 있으면, 처음 실행 시 알맞은 버전의 빌드 도구를 자동으로 받는다. *어느 머신에서나 같은 빌드*가 보장되는 풍경 — 11년 전 자바 개발자가 보면 *부러워할 만한* 풍경이다.

Spring Boot의 Maven/Gradle 플러그인도 toolchain 정보를 읽어 *어떤 자바로 컴파일·패키징할지*를 자동으로 맞춰준다. 컨테이너 이미지 빌드(buildpack 또는 layered jar)도 toolchain의 자바 버전을 그대로 따른다. *플러그인 한 줄과 toolchain 블록 한 줄*이면, "이 프로젝트는 Java 21 LTS로 도는 결제 서비스다"라는 사실이 빌드 시스템에 *명시적으로* 박힌다. 옆 팀이 우리 레포를 처음 클론해 빌드하더라도 머신의 자바 버전 때문에 *난감해질 일*이 없다.

### §19A.8 JUnit 5와 Modern Java

마지막으로 테스트다. 도구가 늘어나면 *테스트하는 방법*도 같이 진화해야 한다. JUnit 5(Jupiter)는 Modern Java의 도구들과 자연스럽게 결합한다.

**records와 `@ParameterizedTest`** — records의 *값 객체* 성격이 파라미터화 테스트와 궁합이 좋다. 옛 JUnit에서 케이스를 표현하려면 `Object[][]`나 `Stream<Arguments>` 같은 흐릿한 형태에 의존해야 했는데, records는 그 흐릿함을 정리해준다.

```java
record DiscountCase(int amount, int memberLevel, int expected) {}

@ParameterizedTest
@MethodSource("discountCases")
void 할인_계산이_레벨별로_달라진다(DiscountCase tc) {
    assertThat(calculator.discount(tc.amount(), tc.memberLevel()))
        .isEqualTo(tc.expected());
}

static Stream<DiscountCase> discountCases() {
    return Stream.of(
        new DiscountCase(10_000, 1, 1_000),
        new DiscountCase(10_000, 2, 1_500),
        new DiscountCase(10_000, 3, 2_500)
    );
}
```

*어떤 입력에서 어떤 결과를 기대하는지* 한눈에 들어온다. 케이스가 늘어날수록 records의 가독성 효과가 더 커진다.

**sealed exhaustiveness 테스트** — 13장에서 `switch`의 *모든 가지를 다루었는지* 컴파일러가 검증해주는 흐름을 봤다. 그 보장은 *컴파일 타임*의 것이고, 런타임에 *모든 분기가 실제로 도달 가능한지*는 테스트로 한 번 더 잡아두는 편이 낫다. `@ParameterizedTest`에 `Stream`을 모든 permitted 서브타입으로 채워 *전부 한 번씩 통과시키는* 패턴이 유용하다.

**virtual thread를 위한 `@Timeout`** — virtual thread 코드를 테스트할 때 한 가지 *함정*이 있다. JUnit의 기본 `@Timeout`은 *같은 스레드*에서 시간을 잰다. 우리 테스트 코드가 virtual thread 안에서 막혀 있으면, 외부에서 timeout이 발화돼야 하는데 그게 안 일어날 수 있다. JUnit 5.10부터 들어온 `threadMode = SEPARATE_THREAD` 옵션이 그 자리를 풀어준다.

```java
@Test
@Timeout(value = 5, unit = TimeUnit.SECONDS, threadMode = ThreadMode.SEPARATE_THREAD)
void virtual_thread_안에서_데드락이_나도_빠져나온다() {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        // 의심스러운 코드
    }
}
```

테스트가 *무한히 매달리는* 사고를 피하는 한 줄. 14장의 *끔찍한 새벽*을 두 번 겪지 않으려면 기억해두자.

### 마무리: PayBridge의 CI 파이프라인 변천기

이번 장에서 짚은 도구들을 *한 회사의 CI 변천*으로 묶어 보자. PayBridge는 2014년에 Java 8 + Maven 3.2 + JUnit 4 + Jenkins 1.x로 시작했다. 빌드 머신에 JDK 8을 직접 깔았고, *어떤 머신*에서 빌드되느냐가 결과를 *살짝씩* 흔들었다. 2018년에 Java 11로 옮기면서 모듈 시스템에 발을 담갔고, jlink로 슬림 JRE를 만들기 시작했다. 컨테이너 이미지가 600MB에서 220MB로 줄었다.

2021년에 Java 17 LTS로 한 번 더 옮기면서, Gradle 7.3과 toolchain plugin·foojay-resolver를 도입했다. CI 머신에 JDK를 깔지 않게 됐다. *Jenkins 노드 셋업이 한 단계 줄어든 날* 운영팀이 한숨을 돌렸다. JFR을 production에 *상시 켜두기* 시작한 것도 이때다. p99 알람이 울리면 그 직전 1분의 JFR snapshot이 자동으로 슬랙으로 떨어진다.

2024년에 Java 21로 가면서 virtual thread를 도입했고, JUnit 5의 `threadMode = SEPARATE_THREAD`를 테스트 디폴트로 묶었다. 2026년 지금, Java 25를 검토하는 단계다. 19장에서 본 CDS·AOT 캐시를 컨테이너 빌드에 끼우고, Compact Object Headers를 켤지를 측정으로 결정 중이다.

이 변천을 한 줄로 묶는다면 — *도구는 자바와 함께 자란다*. 우리가 자바 11년치의 언어 진화를 따라온 만큼, 도구 진화에도 따라잡을 자격이 있다. JShell 한 번 띄워 새 문법 감을 잡고, jpackage로 사내 도구 인스톨러를 만들고, jwebserver로 빠르게 정적 파일을 내주고, JFR를 켜둬 운영을 관찰하고, toolchain plugin으로 빌드를 단단히 묶는 일 — 어느 것도 *큰 결단을 필요로 하지 않는다*. 손에 닿을 때마다 한 도구씩 익혀두자.

다음 장에서는 결을 크게 돌린다. *멈춰 있는 코드베이스를 어디서부터 손대야 하는가*. Java 8 → 17 마이그레이션의 현장 함정과 권장 순서를 정리한다. 11년의 진화가 마이그레이션이라는 한 단어에 모이는 자리다.

---

# Part IX. 마이그레이션 · 보안 · Spring 시너지

11년의 자바를 *읽는 일*과 *실제로 옮기는 일*은 다르다. 책의 모든 도구가 이 부에 와서 *한 자리에 모인다*. 마이그레이션의 함정, 보안 모델의 변화, 그리고 Spring Framework와의 시너지 — 세 장이 묶여 *현장의 자바*가 어떻게 동작하는지를 본다.

20장은 Java 8 → 17 마이그레이션의 *현장*이다. Spring Boot 3 이주 첫날 700개의 컴파일 에러가 떠오르는 그 *막막함*에서 시작해, `javax.*` → `jakarta.*` namespace 대변환, JEP 320 (Java EE 모듈 제거)의 충격, deprecated API 정리의 순서, JDK 벤더 선택(Temurin·Corretto·Liberica·Zulu)의 기준까지. *어디서부터 손을 대야 하는지* 묻는 모든 사람을 위한 장이다.

20A장은 자바 보안의 11년 변화다. SecurityManager의 *종말*(JEP 411), KEM API(Java 21, JEP 452), KDF API(Java 25, JEP 510)의 표준화, post-quantum cryptography 대비 — 자바가 *암호화와 인증의 표준*을 어떻게 다시 짜고 있는지를 본다. Spring Security 6 업그레이드 중에 KEM·KDF라는 단어를 처음 만난 그 *멀게 느껴지는 거리감*이 풀린다.

21장은 *Spring Boot 3.x × Java 21/25* — 시너지의 고유성을 본다. Spring Boot 3.0이 Java 17을 베이스라인으로 못 박은 일, Spring Boot 3.2의 `spring.threads.virtual.enabled` 한 줄이 책 14장의 도구를 *한 줄의 설정*으로 켜는 일, Spring AOT가 GraalVM 네이티브 이미지와 짝을 이루는 일, JDK CDS 통합과 Project Leyden의 AOT Cache가 *어떻게 짝이 맞는지*. 책의 모든 도구 — records, sealed, pattern matching, virtual thread, AOT — 가 한 결제 마이크로서비스에 모인다.

이 세 장이 묶여 *Modern Java를 실제로 도입한다는 일*의 무게가 분명해진다. 옮기는 일은 결국 *조직의 일*이고, *팀의 합의*이며, *옛 코드와의 마찰*이다. 책의 가장 무거운 자리이지만 동시에 가장 현실적인 자리다.

---

## 20장. Java 8 → 17 마이그레이션 — 현장의 함정과 권장 순서

Spring Boot 3로 옮기는 첫날 아침을 한번 떠올려보자. 의욕 가득한 시니어 한 명이 회사 결제 모듈의 `pom.xml`에서 `<spring-boot.version>2.5.6</spring-boot.version>`을 `3.2.0`으로 바꾸고, `<java.version>1.8</java.version>`을 `17`로 올린 다음 `mvn clean install`을 친다. 모니터에 빨간 글자가 7초간 흘러내리더니, "BUILD FAILURE — 700 errors"라는 한 줄로 마무리된다. 익숙한 클래스가 사라졌다고 한다. `javax.xml.bind.JAXBContext`도, `javax.annotation.PostConstruct`도, `javax.servlet.http.HttpServletRequest`도. 1번 에러를 클릭해 들어가니 같은 패턴이 연달아 200줄, 그 아래로 또 200줄.

이런 화면을 본 적이 한 번이라도 있다면 다음 의문을 안 가질 수가 없다. *어디서부터 손대야 할까?*

쉬워 보이는 답은 "에러 메시지를 따라 위에서 아래로 고치자"다. 이게 통할 것 같지만, 막상 해보면 끝이 보이지 않는다. JAXB 의존성을 추가하면 이번에는 `javax.activation`이 깨지고, 그걸 jakarta로 바꾸면 Spring이 못 알아본다. Mockito가 ASM 옛 버전을 끌어와 `--add-opens`를 요구하고, Lombok이 17용이 아니라며 침묵한다. 일주일을 그렇게 보내고 나면 "Java 8에 머무는 편이 낫겠다"는 결론이 머릿속에서 슬며시 자라난다.

그런데 *원래* Java 8 → 17 마이그레이션은 이렇게 가야 하는 길이 아니다. 한꺼번에 점프하지 않고, 11 → 17 → 21로 한 칸씩 끊어가야 하는 길이다. 이 장에서는 그 칸들을 하나하나 짚어보자. 각 칸에서 어떤 함정이 기다리고 있는지, 왜 그게 함정인지, 그리고 그걸 피해 가는 6단계 권장 순서가 어떻게 짜이는지를 살펴보자.

### JEP 320이 남긴 깊은 구덩이

Java 11이 LTS로 나왔을 때 가장 큰 충격은 `var`도 HttpClient도 아니었다. **JEP 320 — Java EE / CORBA 모듈의 제거**였다. JDK가 11년간 끌어안아 왔던 다음 패키지들이 *전부* 사라졌다.

- `javax.xml.bind.*` (JAXB)
- `javax.xml.ws.*` (JAX-WS)
- `javax.activation.*` (JAF)
- `javax.xml.soap.*` (SAAJ)
- `javax.annotation.*` (Common Annotations — `@PostConstruct`, `@Resource` 등)
- `org.omg.CORBA.*` (CORBA)
- `javax.transaction.*` (JTA — Java EE 측 일부)

왜 이런 일이 벌어졌을까. Java EE가 Jakarta EE로 이양되면서 이 모듈들의 *진짜 주인*이 OpenJDK 바깥으로 옮겨갔기 때문이다. Oracle은 "이건 우리가 들고 있을 게 아니다"라고 판단했고, 11에서 깔끔히 잘라냈다. 그런데 한국의 SI·금융권 코드베이스 중 적지 않은 비율이 *바로 이 모듈들*을 SOAP·구공공 API·EAI 연동에서 사용하고 있었다. 외환·국세청·관세청·금융결제원 연동 코드를 한 번이라도 만져본 사람이라면 `JAXBContext.newInstance(...)`가 어떤 코드에서 어떤 식으로 살아 있는지 몸으로 안다.

해결책 자체는 의외로 간단하다. 깨진 모듈마다 *별도의 의존성*을 `pom.xml`에 추가하면 된다.

```xml
<!-- JAXB -->
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>4.0.2</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>4.0.5</version>
</dependency>

<!-- Common Annotations (@PostConstruct, @Resource) -->
<dependency>
    <groupId>jakarta.annotation</groupId>
    <artifactId>jakarta.annotation-api</artifactId>
    <version>3.0.0</version>
</dependency>

<!-- Activation -->
<dependency>
    <groupId>jakarta.activation</groupId>
    <artifactId>jakarta.activation-api</artifactId>
    <version>2.1.3</version>
</dependency>
```

문제는 *간단한 해결*이 *간단한 작업*을 뜻하지 않는다는 점이다. 의존성을 추가하는 일은 1분이면 끝나지만, 그 직후부터 `javax.xml.bind.JAXBContext` → `jakarta.xml.bind.JAXBContext`로 import를 바꿔야 하고, `@PostConstruct`의 패키지도 바꿔야 한다. 그 작업이 코드베이스 전체에 *어디어디 흩어져 있는지*가 한눈에 안 보인다는 게 진짜 함정이다. 한 모듈을 다 고친 줄 알았는데 빌드 캐시가 꼬여 빌드만 통과하고 런타임에서 `ClassNotFoundException`이 터지기도 한다. 찜찜한 경험이다.

권장은 이렇다. IDE의 *프로젝트 전체 찾아 바꾸기*를 쓰되, 한 번에 한 패키지씩만 한다. JAXB 먼저, 그 다음 annotation, 그 다음 activation 순서로. 한 패키지를 바꿀 때마다 `mvn clean test`를 돌려서 그 단위로 검증한다. 한꺼번에 다 바꾸면 어디서 깨졌는지 추적이 안 된다. 시간이 더 걸리는 것 같지만, 결과적으로는 빠르다.

### strong encapsulation — 라이브러리의 침묵

JDK 9 이후 모듈 시스템이 들어오면서 *내부 API*에 자물쇠를 채우기 시작했다. `sun.misc.Unsafe`, `sun.reflect.*`, `com.sun.*`. JDK 16에서 JEP 396이 그 자물쇠를 *기본값으로 강제*했고, JDK 17에서 JEP 403이 강제의 마지막 못을 박았다 — "이제 `--illegal-access=permit` 옵션 자체가 사라진다."

이게 무슨 뜻인가. 우리가 직접 `sun.misc.Unsafe`를 쓸 일은 거의 없다. 그러나 우리가 *의존하는 라이브러리*가 `Unsafe`를 쓰는 일은 흔하다. 옛 Mockito가 mock 객체를 만들 때, 옛 ByteBuddy가 클래스를 바이트코드 레벨에서 합성할 때, 옛 Hibernate Proxy가 `Unsafe.allocateInstance()`로 빈 객체를 만들 때 — 전부 내부 API를 쓴다. JDK 17로 올린 직후 다음 같은 메시지를 만나면 그 신호다.

```
java.lang.reflect.InaccessibleObjectException:
  Unable to make field private final java.util.Comparator
  java.util.PriorityQueue.comparator accessible:
  module java.base does not "opens java.util" to unnamed module
```

해결은 두 갈래다. 첫째, *라이브러리를 새 버전으로 올린다.* Mockito 5.x, ByteBuddy 1.14+, Hibernate 6, ASM 9.5+. 둘째, 라이브러리가 아직 업데이트되지 않았다면 `--add-opens`로 *임시* 통로를 연다.

```bash
java --add-opens=java.base/java.util=ALL-UNNAMED \
     --add-opens=java.base/java.lang.reflect=ALL-UNNAMED \
     -jar app.jar
```

Maven Surefire 플러그인이나 Gradle test task에 이걸 넣어두면 테스트는 통과한다. 그런데 *반드시* 그건 임시 조치다. `--add-opens` 목록이 길어질수록 그건 "라이브러리 업그레이드 빚이 쌓이고 있다"는 신호로 봐야 한다. JDK 24 이후에는 `Unsafe`의 메모리 접근 메서드가 본격 deprecate됐고, FFM API(MemorySegment)로 옮겨 가는 흐름이다. 즉 이 빚은 *시간이 갈수록* 청구서가 두꺼워진다. 기억해두자.

### Nashorn의 죽음 — 작지만 아픈 흔적

JEP 372(Java 15)로 Nashorn JavaScript 엔진이 사라졌다. 평소에는 안 쓰는 기능 같지만, 의외의 곳에서 발목을 잡는다. 결제 규칙 엔진이 `ScriptEngineManager().getEngineByName("nashorn")`을 호출해 동적 룰을 평가하던 코드. 옛 Drools 일부 룰의 평가식. JIRA·Jenkins 플러그인이 사용자 입력을 JavaScript로 받아 처리하는 부분. 이런 곳들이 갑자기 `null`을 받는다 — `getEngineByName`은 엔진이 없으면 예외를 던지지 않고 `null`을 반환한다. 이 동작이 더 사악하다. 런타임에 NPE로 터지기 때문이다.

대안은 GraalVM JavaScript다. `org.graalvm.js:js`와 `org.graalvm.js:js-scriptengine` 의존성을 추가하면 `ScriptEngineManager`에서 `"js"` 또는 `"graal.js"`로 잡힌다.

```xml
<dependency>
    <groupId>org.graalvm.js</groupId>
    <artifactId>js</artifactId>
    <version>23.1.2</version>
</dependency>
<dependency>
    <groupId>org.graalvm.js</groupId>
    <artifactId>js-scriptengine</artifactId>
    <version>23.1.2</version>
</dependency>
```

호환성은 대체로 양호하지만 100%는 아니다. Nashorn의 `Java.type(...)` 같은 비표준 헬퍼는 그대로 도는데, ES5/ES6 표준에 더 엄격해진 부분이 있다. 마이그레이션 전 *기존 스크립트의 단위 테스트를 늘려두는 편*이 안전하다. 옛 룰 한 줄이 새 엔진에서 다르게 평가되는 일은 결제·세금 도메인에선 끔찍한 일이 될 수 있다.

### SecurityManager — 엔터프라이즈의 큰 함정

이 함정은 의외로 사람들이 자주 놓친다. JEP 411(Java 17)로 `SecurityManager`가 deprecated for removal로 표시됐고, JEP 486(Java 24)에서 제거됐다. 이 사실 자체는 한 줄 뉴스다. 그런데 그 한 줄이 한국 금융권·공공 코드베이스에 무엇을 의미하는지를 따져보면 작지 않다.

옛날 옛적, 자바 1.0 때부터 "신뢰할 수 없는 코드를 같은 JVM에서 격리해 돌리는 모델"이 자바의 큰 약속이었다. Applet, Java Web Start, 그리고 일부 *멀티테넌트 애플리케이션 서버*가 이 모델 위에 서 있었다. 정책 파일(`java.policy`)을 작성해 "이 코드는 이 디렉터리만 읽을 수 있다", "저 코드는 네트워크 호출 금지"를 선언했다. WebSphere, WebLogic의 옛 보안 정책, 일부 SI 프레임워크의 커스텀 `Permission` 구현이 이 위에서 돌았다.

이 모델이 *왜* 끝났을까. 한 줄로 답하면, **그 모델이 약속한 격리를 자바가 끝내 보장하지 못했다.** Sandbox escape 취약점이 너무 자주 발견됐고, JIT의 인라이닝·escape analysis·OSR이 정책 검사를 우회할 수 있는 경로를 만들었다. 클라우드 시대에 들어와 격리는 OS 컨테이너·VM·gVisor·Firecracker 같은 *바깥의 도구*가 책임지는 일이 됐다. JVM 안에서 풀 수 있는 일이 아니었다는 회고가 OpenJDK 진영의 공식 입장이다.

그래서 무슨 일이 벌어지는가. 기업 코드베이스 어딘가에 다음 같은 패턴이 살아 있다면 적색 경보다.

```java
System.setSecurityManager(new MyPolicySecurityManager());
// 또는
AccessController.doPrivileged((PrivilegedAction<X>) () -> { ... });
```

`AccessController` 자체도 deprecated, `Subject.doAs`·`Subject.callAs`까지 함께 정리되는 흐름이다. JDK 17에서는 경고만, 21까지는 동작은 하되 `-Djava.security.manager=allow`를 명시해야 한다. 24부터는 *런타임 오류*. 17 마이그레이션 시점에 이 코드가 있다면, *제거 또는 대체 설계*가 함께 가야 한다. 모니터링만 해두는 건 부족하다.

대안은 어디서 찾아야 할까. 세 갈래다.

- **Java Agent + Byte Buddy**로 instrumentation 시점에 위험 호출을 가로채는 방식. 정책 표현력은 좋지만 코드 복잡도가 오른다.
- **OS-level sandbox**(seccomp, AppArmor, gVisor, 컨테이너 capability 제한). 가장 권장되는 길.
- **모듈 시스템(JPMS)의 strong encapsulation**. 라이브러리 격리에 한해 부분적 대안. 다만 우리가 4·6장에서 다뤘듯 JPMS 자체가 본격 도입에 진입 비용이 크다.

엔터프라이즈 마이그레이션 일정을 짤 때, "SecurityManager 사용 코드의 식별과 대체"는 *반드시 별도 항목*으로 잡아두는 편이 낫다. 다른 일정 안에 묻혀 있다가 막판에 발견되면 일정 전체가 흔들린다.

### HttpClient — Java 11이 준 표준 도구

JEP 321(Java 11)로 `java.net.http.HttpClient`가 표준화됐다. Java 11 베이스라인에 도달했다면 *반드시* 알고 있어야 할 표준 도구다. 동기·비동기·HTTP/1.1·HTTP/2·WebSocket을 한 API로 다룬다.

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(5))
    .build();

HttpRequest req = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/v1/orders/42"))
    .header("Authorization", "Bearer " + token)
    .GET()
    .build();

HttpResponse<String> res = client.send(req, BodyHandlers.ofString());
```

비동기는 `sendAsync`가 `CompletableFuture<HttpResponse<T>>`를 돌려준다. Reactive 흐름이 필요하다면 그 위에 chain을 걸면 된다.

21장에서 본격적으로 다룰 일이지만, 마이그레이션 맥락에서 한 가지만 미리 짚어두자. `HttpClient`는 **virtual thread와의 시너지가 결정적**이다. 14장에서 봤듯이 virtual thread는 blocking I/O를 받아낼 때 가장 빛난다. `client.send(...)`의 동기 호출을 virtual thread 안에서 그대로 적어두면, JDK 21+ 환경에서 자동으로 unmount되고 carrier thread를 반납한다. WebClient를 쓸 때처럼 `Mono`·`Flux`를 chain할 필요가 없고, RestTemplate처럼 thread pool에 묶이지도 않는다. *동기 코드의 명료함*과 *비동기의 처리량*이 같은 자리에서 만난다.

그러니 17 마이그레이션 시점에 다음을 함께 고려하는 편이 낫다. Apache HttpClient 4.x를 쓰던 코드가 있다면, 우선 5.x로 올리거나 가능하면 `java.net.http.HttpClient`로 옮긴다. `RestTemplate`은 Spring 6에서 deprecated는 아니지만 *유지보수 모드*다. WebClient는 reactive 스택이 정말 필요할 때만. 새 코드라면 `HttpClient` + virtual thread가 가장 자연스러운 선택지다. 네 가지를 한 화면에 놓고 비교하는 일은 21장의 몫이고, 여기서는 *마이그레이션 시점의 한 줄 가이드*만 챙겨두자.

### Docker RSS의 늘어남 — 컨테이너의 작은 비명

Java 17로 올린 직후 운영팀에서 보내는 메시지가 늘어나는 신호가 하나 있다. "결제 서비스 pod이 OOMKilled로 자주 재시작합니다." Heap은 그대로 둔 채 JDK만 8 → 17로 올렸을 뿐인데, 컨테이너 메모리 limit이 빠듯해진다. 왜일까.

여러 요인이 겹친다.

- **PermGen 시대에서 Metaspace로** — 8 이전엔 PermGen이 고정 크기였다(`-XX:MaxPermSize`). 8부터는 Metaspace로 바뀌면서 native 메모리에서 자랄 수 있게 됐고, 17 시점엔 그 사이즈가 옛날보다 한 자릿수 더 크다. 클래스로딩이 많은 Spring Boot 앱에서 Metaspace가 100~200MB는 흔하다.
- **G1 + JFR + JIT C2 캐시** — G1이 default가 되면서 region 메타데이터가 native 메모리를 잡는다. JFR이 default로 켜져 있고, JIT의 C2 컴파일러가 코드 캐시(`-XX:ReservedCodeCacheSize`, 기본 240MB)를 예약한다.
- **Compressed OOPs의 변화** — heap 32GB 미만에서는 여전히 켜지지만, 옛 JVM과 약간 다른 패턴으로 정렬한다. CleverTap 블로그가 이 부분을 자세히 기록했다.
- **NIO direct buffer·Netty native** — Spring WebFlux나 Netty 기반 클라이언트가 쓰는 direct memory가 누적된다.

이 모두를 합치면 컨테이너 RSS는 *heap의 두 배*에 가까워진다. 4GB heap을 쓰는 앱이 8GB 컨테이너 limit에서 OOMKilled를 만난다. 옛 8 시절엔 6GB로도 충분했던 같은 앱이.

대처는 두 단계다. 첫째, *측정*. `jcmd <pid> VM.native_memory summary`로 native memory breakdown을 본다. 둘째, *limit 조정과 옵션 정리*. 컨테이너 limit을 heap의 1.7~2.0배로 잡고, `-XX:MaxMetaspaceSize`로 Metaspace 상한을 명시한다. `-XX:MaxDirectMemorySize`도 명시. Spring Boot 3.4의 *Container Awareness 개선*이 자동 계산을 돕긴 하지만, 기본값을 그대로 믿기보다는 한 번 측정해보고 결정하는 편이 안전하다.

### javax → jakarta — Spring Boot 3의 큰 산

Spring Boot 2.7 → 3.0이 들고 온 가장 큰 깨짐은 코드 한 줄로 요약된다. **`javax.*` → `jakarta.*`.** Java EE의 패키지 이름이 Jakarta EE로 *완전 이양*되면서 Spring 6도 이 전환을 그대로 받아들였다.

영향 범위가 작지 않다.

| 옛 패키지 | 새 패키지 |
|---|---|
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.transaction.*` (JTA) | `jakarta.transaction.*` |
| `javax.inject.*` | `jakarta.inject.*` |
| `javax.annotation.*` | `jakarta.annotation.*` |
| `javax.ws.rs.*` (JAX-RS) | `jakarta.ws.rs.*` |
| `javax.mail.*` | `jakarta.mail.*` |

엔티티 한 줄을 보자.

```java
// Before (Spring Boot 2.x, javax)
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;

@Entity
public class Order {
    @Id private Long id;
    @NotNull private String customerId;
}

// After (Spring Boot 3.x, jakarta)
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotNull;

@Entity
public class Order {
    @Id private Long id;
    @NotNull private String customerId;
}
```

import 한 줄씩 손으로 바꿀 일은 아니다. 자동 변환 도구가 잘 갖춰져 있다.

- **OpenRewrite**의 `org.openrewrite.java.migrate.JavaxToJakarta` recipe — Maven·Gradle 양쪽에서 한 줄로 적용된다.
- **Spring Boot Migrator**(`spring-boot-migrator`) — Spring 팀이 직접 만든 도구. 2.7 → 3.x 전환의 전반을 자동화한다.
- **IntelliJ의 *Migrate Java EE to Jakarta EE*** — Ultimate에 내장.

OpenRewrite를 한번 보자. Maven plugin으로 실행하면 다음 한 줄이다.

```bash
mvn org.openrewrite.maven:rewrite-maven-plugin:run \
    -Drewrite.activeRecipes=org.openrewrite.java.migrate.JavaxToJakarta \
    -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-migrate-java:RELEASE
```

수만 라인의 import가 한 번에 바뀐다. 단 *완전 자동*은 아니다. 다음 같은 곳은 수동 검토가 필요하다.

- 문자열 안에 `"javax.persistence."`처럼 패키지 이름이 적힌 부분(쿼리 hint, custom annotation processor 등).
- 외부 라이브러리가 아직 javax-only인 경우 — Hibernate 5는 javax, Hibernate 6은 jakarta. 두 세계가 같은 클래스패스에 있으면 충돌한다.
- 톰캣 9(javax.servlet)와 톰캣 10/11(jakarta.servlet)은 서로 다른 namespace를 쓴다. 같이 깔리면 모호한 오류가 난다.

이 산을 넘었다면 마이그레이션의 가장 큰 봉우리를 넘은 셈이다.

### 권장 순서 6단계 — 한 칸씩 끊어가기

위의 함정들을 다 안다면, 이제 *어떤 순서*로 밟는 게 가장 사고가 적은가를 정해야 한다. 경험적으로 자리잡힌 길은 다음 6단계다.

**1단계. JDK만 11으로, 코드는 그대로.**
`<java.version>1.8</java.version>` → `11`. Spring Boot도, 라이브러리 버전도 그대로. 빌드만 성공시킨다. 여기서 깨지는 것들이 *JDK 11의 큰 변화* 자체에 대한 노출이다. JEP 320 흔적, strong encapsulation 경고, 옛 `--add-opens` 필요 라이브러리. 이 단계에서 깨진 부분을 다 고친다. *Spring Boot 버전은 손대지 않는다.* 두 변수를 동시에 움직이면 어느 쪽에서 깨졌는지 추적이 안 된다.

**2단계. JDK 17으로, 여전히 Spring Boot 2.7.**
17의 변화는 11에 비하면 작다. records·sealed·pattern이 표준화됐을 뿐 *기존 코드*를 강제로 깨는 변화는 적다. SecurityManager 경고가 본격화된다 — 이 단계에서 코드 식별만 해두자. 17이 빌드되면 *그 자리에서 멈춘다*. 코드를 records로 리팩토링하지 않는다. 그건 다음 자리의 일이다.

**3단계. Spring Boot 2.7 → 3.x.**
드디어 javax → jakarta 전환. OpenRewrite recipe를 돌리고, 수동 검토 항목을 한 번 훑는다. Tomcat·Hibernate·Validator 버전이 함께 올라간다. *이 단계가 가장 위험하고 가장 시간이 많이 든다.* 보통 4주 일정 중 2주를 여기에 쓴다. 단계 끝에 통합 테스트를 다 통과시킨 다음, 그 시점으로 *반드시* 태그를 끊어둔다. 이후 어느 단계에서 문제가 나면 여기로 되돌아올 수 있게.

**4단계. records를 DTO부터.**
API request/response, query projection, 내부 event. *Entity는 건드리지 않는다.* JPA의 mutable·no-args 요구와 records가 안 맞는 건 11장에서 봤다. DTO부터 시작해서 점진적으로 늘려가자. Jackson은 records를 자연스럽게 지원한다. `@RequestBody record CreateOrderRequest(...)` 한 줄이면 끝난다.

**5단계. var·switch expression·pattern matching의 점진적 도입.**
새 코드에서는 적극 쓰고, 기존 코드는 *수정의 자연스러운 흐름 안에서만* 바꾼다. 9·10·12·13장에서 다룬 각 도구의 가이드라인을 팀 컨벤션으로 적어 둔다. 한꺼번에 코드베이스 전체를 갈아엎는 PR은 리뷰가 안 된다. 끔찍한 일이다.

**6단계. JDK 21+ 베이스로 virtual thread.**
Spring Boot 3.2+, `spring.threads.virtual.enabled=true`. 14·15장에서 본 ThreadLocal·pinning 가이드를 다시 펼친다. 모니터링에 JFR `jdk.VirtualThreadPinned` 이벤트를 잡아두고, HikariCP·Caffeine·Apache HttpClient 등 *synchronized 무거운* 라이브러리 버전을 점검한다. JDK 24의 JEP 491이 pinning을 거의 없애지만, LTS 정책상 21에 머문다면 한동안은 라이브러리 audit이 필요하다.

이 6단계의 핵심 원리는 한 줄이다 — *한 번에 하나의 변수만 움직이자.* JDK 버전을 올리는 PR과 라이브러리를 올리는 PR과 코드 스타일을 바꾸는 PR을 *섞지 말자.* 섞으면 그건 마이그레이션이 아니라 도박이 된다.

### 한국 SI·금융권의 회고담

이 6단계를 정직하게 밟는 일이 *얼마나 어려운가*는 한국 SI·금융권 현장에서 자주 나오는 회고에서 잘 드러난다. 일반화된 한 토막을 들여다보자.

한 카드사의 핵심 채널 시스템이 Java 8 + Spring Boot 1.5 + 옛 Tomcat 8.5에서 출발했다. 시스템 자체는 7년간 안정적으로 돌았다. 그런데 2023년 보안 감사에서 "지원 종료된 JDK·프레임워크" 항목이 적색으로 잡혔고, 1년 안에 17까지 올리라는 지시가 떨어졌다. 첫 시도는 *한 번에 17로 점프*였다. SI 외주가 들어와 6주를 들였는데, 결국 통합테스트의 30%가 깨진 채로 일정을 못 맞췄다. 실패의 원인을 회고할 때 빠지지 않고 나오는 표현이 이런 것들이다.

- "JAXB·JAX-WS 의존성을 별도로 분리하는 작업이 *각 모듈 담당자마다 다른 방식*으로 풀려서 결과적으로 중복 의존성이 늘었다."
- "내부 EAI 어댑터가 `sun.reflect.Reflection`을 직접 호출하는 줄을 *아무도 몰랐다.* 운영 트래픽이 들어오기 전까지 못 잡아냈다."
- "도커 메모리를 옛날 기준으로 잡았다가 새벽에 OOMKilled가 연쇄로 일어났다. 결제 시간대 중간에."
- "SecurityManager 정책 파일이 옛 코드 어딘가에서 여전히 살아 있는 줄 *나중에야* 발견했다."

두 번째 시도는 외주 PM이 바뀌었고, 6단계 권장 순서를 그대로 따랐다. 8 → 11 → 17 → Spring Boot 3 → 코드 정리의 칸을 분기 단위로 끊어, 9개월에 마무리됐다. 시간으로는 길었지만 운영 사고는 *한 건도 없었다*. 이 회고담의 가르침은 한 줄이다 — *마이그레이션은 단번에 점프하는 일이 아니라, 한 칸씩 끊어가는 일이다.*

글로벌 사례도 결을 같이한다. CleverTap이 정리한 "Pitfalls When Upgrading from Java 8 to Java 17"이 Docker RSS·G1 메모리·Mockito 버전 함정을 자세히 적었고, Aviator의 "Java Version Upgrade" 글이 비슷한 8 → 17 여정을 다뤘다. Systematic의 "Java Migration Journey from Java 8 to Java 17"은 *한 칸씩 끊어 가는 전략*을 명시적으로 권장한다. 어느 한 사례를 베껴 따라가는 일은 답이 아니다. *모든 사례가 같은 가르침을 반복한다는 사실*이 답이다.

### PayBridge의 4주 마이그레이션 일정

1장에서 우리는 PayBridge라는 가상 결제사를 만났다. 결제 모듈 한 줄을 11년 전 Java 8로 시작해서, 지금은 17 베이스라인에 머물러 있다. 이 회사가 *향후 1년 안에* Java 21로 옮기겠다고 결정했다고 해보자. 6단계 권장 순서를 4주 일정으로 어떻게 짤 수 있을까. 일반화된 일정을 한번 펼쳐보자.

**Week 1 — 측정과 식별.**

월요일. 빌드만 17로 올리는 *spike PR*을 만든다. 깨지는 곳을 그라운드 트루스로 기록한다. 화요일~목요일. 다음을 식별한다.

- `sun.*`, `com.sun.*` 직접 호출 코드.
- `SecurityManager`·`AccessController.doPrivileged` 사용처.
- Nashorn `ScriptEngineManager` 호출처.
- Apache HttpClient 4.x·Mockito 3.x·ByteBuddy 1.10 미만·Lombok 1.18.22 미만.
- JAXB·JAX-WS·`@PostConstruct`·`javax.transaction` 사용처.

금요일. 결과를 *마이그레이션 부채 리포트*로 정리해 팀 전체에 공유한다. 이 리포트가 이후 3주의 *작업 백로그*가 된다.

**Week 2 — 의존성 정리.**

월·화요일. JAXB·Activation·Annotations 의존성을 jakarta 패키지로 추가하고, import를 단계적으로 바꾼다. 한 패키지 단위로 PR을 끊는다. 수요일. Mockito 5.x, ByteBuddy 1.14+, Lombok 최신, Apache HttpClient 5.x로 일제히 올린다. 테스트가 깨진 곳을 모듈별로 분담. 목·금요일. 빌드와 모든 테스트가 통과하는 *그린* 상태를 만든다. 이 시점에 `spring-boot.version`은 아직 2.7.x.

**Week 3 — Spring Boot 3 전환.**

월요일. OpenRewrite recipe로 javax → jakarta 일괄 변환. 변환 후 빌드. 화·수·목요일. 톰캣 10·Hibernate 6·Validator 3.x로의 자연스러운 업그레이드. 빌드 깨짐, 통합테스트 깨짐의 대부분이 여기서 나온다. 한 항목씩 *짧은 PR*로 푼다. 금요일. 통합 테스트 전 항목 통과. *반드시* 이 시점에 release candidate 태그를 단다.

**Week 4 — 코드 현대화와 운영 점검.**

월·화요일. records를 DTO에 도입. 가장 트래픽이 많은 5개 API의 request/response부터. 수요일. `switch expression`·pattern matching을 *컨트롤러 분기*에 점진 적용. 도메인 핵심에는 손대지 않는다. 목요일. Docker memory limit 재설정 — `jcmd VM.native_memory summary` 측정 후 heap의 1.8배로. JFR 이벤트 수집 시작. 금요일. 단계 결과를 *staging*에 배포해 일주일 운영. 별다른 사고가 없으면 다음 주 운영 배포.

이 일정의 어디에도 *한꺼번에 다 한다*는 줄이 없다. PayBridge처럼 7년차 운영 시스템이라면 더 그렇다. 한 칸씩 끊어가는 4주가 한 번에 점프하는 6주보다 *짧고 안전하다.* 1장의 결론이 여기서 다시 만나진다 — *시간을 아끼는 길은, 시간을 아끼려 들지 않는 길이다.*

### 마무리

11년의 자바를 한 번에 따라잡는 길은 없다. 한 칸씩 끊어가는 길만 있다. JEP 320이 EE를 잘라낸 자리, strong encapsulation이 내부 API의 자물쇠를 채운 자리, Nashorn이 사라진 자리, SecurityManager가 떠나는 자리, HttpClient가 새 표준이 된 자리, javax가 jakarta가 된 자리, Docker RSS가 슬며시 늘어난 자리 — 이 자리들 하나하나를 *그 자리의 함정*으로 인지하고, *그 자리에서 해결*하자. 다른 자리의 해결이 끝나기 전에는 다음 자리로 옮기지 않는 편이 낫다.

도구는 우리 손에 있다. OpenRewrite, Spring Boot Migrator, IDE의 자동 변환, JFR과 `jcmd`. 외부의 회고담도 있다. CleverTap, Aviator, Systematic의 글들, 그리고 무엇보다 *우리 옆 팀의 회고담*. 다음 장에서는 마이그레이션의 결을 같이 가는 한 가지 주제를 따로 짚는다. 자바 보안 모델의 11년 변화, 그리고 KEM·KDF가 *우리도 모르는 사이* 우리 앱에 들어와 있다는 사실을 말이다.

---

## 20A장. 자바 보안의 11년 변화 — SecurityManager의 종말부터 KEM·KDF까지

Spring Security 6 업그레이드 중에 이런 상황이 벌어졌다고 해보자. 빌드는 통과했고 테스트도 그린이다. 그런데 회사의 결제 모듈에서 *키 파생* 로직을 새로 짜야 할 일이 생긴다. 토큰 발급 한 줄을 바꾸려고 코드를 열었더니, 보안팀이 보내준 가이드에 *KEM*과 *KDF*라는 단어가 줄줄이 적혀 있다. "JDK 25부터 표준화된 KDF API를 쓰세요. KEM은 Java 21부터 들어왔으니 그쪽이 적합합니다." 한 줄 한 줄은 분명 한국어인데, 머릿속에는 *어디서부터 따라가야 할까*라는 의문만 남는다. 찜찜하다.

보안은 평소에 우리가 잘 안 만진다. JDK가 알아서 처리해주는 영역이고, Spring Security가 그 위에서 한 번 더 감춰준다. 그런데 *어떤 사건들*이 자바의 보안 모델을 11년에 걸쳐 조용히 바꿔놓았고, 그 변화의 일부는 *마이그레이션 시점에 반드시* 우리 앞에 나타난다. 자바 보안 모델의 변화를 어디까지 알아야 할까? 한 번 짚어보자.

### SecurityManager — 30년 묵은 모델의 종말

20장에서 짧게 만났던 그 SecurityManager 얘기를 좀 더 들여다보자. 자바 1.0 때부터 자바는 한 가지 약속을 끌고 왔다. *신뢰할 수 없는 코드를 같은 JVM에서 격리해 돌릴 수 있다*는 약속. Applet, Java Web Start, 일부 멀티테넌트 앱 서버가 이 위에 서 있었고, `SecurityManager` + `AccessController` + `java.policy` 파일이 그 *정책 표현 도구*였다.

이 모델이 *왜* 끝나야 했을까. 한 줄로 답하면, **그 모델이 약속한 격리를 자바가 끝내 보장하지 못했다.** JEP 411의 회고가 솔직하다. Sandbox escape 취약점이 너무 자주 발견됐고, JIT의 인라이닝·escape analysis 같은 *수십 년 묵은 최적화 경로*가 정책 검사를 *자동으로 우회*할 수 있는 상태에 다다랐다. 더 큰 변화는 *세계의 변화*였다 — Applet은 사라졌고, 클라우드 시대에 들어와 격리는 OS 컨테이너·VM·gVisor·Firecracker 같은 *바깥의 도구*가 책임지는 일이 됐다. JEP 411(Java 17)의 deprecation과 JEP 486(Java 24)의 제거는 자바의 약속을 *포기한* 게 아니라, 그 약속이 살아 있던 *세계가 끝났음을 인정한* 일에 가깝다.

엔터프라이즈에서 `System.setSecurityManager(...)`도 `AccessController.doPrivileged(...)`도 한 줄씩 정리되어야 한다. 그 자리에 들어서는 것은 *바깥의 격리 도구*다 — Java Agent + Byte Buddy, OS 레벨 sandbox(seccomp·AppArmor·gVisor), 모듈 시스템의 strong encapsulation. 어느 길도 *JVM 안에서 한 방에 풀 수 있는 답*은 아니다. 그게 SecurityManager 종말의 가장 큰 의미다.

### JEP 452 KEM — post-quantum의 첫 단추

여기서부터는 좀 다른 결의 변화다. *사라지는 모델*이 아니라 *새로 들어오는 도구*다. JEP 452(Java 21)로 들어온 **Key Encapsulation Mechanism API**가 그것이다.

KEM이 뭔지 한 줄로 적어보자. *상대방의 공개 키*를 받아서, *공유 비밀(shared secret)*과 그 공유 비밀을 *암호화한 캡슐(encapsulation)*을 함께 만들어내는 메커니즘이다. 캡슐만 상대방에게 보내면, 상대방은 자기 비밀키로 캡슐을 열어 같은 공유 비밀을 얻는다. 이 공유 비밀은 이후 *대칭키 암호화*의 시드로 쓰인다.

```java
KEM kem = KEM.getInstance("DHKEM");
KEM.Encapsulator e = kem.newEncapsulator(publicKey);
KEM.Encapsulated enc = e.encapsulate();
SecretKey sharedSecret = enc.key();      // 공유 비밀
byte[] capsule = enc.encapsulation();    // 캡슐 (상대에게 전송)
byte[] params = enc.params();            // 추가 파라미터
```

받는 쪽:

```java
KEM.Decapsulator d = kem.newDecapsulator(privateKey);
SecretKey sharedSecret = d.decapsulate(capsule);
```

여기서 "그게 RSA 키 교환이랑 뭐가 다른가?"라는 의문이 자연스럽게 생긴다. 답이 KEM의 진짜 의미를 가른다. **KEM은 알고리즘이 아니라 *추상 계층*이다.** "DHKEM"은 한 구현이고, *PQC(post-quantum cryptography)* 알고리즘인 **CRYSTALS-Kyber**(2024년 NIST FIPS 203 표준)도 같은 `KEM` 인터페이스로 들어온다. 즉 KEM API는 *양자내성 암호로 옮겨갈 때 코드를 통째로 다시 짜지 않아도 되게 하는* 추상화 자리에 가깝다.

왜 *지금* 이 자리가 필요할까. 양자 컴퓨터가 RSA·ECC를 깨는 시점이 언제일지에 대해서는 의견이 갈리지만, "그 시점이 오면 *지금 암호화해서 저장 중인* 데이터도 미래에 복호화될 수 있다"는 *harvest now, decrypt later* 시나리오는 이미 위협 모델에 들어와 있다. 그래서 *지금부터* PQC로 점진 이양할 수 있는 *언어 레벨 추상화*가 필요했고, KEM이 그 자리를 잡았다.

평소엔 우리가 KEM을 직접 호출할 일이 거의 없다. TLS 1.3 이상의 핸드셰이크가 *그 안에서* KEM을 쓴다. 그러나 결제 토큰화·키 분배·서명 시스템처럼 *키 자체를 다루는* 코드라면 한 번쯤 알고 있어야 한다. 11년 후 우리가 양자 시대에 대비된 결제 인프라를 짤 때, KEM은 *그날의 도구*다.

### JEP 478 → 510 KDF — 키 파생의 표준화

KEM이 *공유 비밀을 만드는* 메커니즘이라면, **KDF(Key Derivation Function)**는 *그 공유 비밀에서 실제 사용할 키를 파생하는* 메커니즘이다. HKDF, PBKDF2, Argon2 같은 알고리즘들이 여기에 들어간다.

JDK 24에서 JEP 478로 preview 도입됐고, JDK 25에서 JEP 510으로 표준화됐다. 표준화된 API는 다음과 같다.

```java
KDF hkdf = KDF.getInstance("HKDF-SHA256");

HKDFParameterSpec spec = HKDFParameterSpec
    .ofExtract()
    .addIKM(sharedSecret.getEncoded())  // KEM의 결과
    .addSalt("payment-token-v1".getBytes())
    .thenExpand("session-key".getBytes(), 32);

SecretKey sessionKey = hkdf.deriveKey("AES", spec);
```

왜 이걸 자바가 *직접* 표준화해야 했을까. KDF가 *Bouncy Castle·Tink·Conscrypt* 같은 외부 라이브러리에 흩어져 있던 게 문제였다. 라이브러리마다 API가 달랐고, *알고리즘 이름 한 줄 차이*로 보안 사고가 나는 일이 종종 있었다. PBKDF2의 iteration count를 보안 기준보다 낮게 설정해놓고 라이브러리 default라 믿고 넘어가는 일, HKDF의 salt를 빈 값으로 두는 일. 자바 표준에 들어오면 API 자체가 *안전한 기본값*을 강제할 수 있다.

세 가지 알고리즘이 첫 표준으로 들어온다. **HKDF**(RFC 5869, 일반 키 파생), **PBKDF2**(RFC 8018, 패스워드 기반), **Argon2**(메모리 하드, 패스워드 해싱). 이 셋이 표준 자바 라이브러리 안에서 같은 `KDF` 인터페이스로 잡힌다는 사실 자체가 *큰 진전*이다.

`PBKDF2`나 `Argon2` 쪽이 더 익숙할 수 있다. *사용자 비밀번호*를 다루는 코드라면 거의 항상 `PBKDF2`나 `Argon2`를 거친다. Spring Security 6의 `BCryptPasswordEncoder`·`Argon2PasswordEncoder` 안쪽이 JDK 25 이후에는 *표준 KDF API*에 얹혀서 동작하도록 진화할 가능성이 크다. 기억해두자 — 우리가 직접 안 만지는 것 같지만, KDF는 *이미 우리 앱 안*에 들어와 있다.

### TLS 1.3 (Java 11)과 EdDSA (Java 15)

마이그레이션 맥락에서 두 가지 변화는 짧게라도 짚어두자.

**TLS 1.3**이 Java 11에서 표준 지원됐다. 핸드셰이크 라운드트립이 1.2의 절반으로 줄어들고(0-RTT 옵션까지), Cipher Suite가 *forward secrecy*를 강제하는 작은 집합으로 정리됐다. JVM은 자동으로 TLS 1.3을 우선 협상한다. 마이그레이션 시점에 신경 쓸 부분은 거의 없지만, *옛 SSL 검증 코드*가 1.2 가정 위에 짜여 있다면 한 번 점검할 일이 있다. 인증서 체인 검증의 일부 동작이 1.3에서 *더 엄격*해진 부분이 있다.

**JEP 339 — EdDSA(Edwards-Curve Digital Signature Algorithm)**이 Java 15에서 들어왔다. Ed25519와 Ed448. ECDSA보다 *결정론적 서명*이고, *더 빠르고*, *구현 함정이 적다*. 옛 ECDSA가 random nonce를 잘못 다루면 비밀키가 노출되는 함정이 있었던 데 비해, EdDSA는 그 함정 자체를 알고리즘 차원에서 막는다. JWT(JOSE) 서명, SSH 키, 일부 블록체인 통신에서 이미 default가 된 알고리즘이다.

```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("Ed25519");
KeyPair kp = kpg.generateKeyPair();

Signature sig = Signature.getInstance("Ed25519");
sig.initSign(kp.getPrivate());
sig.update("payment-receipt".getBytes());
byte[] signature = sig.sign();
```

JWT를 발급하는 코드라면 `RS256` 대신 `EdDSA`(Ed25519)로 이주하는 일을 *Java 15 이상 베이스라인의 자연스러운 흐름*으로 두는 편이 낫다. 토큰 사이즈가 작아지고, 검증 속도도 빨라진다.

### sealed로 토큰 상태 — 결제 토큰화 예제

이 자리에서 sealed가 *왜 보안 도메인에서 특별히 유용한가*를 한 번 짚어두자. 13장에서 sealed가 sum type으로서 *exhaustiveness*를 컴파일러 차원에서 보증한다는 점을 봤다. 보안 도메인에서는 그 보증이 *invariant 유지*로 직결된다.

결제 토큰을 모델링한다고 해보자. KEM으로 만든 공유 비밀과 KDF로 파생한 세션 키가 *Success* 분기에 함께 실린다.

```java
sealed interface AuthResult
    permits AuthResult.Success, AuthResult.Failure {

    record Success(String principal, SecretKey sessionKey, byte[] capsule)
        implements AuthResult {}
    record Failure(FailureKind kind, String reason) implements AuthResult {}

    enum FailureKind { BAD_CREDENTIALS, EXPIRED, LOCKED }
}

AuthResult authenticate(String principal, PublicKey clientKey) {
    var enc = kem.newEncapsulator(clientKey).encapsulate();
    var spec = HKDFParameterSpec.ofExtract()
        .addIKM(enc.key().getEncoded())
        .addSalt(("session-" + principal).getBytes())
        .thenExpand("payment-v1".getBytes(), 32);
    var sessionKey = kdf.deriveKey("AES", spec);
    return new AuthResult.Success(principal, sessionKey, enc.encapsulation());
}
```

호출 측에서는 sealed의 보증을 그대로 쓴다.

```java
return switch (authenticate(userId, clientKey)) {
    case Success(var p, var k, var capsule) ->
        ResponseEntity.ok(new SessionResponse(p, capsule));
    case Failure(FailureKind.EXPIRED, var reason) ->
        ResponseEntity.status(401).body("session expired");
    case Failure(var kind, var reason) ->
        ResponseEntity.status(403).body(reason);
};
```

`default`가 없다. *모든 결과 분기*가 명시적으로 처리됐음을 컴파일러가 *증명*한다. 새로운 결과 상태가 sealed에 추가되는 순간, *이 코드는 컴파일 에러를 낸다.* 즉 보안적으로 중요한 분기가 *조용히 누락되는 일*이 원천적으로 막힌다. 옛 OOP 스타일의 abstract class + visitor 패턴이 *그동안 풀려고 애썼지만 늘 실패했던* 이 문제를, sealed + pattern matching이 *언어 차원에서 보증*한다.

KEM이 *공유 비밀*을 만들고, KDF가 *세션 키*를 파생하며, sealed + records가 *결과의 모든 분기*를 컴파일 시점에 강제한다. *세 가지 변화*가 한 자리에서 만나 보안 도메인의 코드를 *읽고 검증할 수 있는 모양*으로 만든다. Spring Security 6도 이 결을 받아들이는 흐름이다. `Authentication`·`OAuth2Token` 같은 핵심 타입들이 records로, 일부 상태 분기는 sealed 위에 얹혀가는 방향으로 진화 중이다. 새 코드에서 우리가 같은 패턴을 직접 쓸 수 있다는 사실이 중요하다.

### 보안 모델의 11년을 한 줄로

자바 보안 모델의 11년 변화를 한 줄로 적으면 이렇다 — **JVM이 모든 격리를 떠맡으려던 모델에서, 표준 암호 도구를 잘 갖춰주는 모델로 옮겨왔다.** SecurityManager가 떠난 자리는 OS 컨테이너와 Java Agent가 채운다. 그 빈자리에 KEM·KDF·EdDSA·TLS 1.3 같은 *모던 암호 기본기*가 표준 라이브러리로 들어왔다. 자바는 *덜 가두려 하고, 더 잘 만들어주려는* 방향으로 움직였다.

이 변화가 마이그레이션 시점에 우리 앞에 어떻게 나타나는가는 두 갈래다. *제거되는 것들*에 대한 대응(SecurityManager·AccessController), 그리고 *새로 들어온 것들*에 대한 채택(KEM·KDF·EdDSA). 둘 다 *지금* 시작해두지 않으면 5년 뒤 더 큰 부채가 된다.

보안 API는 *우리가 안 만지는 것 같지만* 깊은 곳에서 이미 우리 앱을 떠받친다. Spring Security가, Tomcat의 TLS가, JWT 라이브러리가, JDBC 드라이버의 SSL 검증이 — 다 그 깊은 곳에 살고 있다. 깊다고 *몰라도 되는* 자리가 아니라, 깊은 만큼 *한 번은 알고 있어야 하는* 자리다.

다음 장에서는 모던 자바와 Spring Boot 3가 *서로 어떻게 맞물리는가*를 따로 묶어서 보자. 마이그레이션이 끝난 자리, 그 위에서 어떤 *Spring 고유의 패턴*이 자라나는지를 짚는 자리다.

---

## 21장. Spring Boot 3.x × Java 21/25 — 시너지의 *고유성*

한 결제 마이크로서비스에 records·sealed·virtual thread·AOT를 한 번에 넣어야 한다고 해보자.

PayBridge의 결제 게이트웨이 한 조각을 떠올려 보자. 가맹점이 보내는 결제 요청을 받아 사기 탐지 시스템에 묻고, 카드사 어댑터에 라우팅하고, 정산 큐에 이벤트를 흘려보내는 평범한 마이크로서비스다. 요청 DTO는 record로, 결과 타입은 `sealed PaymentResult`로 모델링했다. 컨트롤러는 외부 API 두 개를 동시에 호출해야 하니 virtual thread로 받는다. 콜드 스타트 12초가 SLA를 깎아먹어서 AOT cache도 켜야 한다. 11장에서 records의 신원을, 12·13장에서 sealed와 pattern matching을, 14장에서 virtual thread를, 19장에서 Leyden을 따로따로 살펴봤다. 이제 그 도구가 한 컨트롤러에 모인다.

그런데 책 전체에서 쌓은 도구가 한 자리에 모이는 *후련함*은 있지만, 동시에 한 가지 물음이 따라온다. *Spring과 Modern Java가 가장 잘 맞물리는 자리는 어디일까?* Spring Boot 3.x에 `spring.threads.virtual.enabled=true` 한 줄 더 넣고 끝나는 이야기가 아니다. Spring Data의 record projection, `@ConfigurationProperties` + record의 immutable config, Spring 6의 `RestClient`, 살아남은 WebFlux의 자리 — 이런 *Spring 고유의 패턴*이 따로 있다. 그 자리를 한 장에 모아보자. 단순 종합이 아니라, 다른 챕터에서는 다루지 못한 *Spring × Modern Java*만의 결합점에 집중하자.

### §21.1 Spring Data와 record projection — 세 가지 길

먼저 가장 자주 마주치는 자리부터 들여다보자. Spring Data JPA는 entity 전체가 아니라 *필요한 컬럼만 뽑는* projection을 오래전부터 지원해 왔다. 그 방식이 세 가지다.

**interface projection.**

```java
public interface PaymentSummary {
    String merchantId();
    BigDecimal amount();
    Instant capturedAt();
}

public interface PaymentRepository extends JpaRepository<Payment, Long> {
    List<PaymentSummary> findByMerchantId(String merchantId);
}
```

Spring Data가 런타임에 JDK proxy로 구현체를 만들어 준다. 가벼워 보이지만, 이 proxy는 *getter 호출마다* 내부 맵에서 값을 꺼내 변환한다. nested projection을 쓰면 entity 전체를 fetch한 뒤 필드를 골라내는 일도 일어난다. 무겁다고 할 정도는 아니지만, *어떤 코드가 도는지가 잘 안 보인다*는 점이 *찜찜하다*.

**class projection (DTO projection).**

```java
public class PaymentSummaryDto {
    private final String merchantId;
    private final BigDecimal amount;
    private final Instant capturedAt;
    public PaymentSummaryDto(String merchantId, BigDecimal amount, Instant capturedAt) { /*...*/ }
    // getters, equals, hashCode, toString ...
}
```

명시적이고, 어떤 생성자가 호출되는지가 분명하다. 그러나 boilerplate가 무겁다. 그래서 Lombok `@Value`를 쓰던 시절이 있었다.

**record projection.**

```java
public record PaymentSummary(
    String merchantId,
    BigDecimal amount,
    Instant capturedAt
) {}

public interface PaymentRepository extends JpaRepository<Payment, Long> {
    List<PaymentSummary> findByMerchantId(String merchantId);
}
```

Spring Data 3.x는 record를 일급 시민으로 다룬다. canonical constructor의 시그니처를 그대로 읽어 JPQL의 `new` 구문으로 변환한다. interface projection처럼 가볍지만, *코드가 정직하다*. 어떤 생성자가 호출되는지가 한눈에 보인다. equals·hashCode·toString도 컴파일러가 정확히 만들어 준다.

세 길의 미세 차이를 표로 정리해 보자.

| 항목 | interface | class | record |
|------|-----------|-------|--------|
| 보일러플레이트 | 없음 | 무거움 | 없음 |
| 동작의 *가시성* | 낮음 (proxy) | 높음 | 높음 |
| equals/hashCode | 자동 (이름 기반) | 직접 작성 | 자동 (컴포넌트) |
| nested projection | 가능 | 가능 | 가능 (Java 16+) |
| Jackson 직렬화 | 어색함 (proxy) | 자연스러움 | 자연스러움 |
| Compile-time 검증 | 약함 | 강함 | 가장 강함 |

답이 보이는가? 신규 코드라면 *record projection이 기본이다*. interface projection은 nested 구조가 꼭 필요하거나 옛 코드와의 일관성 때문에 남길 뿐이다. record는 Spring Data의 query parser, Jackson의 직렬화, Bean Validation의 어노테이션 처리 — 이 세 곳에서 모두 *자연스러운 1급 시민*이다.

한 가지 *기억해두자*. record projection은 JPQL `new com.paybridge.PaymentSummary(p.merchantId, p.amount, p.capturedAt)`을 자동으로 만들어 주는 것이 핵심이라, *컴포넌트의 이름과 entity 필드의 이름이 일치해야* 한다. 일치하지 않으면 직접 JPQL을 적어 `new` 구문을 쓰자. 이 한 가지만 지키면, record projection이 가장 깔끔하다.

#### Spring Data AOT Repositories — 빌드 타임에 미리 만들기

여기서 한 걸음 더 나간 도구가 있다. **Spring Data AOT Repositories**다. Spring Data 3.x는 빌드 타임에 repository의 query 메서드와 metadata를 *미리 생성*한다. 런타임 reflection이 줄고, GraalVM native image와의 호환성이 올라가며, 무엇보다 컴파일러가 잘못된 메서드명을 더 빨리 잡아낸다.

```java
@Repository
public interface PaymentRepository extends JpaRepository<Payment, Long> {
    List<PaymentSummary> findByMerchantIdAndCapturedAtBetween(
        String merchantId, Instant from, Instant to);
}
```

이 메서드명을 빌드 타임에 파싱해서 JPQL 문자열·매개변수 바인딩 정보·결과 매핑 메타데이터를 자바 코드로 생성해 둔다. 런타임에는 그 생성 결과만 실행한다. 컴파일 타임 JPA 메타모델(`Payment_.merchantId`)과 함께 쓰면 *문자열 기반 query 작성의 마지막 자리까지* 코드로 옮길 수 있다.

```java
// 컴파일 타임 JPA 메타모델 활용
Specification<Payment> spec = (root, query, cb) ->
    cb.equal(root.get(Payment_.merchantId), merchantId);
```

`Payment_`는 Hibernate Annotation Processor가 빌드 타임에 생성하는 메타모델 클래스다. `Payment_.merchantId`가 *문자열이 아닌 필드 참조*라는 점이 핵심이다. 컬럼명을 잘못 적는 *난감한* 사고가 컴파일 단계에서 잡힌다. record projection + AOT repositories + 메타모델 — 이 세 도구가 한 줄로 이어지면, Spring Data의 코드가 *런타임이 아니라 컴파일러가 검증하는 코드*로 바뀐다.

### §21.2 `@ConfigurationProperties` + record — immutable config의 자리

다음으로 살펴볼 자리는 설정이다. Spring 진영에서 오랫동안 `@ConfigurationProperties`로 외부 설정을 객체에 바인딩해 왔다. 옛 패턴은 setter가 있는 mutable POJO였다. setter가 노출돼 있다는 *찜찜함*이 늘 따라왔다 — 누군가 런타임에 설정을 *바꿔버릴* 수 있다는 가능성이 늘 열려 있었다.

```java
// 옛 패턴 — mutable, setter 노출, *찜찜함*
@ConfigurationProperties("paybridge.gateway")
public class GatewayProperties {
    private String baseUrl;
    private Duration timeout;
    private int maxRetries;
    // getters & setters ...
}
```

Spring Boot 3.x에서는 record가 *기본 후보*가 된다.

```java
@ConfigurationProperties("paybridge.gateway")
public record GatewayProperties(
    String baseUrl,
    Duration timeout,
    int maxRetries
) {}
```

`@ConstructorBinding`이 Spring Boot 3에서 *자동화*됐다. 옛 버전에서는 record나 immutable 클래스에 명시적으로 어노테이션을 붙여 줘야 했지만, 이제는 record 자체가 신호다. `application.yml`의

```yaml
paybridge:
  gateway:
    base-url: https://card.example.com
    timeout: 5s
    max-retries: 3
```

가 그대로 canonical constructor에 바인딩된다. setter가 없으니 *애초에* 변경 가능성이 닫혀 있다.

#### nested record와 validation

설정이 복잡해지면 nested record로 표현한다. JSR-380 (Bean Validation) 어노테이션도 그대로 붙는다.

```java
@ConfigurationProperties("paybridge.gateway")
@Validated
public record GatewayProperties(
    @NotBlank String baseUrl,
    @NotNull Duration timeout,
    @Min(0) @Max(10) int maxRetries,
    @Valid Pool pool
) {
    public record Pool(
        @Min(1) int maxSize,
        @NotNull Duration keepAlive
    ) {}
}
```

`@Valid`가 nested record까지 검증을 흘려보낸다. 잘못된 설정값으로 부팅하다 12시간 뒤 운영에서 *터지는* 끔찍한 일을, 부팅 첫 1초에 잡아준다.

#### `@RefreshScope`와 immutable의 충돌

그러나 한 가지 짚어야 한다. **`@RefreshScope`와 record는 본질적으로 어긋난다**. `@RefreshScope`는 런타임에 설정을 다시 읽어 빈을 *교체*하는 도구다. immutable record는 *교체* 자체를 거부한다. 어떻게 해야 할까?

두 가지 길이 있다.

첫째, **빈 자체를 교체하는 패턴**. `@RefreshScope`를 record 빈에 직접 붙이고, 같은 컨테이너 안에서 *새 record 인스턴스를 만들어 갈아끼우는* 방식이다. record 자체는 변하지 않지만, 같은 이름의 빈이 가리키는 인스턴스가 바뀐다. Spring Cloud의 `@RefreshScope` 동작 그 자체다.

```java
@RefreshScope
@ConfigurationProperties("paybridge.gateway")
public record GatewayProperties(/* ... */) {}
```

이때 *주의해야 한다*. record 인스턴스를 *필드로 캐시한 빈*은 새 인스턴스를 못 본다. proxy를 통한 lazy lookup이 필요하다.

```java
@Service
@RequiredArgsConstructor
public class GatewayClient {
    private final GatewayProperties properties; // @RefreshScope proxy
    // 매 호출마다 properties.timeout()이 *현재* 값을 반환
}
```

둘째, **변경이 필요한 부분만 분리**. 대부분의 설정은 *부팅 시점에 한 번* 읽고 끝이다. 정말 런타임에 바뀌어야 하는 값(예: 사기 탐지 임계값, feature flag) 몇 개만 떼어 `@RefreshScope`로 관리하고, 나머지는 immutable record로 둔다. *모든 설정이 refresh되어야 하는 건 아니다*. 분리하는 편이 깔끔하다.

PayBridge의 경험을 빌리면, 첫 길보다 둘째 길이 *사고가 덜 난다*. 모든 설정을 refresh 대상으로 두면 어느 빈이 옛 값으로 굳었는지 추적하기가 *번거롭다*. 정말 가변이어야 할 값을 따로 분리하는 편이 좋다.

### §21.3 RestClient — 네 가지 HTTP client의 자리 정리

그 다음으로, HTTP client 이야기를 한 번 정리하자. Spring 진영에 HTTP client가 *네 개*나 있다. 처음 보는 개발자가 *난감해할* 만하다.

| 도구 | 도입 | 모델 | 자리 |
|------|------|------|------|
| `RestTemplate` | Spring 3.0 (2009) | 동기, blocking | legacy — 신규는 권장 안 함 |
| `WebClient` | Spring 5 (2017) | 비동기, reactive | reactive 스택, backpressure |
| Java 11 `HttpClient` | Java 11 (2018) | 동기/비동기 모두 | 표준 라이브러리, Spring 의존 없음 |
| `RestClient` | Spring 6.1 (2023) | 동기, fluent | **신규 동기 호출의 기본** |

Spring 측이 *왜* RestClient를 새로 만들었을까? RestTemplate은 API가 낡았고 fluent하지 않다. WebClient는 fluent하지만 reactive 타입(`Mono`·`Flux`)을 강제한다 — 단순 동기 호출에는 *과하다*. Java 11 HttpClient는 표준이지만 Spring의 `ClientHttpRequestInterceptor`, `MessageConverter`, `Observation` 같은 통합 도구를 못 쓴다. 그 사이의 빈자리를 채우려고 등장한 것이 RestClient다.

```java
// RestClient — Spring 6.1
@Configuration
public class HttpClients {
    @Bean
    RestClient cardAdapterClient(RestClient.Builder builder) {
        return builder
            .baseUrl("https://card.example.com")
            .defaultHeader("X-API-Key", "${paybridge.card.key}")
            .requestInterceptor(observationInterceptor())
            .build();
    }
}

@Service
public class CardAdapter {
    private final RestClient client;

    public AuthResult authorize(AuthRequest req) {
        return client.post()
            .uri("/authorize")
            .body(req)
            .retrieve()
            .body(AuthResult.class);
    }
}
```

fluent하고, 동기다. 코드가 한눈에 읽힌다. *예외*는 자연스럽게 위로 던져진다. stack trace가 친절하다 — 디버깅하는 새벽에 *후련함*을 느끼게 된다.

#### 언제 어느 것을 택하나

네 도구의 자리를 정리해 보자.

- **RestClient (기본)**: 동기 호출 + virtual thread. 신규 코드의 99%가 여기다.
- **WebClient**: 진짜로 reactive 스택을 쓰는 경우. backpressure가 필요한 streaming, SSE, WebSocket. 21.4에서 살펴본다.
- **Java 11 HttpClient**: Spring 의존을 피하려는 라이브러리·SDK 작성. CLI 도구. 또는 HTTP/2 push 같은 *특수* 기능.
- **RestTemplate**: 이미 쓰고 있는 옛 코드. 새 코드에는 쓰지 말자.

여기서 한 가지 흥미로운 시너지가 있다. **RestClient + virtual thread**다. RestClient는 내부적으로 blocking I/O를 한다. blocking이 *나쁜 단어*였던 시절이 있었다 — Tomcat 200 thread pool 시대였다. virtual thread 위에서는 blocking이 *cheap*하다. 200개의 동시 호출이 200ms씩 걸리는 외부 API라면, virtual thread 위의 RestClient는 *시퀀셜처럼 보이는 코드로 거의 병렬*에 가까운 처리량을 낸다.

```java
@RestController
public class PaymentController {
    private final RestClient fraudClient;
    private final RestClient cardClient;
    private final ExecutorService executor =
        Executors.newVirtualThreadPerTaskExecutor();

    @PostMapping("/payments")
    public PaymentResponse pay(@RequestBody PaymentRequest req) throws InterruptedException, ExecutionException {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var fraud = scope.fork(() ->
                fraudClient.post().uri("/check").body(req).retrieve().body(FraudResult.class));
            var auth = scope.fork(() ->
                cardClient.post().uri("/authorize").body(req).retrieve().body(AuthResult.class));
            scope.join().throwIfFailed();
            return merge(fraud.get(), auth.get());
        }
    }
}
```

코드가 *동기처럼 보인다*. 그런데 두 외부 API가 *동시에* 호출된다. Java 8 시대에 `CompletableFuture.supplyAsync`를 두 번 부르고 `thenCombine`으로 합치던 코드가 — 그 *번거롭던* 비동기 조합이 — 다섯 줄로 정직하게 표현된다. 8B장에서 살펴본 비동기 조합의 *번거로움*을, 14·16장의 도구가 정리하고, 21장의 RestClient가 마무리한다.

### §21.4 WebFlux는 *어느 자리에* 살아남는가

여기서 솔직해질 자리가 있다. virtual thread가 표준화되면서 *모든 reactive를 대체할 것*이라는 기대가 한동안 있었다. 8B장에서 reactive와 virtual thread의 대비를 본격적으로 짚었다. 그 결론을 한 줄로 회수하자면 — **virtual thread가 있어도 reactive는 살아남는다. 단 그 자리는 좁아졌다.**

그 *좁아진 자리*가 어디인가? 네 곳이다.

#### ① backpressure가 필요한 곳 — Kafka consumer fan-out

Kafka에서 100만 건/초 메시지를 consume해 외부 API로 fan-out하는 컨슈머를 떠올려 보자. 외부 API의 처리 속도가 1만 건/초라면, consumer는 자기 속도가 아니라 *외부 API의 속도에 맞춰* 흘러야 한다. 이게 backpressure다.

virtual thread로는 깔끔하지 않다. virtual thread 100만 개를 만들 수는 있지만, 외부 API가 *떠밀리는 속도*를 자연스럽게 표현할 도구가 없다. Reactor의 `Flux.flatMap(concurrency)`은 그 자리에 정확히 들어맞는다.

```java
Flux.from(kafkaPublisher)
    .flatMap(msg -> webClient.post().bodyValue(msg).retrieve().bodyToMono(Result.class),
             /* concurrency */ 32,
             /* prefetch */ 256)
    .subscribe();
```

`concurrency=32`가 한 번에 진행 중인 외부 호출 수를 제한한다. `prefetch=256`이 upstream에서 미리 받아 둘 버퍼 크기다. 두 숫자가 *떠밀림*을 자연스럽게 표현한다.

#### ② SSE (Server-Sent Events) — 긴 수명의 스트림

결제 상태 변경 알림을 가맹점 대시보드로 *밀어주는* 채널을 떠올려 보자. 한 연결이 *몇 시간* 살아 있고, 그 동안 띄엄띄엄 이벤트가 흘러간다. WebFlux의

```java
@GetMapping(value = "/payments/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<PaymentEvent> stream(@RequestParam String merchantId) {
    return eventBus.subscribe(merchantId);
}
```

는 *수만 개의 idle 연결*을 가볍게 들고 있을 수 있다. 같은 일을 virtual thread + RestClient로 한다면 — 굳이 못 할 건 없지만 *어색하다*. SSE는 *push 방향의 streaming*이라 reactive의 자연 영역이다.

#### ③ WebSocket streaming

마찬가지다. 양방향 streaming, hot/cold stream의 구분, multicast가 필요한 자리. Reactor의 `Sinks.Many`, `share()`, `replay()`가 그 자리에 그대로 들어맞는다.

#### ④ R2DBC — reactive 데이터베이스

JDBC는 blocking API다. virtual thread 위에서는 blocking이 *cheap*하니, JDBC + virtual thread로 대부분의 자리가 메워진다. 그런데 *reactive하게 fan-out된 파이프라인*의 한 곳만 JDBC라면, 그 자리가 blocking sink가 돼 backpressure를 깬다. R2DBC는 reactive 파이프라인의 *끝까지* reactive를 보장하려는 시도다.

R2DBC가 모든 자리에서 JDBC를 대체할 도구는 아니다. JPA의 ORM 기능을 누리지 못하고, query DSL도 빈약하다. 그러나 *대규모 reactive 스트림*에서 DB가 종착지라면 — 그 한 자리에서는 R2DBC가 답이다.

#### 결론 — 좁아졌지만 사라지지 않는다

네 자리를 보면 패턴이 보인다. *진짜 streaming 모델*이 필요한 자리, *떠밀림*을 명시적으로 표현해야 하는 자리, *연결의 양*이 thread보다 더 많을 수 있는 자리. 이 세 가지가 reactive의 자연 영역이다. virtual thread는 *thread-per-request*의 부활이지, *push-based streaming*의 부활이 아니다. 두 모델은 다른 문제를 푼다.

PayBridge에서도 같은 그림이 그려져 있다. 결제 API 게이트웨이(요청·응답 한 사이클)는 virtual thread + RestClient로 옮겼고, 가맹점 알림 channel과 정산 큐 fan-out은 WebFlux + R2DBC로 유지한다. *모든 코드를 한 모델로 통일하려고 애쓰지 말자*. 자리에 맞는 도구를 쓰는 편이 낫다.

### §21.5 `spring.threads.virtual.enabled=true`의 본격 활용

14장에서 한 줄로 호명만 했던 이야기를 이제 본격적으로 풀어보자.

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

Spring Boot 3.2부터 등장한 한 줄이다. 한 줄이 무엇을 바꾸나? *Tomcat의 request handler executor*를 platform thread pool에서 virtual thread per task executor로 갈아끼운다. `@Async`의 기본 executor도, `TaskExecutionAutoConfiguration`이 만드는 `taskExecutor` 빈도, 모두 virtual thread를 쓰게 된다.

#### 서블릿 컨테이너별 지원 상태

| 컨테이너 | virtual thread 지원 | 비고 |
|----------|---------------------|------|
| Tomcat 10.1+ | ✓ | Spring Boot 3.2부터 자동 |
| Jetty 12+ | ✓ | `VirtualThreadPool` 옵션 |
| Undertow | 제한적 | XNIO 워커 스레드 모델, 부분 적용 |
| Netty | N/A | event loop 모델 — virtual thread 불필요 |

Spring Boot 3.x의 기본은 Tomcat이다. 한 줄 설정으로 끝난다. Jetty로 갈아끼울 때는 `JettyVirtualThreadPool` 설정을 명시적으로 켜자.

#### JDBC 드라이버의 Loom-readiness

여기서 *반드시 짚어야 할* 부분이 있다. **JDBC 드라이버와 connection pool이 Loom-ready인가**다. 15장에서 살펴본 pinning 문제의 가장 흔한 발원지가 바로 이 두 곳이다.

| 라이브러리 | Loom-ready 버전 | 이슈 |
|-----------|-----------------|------|
| HikariCP | 5.1.0+ | 옛 버전은 `synchronized` 블록에서 pin |
| MySQL Connector/J | 8.4.0+ | 옛 버전은 socket I/O에서 pin |
| PostgreSQL JDBC | 42.7.0+ | 비교적 일찍부터 안전 |
| MariaDB Connector/J | 3.3.0+ | 신규 버전 권장 |
| Oracle JDBC | 23ai 이상 권장 | 옛 버전 호환성 부족 |

PayBridge의 *덜컥*했던 새벽이 정확히 여기서 시작됐다. HikariCP 4.x 버전이 남아 있던 인스턴스에서 virtual thread를 켜자 deadlock이 났다. JFR의 `jdk.VirtualThreadPinned` 이벤트로 진단하고, HikariCP를 5.1.0으로 올려 해결했다. *기억해두자*. virtual thread를 켤 때는 *반드시* 의존성 트리의 connection pool과 JDBC 드라이버 버전을 확인하자. Java 24의 JEP 491이 `synchronized` 블록의 pinning을 해결하지만, 21에 머무른다면 *수동으로 버전을 정렬*하는 편이 안전하다.

#### Spring Boot 3.4의 부속 도구

같이 챙겨야 할 *주변 도구*도 몇 개 있다. Spring Boot 3.4에 와서 깔끔해진 것들이다.

**SSL bundle.** SSL 설정이 여기저기 흩어져 있던 *번거로움*을 정리한 도구다.

```yaml
spring:
  ssl:
    bundle:
      pem:
        card-adapter:
          keystore:
            certificate: classpath:certs/card.crt
            private-key: classpath:certs/card.key
          truststore:
            certificate: classpath:certs/card-ca.crt
```

```java
@Bean
RestClient cardAdapterClient(RestClient.Builder builder, SslBundles bundles) {
    return builder
        .baseUrl("https://card.example.com")
        .apply(b -> b.sslBundle(bundles.getBundle("card-adapter")))
        .build();
}
```

여러 외부 API마다 다른 인증서를 쓰는 결제 시스템에서 *후련한* 도구다.

**Docker Compose support.** 로컬에서 외부 서비스(Postgres·Redis·Kafka)를 띄울 때 `compose.yml`을 자동으로 인식한다. `application.yml`의 datasource URL을 *덮어쓰지 않고도* 컨테이너 주소가 자동 주입된다.

```yaml
# compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: paybridge
```

`spring-boot-docker-compose` 의존성만 추가하면 `mvn spring-boot:run`이 알아서 compose를 띄우고 datasource를 잡아준다. 로컬 개발의 *지긋지긋한* 환경 변수 셋업이 줄어든다.

### §21.6 Observability + JFR — production 모니터링의 한 페이지

virtual thread를 켰는데 *덜컥*하는 일을 막으려면, observability를 같이 챙겨야 한다. Spring 6는 Micrometer 기반의 Observation API를 1급 시민으로 두고 있다.

```java
@RestController
@RequiredArgsConstructor
public class PaymentController {
    private final ObservationRegistry registry;
    private final CardAdapter cardAdapter;

    @PostMapping("/payments")
    public PaymentResponse pay(@RequestBody PaymentRequest req) {
        return Observation.createNotStarted("payment.authorize", registry)
            .lowCardinalityKeyValue("merchant_type", req.merchantType())
            .observe(() -> cardAdapter.authorize(req));
    }
}
```

`Observation`이 한 번에 *trace span*, *metrics*, *logs context*를 만든다. Zipkin·Jaeger 같은 trace 백엔드, Prometheus 같은 metrics 백엔드, MDC를 통한 logs context — 한 줄에 세 곳이 동시에 채워진다.

virtual thread에서 *반드시* 켜야 할 것이 하나 있다. **JFR (Java Flight Recorder)**다. `jdk.VirtualThreadPinned` 이벤트가 자동으로 수집된다.

```bash
java -XX:StartFlightRecording=filename=paybridge.jfr,duration=60s,settings=profile \
     -jar paybridge-gateway.jar
```

운영 중에도 부담이 거의 없다 (1~2% overhead). 수집된 `.jfr` 파일을 JMC(JDK Mission Control)로 열면 *어느 코드에서 pinning이 났는지* 한눈에 보인다. 15장에서 본 그 도구다.

production에서는 한 발 더 나간다. Spring Boot Actuator의 `/actuator/threaddump`로 virtual thread 덤프를 받을 수 있고, `/actuator/metrics/jvm.threads.virtual.live`로 라이브 카운트를 확인할 수 있다. *문제가 생기기 전*에 보이는 도구를 켜두는 편이 낫다.

### §21.7 결제 마이크로서비스 — 도구가 한 자리에 모이는 후련함

이제 책 전체에서 쌓은 도구를 한 컨트롤러에 모아보자. PayBridge의 `/payments/authorize` 엔드포인트다.

```java
// 도메인 모델 — records + sealed
public record PaymentRequest(
    @NotBlank String merchantId,
    @NotNull @Positive BigDecimal amount,
    @NotBlank String currency,
    @Valid CardInfo card
) {
    public record CardInfo(
        @Pattern(regexp = "\\d{13,19}") String number,
        @Pattern(regexp = "\\d{2}/\\d{2}") String expiry
    ) {}
}

public sealed interface PaymentResult permits Approved, Declined, Failed {
    record Approved(String authCode, Instant capturedAt) implements PaymentResult {}
    record Declined(String reason, String issuerMessage) implements PaymentResult {}
    record Failed(String errorCode, Throwable cause) implements PaymentResult {}
}

// 컨트롤러 — virtual thread + structured concurrency + RestClient
@RestController
@RequiredArgsConstructor
public class PaymentController {
    private final RestClient fraudClient;
    private final RestClient cardClient;
    private final PaymentRepository repository;
    private final ObservationRegistry observations;

    @PostMapping("/payments/authorize")
    public ResponseEntity<PaymentResponse> authorize(@Valid @RequestBody PaymentRequest req)
            throws InterruptedException {
        return Observation.createNotStarted("payment.authorize", observations)
            .lowCardinalityKeyValue("merchant", req.merchantId())
            .observe(() -> {
                PaymentResult result = process(req);
                return toResponse(result);
            });
    }

    private PaymentResult process(PaymentRequest req) throws InterruptedException {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var fraud = scope.fork(() ->
                fraudClient.post().uri("/check").body(req).retrieve().body(FraudResult.class));
            var auth = scope.fork(() ->
                cardClient.post().uri("/authorize").body(req).retrieve().body(AuthResult.class));
            scope.join().throwIfFailed();

            return switch (auth.get()) {
                case AuthResult.Ok(var code) when !fraud.get().suspicious() ->
                    new PaymentResult.Approved(code, Instant.now());
                case AuthResult.Ok(var __) ->
                    new PaymentResult.Declined("FRAUD_SUSPECTED", "blocked by risk engine");
                case AuthResult.Rejected(var msg) ->
                    new PaymentResult.Declined("ISSUER_REJECTED", msg);
            };
        } catch (Exception e) {
            return new PaymentResult.Failed("UPSTREAM_ERROR", e);
        }
    }

    private ResponseEntity<PaymentResponse> toResponse(PaymentResult r) {
        return switch (r) {
            case PaymentResult.Approved(var code, var at) ->
                ResponseEntity.ok(new PaymentResponse.Success(code, at));
            case PaymentResult.Declined(var reason, var msg) ->
                ResponseEntity.status(402).body(new PaymentResponse.Failure(reason, msg));
            case PaymentResult.Failed(var code, var __) ->
                ResponseEntity.status(503).body(new PaymentResponse.Failure(code, "retry"));
        };
    }
}
```

여기 모인 도구를 헤아려 보자.

- **record DTO**: 요청·응답의 신원 (11장)
- **Bean Validation**: nested record까지 검증 (21.2)
- **sealed interface `PaymentResult`**: 합 타입으로 결과 모델링 (12장)
- **pattern matching `switch`**: 결과 분기를 *exhaustive*하게 (13장)
- **virtual thread (`spring.threads.virtual.enabled=true`)**: thread-per-request 부활 (14장)
- **`StructuredTaskScope`**: 두 외부 호출의 *구조적* 병렬 (16장)
- **RestClient**: 동기 fluent HTTP (21.3)
- **Observation API**: trace + metrics + logs (21.6)

같은 컨트롤러를 *Java 8*로 적었다면 어땠을까? 80줄짜리 코드가 200줄로 늘어났을 것이다. DTO는 Lombok `@Value`나 직접 작성한 클래스로, 결과 분기는 `instanceof` 캐스트 사다리로, 두 외부 호출은 `CompletableFuture.supplyAsync` 두 번과 `thenCombine`으로 — 줄 수도 늘어나지만 *읽히는 정도*가 다르다. 같은 의도를 표현하는데 손가락 무게가 다르다.

코드를 위에서 아래로 한 번만 읽어 보자. *비즈니스 로직만 보인다*. 어떻게 thread를 다루는지, 어떻게 결과를 분기하는지, 어떻게 검증하는지 — 그 *기계적인 부분*이 언어와 프레임워크의 어휘 안으로 사라져 있다. 11년 동안 자바가 걸어온 길의 *후련한* 결말이다.

### §21.8 21에 머무를지, 25로 갈지

마지막 한 자리를 정리하자. 모든 자바 개발자가 마주하는 *판단*이다. *우리 서비스는 21에 머물러야 할까, 25로 가야 할까?*

PayBridge의 결정을 그대로 빌려 와 일반화해 보자.

| 판단 기준 | 21 (이중 LTS) | 25 (현재 LTS) |
|-----------|---------------|---------------|
| 지원 기간 | Oracle 8년 (2031) | Oracle 8년 (2033) |
| 검증 깊이 | 2년 이상 production 검증 | 갓 나옴, 검증 진행 중 |
| 라이브러리 호환 | 거의 모든 라이브러리 ✓ | 일부 옛 라이브러리 미검증 |
| Spring Boot | 3.2~3.4 모두 ✓ | 3.4+ 권장 |
| virtual thread pinning | JEP 491 *없음* — 옛 `synchronized` 주의 | JEP 491 적용 — pinning 거의 사라짐 |
| AOT cache | CDS만 (3.3+) | JEP 483/514 본격 |
| Compact Object Headers | 없음 | 있음 — heap ~10~25% 절감 |
| Stream Gatherers | 없음 | 표준 |

이 표가 결정의 *반*이다. 나머지 반은 *서비스의 성격*이다.

- **고도 안정성 우선 (금융 거래, 결제 게이트웨이)**: 21에 머무는 편이 낫다. 검증된 동작, 라이브러리 매트릭스의 *익숙함*이 안정성의 일부다.
- **신규 도구 활용 우선 (대용량 캐시 서비스, batch 정산, AI/ML inference)**: 25로 가는 편이 낫다. Compact Object Headers의 메모리 절감, AOT cache의 콜드 스타트 단축, Gatherer의 표현력이 *실제 ROI*로 돌아온다.
- **virtual thread 본격 활용**: 25 권장. JEP 491이 pinning을 거의 없앤다.
- **마이그레이션 비용 (구버전 라이브러리, 사내 빌드 인프라)**: 21 유지가 안전하다. *완벽한 LTS*는 *내 코드가 도는 LTS*다.

PayBridge는 두 갈래로 갔다. 결제 게이트웨이는 21에 머물고, 정산 배치와 사기 탐지는 25로 갔다. *서비스마다 다른 LTS를 쓰는 것*이 11년 전에는 *번거롭게* 들렸겠지만, 지금은 GitHub Actions toolchain·Docker base image·Spring Boot 의존성 매니지먼트가 모두 *서비스별 자바 버전*을 자연스럽게 다룬다. 한 LTS로 사내 표준을 강제할 이유는 옛날만큼 강하지 않다.

한국 사례를 짚어보자. 우아한형제들의 기술 블로그(`techblog.woowahan.com`)는 virtual thread 전환 측정을, 카카오페이의 기술 블로그(`tech.kakaopay.com`)는 Spring에서 virtual thread를 실제로 어떻게 켰는지를 적어 두었다. velog의 여러 개발자 글, `findstar.pe.kr` 같은 한국 개발자 블로그도 *현장의 측정값*을 공유한다. 이 글들이 공통으로 말하는 것이 하나 있다 — *직접 측정해라*. 외부 글의 수치를 그대로 우리 서비스에 옮겨 적용할 수는 없다. JFR을 켜고, JMH로 마이크로 벤치마크를 돌리고, *우리 워크로드에서* 측정한 숫자로 판단하자.

### 마무리

Spring Boot 3.x × Java 21/25의 결합점을 한 장에 모았다. *Spring 고유*의 자리만 다섯 곳을 짚었다 — Spring Data record projection + AOT repositories, `@ConfigurationProperties` + record + `@RefreshScope`, RestClient의 자리, WebFlux가 살아남는 네 영역, `spring.threads.virtual.enabled` + observability. 여기에 더해 결제 마이크로서비스 한 컨트롤러에 책 전체의 도구를 모으는 *후련함*을 보여줬다. 21에 머무를지 25로 갈지의 판단 기준도 함께 정리했다.

이 장이 책의 *현장 정착점*이다. 11년 동안 자바가 걸어온 길이 *Spring과 만나는 자리*에서 어떻게 표현되는지 한 줄로 이어진다. 우리가 매일 적는 컨트롤러, repository, configuration, HTTP client — 그 평범한 자리에 현대 자바의 모든 도구가 자연스럽게 들어가 있다. 한 줄짜리 record가 어떻게 그곳에 도달했는지, 한 줄짜리 `spring.threads.virtual.enabled`가 어떤 11년의 진화 끝에 가능해졌는지를 *기억해두자*.

그렇다면 여기서 멈출까? 자바는 어디까지 갈까? Project Valhalla의 value class, Project Amber의 다음 카드, Project Babylon의 GPU·이질 컴퓨팅, Project Leyden의 종착점 — 26 이후의 자바가 무엇을 준비하고 있는지 마지막 장에서 함께 들여다보자. 1장에서 시작한 PayBridge 이야기를 *5년 뒤*로 한 번 연장해 보자. 책의 마지막 장이다.

---

# Part X. 다음 자바

11년을 거슬러 올라온 책이 마지막에 와서 *앞을 본다*. Java 26 이후의 자바 — Valhalla, Amber, Babylon, Leyden — 가 어떤 모양으로 도착할지를 그린다. 이 부의 한 장(22장)이 1장의 지도를 *미래로 연장*하며 책을 닫는다.

22장은 네 Project의 미래상이다. *Valhalla* — value class와 primitive class가 들어오면 자바의 객체 모델이 어떻게 바뀌는지, `Integer`와 `int`의 경계가 어떻게 *흐려지는지*를 본다. *Amber* — primitive type patterns, with expressions, deconstruction의 확장이 records와 sealed 위에서 *어디까지 갈 수 있는지*. *Babylon* — Code Reflection이 자바 코드를 *런타임에 다른 형태로 변환*하는 일이 어떻게 GPU·CUDA·SQL로 옮겨갈 수 있는지. *Leyden* — AOT의 그 다음 한 걸음, *condensers*가 무엇을 약속하는지.

그리고 PayBridge의 5년 뒤 코드를 함께 상상한다. 11년의 결제 SaaS 코드베이스가 *어떻게 변해갈지*를 그려보며, 책의 시작에서 만난 PayBridge와 *수미상관*을 이룬다. 람다·records·virtual thread·AOT를 거쳐온 코드가 그 다음 무엇을 향하는지를 함께 본다.

자바의 11년을 한 줄로 묶어낸 이 책이 마지막에 와서 *그 한 줄을 미래로 연장*한다. 자바는 어디까지 갈까. 함께 그 풍경을 그려보자.

---

## 22장. Valhalla · Amber · Babylon · Leyden — 26 이후의 자바

PayBridge의 5년 뒤 코드를 상상해 보자.

2030년의 어느 평범한 화요일이다. PayBridge는 이제 가맹점 수십만 개를 처리하는 동남아 최대 결제 미들레이어가 됐다. 사내 LTS는 *Java 30*이다. 결제 컨트롤러는 21장에서 본 그 코드의 *5년 뒤 버전*이다. 도메인 모델은 여전히 record와 sealed로 적혀 있는데, 자세히 들여다보면 한 가지가 달라졌다. record 앞에 `value`라는 키워드가 붙어 있다. `Optional<T>`도 value class가 됐다. 정산 배치는 GPU에서 도는데, 그 코드를 자바로 직접 적었다. JNI도, CUDA도, Python bridge도 없다. 그리고 콜드 스타트가 *400ms*다.

이 풍경이 *그럴듯해* 보이는가? 그렇다면 좋은 신호다. 1장에서 그린 PayBridge의 11년 코드 변천 이야기를 *5년 뒤*로 연장해 보자. 그 5년 동안 자바는 무엇을 했을까. *자바는 어디까지 갈까?* 이 책의 마지막 장에서, 26 이후의 자바가 어떤 모양으로 만들어지고 있는지 함께 살펴보자.

> **이 장의 disclaimer — 시점 명시**
>
> 이 책이 인쇄되는 시점(2026년 5월)을 기준으로 *알려진* 26 이후의 모습을 정리한다. **JEP 401 (Value Classes and Objects)**, Project Valhalla, Project Amber, Project Babylon, Project Leyden 모두 *진행 중*이다. 이 글에 적힌 어휘, 키워드, 일정은 변할 수 있다. 특히 String Templates가 21·22 preview를 거쳐 23에서 *철회*되고 재설계 중인 사례에서 보듯이, OpenJDK의 *preview 단계 자정*은 자주 일어난다. 이 장은 *방향*을 읽는 자료이지, *확정된 스펙*이 아니다. 인쇄 이후의 최신 상태는 OpenJDK 공식 페이지(`openjdk.org/projects/valhalla`, `openjdk.org/projects/amber`, `openjdk.org/projects/babylon`, `openjdk.org/projects/leyden`)에서 확인하자.

### Project Valhalla — primitive와 reference의 *통합*

먼저 가장 오래 기다린 프로젝트부터 살펴보자. Project Valhalla는 2014년 *책의 출발점인 Java 8과 같은 해*에 시작됐다. 그동안 자바 진영의 거의 모든 발표에서 한 번씩은 언급됐고, 그때마다 *조금만 더*라는 말이 따라왔다. 11년이 지난 지금, Valhalla는 마침내 가시 거리에 들어왔다. **JEP 401: Value Classes and Objects** — Java 26 preview 타깃으로 예고되어 있다.

Valhalla가 풀려는 문제가 무엇인가? *primitive와 reference의 분리*다. Java 8에서 `int`와 `Integer`의 차이를 처음 만난 신입 개발자가 *난감해했던* 그 자리다. `int`는 메모리에 4바이트로 *납작하게* 박혀 있다. `Integer`는 객체라 헤더 16바이트 + 값 4바이트 + 정렬 패딩까지, 한 개당 *수십 배 무거운* 신원을 갖는다. 그래서 `List<Integer>` 천만 개는 *수백 메가바이트의 heap*을 먹는다. `int[]` 천만 개는 40MB짜리 *연속 메모리*다.

11년 동안 이 *찜찜함*을 우회로 살아왔다. Stream API에 `IntStream`이 따로 있는 이유, `Optional`이 `OptionalInt`·`OptionalLong`을 따로 가진 이유, generics에 primitive를 못 쓰는 이유 — 전부 같은 한 가지 *분리*에서 나온 비용이다.

#### value class — 객체이되 신원이 없다

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

#### null-restricted types

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

#### frozen arrays

또 하나 짚어야 할 카드가 있다. **frozen array**다. 자바의 array는 mutable이다. `int[] arr`을 받은 메서드가 안에서 값을 바꿔 버릴 수 있다. 그래서 immutable한 데이터를 표현하려고 `List.copyOf(...)`로 한 번 더 감싸는 *번거로움*이 따라왔다.

```java
// 가상의 미래 자바
int[] data = {1, 2, 3, 4, 5};
int!frozen[] view = data.freeze();
// view[0] = 99; // 컴파일 에러
```

frozen array는 *읽기 전용* 약속을 array 자체에 박는다. value class array와 결합하면 — `Money!frozen[]` 같은 표현이 — *완벽한 immutable + flat memory*의 자리를 만든다. 함수형 자바의 가장 *번거롭던* 자리가 정리된다.

#### Valhalla가 흔드는 표면들

Valhalla가 정식화되면 자바 전반이 흔들린다. 흔들리는 자리를 헤아려 보자.

- **`Optional<T>`이 value class로 옮겨감.** 박싱 비용이 사라진다. `OptionalInt`·`OptionalLong`이 *불필요해진다*.
- **`Integer`·`Long`·`Double` 등 wrapper가 value class로 재정의됨.** 호환성을 유지하면서 박싱 비용 소멸.
- **`Stream<Integer>`와 `IntStream`의 *분리 이유 자체가 사라짐*.** 11년 동안 두 길로 갈라져 있던 API가 자연 통합.
- **Vector API가 정식 표준화됨.** Valhalla를 기다리느라 9차 incubator에 머물던 JEP 489가 마침내 표준이 된다.
- **`@ValueBased` 어노테이션이 *진짜 약속*이 됨.** Java 16에서 hint로 도입됐던 어노테이션이, 언어 차원의 키워드로 정식화.

이 다섯 자리는 *우리가 매일 적던 코드*다. 그 자리에서 *동일한 의도가 더 효율적인 표현*으로 바뀐다. Valhalla가 정착하면, *Java 30의 코드를 Java 25 개발자가 봐도 거의 똑같이 읽힌다*. 그러나 그 코드가 도는 효율은 *수 배 차이*가 난다. 이게 호환성을 지키며 진화하는 자바의 *고유한* 방식이다.

### Project Amber의 다음 카드

다음으로 Amber를 들여다보자. Amber는 자바의 *언어 표면*을 다듬는 우산 프로젝트다. records, sealed classes, pattern matching, text blocks, `var` — 11장부터 13장까지 살펴본 카드들이 전부 Amber에서 나왔다. 다음 카드는 무엇인가?

#### primitive type patterns

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

#### array patterns

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

#### with-expressions — record의 *부분 복사*

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

### String Templates의 좌초와 재설계 — 사후 추적

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

### Project Babylon — Java가 GPU·자동미분에 닿는다

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

#### 자동미분 (autodiff)

```java
// 가상의 미래 자바
Function<Double, Double> f = x -> x * x + 3 * x + 1;
Function<Double, Double> dfdx = Autodiff.derivative(f);
double slope = dfdx.apply(2.0);  // = 2*2 + 3 = 7
```

람다의 *구조*를 들여다보고, 미분 규칙을 적용해 *새 람다*를 만든다. ML 학습 코드를 자바로 적을 수 있다.

#### SQL DSL

```java
// 가상의 미래 자바
Stream<Payment> result = sql.from(Payment.class)
    .where(p -> p.amount().compareTo(BigDecimal.valueOf(1000)) > 0)
    .where(p -> p.status() == PaymentStatus.APPROVED)
    .stream();
// 람다가 *컴파일러 차원*에서 SQL where 절로 변환됨
```

JOOQ, QueryDSL, Criteria API가 지금까지 *문자열 빌더*나 *메타모델 + builder*로 우회했던 자리를, Babylon이 *언어 차원에서* 풀어낸다.

#### HAT (Heterogeneous Accelerator Toolkit)

Babylon의 첫 가시적 결실이 **HAT**다. CPU·GPU·FPGA 같은 이질 가속기에 *동일한 자바 코드*가 매핑되는 toolkit이다. 머신러닝, 행렬 연산, 신호 처리 — 그동안 Python이나 C++로 적던 자리가 자바로 옮겨질 수 있다.

PayBridge의 5년 뒤를 다시 떠올려 보자. 정산 배치가 GPU에서 돈다고 했다. 그 코드가 *자바*다. 11장에서 적은 record DTO, 13장에서 적은 sealed result, 14장에서 적은 virtual thread — 같은 어휘로 GPU·CPU·FPGA가 매핑된다. *한 언어로 끝나는* 자바의 야망이다.

언제 오는가? *모른다*. Babylon은 가장 야심차고 가장 *느린* 프로젝트다. 그러나 방향은 분명하다 — 자바는 *자기 영역 밖*까지 자기 어휘를 확장한다.

### Project Leyden의 종착점 — *static image + AOT code cache*의 일반화

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

### 호환성 — 자바의 *가장 큰 자산*

여기서 한 발 물러서 보자. Valhalla, Amber, Babylon, Leyden — 네 프로젝트를 관통하는 *공통점*이 무엇인가? **호환성을 깨지 않으면서** 진화한다는 점이다.

- **Valhalla.** value class는 기존 class와 호환된다. `Optional`이 value class로 옮겨가도, 옛 코드는 한 글자도 안 바꿔도 돈다.
- **Amber.** primitive patterns, array patterns, with-expressions — 모두 옛 문법을 *대체*하지 않고 *추가*한다. records, sealed, pattern matching이 그랬듯이.
- **Babylon.** code reflection은 *기존 람다 위에 얹는* 도구다. 옛 람다는 그대로 돈다. Babylon이 들여다보고 싶을 때만 들여다본다.
- **Leyden.** AOT cache는 *training run*의 결과를 *선택적으로* 적용한다. 기존 부팅 경로는 그대로 살아 있다.

이게 자바의 *가장 큰 자산*이다. 11년 동안 Java 8에서 Java 25까지 오면서, 거의 모든 옛 코드가 *컴파일러 한 줄 옵션*만으로 새 JVM에서 돈다. 다른 언어 진영의 *깨는 변경*과 비교해 보자. Python 2 → 3는 *10년의 고통*이었다. Scala 2 → 3는 *대대적 재작성*이었다. 자바는 같은 11년에 *람다·records·virtual thread·AOT·pattern matching*을 가져왔는데, 그 사이 *깨는 변경은 거의 없었다*.

이게 *지루함*인가? 아니다. *신뢰*다. 어제의 코드가 내일도 도는 것 — 엔터프라이즈가 자바를 떠나지 못하는 진짜 이유다. 11년 전 Java 8로 적은 PayBridge의 첫 마이크로서비스가 *지금도 그대로 도는* 자리를 만들어 준 것은, 컴파일러 팀의 *고집스러운* 호환성 약속이었다.

### 수미상관 — PayBridge의 가상 Java 30 코드

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

### 마무리 — 11년의 자바를 견뎌낸 자바 개발자에게

이 책을 여기까지 따라온 자바 개발자에게 한 페이지의 헌사를 남기자.

11년이라는 시간을 한 줄로 정리하기는 어렵다. 람다를 처음 만났을 때의 *어색함*, Stream의 `peek`을 두고 배포한 *찜찜함*, Optional을 처음 잘못 쓴 *당혹감*, NullPointerException의 *지긋지긋함*, 30자 타입 선언의 *번거로움*, jakarta namespace 전환 첫날의 *막막함*, virtual thread 켰는데 deadlock이 난 *끔찍한* 새벽, 콜드 스타트 8초의 *난감함*, String Templates 좌초의 *허망함*, 600줄짜리 `if-else` 분기를 패턴 매칭으로 옮긴 *후련함*, 그리고 한 컨트롤러에 11년의 도구가 모이는 그 *깊은 만족감*.

이 모든 감정을 함께 겪으며 코드를 다듬어 온 11년이다. 그 코드는 지금도 어딘가에서 돌고 있고, 누군가의 결제 거래를 처리하고 있고, 누군가의 메시지를 전달하고 있다. *어제의 자바가 오늘도 돈다.* 그게 자바라는 언어의 *가장 큰 약속*이고, 그 약속을 *지키는 일*이 컴파일러 팀의 *고집스러운 일관성* 위에서만 가능했다.

자바는 *완벽한 언어*가 아니다. Kotlin·Scala·Rust가 자바보다 표현력에서 앞선 자리가 여럿 있다. 자바는 그 자리를 *서두르지 않고* 한 LTS, 한 preview, 한 자정을 거쳐 받아들인다. records가 14에서 16까지 2년, virtual thread가 19에서 21까지 2년, AOT가 10에서 25까지 15년 — 자바의 시간 단위는 다른 언어보다 길다. 그 *느림*이 호환성을 만들고, 그 호환성이 PayBridge 같은 회사가 16년의 코드를 *한 언어로* 이어 쓸 수 있는 자산이 된다.

이 책의 마지막 한 페이지에서, 한 가지를 *기억해두자*. *Modern Java는 끝나지 않았다.* Valhalla가 들어오고, Babylon이 GPU에 닿고, Leyden이 콜드 스타트를 풀고, Amber가 with-expression을 가져오는 그 *다음 11년*이 우리를 기다리고 있다. 그리고 그 11년의 코드는 지금 우리가 쓰는 자바와 *같은 자바*다 — 더 빠르고, 더 안전하고, 더 표현력이 풍부하지만, 한 줄을 *대대적으로 재작성*하지 않아도 되는 자바.

이제 우리가 할 일은 한 가지다. 다음 자바를 *함께 기다려보자*. JEP를 읽고, preview를 켜 보고, 우리 코드에 *맞는 자리*를 찾아 천천히 옮겨가 보자. 11년 전 람다를 처음 손에 잡았을 때 그랬듯이 — *어색함*에서 시작해 *익숙함*을 거쳐 *후련함*에 도달해 보자.

자바 개발자로서의 11년을 견뎌낸 당신에게, 그리고 다음 11년을 함께 걸어갈 당신에게, 이 책을 바친다.

*함께 다음 자바를 기다려보자.*

---

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

---

# 부록 B. JLS 인용 인덱스

본문에서 우리는 JLS(Java Language Specification)와 JVM 스펙을 곳곳에서 인용했다. 어떤 자리는 한 페이지짜리 박스를 통째로 할애했고, 어떤 자리는 본문 한 줄에 §번호만 슬쩍 끼워두었다. 이 부록은 그 인용을 *양방향으로* 찾을 수 있게 한 인덱스다.

두 표가 있다. 첫 번째 표는 *챕터에서 JLS로* — "내가 11장에서 본 records 정의는 JLS의 어디인가?". 두 번째 표는 *JLS에서 챕터로* — "JLS §14.30을 봤는데, 이 책에서 어디에 나오는가?". 두 방향 모두 자주 쓰인다.

인용은 가급적 *원문 + 한국어 번역*을 짝지어 본문에 실었다. JLS는 영문이 정본이지만, 한국 독자를 위해 의미를 풀어 번역하고 그 옆에 원문을 박스로 같이 두었다. 박스를 *2~4단 구성*(원문 / 번역 / 의미 해설 / 본문과의 연결)으로 정리한 것도 이 때문이다.

기준 JLS 버전은 *JLS 21(JSR 396)*이고, 25 표준화 항목은 *JLS 25*(2025-09-16 GA 시점)를 참조했다. Memory Model 부분은 JSR-133 원문도 함께 인용했다.

---

## B.1 표 1 — 챕터 → JLS

본문 챕터 순서로 정리했다. 각 행의 *주제* 열은 해당 인용이 답하려는 질문을, *인용 위치* 열은 본문 안에서 그 박스가 어디 들어갔는지를 알려준다.

| 챕터 | JLS § | 정식 명칭 | 주제 | 인용 위치 |
|---|---|---|---|---|
| 3장 | §15.27 | Lambda Expressions | "effectively final"의 정확한 정의 | 본문 박스 1쪽 |
| 3장 | §15.27.2 | Lambda Body | 람다 본체와 enclosing 컨텍스트의 관계 | 본문 박스 0.5쪽 |
| 5장 | (패키지 문서) | `java.util.stream` | Stream의 *non-interference* 조건 | 본문 박스 1쪽 |
| 6장 | (패키지 문서) | `java.util.stream.Gatherer` | Gatherer의 contract — `integrator`·`finisher`·`combiner` | 본문 박스 1쪽 |
| 7장 | (Javadoc) | `java.util.Optional` | "value-based class" — `==` 비교 금지 근거 | 본문 박스 0.5쪽 |
| 8A장 | §17.4 | Memory Model | happens-before 관계의 정의 | 본문 박스 2쪽 (JSR-133 원문 포함) |
| 8A장 | §17.5 | final Field Semantics | `final` 필드의 publication 보장 | 본문 박스 1쪽 |
| 8A장 | (JSR-133 원문) | JSR-133 Java Memory Model | happens-before·sequential consistency·OOTA 차단 | 본문 박스 2쪽 |
| 9장 | §7.7 | Module Declarations | `module-info.java`의 5개 키워드 정의 | 본문 박스 1쪽 |
| 9장 | §7.7.1 | Dependences | `requires` / `requires transitive` / `requires static` | 본문 박스 0.5쪽 |
| 10장 | §14.4 | Local Variable Declaration Statements (LVTI) | `var`의 추론 규칙 | 본문 박스 1쪽 |
| 10장 | §14.11 | The `switch` Statement | switch statement (fall-through 형식) | 본문 박스 1쪽 |
| 10장 | §15.28 | Switch Expressions | `case L ->`·`yield`의 정의 | 본문 박스 1쪽 |
| 10장 | §3.10.6 | Text Blocks | incidental whitespace 알고리즘 — *왜 들여쓰기가 자동 제거되는가* | 본문 박스 1쪽 (예제 포함) |
| 11장 | §8.10 | Record Classes | record의 정의·자동 생성 멤버 | 본문 박스 1쪽 |
| 11장 | §8.10.4 | Record Constructors | canonical constructor·compact constructor의 정의 | 본문 박스 0.5쪽 |
| 12장 | §8.1.1.2 | `sealed` Classes | `sealed`·`permits`·`non-sealed`·`final`의 정의 | 본문 박스 1쪽 |
| 13장 | §14.30 | Patterns | pattern의 정의 — type pattern·record pattern | 본문 박스 1쪽 |
| 13장 | §14.30.3 | Exhaustiveness of switch | exhaustiveness check의 정의 — sealed와의 관계 | 본문 박스 1쪽 |
| 14장 | §17.1 | Threads | Thread의 정의 (virtual / platform) | 본문 박스 0.5쪽 |
| 14장 | (JEP 444 원문) | Virtual Threads | virtual thread의 의도·M:N 스케줄링 | 본문 박스 1쪽 |
| 16장 | (JEP 506 원문) | Scoped Values | ScopedValue의 contract — bounded·immutable | 본문 박스 1쪽 |
| 16장 | (JEP 505 원문) | Structured Concurrency | `StructuredTaskScope`의 success/failure semantics | 본문 박스 0.5쪽 |
| 17장 | §12.6 | Finalization of Class Instances | finalize의 deprecation — Cleaner 권장 | 본문 박스 0.5쪽 |
| 18장 | (Javadoc) | `java.lang.foreign.MemorySegment` | MemorySegment의 lifetime 규칙 | 본문 박스 0.5쪽 |
| 22장 | (Project Valhalla draft) | Value Classes | value class의 의도·미래 | 본문 박스 0.5쪽 (disclaimer 포함) |

3장의 §15.27 박스는 책 전체에서 가장 자주 *되돌아보게 되는* 인용이다. "effectively final"이 람다·local class·익명 inner class 모두에 적용되는 *하나의 정의*임을 거기서 못박는다.

8A장의 §17.4 박스는 책에서 가장 길게 인용한 부분이다. JSR-133 원문까지 함께 실은 이유는 — JLS 본문은 happens-before의 *정의*만 다루는데, *왜 그렇게 정의했는가*는 JSR-133 원문이 답하기 때문이다.

---

## B.2 표 2 — JLS § → 챕터

JLS 섹션 번호 순으로 정렬했다. JLS를 보다가 *이 부분이 책의 어디서 다뤄졌나*를 찾을 때 쓰자.

| JLS § | 정식 명칭 | 챕터 | 비고 |
|---|---|---|---|
| §3.10.6 | Text Blocks (incidental whitespace) | 10장 | 알고리즘 박스 |
| §7.7 | Module Declarations | 9장 | 5개 키워드 |
| §7.7.1 | Dependences | 9장 | `requires` 변형 |
| §8.1.1.2 | `sealed` Classes | 12장 | permits·non-sealed·final |
| §8.10 | Record Classes | 11장 | record 정의 |
| §8.10.4 | Record Constructors | 11장 | canonical·compact |
| §12.6 | Finalization of Class Instances | 17장 | finalize deprecation |
| §14.4 | Local Variable Declaration (LVTI) | 10장 | `var` 추론 |
| §14.11 | The `switch` Statement | 10장 | statement form |
| §14.30 | Patterns | 13장 | pattern 정의 |
| §14.30.3 | Exhaustiveness of switch | 13장 | sealed exhaustive |
| §15.27 | Lambda Expressions | 3장 | effectively final |
| §15.27.2 | Lambda Body | 3장 | enclosing context |
| §15.28 | Switch Expressions | 10장 | `case L ->`·`yield` |
| §17.1 | Threads | 14장 | virtual / platform |
| §17.4 | Memory Model | 8A장 | happens-before |
| §17.5 | `final` Field Semantics | 8A장 | publication 보장 |
| (JSR-133) | Java Memory Model | 8A장 | happens-before 정의문 |
| (JEP 444) | Virtual Threads | 14장 | M:N 스케줄링 |
| (JEP 506) | Scoped Values | 16장 | bounded·immutable |
| (JEP 505) | Structured Concurrency | 16장 | StructuredTaskScope |
| (`java.util.stream`) | Stream non-interference | 5장 | 패키지 문서 |
| (`Gatherer`) | Gatherer contract | 6장 | integrator·finisher |
| (`Optional`) | value-based class | 7장 | `==` 금지 |
| (`MemorySegment`) | lifetime 규칙 | 18장 | FFM |
| (Valhalla draft) | Value Classes | 22장 | disclaimer 박스 |

§17.4와 §17.5가 같은 8A장에 모이는 게 자연스럽다. 메모리 모델 한 단원에서 *happens-before*와 *`final` field publication*은 같은 동전의 양면이기 때문이다.

§14.30·§14.30.3 둘이 13장에 함께 묶이는 것도 마찬가지 — 패턴 매칭의 *정의*(§14.30)와 *그 정당성 보장*(§14.30.3, exhaustiveness)이 한 호흡에 들어간다.

---

## B.3 인용 박스의 구조 — *원문 / 번역 / 의미 / 연결*

본문에 들어간 모든 JLS 인용 박스는 동일한 4단 구성을 따랐다. 다시 읽거나 인용을 직접 참조할 때 도움이 되도록 그 구조를 적어둔다.

```
┌─────────────────────────────────────┐
│ JLS §X.Y (정식 명칭)                  │
├─────────────────────────────────────┤
│ [원문 — 영문]                         │
│ A record class is a special kind... │
├─────────────────────────────────────┤
│ [한국어 번역]                          │
│ record 클래스는 ... 의 특별한 종류다.    │
├─────────────────────────────────────┤
│ [의미 해설]                            │
│ "shallowly immutable"이 왜 중요한가...  │
├─────────────────────────────────────┤
│ [본 챕터 본문과의 연결]                  │
│ 우리가 위 예제에서 본 Point는 ...        │
└─────────────────────────────────────┘
```

- *원문*은 가급적 한 문장 또는 한 문단으로 끊는다. 너무 길면 문맥이 흐트러진다.
- *번역*은 직역보다 *의미가 통하는 번역*을 선호한다. 자바 용어는 그대로 두되, 일반어는 한국어로.
- *의미 해설*은 spec의 표현이 *왜 그렇게* 됐는지를 한 문단으로 푼다.
- *연결*은 본문의 그 자리에서 이 박스를 *왜 펼쳤는가*를 한 줄로 적는다.

이 4단 구성이 책 전체에서 일관되니, 박스의 모양만 봐도 "지금 spec을 읽고 있구나"가 바로 보일 것이다.

---

## B.4 spec 원문을 직접 읽고 싶다면

OpenJDK 공식 사이트에서 JLS 25 정본을 PDF/HTML로 받을 수 있다. URL은 시점에 따라 바뀌니 *jls 25 pdf*로 검색하는 편이 빠르다. 책에서 쓴 §번호는 JLS 21·25 모두 거의 같지만, 25에서 새로 추가된 항목(예: `void main()`, sealed 관련 보강)은 25 정본을 참조해야 정확하다.

JSR-133(Java Memory Model)은 별도 문서다. *Java Memory Model and Thread Specification*이라는 제목의 PDF가 정본이고, Doug Lea의 [JSR-133 cookbook](https://gee.cs.oswego.edu/dl/jmm/cookbook.html)이 더 읽기 좋은 해설이다. 8A장의 후반부는 이 둘을 함께 읽기를 권한다.

JEP 원문은 `openjdk.org/jeps/{번호}` 한 줄로 충분하다. 부록 A의 JEP 일람과 함께 보면 좋다.

---

## B.5 인용 누락에 대한 양해

이 책은 JLS의 *모든* 인용을 다루지 않는다. 자바의 핵심 변화 — 11년의 굵직한 변화에 한정해 인용을 골랐다. 예를 들어 generics(§8.4), exceptions(§11), annotations(§9.6) 같은 *이미 알고 있다고 전제한 영역*은 인용을 생략했다.

또 한 가지 — 책에서 spec을 *부분적으로 단순화한* 자리도 있다. 정확한 spec 문장은 종종 너무 정밀해서 한 권의 책에서 다 풀기 어렵다. 본문 박스에서 "단순화"라는 말이 등장한다면, 원문은 더 정밀하고 더 까다롭다는 뜻이다. 정확한 동작이 의심스러우면 늘 *원문 정본*으로 돌아가자.

마지막으로 — *spec은 진화한다*. 25 시점의 spec이 26·27에서 어떻게 바뀔지는 아무도 정확히 모른다. Project Valhalla·Amber·Babylon·Leyden이 spec에 닿을 때, 이 인덱스도 함께 갱신될 것이다. 22장의 disclaimer 박스를 한 번 더 짚어두자.

---

# 부록 C. 마이그레이션 체크리스트

본문 20·20A·21장에서 우리는 마이그레이션의 *왜*와 *어떻게*를 길게 다뤘다. 이 부록은 실무에서 한 장 인쇄해서 *벽에 붙여놓고 줄을 그어가며* 쓸 수 있는 체크리스트다. 4단계로 나눴다 — 8 → 11, 11 → 17, 17 → 21, 21 → 25.

각 단계는 *건너뛰지 말자*. 8에서 21로 한 번에 이주하는 시도는 흔하지만, 단계마다 *고유한 함정*이 있어서 한꺼번에 처리하면 어디서 뭐가 깨졌는지 분간하기 어렵다. 단계별로 빌드를 통과시키고, CI를 녹색으로 만든 뒤 다음 단계로 넘어가는 편이 낫다.

---

## C.1 Step 1 — JDK 8 → JDK 11

가장 큰 충격원은 **Java EE 모듈 제거**(JEP 320)와 **Oracle JDK 라이선스 유료화**다. 빌드가 깨지는 자리 대부분이 이 둘이다.

### 빌드·런타임 환경

- [ ] JDK 배포본 결정 — OpenJDK·Temurin·Corretto·Liberica·Zulu 중 하나로 표준화
- [ ] 빌드 도구 최소 버전 확보 — Maven 3.6.3+, Gradle 7.3+
- [ ] CI/CD 파이프라인의 JDK 이미지 갱신
- [ ] 로컬 개발자 환경 — 모든 팀원 동일 JDK 버전·배포본 합의

### 코드 변경 — javax.* 제거 항목

- [ ] **JAXB**(`javax.xml.bind`) — `jakarta.xml.bind` + `org.glassfish.jaxb` 의존성 추가
- [ ] **JAX-WS**(`javax.xml.ws`) — `jakarta.xml.ws` + Metro·CXF로 이주
- [ ] **JTA**(`javax.transaction`) — `jakarta.transaction-api` 추가
- [ ] **CORBA**(`javax.activity`, `org.omg.*`) — 사용 중이면 별도 라이브러리 필요. 가능하면 *제거 권장*
- [ ] **javax.annotation**(`@PostConstruct`, `@PreDestroy` 등) — `jakarta.annotation-api` 추가
- [ ] **Nashorn**(`javax.script` ECMAScript 엔진) — 11에서 deprecation, 15에서 제거. GraalVM JS로 대체

### 내부 API·classpath

- [ ] `jdeps --jdk-internals` 실행 — `sun.*`·`com.sun.*` 사용처 식별
- [ ] `--add-opens`·`--add-exports`로 임시 허용 자리 목록화 (나중에 갚을 빚으로)
- [ ] reflection 기반 라이브러리(Lombok·Mockito·ByteBuddy) — 11 지원 버전 확인
- [ ] AspectJ 사용 시 — Java 11 호환 1.9.6+ 이상

### 빌드 인자

- [ ] `--release 11` 사용 — `-source`/`-target` 조합보다 안전
- [ ] Surefire/Failsafe — 2.22.2+ (모듈 시스템 인식)
- [ ] JaCoCo — 0.8.6+ (Java 11 bytecode 지원)

### 운영 환경

- [ ] **Docker 이미지 RSS 증가 대비** — JDK 8 대비 ~20% 증가 흔함. 컨테이너 memory limit 재산정
- [ ] G1이 default가 됨 — `-XX:+UseG1GC`는 명시 불필요
- [ ] `CompressedOops` 기본 동작 변경 확인
- [ ] JFR·JMC 사용 시작 검토 — 11부터 오픈소스

### 검증

- [ ] 전체 테스트 통과
- [ ] 부하 테스트 — throughput·p99 latency를 8 baseline과 비교
- [ ] 프로덕션 카나리아 배포 — 최소 1주

---

## C.2 Step 2 — JDK 11 → JDK 17

이 단계의 핵심은 **Spring Boot 2.7 → 3.x**다. 사실상 *javax → jakarta* 패키지 이주가 가장 큰 작업이다. Spring을 안 쓴다면 훨씬 가볍다.

### 빌드·런타임 환경

- [ ] JDK 17 LTS 확보 — Temurin·Corretto·Liberica 17
- [ ] Maven 3.6.3+ / Gradle 7.5+ (Gradle 8 권장)
- [ ] Kotlin 사용 시 — 1.7.0+ (JVM target 17 지원)

### Spring Boot 3.x 이주

- [ ] **javax → jakarta** 패키지 import 변경 (대규모 sed/IDE 작업)
- [ ] Spring Boot 3.x baseline — Java 17
- [ ] Spring Security 6 — 설정 API 대거 변경 (`WebSecurityConfigurerAdapter` deprecated)
- [ ] Spring Data 3.x — repository 메서드 시그니처 변경 일부
- [ ] Hibernate 6 — query·LazyInitializationException 동작 변경
- [ ] application.properties — `spring.config.*` 키 일부 변경
- [ ] Actuator — 일부 엔드포인트 응답 형식 변경

### 언어 신규 기능 *도입 후보* (점진 적용)

- [ ] **records** — DTO부터 시작. 14~16에서 도입된 product type
- [ ] **sealed classes** — 도메인 모델의 *합 타입* 자리
- [ ] **pattern matching for `instanceof`** — `if (x instanceof Foo f) ...` 패턴
- [ ] **switch expression** — `case L ->`·`yield`
- [ ] **text blocks** — JSON·SQL·HTML 리터럴 정리

### 보안

- [ ] **SecurityManager deprecation 영향 확인** — 17에서 deprecated. 25+ 완전 제거 예정
- [ ] `--add-opens` 필요 자리 재확인 — strong encapsulation default (JEP 403)
- [ ] **EdDSA** 사용 검토 (Ed25519·Ed448) — TLS·서명에서 RSA·ECDSA 대안

### 빌드 인자

- [ ] `--release 17`
- [ ] `--enable-preview` 사용처 식별 — preview 기능을 production에 쓰지 않기 권장
- [ ] JaCoCo 0.8.8+
- [ ] PIT mutation testing 1.9.0+ (사용 중이면)

### 운영 환경

- [ ] Generational ZGC (21에서 도입, 23 default) 대비 — 17에선 G1 또는 비-generational ZGC
- [ ] Container-aware CPU·memory 인식 자동화 (11+부터 default지만 재확인)
- [ ] JFR streaming 활용 검토

### 검증

- [ ] 컴파일·테스트 통과
- [ ] Spring Boot 3.x 통합 테스트
- [ ] 회귀 시나리오 — 인증·트랜잭션·캐시
- [ ] 프로덕션 카나리아 — 최소 2주 (Spring Boot 3.x 안정성 검증 필요)

---

## C.3 Step 3 — JDK 17 → JDK 21

이 단계의 *진짜* 변화는 **Virtual Threads**다. 도입 자체는 한 줄(`spring.threads.virtual.enabled=true`)이지만, *어디에 적용할지*가 가장 중요한 결정이다.

### 빌드·런타임 환경

- [ ] JDK 21 LTS 확보
- [ ] Spring Boot 3.2+ (virtual thread 통합 안정화 버전)
- [ ] Maven 3.9+ / Gradle 8.5+

### Virtual Thread 도입 후보 식별

- [ ] **I/O-bound 컨트롤러** — 외부 API·DB 호출이 주된 작업
- [ ] **batch / scheduled 작업** — 다수의 동시 작업이 I/O 대기 위주
- [ ] CPU-bound 작업은 *제외* — virtual thread의 이득 없음
- [ ] `spring.threads.virtual.enabled=true` 시범 적용 (스테이징 먼저)

### Pinning 위험 자리 audit (JEP 491 *이전*에는 특히 중요)

- [ ] **HikariCP 버전 확인** — 5.0.0+ (synchronized → ReentrantLock)
- [ ] **MySQL Connector/J** — 8.0.32+ (pinning 해소)
- [ ] **Postgres JDBC** — 42.5.0+ 권장
- [ ] **Caffeine 캐시** — 3.1.5+ (synchronized 제거)
- [ ] **Apache HttpClient** — 5.x 사용
- [ ] **MongoDB Java Driver** — 4.10+
- [ ] **Redis (Lettuce/Jedis)** — 최신 버전 확인
- [ ] **JFR `jdk.VirtualThreadPinned` 이벤트** 모니터링 활성화

### ThreadLocal 사용처 재검토

- [ ] **ThreadLocal 사용처 인벤토리** — 수백만 virtual thread 환경에서 메모리 폭발 위험
- [ ] **MDC**(SLF4J) — virtual thread에서 동작 검증
- [ ] **Security Context** — Spring Security의 `SecurityContextHolder`
- [ ] **트랜잭션 컨텍스트** — `TransactionSynchronizationManager`
- [ ] **ScopedValue 검토** (21 preview, 25 표준) — long-lived per-thread caching의 후임 후보

### 언어 신규 기능 *도입 후보* (점진 적용)

- [ ] **pattern matching for `switch`** — sealed exhaustive switch
- [ ] **record patterns** — `case Point(int x, int y) -> ...`
- [ ] **Sequenced Collections** — `getFirst`·`getLast`·`reversed` 활용
- [ ] **String Templates** — 21 preview였으나 23에서 철회. *도입 보류*

### 운영 환경

- [ ] **Generational ZGC 활성화 검토** — `-XX:+UseZGC -XX:+ZGenerational`
- [ ] 컨테이너 메모리 — ZGC는 off-heap 메타데이터 ~5% 추가 필요
- [ ] GC log 형식 — `-Xlog:gc*:file=...` (`-XX:+PrintGCDetails` deprecated)

### 검증

- [ ] virtual thread 시범 적용 — 컨트롤러 1~2개부터
- [ ] pinning 모니터링 — 1주간 JFR 이벤트 0건 확인
- [ ] 부하 테스트 — throughput·p99·메모리 사용량
- [ ] 프로덕션 카나리아 — 최소 2주

---

## C.4 Step 4 — JDK 21 → JDK 25

25는 *언어*보다 *런타임·메모리·시작 시간*의 LTS다. Virtual Thread를 이미 도입했다면 이 단계의 충격은 매우 작다. *측정 후 옵트인*이 키워드.

### 빌드·런타임 환경

- [ ] JDK 25 LTS 확보
- [ ] Spring Boot 3.4+ (CDS·AOT 통합)
- [ ] Maven 3.9.6+ / Gradle 8.10+

### Compact Object Headers (JEP 519)

- [ ] **벤치마크 — 옵트인 후 측정**: `-XX:+UseCompactObjectHeaders`
- [ ] heap 사용량 ~10~22% 감소 확인
- [ ] CPU·throughput·latency 회귀 확인 (드물지만 발생 가능)
- [ ] **production 적용 결정 — 측정값 기반**. default 아님

### AOT Class Loading & Linking (JEP 483 + 514·515)

- [ ] Spring Boot 3.4+ CDS 활성화 — `spring-boot-maven-plugin`의 `process-aot` goal
- [ ] training run → AOT cache 생성 흐름 CI에 편입
- [ ] startup time 측정 — Petclinic 기준 ~36~42% 단축
- [ ] cache 무효화 정책 — 배포 파이프라인에 통합
- [ ] *GraalVM Native Image와 비교* 결정 — AOT만으로 충분한지

### Virtual Thread `synchronized` (JEP 491)

- [ ] JDK 24+부터 `synchronized` pinning 해소
- [ ] 21~23에서 ReentrantLock으로 회피했던 자리 — *그대로 둘지* 결정
- [ ] 신규 코드는 `synchronized`도 안전 — 단, 라이브러리 호환성 확인

### Scoped Values (JEP 506 표준)

- [ ] ThreadLocal 사용처 — ScopedValue로 단계적 이주 검토
- [ ] 인증 컨텍스트·요청 ID·테넌트 ID 같은 *읽기 전용·범위 한정* 데이터 우선
- [ ] Spring Security 통합 — Spring 측 ScopedValue 지원 시점 확인 필요

### Structured Concurrency (JEP 505 preview)

- [ ] 25에서도 *preview* — production 사용은 신중
- [ ] StructuredTaskScope 시범 적용 — fan-out 자리 1~2건
- [ ] 표준화 일정 모니터링 — JDK 26 표준 후보

### 언어 신규 기능

- [ ] **Flexible Constructor Bodies** (JEP 513) — `super(...)` 전 statement 허용
- [ ] **Module Import Declarations** (JEP 511) — `import module java.base;` (학습·스크립트용)
- [ ] **Compact Source Files**·**Instance Main** (JEP 512) — `void main()` (학습용)
- [ ] **Stream Gatherers** (JEP 485, 24부터 표준) — 슬라이딩 윈도우·fold·scan 도입 검토

### 보안

- [ ] **SecurityManager 완전 제거 대비** (JEP 486, 25+에서 진행) — 사용처 모두 제거
- [ ] **KDF API** (JEP 510) — HKDF·PBKDF 표준 사용 가능
- [ ] post-quantum 준비 — KEM·KDF 표준 API 활용

### 운영 환경

- [ ] **Generational Shenandoah** (JEP 521) — Red Hat 환경 고려
- [ ] AOT 사용 시 — 컨테이너 이미지에 cache 포함
- [ ] CDS archive — image build 단계에서 생성

### 검증

- [ ] 컴파일·테스트 통과
- [ ] Compact Object Headers 측정 → 옵트인 결정
- [ ] AOT startup time 측정 → CI에 baseline 기록
- [ ] 프로덕션 카나리아 — 최소 1주 (25는 비교적 안전한 LTS)

---

## C.5 단계 전체에 걸친 *상시 항목*

단계와 무관하게 마이그레이션 작업 내내 챙겨야 할 항목들이다.

- [ ] **빌드 시간 변화 추적** — JDK 버전별 컴파일 시간을 CI에서 측정
- [ ] **의존성 호환성 매트릭스** 유지 — 팀 내부 위키에 라이브러리별 검증 버전 기록
- [ ] **롤백 계획** — 각 단계마다 이전 JDK로 되돌릴 수 있는 절차 문서화
- [ ] **카나리아 → 점진 배포** 흐름 — 모든 단계에서 동일
- [ ] **변경 사항 changelog** 작성 — 팀 외부(다른 팀·운영팀)에 영향 가는 변경 공유
- [ ] **JFR baseline** 캡처 — 단계 전·후 비교 가능하도록
- [ ] **deprecation 경고 0** 목표 — `-Xlint:deprecation` 활성화 후 점진 청소

---

## C.6 시간 견적 (참고치)

작은 서비스(코드 5만 LOC 이내, 의존성 30개 미만) 기준 *대략적인* 견적이다. 큰 모놀리스는 단계마다 ×3~5 곱해 보는 게 안전하다.

| 단계 | 코드 변경 | 검증 | 카나리아 | 합계 |
|---|---|---|---|---|
| 8 → 11 | 1~2주 | 1주 | 1주 | **3~4주** |
| 11 → 17 (Spring Boot 3 포함) | 2~4주 | 2주 | 2주 | **6~8주** |
| 17 → 21 | 1주 | 1주 | 2주 | **4주** |
| 21 → 25 | 0.5주 | 1주 | 1주 | **2~3주** |

11 → 17이 가장 무거운 이유는 *Spring Boot 3.x*와 *jakarta 패키지 이주* 때문이다. 21 → 25는 *언어 변화가 거의 없으니* 가벼운 편이다.

이 견적을 *팀 외부에 보고할 때*는 ×1.5 보정해 보고하자. 마이그레이션은 늘 예상보다 길게 끈다 — *난감한* 의존성 하나가 한 주를 통째로 잡아먹곤 한다. 시간 여유를 두고 잡는 편이 낫다.

---

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

---

## 판권

**책 제목**: Modern Java Bible — Java 8에서 25까지, 그리고 그 너머
**저자**: Toby-AI
**버전**: 1.0.0
**발행일**: 2026-05-11
**언어**: 한국어
**라이선스**: CC BY-NC-SA 4.0 (저작자 표시 · 비상업적 이용 · 동일조건 변경허락 4.0 국제)
**라이선스 링크**: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko
**식별자**: modern-java-bible-v1.0.0
**제작 도구**: book-writer 하네스 v1.2.0

본 책은 Anthropic Claude(Opus 4.7)와 book-writer 하네스를 활용해 자동 저술되었습니다. 책의 내용은 Toby-AI가 책임집니다.

본 책은 Creative Commons BY-NC-SA 4.0 라이선스로 배포됩니다. 출처를 표시하고 비상업적 목적으로 자유롭게 공유 · 수정할 수 있으며, 파생물은 동일 라이선스로 배포해야 합니다.
