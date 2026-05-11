# 12장. Spring Security 테스팅 — `@WithMockUser`부터 OAuth2 mock까지

> **선행 필요:** 2장(필터 체인), 3장(컴포넌트 모델), 5장(JWT 자원 서버), 8장(인가), 11장(Reactive 보안). 본 챕터는 책 전반의 어휘 위에서 "그 모든 결정을 어떻게 회귀 안전망에 묶을 것인가"에 답한다.

운영에서 발견된 권한 버그를 떠올려 보자. "관리자 화면에 일반 사용자가 들어와 본 적이 없는 데이터를 한 번 클릭으로 다운로드해 갔다." 사후 조사에 들어가면 거의 매번 같은 패턴이 나온다. **`@PreAuthorize`를 단 줄 알았는데 안 달려 있었다**, **`@EnableMethodSecurity`가 아니라 옛 `@EnableGlobalMethodSecurity`가 남아 있어 메서드 단위 인가가 통째로 무력화돼 있었다**, **`csrf().disable()`을 API용 체인에서만 끄려 했는데 전역에 적용돼 폼 로그인이 깨졌다**. 운영에서 발견되기 전까지 아무도 몰랐다. 단위 테스트도 통합 테스트도 인증된 사용자로 호출해 본 적이 없으니 당연하다.

보안 규칙은 다른 비즈니스 로직과 결정적으로 다르다. **한 번 잘못 짜면 운영에서야 발견된다**. 평소엔 잘 돌아가다가, 권한 없는 사용자가 어쩌다 그 경로를 밟는 순간에만 깨진다. 그래서 테스트가 더 중요하다. 정확히 말하면, **인증된 사용자/익명 사용자/권한 없는 사용자/만료된 토큰 사용자**를 각각 만들어 같은 엔드포인트를 호출했을 때 시스템이 어떻게 반응하는지를 코드로 박아 두는 일이 더 중요하다.

그렇다면 어떻게 해야 할까? `MockMvc`로 컨트롤러를 부르면 되지 않을까? 그렇다. 하지만 그것만으론 모자란다. 보안 필터 체인은 컨트롤러보다 앞에 있고, `SecurityContext`는 스레드 로컬에 묶여 있으며, OAuth2 로그인은 외부 IdP와 왕복한다. 이 세 가지를 어떻게 흉내 낼지가 12장의 주제다. 한 절씩 짚어 보자.

## 12.1 의존성과 기본 좌표 — `spring-security-test`는 어디에 사는가

먼저 의존성부터 짚는다. `spring-boot-starter-security`를 넣고 `spring-boot-starter-test`까지 더한 프로젝트라면 십중팔구 `spring-security-test`는 이미 클래스패스에 있다. Spring Boot 4의 BOM이 자동으로 끌고 들어오기 때문이다. 그래도 한 번은 확인해 두자.

```kotlin
// build.gradle.kts
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-security")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.security:spring-security-test")
}
```

`spring-security-test`가 제공하는 것은 크게 네 묶음이다.

1. **`@WithMockUser`·`@WithUserDetails`·`@WithSecurityContext`** — 어노테이션 한 줄로 `SecurityContext`를 채워 주는 도구
2. **`SecurityMockMvcRequestPostProcessors`** — `MockMvc` 요청에 인증 정보를 주입하는 후처리기(`csrf()`, `user()`, `jwt()`, `oauth2Login()` 등)
3. **`SecurityMockMvcResultMatchers`·`SecurityMockMvcConfigurers`** — `authenticated()`/`unauthenticated()` 결과 매처와 필터 등록
4. **`SecurityMockServerConfigurers`** — `WebTestClient`(Reactive) 쪽의 `mutateWith(...)` 변환기

이 네 묶음의 이름 차이가 처음엔 헷갈린다. **Servlet 쪽은 `MockMvc`, Reactive 쪽은 `WebTestClient`** 라고 외워 두자. 그리고 같은 개념(가짜 사용자, mock JWT, mock OAuth2 로그인)이 두 쪽에 각각 따로 산다고 기억해 두면 마찰이 줄어든다.

마지막으로 한 가지 좌표. Spring Security 7.0이 테스트 API를 깬 적은 없다. 5.x·6.x에서 쓰던 `@WithMockUser`, `csrf()`, `jwt()` 호출은 7.0에서도 그대로 유효하다. **다만 7.0에서 Lambda DSL이 강제되고 `requireExplicitSave(true)`가 기본 권고가 되면서, 테스트가 검증해야 할 동작 자체가 미묘하게 바뀌었다.** 이 점은 12.10에서 따로 다룬다.

## 12.2 `@WithMockUser` — 가장 쉬운 인증 주입

가장 자주 쓰는 도구부터 살펴보자. `@WithMockUser`는 테스트 메서드를 호출하기 전에 `SecurityContextHolder`에 가짜 `Authentication`을 꽂아 둔다. 별다른 설정 없이 "이 테스트는 ROLE_USER가 들어왔다고 치자"라고 한 줄로 선언할 수 있다.

```java
@WebMvcTest(OrderController.class)
@Import(SecurityConfig.class)
class OrderControllerTest {

    @Autowired MockMvc mvc;

    @Test
    @WithMockUser(username = "alice", roles = "USER")
    void 일반_사용자는_자기_주문_목록을_조회할_수_있다() throws Exception {
        mvc.perform(get("/orders"))
            .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(username = "bob", roles = "ADMIN")
    void 관리자는_모든_주문을_조회할_수_있다() throws Exception {
        mvc.perform(get("/orders/all"))
            .andExpect(status().isOk());
    }

    @Test
    void 익명_사용자는_접근하면_302로_로그인_페이지로_리다이렉트된다() throws Exception {
        mvc.perform(get("/orders"))
            .andExpect(status().is3xxRedirection())
            .andExpect(redirectedUrlPattern("**/login"));
    }
}
```

`@WithMockUser`가 채워 주는 기본값을 한 번 분명히 짚고 가자. `username`은 `"user"`, `password`는 `"password"`, `roles`는 `{"USER"}`다. `roles`를 지정하면 자동으로 `ROLE_` 접두사가 붙는다. 즉 `roles = "ADMIN"`은 `ROLE_ADMIN` 권한으로 들어간다. **접두사 없이 직접 권한 이름을 박고 싶다면 `authorities = {"SCOPE_orders.read", "factor:password"}` 쪽을 써야 한다**. 이 둘을 헷갈리면 `hasAuthority("ADMIN")` 같은 표현식이 통과해 버려서 "테스트는 초록불인데 운영은 빨갛다" 같은 찜찜한 사태가 벌어진다.

```java
// roles와 authorities는 의미가 다르다. 한 번 짚어 두자.
@WithMockUser(roles = "ADMIN")              // -> ROLE_ADMIN
@WithMockUser(authorities = "ADMIN")        // -> ADMIN (ROLE_ 안 붙음)
@WithMockUser(authorities = {"SCOPE_orders.read", "factor:password"})
```

`@WithMockUser`는 메서드뿐 아니라 클래스에도 달 수 있다. 클래스 전체가 같은 사용자로 돌아가야 하는 경우엔 클래스 레벨에 한 번만 달고, 예외만 메서드 레벨로 덮어쓰는 편이 낫다.

```java
@WebMvcTest(AdminController.class)
@Import(SecurityConfig.class)
@WithMockUser(roles = "ADMIN")                 // 클래스 전체 기본값
class AdminControllerTest {

    @Test
    void 관리자는_사용자_목록을_본다() { /* ROLE_ADMIN로 동작 */ }

    @Test
    @WithMockUser(roles = "USER")              // 이 메서드만 덮어씀
    void 일반_사용자는_관리자_화면_접근_시_403이다() throws Exception {
        mvc.perform(get("/admin/users"))
            .andExpect(status().isForbidden());
    }
}
```

### `@WithMockUser`로 통과했는데 운영에선 깨졌다 — 함정 정리

다음 함정은 한 번쯤은 다 맞아 본다. 같이 정리해 두자.

**함정 1: 운영의 `UserDetailsService`를 거치지 않는다는 사실을 잊는다.** `@WithMockUser`는 메모리상에서 `org.springframework.security.core.userdetails.User` 객체를 만들어 꽂는다. 운영에서 사용자가 로그인할 때 거치는 `UserDetailsService.loadUserByUsername(...)`은 호출되지 않는다. 그래서 운영에선 `loadUserByUsername`이 throw하는 예외 처리·계정 잠금 검사·권한 동적 계산이 전부 우회된다. **인증 자체를 검증하고 싶다면 `@WithMockUser`가 아니라 `@WithUserDetails`를 쓰는 편이 낫다**(다음 절).

**함정 2: 권한이 정적이다.** `@WithMockUser`로 주입한 권한은 그 테스트가 끝날 때까지 변하지 않는다. 운영 코드에서 "방금 MFA를 통과하면 권한이 추가된다" 류 동적 권한 부여가 있다면 그 흐름은 `@WithMockUser`로 검증되지 않는다. 이런 경우엔 `@WithSecurityContext`로 직접 컨텍스트를 구성하거나, 실제 인증 흐름을 태우는 통합 테스트로 가야 한다.

**함정 3: `password` 필드를 검증하지 않는다.** `@WithMockUser(password = "secret")`을 줘도 그 비밀번호로 인증되는 게 아니다. 그저 `User` 객체의 필드에 그 값이 박힐 뿐이다. `PasswordEncoder` 검증을 우회한다는 사실을 기억해 두자.

## 12.3 `@WithUserDetails` — 실제 `UserDetailsService`를 거친다

`@WithMockUser`의 함정 1을 피하려면 `@WithUserDetails`를 쓰면 된다. 이름 그대로다. 빈으로 등록된 `UserDetailsService`(또는 명시적으로 지정한 빈)의 `loadUserByUsername(...)`을 실제로 호출해서, 그 결과로 `SecurityContext`를 채운다.

```java
@SpringBootTest
@AutoConfigureMockMvc
class OrderControllerIntegrationTest {

    @Autowired MockMvc mvc;

    @Test
    @WithUserDetails("alice@example.com")
    void DB에_등록된_사용자로_주문을_조회한다() throws Exception {
        mvc.perform(get("/orders"))
            .andExpect(status().isOk());
    }

    @Test
    @WithUserDetails(value = "bob", userDetailsServiceBeanName = "adminUserDetailsService")
    void 관리자_전용_UserDetailsService를_사용한다() throws Exception {
        mvc.perform(get("/admin/users"))
            .andExpect(status().isOk());
    }
}
```

`@WithUserDetails`는 **실제 사용자 데이터를 거치니까 운영에 더 가깝다**. DB의 `users` 테이블에 시드를 박아 두고 그 사용자로 로그인하는 시나리오를 통합 테스트로 충분히 검증할 수 있다. 다만 트레이드오프가 있다. 빠르지 않다. `@WebMvcTest` 같은 슬라이스 테스트에선 `UserDetailsService` 빈이 없을 수 있어서 그대로 못 쓰는 경우가 흔하다. 일반적으로는 **단위 슬라이스에선 `@WithMockUser`, 통합 슬라이스에선 `@WithUserDetails`** 로 나누는 편이 깔끔하다.

## 12.4 `@WithSecurityContext` — 커스텀 컨텍스트가 필요할 때

`@WithMockUser`로도 `@WithUserDetails`로도 못 만드는 컨텍스트가 있다. 대표적으로 OAuth2 자원 서버에서 받은 `JwtAuthenticationToken`이나, 7.0의 MFA 통과 흐름에서 만들어지는 다중 factor 권한 묶음 같은 경우다. 이럴 땐 `@WithSecurityContext` 메타 어노테이션을 만들어 두자.

```java
// 1) 어노테이션 정의
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@WithSecurityContext(factory = WithMockJwtSecurityContextFactory.class)
public @interface WithMockJwt {
    String subject() default "alice";
    String[] scopes() default {"orders.read"};
    String[] factors() default {"factor:password"};
}

// 2) 컨텍스트 팩토리 구현
public class WithMockJwtSecurityContextFactory
        implements WithSecurityContextFactory<WithMockJwt> {

    @Override
    public SecurityContext createSecurityContext(WithMockJwt anno) {
        Jwt jwt = Jwt.withTokenValue("mock-token")
            .header("alg", "none")
            .subject(anno.subject())
            .claim("scope", String.join(" ", anno.scopes()))
            .build();

        Collection<GrantedAuthority> authorities = new ArrayList<>();
        for (String scope : anno.scopes()) {
            authorities.add(new SimpleGrantedAuthority("SCOPE_" + scope));
        }
        for (String factor : anno.factors()) {
            authorities.add(new SimpleGrantedAuthority(factor));
        }

        JwtAuthenticationToken auth = new JwtAuthenticationToken(jwt, authorities);
        SecurityContext ctx = SecurityContextHolder.createEmptyContext();
        ctx.setAuthentication(auth);
        return ctx;
    }
}

// 3) 테스트에서 사용
@Test
@WithMockJwt(scopes = {"orders.read", "orders.write"})
void JWT_토큰으로_주문을_생성한다() throws Exception {
    mvc.perform(post("/orders").contentType(APPLICATION_JSON).content("{}").with(csrf()))
        .andExpect(status().isCreated());
}
```

이 패턴이 한 번 만들어 두면 두고두고 편하다. MFA factor 조합 검증, 다중 issuer 시나리오, 커스텀 `Authentication` 타입을 쓰는 경우에 특히 그렇다. 팀 단위로 공용 테스트 유틸 모듈에 빼 두자.

## 12.5 `SecurityMockMvcRequestPostProcessors` — 요청 한 줄에 인증 주입

`@WithMockUser`가 메서드 단위로 컨텍스트를 깔아 둔다면, `SecurityMockMvcRequestPostProcessors`는 **요청 한 번 단위로 인증을 갈아 끼울 수 있게** 해 준다. `MockMvc.perform(...)` 체인 안에 `.with(...)`로 끼우는 방식이다. 어노테이션과 어느 쪽이 좋은가? 같은 메서드 안에서 두 사용자를 비교해야 할 때, 또는 어노테이션이 안 먹는 파라미터화 테스트에서 후처리기 쪽이 훨씬 유연하다.

```java
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;

@Test
void 같은_엔드포인트에_두_사용자가_다르게_반응한다() throws Exception {
    // alice는 USER — 자기 주문만 본다
    mvc.perform(get("/orders/42").with(user("alice").roles("USER")))
        .andExpect(status().isForbidden());

    // admin은 ADMIN — 모든 주문 본다
    mvc.perform(get("/orders/42").with(user("admin").roles("ADMIN")))
        .andExpect(status().isOk());
}
```

자주 쓰는 후처리기를 한자리에 모아 두자.

| 후처리기 | 의미 |
|----------|------|
| `user("alice")` | 폼/Basic 사용자처럼 `UsernamePasswordAuthenticationToken` 주입 |
| `user("alice").roles("ADMIN")` | 권한 명시 |
| `user("alice").authorities(new SimpleGrantedAuthority("SCOPE_x"))` | 접두사 없는 권한 |
| `anonymous()` | 익명 사용자로 강제 |
| `httpBasic("alice", "pw")` | `Authorization: Basic ...` 헤더 부착 |
| `csrf()` | CSRF 토큰 동봉 |
| `csrf().asHeader()` | 토큰을 폼이 아닌 `X-CSRF-TOKEN` 헤더로 |
| `jwt()` | mock `JwtAuthenticationToken` 주입 (자원 서버) |
| `opaqueToken()` | mock opaque 토큰 인증 |
| `oauth2Login()` | mock OAuth2 로그인 사용자 |
| `oidcLogin()` | mock OIDC 로그인 사용자 |
| `oauth2Client("registrationId")` | `OAuth2AuthorizedClient` 주입 (HTTP 클라이언트가 access token 자동 첨부하는 흐름 검증) |

이 중에서 `csrf()`는 가장 자주 잊는다. 따로 절 하나를 빼서 다루자(12.7).

## 12.6 `jwt()`·`opaqueToken()` — 자원 서버 시나리오 mock

5장에서 `oauth2ResourceServer(o -> o.jwt(...))`로 자원 서버를 구성했다. 실제 운영에서는 IdP에서 발급된 JWT를 `Authorization: Bearer ...`로 받는다. 테스트할 때 매번 진짜 IdP를 띄울 순 없다. `jwt()` 후처리기가 이 자리를 채워 준다.

```java
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;

@Test
void 자원_서버는_SCOPE_orders_read_가_있을_때만_읽기를_허용한다() throws Exception {
    mvc.perform(get("/api/orders")
            .with(jwt().jwt(jwt -> jwt
                .subject("alice")
                .claim("scope", "orders.read"))))
        .andExpect(status().isOk());

    mvc.perform(get("/api/orders")
            .with(jwt().jwt(jwt -> jwt
                .subject("eve")
                .claim("scope", "profile"))))
        .andExpect(status().isForbidden());
}

@Test
void JWT의_권한을_커스텀_컨버터로_매핑하는_경우에도_확인한다() throws Exception {
    mvc.perform(get("/api/admin")
            .with(jwt()
                .jwt(jwt -> jwt.subject("admin").claim("roles", List.of("ADMIN")))
                .authorities(new SimpleGrantedAuthority("ROLE_ADMIN"))))
        .andExpect(status().isOk());
}
```

`jwt()`의 기본 권한 매핑이 운영의 `JwtAuthenticationConverter`와 달라 보일 때가 있다. 기본적으로 `scope`/`scp` 클레임을 `SCOPE_*`로 매핑해 주는 것까지는 같다. 그런데 커스텀 컨버터로 `roles` 클레임을 `ROLE_*`로 매핑하고 있다면, 테스트에서도 `.authorities(...)`로 그 권한을 명시해 주거나 실제 컨버터 빈을 통과시켜야 한다. **이 정렬을 흘리면 단위 테스트는 통과하는데 운영에선 403이 떨어진다**. 한 번 데이고 나면 잊지 않는다.

opaque 토큰 자원 서버도 비슷하다. `opaqueToken()` 후처리기가 introspection 응답을 흉내 낸다.

```java
@Test
void opaque_토큰_시나리오() throws Exception {
    mvc.perform(get("/api/orders")
            .with(opaqueToken()
                .principal(new DefaultOAuth2AuthenticatedPrincipal(
                    "alice",
                    Map.of("scope", "orders.read", "active", true),
                    AuthorityUtils.createAuthorityList("SCOPE_orders.read")))))
        .andExpect(status().isOk());
}
```

## 12.7 `csrf()` — 빠뜨리면 무조건 403

POST/PUT/DELETE/PATCH 메서드를 테스트하면서 `csrf()`를 안 붙이면 어김없이 403이 떨어진다. 그리고 그 응답 본문은 친절하지 않다. `Invalid CSRF Token`이 떨어지면 그나마 다행이고, 그냥 403만 나올 때도 있다. 처음 보는 사람은 "권한이 없다는 건가? 사용자 주입이 잘못된 건가?"라고 한참 헤매게 된다. 그 시간을 줄이자.

```java
@Test
@WithMockUser
void 주문_생성은_CSRF_토큰이_있어야_한다() throws Exception {
    // 잘못된 예 — 403이 떨어진다
    mvc.perform(post("/orders").contentType(APPLICATION_JSON).content("{}"))
        .andExpect(status().isForbidden());

    // 옳은 예 — csrf()를 동봉한다
    mvc.perform(post("/orders").contentType(APPLICATION_JSON).content("{}").with(csrf()))
        .andExpect(status().isCreated());
}
```

CSRF가 **켜져 있는 동작도 테스트해야 한다**는 점이 의외로 자주 빠진다. "운영에서 CSRF가 안 켜진 줄 모르고 있다가 6개월 뒤 침투 테스트에서 발견" 같은 일이 일어난다. `csrf()` 없이 `.andExpect(status().isForbidden())`을 만드는 테스트도 한 개쯤 박아 두자. CSRF 보호가 실수로 꺼지는 일을 회귀 테스트가 잡아 준다.

```java
@Test
@WithMockUser
void CSRF_보호가_꺼지지_않았는지_회귀_테스트로_확인한다() throws Exception {
    mvc.perform(post("/orders").contentType(APPLICATION_JSON).content("{}"))
        .andExpect(status().isForbidden())
        .andExpect(content().string(containsString("CSRF")));
}
```

7.0에서 SPA용으로 추가된 `http.csrf(CsrfConfigurer::spa)` 단축도 테스트로 묶을 수 있다. CookieCsrfTokenRepository 기반으로 `XSRF-TOKEN` 쿠키와 `X-XSRF-TOKEN` 헤더가 짝지어 동작하는지 검증하면 된다.

```java
@Test
void SPA_모드의_CSRF는_쿠키_헤더_왕복이_정상이다() throws Exception {
    // 1) GET으로 토큰 쿠키 발급
    MvcResult r = mvc.perform(get("/api/me").with(user("alice")))
        .andReturn();
    Cookie csrf = r.getResponse().getCookie("XSRF-TOKEN");
    assertThat(csrf).isNotNull();

    // 2) POST에 헤더로 토큰을 넣어 보낸다
    mvc.perform(post("/api/orders")
            .with(user("alice"))
            .cookie(csrf)
            .header("X-XSRF-TOKEN", csrf.getValue())
            .contentType(APPLICATION_JSON).content("{}"))
        .andExpect(status().isCreated());
}
```

## 12.8 `oauth2Login()`·`oidcLogin()` — OAuth2 클라이언트 시나리오

6장에서 외부 IdP(Google/Keycloak)에 로그인을 위임하는 흐름을 다뤘다. 그 흐름을 어떻게 테스트할까? IdP 왕복을 실제로 태우려면 컨테이너로 Keycloak을 띄워야 한다. 단위 슬라이스에선 그게 부담스럽다. `oauth2Login()`/`oidcLogin()` 후처리기가 그 자리에서 "이 사용자는 IdP를 거쳐 로그인된 상태"라고 흉내 내 준다.

```java
@Test
void OIDC_로그인_사용자는_프로필_화면에_접근한다() throws Exception {
    mvc.perform(get("/profile")
            .with(oidcLogin()
                .idToken(t -> t.subject("alice").claim("email", "alice@example.com"))
                .authorities(new SimpleGrantedAuthority("ROLE_USER"))))
        .andExpect(status().isOk())
        .andExpect(content().string(containsString("alice@example.com")));
}

@Test
void OAuth2_로그인_사용자는_OIDC_id_token이_없어도_된다() throws Exception {
    mvc.perform(get("/dashboard")
            .with(oauth2Login()
                .attributes(a -> a.put("login", "alice"))
                .authorities(new SimpleGrantedAuthority("ROLE_USER"))))
        .andExpect(status().isOk());
}
```

서비스 코드가 access token으로 외부 API를 호출하는 흐름은 또 다르다. 6장에서 본 `@HttpExchange` + `@ClientRegistrationId`로 access token 자동 주입하는 코드를 테스트하려면 `oauth2Client(...)`로 `OAuth2AuthorizedClient`를 미리 깔아 둬야 한다.

```java
@Test
void HttpExchange는_등록된_AuthorizedClient의_access_token을_자동_첨부한다() throws Exception {
    mvc.perform(get("/me/external-profile")
            .with(oauth2Login().authorities(new SimpleGrantedAuthority("ROLE_USER")))
            .with(oauth2Client("keycloak")
                .accessToken(new OAuth2AccessToken(
                    OAuth2AccessToken.TokenType.BEARER,
                    "mocked-access-token",
                    Instant.now(), Instant.now().plusSeconds(300)))))
        .andExpect(status().isOk());
}
```

그래도 어디까지나 mock이다. 진짜 IdP의 거동(예: `nonce` 불일치, JWKs 만료, refresh 회전)이 의심된다면 mock으로는 못 잡는다. **WireMock + `@AutoConfigureWireMock`** 으로 가짜 IdP를 띄우거나 Testcontainers로 Keycloak을 띄워야 한다. 이 경계는 12.13에서 다시 짚는다.

## 12.9 `authenticated()`·`unauthenticated()` — 결과 매처

요청을 검증할 때 응답 상태 코드만 보는 것으론 부족할 때가 있다. "이 요청 후에 정말 인증된 상태가 됐는지"를 결과 단계에서 확인하고 싶다. `SecurityMockMvcResultMatchers`가 그 자리에 있다.

```java
import static org.springframework.security.test.web.servlet.response.SecurityMockMvcResultMatchers.*;

@Test
void 로그인_성공_시_인증_상태가_된다() throws Exception {
    mvc.perform(formLogin("/login").user("alice").password("password"))
        .andExpect(authenticated().withUsername("alice").withRoles("USER"));
}

@Test
void 로그인_실패_시_인증되지_않은_상태가_유지된다() throws Exception {
    mvc.perform(formLogin("/login").user("alice").password("wrong"))
        .andExpect(unauthenticated());
}

@Test
void 로그아웃_후_보호된_자원_접근은_익명_상태다() throws Exception {
    mvc.perform(logout())
        .andExpect(unauthenticated());
}
```

`formLogin()`과 `logout()`은 `SecurityMockMvcRequestBuilders`에 있는 헬퍼다. 폼 로그인의 기본 엔드포인트(`/login`, `/logout`)와 파라미터(`username`/`password`)를 알아서 채워 준다. 커스텀 로그인 URL을 쓰면 `formLogin("/custom/login")`처럼 명시해 주자.

## 12.10 `requireExplicitSave(true)` 환경에서의 컨텍스트 저장 검증

7.0의 기본 권고가 `securityContext(s -> s.requireExplicitSave(true))`로 바뀌었다. 그러면서 한 가지 미묘한 변화가 생긴다. **`SecurityContext`가 자동으로 세션에 저장되지 않는다는 점**이다. 명시적으로 `SecurityContextHolderStrategy.getContext()`를 받아 `SecurityContextRepository.saveContext(...)`로 저장해야 한다. Spring Security가 제공하는 필터·표준 흐름은 이미 그렇게 하지만, 직접 작성한 커스텀 필터에서 `SecurityContextHolder.setContext(...)`만 호출해 두면 세션에 저장되지 않아 다음 요청에서 익명이 된다.

이 회귀를 테스트로 잡으려면 두 번 요청해 보면 된다.

```java
@Test
void 커스텀_인증_필터를_통과한_사용자는_다음_요청에서도_인증_상태다() throws Exception {
    // 1) 인증을 만들어 주는 첫 요청 — 세션 쿠키를 받는다
    MvcResult r = mvc.perform(post("/internal/login").with(csrf())
            .param("user", "alice"))
        .andExpect(status().isOk())
        .andExpect(authenticated().withUsername("alice"))
        .andReturn();
    MockHttpSession session = (MockHttpSession) r.getRequest().getSession();

    // 2) 같은 세션으로 두 번째 요청 — 여전히 인증 상태여야 한다
    mvc.perform(get("/me").session(session))
        .andExpect(status().isOk())
        .andExpect(authenticated().withUsername("alice"));
}
```

두 번째 요청에서 401/익명이 떨어지면 거의 확실히 첫 요청에서 `SecurityContext`를 세션에 저장하지 못한 것이다. 7.0 마이그레이션 후 운영 트래픽에서 "방금 로그인했는데 한 번 더 누르면 로그인 화면" 사고가 종종 보고된다. 위 두 줄짜리 회귀 테스트가 그걸 사전에 잡아 준다.

## 12.11 Reactive 보안 테스트 — `WebTestClient`와 `mutateWith`

11장에서 다룬 WebFlux 보안은 테스트 도구가 완전히 다르다. `MockMvc`를 못 쓴다. 대신 `WebTestClient`가 있고, 인증 주입은 `SecurityMockServerConfigurers`의 `mockUser()`/`mockJwt()`/`mockOAuth2Login()`을 `.mutateWith(...)`로 끼우는 방식이다.

```java
import static org.springframework.security.test.web.reactive.server.SecurityMockServerConfigurers.*;

@SpringBootTest
@AutoConfigureWebTestClient
class ReactiveOrderHandlerTest {

    @Autowired WebTestClient client;

    @Test
    void 인증된_사용자는_주문_목록을_본다() {
        client.mutateWith(mockUser("alice").roles("USER"))
            .get().uri("/orders")
            .exchange()
            .expectStatus().isOk();
    }

    @Test
    void JWT_자원_서버_시나리오() {
        client.mutateWith(mockJwt()
                .jwt(j -> j.subject("alice").claim("scope", "orders.read")))
            .get().uri("/api/orders")
            .exchange()
            .expectStatus().isOk();
    }

    @Test
    void 권한_부족은_403이다() {
        client.mutateWith(mockUser("alice").roles("USER"))
            .get().uri("/admin/users")
            .exchange()
            .expectStatus().isForbidden();
    }

    @Test
    void OIDC_로그인_사용자_시나리오() {
        client.mutateWith(mockOidcLogin()
                .idToken(t -> t.subject("alice").claim("email", "alice@example.com")))
            .get().uri("/profile")
            .exchange()
            .expectStatus().isOk();
    }
}
```

CSRF도 `SecurityMockServerConfigurers.csrf()`로 동봉할 수 있다.

```java
@Test
void Reactive에서_POST는_CSRF_토큰이_필요하다() {
    client.mutateWith(mockUser("alice"))
        .mutateWith(csrf())
        .post().uri("/orders")
        .bodyValue(Map.of())
        .exchange()
        .expectStatus().isCreated();
}
```

핵심 감각 한 가지를 챙겨 두자. **Servlet 쪽과 이름이 비슷하지만 API가 다르다.** `MockMvc.with(jwt(...))`와 `WebTestClient.mutateWith(mockJwt(...))`가 짝이다. `csrf()`는 양쪽에 다 있지만 import 경로가 다르다. IDE의 자동 import에 한 번 데이고 나면 잊지 않는다.

## 12.12 Method Security 테스트 — `@PreAuthorize`의 단위 검증

8장에서 본 `@PreAuthorize` 같은 메서드 단위 인가는 어떻게 테스트해야 할까? 흥미로운 트레이드오프가 있다. **`@PreAuthorize`는 Spring AOP 프록시로 동작한다**. 그래서 `new OrderService()`로 직접 만들어 메서드를 호출하면 인가가 안 걸린다. 빈으로 등록해 컨테이너에서 꺼내 써야 인가가 동작한다.

```java
@SpringBootTest
class OrderServiceMethodSecurityTest {

    @Autowired OrderService service;

    @Test
    @WithMockUser(roles = "USER")
    void USER는_자기_주문만_조회한다() {
        Order o = service.findOne(42L, "alice");
        assertThat(o).isNotNull();
    }

    @Test
    @WithMockUser(username = "eve", roles = "USER")
    void 다른_사용자_주문_조회는_AccessDeniedException이다() {
        assertThatThrownBy(() -> service.findOne(42L, "alice"))
            .isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithAnonymousUser
    void 익명_사용자_호출은_AuthenticationCredentialsNotFoundException이다() {
        assertThatThrownBy(() -> service.findOne(42L, "alice"))
            .isInstanceOf(AuthenticationCredentialsNotFoundException.class);
    }
}
```

이 테스트가 동작하려면 `@EnableMethodSecurity`가 설정 클래스에 달려 있어야 한다. **여기서 가장 흔한 함정은 `@WebMvcTest`로 슬라이스 테스트를 짰는데 메서드 보안이 동작하지 않아 모든 테스트가 초록불이 되는 경우다.** `@WebMvcTest`는 컨트롤러 레이어만 로드하고 서비스 빈은 mock으로 채운다. 그래서 `@PreAuthorize`가 붙은 실제 서비스가 컨테이너에 없다. **메서드 보안 검증은 `@SpringBootTest` 또는 `@SpringBootTest` 슬라이스를 쓰자**. 적어도 `@Import(SecurityConfig.class)`와 `@Import(OrderService.class)`로 명시적으로 끌어와야 한다.

`@PreAuthorize`의 SpEL이 복잡해질수록 단위 테스트가 점점 어려워진다. 8장에서 한 번 짚었지만, "SpEL에 너무 많은 로직을 넣지 말자"는 권고는 테스트 가능성 측면에서도 살아 있다. **SpEL에서 분기가 둘을 넘기 시작하면 서비스 메서드 안에서 `AuthorizationManager`를 직접 호출하는 패턴으로 바꾸는 편이 낫다**. 그래야 단위 테스트로 분기마다 검증할 수 있다.

## 12.13 테스트 슬라이스 — `@WebMvcTest` vs `@SpringBootTest`

지금까지 본 예제에서 두 어노테이션을 섞어 썼다. 정리해 두자.

**`@WebMvcTest`** — 웹 레이어만 로드한다. `MockMvc`를 자동 구성하고 컨트롤러·`ControllerAdvice`·`@JsonComponent`만 끌어온다. **`@Configuration`은 끌어오지 않는다**. 즉 `SecurityConfig`가 자동으로 적용되지 않는다. 이게 가장 큰 함정이다.

해법은 둘이다. 첫째, `@Import(SecurityConfig.class)`로 명시적으로 가져온다. 둘째, `excludeAutoConfiguration` 같은 옵션을 쓰지 말고 Spring Boot의 자동 구성을 기본대로 둬서 `SecurityAutoConfiguration`이 일하게 둔다. 일반적으로는 첫 번째가 명시적이라 권장된다.

```java
@WebMvcTest(OrderController.class)
@Import(SecurityConfig.class)           // ← 이게 없으면 보안이 안 걸린다
class OrderControllerSliceTest {
    // ...
}
```

이걸 빼먹으면 모든 엔드포인트가 익명으로 통과해 버려서 "테스트는 다 초록불, 운영은 다 401"이 된다. 끔찍한 일이다.

**`@SpringBootTest`** — 전체 컨텍스트를 로드한다. 보안 설정·서비스·리포지토리 모두 실제 빈으로 올라온다. 데이터베이스가 필요하면 `@AutoConfigureTestDatabase`나 Testcontainers로 띄운다. 느리지만 운영에 가장 가깝다.

권장 조합은 이렇다.

| 시나리오 | 슬라이스 | 사용자 주입 |
|----------|----------|-------------|
| 컨트롤러 인가 매핑(`hasRole` 등) | `@WebMvcTest` + `@Import(SecurityConfig)` | `@WithMockUser` 또는 `.with(user(...))` |
| `@PreAuthorize` 메서드 보안 | `@SpringBootTest` 또는 슬라이스 + 서비스 import | `@WithMockUser`/`@WithUserDetails` |
| 자원 서버 JWT 검증 | `@SpringBootTest` | `.with(jwt(...))` |
| OAuth2 Client 로그인 흐름 | `@SpringBootTest` | `.with(oauth2Login())`, IdP 흉내는 WireMock |
| 통합 시나리오(로그인 → 권한 → 로그아웃) | `@SpringBootTest` + 실제 DB | `formLogin()`/`logout()` + `authenticated()`/`unauthenticated()` |

### 어디까지 mock하고, 어디부터는 컨테이너로 가야 하는가

`oauth2Login()`/`jwt()`/`opaqueToken()` 후처리기는 **인증된 상태를 흉내 낸다**. 그 상태를 만드는 과정(IdP 왕복, JWKs 다운로드, 토큰 서명 검증)은 흉내 내지 않는다. 그래서 다음 같은 문제는 mock 테스트로는 절대 못 잡는다.

- IdP의 `iss`/`aud` 클레임이 자원 서버 설정과 맞지 않는 경우
- JWKs 캐시가 만료된 뒤 재다운로드에 실패하는 경우
- PKCE `code_verifier`/`code_challenge` 짝이 맞지 않는 경우
- DPoP의 `cnf.jkt` 검증이 깨지는 경우 (5장)
- `nonce` 불일치로 OIDC 로그인이 거부되는 경우

이 시나리오들은 **WireMock**이나 **Testcontainers + Keycloak**으로 진짜 IdP를 흉내 내야 잡힌다. 권장 가이드는 이렇다.

1. **컨트롤러 인가 매핑·CSRF·CORS·헤더** → mock으로 충분하다. 빠르고 회귀 안전망으로 가성비가 가장 좋다.
2. **OAuth2/OIDC 통합 흐름** → 슬라이스 테스트 한두 개는 mock으로 두고, 핵심 시나리오(로그인 성공, 잘못된 nonce, JWKs 회전) 한 개씩은 WireMock으로 검증한다.
3. **운영 통합 검증** → Testcontainers로 Keycloak·PostgreSQL을 띄워 한두 개의 시나리오를 끝까지 태운다. 매 PR마다 돌리진 못해도 nightly 잡으로는 돌리는 편이 낫다.

이 세 층을 한데 묶어 두면 단위 테스트의 속도와 통합 테스트의 신뢰도를 양쪽 다 챙길 수 있다.

## 12.14 통합 시나리오 — Form Login + Remember-Me + Session Fixation을 한 테스트로

마지막으로, 책 전반의 결정을 한 테스트 안에서 검증하는 예제를 하나 두자. 4장에서 다룬 폼 로그인 + Remember-Me + Session Fixation 보호가 함께 동작하는지를 한 번에 본다.

```java
@SpringBootTest
@AutoConfigureMockMvc
class FormLoginIntegrationTest {

    @Autowired MockMvc mvc;

    @Test
    void 로그인하면_세션ID가_바뀌고_remember_me_쿠키가_생긴다() throws Exception {
        // 1) 로그인 전 세션 ID
        MvcResult before = mvc.perform(get("/"))
            .andReturn();
        String oldSessionId = before.getRequest().getSession().getId();

        // 2) 폼 로그인 — remember-me 체크
        MvcResult login = mvc.perform(formLogin("/login")
                .user("alice").password("password")
                .param("remember-me", "on"))
            .andExpect(authenticated().withUsername("alice"))
            .andReturn();

        // 3) Session Fixation 보호 — 세션 ID가 갈렸어야 한다
        String newSessionId = login.getRequest().getSession().getId();
        assertThat(newSessionId).isNotEqualTo(oldSessionId);

        // 4) Remember-Me 쿠키가 설정됐다
        Cookie rememberMe = login.getResponse().getCookie("remember-me");
        assertThat(rememberMe).isNotNull();
        assertThat(rememberMe.isHttpOnly()).isTrue();

        // 5) 새 세션을 버리고 remember-me 쿠키만으로 재접속해 인증 유지 확인
        mvc.perform(get("/me").cookie(rememberMe))
            .andExpect(authenticated().withUsername("alice"));
    }
}
```

이 테스트 하나가 4장 + 9장 + 10장의 결정을 묶어서 회귀로 잡는다. 시간이 지나 누군가가 `migrateSession()`을 `none()`으로 바꾸거나, `remember-me`의 `httpOnly`를 꺼 버리면 이 테스트가 빨갛게 떨어진다. 시니어 독자에게 권하고 싶은 패턴이다. **단위 슬라이스에서 잡을 수 있는 것은 단위에서 잡되, 시나리오 통합은 한두 개의 굵은 통합 테스트로 못 박아 둔다**. 둘의 비율이 어떻게 되어야 하는지는 팀마다 다르지만, 한 가지는 분명하다. 통합 테스트가 0개라면 12장의 거의 모든 함정이 그대로 운영으로 흘러간다.

## 12.15 핵심 5줄 요약

1. **`@WithMockUser`는 빠른 단위, `@WithUserDetails`는 운영 가까운 통합, `@WithSecurityContext`는 커스텀.** 셋의 트레이드오프를 분명히 하자.
2. **`csrf()` 빠뜨리면 무조건 403.** 그리고 CSRF가 켜져 있는지 검증하는 회귀 테스트도 한 개는 박아 두자.
3. **`jwt()`/`opaqueToken()`/`oauth2Login()`/`oidcLogin()`은 상태를 흉내 낸다. 흐름은 흉내 내지 않는다.** IdP 통합 자체는 WireMock·Testcontainers로 가자.
4. **`@WebMvcTest`는 `@Import(SecurityConfig)`가 없으면 보안이 적용되지 않는다.** "모든 테스트가 초록불, 운영은 다 401" 사고의 단골 원인.
5. **7.0의 testing API는 그대로 유효하지만, `requireExplicitSave(true)`와 SPA CSRF 모드는 회귀 테스트 한 개씩을 더 박을 가치가 있다.**

## 12.16 다음 챕터에서 답할 것

12장에서는 보안 결정을 회귀 안전망에 묶는 도구를 한 번 훑었다. 그렇다면 운영 중인 5.x/6.x 코드베이스를 7.0으로 옮기는 일은 어떻게 안전하게 할 수 있을까? 마이그레이션 함정 다섯 가지의 본격 답이 13장에서 펼쳐진다. 1장에서 미리 본 빨간 줄들이 어디서 무엇으로 변하는지, 그리고 OpenRewrite로 어디까지 자동화할 수 있는지를 같이 본다.
