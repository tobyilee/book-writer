# 6장. OAuth2 Client + OIDC Login — 외부 IdP에 로그인을 위임하다

이번엔 우리 시스템이 IdP를 신뢰하는 클라이언트가 된다. 5장에서는 외부에서 발급된 JWT를 받아 검증하기만 하면 됐다. 자원 서버는 키를 들고 서명만 맞춰보면 그만이었다. 그런데 이번 장의 입장은 정반대다. 우리가 직접 사용자에게 로그인 화면을 보여주는 대신, "Sign in with Google" 버튼 하나를 띄워두고 Google에게 신원 확인을 맡긴다. 사용자는 Google 화면에서 이메일과 비밀번호를 친다. 우리 서버는 그 어떤 비밀번호도 보지 않는다. Google이 "이 사용자 맞아요"라고 신호만 보내준다.

자, 그러면 그 한 번의 버튼 클릭 뒤에서 무슨 일이 벌어지는지 그려보자. 흐름이 머릿속에 또렷이 그려지지 않으면, 나중에 콜백 URL 한 글자 때문에 두 시간을 날려도 영문을 모른다. 차근차근 따라가 보자.

## 한 번의 버튼 클릭, 일곱 번의 왕복

브라우저 주소창에 `/oauth2/authorization/google` 이 한 줄이 찍히는 순간부터 이야기가 시작된다. 사용자가 직접 칠 일은 거의 없고, 우리가 만든 로그인 페이지의 "Sign in with Google" 링크가 이 경로를 가리킨다. 이 경로가 어떻게 동작하는지부터 보자.

Spring Security 7에 `oauth2Login()`을 켜는 순간, 필터 체인 안에 두 개의 필터가 자리를 잡는다. 하나는 `OAuth2AuthorizationRequestRedirectFilter`, 다른 하나는 `OAuth2LoginAuthenticationFilter`. 이름이 길어서 부담스러운데, 역할로 외워두면 편하다. 앞 녀석은 사용자를 IdP로 *떠밀어 보내는* 필터고, 뒤 녀석은 IdP가 *돌려보낸 결과를 받는* 필터다. 둘이 한 짝이다.

먼저 첫 번째 필터의 일을 따라가 보자. 사용자가 `/oauth2/authorization/google`로 들어왔다. 필터는 경로 끝의 `google`을 보고 "아, 이 사용자는 google이라는 registration으로 로그인하려는구나" 하고 알아차린다. 그 정보를 `ClientRegistrationRepository`에서 꺼낸다. 거기에는 우리가 application.yml에 적어둔 `client-id`, `client-secret`, `redirect-uri`, `scope` 같은 메타데이터가 들어 있다. 필터는 이 정보를 바탕으로 IdP의 인가 엔드포인트(보통 `https://accounts.google.com/o/oauth2/v2/auth`)로 가는 URL을 조립한다. 그 URL에는 우리 client_id, 우리가 요청하는 scope, state 값, redirect_uri, 그리고 7.0부터는 기본으로 PKCE 챌린지까지 붙어 있다.

조립이 끝나면 필터는 사용자 브라우저에 `302 Found` 응답을 내려보낸다. 사용자는 곧장 Google 로그인 화면으로 떠밀려 간다. 우리 서버는 잠시 사용자를 잊는다.

사용자는 Google 화면에서 이메일과 비밀번호를 입력하고, "이 앱이 당신의 이메일과 프로필을 보겠다는데 허락하시겠습니까?" 같은 동의 화면을 마주한다. 동의하는 순간, Google은 사용자 브라우저를 우리가 등록해둔 `redirect_uri`로 다시 떠민다. 이 콜백 경로가 바로 `/login/oauth2/code/google`이다. URL에는 `code=...&state=...` 두 개의 쿼리 파라미터가 붙어 있다. 그 `code`가 우리가 받아내야 할 *인가 코드*다.

이제 두 번째 필터, `OAuth2LoginAuthenticationFilter`가 깨어난다. 이 필터는 자기에게 들어온 요청의 `state`가 처음에 우리가 만들어 IdP에 던졌던 그 state와 일치하는지부터 확인한다. 일치하지 않으면 CSRF 가능성을 의심해 즉시 거절한다. 일치하면 다음 단계로 넘어가는데, 여기서부터가 진짜 핵심이다.

필터는 IdP의 토큰 엔드포인트(`https://oauth2.googleapis.com/token` 같은 곳)에 백채널로 직접 POST를 친다. 이 호출은 사용자 브라우저를 거치지 않는다. 우리 서버가 IdP에 직통으로 묻는다. 요청 바디에는 방금 받은 `code`, 우리 `client_id`/`client_secret`, 그리고 PKCE를 켰다면 `code_verifier`까지 들어간다. IdP는 이 셋이 모두 맞으면 `access_token`과 (OIDC 흐름이면) `id_token`을 돌려준다. 코드를 토큰으로 *교환*한다고 흔히 부르는 단계다.

토큰을 받으면 필터는 `id_token`을 디코드한다. 5장에서 다룬 JWT 디코딩과 똑같은 절차다. 헤더의 `kid`로 IdP의 JWKs에서 공개키를 찾고, 서명을 검증하고, `iss`/`aud`/`exp`/`nonce` 클레임을 일일이 확인한다. 검증을 통과한 `id_token`의 페이로드가 `OidcIdToken` 객체가 되고, 이걸 바탕으로 `OidcUser` 인스턴스가 만들어진다. `OidcUser`는 `OAuth2User`의 확장이고, 결국 `Authentication` 객체로 감싸여 `SecurityContextHolder`에 안착한다.

여기까지가 흔히 말하는 *Authorization Code Flow*다. 그림으로 정리해두자.

```
[브라우저] ──(1) /oauth2/authorization/google──> [우리 서버]
[우리 서버] ──(2) 302 redirect─────────────────> [브라우저]
[브라우저] ──(3) GET accounts.google.com/auth?…> [Google]
[Google]   ─ 로그인 + 동의 화면
[Google]   ──(4) 302 redirect with code, state─> [브라우저]
[브라우저] ──(5) GET /login/oauth2/code/google──> [우리 서버]
[우리 서버] ──(6) POST /token (백채널)─────────> [Google]
[Google]   ──(7) access_token + id_token───────> [우리 서버]
[우리 서버] ─ id_token 검증 → OidcUser 생성 → 세션 확립
[우리 서버] ──(8) 302 redirect to /───────────> [브라우저]
```

이 여덟 단계가 한 번의 버튼 클릭 뒤에 일어난다. 사용자 입장에서는 그저 "Sign in with Google을 눌렀더니 우리 사이트에 로그인됐다"이지만, 내부적으로는 브라우저가 세 번, 서버 간 백채널이 한 번, 총 네 차례의 왕복이 발생한다. 어디 한 군데가 어긋나면 사용자는 "Login Failed"만 보고, 우리는 로그를 뒤져야 한다. 그러니 어디서 무엇이 오가는지를 머릿속에 또렷이 그려두는 편이 낫다.

## 이걸 켜는 데 필요한 코드

이 모든 흐름을 활성화하는 코드는 놀랍게도 짧다. 살펴보자.

```java
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2Login(Customizer.withDefaults())
        .build();
}
```

`oauth2Login(Customizer.withDefaults())` 단 한 줄. 그리고 `application.yml` 쪽에 IdP 메타데이터를 적어준다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope:
              - openid
              - email
              - profile
        provider:
          google:
            issuer-uri: https://accounts.google.com
```

여기서 마법 같은 한 줄이 `issuer-uri`다. 이 한 줄을 적어두면 Spring Security는 부팅할 때 `https://accounts.google.com/.well-known/openid-configuration`을 한 번 조회한다. 그 응답에 인가 엔드포인트, 토큰 엔드포인트, userinfo 엔드포인트, JWKs URL, 지원하는 알고리즘 목록이 전부 들어 있다. 이를 *OIDC discovery*라고 부르고, 우리는 이 URL들을 일일이 적어둘 필요가 없어진다. 자그마한 줄 하나가 메타데이터 다섯 개를 알아서 채운다.

기억해두자. 5장의 자원 서버 쪽도 `issuer-uri` 한 줄로 JWKs URL과 디코더를 자동 구성했다. 이 장의 클라이언트 쪽도 마찬가지다. Spring Security가 OIDC 표준 위에 얇은 컨벤션을 얹어둔 결과다. 우리가 외울 게 적을수록 사고가 적다.

`registration.google` 이름을 우리 마음대로 바꿔도 좋다. `registration.my-keycloak`, `registration.azure-ad` 같은 식이다. 그 이름이 곧 URL 조각이 된다. 우리가 `keycloak`이라고 적으면 사용자가 갈 경로는 `/oauth2/authorization/keycloak`이 되고, 콜백은 `/login/oauth2/code/keycloak`이 된다. 이 컨벤션이 너무 일관적이라 처음엔 신기하다.

Keycloak이라면 이렇게 적힌다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: my-app
            client-secret: ${KEYCLOAK_SECRET}
            scope: [openid, email, profile]
        provider:
          keycloak:
            issuer-uri: https://auth.example.com/realms/app
```

`issuer-uri`가 `accounts.google.com`이든 `auth.example.com/realms/app`이든 코드 쪽은 손댈 게 없다. IdP를 바꾸는 일이 application.yml 한 블록의 변경이 되도록, OIDC discovery가 그 사이를 다 흡수한다.

## ID Token과 Access Token, 헷갈리지 말자

여기서 한 번 멈춰서 토큰 둘의 차이를 못 박아두자. 둘을 헷갈리면 보안 모델 전체가 무너진다.

비유부터 가자. **ID Token은 여권이고, Access Token은 출입증이다.** 여권은 "이 사람이 누구인지"를 증명한다. 사진과 이름이 박혀 있고, 발급 기관이 서명해뒀다. 출입증은 "이 사람이 이 건물의 이 층에 들어갈 수 있다"를 증명한다. 출입증 자체에는 사진이 없을 수도 있다. 카드를 가진 사람이 그 권한을 가졌다는 뜻일 뿐이다.

ID Token도 마찬가지다. JWT 형식이고, `sub`(사용자 식별자), `name`, `email`, `picture` 같은 사용자 정보가 페이로드에 들어 있다. 누구에게 발급된 토큰인지(`aud` 클레임)는 *우리 client_id*가 박혀 있다. 즉 이 토큰은 *우리에게* 발급된, *사용자 신원 증명용*이다.

Access Token은 다르다. 어떤 자원 서버에 어떤 권한으로 접근할 수 있는지를 표현하는 *허가증*이다. `aud` 클레임에 자원 서버의 식별자가 박힌다. JWT일 수도 있고 opaque 문자열일 수도 있다. 사용자 신원을 표현하는 게 본업이 아니다.

**그래서 ID Token으로 API를 인가하면 안 된다.** 이게 바로 본 장의 함정 셋 중 하나(§7.4 함정 16)다. 어떤 개발자는 "ID Token도 JWT고, 거기에 `sub`가 있으니 API 인가에 그대로 쓰면 되겠지" 하고 헷갈린다. 그러면 ID Token이 자원 서버로 흘러간다. 자원 서버는 그 토큰이 자기 앞으로 발급된 게 아니라는 사실(`aud`가 자기가 아닌 것)을 검증해야 막아낼 수 있다. 검증을 게을리하면 *우리 client에게 신원을 증명한 토큰*이 *다른 서비스의 자원을 여는 키*로 쓰이는 사고가 난다. 보안 모델이 한 단어로 무너진다.

규칙은 단순하다. **사용자 식별 → ID Token. API 호출 → Access Token.** 둘이 같은 응답에 묶여 와도, 쓰임새는 별개로 두자.

## `OAuth2LoginAuthenticationFilter` 내부, 한 겹 더 벗기기

위에서 흐름을 그렸으니, 이제 그 핵심 필터의 일을 한 겹 더 벗겨보자. 이걸 알면 디버깅 속도가 달라진다.

`OAuth2LoginAuthenticationFilter`는 들어온 콜백 요청을 받자마자 `OAuth2LoginAuthenticationToken`이라는 임시 인증 토큰을 만든다. 미완성 인증 표시다. 이 토큰을 들고 `AuthenticationManager`에게 인증을 위임한다. 3장에서 본 익숙한 패턴이다.

이 인증 매니저 뒤에는 `OAuth2LoginAuthenticationProvider`가 자리 잡고 있다. 이 프로바이더가 진짜 일을 한다. 먼저 `OAuth2AuthorizationCodeAuthenticationProvider`를 통해 code↔token 교환을 수행한다. 교환의 결과로 `OAuth2AccessTokenResponse`가 돌아오는데, 거기 안에 access token과 (있다면) id token이 들어 있다.

id token이 있으면 흐름이 OIDC 쪽으로 갈라진다. `OidcAuthorizationCodeAuthenticationProvider`가 id token을 디코드한다. 디코드 자체는 `OidcIdTokenDecoderFactory`가 IdP별로 만든 `JwtDecoder`가 처리한다. 이 디코더가 JWKs를 조회해 서명을 검증하고, `iss`/`aud`/`exp`/`iat`/`nonce`를 검증한다. 검증을 통과하면 `OidcIdToken`이 손에 들어온다.

그 다음 차례는 `OidcUserService`다. 기본 구현은 `OidcUserService`(이름 그대로)인데, id token만으로 사용자 정보가 충분하면 그것만으로 `OidcUser`를 만들고, 부족하면 userinfo 엔드포인트를 한 번 더 호출해 추가 클레임을 가져온다. userinfo 호출은 access token을 Bearer로 들고 가서 친다. 이 단계까지 끝나면 우리 손에 `DefaultOidcUser`가 들어오고, 그게 `OAuth2LoginAuthenticationToken`의 principal로 들어가 인증이 성립한다.

이 흐름의 어디에 끼어들고 싶을 때가 있다. 가장 흔한 경우가 "사용자의 이메일을 받아서 우리 DB에 회원으로 등록하거나, 권한을 매핑하고 싶다"는 요구다. 그럴 때 우리가 갈아 끼울 곳은 `OidcUserService`다.

```java
@Bean
OidcUserService customOidcUserService(UserRepository users) {
    return new OidcUserService() {
        @Override
        public OidcUser loadUser(OidcUserRequest userRequest) {
            OidcUser delegate = super.loadUser(userRequest);
            String email = delegate.getEmail();
            var ourUser = users.findOrCreateByEmail(email);
            // 우리 DB의 권한을 ID 토큰 클레임 위에 더 얹는다
            var authorities = new HashSet<GrantedAuthority>(delegate.getAuthorities());
            ourUser.getRoles().forEach(r -> authorities.add(new SimpleGrantedAuthority("ROLE_" + r)));
            return new DefaultOidcUser(authorities, delegate.getIdToken(), delegate.getUserInfo());
        }
    };
}
```

그리고 체인에 연결한다.

```java
http.oauth2Login(o -> o.userInfoEndpoint(u -> u.oidcUserService(customOidcUserService)));
```

이 패턴이면 IdP로부터 받은 신원 정보 위에 우리 도메인의 권한을 얹을 수 있다. "IdP가 인증을 하고, 우리가 인가를 한다"는 깔끔한 책임 분리다. 권한 매핑이 한 곳에 모이니, 나중에 권한 규칙이 바뀌어도 손볼 곳이 명확하다.

## PKCE — 가로채도 못 바꾸게 하는 한 수

이제 PKCE 이야기를 하자. 이름은 `Proof Key for Code Exchange`인데, 한 줄로 표현하면 이렇다.

**공격자가 redirect URI를 가로채 인가 코드를 훔쳐도, 그 코드를 토큰으로 못 바꾸게 한다.**

원래 OAuth 2.0의 약한 고리가 이 redirect였다. 인가 코드는 짧은 시간만 살아 있지만, 그 짧은 사이에 모바일 앱의 커스텀 스킴이 다른 앱에 가로채지거나, SPA의 URL이 브라우저 히스토리에 남거나, 로컬 프록시가 캡처할 수 있었다. 코드만 손에 들어오면 공격자는 자기가 적절한 client_id를 갖고 있다면 그 코드를 토큰으로 교환할 수 있었다. 그래서 PKCE라는 추가 단계가 생겼다.

원리는 단순하다. 클라이언트(우리 서버 또는 SPA)는 인가 요청 *직전에* 랜덤 문자열 하나를 생성한다. 이걸 `code_verifier`라고 부른다. 그 문자열의 SHA-256 해시를 base64로 인코딩한 게 `code_challenge`다. 인가 요청 URL에 `code_challenge`와 `code_challenge_method=S256`을 함께 실어 IdP에 보낸다. IdP는 이 챌린지 값을 인가 코드와 묶어 자기 쪽에 잠시 저장해둔다.

나중에 우리가 토큰 엔드포인트로 코드를 교환하러 갈 때, 원본 `code_verifier`를 함께 보낸다. IdP는 받은 verifier를 해시해 자기가 저장해둔 챌린지와 비교한다. 일치해야 토큰을 내준다. 즉 *코드를 처음 만든 그 세션*만이 그 코드를 토큰으로 바꿀 수 있다. 가로챈 공격자에게는 코드만 있을 뿐 verifier가 없으니 손쓸 도리가 없다.

원래 PKCE는 *public client*(SPA, 모바일 앱처럼 client_secret을 못 숨기는 클라이언트)를 위한 보강책이었다. confidential client는 client_secret이 백채널에 안전히 살아 있으니 PKCE 없이도 충분하다고 여겨졌다.

그런데 RFC 9700(2025년 1월 발행된 OAuth 2.0 Security BCP)이 입장을 더 단호하게 정리했다. *모든 클라이언트가 PKCE를 써야 한다.* public이든 confidential이든 가리지 않는다. redirect 가로채기 공격은 client_secret이 있다고 사라지지 않기 때문이다. OAuth 2.1 draft도 이 입장을 그대로 흡수해 PKCE를 필수화했다.

Spring Security 7은 이 흐름에 동참한다. Authorization Server 쪽은 PKCE가 기본 활성화고, Client 쪽도 PKCE를 권장 default로 밀어둔다. 다만 confidential client에서는 명시적으로 PKCE를 켜주는 게 가장 안전하다. 이렇게 한다.

```java
@Bean
SecurityFilterChain web(HttpSecurity http,
                        ClientRegistrationRepository repo) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2Login(o -> o.authorizationEndpoint(
            ep -> ep.authorizationRequestResolver(pkceResolver(repo))))
        .build();
}

private DefaultOAuth2AuthorizationRequestResolver pkceResolver(
        ClientRegistrationRepository repo) {
    var resolver = new DefaultOAuth2AuthorizationRequestResolver(
        repo, "/oauth2/authorization");
    resolver.setAuthorizationRequestCustomizer(
        OAuth2AuthorizationRequestCustomizers.withPkce());
    return resolver;
}
```

`OAuth2AuthorizationRequestCustomizers.withPkce()` 이 한 줄이 인가 요청에 `code_challenge`를 끼워 넣는다. 6.x에서 올라온 코드를 점검할 때 이 줄이 누락돼 있다면, 명시적으로 다시 켜주는 편이 낫다. 7.0의 기본이 권장 ON이지만, 명시적으로 켜져 있는 코드가 6개월 뒤의 우리에게 친절하다.

## 7.0이 들고 온 신선한 변화들

이번 절은 7.0에서 새로 들어온 OAuth2 클라이언트 쪽 변화 둘을 묶어 보자.

### `@ClientRegistrationId` 타입 레벨 어노테이션

7.0 이전에는 OAuth2 클라이언트가 외부 API를 호출할 때 어떤 registration의 토큰을 써야 하는지를 메서드 인자에 `@RegisteredOAuth2AuthorizedClient("google")` 같은 식으로 끼워 넣었다. 한 클래스 안에서 메서드마다 동일한 registration이 반복되는 일이 잦았다. 7.0은 이걸 타입 레벨로 끌어올렸다.

```java
@ClientRegistrationId("github")
public interface GitHubClient {

    @GetExchange("/user")
    GitHubUser me();

    @GetExchange("/user/repos")
    List<Repo> myRepos();
}
```

클래스(여기선 인터페이스)에 한 번 박아두면 그 안의 모든 호출이 해당 registration의 access token을 자동으로 들고 간다. 이게 가능해진 배경이 다음 항목이다.

### OAuth2 Support for HTTP Service Clients

Spring Framework 6.x가 들고 온 `@HttpExchange` 인터페이스 클라이언트는 이미 우리에게 친숙하다. 인터페이스에 `@GetExchange`, `@PostExchange`를 박아두면 `WebClient`/`RestClient` 기반의 구현체가 알아서 만들어진다. 7.0의 Spring Security는 이 인터페이스 클라이언트가 OAuth2 흐름과 잘 어울리도록 한 단계 더 묶어준다.

`@ClientRegistrationId("github")`가 붙은 인터페이스 클라이언트는 호출 시점에 현재 사용자의 `OAuth2AuthorizedClient`를 찾아 `Authorization: Bearer ...` 헤더를 자동으로 끼워 넣는다. 우리가 토큰을 꺼내 헤더에 손으로 박을 일이 사라진다. 토큰이 만료되면 refresh token으로 자동 갱신까지 한다.

```java
@RestController
class DashboardController {
    private final GitHubClient github;

    @GetMapping("/me/repos")
    List<Repo> myRepos() {
        return github.myRepos(); // 토큰은 알아서 붙는다
    }
}
```

이 한 줄에 토큰의 수명 주기, 갱신, 헤더 주입이 다 들어 있다. 그만큼 우리 코드는 *비즈니스*만 남는다. 5장에서 자원 서버를 한 줄로 켰던 그 느낌이 클라이언트 쪽에도 도착한 셈이다.

### Dynamic Client Registration

또 한 가지, 7.0은 OAuth 2.0 Dynamic Client Registration Protocol을 지원한다. 멀티 테넌트 환경에서 새 IdP가 추가될 때마다 application.yml에 손으로 적어 재배포하는 일이 줄어든다. 코드에서 동적으로 client를 등록하고 등록 결과를 영속화할 수 있다. 일반적인 단일 IdP 시스템에서는 쓸 일이 별로 없지만, SaaS형 제품에서 고객사마다 자기 IdP를 붙이게 해야 한다면 이걸 떠올리자.

## RFC 9700이 권하는 일곱 가지, 7.0이 답하는 방식

OAuth 2.0 Security Best Current Practice가 2025년 1월에 RFC 9700으로 정식 발행됐다. 6749/6750/6819를 모두 업데이트한다. 권하는 일곱 가지를 7.0과 매핑해보자.

| RFC 9700 권고 | Spring Security 7의 대응 |
|---|---|
| 1. Authorization Code + PKCE를 *모든* 클라이언트가 사용한다 | Auth Server PKCE 기본 ON, Client는 `withPkce()` 명시 권장 |
| 2. Implicit grant 금지 | 7.0 client에서 제거 노선 |
| 3. Password grant 금지 | 7.0에서 완전 제거 |
| 4. Redirect URI는 *정확 매칭* | `ClientRegistration.redirectUri`는 처음부터 exact 등록 |
| 5. Sender-constrained 토큰 권장(mTLS, DPoP) | 7.0 DPoP 지원 (RFC 9449) |
| 6. Refresh Token은 회전 또는 sender-constrain | Authorization Server가 회전(rotate) 지원 |
| 7. Access Token을 쿼리스트링에 넣지 말 것 | 클라이언트 기본이 `Authorization: Bearer` 헤더 |

표 한 장이지만 의미는 묵직하다. *우리가 7.0의 기본값만 따라가도 BCP의 일곱 가지를 거의 다 만족한다.* 한두 가지(PKCE 명시화, redirect URI exact 등록)만 코드에서 챙기면 된다. 표준을 따라가려고 우리가 따로 노력할 일이 적다는 뜻이고, 이건 프레임워크가 우리에게 주는 가장 큰 선물 중 하나다.

OAuth 2.1 draft는 이 BCP의 핵심을 코어 스펙으로 흡수했다. 필수 PKCE, Implicit/ROPC 제거, exact redirect URI까지 모두 코어로 빨려 들어갔다. 즉 OAuth 2.1로 넘어가는 시점에는 위 표의 1~4번이 "권고"가 아니라 "스펙 그 자체"가 된다. 7.0은 이미 그 자리를 미리 비워두고 있다.

## 함정 셋, 미리 보자

이번 장의 함정 셋은 모두 *너무 사소해 보여서 지나치기 쉬운데, 막상 새면 보안 모델이 통째로 무너지는* 종류다. 하나씩 짚어보자.

### 함정 1. Redirect URI 와일드카드

"테스트 환경마다 호스트가 달라서 일일이 등록하기 번거롭다. 그냥 `https://*.example.com/login/oauth2/code/google`로 와일드카드 등록해두자." 이 한 줄의 편의가 *open redirect* 공격의 문을 연다.

공격 시나리오는 이렇다. 공격자가 `https://evil.example.com`을 자기 서버로 띄운다. `example.com`의 서브도메인 와일드카드가 허용되니, 공격자는 `redirect_uri=https://evil.example.com/login/oauth2/code/google`을 인가 요청에 끼워 IdP로 사용자를 보낸다. IdP는 등록된 패턴과 매칭되니 받아들이고, 코드를 `evil.example.com`으로 돌려보낸다. 공격자 손에 코드가 들어간다. 그 다음은 우리가 막 배운 PKCE가 그 코드를 토큰으로 못 바꾸게 막아주지만, 그렇다고 공격 표면을 열어두는 것 자체가 정당화되진 않는다.

해법은 단호하다. **redirect URI는 환경별로 정확 매칭으로 등록한다.** dev, staging, prod가 다르다면 IdP에 셋을 별도 client로 등록한다. RFC 9700도 그렇게 요구한다. 와일드카드는 그 자체로 BCP 위반이다.

### 함정 2. confidential client에서 PKCE 누락

이건 6.x에서 올라온 코드에서 흔히 만난다. 6.x 시절 confidential client 쪽 PKCE는 *선택*이었고, 일부 코드는 explicit하게 PKCE를 *끄고* 있었다("어차피 client_secret이 있는데 뭐"). 7.0으로 업그레이드해도 그 explicit한 비활성화는 그대로 살아 있다.

해법도 단순하다. 위에서 본 `OAuth2AuthorizationRequestCustomizers.withPkce()` 한 줄을 추가한다. 6.x에서 올라온 OAuth2 클라이언트 설정은 이 한 줄이 들어 있는지 반드시 확인하자. 잊지 말자.

### 함정 3. ID Token으로 API 인가

이건 앞서 비유로 박아뒀다. 여권으로 출입증을 흉내 내는 일이다. ID Token의 `aud`는 *우리 client_id*고, Access Token의 `aud`는 *자원 서버의 식별자*다. 둘은 발급 대상이 다르다. ID Token을 자원 서버로 보내는 시점에 자원 서버가 `aud` 검증을 하고 있다면 거절될 것이다. 검증을 안 하고 있다면? 그 자원 서버는 *우리가 받은 신원 증명*을 자기 자원의 열쇠로 받아들이는 셈이다. 이건 끔찍한 일이다.

규칙을 다시 못 박아두자. **API 호출에는 Access Token. 사용자 식별에는 ID Token.** 둘이 한 응답에 묶여 와도, 쓰임새가 섞이지 않게 한다. `OAuth2AuthorizedClient`에서 토큰을 꺼낼 때 `getAccessToken()`을 쓰지, `getIdToken()` 같은 걸 자원 호출에 쓰지 않는다. 자원 서버 쪽도 5장에서 본 `JwtAuthenticationConverter`에서 `aud` 검증을 빼먹지 말자.

## 두 체인이 만나는 곳

5장에서는 자원 서버 한 채널만 다뤘다. 이번 장은 클라이언트만 다뤘다. 그런데 현실은 둘이 한 시스템 안에 같이 사는 경우가 많다. 우리가 만든 웹 앱이 사용자에게는 OIDC로 로그인을 받고, 백엔드 API에는 JWT로 인증을 거는, 두 얼굴을 가진 시스템이다.

이걸 어떻게 분리할지는 2장에서 미리 그려뒀던 *두 개의 체인* 패턴을 떠올리면 답이 그려진다.

```java
@Bean @Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .csrf(CsrfConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .build();
}

@Bean @Order(2)
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2Login(Customizer.withDefaults())
        .build();
}
```

`/api/**` 는 자원 서버, 나머지는 OIDC 로그인. 같은 IdP를 바라봐도 좋고, IdP가 달라도 좋다. 두 체인은 같은 application.yml의 `spring.security.oauth2.client` 블록과 `spring.security.oauth2.resourceserver` 블록을 각각 본다. 한 줄짜리 issuer-uri가 양쪽에서 메타데이터를 끌어와 자동으로 와이어링한다.

웹 채널에서 로그인한 사용자가 SPA를 통해 우리 API를 호출할 때는, 보통 두 가지 패턴 중 하나를 쓴다. 하나는 *세션 기반*. 같은 도메인이라면 OIDC로 들어온 세션을 SPA가 그대로 쓰고, API는 세션을 인증 수단으로 받는다. 이때 API 체인에는 `oauth2ResourceServer` 대신 세션 인증을 그대로 사용한다. 다른 하나는 *Backend-for-Frontend(BFF)* 패턴. BFF가 OIDC로 토큰을 받아 보관하고, SPA에는 HttpOnly 쿠키만 노출하며, 백엔드 API 호출은 BFF가 access token을 붙여 대신 한다. 14장에서 이 BFF 패턴을 따로 다룬다.

지금 이 장에서 기억해둘 것은 단순하다. **OIDC 로그인 체인과 자원 서버 체인은 서로 독립이고, 같은 시스템에서 공존할 수 있다.** 각자 자기 토큰 모델을 쓰고, 우리는 두 채널을 명확히 분리해 설정한다. 한 체인 안에 둘을 우겨넣으려고 하면 갑자기 설정이 난감해진다.

## 마무리

이번 장에서 사용자가 누른 한 번의 "Sign in with Google" 뒤에 어떤 일이 벌어지는지 끝까지 따라가 봤다. `/oauth2/authorization/{id}`로 시작해 IdP를 거쳐 `/login/oauth2/code/{id}`로 돌아오는 여정, 그 사이에서 PKCE가 가로채기 공격을 어떻게 막는지, ID Token과 Access Token의 역할이 어떻게 다른지, 7.0이 들고 온 `@ClientRegistrationId`와 `@HttpExchange` 통합이 우리 코드를 얼마나 가볍게 만드는지, 그리고 RFC 9700이 권하는 일곱 가지 중 우리가 손수 챙길 게 사실 둘셋뿐이라는 사실까지 짚었다.

기억해두자. **표준의 기본값 위에 서면 우리가 따로 노력할 일이 적어진다.** 7.0의 OAuth2 클라이언트 기본은 그 자체가 RFC 9700과 OAuth 2.1의 방향이다. 우리가 명시적으로 PKCE를 켜고, redirect URI를 정확 매칭으로 등록하고, ID Token과 Access Token을 헷갈리지 않는다면, 그것만으로 보안 모델의 90%가 깔린다. 나머지 10%는 운영 디테일이다.

다음 장에서는 패스워드 너머의 인증으로 넘어간다. One-Time Token, Passkeys, 그리고 7.0이 1급으로 끌어올린 Multi-Factor Authentication까지. 이번 장에서 본 "외부 IdP가 인증을 대신해주는" 모델 위에, "그 IdP가 어떤 factor로 사용자를 확인하는가"라는 질문이 한 겹 더 얹힌다. 인증 모델의 깊이가 한 단계 더 들어간다.
