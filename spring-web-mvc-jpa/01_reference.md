<!-- 검색 시점: 2026-05-25 기준 / 출처 레인: web.md · papers.md · community.md -->

# React/Next.js 개발자를 위한 Spring MVC + JPA 백엔드 입문 — 레퍼런스

**대상 독자:** 자바 문법은 끝냈고 SQL 기본은 알지만 백엔드 실무 경험이 없는 프런트엔드 개발자(React/Next.js 능숙, Cursor로 AI 페어코딩 경험). 자세한 설명이 필요한 입문자.
**버전 기준:** Spring Boot **3.x**(권장 3.5), Spring Framework **6.x**, Spring Security **6.x**, Java **17/21 LTS**, Jakarta EE 9+(`jakarta.*`).

> ⚠️ **버전 신선도 경고 (fact-checker 필독):** 집필 기준은 Spring Boot **3.x**지만, 2026-05-25 시점 실제 최신 stable은 **Spring Boot 4.0.6(2026-04-23) / Spring Framework 7.0**이다. 또한 **Spring Boot 3.5의 OSS 커뮤니티 지원은 2026-06-30에 종료**된다(상용은 2032까지). 본문은 "3.x가 여전히 프로덕션 주류라 학습 기준으로 삼되, 신규 그린필드는 4.x를 고려하라"를 명시해야 한다. [web 자료 1·2]

---

## 1. 개념과 정의

### 1.1 HTTP/웹 핵심 — 프런트가 이미 아는 것 vs 새로 배울 것
- **이미 아는 것(경계):** 프런트 개발자는 `fetch`를 통해 요청·응답, 메서드(GET/POST/PUT/DELETE), 상태코드(200/201/400/401/404/500), 헤더, JSON 바디, CORS를 이미 다뤄봤다. — 책은 이 자산을 출발점으로 삼아 **"클라이언트 입장에서 본 HTTP"를 "서버 입장에서 본 HTTP"로 뒤집는다.**
- **새로 배울 것:** 서버가 요청을 라우팅·역직렬화·검증·처리·직렬화하는 전 과정, 쿠키/세션의 서버 측 수명주기, 상태코드를 **내가 결정**하는 책임. REST는 단순 규약이 아니라 아키텍처 스타일이라는 점(§1.2).
- 표준 1차 근거 권장: HTTP semantics RFC 9110, 쿠키 RFC 6265, JWT RFC 7519. [papers 메모]

### 1.2 REST — 권위 있는 정의 vs 업계 용법
- **1차 정의:** Roy T. Fielding, 2000 박사학위 논문 "Architectural Styles and the Design of Network-based Software Architectures"(UC Irvine), Chapter 5. REST는 분산 하이퍼미디어를 위한 아키텍처 스타일로, **client-server · stateless · cacheable · uniform interface · layered system**(+ 선택 code-on-demand) 제약의 조합. [papers 자료 1]
- **논쟁(§4.1로 연결):** 업계의 "REST API"는 Fielding의 엄밀한 정의(특히 HATEOAS)와 다르게 느슨히 차용된다. [papers 자료 1 보충]

### 1.3 IoC / DI — Spring의 심장, 그리고 프런트와의 연결고리
- **개념(1차):** Martin Fowler, 2004, "Inversion of Control Containers and the Dependency Injection pattern". 객체가 협력자를 직접 만들지 않고 **외부(컨테이너)가 주입** → 결합도↓, 테스트 시 mock 주입 쉬움. Fowler가 모호한 "IoC" 대신 **DI**라는 명칭을 정착시킴. Spring 권장은 **생성자 주입**. [papers 자료 2]
- **프런트 다리:** NestJS `@Injectable`/Angular DI가 같은 계보 — Next.js만 쓴 독자에겐 "props로 의존성을 내려주는 것의 런타임 자동화" 비유가 유효. [web 자료 12]

### 1.4 Spring Web MVC — DispatcherServlet과 요청 흐름
- DispatcherServlet = **Front Controller**, 모든 요청의 진입점. 흐름: 요청 → DispatcherServlet → HandlerMapping → `@Controller`/`@RestController` → (REST는 바디 직렬화 / MVC는 ViewResolver→View). 초기화 시 IoC 컨테이너 생성, 싱글톤 빈 사전 인스턴스화. [web 자료 4]
- Spring Boot 진입: `start.spring.io`(Initializr) + 자동설정(auto-configuration)으로 보일러플레이트 제거.

### 1.5 ORM/JPA의 본질
- **임피던스 불일치:** 객체 모델 ↔ 관계형 모델의 간극을 ORM이 메우지만 추상화는 **누수된다(Ted Neward, 2006, "The Vietnam of Computer Science")** — 편하지만 결국 생성 SQL을 봐야 하는 순간이 온다. [papers 자료 4] → §5의 실무 규율의 이론적 근거.
- **Repository 패턴:** Eric Evans, 2003(DDD). Spring Data JPA `Repository`가 이 패턴의 구현 — 인터페이스만 선언하면 프록시가 구현 제공. [papers 자료 3]
- **영속성 컨텍스트:** 트랜잭션 동안 엔티티를 추적하는 "출석부". 더티 체킹으로 `save()` 없이도 변경 감지→커밋 시 UPDATE. **트랜잭션 밖에선 컨텍스트 없음**(→ LazyInitializationException). [web 자료 자료 — JPA, community 패턴 3]

### 1.6 Jakarta 네임스페이스
- 2017 Oracle→Eclipse 기증 → 상표 문제로 Jakarta EE 리브랜딩 → Jakarta EE 9에서 `javax.*`→`jakarta.*` 전면 전환(`javax.persistence`→`jakarta.persistence` 등). **Spring Boot 3.0이 이를 채택한 첫 버전.** [web 자료 3]

---

## 2. 핵심 관점들 (프런트엔드 멘탈 모델 ↔ Spring 대응)

| 프런트(React/Next/Node) | Spring 백엔드 | 핵심 차이·주의 |
|---|---|---|
| `fetch`로 요청 보내는 **클라이언트** | 요청을 받는 **서버** | 상태코드·직렬화를 내가 결정 [web 1.1] |
| Next.js API routes / 서버액션 | `@RestController` + `@RequestMapping` | 라우팅이 어노테이션 기반, 메서드=핸들러 [web 자료 4] |
| props/context로 의존성 전달, NestJS `@Injectable` | DI/IoC 컨테이너, 생성자 주입 | 런타임 자동 와이어링("magic") — 무엇으로 치환되는지 봐야 [papers 2 · community 2] |
| `fetch().json()` 수동 파싱 | Jackson 자동 직렬화/역직렬화 + `@Valid` | 검증·역직렬화가 프레임워크 책임 [web 자료 5] |
| Prisma/Drizzle ORM, 쿼리 직접 | JPA/Hibernate, 영속성 컨텍스트·더티 체킹 | "save 안 했는데 바뀜" 등 비가시 동작 [community 3] |
| Next.js SSR/서버컴포넌트 | Thymeleaf SSR(MPA) | Thymeleaf는 "데이터+템플릿→완성 HTML"의 더 단순한 모델 [web 11] |
| 토큰을 localStorage/쿠키에 저장 | 세션(서버 스토어) or JWT | 저장 위치·폐기 전략이 트레이드오프 [web 7 · community 6] |

- **언어+패러다임 더블 펀치(현장 합의):** JS→Java는 새 언어 + 정적 타입 + 어노테이션 마법이 동시에 온다. 책 톤은 **"마법 걷어내기(minus the magic)"** — 어노테이션이 무엇을 하는지 보여주기. [community 2 · web 자료 4]
- **학습 순서 관점(현장 합의):** IoC/DI/AOP 이론부터 시작하면 막힌다 → **동작하는 엔드포인트 먼저, 이론은 뒤에.** 프런트에서 "일단 렌더부터" 배운 경로와 동일. [community 1]

---

## 3. 대표 사례 / 표준 패턴

- **REST API 개발 단계:** DTO 정의 → 컨트롤러 파라미터에 `@Valid`(Jakarta Bean Validation/Hibernate Validator) → 실패 시 `MethodArgumentNotValidException` → `@RestControllerAdvice`+`@ExceptionHandler`로 전역 처리 → `ResponseEntity`로 구조화 응답(타임스탬프·상태·필드별 메시지). 검증은 **DTO 계층**에서(엔티티 아님). [web 자료 5]
- **Spring Security 6.x 설정(최신):** `WebSecurityConfigurerAdapter` **제거됨** → `SecurityFilterChain` 빈 + 람다 DSL. `authorizeRequests`→**`authorizeHttpRequests`**, `antMatchers`/`mvcMatchers`→**`requestMatchers`**. [web 자료 8]
- **N+1 해법 4종:** ① JOIN FETCH ② `@EntityGraph(attributePaths=…)` ③ 배치 페치(`hibernate.default_batch_fetch_size`) ④ DTO 프로젝션. JOIN FETCH+페이징은 중복 row/페이징 깨짐 함정 → 배치 페치로 우회. [web 자료 6 · community 4]
- **AI 페어코딩 워크플로(후반부):** Cursor(IDE)+Claude Code(터미널 장기작업) 조합. **스펙→계획→구현→테스트**. Claude Code Plan Mode(Shift+Tab)로 스펙 초안·기존 코드 탐색. 프롬프트 끝에 "Ask me questions"로 모호성 되묻게. AI는 스캐폴드/엔티티 생성에 강함. [web 자료 9·10 · community 7]

---

## 4. 논쟁점 · 상충 관점 (트레이드오프)

### 4.1 REST: 엄밀한 정의 vs 실무 용법
- 관점 A(엄밀): Fielding 제약(특히 HATEOAS)을 지켜야 진짜 REST. 관점 B(실무): 대부분의 "REST API"는 HTTP+JSON+자원 URL 수준의 느슨한 차용. [papers 1]

### 4.2 JWT(stateless) vs 세션(stateful) — 커뮤니티 강하게 갈림
- **관점 A(JWT 기본):** 공유 스토어 없이 수평 확장, 여러 프런트엔드 서빙 API/모바일에 적합, 짧은 액세스 토큰+리프레시. [web 자료 7]
- **관점 B(세션 재평가, 2025 흐름):** 즉시 폐기·"모든 기기 로그아웃"이 필요하면 세션이 단순·안전. 브라우저 쿠키가 localStorage보다 XSS에 강함. **"매 요청 Redis/DB로 JWT 검증 = stateless 이점 잃은 stateful 재발명."** [web 자료 7 · community 6]
- **프런트 진입점:** "토큰을 localStorage vs httpOnly 쿠키 어디 저장?"이 프런트 개발자에게 직접 와닿는 갈등. [community 6]

### 4.3 SSR(Thymeleaf) vs CSR(React) — "굳이 Thymeleaf?"
- 회의: React/Next 쓰던 사람이 退보 아닌가. 옹호: 관리자·간단 CRUD·SEO 페이지는 SSR이 빠르고 단순, 프런트/백 버저닝·API 계약 불필요(Wim Deblauwe). 결론: "도구는 상황 따라." [web 자료 11 · community 8]

### 4.4 AI로 배우기 — 기대 vs 불안
- 기대: 보일러플레이트 제거, 백과사전적 멘토. 불안: 생성 코드 이해 못 하면 디버깅서 무너짐, **버전 안 맞는/구버전 API를 자신 있게 제안**(예: `javax.*` import, `WebSecurityConfigurerAdapter` 상속). 합의: 코드 읽고 SQL/동작 검증, 버전을 프롬프트에 명시. [web 자료 9 · community 7]

### 4.5 ORM 추상화 — 편의 vs 누수
- JPA의 마법(더티 체킹·지연 로딩)은 편하지만 N+1·LazyInitializationException·`@Transactional` self-invocation 무효 등으로 누수. → "SQL 로그를 보라"는 규율. [papers 4 · community 3·4]

---

## 5. 실무 적용 팁

- **신선도/버전 규율:** 인터넷·AI의 예제는 `javax.*`, `WebSecurityConfigurerAdapter`, `authorizeRequests` 등 구버전 패턴을 줄 수 있다 → 3.x/6.x 기준으로 식별·치환. AI엔 버전 명시. [web 3·8·9 · community 5]
- **JPA 함정 3종:** ① 더티 체킹/flush 타이밍("save 없이 바뀜") ② `@Transactional` self-invocation 무효 ③ 트랜잭션 밖 지연 로딩 → LazyInitializationException. 영속성 컨텍스트="출석부" 비유. [community 3]
- **N+1은 운영서 터진다:** 개발 땐 데이터 적어 안 보임 → **SQL 로그 켜서 직접 보기** 실습. [community 4]
- **검증은 DTO에서, 예외는 전역 핸들러로.** [web 자료 5]
- **AI 학습 루틴:** 스캐폴드는 AI, 비즈니스 로직은 직접; 생성 코드는 반드시 읽고 검증; "Ask me questions"로 스펙 명료화; 작업을 작게 쪼개 TDD처럼. [web 자료 10 · community 7]
- **학습 진입 순서:** 동작하는 REST 엔드포인트 → 점진적으로 DI/JPA/보안. 이론 선행 금물. [community 1]

---

## 6. 참고문헌 (발행일·버전·검색시점 신선도 메타 포함)

**1차/권위 (web 레인, 검색 2026-05-25):**
1. Spring Boot 버전·EOL — endoflife.date/spring-boot, spring.io. *3.5 출시 2025-05-31, OSS 종료 2026-06-30 / 4.0 출시 2025-11-30, 최신 4.0.6 2026-04-23.*
2. Spring Boot 3.0 Release Notes — github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes. *SB3.x = Java17+ / Spring Framework 6.*
3. Preparing for Spring Boot 3.0 (javax→jakarta) — spring.io/blog/2022/05/24/preparing-for-spring-boot-3-0/. *Jakarta EE 9 기준.*
4. DispatcherServlet/IoC — medium @sweetyleah0, javarevisited.blogspot.com. *개념(버전 무관).*
5. REST 검증·예외·ResponseEntity — baeldung.com/exception-handling-for-rest-with-spring, javathinking.com, dev.to @gianfcop98. *SB3.x/Jakarta Bean Validation.*
6. N+1 — sharpskill.dev (2026 가이드), baeldung EntityGraph, tech.asimio.net. *개념 안정.*
7. JWT vs 세션 — medium @mesfandiari77 (2025), ducktypelabs.com, stytch.com. *2025 논쟁.*
8. Spring Security 6 SecurityFilterChain — spring.io/blog/2022/02/21/...without-the-websecurityconfigureradapter, danvega.dev/blog/spring-security-6, baeldung. *Security 6.x 기준.*
9. AI 페어코딩 Spring — katyella.com, codenote.net, alexmanrique.com(2026-02), github.com/piomin/claude-ai-spring-boot. *2026-02~05.*
10. 스펙 주도 개발/좋은 질문 — github.blog spec-driven, addyosmani.com/blog/good-spec, developers.redhat.com(2025-10). *2025-10.*
11. Thymeleaf vs React SSR/CSR — medium @sitharawanigasooriya_, javaguides.net(2024-08), wimdeblauwe.com(2024-12). *2024~2025.*
12. Spring Boot vs Node — swiftorial.com, javacodegeeks.com(2025-12). *2025.*

**Seminal/이론 (papers 레인):**
- Fielding, R.T. (2000). *Architectural Styles and the Design of Network-based Software Architectures.* PhD diss., UC Irvine. roy.gbiv.com/pubs/dissertation/top.htm
- Fowler, M. (2004). *Inversion of Control Containers and the Dependency Injection pattern.* martinfowler.com/articles/injection.html
- Evans, E. (2003). *Domain-Driven Design.* Addison-Wesley (ISBN 0-321-12521-5).
- Neward, T. (2006). *The Vietnam of Computer Science.* (ORM 임피던스 불일치.)
- 표준(권장 추가 인용): RFC 9110(HTTP Semantics), RFC 6265(Cookies), RFC 7519(JWT).

**커뮤니티 (community 레인, 검증되지 않은 현장 의견 — 사실 주장 아닌 "공감/논쟁" 소재):**
- 인프런 김영한 스프링 강의·우아한형제들 백엔드 로드맵(국내 표준 학습 경로), OKKY/r/SpringBoot/r/java 반복 패턴, dev.to/headf1rst(`@Transactional` 함정), thameena.blog(영속성 컨텍스트 비유).

---

## 7. 리서치 한계 (커버하지 못한 영역)

- **한국 커뮤니티 원문 인용 부족:** WebSearch가 미국 중심이라 OKKY/velog **개별 스레드 날것 인용**을 직접 확보하지 못함. 반복 패턴·정황은 신뢰도 있으나, 챕터 오프닝용 생생한 인용은 추가 패스(velog/OKKY 직접 수집) 권장. [community 한계]
- **회사 1차 사례 미수집:** 우아한형제들·토스·카카오 tech의 N+1/트랜잭션 실전 포스트모템을 개별 글까지 파지 못함 — 사례 보강 가치 큼. [web 한계]
- **표준 1차 인용(RFC) 본문 미수집:** HTTP/쿠키/JWT RFC를 식별만 하고 구체 조항 인용은 미확보 — 보안·HTTP 챕터에서 보강 권장. [papers 한계]
- **학술 논문 희소:** 주제 특성상 peer-reviewed 논문 밀도가 낮음 — 이론은 seminal 문헌으로 충분히 커버되나, ORM 성능 등은 산업 문헌 의존.
- **버전 경계 리스크(중요):** 집필 기준 3.x가 OSS EOL(2026-06-30)에 근접하고 4.x/Framework 7이 이미 stable. 본문은 이 사실을 숨기지 말고 "왜 3.x로 배우는가"를 명시해야 하며, Jackson 3·API versioning 등 4.x 변경은 §1·§3 일부 세부(직렬화)에 영향 가능 — fact-checker가 3.x 한정으로 대조할 것. [web 1·2]
