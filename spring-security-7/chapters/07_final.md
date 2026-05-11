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
