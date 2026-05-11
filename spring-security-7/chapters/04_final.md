# 4장. 폼 로그인·HTTP Basic·Remember-Me — 세션 기반 인증의 정석

> 선행 필요: 2장(필터 체인), 3장(컴포넌트 모델)

가장 오래된 친구부터 만나자. Spring Security를 처음 켤 때 누구나 본 그 폼. 흰 바탕에 `Username`과 `Password` 두 칸이 떡 놓여 있고, 한 번도 손대지 않았는데도 어찌어찌 동작한다. 너무 단순해서 가끔은 잊는다. 이 폼 뒤에는 11개의 필터와 네 개의 협력자가, 그리고 30년 가까이 운영된 세션이라는 기계가 묵묵히 돌고 있다는 사실을.

이 폼이 한물갔다고 생각하는 사람이 많다. JWT가 등장한 뒤로는 더 그렇다. 그런데 7.0 GA 릴리스 노트를 펴 보면 좀 의외다. 폼 로그인은 멀쩡히 살아 있고, 오히려 `securityContext.requireExplicitSave(true)`처럼 미묘한 기본값이 바뀌었으며, `PasswordEncoder` 자리에는 Password4j 기반 신규 인코더가 무려 다섯 종이나 추가됐다. 한물갔다고 보기엔 너무 활기차다.

그렇다면 다시 펴 보자. 단, 처음 보는 사람의 눈이 아니라 "내가 어디서 다쳤었는지" 기억하는 사람의 눈으로. 가장 오래된 친구가 가장 정직하게 보여 주는 것이 있는 법이다. 인증·세션·쿠키라는 세 단어가 한 요청 안에서 어떤 춤을 추는지, 그리고 그 춤이 흐트러지면 어디가 먼저 무너지는지.

## 4.1 한 번의 로그인이 통과하는 길

회원이 폼에 `alice / p@ssw0rd`를 입력하고 로그인 버튼을 눌렀다고 상상해 보자. 브라우저는 `POST /login`을 던지고, 서버 어딘가에서 인증이 성공한 뒤, 다음 요청부터는 "안녕하세요 alice 님"이 뜬다. 사이에서 무슨 일이 일어났을까?

2장에서 본 필터 체인을 떠올리면 답이 쉽다. 폼 로그인의 모든 마법은 `UsernamePasswordAuthenticationFilter` 한 자리에서 시작된다.

```java
@Configuration
@EnableWebSecurity
class WebSecurityConfig {
    @Bean
    SecurityFilterChain web(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(a -> a
                .requestMatchers("/", "/login", "/signup").permitAll()
                .anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .logout(Customizer.withDefaults())
            .build();
    }
}
```

이 짧은 빈 정의 한 조각이 깔리는 순간, 다음 시퀀스가 자동으로 완성된다.

1. `UsernamePasswordAuthenticationFilter`가 `POST /login`을 가로채 폼 파라미터에서 `username`과 `password`를 꺼낸다.
2. 두 값을 들고 `UsernamePasswordAuthenticationToken`을 만든다. 이때 토큰은 아직 "주장(claim)"에 불과하다. 검증된 게 아니다.
3. 이 토큰을 `AuthenticationManager`에 넘긴다. 3장에서 본 그 위임 모델대로 `ProviderManager`가 등장하고, 폼 로그인에 어울리는 `DaoAuthenticationProvider`가 골라진다.
4. `DaoAuthenticationProvider`는 `UserDetailsService.loadUserByUsername("alice")`를 호출해 저장소에서 사용자를 꺼낸다.
5. 꺼낸 사용자의 해시된 패스워드와, 토큰에 담겨 있던 원본 패스워드를 `PasswordEncoder.matches(raw, encoded)`로 비교한다.
6. 일치하면 인증된 `Authentication` 객체가 반환된다. 이 객체가 곧 `SecurityContext`에 담기고, `HttpSessionSecurityContextRepository`가 그것을 세션의 `SPRING_SECURITY_CONTEXT` 속성에 저장한다.

여기서 잠깐 멈춰 보자. 한 흐름인 것 같지만 사실 여섯 개의 협력자가 정확히 자기 일만 한다. 필터는 HTTP를 다루고, 매니저는 위임만 하고, 프로바이더는 자격 증명을 검증만 하고, 사용자 서비스는 저장소만 들여다보고, 인코더는 해시 비교만 하고, 리포지토리는 세션에만 손을 댄다. 단 한 번의 로그인이 이렇게나 잘게 쪼개진다.

처음 본 사람에게는 과해 보일 수 있다. 그런데 이렇게 나뉘어 있기 때문에 우리는 나중에 `UserDetailsService`만 갈아 끼워 JDBC를 LDAP로 바꿀 수 있고, `PasswordEncoder`만 갈아 끼워 BCrypt를 Argon2id로 바꿀 수 있다. 한 덩어리였다면 갈아 끼울 자리가 없다. 컴포넌트 분리의 가치는 "왜 이렇게 복잡해?"라는 첫인상이 가신 뒤에야 비로소 보인다.

### 그 다음 요청은 어떻게 알아보는가

로그인 성공 시 응답은 `302 Found`로 원래 가려던 곳(혹은 `/`)으로 리다이렉트되고, `Set-Cookie: JSESSIONID=...`가 함께 떨어진다. 다음 요청부터는 브라우저가 그 쿠키를 자동으로 들고 다니고, 서버 쪽 필터 체인의 앞쪽에 자리 잡은 `SecurityContextHolderFilter`(과거 `SecurityContextPersistenceFilter`의 후신)가 세션에서 `SecurityContext`를 꺼내 `SecurityContextHolder`에 심는다. 컨트롤러는 그저 `Authentication`을 받아 쓰기만 한다. 누가 어디서 그걸 꺼냈는지는 신경 쓰지 않는다.

이 흐름이 한 번 머릿속에 박히면, 뒤에 나오는 모든 변종 — Basic, Remember-Me, JWT, OAuth2 — 이 결국 이 큰 그림의 어느 부분을 갈아 끼운 것인지가 또렷이 보인다.

### 7.0의 미묘한 기본값: `requireExplicitSave(true)`

여기서 7.0이 살짝 바꾼 기본값 하나를 짚고 가자. 과거 5.x 시절에는 응답이 커밋될 때 자동으로 `SecurityContext`를 세션에 저장해 주는 동작이 기본이었다. 그런데 이게 묘하게 찜찜한 구석이 있었다. 응답을 내려보내는 마지막 순간에 컨텍스트를 슬쩍 저장하는 식이라, 비동기 응답이나 응답 후 처리 코드와 묘하게 엇박이 났다.

7.0의 권장 기본값은 `securityContext.requireExplicitSave(true)`다. 의미는 단순하다. "저장은 우리가 알아서 안 한다. 명시적으로 `SecurityContextRepository`에 저장하라." 폼 로그인 같은 표준 시나리오에서는 인증 필터가 알아서 저장해 주니 평소엔 차이를 못 느낀다. 그러나 인증 흐름을 직접 짜는 경우 — 가령 OTP 검증 후 수동으로 `SecurityContext`를 만들어 넣는 경우 — 저장을 안 해 주면 다음 요청에서 인증이 휘발된다. "왜 분명히 set했는데 다음 요청에서 anonymous지?"의 8할은 여기서 온다.

기억해두자. 7.0에서 컨텍스트는 자동으로 저장되지 않는다. 직접 만들었으면 직접 저장해 줘야 한다.

## 4.2 `PasswordEncoder` — 비교 하나에 모든 안전이 걸려 있다

위 시퀀스 5단계의 한 줄, `PasswordEncoder.matches(raw, encoded)`. 코드로는 한 줄이지만 보안의 무게로는 전체 시퀀스에서 가장 무거운 한 줄이다. 패스워드를 평문으로 저장하지 않고 해시해 둔다는 것은 너무 당연하다고 다들 말한다. 그런데 어떤 해시로? 얼마나 강하게?

### 두 인코더를 두고 고민할 때마다 떠오르는 질문

BCrypt와 Argon2를 두고 고민할 때마다 떠오르는 질문이 있다. "지금 내 운영 환경에서, 공격자가 GPU 클러스터를 빌려 오프라인 brute-force를 돌릴 수 있다고 가정할 때, 한 번의 검증에 1초씩 걸리도록 비용을 조여도 되는가?" 답이 "그렇다"면 Argon2id 같은 메모리 하드 함수를 켜는 편이 낫다. 답이 "1초는 너무 길다, 100ms 안에 끝나야 한다"면 BCrypt에 work factor 12 정도를 두고 가는 것이 현실적이다.

물론 Argon2id가 더 강하다. 하지만 강한 만큼 메모리와 CPU를 먹는다. 로그인 폭주 시 인스턴스가 흔들릴 수도 있다. 정답이 하나 있는 게 아니라 트레이드오프가 있을 뿐이다.

### 7.0의 Password4j 5종 — 선택지가 늘었다는 건 좋은 일이다. 그런데 왜 굳이 다섯이나?

7.0 릴리스 노트의 Cryptography 섹션을 펴 보면 다음 다섯이 새로 들어왔다.

- `Argon2Password4jPasswordEncoder`
- `BcryptPassword4jPasswordEncoder`
- `ScryptPassword4jPasswordEncoder`
- `Pbkdf2Password4jPasswordEncoder`
- `BalloonHashingPassword4jPasswordEncoder`

기존에도 Spring Security는 BCrypt와 Argon2와 PBKDF2를 자체 구현 또는 BouncyCastle 기반으로 제공해 왔다. 그런데 굳이 Password4j 기반 다섯 종을 더 얹은 이유는 뭘까?

핵심은 두 가지다. 첫째, Password4j는 패스워드 해시 라이브러리 한 가지에만 집중하는 프로젝트라 튜닝 파라미터의 노출이 풍부하고, 알고리즘 업데이트가 빠르다. 둘째, **Balloon Hashing**이라는 비교적 새로운 메모리 하드 함수가 표준 옵션으로 들어왔다. Argon2의 대안 후보로 학계에서 꾸준히 논의된 알고리즘이고, 이걸 쓰고 싶었던 사람들이 직접 인코더를 짜지 않아도 되도록 통합한 셈이다.

그러면 다섯 중 무엇을 골라야 하나? 다음 정도로 정리하면 큰 문제는 없다.

- 새 프로젝트라면 `Argon2Password4jPasswordEncoder`를 기본으로 고려하자. 메모리 하드, OWASP가 패스워드 해싱 1순위로 추천하는 알고리즘이다.
- 이미 BCrypt로 굴러가는 시스템이라면 `BcryptPassword4jPasswordEncoder`로 같은 알고리즘을 유지하되 라이브러리만 갈아 끼우면 된다. 마이그레이션 부담이 작다.
- 새 알고리즘 도입에 신중한 팀이거나 FIPS 같은 제약이 있다면 `Pbkdf2Password4jPasswordEncoder`가 무난하다.
- Balloon Hashing은 호기심이 아니라면 굳이 먼저 고를 이유는 없다. 검증된 운영 사례가 아직 적다.

```java
@Bean
PasswordEncoder passwordEncoder() {
    return new Argon2Password4jPasswordEncoder();
}
```

한 줄로 끝난다. 그런데 이 한 줄을 바꾸면 운영 중인 모든 패스워드 검증의 비용 곡선이 통째로 바뀐다는 점을 잊지 말자. 인코더를 바꿀 때는 부하 테스트를 함께 돌려 보는 편이 안전하다.

### 알고리즘을 바꾸고 싶을 때 — `DelegatingPasswordEncoder`

BCrypt로 1년을 쓰다가 Argon2id로 옮기고 싶어졌다고 해 보자. 기존 사용자들의 해시는 `$2a$...` 형태로 저장돼 있다. 모두 한꺼번에 다시 해싱할 수는 없다(원본 패스워드를 모르니까). 그렇다면 어떻게 해야 할까?

답은 `DelegatingPasswordEncoder`다. 저장된 해시 앞에 알고리즘 식별자(`{bcrypt}...`, `{argon2}...`)를 붙여 두면, 검증 시점에는 식별자에 맞는 인코더로 매칭하고, 인코딩 시점에는 현재 디폴트(예: Argon2)를 쓴다. 사용자가 다음에 로그인하거나 비밀번호를 바꿀 때 자연스럽게 새 알고리즘으로 갈아 끼울 수 있다.

```java
@Bean
PasswordEncoder passwordEncoder() {
    return PasswordEncoderFactories.createDelegatingPasswordEncoder();
}
```

`PasswordEncoderFactories.createDelegatingPasswordEncoder()`가 표준 매핑을 다 끼워 준다. 운영 시스템에서 단일 인코더로 못 박지 말고, 처음부터 위임 인코더로 시작해 두는 편이 낫다. 알고리즘 교체는 언젠가 반드시 일어난다.

## 4.3 `UserDetailsService` — 진짜 운영에 맞춰 갈아 끼우자

`UserDetailsService`는 너무 단순한 인터페이스라 종종 만만하게 본다. 메서드가 하나뿐이다.

```java
UserDetails loadUserByUsername(String username) throws UsernameNotFoundException;
```

문서에서 보여 주는 예제는 보통 `InMemoryUserDetailsManager`다. 메모리에 사용자 두 명 박아 두고 동작 확인하는 용도. 그런데 운영에서 이걸 그대로 쓰는 사람은 없을 것이고, 그래서도 안 된다. 어떻게 갈아 끼워야 할까?

### JDBC: 가장 흔한 시작

가장 표준적인 출발점은 `JdbcUserDetailsManager`다. Spring Security가 권하는 기본 스키마(`users` 테이블과 `authorities` 테이블)에 데이터를 넣고 빈만 등록하면 끝이다. 하지만 현실의 사용자 테이블은 거의 다 도메인 요구에 맞춰 다른 모양을 하고 있다. 그렇다면 직접 구현하는 편이 자연스럽다.

```java
@Service
class JpaUserDetailsService implements UserDetailsService {
    private final UserRepository users;

    JpaUserDetailsService(UserRepository users) { this.users = users; }

    @Override
    public UserDetails loadUserByUsername(String username) {
        var user = users.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException(username));
        return User.withUsername(user.getEmail())
            .password(user.getPasswordHash())
            .authorities(user.getRoles().stream()
                .map(r -> "ROLE_" + r.name())
                .toArray(String[]::new))
            .accountLocked(user.isLocked())
            .disabled(!user.isActive())
            .build();
    }
}
```

여기서 자주 빠뜨리는 한 가지가 있다. `accountLocked`, `disabled`, `accountExpired`, `credentialsExpired` 네 가지 플래그다. 사용자를 "삭제 표시만 하고 행은 남기는" 운영 정책에서, 이 플래그를 안 채우면 비활성 계정도 로그인이 통과한다. 데이터 모델과 보안 모델 사이의 간극이 가장 자주 새는 자리다. 새 `UserDetailsService` 구현을 만들 때마다 네 플래그 매핑을 명시적으로 확인하자.

### 한 가지 더: 빈 등록만으로는 부족할 때

`UserDetailsService`만 등록하고 끝나면 보통 잘 돈다. `DaoAuthenticationProvider`가 자동으로 빈을 골라 쓰기 때문이다. 그러나 사용자 정의 `AuthenticationProvider`를 직접 등록하는 경우, 또는 여러 `UserDetailsService`가 빈 컨테이너에 동시에 있는 경우에는 자동 매칭이 깨진다. 그럴 때는 명시적으로 매니저를 구성한다.

```java
@Bean
DaoAuthenticationProvider authProvider(UserDetailsService uds, PasswordEncoder enc) {
    var provider = new DaoAuthenticationProvider();
    provider.setUserDetailsService(uds);
    provider.setPasswordEncoder(enc);
    return provider;
}
```

`AuthenticationProvider` 빈으로 등록하면 Spring Security가 `ProviderManager`의 위임 목록에 자동으로 추가한다. 빈 이름이 충돌할 일이 없도록 메서드 이름은 명확히 짓자.

## 4.4 HTTP Basic — 매 요청 인증의 단순함과 위험

폼 로그인이 사람을 위한 인증이라면, HTTP Basic은 기계를 위한 인증에 가깝다. `Authorization: Basic ZGVtbzpwYXNzd29yZA==` 한 줄을 매 요청에 붙이면 끝이다. 헤더의 base64를 풀면 `demo:password`가 그대로 보인다. 그래서 HTTPS가 아닌 데서 Basic은 쓰지 않는 편이 낫다. 평문이나 다름없다.

내부 도구, 테스트 자동화, 모놀리식 안의 서버-투-서버 호출 같은 곳에서는 여전히 쓸 만하다. 설정도 한 줄이다.

```java
http.httpBasic(Customizer.withDefaults());
```

`BasicAuthenticationFilter`가 헤더를 읽고 `UsernamePasswordAuthenticationToken`을 만들어 `AuthenticationManager`에 넘긴다. 이후 흐름은 폼 로그인과 동일하다.

### Basic + `STATELESS` 조합

여기서 미묘한 부분이 등장한다. Basic은 매 요청 인증이라, 세션을 만들 필요가 없다. 그런데 기본 설정에서는 세션이 생긴다. 왜? 인증된 `SecurityContext`를 자동으로 세션에 저장해 두기 때문이다. M2M API에서 세션이 늘어나는 건 자원 낭비고, 부하 분산 측면에서도 찜찜하다. 그렇다면 어떻게 해야 할까?

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .httpBasic(Customizer.withDefaults())
        .securityContext(s -> s.requireExplicitSave(true))
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .csrf(CsrfConfigurer::disable)
        .build();
}
```

핵심은 두 줄이다. `requireExplicitSave(true)`로 컨텍스트를 자동 저장하지 않게 하고, `sessionCreationPolicy(STATELESS)`로 세션 생성을 막는다. CSRF도 Basic의 매 요청 자격 증명 모델에서는 의미가 없으므로 disable한다.

세션이 안 만들어지면 `JSESSIONID` 쿠키도 응답에 붙지 않는다. 클라이언트는 매 요청 헤더만 들고 다닌다. 작은 마이크로서비스 사이의 인증, CI에서 호출하는 관리 API 등에 어울리는 구성이다. 함께 다음 장 JWT 자원 서버 구성과 비교해 보면 차이가 또렷해진다. JWT는 토큰 자체가 클레임을 들고 다니지만 Basic은 매번 자격 증명을 그대로 보낸다는 점, 그것만 다를 뿐이다.

## 4.5 Remember-Me — 영원히 사는 듯한 토큰의 찜찜함

`remember-me` 체크박스. 한 번 누르면 브라우저를 닫았다 열어도 로그인이 유지된다. 사용성 측면에서 매력적이고, 그래서 7.0에도 멀쩡히 살아 있다. 그런데 이게 가장 찜찜한 부분이 있다. 토큰이 영원히 사는 듯한 착각, 그게 운영에서 가장 자주 발등을 찍는다.

### 두 가지 모드: Hash vs Persistent

Spring Security의 Remember-Me는 두 가지 구현이 있다.

**Hash-based** 모드는 가장 단순하다. 쿠키 안에 `username + 만료시간 + 해시(username:만료시간:password:key)` 형태의 문자열을 담는다. 서버는 쿠키만 받으면 즉시 검증할 수 있다. 저장소가 필요 없다. 그런데 약점이 보인다. 패스워드 해시를 키 재료로 쓰므로, 패스워드가 바뀌면 토큰이 무효화된다. 그건 좋다. 그러나 토큰이 탈취되면 만료 시점까지는 그대로 사용 가능하다. 무효화할 방법이 없다.

**Persistent** 모드는 토큰을 DB에 저장한다. 쿠키에는 `series`와 `token` 두 식별자만 담는다. 매번 사용될 때마다 `token`을 회전시켜 새 값을 발급한다. 만약 동일한 `series`로 옛날 `token`이 다시 들어오면? 그건 누군가 토큰을 훔쳤다는 신호다. Spring Security는 해당 사용자의 모든 Remember-Me 토큰을 폐기한다.

```java
http.rememberMe(rm -> rm
    .key("change-me-please")
    .tokenValiditySeconds(60 * 60 * 24 * 14)
    .tokenRepository(persistentTokenRepository())
    .userDetailsService(userDetailsService));
```

`tokenRepository`를 지정하면 자동으로 Persistent 모드가 선택된다. 운영에서 Remember-Me를 굳이 쓴다면 Persistent를 쓰는 편이 낫다. 회전과 도난 감지가 들어 있는 점이 결정적이다.

### 모바일과 SPA에는 추천하기 어렵다

Remember-Me는 본질적으로 쿠키 메커니즘이다. 그런데 모바일 네이티브 앱은 쿠키 모델이 어색하다(키체인을 쓰는 게 자연스럽다). SPA는 토큰을 서버에서 받아 클라이언트에서 관리하는 흐름이 흔하다. 둘 다 Remember-Me의 자리가 어색해진다.

오래 머무는 데스크톱 웹, 이메일 클라이언트류 사내 앱, 운영 대시보드 — 이 정도에서는 여전히 유용하다. 그러나 "사용자가 한 달은 로그인을 유지하고 싶다"는 요구를 SPA 환경에서 받으면, Remember-Me로 답하지 말고 OAuth2의 refresh token 회전 모델로 답하는 편이 안전하다. 다음 장에서 다룰 이야기다.

기억해두자. Remember-Me 토큰은 사용자의 두 번째 자격 증명이다. 첫 번째 자격 증명(패스워드)만큼이나 신중하게 만료·회전·도난 감지 정책을 설계해야 한다.

## 4.6 Session Fixation — 가장 오래된 함정 하나

Spring Security가 기본으로 막아 주는 함정 중 가장 우아한 것이 Session Fixation이다. 시나리오는 이렇다.

공격자가 어떤 사이트에 접속해 `JSESSIONID=ABC123` 쿠키를 받는다. 그러고 나서 피해자에게 그 세션 ID를 쓰도록 유도한다(URL에 ID를 박는 옛 방식, XSS로 쿠키 주입 등 방법은 다양하다). 피해자가 그 `JSESSIONID`로 로그인에 성공하면? 서버는 이미 `ABC123` 세션에 인증 정보를 채워 넣는다. 공격자는 자기도 `JSESSIONID=ABC123`을 가지고 있으니, 이제 같은 세션을 공유한다. 끝.

이 끔찍한 일을 막는 표준 대응이 **로그인 직후 세션 ID를 갈아 끼우는 것**이다. Spring Security 기본값은 `migrateSession()`이다. 인증이 성공한 순간, 기존 세션의 속성들은 그대로 가져가되 세션 ID 자체는 새로 발급한다. 공격자가 가진 `ABC123`은 그 순간부터 무용지물이 된다.

기본값이 안전하니 보통은 신경 쓸 일이 없다. 그런데 옵션이 네 가지나 있고, 잘못 고르면 보호가 풀린다.

```java
http.sessionManagement(s -> s
    .sessionFixation(SessionFixationConfigurer::migrateSession));
```

| 옵션 | 의미 | 권장 여부 |
|------|------|----------|
| `migrateSession()` | 세션 ID를 새로 발급하고 기존 속성을 이전 | 기본값, 권장 |
| `newSession()` | 세션 ID도 새로 발급하고 속성도 모두 버림 | 익명 세션에 담겼던 장바구니가 사라지는 등 부작용 가능 |
| `changeSessionId()` | 서블릿 3.1의 `HttpServletRequest.changeSessionId()` 사용 | 컨테이너 의존, 일부 환경에서 마이그레이션 동작과 미묘하게 다름 |
| `none()` | 보호 끔 | 절대 쓰지 말자 |

기본을 그대로 쓰면 안전하다. 그러나 누군가 "세션 정책을 커스텀하겠다"며 손을 댄 코드에서 `.none()`이 박혀 있는 경우를 종종 본다. 보안 코드 리뷰에서 `sessionFixation`을 검색해 보고, `none`이 나오면 즉시 정정하자.

## 4.7 정적 자원은 보안 필터를 태우지 말자

마지막으로 작지만 의외로 많이 새는 부분 하나. CSS, JS, 이미지 같은 정적 자원에 대해서까지 보안 필터를 통과시키는 일이다.

코드는 보통 이런 모양이다.

```java
http.authorizeHttpRequests(a -> a
    .requestMatchers("/css/**", "/js/**", "/images/**").permitAll()
    .anyRequest().authenticated());
```

`permitAll()`로 열어 뒀으니 문제없다고 생각하기 쉽다. 그런데 잘 보자. `permitAll`은 "인가 결정에서 허용"이라는 뜻이지, "필터 체인을 안 태운다"는 뜻이 아니다. 즉, CSS 파일 한 장을 받기 위해 `SecurityContextHolderFilter`부터 `AuthorizationFilter`까지 11개의 필터를 그대로 통과시킨다는 말이다. 페이지 한 번 로딩에 정적 자원 30개가 붙어 있다면? 그 30개 모두 필터 체인을 거친다. 성능적으로 번거롭다.

한 한국 velog 글의 표현을 빌리자면, "보안 필터가 다 필요해서 거치는 게 아니라, 안 빼면 거치게 되는 것"이다. 그렇다면 어떻게 빼낼까?

```java
@Bean
WebSecurityCustomizer webSecurityCustomizer() {
    return web -> web.ignoring()
        .requestMatchers("/css/**", "/js/**", "/images/**", "/favicon.ico");
}
```

`WebSecurityCustomizer`로 ignore 패턴을 정의하면, 매칭된 요청은 Spring Security 필터 체인을 **아예 통과하지 않는다**. 정적 자원처럼 정말로 보안 결정이 필요 없는 경로에 적용하면 응답 속도가 좋아진다.

단 한 가지 주의. ignore에 등록한 경로는 정말로 보안 필터의 보호가 필요 없는 곳이어야 한다. 사용자 데이터가 끼어들거나, 인증된 사용자에게만 보여야 하는 컨텐츠라면 ignore가 아니라 `permitAll`/`authenticated`로 인가 단계에서 결정해야 한다. 잘못 ignore하면 인증 헤더도 안 읽고, CSRF 검증도 안 한다. 보호를 통째로 빼는 셈이다.

기억해두자. `permitAll`은 "통과시키되 검사한다"이고, `ignore`는 "검사도 안 한다"이다. 두 의미를 헷갈리면 곤란하다.

### 7.0 마이그레이션 함정: `WebSecurityCustomizer`를 빼먹는 경우

이게 마이그레이션의 흔한 함정 5번이다. 옛날 `WebSecurityConfigurerAdapter` 시절에는 `configure(WebSecurity)` 메서드를 오버라이드해 ignore 패턴을 잡았다. 어댑터가 사라지고 `SecurityFilterChain` 빈 방식으로 옮겨 오면서, 같은 자리에 ignore가 누락되는 일이 잦다. velog 후기들이 공통적으로 짚는 부분이다. 빌드는 되고 보안도 켜져 있으니 동작은 한다. 그런데 정적 자원 요청까지 필터 11개를 통과해 응답이 느려진다. 직접 측정하지 않으면 모른다.

7.0으로 올릴 때 한 번 점검하자. 옛 코드에 `web.ignoring()`이 있었다면, 새 코드에 `WebSecurityCustomizer` 빈으로 옮겨졌는지 확인하면 된다.

## 4.8 로그인 후 어디로 보낼 것인가

작은 디테일이지만 사용자 경험을 좌우하는 부분이 있다. 로그인 폼에 도착하기 직전에 사용자가 가려던 페이지가 어디든 — 로그인 성공 후 거기로 돌려보내 줘야 자연스럽다. "그렇게 안 해 주면 항상 홈으로 가는 사이트가 되어 버린다.

Spring Security는 이걸 자동으로 해 준다. `ExceptionTranslationFilter`가 인증되지 않은 요청에 대해 `AuthenticationException`을 받으면, 원래 가려던 URL을 `RequestCache`(기본 구현은 `HttpSessionRequestCache`)에 저장한 뒤 로그인 페이지로 보낸다. 인증이 성공하면 `SavedRequestAwareAuthenticationSuccessHandler`가 그 저장된 URL을 꺼내 리다이렉트한다.

```java
http.formLogin(form -> form
    .loginPage("/login")
    .defaultSuccessUrl("/dashboard", false)
    .failureUrl("/login?error"));
```

`defaultSuccessUrl`의 두 번째 인자가 `true`면 항상 그 URL로 보낸다(저장된 요청을 무시한다). `false`면 저장된 요청을 우선한다. 보통은 `false`가 자연스럽다.

여기서도 작은 함정 하나. `loginPage("/login")`을 명시하면 `permitAll`을 같이 잊지 말자. 로그인 페이지를 인증 필요로 잠가 두면 인증 실패 → 로그인 페이지 → 또 인증 실패의 무한 리다이렉트가 만들어진다. 끔찍한 일이다.

## 4.9 로그아웃 — 보기보다 신경 쓸 게 많다

```java
http.logout(Customizer.withDefaults());
```

기본 설정만 켜 두면 `POST /logout`이 자동으로 등록된다. `LogoutFilter`가 가로채 다음 일을 한다.

1. `SecurityContextHolder`를 비운다.
2. 세션을 무효화한다(`invalidateHttpSession(true)` 기본).
3. Remember-Me 쿠키를 삭제한다(설정돼 있다면).
4. `clearAuthentication(true)`로 인증 객체도 정리한다.
5. 로그아웃 후 페이지(`/login?logout` 기본)로 리다이렉트한다.

여기서 짚을 게 두 가지 있다.

**첫째, 로그아웃이 GET이 아니라 POST다.** 왜 그럴까? CSRF 때문이다. 만약 GET으로 로그아웃이 가능하면, `<img src="/logout">` 한 줄을 다른 사이트에 박아 둔 공격자가 사용자가 그 페이지를 여는 순간 우리 사이트에서 로그아웃시켜 버릴 수 있다. 무해해 보이지만 사용자 흐름을 깰 수 있고, 그 사이 다른 공격을 위한 준비 단계가 될 수 있다. POST + CSRF 토큰 조합이 그래서 표준이다.

이걸 GET으로 바꾸고 싶다는 충동이 들 때가 있다. "로그아웃 버튼이 단순 링크였으면 좋겠어요"라는 요청이 들어오면 흔히 그렇게 된다. 그렇다면 CSRF 토큰을 쿼리스트링이나 헤더로 어떻게 실어 보낼지 함께 설계해야 한다. CSRF는 다음 9장에서 자세히 다룬다.

**둘째, OIDC 환경의 로그아웃은 다른 이야기다.** 단순히 우리 세션만 끊는 것으로는 부족하다. IdP 측 세션도 끊지 않으면, 사용자가 다시 IdP에 가서 자동으로 로그인된 채 우리 사이트로 돌아온다. OIDC end_session_endpoint를 호출하는 흐름이 별도로 필요하다. 6장에서 OAuth2 Client + OIDC를 다룰 때 다시 만난다.

## 4.10 정리 — 가장 오래된 방식의 가장 정직한 모습

폼 로그인 한 흐름이 컴포넌트 여섯 개를 거치고, 인코더 한 줄이 보안의 무게를 짊어지고, 세션 ID 하나가 30년 가까이 된 함정을 피해 다닌다. 단순하다고 생각했던 모델 안에 이만큼의 결정이 들어 있다.

핵심 다섯 줄로 정리해 보자.

- 폼 로그인 시퀀스는 `UsernamePasswordAuthenticationFilter` → `AuthenticationManager` → `DaoAuthenticationProvider` → `UserDetailsService` → `PasswordEncoder.matches` → `HttpSessionSecurityContextRepository`다. 갈아 끼울 자리가 다섯이다.
- `PasswordEncoder`는 처음부터 `DelegatingPasswordEncoder`로 시작하자. 7.0의 Password4j 5종 중에서는 새 시스템에 Argon2id가 무난하다.
- `UserDetailsService`를 직접 구현할 땐 `locked / disabled / expired` 플래그 매핑을 빠뜨리지 말자.
- HTTP Basic은 `STATELESS` + `requireExplicitSave(true)`와 함께 쓰자. Remember-Me는 Persistent 모드로, SPA·모바일에는 권하지 말자.
- 정적 자원은 `WebSecurityCustomizer`로 ignore하자. `permitAll`과 의미가 다르다.

다음 5장은 이 모델의 정반대 편을 본다. 세션 없이, 매 요청을 토큰 하나로 인증하는 모델 — JWT 자원 서버. 같은 컴포넌트 모델이 stateless 세계에서 어떻게 다시 그려지는지, 그리고 Bearer 토큰의 본질적 한계를 7.0이 어떻게 sender-constrained 토큰(DPoP)으로 끌고 가는지 함께 살펴보자.
