# Spring Security 7 심층 활용 — 레퍼런스

> 본 문서는 책 저술가가 곧장 활용할 단일 reference다. Spring Security 7.0 GA(2025-11-17) 시점의 공식 문서·공식 블로그·표준(RFC/W3C/NIST)·커뮤니티·기술 블로그를 종합했다.
> 출처 태그: [W]=웹/공식문서·블로그, [S]=표준/RFC/스펙, [C]=커뮤니티/한국 기술블로그·velog.
> 분량 목표 7,000~12,000 단어. 코드 스니펫은 Spring Boot 4.0 / Spring Security 7.0.x 기준 (불확실 영역은 명시).

---

## § 0. 리서치 브리프

- **주제:** Spring Security 7 심층 활용 (Spring Boot 4 기반)
- **독자:** Spring/Spring Boot에 익숙한 중급~시니어. Spring Security 5.x/6.x를 표면적으로만 써본 개발자
- **포지셔닝:** 5/6에서 7로의 변화를 다루되, 책의 뼈대는 "내부 아키텍처 + 시나리오별 활용"이며 7의 신기능은 그 위에 얹는다
- **권위 비중:** 공식 문서(docs.spring.io) > Spring 공식 블로그 > 표준(RFC/W3C) > 검증된 저자 블로그(Baeldung, Vlad, Marco Behler, dimitri.codes, Dan Vega) > 일반 블로그·velog

---

## § 1. 개념·정의

### 1.1 보안 기본 용어

- **인증(Authentication):** 요청자가 누구인지 확인하는 과정. 결과물은 `Authentication` 객체(주체+크리덴셜+권한). [C]
- **인가(Authorization):** 인증된 주체가 특정 리소스에 접근할 자격이 있는지 결정하는 과정. 인증 필터가 인가 필터보다 앞에 오기 때문에, 인증을 통과한 요청만 인가 단계에 진입한다. [C](https://velog.io/@on5949/SpringSecurity-%EC%8A%A4%ED%94%84%EB%A7%81-%EC%8B%9C%ED%81%90%EB%A6%AC%ED%8B%B0-%ED%95%84%ED%84%B0-%EC%B2%B4%EC%9D%B8-%EC%8B%AC%ED%99%94)
- **세션 기반 vs 토큰 기반:** 세션은 서버가 식별자만 쿠키로 발급하고 상태를 서버가 보관(stateful). 토큰(JWT 등)은 토큰 자체에 클레임을 담아 서버 상태 없이 검증 가능(stateless). [W](https://dzone.com/articles/stop-using-jwts-as-session-tokens)
- **OAuth2:** "권한 위임" 프로토콜. 사용자가 자기 자원에 대한 제한된 접근권을 제3자 클라이언트에게 위임. 인증 자체가 아닌 인가 위임 프레임워크. [S](https://datatracker.ietf.org/doc/rfc9700/)
- **OIDC(OpenID Connect):** OAuth2 위의 신원 계층. ID Token(JWT) + UserInfo Endpoint로 "누구"인지를 표준화. [W](https://developer.okta.com/blog/2020/01/23/pkce-oauth2-spring-boot)
- **Passkey:** WebAuthn 위에서 정의되는 사용자 친화 표현. 디바이스/플랫폼/클라우드 동기화 가능한 공개키 자격증명. [S](https://www.w3.org/TR/webauthn-3/) / [W](https://docs.spring.io/spring-security/reference/servlet/authentication/passkeys.html)
- **Zero Trust:** "네트워크 위치만으로 신뢰를 부여하지 않는다"는 패러다임. NIST SP 800-207의 7 tenets로 정의. [S](https://csrc.nist.gov/pubs/sp/800/207/final)

### 1.2 Spring Security 핵심 객체 모델

| 객체 | 책임 |
|------|------|
| `SecurityContextHolder` | 현재 스레드의 `SecurityContext` 보관 (전략 패턴) |
| `SecurityContext` | `Authentication` 한 개를 담는 컨테이너 |
| `Authentication` | 주체(`principal`), 크리덴셜, `GrantedAuthority` 리스트, 인증 여부 |
| `GrantedAuthority` | `getAuthority()` 한 메서드. 기본 prefix `ROLE_` |
| `AuthenticationManager` | 인증 요청 처리 진입점 (보통 `ProviderManager`) |
| `AuthenticationProvider` | 실제 검증 로직 (UserDetails 기반/JWT 기반/LDAP 등) |
| `AuthorizationManager<T>` | 인가 결정. `AuthorizationResult authorize(Supplier<Authentication>, T)` |
| `SecurityFilterChain` | 매칭된 요청에 대해 실행될 필터 리스트 묶음 |

출처: [W](https://docs.spring.io/spring-security/reference/servlet/architecture.html), [W](https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html)

### 1.3 Spring Security 7의 한 줄 요약

> 7.0의 변화는 (1) **레거시 DSL/Matcher 제거**, (2) **`AuthorizationManager`로의 완전 이주**, (3) **Passkeys/OTT/MFA 같은 모던 인증의 1급 시민화**, (4) **Spring Authorization Server·Kerberos 통합**, (5) **Jackson 3·Spring Boot 4 노선 합류**. — `What's New in Spring Security 7.0` [W](https://docs.spring.io/spring-security/reference/whats-new.html)

---

## § 2. Spring Security 내부 아키텍처

### 2.1 요청이 통과하는 길

서블릿 컨테이너 입장에서 Spring Security는 한 개의 `Filter`다. 정확히는 `DelegatingFilterProxy`다. 컨테이너가 등록하는 필터는 빈 라이프사이클을 모르지만, `DelegatingFilterProxy`는 ApplicationContext에서 `springSecurityFilterChain` 이름의 빈을 lazy lookup해서 위임한다.

> "Spring provides a `Filter` implementation named `DelegatingFilterProxy` that allows bridging between the Servlet container's lifecycle and Spring's `ApplicationContext`." — Spring docs [W](https://docs.spring.io/spring-security/reference/servlet/architecture.html)

그 빈이 `FilterChainProxy`다. `FilterChainProxy`는 여러 개의 `SecurityFilterChain`을 갖고, 들어온 요청에 대해 **가장 먼저 매칭되는 하나**만 실행한다. 매칭은 단순 URL이 아니라 `RequestMatcher`로 판단되기 때문에 헤더·메서드·호스트 같은 조건도 가능하다.

> "Only the first `SecurityFilterChain` that matches is invoked." — Spring docs [W](https://docs.spring.io/spring-security/reference/servlet/architecture.html)

`FilterChainProxy`는 매 호출 끝에 `SecurityContext`를 비워서 스레드 풀로 인한 컨텍스트 누수를 막고, `HttpFirewall`을 통해 비정상 요청(이중 슬래시, 인코딩 우회)을 차단한다.

### 2.2 필터 순서 (개념적)

기본 구성에서 한 체인 내 필터 순서(요약):

1. `DisableEncodeUrlFilter`, `WebAsyncManagerIntegrationFilter`
2. `SecurityContextHolderFilter` — 세션/요청에서 SecurityContext 로드
3. `HeaderWriterFilter` — 보안 헤더(HSTS, X-Frame-Options, CSP) 작성
4. `CorsFilter` — CORS 처리 (Security가 처리하기 **이전**에 실행되도록 배치하는 게 핵심)
5. `CsrfFilter`
6. `LogoutFilter`
7. 인증 필터들: `UsernamePasswordAuthenticationFilter`, `OAuth2LoginAuthenticationFilter`, `BearerTokenAuthenticationFilter`, `OneTimeTokenAuthenticationFilter`(7), `WebAuthnAuthenticationFilter`(7) 등
8. `RequestCacheAwareFilter`, `SecurityContextHolderAwareRequestFilter`
9. `AnonymousAuthenticationFilter`
10. `ExceptionTranslationFilter`
11. `AuthorizationFilter` (이전 세대의 `FilterSecurityInterceptor`를 7에서 완전히 대체)

[W](https://docs.spring.io/spring-security/reference/servlet/architecture.html)

### 2.3 `ExceptionTranslationFilter`의 흐름

```
try {
    chain.doFilter(req, res);
} catch (AuthenticationException ae) {
    // 인증이 아예 안 됐거나 끊김 → AuthenticationEntryPoint 호출 (로그인 화면 리다이렉트 / 401)
} catch (AccessDeniedException ade) {
    if (anonymous) startAuthentication(); else accessDenied(); // 403
}
```

이 필터 덕분에 인증/인가 실패가 비즈니스 코드에서 흘러 나와도 일관된 HTTP 응답으로 번역된다. [W](https://docs.spring.io/spring-security/reference/servlet/architecture.html)

### 2.4 인증 컴포넌트 위임 모델

```
[Auth Filter]
   └─ AuthenticationManager (=ProviderManager)
           ├─ DaoAuthenticationProvider (UserDetailsService 사용)
           ├─ JwtAuthenticationProvider
           ├─ OAuth2LoginAuthenticationProvider
           └─ ... 등록된 모든 Provider 순회 → 첫 supports() match
```

`ProviderManager`는 다양한 `AuthenticationProvider`를 순회하면서 자신이 처리할 수 있는 토큰을 만나는 첫 provider에게 위임한다. `AuthenticationManagerResolver`는 요청별로 다른 manager를 골라줄 때 쓴다(다중 테넌트, 다중 issuer 자원 서버에서 유용). [W](https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html)

### 2.5 인가 컴포넌트: `AuthorizationManager` 신모델

7.0에서 레거시 `AccessDecisionManager` / `AccessDecisionVoter` API는 **별도 모듈 `spring-security-access`로 격리**됐다. 기본 의존성에 더이상 포함되지 않는다. [W](https://docs.spring.io/spring-security/reference/whats-new.html)

```java
@FunctionalInterface
public interface AuthorizationManager<T> {
    AuthorizationResult authorize(Supplier<Authentication> auth, T object);
    default void verify(Supplier<Authentication> auth, T object) {...}
}
```

주요 구현체:

- `AuthorityAuthorizationManager` — 특정 권한 보유 여부
- `AuthenticatedAuthorizationManager` — anonymous / remember-me / fully-authenticated 구분
- `RequestMatcherDelegatingAuthorizationManager` — URL 매칭별 위임 (URL 인가의 엔진)
- **신규 7.0**: `AllAuthoritiesAuthorizationManager` — **AND** 조건. 권한을 모두 가져야 통과 (기존 `hasAnyRole`이 OR였던 것과 대비)
- **신규 7.0**: `AuthorizationManagerFactory` — 팩토리 추상화. `permitAll()`/`hasRole()`/`hasAnyRole()` 같은 빌더를 한 곳에서 커스터마이즈 가능. 기본 prefix·trustResolver·roleHierarchy 주입.

[W](https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html)

### 2.6 `SecurityContextHolder` 전략과 스레드

기본은 `MODE_THREADLOCAL`. 비동기·자식 스레드로 컨텍스트가 흘러야 하면 `MODE_INHERITABLETHREADLOCAL`. 그러나 **스레드 풀과 함께 쓰면 위험**하다.

> "When Spring Async annotation is used with `MODE_INHERITABLETHREADLOCAL`, with thread pools this is dangerous because when a thread is reused from a pool, the security context which was set for the thread when it was created is reused, leading to an issue where a task relies on a completely wrong, some other user's security context." — [W](https://github.com/spring-projects/spring-security/issues/6856)

권장 패턴:

- 풀 스레드: `DelegatingSecurityContextRunnable`/`Callable`, `DelegatingSecurityContextAsyncTaskExecutor`로 명시 전파
- Virtual Threads (Java 21+): 스레드가 task 단위로 새로 만들어지므로 `MODE_THREADLOCAL`로도 안전. 단, "carrier thread pinning 회피"는 별개 이슈. (자세한 가이드는 Spring 공식 문서에 아직 빈약 — 책에서 별도 박스로 다루기 권장)

### 2.7 Reactive Security 내부

서블릿 세계의 `HttpSecurity`/`SecurityFilterChain`은 WebFlux에서 각각 `ServerHttpSecurity`/`SecurityWebFilterChain`으로 대응된다. 진입점은 `AuthenticationWebFilter`, 인증 매니저는 `ReactiveAuthenticationManager`, 컨텍스트 저장은 `ServerSecurityContextRepository`.

```java
@Bean
SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
    return http
        .authorizeExchange(ex -> ex.anyExchange().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}
```

블로킹 API(`SecurityContextHolder`)는 reactive 흐름에서 쓰지 말 것 — `ReactiveSecurityContextHolder.getContext()`로 대신. [W](https://docs.spring.io/spring-security/reference/reactive/configuration/webflux.html)

---

## § 3. Spring Security 7 변경점 상세

### 3.1 릴리스 타임라인 (확정 사실)

- **2025-07-21** 7.0.0-M1 [W](https://spring.io/blog/2025/07/21/spring-security-7-0-0-M1-available-now/)
- **2025-08-18** 7.0.0-M2 [W](https://spring.io/blog/2025/08/18/spring-security-7-0-0-M2-available-now/)
- **2025-11-17** 7.0.0 **GA** (with 6.5.7 / 6.4.13) [W](https://spring.io/blog/2025/11/17/spring-security-releases/)
- **2026-01-19** 7.1.0-M1
- **2026-02-13** 6.5.8 / 7.0.3 / 7.1.0-M2

Spring Boot 4.0이 동시에 출시되며 Spring Security 7.0을 기본으로 묶는다. [W](https://www.infoq.com/news/2025/11/spring-7-spring-boot-4/)

### 3.2 What's New — 영역별 전체 정리

다음 목록은 공식 `whats-new.html` 페이지 [W](https://docs.spring.io/spring-security/reference/whats-new.html)를 정리한 것이다.

**Modules**
- Spring Authorization Server가 Spring Security 산하로 흡수 (`spring-security-oauth2-authorization-server:7.0.0`, 패키지/메이븐 좌표는 거의 그대로) [W](https://spring.io/blog/2025/09/11/spring-authorization-server-moving-to-spring-security-7-0/)
- Spring Security Kerberos Extension도 본체로 흡수

**Core / Authorization**
- `AuthorizationManager#check` 제거. `authorize`만 남음 (5.5 이후 deprecated였음)
- Access API(`AccessDecisionManager`, `AccessDecisionVoter`)는 `spring-security-access` 별도 모듈로 분리
- `AllAuthoritiesAuthorizationManager` / `AllAuthoritiesReactiveAuthorizationManager` 추가 (AND 의미 매니저)
- `AuthorizationManagerFactory` 추가
- **신규: Multi-Factor Authentication 1급 지원** — `@EnableMultiFactorAuthentication(authorities = { PASSWORD_AUTHORITY, OTT_AUTHORITY })` 으로 "두 가지 factor 누적"을 권한 누적 모델로 표현. 미완 factor가 있으면 자동 redirect. [W](https://spring.io/blog/2025/10/21/multi-factor-authentication-in-spring-security-7/)
- `Authentication.Builder` — 기존 Authentication을 변형/머지

**Configuration / DSL**
- `HttpSecurity.and()` **삭제**. Lambda DSL이 강제. — `http.authorizeHttpRequests(...).csrf(...).oauth2Login(...)` 같이 람다로 연결
- `authorizeRequests` **삭제**, `authorizeHttpRequests`만 남음
- SPA용 CSRF 단축: `http.csrf(CsrfConfigurer::spa)` — `CookieCsrfTokenRepository.withHttpOnlyFalse()` + `SpaCsrfTokenRequestHandler`를 한 번에 적용 [W](https://dimitri.codes/spring-security-csrf-spa/)
- 모듈식 구성(Servlet/WebFlux 모두) 지원 — 기능별로 `Customizer<HttpSecurity>` 빈을 등록해 조합

**Cryptography**
- Password4j 기반 인코더 추가: `Argon2Password4jPasswordEncoder`, `BcryptPassword4jPasswordEncoder`, `ScryptPassword4jPasswordEncoder`, `Pbkdf2Password4jPasswordEncoder`, `BalloonHashingPassword4jPasswordEncoder`

**OAuth 2.0 / OIDC**
- **Password Grant 완전 제거** (RFC 9700/OAuth 2.1과 보조 맞춤)
- `@ClientRegistrationId` 타입 레벨 적용 가능
- OAuth 2.0 Dynamic Client Registration Protocol 지원
- Authorization Server에서 PKCE 기본 활성화
- `NimbusJwtDecoder`의 커스텀 `JwkSource` 지원, `NimbusJwtEncoder` 빌더(EC/RSA/secret key 지정 가능)
- OAuth2 Support for HTTP Service Clients (Spring Framework 6.x `@HttpExchange` 인터페이스 클라이언트에 access token을 자동 주입)

**SAML 2.0**
- OpenSAML 5로 이관. OpenSAML 4 지원 제거
- `AssertingPartyDetails` 클래스 기반 API → `AssertingPartyMetadata` 인터페이스 기반으로 교체
- JDBC 기반 `AssertingPartyMetadataRepository` 추가

**LDAP**
- `ApacheDsContainer`와 Apache DS 지원 제거. UnboundID로 통일

**Web**
- `MvcRequestMatcher`/`AntPathRequestMatcher` 제거. **`PathPatternRequestMatcher`만** 남음
- `LoginUrlAuthenticationEntryPoint`가 기본적으로 **상대 경로 리다이렉트**를 사용 (역프록시 뒤 hostname 문제 완화)
- Authorized 객체에 대해 Spring MVC 타입 지원
- 기본 로그인 페이지가 `factor.type` / `factor.reason` 파라미터로 MFA factor 표시 지원

**Jackson**
- 기본 직렬화/역직렬화 라이브러리가 **Jackson 3**. `SecurityJackson2Modules` → `SecurityJacksonModules`. Jackson 2 지원은 deprecated. [W](https://docs.spring.io/spring-security/reference/migration/index.html)

### 3.3 deprecation → 제거 매핑 (책에서 표로 다루기 좋음)

| 5.x/6.x | 6.5 (전환기) | 7.0 |
|----------|--------------|-----|
| `WebSecurityConfigurerAdapter` 클래스 상속 | deprecated → 빈 등록 방식 | 이미 6.0에서 제거 |
| `antMatchers()`, `mvcMatchers()`, `regexMatchers()` | deprecated, `requestMatchers()` 권고 | 제거. `PathPatternRequestMatcher`로 |
| `authorizeRequests` | deprecated | 제거. `authorizeHttpRequests`만 |
| `.and()` 체이닝 | deprecated | 제거. Lambda DSL만 |
| `HttpSecurity#apply(...)` | deprecated, `.with(...)` 권장 | 제거 |
| `AccessDecisionManager`/`Voter` | 5.5부터 deprecated | 별도 모듈로 분리 |
| `AuthorizationManager#check` | deprecated | 제거. `authorize` |
| `AntPathRequestMatcher` | deprecated | 제거 |
| OAuth2 Password Grant | deprecated | 제거 |
| OpenSAML 4 | 6.x에서 5도 옵션 | 4 제거 |
| Jackson 2 modules | 6.x 기본 | Jackson 3 기본 |

[W](https://medium.com/@reyanshicodes/spring-security-6-migration-nightmare-breaking-changes-survival-guide-feacb14a976b), [W](https://copyprogramming.com/howto/difference-between-requestmatchers-mvcmatchers-and-mvcmatcher), [W](https://github.com/spring-projects/spring-security/issues/12629)

### 3.4 권고 마이그레이션 순서

공식 가이드는 "6.5로 먼저 올리고, 6.5의 preparation step을 적용한 뒤 7.0으로 점프"를 권한다.

1. Spring Boot 3.5 / Spring Security 6.5 latest patch로 올림
2. 6.5의 `/migration-7/` 챕터에 따라:
   - `antMatchers`→`requestMatchers` 일괄 치환
   - `.and()` 체이닝 제거 → Lambda DSL
   - `apply(...)` → `with(...)`
   - `AuthorizationManager.check` 사용처 → `authorize`
   - Jackson 3 호환 검증 (`SecurityJacksonModules`)
3. CI에서 deprecation warning 0 확인
4. Spring Boot 4.0 + Security 7.0 latest patch로 점프
5. SAML 사용처는 OpenSAML 5 의존성 명시
6. LDAP 사용처는 UnboundID 확인

[W](https://docs.spring.io/spring-security/reference/migration/index.html), [W](https://docs.spring.io/spring-security/reference/6.5/migration-7/index.html)

자동화 도구: **OpenRewrite `rewrite-spring`** 레시피가 6.4/6.5 deprecation을 자동 치환한다. [W](https://github.com/openrewrite/rewrite-spring/issues/793)

---

## § 4. 인증 시나리오별 동작 원리

### 4.1 Form Login + Session

```java
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/", "/login", "/signup").permitAll()
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .logout(Customizer.withDefaults())
        .build();
}
```

흐름: `UsernamePasswordAuthenticationFilter`가 `POST /login` 폼을 가로채 `UsernamePasswordAuthenticationToken` 생성 → `AuthenticationManager` → `DaoAuthenticationProvider` → `UserDetailsService.loadUserByUsername()` → `PasswordEncoder.matches()` → 성공 시 `SecurityContext` 채우고 세션에 저장(`HttpSessionSecurityContextRepository`). [W](https://docs.spring.io/spring-security/reference/servlet/architecture.html)

### 4.2 HTTP Basic

테스트·내부 도구·M2M에서 유용. `BasicAuthenticationFilter`가 `Authorization: Basic ...` 헤더를 decode 후 동일하게 `AuthenticationManager`에 위임. 매 요청 인증이라 stateless하게 동작시키려면 `securityContext(s -> s.requireExplicitSave(true))`와 `sessionManagement(s -> s.sessionCreationPolicy(STATELESS))` 조합.

### 4.3 Remember-Me

세션 만료 후에도 쿠키로 재인증. Hash-based(간단·무상태) vs Persistent(테이블 저장, 토큰 회전). 모바일/SPA 환경에서는 **사용 비추**(쿠키-only). 서비스에서 길게 머무는 데스크톱 웹에 적합.

### 4.4 JWT 자원 서버 (Bearer)

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .csrf(CsrfConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .build();
}
```

`application.yml`:
```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
```

`issuer-uri` 한 줄로 `ReactiveJwtDecoders.fromIssuerLocation` / `JwtDecoders.fromIssuerLocation`이 OIDC discovery → JWKs URL을 캐시하고 `JwtDecoder`를 자동 생성. 커스터마이즈가 필요하면 직접 `JwtDecoder` 빈 등록. [W](https://docs.spring.io/spring-security/reference/reactive/oauth2/resource-server/jwt.html)

토큰의 `scope`/`scp` 클레임은 자동으로 `SCOPE_*` 권한으로 매핑된다. `roles` 같은 커스텀 클레임은 `JwtAuthenticationConverter`로 직접 매핑.

### 4.5 Opaque Token + Token Introspection

JWT가 아닌 불투명 토큰이면 매 요청 introspection endpoint 호출 → `oauth2ResourceServer(o -> o.opaqueToken(...))`. 비용·지연이 있으니 cache 필수.

### 4.6 OAuth2 Client + OIDC Login

```java
http.oauth2Login(o -> o.userInfoEndpoint(u -> u.oidcUserService(myOidcUserService)));
```

기본 흐름: `/oauth2/authorization/{registrationId}` → IdP 리다이렉트 → `/login/oauth2/code/{registrationId}` 콜백 → `OAuth2AuthorizationRequestRedirectFilter`/`OAuth2LoginAuthenticationFilter`가 code↔token 교환 → ID Token 디코드 → `OidcUser` 생성. **7.0부터 PKCE는 confidential client에도 기본 권장**. 확실히 켜려면 `OAuth2AuthorizationRequestCustomizers.withPkce()`. [W](https://www.baeldung.com/spring-security-pkce-secret-clients)

### 4.7 One-Time Token (OTT) / Magic Link (Spring Security 6.4 도입, 7에서 안정)

```java
http.oneTimeTokenLogin(ott -> ott
    .tokenGenerationSuccessHandler(magicLinkSender)
);
```

- 핵심 API: `OneTimeTokenService` (저장소). 구현: `InMemoryOneTimeTokenService`, `JdbcOneTimeTokenService` [W](https://docs.spring.io/spring-security/reference/servlet/authentication/onetimetoken.html)
- 전송 방식(메일·SMS)은 라이브러리가 결정하지 않음 → `OneTimeTokenGenerationSuccessHandler` 직접 구현
- 기본 generation/submit 페이지가 자동 제공되지만 프로덕션에서는 자체 UI 권장
- MFA의 두 번째 factor로 사용하기 좋다(§4.10 참고)

### 4.8 Passkeys / WebAuthn

```java
http.formLogin(withDefaults())
    .webAuthn(w -> w
        .rpId("example.com")
        .allowedOrigins("https://example.com")
    );
```

- 의존성: `spring-security-webauthn` (내부적으로 WebAuthn4J 사용) [W](https://docs.spring.io/spring-security/reference/servlet/authentication/passkeys.html)
- 등록 ceremony: `POST /webauthn/register/options` → `navigator.credentials.create()` → `POST /webauthn/register`
- 인증 ceremony: `POST /webauthn/authenticate/options` → `navigator.credentials.get()` → `POST /login/webauthn`
- 영속화: 기본 in-memory. 프로덕션은 `JdbcPublicKeyCredentialUserEntityRepository` + `JdbcUserCredentialRepository`
- 기본 등록/로그인 페이지가 자동 생성(브라우저에서 즉시 동작 확인 가능)

저자 노트(책 활용): "passkey 등록 후 패스워드를 비활성화하면 안 된다 — 디바이스 분실 시 복구 동선이 필요"라는 운영상 함정을 강조하면 좋다.

### 4.9 OAuth 2.0 DPoP-Bound Tokens (RFC 9449)

Spring Security 7은 자원 서버 측에서 DPoP-bound access token을 1급 처리.

- 액세스 토큰 JWT의 `cnf.jkt`(JWK SHA-256 thumbprint) 클레임이 클라이언트 키를 묶음
- 매 요청 `DPoP` 헤더(또 다른 JWT, `htm`/`htu`/`iat`/`jti`/`ath` 포함)를 검증
- `NimbusJwtEncoder`로 DPoP proof 자체를 만들 수 있는 예제가 공식 문서에 포함 [W](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/dpop-tokens.html)

값어치: 토큰을 sender-constrain. 토큰만 탈취해도 키 없이는 쓸 수 없다. BCP(RFC 9700)가 권장하는 sender-constraining의 표준 구현.

### 4.10 Multi-Factor Authentication (Spring Security 7 신규)

```java
@Configuration
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
class MfaConfig {}
```

핵심 아이디어: factor를 "추가 인증 메커니즘"이 아니라 **권한(Authority)** 으로 표현. 1번째 factor 성공 시 그 factor의 권한만 부여 → 인가 규칙에서 "두 factor 모두 필요"라고 적으면 사용자가 자동으로 다음 factor 페이지로 redirect됨. [W](https://spring.io/blog/2025/10/21/multi-factor-authentication-in-spring-security-7/), [W](https://docs.spring.io/spring-security/reference/servlet/authentication/mfa.html)

선택적 MFA(민감 endpoint에만):

```java
@Bean
AuthorizationManagerFactory<RequestAuthorizationContext> mfaFactory() {
    return new DefaultAuthorizationManagerFactory<>();
}
http.authorizeHttpRequests(a -> a
    .requestMatchers("/admin/**").access(mfaFactory.allAuthorities("FACTOR_PASSWORD", "FACTOR_OTT"))
    .anyRequest().authenticated());
```

### 4.11 SAML 2.0 (요점만)

엔터프라이즈 SSO. 7.0에서 OpenSAML 5 강제. `Saml2LoginConfigurer`로 SP 설정 → IdP metadata import(파일/URL/JDBC). 자세한 책 비중은 낮게 잡되 "IdP-initiated vs SP-initiated", "SLO 응답이 검증 실패해도 LogoutResponse를 돌려준다"는 7.0 동작 변경을 짚으면 충분.

### 4.12 LDAP / 커스텀 Authentication

7.0부터 임베디드 디렉터리 서버는 **UnboundID만**. ApacheDS는 사라짐.

커스텀 `AuthenticationProvider`를 만들고 싶을 때 패턴:

1. `AbstractAuthenticationToken` 상속 → 토큰 클래스 정의
2. `AuthenticationProvider.supports(Class)` 구현
3. `AuthenticationProvider.authenticate(Authentication)` 구현 (실패 시 `AuthenticationException` throw)
4. `AuthenticationManagerBuilder` 또는 `@Bean ProviderManager`로 등록

---

## § 5. 인가 모델

### 5.1 URL 기반 — `authorizeHttpRequests`

```java
http.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET, "/health").permitAll()
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .requestMatchers("/orders/**").hasAuthority("SCOPE_orders.read")
    .anyRequest().authenticated()
);
```

7에서 `PathPatternRequestMatcher`로 매처가 통일됐다는 점이 중요. Spring MVC와 같은 패턴 파서를 쓰므로 path variable 매칭이 일관된다.

```java
var p = PathPatternRequestMatcher.withDefaults();
http.authorizeHttpRequests(a -> a
    .requestMatchers(p.matcher("/products/{id}")).hasRole("USER")
    .requestMatchers(p.matcher("/products/{id}/edit")).hasRole("ADMIN")
    .anyRequest().authenticated());
```

[W](https://copyprogramming.com/howto/difference-between-requestmatchers-mvcmatchers-and-mvcmatcher)

### 5.2 Method Security

```java
@Configuration
@EnableMethodSecurity   // (NOT @EnableGlobalMethodSecurity)
class SecConfig {}
```

> "In Spring Security 6.2.7, if you only supply `@EnableGlobalMethodSecurity`, no method-security beans (e.g. `MethodSecurityInterceptor`) are registered, and no warning or error is logged. As a result, annotations like `@PreAuthorize` silently have no effect." — [W](https://github.com/spring-projects/spring-security/issues/17487)

> **함정**: 6.2.x에서 `@EnableGlobalMethodSecurity` (구버전 어노테이션)가 남아 있으면 method-security 빈이 등록되지 않아 `@PreAuthorize`가 **소리 없이 무력화**된다. 경고 로그도 없음. 7로 올릴 때 반드시 grep.

`@PreAuthorize("hasRole('ADMIN') and #user.id == authentication.principal.id")` 같은 SpEL은 `MethodSecurityExpressionHandler`가 평가. 6.3+에서 메타 어노테이션·`MethodAuthorizationDeniedHandler`로 인가 실패 응답을 커스터마이즈 가능. [W](https://www.baeldung.com/spring-security-6-3)

### 5.3 도메인 객체 보안 (ACL)

`spring-security-acl` 모듈. 객체 인스턴스 단위 권한이 필요할 때(예: 게시물 ID별 편집 권한). 책에서는 "쓸 만한 대안: AuthorizationManager로 #post.author == authentication.name SpEL"을 동시에 제시하면 도움이 된다.

### 5.4 Role Hierarchy

```java
@Bean
static RoleHierarchy roleHierarchy() {
    return RoleHierarchyImpl.withDefaultRolePrefix()
        .role("ADMIN").implies("STAFF")
        .role("STAFF").implies("USER")
        .build();
}
```

`ADMIN`으로 인증된 사용자는 `USER` 권한도 자동 보유한 것처럼 동작. [W](https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html)

### 5.5 Reactive Authorization

`authorizeExchange`로 동일 의미를 가진다. method security는 `@EnableReactiveMethodSecurity`. SpEL의 `authentication`/`principal`은 `Mono`로 흘러간다.

---

## § 6. 보안 표준과 트렌드

### 6.1 OWASP Top 10 2021 (Spring Security 책에서 자주 인용해야 할 항목)

| 코드 | 항목 | Spring Security가 다루는 지점 |
|------|------|-------------------------------|
| A01 | Broken Access Control | `AuthorizationManager`, method security, ACL, role hierarchy |
| A02 | Cryptographic Failures | `PasswordEncoder`(BCrypt/Argon2/PBKDF2), JWT 키 관리, JWE |
| A03 | Injection | (직접 다루지 않음 — Spring 입력 검증 영역) |
| A05 | Security Misconfiguration | 기본 secure headers, HSTS, X-Frame-Options |
| A07 | Identification & Authentication Failures | Form/MFA/Passkeys, session fixation 방지, brute-force lockout |
| A08 | Software & Data Integrity Failures | SBOM, dependency scanning (Spring Security 7는 Jackson 3로 ObjectMapper polymorphic 위험 정리) |

A01은 2021판에서 5위→**1위**로 상승. 평균 발견율 3.81%. [S](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/)
A02는 이전 "Sensitive Data Exposure"에서 이름·범위 변경. 약한 알고리즘·하드코딩 비밀번호 등 포함. [S](https://owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/)

### 6.2 OAuth 2.0 Security BCP — RFC 9700

2025-01 발행. RFC 6749/6750/6819를 업데이트하는 BCP. [S](https://datatracker.ietf.org/doc/rfc9700/)

핵심 규범 (Spring Security 7과 매핑):

- **Authorization Code + PKCE를 모든 클라이언트가 사용해야 한다** (public + confidential) → 7.0 Auth Server에서 PKCE 기본 ON [W](https://docs.spring.io/spring-security/reference/whats-new.html)
- **Implicit grant 사용 금지** → 7.0 client에서 제거 노선
- **Password Grant 사용 금지** → 7.0에서 완전 제거
- Redirect URI는 정확 매칭(exact string)
- Sender-constrained 토큰 권장 (mTLS, DPoP) → 7.0 DPoP 지원
- Refresh Token은 회전(rotate) 또는 sender-constrain
- Access Token을 query string에 넣지 말 것 → Authorization 헤더만

OAuth 2.1 draft도 BCP의 내용 다수를 코어 스펙으로 흡수 (필수 PKCE, Implicit/ROPC 제거, exact redirect URI). [S](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)

### 6.3 JWT BCP — RFC 8725 / BCP 225

[S](https://www.rfc-editor.org/rfc/rfc8725.html)

요점:

- `alg: none`을 절대 받아들이지 말 것
- `alg` 화이트리스트 강제 (서버가 결정)
- key confusion(예: HMAC 키를 RSA 공개키로 검증) 방지
- 약한 대칭키(사람이 외울 수 있는 패스워드) 금지
- 모든 클레임 검증: `iss`, `aud`, `exp`, `nbf`
- 페이로드는 평문 — PII/비밀 넣지 말 것

Spring Security는 `NimbusJwtDecoder`가 알고리즘 명시 시 그것만 허용한다. 키 확인 콜백을 헷갈리게 작성하면 RFC가 경고하는 key confusion에 빠질 수 있으므로 `JWKSet` 기반 디코더 사용을 권장.

### 6.4 WebAuthn Level 3 / Passkeys / FIDO Alliance

- W3C [WebAuthn Level 3 Working Draft](https://www.w3.org/TR/webauthn-3/) — 2025-01 publish. [S]
- FIDO Alliance가 WebAuthn + CTAP를 묶어 FIDO2로 정의. [S](https://fidoalliance.org/specifications/)
- Passkey는 "동기화 가능한 + 다중 디바이스" 사용자 친화 표현. WebAuthn 위에서 정의.
- 등록/인증 두 ceremony, "user verification" 플래그가 핵심 — biometric/PIN이 통과되면 UV=true. 책의 보안 모델 설명에서 challenge·signature·attestation을 한 다이어그램으로 정리하면 좋다.

### 6.5 NIST SP 800-207 Zero Trust

[S](https://csrc.nist.gov/pubs/sp/800/207/final)

핵심 7 tenets:

1. 모든 데이터 소스·서비스를 리소스로 본다
2. 모든 통신은 네트워크 위치와 무관하게 보호된다
3. 리소스 접근은 **세션 단위**로 부여된다
4. 접근은 **동적 정책**(주체·디바이스 신원·자산 상태·행동 속성)에 따라 결정된다
5. 자산의 보안 자세를 지속 모니터링
6. 인증·인가는 **접근 전에 동적이고 엄격하게** 강제된다
7. 조직은 자산·네트워크·통신의 현재 상태에 대해 최대한 많은 정보를 수집한다

책에서 활용: "Spring Security의 stateless JWT + 매 요청 인가 + DPoP/mTLS sender-constrain + MFA + 세션 단위 권한 부여"가 어떻게 Zero Trust 원칙 4·6에 매핑되는지를 박스로 그리면 강력하다.

### 6.6 BFF (Backend-for-Frontend) 패턴

SPA + OAuth2의 표준 모범. Token Handler Pattern이라고도. [W](https://curity.io/resources/learn/the-token-handler-pattern/), [W](https://duendesoftware.com/blog/20210326-bff)

핵심:

- 브라우저는 **OAuth 클라이언트 역할을 하지 않는다.** 토큰을 직접 다루지 않음
- BFF가 confidential client. 브라우저에는 HttpOnly·SameSite session cookie만
- BFF가 자기 도메인의 자원이면 CORS 불필요
- 토큰은 서버 측 저장 → XSS로 새지 않음
- CSRF는 SameSite + custom header(이중 방어)

Spring Cloud Gateway + Spring Security oauth2Login으로 구성 가능. [W](https://www.baeldung.com/spring-cloud-gateway-bff-oauth2)

7.0의 `http.csrf(CsrfConfigurer::spa)`는 BFF 시나리오를 직접 단순화한다. [W](https://github.com/spring-projects/spring-security/issues/14149)

### 6.7 CORS / CSRF / Headers — 자주 헷갈리는 부분

- **CORS는 Spring Security가 처리하기 _이전_ 에 통과되어야 한다.** preflight(OPTIONS)는 쿠키 없이 오므로 Security가 401로 차단하면 SPA가 죽는다. `http.cors(Customizer.withDefaults())` + `CorsConfigurationSource` 빈으로 권장. OPTIONS 허용 필수. [W](https://www.baeldung.com/spring-security-cors-preflight)
- **CSRF**: stateful(쿠키 기반) 흐름에서 필수. Bearer token API는 보통 disable해도 안전(토큰이 쿠키로 자동 첨부되지 않으므로). SPA + BFF는 7.0 `spa()` 한 줄이 가장 깔끔.
- **HSTS**: HTTPS-only 환경에서 켜기. dev 환경에서는 끄거나 `includeSubDomains` 끄기 (한 번 켜지면 브라우저가 캐시).
- **Content Security Policy**: Spring Security는 헤더 작성만 도와줌. 정책 자체는 앱이 결정.

### 6.8 Secret 회전, 키 관리

- JWT 서명 키: JWK rotation. `JWKSet` URL을 IdP가 노출 → kid로 식별, 클라이언트는 캐시. `NimbusJwtDecoder` + `JwkSourceBuilder`로 7.0에서 커스텀 회전 로직 주입 가능 [W](https://docs.spring.io/spring-security/reference/whats-new.html)
- 패스워드: BCrypt 12 work factor 권장. Argon2id가 더 강함 → 7.0 `Argon2Password4jPasswordEncoder` 사용
- DB credential: Spring Cloud Config + Vault 권장. application.yml에 평문 금지 (Actuator `env` endpoint 노출 사고가 우아한형제들 기술블로그에 실제 사례로 정리됨) [C](https://techblog.woowahan.com/9232/)

---

## § 7. 실무 함정 사례 (커뮤니티)

### 7.1 마이그레이션 함정 (5/6 → 6/7)

**함정 1. Stack Overflow 2019년 답변 복붙**
> "Most Spring Security problems in code review come from copy-pasting a Stack Overflow answer from 2019 using `WebSecurityConfigurerAdapter`." — [W](https://www.toptal.com/spring/spring-security-tutorial)
- 증상: 빌드는 되는데 인증이 작동하지 않음, deprecated 경고 폭주
- 해법: 6.5의 prep step 단계 빠짐없이 적용 후 7로

**함정 2. `@EnableGlobalMethodSecurity` 잔존**
- `@PreAuthorize`가 소리 없이 무력화 — 6.2.7 issue [W](https://github.com/spring-projects/spring-security/issues/17487)
- 해법: 전체 모듈 grep 후 `@EnableMethodSecurity`로 교체

**함정 3. `.and()` 체이닝**
- 7에서 컴파일 에러. 마이그레이션 첫 빌드에서 가장 많이 보이는 에러
- 해법: Lambda DSL로 일괄 치환. IDE 인스펙션·OpenRewrite 활용

**함정 4. `mvcMatchers` vs `antMatchers` 차이**
- `MvcRequestMatcher`는 Spring MVC path matching을 따라 `/api`와 `/api/` 같이 trailing slash 보정. `AntPathRequestMatcher`는 안 함. 잘못 섞이면 403/200 일관성 깨짐. [W](https://sensei.securecodewarrior.com/recipes/scw:spring:access-control-use-mvcMatchers-over-antMatchers)
- 7.0에서는 `PathPatternRequestMatcher`로 통일 — 좋은 일

**함정 5. 한국 velog/블로그 사례 — `SecurityFilterChain`만 만들고 `WebSecurityCustomizer`를 잊음**
- 정적 자원(`/css/**`, `/js/**`)에 대해 필터를 아예 안 태우려면 `WebSecurityCustomizer`로 ignore 처리해야 효율적 [C](https://velog.io/@nays33/WebSecurityConfigurerAdapter-%EB%8C%80%EC%8B%A0-Securityfilterchain-WebSecurityCustomizer%EB%A1%9C-%EC%A7%81%EC%A0%91-%EC%BB%A4%EC%8A%A4%ED%84%B0%EB%A7%88%EC%9D%B4%EC%A7%95-%ED%95%98%EA%B8%B0)

### 7.2 JWT 함정

**함정 6. JWT를 세션 토큰처럼 쓴다**
> "Some experts argue that JWTs which just store a simple session token are inefficient and less flexible than a regular session cookie, and don't gain you any advantage." — [W](https://gist.github.com/samsch/0d1f3d3b4745d778f78b230cf6061452)
- 강제 로그아웃 불가, 권한 변경 즉시 반영 불가 — 기능 부재가 핵심 함정
- 해법: blacklist 캐시(Redis) 또는 짧은 access token + refresh token 회전

**함정 7. localStorage에 JWT 저장**
- XSS 한 번이면 토큰 탈취. [W](https://katyella.com/blog/spring-boot-security-best-practices/)
- 해법: HttpOnly·Secure·SameSite=Strict 쿠키 + CSRF 토큰. 또는 BFF로 토큰을 브라우저에서 완전 분리

**함정 8. `alg: none` 또는 알고리즘 confusion**
- RFC 8725가 첫 번째로 경고. [S](https://www.rfc-editor.org/rfc/rfc8725.html)
- 해법: `JwtDecoder` 구성 시 알고리즘 명시. JWKS 기반 verify 사용

**함정 9. Refresh Token Rotation 미구현**
- access token만 짧게 잡고 refresh token은 1년 — 사실상 영구 세션. 탈취 시 무한 사용
- 해법: 회전(이전 토큰 invalidate) + reuse detection → 재사용 감지 시 사용자 전체 토큰 폐기 [W](https://thachtaro2210.github.io/posts/springboot-jwt-refresh-rotation/)

### 7.3 세션 / 쿠키 함정

**함정 10. CSRF disable 후 Form 로그인**
- "API니까 disable" 했는데 form login도 같이 깨짐. CSRF는 stateful flow에서 필수
- 해법: 자원 서버 경로만 `securityMatcher`로 분리해 stateless·csrf disable, 웹 경로는 stateful·csrf enable로 분리한 두 개의 `SecurityFilterChain`

**함정 11. CORS preflight 401**
- Security 필터가 CORS보다 앞에 와서 OPTIONS 요청을 인증 요구. 브라우저 SPA가 모든 호출에서 깨짐
- 해법: `http.cors(...)` 명시 + `CorsConfigurationSource` 빈. Security가 CORS 빈을 찾아 자기보다 앞에 둠. [W](https://www.baeldung.com/spring-security-cors-preflight)

**함정 12. Session Fixation**
- 로그인 전 발급된 세션ID로 인증 후에도 그대로 사용 — 공격자가 미리 알아낸 세션ID로 가로채기
- Spring Security 기본은 `sessionManagement().sessionFixation().migrateSession()` (안전). 그러나 커스텀 세션 관리 시 잘못 끄는 경우 종종 발생

**함정 13. MODE_INHERITABLETHREADLOCAL + 스레드 풀**
- §2.6 참조. 다른 사용자의 SecurityContext가 다음 요청에 노출 [W](https://github.com/spring-projects/spring-security/issues/6856)

### 7.4 OAuth2 / OIDC 함정

**함정 14. Redirect URI 와일드카드**
- "테스트하기 편하니까 `https://*.example.com/*`" — RFC 9700 위반. open redirect 공격 가능
- 해법: 정확 매칭 등록. 환경별로 분리 등록 [S](https://datatracker.ietf.org/doc/rfc9700/)

**함정 15. confidential client에서 PKCE 안 씀**
- 7.0 default가 변경됐지만, 6.x에서 올라온 코드가 explicit하게 끄고 있을 수 있음
- 해법: `OAuth2AuthorizationRequestCustomizers.withPkce()` 명시

**함정 16. ID Token으로 API 인가**
- ID Token은 사용자 식별용. Access Token으로 자원 접근. 헷갈리면 보안 모델이 무너짐

### 7.5 Spring Boot Actuator 사고 (한국 사례)

> "Security Actuator 안전하게 사용하기" — 우아한형제들 기술블로그
> Actuator는 개발자에게 편리하지만 잘못 쓰면 매우 위험. `env`/`heapdump`/`configprops` 노출 사고 사례 정리. [C](https://techblog.woowahan.com/9232/)

해법:
- 운영망에서는 `management.endpoints.web.exposure.include`를 `health` 정도로 제한
- 별도 포트로 노출 (`management.server.port`)
- Spring Security로 actuator 경로에 별도 인증 chain

### 7.6 한국 velog 공통 시행착오

velog 글들에서 반복되는 패턴 [C]:

- "Spring Boot 3.x로 올렸더니 모든 `WebSecurityConfigurerAdapter` 빨갛게" — 가장 흔한 첫 경험
- "람다 DSL 처음 보면 어색하지만 한 번 익히면 더 명확함" 후기
- "JWT 직접 구현 vs `oauth2ResourceServer.jwt()` — 후자가 압도적으로 안전·간결" 결론에 수렴
- 인증/인가 메커니즘 설명 시 "인증 필터는 인가 필터보다 앞쪽" 원칙을 학습 시점마다 재발견 [C](https://velog.io/@on5949/SpringSecurity-%EC%8A%A4%ED%94%84%EB%A7%81-%EC%8B%9C%ED%81%90%EB%A6%AC%ED%8B%B0-%ED%95%84%ED%84%B0-%EC%B2%B4%EC%9D%B8-%EC%8B%AC%ED%99%94)

### 7.7 Lambda DSL 학습 곡선

> "The previous configuration approach was unclear about what object was getting configured without knowing the return type, and the deeper the nesting the more confusing it became." — Spring 팀 [W](https://spring.io/blog/2019/11/21/spring-security-lambda-dsl/)

긍정 의견: 람다 DSL은 자동 들여쓰기·`.and()` 불필요·readability 개선.
부정 의견(커뮤니티): 입문자에게 IntelliJ 자동완성 의존도가 높아짐, 한 줄로 끝나던 설정이 여러 줄로 늘어남.

7.0에서는 선택이 아니라 강제. 책에서는 "Lambda DSL 핵심 5분 가이드" 박스를 챕터 초반에 두는 게 효과적.

---

## § 8. 핵심 코드 패턴 (Spring Boot 4 + Spring Security 7)

> 7.0의 정확한 시그니처는 GA(2025-11-17) 기준 공식 docs를 따랐다. 7.1 milestone 시점의 미세 변동은 본 책 출간 시점 재확인 필요.

### 8.1 가장 기본 — 폼 로그인 + 세션

```java
@Configuration
@EnableWebSecurity
class WebSecurityConfig {
    @Bean
    SecurityFilterChain web(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(a -> a
                .requestMatchers("/", "/login", "/signup", "/css/**").permitAll()
                .anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .logout(Customizer.withDefaults())
            .csrf(Customizer.withDefaults())
            .headers(h -> h.contentSecurityPolicy(c -> c.policyDirectives("default-src 'self'")))
            .build();
    }

    @Bean
    PasswordEncoder passwordEncoder() {
        return new Argon2Password4jPasswordEncoder(); // 7.0 신규
    }
}
```

### 8.2 두 개의 체인 — 웹 + API 분리

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .csrf(CsrfConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .build();
}

@Bean
@Order(2)
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/", "/login").permitAll()
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .csrf(Customizer.withDefaults())
        .build();
}
```

### 8.3 SPA용 CSRF + CORS

```java
@Bean
SecurityFilterChain spa(HttpSecurity http, CorsConfigurationSource cors) throws Exception {
    return http
        .cors(c -> c.configurationSource(cors))
        .csrf(CsrfConfigurer::spa)        // 7.0 한 줄
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2Login(Customizer.withDefaults())
        .build();
}

@Bean
CorsConfigurationSource corsConfig() {
    var c = new CorsConfiguration();
    c.setAllowedOrigins(List.of("https://app.example.com"));
    c.setAllowedMethods(List.of("GET","POST","PUT","DELETE","OPTIONS"));
    c.setAllowedHeaders(List.of("*"));
    c.setAllowCredentials(true);
    var src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/**", c);
    return src;
}
```

### 8.4 JWT 커스텀 권한 매핑

```java
@Bean
JwtAuthenticationConverter jwtAuthConverter() {
    var roles = new JwtGrantedAuthoritiesConverter();
    roles.setAuthoritiesClaimName("roles");
    roles.setAuthorityPrefix("ROLE_");
    var conv = new JwtAuthenticationConverter();
    conv.setJwtGrantedAuthoritiesConverter(roles);
    return conv;
}

@Bean
SecurityFilterChain api(HttpSecurity http, JwtAuthenticationConverter conv) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(conv)))
        .build();
}
```

### 8.5 OAuth2 Login + PKCE (confidential client)

```java
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2Login(o -> o.authorizationEndpoint(
            ep -> ep.authorizationRequestResolver(
                pkceResolver(clientRegistrationRepository()))))
        .build();
}

DefaultOAuth2AuthorizationRequestResolver pkceResolver(ClientRegistrationRepository repo) {
    var resolver = new DefaultOAuth2AuthorizationRequestResolver(repo, "/oauth2/authorization");
    resolver.setAuthorizationRequestCustomizer(OAuth2AuthorizationRequestCustomizers.withPkce());
    return resolver;
}
```

### 8.6 One-Time Token (Magic Link)

```java
@Bean
SecurityFilterChain ott(HttpSecurity http, MagicLinkSender sender) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oneTimeTokenLogin(ott -> ott
            .tokenGenerationSuccessHandler(sender::send))
        .build();
}

@Bean
OneTimeTokenService oneTimeTokenService(JdbcOperations jdbc) {
    return new JdbcOneTimeTokenService(jdbc);
}
```

### 8.7 Passkeys

```java
@Bean
SecurityFilterChain passkey(HttpSecurity http) throws Exception {
    return http
        .formLogin(Customizer.withDefaults())
        .webAuthn(w -> w
            .rpId("example.com")
            .rpName("Example")
            .allowedOrigins("https://example.com"))
        .build();
}
```

### 8.8 MFA — Password + OTT

```java
@Configuration
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
class MfaConfig {
    @Bean
    SecurityFilterChain http(HttpSecurity http, MagicLinkSender sender) throws Exception {
        return http
            .authorizeHttpRequests(a -> a.anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(ott -> ott.tokenGenerationSuccessHandler(sender::send))
            .build();
    }
}
```

### 8.9 Role Hierarchy

```java
@Bean
static RoleHierarchy roleHierarchy() {
    return RoleHierarchyImpl.withDefaultRolePrefix()
        .role("ADMIN").implies("MANAGER")
        .role("MANAGER").implies("USER")
        .build();
}

@Bean
static GrantedAuthorityDefaults defaults() {
    return new GrantedAuthorityDefaults("ROLE_");
}
```

### 8.10 Method Security 메타 어노테이션

```java
@Target(METHOD)
@Retention(RUNTIME)
@PreAuthorize("hasRole('ADMIN')")
public @interface AdminOnly {}

@Service
class OrderService {
    @AdminOnly
    public void cancelAll() {...}
}
```

### 8.11 Reactive (WebFlux) 자원 서버

```java
@Bean
SecurityWebFilterChain reactive(ServerHttpSecurity http) {
    return http
        .authorizeExchange(ex -> ex
            .pathMatchers("/actuator/health").permitAll()
            .anyExchange().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .csrf(ServerHttpSecurity.CsrfSpec::disable)
        .build();
}
```

### 8.12 SecurityContext를 비동기로 안전 전파

```java
@Bean
AsyncTaskExecutor delegatingExecutor(ThreadPoolTaskExecutor base) {
    return new DelegatingSecurityContextAsyncTaskExecutor(base);
}
```

---

## § 9. 논쟁점·상충 관점

- **JWT vs Session.** [W](https://dzone.com/articles/stop-using-jwts-as-session-tokens) "API에는 JWT, 웹 앱에는 세션" 단순 이분법은 위험. BFF 등장 이후 합의되어 가는 새 표준은 "브라우저는 세션 쿠키, 서비스 간은 토큰". 책에서는 두 관점 모두 제시 후 BFF로 수렴하는 게 흐름이 자연스럽다.
- **`@PreAuthorize` SpEL의 깊이.** 비즈니스 로직을 SpEL에 너무 많이 넣으면 테스트가 어려워진다는 반대 의견 존재. 대안: 서비스 메서드 내부에서 `AuthorizationManager`/`@Service` 권한 검사.
- **Spring Authorization Server를 직접 운영 vs 외부 IdP 사용.** Spring Authorization Server가 7.0에 흡수되며 운영 부담이 줄었지만, 여전히 IDaaS(Auth0, Okta, Keycloak)를 쓰는 게 일반적 베스트프랙티스 — 책에서 결정 트리 제시 권장.
- **JWT in localStorage vs cookie.** 다수의 보안 가이드는 HttpOnly 쿠키. 그러나 SPA 백엔드가 도메인 분리된 경우 쿠키 전달이 까다로워 일부 팀은 in-memory + refresh 패턴을 채택. 정답이 하나가 아님을 명시.

---

## § 10. 참고문헌

### 공식 문서 / Spring 공식 블로그

- Spring Security Reference — What's New in 7.0: https://docs.spring.io/spring-security/reference/whats-new.html
- Spring Security Migration Guide: https://docs.spring.io/spring-security/reference/migration/index.html
- Servlet Architecture: https://docs.spring.io/spring-security/reference/servlet/architecture.html
- Authorization Architecture: https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html
- Method Security: https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html
- Passkeys: https://docs.spring.io/spring-security/reference/servlet/authentication/passkeys.html
- One-Time Token Login: https://docs.spring.io/spring-security/reference/servlet/authentication/onetimetoken.html
- MFA: https://docs.spring.io/spring-security/reference/servlet/authentication/mfa.html
- DPoP Tokens: https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/dpop-tokens.html
- OAuth2 Resource Server JWT: https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
- WebFlux Configuration: https://docs.spring.io/spring-security/reference/reactive/configuration/webflux.html
- CSRF: https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html
- Spring Blog — Spring Security 7.0 GA: https://spring.io/blog/2025/11/17/spring-security-releases/
- Spring Blog — Authorization Server moves to Security 7: https://spring.io/blog/2025/09/11/spring-authorization-server-moving-to-spring-security-7-0/
- Spring Blog — MFA in Security 7: https://spring.io/blog/2025/10/21/multi-factor-authentication-in-spring-security-7/
- Spring Blog — Lambda DSL 도입 배경: https://spring.io/blog/2019/11/21/spring-security-lambda-dsl/

### 표준 / RFC / W3C / NIST

- RFC 9700 — OAuth 2.0 Security Best Current Practice (2025-01): https://datatracker.ietf.org/doc/rfc9700/
- RFC 8725 / BCP 225 — JWT Best Current Practices: https://www.rfc-editor.org/rfc/rfc8725.html
- RFC 9449 — OAuth 2.0 DPoP: https://www.rfc-editor.org/rfc/rfc9449.html
- OAuth 2.1 Draft: https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/
- W3C WebAuthn Level 3 Working Draft: https://www.w3.org/TR/webauthn-3/
- FIDO Alliance Specifications: https://fidoalliance.org/specifications/
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- OWASP Top 10:2021 — A01 Broken Access Control: https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/
- OWASP Top 10:2021 — A02 Cryptographic Failures: https://owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/
- OWASP Top 10:2021 — A07 Authentication Failures: https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/

### 검증된 저자 블로그

- Baeldung — AuthorizationManager: https://www.baeldung.com/spring-security-authorizationmanager
- Baeldung — Passkeys integration: https://www.baeldung.com/spring-security-integrate-passkeys
- Baeldung — One-Time Token: https://www.baeldung.com/spring-security-one-time-token-login
- Baeldung — Spring Cloud Gateway BFF + OAuth2: https://www.baeldung.com/spring-cloud-gateway-bff-oauth2
- Baeldung — PKCE for Secret Clients: https://www.baeldung.com/spring-security-pkce-secret-clients
- Baeldung — CORS Preflight + Security: https://www.baeldung.com/spring-security-cors-preflight
- Baeldung — Method Security: https://www.baeldung.com/spring-security-method-security
- Baeldung — Spring Security 6.3 What's New: https://www.baeldung.com/spring-security-6-3
- Baeldung — MFA in Security 7: https://www.baeldung.com/spring-security-7-mfa
- Dimitri (dimitri.codes) — Authorization Server in Security 7: https://dimitri.codes/authorization-server/
- Dimitri — CSRF for SPA: https://dimitri.codes/spring-security-csrf-spa/
- Dimitri — MFA: https://dimitri.codes/multi-factor-authentication-spring-security/
- Dan Vega — Spring Security 7 MFA: https://www.danvega.dev/blog/spring-security-7-multi-factor-authentication
- Curity — Token Handler Pattern (BFF): https://curity.io/resources/learn/the-token-handler-pattern/
- Curity — WebAuthn Overview: https://curity.io/resources/learn/webauthn-overview/
- Auth0 — PKCE in Spring Security: https://auth0.com/blog/pkce-in-web-applications-with-spring-security/
- Auth0 — Passkeys for Java: https://auth0.com/blog/webauthn-and-passkeys-for-java-developers/
- Okta — PKCE with Spring Boot: https://developer.okta.com/blog/2020/01/23/pkce-oauth2-spring-boot
- Duende — Securing SPAs with BFF: https://duendesoftware.com/blog/20210326-bff
- Reyanshicodes — Spring Security 6 Migration Nightmare: https://medium.com/@reyanshicodes/spring-security-6-migration-nightmare-breaking-changes-survival-guide-feacb14a976b
- InfoQ — Spring 7 / Boot 4 release coverage: https://www.infoq.com/news/2025/11/spring-7-spring-boot-4/

### 한국 기술 블로그 / 커뮤니티 (velog 등)

- 우아한형제들 기술블로그 — Security Actuator 안전하게 사용하기: https://techblog.woowahan.com/9232/
- velog @pjh612 — WebSecurityConfigurerAdapter deprecated 대처: https://velog.io/@pjh612/Deprecated%EB%90%9C-WebSecurityConfigurerAdapter-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%8C%80%EC%B2%98%ED%95%98%EC%A7%80
- velog @nays33 — SecurityFilterChain + WebSecurityCustomizer 커스터마이징: https://velog.io/@nays33/WebSecurityConfigurerAdapter-%EB%8C%80%EC%8B%A0-Securityfilterchain-WebSecurityCustomizer%EB%A1%9C-%EC%A7%81%EC%A0%91-%EC%BB%A4%EC%8A%A4%ED%84%B0%EB%A7%88%EC%9D%B4%EC%A7%95-%ED%95%98%EA%B8%B0
- velog @on5949 — 스프링 시큐리티 필터 체인 심화: https://velog.io/@on5949/SpringSecurity-%EC%8A%A4%ED%94%84%EB%A7%81-%EC%8B%9C%ED%81%90%EB%A6%AC%ED%8B%B0-%ED%95%84%ED%84%B0-%EC%B2%B4%EC%9D%B8-%EC%8B%AC%ED%99%94
- velog @jwkwon0817 — Spring Security config using Bean: https://velog.io/@jwkwon0817/spring-security-config-using-bean
- velog @goat_hoon — Spring Security를 활용한 JWT 도입기: https://velog.io/@goat_hoon/Spring-Security%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-JWT-%EB%8F%84%EC%9E%85%EA%B8%B0
- velog @soheelog — Spring Security JWT 설정: https://velog.io/@soheelog/Spring-Security-JWT-%EC%84%A4%EC%A0%95

### 일반 보안·비교 분석

- WorkOS — OAuth Best Practices Reading 9700: https://workos.com/blog/oauth-best-practices
- Scalekit — OAuth 2.0 Best Practices RFC 9700: https://www.scalekit.com/blog/oauth-2-0-best-practices-rfc9700
- Authgear — Demonstrating Proof-of-Possession (DPoP) Guide: https://www.authgear.com/post/demonstrating-proof-of-possession-dpop
- FusionAuth — OAuth 2.0 vs OAuth 2.1: https://fusionauth.io/articles/oauth/differences-between-oauth-2-oauth-2-1
- DZone — Stop Using JWTs as Session Tokens: https://dzone.com/articles/stop-using-jwts-as-session-tokens
- GitHub gist samsch — Stop Using JWTs: https://gist.github.com/samsch/0d1f3d3b4745d778f78b230cf6061452
- BezKoder — Refresh Token Rotation Example: https://www.bezkoder.com/spring-boot-refresh-token-jwt/
- ThachTaro — Refresh Token Rotation: https://thachtaro2210.github.io/posts/springboot-jwt-refresh-rotation/
- DevGlan — JWT Authentication Pitfalls: https://www.devglan.com/spring-security/jwt-authentication-spring-security
- Katyella — Spring Boot Security Best Practices: https://katyella.com/blog/spring-boot-security-best-practices/

### GitHub / Issue Tracker (인용 근거)

- spring-security#17487 — @PreAuthorize silently disabled: https://github.com/spring-projects/spring-security/issues/17487
- spring-security#14149 — Simplify CSRF Configuration for SPAs: https://github.com/spring-projects/spring-security/issues/14149
- spring-security#6856 — MODE_INHERITABLETHREADLOCAL + thread pools 위험: https://github.com/spring-projects/spring-security/issues/6856
- spring-security#12629 — Deprecate .and() + non-lambda DSL: https://github.com/spring-projects/spring-security/issues/12629
- openrewrite/rewrite-spring#793 — Migration Recipe for 6.4/6.5 deprecations: https://github.com/openrewrite/rewrite-spring/issues/793

---

## § 11. 리서치 한계

수집 과정에서 의도적으로 또는 접근 제약으로 충분히 다루지 못한 영역을 정직히 기록한다.

1. **7.1.x milestone API 시그니처.** 책 출간 시점 GA(7.0.x)와 7.1 milestone이 공존할 수 있다. 정확한 패키지/메서드 시그니처는 출간 직전 docs로 재검증 필요. 특히 `AuthorizationManagerFactory`, `@EnableMultiFactorAuthentication`은 minor 보강 가능성.
2. **Spring Authorization Server의 흡수 후 패키지 변경 상세.** 공식 공지는 "minor relocation"만 언급. 정확한 import 변경 목록은 7.0.0 changelog 직접 확인이 필요하다.
3. **Virtual Threads + Spring Security 공식 가이드.** 현재 공식 문서가 빈약. Carrier pinning, `SecurityContext` 전파를 Loom 환경에서 다루는 단일 reference 자료가 부족 — 책에서는 경험적 패턴 + 공식 docs 인용 한도 내에서.
4. **Reddit / Hacker News 정량적 의견 분포.** 검색 도구가 reddit 본문 접근에 제한 — 대신 동일 주제의 medium/dev.to/velog 글을 통해 의견을 간접 수집. r/SpringBoot 직접 토픽은 추가 도구로 보강 권장.
5. **Spring 공식 한국 컨퍼런스(SpringCamp) 영상 자료.** 본 라운드에서 영상 트랜스크립트 추출은 생략. 책 후반 사례 보강 시 별도 단계로.
6. **Spring Authorization Server의 OAuth2 Dynamic Client Registration 구체 예제.** 공식 What's New에서 새 기능으로 적시했지만, 종합적 튜토리얼은 GA 직후라 정리된 글이 거의 없다 — 책에서는 RFC 7591 인용 + 공식 docs 직접 참조 구조로.
7. **OKKY, 카카오/토스 기술블로그에서 Spring Security 7 직접 다룬 글.** 검색 시점에 GA 후 6개월이 안 되어 한국어 deep-dive 자료가 거의 없음 — velog 단편글 위주. 카카오/토스의 Spring Security 운영기는 6.x 기준이거나 사내 비공개. 책에서는 5/6 단계의 한국 노하우를 7 맥락으로 재해석하는 게 현실적 접근.

리서치 결과의 **신뢰 등급**: 공식 docs·spring.io blog·RFC·NIST는 최상. Baeldung·Auth0·Curity·Dimitri는 검증된 저자 블로그로 중상. velog/medium 일반 글은 사례·시행착오 인용 용도로 중. 본 reference는 책 챕터 작성 시 출처 태그를 그대로 따라 인용·검증할 수 있도록 URL을 모두 보존했다.
