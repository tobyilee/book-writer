# Modern Java Bible
## Java 8에서 25까지, 그리고 그 너머

> 11년의 자바 진화를 한 권에 압축한, Spring 엔터프라이즈 개발자를 위한 레퍼런스 겸 가이드.

- **저자:** Toby-AI
- **버전:** v1.0.0
- **발행일:** 2026-05-11
- **언어:** 한국어 (ko)
- **분량:** 본문 약 453,000자, 국판 약 720~780페이지 / 22개 본문 장 + 서론 + 부록 4종

---

## 책 소개

Java 8이 람다와 Stream을 가지고 등장한 2014년부터 Java 25가 Virtual Thread, Structured Concurrency, Compact Object Headers를 들고 LTS의 자리에 앉은 2025년까지 — 11년이라는 시간 동안 자바는 한 번이 아니라 여러 번, 그것도 깊이 변했다. 함수형이 들어오고, 데이터지향이 합류하고, 모듈 시스템이 흔들리고, Loom이 우리가 알던 동시성을 다시 짰다. 그런데 정작 자바를 매일 쓰는 우리는 그 변화의 절반쯤을 흘려보낸 채 Java 8 코드 위에서 살고 있다.

이 책은 그 11년치의 변화를 *한 권에 정직하게* 담아내려는 시도다. JLS 인용을 두텁게 깔아 *왜 그렇게 동작하는가*를 짚고, Spring Framework 맥락의 실무 예시(가상의 결제 SaaS "PayBridge")로 추상에 살을 붙였다. 람다·Stream·Optional의 함수형 어휘에서 records·sealed·pattern matching의 데이터지향 모델, Virtual Thread·Structured Concurrency·Scoped Values의 Loom 시대, FFM·Vector·AOT·Compact Object Headers의 메모리·네이티브 풍경, 그리고 Java 8 → 17/21/25 마이그레이션·보안·Spring Boot 3 시너지까지 — Bible이라는 이름의 무게를 정직하게 받아들인 한 권이다.

다른 자료와의 차이는 *통사*에 있다. 개별 기능을 하나씩 소개하는 책은 많지만, 이 책은 11년의 자바를 *시간 축*(Java 8 → 11 → 17 → 21 → 25 LTS)과 *주제 축*(함수형·데이터지향·동시성·언어 표면·성능)이 교차하는 더블 헬릭스 구조로 엮는다. 그래서 *기능*이 아니라 *왜 그 시점에 그 기능이*를 읽을 수 있다.

---

## 누구를 위한 책인가

- **Spring Framework로 엔터프라이즈 애플리케이션을 만드는 자바 개발자.** records와 sealed를 들어는 봤지만 *왜 ADT인지*는 한 번도 진지하게 본 적이 없다면, 이 책의 Part VI이 그 자리다.
- **Java 8/11/17에 머물러 있는 코드베이스를 21·25로 옮기려는 팀.** Part IX의 마이그레이션 챕터와 부록 C의 체크리스트가 *언제·어떤 순서로*를 그려준다.
- **모던 자바의 함수형·동시성 패러다임을 깊게 이해하려는 시니어 개발자.** JMM·Stream의 spliterator·Virtual Thread의 pinning·Structured Concurrency의 cancellation 정책 — *내부 구현 수준*에서 다룬다.
- **자바 진화의 큰 그림을 잡고 싶은 학습자.** 1장(11년의 지도)과 2장(다섯 가지 동력)만 읽어도 *왜 그렇게 됐는지*가 보인다.

읽고 나면 자기 코드베이스가 Java 8 어디에 멈춰 있는지 진단하고, 21/25로 옮기는 길을 그릴 수 있다. 함수형·데이터지향·동시성 세 축에서 *왜* 그렇게 써야 하는지 JLS 수준으로 설명할 수 있다.

---

## 이 책의 약속

- **함수형 어휘의 깊이.** 람다·`Function` 합성·Stream API·Collector·Reducer·Gatherer(Java 22+)·`Optional<T>`의 약속과 함정을 *내부 구현*까지.
- **데이터지향 자바의 완성도.** Records → Sealed → Pattern Matching이 어떻게 자바에 *ADT*를 들여놨는지, *Result 타입*을 어떻게 직접 빚는지.
- **동시성 두 시대를 한 권에.** Loom 이전(JMM·j.u.c·CompletableFuture·Reactive Streams Flow)과 이후(Virtual Thread·Structured Concurrency·Scoped Values)를 분리하지 않고 *연결*해서 본다.
- **JLS 인용 체계.** 본문 핵심 동작은 JLS §·JEP·JSR로 뒷받침. 부록 B의 인용 인덱스로 역추적 가능.
- **60+ JEP 망라.** Java 9의 JPMS부터 Java 25의 Compact Object Headers까지 — 부록 A에 버전·Project·표준화 시점으로 정렬.
- **Spring Boot 3 × Java 21/25 시너지.** AOT·Virtual Thread·records 시너지가 Spring 코드에서 *어떻게 다르게 생기는지*.
- **마이그레이션의 현장.** 가상의 PayBridge 사례로 Java 8 → 11 → 17 → 21 → 25 단계 이주의 함정과 순서.
- **Java 8 vs 25 코드 패턴 30선.** 부록 D에서 11년의 변화를 *코드 한 짝*으로 압축.

---

## 차례

**서론. 왜 이 책인가** — 11년의 변화를 왜 지금 한 권에 담아야 하는가

### Part I. 11년의 자바, 한 장의 지도

1. **11년의 자바, 한 장의 지도** — Java 8부터 25까지의 LTS·릴리스 케이던스·Project 매트릭스
2. **11년 변화의 다섯 가지 동력** — 함수형·데이터지향·동시성·언어 표면·성능, 다섯 축으로 통사를 읽기

### Part II. 함수형 자바의 어휘

3. **람다와 함수형 인터페이스** — 그 익숙함의 진짜 의미, `Function` 합성과 *invokedynamic*의 내부
4. **`java.time`과 종종 잊히는 Java 8의 보석들** — `Optional` 이전에 Java 8이 들여놓은 것들

### Part III. 스트림과 Optional의 모든 것

5. **Stream API** — 선언적 데이터 파이프라인의 해부, spliterator·short-circuit·parallel
6. **Collector · Reducer · Gatherer** — Stream의 종착과 새 중간 정거장 (Java 22+ Gatherers)
7. **`Optional<T>`** — 약속과 함정, `Optional<List<T>>` 같은 안티패턴까지

### Part IV. 동시성 I — Loom 이전의 모든 것

8A. **j.u.c와 Java Memory Model** — happens-before·volatile·synchronized·`Atomic*`의 토대
8B. **CompletableFuture와 Reactive Streams Flow** — 비동기 조합의 두 갈래

### Part V. 언어 표면의 진화 (Java 9 ~ Java 23)

9. **JPMS** — 실패인가 미완인가, 모듈 시스템이 실제 코드에 미친 영향
10. **`var` · switch · text blocks · Sequenced Collections** — 작지만 결정적인 변화들

### Part VI. 데이터지향 자바 — Records · Sealed · Pattern

11. **Records** — 자바가 마침내 인정한 *데이터의 신원*
12. **Sealed Classes** — 합 타입(Sum Type)이 자바에 들어온 날
13. **Pattern Matching** — ADT를 풀어내는 도구, `Result<T, E>`를 직접 짓다

### Part VII. 동시성 II — Loom 시대

14. **Virtual Threads** — thread-per-request의 부활, carrier thread와 continuation의 내부
15. **Pinning · ThreadLocal · 함정들** — Virtual Thread가 우리를 실망시키는 자리
16. **Structured Concurrency와 Scoped Values** — concurrent 코드의 *문법*

### Part VIII. 메모리 · 네이티브 · 성능 · 도구

17. **GC 11년의 진화** — Serial부터 G1·ZGC·Generational Shenandoah까지
18. **Foreign Function & Memory API · Vector API · Class-File API** — JNI의 종말과 SIMD의 자바
19. **AOT · Leyden · Compact Object Headers** — 시작 시간과 메모리의 새 풍경
19A. **모던 자바의 도구들** — JShell·JFR·jpackage·jlink·jextract 일습

### Part IX. 마이그레이션 · 보안 · Spring 시너지

20. **Java 8 → 17 마이그레이션** — 현장의 함정과 권장 순서
20A. **자바 보안의 11년 변화** — SecurityManager의 종말부터 KEM·KDF까지
21. **Spring Boot 3.x × Java 21/25** — 시너지의 *고유성*

### Part X. 다음 자바

22. **Valhalla · Amber · Babylon · Leyden** — 26 이후의 자바

### 부록

- **A. JEP 일람** — 60+ JEP를 버전·Project·표준화 시점으로 정렬
- **B. JLS 인용 인덱스** — 본문에 나온 JLS 인용을 §·페이지·챕터 번호로 색인
- **C. 마이그레이션 체크리스트** — 20장의 핵심을 한 페이지로
- **D. Java 8 vs 25 코드 패턴 30선** — 11년의 변화를 *코드 한 짝*으로 압축

---

## 저자 소개

**Toby-AI**는 book-writer 하네스(v1.2.0)와 Anthropic Claude(Opus 4.7)가 협업해 빚어낸 가상 저자 페르소나다. 자바·Spring·동시성·아키텍처에 관한 11년치 1차·2차 자료를 학습하고, JLS·JEP·JSR을 일관된 인용 체계로 끌어와 책 한 권을 정직하게 빚는 일에 집중한다. 저자명이 사람이 아니라는 사실은 콜로폰과 이 페이지에 명시한다 — 책의 내용에 대한 책임 역시 Toby-AI가 진다.

---

## 책 정보

- **파일:** `Modern-Java-Bible-v1.0.0.epub`
- **형식:** EPUB 3 (ko), 표지 포함 1600×2560 PNG
- **분량:** 본문 약 453,000자, 국판 720~780페이지
- **챕터:** 본문 22장(서론 포함) + 부록 4종
- **버전:** v1.0.0 (2026-05-11)
- **라이선스:** CC BY-NC-SA 4.0 (저작자 표시 · 비상업적 이용 · 동일조건 변경허락 4.0 국제) — https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko
- **식별자:** `modern-java-bible-v1.0.0`
- **표준 검증:** epubcheck 3.3 통과 (fatal 0 / error 0 / warning 0)
- **제작:** book-writer 하네스 v1.2.0
