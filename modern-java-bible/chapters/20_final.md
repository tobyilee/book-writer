# 20장. Java 8 → 17 마이그레이션 — 현장의 함정과 권장 순서

Spring Boot 3로 옮기는 첫날 아침을 한번 떠올려보자. 의욕 가득한 시니어 한 명이 회사 결제 모듈의 `pom.xml`에서 `<spring-boot.version>2.5.6</spring-boot.version>`을 `3.2.0`으로 바꾸고, `<java.version>1.8</java.version>`을 `17`로 올린 다음 `mvn clean install`을 친다. 모니터에 빨간 글자가 7초간 흘러내리더니, "BUILD FAILURE — 700 errors"라는 한 줄로 마무리된다. 익숙한 클래스가 사라졌다고 한다. `javax.xml.bind.JAXBContext`도, `javax.annotation.PostConstruct`도, `javax.servlet.http.HttpServletRequest`도. 1번 에러를 클릭해 들어가니 같은 패턴이 연달아 200줄, 그 아래로 또 200줄.

이런 화면을 본 적이 한 번이라도 있다면 다음 의문을 안 가질 수가 없다. *어디서부터 손대야 할까?*

쉬워 보이는 답은 "에러 메시지를 따라 위에서 아래로 고치자"다. 이게 통할 것 같지만, 막상 해보면 끝이 보이지 않는다. JAXB 의존성을 추가하면 이번에는 `javax.activation`이 깨지고, 그걸 jakarta로 바꾸면 Spring이 못 알아본다. Mockito가 ASM 옛 버전을 끌어와 `--add-opens`를 요구하고, Lombok이 17용이 아니라며 침묵한다. 일주일을 그렇게 보내고 나면 "Java 8에 머무는 편이 낫겠다"는 결론이 머릿속에서 슬며시 자라난다.

그런데 *원래* Java 8 → 17 마이그레이션은 이렇게 가야 하는 길이 아니다. 한꺼번에 점프하지 않고, 11 → 17 → 21로 한 칸씩 끊어가야 하는 길이다. 이 장에서는 그 칸들을 하나하나 짚어보자. 각 칸에서 어떤 함정이 기다리고 있는지, 왜 그게 함정인지, 그리고 그걸 피해 가는 6단계 권장 순서가 어떻게 짜이는지를 살펴보자.

## JEP 320이 남긴 깊은 구덩이

Java 11이 LTS로 나왔을 때 가장 큰 충격은 `var`도 HttpClient도 아니었다. **JEP 320 — Java EE / CORBA 모듈의 제거**였다. JDK가 11년간 끌어안아 왔던 다음 패키지들이 *전부* 사라졌다.

- `javax.xml.bind.*` (JAXB)
- `javax.xml.ws.*` (JAX-WS)
- `javax.activation.*` (JAF)
- `javax.xml.soap.*` (SAAJ)
- `javax.annotation.*` (Common Annotations — `@PostConstruct`, `@Resource` 등)
- `org.omg.CORBA.*` (CORBA)
- `javax.transaction.*` (JTA — Java EE 측 일부)

왜 이런 일이 벌어졌을까. Java EE가 Jakarta EE로 이양되면서 이 모듈들의 *진짜 주인*이 OpenJDK 바깥으로 옮겨갔기 때문이다. Oracle은 "이건 우리가 들고 있을 게 아니다"라고 판단했고, 11에서 깔끔히 잘라냈다. 그런데 한국의 SI·금융권 코드베이스 중 적지 않은 비율이 *바로 이 모듈들*을 SOAP·구공공 API·EAI 연동에서 사용하고 있었다. 외환·국세청·관세청·금융결제원 연동 코드를 한 번이라도 만져본 사람이라면 `JAXBContext.newInstance(...)`가 어떤 코드에서 어떤 식으로 살아 있는지 몸으로 안다.

해결책 자체는 의외로 간단하다. 깨진 모듈마다 *별도의 의존성*을 `pom.xml`에 추가하면 된다.

```xml
<!-- JAXB -->
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>4.0.2</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>4.0.5</version>
</dependency>

<!-- Common Annotations (@PostConstruct, @Resource) -->
<dependency>
    <groupId>jakarta.annotation</groupId>
    <artifactId>jakarta.annotation-api</artifactId>
    <version>3.0.0</version>
</dependency>

<!-- Activation -->
<dependency>
    <groupId>jakarta.activation</groupId>
    <artifactId>jakarta.activation-api</artifactId>
    <version>2.1.3</version>
</dependency>
```

문제는 *간단한 해결*이 *간단한 작업*을 뜻하지 않는다는 점이다. 의존성을 추가하는 일은 1분이면 끝나지만, 그 직후부터 `javax.xml.bind.JAXBContext` → `jakarta.xml.bind.JAXBContext`로 import를 바꿔야 하고, `@PostConstruct`의 패키지도 바꿔야 한다. 그 작업이 코드베이스 전체에 *어디어디 흩어져 있는지*가 한눈에 안 보인다는 게 진짜 함정이다. 한 모듈을 다 고친 줄 알았는데 빌드 캐시가 꼬여 빌드만 통과하고 런타임에서 `ClassNotFoundException`이 터지기도 한다. 찜찜한 경험이다.

권장은 이렇다. IDE의 *프로젝트 전체 찾아 바꾸기*를 쓰되, 한 번에 한 패키지씩만 한다. JAXB 먼저, 그 다음 annotation, 그 다음 activation 순서로. 한 패키지를 바꿀 때마다 `mvn clean test`를 돌려서 그 단위로 검증한다. 한꺼번에 다 바꾸면 어디서 깨졌는지 추적이 안 된다. 시간이 더 걸리는 것 같지만, 결과적으로는 빠르다.

## strong encapsulation — 라이브러리의 침묵

JDK 9 이후 모듈 시스템이 들어오면서 *내부 API*에 자물쇠를 채우기 시작했다. `sun.misc.Unsafe`, `sun.reflect.*`, `com.sun.*`. JDK 16에서 JEP 396이 그 자물쇠를 *기본값으로 강제*했고, JDK 17에서 JEP 403이 강제의 마지막 못을 박았다 — "이제 `--illegal-access=permit` 옵션 자체가 사라진다."

이게 무슨 뜻인가. 우리가 직접 `sun.misc.Unsafe`를 쓸 일은 거의 없다. 그러나 우리가 *의존하는 라이브러리*가 `Unsafe`를 쓰는 일은 흔하다. 옛 Mockito가 mock 객체를 만들 때, 옛 ByteBuddy가 클래스를 바이트코드 레벨에서 합성할 때, 옛 Hibernate Proxy가 `Unsafe.allocateInstance()`로 빈 객체를 만들 때 — 전부 내부 API를 쓴다. JDK 17로 올린 직후 다음 같은 메시지를 만나면 그 신호다.

```
java.lang.reflect.InaccessibleObjectException:
  Unable to make field private final java.util.Comparator
  java.util.PriorityQueue.comparator accessible:
  module java.base does not "opens java.util" to unnamed module
```

해결은 두 갈래다. 첫째, *라이브러리를 새 버전으로 올린다.* Mockito 5.x, ByteBuddy 1.14+, Hibernate 6, ASM 9.5+. 둘째, 라이브러리가 아직 업데이트되지 않았다면 `--add-opens`로 *임시* 통로를 연다.

```bash
java --add-opens=java.base/java.util=ALL-UNNAMED \
     --add-opens=java.base/java.lang.reflect=ALL-UNNAMED \
     -jar app.jar
```

Maven Surefire 플러그인이나 Gradle test task에 이걸 넣어두면 테스트는 통과한다. 그런데 *반드시* 그건 임시 조치다. `--add-opens` 목록이 길어질수록 그건 "라이브러리 업그레이드 빚이 쌓이고 있다"는 신호로 봐야 한다. JDK 24 이후에는 `Unsafe`의 메모리 접근 메서드가 본격 deprecate됐고, FFM API(MemorySegment)로 옮겨 가는 흐름이다. 즉 이 빚은 *시간이 갈수록* 청구서가 두꺼워진다. 기억해두자.

## Nashorn의 죽음 — 작지만 아픈 흔적

JEP 372(Java 15)로 Nashorn JavaScript 엔진이 사라졌다. 평소에는 안 쓰는 기능 같지만, 의외의 곳에서 발목을 잡는다. 결제 규칙 엔진이 `ScriptEngineManager().getEngineByName("nashorn")`을 호출해 동적 룰을 평가하던 코드. 옛 Drools 일부 룰의 평가식. JIRA·Jenkins 플러그인이 사용자 입력을 JavaScript로 받아 처리하는 부분. 이런 곳들이 갑자기 `null`을 받는다 — `getEngineByName`은 엔진이 없으면 예외를 던지지 않고 `null`을 반환한다. 이 동작이 더 사악하다. 런타임에 NPE로 터지기 때문이다.

대안은 GraalVM JavaScript다. `org.graalvm.js:js`와 `org.graalvm.js:js-scriptengine` 의존성을 추가하면 `ScriptEngineManager`에서 `"js"` 또는 `"graal.js"`로 잡힌다.

```xml
<dependency>
    <groupId>org.graalvm.js</groupId>
    <artifactId>js</artifactId>
    <version>23.1.2</version>
</dependency>
<dependency>
    <groupId>org.graalvm.js</groupId>
    <artifactId>js-scriptengine</artifactId>
    <version>23.1.2</version>
</dependency>
```

호환성은 대체로 양호하지만 100%는 아니다. Nashorn의 `Java.type(...)` 같은 비표준 헬퍼는 그대로 도는데, ES5/ES6 표준에 더 엄격해진 부분이 있다. 마이그레이션 전 *기존 스크립트의 단위 테스트를 늘려두는 편*이 안전하다. 옛 룰 한 줄이 새 엔진에서 다르게 평가되는 일은 결제·세금 도메인에선 끔찍한 일이 될 수 있다.

## SecurityManager — 엔터프라이즈의 큰 함정

이 함정은 의외로 사람들이 자주 놓친다. JEP 411(Java 17)로 `SecurityManager`가 deprecated for removal로 표시됐고, JEP 486(Java 24)에서 제거됐다. 이 사실 자체는 한 줄 뉴스다. 그런데 그 한 줄이 한국 금융권·공공 코드베이스에 무엇을 의미하는지를 따져보면 작지 않다.

옛날 옛적, 자바 1.0 때부터 "신뢰할 수 없는 코드를 같은 JVM에서 격리해 돌리는 모델"이 자바의 큰 약속이었다. Applet, Java Web Start, 그리고 일부 *멀티테넌트 애플리케이션 서버*가 이 모델 위에 서 있었다. 정책 파일(`java.policy`)을 작성해 "이 코드는 이 디렉터리만 읽을 수 있다", "저 코드는 네트워크 호출 금지"를 선언했다. WebSphere, WebLogic의 옛 보안 정책, 일부 SI 프레임워크의 커스텀 `Permission` 구현이 이 위에서 돌았다.

이 모델이 *왜* 끝났을까. 한 줄로 답하면, **그 모델이 약속한 격리를 자바가 끝내 보장하지 못했다.** Sandbox escape 취약점이 너무 자주 발견됐고, JIT의 인라이닝·escape analysis·OSR이 정책 검사를 우회할 수 있는 경로를 만들었다. 클라우드 시대에 들어와 격리는 OS 컨테이너·VM·gVisor·Firecracker 같은 *바깥의 도구*가 책임지는 일이 됐다. JVM 안에서 풀 수 있는 일이 아니었다는 회고가 OpenJDK 진영의 공식 입장이다.

그래서 무슨 일이 벌어지는가. 기업 코드베이스 어딘가에 다음 같은 패턴이 살아 있다면 적색 경보다.

```java
System.setSecurityManager(new MyPolicySecurityManager());
// 또는
AccessController.doPrivileged((PrivilegedAction<X>) () -> { ... });
```

`AccessController` 자체도 deprecated, `Subject.doAs`·`Subject.callAs`까지 함께 정리되는 흐름이다. JDK 17에서는 경고만, 21까지는 동작은 하되 `-Djava.security.manager=allow`를 명시해야 한다. 24부터는 *런타임 오류*. 17 마이그레이션 시점에 이 코드가 있다면, *제거 또는 대체 설계*가 함께 가야 한다. 모니터링만 해두는 건 부족하다.

대안은 어디서 찾아야 할까. 세 갈래다.

- **Java Agent + Byte Buddy**로 instrumentation 시점에 위험 호출을 가로채는 방식. 정책 표현력은 좋지만 코드 복잡도가 오른다.
- **OS-level sandbox**(seccomp, AppArmor, gVisor, 컨테이너 capability 제한). 가장 권장되는 길.
- **모듈 시스템(JPMS)의 strong encapsulation**. 라이브러리 격리에 한해 부분적 대안. 다만 우리가 4·6장에서 다뤘듯 JPMS 자체가 본격 도입에 진입 비용이 크다.

엔터프라이즈 마이그레이션 일정을 짤 때, "SecurityManager 사용 코드의 식별과 대체"는 *반드시 별도 항목*으로 잡아두는 편이 낫다. 다른 일정 안에 묻혀 있다가 막판에 발견되면 일정 전체가 흔들린다.

## HttpClient — Java 11이 준 표준 도구

JEP 321(Java 11)로 `java.net.http.HttpClient`가 표준화됐다. Java 11 베이스라인에 도달했다면 *반드시* 알고 있어야 할 표준 도구다. 동기·비동기·HTTP/1.1·HTTP/2·WebSocket을 한 API로 다룬다.

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(5))
    .build();

HttpRequest req = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/v1/orders/42"))
    .header("Authorization", "Bearer " + token)
    .GET()
    .build();

HttpResponse<String> res = client.send(req, BodyHandlers.ofString());
```

비동기는 `sendAsync`가 `CompletableFuture<HttpResponse<T>>`를 돌려준다. Reactive 흐름이 필요하다면 그 위에 chain을 걸면 된다.

21장에서 본격적으로 다룰 일이지만, 마이그레이션 맥락에서 한 가지만 미리 짚어두자. `HttpClient`는 **virtual thread와의 시너지가 결정적**이다. 14장에서 봤듯이 virtual thread는 blocking I/O를 받아낼 때 가장 빛난다. `client.send(...)`의 동기 호출을 virtual thread 안에서 그대로 적어두면, JDK 21+ 환경에서 자동으로 unmount되고 carrier thread를 반납한다. WebClient를 쓸 때처럼 `Mono`·`Flux`를 chain할 필요가 없고, RestTemplate처럼 thread pool에 묶이지도 않는다. *동기 코드의 명료함*과 *비동기의 처리량*이 같은 자리에서 만난다.

그러니 17 마이그레이션 시점에 다음을 함께 고려하는 편이 낫다. Apache HttpClient 4.x를 쓰던 코드가 있다면, 우선 5.x로 올리거나 가능하면 `java.net.http.HttpClient`로 옮긴다. `RestTemplate`은 Spring 6에서 deprecated는 아니지만 *유지보수 모드*다. WebClient는 reactive 스택이 정말 필요할 때만. 새 코드라면 `HttpClient` + virtual thread가 가장 자연스러운 선택지다. 네 가지를 한 화면에 놓고 비교하는 일은 21장의 몫이고, 여기서는 *마이그레이션 시점의 한 줄 가이드*만 챙겨두자.

## Docker RSS의 늘어남 — 컨테이너의 작은 비명

Java 17로 올린 직후 운영팀에서 보내는 메시지가 늘어나는 신호가 하나 있다. "결제 서비스 pod이 OOMKilled로 자주 재시작합니다." Heap은 그대로 둔 채 JDK만 8 → 17로 올렸을 뿐인데, 컨테이너 메모리 limit이 빠듯해진다. 왜일까.

여러 요인이 겹친다.

- **PermGen 시대에서 Metaspace로** — 8 이전엔 PermGen이 고정 크기였다(`-XX:MaxPermSize`). 8부터는 Metaspace로 바뀌면서 native 메모리에서 자랄 수 있게 됐고, 17 시점엔 그 사이즈가 옛날보다 한 자릿수 더 크다. 클래스로딩이 많은 Spring Boot 앱에서 Metaspace가 100~200MB는 흔하다.
- **G1 + JFR + JIT C2 캐시** — G1이 default가 되면서 region 메타데이터가 native 메모리를 잡는다. JFR이 default로 켜져 있고, JIT의 C2 컴파일러가 코드 캐시(`-XX:ReservedCodeCacheSize`, 기본 240MB)를 예약한다.
- **Compressed OOPs의 변화** — heap 32GB 미만에서는 여전히 켜지지만, 옛 JVM과 약간 다른 패턴으로 정렬한다. CleverTap 블로그가 이 부분을 자세히 기록했다.
- **NIO direct buffer·Netty native** — Spring WebFlux나 Netty 기반 클라이언트가 쓰는 direct memory가 누적된다.

이 모두를 합치면 컨테이너 RSS는 *heap의 두 배*에 가까워진다. 4GB heap을 쓰는 앱이 8GB 컨테이너 limit에서 OOMKilled를 만난다. 옛 8 시절엔 6GB로도 충분했던 같은 앱이.

대처는 두 단계다. 첫째, *측정*. `jcmd <pid> VM.native_memory summary`로 native memory breakdown을 본다. 둘째, *limit 조정과 옵션 정리*. 컨테이너 limit을 heap의 1.7~2.0배로 잡고, `-XX:MaxMetaspaceSize`로 Metaspace 상한을 명시한다. `-XX:MaxDirectMemorySize`도 명시. Spring Boot 3.4의 *Container Awareness 개선*이 자동 계산을 돕긴 하지만, 기본값을 그대로 믿기보다는 한 번 측정해보고 결정하는 편이 안전하다.

## javax → jakarta — Spring Boot 3의 큰 산

Spring Boot 2.7 → 3.0이 들고 온 가장 큰 깨짐은 코드 한 줄로 요약된다. **`javax.*` → `jakarta.*`.** Java EE의 패키지 이름이 Jakarta EE로 *완전 이양*되면서 Spring 6도 이 전환을 그대로 받아들였다.

영향 범위가 작지 않다.

| 옛 패키지 | 새 패키지 |
|---|---|
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.transaction.*` (JTA) | `jakarta.transaction.*` |
| `javax.inject.*` | `jakarta.inject.*` |
| `javax.annotation.*` | `jakarta.annotation.*` |
| `javax.ws.rs.*` (JAX-RS) | `jakarta.ws.rs.*` |
| `javax.mail.*` | `jakarta.mail.*` |

엔티티 한 줄을 보자.

```java
// Before (Spring Boot 2.x, javax)
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;

@Entity
public class Order {
    @Id private Long id;
    @NotNull private String customerId;
}

// After (Spring Boot 3.x, jakarta)
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotNull;

@Entity
public class Order {
    @Id private Long id;
    @NotNull private String customerId;
}
```

import 한 줄씩 손으로 바꿀 일은 아니다. 자동 변환 도구가 잘 갖춰져 있다.

- **OpenRewrite**의 `org.openrewrite.java.migrate.JavaxToJakarta` recipe — Maven·Gradle 양쪽에서 한 줄로 적용된다.
- **Spring Boot Migrator**(`spring-boot-migrator`) — Spring 팀이 직접 만든 도구. 2.7 → 3.x 전환의 전반을 자동화한다.
- **IntelliJ의 *Migrate Java EE to Jakarta EE*** — Ultimate에 내장.

OpenRewrite를 한번 보자. Maven plugin으로 실행하면 다음 한 줄이다.

```bash
mvn org.openrewrite.maven:rewrite-maven-plugin:run \
    -Drewrite.activeRecipes=org.openrewrite.java.migrate.JavaxToJakarta \
    -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-migrate-java:RELEASE
```

수만 라인의 import가 한 번에 바뀐다. 단 *완전 자동*은 아니다. 다음 같은 곳은 수동 검토가 필요하다.

- 문자열 안에 `"javax.persistence."`처럼 패키지 이름이 적힌 부분(쿼리 hint, custom annotation processor 등).
- 외부 라이브러리가 아직 javax-only인 경우 — Hibernate 5는 javax, Hibernate 6은 jakarta. 두 세계가 같은 클래스패스에 있으면 충돌한다.
- 톰캣 9(javax.servlet)와 톰캣 10/11(jakarta.servlet)은 서로 다른 namespace를 쓴다. 같이 깔리면 모호한 오류가 난다.

이 산을 넘었다면 마이그레이션의 가장 큰 봉우리를 넘은 셈이다.

## 권장 순서 6단계 — 한 칸씩 끊어가기

위의 함정들을 다 안다면, 이제 *어떤 순서*로 밟는 게 가장 사고가 적은가를 정해야 한다. 경험적으로 자리잡힌 길은 다음 6단계다.

**1단계. JDK만 11으로, 코드는 그대로.**
`<java.version>1.8</java.version>` → `11`. Spring Boot도, 라이브러리 버전도 그대로. 빌드만 성공시킨다. 여기서 깨지는 것들이 *JDK 11의 큰 변화* 자체에 대한 노출이다. JEP 320 흔적, strong encapsulation 경고, 옛 `--add-opens` 필요 라이브러리. 이 단계에서 깨진 부분을 다 고친다. *Spring Boot 버전은 손대지 않는다.* 두 변수를 동시에 움직이면 어느 쪽에서 깨졌는지 추적이 안 된다.

**2단계. JDK 17으로, 여전히 Spring Boot 2.7.**
17의 변화는 11에 비하면 작다. records·sealed·pattern이 표준화됐을 뿐 *기존 코드*를 강제로 깨는 변화는 적다. SecurityManager 경고가 본격화된다 — 이 단계에서 코드 식별만 해두자. 17이 빌드되면 *그 자리에서 멈춘다*. 코드를 records로 리팩토링하지 않는다. 그건 다음 자리의 일이다.

**3단계. Spring Boot 2.7 → 3.x.**
드디어 javax → jakarta 전환. OpenRewrite recipe를 돌리고, 수동 검토 항목을 한 번 훑는다. Tomcat·Hibernate·Validator 버전이 함께 올라간다. *이 단계가 가장 위험하고 가장 시간이 많이 든다.* 보통 4주 일정 중 2주를 여기에 쓴다. 단계 끝에 통합 테스트를 다 통과시킨 다음, 그 시점으로 *반드시* 태그를 끊어둔다. 이후 어느 단계에서 문제가 나면 여기로 되돌아올 수 있게.

**4단계. records를 DTO부터.**
API request/response, query projection, 내부 event. *Entity는 건드리지 않는다.* JPA의 mutable·no-args 요구와 records가 안 맞는 건 11장에서 봤다. DTO부터 시작해서 점진적으로 늘려가자. Jackson은 records를 자연스럽게 지원한다. `@RequestBody record CreateOrderRequest(...)` 한 줄이면 끝난다.

**5단계. var·switch expression·pattern matching의 점진적 도입.**
새 코드에서는 적극 쓰고, 기존 코드는 *수정의 자연스러운 흐름 안에서만* 바꾼다. 9·10·12·13장에서 다룬 각 도구의 가이드라인을 팀 컨벤션으로 적어 둔다. 한꺼번에 코드베이스 전체를 갈아엎는 PR은 리뷰가 안 된다. 끔찍한 일이다.

**6단계. JDK 21+ 베이스로 virtual thread.**
Spring Boot 3.2+, `spring.threads.virtual.enabled=true`. 14·15장에서 본 ThreadLocal·pinning 가이드를 다시 펼친다. 모니터링에 JFR `jdk.VirtualThreadPinned` 이벤트를 잡아두고, HikariCP·Caffeine·Apache HttpClient 등 *synchronized 무거운* 라이브러리 버전을 점검한다. JDK 24의 JEP 491이 pinning을 거의 없애지만, LTS 정책상 21에 머문다면 한동안은 라이브러리 audit이 필요하다.

이 6단계의 핵심 원리는 한 줄이다 — *한 번에 하나의 변수만 움직이자.* JDK 버전을 올리는 PR과 라이브러리를 올리는 PR과 코드 스타일을 바꾸는 PR을 *섞지 말자.* 섞으면 그건 마이그레이션이 아니라 도박이 된다.

## 한국 SI·금융권의 회고담

이 6단계를 정직하게 밟는 일이 *얼마나 어려운가*는 한국 SI·금융권 현장에서 자주 나오는 회고에서 잘 드러난다. 일반화된 한 토막을 들여다보자.

한 카드사의 핵심 채널 시스템이 Java 8 + Spring Boot 1.5 + 옛 Tomcat 8.5에서 출발했다. 시스템 자체는 7년간 안정적으로 돌았다. 그런데 2023년 보안 감사에서 "지원 종료된 JDK·프레임워크" 항목이 적색으로 잡혔고, 1년 안에 17까지 올리라는 지시가 떨어졌다. 첫 시도는 *한 번에 17로 점프*였다. SI 외주가 들어와 6주를 들였는데, 결국 통합테스트의 30%가 깨진 채로 일정을 못 맞췄다. 실패의 원인을 회고할 때 빠지지 않고 나오는 표현이 이런 것들이다.

- "JAXB·JAX-WS 의존성을 별도로 분리하는 작업이 *각 모듈 담당자마다 다른 방식*으로 풀려서 결과적으로 중복 의존성이 늘었다."
- "내부 EAI 어댑터가 `sun.reflect.Reflection`을 직접 호출하는 줄을 *아무도 몰랐다.* 운영 트래픽이 들어오기 전까지 못 잡아냈다."
- "도커 메모리를 옛날 기준으로 잡았다가 새벽에 OOMKilled가 연쇄로 일어났다. 결제 시간대 중간에."
- "SecurityManager 정책 파일이 옛 코드 어딘가에서 여전히 살아 있는 줄 *나중에야* 발견했다."

두 번째 시도는 외주 PM이 바뀌었고, 6단계 권장 순서를 그대로 따랐다. 8 → 11 → 17 → Spring Boot 3 → 코드 정리의 칸을 분기 단위로 끊어, 9개월에 마무리됐다. 시간으로는 길었지만 운영 사고는 *한 건도 없었다*. 이 회고담의 가르침은 한 줄이다 — *마이그레이션은 단번에 점프하는 일이 아니라, 한 칸씩 끊어가는 일이다.*

글로벌 사례도 결을 같이한다. CleverTap이 정리한 "Pitfalls When Upgrading from Java 8 to Java 17"이 Docker RSS·G1 메모리·Mockito 버전 함정을 자세히 적었고, Aviator의 "Java Version Upgrade" 글이 비슷한 8 → 17 여정을 다뤘다. Systematic의 "Java Migration Journey from Java 8 to Java 17"은 *한 칸씩 끊어 가는 전략*을 명시적으로 권장한다. 어느 한 사례를 베껴 따라가는 일은 답이 아니다. *모든 사례가 같은 가르침을 반복한다는 사실*이 답이다.

## PayBridge의 4주 마이그레이션 일정

1장에서 우리는 PayBridge라는 가상 결제사를 만났다. 결제 모듈 한 줄을 11년 전 Java 8로 시작해서, 지금은 17 베이스라인에 머물러 있다. 이 회사가 *향후 1년 안에* Java 21로 옮기겠다고 결정했다고 해보자. 6단계 권장 순서를 4주 일정으로 어떻게 짤 수 있을까. 일반화된 일정을 한번 펼쳐보자.

**Week 1 — 측정과 식별.**

월요일. 빌드만 17로 올리는 *spike PR*을 만든다. 깨지는 곳을 그라운드 트루스로 기록한다. 화요일~목요일. 다음을 식별한다.

- `sun.*`, `com.sun.*` 직접 호출 코드.
- `SecurityManager`·`AccessController.doPrivileged` 사용처.
- Nashorn `ScriptEngineManager` 호출처.
- Apache HttpClient 4.x·Mockito 3.x·ByteBuddy 1.10 미만·Lombok 1.18.22 미만.
- JAXB·JAX-WS·`@PostConstruct`·`javax.transaction` 사용처.

금요일. 결과를 *마이그레이션 부채 리포트*로 정리해 팀 전체에 공유한다. 이 리포트가 이후 3주의 *작업 백로그*가 된다.

**Week 2 — 의존성 정리.**

월·화요일. JAXB·Activation·Annotations 의존성을 jakarta 패키지로 추가하고, import를 단계적으로 바꾼다. 한 패키지 단위로 PR을 끊는다. 수요일. Mockito 5.x, ByteBuddy 1.14+, Lombok 최신, Apache HttpClient 5.x로 일제히 올린다. 테스트가 깨진 곳을 모듈별로 분담. 목·금요일. 빌드와 모든 테스트가 통과하는 *그린* 상태를 만든다. 이 시점에 `spring-boot.version`은 아직 2.7.x.

**Week 3 — Spring Boot 3 전환.**

월요일. OpenRewrite recipe로 javax → jakarta 일괄 변환. 변환 후 빌드. 화·수·목요일. 톰캣 10·Hibernate 6·Validator 3.x로의 자연스러운 업그레이드. 빌드 깨짐, 통합테스트 깨짐의 대부분이 여기서 나온다. 한 항목씩 *짧은 PR*로 푼다. 금요일. 통합 테스트 전 항목 통과. *반드시* 이 시점에 release candidate 태그를 단다.

**Week 4 — 코드 현대화와 운영 점검.**

월·화요일. records를 DTO에 도입. 가장 트래픽이 많은 5개 API의 request/response부터. 수요일. `switch expression`·pattern matching을 *컨트롤러 분기*에 점진 적용. 도메인 핵심에는 손대지 않는다. 목요일. Docker memory limit 재설정 — `jcmd VM.native_memory summary` 측정 후 heap의 1.8배로. JFR 이벤트 수집 시작. 금요일. 단계 결과를 *staging*에 배포해 일주일 운영. 별다른 사고가 없으면 다음 주 운영 배포.

이 일정의 어디에도 *한꺼번에 다 한다*는 줄이 없다. PayBridge처럼 7년차 운영 시스템이라면 더 그렇다. 한 칸씩 끊어가는 4주가 한 번에 점프하는 6주보다 *짧고 안전하다.* 1장의 결론이 여기서 다시 만나진다 — *시간을 아끼는 길은, 시간을 아끼려 들지 않는 길이다.*

## 마무리

11년의 자바를 한 번에 따라잡는 길은 없다. 한 칸씩 끊어가는 길만 있다. JEP 320이 EE를 잘라낸 자리, strong encapsulation이 내부 API의 자물쇠를 채운 자리, Nashorn이 사라진 자리, SecurityManager가 떠나는 자리, HttpClient가 새 표준이 된 자리, javax가 jakarta가 된 자리, Docker RSS가 슬며시 늘어난 자리 — 이 자리들 하나하나를 *그 자리의 함정*으로 인지하고, *그 자리에서 해결*하자. 다른 자리의 해결이 끝나기 전에는 다음 자리로 옮기지 않는 편이 낫다.

도구는 우리 손에 있다. OpenRewrite, Spring Boot Migrator, IDE의 자동 변환, JFR과 `jcmd`. 외부의 회고담도 있다. CleverTap, Aviator, Systematic의 글들, 그리고 무엇보다 *우리 옆 팀의 회고담*. 다음 장에서는 마이그레이션의 결을 같이 가는 한 가지 주제를 따로 짚는다. 자바 보안 모델의 11년 변화, 그리고 KEM·KDF가 *우리도 모르는 사이* 우리 앱에 들어와 있다는 사실을 말이다.
