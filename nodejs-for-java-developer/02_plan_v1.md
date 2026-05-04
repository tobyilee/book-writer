# Java/Spring/Kotlin 개발자를 위한 Node.js 저술 계획

본 문서는 `01_reference.md`에서 수집한 사실·수치·일화를 토대로, Java/Spring/Kotlin 백엔드 경력자가 Node.js 진영을 빠르게 이해하고 실무로 옮길 수 있게 하는 책의 구조를 설계한 것이다. 입문서가 아니라 "이미 백엔드를 잘 아는 사람의 패러다임 이전"을 돕는 비교·실무 가이드를 지향한다.

---

## 1. 제목 후보

### 후보 A — 정공법 비교서

- **제목:** 자바 개발자를 위한 Node.js
- **부제:** 스프링에서 익힌 직관을 그대로 들고 가는 백엔드 패러다임 이전
- **슬로건:** "런타임만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다."
- **고른 이유와 독자:** 가장 검색 친화적이고 의도가 분명하다. 서점·온라인 검색에서 "java node 비교", "spring nestjs"를 치고 들어오는 시니어/미드 백엔드 개발자에게 곧장 닿는다. 부제로 "패러다임 이전"이라는 단어를 박아 입문서가 아니라는 신호도 같이 준다.

### 후보 B — 관점·이야기 중심

- **제목:** 다른 런타임, 같은 백엔드
- **부제:** Java/Spring/Kotlin 경력 개발자가 Node.js로 옮겨가는 길
- **슬로건:** "이벤트 루프와 스레드 풀, 이름만 다를 뿐 우리가 풀어온 문제는 같다."
- **고른 이유와 독자:** "이전 경력이 헛되지 않다"는 메시지를 표지부터 내건다. Node를 배우면서도 Spring 경력에 자부심을 갖고 있는 미드/시니어, 특히 팀 안에서 새 스택을 검토해야 하는 테크 리드에게 어필한다. B는 정체성에 호소하는 톤이라 책의 비교 관점과도 잘 맞는다.

### 후보 C — 실무 가이드 톤

- **제목:** Spring을 떠나기 전에 — Node.js 실전 가이드
- **부제:** PayPal·Netflix·당근마켓이 갔던 길, 그리고 Uber가 돌아온 길
- **슬로건:** "갈아탈 것인가, 같이 굴릴 것인가 — 결정 전에 펼치는 책."
- **고른 이유와 독자:** "결정"이라는 행위에 초점을 맞춘 제목. 마이그레이션을 검토 중인 테크 리드·아키텍트·CTO 후보군에 닿는다. 후퇴 사례(Uber)까지 표지에 명시해 균형감을 약속한다는 점이 차별점이다.

### 추천

**후보 B — 다른 런타임, 같은 백엔드** 를 추천한다.

- 책의 핵심 메시지("백엔드 직관은 그대로 쓸 수 있다, 도구만 바꾸면 된다")를 가장 잘 압축한다.
- 후보 A는 단단하지만 너무 "교과서"스럽고, 후보 C는 마케팅 이미지가 강해 본문의 9개 영역 균형과 어긋날 수 있다.
- B는 본문의 평어체·청유형과 어울리는 잔잔한 톤이라, 표지부터 본문까지 일관성이 잡힌다.

---

## 2. 책 특성

- **장르 포지셔닝:** **비교 기반 실무 가이드**. 입문서가 아니라 "이미 백엔드를 아는 사람의 두 번째 런타임"으로서 위치를 잡는다. 1차 자료·실제 마이그레이션 회고가 본문 안에 녹아드는 회고적 가이드의 톤을 유지한다.
- **분량 목표:** 본문 9개 챕터 + 프롤로그/에필로그. 챕터 평균 32~38페이지, 마이그레이션 챕터(8장)만 약 50페이지. **총 290~330페이지(약 22만~26만자) 목표.**
- **난이도:**
  - 진입: 백엔드 5년 이상, Spring/JPA/Kotlin·Java 운영 경험 있음. JS는 "써본 적은 있지만 본격적으로 백엔드를 짜본 적은 없다." async/await의 모양은 알지만 이벤트 루프 모델을 자기 언어로 설명하지는 못한다.
  - 도착: NestJS로 작은 서비스를 직접 설계·운영하고, BFF 또는 마이크로서비스 한 조각을 Strangler Fig 패턴으로 마이그레이션할 수 있다. Node 운영 도구 체인(clinic.js, Pino, OpenTelemetry, PM2/K8s)을 JVM 도구와 매핑해 머릿속에 가지고 있다.
- **독자 여정 한 줄:** 1장에서는 "Node.js가 정말 백엔드 일감을 감당할 수 있을까"를 의심하던 독자가, 8장 후반에서는 "우리 팀의 어느 경계부터 잘라내 Node로 옮길지"를 결정할 수 있게 된다. 9장에서는 그 결정을 조직 안에서 설득할 언어를 갖는다.
- **톤(스타일 가이드 준수):**
  - 평어체 기반(`-다`, `-한다`)에 청유형(`살펴보자`, `옮겨보자`, `생각해보자`)을 적극 섞는다.
  - 새 개념을 도입할 때 수사적 질문(`왜 그럴까?`, `그렇다면 어떻게 다를까?`)을 먼저 던진다.
  - 상황 가정(`Spring 모놀리스를 운영해온 팀이 있다고 해보자`)으로 들어간다.
  - "난감하다", "찜찜하다", "번거롭다" 같은 감정 어휘를 비교 지점에서 자연스럽게 사용한다.
  - "Java/Spring에서는 X였지만 Node.js에서는 Y다"라는 비교 구도가 부록·박스가 아니라 본문 흐름의 일부로 흐른다.

---

## 3. 내러티브 아크

이 책은 **의심 → 발견 → 도구 익숙해지기 → 실무 현실 → 결단**이라는 곡선으로 흐른다.

1~2장은 **의심과 발견**의 구간이다. 1장에서 Spring 백엔드 개발자가 Node.js를 처음 마주하며 갖는 의심("단일 스레드인데 어떻게 잘 돌까", "콜백 지옥은 아직 살아 있나")을 정직하게 꺼내고, 이벤트 루프와 V8/libuv 구조로 그 의심을 해소한다. 2장에서는 JS와 TS의 모양을 Java/Kotlin과 나란히 두고 본다. 여기서 독자는 "내 직관이 그대로 쓰이는 부분"과 "다시 학습해야 하는 부분"을 분리한다.

3~5장은 **도구를 다루는 손에 익히는 구간**이다. 3장에서 활용 패턴(REST/GraphQL/CLI/워커/WebSocket/서버리스)의 지형을 한 번 훑고, 4장에서 NestJS를 Spring Boot와 정면으로 맞붙인다. 4장은 이 책의 첫 번째 두께 있는 챕터다 — DI·모듈·인터셉터·가드를 Spring의 어노테이션 체계와 일대일로 매핑하고, "DI가 진짜 DI인가" 같은 논쟁점도 짚는다. 5장은 ORM이다. Hibernate에서 자라온 사람에게 "마법의 부재"가 어떤 충격인지 정직하게 다루고, Prisma·Drizzle·TypeORM의 선택지를 펼친다.

6~7장은 **실무 현실**로 진입한다. 6장에서 디버깅 도구(jstack/jmap/VisualVM ↔ `--inspect`/clinic.js/heap snapshot)를 매핑하고, 7장에서 배포·운영(PM2/Docker/K8s, Pino/OTel/APM, graceful shutdown)을 다룬다. 여기까지 오면 독자는 손에 도구가 들려 있는 상태다.

8~9장이 **결단의 구간**이다. 8장은 이 책의 절정이다. PayPal·LinkedIn·Netflix·Walmart·당근마켓 사례로 "어떻게 옮겼는가"를 보여주고, Uber 후퇴 사례로 "왜 돌아왔는가"를 같이 본다. Strangler Fig 패턴을 단계별로 풀고, 모놀리스 → BFF → 부분 마이크로서비스로 가는 결정 트리를 제시한다. 9장은 이를 조직과 커리어 차원으로 끌어올린다 — 팀에 어떻게 도입을 설득하고, 어떤 신호가 보이면 후퇴를 결정해야 하는지를 정리한다.

이 곡선의 핵심은, 독자가 도구만 바꾸면서 자기 백엔드 직관을 재확인하게 만든다는 점이다. "내가 Spring에서 풀던 문제는 Node에서도 똑같은 문제다, 다만 도구의 이름이 다를 뿐이다." 이 메시지가 8~9장에서 결단으로 자연스럽게 이어진다.

---

## 4. 챕터 목록

### 프롤로그. Spring 개발자가 Node.js 폴더를 처음 열었을 때

- **핵심 질문:** Java/Spring 개발자가 Node.js 프로젝트 폴더를 처음 열고 가장 먼저 느끼는 어색함은 무엇인가? 그 어색함은 어디서 오는가?
- **분량:** 약 8~10페이지(짧은 도입).
- **역할:** 본문이 아니라 책의 톤 잡기. `package.json` vs `pom.xml`, `node_modules` vs Maven 로컬 저장소, "fat jar"의 부재를 짧게 시각적으로 대비하면서, 독자에게 "이 책은 당신이 이미 아는 것에서 출발한다"는 신호를 준다.

---

### 1장. 단일 스레드는 정말 일감을 감당할 수 있는가 — 런타임의 본체

- **부제:** V8과 libuv, 이벤트 루프, 그리고 Spring 서블릿 스레드 모델과의 헤어짐
- **핵심 질문:** 한 개 스레드에서 도는 런타임이 어떻게 수만 커넥션을 처리하나? 그리고 그게 막히면 무슨 일이 벌어지나?
- **주요 내용 (10불릿):**
  - 가벼운 도입: Spring 서블릿이 "요청 = 스레드"였다는 사실을 한 단락으로 환기.
  - V8 엔진의 위치 — JIT 컴파일이 JVM의 HotSpot/G1과 어떻게 닮고 다른지.
  - libuv의 이벤트 루프 6단계(timers → pending → idle/prepare → poll → check → close)를 그림과 함께. epoll/kqueue 위에서 어떻게 도는지.
  - 워커 스레드 풀(기본 4개)의 역할 — 파일 I/O·DNS·crypto가 어디로 가는지.
  - **JS 코드 예시:** `setTimeout` + `setImmediate` + `process.nextTick`의 실행 순서를 보여주는 짧은 스크립트.
  - "이벤트 루프를 막는다"의 실체 — CPU 바운드 코드 한 줄이 모든 사용자를 줄 세우는 시연 코드.
  - **TS 코드 예시:** `perf_hooks.monitorEventLoopDelay()`로 p99 lag 측정하기.
  - Worker Threads의 위치 — Java의 ForkJoinPool과 닮은 점, V8 인스턴스를 따로 갖는 비용.
  - Java Virtual Threads(Project Loom)와의 비교 — 같은 목적지(높은 동시성), 다른 길.
  - GC 비교 — V8의 New/Old Space와 JVM의 G1/ZGC. Node가 큰 힙을 안 다루는 이유.
- **Java/Spring 비교 포인트:** 서블릿 스레드 풀 vs 이벤트 루프, ThreadPoolExecutor vs Worker Threads, Loom vs async/await(같은 목적지로 가는 두 길)을 본문 안에 맞물려 풀어낸다. 부록이 아니다.
- **인용할 리서치 자료:** §1.1, §1.2 (libuv·V8·이벤트 루프 단계), §2의 Top 10 중 1번(단일 스레드 충격), §4.1(Don't block the event loop, Worker Threads, Virtual Threads 비교), §4.5(이벤트 루프 블로킹 탐지). Walmart의 "convoy effect" 사례(§3.4)를 힌트로 살짝 흘려 8장에서 다시 회수하게 한다.
- **예상 분량:** 약 32페이지(약 25,000자).

---

### 2장. JavaScript와 TypeScript — Java 개발자가 다시 학습할 것과 그대로 쓸 것

- **부제:** 구조적 타입, 클로저, Promise, 그리고 TS 유틸리티 타입의 자리
- **핵심 질문:** Kotlin·Java 출신이 TypeScript에서 가장 헷갈리는 지점은 어디고, 반대로 그대로 가져갈 수 있는 직관은 무엇인가?
- **주요 내용 (11불릿):**
  - 도입 — "콜백 지옥은 무엇인가"는 한 단락으로 빠르게 넘긴다(독자는 이미 안다).
  - `this` 바인딩이 호출 시점에 결정되는 모델 — Java의 인스턴스 고정 `this`와 어떻게 다른가.
  - 화살표 함수가 등장하면서 정리된 부분과 여전히 남는 함정.
  - 클로저와 var/let — Java의 final 캡처와 비교했을 때 어디서 버그가 생기는가.
  - Promise·async/await의 함정 3종 — `forEach` 안의 await, 빠진 `Promise.all`, 잡히지 않은 rejection.
  - **TS 코드 예시:** Kotlin의 `suspend fun loadUser(): User`와 같은 시그니처를 TS로 옮긴 비교.
  - 구조적 타입 vs 명목적 타입 — "implements 안 써도 호환된다"가 만드는 자유와 위험.
  - TS 제네릭의 컴파일 타임 소거와 Java의 타입 소거 비교.
  - 유틸리티 타입(`Partial`, `Pick`, `Omit`, `Record`, `ReturnType`)이 Kotlin 데이터 클래스 + 리플렉션을 어떻게 컴파일타임에 대체하는가.
  - **TS 코드 예시:** API 응답 DTO에 `Pick`/`Omit`을 적용해 입력/출력 타입을 갈라내는 패턴.
  - JS → JSDoc → `// @ts-check` → TS로 가는 단계적 도입 권고.
- **Java/Spring 비교 포인트:** 명목적 타입과 구조적 타입의 사상 차이를 본문에서 정면으로 다룬다. CompletableFuture와 async/await의 모양은 비슷해도 사용 패턴이 다르다는 점, Kotlin의 `suspend`와 JS의 async/await을 한 페이지에 병치하는 코드 비교를 넣는다.
- **인용할 리서치 자료:** §2의 Top 10 중 2번(this), 3번(Promise), 7번(타입 시스템), §4.2 전체. Kotlin suspend ↔ JS await 비교는 §7의 Joffrey Bion 글을 인용. TS 시장 신호(GitHub 1위, 채용 65%)는 §4.2의 tech-insider.org 출처.
- **예상 분량:** 약 30페이지(약 23,000자).

---

### 3장. 활용 패턴의 지형 — REST·GraphQL·CLI·워커·WebSocket·서버리스

- **부제:** Spring 진영의 어떤 도구가 Node에서는 어디에 있는가
- **핵심 질문:** Spring MVC, Spring Batch, Spring WebFlux, Spring Cloud Function… 각각의 자리에 Node에서는 무엇이 있는가? 그리고 어디서 모양이 갈라지는가?
- **주요 내용 (10불릿):**
  - REST: Express(생태계) / Fastify(성능) / NestJS(구조)의 삼각 구도. JAX-RS·Spring MVC와의 매핑.
  - **TS 코드 예시:** 같은 엔드포인트를 Spring Boot 컨트롤러와 NestJS 컨트롤러로 나란히 보여주는 비교 코드(이 챕터의 시그니처 페이지).
  - GraphQL: Apollo·Mercurius. NestJS의 DI와 결합한 request scope DataLoader가 N+1을 어떻게 푸는가.
  - **TS 코드 예시:** NestJS + DataLoader로 N+1을 막는 짧은 리졸버.
  - CLI: commander/yargs/oclif는 picocli의 자리. Vite/esbuild로 단일 실행 파일 번들링.
  - 백그라운드 워커: BullMQ가 사실상 표준. Spring Batch와 다른 모델(분산 큐 + 워커 풀), 우선순위·재시도·딜레이·repeatable cron.
  - **TS 코드 예시:** BullMQ로 이메일 발송 잡을 정의하고 워커가 처리하는 짧은 코드.
  - WebSocket: Socket.IO(폴리필 + 자체 프레이밍) vs `ws`(raw). Spring WebFlux + STOMP의 RabbitMQ 통합과 무엇이 다른가.
  - 서버리스: Lambda·Vercel·Cloudflare Workers. Spring Boot Lambda 콜드 스타트 3~10초(SnapStart 1.5초/180ms) vs Node 200ms 미만 — 왜 이 격차가 본질적인가.
  - 패턴 선택 가이드: 트래픽 모양·팀 크기·운영 부담을 축으로 한 의사결정 표.
- **Java/Spring 비교 포인트:** Spring 진영의 풀 스택 매트릭스(MVC/Batch/WebFlux/Cloud Function)를 Node 도구와 일대일로 짝지은 표를 챕터 초입에 둔다. 본문은 그 표를 풀어내는 식으로 진행.
- **인용할 리서치 자료:** §4.3 전체, §4.4의 Express/Fastify 표, §4.7의 콜드 스타트 수치, §3.6의 당근마켓 푸시 알림 사례(BullMQ 위치 강화에 활용). GraphQL N+1은 §4.3의 dev.to/tugascript와 wanago.io 출처.
- **예상 분량:** 약 36페이지(약 28,000자).

---

### 4장. NestJS와 Spring Boot — 가장 닮은 두 프레임워크의 정면 비교

- **부제:** 모듈, DI, 데코레이터, 인터셉터·가드 — 그리고 진짜 DI 논쟁
- **핵심 질문:** Spring Boot 출신이 NestJS를 처음 쓸 때 가장 자주 데이는 지점은 어디인가? 그리고 어디서 Spring이 그리워지고, 어디서 NestJS가 더 가뿐한가?
- **주요 내용 (12불릿):**
  - 도입 — Spring Boot가 t2.micro에서 무부하 27~29% CPU를 먹고 NestJS로 옮겨 6~7%로 떨어졌다는 dev.to 후기로 시작.
  - 공통 DNA — 모듈/컨트롤러/서비스, DI 컨테이너, AOP에 대응하는 인터셉터·가드, 데코레이터(어노테이션) 라우팅.
  - 차이 1 — Spring의 클래스패스 컴포넌트 스캔 vs NestJS `@Module`의 명시적 그래프(`imports`/`providers`/`exports`).
  - **TS 코드 예시:** 같은 도메인을 Spring `@Service`/`@Repository`/`@RestController` 패키지 구조와 NestJS `*.module.ts`/`*.service.ts`/`*.controller.ts` 구조로 나란히.
  - 차이 2 — Java 어노테이션 vs TS 데코레이터의 메타데이터 모델, `reflect-metadata`의 자리.
  - 차이 3 — Spring은 트랜잭션·캐시·배치·시큐리티 ecosystem이 두껍다. NestJS는 시작 시간·메모리에서 우위.
  - 인터셉터·가드·파이프 — Spring의 `HandlerInterceptor`, `Filter`, `MethodSecurity`, `@Valid`와 일대일 매핑.
  - **TS 코드 예시:** JWT 인증 가드 + 요청 로깅 인터셉터 + DTO 검증 파이프를 한 모듈에 묶은 NestJS 코드.
  - `forwardRef`와 순환 의존 — 등장하면 설계 점검 신호. Spring에서도 같은 신호인 점.
  - "DI인가 hardwiring인가" 논쟁(Hacker News 인용)을 정직하게 다루고, Spring Bean 정의(자바 컨피그·컴포넌트 스캔)와의 차이를 본문에서 정리.
  - 호불호 — Spring/Kotlin 20년차의 NestJS 전환 회고 vs "Express/Fastify로 충분한 작은 서비스에 NestJS는 과한 보일러플레이트"라는 반대 견해.
  - 결정 가이드 — 팀 규모·서비스 수·도메인 폭을 기준으로 NestJS / Fastify 선택 표.
- **Java/Spring 비교 포인트:** 이 챕터는 책에서 비교 밀도가 가장 높다. 거의 모든 절이 Spring과의 정면 매핑이고, 코드도 양쪽을 함께 보여준다. "DI는 진짜 DI인가"를 회피하지 않고 다룬다.
- **인용할 리서치 자료:** §4.4 전체, §5.2(NestJS 호불호), §2의 Top 10 중 4번(`forwardRef`), §3.6(국내 NestJS 도입 — 토스·당근마켓·인프런 언급은 1차 출처 한계까지 적시), §4.4의 dev.to/digvijay 후기와 agilecoding.io의 Spring/Kotlin 20년차 회고, Hacker News의 진짜 DI 논쟁.
- **예상 분량:** 약 44페이지(약 35,000자) — 다른 프레임워크 챕터보다 두껍게.

---

### 5장. ORM과 데이터베이스 — Hibernate의 마법이 사라진 자리

- **부제:** Prisma, Drizzle, TypeORM, 그리고 명시적 트랜잭션의 세계
- **핵심 질문:** JPA/Hibernate에서 자라온 개발자가 Prisma를 처음 만났을 때 어떤 감각이 사라졌다고 느끼는가? 그 사라짐을 어떻게 설계로 메우는가?
- **주요 내용 (12불릿):**
  - 도입 — "Hibernate의 마법이 그립다"는 감각을 한 단락으로 정직하게 꺼낸다. lazy loading, dirty checking, `@Transactional` AOP가 모두 없거나 다르다는 사실을 미리 던져둔다.
  - Prisma vs Drizzle vs TypeORM 비교표 — 스키마 정의, 타입 안전, 마이그레이션, 번들 크기, 콜드 스타트, Hibernate와의 거리.
  - Prisma의 명시적 `include`/`select` — Hibernate의 lazy proxy와 정면 비교.
  - **TS 코드 예시:** Prisma로 user + posts를 한 번에 가져오는 `findMany({ include: { posts: true } })`와, 빠뜨렸을 때 `user.posts`가 `undefined`가 되는 시연.
  - LazyInitializationException이 사라진 대신 "왜 user.posts가 undefined냐"가 새 질문이 된다는 사실.
  - Unit of Work의 부재 — Hibernate는 세션 안 변경을 자동 추적해 flush 시 SQL 생성. Prisma는 메서드 호출이 곧 SQL. Prisma 이슈 #4991의 오랜 요청을 인용.
  - 트랜잭션 — `@Transactional` AOP 마법 vs `prisma.$transaction([...])` 또는 콜백. 분산 트랜잭션·Saga는 별도라는 점.
  - **TS 코드 예시:** Prisma `$transaction`으로 두 쓰기를 묶는 코드와, Spring의 `@Transactional` 자바 코드 병치.
  - Drizzle의 위치 — JOOQ/Querydsl과 닮은 SQL-가까운 모델, Edge·Lambda에 강한 가벼움.
  - Mongoose — Spring Data MongoDB의 자리. 스키마와 타입의 결합.
  - Redis — `ioredis`/`node-redis`. Spring Data Redis와 동일한 Pub/Sub·스트림·Lua 패턴.
  - 선택 가이드 — "Hibernate가 그리우면 Prisma, JOOQ가 그리우면 Drizzle, 마이그레이션 안정성이 최우선이면 Prisma."
- **Java/Spring 비교 포인트:** "Hibernate-like 마법은 적지만 타입 안전이 강하다"는 프레이밍을 본문 흐름의 축으로 삼는다. dirty checking·lazy loading·`@Transactional` AOP의 부재를 단점이 아니라 "다른 설계"로 풀어낸다.
- **인용할 리서치 자료:** §4.8 전체, §2의 Top 10 중 5번(lazy loading)과 6번(트랜잭션), §5.3(ORM 논쟁), §6의 팁 4번(N+1 방지). Prisma 공식 문서 두 페이지(transactions, relation queries)와 GitHub 이슈 #4991, betterprogramming.pub의 "Hibernate is not so evil" 글을 같이 인용.
- **예상 분량:** 약 38페이지(약 30,000자).

---

### 6장. 디버깅 — JVM 도구 체인을 Node 도구 체인으로 옮기기

- **부제:** jstack·jmap·VisualVM 대신 `--inspect`·clinic.js·heap snapshot
- **핵심 질문:** 운영 중인 Spring Boot 앱에서 jstack/jmap을 떴던 손이, Node.js 앞에서 어떤 명령을 치게 되는가? 그리고 어디서 도구의 사상이 갈라지는가?
- **주요 내용 (10불릿):**
  - JVM 도구 ↔ Node 도구 매핑 표(§4.5). 챕터의 표지 페이지로 두고 본문이 그 표를 풀어낸다.
  - `--inspect` + Chrome DevTools — VisualVM의 자리. 원격 디버깅, 브레이크포인트, CPU 프로파일.
  - **CLI 예시:** 원격 컨테이너의 Node 프로세스에 `--inspect=0.0.0.0:9229`로 접속하고 SSH 포트포워딩으로 DevTools 붙이기.
  - 힙 스냅샷 — `v8.writeHeapSnapshot()`, `--heapsnapshot-signal=SIGUSR2`. 힙의 약 2배 메모리를 잠시 더 쓰며 이벤트 루프를 막는다는 운영 주의사항.
  - clinic.js 3종(doctor/flame/bubbleprof) — JFR과 async-profiler의 자리에 있는 Node 도구들.
  - **CLI 예시:** `clinic doctor -- node app.js`로 이벤트 루프 lag·GC·CPU·핸들 그래프를 한 번에 받기.
  - 이벤트 루프 블로킹 탐지 — `loopbench`, `event-loop-lag`, `perf_hooks.monitorEventLoopDelay()`. p99 lag 50ms 임계.
  - 메모리 누수 사냥 — Anvil과 dev.to의 2GB 누수 회고 사례. retainer chain을 어떻게 읽는가.
  - Netflix flame graph 사례 — production에서 정규식 한 줄이 핫스팟이었다는 회고. 도구 없으면 영영 못 찾는 종류의 버그.
  - 운영에서의 헬스 체크 + 디버깅 통합 — 트래픽 빠진 인스턴스에서만 스냅샷 받기.
- **Java/Spring 비교 포인트:** "도구 이름이 다 바뀌지만 사고 방식은 같다"는 메시지를 표 + 본문으로 강하게 가져간다. JFR ↔ clinic flame, MAT ↔ Chrome DevTools Memory의 사고 방식 매핑.
- **인용할 리서치 자료:** §4.5 전체, §3.3(Netflix flame graph), §6의 팁 1번(이벤트 루프 막지 마라), §7의 Anvil 메모리 누수 회고, dev.to 2GB 누수 회고.
- **예상 분량:** 약 30페이지(약 24,000자).

---

### 7장. 배포와 운영 — 컨테이너 시대의 Node 운영 매뉴얼

- **부제:** PM2·Docker·Kubernetes, Pino·OpenTelemetry·APM, graceful shutdown
- **핵심 질문:** Spring Boot fat jar 한 개를 던지던 운영 모델이 Node로 오면 어떻게 바뀌는가? 그리고 무엇이 그대로인가?
- **주요 내용 (12불릿):**
  - 도입 — fat jar 모델 vs "node 런타임 + 프로젝트 + node_modules" 모델. Docker가 사실상 표준 단위가 된 이유.
  - PM2 cluster vs Node `cluster` 모듈 vs Docker — 어디서 어느 도구가 맞는가.
  - K8s 안에서 PM2 cluster를 빼야 하는 이유 — K8s가 이미 재시작·스케일링을 담당.
  - **YAML 예시:** Node 앱의 minimal Dockerfile + K8s Deployment(liveness/readiness/`terminationGracePeriodSeconds` 포함).
  - graceful shutdown — SIGTERM → HTTP close → DB/큐 close → 진행 중 잡 마무리 → exit. PM2 SIGINT + 1.6초 SIGKILL의 기본값. Spring Boot 2.3+의 `server.shutdown=graceful` 비교.
  - **TS 코드 예시:** NestJS `enableShutdownHooks()` + 커스텀 `OnApplicationShutdown` 서비스로 graceful shutdown 구현.
  - 로깅 — Pino vs Winston 성능 표(§4.7). Pino + `@opentelemetry/instrumentation-pino`로 trace_id 자동 주입. Logback + MDC와의 사고 방식 매핑.
  - **TS 코드 예시:** Pino 구조화 로그 + correlation id + OTel trace context 자동 주입.
  - APM — Datadog/New Relic/Dynatrace + OpenTelemetry SDK. Spring의 Micrometer + Actuator와 매핑.
  - 헬스 체크 — `@nestjs/terminus`(liveness/readiness 분리), Express는 직접 미들웨어. Spring Actuator `/actuator/health`와 정확히 같은 자리.
  - Lambda 콜드 스타트 운영 디테일 — Provisioned Concurrency, init phase 외부화 패턴.
  - 운영 체크리스트 — 첫날부터 넣어야 할 항목 10개(graceful shutdown, 구조화 로깅, OTel, 헬스 체크, lag 모니터, …).
- **Java/Spring 비교 포인트:** Spring Actuator·Micrometer·Logback·MDC가 NestJS Terminus·OpenTelemetry·Pino·correlation id로 어떻게 옮겨지는지 본문 흐름의 축. fat jar의 부재가 만드는 운영 사고방식의 차이.
- **인용할 리서치 자료:** §4.6 전체, §4.7 전체, §6의 팁 5/6/7번, §7의 dev.to/prateekbka(PM2 vs Cluster vs Docker)와 trendyol-tech(Spring Boot graceful shutdown). 콜드 스타트 비교는 §4.6의 dev.to/aws와 arnoldgalovics.com.
- **예상 분량:** 약 36페이지(약 28,000자).

---

### 8장. Java/Spring에서 Node.js로 — 마이그레이션 전략 (책의 절정)

- **부제:** PayPal·LinkedIn·Netflix·Walmart·당근마켓이 갔던 길, Uber가 돌아온 길, 그리고 우리가 갈 길
- **핵심 질문:** 우리 팀의 어느 경계부터 Node로 잘라내야 하는가? 그리고 어떤 신호가 보이면 멈춰야 하는가?
- **주요 내용 (14불릿):**
  - 도입 — "갈아탔다는 사례만 보면 안 된다." 책의 메시지를 가장 강하게 깐다.
  - 사례 1 — **PayPal 계정 개요 페이지**. 가장 많이 접근되는 페이지를 Java에서 Node로. 인력 5명(Java) vs 2명(Node), 처리량 2배 RPS, 응답 35% 감소, 코드 33% 감소·40% 적은 파일. Express 비강제성 → 사내 Kraken.js로 컨벤션 강제.
  - 사례 2 — **LinkedIn**. 모바일 백엔드를 Rails에서 Node로. 서버 30대 → 3대, 10배 헤드룸, 약 20배 처리, 코드 60K → 2K 라인. "다른 서비스와 대화하기"가 Node의 강점이라는 교훈.
  - 사례 3 — **Netflix UI 서버**. 시작 시간 40분 → 1분 미만, 응답 70% 감소. Java 마이크로서비스를 그대로 두고 BFF 레이어만 Restify·Docker로 분리. Java 완전 대체가 아니었다는 사실.
  - 사례 4 — **Walmart Black Friday**. 모바일 70%, IO 바운드 + SSR. 55% 트래픽이 Node로 갈 때 CPU 1%, 15억 달러 처리. "convoy effect"라는 운영 함정과 hula-hoop·CDN 전략(1장에서 흘려둔 힌트의 회수).
  - 사례 5 — **당근마켓 푸시 알림**. Rails에서 Node + TS로 분리. 1,500 RPS 누락 없는 처리. 한국 사례.
  - 사례 6 — **Uber의 후퇴**. RTAPI를 Node로 만들었다가 2018년 신규 권장 스택에서 Node + HTTP/JSON 제외. 신규 엔지니어 온보딩 비용. "기술 선택의 정답은 시점·조직·도메인에 따라 다르다"는 메시지.
  - Strangler Fig 패턴 — Martin Fowler 정의에서 출발해 단계별 분해.
    1. API Gateway 분리(NGINX/Envoy/AWS API Gateway).
    2. 공유 DB 단계 — 새 Node 서비스가 모놀리스 DB 직접 읽기.
    3. DB 분리(CDC/이벤트 스트림) — Debezium·Kafka로 점진적 데이터 이전.
    4. 트래픽 점진 이전 — feature flag, canary, shadow traffic.
    5. anti-corruption layer — 모놀리스 도메인이 새 시스템에 새지 않게.
  - **다이어그램:** Strangler Fig 5단계의 시퀀스 그림. 각 단계마다 "Spring 모놀리스에 어떤 변경이 들어가는가"를 한 줄씩.
  - 결정 트리 — "BFF부터 시작하라"의 근거(PayPal·Netflix). 핵심 도메인 서비스는 마지막에. CPU 바운드는 worker_threads 또는 다른 언어 마이크로서비스로.
  - 후퇴 신호 체크리스트 — 신규 엔지니어 온보딩 시간, 이벤트 루프 lag p99, CPU 바운드 비중, 운영 사고 빈도, 커뮤니티/사내 라이브러리 부채.
  - **TS 코드 예시:** Spring 모놀리스 앞단에 NestJS BFF를 두고 일부 라우트만 받아내는 최소 Skeleton. Spring REST 호출을 anti-corruption layer로 감싸 새 도메인 모델로 변환하는 코드.
  - 학술적 뒷받침 — IEEE 2021 "Microservice Migration Using Strangler Fig Pattern: A Case Study on the Green Button System" 인용.
  - 마이그레이션 6개월 로드맵 샘플 — 1개월 BFF 셋업, 2~3개월 한 도메인 이전, 4개월 운영 안정화, 5~6개월 다음 도메인.
- **Java/Spring 비교 포인트:** 이 챕터는 비교 자체가 본문이다. Spring 모놀리스가 어떻게 변형되며 Node 서비스가 옆자리에 들어오는지, 어디서 데이터·도메인 모델을 어떻게 분리하는지가 모두 Spring 운영 경험을 전제로 풀린다.
- **인용할 리서치 자료:** §3 전체(6개 케이스 모두), §4.9 전체(Strangler Fig 단계·실패 사례), §5.6(모놀리스 vs 마이크로서비스 균형), §6의 팁 8번(BFF부터)과 9번(CPU 바운드 분리). PayPal·LinkedIn·Netflix·Walmart·당근마켓·Uber 6개 사례를 균형 있게 배치.
- **예상 분량:** 약 50~52페이지(약 40,000자) — 책의 절정으로서 다른 챕터보다 두껍게.

---

### 9장. 결정과 설득 — 팀과 커리어에 Node를 들이는 법

- **부제:** 도입을 설득할 언어, 후퇴를 결정할 신호, 그리고 다음 한 걸음
- **핵심 질문:** 8장의 결정을 가지고 조직 안으로 돌아갈 때 무엇이 필요한가? 그리고 이 책을 덮고 나서 가장 먼저 해야 할 일은 무엇인가?
- **주요 내용 (10불릿):**
  - 팀 안에서의 도입 설득 — 기술 선택 회의에서 "왜 Node인가"를 한 페이지로 답하는 템플릿. 8장 사례를 어떻게 인용할지 포함.
  - 채용·온보딩 — Spring 출신을 Node 팀에 태우는 학습 경로(이 책의 장 순서가 그대로 4~6주 학습 플랜).
  - 코드 리뷰 가이드 — Spring 출신이 Node PR을 볼 때 자주 놓치는 항목 체크리스트(이벤트 루프 블로킹 가능성, `await` 누락, Prisma `select` 누락, graceful shutdown 누락, …).
  - 모놀리스 vs 마이크로서비스의 균형 — modular monolith부터 시작하라는 일반 권고를 Node 맥락에서 어떻게 적용할지.
  - 후퇴 신호 — Uber 사례에서 뽑은 신호를 자기 조직에 어떻게 측정·관찰할지(온보딩 시간, 사내 라이브러리 부채, 운영 사고 빈도).
  - 커리어 신호 — TypeScript가 GitHub 1위, 채용 65%가 TS 요구. Spring 경력 + Node/TS는 어떤 시장 지점에 도달하는가.
  - Bun·Deno의 위치 — Node가 책의 주제이지만 2026년 시점에 알아둘 옵션. 박스 코멘트가 아니라 짧은 절로.
  - JVM 진영과 결별이 아니다 — Java Virtual Threads, GraalVM Native Image, SnapStart의 의미. "두 진영을 같이 돌리는 팀"의 모습.
  - 다음 한 걸음 — 독자 유형별 액션 아이템. 시니어 IC / 테크 리드 / 아키텍트 각각.
  - 닫는 말 — 1장에서 던진 의심에 대한 마지막 대답.
- **Java/Spring 비교 포인트:** 비교가 기술에서 조직·커리어 차원으로 올라온다. "기술 선택은 도구 선택이 아니라 팀의 학습 곡선과 운영 문화의 선택"이라는 메시지를 Spring 진영의 성숙도와 Node 진영의 빠른 변화 양쪽을 인정하는 톤으로 마무리.
- **인용할 리서치 자료:** §3.5(Uber 후퇴 신호), §4.2(TS 시장 신호), §5(논쟁점 5개 영역의 균형), §5.6(modular monolith), §6의 팁 10번(빌드 타임 최적화), §8의 한계 7번(Bun/Deno 박스 코멘트). 1장에서 흘려둔 "단일 스레드는 정말 일감을 감당할 수 있는가" 질문을 여기서 회수해 닫는다.
- **예상 분량:** 약 26페이지(약 20,000자).

---

### 에필로그. 두 런타임을 같이 돌리는 백엔드 개발자

- **분량:** 약 6~8페이지.
- **역할:** 기술적 결론이 아니라 정체성에 대한 마지막 한 마디. "Spring을 떠난 게 아니라 도구가 한 개 늘었을 뿐이다." 1장 프롤로그와 짝을 이뤄 책 전체를 닫는다.

---

## 5. 챕터 간 callback 계획

이 책은 **1장에서 던진 질문이 8~9장에서 회수되는 구조**다. 편집자가 챕터 간 흐름을 점검할 때 참고할 수 있도록 주요 callback을 정리한다.

- **1장 → 8장:** 1장에서 Walmart의 "convoy effect"를 짧게 흘리고, 8장 Walmart 사례에서 이벤트 루프 블로킹과 SSR 페이지 렌더링이 만든 운영 함정으로 회수한다. "이벤트 루프를 막지 마라"는 추상 권고가 8장에서 구체적 사고로 변한다.
- **1장 → 9장:** "단일 스레드는 정말 일감을 감당할 수 있는가"라는 1장의 의심을, 9장 닫는 말에서 PayPal·LinkedIn·Netflix·당근마켓 수치로 답한다. 그리고 Uber 후퇴를 함께 두며 "감당한다, 단 조건이 있다"는 결론으로 닫는다.
- **2장 → 4장:** 2장에서 본 TS 데코레이터·구조적 타입·유틸리티 타입이 4장 NestJS DI/모듈 시스템에서 그대로 사용된다. 2장의 추상 개념이 4장에서 실제 프레임워크로 구체화된다.
- **2장 → 5장:** 2장에서 본 Promise·async/await 패턴이 5장 Prisma `$transaction` 콜백 형태로 다시 등장. "트랜잭션을 닫지 못하고 await을 빠뜨리면 어떤 일이 벌어지는가"가 5장에서 시연된다.
- **3장 → 7장:** 3장의 BullMQ 워커가 7장의 graceful shutdown 절에서 다시 등장. "진행 중 잡을 어떻게 마무리하느냐"가 3장의 큐와 7장의 운영을 잇는다.
- **4장 → 7장:** 4장의 NestJS 모듈/DI가 7장의 `@nestjs/terminus`(헬스 체크)와 `enableShutdownHooks()`(graceful shutdown)에서 운영 측면으로 확장된다.
- **5장 → 8장:** 5장에서 다룬 Prisma `$transaction` 명시성이 8장 Strangler Fig 단계에서 "공유 DB → DB 분리" 단계의 데이터 일관성 도전과 연결된다.
- **6장 → 8장:** 6장의 clinic.js·heap snapshot·이벤트 루프 lag 모니터링이 8장의 후퇴 신호 체크리스트로 회수된다. "도구로 측정하지 못하는 것은 결정할 수 없다."
- **7장 → 9장:** 7장의 운영 체크리스트(graceful shutdown, 구조화 로깅, OTel, 헬스 체크, lag 모니터)가 9장의 코드 리뷰 가이드 체크리스트로 압축·재인용된다.
- **8장 → 9장:** 8장의 6개 사례와 Strangler Fig 패턴이 9장의 도입 설득 템플릿과 후퇴 신호 체크리스트의 직접 인용원이 된다. 8장이 본문이라면 9장은 그 본문을 조직과 커리어 언어로 번역한 부록 같은 본문이다.

---

## 6. 자기 점검 (체크리스트)

- [x] 모든 챕터가 핵심 질문에 답한다 — 1장(런타임 작동 원리), 2장(언어 차이), 3장(패턴 지형), 4장(NestJS vs Spring), 5장(ORM 마법의 부재), 6장(디버깅 도구 매핑), 7장(운영), 8장(마이그레이션 전략), 9장(결정과 설득).
- [x] 챕터 순서에 맥이 흐른다 — 의심·발견 → 도구 익숙해지기 → 실무 현실 → 결단의 곡선.
- [x] 대상 독자 수준에 맞는다 — "콜백 지옥은 무엇인가" 같은 클리셰는 한 단락으로 빠르게 처리, 본질은 비교 관점에 둠.
- [x] 레퍼런스의 9개 영역(§4.1~§4.9)이 모두 1~9장에 매핑됨. 6개 마이그레이션 사례(§3.1~§3.6) 모두 8장에 배치됨. Top 10 헷갈림 지점(§2)은 1·2·4·5·7장에 분산.
- [x] 챕터 간 중복 없음 — Spring 비교는 모든 챕터에 흐르되 각 챕터가 다른 비교 축(스레드 모델·언어·프레임워크·ORM·도구·운영·전략·조직)을 담당.
- [x] 예상 분량 합계 — 8 + 32 + 30 + 36 + 44 + 38 + 30 + 36 + 50 + 26 + 7 ≈ **337페이지** (목표 290~330의 상단). 마이그레이션 챕터에 가중치를 두느라 약간 상향.

---

## 7. 보고

### (1) 저장 절대경로

`/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/nodejs-for-java-developer/nodejs-for-java-developer/02_plan.md`

### (2) 확정한 챕터 수와 총 예상 페이지

- **챕터 수:** 본문 9개 챕터 + 프롤로그/에필로그(짧음).
- **총 예상 페이지:** 약 **337페이지**(약 25만~26만자). 목표 범위 290~350페이지 안. 8장(마이그레이션) 50페이지·4장(NestJS) 44페이지에 무게중심을 두었다.

### (3) 추가로 고려할 만한 챕터·구성 제안 (요청자 검토용)

리서치를 한 번 더 훑으면서 책 구조에 더 넣어볼 만한 것을 짧게 적어둔다. 모두 선택사항이며, 본 계획에는 반영하지 않았다.

1. **"Bun·Deno를 9장 안의 절이 아니라 별도 부록으로 빼는 안."** 2026년 시점에 Bun이 Node 호환 런타임으로 빠르게 자라는 중이라, 부록 A로 20페이지 정도 따로 두는 선택지도 있다. 다만 책의 메시지가 흐려질 위험이 커 본 계획에서는 9장의 한 절로만 두었다.
2. **"보안" 챕터의 부재.** 현재 9개 영역에 보안이 빠져 있다. 7장(운영) 안에 보안 절을 한 개 넣는 정도로는 충분하지 않을 수 있다. JWT/OAuth/CORS/CSP/Rate Limiting/Helmet/의존성 취약점 스캐닝 같은 주제를 별도 챕터(예: 7장과 8장 사이)로 두면 실무 가이드로서 두께가 더 단단해진다. 다만 사용자가 제시한 9개 영역을 존중하기 위해 본 계획에서는 7장 운영의 일부(헬스 체크·로깅) 정도로만 흡수했다.
3. **"테스트" 챕터의 부재.** Jest/Vitest/Supertest/`@nestjs/testing`이 본문에 분산되어 있지만 단독 챕터는 없다. 7장 또는 4장에 테스트 절을 보강할지, 또는 별도 챕터로 둘지는 사용자 판단이 필요한 지점.
4. **사례 균형 보강 — 한국 사례 추가.** 8장에 당근마켓이 들어가 있지만, §3.6과 §8의 한계 2~3번에서 지적했듯이 토스·인프런·LINE의 1차 회고 자료가 빈약하다. Phase 4(챕터 저술) 전에 한국어 1차 자료(toss.tech, line engineering, woowahan tech, kakao tech)에 대한 보강 리서치를 한 번 더 돌리면 8장의 균형이 더 좋아진다.
5. **편집자에게 — 분량 압박이 있을 경우의 우선 축소 후보.** 3장(36p)을 30p로, 6장(30p)을 26p로 줄이는 게 가장 안전하다. 8장과 4장은 책의 정체성이라 줄이지 않는 편이 낫다.

리서치의 한계는 §8에서 자체 적시되어 있고, 본 계획에서는 그 한계를 인지한 상태에서 1차 출처가 단단한 사실 위주로 챕터를 짰다. 한국 사례 보강(위 3번)이 가장 현실적인 다음 작업이다.
