# 3장. 인증과 인가의 컴포넌트 모델

> 선행 필요: 2장 (필터 체인의 큰 그림)

이 챕터는 어휘를 박는 챕터다. 너무 익숙해 보이는 이름들이지만, 이름과 책임을 정확히 짝지을 수 있을 때 비로소 7.0의 새 모델이 보인다. `AuthenticationManager`라는 이름은 익숙하다. `SecurityContextHolder`도 한두 번은 써봤을 것이다. 그러나 누군가 "그 둘 사이에 `ProviderManager`가 왜 끼어 있느냐"고 물으면 잠시 멈칫하게 된다. "`AuthorizationManager`에서 `check`는 왜 사라졌느냐"고 물으면 더 막막해진다. 자, 이런 상황을 가정해보자. 5.x 시절에 잘 돌던 코드를 7.0으로 올렸더니 인가 로직이 컴파일조차 안 되고, 비동기로 보낸 작업에서 갑자기 다른 사용자의 권한이 튀어나온다. 이때 도움이 되는 건 화려한 새 API의 사용법이 아니라, 이 한 줄의 메서드 호출이 안에서 어떤 객체에게 책임을 넘기는지에 대한 명확한 어휘다.

2장에서 우리는 한 요청이 어떤 필터 11개를 거쳐 어떻게 컨트롤러에 도달하는지를 따라가 봤다. 그 흐름에서 인증과 인가는 사실 두 개의 특정 지점에서 결정된다. 하나는 인증 필터(`UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter` 등)에서 신원이 만들어지는 순간, 다른 하나는 `AuthorizationFilter`에서 "이 신원이 이 자원에 손댈 수 있는가"를 묻는 순간이다. 그런데 그 두 지점 모두 필터 자신이 직접 일을 처리하지는 않는다. 필터는 결정을 다른 컴포넌트에게 위임한다. 그 위임의 사슬을 정확히 풀어 보는 것이 이번 챕터의 일이다. 어휘를 박는다는 것은 단지 명칭을 외운다는 뜻이 아니다. 어떤 객체가 어떤 책임을 지고, 어떤 객체가 어떤 책임에 손대지 않아야 하는지를 머릿속에 박는다는 뜻이다.

이 챕터의 핵심 질문은 단순하다. **`AuthenticationManager`, `AuthorizationManager`, `SecurityContextHolder`는 각각 무엇을 책임지고, 7.0에서 어떻게 바뀌었는가?** 이 셋의 책임 분담을 또렷이 그릴 수 있게 되면, 이후 모든 챕터의 코드와 설정이 같은 어휘 안에서 말하기 시작한다.

## 인증의 주어 — `Authentication`이라는 객체

먼저 가장 작은 단위부터 살펴보자. Spring Security의 모든 인증 흐름은 `Authentication`이라는 인터페이스 하나로 수렴한다. 이 객체는 두 가지 얼굴을 가진다. 인증 전에는 "내가 이 자격 증명으로 로그인하려 한다"는 요청이고, 인증 후에는 "나는 이런 신원을 가진 사용자이며 이런 권한을 들고 있다"는 결과다. 같은 인터페이스가 입력으로도 쓰이고 출력으로도 쓰이는, 다소 독특한 구조다.

```java
public interface Authentication extends Principal, Serializable {
    Collection<? extends GrantedAuthority> getAuthorities();
    Object getCredentials();
    Object getDetails();
    Object getPrincipal();
    boolean isAuthenticated();
    void setAuthenticated(boolean isAuthenticated) throws IllegalArgumentException;
}
```

폼 로그인을 예로 들면 입력 단계에서 `UsernamePasswordAuthenticationToken`이 만들어진다. 이 시점의 `principal`은 사용자가 입력한 username 문자열이고, `credentials`는 평문 비밀번호다. 인증을 통과하면 같은 클래스의 새 인스턴스가 만들어지는데, 이번에는 `principal`이 `UserDetails`로 채워지고 `credentials`는 보안상 비워지며 `authorities`가 들어찬다. 같은 클래스가 두 가지 상태로 쓰인다는 점이 처음에는 어색하다. 하지만 인증 전/후의 정보 흐름이 결국 같은 구조를 공유한다는 설계 의도를 받아들이면, "이 토큰은 지금 어느 단계인가"를 `isAuthenticated()` 한 줄로 가늠할 수 있다는 점이 꽤 우아하게 다가온다.

이 객체의 `principal`은 사실상 자유 양식이다. 폼 로그인에서는 `UserDetails`, OAuth2 Login에서는 `OAuth2User` 또는 `OidcUser`, JWT 자원 서버에서는 `Jwt` 객체 자체일 수 있다. 그래서 `@AuthenticationPrincipal`로 컨트롤러 파라미터에 꽂을 때 무엇이 들어올지는 인증 시나리오마다 다르다. 4장과 5장에서 이 차이를 다시 만날 것이다. 지금은 일단 "이 객체 하나가 인증의 시작이자 끝"이라는 것만 기억해두자.

### `GrantedAuthority` — 권한의 표현 모델

`Authentication`의 `authorities` 컬렉션은 그 사용자가 무엇을 할 수 있는지를 알려주는 라벨의 집합이다. 인터페이스 자체는 단 한 줄짜리다.

```java
public interface GrantedAuthority extends Serializable {
    String getAuthority();
}
```

기본 구현체는 `SimpleGrantedAuthority`. 그저 문자열 하나를 들고 다닌다. 이 단순함이 Spring Security 권한 모델의 미덕이자 가끔 함정이다. 모든 권한은 결국 문자열이다. `ROLE_ADMIN`도 `SCOPE_orders.read`도 `factor:password`도 그저 문자열이다. 문자열 비교로 통과가 결정된다. 이 모델이 단순하기 때문에 인증 시나리오가 무엇이든 — 폼 로그인이든 JWT든 Passkeys든 — 똑같은 인가 로직을 통과할 수 있다.

`ROLE_` 접두사 컨벤션도 같은 문맥에서 이해해야 한다. `hasRole("ADMIN")`은 내부적으로 `ROLE_ADMIN` 문자열을 가진 authority를 찾는다. `hasAuthority("ADMIN")`은 정확히 `ADMIN` 문자열을 찾는다. 이 둘이 같지 않다는 사실은 5.x 시절부터 수많은 개발자를 당황시킨 작은 함정이다. JWT의 scope 권한은 `SCOPE_` 접두사로 자동 매핑되고, MFA의 factor는 7.0에서 자체 접두사 컨벤션을 따른다. 접두사를 바꾸고 싶다면 `GrantedAuthorityDefaults` 빈으로 전역 기본값을 갈아끼울 수 있다. 흔히 쓰진 않지만 알아두면 좋다.

```java
@Bean
static GrantedAuthorityDefaults grantedAuthorityDefaults() {
    return new GrantedAuthorityDefaults("ROLE_");
}
```

8장에서 권한 모델을 본격적으로 풀 때 이 단순한 문자열 모델이 어떻게 URL 기반 인가, 메서드 기반 인가, Role Hierarchy로 확장되는지를 함께 살펴보자. 지금은 권한이 그저 문자열이라는 사실, 그리고 그 사실이 인가 모델의 일관성을 떠받친다는 사실만 머릿속에 박아 두면 충분하다.

## `AuthenticationManager` — 인증의 입구

인증 필터가 토큰 객체를 만들었다고 해서 그 자신이 직접 사용자를 검증하지는 않는다. 필터는 토큰을 들고 `AuthenticationManager`에게 묻는다. "이 자격 증명이 진짜인가?" 그러면 `AuthenticationManager`는 "진짜라면 인증된 `Authentication`을 돌려주고, 가짜라면 `AuthenticationException`을 던진다"는 단순한 계약을 따른다.

```java
public interface AuthenticationManager {
    Authentication authenticate(Authentication authentication)
        throws AuthenticationException;
}
```

이 인터페이스가 다 한 줄이라는 점이 흥미롭다. Spring Security 안에서 가장 중요한 결정을 내리는 컴포넌트가 가장 짧은 인터페이스로 정의되어 있다. 인터페이스가 짧다는 건 구현이 자유롭다는 뜻이다. 우리가 만든 `AuthenticationManager` 빈을 등록해도 되고, 시나리오마다 다른 매니저를 골라줄 수도 있다.

### `ProviderManager`는 단순한 if문이 아니다

거의 모든 실전 코드에서 `AuthenticationManager`의 실제 인스턴스는 `ProviderManager`다. 이 객체는 여러 `AuthenticationProvider`를 리스트로 들고 있다가, 토큰이 들어오면 처음부터 끝까지 한 명씩 묻는다. "당신이 이걸 처리할 수 있느냐?" 처음으로 "예"라고 답한 provider에게 검증을 맡긴다.

```
[Auth Filter]
   └─ AuthenticationManager (= ProviderManager)
           ├─ DaoAuthenticationProvider          (UsernamePasswordToken 처리)
           ├─ JwtAuthenticationProvider          (BearerTokenAuthentication 처리)
           ├─ OAuth2LoginAuthenticationProvider  (OAuth2LoginToken 처리)
           └─ ... 등록된 모든 Provider 순회
```

처음 보면 "그냥 if-else 사다리 아닌가" 싶을 수 있다. 그런데 이 구조의 진짜 이름은 책임 연쇄 패턴(Chain of Responsibility)이다. 단순한 분기 처리가 아니라 명시적인 설계 의도를 가진 패턴이다. 무엇이 달라지는지 살펴보자.

첫째, **provider의 추가·제거가 다른 provider를 건드리지 않는다.** 새로운 인증 방식을 도입하고 싶다면 새 provider 하나를 빈으로 등록하면 끝이다. 기존 분기 로직을 한 줄도 수정할 필요가 없다. 둘째, **provider 순서를 통해 우선순위를 표현할 수 있다.** 같은 토큰을 처리할 수 있는 provider가 둘이라면 먼저 등록된 쪽이 이긴다. 셋째, **하나의 provider가 실패해도 다음 provider로 자연스럽게 넘어갈 수 있다** — 단, 이 부분은 약간의 주의가 필요하다.

각 provider는 자신이 처리할 수 있는지를 `supports(Class<?> token)` 메서드로 답한다. `DaoAuthenticationProvider`는 `UsernamePasswordAuthenticationToken.class.isAssignableFrom(token)`을 검사하고, `JwtAuthenticationProvider`는 `BearerTokenAuthenticationToken.class`를 검사한다. 토큰 클래스로 일치 여부를 판단하는 것이지, 토큰 안의 내용으로 판단하는 게 아니다. 이 점은 처음 직접 provider를 만들 때 흔히 놓치는 부분이다. "내 provider가 분명 등록됐는데 호출이 안 된다"는 의문의 답은 십중팔구 `supports()`에서 false를 돌리고 있기 때문이다.

```java
public class CustomTokenProvider implements AuthenticationProvider {
    @Override
    public boolean supports(Class<?> authentication) {
        return CustomToken.class.isAssignableFrom(authentication);
    }
    @Override
    public Authentication authenticate(Authentication auth) {
        // 실제 검증 로직
    }
}
```

그리고 `authenticate()` 안에서 던지는 예외에도 두 가지 종류가 있다는 것을 잊지 말자. **`AuthenticationException`을 던지면 `ProviderManager`는 다음 provider로 넘어가지 않는다 — 인증 실패로 그대로 종결된다.** 다음 provider에게 기회를 주고 싶다면 그 provider에서 예외를 던지지 말고 `null`을 돌려야 한다. 이 미묘한 차이는 공식 docs에도 그리 도드라지게 적혀 있지 않아 직접 디버깅으로 알아내는 경우가 많다. 한 번 알고 나면 별 것 아닌데, 모르면 한참 헤맨다.

### `AuthenticationProvider`의 실전 — `DaoAuthenticationProvider`

가장 자주 만나는 provider는 폼 로그인의 짝꿍인 `DaoAuthenticationProvider`다. 이 친구의 일은 두 단계로 나뉜다. 먼저 `UserDetailsService`로 username에 해당하는 `UserDetails`를 가져온다. 그다음 `PasswordEncoder`로 비밀번호를 비교한다. 두 단계가 모두 통과하면 비밀번호를 지운 새 토큰을 돌려준다.

```java
@Bean
DaoAuthenticationProvider daoProvider(UserDetailsService uds,
                                       PasswordEncoder enc) {
    DaoAuthenticationProvider p = new DaoAuthenticationProvider();
    p.setUserDetailsService(uds);
    p.setPasswordEncoder(enc);
    return p;
}
```

`UserDetailsService`는 거의 모든 폼 로그인 튜토리얼의 주인공이다. 그런데 자주 놓치는 사실이 하나 있다. **`UserDetailsService`는 인증 단계에서만 호출된다.** 인가 결정 단계에서 매번 DB를 다시 뒤지지 않는다. 한 번 인증을 통과한 사용자의 권한은 `SecurityContextHolder`에 보관된 `Authentication` 객체 안에 박혀 있고, 이후의 모든 요청은 그 박힌 값을 그대로 쓴다. 그래서 사용자의 권한을 DB에서 바꿔도 그 사용자가 다시 로그인하기 전까지는 반영되지 않는다. 운영 중에 "관리자 권한을 회수했는데 왜 여전히 들어가지느냐"는 질문이 들어오면, 답은 거의 항상 여기 있다. 권한을 즉시 회수하고 싶다면 세션 자체를 만료시키거나, 매 요청마다 권한을 재조회하는 별도 패턴을 도입해야 한다. 후자는 성능 부담이 따른다. 보안과 성능 사이의 익숙한 줄다리기다.

### `AuthenticationManagerResolver` — 다중 issuer/멀티 테넌트

지금까지의 그림은 "애플리케이션 하나에 `AuthenticationManager` 하나"라는 가정 위에 서 있다. 그런데 SaaS 환경을 떠올려보자. 같은 자원 서버가 여러 테넌트의 사용자를 받는다. 테넌트 A의 토큰은 IdP A가 발급하고, 테넌트 B의 토큰은 IdP B가 발급한다. JWK 키도 다르고 issuer URL도 다르다. 이 상황에서 단일 `AuthenticationManager`로 모든 요청을 처리하려고 들면 매우 번거롭다.

이 문제에 답하는 것이 `AuthenticationManagerResolver`다.

```java
public interface AuthenticationManagerResolver<C> {
    AuthenticationManager resolve(C context);
}
```

요청 컨텍스트를 받아서 그 요청에 맞는 `AuthenticationManager`를 골라준다. 자원 서버의 경우에는 보통 JWT의 issuer claim을 읽어 테넌트를 식별하고, 그 테넌트 전용 매니저를 돌려준다. Spring Security는 `JwtIssuerAuthenticationManagerResolver`라는 미리 만들어진 구현체를 제공한다.

```java
JwtIssuerAuthenticationManagerResolver resolver =
    JwtIssuerAuthenticationManagerResolver.fromTrustedIssuers(
        "https://idp-a.example.com",
        "https://idp-b.example.com"
    );

http.oauth2ResourceServer(oauth2 -> oauth2
    .authenticationManagerResolver(resolver));
```

이 한 줄짜리 추상화가 7.0에서도 그대로 살아 있다는 점이 반갑다. 5장에서 자원 서버를 다룰 때 이 resolver를 다시 만나게 된다. 지금은 "단일 매니저로 부족하면 resolver를 끼울 수 있다"는 사실만 기억해두면 충분하다.

## `AuthorizationManager` — 인가의 신모델, 그리고 사라진 `check`

여기서부터가 7.0의 진짜 변화다. 결론부터 말하면 7.0에서 `AuthorizationManager` 인터페이스는 더 이상 `check` 메서드를 가지지 않는다. 오직 `authorize`만 남았다.

```java
@FunctionalInterface
public interface AuthorizationManager<T> {
    AuthorizationResult authorize(Supplier<Authentication> auth, T object);

    default void verify(Supplier<Authentication> auth, T object) {
        AuthorizationResult result = authorize(auth, object);
        if (result != null && !result.isGranted()) {
            throw new AuthorizationDeniedException("Access Denied", result);
        }
    }
}
```

`check`는 어디로 갔는가? 5.5 시점부터 deprecated였고, 7.0에서 완전히 제거됐다. 그렇다면 왜 사라진 걸까? 두 가지 이유가 함께 작용했다. 첫째, `check`가 돌려주던 `AuthorizationDecision`은 단순한 boolean 래퍼였다. `authorize`가 돌려주는 `AuthorizationResult`는 같은 boolean에 더 풍부한 부가 정보(거부 사유, 권장 응답 등)를 실을 여지를 가진 상위 추상이다. 둘째, 메서드 이름이 두 개라는 사실 자체가 불필요한 혼란이었다. 같은 의미를 가진 API가 두 개 있을 이유가 없다.

이 변경은 표면적으로는 단순한 이름 정리지만, 6.x 코드를 7.0으로 옮기는 사람에게는 꽤 성가신 일이 된다. 다음 코드를 보자.

```java
// 6.x — 7.0에서는 컴파일 에러
AuthorizationManager<RequestAuthorizationContext> mgr = (auth, ctx) -> {
    return new AuthorizationDecision(auth.get().getAuthorities()
        .stream().anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN")));
};
http.authorizeHttpRequests(a -> a
    .requestMatchers("/admin/**").access(mgr));
```

7.0에서 이 코드는 두 곳에서 빨갛게 변한다. `AuthorizationDecision`을 직접 만들고 있는 부분, 그리고 람다 안에서 `check`처럼 동작하던 시그니처가 `authorize`로 바뀐 부분. 7.0에서는 다음처럼 적는다.

```java
// 7.0
AuthorizationManager<RequestAuthorizationContext> mgr = (auth, ctx) -> {
    boolean granted = auth.get().getAuthorities()
        .stream().anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));
    return new AuthorizationDecision(granted);  // AuthorizationResult 구현체
};
```

`AuthorizationDecision` 자체는 7.0에서도 살아남았다 — 그저 `AuthorizationResult` 인터페이스의 구현체로 재배치됐을 뿐이다. 그래서 거의 모든 마이그레이션은 람다 시그니처와 메서드 이름만 고치면 끝난다. 그런데 람다를 직접 작성하지 않고 미리 만들어진 매니저를 쓰는 코드 — 즉 `AuthorityAuthorizationManager.hasRole("ADMIN")` 같은 호출 — 은 손댈 필요조차 없다. 미리 만들어진 매니저들이 7.0의 새 시그니처로 이미 갱신되어 있기 때문이다.

13장 마이그레이션 챕터에서 이 부분을 다시 자세히 살펴보겠다. 지금은 "이름만 바뀐 것이지만 무시할 수 없는 변화"라는 점, 그리고 "기성품 매니저를 쓰면 무난히 넘어간다"는 점을 기억해두자.

### 다섯 개의 주요 구현체

`AuthorizationManager`는 인터페이스지만, 7.0이 기본 제공하는 구현체 다섯 가지가 거의 모든 인가 시나리오를 덮는다. 하나씩 살펴보자.

**`AuthorityAuthorizationManager`** — 가장 흔히 쓰는 매니저다. 특정 권한 하나(또는 OR 조건)를 가진 사용자만 통과시킨다. `hasRole("ADMIN")`, `hasAuthority("SCOPE_orders.read")`, `hasAnyRole("ADMIN", "MANAGER")` 같은 익숙한 호출의 뒤에서 일하는 친구다.

```java
AuthorizationManager<RequestAuthorizationContext> adminOnly =
    AuthorityAuthorizationManager.hasRole("ADMIN");
```

**`AuthenticatedAuthorizationManager`** — 권한이 아니라 "어떤 종류의 인증"을 거쳤느냐를 따진다. `authenticated()`, `fullyAuthenticated()`, `rememberMe()`, `anonymous()`의 네 가지 모드를 가진다. 가장 자주 쓰이는 모드는 두 개. `authenticated()`는 익명이 아닌 모든 인증된 사용자를 통과시킨다. `fullyAuthenticated()`는 Remember-Me로 들어온 사용자는 막고 직접 로그인한 사용자만 통과시킨다. "비밀번호 변경 같은 민감한 화면은 fully만"이라는 패턴이 여기서 나온다.

**`RequestMatcherDelegatingAuthorizationManager`** — URL 기반 인가의 엔진이다. URL 패턴을 키로, 그 패턴에 적용할 매니저를 값으로 가진 맵을 들고 있다가, 요청이 들어오면 매칭되는 첫 항목을 찾아 위임한다. `authorizeHttpRequests` DSL의 모든 `requestMatchers(...).hasRole(...)` 호출은 결국 이 매니저의 맵에 항목을 한 줄씩 추가하는 셈이다. 사용자가 직접 인스턴스화할 일은 거의 없지만, 디버거에서 인가 흐름을 따라가다 보면 자주 마주친다.

**`AllAuthoritiesAuthorizationManager`** — 7.0 신규다. 이름이 모든 것을 말한다. 여러 권한을 **모두** 가진 사용자만 통과시키는 AND 조건 매니저다. 기존 `hasAnyRole`이 OR였던 것과 정확히 대비된다.

```java
AuthorizationManager<RequestAuthorizationContext> mfaRequired =
    AllAuthoritiesAuthorizationManager.hasAllAuthorities(
        "factor:password", "factor:ott");
```

이 매니저가 신규로 등장한 데에는 배경이 있다. MFA(Multi-Factor Authentication)가 7.0에서 1급 시민이 됐다는 점이다. 7장에서 자세히 다루지만, 7.0의 MFA 모델은 각 factor를 권한으로 표현한다. 비밀번호를 통과하면 `factor:password` 권한을, OTT를 통과하면 `factor:ott` 권한을 추가하는 식이다. 그리고 보호된 자원에 들어가려면 두 factor 모두 통과해야 한다 — 즉 두 권한을 **모두** 가져야 한다. 이 의미를 표현하려고 OR 매니저만 있던 시절에는 SpEL이나 커스텀 매니저로 우회해야 했다. 이제는 한 줄로 표현된다.

**`AuthorizationManagerFactory`** — 마지막은 매니저 자체가 아니라 매니저를 만드는 공장이다. 7.0 신규. `permitAll()`, `hasRole()`, `hasAnyRole()` 같은 빌더 메서드를 한 곳에 모아 둔 추상이다. 평소에는 무심코 지나치게 되지만, **기본 prefix를 바꾸거나, `RoleHierarchy`를 끼우거나, `AuthenticationTrustResolver`를 갈아끼우고 싶을 때** 이 팩토리 한 군데만 손대면 모든 매니저가 그 변경을 받는다.

```java
@Bean
AuthorizationManagerFactory<RequestAuthorizationContext> mgrFactory(
        RoleHierarchy hierarchy) {
    DefaultAuthorizationManagerFactory<RequestAuthorizationContext> factory =
        new DefaultAuthorizationManagerFactory<>();
    factory.setRoleHierarchy(hierarchy);
    return factory;
}
```

6.x까지는 `RoleHierarchy`를 전역에 적용하기 위해 별도의 빈을 여러 군데 끼워 넣어야 했고, 그 과정에서 "여기엔 적용되고 저기엔 안 된다"는 작은 불일치가 자주 발생했다. 팩토리 추상이 도입되면서 그 불일치가 한 군데에서 처리된다. 작은 변화처럼 보이지만 7장 MFA와 8장 인가에서 자주 도움이 된다.

### `AccessDecisionManager`/`Voter`의 분리 — 어디로 갔는가

여기서 또 하나의 변화가 등장한다. 7.0 이전 시대의 인가 모델은 사실 두 개가 공존했다. 신모델인 `AuthorizationManager`와, 그보다 오래된 `AccessDecisionManager` + `AccessDecisionVoter` 조합이다. 후자는 5.5에서 deprecated 처리됐지만 7.0 이전까지는 기본 의존성에 함께 들어 있었다. 7.0에서 이 레거시 API는 **별도 모듈 `spring-security-access`로 격리됐다.** 기본 의존성에는 더 이상 포함되지 않는다.

운영 중인 코드가 옛 모델을 직접 의존하고 있다면 두 갈래의 선택지가 있다. 첫째, `build.gradle`에 `spring-security-access`를 명시적으로 추가해서 일단 빌드를 통과시키는 임시 처방. 둘째, 사용처를 `AuthorizationManager`로 옮겨 적는 본격 처방. 임시 처방은 진짜 임시여야 한다. 별도 모듈에 들어갔다는 것은 향후 메이저 릴리스에서 완전히 사라질 가능성이 매우 높다는 신호이기 때문이다.

이주 동선은 의외로 단순하다. `AccessDecisionVoter` 하나를 `AuthorizationManager` 하나로 갈아끼우면 된다. voter의 `vote()` 메서드가 돌려주던 `ACCESS_GRANTED`/`ACCESS_DENIED`/`ACCESS_ABSTAIN`은 `AuthorizationManager.authorize()`가 돌려주는 `AuthorizationDecision`의 `granted` 여부와 거의 1:1 대응된다. 다만 ABSTAIN(기권)은 신모델에 없다 — null을 돌려주는 것이 의미상 가장 가깝다. 여러 voter를 조합하던 `AffirmativeBased`/`ConsensusBased`/`UnanimousBased` 같은 manager들은 `RequestMatcherDelegatingAuthorizationManager`나 직접 작성한 합성 매니저로 옮긴다. 13장에서 이 이주를 단계별로 다시 살펴보자.

## `SecurityContextHolder` — 컨텍스트는 어디에 사는가

지금까지 우리는 "누가 인증을 결정하느냐", "누가 인가를 결정하느냐"를 따라왔다. 그런데 인증이 결정된 다음, 그 결과인 `Authentication` 객체는 어디에 보관되는가? 한 요청 안에서 컨트롤러가 `@AuthenticationPrincipal`로 받아 쓰는 그 객체는 어떤 저장소에 사는가? 답이 `SecurityContextHolder`다.

`SecurityContextHolder`는 정적 유틸리티처럼 생긴 객체다. `getContext()`로 현재 컨텍스트를 가져오고, `setContext()`로 채워 넣는다. 컨텍스트는 곧 `SecurityContext`이고, 그 안에 `Authentication`이 하나 들어 있다.

```java
SecurityContext ctx = SecurityContextHolder.getContext();
Authentication auth = ctx.getAuthentication();
```

이 컴포넌트의 핵심은 "전역적으로 보이지만 사실은 스레드별로 격리된다"는 점이다. A 사용자의 요청을 처리하는 스레드 1과 B 사용자의 요청을 처리하는 스레드 2가 같은 `SecurityContextHolder.getContext()`를 호출해도 서로 다른 컨텍스트를 받는다. 이 격리는 `ThreadLocal`이 책임진다.

그런데 격리 전략이 하나만 있는 게 아니다. `SecurityContextHolder`는 세 가지 전략을 지원한다.

### 세 가지 저장 전략

**`MODE_THREADLOCAL`** (기본값) — 컨텍스트가 현재 스레드에만 매여 산다. 자식 스레드로는 자동 전파되지 않는다. 가장 안전한 선택이다. 서블릿 컨테이너의 요청 스레드 모델과 자연스럽게 맞물린다.

**`MODE_INHERITABLETHREADLOCAL`** — 자바의 `InheritableThreadLocal`을 사용한다. 부모 스레드의 컨텍스트가 자식 스레드 생성 시점에 자동으로 복사된다. `@Async`를 도입했는데 비동기 메서드 안에서 `SecurityContextHolder.getContext()`가 비어 있을 때, 처음 만나는 유혹이 이 모드다. "한 줄로 해결되네"라는 생각이 든다.

**`MODE_GLOBAL`** — 컨텍스트가 JVM 전체에서 공유된다. 데스크톱 자바 애플리케이션에서나 쓸 법한 모드다. 멀티 사용자를 다루는 서버에서 이 모드를 켜는 것은 모든 사용자에게 같은 신원을 부여하는 셈이다. 거의 만나지 않는 선택이지만, 잊지 말자 — 만약 마주친다면 그것은 거의 항상 실수다.

기본값인 `MODE_THREADLOCAL`이 가장 안전하다는 점은 의심의 여지가 없다. 그렇다면 비동기 전파는 어떻게 해야 할까? 그 답을 보기 전에, `MODE_INHERITABLETHREADLOCAL`이 왜 그렇게 위험한지를 먼저 짚어 두자. 한 번 만나면 잊기 어려운 종류의 함정이다.

### `InheritableThreadLocal` + 스레드 풀 — 끔찍한 일이 될 수 있다

이런 상황을 가정해보자. 어느 팀이 `@Async`를 도입했고, 비동기 메서드 안에서 `SecurityContextHolder.getContext().getAuthentication()`이 null이라 당황한다. 검색해보니 누군가 답을 알려준다.

> "`SecurityContextHolder.setStrategyName(SecurityContextHolder.MODE_INHERITABLETHREADLOCAL)`을 부르면 자식 스레드로 컨텍스트가 흘러갑니다."

한 줄짜리 해결책. 적용해보니 진짜로 작동한다. 비동기 메서드 안에서도 사용자 정보가 보인다. 며칠 동안 문제가 없다. 그러다 어느 날 보안팀에서 이상한 보고를 받는다. 사용자 A가 자신의 페이지에 사용자 B의 이름이 보였다고 한다. 처음에는 캐싱 문제로 의심한다. 캐시를 끄고도 재현된다. 로그를 한참 뒤지다 보면 한 가지 패턴이 보인다 — 비동기 작업의 결과가 다른 사용자의 컨텍스트를 들고 돌아온다.

이게 어떻게 가능한지 살펴보자. `@Async`는 보통 `ThreadPoolTaskExecutor` 같은 **풀 스레드** 위에서 돈다. 풀이라는 말의 의미는 명확하다. 한 번 만들어진 스레드는 작업이 끝나도 사라지지 않고 풀로 돌아가 다음 작업을 기다린다. 그런데 `InheritableThreadLocal`은 스레드가 **생성되는 시점**에 부모의 값을 복사한다. 풀의 스레드가 처음 만들어졌을 때 그 부모 — 즉 그 시점의 요청 스레드 — 의 컨텍스트가 풀 스레드에 영원히 박힌다. 그 풀 스레드가 다음 사용자의 요청을 처리할 때, 이전 사용자의 컨텍스트가 그대로 살아 있다.

> "When Spring Async annotation is used with `MODE_INHERITABLETHREADLOCAL`, with thread pools this is dangerous because when a thread is reused from a pool, the security context which was set for the thread when it was created is reused, leading to an issue where a task relies on a completely wrong, some other user's security context." — Spring Security 이슈 트래커 #6856

찜찜한 정도가 아니다. 끔찍한 일이다. 사용자 A의 비동기 작업이 사용자 B의 권한으로 데이터에 접근하고 있을 수 있다. 사용자 B의 비밀번호 변경 요청이 사용자 A의 신원으로 처리될 수도 있다. 운영 환경에서 이 문제가 발현되면 보안 사고는 거의 불가피하다.

이 함정을 피하는 길은 두 가지다. 첫째이자 정도(正道)는 **`MODE_INHERITABLETHREADLOCAL`을 쓰지 않는 것.** 기본값 `MODE_THREADLOCAL`을 유지하면 이 시나리오 자체가 성립하지 않는다. 둘째는 컨텍스트가 자식 스레드로 흘러야 할 때 **자동 상속에 기대지 말고 명시적으로 전파하는 것.** Spring Security가 그 명시적 전파를 위한 도구를 미리 준비해 두었다.

### 명시적 전파 — `DelegatingSecurityContext*`

핵심 도구는 세 가지다. `DelegatingSecurityContextRunnable`, `DelegatingSecurityContextCallable`, 그리고 `DelegatingSecurityContextAsyncTaskExecutor`. 이름이 길지만 기능은 단순하다. 작업을 감싸서 "현재 스레드의 컨텍스트를 캡처해 둔 뒤, 작업이 실행될 때 그 스레드에 그 컨텍스트를 잠시 심어 두고, 작업이 끝나면 깨끗이 치운다." 풀 스레드를 쓰더라도 누수가 발생하지 않는다.

가장 자주 쓰는 패턴은 Executor 자체를 감싸는 방식이다. 한 번 설정해 두면 `@Async`로 보내는 모든 작업이 자동으로 안전한 전파를 받는다.

```java
@Bean
AsyncTaskExecutor delegatingExecutor(ThreadPoolTaskExecutor base) {
    return new DelegatingSecurityContextAsyncTaskExecutor(base);
}
```

이 한 줄로 충분하다. `@Async` 메서드 본문 어디서나 `SecurityContextHolder.getContext()`가 정확히 호출자의 컨텍스트를 돌려준다. 게다가 풀 스레드 누수도 없다. 작업이 끝나면 컨텍스트가 치워지기 때문이다. `MODE_INHERITABLETHREADLOCAL`의 "한 줄짜리 마법"보다 훨씬 안전한 한 줄이다.

수동으로 작업을 감쌀 일이 있다면 `Runnable`/`Callable` 버전을 쓴다.

```java
SecurityContext ctx = SecurityContextHolder.getContext();
executor.submit(new DelegatingSecurityContextCallable<>(() -> {
    // 여기서 SecurityContextHolder.getContext()는 ctx와 같다
    return doSomething();
}, ctx));
```

10장에서 세션·쿠키·컨텍스트 전파를 종합적으로 다룰 때 이 패턴들이 다시 등장한다. 지금은 "비동기 전파가 필요하면 모드를 바꾸지 말고 명시적으로 감싸자"는 원칙만 박아 두자.

### Virtual Threads — Java 21+ 시대의 안전망

자바 21이 가져온 가상 스레드(Virtual Threads)는 이 그림에 또 다른 변수를 던진다. 가상 스레드는 풀이 아니다. 각 작업마다 새로 만들어지고 작업이 끝나면 회수된다. 그렇다면 `ThreadLocal`은 어떻게 동작할까? 가상 스레드도 일반 스레드와 똑같이 `ThreadLocal`을 지원하지만, **스레드가 작업 단위로 새로 만들어지기 때문에 풀 누수가 본질적으로 발생하지 않는다.** 즉 `MODE_THREADLOCAL`만으로도 비동기 컨텍스트 누수가 사라진다.

이것이 7.0 시대의 새로운 풍경이다. Spring Boot 4.0이 가상 스레드를 1급으로 받아들이고, `spring.threads.virtual.enabled=true` 한 줄로 서블릿 컨테이너의 요청 처리 스레드도 가상 스레드로 갈아끼울 수 있게 됐다. 이 시대에는 `MODE_INHERITABLETHREADLOCAL`을 떠올릴 이유 자체가 거의 사라진다.

다만 가상 스레드에도 자기 나름의 까다로움이 있다. 가장 자주 거론되는 것이 carrier thread pinning — 가상 스레드가 동기화 블록이나 JNI 호출에 갇혀 carrier 스레드를 점유하는 현상이다. 그러나 이것은 SecurityContext의 안전성과는 다른 차원의 문제이고, Spring 공식 문서도 아직 가상 스레드와 Security의 상호작용에 대해서는 빈약한 편이다. 7.1.x 마일스톤에서 이 부분이 더 정리될 것으로 기대된다. 지금 우리가 기억해 둘 한 줄은 단순하다. **가상 스레드 위에서 `MODE_THREADLOCAL`은 비동기 전파 문제를 자연스럽게 녹인다 — 단, `DelegatingSecurityContext*`로 안전망을 한 겹 더 두는 것이 여전히 권장된다.** 무료로 얻는 안전을 굳이 마다할 이유가 없다.

## 세 컴포넌트를 한 그림으로

여기까지 따라왔다면 머릿속에 세 가지 어휘가 자리를 잡았을 것이다. `AuthenticationManager`가 신원을 만들고, `SecurityContextHolder`가 그 신원을 보관하고, `AuthorizationManager`가 그 신원으로 자원 접근을 결정한다. 이 셋의 협업이 한 요청의 보안 처리 전부다. 한 그림으로 정리해보자.

```
[Auth Filter]                                  [AuthorizationFilter]
     │                                                   │
     │ authenticate(Token)                               │ authorize(Authentication, RequestContext)
     ▼                                                   ▼
AuthenticationManager                            AuthorizationManager
   = ProviderManager                                = RequestMatcherDelegating...
       │                                                 │
       ├─ DaoAuthenticationProvider                      ├─ AuthorityAuthorizationManager
       ├─ JwtAuthenticationProvider                      ├─ AuthenticatedAuthorizationManager
       └─ ...                                            ├─ AllAuthoritiesAuthorizationManager
                                                         └─ (사용자 정의)
              │                                                 │
              ▼                                                 ▼
         SecurityContextHolder.setContext(...)            granted? → 통과 / denied? → AccessDeniedException
              │
              ▼
         SecurityContextRepository에 저장
              │
              ▼
     다음 요청에서 다시 꺼냄
```

`AuthorizationManagerFactory`는 이 그림의 가운데 어디쯤 — 인가 매니저들을 만드는 공장으로서 — 자리 잡는다. `AuthenticationManagerResolver`는 왼쪽의 매니저 자리를 요청 컨텍스트에 따라 동적으로 갈아끼우는 역할을 한다. 이 둘은 단일 매니저 가정이 부족할 때 슬쩍 끼어드는 추상이다.

이 그림 한 장이 이후 챕터의 거의 모든 보안 결정의 좌표축이 된다. 4장에서 폼 로그인을 다룰 때 `DaoAuthenticationProvider`가 어느 자리에 사는지를 다시 떠올리자. 5장에서 JWT 자원 서버를 다룰 때 `JwtAuthenticationProvider`와 `JwtIssuerAuthenticationManagerResolver`가 어디에 꽂히는지 떠올리자. 7장에서 MFA를 다룰 때 `AllAuthoritiesAuthorizationManager`가 왜 신규로 등장했는지 떠올리자. 8장에서 인가의 5층 구조를 풀 때 `AuthorizationManagerFactory`가 왜 한 군데에서 모든 매니저를 일관되게 만드는 이점을 주는지 떠올리자. 같은 그림, 같은 어휘, 다른 시나리오다.

## 마무리

이 챕터는 어휘를 박는 챕터였다. 이름들이 익숙해도 책임을 정확히 짝지을 수 있는지를 점검해 보자. 누군가 "5.x 코드에서 `AuthorizationManager.check`를 부르고 있는데 7.0으로 옮기면 어디부터 손대야 하느냐"고 묻는다면 답을 그릴 수 있는가? `@Async` 메서드 안에서 컨텍스트가 비어 있다는 동료에게 `MODE_INHERITABLETHREADLOCAL`이 아니라 `DelegatingSecurityContextAsyncTaskExecutor`를 권하면서 그 이유를 한 문단으로 풀어낼 수 있는가? 권한이 그저 문자열이라는 단순함이 왜 인가 모델의 일관성을 떠받치는지 설명할 수 있는가? 이 세 질문에 답할 수 있다면 우리는 이 챕터의 일을 끝낸 셈이다.

### 챕터 요약 5줄

1. `Authentication`은 인증 전/후를 같은 인터페이스로 표현하고, `GrantedAuthority`는 권한을 그저 문자열로 표현해 모든 인증 시나리오를 같은 인가 모델로 합류시킨다.
2. `AuthenticationManager`의 실전 구현은 `ProviderManager`이며, 여러 `AuthenticationProvider`를 책임 연쇄 패턴으로 순회하면서 `supports()` 매칭으로 토큰을 분배한다.
3. 7.0에서 `AuthorizationManager#check`는 제거되고 `authorize`만 남았다. 주요 구현체 다섯(`AuthorityAuthorizationManager`, `AuthenticatedAuthorizationManager`, `RequestMatcherDelegatingAuthorizationManager`, 신규 `AllAuthoritiesAuthorizationManager`, 신규 `AuthorizationManagerFactory`)이 거의 모든 인가 시나리오를 덮는다.
4. `AccessDecisionManager`/`Voter` 레거시는 `spring-security-access` 별도 모듈로 격리됐다 — 임시방편으로 의존성을 추가할 수 있지만 본격 이주는 `AuthorizationManager`로.
5. `SecurityContextHolder.MODE_INHERITABLETHREADLOCAL` + 스레드 풀은 다른 사용자의 컨텍스트가 다음 요청에 새는 끔찍한 함정이다. `DelegatingSecurityContextAsyncTaskExecutor`로 명시 전파하거나, 가상 스레드 위에서 `MODE_THREADLOCAL`을 유지하자.

### 다음 챕터에서 답할 것

여기까지 우리는 책의 토대 둘 — 필터 체인(2장)과 컴포넌트 모델(3장) — 을 박았다. 이제 이 어휘를 들고 인증 시나리오의 첫 번째인 폼 로그인의 세계로 들어간다. 가장 오래된 인증 방식이 7.0에서도 어떻게 살아 있고, 어떤 함정이 여전한가? `requireExplicitSave(true)`가 왜 권장 기본값이 됐고, Remember-Me는 어디서 멈춰야 하는가? `PasswordEncoder` 선택은 7.0의 Password4j 인코더 5종까지 와서 어떻게 달라졌는가? 다음 챕터에서 답하자.
