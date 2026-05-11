# 9장. CSRF·CORS·보안 헤더 — 가장 헷갈리는 셋

신입 시절 가장 헷갈렸던 셋이 있다. CSRF, CORS, 그리고 보안 헤더다. 이름부터 비슷해서 머리가 어지럽고, 어디에 무엇이 쓰이는지 구분이 안 가서 늘 인터넷 검색 결과를 그대로 복붙하곤 했다. 누군가 "CSRF는 켜라, CORS는 미리 통과시켜라"라고 한 줄로 정리해줬을 때 비로소 안개가 걷히는 느낌이었다.

그렇다면 그 한 줄은 도대체 무슨 뜻일까. 왜 어떤 건 켜야 하고 어떤 건 미리 통과시켜야 한다는 걸까. 이 장은 그 짧은 한 마디를 천천히 풀어보는 데 거의 모든 페이지를 쓴다. 결론부터 던지면, 두 기능은 출발지부터 목적지까지 모두 다르다. 단지 영문 약자가 비슷할 뿐이다.

CORS와 CSRF는 이름이 비슷해서 더 헷갈린다. 알파벳 네 글자 중 세 글자가 같으니 처음 보는 사람 입장에서는 같은 가족처럼 느껴질 만하다. 그러나 한쪽은 "다른 출처에서 우리 API를 부르려고 할 때 브라우저가 미리 확인하는 절차"이고, 다른 한쪽은 "사용자가 모르는 사이에 우리 도메인에 위장된 요청이 날아드는 공격을 막는 토큰 검사"다. 방향도, 출발지도, 목적도 다르다. 다만 둘 다 브라우저 동작과 깊게 얽혀 있어서, 잘못 건드리면 똑같이 "401이 떨어지고 SPA가 안 뜬다" 같은 증상으로 수렴할 뿐이다. 그래서 더 헷갈린다.

순서는 요청이 들어오는 흐름을 그대로 따라가 보자. CORS 검사가 Security보다 먼저 끝나야 하니 CORS부터 시작한다. 그다음 CSRF의 의미와 7.0이 새로 내놓은 한 줄짜리 단축 설정 `csrf(CsrfConfigurer::spa)`를 살펴보고, 이어서 `HeaderWriterFilter`가 알아서 써주는 보안 헤더들을 하나씩 짚어 본다. 마지막으로 HTTPS와 TLS 운영 맥락 — 특히 리버스 프록시 뒤에서 자주 깨지는 부분 — 을 정리한다. 가장 헷갈리는 셋을 함께 정리해두자.

## CORS는 Security보다 먼저 통과해야 한다

CORS(Cross-Origin Resource Sharing)는 사실 Spring Security의 기능이 아니다. 브라우저가 보안을 위해 정해둔 규약이고, 서버는 그 규약에 응답할 뿐이다. 그런데도 Spring Security 책에서 CORS를 다루는 이유는, 잘못 다루면 가장 먼저 꼬이는 자리가 바로 보안 필터 체인이기 때문이다.

상황을 가정해보자. 프런트엔드 SPA는 `https://app.example.com`에 배포되어 있고, API 서버는 `https://api.example.com`이다. 도메인이 다르니 브라우저는 본 요청을 보내기 전에 OPTIONS 메서드로 "이 출처에서 이 메서드를 보내도 되겠냐"고 미리 묻는다. 이걸 preflight 요청이라고 부른다. preflight는 쿠키도 인증 헤더도 가지고 오지 않는다. 그저 미리 확인만 하는 가벼운 노크다.

그런데 우리 서버 앞에는 Spring Security 필터 체인이 떡 버티고 있다. 이 체인은 들어오는 모든 요청에 "당신은 인증되었나"를 묻는다. 인증 안 된 OPTIONS 요청? 당연히 401이다. 그리고 브라우저는 401을 보고는 본 요청을 아예 보내지 않는다. 프런트 콘솔에는 "CORS error"가 떠 있고, 백엔드 로그에는 OPTIONS 요청에 대한 401만 남아 있다. 양쪽 어디에도 명확한 원인이 안 보인다. 난감하다.

신입 시절 이 증상을 처음 만났을 때는 "CORS 설정을 어떻게 해야 한다더라"를 검색한 끝에 컨트롤러 메서드마다 `@CrossOrigin`을 붙이는 처방을 따라했다. 일부는 풀리고 일부는 그대로 깨진다. 또 어떤 글은 `WebMvcConfigurer`의 `addCorsMappings`를 권한다. 그것도 일부는 풀리고 일부는 그대로 깨진다. 처방이 듣지 않는 진짜 이유는 한 가지였다. **요청은 Spring MVC에 닿기도 전에 Security 필터에서 401로 끊긴다.** MVC 단계에서 CORS 헤더를 붙여줘봐야 그건 본 요청용이지, preflight를 통과시키는 건 아니다.

그렇다면 어떻게 해야 할까. 답은 의외로 간결하다. Security 필터 체인에 "CORS 처리는 너희 필터들이 일하기 _전에_ 끝나야 한다"고 명시적으로 알려주는 것이다.

```java
@Bean
SecurityFilterChain spa(HttpSecurity http, CorsConfigurationSource cors) throws Exception {
    return http
        .cors(c -> c.configurationSource(cors))
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2Login(Customizer.withDefaults())
        .build();
}
```

`http.cors(...)` 한 줄이 들어가면 Spring Security는 컨테이너에 등록된 `CorsConfigurationSource` 빈을 찾아 `CorsFilter`로 감싼 뒤, 자기 자신보다 앞쪽에 배치한다. 이제 OPTIONS 요청은 Security 체인이 인증을 검사하기 전에 CORS 필터에서 처리되고, allowed origin이면 그대로 응답 헤더를 붙여 통과시킨다. SPA가 살아난다.

여기서 한 가지 잊지 말자. `http.cors(...)`만 호출하고 `CorsConfigurationSource` 빈을 등록하지 않으면 효과가 거의 없다. 빈이 없으면 Security가 기본값으로 동작하는데, 그 기본값은 대개 실제 환경에서는 충분하지 않다. CORS 정책의 실제 내용은 빈에 담아둬야 한다.

### `CorsConfigurationSource` 빈을 어떻게 채울까

빈의 구조는 단순하다. 한 객체 안에 "어떤 출처를", "어떤 메서드를", "어떤 헤더를" 허용할지, 그리고 자격 증명(쿠키·Authorization 헤더)을 함께 보낼 수 있는지를 담는다.

```java
@Bean
CorsConfigurationSource corsConfig() {
    var c = new CorsConfiguration();
    c.setAllowedOrigins(List.of("https://app.example.com"));
    c.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    c.setAllowedHeaders(List.of("*"));
    c.setAllowCredentials(true);
    c.setMaxAge(3600L);

    var src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/**", c);
    return src;
}
```

이 코드를 한 줄씩 곱씹어보자. 첫째, `allowedOrigins`는 도메인 화이트리스트다. `*`을 쓰고 싶은 유혹이 들지만, `allowCredentials=true`와 함께 쓰면 브라우저가 거부한다 — 명세상 그렇게 되어 있다. 운영에서는 출처를 명시적으로 적어두는 편이 낫다. 패턴 매칭이 필요하면 `setAllowedOriginPatterns(...)`을 쓴다.

둘째, `allowedMethods`에 `OPTIONS`를 잊지 말자. preflight 자체가 OPTIONS이므로 이게 빠지면 처음부터 막힌다. 셋째, `allowedHeaders`에는 SPA가 실제로 보내는 헤더들 — 예컨대 `Authorization`, `Content-Type`, `X-XSRF-TOKEN` — 을 허용해야 한다. 운영 환경에서는 `*` 대신 필요한 것만 명시하는 편이 안전하다.

넷째, `allowCredentials=true`는 쿠키 기반 인증이나 BFF 시나리오일 때 켠다. JWT를 Authorization 헤더로만 주고받는다면 굳이 켤 필요는 없다 — 다만, 그 경우라도 헤더 자체는 자격 증명에 해당하므로 정책상 켜두는 일이 많다. 마지막 `maxAge`는 브라우저가 preflight 결과를 캐시하는 시간이다. 잘 정해두면 OPTIONS 트래픽이 눈에 띄게 줄어든다.

빈 하나로 모든 경로의 CORS 정책을 통일하기 어렵다면, 같은 `UrlBasedCorsConfigurationSource`에 여러 패턴을 등록할 수 있다. 예컨대 `/api/public/**`은 모든 출처에서 GET만 허용하고, `/api/private/**`은 특정 출처에 한해 자격 증명을 허용하는 식이다. 한 객체 안에 정책을 모아두면 운영 중에 정책을 추적하기 쉬워진다.

### preflight 401, 디버깅 순서

CORS preflight 401이 떴다면 다음 순서로 짚어보자. 첫째, 응답이 정말 401인지, 아니면 403이나 405인지 본다. 401이면 Security 필터에서 끊긴 것이고, 403/405면 다른 자리에서 거부된 것이다. 둘째, 브라우저 네트워크 탭에서 OPTIONS 요청의 `Origin`과 `Access-Control-Request-Method` 헤더 값을 본다. 셋째, Security 로그를 `DEBUG`로 켜고 OPTIONS 요청이 어느 필터에서 끊겼는지 본다. `CorsFilter`가 그 앞에 있지 않다면 `http.cors(...)`이 누락된 것이다. 넷째, `CorsConfigurationSource` 빈이 컨텍스트에 등록되어 있는지 확인한다. 둘 중 하나라도 빠지면 증상이 똑같이 보인다.

여기까지가 CORS다. 정리하면, **`http.cors(...)` + `CorsConfigurationSource` 빈**, 이 두 가지가 한 묶음이다. 그리고 이 묶음의 의미는 "Security가 일하기 전에 CORS를 먼저 통과시켜라"다.

## CSRF — 왜 켜야 하는가

CORS의 검사가 끝나면 본 요청이 들어온다. 이제 진짜 보안의 문제다. CSRF(Cross-Site Request Forgery)는 사용자가 우리 사이트에 로그인한 상태에서, 다른 사이트를 방문했다가 그 사이트가 몰래 우리 사이트로 요청을 보내는 공격을 막는 방어다. 핵심은 "사용자가 모르는 사이에"라는 부분이다.

상황을 가정해보자. 사용자가 우리 은행 사이트에 로그인해 세션 쿠키를 받았다. 그 상태로 다른 탭에서 어떤 게시판을 열었는데, 게시글에 숨겨진 `<form action="https://bank.example.com/transfer" method="post">`가 자동으로 제출되도록 짜여 있다. 브라우저는 우리 은행 도메인으로 가는 요청에 쿠키를 자동으로 첨부한다. 서버 입장에서는 이게 진짜 사용자의 요청인지, 다른 사이트가 사용자 모르게 흘려보낸 위장 요청인지 분간하기 어렵다. 송금이 일어난다. 끔찍한 일이다.

CSRF 토큰은 이 분간을 위한 도구다. 우리 서버가 만든 비밀 값을 폼이나 헤더에 같이 실어 보내면, 진짜 우리 사이트에서 출발한 요청만 그 값을 가질 수 있다. 다른 사이트는 같은 출처가 아니므로 우리 서버가 발급한 토큰을 읽지 못한다 — 브라우저의 same-origin policy 덕분이다. 토큰 일치 여부만 확인하면 위장 요청을 분명하게 걸러낼 수 있다.

그렇다면 어떤 흐름에서 CSRF가 필수일까. 정답은 단 한 줄이다. **쿠키로 자동 인증되는 모든 흐름**. 폼 로그인 + 세션 쿠키, OIDC 로그인 + 세션 쿠키, BFF 패턴의 세션 쿠키 — 이 모두가 stateful 흐름이고, 브라우저가 쿠키를 자동으로 보내므로 CSRF가 가능하다. 따라서 CSRF 토큰도 함께 필요하다.

반대로 Bearer 토큰(JWT)을 헤더로 명시적으로 실어 보내는 API는 CSRF의 사정권 바깥이다. 브라우저가 토큰을 자동으로 첨부하지 않기 때문이다. localStorage에 저장된 JWT를 위장 요청이 마음대로 읽지 못한다(읽힌다면 그건 XSS이지 CSRF가 아니다). 그래서 "순수 자원 서버" 체인에서는 `csrf.disable()`이 합리적이다.

이 구분이 명확해지면, "CSRF 켜? 꺼?"라는 질문에 한 줄로 답할 수 있다. 쿠키로 인증하면 켜고, Bearer로만 인증하면 꺼라. 그 한 줄이다.

### 함정: "API니까 CSRF disable" — 그리고 form login이 깨진다

이 시점에서 정말 자주 보는 함정을 짚어보자. 어느 날 팀에서 React로 SPA를 새로 만들기로 했다. 백엔드는 기존 Spring Boot에 REST API를 추가하는 형태다. 인증은 일단 JWT로 가기로 정했다. 그래서 누군가 `SecurityFilterChain`을 열고 `.csrf(c -> c.disable())`을 한 줄 추가한다. SPA에서 로그인이 잘 된다. 다들 만족한다.

며칠 후 운영 관리자 화면을 만진 동료가 슬쩍 묻는다. "어… 관리자 페이지 로그인이 깨졌어요. 폼 제출이 403이 떨어집니다." 처음엔 무슨 말인지 모른다. 코드를 보니 `formLogin()`도, `permitAll()`도 그대로다. 그런데 폼만 제출하면 403이다. 그제야 깨닫는다. **CSRF를 disable했으니 폼에 있던 hidden CSRF 토큰도 의미가 사라졌고, 동시에 폼 로그인 자체가 토큰 없이 동작하도록 무방비가 된 게 아니라 — 정확히는 polling 동작에서 토큰 검증을 우회하긴 했지만 — 다른 모든 폼 기반 POST가 일관성을 잃었구나.** 더 큰 문제는 운영자 화면이 stateful 흐름이라는 사실이다. 거기는 CSRF가 켜져 있어야 한다.

잠깐, 헷갈리니까 다시 정리하자. `csrf.disable()`은 전체 체인에 적용된다. SPA용 API 경로와 운영자용 폼 페이지가 같은 `SecurityFilterChain` 안에 있으면, disable은 둘 다 영향을 준다. SPA에서는 문제가 없지만(어차피 Bearer로 가니까), 폼 쪽은 보호가 사라진다. 보호가 사라진 채로 동작이 멈춰 보이는 이유는, Spring Security 6 이후의 일부 흐름에서 CSRF가 꺼지면 폼 로그인 자체의 hidden 토큰 처리 경로가 어긋나며 의도치 않은 redirect나 403 응답을 만들기 때문이다. 어쨌든 결과는 같다. 폼 로그인이 깨진다. 찜찜하다.

그렇다면 어떻게 해야 할까. 답은 7장에서 이미 깔아둔 패턴이다. **체인을 두 개로 분리한다.**

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .csrf(c -> c.disable())
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}

@Bean
@Order(2)
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .csrf(Customizer.withDefaults())
        .authorizeHttpRequests(a -> a
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .build();
}
```

`/api/**`는 stateless·JWT·CSRF disable, 그 외 웹 경로는 stateful·세션·CSRF enable. 두 체인은 같은 애플리케이션 안에 공존하지만 서로의 결정을 침범하지 않는다. 이 구조가 자리 잡으면 "CSRF disable로 폼 로그인이 깨지는" 상황은 다시 일어나지 않는다. 기억해두자. CSRF는 체인 단위 결정이고, 체인을 분리하면 결정도 분리된다.

### 7.0의 한 줄 단축 — `csrf(CsrfConfigurer::spa)`

여기까지 따라온 독자라면 한 가지 질문이 떠오를 것이다. "SPA가 쿠키 세션을 쓰는 경우는 어떻게 하지?" BFF 패턴이 대표적이다. SPA에서 직접 JWT를 가지고 다니는 대신, 서버가 세션 쿠키를 두고 토큰은 서버 안에 가둬두는 구조. 이 경우 SPA는 쿠키로 인증하니까 CSRF가 필요하다. 그런데 JS로 동작하는 SPA에서 hidden form 토큰 패턴은 어울리지 않는다. 헤더로 토큰을 실어 보내야 한다.

이 시나리오를 위해 6.x에서는 `CookieCsrfTokenRepository.withHttpOnlyFalse()`를 등록해 토큰을 JS가 읽을 수 있는 쿠키로 내려주고, 별도의 `CsrfTokenRequestAttributeHandler`/`XorCsrfTokenRequestAttributeHandler`를 손수 조립해 헤더 검증 흐름을 구성해야 했다. 한두 줄로 끝나지 않고, 클래스 이름도 길고, 미묘한 버그가 자주 났다. 번거롭다.

7.0이 이 묶음을 한 줄로 정리해줬다.

```java
http.csrf(CsrfConfigurer::spa);
```

이 한 줄이 무엇을 대체하는지 풀어두자.

```java
// 한 줄이 대체하는 것
http.csrf(c -> c
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
    .csrfTokenRequestHandler(new SpaCsrfTokenRequestHandler()));
```

`CookieCsrfTokenRepository.withHttpOnlyFalse()`는 토큰을 `XSRF-TOKEN`이라는 쿠키로 내려주되, HttpOnly를 끄기 때문에 JS가 읽을 수 있다. SPA는 이 쿠키를 읽어 `X-XSRF-TOKEN` 헤더에 실어 다음 요청에 붙인다. `SpaCsrfTokenRequestHandler`는 그 헤더 값을 검증한다. 이 두 가지가 SPA의 표준 패턴 — 흔히 "double submit cookie"라고 부르는 — 의 Spring Security식 구현이다.

7.0의 한 줄 단축은 이 묶음에 이름을 붙여준 셈이다. 코드를 읽는 사람이 "아, 이 체인은 SPA 패턴이구나"를 즉시 알아본다. 한 줄의 의미가 그렇게 크다. 새로 시작하는 BFF 프로젝트라면 `csrf(CsrfConfigurer::spa)`로 시작하는 편이 낫다.

물론 한 줄로 모든 SPA 시나리오가 풀리는 건 아니다. 도메인이 분리된 경우 — 즉 SPA가 `app.example.com`, API가 `api.example.com`처럼 다른 호스트일 때 — 쿠키 도메인 설정을 신경 써야 한다. 쿠키 도메인이 맞지 않으면 SPA가 토큰 쿠키를 읽지 못한다. 또한 SameSite 속성이 `Strict`이면 cross-origin SPA에서 쿠키가 전송되지 않을 수 있다. 이 부분은 10장의 쿠키 절에서 더 자세히 본다. 일단은 "같은 도메인의 BFF"라면 한 줄로 충분하다는 것만 기억해두자.

## 보안 헤더 — `HeaderWriterFilter`가 알아서 써주는 것들

이제 셋 중 마지막이다. 보안 헤더는 응답에 한두 줄 더 붙는 것뿐이지만, 그 한 줄이 막아주는 공격의 범위는 꽤 넓다. 그리고 다행히도 Spring Security는 기본값만으로도 합리적인 헤더를 자동으로 써준다. `HeaderWriterFilter`라는 필터가 응답이 나갈 때마다 정해진 헤더를 끼워 넣는다.

기본으로 붙는 헤더는 대략 다음과 같다. `Cache-Control: no-cache, no-store, max-age=0, must-revalidate`, `Pragma: no-cache`, `Expires: 0`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security: max-age=...`(HTTPS 응답에 한해), `Referrer-Policy: no-referrer`(7.0 기본은 `strict-origin-when-cross-origin`으로 바뀌었다는 점도 챙겨두자, 사실 확인 필요). 이 정도면 OWASP Top 10의 A05(Security Misconfiguration)에서 자주 지적되는 항목들이 즉시 채워진다.

하지만 기본값이 늘 옳은 건 아니다. 환경에 따라 끄거나 바꿔야 하는 헤더도 있다. 하나씩 살펴보자.

### HSTS — 한 번 잘못 켜면 며칠을 고생한다

`Strict-Transport-Security`(HSTS)는 브라우저에게 "이 도메인은 앞으로 HTTPS로만 접속해"라고 명령하는 헤더다. 한 번이라도 받은 브라우저는 그 도메인에 대해 HTTP 접속을 자동으로 HTTPS로 바꿔준다. 평문 통신을 강제로 차단하는 강력한 도구다.

문제는 이 명령에 유효기간(`max-age`)이 있다는 점이고, 더 큰 문제는 그게 브라우저에 캐시된다는 점이다. 운영 환경에서야 좋은 일이다. 그러나 개발 환경에서는 한 번 잘못 쓴 HSTS가 브라우저에 남아 며칠을 고생시킨다. 로컬에서 HTTPS로 실험하다가 HSTS 헤더를 받은 브라우저는, 그날 이후로 `http://localhost:8080`을 입력해도 자동으로 `https://localhost:8080`으로 바꿔버린다. 인증서가 없는 dev 환경에서는 그대로 접근 불가가 된다. 끔찍한 일이다.

게다가 `includeSubDomains` 옵션을 켠 채로 회사 도메인 본 사이트에서 HSTS를 받으면, 그 안의 모든 서브도메인이 HTTPS 강제 대상이 된다. dev 서브도메인까지 막혀버린다. 캐시는 브라우저별·기기별로 살아 있어서, 팀원 전체가 같은 시점에 같은 증상을 겪지 않으니 디버깅도 어렵다.

그렇다면 어떻게 해야 할까. 두 가지를 기억해두자.

첫째, **개발 환경 프로파일에서는 HSTS를 끈다.** 

```java
@Configuration
@Profile("dev")
class DevSecurityHeaders {
    @Bean
    SecurityFilterChain dev(HttpSecurity http) throws Exception {
        return http
            .headers(h -> h.httpStrictTransportSecurity(hsts -> hsts.disable()))
            // ... 나머지 설정
            .build();
    }
}
```

둘째, **프로덕션에서도 `includeSubDomains`와 `preload`는 도메인 전체 정책을 확신한 다음에 켠다.** 한 번 preload 목록에 올라가면 되돌리기가 매우 어렵다. 캐시 시간을 처음에는 짧게 — 하루나 일주일 — 잡고, 안정화된 다음 1년으로 늘리는 편이 안전하다.

HSTS는 강한 도구다. 강한 도구는 천천히 휘둘러야 한다.

### X-Frame-Options와 Content-Security-Policy의 frame-ancestors

`X-Frame-Options: DENY`는 우리 페이지가 다른 사이트의 `<iframe>` 안에서 렌더링되는 것을 막는다. clickjacking 방어다. 공격자가 우리 페이지를 투명한 iframe으로 띄우고 그 위에 미끼 버튼을 겹쳐 두면, 사용자가 미끼를 누르는 순간 사실은 우리 페이지의 진짜 버튼이 눌린다. 송금 버튼이거나 권한 변경 버튼이면 큰일이다.

기본값 `DENY`는 가장 안전하다. 어떤 도메인이든 iframe으로 띄우지 못하게 한다. 같은 출처 안에서는 띄워야 한다면 `SAMEORIGIN`으로, 특정 신뢰 도메인에서만 띄우게 하려면 CSP의 `frame-ancestors` 지시어를 같이 쓴다. `X-Frame-Options`는 단일 도메인 화이트리스트가 안 되지만, `frame-ancestors`는 여러 도메인을 받는다. 현대 브라우저는 둘 다 인식하므로, 신뢰 iframe 호스트가 두 개 이상이면 CSP 쪽에 명세를 두고 `X-Frame-Options`는 그대로 두는 편이 낫다.

### Referrer-Policy

`Referrer-Policy`는 사용자가 우리 사이트의 링크를 눌러 외부 사이트로 이동할 때, 어디서 왔는지를 외부에 얼마나 알려줄지를 정한다. 기본값 `no-referrer`는 아무것도 알리지 않는다. 강한 정책이지만 분석 도구나 정상적인 인바운드 트래킹이 깨질 수 있다. 7.0에서 기본값이 완화 방향(`strict-origin-when-cross-origin`)으로 옮겨갔다면(사실 확인 필요), 동일 출처일 때만 전체 URL을 보내고 외부로 갈 때는 출처(origin)만 보내는 절충안이다. 운영자가 명시적으로 정해두는 편이 좋다.

### Permissions-Policy

`Permissions-Policy`는 이전의 `Feature-Policy`를 이어받은 헤더다. 브라우저 기능 — 카메라, 마이크, 지오로케이션, USB 등 — 을 페이지가 사용하지 못하도록 막거나 특정 출처에만 허용한다. 우리 페이지가 카메라를 쓸 일이 없다면 `camera=()`처럼 비워두는 편이 낫다. iframe으로 들어온 외부 위젯이 사용자에게 카메라 권한을 요구하는 사고를 막아준다.

```java
http.headers(h -> h
    .permissionsPolicyHeader(p -> p
        .policy("camera=(), microphone=(), geolocation=(self)")));
```

이 헤더의 핵심은 명시성이다. "우리는 이런 기능을 쓰지 않는다"는 선언이 곧 방어다.

### Content-Security-Policy — 정책은 앱이 결정한다

CSP는 보안 헤더 중 가장 강력하면서도 가장 다루기 어려운 헤더다. 어떤 스크립트·스타일·이미지를 어디서 불러올 수 있는지, 인라인 스크립트를 허용할지, eval을 허용할지 등을 세밀하게 정한다. XSS의 영향을 크게 줄이는 도구다.

여기서 분명히 해둘 게 있다. **Spring Security는 CSP 헤더를 _작성_ 해줄 뿐, 정책 _내용_ 은 앱이 결정한다.** 어떤 도메인의 CDN을 쓰는지, 어떤 분석 스크립트를 임베드하는지, Webpack hash를 쓸지 nonce를 쓸지 — 이건 모두 애플리케이션의 정책 결정이다. Security는 그 결정을 헤더 한 줄로 옮겨주는 도구다.

```java
http.headers(h -> h
    .contentSecurityPolicy(csp -> csp
        .policyDirectives(
            "default-src 'self'; " +
            "script-src 'self' 'nonce-{NONCE}' https://cdn.example.com; " +
            "style-src 'self' 'unsafe-inline'; " +
            "img-src 'self' data: https:; " +
            "object-src 'none'; " +
            "frame-ancestors 'none'; " +
            "base-uri 'self'")));
```

이 정책을 짜는 일은 보안 엔지니어와 프런트엔드 엔지니어가 함께 머리를 맞대는 작업이다. 처음에는 `Content-Security-Policy-Report-Only`로 띄워두고 위반 리포트를 받아서 점진적으로 좁혀가는 편이 안전하다. 한 번에 강한 정책을 던지면 사이트의 절반이 깨진다. 진짜 끔찍한 일이다.

### CSP nonce / hash — 인라인 스크립트와의 타협

CSP를 강하게 쓰려면 인라인 스크립트와 인라인 스타일을 막아야 한다. 그러나 현실에서 모든 인라인을 제거하기는 어렵다. 그래서 두 가지 우회 도구가 있다.

**nonce**는 요청마다 생성한 일회용 토큰을 응답 헤더의 CSP와 HTML 인라인 스크립트 양쪽에 같이 적어두는 방식이다. 같은 nonce를 가진 스크립트만 실행된다. 매 응답마다 nonce가 바뀌므로 공격자가 인라인 스크립트를 주입해도 nonce를 맞출 수 없다.

**hash**는 인라인 스크립트의 SHA-256 해시를 미리 계산해 CSP에 등록하는 방식이다. 정적인 인라인 스크립트라면 hash가 적합하고, 동적이라면 nonce가 적합하다.

Spring Security 7.0에는 nonce와 hash 패턴을 지원하기 위한 인프라가 정비되고 있다(사실 확인 필요 — 정확한 API 시그니처는 공식 레퍼런스를 보자). 이 책에서는 깊이 파고들지 않지만, CSP를 본격적으로 도입한다면 nonce 패턴을 익혀두는 편이 낫다.

### 정리: 헤더 한 줄이 무엇을 바꾸는가

보안 헤더는 응답에 글자 몇 개를 더하는 것뿐이다. 그러나 그 한 줄이 brower의 동작 자체를 바꾼다. iframe을 못 띄우게 하고, HTTPS만 쓰게 하고, 외부 CDN의 스크립트를 막아준다. 코드 한 줄도 추가하지 않고 공격 표면이 좁아진다.

기본값이 합리적이라는 게 Spring Security의 큰 미덕이다. 다만 환경에 맞게 조정해야 하는 것들 — HSTS는 dev에서 끄고, CSP는 정책을 직접 정하고, Permissions-Policy는 쓰지 않는 기능을 명시적으로 비우자 — 만큼은 잊지 말자.

## HTTPS와 TLS 운영 — 리버스 프록시 뒤에서 새는 자리

마지막으로 운영 환경의 HTTPS 이야기를 짧게 짚고 가자. 보안 헤더의 HSTS도, CSP의 `upgrade-insecure-requests`도, 모두 HTTPS가 전제다. 그런데 정작 우리 애플리케이션은 HTTPS로 직접 청취하지 않는 경우가 많다. Nginx, AWS ALB, Cloudflare가 앞에 서서 TLS를 종료하고, 우리 Spring Boot는 그 뒤에서 평문 HTTP로 요청을 받는다. 이 구조에서 보안 결정을 잘못 내리면 미묘하게 새는 자리가 생긴다.

### `requiresChannel` — HTTPS 강제 리다이렉트

가장 단순한 도구부터 보자. Spring Security에는 채널 — 즉 요청이 들어온 스킴 — 을 강제하는 설정이 있다.

```java
http.requiresChannel(c -> c.anyRequest().requiresSecure());
```

이 한 줄을 켜면 HTTP로 들어온 요청은 HTTPS로 redirect된다. 그런데 여기서 첫 번째 함정이 등장한다. 리버스 프록시 뒤에서는 Spring Boot가 받는 요청 자체가 평문 HTTP로 보이기 때문이다. 프록시가 TLS를 종료했으니 당연하다. 그러면 `requiresChannel`이 모든 요청을 HTTPS로 redirect하려고 하고, 그 redirect도 평문이므로 또 들어오고… 무한 루프다. 난감하다.

해법은 두 갈래다. 하나는 **프록시에서 HTTPS 강제를 하고 애플리케이션에서는 켜지 않는** 방식이다. 가장 단순하다. 다른 하나는 **프록시가 `X-Forwarded-Proto: https` 헤더를 붙이도록 하고, Spring Boot가 그 헤더를 읽도록 설정하는** 방식이다. 이 헤더가 보이면 `ServletRequest.isSecure()`가 `true`를 반환하므로 redirect 루프가 풀린다.

### `X-Forwarded-*` 헤더와 `ForwardedHeaderFilter`

`X-Forwarded-Proto`, `X-Forwarded-For`, `X-Forwarded-Host`는 리버스 프록시가 원본 요청의 정보를 뒷단에 알려주는 표준 비공식 헤더 묶음이다. 비공식이라고는 하지만 사실상 표준이며, RFC 7239가 정식화된 `Forwarded` 헤더로 통합하려 하고 있다(사실 확인 필요).

Spring Boot에서 이 헤더를 신뢰하도록 하려면 두 가지 방법이 있다. application.yml에 `server.forward-headers-strategy=framework`(또는 `native`)를 설정하거나, `ForwardedHeaderFilter`를 직접 빈으로 등록하는 방법이다.

```yaml
server:
  forward-headers-strategy: framework
```

이 설정 한 줄이 켜지면 Spring MVC의 요청 객체는 프록시 이전의 원본 스킴·호스트·IP를 그대로 보여준다. Spring Security는 그 위에서 자연스럽게 동작한다. `requiresChannel`도, redirect URL 생성도, 로그인 후 리다이렉트 URL 결정도 모두 원본 정보를 기준으로 돌아간다.

여기서 한 가지 주의해야 한다. `X-Forwarded-*` 헤더는 클라이언트가 직접 보낼 수도 있다. 신뢰할 수 없는 클라이언트가 헤더를 위조해 보내면 Spring Boot는 그걸 믿고 잘못된 결정을 내릴 수 있다. 그래서 이 설정은 **반드시 신뢰할 수 있는 프록시 뒤에서만** 켠다. 그리고 프록시는 자신을 거치는 요청의 `X-Forwarded-*` 헤더를 매번 다시 써주도록 설정해야 한다. 클라이언트가 보낸 값을 그대로 통과시키지 않게.

### `LoginUrlAuthenticationEntryPoint`의 상대 경로 리다이렉트

리버스 프록시 환경에서 미묘하게 새는 또 하나의 자리가 `LoginUrlAuthenticationEntryPoint`다. 인증되지 않은 사용자가 보호 자원을 요청하면 이 진입점이 로그인 페이지로 redirect를 보내는데, 이때 redirect URL을 절대 URL로 만들지 상대 URL로 만들지가 환경에 따라 다르게 동작한다.

만약 절대 URL을 만든다면 Spring Boot가 보고 있는 스킴·호스트가 redirect Location 헤더에 박힌다. 프록시 뒤에서 `X-Forwarded-*` 처리를 안 했다면 `http://internal-host:8080/login` 같은 내부 주소가 그대로 클라이언트로 갈 수도 있다. 클라이언트는 그 URL을 따라가다 끊긴다.

해법은 두 가지다. 하나는 위에서 본 `server.forward-headers-strategy`를 켜서 원본 정보 기반으로 redirect URL이 만들어지도록 하는 것이다. 다른 하나는 **redirect를 상대 경로로** 보내도록 하는 것이다. Spring Security에는 절대/상대 redirect를 제어하는 옵션이 있다(사실 확인 필요 — 7.0의 구체적 API명). 상대 경로 redirect는 프록시·호스트 환경에 의존하지 않으므로 다중 프록시 구조에서 가장 안전하다.

### 운영 체크리스트

인증서 관리 — 발급, 회전, OCSP stapling — 는 이 책의 범위 밖이다. 그러나 Spring Boot 운영자가 HTTPS와 관련해 챙겨야 할 체크리스트는 짚고 가는 편이 낫다.

첫째, **TLS 종료 위치를 분명히 한다.** 프록시인가, 애플리케이션인가. 둘 다인가? 둘 다 종료한다면 mTLS 같은 특수 시나리오가 아니면 보통 비효율이다.

둘째, **`X-Forwarded-*` 헤더의 신뢰 경계를 정한다.** 프록시 뒤에서만 신뢰하고, 직접 외부에 노출된 인스턴스에서는 끈다. 신뢰 경계가 흐려지면 redirect URL이나 IP 기반 결정이 모두 위장 대상이 된다.

셋째, **HSTS를 켜되 환경별로 분리한다.** dev에서는 끄고, staging에서는 짧게, prod에서는 길게.

넷째, **인증서 만료를 자동 모니터링한다.** Let's Encrypt를 쓴다면 90일 자동 갱신 파이프라인이 잘 돌아가는지 정기 점검. 인증서 만료는 가장 흔한 자해 사고다.

다섯째, **TLS 버전을 1.2 이상으로 강제한다.** 1.0/1.1은 이미 비표준화되었다. 프록시 설정에서 명시적으로 제한해두는 편이 안전하다.

여섯째, **세션 쿠키에 `Secure` 플래그를 켠다.** HTTPS에서만 쿠키가 전송된다. 10장 쿠키 절에서 다시 짚는다.

운영 환경의 HTTPS는 코드보다 인프라 결정의 영역이 크다. 그러나 그 결정들이 결국 Spring Security의 동작에 영향을 준다는 점을 알아두면, 로그인 redirect가 이상하게 도는 날 가장 먼저 어디를 봐야 할지 안다.

## 마무리

가장 헷갈리는 셋을 정리해보자.

**CORS는 Security보다 먼저.** preflight OPTIONS 요청이 인증을 요구받지 않도록 `http.cors(...)` + `CorsConfigurationSource` 빈을 묶음으로 둔다. allowedOrigins는 명시하고, OPTIONS를 메서드에 꼭 포함시키자.

**CSRF는 쿠키 흐름에서 켠다.** Bearer 토큰 API는 disable해도 안전하지만, 같은 체인에 폼 로그인이 섞이지 않게 체인을 분리하자. 7.0의 `csrf(CsrfConfigurer::spa)` 한 줄은 BFF·SPA 시나리오의 표준이 된다.

**보안 헤더는 기본값이 합리적이다.** 그러나 HSTS는 dev에서 끄고, CSP의 정책은 앱이 직접 정하고, Permissions-Policy로 쓰지 않는 기능을 명시적으로 비워두자. 한 번 잘못 켠 HSTS가 며칠을 고생시킨다는 사실은 잊지 말자.

**HTTPS는 종료 위치와 `X-Forwarded-*` 신뢰 경계로 결정된다.** `server.forward-headers-strategy`를 켜서 Spring Boot가 원본 스킴을 보게 만들고, `requiresChannel`은 프록시 환경에서 신중하게 쓰자.

이 셋을 한 줄로 다시 정리하면, **"CORS는 미리 통과시키고, CSRF는 흐름에 맞게 켜고, 보안 헤더는 기본을 신뢰하되 환경에 맞게 조정한다."** 처음 들었을 때는 추상적이던 그 한 줄이, 이제는 실제 코드와 함정과 함께 떠오를 것이다.

다음 장에서는 이 장에서 살짝 비춰둔 세션과 쿠키의 세계를 본격적으로 다룬다. `sessionCreationPolicy`의 네 가지 모드, `requireExplicitSave`의 7.0 권고 기본, `HttpOnly`·`Secure`·`SameSite` 쿠키 속성, 그리고 비동기 컨텍스트 전파에서 발생하는 미묘한 누수까지. 상태가 있을 때와 없을 때 코드가 어떻게 갈라지는지를 모서리까지 따라가 보자.
