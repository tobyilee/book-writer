# 토비의 Spring Security 7

**내부 아키텍처부터 Zero Trust·Passkeys·MFA까지, Spring Boot 4 기반 심층 레퍼런스**

저자: Toby-AI

판본: v1.0.0 · 발행일: 2026-05-11

---

# 차례

- 머리말 — 이 책을 펴 든 독자에게

- 1장. 왜 Spring Security를 다시 봐야 하는가
- 2장. 한 요청이 통과하는 길 — 필터 체인 해부
- 3장. 인증과 인가의 컴포넌트 모델
- 4장. 폼 로그인·HTTP Basic·Remember-Me — 세션 기반 인증의 정석
- 5장. JWT 자원 서버 — Bearer 토큰의 끝까지, 그리고 sender-constrained로
- 6장. OAuth2 Client + OIDC Login — 외부 IdP에 로그인을 위임하다
- 7장. Passkeys·One-Time Token·MFA — 패스워드 너머의 인증
- 8장. 권한은 어디에 사는가 — 인가의 5층 구조
- 9장. CSRF·CORS·보안 헤더 — 가장 헷갈리는 셋
- 10장. 세션·쿠키·컨텍스트 전파 — 상태 관리의 모든 모서리
- 11장. Reactive 보안 — WebFlux에서 다시 그리는 인증·인가
- 12장. Spring Security 테스팅 — `@WithMockUser`부터 OAuth2 mock까지
- 13장. 5/6에서 7로 — 마이그레이션 실전 가이드
- 14장. Zero Trust·BFF·운영의 모서리 — 트렌드와 표준
- 15장. 한 권을 한 시나리오로 — 통합 실전 워크스루

- 맺음말 — 책을 덮는 독자에게
- 부록 A. 마이그레이션 체크리스트 한 페이지
- 참고문헌
- 판권

---

# 머리말 — 이 책을 펴 든 독자에게

이 책을 펴 든 독자에게 가장 먼저 하고 싶은 말은 사실 짧다. **잘 오셨다.**

이 책은 2025년 11월 17일에 GA된 Spring Security 7.0을 기준으로 다시 쓰는, 한국어 심층 레퍼런스다. 처음 잡힌 목표는 단순했다. 7.0이 우리 코드에서 무엇을 빨갛게 만드는지를 한 권에 모으는 것. 그런데 책을 짜다 보니, 그것만으로는 모자란다는 사실을 깨달았다. 빨간 줄을 어떻게 푸는가보다 중요한 질문이 따로 있었다. "그 빨간 줄을 만든 결정들이 왜 이렇게 묶여 있는가." 그 질문에 답하려면 필터 한 줄의 자리에서부터 다시 시작해야 한다. 그렇게 책의 첫 토대 두 장(2장 필터 체인, 3장 컴포넌트 모델)이 자리를 잡았다.

## 이 책이 답하려는 질문들

이 책은 다음 질문들에 답하려고 짜였다.

- 한 요청이 `http://localhost/api/orders`에 들어왔을 때, Spring Security 안에서 무슨 일이 11번 일어나는가?
- `AuthenticationManager`와 `AuthorizationManager`는 7.0에서 정확히 어떻게 바뀌었고, 어디서 일이 갈리는가?
- 폼 로그인·HTTP Basic·Remember-Me는 2025년에도 여전히 정석으로 살아 있는가? 어디서 멈춰야 하는가?
- JWT 자원 서버 한 줄(`oauth2ResourceServer(o -> o.jwt())`)이 정확히 무엇을 켜는가? Bearer 토큰의 한계 너머 sender-constrained(DPoP)는 어떻게 동작하는가?
- 외부 IdP에 로그인을 위임할 때(OAuth2 Client + OIDC), PKCE·redirect URI·ID Token vs Access Token의 함정은 어디에서 폭발하는가?
- 패스워드 없는 인증(Passkeys), 매직 링크(OTT), 그리고 7.0이 1급으로 끌어올린 MFA를 한 모델 위에서 어떻게 조립하는가?
- 인가의 5층 구조(URL·메서드·메타·도메인·거부 응답)에서 비즈니스 규칙은 어느 층에 살아야 하는가?
- CSRF는 왜 켜고, CORS는 왜 미리 통과시키며, 헤더 한 줄이 무엇을 바꾸는가?
- 세션 정책 네 가지의 의미와, `MODE_INHERITABLETHREADLOCAL` + 스레드 풀이라는 끔찍한 함정은 어디서 새는가?
- Reactive(WebFlux) 세계에서 같은 어휘가 어떻게 비틀리는가?
- 위 모든 결정을 회귀 가능한 테스트의 안전망에 어떻게 묶는가?
- 운영 중인 5.x/6.x 코드베이스를 깨지 않고 7.0으로 옮기는 안전한 순서는?
- Zero Trust·BFF·Secret 회전·Actuator 노출 사고 같은 운영의 모서리에는 무엇이 있는가?
- 그래서 결국, 이 모든 결정을 한 프로젝트에 어떻게 합치는가?

15개 챕터가 차례로 그 답을 펼친다.

## 누구를 위한 책인가

중급에서 시니어까지를 가정한다. Spring Boot로 REST API와 폼 로그인을 직접 만들어 본 적이 있고, Spring Security 5.x/6.x를 표면적으로라도 써본 독자라면 어디서부터 펴도 어색하지 않다. 만약 Spring Security가 처음이라면 1장의 멘탈 모델(1.3절)과 2장의 필터 지도를 한 번 더 천천히 읽어 보길 권한다. 그 한 번이 책 전체의 좌표를 안정시킨다.

이 책은 또한, **운영 중인 코드를 7.0으로 옮겨야 하는 시니어 개발자**에게도 별도 경로를 준비해 두었다. 1장 직후 13장으로 점프해도 좋다(독자 경로 2). 함정 5건의 본격 답과 OpenRewrite 자동화 레시피가 13장에 모여 있다.

## 어떻게 읽으면 좋은가

가능하면 1장부터 차례로 읽는 통독을 권한다. 2~3장에서 박은 어휘가 이후 모든 챕터의 코드와 다이어그램에 그대로 흐른다. 책을 덮을 때 한 권의 "Spring Security 7 운영 매뉴얼"이 머릿속에 남는다.

그러나 책의 두께가 부담스럽다면 1장의 챕터 의존도 지도(1.4절)를 보고 자기 입장에 맞는 경로를 골라 잡자. 시니어 독자가 "Passkeys만 도입해야 한다"거나 "MFA만 붙이면 된다"는 상황이라면, 2~3장으로 어휘만 깔고 곧장 해당 챕터로 가도 좋다. 도입 후 12장 테스팅 챕터로 회귀 안전망을 구성하는 것까지 한 사이클로 묶으면 된다.

매 챕터 머리에는 **"선행 필요: N장, M장"** 한 줄이 나온다. 어디서부터 펴도 자기 위치를 잃지 않게 하기 위함이다. 챕터 끝의 "핵심 5줄 요약"과 "다음 챕터에서 답할 것"은 빠르게 다시 펴서 좌표를 잡는 데 쓰자.

## 톤과 약속

평어체(`-다`/`-한다`) 기반에, 새 개념을 도입하거나 흐름을 전환할 때는 청유형(`-자`/`-보자`)을 적극 쓴다. "이런 상황을 가정해보자" 한 단락으로 챕터를 여는 자리가 적지 않다. 함정과 실수 코드 앞에서는 "틀렸다"가 아니라 "난감하다", "찜찜하다"는 감각을 그대로 적었다. 보안 코드를 보는 일은 사실 그런 감각의 일이다.

코드 예제는 Spring Boot 4 + Spring Security 7.0 GA를 기준으로 한다. 7.1.x 마일스톤에서 미세하게 시그니처가 바뀔 수 있는 자리에는 본문에 명시했다. 출간 시점의 공식 docs(`docs.spring.io/spring-security/reference/whats-new.html`)와 본 책을 교차 검증의 짝으로 두면 된다.

## 감사의 말

이 책은 Spring 팀의 7.0 GA 발표(2025-11-17)와 함께 시작됐다. NIST SP 800-207, RFC 9700, RFC 8725, RFC 9449, W3C WebAuthn Level 3 같은 표준 문서들이 책 전체의 베이스 라인을 받쳐 줬다. Baeldung·Curity·Dimitri Mes·Dan Vega·Auth0·Okta 같은 검증된 저자 블로그들이 본문의 코드 예제와 운영 감각을 더 풍부하게 만들어 줬다. 우아한형제들 기술블로그의 Actuator 노출 사고 회고는 14장 운영 절의 가장 정직한 사례가 됐다. 한국 velog 단편글들도 시행착오의 풍경을 솔직하게 비춰 줬다. 모두에게 감사한다.

마지막으로, 이 책의 거의 모든 단계는 `book-writer` 하네스(v1.2.0) 기반의 AI 에이전트 협업으로 산출됐다. 리서치·계획·계획 리뷰·챕터 저술·스타일 점검·편집·표지 디자인·EPUB 빌드 전 과정이 그 하네스 위에서 돌아갔다. 그 도구를 만들고 다듬어 준 오픈소스 생태계에도 함께 감사를 적어 둔다.

자, 그러면 시작하자. 첫 빌드의 빨간 줄 앞에 서서.

— 2026년 봄, 저자

---

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

---

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

---

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

---

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

---

# 5장. JWT 자원 서버 — Bearer 토큰의 끝까지, 그리고 sender-constrained로

JWT라는 단어를 들으면 마음이 두 갈래로 갈라진다. 한쪽은 stateless의 아름다움이다. 서버에 세션 저장소가 필요 없고, 토큰만 들고 있으면 어떤 인스턴스든 그 요청을 처리할 수 있다. 마이크로서비스 사이를 옮겨다닐 때마다 사용자 정보를 다시 묻지 않아도 된다. 다른 한쪽은 운영에서 만난 함정들이다. 강제 로그아웃이 안 된다거나, XSS 한 번에 토큰이 새거나, `alg: none`을 받아들이는 서버가 발견되었다는 보안 보고서가 떠오른다.

이 두 얼굴을 동시에 봐야 한다. JWT는 안 쓸 수 있는 기술이 아니다. 시중에서 가장 많이 쓰이는 토큰이고, 마이크로서비스를 한 줄로 묶는 표준 어휘다. 그렇다면 어떻게 해야 할까? 한 번에 둘 다 보자. 안전하게 도입하는 정석을 먼저 익히고, 흔히 빠지는 함정 네 개를 코드 레벨에서 풀어낸 다음, Bearer 토큰의 본질적 한계를 짚고 그 다음 단계인 sender-constrained 토큰(DPoP)으로 마무리한다. 한 챕터 안에서 "Bearer의 끝"에서 "Bearer 너머"로 건너가 보자.

## 5.1 한 줄로 끝나는 자원 서버 — 그러나 그 한 줄이 하는 일

Spring Security 7로 가장 단순한 JWT 자원 서버를 구성하면 코드는 이렇게 줄어든다.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .csrf(CsrfConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .build();
}
```

`application.yml`은 더 짧다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
```

이게 전부다. 사용자가 `Authorization: Bearer eyJhbG...` 헤더를 달아 보내면, 이 한 묶음이 토큰의 서명을 검증하고, 만료를 확인하고, 발급자가 우리가 신뢰하는 그 IdP가 맞는지 확인한 뒤, `Authentication` 객체를 만들어 `SecurityContext`에 꽂아 준다. 컨트롤러는 `@AuthenticationPrincipal Jwt jwt`로 토큰을 받거나 `Authentication`을 주입받아 일을 시작한다.

여기까지만 보면 마치 마법 같다. 그렇다면 그 마법의 안쪽은 어떻게 생겼을까? 한 줄 한 줄 뜯어보자. 이 안쪽을 모르면, 함정에 빠졌을 때 어디서 빠진 건지 추적할 수 없다.

### `oauth2ResourceServer(o -> o.jwt(...))`가 하는 일

이 한 줄이 필터 체인에 `BearerTokenAuthenticationFilter`와 `JwtAuthenticationProvider`를 동시에 꽂는다. 2장에서 본 인증 흐름을 떠올려 보자. 필터가 요청에서 인증 정보를 뽑아 `AuthenticationToken`을 만들고, `AuthenticationManager`에 위임하고, `AuthenticationProvider`가 실제 검증을 수행한다. JWT의 경우 이 셋이 다음처럼 묶인다.

| 컴포넌트 | 역할 |
|---------|------|
| `BearerTokenAuthenticationFilter` | `Authorization: Bearer ...` 헤더(또는 `access_token` 폼·쿼리)에서 토큰 추출 |
| `BearerTokenAuthenticationToken` | 미인증 상태의 토큰 객체 |
| `JwtAuthenticationProvider` | `JwtDecoder.decode(...)`로 검증 + `JwtAuthenticationConverter`로 권한 매핑 |
| `JwtDecoder` | 서명·만료·발급자 검증의 실제 일꾼 |

핵심은 `JwtDecoder`다. 이 친구가 토큰의 진위 여부를 책임진다. 그리고 이 친구를 만드는 것이 바로 `issuer-uri` 한 줄이다.

### `JwtDecoders.fromIssuerLocation` — 한 줄이 만드는 네 가지 일

`issuer-uri: https://auth.example.com/realms/app` 한 줄을 적으면 Spring Security가 자동으로 `JwtDecoders.fromIssuerLocation(...)`을 호출한다. 이 한 메서드가 네 가지 일을 한다.

첫째, OIDC discovery 문서를 가져온다. `https://auth.example.com/realms/app/.well-known/openid-configuration`에 GET 요청을 보내 IdP가 자기 자신을 어떻게 소개하는지 읽는다. 여기에는 `issuer`, `jwks_uri`, `authorization_endpoint`, 지원하는 알고리즘 등이 들어 있다.

둘째, `jwks_uri`에서 JWKs(JSON Web Key Set)를 가져온다. IdP가 토큰 서명에 쓰는 공개키 집합이다. `kid`(key id)로 각 키를 식별할 수 있도록 되어 있다.

셋째, JWKs를 캐시한다. 매 요청마다 IdP에 공개키를 다시 묻는 일은 끔찍한 일이다. 트래픽도 늘고 IdP가 다운되면 전체 자원 서버가 죽는다. Spring Security는 캐시를 가지고 있다가 `kid`로 적중하지 않을 때만 다시 가져오는 식으로 동작한다.

넷째, `NimbusJwtDecoder`를 만들어 빈으로 등록한다. 이 디코더가 `iss`, `exp`, `nbf` 같은 기본 클레임을 자동 검증한다.

이 네 가지가 한 줄에 들어 있다. 다른 말로 하면, 이 한 줄을 적기 전에 IdP의 OIDC discovery가 켜져 있어야 한다. 자체 발급 IdP를 쓰는데 discovery 엔드포인트가 없다면 한 줄로 끝나지 않는다. 그땐 `jwk-set-uri`만 따로 지정하거나 `JwtDecoder`를 직접 빈으로 등록해야 한다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jwk-set-uri: https://auth.example.com/keys
```

`jwk-set-uri`만 적으면 discovery를 건너뛰고 JWKs만 가져온다. 다만 `iss` 검증은 자동으로 일어나지 않으니, `JwtDecoder`에 `OAuth2TokenValidator`를 직접 끼워 발급자 검증을 추가하는 편이 낫다.

### Spring Security 7에서 새로 생긴 두 가지 — `NimbusJwtDecoder` 커스텀 JwkSource와 `NimbusJwtEncoder` 빌더

7.0에서는 `NimbusJwtDecoder`가 커스텀 `JwkSource`를 받을 수 있게 되었다. 표준 JWKs URL 캐시를 그대로 두고 싶지만, 회전 정책이나 폴백 키 로직을 직접 짜야 하는 환경에서는 이 확장점이 매우 유용하다.

```java
@Bean
JwtDecoder jwtDecoder(JwkSource<SecurityContext> jwkSource) {
    return NimbusJwtDecoder.withJwkSource(jwkSource)
        .jwsAlgorithms(algs -> {
            algs.add(SignatureAlgorithm.RS256);
            algs.add(SignatureAlgorithm.ES256);
        })
        .build();
}
```

또 하나, `NimbusJwtEncoder`의 빌더가 생겼다. RSA·EC·secret key를 빌더로 선언하고 `JwtEncoderParameters`를 넣어 토큰을 발급할 수 있다. 자원 서버는 보통 토큰을 발급하는 쪽이 아니지만, 뒤에서 다룰 DPoP의 `DPoP` 헤더(클라이언트가 만드는 proof JWT)나 통합 테스트용 토큰 발급, 그리고 자체 마이크로서비스 간 토큰 발급에 그대로 쓸 수 있다.

```java
@Bean
NimbusJwtEncoder jwtEncoder(JWKSource<SecurityContext> jwkSource) {
    return new NimbusJwtEncoder(jwkSource);
}
```

이 두 가지 변화 덕분에 7.0에서는 "Spring Boot의 기본 설정"에서 한 발만 비켜나도 결국 직접 만들어야 했던 boilerplate가 크게 줄었다. 6.x까지는 키 회전 로직을 직접 짜려면 `NimbusJwtDecoder`를 우회해 `Nimbus` SDK를 통째로 임포트해야 했는데, 7.0에서는 Spring Security의 추상 안에서 끝낸다.

### `STATELESS` 한 줄의 의미

`sessionManagement(s -> s.sessionCreationPolicy(STATELESS))`를 적으면 Spring Security는 이 체인 안에서 세션을 만들지도, 읽지도 않는다. `HttpSession`이 생기지 않고, `JSESSIONID` 쿠키도 발급되지 않는다. 이게 stateless의 본질이다.

여기서 한 가지를 짚고 가자. `STATELESS`는 "Spring Security가 세션을 안 쓴다"는 뜻이다. 애플리케이션 코드에서 `request.getSession()`을 호출하면 그건 그대로 만들어진다. 가끔 "stateless인데 왜 JSESSIONID가 나오죠"라는 질문을 받는데, 거의 대부분 컨트롤러 어딘가에서 세션을 만들고 있다. JWT 자원 서버라면 컨트롤러나 인터셉터에서 세션을 건드리지 않는 편이 낫다.

### CSRF disable이 안전한 이유 — 그리고 안 안전한 경우

`csrf(CsrfConfigurer::disable)`도 같이 꽂혀 있다. JWT 자원 서버에서 CSRF가 안전하게 꺼지는 이유는 단순하다. CSRF 공격은 "브라우저가 자동으로 첨부하는 인증 정보"를 악용하는 공격이다. 쿠키는 브라우저가 자동으로 첨부한다. 그러나 `Authorization: Bearer` 헤더는 브라우저가 자동으로 붙여 주지 않는다. 자바스크립트가 명시적으로 헤더를 적어야 한다. 그래서 CSRF가 자연스럽게 무력화된다.

다만 한 가지 경우엔 찜찜하다. 토큰을 쿠키에 담아 보내고 서버가 쿠키에서 토큰을 읽도록 만들어 둔 경우다. 이때는 다시 쿠키 기반이 되니까 CSRF가 살아난다. "토큰을 쿠키에 담는데 CSRF disable로 두자"는 결정은 처음부터 다시 생각하는 편이 낫다. 5.3절 함정 7에서 다시 본다.

## 5.2 권한 매핑 — `scope`/`scp`에서 커스텀 `roles`까지

토큰의 서명이 검증되었다고 끝나는 것이 아니다. 이 토큰을 가진 사람이 무엇을 할 수 있는지를 결정해야 한다. Spring Security의 인가는 `Authentication`에 들어 있는 `GrantedAuthority` 컬렉션을 본다. JWT의 어떤 클레임이 이 컬렉션으로 바뀌는지가 권한 매핑의 핵심이다.

기본 동작은 단순하다. 토큰의 `scope` 또는 `scp` 클레임을 자동으로 `SCOPE_*` 권한으로 매핑한다. `scope: "read write admin"`이라는 토큰이 들어오면 `SCOPE_read`, `SCOPE_write`, `SCOPE_admin` 세 권한이 부여된다. URL 인가에서는 이렇게 쓸 수 있다.

```java
.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET, "/api/items").hasAuthority("SCOPE_read")
    .requestMatchers(HttpMethod.POST, "/api/items").hasAuthority("SCOPE_write")
    .anyRequest().authenticated())
```

여기까지가 표준 OAuth2 어휘다. 그런데 현실에서는 `roles`라는 커스텀 클레임을 쓰는 IdP가 많다. Keycloak, Auth0, Okta 모두 자기 입맛대로 클레임을 추가한다. 이때 손을 봐줘야 한다.

```java
@Bean
JwtAuthenticationConverter jwtAuthConverter() {
    var roles = new JwtGrantedAuthoritiesConverter();
    roles.setAuthoritiesClaimName("roles");
    roles.setAuthorityPrefix("ROLE_");
    var conv = new JwtAuthenticationConverter();
    conv.setJwtGrantedAuthoritiesConverter(roles);
    return conv;
}

@Bean
SecurityFilterChain api(HttpSecurity http, JwtAuthenticationConverter conv) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(conv)))
        .build();
}
```

`JwtGrantedAuthoritiesConverter`가 `roles` 클레임을 읽어 `ROLE_*` 접두어를 붙여 권한으로 만든다. 그 다음 `hasRole("ADMIN")`은 내부적으로 `ROLE_ADMIN` 권한을 찾는다. 이 짝을 맞추지 않으면 권한이 분명 토큰에 있는데도 403이 떨어진다. "분명히 admin 롤인데 왜 403이지?"라는 질문이 가장 자주 나오는 자리가 바로 여기다.

`hasAuthority`와 `hasRole`의 차이를 한 번 더 짚어 두자. `hasAuthority("ADMIN")`은 권한 이름이 정확히 `ADMIN`인지 본다. `hasRole("ADMIN")`은 자동으로 `ROLE_` 접두어를 붙여 `ROLE_ADMIN`을 찾는다. 변환기에서 `setAuthorityPrefix("ROLE_")`를 적었다면 `hasRole`을, 안 적었다면 `hasAuthority`로 풀네임을 적는 편이 일관성 있다.

### 중첩된 클레임 — Keycloak의 `realm_access.roles`

조금 더 까다로운 경우가 있다. Keycloak은 권한을 `realm_access.roles` 같은 중첩된 구조에 담는다. `JwtGrantedAuthoritiesConverter`는 일차원 배열만 지원하기 때문에 이 경우엔 변환기를 직접 짜야 한다.

```java
@Bean
JwtAuthenticationConverter keycloakJwtAuthConverter() {
    var conv = new JwtAuthenticationConverter();
    conv.setJwtGrantedAuthoritiesConverter(jwt -> {
        Map<String, Object> realm = jwt.getClaim("realm_access");
        if (realm == null) return List.of();
        Collection<String> roles = (Collection<String>) realm.get("roles");
        if (roles == null) return List.of();
        return roles.stream()
            .map(r -> new SimpleGrantedAuthority("ROLE_" + r))
            .collect(Collectors.toList());
    });
    return conv;
}
```

매 요청마다 도는 코드이므로 캐스팅 안전성에 신경 쓰는 편이 낫다. 한 IdP를 정해 변환기를 한 번 짠 다음, 사내 공유 라이브러리로 빼서 모든 자원 서버가 같은 변환을 쓰도록 만드는 편이 가장 깔끔하다.

### 변환기를 직접 갈아 끼우기 — `setJwtAuthenticationConverter` vs `Converter<Jwt, AbstractAuthenticationToken>`

권한만 바꾸는 것이 아니라 토큰을 어떤 `Authentication` 객체로 만들지를 통째로 바꾸고 싶을 때가 있다. 가령 토큰의 `sub`을 우리 도메인의 `UserId`로 정규화하거나, `preferred_username` 대신 우리 DB의 사용자 ID를 `principal`로 쓰고 싶다거나. 그땐 `JwtAuthenticationConverter`를 통째로 갈아 끼울 수 있다.

```java
Converter<Jwt, AbstractAuthenticationToken> converter = jwt -> {
    var authorities = extractRoles(jwt);
    var principal = userResolver.resolve(jwt.getSubject());
    return new JwtAuthenticationToken(jwt, authorities, principal.getUsername());
};
http.oauth2ResourceServer(o -> o.jwt(j -> j.jwtAuthenticationConverter(converter)));
```

다만 한 가지 주의할 점이 있다. 이 변환기는 매 요청 호출된다. 여기서 DB를 친다거나 외부 호출을 한다면 모든 요청 지연이 그만큼 늘어난다. 단순 캐싱이라도 끼워 두지 않으면 트래픽이 늘었을 때 끔찍한 일이 벌어진다. 가능하면 토큰 안에 있는 정보만으로 끝내고, DB가 필요한 결정은 컨트롤러 레벨에서 하는 편이 낫다.

## 5.3 Opaque Token + Introspection — JWT의 반대편

JWT가 모든 답은 아니다. JWT의 단점 하나가 강제 로그아웃이 어렵다는 것인데, 이 단점을 정면으로 해결하는 토큰이 불투명 토큰(opaque token)이다. 토큰 자체엔 의미가 없고, 그저 임의의 문자열이다. 서버가 토큰을 받으면 IdP의 introspection 엔드포인트(`POST /introspect`, RFC 7662)에 "이 토큰 살아 있나요? 권한은 뭐죠?"라고 묻는다. IdP가 응답을 돌려준다.

Spring Security 7에서는 이렇게 쓴다.

```java
http.oauth2ResourceServer(o -> o.opaqueToken(t -> t
    .introspectionUri("https://auth.example.com/oauth2/introspect")
    .introspectionClientCredentials("resource-server-id", "secret")));
```

`application.yml`로도 쓸 수 있다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        opaquetoken:
          introspection-uri: https://auth.example.com/oauth2/introspect
          client-id: resource-server-id
          client-secret: change-me
```

장단점이 분명하다. 장점은 강제 무효화가 즉시 반영된다. IdP에서 토큰을 폐기하면 다음 introspection이 `active: false`를 돌려준다. 단점은 매 요청마다 IdP에 네트워크 호출이 일어난다는 것이다. 트래픽이 늘면 IdP가 병목이 되고, IdP가 죽으면 자원 서버 전체가 죽는다.

이 단점을 완화하는 정석이 캐시다. Spring Security 7은 `OpaqueTokenIntrospector`를 빈으로 끼울 수 있게 해 두었으니, 캐싱 디코레이터를 한 번만 짜 두면 된다.

```java
@Bean
OpaqueTokenIntrospector cachingIntrospector() {
    var delegate = new SpringOpaqueTokenIntrospector(introspectionUri, clientId, secret);
    return new CachingOpaqueTokenIntrospector(delegate, Duration.ofMinutes(1));
}
```

`CachingOpaqueTokenIntrospector`는 Spring이 기본 제공하지 않으니 직접 짜야 한다. 핵심은 토큰을 키로 결과를 짧게 캐시하는 것이다. 캐시 만료를 너무 길게 잡으면 강제 로그아웃의 즉시성이 사라지므로, 1분 안팎이 보통의 절충점이다. 강제 로그아웃이 1분 이내 반영되면 충분하다는 정책이 운영 측에서 합의되어야 한다.

그렇다면 JWT와 불투명 토큰 중 무엇을 골라야 할까? 정답은 "둘 다 같이"인 경우가 많다. 마이크로서비스 사이는 stateless JWT로 빠르게 흐르고, 사용자 직접 노출 엔드포인트(특히 admin/billing 등 폐기가 시급한 영역)는 불투명 토큰으로 닫는 식이다. 둘을 섞을 때는 `securityMatcher`로 체인을 분리하는 편이 가장 깔끔하다.

## 5.4 JWT 함정 네 가지 — 가장 많이 보는 안티패턴

여기서부터가 이번 장의 무게중심이다. 위에서 본 정석은 한 번 익혀 두면 그대로 쓰면 된다. 문제는 정석을 알면서도 한 발씩 미끄러져 만들어지는 함정들이다. 네 개를 차례로 보자. 각각 "이런 코드를 본 적이 있는가"로 시작해서, 왜 위험한지 풀어내고, 어떻게 고치는지를 코드로 보여 준다.

### 함정 1 — JWT를 세션 토큰처럼 쓰는 경우

이런 코드를 본 적이 있는가? 사내 모놀리스에서 JWT를 발급해 쓰는데, 토큰 만료가 두 시간이고, 토큰 안에는 `sub`과 `roles` 정도밖에 없다. 사용자가 비밀번호를 바꿔도 그 시점에 발급된 토큰은 그대로 유효하다. 관리자가 어떤 사용자를 강제로 로그아웃시키려고 해도 토큰이 살아 있는 동안에는 방법이 없다.

> "Some experts argue that JWTs which just store a simple session token are inefficient and less flexible than a regular session cookie, and don't gain you any advantage." — GitHub Gist, Samsch

이건 사실 JWT의 결함이 아니라 **JWT를 안 어울리는 자리에 쓴 결과**다. 세션은 본질적으로 stateful이다. 강제 무효화가 가능해야 하고, 권한 변경이 즉시 반영되어야 한다. JWT는 정반대다. 서명된 그 시점의 정보를 그대로 들고 다닌다. 두 모델을 합치려는 시도가 함정 1을 만든다.

그렇다면 어떻게 해야 할까? 두 가지 길이 있다.

**해법 A — 짧은 access token + refresh token 회전.** Access token을 5~15분으로 짧게 잡고, refresh token으로 갱신한다. 강제 로그아웃이 필요하면 refresh token 쪽을 폐기하면 다음 갱신에서 끊긴다. 즉시성은 access token 수명만큼 늦지만, 5분 이내 반영되면 대부분의 운영 정책에 충분하다.

**해법 B — JWT는 그대로 두고 블랙리스트 캐시.** JWT의 `jti`(고유 ID) 클레임을 Redis 같은 저장소에 폐기 표시로 남긴다. 자원 서버가 토큰을 검증한 다음, `jti`가 블랙리스트에 있으면 거부한다. 매 요청 Redis를 한 번 더 친다는 점에서 stateless의 매력은 줄지만, 즉시성은 살아난다.

```java
@Bean
JwtDecoder jwtDecoder(JWTProcessor<SecurityContext> processor, RevokedJtiStore store) {
    var decoder = new NimbusJwtDecoder(processor);
    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
        JwtValidators.createDefaultWithIssuer(issuer),
        new RevokedJtiValidator(store)
    ));
    return decoder;
}

class RevokedJtiValidator implements OAuth2TokenValidator<Jwt> {
    private final RevokedJtiStore store;
    public OAuth2TokenValidatorResult validate(Jwt jwt) {
        String jti = jwt.getId();
        if (jti != null && store.isRevoked(jti)) {
            return OAuth2TokenValidatorResult.failure(
                new OAuth2Error("invalid_token", "Revoked", null));
        }
        return OAuth2TokenValidatorResult.success();
    }
}
```

여기서 한 가지 기억해 둘 점이 있다. 이 두 해법은 결국 stateless의 일부를 포기한 것이다. 그게 잘못된 결정은 아니다. 다만 "JWT를 쓰면 무조건 stateless"라는 신화를 깨고, "어디까지 stateless로 갈지를 의식적으로 결정한다"는 자세를 갖는 편이 낫다.

### 함정 2 — `localStorage`에 JWT 저장하기

이런 코드를 본 적이 있는가? 로그인 응답에서 받은 JWT를 SPA가 `localStorage.setItem('token', resp.token)`으로 저장한다. 이후 모든 fetch 호출에서 `Authorization: Bearer ${localStorage.getItem('token')}` 헤더로 토큰을 보낸다. 깔끔해 보이고, 만들기도 쉽다.

문제는 XSS다. 사이트 어딘가 하나라도 사용자 입력을 그대로 렌더하는 곳이 있으면 — 댓글, 검색어, 프로필 입력 — 공격자가 스크립트를 주입해 `localStorage.getItem('token')`을 자기 서버로 보낼 수 있다. XSS 한 번이면 끝이다. HttpOnly 쿠키는 자바스크립트에서 못 읽지만, `localStorage`는 같은 도메인 모든 스크립트에 열려 있다.

그렇다면 어디에 토큰을 둬야 할까? 세 가지 답이 있다.

**답 1 — HttpOnly·Secure·SameSite 쿠키.** 가장 표준적인 답이다. 자바스크립트에서 못 읽고, 브라우저가 요청에 자동으로 첨부한다. 다만 CSRF가 다시 살아나니까 CSRF 토큰을 같이 보내야 한다. 9장에서 더 깊이 본다.

**답 2 — 메모리에만 둔다.** 토큰을 자바스크립트 변수로만 들고, 새로고침 시 다시 인증한다. XSS에 대한 노출 시간을 페이지 라이프타임으로 줄인다. 다만 UX가 떨어지고, 새 탭이 열리면 다시 로그인이 필요하다.

**답 3 — BFF로 토큰을 브라우저에서 완전히 분리.** Backend-for-Frontend가 OAuth 클라이언트 역할을 하고, 브라우저는 자기 도메인의 HttpOnly 세션 쿠키만 가진다. 토큰은 BFF 서버에만 존재한다. SPA의 보안 모델로는 사실상 정답에 가깝다. 14장에서 BFF 패턴을 다룬다.

요약하자면 이렇다.

| 저장 위치 | XSS 노출 | CSRF 노출 | UX |
|----------|---------|----------|----|
| `localStorage` | 매우 높음 | 낮음 | 좋음 |
| `sessionStorage` | 매우 높음 | 낮음 | 보통 |
| 메모리 변수 | 낮음(페이지 단위) | 낮음 | 나쁨(새로고침 시 로그인) |
| HttpOnly 쿠키 | 없음(직접 탈취 불가) | 있음(대응 필요) | 좋음 |
| BFF(서버 측 저장) | 없음 | 있음(대응 가능) | 좋음 |

`localStorage`만 빨강이다. 한 번 새면 끝이라는 점에서 다른 옵션과 차원이 다르다. "JWT는 무조건 `localStorage`"라는 옛 튜토리얼은 잊는 편이 낫다.

### 함정 3 — `alg: none` 또는 알고리즘 confusion

이런 코드를 본 적이 있는가? 오래된 JWT 라이브러리를 쓰는 서버에서 `verify(token, publicKey)`를 호출했는데, 라이브러리가 토큰의 `alg` 헤더를 보고 "이건 `none`이니 서명 검증 안 함"이라고 판단해 통과시켜 준다. 또는 RSA로 서명된 토큰을 받기로 했는데, 공격자가 `alg`를 `HS256`으로 바꿔 RSA 공개키를 HMAC 키로 사용해 서명한 토큰을 보낸다.

이 두 가지가 JWT의 가장 유서 깊은 함정이다. RFC 8725(JSON Web Token Best Current Practices)가 첫 번째와 두 번째 권고로 정확히 이 둘을 짚고 있다.

> RFC 8725 권고 — 첫째, `alg: none`을 절대 받아들이지 말 것. 둘째, 서버가 알고리즘 화이트리스트를 강제할 것. 셋째, key confusion(HMAC 키를 공개키로 검증하는 식)을 방지할 것.

Spring Security의 `NimbusJwtDecoder`는 기본적으로 안전한 쪽으로 구성되어 있다. `JwtDecoders.fromIssuerLocation(...)`은 OIDC discovery에서 IdP가 지원하는 알고리즘 목록을 읽어 그것만 허용한다. 그러나 `JwtDecoder`를 직접 빈으로 등록할 때 흔하게 실수가 나온다. 다음 코드를 보자.

```java
// 위험 — alg 검증 없이 모든 알고리즘 허용
@Bean
JwtDecoder unsafeDecoder() {
    return token -> {
        var jwt = SignedJWT.parse(token);
        // 검증 없이 클레임만 꺼냄
        return new Jwt(token, ..., jwt.getJWTClaimsSet().getClaims());
    };
}
```

이건 극단적인 안티패턴이지만, 실제로 "토큰 디버깅"을 위해 임시로 짠 코드가 프로덕션에 흘러가는 사고가 있다. 정석은 이렇다.

```java
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder
        .withJwkSetUri("https://auth.example.com/keys")
        .jwsAlgorithms(algs -> algs.add(SignatureAlgorithm.RS256))  // 화이트리스트
        .build();
}
```

`jwsAlgorithms`로 명시한 알고리즘만 허용된다. `RS256`만 허용하면 공격자가 `HS256`이나 `none`으로 우회할 수 없다. 그리고 `withJwkSetUri`를 쓰면 `JWKSet` 안의 키 타입이 알고리즘과 짝이 안 맞을 때 자동으로 거부된다. RSA 공개키를 HS256으로 쓰려는 시도가 차단된다.

7.0에서 새로 생긴 `NimbusJwtDecoder.withJwkSource(...)`도 같은 안전 보장을 그대로 가져간다. 키 회전을 직접 짜더라도, 알고리즘 화이트리스트는 빠짐없이 적어 두는 편이 낫다.

또 한 가지 주의. 대칭키(HMAC) 기반 JWT를 쓰는 환경에서 키를 사람이 외울 수 있는 패스워드로 잡는 경우가 있다. `"my-secret-jwt-key"` 같은 식이다. RFC 8725는 약한 대칭키를 명시적으로 금지한다. HS256은 256비트(32바이트) 이상의 충분히 랜덤한 키를 써야 한다. 가능하면 비대칭(RSA/EC)으로 가는 편이 안전하다. IdP가 JWKs 회전을 지원하기도 쉽다.

### 함정 4 — Refresh Token 회전 미구현

이런 코드를 본 적이 있는가? Access token은 15분으로 짧게 잡았다. 좋다. 그런데 refresh token은 1년이다. 그리고 refresh token으로 새 access token을 요청하면, refresh token은 그대로 살아 있다. 그러면 refresh token은 사실상 1년짜리 영구 세션이다. 한 번 탈취되면 1년 내내 새 access token을 무한히 받아 갈 수 있다.

함정 4의 본질은 refresh token이 access token보다 훨씬 강한 자격증명이라는 사실을 잊는 것이다. Access token이 짧다고 안심하면 안 된다. 길게 살아 있는 refresh token이 그만큼 중요하다.

해법은 두 가지를 동시에 해야 한다.

**해법 1 — 회전(rotation).** Refresh token으로 갱신할 때마다 새 refresh token을 발급하고, 이전 토큰은 무효화한다. 정상 클라이언트는 항상 가장 최신 토큰만 가지고 있다.

**해법 2 — 재사용 감지(reuse detection).** 이미 무효화된 refresh token이 다시 들어오면, 그 사용자의 모든 refresh token을 폐기한다. 정상 클라이언트가 회전한 다음에는 옛 토큰을 절대 쓰지 않으니, 옛 토큰이 다시 들어왔다는 건 누군가가 옛 토큰을 가지고 있다는 뜻이다. 즉 탈취가 의심되는 상황이다. 가장 안전한 반응은 그 사용자의 세션을 통째로 끊고 재로그인을 요구하는 것이다.

Spring Authorization Server에서는 이 두 동작이 기본으로 들어 있다. 자체 발급 IdP를 만들 때는 직접 구현해야 하는데, 로직 자체는 단순하다.

```java
public TokenResponse refresh(String refreshToken) {
    var stored = refreshTokenRepo.findActive(refreshToken)
        .orElseThrow(() -> reuseDetected(refreshToken));

    refreshTokenRepo.markRevoked(stored.id());

    var newAccess = jwtIssuer.issueAccess(stored.userId());
    var newRefresh = refreshTokenRepo.issueNew(stored.userId(), stored.familyId());

    return new TokenResponse(newAccess, newRefresh);
}

private RuntimeException reuseDetected(String token) {
    refreshTokenRepo.findRevoked(token).ifPresent(revoked ->
        refreshTokenRepo.revokeFamily(revoked.familyId())  // 같은 사용자 패밀리 전체 폐기
    );
    return new BadCredentialsException("refresh token reuse detected");
}
```

`familyId`를 두는 이유는 한 사용자의 토큰 체인을 식별하기 위해서다. 회전이 일어날 때마다 같은 `familyId`로 새 토큰을 발급한다. 재사용이 감지되면 같은 `familyId`의 모든 토큰을 폐기해 그 사용자를 통째로 끊는다. 사용자 입장에선 강제 재로그인이지만, 토큰 탈취 의심 상황에서 이것 외에 더 안전한 대응은 없다.

여기까지가 JWT의 네 가지 함정이다. 마지막으로 RFC 8725의 권고를 우리 코드와 맞춰 보는 표 하나로 이 절을 닫는다.

### RFC 8725 권고 매핑

| RFC 8725 권고 | Spring Security 7 대응 | 우리가 신경 쓸 것 |
|---------------|----------------------|---------------|
| `alg: none` 거부 | `NimbusJwtDecoder` 기본 거부 | 직접 디코더 짤 때 화이트리스트 명시 |
| 알고리즘 화이트리스트 | `.jwsAlgorithms(...)` | 키 타입과 알고리즘 짝 검증 |
| Key confusion 방지 | `JWKSet` 기반 디코더 | 키 타입을 디코더에 직접 전달하지 말 것 |
| 약한 대칭키 금지 | — | HS256 키는 32바이트 이상 랜덤, 가능하면 비대칭으로 |
| 모든 클레임 검증 (`iss`, `aud`, `exp`, `nbf`) | `JwtValidators.createDefault[WithIssuer]` | `aud` 검증을 잊지 말 것(자원 서버 식별) |
| 페이로드는 평문 | — | PII·비밀을 클레임에 넣지 말 것 |

`aud` 검증이 비어 있는 경우가 의외로 많다. 같은 IdP가 여러 자원 서버에 토큰을 발급할 때, 자원 서버 A가 자원 서버 B용 토큰을 받아도 그냥 통과시킨다. 일종의 권한 상승 통로가 된다. `JwtDecoder`를 직접 빈으로 등록할 때는 `audience` 검증을 꼭 추가하자.

```java
OAuth2TokenValidator<Jwt> withAudience = jwt -> {
    if (jwt.getAudience() != null && jwt.getAudience().contains("api.example.com")) {
        return OAuth2TokenValidatorResult.success();
    }
    return OAuth2TokenValidatorResult.failure(
        new OAuth2Error("invalid_token", "invalid audience", null));
};
decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
    JwtValidators.createDefaultWithIssuer(issuer),
    withAudience
));
```

## 5.5 Bearer의 본질적 한계 — 그리고 sender-constrained 토큰

여기까지가 Bearer 토큰을 안전하게 쓰는 정석이다. 권한 매핑을 정확히 하고, 함정 네 개를 다 피했다고 하자. 그런데도 여전히 남는 위험이 하나 있다. 무엇일까? 토큰이 새는 순간 끝이라는 사실이다.

Bearer 토큰의 정의가 정확히 그런 의미다. "들고 있는 사람(bearer)이 권한자다." 토큰을 가지고만 있으면, 누가 가지고 있든 쓸 수 있다. 정당한 클라이언트가 만든 요청과 공격자가 그 토큰을 훔쳐 만든 요청을 자원 서버는 구별할 수 없다. HTTPS·HttpOnly·짧은 만료·재사용 감지를 다 해도, 어쨌든 어디선가 한 번 새면 그 만료 시간만큼은 공격자가 쓸 수 있다.

이걸 바꾸려면 토큰의 성격 자체를 바꿔야 한다. "들고만 있으면 쓸 수 있는" 토큰에서 "특정 클라이언트만 쓸 수 있는" 토큰으로. 이걸 sender-constrained 토큰이라고 한다.

토큰을 잘 만들었는데도 누군가 가로채면 끝이다. 그렇다면 어떻게 해야 할까? 토큰에 "이 토큰을 만들어 달라고 한 클라이언트의 키"를 묶어 두면 된다. 자원 서버는 요청이 들어올 때마다 "이 요청을 한 사람이 그 키를 정말로 가지고 있는지"를 확인한다. 키 없이는 토큰만으로 요청을 못 만든다. 토큰이 새도 키가 안 새면 안전하다.

이 아이디어를 표준화한 것이 RFC 9449, OAuth 2.0 DPoP-Bound Tokens다. 그리고 Spring Security 7이 자원 서버 측에서 이를 1급으로 처리한다.

### DPoP의 두 조각 — 토큰의 `cnf.jkt`와 매 요청 `DPoP` 헤더

DPoP는 두 가지가 한 쌍을 이룬다.

**첫 번째 조각 — 액세스 토큰의 `cnf.jkt` 클레임.** 클라이언트가 토큰을 요청할 때 자기 공개키의 SHA-256 thumbprint(`jkt`, JWK Thumbprint)를 같이 보낸다. IdP는 발급하는 access token JWT에 `cnf.jkt`라는 클레임으로 이 thumbprint를 박아 넣는다.

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-123",
  "aud": "api.example.com",
  "exp": 1700000000,
  "cnf": {
    "jkt": "0ZcOCORZNYy-DWpqq30jZyJGHTN0d2HglBV3uiguA4I"
  }
}
```

이 토큰은 그 thumbprint에 해당하는 키 쌍을 가진 클라이언트만 쓸 수 있다는 의미가 박혀 있다.

**두 번째 조각 — 매 요청의 `DPoP` 헤더.** 클라이언트는 자원 서버에 요청할 때 `Authorization: DPoP eyJhbG...`(`Bearer` 대신 `DPoP` 스킴) 헤더와 함께, `DPoP` 헤더에 별도의 JWT(DPoP proof)를 담아 보낸다. 이 proof JWT는 클라이언트가 자기 개인키로 서명한 짧은 JWT이고, 다음 클레임을 가진다.

| 클레임 | 의미 |
|--------|------|
| `htm` | HTTP 메서드 (예: `GET`) |
| `htu` | HTTP URI (예: `https://api.example.com/items`) |
| `iat` | 발급 시각 (보통 ±60초 윈도우 내) |
| `jti` | 고유 ID — 자원 서버가 재사용 방지에 쓸 수 있음 |
| `ath` | access token의 SHA-256 해시 — 어떤 access token에 짝지어진 proof인지 묶음 |

자원 서버는 이 proof JWT의 서명을 검증한다. 검증에 쓰는 공개키는 proof JWT의 `jwk` 헤더에 들어 있다. 그리고 그 공개키의 thumbprint가 access token의 `cnf.jkt`와 일치하는지 확인한다. 일치하면 "이 요청을 만든 사람이 토큰에 박힌 그 키를 가지고 있다"는 증명이 되는 것이다.

요약 흐름은 이렇다.

```
[Client] --(1) 토큰 요청 + 자기 공개키 thumbprint--> [IdP]
[IdP] --(2) access token (cnf.jkt 포함)--> [Client]

[Client] --(3) Authorization: DPoP <access_token>
              DPoP: <proof JWT signed by private key, with htm/htu/iat/jti/ath>
              --> [Resource Server]

[Resource Server]
  - proof JWT 서명 검증 (proof의 jwk 헤더에 있는 공개키로)
  - access token의 cnf.jkt == hash(proof.jwk) 확인
  - htm/htu가 요청과 일치하는지
  - iat가 너무 오래되지 않았는지 (±60초 등)
  - jti가 최근에 본 적 없는지 (replay 방지)
  - ath가 access token 해시와 맞는지
```

토큰만 새도 공격자는 클라이언트의 개인키가 없어 proof를 만들 수 없다. 토큰이 sender-constrain된다.

### Spring Security 7에서의 1급 처리

7.0은 이 검증 흐름을 자원 서버 측에서 표준 컴포넌트로 처리한다. 공식 docs의 dpop-tokens 페이지가 자원 서버 구성을 다룬다. 본질적으로는 `oauth2ResourceServer`의 JWT 디코더가 `cnf.jkt`와 `DPoP` 헤더를 짝지어 검증할 수 있도록 확장된 형태다.

```java
// 책 출간 시점의 7.x 정확한 시그니처는 공식 docs 재확인 필요
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o
            .jwt(Customizer.withDefaults())
            // DPoP를 1급으로 처리
        )
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .build();
}
```

7.0 GA(2025-11-17)에 기본 도입되었지만, 7.1.x 마일스톤에서 시그니처가 일부 다듬어질 수 있다. 책의 정확한 코드는 출간 시점에 공식 `dpop-tokens.html` 문서를 한 번 더 확인하는 편이 낫다. 핵심 개념은 안정되어 있다.

클라이언트 측에서 DPoP proof를 만들 때 7.0의 `NimbusJwtEncoder` 빌더가 그대로 쓰인다. 자기 EC 키 쌍을 만들고, 빌더에 키를 등록하고, `htm`/`htu`/`iat`/`jti`/`ath`를 클레임으로 채워 매 요청 발급한다. 공식 docs에 예제가 포함되어 있다. 클라이언트가 Spring Security 7을 함께 쓴다면 자원 서버와 발급 코드가 같은 추상 위에서 돌아간다.

### DPoP의 한계와 호환성

DPoP가 모든 답은 아니다. 몇 가지 제약을 알고 도입하는 편이 낫다.

**첫째, IdP 지원이 필요하다.** Access token에 `cnf.jkt`를 박는 것은 IdP의 일이다. Keycloak, Auth0, Okta, Spring Authorization Server가 단계적으로 DPoP를 지원하고 있다. 지원이 안 되는 IdP에서는 자원 서버만으로는 도입할 수 없다.

**둘째, 클라이언트 구현 복잡도가 올라간다.** 매 요청 proof JWT를 만들어야 한다. SPA에서는 WebCrypto API로 EC 키를 만들고 IndexedDB에 저장하는 식인데, 키 관리 로직 자체가 만만치 않다. 모바일 앱은 OS 키스토어에 키를 두는 식으로 비교적 깔끔하다.

**셋째, mTLS와 역할이 겹친다.** 클라이언트 인증서 기반 mTLS(RFC 8705)도 sender-constraining의 표준 방법이다. mTLS는 인프라 레벨(TLS terminator)에서 잡고, DPoP는 애플리케이션 레벨에서 잡는다는 차이가 있다. BFF 같은 confidential client는 mTLS가, 모바일·SPA처럼 인프라 통제가 약한 클라이언트는 DPoP가 더 자연스럽다.

**넷째, 모든 요청에서 검증이 일어난다.** Proof JWT 파싱과 서명 검증이 매 요청 도는데, 트래픽이 큰 서비스에서는 무시할 수 없는 비용이다. EC 서명(P-256)이 RSA보다 훨씬 빠르므로 키 타입을 EC로 잡는 편이 낫다.

그럼에도 불구하고 가치는 분명하다. OAuth 2.0 Security BCP(RFC 9700)가 권장하는 sender-constraining의 표준 구현이고, Bearer 토큰 모델로는 도달할 수 없는 위협 모델을 막아 준다. 토큰 탈취가 곧 계정 탈취로 이어지지 않게 만든다는 것은 운영적으로 매우 큰 안심이다. Zero Trust 원칙(NIST SP 800-207 tenet 4·6 — "동적이고 엄격한 인증·인가")과도 자연스럽게 맞아 들어간다.

도입은 단계적으로 가는 편이 낫다. 가장 민감한 자원 서버(admin·billing)부터 DPoP를 강제하고, 나머지는 Bearer를 유지하면서 차츰 늘려 간다. IdP·클라이언트·자원 서버 셋이 동시에 준비되어야 한다는 점만 잊지 않으면 된다.

## 5.6 운영 가이드라인 — 토큰 수명, 회전, 모니터링

이번 장의 정리로 운영 측 가이드라인 몇 가지를 묶어 두자. 코드 레벨에서 함정을 다 피했어도, 운영 정책이 흐트러지면 그 안전이 천천히 무너진다.

**Access token 수명.** 5~15분이 일반적인 절충점이다. 짧을수록 강제 무효화의 즉시성이 좋아지지만, refresh token 갱신 트래픽이 늘어난다. 너무 길게 잡으면(2시간 같은) 사실상 함정 1로 회귀한다.

**Refresh token 수명.** 회전이 정상 동작한다는 가정 아래 일 단위·주 단위 정도가 합리적이다. 회전이 없다면 refresh token은 그 수명만큼의 영구 세션이다.

**`aud` 클레임 검증.** 자원 서버가 여럿이면 반드시 켜자. 모든 자원 서버가 같은 IdP의 토큰을 무차별 받아들이면 권한 상승 통로가 된다.

**키 회전.** IdP의 JWKs를 자원 서버가 캐시한다. 회전 시 `kid`가 바뀌므로, 새 `kid`를 만난 자원 서버가 즉시 JWKs를 재조회하도록 디코더가 구성되어야 한다. `NimbusJwtDecoder`의 기본 동작이 이렇게 되어 있다. 직접 짠 디코더가 있다면 같은 동작을 보장하자.

**모니터링.** 거부된 토큰을 로그로 남기자. `alg` 헤더가 예상과 다른 토큰, `aud`가 다른 토큰, `cnf.jkt`가 일치하지 않는 토큰. 정상 트래픽에서는 거의 나오지 않아야 한다. 갑자기 늘어나면 공격 시도이거나 IdP 설정 실수다.

**로그에 토큰 자체를 남기지 말 것.** 끔찍하게 흔한 실수다. 인증 실패 디버깅을 위해 토큰을 통째로 로그에 찍는 사례가 있는데, 그 로그가 다른 시스템에 흘러가는 순간 토큰이 새는 것과 똑같다. 헤더 일부(앞 8자)나 `jti`만 남기는 정도가 안전선이다.

## 마무리

JWT는 매력적이지만 만만하지 않다. 한 줄로 자원 서버를 띄울 수 있다는 사실에 너무 빨리 끌려가면, 함정 네 개 중 하나에 다시 빠지기 쉽다. 이번 장에서 본 정석을 한 번 더 정리해 두자.

`issuer-uri` 한 줄이 OIDC discovery부터 JWKs 캐시·검증 디코더 등록까지 네 가지 일을 한다는 것을 기억해 두자. `STATELESS`는 Spring Security가 세션을 안 쓴다는 뜻이지, 애플리케이션이 세션을 안 쓴다는 뜻은 아니라는 점도 잊지 말자. 권한 매핑은 `scope`/`scp`가 자동이지만 커스텀 클레임은 직접 변환기를 끼워야 하고, `hasRole`과 `hasAuthority`의 짝을 맞추는 일이 가장 흔한 403의 원인이다.

함정 네 개는 코드 레벨에서 빠짐없이 점검하는 편이 낫다. JWT를 세션처럼 쓰지 말고, 강제 무효화가 필요하면 짧은 access token + refresh rotation 또는 블랙리스트로 의식적으로 결정하자. `localStorage`는 XSS 한 번이면 끝이라는 사실을 잊지 말고, HttpOnly 쿠키나 BFF로 옮기는 편이 낫다. `alg: none`과 알고리즘 confusion은 RFC 8725가 첫 번째로 경고하는 함정이고, 화이트리스트와 JWKs 기반 디코더로 막힌다. Refresh token rotation 없이 긴 수명을 잡으면 영구 세션이 되어 버린다는 점, 재사용 감지로 패밀리 전체를 폐기하는 정석을 함께 기억해 두자.

그리고 마지막으로 DPoP다. Bearer 토큰이 새는 순간 끝이라는 본질적 한계 위에, sender-constrained라는 한 층을 더 얹는 표준이다. Spring Security 7이 자원 서버 측에서 1급으로 처리한다는 것은, 우리가 Zero Trust 원칙에 한 발 더 가깝게 갈 수 있는 길이 열렸다는 의미다. 모든 자원 서버를 한 번에 바꿀 필요는 없다. 가장 민감한 영역부터, IdP·클라이언트가 준비된 순서대로 천천히 도입하자.

다음 6장에서는 자원 서버의 반대편, 즉 외부 IdP에 로그인을 위임하는 OAuth2 Client + OIDC Login의 흐름을 본다. 이번 장의 JWT 어휘 — `JwtDecoder`, `JwtAuthenticationConverter`, `Authentication` — 가 그대로 이어진다. 7.0에서 PKCE가 confidential client에도 기본 권장되는 변화부터 살펴보자.

---

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

---

# 7장. Passkeys·One-Time Token·MFA — 패스워드 너머의 인증

패스워드는 죽지 않는다. 죽지 않을 것이다. 하지만 패스워드만으로는 부족하다는 것이, 점점 분명해진다.

매년 유출되는 자격 증명 데이터베이스의 규모를 보고 있으면 묘한 무력감이 든다. 우리가 BCrypt로, Argon2로, Password4j로 아무리 정성스럽게 해시를 굽는다 한들, 사용자가 같은 패스워드를 다른 사이트에서 한 번이라도 재사용한다면 우리 서비스의 안전과는 무관하게 그 계정은 이미 위험에 노출된 셈이다. 한쪽에서 평문으로 보관되던 것이 다른 쪽까지 끌어내린다. 끔찍한 일이다.

그렇다면 어떻게 해야 할까? 답은 두 갈래다. 하나는 **패스워드를 보조할 두 번째 factor를 쌓는 것**(MFA), 또 하나는 **패스워드 자체를 공개키 암호로 대체하는 것**(Passkeys)이다. Spring Security 7.0은 이 두 갈래 모두에 1급 시민(first-class citizen) 대접을 한다. 6.4에서 시범적으로 들어왔던 **One-Time Token (OTT)**이 7.0에서 안정화되었고, 6.4에서 도입된 **WebAuthn / Passkeys** 지원이 7.0에서 본격적인 형태를 갖췄으며, 무엇보다 **MFA가 7.0의 신규 기능으로 정식 합류**했다. 이 세 가지를 한 자리에서 정리하자.

이 장은 책의 절정 중 하나다. 그러니 천천히 가자. 먼저 OTT로 호흡을 맞추고, Passkeys로 본격적인 공개키 세계에 발을 들이고, 마지막에 MFA로 이 모든 것을 묶는다.

---

## 7.1 One-Time Token — 매직 링크의 표준 자리

### 왜 OTT가 다시 떠올랐는가

이메일에 도착한 링크 하나를 눌러 로그인하는 경험을, 한 번쯤은 해봤을 것이다. Slack, Notion, Medium 같은 서비스에서 친숙해진 그 흐름. 흔히 **매직 링크(magic link)**라 부른다. 사용자에게 패스워드를 외우라고 강요하지 않고, 그가 통제하는 채널(보통 이메일)로 짧은 수명의 토큰을 보내 "당신이 이 메일을 받을 수 있다면 당신이 맞다"고 가정하는 패턴이다.

흥미로운 점은 이 패턴이 새롭지 않다는 사실이다. 비밀번호 분실(password reset) 메일이 사실은 매직 링크의 일종이다. 그런데도 **로그인** 동선으로 정식화하려고 하면 모두가 비슷한 코드를 다시 짠다. 토큰 만들고, 저장하고, 메일로 보내고, 쿼리스트링으로 받고, 한 번 쓰면 무효화하고…. 번거롭다. 번거롭다 못해 매번 자잘한 실수가 나온다. 만료 검증을 빼먹거나, 1회용을 보장하지 않거나, 토큰을 평문으로 저장하거나.

Spring Security는 6.4에서 이 패턴을 표준화한 `oneTimeTokenLogin()` DSL을 도입했고, 7.0에서 안정 단계로 끌어올렸다. 더 이상 이런 보일러플레이트를 직접 쓸 이유가 없다.

### 가장 작은 설정으로 시작하자

```java
@Configuration
class OttConfig {

    @Bean
    SecurityFilterChain ott(HttpSecurity http, MagicLinkSender sender) throws Exception {
        return http
            .authorizeHttpRequests(a -> a.anyRequest().authenticated())
            .oneTimeTokenLogin(ott -> ott
                .tokenGenerationSuccessHandler(sender::send))
            .build();
    }

    @Bean
    OneTimeTokenService oneTimeTokenService(JdbcOperations jdbc) {
        return new JdbcOneTimeTokenService(jdbc);
    }
}
```

여기에 등장하는 두 등장인물을 살펴보자.

**`OneTimeTokenService`**는 토큰의 저장소다. 기본 구현은 두 가지. `InMemoryOneTimeTokenService`는 개발·테스트용이고, `JdbcOneTimeTokenService`는 운영용이다. 토큰의 생성·검증·만료·1회 사용 보장이 이 한 빈에 위임된다. 우리가 직접 손댈 부분이 거의 없다.

**`OneTimeTokenGenerationSuccessHandler`**는 토큰이 생성된 직후의 후속 처리다. 즉, **사용자에게 토큰을 어떻게 전달하느냐**가 여기에 들어간다. 이메일이든 SMS든 카카오톡 알림이든, 전송 채널은 라이브러리가 강제하지 않는다. 우리가 직접 메서드 한 개를 구현하면 된다.

```java
@Component
class MagicLinkSender implements OneTimeTokenGenerationSuccessHandler {

    private final JavaMailSender mailSender;
    private final UriComponentsBuilder uriBuilder; // /login/ott?token=...

    public void handle(HttpServletRequest req, HttpServletResponse res, OneTimeToken token) {
        String link = uriBuilder.cloneBuilder()
            .queryParam("token", token.getTokenValue())
            .toUriString();

        SimpleMailMessage mail = new SimpleMailMessage();
        mail.setTo(token.getUsername());
        mail.setSubject("로그인 링크가 도착했습니다");
        mail.setText("아래 링크는 5분 동안만 유효합니다.\n\n" + link);
        mailSender.send(mail);
    }
}
```

이 핸들러는 **반드시 직접 구현해야 한다**는 점을 기억해두자. 라이브러리는 "토큰을 어디로 보낼지 알 수 없다"는 입장에서 추상화를 멈춘다. 메일·SMS·푸시·심지어 메신저 봇까지, 채널은 우리 도메인의 문제다. 이 분리가 처음에는 불친절해 보일 수 있지만, 우리 서비스에 맞춰 자유롭게 채널을 고를 수 있는 여지를 남긴 것이라고 생각하면 된다.

### 기본 페이지와 그 한계

설정만 해두면 Spring Security는 두 페이지를 자동으로 제공한다.

- `/ott/generate` — 사용자가 이메일을 입력해 토큰 발급을 요청하는 페이지
- `/login/ott` — 사용자가 받은 토큰을 제출하는 페이지(URL의 `token` 쿼리에서 자동 추출)

`mvn spring-boot:run`만 해도 바로 동작 확인이 된다. 매우 친절하다. 하지만 이 기본 페이지에 대해서는 한 가지 당부가 있다. **프로덕션에는 그대로 쓰지 않는 편이 낫다.** 디자인이 회사 톤과 어울리지 않는 것은 둘째 문제고, 더 큰 이유는 두 가지다.

첫째, 사용자가 매직 링크를 받기 전에 보게 되는 안내(예: "이메일을 확인해주세요" 같은 안내문)와 사용자가 링크 클릭 후 만료된 경우의 안내가 우리가 만들고 싶은 메시지와 다를 수 있다. 둘째, 본인 인증 절차나 캡차 같은 보호장치를 끼워 넣을 자리가 필요하다. 매직 링크 발급을 무방비로 열어두면 메일 폭격에 악용될 수 있다. 찜찜하다.

그러니 OTT를 시범적으로 붙여보고 동작이 확인되면, 두 페이지를 우리 프로젝트의 UI 컴포넌트로 옮겨오자. `loginPage()`와 `tokenGeneratingUrl()` 같은 설정으로 경로를 갈아끼울 수 있다.

### Magic Link 흐름을 한눈에

OTT가 무엇을 하는지 시퀀스로 보면 명확하다.

```
사용자             브라우저              Spring Security          MagicLinkSender
  │                  │                       │                         │
  │  이메일 입력     │                       │                         │
  │ ───────────────▶ │                       │                         │
  │                  │  POST /ott/generate   │                         │
  │                  │ ────────────────────▶ │                         │
  │                  │                       │  OneTimeTokenService    │
  │                  │                       │   .generate(username)   │
  │                  │                       │ ───────────┐            │
  │                  │                       │ ◀──────────┘            │
  │                  │                       │  handler.handle(token)  │
  │                  │                       │ ──────────────────────▶ │
  │                  │                       │                         │ 메일 발송
  │                  │  200 OK + "확인하세요"│                         │
  │                  │ ◀──────────────────── │                         │
  │   이메일 수신·링크 클릭                  │                         │
  │ ──────────────────────────────────────▶  │                         │
  │                  │  GET /login/ott?token │                         │
  │                  │ ────────────────────▶ │                         │
  │                  │                       │  service.consume(token) │
  │                  │                       │ ───────────┐            │
  │                  │                       │ ◀──────────┘            │
  │                  │  302 → / (인증 완료)  │                         │
  │                  │ ◀──────────────────── │                         │
```

핵심은 두 가지다. 첫째, **토큰은 1회용이다.** `consume()`이 호출된 순간 저장소에서 사라진다. 사용자가 실수로 같은 링크를 두 번 클릭해도 두 번 로그인되지 않는다. 둘째, **토큰은 짧은 수명이다.** 기본은 5분. 메일 지연이나 사용자의 게으름에 비해 너무 짧지 않으냐는 의견이 있을 수 있지만, 매직 링크의 보안 모델은 짧은 수명이 본질이다. 길게 잡고 싶다면 우리 도메인에서 의식적으로 그 트레이드오프를 선택해야 한다.

### OTT를 어디에 쓸까

OTT는 "사용자가 자기 채널을 통제한다"는 가정 위에서만 안전하다. 메일 계정이 탈취되면 우리 서비스도 함께 끌려간다. 그래서 OTT를 **단독 인증 수단**으로 쓰는 것은 한 번 더 생각해볼 일이다. 메일 보안에 의존도가 너무 커진다.

OTT가 가장 빛나는 자리는 **두 번째 factor**다. 패스워드를 한 번 검증하고, 추가로 OTT로 "이 사용자가 자기 메일을 진짜로 가지고 있는가"를 한 번 더 확인하는 흐름. 이 조합은 잠시 후 MFA 절에서 다시 보게 된다.

---

## 7.2 Passkeys — 서버는 비밀을 모른다

### 발상의 전환

OTT가 패스워드의 짐을 덜어주는 방식이라면, Passkeys는 패스워드 자체를 **대체**하는 방식이다.

원리는 이렇다. 사용자가 로그인할 때 서버로 보내는 것은 더 이상 어떤 비밀(secret)이 아니다. 사용자의 디바이스(아이폰의 Secure Enclave, 안드로이드의 Strongbox, Mac의 Touch ID, Windows Hello, YubiKey 같은 외장 키)가 가지고 있는 **개인키로 챌린지에 서명한 결과**다. 서버는 그 사용자의 **공개키**만 가지고 있고, 그것으로 서명을 검증한다. 즉,

> 서버는 사용자의 비밀을 모른다.

이 한 문장이 패스워드와 Passkeys의 가장 큰 차이다. 패스워드는 사용자의 비밀이 서버에 어떤 형태로든(해시라 해도) 도착한다. Passkeys에서는 비밀이 디바이스 밖으로 한 번도 나오지 않는다. DB가 유출되어도 그 안에 있는 것은 공개키뿐이라, 누구든 봐도 무방하다. 처음 이 발상을 마주했을 때 잠시 멈췄다. 이렇게 깔끔할 수도 있구나, 싶었다.

이 모델의 표준이 **W3C WebAuthn**이고, FIDO Alliance가 WebAuthn과 CTAP(외장 인증기 프로토콜)를 묶어 정의한 것이 **FIDO2**다. WebAuthn Level 3 워킹 드래프트는 2025년 1월에 공개되었고, **Passkey**는 이 위에서 "동기화 가능하고 다중 디바이스로 옮겨다닐 수 있는 사용자 친화적 자격증명"을 가리키는 마케팅적 용어로 굳어졌다. 우리가 화면에서 "Passkey로 로그인"이라고 적는 그 Passkey는, 사실은 그 아래 WebAuthn 규격을 따라 동작하고 있다.

### Spring Security가 도와주는 부분

WebAuthn을 직접 구현하려고 들면 만만치 않다. CBOR로 인코딩된 attestation 객체를 풀고, 다양한 attestation 포맷을 분기하고, 챌린지의 일회성과 origin·rpId의 일치를 검증하고…. 다행히 Spring Security 6.4에서 `spring-security-webauthn` 모듈이 합류했고, 내부적으로 검증된 `WebAuthn4J` 라이브러리에 위임한다. 우리가 직접 손댈 부분은 놀랄 만큼 적다.

가장 간단한 설정은 이것이다.

```java
@Bean
SecurityFilterChain passkey(HttpSecurity http) throws Exception {
    return http
        .formLogin(Customizer.withDefaults())
        .webAuthn(w -> w
            .rpId("example.com")
            .rpName("Example")
            .allowedOrigins("https://example.com"))
        .build();
}
```

세 가지 설정값을 짚어두자.

- **`rpId`** — Relying Party ID. 우리 서비스를 식별하는 도메인이다. 일반적으로 호스트명. 이 값은 자격증명이 어느 사이트에 묶여 있는지를 결정한다(이 묶임이 피싱을 막는 핵심 장치다). 서브도메인을 통합하려면 상위 도메인(`example.com`)을 잡는 것이 보통이다.
- **`rpName`** — Relying Party Name. 사용자의 화면(예: "이 사이트에 Passkey를 저장할까요?" 다이얼로그)에 표시되는 이름이다. 사용자가 알아볼 수 있게 적자.
- **`allowedOrigins`** — 자격증명 사용을 허용하는 origin 목록이다. 잘못 풀어두면 다른 origin에서도 우리 자격증명을 쓸 여지가 생긴다. 반드시 정확한 https URL로 한정하자.

이 설정만 해두면, `formLogin()`과 함께 기본 로그인 페이지에 **"Passkey로 로그인"** 버튼이 추가되고, `/webauthn/register`라는 등록 페이지도 자동으로 제공된다. 동작 확인이 즉시 가능하다.

### 등록 ceremony — 첫 한 번의 의식

Passkeys에서 "등록(registration)"과 "인증(authentication)"은 각각 **ceremony**라 불린다. 의식이라고 번역하니 좀 거창해 보이지만, 표준 문서가 그렇게 부르니 우리도 그 어휘를 따르자.

등록은 **사용자가 자기 디바이스를 우리 서버에 처음 묶는 과정**이다. 세 단계로 이루어진다.

```
브라우저                Spring Security                인증기(Authenticator)
   │                          │                              │
   │ ① POST /webauthn/register/options                       │
   │ ───────────────────────▶ │                              │
   │                          │ challenge·rpId·user.id 생성   │
   │ ◀─────────────────────── │                              │
   │   { challenge, rp, user, pubKeyCredParams, ... }        │
   │                          │                              │
   │ ② navigator.credentials.create(options)                 │
   │ ───────────────────────────────────────────────────────▶│
   │                          │              Touch ID / FIDO 키 누름
   │                          │              개인키 생성·attestation 서명
   │ ◀─────────────────────────────────────────────────────── │
   │   PublicKeyCredential { attestation, clientDataJSON }   │
   │                          │                              │
   │ ③ POST /webauthn/register                               │
   │ ───────────────────────▶ │                              │
   │                          │ WebAuthn4J가 검증·저장        │
   │ ◀─────────────────────── │                              │
   │   { success: true }                                     │
```

① 단계에서 서버가 챌린지를 만들고, ② 단계에서 브라우저가 인증기에게 "이 챌린지에 서명해줘"라고 부탁하면, ③ 단계에서 그 결과를 서버가 검증해 공개키와 자격증명 ID를 저장한다. 이게 전부다.

이때 저장되는 것은 **두 가지**다.

- **사용자 엔티티(`PublicKeyCredentialUserEntity`)** — `name`, `displayName`, 그리고 WebAuthn 안에서만 의미를 가지는 `user.id`. 우리 도메인의 username과는 별개로 관리된다.
- **자격증명(`CredentialRecord`)** — 그 사용자의 어느 디바이스가 어떤 공개키로 묶여 있는지. 한 사용자가 여러 디바이스를 가질 수 있으니 이 관계는 1:N이다.

이 두 데이터의 영속화가 다음 절에서 보는 JDBC 저장소다.

### 인증 ceremony — 매번의 의식

인증은 등록과 매우 비슷한 흐름인데, 키를 만드는 대신 **이미 있는 키로 서명**한다.

```
브라우저                Spring Security                인증기
   │                          │                              │
   │ ① POST /webauthn/authenticate/options                   │
   │ ───────────────────────▶ │                              │
   │                          │ challenge·allowCredentials 생성
   │ ◀─────────────────────── │                              │
   │   { challenge, allowCredentials, rpId }                 │
   │                          │                              │
   │ ② navigator.credentials.get(options)                    │
   │ ───────────────────────────────────────────────────────▶│
   │                          │              Touch ID 누름
   │                          │              개인키로 서명
   │ ◀─────────────────────────────────────────────────────── │
   │   AuthenticatorAssertion { signature, clientDataJSON }  │
   │                          │                              │
   │ ③ POST /login/webauthn                                  │
   │ ───────────────────────▶ │                              │
   │                          │ 공개키로 서명 검증·signCount 갱신
   │                          │ SecurityContext 채움          │
   │ ◀─────────────────────── │                              │
```

여기서도 ③ 단계의 검증이 핵심이다. WebAuthn4J가 챌린지의 일회성, origin의 일치, rpIdHash의 일치, `signCount`의 단조 증가(복제 자격증명 탐지) 등을 검사한다. 우리는 결과만 받는다.

### JDBC로 영속화하자

기본 상태에서는 자격증명이 **in-memory**에 저장된다. 데모로는 충분하지만, 서버가 한 번 죽으면 모든 사용자가 다시 등록해야 한다. 초난감한 상황이다. 프로덕션에서는 JDBC 저장소로 바꾸자.

```java
@Bean
PublicKeyCredentialUserEntityRepository userEntities(JdbcOperations jdbc) {
    return new JdbcPublicKeyCredentialUserEntityRepository(jdbc);
}

@Bean
UserCredentialRepository userCredentials(JdbcOperations jdbc) {
    return new JdbcUserCredentialRepository(jdbc);
}
```

이 두 빈을 등록하면 `WebAuthnConfigurer`가 자동으로 발견해 in-memory 대신 JDBC 구현을 쓴다. 테이블 스키마는 Spring Security 배포본의 `schema/webauthn` 디렉터리에 있으니 그대로 가져다 쓰면 된다.

운영에서는 한 가지 작은 결정을 더 해두는 편이 낫다. **자격증명 라벨**(`label`)이다. 한 사용자가 "회사 노트북", "개인 폰", "백업용 YubiKey"처럼 여러 자격증명을 가질 수 있는데, 분실 시 어느 것을 폐기할지 사용자가 알아볼 수 있어야 한다. 자동으로 "Macintosh"라는 이름만 보여주면 사용자는 자기 자격증명 목록을 보고도 어느 게 어느 것인지 헷갈리게 된다. 이 라벨을 사용자가 직접 정하게 하는 UI를 한 번에 만들어두는 편이 나중에 후회를 줄인다.

### 운영 함정 — Passkey 등록 후 패스워드를 꺼버리지 말자

이쯤에서 가장 강조해두고 싶은 운영 원칙이 하나 있다.

> **Passkey를 등록했다고 해서 패스워드를 꺼버리면 안 된다.**

기술적으로 가능하다. Passkey만으로 로그인하는 흐름은 동작한다. 그런데 사용자의 디바이스가 **분실되거나 망가지면 어떻게 될까?**

물론 Passkey는 iCloud Keychain이나 Google Password Manager 같은 클라우드를 통해 디바이스 간에 동기화될 수 있다. 그래서 폰 하나를 잃어도 새 폰으로 복구되는 경험이 많다. 그러나 모든 사용자가 동기화 가능한 Passkey만 쓰는 것은 아니다. YubiKey 같은 디바이스 바운드 Passkey만 가진 사용자는 그 키를 잃어버리면 끝이다. 또 동기화되더라도, 사용자가 클라우드 계정을 잃으면 함께 사라진다.

이때 **로그인 복구 동선**이 없으면, 우리 서비스는 사용자에게 "고객센터로 연락주세요" 외에는 해줄 말이 없게 된다. 끔찍한 일이다. 사용자는 단지 폰을 바꿨을 뿐인데 우리 서비스에서 영영 차단된다.

그래서 권장 패턴은 이렇다.

1. **Passkey를 기본 인증 수단으로 끌어올리되, 패스워드를 비활성화하지 않는다.**
2. **패스워드 분실 시 OTT(매직 링크)로 재설정할 수 있도록 동선을 열어둔다.**
3. **사용자 본인에게 "여러 개의 Passkey를 등록해두자"고 권장한다** — 폰 1개, 노트북 1개, 백업용 YubiKey 1개 같은 식으로.

Passkey의 보안적 우수성에 도취돼서 "패스워드는 이제 필요 없다"라고 잘라버리고 싶은 마음이 들 수 있다. 그러나 인증 시스템의 품질은 **잘 동작할 때**가 아니라 **무언가 잘못됐을 때**의 동선으로 결정된다. 잊지 말자.

### W3C WebAuthn / FIDO Alliance — 표준의 좌표

마지막으로, 우리가 다루는 것이 표준 어디에 위치하는지를 짚어두자.

- **W3C WebAuthn Level 3** — 브라우저 API(`navigator.credentials.create/get`)와 서버 측 검증 절차를 정의한 W3C 권고. 2025년 1월 워킹 드래프트가 공개되었다.
- **FIDO2** — FIDO Alliance가 WebAuthn(브라우저-서버 간 프로토콜)과 **CTAP**(브라우저-인증기 간 프로토콜)을 묶어 정의한 우산.
- **Passkey** — FIDO Alliance와 플랫폼 벤더(Apple, Google, Microsoft)가 함께 채택한 사용자용 용어. "동기화 가능한 WebAuthn 자격증명"이라고 봐도 무방하다.

Spring Security가 의존하는 `WebAuthn4J`가 이 모든 규격을 충실히 따르고 있고, 신뢰할 만한 attestation 검증과 metadata 서비스(FIDO MDS) 연동도 지원한다. 우리는 그 위에 서 있다는 점만 기억해두면 된다.

---

## 7.3 Multi-Factor Authentication — factor를 권한으로 본다

### 다른 프레임워크의 풍경

MFA를 정식으로 도입해본 적이 있는 사람은 그 작업의 무게를 안다. 보통 이런 식이다. 패스워드 로그인 성공 후 "절반쯤 인증된" 임시 세션을 만들고, 두 번째 factor 페이지로 보낸 뒤, 거기서 성공하면 비로소 "완전 인증된" 세션으로 승격한다. 그 사이를 표현하는 **상태 머신**이 필요하고, 인가 규칙도 그 상태를 따라 분기한다.

```
[anonymous] ── 패스워드 입력 ──▶ [partially-authenticated]
                                  ├─ OTT 입력 ─▶ [fully-authenticated]
                                  ├─ TOTP 입력 ─▶ [fully-authenticated]
                                  └─ 타임아웃 ─▶ [anonymous]
```

이 상태를 별도 객체로 관리하다 보면, 그 상태가 인가 코드로 새어 나간다. `if (auth.isFullyAuthenticated())` 같은 분기가 컨트롤러나 보안 설정에 박힌다. 우리가 만들고 있는 게 인가 시스템인지 상태 머신인지 헷갈리는 순간이 온다. 찜찜하다.

### 발상의 우아함 — "factor는 권한이다"

Spring Security 7.0의 MFA 모델을 처음 본 순간, 잠시 멈췄다.

> **factor를 추가 인증 메커니즘이 아니라 권한(Authority)으로 표현한다.**

이 한 줄에 모든 것이 담겨 있다. 패스워드로 인증되면 사용자는 `FACTOR_PASSWORD` 권한을 얻는다. OTT로 인증되면 `FACTOR_OTT` 권한을 얻는다. 그러면 "두 factor 모두 필요한 endpoint"는 어떻게 표현될까? **그냥 두 권한을 모두 요구하는 인가 규칙**이다. 별도의 상태 머신이 필요하지 않다.

이 발상이 우아한 이유는, Spring Security가 이미 가지고 있는 **인가 체계 위에 MFA가 그대로 녹는다**는 점이다. `GrantedAuthority`, `AuthorizationManager`, `authorizeHttpRequests` — 이 모든 기존 도구가 그대로 일한다. MFA는 새로운 개념을 도입하는 게 아니라, **권한이라는 기존 개념을 한 단계 더 잘 활용**하는 방식이다.

3장에서 우리는 `GrantedAuthority`가 "이 사용자가 가진 권한"을 표현하는 단순한 인터페이스라고 봤다. 거기에 `ROLE_USER`, `SCOPE_read:profile` 같은 값이 들어간다고 했다. 이제 그 자리에 `FACTOR_PASSWORD`, `FACTOR_OTT`가 들어간다고 생각하자. 같은 자리, 같은 의미. 권한이 누적되면 인가가 통과한다.

### 가장 기본적인 형태

```java
@Configuration
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
class MfaConfig {

    @Bean
    SecurityFilterChain http(HttpSecurity http, MagicLinkSender sender) throws Exception {
        return http
            .authorizeHttpRequests(a -> a.anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(ott -> ott.tokenGenerationSuccessHandler(sender::send))
            .build();
    }
}
```

여기서 일어나는 일을 단계로 풀어보자.

1. 사용자가 처음 접근한다. 어떤 권한도 없는 상태.
2. 인가 규칙(`anyRequest().authenticated()`)이 실패한다. 로그인 페이지로 redirect.
3. 사용자가 패스워드를 입력해 성공한다. 이 순간 부여되는 권한은 **`FACTOR_PASSWORD`뿐**이다. 아직 "완전 인증"이 아니다.
4. 사용자가 보호된 endpoint에 다시 접근하면, `@EnableMultiFactorAuthentication`이 요구하는 권한 집합(`FACTOR_PASSWORD` AND `FACTOR_OTT`) 중 `FACTOR_OTT`가 빠져 있음을 감지한다.
5. **자동으로 OTT 발급 페이지로 redirect.** 사용자는 메일로 받은 링크를 누른다.
6. OTT 검증이 성공하면 권한이 누적된다. 이제 `FACTOR_PASSWORD`와 `FACTOR_OTT` 모두 보유.
7. 원래 가려던 endpoint로 redirect. 통과.

여기서 두 가지를 짚어두자.

**첫째**, "1차 factor 성공 시 그 factor의 권한만 부여"라는 규칙이 핵심이다. 다른 프레임워크에서는 "절반 인증" 같은 별도 상태를 두지만, Spring Security 7.0에서는 그저 "권한이 일부만 있는 정상 인증"으로 본다. 권한이 부족하면 인가가 통과되지 않을 뿐이다.

**둘째**, **자동 redirect를 누가 해주는가?** 인가 체계가 직접 한다. Spring Security 7.0은 부족한 factor가 무엇인지 파악해서, 그 factor를 발급할 수 있는 페이지로 사용자를 안내한다. 우리가 컨트롤러에서 "if absent factor X then redirect to /Y" 같은 코드를 한 줄도 쓰지 않아도 된다.

### 선택적 MFA — 민감 endpoint에만 두 factor

전체 endpoint에 MFA를 강요하기는 무겁다. 보통은 **민감 endpoint**(관리자 페이지, 결제 정보 변경 등)에만 두 factor를 요구하고, 일반 endpoint는 하나의 factor로도 통과시키고 싶다. 7.0은 이것을 위한 깔끔한 길을 마련해두었다.

```java
@Bean
AuthorizationManagerFactory<RequestAuthorizationContext> mfa() {
    return new DefaultAuthorizationManagerFactory<>();
}

@Bean
SecurityFilterChain http(HttpSecurity http,
                         AuthorizationManagerFactory<RequestAuthorizationContext> mfa) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/admin/**").access(
                mfa.allAuthorities("FACTOR_PASSWORD", "FACTOR_OTT"))
            .anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .oneTimeTokenLogin(ott -> ott.tokenGenerationSuccessHandler(sender::send))
        .build();
}
```

여기 등장한 `AuthorizationManagerFactory`가 어떤 존재인지 잠깐 짚자. 이름이 거창하지만, 본질은 "여러 권한·역할 조합을 한 자리에서 만들어내는 빌더"다. `allAuthorities("FACTOR_PASSWORD", "FACTOR_OTT")`는 "이 두 권한이 모두 있어야 통과"라는 의미의 `AuthorizationManager`를 만들어 준다. 7.0에서 새로 들어온 `AllAuthoritiesAuthorizationManager`가 그 결과물이다.

이 팩토리는 8장에서 인가 모델을 본격적으로 다룰 때 다시 만나게 된다. 지금은 "MFA를 endpoint별로 켜고 끄는 손잡이"라는 정도로 이해해두면 충분하다.

> **8장 미리보기 — `AuthorizationManagerFactory`**
>
> 8장에서 우리는 인가가 살 수 있는 다섯 층(URL, 메서드, 도메인 객체, 메시지, 리액티브)을 차례로 본다. `AuthorizationManagerFactory`는 그 각 층에서 권한 조합을 일관되게 표현하기 위한 통합 진입점이다. 여기서는 **MFA를 일부 endpoint에만 적용하는 가장 깔끔한 길**이라는 한 가지 활용만 기억해두자.

### 기본 로그인 페이지가 friendly하게 도와준다 — `factor.type` / `factor.reason`

MFA의 사용자 경험에서 까다로운 부분은 "지금 사용자가 어느 단계에 있는지"를 화면이 알려주는 것이다. "패스워드를 다시 입력해주세요"인지, "이메일로 보낸 코드를 입력해주세요"인지가 모호하면 사용자는 화면 앞에서 멈춘다.

Spring Security 7.0의 기본 로그인 페이지는 이를 위해 두 가지 쿼리 파라미터를 자동으로 인식한다.

- **`factor.type`** — 어떤 factor를 요구하는지(예: `password`, `ott`)
- **`factor.reason`** — 왜 요구하는지(예: `missing`, `expired`)

자동 redirect 시 이 파라미터가 붙어서 도착하고, 기본 페이지가 그에 맞춰 적절한 안내를 보여준다. 예컨대 "두 번째 단계: 이메일로 보낸 링크를 클릭해주세요"라는 안내문이 자동으로 노출되는 식이다.

우리가 자체 UI로 갈아끼울 때는 이 두 파라미터를 우리 페이지에서 직접 읽어 분기해주면 된다. 컴포넌트 한두 개로 끝나는 일이지만, MFA의 사용자 경험에서 결정적인 차이를 만든다.

---

## 7.4 세 가지를 묶어보는 시나리오

지금까지 본 도구를 한 시나리오에서 조합해보자. 가상의 SaaS를 상상해보자. 이름은 **"InternalDocs"**라 하자. 사내 문서를 다루는 서비스다.

- **모든 사용자**는 로그인할 때 패스워드를 사용한다. 회사 메일을 외부에서 자주 접근하므로, **두 번째 factor**로 OTT를 강제한다.
- **관리자 페이지**(`/admin/**`)에는 한 단계 더 — Passkey가 등록된 사용자만 들어갈 수 있게 한다.
- **본인은** Passkey를 등록해두면, 다음번 패스워드 단계를 Passkey로 대체할 수 있다.

설정은 이렇게 짠다.

```java
@Configuration
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
class InternalDocsSecurity {

    @Bean
    SecurityFilterChain chain(HttpSecurity http,
                              MagicLinkSender sender,
                              AuthorizationManagerFactory<RequestAuthorizationContext> mfa) throws Exception {
        return http
            .authorizeHttpRequests(a -> a
                .requestMatchers("/admin/**").access(
                    mfa.allAuthorities("FACTOR_PASSWORD", "FACTOR_OTT", "FACTOR_WEBAUTHN"))
                .anyRequest().authenticated())
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(ott -> ott.tokenGenerationSuccessHandler(sender::send))
            .webAuthn(w -> w
                .rpId("internaldocs.example.com")
                .rpName("InternalDocs")
                .allowedOrigins("https://internaldocs.example.com"))
            .build();
    }

    @Bean
    OneTimeTokenService oneTimeTokenService(JdbcOperations jdbc) {
        return new JdbcOneTimeTokenService(jdbc);
    }

    @Bean
    PublicKeyCredentialUserEntityRepository userEntities(JdbcOperations jdbc) {
        return new JdbcPublicKeyCredentialUserEntityRepository(jdbc);
    }

    @Bean
    UserCredentialRepository userCredentials(JdbcOperations jdbc) {
        return new JdbcUserCredentialRepository(jdbc);
    }
}
```

(`FACTOR_WEBAUTHN`은 Passkey 인증 성공 시 부여되는 권한 이름이다. 정확한 상수는 Spring Security 문서를 따르되, 본질은 "Passkey라는 factor를 통과한 사람"이다.)

이 설정 한 묶음으로 무엇이 가능해지는지 정리하면 이렇다.

- 일반 사용자: 패스워드(`FACTOR_PASSWORD`) → OTT(`FACTOR_OTT`) → `/docs/**` 접근 가능
- 관리자: 위 두 factor 위에 Passkey(`FACTOR_WEBAUTHN`)까지 → `/admin/**` 접근 가능
- 누구든 Passkey 등록은 자기 페이지에서 자율적으로 — 등록되어 있으면 다음 로그인부터 패스워드 단계를 Passkey로 대체 가능
- 메일을 잃어버린 사용자: 패스워드는 살아있으니 매직 링크 재발급으로 복구 가능
- 폰을 잃어버린 사용자: Passkey가 사라져도 패스워드 + OTT 동선이 살아있으니 정상 로그인 가능, 그 후 새 Passkey를 다시 등록

세 가지 도구가 따로 일하지 않고 **한 모델 위에서 조립된다**. 이게 7.0이 우리에게 준 가장 큰 선물이다. 더 이상 인증을 직접 짤 일이 없다.

---

## 마무리

이번 장에서 다룬 세 가지를 한 줄씩 다시 새겨두자.

- **One-Time Token** — 매직 링크의 표준화. `OneTimeTokenService`로 저장하고, `OneTimeTokenGenerationSuccessHandler`로 메일/SMS를 직접 보낸다. 기본 페이지는 데모용. 프로덕션은 자체 UI로 옮기는 편이 낫다.
- **Passkeys** — 서버가 비밀을 모르는 인증. `WebAuthn4J`가 안에서 일한다. JDBC 영속화는 두 개의 Repository 빈으로 끝난다. **패스워드를 절대 꺼버리지 말자** — 디바이스 분실 복구 동선이 사라진다.
- **MFA** — factor를 권한으로 본다. `@EnableMultiFactorAuthentication`이 권한이 부족한 사용자를 자동으로 다음 factor 페이지로 안내한다. 선택적 MFA는 `AuthorizationManagerFactory.allAuthorities(...)`로 endpoint별 조립.

세 가지 모두에 공통된 한 가지 원칙이 있다. **"인증 흐름은 별도 상태 머신이 아니라, 권한이라는 단순한 어휘로 표현된다."** Spring Security 7.0이 이전 버전과 가장 다른 정신적 좌표가 여기다. 인증·인가의 경계가 흐려지면서, 우리는 "어느 factor를 통과했는가"라는 사실 자체를 권한으로 들고 다닌다. 이 관점이 익으면, 앞으로 만나게 될 새로운 인증 방식(예: WebAuthn 외의 어떤 것)도 같은 자리에 끼워 넣을 수 있다는 자신감이 생긴다.

자, 그러면 자연스럽게 다음 장으로 넘어갈 차례다. **권한**이라는 단어가 이 장에서 정말 많이 등장했다. 그런데 권한이 어디에서 만들어지고, 어디에서 검사되고, 어느 코드 층에 살아야 하는가? 8장에서 인가 모델의 다섯 층 구조 — URL, 메서드, 도메인 객체, 메시지, 리액티브 — 를 한 번에 정리하자. 이번 장에서 잠깐 만난 `AuthorizationManagerFactory`도 거기서 본격적으로 다룬다.

---

# 8장. 권한은 어디에 사는가 — 인가의 5층 구조

**선행 필요:** 2장(필터 체인), 3장(`AuthorizationManager`), 4~7장(권한·SCOPE·Authority의 생산자)

---

운영 중인 주문 시스템에 새 기능을 붙인다고 해보자. "관리자는 모든 주문을 취소할 수 있어야 한다. 매니저는 자기 부서의 주문만 취소할 수 있다. 일반 사용자는 본인이 만든 주문만 취소할 수 있다." 요구사항을 받아들고 IDE를 켠 순간, 가장 먼저 떠오르는 질문은 이것이다. 이 규칙들은 도대체 코드 어디에 살아야 하는가?

`SecurityFilterChain`의 `authorizeHttpRequests`에 한 줄 더 추가하면 될까? 컨트롤러 메서드 위에 `@PreAuthorize`를 붙이면 될까? 아니면 서비스 안에서 `if` 문으로 직접 비교해야 할까? 그것도 아니면 도메인 객체 자체에 권한 정보를 매달아야 할까?

어느 답이든 코드는 작동한다. 그러나 어디에 두느냐에 따라 6개월 뒤 운영의 모습이 완전히 달라진다. URL에만 의존하면 API 한 곳이 깨질 때마다 보안 규칙을 다시 짜야 한다. 서비스 안에 `if` 문을 흩뿌리면 보안 규칙이 비즈니스 로직 사이에 숨어 감사가 불가능해진다. 도메인 객체에 권한을 박으면 객체 모델이 점점 무거워진다.

Spring Security가 이 모든 층위를 한꺼번에 제공하는 데에는 이유가 있다. 모든 권한 검사를 한 층에 몰아넣으려는 시도는 거의 예외 없이 실패한다. 그렇다면 함께 사고 모델을 정돈해보자. 우리가 다룰 인가의 층은 다섯 개다.

## 8.1 권한이 사는 다섯 개의 층

OWASP가 2017판에서 5위였던 "Broken Access Control"을 2021판에서 **1위**로 올린 것은 우연이 아니다. 평균 발견율 3.81%. 열에 가까운 애플리케이션에 권한 결함이 살아 있다는 뜻이다. 그리고 결함의 대부분은 "권한 규칙을 어디에 둘지" 모호하게 흩뿌린 코드에서 자란다.

다섯 개의 층을 한눈에 보자. 위로 갈수록 거칠고(coarse-grained) 아래로 갈수록 미세하다(fine-grained).

```
┌─────────────────────────────────────────────────────┐
│ 1층. URL 패턴       authorizeHttpRequests            │   거칠다
│   ──────────────────────────────────────────────    │
│ 2층. HTTP Method    requestMatchers(POST, "/...")   │
│   ──────────────────────────────────────────────    │
│ 3층. 메서드 경계    @PreAuthorize / @PostAuthorize  │
│   ──────────────────────────────────────────────    │
│ 4층. 메타 어노테이션  @AdminOnly, @CanEditPost       │
│   ──────────────────────────────────────────────    │
│ 5층. 도메인 객체    #post.author == auth.name / ACL  │   미세하다
└─────────────────────────────────────────────────────┘
```

이 그림이 8장의 척추다. 다섯 층은 경쟁 관계가 아니라 **분담 관계**다. URL 한 줄로 막을 수 있는 건 1층에서 막아 비즈니스 코드를 깨끗하게 유지하고, 비즈니스 의미가 강하게 묶이는 규칙은 아래층으로 내려 보낸다. 그러면 코드 본문은 자기 책임에만 집중하고, 보안 규칙은 한곳에 모여 감사 가능한 형태로 남는다.

층 사이의 결정 기준을 한 문장으로 요약하면 이렇다. **"누가 호출했는가"만으로 결정되면 위층, "무엇을 향해 호출했는가"가 함께 필요하면 아래층이다.** `/admin/**`에 매니저 권한을 막는 건 위층의 일이다. "본인이 작성한 글만 수정 가능"이라는 규칙은 도메인 객체를 봐야 결론이 나니 아래층의 일이다.

이제 한 층씩 내려가 보자.

## 8.2 1층 — URL 기반 인가

가장 거친 층은 URL이다. `SecurityFilterChain` 안에서 `authorizeHttpRequests` 한 블록으로 끝난다. 7.0에서 가장 눈에 띄는 변화는 매처가 `PathPatternRequestMatcher`로 통일됐다는 점이다. Spring MVC가 라우팅에 쓰는 바로 그 패턴 파서를 보안 매칭에도 동일하게 쓴다. 6.x 시절 `mvcMatchers`/`antMatchers`/`AntPathRequestMatcher` 사이를 오가며 `/api`와 `/api/`가 같은지 다른지 헷갈리던 시간은 이제 끝난다. 좋은 일이다.

기본 형태부터 보자.

```java
http.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET, "/health").permitAll()
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .requestMatchers("/orders/**").hasAuthority("SCOPE_orders.read")
    .anyRequest().authenticated()
);
```

코드를 위에서 아래로 읽으면 그대로 의미가 잡힌다. `/health`는 누구나 통과. `/admin/**`은 `ADMIN` 역할만. `/orders/**`는 `SCOPE_orders.read` 권한을 가진 자만. 그 외 모든 요청은 인증된 사용자여야 한다.

여기서 한 가지 짚고 가자. **순서가 의미를 만든다.** Spring Security는 위에서 아래로 매칭을 시도하고, 첫 매치에서 결정을 확정한다. `anyRequest()`를 가장 먼저 두면 그 아래 규칙들은 영원히 도달하지 않는다. 처음 이 사실을 모르고 `anyRequest().permitAll()`을 맨 위에 둔 코드는 그야말로 끔찍한 일이다. 모든 URL이 무방비로 열린다.

7.0의 통일 매처는 path variable 매칭도 일관되게 처리한다.

```java
var p = PathPatternRequestMatcher.withDefaults();
http.authorizeHttpRequests(a -> a
    .requestMatchers(p.matcher("/products/{id}")).hasRole("USER")
    .requestMatchers(p.matcher("/products/{id}/edit")).hasRole("ADMIN")
    .anyRequest().authenticated());
```

같은 path variable을 컨트롤러와 보안 규칙이 똑같이 해석한다는 점은 마음의 평화에 큰 도움이 된다. 6.x에서 trailing slash 하나로 403과 200이 갈렸던 함정이 사라진 셈이다.

## 8.3 2층 — HTTP Method까지 보는 인가

URL이 같아도 `GET`과 `POST`는 의미가 다르다. 같은 `/posts/{id}`라도 조회는 누구나 가능하지만 수정은 작성자만 가능해야 하는 경우가 그렇다. 이때 2층으로 내려간다.

```java
http.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET,  "/posts/**").permitAll()
    .requestMatchers(HttpMethod.POST, "/posts/**").hasRole("USER")
    .requestMatchers(HttpMethod.PUT,  "/posts/**").hasRole("USER")
    .requestMatchers(HttpMethod.DELETE, "/posts/**").hasRole("ADMIN")
    .anyRequest().authenticated()
);
```

HTTP 메서드를 첫 인자로 추가하기만 하면 끝이다. 코드를 읽어보면 머릿속에 자연스럽게 "조회는 열고, 작성·수정은 사용자, 삭제는 관리자"라는 문장이 그려진다. 의미가 코드에 그대로 박힌다. 이게 1·2층 인가가 주는 가장 큰 가치다. **권한 규칙이 비즈니스 코드 바깥에 명문화되어 한곳에 모인다.**

여기서 `hasRole`과 `hasAuthority`, `hasAnyRole`이 어떻게 다른지 한 번 정리하고 가는 편이 낫다. 이 셋의 차이를 모호하게 두면 두고두고 디버깅의 원흉이 된다.

### `hasRole` vs `hasAuthority` vs `hasAnyRole`

Spring Security 내부에서 권한은 모두 `GrantedAuthority`라는 한 가지 타입이다. `ROLE_ADMIN`, `SCOPE_orders.read`, `factor.password` 같은 문자열이 모두 같은 통 안에 들어 있다. 그렇다면 왜 `hasRole`과 `hasAuthority`가 따로 있을까?

답은 `ROLE_` 접두사다.

- `hasRole("ADMIN")` — 내부에서 자동으로 `"ROLE_"`을 붙여 `ROLE_ADMIN`을 찾는다. 인자에는 절대 `ROLE_`을 붙이지 말자.
- `hasAuthority("ROLE_ADMIN")` — 접두사를 붙이지 않는다. 문자열 그대로 매칭한다.
- `hasAuthority("SCOPE_orders.read")` — OAuth2 스코프처럼 `ROLE_`이 붙지 않는 권한을 검사할 때 쓴다.
- `hasAnyRole("ADMIN", "STAFF")` — `hasRole`의 OR 버전. 역시 `ROLE_`이 자동으로 붙는다.
- `hasAnyAuthority(...)` — `hasAuthority`의 OR 버전. 접두사 처리 안 함.

규칙을 한 줄로 요약하면, **"`ROLE_`을 자동으로 붙여주는 게 `hasRole`, 안 붙이는 게 `hasAuthority`"**다. 두 함수를 같은 코드에서 섞어 쓸 때 가장 자주 사고가 난다. 예를 들어 `hasRole("ROLE_ADMIN")`이라고 쓰면 내부에서 `ROLE_ROLE_ADMIN`을 찾아 헤매다 실패한다. 이런 코드가 운영 환경에 올라가서 며칠 동안 "왜 관리자가 들어가지지 않는다는 컴플레인이 들어오지?"로 헤매면 정말로 난감해진다. 기억해두자.

OAuth2 스코프는 거의 항상 `hasAuthority`로 검사한다. 5장에서 본 것처럼 JWT의 `scope` 클레임은 기본적으로 `SCOPE_` 접두사가 붙은 `GrantedAuthority`로 매핑된다. `SCOPE_`는 `ROLE_`이 아니므로 `hasRole`로는 잡을 수 없다.

## 8.4 3층 — 메서드 경계의 인가

URL이 막지 못하는 상황을 생각해보자. 같은 컨트롤러의 같은 엔드포인트로 들어오는 요청인데, 내부의 어떤 서비스 메서드를 호출하느냐에 따라 권한이 갈려야 한다면 어떻게 할까? 또는 컨트롤러를 거치지 않고 스케줄러·메시지 컨슈머가 비즈니스 메서드를 직접 부를 때 동일한 권한 규칙을 적용하고 싶다면?

이때 3층이 필요하다. 메서드에 직접 인가를 거는 Method Security다.

```java
@Configuration
@EnableMethodSecurity   // ← 7.0의 표준
class SecConfig {}

@Service
class OrderService {

    @PreAuthorize("hasRole('ADMIN')")
    public void cancelAll() { ... }

    @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
    public Order findById(Long id) { ... }
}
```

`@PreAuthorize`는 메서드 진입 직전에 SpEL 식을 평가해 통과 여부를 결정한다. 통과하지 못하면 `AccessDeniedException`이 던져지고, 8.10절에서 다룰 `ExceptionTranslationFilter`가 이를 403 응답으로 번역한다. `@PostAuthorize`는 메서드가 반환한 뒤 반환값을 보고 결정한다. `@Secured`는 역할만 보는 단순한 형태다. `@PreAuthorize`가 가장 표현력이 좋고, 실무에서 압도적으로 많이 쓰인다.

여기서 가장 중요한 함정을 한 절 통째로 할애해 짚어야 한다.

### 함정 — `@EnableGlobalMethodSecurity` 잔존 시 `@PreAuthorize`가 소리 없이 무력화된다

6.2.7 issue #17487에 이런 질문이 올라온 적이 있다.

> "왜 내 `@PreAuthorize`가 동작 안 하는지 모르겠다. 코드는 컴파일되고, 앱은 정상 기동되고, 에러도 안 난다. 그런데 관리자 권한이 없는 사용자도 `cancelAll()`을 호출할 수 있다."

원인은 단 한 줄이었다. 설정 클래스에 옛날 어노테이션 `@EnableGlobalMethodSecurity`가 그대로 남아 있던 것. Spring Security 6.x 어느 시점부터 이 어노테이션은 deprecated가 되었고, 6.2.7에서는 **메서드 보안 빈(`MethodSecurityInterceptor`)을 등록하지 않는다.** 경고 로그도, 예외도 없다. `@PreAuthorize`가 그냥 평범한 어노테이션 한 줄이 되어 컴파일러를 통과한다.

> "If you only supply `@EnableGlobalMethodSecurity`, no method-security beans are registered, and no warning or error is logged. As a result, annotations like `@PreAuthorize` silently have no effect." — Spring Security issue #17487

소리 없이 깨지는 건 가장 끔찍한 종류의 버그다. 빨간 줄이 뜨지 않고, 테스트가 잘 짜여 있지 않으면 운영에 올라가서야 발견된다. 그것도 누군가 권한 검사를 우회한 흔적이 로그에 찍히고 나서.

7.0으로 올릴 때, 또는 6.x에서 이미 작업 중이라면 반드시 한 번은 전체 모듈을 grep해두자.

```bash
grep -rn "@EnableGlobalMethodSecurity" src/
```

한 줄이라도 잡히면 즉시 `@EnableMethodSecurity`로 교체한다. `@EnableMethodSecurity`는 `@PreAuthorize`/`@PostAuthorize`/`@Secured`/`@PreFilter`/`@PostFilter`를 모두 기본 활성화한다. 옵션(`prePostEnabled`, `securedEnabled` 등)을 굳이 명시할 필요도 없다. 모르고 옛 어노테이션을 쓰는 것보다, 명확하게 새 어노테이션 한 줄을 두고 두 발 뻗고 자는 편이 낫다.

### SpEL의 매력과 위험

`@PreAuthorize`의 진짜 힘은 SpEL에서 나온다.

```java
@PreAuthorize("hasRole('ADMIN') and #user.id == authentication.principal.id")
public void updateProfile(User user) { ... }
```

이 식은 두 가지를 동시에 검사한다. 호출자가 `ADMIN` 역할을 가졌고, **메서드 인자로 들어온 `user` 객체의 `id`가 인증된 주체의 `id`와 같은가**. SpEL 안에서 메서드 인자(`#user`), 인증 객체(`authentication`), 주체(`principal`)를 모두 참조할 수 있다. 이게 매력이다. 비즈니스 의미를 어노테이션 한 줄에 담을 수 있다.

그러나 매력은 위험과 짝을 이룬다. 식이 길어지면 어떤 일이 벌어지는지 보자.

```java
@PreAuthorize(
  "hasRole('ADMIN') or " +
  "(hasRole('MANAGER') and #order.department == authentication.principal.department) or " +
  "(hasRole('USER') and #order.userId == authentication.principal.id and " +
  "  #order.status == T(com.example.OrderStatus).DRAFT)"
)
public void cancelOrder(Order order) { ... }
```

코드 본문보다 어노테이션이 길다. SpEL이라 컴파일 타임 타입 체크가 약하고, 리팩토링 때 IDE가 따라가지 못한다. 단위 테스트를 짜려면 `MethodSecurityExpressionHandler` 컨텍스트가 필요해서 순수 자바 테스트로는 검증되지 않는다.

**보안 규칙이 코드 본문을 가린다면, 결국 보안이 비즈니스의 적이 된다.** 어떤 시점이 오면 SpEL을 줄이고 비즈니스 메서드 안에서 명시적으로 `AuthorizationManager`를 부르는 편이 낫다. SpEL은 "한 문장으로 자연스럽게 읽힐 때까지"가 사용 한계라고 마음에 두자.

### 커스텀 SpEL 함수 — `MethodSecurityExpressionHandler`

SpEL 식이 반복된다면 함수로 추출하는 편이 깔끔하다. `MethodSecurityExpressionRoot`를 확장하거나, 별도 빈을 등록해 `@bean.method()` 형태로 호출할 수 있다.

```java
@Component("perm")
class PermissionChecker {
    public boolean canEditOrder(Long orderId) {
        // 복잡한 권한 로직을 자바로 표현
        return orderRepository.findById(orderId)
            .map(o -> o.belongsToCurrentUser())
            .orElse(false);
    }
}

@Service
class OrderService {
    @PreAuthorize("@perm.canEditOrder(#orderId)")
    public void edit(Long orderId, EditCommand cmd) { ... }
}
```

SpEL 식은 짧게 유지하고 복잡한 판단은 자바 코드에 둔다. 테스트도 `PermissionChecker`만 단위 테스트로 검증할 수 있다. **SpEL은 가능한 한 호출 한 줄에 가깝게 유지하는 편이 바람직하다.**

`MethodSecurityExpressionHandler`를 직접 커스터마이즈해야 하는 경우는 흔하지 않다. 다만 모든 메서드 보안 식에 공통 변수를 주입하거나, 평가 환경을 통째로 바꿔야 할 때는 빈으로 노출해 교체할 수 있다.

```java
@Bean
static MethodSecurityExpressionHandler expressionHandler(RoleHierarchy roleHierarchy) {
    var handler = new DefaultMethodSecurityExpressionHandler();
    handler.setRoleHierarchy(roleHierarchy);
    return handler;
}
```

여기에 8.7절에서 다룰 `RoleHierarchy`를 주입하면, `@PreAuthorize("hasRole('STAFF')")`라고 써도 `ADMIN`이 자동 통과한다.

## 8.5 4층 — 메타 어노테이션으로 의미를 묶기

`@PreAuthorize("hasRole('ADMIN')")`가 코드베이스 곳곳에 반복된다고 상상해보자. 50개 메서드에 같은 식이 박혀 있다면, 정책이 바뀌어 `ADMIN`을 `SUPER_ADMIN`으로 바꿔야 할 때 50번 수정해야 한다. 한 줄이라도 빠뜨리면 그 메서드는 다음 빌드까지 잠재적 보안 구멍으로 남는다. 찜찜한 일이다.

해법은 의미를 묶는 것이다. Spring Security 6.3부터 메타 어노테이션 패턴이 1급으로 지원된다.

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@PreAuthorize("hasRole('ADMIN')")
public @interface AdminOnly {}

@Service
class OrderService {
    @AdminOnly
    public void cancelAll() { ... }

    @AdminOnly
    public void purgeOldOrders() { ... }
}
```

`@AdminOnly`라는 이름이 코드에 박힌다. 의미가 즉시 읽힌다. 그리고 정책이 바뀌면 `@AdminOnly` 어노테이션 정의 한 곳만 수정하면 된다. 50개 메서드는 그대로다.

좀 더 흥미로운 예를 보자.

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@PreAuthorize("hasRole('USER') and #post.author == authentication.name")
public @interface CanEditOwnPost {}

@Service
class PostService {
    @CanEditOwnPost
    public void edit(Post post, EditCommand cmd) { ... }
}
```

"자신이 작성한 게시물만 수정 가능"이라는 정책이 어노테이션 이름으로 코드에 박힌다. 본문은 그저 `edit(...)` 한 줄이다. **코드와 정책이 한 줄 안에 자연스럽게 동거한다.** 이 정도가 메서드 보안의 이상적인 모습이다.

7장에서 본 `@EnableMultiFactorAuthentication`도 사실은 메타 어노테이션 묶음의 한 형태다. MFA 정책을 `factor.password`와 `factor.ott` 같은 권한으로 표현하고, 메타 어노테이션으로 의미를 묶는 흐름이 7.0의 권장 방향이다.

## 8.6 5층 — 도메인 객체 단위 인가

가장 미세한 층이다. "본인이 작성한 게시물만 수정 가능"이라는 규칙은 4층 메타 어노테이션의 SpEL로 표현했지만, 그것이 가능했던 건 `#post`라는 메서드 인자에서 작성자 정보를 꺼낼 수 있었기 때문이다. 인자만으로 결정되지 않고 더 복잡한 객체 단위 권한이 필요하다면 어떻게 할까?

대부분의 경우, SpEL과 `AuthorizationManager`만으로 충분히 풀린다.

```java
@PreAuthorize("#post.author == authentication.name")
public void deletePost(Post post) { ... }
```

```java
@PreAuthorize("@postPermissionService.canEdit(#postId, authentication.name)")
public void editPost(Long postId) { ... }
```

이 두 패턴이 5층의 90%를 차지한다. SpEL이 객체 속성과 인증 주체를 직접 비교하거나, 별도 권한 빈에 위임해서 자바 코드로 판단을 위임하는 것. 권한 결정이 객체의 상태에 따라 달라지더라도 결국 한 번의 함수 호출로 답이 나온다면 이 두 패턴으로 끝난다.

> ### 박스 — 도메인 객체 ACL이 필요해지는 순간
>
> 그런데 가끔, 정말 가끔, 객체 인스턴스 단위 권한이 시스템 전체에 걸쳐 영속화되어야 하는 경우가 있다. "특정 게시물 ID에 대해 사용자 A는 읽기, B는 읽기·쓰기, C는 권한 없음"이 데이터로 관리되는 위키 시스템이나 협업 도구가 그렇다. 이때 `spring-security-acl` 모듈이 등장한다.
>
> ACL은 별도 테이블(`acl_object_identity`, `acl_entry` 등)에 객체별 권한을 저장하고, `@PreAuthorize("hasPermission(#post, 'WRITE')")` 같은 표현식으로 검사한다. 강력하지만 **무겁다.** 별도 스키마, 별도 캐시, 별도 운영. 작은 시스템에서 도입하면 배보다 배꼽이 더 커진다.
>
> 그러니 ACL은 마지막 선택지로 두는 편이 낫다. 객체 ID별 권한 저장이 시스템의 핵심 기능이라면 도입하고, 그게 아니라면 SpEL과 `AuthorizationManager` 빈으로 충분하다. "ACL이 필요한 것 같다"고 느낄 때, 한 번 더 "이 정책을 권한 빈 하나로 표현할 수 없는가?"를 물어보자.

도메인 객체 인가의 핵심은 결국 **"코드 본문은 비즈니스만, 권한은 메타 어노테이션이나 SpEL로 모아두기"**다. 객체 안에 권한 메서드(`isOwnedBy(user)` 같은)를 두는 건 자연스럽지만, 그것을 호출하는 책임은 도메인 객체 자신이 아니라 메서드 보안 층에 두는 편이 깔끔하다.

## 8.7 Role Hierarchy — 권한을 계층으로 묶기

요구사항이 이렇게 바뀌었다고 해보자. "관리자는 매니저가 할 수 있는 일을 모두 할 수 있어야 한다. 매니저는 일반 사용자가 할 수 있는 일을 모두 할 수 있어야 한다." 가장 둔한 방법은 모든 메서드에 `hasAnyRole('ADMIN', 'MANAGER')`라고 죽 늘어놓는 것이다. 또는 `MANAGER` 권한을 검사하는 곳마다 `ADMIN`도 함께 포함시키는 것이다. 컴파일은 되지만, 관리·매니저·사용자 권한 사이의 의미 관계가 코드 전체에 흩어져 보이지 않게 된다.

Spring Security는 이 문제를 `RoleHierarchy`로 깔끔하게 해결한다.

```java
@Bean
static RoleHierarchy roleHierarchy() {
    return RoleHierarchyImpl.withDefaultRolePrefix()
        .role("ADMIN").implies("MANAGER")
        .role("MANAGER").implies("USER")
        .build();
}

@Bean
static GrantedAuthorityDefaults authorityDefaults() {
    return new GrantedAuthorityDefaults("ROLE_");
}
```

한 번 빈으로 등록해두면 `ADMIN`으로 인증된 사용자는 `MANAGER`와 `USER` 권한도 자동으로 가진 것처럼 동작한다. 코드의 모든 `hasRole`, `hasAuthority` 검사에 이 계층이 일관되게 적용된다. 권한 사이의 관계가 한곳에 명문화되어 보이고, 메서드 단위 규칙은 가장 적합한 최소 권한만 적시하면 된다. 깔끔하다.

`withDefaultRolePrefix()`는 `ROLE_` 접두사를 자동으로 붙여주는 빌더다. `role("ADMIN")`이라고만 써도 내부에서는 `ROLE_ADMIN`을 다루고, `implies("MANAGER")`도 같은 방식이다. 만약 `ROLE_` 외의 접두사를 쓰거나 접두사 없이 권한을 다룬다면 `withRolePrefix("")`나 다른 빌더 옵션을 쓸 수 있지만, 표준 관행을 그대로 따르는 편이 협업에서 혼란을 줄인다.

주의할 점이 하나 있다. **Role Hierarchy는 `MethodSecurityExpressionHandler`와 `AuthorizationManager` 양쪽 모두에 주입되어야 일관되게 동작한다.** Spring Boot의 자동 설정이 대부분 해주지만, 커스텀 `MethodSecurityExpressionHandler`를 등록하면서 `setRoleHierarchy(...)`를 빼먹으면 메서드 보안에서만 계층이 동작 안 하는 묘한 상황이 벌어진다. 그러면 URL에서는 계층이 통하는데 메서드에서는 안 통하는, 정말 찜찜한 디버깅 시간을 보내게 된다. 잊지 말자.

## 8.8 `AuthorizationManagerFactory` — 권한 빌더의 중앙 집중

7장에서 MFA를 다룰 때 슬쩍 언급한 `AuthorizationManagerFactory`가 본격적으로 무대에 오를 차례다. 7장에서는 "선택적 MFA를 표현할 때 `AuthorizationManagerFactory.allAuthorities(...)`로 두 factor를 AND로 묶는다"라는 미리보기로 끝났다. 그 빌더가 어디서 왔는지 이제 그림이 잡힌다.

`AuthorizationManagerFactory`는 7.0에서 도입된 팩토리 추상화다. `permitAll()`, `hasRole(...)`, `hasAnyRole(...)`, `hasAuthority(...)`, `allAuthorities(...)`, `anyAuthority(...)` 같은 빌더를 한 곳에서 만들어내고, 그 기본값(접두사, `RoleHierarchy`, `AuthenticationTrustResolver`)을 한 곳에서 커스터마이즈할 수 있다.

```java
@Bean
AuthorizationManagerFactory<Object> authorizationManagerFactory(
        RoleHierarchy roleHierarchy) {
    return AuthorizationManagerFactories.<Object>multiFactor()
        .roleHierarchy(roleHierarchy)
        .build();
}
```

그리고 7장의 MFA 패턴이 자연스럽게 이어진다.

```java
AuthorizationManager<RequestAuthorizationContext> requireMfa =
    authzFactory.allAuthorities("factor.password", "factor.ott");

http.authorizeHttpRequests(a -> a
    .requestMatchers("/sensitive/**").access(requireMfa)
    .anyRequest().authenticated());
```

`allAuthorities`는 7.0 신규 `AllAuthoritiesAuthorizationManager`를 만들어 두 권한을 **AND**로 요구한다. 이게 `hasAnyAuthority`(OR)와 짝을 이루는 새 구현체다. 비밀번호로 인증했고 OTT까지 거친 사용자만 `/sensitive/**`에 접근할 수 있다. 7장의 MFA가 결국 인가의 한 모양이라는 것이 이제 명확해진다.

`AuthorizationManagerFactory`의 진짜 가치는 **모든 권한 검사의 기본 동작을 한 곳에서 통제할 수 있다는 점**이다. 접두사를 `ROLE_` 대신 `AUTH_`로 바꾸고 싶다면? `roleHierarchy`를 빌더에 통합하고 싶다면? 익명 사용자도 일부 권한 검사를 통과시키고 싶다면? 모두 이 팩토리 한 곳에서 끝난다.

## 8.9 거부를 어떻게 표현할 것인가 — `AuthenticationEntryPoint`와 `AccessDeniedHandler`

권한 결정의 절반은 통과시키는 것이고, 나머지 절반은 거부하는 것이다. 그리고 거부하는 방식이 일관되지 않으면 클라이언트는 매우 혼란스러워진다. 어떤 API는 401을 주고, 어떤 API는 302를 주고, 또 어떤 API는 500을 주고 JSON 안에 한국어 에러 메시지가 들어 있는 식이라면, 프론트엔드 개발자는 분기 처리에 점점 화가 난다. 그것도 정말로 화가 난다.

Spring Security가 이 거부를 어떻게 다루는지는 2장에서 한 번 살펴봤다. 여기서 다시 짚고, 8장에서 이를 어떻게 커스터마이즈할지 본다.

### 두 핸들러의 분기점 — `ExceptionTranslationFilter`

`ExceptionTranslationFilter`는 필터 체인의 거의 끝에 자리잡고, 자신보다 뒤쪽 필터에서 던져진 보안 예외를 잡아 일관된 HTTP 응답으로 번역한다. 핵심은 두 가지 예외를 두 가지 핸들러로 보낸다는 점이다.

```
try {
    chain.doFilter(req, res);
} catch (AuthenticationException ae) {
    // "당신이 누군지 모릅니다" 또는 "당신의 인증이 만료됐습니다"
    authenticationEntryPoint.commence(req, res, ae);
} catch (AccessDeniedException ade) {
    if (anonymous(authentication)) {
        // 익명인데 권한 자원에 접근 → 일단 로그인부터
        authenticationEntryPoint.commence(req, res, ade);
    } else {
        // 인증은 됐는데 권한이 없음
        accessDeniedHandler.handle(req, res, ade);
    }
}
```

요약하면 이렇다.

- `AuthenticationEntryPoint` — **인증되지 않은 사용자가 보호된 자원에 접근**할 때 호출된다. 401 응답을 주거나, 로그인 페이지로 리다이렉트한다.
- `AccessDeniedHandler` — **인증된 사용자가 권한이 부족한 자원에 접근**할 때 호출된다. 403 응답을 준다.

두 핸들러는 한 쌍이다. 한쪽만 커스터마이즈하고 다른 쪽을 기본값으로 두면 응답 형태가 들쭉날쭉해진다. 짝지어 함께 다루자.

### REST API를 위한 ProblemDetail 응답

전통적인 폼 로그인 앱이라면 기본 동작이 알맞다. 인증이 필요하면 로그인 페이지로 리다이렉트, 권한이 부족하면 403 페이지를 보여준다. 그러나 REST API라면 사정이 다르다. 클라이언트는 사람이 아니라 SPA의 JavaScript 코드다. HTML 페이지를 받으면 무엇을 해야 할지 모른다.

RFC 7807이 정의한 `ProblemDetail` 표준 형태로 응답하는 편이 깔끔하다.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .exceptionHandling(e -> e
            .authenticationEntryPoint(restAuthenticationEntryPoint())
            .accessDeniedHandler(restAccessDeniedHandler()))
        .build();
}

private AuthenticationEntryPoint restAuthenticationEntryPoint() {
    return (req, res, ex) -> {
        var problem = ProblemDetail.forStatus(HttpStatus.UNAUTHORIZED);
        problem.setTitle("Authentication required");
        problem.setDetail("이 자원에 접근하려면 인증이 필요합니다.");
        problem.setType(URI.create("https://api.example.com/errors/unauthorized"));
        writeProblem(res, problem);
    };
}

private AccessDeniedHandler restAccessDeniedHandler() {
    return (req, res, ex) -> {
        var problem = ProblemDetail.forStatus(HttpStatus.FORBIDDEN);
        problem.setTitle("Access denied");
        problem.setDetail("이 자원에 접근할 권한이 없습니다.");
        problem.setType(URI.create("https://api.example.com/errors/forbidden"));
        writeProblem(res, problem);
    };
}

private void writeProblem(HttpServletResponse res, ProblemDetail problem) throws IOException {
    res.setStatus(problem.getStatus());
    res.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
    new ObjectMapper().writeValue(res.getWriter(), problem);
}
```

응답이 일관된 모양을 갖는다. 클라이언트는 `application/problem+json` 한 가지만 알면 된다. 401과 403의 차이도 명확히 구분된다. 9장에서 다룰 보안 헤더와 짝을 이뤄, "거부 응답이 어떤 메타데이터를 함께 가져야 하는가"라는 더 큰 질문에 답할 수 있다.

### Method Security의 거부 응답 — `MethodAuthorizationDeniedHandler`

3층 메서드 보안이 거부될 때, 즉 `@PreAuthorize`가 실패할 때도 같은 모양의 응답을 주고 싶다면 `MethodAuthorizationDeniedHandler`를 활용한다. 6.3+에서 추가된 기능이다.

```java
@PreAuthorize("hasRole('ADMIN')")
@HandleAuthorizationDenied(handlerClass = AdminOnlyDeniedHandler.class)
public void cancelAll() { ... }
```

`AdminOnlyDeniedHandler`는 `MethodAuthorizationDeniedHandler` 구현체로, 거부됐을 때의 응답이나 대체 반환값을 정의한다. URL 인가의 `AccessDeniedHandler`와 의미적으로 같은 짝이지만, 메서드 단위로 동작한다. `@ControllerAdvice`로 `AccessDeniedException`을 잡는 방법도 있지만, 메서드 보안의 의미를 어노테이션 안에 응축하고 싶다면 `@HandleAuthorizationDenied`가 더 자연스럽다.

`@ControllerAdvice`로 `AccessDeniedException`/`AuthenticationException`을 잡아 통합 처리하는 패턴도 흔히 쓰인다. 그러나 주의해야 한다. **`ExceptionTranslationFilter`가 컨트롤러보다 뒤쪽(바깥쪽)에 있다는 사실을 기억하자.** 컨트롤러에서 던져진 보안 예외는 `@ControllerAdvice`로 잡힐 수 있지만, 컨트롤러까지 도달하지 못한 인가 거부(`AuthorizationFilter`에서 막힌 것)는 `ExceptionTranslationFilter`만 잡을 수 있다. 두 경로를 통합하려면 양쪽 모두 같은 응답 포맷을 쓰도록 맞춰야 한다.

## 8.10 인가와 OWASP A01 — 한눈에 매핑

OWASP Top 10 2021에서 "Broken Access Control"이 1위로 올라왔다는 사실을 처음에 언급했다. 평균 발견율 3.81%. 이제 5층 모델 위에서 이 통계를 다시 읽어보자.

| OWASP A01 결함 유형 | 5층 구조에서의 대응 |
|---------------------|---------------------|
| URL 접근 제어 누락 | 1·2층 — `authorizeHttpRequests` + `anyRequest().authenticated()` |
| HTTP 메서드 우회(`GET`은 막았는데 `POST`는 통과) | 2층 — `requestMatchers(HttpMethod, ...)` |
| 비즈니스 로직 권한 누락 | 3·4층 — `@PreAuthorize`, 메타 어노테이션 |
| IDOR(Insecure Direct Object Reference) | 5층 — `#post.author == authentication.name` 또는 권한 빈 |
| Role 상승 / Vertical privilege escalation | Role Hierarchy + 메타 어노테이션 일관성 |
| 거부 응답 누설 / 누락 | 8.9절 `AccessDeniedHandler` + ProblemDetail |

5층 중 어느 한 층이라도 비어 있으면 그 자리가 곧 A01의 결함이 된다. 1층만으로 막으려 들면 IDOR이 새고, 5층만 짜놓고 1층을 비워두면 URL 통째로 노출된다. **다섯 층은 함께 묶일 때 완전해진다.** OWASP가 보여주는 발견율 3.81%는 그 어느 한 층의 결함이 아니라, 층들 사이의 연결이 끊어진 자리에서 자라난 결과다.

## 8.11 정리 — 권한이 사는 자리를 결정하는 법

다섯 층을 한 그림으로 묶어 다시 보면, 결국 결정은 두 축으로 내려진다. **하나는 결정에 필요한 정보의 위치(URL인가, 메서드 인자인가, 객체 상태인가), 다른 하나는 그 규칙이 얼마나 자주 바뀌는가(인프라처럼 안정적인가, 비즈니스처럼 변하는가)**다.

URL과 HTTP 메서드만으로 결론이 나는 규칙은 위로 올린다. 결정에 객체의 상태가 필요하면 아래로 내린다. 자주 바뀌는 비즈니스 규칙은 자바 코드(권한 빈)로 두어 IDE의 도움을 받는다. 안정적이고 광범위한 규칙은 URL 매처나 메타 어노테이션으로 명문화한다.

기억할 다섯 가지만 추리자.

1. **`@EnableGlobalMethodSecurity`는 즉시 grep해 `@EnableMethodSecurity`로 교체한다.** 소리 없이 깨지는 보안만큼 끔찍한 건 없다.
2. **`hasRole`은 `ROLE_`을 자동으로 붙이고, `hasAuthority`는 안 붙인다.** OAuth2 스코프는 `hasAuthority("SCOPE_...")`로 검사한다.
3. **SpEL이 코드 본문을 가리면 권한 빈으로 추출한다.** `@PreAuthorize("@perm.canEdit(#id)")`가 긴 SpEL보다 낫다.
4. **Role Hierarchy는 한 곳에 명문화하고, `MethodSecurityExpressionHandler`에도 같이 주입한다.** URL과 메서드의 계층이 어긋나면 디버깅이 끔찍해진다.
5. **`AuthenticationEntryPoint`와 `AccessDeniedHandler`는 짝으로 커스터마이즈한다.** API는 ProblemDetail로, 401과 403을 명확히 구분해서.

8장에서 우리는 인증된 사용자에게 "무엇을 허용할지" 결정하는 다섯 층을 둘러봤다. 다음 9장에서는 다른 종류의 문제를 다룬다. **인증·인가가 다 통과한 정상 요청처럼 보이는데, 사실은 다른 사이트에서 위조해 보낸 요청이라면?** CSRF가 던지는 질문이다. 그리고 그것과 한 묶음으로 헷갈리는 CORS, 그리고 헤더 한 줄이 막아주는 위협들까지 — 가장 헷갈리는 셋을 한 챕터에서 풀어보자.

---

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

---

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

---

# 11장. Reactive 보안 — WebFlux에서 다시 그리는 인증·인가

> **선행 필요:** 2장(필터 체인), 3장(컴포넌트 모델), 5장(JWT 자원 서버) 또는 8장(인가 어휘).

WebFlux 프로젝트를 처음 짤 때 가장 먼저 부딪치는 벽 중 하나가 보안이다. 컨트롤러는 `Mono`와 `Flux`로 깔끔하게 흘러가는데, `SecurityConfig`를 열어 익숙한 `HttpSecurity`를 타이핑하기 시작하면 IDE가 빨갛게 운다. `authorizeHttpRequests`도, `SecurityFilterChain`도 보이지 않는다. 익숙한 단어들이 단 한 글자씩 비틀어진 채로 거기 있다.

서블릿 책의 모든 코드가 비슷한 모양으로 옮겨질 듯하지만, `Mono`와 `Flux`가 끼어드는 순간 모서리가 보인다. `Authentication`을 꺼내려고 `SecurityContextHolder.getContext()`를 호출한 코드가 빈 컨텍스트를 돌려준다. `JwtAuthenticationConverter`를 그대로 빈으로 등록했더니 시동도 안 걸린다. 한 줄 한 줄이 잔잔히 어긋난다.

물론 어긋남은 우연이 아니다. WebFlux의 전제는 **스레드 하나가 절대로 멈추지 않는다**는 것이다. 이 약속을 지키기 위해 Spring Security 팀은 인증·인가의 모든 구성요소를 reactive 시그니처로 다시 그렸다. 이름이 비슷한 건 친절함이고, 시그니처가 비틀린 건 약속을 지키기 위한 정직함이다. 이 챕터에서는 그 비틀림의 규칙을 익히고, 서블릿에서 옮길 때 가장 자주 막히는 함정 다섯을 짚는다. 끝에 가서는 한 요청이 `AuthenticationWebFilter`를 통과해 컨트롤러 메서드까지 도달하는 길을 머릿속에 그릴 수 있게 된다.

## 11.1 같은 이름, 다른 시그니처 — 대응 매핑

먼저 어휘를 맞춰두자. 서블릿 책에서 익숙해진 이름들이 WebFlux에서 어떻게 변형되는지 한눈에 보는 것부터다. 표는 단순히 외워야 할 짝이 아니라 "왜 이렇게 갈라졌는가"를 묻는 시작점이다.

| 서블릿 (블로킹) | WebFlux (reactive) | 핵심 차이 |
|---|---|---|
| `HttpSecurity` | `ServerHttpSecurity` | DSL 진입점. 메서드 이름은 비슷하지만 반환 타입이 `Mono`로 묶인다 |
| `SecurityFilterChain` | `SecurityWebFilterChain` | 빈 타입. `WebFilter` 시퀀스를 갖는다 |
| `Filter` | `WebFilter` | 시그니처가 `Mono<Void> filter(ServerWebExchange, WebFilterChain)`로 바뀐다 |
| `AuthenticationManager` | `ReactiveAuthenticationManager` | `authenticate(...)`가 `Mono<Authentication>`을 반환 |
| `AuthenticationProvider` | `ReactiveAuthenticationManager`만 존재 | provider 추상이 사라지고 매니저 자체가 `Mono` 합성으로 위임을 표현 |
| `UserDetailsService` | `ReactiveUserDetailsService` | `findByUsername(...)`이 `Mono<UserDetails>` |
| `JwtDecoder` | `ReactiveJwtDecoder` | 디코드 결과가 `Mono<Jwt>` |
| `SecurityContextRepository` | `ServerSecurityContextRepository` | 저장/로드가 `Mono<Void>` / `Mono<SecurityContext>` |
| `SecurityContextHolder` | `ReactiveSecurityContextHolder` | ThreadLocal이 아니라 **Reactor Context**에서 꺼낸다 |
| `authorizeHttpRequests` | `authorizeExchange` | 매처 이름이 `requestMatchers` → `pathMatchers`로 |
| `@EnableMethodSecurity` | `@EnableReactiveMethodSecurity` | SpEL의 `authentication`이 `Mono`로 흘러감 |
| `HttpFirewall` | (별도 추상 없음) | reactor-netty/Tomcat 단의 검증으로 위임 |

이름이 살짝 다른 이유는 단순한 변덕이 아니다. **블로킹 호출이 가능한 메서드와 절대 블로킹해서는 안 되는 메서드를 컴파일러 수준에서 구별하기 위해서다.** 서블릿용 인터페이스 자리에 그대로 `ReactiveAuthenticationManager`를 두면, 구현체에서 무심코 `userRepository.findByUsername(...)`(JPA 동기 메서드)을 호출해도 컴파일이 통과한다. 새 이름은 "여기는 reactive 세계다. 들어올 때 신발을 갈아 신어라"라는 표시다.

기억해두자. 두 세계의 클래스를 같은 빈 컨테이너에 같이 등록하는 것은 가능하다. 그러나 한 `WebFilter` 안에서 블로킹 `JwtDecoder`를 호출하는 것은 가능해도 권장되지 않는다. 같은 단어, 다른 약속이라는 점을 잊지 말자.

### 11.1.1 가장 짧은 설정

본격적인 설명에 들어가기 전에, 우선 가장 짧은 설정 하나를 살펴보자. 서블릿의 `SecurityFilterChain`을 빈으로 등록하던 그 패턴 그대로다.

```java
@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(ex -> ex
                .pathMatchers("/actuator/health").permitAll()
                .anyExchange().authenticated())
            .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
            .csrf(ServerHttpSecurity.CsrfSpec::disable)
            .build();
    }
}
```

서블릿 코드와 거의 같은 모양이다. `@EnableWebFluxSecurity`, `ServerHttpSecurity`, `SecurityWebFilterChain` — 이 세 단어만 바꿔 끼웠다. 그런데 이 한 빈이 시동되는 순간, Spring Security는 내부적으로 무려 10개 가까운 `WebFilter`를 묶어 하나의 `SecurityWebFilterChain`을 구성한다. 그 안에서 무슨 일이 일어나는지 다음 절에서 한 발 들어가 보자.

## 11.2 진입점 셋 — `AuthenticationWebFilter`, `ReactiveAuthenticationManager`, `ServerSecurityContextRepository`

서블릿에서 인증의 주연은 셋이었다. 인증 필터(`UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter` 등), `AuthenticationManager`, `SecurityContextRepository`. WebFlux도 똑같이 셋이다. 이름과 시그니처만 비틀려 있다.

```text
ServerWebExchange
        │
        ▼
┌───────────────────────────────┐
│  AuthenticationWebFilter      │
│  ─ ServerAuthenticationConverter (요청 → 토큰)
│  ─ ReactiveAuthenticationManager (토큰 → 인증된 Authentication)
│  ─ ServerAuthenticationSuccessHandler / FailureHandler
│  ─ ServerSecurityContextRepository (저장)
└───────────────────────────────┘
        │  (Reactor Context에 SecurityContext 주입)
        ▼
   AuthorizationWebFilter / 컨트롤러
```

흐름의 순서는 서블릿과 동일하다. 다만 모든 화살표 위에 `Mono`가 얹혀 있다고 보면 된다.

### 11.2.1 `AuthenticationWebFilter`

`AuthenticationWebFilter`는 서블릿의 `AbstractAuthenticationProcessingFilter`에 해당하는 추상화다. 그러나 추상 클래스를 상속하는 게 아니라, **변환기와 매니저를 조립**해 만든다.

```java
ReactiveAuthenticationManager manager = ...;
ServerAuthenticationConverter converter = ...;

AuthenticationWebFilter filter = new AuthenticationWebFilter(manager);
filter.setServerAuthenticationConverter(converter);
filter.setRequiresAuthenticationMatcher(
    ServerWebExchangeMatchers.pathMatchers(HttpMethod.POST, "/api/login"));
filter.setSecurityContextRepository(new WebSessionServerSecurityContextRepository());
```

서블릿에서 `UsernamePasswordAuthenticationFilter`를 상속하던 코드가, 여기서는 인스턴스를 조립하는 코드로 바뀌었다. 처음 보면 어색하지만 익숙해지면 오히려 더 명료하다. "어디서 토큰을 만들고, 어디서 인증하고, 어디에 저장할 것인가"를 한 화면에서 선언하기 때문이다.

`ServerAuthenticationConverter`는 `ServerWebExchange`를 받아 `Mono<Authentication>`을 돌려준다. JWT의 `Authorization: Bearer ...` 헤더에서 토큰을 꺼내거나, 폼 파라미터에서 username/password를 추출하는 책임이 여기 산다. 서블릿의 `HttpServletRequest → Authentication` 추출 로직이 이 자리에 그대로 옮겨 온 것이다.

### 11.2.2 `ReactiveAuthenticationManager`

서블릿에서 `AuthenticationManager`의 표준 구현은 `ProviderManager`였다. 여러 `AuthenticationProvider`를 줄 세워 `supports(...)`로 분기시키는 위임 모델이었다. WebFlux에서는 provider 추상이 사라졌다. 대신 `ReactiveAuthenticationManager` 자체를 합성한다.

```java
ReactiveAuthenticationManager passwordManager = new UserDetailsRepositoryReactiveAuthenticationManager(uds);
ReactiveAuthenticationManager jwtManager = new JwtReactiveAuthenticationManager(decoder);

ReactiveAuthenticationManager delegating = new DelegatingReactiveAuthenticationManager(
    passwordManager, jwtManager);
```

`DelegatingReactiveAuthenticationManager`는 첫 번째 매니저가 `Mono.empty()`를 돌려주면 다음 매니저로 넘어간다. provider 모델이 reactive 합성으로 자연스럽게 표현된 모습이다.

> **왜 provider가 사라졌을까?**
> Reactor의 합성 연산자(`Mono.switchIfEmpty`, `flatMap`)가 provider 패턴이 하던 일을 더 작은 추상으로 표현할 수 있기 때문이다. provider라는 별도의 인터페이스를 두지 않아도 매니저 자체로 위임을 표현할 수 있다. 작아진 추상이 더 깊은 자유를 준다.

### 11.2.3 `ServerSecurityContextRepository`

서블릿에서 세션에 `SecurityContext`를 저장하던 자리는 `HttpSessionSecurityContextRepository`였다. WebFlux의 대응자는 `WebSessionServerSecurityContextRepository`다. 이름이 길지만 하는 일은 같다 — `SecurityContext`를 어디에 둘 것인가.

```java
public interface ServerSecurityContextRepository {
    Mono<Void> save(ServerWebExchange exchange, SecurityContext context);
    Mono<SecurityContext> load(ServerWebExchange exchange);
}
```

기본은 `WebSession`(서블릿 세션의 reactive 버전)에 저장하는 구현이다. 자원 서버처럼 stateless로 운영하고 싶다면 `NoOpServerSecurityContextRepository.getInstance()`를 끼우면 된다. JWT 자원 서버 설정에서 별 신경 안 써도 stateless로 동작하는 이유가 이 빈이 자동으로 No-Op으로 채워지기 때문이다.

다시 흐름을 그려보자. 한 요청이 들어오면 `AuthenticationWebFilter`가 매처에 걸려 변환기로 `Authentication`을 만들고, 매니저로 인증을 마치고, 결과를 저장소에 저장한다. 이 모든 단계가 `Mono` 체인으로 이어진다. 한 단계도 블로킹을 허용하지 않는다.

## 11.3 블로킹 API 금지 — `SecurityContextHolder`는 손대지 말자

서블릿에서 그 어느 곳에서나 `SecurityContextHolder.getContext().getAuthentication()`을 호출해 현재 사용자를 꺼냈다. 어디서든 한 줄로 끝났다. 이 한 줄이 WebFlux로 옮기는 사람들의 첫 번째 함정이다.

```java
// 이렇게 쓰면 안 된다 — WebFlux에서는 거의 항상 null
@GetMapping("/me")
public Mono<String> me() {
    Authentication auth = SecurityContextHolder.getContext().getAuthentication();
    return Mono.just(auth.getName());  // NullPointerException
}
```

왜 `null`일까? `SecurityContextHolder`의 기본 전략은 `ThreadLocal`이다. 서블릿 컨테이너는 한 요청이 한 스레드를 점유하므로 `ThreadLocal`이 곧 "현재 요청의 컨텍스트"였다. WebFlux는 다르다. 한 요청이 여러 스레드 사이를 옮겨 다닌다. event loop 스레드에서 시작해 `subscribeOn(...)`이 끼이는 순간 다른 스레드로 점프한다. `ThreadLocal`은 그 점프 사이에서 사라진다.

그래서 reactive 코드에서는 `ThreadLocal` 대신 **Reactor Context**라는 다른 그릇을 쓴다. Reactor가 각 신호(`onNext`, `onError`)와 함께 전달하는 불변 키-값 저장소다. Spring Security는 이 Context의 특정 키에 `SecurityContext`를 담아 둔다. 그걸 꺼내는 API가 `ReactiveSecurityContextHolder`다.

```java
// 권장 — Reactor Context에서 꺼낸다
@GetMapping("/me")
public Mono<String> me() {
    return ReactiveSecurityContextHolder.getContext()
        .map(SecurityContext::getAuthentication)
        .map(Authentication::getName);
}
```

`getContext()`의 반환 타입은 `Mono<SecurityContext>`다. 인증된 사용자가 없으면 `Mono.empty()`다. 즉 이 코드는 "Reactor Context에서 SecurityContext를 꺼내고, 거기서 Authentication을 꺼내고, 그 name을 돌려준다. 컨텍스트가 비어 있으면 빈 응답"으로 읽힌다. 한 단계도 블로킹이 아니다.

물론 컨트롤러 인자로 그냥 받아도 된다. Spring Security가 `Authentication`/`Principal`을 컨트롤러 파라미터로 자동 주입해주기 때문이다.

```java
@GetMapping("/me")
public Mono<String> me(Authentication auth) {
    return Mono.just(auth.getName());
}
```

`@AuthenticationPrincipal`을 쓰는 패턴도 그대로 작동한다. 이 두 방식이 컨트롤러 입장에서는 가장 깔끔하다.

> **잊지 말자.** `SecurityContextHolder.getContext()`는 WebFlux에서 **null이거나 잘못된 사용자의 컨텍스트**를 돌려줄 수 있다. 후자가 더 무섭다. 만약 application 어디선가 `SecurityContextHolder.MODE_INHERITABLETHREADLOCAL`을 설정하고 있다면, event loop 스레드의 ThreadLocal에 직전 요청의 컨텍스트가 남아 다음 요청에 그대로 새어 나갈 수 있다. **다른 사용자의 권한이 다른 사용자에게 적용되는 사고**가 여기서 난다. 한 번 일어나면 디버깅하기 끔찍한 일이다.

### 11.3.1 차단 함정 모음

WebFlux로 옮기다 블로킹을 무심코 부르는 자리는 의외로 많다. 자주 마주치는 셋을 미리 알아두자.

**(1) JPA Repository를 reactive 매니저 안에서 부른다.** `UserDetailsRepositoryReactiveAuthenticationManager`가 받는 `ReactiveUserDetailsService` 구현체에서 `userRepository.findByUsername(...)`(JPA)을 그대로 호출하면 컴파일은 되지만 event loop이 멈춘다. `Mono.fromCallable(() -> userRepository.findByUsername(name)).subscribeOn(Schedulers.boundedElastic())`처럼 별도 스케줄러로 보내는 것이 차선이다. 제일 좋은 건 R2DBC 같은 reactive 드라이버를 쓰는 것이다.

**(2) `JwtDecoder`(서블릿용)를 `ReactiveJwtDecoder` 자리에 등록한다.** 둘은 다른 인터페이스다. 자원 서버 설정에서 IDE의 자동 임포트가 서블릿용을 가져오면 시동은 되어도 JWT 검증에서 매번 블로킹 HTTP 호출(JWKs 조회)이 일어난다. 시그니처가 다르니 잘 보고 임포트하자.

**(3) `@PreAuthorize`의 SpEL 안에서 동기 서비스를 부른다.** `@PreAuthorize("@authz.canRead(#id)")` 같은 패턴에서 `authz.canRead(...)`가 JPA를 호출한다면, reactive method security 안에서도 블로킹이 일어난다. SpEL은 reactive 식을 평가하지만 그 안에서 부른 메서드까지 reactive로 만들지는 못한다. 이 경우 `Mono<Boolean>`을 돌려주는 메서드로 바꾸자. `@PreAuthorize`는 reactive 반환을 이해한다.

스레드 하나가 멈추는 순간 WebFlux의 전제가 무너진다. 이 문장을 책상 옆 메모에 붙여두자.

## 11.4 WebFlux 자원 서버 — `ReactiveJwtDecoders.fromIssuerLocation`

JWT 자원 서버는 reactive에서도 가장 자주 만들어지는 구성이다. 5장에서 본 서블릿 자원 서버와 시그니처 한 줄만 다르다.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/app
```

이 한 줄이 자동으로 하는 일은 서블릿과 같다. `${issuer-uri}/.well-known/openid-configuration`에 OIDC discovery를 쳐서 JWKs URL을 알아내고, 그걸 캐시한 뒤 `ReactiveJwtDecoder`를 만들어 빈으로 등록한다. 다만 빈 타입이 `JwtDecoder`가 아니라 `ReactiveJwtDecoder`라는 점만 다르다.

수동으로 만들고 싶다면 이렇게 된다.

```java
@Bean
ReactiveJwtDecoder jwtDecoder() {
    return ReactiveJwtDecoders.fromIssuerLocation(
        "https://auth.example.com/realms/app");
}
```

서블릿용은 `JwtDecoders.fromIssuerLocation`, reactive용은 `ReactiveJwtDecoders.fromIssuerLocation`이다. 단어 하나 차이지만 두 메서드가 돌려주는 객체는 전혀 다르다. 앞쪽은 동기 HTTP 클라이언트(RestTemplate)로 JWKs를 조회하고, 뒤쪽은 `WebClient`로 조회한다. event loop 위에서 도는 자원 서버가 첫 요청마다 RestTemplate으로 JWKs를 받느라 멈춰서는 안 되기 때문이다.

### 11.4.1 권한 변환기

토큰의 `scope`/`scp` 클레임을 `SCOPE_*` 권한으로 자동 매핑하는 동작은 reactive도 동일하다. 커스텀 클레임(`roles`, `groups`)을 권한으로 매핑하려면 `JwtAuthenticationConverter`의 reactive 대응자가 필요한데, 이름이 `ReactiveJwtAuthenticationConverterAdapter`로 길어진다.

```java
@Bean
Converter<Jwt, Mono<AbstractAuthenticationToken>> jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter grantedAuthoritiesConverter = new JwtGrantedAuthoritiesConverter();
    grantedAuthoritiesConverter.setAuthorityPrefix("ROLE_");
    grantedAuthoritiesConverter.setAuthoritiesClaimName("roles");

    JwtAuthenticationConverter delegate = new JwtAuthenticationConverter();
    delegate.setJwtGrantedAuthoritiesConverter(grantedAuthoritiesConverter);

    return new ReactiveJwtAuthenticationConverterAdapter(delegate);
}
```

```java
http.oauth2ResourceServer(o -> o.jwt(j -> j
    .jwtAuthenticationConverter(jwtAuthenticationConverter())));
```

서블릿 코드에서 `JwtAuthenticationConverter`를 바로 넘기던 자리에, reactive에서는 `Converter<Jwt, Mono<AbstractAuthenticationToken>>`을 넘긴다. 변환 자체가 비동기일 수 있다는 약속이다. 권한을 별도 DB에서 끌어와야 하는 시나리오라면 이 시그니처가 자연스럽다.

### 11.4.2 Introspection

Opaque 토큰을 쓸 때도 마찬가지다. `OpaqueTokenIntrospector` 대신 `ReactiveOpaqueTokenIntrospector`를 빈으로 등록한다. 매 요청 IdP에 introspection을 쳐야 하므로 캐시(예: Caffeine)는 reactive에서도 필수다.

## 11.5 인가 — `authorizeExchange`

서블릿의 `authorizeHttpRequests`에 해당하는 자리가 `authorizeExchange`다. 매처 이름도 `requestMatchers` → `pathMatchers`로 바뀐다. 그 외는 거의 동일하다.

```java
http.authorizeExchange(ex -> ex
    .pathMatchers("/actuator/health").permitAll()
    .pathMatchers(HttpMethod.GET, "/api/posts/**").permitAll()
    .pathMatchers("/api/admin/**").hasRole("ADMIN")
    .pathMatchers("/api/users/**").hasAnyAuthority("SCOPE_users.read", "SCOPE_users.write")
    .anyExchange().authenticated());
```

서블릿 코드와 거의 같은 모양이다. 그래서 옮기는 일이 가볍게 느껴진다. 그러나 한 가지 다르다 — `RequestMatcher`가 아니라 `ServerWebExchangeMatcher`다. 커스텀 매처를 끼우는 자리에서 시그니처가 살짝 비틀린다.

```java
// 서블릿
RequestMatcher matcher = request -> request.getHeader("X-Tenant") != null;

// WebFlux
ServerWebExchangeMatcher matcher = exchange ->
    Mono.justOrEmpty(exchange.getRequest().getHeaders().getFirst("X-Tenant"))
        .flatMap(t -> MatchResult.match())
        .switchIfEmpty(MatchResult.notMatch());
```

`MatchResult`가 `Mono`로 감싸진 채 흘러간다. reactive의 약속이 매처 한 줄에도 스며들어 있다.

### 11.5.1 `access(...)`로 커스텀 매니저 꽂기

`hasRole`/`hasAuthority`보다 복잡한 인가 결정은 `access(...)`에 `ReactiveAuthorizationManager`를 직접 끼워서 표현한다. 서블릿의 `AuthorizationManager`와 거의 동일하지만 반환이 `Mono<AuthorizationDecision>`이다.

```java
ReactiveAuthorizationManager<AuthorizationContext> tenantMatch = (authMono, ctx) ->
    authMono.map(auth -> {
        String userTenant = (String) ((Jwt) auth.getPrincipal()).getClaims().get("tenant");
        String reqTenant = ctx.getExchange().getRequest().getHeaders().getFirst("X-Tenant");
        return new AuthorizationDecision(Objects.equals(userTenant, reqTenant));
    });

http.authorizeExchange(ex -> ex
    .pathMatchers("/api/tenant/**").access(tenantMatch)
    .anyExchange().authenticated());
```

`authMono`로 받는 부분이 핵심이다. **`Authentication`을 동기로 받지 않는다.** 인가 매니저가 호출되는 시점에 아직 인증이 끝나지 않았을 수 있고, 인증이 reactive 합성에서 늦게 도착할 수 있기 때문이다. Reactive로 받는 게 정직한 약속이다.

## 11.6 Reactive Method Security

URL 인가만으로는 좁다. 도메인 로직 안에서 인가를 표현하고 싶을 때 `@PreAuthorize`를 쓰는 자리, WebFlux에서는 `@EnableReactiveMethodSecurity`가 그 자리를 받는다.

```java
@Configuration
@EnableWebFluxSecurity
@EnableReactiveMethodSecurity
public class SecurityConfig {
    // ...
}
```

서블릿의 `@EnableMethodSecurity`와 어노테이션 이름만 다르다. 서비스 코드의 `@PreAuthorize`/`@PostAuthorize`는 그대로 동작한다 — 단, **반환 타입이 `Mono`/`Flux`인 메서드만**.

```java
public interface PostService {

    @PreAuthorize("hasAuthority('SCOPE_posts.read')")
    Mono<Post> findById(String id);

    @PostAuthorize("returnObject.author == authentication.name")
    Mono<Post> findByIdEnforceOwner(String id);

    @PreAuthorize("@authz.canEdit(#id, authentication)")
    Mono<Void> update(String id, PostUpdate cmd);
}
```

세 가지 짚어야 한다.

**첫째, SpEL 안의 `authentication`/`principal`은 `Mono`로 흘러간다.** 위 예제의 두 번째 `@PostAuthorize`에서 `authentication.name`은 표면적으로는 동기 접근처럼 보이지만, Spring Security가 식을 평가하기 전에 `Mono<Authentication>`을 unwrap한 뒤 평가한다. 사용자가 SpEL을 동기처럼 쓰게 해주려는 배려다.

**둘째, 외부 빈을 부르는 `@authz.canEdit(...)` 같은 패턴은 반환 타입에 주의해야 한다.** `canEdit`이 `boolean`(동기)을 돌려준다면 그 안에서 절대 블로킹 호출을 하면 안 된다. DB 조회가 필요하면 시그니처를 `Mono<Boolean>`으로 바꾸자. reactive method security는 SpEL이 `Mono<Boolean>`을 돌려주면 그 결과를 기다린다.

**셋째, 반환 타입이 `Mono`/`Flux`가 아닌 메서드에 `@PreAuthorize`를 붙이면 무력하다.** 정확히는 reactive 모드에서는 동작이 일관되지 않을 수 있다. 서비스 메서드 시그니처가 reactive로 통일되어 있어야 인가 어노테이션이 일관되게 적용된다. 한 클래스 안에 `String findName()`(동기)과 `Mono<Post> findById(...)`(reactive)가 섞여 있으면 끔찍한 일이 된다. 한 가지로 통일하자.

> **권장:** WebFlux 프로젝트의 서비스 레이어는 가능한 한 모든 public 메서드가 `Mono`/`Flux`를 돌려주도록 통일하는 것이 좋다. method security가 일관되게 동작할 뿐 아니라, 컨트롤러까지의 흐름에서 블로킹이 끼어들 자리가 사라진다.

## 11.7 7.0 신규 — `AllAuthoritiesReactiveAuthorizationManager`

서블릿 8장에서 살펴본 `AllAuthoritiesAuthorizationManager`(AND 의미)의 reactive 짝이 7.0에서 추가됐다. 이름이 길지만 하는 일은 단순하다. **모든 권한을 동시에 갖고 있어야 통과**시키는 매니저다.

서블릿의 `hasAnyAuthority(...)`는 OR다. 하나만 있어도 통과다. 그런데 MFA처럼 "패스워드도 통과해야 하고 OTT도 통과해야 한다"는 상황은 AND가 필요하다. 6.x까지는 이걸 표현하려면 SpEL에서 `hasAuthority('A') and hasAuthority('B')`를 직접 써야 했다. 7.0의 `AllAuthorities...` 매니저가 이 패턴을 정식 매니저로 들어 올렸다.

```java
ReactiveAuthorizationManager<AuthorizationContext> mfa =
    AllAuthoritiesReactiveAuthorizationManager.hasAllAuthorities(
        "FACTOR_PASSWORD", "FACTOR_OTT");

http.authorizeExchange(ex -> ex
    .pathMatchers("/api/funds/transfer").access(mfa)
    .anyExchange().authenticated());
```

이 매니저가 의미 있는 자리는 7장에서 본 `@EnableMultiFactorAuthentication`이 만들어내는 권한 모델이다. 패스워드 인증 성공 시 `FACTOR_PASSWORD`, OTT 인증 성공 시 `FACTOR_OTT`가 누적된다. 송금처럼 두 factor 모두 요구하는 엔드포인트에서 이 매니저가 짧고 명료한 표현을 준다.

`hasAnyAuthority` 대신 `hasAllAuthorities`라는 표현이 WebFlux의 매처 DSL 안에서 깔끔하게 자리 잡지 못하는 점은 작은 아쉬움이다. 그래서 `access(...)`에 매니저를 직접 끼우는 패턴이 권장된다. 7장 MFA를 reactive로 옮길 일이 있다면 이 매니저를 잊지 말자.

## 11.8 컨텍스트 전파 — Reactor Context와 `contextWrite`

reactive에서 `SecurityContext`가 어떻게 흘러가는지를 한 번 분명히 짚자. 서블릿에서는 `ThreadLocal`이 그릇이었다. WebFlux에서는 **Reactor Context**가 그릇이다.

Reactor Context는 신호(`onNext`, `onError`)와 함께 위에서 아래로 흐르는 불변 키-값 저장소다. 그러나 흐름의 방향이 자주 헷갈린다. **신호는 downstream(아래)으로 흐르지만, Context는 마지막 `subscribe` 시점에서 거꾸로 upstream(위)로 전파된다.** 즉 어디선가 `subscribe`할 때 Context에 값을 넣어야 그 아래(체인 위쪽)의 연산자들이 그 값을 본다.

Spring Security는 이 메커니즘을 활용해 인증된 `SecurityContext`를 Reactor Context의 특정 키에 담아 둔다. 그 키를 꺼내는 표준 API가 `ReactiveSecurityContextHolder`다. 즉 `ReactiveSecurityContextHolder.getContext()`는 Reactor Context에서 키 하나를 꺼내는 한 줄에 불과하다. 마법이 아니다.

### 11.8.1 테스트나 비동기 호출에서 컨텍스트 주입하기

운영 코드에서는 `AuthenticationWebFilter`가 알아서 Context에 `SecurityContext`를 심어준다. 그러나 테스트나 단위 메서드 호출에서는 직접 주입해야 한다.

```java
SecurityContext ctx = new SecurityContextImpl(
    new TestingAuthenticationToken("alice", null, "ROLE_USER"));

Mono<String> mono = service.currentUserName()
    .contextWrite(ReactiveSecurityContextHolder.withSecurityContext(Mono.just(ctx)));

StepVerifier.create(mono).expectNext("alice").verifyComplete();
```

`contextWrite(...)`는 Reactor의 표준 연산자다. 그 안에 `ReactiveSecurityContextHolder.withSecurityContext(...)`가 만든 Context 수정자를 넣어 주면 된다. 12장에서 `WebTestClient.mutateWith(mockUser(...))`가 결국 하는 일도 같은 메커니즘이다.

### 11.8.2 `SecurityContextServerWebExchange`로 보강

가끔 `WebFilter`의 downstream에 `ServerWebExchange`를 통해 `SecurityContext`를 넘기고 싶을 때가 있다. 이때 쓰는 패턴이 `SecurityContextServerWebExchange`다. 평소 직접 마주칠 일은 적지만, 커스텀 `WebFilter`를 짤 때 한 번쯤 마주친다는 것만 알아두면 된다.

```java
SecurityContext ctx = ...;
ServerWebExchange decorated = new SecurityContextServerWebExchange(exchange, Mono.just(ctx));
return chain.filter(decorated);
```

핵심은 변하지 않는다. Context는 위에서 아래로, 또 거꾸로 흐르는 그릇이고, Spring Security는 그 그릇의 특정 자리에 `SecurityContext`를 둔다는 점이다.

## 11.9 서블릿에서 옮길 때 가장 자주 막히는 다섯

이 챕터의 마지막 절은 실전 체크리스트다. 서블릿 보안 코드를 WebFlux로 옮기다 마주치는 흔한 함정을 다섯 가지로 모았다. 어느 하나라도 익숙하다면, 그 자리에서 잠시 멈추고 본 챕터의 해당 절을 다시 펴 보자.

### 함정 1. 블로킹 호출을 reactive 매니저에 끼웠다

가장 자주 일어난다. `ReactiveUserDetailsService` 구현체 안에서 JPA `userRepository.findByUsername(...)`을 부르거나, `ReactiveAuthenticationManager` 안에서 동기 HTTP 클라이언트로 외부 API를 친다. 컴파일은 통과한다. 런타임에 `BlockHound`(개발 환경에서 블로킹을 탐지하는 라이브러리)가 잡아주지 않는 한 조용히 event loop을 멈춘다.

**증상.** 트래픽이 늘면 응답 시간이 비선형으로 폭증한다. 스레드 덤프를 떠 보면 reactor-http-nio-* 스레드들이 JDBC 호출에서 박혀 있다.

**해법.** R2DBC 같은 reactive 드라이버로 옮기는 게 가장 깔끔하다. 옮길 수 없는 자원이라면 `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())`으로 별도 풀로 보내자. 그러나 이건 차선이다.

### 함정 2. suspending 함수와 `Mono`를 섞었다

Kotlin 프로젝트에서 자주 만난다. Spring Security 자체는 `Mono`/`Flux` 시그니처지만, 컨트롤러를 `suspend fun`으로 쓰는 팀이 있다. 두 세계는 spring-web의 어댑터로 잘 이어지지만, 보안의 SpEL이 `Mono<Boolean>`을 기대하는 자리에 `suspend fun`을 그대로 넘기면 어색해진다.

**해법.** `@PreAuthorize` 안에서 부르는 빈 메서드는 `Mono<Boolean>`을 돌려주는 자바 메서드로 두는 편이 낫다. Kotlin이라면 `mono { ... }` 빌더로 감싸자. 어댑터를 한 번만 거치면 그 다음은 평화롭다.

### 함정 3. Reactor Context가 끊겼다

`Schedulers.parallel()`이나 외부 라이브러리의 자체 스케줄러로 작업을 넘기는 순간, Reactor Context가 그쪽으로 따라가지 못하는 경우가 있다. 정확히는 Reactor의 표준 연산자는 Context를 잘 전파하지만, 일부 외부 라이브러리는 `Mono.subscribe()`만 호출하고 Context 인자를 빠뜨린다.

**증상.** 분명히 인증된 요청인데 `ReactiveSecurityContextHolder.getContext()`가 `Mono.empty()`를 돌려준다.

**해법.** Reactor 표준 연산자(`flatMap`, `subscribeOn`, `publishOn`)만 쓰는 한 Context는 끊기지 않는다. 외부 라이브러리를 거친다면 그 직후에 `contextWrite(...)`로 컨텍스트를 다시 심어줘야 한다.

### 함정 4. 에러 핸들러 시그니처가 다르다

서블릿의 `AuthenticationEntryPoint`/`AccessDeniedHandler`를 그대로 등록하면 어색하다. WebFlux는 대응 타입이 `ServerAuthenticationEntryPoint`/`ServerAccessDeniedHandler`다. 이름이 짧아 보이지만 한 글자 빼먹으면 IDE는 빨갛게 운다.

```java
http.exceptionHandling(e -> e
    .authenticationEntryPoint((exchange, ex) -> {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        return exchange.getResponse().writeWith(Mono.just(
            exchange.getResponse().bufferFactory().wrap(
                "{\"error\":\"unauthenticated\"}".getBytes())));
    }));
```

ProblemDetail(8장에서 본 그 모델)을 reactive에서 그대로 쓰고 싶다면 `ProblemDetail` 객체를 JSON으로 직렬화해 `writeWith`에 넘기면 된다. 자세한 패턴은 8장의 거부 표현 절을 참조하자.

### 함정 5. 테스트 패턴이 다르다

서블릿 책에서 익숙해진 `@WithMockUser` + `MockMvc` 조합이 reactive에서는 `WebTestClient` + `mutateWith(SecurityMockServerConfigurers.mockUser(...))`로 바뀐다. 어노테이션도 일부는 그대로 쓰이지만, `SecurityMockMvcRequestPostProcessors`의 `csrf()`/`user()`/`jwt()` 자리는 `SecurityMockServerConfigurers`의 대응자로 갈아탄다.

```java
webTestClient
    .mutateWith(SecurityMockServerConfigurers.mockUser("alice").roles("ADMIN"))
    .mutateWith(SecurityMockServerConfigurers.csrf())
    .post().uri("/api/admin/users")
    .exchange().expectStatus().isOk();
```

JWT 자원 서버 mock도 마찬가지로 `SecurityMockServerConfigurers.mockJwt()` 자리가 있다. 자세한 reactive 테스트 패턴은 12장에서 본격적으로 다룬다.

## 11.10 한 그림으로 요약

WebFlux 보안의 한 요청을 한 그림으로 정리하자.

```text
   ServerWebExchange
        │
        │ ① CORS, CSRF, Header 필터들
        ▼
   AuthenticationWebFilter
        │ ② ServerAuthenticationConverter: exchange → Mono<Authentication>
        │ ③ ReactiveAuthenticationManager: Mono<Authentication> → Mono<Authentication>(인증완료)
        │ ④ ServerSecurityContextRepository: Mono<Void> save
        ▼
   (Reactor Context에 SecurityContext 주입)
        │
        ▼
   AuthorizationWebFilter
        │ ⑤ ReactiveAuthorizationManager: AuthorizationContext → Mono<AuthorizationDecision>
        ▼
   컨트롤러 / 서비스 (@PreAuthorize는 reactive method security가 평가)
        │
        ▼
   응답
```

한 단계 한 단계가 `Mono`로 묶여 있다. 어느 한 점에서 블로킹이 끼면 event loop이 멈춘다. 멈추면 WebFlux의 전제가 무너지고, 그 순간 reactive를 쓰는 이유가 사라진다. 외워두자.

## 11.11 핵심 요약

- 서블릿의 보안 추상은 거의 그대로 reactive 짝이 있다. 이름이 비슷한 건 친절함이고, 시그니처가 비틀린 건 약속을 지키기 위한 정직함이다.
- 진입의 삼각형은 `AuthenticationWebFilter` + `ReactiveAuthenticationManager` + `ServerSecurityContextRepository`다. provider 추상은 사라지고 매니저 합성이 그 자리를 대신한다.
- `SecurityContextHolder.getContext()`는 WebFlux에서 위험하다. `ReactiveSecurityContextHolder.getContext()` 또는 컨트롤러 파라미터 주입을 쓰자.
- 자원 서버는 `ReactiveJwtDecoders.fromIssuerLocation`과 `ReactiveJwtAuthenticationConverterAdapter`로 짠다. 인가는 `authorizeExchange`, method security는 `@EnableReactiveMethodSecurity`다.
- 컨텍스트의 그릇은 ThreadLocal이 아니라 Reactor Context다. 테스트와 비동기 호출에서는 `contextWrite(...)`로 직접 심어주자.

## 11.12 다음 챕터에서 답할 것

11장까지 인증·인가·횡단·reactive까지 모든 본문 어휘가 깔렸다. 이제 남은 질문은 단 하나다. **이 모든 결정을 어떻게 회귀 가능한 안전망으로 묶을 것인가.** 12장은 `@WithMockUser`/`SecurityMockMvcRequestPostProcessors`/`oauth2Login()`/`jwt()` mock부터 시작해, 본 챕터의 `WebTestClient` + `mutateWith(mockUser(...))` 패턴을 다시 마주한다. 이 책에서 내린 모든 보안 결정이 다음 챕터에서 한 번씩 시험대에 오른다.

---

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

---

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

---

# 14장. Zero Trust·BFF·운영의 모서리 — 트렌드와 표준

> **선행 필요:** 1장(멘탈 모델), 5장(JWT/DPoP), 6장(OAuth2 Client), 8장(인가), 9·10장(횡단)

한 권의 책을 거의 다 읽었다. `SecurityFilterChain`이 어떻게 짜이는지 알게 됐고, `AuthorizationManager`가 무슨 일을 하는지도 손에 잡힌다. JWT 자원 서버를 직접 세워 봤고, DPoP로 sender-constrained 토큰까지 다뤘다. Passkeys 등록 ceremony도, OTT 매직 링크도, MFA factor를 권한으로 표현하는 모델도 모두 지나왔다. 인가의 다섯 층을 가르며 SpEL 함정도 짚었고, CSRF·CORS·헤더가 왜 헷갈리는지도 풀었다. Reactive 보안과 테스팅 안전망까지 깔렸고, 마이그레이션 함정 5건을 13장에서 정리했다.

그런데, 잠깐 한 발 물러서 보자. 우리가 만든 이 시스템은 **어떤 시대의 어디에 서 있는가?**

이 질문은 한가한 질문이 아니다. 운영을 한 해 이상 해 본 사람이라면 누구나 안다. 표준은 끊임없이 갱신되고, 어제의 모범이 오늘의 안티 패턴이 된다. 2018년에 "API는 JWT, 웹은 세션"이라는 단순 이분법이 흔한 답이었지만, 지금은 BFF(Backend-for-Frontend) 패턴이 그 자리를 빠르게 채우고 있다. 그 사이에 NIST는 SP 800-207로 "Zero Trust"를 표준 문서화했고, OAuth 2.0은 RFC 9700으로 BCP를 갱신했고, JWT는 RFC 8725로 사용 모범이 정리됐다. 우리가 한 번 만든 코드가 그 흐름과 호흡을 같이하지 않으면, 일 년 뒤에 다시 모든 결정을 검토해야 한다.

이번 장은 그 호흡 맞추기다. 신기능 자랑이 아니라, 우리가 14장 이전까지 짜 둔 모든 코드가 **현재 표준의 어느 좌표에 정확히 얹히는지** 그려 보자는 이야기다. 그리고 그 좌표 옆에 있는 운영의 모서리들 — Secret 회전, Actuator 노출, 감사 로그 — 을 차근차근 짚는다. 마지막엔 책 전체에서 미뤄 둔 논쟁점들을 한자리에 모아 정리한다. JWT vs 세션, localStorage vs Cookie, 자체 IdP vs 외부 IdP. 답은 하나가 아닐 것이다. 그러나 답을 못 정해서가 아니라, 답이 시스템 맥락에 따라 갈리기 때문이라는 것을, 이 장이 끝날 때쯤 함께 보게 될 것이다.

한 가지 미리 약속해 두자. **Zero Trust는 "원칙"이지 "제품"이 아니다.** 어떤 벤더가 "우리 솔루션이 Zero Trust"라고 광고한다면, 그건 정확하지 않은 표현이다. NIST SP 800-207은 일곱 가지 원칙을 제시할 뿐, 한 줄의 코드도, 한 가지의 제품도 권하지 않는다. 우리가 할 일은 그 원칙들을 우리 손에 익은 Spring Security 부품 위에 하나씩 얹어 보는 것이다. 그리고 빈자리가 어디인지 정확히 찾아내는 것이다.

## 14.1 NIST SP 800-207 Zero Trust 7 tenets — Spring Security와 정면으로 맞대 보자

먼저 Zero Trust부터 짚어 보자. NIST가 2020년에 SP 800-207을 최종 확정했고, 그 안에 일곱 가지 원칙(tenets)이 박혀 있다. 보안 업계가 이 문서를 표준 문서로 받아들였기 때문에, "Zero Trust"라는 단어를 진지하게 쓰는 사람은 누구든 이 일곱 원칙을 참조점으로 삼는다. 그러니 우리도 한 번은 정면으로 봐야 한다. 그리고 더 중요한 건, 우리가 이 책에서 짜 온 코드가 일곱 원칙 각각에 어떻게 닿는지 손가락으로 짚어 보는 것이다.

원칙은 이렇다.

> **NIST SP 800-207 7 tenets** ([NIST 원문](https://csrc.nist.gov/pubs/sp/800/207/final))
>
> 1. 모든 데이터 소스·서비스를 리소스로 본다.
> 2. 모든 통신은 네트워크 위치와 무관하게 보호된다.
> 3. 리소스 접근은 **세션 단위**로 부여된다.
> 4. 접근은 **동적 정책**(주체·디바이스 신원·자산 상태·행동 속성)에 따라 결정된다.
> 5. 자산의 보안 자세를 지속 모니터링한다.
> 6. 인증·인가는 **접근 전에 동적이고 엄격하게** 강제된다.
> 7. 조직은 자산·네트워크·통신의 현재 상태에 대해 최대한 많은 정보를 수집한다.

읽기에 추상적이다. 한 줄씩 우리 코드 어휘로 옮겨 보자.

**원칙 1 — 모든 데이터 소스·서비스를 리소스로 본다.** 이 한 줄이 사실 가장 깊다. 옛날 네트워크 보안 모델은 "내부망은 안전, 외부망은 위험"이라는 경계를 그었다. 회사 VPN 안에 들어오면 모든 내부 API가 자동으로 신뢰됐다. 지금은 그게 통하지 않는다. 사내 API라도 인증을 요구해야 하고, 마이크로서비스 간 호출도 토큰을 들고 다녀야 한다. Spring Security에서 보면 어떤가? 2장에서 짠 `SecurityFilterChain`이 모든 `HttpServletRequest`를 똑같이 필터에 태운다. `/internal/health`라고 해서 자동 허용되지 않는다. `permitAll()`은 우리가 명시적으로 허용하지 않는 한 절대 켜지지 않는다. 7.0의 기본 정책이 "인증된 요청 외엔 거부"인 이유가 이것이다. 원칙 1이 코드 정책으로 박혀 있는 셈이다.

**원칙 2 — 모든 통신은 네트워크 위치와 무관하게 보호된다.** TLS다. HTTPS다. 그것도 외부 통신만이 아니라 서비스 간 통신까지. 9장에서 다뤘던 HSTS와 `X-Forwarded-Proto` 처리가 여기에 닿는다. Spring Security가 HTTPS를 직접 강제하지는 않지만, `requiresChannel(c -> c.anyRequest().requiresSecure())` 한 줄로 HTTP 요청을 HTTPS로 리다이렉트할 수 있다. 더 깊게 가면 서비스 메시(Istio·Linkerd) 영역으로 넘어가는데, 그건 본 책 범위 밖이다. 다만 좌표만 박아 두자 — Zero Trust가 말하는 "통신 보호"는 클라이언트-서버 한 단만이 아니라 백엔드 내부의 모든 hop까지 포함한다.

**원칙 3 — 리소스 접근은 세션 단위로 부여된다.** 여기가 흥미롭다. 한 번 로그인했다고 모든 자원에 무제한 접근을 주지 말라는 이야기다. "세션 단위"라는 게 우리가 흔히 쓰는 HTTP 세션 쿠키만 의미하는 게 아니다. NIST 문서 맥락에서 "session"은 "특정 자원에 대한 특정 시점의 접근 권한"에 가깝다. 즉, 같은 사용자라도 자원이 바뀌면 권한을 다시 평가해야 한다는 뜻이다. 우리 코드에서 이걸 가장 잘 구현한 자리가 바로 7장에서 다룬 MFA다. `factor.type=password`로 인증한 사용자가 `/admin/users` 자원에 접근하려는데, 그 자원이 `FACTOR_OTT`를 요구한다면 다시 OTT factor를 받아야 한다. 같은 세션 안에서도 자원에 따라 권한이 다르게 평가되는 것. 이게 원칙 3의 코드적 구현이다. `@EnableMultiFactorAuthentication`이 Zero Trust 원칙 3과 정확히 닿는다는 사실은 한 번 음미해 볼 가치가 있다.

**원칙 4 — 접근은 동적 정책에 따라 결정된다.** 이 원칙이 우리 책 5장과 가장 강하게 연결된다. "동적 정책"이라는 게 무슨 뜻인가? 주체의 신원만이 아니라, 디바이스의 상태, 자산의 위험도, 행동 패턴까지 종합해 매번 결정한다는 이야기다. 우리가 5장 후반에 다룬 **DPoP (RFC 9449)** 가 정확히 여기에 들어맞는다. Bearer 토큰이 단순히 "이 토큰을 들고 있는 자에게 접근 허용"이라면, DPoP는 "이 토큰 + 이 클라이언트 키 쌍을 함께 증명할 수 있는 자에게만 접근 허용"이다. 토큰을 누가 탈취해도 클라이언트 개인키 없이는 못 쓴다. 매 요청마다 `DPoP` 헤더(`htm`·`htu`·`iat`·`jti`·`ath`)를 검증해, 정적인 "토큰 소유"가 아니라 동적인 "키 소유 증명"으로 접근을 결정한다. mTLS도 비슷한 자리에 들어간다 — 클라이언트 인증서로 매 요청 신원을 동적 평가하는 방식이다. 둘 다 sender-constrained 토큰 패밀리에 속한다. 5장 5.9절에서 다뤘던 `cnf.jkt` JWK thumbprint 검증의 정확한 정당화가 여기에 있다 — Zero Trust 원칙 4가 코드로 박힌 형태가 DPoP다.

**원칙 5 — 자산의 보안 자세를 지속 모니터링한다.** 운영 영역이다. 14.5절의 관측·감사에서 본격적으로 다룬다. 짧게 좌표만 박자면, `AuthenticationSuccessEvent`/`AuthenticationFailureEvent`를 수집해 brute-force 탐지를 구성하는 것, JWK 회전 로그를 남기는 것, Actuator의 `health` endpoint를 모니터링 시스템에 연결하는 것이 모두 이 원칙의 코드적 구현이다.

**원칙 6 — 인증·인가는 접근 전에 동적이고 엄격하게 강제된다.** 이 원칙이 사실 우리 책 2~3장의 정확한 정당화다. `AuthorizationFilter`가 자원 핸들러보다 앞에 위치해 매 요청 권한을 평가한다는 점, `STATELESS` 세션 정책의 자원 서버가 매 요청마다 JWT 서명·발급자·만료를 검증한다는 점, `@PreAuthorize`가 메서드 호출 전에 SpEL을 평가한다는 점. 이 모든 게 "접근 전에 강제"의 구현이다. Spring Security의 필터 체인 구조 자체가 원칙 6을 보장하는 아키텍처다.

**원칙 7 — 조직은 자산·네트워크·통신 상태 정보를 최대한 많이 수집한다.** 다시 운영 영역이다. 감사 로그, 메트릭, 트레이싱. Spring Boot 4의 Actuator + Micrometer + OpenTelemetry 묶음이 이 원칙의 도구 셋이다.

이렇게 일곱 원칙을 우리 코드와 맞대 보면 한 가지가 또렷해진다. Spring Security 7로 평범하게 자원 서버 + OAuth2 Client + MFA를 구성하는 행위 자체가 이미 Zero Trust 일곱 원칙의 절반 이상을 자연스럽게 만족시킨다. 우리는 "Zero Trust 도입"이라는 거창한 프로젝트를 별도로 띄울 필요가 없다. 부족한 모서리만 채우면 된다. 그게 어느 모서리인지 정확히 가리는 게 이번 장의 목표다.

> **박스 — Zero Trust 7 tenets ↔ Spring Security 7 매핑**
>
> | 원칙 | 대응 Spring Security 부품 | 본 책 챕터 |
> |------|---------------------------|-----------|
> | 1. 모든 자원에 인증 | 필터 체인 기본 정책, `anyRequest().authenticated()` | 2장, 8장 |
> | 2. 위치 무관 통신 보호 | `requiresChannel`, HSTS, `X-Forwarded-Proto` | 9장 |
> | 3. 세션 단위 권한 | MFA factor, `@EnableMultiFactorAuthentication` | 7장 |
> | 4. 동적 정책 | DPoP(`cnf.jkt`), mTLS, `JwtAuthenticationConverter` 동적 권한 매핑 | 5장 |
> | 5. 지속 모니터링 | `AuthenticationEvent`, Actuator metrics | 14.5절 |
> | 6. 접근 전 강제 | `AuthorizationFilter`, `@PreAuthorize`, STATELESS 자원 서버 | 2장, 5장, 8장 |
> | 7. 정보 수집 | 감사 로그, Micrometer, OpenTelemetry | 14.5절 |

이 표가 14장의 척추다. 14.2 이후의 절들은 이 표의 빈자리(주로 5·7번 원칙)를 채우는 이야기로 흐른다.

### 14.1.1 DPoP가 원칙 4에 정확히 들어맞는 이유 (5장 cross-ref)

원칙 4 — "접근은 동적 정책에 따라 결정된다" — 를 한 단락 더 깊이 보고 가자. 5장에서 DPoP를 다룰 때는 "Bearer 토큰의 한계를 넘는 진화"라는 표현을 썼다. 그 표현을 Zero Trust 어휘로 다시 풀어 보면 이렇다. Bearer 토큰은 정적이다. 토큰 한 줄을 들고 있으면 누구나 쓸 수 있다는 게 "Bearer"의 정의다. 그런데 원칙 4가 요구하는 것은 동적 평가다. "지금 이 요청을 보내는 자가 이 토큰의 정당한 소유자인가?"를 매번 묻는 것. DPoP는 이 질문에 답한다. 매 요청마다 클라이언트가 자신의 개인키로 서명한 `DPoP` JWT 헤더를 함께 보내고, 자원 서버는 그 서명이 토큰의 `cnf.jkt`에 박힌 공개키와 일치하는지 검증한다. 토큰 + 키 쌍이 함께 증명되어야 자원 접근이 허용된다.

이 한 동작이 Zero Trust 원칙 4의 가장 작고 명확한 구현 사례다. "동적 정책"이라는 추상적 표현이 코드 두 줄(`OAuth2ResourceServerConfigurer.jwt(...)` + `DPoP` 검증) 안에 박힌다. 다만 한 가지 짚고 가자 — DPoP가 Zero Trust의 전부는 아니다. 디바이스 신원, 자산 상태, 행동 속성까지 종합 평가하는 본격 Zero Trust 정책 엔진(Open Policy Agent 같은 외부 시스템)을 도입하는 게 다음 단계다. 우리 책 범위는 거기까지 가지 않는다. 그러나 DPoP라는 한 발자국으로 우리가 이미 그 길의 입구에 서 있다는 사실은 분명하다.

## 14.2 BFF (Backend-for-Frontend) — SPA + OAuth2의 새 표준

자, 두 번째 큰 트렌드로 넘어가자. BFF다. 이름이 좀 추상적이라 처음 들으면 갸우뚱하게 되는데, 한 줄로 정리하면 이렇다.

> **BFF = 브라우저(SPA)와 외부 API/IdP 사이에 서서, 브라우저 대신 OAuth 클라이언트 역할을 해 주는 작은 백엔드.**

왜 이런 게 필요한가? 이 질문에 답하려면 우리가 5장과 6장에서 마주쳤던 두 가지 불편한 사실을 다시 떠올려야 한다.

첫째, **브라우저는 OAuth 클라이언트가 되기에 적합하지 않다.** 자바스크립트 코드는 모두 평문으로 노출되니까 client secret을 숨길 곳이 없다. PKCE가 그 빈자리를 메우긴 했지만, 그래도 토큰을 어디에 보관할지가 남는다. `localStorage`? XSS 한 번이면 끝이다 — 5장 7.2절 함정 7에서 본 그대로. `sessionStorage`도 마찬가지. 메모리에 보관? 페이지 리프레시 한 번에 사라진다. HttpOnly 쿠키? 도메인 분리된 SPA에선 전달이 까다롭다. 어느 쪽을 잡아도 한 번씩은 난감해진다.

둘째, **CSRF 보호가 어색해진다.** SPA가 직접 OAuth 클라이언트면 stateful 세션이 없으니까 CSRF 토큰을 발급할 자리가 없다. 결국 "API 호출이니까 CSRF disable"로 가게 되는데, 그러면 9장에서 다룬 stateful 흐름의 보호망이 사라진다.

이 두 가지 불편함을 한 방에 해결하는 패턴이 BFF다. 그림으로 그려 보자.

```
[브라우저(SPA)]
     ↓ (1) 같은 도메인의 BFF에 HTTP 호출
     ↓     세션 쿠키(HttpOnly·Secure·SameSite=Strict)만 들고 다님
     ↓     토큰은 쳐다보지도 않음
[BFF (Spring Cloud Gateway + Spring Security)]
     ↓ (2) 자기가 OAuth confidential client
     ↓     IdP에서 받은 access/refresh token을 서버 측에서 보관
     ↓     SPA에서 들어온 호출에 토큰을 자동 첨부해 IdP/자원 서버로 forward
[외부 IdP (Keycloak/Auth0/Google)] ←→ [자원 서버 (Spring Security oauth2ResourceServer)]
```

핵심을 다시 짚자.

- **브라우저는 OAuth 클라이언트가 아니다.** 토큰을 보지도 않는다.
- **브라우저는 BFF와 같은 도메인.** 그러므로 CORS 필요 없음. HttpOnly·SameSite 쿠키만으로 통신.
- **토큰은 서버 측 저장.** XSS로 새지 않는다.
- **CSRF 보호는 SameSite + custom header 이중 방어.** stateful 흐름이 살아 있으므로 9장의 CSRF 보호망이 그대로 적용된다.

이 패턴을 Curity 팀이 2021년에 "Token Handler Pattern"이라는 이름으로 정리했고, Duende가 같은 시기에 "BFF" 이름으로 정리했다. 둘 다 같은 모델이다. 그리고 Spring 진영에서는 Spring Cloud Gateway + Spring Security `oauth2Login`의 조합이 BFF 구현의 사실상 표준이 됐다.

### 14.2.1 Spring Cloud Gateway + `oauth2Login`으로 BFF를 짜 보자

코드 골격은 의외로 간단하다. 빌드 의존성에 `spring-cloud-starter-gateway`와 `spring-boot-starter-oauth2-client`를 함께 박고, 다음 구성을 올린다.

```java
@Configuration
@EnableWebFluxSecurity
class BffSecurityConfig {

    @Bean
    SecurityWebFilterChain bff(ServerHttpSecurity http,
                               ReactiveClientRegistrationRepository clients) {
        return http
            .authorizeExchange(a -> a
                .pathMatchers("/", "/index.html", "/static/**", "/login").permitAll()
                .anyExchange().authenticated())
            .oauth2Login(Customizer.withDefaults())
            .logout(l -> l.logoutSuccessHandler(
                new OidcClientInitiatedServerLogoutSuccessHandler(clients)))
            .csrf(csrf -> csrf.csrfTokenRepository(
                CookieServerCsrfTokenRepository.withHttpOnlyFalse()))
            .build();
    }
}
```

BFF는 보통 Reactive(WebFlux) 기반이다. 그래서 `ServerHttpSecurity`를 쓴다 — 11장에서 다룬 어휘다. 핵심 줄은 세 개다. `oauth2Login`이 외부 IdP와의 인증 흐름을 처리하고, `OidcClientInitiatedServerLogoutSuccessHandler`가 OIDC RP-initiated logout으로 IdP 세션까지 정리하고, `CookieServerCsrfTokenRepository.withHttpOnlyFalse()`가 SPA의 자바스크립트가 CSRF 토큰을 읽어 custom header(`X-XSRF-TOKEN`)로 첨부할 수 있도록 한다.

그런데 여기서 한 가지 짚어 둘 게 있다. **CSRF 보호가 BFF 시나리오에서 의외로 까다롭다.** Stateful 세션 흐름이 살아 있으니까 CSRF 토큰은 꼭 필요한데, SPA가 자바스크립트로 호출하니까 토큰을 어떻게 전달할지가 고민이다. 6.x 시절에는 위 코드처럼 `withHttpOnlyFalse()`를 명시적으로 박고, SPA 측 fetch 인터셉터에서 쿠키를 읽어 헤더에 다시 박는 보일러플레이트를 직접 짜야 했다. 그게 적잖이 번거로웠다. 그래서 누가 GitHub 이슈를 띄웠다.

> **Spring Security 이슈 [#14149](https://github.com/spring-projects/spring-security/issues/14149)** — "Simplify CSRF Configuration for SPAs"

이 이슈가 7.0에서 답을 얻었다. `http.csrf(CsrfConfigurer::spa)` 한 줄이다.

```java
return http
    .authorizeExchange(...)
    .oauth2Login(Customizer.withDefaults())
    .csrf(CsrfConfigurer::spa)   // ← 7.0의 한 줄
    .build();
```

이 한 줄이 무엇을 자동으로 해 주는가? `CookieCsrfTokenRepository.withHttpOnlyFalse()`, `XorCsrfTokenRequestAttributeHandler`, BFF 모드에 맞는 `CsrfTokenRequestHandler` 조합을 한 번에 박는다. 9장 9.3절에서 본 그대로다. SPA + BFF 구성에서 가장 흔히 틀리는 부분 — CSRF 토큰을 쿠키로 발급하면서도 헤더로 받아야 한다는 비대칭 — 이 한 줄로 표준화된다.

이 한 줄이 BFF 패턴 보급에 기여한 바를 우리는 좀 과소평가하기 쉽다. 하지만 솔직히 말해, 6.x 시절 BFF 한번 짜 본 사람이라면 안다. `withHttpOnlyFalse()`니 `CookieCsrfTokenRepository`니 하는 단어 조합을 검색하는 데만 한나절이 가던 시절이 있었다. 7.0의 한 줄은 그 한나절을 지운다. 작은 일 같지만 의미는 작지 않다.

### 14.2.2 BFF가 답하는 것, 답하지 못하는 것

BFF는 마법이 아니다. 솔직히 어떤 문제를 답하고 어떤 문제는 답하지 못하는지 짚어 보자.

**답하는 것:**
- 브라우저에서 토큰 보관 위치 문제 (서버 측으로 옮김)
- XSS로 인한 토큰 탈취 (브라우저에 토큰 자체가 없음)
- 도메인 분리된 SPA의 CORS 복잡성 (같은 도메인의 BFF로 호출)
- SPA의 CSRF 보호 (stateful 세션 + SameSite + custom header)

**답하지 못하는 것:**
- BFF 자체가 침해되면 모든 사용자의 토큰이 위험 (그래서 BFF 보안이 더 중요)
- 모바일 앱은 BFF 대상이 아니다 (모바일은 그냥 OAuth 네이티브 클라이언트로 가는 게 정석)
- 마이크로서비스 간 호출의 인증 (이건 자원 서버 + JWT가 풀 문제)

그러니까 BFF는 **SPA를 위한 패턴**이지 모든 클라이언트 유형의 답이 아니다. 모바일 앱이 있으면 모바일은 모바일대로 native OAuth + Authorization Code + PKCE로 가야 한다. 그리고 BFF 백엔드 자체의 보안 — Secret 관리, 토큰 회전, 침해 대응 — 은 별도로 챙겨야 한다. 그게 다음 절의 주제다.

> **요약 박스 — SPA 보안 결정 트리**
>
> - SPA가 모놀리식 백엔드와 같은 도메인? → 보통 세션 쿠키만으로 충분. BFF 없이도 됨.
> - SPA와 백엔드 도메인이 분리? + 외부 IdP 사용? → **BFF 강력 권장**.
> - 모바일 앱 + SPA 함께 운영? → 모바일은 native OAuth, SPA는 BFF. 두 트랙 별도 운영.
> - 마이크로서비스 간 호출? → BFF와 무관. JWT 자원 서버 + DPoP/mTLS.

## 14.3 Secret 회전·키 관리 — 운영의 첫 번째 모서리

Zero Trust 원칙과 BFF 패턴까지 좌표를 박았다. 이제 운영의 모서리들로 넘어가자. 첫 번째 모서리는 Secret이다.

Secret이 뭔지부터 분명히 하자. 시스템이 "비밀로 유지해야 정상 동작하는 값" 전부다. 우리 책 범위에서 보면 적어도 다음이 있다.

- JWT 서명 키 (대칭이면 HS256의 shared secret, 비대칭이면 RS256/ES256의 개인키)
- 패스워드 인코딩의 work factor와 salt
- OAuth2 client_secret
- DB credential
- 외부 API 키

이 값들이 노출되면 시스템이 사실상 무너진다. 그래서 두 가지가 모두 중요하다. **(1) 노출되지 않게 보관하기**, 그리고 **(2) 주기적으로 갈아 끼우기 (rotation)**. 둘 다 평소엔 신경을 덜 쓰다가 사고가 나야 그 중요성을 절감하게 된다. 그래서 더 찜찜한 영역이다. 끔찍한 일이다.

### 14.3.1 JWK 회전 — 키 한 짝을 갈아 끼우는 안전한 절차

JWT를 RS256/ES256 같은 비대칭 알고리즘으로 서명한다고 해 보자. IdP가 공개키를 JWKS endpoint(보통 `/.well-known/jwks.json`)로 노출하고, 자원 서버는 그걸 캐시해 두고 토큰 검증에 쓴다. 5장에서 본 그림이다. 그런데 개인키가 외부에 한 번 노출되면 어떻게 해야 할까?

가장 안전한 답은 **무중단으로 새 키 쌍을 추가하고, 옛 키 쌍을 점진적으로 폐기하는 것**이다. JWKS는 키 배열이다. 새 `kid`(key id)로 키 쌍을 하나 더 추가해도 기존 토큰의 검증이 깨지지 않는다. JWT 헤더의 `kid`가 옛 키를 가리키면 옛 공개키로, 새 키를 가리키면 새 공개키로 검증된다. 일정 기간 두 키를 함께 운영하다가 옛 토큰의 만료(보통 access token TTL인 15분~1시간)가 지나면 옛 키를 JWKS에서 제거한다.

자원 서버 측 코드에서 7.0이 제공하는 단축은 `NimbusJwtDecoder` + `JwkSourceBuilder`다.

```java
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder
        .withJwkSetUri("https://idp.example.com/.well-known/jwks.json")
        .cache(Duration.ofMinutes(5))         // JWKS 캐시 TTL
        .restOperations(restTemplate())       // 커스텀 timeout/retry 가능
        .build();
}
```

핵심은 두 가지다. **JWKS를 메모리에 캐시하되 TTL을 둔다.** 너무 길면 회전이 늦게 반영되고, 너무 짧으면 IdP에 부하가 간다. 보통 5~15분이 균형점이다. 그리고 **JWKS endpoint 호출 실패를 우아하게 처리한다.** IdP가 잠시 다운돼도 캐시된 키로 계속 검증할 수 있게 timeout과 retry를 명시적으로 설정해 두자. 기본값으로 두면 첫 호출 실패가 그대로 자원 서버 다운으로 이어지는 경우가 있다.

회전 운영을 자동화하려면 IdP 측에서 cron 스케줄로 새 키를 발급하고 JWKS에 추가하는 작업이 필요한데, Spring Authorization Server는 7.0에서 이걸 직접 지원한다. 외부 IdP(Keycloak·Auth0)는 콘솔에서 회전 주기를 설정하면 된다. Spring Security 측은 그 변화를 자동으로 따라가도록 위 코드만 정확히 짜 두면 된다. 한 번 짜 두면 운영자가 손을 댈 일이 거의 없다 — 이게 표준의 힘이다.

### 14.3.2 BCrypt 12 → Argon2id로 옮겨 가는 의미

다음으로 패스워드. 7.0에서 추가된 Password4j 기반 인코더 다섯 개 — `Argon2Password4jPasswordEncoder`, `ScryptPassword4jPasswordEncoder`, `BCryptPassword4jPasswordEncoder`, `PBKDF2Password4jPasswordEncoder`, `BalloonHashingPassword4jPasswordEncoder` — 가 1장에서 큰 그림으로 짚었던 변화다. 그중 가장 권장되는 게 Argon2id다.

왜 옮겨 가는가? 한 줄로 답하면 — **BCrypt가 GPU 공격에 약하다.** BCrypt는 2000년 전후로 표준이 됐고, 그때 기준으로는 충분히 안전했다. work factor 10~12면 단일 CPU에서 검증에 100ms~300ms가 걸렸다. 그런데 2020년대 들어 GPU/ASIC을 동원하면 BCrypt 12의 무차별 대입 속도가 초당 수천~수만 번에 도달한다. Argon2id는 메모리 hard 함수다. 검증할 때 일정량의 메모리(예: 64MB)를 점유해야 해서 GPU 병렬화의 이점이 크게 줄어든다. OWASP가 2021년부터 Argon2id를 1순위 권장 알고리즘으로 올린 이유다.

전환은 점진적으로 한다. Spring Security의 `DelegatingPasswordEncoder`가 prefix(`{bcrypt}`, `{argon2}`)로 알고리즘을 구분하기 때문에, 기존 BCrypt 해시를 그대로 두고 새로 등록되는 사용자만 Argon2id로 인코딩해도 시스템이 자연스럽게 굴러간다. 로그인 성공 시점에 옛 해시를 재인코딩해 점진적으로 갈아 끼우는 패턴도 표준이다 (`PasswordEncoder.upgradeEncoding(encodedPassword)`로 판단).

```java
@Bean
PasswordEncoder passwordEncoder() {
    String idForEncode = "argon2";
    Map<String, PasswordEncoder> encoders = new HashMap<>();
    encoders.put("argon2", new Argon2Password4jPasswordEncoder());
    encoders.put("bcrypt", new BCryptPasswordEncoder(12));
    encoders.put("pbkdf2", new Pbkdf2PasswordEncoder("", 16, 310_000, SHA256));
    return new DelegatingPasswordEncoder(idForEncode, encoders);
}
```

이 코드 한 번 박아 두면 신규 사용자는 자동으로 Argon2id로 가고, 기존 BCrypt 사용자도 검증은 그대로 된다. 점진 마이그레이션이 깔끔하게 굴러간다.

### 14.3.3 application.yml에 평문은 절대 두지 말자 — Vault 패턴

마지막으로 한 가지만 더. 운영 코드베이스에서 자주 보이는 안티 패턴이 있다.

```yaml
# application.yml — 절대 이렇게 두지 말자
spring:
  datasource:
    password: SuperSecret123!
  security:
    oauth2:
      client:
        registration:
          google:
            client-secret: abc-xyz-secret
```

이게 왜 문제인가? 평문 secret이 소스 코드 저장소에 들어간다. Git 히스토리에 박혀서 한 번 커밋되면 사실상 영구히 노출된다. 더 큰 문제는 다음 절의 Actuator 사고로 이어진다 — Actuator `env` endpoint가 한 번 노출되면 이 평문이 그대로 외부에 뿌려진다.

해법은 외부 secret store다. 가장 표준적인 조합은 **Spring Cloud Config + HashiCorp Vault**다. 또는 AWS Secrets Manager, Azure Key Vault, GCP Secret Manager 같은 클라우드 네이티브 서비스도 있다. 어느 쪽이든 핵심 원칙은 동일하다 — **application.yml에는 secret store의 참조만, 실제 값은 런타임에 안전하게 주입.** Spring Boot의 `${...}` placeholder가 환경 변수, Vault, K8s Secret 어디든 동일한 문법으로 받아 준다.

이 한 가지 원칙을 운영 첫날부터 박아 두자. "나중에 옮기겠다"는 평문 secret은 거의 영원히 그 자리에 있다. 그리고 어느 날 사고가 난다.

## 14.4 Actuator 안전 운영 — 찜찜한 endpoint 하나가 모든 보안을 무너뜨릴 수 있다

Secret 이야기의 자연스러운 다음 단계가 Actuator다. 한국 개발자라면 우아한형제들 기술블로그의 "Security Actuator 안전하게 사용하기" 글을 한 번쯤 봤거나 들었을 것이다 ([techblog.woowahan.com/9232](https://techblog.woowahan.com/9232/)). 그 글이 정리하는 핵심을 한 줄로 옮기면 이렇다 — **Actuator는 개발자에게 편리하지만, 잘못 노출하면 매우 위험하다.**

Spring Boot Actuator는 개발 편의 도구다. `/actuator/health`로 상태를 보고, `/actuator/metrics`로 메트릭을 빼내고, `/actuator/env`로 설정값을 검사하고, `/actuator/heapdump`로 힙 덤프를 받는다. 운영 중에 한 번 갖다 쓰면 정말 편한 도구들이다. 그런데 이 endpoint들이 외부에 노출되면 어떻게 되는가?

- `/actuator/env` → application.yml의 모든 설정값(DB password 평문 포함) 노출
- `/actuator/heapdump` → 메모리 덤프 통째로 노출. 그 안에 평문 토큰·세션·비밀번호가 모두 들어 있음
- `/actuator/configprops` → 모든 `@ConfigurationProperties` 값 노출
- `/actuator/threaddump` → 실행 중인 스레드 정보. 토큰이 메서드 파라미터에 박혀 있으면 함께 노출

한 번 노출되면 그 자체가 사고다. 우아한형제들 글에 정리된 실제 사례를 보자. "잘못 쓰면 매우 위험하다"는 말은 과장이 아니다. 노출된 `env` endpoint에서 DB credential을 추출한 공격자가 DB에 직접 접속한 사례, heap dump에서 active session token을 추출해 다른 사용자로 가장한 사례. 모두 운영에서 실제로 일어났다.

### 14.4.1 Actuator 노출 정책 — 최소 권한의 원칙

Spring Boot 3 이후의 기본값은 사실 꽤 안전하다. `management.endpoints.web.exposure.include`의 기본값이 `health` 하나뿐이다. 즉, 별도 설정 없이는 `/actuator/health`만 노출되고 나머지는 모두 차단된다. 그런데 운영에서 모니터링 도구가 메트릭을 빼내야 한다거나 디버깅이 필요하다며 `*`로 풀어 두는 경우가 있다. 이게 사고의 시작이다.

권장 패턴은 이렇다.

```yaml
# application.yml — 외부 노출용 (운영)
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus   # 꼭 필요한 것만
        exclude: env,beans,configprops,heapdump,threaddump
  endpoint:
    health:
      show-details: when-authorized       # 인증된 사용자에게만 상세 노출
      show-components: when-authorized
```

원칙은 단순하다. **노출 목록은 include로 명시적으로 켠다. exclude는 안전망.** `*`는 절대 쓰지 말자. 그리고 `health.show-details`도 기본값 `never` 또는 `when-authorized`로 두자. `always`는 데이터센터 IP 정보까지 노출하는 경우가 있다.

### 14.4.2 별도 SecurityFilterChain으로 Actuator 격리

한 발 더 나간 패턴은 Actuator를 **별도 `SecurityFilterChain`으로 격리**하는 것이다. 2장에서 본 두 개의 체인 패턴이 여기서 다시 빛난다.

```java
@Configuration
@EnableWebSecurity
class ActuatorSecurityConfig {

    @Bean
    @Order(1)   // 먼저 매칭
    SecurityFilterChain actuator(HttpSecurity http) throws Exception {
        return http
            .securityMatcher("/actuator/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers("/actuator/health", "/actuator/info").permitAll()
                .anyRequest().hasRole("OPS"))
            .httpBasic(Customizer.withDefaults())
            .csrf(CsrfConfigurer::disable)   // Actuator는 stateless
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .build();
    }

    @Bean
    @Order(2)
    SecurityFilterChain app(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(a -> a.anyRequest().authenticated())
            .oauth2Login(Customizer.withDefaults())
            .build();
    }
}
```

이 패턴의 장점은 명료하다. **Actuator 경로는 일반 사용자 인증과 완전히 분리된 별도 정책으로 굴러간다.** `ROLE_OPS`를 가진 운영자만 접근 가능, HTTP Basic으로 SRE 도구가 직접 호출 가능, 세션 없음, CSRF 없음. 그리고 일반 사용자가 어떤 OIDC 흐름으로 로그인하든 Actuator 경로는 완전히 격리된다.

추가로, **별도 포트로 노출하는 것**도 강력한 패턴이다.

```yaml
management:
  server:
    port: 9001    # 운영 전용 포트
    address: 127.0.0.1   # 외부 인터페이스에 바인딩 안 함
```

이렇게 두면 외부 LB가 9001 포트로는 트래픽을 보내지 않고, 내부 모니터링 시스템이나 SRE의 SSH 터널을 통해서만 접근 가능하다. 이게 가장 안전한 모델이다. "기본 격리 + 인증 격리"의 이중 방어.

이런 식으로 한 번 분리해 두면, 일반 비즈니스 코드의 보안 정책이 바뀌어도 Actuator 정책은 영향을 받지 않는다. 그리고 그 반대도 마찬가지. 운영팀이 새 메트릭 endpoint를 켜고 싶다고 비즈니스 보안에 손댈 일이 없다. 운영의 안정성은 결국 이런 모서리들에서 결정된다.

## 14.5 관측·감사 — 누가 언제 무엇을 했는가

Zero Trust 원칙 5와 7 — 지속 모니터링과 정보 수집 — 이 운영 영역에서 구체화되는 곳이 관측과 감사다. Spring Security가 이걸 위해 명시적으로 제공하는 것이 **인증 이벤트**다.

### 14.5.1 `AuthenticationSuccessEvent` / `AuthenticationFailureEvent`

`AuthenticationManager`가 인증을 처리할 때마다 Spring `ApplicationEventPublisher`로 이벤트를 던진다. 두 종류가 핵심이다.

- `AuthenticationSuccessEvent` — 인증 성공
- `AbstractAuthenticationFailureEvent`의 하위 — `BadCredentialsException`, `UsernameNotFoundException`, `LockedException` 등 각 실패 사유별로 세분화된 이벤트

이걸 `@EventListener`로 받아서 감사 로그에 쌓는 게 가장 깔끔한 패턴이다.

```java
@Component
class AuthenticationAuditListener {

    private static final Logger log = LoggerFactory.getLogger("AUDIT");

    @EventListener
    void onSuccess(AuthenticationSuccessEvent event) {
        Authentication auth = event.getAuthentication();
        log.info("AUTH_SUCCESS user={} authorities={} timestamp={}",
            auth.getName(),
            auth.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList(),
            Instant.now());
    }

    @EventListener
    void onFailure(AbstractAuthenticationFailureEvent event) {
        Authentication auth = event.getAuthentication();
        log.warn("AUTH_FAILURE user={} reason={} timestamp={}",
            auth != null ? auth.getName() : "unknown",
            event.getException().getClass().getSimpleName(),
            Instant.now());
    }
}
```

이 한 컴포넌트가 박혀 있으면 모든 인증 시도가 `AUDIT` 로그에 남는다. 운영팀의 SIEM(Security Information and Event Management) 시스템이 이 로그를 흡수해 알람을 만들 수 있다.

### 14.5.2 Brute-force 탐지 — 실패 이벤트 카운트로 한 단계 더

실패 이벤트를 단순히 로그로만 남기지 말고, **카운트해서 임계치를 넘으면 차단**까지 가는 게 한 단계 더 나간 패턴이다. 가장 단순한 구현은 in-memory 카운터 + 일정 시간 슬라이딩 윈도우다.

```java
@Component
class BruteForceProtection {

    private final Cache<String, AtomicInteger> failures =
        Caffeine.newBuilder()
            .expireAfterWrite(Duration.ofMinutes(15))
            .build();

    @EventListener
    void onFailure(AbstractAuthenticationFailureEvent event) {
        String username = event.getAuthentication().getName();
        int count = failures.get(username, k -> new AtomicInteger()).incrementAndGet();
        if (count >= 5) {
            // 외부 IdP API 호출 또는 로컬 DB의 user.locked 플래그를 set
            lockUser(username);
        }
    }

    @EventListener
    void onSuccess(AuthenticationSuccessEvent event) {
        failures.invalidate(event.getAuthentication().getName());
    }
}
```

15분 안에 5번 실패하면 잠근다. 성공하면 카운터 리셋. 단순하지만 효과적이다. 분산 환경이면 Caffeine 캐시 자리를 Redis로 바꾸면 된다. 더 정교한 정책 — IP 기반, 디바이스 핑거프린트 — 으로 확장하려면 별도 보안 미들웨어(reCAPTCHA·Cloudflare Bot Management)와 결합하는 게 자연스럽다. 다만 시작은 위 코드 한 컴포넌트면 충분하다. 첫 안전망부터 깔자.

### 14.5.3 감사 로그 패턴 — 인증을 넘어 인가까지

인증 이벤트만이 아니라 **권한 거부 사건도 감사에 남기는 것**이 좋다. `AccessDeniedException`이 발생하는 자리에 hook을 박자. 8장에서 다룬 `AccessDeniedHandler`가 가장 자연스러운 자리다.

```java
@Component
class AuditingAccessDeniedHandler implements AccessDeniedHandler {

    private static final Logger log = LoggerFactory.getLogger("AUDIT");

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response,
                       AccessDeniedException denied) throws IOException {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        log.warn("ACCESS_DENIED user={} method={} path={} authorities={}",
            auth != null ? auth.getName() : "anonymous",
            request.getMethod(),
            request.getRequestURI(),
            auth != null ? auth.getAuthorities() : List.of());
        // 그 다음 ProblemDetail로 403 응답 (8장 8.8절 참조)
        response.setStatus(HttpStatus.FORBIDDEN.value());
        response.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
        new ObjectMapper().writeValue(response.getOutputStream(),
            ProblemDetail.forStatusAndDetail(FORBIDDEN, "Access denied"));
    }
}
```

이 한 컴포넌트로 모든 권한 거부가 감사 로그에 남는다. 어떤 사용자가 어떤 자원을 어떻게 시도했는지 — 사고 발생 시 가장 먼저 보고 싶은 정보가 자동으로 쌓인다. 그리고 8장에서 짠 `AccessDeniedHandler` 자리에 자연스럽게 들어간다. 별도 인프라가 아니다.

## 14.6 책 전체를 가로지른 논쟁점들 — 정답이 하나가 아닌 결정들

자, 이제 14장의 마지막 절이다. 책을 읽어 오면서 곳곳에서 마주친 논쟁점들이 있다. 5장의 JWT 함정 박스, 7장의 MFA factor 정책, 9장의 CSRF disable 결정. 매번 "이건 시스템 맥락에 따라 다르다"고 말하고 미뤘던 결정들이다. 그 결정들을 한자리에 모아 정리하자. 답은 여전히 하나가 아니다. 다만 **각 답이 어떤 맥락에서 정답이 되는지**를 또렷이 가리는 게 이 절의 목표다.

### 14.6.1 JWT vs Session — 새 합의는 "둘 다 쓴다"로 수렴한다

가장 오래된 논쟁이다. DZone에 실린 한 글이 한 시대를 대변한다 — "Stop Using JWTs as Session Tokens" ([dzone.com](https://dzone.com/articles/stop-using-jwts-as-session-tokens)). 한 GitHub gist에서는 더 직설적이다 — "단순한 세션 토큰 용도의 JWT는 정규 세션 쿠키보다 비효율적이고 덜 유연하며, 얻는 이점도 없다" ([samsch gist](https://gist.github.com/samsch/0d1f3d3b4745d778f78b230cf6061452)). 이 의견의 핵심 논거는 5장 함정 6에서 짚었던 그것이다. **JWT는 강제 로그아웃이 어렵고, 권한 변경이 즉시 반영되지 않는다.** 자체 발급한 토큰을 외부에서 만료시키려면 별도 blacklist 캐시가 필요한데, 그러면 사실상 세션 저장소가 다시 등장한다.

반대편 의견도 있다. 마이크로서비스 환경에서는 stateless의 가치가 크다. 자원 서버가 토큰 검증을 위해 IdP에 매번 묻는 게 아니라 JWKS 캐시만으로 즉시 검증할 수 있다는 점, 서비스 간 호출에서 토큰을 자연스럽게 forward할 수 있다는 점. 이건 세션 모델로는 어렵다.

새로 형성되고 있는 합의는 이렇다. **브라우저 ↔ BFF 사이는 세션 쿠키, BFF ↔ 자원 서버 사이는 JWT.** 이 한 줄이 두 진영의 강점을 모두 살린다. 브라우저는 stateful 세션 보호망(CSRF·SameSite·HttpOnly)을 그대로 누리고, 백엔드 서비스 간은 stateless JWT의 확장성을 누린다. 14.2절의 BFF 패턴이 사실상 이 합의의 코드적 구현이다.

그러니 "JWT를 쓸까 세션을 쓸까?"라는 질문 자체가 잘못 던져진 질문일 수 있다. 정확한 질문은 "어디에 JWT를, 어디에 세션을 쓸까?"다. 그리고 본 책의 답은 — 브라우저 측은 세션, 서비스 간은 JWT, 둘을 잇는 BFF가 변환 계층.

### 14.6.2 Spring Authorization Server 직접 운영 vs 외부 IdP

이 결정은 운영 능력의 문제다.

Spring Authorization Server가 7.0에 흡수되면서 운영 부담이 크게 줄었다. 같은 릴리스 사이클을 타니까 버전 충돌이 없고, 같은 Spring Security 어휘로 설정할 수 있다. 그런데도 여전히 외부 IdaaS(Auth0, Okta, Keycloak, Authentik)를 쓰는 게 일반적 best practice다. 이유가 있다.

**자체 운영의 부담:**
- JWK 회전 운영 (자동화 가능하지만 첫 셋업이 무겁다)
- 사용자 디렉토리 관리, 비밀번호 재설정 흐름
- MFA factor 발급·관리
- SOC 2, ISO 27001 같은 컴플라이언스 감사
- 24/7 가용성 보장

**외부 IdaaS의 가치:**
- 위 항목 전부를 벤더가 책임
- 새 표준(OAuth 2.1, FAPI 2.0, OpenID4VC) 대응이 자동
- 보안 사고 시 책임 분담

언제 자체 운영이 맞는가? 외부 IdaaS에 사용자 데이터를 맡기기 곤란한 경우(정부·금융·헬스케어 일부 시나리오), 또는 사용자가 1만 명을 훨씬 넘어 외부 IdaaS 라이선스 비용이 자체 운영 비용을 넘는 경우. 그 외의 90%는 외부 IdaaS가 답이다.

본 책의 권고는 명확하다 — **운영팀이 키 관리·디렉토리 운영·컴플라이언스 감사를 모두 떠맡을 자신이 있는 게 아니라면, 외부 IdaaS를 쓰자.** Spring Security는 OAuth2 Client 측에서 외부 IdaaS와 너무 잘 통합되므로 그쪽 길이 정석에 가깝다.

### 14.6.3 localStorage vs Cookie — 다시 한 번

이 논쟁은 사실 14.2의 BFF 절에서 거의 답이 나왔다. 그러나 다시 한 번 정리하자.

**localStorage:**
- XSS 한 번이면 토큰 탈취. 5장 함정 7.
- 도메인 분리된 SPA에서 쿠키 전달이 까다로울 때 일부 팀이 채택.
- 본 책 권고: **피해야 한다.**

**HttpOnly Cookie:**
- 자바스크립트로 읽을 수 없으니 XSS 안전망 한 겹.
- CSRF 보호 필요 (SameSite + custom header).
- 같은 도메인 또는 BFF가 있으면 자연스럽게 동작.
- 본 책 권고: **기본값.**

**in-memory + refresh:**
- 토큰을 메모리에만 보관. 페이지 리프레시 시 silent refresh.
- 도메인 분리 + 쿠키가 어려운 환경의 차선.
- 본 책 권고: **HttpOnly 쿠키가 불가능한 경우의 차선.**

OWASP·Auth0·Curity·NIST가 모두 HttpOnly 쿠키를 1순위로 권고한다. 본 책도 동의한다. localStorage는 마지막 선택지로 두자.

### 14.6.4 보안과 사용성의 끝없는 줄다리기

이 절의 결론이자 책의 결론에 가까운 한 단락이다.

읽다 보면 느꼈을 것이다. 보안 결정의 거의 모든 자리에서 한쪽에는 "더 안전하게"가, 반대편에는 "더 편하게"가 서 있다. MFA factor를 추가하면 보안은 올라가는데 로그인 단계가 늘어난다. 세션 TTL을 짧게 잡으면 토큰 탈취 시 노출 시간이 줄지만 사용자는 자주 다시 로그인해야 한다. CSP를 빡빡하게 잡으면 XSS 보호가 단단해지지만 외부 분석 도구나 위젯이 깨진다. DPoP를 도입하면 sender-constrained 토큰의 안전성을 얻지만 클라이언트 구현 복잡도가 올라간다.

정답은 하나가 아니다. 그러나 한 가지 원칙은 있다. **사용자 경험을 일정 수준 깎으면서까지 지켜야 할 자산이 무엇인가를 먼저 정하자.** 일반 SaaS의 로그인이라면 비밀번호 + OTP 2 factor면 충분할 수 있다. 금융 서비스라면 Passkeys + 디바이스 바인딩까지 가야 한다. 정부 시스템이라면 mTLS + 하드웨어 토큰까지. 자산의 가치가 곧 보안의 깊이를 정한다.

그리고 그 깊이를 한 번에 다 박지 말자. 점진적으로 가는 게 낫다. BFF + 세션 쿠키 + HttpOnly로 시작해, 운영 데이터가 쌓이면 MFA를 더하고, 그 다음 DPoP를 더하고. Spring Security 7은 이 단계적 진화의 각 단계에 맞는 부품을 빠짐없이 제공한다. 그게 우리가 14장 첫머리에서 박은 명제 — "Zero Trust는 원칙이지 제품이 아니다" — 의 진짜 의미다.

> **좌표 박스 — K8s Service Mesh / mTLS와의 관계**
>
> 본 책 범위 밖이지만 한 번 좌표만 박아 두자. Istio·Linkerd·Cilium 같은 Service Mesh는 sidecar(Envoy)로 서비스 간 트래픽을 가로채 mTLS로 자동 암호화·인증한다. Zero Trust 원칙 2(위치 무관 통신 보호)의 가장 강력한 구현이다. Spring Security 7은 이 영역과 직접 부딪히지 않는다 — mTLS는 sidecar가, JWT 자원 서버는 애플리케이션이 책임진다. 그리고 sender-constrained 토큰의 표준은 DPoP만 있는 게 아니다. RFC 8705(OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens)가 mTLS 인증서 기반 토큰 바인딩을 표준화했다. Spring Security 7도 자원 서버 측에서 `cnf.x5t#S256` 검증으로 지원 가능. FAPI 2.0 같은 고보안 환경에서는 DPoP보다 mTLS-bound가 더 흔하다. 본격 도입은 다른 책의 몫이다.

## 14장 핵심 5줄 요약

1. **Zero Trust는 원칙이지 제품이 아니다.** NIST SP 800-207의 7 tenets 각각이 Spring Security 7의 부품(필터 체인, `AuthorizationManager`, MFA, DPoP, STATELESS 자원 서버, 인증 이벤트)에 직접 매핑된다.
2. **BFF가 SPA + OAuth2의 새 표준이다.** 브라우저는 OAuth 클라이언트가 아니다. HttpOnly 세션 쿠키만. `http.csrf(CsrfConfigurer::spa)` 한 줄이 7.0의 BFF 코드를 단순화했다.
3. **Secret은 외부 저장소에. application.yml에 평문 금지.** JWK는 무중단으로 회전. 패스워드는 BCrypt 12에서 Argon2id로 점진 이행.
4. **Actuator는 별도 `SecurityFilterChain`으로 격리.** 노출 목록은 include로 명시. `*`는 절대 쓰지 말자. 가능하면 별도 포트(`management.server.port`)로.
5. **모든 결정에 정답은 하나가 아니다.** JWT vs 세션, 자체 IdP vs 외부, localStorage vs Cookie — 답은 시스템 맥락이 정한다. 본 책 권고: 브라우저는 세션, 서비스 간은 JWT, 외부 IdaaS 우선, HttpOnly 쿠키 기본.

## 다음 챕터에서 답할 것

그래서 이 모든 결정을 한 프로젝트에서 어떻게 합치는가? 한 권의 책에서 우리가 만난 부품들 — 두 개의 `SecurityFilterChain`, OAuth2 Login + PKCE, JWT 자원 서버 + DPoP, MFA, BFF의 CSRF·CORS·CSP, 12장의 회귀 테스트, 14장의 감사 로그와 키 회전 — 을 한 프로젝트에 모두 합쳐 빌드한다면 어떻게 짜이는가?

마지막 챕터는 통합 워크스루다. 모놀리식 백엔드(Spring Boot 4) + SPA(React) + 외부 IdP(Keycloak) + BFF(Spring Cloud Gateway) 조합으로, 처음부터 끝까지 한 시나리오를 끝까지 빌드한다. 이 책을 덮고 나면 자기 프로젝트에 무엇을 만들 수 있는지의 구체적 증명이 거기에 있다. 한 권을 한 시나리오로 합치는 길로 함께 가 보자.

---

# 15장. 한 권을 한 시나리오로 — 통합 실전 워크스루

> 선행 필요: 1~14장 전부. 책의 출구 챕터.

여행이 끝나간다. 1장에서 빨갛게 변한 빌드 화면을 같이 들여다본 게 엊그제 같은데, 그 사이 우리는 필터 체인 한 줄씩을 헤집었고, JWT의 `cnf.jkt` 클레임이 무엇을 의미하는지 알아냈고, OAuth2 Authorization Code 흐름의 다섯 박스를 그렸고, Passkeys ceremony 두 가지를 따라 그렸고, MFA의 factor가 사실 권한이라는 사실에 잠시 멈춰 섰고, 인가의 다섯 층을 줄지어 늘어놓았으며, 마침내 BFF라는 패턴 앞에서 "그래서 우리 SPA는 어떻게 해야 하지?"라는 물음에 답을 마련했다.

그런데 솔직히 말해 보자. 한 챕터씩 떼어서 볼 때는 명료하던 그림이, 한 프로젝트 안에 다 합쳐 놓으려고 보면 다시 흐릿해진다. 자주 일어나는 일이다. 인증과 인가, 클라이언트와 자원 서버, 세션과 토큰, BFF와 SPA — 이 어휘들이 한 시스템 안에서 어떻게 손을 잡는지, 그 손목 위로 어떤 헤더가 흐르고 어떤 쿠키가 오가는지를 한눈에 보지 못하면 책을 덮은 뒤에도 한참 헤매게 된다. 그래서 마지막 한 챕터를, 책 전체를 한 시나리오로 묶는 데 쓰기로 했다.

## 15.1 ShopVault — 한 권을 통과시킬 한 가게

상상해 보자. 우리가 새로 맡은 서비스 이름은 **ShopVault**다. 작지만 만만치는 않은 온라인 상점이다. 일반 사용자는 상품을 보고, 장바구니에 담고, 주문하고, 결제한다. 운영 측은 별도의 관리자 대시보드로 주문을 처리하고, 재고를 조정하며, 가끔은 환불 같은 민감한 작업을 한다. 외부에서 결제를 처리할 게이트웨이 한 곳과도 OAuth2로 묶여 있다. 그리고 인증·인가의 신원 서버는 회사가 외부에 운영하는 Keycloak 한 대.

지나치게 친근한 시나리오 아닌가? 이 책을 읽는 한국 개발자라면, 이름만 바꾸면 사실 자기 팀에서 한 번쯤 마주친 그림일 것이다. 그래서 골랐다. 새로움이 아니라 익숙함이 이번 장의 무기다. 익숙한 풍경 위에 7.0의 어휘들을 한 줄씩 덧그려 보자는 거다.

ShopVault의 구성 요소를 풀어 보면 이렇다.

- **shop-web** — React SPA. 일반 사용자도 보고, 관리자도 본다. 한 도메인 `app.shopvault.com` 아래에서 서비스된다.
- **shop-bff** — Spring Cloud Gateway 기반의 BFF. `app.shopvault.com`이 실제로 가리키는 첫 번째 서버다. SPA 정적 자원을 내려주고, `/api/**`로 들어오는 요청을 자원 서버로 fan out한다. OAuth2 confidential client 역할을 맡는다.
- **shop-api** — Spring Boot 4.0 모놀리식 백엔드. JWT Bearer + DPoP 자원 서버다. `api.shopvault.com` 도메인으로 직접 접근도 가능하지만, 브라우저는 BFF를 통해서만 닿는다.
- **shop-keycloak** — Keycloak 25.x 한 대. `auth.shopvault.com` 도메인. realm 한 개(`shopvault`), 클라이언트 두 개(`shopvault-bff` confidential, `shopvault-api` 자원 서버), 외부 결제 게이트웨이용 클라이언트(`shopvault-payment-client`) 한 개.
- **payment-gateway** — 외부 결제사 OAuth2 자원 서버. 우리는 client credentials grant로 access token을 받아 호출한다.

이 다섯 조각이 우리 시나리오의 전부다. 한 페이지짜리 아키텍처 그림으로 박아 두자.

```
                          ┌──────────────────────────────┐
                          │      shop-keycloak           │
                          │      (auth.shopvault.com)    │
                          │ realm: shopvault             │
                          │ clients: bff / api / payment │
                          └───┬────────────┬─────────────┘
                              │            │
              Auth Code+PKCE  │            │ JWKs
                              │            │ (issuer-uri discovery)
                              │            │
            ┌─────────────────▼────────┐   │
            │     shop-bff             │   │
 Browser ───▶ Spring Cloud Gateway     │   │
 (HttpOnly  │ oauth2Login (confidential)│  │
  Session   │ HttpOnly Session Cookie  │   │
  Cookie)   │ csrf(spa)                │   │
            │ token-relay filter       │   │
            └───────────┬──────────────┘   │
                        │                  │
              Bearer +  │                  │
              DPoP      ▼                  │
            ┌──────────────────────────┐   │
            │     shop-api             │◀──┘
            │ Spring Boot 4 / Sec 7    │
            │  ┌────────────────────┐  │
            │  │ FilterChain @Order(1) /actuator/** (no auth, isolated port)
            │  │ FilterChain @Order(2) /api/** (oauth2ResourceServer.jwt + DPoP)
            │  └────────────────────┘  │
            │ MFA factor authorities    │
            │ @PreAuthorize on services │
            └───────────┬──────────────┘
                        │
                        │ @HttpExchange + @ClientRegistrationId("payment")
                        │ (client_credentials, access token auto-injected)
                        ▼
            ┌──────────────────────────┐
            │   payment-gateway        │
            │   (외부 OAuth2 자원 서버) │
            └──────────────────────────┘
```

이 그림 한 장에 책의 거의 모든 어휘가 들어 있다. 필터 체인은 2장, 컴포넌트 위임은 3장, OAuth2 Client는 6장, 자원 서버와 DPoP는 5장, 세션·쿠키는 10장, CSRF SPA 모드는 9장, MFA factor 권한은 7장, 메서드 보안은 8장, BFF 패턴은 14장. 한 챕터씩 떼어 보던 어휘가, 한 시스템 안에서 어떤 자리에 들어가 어떤 이웃과 손을 잡는지를 이 그림이 정직하게 보여 준다.

이 장의 흐름은 이렇게 잡았다. 먼저 Keycloak 쪽 설정을 짚는다(15.2). 그다음 BFF 한 덩어리를 빌드한다(15.3). 그다음 자원 서버 `shop-api`를 두 개의 `SecurityFilterChain`으로 분리해 짜고(15.4), 메서드 보안과 MFA를 거기 얹는다(15.5, 15.6). 그다음 세 가지 인증 흐름 — 일반 사용자 로그인(15.7), 관리자 MFA 로그인(15.8), SPA → BFF → API 호출(15.9) — 을 시퀀스로 따라간다. 마지막으로 외부 결제 게이트웨이 호출(15.10)과 운영 체크리스트(15.11), 그리고 14개 챕터의 어휘가 어떻게 이 한 시스템에 다 녹았는지 회고하는 단(15.12)으로 마무리한다.

> **시그니처 변동 가능성에 대한 한 마디 (다시).** 이 장의 코드는 모두 Spring Security 7.0 GA(2025-11-17) 기준이다. 7.1.x milestone 단계에서 `AuthorizationManagerFactory`, `@EnableMultiFactorAuthentication` 같은 신규 API의 시그니처가 미세하게 다듬어질 가능성이 있다. 본문 코드를 그대로 옮겨 빌드가 살짝 어긋난다면, 7.0 GA로 의존성을 고정하거나 출간 시점의 공식 docs를 한 번 더 확인하는 편이 낫다. 이 책의 1장과 13장에서 같은 당부를 했지만, 마지막 장에서 한 번 더 짚어 둔다.

## 15.2 Keycloak 한 realm, 세 클라이언트

이 장은 Keycloak 설정 가이드가 아니다. 그러나 클라이언트 세 개의 정체와 권한 모델만큼은 한 번 정리해 두지 않으면, 뒤따라 나올 BFF·자원 서버 코드의 클레임 처리가 공중에 뜬다. 짧게만 짚자.

realm 이름은 `shopvault`. 그 안에 클라이언트를 세 개 만든다.

**클라이언트 1: `shopvault-bff` (confidential client)**

- Client type: OpenID Connect
- Access type: confidential
- Standard flow enabled (Authorization Code Grant)
- PKCE: required (S256)
- Valid redirect URIs: `https://app.shopvault.com/login/oauth2/code/keycloak`
- Web origins: `https://app.shopvault.com`
- Service account roles: 비활성화

`shopvault-bff`는 BFF가 사용자 로그인을 대리할 때 쓰는 OIDC 클라이언트다. PKCE는 7.0이 기본으로 켜 주지만, IdP 측에서도 `required`로 명시해 두면 6.x에서 올라온 코드가 explicit하게 끄고 있어도 IdP가 잘라낸다. 함정 15(레퍼런스 §7.4)에서 짚었던 그 경우다.

**클라이언트 2: `shopvault-api` (resource server)**

- Client type: OpenID Connect
- Access type: bearer-only
- Audience mapper로 access token에 `aud: shopvault-api` 추가
- Role 매핑: realm role `customer`, `admin`, `payment-admin`을 토큰의 `roles` 클레임으로 포함

자원 서버는 토큰을 검증할 뿐 토큰을 발급하지 않는다. `bearer-only`로 두는 게 자연스럽다. `aud` 클레임을 명시적으로 추가해 두는 이유는, JWT 함정 8(레퍼런스 §7.2) 그러니까 알고리즘·발급자 confusion을 한 겹 더 막기 위해서다. 자원 서버 측 코드에서 audience를 `OAuth2TokenValidator`로 검증해 줄 수 있다.

**클라이언트 3: `shopvault-payment-client` (client credentials)**

- Access type: confidential
- Service Accounts Enabled: true
- Standard flow: disabled
- Direct access grants: disabled
- 별도 realm role `payment:charge` 부여

이건 사용자 인증과 무관하다. `shop-api`가 외부 결제 게이트웨이를 부를 때 client credentials grant로 access token을 받기 위한 클라이언트다. 사용자가 끼지 않으므로 redirect URI도 없고 PKCE도 없다.

마지막으로 realm role 세 개를 만든다. `customer`, `admin`, `payment-admin`. 일반 가입자는 자동으로 `customer`. 관리자는 별도 그룹에 `admin`. 결제 환불 권한을 가진 사람만 `payment-admin`을 더 받는다. Keycloak에서 client scope의 role mapper를 통해 이 세 role이 access token의 `roles` 클레임 배열로 포함되도록 설정해 두자. 이 결정이 곧 자원 서버에서 `JwtAuthenticationConverter`가 다룰 클레임이 된다.

여기까지 짚고, 이제 코드로 넘어가자.

## 15.3 shop-bff — Spring Cloud Gateway로 빌드하는 BFF

BFF부터 짓는 이유는 단순하다. 이 시스템에서 브라우저가 가장 먼저 만나는 서버이기 때문이다. 14장에서 BFF의 원리는 다뤘다. 여기서는 코드를 짠다.

`build.gradle`의 핵심 의존성은 세 줄이다.

```kotlin
implementation("org.springframework.cloud:spring-cloud-starter-gateway")
implementation("org.springframework.boot:spring-boot-starter-oauth2-client")
implementation("org.springframework.cloud:spring-cloud-starter-oauth2")
```

Spring Cloud Gateway는 reactive(WebFlux) 위에서 돈다. 그래서 11장에서 다룬 reactive 보안 API가 여기서 깨어난다. 잊지 말자.

`application.yml`은 이렇게 짠다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            provider: keycloak
            client-id: shopvault-bff
            client-secret: ${KEYCLOAK_BFF_SECRET}
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            scope: openid, profile, email
        provider:
          keycloak:
            issuer-uri: https://auth.shopvault.com/realms/shopvault
  cloud:
    gateway:
      routes:
        - id: api
          uri: https://api.shopvault.com
          predicates:
            - Path=/api/**
          filters:
            - TokenRelay
        - id: spa
          uri: https://shop-web.internal.shopvault.com
          predicates:
            - Path=/**

server:
  servlet:
    session:
      cookie:
        same-site: lax
        http-only: true
        secure: true
        name: SHOPVAULT_SESSION
```

여기서 눈여겨볼 건 두 가지다.

첫째, `TokenRelay`라는 한 단어. Spring Cloud Gateway가 BFF에 내장해 준 마법이다. 사용자가 BFF 세션을 가진 채로 `/api/**`를 호출하면, gateway 필터가 사용자의 OAuth2 `OAuth2AuthorizedClient`에서 access token을 꺼내 `Authorization: Bearer <token>` 헤더로 자원 서버 요청에 붙여 준다. 우리가 직접 access token을 만지지 않아도 된다. 14장에서 "BFF는 토큰을 서버 측에 가둔다"고 말한 그 약속이, 이 한 줄로 실현된다.

둘째, 세션 쿠키 설정. `http-only: true`, `secure: true`, `same-site: lax`. 이 세 줄은 협상의 여지가 없다. XSS로 새지 않게 `HttpOnly`, HTTPS 외에는 전송되지 않게 `Secure`, CSRF의 첫 줄 방어로 `SameSite=Lax`. 11장과 9장에서 한 약속 그대로다.

이제 Security 설정. Reactive 환경이라는 사실을 잊지 말자.

```java
@Configuration
@EnableWebFluxSecurity
class BffSecurityConfig {

    @Bean
    SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        return http
            .authorizeExchange(ex -> ex
                .pathMatchers("/", "/index.html", "/assets/**", "/login", "/oauth2/**", "/login/oauth2/**")
                    .permitAll()
                .anyExchange().authenticated())
            .oauth2Login(Customizer.withDefaults())
            .logout(l -> l.logoutSuccessHandler(oidcLogoutSuccessHandler()))
            .csrf(ServerHttpSecurity.CsrfSpec::spa)   // 7.0 한 줄 (SPA-친화 모드)
            .headers(h -> h
                .hsts(hsts -> hsts.includeSubdomains(true).maxAge(Duration.ofDays(365)))
                .contentSecurityPolicy(csp -> csp.policyDirectives(
                    "default-src 'self'; script-src 'self'; object-src 'none'")))
            .build();
    }

    @Bean
    ServerLogoutSuccessHandler oidcLogoutSuccessHandler() {
        var handler = new OidcClientInitiatedServerLogoutSuccessHandler(clientRegistrationRepository);
        handler.setPostLogoutRedirectUri("{baseUrl}/");
        return handler;
    }

    private final ReactiveClientRegistrationRepository clientRegistrationRepository;
    BffSecurityConfig(ReactiveClientRegistrationRepository repo) {
        this.clientRegistrationRepository = repo;
    }
}
```

`csrf(... .spa)` 한 줄이 7.0에서 추가된 SPA-친화 CSRF 모드다. 이전에는 SPA가 `XSRF-TOKEN` 쿠키를 읽어 헤더로 다시 넣어 주는 패턴을 우리가 직접 빌드해야 했지만, 이제는 한 줄이 그 패턴을 표준으로 묶어 준다(레퍼런스 §6.6, §8.3). HSTS·CSP·HttpOnly 세션의 헤더 3종 세트는 9장에서 다룬 그대로다.

`oauth2Login(Customizer.withDefaults())`만으로 PKCE가 켜진다는 점은 6장에서 확인했다. confidential client에 PKCE를 굳이 다시 켜지 않아도 7.0의 기본 동작이 그렇게 한다. 6.x에서 올라온 코드가 explicit하게 끄고 있지만 않다면 신경 쓰지 않아도 된다.

로그아웃은 OIDC RP-initiated logout으로 잡았다. 사용자가 `/logout`을 누르면, BFF가 세션을 무효화하고 Keycloak의 end-session endpoint로 redirect한다. Keycloak 측에서도 SSO 세션이 닫히고, 브라우저는 다시 BFF 홈으로 돌아온다. 이 동선을 빠뜨리면, 사용자가 BFF에서는 로그아웃했는데 IdP에 가면 여전히 로그인 상태로 남아 있는 — 그러니까 다음번 `/login`에서 묻지도 따지지도 않고 통과되는 — 찜찜한 풍경이 생긴다.

여기까지 짠 BFF는 이미 가동된다. 브라우저가 `app.shopvault.com`을 처음 열면 정적 자원이 내려가고, SPA가 부팅한다. SPA가 `fetch('/api/me')`를 던지면 BFF가 인증을 요구하고, 사용자는 `/login`을 거쳐 Keycloak으로 redirect된다.

## 15.4 shop-api — 두 개의 `SecurityFilterChain`

이제 자원 서버다. 8장의 인가, 5장의 JWT·DPoP, 그리고 14장의 Actuator 격리가 한 자리에 모인다.

먼저 `application.yml`.

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.shopvault.com/realms/shopvault
          # JWKs URL은 issuer-uri의 OIDC discovery로 자동 결정

management:
  endpoints:
    web:
      exposure:
        include: health, info, prometheus
  server:
    port: 9001          # Actuator를 별도 포트로 격리 (14장 §14.5)
```

Actuator를 별도 포트로 빼는 건 14장에서 본 한국 우아한형제들 사례의 교훈이다. `env` 같은 endpoint가 같은 포트에 노출돼 외부에서 접근 가능했던 그 사고. 한 줄 분리로 막을 수 있는 일이라면, 막아 두는 편이 낫다.

이제 Security 설정. 두 개의 `SecurityFilterChain`을 짠다.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
class ShopApiSecurityConfig {

    /**
     * (1) Actuator 전용 체인 — 격리, 인증 없음(내부망 한정)
     *     별도 포트(9001)에서만 노출되므로 외부에서 닿지 않는다.
     */
    @Bean
    @Order(1)
    SecurityFilterChain actuatorChain(HttpSecurity http) throws Exception {
        return http
            .securityMatcher(EndpointRequest.toAnyEndpoint())
            .authorizeHttpRequests(a -> a.anyRequest().permitAll())
            .csrf(CsrfConfigurer::disable)
            .build();
    }

    /**
     * (2) API 본체 체인 — JWT + DPoP, stateless, scope/role 기반 인가
     */
    @Bean
    @Order(2)
    SecurityFilterChain apiChain(HttpSecurity http,
                                  JwtAuthenticationConverter jwtConverter) throws Exception {
        return http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers(HttpMethod.GET, "/api/products/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .oauth2ResourceServer(o -> o
                .jwt(j -> j.jwtAuthenticationConverter(jwtConverter)))
            .csrf(CsrfConfigurer::disable)
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .build();
    }

    /**
     * Keycloak realm role을 권한으로 매핑 + SCOPE_* 권한도 같이 살림.
     */
    @Bean
    JwtAuthenticationConverter jwtAuthenticationConverter() {
        var roles = new JwtGrantedAuthoritiesConverter();
        roles.setAuthoritiesClaimName("roles");
        roles.setAuthorityPrefix("ROLE_");

        var scopes = new JwtGrantedAuthoritiesConverter();   // 기본 scp/scope → SCOPE_*

        var conv = new JwtAuthenticationConverter();
        conv.setJwtGrantedAuthoritiesConverter(jwt -> {
            var combined = new ArrayList<GrantedAuthority>();
            combined.addAll(roles.convert(jwt));
            combined.addAll(scopes.convert(jwt));
            return combined;
        });
        return conv;
    }

    /**
     * audience 검증을 한 겹 더 (RFC 8725 §4.1 권고).
     */
    @Bean
    JwtDecoder jwtDecoder(OAuth2ResourceServerProperties props) {
        var decoder = NimbusJwtDecoder
            .withIssuerLocation(props.getJwt().getIssuerUri())
            .build();

        var withAud = new DelegatingOAuth2TokenValidator<>(
            JwtValidators.createDefaultWithIssuer(props.getJwt().getIssuerUri()),
            new JwtClaimValidator<List<String>>("aud",
                aud -> aud != null && aud.contains("shopvault-api")));
        decoder.setJwtValidator(withAud);
        return decoder;
    }
}
```

체인이 두 개라는 사실, `@Order`로 우선순위를 명시했다는 사실, 그리고 첫 체인이 `securityMatcher`로 Actuator만 잡고 두 번째 체인이 `/api/**`만 잡는다는 사실 — 이 셋이 핵심이다. 2장에서 본 "필터 체인은 `SecurityFilterChainProxy`가 첫 매칭만 사용한다"는 규칙이 여기서 작동한다. 두 체인은 서로의 영역에 발을 들이지 않는다.

`JwtAuthenticationConverter`는 두 가지 일을 한꺼번에 한다. Keycloak이 토큰에 넣어 준 `roles` 클레임을 `ROLE_*` 권한으로 매핑하고, 동시에 OAuth2 표준 `scope`/`scp` 클레임은 `SCOPE_*`로 매핑해 둔다. 이 둘이 동시에 권한 컬렉션에 들어가야, 다음 절의 메서드 보안이 `hasRole('ADMIN')`도 `hasAuthority('SCOPE_order:write')`도 함께 표현할 수 있다.

`JwtDecoder`를 직접 빈으로 등록해 `aud` validator를 더한 부분도 그냥 지나치지 말자. RFC 8725 §4.1이 audience 검증을 명시적으로 권고하고 있고, 우리는 그걸 한 줄 더 적어 준다. 토큰이 다른 자원 서버용으로 발급된 것을 우리 자원 서버가 받아 들이는 — 그러니까 "내가 받을 토큰이 아닌데도 받아 들이는" — 잠재적 사고 한 종류를 막는다.

이제 DPoP다. 5장에서 RFC 9449를 따라 살펴본 바로 그것이다. Spring Security 7은 DPoP-bound 토큰을 자원 서버 측에서 1급으로 처리한다(레퍼런스 §4.9). 한 줄을 더 얹자.

```java
http.oauth2ResourceServer(o -> o
    .jwt(j -> j.jwtAuthenticationConverter(jwtConverter))
    .dPoP(Customizer.withDefaults()));   // 7.0 신규
```

이 한 줄로 자원 서버는 매 요청의 `DPoP` 헤더를 검증한다. 토큰 안의 `cnf.jkt`(JWK SHA-256 thumbprint)와 DPoP proof JWT 안의 공개 키 thumbprint가 일치하는지, `htm`(HTTP method), `htu`(HTTP URI), `iat`, `jti`, `ath`(access token SHA-256 hash)가 적절한지를 본다. 이 검증이 통과하지 못하면 401이다. 토큰을 누군가 훔쳐 가도, DPoP 개인 키 없이는 쓰지 못한다. BFF 측에서도 access token을 자원 서버에 보내기 전에 DPoP proof를 매번 만들어 헤더에 붙여야 하는데, 이 부분은 Spring Security가 client 측에도 helper를 제공한다(레퍼런스 §4.9의 `NimbusJwtEncoder` 예제 참조). 단, 7.0 GA 시점 client 측 DPoP API의 시그니처는 미세 보강 가능성이 있으니, 출간 시점 docs를 한 번 더 확인하자.

> **결정의 기록.** ShopVault는 DPoP를 켜기로 했다. 5장 끝의 "DPoP 결정 기준"에서 본 그 결정이다. 결제 흐름이 끼어 있고, refresh 없는 access token이 BFF에서 자원 서버로 흐르며, 토큰 탈취로 단 한 번이라도 결제가 일어나면 곤란하기 때문이다. 단순한 게시판형 서비스라면 DPoP 없이 가도 무방하다. 모든 시스템에 DPoP가 답인 것은 아니다.

## 15.5 메서드 보안 — 서비스 계층에 인가를 새긴다

URL 인가만으로는 부족하다. 8장에서 다섯 층의 인가 모델을 따라 내려가며 본 그 사실이다. URL은 첫 번째 줄이고, 메서드 보안이 두 번째 줄이며, 도메인 객체 보안이 그 아래다.

ShopVault의 서비스 계층 한 단면을 보자.

```java
@Service
class OrderService {

    @PreAuthorize("hasAuthority('SCOPE_order:read') and hasRole('CUSTOMER')")
    public List<Order> myOrders(Authentication auth) { ... }

    @PreAuthorize("hasAuthority('SCOPE_order:write') and hasRole('CUSTOMER')")
    public Order place(NewOrder draft, Authentication auth) { ... }

    @PreAuthorize("hasRole('ADMIN')")
    public void cancel(long orderId, String reason) { ... }

    @PreAuthorize("hasRole('PAYMENT_ADMIN')")
    public Refund refund(long orderId, Money amount) { ... }
}
```

`@EnableMethodSecurity`가 `apiChain` 설정 클래스에 붙어 있으니, 이 어노테이션이 그대로 살아난다. 6.x 시절에 `@EnableGlobalMethodSecurity`를 같이 쓰던 코드라면, 함정 2(13장 13.4)에서 본 대로 정확히 한 군데로 통일해 두자. 두 어노테이션이 한 모듈 안에 섞이면 `@PreAuthorize`가 조용히 무력화되는 경우가 있다.

`refund` 같은 메서드에는 한 줄을 더 얹어 두면 좋다.

```java
@PreAuthorize("hasRole('PAYMENT_ADMIN') and hasAuthority('FACTOR_OTT')")
public Refund refund(long orderId, Money amount) { ... }
```

`FACTOR_OTT`라는 권한이 어디서 오는가? 7장에서 본 MFA factor 권한이다. 1차 패스워드 인증만 통과한 사용자는 `FACTOR_PASSWORD` 권한만 가지고, 2차 OTT까지 통과해야 `FACTOR_OTT`가 더해진다. 메서드 보안 한 줄로 "환불은 MFA를 통과한 관리자만"이라고 말할 수 있게 되는 거다. Spring 공식 블로그(2025-10-21)가 자랑스럽게 미는 모델 그대로다.

## 15.6 관리자 MFA — factor가 권한이 되는 모델

이제 관리자 측 흐름을 만들자. 일반 사용자는 패스워드 한 번이면 충분하지만, 관리자는 그렇게 두면 곤란하다. 7장에서 다룬 MFA를 여기에 얹는다.

기본 아이디어를 먼저 짚자. 7.0의 MFA는 "두 번째 인증 단계"를 별도 컴포넌트로 만들지 않는다. 대신 "각 factor를 통과했는지"를 권한(`FactorGrantedAuthority`)으로 표현한다. 인가 규칙이 "두 factor 모두 필요"라고 적으면, 사용자가 하나만 통과한 상태에서 그 URL을 부르려고 할 때 Spring Security가 자동으로 다음 factor 입력 페이지로 redirect한다. 인증 흐름의 추가 단계가 인가 규칙으로 표현된다는 게 핵심이다.

ShopVault의 관리자 동선은 Keycloak에 위탁하지 않고 자원 서버 측에서 직접 MFA를 받기로 했다고 가정하자. 실제로는 Keycloak에서 MFA를 끝낸 토큰을 받는 흐름이 더 일반적이지만, 7.0의 새 API를 한 번 체험해 보기 위해 자원 서버 측 MFA를 짜본다.

```java
@Configuration
@EnableMultiFactorAuthentication(authorities = {
    FactorGrantedAuthority.PASSWORD_AUTHORITY,
    FactorGrantedAuthority.OTT_AUTHORITY
})
class AdminMfaConfig {

    @Bean
    @Order(0)   // apiChain보다 먼저 매칭되도록
    SecurityFilterChain adminChain(HttpSecurity http,
                                    MagicLinkSender magicLinkSender,
                                    AuthorizationManagerFactory<RequestAuthorizationContext> mfa) throws Exception {
        return http
            .securityMatcher("/admin/**")
            .authorizeHttpRequests(a -> a
                .requestMatchers("/admin/refund/**")
                    .access(mfa.allAuthorities("FACTOR_PASSWORD", "FACTOR_OTT"))
                .anyRequest()
                    .access(mfa.allAuthorities("FACTOR_PASSWORD")))
            .formLogin(Customizer.withDefaults())
            .oneTimeTokenLogin(ott -> ott
                .tokenGenerationSuccessHandler(magicLinkSender::send))
            .build();
    }
}
```

해석해 보자. `@EnableMultiFactorAuthentication`이 두 가지 factor를 시스템에 등록한다. `adminChain`의 `securityMatcher("/admin/**")`은 관리자 페이지 전체를 잡고, `/admin/refund/**`만은 두 factor를 모두 요구하며, 나머지 관리자 페이지는 패스워드 한 단계만 요구한다.

관리자가 `/admin`에 처음 들어오면 패스워드 폼이 뜬다. 통과하면 `FACTOR_PASSWORD` 권한이 컨텍스트에 박힌다. 일반 관리자 페이지는 여기서 통과된다. 그런데 `/admin/refund/*`을 누르는 순간 인가 규칙이 `FACTOR_OTT`도 요구하기 때문에, Spring Security가 자동으로 OTT 발급 페이지로 redirect한다. 매직 링크가 메일로 날아오고, 관리자가 링크를 클릭해 OTT 토큰을 제출하면 `FACTOR_OTT`도 권한 컬렉션에 더해진다. 이제 환불 페이지가 열린다.

다음에 같은 관리자가 다시 환불 페이지에 들어올 때는, 세션 안에 두 factor 권한이 모두 살아 있으니 매끄럽게 통과된다. 한 번 통과한 factor는 세션 동안 유지된다. 단, 세션 만료나 명시적 로그아웃 뒤에는 처음부터 다시 시작이다.

이 모델이 우리 머리에 박혔으면 좋겠다. **factor는 추가 단계가 아니라 권한이다.** 그래서 메서드 보안에서도 한 줄로 `hasAuthority('FACTOR_OTT')`를 적을 수 있고, URL 규칙에서도 같은 어휘를 쓴다. 인증과 인가가 한 어휘로 묶이는 순간이다.

`MagicLinkSender`는 우리가 직접 구현해야 한다. 7.0이 라이브러리로 매직 링크 전송 자체는 제공하지 않는다(레퍼런스 §4.7). 메일 발송이든 SMS든 우리 도메인의 책임이다. 한 인터페이스만 보여 두자.

```java
@Component
class MagicLinkSender implements OneTimeTokenGenerationSuccessHandler {

    private final MailService mail;

    @Override
    public void handle(HttpServletRequest req, HttpServletResponse res,
                       OneTimeToken token) throws IOException {
        var link = UriComponentsBuilder.fromHttpUrl(req.getRequestURL().toString())
            .replacePath("/login/ott")
            .queryParam("token", token.getTokenValue())
            .build().toUriString();

        var username = token.getUsername();
        mail.send(username + "@shopvault.com",
            "ShopVault 관리자 추가 인증",
            "다음 링크로 5분 안에 인증을 완료해 주세요: " + link);
    }
}
```

`OneTimeTokenService`는 빈으로 등록해 두자. 운영 환경이라면 `InMemoryOneTimeTokenService`가 아니라 `JdbcOneTimeTokenService`로. 토큰 저장이 메모리에만 있으면 다중 인스턴스 환경에서 망가진다.

```java
@Bean
OneTimeTokenService ottService(JdbcOperations jdbc) {
    return new JdbcOneTimeTokenService(jdbc);
}
```

## 15.7 인증 흐름 1 — 일반 사용자 로그인 (SPA → BFF → Keycloak)

자, 이제 흐름을 따라가 보자. 첫 번째 시나리오는 가장 흔한 일반 사용자 로그인이다.

```
[Browser]                  [shop-bff]                 [Keycloak]
   │                            │                          │
   │── GET /app ───────────────▶│                          │
   │◀── 200 OK (SPA bundle) ────│                          │
   │                            │                          │
   │── GET /api/me (no cookie) ▶│                          │
   │                            │ (no session → 401)        │
   │◀── 401 + Location: /login ─│                          │
   │                            │                          │
   │── GET /login ─────────────▶│                          │
   │                            │── 302 to /oauth2/         │
   │                            │    authorization/keycloak │
   │◀── 302 (redirect) ─────────│                          │
   │                            │                          │
   │── GET /oauth2/             │                          │
   │   authorization/keycloak ─▶│                          │
   │                            │  PKCE code_verifier      │
   │                            │  생성 + 세션에 저장       │
   │                            │  state, nonce 생성        │
   │◀── 302 to Keycloak ────────│                          │
   │   (code_challenge=S256...)                            │
   │                            │                          │
   │── GET /realms/shopvault/   │                          │
   │   protocol/openid-connect/ │                          │
   │   auth?... ──────────────────────────────────────────▶│
   │                            │       (Keycloak 로그인 폼) │
   │◀──────────────────────────────────────── 200 form ────│
   │                            │                          │
   │── POST credentials ──────────────────────────────────▶│
   │                            │       (검증, code 발급)   │
   │◀───────────────────── 302 to /login/oauth2/code/... ──│
   │                            │                          │
   │── GET /login/oauth2/       │                          │
   │   code/keycloak?code=...─▶│                          │
   │                            │── POST /token ──────────▶│
   │                            │   (code + verifier)      │
   │                            │◀── access + id + refresh ─│
   │                            │  세션 생성, 토큰 보관      │
   │                            │  Set-Cookie:              │
   │                            │   SHOPVAULT_SESSION=...   │
   │◀── 302 to / + cookie ──────│                          │
   │                            │                          │
   │── GET /api/me (cookie) ───▶│                          │
   │                            │── GET /api/me            │
   │                            │   Authorization: Bearer ─▶ shop-api
   │                            │      + DPoP proof        │
   │                            │◀────────────── {user} ────│
   │◀── 200 {user} ─────────────│                          │
```

이 그림이 14장 BFF 패턴의 약속을 한 시퀀스로 풀어낸 것이다. 브라우저는 access token을 한 번도 손에 쥐지 않는다. 그저 HttpOnly 세션 쿠키 하나로 BFF와 대화할 뿐이고, 토큰은 BFF의 세션 안에 갇혀 있다. 14장에서 우리가 한 약속이 그것이었다.

여기서 짚을 만한 작은 디테일이 몇 가지 있다.

첫째, `code_verifier`는 BFF의 세션에 저장된다. PKCE의 의미가 "code 탈취만으로 토큰을 받지 못하게 한다"인데, BFF는 자기 세션 안에 verifier를 보관해 두었다가 token endpoint를 호출할 때 함께 보낸다. 6.x까지는 confidential client에서 PKCE를 explicit하게 켜야 했지만 7.0의 기본이 바뀌었다(레퍼런스 §4.6, §8.5). 6.x에서 올라온 코드가 명시적으로 `setPkce(false)` 같은 짓을 하고 있지 않다면, 우리가 한 줄 더 적지 않아도 PKCE가 동작한다.

둘째, `state`는 CSRF 방어, `nonce`는 ID Token replay 방어다. 둘 다 Spring Security가 자동으로 만들고 자동으로 검증한다. 우리가 손댈 일은 거의 없다.

셋째, 마지막 응답의 `302 to /`. 사용자는 `/login`에서 시작했을 수도 있고, `/orders/123`에서 401을 만나 `/login`으로 끌려왔을 수도 있다. Spring Security는 처음 401이 일어난 그 자리를 `savedRequest`로 기억해 두었다가 인증이 끝나면 그쪽으로 다시 보내 준다. 매끄러운 UX의 작은 비밀이다.

## 15.8 인증 흐름 2 — 관리자 MFA 로그인

두 번째 시나리오. 환불 권한을 가진 `payment-admin` 사용자가 환불 페이지를 누른다.

```
[Browser]              [shop-bff]            [shop-api admin chain]
   │                       │                          │
   │── GET /admin/refund ─▶│                          │
   │                       │   (no session → 401, redirect /login)
   │                       │                          │
   │── /login flow with    │                          │
   │   Keycloak (앞과 동일) │                          │
   │                       │                          │
   │   세션 생성, 토큰 보관 │                          │
   │   (Keycloak의 roles 클레임에 admin, payment-admin) │
   │                       │                          │
   │── GET /admin/refund ─▶│── relay ────────────────▶│
   │                       │                          │ 토큰 검증 OK
   │                       │                          │ 권한: ROLE_PAYMENT_ADMIN
   │                       │                          │       FACTOR_PASSWORD
   │                       │                          │ /admin/refund 인가 규칙:
   │                       │                          │  PASSWORD ∧ OTT
   │                       │                          │ → factor 부족
   │                       │                          │
   │                       │◀── 302 to /login/ott ────│
   │◀── 302 to /login/ott ─│                          │
   │                       │                          │
   │── POST /login/ott ───▶│── /login/ott ───────────▶│
   │   (사용자명만)         │                          │ OneTimeTokenService
   │                       │                          │ 토큰 생성
   │                       │                          │ MagicLinkSender 호출
   │                       │                          │
   │            ✉ 이메일 도착 (링크 안에 token=...)       │
   │                       │                          │
   │── 링크 클릭 ──────────▶│── /login/ott?token=... ─▶│
   │                       │                          │ 토큰 검증 OK
   │                       │                          │ FACTOR_OTT 권한 부여
   │                       │                          │ → 두 factor 충족
   │                       │◀── 302 to /admin/refund ─│
   │◀── 302 to /admin/    ──│                          │
   │   refund               │                          │
   │── GET /admin/refund ─▶│── relay ────────────────▶│ 통과
   │◀── 200 ────────────────│◀── 200 ──────────────────│
```

이 흐름을 한 줄로 요약하면 이렇다. **인가 규칙이 "factor 부족"을 발견하는 순간, Spring Security가 적절한 인증 흐름으로 자동 분기시킨다.** 우리가 직접 "이 사용자는 OTT를 더 받아야 한다"는 분기를 짤 필요가 없다. `@EnableMultiFactorAuthentication`이 그 분기를 시스템에 박아 두었기 때문이다.

7장에서 본 그림이 이 자리에서 실제로 살아 돌아간다. 그때 약속처럼, factor는 추가 단계가 아니라 권한이다. 같은 어휘로 인증과 인가가 묶인다.

## 15.9 인증 흐름 3 — SPA → BFF → API 호출

세 번째 시나리오. 가장 짧지만 가장 자주 일어나는 흐름이다.

이미 로그인을 마친 사용자가 SPA 안에서 `장바구니에 담기`를 누른다. SPA는 `POST /api/cart`를 던진다. 그게 전부다. SPA 측 코드에서 토큰을 다루는 줄은 하나도 없다.

```javascript
// SPA 측 — 그냥 fetch 한 줄
await fetch('/api/cart', {
  method: 'POST',
  body: JSON.stringify({ productId, qty }),
  headers: { 'Content-Type': 'application/json', 'X-XSRF-TOKEN': csrfToken },
  credentials: 'same-origin'
});
```

BFF로 들어온 이 요청은 다음을 거친다.

1. `same-origin`이므로 세션 쿠키가 자동으로 함께 온다.
2. CSRF 토큰을 헤더에서 본다 — `csrf(... .spa)`가 받아 주는 표준 패턴.
3. 인증 체크 — 세션에서 `OAuth2AuthorizedClient` 발견.
4. Gateway의 `TokenRelay` 필터가 `OAuth2AuthorizedClient`에서 access token을 꺼내 `Authorization: Bearer <token>`을 만든다.
5. 같은 자리에서 DPoP proof JWT를 만들어 `DPoP: <proof>` 헤더를 더한다. (DPoP 키는 BFF가 보관)
6. `shop-api`로 forward.

`shop-api` 측에서는 다음을 거친다.

1. `apiChain`의 `oauth2ResourceServer.jwt(...)`이 JWT 서명·발급자·audience·만료를 검증.
2. `dPoP(...)`가 DPoP 헤더 검증 — `cnf.jkt` 일치, `htm/htu/iat/jti/ath` 검증.
3. `JwtAuthenticationConverter`가 `roles`·`scope` 클레임을 `ROLE_*`·`SCOPE_*` 권한으로 만들어 `Authentication`에 박는다.
4. URL 인가 — `/api/cart`는 `anyRequest().authenticated()`에 걸려 통과.
5. 컨트롤러 → `OrderService.place(...)` 호출.
6. 메서드 보안 — `@PreAuthorize("hasAuthority('SCOPE_order:write') and hasRole('CUSTOMER')")` 검증.
7. 비즈니스 로직 실행, 응답 반환.

브라우저에서 본 한 줄의 `fetch`는 이 일곱 단계를 통과한 결과로 200이 돼서 돌아온다. 한 시스템 안에서 이렇게 많은 결정이 한 요청에 묶여 있다는 사실을, 우리는 가끔 잊는다. 잊지 말자. 인증과 인가는 같이 산다.

여기까지 따라온 독자에게 작은 보너스 질문 하나. **이 흐름에서 가장 위험한 한 줄은 어디인가?** 잠시 멈춰 답을 떠올려 보자.

답은 BFF의 세션 쿠키 설정이다. `SameSite`, `Secure`, `HttpOnly` 셋 중 어느 하나라도 빠지면, 이 잘 만든 시스템이 한 줄로 무너진다. 9장과 10장에서 길게 다뤘던 그 이유 때문에. SPA에서 토큰을 다루지 않게 만들어 둔 모든 노력이 — `HttpOnly`가 없으면 XSS 한 번으로 세션 쿠키가 새 나갔을 때 — 다시 흔들린다. 한 줄을 보자.

```yaml
server:
  servlet:
    session:
      cookie:
        same-site: lax        # 비워 두지 말 것
        http-only: true       # 비워 두지 말 것
        secure: true          # 비워 두지 말 것
```

이 세 줄이 한 시스템의 보안에서 마지막 보루다. 자주 잊고 자주 깨진다.

## 15.10 외부 결제 호출 — `@HttpExchange` + `@ClientRegistrationId`

마지막 한 조각. `shop-api`가 외부 결제 게이트웨이를 호출할 때다. 사용자가 끼지 않는 client credentials 흐름이고, 우리는 access token을 매번 직접 만들고 싶지 않다.

Spring Boot 4 / Spring 7의 `@HttpExchange`와 Spring Security 7의 `@ClientRegistrationId`가 만나면 이렇게 깔끔해진다.

```java
@HttpExchange("https://api.payment-gateway.com")
@ClientRegistrationId("payment")
interface PaymentClient {

    @PostExchange("/charges")
    ChargeResult charge(@RequestBody ChargeRequest req);

    @PostExchange("/refunds")
    RefundResult refund(@RequestBody RefundRequest req);
}
```

그리고 `application.yml`에 결제용 client registration을 한 자리에 적어 둔다.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          payment:
            client-id: shopvault-payment-client
            client-secret: ${PAYMENT_CLIENT_SECRET}
            authorization-grant-type: client_credentials
            scope: payment:charge
        provider:
          payment:
            token-uri: https://auth.shopvault.com/realms/shopvault/protocol/openid-connect/token
```

이걸로 끝이다. `@HttpExchange` 인터페이스를 빈으로 등록해 두면(`HttpServiceProxyFactory` 한 줄), Spring Security가 호출 시점에 client credentials 흐름으로 access token을 받아 자동으로 `Authorization: Bearer ...` 헤더에 넣어 준다. 토큰 만료가 가까워지면 백그라운드에서 갱신한다. 우리는 그저 인터페이스 메서드를 부를 뿐이다.

```java
@Service
class RefundFlow {
    private final PaymentClient payment;

    @PreAuthorize("hasRole('PAYMENT_ADMIN') and hasAuthority('FACTOR_OTT')")
    public Refund refund(long orderId, Money amount) {
        var result = payment.refund(new RefundRequest(orderId, amount));
        // ... domain logic
    }
}
```

이 한 메서드가 책 전체의 결을 한 자리에 묶는다. 메서드 보안(8장), MFA factor(7장), 외부 OAuth2 호출(6장), 그리고 그 호출의 깔끔한 추상화(`@HttpExchange`). 우리가 1장에서 출발해 여기까지 온 거리를, 이 짧은 메서드 하나가 정직하게 비추어 준다.

## 15.11 운영 체크리스트 — 빌드보다 오래 가는 것들

코드가 끝났다고 시스템이 끝나는 건 아니다. ShopVault가 운영에 들어가기 전에 한 번은 짚어야 할 것들을 묶어 두자. 14장의 운영 절을 떠올리며 적는다.

- [ ] **인증 이벤트 audit.** `AuthenticationSuccessEvent`, `AuthenticationFailureBadCredentialsEvent`, `LogoutSuccessEvent` 같은 Spring의 application event를 `ApplicationListener`로 받아 audit 로그에 적자. IP, 사용자명, 시각, factor 정보를 묶어. 사고가 나면 첫 번째로 펴 보게 된다.
- [ ] **JWK 회전 schedule.** Keycloak 측 JWK는 주기적으로 회전된다. 자원 서버의 `NimbusJwtDecoder`는 JWKs URL을 캐시한다. 새 키가 등장하면 `kid`로 자동 fetch하지만, 캐시 TTL이 너무 길면 회전 직후 잠깐 401이 폭주할 수 있다. `JwkSourceBuilder`로 캐시 정책을 명시적으로 잡아 두자(레퍼런스 §6.8).
- [ ] **모니터링 대시보드.** `prometheus` endpoint를 통해 Spring Security의 인증/인가 카운터를 노출하자. `spring.security.filter.invocations`, `spring.security.authentication.{success,failure}` 같은 지표가 핵심. 인증 실패율이 평소의 10배로 튀면 알람.
- [ ] **Actuator 격리.** `shop-api`의 `application.yml`에서 본 `management.server.port: 9001`이 살아 있는지 배포 환경 변수에서 다시 한번 확인. 같은 포트에 같이 노출되어 있으면, 14장에서 본 사고의 길이 열린다(레퍼런스 §7.5).
- [ ] **CSP 정책 점검.** BFF의 `Content-Security-Policy` 헤더가 SPA의 외부 폰트·이미지·CDN을 정확히 반영하는지. 너무 느슨하면 XSS 방어가 약해지고, 너무 빡빡하면 SPA가 깨진다.
- [ ] **deprecation warning 0.** 빌드 로그에서 Spring Security 관련 deprecation warning이 0건인지. 7.0에서 deprecation으로 표시된 API는 7.1에서 빠질 수 있다. 출시 일정을 따라가는 팀이라면 warning을 무시하지 말자.
- [ ] **테스트 회귀 안전망.** 12장에서 만든 인증/인가 통합 테스트가 CI에 묶여 있는지. 적어도 다섯 가지는 — 일반 사용자 정상 로그인, 관리자 MFA 흐름, 권한 부족 시 403, JWT 만료 시 401, DPoP 헤더 누락 시 401 — 회귀로 잡아 두자.
- [ ] **시크릿 관리.** `KEYCLOAK_BFF_SECRET`, `PAYMENT_CLIENT_SECRET`이 어디 있는가. application.yml에 평문으로 들어가 있으면 끔찍한 일이다. Vault, AWS Secrets Manager, Kubernetes Secret 중 하나여야 한다.

이 체크리스트는 ShopVault의 한 PR에 그대로 댓글로 붙여 둘 만한 분량이다. 한 번 만들어 두고, 새 서비스가 올라올 때마다 다시 펴 보자.

## 15.12 한 권의 어휘가 한 시스템에 녹았다 — 회고

자, 이 책을 처음 펼쳤을 때를 기억해 보자. 1장에서 빌드가 한 줄도 통과하지 못하던 그 화면. `WebSecurityConfigurerAdapter`가 사라졌다는 사실 앞에서 잠시 막막했던 그 순간. 책의 처음과 끝을 한 화면에 놓고 보면, 우리가 얼마나 멀리 왔는지 정직하게 보인다.

이 마지막 시나리오 안에서 14개 챕터의 어휘가 어떻게 살아 있는지 한 번만 정리해 두자. 길지 않게.

- **1장**의 큰 그림 다섯 개 — 레거시 DSL 제거, 인가 두뇌 교체, Authorization Server 흡수, 모던 인증 1급화, 토대 라이브러리 교체 — 이 다섯 갈래가 ShopVault의 모든 코드 줄에 흩어져 있다.
- **2장**의 필터 체인 순서는 `shop-api`의 두(아니, 세) `SecurityFilterChain`이 `@Order`로 줄 세우는 그 자리에 정확히 박혀 있다.
- **3장**의 컴포넌트 위임 모델(`AuthenticationManager` → `Provider`)은 `oauth2ResourceServer.jwt(...)`의 내부에서 묵묵히 돈다.
- **4장**의 폼 로그인은 관리자 MFA의 1차 단계에서 살아 있다.
- **5장**의 JWT 자원 서버와 DPoP는 `apiChain`의 `oauth2ResourceServer.jwt(...).dPoP(...)` 한 줄에서 만난다.
- **6장**의 OAuth2 Client + OIDC는 BFF의 `oauth2Login(Customizer.withDefaults())`이 그대로 들고 있다.
- **7장**의 OTT·MFA는 관리자 환불 흐름 안에서 factor 권한 모델 그대로 살아난다.
- **8장**의 인가 다섯 층은 URL 인가 + 메서드 보안 + (필요 시) 도메인 객체 보안의 결합으로 ShopVault의 백엔드에 새겨졌다.
- **9장**의 CSRF·CORS·헤더는 BFF의 `csrf(... .spa)` + HSTS + CSP에 묶였다.
- **10장**의 세션·쿠키는 BFF의 `HttpOnly·Secure·SameSite` 한 줄에 응축됐다.
- **11장**의 Reactive 보안은 Spring Cloud Gateway 위에서 `SecurityWebFilterChain`이 도는 그 자리에서 작동한다.
- **12장**의 테스팅 패턴은 운영 체크리스트의 회귀 안전망 다섯 시나리오로 들어갔다.
- **13장**의 마이그레이션 어휘는 이 책의 모든 코드가 7.0 GA 시그니처로 적혔다는 사실 자체로 증명된다.
- **14장**의 Zero Trust·BFF·운영 어휘는 ShopVault의 전체 아키텍처와 운영 체크리스트 그 자체다.

한 권의 어휘가 한 시스템에 다 녹았다. 책 한 권이 책장에 꽂힌 채로 끝나지 않고, 우리가 손으로 짠 코드 안에 살아남았다. 그 사실이 이 책이 마지막에 우리에게 줄 수 있는 가장 솔직한 선물이다.

## 15.13 책을 덮은 뒤 — 어디서 더 읽을 것인가

이 책은 여기까지다. 그러나 Spring Security는 여기서 멈추지 않는다. 7.1.x milestone이 이미 굴러가고 있고, 8.0이 어딘가 먼 길 위에 있다. 우리가 책을 덮은 뒤 어디서 더 읽으면 좋을지 짧게 적어 두자.

**가장 먼저 들를 곳은 공식 docs다.** `docs.spring.io/spring-security/reference/whats-new.html`은 7.0 GA 이후의 변경이 차곡차곡 쌓이는 자리다. 이 책이 출간된 뒤 새로 들어오는 API는 거기서 가장 빠르게 본다. 그다음은 Spring 공식 블로그(`spring.io/blog`)다. 큰 변화가 있을 때마다 팀이 글을 올린다. 2025-10-21의 MFA 글이 좋은 예다.

**표준 문서도 같이 펴자.** RFC 9700(OAuth 2.0 Security BCP), RFC 8725(JWT BCP), RFC 9449(DPoP), NIST SP 800-207(Zero Trust). 이 네 개 문서가 이 책 전체의 베이스 라인이다. Spring Security는 이 표준들의 한국어 구현체에 가깝다 — 표준을 같이 읽으면, 라이브러리의 다음 행보를 미리 짐작할 수 있다.

**검증된 저자 블로그 묶음.** Baeldung(`baeldung.com`)은 7.0 API의 코드 예제가 가장 빠르게 올라온다. Curity(`curity.io`)의 token handler pattern 시리즈는 BFF를 더 깊게 보고 싶을 때. Dimitri Mes의 블로그는 7.0 deep-dive가 자주 올라온다. 한국어 자료는 — 2025년 말 시점 아직 deep-dive가 적다. velog 단편글이 시행착오 사례로는 가치가 있지만, 어휘를 잡는 자료로는 한계가 있다. 1~2년 안에 카카오/토스 기술블로그에서 7.x deep-dive가 올라올 것을 기대해 보자.

**7.1.x 추적은 GitHub로.** `github.com/spring-projects/spring-security`의 milestone 페이지가 가장 빠르다. issue tracker의 `team/oauth2`, `team/web-security` 라벨을 follow해 두면, 책에서 다룬 API의 추가 보강이 일어날 때 알람이 온다. 이 책 본문이 "7.0 GA 기준"이라 못 박은 부분이 7.1.x에서 어떻게 보강되는지, 거기서 직접 확인하자.

## 15.14 마무리 — 그리고 이 책을 덮는 한 마디

길고 긴 여행이었다. 솔직히 말하면, 이 책을 쓰는 사람의 자리에서도 마지막 장을 쓰는 순간이 가장 후련하다. 1장에서 약속한 모든 것이 이제 우리 손 안에 있다. Spring Security 7.0의 큰 그림, 함정 5건, 5장에 걸친 인증 시나리오, 8장의 인가, 횡단 관심사 셋, Reactive, 테스팅, 마이그레이션, 트렌드, 그리고 통합. 책 한 권이 한 도구의 GA를 따라가는 한 사이클을 닫았다.

기억해 두자. 보안은 단번에 끝나는 일이 아니다. 표준은 매년 갱신되고, 라이브러리는 minor마다 깎이고, 함정은 새로 생긴다. 이 책이 마지막에 줄 수 있는 가장 정직한 약속은 "당신이 이 책을 덮은 시점부터 6개월 안에 7.1.x 안에서 무언가가 바뀐다"는 사실이다. 그 변화를 두려워하지 말자. 우리가 1~14장에서 박아 둔 어휘가 그대로 살아 있으면, 6개월 뒤에 바뀐 API의 시그니처를 만났을 때 우리는 "아, 이 자리에 새 도구가 들어왔구나"라고 즉시 알아본다. 이 책이 정말 약속하고 싶었던 것은 그것이다. 코드 한 줄이 아니라 어휘 한 단어. 시그니처가 아니라 의미. 그래서 라이브러리가 바뀌어도 우리가 같이 바뀔 수 있다.

ShopVault는 가상의 가게지만, 그 가게의 코드를 손에 쥔 우리는 가상이 아니다. 이 책을 덮고 자기 팀의 코드로 돌아갔을 때, 우리는 이전과는 조금 다른 눈으로 그 코드를 본다. `SecurityFilterChain` 한 줄 앞에서 잠시 멈추고, 두 체인으로 나눌 자리를 가늠해 본다. `localStorage`에 JWT가 들어가 있는 자리에서는 가슴이 잠시 답답해진다. `WebSecurityConfigurerAdapter`라는 단어가 PR 어딘가에서 보이면 손이 자연스럽게 그 줄을 들어낸다. 그 작은 변화가 사실은 이 책이 노린 가장 정확한 효과다.

이 책을 덮고 무엇을 만들지는 이제 당신에게 달렸다. 그리고 그것이 가장 즐거운 일이다.

— 끝.

---

# 맺음말 — 책을 덮는 독자에게

길고 긴 책이었다.

15장의 마지막 단락에서 적은 그 한 줄을 한 번만 더 적어 두고 싶다. **"코드 한 줄이 아니라 어휘 한 단어. 시그니처가 아니라 의미."** 이 책이 정말 약속하고 싶었던 것은 그것이다.

Spring Security 7.0은 2025년 11월에 GA됐고, 우리는 그 GA의 첫 빌드에서 빨간 줄을 마주했다. 그 빨간 줄을 푸는 일이 단순한 메서드 이름 치환이 아니라 어휘 단위의 재정렬이라는 사실을, 책의 어딘가에서 한 번쯤은 체감했기를 바란다. `WebSecurityConfigurerAdapter`가 사라진 자리에는 `SecurityFilterChain` 빈이 들어선 게 아니라 **"누가 무엇을 어떤 자리에서 결정하는가"** 의 모델이 다시 그려졌다. 그 모델을 손에 쥐면, 6개월 뒤 7.1.x에서 시그니처가 또 미세하게 바뀌어도 우리는 "아, 이 자리에 새 도구가 들어왔구나"라고 즉시 알아본다.

그래서 책을 덮은 뒤 무엇을 해야 하는가?

**작은 일부터 시작하자.** 자기 팀 코드 베이스를 한 번 펴서, 첫째로 `grep -r "@EnableGlobalMethodSecurity" src/`를 돌려 보자. 0건이 나오면 안심. 한 건이라도 나오면 그 자리에서 13장의 마이그레이션 절로 다시 가자. 둘째로 SPA의 토큰 저장 위치를 확인해 보자. `localStorage`에 JWT가 들어가 있다면 5장의 BFF 절을 다시 펴자. 셋째로 운영 중인 `SecurityFilterChain` 빈이 한 개인지 두 개인지 보자. 한 개라면 8장의 두 체인 분리 절을 다시 펴자. 이 세 가지가 가장 흔한 시작점이다.

**그리고 어휘를 동료들과 나누자.** 이 책이 박은 어휘 — 필터 11종의 자리, `AuthorizationManager`의 5종 구현체, OWASP A01·A02·A07, Zero Trust 원칙 4·6, sender-constrained 토큰, factor를 권한으로 표현하는 MFA — 가 동료의 입에서 같이 나오기 시작하면, 코드 리뷰의 풍경이 달라진다. PR 디스커션의 단어가 정확해지고, 단어가 정확해지면 결정이 정확해진다. 그게 코드 베이스를 오래 가게 만드는 일이다.

**책 너머의 자료도 함께 읽자.** 15.13절에 어디서 더 읽을지 정리해 두었다. 공식 docs의 `whats-new.html`이 출간 이후 추가된 변경의 첫 정착지다. RFC 9700·8725·9449, NIST SP 800-207의 원문도 이 책의 베이스 라인이다. 1~2년 안에 카카오·토스 같은 한국 기술블로그에서 7.x deep-dive가 올라올 것을 기대해 보자.

그리고 마지막으로 — 이 책이 닿지 못한 자리가 있다는 사실도 잊지 말자. 1.5절의 "이 책이 다루지 않는 것" 다섯 가지는 정직한 한계다. Spring Authorization Server 서버 측 깊은 운영, GraphQL/gRPC 보안, 모바일 앱 측 보안, MDM/디바이스 신원, K8s Service Mesh와의 mTLS 통합. 그 영역에는 다른 책들이 있다. 그 책들도 함께 펴자.

자, 정말 책을 덮을 시간이다.

이 책을 덮고 무엇을 만들지는, 이제 당신에게 달렸다. 그리고 그것이 가장 즐거운 일이다.

— 끝.

---

# 부록 A. 마이그레이션 체크리스트 한 페이지

5.x/6.x 코드를 7.0으로 옮겨야 하는 시니어 개발자가 한 페이지로 들고 다닐 수 있는 체크리스트다. 13장의 본격 답을 한 화면에 압축했다.

## 13장 핵심 5건

| # | 함정 | grep / 진단 | 답 |
|---|------|-------------|-----|
| 1 | `WebSecurityConfigurerAdapter` 잔재 | `grep -r "WebSecurityConfigurerAdapter" src/` | `SecurityFilterChain` 빈으로 분리. 13.1·13.3 |
| 2 | `@EnableGlobalMethodSecurity` 잔존 | `grep -r "@EnableGlobalMethodSecurity" src/` | `@EnableMethodSecurity`로 교체. `@PreAuthorize`가 조용히 죽는 함정. 8.2·13.4 |
| 3 | `.and()` 체이닝 | 컴파일 에러로 즉시 노출 | 람다 DSL로 재작성. 1.6·13.2 |
| 4 | `antMatchers`/`mvcMatchers` 혼용 | 컴파일 에러 + 코드 검색 | `requestMatchers(...)`로 통일. 13.5 |
| 5 | `WebSecurityCustomizer` 누락 | 정적 자원에 필터가 다 태워지는 비효율 | `WebSecurityCustomizer`로 ignore. `permitAll`과 의미가 다르다. 4.7·13.6 |

## 6단계 PR 분할

운영을 깨지 않고 7.0으로 옮기는 가장 안전한 길.

- **PR 1.** Spring Boot 6.5로 patch. `build.gradle`의 버전 숫자만. deprecated 경고만 뜬다. CI 초록 → 운영 배포.
- **PR 2.** `./gradlew rewriteRun`(OpenRewrite). 람다 DSL·`requestMatchers`·`authorizeHttpRequests` 자동 치환. CI 초록 → 운영 배포.
- **PR 3.** 손 변환 잔여분. `WebSecurityConfigurerAdapter`·`@EnableGlobalMethodSecurity`·`WebSecurityCustomizer` 누락 등 사람이 봐야 할 곳. 모듈별로 더 쪼개도 좋다. CI 초록 → 운영 배포.
- **PR 4.** `-Werror`로 deprecation 경고 0 영구화. CI에 박는다. CI 초록 → 운영 배포.
- **PR 5.** Spring Boot 4.0.x로 점프. 빨갛게 변하는 곳이 거의 없어야 정상. CI 초록 → 운영 배포.
- **PR 6 이후.** SAML/LDAP/Authorization Server 영역별 정리. 사용처가 있다면 분리 PR.

각 PR은 작고, 리뷰 가능하고, 회귀가 생기면 단일 PR을 revert하면 끝난다. 한 번에 모두 바꾸려는 충동이 들 때마다, 이 6단계 분할 PR을 떠올리자.

## 자동화 한 줄

```bash
# OpenRewrite 6.4/6.5 deprecation 자동 치환
./gradlew rewriteRun \
  -Dorg.openrewrite.recipe=org.openrewrite.java.spring.security6.UpgradeSpringSecurity_6_5
```

## CI에 박는 두 줄

```yaml
# build.gradle.kts
tasks.withType<JavaCompile> {
    options.compilerArgs.addAll(listOf("-Xlint:deprecation", "-Werror"))
}
```

deprecation 0이 영구화되면, 다시는 함정이 PR로 들어오지 않는다.

---

# 참고문헌

본 책 본문에서 인용한 모든 출처를 분류해 정리한다. URL은 2026년 5월 시점에 접근 확인됐다. 출간 후 일부 링크가 변동될 수 있으니, 핵심 문서는 제목·저자로 재검색 가능하도록 표기했다.

## 공식 문서 — Spring 팀

- Spring Security Reference — What's New in 7.0. https://docs.spring.io/spring-security/reference/whats-new.html
- Spring Security Migration Guide. https://docs.spring.io/spring-security/reference/migration/index.html
- Servlet Architecture. https://docs.spring.io/spring-security/reference/servlet/architecture.html
- Authorization Architecture. https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html
- Method Security. https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html
- Passkeys (WebAuthn). https://docs.spring.io/spring-security/reference/servlet/authentication/passkeys.html
- One-Time Token Login. https://docs.spring.io/spring-security/reference/servlet/authentication/onetimetoken.html
- Multi-Factor Authentication. https://docs.spring.io/spring-security/reference/servlet/authentication/mfa.html
- DPoP Tokens. https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/dpop-tokens.html
- OAuth2 Resource Server — JWT. https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html
- WebFlux Configuration. https://docs.spring.io/spring-security/reference/reactive/configuration/webflux.html
- CSRF. https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html

## Spring 공식 블로그

- "Spring Security 7.0 GA" (2025-11-17). https://spring.io/blog/2025/11/17/spring-security-releases/
- "Spring Authorization Server moving to Spring Security 7.0" (2025-09-11). https://spring.io/blog/2025/09/11/spring-authorization-server-moving-to-spring-security-7-0/
- "Multi-Factor Authentication in Spring Security 7" (2025-10-21). https://spring.io/blog/2025/10/21/multi-factor-authentication-in-spring-security-7/
- "Spring Security Lambda DSL" (2019-11-21). https://spring.io/blog/2019/11/21/spring-security-lambda-dsl/

## 표준·RFC·W3C·NIST·OWASP

- RFC 9700. *OAuth 2.0 Security Best Current Practice* (2025-01). https://datatracker.ietf.org/doc/rfc9700/
- RFC 8725 / BCP 225. *JSON Web Token Best Current Practices*. https://www.rfc-editor.org/rfc/rfc8725.html
- RFC 9449. *OAuth 2.0 Demonstrating Proof of Possession (DPoP)*. https://www.rfc-editor.org/rfc/rfc9449.html
- RFC 8705. *OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens*. https://www.rfc-editor.org/rfc/rfc8705.html
- RFC 7807. *Problem Details for HTTP APIs*. https://www.rfc-editor.org/rfc/rfc7807.html
- OAuth 2.1 Draft (IETF). https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/
- W3C WebAuthn Level 3 Working Draft. https://www.w3.org/TR/webauthn-3/
- FIDO Alliance Specifications. https://fidoalliance.org/specifications/
- NIST SP 800-207. *Zero Trust Architecture*. https://csrc.nist.gov/pubs/sp/800/207/final
- OWASP Top 10:2021 — A01 Broken Access Control. https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/
- OWASP Top 10:2021 — A02 Cryptographic Failures. https://owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/
- OWASP Top 10:2021 — A07 Identification and Authentication Failures. https://owasp.org/Top10/2021/A07_2021-Identification_and_Authentication_Failures/

## 검증된 저자 블로그

- Baeldung. AuthorizationManager. https://www.baeldung.com/spring-security-authorizationmanager
- Baeldung. Passkeys Integration. https://www.baeldung.com/spring-security-integrate-passkeys
- Baeldung. One-Time Token Login. https://www.baeldung.com/spring-security-one-time-token-login
- Baeldung. Spring Cloud Gateway BFF + OAuth2. https://www.baeldung.com/spring-cloud-gateway-bff-oauth2
- Baeldung. PKCE for Secret Clients. https://www.baeldung.com/spring-security-pkce-secret-clients
- Baeldung. CORS Preflight + Security. https://www.baeldung.com/spring-security-cors-preflight
- Baeldung. Method Security. https://www.baeldung.com/spring-security-method-security
- Baeldung. Spring Security 6.3 What's New. https://www.baeldung.com/spring-security-6-3
- Baeldung. MFA in Spring Security 7. https://www.baeldung.com/spring-security-7-mfa
- Dimitri Mes. Authorization Server in Security 7. https://dimitri.codes/authorization-server/
- Dimitri Mes. CSRF for SPA. https://dimitri.codes/spring-security-csrf-spa/
- Dimitri Mes. Multi-Factor Authentication. https://dimitri.codes/multi-factor-authentication-spring-security/
- Dan Vega. Spring Security 7 MFA. https://www.danvega.dev/blog/spring-security-7-multi-factor-authentication
- Curity. Token Handler Pattern (BFF). https://curity.io/resources/learn/the-token-handler-pattern/
- Curity. WebAuthn Overview. https://curity.io/resources/learn/webauthn-overview/
- Auth0. PKCE in Spring Security. https://auth0.com/blog/pkce-in-web-applications-with-spring-security/
- Auth0. Passkeys for Java Developers. https://auth0.com/blog/webauthn-and-passkeys-for-java-developers/
- Okta Developer. PKCE with Spring Boot. https://developer.okta.com/blog/2020/01/23/pkce-oauth2-spring-boot
- Duende Software. Securing SPAs with BFF. https://duendesoftware.com/blog/20210326-bff
- InfoQ. Spring 7 / Boot 4 Release Coverage. https://www.infoq.com/news/2025/11/spring-7-spring-boot-4/

## 한국 기술 블로그·커뮤니티

- 우아한형제들 기술블로그. "Spring Security Actuator 안전하게 사용하기". https://techblog.woowahan.com/9232/
- velog @pjh612. "Deprecated된 WebSecurityConfigurerAdapter 어떻게 대처하지?". https://velog.io/@pjh612/Deprecated%EB%90%9C-WebSecurityConfigurerAdapter-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%8C%80%EC%B2%98%ED%95%98%EC%A7%80
- velog @nays33. "SecurityFilterChain + WebSecurityCustomizer 커스터마이징".
- velog @on5949. "스프링 시큐리티 필터 체인 심화".
- velog @jwkwon0817. "Spring Security config using Bean".
- velog @goat_hoon. "Spring Security를 활용한 JWT 도입기".
- velog @soheelog. "Spring Security JWT 설정".

## 일반 보안·분석

- DZone. "Stop Using JWTs as Session Tokens". https://dzone.com/articles/stop-using-jwts-as-session-tokens
- GitHub Gist @samsch. "Stop Using JWTs". https://gist.github.com/samsch/0d1f3d3b4745d778f78b230cf6061452
- WorkOS. "OAuth Best Practices: Reading RFC 9700". https://workos.com/blog/oauth-best-practices
- Scalekit. "OAuth 2.0 Best Practices RFC 9700". https://www.scalekit.com/blog/oauth-2-0-best-practices-rfc9700
- Authgear. "Demonstrating Proof-of-Possession (DPoP) Guide". https://www.authgear.com/post/demonstrating-proof-of-possession-dpop
- FusionAuth. "OAuth 2.0 vs OAuth 2.1". https://fusionauth.io/articles/oauth/differences-between-oauth-2-oauth-2-1
- BezKoder. "Refresh Token Rotation Example". https://www.bezkoder.com/spring-boot-refresh-token-jwt/
- Toptal. "Spring Security Code Review Pitfalls".

## GitHub Issue Tracker (인용 근거)

- spring-projects/spring-security#17487. `@PreAuthorize` silently disabled when `@EnableGlobalMethodSecurity` remains. https://github.com/spring-projects/spring-security/issues/17487
- spring-projects/spring-security#14149. Simplify CSRF Configuration for SPAs. https://github.com/spring-projects/spring-security/issues/14149
- spring-projects/spring-security#6856. `MODE_INHERITABLETHREADLOCAL` + thread pools 위험.
- spring-projects/spring-security#12629. Deprecate `.and()` + non-lambda DSL.
- openrewrite/rewrite-spring#793. Migration Recipe for 6.4/6.5 deprecations.

---

# 판권

**책 제목:** 토비의 Spring Security 7
**부제:** 내부 아키텍처부터 Zero Trust·Passkeys·MFA까지, Spring Boot 4 기반 심층 레퍼런스
**저자:** Toby-AI
**책 버전:** v1.0.0
**발행일:** 2026-05-11
**언어:** 한국어
**식별자:** book/toby-spring-security-7@v1.0.0

## 라이선스

이 책은 [**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko) 라이선스로 배포된다.

- **저작자 표시(BY).** 출처를 밝힐 것. 저작자는 *Toby-AI*.
- **비상업적 이용(NC).** 상업적 목적으로 이용할 수 없다.
- **동일조건 변경허락(SA).** 변경·재배포 시 동일한 라이선스를 적용해야 한다.

원문 라이선스 전문: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.ko
[CC BY-NC-SA 4.0]

## 산출 도구 크레딧

이 책은 `book-writer` 하네스(v1.2.0)로 산출됐다. 리서치·계획·계획 리뷰·챕터 저술·스타일 점검·편집·표지 디자인·EPUB 빌드 전 과정을 AI 에이전트 협업으로 수행했다. 하네스 자체는 MIT 라이선스로, 책 콘텐츠는 위의 CC BY-NC-SA 4.0으로 각각 배포된다.

- 하네스 출처: https://github.com/tobyilee/book-writer

## 인용 표기 예시

```
Toby-AI. (2026). 《토비의 Spring Security 7: 내부 아키텍처부터 Zero Trust·Passkeys·MFA까지, Spring Boot 4 기반 심층 레퍼런스》 (v1.0.0). CC BY-NC-SA 4.0.
book/toby-spring-security-7@v1.0.0.
```

© 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0
