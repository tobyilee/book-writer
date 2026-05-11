# 20A장. 자바 보안의 11년 변화 — SecurityManager의 종말부터 KEM·KDF까지

Spring Security 6 업그레이드 중에 이런 상황이 벌어졌다고 해보자. 빌드는 통과했고 테스트도 그린이다. 그런데 회사의 결제 모듈에서 *키 파생* 로직을 새로 짜야 할 일이 생긴다. 토큰 발급 한 줄을 바꾸려고 코드를 열었더니, 보안팀이 보내준 가이드에 *KEM*과 *KDF*라는 단어가 줄줄이 적혀 있다. "JDK 25부터 표준화된 KDF API를 쓰세요. KEM은 Java 21부터 들어왔으니 그쪽이 적합합니다." 한 줄 한 줄은 분명 한국어인데, 머릿속에는 *어디서부터 따라가야 할까*라는 의문만 남는다. 찜찜하다.

보안은 평소에 우리가 잘 안 만진다. JDK가 알아서 처리해주는 영역이고, Spring Security가 그 위에서 한 번 더 감춰준다. 그런데 *어떤 사건들*이 자바의 보안 모델을 11년에 걸쳐 조용히 바꿔놓았고, 그 변화의 일부는 *마이그레이션 시점에 반드시* 우리 앞에 나타난다. 자바 보안 모델의 변화를 어디까지 알아야 할까? 한 번 짚어보자.

## SecurityManager — 30년 묵은 모델의 종말

20장에서 짧게 만났던 그 SecurityManager 얘기를 좀 더 들여다보자. 자바 1.0 때부터 자바는 한 가지 약속을 끌고 왔다. *신뢰할 수 없는 코드를 같은 JVM에서 격리해 돌릴 수 있다*는 약속. Applet, Java Web Start, 일부 멀티테넌트 앱 서버가 이 위에 서 있었고, `SecurityManager` + `AccessController` + `java.policy` 파일이 그 *정책 표현 도구*였다.

이 모델이 *왜* 끝나야 했을까. 한 줄로 답하면, **그 모델이 약속한 격리를 자바가 끝내 보장하지 못했다.** JEP 411의 회고가 솔직하다. Sandbox escape 취약점이 너무 자주 발견됐고, JIT의 인라이닝·escape analysis 같은 *수십 년 묵은 최적화 경로*가 정책 검사를 *자동으로 우회*할 수 있는 상태에 다다랐다. 더 큰 변화는 *세계의 변화*였다 — Applet은 사라졌고, 클라우드 시대에 들어와 격리는 OS 컨테이너·VM·gVisor·Firecracker 같은 *바깥의 도구*가 책임지는 일이 됐다. JEP 411(Java 17)의 deprecation과 JEP 486(Java 24)의 제거는 자바의 약속을 *포기한* 게 아니라, 그 약속이 살아 있던 *세계가 끝났음을 인정한* 일에 가깝다.

엔터프라이즈에서 `System.setSecurityManager(...)`도 `AccessController.doPrivileged(...)`도 한 줄씩 정리되어야 한다. 그 자리에 들어서는 것은 *바깥의 격리 도구*다 — Java Agent + Byte Buddy, OS 레벨 sandbox(seccomp·AppArmor·gVisor), 모듈 시스템의 strong encapsulation. 어느 길도 *JVM 안에서 한 방에 풀 수 있는 답*은 아니다. 그게 SecurityManager 종말의 가장 큰 의미다.

## JEP 452 KEM — post-quantum의 첫 단추

여기서부터는 좀 다른 결의 변화다. *사라지는 모델*이 아니라 *새로 들어오는 도구*다. JEP 452(Java 21)로 들어온 **Key Encapsulation Mechanism API**가 그것이다.

KEM이 뭔지 한 줄로 적어보자. *상대방의 공개 키*를 받아서, *공유 비밀(shared secret)*과 그 공유 비밀을 *암호화한 캡슐(encapsulation)*을 함께 만들어내는 메커니즘이다. 캡슐만 상대방에게 보내면, 상대방은 자기 비밀키로 캡슐을 열어 같은 공유 비밀을 얻는다. 이 공유 비밀은 이후 *대칭키 암호화*의 시드로 쓰인다.

```java
KEM kem = KEM.getInstance("DHKEM");
KEM.Encapsulator e = kem.newEncapsulator(publicKey);
KEM.Encapsulated enc = e.encapsulate();
SecretKey sharedSecret = enc.key();      // 공유 비밀
byte[] capsule = enc.encapsulation();    // 캡슐 (상대에게 전송)
byte[] params = enc.params();            // 추가 파라미터
```

받는 쪽:

```java
KEM.Decapsulator d = kem.newDecapsulator(privateKey);
SecretKey sharedSecret = d.decapsulate(capsule);
```

여기서 "그게 RSA 키 교환이랑 뭐가 다른가?"라는 의문이 자연스럽게 생긴다. 답이 KEM의 진짜 의미를 가른다. **KEM은 알고리즘이 아니라 *추상 계층*이다.** "DHKEM"은 한 구현이고, *PQC(post-quantum cryptography)* 알고리즘인 **CRYSTALS-Kyber**(2024년 NIST FIPS 203 표준)도 같은 `KEM` 인터페이스로 들어온다. 즉 KEM API는 *양자내성 암호로 옮겨갈 때 코드를 통째로 다시 짜지 않아도 되게 하는* 추상화 자리에 가깝다.

왜 *지금* 이 자리가 필요할까. 양자 컴퓨터가 RSA·ECC를 깨는 시점이 언제일지에 대해서는 의견이 갈리지만, "그 시점이 오면 *지금 암호화해서 저장 중인* 데이터도 미래에 복호화될 수 있다"는 *harvest now, decrypt later* 시나리오는 이미 위협 모델에 들어와 있다. 그래서 *지금부터* PQC로 점진 이양할 수 있는 *언어 레벨 추상화*가 필요했고, KEM이 그 자리를 잡았다.

평소엔 우리가 KEM을 직접 호출할 일이 거의 없다. TLS 1.3 이상의 핸드셰이크가 *그 안에서* KEM을 쓴다. 그러나 결제 토큰화·키 분배·서명 시스템처럼 *키 자체를 다루는* 코드라면 한 번쯤 알고 있어야 한다. 11년 후 우리가 양자 시대에 대비된 결제 인프라를 짤 때, KEM은 *그날의 도구*다.

## JEP 478 → 510 KDF — 키 파생의 표준화

KEM이 *공유 비밀을 만드는* 메커니즘이라면, **KDF(Key Derivation Function)**는 *그 공유 비밀에서 실제 사용할 키를 파생하는* 메커니즘이다. HKDF, PBKDF2, Argon2 같은 알고리즘들이 여기에 들어간다.

JDK 24에서 JEP 478로 preview 도입됐고, JDK 25에서 JEP 510으로 표준화됐다. 표준화된 API는 다음과 같다.

```java
KDF hkdf = KDF.getInstance("HKDF-SHA256");

HKDFParameterSpec spec = HKDFParameterSpec
    .ofExtract()
    .addIKM(sharedSecret.getEncoded())  // KEM의 결과
    .addSalt("payment-token-v1".getBytes())
    .thenExpand("session-key".getBytes(), 32);

SecretKey sessionKey = hkdf.deriveKey("AES", spec);
```

왜 이걸 자바가 *직접* 표준화해야 했을까. KDF가 *Bouncy Castle·Tink·Conscrypt* 같은 외부 라이브러리에 흩어져 있던 게 문제였다. 라이브러리마다 API가 달랐고, *알고리즘 이름 한 줄 차이*로 보안 사고가 나는 일이 종종 있었다. PBKDF2의 iteration count를 보안 기준보다 낮게 설정해놓고 라이브러리 default라 믿고 넘어가는 일, HKDF의 salt를 빈 값으로 두는 일. 자바 표준에 들어오면 API 자체가 *안전한 기본값*을 강제할 수 있다.

세 가지 알고리즘이 첫 표준으로 들어온다. **HKDF**(RFC 5869, 일반 키 파생), **PBKDF2**(RFC 8018, 패스워드 기반), **Argon2**(메모리 하드, 패스워드 해싱). 이 셋이 표준 자바 라이브러리 안에서 같은 `KDF` 인터페이스로 잡힌다는 사실 자체가 *큰 진전*이다.

`PBKDF2`나 `Argon2` 쪽이 더 익숙할 수 있다. *사용자 비밀번호*를 다루는 코드라면 거의 항상 `PBKDF2`나 `Argon2`를 거친다. Spring Security 6의 `BCryptPasswordEncoder`·`Argon2PasswordEncoder` 안쪽이 JDK 25 이후에는 *표준 KDF API*에 얹혀서 동작하도록 진화할 가능성이 크다. 기억해두자 — 우리가 직접 안 만지는 것 같지만, KDF는 *이미 우리 앱 안*에 들어와 있다.

## TLS 1.3 (Java 11)과 EdDSA (Java 15)

마이그레이션 맥락에서 두 가지 변화는 짧게라도 짚어두자.

**TLS 1.3**이 Java 11에서 표준 지원됐다. 핸드셰이크 라운드트립이 1.2의 절반으로 줄어들고(0-RTT 옵션까지), Cipher Suite가 *forward secrecy*를 강제하는 작은 집합으로 정리됐다. JVM은 자동으로 TLS 1.3을 우선 협상한다. 마이그레이션 시점에 신경 쓸 부분은 거의 없지만, *옛 SSL 검증 코드*가 1.2 가정 위에 짜여 있다면 한 번 점검할 일이 있다. 인증서 체인 검증의 일부 동작이 1.3에서 *더 엄격*해진 부분이 있다.

**JEP 339 — EdDSA(Edwards-Curve Digital Signature Algorithm)**이 Java 15에서 들어왔다. Ed25519와 Ed448. ECDSA보다 *결정론적 서명*이고, *더 빠르고*, *구현 함정이 적다*. 옛 ECDSA가 random nonce를 잘못 다루면 비밀키가 노출되는 함정이 있었던 데 비해, EdDSA는 그 함정 자체를 알고리즘 차원에서 막는다. JWT(JOSE) 서명, SSH 키, 일부 블록체인 통신에서 이미 default가 된 알고리즘이다.

```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("Ed25519");
KeyPair kp = kpg.generateKeyPair();

Signature sig = Signature.getInstance("Ed25519");
sig.initSign(kp.getPrivate());
sig.update("payment-receipt".getBytes());
byte[] signature = sig.sign();
```

JWT를 발급하는 코드라면 `RS256` 대신 `EdDSA`(Ed25519)로 이주하는 일을 *Java 15 이상 베이스라인의 자연스러운 흐름*으로 두는 편이 낫다. 토큰 사이즈가 작아지고, 검증 속도도 빨라진다.

## sealed로 토큰 상태 — 결제 토큰화 예제

이 자리에서 sealed가 *왜 보안 도메인에서 특별히 유용한가*를 한 번 짚어두자. 13장에서 sealed가 sum type으로서 *exhaustiveness*를 컴파일러 차원에서 보증한다는 점을 봤다. 보안 도메인에서는 그 보증이 *invariant 유지*로 직결된다.

결제 토큰을 모델링한다고 해보자. KEM으로 만든 공유 비밀과 KDF로 파생한 세션 키가 *Success* 분기에 함께 실린다.

```java
sealed interface AuthResult
    permits AuthResult.Success, AuthResult.Failure {

    record Success(String principal, SecretKey sessionKey, byte[] capsule)
        implements AuthResult {}
    record Failure(FailureKind kind, String reason) implements AuthResult {}

    enum FailureKind { BAD_CREDENTIALS, EXPIRED, LOCKED }
}

AuthResult authenticate(String principal, PublicKey clientKey) {
    var enc = kem.newEncapsulator(clientKey).encapsulate();
    var spec = HKDFParameterSpec.ofExtract()
        .addIKM(enc.key().getEncoded())
        .addSalt(("session-" + principal).getBytes())
        .thenExpand("payment-v1".getBytes(), 32);
    var sessionKey = kdf.deriveKey("AES", spec);
    return new AuthResult.Success(principal, sessionKey, enc.encapsulation());
}
```

호출 측에서는 sealed의 보증을 그대로 쓴다.

```java
return switch (authenticate(userId, clientKey)) {
    case Success(var p, var k, var capsule) ->
        ResponseEntity.ok(new SessionResponse(p, capsule));
    case Failure(FailureKind.EXPIRED, var reason) ->
        ResponseEntity.status(401).body("session expired");
    case Failure(var kind, var reason) ->
        ResponseEntity.status(403).body(reason);
};
```

`default`가 없다. *모든 결과 분기*가 명시적으로 처리됐음을 컴파일러가 *증명*한다. 새로운 결과 상태가 sealed에 추가되는 순간, *이 코드는 컴파일 에러를 낸다.* 즉 보안적으로 중요한 분기가 *조용히 누락되는 일*이 원천적으로 막힌다. 옛 OOP 스타일의 abstract class + visitor 패턴이 *그동안 풀려고 애썼지만 늘 실패했던* 이 문제를, sealed + pattern matching이 *언어 차원에서 보증*한다.

KEM이 *공유 비밀*을 만들고, KDF가 *세션 키*를 파생하며, sealed + records가 *결과의 모든 분기*를 컴파일 시점에 강제한다. *세 가지 변화*가 한 자리에서 만나 보안 도메인의 코드를 *읽고 검증할 수 있는 모양*으로 만든다. Spring Security 6도 이 결을 받아들이는 흐름이다. `Authentication`·`OAuth2Token` 같은 핵심 타입들이 records로, 일부 상태 분기는 sealed 위에 얹혀가는 방향으로 진화 중이다. 새 코드에서 우리가 같은 패턴을 직접 쓸 수 있다는 사실이 중요하다.

## 보안 모델의 11년을 한 줄로

자바 보안 모델의 11년 변화를 한 줄로 적으면 이렇다 — **JVM이 모든 격리를 떠맡으려던 모델에서, 표준 암호 도구를 잘 갖춰주는 모델로 옮겨왔다.** SecurityManager가 떠난 자리는 OS 컨테이너와 Java Agent가 채운다. 그 빈자리에 KEM·KDF·EdDSA·TLS 1.3 같은 *모던 암호 기본기*가 표준 라이브러리로 들어왔다. 자바는 *덜 가두려 하고, 더 잘 만들어주려는* 방향으로 움직였다.

이 변화가 마이그레이션 시점에 우리 앞에 어떻게 나타나는가는 두 갈래다. *제거되는 것들*에 대한 대응(SecurityManager·AccessController), 그리고 *새로 들어온 것들*에 대한 채택(KEM·KDF·EdDSA). 둘 다 *지금* 시작해두지 않으면 5년 뒤 더 큰 부채가 된다.

보안 API는 *우리가 안 만지는 것 같지만* 깊은 곳에서 이미 우리 앱을 떠받친다. Spring Security가, Tomcat의 TLS가, JWT 라이브러리가, JDBC 드라이버의 SSL 검증이 — 다 그 깊은 곳에 살고 있다. 깊다고 *몰라도 되는* 자리가 아니라, 깊은 만큼 *한 번은 알고 있어야 하는* 자리다.

다음 장에서는 모던 자바와 Spring Boot 3가 *서로 어떻게 맞물리는가*를 따로 묶어서 보자. 마이그레이션이 끝난 자리, 그 위에서 어떤 *Spring 고유의 패턴*이 자라나는지를 짚는 자리다.
