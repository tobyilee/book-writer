# 14장. Zero Trust·BFF·운영의 모서리 — 트렌드와 표준

> **선행 필요:** 1장(멘탈 모델), 5장(JWT/DPoP), 6장(OAuth2 Client), 8장(인가), 9·10장(횡단)

한 권의 책을 거의 다 읽었다. `SecurityFilterChain`이 어떻게 짜이는지 알게 됐고, `AuthorizationManager`가 무슨 일을 하는지도 손에 잡힌다. JWT 자원 서버를 직접 세워 봤고, DPoP로 sender-constrained 토큰까지 다뤘다. Passkeys 등록 ceremony도, OTT 매직 링크도, MFA factor를 권한으로 표현하는 모델도 모두 지나왔다. 인가의 다섯 층을 가르며 SpEL 함정도 짚었고, CSRF·CORS·헤더가 왜 헷갈리는지도 풀었다. Reactive 보안과 테스팅 안전망까지 깔렸고, 마이그레이션 함정 5건을 13장에서 정리했다.

그런데, 잠깐 한 발 물러서 보자. 우리가 만든 이 시스템은 **어떤 시대의 어디에 서 있는가?**

이 질문은 한가한 질문이 아니다. 운영을 한 해 이상 해 본 사람이라면 누구나 안다. 표준은 끊임없이 갱신되고, 어제의 모범이 오늘의 안티 패턴이 된다. 2018년에 "API는 JWT, 웹은 세션"이라는 단순 이분법이 흔한 답이었지만, 지금은 BFF(Backend-for-Frontend) 패턴이 그 자리를 빠르게 채우고 있다. 그 사이에 NIST는 SP 800-207로 "Zero Trust"를 표준 문서화했고, OAuth 2.0은 RFC 9700으로 BCP를 갱신했고, JWT는 RFC 8725로 사용 모범이 정리됐다. 우리가 한 번 만든 코드가 그 흐름과 호흡을 같이하지 않으면, 일 년 뒤에 다시 모든 결정을 검토해야 한다.

이번 장은 그 호흡 맞추기다. 신기능 자랑이 아니라, 우리가 14장 이전까지 짜 둔 모든 코드가 **현재 표준의 어느 좌표에 정확히 얹히는지** 그려 보자는 이야기다. 그리고 그 좌표 옆에 있는 운영의 모서리들 — Secret 회전, Actuator 노출, 감사 로그 — 을 차근차근 짚는다. 마지막엔 책 전체에서 미뤄 둔 논쟁점들을 한자리에 모아 정리한다. JWT vs 세션, localStorage vs Cookie, 자체 IdP vs 외부 IdP. 답은 하나가 아닐 것이다. 그러나 답을 못 정해서가 아니라, 답이 시스템 맥락에 따라 갈리기 때문이라는 것을, 이 장이 끝날 때쯤 함께 보게 될 것이다.

한 가지 미리 약속해 두자. **Zero Trust는 "원칙"이지 "제품"이 아니다.** 어떤 벤더가 "우리 솔루션이 Zero Trust"라고 광고한다면, 그건 정확하지 않은 표현이다. NIST SP 800-207은 일곱 가지 원칙을 제시할 뿐, 한 줄의 코드도, 한 가지의 제품도 권하지 않는다. 우리가 할 일은 그 원칙들을 우리 손에 익은 Spring Security 부품 위에 하나씩 얹어 보는 것이다. 그리고 빈자리가 어디인지 정확히 찾아내는 것이다.

## 14.1 NIST SP 800-207 Zero Trust 7 tenets — Spring Security와 정면으로 맞대 보자

먼저 Zero Trust부터 짚어 보자. NIST가 2020년에 SP 800-207을 최종 확정했고, 그 안에 일곱 가지 원칙(tenets)이 박혀 있다. 보안 업계가 이 문서를 표준 문서로 받아들였기 때문에, "Zero Trust"라는 단어를 진지하게 쓰는 사람은 누구든 이 일곱 원칙을 참조점으로 삼는다. 그러니 우리도 한 번은 정면으로 봐야 한다. 그리고 더 중요한 건, 우리가 이 책에서 짜 온 코드가 일곱 원칙 각각에 어떻게 닿는지 손가락으로 짚어 보는 것이다.

원칙은 이렇다.

> **NIST SP 800-207 7 tenets** ([NIST 원문](https://csrc.nist.gov/pubs/sp/800/207/final))
>
> 1. 모든 데이터 소스·서비스를 리소스로 본다.
> 2. 모든 통신은 네트워크 위치와 무관하게 보호된다.
> 3. 리소스 접근은 **세션 단위**로 부여된다.
> 4. 접근은 **동적 정책**(주체·디바이스 신원·자산 상태·행동 속성)에 따라 결정된다.
> 5. 자산의 보안 자세를 지속 모니터링한다.
> 6. 인증·인가는 **접근 전에 동적이고 엄격하게** 강제된다.
> 7. 조직은 자산·네트워크·통신의 현재 상태에 대해 최대한 많은 정보를 수집한다.

읽기에 추상적이다. 한 줄씩 우리 코드 어휘로 옮겨 보자.

**원칙 1 — 모든 데이터 소스·서비스를 리소스로 본다.** 이 한 줄이 사실 가장 깊다. 옛날 네트워크 보안 모델은 "내부망은 안전, 외부망은 위험"이라는 경계를 그었다. 회사 VPN 안에 들어오면 모든 내부 API가 자동으로 신뢰됐다. 지금은 그게 통하지 않는다. 사내 API라도 인증을 요구해야 하고, 마이크로서비스 간 호출도 토큰을 들고 다녀야 한다. Spring Security에서 보면 어떤가? 2장에서 짠 `SecurityFilterChain`이 모든 `HttpServletRequest`를 똑같이 필터에 태운다. `/internal/health`라고 해서 자동 허용되지 않는다. `permitAll()`은 우리가 명시적으로 허용하지 않는 한 절대 켜지지 않는다. 7.0의 기본 정책이 "인증된 요청 외엔 거부"인 이유가 이것이다. 원칙 1이 코드 정책으로 박혀 있는 셈이다.

**원칙 2 — 모든 통신은 네트워크 위치와 무관하게 보호된다.** TLS다. HTTPS다. 그것도 외부 통신만이 아니라 서비스 간 통신까지. 9장에서 다뤘던 HSTS와 `X-Forwarded-Proto` 처리가 여기에 닿는다. Spring Security가 HTTPS를 직접 강제하지는 않지만, `requiresChannel(c -> c.anyRequest().requiresSecure())` 한 줄로 HTTP 요청을 HTTPS로 리다이렉트할 수 있다. 더 깊게 가면 서비스 메시(Istio·Linkerd) 영역으로 넘어가는데, 그건 본 책 범위 밖이다. 다만 좌표만 박아 두자 — Zero Trust가 말하는 "통신 보호"는 클라이언트-서버 한 단만이 아니라 백엔드 내부의 모든 hop까지 포함한다.

**원칙 3 — 리소스 접근은 세션 단위로 부여된다.** 여기가 흥미롭다. 한 번 로그인했다고 모든 자원에 무제한 접근을 주지 말라는 이야기다. "세션 단위"라는 게 우리가 흔히 쓰는 HTTP 세션 쿠키만 의미하는 게 아니다. NIST 문서 맥락에서 "session"은 "특정 자원에 대한 특정 시점의 접근 권한"에 가깝다. 즉, 같은 사용자라도 자원이 바뀌면 권한을 다시 평가해야 한다는 뜻이다. 우리 코드에서 이걸 가장 잘 구현한 자리가 바로 7장에서 다룬 MFA다. `factor.type=password`로 인증한 사용자가 `/admin/users` 자원에 접근하려는데, 그 자원이 `FACTOR_OTT`를 요구한다면 다시 OTT factor를 받아야 한다. 같은 세션 안에서도 자원에 따라 권한이 다르게 평가되는 것. 이게 원칙 3의 코드적 구현이다. `@EnableMultiFactorAuthentication`이 Zero Trust 원칙 3과 정확히 닿는다는 사실은 한 번 음미해 볼 가치가 있다.

**원칙 4 — 접근은 동적 정책에 따라 결정된다.** 이 원칙이 우리 책 5장과 가장 강하게 연결된다. "동적 정책"이라는 게 무슨 뜻인가? 주체의 신원만이 아니라, 디바이스의 상태, 자산의 위험도, 행동 패턴까지 종합해 매번 결정한다는 이야기다. 우리가 5장 후반에 다룬 **DPoP (RFC 9449)** 가 정확히 여기에 들어맞는다. Bearer 토큰이 단순히 "이 토큰을 들고 있는 자에게 접근 허용"이라면, DPoP는 "이 토큰 + 이 클라이언트 키 쌍을 함께 증명할 수 있는 자에게만 접근 허용"이다. 토큰을 누가 탈취해도 클라이언트 개인키 없이는 못 쓴다. 매 요청마다 `DPoP` 헤더(`htm`·`htu`·`iat`·`jti`·`ath`)를 검증해, 정적인 "토큰 소유"가 아니라 동적인 "키 소유 증명"으로 접근을 결정한다. mTLS도 비슷한 자리에 들어간다 — 클라이언트 인증서로 매 요청 신원을 동적 평가하는 방식이다. 둘 다 sender-constrained 토큰 패밀리에 속한다. 5장 5.9절에서 다뤘던 `cnf.jkt` JWK thumbprint 검증의 정확한 정당화가 여기에 있다 — Zero Trust 원칙 4가 코드로 박힌 형태가 DPoP다.

**원칙 5 — 자산의 보안 자세를 지속 모니터링한다.** 운영 영역이다. 14.5절의 관측·감사에서 본격적으로 다룬다. 짧게 좌표만 박자면, `AuthenticationSuccessEvent`/`AuthenticationFailureEvent`를 수집해 brute-force 탐지를 구성하는 것, JWK 회전 로그를 남기는 것, Actuator의 `health` endpoint를 모니터링 시스템에 연결하는 것이 모두 이 원칙의 코드적 구현이다.

**원칙 6 — 인증·인가는 접근 전에 동적이고 엄격하게 강제된다.** 이 원칙이 사실 우리 책 2~3장의 정확한 정당화다. `AuthorizationFilter`가 자원 핸들러보다 앞에 위치해 매 요청 권한을 평가한다는 점, `STATELESS` 세션 정책의 자원 서버가 매 요청마다 JWT 서명·발급자·만료를 검증한다는 점, `@PreAuthorize`가 메서드 호출 전에 SpEL을 평가한다는 점. 이 모든 게 "접근 전에 강제"의 구현이다. Spring Security의 필터 체인 구조 자체가 원칙 6을 보장하는 아키텍처다.

**원칙 7 — 조직은 자산·네트워크·통신 상태 정보를 최대한 많이 수집한다.** 다시 운영 영역이다. 감사 로그, 메트릭, 트레이싱. Spring Boot 4의 Actuator + Micrometer + OpenTelemetry 묶음이 이 원칙의 도구 셋이다.

이렇게 일곱 원칙을 우리 코드와 맞대 보면 한 가지가 또렷해진다. Spring Security 7로 평범하게 자원 서버 + OAuth2 Client + MFA를 구성하는 행위 자체가 이미 Zero Trust 일곱 원칙의 절반 이상을 자연스럽게 만족시킨다. 우리는 "Zero Trust 도입"이라는 거창한 프로젝트를 별도로 띄울 필요가 없다. 부족한 모서리만 채우면 된다. 그게 어느 모서리인지 정확히 가리는 게 이번 장의 목표다.

> **박스 — Zero Trust 7 tenets ↔ Spring Security 7 매핑**
>
> | 원칙 | 대응 Spring Security 부품 | 본 책 챕터 |
> |------|---------------------------|-----------|
> | 1. 모든 자원에 인증 | 필터 체인 기본 정책, `anyRequest().authenticated()` | 2장, 8장 |
> | 2. 위치 무관 통신 보호 | `requiresChannel`, HSTS, `X-Forwarded-Proto` | 9장 |
> | 3. 세션 단위 권한 | MFA factor, `@EnableMultiFactorAuthentication` | 7장 |
> | 4. 동적 정책 | DPoP(`cnf.jkt`), mTLS, `JwtAuthenticationConverter` 동적 권한 매핑 | 5장 |
> | 5. 지속 모니터링 | `AuthenticationEvent`, Actuator metrics | 14.5절 |
> | 6. 접근 전 강제 | `AuthorizationFilter`, `@PreAuthorize`, STATELESS 자원 서버 | 2장, 5장, 8장 |
> | 7. 정보 수집 | 감사 로그, Micrometer, OpenTelemetry | 14.5절 |

이 표가 14장의 척추다. 14.2 이후의 절들은 이 표의 빈자리(주로 5·7번 원칙)를 채우는 이야기로 흐른다.

### 14.1.1 DPoP가 원칙 4에 정확히 들어맞는 이유 (5장 cross-ref)

원칙 4 — "접근은 동적 정책에 따라 결정된다" — 를 한 단락 더 깊이 보고 가자. 5장에서 DPoP를 다룰 때는 "Bearer 토큰의 한계를 넘는 진화"라는 표현을 썼다. 그 표현을 Zero Trust 어휘로 다시 풀어 보면 이렇다. Bearer 토큰은 정적이다. 토큰 한 줄을 들고 있으면 누구나 쓸 수 있다는 게 "Bearer"의 정의다. 그런데 원칙 4가 요구하는 것은 동적 평가다. "지금 이 요청을 보내는 자가 이 토큰의 정당한 소유자인가?"를 매번 묻는 것. DPoP는 이 질문에 답한다. 매 요청마다 클라이언트가 자신의 개인키로 서명한 `DPoP` JWT 헤더를 함께 보내고, 자원 서버는 그 서명이 토큰의 `cnf.jkt`에 박힌 공개키와 일치하는지 검증한다. 토큰 + 키 쌍이 함께 증명되어야 자원 접근이 허용된다.

이 한 동작이 Zero Trust 원칙 4의 가장 작고 명확한 구현 사례다. "동적 정책"이라는 추상적 표현이 코드 두 줄(`OAuth2ResourceServerConfigurer.jwt(...)` + `DPoP` 검증) 안에 박힌다. 다만 한 가지 짚고 가자 — DPoP가 Zero Trust의 전부는 아니다. 디바이스 신원, 자산 상태, 행동 속성까지 종합 평가하는 본격 Zero Trust 정책 엔진(Open Policy Agent 같은 외부 시스템)을 도입하는 게 다음 단계다. 우리 책 범위는 거기까지 가지 않는다. 그러나 DPoP라는 한 발자국으로 우리가 이미 그 길의 입구에 서 있다는 사실은 분명하다.

## 14.2 BFF (Backend-for-Frontend) — SPA + OAuth2의 새 표준

자, 두 번째 큰 트렌드로 넘어가자. BFF다. 이름이 좀 추상적이라 처음 들으면 갸우뚱하게 되는데, 한 줄로 정리하면 이렇다.

> **BFF = 브라우저(SPA)와 외부 API/IdP 사이에 서서, 브라우저 대신 OAuth 클라이언트 역할을 해 주는 작은 백엔드.**

왜 이런 게 필요한가? 이 질문에 답하려면 우리가 5장과 6장에서 마주쳤던 두 가지 불편한 사실을 다시 떠올려야 한다.

첫째, **브라우저는 OAuth 클라이언트가 되기에 적합하지 않다.** 자바스크립트 코드는 모두 평문으로 노출되니까 client secret을 숨길 곳이 없다. PKCE가 그 빈자리를 메우긴 했지만, 그래도 토큰을 어디에 보관할지가 남는다. `localStorage`? XSS 한 번이면 끝이다 — 5장 7.2절 함정 7에서 본 그대로. `sessionStorage`도 마찬가지. 메모리에 보관? 페이지 리프레시 한 번에 사라진다. HttpOnly 쿠키? 도메인 분리된 SPA에선 전달이 까다롭다. 어느 쪽을 잡아도 한 번씩은 난감해진다.

둘째, **CSRF 보호가 어색해진다.** SPA가 직접 OAuth 클라이언트면 stateful 세션이 없으니까 CSRF 토큰을 발급할 자리가 없다. 결국 "API 호출이니까 CSRF disable"로 가게 되는데, 그러면 9장에서 다룬 stateful 흐름의 보호망이 사라진다.

이 두 가지 불편함을 한 방에 해결하는 패턴이 BFF다. 그림으로 그려 보자.

```
[브라우저(SPA)]
     ↓ (1) 같은 도메인의 BFF에 HTTP 호출
     ↓     세션 쿠키(HttpOnly·Secure·SameSite=Strict)만 들고 다님
     ↓     토큰은 쳐다보지도 않음
[BFF (Spring Cloud Gateway + Spring Security)]
     ↓ (2) 자기가 OAuth confidential client
     ↓     IdP에서 받은 access/refresh token을 서버 측에서 보관
     ↓     SPA에서 들어온 호출에 토큰을 자동 첨부해 IdP/자원 서버로 forward
[외부 IdP (Keycloak/Auth0/Google)] ←→ [자원 서버 (Spring Security oauth2ResourceServer)]
```

핵심을 다시 짚자.

- **브라우저는 OAuth 클라이언트가 아니다.** 토큰을 보지도 않는다.
- **브라우저는 BFF와 같은 도메인.** 그러므로 CORS 필요 없음. HttpOnly·SameSite 쿠키만으로 통신.
- **토큰은 서버 측 저장.** XSS로 새지 않는다.
- **CSRF 보호는 SameSite + custom header 이중 방어.** stateful 흐름이 살아 있으므로 9장의 CSRF 보호망이 그대로 적용된다.

이 패턴을 Curity 팀이 2021년에 "Token Handler Pattern"이라는 이름으로 정리했고, Duende가 같은 시기에 "BFF" 이름으로 정리했다. 둘 다 같은 모델이다. 그리고 Spring 진영에서는 Spring Cloud Gateway + Spring Security `oauth2Login`의 조합이 BFF 구현의 사실상 표준이 됐다.

### 14.2.1 Spring Cloud Gateway + `oauth2Login`으로 BFF를 짜 보자

코드 골격은 의외로 간단하다. 빌드 의존성에 `spring-cloud-starter-gateway`와 `spring-boot-starter-oauth2-client`를 함께 박고, 다음 구성을 올린다.

```java
@Configuration
@EnableWebFluxSecurity
class BffSecurityConfig {

    @Bean
    SecurityWebFilterChain bff(ServerHttpSecurity http,
                               ReactiveClientRegistrationRepository clients) {
        return http
            .authorizeExchange(a -> a
                .pathMatchers("/", "/index.html", "/static/**", "/login").permitAll()
                .anyExchange().authenticated())
            .oauth2Login(Customizer.withDefaults())
            .logout(l -> l.logoutSuccessHandler(
                new OidcClientInitiatedServerLogoutSuccessHandler(clients)))
            .csrf(csrf -> csrf.csrfTokenRepository(
                CookieServerCsrfTokenRepository.withHttpOnlyFalse()))
            .build();
    }
}
```

BFF는 보통 Reactive(WebFlux) 기반이다. 그래서 `ServerHttpSecurity`를 쓴다 — 11장에서 다룬 어휘다. 핵심 줄은 세 개다. `oauth2Login`이 외부 IdP와의 인증 흐름을 처리하고, `OidcClientInitiatedServerLogoutSuccessHandler`가 OIDC RP-initiated logout으로 IdP 세션까지 정리하고, `CookieServerCsrfTokenRepository.withHttpOnlyFalse()`가 SPA의 자바스크립트가 CSRF 토큰을 읽어 custom header(`X-XSRF-TOKEN`)로 첨부할 수 있도록 한다.

그런데 여기서 한 가지 짚어 둘 게 있다. **CSRF 보호가 BFF 시나리오에서 의외로 까다롭다.** Stateful 세션 흐름이 살아 있으니까 CSRF 토큰은 꼭 필요한데, SPA가 자바스크립트로 호출하니까 토큰을 어떻게 전달할지가 고민이다. 6.x 시절에는 위 코드처럼 `withHttpOnlyFalse()`를 명시적으로 박고, SPA 측 fetch 인터셉터에서 쿠키를 읽어 헤더에 다시 박는 보일러플레이트를 직접 짜야 했다. 그게 적잖이 번거로웠다. 그래서 누가 GitHub 이슈를 띄웠다.

> **Spring Security 이슈 [#14149](https://github.com/spring-projects/spring-security/issues/14149)** — "Simplify CSRF Configuration for SPAs"

이 이슈가 7.0에서 답을 얻었다. `http.csrf(CsrfConfigurer::spa)` 한 줄이다.

```java
return http
    .authorizeExchange(...)
    .oauth2Login(Customizer.withDefaults())
    .csrf(CsrfConfigurer::spa)   // ← 7.0의 한 줄
    .build();
```

이 한 줄이 무엇을 자동으로 해 주는가? `CookieCsrfTokenRepository.withHttpOnlyFalse()`, `XorCsrfTokenRequestAttributeHandler`, BFF 모드에 맞는 `CsrfTokenRequestHandler` 조합을 한 번에 박는다. 9장 9.3절에서 본 그대로다. SPA + BFF 구성에서 가장 흔히 틀리는 부분 — CSRF 토큰을 쿠키로 발급하면서도 헤더로 받아야 한다는 비대칭 — 이 한 줄로 표준화된다.

이 한 줄이 BFF 패턴 보급에 기여한 바를 우리는 좀 과소평가하기 쉽다. 하지만 솔직히 말해, 6.x 시절 BFF 한번 짜 본 사람이라면 안다. `withHttpOnlyFalse()`니 `CookieCsrfTokenRepository`니 하는 단어 조합을 검색하는 데만 한나절이 가던 시절이 있었다. 7.0의 한 줄은 그 한나절을 지운다. 작은 일 같지만 의미는 작지 않다.

### 14.2.2 BFF가 답하는 것, 답하지 못하는 것

BFF는 마법이 아니다. 솔직히 어떤 문제를 답하고 어떤 문제는 답하지 못하는지 짚어 보자.

**답하는 것:**
- 브라우저에서 토큰 보관 위치 문제 (서버 측으로 옮김)
- XSS로 인한 토큰 탈취 (브라우저에 토큰 자체가 없음)
- 도메인 분리된 SPA의 CORS 복잡성 (같은 도메인의 BFF로 호출)
- SPA의 CSRF 보호 (stateful 세션 + SameSite + custom header)

**답하지 못하는 것:**
- BFF 자체가 침해되면 모든 사용자의 토큰이 위험 (그래서 BFF 보안이 더 중요)
- 모바일 앱은 BFF 대상이 아니다 (모바일은 그냥 OAuth 네이티브 클라이언트로 가는 게 정석)
- 마이크로서비스 간 호출의 인증 (이건 자원 서버 + JWT가 풀 문제)

그러니까 BFF는 **SPA를 위한 패턴**이지 모든 클라이언트 유형의 답이 아니다. 모바일 앱이 있으면 모바일은 모바일대로 native OAuth + Authorization Code + PKCE로 가야 한다. 그리고 BFF 백엔드 자체의 보안 — Secret 관리, 토큰 회전, 침해 대응 — 은 별도로 챙겨야 한다. 그게 다음 절의 주제다.

> **요약 박스 — SPA 보안 결정 트리**
>
> - SPA가 모놀리식 백엔드와 같은 도메인? → 보통 세션 쿠키만으로 충분. BFF 없이도 됨.
> - SPA와 백엔드 도메인이 분리? + 외부 IdP 사용? → **BFF 강력 권장**.
> - 모바일 앱 + SPA 함께 운영? → 모바일은 native OAuth, SPA는 BFF. 두 트랙 별도 운영.
> - 마이크로서비스 간 호출? → BFF와 무관. JWT 자원 서버 + DPoP/mTLS.

## 14.3 Secret 회전·키 관리 — 운영의 첫 번째 모서리

Zero Trust 원칙과 BFF 패턴까지 좌표를 박았다. 이제 운영의 모서리들로 넘어가자. 첫 번째 모서리는 Secret이다.

Secret이 뭔지부터 분명히 하자. 시스템이 "비밀로 유지해야 정상 동작하는 값" 전부다. 우리 책 범위에서 보면 적어도 다음이 있다.

- JWT 서명 키 (대칭이면 HS256의 shared secret, 비대칭이면 RS256/ES256의 개인키)
- 패스워드 인코딩의 work factor와 salt
- OAuth2 client_secret
- DB credential
- 외부 API 키

이 값들이 노출되면 시스템이 사실상 무너진다. 그래서 두 가지가 모두 중요하다. **(1) 노출되지 않게 보관하기**, 그리고 **(2) 주기적으로 갈아 끼우기 (rotation)**. 둘 다 평소엔 신경을 덜 쓰다가 사고가 나야 그 중요성을 절감하게 된다. 그래서 더 찜찜한 영역이다. 끔찍한 일이다.

### 14.3.1 JWK 회전 — 키 한 짝을 갈아 끼우는 안전한 절차

JWT를 RS256/ES256 같은 비대칭 알고리즘으로 서명한다고 해 보자. IdP가 공개키를 JWKS endpoint(보통 `/.well-known/jwks.json`)로 노출하고, 자원 서버는 그걸 캐시해 두고 토큰 검증에 쓴다. 5장에서 본 그림이다. 그런데 개인키가 외부에 한 번 노출되면 어떻게 해야 할까?

가장 안전한 답은 **무중단으로 새 키 쌍을 추가하고, 옛 키 쌍을 점진적으로 폐기하는 것**이다. JWKS는 키 배열이다. 새 `kid`(key id)로 키 쌍을 하나 더 추가해도 기존 토큰의 검증이 깨지지 않는다. JWT 헤더의 `kid`가 옛 키를 가리키면 옛 공개키로, 새 키를 가리키면 새 공개키로 검증된다. 일정 기간 두 키를 함께 운영하다가 옛 토큰의 만료(보통 access token TTL인 15분~1시간)가 지나면 옛 키를 JWKS에서 제거한다.

자원 서버 측 코드에서 7.0이 제공하는 단축은 `NimbusJwtDecoder` + `JwkSourceBuilder`다.

```java
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder
        .withJwkSetUri("https://idp.example.com/.well-known/jwks.json")
        .cache(Duration.ofMinutes(5))         // JWKS 캐시 TTL
        .restOperations(restTemplate())       // 커스텀 timeout/retry 가능
        .build();
}
```

핵심은 두 가지다. **JWKS를 메모리에 캐시하되 TTL을 둔다.** 너무 길면 회전이 늦게 반영되고, 너무 짧으면 IdP에 부하가 간다. 보통 5~15분이 균형점이다. 그리고 **JWKS endpoint 호출 실패를 우아하게 처리한다.** IdP가 잠시 다운돼도 캐시된 키로 계속 검증할 수 있게 timeout과 retry를 명시적으로 설정해 두자. 기본값으로 두면 첫 호출 실패가 그대로 자원 서버 다운으로 이어지는 경우가 있다.

회전 운영을 자동화하려면 IdP 측에서 cron 스케줄로 새 키를 발급하고 JWKS에 추가하는 작업이 필요한데, Spring Authorization Server는 7.0에서 이걸 직접 지원한다. 외부 IdP(Keycloak·Auth0)는 콘솔에서 회전 주기를 설정하면 된다. Spring Security 측은 그 변화를 자동으로 따라가도록 위 코드만 정확히 짜 두면 된다. 한 번 짜 두면 운영자가 손을 댈 일이 거의 없다 — 이게 표준의 힘이다.

### 14.3.2 BCrypt 12 → Argon2id로 옮겨 가는 의미

다음으로 패스워드. 7.0에서 추가된 Password4j 기반 인코더 다섯 개 — `Argon2Password4jPasswordEncoder`, `ScryptPassword4jPasswordEncoder`, `BCryptPassword4jPasswordEncoder`, `PBKDF2Password4jPasswordEncoder`, `BalloonHashingPassword4jPasswordEncoder` — 가 1장에서 큰 그림으로 짚었던 변화다. 그중 가장 권장되는 게 Argon2id다.

왜 옮겨 가는가? 한 줄로 답하면 — **BCrypt가 GPU 공격에 약하다.** BCrypt는 2000년 전후로 표준이 됐고, 그때 기준으로는 충분히 안전했다. work factor 10~12면 단일 CPU에서 검증에 100ms~300ms가 걸렸다. 그런데 2020년대 들어 GPU/ASIC을 동원하면 BCrypt 12의 무차별 대입 속도가 초당 수천~수만 번에 도달한다. Argon2id는 메모리 hard 함수다. 검증할 때 일정량의 메모리(예: 64MB)를 점유해야 해서 GPU 병렬화의 이점이 크게 줄어든다. OWASP가 2021년부터 Argon2id를 1순위 권장 알고리즘으로 올린 이유다.

전환은 점진적으로 한다. Spring Security의 `DelegatingPasswordEncoder`가 prefix(`{bcrypt}`, `{argon2}`)로 알고리즘을 구분하기 때문에, 기존 BCrypt 해시를 그대로 두고 새로 등록되는 사용자만 Argon2id로 인코딩해도 시스템이 자연스럽게 굴러간다. 로그인 성공 시점에 옛 해시를 재인코딩해 점진적으로 갈아 끼우는 패턴도 표준이다 (`PasswordEncoder.upgradeEncoding(encodedPassword)`로 판단).

```java
@Bean
PasswordEncoder passwordEncoder() {
    String idForEncode = "argon2";
    Map<String, PasswordEncoder> encoders = new HashMap<>();
    encoders.put("argon2", new Argon2Password4jPasswordEncoder());
    encoders.put("bcrypt", new BCryptPasswordEncoder(12));
    encoders.put("pbkdf2", new Pbkdf2PasswordEncoder("", 16, 310_000, SHA256));
    return new DelegatingPasswordEncoder(idForEncode, encoders);
}
```

이 코드 한 번 박아 두면 신규 사용자는 자동으로 Argon2id로 가고, 기존 BCrypt 사용자도 검증은 그대로 된다. 점진 마이그레이션이 깔끔하게 굴러간다.

### 14.3.3 application.yml에 평문은 절대 두지 말자 — Vault 패턴

마지막으로 한 가지만 더. 운영 코드베이스에서 자주 보이는 안티 패턴이 있다.

```yaml
# application.yml — 절대 이렇게 두지 말자
spring:
  datasource:
    password: SuperSecret123!
  security:
    oauth2:
      client:
        registration:
          google:
            client-secret: abc-xyz-secret
```

이게 왜 문제인가? 평문 secret이 소스 코드 저장소에 들어간다. Git 히스토리에 박혀서 한 번 커밋되면 사실상 영구히 노출된다. 더 큰 문제는 다음 절의 Actuator 사고로 이어진다 — Actuator `env` endpoint가 한 번 노출되면 이 평문이 그대로 외부에 뿌려진다.

해법은 외부 secret store다. 가장 표준적인 조합은 **Spring Cloud Config + HashiCorp Vault**다. 또는 AWS Secrets Manager, Azure Key Vault, GCP Secret Manager 같은 클라우드 네이티브 서비스도 있다. 어느 쪽이든 핵심 원칙은 동일하다 — **application.yml에는 secret store의 참조만, 실제 값은 런타임에 안전하게 주입.** Spring Boot의 `${...}` placeholder가 환경 변수, Vault, K8s Secret 어디든 동일한 문법으로 받아 준다.

이 한 가지 원칙을 운영 첫날부터 박아 두자. "나중에 옮기겠다"는 평문 secret은 거의 영원히 그 자리에 있다. 그리고 어느 날 사고가 난다.

## 14.4 Actuator 안전 운영 — 찜찜한 endpoint 하나가 모든 보안을 무너뜨릴 수 있다

Secret 이야기의 자연스러운 다음 단계가 Actuator다. 한국 개발자라면 우아한형제들 기술블로그의 "Security Actuator 안전하게 사용하기" 글을 한 번쯤 봤거나 들었을 것이다 ([techblog.woowahan.com/9232](https://techblog.woowahan.com/9232/)). 그 글이 정리하는 핵심을 한 줄로 옮기면 이렇다 — **Actuator는 개발자에게 편리하지만, 잘못 노출하면 매우 위험하다.**

Spring Boot Actuator는 개발 편의 도구다. `/actuator/health`로 상태를 보고, `/actuator/metrics`로 메트릭을 빼내고, `/actuator/env`로 설정값을 검사하고, `/actuator/heapdump`로 힙 덤프를 받는다. 운영 중에 한 번 갖다 쓰면 정말 편한 도구들이다. 그런데 이 endpoint들이 외부에 노출되면 어떻게 되는가?

- `/actuator/env` → application.yml의 모든 설정값(DB password 평문 포함) 노출
- `/actuator/heapdump` → 메모리 덤프 통째로 노출. 그 안에 평문 토큰·세션·비밀번호가 모두 들어 있음
- `/actuator/configprops` → 모든 `@ConfigurationProperties` 값 노출
- `/actuator/threaddump` → 실행 중인 스레드 정보. 토큰이 메서드 파라미터에 박혀 있으면 함께 노출

한 번 노출되면 그 자체가 사고다. 우아한형제들 글에 정리된 실제 사례를 보자. "잘못 쓰면 매우 위험하다"는 말은 과장이 아니다. 노출된 `env` endpoint에서 DB credential을 추출한 공격자가 DB에 직접 접속한 사례, heap dump에서 active session token을 추출해 다른 사용자로 가장한 사례. 모두 운영에서 실제로 일어났다.

### 14.4.1 Actuator 노출 정책 — 최소 권한의 원칙

Spring Boot 3 이후의 기본값은 사실 꽤 안전하다. `management.endpoints.web.exposure.include`의 기본값이 `health` 하나뿐이다. 즉, 별도 설정 없이는 `/actuator/health`만 노출되고 나머지는 모두 차단된다. 그런데 운영에서 모니터링 도구가 메트릭을 빼내야 한다거나 디버깅이 필요하다며 `*`로 풀어 두는 경우가 있다. 이게 사고의 시작이다.

권장 패턴은 이렇다.

```yaml
# application.yml — 외부 노출용 (운영)
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus   # 꼭 필요한 것만
        exclude: env,beans,configprops,heapdump,threaddump
  endpoint:
    health:
      show-details: when-authorized       # 인증된 사용자에게만 상세 노출
      show-components: when-authorized
```

원칙은 단순하다. **노출 목록은 include로 명시적으로 켠다. exclude는 안전망.** `*`는 절대 쓰지 말자. 그리고 `health.show-details`도 기본값 `never` 또는 `when-authorized`로 두자. `always`는 데이터센터 IP 정보까지 노출하는 경우가 있다.

### 14.4.2 별도 SecurityFilterChain으로 Actuator 격리

한 발 더 나간 패턴은 Actuator를 **별도 `SecurityFilterChain`으로 격리**하는 것이다. 2장에서 본 두 개의 체인 패턴이 여기서 다시 빛난다.

```java
@Configuration
@EnableWebSecurity
class ActuatorSecurityConfig {

    @Bean
    @Order(1)   // 먼저 매칭
    SecurityFilterChain actuator(HttpSecurity http) throws Exception {
        return http
            .securityMatcher("/actuator/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers("/actuator/health", "/actuator/info").permitAll()
                .anyRequest().hasRole("OPS"))
            .httpBasic(Customizer.withDefaults())
            .csrf(CsrfConfigurer::disable)   // Actuator는 stateless
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .build();
    }

    @Bean
    @Order(2)
    SecurityFilterChain app(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(a -> a.anyRequest().authenticated())
            .oauth2Login(Customizer.withDefaults())
            .build();
    }
}
```

이 패턴의 장점은 명료하다. **Actuator 경로는 일반 사용자 인증과 완전히 분리된 별도 정책으로 굴러간다.** `ROLE_OPS`를 가진 운영자만 접근 가능, HTTP Basic으로 SRE 도구가 직접 호출 가능, 세션 없음, CSRF 없음. 그리고 일반 사용자가 어떤 OIDC 흐름으로 로그인하든 Actuator 경로는 완전히 격리된다.

추가로, **별도 포트로 노출하는 것**도 강력한 패턴이다.

```yaml
management:
  server:
    port: 9001    # 운영 전용 포트
    address: 127.0.0.1   # 외부 인터페이스에 바인딩 안 함
```

이렇게 두면 외부 LB가 9001 포트로는 트래픽을 보내지 않고, 내부 모니터링 시스템이나 SRE의 SSH 터널을 통해서만 접근 가능하다. 이게 가장 안전한 모델이다. "기본 격리 + 인증 격리"의 이중 방어.

이런 식으로 한 번 분리해 두면, 일반 비즈니스 코드의 보안 정책이 바뀌어도 Actuator 정책은 영향을 받지 않는다. 그리고 그 반대도 마찬가지. 운영팀이 새 메트릭 endpoint를 켜고 싶다고 비즈니스 보안에 손댈 일이 없다. 운영의 안정성은 결국 이런 모서리들에서 결정된다.

## 14.5 관측·감사 — 누가 언제 무엇을 했는가

Zero Trust 원칙 5와 7 — 지속 모니터링과 정보 수집 — 이 운영 영역에서 구체화되는 곳이 관측과 감사다. Spring Security가 이걸 위해 명시적으로 제공하는 것이 **인증 이벤트**다.

### 14.5.1 `AuthenticationSuccessEvent` / `AuthenticationFailureEvent`

`AuthenticationManager`가 인증을 처리할 때마다 Spring `ApplicationEventPublisher`로 이벤트를 던진다. 두 종류가 핵심이다.

- `AuthenticationSuccessEvent` — 인증 성공
- `AbstractAuthenticationFailureEvent`의 하위 — `BadCredentialsException`, `UsernameNotFoundException`, `LockedException` 등 각 실패 사유별로 세분화된 이벤트

이걸 `@EventListener`로 받아서 감사 로그에 쌓는 게 가장 깔끔한 패턴이다.

```java
@Component
class AuthenticationAuditListener {

    private static final Logger log = LoggerFactory.getLogger("AUDIT");

    @EventListener
    void onSuccess(AuthenticationSuccessEvent event) {
        Authentication auth = event.getAuthentication();
        log.info("AUTH_SUCCESS user={} authorities={} timestamp={}",
            auth.getName(),
            auth.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList(),
            Instant.now());
    }

    @EventListener
    void onFailure(AbstractAuthenticationFailureEvent event) {
        Authentication auth = event.getAuthentication();
        log.warn("AUTH_FAILURE user={} reason={} timestamp={}",
            auth != null ? auth.getName() : "unknown",
            event.getException().getClass().getSimpleName(),
            Instant.now());
    }
}
```

이 한 컴포넌트가 박혀 있으면 모든 인증 시도가 `AUDIT` 로그에 남는다. 운영팀의 SIEM(Security Information and Event Management) 시스템이 이 로그를 흡수해 알람을 만들 수 있다.

### 14.5.2 Brute-force 탐지 — 실패 이벤트 카운트로 한 단계 더

실패 이벤트를 단순히 로그로만 남기지 말고, **카운트해서 임계치를 넘으면 차단**까지 가는 게 한 단계 더 나간 패턴이다. 가장 단순한 구현은 in-memory 카운터 + 일정 시간 슬라이딩 윈도우다.

```java
@Component
class BruteForceProtection {

    private final Cache<String, AtomicInteger> failures =
        Caffeine.newBuilder()
            .expireAfterWrite(Duration.ofMinutes(15))
            .build();

    @EventListener
    void onFailure(AbstractAuthenticationFailureEvent event) {
        String username = event.getAuthentication().getName();
        int count = failures.get(username, k -> new AtomicInteger()).incrementAndGet();
        if (count >= 5) {
            // 외부 IdP API 호출 또는 로컬 DB의 user.locked 플래그를 set
            lockUser(username);
        }
    }

    @EventListener
    void onSuccess(AuthenticationSuccessEvent event) {
        failures.invalidate(event.getAuthentication().getName());
    }
}
```

15분 안에 5번 실패하면 잠근다. 성공하면 카운터 리셋. 단순하지만 효과적이다. 분산 환경이면 Caffeine 캐시 자리를 Redis로 바꾸면 된다. 더 정교한 정책 — IP 기반, 디바이스 핑거프린트 — 으로 확장하려면 별도 보안 미들웨어(reCAPTCHA·Cloudflare Bot Management)와 결합하는 게 자연스럽다. 다만 시작은 위 코드 한 컴포넌트면 충분하다. 첫 안전망부터 깔자.

### 14.5.3 감사 로그 패턴 — 인증을 넘어 인가까지

인증 이벤트만이 아니라 **권한 거부 사건도 감사에 남기는 것**이 좋다. `AccessDeniedException`이 발생하는 자리에 hook을 박자. 8장에서 다룬 `AccessDeniedHandler`가 가장 자연스러운 자리다.

```java
@Component
class AuditingAccessDeniedHandler implements AccessDeniedHandler {

    private static final Logger log = LoggerFactory.getLogger("AUDIT");

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response,
                       AccessDeniedException denied) throws IOException {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        log.warn("ACCESS_DENIED user={} method={} path={} authorities={}",
            auth != null ? auth.getName() : "anonymous",
            request.getMethod(),
            request.getRequestURI(),
            auth != null ? auth.getAuthorities() : List.of());
        // 그 다음 ProblemDetail로 403 응답 (8장 8.8절 참조)
        response.setStatus(HttpStatus.FORBIDDEN.value());
        response.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
        new ObjectMapper().writeValue(response.getOutputStream(),
            ProblemDetail.forStatusAndDetail(FORBIDDEN, "Access denied"));
    }
}
```

이 한 컴포넌트로 모든 권한 거부가 감사 로그에 남는다. 어떤 사용자가 어떤 자원을 어떻게 시도했는지 — 사고 발생 시 가장 먼저 보고 싶은 정보가 자동으로 쌓인다. 그리고 8장에서 짠 `AccessDeniedHandler` 자리에 자연스럽게 들어간다. 별도 인프라가 아니다.

## 14.6 책 전체를 가로지른 논쟁점들 — 정답이 하나가 아닌 결정들

자, 이제 14장의 마지막 절이다. 책을 읽어 오면서 곳곳에서 마주친 논쟁점들이 있다. 5장의 JWT 함정 박스, 7장의 MFA factor 정책, 9장의 CSRF disable 결정. 매번 "이건 시스템 맥락에 따라 다르다"고 말하고 미뤘던 결정들이다. 그 결정들을 한자리에 모아 정리하자. 답은 여전히 하나가 아니다. 다만 **각 답이 어떤 맥락에서 정답이 되는지**를 또렷이 가리는 게 이 절의 목표다.

### 14.6.1 JWT vs Session — 새 합의는 "둘 다 쓴다"로 수렴한다

가장 오래된 논쟁이다. DZone에 실린 한 글이 한 시대를 대변한다 — "Stop Using JWTs as Session Tokens" ([dzone.com](https://dzone.com/articles/stop-using-jwts-as-session-tokens)). 한 GitHub gist에서는 더 직설적이다 — "단순한 세션 토큰 용도의 JWT는 정규 세션 쿠키보다 비효율적이고 덜 유연하며, 얻는 이점도 없다" ([samsch gist](https://gist.github.com/samsch/0d1f3d3b4745d778f78b230cf6061452)). 이 의견의 핵심 논거는 5장 함정 6에서 짚었던 그것이다. **JWT는 강제 로그아웃이 어렵고, 권한 변경이 즉시 반영되지 않는다.** 자체 발급한 토큰을 외부에서 만료시키려면 별도 blacklist 캐시가 필요한데, 그러면 사실상 세션 저장소가 다시 등장한다.

반대편 의견도 있다. 마이크로서비스 환경에서는 stateless의 가치가 크다. 자원 서버가 토큰 검증을 위해 IdP에 매번 묻는 게 아니라 JWKS 캐시만으로 즉시 검증할 수 있다는 점, 서비스 간 호출에서 토큰을 자연스럽게 forward할 수 있다는 점. 이건 세션 모델로는 어렵다.

새로 형성되고 있는 합의는 이렇다. **브라우저 ↔ BFF 사이는 세션 쿠키, BFF ↔ 자원 서버 사이는 JWT.** 이 한 줄이 두 진영의 강점을 모두 살린다. 브라우저는 stateful 세션 보호망(CSRF·SameSite·HttpOnly)을 그대로 누리고, 백엔드 서비스 간은 stateless JWT의 확장성을 누린다. 14.2절의 BFF 패턴이 사실상 이 합의의 코드적 구현이다.

그러니 "JWT를 쓸까 세션을 쓸까?"라는 질문 자체가 잘못 던져진 질문일 수 있다. 정확한 질문은 "어디에 JWT를, 어디에 세션을 쓸까?"다. 그리고 본 책의 답은 — 브라우저 측은 세션, 서비스 간은 JWT, 둘을 잇는 BFF가 변환 계층.

### 14.6.2 Spring Authorization Server 직접 운영 vs 외부 IdP

이 결정은 운영 능력의 문제다.

Spring Authorization Server가 7.0에 흡수되면서 운영 부담이 크게 줄었다. 같은 릴리스 사이클을 타니까 버전 충돌이 없고, 같은 Spring Security 어휘로 설정할 수 있다. 그런데도 여전히 외부 IdaaS(Auth0, Okta, Keycloak, Authentik)를 쓰는 게 일반적 best practice다. 이유가 있다.

**자체 운영의 부담:**
- JWK 회전 운영 (자동화 가능하지만 첫 셋업이 무겁다)
- 사용자 디렉토리 관리, 비밀번호 재설정 흐름
- MFA factor 발급·관리
- SOC 2, ISO 27001 같은 컴플라이언스 감사
- 24/7 가용성 보장

**외부 IdaaS의 가치:**
- 위 항목 전부를 벤더가 책임
- 새 표준(OAuth 2.1, FAPI 2.0, OpenID4VC) 대응이 자동
- 보안 사고 시 책임 분담

언제 자체 운영이 맞는가? 외부 IdaaS에 사용자 데이터를 맡기기 곤란한 경우(정부·금융·헬스케어 일부 시나리오), 또는 사용자가 1만 명을 훨씬 넘어 외부 IdaaS 라이선스 비용이 자체 운영 비용을 넘는 경우. 그 외의 90%는 외부 IdaaS가 답이다.

본 책의 권고는 명확하다 — **운영팀이 키 관리·디렉토리 운영·컴플라이언스 감사를 모두 떠맡을 자신이 있는 게 아니라면, 외부 IdaaS를 쓰자.** Spring Security는 OAuth2 Client 측에서 외부 IdaaS와 너무 잘 통합되므로 그쪽 길이 정석에 가깝다.

### 14.6.3 localStorage vs Cookie — 다시 한 번

이 논쟁은 사실 14.2의 BFF 절에서 거의 답이 나왔다. 그러나 다시 한 번 정리하자.

**localStorage:**
- XSS 한 번이면 토큰 탈취. 5장 함정 7.
- 도메인 분리된 SPA에서 쿠키 전달이 까다로울 때 일부 팀이 채택.
- 본 책 권고: **피해야 한다.**

**HttpOnly Cookie:**
- 자바스크립트로 읽을 수 없으니 XSS 안전망 한 겹.
- CSRF 보호 필요 (SameSite + custom header).
- 같은 도메인 또는 BFF가 있으면 자연스럽게 동작.
- 본 책 권고: **기본값.**

**in-memory + refresh:**
- 토큰을 메모리에만 보관. 페이지 리프레시 시 silent refresh.
- 도메인 분리 + 쿠키가 어려운 환경의 차선.
- 본 책 권고: **HttpOnly 쿠키가 불가능한 경우의 차선.**

OWASP·Auth0·Curity·NIST가 모두 HttpOnly 쿠키를 1순위로 권고한다. 본 책도 동의한다. localStorage는 마지막 선택지로 두자.

### 14.6.4 보안과 사용성의 끝없는 줄다리기

이 절의 결론이자 책의 결론에 가까운 한 단락이다.

읽다 보면 느꼈을 것이다. 보안 결정의 거의 모든 자리에서 한쪽에는 "더 안전하게"가, 반대편에는 "더 편하게"가 서 있다. MFA factor를 추가하면 보안은 올라가는데 로그인 단계가 늘어난다. 세션 TTL을 짧게 잡으면 토큰 탈취 시 노출 시간이 줄지만 사용자는 자주 다시 로그인해야 한다. CSP를 빡빡하게 잡으면 XSS 보호가 단단해지지만 외부 분석 도구나 위젯이 깨진다. DPoP를 도입하면 sender-constrained 토큰의 안전성을 얻지만 클라이언트 구현 복잡도가 올라간다.

정답은 하나가 아니다. 그러나 한 가지 원칙은 있다. **사용자 경험을 일정 수준 깎으면서까지 지켜야 할 자산이 무엇인가를 먼저 정하자.** 일반 SaaS의 로그인이라면 비밀번호 + OTP 2 factor면 충분할 수 있다. 금융 서비스라면 Passkeys + 디바이스 바인딩까지 가야 한다. 정부 시스템이라면 mTLS + 하드웨어 토큰까지. 자산의 가치가 곧 보안의 깊이를 정한다.

그리고 그 깊이를 한 번에 다 박지 말자. 점진적으로 가는 게 낫다. BFF + 세션 쿠키 + HttpOnly로 시작해, 운영 데이터가 쌓이면 MFA를 더하고, 그 다음 DPoP를 더하고. Spring Security 7은 이 단계적 진화의 각 단계에 맞는 부품을 빠짐없이 제공한다. 그게 우리가 14장 첫머리에서 박은 명제 — "Zero Trust는 원칙이지 제품이 아니다" — 의 진짜 의미다.

> **좌표 박스 — K8s Service Mesh / mTLS와의 관계**
>
> 본 책 범위 밖이지만 한 번 좌표만 박아 두자. Istio·Linkerd·Cilium 같은 Service Mesh는 sidecar(Envoy)로 서비스 간 트래픽을 가로채 mTLS로 자동 암호화·인증한다. Zero Trust 원칙 2(위치 무관 통신 보호)의 가장 강력한 구현이다. Spring Security 7은 이 영역과 직접 부딪히지 않는다 — mTLS는 sidecar가, JWT 자원 서버는 애플리케이션이 책임진다. 그리고 sender-constrained 토큰의 표준은 DPoP만 있는 게 아니다. RFC 8705(OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens)가 mTLS 인증서 기반 토큰 바인딩을 표준화했다. Spring Security 7도 자원 서버 측에서 `cnf.x5t#S256` 검증으로 지원 가능. FAPI 2.0 같은 고보안 환경에서는 DPoP보다 mTLS-bound가 더 흔하다. 본격 도입은 다른 책의 몫이다.

## 14장 핵심 5줄 요약

1. **Zero Trust는 원칙이지 제품이 아니다.** NIST SP 800-207의 7 tenets 각각이 Spring Security 7의 부품(필터 체인, `AuthorizationManager`, MFA, DPoP, STATELESS 자원 서버, 인증 이벤트)에 직접 매핑된다.
2. **BFF가 SPA + OAuth2의 새 표준이다.** 브라우저는 OAuth 클라이언트가 아니다. HttpOnly 세션 쿠키만. `http.csrf(CsrfConfigurer::spa)` 한 줄이 7.0의 BFF 코드를 단순화했다.
3. **Secret은 외부 저장소에. application.yml에 평문 금지.** JWK는 무중단으로 회전. 패스워드는 BCrypt 12에서 Argon2id로 점진 이행.
4. **Actuator는 별도 `SecurityFilterChain`으로 격리.** 노출 목록은 include로 명시. `*`는 절대 쓰지 말자. 가능하면 별도 포트(`management.server.port`)로.
5. **모든 결정에 정답은 하나가 아니다.** JWT vs 세션, 자체 IdP vs 외부, localStorage vs Cookie — 답은 시스템 맥락이 정한다. 본 책 권고: 브라우저는 세션, 서비스 간은 JWT, 외부 IdaaS 우선, HttpOnly 쿠키 기본.

## 다음 챕터에서 답할 것

그래서 이 모든 결정을 한 프로젝트에서 어떻게 합치는가? 한 권의 책에서 우리가 만난 부품들 — 두 개의 `SecurityFilterChain`, OAuth2 Login + PKCE, JWT 자원 서버 + DPoP, MFA, BFF의 CSRF·CORS·CSP, 12장의 회귀 테스트, 14장의 감사 로그와 키 회전 — 을 한 프로젝트에 모두 합쳐 빌드한다면 어떻게 짜이는가?

마지막 챕터는 통합 워크스루다. 모놀리식 백엔드(Spring Boot 4) + SPA(React) + 외부 IdP(Keycloak) + BFF(Spring Cloud Gateway) 조합으로, 처음부터 끝까지 한 시나리오를 끝까지 빌드한다. 이 책을 덮고 나면 자기 프로젝트에 무엇을 만들 수 있는지의 구체적 증명이 거기에 있다. 한 권을 한 시나리오로 합치는 길로 함께 가 보자.
