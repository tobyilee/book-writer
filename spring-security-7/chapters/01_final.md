# 1장. 왜 Spring Security를 다시 봐야 하는가

이런 상황을 가정해보자. 잘 돌아가던 Spring Boot 3.4 프로젝트가 있다. `WebSecurityConfigurerAdapter` 시절의 흔적을 지운 뒤 `SecurityFilterChain` 빈으로 옮겨 둔 지도 한참 됐고, JWT 자원 서버 한 개와 폼 로그인 한 개를 잘 분리해 두었다. 팀 회의에서 "이제 Spring Boot 4로 올리자"는 결정이 나왔다. 한 사람 손을 든다. "마침 Spring Security 7.0이 GA됐던데, 같이 가시죠." 모두가 동의한다. 의존성 버전 한 줄을 바꾸고 빌드를 돌린다.

빌드가 깨진다. 그것도 한두 군데가 아니다. 솔직히 말해 난감하다.

`http.authorizeRequests(...)` 자리에 빨간 줄이 친다. `.and()`로 이어 붙였던 모든 체인이 빨갛다. `antMatchers("/api/**")` 자리도 빨갛다. `WebSecurityConfigurerAdapter`는 이미 6.x에서 사라졌으니 그것까진 알았다 치자. 그런데 `AccessDecisionManager`를 직접 빈으로 등록해 두었던 권한 정책 모듈은 컴파일 자체가 안 된다. 패키지가 통째로 없어진 것 같다. 한 명이 검색창에 "Spring Security 7 migration"을 친다. 누군가는 같은 IDE 화면에서 Stack Overflow 2019년 답변을 복붙하고 있다. "이거 그대로 쓰면 되겠지?" 옆 사람이 말리지 않는다. 끔찍한 일이다. 그 답변이 작성된 시점에는 `WebSecurityConfigurerAdapter`라는 클래스가 존재했기 때문에.

이게 2025년 11월 17일 이후 적지 않은 팀에서 일어나고 있는 풍경이다.

찜찜한 풍경이다. 단순히 메서드 이름 몇 개가 바뀐 이야기가 아니기 때문이다. Spring Security 5에서 6으로 넘어올 때도 우리는 비슷한 진통을 겪었다. 그때 람다 DSL이 도입됐고, `WebSecurityConfigurerAdapter`가 deprecated 됐고, 한국의 velog에는 "어떻게 대처해야 하지?"라는 글이 줄줄이 올라왔다. 그런데도 그때는 "당분간 옛날 방식도 살아 있다"는 도피로가 있었다. 6에서 7로 넘어오는 지금은 다르다. 도피로가 닫혔다. `.and()`도, `antMatchers`도, `authorizeRequests`도 더 이상 컴파일되지 않는다. 코드를 다시 봐야 한다. 그것도 표면만이 아니라 어휘 단위로 다시 봐야 한다.

이 책이 이야기하려는 게 그것이다. 이 장은 그 출발점이다.

## 1.1 무엇이 GA되었는가 — 2025년 11월 17일이라는 좌표

먼저 사실 관계부터 짚자. Spring Security 7.0은 2025년 11월 17일에 정식 출시됐다. Spring 공식 블로그가 같은 날짜로 `Spring Security Releases` 글을 올렸고, 같은 발표에서 6.5.7과 6.4.13 패치도 함께 풀렸다. Spring Boot 4.0도 같은 흐름 위에서 출시되며 Spring Security 7.0을 기본 의존성으로 묶었다. 그러니까 2025년 말부터 새로 잡힌 `start.spring.io`의 모든 프로젝트는 별다른 옵션 없이 Spring Security 7로 시작한다.

타임라인을 조금 더 풀어 보면 이렇다. 7.0.0-M1이 2025년 7월 21일에, M2가 8월 18일에 나왔다. 11월 17일 GA. 그리고 2026년 1월 19일에 7.1.0-M1, 2월 13일에 7.0.3 패치와 7.1.0-M2가 이어졌다. 그러니까 우리가 이 책에서 안전하게 기준 삼을 수 있는 API는 7.0 GA 라인의 것이다. 7.1.x 마일스톤은 보강 작업이 더 들어갈 수 있으므로, 만약 본문 코드의 시그니처가 7.1.x에서 미세하게 다르다 싶으면 출간 시점의 공식 docs를 한 번 더 확인하자. 책은 7.0 GA를 기준으로 쓴다.

큰 그림은 다섯 가지다. 외워둘 가치가 있다.

**첫째, 레거시 DSL과 매처가 사라졌다.** `HttpSecurity.and()`가 컴파일되지 않는다. `authorizeRequests`가 없다. `antMatchers`, `mvcMatchers`, `regexMatchers`가 모두 빠지고 `requestMatchers(...)` 안에서 동작하는 `PathPatternRequestMatcher`로 통일됐다. `AntPathRequestMatcher`도 같이 사라졌다. 람다 DSL이 선택이 아니라 강제다. 6.x 시절에 "익숙해지면 좋다더라"였던 것이 이제는 "익숙해지지 않으면 코드를 못 쓴다"가 됐다.

**둘째, 인가의 두뇌가 갈렸다.** `AccessDecisionManager`와 `AccessDecisionVoter` 시절의 API가 7.0의 기본 의존성에서 빠졌다. 호환을 위해 `spring-security-access`라는 별도 모듈로 격리되어 있긴 하지만, 새로 짜는 코드라면 `AuthorizationManager`로 가는 것이 정답이다. `AuthorizationManager#check`는 7.0에서 완전히 제거됐고, `authorize`만 남았다. 동시에 `AllAuthoritiesAuthorizationManager`(AND 의미의 새 매니저)와 `AuthorizationManagerFactory`라는 팩토리 추상화가 더해졌다. 즉, 같은 자리의 부품을 그대로 두고 옷만 갈아입힌 게 아니다. 자리도 바뀌었고 부품도 바뀌었다.

**셋째, Spring Authorization Server가 본체로 들어왔다.** 이제까지 별도 프로젝트로 관리되던 Spring Authorization Server가 `spring-security-oauth2-authorization-server:7.0.0` 좌표로 Spring Security 산하에 흡수됐다. Spring Security Kerberos Extension도 같이 들어왔다. 이게 무슨 뜻인가? 우리가 자체 IdP를 운영할 때 더 이상 외부 모듈로 끌고 들어올 필요가 없다. 같은 릴리스 사이클을 타니까 버전 충돌의 가능성도 줄었다. 단, 본 책은 자원 서버와 OAuth2 클라이언트 측에 집중한다. Authorization Server 본격 운영은 다른 책의 몫이다.

**넷째, 모던 인증이 1급 시민이 됐다.** Passkeys(WebAuthn), One-Time Token(매직 링크), 그리고 Multi-Factor Authentication — 이 세 가지가 7.0에서 본격적인 1급 지원으로 들어왔다. 특히 MFA는 새로 도입된 `@EnableMultiFactorAuthentication` 어노테이션 한 줄로 "패스워드 + OTT" 같은 누적 factor를 권한(`GrantedAuthority`)으로 표현해 버린다. Spring 공식 블로그가 2025년 10월 21일에 이 기능 단독 글을 올렸을 정도로 팀이 자신 있게 미는 변화다. Passkeys는 등록/인증 두 ceremony를 DSL이 직접 받아준다.

**다섯째, 토대 라이브러리가 갈아엎혔다.** Jackson 3, OpenSAML 5, UnboundID LDAP, Password4j 인코더 묶음. `SecurityJackson2Modules`가 `SecurityJacksonModules`로 이름을 바꿨고, OpenSAML 4는 지원이 끊겼고, ApacheDS는 빠졌다. 그리고 BCrypt 외에 Argon2id, Scrypt, PBKDF2, Balloon hashing이 Password4j 기반의 새 인코더로 추가됐다. 이건 단순한 의존성 교체처럼 보이지만, "왜 이걸 갈았는가"를 따라가 보면 결국 보안 표준의 시대 흐름이 보인다. 약한 알고리즘은 점점 빠지고, polymorphic deserialization 위험을 안고 가던 Jackson 2 모듈은 Jackson 3 모듈로 정리됐다. 이 흐름은 OWASP A02(Cryptographic Failures)·A08(Software & Data Integrity Failures) 같은 좌표와 직접 만난다 — 1.3절에서 다시 부른다.

이 다섯 가지가 7.0의 큰 그림이다. 첫 빌드에서 빨간 줄이 폭주하는 이유는 사실상 첫 번째와 두 번째 묶음이다. 나머지 세 가지는 새로 짤 때 만나는 변화고. 이걸 머릿속에 분리해 두면, 다음 절에서 다룰 "함정 5건"이 왜 그런 형태로 묶이는지 자연스럽게 보인다. 기억해두자.

## 1.2 5/6 코드는 7에서 무엇이 빨갛게 변하는가 — 함정 5건 한눈 표

여기까지 읽고도 "그래서 우리 코드를 열면 정확히 어디가 빨갛게 될까?"가 가장 궁금할 것이다. 솔직히 그게 정상이다. 그래서 본격적인 답을 13장으로 미루기 전에, 이 자리에서 함정 5건을 미리 한눈에 보여 두자. 이 표는 책 전체에서 가장 자주 다시 펴게 될 페이지가 될지도 모른다.

| # | 함정 | 5/6 시절 코드 모양 | 7에서 일어나는 일 | 본격 답 |
|---|------|--------------------|--------------------|---------|
| 1 | Stack Overflow 2019 복붙 | `extends WebSecurityConfigurerAdapter` + `configure(HttpSecurity)` | 클래스 자체가 없음. 6.0에서 이미 제거됐다 | 13장 13.1, 13.3 |
| 2 | `@EnableGlobalMethodSecurity` 잔존 | `@EnableGlobalMethodSecurity(prePostEnabled = true)` | 컴파일은 되지만 `@PreAuthorize`가 조용히 무력화될 수 있음 (이슈 #17487) | 8장 8.2, 13장 13.4 |
| 3 | `.and()` 체이닝 | `http.csrf().disable().and().authorizeRequests()...` | 컴파일 에러. 첫 빌드에서 가장 많이 보이는 빨간 줄 | 13장 13.2 |
| 4 | `mvcMatchers`/`antMatchers` 혼용 | `.antMatchers("/api/**")` 또는 `.mvcMatchers(...)` | 둘 다 사라짐. `requestMatchers(...)` 안에서 `PathPatternRequestMatcher`로 통일 | 13장 13.5 |
| 5 | `WebSecurityCustomizer` 누락 | 정적 자원까지 SecurityFilterChain 한 줄로 `permitAll()` | 빌드는 되지만 정적 자원에 필터가 다 태워져 비효율. velog 단골 사례 | 4장 4.7, 13장 13.6 |

이 표가 함의하는 바를 한 줄로 압축하면 이렇다. **함정 1·3·4는 컴파일 단계에서 잡히고, 함정 2·5는 컴파일 단계를 통과한 뒤 운영에서 발현된다.** 컴파일러가 잡아 주는 함정은 빨갛게 보이니까 차라리 다행이다. 정작 난감한 건 빨갛지 않게 통과한 뒤 운영에서 권한 검사가 사라지거나 정적 자원에 필터가 줄줄 태워지는 경우다. 함정 2가 특히 그렇다. `@PreAuthorize`가 동작하지 않는다는 사실은 단위 테스트가 없으면 오랫동안 모를 수 있다. 인가가 통째로 무력화된 채 운영에 떠 있는 시스템 — 끔찍한 일이다. 그래서 12장에서 이 책은 "인가 결정을 회귀 가능한 테스트로 묶는" 별도 챕터를 따로 약속한다.

함정 1에 대한 코멘트를 하나만 덧붙여 두자. Toptal에 실린 한 글이 이렇게 잘라 말한다 — "Spring Security 코드 리뷰에서 발견되는 문제 대부분은 2019년 Stack Overflow 답변을 복붙한 데서 온다." 농담처럼 들리지만 실제 자주 일어난다. AI 어시스턴트도 도움이 되지 못하는 경우가 많다. 학습 데이터의 중심이 여전히 5.x/6.x 초기 시절에 있기 때문이다. 그러니 7.0 코드를 쓸 때는, 어떤 출처에서 가져왔든 한 번은 의심하자. 7.0 GA 이후의 공식 docs(`docs.spring.io/spring-security/reference/whats-new.html`)와 본 책을 교차 검증의 짝으로 두면 된다.

함정 2는 따로 한 단락 들어줄 가치가 있다. `@EnableMethodSecurity`는 6.0에 도입됐고, 그 이전의 `@EnableGlobalMethodSecurity`는 deprecated였다. 7.0에서 둘 다 살아 있을 수는 있지만, 같은 모듈 안에 둘이 섞이면 우선순위 충돌로 `@PreAuthorize`가 조용히 죽는 경우가 있다. Spring Security 이슈 트래커 #17487에 정확히 같은 증상이 정리되어 있다. 마이그레이션 PR에서 이걸 한 줄 grep으로 잡아내는 게 가장 빠른 안전망이다 — `grep -r "@EnableGlobalMethodSecurity" src/`. 한 번 돌려보자. 0건이 나오면 안심.

이 함정 5건의 본격 답은 13장에서 펼쳐진다. 13장은 마이그레이션을 한 번에 끝내고 싶은 독자를 위해 "공식 권고 순서 → deprecation 매핑표 → OpenRewrite 자동화 → CI 체크리스트"의 흐름으로 묶여 있다. 운영 코드를 당장 옮겨야 한다면, 1장만 읽고 13장으로 점프해도 좋다(그 다음 2~3장으로 돌아오면 된다). 책 끝의 챕터 의존도 지도가 그 경로를 보장한다.

## 1.3 보안 멘탈 모델 5분 — 책 전체의 어휘를 박는다

자, 잠시 호흡을 가다듬자. 1장이 책의 좌표축을 박는 챕터라 했다. 그 좌표축의 두 번째가 멘탈 모델이다. Spring Security 7의 신기능 다섯 가지보다 더 오래 가는 어휘이기도 하다. 이 절 다섯 단락을 머리에 박아 두면, 이 책 전체가 같은 어휘로 말한다. 그리고 책을 덮은 뒤에도 다른 자료를 읽을 때 좌표를 잃지 않는다. 길게 풀지 않고 다섯 분 안에 끝낸다. 차근차근 살펴보자.

### 1.3.1 인증과 인가는 다른 일이다

**인증(authentication)** 은 "당신이 누구인가"를 확인하는 일이다. 결과물은 `Authentication` 객체 한 개 — 주체(principal), 크리덴셜, 권한 목록을 담은 컨테이너. **인가(authorization)** 는 "그 사람이 이 일을 해도 되는가"를 결정하는 일이다. 결과물은 `AuthorizationResult`. 통과인지 아닌지의 판정.

이 둘이 같은 코드에서 섞이면 사고가 일어난다. 가장 흔한 예가 6장에서 다룰 "ID Token으로 API 인가하기"의 함정이다. OIDC의 ID Token은 "이 사용자가 누구인지"를 IdP가 클라이언트에게 알려주는 토큰이다. API 자원 서버가 "이 사용자가 무엇을 할 수 있는지"를 판단하는 데 쓰라고 발급된 토큰이 아니다. 그 자리에는 Access Token이 있다. 두 토큰의 용도를 헷갈리면 보안 모델 전체가 무너진다.

Spring Security의 필터 체인이 인증 필터들을 인가 필터(`AuthorizationFilter`)보다 항상 앞에 두는 이유가 여기 있다. 인증을 통과한 요청만 인가 단계에 들어간다. 인가 단계에 들어가지 못한 요청은 `ExceptionTranslationFilter`가 401(인증 안 됨)이나 403(인가 안 됨)으로 번역해 내보낸다. 같은 401·403도 의미가 다르다. 401은 "당신을 모르겠다", 403은 "당신을 알지만 이건 못 한다"다. 이 한 줄을 잊지 말자.

### 1.3.2 세션과 토큰은 서로 다른 트레이드오프다

**세션(stateful):** 서버가 식별자(예: `JSESSIONID`) 한 개를 쿠키로 발급하고, 그 식별자에 묶인 상태(사용자, 권한, 장바구니 등)는 서버가 보관한다. **토큰(stateless, 주로 JWT):** 토큰 자체에 클레임을 담아 서버는 검증만 하고 상태를 보관하지 않는다.

자, 어느 쪽이 더 나은가? 이 질문에 한 줄로 답하지 말자. 둘은 다른 트레이드오프를 갖는다. 세션은 즉시 무효화(로그아웃, 권한 강등)가 자연스럽고, 페이로드가 작고(쿠키에 식별자 하나), 클러스터링이라는 운영 비용을 진다. 토큰은 서버 상태가 없어 수평 확장이 자유롭고, 서비스 간 호출에 자연스럽게 끼워 보낼 수 있고, 그 대신 즉시 무효화가 어렵고 페이로드가 더 크다.

5장에서 본격적으로 다룰 함정 하나를 미리 알려주자면, "JWT를 세션 토큰처럼 쓰는" 패턴이다. 즉시 로그아웃이 안 되니 Redis에 블랙리스트를 둔다. 권한이 바뀌면 즉시 반영해야 하니 또 Redis를 본다. 결국 stateless의 장점을 다 버리고 stateful로 회귀하는데 운영 부담은 두 배가 된다. DZone에 "Stop Using JWTs as Session Tokens"라는 글이 괜히 인기를 끈 게 아니다.

세 줄로 정리하자. **(a) 브라우저-서버 단방향 사용자 세션이라면 세션 쿠키.** **(b) 서비스 간 호출이나 자원 서버 보호라면 access token.** **(c) SPA + 외부 IdP는 BFF로 두 가지를 합성한다.** (c)에 대한 본격 답은 14장이다.

### 1.3.3 OWASP Top 10 — 책에서 자주 만날 세 항목

OWASP Top 10은 웹 보안 위협의 세계 표준 카탈로그다. 2021년판에서 우리가 자주 만날 항목은 셋이다.

- **A01: Broken Access Control.** 2017년판 5위에서 **1위로 올라왔다.** 평균 발견율 3.81%. 즉, 검사한 웹 애플리케이션 100개 중 거의 4개꼴로 인가가 깨져 있더라는 통계다. Spring Security가 이 항목에 직접 답한다 — `AuthorizationManager`, method security, role hierarchy, ACL. 8장이 통째로 이 영역이다.
- **A02: Cryptographic Failures.** 약한 알고리즘, 하드코딩 비밀번호, 평문 저장. Spring Security 측면에서는 `PasswordEncoder` 선택과 JWT 키 관리가 여기 걸린다. 7.0의 Password4j 인코더 묶음이 직접 응답하는 자리다.
- **A07: Identification and Authentication Failures.** 세션 고정, 약한 로그인 흐름, brute-force 방어 부재. Form/MFA/Passkeys가 다 이 자리에 답한다.

이 세 코드(A01·A02·A07)는 책 곳곳에서 다시 만난다. 외우자는 게 아니다. 우리가 짠 코드가 어느 영역에 응답하고 있는지를 셋 중 하나의 좌표로 부를 수 있으면 충분하다.

### 1.3.4 Zero Trust — 한 줄 정의와 좌표

**"네트워크 위치만으로 신뢰를 부여하지 않는다."** 이것이 NIST SP 800-207이 정의하는 Zero Trust 아키텍처의 한 줄 정의다. 사내망 안에서 왔다고 자동으로 신뢰하지 않고, 인터넷에서 왔다고 무조건 의심하지도 않는다. 모든 통신이 그 자체로 보호되고, 모든 접근이 동적 정책으로 평가된다.

NIST는 7 tenets로 풀어 두었는데, 우리가 책에서 자주 인용할 것은 두 개다. **원칙 4: 동적 정책으로 접근을 결정한다.** **원칙 6: 인증·인가는 접근 직전에 동적이고 엄격하게 강제한다.** 무슨 뜻인가? 한 번 로그인했다고 다음 요청에서 묻지 않는 게 아니라, 매 요청에서 토큰/세션을 검증해야 한다는 뜻이다. 그래서 Spring Security의 stateless JWT + 매 요청 인가 구조가 Zero Trust 원칙 6에 정확히 매핑된다. 5장에서 자세히 다룰 DPoP는 원칙 4(sender-constrained, 즉 토큰을 누가 가지고 있느냐가 동적 정책의 일부가 됨)와 맞붙는다.

14장에서 이 좌표를 다시 펼친다. 1장에서는 한 줄 정의와 두 원칙만 가지고 가자.

### 1.3.5 이 어휘들을 책의 곳곳에 박는다

지금까지의 어휘를 짧게 정리하자: **인증/인가** 구분, **세션/토큰** 트레이드오프, **OWASP A01·A02·A07** 좌표, **Zero Trust 원칙 4·6**. 다섯 분이면 머리에 들어온다.

이 책의 모든 챕터가 이 어휘로 말한다. 3장에서 `AuthenticationManager`와 `AuthorizationManager`를 가를 때 1.3.1이 다시 나온다. 4장과 5장이 갈리는 지점에 1.3.2가 있다. 8장이 A01에 답한다. 14장이 Zero Trust 원칙들 위에 모든 결정을 다시 얹는다. 그러니 잊지 말자. 다섯 줄을 종이에 적어 책상 옆에 붙여 두는 것도 권하고 싶다.

## 1.4 이 책의 사용법 — 챕터 의존도와 독자 경로 3종

책의 구조를 한 그림으로 설명할 수 있는 게 가장 좋다. 그래서 챕터 의존도 지도를 먼저 보여주자.

```
1장 (좌표축)
 │
 ├─► 2장 필터 체인 ──► 3장 컴포넌트 모델
 │                       │
 │                       ├─► 4장 폼/Basic/Remember-Me
 │                       ├─► 5장 JWT + DPoP
 │                       ├─► 6장 OAuth2/OIDC (5장 토큰 어휘 필요)
 │                       └─► 7장 Passkeys/OTT/MFA (4장 세션 어휘 필요)
 │                       │
 │                       ├─► 8장 인가 5층 (4~7장 권한 생산자 필요)
 │                       ├─► 9장 CSRF/CORS/헤더
 │                       ├─► 10장 세션/쿠키/컨텍스트
 │                       └─► 11장 Reactive 보안
 │                              │
 │                              └─► 12장 테스팅
 │
 └─► 13장 마이그레이션 (1장 직후 점프 가능)
 │
 └─► 14장 Zero Trust/BFF/운영 (1·5·6·8·9·10장 어휘 필요)
        │
        └─► 15장 통합 실전 (전 챕터 종합)
```

세 가지 독자 경로를 명시한다.

**경로 1 — 통독.** `1 → 2 → 3 → 4 → ... → 15`. 가장 권하는 순서다. 2~3장에서 박은 어휘가 이후 모든 챕터의 코드와 다이어그램에 그대로 흐른다. 책을 덮을 때 한 권의 "Spring Security 7 운영 매뉴얼"이 머릿속에 남는다.

**경로 2 — 5/6 마이그레이션이 급한 독자.** `1 → 13 → 2 → 3 → ...`. 운영 코드를 빨리 옮겨야 한다면 1장 직후 13장으로 점프하자. 함정 5건의 본격 답과 OpenRewrite 자동화 레시피가 13장에 있다. 그 다음 2~3장으로 돌아와 어휘를 다지고, 필요한 시나리오 챕터로 가면 된다.

**경로 3 — 특정 신기능만 빨리 도입.** `1 → 2 → 3 → 해당 챕터 (+ 12장)`. 시니어 독자가 "Passkeys만 도입해야 한다"거나 "MFA만 붙이면 된다"는 상황이라면, 2~3장으로 어휘만 깔고 곧장 7장으로 가도 좋다. 도입 후 12장 테스팅 챕터로 회귀 안전망을 구성하는 것까지 한 사이클로 묶어 두면 된다.

각 챕터의 머리에는 **"선행 필요: N장"** 한 줄이 동일하게 노출되어 있다. 어디서부터 펴도 자기 위치를 잃지 않게 하기 위함이다. 시니어 독자에게는 12장(테스팅)이 따로 약속되어 있다는 점도 한 번 짚자. `@WithMockUser`부터 OAuth2 mock, Reactive `mutateWith(mockUser())`까지를 한 챕터에 모아 두었다. 본문 챕터의 인증·인가·Reactive 어휘가 모두 깔린 시점에서 "이 모든 결정을 어떻게 테스트로 묶을 것인가"에 답하는 자리다.

### 1.4.1 챕터별 한 줄 약속

빠르게 훑어 두자.

- **2장.** 필터 체인 — `DelegatingFilterProxy → FilterChainProxy → SecurityFilterChain`. 필터 11종이 한 요청 위에서 무엇을 하는지. 그리고 내 Filter를 끼우는 법.
- **3장.** 컴포넌트 모델 — `AuthenticationManager`/`AuthorizationManager`/`SecurityContextHolder`. 7.0에서 어떻게 바뀌었는지.
- **4장.** 폼/Basic/Remember-Me — 가장 오래된 인증의 7.0 권장 구성.
- **5장.** JWT 자원 서버 — Bearer 토큰의 끝까지. 그리고 DPoP로 sender-constrained 토큰까지 가는 자연스러운 진화.
- **6장.** OAuth2 Client + OIDC Login — 외부 IdP에 로그인 위임. PKCE 기본 ON 시대의 흐름.
- **7장.** Passkeys / One-Time Token / MFA — 패스워드 너머의 인증, 7.0 1급 모델 세 가지.
- **8장.** 인가의 5층 구조 — URL/Method/Role Hierarchy/ACL/거부 응답. 권한이 코드 어느 층에 살아야 하는가.
- **9장.** CSRF/CORS/헤더 — 가장 헷갈리는 셋. `csrf(spa)` 한 줄이 바꾸는 것.
- **10장.** 세션/쿠키/컨텍스트 전파 — stateful과 stateless의 경계, 비동기 누수 회피.
- **11장.** Reactive 보안 — WebFlux에서 다시 그리는 인증·인가.
- **12장.** 테스팅 — `@WithMockUser`부터 OAuth2 mock까지의 안전망.
- **13장.** 5/6 → 7 마이그레이션 — 함정 5건의 본격 답과 자동화.
- **14장.** Zero Trust/BFF/운영 — 트렌드와 운영의 모서리.
- **15장.** 통합 실전 — 한 권을 한 시나리오로.

이걸 다 읽어야 할까? 그렇다. 그러나 한 번에 다 읽을 필요는 없다. 위 의존도 지도와 경로 3종으로 자기 입장에 맞게 잘라 읽자.

## 1.5 이 책이 다루지 않는 것 — 정직하게

마지막으로 정직한 절 하나를 끼우자. Spring Security 7을 다루는 이 책이 의도적으로 비워 둔 자리가 있다. 다섯 가지를 짚는다.

**(1) Spring Authorization Server의 서버 측 깊은 운영.** Authorization Server가 7.0에 흡수되긴 했지만, 본 책은 자원 서버와 클라이언트 측의 활용에 집중한다. IdP를 직접 운영하면서 client registration, consent 화면 커스터마이즈, multi-tenant 토큰 발급 정책을 깊이 다루는 것은 별도 책의 몫이다. 7.0의 What's New에 적힌 OAuth 2.0 Dynamic Client Registration도 표면 수준의 소개에 그친다 — GA 직후라 정리된 deep-dive 자료가 아직 충분치 않다는 사실을 정직하게 말한다.

**(2) GraphQL과 gRPC 보안.** Spring Security가 두 영역에 손이 닿지 않는다는 뜻은 아니다. `@PreAuthorize`는 GraphQL DataFetcher에서도, gRPC 서비스 메서드에서도 동작한다. 그러나 GraphQL 권한 모델(field-level authorization, dataloader caching의 보안 함의)과 gRPC의 인터셉터 기반 인증·인가 패턴은 본 책의 범위 밖이다. REST와 SPA 시나리오가 중심이다.

**(3) 모바일 앱 측 보안.** iOS/Android 앱이 OAuth2 PKCE 클라이언트로서 Spring 자원 서버를 호출하는 시나리오는 6장 끝에서 짧게 언급하지만, 모바일 측의 keychain 보관, certificate pinning, 디바이스 attestation 같은 영역은 다루지 않는다.

**(4) MDM(Mobile Device Management)과 디바이스 신원.** Zero Trust 원칙 4가 요구하는 "동적 정책"에는 디바이스 신원과 자산 상태가 들어가지만, 그것은 Spring Security 단독으로 해결되는 영역이 아니다. MDM 제품, 디바이스 인증서, IdP의 디바이스 정책과의 통합이 필요하다. 14장에서 한 단락 트렌드 박스로 좌표만 짚는다.

**(5) Kubernetes Service Mesh와의 mTLS 통합.** Istio/Linkerd가 사이드카로 처리하는 mTLS는 Spring Security와 결이 다르다. Service Mesh 레벨의 sender-constrained 모델은 5장 DPoP의 응용 너머에 있다. 같은 14장 트렌드 박스에서 한 단락으로만.

그러니 이 책을 덮은 뒤에도 더 읽어야 할 것이 있다는 사실을 미리 말해 두자. 15장 마지막 절에 "이 책을 덮은 뒤"라는 자리를 따로 두고, 거기서 Curity 시리즈, Spring 공식 docs의 심층 페이지, RFC 원문, 7.1.x 마일스톤 추적법을 안내한다. 책이 안내자라면, 안내자가 데려가지 못하는 곳까지는 안내자도 솔직히 말해야 한다.

## 1.6 잠깐, 람다 DSL이라는 멀미

본론으로 넘어가기 전에 한 토픽만 더 짚자. 7.0의 빨간 줄을 가장 많이 만들어 내는 변경이자, 그러면서도 입문자에게 가장 멀미가 나는 변경 — 람다 DSL이다.

Spring 팀이 람다 DSL을 도입하면서 공식 블로그(2019-11-21)에 이렇게 적었다. "이전 구성 방식은 반환 타입을 모르면 무엇이 구성되는 것인지 불분명했고, 중첩이 깊어질수록 더 헷갈렸다." 옳은 말이다. `.and()`로 끝없이 이어 붙던 시절의 코드는, 한 줄 한 줄이 어떤 객체에 대한 호출인지 정확히 알기 어려웠다. 람다 DSL은 그 모호함을 해결한다. `http.csrf(csrf -> csrf.disable())`이라 적으면 람다 안에서 자기가 `CsrfConfigurer`를 만지고 있다는 사실이 명백하다.

그런데 입문자 입장에서는 어떻게 보일까? 한 줄이 여러 줄로 늘어났다. 들여쓰기가 깊어졌다. IntelliJ 자동완성에 더 많이 기대게 됐다. 익숙해지기 전까지 코드가 더 길고 어지러워 보인다 — 한국 velog에 이 멀미를 호소하는 글이 줄줄이 올라온 이유다. 그 멀미는 정상이다. 하지만 한 번만 익숙해지자. 그러면 `.and()` 시절로 돌아가고 싶지 않아질 것이다. velog 글 다수가 같은 결론에 수렴한다 — "처음엔 어색하지만 한 번 익히면 더 명확하다."

7.0에서 람다 DSL은 선택이 아니라 강제다. `.and()`가 없으니 다른 선택지가 없다. 우리가 할 일은 "Lambda DSL 핵심 5분 가이드"를 머리에 박는 것이다. 두 패턴만 외우면 거의 다 된다.

**패턴 1 — 기본 활성화 한 줄.** `Customizer.withDefaults()`를 넣어 기본값으로 켠다.

```java
http.formLogin(Customizer.withDefaults());
http.csrf(Customizer.withDefaults());
```

**패턴 2 — 커스터마이즈는 람다.** 람다가 받는 객체의 이름을 짧게(`a`, `o`, `csrf`) 두는 게 관용이다.

```java
http
    .authorizeHttpRequests(a -> a
        .requestMatchers("/", "/login").permitAll()
        .anyRequest().authenticated())
    .oauth2Login(o -> o.loginPage("/login"))
    .csrf(CsrfConfigurer::spa);   // 7.0 신규 SPA 한 줄
```

요점은 두 가지다. **(a) 각 람다 안에서는 자기 configurer만 만진다.** `csrf` 람다 안에서 `formLogin` 메서드를 찾지 말자 — 찾을 수 없다. **(b) `http.` 뒤에서는 같은 `HttpSecurity`가 그대로 흐른다.** 그래서 점(.)으로 옆 메서드를 이어 부를 수 있다.

이 두 패턴이 머리에 있으면 7.0 코드 90% 이상은 일관되게 읽힌다. 이걸 모르면 첫 빌드의 빨간 줄을 풀 때마다 매번 검색을 해야 한다 — 번거롭다. 5분만 투자하자.

## 1.7 첫 빌드의 빨간 줄 앞에 서서

이제 1장을 닫는다. 첫 단락의 풍경으로 돌아가 보자. `.and()` 자리에 빨간 줄이 친 그 화면이다. 회의실에서 누군가가 Stack Overflow를 켰고, 누군가는 막막한 표정이다.

이 풍경은 사실, 두려운 풍경이 아니다. **빨간 줄이 빨갛게 보여 다행이다.** 컴파일러가 잡아주는 함정은 우리가 한 번에 인지할 수 있는 함정이다. 진짜 무서운 건 빨갛지 않게 통과하는 함정이다. `@EnableGlobalMethodSecurity`가 그대로 남아 `@PreAuthorize`가 죽는 함정. JWT를 `localStorage`에 박아 두고 마음 놓는 함정. CSRF를 그냥 `disable()`로 끄고 폼 로그인이 같이 깨지는 함정. 이 책 전체에서 우리는 빨갛지 않은 함정을 빨갛게 만드는 작업을 한다.

다음 장에서 우리는 한 요청이 Spring Security 안에서 무엇을 11번 거치는지를 처음부터 끝까지 따라간다. `DelegatingFilterProxy`가 컨테이너와 ApplicationContext의 다리를 어떻게 놓는지, `FilterChainProxy`가 왜 매 호출 끝에 `SecurityContext`를 비우는지, `ExceptionTranslationFilter`가 401과 403을 어떻게 갈라 응답하는지. 그리고 7.0에서 `AuthorizationFilter`가 `FilterSecurityInterceptor`를 완전히 대체했다는 사실의 의미. 그 길을 한 번 끝까지 걸어 두면, 이후 모든 챕터에서 "이 코드는 어느 필터에 꽂히는가"를 자기 손으로 답할 수 있게 된다. 그것이 이 책이 약속하는 가장 큰 자산이다.

한 가지만 더 당부하자. 1장의 멘탈 모델 5분(1.3절)을 한 번만 더 훑고 2장으로 넘어가자. 인증/인가, 세션/토큰, OWASP A01·A02·A07, Zero Trust 원칙 4·6. 다섯 줄이다. 이게 머릿속에 있으면 2장의 필터 11종이 단순한 클래스 이름 나열로 보이지 않는다. 각 필터가 어느 어휘의 어느 자리에 응답하는지가 보인다.

자, 그러면 2장으로 가자.

## 챕터 요약 — 5줄

- Spring Security 7.0은 2025년 11월 17일에 GA됐고, Spring Boot 4.0과 함께 묶여 출시됐다. 이제 새 프로젝트의 기본값이다.
- 7.0의 큰 그림 다섯 가지: 레거시 DSL/매처 제거, `AuthorizationManager`로 완전 이주, Authorization Server·Kerberos 흡수, Passkeys/OTT/MFA의 1급 시민화, Jackson 3/OpenSAML 5/Password4j 등 토대 갈아엎기.
- 5/6 코드가 7에서 빨갛게 변하는 함정 5건: SO 2019 복붙, `@EnableGlobalMethodSecurity` 잔존, `.and()` 체이닝, `mvcMatchers`/`antMatchers` 혼용, `WebSecurityCustomizer` 누락. 본격 답은 13장.
- 책 전체의 어휘 5분: 인증 vs 인가, 세션 vs 토큰, OWASP A01·A02·A07, Zero Trust 한 줄 정의와 원칙 4·6. 종이에 적어 두자.
- 챕터 의존도와 독자 경로 3종(통독 / 마이그레이션 우선 / 신기능만 빨리 도입)으로 이 책은 어디서부터 펴도 안전하게 읽을 수 있게 짜여 있다.

## 다음 챕터에서 답할 것

`http://localhost/api/orders` 요청 하나가 Spring Security 안에서 무엇을 11번 거치는가 — 필터 체인의 처음부터 끝까지.
