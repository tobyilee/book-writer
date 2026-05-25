<!-- 검색 시점: 2026-05-25 기준 -->

# 웹 리서치: React/Next.js 개발자를 위한 Spring MVC + JPA 백엔드 입문

신선도 주의: 이 책은 **Spring Boot 3.x**를 기준으로 한다. 2026-05-25 시점 실제 최신 stable은 **Spring Boot 4.0.6 (2026-04-23)** / **Spring Framework 7.0**이다. 3.x는 여전히 프로덕션 주류이지만 OSS 지원 종료가 임박했으므로(아래) "왜 3.x인가"를 책에서 명시해야 한다.

---

## 자료 1: Spring Boot 버전·EOL 현황 (1차/권위)
- 출처: https://endoflife.date/spring-boot , https://spring.io/projects/spring-boot/
- 발행일/검색: endoflife.date는 상시 갱신, 검색 시점 2026-05-25
- 핵심 사실 (날짜 못 박음):
  - **Spring Boot 3.5** — 출시 2025-05-31, **OSS 커뮤니티 지원 종료 2026-06-30**(상용 2032-06-30). 3.x의 마지막 마이너.
  - 3.4 — 2024-11-30 출시, OSS 지원 종료 2025-12-31 (이미 종료)
  - 3.3 — 2024-05-31 출시, OSS 지원 종료 2025-06-30 (이미 종료)
  - 3.2 — 2023-11-30 출시, OSS 지원 종료 2024-12-31 (이미 종료)
  - **4.0** — 2025-11-30 출시, 최신 4.0.6(2026-04-23), OSS 지원 2026-12-31까지
  - 3.5~4.0은 Java 17~25 지원
- 신선도 메타: **"Spring Boot 3.5 / 2025-05 기준"** — 책 집필 시점에 3.x 패치는 2026-06-30 이후 OSS로는 끊김. 독자에게 "학습은 3.x로, 신규 그린필드는 4.x 고려" 안내 권장.

## 자료 2: Spring Boot 3.0 = Spring Framework 6 + Java 17 + Jakarta EE 9 베이스라인
- 출처: https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes , https://spring.io/blog/2022/05/24/preparing-for-spring-boot-3-0/
- 핵심: Spring Boot 3.x 전 라인은 **Java 17 이상 필수**. Spring Boot 3.0은 Spring Framework 6 위에 올라가며 이를 요구한다.
- 신선도: "Spring Boot 3.x / Spring Framework 6.x / Java 17 기준" — 본문 버전 규율의 기준점.

## 자료 3: javax → jakarta 네임스페이스 전환 (왜 바뀌었나)
- 출처: https://spring.io/blog/2022/05/24/preparing-for-spring-boot-3-0/ , https://www.javacodegeeks.com/2024/12/spring-boot-3-and-the-move-to-jakarta-ee-what-developers-need-to-know.html
- 핵심 인용/사실:
  - 2017년 Oracle이 Java EE를 Eclipse 재단에 기증 → "Java" 상표 문제로 **Jakarta EE**로 리브랜딩.
  - Jakarta EE 9에서 패키지 네임스페이스 `javax.*` → `jakarta.*` 전면 변경 (예: `javax.servlet` → `jakarta.servlet`, `javax.persistence` → `jakarta.persistence`).
  - "The change was mechanical, but it touched every file in every Jakarta EE codebase on the planet" — 메이저 버전 브레이크의 원인.
  - Spring Boot 3.0이 **Jakarta EE 9 API(`jakarta.*`)를 쓰는 첫 버전**. Tomcat 10 / Jetty 11이 이를 지원.
- 함정: 인터넷의 오래된 예제·스택오버플로 답변은 `javax.*` import를 쓴다 → 3.x에서 컴파일 안 됨. **AI도 같은 함정** (자료 9 참조).
- 신선도: "Spring Boot 3.0+ / Jakarta EE 9 기준".

## 자료 4: DispatcherServlet · Front Controller · IoC/DI
- 출처: https://medium.com/@sweetyleah0/spring-mvc-minus-the-magic-autowiring-dispatcherservlet-explained-65f7a09d63e4 , https://javarevisited.blogspot.com/2017/09/dispatcherservlet-of-spring-mvc-10-points-to-remember.html
- 핵심:
  - DispatcherServlet은 Spring MVC의 **Front Controller** — 모든 들어오는 웹 요청이 개별 컨트롤러에 닿기 전 먼저 통과하는 진입점.
  - 요청 흐름: 요청 → DispatcherServlet → (HandlerMapping으로) `@Controller`/`@RestController` 위임 → 컨트롤러 처리 → (뷰 이름 반환 시) ViewResolver로 View 결정 → 렌더.
  - DispatcherServlet 초기화 시 IoC 컨테이너 생성, 싱글톤 빈 사전 인스턴스화, 서비스/DAO/DataSource/핸들러에 의존성 주입 완료.
  - **IoC = 제어의 역전**: 객체가 자기 의존성을 직접 만들지 않고, 프레임워크(Spring)가 그 책임을 가져간다. Autowiring은 컨테이너 안 빈끼리 의존성을 자동 주입하는 방식.
- 신선도: 개념 자체는 버전 무관(안정적).

## 자료 5: REST API 검증·예외처리·ResponseEntity (DTO 중심)
- 출처: https://www.baeldung.com/exception-handling-for-rest-with-spring , https://www.javathinking.com/blog/spring-rest-api-validation-should-be-in-dto-or-in-entity/ , https://dev.to/gianfcop98/spring-boot-and-validation-a-complete-guide-with-valid-and-validated-471p
- 핵심:
  - Spring은 **Jakarta Bean Validation(기본 구현체 Hibernate Validator)**을 통합. 컨트롤러 파라미터에 `@Valid`(또는 클래스에 `@Validated`)를 붙이면 역직렬화된 DTO를 자동 검증.
  - 검증 실패 시 `MethodArgumentNotValidException` 발생.
  - 권장 패턴: `@RestControllerAdvice` + `@ExceptionHandler`로 **전역 예외 처리** → 필드 에러를 매핑해 `ResponseEntity.badRequest()`로 구조화 응답(타임스탬프·상태코드·필드별 메시지) 반환.
  - 검증은 **DTO 계층**에서 (엔티티가 아니라) — 영속 계층까지 예외가 흘러가지 않게. 계층 독립성·중복 방지.
  - 생성/수정에 다른 제약이 필요하면 `@Validated` + validation groups.
- 신선도: "Spring Boot 3.x / Jakarta Bean Validation 기준". (주의: Spring Boot 4는 Jackson 3로 이동 — 직렬화 세부가 달라질 수 있음, 3.x는 Jackson 2.)

## 자료 6: Spring Data JPA N+1 문제와 해법
- 출처: https://sharpskill.dev/en/blog/spring-boot/spring-data-jpa-n-plus-1-fetch-join-entitygraph (2026 가이드) , https://www.baeldung.com (EntityGraph), https://tech.asimio.net/2020/11/06/Preventing-N-plus-1-select-problem-using-Spring-Data-JPA-EntityGraph.html
- 핵심:
  - N+1: 부모 컬렉션 1번 조회 후, 각 부모의 연관(자식)을 위해 N번 추가 쿼리. `@OneToMany`/`@ManyToMany`의 기본 LAZY 로딩에서 발생.
  - 예: 주문 100건 조회 → `getCustomer()` 접근 시 101개 쿼리. 1,000 유저 → 1,001 쿼리.
  - 해법: ① **JOIN FETCH**(JPQL에서 즉시 로딩), ② **`@EntityGraph(attributePaths=...)`**(가져올 연관 선언), ③ **배치 페치**(`hibernate.default_batch_fetch_size`) — fetch join이 카르테시안 곱을 키울 때, ④ **DTO 프로젝션**(필요 컬럼만).
  - "잘못된 fetch 전략이 Spring Boot 성능 문제의 가장 흔한 원인 — 특히 N+1."
- 신선도: 개념·API 안정적. "2026 가이드" 출처가 최신 권장(EntityGraph vs JOIN FETCH 선택) 정리.

## 자료 7: JWT(stateless) vs 세션(stateful) 트레이드오프
- 출처: https://medium.com/@mesfandiari77/...why-jwt-might-be-overkill... (2025) , https://ducktypelabs.com/review-stop-using-jwt-for-sessions/ , https://stytch.com/blog/jwts-vs-sessions-which-is-right-for-you/
- 핵심 (양쪽 관점 병기):
  - **세션(stateful):** 즉시 폐기(revocation)·세밀한 제어 가능(`session.invalidate()`로 강제 로그아웃, "모든 기기 로그아웃"). 대가는 공유 세션 스토어. 전통 웹앱/SSR/브라우저 SPA/내부 도구에 적합. 브라우저 쿠키 사용 → localStorage보다 XSS에 강함.
  - **JWT(stateless):** 공유 스토어 없이 수평 확장 쉬움. 대가는 **로그아웃·폐기가 어렵다** — 서명된 JWT는 만료 전까지 유효, 무효화 수단 없음. 여러 프런트엔드를 서빙하는 API, 짧은 수명 액세스 토큰+리프레시 토큰에 적합.
  - 2025 관점(논쟁점): "stateless가 현대 표준, 세션은 유물"이라는 통념에 도전. **매 요청마다 Redis/DB로 JWT 상태를 확인한다면 — 추가 단계만 늘린 stateful을 재발명한 것이고 JWT의 본질적 이점을 잃은 것.**
- 신선도: "2025 기준 논쟁" — 본문 트레이드오프 챕터의 핵심 갈등.

## 자료 8: Spring Security 6.x — SecurityFilterChain 람다 DSL (WebSecurityConfigurerAdapter 제거)
- 출처: https://spring.io/blog/2022/02/21/spring-security-without-the-websecurityconfigureradapter/ (1차) , https://www.danvega.dev/blog/spring-security-6 , https://www.baeldung.com/spring-deprecated-websecurityconfigureradapter
- 핵심 사실:
  - **Spring Security 6.x에서 `WebSecurityConfigurerAdapter` 클래스 제거됨.** 상속 기반 설정 → **컴포넌트(빈) 기반 설정**으로 전환.
  - 새 방식: `SecurityFilterChain` 빈 + `WebSecurityCustomizer` 빈을 선언. **람다 DSL**로 설정.
  - 변경 사항: `authorizeRequests`(deprecated) → **`authorizeHttpRequests`**; `antMatchers`/`mvcMatchers`/`regexMatchers`(deprecated) → **`requestMatchers`**/`securityMatchers`.
  - 람다 DSL이 권장 — 더 읽기 쉽고 간결.
- 함정: 구버전(5.x 이하) 예제·튜토리얼·AI 출력이 `WebSecurityConfigurerAdapter`를 상속하는 코드를 줌 → 6.x에서 컴파일 실패. 본문 fact-check 대상.
- 신선도: "Spring Security 6.x 기준" (이 패턴은 5.7부터 점진 도입되어 6.x에서 완성).

## 자료 9: AI 페어코딩으로 Spring/JPA 학습·개발 (Cursor / Claude Code / Codex)
- 출처: https://katyella.com/blog/ai-assisted-java-development-claude-code/ , https://codenote.net/en/posts/java-spring-boot-ai-coding-agents-acceleration/ , https://alexmanrique.com/blog/development/2026/02/19/migrating-to-java17-and-spring-boot-335-using-claude-code-and-cursor.html , https://github.com/piomin/claude-ai-spring-boot
- 핵심:
  - 2026 일반 조합: **IDE의 Cursor + 터미널의 Claude Code(장기 작업)** — 표면이 달라 충돌 안 함.
  - AI는 Spring Boot 스캐폴드(REST API+JPA 엔티티+서비스 계층)를 한 방에 생성, 그 위에 비즈니스 로직을 얹기 좋음. JPA/Hibernate 엔티티 생성에 특히 강함(스키마/도메인 설명 → 정확한 엔티티 빠르게).
  - **검증 규율(중요):** "도구를 완전히 신뢰하지 말고 무엇을 하는지 리뷰·이해하라."
  - **가장 흔한 환각:** AI가 **현재 Java/라이브러리 버전에 없는 API를 제안** (예: `String.indent()`는 Java 12+인데 Java 11 프로젝트에 제안). → AI에게 버전을 명시해야 함. Spring에선 `javax.*` import, `WebSecurityConfigurerAdapter` 상속 같은 구버전 패턴이 정확히 이 함정.
- 신선도: "2026-02~05 기준" 도구 워크플로.

## 자료 10: 스펙 주도 개발(Spec-Driven) — AI에게 좋은 질문하기·학습 가속
- 출처: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ , https://addyosmani.com/blog/good-spec/ , https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality
- 핵심:
  - 워크플로: **스펙 → 계획 → 구현 → 테스트.** 명확한 markdown 스펙(무엇을 만들지)을 쓰고 에이전트가 구현.
  - 좋은 질문 기법: 프롬프트 마지막 문장을 **"내게 질문해줘(Ask me questions)"**로 — AI가 모호성을 되묻게 강제. "make sure you understand"로 이해 확인.
  - Claude Code의 **Plan Mode(Shift+Tab)**: 만들 것을 설명하면 에이전트가 기존 코드를 탐색하며 스펙 초안 작성, 모호성을 질문.
  - 작업을 작고 리뷰 가능한 단위로 쪼갠다 — 거의 TDD처럼 각 작업을 독립적으로 구현·테스트.
  - 학습 효과: "AI가 백과사전적 멘토 역할을 해 도메인을 더 빨리 배운다."
- 신선도: "2025-10 기준" — 후반부 "백엔드에 익숙해진 뒤 실제 개발 워크플로" 챕터의 토대.

## 자료 11: Thymeleaf(SSR) vs React(CSR) — 프런트엔드 관점
- 출처: https://medium.com/@sitharawanigasooriya_/...next-js-and-thymeleaf... , https://www.javaguides.net/2024/08/thymeleaf-vs-react-js.html , https://www.wimdeblauwe.com/blog/2024/12/31/problems-i-no-longer-have-by-using-server-side-rendering/
- 핵심 비교:
  - Thymeleaf = **서버사이드 렌더링(SSR)**, Java 템플릿 엔진. 서버가 HTML을 완성해 전송. 자바/Spring 개발자에게 학습 곡선 낮음(HTML 유사 문법). 다중 페이지 앱(MPA)에 흔히 사용.
  - React = 기본 **클라이언트사이드 렌더링(CSR)**. 브라우저가 최소 HTML+큰 JS 번들을 받아 동적 렌더. SPA.
  - SEO: Thymeleaf는 서버 렌더 HTML이라 크롤링 쉬움 ↔ React CSR은 어려울 수 있음(SSR로 보완).
  - SSR 이점(Wim Deblauwe): 프런트/백엔드 별도 버저닝 불필요, 매 상호작용에 최신 페이지.
- 프런트 개발자 관점: Next.js의 SSR/서버컴포넌트 멘탈 모델과 대응시키되, Thymeleaf는 "데이터 + 템플릿 → 완성 HTML"이라는 더 단순한 모델임을 강조.
- 신선도: "2024~2025 기준" 비교 (개념 안정적).

## 자료 12: Spring Boot vs Node.js/Express — 프런트엔드 개발자 학습곡선
- 출처: https://www.swiftorial.com/matchups/backend_framework/spring-vs-nodejs-java-vs-express-nestjs/ , https://www.javacodegeeks.com/2025/12/microservices-wars-spring-boot-vs-node-js-for-enterprise-architecture.html
- 핵심:
  - Node/Express: JS 친숙 개발자에게 진입 완만, 비동기·이벤트 루프 이해가 관건. DI는 내장 아님(InversifyJS/Awilix 등 외부).
  - Spring: Java + DI/AOP 개념으로 초기 학습 곡선 가파름, 생태계 방대해 처음엔 압도적. 단 Spring Boot가 설정·셋업을 대폭 단순화. **DI는 1급 내장 기능.**
  - React 개발자 인사이트: Node는 프런트/백 같은 언어(JS)라 친숙 ↔ Spring은 새 언어(Java) + 새 패러다임(DI). 책의 핵심 다리: NestJS의 DI(@Injectable)가 Spring DI의 좋은 비유.
- 신선도: "2025 기준" 비교.

---

## 커버리지 메모 (web 레인)
- 1차 소스(spring.io 블로그, GitHub 릴리스 노트, endoflife.date) 확보 — fact-checker 대조 기준 충분.
- 한국 엔지니어링 블로그(우아한형제들·토스·카카오 tech)는 이번 패스에서 개별 글까지 파고들지 못함 — community 레인 및 추가 패스 권장.
- 회사 1차 출처로 N+1·트랜잭션 성능 사례(우아한형제들 기술블로그 다수 존재) 보강 가치 있음.
