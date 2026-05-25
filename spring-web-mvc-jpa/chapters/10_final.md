# 10장. JWT로 인증하기 — stateless 구현과 신선도 함정의 클라이맥스

당신이 React 앱에 로그인 화면을 붙였다고 해보자. 사용자가 아이디와 비밀번호를 넣고 "로그인" 버튼을 누른다. 서버가 "맞네, 환영해"라고 답한다. 그런데 여기서부터가 진짜 문제다. 그다음 사용자가 할 일을 만들려고 `POST /api/tasks`를 때릴 때, 서버는 *이 요청을 보낸 사람이 방금 로그인한 그 사람*이라는 걸 어떻게 알아볼까?

HTTP는 본래 한 번 요청하고 답하면 서로를 잊어버리는, 기억력이 없는(stateless) 프로토콜이다. 매 요청은 처음 보는 손님처럼 도착한다. 그러니 "방금 로그인했잖아요"는 서버에게 통하지 않는다. 요청 하나하나가 자기가 누구인지를 *스스로 증명*해야 한다. 그렇다면 어떻게 해야 할까? 로그인할 때 서버가 일종의 '출입증'을 하나 발급하고, 사용자는 그 뒤로 모든 요청에 그 출입증을 붙여 보내면 된다. 서버는 출입증만 확인하면 "아, 김아무개구나" 하고 알아본다.

그 출입증을 만드는 가장 흔한 방법 중 하나가 바로 이번 장의 주인공, **JWT(JSON Web Token)**다. 9장에서 우리는 필터체인이라는 검문소의 줄을 그렸다. 오늘은 그 줄에 *진짜 인증 필터*를 하나 끼워, 출입증을 검사하는 실제 검문소를 세운다. 그리고 그 과정에서 — 이 책 전체를 관통해온 신선도 함정이 마침내 정면으로 터진다. 마음을 단단히 먹고 들어가 보자.

## 출입증 안에 뭐가 들었나 — JWT의 세 조각

JWT는 거창한 이름과 달리 구조가 단순하다. RFC 7519로 규격이 정해진 토큰인데, 점(`.`) 두 개로 나뉜 세 조각의 문자열일 뿐이다.

```
xxxxx.yyyyy.zzzzz
헤더   페이로드  서명
```

각 조각이 무슨 일을 하는지 하나씩 보자.

- **헤더(header):** "이 토큰은 어떤 알고리즘으로 서명됐다"는 메타 정보를 담는다. 예컨대 "HS256으로 서명함" 같은 내용이다.
- **페이로드(payload):** 진짜 알맹이다. "이 사용자는 누구인가(sub)", "언제 만료되나(exp)" 같은 정보(클레임claim이라 부른다)가 들어간다. 우리 TaskBoard라면 "사용자 ID는 42, 역할은 USER" 같은 게 여기 실린다.
- **서명(signature):** 헤더와 페이로드를 *서버만 아는 비밀 키*로 봉인한 도장이다.

여기서 한 가지 의문이 생긴다. 헤더와 페이로드는 사실 *암호화된 게 아니라 그냥 인코딩*만 된 거라, 누구든 까서 읽을 수 있다. 그렇다면 누가 페이로드를 "사용자 ID는 42"에서 "사용자 ID는 1(관리자)"로 슬쩍 고쳐버리면 어떻게 될까? 바로 이 지점에서 세 번째 조각, 서명이 일한다. 페이로드를 한 글자라도 건드리면 서명이 더는 들어맞지 않는다. 서버는 받은 토큰의 서명을 자기 비밀 키로 다시 계산해보고, 어긋나면 "위조된 출입증"이라며 즉시 내친다. 그러니 **JWT는 내용을 숨기는 도구가 아니라, 내용이 위조되지 않았음을 보증하는 도구**다. 이 점을 꼭 기억해두자. 페이로드에 비밀번호 같은 민감 정보를 넣으면 안 되는 이유가 바로 여기 있다 — 누구나 읽을 수 있으니까.

## 출입증을 서버에 적어두지 않는다는 것 — stateless 모델

JWT의 진짜 매력은 구조가 아니라 *운영 방식*에 있다. 9장 끝에서 예고했듯, JWT는 **stateless(상태 없음)** 인증의 대표 선수다. 무슨 뜻일까?

세션 방식(11장에서 자세히 본다)을 떠올려보자. 그쪽은 서버가 "출입증 A-1234는 김아무개에게 발급됨"이라는 명단을 *서버 안 어딘가*에 적어둔다. 요청이 올 때마다 그 명단을 뒤져 "A-1234가 명단에 있나?"를 확인한다. 반면 JWT는 그 명단을 두지 않는다. 출입증 자체에 "나는 김아무개, 만료는 3시"라고 적혀 있고 위조 방지 도장(서명)까지 찍혀 있으니, 서버는 명단을 뒤질 필요 없이 *도장만 진짜인지* 확인하면 끝이다.

이게 왜 좋을까? 서버를 여러 대로 늘릴 때 빛을 발한다. 트래픽이 몰려 서버를 3대, 5대로 수평 확장한다고 해보자. 세션 명단을 쓰면 그 명단을 모든 서버가 공유해야 한다(보통 Redis 같은 공유 저장소를 둔다). 그런데 JWT는 출입증이 자기 정보를 다 들고 다니니, 어느 서버로 요청이 가든 그 서버 혼자 도장만 확인하면 된다. 공유 저장소가 필요 없다. 여러 프런트엔드와 모바일 앱이 같은 API를 두드리는 상황이라면 특히 잘 맞는다.

물론 공짜는 아니다. 명단을 안 두니, 한번 발급한 출입증을 *중간에 강제로 무효화*하기가 까다롭다. "이 사용자 지금 당장 로그아웃시켜!"가 세션만큼 깔끔하지 않다. 그래서 실무에서는 출입증의 수명을 짧게 — 보통 **짧은 액세스 토큰(access token)** 으로 — 끊어두고, 그게 만료되면 **리프레시 토큰(refresh token)** 으로 새로 발급받는 식으로 보완한다. 이 두 토큰의 구체적인 설계는 책의 범위를 넘으니 여기서는 "짧게 끊고 갱신한다"는 개념만 잡아두자. 무효화의 어려움은 11장에서 세션과 정면으로 비교할 핵심 트레이드오프이기도 하다.

## 프런트의 오랜 숙제 — 토큰을 어디에 둘까

여기서 짚고 갈 게 하나 있다. 서버가 발급한 그 토큰을, 프런트 개발자인 당신이 브라우저의 *어디에* 저장할 것인가? 흔한 후보는 둘이다. 자바스크립트로 자유롭게 읽고 쓰는 `localStorage`냐, 자바스크립트가 손대지 못하도록 봉인하는 `httpOnly` 쿠키냐.

지금 이 자리에서 "무조건 이게 정답"이라고 못 박진 않겠다. 둘 중 무엇을 고르느냐는 XSS·CSRF 같은 공격과 5장에서 씨름한 CORS의 `allowCredentials` 설정까지 얽힌 *보안 결정*이고, 이건 JWT냐 세션이냐의 선택과도 맞물려 있어서 11장에서 트레이드오프를 정면으로 펼쳐놓고 함께 판단할 것이다. 다만 오늘 기억해둘 건 이것이다 — **토큰을 어디 두느냐는 프런트의 사소한 구현 디테일이 아니라 보안 결정**이라는 것. (프런트 ↔ 백엔드 대응이 헷갈리면 부록 A 대조표의 '토큰 저장' 항목을 함께 보자.) 이 장의 코드 예시는 설명을 단순하게 하려고 `Authorization: Bearer` 헤더 방식을 쓰지만, 그 선택의 무게는 잊지 말자.

## 검문소를 세운다 — 필터체인에 JWT 인증 필터 끼우기

이제 9장에서 그린 그림을 코드로 옮길 차례다. 우리가 할 일을 큰 그림으로 먼저 보자.

1. 사용자가 아이디·비밀번호로 로그인하면, 서버가 검증 후 **JWT를 발급**해 돌려준다.
2. 그 뒤로 사용자는 모든 요청의 `Authorization` 헤더에 `Bearer {토큰}`을 실어 보낸다.
3. 9장의 필터체인 어딘가에 **JWT 검증 필터**를 끼워, 요청이 컨트롤러에 닿기 전에 토큰을 확인한다.
4. 토큰이 유효하면 "이 요청은 김아무개가 보냈다"는 사실을 Security에 등록하고 통과시킨다.

3번이 9장과 10장을 잇는 핵심이다. 9장에서 "검문소의 줄"을 그렸다면, 오늘은 그 줄에 *우리가 만든 검문소 하나*를 직접 끼워 넣는 것이다.

먼저 토큰을 발급하고 검증하는 도구가 필요하다. JWT는 라이브러리로 다루는데, 자바 진영에서 널리 쓰이는 게 `jjwt`나 `nimbus-jose-jwt` 같은 것들이다. 토큰을 만들고 푸는 작은 부품을 하나 만들어보자.

```java
@Component
public class JwtTokenProvider {

    private final SecretKey key;
    private final long validityMs = 1000L * 60 * 30; // 30분짜리 짧은 토큰

    public JwtTokenProvider(@Value("${jwt.secret}") String secret) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
    }

    // 로그인 성공 시 토큰 발급
    public String createToken(String username) {
        Date now = new Date();
        return Jwts.builder()
            .subject(username)
            .issuedAt(now)
            .expiration(new Date(now.getTime() + validityMs))
            .signWith(key)
            .compact();
    }

    // 요청에 실려 온 토큰에서 사용자 식별
    public String getUsername(String token) {
        return Jwts.parser()
            .verifyWith(key)
            .build()
            .parseSignedClaims(token)
            .getPayload()
            .getSubject();
    }
}
```

코드를 한 줄씩 곱씹어보자. `createToken`은 로그인에 성공했을 때 불린다. "이 토큰의 주인은 username이다(`subject`)", "발급 시각은 지금", "30분 뒤 만료" 같은 정보를 담고, 마지막에 우리만 아는 비밀 키로 `signWith` — 즉 도장을 찍어 — `compact()`로 한 줄 문자열로 압축한다. 반대로 `getUsername`은 들어온 토큰을 `verifyWith`로 *서명을 검증하면서* 풀어 페이로드의 주인을 꺼낸다. 서명이 안 맞으면 여기서 예외가 터지고, 그건 곧 "위조된 토큰"이라는 뜻이다.

한 가지 일러둘 게 있다. 위 코드는 `jjwt` 0.12.x 계열의 빌더·파서 API다(`Jwts.builder().subject()`, `Jwts.parser().verifyWith().build().parseSignedClaims()`). 그런데 jjwt는 0.11→0.12에서 이 API가 크게 바뀌었다. 인터넷과 AI가 주는 예제는 구버전(`Jwts.parserBuilder()`, `setSubject()` 등)을 섞어 줄 위험이 큰 영역이니, 이 점은 잠시 뒤 신선도 함정 절에서 다시 짚는다.

이 부품을 매 요청마다 호출할 필터가 그다음이다. 9장에서 말한 "검문소" 그 자체다.

```java
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtTokenProvider tokenProvider;

    public JwtAuthenticationFilter(JwtTokenProvider tokenProvider) {
        this.tokenProvider = tokenProvider;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain)
            throws ServletException, IOException {

        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            String token = header.substring(7);
            String username = tokenProvider.getUsername(token); // 유효하지 않으면 예외
            var auth = new UsernamePasswordAuthenticationToken(
                username, null, List.of()); // 권한은 단순화
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        chain.doFilter(request, response); // 다음 검문소로 넘긴다
    }
}
```

복잡해 보이지만 하는 일은 9장에서 그린 그대로다. `Authorization` 헤더에서 `Bearer ` 뒤의 토큰을 떼어내고, 아까 만든 `JwtTokenProvider`로 검증하고, 통과하면 "이 요청은 이 사용자가 보냈다"를 `SecurityContextHolder`에 등록한다. 이렇게 등록해두면, 그다음 인가 필터가 "이 사용자가 이 경로에 들어갈 권한이 있나"를 따질 때 이 정보를 본다. 마지막 `chain.doFilter`로 다음 검문소에게 요청을 넘긴다 — 줄을 따라 흘러가는 것이다. 참고로 `HttpServletRequest`를 비롯한 서블릿 API는 Spring Security 6.x에서 `javax.servlet`이 아니라 `jakarta.servlet` 네임스페이스다. 이 책이 거듭 경고해온 javax→jakarta 함정이 여기서도 그대로 적용된다.

## 신선도 함정의 클라이맥스 — AI가 들고 오는 구버전 코드

자, 이제 이 책 전체를 관통해온 이야기의 정점이다. 2장에서 개념으로 심고, 3장과 6장에서 import 한 줄로 맛본 그 신선도 함정 — 오늘 정면으로 터뜨린다.

당신이 Cursor나 Claude Code에게 이렇게 부탁했다고 해보자. "Spring Security로 JWT 인증 설정을 만들어줘." 십중팔구, AI는 아주 자신 있게 이런 코드를 내놓을 것이다.

```java
// ⚠️ AI가 자신 있게 주는 구버전 코드 (Spring Security 5.x 이하)
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .authorizeRequests()
                .antMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated()
            .and()
            .addFilterBefore(jwtFilter(),
                UsernamePasswordAuthenticationFilter.class);
    }
}
```

이 코드를 본 순간, 9장을 함께 걸어온 당신이라면 어딘가 *낯설다*는 느낌이 들어야 한다. 9장에서 우리가 쓴 건 분명 `SecurityFilterChain` 빈이었는데, 여기엔 그게 없다. 대신 `WebSecurityConfigurerAdapter`라는 걸 *상속*하고 `configure` 메서드를 *오버라이드*하고 있다. 게다가 `authorizeRequests`니 `antMatchers`니 하는 이름들 — 9장에서 "이건 옛 이름"이라고 예고했던 바로 그것들이다.

이게 왜 이런 일이 벌어질까? AI는 인터넷에 쌓인 방대한 예제를 학습한다. 그런데 Spring Security 5.x 시절의 이 패턴이 수년간 너무도 널리 쓰여, 인터넷에 압도적으로 많이 남아 있다. AI는 "더 흔한 패턴"을 자신 있게 줄 뿐, "더 최신인 패턴"을 가려내주지 못한다. 그러니 AI가 자신 있다고 해서 옳은 게 아니다. 이 한 문장이 이 책이 거듭 강조해온 핵심이다.

그렇다면 무엇이 잘못됐고, 어떻게 고쳐야 할까? Spring Boot 3.x가 품는 **Spring Security 6.x**에서는 다음이 사실이다.

- `WebSecurityConfigurerAdapter`는 **아예 제거됐다.** 상속할 클래스 자체가 없다. 이 코드는 6.x에서 컴파일조차 되지 않는다.
- `authorizeRequests`는 **`authorizeHttpRequests`** 로 바뀌었다.
- `antMatchers`(와 `mvcMatchers`)는 **`requestMatchers`** 로 통합됐다.
- `.and()`로 줄줄이 잇던 옛 방식 대신, 람다 DSL로 각 설정을 블록으로 받는다.

같은 의도를 6.x로 다시 쓰면 이렇게 된다.

```java
// ✅ Spring Security 6.x — SecurityFilterChain 빈 + 람다 DSL
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtFilter) {
        this.jwtFilter = jwtFilter;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable()) // JWT는 stateless라 보통 끈다(쿠키 인증이면 재고)
            .sessionManagement(sm -> sm
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/tasks/**").authenticated()
                .anyRequest().permitAll()
            )
            .addFilterBefore(jwtFilter,
                UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

before와 after를 나란히 두고 보면 차이가 또렷하다. 9장에서 우리가 이미 `SecurityFilterChain` 빈을 썼기 때문에, 사실 after 쪽이 훨씬 익숙하게 읽힐 것이다 — 9장에서 그려둔 그림 그대로, 거기에 인증 필터 한 줄(`addFilterBefore`)을 더했을 뿐이다. JWT는 stateless라 서버 세션을 안 만들도록 `STATELESS`로 못 박은 것, 그리고 `/api/auth/**`(로그인) 경로는 열어두고 `/api/tasks/**`는 인증을 요구한 것이 새로 추가된 의도다.

기억해두자. 보안 설정만큼은 AI에게 받은 코드를 *그대로 믿어선 안 된다*. 이 셋만 걸러도 가장 흔한 함정은 피한다 — 구체적인 점검 습관은 아래 AI 페어코딩 사이드바에 정리해뒀으니 곁에 두고 쓰자.

## 로그인 엔드포인트와 보호된 엔드포인트

마지막으로, 이 모든 걸 TaskBoard에 실제로 연결해보자. 우선 토큰을 발급하는 로그인 엔드포인트가 필요하다.

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService; // 비밀번호 검증 + 토큰 발급

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<TokenResponse> login(@Valid @RequestBody LoginRequest req) {
        String token = authService.login(req.username(), req.password());
        return ResponseEntity.ok(new TokenResponse(token));
    }
}
```

`AuthService` 안에서는 9장에서 심어둔 `PasswordEncoder`(BCrypt)가 비로소 일한다. 사용자가 보낸 평문 비밀번호를, DB에 해싱돼 저장된 비밀번호와 `passwordEncoder.matches(...)`로 대조한다. 맞으면 `JwtTokenProvider.createToken`으로 토큰을 발급해 돌려준다. 9장에서 "다음 장에서 활약한다"던 BCrypt가 여기서 약속을 지키는 셈이다.

이제 흐름 전체가 한 바퀴 돈다. 프런트는 `/api/auth/login`으로 아이디·비밀번호를 보내 토큰을 받고, 그 뒤 `/api/tasks`를 부를 때마다 `Authorization: Bearer {토큰}`을 실어 보낸다. 우리가 끼운 `JwtAuthenticationFilter`가 그 토큰을 검문하고, 통과한 요청만 컨트롤러에 닿는다. 토큰 없이 `/api/tasks`를 때리면? 9장에서 본 그대로, 컨트롤러 근처에도 못 가고 401로 되돌려진다.

> **AI 페어코딩 학습 포인트**
>
> 이 장이 신선도 함정의 클라이맥스인 만큼, AI 활용법도 한 단계 단단해질 차례다. JWT·Security 설정을 AI에게 시킬 때는 프롬프트에 "Spring Boot 3.x, Spring Security 6.x, jakarta 네임스페이스, jjwt 0.12 기준" 같은 버전 좌표를 *먼저* 못 박자. 그래도 AI는 구버전을 섞어 줄 때가 많다. 받은 코드는 이 장에서 익힌 before/after의 눈으로 거른다 — ① `WebSecurityConfigurerAdapter`를 상속하고 있지 않은가, ② `authorizeRequests`·`antMatchers` 같은 옛 이름이 보이지 않는가, ③ jjwt가 `parserBuilder()`·`setSubject()` 같은 구버전 빌더를 쓰지 않는가, ④ import가 `javax.*`가 아니라 `jakarta.*`인가. 하나라도 보이면 그건 십중팔구 시점이 어긋난 코드다. 의심스러우면 AI에게 "이 코드 Spring Security 6.x에서 컴파일돼? `WebSecurityConfigurerAdapter`는 제거된 걸로 아는데"라고 *되물어* 스스로 교정하게 하는 것도 좋은 방법이다. 더 촘촘한 점검 목록은 부록 B 신선도 체크리스트로 확인하자.

## 마무리

오늘 우리는 9장에서 그린 검문소의 줄에 *진짜 인증 필터*를 끼워, stateless 로그인을 직접 완성했다. JWT가 헤더·페이로드·서명 세 조각으로 되어 있고(RFC 7519), 서명이 위조를 막는 도장이며, 명단을 서버에 두지 않아 수평 확장에 강하다는 것 — 그리고 그 대가로 즉시 무효화가 까다롭다는 것까지 보았다. 무엇보다, AI가 자신 있게 들고 오는 `WebSecurityConfigurerAdapter` 구버전 코드를 6.x 람다 DSL로 고쳐내는 before/after를 손으로 겪었다. 이 책이 처음부터 깔아온 신선도 서사가 여기서 정점을 찍었다.

기억해두자. AI의 자신감은 정확성의 보증이 아니다. 특히 Security처럼 버전 경계가 뚜렷한 영역일수록, "이거 최신 맞아?"를 묻는 당신의 눈이 마지막 방어선이다.

그런데 — JWT가 정말 유일한 답일까? "이 사용자 지금 당장, 모든 기기에서 로그아웃시켜"가 필요해지는 순간, 명단 없는 stateless의 매력은 곧장 골칫거리로 바뀐다. 그렇다면 다른 길은 없을까? **다음 장에서는 정반대의 선택 — 세션(stateful) 방식**을 같은 TaskBoard에 두 번째로 적용해보고, 두 길의 트레이드오프를 정면으로 견줘본다. 오늘 만든 출입증을 손에 쥔 채, 다른 길로 한번 걸어가 보자.
