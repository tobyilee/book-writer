# 자바 개발자를 위한 Node.js

> Spring 직관을 그대로 들고 가는 두 번째 런타임 가이드 — Java/Spring/Kotlin 시니어가 Node.js로 두 번째 런타임을 갖는 길.

- **저자:** Toby-AI
- **부제:** Spring 직관을 그대로 들고 가는 두 번째 런타임 가이드
- **버전:** v1.0.0
- **발행일:** 2026-05-04
- **언어:** 한국어 (ko)
- **분량:** 프롤로그 + 9개 본문 챕터 + 에필로그 (총 11개 챕터) / 본문 약 297,000자 (약 360페이지)
- **포맷:** EPUB 3 (epubcheck 통과)

## 이 책은 무엇인가

이 책은 입문서가 아니다. 이미 Java와 Spring으로 5년 이상 백엔드를 짜온 손이 두 번째 런타임으로 Node.js를 받아들이는 자리에 놓인 책이다. 서블릿 스레드 모델과 이벤트 루프, Spring Boot와 NestJS, Hibernate와 Prisma, JVM 도구 체인과 Node 도구 체인, fat jar와 Docker 이미지 — 이 책의 11개 챕터는 두 진영의 모든 비교를 1차 자료(공식 문서·소스코드·엔지니어링 블로그)에 근거해 평어체로 풀어낸다.

다른 Node.js 책과의 차별점은 세 가지다. 첫째, **모든 설명이 비교의 형태로 흐른다.** "Spring에서는 X였는데 Node에서는 Y다"라는 구도가 박스나 부록이 아니라 본문의 산문 그 자체로 흐른다. 둘째, **결정 차원의 사례 회수가 책 후반부의 절정이 된다.** PayPal, LinkedIn, Netflix, Walmart, Uber, 그리고 한국의 당근마켓·줌인터넷·직방·인프랩까지 10개 마이그레이션·도입 사례가 챕터 곳곳에 분산 배치되었다가, 8장에서 Strangler Fig 패턴이라는 결정 프레임으로 다시 모인다. 셋째, **2026년 시점의 균형 잡힌 시야를 끝까지 유지한다.** Bun과 Deno, Java Virtual Threads와 GraalVM Native Image, AWS Lambda SnapStart의 자리를 인정하고, 어느 한쪽도 유토피아·디스토피아로 그리지 않는다.

본문이 한 줄로 못 박는 메시지는 이렇다 — **"도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다."** 이 메시지는 1장 도입의 Walmart convoy effect 일화, 9장의 조직 설득 장면, 그리고 에필로그의 정체성 회복 장면에서 책 정체성으로 세 번 박힌다.

이 책은 의심에서 시작해 결단으로 끝난다. 1장에서 "단일 스레드가 정말 일감을 감당할 수 있을까"를 의심하던 독자가, 8장 후반에서는 "우리 팀의 어느 경계부터 잘라내 Node로 옮길지"를 결정할 수 있게 된다. 9장과 에필로그에서는 그 결정을 조직 안에서 설득할 언어와, 두 진영을 같이 돌리는 백엔드 개발자라는 정체성을 갖는다.

## 누구를 위한 책인가

- **주된 독자:** Java/Spring/Kotlin으로 5년 이상 백엔드를 짜온 시니어/미드 개발자. 모놀리스나 마이크로서비스를 운영해본 경험이 있고, JPA·Hibernate·Spring Security를 손에 익힌 사람.
- **진입 상태:** JavaScript는 써본 적이 있지만 본격적으로 백엔드를 짜본 적은 없다. async/await의 모양은 알지만 이벤트 루프 모델을 자기 언어로 설명하지는 못한다. NestJS는 이름만 들어봤다.
- **도착 상태:** NestJS로 작은 서비스를 직접 설계·운영하고, BFF 또는 마이크로서비스 한 조각을 Strangler Fig 패턴으로 마이그레이션할 수 있다. Node 운영 도구 체인(clinic.js, Pino, OpenTelemetry, PM2/K8s, Helmet/JWT, Jest/Supertest, GitHub Actions)을 JVM 도구와 매핑해 머릿속에 가지고 있다. Bun·Deno·Loom·SnapStart의 자리를 균형 있게 판단할 수 있다.

이 책은 다음과 같은 사람에게 어울리지 않는다. JavaScript 자체를 처음 만나는 사람, Spring 경험이 없는 채로 Node를 시작하는 사람, "둘 중 어느 쪽이 더 우월한가"를 듣고 싶은 사람. 이 책은 양쪽 다 충분히 인정한다.

## 무엇을 얻게 되는가

- **Spring Boot ↔ NestJS의 정면 비교** — 모듈 시스템, DI, 컨트롤러·서비스·인터셉터·가드·파이프, `@SpringBootTest`/`@MockBean` ↔ NestJS Test 모듈 매핑까지. forwardRef와 순환 의존이 등장하는 자리에서 정직하게 멈춘다.
- **JPA/Hibernate ↔ Prisma의 "마법의 부재" 정직한 다루기** — LazyInitializationException 대신 등장하는 것, Unit of Work가 어디로 갔는지, `@Transactional`의 자리에 들어선 것, N+1 문제와 DataLoader. Drizzle(JOOQ가 그리운 사람의 자리)·TypeORM·Mongoose까지 함께.
- **JVM 도구 체인 → Node 도구 체인 매핑** — VisualVM·jmap·JFR·async-profiler의 자리에 `--inspect`·heap snapshot·clinic.js·Netflix flame graph 사례가 들어선다. 이벤트 루프 lag 측정처럼 Node에만 있는 항목도 빠뜨리지 않는다.
- **마이그레이션 사례 10건 + Strangler Fig 패턴** — PayPal·LinkedIn·Netflix·Walmart의 결정을 결정 차원으로 다시 보고, 한국 사례(당근마켓·줌인터넷·직방·인프랩)와 Uber의 후퇴 신호까지 더해 모놀리스 → BFF → 부분 마이크로서비스로 가는 결정 시나리오를 산문으로 통합한다.
- **2026년 시점의 균형 잡힌 운영 매뉴얼** — Dockerfile 멀티 스테이지·tini·graceful shutdown·Pino 로깅·헬스체크 분리·Helmet/CORS/JWT/Rate Limit, GitHub Actions로 짠 CI/CD, 그리고 Bun·Deno·Loom·SnapStart까지 끝에 한 번 더.

## 차례

1. **프롤로그. Spring 개발자가 Node.js 폴더를 처음 열었을 때** — `package.json`과 `node_modules`, fat jar의 부재, 그 어색함의 정체.
2. **1장. 단일 스레드는 정말 일감을 감당할 수 있는가** — V8과 libuv, 이벤트 루프 6단계, Worker Threads, Java Virtual Threads와의 비교. Walmart convoy effect로 들어간다.
3. **2장. JavaScript와 TypeScript** — `this`의 호출 시점 결정, 클로저와 `var`/`let`, Promise/`async`/`await` 함정 3종, 구조적 타입 vs 명목적 타입, npm·pnpm·monorepo의 자리.
4. **3장. 활용 패턴의 지형** — REST(Express·Fastify·NestJS 삼각 구도), GraphQL, CLI, BullMQ 워커, WebSocket, 서버리스. LinkedIn이 보여준 Node가 잘하는 자리에서 시작한다.
5. **4장. NestJS와 Spring Boot — 가장 닮은 두 프레임워크의 정면 비교** — 공통 DNA, 클래스패스 스캔 vs 명시적 모듈 그래프, 인터셉터·가드·파이프, forwardRef의 신호, NestJS 테스트 6페이지, 직방의 1인칭 적응기.
6. **5장. ORM과 데이터베이스 — Hibernate의 마법이 사라진 자리** — Prisma·Drizzle·TypeORM 세 가지 길, include/select, Unit of Work의 부재, 트랜잭션, N+1과 DataLoader, Redis와 Mongoose, Flyway/Liquibase의 자리.
7. **6장. 디버깅 — JVM 도구 체인을 Node 도구 체인으로 옮기기** — `--inspect`·heap snapshot·clinic.js·이벤트 루프 블로킹 탐지·Netflix flame graph 회수·메모리 누수 사냥·`process.report`까지.
8. **7장. 배포·운영·보안·CI/CD — 컨테이너 시대의 Node 운영 매뉴얼** — PM2와 cluster, Dockerfile 멀티 스테이지, Graceful shutdown, Pino, 헬스 체크 분리, 서버리스 콜드 스타트, Spring Security의 자리(Helmet·CORS·JWT·OAuth·Rate Limit·의존성 스캔), GitHub Actions CI/CD.
9. **8장. Java/Spring에서 Node.js로 — 마이그레이션 전략** — Strangler Fig 단계별, Walmart·LinkedIn·PayPal·Netflix·Uber·당근마켓·줌·직방·인프랩의 결정 회수.
10. **9장. 결정과 설득 — 팀과 커리어에 Node를 들이는 법** — 도입 설득 언어, PR 리뷰의 함정, 후퇴 신호 측정, Node와 Bun이 한 자리에서 보여주는 모습.
11. **에필로그. 두 런타임을 같이 돌리는 백엔드 개발자** — JVM과 결별이 아니다. Java Virtual Threads·GraalVM Native Image·SnapStart의 자리를 인정하며, "도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다"의 마지막 회수.

## 저자 소개

Toby-AI는 Java/Spring/Kotlin 백엔드 개발자가 두 번째 런타임을 받아들이는 자리에 서기 위해 설계된 AI 저자 페르소나다. 이 책은 1차 자료(공식 문서, 오픈소스 저장소, 엔지니어링 블로그, 컨퍼런스 발표, 한국·해외 개발자 커뮤니티의 회고)를 평어체 비교 톤으로 통합한 결과다. 책 곳곳에 등장하는 사례·수치·일화는 모두 출처가 검증된 자료에서 가져왔다.

## 책 정보

- **파일:** `자바-개발자를-위한-Node.js-v1.0.0.epub`
- **형식:** EPUB 3 (한국어 / ko)
- **메타데이터:** 제목, 부제, 저자(Toby-AI), 언어, 버전이 EPUB 메타로 박혀 있음
- **표지:** 전용 표지 이미지(1600×2560 PNG) 임베드
- **차례:** EPUB 리더의 ToC에서 11개 챕터 + 표지 + 타이틀 페이지로 분리되어 표시
- **표준 검증:** epubcheck 통과
- **분량:** 본문 약 297,000자 / 약 360페이지
- **슬로건:** "도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다."
