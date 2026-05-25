<!-- fact-check 로그 / 장르: tech-book / 검색·검증 시점: 2026-05-25 -->
<!-- 대조 기준: 01_reference.md (특히 §1·§3·§5·§6), research/web.md, research/papers.md -->
<!-- 2차 웹 확인: jjwt 0.11→0.12 API (GitHub jwtk/jjwt, Baeldung) -->

# 팩트체크 로그 — React/Next.js 개발자를 위한 Spring MVC + JPA 입문

라운드 1 (전 14장 초안 1차 검증). 판정 라벨: ✅확인됨 / ❌정정 필요 / ⚠️출처 없음·불확실 / 🕒신선도(시점 명기 필요).

**총평(한 줄):** 사실 오류(❌)는 **없음**. 모든 `(사실 확인 필요)` 주석은 레퍼런스/1차 출처로 ✅ 해소 가능하며, 주석 자체를 제거(또는 평문 신선도 경고로 치환)하면 된다. jjwt 0.12 API는 웹 2차 확인까지 통과. 미해소 위험 항목 없음.

---

## 공통 결론 — `(사실 확인 필요)` 주석 처리 지침

초안에 달린 18개 주석을 전수 검증했다. **전부 정확하거나 정당한 일반 서술이므로, 주석을 다음과 같이 해소(=삭제 또는 치환)하라.** 사실이 맞는데 주석만 남으면 final에 미해소 주석이 남는 사고이므로 반드시 처리할 것.

| 위치 | 주석 처리 |
|------|-----------|
| 01:46, 01:106 | RFC 9110 정확 → 괄호 `(사실 확인 필요)` **삭제** |
| 01:75 | Fielding 2000 정확 → `(사실 확인 필요)` **삭제** |
| 02:59 / 14:38 | 4.0.x·Framework 7 정확 → 주석 **삭제**, 단 🕒 시점 표기는 유지(아래 참고) |
| 02:60 | 3.5 OSS EOL 2026-06-30 정확 → 주석 **삭제** |
| 03:51 | Initializr 메뉴는 휘발성 → 본문이 이미 "달라질 수 있다"고 경고함. `(사실 확인 필요…)` **삭제**(본문 경고로 충분) |
| 03:53 | 버전 수치 정확 → `(사실 확인 필요…)` **삭제** |
| 08:54 | 회사별 구체 수치는 레퍼런스에 없음 → 아래 ⚠️ 지침대로 **약화 후 주석 삭제** |
| 09:72, 09:101 | Security 6.x API 정확 → 인용 블록 주석 **삭제** |
| 10:95 | jjwt 0.12 API 정확(웹 확인) → 주석 **삭제** |
| 10:129 | jakarta.servlet·필터 API 정확 → 주석 **삭제** |
| 10:203 | 6.x DSL 정확 → 주석 **삭제** |
| 11:66, 11:109 | Security/CORS 6.x API 정확 → 주석 **삭제** |
| 13:30 | Plan Mode = Shift+Tab 정확(레퍼런스 §3·web.md) → `(사실 확인 필요…)` **삭제**, 본문의 "공식 문서 확인" 안내문은 유지 가능 |
| 14:42 | Jackson 3·API versioning은 4.x 방향성으로 정확 → `(사실 확인 필요…)` **삭제**, 🕒 "2026-05 기준 가늠" 표기는 유지 |

---

## 1장 — fetch 너머의 HTTP

- ✅ **RFC 9110(HTTP Semantics)이 HTTP 메서드 의미를 정의** (01:46, 01:106) — 레퍼런스 §1.1·§6(표준 인용 권장: RFC 9110)과 일치. papers.md도 RFC 7231/9110을 HTTP semantics 근거로 명시.
  → **주석 해소:** "…정의되어 있다(사실 확인 필요)." 의 `(사실 확인 필요)`를 삭제. 사실 정확.
- ✅ **REST = Roy Fielding 2000년 박사학위 논문의 아키텍처 스타일** (01:75) — 레퍼런스 §1.2 / papers.md 문헌1과 정확히 일치 (Roy T. Fielding, 2000, UC Irvine, Ch.5).
  → **주석 해소:** `(사실 확인 필요)` 삭제.
- ✅ GET은 서버 상태를 바꾸지 않는다(안전성) — RFC 9110 §9.2.1 취지와 일치. 본문이 "멱등"과 "안전"을 혼용하지 않고 "상태를 바꾸지 않아야"로 적어 정확.
- ✅ 상태코드 의미(200/201/400/401/404/500/409/422) — 표준 의미와 일치. 정정 불필요.

## 2장 — AI와 함께 배운다는 것

- ✅ `WebSecurityConfigurerAdapter`가 Spring Security 6.x에서 **제거**, `authorizeRequests`→`authorizeHttpRequests`, `antMatchers`→`requestMatchers` (02:42, 02:48–51) — 레퍼런스 §3·§5 / web.md §8과 정확히 일치.
- 🕒/✅ **"최신 stable은 Spring Boot 4.0.6(2026-04-23 릴리스), Spring Framework 7.0"** (02:59) — 레퍼런스 §6 자료1과 **정확히 일치** (4.0.6 / 2026-04-23). 사실 맞음.
  → **주석 해소:** `(사실 확인 필요 — …대조)` 삭제. 단 이 수치는 휘발성이므로 본문에 "2026년 5월 기준"이 이미 깔려 있는지 확인(57행에 있음) → 유지.
- ✅ **"3.5의 OSS 커뮤니티 지원은 2026-06-30에 끝난다 / 상용 지원은 더 길다"** (02:60) — 레퍼런스 §6 자료1·신선도 경고박스와 일치(OSS 종료 2026-06-30, 상용 2032). 정확.
  → **주석 해소:** `(사실 확인 필요 — 상용 지원은 더 길게 이어진다)` 삭제. 본문이 "상용은 더 길다"를 이미 함의하므로 한 줄 덧붙여도 좋음(상용 2032).
- ✅ Java 17/21 LTS, Spring Boot 3.x가 Java 17+ 요구 — 레퍼런스 §6 자료2와 일치.

## 3장 — 첫 엔드포인트

- ✅ Gradle/Maven, `./gradlew bootRun`, `@SpringBootApplication`, 톰캣 자동설정 — 개념·명령 모두 정확(레퍼런스 §1.4).
- ✅ **Spring Boot 3.0이 jakarta 네임스페이스를 채택한 첫 버전** (03:176) — 레퍼런스 §1.6 / web.md 자료3과 정확히 일치.
- ⚠️→해소 **Initializr 정확한 메뉴 명칭·기본 선택값** (03:51) — Spring Initializr UI는 시점에 따라 바뀌는 휘발성 영역이라 1차 고정 불가. 단 본문이 이미 "화면 구성·선택지는 달라질 수 있다"고 명시적으로 경고하고 있어 **정당한 신선도 가드**다. 과잉 출처 요구 불필요.
  → **주석 해소:** 인용 박스의 `(사실 확인 필요: Initializr의 정확한 메뉴 명칭·기본 선택값)` 삭제. 본문 경고 문장으로 충분.
- ✅ **2026-05 시점 최신 stable·3.x EOL** (03:53) — 02장과 동일 근거로 정확(4.0.x stable, 3.5 OSS EOL 2026-06-30).
  → **주석 해소:** `(사실 확인 필요: …레퍼런스 §6 대조)` 삭제.
- ✅ Java 17 record DTO(5장에서 사용) 언급과 정합 — Java 16+ record 정식, Spring Boot 3.x는 17+이므로 안전.

## 4장 — DI와 IoC

- ✅ **Martin Fowler 2004, "IoC" 대신 "DI" 명칭 제안·정착** (04:61, 04:168) — 레퍼런스 §1.3 / papers.md 문헌2와 정확히 일치.
- ✅ 생성자 주입 권장(불변성·테스트), 단일 생성자는 `@Autowired` 생략 가능 (04:140–148) — Spring 공식 권장과 일치. 정확.
- ✅ 빈 기본 스코프 = 싱글톤, 시작 시 사전 인스턴스화 (04:154–156) — 레퍼런스 §1.4와 일치.
- ✅ `@Component`/`@Service`/`@RestController` 스테레오타입 관계 — 정확.

## 5장 — REST API·검증·예외·CORS·테스트

- ✅ Jakarta Bean Validation(구현체 Hibernate Validator), `@Valid @RequestBody`, `MethodArgumentNotValidException`, `@RestControllerAdvice`+`@ExceptionHandler`, `ResponseEntity` (05 전반) — 레퍼런스 §3·§5 / web.md 자료5와 정확히 일치.
- ✅ `jakarta.validation.constraints.*` 네임스페이스, `spring-boot-starter-validation` 의존성 필요 (05:62–77) — 정확.
- ✅ `@WebMvcTest`로 컨트롤러 슬라이스 테스트, MockMvc ≈ supertest, `jsonPath` (05:283–322) — API 정확. `@WebMvcTest`는 웹 계층만 로드하고 서비스는 mock 필요하다는 설명도 정확.
- ✅ CORS는 브라우저(Same-Origin Policy)가 막고 서버가 허용 헤더로 푼다, preflight=OPTIONS, `CorsConfigurationSource`/`UrlBasedCorsConfigurationSource` 빈 (05:215–261) — 개념·API 정확(레퍼런스 §1.1·§3).
- ✅ `allowCredentials(true)` + `allowedOrigins("*")` 동시 사용 시 브라우저 거부 (05:261, 11장 재등장) — CORS 스펙상 정확.

## 6장 — JPA 부착

- ✅ **임피던스 불일치 / Ted Neward 2006 "The Vietnam of Computer Science"** (06:17) — 레퍼런스 §1.5 / papers.md 문헌4와 정확히 일치. 연도 2006 정확.
- ✅ **Repository 패턴 = Eric Evans 2003 DDD, Spring Data JPA가 프록시로 구현** (06:93) — 레퍼런스 §1.5 / papers.md 문헌3과 일치. 연도 2003 정확.
- ✅ JPA=Jakarta Persistence API, 구현체 Hibernate (06:15) — 정확. (네임스페이스 전환으로 "Java Persistence API"가 아니라 "Jakarta Persistence API"로 표기한 것도 jakarta 시대에 맞다.)
- ✅ `jakarta.persistence.*` import, `@Entity`/`@Id`/`@GeneratedValue(IDENTITY)`/`@ManyToOne`/`@JoinColumn`/`@OneToMany`, `protected` 기본 생성자 요구 (06 전반) — 모두 정확.
- ✅ `JpaRepository<Task, Long>`가 save/findById/findAll/deleteById 제공 — 정확.
- ✅ H2 `jdbc:h2:mem:`, `ddl-auto: create-drop`(운영 금지)·`validate`/`none`, `show-sql: true` (06:167–199) — 설정·경고 정확.

## 7장 — 영속성 컨텍스트

- ✅ 영속성 컨텍스트=1차 캐시, 더티 체킹(변경 감지), 스냅샷 비교, save 없이 UPDATE (07 전반) — 레퍼런스 §1.5 / community 패턴3과 일치. 개념 정확.
- ✅ 엔티티 생애 transient/persistent/detached (07:61–77) — JPA 표준 상태 모델과 정확히 일치(용어: 비영속/영속/준영속).
- ✅ 연관관계 주인 = `@JoinColumn` 가진 쪽, `mappedBy`=거울 (07:142–168) — 정확.
- ✅ `@ManyToOne` 기본 EAGER / `@OneToMany` 기본 LAZY, LAZY 권장, 프록시 (07:200–202) — JPA 스펙 기본값과 정확히 일치(다대일·일대일=EAGER, 일대다·다대다=LAZY).
- ✅ `LazyInitializationException`은 트랜잭션(컨텍스트) 밖 지연 로딩 접근 시 (07:204–208) — 정확.
- ✅ `@Transactional`이 컨텍스트 경계, `readOnly=true`로 스냅샷 생략 (07:210–230) — 정확.

## 8장 — N+1과 SQL 로그

- ✅ **N+1 정의·발생 원리(지연 로딩+컬렉션 접근), 해법 4종**(JOIN FETCH / `@EntityGraph(attributePaths)` / 배치 페치 `hibernate.default_batch_fetch_size` / DTO 프로젝션) (08:58–137) — 레퍼런스 §3 N+1 4종·web.md 자료6과 정확히 일치.
- ✅ JOIN FETCH+페이징 함정: 컬렉션 fetch + 페이징 시 메모리 페이징 경고 `firstResult/maxResults specified with collection fetch; applying in memory` (08:139–152) — Hibernate 실제 경고 메시지와 정확히 일치. 배치 페치로 우회 권장도 정확.
- ✅ `@Transactional` self-invocation 무효(프록시 미경유) (08:181–198) — 레퍼런스 §4.5·community 패턴과 일치. 정확.
- ✅ `@DataJpaTest` = 리포지토리 슬라이스, 인메모리 DB·자동 롤백 (08:215–246) — 정확.
- ⚠️→약화 **"우아한형제들·토스·카카오 등 기술 블로그… 응답 수 초·쿼리 수백·수천 번… 대폭 단축"** (08:54) — N+1이 흔한 통과의례라는 **일반 서술은 정당**(community·web 한계 메모와 정합). 그러나 **특정 회사명을 들며 구체 수치를 귀속**하는 부분은 레퍼런스에 개별 포스트모템 원문이 **없다**(레퍼런스 §7 "회사 1차 사례 미수집"으로 명시적 한계). 구체 수치·회사 귀속은 출처 없음.
  → **정정 지시:** 회사명 나열과 수치 뉘앙스를 약화하라. 예) "국내외 여러 회사 기술 블로그에서 N+1로 응답이 느려졌다가 쿼리를 크게 줄여 개선한 사례를 어렵지 않게 볼 수 있다"처럼 **특정 회사 귀속·구체 수치를 빼고** 일반화. 그 후 `(구체 수치·출처는 사실 확인 필요)` 주석 삭제. (특정 회사 포스트모템을 꼭 인용하려면 개별 글 URL을 확보해 각주로 달 것 — 미확보 시 일반화가 안전.)

## 9장 — 보안 기초

- ✅ 인증(authentication)/인가(authorization) 구분, 인증 선행 (09:9–17) — 정확.
- ✅ 필터체인 모델, Next.js middleware / Express 미들웨어 비유 (09:19–37) — 레퍼런스 §2 / web.md와 정합. 비유 적절.
- ✅ **`SecurityFilterChain` 빈 + `authorizeHttpRequests`/`requestMatchers`/`httpBasic` 람다 DSL** (09:47–70, 주석 09:72) — 레퍼런스 §3·§5 / web.md §8과 정확히 일치. `http.build()` 반환도 정확.
  → **주석 해소:** 09:72 인용 박스 삭제. API 정확.
- ✅ Security 의존성 추가 시 전체 잠김·임시 비밀번호 콘솔 출력 (09:41) — 정확.
- ✅ **`BCryptPasswordEncoder`/`PasswordEncoder` 빈, BCrypt 의도적 느린 해시** (09:84–101, 주석 09:101) — 레퍼런스 §3·§5 / web.md §8과 정합. 클래스명·빈 등록 방식 정확.
  → **주석 해소:** 09:101 인용 박스 삭제.
- ✅ 401(미인증)/403(권한 없음) 구분 — 정확.

## 10장 — JWT (신선도 클라이맥스)

- ✅ **JWT = RFC 7519, 헤더.페이로드.서명 3조각, HS256, 서명은 위조 방지(암호화 아님), 페이로드에 민감정보 금지** (10:9–24) — 레퍼런스 §1.1·§6(RFC 7519) / papers.md와 정확히 일치.
- ✅ stateless 모델·수평 확장 이점·즉시 무효화 어려움·짧은 access + refresh 토큰 (10:26–34) — 레퍼런스 §4.2 / web.md 자료7과 일치.
- ✅ localStorage(XSS 노출) vs httpOnly 쿠키(JS 접근 불가, CSRF 숙제) (10:36–46) — 레퍼런스 §4.2·§4.2 프런트 진입점과 일치. 정확.
- ✅✅ **jjwt 0.12.x API: `Jwts.builder().subject().issuedAt().expiration().signWith(key).compact()` / `Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload().getSubject()` / `Keys.hmacShaKeyFor`** (10:61–92, 주석 10:95) — **레퍼런스에 jjwt 세부 없어 웹 2차 확인 수행**. GitHub jwtk/jjwt 및 Baeldung 확인 결과: 0.12에서 `Jwts.parser()`가 `JwtParserBuilder` 반환, `verifyWith`/`parseSignedClaims`/`getPayload`가 신 API, 구버전 `parserBuilder()`/`setSigningKey()`/`setSubject()`는 제거·deprecated. **초안 코드가 0.12 신 API와 정확히 일치.** 초안이 경고한 구버전 패턴(`parserBuilder()`, `setSubject()`)도 정확히 0.11 이하 패턴이 맞다.
  → **주석 해소:** 10:95 인용 박스 삭제. API 정확(2차 확인 완료).
- ✅ **`OncePerRequestFilter`/`SecurityContextHolder`/`UsernamePasswordAuthenticationToken`, `HttpServletRequest`=`jakarta.servlet.*`** (10:101–129, 주석 10:129) — 레퍼런스 §1.6·§3·§5와 정합. Spring Security 6.x(Spring 6/Jakarta EE 9+)에서 서블릿 API는 `jakarta.servlet.*`가 맞다. 정확.
  → **주석 해소:** 10:129 인용 박스 삭제.
- ✅ **before/after 교정: `WebSecurityConfigurerAdapter` 제거, `.csrf(csrf->csrf.disable())`, `.sessionManagement(sm->sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))`, `.authorizeHttpRequests`, `.requestMatchers`, `.addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)`** (10:139–203, 주석 10:203) — 레퍼런스 §3·§5 / web.md §8과 정확히 일치. 구버전 `.csrf().disable().authorizeRequests().antMatchers().and().addFilterBefore(...)` 대비도 정확. JWT는 stateless라 보통 CSRF off + STATELESS도 통상 권장과 일치.
  → **주석 해소:** 10:203 인용 박스 삭제.

## 11장 — 세션(stateful)·트레이드오프

- ✅ **2025 흐름: "매 요청 Redis/DB로 JWT 검증=stateless 이점 잃은 stateful 재발명"** 비판 (11:13–17) — 레퍼런스 §4.2 관점B / web.md 자료7(2025 논쟁)과 정확히 일치. 시점 "2025년 들어" 표기 적절(🕒 충족).
- ✅ 세션=서버 세션 스토어 + 세션 ID 쿠키(JSESSIONID), 기본 메모리·다중 서버 시 Redis(Spring Session) (11:19–72) — 정확.
- ✅ **`SessionCreationPolicy.IF_REQUIRED`/`sessionManagement`/`formLogin` 람다 DSL** (11:35–66, 주석 11:66) — 레퍼런스 §3·§5 / web.md §8과 정합. API 정확. `formLogin`이 세션·JSESSIONID 자동 처리도 정확.
  → **주석 해소:** 11:66 인용 박스 삭제.
- ✅ **`CorsConfiguration.setAllowCredentials(true)`/`setAllowedOrigins`/`setAllowedMethods`/`setAllowedHeaders`, `fetch(..., {credentials:'include'})`** (11:84–109, 주석 11:109) — Spring Framework 6.x `CorsConfiguration` API와 정확히 일치. credentials+wildcard 금지도 정확.
  → **주석 해소:** 11:109 인용 박스 삭제.
- ✅ 트레이드오프 표(즉시 폐기·확장성·XSS·구현 손품) (11:127–134) — 레퍼런스 §4.2와 정합. 균형 잡힌 서술, 단정 오류 없음.

## 12장 — Thymeleaf·SSR vs CSR

- ✅ `@Controller`(뷰 이름 반환) vs `@RestController`(JSON), `Model.addAttribute`, `templates/` 경로, `th:each`/`th:text`/`th:href`/`@{...}`/`${...}`, `@PathVariable`, 자연 템플릿 (12 전반) — 레퍼런스 §2 / web.md 자료11과 정합. Thymeleaf 문법 정확. 본문이 "Thymeleaf 문법은 버전 따라 세부 변동" 가드까지 둠(🕒 충족).
- ✅ SSR/CSR 트레이드오프, 관리자·CRUD·SEO엔 SSR, 풍부한 상호작용·다중 클라이언트엔 CSR/REST (Wim Deblauwe 맥락) (12:123–139) — 레퍼런스 §4.3과 일치. 균형 서술, 단정 오류 없음.
- ✅ React Server Components/SSR hydration 설명 (12:107–119) — 프런트 사실관계 정확(서버 컴포넌트는 서버 렌더 결과 HTML 전송, Thymeleaf는 hydration 단계 없음). 정확.

## 13장 — 스펙→설계→구현→테스트 (AI 워크플로)

- ✅ 스펙→설계→구현→테스트, "Ask me questions", 버전·컨벤션 컨텍스트 제공 (13 전반) — 레퍼런스 §3·§5 / web.md 자료9·10과 일치.
- ✅ Cursor(IDE 내장) / Claude Code(터미널, Anthropic) 역할 구분 (13:24–32) — 레퍼런스 §3과 일치. "Claude Code = Anthropic이 만든 터미널 기반 코딩 에이전트" 정확.
- ✅ **Claude Code Plan Mode = `Shift+Tab` 전환** (13:30, 주석) — 레퍼런스 §3(자료9·10) / web.md L96 "Plan Mode(Shift+Tab)"와 정확히 일치. 본문이 "구체 키·동작은 공식 문서로 재확인" 가드도 둠(🕒 충족, 도구 UX는 휘발성).
  → **주석 해소:** 13:30 `(사실 확인 필요 — Plan Mode 진입 키·동작 세부는 공식 문서로 재확인)` 삭제. 본문의 "도구의 구체 기능·UX는 빠르게 바뀔 수 있으니 공식 문서 확인"(13:28) 가드는 유지.
- ✅ 다대다(`@ManyToMany`)+목록+페이징이 N+1·페이징 함정 동시 유발, 검증 4렌즈(네임스페이스/SQL 로그/DTO/트랜잭션) (13:84–124) — 8장과 정합, 기술적으로 정확.

## 14장 — 정리·3.x→4.x

- 🕒/✅ **"2026년 5월 기준 최신 stable 4.0.x대, Spring Framework 7.0, 3.5 OSS 지원 종료 코앞"** (14:38, 주석) — 레퍼런스 §6과 정확히 일치(4.0.6 / 2026-04-23, 3.5 OSS EOL 2026-06-30). 본문이 시점·휘발성 경고를 이미 포함.
  → **주석 해소:** `(사실 확인 필요 — …공식 문서를 함께 확인하자.)` 중 **앞부분(수치 대조 요구)은 삭제**(검증 완료), **뒷부분(시점·공식문서 확인 권고)은 본문 평문으로 남겨도 무방**. "정확한 4.0 패치 버전"을 굳이 명시하려면 "4.0.6(2026-04-23)"로 박아도 사실에 부합.
- ✅/🕒 **4.x 변경: Jackson 3 메이저 전환, API versioning** (14:42, 주석) — web.md L53 "Spring Boot 4는 Jackson 3로 이동, 3.x는 Jackson 2" / 레퍼런스 §7 "Jackson 3·API versioning 등 4.x 변경"과 일치. 방향성으로 정확. 구체 변경 목록은 시점 의존이므로 "가늠"으로 표현한 것이 적절(🕒 충족).
  → **주석 해소:** `(사실 확인 필요 — 4.x/Framework 7의 구체 변경 목록은…)` 삭제. 본문이 이미 "큰 줄기만 가늠", "마이그레이션 가이드를 1차 근거로 확인" 가드를 포함하므로 평문 안내는 유지.
- ✅ jakarta 전환은 3.0의 가장 큰 강이고 4.x로 자산 이월 (14:40) — 정확.

---

## 미해소(위험) 항목

**없음.** 모든 구체 주장이 레퍼런스 또는 1차/2차 출처로 확인됨. 단 8:54의 회사 귀속·구체 수치만 ⚠️(출처 없음)으로, 저술가 재량으로 덮지 말고 **반드시 일반화 약화**로 처리할 것(사실 오류는 아니나, 검증 불가한 구체 귀속이므로 책 신뢰도 보호 차원).

## chapter-writer 액션 요약

1. **18개 `(사실 확인 필요)` 주석 전부 삭제** (위 표·각 장 지침대로). 사실은 전부 맞으므로 주석만 걷어내면 됨.
2. **8:54만 본문 약화**: 특정 회사명(우아한형제들·토스·카카오) 귀속 + 구체 수치 뉘앙스를 일반화한 뒤 주석 삭제.
3. 🕒 시점·휘발성 가드 문장(2026-05 기준, 공식 문서 확인 권고)은 **유지**가 바람직 — 빠르게 바뀌는 버전·도구 UX 영역이므로.
4. 선택: 14:38에 "4.0.6(2026-04-23)" / 3.5 상용 지원 2032 같은 구체 수치를 박아 신뢰도를 더 높일 수 있음(레퍼런스 §6 근거 있음).
