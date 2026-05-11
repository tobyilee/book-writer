# 11장. Reactive 보안 — WebFlux에서 다시 그리는 인증·인가

> **선행 필요:** 2장(필터 체인), 3장(컴포넌트 모델), 5장(JWT 자원 서버) 또는 8장(인가 어휘).

WebFlux 프로젝트를 처음 짤 때 가장 먼저 부딪치는 벽 중 하나가 보안이다. 컨트롤러는 `Mono`와 `Flux`로 깔끔하게 흘러가는데, `SecurityConfig`를 열어 익숙한 `HttpSecurity`를 타이핑하기 시작하면 IDE가 빨갛게 운다. `authorizeHttpRequests`도, `SecurityFilterChain`도 보이지 않는다. 익숙한 단어들이 단 한 글자씩 비틀어진 채로 거기 있다.

서블릿 책의 모든 코드가 비슷한 모양으로 옮겨질 듯하지만, `Mono`와 `Flux`가 끼어드는 순간 모서리가 보인다. `Authentication`을 꺼내려고 `SecurityContextHolder.getContext()`를 호출한 코드가 빈 컨텍스트를 돌려준다. `JwtAuthenticationConverter`를 그대로 빈으로 등록했더니 시동도 안 걸린다. 한 줄 한 줄이 잔잔히 어긋난다.

물론 어긋남은 우연이 아니다. WebFlux의 전제는 **스레드 하나가 절대로 멈추지 않는다**는 것이다. 이 약속을 지키기 위해 Spring Security 팀은 인증·인가의 모든 구성요소를 reactive 시그니처로 다시 그렸다. 이름이 비슷한 건 친절함이고, 시그니처가 비틀린 건 약속을 지키기 위한 정직함이다. 이 챕터에서는 그 비틀림의 규칙을 익히고, 서블릿에서 옮길 때 가장 자주 막히는 함정 다섯을 짚는다. 끝에 가서는 한 요청이 `AuthenticationWebFilter`를 통과해 컨트롤러 메서드까지 도달하는 길을 머릿속에 그릴 수 있게 된다.

## 11.1 같은 이름, 다른 시그니처 — 대응 매핑

먼저 어휘를 맞춰두자. 서블릿 책에서 익숙해진 이름들이 WebFlux에서 어떻게 변형되는지 한눈에 보는 것부터다. 표는 단순히 외워야 할 짝이 아니라 "왜 이렇게 갈라졌는가"를 묻는 시작점이다.

| 서블릿 (블로킹) | WebFlux (reactive) | 핵심 차이 |
|---|---|---|
| `HttpSecurity` | `ServerHttpSecurity` | DSL 진입점. 메서드 이름은 비슷하지만 반환 타입이 `Mono`로 묶인다 |
| `SecurityFilterChain` | `SecurityWebFilterChain` | 빈 타입. `WebFilter` 시퀀스를 갖는다 |
| `Filter` | `WebFilter` | 시그니처가 `Mono<Void> filter(ServerWebExchange, WebFilterChain)`로 바뀐다 |
| `AuthenticationManager` | `ReactiveAuthenticationManager` | `authenticate(...)`가 `Mono<Authentication>`을 반환 |
| `AuthenticationProvider` | `ReactiveAuthenticationManager`만 존재 | provider 추상이 사라지고 매니저 자체가 `Mono` 합성으로 위임을 표현 |
| `UserDetailsService` | `ReactiveUserDetailsService` | `findByUsername(...)`이 `Mono<UserDetails>` |
| `JwtDecoder` | `ReactiveJwtDecoder` | 디코드 결과가 `Mono<Jwt>` |
| `SecurityContextRepository` | `ServerSecurityContextRepository` | 저장/로드가 `Mono<Void>` / `Mono<SecurityContext>` |
| `SecurityContextHolder` | `ReactiveSecurityContextHolder` | ThreadLocal이 아니라 **Reactor Context**에서 꺼낸다 |
| `authorizeHttpRequests` | `authorizeExchange` | 매처 이름이 `requestMatchers` → `pathMatchers`로 |
| `@EnableMethodSecurity` | `@EnableReactiveMethodSecurity` | SpEL의 `authentication`이 `Mono`로 흘러감 |
| `HttpFirewall` | (별도 추상 없음) | reactor-netty/Tomcat 단의 검증으로 위임 |

이름이 살짝 다른 이유는 단순한 변덕이 아니다. **블로킹 호출이 가능한 메서드와 절대 블로킹해서는 안 되는 메서드를 컴파일러 수준에서 구별하기 위해서다.** 서블릿용 인터페이스 자리에 그대로 `ReactiveAuthenticationManager`를 두면, 구현체에서 무심코 `userRepository.findByUsername(...)`(JPA 동기 메서드)을 호출해도 컴파일이 통과한다. 새 이름은 "여기는 reactive 세계다. 들어올 때 신발을 갈아 신어라"라는 표시다.

기억해두자. 두 세계의 클래스를 같은 빈 컨테이너에 같이 등록하는 것은 가능하다. 그러나 한 `WebFilter` 안에서 블로킹 `JwtDecoder`를 호출하는 것은 가능해도 권장되지 않는다. 같은 단어, 다른 약속이라는 점을 잊지 말자.

### 11.1.1 가장 짧은 설정

본격적인 설명에 들어가기 전에, 우선 가장 짧은 설정 하나를 살펴보자. 서블릿의 `SecurityFilterChain`을 빈으로 등록하던 그 패턴 그대로다.

```java
@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(ex -> ex
                .pathMatchers("/actuator/health").permitAll()
                .anyExchange().authenticated())
            .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
            .csrf(ServerHttpSecurity.CsrfSpec::disable)
            .build();
    }
}
```

서블릿 코드와 거의 같은 모양이다. `@EnableWebFluxSecurity`, `ServerHttpSecurity`, `SecurityWebFilterChain` — 이 세 단어만 바꿔 끼웠다. 그런데 이 한 빈이 시동되는 순간, Spring Security는 내부적으로 무려 10개 가까운 `WebFilter`를 묶어 하나의 `SecurityWebFilterChain`을 구성한다. 그 안에서 무슨 일이 일어나는지 다음 절에서 한 발 들어가 보자.

## 11.2 진입점 셋 — `AuthenticationWebFilter`, `ReactiveAuthenticationManager`, `ServerSecurityContextRepository`

서블릿에서 인증의 주연은 셋이었다. 인증 필터(`UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter` 등), `AuthenticationManager`, `SecurityContextRepository`. WebFlux도 똑같이 셋이다. 이름과 시그니처만 비틀려 있다.

```text
ServerWebExchange
        │
        ▼
┌───────────────────────────────┐
│  AuthenticationWebFilter      │
│  ─ ServerAuthenticationConverter (요청 → 토큰)
│  ─ ReactiveAuthenticationManager (토큰 → 인증된 Authentication)
│  ─ ServerAuthenticationSuccessHandler / FailureHandler
│  ─ ServerSecurityContextRepository (저장)
└───────────────────────────────┘
        │  (Reactor Context에 SecurityContext 주입)
        ▼
   AuthorizationWebFilter / 컨트롤러
```

흐름의 순서는 서블릿과 동일하다. 다만 모든 화살표 위에 `Mono`가 얹혀 있다고 보면 된다.

### 11.2.1 `AuthenticationWebFilter`

`AuthenticationWebFilter`는 서블릿의 `AbstractAuthenticationProcessingFilter`에 해당하는 추상화다. 그러나 추상 클래스를 상속하는 게 아니라, **변환기와 매니저를 조립**해 만든다.

```java
ReactiveAuthenticationManager manager = ...;
ServerAuthenticationConverter converter = ...;

AuthenticationWebFilter filter = new AuthenticationWebFilter(manager);
filter.setServerAuthenticationConverter(converter);
filter.setRequiresAuthenticationMatcher(
    ServerWebExchangeMatchers.pathMatchers(HttpMethod.POST, "/api/login"));
filter.setSecurityContextRepository(new WebSessionServerSecurityContextRepository());
```

서블릿에서 `UsernamePasswordAuthenticationFilter`를 상속하던 코드가, 여기서는 인스턴스를 조립하는 코드로 바뀌었다. 처음 보면 어색하지만 익숙해지면 오히려 더 명료하다. "어디서 토큰을 만들고, 어디서 인증하고, 어디에 저장할 것인가"를 한 화면에서 선언하기 때문이다.

`ServerAuthenticationConverter`는 `ServerWebExchange`를 받아 `Mono<Authentication>`을 돌려준다. JWT의 `Authorization: Bearer ...` 헤더에서 토큰을 꺼내거나, 폼 파라미터에서 username/password를 추출하는 책임이 여기 산다. 서블릿의 `HttpServletRequest → Authentication` 추출 로직이 이 자리에 그대로 옮겨 온 것이다.

### 11.2.2 `ReactiveAuthenticationManager`

서블릿에서 `AuthenticationManager`의 표준 구현은 `ProviderManager`였다. 여러 `AuthenticationProvider`를 줄 세워 `supports(...)`로 분기시키는 위임 모델이었다. WebFlux에서는 provider 추상이 사라졌다. 대신 `ReactiveAuthenticationManager` 자체를 합성한다.

```java
ReactiveAuthenticationManager passwordManager = new UserDetailsRepositoryReactiveAuthenticationManager(uds);
ReactiveAuthenticationManager jwtManager = new JwtReactiveAuthenticationManager(decoder);

ReactiveAuthenticationManager delegating = new DelegatingReactiveAuthenticationManager(
    passwordManager, jwtManager);
```

`DelegatingReactiveAuthenticationManager`는 첫 번째 매니저가 `Mono.empty()`를 돌려주면 다음 매니저로 넘어간다. provider 모델이 reactive 합성으로 자연스럽게 표현된 모습이다.

> **왜 provider가 사라졌을까?**
> Reactor의 합성 연산자(`Mono.switchIfEmpty`, `flatMap`)가 provider 패턴이 하던 일을 더 작은 추상으로 표현할 수 있기 때문이다. provider라는 별도의 인터페이스를 두지 않아도 매니저 자체로 위임을 표현할 수 있다. 작아진 추상이 더 깊은 자유를 준다.

### 11.2.3 `ServerSecurityContextRepository`

서블릿에서 세션에 `SecurityContext`를 저장하던 자리는 `HttpSessionSecurityContextRepository`였다. WebFlux의 대응자는 `WebSessionServerSecurityContextRepository`다. 이름이 길지만 하는 일은 같다 — `SecurityContext`를 어디에 둘 것인가.

```java
public interface ServerSecurityContextRepository {
    Mono<Void> save(ServerWebExchange exchange, SecurityContext context);
    Mono<SecurityContext> load(ServerWebExchange exchange);
}
```

기본은 `WebSession`(서블릿 세션의 reactive 버전)에 저장하는 구현이다. 자원 서버처럼 stateless로 운영하고 싶다면 `NoOpServerSecurityContextRepository.getInstance()`를 끼우면 된다. JWT 자원 서버 설정에서 별 신경 안 써도 stateless로 동작하는 이유가 이 빈이 자동으로 No-Op으로 채워지기 때문이다.

다시 흐름을 그려보자. 한 요청이 들어오면 `AuthenticationWebFilter`가 매처에 걸려 변환기로 `Authentication`을 만들고, 매니저로 인증을 마치고, 결과를 저장소에 저장한다. 이 모든 단계가 `Mono` 체인으로 이어진다. 한 단계도 블로킹을 허용하지 않는다.

## 11.3 블로킹 API 금지 — `SecurityContextHolder`는 손대지 말자

서블릿에서 그 어느 곳에서나 `SecurityContextHolder.getContext().getAuthentication()`을 호출해 현재 사용자를 꺼냈다. 어디서든 한 줄로 끝났다. 이 한 줄이 WebFlux로 옮기는 사람들의 첫 번째 함정이다.

```java
// 이렇게 쓰면 안 된다 — WebFlux에서는 거의 항상 null
@GetMapping("/me")
public Mono<String> me() {
    Authentication auth = SecurityContextHolder.getContext().getAuthentication();
    return Mono.just(auth.getName());  // NullPointerException
}
```

왜 `null`일까? `SecurityContextHolder`의 기본 전략은 `ThreadLocal`이다. 서블릿 컨테이너는 한 요청이 한 스레드를 점유하므로 `ThreadLocal`이 곧 "현재 요청의 컨텍스트"였다. WebFlux는 다르다. 한 요청이 여러 스레드 사이를 옮겨 다닌다. event loop 스레드에서 시작해 `subscribeOn(...)`이 끼이는 순간 다른 스레드로 점프한다. `ThreadLocal`은 그 점프 사이에서 사라진다.

그래서 reactive 코드에서는 `ThreadLocal` 대신 **Reactor Context**라는 다른 그릇을 쓴다. Reactor가 각 신호(`onNext`, `onError`)와 함께 전달하는 불변 키-값 저장소다. Spring Security는 이 Context의 특정 키에 `SecurityContext`를 담아 둔다. 그걸 꺼내는 API가 `ReactiveSecurityContextHolder`다.

```java
// 권장 — Reactor Context에서 꺼낸다
@GetMapping("/me")
public Mono<String> me() {
    return ReactiveSecurityContextHolder.getContext()
        .map(SecurityContext::getAuthentication)
        .map(Authentication::getName);
}
```

`getContext()`의 반환 타입은 `Mono<SecurityContext>`다. 인증된 사용자가 없으면 `Mono.empty()`다. 즉 이 코드는 "Reactor Context에서 SecurityContext를 꺼내고, 거기서 Authentication을 꺼내고, 그 name을 돌려준다. 컨텍스트가 비어 있으면 빈 응답"으로 읽힌다. 한 단계도 블로킹이 아니다.

물론 컨트롤러 인자로 그냥 받아도 된다. Spring Security가 `Authentication`/`Principal`을 컨트롤러 파라미터로 자동 주입해주기 때문이다.

```java
@GetMapping("/me")
public Mono<String> me(Authentication auth) {
    return Mono.just(auth.getName());
}
```

`@AuthenticationPrincipal`을 쓰는 패턴도 그대로 작동한다. 이 두 방식이 컨트롤러 입장에서는 가장 깔끔하다.

> **잊지 말자.** `SecurityContextHolder.getContext()`는 WebFlux에서 **null이거나 잘못된 사용자의 컨텍스트**를 돌려줄 수 있다. 후자가 더 무섭다. 만약 application 어디선가 `SecurityContextHolder.MODE_INHERITABLETHREADLOCAL`을 설정하고 있다면, event loop 스레드의 ThreadLocal에 직전 요청의 컨텍스트가 남아 다음 요청에 그대로 새어 나갈 수 있다. **다른 사용자의 권한이 다른 사용자에게 적용되는 사고**가 여기서 난다. 한 번 일어나면 디버깅하기 끔찍한 일이다.

### 11.3.1 차단 함정 모음

WebFlux로 옮기다 블로킹을 무심코 부르는 자리는 의외로 많다. 자주 마주치는 셋을 미리 알아두자.

**(1) JPA Repository를 reactive 매니저 안에서 부른다.** `UserDetailsRepositoryReactiveAuthenticationManager`가 받는 `ReactiveUserDetailsService` 구현체에서 `userRepository.findByUsername(...)`(JPA)을 그대로 호출하면 컴파일은 되지만 event loop이 멈춘다. `Mono.fromCallable(() -> userRepository.findByUsername(name)).subscribeOn(Schedulers.boundedElastic())`처럼 별도 스케줄러로 보내는 것이 차선이다. 제일 좋은 건 R2DBC 같은 reactive 드라이버를 쓰는 것이다.

**(2) `JwtDecoder`(서블릿용)를 `ReactiveJwtDecoder` 자리에 등록한다.** 둘은 다른 인터페이스다. 자원 서버 설정에서 IDE의 자동 임포트가 서블릿용을 가져오면 시동은 되어도 JWT 검증에서 매번 블로킹 HTTP 호출(JWKs 조회)이 일어난다. 시그니처가 다르니 잘 보고 임포트하자.

**(3) `@PreAuthorize`의 SpEL 안에서 동기 서비스를 부른다.** `@PreAuthorize("@authz.canRead(#id)")` 같은 패턴에서 `authz.canRead(...)`가 JPA를 호출한다면, reactive method security 안에서도 블로킹이 일어난다. SpEL은 reactive 식을 평가하지만 그 안에서 부른 메서드까지 reactive로 만들지는 못한다. 이 경우 `Mono<Boolean>`을 돌려주는 메서드로 바꾸자. `@PreAuthorize`는 reactive 반환을 이해한다.

스레드 하나가 멈추는 순간 WebFlux의 전제가 무너진다. 이 문장을 책상 옆 메모에 붙여두자.

## 11.4 WebFlux 자원 서버 — `ReactiveJwtDecoders.fromIssuerLocation`

JWT 자원 서버는 reactive에서도 가장 자주 만들어지는 구성이다. 5장에서 본 서블릿 자원 서버와 시그니처 한 줄만 다르다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
```

이 한 줄이 자동으로 하는 일은 서블릿과 같다. `${issuer-uri}/.well-known/openid-configuration`에 OIDC discovery를 쳐서 JWKs URL을 알아내고, 그걸 캐시한 뒤 `ReactiveJwtDecoder`를 만들어 빈으로 등록한다. 다만 빈 타입이 `JwtDecoder`가 아니라 `ReactiveJwtDecoder`라는 점만 다르다.

수동으로 만들고 싶다면 이렇게 된다.

```java
@Bean
ReactiveJwtDecoder jwtDecoder() {
    return ReactiveJwtDecoders.fromIssuerLocation(
        "https://auth.example.com/realms/app");
}
```

서블릿용은 `JwtDecoders.fromIssuerLocation`, reactive용은 `ReactiveJwtDecoders.fromIssuerLocation`이다. 단어 하나 차이지만 두 메서드가 돌려주는 객체는 전혀 다르다. 앞쪽은 동기 HTTP 클라이언트(RestTemplate)로 JWKs를 조회하고, 뒤쪽은 `WebClient`로 조회한다. event loop 위에서 도는 자원 서버가 첫 요청마다 RestTemplate으로 JWKs를 받느라 멈춰서는 안 되기 때문이다.

### 11.4.1 권한 변환기

토큰의 `scope`/`scp` 클레임을 `SCOPE_*` 권한으로 자동 매핑하는 동작은 reactive도 동일하다. 커스텀 클레임(`roles`, `groups`)을 권한으로 매핑하려면 `JwtAuthenticationConverter`의 reactive 대응자가 필요한데, 이름이 `ReactiveJwtAuthenticationConverterAdapter`로 길어진다.

```java
@Bean
Converter<Jwt, Mono<AbstractAuthenticationToken>> jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
    grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
    grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");

    JwtAuthenticationConverter delegate = new JwtAuthenticationConverter();
    delegate.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);

    return new ReactiveJwtAuthenticationConverterAdapter(delegate);
}
```

```java
http.oauth2ResourceServer(o -> o.jwt(j -> j
    .jwtAuthenticationConverter(jwtAuthenticationConverter())));
```

서블릿 코드에서 `JwtAuthenticationConverter`를 바로 넘기던 자리에, reactive에서는 `Converter<Jwt, Mono<AbstractAuthenticationToken>>`을 넘긴다. 변환 자체가 비동기일 수 있다는 약속이다. 권한을 별도 DB에서 끌어와야 하는 시나리오라면 이 시그니처가 자연스럽다.

### 11.4.2 Introspection

Opaque 토큰을 쓸 때도 마찬가지다. `OpaqueTokenIntrospector` 대신 `ReactiveOpaqueTokenIntrospector`를 빈으로 등록한다. 매 요청 IdP에 introspection을 쳐야 하므로 캐시(예: Caffeine)는 reactive에서도 필수다.

## 11.5 인가 — `authorizeExchange`

서블릿의 `authorizeHttpRequests`에 해당하는 자리가 `authorizeExchange`다. 매처 이름도 `requestMatchers` → `pathMatchers`로 바뀐다. 그 외는 거의 동일하다.

```java
http.authorizeExchange(ex -> ex
    .pathMatchers("/actuator/health").permitAll()
    .pathMatchers(HttpMethod.GET, "/api/posts/**").permitAll()
    .pathMatchers("/api/admin/**").hasRole("ADMIN")
    .pathMatchers("/api/users/**").hasAnyAuthority("SCOPE_users.read", "SCOPE_users.write")
    .anyExchange().authenticated());
```

서블릿 코드와 거의 같은 모양이다. 그래서 옮기는 일이 가볍게 느껴진다. 그러나 한 가지 다르다 — `RequestMatcher`가 아니라 `ServerWebExchangeMatcher`다. 커스텀 매처를 끼우는 자리에서 시그니처가 살짝 비틀린다.

```java
// 서블릿
RequestMatcher matcher = request -> request.getHeader("X-Tenant") != null;

// WebFlux
ServerWebExchangeMatcher matcher = exchange ->
    Mono.justOrEmpty(exchange.getRequest().getHeaders().getFirst("X-Tenant"))
        .flatMap(t -> MatchResult.match())
        .switchIfEmpty(MatchResult.notMatch());
```

`MatchResult`가 `Mono`로 감싸진 채 흘러간다. reactive의 약속이 매처 한 줄에도 스며들어 있다.

### 11.5.1 `access(...)`로 커스텀 매니저 꽂기

`hasRole`/`hasAuthority`보다 복잡한 인가 결정은 `access(...)`에 `ReactiveAuthorizationManager`를 직접 끼워서 표현한다. 서블릿의 `AuthorizationManager`와 거의 동일하지만 반환이 `Mono<AuthorizationDecision>`이다.

```java
ReactiveAuthorizationManager<AuthorizationContext> tenantMatch = (authMono, ctx) ->
    authMono.map(auth -> {
        String userTenant = (String) ((Jwt) auth.getPrincipal()).getClaims().get("tenant");
        String reqTenant = ctx.getExchange().getRequest().getHeaders().getFirst("X-Tenant");
        return new AuthorizationDecision(Objects.equals(userTenant, reqTenant));
    });

http.authorizeExchange(ex -> ex
    .pathMatchers("/api/tenant/**").access(tenantMatch)
    .anyExchange().authenticated());
```

`authMono`로 받는 부분이 핵심이다. **`Authentication`을 동기로 받지 않는다.** 인가 매니저가 호출되는 시점에 아직 인증이 끝나지 않았을 수 있고, 인증이 reactive 합성에서 늦게 도착할 수 있기 때문이다. Reactive로 받는 게 정직한 약속이다.

## 11.6 Reactive Method Security

URL 인가만으로는 좁다. 도메인 로직 안에서 인가를 표현하고 싶을 때 `@PreAuthorize`를 쓰는 자리, WebFlux에서는 `@EnableReactiveMethodSecurity`가 그 자리를 받는다.

```java
@Configuration
@EnableWebFluxSecurity
@EnableReactiveMethodSecurity
public class SecurityConfig {
    // ...
}
```

서블릿의 `@EnableMethodSecurity`와 어노테이션 이름만 다르다. 서비스 코드의 `@PreAuthorize`/`@PostAuthorize`는 그대로 동작한다 — 단, **반환 타입이 `Mono`/`Flux`인 메서드만**.

```java
public interface PostService {

    @PreAuthorize("hasAuthority('SCOPE_posts.read')")
    Mono<Post> findById(String id);

    @PostAuthorize("returnObject.author == authentication.name")
    Mono<Post> findByIdEnforceOwner(String id);

    @PreAuthorize("@authz.canEdit(#id, authentication)")
    Mono<Void> update(String id, PostUpdate cmd);
}
```

세 가지 짚어야 한다.

**첫째, SpEL 안의 `authentication`/`principal`은 `Mono`로 흘러간다.** 위 예제의 두 번째 `@PostAuthorize`에서 `authentication.name`은 표면적으로는 동기 접근처럼 보이지만, Spring Security가 식을 평가하기 전에 `Mono<Authentication>`을 unwrap한 뒤 평가한다. 사용자가 SpEL을 동기처럼 쓰게 해주려는 배려다.

**둘째, 외부 빈을 부르는 `@authz.canEdit(...)` 같은 패턴은 반환 타입에 주의해야 한다.** `canEdit`이 `boolean`(동기)을 돌려준다면 그 안에서 절대 블로킹 호출을 하면 안 된다. DB 조회가 필요하면 시그니처를 `Mono<Boolean>`으로 바꾸자. reactive method security는 SpEL이 `Mono<Boolean>`을 돌려주면 그 결과를 기다린다.

**셋째, 반환 타입이 `Mono`/`Flux`가 아닌 메서드에 `@PreAuthorize`를 붙이면 무력하다.** 정확히는 reactive 모드에서는 동작이 일관되지 않을 수 있다. 서비스 메서드 시그니처가 reactive로 통일되어 있어야 인가 어노테이션이 일관되게 적용된다. 한 클래스 안에 `String findName()`(동기)과 `Mono<Post> findById(...)`(reactive)가 섞여 있으면 끔찍한 일이 된다. 한 가지로 통일하자.

> **권장:** WebFlux 프로젝트의 서비스 레이어는 가능한 한 모든 public 메서드가 `Mono`/`Flux`를 돌려주도록 통일하는 것이 좋다. method security가 일관되게 동작할 뿐 아니라, 컨트롤러까지의 흐름에서 블로킹이 끼어들 자리가 사라진다.

## 11.7 7.0 신규 — `AllAuthoritiesReactiveAuthorizationManager`

서블릿 8장에서 살펴본 `AllAuthoritiesAuthorizationManager`(AND 의미)의 reactive 짝이 7.0에서 추가됐다. 이름이 길지만 하는 일은 단순하다. **모든 권한을 동시에 갖고 있어야 통과**시키는 매니저다.

서블릿의 `hasAnyAuthority(...)`는 OR다. 하나만 있어도 통과다. 그런데 MFA처럼 "패스워드도 통과해야 하고 OTT도 통과해야 한다"는 상황은 AND가 필요하다. 6.x까지는 이걸 표현하려면 SpEL에서 `hasAuthority('A') and hasAuthority('B')`를 직접 써야 했다. 7.0의 `AllAuthorities...` 매니저가 이 패턴을 정식 매니저로 들어 올렸다.

```java
ReactiveAuthorizationManager<AuthorizationContext> mfa =
    AllAuthoritiesReactiveAuthorizationManager.hasAllAuthorities(
        "FACTOR_PASSWORD", "FACTOR_OTT");

http.authorizeExchange(ex -> ex
    .pathMatchers("/api/funds/transfer").access(mfa)
    .anyExchange().authenticated());
```

이 매니저가 의미 있는 자리는 7장에서 본 `@EnableMultiFactorAuthentication`이 만들어내는 권한 모델이다. 패스워드 인증 성공 시 `FACTOR_PASSWORD`, OTT 인증 성공 시 `FACTOR_OTT`가 누적된다. 송금처럼 두 factor 모두 요구하는 엔드포인트에서 이 매니저가 짧고 명료한 표현을 준다.

`hasAnyAuthority` 대신 `hasAllAuthorities`라는 표현이 WebFlux의 매처 DSL 안에서 깔끔하게 자리 잡지 못하는 점은 작은 아쉬움이다. 그래서 `access(...)`에 매니저를 직접 끼우는 패턴이 권장된다. 7장 MFA를 reactive로 옮길 일이 있다면 이 매니저를 잊지 말자.

## 11.8 컨텍스트 전파 — Reactor Context와 `contextWrite`

reactive에서 `SecurityContext`가 어떻게 흘러가는지를 한 번 분명히 짚자. 서블릿에서는 `ThreadLocal`이 그릇이었다. WebFlux에서는 **Reactor Context**가 그릇이다.

Reactor Context는 신호(`onNext`, `onError`)와 함께 위에서 아래로 흐르는 불변 키-값 저장소다. 그러나 흐름의 방향이 자주 헷갈린다. **신호는 downstream(아래)으로 흐르지만, Context는 마지막 `subscribe` 시점에서 거꾸로 upstream(위)로 전파된다.** 즉 어디선가 `subscribe`할 때 Context에 값을 넣어야 그 아래(체인 위쪽)의 연산자들이 그 값을 본다.

Spring Security는 이 메커니즘을 활용해 인증된 `SecurityContext`를 Reactor Context의 특정 키에 담아 둔다. 그 키를 꺼내는 표준 API가 `ReactiveSecurityContextHolder`다. 즉 `ReactiveSecurityContextHolder.getContext()`는 Reactor Context에서 키 하나를 꺼내는 한 줄에 불과하다. 마법이 아니다.

### 11.8.1 테스트나 비동기 호출에서 컨텍스트 주입하기

운영 코드에서는 `AuthenticationWebFilter`가 알아서 Context에 `SecurityContext`를 심어준다. 그러나 테스트나 단위 메서드 호출에서는 직접 주입해야 한다.

```java
SecurityContext ctx = new SecurityContextImpl(
    new TestingAuthenticationToken("alice", null, "ROLE_USER"));

Mono<String> mono = service.currentUserName()
    .contextWrite(ReactiveSecurityContextHolder.withSecurityContext(Mono.just(ctx)));

StepVerifier.create(mono).expectNext("alice").verifyComplete();
```

`contextWrite(...)`는 Reactor의 표준 연산자다. 그 안에 `ReactiveSecurityContextHolder.withSecurityContext(...)`가 만든 Context 수정자를 넣어 주면 된다. 12장에서 `WebTestClient.mutateWith(mockUser(...))`가 결국 하는 일도 같은 메커니즘이다.

### 11.8.2 `SecurityContextServerWebExchange`로 보강

가끔 `WebFilter`의 downstream에 `ServerWebExchange`를 통해 `SecurityContext`를 넘기고 싶을 때가 있다. 이때 쓰는 패턴이 `SecurityContextServerWebExchange`다. 평소 직접 마주칠 일은 적지만, 커스텀 `WebFilter`를 짤 때 한 번쯤 마주친다는 것만 알아두면 된다.

```java
SecurityContext ctx = ...;
ServerWebExchange decorated = new SecurityContextServerWebExchange(exchange, Mono.just(ctx));
return chain.filter(decorated);
```

핵심은 변하지 않는다. Context는 위에서 아래로, 또 거꾸로 흐르는 그릇이고, Spring Security는 그 그릇의 특정 자리에 `SecurityContext`를 둔다는 점이다.

## 11.9 서블릿에서 옮길 때 가장 자주 막히는 다섯

이 챕터의 마지막 절은 실전 체크리스트다. 서블릿 보안 코드를 WebFlux로 옮기다 마주치는 흔한 함정을 다섯 가지로 모았다. 어느 하나라도 익숙하다면, 그 자리에서 잠시 멈추고 본 챕터의 해당 절을 다시 펴 보자.

### 함정 1. 블로킹 호출을 reactive 매니저에 끼웠다

가장 자주 일어난다. `ReactiveUserDetailsService` 구현체 안에서 JPA `userRepository.findByUsername(...)`을 부르거나, `ReactiveAuthenticationManager` 안에서 동기 HTTP 클라이언트로 외부 API를 친다. 컴파일은 통과한다. 런타임에 `BlockHound`(개발 환경에서 블로킹을 탐지하는 라이브러리)가 잡아주지 않는 한 조용히 event loop을 멈춘다.

**증상.** 트래픽이 늘면 응답 시간이 비선형으로 폭증한다. 스레드 덤프를 떠 보면 reactor-http-nio-* 스레드들이 JDBC 호출에서 박혀 있다.

**해법.** R2DBC 같은 reactive 드라이버로 옮기는 게 가장 깔끔하다. 옮길 수 없는 자원이라면 `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())`으로 별도 풀로 보내자. 그러나 이건 차선이다.

### 함정 2. suspending 함수와 `Mono`를 섞었다

Kotlin 프로젝트에서 자주 만난다. Spring Security 자체는 `Mono`/`Flux` 시그니처지만, 컨트롤러를 `suspend fun`으로 쓰는 팀이 있다. 두 세계는 spring-web의 어댑터로 잘 이어지지만, 보안의 SpEL이 `Mono<Boolean>`을 기대하는 자리에 `suspend fun`을 그대로 넘기면 어색해진다.

**해법.** `@PreAuthorize` 안에서 부르는 빈 메서드는 `Mono<Boolean>`을 돌려주는 자바 메서드로 두는 편이 낫다. Kotlin이라면 `mono { ... }` 빌더로 감싸자. 어댑터를 한 번만 거치면 그 다음은 평화롭다.

### 함정 3. Reactor Context가 끊겼다

`Schedulers.parallel()`이나 외부 라이브러리의 자체 스케줄러로 작업을 넘기는 순간, Reactor Context가 그쪽으로 따라가지 못하는 경우가 있다. 정확히는 Reactor의 표준 연산자는 Context를 잘 전파하지만, 일부 외부 라이브러리는 `Mono.subscribe()`만 호출하고 Context 인자를 빠뜨린다.

**증상.** 분명히 인증된 요청인데 `ReactiveSecurityContextHolder.getContext()`가 `Mono.empty()`를 돌려준다.

**해법.** Reactor 표준 연산자(`flatMap`, `subscribeOn`, `publishOn`)만 쓰는 한 Context는 끊기지 않는다. 외부 라이브러리를 거친다면 그 직후에 `contextWrite(...)`로 컨텍스트를 다시 심어줘야 한다.

### 함정 4. 에러 핸들러 시그니처가 다르다

서블릿의 `AuthenticationEntryPoint`/`AccessDeniedHandler`를 그대로 등록하면 어색하다. WebFlux는 대응 타입이 `ServerAuthenticationEntryPoint`/`ServerAccessDeniedHandler`다. 이름이 짧아 보이지만 한 글자 빼먹으면 IDE는 빨갛게 운다.

```java
http.exceptionHandling(e -> e
    .authenticationEntryPoint((exchange, ex) -> {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        return exchange.getResponse().writeWith(Mono.just(
            exchange.getResponse().bufferFactory().wrap(
                "{\"error\":\"unauthenticated\"}".getBytes())));
    }));
```

ProblemDetail(8장에서 본 그 모델)을 reactive에서 그대로 쓰고 싶다면 `ProblemDetail` 객체를 JSON으로 직렬화해 `writeWith`에 넘기면 된다. 자세한 패턴은 8장의 거부 표현 절을 참조하자.

### 함정 5. 테스트 패턴이 다르다

서블릿 책에서 익숙해진 `@WithMockUser` + `MockMvc` 조합이 reactive에서는 `WebTestClient` + `mutateWith(SecurityMockServerConfigurers.mockUser(...))`로 바뀐다. 어노테이션도 일부는 그대로 쓰이지만, `SecurityMockMvcRequestPostProcessors`의 `csrf()`/`user()`/`jwt()` 자리는 `SecurityMockServerConfigurers`의 대응자로 갈아탄다.

```java
webTestClient
    .mutateWith(SecurityMockServerConfigurers.mockUser("alice").roles("ADMIN"))
    .mutateWith(SecurityMockServerConfigurers.csrf())
    .post().uri("/api/admin/users")
    .exchange().expectStatus().isOk();
```

JWT 자원 서버 mock도 마찬가지로 `SecurityMockServerConfigurers.mockJwt()` 자리가 있다. 자세한 reactive 테스트 패턴은 12장에서 본격적으로 다룬다.

## 11.10 한 그림으로 요약

WebFlux 보안의 한 요청을 한 그림으로 정리하자.

```text
   ServerWebExchange
        │
        │ ① CORS, CSRF, Header 필터들
        ▼
   AuthenticationWebFilter
        │ ② ServerAuthenticationConverter: exchange → Mono<Authentication>
        │ ③ ReactiveAuthenticationManager: Mono<Authentication> → Mono<Authentication>(인증완료)
        │ ④ ServerSecurityContextRepository: Mono<Void> save
        ▼
   (Reactor Context에 SecurityContext 주입)
        │
        ▼
   AuthorizationWebFilter
        │ ⑤ ReactiveAuthorizationManager: AuthorizationContext → Mono<AuthorizationDecision>
        ▼
   컨트롤러 / 서비스 (@PreAuthorize는 reactive method security가 평가)
        │
        ▼
   응답
```

한 단계 한 단계가 `Mono`로 묶여 있다. 어느 한 점에서 블로킹이 끼면 event loop이 멈춘다. 멈추면 WebFlux의 전제가 무너지고, 그 순간 reactive를 쓰는 이유가 사라진다. 외워두자.

## 11.11 핵심 요약

- 서블릿의 보안 추상은 거의 그대로 reactive 짝이 있다. 이름이 비슷한 건 친절함이고, 시그니처가 비틀린 건 약속을 지키기 위한 정직함이다.
- 진입의 삼각형은 `AuthenticationWebFilter` + `ReactiveAuthenticationManager` + `ServerSecurityContextRepository`다. provider 추상은 사라지고 매니저 합성이 그 자리를 대신한다.
- `SecurityContextHolder.getContext()`는 WebFlux에서 위험하다. `ReactiveSecurityContextHolder.getContext()` 또는 컨트롤러 파라미터 주입을 쓰자.
- 자원 서버는 `ReactiveJwtDecoders.fromIssuerLocation`과 `ReactiveJwtAuthenticationConverterAdapter`로 짠다. 인가는 `authorizeExchange`, method security는 `@EnableReactiveMethodSecurity`다.
- 컨텍스트의 그릇은 ThreadLocal이 아니라 Reactor Context다. 테스트와 비동기 호출에서는 `contextWrite(...)`로 직접 심어주자.

## 11.12 다음 챕터에서 답할 것

11장까지 인증·인가·횡단·reactive까지 모든 본문 어휘가 깔렸다. 이제 남은 질문은 단 하나다. **이 모든 결정을 어떻게 회귀 가능한 안전망으로 묶을 것인가.** 12장은 `@WithMockUser`/`SecurityMockMvcRequestPostProcessors`/`oauth2Login()`/`jwt()` mock부터 시작해, 본 챕터의 `WebTestClient` + `mutateWith(mockUser(...))` 패턴을 다시 마주한다. 이 책에서 내린 모든 보안 결정이 다음 챕터에서 한 번씩 시험대에 오른다.
