# 2장. 한 요청이 통과하는 길 — 필터 체인 해부

> **선행 필요:** 1장(좌표축·멘탈 모델)

한 번 상상해보자. 사용자가 브라우저 주소창에 `https://shop.example.com/api/orders`를 치고 엔터를 누른다. 그 짧은 시간에, 그러니까 우리가 커피 한 모금을 마시기 전 그 잠깐 사이에, 서버 어딘가에서는 적어도 열 개가 넘는 보안 필터가 차례로 깨어나 이 요청을 한 번씩 들여다본다. 누구는 헤더를 붙이고, 누구는 토큰을 검사하고, 누구는 컨텍스트를 비운다. 그러고 나서야 비로소 컨트롤러의 `@GetMapping("/api/orders")`가 호출된다.

이 길을 한 번도 끝까지 따라가본 적이 없다면, Spring Security의 어떤 옵션도 정확히 이해하기 어렵다. `csrf(CsrfConfigurer::disable)` 한 줄을 쓰면서도 "이게 정확히 어느 시점에 작동하는 거지?" 하는 찜찜한 기분이 가시지 않는다. 운영 중에 "CORS preflight가 401로 떨어진다"는 슬랙 알림을 받으면 어디서부터 봐야 할지 막막하다. 그렇다면 어떻게 해야 할까? 한 번, 진지하게, 요청 하나를 처음부터 끝까지 따라가보자. 우리가 그릴 이 지도가 책의 나머지 모든 장의 어휘를 떠받친다.

이 장에서는 욕심을 부리지 않는다. 인증을 깊이 파고들거나 인가 모델을 펴 보이는 일은 다음 장들의 몫이다. 우리는 다만 "한 요청이 어디로 어떻게 흘러가는가"라는 질문 하나에만 매달려, 그 길목마다 서 있는 컴포넌트들의 이름을 정확히 호명한다. 이름을 부를 수 있게 되면 그다음부터는 두렵지 않다.

---

## 2.1 서블릿 컨테이너의 눈에 비친 Spring Security

먼저 한 가지 사실을 분명히 하고 시작하자. **서블릿 컨테이너의 입장에서 Spring Security는 단 한 개의 `Filter`다.** Tomcat이든 Jetty든, 컨테이너는 자신이 등록한 필터 목록에 "Spring Security"라는 거대하고 복잡한 무언가가 들어 있다고 생각하지 않는다. 컨테이너의 눈에는 그저 평범한 `jakarta.servlet.Filter` 구현체 하나가 보일 뿐이다.

그 하나의 필터 이름이 `DelegatingFilterProxy`다. 이름이 길어서 처음 보면 위압적이지만, 하는 일은 단순하다. 컨테이너가 자기에게 요청을 넘겨주면, 자기는 직접 처리하지 않고 Spring `ApplicationContext`에 있는 어떤 빈에게 위임한다. 그 빈의 이름은 `springSecurityFilterChain`으로 고정되어 있다.

> "Spring provides a `Filter` implementation named `DelegatingFilterProxy` that allows bridging between the Servlet container's lifecycle and Spring's `ApplicationContext`." — Spring 공식 문서

왜 이렇게 한 단계를 더 두는 걸까? 잠시 멈추고 생각해보자. 서블릿 컨테이너의 라이프사이클과 Spring 빈의 라이프사이클은 다르다. 컨테이너가 필터를 등록할 시점에는 Spring `ApplicationContext`가 아직 완전히 준비되지 않았을 수 있다. 그렇다고 보안 빈을 컨테이너가 직접 들고 있으면, 우리가 자랑하는 의존성 주입이며 빈 라이프사이클이며 하는 것들이 다 무용지물이 된다. 그래서 컨테이너에는 가짜를 등록해두고, 진짜 일은 Spring 쪽에서 처리하도록 한 걸음 비켜둔 것이다. 이 분리가 만들어내는 자유는 책의 뒤에 갈수록 더 잘 느낄 수 있다.

`DelegatingFilterProxy`가 위임하는 빈은 `FilterChainProxy`다. 여기서부터가 진짜다. `FilterChainProxy`는 자기 안에 여러 개의 `SecurityFilterChain`을 갖고 있고, 들어온 요청이 그중 어떤 체인에 속하는지를 판단해 그 체인 안의 필터들만 차례로 실행한다.

```
┌────────────────────────────────────────────────────────────┐
│ Servlet Container (Tomcat / Jetty)                         │
│                                                            │
│   request ──▶ [DelegatingFilterProxy]                      │
│                       │                                    │
│                       ▼                                    │
│              ┌─────────────────────┐                       │
│              │   FilterChainProxy   │ (Spring Bean)        │
│              │                     │                       │
│              │  ┌───────────────┐  │                       │
│              │  │ Chain #1 (/api)│  │  ← 첫 매치만 실행    │
│              │  └───────────────┘  │                       │
│              │  ┌───────────────┐  │                       │
│              │  │ Chain #2 (/) │  │                       │
│              │  └───────────────┘  │                       │
│              └─────────────────────┘                       │
│                       │                                    │
│                       ▼                                    │
│                 [Controller]                               │
└────────────────────────────────────────────────────────────┘
```

이 그림 한 장이 머릿속에 들어오면 절반은 끝났다고 봐도 좋다. 컨테이너가 보는 것은 `DelegatingFilterProxy` 하나, 그 안쪽으로 들어가면 `FilterChainProxy`가 여러 체인을 들고 분기시키는 구조다.

### 2.1.1 "Only the first SecurityFilterChain that matches is invoked"

이 한 문장을 굵게 새겨두자. 이건 Spring 공식 문서에 그대로 적혀 있는 말이고, 그 함의가 생각보다 깊다.

> "Only the first `SecurityFilterChain` that matches is invoked." — Spring 공식 문서

문장 자체는 짧지만 함정이 도사리고 있다. 우리가 두 개의 `SecurityFilterChain` 빈을 만들었다고 해보자. 하나는 `/api/**`를 위한 stateless JWT 체인이고, 다른 하나는 나머지 모든 경로를 위한 stateful 폼 로그인 체인이다. 만약 등록 순서가 잘못되면 어떻게 될까? `/api/orders` 요청이 와도 `FilterChainProxy`는 폼 로그인 체인을 먼저 매칭해버린다. 그 결과 JWT 검증은 한 번도 일어나지 않고, 사용자는 영문 모를 로그인 페이지로 리다이렉트된다. 운영 중에 이 증상을 만나면 정말 난감하다.

그렇다면 어떻게 해야 할까? 두 가지 도구를 알아두자.

첫째, `@Order(...)` 어노테이션이다. 숫자가 작을수록 먼저 평가된다. 좁은 경로(`/api/**`)를 위한 체인에 더 낮은 숫자를 주는 게 자연스럽다.

둘째, `securityMatcher(...)`다. 체인이 어떤 요청에 반응할지를 명시적으로 선언한다. 이걸 빠뜨리면 그 체인은 모든 요청에 매칭되어버려서, 다른 체인이 영영 호출되지 않는다.

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")                       // ← 이 체인의 영역 선언
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
        // securityMatcher 생략 → "위에서 안 잡힌 나머지 전부"
        .authorizeHttpRequests(a -> a
            .requestMatchers("/", "/login").permitAll()
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .csrf(Customizer.withDefaults())
        .build();
}
```

이 두 빈을 함께 등록하고 나면, `/api/...`로 시작하는 요청은 첫 번째 체인이 잡고, 나머지는 두 번째 체인이 잡는다. 첫 매치 원칙이 둘을 깔끔히 분리해준다.

`securityMatcher`를 빼고 `@Order`만 매겨두면 어떻게 될까? 첫 번째 체인이 모든 요청을 다 먹어버리고, 두 번째 체인은 영영 호출되지 않는다. 빌드에는 아무 문제가 없고, 런타임에도 예외가 나지 않는다. 그저 폼 로그인이 동작하지 않을 뿐이다. 이런 종류의 함정이 가장 끔찍하다. 에러가 나면 그래도 추적할 단서가 있는데, 조용히 작동만 안 하는 경우엔 한참을 헤매게 된다.

### 2.1.2 `HttpFirewall` — 들어오기 전 검열관

`FilterChainProxy`가 요청을 받아 체인을 고르기 전에, 한 단계의 검열이 더 있다. `HttpFirewall`이다. 이름이 거창하지만 역할은 명료하다. **HTTP 표준에서 벗어난 비정상 요청을 진입 단계에서 차단**한다.

예를 들어 `/api//orders`처럼 이중 슬래시가 들어간 경로, `%2e%2e/`로 디렉터리 탈출을 시도하는 인코딩, 제어 문자가 박힌 헤더 이름. 이런 것들은 정상적인 클라이언트가 만들 일이 거의 없다. 그런데 매처 한 줄에 따라 같은 경로가 누군가에게는 `/api/orders`로 보이고 누군가에게는 `/api//orders`로 보인다면, 권한 검사를 우회할 수 있는 작은 틈이 열린다. `HttpFirewall`은 이런 모호함을 진입선에서 잘라낸다.

기본 구현은 `StrictHttpFirewall`이고, 사실상 우리가 손댈 일은 거의 없다. 다만 정상 요청이 차단되는 일이 생기면(예: legacy 서비스가 백슬래시 경로를 보내온다든지) 커스텀이 가능하다는 정도만 기억해두자. 무분별하게 룰을 풀어주는 일은 권하지 않는다. 한 번 풀린 문은 다시 닫기 어렵다.

### 2.1.3 매 호출의 끝, 컨텍스트 청소

`FilterChainProxy`가 자기 일을 마칠 때 또 하나 중요한 일을 한다. **현재 스레드의 `SecurityContext`를 비운다.** 왜 그럴까? 톰캣 같은 컨테이너는 스레드 풀로 요청을 처리한다. 사용자 A가 쓰던 스레드를, 잠시 뒤 사용자 B의 요청이 다시 가져다 쓴다. 만약 A의 인증 정보가 ThreadLocal에 그대로 남아 있다면 어떻게 될까? B가 갑자기 A의 권한을 갖게 된다. 끔찍한 일이다.

그래서 매 요청의 끝, 정확히는 `finally` 블록에서 `SecurityContextHolder.clearContext()`가 호출된다. 이 청소 동작은 `FilterChainProxy`의 책임이고, 우리가 어떤 필터를 추가하든 어떤 구성을 짜든 이 동작만큼은 보장된다. 잊지 말자. ThreadLocal과 스레드 풀의 조합은 자기 자신을 보호하는 청소부가 반드시 필요하다.

---

## 2.2 한 체인 안의 11명을 호명한다

이제 우리는 한 `SecurityFilterChain` 안으로 들어왔다. 이 안에는 기본 구성 기준으로 열 명이 좀 넘는 필터가 정해진 순서대로 줄지어 서 있다. 순서가 바뀌면 결과가 바뀌므로, 이 순서가 곧 동작의 의미다. 함께 천천히 호명해보자.

```
요청 ──▶ ① DisableEncodeUrlFilter
       ──▶ ② WebAsyncManagerIntegrationFilter
       ──▶ ③ SecurityContextHolderFilter     ◀── 세션에서 컨텍스트 로드
       ──▶ ④ HeaderWriterFilter              ◀── 보안 헤더 작성
       ──▶ ⑤ CorsFilter                      ◀── preflight 통과
       ──▶ ⑥ CsrfFilter                      ◀── 위변조 토큰 검사
       ──▶ ⑦ LogoutFilter
       ──▶ ⑧ 인증 필터들                      ◀── Form/Basic/JWT/OAuth2/OTT/WebAuthn
       ──▶ ⑨ RequestCacheAwareFilter
       ──▶ ⑩ SecurityContextHolderAwareRequestFilter
       ──▶ ⑪ AnonymousAuthenticationFilter   ◀── 익명 사용자 채우기
       ──▶ ⑫ ExceptionTranslationFilter      ◀── 인증·인가 예외 번역
       ──▶ ⑬ AuthorizationFilter             ◀── (7.0) 최종 인가 결정
       ──▶ [Servlet / Controller]
```

번호는 편의를 위한 것일 뿐, 외울 필요는 없다. 우리가 정확히 알아야 할 것은 **어떤 필터가 어떤 일에 책임이 있고, 그 책임의 결과가 다음 필터에게 어떻게 전달되는가**다. 한 명씩 만나보자.

### 2.2.1 `SecurityContextHolderFilter` — 컨텍스트를 깨우는 자

요청이 들어오면 가장 먼저 해야 할 일은 "이 요청을 보낸 사람이 누구인가"를 알아내는 게 아니다. 그 전에 **이전 요청에서 만들어진 인증 정보를 다시 불러올 수 있는지** 확인해야 한다. 폼 로그인을 한 사용자라면 `HttpSession` 안에 `SecurityContext`가 저장되어 있을 것이다. 그 컨텍스트를 꺼내 현재 스레드의 `SecurityContextHolder`에 얹어주는 일이 이 필터의 책임이다.

5.x/6.x를 거치며 이 필터는 한 가지 중요한 변화를 겪었다. 이전 세대의 `SecurityContextPersistenceFilter`는 컨텍스트를 자동으로 저장하기까지 했는데, 7.0에서는 그 책임이 떨어져 나갔다. 이제 컨텍스트의 **저장은 명시적**이다. 인증 필터가 로그인을 성공시킨 시점에 직접 저장한다. 이게 좋은 일인지 헷갈리는 일인지 처음엔 애매하다. 하지만 결과적으로 "언제 컨텍스트가 디스크로 내려가는가"가 또렷해져서, 비동기 흐름에서 컨텍스트가 새는 버그가 줄어든다.

7.0 권고 설정 한 줄을 미리 봐두자.

```java
http.securityContext(c -> c.requireExplicitSave(true));
```

이 한 줄이 무엇을 의미하는지는 10장에서 자세히 풀어낸다. 지금은 "컨텍스트는 알아서 저장되지 않는다"는 사실만 기억해두자.

### 2.2.2 `HeaderWriterFilter` — 보안 헤더를 박는 자

이 필터가 응답에 박아주는 헤더들이 책임지는 영역은 의외로 넓다. HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy, 그리고 CSP까지. 우리가 따로 설정하지 않아도 기본값으로 제법 많은 헤더가 박힌다.

```java
http.headers(h -> h
    .contentSecurityPolicy(c -> c.policyDirectives("default-src 'self'"))
    .frameOptions(f -> f.sameOrigin()));
```

여기서 한 가지 의문이 생긴다. "헤더는 응답을 내보낼 때 박는 건데, 왜 입력 단계의 필터가 책임지지?" 좋은 질문이다. 정확히 말하면, 이 필터는 응답이 나가기 전에 `ResponseWrapper`를 끼워두고, 응답 헤더가 커밋되는 순간 자기 헤더들을 함께 박는다. 그러니까 **입구 쪽 필터가 출구 쪽 책임까지 맡고 있는** 셈이다. 필터 체인의 흐름이 단방향이 아니라는 점을 여기서 한 번 체감해두자. 들어갈 때 등록하고 나올 때 작동하는 책임이 적지 않다.

### 2.2.3 `CorsFilter` — Security보다 먼저 처리되어야 하는 자

CORS는 헷갈리는 손님이다. 같은 도메인에서는 존재하지도 않는데, 도메인이 갈리는 순간 갑자기 모든 규칙을 다시 써야 한다. 그리고 그 첫 인사인 preflight 요청(`OPTIONS`)은 본 요청과 다른 길로 도착한다. 이 preflight가 인증을 필요로 한다면, 한 번도 인증 정보를 보낸 적 없는 브라우저는 곧장 401을 받고 멈춰선다. 그러면 본 요청은 시작조차 못 한다. 정말 끔찍한 일이다.

그래서 CORS 필터는 **Spring Security의 인증·인가 흐름보다 앞에서 처리되어야 한다**. 위 순서표에서 `CorsFilter`가 다섯 번째에 있는 이유다. preflight 요청은 여기서 200 OK로 짧게 응답되고, 더 안쪽으로 들어가지 않는다.

이걸 구성하는 방법은 단순하다.

```java
http.cors(c -> c.configurationSource(corsConfig));
```

`http.cors(...)`를 호출하면 Spring Security는 우리가 빈으로 등록한 `CorsConfigurationSource`를 찾아 `CorsFilter`를 적절한 위치에 자동으로 끼워준다. 우리는 정책만 결정하면 된다.

> **CORS와 CSRF는 9장에서 본격적으로 다룬다.** 이 장에서는 "왜 이 자리에 있는가"만 보는 걸로 충분하다.

### 2.2.4 `CsrfFilter` — 위변조 토큰을 검사하는 자

stateful 세션을 쓰는 흐름에서는 사용자의 쿠키가 자동으로 모든 요청에 따라붙는다. 여기에 약점이 있다. 악의적인 사이트가 사용자의 브라우저를 통해 우리 서버로 요청을 보내면, 쿠키도 함께 전송되므로 서버 입장에서는 "정상적인 사용자 요청"처럼 보인다. CSRF가 노리는 정확히 그 틈이다.

`CsrfFilter`는 상태를 바꾸는 요청(POST, PUT, DELETE 등)에 대해 별도의 토큰 검증을 요구한다. 토큰을 모르는 외부 사이트는 위조된 요청을 보내도 막힌다.

7.0에서 SPA 시나리오를 위한 단축 표현이 추가됐다.

```java
http.csrf(CsrfConfigurer::spa);   // 7.0 신규
```

이 한 줄이 `CookieCsrfTokenRepository.withHttpOnlyFalse()`와 `SpaCsrfTokenRequestHandler`를 함께 적용한다. 이전에는 SPA 환경에서 CSRF를 정확히 켜기가 번거로웠는데, 7.0이 그 번거로움을 한 줄로 줄여줬다.

API 전용 체인에서는 `csrf(CsrfConfigurer::disable)`로 끄는 경우가 많은데, 이때 함정이 하나 있다. **두 개의 체인을 운영할 때, 폼 로그인이 살아 있는 웹용 체인에서까지 무심코 CSRF를 끄지 않도록 주의하자.** stateful 흐름에서 CSRF를 끄는 순간 사실상 문이 열린다. "API니까 disable"이 머릿속에 박혀 있으면, 어느새 웹 체인에까지 같은 코드가 복붙된다. 이건 13장 마이그레이션 함정 절에서 다시 만나게 된다.

### 2.2.5 인증 필터들 — 토큰을 풀어내는 자들

이제부터가 다채롭다. 한 체인 안에는 한 번에 여러 인증 필터가 들어 있을 수 있고, 각자 자기가 처리할 수 있는 형식의 요청만 잡아낸다.

- `UsernamePasswordAuthenticationFilter` — 폼 로그인용. 기본 `/login` 경로의 POST를 잡는다.
- `BasicAuthenticationFilter` — HTTP Basic. `Authorization: Basic ...` 헤더를 본다.
- `BearerTokenAuthenticationFilter` — 자원 서버. `Authorization: Bearer ...`를 본다.
- `OAuth2LoginAuthenticationFilter` — `/login/oauth2/code/{registrationId}` 콜백을 받는다.
- `OneTimeTokenAuthenticationFilter` — 7.0 안정화. 매직 링크 흐름.
- `WebAuthnAuthenticationFilter` — 7.0 안정화. Passkeys 흐름.

각 필터가 어떤 토큰을 만들고 어떤 `AuthenticationManager`에게 검증을 위임하는지는 3장에서 펼친다. 지금은 한 가지만 잡고 가자. **인증 필터는 인증의 시작점이지 종착점이 아니다.** 실제 검증의 책임은 `AuthenticationManager`(보통 `ProviderManager`)에게 있다. 필터는 그저 요청에서 자격 증명을 뽑아내고, 매니저의 결과를 받아 `SecurityContext`에 채워 넣을 뿐이다. 이 분리가 만들어주는 유연함이 적지 않다.

### 2.2.6 `AnonymousAuthenticationFilter` — 모르는 사람도 누군가는 되게

인증 필터들이 모두 침묵했다면 — 즉, 이 요청에는 자격 증명이 없거나 검증되지 못했다면 — `SecurityContext`는 비어 있을 것이다. 그런데 `AuthorizationFilter`에 이르러서 "권한이 어떻게 되는가"를 검사하려면 그 비어 있음이 곤란하다. `null`을 들고 권한을 따질 수는 없다.

그래서 이 자리에 `AnonymousAuthenticationFilter`가 서 있다. 컨텍스트가 비어 있으면 `ROLE_ANONYMOUS` 권한을 가진 가짜 `Authentication` 객체를 슬며시 채워 넣는다. 익명 사용자도 어쨌든 "누군가"가 되어 다음 필터로 흘러간다.

이 작은 트릭 덕분에 인가 단계의 코드가 단순해진다. "인증된 사용자인가, 아닌가"를 매번 따지는 게 아니라, "이 권한이 충분한가, 부족한가"라는 한 가지 질문으로 정리된다. 부족하면 다음 차례인 `ExceptionTranslationFilter`가 적절한 응답을 내준다. 영리한 구조다.

### 2.2.7 `ExceptionTranslationFilter` — 가장 토비스러운 자리

이 필터는 챕터 전체에서 가장 흥미로운 자리에 서 있다. 자기는 거의 아무 일도 하지 않으면서, 그 안쪽에서 던져진 예외들을 일관된 HTTP 응답으로 번역한다. 우아하다.

그 일을 코드로 풀어 보면 대략 이렇다.

```java
try {
    chain.doFilter(req, res);                    // 안쪽으로 진입
} catch (AuthenticationException ae) {
    // 인증이 아예 안 됐거나 끊김
    //   → AuthenticationEntryPoint 호출
    //     · 웹: 로그인 페이지로 리다이렉트
    //     · API: 401 Unauthorized
} catch (AccessDeniedException ade) {
    if (anonymous) {
        startAuthentication();                   // 익명이면 우선 로그인 유도
    } else {
        accessDenied();                          // 그렇지 않으면 403 Forbidden
    }
}
```

이 짧은 흐름이 만들어내는 의미가 크다. 안쪽 어디서든 — `AuthorizationFilter`에서든, `@PreAuthorize`가 걸린 메서드에서든, 자원 서버의 JWT 검증 단계에서든 — `AuthenticationException`이나 `AccessDeniedException`이 던져지면 모두 여기로 모인다. 그리고 각자 알맞은 응답으로 번역된다. 비즈니스 코드는 자기 예외만 던지면 되고, HTTP 응답의 정합성은 이 필터가 책임진다.

여기서 한 가지 의문이 생긴다. "인증이 안 된 익명 사용자가 권한이 부족한 자원에 접근하면, 401일까 403일까?" 코드를 다시 보자. `AccessDeniedException`인데 사용자가 익명이면 `startAuthentication()`을 부른다. 즉 **익명이면 우선 로그인하라**는 메시지를 보낸다. 웹에서는 로그인 페이지로 리다이렉트, API에서는 401이다. 이미 인증된 사용자가 권한이 모자라면 그때 비로소 403이다. 사람의 직관에 잘 맞는 분기다.

`AuthenticationEntryPoint`와 `AccessDeniedHandler`를 우리가 커스텀하면, 이 번역의 출력만 갈아끼울 수 있다. ProblemDetail(RFC 7807) 형식으로 일관된 에러 응답을 내고 싶다든지, 사내 표준 에러 코드를 박고 싶다든지 할 때 손댈 자리가 바로 여기다. 자세한 활용은 8장 후반에서 다시 만난다.

### 2.2.8 `AuthorizationFilter` — 7.0의 새 종착역

이 자리는 7.0에서 큰 정리가 일어났다. 과거에는 `FilterSecurityInterceptor`라는 또 다른 컴포넌트가 인가 결정을 책임졌고, 같은 일을 새 모델인 `AuthorizationFilter`가 또 할 수 있어 두 길이 공존했다. **7.0에서는 `FilterSecurityInterceptor`가 완전히 사라졌다.** 인가의 종착역은 이제 오직 `AuthorizationFilter` 하나다.

이 필터가 하는 일은 간결하다. 등록된 `AuthorizationManager`에게 "이 요청, 이 사용자, 통과시킬까요?"라고 묻고, 결과가 거부면 `AccessDeniedException`을 던진다. 그러면 바로 앞에서 만난 `ExceptionTranslationFilter`가 받아 적절히 번역한다.

`AuthorizationManager`의 신모델, 그 안에서도 7.0에 추가된 `AllAuthoritiesAuthorizationManager`(AND 조건)와 `AuthorizationManagerFactory` 같은 등장인물들은 3장에서 본격적으로 호명한다. 지금은 한 가지만 잡고 가자. **인가는 한 곳에서 결정된다.** 그 한 곳이 바로 이 필터다.

> **알아두면 좋다 — 5.x/6.x 코드에서 `.access(...)` 나 `AccessDecisionManager`를 봤다면**
> 그건 옛 세대의 어휘다. 7.0에서는 `Access*` 계열 API가 별도 모듈 `spring-security-access`로 격리됐다. 기본 의존성에 더는 들어 있지 않다. 마이그레이션의 핵심 함정 중 하나이고, 자세한 답은 13장에 펼친다.

---

## 2.3 그래서 한 요청은 어떻게 흘러가는가

이제 우리가 호명한 이름들로 시작 시나리오를 다시 따라가보자. 사용자가 폼 로그인을 마치고 `GET /api/orders`를 보낸다.

```
[Browser]
    │
    │ GET /api/orders
    │ Cookie: JSESSIONID=...
    ▼
[Servlet Container] ──▶ [DelegatingFilterProxy]
                                 │
                                 ▼
                       [FilterChainProxy]
                                 │
                       ┌─────────┴─────────┐
                       │ 첫 매치만 실행      │
                       │ → Chain "/api/**" │
                       └─────────┬─────────┘
                                 ▼
        ┌────────────────────────────────────────┐
        │ SecurityContextHolderFilter            │
        │   세션에서 SecurityContext 로드          │
        ├────────────────────────────────────────┤
        │ HeaderWriterFilter                     │
        │   응답 헤더 등록 예약 (HSTS, CSP, ...)    │
        ├────────────────────────────────────────┤
        │ CorsFilter                             │
        │   preflight면 여기서 종결                │
        ├────────────────────────────────────────┤
        │ CsrfFilter                             │
        │   API 체인이라 disable이면 통과          │
        ├────────────────────────────────────────┤
        │ BearerTokenAuthenticationFilter        │
        │   Authorization: Bearer ... 추출         │
        │   → AuthenticationManager 위임          │
        │   → SecurityContext 채움                │
        ├────────────────────────────────────────┤
        │ (anonymous 필요 없음 — 인증됨)            │
        ├────────────────────────────────────────┤
        │ ExceptionTranslationFilter             │
        │   안쪽 호출을 try-catch로 감쌈            │
        ├────────────────────────────────────────┤
        │ AuthorizationFilter                    │
        │   AuthorizationManager에게 결정 위임      │
        │   허가 → 통과 / 거부 → AccessDenied      │
        └────────────────────────────────────────┘
                                 │
                                 ▼
                        [DispatcherServlet]
                                 │
                                 ▼
                  @GetMapping("/api/orders") 컨트롤러
                                 │
                                 ▼
                            [응답]
                                 │
              (역순으로 빠져나오며 헤더 박힘, 컨텍스트 청소)
                                 │
                                 ▼
                           [Browser]
```

이 그림에서 화살표가 위에서 아래로만 흐르지 않는다는 점에 주목하자. 응답이 나갈 때 역순으로 빠져나오며 `HeaderWriterFilter`가 헤더를 박고, 마지막에 `FilterChainProxy`가 `SecurityContext`를 청소한다. 들어올 때 한 일과 나갈 때 한 일이 짝을 이루는 구조다.

여기까지 따라왔다면, 책의 다른 모든 장에서 마주칠 코드의 위치를 우리는 짚어낼 수 있다. `csrf(...)`는 ⑥번 자리에 영향을 주고, `oauth2ResourceServer(o -> o.jwt(...))`는 ⑧번 자리에 `BearerTokenAuthenticationFilter`를 끼워 넣는다. `authorizeHttpRequests(...)`는 ⑬번 자리에 `RequestMatcherDelegatingAuthorizationManager`를 구성해 박는다. 그저 람다 한 줄 한 줄이, 이 줄지어 선 필터들 어딘가에 한 마디씩 보태고 있을 뿐이다.

---

## 2.4 두 개의 체인 — 웹 stateful + API stateless

앞서 살짝 보였지만, 실무에서 가장 흔히 만나는 패턴은 **두 개의 `SecurityFilterChain`을 한 애플리케이션에 함께 두는 것**이다. 한쪽은 사람이 브라우저로 보는 화면, 다른 한쪽은 SPA나 모바일 앱이 호출하는 API다. 둘은 보안 결정의 결이 다르다.

| 결정 | 웹용 (사람의 브라우저) | API용 (프로그램이 호출) |
|---|---|---|
| 세션 정책 | `IF_REQUIRED` (기본) | `STATELESS` |
| CSRF | 켠다 | 끈다(또는 SPA 모드) |
| 인증 방식 | 폼 로그인 / OAuth2 Login | JWT 자원 서버 |
| 미인증 응답 | 로그인 페이지 리다이렉트 | 401 JSON |

코드로 풀면 이렇게 나란히 둘 수 있다.

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
            .requestMatchers("/", "/login", "/signup", "/css/**").permitAll()
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .csrf(Customizer.withDefaults())
        .build();
}
```

`FilterChainProxy`는 들어온 요청에 대해 `@Order(1)`부터 매처를 평가한다. `/api/orders`는 첫 체인이 잡고, `/dashboard`는 두 번째 체인이 잡는다. 두 체인이 각자 자기 색깔의 보안을 가진 채로 한 애플리케이션 안에서 공존한다.

이 구성을 처음 짜는 분들이 흔히 빠지는 함정 셋을 짧게 짚어두자. 자세한 답은 해당 장에서 다시 만난다.

1. **API 체인의 `securityMatcher`를 빠뜨림.** 그러면 첫 체인이 모든 요청을 먹는다. 폼 로그인은 영영 동작하지 않는다.
2. **`@Order`를 안 매김.** 두 빈의 평가 순서가 빌드마다 들쭉날쭉해진다. 정상 동작이 운으로 결정되는 끔찍한 상황이다.
3. **API 체인에서 CSRF를 끈 코드를 그대로 웹 체인에 복붙.** 13장에서 다시 만난다.

이 패턴은 8장(인가)과 15장(통합 실전)에서 본격적으로 다시 펼쳐진다. 지금은 "두 체인이 공존할 수 있고, `FilterChainProxy`가 첫 매치 원칙으로 둘을 분리한다"는 사실만 머릿속에 박아두자.

---

## 2.5 내가 만든 Filter를 끼우는 법

여기까지 읽으면 자연스럽게 떠오르는 질문이 있다. "그러면 내가 직접 만든 Filter는 어디에 어떻게 끼우지?" 시니어 독자가 가장 자주 묻는 질문 중 하나다.

요청별 감사 로그를 남기고 싶다. 사내 SSO에서 받은 커스텀 헤더를 파싱해 `Authentication`을 만들고 싶다. 들어온 토큰을 미리 한 번 다듬어두고 싶다. 이런 요구는 `HttpSecurity` DSL의 기본 메뉴 바깥에 있다. 우리만의 필터를 한 명 더 끼워야 한다.

도구는 셋이다.

```java
http.addFilterBefore(myFilter, BasicAuthenticationFilter.class);
http.addFilterAfter (myFilter, BasicAuthenticationFilter.class);
http.addFilterAt    (myFilter, BasicAuthenticationFilter.class);
```

이름이 직관적이라 헷갈리지 않는다. 어떤 표준 필터의 **앞**, **뒤**, **같은 자리**에 자기 필터를 끼우는 것이다. 단, `addFilterAt`은 같은 자리에 들어갈 뿐 표준 필터를 대체하지는 않는다는 점에 유의하자.

### 2.5.1 자리 결정의 감각

그렇다면 어디에 끼워야 할까? 한 가지 원칙으로 정리할 수 있다.

> **내 필터가 의존하는 정보가 채워진 이후에, 내 필터의 결과가 필요한 자리 이전에 끼운다.**

말이 추상적이니 예를 보자. 우리가 만들 필터의 책임이 "현재 인증된 사용자의 ID를 로그에 남기는 것"이라고 하자. 그렇다면 이 필터는 **`AuthorizationFilter` 이전, 그리고 인증 필터들 이후**에 있어야 한다. 인증이 끝나기 전이라면 `SecurityContext`가 비어 있을 테고, 인가가 끝난 후라면 거부된 요청은 이미 응답으로 빠져나간 뒤다.

```java
http.addFilterAfter(new AuditLogFilter(), AuthorizationFilter.class);
// → 인증·인가가 모두 끝난 직후, 컨트롤러로 진입하기 직전에 로그를 남긴다
```

반대로 "커스텀 헤더에서 인증 정보를 뽑아 직접 `SecurityContext`를 채우는 필터"라면, **`UsernamePasswordAuthenticationFilter` 즈음에**, 그것도 보통은 그 **앞**에 끼우는 게 자연스럽다.

```java
http.addFilterBefore(new HeaderAuthFilter(), UsernamePasswordAuthenticationFilter.class);
```

자리를 잘못 잡으면 어떻게 될까? 인가 필터보다 뒤에 인증 필터를 두면, 인가는 항상 익명 상태로 평가해 모든 요청을 거부한다. `CorsFilter`보다 뒤에 CORS preflight 처리 로직을 두면, preflight는 영영 처리되지 않는다. 증상이 또렷하게 드러나지 않는 경우가 많아서, "왜 안 되지?"를 한참 헤매게 된다. 자리 결정은 곧 의미 결정이다.

### 2.5.2 `OncePerRequestFilter` 패턴

직접 필터를 만들 때 한 가지 권장 패턴이 있다. `OncePerRequestFilter`를 상속하는 것이다.

```java
public class AuditLogFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(AuditLogFilter.class);

    @Override
    protected void doFilterInternal(HttpServletRequest req,
                                    HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        var auth = SecurityContextHolder.getContext().getAuthentication();
        var who  = (auth != null) ? auth.getName() : "anonymous";
        log.info("ACCESS {} {} by {}", req.getMethod(), req.getRequestURI(), who);

        chain.doFilter(req, res);
    }
}
```

왜 굳이 이 추상 클래스를 상속할까? 서블릿 컨테이너는 한 요청 안에서 같은 필터를 두 번 호출하는 경우가 있다. forward나 include 같은 디스패치가 끼면 그렇다. 그때마다 우리 필터가 또 로그를 남기면 한 요청에 두 줄, 세 줄이 찍힌다. 찜찜하다. `OncePerRequestFilter`는 요청 속성에 표시를 남겨 같은 요청 안에서 자기 자신을 두 번 호출하지 않도록 보장한다. 이 안전망 위에서 비즈니스 로직에 집중할 수 있다.

`HttpServletRequest`로 캐스팅하는 보일러플레이트도 줄어든다. 부모 클래스가 이미 캐스팅해서 넘겨주니, 우리는 `doFilterInternal`만 채우면 된다. 작은 편의지만, 매 필터마다 같은 코드를 반복하지 않게 해준다.

### 2.5.3 한 번 더 — 빈으로 등록할 때의 함정

여기서 잠깐 멈추고 한 가지 함정을 짚자. 우리가 만든 필터를 `@Component` 같은 어노테이션으로 빈으로 등록하면 어떻게 될까? Spring Boot의 servlet auto-configuration이 그 빈을 보고 **컨테이너에 자동으로 등록해버린다.** 그러면 `FilterChainProxy` 바깥에서, 우리가 의도하지 않은 자리에서, 같은 필터가 한 번 더 실행된다.

그 결과 요청 한 번에 우리 필터가 두 번 호출되는 상황이 벌어진다. 인증 정보가 두 번 채워지거나, 로그가 두 번 찍힌다. 끔찍한 일이다.

해결책은 두 가지다.

```java
// 방법 1: 빈으로 등록하되, servlet container의 자동 등록을 막는다
@Bean
FilterRegistrationBean<AuditLogFilter> disableAutoRegistration(AuditLogFilter f) {
    var reg = new FilterRegistrationBean<>(f);
    reg.setEnabled(false);
    return reg;
}

// 방법 2: 빈으로 등록하지 않고 HttpSecurity에서만 new로 끼운다
http.addFilterAfter(new AuditLogFilter(), AuthorizationFilter.class);
```

둘 중 어느 쪽이든 좋다. 다만 어느 쪽이든 **"이 필터는 Spring Security 체인 안쪽에만 산다"**는 의도를 코드에서 드러내는 게 바람직하다. 6개월 뒤의 우리 자신이 헤매지 않으려면.

---

## 2.6 잠깐 짚고 가는 함정 하나 — 정적 자원과 `permitAll`

작은 이야기로 한 절을 더 쓴다. 시니어 독자라면 한 번쯤 만났을 풍경이다.

폼 로그인을 켠 웹 애플리케이션에 CSS와 JS, 이미지가 잔뜩 있다. 로그인 페이지에서도 보여줘야 하니까, 우리는 자연스럽게 `permitAll`을 떠올린다.

```java
.authorizeHttpRequests(a -> a
    .requestMatchers("/css/**", "/js/**", "/images/**").permitAll()
    .anyRequest().authenticated())
```

문제는 없어 보인다. 그런데 사실은, 정적 자원에 대한 요청도 매 번 우리의 보안 필터 체인을 전부 통과한다. 11명의 필터가 한 번씩 깨어나 자기 일을 한다. CSS 하나를 받기 위해 세션을 열고 컨텍스트를 로드하고 헤더를 박는다. 한 페이지가 정적 자원 50개를 호출한다고 생각해보자. 필터 호출이 500번을 넘는다. 동작은 한다. 한다. 그런데 뒷맛이 찜찜하다.

대안은 `WebSecurityCustomizer`다.

```java
@Bean
WebSecurityCustomizer ignore() {
    return web -> web.ignoring().requestMatchers("/css/**", "/js/**", "/images/**");
}
```

이렇게 풀어두면, 매칭된 요청은 Spring Security의 필터 체인 자체를 건너뛴다. 보안이 무의미한 정적 자원에 대해 비용을 내지 않는 길이다.

물론 주의가 따른다. **민감하지 않은 진짜 정적 자원에만 쓰자.** 사용자별로 분리된 업로드 파일 같은 자원은 절대 여기에 넣으면 안 된다. 한 번 ignore된 자원은 우리의 어떤 인가 규칙도 통과하지 않는다. 풀고 잠그는 일은 신중해야 한다.

이 함정도 13장에서 마이그레이션 함정 중 하나로 다시 만나게 된다. 5.x 시절에 `WebSecurityCustomizer`로 잘 풀어뒀던 코드를 7.0으로 옮기는 과정에서 무심코 빠뜨리는 경우가 많기 때문이다.

---

## 2.7 챕터 요약 — 5줄

1. 컨테이너의 눈에 Spring Security는 `DelegatingFilterProxy` 하나이고, 그 뒤에서 `FilterChainProxy`가 여러 `SecurityFilterChain`을 들고 첫 매치 원칙으로 분기시킨다.
2. 한 체인 안에는 `SecurityContextHolderFilter` → `HeaderWriterFilter` → `CorsFilter` → `CsrfFilter` → 인증 필터들 → `AnonymousAuthenticationFilter` → `ExceptionTranslationFilter` → `AuthorizationFilter`가 정해진 순서로 줄지어 서 있다. 순서가 곧 의미다.
3. `ExceptionTranslationFilter`가 안쪽 모든 인증·인가 예외를 일관된 HTTP 응답으로 번역하는 우아한 자리에 서 있고, 7.0에서는 `FilterSecurityInterceptor`가 사라지고 `AuthorizationFilter`가 인가의 단일 종착역이 됐다.
4. 두 개의 `SecurityFilterChain`(웹 stateful + API stateless)을 한 애플리케이션에 두는 패턴이 표준이며, `@Order`와 `securityMatcher`를 함께 쓰는 게 안전하다.
5. 내가 만든 필터는 `addFilterBefore`/`addFilterAfter`로 표준 필터 사이에 끼우고, `OncePerRequestFilter`를 상속해 중복 호출을 막자. 자동 빈 등록은 막아두는 편이 낫다.

## 다음 챕터에서 답할 것

이 장에서 우리는 필터들의 이름과 자리를 호명했다. 그러나 각 필터의 안쪽에서 실제로 누구에게 무엇을 맡기는지는 아직 들여다보지 않았다. 인증 필터가 위임하는 `AuthenticationManager`는 정확히 누구인가? `ProviderManager`는 여러 `AuthenticationProvider`를 어떻게 골라 쓰는가? `AuthorizationFilter`가 결정 위임하는 `AuthorizationManager`의 신모델은 5.x/6.x와 무엇이 어떻게 다른가? 그리고 7.0에서 새로 합류한 `AuthorizationManagerFactory`와 `AllAuthoritiesAuthorizationManager`는 어떤 자리를 채우는가?

다음 장에서 이 컴포넌트들의 어휘를 정립하자. 이번 장의 필터 지도 위에, 그 안쪽 컴포넌트들의 위임 모델을 한 겹 더 얹으면, 책의 모든 인증·인가 시나리오를 그 위에서 정확하게 그려낼 수 있게 된다.
