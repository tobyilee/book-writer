# 5장. JWT 자원 서버 — Bearer 토큰의 끝까지, 그리고 sender-constrained로

JWT라는 단어를 들으면 마음이 두 갈래로 갈라진다. 한쪽은 stateless의 아름다움이다. 서버에 세션 저장소가 필요 없고, 토큰만 들고 있으면 어떤 인스턴스든 그 요청을 처리할 수 있다. 마이크로서비스 사이를 옮겨다닐 때마다 사용자 정보를 다시 묻지 않아도 된다. 다른 한쪽은 운영에서 만난 함정들이다. 강제 로그아웃이 안 된다거나, XSS 한 번에 토큰이 새거나, `alg: none`을 받아들이는 서버가 발견되었다는 보안 보고서가 떠오른다.

이 두 얼굴을 동시에 봐야 한다. JWT는 안 쓸 수 있는 기술이 아니다. 시중에서 가장 많이 쓰이는 토큰이고, 마이크로서비스를 한 줄로 묶는 표준 어휘다. 그렇다면 어떻게 해야 할까? 한 번에 둘 다 보자. 안전하게 도입하는 정석을 먼저 익히고, 흔히 빠지는 함정 네 개를 코드 레벨에서 풀어낸 다음, Bearer 토큰의 본질적 한계를 짚고 그 다음 단계인 sender-constrained 토큰(DPoP)으로 마무리한다. 한 챕터 안에서 "Bearer의 끝"에서 "Bearer 너머"로 건너가 보자.

## 5.1 한 줄로 끝나는 자원 서버 — 그러나 그 한 줄이 하는 일

Spring Security 7로 가장 단순한 JWT 자원 서버를 구성하면 코드는 이렇게 줄어든다.

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

`application.yml`은 더 짧다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
```

이게 전부다. 사용자가 `Authorization: Bearer eyJhbG...` 헤더를 달아 보내면, 이 한 묶음이 토큰의 서명을 검증하고, 만료를 확인하고, 발급자가 우리가 신뢰하는 그 IdP가 맞는지 확인한 뒤, `Authentication` 객체를 만들어 `SecurityContext`에 꽂아 준다. 컨트롤러는 `@AuthenticationPrincipal Jwt jwt`로 토큰을 받거나 `Authentication`을 주입받아 일을 시작한다.

여기까지만 보면 마치 마법 같다. 그렇다면 그 마법의 안쪽은 어떻게 생겼을까? 한 줄 한 줄 뜯어보자. 이 안쪽을 모르면, 함정에 빠졌을 때 어디서 빠진 건지 추적할 수 없다.

### `oauth2ResourceServer(o -> o.jwt(...))`가 하는 일

이 한 줄이 필터 체인에 `BearerTokenAuthenticationFilter`와 `JwtAuthenticationProvider`를 동시에 꽂는다. 2장에서 본 인증 흐름을 떠올려 보자. 필터가 요청에서 인증 정보를 뽑아 `AuthenticationToken`을 만들고, `AuthenticationManager`에 위임하고, `AuthenticationProvider`가 실제 검증을 수행한다. JWT의 경우 이 셋이 다음처럼 묶인다.

| 컴포넌트 | 역할 |
|---------|------|
| `BearerTokenAuthenticationFilter` | `Authorization: Bearer ...` 헤더(또는 `access_token` 폼·쿼리)에서 토큰 추출 |
| `BearerTokenAuthenticationToken` | 미인증 상태의 토큰 객체 |
| `JwtAuthenticationProvider` | `JwtDecoder.decode(...)`로 검증 + `JwtAuthenticationConverter`로 권한 매핑 |
| `JwtDecoder` | 서명·만료·발급자 검증의 실제 일꾼 |

핵심은 `JwtDecoder`다. 이 친구가 토큰의 진위 여부를 책임진다. 그리고 이 친구를 만드는 것이 바로 `issuer-uri` 한 줄이다.

### `JwtDecoders.fromIssuerLocation` — 한 줄이 만드는 네 가지 일

`issuer-uri: https://auth.example.com/realms/app` 한 줄을 적으면 Spring Security가 자동으로 `JwtDecoders.fromIssuerLocation(...)`을 호출한다. 이 한 메서드가 네 가지 일을 한다.

첫째, OIDC discovery 문서를 가져온다. `https://auth.example.com/realms/app/.well-known/openid-configuration`에 GET 요청을 보내 IdP가 자기 자신을 어떻게 소개하는지 읽는다. 여기에는 `issuer`, `jwks_uri`, `authorization_endpoint`, 지원하는 알고리즘 등이 들어 있다.

둘째, `jwks_uri`에서 JWKs(JSON Web Key Set)를 가져온다. IdP가 토큰 서명에 쓰는 공개키 집합이다. `kid`(key id)로 각 키를 식별할 수 있도록 되어 있다.

셋째, JWKs를 캐시한다. 매 요청마다 IdP에 공개키를 다시 묻는 일은 끔찍한 일이다. 트래픽도 늘고 IdP가 다운되면 전체 자원 서버가 죽는다. Spring Security는 캐시를 가지고 있다가 `kid`로 적중하지 않을 때만 다시 가져오는 식으로 동작한다.

넷째, `NimbusJwtDecoder`를 만들어 빈으로 등록한다. 이 디코더가 `iss`, `exp`, `nbf` 같은 기본 클레임을 자동 검증한다.

이 네 가지가 한 줄에 들어 있다. 다른 말로 하면, 이 한 줄을 적기 전에 IdP의 OIDC discovery가 켜져 있어야 한다. 자체 발급 IdP를 쓰는데 discovery 엔드포인트가 없다면 한 줄로 끝나지 않는다. 그땐 `jwk-set-uri`만 따로 지정하거나 `JwtDecoder`를 직접 빈으로 등록해야 한다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: https://auth.example.com/keys
```

`jwk-set-uri`만 적으면 discovery를 건너뛰고 JWKs만 가져온다. 다만 `iss` 검증은 자동으로 일어나지 않으니, `JwtDecoder`에 `OAuth2TokenValidator`를 직접 끼워 발급자 검증을 추가하는 편이 낫다.

### Spring Security 7에서 새로 생긴 두 가지 — `NimbusJwtDecoder` 커스텀 JwkSource와 `NimbusJwtEncoder` 빌더

7.0에서는 `NimbusJwtDecoder`가 커스텀 `JwkSource`를 받을 수 있게 되었다. 표준 JWKs URL 캐시를 그대로 두고 싶지만, 회전 정책이나 폴백 키 로직을 직접 짜야 하는 환경에서는 이 확장점이 매우 유용하다.

```java
@Bean
JwtDecoder jwtDecoder(JwkSource<SecurityContext> jwkSource) {
    return NimbusJwtDecoder.withJwkSource(jwkSource)
        .jwsAlgorithms(algs -> {
            algs.add(SignatureAlgorithm.RS256);
            algs.add(SignatureAlgorithm.ES256);
        })
        .build();
}
```

또 하나, `NimbusJwtEncoder`의 빌더가 생겼다. RSA·EC·secret key를 빌더로 선언하고 `JwtEncoderParameters`를 넣어 토큰을 발급할 수 있다. 자원 서버는 보통 토큰을 발급하는 쪽이 아니지만, 뒤에서 다룰 DPoP의 `DPoP` 헤더(클라이언트가 만드는 proof JWT)나 통합 테스트용 토큰 발급, 그리고 자체 마이크로서비스 간 토큰 발급에 그대로 쓸 수 있다.

```java
@Bean
NimbusJwtEncoder jwtEncoder(JWKSource<SecurityContext> jwkSource) {
    return new NimbusJwtEncoder(jwkSource);
}
```

이 두 가지 변화 덕분에 7.0에서는 "Spring Boot의 기본 설정"에서 한 발만 비켜나도 결국 직접 만들어야 했던 boilerplate가 크게 줄었다. 6.x까지는 키 회전 로직을 직접 짜려면 `NimbusJwtDecoder`를 우회해 `Nimbus` SDK를 통째로 임포트해야 했는데, 7.0에서는 Spring Security의 추상 안에서 끝낸다.

### `STATELESS` 한 줄의 의미

`sessionManagement(s -> s.sessionCreationPolicy(STATELESS))`를 적으면 Spring Security는 이 체인 안에서 세션을 만들지도, 읽지도 않는다. `HttpSession`이 생기지 않고, `JSESSIONID` 쿠키도 발급되지 않는다. 이게 stateless의 본질이다.

여기서 한 가지를 짚고 가자. `STATELESS`는 "Spring Security가 세션을 안 쓴다"는 뜻이다. 애플리케이션 코드에서 `request.getSession()`을 호출하면 그건 그대로 만들어진다. 가끔 "stateless인데 왜 JSESSIONID가 나오죠"라는 질문을 받는데, 거의 대부분 컨트롤러 어딘가에서 세션을 만들고 있다. JWT 자원 서버라면 컨트롤러나 인터셉터에서 세션을 건드리지 않는 편이 낫다.

### CSRF disable이 안전한 이유 — 그리고 안 안전한 경우

`csrf(CsrfConfigurer::disable)`도 같이 꽂혀 있다. JWT 자원 서버에서 CSRF가 안전하게 꺼지는 이유는 단순하다. CSRF 공격은 "브라우저가 자동으로 첨부하는 인증 정보"를 악용하는 공격이다. 쿠키는 브라우저가 자동으로 첨부한다. 그러나 `Authorization: Bearer` 헤더는 브라우저가 자동으로 붙여 주지 않는다. 자바스크립트가 명시적으로 헤더를 적어야 한다. 그래서 CSRF가 자연스럽게 무력화된다.

다만 한 가지 경우엔 찜찜하다. 토큰을 쿠키에 담아 보내고 서버가 쿠키에서 토큰을 읽도록 만들어 둔 경우다. 이때는 다시 쿠키 기반이 되니까 CSRF가 살아난다. "토큰을 쿠키에 담는데 CSRF disable로 두자"는 결정은 처음부터 다시 생각하는 편이 낫다. 5.3절 함정 7에서 다시 본다.

## 5.2 권한 매핑 — `scope`/`scp`에서 커스텀 `roles`까지

토큰의 서명이 검증되었다고 끝나는 것이 아니다. 이 토큰을 가진 사람이 무엇을 할 수 있는지를 결정해야 한다. Spring Security의 인가는 `Authentication`에 들어 있는 `GrantedAuthority` 컬렉션을 본다. JWT의 어떤 클레임이 이 컬렉션으로 바뀌는지가 권한 매핑의 핵심이다.

기본 동작은 단순하다. 토큰의 `scope` 또는 `scp` 클레임을 자동으로 `SCOPE_*` 권한으로 매핑한다. `scope: "read write admin"`이라는 토큰이 들어오면 `SCOPE_read`, `SCOPE_write`, `SCOPE_admin` 세 권한이 부여된다. URL 인가에서는 이렇게 쓸 수 있다.

```java
.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET, "/api/items").hasAuthority("SCOPE_read")
    .requestMatchers(HttpMethod.POST, "/api/items").hasAuthority("SCOPE_write")
    .anyRequest().authenticated())
```

여기까지가 표준 OAuth2 어휘다. 그런데 현실에서는 `roles`라는 커스텀 클레임을 쓰는 IdP가 많다. Keycloak, Auth0, Okta 모두 자기 입맛대로 클레임을 추가한다. 이때 손을 봐줘야 한다.

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

`JwtGrantedAuthoritiesConverter`가 `roles` 클레임을 읽어 `ROLE_*` 접두어를 붙여 권한으로 만든다. 그 다음 `hasRole("ADMIN")`은 내부적으로 `ROLE_ADMIN` 권한을 찾는다. 이 짝을 맞추지 않으면 권한이 분명 토큰에 있는데도 403이 떨어진다. "분명히 admin 롤인데 왜 403이지?"라는 질문이 가장 자주 나오는 자리가 바로 여기다.

`hasAuthority`와 `hasRole`의 차이를 한 번 더 짚어 두자. `hasAuthority("ADMIN")`은 권한 이름이 정확히 `ADMIN`인지 본다. `hasRole("ADMIN")`은 자동으로 `ROLE_` 접두어를 붙여 `ROLE_ADMIN`을 찾는다. 변환기에서 `setAuthorityPrefix("ROLE_")`를 적었다면 `hasRole`을, 안 적었다면 `hasAuthority`로 풀네임을 적는 편이 일관성 있다.

### 중첩된 클레임 — Keycloak의 `realm_access.roles`

조금 더 까다로운 경우가 있다. Keycloak은 권한을 `realm_access.roles` 같은 중첩된 구조에 담는다. `JwtGrantedAuthoritiesConverter`는 일차원 배열만 지원하기 때문에 이 경우엔 변환기를 직접 짜야 한다.

```java
@Bean
JwtAuthenticationConverter keycloakJwtAuthConverter() {
    var conv = new JwtAuthenticationConverter();
    conv.setJwtGrantedAuthoritiesConverter(jwt -> {
        Map<String, Object> realm = jwt.getClaim("realm_access");
        if (realm == null) return List.of();
        Collection<String> roles = (Collection<String>) realm.get("roles");
        if (roles == null) return List.of();
        return roles.stream()
            .map(r -> new SimpleGrantedAuthority("ROLE_" + r))
            .collect(Collectors.toList());
    });
    return conv;
}
```

매 요청마다 도는 코드이므로 캐스팅 안전성에 신경 쓰는 편이 낫다. 한 IdP를 정해 변환기를 한 번 짠 다음, 사내 공유 라이브러리로 빼서 모든 자원 서버가 같은 변환을 쓰도록 만드는 편이 가장 깔끔하다.

### 변환기를 직접 갈아 끼우기 — `setJwtAuthenticationConverter` vs `Converter<Jwt, AbstractAuthenticationToken>`

권한만 바꾸는 것이 아니라 토큰을 어떤 `Authentication` 객체로 만들지를 통째로 바꾸고 싶을 때가 있다. 가령 토큰의 `sub`을 우리 도메인의 `UserId`로 정규화하거나, `preferred_username` 대신 우리 DB의 사용자 ID를 `principal`로 쓰고 싶다거나. 그땐 `JwtAuthenticationConverter`를 통째로 갈아 끼울 수 있다.

```java
Converter<Jwt, AbstractAuthenticationToken> converter = jwt -> {
    var authorities = extractRoles(jwt);
    var principal = userResolver.resolve(jwt.getSubject());
    return new JwtAuthenticationToken(jwt, authorities, principal.getUsername());
};
http.oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(converter)));
```

다만 한 가지 주의할 점이 있다. 이 변환기는 매 요청 호출된다. 여기서 DB를 친다거나 외부 호출을 한다면 모든 요청 지연이 그만큼 늘어난다. 단순 캐싱이라도 끼워 두지 않으면 트래픽이 늘었을 때 끔찍한 일이 벌어진다. 가능하면 토큰 안에 있는 정보만으로 끝내고, DB가 필요한 결정은 컨트롤러 레벨에서 하는 편이 낫다.

## 5.3 Opaque Token + Introspection — JWT의 반대편

JWT가 모든 답은 아니다. JWT의 단점 하나가 강제 로그아웃이 어렵다는 것인데, 이 단점을 정면으로 해결하는 토큰이 불투명 토큰(opaque token)이다. 토큰 자체엔 의미가 없고, 그저 임의의 문자열이다. 서버가 토큰을 받으면 IdP의 introspection 엔드포인트(`POST /introspect`, RFC 7662)에 "이 토큰 살아 있나요? 권한은 뭐죠?"라고 묻는다. IdP가 응답을 돌려준다.

Spring Security 7에서는 이렇게 쓴다.

```java
http.oauth2ResourceServer(o -> o.opaqueToken(t -> t
    .introspectionUri("https://auth.example.com/oauth2/introspect")
    .introspectionClientCredentials("resource-server-id", "secret")));
```

`application.yml`로도 쓸 수 있다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        opaquetoken:
          introspection-uri: https://auth.example.com/oauth2/introspect
          client-id: resource-server-id
          client-secret: change-me
```

장단점이 분명하다. 장점은 강제 무효화가 즉시 반영된다. IdP에서 토큰을 폐기하면 다음 introspection이 `active: false`를 돌려준다. 단점은 매 요청마다 IdP에 네트워크 호출이 일어난다는 것이다. 트래픽이 늘면 IdP가 병목이 되고, IdP가 죽으면 자원 서버 전체가 죽는다.

이 단점을 완화하는 정석이 캐시다. Spring Security 7은 `OpaqueTokenIntrospector`를 빈으로 끼울 수 있게 해 두었으니, 캐싱 디코레이터를 한 번만 짜 두면 된다.

```java
@Bean
OpaqueTokenIntrospector cachingIntrospector() {
    var delegate = new SpringOpaqueTokenIntrospector(introspectionUri, clientId, secret);
    return new CachingOpaqueTokenIntrospector(delegate, Duration.ofMinutes(1));
}
```

`CachingOpaqueTokenIntrospector`는 Spring이 기본 제공하지 않으니 직접 짜야 한다. 핵심은 토큰을 키로 결과를 짧게 캐시하는 것이다. 캐시 만료를 너무 길게 잡으면 강제 로그아웃의 즉시성이 사라지므로, 1분 안팎이 보통의 절충점이다. 강제 로그아웃이 1분 이내 반영되면 충분하다는 정책이 운영 측에서 합의되어야 한다.

그렇다면 JWT와 불투명 토큰 중 무엇을 골라야 할까? 정답은 "둘 다 같이"인 경우가 많다. 마이크로서비스 사이는 stateless JWT로 빠르게 흐르고, 사용자 직접 노출 엔드포인트(특히 admin/billing 등 폐기가 시급한 영역)는 불투명 토큰으로 닫는 식이다. 둘을 섞을 때는 `securityMatcher`로 체인을 분리하는 편이 가장 깔끔하다.

## 5.4 JWT 함정 네 가지 — 가장 많이 보는 안티패턴

여기서부터가 이번 장의 무게중심이다. 위에서 본 정석은 한 번 익혀 두면 그대로 쓰면 된다. 문제는 정석을 알면서도 한 발씩 미끄러져 만들어지는 함정들이다. 네 개를 차례로 보자. 각각 "이런 코드를 본 적이 있는가"로 시작해서, 왜 위험한지 풀어내고, 어떻게 고치는지를 코드로 보여 준다.

### 함정 1 — JWT를 세션 토큰처럼 쓰는 경우

이런 코드를 본 적이 있는가? 사내 모놀리스에서 JWT를 발급해 쓰는데, 토큰 만료가 두 시간이고, 토큰 안에는 `sub`과 `roles` 정도밖에 없다. 사용자가 비밀번호를 바꿔도 그 시점에 발급된 토큰은 그대로 유효하다. 관리자가 어떤 사용자를 강제로 로그아웃시키려고 해도 토큰이 살아 있는 동안에는 방법이 없다.

> "Some experts argue that JWTs which just store a simple session token are inefficient and less flexible than a regular session cookie, and don't gain you any advantage." — GitHub Gist, Samsch

이건 사실 JWT의 결함이 아니라 **JWT를 안 어울리는 자리에 쓴 결과**다. 세션은 본질적으로 stateful이다. 강제 무효화가 가능해야 하고, 권한 변경이 즉시 반영되어야 한다. JWT는 정반대다. 서명된 그 시점의 정보를 그대로 들고 다닌다. 두 모델을 합치려는 시도가 함정 1을 만든다.

그렇다면 어떻게 해야 할까? 두 가지 길이 있다.

**해법 A — 짧은 access token + refresh token 회전.** Access token을 5~15분으로 짧게 잡고, refresh token으로 갱신한다. 강제 로그아웃이 필요하면 refresh token 쪽을 폐기하면 다음 갱신에서 끊긴다. 즉시성은 access token 수명만큼 늦지만, 5분 이내 반영되면 대부분의 운영 정책에 충분하다.

**해법 B — JWT는 그대로 두고 블랙리스트 캐시.** JWT의 `jti`(고유 ID) 클레임을 Redis 같은 저장소에 폐기 표시로 남긴다. 자원 서버가 토큰을 검증한 다음, `jti`가 블랙리스트에 있으면 거부한다. 매 요청 Redis를 한 번 더 친다는 점에서 stateless의 매력은 줄지만, 즉시성은 살아난다.

```java
@Bean
JwtDecoder jwtDecoder(JWTProcessor<SecurityContext> processor, RevokedJtiStore store) {
    var decoder = new NimbusJwtDecoder(processor);
    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
        JwtValidators.createDefaultWithIssuer(issuer),
        new RevokedJtiValidator(store)
    ));
    return decoder;
}

class RevokedJtiValidator implements OAuth2TokenValidator<Jwt> {
    private final RevokedJtiStore store;
    public OAuth2TokenValidatorResult validate(Jwt jwt) {
        String jti = jwt.getId();
        if (jti != null && store.isRevoked(jti)) {
            return OAuth2TokenValidatorResult.failure(
                new OAuth2Error("invalid_token", "Revoked", null));
        }
        return OAuth2TokenValidatorResult.success();
    }
}
```

여기서 한 가지 기억해 둘 점이 있다. 이 두 해법은 결국 stateless의 일부를 포기한 것이다. 그게 잘못된 결정은 아니다. 다만 "JWT를 쓰면 무조건 stateless"라는 신화를 깨고, "어디까지 stateless로 갈지를 의식적으로 결정한다"는 자세를 갖는 편이 낫다.

### 함정 2 — `localStorage`에 JWT 저장하기

이런 코드를 본 적이 있는가? 로그인 응답에서 받은 JWT를 SPA가 `localStorage.setItem('token', resp.token)`으로 저장한다. 이후 모든 fetch 호출에서 `Authorization: Bearer ${localStorage.getItem('token')}` 헤더로 토큰을 보낸다. 깔끔해 보이고, 만들기도 쉽다.

문제는 XSS다. 사이트 어딘가 하나라도 사용자 입력을 그대로 렌더하는 곳이 있으면 — 댓글, 검색어, 프로필 입력 — 공격자가 스크립트를 주입해 `localStorage.getItem('token')`을 자기 서버로 보낼 수 있다. XSS 한 번이면 끝이다. HttpOnly 쿠키는 자바스크립트에서 못 읽지만, `localStorage`는 같은 도메인 모든 스크립트에 열려 있다.

그렇다면 어디에 토큰을 둬야 할까? 세 가지 답이 있다.

**답 1 — HttpOnly·Secure·SameSite 쿠키.** 가장 표준적인 답이다. 자바스크립트에서 못 읽고, 브라우저가 요청에 자동으로 첨부한다. 다만 CSRF가 다시 살아나니까 CSRF 토큰을 같이 보내야 한다. 9장에서 더 깊이 본다.

**답 2 — 메모리에만 둔다.** 토큰을 자바스크립트 변수로만 들고, 새로고침 시 다시 인증한다. XSS에 대한 노출 시간을 페이지 라이프타임으로 줄인다. 다만 UX가 떨어지고, 새 탭이 열리면 다시 로그인이 필요하다.

**답 3 — BFF로 토큰을 브라우저에서 완전히 분리.** Backend-for-Frontend가 OAuth 클라이언트 역할을 하고, 브라우저는 자기 도메인의 HttpOnly 세션 쿠키만 가진다. 토큰은 BFF 서버에만 존재한다. SPA의 보안 모델로는 사실상 정답에 가깝다. 14장에서 BFF 패턴을 다룬다.

요약하자면 이렇다.

| 저장 위치 | XSS 노출 | CSRF 노출 | UX |
|----------|---------|----------|----|
| `localStorage` | 매우 높음 | 낮음 | 좋음 |
| `sessionStorage` | 매우 높음 | 낮음 | 보통 |
| 메모리 변수 | 낮음(페이지 단위) | 낮음 | 나쁨(새로고침 시 로그인) |
| HttpOnly 쿠키 | 없음(직접 탈취 불가) | 있음(대응 필요) | 좋음 |
| BFF(서버 측 저장) | 없음 | 있음(대응 가능) | 좋음 |

`localStorage`만 빨강이다. 한 번 새면 끝이라는 점에서 다른 옵션과 차원이 다르다. "JWT는 무조건 `localStorage`"라는 옛 튜토리얼은 잊는 편이 낫다.

### 함정 3 — `alg: none` 또는 알고리즘 confusion

이런 코드를 본 적이 있는가? 오래된 JWT 라이브러리를 쓰는 서버에서 `verify(token, publicKey)`를 호출했는데, 라이브러리가 토큰의 `alg` 헤더를 보고 "이건 `none`이니 서명 검증 안 함"이라고 판단해 통과시켜 준다. 또는 RSA로 서명된 토큰을 받기로 했는데, 공격자가 `alg`를 `HS256`으로 바꿔 RSA 공개키를 HMAC 키로 사용해 서명한 토큰을 보낸다.

이 두 가지가 JWT의 가장 유서 깊은 함정이다. RFC 8725(JSON Web Token Best Current Practices)가 첫 번째와 두 번째 권고로 정확히 이 둘을 짚고 있다.

> RFC 8725 권고 — 첫째, `alg: none`을 절대 받아들이지 말 것. 둘째, 서버가 알고리즘 화이트리스트를 강제할 것. 셋째, key confusion(HMAC 키를 공개키로 검증하는 식)을 방지할 것.

Spring Security의 `NimbusJwtDecoder`는 기본적으로 안전한 쪽으로 구성되어 있다. `JwtDecoders.fromIssuerLocation(...)`은 OIDC discovery에서 IdP가 지원하는 알고리즘 목록을 읽어 그것만 허용한다. 그러나 `JwtDecoder`를 직접 빈으로 등록할 때 흔하게 실수가 나온다. 다음 코드를 보자.

```java
// 위험 — alg 검증 없이 모든 알고리즘 허용
@Bean
JwtDecoder unsafeDecoder() {
    return token -> {
        var jwt = SignedJWT.parse(token);
        // 검증 없이 클레임만 꺼냄
        return new Jwt(token, ..., jwt.getJWTClaimsSet().getClaims());
    };
}
```

이건 극단적인 안티패턴이지만, 실제로 "토큰 디버깅"을 위해 임시로 짠 코드가 프로덕션에 흘러가는 사고가 있다. 정석은 이렇다.

```java
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder
        .withJwkSetUri("https://auth.example.com/keys")
        .jwsAlgorithms(algs -> algs.add(SignatureAlgorithm.RS256))  // 화이트리스트
        .build();
}
```

`jwsAlgorithms`로 명시한 알고리즘만 허용된다. `RS256`만 허용하면 공격자가 `HS256`이나 `none`으로 우회할 수 없다. 그리고 `withJwkSetUri`를 쓰면 `JWKSet` 안의 키 타입이 알고리즘과 짝이 안 맞을 때 자동으로 거부된다. RSA 공개키를 HS256으로 쓰려는 시도가 차단된다.

7.0에서 새로 생긴 `NimbusJwtDecoder.withJwkSource(...)`도 같은 안전 보장을 그대로 가져간다. 키 회전을 직접 짜더라도, 알고리즘 화이트리스트는 빠짐없이 적어 두는 편이 낫다.

또 한 가지 주의. 대칭키(HMAC) 기반 JWT를 쓰는 환경에서 키를 사람이 외울 수 있는 패스워드로 잡는 경우가 있다. `"my-secret-jwt-key"` 같은 식이다. RFC 8725는 약한 대칭키를 명시적으로 금지한다. HS256은 256비트(32바이트) 이상의 충분히 랜덤한 키를 써야 한다. 가능하면 비대칭(RSA/EC)으로 가는 편이 안전하다. IdP가 JWKs 회전을 지원하기도 쉽다.

### 함정 4 — Refresh Token 회전 미구현

이런 코드를 본 적이 있는가? Access token은 15분으로 짧게 잡았다. 좋다. 그런데 refresh token은 1년이다. 그리고 refresh token으로 새 access token을 요청하면, refresh token은 그대로 살아 있다. 그러면 refresh token은 사실상 1년짜리 영구 세션이다. 한 번 탈취되면 1년 내내 새 access token을 무한히 받아 갈 수 있다.

함정 4의 본질은 refresh token이 access token보다 훨씬 강한 자격증명이라는 사실을 잊는 것이다. Access token이 짧다고 안심하면 안 된다. 길게 살아 있는 refresh token이 그만큼 중요하다.

해법은 두 가지를 동시에 해야 한다.

**해법 1 — 회전(rotation).** Refresh token으로 갱신할 때마다 새 refresh token을 발급하고, 이전 토큰은 무효화한다. 정상 클라이언트는 항상 가장 최신 토큰만 가지고 있다.

**해법 2 — 재사용 감지(reuse detection).** 이미 무효화된 refresh token이 다시 들어오면, 그 사용자의 모든 refresh token을 폐기한다. 정상 클라이언트가 회전한 다음에는 옛 토큰을 절대 쓰지 않으니, 옛 토큰이 다시 들어왔다는 건 누군가가 옛 토큰을 가지고 있다는 뜻이다. 즉 탈취가 의심되는 상황이다. 가장 안전한 반응은 그 사용자의 세션을 통째로 끊고 재로그인을 요구하는 것이다.

Spring Authorization Server에서는 이 두 동작이 기본으로 들어 있다. 자체 발급 IdP를 만들 때는 직접 구현해야 하는데, 로직 자체는 단순하다.

```java
public TokenResponse refresh(String refreshToken) {
    var stored = refreshTokenRepo.findActive(refreshToken)
        .orElseThrow(() -> reuseDetected(refreshToken));

    refreshTokenRepo.markRevoked(stored.id());

    var newAccess = jwtIssuer.issueAccess(stored.userId());
    var newRefresh = refreshTokenRepo.issueNew(stored.userId(), stored.familyId());

    return new TokenResponse(newAccess, newRefresh);
}

private RuntimeException reuseDetected(String token) {
    refreshTokenRepo.findRevoked(token).ifPresent(revoked ->
        refreshTokenRepo.revokeFamily(revoked.familyId())  // 같은 사용자 패밀리 전체 폐기
    );
    return new BadCredentialsException("refresh token reuse detected");
}
```

`familyId`를 두는 이유는 한 사용자의 토큰 체인을 식별하기 위해서다. 회전이 일어날 때마다 같은 `familyId`로 새 토큰을 발급한다. 재사용이 감지되면 같은 `familyId`의 모든 토큰을 폐기해 그 사용자를 통째로 끊는다. 사용자 입장에선 강제 재로그인이지만, 토큰 탈취 의심 상황에서 이것 외에 더 안전한 대응은 없다.

여기까지가 JWT의 네 가지 함정이다. 마지막으로 RFC 8725의 권고를 우리 코드와 맞춰 보는 표 하나로 이 절을 닫는다.

### RFC 8725 권고 매핑

| RFC 8725 권고 | Spring Security 7 대응 | 우리가 신경 쓸 것 |
|---------------|----------------------|---------------|
| `alg: none` 거부 | `NimbusJwtDecoder` 기본 거부 | 직접 디코더 짤 때 화이트리스트 명시 |
| 알고리즘 화이트리스트 | `.jwsAlgorithms(...)` | 키 타입과 알고리즘 짝 검증 |
| Key confusion 방지 | `JWKSet` 기반 디코더 | 키 타입을 디코더에 직접 전달하지 말 것 |
| 약한 대칭키 금지 | — | HS256 키는 32바이트 이상 랜덤, 가능하면 비대칭으로 |
| 모든 클레임 검증 (`iss`, `aud`, `exp`, `nbf`) | `JwtValidators.createDefault[WithIssuer]` | `aud` 검증을 잊지 말 것(자원 서버 식별) |
| 페이로드는 평문 | — | PII·비밀을 클레임에 넣지 말 것 |

`aud` 검증이 비어 있는 경우가 의외로 많다. 같은 IdP가 여러 자원 서버에 토큰을 발급할 때, 자원 서버 A가 자원 서버 B용 토큰을 받아도 그냥 통과시킨다. 일종의 권한 상승 통로가 된다. `JwtDecoder`를 직접 빈으로 등록할 때는 `audience` 검증을 꼭 추가하자.

```java
OAuth2TokenValidator<Jwt> withAudience = jwt -> {
    if (jwt.getAudience() != null && jwt.getAudience().contains("api.example.com")) {
        return OAuth2TokenValidatorResult.success();
    }
    return OAuth2TokenValidatorResult.failure(
        new OAuth2Error("invalid_token", "invalid audience", null));
};
decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
    JwtValidators.createDefaultWithIssuer(issuer),
    withAudience
));
```

## 5.5 Bearer의 본질적 한계 — 그리고 sender-constrained 토큰

여기까지가 Bearer 토큰을 안전하게 쓰는 정석이다. 권한 매핑을 정확히 하고, 함정 네 개를 다 피했다고 하자. 그런데도 여전히 남는 위험이 하나 있다. 무엇일까? 토큰이 새는 순간 끝이라는 사실이다.

Bearer 토큰의 정의가 정확히 그런 의미다. "들고 있는 사람(bearer)이 권한자다." 토큰을 가지고만 있으면, 누가 가지고 있든 쓸 수 있다. 정당한 클라이언트가 만든 요청과 공격자가 그 토큰을 훔쳐 만든 요청을 자원 서버는 구별할 수 없다. HTTPS·HttpOnly·짧은 만료·재사용 감지를 다 해도, 어쨌든 어디선가 한 번 새면 그 만료 시간만큼은 공격자가 쓸 수 있다.

이걸 바꾸려면 토큰의 성격 자체를 바꿔야 한다. "들고만 있으면 쓸 수 있는" 토큰에서 "특정 클라이언트만 쓸 수 있는" 토큰으로. 이걸 sender-constrained 토큰이라고 한다.

토큰을 잘 만들었는데도 누군가 가로채면 끝이다. 그렇다면 어떻게 해야 할까? 토큰에 "이 토큰을 만들어 달라고 한 클라이언트의 키"를 묶어 두면 된다. 자원 서버는 요청이 들어올 때마다 "이 요청을 한 사람이 그 키를 정말로 가지고 있는지"를 확인한다. 키 없이는 토큰만으로 요청을 못 만든다. 토큰이 새도 키가 안 새면 안전하다.

이 아이디어를 표준화한 것이 RFC 9449, OAuth 2.0 DPoP-Bound Tokens다. 그리고 Spring Security 7이 자원 서버 측에서 이를 1급으로 처리한다.

### DPoP의 두 조각 — 토큰의 `cnf.jkt`와 매 요청 `DPoP` 헤더

DPoP는 두 가지가 한 쌍을 이룬다.

**첫 번째 조각 — 액세스 토큰의 `cnf.jkt` 클레임.** 클라이언트가 토큰을 요청할 때 자기 공개키의 SHA-256 thumbprint(`jkt`, JWK Thumbprint)를 같이 보낸다. IdP는 발급하는 access token JWT에 `cnf.jkt`라는 클레임으로 이 thumbprint를 박아 넣는다.

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-123",
  "aud": "api.example.com",
  "exp": 1700000000,
  "cnf": {
    "jkt": "0ZcOCORZNYy-DWpqq30jZyJGHTN0d2HglBV3uiguA4I"
  }
}
```

이 토큰은 그 thumbprint에 해당하는 키 쌍을 가진 클라이언트만 쓸 수 있다는 의미가 박혀 있다.

**두 번째 조각 — 매 요청의 `DPoP` 헤더.** 클라이언트는 자원 서버에 요청할 때 `Authorization: DPoP eyJhbG...`(`Bearer` 대신 `DPoP` 스킴) 헤더와 함께, `DPoP` 헤더에 별도의 JWT(DPoP proof)를 담아 보낸다. 이 proof JWT는 클라이언트가 자기 개인키로 서명한 짧은 JWT이고, 다음 클레임을 가진다.

| 클레임 | 의미 |
|--------|------|
| `htm` | HTTP 메서드 (예: `GET`) |
| `htu` | HTTP URI (예: `https://api.example.com/items`) |
| `iat` | 발급 시각 (보통 ±60초 윈도우 내) |
| `jti` | 고유 ID — 자원 서버가 재사용 방지에 쓸 수 있음 |
| `ath` | access token의 SHA-256 해시 — 어떤 access token에 짝지어진 proof인지 묶음 |

자원 서버는 이 proof JWT의 서명을 검증한다. 검증에 쓰는 공개키는 proof JWT의 `jwk` 헤더에 들어 있다. 그리고 그 공개키의 thumbprint가 access token의 `cnf.jkt`와 일치하는지 확인한다. 일치하면 "이 요청을 만든 사람이 토큰에 박힌 그 키를 가지고 있다"는 증명이 되는 것이다.

요약 흐름은 이렇다.

```
[Client] --(1) 토큰 요청 + 자기 공개키 thumbprint--> [IdP]
[IdP] --(2) access token (cnf.jkt 포함)--> [Client]

[Client] --(3) Authorization: DPoP <access_token>
              DPoP: <proof JWT signed by private key, with htm/htu/iat/jti/ath>
              --> [Resource Server]

[Resource Server]
  - proof JWT 서명 검증 (proof의 jwk 헤더에 있는 공개키로)
  - access token의 cnf.jkt == hash(proof.jwk) 확인
  - htm/htu가 요청과 일치하는지
  - iat가 너무 오래되지 않았는지 (±60초 등)
  - jti가 최근에 본 적 없는지 (replay 방지)
  - ath가 access token 해시와 맞는지
```

토큰만 새도 공격자는 클라이언트의 개인키가 없어 proof를 만들 수 없다. 토큰이 sender-constrain된다.

### Spring Security 7에서의 1급 처리

7.0은 이 검증 흐름을 자원 서버 측에서 표준 컴포넌트로 처리한다. 공식 docs의 dpop-tokens 페이지가 자원 서버 구성을 다룬다. 본질적으로는 `oauth2ResourceServer`의 JWT 디코더가 `cnf.jkt`와 `DPoP` 헤더를 짝지어 검증할 수 있도록 확장된 형태다.

```java
// 책 출간 시점의 7.x 정확한 시그니처는 공식 docs 재확인 필요
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o
            .jwt(Customizer.withDefaults())
            // DPoP를 1급으로 처리
        )
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .build();
}
```

7.0 GA(2025-11-17)에 기본 도입되었지만, 7.1.x 마일스톤에서 시그니처가 일부 다듬어질 수 있다. 책의 정확한 코드는 출간 시점에 공식 `dpop-tokens.html` 문서를 한 번 더 확인하는 편이 낫다. 핵심 개념은 안정되어 있다.

클라이언트 측에서 DPoP proof를 만들 때 7.0의 `NimbusJwtEncoder` 빌더가 그대로 쓰인다. 자기 EC 키 쌍을 만들고, 빌더에 키를 등록하고, `htm`/`htu`/`iat`/`jti`/`ath`를 클레임으로 채워 매 요청 발급한다. 공식 docs에 예제가 포함되어 있다. 클라이언트가 Spring Security 7을 함께 쓴다면 자원 서버와 발급 코드가 같은 추상 위에서 돌아간다.

### DPoP의 한계와 호환성

DPoP가 모든 답은 아니다. 몇 가지 제약을 알고 도입하는 편이 낫다.

**첫째, IdP 지원이 필요하다.** Access token에 `cnf.jkt`를 박는 것은 IdP의 일이다. Keycloak, Auth0, Okta, Spring Authorization Server가 단계적으로 DPoP를 지원하고 있다. 지원이 안 되는 IdP에서는 자원 서버만으로는 도입할 수 없다.

**둘째, 클라이언트 구현 복잡도가 올라간다.** 매 요청 proof JWT를 만들어야 한다. SPA에서는 WebCrypto API로 EC 키를 만들고 IndexedDB에 저장하는 식인데, 키 관리 로직 자체가 만만치 않다. 모바일 앱은 OS 키스토어에 키를 두는 식으로 비교적 깔끔하다.

**셋째, mTLS와 역할이 겹친다.** 클라이언트 인증서 기반 mTLS(RFC 8705)도 sender-constraining의 표준 방법이다. mTLS는 인프라 레벨(TLS terminator)에서 잡고, DPoP는 애플리케이션 레벨에서 잡는다는 차이가 있다. BFF 같은 confidential client는 mTLS가, 모바일·SPA처럼 인프라 통제가 약한 클라이언트는 DPoP가 더 자연스럽다.

**넷째, 모든 요청에서 검증이 일어난다.** Proof JWT 파싱과 서명 검증이 매 요청 도는데, 트래픽이 큰 서비스에서는 무시할 수 없는 비용이다. EC 서명(P-256)이 RSA보다 훨씬 빠르므로 키 타입을 EC로 잡는 편이 낫다.

그럼에도 불구하고 가치는 분명하다. OAuth 2.0 Security BCP(RFC 9700)가 권장하는 sender-constraining의 표준 구현이고, Bearer 토큰 모델로는 도달할 수 없는 위협 모델을 막아 준다. 토큰 탈취가 곧 계정 탈취로 이어지지 않게 만든다는 것은 운영적으로 매우 큰 안심이다. Zero Trust 원칙(NIST SP 800-207 tenet 4·6 — "동적이고 엄격한 인증·인가")과도 자연스럽게 맞아 들어간다.

도입은 단계적으로 가는 편이 낫다. 가장 민감한 자원 서버(admin·billing)부터 DPoP를 강제하고, 나머지는 Bearer를 유지하면서 차츰 늘려 간다. IdP·클라이언트·자원 서버 셋이 동시에 준비되어야 한다는 점만 잊지 않으면 된다.

## 5.6 운영 가이드라인 — 토큰 수명, 회전, 모니터링

이번 장의 정리로 운영 측 가이드라인 몇 가지를 묶어 두자. 코드 레벨에서 함정을 다 피했어도, 운영 정책이 흐트러지면 그 안전이 천천히 무너진다.

**Access token 수명.** 5~15분이 일반적인 절충점이다. 짧을수록 강제 무효화의 즉시성이 좋아지지만, refresh token 갱신 트래픽이 늘어난다. 너무 길게 잡으면(2시간 같은) 사실상 함정 1로 회귀한다.

**Refresh token 수명.** 회전이 정상 동작한다는 가정 아래 일 단위·주 단위 정도가 합리적이다. 회전이 없다면 refresh token은 그 수명만큼의 영구 세션이다.

**`aud` 클레임 검증.** 자원 서버가 여럿이면 반드시 켜자. 모든 자원 서버가 같은 IdP의 토큰을 무차별 받아들이면 권한 상승 통로가 된다.

**키 회전.** IdP의 JWKs를 자원 서버가 캐시한다. 회전 시 `kid`가 바뀌므로, 새 `kid`를 만난 자원 서버가 즉시 JWKs를 재조회하도록 디코더가 구성되어야 한다. `NimbusJwtDecoder`의 기본 동작이 이렇게 되어 있다. 직접 짠 디코더가 있다면 같은 동작을 보장하자.

**모니터링.** 거부된 토큰을 로그로 남기자. `alg` 헤더가 예상과 다른 토큰, `aud`가 다른 토큰, `cnf.jkt`가 일치하지 않는 토큰. 정상 트래픽에서는 거의 나오지 않아야 한다. 갑자기 늘어나면 공격 시도이거나 IdP 설정 실수다.

**로그에 토큰 자체를 남기지 말 것.** 끔찍하게 흔한 실수다. 인증 실패 디버깅을 위해 토큰을 통째로 로그에 찍는 사례가 있는데, 그 로그가 다른 시스템에 흘러가는 순간 토큰이 새는 것과 똑같다. 헤더 일부(앞 8자)나 `jti`만 남기는 정도가 안전선이다.

## 마무리

JWT는 매력적이지만 만만하지 않다. 한 줄로 자원 서버를 띄울 수 있다는 사실에 너무 빨리 끌려가면, 함정 네 개 중 하나에 다시 빠지기 쉽다. 이번 장에서 본 정석을 한 번 더 정리해 두자.

`issuer-uri` 한 줄이 OIDC discovery부터 JWKs 캐시·검증 디코더 등록까지 네 가지 일을 한다는 것을 기억해 두자. `STATELESS`는 Spring Security가 세션을 안 쓴다는 뜻이지, 애플리케이션이 세션을 안 쓴다는 뜻은 아니라는 점도 잊지 말자. 권한 매핑은 `scope`/`scp`가 자동이지만 커스텀 클레임은 직접 변환기를 끼워야 하고, `hasRole`과 `hasAuthority`의 짝을 맞추는 일이 가장 흔한 403의 원인이다.

함정 네 개는 코드 레벨에서 빠짐없이 점검하는 편이 낫다. JWT를 세션처럼 쓰지 말고, 강제 무효화가 필요하면 짧은 access token + refresh rotation 또는 블랙리스트로 의식적으로 결정하자. `localStorage`는 XSS 한 번이면 끝이라는 사실을 잊지 말고, HttpOnly 쿠키나 BFF로 옮기는 편이 낫다. `alg: none`과 알고리즘 confusion은 RFC 8725가 첫 번째로 경고하는 함정이고, 화이트리스트와 JWKs 기반 디코더로 막힌다. Refresh token rotation 없이 긴 수명을 잡으면 영구 세션이 되어 버린다는 점, 재사용 감지로 패밀리 전체를 폐기하는 정석을 함께 기억해 두자.

그리고 마지막으로 DPoP다. Bearer 토큰이 새는 순간 끝이라는 본질적 한계 위에, sender-constrained라는 한 층을 더 얹는 표준이다. Spring Security 7이 자원 서버 측에서 1급으로 처리한다는 것은, 우리가 Zero Trust 원칙에 한 발 더 가깝게 갈 수 있는 길이 열렸다는 의미다. 모든 자원 서버를 한 번에 바꿀 필요는 없다. 가장 민감한 영역부터, IdP·클라이언트가 준비된 순서대로 천천히 도입하자.

다음 6장에서는 자원 서버의 반대편, 즉 외부 IdP에 로그인을 위임하는 OAuth2 Client + OIDC Login의 흐름을 본다. 이번 장의 JWT 어휘 — `JwtDecoder`, `JwtAuthenticationConverter`, `Authentication` — 가 그대로 이어진다. 7.0에서 PKCE가 confidential client에도 기본 권장되는 변화부터 살펴보자.
