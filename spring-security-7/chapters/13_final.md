# 13장. 5/6에서 7로 — 마이그레이션 실전 가이드

마이그레이션은 두려운 작업이다. 운영 중인 프로젝트의 `build.gradle`에서 `spring-boot-starter-parent`의 버전 한 줄을 올린 뒤, IDE가 빨갛게 물든 첫 화면을 마주하는 순간을 떠올려보자. `WebSecurityConfigurerAdapter`에 빨간 줄, `antMatchers`에 빨간 줄, `.and()`에 빨간 줄, `authorizeRequests`에 빨간 줄. 한 화면에 빨간 줄이 수십 개씩 들어찬다. 익숙한 코드는 갑자기 낯선 외국어처럼 보이고, 어디서부터 손을 대야 할지 막막함이 몰려온다.

그런데 이 빨간 줄들은 사실 친절한 안내다. 잠시 호흡을 가다듬고 살펴보면, 빨간 줄 하나하나가 "이 부분을 이렇게 바꾸세요"라는 명확한 신호임을 알게 된다. 문제는 빨간 줄의 양이 아니라, 한 번에 모두 바꾸려는 충동이다. 12장까지 살펴본 모든 변경점 — 람다 DSL, `authorizeHttpRequests`, `PathPatternRequestMatcher`, `AuthorizationManager`, OpenSAML 5, Jackson 3 — 이 모두 한 번에 들이닥치면 정말로 끔찍한 일이 된다.

그렇다면 어떻게 해야 할까? 답은 분명하다. **한 번에 모두 바꾸지 말자.** 공식 가이드도, 현장의 경험도 같은 답을 가리킨다. 단계를 쪼개고, 각 단계마다 빌드와 테스트가 초록색이 된 것을 확인한 뒤 다음 단계로 넘어가는 것. 이 장은 그 안전한 단계와, 단계마다 마주칠 함정과, 그 함정을 빠르게 빠져나오는 도구를 정리한다.

이 장은 책의 어느 챕터보다 실무적이다. 1장에서 미리 본 함정 5건의 본격 답이 여기에 있고, 2~12장에서 분산해 다룬 변경점들이 한 곳에 모인다. 마이그레이션 우선 독자가 1장 직후 곧장 13장으로 건너왔다면, 이 장이 곧 책의 첫 본편이 되는 셈이다.

## 13.1 어디서부터 손을 댈까 — 공식 권고 순서

운영 중인 5.x 혹은 6.x 코드베이스가 있다고 해보자. PR 하나로 모든 deprecated 코드를 바꿔 7.0으로 올리는 시나리오를 상상해 본다. 변경 파일 200개, 라인 수 5000줄, 리뷰어는 망연자실, 회귀 테스트는 어디서 깨졌는지 추적 불가. 끔찍한 일이다.

Spring 팀이 권하는 순서는 정반대다. 한 마디로 요약하면 이렇다.

> **6.5 patch → 6.5 preparation step → 7.0 점프.**

세 단계로 쪼개진 이 길이 마이그레이션의 가장 짧은 경로다. 각 단계에서 정확히 무엇을 하는지 차근차근 살펴보자.

### 1단계 — 가장 최신 6.5 패치로 올리기

먼저 현재 코드를 **Spring Boot 3.5 / Spring Security 6.5 최신 패치**로 끌어올린다. 5.x에서 곧장 7.0으로 가는 건 권장하지 않는다. 5.x → 6.x 점프 자체가 만만치 않은 변화였기 때문이다(예: 6.0에서 `WebSecurityConfigurerAdapter` 제거, Spring Boot 3 = Java 17 강제, Jakarta EE 9 네임스페이스 전환). 5.x 사용자라면 일단 6.x로 한 차례 정착하고 거기서 다시 7.0을 보는 편이 안전하다.

이미 6.x를 쓰고 있다면 6.5의 마지막 patch(집필 시점 6.5.7 이상)까지 올리자. 6.5는 Spring 팀이 의도적으로 만든 **7.0의 전실(antechamber)** 이다. 6.5에서 deprecated 표시된 API들은 곧 7.0에서 제거될 항목이고, 6.5는 그것을 가능한 한 빨리 알려주려 한다. 컴파일러 경고가 마이그레이션 todo 리스트가 되는 셈이다.

### 2단계 — 6.5 preparation step 적용

이게 마이그레이션의 진짜 본체다. 공식 docs의 `migration-7/` 챕터에 정리된 항목을 6.5에서 미리 다 끝낸다. 핵심은 다음 다섯 가지다.

1. `antMatchers` / `mvcMatchers` / `regexMatchers` → `requestMatchers`
2. `.and()` 체이닝 → Lambda DSL
3. `apply(...)` → `with(...)`
4. `AuthorizationManager#check` 사용처 → `authorize`
5. Jackson 3 호환 검증 (`SecurityJacksonModules`)

각 항목은 뒤의 절에서 자세히 본다. 여기서 짚어둘 한 가지는, **이 단계는 여전히 6.5에서 한다**는 점이다. 즉, 패키지 좌표는 그대로고 의존성도 바뀌지 않는다. 코드만 새 어법으로 옮긴다. 이 단계에서 CI가 초록불을 유지하면, 7.0 점프는 정말로 "버전 숫자 하나 올리기"에 가까워진다.

### 3단계 — CI에서 deprecation warning 0 확인

2단계가 끝났다는 신호는 무엇일까? 단순하다. **CI 로그에 Spring Security 관련 deprecation warning이 하나도 안 나오는 것.** 빌드 스크립트에 `-Werror` 또는 `-Xlint:deprecation`을 켜고 빌드를 돌려보자. 6.5에서 deprecated였던 호출이 한 곳이라도 남아 있으면, 7.0 빌드는 그곳에서 컴파일 에러로 멈춘다. 미리 0으로 만들어두는 편이 훨씬 낫다.

### 4단계 — 7.0 점프

여기서 비로소 의존성을 바꾼다.

```gradle
// build.gradle.kts
implementation("org.springframework.boot:spring-boot-starter-web") // Spring Boot 4
implementation("org.springframework.boot:spring-boot-starter-security") // Security 7
```

Spring Boot 4.0이 Spring Security 7.0을 기본으로 묶기 때문에, 보통 `spring-boot-starter-parent` 또는 `dependency-management` 좌표 한 줄을 4.0.x로 올리는 것으로 끝난다. 만약 2단계의 청소가 깔끔했다면, 이 점프에서 새로 빨갛게 변하는 곳은 **잔여 deprecation**(즉 6.5에서 놓친 것)과 **SAML/LDAP/Jackson 같은 영역별 변경**뿐일 가능성이 높다.

### 5단계 — 영역별 정리

마지막으로 다음 세 가지를 점검한다.

- SAML 사용처라면 OpenSAML 5 의존성 명시 (§13.8)
- LDAP 사용처라면 UnboundID 확인 (§13.9)
- Spring Authorization Server를 운영한다면 `spring-security-oauth2-authorization-server:7.0.0`으로 좌표 교체 (§13.10)

다섯 단계 모두 마쳤다면, 빌드는 초록색이고 deprecation 경고는 0이고 운영 동작은 변하지 않은 상태가 된다. 그게 안전한 마이그레이션의 끝이다.

> **표 13-1. 마이그레이션 5단계 체크리스트**
>
> | 단계 | 행동 | 신호 |
> |------|------|------|
> | 1 | Spring Boot 3.5 + Security 6.5 최신 patch로 올림 | 빌드 초록 |
> | 2 | 6.5 preparation step의 5개 항목 일괄 치환 | 코드 컴파일 통과 |
> | 3 | CI에서 deprecation warning 0 확인 | 경고 0 |
> | 4 | Spring Boot 4.0 + Security 7.0으로 점프 | 빌드 초록 |
> | 5 | SAML / LDAP / Authorization Server 영역별 정리 | 통합 테스트 통과 |

## 13.2 deprecation에서 제거까지 — 한눈에 보는 매핑표

마이그레이션의 본질은 결국 **어떤 API가 어디서 사라졌는가**를 아는 것이다. 5.x/6.x에서 익숙했던 API를 6.5와 7.0이 어떻게 처리하는지, 한 표로 정리해 두자.

> **표 13-2. deprecation → 제거 매핑표**
>
> | 5.x / 6.x 어법 | 6.5 (전환기) | 7.0 (현재) | 본 책 cross-ref |
> |----------------|---------------|------------|------------------|
> | `WebSecurityConfigurerAdapter` 상속 | deprecated (빈 등록 권고) | **이미 6.0에서 제거됨** | §13.4 |
> | `antMatchers()`, `mvcMatchers()`, `regexMatchers()` | deprecated, `requestMatchers()` 권고 | 제거 — `PathPatternRequestMatcher` 통일 | §13.6 |
> | `authorizeRequests(...)` | deprecated | 제거 — `authorizeHttpRequests`만 | §13.5 |
> | `.and()` 체이닝 | deprecated | 제거 — Lambda DSL 강제 | §13.5 |
> | `HttpSecurity#apply(...)` | deprecated, `.with(...)` 권장 | 제거 | §13.5 |
> | `AccessDecisionManager` / `AccessDecisionVoter` | 5.5부터 deprecated | 별도 모듈(`spring-security-access`)로 분리 | 3장 §3.x, 8장 |
> | `AuthorizationManager#check` | deprecated | 제거 — `authorize`만 남음 | 8장 |
> | `AntPathRequestMatcher` | deprecated | 제거 | §13.6 |
> | OAuth2 Password Grant | deprecated | 완전 제거 (RFC 9700/OAuth 2.1 동조) | 6장 |
> | OpenSAML 4 | 6.x에서 5도 옵션 | OpenSAML 4 지원 제거 | §13.8 |
> | Jackson 2 modules (`SecurityJackson2Modules`) | 6.x 기본 | Jackson 3 기본 (`SecurityJacksonModules`) | §13.7 |

이 표가 13장의 지도다. 본인의 코드베이스를 grep으로 한 번씩 훑으며 위 키워드가 어디에 얼마나 남아 있는지 파악해두자. 이게 마이그레이션 작업량을 산정하는 가장 빠른 방법이다.

```bash
# 코드베이스 진단용 grep — 마이그레이션 전 한 번
grep -rn "WebSecurityConfigurerAdapter" src/ test/
grep -rn "antMatchers\|mvcMatchers\|regexMatchers" src/ test/
grep -rn "authorizeRequests" src/ test/
grep -rn "\.and()" src/ test/    # 오탐 많음, 결과는 눈으로 필터링
grep -rn "@EnableGlobalMethodSecurity" src/ test/
grep -rn "AccessDecisionManager\|AccessDecisionVoter" src/ test/
grep -rn "SecurityJackson2Modules" src/ test/
grep -rn "AntPathRequestMatcher\|MvcRequestMatcher" src/ test/
```

각 명령의 출력 라인 수를 적어두면, "오늘은 antMatchers 50군데 중 30군데 정리"처럼 진행률을 추적할 수 있다. 막연한 두려움을 구체적인 todo 리스트로 바꾸는 작업이다.

## 13.3 자동화부터 시작하자 — OpenRewrite

이쯤 되면 한 가지 의문이 든다. "이 단순 치환을 정말 사람이 손으로 해야 할까?" 정답은 "아니다"다. 단순 패턴 치환은 도구가 더 정확하고 빠르다. 손으로 하면 50번째쯤에서 반드시 한 곳을 빼먹는다. 그게 사람이다.

마이그레이션 자동화의 표준 도구는 **OpenRewrite**다. `rewrite-spring` 레시피가 Spring Security 6.4/6.5의 주요 deprecation을 자동 치환해 준다.

### Gradle에서 한 번 돌려보기

`build.gradle.kts`에 다음과 같이 OpenRewrite 플러그인을 추가한다.

```kotlin
plugins {
    id("org.openrewrite.rewrite") version "6.27.0"  // 집필 시점 기준, 최신 확인
}

rewrite {
    activeRecipe(
        "org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_5",
        "org.openrewrite.java.spring.security6.UpgradeSpringSecurity_6_5",
    )
}

dependencies {
    rewrite("org.openrewrite.recipe:rewrite-spring:5.x.x")  // 최신 확인
}
```

그리고 다음 명령을 돌린다.

```bash
./gradlew rewriteDryRun        # 변경 미리보기 (안전, 파일을 안 바꿈)
./gradlew rewriteRun           # 실제 적용
```

`rewriteDryRun`이 출력하는 diff를 한 번 훑어보자. 한 번에 수십~수백 파일을 자동으로 새 어법으로 바꿔주는 것을 보면, 의외로 마이그레이션이 별것 아니구나 하는 안도감이 든다.

### Maven에서 돌리기

```bash
mvn org.openrewrite.maven:rewrite-maven-plugin:dryRun \
    -Drewrite.activeRecipes=org.openrewrite.java.spring.security6.UpgradeSpringSecurity_6_5 \
    -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:LATEST

mvn org.openrewrite.maven:rewrite-maven-plugin:run \
    -Drewrite.activeRecipes=org.openrewrite.java.spring.security6.UpgradeSpringSecurity_6_5 \
    -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:LATEST
```

### 도구의 한계 — 자동화가 닿지 못하는 곳

OpenRewrite는 강력하지만 만능은 아니다. 다음과 같은 변경은 사람의 판단이 필요하다.

- **`WebSecurityConfigurerAdapter` 상속 → `SecurityFilterChain` 빈으로 구조 자체 전환** 일부는 자동화되지만, `configure(WebSecurity)` 같은 메서드의 내용은 사람의 개입이 필요한 경우가 많다.
- **`AccessDecisionManager` → `AuthorizationManager`** 의미는 비슷하지만 인터페이스가 다르고 voter 합산 로직이 다르다. 자동 변환은 위험하다.
- **OpenSAML 4 → OpenSAML 5** 의존성 좌표뿐 아니라 `AssertingPartyDetails` → `AssertingPartyMetadata` API 모양이 바뀌었다.
- **Jackson 2 → Jackson 3** ObjectMapper 구성을 직접 만진 곳은 모두 손봐야 한다.

OpenRewrite를 먼저 돌려 80%를 치우고, 남은 20%를 사람이 손으로 정리하는 흐름이 가장 빠르고 가장 안전하다. 처음부터 손으로 다 하려고 들지 말자.

## 13.4 첫 번째 큰 산 — `WebSecurityConfigurerAdapter`

본격적인 항목별 가이드는 가장 큰 산부터 시작한다. **5.x 코드를 6.x로 옮길 때 사람들이 가장 먼저 부딪히는 벽**이 바로 이것이다. 정확히 말하면 이 변경은 **6.0에서 이미 일어난 일**이다. 즉, 7.0이 새로 가져온 변화는 아니다. 다만 7.0으로 가는 길이 곧 6.x를 거치는 길이고, 아직도 운영 코드에 5.x 잔재가 남아 있는 프로젝트가 흔하다. 그래서 13장 가장 앞에 둔다.

### 5.x 어법

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/", "/login", "/signup", "/css/**").permitAll()
                .anyRequest().authenticated()
            .and()
            .formLogin()
            .and()
            .logout()
            .and()
            .csrf();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService).passwordEncoder(passwordEncoder());
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

이 코드를 보면 어떤 느낌이 드는가? 5.x를 오래 쓴 개발자에게는 익숙하고 자연스러운 모양이다. 그런데 Spring 7.0에서는 이 코드의 **거의 모든 부분**이 빨갛게 변한다. `WebSecurityConfigurerAdapter` 자체가 사라졌고, `authorizeRequests`도, `antMatchers`도, `.and()`도, `configure(AuthenticationManagerBuilder)`도 전부 없다. 7.0 코드에서는 빨간 줄이 안 나오는 부분이 `@Configuration`과 `@Bean`뿐이다.

### 7.0 어법

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain web(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(a -> a
                .requestMatchers("/", "/login", "/signup", "/css/**").permitAll()
                .anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .logout(Customizer.withDefaults())
            .csrf(Customizer.withDefaults())
            .build();
    }

    @Bean
    AuthenticationManager authenticationManager(
            UserDetailsService userDetailsService,
            PasswordEncoder passwordEncoder) {
        var provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder);
        return new ProviderManager(provider);
    }

    @Bean
    PasswordEncoder passwordEncoder() {
        return new Argon2Password4jPasswordEncoder();  // 7.0 신규 (Cryptography 절)
    }
}
```

차이를 짚어보자. 첫째, **상속이 사라졌다**. 더 이상 `extends WebSecurityConfigurerAdapter`가 없다. `@Configuration` 클래스 안에 보통 `@Bean` 메서드들로 설정을 노출한다. 둘째, **`SecurityFilterChain`을 빈으로 반환**한다. `HttpSecurity`가 어디서 어떻게 만들어지는지 신경 쓸 필요 없이, 매개변수로 받아 빌더 호출 후 `build()`로 끝낸다. 셋째, **`AuthenticationManager`도 명시적 빈**이다. 5.x의 `configure(AuthenticationManagerBuilder)` 콜백 대신, `AuthenticationManager` 빈을 직접 등록한다.

이 모양이 익숙해지면 5.x 어법이 오히려 어색해 보인다. 클래스 상속은 결합도가 높고, `configure(...)` 콜백은 "이 메서드가 언제 호출되는지", "내가 만든 객체가 누구에게 전달되는지"가 불투명하다. 빈 등록은 의존성 그래프가 명시적이다. Spring 답다고 할 수 있다.

### 마이그레이션 팁

- `configure(WebSecurity)`로 정적 자원 무시 처리를 했다면 → `WebSecurityCustomizer` 빈으로 옮긴다(§13.11 함정 5 참고).
- `configure(AuthenticationManagerBuilder)`로 여러 provider를 등록했다면 → 각 provider를 빈으로 만들고 `ProviderManager` 빈으로 묶는다.
- 클래스 한 개에 다 들어가던 5.x 코드를 → `@Configuration` 클래스 한 개로 그대로 옮겨도 무방하다. 굳이 클래스를 쪼갤 필요는 없다.

## 13.5 두 번째 — Lambda DSL과 `authorizeHttpRequests`

`WebSecurityConfigurerAdapter`가 첫 번째 큰 산이라면, **Lambda DSL의 강제**는 두 번째 큰 산이다. 7.0에서 `HttpSecurity.and()`가 완전히 삭제됐다. 이제 모든 설정은 람다 안에서 이어져야 한다.

### 5.x/6.x 어법 (체이닝 + `.and()`)

```java
http
    .authorizeRequests()
        .antMatchers("/api/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated()
        .and()
    .formLogin()
        .loginPage("/login")
        .permitAll()
        .and()
    .logout()
        .logoutSuccessUrl("/")
        .and()
    .csrf().disable();
```

이 코드의 문제는 무엇일까? Spring 공식 블로그가 한 마디로 정리한다.

> "The previous configuration approach was unclear about what object was getting configured without knowing the return type, and the deeper the nesting the more confusing it became."

`.permitAll()`이 무엇에 대한 permitAll인지, `.disable()`이 어디서 끝나는지, `.and()` 하나가 위로 몇 단계를 올라가는지 모호하다. 코드를 처음 보는 사람에게는 정말 난감한 구조다. 들여쓰기에 의존해 의미를 추측해야 하기 때문이다.

### 7.0 어법 (Lambda DSL 강제)

```java
http
    .authorizeHttpRequests(a -> a
        .requestMatchers("/api/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated())
    .formLogin(form -> form
        .loginPage("/login")
        .permitAll())
    .logout(logout -> logout
        .logoutSuccessUrl("/"))
    .csrf(CsrfConfigurer::disable);
```

람다 안의 모든 호출이 한 객체(`AuthorizeHttpRequestsConfigurer` 등)에 한정된다는 사실이 코드에 박혀 있다. `permitAll()`이 form login의 일부라는 게 들여쓰기뿐 아니라 람다 스코프로도 명확하다. 자동완성도 명확하다(IntelliJ가 람다 인자의 타입을 알기 때문에). `.and()`를 헤맬 일이 없다.

### `authorizeRequests` → `authorizeHttpRequests`

이름 차이가 단순한 리네임이 아니라는 점은 짚어두자. 두 API의 **내부 모델이 다르다**.

- `authorizeRequests`: 구 모델. `AccessDecisionManager` + `AccessDecisionVoter` 기반.
- `authorizeHttpRequests`: 신 모델. `AuthorizationManager` 기반(8장 참고).

7.0에서 `authorizeRequests`는 완전히 사라진다. 신 모델은 단일 함수형 인터페이스(`AuthorizationManager#authorize`)로 단순해졌고, AND/OR 조합도 `AllAuthoritiesAuthorizationManager` 같은 매니저로 처리한다. 차이가 단지 이름만이 아니라 인가 모델의 세대 차라는 것을 기억해두자.

### `apply(...)` → `with(...)`

체이닝 변경의 곁가지로, **커스텀 Configurer를 적용하는 메서드**도 바뀌었다.

```java
// 6.x
http.apply(new MyCustomConfigurer());

// 7.0
http.with(new MyCustomConfigurer(), Customizer.withDefaults());
```

`with(...)`는 두 번째 인자로 `Customizer`를 받아 람다 일관성을 유지한다. 마이그레이션할 때 잊지 말자.

> **5분 박스: Lambda DSL 핵심 3원칙**
>
> 1. 모든 최상위 설정 메서드는 `Customizer<X>`를 받는다. 변경할 게 없으면 `Customizer.withDefaults()`.
> 2. 람다 내부에서 더 이상 `.and()`로 나오지 않는다. 종료는 람다 끝(`)`)이다.
> 3. 메서드 레퍼런스 단축: `csrf(CsrfConfigurer::disable)`, `csrf(CsrfConfigurer::spa)` 같이 자주 쓰이는 패턴은 한 줄로 끝난다.

## 13.6 세 번째 — 매처 일괄 전환

세 번째 큰 변화는 **요청 매처의 완전 통일**이다. 7.0에서 `AntPathRequestMatcher`와 `MvcRequestMatcher`가 모두 제거되고, **`PathPatternRequestMatcher`만** 남는다.

### 왜 통일했나

5.x 시절을 떠올려보자. 한 클래스 안에서 누군가는 `antMatchers("/api/**")`를, 다른 누군가는 `mvcMatchers("/api/**")`를 썼다. 두 매처는 미묘하게 다르다. `MvcRequestMatcher`는 Spring MVC의 경로 매칭 규칙을 따라 `/api`와 `/api/`를 같은 것으로 보정한다. `AntPathRequestMatcher`는 그런 보정이 없다. 이게 잘못 섞이면 어떤 일이 벌어질까? 같은 경로에 대해 403과 200이 일관성 없이 튀어나오는, 정말 디버깅하기 끔찍한 상황이 된다.

7.0의 `PathPatternRequestMatcher`는 Spring Framework 6의 `PathPattern` 엔진(Spring MVC와 WebFlux가 공유하는 새 경로 매칭 엔진)을 그대로 사용한다. 이제 매처 종류로 인한 불일치가 사라진다. 좋은 일이다.

### 변환 예시

```java
// 6.x — 혼재된 매처
.authorizeHttpRequests(a -> a
    .requestMatchers(antMatchers("/static/**")).permitAll()
    .requestMatchers(mvcMatchers("/api/admin")).hasRole("ADMIN")
    .anyRequest().authenticated())

// 7.0 — PathPattern 단일
.authorizeHttpRequests(a -> a
    .requestMatchers("/static/**").permitAll()           // 문자열 직접
    .requestMatchers("/api/admin").hasRole("ADMIN")      // PathPattern 자동
    .anyRequest().authenticated())
```

문자열만 넘기는 `requestMatchers(String...)`이 가장 일반적인 형태다. 내부적으로 `PathPatternRequestMatcher`가 만들어진다.

만약 HTTP 메서드 한정이 필요하다면:

```java
.requestMatchers(HttpMethod.POST, "/api/orders").hasRole("USER")
.requestMatchers(HttpMethod.GET, "/public/**").permitAll()
```

만약 직접 `RequestMatcher` 인스턴스를 만들어 쓰던 곳이 있다면:

```java
// 6.x
RequestMatcher matcher = new AntPathRequestMatcher("/api/**");

// 7.0
RequestMatcher matcher = PathPatternRequestMatcher.withDefaults().matcher("/api/**");
```

`AntPathRequestMatcher`를 직접 인스턴스화한 코드가 있다면, 마이그레이션 시 grep으로 한 번에 잡아 모두 위의 패턴으로 바꿔야 한다.

### 부수 효과 — 상대 경로 리다이렉트

매처 통일과 함께 들어온 작은 변화 하나를 짚어둘 만하다. 7.0에서 **`LoginUrlAuthenticationEntryPoint`가 기본적으로 상대 경로 리다이렉트**를 사용한다. 역프록시(Nginx 등) 뒤에서 hostname이 컨테이너 내부 이름으로 잡히는 문제가 완화된다. 만약 절대 경로가 필요한 케이스가 있다면 명시적으로 설정해야 하지만, 대부분의 경우는 더 잘 동작한다.

## 13.7 Jackson 2에서 Jackson 3으로

이 절은 짧지만 잊으면 따끔하다. 7.0의 기본 직렬화 라이브러리가 **Jackson 3**이다. Spring Security가 SecurityContext, Authentication, OAuth2 토큰 정보 등을 세션/쿠키/Redis 등에 저장할 때 쓰는 mixin 모듈도 함께 바뀌었다.

### 변환

```java
// 6.x
ObjectMapper mapper = new ObjectMapper();
mapper.registerModules(SecurityJackson2Modules.getModules(loader));

// 7.0
ObjectMapper mapper = new ObjectMapper();
mapper.registerModules(SecurityJacksonModules.getModules(loader));
```

좌표 자체는 한 글자가 바뀐 셈이지만(`Jackson2` → `Jackson`), 내부적으로 Jackson 3 API에 의존하므로 직접 ObjectMapper를 만들어 쓰던 곳이 있다면 의존성 트리도 점검해야 한다.

### 진짜 함정은 직렬화 호환성

진짜 주의할 곳은 **운영 환경에서 이전 버전이 직렬화한 데이터를 7.0이 읽을 때**다. Redis에 저장된 세션, RememberMe 토큰의 직렬화 형식 등에서 호환성 이슈가 발생할 수 있다. 무중단 배포라면 잠시 양쪽 버전이 공존하는 시점이 있는데, 이때 한쪽이 쓴 데이터를 다른 쪽이 못 읽는 사태가 벌어질 수 있다.

해법은 단순하다. 마이그레이션 전에 **세션 저장소를 비우거나, 만료 시간을 짧게 잡고 단계적으로 만료시키는** 것이다. RememberMe 쿠키는 사용자가 다시 로그인하면 자연스레 새 형식으로 교체된다. 운영 점검 시점에 신경 써둘 항목이다.

## 13.8 SAML — OpenSAML 4에서 5로

SAML 사용자가 아니라면 이 절은 건너뛰어도 좋다. 다만 사용자라면 의외로 손이 많이 가는 변경이라 짚어둔다.

### 의존성 좌표

OpenSAML은 메이븐 좌표가 까다롭다. 7.0에서는 다음과 같이 명시한다.

```xml
<repositories>
    <repository>
        <id>shibboleth</id>
        <url>https://build.shibboleth.net/maven/releases/</url>
    </repository>
</repositories>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-saml2-service-provider</artifactId>
</dependency>
<dependency>
    <groupId>org.opensaml</groupId>
    <artifactId>opensaml-core-impl</artifactId>
    <version>5.x.x</version>
</dependency>
```

shibboleth 리포지토리는 OpenSAML이 Maven Central에 직접 올라오지 않기 때문에 추가가 필요하다. 6.x에서 4 버전을 쓰고 있었다면 5로 명시 업그레이드한다.

### API 변경 — `AssertingPartyDetails` → `AssertingPartyMetadata`

코드 레벨의 핵심 변경은 인터페이스 명 변경이다.

```java
// 6.x
RelyingPartyRegistration registration = RelyingPartyRegistrations
    .fromMetadataLocation("https://idp.example.com/metadata.xml")
    .registrationId("okta")
    .build();

// AssertingPartyDetails details = registration.getAssertingPartyDetails();
// details.getEntityId();

// 7.0
// AssertingPartyMetadata metadata = registration.getAssertingPartyMetadata();
// metadata.getEntityId();
```

기존 `AssertingPartyDetails` 클래스가 `AssertingPartyMetadata` 인터페이스로 교체됐다. 의미는 같지만 추상화가 정돈된 셈이다. JDBC 기반 `AssertingPartyMetadataRepository`도 추가됐으니, 메타데이터를 DB에 저장하는 운영이라면 함께 살펴볼 만하다.

직접 `AssertingPartyDetails`를 import해 쓰던 코드가 있다면 grep으로 잡아 모두 `AssertingPartyMetadata`로 바꿔야 한다. IDE가 자동으로 추천하긴 하지만 인터페이스 메서드 시그니처가 미묘하게 다를 수 있어 컴파일 에러를 따라가며 정리하는 편이 안전하다.

## 13.9 LDAP — ApacheDS 제거, UnboundID로 통일

이것도 짧다. 7.0에서 `ApacheDsContainer`와 Apache DS 기반 임베디드 LDAP 지원이 **완전히 제거**됐다. 임베디드 LDAP은 이제 UnboundID 한 가지만 남는다.

```java
// 6.x — ApacheDS 임베디드
@Bean
DefaultSpringSecurityContextSource contextSource() {
    var server = new ApacheDsContainer(...);
    server.start();
    return new DefaultSpringSecurityContextSource(...);
}

// 7.0 — UnboundID 임베디드
@Bean
EmbeddedLdapServerContextSourceFactoryBean ldap() {
    var factory = EmbeddedLdapServerContextSourceFactoryBean.fromEmbeddedLdapServer();
    factory.setLdif("classpath:users.ldif");
    factory.setPort(0);  // 임의 포트
    return factory;
}
```

운영 LDAP(외부 디렉터리 서버) 연동은 영향이 없다. 테스트에서 임베디드 LDAP을 띄우던 코드만 손보면 끝이다. UnboundID는 Spring Security 6.x부터 이미 기본 권장이었으므로 대부분 6.x 시점에서 이미 옮겼을 가능성이 높다. ApacheDS 잔재가 있는지 한 번 확인하는 정도로 충분하다.

## 13.10 Spring Authorization Server 흡수

7.0에서 의외로 큰 정리 작업 중 하나가 **Spring Authorization Server의 본가 흡수**다. 별도 프로젝트였던 Authorization Server가 Spring Security 산하로 들어왔다. 의존성 좌표가 바뀐다.

```xml
<!-- 6.x 시절 (별도 프로젝트) -->
<!-- <artifactId>spring-security-oauth2-authorization-server</artifactId>
     <version>1.x.x</version> -->

<!-- 7.0 -->
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-oauth2-authorization-server</artifactId>
    <version>7.0.0</version>
</dependency>
```

좋은 소식은 **패키지 경로와 클래스 이름은 거의 그대로 유지**된다는 점이다. import 문을 일일이 바꿀 필요는 없다. 다만 두 가지를 짚어두자.

첫째, **Authorization Server에서 PKCE가 기본 활성화**됐다. 클라이언트가 PKCE를 명시적으로 끄지 않는 한 자동으로 강제된다. 6장에서 다뤘듯 confidential client에서도 PKCE를 쓰는 게 RFC 9700의 권고고, 7.0이 그 권고를 default로 끌어들였다.

둘째, **OAuth 2.0 Dynamic Client Registration Protocol** 지원이 추가됐다. 운영 중에 클라이언트를 동적으로 등록하는 시나리오(다중 테넌트, 외부 통합)에서 유용하다.

다만 솔직하게 짚어둘 부분이 있다. Authorization Server의 흡수는 **2026년 5월 집필 시점에도 일부 영역이 정착 중**이다. 책을 덮은 뒤에는 공식 docs의 migration 가이드를 한 번 더 확인하자. 특히 자체 Authorization Server를 운영한다면, 7.1.x milestone에서 추가 변경이 있을 가능성이 있다.

## 13.11 함정 5건 — 마이그레이션 첫 빌드에서 만나는 풍경

지금까지 살펴본 항목별 가이드를 알고 있어도, 첫 빌드에서는 반드시 무언가가 깨진다. 그게 마이그레이션의 본성이다. 이 절에서는 운영 현장에서 가장 흔히 보고되는 함정 다섯 가지를 정리한다. 1장에서 미리본 표가 여기서 본격적인 답을 만난다.

### 함정 1. Stack Overflow 2019년 답변 복붙

> "Most Spring Security problems in code review come from copy-pasting a Stack Overflow answer from 2019 using `WebSecurityConfigurerAdapter`." — Toptal Spring Tutorial

이 코드를 본 적이 있는가? 신입 개발자가 Spring Security 설정을 검색해 가져온 첫 코드. `WebSecurityConfigurerAdapter`를 상속하고, `authorizeRequests().antMatchers(...)`로 시작하고, `.and()`를 줄줄이 늘어놓은, 2019년 풍의 코드. 빌드는 어찌어찌 통과되는데, 실제로 요청을 보내면 인증이 안 되거나 권한 체크가 무력화되거나, deprecated 경고가 콘솔을 뒤덮는다. 디버깅하기 정말 끔찍하다.

**왜 위험한가:** 컴파일은 되는데 동작이 어긋난다. 6.x에서는 `WebSecurityConfigurerAdapter`가 deprecated 표시만 띄울 뿐 동작은 한다(또는 일부만 한다). 7.0에서는 그 클래스 자체가 없으니 컴파일 에러로 멈춘다. 컴파일 에러는 차라리 친절한 신호다. 무서운 건 "되긴 되는데 안 되는" 6.x 시절의 잿빛 영역이다.

**해법:** 신뢰 가능한 1차 출처에서만 코드를 가져오자. 공식 reference docs의 예제, Spring Security GitHub 샘플 리포지토리, Spring 공식 블로그. 검색 결과에서 가장 위에 뜬다고 해서 시간순으로 정렬해보지 않으면, 2019년 글이 첫 결과인 경우가 흔하다. 글 작성일을 반드시 확인하자.

이 책의 코드 예제는 모두 7.0 기준으로 작성됐다. 책을 곁에 두고 복사하면 적어도 SO 2019 함정은 피한다.

### 함정 2. `@EnableGlobalMethodSecurity` 잔존

```java
// 5.x 잔재
@EnableGlobalMethodSecurity(prePostEnabled = true, securedEnabled = true)
@Configuration
public class MethodSecurityConfig { }
```

이 어노테이션이 한 군데라도 남아 있으면, **`@PreAuthorize`가 소리 없이 무력화**된다. 컴파일 에러도 없고, 런타임 경고도 없고, 단지 `@PreAuthorize`가 적용된 메서드가 누구나 호출 가능해진다. 정말로 찜찜한 상황이다(실제 6.2.7 issue #17487로 보고된 사례다).

**왜 위험한가:** `@EnableGlobalMethodSecurity`와 `@EnableMethodSecurity`가 한 컨텍스트에 공존하면 메서드 보안 설정이 충돌하거나, 어느 한쪽이 적용되지 않는 미묘한 상태가 된다. 잘못된 한쪽이 적용되면 보안 게이트가 통째로 열린다.

**해법:** 마이그레이션 시 다음 한 줄을 반드시 돌리자.

```bash
grep -rn "@EnableGlobalMethodSecurity" src/ test/
```

결과가 0줄이어야 한다. 한 군데라도 있다면 `@EnableMethodSecurity`로 교체한다. 두 어노테이션의 default가 살짝 다르므로 옵션도 확인하자.

```java
// 7.0 권장
@EnableMethodSecurity  // prePostEnabled=true가 default
@Configuration
public class MethodSecurityConfig { }
```

추가로, 메서드 보안의 동작은 통합 테스트로 반드시 검증하자. 권한이 부족한 사용자가 호출하면 `AccessDeniedException`이 나는지, 12장에서 다룬 `@WithMockUser`로 회귀 테스트를 짜두면 이 함정에 다시 빠질 일이 없다.

### 함정 3. `.and()` 체이닝 잔존

```java
// 7.0에서 컴파일 에러
http.csrf().disable().authorizeRequests().anyRequest().authenticated().and().formLogin();
```

이 코드는 7.0에서 빨갛게 변한다. `.and()`가 없기 때문이다. **마이그레이션 첫 빌드에서 가장 많이 보이는 에러**가 바로 이것이다. IntelliJ가 한 화면에 빨간 줄을 수십 개 뿌리는데, 그 대부분이 `.and()`다.

**왜 발생하는가:** `.and()`는 빌더의 부모로 한 단계 올라가는 어법이었다. Lambda DSL은 부모 객체를 직접 노출하지 않으므로 `.and()`가 의미를 잃는다.

**해법:** OpenRewrite가 가장 잘 처리하는 패턴이다. §13.3의 `./gradlew rewriteRun`을 돌리면 `.and()` 체인이 람다 형태로 자동 변환된다. 자동화로 안 잡힌 잔여분은 컴파일 에러를 따라가며 손으로 정리하면 된다. IntelliJ의 "Spring Security DSL" 인스펙션도 도움이 된다.

손으로 변환할 때 한 가지 팁: **한 번에 한 메서드만 변환**하자. `csrf().disable()` 한 줄을 `csrf(CsrfConfigurer::disable)`로 바꾸고 빌드 → 다음 줄로 넘어가는 식. 람다 스코프를 잘못 닫아 의도와 다른 객체에 호출이 붙는 실수를 막을 수 있다.

### 함정 4. mvc / ant 매처 혼합

```java
// 6.x — 같은 클래스 안에서 두 매처가 혼재
.requestMatchers(antMatchers("/api/users")).hasRole("USER")
.requestMatchers(mvcMatchers("/api/orders")).hasRole("USER")
```

이 코드의 문제는 §13.6에서 살짝 짚었다. 두 매처는 trailing slash 같은 경계 상황에서 다르게 동작한다. `/api/users`와 `/api/users/`를 한쪽은 같은 것으로, 다른 쪽은 다른 것으로 본다. 인가 정책이 일관성을 잃는다. 정말 디버깅하기 끔찍한 종류의 버그다.

**왜 발생하는가:** 코드베이스에 두 매처가 섞이는 건 보통 여러 개발자가 다른 시점에 코드를 추가했기 때문이다. 한쪽은 2020년 풍, 다른 쪽은 2022년 풍. 결과적으로 같은 컨트롤러를 보호하는 두 규칙이 다르게 매칭된다.

**해법:** 7.0에서는 이 함정이 **자동으로 해결**된다. `PathPatternRequestMatcher` 하나만 남기 때문이다. 마이그레이션 후에는 매처가 혼재할 가능성 자체가 사라진다. 좋은 일이다.

다만 7.0으로 옮기는 과정에서 한 가지 회귀를 점검하자. `MvcRequestMatcher`가 적용되던 경로(예: `/api/users` ↔ `/api/users/`)의 매칭 결과가 미세하게 바뀔 수 있다. 통합 테스트로 정상 경로와 trailing slash 경로 모두 호출해보고, 인가 동작이 의도대로인지 확인하자.

### 함정 5. `SecurityFilterChain`만 만들고 `WebSecurityCustomizer`를 잊음

velog와 한국 블로그에서 반복적으로 보고되는 패턴이다.

```java
// 함정 — 정적 자원에 대해 매번 인증 필터 체인을 통과
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/css/**", "/js/**", "/images/**").permitAll()
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .build();
}
```

이 코드는 잘못된 게 아니다. 동작은 한다. 다만 **`/css/**`, `/js/**` 같은 정적 자원 요청이 매번 전체 보안 필터 체인을 통과한다**는 비효율이 있다. 보안 컨텍스트 로드, CSRF 토큰 확인, 세션 검사… 모두 정적 파일 한 장에 대해 일어난다.

**왜 발생하는가:** 5.x의 `configure(WebSecurity)` 콜백을 옮기는 과정에서 `WebSecurityCustomizer` 빈 등록을 잊는 경우가 많다. 어디로 옮겨야 할지 명확하지 않은 데다, 빠뜨려도 동작은 하기 때문에 누가 알려주지 않으면 영영 못 알아차린다.

**해법:** 정적 자원은 보안 필터 체인을 **완전히 우회**시키자.

```java
@Bean
WebSecurityCustomizer webSecurityCustomizer() {
    return web -> web.ignoring()
        .requestMatchers("/css/**", "/js/**", "/images/**", "/webjars/**", "/favicon.ico");
}
```

이 빈을 추가하면 해당 경로 요청은 Spring Security 필터 체인이 아예 적용되지 않는다. 성능도 좋고, 의도도 명확하다. 다만 **인증이 필요한 자원이 절대 이 패턴에 포함되지 않도록** 주의하자. 한 번 우회시키면 어떤 인가 규칙도 적용되지 않으니, 패턴을 좁게 잡는 게 안전하다.

> **표 13-3. 마이그레이션 함정 5건 요약**
>
> | 함정 | 증상 | 해법 한 줄 |
> |------|------|------------|
> | 1. SO 2019 복붙 | 컴파일 에러 또는 인증 무작동 | 공식 docs/책의 7.0 예제로 |
> | 2. `@EnableGlobalMethodSecurity` 잔존 | `@PreAuthorize` 소리 없이 무력화 | `@EnableMethodSecurity`로 교체 + 통합 테스트 |
> | 3. `.and()` 체이닝 | 컴파일 에러 폭주 | OpenRewrite + 손 마무리 |
> | 4. mvc/ant 매처 혼합 | 403/200 일관성 깨짐 | 7.0에서 자동 해결, trailing slash 회귀 점검 |
> | 5. `WebSecurityCustomizer` 누락 | 정적 자원 매 요청 보안 체인 통과 | `WebSecurityCustomizer` 빈 등록 |

## 13.12 CI에서 deprecation warning 0 만들기

마이그레이션의 종착점은 "빌드가 초록색이고 통합 테스트가 통과한다"가 아니다. **CI 로그에 deprecation warning이 하나도 없을 때**가 진짜 끝이다. 경고는 미래의 컴파일 에러다. 미루면 다음 마이너 업그레이드에서 그대로 빨간 줄이 된다.

### 컴파일러 옵션

Gradle (Kotlin DSL):

```kotlin
tasks.withType<JavaCompile>().configureEach {
    options.compilerArgs.addAll(listOf(
        "-Xlint:deprecation",
        "-Werror"  // 경고를 에러로 격상
    ))
}
```

Maven:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <compilerArgs>
            <arg>-Xlint:deprecation</arg>
            <arg>-Werror</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

`-Werror`는 마이그레이션이 끝난 뒤에 켜는 편이 낫다. 마이그레이션 중에는 deprecation이 잔뜩 있는 상태가 정상이므로, 처음부터 켜두면 빌드가 통째로 안 돈다. 단계 2(preparation step)를 끝낸 직후, 빌드가 다시 초록색이 된 시점에 `-Werror`를 켜고 CI를 돌리자. 경고가 하나 남았다면 그 자리에서 잡힌다.

### 체크리스트 — CI 통과 기준

운영에 마이그레이션을 배포하기 전, 다음 체크리스트가 모두 통과되는지 확인하자.

- [ ] `./gradlew clean build` (또는 `mvn clean verify`) 초록색
- [ ] `-Xlint:deprecation` 켜고 Spring Security 관련 deprecation warning 0
- [ ] 정적 분석(`SpotBugs`, `SonarQube` 등) 신규 보안 경고 0
- [ ] `grep -rn "WebSecurityConfigurerAdapter\|antMatchers\|authorizeRequests\|@EnableGlobalMethodSecurity\|SecurityJackson2Modules" src/ test/` 결과 0줄
- [ ] 통합 테스트의 인증/인가 시나리오 5개 이상 통과 (12장 패턴 참고)
- [ ] 정상 경로/trailing slash 양쪽에서 인가 동작 동일 (함정 4 회귀 점검)
- [ ] OAuth2 로그인 / JWT 자원 서버 등 사용 중인 흐름 수동 점검
- [ ] SAML/LDAP/Authorization Server 사용처 있다면 영역별 통합 테스트 통과

체크리스트가 모두 통과되면, 그제서야 운영 배포 후보다. 한 단계라도 빨간색이면, 그 단계를 마무리한 뒤 다시 돌린다. 운영에서 문제가 터지는 비용은 마이그레이션 작업을 하루 미루는 비용과 비교할 수 없을 정도로 크다. 잊지 말자.

## 13.13 단계적 이전을 권하는 마지막 한 마디

13장의 모든 절을 정리한 다음, 마지막으로 한 가지를 다시 강조하자. **한 번에 모두 바꾸지 말자**는 그 말이다.

마이그레이션을 PR 한 개로 끝내는 시나리오를 또 떠올려보자. 변경 파일 200개, 라인 수 5000줄, 리뷰는 사실상 불가능하고, 어디서 회귀가 발생했는지 추적도 불가능하다. 정말 끔찍한 일이다. 그 PR이 운영에 나가는 순간을 상상하면 더더욱 그렇다.

권할 만한 분할은 다음 정도다.

- **PR 1: 6.5로 패치 올리기** — `build.gradle` / `pom.xml`의 버전 숫자만 바꾼다. 기존 코드는 deprecated 경고만 띄울 뿐 동작은 한다. CI 초록. 운영 배포.
- **PR 2: OpenRewrite 자동 치환** — `./gradlew rewriteRun` 결과를 그대로 커밋. 람다 DSL, `requestMatchers`, `authorizeHttpRequests` 등 단순 패턴이 자동 변환된다. CI 초록. 운영 배포.
- **PR 3: 손 변환 잔여분** — `WebSecurityConfigurerAdapter` 잔재, `@EnableGlobalMethodSecurity` 잔재, `WebSecurityCustomizer` 누락 등 사람이 봐야 할 곳. 가능하면 모듈별로 더 쪼개도 좋다. CI 초록. 운영 배포.
- **PR 4: `-Werror` 켜기** — deprecation 0임을 CI에 영구적으로 박는다. CI 초록. 운영 배포.
- **PR 5: 7.0 점프** — `build.gradle`의 Spring Boot 버전을 4.0.x로. 여기서 빨갛게 변하는 곳이 거의 없어야 정상이다. CI 초록. 운영 배포.
- **PR 6 이후: SAML/LDAP/Authorization Server 영역별 정리** — 사용처가 있다면 각 영역별로 분리 PR.

각 PR은 작고, 리뷰 가능하고, 회귀가 생기면 단일 PR을 revert하면 끝난다. 이게 운영을 깨지 않고 7.0으로 옮기는 가장 안전한 길이다. 한 번에 모두 바꾸려는 충동이 들 때마다, 이 6단계 분할 PR을 떠올리자.

## 마무리

마이그레이션은 두려운 작업이라고 첫 줄에 적었다. 13장을 따라온 지금쯤이면, 그 두려움이 조금은 가셨기를 바란다. 빨갛게 물든 첫 화면은 사실 친절한 안내일 뿐이고, OpenRewrite는 단순 치환의 80%를 처리해주고, 6.5 preparation step과 단계 분할 PR은 사람의 실수가 폭발하지 않게 막아준다. 5/6에서 7로 가는 길은 막막한 도약이 아니라, 잘 정비된 다섯 단계의 계단이다.

이 장이 책 본문의 마지막 실무 가이드다. 다음 14장은 시야를 한 단계 넓힌다. Spring Security 7로 만든 시스템이 **Zero Trust 원칙과 BFF 패턴의 시대**에 어떻게 위치하는지, 운영의 어느 모서리가 흔히 빈틈으로 남는지 살펴본다. 13장이 "현재 코드를 7.0으로 안전하게 옮기는 길"이었다면, 14장은 "7.0 위에서 짓는 시스템이 표준의 어느 자리에 서야 하는가"의 질문이다. 그 자리를 알면, 마이그레이션이 단순한 버전 업그레이드가 아니라 시스템 보안 모델의 한 단계 진화로 보이기 시작한다. 그 시야를 함께 살펴보자.
