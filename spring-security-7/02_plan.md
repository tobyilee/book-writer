# Spring Security 7 심층 활용 — 저술 계획 (v2, 1차 리뷰 반영)

## 0. 제목 후보

### 후보 A. **토비의 Spring Security 7**
- 부제: *내부 아키텍처부터 Zero Trust·Passkeys·MFA까지, Spring Boot 4 기반 심층 레퍼런스*
- 슬러그: `toby-spring-security-7`
- 한 줄 컨셉: "토비의 스프링" 계보를 잇는 보안 레퍼런스. 필터 한 줄이 왜 그렇게 동작하는지를 끝까지 파고든다.
- 추천도: ★★★★★ — Toby 평어체 톤과 가장 잘 맞고, 본 하네스의 기본 저자(Toby-AI) 시리즈와도 자연스럽다. "내부 메커니즘 → 실무 시나리오 → 트렌드 → 통합 실전"으로 이어지는 토비식 서술 약속을 제목이 직접 보증한다.

### 후보 B. **Spring Security 7 심층 가이드**
- 부제: *Spring Boot 4와 함께 다시 쓰는 인증·인가의 정석*
- 슬러그: `spring-security-7-deep-guide`
- 한 줄 컨셉: 중립적·교과서적인 레퍼런스 톤. 5.x/6.x 경험자가 7로 점프할 때 곁에 두는 책.
- 추천도: ★★★★ — 검색 친화적이고 안전한 선택이지만 시장에 비슷한 제목이 흔해 차별점이 약하다.

### 후보 C. **다시 쓰는 Spring Security**
- 부제: *7.0 GA 이후, AuthorizationManager·Passkeys·DPoP 시대의 인증·인가 설계*
- 슬러그: `rewriting-spring-security`
- 한 줄 컨셉: "필터 체인부터 다시 짠다"는 메시지를 전면에. 마이그레이션 강조형.
- 추천도: ★★★ — 카피는 강하지만, 초·중급 독자가 "마이그레이션 책"으로만 오해할 위험. 본 책은 마이그레이션 챕터를 포함하되 전반은 심층 레퍼런스이므로 톤이 다소 어긋난다.

**추천: 후보 A — `toby-spring-security-7`**
이유: (1) 본 하네스의 산출 정체성과 일치, (2) "Toby의 ~" 컨벤션이 평어체·청유형 톤을 자연스럽게 정당화, (3) 부제에서 책의 전 범위(아키텍처·Zero Trust·Passkeys·MFA)를 한눈에 약속. 출판/공유 메타데이터에서도 같은 슬러그(`toby-spring-security-7`)로 일관 유지가 가능하다.

---

## 1. 책 특성

- **장르:** 심층 기술 레퍼런스(Deep-dive Reference) — 챕터별 독립 가치가 있고, 통독 시 한 권의 "Spring Security 7 운영 매뉴얼"이 되는 구조. 단순 튜토리얼이 아니다.
- **분량:** 15개 챕터, 본문 470~550페이지(한글 글자 수 기준 약 31만~37만 자, 한 챕터 평균 약 32p). 머리말·맺음말·부록 포함 시 약 500~590페이지.
- **난이도:** 중급~시니어. Spring Boot로 REST API와 폼 로그인을 만들어본 경험이 있고, Spring Security 5.x/6.x를 표면적으로 써본 독자를 가정한다. 자바 17+/21, Spring Boot 4.0 + Spring Security 7.0 GA를 기준으로 한다.
- **독자 여정:**
  - 진입 상태: `SecurityFilterChain` 빈을 만들어 본 적은 있지만 "왜 이렇게 짜야 하는지"는 불분명. JWT를 도입했는데 운영 중 의문점이 쌓여간다. 7.0 마이그레이션 공지를 보고 막막함을 느낀다.
  - 출구 상태: 한 요청이 필터를 통과하는 전체 경로를 머릿속에 그릴 수 있다. 시나리오(폼/Basic/JWT/OAuth2/OIDC/Passkeys/MFA)별로 어느 컴포넌트가 무엇을 하는지 안다. 7.0의 새 모델(`AuthorizationManager`, `AuthorizationManagerFactory`, `@EnableMultiFactorAuthentication`, `csrf(spa)`, DPoP)을 자기 프로젝트에 도입할 수 있다. 인가 결정을 단위/통합 테스트로 안전망에 묶을 수 있다. BFF·Zero Trust 같은 트렌드를 기존 자산과 어떻게 연결할지 판단할 수 있다.
- **차별점(시중 책 대비):**
  1. 7.0 GA(2025-11-17) 기준 첫 한국어 심층 레퍼런스 — 리서치 §3.1 타임라인 인용.
  2. "신모델만" 다루지 않고 5/6→7 마이그레이션 함정을 별도 챕터로 (리서치 §3.3 deprecation 매핑표, §3.4 권고 순서, §7.1 마이그레이션 함정 5건 흡수). 1장에 함정 5건 미리보기 표 + 12장 본편.
  3. Passkeys, One-Time Token, MFA를 7장 "패스워드 너머의 인증"에 1급으로 묶고, DPoP는 5장 JWT 자원 서버 후반에 sender-constrained 토큰의 자연스러운 진화로 배치 — 표면 소개에 그치지 않고 등록/인증 ceremony, 운영 함정, MFA 1급 권한 모델, `cnf.jkt` 검증까지.
  4. Reactive(WebFlux) 보안을 별도 챕터로 (§2.7, §5.5, §8.11 흡수).
  5. **테스팅을 별도 챕터로** — 인가·OAuth2·자원 서버·Reactive 보안 테스트 패턴을 시니어 독자에게 1급으로 약속.
  6. 실무 함정 사례를 챕터 머리에 배치 — 리서치 §7 전체를 챕터별로 매핑.
  7. 최종 챕터에서 SPA + BFF + 자원 서버 + IdP 조합을 처음부터 끝까지 한 시나리오로 통합 — 별도 챕터로 독립.

---

## 2. 내러티브 아크 (15 챕터)

도입(1) → 토대(2~3) → 인증 시나리오(4~7) → 인가(8) → 횡단(9~10) → Reactive(11) → 테스팅(12) → 마이그레이션(13) → 트렌드·운영(14) → 통합 실전(15). 이 흐름은 의도적이다.

**1장(도입)** 은 "왜 지금 다시 보는가"로 시작한다. 7.0 GA가 가져온 변화와 함께, 5.x/6.x 시절 코드가 빨갛게 물드는 첫 빌드의 당혹감을 공감한다. 1장은 추가로 두 개의 좌표를 박는다: **(a) "보안 멘탈 모델 5분"** — OWASP/인증vs인가/세션vs토큰/Zero Trust 한 줄 정의로 책 전체의 어휘 기반을 만든다. **(b) "5/6 코드는 7에서 무엇이 빨갛게 변하는가"** — 마이그레이션 함정 5건 한눈 표를 미리 노출하고 본격 답은 13장 cross-ref. 1장이 책 전체의 좌표축을 책임진다.

**2~3장(토대)** 은 모든 이후 챕터의 어휘를 정립한다. 필터 한 줄의 동작을 끝까지 파고드는 2장과, 인증·인가 컴포넌트 모델을 정리하는 3장. 2장 후반에 "내가 만든 Filter를 끼우는 법"(`addFilterBefore`/`addFilterAfter`) 절을 두어 시니어의 흔한 질문을 같은 자리에서 답한다.

**4~7장(인증 시나리오)** 은 점진적 복잡도다. Form/Basic/Remember-Me(4장) → JWT 자원 서버 + DPoP(5장) → OAuth2 Client + OIDC + PKCE(6장) → Passkeys/OTT/MFA(7장). 매 챕터 끝에 "이 모델은 어떤 위협을 막고 어떤 위협엔 무력한가"를 정리해 다음 챕터가 풀어야 할 문제를 예고한다. DPoP가 5장 후반에 자리 잡음으로써 토큰 보호의 진화(Bearer → sender-constrained)가 한 챕터 안에서 완결된다.

**8장(인가)** 은 URL/Method/Role Hierarchy/`AuthorizationManager` 활용을 중심으로 응축한다. 도메인 객체 ACL은 본문 흐름을 깨지 않도록 **짧은 박스**로 처리해 분량 압박을 덜었다. Error Handling(`AuthenticationEntryPoint`/`AccessDeniedHandler`/ProblemDetail)도 인가 결정의 짝으로 8장 후반에 한 절을 둔다.

**9~10장(횡단)** 은 CSRF·CORS·헤더(9장)와 세션·쿠키·컨텍스트(10장)를 깊이 다룬다. **11장**은 Reactive 보안을 별도로.

**12장(테스팅)** 은 본 책의 새 약속이다. `@WithMockUser`/`SecurityMockMvcRequestPostProcessors`/`oauth2Login()`/`jwt()` mock/Reactive `mutateWith(mockUser())` + 7.0의 testing 변경점. 위치는 Reactive(11장) 직후·마이그레이션(13장) 직전 — 본문 챕터의 인증·인가·Reactive 어휘가 모두 깔린 시점에서 "이 모든 결정을 어떻게 테스트로 묶을 것인가"에 답한다.

**13장(마이그레이션)** 은 5/6→7 전환의 모든 함정을 한곳에 모은다. 1장에서 미리 본 함정 5건의 본편 답이 여기서 펼쳐진다.

**14장(트렌드·운영)** 은 Zero Trust 7 tenets/BFF/Secret 회전/Actuator/관측·감사/논쟁점을 다룬다. DPoP는 5장에서 본격적으로 다뤘으므로 14장에서는 Zero Trust 원칙 4(sender-constrained) 매핑 안에서 한 단락으로만 cross-ref.

**15장(통합 실전)** 은 책의 출구. 모놀리식 + SPA + 자원 서버 + 외부 IdP 조합을 처음부터 끝까지 빌드한다. 14장과 분리됨으로써 "이 책을 덮으면 무엇을 만들 수 있는가"의 답이 단독 챕터로 또렷해진다.

각 챕터는 단독으로도 가치가 있도록 짰다. 시니어 독자는 7장 Passkeys만 펴고 도입 가능하다. 12장 테스팅만 펴서 기존 시스템에 안전망을 추가할 수도 있다. 그러나 처음부터 읽으면 2~3장의 어휘가 이후 모든 챕터의 코드와 다이어그램에 그대로 흘러 일관된 감각을 갖게 된다.

**독자 경로 3종(1장 챕터 의존도 지도에 명시):**
- 경로 1 (통독): 1 → 2 → 3 → ... → 15
- 경로 2 (5/6 마이그레이션 우선): 1 → 13 → 2 → 3 → ... → 15
- 경로 3 (특정 신기능만): 1 → 2 → 3 → 해당 챕터 (+ 12장 테스팅)

---

## 3. 챕터 목록

### 1장. 왜 Spring Security를 다시 봐야 하는가
- **선행 필요:** 없음 (책의 좌표축을 박는 챕터)
- **핵심 질문:** 7.0 GA가 가져온 변화는 무엇이고, 5.x/6.x 코드는 왜 갑자기 빨갛게 물드는가? 그리고 이 책의 어휘로 보안을 어떻게 사고할 것인가?
- **주요 내용:**
  - 2025-11-17 GA, Spring Boot 4.0과 묶임 — 리서치 §3.1 타임라인 인용
  - 5.x 코드 복붙의 함정 — "2019년 Stack Overflow 답변" 인용(리서치 §7.1 함정 1)
  - 7.0의 큰 그림 5가지: `AccessDecisionManager` 분리, Lambda DSL 강제, Authorization Server 흡수, MFA 1급, Passkeys/OTT/DPoP 안정화 (§3.2)
  - **[신설] 보안 멘탈 모델 5분** — OWASP Top 10 2021(A01·A02·A07) / 인증 vs 인가 / 세션 vs 토큰 트레이드오프 / Zero Trust 한 줄 정의. 책 전체 어휘 기반 (§6.1, §6.5)
  - **[신설] 5/6 코드는 7에서 무엇이 빨갛게 변하는가** — 마이그레이션 함정 5건(§7.1) 한눈 표 + 각 함정의 본격 답이 13장 어느 절인지 페이지 cross-ref
  - 책의 사용법 안내(독자 여정, 챕터 의존도 지도, 독자 경로 3종)
  - **[신설] 이 책이 다루지 않는 것** — GraphQL/gRPC 보안, Spring Authorization Server 서버 측 깊은 운영, 모바일 앱 측 보안, MDM, K8s Service Mesh와의 mTLS 통합 (리서치 한계 §11.2/§11.6 인용)
- **독자가 얻는 것:** 책을 끝까지 읽을 이유 + 7.0 시대 보안 설계의 좌표축 + 빨간 줄의 답이 어디 있는지의 지도
- **예상 분량:** 28~32페이지
- **위치/역할:** 정서적·논리적 진입점. 평어체와 청유형 톤을 처음 노출하는 챕터. 책 전체 어휘의 닻.

### 2장. 한 요청이 통과하는 길 — 필터 체인 해부
- **선행 필요:** 1장
- **핵심 질문:** `http://localhost/api/orders` 한 번이 들어왔을 때, Spring Security 안에서 무슨 일이 11번 일어나는가?
- **주요 내용:**
  - `DelegatingFilterProxy` → `FilterChainProxy` → `SecurityFilterChain` 위임 (§2.1)
  - "Only the first SecurityFilterChain that matches is invoked" — 공식 docs 인용
  - 필터 11종 순서와 책임 (§2.2)
  - `ExceptionTranslationFilter` 내부 흐름 — `AuthenticationException`/`AccessDeniedException` 번역 (§2.3)
  - 7.0에서 `FilterSecurityInterceptor` 완전 제거 → `AuthorizationFilter` (단, 이름만 짚고 본격 설명은 3장으로 차단)
  - `HttpFirewall`로 비정상 요청 차단 (§2.1)
  - 두 개의 `SecurityFilterChain`(웹+API 분리) 패턴 미리보기 (§8.2)
  - **[신설] 내가 만든 Filter를 끼우는 법** — `addFilterBefore`/`addFilterAfter`, Order 결정 패턴, 잘못된 위치에 끼웠을 때의 증상 (4~6p)
- **독자가 얻는 것:** 이후 모든 챕터에서 "이 코드는 어느 필터에 꽂히는가"를 자기 손으로 답할 수 있는 머릿속 지도
- **예상 분량:** 38~44페이지
- **위치/역할:** 책의 토대 1. 가장 많은 다이어그램이 들어가는 챕터.

### 3장. 인증과 인가의 컴포넌트 모델
- **선행 필요:** 2장
- **핵심 질문:** `AuthenticationManager`, `AuthorizationManager`, `SecurityContextHolder`는 각각 무엇을 책임지고, 7.0에서 어떻게 바뀌었는가?
- **주요 내용:**
  - `ProviderManager` 위임 모델과 `AuthenticationProvider.supports()` 매칭 (§2.4)
  - `AuthenticationManagerResolver` — 다중 issuer/다중 테넌트 (§2.4)
  - `AuthorizationManager` 신모델 — 7.0에서 `check` 제거, `authorize`만 (§2.5, §3.3)
  - 주요 구현체 5종: `AuthorityAuthorizationManager`, `AuthenticatedAuthorizationManager`, `RequestMatcherDelegatingAuthorizationManager`, **신규** `AllAuthoritiesAuthorizationManager`(AND), `AuthorizationManagerFactory` (§2.5)
  - `AccessDecisionManager`/`Voter`가 `spring-security-access`로 분리됨 (§2.5, §3.3)
  - `SecurityContextHolder` 전략과 위험(`MODE_INHERITABLETHREADLOCAL` + 스레드 풀 → 다른 사용자 컨텍스트 누수, §2.6, §7.3 함정 13)
  - `DelegatingSecurityContextAsyncTaskExecutor` 전파 패턴 (§8.12)
  - Virtual Threads(Java 21+)와 `MODE_THREADLOCAL` (§2.6)
- **독자가 얻는 것:** 모든 인증·인가 동작의 "주어"를 정확히 부를 수 있는 어휘
- **예상 분량:** 34~40페이지
- **위치/역할:** 책의 토대 2. 이후 모든 챕터가 이 어휘로 말한다.

### 4장. 폼 로그인·HTTP Basic·Remember-Me — 세션 기반 인증의 정석
- **선행 필요:** 2장, 3장
- **핵심 질문:** 가장 오래된 인증 방식이 7.0에서 어떻게 살아 있고, 어떤 함정이 여전한가?
- **주요 내용:**
  - Form Login + 세션 풀 시퀀스 (§4.1, §8.1)
  - `PasswordEncoder` 선택: BCrypt/Argon2/PBKDF2 + 7.0 Password4j 5종 신규 인코더 (§3.2)
  - HTTP Basic — `securityContext.requireExplicitSave(true)` + `STATELESS` 조합 (§4.2)
  - Remember-Me — Hash vs Persistent, 모바일/SPA 비추천 이유 (§4.3)
  - Session Fixation 기본 보호 `migrateSession()` (§7.3 함정 12)
  - 정적 자원 ignore: `WebSecurityCustomizer` 패턴 (§7.1 함정 5)
- **독자가 얻는 것:** 7.0 시대에도 유효한 세션 기반 인증의 권장 구성과 함정 회피법
- **예상 분량:** 28~32페이지

### 5장. JWT 자원 서버 — Bearer 토큰의 끝까지, 그리고 sender-constrained로
- **선행 필요:** 2장, 3장
- **핵심 질문:** `issuer-uri` 한 줄이 어떻게 안전한 자원 서버를 만들고, 무엇을 안 막아 주는가? 그리고 토큰 탈취를 어떻게 막을 수 있는가?
- **주요 내용:**
  - 기본 구성 — `oauth2ResourceServer(o -> o.jwt(...))` + `STATELESS` (§4.4, §8.2)
  - `JwtDecoders.fromIssuerLocation`이 하는 일 — OIDC discovery → JWKs 캐시 (§4.4)
  - 7.0 신규: `NimbusJwtDecoder` 커스텀 `JwkSource`, `NimbusJwtEncoder` 빌더 (§3.2)
  - 권한 매핑 — `scope`/`scp` 자동 `SCOPE_*`, 커스텀은 `JwtAuthenticationConverter` (§8.4)
  - Opaque Token + Introspection 캐시 (§4.5)
  - **JWT 함정 4건 별도 절:**
    - JWT를 세션 토큰처럼 쓰는 함정 (§7.2 함정 6)
    - `localStorage` 저장 → XSS 한 번이면 끝 (§7.2 함정 7)
    - `alg: none` / 알고리즘 confusion — RFC 8725 (§7.2 함정 8, §6.3)
    - Refresh Token 회전 미구현 (§7.2 함정 9)
  - RFC 8725 / BCP 225 권장 사항 매핑 (§6.3)
  - **[이동] JWT의 한계와 sender-constrained 토큰: DPoP** — Bearer 토큰의 본질적 한계 → RFC 9449 DPoP → 자원 서버 1급 처리 (§4.9)
    - 액세스 토큰 JWT의 `cnf.jkt` (JWK SHA-256 thumbprint)
    - 매 요청 `DPoP` 헤더(`htm`/`htu`/`iat`/`jti`/`ath`) 검증
    - 토큰 탈취 대응의 표준 구현, 한계와 호환성
- **독자가 얻는 것:** JWT를 자신 있게 도입하고, 어디서 멈춰야 하는지 아는 감각. Bearer에서 sender-constrained로의 진화를 한 챕터에서 본다.
- **예상 분량:** 42~48페이지
- **위치/역할:** 시중에서 가장 많이 쓰지만 가장 위험한 토픽. 가장 두꺼운 시나리오 챕터.

### 6장. OAuth2 Client + OIDC Login — 외부 IdP에 로그인을 위임하다
- **선행 필요:** 2장, 3장, 5장(토큰 어휘)
- **핵심 질문:** Google/Keycloak/Auth0에 로그인을 위임하면서도 사용자의 신원과 권한을 안전하게 받아 오는 방법은?
- **주요 내용:**
  - 기본 흐름 — `/oauth2/authorization/{id}` → IdP → `/login/oauth2/code/{id}` 콜백 (§4.6)
  - `OAuth2LoginAuthenticationFilter` 내부 — code↔token 교환, ID Token 디코드, `OidcUser` 생성 (§4.6)
  - **PKCE** — 7.0부터 confidential client에도 기본 권장 (§4.6, §8.5)
  - 7.0 신규: `@ClientRegistrationId` 타입 레벨, Dynamic Client Registration (§3.2)
  - OAuth2 Support for HTTP Service Clients — `@HttpExchange`에 access token 자동 주입 (§3.2)
  - **함정 3건:** Redirect URI 와일드카드 → open redirect (§7.4 함정 14), confidential client에서 PKCE 누락 (§7.4 함정 15), ID Token으로 API 인가 (§7.4 함정 16)
  - RFC 9700(2025-01)이 요구하는 7가지 규범과 7.0 매핑 (§6.2)
  - OAuth 2.1 draft가 흡수한 변경 (§6.2)
- **독자가 얻는 것:** 외부 IdP 연동의 표준 흐름과 BCP 준수 체크리스트
- **예상 분량:** 32~38페이지

### 7장. Passkeys·One-Time Token·MFA — 패스워드 너머의 인증
- **선행 필요:** 2장, 3장, 4장(세션 어휘)
- **핵심 질문:** 패스워드 없이 또는 패스워드 위에 두 번째 factor를 쌓는 7.0의 1급 모델은 무엇이고, 어떻게 도입하는가?
- **주요 내용:**
  - **One-Time Token(OTT)** — 6.4 도입, 7.0 안정 (§4.7, §8.6)
  - **Passkeys / WebAuthn** (§4.8, §8.7) — 등록/인증 ceremony 3단계 + JDBC 영속화 + 운영 함정
    - W3C WebAuthn Level 3 / FIDO Alliance 표준 매핑 (§6.4)
  - **Multi-Factor Authentication — 7.0 신규 1급 지원** (§4.10, §8.8)
    - factor를 **권한(Authority)** 으로 표현 — `@EnableMultiFactorAuthentication`
    - 선택적 MFA — `AuthorizationManagerFactory.allAuthorities(...)` (**8장에서 자세히 다룰 `AuthorizationManagerFactory`의 미리보기**라고 명시 + 8장에 cross-ref 박스)
    - `factor.type` / `factor.reason` 파라미터
- **독자가 얻는 것:** "패스워드만으로는 부족하다"는 시대에 7.0이 제시하는 표준 솔루션 세 가지를 자기 프로젝트에 도입할 수 있다.
- **예상 분량:** 38~44페이지
- **위치/역할:** 7.0의 가장 큰 신기능 묶음. 책 후반부 가치 정점 중 하나.

### 8장. 권한은 어디에 사는가 — 인가의 5층 구조
- **선행 필요:** 2장, 3장, 4~7장(권한·SCOPE·Authority 생산자)
- **핵심 질문:** 비즈니스 규칙이 인증된 사용자에게 무엇을 허용할지 결정할 때, 코드 어느 층에 그 규칙이 살아야 하는가?
- **주요 내용:**
  - URL 기반 — `authorizeHttpRequests`와 7.0 통일 매처 `PathPatternRequestMatcher` (§5.1, §3.2)
  - `requestMatchers(HttpMethod, path)`, `hasRole`/`hasAuthority`/`hasAnyRole` 의미 차이
  - **Method Security** — `@EnableMethodSecurity`(NOT `@EnableGlobalMethodSecurity`) (§5.2)
  - **함정: `@EnableGlobalMethodSecurity` 잔존 시 `@PreAuthorize` 무력화** (§5.2, §7.1 함정 2)
  - `@PreAuthorize` SpEL + `MethodSecurityExpressionHandler` (§5.2)
  - 메타 어노테이션 패턴(6.3+) (§5.2, §8.10)
  - `MethodAuthorizationDeniedHandler` 커스터마이즈 (§5.2)
  - **Role Hierarchy** — `RoleHierarchyImpl` (§5.4, §8.9)
  - `AuthorizationManagerFactory` 본격 — 7장 MFA에서 미리 본 `allAuthorities`를 다시 (cross-ref)
  - **[박스 축소] 도메인 객체 ACL** — `spring-security-acl` vs `AuthorizationManager` SpEL(`#post.author == authentication.name`) 대안을 짧은 박스로 (§5.3). 본문에 두텁게 풀지 않고 "언제 ACL이 필요해지는가"만.
  - 논쟁점: `@PreAuthorize` SpEL이 비즈니스 로직을 잠식할 위험 (§9)
  - OWASP A01 매핑 — 평균 발견율 3.81% (§6.1)
  - **[신설] 거부를 어떻게 표현할 것인가** — `AuthenticationEntryPoint`/`AccessDeniedHandler` 커스터마이즈 + ProblemDetail(`@ControllerAdvice`) 정합 + 9장 헤더와의 짝 (6~8p)
- **독자가 얻는 것:** URL/메서드/도메인 객체/계층 권한을 한 사고 모델 안에 통합해 결정하고, 거부 응답까지 일관되게 설계할 수 있다.
- **예상 분량:** 36~42페이지
- **위치/역할:** 인증 시나리오 묶음 이후의 자연스러운 다음 단계. 책의 사실상 세 번째 토대.

### 9장. CSRF·CORS·보안 헤더 — 가장 헷갈리는 셋
- **선행 필요:** 2장, 3장, 4장
- **핵심 질문:** 왜 CSRF는 켜고 CORS는 미리 통과시켜야 하며, 헤더 한 줄이 무엇을 바꾸는가?
- **주요 내용:**
  - **CORS는 Security보다 먼저** — preflight 401 함정 (§6.7, §7.3 함정 11)
  - `http.cors(...)` + `CorsConfigurationSource` 빈 패턴
  - **CSRF의 의미** — stateful 쿠키 흐름 필수 (§6.7)
  - 7.0 신규 단축: `http.csrf(CsrfConfigurer::spa)` (§3.2, §6.7, §8.3)
  - **함정: "API니까 CSRF disable" 후 form login 깨짐** (§7.3 함정 10, §8.2)
  - **헤더 작성** — HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy, CSP (§2.2, §6.7)
  - HSTS dev 환경 주의
  - CSP — 헤더 작성만 도와줌, 정책은 앱이 결정
  - **[신설] HTTPS/TLS 운영 맥락** — 역프록시 뒤에서 `X-Forwarded-Proto` 처리, `LoginUrlAuthenticationEntryPoint`의 상대 경로 리다이렉트 (3~4p)
- **독자가 얻는 것:** "CORS preflight 401"이 떴을 때 한 번에 원인을 짚는 직관
- **예상 분량:** 26~30페이지

### 10장. 세션·쿠키·컨텍스트 전파 — 상태 관리의 모든 모서리
- **선행 필요:** 2장, 3장, 4장
- **핵심 질문:** 세션이 있을 때와 없을 때의 코드가 어떻게 갈리며, 비동기 컨텍스트는 어디서 새는가?
- **주요 내용:**
  - `sessionCreationPolicy`: `ALWAYS` / `IF_REQUIRED` / `NEVER` / `STATELESS`
  - `HttpSessionSecurityContextRepository` 동작 (§4.1)
  - `securityContext().requireExplicitSave(true)` — 7.0 권고 기본 (§4.2)
  - Session Fixation 보호 모드 (§7.3 함정 12)
  - 동시 세션 제어 — `maximumSessions(1)`
  - 쿠키 속성 — `HttpOnly`/`Secure`/`SameSite` (§7.2 함정 7, §6.6 BFF)
  - **컨텍스트 전파:** `MODE_INHERITABLETHREADLOCAL` + 스레드 풀 위험 (§2.6, §7.3 함정 13)
  - `DelegatingSecurityContextRunnable/Callable/AsyncTaskExecutor` (§8.12)
  - `@Async`와 `SecurityContext` 전파 베스트프랙티스
  - Reactive로의 다리: `ReactiveSecurityContextHolder` 미리보기 — 11장 예고
- **독자가 얻는 것:** stateful·stateless 경계에서 일어나는 미묘한 누수와 보호 동작을 모두 이해한다.
- **예상 분량:** 26~30페이지

### 11장. Reactive 보안 — WebFlux에서 다시 그리는 인증·인가
- **선행 필요:** 2장, 3장, 5장(또는 8장의 인가 어휘)
- **핵심 질문:** 블로킹 세계의 `HttpSecurity`/`SecurityFilterChain`이 WebFlux에서 어떻게 변형되는가?
- **주요 내용:**
  - `ServerHttpSecurity`/`SecurityWebFilterChain` 대응 매핑 (§2.7)
  - 진입점 `AuthenticationWebFilter`, `ReactiveAuthenticationManager`, `ServerSecurityContextRepository` (§2.7)
  - 블로킹 API 금지 — `SecurityContextHolder` ❌, `ReactiveSecurityContextHolder.getContext()` ✅ (§2.7)
  - WebFlux 자원 서버 — `ReactiveJwtDecoders.fromIssuerLocation` (§4.4, §8.11)
  - 인가 — `authorizeExchange` (§5.5)
  - Reactive Method Security — `@EnableReactiveMethodSecurity` (§5.5)
  - 7.0 신규: `AllAuthoritiesReactiveAuthorizationManager`(AND) (§3.2)
  - Reactive와 컨텍스트 전파 — Reactor Context 전달
- **독자가 얻는 것:** WebFlux 프로젝트에서 서블릿 책 지식을 그대로 옮겨 적용할 수 있다.
- **예상 분량:** 26~30페이지

### 12장. Spring Security 테스팅 — `@WithMockUser`부터 OAuth2 mock까지
- **선행 필요:** 2장, 3장, 5장, 8장(인가), 11장(Reactive 보안 테스트 절을 위해)
- **핵심 질문:** 인증·인가 결정과 토큰 검증, 그리고 Reactive 보안을 어떻게 단위/통합 테스트의 안전망에 묶을 것인가?
- **주요 내용:**
  - 테스트 의존성 — `spring-security-test`의 자리
  - `@WithMockUser`/`@WithUserDetails`/`@WithSecurityContext` — 의미 차이와 함정
  - `SecurityMockMvcRequestPostProcessors` — `csrf()`/`user(...)`/`httpBasic(...)`/`anonymous()`
  - OAuth2 클라이언트 mock — `oauth2Login()`/`oidcLogin()` post processor
  - 자원 서버 mock — `jwt()`/`opaqueToken()` post processor, 권한 자동 매핑
  - **MockMvc 통합 테스트 패턴** — `@SpringBootTest` + `@AutoConfigureMockMvc(addFilters=true)` vs `@WebMvcTest`의 보안 적용 차이
  - **WebTestClient + Reactive 보안** — `mutateWith(SecurityMockServerConfigurers.mockUser(...))`, `mockJwt()`, `mockOAuth2Login()`
  - Method Security 테스트 — `@PreAuthorize` 단위 테스트의 ApplicationContext 의존
  - CSRF/CORS/Header 검증 패턴 — 9장 결정의 회귀 테스트
  - 7.0의 testing 변경점 — Lambda DSL 강제와 함께 바뀐 시그니처, `requireExplicitSave` 환경에서의 컨텍스트 저장 검증
  - 통합 시나리오 — Form Login + Remember-Me + Session Fixation 동작을 한 테스트로
- **독자가 얻는 것:** 이 책 전체에서 내린 보안 결정들을 회귀 가능한 테스트로 묶는 패턴 세트
- **예상 분량:** 22~26페이지
- **위치/역할:** 본문 챕터의 어휘가 모두 깔린 시점에서 안전망을 제시. 시니어 독자에게 가장 자주 인용될 챕터로 의도.

### 13장. 5/6에서 7로 — 마이그레이션 실전 가이드
- **선행 필요:** 2장, 3장 (전체 통독자) 또는 1장만 (마이그레이션 우선 독자)
- **핵심 질문:** 운영 중인 5.x/6.x 코드베이스를 7.0으로 옮기는 안전한 순서는?
- **주요 내용:**
  - 공식 권고 순서: 6.5 patch → preparation step → 7.0 점프 (§3.4)
  - **deprecation → 제거 매핑표** — `WebSecurityConfigurerAdapter`, `antMatchers`/`mvcMatchers`, `authorizeRequests`, `.and()`, `apply(...)`, `AccessDecisionManager`/`Voter`, `AuthorizationManager#check`, `AntPathRequestMatcher`, OAuth2 Password Grant, OpenSAML 4, Jackson 2 (§3.3)
  - Jackson 3 전환 — `SecurityJackson2Modules` → `SecurityJacksonModules` (§3.2)
  - 매처 일괄 전환 → `PathPatternRequestMatcher` (§3.2, §7.1 함정 4)
  - Lambda DSL 강제 (§3.2, §7.7)
  - **함정 5개 정리:** SO 2019 복붙, `@EnableGlobalMethodSecurity` 잔존, `.and()`, mvc/ant 혼합, `WebSecurityCustomizer` 누락 (§7.1) — 1장 미리보기 표의 본격 답
  - **자동화:** OpenRewrite `rewrite-spring` 레시피 — 6.4/6.5 deprecation 자동 치환 (§3.4)
  - CI에서 deprecation warning 0 만들기 체크리스트
  - SAML — OpenSAML 5 의존성, `AssertingPartyMetadata` API (§3.2)
  - LDAP — UnboundID 통일, ApacheDS 제거 (§3.2, §4.12)
  - Spring Authorization Server 흡수 — 패키지 이동 처리 (§3.2)
- **독자가 얻는 것:** 운영 코드베이스를 깨지 않고 7.0으로 옮기는 실행 가능한 단계와 체크리스트
- **예상 분량:** 32~38페이지

### 14장. Zero Trust·BFF·운영의 모서리 — 트렌드와 표준
- **선행 필요:** 1장(멘탈 모델), 5장(JWT/DPoP), 6장(OAuth2), 8장(인가), 9·10장(횡단)
- **핵심 질문:** Spring Security 7로 만든 시스템이 Zero Trust 원칙·BFF 패턴 시대에 어떻게 위치하며, 운영의 모서리는 어디인가?
- **주요 내용:**
  - **NIST SP 800-207 Zero Trust 7 tenets** — Spring Security 매핑 (§6.5): stateless JWT + 매 요청 인가(원칙 6) + sender-constrained 토큰(원칙 4, **5장 DPoP cross-ref 한 단락**) + MFA + 세션 단위 권한(원칙 3)
  - **BFF (Backend-for-Frontend) 패턴** — SPA + OAuth2 표준 모범 (§6.6)
    - 브라우저는 OAuth 클라이언트가 아니다. HttpOnly 세션 쿠키만
    - Spring Cloud Gateway + `oauth2Login`으로 confidential client
    - 7.0 `http.csrf(CsrfConfigurer::spa)` 한 줄이 BFF를 단순화 (issue #14149)
  - **Secret 회전·키 관리** (§6.8): JWK rotation, `NimbusJwtDecoder` + `JwkSourceBuilder`, BCrypt 12 → Argon2id, Vault
  - **Actuator 안전 운영** — `env`/`heapdump`/`configprops` 노출 사고(우아한형제들 사례 §7.5)
  - **관측·감사** — 인증 이벤트, `AuthenticationSuccessEvent`/`AuthenticationFailureEvent`, audit log 패턴
  - **논쟁점 정리** — JWT vs Session, Authorization Server 직접 운영 vs 외부 IdP, localStorage vs Cookie (§9)
  - K8s Service Mesh / mTLS 와의 관계 — 한 단락 트렌드 박스(본 책 범위 밖이지만 좌표만)
- **독자가 얻는 것:** 1장에서 박은 좌표(Zero Trust/OWASP) 위에 Spring Security 7 결정들이 어떻게 얹히는지의 그림 + 운영의 흔한 빈틈 체크리스트
- **예상 분량:** 32~38페이지

### 15장. 한 권을 한 시나리오로 — 통합 실전 워크스루
- **선행 필요:** 1~14장 (책의 출구 챕터)
- **핵심 질문:** 이 책의 모든 결정을 한 프로젝트에 어떻게 합쳐 빌드하는가?
- **주요 내용:**
  - 모놀리식 백엔드(Spring Boot 4) + SPA(React/Vue) + 외부 IdP(Keycloak) + BFF(Spring Cloud Gateway)
  - 두 개의 `SecurityFilterChain` — 웹용 stateful, API용 stateless (§8.2)
  - OAuth2 Login + PKCE + 패스워드 + OTT MFA
  - JWT 자원 서버 + DPoP(5장 결정 적용)
  - CSRF(SPA 모드)·CORS·CSP·HSTS·세션 정책
  - 12장 테스팅 패턴으로 회귀 안전망 — 핵심 인가 시나리오 5개를 통합 테스트로
  - 운영 체크리스트: 인증 이벤트 audit, JWK 회전 schedule, 모니터링 대시보드, deprecation warning 0
  - **마지막 절: 이 책을 덮은 뒤** — 어디서 더 읽을지(공식 docs·RFC·Curity 시리즈), 7.1.x milestone 추적법
- **독자가 얻는 것:** 책 전체 지식을 한 프로젝트로 통합해 본 경험. "이 책을 덮으면 무엇을 만들 수 있는가"의 구체적 증명.
- **예상 분량:** 28~34페이지
- **위치/역할:** 책의 클로징. 단독 통합 실전 챕터로 분리되어 약속이 또렷해진다.

---

## 4. 챕터별 분량·역할 요약

| 장 | 제목(축약) | 분량(p) | 묶음 |
|----|-----------|---------|------|
| 1  | 왜 다시 봐야 하는가 (+멘탈 모델/함정 미리보기/범위 밖) | 28~32 | 도입 |
| 2  | 필터 체인 해부 (+커스텀 Filter) | 38~44 | 토대 |
| 3  | 컴포넌트 모델 | 34~40 | 토대 |
| 4  | 폼/Basic/Remember-Me | 28~32 | 인증 시나리오 |
| 5  | JWT 자원 서버 + DPoP | 42~48 | 인증 시나리오 |
| 6  | OAuth2 Client + OIDC | 32~38 | 인증 시나리오 |
| 7  | Passkeys/OTT/MFA | 38~44 | 인증 시나리오 |
| 8  | 인가의 5층 구조 (+Error Handling, ACL 박스) | 36~42 | 인가 |
| 9  | CSRF·CORS·헤더 (+HTTPS/TLS 운영) | 26~30 | 횡단 |
| 10 | 세션·쿠키·컨텍스트 | 26~30 | 횡단 |
| 11 | Reactive 보안 | 26~30 | 횡단 |
| 12 | **테스팅** | 22~26 | 테스팅 (신설) |
| 13 | 5/6 → 7 마이그레이션 | 32~38 | 마이그레이션 |
| 14 | Zero Trust·BFF·운영 | 32~38 | 트렌드·운영 |
| 15 | 통합 실전 워크스루 | 28~34 | 클로징 (분할) |
| 합계 | 15개 챕터 | **470~546p** (본문) | |

부록(머리말 5p + 맺음말 5p + 참고문헌 10p + 색인 15p) 포함 시 총 **약 505~580페이지**.

---

## 5. 리서치 매핑 (갱신)

- **§1 개념** → 1장 도입 어휘 + 1장 "보안 멘탈 모델 5분"
- **§2 내부 아키텍처** → 2장(필터), 3장(컴포넌트), 10장(`SecurityContextHolder`), 11장(Reactive)
- **§3 변경점·deprecation** → 1장 큰 그림 + 1장 함정 5건 미리보기, 13장 마이그레이션 전 페이지
- **§4 인증 시나리오** → 4·5·6·7장, 5장에 §4.9 DPoP 흡수
- **§5 인가 모델** → 8장 전체, 11장 Reactive 부분
- **§6 표준·트렌드** → 1장(§6.1 OWASP, §6.5 Zero Trust 좌표), 5장(§6.3 RFC 8725), 6장(§6.2 RFC 9700), 9장(§6.7 CORS/CSRF/Headers + HTTPS), 14장(§6.5 NIST/Zero Trust, §6.6 BFF, §6.8 Secret 회전)
- **§7 실무 함정** → 1장(함정 5건 미리보기 표) + 각 시나리오 챕터 머리(분산) + 13장(마이그레이션 함정 종합) + 14장(Actuator §7.5)
- **§8 코드 패턴** → 각 챕터 예제로 흡수, 12장 테스팅 패턴은 별도
- **§9 논쟁점** → 5·8장 끝의 "관점들" 박스 + 14장 논쟁점 정리 절
- **§11 리서치 한계** → 1장 "이 책이 다루지 않는 것" 절 + 7.1.x milestone API 변동 가능성 경고

리서치의 **공식·RFC·NIST** 출처는 본문 인용으로 직접 노출하고, **검증된 저자 블로그(Baeldung·Auth0·Curity·Dimitri)** 는 추가 자료 박스로, **velog/medium** 일반 글은 시행착오 사례 인용 용도로 등급화해 사용한다.

---

## 6. 톤·집필 원칙 메모

- 평어체 기반(`-다`/`-한다`). 새 개념 도입·전환에는 청유형(`-자`/`-보자`) 적극 사용.
- 챕터 머리에 "이런 상황을 가정해보자" 한 단락으로 독자 정서적 진입.
- "왜 그럴까?" → 답을 펴는 문답식 전개.
- 함정·실수 코드는 단순히 "틀렸다"가 아니라 "난감하다", "찜찜하다"로 감정 공감.
- 매 챕터 끝에 핵심 5줄 요약 + "다음 챕터에서 답할 것" 한 줄.
- 다이어그램은 2장(필터 순서)·3장(컴포넌트 위임)·5장(JWT/DPoP 검증)·6장(OAuth2 시퀀스)·7장(WebAuthn ceremony)·14장(BFF 아키텍처)·15장(통합 시나리오)에 집중 배치.
- 챕터별 "선행 필요" 한 줄을 본문 머리에도 동일하게 노출 — 독자가 어디부터 펴도 안심하게.

---

## 7. 리뷰 1차 반영 내역

### 필수 5건 (모두 반영)

1. **13장 분할 →** 트렌드(14장 "Zero Trust·BFF·운영의 모서리", 32~38p) + 통합 실전(15장 "한 권을 한 시나리오로", 28~34p)로 두 챕터로 나눔. 운영(키 회전·Actuator·관측·감사·논쟁점)은 14장 후반 절들로 흡수. DPoP는 5장으로 이동했으므로 14장에서는 Zero Trust 원칙 4 매핑 안의 한 단락 cross-ref로 압축.
2. **테스팅 신설 →** 12장으로 새 챕터 신설(22~26p). 위치는 Reactive(11장) 직후·마이그레이션(13장) 직전 — 본문 어휘가 모두 깔린 시점. `@WithMockUser`/`SecurityMockMvcRequestPostProcessors`/`oauth2Login()`/`jwt()` mock/`WebTestClient` `mutateWith` + 7.0 testing 변경점 포함.
3. **1장 "5/6 코드는 7에서 무엇이 빨갛게 변하는가" 절 추가 →** 함정 5건 한눈 표 + 13장 cross-ref. 챕터 의존도 지도에 "마이그레이션 우선 독자 경로(1→13→2→3→...)"도 함께 명시.
4. **1장 "보안 멘탈 모델 5분" 절 신설 →** OWASP A01·A02·A07 / 인증 vs 인가 / 세션 vs 토큰 / Zero Trust 한 줄 정의. 책 전체 어휘 기반. 1장 분량 22~26p → 28~32p로 늘어남.
5. **DPoP를 5장으로 이동 →** 5장 후반에 "JWT의 한계와 sender-constrained 토큰: DPoP" 절로. 5장 분량 36~42p → 42~48p. 14장에는 Zero Trust 원칙 4 매핑 안에서 한 단락 cross-ref만.

### 권고 4건 (모두 반영)

- **선행 지식 의존도 명시 →** 모든 챕터에 "선행 필요: N장, M장" 한 줄 추가. 7장 MFA 절에 "8장에서 자세히 다룰 `AuthorizationManagerFactory`의 미리보기" 명시 + 8장에 역방향 cross-ref 박스.
- **8장 응축 우려 →** 8장 분량을 34~40p → 36~42p로 늘리고, 도메인 객체 ACL은 본문 절이 아닌 **짧은 박스**로 축소. URL/Method/Role/Error Handling을 본문 흐름의 중심으로.
- **커스텀 Filter 추가 →** 2장 후반에 "내가 만든 Filter를 끼우는 법"(`addFilterBefore`/`addFilterAfter` + Order 패턴, 4~6p) 절 신설.
- **Error handling →** 8장 후반에 "거부를 어떻게 표현할 것인가" 절(`AuthenticationEntryPoint`/`AccessDeniedHandler` + ProblemDetail, 6~8p) 신설. 9장 헤더와의 짝으로 연결.

### 선택 2건 (모두 반영)

- **8장 제목 질문화 →** "인가의 모든 것 — URL·Method·Role Hierarchy·도메인 객체" → **"권한은 어디에 사는가 — 인가의 5층 구조"** 로 변경.
- **"이 책이 다루지 않는 것" 단락 →** 1장 끝에 신설 — GraphQL/gRPC 보안, Spring Authorization Server 서버 측 깊은 운영, 모바일 앱 측 보안, MDM, K8s Service Mesh와의 mTLS 통합은 본 책 범위 밖. 리서치 한계 §11.2/§11.6 인용.

### 부수 정합 변경

- 차별점 3번 문구를 "Passkeys/OTT/MFA를 7장에 1급으로 묶고, DPoP는 5장 JWT 자원 서버 후반에 sender-constrained 토큰의 자연스러운 진화로 배치"로 정직하게 수정.
- 차별점에 5번 "테스팅 별도 챕터" 항목 추가, 기존 5·6번을 6·7번으로 밀어냄.
- 9장에 HTTPS/TLS 운영 맥락(역프록시·`X-Forwarded-Proto`·`LoginUrlAuthenticationEntryPoint` 상대 경로) 짧은 절 추가 (3~4p).
- 1장 챕터 의존도 지도에 독자 경로 3종 명시.

상세 변경 이유와 의사결정 흐름은 `03_review_log.md`에 append됨.
