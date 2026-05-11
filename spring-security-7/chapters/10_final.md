# 10장. 세션·쿠키·컨텍스트 전파 — 상태 관리의 모든 모서리

> 선행 필요: 2장(필터 체인), 3장(컴포넌트 모델), 4장(폼 로그인)

상태가 있다는 것은 비용이지만, 상태가 없다는 것 또한 다른 비용이다. 한쪽에는 세션이라는 무거운 짐을 들고 가는 길이 있고, 다른 한쪽에는 매 요청마다 토큰을 재검증해야 하는 가벼우면서도 만만치 않은 길이 있다. 어느 길이 우리 시스템에 맞는지 결정하는 일은 단순한 취향의 문제가 아니다. 어떤 모서리에서 어떤 누수가 일어나는지 알고 결정해야 한다.

이런 상황을 한번 상상해보자. 한 사용자가 결제를 진행하던 중 결제 결과를 비동기로 후처리하는 메서드가 호출됐다. `@Async`로 묶인 평범한 메서드다. 그런데 어느 날 운영 환경에서 이상한 로그가 찍힌다. 사용자 A의 결제 요청에서 시작된 비동기 작업이, 사용자 B의 권한으로 감사 로그에 기록된 것이다. 코드는 분명히 멀쩡해 보이는데 어떻게 이런 일이 벌어졌을까? 답을 알고 나면 모골이 송연해진다. 그리고 이 답은 이 장 후반부에 정확히 같은 코드 패턴으로 재현해볼 것이다.

세션 정책 한 줄, 쿠키 속성 하나, `SecurityContextHolder`의 전략 모드 하나가 시스템 전체의 안전성과 사용성을 가른다. 작은 결정처럼 보이지만 잘못 고르면 그 비용은 절대 작지 않다. 하나씩 모서리를 따라가며 살펴보자.

## 세션을 가질 것인가 말 것인가 — `sessionCreationPolicy`

먼저 가장 자주 마주치게 되는 한 줄부터 보자. 4장과 5장에서 무심코 적었던 그 한 줄이다.

```java
http.sessionManagement(s -> s.sessionCreationPolicy(STATELESS));
```

`STATELESS`. 이름만 보면 "세션을 안 쓴다"는 뜻 같다. 그런데 정확히 무엇을 안 쓴다는 걸까? `HttpSession` 자체가 안 만들어지는 걸까, 아니면 만들어지긴 하는데 보안 컨텍스트만 저장하지 않는 걸까? 그리고 `STATELESS`가 있다는 건, 그 반대편에 다른 모드들도 있다는 뜻이다. 어떤 모드들이 있고 어떻게 다를까?

Spring Security가 제공하는 정책은 모두 네 가지다.

| 정책 | 의미 | 주요 사용처 |
|------|------|------------|
| `ALWAYS` | 세션이 없으면 무조건 만든다 | 매우 드물다. 익명 요청에도 세션이 필요한 특수 케이스 |
| `IF_REQUIRED` (기본값) | 필요할 때만 만든다 | 폼 로그인 등 전통적인 웹 앱 |
| `NEVER` | Spring Security는 세션을 만들지 않지만, 다른 곳에서 이미 만들어져 있으면 사용한다 | 외부 시스템이 세션을 관리하는 혼합 환경 |
| `STATELESS` | 세션을 만들지도, 사용하지도 않는다 | JWT 자원 서버, HTTP Basic API |

핵심은 `NEVER`와 `STATELESS`의 차이다. 이 둘을 헷갈리는 경우가 의외로 많다. `NEVER`는 "Security가 적극적으로 세션을 만들진 않겠다"는 소극적 자세고, `STATELESS`는 "어떤 경우에도 세션이라는 개념 자체를 외면하겠다"는 강한 선언이다. 자원 서버에서 무심코 `NEVER`를 골랐다가, 다른 필터나 인터셉터가 세션을 한 번 만들어 두면 그 세션을 그대로 들고 가게 된다. 이런 미묘한 누수가 실제로 일어난다. JWT API라면 망설임 없이 `STATELESS`를 고르는 편이 낫다.

그렇다면 `IF_REQUIRED`는 언제 세션을 만들까? 답은 단순하다. 인증이 성공해 `SecurityContext`를 저장해야 할 때다. 익명 요청은 컨텍스트가 비어 있으니 세션을 안 만들고, 폼 로그인이 성공해 채워진 컨텍스트가 생기는 순간 세션이 생긴다. 4장에서 본 폼 로그인의 가장 평범한 흐름이 바로 이 정책 위에서 돌아간다. 별다른 설정을 안 하면 이게 기본이라는 점을 기억해두자.

### `HttpSessionSecurityContextRepository`가 하는 일

세션을 만든다고 끝이 아니다. 그 세션에 무엇이 어떻게 저장되는지를 책임지는 컴포넌트가 따로 있다. 이름이 길지만 한 번 보면 잊히지 않는다. `HttpSessionSecurityContextRepository`다.

이 저장소가 하는 일을 그림으로 그려보자.

- **요청이 들어올 때:** `SecurityContextHolderFilter`(과거의 `SecurityContextPersistenceFilter`)가 세션에서 `SPRING_SECURITY_CONTEXT` 키로 컨텍스트를 꺼내 `SecurityContextHolder`에 채워 넣는다.
- **요청이 끝날 때:** 응답이 클라이언트로 나가기 직전, 같은 키로 컨텍스트를 다시 세션에 저장한다.

이 단순한 사이클이 우리가 일상적으로 의지하는 "한 번 로그인하면 다음 요청에도 인증 상태가 유지된다"는 마법의 정체다. 마법은 보통 너무 자연스럽게 작동해서 그 존재 자체를 잊게 만드는데, 바로 그 자연스러움이 함정이기도 하다. 6.x까지의 기본 동작에는 한 가지 미묘한 문제가 숨어 있었기 때문이다.

### `requireExplicitSave(true)` — 7.0이 권장하는 새 기본

문제는 이런 것이었다. 컨텍스트가 언제 저장되는가? 답은 "응답이 나갈 때 자동으로". 좋게 들리지만, 자세히 보면 살짝 찜찜한 구석이 있다. "응답이 나갈 때"라는 시점은 필터 체인의 모든 후처리가 끝난 한참 뒤다. 그 사이에 누군가 `SecurityContextHolder`를 건드려 컨텍스트를 갱신했다면, 그 갱신이 자동 저장의 대상이 된다. 의도한 갱신이라면 좋겠지만, 의도하지 않은 사이드 이펙트라면? 또는 같은 요청 안에서 컨텍스트를 여러 번 바꿨는데 마지막 상태만 저장된다면?

더 큰 문제는 `STATELESS` 시나리오에서 일어났다. JWT 자원 서버를 만들면서 매 요청마다 토큰을 디코드해 컨텍스트를 채우는 코드를 짰다고 해보자. 무심코 `securityContext()` 설정을 안 건드리면, Spring Security는 "세션은 안 만들지만, 혹시 모르니 컨텍스트는 알아서 저장할 준비를 해두는" 흐름으로 갔다. 결과적으로 `STATELESS`라는 이름과 달리 어딘가에서 컨텍스트가 새는 듯한 동작이 일어나곤 했다.

Spring Security 6.x 후반부터 권장하기 시작했고 7.0에서 사실상 기본이 된 답이 바로 이것이다.

```java
http.securityContext(s -> s.requireExplicitSave(true));
```

이 한 줄이 무엇을 바꾸는가? **컨텍스트 저장은 명시적으로만 일어난다.** 더 이상 응답이 나갈 때 자동으로 저장되지 않는다. 저장하고 싶으면 `SecurityContextRepository.saveContext(...)`를 직접 호출하거나, 인증 필터가 알아서 저장 로직을 책임진다. 이 변화는 두 가지 의미를 가진다.

첫째, 의도가 코드에 드러난다. "어, 이건 누가 저장한 거지?"라는 의문이 사라진다. 둘째, `STATELESS` 흐름이 진짜 stateless다워진다. 자원 서버는 매 요청마다 새 컨텍스트를 만들 뿐, 어디에도 보관하지 않는다.

HTTP Basic 인증을 stateless하게 운영하고 싶다면 4장에서 본 그 조합을 다시 떠올려보자.

```java
http
    .httpBasic(Customizer.withDefaults())
    .securityContext(s -> s.requireExplicitSave(true))
    .sessionManagement(s -> s.sessionCreationPolicy(STATELESS));
```

이 세 줄이 함께 가야 진짜 매 요청 인증이 된다. 한 줄만 빠지면 미묘하게 stateful한 동작이 끼어든다. 기억해두자.

### 두 모드를 한 시스템에 — 두 개의 `SecurityFilterChain`

실무에서 흔히 마주치는 시나리오를 하나 짚어보자. 같은 애플리케이션이 두 가지 인터페이스를 동시에 제공한다. 관리자용 웹 UI는 폼 로그인 + 세션을, 외부 API는 JWT + stateless를 쓴다. 한 `SecurityFilterChain`으로 양쪽 정책을 다 만족시키려고 하면 결국 둘 다 어색해진다. 어떻게 해야 할까?

답은 8장과 5장에서 이미 살짝 봤다. **두 개의 체인을 만들자.**

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
        .securityContext(s -> s.requireExplicitSave(true))
        .build();
}

@Bean
@Order(2)
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .csrf(Customizer.withDefaults())
        // sessionManagement는 기본값 IF_REQUIRED — 그대로 둔다
        .build();
}
```

두 체인은 서로의 정책을 침범하지 않는다. `/api/**`로 들어오는 요청은 첫 번째 체인이 매칭해 stateless하게 처리하고, 그 외 요청은 두 번째 체인이 stateful하게 처리한다. 한 시스템 안에 세션 정책이 둘인 셈이다. 이런 분리가 가능하다는 점이 Spring Security의 큰 자산이다. 2장 후반에서 강조한 "Only the first matching filter chain is invoked"라는 원칙이 여기서 빛을 발한다.

## 세션 고정 공격과 보호 모드

세션이 있다는 건 그 세션을 노리는 공격도 있다는 뜻이다. 가장 고전적이면서도 여전히 유효한 것이 **세션 고정 공격**이다. 들어본 듯 안 들어본 듯한 이름이지만, 원리는 단순하다.

상상해보자. 공격자가 우리 서비스에 먼저 접속해 익명 세션ID 하나를 발급받는다. 그러고는 그 세션ID를 어떻게든 피해자의 브라우저에 심어 둔다(피싱 링크나 XSS 등으로). 피해자가 그 세션ID 그대로 우리 서비스에 로그인하면, 서버는 "아, 이 세션ID로 로그인한 사용자구나" 하고 그 세션에 인증 정보를 채워 넣는다. 공격자는 처음부터 그 세션ID를 알고 있었으니, 이제 그 세션ID로 피해자 행세를 하며 들어올 수 있다. 끔찍한 일이다.

이 공격을 막는 방법은 명확하다. **로그인 성공 순간, 세션을 새로 갈아치우는 것이다.** 공격자가 알고 있던 세션ID는 이제 유효한 인증 정보가 없는 빈 껍데기가 되고, 피해자에게는 새로 발급된 세션ID가 쥐어진다. 이 동작을 Spring Security가 어떻게 제공하는지 살펴보자.

`sessionManagement().sessionFixation()`에는 네 가지 모드가 있다.

| 모드 | 동작 |
|------|------|
| `migrateSession()` (기본값) | 기존 세션의 속성들을 새 세션으로 복사하고 기존 세션은 무효화 |
| `newSession()` | 완전히 새 세션을 만든다. 기존 속성도 안 가져온다 |
| `changeSessionId()` | 세션 객체는 그대로 두고 ID만 갈아낀다 (Servlet 3.1+) |
| `none()` | 아무것도 안 한다. **공격에 그대로 노출** |

기본이 `migrateSession()`이라는 점은 다행이다. 별다른 설정 없이도 안전하다. 그렇다면 이 모드들 사이의 차이는 무엇일까?

`changeSessionId()`는 가장 가볍다. 세션 자체는 그대로니까 안에 담긴 속성도 그대로 살아 있다. 컨테이너가 ID만 바꿔주면 끝이다. `migrateSession()`은 안전한 기본 동작이지만, 새 세션을 만들고 속성을 복사하는 비용이 추가로 든다. `newSession()`은 가장 깔끔하지만, 로그인 전에 세션에 담아두던 정보가 있었다면(예: 장바구니, 로그인 후 돌아갈 URL) 그 정보를 잃는다.

`none()`은 어떤 경우에 쓸까? 정직하게 말하면, 쓸 일이 거의 없다. 외부 시스템이 세션 ID 관리를 책임지는 매우 특수한 통합 시나리오 정도다. **커스텀 세션 관리를 짜다가 무심코 `none()`을 켜는 실수**는 함정 12로 분류될 만큼 흔하다. 정말 이 모드가 필요한지 한 번 더 의심해보는 편이 낫다.

## 동시 세션을 어떻게 다스릴 것인가

한 사용자가 한 계정으로 여러 디바이스에서 동시에 접속한다. 이 상황을 어떻게 다룰 것인가? 답은 도메인에 따라 갈린다.

은행이나 결제 시스템처럼 보안이 무거운 도메인은 "한 사람당 한 세션만"이 합리적이다. 다른 디바이스에서 로그인하면 기존 세션을 끊는다. 반대로 동영상 스트리밍이나 협업 도구 같은 서비스는 멀티 디바이스가 당연한 사용 패턴이다. 어느 쪽이든 Spring Security는 도구를 제공한다.

```java
http.sessionManagement(s -> s
    .maximumSessions(1)
    .maxSessionsPreventsLogin(false)
    .expiredUrl("/login?expired"));
```

이 짧은 설정이 무엇을 의미하는지 한 줄씩 풀어보자. `maximumSessions(1)`은 한 사용자당 활성 세션 수를 1로 제한한다. `maxSessionsPreventsLogin(false)`는 "초과될 때 어떻게 할 것인가"를 정한다. `false`면 새 로그인을 허용하고 가장 오래된 세션을 만료시킨다. `true`로 두면 반대다 — 이미 세션이 있으면 새 로그인을 차단한다. `expiredUrl`은 만료당한 세션이 다음 요청을 보냈을 때 리다이렉트할 위치다.

`true`와 `false` 어느 쪽이 좋을까? 트레이드오프가 있다. `true`는 보안적으로 살짝 더 안전하다 — 이미 로그인된 정상 사용자를 보호하니까. 하지만 사용성이 떨어진다. 사용자가 다른 곳에서 로그아웃을 안 하고 자리를 떴다면, 다음에 다시 들어올 때 "이미 로그인되어 있다"는 거부 메시지를 만나야 한다. 사용자는 자기가 어디서 로그인했는지 기억 못 한다. 보통은 `false`가 무난하다.

여기서 한 가지 짚어둘 점이 있다. 동시 세션 제어가 동작하려면 Spring Security가 세션의 생성·소멸을 추적할 수 있어야 한다. 이를 위해 `HttpSessionEventPublisher`라는 리스너 빈을 등록해야 한다.

```java
@Bean
HttpSessionEventPublisher httpSessionEventPublisher() {
    return new HttpSessionEventPublisher();
}
```

이 빈을 빼먹으면 `maximumSessions` 설정이 조용히 무력화된다. 빌드는 되고 로그도 안 찍히는데 동작만 안 한다. 정말 찜찜한 종류의 실수다. 이 빈은 꼭 함께 등록하자.

## 쿠키 — 작지만 까다로운 모서리

세션이 살아 움직이려면 결국 쿠키가 있어야 한다. 서버는 `JSESSIONID`라는 쿠키로 브라우저와 세션 ID를 주고받는다. 그리고 이 쿠키 한 줄에 붙는 속성 몇 개가 시스템의 보안 등급을 좌우한다. 하나씩 살펴보자.

### `HttpOnly` — 자바스크립트의 접근을 막는다

`HttpOnly` 플래그가 붙은 쿠키는 `document.cookie`로 읽을 수 없다. 자바스크립트가 손대지 못한다. XSS 공격이 한 번 성공해 임의의 스크립트가 브라우저에서 실행되더라도, 세션 쿠키만큼은 가져갈 수 없다. 가장 기본적이면서 가장 강력한 방어다.

Spring Boot는 기본으로 `JSESSIONID`에 `HttpOnly`를 붙인다. `server.servlet.session.cookie.http-only` 속성이 기본 `true`다. 우리가 직접 쿠키를 만드는 경우에도 잊지 말고 켜자.

### `Secure` — HTTPS에서만 전송

`Secure` 속성이 붙은 쿠키는 HTTPS 연결에서만 전송된다. HTTP로는 절대 새지 않는다. 운영 환경의 모든 세션 쿠키는 이 속성을 반드시 켜야 한다.

`application.yml`에서 다음과 같이 설정한다.

```yaml
server:
  servlet:
    session:
      cookie:
        secure: true
        http-only: true
        same-site: lax
```

문제는 개발 환경이다. 로컬에서 HTTP로 띄워놓고 `secure: true`를 쓰면 브라우저가 쿠키를 안 보낸다. 결과는 "왜 로그인 안 돼?"의 무한 루프다. 이 부분은 환경별 프로파일로 갈라두는 편이 낫다. 운영 프로파일에만 `secure: true`, 로컬은 끄거나 `mkcert` 같은 도구로 로컬 HTTPS를 켜는 방법도 있다.

### `SameSite` — 가장 헷갈리는 한 칸

여기서 잠시 멈춰서 깊게 보자. `SameSite`는 비교적 최근에 표준화됐고, 그만큼 결정의 무게가 무겁다. 세 가지 값이 있다.

| 값 | 의미 |
|----|------|
| `Strict` | 다른 사이트에서 우리 사이트로 오는 모든 요청에 쿠키를 첨부하지 않는다 |
| `Lax` | 다른 사이트에서 오더라도 최상위 네비게이션(링크 클릭 등)에는 쿠키를 첨부한다. 폼 POST나 iframe, fetch에는 안 붙인다 |
| `None` | 모든 크로스 사이트 요청에 쿠키를 첨부한다. 단, `Secure`와 함께 써야 한다 |

`Strict`가 가장 안전하다는 건 명확하다. CSRF 공격을 사실상 원천 차단한다. 그런데 왜 모두가 `Strict`를 안 쓸까? 보안과 사용성이 살짝 갈리는 지점이 바로 여기다.

이런 상황을 상상해보자. 친구가 SNS에 우리 서비스의 어떤 페이지 링크를 올렸다. 다른 사용자가 그 링크를 클릭한다. `Strict`라면? 쿠키가 안 따라간다. 그 사용자는 이미 우리 서비스에 로그인되어 있었는데도 비로그인 상태로 페이지를 만나게 된다. "왜 또 로그인하라고 하지?" 하고 떠나버린다. 정말 난감한 사용자 경험이다.

`Lax`는 이 문제를 우아하게 푼다. 최상위 네비게이션(GET 요청으로 이뤄지는 단순 링크 이동)에는 쿠키를 붙여준다. 그래서 외부 링크로 들어와도 로그인 상태가 유지된다. 반면 POST 요청이나 fetch는 외부에서 못 보낸다 — CSRF의 표적이 되는 그 동작들 말이다. 보안과 사용성의 균형이 잡힌다. **현대 브라우저의 기본값이 `Lax`인 이유다.**

`None`은 언제 쓸까? SPA가 별도 도메인에 있고 API 서버가 또 다른 도메인이라면, 크로스 사이트로 쿠키를 보내야 한다. 이때 `None; Secure` 조합이 필수다. 하지만 이 길로 가면 CSRF 방어를 다른 수단(custom header, double-submit token)으로 보강해야 한다. 6장 BFF 패턴이 권하는 길은 차라리 도메인을 합치고 `Lax`로 가는 쪽이다. 가능하면 그렇게 하는 것이 바람직하다.

### 토큰을 쿠키에 담을 때

JWT 같은 토큰을 어디에 저장할 것인가는 5장에서 자세히 다뤘다. `localStorage`는 XSS 한 번이면 끝이라는 점도 강조했다. 그 결론을 다시 한번 짚자면, **토큰을 굳이 브라우저가 직접 들고 있어야 한다면 `HttpOnly; Secure; SameSite=Lax` 쿠키에 담아야 한다.** 그리고 이왕이면 거기서 한 걸음 더 나가서, 14장에서 본격적으로 다룰 **BFF 패턴**으로 토큰 자체를 브라우저에서 제거하는 편이 낫다. 브라우저에는 세션 쿠키만, 서버 측에서 토큰을 다룬다. 이게 가장 안전하고 가장 단순하다.

## 컨텍스트 전파의 함정 — 비동기와 스레드 풀의 만남

이제 이 장을 시작할 때 던졌던 질문으로 돌아가자. 사용자 A의 요청에서 시작된 비동기 작업이 어떻게 사용자 B의 권한으로 실행되는가? 답을 풀기 전에 `SecurityContextHolder`라는 친구의 본모습을 먼저 알아보자.

`SecurityContextHolder`는 이름이 거창하지만 본질은 단순하다. 현재 스레드에 묶인 보안 컨텍스트를 들고 있는 보관함이다. 이 보관함이 "현재 스레드에 묶인다"는 점이 핵심이다. 기본 구현은 `ThreadLocal`이다.

### 세 가지 전략 모드

`SecurityContextHolder`는 세 가지 저장 전략을 제공한다.

| 모드 | 동작 |
|------|------|
| `MODE_THREADLOCAL` (기본) | 현재 스레드에만 컨텍스트가 묶인다. 자식 스레드는 못 본다 |
| `MODE_INHERITABLETHREADLOCAL` | 자식 스레드도 부모의 컨텍스트를 상속 |
| `MODE_GLOBAL` | 전체 JVM이 단 하나의 컨텍스트를 공유 (테스트나 standalone에서나) |

`MODE_GLOBAL`은 거의 쓸 일이 없으니 잊어도 좋다. 흥미로운 건 앞의 둘이다.

`MODE_THREADLOCAL`은 가장 안전하다. 컨텍스트가 한 스레드에 갇혀 있으니 다른 스레드로 새 나갈 일이 없다. 단점도 명확하다 — 비동기 작업에서 부모의 컨텍스트를 안 보여준다. `@Async` 메서드 안에서 `SecurityContextHolder.getContext()`를 하면 빈 컨텍스트가 나온다.

이 문제를 가장 단순하게 풀어주는 게 `MODE_INHERITABLETHREADLOCAL`이다. 자식 스레드가 부모의 컨텍스트를 자동 상속한다. 비동기 작업에서도 보안 정보가 따라간다. 편하다. 그런데 이게 정말 안전할까?

### 끔찍한 일이 될 수 있는 조합

핵심을 정확히 말하자. **`MODE_INHERITABLETHREADLOCAL`과 스레드 풀의 만남은 끔찍한 일이 될 수 있다.**

왜 그럴까? `InheritableThreadLocal`이 "상속"하는 시점은 **자식 스레드가 만들어지는 그 순간**이다. 그 순간의 부모 스레드의 컨텍스트가 자식에게 복사된다. 그런데 스레드 풀은 어떻게 동작하는가? 풀은 스레드를 미리 만들어 둔다. 그리고 그 스레드를 **재사용**한다.

이게 무슨 뜻일까? 스레드 풀이 처음 스레드를 만든 시점이 마침 사용자 B의 요청을 처리 중이었다고 해보자. 그 순간 자식 스레드에 사용자 B의 컨텍스트가 상속된다. 풀의 스레드는 작업을 끝내고 풀로 돌아간다. 그런데 그 스레드 안에 있던 `ThreadLocal` 값은 지워지지 않는다. 사용자 B의 컨텍스트가 그대로 남아 있는 것이다.

이제 사용자 A가 요청을 보냈고, A의 흐름에서 `@Async` 메서드가 호출된다. 풀에서 스레드를 하나 꺼내 작업을 맡긴다. 마침 그 스레드가 아까 사용자 B의 컨텍스트를 들고 있던 그 스레드라면? `SecurityContextHolder.getContext()`는 **사용자 B의 컨텍스트를 반환한다**. 사용자 A의 요청에서 시작된 작업이 사용자 B의 권한으로 실행된다.

Spring Security 공식 이슈 트래커의 표현이 정확하다.

> "When Spring Async annotation is used with `MODE_INHERITABLETHREADLOCAL`, with thread pools this is dangerous because when a thread is reused from a pool, the security context which was set for the thread when it was created is reused, leading to an issue where a task relies on a completely wrong, some other user's security context."

운영 환경에서 이런 일이 벌어졌다고 상상해보자. 감사 로그가 어긋난다. 보안 결정이 잘못된 권한으로 내려진다. 데이터 변경의 출처가 뒤바뀐다. 어디서부터 풀어야 할지 막막한 종류의 사고다. 정말 끔찍한 일이다.

### 그렇다면 어떻게 해야 할까

해법은 두 갈래다.

**첫째, 기본 모드(`MODE_THREADLOCAL`)를 유지하고, 전파가 필요한 곳에만 명시적으로 전파한다.** Spring Security가 이미 도구를 제공한다. `DelegatingSecurityContextRunnable`, `DelegatingSecurityContextCallable`, `DelegatingSecurityContextAsyncTaskExecutor`다.

```java
@Bean
AsyncTaskExecutor delegatingExecutor(ThreadPoolTaskExecutor base) {
    return new DelegatingSecurityContextAsyncTaskExecutor(base);
}
```

이름이 길지만 동작은 단순하다. `Executor`가 작업을 받을 때 **현재 스레드의 컨텍스트를 캡처**해 두고, 작업이 실제로 실행될 때 그 캡처해둔 컨텍스트로 `SecurityContextHolder`를 채운다. 작업이 끝나면 깨끗이 비운다. 풀 스레드에 컨텍스트가 잔류하지 않는다.

`@Async`를 쓴다면, `AsyncConfigurer`에 이 Executor를 등록하면 된다.

```java
@Configuration
@EnableAsync
class AsyncConfig implements AsyncConfigurer {

    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor base = new ThreadPoolTaskExecutor();
        base.setCorePoolSize(8);
        base.setMaxPoolSize(16);
        base.initialize();
        return new DelegatingSecurityContextAsyncTaskExecutor(base);
    }
}
```

이렇게 하면 `@Async` 메서드 안에서도 호출한 사용자의 컨텍스트를 안전하게 본다. 그리고 풀로 돌아간 스레드는 컨텍스트를 들고 있지 않다.

**둘째, Java 21+의 Virtual Threads를 활용한다.** 가상 스레드는 작업 단위로 새로 만들어지고 끝나면 사라진다. 풀에 잔류하지 않는다. 그래서 `MODE_THREADLOCAL`만으로도 안전하다 — 가상 스레드 자체가 task 단위이므로 ThreadLocal이 다른 작업으로 새지 않는다. Spring Boot 4.0이 가상 스레드를 1급으로 지원하므로, 충분히 고려할 만한 선택지다. 다만 carrier thread pinning 회피 같은 별개 이슈는 따로 챙겨야 한다. 가상 스레드의 깊은 동작은 본 책의 범위를 벗어나므로 공식 문서를 참고하자.

여기서 명심할 한 가지. **`MODE_INHERITABLETHREADLOCAL`은 함부로 켜지 말자.** 옛 가이드나 블로그 글에서 "비동기 전파를 위해 InheritableThreadLocal로 바꿔라"라는 조언이 종종 보인다. 그 조언이 단일 스레드 환경에서는 맞지만, 스레드 풀이 끼는 순간 함정이 된다는 점을 명심해야 한다.

### `@Async` 베스트프랙티스 정리

`@Async`와 보안 컨텍스트의 조합을 한 번에 정리해두자.

```java
// 권장 패턴
@Service
class OrderService {

    @Async
    public CompletableFuture<Receipt> processAsync(OrderId id) {
        // DelegatingSecurityContextAsyncTaskExecutor가 등록돼 있으면
        // 여기서 SecurityContextHolder가 호출자 컨텍스트를 그대로 본다
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        // ... 호출자 권한으로 안전하게 처리
        return CompletableFuture.completedFuture(receipt);
    }
}
```

이 짧은 코드가 안전하게 동작하려면 세 가지가 맞아야 한다.

1. `MODE_INHERITABLETHREADLOCAL`을 켜지 않았다(기본값 유지).
2. `@Async`가 쓰는 Executor가 `DelegatingSecurityContextAsyncTaskExecutor`로 감싸져 있다.
3. 메서드 안에서 `SecurityContextHolder.getContext()`를 직접 읽되, 컨텍스트를 다른 스레드로 다시 넘기지는 않는다.

세 조건이 갖춰지면 `@Async`는 안전하다. 하나라도 어긋나면 위의 함정으로 빨려 들어간다. 매번 점검하자.

### 한 단계 더 — `CompletableFuture` 체이닝

`@Async`만 쓰는 게 아니라 `CompletableFuture.supplyAsync(...)`로 직접 작업을 만들고 체이닝하는 코드도 흔하다. 이 경우에도 같은 함정이 도사린다. 기본 `ForkJoinPool.commonPool()`을 쓰면 풀 스레드에 컨텍스트가 잔류할 수 있다. 답은 같다 — `DelegatingSecurityContextExecutor`로 감싼 풀을 명시적으로 넘기는 것이다.

```java
private final Executor secured;  // DelegatingSecurityContextExecutor로 감쌈

public CompletableFuture<Result> compute() {
    return CompletableFuture.supplyAsync(this::step1, secured)
        .thenApplyAsync(this::step2, secured);
}
```

`thenApplyAsync`에 Executor를 안 넘기면 또 다시 commonPool로 빠진다. 모든 async 단계에 명시적으로 secured Executor를 넘기자. 번거롭게 느껴질 수 있지만, 한 번 표준 패턴으로 만들어두면 그 다음부터는 자연스럽다.

## Reactive로의 다리 — `ReactiveSecurityContextHolder`

지금까지 본 모든 이야기는 서블릿 세계의 이야기다. `ThreadLocal`이라는 가정 위에 서 있다. 그런데 WebFlux로 가면 어떻게 될까?

WebFlux는 한 요청이 여러 스레드를 옮겨 다니며 처리된다. `ThreadLocal`이라는 가정 자체가 깨진다. 그래서 `SecurityContextHolder`를 그대로 호출하면 빈 컨텍스트가 나오거나 다른 사용자의 컨텍스트가 나온다. Reactive 흐름에서는 반드시 다른 도구를 써야 한다.

미리 한 줄만 맛보자.

```java
Mono<Authentication> auth = ReactiveSecurityContextHolder.getContext()
    .map(SecurityContext::getAuthentication);
```

이 한 줄이 무엇을 의미하는지, 그리고 Reactor Context를 통해 컨텍스트가 어떻게 흐르는지는 11장에서 본격적으로 다룬다. 지금 기억해둘 것은 단 하나다 — **Reactive 흐름에서는 `SecurityContextHolder`를 직접 호출하지 말자.** 컴파일은 되지만 동작은 엉뚱하다. 11장에서 그 정확한 의미를 풀 것이다.

## 마무리

이 장에서 보고 싶었던 것은 단순한 설정값 목록이 아니다. **상태가 어디에 살고, 어디로 흐르며, 어디서 새는가** 하는 모서리들의 풍경이었다. 다섯 가지로 압축해 기억해두자.

1. **세션 정책 네 가지의 의미를 분명히 하자.** `STATELESS`는 단순히 "세션 안 만든다"가 아니라 "세션이라는 개념 자체를 외면한다"다. `NEVER`와 헷갈리지 말자.
2. **`requireExplicitSave(true)`는 7.0의 새 권장 기본이다.** 컨텍스트가 언제 어디서 저장되는지를 코드에 드러내는 것이 모호한 자동 동작보다 낫다.
3. **세션 고정 보호는 기본이 안전하다 — `migrateSession()`. 함부로 `none()`을 켜지 말자.**
4. **쿠키 속성 세 줄을 잊지 말자.** `HttpOnly`, `Secure`, `SameSite=Lax`. `Strict`는 사용성 비용이 크다. `None`은 진짜 필요할 때만.
5. **`MODE_INHERITABLETHREADLOCAL`과 스레드 풀의 만남은 끔찍한 일이다.** 비동기에 컨텍스트가 필요하면 `DelegatingSecurityContextAsyncTaskExecutor`로 명시적으로 전파하자. Virtual Threads가 새로운 선택지다.

다음 장에서는 이 장 마지막에서 살짝 본 그 문제를 본격적으로 다룬다. Reactive 세계에서 인증과 인가는 어떻게 다시 그려지는가? `ServerHttpSecurity`, `ReactiveAuthenticationManager`, `ReactiveSecurityContextHolder`라는 새 어휘들이 등장한다. 서블릿 책에서 쌓아온 직관이 어디까지 그대로 통하고, 어디서 새로 배워야 하는지를 함께 살펴보자.
