# 15장. 한 권을 한 시나리오로 — 통합 실전 워크스루

> 선행 필요: 1~14장 전부. 책의 출구 챕터.

여행이 끝나간다. 1장에서 빨갛게 변한 빌드 화면을 같이 들여다본 게 엊그제 같은데, 그 사이 우리는 필터 체인 한 줄씩을 헤집었고, JWT의 `cnf.jkt` 클레임이 무엇을 의미하는지 알아냈고, OAuth2 Authorization Code 흐름의 다섯 박스를 그렸고, Passkeys ceremony 두 가지를 따라 그렸고, MFA의 factor가 사실 권한이라는 사실에 잠시 멈춰 섰고, 인가의 다섯 층을 줄지어 늘어놓았으며, 마침내 BFF라는 패턴 앞에서 "그래서 우리 SPA는 어떻게 해야 하지?"라는 물음에 답을 마련했다.

그런데 솔직히 말해 보자. 한 챕터씩 떼어서 볼 때는 명료하던 그림이, 한 프로젝트 안에 다 합쳐 놓으려고 보면 다시 흐릿해진다. 자주 일어나는 일이다. 인증과 인가, 클라이언트와 자원 서버, 세션과 토큰, BFF와 SPA — 이 어휘들이 한 시스템 안에서 어떻게 손을 잡는지, 그 손목 위로 어떤 헤더가 흐르고 어떤 쿠키가 오가는지를 한눈에 보지 못하면 책을 덮은 뒤에도 한참 헤매게 된다. 그래서 마지막 한 챕터를, 책 전체를 한 시나리오로 묶는 데 쓰기로 했다.

## 15.1 ShopVault — 한 권을 통과시킬 한 가게

상상해 보자. 우리가 새로 맡은 서비스 이름은 **ShopVault**다. 작지만 만만치는 않은 온라인 상점이다. 일반 사용자는 상품을 보고, 장바구니에 담고, 주문하고, 결제한다. 운영 측은 별도의 관리자 대시보드로 주문을 처리하고, 재고를 조정하며, 가끔은 환불 같은 민감한 작업을 한다. 외부에서 결제를 처리할 게이트웨이 한 곳과도 OAuth2로 묶여 있다. 그리고 인증·인가의 신원 서버는 회사가 외부에 운영하는 Keycloak 한 대.

지나치게 친근한 시나리오 아닌가? 이 책을 읽는 한국 개발자라면, 이름만 바꾸면 사실 자기 팀에서 한 번쯤 마주친 그림일 것이다. 그래서 골랐다. 새로움이 아니라 익숙함이 이번 장의 무기다. 익숙한 풍경 위에 7.0의 어휘들을 한 줄씩 덧그려 보자는 거다.

ShopVault의 구성 요소를 풀어 보면 이렇다.

- **shop-web** — React SPA. 일반 사용자도 보고, 관리자도 본다. 한 도메인 `app.shopvault.com` 아래에서 서비스된다.
- **shop-bff** — Spring Cloud Gateway 기반의 BFF. `app.shopvault.com`이 실제로 가리키는 첫 번째 서버다. SPA 정적 자원을 내려주고, `/api/**`로 들어오는 요청을 자원 서버로 fan out한다. OAuth2 confidential client 역할을 맡는다.
- **shop-api** — Spring Boot 4.0 모놀리식 백엔드. JWT Bearer + DPoP 자원 서버다. `api.shopvault.com` 도메인으로 직접 접근도 가능하지만, 브라우저는 BFF를 통해서만 닿는다.
- **shop-keycloak** — Keycloak 25.x 한 대. `auth.shopvault.com` 도메인. realm 한 개(`shopvault`), 클라이언트 두 개(`shopvault-bff` confidential, `shopvault-api` 자원 서버), 외부 결제 게이트웨이용 클라이언트(`shopvault-payment-client`) 한 개.
- **payment-gateway** — 외부 결제사 OAuth2 자원 서버. 우리는 client credentials grant로 access token을 받아 호출한다.

이 다섯 조각이 우리 시나리오의 전부다. 한 페이지짜리 아키텍처 그림으로 박아 두자.

```
                          ┌──────────────────────────────┐
                          │      shop-keycloak           │
                          │      (auth.shopvault.com)    │
                          │ realm: shopvault             │
                          │ clients: bff / api / payment │
                          └───┬────────────┬─────────────┘
                              │            │
              Auth Code+PKCE  │            │ JWKs
                              │            │ (issuer-uri discovery)
                              │            │
            ┌─────────────────▼────────┐   │
            │     shop-bff             │   │
 Browser ───▶ Spring Cloud Gateway     │   │
 (HttpOnly  │ oauth2Login (confidential)│  │
  Session   │ HttpOnly Session Cookie  │   │
  Cookie)   │ csrf(spa)                │   │
            │ token-relay filter       │   │
            └───────────┬──────────────┘   │
                        │                  │
              Bearer +  │                  │
              DPoP      ▼                  │
            ┌──────────────────────────┐   │
            │     shop-api             │◀──┘
            │ Spring Boot 4 / Sec 7    │
            │  ┌────────────────────┐  │
            │  │ FilterChain @Order(1) /actuator/** (no auth, isolated port)
            │  │ FilterChain @Order(2) /api/** (oauth2ResourceServer.jwt + DPoP)
            │  └────────────────────┘  │
            │ MFA factor authorities    │
            │ @PreAuthorize on services │
            └───────────┬──────────────┘
                        │
                        │ @HttpExchange + @ClientRegistrationId("payment")
                        │ (client_credentials, access token auto-injected)
                        ▼
            ┌──────────────────────────┐
            │   payment-gateway        │
            │   (외부 OAuth2 자원 서버) │
            └──────────────────────────┘
```

이 그림 한 장에 책의 거의 모든 어휘가 들어 있다. 필터 체인은 2장, 컴포넌트 위임은 3장, OAuth2 Client는 6장, 자원 서버와 DPoP는 5장, 세션·쿠키는 10장, CSRF SPA 모드는 9장, MFA factor 권한은 7장, 메서드 보안은 8장, BFF 패턴은 14장. 한 챕터씩 떼어 보던 어휘가, 한 시스템 안에서 어떤 자리에 들어가 어떤 이웃과 손을 잡는지를 이 그림이 정직하게 보여 준다.

이 장의 흐름은 이렇게 잡았다. 먼저 Keycloak 쪽 설정을 짚는다(15.2). 그다음 BFF 한 덩어리를 빌드한다(15.3). 그다음 자원 서버 `shop-api`를 두 개의 `SecurityFilterChain`으로 분리해 짜고(15.4), 메서드 보안과 MFA를 거기 얹는다(15.5, 15.6). 그다음 세 가지 인증 흐름 — 일반 사용자 로그인(15.7), 관리자 MFA 로그인(15.8), SPA → BFF → API 호출(15.9) — 을 시퀀스로 따라간다. 마지막으로 외부 결제 게이트웨이 호출(15.10)과 운영 체크리스트(15.11), 그리고 14개 챕터의 어휘가 어떻게 이 한 시스템에 다 녹았는지 회고하는 단(15.12)으로 마무리한다.

> **시그니처 변동 가능성에 대한 한 마디 (다시).** 이 장의 코드는 모두 Spring Security 7.0 GA(2025-11-17) 기준이다. 7.1.x milestone 단계에서 `AuthorizationManagerFactory`, `@EnableMultiFactorAuthentication` 같은 신규 API의 시그니처가 미세하게 다듬어질 가능성이 있다. 본문 코드를 그대로 옮겨 빌드가 살짝 어긋난다면, 7.0 GA로 의존성을 고정하거나 출간 시점의 공식 docs를 한 번 더 확인하는 편이 낫다. 이 책의 1장과 13장에서 같은 당부를 했지만, 마지막 장에서 한 번 더 짚어 둔다.

## 15.2 Keycloak 한 realm, 세 클라이언트

이 장은 Keycloak 설정 가이드가 아니다. 그러나 클라이언트 세 개의 정체와 권한 모델만큼은 한 번 정리해 두지 않으면, 뒤따라 나올 BFF·자원 서버 코드의 클레임 처리가 공중에 뜬다. 짧게만 짚자.

realm 이름은 `shopvault`. 그 안에 클라이언트를 세 개 만든다.

**클라이언트 1: `shopvault-bff` (confidential client)**

- Client type: OpenID Connect
- Access type: confidential
- Standard flow enabled (Authorization Code Grant)
- PKCE: required (S256)
- Valid redirect URIs: `https://app.shopvault.com/login/oauth2/code/keycloak`
- Web origins: `https://app.shopvault.com`
- Service account roles: 비활성화

`shopvault-bff`는 BFF가 사용자 로그인을 대리할 때 쓰는 OIDC 클라이언트다. PKCE는 7.0이 기본으로 켜 주지만, IdP 측에서도 `required`로 명시해 두면 6.x에서 올라온 코드가 explicit하게 끄고 있어도 IdP가 잘라낸다. 함정 15(레퍼런스 §7.4)에서 짚었던 그 경우다.

**클라이언트 2: `shopvault-api` (resource server)**

- Client type: OpenID Connect
- Access type: bearer-only
- Audience mapper로 access token에 `aud: shopvault-api` 추가
- Role 매핑: realm role `customer`, `admin`, `payment-admin`을 토큰의 `roles` 클레임으로 포함

자원 서버는 토큰을 검증할 뿐 토큰을 발급하지 않는다. `bearer-only`로 두는 게 자연스럽다. `aud` 클레임을 명시적으로 추가해 두는 이유는, JWT 함정 8(레퍼런스 §7.2) 그러니까 알고리즘·발급자 confusion을 한 겹 더 막기 위해서다. 자원 서버 측 코드에서 audience를 `OAuth2TokenValidator`로 검증해 줄 수 있다.

**클라이언트 3: `shopvault-payment-client` (client credentials)**

- Access type: confidential
- Service Accounts Enabled: true
- Standard flow: disabled
- Direct access grants: disabled
- 별도 realm role `payment:charge` 부여

이건 사용자 인증과 무관하다. `shop-api`가 외부 결제 게이트웨이를 부를 때 client credentials grant로 access token을 받기 위한 클라이언트다. 사용자가 끼지 않으므로 redirect URI도 없고 PKCE도 없다.

마지막으로 realm role 세 개를 만든다. `customer`, `admin`, `payment-admin`. 일반 가입자는 자동으로 `customer`. 관리자는 별도 그룹에 `admin`. 결제 환불 권한을 가진 사람만 `payment-admin`을 더 받는다. Keycloak에서 client scope의 role mapper를 통해 이 세 role이 access token의 `roles` 클레임 배열로 포함되도록 설정해 두자. 이 결정이 곧 자원 서버에서 `JwtAuthenticationConverter`가 다룰 클레임이 된다.

여기까지 짚고, 이제 코드로 넘어가자.

## 15.3 shop-bff — Spring Cloud Gateway로 빌드하는 BFF

BFF부터 짓는 이유는 단순하다. 이 시스템에서 브라우저가 가장 먼저 만나는 서버이기 때문이다. 14장에서 BFF의 원리는 다뤘다. 여기서는 코드를 짠다.

`build.gradle`의 핵심 의존성은 세 줄이다.

```kotlin
implementation("org.springframework.cloud:spring-cloud-starter-gateway")
implementation("org.springframework.boot:spring-boot-starter-oauth2-client")
implementation("org.springframework.cloud:spring-cloud-starter-oauth2")
```

Spring Cloud Gateway는 reactive(WebFlux) 위에서 돈다. 그래서 11장에서 다룬 reactive 보안 API가 여기서 깨어난다. 잊지 말자.

`application.yml`은 이렇게 짠다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            provider: keycloak
            client-id: shopvault-bff
            client-secret: ${KEYCLOAK_BFF_SECRET}
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            scope: openid, profile, email
        provider:
          keycloak:
            issuer-uri: https://auth.shopvault.com/realms/shopvault
  cloud:
    gateway:
      routes:
        - id: api
          uri: https://api.shopvault.com
          predicates:
            - Path=/api/**
          filters:
            - TokenRelay
        - id: spa
          uri: https://shop-web.internal.shopvault.com
          predicates:
            - Path=/**

server:
  servlet:
    session:
      cookie:
        same-site: lax
        http-only: true
        secure: true
        name: SHOPVAULT_SESSION
```

여기서 눈여겨볼 건 두 가지다.

첫째, `TokenRelay`라는 한 단어. Spring Cloud Gateway가 BFF에 내장해 준 마법이다. 사용자가 BFF 세션을 가진 채로 `/api/**`를 호출하면, gateway 필터가 사용자의 OAuth2 `OAuth2AuthorizedClient`에서 access token을 꺼내 `Authorization: Bearer <token>` 헤더로 자원 서버 요청에 붙여 준다. 우리가 직접 access token을 만지지 않아도 된다. 14장에서 "BFF는 토큰을 서버 측에 가둔다"고 말한 그 약속이, 이 한 줄로 실현된다.

둘째, 세션 쿠키 설정. `http-only: true`, `secure: true`, `same-site: lax`. 이 세 줄은 협상의 여지가 없다. XSS로 새지 않게 `HttpOnly`, HTTPS 외에는 전송되지 않게 `Secure`, CSRF의 첫 줄 방어로 `SameSite=Lax`. 11장과 9장에서 한 약속 그대로다.

이제 Security 설정. Reactive 환경이라는 사실을 잊지 말자.

```java
@Configuration
@EnableWebFluxSecurity
class BffSecurityConfig {

    @Bean
    SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(ex -> ex
                .pathMatchers("/", "/index.html", "/assets/**", "/login", "/oauth2/**", "/login/oauth2/**")
                    .permitAll()
                .anyExchange().authenticated())
            .oauth2Login(Customizer.withDefaults())
            .logout(l -> l.logoutSuccessHandler(oidcLogoutSuccessHandler()))
            .csrf(ServerHttpSecurity.CsrfSpec::spa)   // 7.0 한 줄 (SPA-친화 모드)
            .headers(h -> h
                .hsts(hsts -> hsts.includeSubdomains(true).maxAge(Duration.ofDays(365)))
                .contentSecurityPolicy(csp -> csp.policyDirectives(
                    "default-src 'self'; script-src 'self'; object-src 'none'")))
            .build();
    }

    @Bean
    ServerLogoutSuccessHandler oidcLogoutSuccessHandler() {
        var handler = new OidcClientInitiatedServerLogoutSuccessHandler(clientRegistrationRepository);
        handler.setPostLogoutRedirectUri("{baseUrl}/");
        return handler;
    }

    private final ReactiveClientRegistrationRepository clientRegistrationRepository;
    BffSecurityConfig(ReactiveClientRegistrationRepository repo) {
        this.clientRegistrationRepository = repo;
    }
}
```

`csrf(... .spa)` 한 줄이 7.0에서 추가된 SPA-친화 CSRF 모드다. 이전에는 SPA가 `XSRF-TOKEN` 쿠키를 읽어 헤더로 다시 넣어 주는 패턴을 우리가 직접 빌드해야 했지만, 이제는 한 줄이 그 패턴을 표준으로 묶어 준다(레퍼런스 §6.6, §8.3). HSTS·CSP·HttpOnly 세션의 헤더 3종 세트는 9장에서 다룬 그대로다.

`oauth2Login(Customizer.withDefaults())`만으로 PKCE가 켜진다는 점은 6장에서 확인했다. confidential client에 PKCE를 굳이 다시 켜지 않아도 7.0의 기본 동작이 그렇게 한다. 6.x에서 올라온 코드가 explicit하게 끄고 있지만 않다면 신경 쓰지 않아도 된다.

로그아웃은 OIDC RP-initiated logout으로 잡았다. 사용자가 `/logout`을 누르면, BFF가 세션을 무효화하고 Keycloak의 end-session endpoint로 redirect한다. Keycloak 측에서도 SSO 세션이 닫히고, 브라우저는 다시 BFF 홈으로 돌아온다. 이 동선을 빠뜨리면, 사용자가 BFF에서는 로그아웃했는데 IdP에 가면 여전히 로그인 상태로 남아 있는 — 그러니까 다음번 `/login`에서 묻지도 따지지도 않고 통과되는 — 찜찜한 풍경이 생긴다.

여기까지 짠 BFF는 이미 가동된다. 브라우저가 `app.shopvault.com`을 처음 열면 정적 자원이 내려가고, SPA가 부팅한다. SPA가 `fetch('/api/me')`를 던지면 BFF가 인증을 요구하고, 사용자는 `/login`을 거쳐 Keycloak으로 redirect된다.

## 15.4 shop-api — 두 개의 `SecurityFilterChain`

이제 자원 서버다. 8장의 인가, 5장의 JWT·DPoP, 그리고 14장의 Actuator 격리가 한 자리에 모인다.

먼저 `application.yml`.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.shopvault.com/realms/shopvault
          # JWKs URL은 issuer-uri의 OIDC discovery로 자동 결정

management:
  endpoints:
    web:
      exposure:
        include: health, info, prometheus
  server:
    port: 9001          # Actuator를 별도 포트로 격리 (14장 §14.5)
```

Actuator를 별도 포트로 빼는 건 14장에서 본 한국 우아한형제들 사례의 교훈이다. `env` 같은 endpoint가 같은 포트에 노출돼 외부에서 접근 가능했던 그 사고. 한 줄 분리로 막을 수 있는 일이라면, 막아 두는 편이 낫다.

이제 Security 설정. 두 개의 `SecurityFilterChain`을 짠다.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class ShopApiSecurityConfig {

    /**
     * (1) Actuator 전용 체인 — 격리, 인증 없음(내부망 한정)
     *     별도 포트(9001)에서만 노출되므로 외부에서 닿지 않는다.
     */
    @Bean
    @Order(1)
    SecurityFilterChain actuatorChain(HttpSecurity http) throws Exception {
        return http
            .securityMatcher(EndpointRequest.toAnyEndpoint())
            .authorizeHttpRequests(a -> a.anyRequest().permitAll())
            .csrf(CsrfConfigurer::disable)
            .build();
    }

    /**
     * (2) API 본체 체인 — JWT + DPoP, stateless, scope/role 기반 인가
     */
    @Bean
    @Order(2)
    SecurityFilterChain apiChain(HttpSecurity http,
                                  JwtAuthenticationConverter jwtConverter) throws Exception {
        return http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers(HttpMethod.GET, "/api/products/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .oauth2ResourceServer(o -> o
                .jwt(j -> j.jwtAuthenticationConverter(jwtConverter)))
            .csrf(CsrfConfigurer::disable)
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .build();
    }

    /**
     * Keycloak realm role을 권한으로 매핑 + SCOPE_* 권한도 같이 살림.
     */
    @Bean
    JwtAuthenticationConverter jwtAuthenticationConverter() {
        var roles = new JwtGrantedAuthoritiesConverter();
        roles.setAuthoritiesClaimName("roles");
        roles.setAuthorityPrefix("ROLE_");

        var scopes = new JwtGrantedAuthoritiesConverter();   // 기본 scp/scope → SCOPE_*

        var conv = new JwtAuthenticationConverter();
        conv.setJwtGrantedAuthoritiesConverter(jwt -> {
            var combined = new ArrayList<GrantedAuthority>();
            combined.addAll(roles.convert(jwt));
            combined.addAll(scopes.convert(jwt));
            return combined;
        });
        return conv;
    }

    /**
     * audience 검증을 한 겹 더 (RFC 8725 §4.1 권고).
     */
    @Bean
    JwtDecoder jwtDecoder(OAuth2ResourceServerProperties props) {
        var decoder = NimbusJwtDecoder
            .withIssuerLocation(props.getJwt().getIssuerUri())
            .build();

        var withAud = new DelegatingOAuth2TokenValidator<>(
            JwtValidators.createDefaultWithIssuer(props.getJwt().getIssuerUri()),
            new JwtClaimValidator<List<String>>("aud",
                aud -> aud != null && aud.contains("shopvault-api")));
        decoder.setJwtValidator(withAud);
        return decoder;
    }
}
```

체인이 두 개라는 사실, `@Order`로 우선순위를 명시했다는 사실, 그리고 첫 체인이 `securityMatcher`로 Actuator만 잡고 두 번째 체인이 `/api/**`만 잡는다는 사실 — 이 셋이 핵심이다. 2장에서 본 "필터 체인은 `SecurityFilterChainProxy`가 첫 매칭만 사용한다"는 규칙이 여기서 작동한다. 두 체인은 서로의 영역에 발을 들이지 않는다.

`JwtAuthenticationConverter`는 두 가지 일을 한꺼번에 한다. Keycloak이 토큰에 넣어 준 `roles` 클레임을 `ROLE_*` 권한으로 매핑하고, 동시에 OAuth2 표준 `scope`/`scp` 클레임은 `SCOPE_*`로 매핑해 둔다. 이 둘이 동시에 권한 컬렉션에 들어가야, 다음 절의 메서드 보안이 `hasRole('ADMIN')`도 `hasAuthority('SCOPE_order:write')`도 함께 표현할 수 있다.

`JwtDecoder`를 직접 빈으로 등록해 `aud` validator를 더한 부분도 그냥 지나치지 말자. RFC 8725 §4.1이 audience 검증을 명시적으로 권고하고 있고, 우리는 그걸 한 줄 더 적어 준다. 토큰이 다른 자원 서버용으로 발급된 것을 우리 자원 서버가 받아 들이는 — 그러니까 "내가 받을 토큰이 아닌데도 받아 들이는" — 잠재적 사고 한 종류를 막는다.

이제 DPoP다. 5장에서 RFC 9449를 따라 살펴본 바로 그것이다. Spring Security 7은 DPoP-bound 토큰을 자원 서버 측에서 1급으로 처리한다(레퍼런스 §4.9). 한 줄을 더 얹자.

```java
http.oauth2ResourceServer(o -> o
    .jwt(j -> j.jwtAuthenticationConverter(jwtConverter))
    .dPoP(Customizer.withDefaults()));   // 7.0 신규
```

이 한 줄로 자원 서버는 매 요청의 `DPoP` 헤더를 검증한다. 토큰 안의 `cnf.jkt`(JWK SHA-256 thumbprint)와 DPoP proof JWT 안의 공개 키 thumbprint가 일치하는지, `htm`(HTTP method), `htu`(HTTP URI), `iat`, `jti`, `ath`(access token SHA-256 hash)가 적절한지를 본다. 이 검증이 통과하지 못하면 401이다. 토큰을 누군가 훔쳐 가도, DPoP 개인 키 없이는 쓰지 못한다. BFF 측에서도 access token을 자원 서버에 보내기 전에 DPoP proof를 매번 만들어 헤더에 붙여야 하는데, 이 부분은 Spring Security가 client 측에도 helper를 제공한다(레퍼런스 §4.9의 `NimbusJwtEncoder` 예제 참조). 단, 7.0 GA 시점 client 측 DPoP API의 시그니처는 미세 보강 가능성이 있으니, 출간 시점 docs를 한 번 더 확인하자.

> **결정의 기록.** ShopVault는 DPoP를 켜기로 했다. 5장 끝의 "DPoP 결정 기준"에서 본 그 결정이다. 결제 흐름이 끼어 있고, refresh 없는 access token이 BFF에서 자원 서버로 흐르며, 토큰 탈취로 단 한 번이라도 결제가 일어나면 곤란하기 때문이다. 단순한 게시판형 서비스라면 DPoP 없이 가도 무방하다. 모든 시스템에 DPoP가 답인 것은 아니다.

## 15.5 메서드 보안 — 서비스 계층에 인가를 새긴다

URL 인가만으로는 부족하다. 8장에서 다섯 층의 인가 모델을 따라 내려가며 본 그 사실이다. URL은 첫 번째 줄이고, 메서드 보안이 두 번째 줄이며, 도메인 객체 보안이 그 아래다.

ShopVault의 서비스 계층 한 단면을 보자.

```java
@Service
class OrderService {

    @PreAuthorize("hasAuthority('SCOPE_order:read') and hasRole('CUSTOMER')")
    public List<Order> myOrders(Authentication auth) { ... }

    @PreAuthorize("hasAuthority('SCOPE_order:write') and hasRole('CUSTOMER')")
    public Order place(NewOrder draft, Authentication auth) { ... }

    @PreAuthorize("hasRole('ADMIN')")
    public void cancel(long orderId, String reason) { ... }

    @PreAuthorize("hasRole('PAYMENT_ADMIN')")
    public Refund refund(long orderId, Money amount) { ... }
}
```

`@EnableMethodSecurity`가 `apiChain` 설정 클래스에 붙어 있으니, 이 어노테이션이 그대로 살아난다. 6.x 시절에 `@EnableGlobalMethodSecurity`를 같이 쓰던 코드라면, 함정 2(13장 13.4)에서 본 대로 정확히 한 군데로 통일해 두자. 두 어노테이션이 한 모듈 안에 섞이면 `@PreAuthorize`가 조용히 무력화되는 경우가 있다.

`refund` 같은 메서드에는 한 줄을 더 얹어 두면 좋다.

```java
@PreAuthorize("hasRole('PAYMENT_ADMIN') and hasAuthority('FACTOR_OTT')")
public Refund refund(long orderId, Money amount) { ... }
```

`FACTOR_OTT`라는 권한이 어디서 오는가? 7장에서 본 MFA factor 권한이다. 1차 패스워드 인증만 통과한 사용자는 `FACTOR_PASSWORD` 권한만 가지고, 2차 OTT까지 통과해야 `FACTOR_OTT`가 더해진다. 메서드 보안 한 줄로 "환불은 MFA를 통과한 관리자만"이라고 말할 수 있게 되는 거다. Spring 공식 블로그(2025-10-21)가 자랑스럽게 미는 모델 그대로다.

## 15.6 관리자 MFA — factor가 권한이 되는 모델

이제 관리자 측 흐름을 만들자. 일반 사용자는 패스워드 한 번이면 충분하지만, 관리자는 그렇게 두면 곤란하다. 7장에서 다룬 MFA를 여기에 얹는다.

기본 아이디어를 먼저 짚자. 7.0의 MFA는 "두 번째 인증 단계"를 별도 컴포넌트로 만들지 않는다. 대신 "각 factor를 통과했는지"를 권한(`FactorGrantedAuthority`)으로 표현한다. 인가 규칙이 "두 factor 모두 필요"라고 적으면, 사용자가 하나만 통과한 상태에서 그 URL을 부르려고 할 때 Spring Security가 자동으로 다음 factor 입력 페이지로 redirect한다. 인증 흐름의 추가 단계가 인가 규칙으로 표현된다는 게 핵심이다.

ShopVault의 관리자 동선은 Keycloak에 위탁하지 않고 자원 서버 측에서 직접 MFA를 받기로 했다고 가정하자. 실제로는 Keycloak에서 MFA를 끝낸 토큰을 받는 흐름이 더 일반적이지만, 7.0의 새 API를 한 번 체험해 보기 위해 자원 서버 측 MFA를 짜본다.

```java
@Configuration
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
class AdminMfaConfig {

    @Bean
    @Order(0)   // apiChain보다 먼저 매칭되도록
    SecurityFilterChain adminChain(HttpSecurity http,
                                    MagicLinkSender magicLinkSender,
                                    AuthorizationManagerFactory<RequestAuthorizationContext> mfa) throws Exception {
        return http
            .securityMatcher("/admin/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers("/admin/refund/**")
                    .access(mfa.allAuthorities("FACTOR_PASSWORD", "FACTOR_OTT"))
                .anyRequest()
                    .access(mfa.allAuthorities("FACTOR_PASSWORD")))
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(ott -> ott
                .tokenGenerationSuccessHandler(magicLinkSender::send))
            .build();
    }
}
```

해석해 보자. `@EnableMultiFactorAuthentication`이 두 가지 factor를 시스템에 등록한다. `adminChain`의 `securityMatcher("/admin/**")`은 관리자 페이지 전체를 잡고, `/admin/refund/**`만은 두 factor를 모두 요구하며, 나머지 관리자 페이지는 패스워드 한 단계만 요구한다.

관리자가 `/admin`에 처음 들어오면 패스워드 폼이 뜬다. 통과하면 `FACTOR_PASSWORD` 권한이 컨텍스트에 박힌다. 일반 관리자 페이지는 여기서 통과된다. 그런데 `/admin/refund/*`을 누르는 순간 인가 규칙이 `FACTOR_OTT`도 요구하기 때문에, Spring Security가 자동으로 OTT 발급 페이지로 redirect한다. 매직 링크가 메일로 날아오고, 관리자가 링크를 클릭해 OTT 토큰을 제출하면 `FACTOR_OTT`도 권한 컬렉션에 더해진다. 이제 환불 페이지가 열린다.

다음에 같은 관리자가 다시 환불 페이지에 들어올 때는, 세션 안에 두 factor 권한이 모두 살아 있으니 매끄럽게 통과된다. 한 번 통과한 factor는 세션 동안 유지된다. 단, 세션 만료나 명시적 로그아웃 뒤에는 처음부터 다시 시작이다.

이 모델이 우리 머리에 박혔으면 좋겠다. **factor는 추가 단계가 아니라 권한이다.** 그래서 메서드 보안에서도 한 줄로 `hasAuthority('FACTOR_OTT')`를 적을 수 있고, URL 규칙에서도 같은 어휘를 쓴다. 인증과 인가가 한 어휘로 묶이는 순간이다.

`MagicLinkSender`는 우리가 직접 구현해야 한다. 7.0이 라이브러리로 매직 링크 전송 자체는 제공하지 않는다(레퍼런스 §4.7). 메일 발송이든 SMS든 우리 도메인의 책임이다. 한 인터페이스만 보여 두자.

```java
@Component
class MagicLinkSender implements OneTimeTokenGenerationSuccessHandler {

    private final MailService mail;

    @Override
    public void handle(HttpServletRequest req, HttpServletResponse res,
                       OneTimeToken token) throws IOException {
        var link = UriComponentsBuilder.fromHttpUrl(req.getRequestURL().toString())
            .replacePath("/login/ott")
            .queryParam("token", token.getTokenValue())
            .build().toUriString();

        var username = token.getUsername();
        mail.send(username + "@shopvault.com",
            "ShopVault 관리자 추가 인증",
            "다음 링크로 5분 안에 인증을 완료해 주세요: " + link);
    }
}
```

`OneTimeTokenService`는 빈으로 등록해 두자. 운영 환경이라면 `InMemoryOneTimeTokenService`가 아니라 `JdbcOneTimeTokenService`로. 토큰 저장이 메모리에만 있으면 다중 인스턴스 환경에서 망가진다.

```java
@Bean
OneTimeTokenService ottService(JdbcOperations jdbc) {
    return new JdbcOneTimeTokenService(jdbc);
}
```

## 15.7 인증 흐름 1 — 일반 사용자 로그인 (SPA → BFF → Keycloak)

자, 이제 흐름을 따라가 보자. 첫 번째 시나리오는 가장 흔한 일반 사용자 로그인이다.

```
[Browser]                  [shop-bff]                 [Keycloak]
   │                            │                          │
   │── GET /app ───────────────▶│                          │
   │◀── 200 OK (SPA bundle) ────│                          │
   │                            │                          │
   │── GET /api/me (no cookie) ▶│                          │
   │                            │ (no session → 401)        │
   │◀── 401 + Location: /login ─│                          │
   │                            │                          │
   │── GET /login ─────────────▶│                          │
   │                            │── 302 to /oauth2/         │
   │                            │    authorization/keycloak │
   │◀── 302 (redirect) ─────────│                          │
   │                            │                          │
   │── GET /oauth2/             │                          │
   │   authorization/keycloak ─▶│                          │
   │                            │  PKCE code_verifier      │
   │                            │  생성 + 세션에 저장       │
   │                            │  state, nonce 생성        │
   │◀── 302 to Keycloak ────────│                          │
   │   (code_challenge=S256...)                            │
   │                            │                          │
   │── GET /realms/shopvault/   │                          │
   │   protocol/openid-connect/ │                          │
   │   auth?... ──────────────────────────────────────────▶│
   │                            │       (Keycloak 로그인 폼) │
   │◀──────────────────────────────────────── 200 form ────│
   │                            │                          │
   │── POST credentials ──────────────────────────────────▶│
   │                            │       (검증, code 발급)   │
   │◀───────────────────── 302 to /login/oauth2/code/... ──│
   │                            │                          │
   │── GET /login/oauth2/       │                          │
   │   code/keycloak?code=...─▶│                          │
   │                            │── POST /token ──────────▶│
   │                            │   (code + verifier)      │
   │                            │◀── access + id + refresh ─│
   │                            │  세션 생성, 토큰 보관      │
   │                            │  Set-Cookie:              │
   │                            │   SHOPVAULT_SESSION=...   │
   │◀── 302 to / + cookie ──────│                          │
   │                            │                          │
   │── GET /api/me (cookie) ───▶│                          │
   │                            │── GET /api/me            │
   │                            │   Authorization: Bearer ─▶ shop-api
   │                            │      + DPoP proof        │
   │                            │◀────────────── {user} ────│
   │◀── 200 {user} ─────────────│                          │
```

이 그림이 14장 BFF 패턴의 약속을 한 시퀀스로 풀어낸 것이다. 브라우저는 access token을 한 번도 손에 쥐지 않는다. 그저 HttpOnly 세션 쿠키 하나로 BFF와 대화할 뿐이고, 토큰은 BFF의 세션 안에 갇혀 있다. 14장에서 우리가 한 약속이 그것이었다.

여기서 짚을 만한 작은 디테일이 몇 가지 있다.

첫째, `code_verifier`는 BFF의 세션에 저장된다. PKCE의 의미가 "code 탈취만으로 토큰을 받지 못하게 한다"인데, BFF는 자기 세션 안에 verifier를 보관해 두었다가 token endpoint를 호출할 때 함께 보낸다. 6.x까지는 confidential client에서 PKCE를 explicit하게 켜야 했지만 7.0의 기본이 바뀌었다(레퍼런스 §4.6, §8.5). 6.x에서 올라온 코드가 명시적으로 `setPkce(false)` 같은 짓을 하고 있지 않다면, 우리가 한 줄 더 적지 않아도 PKCE가 동작한다.

둘째, `state`는 CSRF 방어, `nonce`는 ID Token replay 방어다. 둘 다 Spring Security가 자동으로 만들고 자동으로 검증한다. 우리가 손댈 일은 거의 없다.

셋째, 마지막 응답의 `302 to /`. 사용자는 `/login`에서 시작했을 수도 있고, `/orders/123`에서 401을 만나 `/login`으로 끌려왔을 수도 있다. Spring Security는 처음 401이 일어난 그 자리를 `savedRequest`로 기억해 두었다가 인증이 끝나면 그쪽으로 다시 보내 준다. 매끄러운 UX의 작은 비밀이다.

## 15.8 인증 흐름 2 — 관리자 MFA 로그인

두 번째 시나리오. 환불 권한을 가진 `payment-admin` 사용자가 환불 페이지를 누른다.

```
[Browser]              [shop-bff]            [shop-api admin chain]
   │                       │                          │
   │── GET /admin/refund ─▶│                          │
   │                       │   (no session → 401, redirect /login)
   │                       │                          │
   │── /login flow with    │                          │
   │   Keycloak (앞과 동일) │                          │
   │                       │                          │
   │   세션 생성, 토큰 보관 │                          │
   │   (Keycloak의 roles 클레임에 admin, payment-admin) │
   │                       │                          │
   │── GET /admin/refund ─▶│── relay ────────────────▶│
   │                       │                          │ 토큰 검증 OK
   │                       │                          │ 권한: ROLE_PAYMENT_ADMIN
   │                       │                          │       FACTOR_PASSWORD
   │                       │                          │ /admin/refund 인가 규칙:
   │                       │                          │  PASSWORD ∧ OTT
   │                       │                          │ → factor 부족
   │                       │                          │
   │                       │◀── 302 to /login/ott ────│
   │◀── 302 to /login/ott ─│                          │
   │                       │                          │
   │── POST /login/ott ───▶│── /login/ott ───────────▶│
   │   (사용자명만)         │                          │ OneTimeTokenService
   │                       │                          │ 토큰 생성
   │                       │                          │ MagicLinkSender 호출
   │                       │                          │
   │            ✉ 이메일 도착 (링크 안에 token=...)       │
   │                       │                          │
   │── 링크 클릭 ──────────▶│── /login/ott?token=... ─▶│
   │                       │                          │ 토큰 검증 OK
   │                       │                          │ FACTOR_OTT 권한 부여
   │                       │                          │ → 두 factor 충족
   │                       │◀── 302 to /admin/refund ─│
   │◀── 302 to /admin/    ──│                          │
   │   refund               │                          │
   │── GET /admin/refund ─▶│── relay ────────────────▶│ 통과
   │◀── 200 ────────────────│◀── 200 ──────────────────│
```

이 흐름을 한 줄로 요약하면 이렇다. **인가 규칙이 "factor 부족"을 발견하는 순간, Spring Security가 적절한 인증 흐름으로 자동 분기시킨다.** 우리가 직접 "이 사용자는 OTT를 더 받아야 한다"는 분기를 짤 필요가 없다. `@EnableMultiFactorAuthentication`이 그 분기를 시스템에 박아 두었기 때문이다.

7장에서 본 그림이 이 자리에서 실제로 살아 돌아간다. 그때 약속처럼, factor는 추가 단계가 아니라 권한이다. 같은 어휘로 인증과 인가가 묶인다.

## 15.9 인증 흐름 3 — SPA → BFF → API 호출

세 번째 시나리오. 가장 짧지만 가장 자주 일어나는 흐름이다.

이미 로그인을 마친 사용자가 SPA 안에서 `장바구니에 담기`를 누른다. SPA는 `POST /api/cart`를 던진다. 그게 전부다. SPA 측 코드에서 토큰을 다루는 줄은 하나도 없다.

```javascript
// SPA 측 — 그냥 fetch 한 줄
await fetch('/api/cart', {
  method: 'POST',
  body: JSON.stringify({ productId, qty }),
  headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': csrfToken },
  credentials: 'same-origin'
});
```

BFF로 들어온 이 요청은 다음을 거친다.

1. `same-origin`이므로 세션 쿠키가 자동으로 함께 온다.
2. CSRF 토큰을 헤더에서 본다 — `csrf(... .spa)`가 받아 주는 표준 패턴.
3. 인증 체크 — 세션에서 `OAuth2AuthorizedClient` 발견.
4. Gateway의 `TokenRelay` 필터가 `OAuth2AuthorizedClient`에서 access token을 꺼내 `Authorization: Bearer <token>`을 만든다.
5. 같은 자리에서 DPoP proof JWT를 만들어 `DPoP: <proof>` 헤더를 더한다. (DPoP 키는 BFF가 보관)
6. `shop-api`로 forward.

`shop-api` 측에서는 다음을 거친다.

1. `apiChain`의 `oauth2ResourceServer.jwt(...)`이 JWT 서명·발급자·audience·만료를 검증.
2. `dPoP(...)`가 DPoP 헤더 검증 — `cnf.jkt` 일치, `htm/htu/iat/jti/ath` 검증.
3. `JwtAuthenticationConverter`가 `roles`·`scope` 클레임을 `ROLE_*`·`SCOPE_*` 권한으로 만들어 `Authentication`에 박는다.
4. URL 인가 — `/api/cart`는 `anyRequest().authenticated()`에 걸려 통과.
5. 컨트롤러 → `OrderService.place(...)` 호출.
6. 메서드 보안 — `@PreAuthorize("hasAuthority('SCOPE_order:write') and hasRole('CUSTOMER')")` 검증.
7. 비즈니스 로직 실행, 응답 반환.

브라우저에서 본 한 줄의 `fetch`는 이 일곱 단계를 통과한 결과로 200이 돼서 돌아온다. 한 시스템 안에서 이렇게 많은 결정이 한 요청에 묶여 있다는 사실을, 우리는 가끔 잊는다. 잊지 말자. 인증과 인가는 같이 산다.

여기까지 따라온 독자에게 작은 보너스 질문 하나. **이 흐름에서 가장 위험한 한 줄은 어디인가?** 잠시 멈춰 답을 떠올려 보자.

답은 BFF의 세션 쿠키 설정이다. `SameSite`, `Secure`, `HttpOnly` 셋 중 어느 하나라도 빠지면, 이 잘 만든 시스템이 한 줄로 무너진다. 9장과 10장에서 길게 다뤘던 그 이유 때문에. SPA에서 토큰을 다루지 않게 만들어 둔 모든 노력이 — `HttpOnly`가 없으면 XSS 한 번으로 세션 쿠키가 새 나갔을 때 — 다시 흔들린다. 한 줄을 보자.

```yaml
server:
  servlet:
    session:
      cookie:
        same-site: lax        # 비워 두지 말 것
        http-only: true       # 비워 두지 말 것
        secure: true          # 비워 두지 말 것
```

이 세 줄이 한 시스템의 보안에서 마지막 보루다. 자주 잊고 자주 깨진다.

## 15.10 외부 결제 호출 — `@HttpExchange` + `@ClientRegistrationId`

마지막 한 조각. `shop-api`가 외부 결제 게이트웨이를 호출할 때다. 사용자가 끼지 않는 client credentials 흐름이고, 우리는 access token을 매번 직접 만들고 싶지 않다.

Spring Boot 4 / Spring 7의 `@HttpExchange`와 Spring Security 7의 `@ClientRegistrationId`가 만나면 이렇게 깔끔해진다.

```java
@HttpExchange("https://api.payment-gateway.com")
@ClientRegistrationId("payment")
interface PaymentClient {

    @PostExchange("/charges")
    ChargeResult charge(@RequestBody ChargeRequest req);

    @PostExchange("/refunds")
    RefundResult refund(@RequestBody RefundRequest req);
}
```

그리고 `application.yml`에 결제용 client registration을 한 자리에 적어 둔다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          payment:
            client-id: shopvault-payment-client
            client-secret: ${PAYMENT_CLIENT_SECRET}
            authorization-grant-type: client_credentials
            scope: payment:charge
        provider:
          payment:
            token-uri: https://auth.shopvault.com/realms/shopvault/protocol/openid-connect/token
```

이걸로 끝이다. `@HttpExchange` 인터페이스를 빈으로 등록해 두면(`HttpServiceProxyFactory` 한 줄), Spring Security가 호출 시점에 client credentials 흐름으로 access token을 받아 자동으로 `Authorization: Bearer ...` 헤더에 넣어 준다. 토큰 만료가 가까워지면 백그라운드에서 갱신한다. 우리는 그저 인터페이스 메서드를 부를 뿐이다.

```java
@Service
class RefundFlow {
    private final PaymentClient payment;

    @PreAuthorize("hasRole('PAYMENT_ADMIN') and hasAuthority('FACTOR_OTT')")
    public Refund refund(long orderId, Money amount) {
        var result = payment.refund(new RefundRequest(orderId, amount));
        // ... domain logic
    }
}
```

이 한 메서드가 책 전체의 결을 한 자리에 묶는다. 메서드 보안(8장), MFA factor(7장), 외부 OAuth2 호출(6장), 그리고 그 호출의 깔끔한 추상화(`@HttpExchange`). 우리가 1장에서 출발해 여기까지 온 거리를, 이 짧은 메서드 하나가 정직하게 비추어 준다.

## 15.11 운영 체크리스트 — 빌드보다 오래 가는 것들

코드가 끝났다고 시스템이 끝나는 건 아니다. ShopVault가 운영에 들어가기 전에 한 번은 짚어야 할 것들을 묶어 두자. 14장의 운영 절을 떠올리며 적는다.

- [ ] **인증 이벤트 audit.** `AuthenticationSuccessEvent`, `AuthenticationFailureBadCredentialsEvent`, `LogoutSuccessEvent` 같은 Spring의 application event를 `ApplicationListener`로 받아 audit 로그에 적자. IP, 사용자명, 시각, factor 정보를 묶어. 사고가 나면 첫 번째로 펴 보게 된다.
- [ ] **JWK 회전 schedule.** Keycloak 측 JWK는 주기적으로 회전된다. 자원 서버의 `NimbusJwtDecoder`는 JWKs URL을 캐시한다. 새 키가 등장하면 `kid`로 자동 fetch하지만, 캐시 TTL이 너무 길면 회전 직후 잠깐 401이 폭주할 수 있다. `JwkSourceBuilder`로 캐시 정책을 명시적으로 잡아 두자(레퍼런스 §6.8).
- [ ] **모니터링 대시보드.** `prometheus` endpoint를 통해 Spring Security의 인증/인가 카운터를 노출하자. `spring.security.filter.invocations`, `spring.security.authentication.{success,failure}` 같은 지표가 핵심. 인증 실패율이 평소의 10배로 튀면 알람.
- [ ] **Actuator 격리.** `shop-api`의 `application.yml`에서 본 `management.server.port: 9001`이 살아 있는지 배포 환경 변수에서 다시 한번 확인. 같은 포트에 같이 노출되어 있으면, 14장에서 본 사고의 길이 열린다(레퍼런스 §7.5).
- [ ] **CSP 정책 점검.** BFF의 `Content-Security-Policy` 헤더가 SPA의 외부 폰트·이미지·CDN을 정확히 반영하는지. 너무 느슨하면 XSS 방어가 약해지고, 너무 빡빡하면 SPA가 깨진다.
- [ ] **deprecation warning 0.** 빌드 로그에서 Spring Security 관련 deprecation warning이 0건인지. 7.0에서 deprecation으로 표시된 API는 7.1에서 빠질 수 있다. 출시 일정을 따라가는 팀이라면 warning을 무시하지 말자.
- [ ] **테스트 회귀 안전망.** 12장에서 만든 인증/인가 통합 테스트가 CI에 묶여 있는지. 적어도 다섯 가지는 — 일반 사용자 정상 로그인, 관리자 MFA 흐름, 권한 부족 시 403, JWT 만료 시 401, DPoP 헤더 누락 시 401 — 회귀로 잡아 두자.
- [ ] **시크릿 관리.** `KEYCLOAK_BFF_SECRET`, `PAYMENT_CLIENT_SECRET`이 어디 있는가. application.yml에 평문으로 들어가 있으면 끔찍한 일이다. Vault, AWS Secrets Manager, Kubernetes Secret 중 하나여야 한다.

이 체크리스트는 ShopVault의 한 PR에 그대로 댓글로 붙여 둘 만한 분량이다. 한 번 만들어 두고, 새 서비스가 올라올 때마다 다시 펴 보자.

## 15.12 한 권의 어휘가 한 시스템에 녹았다 — 회고

자, 이 책을 처음 펼쳤을 때를 기억해 보자. 1장에서 빌드가 한 줄도 통과하지 못하던 그 화면. `WebSecurityConfigurerAdapter`가 사라졌다는 사실 앞에서 잠시 막막했던 그 순간. 책의 처음과 끝을 한 화면에 놓고 보면, 우리가 얼마나 멀리 왔는지 정직하게 보인다.

이 마지막 시나리오 안에서 14개 챕터의 어휘가 어떻게 살아 있는지 한 번만 정리해 두자. 길지 않게.

- **1장**의 큰 그림 다섯 개 — 레거시 DSL 제거, 인가 두뇌 교체, Authorization Server 흡수, 모던 인증 1급화, 토대 라이브러리 교체 — 이 다섯 갈래가 ShopVault의 모든 코드 줄에 흩어져 있다.
- **2장**의 필터 체인 순서는 `shop-api`의 두(아니, 세) `SecurityFilterChain`이 `@Order`로 줄 세우는 그 자리에 정확히 박혀 있다.
- **3장**의 컴포넌트 위임 모델(`AuthenticationManager` → `Provider`)은 `oauth2ResourceServer.jwt(...)`의 내부에서 묵묵히 돈다.
- **4장**의 폼 로그인은 관리자 MFA의 1차 단계에서 살아 있다.
- **5장**의 JWT 자원 서버와 DPoP는 `apiChain`의 `oauth2ResourceServer.jwt(...).dPoP(...)` 한 줄에서 만난다.
- **6장**의 OAuth2 Client + OIDC는 BFF의 `oauth2Login(Customizer.withDefaults())`이 그대로 들고 있다.
- **7장**의 OTT·MFA는 관리자 환불 흐름 안에서 factor 권한 모델 그대로 살아난다.
- **8장**의 인가 다섯 층은 URL 인가 + 메서드 보안 + (필요 시) 도메인 객체 보안의 결합으로 ShopVault의 백엔드에 새겨졌다.
- **9장**의 CSRF·CORS·헤더는 BFF의 `csrf(... .spa)` + HSTS + CSP에 묶였다.
- **10장**의 세션·쿠키는 BFF의 `HttpOnly·Secure·SameSite` 한 줄에 응축됐다.
- **11장**의 Reactive 보안은 Spring Cloud Gateway 위에서 `SecurityWebFilterChain`이 도는 그 자리에서 작동한다.
- **12장**의 테스팅 패턴은 운영 체크리스트의 회귀 안전망 다섯 시나리오로 들어갔다.
- **13장**의 마이그레이션 어휘는 이 책의 모든 코드가 7.0 GA 시그니처로 적혔다는 사실 자체로 증명된다.
- **14장**의 Zero Trust·BFF·운영 어휘는 ShopVault의 전체 아키텍처와 운영 체크리스트 그 자체다.

한 권의 어휘가 한 시스템에 다 녹았다. 책 한 권이 책장에 꽂힌 채로 끝나지 않고, 우리가 손으로 짠 코드 안에 살아남았다. 그 사실이 이 책이 마지막에 우리에게 줄 수 있는 가장 솔직한 선물이다.

## 15.13 책을 덮은 뒤 — 어디서 더 읽을 것인가

이 책은 여기까지다. 그러나 Spring Security는 여기서 멈추지 않는다. 7.1.x milestone이 이미 굴러가고 있고, 8.0이 어딘가 먼 길 위에 있다. 우리가 책을 덮은 뒤 어디서 더 읽으면 좋을지 짧게 적어 두자.

**가장 먼저 들를 곳은 공식 docs다.** `docs.spring.io/spring-security/reference/whats-new.html`은 7.0 GA 이후의 변경이 차곡차곡 쌓이는 자리다. 이 책이 출간된 뒤 새로 들어오는 API는 거기서 가장 빠르게 본다. 그다음은 Spring 공식 블로그(`spring.io/blog`)다. 큰 변화가 있을 때마다 팀이 글을 올린다. 2025-10-21의 MFA 글이 좋은 예다.

**표준 문서도 같이 펴자.** RFC 9700(OAuth 2.0 Security BCP), RFC 8725(JWT BCP), RFC 9449(DPoP), NIST SP 800-207(Zero Trust). 이 네 개 문서가 이 책 전체의 베이스 라인이다. Spring Security는 이 표준들의 한국어 구현체에 가깝다 — 표준을 같이 읽으면, 라이브러리의 다음 행보를 미리 짐작할 수 있다.

**검증된 저자 블로그 묶음.** Baeldung(`baeldung.com`)은 7.0 API의 코드 예제가 가장 빠르게 올라온다. Curity(`curity.io`)의 token handler pattern 시리즈는 BFF를 더 깊게 보고 싶을 때. Dimitri Mes의 블로그는 7.0 deep-dive가 자주 올라온다. 한국어 자료는 — 2025년 말 시점 아직 deep-dive가 적다. velog 단편글이 시행착오 사례로는 가치가 있지만, 어휘를 잡는 자료로는 한계가 있다. 1~2년 안에 카카오/토스 기술블로그에서 7.x deep-dive가 올라올 것을 기대해 보자.

**7.1.x 추적은 GitHub로.** `github.com/spring-projects/spring-security`의 milestone 페이지가 가장 빠르다. issue tracker의 `team/oauth2`, `team/web-security` 라벨을 follow해 두면, 책에서 다룬 API의 추가 보강이 일어날 때 알람이 온다. 이 책 본문이 "7.0 GA 기준"이라 못 박은 부분이 7.1.x에서 어떻게 보강되는지, 거기서 직접 확인하자.

## 15.14 마무리 — 그리고 이 책을 덮는 한 마디

길고 긴 여행이었다. 솔직히 말하면, 이 책을 쓰는 사람의 자리에서도 마지막 장을 쓰는 순간이 가장 후련하다. 1장에서 약속한 모든 것이 이제 우리 손 안에 있다. Spring Security 7.0의 큰 그림, 함정 5건, 5장에 걸친 인증 시나리오, 8장의 인가, 횡단 관심사 셋, Reactive, 테스팅, 마이그레이션, 트렌드, 그리고 통합. 책 한 권이 한 도구의 GA를 따라가는 한 사이클을 닫았다.

기억해 두자. 보안은 단번에 끝나는 일이 아니다. 표준은 매년 갱신되고, 라이브러리는 minor마다 깎이고, 함정은 새로 생긴다. 이 책이 마지막에 줄 수 있는 가장 정직한 약속은 "당신이 이 책을 덮은 시점부터 6개월 안에 7.1.x 안에서 무언가가 바뀐다"는 사실이다. 그 변화를 두려워하지 말자. 우리가 1~14장에서 박아 둔 어휘가 그대로 살아 있으면, 6개월 뒤에 바뀐 API의 시그니처를 만났을 때 우리는 "아, 이 자리에 새 도구가 들어왔구나"라고 즉시 알아본다. 이 책이 정말 약속하고 싶었던 것은 그것이다. 코드 한 줄이 아니라 어휘 한 단어. 시그니처가 아니라 의미. 그래서 라이브러리가 바뀌어도 우리가 같이 바뀔 수 있다.

ShopVault는 가상의 가게지만, 그 가게의 코드를 손에 쥔 우리는 가상이 아니다. 이 책을 덮고 자기 팀의 코드로 돌아갔을 때, 우리는 이전과는 조금 다른 눈으로 그 코드를 본다. `SecurityFilterChain` 한 줄 앞에서 잠시 멈추고, 두 체인으로 나눌 자리를 가늠해 본다. `localStorage`에 JWT가 들어가 있는 자리에서는 가슴이 잠시 답답해진다. `WebSecurityConfigurerAdapter`라는 단어가 PR 어딘가에서 보이면 손이 자연스럽게 그 줄을 들어낸다. 그 작은 변화가 사실은 이 책이 노린 가장 정확한 효과다.

이 책을 덮고 무엇을 만들지는 이제 당신에게 달렸다. 그리고 그것이 가장 즐거운 일이다.

— 끝.
