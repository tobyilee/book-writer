# 자바 개발자를 위한 Node.js 저술 계획 (v2)

본 문서는 `01_reference.md`에서 수집한 사실·수치·일화와 `03_review_log.md`의 plan-reviewer 피드백, 그리고 사용자가 확정한 4개 결정을 통합해 책의 구조를 v2로 다시 묶은 것이다. v1과의 차이는 §8(개정 메모)에 정리했다.

이 책은 입문서가 아니다. 이미 백엔드를 운영해본 사람이 두 번째 런타임으로 Node.js를 받아들이는 비교·실무 가이드를 지향한다. 본문 메시지를 한 줄로 못 박으면 이렇다 — **"도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다."** 이 메시지는 1장 도입부, 9장 본문, 그리고 에필로그에서 책 정체성으로 세 번 반복된다.

---

## 1. 책 제목 (확정)

### 최종안

- **제목:** 자바 개발자를 위한 Node.js
- **부제:** Spring 직관을 그대로 들고 가는 두 번째 런타임 가이드
- **슬로건:** "도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다."

후보 A를 채택한 결정의 근거는 두 가지다. 첫째, 서점·온라인 검색에서 "java node 비교", "spring nestjs"로 들어오는 시니어/미드 백엔드 개발자에게 곧장 닿는다. 둘째, 부제의 "두 번째 런타임 가이드"가 이 책이 입문서가 아니라는 신호를 함께 준다. 본문의 비교 톤과도 어긋나지 않는다. 후보 B의 정체성 메시지("도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다")는 제목에서 뺐지만, 본문(1장 도입·9장·에필로그)의 책 정체성 못 박기로 그대로 흡수한다.

### 기각된 후보 (참고)

- **후보 B — "다른 런타임, 같은 백엔드".** 메시지는 단단하지만 "Node.js"·"Spring"·"Java" 키워드 어디에도 직접 안 걸려 검색 진입이 약하다. 메시지는 본문에서 살린다.
- **후보 C — "Spring을 떠나기 전에 — Node.js 실전 가이드".** "떠나기 전에"라는 부정적 프레이밍이 책의 메시지("두 진영 모두 인정")와 어긋난다.

---

## 2. 책 특성

- **장르 포지셔닝:** **비교 기반 실무 가이드.** 입문서가 아니라 "이미 백엔드를 아는 사람의 두 번째 런타임"으로서 위치를 잡는다. 1차 자료·실제 마이그레이션 회고가 본문 안에 녹아드는 회고적 가이드의 톤을 유지한다.
- **분량 목표:** 본문 9개 챕터 + 프롤로그/에필로그. **총 약 365페이지(약 28만~29만자)**. 4장(NestJS+테스트)·7장(운영+보안+CI/CD)·8장(마이그레이션)에 무게중심. 분량이 350p를 넘었으나 §6의 우선 축소 후보(3장·6장)로 마지막 단계에서 350p 이내로 조정 가능. 현재는 350p에 약간 여유를 두는 안으로 둔다.
- **난이도:**
  - 진입: 백엔드 5년 이상, Spring/JPA/Kotlin·Java 운영 경험 있음. JS는 "써본 적은 있지만 본격적으로 백엔드를 짜본 적은 없다." async/await의 모양은 알지만 이벤트 루프 모델을 자기 언어로 설명하지는 못한다.
  - 도착: NestJS로 작은 서비스를 직접 설계·운영하고, BFF 또는 마이크로서비스 한 조각을 Strangler Fig 패턴으로 마이그레이션할 수 있다. Node 운영 도구 체인(clinic.js, Pino, OpenTelemetry, PM2/K8s, Helmet/JWT, Jest/Supertest, GitHub Actions)을 JVM 도구와 매핑해 머릿속에 가지고 있다.
- **독자 여정 한 줄:** 1장에서는 "Node.js가 정말 백엔드 일감을 감당할 수 있을까"를 의심하던 독자가, 8장 후반에서는 "우리 팀의 어느 경계부터 잘라내 Node로 옮길지"를 결정할 수 있게 된다. 9장과 에필로그에서는 그 결정을 조직 안에서 설득할 언어와, "두 진영을 같이 돌리는" 정체성을 갖는다.
- **톤(스타일 가이드 준수):**
  - 평어체 기반(`-다`, `-한다`)에 청유형(`살펴보자`, `옮겨보자`, `생각해보자`)을 적극 섞는다.
  - 새 개념을 도입할 때 수사적 질문(`왜 그럴까?`, `그렇다면 어떻게 다를까?`)을 먼저 던진다.
  - 상황 가정(`Spring 모놀리스를 운영해온 팀이 있다고 해보자`)으로 들어간다.
  - "난감하다", "찜찜하다", "번거롭다" 같은 감정 어휘를 비교 지점에서 자연스럽게 사용한다.
  - "Java/Spring에서는 X였지만 Node.js에서는 Y다"라는 비교 구도가 부록·박스가 아니라 본문 흐름의 일부로 흐른다.
  - 의사결정·체크리스트 형식은 본문에서는 산문으로 풀고, 표·체크리스트 자체는 절 끝의 정리 자료로만 둔다 (요청 5 반영).

---

## 3. 내러티브 아크

이 책은 **의심 → 발견 → 도구 익숙해지기 → 실무 현실 → 결단 → 정체성 회복**의 곡선으로 흐른다.

1~2장은 **의심과 발견**의 구간이다. 1장 도입은 추상으로 시작하지 않고 Walmart의 "10~80ms convoy effect" 일화로 곧장 들어간다. "단일 스레드가 막히면 어떤 일이 벌어지는가"의 구체적 그림을 1장에서 한 번 보여주고, 8장에서 같은 사례를 "왜 SSR을 CDN으로 빼야 했는가"의 결정 차원으로 다시 본다. 2장은 JS·TS의 모양을 Java/Kotlin과 나란히 두고, 챕터 끝에 npm·pnpm·Bun과 monorepo·workspaces를 Maven multi-module/Gradle composite와 매핑하는 짧은 절을 둔다.

3~5장은 **도구를 다루는 손에 익히는 구간**이다. 3장은 LinkedIn의 "다른 서비스와 대화하기"라는 BFF 강점을 도입에 한 단락 깔아 단순 도구 나열을 막는다. 4장은 PayPal의 "Express 비강제성 → Kraken.js 컨벤션 강제" 일화와 t2.micro CPU 후기를 결합해 "구조 강제의 필요성"을 이중으로 보여준 뒤 NestJS와 Spring Boot를 정면으로 맞붙인다. 4장은 책의 첫 번째 두께 있는 챕터로, NestJS 테스트 절(6p)이 Spring `@SpringBootTest`/`@MockBean` 매핑과 함께 들어간다. 5장은 ORM이다. Hibernate에서 자라온 사람에게 "마법의 부재"가 어떤 충격인지 정직하게 다룬다.

6~7장은 **실무 현실**로 진입한다. 6장은 Netflix의 "production에서 정규식 한 줄이 핫스팟이었다" flame graph 일화로 진입하고, 도구 매핑 표는 일화 다음에 둔다. 7장은 운영의 절정이다 — PM2/Docker/K8s 배포·Pino/OTel 로깅·헬스체크에 더해 보안 운영 6p(Helmet·CORS·JWT·OAuth·Rate Limit·의존성 스캔)와 Node 빌드 파이프라인 4p(GitHub Actions·esbuild/SWC·멀티 아키텍처 Docker·자동 보안 스캔)가 추가된다. 6~7장을 마치면 독자는 손에 도구가 들려 있는 상태다.

8~9장이 **결단의 구간**이다. 8장은 책의 절정이다. 1·3·4·6장에서 본 사례들(Walmart·LinkedIn·PayPal·Netflix)을 "다시 보자"의 형식으로 모아내고, 거기에 Uber 후퇴와 한국 사례를 더해 결정 차원으로 통합한다. Strangler Fig 패턴을 단계별로 풀고, 모놀리스 → BFF → 부분 마이크로서비스로 가는 결정 시나리오를 산문으로 제시한다. 9장은 이를 조직과 커리어 차원으로 끌어올린다 — 도입 설득 언어, PR 리뷰의 함정, 후퇴 신호 측정.

마지막은 **정체성 회복**이다. 에필로그에서 "JVM 진영과 결별이 아니다"라는 메시지를 흡수해, Java Virtual Threads·GraalVM Native Image·SnapStart의 자리를 인정한다. "두 런타임을 같이 돌리는 백엔드 개발자"가 1장 도입의 의심에 대한 마지막 대답이 된다.

이 곡선의 핵심은, 독자가 도구만 바꾸면서 자기 백엔드 직관을 재확인하게 만든다는 점이다. **"내가 Spring에서 풀던 문제는 Node에서도 똑같은 문제다, 다만 도구의 이름이 다를 뿐이다."** 이 메시지가 1장 도입·9장·에필로그에서 책 정체성으로 세 번 박힌다.

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
- **주요 내용:**
  - **도입(1p) — Walmart Black Friday convoy effect.** "페이지 한 번 렌더링에 10~80ms가 걸리고, 그 사이 들어온 다른 요청들이 줄을 선다." 단일 스레드가 막히면 어떤 일이 벌어지는지 8장 회수 전에 1장이 직접 한 번 보여준다 (요청 2·요청 4 반영).
  - 도입 마무리 — Spring 서블릿이 "요청 = 스레드"였다는 사실을 한 단락으로 환기. "왜 단일 스레드 쪽은 멈추지 않을까"라는 의심을 본문 첫 질문으로.
  - V8 엔진의 위치 — JIT 컴파일이 JVM의 HotSpot/G1과 어떻게 닮고 다른지.
  - libuv의 이벤트 루프 6단계(timers → pending → idle/prepare → poll → check → close)를 그림과 함께. epoll/kqueue 위에서 어떻게 도는지.
  - 워커 스레드 풀(기본 4개)의 역할 — 파일 I/O·DNS·crypto가 어디로 가는지.
  - **JS 코드 예시:** `setTimeout` + `setImmediate` + `process.nextTick`의 실행 순서를 보여주는 짧은 스크립트.
  - "이벤트 루프를 막는다"의 실체 — CPU 바운드 코드 한 줄이 모든 사용자를 줄 세우는 시연 코드. Walmart 사례를 다시 한 번 짚어 "convoy effect가 코드 한 줄에서 어떻게 발생하는가"를 보여준다.
  - **TS 코드 예시:** `perf_hooks.monitorEventLoopDelay()`로 p99 lag 측정하기.
  - Worker Threads의 위치 — Java의 ForkJoinPool과 닮은 점, V8 인스턴스를 따로 갖는 비용.
  - Java Virtual Threads(Project Loom)와의 비교 — 같은 목적지(높은 동시성), 다른 길.
  - GC 비교 — V8의 New/Old Space와 JVM의 G1/ZGC. Node가 큰 힙을 안 다루는 이유.
  - **닫는 한 단락 — 책 정체성 첫 못박기.** "도구만 바뀌었을 뿐, 우리가 다루는 동시성 문제 자체는 같다." 9장과 에필로그에서 이 문장이 다시 등장한다.
- **Java/Spring 비교 포인트:** 서블릿 스레드 풀 vs 이벤트 루프, ThreadPoolExecutor vs Worker Threads, Loom vs async/await을 본문 안에 맞물려 풀어낸다. 부록이 아니다.
- **인용할 리서치 자료:** §3.4(Walmart, 도입 일화), §1.1, §1.2 (libuv·V8·이벤트 루프 단계), §2의 Top 10 중 1번(단일 스레드 충격), §4.1(Don't block the event loop, Worker Threads, Virtual Threads 비교), §4.5(이벤트 루프 블로킹 탐지).
- **예상 분량:** 약 33페이지(약 26,000자) — Walmart 도입 1p 추가로 v1 32p에서 +1p.

---

### 2장. JavaScript와 TypeScript — Java 개발자가 다시 학습할 것과 그대로 쓸 것

- **부제:** 구조적 타입, 클로저, Promise, 그리고 npm·pnpm·monorepo의 자리
- **핵심 질문:** Kotlin·Java 출신이 TypeScript에서 가장 헷갈리는 지점은 어디고, 반대로 그대로 가져갈 수 있는 직관은 무엇인가? 그리고 의존성·빌드 도구 운영은 Maven/Gradle과 어떻게 다른가?
- **주요 내용:**
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
  - **신설 절 — 패키지 관리와 모노레포(3~4p, 요청 4 표 채택 반영).** npm vs pnpm vs yarn vs Bun의 차이(설치 속도·디스크 점유·hoisting 동작), `package-lock.json`/`pnpm-lock.yaml`의 의미, npm `workspaces`·pnpm·Turborepo/Nx로 모노레포를 구성하는 방법, Maven multi-module/Gradle composite와의 매핑. Spring 모듈 프로젝트 출신에게 직접 매핑되는 개념이라 본문 뒷부분에 자연스럽게 자리잡는다.
- **Java/Spring 비교 포인트:** 명목적 타입과 구조적 타입의 사상 차이를 본문에서 정면으로 다룬다. CompletableFuture와 async/await의 모양은 비슷해도 사용 패턴이 다르다는 점, Kotlin의 `suspend`와 JS의 async/await을 한 페이지에 병치하는 코드 비교를 넣는다. 마지막 절에서 의존성·빌드 운영을 Maven/Gradle과 직접 매핑.
- **인용할 리서치 자료:** §2의 Top 10 중 2번(this), 3번(Promise), 7번(타입 시스템), §4.2 전체. Kotlin suspend ↔ JS await 비교는 §7의 Joffrey Bion 글. TS 시장 신호(GitHub 1위, 채용 65%)는 §4.2의 tech-insider.org 출처. 패키지 관리 절은 §1.3(npm vs Maven/Gradle 표), §7의 ksaquib·tomgregory 출처에서 출발하되 monorepo·pnpm·Bun은 추가 1차 자료(npm Docs, pnpm Docs)를 본문 작성 시 보강.
- **예상 분량:** 약 33페이지(약 26,000자) — v1 30p에 패키지 관리 절 3p 추가.

---

### 3장. 활용 패턴의 지형 — REST·GraphQL·CLI·워커·WebSocket·서버리스

- **부제:** Spring 진영의 어떤 도구가 Node에서는 어디에 있는가
- **핵심 질문:** Spring MVC, Spring Batch, Spring WebFlux, Spring Cloud Function… 각각의 자리에 Node에서는 무엇이 있는가? 그리고 어디서 모양이 갈라지는가?
- **주요 내용:**
  - **도입(1단락) — LinkedIn의 BFF 강점 일화.** §3.2의 LinkedIn 사례에서 "Node의 강점은 다른 서비스와 대화하기"라는 교훈을 한 단락으로 풀어, 이 장이 단순 도구 나열이 아니라 "Node가 어디서 강점을 보이는가"의 관점으로 시작되게 한다 (요청 4 반영). 8장에서 LinkedIn 사례의 수치(서버 30대 → 3대)를 다시 본다.
  - REST: Express(생태계) / Fastify(성능) / NestJS(구조)의 삼각 구도. JAX-RS·Spring MVC와의 매핑.
  - **TS 코드 예시:** 같은 엔드포인트를 Spring Boot 컨트롤러와 NestJS 컨트롤러로 나란히 보여주는 비교 코드(이 챕터의 시그니처 페이지).
  - GraphQL: Apollo·Mercurius. NestJS의 DI와 결합한 request scope DataLoader가 N+1을 어떻게 푸는가.
  - **TS 코드 예시:** NestJS + DataLoader로 N+1을 막는 짧은 리졸버.
  - CLI: commander/yargs/oclif는 picocli의 자리. Vite/esbuild로 단일 실행 파일 번들링.
  - 백그라운드 워커: BullMQ가 사실상 표준. Spring Batch와 다른 모델(분산 큐 + 워커 풀), 우선순위·재시도·딜레이·repeatable cron.
  - **TS 코드 예시:** BullMQ로 이메일 발송 잡을 정의하고 워커가 처리하는 짧은 코드.
  - WebSocket: Socket.IO(폴리필 + 자체 프레이밍) vs `ws`(raw). Spring WebFlux + STOMP의 RabbitMQ 통합과 무엇이 다른가.
  - 서버리스: Lambda·Vercel·Cloudflare Workers. Spring Boot Lambda 콜드 스타트 3~10초(SnapStart 1.5초/180ms) vs Node 200ms 미만 — 왜 이 격차가 본질적인가.
  - **패턴 선택 — 산문으로 풀기 (요청 5 반영).** "이때는 어떻게 결정해야 할까?"의 수사적 질문으로 진입한 뒤, "트래픽이 종일 평탄하면 컨테이너, 들쭉날쭉하면 서버리스. 큰 팀 + 여러 도메인이면 NestJS, 짧은 수명 + 작은 팀이면 Fastify"의 산문 시나리오. 표는 절 끝에 정리 자료로만.
- **Java/Spring 비교 포인트:** Spring 진영의 풀 스택 매트릭스(MVC/Batch/WebFlux/Cloud Function)를 Node 도구와 일대일로 짝지은 표를 챕터 후반에 둔다. 본문은 산문으로 흐르고, 표는 정리.
- **인용할 리서치 자료:** §3.2(LinkedIn BFF, 도입 일화), §4.3 전체, §4.4의 Express/Fastify 표, §4.7의 콜드 스타트 수치, §3.6의 당근마켓 푸시 알림 사례(BullMQ 위치 강화). GraphQL N+1은 §4.3의 dev.to/tugascript와 wanago.io 출처.
- **예상 분량:** 약 32페이지(약 25,000자) — v1 36p에서 산문화·요청 다이어트로 -4p (분량 압박 시 추가 다이어트 후보).

---

### 4장. NestJS와 Spring Boot — 가장 닮은 두 프레임워크의 정면 비교

- **부제:** 모듈, DI, 데코레이터, 인터셉터·가드, 그리고 테스트 — Spring Boot 출신의 통념이 흔들리는 자리
- **핵심 질문:** Spring Boot 출신이 NestJS를 처음 쓸 때 가장 자주 데이는 지점은 어디인가? 그리고 어디서 Spring이 그리워지고, 어디서 NestJS가 더 가뿐한가?
- **주요 내용:**
  - **도입(1.5p) — PayPal Kraken.js + t2.micro 결합 (요청 4 반영).** §3.1 PayPal에서 Express의 비강제성이 큰 팀에선 일관성 문제로 이어져 사내 Kraken.js로 컨벤션을 강제했다는 일화 한 단락. 거기에 §4.4의 dev.to/digvijay "t2.micro 무부하 27~29% → 6~7%" 후기를 결합해 "구조 강제의 필요성과 가벼움의 약속"이 한 도입에서 같이 보이게 한다. 8장에서 PayPal 사례의 수치(2배 RPS, 35% 응답 감소)를 다시 본다.
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
  - **결정 가이드 — 산문으로 풀기 (요청 5 반영).** "팀 규모 5명 이하 + 마이크로서비스 3개 이하면 Fastify가 더 가볍다. 그 위로 올라가면 NestJS의 모듈 그래프가 짐을 덜어준다."의 산문 시나리오. 비교 표는 본문 끝 한 페이지 정리 자료로만.
  - **신설 절 — NestJS 테스트 (6p, 요청 1 + 사용자 결정 2 반영).** `@nestjs/testing`의 `Test.createTestingModule`이 Spring `@SpringBootTest`/`@MockBean`과 어떻게 매핑되는가. Jest vs Vitest의 차이(Vitest의 Vite 친화성, ESM 지원). Supertest로 컨트롤러 통합 테스트 작성하기. 트랜잭셔널 롤백 패턴(테스트마다 트랜잭션 롤백으로 격리). **TS 코드 예시:** `Test.createTestingModule`로 의존성 주입을 mock한 단위 테스트 + Supertest로 HTTP 통합 테스트를 한 파일에 묶은 코드. 8장 마이그레이션 사례에서 "테스트 커버리지가 어떻게 옮겨갔는가" 한 단락이 이 절을 callback한다.
- **Java/Spring 비교 포인트:** 이 챕터는 책에서 비교 밀도가 가장 높다. 거의 모든 절이 Spring과의 정면 매핑이고, 코드도 양쪽을 함께 보여준다. "DI는 진짜 DI인가"를 회피하지 않고, 테스트 도구 매핑까지 정면으로 다룬다.
- **인용할 리서치 자료:** §3.1(PayPal Kraken.js, 도입), §4.4 전체, §5.2(NestJS 호불호), §2의 Top 10 중 4번(`forwardRef`), §3.6(국내 NestJS 도입 — 토스·당근마켓·인프런 언급은 1차 출처 한계까지 적시), §4.4의 dev.to/digvijay 후기와 agilecoding.io의 Spring/Kotlin 20년차 회고, Hacker News의 진짜 DI 논쟁. 테스트 절은 NestJS 공식 문서(testing), Jest·Vitest 공식 문서, Supertest 문서를 1차 출처로(본문 작성 시 추가 발굴).
- **예상 분량:** 약 50페이지(약 39,000자) — v1 44p + 테스트 절 6p (사용자 결정 2 반영).

---

### 5장. ORM과 데이터베이스 — Hibernate의 마법이 사라진 자리

- **부제:** Prisma, Drizzle, TypeORM, 그리고 명시적 트랜잭션의 세계
- **핵심 질문:** JPA/Hibernate에서 자라온 개발자가 Prisma를 처음 만났을 때 어떤 감각이 사라졌다고 느끼는가? 그 사라짐을 어떻게 설계로 메우는가?
- **주요 내용:**
  - 도입 — "Hibernate의 마법이 그립다"는 감각을 한 단락으로 정직하게 꺼낸다. lazy loading, dirty checking, `@Transactional` AOP가 모두 없거나 다르다는 사실을 미리 던져둔다.
  - Prisma vs Drizzle vs TypeORM 비교표는 챕터 끝 정리 자료로 둔다. 본문은 산문 흐름으로 (요청 5 반영).
  - Prisma의 명시적 `include`/`select` — Hibernate의 lazy proxy와 정면 비교.
  - **TS 코드 예시:** Prisma로 user + posts를 한 번에 가져오는 `findMany({ include: { posts: true } })`와, 빠뜨렸을 때 `user.posts`가 `undefined`가 되는 시연.
  - LazyInitializationException이 사라진 대신 "왜 user.posts가 undefined냐"가 새 질문이 된다는 사실.
  - Unit of Work의 부재 — Hibernate는 세션 안 변경을 자동 추적해 flush 시 SQL 생성. Prisma는 메서드 호출이 곧 SQL. Prisma 이슈 #4991의 오랜 요청을 인용.
  - 트랜잭션 — `@Transactional` AOP 마법 vs `prisma.$transaction([...])` 또는 콜백. 분산 트랜잭션·Saga는 별도라는 점.
  - **TS 코드 예시:** Prisma `$transaction`으로 두 쓰기를 묶는 코드와, Spring의 `@Transactional` 자바 코드 병치.
  - Drizzle의 위치 — JOOQ/Querydsl과 닮은 SQL-가까운 모델, Edge·Lambda에 강한 가벼움.
  - Mongoose — Spring Data MongoDB의 자리. 스키마와 타입의 결합.
  - Redis — `ioredis`/`node-redis`. Spring Data Redis와 동일한 Pub/Sub·스트림·Lua 패턴.
  - **선택 가이드 — 산문으로 (요청 5 반영).** "Hibernate가 그리우면 Prisma, JOOQ가 그리우면 Drizzle, 마이그레이션 안정성이 최우선이면 Prisma."를 산문 흐름으로 풀고, 비교 표는 절 끝.
- **Java/Spring 비교 포인트:** "Hibernate-like 마법은 적지만 타입 안전이 강하다"는 프레이밍을 본문 흐름의 축으로 삼는다. dirty checking·lazy loading·`@Transactional` AOP의 부재를 단점이 아니라 "다른 설계"로 풀어낸다.
- **인용할 리서치 자료:** §4.8 전체, §2의 Top 10 중 5번(lazy loading)과 6번(트랜잭션), §5.3(ORM 논쟁), §6의 팁 4번(N+1 방지). Prisma 공식 문서 두 페이지(transactions, relation queries)와 GitHub 이슈 #4991, betterprogramming.pub의 "Hibernate is not so evil" 글을 같이 인용.
- **예상 분량:** 약 38페이지(약 30,000자) — v1과 동일.

---

### 6장. 디버깅 — JVM 도구 체인을 Node 도구 체인으로 옮기기

- **부제:** jstack·jmap·VisualVM 대신 `--inspect`·clinic.js·heap snapshot
- **핵심 질문:** 운영 중인 Spring Boot 앱에서 jstack/jmap을 떴던 손이, Node.js 앞에서 어떤 명령을 치게 되는가? 그리고 어디서 도구의 사상이 갈라지는가?
- **주요 내용:**
  - **도입(1.5p) — Netflix flame graph 일화 (요청 2·요청 4 반영).** §3.3 Netflix가 production node.js에서 정규식 한 줄이 핫스팟임을 flame graph로 발견했다는 일화. "도구가 없으면 영영 못 찾을 종류의 버그"라는 한 줄로 6장의 핵심 질문("어디서 도구의 사상이 갈라지는가")을 본문 첫 장면으로 가져온다. 표는 일화 다음에. v1에서는 표가 도입이었으나 일화로 바꾼다.
  - JVM 도구 ↔ Node 도구 매핑 표(§4.5). 일화 다음에 정리 자료로 두고 본문이 그 표를 풀어낸다.
  - `--inspect` + Chrome DevTools — VisualVM의 자리. 원격 디버깅, 브레이크포인트, CPU 프로파일.
  - **CLI 예시:** 원격 컨테이너의 Node 프로세스에 `--inspect=0.0.0.0:9229`로 접속하고 SSH 포트포워딩으로 DevTools 붙이기.
  - 힙 스냅샷 — `v8.writeHeapSnapshot()`, `--heapsnapshot-signal=SIGUSR2`. 힙의 약 2배 메모리를 잠시 더 쓰며 이벤트 루프를 막는다는 운영 주의사항.
  - clinic.js 3종(doctor/flame/bubbleprof) — JFR과 async-profiler의 자리에 있는 Node 도구들.
  - **CLI 예시:** `clinic doctor -- node app.js`로 이벤트 루프 lag·GC·CPU·핸들 그래프를 한 번에 받기.
  - 이벤트 루프 블로킹 탐지 — `loopbench`, `event-loop-lag`, `perf_hooks.monitorEventLoopDelay()`. p99 lag 50ms 임계.
  - 메모리 누수 사냥 — Anvil과 dev.to의 2GB 누수 회고 사례. retainer chain을 어떻게 읽는가.
  - 운영에서의 헬스 체크 + 디버깅 통합 — 트래픽 빠진 인스턴스에서만 스냅샷 받기.
- **Java/Spring 비교 포인트:** "도구 이름이 다 바뀌지만 사고 방식은 같다"는 메시지를 일화 + 표 + 본문으로 강하게 가져간다. JFR ↔ clinic flame, MAT ↔ Chrome DevTools Memory의 사고 방식 매핑.
- **인용할 리서치 자료:** §3.3(Netflix flame graph, 도입 일화), §4.5 전체, §6의 팁 1번(이벤트 루프 막지 마라), §7의 Anvil 메모리 누수 회고, dev.to 2GB 누수 회고.
- **예상 분량:** 약 28페이지(약 22,000자) — v1 30p에서 -2p 다이어트 (분량 압박 대응, 요청 다이어트 후보로 명시되어 있어 사전 적용).

---

### 7장. 배포·운영·보안·CI/CD — 컨테이너 시대의 Node 운영 매뉴얼

- **부제:** PM2·Docker·Kubernetes, Pino·OpenTelemetry, graceful shutdown, 보안 운영, 그리고 빌드 파이프라인
- **핵심 질문:** Spring Boot fat jar 한 개를 던지던 운영 모델이 Node로 오면 어떻게 바뀌는가? 그리고 보안·테스트·CI/CD까지 한 챕터 안에서 운영 그림이 완성되려면 무엇이 필요한가?
- **주요 내용:**
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
  - **신설 절 — 보안 운영 (6p, 요청 1 + 사용자 결정 2 반영).**
    - Helmet 미들웨어로 보안 헤더 일괄 설정 (Express 미들웨어, NestJS는 `app.use(helmet())`).
    - CORS 정책 — Spring `WebMvcConfigurer.addCorsMappings` ↔ Express `cors`/NestJS `enableCors`.
    - JWT vs 세션 — stateless API 게이트웨이의 표준은 JWT. Spring Security JWT 필터 ↔ NestJS `JwtAuthGuard`.
    - OAuth — Passport.js + `@nestjs/passport`로 Google/GitHub/회사 SSO 붙이기. Spring Security OAuth2 Client와의 매핑.
    - Rate Limiting — `express-rate-limit`, `@nestjs/throttler`. Spring `RateLimiter`/Bucket4j와의 사고 방식 매핑.
    - 의존성 취약점 스캔 — `npm audit`, Snyk, Dependabot. Spring 진영의 OWASP Dependency-Check와 같은 위치.
    - 메서드 레벨 권한 — Spring Security `@PreAuthorize` ↔ NestJS 가드 + 커스텀 데코레이터로 동등한 표현 만들기.
    - **TS 코드 예시:** NestJS에 Helmet + CORS + JWT 가드 + Throttler를 한 모듈에서 묶어 적용한 코드.
  - **신설 절 — Node 빌드 파이프라인 (4p, 사용자 결정 4 반영).**
    - GitHub Actions·GitLab CI에서 Node 빌드 캐시 — `actions/setup-node@v4` + `cache: 'npm'`/`'pnpm'`로 의존성 캐시. Spring 진영의 Maven dependency cache와 같은 사고 방식.
    - esbuild/SWC 통합 — `tsc`만 쓰면 빌드 타임이 분 단위로 늘 수 있다. esbuild·SWC로 분 → 초.
    - 멀티 아키텍처 Docker 빌드 — `docker buildx` + QEMU로 amd64/arm64 둘 다 산출. Spring Boot Buildpacks와의 비교.
    - 자동 보안 스캔 CI 통합 — Snyk·Dependabot을 PR 단계에서 자동 실행, Spring Boot Maven `dependency-check` 플러그인과 같은 위치.
    - Spring Boot Maven/Gradle 파이프라인과의 비교 — Maven `verify` 단계가 Node에서는 `npm run lint && npm test && npm audit && npm run build`의 명시적 체이닝으로 펼쳐진다.
    - **YAML 예시:** Node 프로젝트의 GitHub Actions 워크플로우 한 개 — install·lint·test·audit·build·multi-arch docker push까지.
  - 운영 체크리스트 — 첫날부터 넣어야 할 항목을 산문 흐름으로 풀고, 절 끝에 정리 자료로 한 페이지(요청 5 반영). graceful shutdown, 구조화 로깅, OTel 자동 계측, liveness/readiness, lag 모니터, 보안 헤더, JWT 검증, Rate Limit, npm audit CI 통합, multi-arch 이미지.
- **Java/Spring 비교 포인트:** Spring Actuator·Micrometer·Logback·MDC·Spring Security·Maven 파이프라인이 NestJS Terminus·OpenTelemetry·Pino·correlation id·Helmet+JWT 가드·GitHub Actions로 어떻게 옮겨지는지 본문 흐름의 축. fat jar의 부재가 만드는 운영 사고방식의 차이.
- **인용할 리서치 자료:** §4.6 전체, §4.7 전체, §6의 팁 5/6/7번, §7의 dev.to/prateekbka(PM2 vs Cluster vs Docker)와 trendyol-tech(Spring Boot graceful shutdown). 콜드 스타트 비교는 §4.6의 dev.to/aws와 arnoldgalovics.com. 보안 절은 Helmet 공식 문서, NestJS 공식 문서(security, authentication, authorization), `@nestjs/throttler` 공식 문서, Snyk·Dependabot 공식 문서를 본문 작성 시 1차로 인용. CI/CD 절은 GitHub Actions `setup-node` 문서, esbuild·SWC 공식 문서, Docker Buildx 문서를 1차로.
- **예상 분량:** 약 46페이지(약 36,000자) — v1 36p + 보안 6p + CI/CD 4p (사용자 결정 2 + 4 반영).

---

### 8장. Java/Spring에서 Node.js로 — 마이그레이션 전략 (책의 절정)

- **부제:** 여러 챕터에서 본 사례를 결정 차원으로 다시 본다 — PayPal·LinkedIn·Netflix·Walmart·Uber, 그리고 한국 사례
- **핵심 질문:** 우리 팀의 어느 경계부터 Node로 잘라내야 하는가? 그리고 어떤 신호가 보이면 멈춰야 하는가?
- **주요 내용:**
  - **도입 — "다시 보자"의 형식 (요청 4 반영).** "1·3·4·6장에서 우리는 Walmart의 convoy effect, LinkedIn의 BFF 강점, PayPal의 Kraken.js 컨벤션, Netflix의 flame graph를 짧게 보았다. 같은 사례들을 이번엔 결정 차원에서 다시 보자." 단순 사례 나열이 아니라 "여러 각도에서 한 번씩 본 사례들이 결정 시점에서 어떻게 통합되는가"의 회수 도입.
  - **확정 사례 5건 + 한국 사례 묶음 (요청 6 반영).** 사례를 두 묶음으로 정리한다.
    - **확정 사례 5건 (1차 자료가 단단함):**
      1. **PayPal 계정 개요 페이지.** 인력 5명(Java) vs 2명(Node), 처리량 2배 RPS, 응답 35% 감소, 코드 33% 감소·40% 적은 파일. (4장 도입 callback) Express 비강제성이 큰 팀에선 어떻게 사내 Kraken.js 컨벤션 강제로 이어졌는가.
      2. **LinkedIn 모바일 백엔드.** Rails에서 Node로. 서버 30대 → 3대, 10배 헤드룸, 약 20배 처리, 코드 60K → 2K 라인. (3장 도입 callback) "다른 서비스와 대화하기"가 Node의 강점이라는 교훈을 BFF 결정 시나리오에 통합.
      3. **Netflix UI 서버.** 시작 시간 40분 → 1분 미만, 응답 70% 감소. (6장 도입 callback) Java 마이크로서비스를 그대로 두고 BFF 레이어만 Restify·Docker로 분리. Java 완전 대체가 아니었다는 사실.
      4. **Walmart Black Friday.** 모바일 70%, IO 바운드 + SSR. 55% 트래픽이 Node로 갈 때 CPU 1%, 15억 달러 처리. (1장 도입 callback) "convoy effect"라는 운영 함정을 1장에서 봤고, 8장에서는 "왜 SSR을 CDN으로 빼야 했는가"의 결정 차원으로 다시 본다 (hula-hoop·CDN 전략).
      5. **Uber의 후퇴.** RTAPI를 Node로 만들었다가 2018년 신규 권장 스택에서 Node + HTTP/JSON 제외. 신규 엔지니어 온보딩 비용. "기술 선택의 정답은 시점·조직·도메인에 따라 다르다"는 메시지.
    - **한국 사례 묶음 (확정 1 + 보강 후보 1자리):**
      1. **확정 — 당근마켓 푸시 알림.** Rails에서 Node + TS로 분리. 1,500 RPS 누락 없는 처리. §3.6 1차 자료.
      2. **[보강 필요] 토스·인프런·LINE·우아한형제들·카카오 1차 자료.** §3.6과 §8-2 한계로 명시된 영역. Phase 4 진입 전 community-research를 한 번 더 돌려 1차 자료(toss.tech, kakao tech, woowahan tech, line engineering 한국어 블로그)를 발굴한다. 보강 결과에 따라 한 자리를 채우거나, 발굴 실패 시 "5+1+한국 사례의 자료 한계" 절로 정직하게 간다 (요청 6 반영).
  - **테스트 callback (사용자 결정 2 반영).** 사례별 본문에 "테스트 커버리지가 어떻게 옮겨갔는가"를 한 단락씩 — PayPal은 Java JUnit 자산을 어떻게 처리했는가, Netflix BFF는 어떻게 계약 테스트를 둘렀는가. 4장 NestJS 테스트 절을 참조 callback.
  - Strangler Fig 패턴 — Martin Fowler 정의에서 출발해 단계별 분해.
    1. API Gateway 분리(NGINX/Envoy/AWS API Gateway).
    2. 공유 DB 단계 — 새 Node 서비스가 모놀리스 DB 직접 읽기.
    3. DB 분리(CDC/이벤트 스트림) — Debezium·Kafka로 점진적 데이터 이전.
    4. 트래픽 점진 이전 — feature flag, canary, shadow traffic.
    5. anti-corruption layer — 모놀리스 도메인이 새 시스템에 새지 않게.
  - **다이어그램:** Strangler Fig 5단계의 시퀀스 그림. 각 단계마다 "Spring 모놀리스에 어떤 변경이 들어가는가"를 한 줄씩.
  - **결정 시나리오 — 산문으로 풀기 (요청 5 반영).** "BFF부터 시작하라"의 근거를 PayPal·Netflix 사례에서 풀고, 핵심 도메인 서비스는 마지막에, CPU 바운드는 worker_threads 또는 다른 언어 마이크로서비스로의 권고를 산문 흐름으로. 결정 트리 형식이 아니라 시나리오 단락. 표는 절 끝 정리.
  - 후퇴 신호 — 산문으로 풀고(요청 5), 절 끝에 체크리스트 정리. 신규 엔지니어 온보딩 시간, 이벤트 루프 lag p99, CPU 바운드 비중, 운영 사고 빈도, 커뮤니티/사내 라이브러리 부채.
  - **TS 코드 예시:** Spring 모놀리스 앞단에 NestJS BFF를 두고 일부 라우트만 받아내는 최소 Skeleton. Spring REST 호출을 anti-corruption layer로 감싸 새 도메인 모델로 변환하는 코드.
  - 학술적 뒷받침 — IEEE 2021 "Microservice Migration Using Strangler Fig Pattern: A Case Study on the Green Button System" 인용.
  - 마이그레이션 6개월 로드맵 샘플 — 1개월 BFF 셋업, 2~3개월 한 도메인 이전, 4개월 운영 안정화, 5~6개월 다음 도메인.
- **Java/Spring 비교 포인트:** 이 챕터는 비교 자체가 본문이다. Spring 모놀리스가 어떻게 변형되며 Node 서비스가 옆자리에 들어오는지, 어디서 데이터·도메인 모델을 어떻게 분리하는지가 모두 Spring 운영 경험을 전제로 풀린다.
- **인용할 리서치 자료:** §3 전체(6개 케이스), §4.9 전체(Strangler Fig 단계·실패 사례), §5.6(모놀리스 vs 마이크로서비스 균형), §6의 팁 8번(BFF부터)과 9번(CPU 바운드 분리). PayPal·LinkedIn·Netflix·Walmart·Uber + 당근마켓 + **[보강 필요] 토스·인프런·LINE·우아한형제들·카카오 1차 자료**.
- **예상 분량:** 약 50~52페이지(약 40,000자) — v1과 동일. 책의 절정.

---

### 9장. 결정과 설득 — 팀과 커리어에 Node를 들이는 법

- **부제:** 도입을 설득할 언어, PR 리뷰의 함정, 후퇴를 결정할 신호, 그리고 다음 한 걸음
- **핵심 질문:** 8장의 결정을 가지고 조직 안으로 돌아갈 때 무엇이 필요한가? 그리고 이 책을 덮고 나서 가장 먼저 해야 할 일은 무엇인가?
- **주요 내용:**
  - **책 정체성 두 번째 못박기 (1단락).** 1장 닫는 한 단락("도구만 바뀌었을 뿐, 우리가 다루는 동시성 문제 자체는 같다.")을 다시 꺼내, 9장은 그 메시지를 조직과 커리어 차원으로 옮기는 자리임을 명시.
  - 팀 안에서의 도입 설득 — 기술 선택 회의에서 "왜 Node인가"를 한 페이지로 답하는 템플릿. 8장 사례를 어떻게 인용할지 포함. 산문으로 풀고, 템플릿은 절 끝 정리 자료(요청 5 반영).
  - 채용·온보딩 — Spring 출신을 Node 팀에 태우는 학습 경로(이 책의 장 순서가 그대로 4~6주 학습 플랜).
  - **PR 리뷰의 함정 — "Spring 출신이 자주 놓치는 5가지" (요청 3·요청 5 반영).** 7장의 운영 체크리스트(graceful shutdown, 구조화 로깅, OTel, 헬스체크, lag 모니터)와 축을 분리해, 9장은 코드 리뷰 시점의 함정에 집중한다. "PR 리뷰에서 가장 자주 데이는 5가지 함정을 살펴보자"의 산문 진입.
    1. 이벤트 루프 블로킹 가능성을 못 알아채는 코드 — 동기 crypto, 큰 JSON.parse, 정규식 backtracking, sync 파일 I/O가 PR에 섞여 들어오는 패턴.
    2. `await` 누락 — `forEach` 안의 await, Promise를 반환하지만 await 안 한 경우, error rejection을 잡지 못한 경우.
    3. Prisma `select`/`include` 누락으로 N+1을 생성하는 쿼리 패턴 — Hibernate 출신이 lazy 가정으로 작성한 코드.
    4. 타입 안전을 우회한 코드 — `any`/`as` 캐스팅, 구조적 타입의 함정(빈 객체가 인터페이스 만족), 외부 응답을 검증 없이 타입만 단정한 경우.
    5. 예외 전파의 모양 — Java의 checked exception이 없어, 비동기 throw가 어디서 잡히는지 본문에서 못 보이는 패턴. `unhandledRejection`까지 가는 경로.
    체크리스트 자체는 챕터 끝 한 페이지 부록 박스로 정리.
  - 모놀리스 vs 마이크로서비스의 균형 — modular monolith부터 시작하라는 일반 권고를 Node 맥락에서 어떻게 적용할지.
  - 후퇴 신호 — Uber 사례에서 뽑은 신호를 자기 조직에 어떻게 측정·관찰할지(온보딩 시간, 사내 라이브러리 부채, 운영 사고 빈도). 7장의 운영 체크리스트와 다른 축(조직·문화 신호).
  - 커리어 신호 — TypeScript가 GitHub 1위, 채용 65%가 TS 요구. Spring 경력 + Node/TS는 어떤 시장 지점에 도달하는가.
  - **신설 짧은 절 — Bun·Deno의 위치 (2p, 사용자 결정 3 + 요청 3 반영).** 박스 코멘트가 아니라 짧은 본문 절. Bun의 Node 호환성과 빠른 시작/패키지 설치, Deno의 보안 모델·표준 라이브러리. "2026년 시점에 Java 출신이 알아둘 만한 옵션"으로 정직하게 위치 지정. 분량 2p 엄격히 제한.
  - 다음 한 걸음 — 독자 유형별 액션 아이템. 시니어 IC / 테크 리드 / 아키텍트 각각.
  - 닫는 말 — 1장에서 던진 의심에 대한 마지막 대답. PayPal·LinkedIn·Netflix·당근마켓 수치로 "감당한다"를 답하고, Uber 후퇴를 함께 두며 "단 조건이 있다"로 닫는다. (JVM 화해 메시지는 에필로그로 이전, 요청 3 반영)
- **Java/Spring 비교 포인트:** 비교가 기술에서 조직·커리어 차원으로 올라온다. "기술 선택은 도구 선택이 아니라 팀의 학습 곡선과 운영 문화의 선택"이라는 메시지를 Spring 진영의 성숙도와 Node 진영의 빠른 변화 양쪽을 인정하는 톤으로 마무리.
- **인용할 리서치 자료:** §3.5(Uber 후퇴 신호), §4.2(TS 시장 신호), §5(논쟁점 5개 영역의 균형), §5.6(modular monolith), §6의 팁 10번(빌드 타임 최적화), §8의 한계 7번(Bun/Deno 짧은 절). 1장에서 던진 "단일 스레드는 정말 일감을 감당할 수 있는가" 질문을 여기서 회수.
- **예상 분량:** 약 33페이지(약 26,000자) — v1 26p에서 +7p (요청 3 반영). PR 리뷰 함정 절 + Bun/Deno 2p + 정체성 못박기 단락 + 산문화로 분량 자연 증가. JVM 화해 절은 에필로그로 빠짐.

---

### 에필로그. 두 런타임을 같이 돌리는 백엔드 개발자

- **분량:** 약 11페이지(요청 3 반영, v1 6~8p에서 +4p).
- **역할 (요청 3 반영):** 기술적 결론이 아니라 정체성에 대한 마지막 한 마디. 9장에서 빼낸 "JVM 진영과 결별이 아니다" 메시지를 흡수해, 이 자리를 두 진영의 화해 자리로 키운다.
- **주요 내용:**
  - 1장 도입의 Walmart convoy effect와 닫는 한 단락("도구만 바뀌었을 뿐")을 다시 꺼내 책 정체성 세 번째 못박기.
  - JVM 진영과의 화해 — Java Virtual Threads(Project Loom)가 같은 동시성 문제를 다른 길로 푼다는 사실, GraalVM Native Image와 SnapStart가 Spring Boot의 콜드 스타트 약점을 어디까지 메우는가, "두 런타임을 같이 돌리는 팀"의 모습.
  - 두 번째 런타임을 갖는다는 것 — Node가 Spring을 대체한다가 아니라, Spring 옆자리에 들어와 함께 돈다. 1장에서 던진 의심에 대한 마지막 대답.
  - 닫는 한 줄 — "Spring을 떠난 게 아니라 도구가 한 개 늘었을 뿐이다."

---

## 5. 챕터 간 callback 계획 (요청 4 반영해 재정리)

이 책의 callback 구조는 **"1·3·4·6장에서 각 사례를 짧게 보고, 8장에서 결정 차원으로 다시 본다"** + **"1장→9장→에필로그에서 책 정체성을 세 번 박는다"** 두 축으로 짜인다.

### 사례 분산 callback (요청 2 + 요청 4 반영)

- **1장 → 8장 (Walmart):** 1장 도입에서 convoy effect를 1페이지 일화로 정직하게 풀고, 1장 본문에서 "이벤트 루프를 막지 마라"의 추상 권고가 어떻게 실제 운영 함정이 되는지 한 번 본다. 8장 사례 4에서는 같은 일을 "왜 SSR을 CDN으로 빼야 했는가"의 결정 차원으로 다시 본다 (hula-hoop·CDN 전략).
- **3장 → 8장 (LinkedIn):** 3장 도입에서 "Node의 강점은 다른 서비스와 대화하기"라는 BFF 교훈을 한 단락으로. 8장 사례 2에서는 같은 사례를 서버 30대 → 3대의 결정 시나리오로 다시.
- **4장 → 8장 (PayPal):** 4장 도입에서 Express 비강제성 → Kraken.js 컨벤션 강제 일화 + t2.micro 후기 결합. 8장 사례 1에서는 PayPal의 마이그레이션 수치(2배 RPS, 35% 응답 감소, 코드 33% 감소)를 결정 시나리오로 다시.
- **6장 → 8장 (Netflix):** 6장 도입에서 "production에서 정규식 한 줄이 핫스팟" flame graph 일화. 8장 사례 3에서는 시작 시간 40분 → 1분 미만의 BFF 분리 결정으로 다시.

### 책 정체성 못박기 (요청 3 반영, 후보 B 메시지의 본문 흡수)

- **1장 닫는 한 단락:** "도구만 바뀌었을 뿐, 우리가 다루는 동시성 문제 자체는 같다."
- **9장 첫 단락:** 1장 닫는 한 단락을 다시 꺼내, 9장이 그 메시지를 조직과 커리어 차원으로 옮기는 자리임을 명시.
- **9장 닫는 말:** 1장에서 던진 의심("단일 스레드는 정말 일감을 감당할 수 있는가")에 대한 마지막 대답.
- **에필로그:** Walmart convoy effect와 1장 닫는 한 단락을 세 번째로 꺼내, JVM 화해 메시지와 함께 "Spring을 떠난 게 아니라 도구가 한 개 늘었을 뿐이다"로 닫는다.

### 그 외 챕터 간 callback (구조 callback)

- **2장 → 4장:** 2장에서 본 TS 데코레이터·구조적 타입·유틸리티 타입이 4장 NestJS DI/모듈 시스템에서 그대로 사용된다.
- **2장 → 5장:** 2장 Promise·async/await 패턴이 5장 Prisma `$transaction` 콜백 형태로 다시 등장.
- **2장 → 7장:** 2장 끝의 패키지 관리·monorepo 절이 7장 CI/CD 파이프라인의 npm cache·workspace 빌드와 연결된다.
- **3장 → 7장:** 3장의 BullMQ 워커가 7장의 graceful shutdown 절에서 다시 등장. "진행 중 잡을 어떻게 마무리하느냐."
- **4장 → 7장:** 4장의 NestJS 모듈/DI가 7장의 `@nestjs/terminus`와 `enableShutdownHooks()`에서 운영 측면으로 확장. 4장의 JWT 가드가 7장 보안 운영 절에서 OAuth·Rate Limit과 묶여 다시 등장.
- **4장 테스트 → 8장:** 4장 NestJS 테스트 절이 8장 마이그레이션 사례마다 "테스트 커버리지가 어떻게 옮겨갔는가" 한 단락으로 callback.
- **5장 → 8장:** 5장 Prisma `$transaction` 명시성이 8장 Strangler Fig "공유 DB → DB 분리" 단계의 데이터 일관성 도전과 연결.
- **6장 → 8장:** 6장의 clinic.js·heap snapshot·이벤트 루프 lag 모니터링이 8장의 후퇴 신호 체크리스트로 회수.
- **7장 → 9장 (축 분리, 요청 3 반영):** 7장은 운영 체크리스트(graceful shutdown, 구조화 로깅, OTel, 헬스체크, lag 모니터)를 담당한다. 9장은 다른 축의 PR 리뷰 함정(이벤트 루프 블로킹 코드 패턴, await 누락, Prisma N+1 패턴, 타입 안전 우회, 예외 전파)을 담당해 중복을 피한다.

---

## 6. 자기 점검 (체크리스트, v2 갱신본)

- [x] **모든 챕터가 핵심 질문에 답한다** — 1장(런타임 작동 원리), 2장(언어 차이 + 패키지 관리), 3장(패턴 지형), 4장(NestJS vs Spring + 테스트), 5장(ORM 마법의 부재), 6장(디버깅 도구 매핑), 7장(운영 + 보안 + CI/CD), 8장(마이그레이션 전략), 9장(결정과 설득 + PR 리뷰 함정 + Bun/Deno). 4장 핵심 질문은 여전히 "NestJS vs Spring Boot 정면 비교"이며, 테스트 절은 그 비교의 한 축으로 들어간다.
- [x] **챕터 순서에 맥이 흐른다** — 의심·발견 → 도구 익숙해지기 → 실무 현실 → 결단 → 정체성 회복의 곡선.
- [x] **대상 독자 수준에 맞는다** — "콜백 지옥은 무엇인가" 같은 클리셰는 한 단락으로 빠르게 처리, 본질은 비교 관점에 둠.
- [x] **레퍼런스의 9개 영역(§4.1~§4.9)이 모두 1~9장에 매핑됨.** 6개 마이그레이션 사례(§3.1~§3.6) 중 5개는 1·3·4·6·8장에 분산 배치, Uber 후퇴 + 당근마켓 + 한국 사례 보강 후보는 8장에 집중. Top 10 헷갈림 지점(§2)은 1·2·4·5·7·9장에 분산.
- [x] **요청 1 (Must-fix) 반영 — 보안·테스트 흡수 완료.** 4장에 NestJS 테스트 6p 절 추가, 7장에 보안 운영 6p 절 추가. 4장 50p, 7장 46p로 분량 갱신.
- [x] **요청 2 반영 — 1장에 1차 자료 무게.** 1장 도입에 Walmart convoy effect 1p 일화. 6장 도입을 Netflix flame graph 일화로 변경.
- [x] **요청 3 반영 — 9장 분량·범위 재조정.** 9장 26p → 33p로 확대 (PR 리뷰 함정 절 신설 + Bun/Deno 2p + 정체성 못박기). JVM 화해 절은 에필로그로 이전, 에필로그 6~8p → 11p. 7장↔9장 체크리스트 중복 해소(7장은 운영 축, 9장은 PR 리뷰 축).
- [x] **요청 4 반영 — 마이그레이션 사례 분산.** Walmart는 1장 도입, LinkedIn BFF는 3장 도입, PayPal Kraken.js는 4장 도입, Netflix flame graph는 6장 도입. 8장은 "다시 보자"의 회수 형식으로 6개 사례를 결정 차원으로 통합.
- [x] **요청 5 반영 — 산문화.** "결정 트리"·"의사결정 표"·"체크리스트" 형식 어휘를 본문에서 산문 흐름으로 풀고, 표·체크리스트 자체는 절 끝의 정리 자료로만 둔다 (3·4·5·8·9장 모두).
- [x] **요청 6 반영 — 한국 사례 보강 To-do 명시.** 8장 인용 자료에 "[보강 필요] 토스·인프런·LINE·우아한형제들·카카오 1차 자료"를 명시. 5+1+한국 사례의 자료 한계 안전판도 명시.
- [x] **사용자 결정 1 반영 — 책 제목 후보 A 채택.** §1에서 후보 A 최종안 명시, B·C는 기각 사유 한 줄씩.
- [x] **사용자 결정 2 반영 — 보안 6p, 테스트 6p, 4장 50p, 7장 46p.**
- [x] **사용자 결정 3 반영 — Bun·Deno는 9장 안 짧은 절 2p (분량 엄격).**
- [x] **사용자 결정 4 반영 — 7장에 Node 빌드 파이프라인 4p 절 신설.**
- [x] **추가 채택 항목 (plan-reviewer §4 표) — 패키지 관리 비교 절.** 2장 끝에 3~4p 절 추가 (npm/pnpm/Bun, monorepo·workspaces, Maven multi-module/Gradle composite 매핑).
- [x] **챕터 핵심 질문이 흐려지지 않았는지 확인.** 4장은 "NestJS vs Spring Boot의 정면 비교"이고 테스트는 그 비교의 한 축. 7장은 "Node 운영 매뉴얼"이고 보안·CI/CD는 운영의 일부. 9장은 "결정과 설득"이고 PR 리뷰 함정·Bun/Deno는 그 결정의 후속 작업. 핵심 질문이 흐려진 챕터 없음.
- [x] **챕터 간 중복 없음** — Spring 비교는 모든 챕터에 흐르되 각 챕터가 다른 비교 축(스레드 모델·언어·프레임워크·ORM·도구·운영·전략·조직)을 담당. 7장(운영)과 9장(PR 리뷰)의 체크리스트 중복은 축 분리로 해소.
- [x] **예상 분량 합계 — 약 365페이지 (목표 350p에서 약 +15p 초과).**
  - 프롤로그 9 + 1장 33 + 2장 33 + 3장 32 + 4장 50 + 5장 38 + 6장 28 + 7장 46 + 8장 51 + 9장 33 + 에필로그 11 = **약 364페이지** (약 28만 4천자).
  - 350p 목표를 약 14p 초과한다. 분량 압박 시 §7-(3)-5 가이드대로 3장 32p → 28p, 6장 28p → 26p, 5장 38p → 36p로 8p 추가 다이어트 가능. 8장과 4장은 줄이지 않는다. 분량 압박이 강하면 350p 정확히 맞출 수 있고, 압박이 약하면 365p에서 출발해 본문 작성 후 마지막 단계에서 조정.

---

## 7. 보고

### (1) 저장 절대경로

`/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/nodejs-for-java-developer/nodejs-for-java-developer/02_plan.md`
v1 백업: `/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/nodejs-for-java-developer/nodejs-for-java-developer/02_plan_v1.md`

### (2) 확정한 챕터 수와 총 예상 페이지

- **챕터 수:** 본문 9개 챕터 + 프롤로그(9p) + 에필로그(11p, 강화).
- **총 예상 페이지:** **약 365페이지(약 28만 4천자).** 목표 350p에서 약 +15p. 4장(NestJS+테스트, 50p)·7장(운영+보안+CI/CD, 46p)·8장(마이그레이션, 51p)에 무게중심. 분량 압박 시 3장·5장·6장에서 최대 8p 추가 다이어트로 350p 정확히 맞출 수 있다.

### (3) v2 갱신본의 핵심 변경 사항 요약

| # | 영역 | v1 | v2 | 출처 |
|---|------|-----|-----|------|
| 1 | 책 제목 | 후보 B 추천 | **후보 A 확정** ("자바 개발자를 위한 Node.js / Spring 직관을 그대로 들고 가는 두 번째 런타임 가이드") | 사용자 결정 1 |
| 2 | 4장 분량 | 44p | **50p** (NestJS 테스트 6p 절 신설) | 사용자 결정 2 + 요청 1 |
| 3 | 7장 분량 | 36p | **46p** (보안 6p + CI/CD 4p 신설) | 사용자 결정 2 + 4 + 요청 1 |
| 4 | 9장 분량 | 26p | **33p** (PR 리뷰 함정 절 + Bun/Deno 2p + 정체성 못박기) | 요청 3 + 사용자 결정 3 |
| 5 | 에필로그 분량 | 6~8p | **11p** (JVM 화해 메시지 흡수) | 요청 3 |
| 6 | 2장 분량 | 30p | **33p** (패키지 관리·monorepo 절 신설) | plan-reviewer §4 표 추가 채택 |
| 7 | 1장 도입 | 추상으로 시작 | **Walmart convoy effect 일화 1p** | 요청 2 + 4 |
| 8 | 6장 도입 | 도구 매핑 표 | **Netflix flame graph 일화** | 요청 2 + 4 |
| 9 | 3장 도입 | 도구 나열 | **LinkedIn BFF 강점 한 단락** | 요청 4 |
| 10 | 4장 도입 | t2.micro 후기 | **PayPal Kraken.js + t2.micro 결합** | 요청 4 |
| 11 | 8장 사례 구도 | 6개 평면 나열 | **확정 5건 + 한국 사례(당근마켓 + 보강 후보 1자리)** | 요청 6 |
| 12 | 산문화 | 결정 트리·체크리스트 형식 어휘 | 본문은 산문, 표는 절 끝 정리 | 요청 5 |
| 13 | 7장↔9장 중복 | 운영 체크리스트 중복 | 7장 운영 축 / 9장 PR 리뷰 축으로 분리 | 요청 3 |
| 14 | 책 정체성 | 후보 B 메시지가 제목에만 | **본문에 1장·9장·에필로그 세 번 못박기** | 사용자 주의사항 |

### (4) 챕터별 새 분량 표

| 단원 | v1 | v2 | 변동 | 사유 |
|------|----|----|------|------|
| 프롤로그 | 8~10p | 9p | ≈ | 변동 없음 |
| 1장 런타임 | 32p | **33p** | +1p | Walmart 도입 1p |
| 2장 JS/TS | 30p | **33p** | +3p | 패키지 관리·monorepo 절 |
| 3장 활용 패턴 | 36p | **32p** | -4p | 산문화 다이어트, 분량 균형 |
| 4장 NestJS | 44p | **50p** | +6p | NestJS 테스트 절 |
| 5장 ORM | 38p | 38p | ≈ | 변동 없음 |
| 6장 디버깅 | 30p | **28p** | -2p | 다이어트, 분량 균형 |
| 7장 배포·운영·보안·CI/CD | 36p | **46p** | +10p | 보안 6p + CI/CD 4p |
| 8장 마이그레이션 | 50~52p | **51p** | ≈ | 사례 회수 형식으로 재구성 |
| 9장 결정과 설득 | 26p | **33p** | +7p | PR 리뷰 함정 + Bun/Deno + 정체성 못박기 |
| 에필로그 | 6~8p | **11p** | +4p | JVM 화해 메시지 흡수 |
| **합계** | **약 337p** | **약 365p** | **+28p** | 보안·테스트·CI/CD·monorepo·정체성 못박기 추가 |

### (5) 한국 사례 보강 To-do — Phase 4 진입 전 추가 community-research 가이드

8장의 한국 사례 묶음에서 "[보강 필요] 토스·인프런·LINE·우아한형제들·카카오 1차 자료"를 채우려면 Phase 4(챕터 저술) 진입 전에 community-research를 한 번 더 돌리는 것이 안전하다. 다음 절차를 권한다.

1. **community-research 에이전트 재실행 — 1차 자료 발굴에 집중.**
   - 대상 도메인: `toss.tech`, `tech.kakao.com`, `techblog.woowahan.com`, `engineering.linecorp.com/ko/blog`, `tech.inflab.com` (인프런), `tech.kakaopay.com`.
   - 검색 쿼리(한국어): "NestJS 도입", "Node.js 마이그레이션", "Spring에서 Node로", "Express 사용기", "TypeScript 백엔드 도입기".
   - 검색 쿼리(영문 보조): site filter로 `site:toss.tech NestJS`, `site:techblog.woowahan.com Node.js`, `site:engineering.linecorp.com Node.js backend`.
   - 출력 포맷: `01_reference.md` §3.6 형식과 동일하게 — 출발점·수치·교훈·1차 출처 URL.

2. **OKKY·velog·F-Lab·요즘IT 한국어 회고 보조 발굴.**
   - "Spring → Node 전환 회고", "NestJS 1년 운영기" 같은 1인 회고가 1차 회사 블로그 부족을 보완할 수 있다. 1차 자료 무게는 약하지만 인용 가능한 일화와 정성적 신호가 있다.
   - velog 태그: `nestjs`, `spring-to-node`, `백엔드-마이그레이션`.

3. **인터뷰·X(트위터)·페이스북 1인 회고 — §8-3 한계 보강.**
   - 한국어 1인 회고가 빈약하다는 §8-3 한계를 메우는 자리. 발굴된 X·페이스북 글은 1차 자료가 아니지만, 8장 본문에서 "사례의 무게는 약하나 정성적 신호로" 인용 가능하다.

4. **보강 결과에 따른 8장 분기 처리.**
   - **시나리오 A — 1차 자료 1건 이상 발굴:** 8장 한국 사례 묶음에 "당근마켓 + 발굴된 사례 1건" 구도로 채운다. 8장 사례는 5(글로벌) + 2(한국)가 된다.
   - **시나리오 B — 1차 자료 없음:** 8장은 5(글로벌) + 1(당근마켓) 구도로 가고, "한국 사례의 자료 한계" 절을 6p 넣어 정직하게 다룬다. velog/OKKY 1인 회고를 정성적 신호로 인용.

5. **재실행 타이밍.** Phase 4(챕터 저술) 시작 직전. 1~2일 소요 예상. 8장 본문 작성이 시작되면 같은 챕터 안에서 사례 발굴이 흐름을 끊으므로, 사전 발굴이 권장된다.

---

## 8. v1과 v2의 개정 메모 (편집자 참고)

- v1은 후보 B를 추천하고 보안·테스트·Bun/Deno·CI/CD·한국 사례 보강을 사용자 판단에 미뤘다. v2는 사용자 결정 4건과 plan-reviewer 6개 요청을 모두 받아들여 다음을 변경했다.
  - 책 제목: 후보 A 확정. 후보 B 메시지는 본문 정체성 못박기로 흡수.
  - 보안 6p (7장), 테스트 6p (4장), CI/CD 4p (7장), 패키지 관리·monorepo 3~4p (2장), Bun/Deno 2p (9장 안의 짧은 절). 새 챕터를 만들지 않고 기존 챕터에 흡수.
  - 마이그레이션 사례 분산 — Walmart(1장), LinkedIn(3장), PayPal(4장), Netflix(6장)에 도입 일화로 미리 한 번 풀고, 8장에서 "다시 보자"의 회수 형식으로 결정 차원으로 통합.
  - 9장은 분량 확대(26p → 33p) + JVM 화해 절 에필로그 이전 + PR 리뷰 함정 축으로 7장 체크리스트 중복 해소.
  - 책 정체성("도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다") 본문에 1장·9장·에필로그 세 번 못박기.
- v1의 강점은 그대로 유지했다 — 9개 영역 매핑, 4장 t2.micro 후기 진입, 5장 "Hibernate의 마법이 사라진 자리" 프레이밍, 1장→8장 Walmart callback 시그니처, 6장 도구 매핑 표(이제 일화 다음에 위치), 8장 50p 절정.
- 분량은 337p → 365p로 약 28p 늘었다. 350p 목표를 14p 초과하지만, 3장·5장·6장에서 최대 8p 다이어트로 좁힐 수 있고, 본문 작성 후 마지막 단계에서 정밀 조정한다. 8장과 4장은 줄이지 않는다.
- 다음 단계는 Phase 4 진입 전 한국 사례 보강 community-research 1회 재실행 (위 §7-(5) 절차).
