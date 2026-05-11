# Modern Java Bible — 저술 계획

**저술 계획 v2 — plan-reviewer 피드백 1차 반영본**

> 본 계획서는 `01_reference.md`(약 900줄, 8개 절·JEP 60+ 정리)와 `03_review_log.md`(plan-reviewer 라운드 1)를 토대로 갱신됐다.
> v1 대비 변경: 신설 챕터 3건(서론·19A 도구·20A 보안), 8장 분할(8A/8B), 부록 4종 명시, 분량 재배분으로 본문 약 306,500자(국판 720~780p), JLS 인용 체계화, 누락 JEP 18건 반영, 한국 사례 분산, 챕터별 고정 도메인 예제 지정.

---

## 1. 책 제목 후보

### 후보 A — **Modern Java Bible: Java 8에서 25까지, 그리고 그 너머** *(추천)*
- **톤:** 진중하고 권위 있는 레퍼런스. "Bible"의 무게값을 정직하게 받아들인다.
- **포지셔닝:** 책장에 꽂아두고 11년 치 자바 진화를 한 권으로 추적하는 항해 지도. Spring Boot 3 베이스라인을 가진 엔터프라이즈 개발자가 자기 코드베이스의 어느 지층까지 따라왔는지 확인하고 다음 한 발을 옮길 때 펴 보는 책.
- **부제 의도:** "그리고 그 너머"는 Valhalla·Leyden·Amber의 미래 챕터를 예고하며, 25가 종착점이 아니라 또 다른 출발점임을 시사한다.

### 후보 B — **모던 자바 통사: 함수형·데이터지향·동시성으로 다시 쓰는 자바**
- **톤:** 학술적이고 사관(史官)적인 시선. 변화의 이유와 인과 관계를 강조.
- **포지셔닝:** "어떤 JEP가 들어왔다"가 아니라 "왜 그 순서로 들어왔는가"를 묻는 책.
- **약점:** "통사"라는 단어가 일부 독자에게 어렵게 들릴 수 있다.

### 후보 C — **다시 쓰는 자바: Java 8 코드를 Java 25 코드로 옮기는 11년의 모든 것**
- **톤:** 실용적이고 손에 잡히는 마이그레이션 가이드.
- **포지셔닝:** "팀의 코드를 21·25로 옮겨야 한다"는 압박 아래 있는 리드 개발자에게 직진.
- **약점:** Bible의 망라성보다 마이그레이션이 전면에 나서 함수형·동시성의 깊이가 묻힌다.

**최종 추천: 후보 A.** B와 C의 강점은 각각 1장(통사적 도입)과 20장(마이그레이션 가이드)으로 흡수한다.

---

## 2. 책 특성

> ## v2 변경: 분량 목표를 본문 ~28만 자에서 **~306,500자**(국판 720~780p)로 상향. 부 도입·부록을 §7 합산에 포함. 무게 가중치 동시성 28%→25%로 약속 정직화, 데이터지향 18% 회복.

| 항목 | 값 | 비고 |
|------|------|------|
| 장르 | 레퍼런스 + 진화사 + 실무 가이드의 혼합 | "Effective Java"의 카드성 + "Real World Haskell"의 흐름 + "토비의 스프링"의 깊이 |
| 형식 | 서론 + 본문 25장(부 도입 10개 포함) + 부록 A·B·C·D | 부록도 책의 일부로 명시 |
| 분량 | **본문 약 306,500자 (국판 720~780p)** | 챕터당 평균 ~12,000자, 합산 검증은 §7 |
| 코드 비율 | **본문 : 코드 ≈ 7 : 3** (코드 약 4만 LOC) | ## v2 신설: Bible급 책의 관례 명시 |
| 난이도 | **중급~고급** | Java 8 람다·스트림은 가볍게 복습, JLS·JMM·Loom 내부 구현은 깊이 들어감 |
| 독자 진입 상태 | Spring Framework로 엔터프라이즈 앱을 만들지만, Java 8~11에 머물러 있고 records·sealed·virtual thread를 "들어는 봤다" 수준 | |
| 독자 출구 상태 | 자기 코드베이스가 Java 8 어디에 멈춰 있는지 진단하고, 21/25로 옮기는 길을 그릴 수 있다. 함수형·데이터지향·동시성 세 축에서 *왜* 그렇게 써야 하는지 JLS 수준으로 설명할 수 있다 | |

**책의 무게 중심 (분량 가중치, v2 갱신)**
- 함수형(Stream·Gatherers·Optional·Collector·람다·함수형 데이터 모델링): **약 21%**
- 데이터지향(records·sealed·pattern matching·ADT): **약 18%** (회복)
- 동시성(j.u.c·JMM·CompletableFuture·parallel stream·Flow·Virtual Thread·Structured Concurrency·Scoped Values): **약 25%** (정직화)
- 진화사·언어 표면(JPMS·var·switch·text blocks·sequenced collections·markdown javadoc·String Templates 좌초사): **약 13%**
- 성능·네이티브·도구·미래(GC·FFM·Vector·Class-File API·AOT/Leyden·Compact Headers·도구·Valhalla): **약 16%**
- 현장 적용(마이그레이션·보안·Spring 시너지): **약 7%**

---

## 3. 책 전체 구조 (10부 25장 + 서론 + 부록 4종)

> ## v2 변경: 신설 챕터 3건(서론, 19A 도구, 20A 보안), 8장을 8A·8B로 분할. 총 챕터 수 25개.

본 책은 **시간 순(LTS 축)과 주제 축의 더블 헬릭스 구조**다. 1·9·13·22장이 시간 축의 마디(8/17/21/25)를 짚어주며, 나머지가 횡단 주제를 깊이 판다.

| 부 | 챕터 | 메시지 | 부 도입 분량 |
|----|------|--------|------:|
| **서론** | (서론) | 왜 이 책인가, 왜 지금인가, 왜 Bible인가 | — |
| **Part I. 지형도 (Foundations)** | 1, 2 | 11년의 자바를 한눈에 — Modern Java가 무엇인지, 왜 그 순서로 바뀌었는지 | 1,500 |
| **Part II. 함수형 자바의 기초** | 3, 4 | 람다·함수형 인터페이스·`java.time`을 다시 — Java 8이 가져온 것의 진짜 의미 | 1,500 |
| **Part III. 스트림과 Optional의 모든 것** | 5, 6, 7 | Stream의 표면에서 Gatherers의 심부까지 — 11년에 걸친 함수형 데이터 파이프라인의 진화 | 1,500 |
| **Part IV. 동시성 I: Loom 이전** | 8A, 8B | JMM의 토대 위에 j.u.c·CompletableFuture·Flow — 우리가 알던 동시성의 한계 | 1,500 |
| **Part V. 언어 표면의 진화 (9~16)** | 9, 10 | JPMS·var·switch·text blocks·Sequenced Collections·Markdown Javadoc·String Templates 자정 | 1,500 |
| **Part VI. 데이터지향 자바 (Records · Sealed · Pattern)** | 11, 12, 13 | Java 17 LTS의 핵심 — records와 sealed가 ADT를 만들고, pattern matching이 그것을 풀어낸다 | 1,500 |
| **Part VII. 동시성 II: Loom 시대** | 14, 15, 16 | Virtual Thread·Structured Concurrency·Scoped Values — thread-per-request의 부활과 그 대가 | 1,500 |
| **Part VIII. 메모리·네이티브·성능·도구** | 17, 18, 19, 19A | GC·FFM/Vector·AOT/Leyden·Compact Headers + 도구 일습(JShell·JFR·jpackage·jlink·jextract) | 1,500 |
| **Part IX. 마이그레이션·보안·Spring 시너지** | 20, 20A, 21 | Java 8 → 21/25, 자바 보안의 11년, Spring Boot 3 시너지 | 1,500 |
| **Part X. 다음 자바** | 22 | Valhalla·Amber·Babylon·Leyden — 26 이후 우리가 마주할 것 | 1,500 |

**부록**
- 부록 A. **JEP 일람** — 60+ JEP를 버전·Project·표준화 시점으로 정렬 (8,000자)
- 부록 B. **JLS 인용 인덱스** — 본문에 나온 JLS 인용을 §·페이지·챕터 번호로 색인 (4,000자) ## v2 신설
- 부록 C. **마이그레이션 체크리스트** — 20장의 핵심을 1페이지로 (2,000자)
- 부록 D. **한 줄 요약 — Java 8 vs Java 25 코드 패턴 30선** — 책의 정체성 압축 (6,000자)

---

## 4. 챕터 목록 (서론 + 25장)

> ## v2 변경: 신설 3건, 분할 1건. 챕터별 분량 §7 표에 맞춰 갱신. 13장 14,500→17,000자, 14장 15,000→18,000자, 8장 17,000→분할 8A(11,000)+8B(10,000). 챕터마다 **고정 도메인 예제**를 v2에서 추가 명시 — 중복 회피.

---

### **서론. 왜 이 책인가**  ## v2 신설
- **핵심 질문:** 우리는 왜 *지금* 11년의 자바 진화를 한 권으로 묶어 읽어야 하는가?
- **주요 내용:**
  - 자바가 "변하지 않는 언어"라는 통념이 깨진 시점
  - Bible이라는 이름의 무게 — 망라성과 깊이의 약속
  - 이 책의 4가지 독해 경로 안내
- **예상 분량:** 2,000자
- **Toby 스타일:** 책 전체의 톤을 결정하는 자리. "11년 전 람다를 처음 만났을 때를 기억하는가" 같은 회상 어조로 출발.

---

### **Part I. 지형도 (Foundations)**

#### 1장. 11년의 자바, 한 장의 지도
- **핵심 질문:** 우리는 지금 자바의 어디쯤에 와 있는가?
- **주요 내용:**
  - Java 8(2014)부터 Java 25(2025)까지 11년의 압축 연대기
  - LTS(8/11/17/21/25)와 6개월 케이던스의 의미 — Mark Reinhold의 *Moving Java Forward Faster*
  - "Modern Java"의 두 얼굴 — 언어 패러다임 확장 + 릴리스 모델 전환
  - 한국 엔터프라이즈의 실제 분포 (8 잔존 → 17 정착 → 21 도입의 흐름) ## v2: 한국 사례를 §6 표에서 다른 챕터에도 분산
  - 이 책이 다루는 범위와 읽는 방법
- **다룰 JEP:** 없음 (메타 챕터)
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring Boot 베이스라인의 시계열 (Boot 2.x = Java 8/11, Boot 3.x = Java 17, Boot 3.2 = Java 21)
- **고정 도메인 예제:** ## v2 신설 — *가상의 결제 SaaS 회사 "PayBridge"의 11년 코드베이스 변천*. 이 도메인이 1·20·22장에서 수미상관으로 회수됨.
- **예상 분량:** 11,000자 (v1 10,000 → v2 11,000) ## v2 변경: Sequenced Collections·HttpClient 등 추가 항목 흡수

#### 2장. 왜 이렇게 됐을까 — Modern Java의 다섯 가지 동력
- **핵심 질문:** 람다·records·virtual thread는 왜 *이 순서로* 들어왔는가?
- **주요 내용:**
  - 다섯 동력: 함수형 패러다임 / 데이터지향 / Loom(동시성) / Panama(네이티브) / Leyden(시작시간)
  - 각 동력의 발원 — Project Lambda, Amber, Loom, Panama, Valhalla
  - Brian Goetz의 *Data-Oriented Programming in Java*가 그리는 큰 그림
  - "자바가 변하지 않는다"는 통념이 깨진 시점
  - 이 다섯 동력이 책의 부(Part) 구조로 어떻게 이어지는지
- **다룰 JEP:** 메타 — 각 Project의 대표 JEP를 한 줄씩만 호명
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring 6/Boot 3의 설계 결정(records DTO, virtual thread executor, AOT)이 이 동력들에서 어떻게 파생됐는지
- **고정 도메인 예제:** 같은 도메인 — 주문 처리 — 을 Java 8 스타일과 Java 25 스타일로 한 페이지씩 나란히 보여주는 "프리뷰". *이 예제는 22장 결말과 수미상관*.
- **예상 분량:** 11,000자

---

### **Part II. 함수형 자바의 기초**

#### 3장. 람다와 함수형 인터페이스 — 그 익숙함의 진짜 의미
- **핵심 질문:** 람다는 단지 익명 클래스의 문법 설탕인가?
- **주요 내용:**
  - JSR 335 — 람다 표현식의 스펙
  - `Function`, `Predicate`, `Supplier`, `Consumer`, `BiFunction`의 합성
  - 메서드 참조 네 가지 (static, instance-bound, unbound, constructor)
  - target type과 inference
  - effectively final의 정확한 의미
  - 인터페이스 default·static 메서드 — 라이브러리 진화의 새 도구
  - **Java 8 vs Java 25 비교:** `Collections.sort` → `comparing().thenComparing()`
- **다룰 JEP:** JSR 335, JEP 126(default/static methods)
- **JLS 인용:** ## v2 명시 — **§15.27** (Lambda Expressions, effectively final 정의 원문)
- **Spring/JPA 연결:** Spring의 `@FunctionalInterface` 활용 — `BeanPostProcessor`, `RowMapper`, `WebClient.exchangeToMono`
- **고정 도메인 예제:** *상품 카탈로그* 정렬·필터링 — 5·6장은 다른 도메인 사용
- **예상 분량:** 13,500자

#### 4장. `java.time`과 종종 잊히는 Java 8의 보석들
- **핵심 질문:** 우리는 정말 `Date`·`Calendar`에서 벗어났는가?
- **주요 내용:**
  - JSR-310 — Stephen Colebourne이 그린 시간 모델
  - `Instant`·`LocalDate`·`ZonedDateTime`·`Duration`·`Period`
  - `Date`·`Calendar`·`Joda-Time`에서 옮겨오는 패턴
  - 인터페이스 default 메서드의 두 얼굴
  - `Map`의 새 메서드들 — `getOrDefault`, `computeIfAbsent`, `merge`, `replaceAll`
  - **Java 8 vs Java 25 비교:** 오래된 `Calendar` 로직을 `java.time`으로
- **다룰 JEP:** JSR-310
- **JLS 인용:** 없음 (API addition)
- **Spring/JPA 연결:** JPA AttributeConverter로 `LocalDate`·`Instant` 매핑, Hibernate 6의 `java.time` 우선 지원
- **고정 도메인 예제:** *결제 정산 시간대* — 한국·미국·UTC가 섞인 도메인
- **예상 분량:** 11,000자

---

### **Part III. 스트림과 Optional의 모든 것**

#### 5장. Stream API — 선언적 데이터 파이프라인의 해부
- **핵심 질문:** Stream은 정확히 무엇이고, 무엇이 아닌가?
- **주요 내용:**
  - Stream의 정체 — Spliterator 위의 lazy pipeline
  - intermediate vs terminal, stateful vs stateless
  - Java 9의 `takeWhile`, `dropWhile`, `iterate`
  - Java 16의 `Stream::toList`
  - Stream을 *오용*하는 패턴 — side effect 남발, `peek` 디버깅, `forEach`로 상태 변경
  - JLS의 stream contract — encounter order, non-interference, statelessness
- **다룰 JEP:** JEP 107, JEP 269
- **JLS 인용:** ## v2 명시 — `java.util.stream` 패키지 문서 (non-interference, side-effects 정의)
- **Spring/JPA 연결:** JPA `Stream<T>` 쿼리의 fetch size·트랜잭션 경계 함정
- **고정 도메인 예제:** *주문 목록 통계 집계* — for-loop → Stream 옮길 때 만나는 4가지 함정
- **예상 분량:** 14,500자

#### 6장. Collector·Reducer·Gatherer — Stream의 종착과 새 중간 정거장
- **핵심 질문:** `collect`는 마법인가, 아니면 우리가 직접 만들 수 있는가?
- **주요 내용:**
  - `Collectors`의 표면 — `toList`, `toMap`, `groupingBy`, `partitioningBy`, `joining`
  - **downstream collector**의 합성
  - 직접 `Collector` 구현 — 5요소 (`supplier`, `accumulator`, `combiner`, `finisher`, `characteristics`)
  - `reduce`의 세 가지 시그니처와 identity·associativity의 의미
  - **Stream Gatherers (JEP 461 → 473 → 485):** 1:1, 1:N, N:1, N:N
  - 내장 gatherer 5종: `fold`, `scan`, `windowFixed`, `windowSliding`, `mapConcurrent`
  - 직접 Gatherer 구현 — `initializer`, `integrator`, `combiner`, `finisher`
  - ## v2 신설 절 — **"함수형 관점: fold·monad·composition"** (2,500자)
    - `reduce`의 monoid 속성 — identity·associativity가 parallel safety의 수학적 기반인 이유
    - Collector의 5요소가 *fold의 일반화*임을 짚기
    - `flatMap`의 monad 의미 — Optional·Stream·CompletableFuture에서 같은 형식인 이유
    - Gatherer가 *함수형 transformer*로 합성 가능함을 코드 한 페이지로
  - **Java 8 vs Java 24 비교:** 슬라이딩 윈도우 이동 평균
- **다룰 JEP:** JEP 461, 473, 485
- **JLS 인용:** 없음 (API)
- **Spring/JPA 연결:** 배치 insert의 fixed-window grouping(`windowFixed(1000)`)으로 JDBC batch size 자동 정합
- **고정 도메인 예제:** *결제 트랜잭션 5분 이동 평균* + *rate-limited 외부 API 호출*
- **예상 분량:** 18,500자 (v1 16,000 → v2 18,500) ## v2 변경: 함수형 깊이 절 추가

#### 7장. `Optional<T>` — 약속과 함정
- **핵심 질문:** Optional을 *제대로* 쓰고 있는가?
- **주요 내용:**
  - 도입 의도 — null의 명시화, *반환값* 한정 사용
  - `map`, `flatMap`, `filter`, `or`, `orElse`, `orElseGet`, `orElseThrow`의 정확한 의미
  - `ifPresent`, Java 9의 `ifPresentOrElse`, `stream()`
  - **하지 말 것:** 필드, 매개변수, `Optional<List<T>>`, `Optional.of(null)` 오해
  - ## v2 신설 절 — **"Optional의 monad 색채"** — `flatMap`이 6장과 같은 형식임을 회수, 함수형 패러다임의 일관성 강조
  - **Java 8 vs Java 25 비교:** Optional의 모범 사용과 안티패턴 6가지
- **다룰 JEP:** API addition
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring Data Repository의 `Optional<Entity>` 반환과 트랜잭션 readOnly 조합
- **고정 도메인 예제:** *User → Address → City → ZipCode* 깊은 탐색 — null-check 지옥에서 flatMap 체인으로
- **예상 분량:** 11,500자 (v1 9,500 → v2 11,500) ## v2 변경: monad 색채 절 추가

---

### **Part IV. 동시성 I — Loom 이전의 모든 것**

> ## v2 변경: 8장을 8A·8B로 분할. JMM이 너무 무거워서 한 챕터에 묶이면 맥이 끊긴다는 리뷰 반영.

#### 8A장. j.u.c와 Java Memory Model — 동시성의 토대  ## v2 신설(분할)
- **핵심 질문:** 우리가 매일 쓰던 `synchronized`·`volatile`은 정확히 무엇을 보장하는가?
- **주요 내용:**
  - JSR 133 — Java Memory Model의 핵심 (Manson·Pugh, 2004)
  - **happens-before** 정확한 정의 — *JSR-133 원문 박스 인용* ## v2 명시
  - volatile read/write, monitor enter/exit, `Thread.start`/`join`, final field semantics
  - "out-of-thin-air" 문제와 well-formed execution
  - `java.util.concurrent`의 지형 — `ExecutorService`, `Future`, `BlockingQueue`, `CountDownLatch`, `Phaser`, `Semaphore`
  - `Fork/Join` 풀과 work-stealing — `RecursiveTask`, `commonPool`의 정체
  - **`parallelStream()`의 함정** — commonPool 컨텐션, blocking I/O 금기, 예측 불가 latency
- **다룰 JEP:** 없음 (JLS·JSR 중심)
- **JLS 인용:** ## v2 명시 — **§17.4** (Memory Model), **§17.5** (final field semantics). JSR-133 PDF 원문을 박스에 한 페이지 인용.
- **Spring/JPA 연결:** `@Transactional` 메서드의 가시성 보장, JPA 1차 캐시의 thread-confinement
- **고정 도메인 예제:** *재고 차감 race condition* — JMM이 무엇을 보장하고 무엇을 안 보장하는지
- **예상 분량:** 11,000자

#### 8B장. CompletableFuture와 Reactive Streams Flow — 비동기 조합의 두 갈래  ## v2 신설(분할)
- **핵심 질문:** 콜백 지옥에서 어떻게 빠져나왔고, 그 다음은 무엇이었나?
- **주요 내용:**
  - `CompletableFuture`의 50개+ 메서드 정리 — `thenApply` vs `thenCompose` vs `thenCombine`
  - 예외 전파 — `handle`, `exceptionally`, `whenComplete`의 차이
  - Executor 지정과 안 함의 의미 — `commonPool` 함정 재방문
  - Java 9 `java.util.concurrent.Flow` — Reactive Streams 인터페이스 표준
  - Reactor·RxJava와 Flow의 관계
  - backpressure의 정확한 의미와 four signals (`onSubscribe`, `onNext`, `onError`, `onComplete`)
  - **이 챕터는 21장 Reactive 시나리오의 토대** ## v2 명시 — 21장에서 다시 회수
- **다룰 JEP:** JEP 266(Reactive Streams Flow)
- **JLS 인용:** 없음
- **Spring/JPA 연결:** `@Async` + `CompletableFuture` 패턴, WebFlux의 `Mono`/`Flux`가 Flow와 어떻게 다른지
- **고정 도메인 예제:** *외부 결제 게이트웨이 3개 병렬 호출* — ExecutorService → CompletableFuture → Flow로 3번 리팩토링
- **예상 분량:** 10,000자

---

### **Part V. 언어 표면의 진화 (Java 9 ~ Java 23)**

#### 9장. JPMS — 실패인가 미완인가
- **핵심 질문:** 왜 우리는 `module-info.java`를 쓰지 않게 됐는가?
- **주요 내용:**
  - Project Jigsaw의 의도 — JAR Hell, strong encapsulation, `jlink`
  - `requires`, `exports`, `opens`, `uses`, `provides`의 의미론
  - 자동 모듈 vs 명시 모듈 vs classpath 혼합의 가시성 규칙
  - 2017년 JCP EC 부결 사건과 OSGi 진영의 반대
  - **현재 상태:** "ignored at app level, but essential at JDK level"
  - **JEP 511 Module Import Declarations (Java 25):** `import module java.base;` ## v2 명시
  - Spring이 modular jar로 가지 않은 이유
- **다룰 JEP:** JEP 200, 201, 220, 261, 494, 511
- **JLS 인용:** **§7.7** (Module Declarations)
- **Spring/JPA 연결:** Spring Boot 3의 fat jar 구조, GraalVM native image가 JPMS 없이 trimming하는 방법
- **고정 도메인 예제:** *내부 도메인 라이브러리 한 개*를 modular jar로 만들고 자동 모듈로 쓰일 때의 차이
- **예상 분량:** 11,000자

#### 10장. `var`·switch·text blocks·Sequenced Collections — 작지만 결정적인 변화
- **핵심 질문:** 작은 문법 변화가 어떻게 코드 베이스의 색깔을 바꾸는가?
- **주요 내용:**
  - **`var` (Java 10, JEP 286):** 정확한 적용 범위와 OpenJDK Amber LVTI Style Guide
  - var가 어울리는 5가지 자리, 어울리지 않는 5가지 자리
  - **Switch Expression (Java 14, JEP 361):** statement → expression, `case L ->`, `yield`
  - **Text Blocks (Java 15, JEP 378):** 삼중 따옴표, incidental whitespace, `\` line continuation
  - SQL·JSON·HTML 임베드 패턴
  - **Helpful NullPointerExceptions (Java 14, JEP 358)**
  - ## v2 신설 — **Sequenced Collections (Java 21, JEP 431)**: `SequencedCollection`, `SequencedSet`, `SequencedMap` — "들어왔는데 잘 모르는" 것의 대표 사례
  - ## v2 신설 — **Markdown Documentation Comments (Java 23, JEP 467)**: `///` 코멘트
  - ## v2 신설 — **JEP 458/512: Compact Source Files + Instance Main Methods** — `void main()` 단독 실행
  - ## v2 신설 — **String Templates 좌초사 (JEP 430·459 → Java 23 철회)**: "preview 단계의 자정" 메타 메시지로 한 절
  - **Java 8 vs Java 21 비교:** 같은 함수의 표면 변화
- **다룰 JEP:** JEP 286, 323, 325, 354, 361, 358, 355, 378, 431, 458, 467, 512, 430(좌초), 459(좌초)
- **JLS 인용:** ## v2 명시 — **§14.4** (LVTI), **§14.11** (switch), **§15.28** (switch expression), **§3.10.6** (text blocks - incidental whitespace 알고리즘 원문 박스)
- **Spring/JPA 연결:** `@Query` 어노테이션 안의 JPQL을 text block으로, Spring config의 가독성
- **고정 도메인 예제:** *한 컨트롤러 메서드*를 Java 8 스타일에서 Java 21 스타일로 옮기며 7가지 표면 변화 적용
- **예상 분량:** 14,500자 (v1 12,500 → v2 14,500) ## v2 변경: Sequenced·Markdown·Compact Source·String Templates 자정 흡수

---

### **Part VI. 데이터지향 자바 — Records · Sealed · Pattern**

#### 11장. Records — 자바가 마침내 인정한 "데이터의 신원"
- **핵심 질문:** Records는 Lombok의 대체인가, 다른 것인가?
- **주요 내용:**
  - JEP 359(14 preview) → 395(16 standard)
  - 컴포넌트·canonical constructor·compact constructor·accessor·`equals`/`hashCode`/`toString` 자동
  - **Records가 안 되는 것:** `extends`, mutable field, JPA Entity
  - **Records vs Lombok:** Brian Goetz의 입장 — Records는 *대체*가 아니라 *신원*
  - ## v2 신설 — **Lombok의 잔존 영역**: `@Slf4j`, `@SneakyThrows`, `@Accessors`는 records가 대체 못 함. mutable Entity, builder 패턴, JPA에서 Lombok이 계속 필요한 이유
  - ## v2 신설 — **Flexible Constructor Bodies (JEP 482/513, Java 23→25 표준)**: `super()/this()` 첫 statement 룰의 종말, records의 compact constructor와 결합
  - 직렬화·역직렬화(Jackson, JPA AttributeConverter, Spring `@ConfigurationProperties`)
  - "왜 records가 14에 preview, 16에 표준이었는가" 진화 박스 ## v2 신설
  - **Java 8 vs Java 21 비교:** DTO 한 개의 변천사 — Lombok `@Value` → record
- **다룰 JEP:** JEP 359, 384, 395, 482, 513
- **JLS 인용:** ## v2 명시 — **§8.10** (Record Classes 원문 박스)
- **Spring/JPA 연결:** Spring Data interface projection vs class projection vs record projection, `@ConfigurationProperties`의 records 친화성
- **고정 도메인 예제:** *주문 시스템의 OrderRequest/Response/Event를 records로* — 13·21장과 도메인 분리
- **예상 분량:** 12,000자

#### 12장. Sealed Classes — 합 타입(Sum Type)이 자바에 들어온 날
- **핵심 질문:** Sealed가 도입되기 전 우리는 무엇을 못 했나?
- **주요 내용:**
  - JEP 360(15 preview) → 409(17 standard)
  - Sub-type의 세 선택지 — `final`, `sealed`, `non-sealed`
  - 같은 모듈/같은 패키지 제약
  - **이것은 ADT의 sum type이다** — 함수형 언어에서 자바로 건너온 개념
  - ## v2 신설/강화 — **Visitor 패턴과의 코드 길이 비교**: 같은 도메인을 Visitor와 sealed로 양쪽 다 구현해 *줄 수와 가독성 측정*
  - 도메인 모델링 사례
- **다룰 JEP:** JEP 360, 397, 409
- **JLS 인용:** ## v2 명시 — **§8.1.1.2** (sealed, permits 원문 박스)
- **Spring/JPA 연결:** 도메인 이벤트(`sealed interface UserEvent permits Created, Updated, Deleted`)의 Spring `ApplicationEventPublisher` 발행
- **고정 도메인 예제:** *결제 상태 모델 (PaymentResult permits Approved, Declined, Pending)* — Visitor 코드와 sealed 코드의 길이 비교 사례
- **예상 분량:** 12,000자 (v1 10,500 → v2 12,000) ## v2 변경: Visitor 코드 길이 비교 절 추가

#### 13장. Pattern Matching — ADT를 풀어내는 도구
- **핵심 질문:** 패턴 매칭이 들어오자 무엇이 가능해졌는가?
- **주요 내용:**
  - JEP 394(16 instanceof) → 441(21 switch) → 440(21 record patterns)
  - guard — `case Point p when p.x() > 0 -> ...`
  - Record deconstruction — `case Point(int x, int y) -> ...`
  - 중첩 deconstruction
  - Java 22의 unnamed pattern `_` (JEP 456)
  - **Records + Sealed + Pattern = ADT 삼위일체** — 세 가지 본격 예제로 다지기 ## v2 강화
    - 예제 1: 표현식 평가기 (Expr / Num / Add / Mul) — 교과서적
    - 예제 2: HTTP `sealed Result<T, E> permits Ok, Err` — 현실 도메인
    - 예제 3: Workflow state machine — `sealed interface OrderState permits Pending, Paid, Shipped, Delivered, Cancelled`
  - ## v2 강화 — preview 진화사(305→394→406→420→427→432→433→441)는 *연표 박스*로 압축, 본문은 21 표준 + 22 unnamed에 집중
  - **Visitor 패턴의 사망 신고서** — Visitor 한 줄 한 줄을 ADT로 옮기는 4페이지 대비 예제 ## v2 강화
  - Brian Goetz의 *Data-Oriented Programming in Java*에서 핵심 문단 정확한 인용 ## v2 명시
  - **Java 8 vs Java 21 비교:** 한 도메인 결과 처리 — instanceof 캐스트 사다리 → pattern matching switch
  - ## v2 신설 — *호 ②와 호 ③의 다리*: 챕터 마지막 1페이지에 "이제 ADT로 도메인을 모델링했으니, 그 도메인 위에서 동시성을 다시 생각해보자"의 14장 예고 문단
- **다룰 JEP:** JEP 305, 394, 406, 420, 427, 432, 433, 440, 441, 456 (단, 본문 깊이는 16·21·22·456에 집중, 나머지는 연표)
- **JLS 인용:** ## v2 명시 — **§14.30** (Patterns 정의), **§14.30.3** (switch exhaustiveness 원문 박스)
- **Spring/JPA 연결:** API 응답의 `sealed Result<T, E>` 패턴, 도메인 이벤트 핸들러의 exhaustive switch
- **고정 도메인 예제:** *산술 표현식 평가기 + HTTP Result + Workflow 상태기계* — 11·21장과 도메인 분리
- **예상 분량:** 17,000자 (v1 14,500 → v2 17,000) ## v2 변경: Bible 미학적 클라이맥스로 분량 확장, 현실 도메인 예제 2개 추가

---

### **Part VII. 동시성 II — Loom 시대**

#### 14장. Virtual Threads — thread-per-request의 부활
- **핵심 질문:** "Reactive 없이도 충분히 빠르다"는 약속은 진짜인가?
- **주요 내용:**
  - Project Loom의 동기 — OS thread의 비용, I/O-bound 워크로드의 idle 점유
  - JEP 425(19 preview) → 444(21 standard)
  - JEP 444 원문 인용 — "virtual thread는 OS thread에 묶이지 않은 Thread 인스턴스"
  - ## v2 강화 — **M:N 스케줄링의 internals**: continuation 개념, ForkJoinPool carrier, mount/unmount의 실제 바이트코드 흐름, `Continuation`·`ContinuationScope`
  - 모든 virtual thread는 daemon, priority 무시, 단일 thread group
  - Brian Goetz의 "virtual memory의 비유"
  - **vs goroutine·async/await·green thread** — 통신 모델·호환성 비교 표
  - ## v2 신설 — 챕터 도입 1페이지가 *13장 회수*: sealed `Result<T,E>`를 virtual thread 결과 처리에 쓰는 한 페이지 예제
  - 성능: SoftwareMill 벤치마크, Cashfree Payments의 production 사례
  - 한국 사례: 우아한형제들·카카오 세미나 인용 ## v2 명시
- **다룰 JEP:** JEP 425, 436, 444
- **JLS 인용:** JEP 444 원문 박스, JLS의 thread 정의(§17.1) 참조
- **Spring/JPA 연결:** `spring.threads.virtual.enabled=true`는 *간략 호명*만 (21장에서 본격 다룸) ## v2 변경: 중복 회피
- **고정 도메인 예제:** *API 서버의 외부 호출 fan-out* — 21장(결제 마이크로서비스)과 도메인 분리
- **예상 분량:** 18,000자 (v1 15,000 → v2 18,000) ## v2 변경: M:N internals 추가

#### 15장. Pinning · ThreadLocal · 함정들 — Virtual Thread가 우리를 실망시키는 자리
- **핵심 질문:** Virtual Thread를 켜기만 하면 모든 게 빨라지는가?
- **주요 내용:**
  - **Pinning이란:** virtual thread가 unmount 못 하는 상황
  - Java 21~23의 `synchronized` pinning — 30년 묵은 JVM 모니터의 OS thread 신원 추적
  - HikariCP·Caffeine·Apache HttpClient·MySQL Connector/J의 이주
  - Netflix의 production deadlock 사례 ## v2 보강: 공식 post-mortem 확인 후 인용
  - **JEP 491 (Java 24):** JVM 모니터가 virtual thread 신원을 추적
  - **ThreadLocal 함정:** 수백만 virtual thread × ThreadLocal 캐시 = 메모리 폭발
  - **모니터링:** `-Djdk.tracePinnedThreads=full`, JFR `jdk.VirtualThreadPinned` 이벤트
  - **CPU-bound 작업에 쓰지 말 것**
  - 한국 사례: 카카오페이의 platform → virtual 전환 측정 인용 ## v2 명시
- **다룰 JEP:** JEP 491
- **JLS 인용:** 없음
- **Spring/JPA 연결:** JDBC 드라이버별 Loom-ready 상태, Spring Boot 3.4 + JDK 24의 `synchronized` 안전성
- **고정 도메인 예제:** *세션 관리 (ThreadLocal SessionContext)의 폭발 사례 + Connection pool pinning 진단*
- **예상 분량:** 12,000자

#### 16장. Structured Concurrency와 Scoped Values — concurrent 코드의 문법
- **핵심 질문:** 동시성에도 *구조*가 있을 수 있는가?
- **주요 내용:**
  - Dijkstra의 *Notes on Structured Programming* 재해석
  - `StructuredTaskScope` — 자식 task를 단일 단위로 묶기
  - ## v2 강화 — **정책 3종을 코드 예제로 모두**: `ShutdownOnFailure`, `ShutdownOnSuccess`, 커스텀 `Joiner`
  - 부모 함수가 반환되기 전 자식이 모두 끝남 — cancellation propagation
  - **Scoped Values (JEP 506, Java 25 표준):** ThreadLocal의 후계자
  - immutable, 부모→자식 binding, 자동 cleanup
  - ## v2 강화 — **ScopedValue rebinding semantics**: `where().run()`의 동적 scope와 정적 scope의 차이
  - **Java 8 ExecutorService vs Java 25 StructuredTaskScope 비교**
  - JEP 453 → 462 → 480 → 499 → 505 → 533까지의 preview 흐름과 그 의미
- **다룰 JEP:** JEP 428, 437, 453, 462, 480, 499, 505, 533, 429, 446, 487, 506
- **JLS 인용:** JEP 506 원문 박스
- **Spring/JPA 연결:** request-scoped 데이터 전달 — Spring의 `RequestContextHolder`(ThreadLocal 기반)에서 Scoped Value로의 이주 검토
- **고정 도메인 예제:** *사용자 인증 컨텍스트 (userId, tenantId) fan-out* — 15장(세션 ThreadLocal)과 도메인 연속, 그러나 도구는 ScopedValue·StructuredTaskScope
- **예상 분량:** 15,000자 (v1 12,500 → v2 15,000) ## v2 변경: 정책 3종 + rebinding semantics 추가

---

### **Part VIII. 메모리 · 네이티브 · 성능 · 도구**

#### 17장. GC 11년의 진화 — Serial부터 Generational Shenandoah까지
- **핵심 질문:** 우리 서비스는 어떤 GC를 써야 하는가?
- **주요 내용:**
  - GC 9종의 지형 — Serial, Parallel, CMS(사망), G1, ZGC, Generational ZGC, Shenandoah, Generational Shenandoah, Epsilon
  - 각 GC의 메커니즘 — region-based, colored pointer, concurrent compaction
  - **JEP 333(11 ZGC) → JEP 377(15 production) → JEP 439(21 generational) → JEP 474(23 default)**
  - JEP 521 — Generational Shenandoah (Java 25)
  - 선택 가이드 — heap 크기, p99 latency 요구, 컨테이너 환경, JDK 버전
  - ## v2 신설 — **PermGen → Metaspace 전환의 영향**: Docker RSS 증가의 직접 원인, CleverTap 사례
  - ## v2 신설 — **벤치마크 박스 3종**: JFokus·Devoxx·JavaOne 발표 슬라이드에서 추출한 실측 표 (Netflix·Pinterest·LinkedIn의 ZGC 사례)
  - Kubernetes pod 메모리 limit과 ZGC/Shenandoah의 off-heap 메타데이터 함정
  - ## v2 신설 — **"메모리의 두 얼굴" 다리 문단**: 8A장의 JMM과 이 챕터의 GC를 연결, 한 페이지로
- **다룰 JEP:** JEP 248(G1 default), 318(Epsilon), 333, 377, 379, 376, 423, 439, 474, 521
- **JLS 인용:** 없음 (구현 영역)
- **Spring/JPA 연결:** Spring Boot 컨테이너의 GC 튜닝, JFR로 GC pause 진단
- **고정 도메인 예제:** *세 워크로드* — REST API(2GB heap, k8s) vs 캐시 서버(50GB heap) vs 배치 잡
- **예상 분량:** 12,000자

#### 18장. Foreign Function & Memory API · Vector API · Class-File API
- **핵심 질문:** JNI는 정말 끝났는가? 자바는 SIMD를 어떻게 표현하는가? ASM은 무엇으로 대체되는가?
- **주요 내용:**
  - **FFM (JEP 442 → 454, Java 22 표준화):** `MemorySegment`, `Arena`, `Linker`, `jextract`
  - JNI의 한계
  - `Arena.ofConfined()`, `Arena.ofShared()`, `Arena.ofAuto()`
  - **Vector API (JEP 338 → 489):** AVX2/AVX-512/NEON/SVE 자동 매핑
  - Valhalla 대기 — value class 도입 전까지 incubator
  - ## v2 신설 — **Class-File API (JEP 466 → 484, Java 24 표준)**: ASM·BCEL을 대체하는 1급 API, Spring AOT·Hibernate가 직접 영향받음
  - Project Panama의 야망 — GPU·SIMD·DPDK·ML inference
- **다룰 JEP:** JEP 412, 442, 454, 338, 414, 489, 466, 484
- **JLS 인용:** 없음 (API)
- **Spring/JPA 연결:** 암호화 라이브러리·이미지 처리·ML 모델 추론을 네이티브로 호출, Spring AOT의 Class-File API 활용
- **고정 도메인 예제:** *기존 JNI C 라이브러리를 jextract + FFM으로 갈아끼우기* + *바이트코드 변환을 ASM에서 Class-File API로*
- **예상 분량:** 11,000자

#### 19장. AOT · Leyden · Compact Object Headers — 시작 시간과 메모리의 새 풍경
- **핵심 질문:** GraalVM 없이도 빠른 자바가 가능한가?
- **주요 내용:**
  - **AppCDS(10) → Dynamic CDS(13) → JEP 483 AOT Class Loading & Linking(24) → JEP 514·515(25)**
  - Project Leyden의 premain branch
  - ## v2 강화 — **GraalVM Native Image의 정확한 정체**: closed-world, reachability metadata, reflection 제약
  - ## v2 강화 — **GraalVM vs JDK AOT 비교 절**: 어디서 무엇을 선택, 트레이드오프
  - Spring Boot 3.3+의 CDS 통합 — training run, cache artifact
  - Spring Petclinic 사례 — startup 36~42% 단축
  - **JEP 519 Compact Object Headers (Java 25):** 96~128비트 → 64비트
  - 캐시 라인 효율, heap 10~22% 감소, CPU 절감 30% 보고
  - 적용 가이드 — 어디서 켜고 어디서 끄는가
- **다룰 JEP:** JEP 310, 350, 483, 514, 515, 519
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring Boot 3.3 CDS, Spring Data AOT Repositories, AWS Lambda·Cloud Run에서의 콜드 스타트
- **고정 도메인 예제:** *Spring Boot 앱 startup 측정* — Baseline → CDS → AOT → Compact Headers 단계별 효과
- **예상 분량:** 10,500자

#### 19A장. Modern Java의 도구들 — JShell부터 jextract까지  ## v2 신설
- **핵심 질문:** 우리가 손에 쥐고 있는 도구들이 11년 사이 얼마나 늘었는가?
- **주요 내용:**
  - **JShell** (Java 9, JEP 222): Spring REPL, JPA 쿼리 디버깅 활용
  - **jpackage** (Java 16, JEP 343): native installer 생성
  - **jlink**: slim JRE
  - **jwebserver** (Java 18, JEP 408): 로컬 개발용 간단 HTTP 서버
  - **jextract**: C header → Java binding (18장의 FFM 전제)
  - **JFR + JMC** (Java 11+, 오픈소스): production-grade profiling — virtual thread pinning 진단의 *실전 시연*
  - **빌드 도구의 자바 호환**: Maven 3.6.3+/Gradle 7.3+, toolchain plugin, foojay-resolver, Maven/Gradle Wrapper
  - **JUnit 5와 Modern Java**: records 친화 테스트, sealed exhaustiveness 테스트, virtual thread를 위한 `@Timeout`
- **다룰 JEP:** JEP 222, 343, 408, 467(이미 10장), 477
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring Boot의 Maven/Gradle plugin이 Java 17·21·25를 어떻게 인식하고 빌드하는가
- **고정 도메인 예제:** *PayBridge 회사의 CI 파이프라인* — Java 8 빌드에서 Java 21 빌드로의 도구 일습 변천
- **예상 분량:** 8,000자

---

### **Part IX. 마이그레이션 · 보안 · Spring 시너지**

#### 20장. Java 8 → 17 마이그레이션 — 현장의 함정과 권장 순서
- **핵심 질문:** 멈춰 있는 코드베이스를 어디서부터 손대야 하는가?
- **주요 내용:**
  - JEP 320(11) — JAXB·JAX-WS·CORBA·`javax.annotation` 제거의 충격
  - Strong encapsulation — `sun.misc.Unsafe`, `--add-opens`, `--add-exports`
  - Nashorn 제거(15) → GraalVM JS 이주
  - ## v2 신설 — **SecurityManager의 deprecation** (JEP 411, Java 17) → **제거** (JEP 486, Java 24): 엔터프라이즈 마이그레이션의 큰 함정
  - ## v2 신설 — **`HttpClient` (Java 11, JEP 321) 표준화**: WebClient·RestTemplate과의 비교, virtual thread + HttpClient 시너지 (21장에서 본격)
  - Docker RSS 증가
  - 빌드 도구 절은 19A장으로 ## v2 변경: 중복 회피
  - Spring Boot 2.7 → 3.0 — `javax.*` → `jakarta.*` namespace rename
  - **권장 순서 6단계**
  - 한국 SI/금융권의 8 → 17 이주 사례 ## v2 보강 명시 (리서치 보강 필요)
  - CleverTap·Aviator·Systematic 사례 인용
- **다룰 JEP:** JEP 320, 396, 403, 372, 411, 486, 321
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring Boot 3.0 jakarta namespace, Hibernate 6, Tomcat 10
- **고정 도메인 예제:** *PayBridge 회사의 4주 마이그레이션 일정* — 1장과 수미상관
- **예상 분량:** 14,500자 (v1 12,500 → v2 14,500) ## v2 변경: SecurityManager·HttpClient·한국 사례 추가

#### 20A장. 자바 보안의 11년 변화  ## v2 신설
- **핵심 질문:** Spring Security와 결을 맞추려면 자바 보안 모델의 변화를 어디까지 알아야 하는가?
- **주요 내용:**
  - `SecurityManager`의 deprecation → 제거의 전사: 왜 30년 묵은 모델이 끝났는가
  - **JEP 452 KEM API (Java 21):** Key Encapsulation Mechanism — post-quantum 대응의 첫 단추
  - **JEP 478 KDF API Preview (Java 24) → JEP 510 표준 (Java 25):** Key Derivation Function
  - TLS 1.3, **EdDSA (JEP 339, Java 15)**
  - 인증서 처리·암호 라이브러리의 변화
  - sealed for invariant — 보안 도메인에서 sealed의 가치
  - Spring Security 6의 Modern Java 패턴
- **다룰 JEP:** JEP 411, 486, 452, 478, 510, 339
- **JLS 인용:** 없음
- **Spring/JPA 연결:** Spring Security 6의 records 기반 Authentication, OAuth2 token에 sealed 적용
- **고정 도메인 예제:** *결제 토큰화*에서 KDF·KEM이 어떻게 들어가는가
- **예상 분량:** 6,000자

#### 21장. Spring Boot 3.x × Java 21/25 — 시너지의 *고유성*
- **핵심 질문:** Spring과 Modern Java는 어디서 가장 잘 *맞물리는가*? — 단순 종합이 아닌 Spring 고유의 패턴
- **주요 내용:** ## v2 대폭 개편 — 재탕 위험 회피, Spring 고유성에 집중
  - **Spring Data Repositories의 records projection의 미세 동작**: interface projection과 다른 점, Spring Data AOT Repositories의 빌드 타임 코드 생성
  - **`@ConfigurationProperties` + records의 immutable config 패턴**과 `@RefreshScope`의 충돌
  - **Spring 6의 `RestClient` (6.1 신규)** — RestTemplate·WebClient·HttpClient(Java 11)와 어떻게 다른지 4자 비교
  - Spring Boot 3.4의 SSL bundle, Docker Compose support 등 Java 21·25 베이스에서의 신기능
  - **WebFlux를 *유지해야 하는* 시나리오 4가지** — backpressure, SSE, server-sent stream, kafka consumer fan-out. 레퍼런스 §6.3(VT vs Reactive 논쟁)을 결론으로 회수
  - Spring 6 Observability + JFR `jdk.VirtualThreadPinned`
  - `spring.threads.virtual.enabled=true`는 본격 다룸 (14장에서는 간략 호명) ## v2 변경: 중복 정리
  - 21에 머무를지 25로 갈지의 판단 기준
  - 한국 사례: velog·findstar.pe.kr 등 개발자 블로그 인용 ## v2 명시
- **다룰 JEP:** 메타 — Spring과의 결합점
- **JLS 인용:** 없음 (Spring 영역)
- **Spring/JPA 연결:** 챕터 전체가 Spring 고유성
- **고정 도메인 예제:** *결제 마이크로서비스* — 11장(주문 records) / 13장(평가기·workflow) / 14장(API 서버)와 도메인 분리
- **예상 분량:** 15,000자 (v1 13,000 → v2 15,000) ## v2 변경: Spring 고유성 강화

---

### **Part X. 다음 자바**

#### 22장. Valhalla · Amber · Babylon · Leyden — 26 이후의 자바
- **핵심 질문:** 5년 뒤의 자바는 어떤 모습일까?
- **주요 내용:**
  - ## v2 신설 — **챕터 도입 disclaimer 박스**: "이 책이 인쇄될 때까지 알려진 26의 모습". JEP 401·Babylon·Leyden의 *최신 상태*를 박스에 못 박는다.
  - **Project Valhalla:** value class (JEP 401, 26 preview 타깃) — primitive와 reference의 통합
  - null-restricted types, frozen arrays
  - **Project Amber의 다음 카드:** primitive type patterns, array patterns, with-expressions
  - ## v2 강화 — **String Templates의 좌초와 재설계**: 10장에서 자정 사례로 다뤘으나, 22장에서 향후 설계 방향을 사후 추적 (마지막 시점 확인 필요 명시)
  - **Project Babylon:** Java가 GPU·자동미분·이질 컴퓨팅을 표현하는 길
  - **Project Leyden의 종착점:** static image + AOT code cache
  - 책의 마무리 — 호환성이 여전히 자바의 가장 큰 자산
  - ## v2 강화 — **수미상관**: 1장(PayBridge 11년)과 2장(주문 처리 Java 8 vs Java 25 프리뷰)을 회수하며 가상 Java 30 버전으로 닫음
- **다룰 JEP:** JEP 401(예고), Babylon JEP draft, Leyden roadmap
- **JLS 인용:** 향후 변경 예고
- **Spring/JPA 연결:** Spring의 다음 5년 — value class DTO, AOT의 일반화, Babylon으로 ML 워크로드 흡수
- **고정 도메인 예제:** *PayBridge의 가상 Java 30 코드*
- **예상 분량:** 12,000자 (v1 10,000 → v2 12,000) ## v2 변경: 도구 마무리·String Templates 사후 추가

---

## 5. 내러티브 아크

### 챕터 간 흐름의 논리

책의 25장은 **3개의 큰 호(arc)** 로 묶인다.

**호 ①: "왜 모던 자바인가" (서론·1~7장)**
서론 + 1·2장에서 11년의 지형도를 펼친 뒤, 3·4장이 Java 8의 함수형 기초를 다지고, 5·6·7장이 Stream·Collector·Gatherer·Optional로 함수형의 정점까지 끌고 간다. 6장 *함수형 관점 절*과 7장 *Optional의 monad 색채*가 호의 봉우리. ## v2 변경: 함수형 깊이 강조.

**호 ②: "자바의 새 신원" (8A·8B~16장)**
8A·8B장이 Loom 이전 동시성의 토대(JMM)와 한계(callback·reactive)를 직시한 뒤, 9·10장이 언어 표면의 진화를 짚고, 11·12·13장에서 데이터지향 자바의 삼위일체(records + sealed + pattern)를 세운다. 그 도구를 손에 쥔 채 14·15·16장이 Virtual Thread → Pinning → Structured Concurrency·Scoped Values로 동시성의 새 모델을 완성한다. ## v2 변경: 13장 말미에서 14장으로 넘어가는 *다리 페이지* 명시 — "ADT로 도메인을 모델링했으니 그 위에서 동시성을 다시 생각해보자".

**호 ③: "현장의 자바" (17~22장)**
17·18·19·19A장이 성능·네이티브·시작시간·도구의 새 풍경을 보여주고, 20·20A·21장이 마이그레이션·보안·Spring 시너지에서 책의 모든 도구를 한 자리에 모은다. 22장이 다음 자바를 예고하며 1장과 수미상관을 이룬다. ## v2 변경: 19A 도구·20A 보안 신설로 망라성 확보.

### 의존성 그래프 (v2 갱신)

```
서론
  ↓
1 ─→ 2 ─┬─→ 3 ─→ 4
        │
        ├─→ 5 ─→ 6 ─→ 7
        │
        ├─→ 8A ─→ 8B ─────────────────────────────────┐
        │                                              │
        ├─→ 9, 10                                      │
        │       │                                      │
        │       ▼                                      │
        │       11 ─→ 12 ─→ 13 ─(다리)→ 14 ─→ 15 ─→ 16
        │
        ├─→ 17 ─→ 18 ─→ 19 ─→ 19A
        │
        └─→ 20 ─→ 20A ─→ 21 ─→ 22
```

- **5·6·7**은 **3**의 함수형 어휘 위에서만 성립.
- **8B**는 **8A**의 JMM 위에서만 의미.
- **13**(Pattern Matching)은 **11·12**(Records·Sealed)의 ADT 위에서만 의미.
- **14·15·16**(Loom 시대)은 **8A·8B**(Loom 이전)와의 대비를 전제.
- **15** Pinning 디버깅은 **8A**(JMM·synchronized)의 이해를 요구.
- **16** Scoped Values는 **8A**(ThreadLocal)과 **14**(VT의 cheap 함)을 동시에 전제.
- **17** 끝에 **8A**와 메모리의 두 얼굴 다리.
- **21** Reactive 회수는 **8B**를 다시 참조.
- **21**(Spring 시너지)은 **11·13·14·19**의 도구를 결제 마이크로서비스에 모음.
- **22**는 **1**의 지도와 **2**의 프리뷰를 미래로 연장하며 책을 닫음.

### 챕터 독립성과 연속성의 균형

각 챕터는 단독으로도 가치 있다 — 6장(Gatherers), 13장(Pattern Matching), 14장(VT), 17장(GC), 19A장(도구)은 그 자체로 "찾아 펴 보는 레퍼런스" 기능을 한다. 동시에 연결해 읽으면 11년의 자바 진화가 한 줄로 이어진다.

**이 책을 읽는 4가지 길 — 실제 구현 약속** ## v2 신설
1. 처음부터 끝까지 — 통사 독해
2. Part II~III(함수형) → Part VI(데이터지향) → Part VII(동시성) — 주제별 심층 독해
3. Part IX(마이그레이션) → Part I(지형도) → 필요한 주제만 — 실무 적용 우선
4. 챕터별 펼쳐 보기 — 레퍼런스 사용

각 챕터 헤더에 *"이 챕터를 읽기 전 권장: 챕터 N"* 미니 박스를 디자인 — 의존성 그래프를 챕터 헤더 메타데이터로 분산. 부 도입 페이지에 길 안내 한 단락.

---

## 6. 챕터별 Toby 스타일 적용 지점

> ## v2 변경: 표에 *도입부 상황 가정*과 *한국 사례 인용 자리* 열 추가. 수사적 질문은 단조로움 회피를 위해 형식 다양화 — "정말 ~인가?"에 더해 "지금 우리는 어디 와 있는가", "그래서 결국 어떻게 쓰는가", "이게 정말 끝일까", "왜 이제야 ~인가", "~을 우리는 어디까지 알아야 하는가" 등.

| 챕터 | 도입부 상황 가정 | 수사적 질문 (다양화) | 청유형 자리 | 공감 표현 자리 | 한국 사례 인용 |
|------|------------------|----------------------|-------------|----------------|------------------|
| 서론 | "11년 전 람다를 처음 만났을 때를 기억하는가" | 왜 *지금* 이 책이 필요한가? | "함께 11년을 거슬러보자" | 8년째 같은 코드베이스를 만지는 *피로감* | (서문) |
| 1 | "당신의 회사 코드베이스가 Java 8에 멈춰 있다고 해보자" | 지금 우리는 어디 와 있을까? | "지도를 펼쳐보자" | "또 새 버전이라니" 하는 *난감함* | 한국 엔터프라이즈 분포 |
| 2 | "기획 회의에서 '왜 굳이 21로?'라는 질문이 나왔다고 해보자" | 왜 이 순서였을까? | "다섯 동력을 살펴보자" | 새 LTS 마이그레이션 첫날의 *난감함* | — |
| 3 | "PR 리뷰에서 6중 중첩 람다를 만났다고 상상해보자" | 람다는 정말 익명 클래스의 설탕일까? | "한번 합성해보자" | 6중 중첩 람다의 *난감함* | — |
| 4 | "결제 정산이 시간대 때문에 새벽에 깨졌다고 해보자" | 우리는 정말 Date에서 벗어났을까? | "`java.time`으로 옮겨보자" | 시간대 버그로 *새벽에 깨는* 끔찍함 | — |
| 5 | "팀 리뷰에서 동료가 `stream.parallel()`을 무심코 던졌다고 해보자" | Stream은 도대체 무엇일까? | "Stream으로 다듬어보자" | `peek` 디버깅 코드를 두고 배포한 *찜찜함* | — |
| 6 | "5분 이동 평균을 Stream으로 구해보라는 요청이 왔다고 해보자" | 왜 그동안 슬라이딩 윈도우가 그렇게 *번거로웠을까*? | "Gatherer로 표현해보자" | `Collectors.toMap` 1000번의 *지긋지긋함* | — |
| 7 | "`user.getAddress().getCity().getZip()`의 NPE를 처음 만난 그날" | Optional을 정말 제대로 쓰고 있을까? | "체인을 만들어보자" | `Optional<List<T>>`를 처음 만났을 때의 *당혹감* | — |
| 8A | "단일 인스턴스에서 잘 돌던 코드가 멀티 코어에서 깨졌다고 해보자" | volatile은 정확히 무엇을 보장하는가? | "JMM을 들여다보자" | OOTA(out-of-thin-air)를 처음 들었을 때의 *난감함* | — |
| 8B | "외부 API 3개를 합쳐야 하는 컨트롤러를 받았다고 해보자" | Reactive Streams는 왜 그렇게 어려웠을까? | "CompletableFuture로 조합해보자" | `ForkJoinPool.commonPool()`에 blocking I/O를 태운 *끔찍한 사건* | — |
| 9 | "라이브러리 의존성 충돌로 split package 에러가 났다고 해보자" | 왜 우리는 모듈을 안 쓰게 됐을까? | "module-info를 한번 써보자" | split package 에러를 처음 만났을 때의 *난감함* | — |
| 10 | "사내 코드 리뷰에서 30자짜리 타입 선언을 매일 적던 동료가" | var는 가독성을 떨어뜨릴까? | "switch expression으로 옮겨보자" | 매일 30자 타입 선언의 *번거로움*, String Templates 좌초의 *허망함* | — |
| 11 | "DTO를 record로 옮겼는데 JPA Entity도 옮기려다 좌절한 동료" | Records가 Lombok의 *대체*일까, *신원*일까? | "DTO를 record로 옮겨보자" | Entity로 record를 시도했다 *좌절*한 경험 | — |
| 12 | "결제 상태가 6개로 늘어났는데 enum이 더 이상 표현을 못 한다고 해보자" | enum으로 충분했을까? | "sealed로 모델링해보자" | Visitor 패턴 코드를 6번째로 적던 *지긋지긋함* | — |
| 13 | "캐스트 사다리가 9단까지 늘어난 컨트롤러를 받았다고 해보자" | 캐스트 사다리, 이게 정말 최선이었을까? | "함께 표현식 평가기를 만들어보자" | `if (x instanceof A) { A a = (A)x; ...}` 사다리의 *끔찍함* | — |
| 14 | "Tomcat 200 thread 풀로 한 달을 버틴 끝에 p99가 800ms였다고 해보자" | 왜 이제야 thread-per-request가 가능해졌을까? | "Tomcat을 virtual thread로 켜보자" | "100 thread 풀로 버텼던" *답답함* | 우아한형제들·카카오 세미나 |
| 15 | "VT를 켰는데 오히려 deadlock이 났다고 해보자" | 켰는데 왜 더 느려졌을까? | "JFR로 pinning을 잡아보자" | virtual thread를 켰는데 deadlock이 난 *끔찍한 새벽* | 카카오페이 전환 측정 |
| 16 | "request-scoped 데이터를 자식 task에 넘기다 ThreadLocal 청소를 잊었다고 해보자" | concurrent 코드에도 *구조*가 있을 수 있을까? | "ScopedValue로 컨텍스트를 전달해보자" | ThreadLocal 청소를 안 해 메모리가 새는 *찜찜함* | — |
| 17 | "Java 8 PermGen OOM에 시달려본 사람이라면" | 우리 서비스는 정말 G1로 두면 되는 걸까? | "내 서비스의 GC를 골라보자, 한 번 측정해보자" | PermGen OOM의 *지긋지긋함*, ZGC의 fragmentation 모드를 보고 *묘하게 안도하는* 감각 | — |
| 18 | "JNI `*.h` 추출에 하루를 통째로 쓴 그날" | JNI는 정말 끝났을까? | "한 줄을 FFM으로 옮겨보자" | JNI boilerplate의 *번거로움*, native crash로 JVM이 통째 죽은 *끔찍한* 기억 | — |
| 19 | "AWS Lambda 콜드 스타트 8초로 SLA를 깬 그날" | 콜드 스타트, 정말 GraalVM만 답일까? | "CDS로 부팅해보자, 직접 측정해보자" | 콜드 스타트 8초의 *난감함* | — |
| 19A | "CI 파이프라인이 Java 17을 인식 못 해 빌드가 깨졌다고 해보자" | 우리 손에 있는 도구를 우리는 어디까지 알고 있을까? | "JShell을 한번 띄워보자, JFR을 켜보자" | toolchain 설정 한 줄에 하루를 쓴 *피곤함* | — |
| 20 | "Spring Boot 3 이주 첫날 컴파일 에러 700개를 받았다고 해보자" | 어디서부터 손대야 할까? | "Java 17로 일단 빌드만 해보자" | jakarta namespace 변환 첫날의 *막막함*, SecurityManager 제거의 *허망함* | 한국 SI/금융권 사례 |
| 20A | "Spring Security 6 업그레이드 중 KEM·KDF가 무엇인지 모르고 막혔다고 해보자" | 보안 모델을 우리는 어디까지 알아야 할까? | "토큰화 코드를 KDF로 다듬어보자" | post-quantum이라는 단어의 *멀게 느껴지는* 거리감 | — |
| 21 | "한 결제 마이크로서비스에 records·sealed·VT·AOT를 한 번에 넣어야 한다면" | Spring과 Modern Java가 가장 잘 맞물리는 자리는 어디일까? | "한 컨트롤러에 모든 도구를 모아보자" | 책 전체에서 쌓은 도구가 한 자리에 모이는 *후련함* | velog·findstar.pe.kr |
| 22 | "PayBridge의 5년 뒤 코드를 상상해보자" | 자바는 어디까지 갈까? | "5년 뒤의 자바를 함께 그려보자" | 11년 변화를 견뎌낸 자바 개발자에 대한 *헌사* | — |

**문체 운영 원칙 (v2 갱신)**
- 매 챕터 도입부 1~2 문단은 위 표의 *상황 가정*을 그대로 활용 — 챕터 저술가가 임의로 정하지 않는다.
- 새 개념 도입은 *수사적 질문* → 자문자답. 형식은 챕터마다 다양화.
- 코드 비판은 *공감 단어* — "이건 틀렸다" 대신 "이건 *찜찜하다*", "*끔찍한 일이다*", "*번거롭다*".
- 학술적 챕터(17·18·19)에서도 공감 표현 살리기 — 단, *실측 권유형*("한 번 측정해보자", "벤치마크를 직접 돌려보자")으로 톤 조정.
- 챕터 마무리는 *청유형* — "다음 장에서는 ...을 살펴보자".
- 외래어 한국어 병기 — JEP·JLS·Stream·Records 등 고유명사는 영문 유지, 일반 용어는 한국어 우선.

---

## 7. 분량 합산 검증 (v2 갱신)

> ## v2 변경: 신설 챕터 3개, 분할 1개, 분량 재배분, 부 도입·부록 명시.

| 부 / 챕터 | 본문 글자수 |
|----|---------------------:|
| 서론 | 2,000 |
| **Part I 부 도입** | 1,500 |
| 1장 | 11,000 |
| 2장 | 11,000 |
| **Part II 부 도입** | 1,500 |
| 3장 | 13,500 |
| 4장 | 11,000 |
| **Part III 부 도입** | 1,500 |
| 5장 | 14,500 |
| 6장 | 18,500 |
| 7장 | 11,500 |
| **Part IV 부 도입** | 1,500 |
| 8A장 | 11,000 |
| 8B장 | 10,000 |
| **Part V 부 도입** | 1,500 |
| 9장 | 11,000 |
| 10장 | 14,500 |
| **Part VI 부 도입** | 1,500 |
| 11장 | 12,000 |
| 12장 | 12,000 |
| 13장 | 17,000 |
| **Part VII 부 도입** | 1,500 |
| 14장 | 18,000 |
| 15장 | 12,000 |
| 16장 | 15,000 |
| **Part VIII 부 도입** | 1,500 |
| 17장 | 12,000 |
| 18장 | 11,000 |
| 19장 | 10,500 |
| 19A장 | 8,000 |
| **Part IX 부 도입** | 1,500 |
| 20장 | 14,500 |
| 20A장 | 6,000 |
| 21장 | 15,000 |
| **Part X 부 도입** | 1,500 |
| 22장 | 12,000 |
| **부록 A. JEP 일람** | 8,000 |
| **부록 B. JLS 인용 인덱스** | 4,000 |
| **부록 C. 마이그레이션 체크리스트** | 2,000 |
| **부록 D. Java 8 vs 25 코드 패턴 30선** | 6,000 |
| **합계** | **약 306,500자** |

**국판 720~780p**로 Bible의 무게값을 정직하게 충족한다.

**무게 중심 검증 (v2 갱신)**
- 함수형 (3,4,5,6,7) = 69,000자 ≈ **23%** (목표 21%, 약속 충족)
- 데이터지향 (11,12,13) = 41,000자 ≈ **18%** ✓ (목표 18% 회복)
- 동시성 (8A,8B,14,15,16) = 66,000자 ≈ **25%** (목표 25% 정직화 달성)
- 진화사·표면 (서론, 1,2,9,10,22) = 61,500자 ≈ **20%**
- 성능·네이티브·도구·미래 (17,18,19,19A) = 41,500자 ≈ **14%**
- 마이그레이션·보안·Spring (20,20A,21) = 35,500자 ≈ **12%**

> ## v2 변경: 동시성 +4%pt(21%→25%), 데이터지향 +4%pt(14%→18%) 두 개 미스 매치 해소. §2 가중치와 §7 합산이 일치.

---

## 8. JLS 인용 체계 (v2 신설)

> ## v2 신설: 부록 B를 받치는 챕터별 JLS 인용 일람표.

| 챕터 | JLS 인용 위치 | 표현 형식 |
|------|--------------|----------|
| 3 | §15.27 (Lambda Expressions, effectively final) | 본문 박스 한 페이지 |
| 5 | `java.util.stream` 패키지 문서 (non-interference) | 본문 박스 |
| 8A | §17.4 (Memory Model), §17.5 (final field), JSR-133 원문 | 본문 박스 두 페이지 |
| 9 | §7.7 (Module Declarations) | 본문 박스 |
| 10 | §14.4 (LVTI), §14.11 (switch), §15.28 (switch expression), §3.10.6 (text blocks incidental whitespace 알고리즘) | 본문 박스 네 개 |
| 11 | §8.10 (Record Classes) | 본문 박스 한 페이지 |
| 12 | §8.1.1.2 (sealed, permits) | 본문 박스 |
| 13 | §14.30 (Patterns), §14.30.3 (switch exhaustiveness) | 본문 박스 두 개 |
| 14 | JEP 444 원문 + JLS §17.1 (thread) | 본문 박스 |
| 16 | JEP 506 원문 | 본문 박스 |

**원칙**: 각 인용 박스는 ① 원문(영문), ② 한국어 번역, ③ 의미 해설, ④ 본 챕터 본문과의 연결 4단으로 구성. 부록 B에서 "본문 페이지 ↔ JLS §" 양방향 색인.

---

## 9. 중복·공백 점검 (v2 신설)

### 중복 위험과 해소 — 챕터별 고정 도메인 예제

> ## v2 변경: records·virtual thread가 여러 챕터에 반복 등장하나, 각 챕터에 *서로 다른 도메인 예제*를 고정해 중복 회피.

| 도구 | 등장 챕터 | 고정 도메인 (서로 다름) |
|------|----------|-------------------------|
| Records | 11, 13, 20A, 21 | 11=주문 시스템 DTO / 13=표현식 평가기·HTTP Result·Workflow 상태 / 20A=결제 토큰 / 21=`@ConfigurationProperties` config |
| Sealed | 12, 13, 20A | 12=결제 상태 PaymentResult / 13=Expr 트리·HTTP Result·OrderState / 20A=인증 토큰 종류 |
| Pattern matching | 13, 20A, 21 | 13=주력 / 20A=암호 알고리즘 분기 / 21=API 응답 매핑 |
| Virtual Thread | 14, 15, 16, 21 | 14=API 서버 fan-out / 15=세션 ThreadLocal 폭발·DB pinning / 16=ScopedValue 인증 컨텍스트 / 21=결제 마이크로서비스 통합 |
| `spring.threads.virtual.enabled` | 14 (간략 호명), 21 (본격) | 14는 한 줄, 21이 본격 다룸 |
| AOT/CDS | 19, 21 | 19=Petclinic 측정 / 21=Spring Data AOT Repositories |
| `HttpClient` (Java 11) | 20 (도입), 21 (Spring 통합) | 20=마이그레이션 맥락 / 21=RestClient·WebClient·RestTemplate 4자 비교 |
| `CompletableFuture` | 8B, 21 (회수) | 8B=주력 / 21=WebFlux 유지 시나리오에서 회수 |

### 공백 해소

1. **GC와 JMM 사이의 다리**: 17장 끝에 "메모리의 두 얼굴" 한 페이지로 8A와 연결. ## v2 명시
2. **Reactive Streams Flow 연결**: 8B → 21장(WebFlux 유지 시나리오)로 직결. ## v2 명시
3. **JEP가 *왜 그 순서로*** 회수: 11장 도입에 "왜 records가 14 preview, 16 표준이었는가" 진화 박스 등 챕터마다 *진화 박스*. ## v2 명시

---

## 10. 리서치 보강 제안 (v2 갱신)

`01_reference.md` §8(리서치 한계) + 리뷰 권고를 종합:

- **8A장:** JSR-133 원문 PDF의 happens-before 정의문 정확한 발췌
- **13장:** Brian Goetz의 *Data-Oriented Programming in Java* InfoQ 글의 핵심 문단 정확한 번역
- **15장:** Netflix의 production deadlock 사례 — 공식 post-mortem 공개 여부 재확인
- **17장:** Netflix·Pinterest·LinkedIn의 ZGC 사례 — JavaOne/Devoxx 발표 슬라이드 추가 수집 (벤치마크 박스 3종용)
- **19장:** Spring Petclinic 정확한 startup 측정 수치 — 최신 Spring Boot 3.4 기준 재확인
- **20장:** 한국 SI/금융권의 8 → 17 이주 사례 1~2건 — OKKY·velog·네이버 카페·tech 블로그 추가 큐레이션
- **21장:** 한국 커뮤니티 사례 — 우아한형제들·카카오페이의 virtual thread 운영 후기에서 인용 가능한 문장 추출
- **22장:** Project Valhalla JEP 401의 최신 상태 (preview 단계 도달 여부 재확인), Babylon JEP draft 상태

리서치 보강은 챕터 작성 시점에 해당 챕터의 항목만 추가 조사하는 전략이 효율적이다.

---

## 11. v2 변경 핵심 요약

> ## v2 변경: plan-reviewer가 즉시 파악할 수 있도록 변경 항목 정리.

### Must Fix 반영 (4건)
1. **동시성 분량 정직화**: 8장 분할(8A+8B = 21,000자), 14장 +3,000자, 16장 +2,500자. 비중 21%→25%. §2 가중치도 28%→25%로 약속과 일치.
2. **데이터지향 분량 회복**: 13장 14,500→17,000자, 12장 10,500→12,000자. 비중 14%→18%.
3. **JLS 인용 체계화**: §8 신설로 챕터별 JLS 인용 일람표, 부록 B 명시.
4. **누락 JEP 18건 반영**: Sequenced Collections(10장), Markdown Javadoc(10장), Flexible Constructor Bodies(11장), Class-File API(18장), Compact Source/Instance Main(10장), KEM/KDF(20A), SecurityManager(20장), String Templates 좌초(10·22장), HttpClient(20·21장), PermGen→Metaspace(17장), JFR·JMC·JShell·jpackage·jlink·jextract(19A장), Maven/Gradle 호환(19A장), JUnit 5(19A장), GraalVM 깊이(19장).

### Should Fix 반영 (8건)
- 13장 JEP 폭격 → preview 진화사를 *연표 박스*로 압축, 본문은 21 표준 + 22 unnamed 집중.
- 6장 함수형 깊이 → "fold·monad·composition" 절 2,500자 신설.
- 8장 비대화 → 8A·8B 분할.
- 17장 벤치마크 표 → 박스 3종 명시.
- 21장 재탕 위험 → Spring 고유성 5개 척추로 개편(Repositories AOT, ConfigurationProperties+records, RestClient 4자 비교, WebFlux 유지 시나리오, Observability).
- 13→14 점프 → 13장 말미에 다리 페이지 명시.
- 한국 사례 분산 → §6 표에 인용 자리 열 추가, 14·15·20·21장에 분배.
- 22장 Valhalla 약속 → disclaimer 박스 명시.

### Nice to Have 반영 (4건)
- 부 도입 페이지 10개 × 1,500자 = 15,000자 명시.
- "이 책을 읽는 4가지 길" → 챕터 헤더 의존성 미니 박스로 구현 약속.
- 코드 비율 7:3 (약 4만 LOC) §2에 명시.
- 부록 A·B·C·D 명시화.

### 신설 챕터 (3건) + 분할 (1건)
- **서론** (2,000자)
- **19A 모던 자바의 도구들** (8,000자)
- **20A 자바 보안의 11년 변화** (6,000자)
- (분할) **8A·8B** — 한 챕터(17,000)에서 두 챕터(11,000+10,000)로

### 총량
- 본문 271,500 → **306,500자**. 국판 720~780p. Bible 약속의 상한.

---

*v1 작성: 2026-05-11, v2 갱신: 2026-05-11 (하네스 v1.2.0)*
