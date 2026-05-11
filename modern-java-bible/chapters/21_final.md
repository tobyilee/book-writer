# 21장. Spring Boot 3.x × Java 21/25 — 시너지의 *고유성*

한 결제 마이크로서비스에 records·sealed·virtual thread·AOT를 한 번에 넣어야 한다고 해보자.

PayBridge의 결제 게이트웨이 한 조각을 떠올려 보자. 가맹점이 보내는 결제 요청을 받아 사기 탐지 시스템에 묻고, 카드사 어댑터에 라우팅하고, 정산 큐에 이벤트를 흘려보내는 평범한 마이크로서비스다. 요청 DTO는 record로, 결과 타입은 `sealed PaymentResult`로 모델링했다. 컨트롤러는 외부 API 두 개를 동시에 호출해야 하니 virtual thread로 받는다. 콜드 스타트 12초가 SLA를 깎아먹어서 AOT cache도 켜야 한다. 11장에서 records의 신원을, 12·13장에서 sealed와 pattern matching을, 14장에서 virtual thread를, 19장에서 Leyden을 따로따로 살펴봤다. 이제 그 도구가 한 컨트롤러에 모인다.

그런데 책 전체에서 쌓은 도구가 한 자리에 모이는 *후련함*은 있지만, 동시에 한 가지 물음이 따라온다. *Spring과 Modern Java가 가장 잘 맞물리는 자리는 어디일까?* Spring Boot 3.x에 `spring.threads.virtual.enabled=true` 한 줄 더 넣고 끝나는 이야기가 아니다. Spring Data의 record projection, `@ConfigurationProperties` + record의 immutable config, Spring 6의 `RestClient`, 살아남은 WebFlux의 자리 — 이런 *Spring 고유의 패턴*이 따로 있다. 그 자리를 한 장에 모아보자. 단순 종합이 아니라, 다른 챕터에서는 다루지 못한 *Spring × Modern Java*만의 결합점에 집중하자.

## §21.1 Spring Data와 record projection — 세 가지 길

먼저 가장 자주 마주치는 자리부터 들여다보자. Spring Data JPA는 entity 전체가 아니라 *필요한 컬럼만 뽑는* projection을 오래전부터 지원해 왔다. 그 방식이 세 가지다.

**interface projection.**

```java
public interface PaymentSummary {
    String merchantId();
    BigDecimal amount();
    Instant capturedAt();
}

public interface PaymentRepository extends JpaRepository<Payment, Long> {
    List<PaymentSummary> findByMerchantId(String merchantId);
}
```

Spring Data가 런타임에 JDK proxy로 구현체를 만들어 준다. 가벼워 보이지만, 이 proxy는 *getter 호출마다* 내부 맵에서 값을 꺼내 변환한다. nested projection을 쓰면 entity 전체를 fetch한 뒤 필드를 골라내는 일도 일어난다. 무겁다고 할 정도는 아니지만, *어떤 코드가 도는지가 잘 안 보인다*는 점이 *찜찜하다*.

**class projection (DTO projection).**

```java
public class PaymentSummaryDto {
    private final String merchantId;
    private final BigDecimal amount;
    private final Instant capturedAt;
    public PaymentSummaryDto(String merchantId, BigDecimal amount, Instant capturedAt) { /*...*/ }
    // getters, equals, hashCode, toString ...
}
```

명시적이고, 어떤 생성자가 호출되는지가 분명하다. 그러나 boilerplate가 무겁다. 그래서 Lombok `@Value`를 쓰던 시절이 있었다.

**record projection.**

```java
public record PaymentSummary(
    String merchantId,
    BigDecimal amount,
    Instant capturedAt
) {}

public interface PaymentRepository extends JpaRepository<Payment, Long> {
    List<PaymentSummary> findByMerchantId(String merchantId);
}
```

Spring Data 3.x는 record를 일급 시민으로 다룬다. canonical constructor의 시그니처를 그대로 읽어 JPQL의 `new` 구문으로 변환한다. interface projection처럼 가볍지만, *코드가 정직하다*. 어떤 생성자가 호출되는지가 한눈에 보인다. equals·hashCode·toString도 컴파일러가 정확히 만들어 준다.

세 길의 미세 차이를 표로 정리해 보자.

| 항목 | interface | class | record |
|------|-----------|-------|--------|
| 보일러플레이트 | 없음 | 무거움 | 없음 |
| 동작의 *가시성* | 낮음 (proxy) | 높음 | 높음 |
| equals/hashCode | 자동 (이름 기반) | 직접 작성 | 자동 (컴포넌트) |
| nested projection | 가능 | 가능 | 가능 (Java 16+) |
| Jackson 직렬화 | 어색함 (proxy) | 자연스러움 | 자연스러움 |
| Compile-time 검증 | 약함 | 강함 | 가장 강함 |

답이 보이는가? 신규 코드라면 *record projection이 기본이다*. interface projection은 nested 구조가 꼭 필요하거나 옛 코드와의 일관성 때문에 남길 뿐이다. record는 Spring Data의 query parser, Jackson의 직렬화, Bean Validation의 어노테이션 처리 — 이 세 곳에서 모두 *자연스러운 1급 시민*이다.

한 가지 *기억해두자*. record projection은 JPQL `new com.paybridge.PaymentSummary(p.merchantId, p.amount, p.capturedAt)`을 자동으로 만들어 주는 것이 핵심이라, *컴포넌트의 이름과 entity 필드의 이름이 일치해야* 한다. 일치하지 않으면 직접 JPQL을 적어 `new` 구문을 쓰자. 이 한 가지만 지키면, record projection이 가장 깔끔하다.

### Spring Data AOT Repositories — 빌드 타임에 미리 만들기

여기서 한 걸음 더 나간 도구가 있다. **Spring Data AOT Repositories**다. Spring Data 3.x는 빌드 타임에 repository의 query 메서드와 metadata를 *미리 생성*한다. 런타임 reflection이 줄고, GraalVM native image와의 호환성이 올라가며, 무엇보다 컴파일러가 잘못된 메서드명을 더 빨리 잡아낸다.

```java
@Repository
public interface PaymentRepository extends JpaRepository<Payment, Long> {
    List<PaymentSummary> findByMerchantIdAndCapturedAtBetween(
        String merchantId, Instant from, Instant to);
}
```

이 메서드명을 빌드 타임에 파싱해서 JPQL 문자열·매개변수 바인딩 정보·결과 매핑 메타데이터를 자바 코드로 생성해 둔다. 런타임에는 그 생성 결과만 실행한다. 컴파일 타임 JPA 메타모델(`Payment_.merchantId`)과 함께 쓰면 *문자열 기반 query 작성의 마지막 자리까지* 코드로 옮길 수 있다.

```java
// 컴파일 타임 JPA 메타모델 활용
Specification<Payment> spec = (root, query, cb) ->
    cb.equal(root.get(Payment_.merchantId), merchantId);
```

`Payment_`는 Hibernate Annotation Processor가 빌드 타임에 생성하는 메타모델 클래스다. `Payment_.merchantId`가 *문자열이 아닌 필드 참조*라는 점이 핵심이다. 컬럼명을 잘못 적는 *난감한* 사고가 컴파일 단계에서 잡힌다. record projection + AOT repositories + 메타모델 — 이 세 도구가 한 줄로 이어지면, Spring Data의 코드가 *런타임이 아니라 컴파일러가 검증하는 코드*로 바뀐다.

## §21.2 `@ConfigurationProperties` + record — immutable config의 자리

다음으로 살펴볼 자리는 설정이다. Spring 진영에서 오랫동안 `@ConfigurationProperties`로 외부 설정을 객체에 바인딩해 왔다. 옛 패턴은 setter가 있는 mutable POJO였다. setter가 노출돼 있다는 *찜찜함*이 늘 따라왔다 — 누군가 런타임에 설정을 *바꿔버릴* 수 있다는 가능성이 늘 열려 있었다.

```java
// 옛 패턴 — mutable, setter 노출, *찜찜함*
@ConfigurationProperties("paybridge.gateway")
public class GatewayProperties {
    private String baseUrl;
    private Duration timeout;
    private int maxRetries;
    // getters & setters ...
}
```

Spring Boot 3.x에서는 record가 *기본 후보*가 된다.

```java
@ConfigurationProperties("paybridge.gateway")
public record GatewayProperties(
    String baseUrl,
    Duration timeout,
    int maxRetries
) {}
```

`@ConstructorBinding`이 Spring Boot 3에서 *자동화*됐다. 옛 버전에서는 record나 immutable 클래스에 명시적으로 어노테이션을 붙여 줘야 했지만, 이제는 record 자체가 신호다. `application.yml`의

```yaml
paybridge:
  gateway:
    base-url: https://card.example.com
    timeout: 5s
    max-retries: 3
```

가 그대로 canonical constructor에 바인딩된다. setter가 없으니 *애초에* 변경 가능성이 닫혀 있다.

### nested record와 validation

설정이 복잡해지면 nested record로 표현한다. JSR-380 (Bean Validation) 어노테이션도 그대로 붙는다.

```java
@ConfigurationProperties("paybridge.gateway")
@Validated
public record GatewayProperties(
    @NotBlank String baseUrl,
    @NotNull Duration timeout,
    @Min(0) @Max(10) int maxRetries,
    @Valid Pool pool
) {
    public record Pool(
        @Min(1) int maxSize,
        @NotNull Duration keepAlive
    ) {}
}
```

`@Valid`가 nested record까지 검증을 흘려보낸다. 잘못된 설정값으로 부팅하다 12시간 뒤 운영에서 *터지는* 끔찍한 일을, 부팅 첫 1초에 잡아준다.

### `@RefreshScope`와 immutable의 충돌

그러나 한 가지 짚어야 한다. **`@RefreshScope`와 record는 본질적으로 어긋난다**. `@RefreshScope`는 런타임에 설정을 다시 읽어 빈을 *교체*하는 도구다. immutable record는 *교체* 자체를 거부한다. 어떻게 해야 할까?

두 가지 길이 있다.

첫째, **빈 자체를 교체하는 패턴**. `@RefreshScope`를 record 빈에 직접 붙이고, 같은 컨테이너 안에서 *새 record 인스턴스를 만들어 갈아끼우는* 방식이다. record 자체는 변하지 않지만, 같은 이름의 빈이 가리키는 인스턴스가 바뀐다. Spring Cloud의 `@RefreshScope` 동작 그 자체다.

```java
@RefreshScope
@ConfigurationProperties("paybridge.gateway")
public record GatewayProperties(/* ... */) {}
```

이때 *주의해야 한다*. record 인스턴스를 *필드로 캐시한 빈*은 새 인스턴스를 못 본다. proxy를 통한 lazy lookup이 필요하다.

```java
@Service
@RequiredArgsConstructor
public class GatewayClient {
    private final GatewayProperties properties; // @RefreshScope proxy
    // 매 호출마다 properties.timeout()이 *현재* 값을 반환
}
```

둘째, **변경이 필요한 부분만 분리**. 대부분의 설정은 *부팅 시점에 한 번* 읽고 끝이다. 정말 런타임에 바뀌어야 하는 값(예: 사기 탐지 임계값, feature flag) 몇 개만 떼어 `@RefreshScope`로 관리하고, 나머지는 immutable record로 둔다. *모든 설정이 refresh되어야 하는 건 아니다*. 분리하는 편이 깔끔하다.

PayBridge의 경험을 빌리면, 첫 길보다 둘째 길이 *사고가 덜 난다*. 모든 설정을 refresh 대상으로 두면 어느 빈이 옛 값으로 굳었는지 추적하기가 *번거롭다*. 정말 가변이어야 할 값을 따로 분리하는 편이 좋다.

## §21.3 RestClient — 네 가지 HTTP client의 자리 정리

그 다음으로, HTTP client 이야기를 한 번 정리하자. Spring 진영에 HTTP client가 *네 개*나 있다. 처음 보는 개발자가 *난감해할* 만하다.

| 도구 | 도입 | 모델 | 자리 |
|------|------|------|------|
| `RestTemplate` | Spring 3.0 (2009) | 동기, blocking | legacy — 신규는 권장 안 함 |
| `WebClient` | Spring 5 (2017) | 비동기, reactive | reactive 스택, backpressure |
| Java 11 `HttpClient` | Java 11 (2018) | 동기/비동기 모두 | 표준 라이브러리, Spring 의존 없음 |
| `RestClient` | Spring 6.1 (2023) | 동기, fluent | **신규 동기 호출의 기본** |

Spring 측이 *왜* RestClient를 새로 만들었을까? RestTemplate은 API가 낡았고 fluent하지 않다. WebClient는 fluent하지만 reactive 타입(`Mono`·`Flux`)을 강제한다 — 단순 동기 호출에는 *과하다*. Java 11 HttpClient는 표준이지만 Spring의 `ClientHttpRequestInterceptor`, `MessageConverter`, `Observation` 같은 통합 도구를 못 쓴다. 그 사이의 빈자리를 채우려고 등장한 것이 RestClient다.

```java
// RestClient — Spring 6.1
@Configuration
public class HttpClients {
    @Bean
    RestClient cardAdapterClient(RestClient.Builder builder) {
        return builder
            .baseUrl("https://card.example.com")
            .defaultHeader("X-API-Key", "${paybridge.card.key}")
            .requestInterceptor(observationInterceptor())
            .build();
    }
}

@Service
public class CardAdapter {
    private final RestClient client;

    public AuthResult authorize(AuthRequest req) {
        return client.post()
            .uri("/authorize")
            .body(req)
            .retrieve()
            .body(AuthResult.class);
    }
}
```

fluent하고, 동기다. 코드가 한눈에 읽힌다. *예외*는 자연스럽게 위로 던져진다. stack trace가 친절하다 — 디버깅하는 새벽에 *후련함*을 느끼게 된다.

### 언제 어느 것을 택하나

네 도구의 자리를 정리해 보자.

- **RestClient (기본)**: 동기 호출 + virtual thread. 신규 코드의 99%가 여기다.
- **WebClient**: 진짜로 reactive 스택을 쓰는 경우. backpressure가 필요한 streaming, SSE, WebSocket. 21.4에서 살펴본다.
- **Java 11 HttpClient**: Spring 의존을 피하려는 라이브러리·SDK 작성. CLI 도구. 또는 HTTP/2 push 같은 *특수* 기능.
- **RestTemplate**: 이미 쓰고 있는 옛 코드. 새 코드에는 쓰지 말자.

여기서 한 가지 흥미로운 시너지가 있다. **RestClient + virtual thread**다. RestClient는 내부적으로 blocking I/O를 한다. blocking이 *나쁜 단어*였던 시절이 있었다 — Tomcat 200 thread pool 시대였다. virtual thread 위에서는 blocking이 *cheap*하다. 200개의 동시 호출이 200ms씩 걸리는 외부 API라면, virtual thread 위의 RestClient는 *시퀀셜처럼 보이는 코드로 거의 병렬*에 가까운 처리량을 낸다.

```java
@RestController
public class PaymentController {
    private final RestClient fraudClient;
    private final RestClient cardClient;
    private final ExecutorService executor =
        Executors.newVirtualThreadPerTaskExecutor();

    @PostMapping("/payments")
    public PaymentResponse pay(@RequestBody PaymentRequest req) throws InterruptedException, ExecutionException {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var fraud = scope.fork(() ->
                fraudClient.post().uri("/check").body(req).retrieve().body(FraudResult.class));
            var auth = scope.fork(() ->
                cardClient.post().uri("/authorize").body(req).retrieve().body(AuthResult.class));
            scope.join().throwIfFailed();
            return merge(fraud.get(), auth.get());
        }
    }
}
```

코드가 *동기처럼 보인다*. 그런데 두 외부 API가 *동시에* 호출된다. Java 8 시대에 `CompletableFuture.supplyAsync`를 두 번 부르고 `thenCombine`으로 합치던 코드가 — 그 *번거롭던* 비동기 조합이 — 다섯 줄로 정직하게 표현된다. 8B장에서 살펴본 비동기 조합의 *번거로움*을, 14·16장의 도구가 정리하고, 21장의 RestClient가 마무리한다.

## §21.4 WebFlux는 *어느 자리에* 살아남는가

여기서 솔직해질 자리가 있다. virtual thread가 표준화되면서 *모든 reactive를 대체할 것*이라는 기대가 한동안 있었다. 8B장에서 reactive와 virtual thread의 대비를 본격적으로 짚었다. 그 결론을 한 줄로 회수하자면 — **virtual thread가 있어도 reactive는 살아남는다. 단 그 자리는 좁아졌다.**

그 *좁아진 자리*가 어디인가? 네 곳이다.

### ① backpressure가 필요한 곳 — Kafka consumer fan-out

Kafka에서 100만 건/초 메시지를 consume해 외부 API로 fan-out하는 컨슈머를 떠올려 보자. 외부 API의 처리 속도가 1만 건/초라면, consumer는 자기 속도가 아니라 *외부 API의 속도에 맞춰* 흘러야 한다. 이게 backpressure다.

virtual thread로는 깔끔하지 않다. virtual thread 100만 개를 만들 수는 있지만, 외부 API가 *떠밀리는 속도*를 자연스럽게 표현할 도구가 없다. Reactor의 `Flux.flatMap(concurrency)`은 그 자리에 정확히 들어맞는다.

```java
Flux.from(kafkaPublisher)
    .flatMap(msg -> webClient.post().bodyValue(msg).retrieve().bodyToMono(Result.class),
             /* concurrency */ 32,
             /* prefetch */ 256)
    .subscribe();
```

`concurrency=32`가 한 번에 진행 중인 외부 호출 수를 제한한다. `prefetch=256`이 upstream에서 미리 받아 둘 버퍼 크기다. 두 숫자가 *떠밀림*을 자연스럽게 표현한다.

### ② SSE (Server-Sent Events) — 긴 수명의 스트림

결제 상태 변경 알림을 가맹점 대시보드로 *밀어주는* 채널을 떠올려 보자. 한 연결이 *몇 시간* 살아 있고, 그 동안 띄엄띄엄 이벤트가 흘러간다. WebFlux의

```java
@GetMapping(value = "/payments/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<PaymentEvent> stream(@RequestParam String merchantId) {
    return eventBus.subscribe(merchantId);
}
```

는 *수만 개의 idle 연결*을 가볍게 들고 있을 수 있다. 같은 일을 virtual thread + RestClient로 한다면 — 굳이 못 할 건 없지만 *어색하다*. SSE는 *push 방향의 streaming*이라 reactive의 자연 영역이다.

### ③ WebSocket streaming

마찬가지다. 양방향 streaming, hot/cold stream의 구분, multicast가 필요한 자리. Reactor의 `Sinks.Many`, `share()`, `replay()`가 그 자리에 그대로 들어맞는다.

### ④ R2DBC — reactive 데이터베이스

JDBC는 blocking API다. virtual thread 위에서는 blocking이 *cheap*하니, JDBC + virtual thread로 대부분의 자리가 메워진다. 그런데 *reactive하게 fan-out된 파이프라인*의 한 곳만 JDBC라면, 그 자리가 blocking sink가 돼 backpressure를 깬다. R2DBC는 reactive 파이프라인의 *끝까지* reactive를 보장하려는 시도다.

R2DBC가 모든 자리에서 JDBC를 대체할 도구는 아니다. JPA의 ORM 기능을 누리지 못하고, query DSL도 빈약하다. 그러나 *대규모 reactive 스트림*에서 DB가 종착지라면 — 그 한 자리에서는 R2DBC가 답이다.

### 결론 — 좁아졌지만 사라지지 않는다

네 자리를 보면 패턴이 보인다. *진짜 streaming 모델*이 필요한 자리, *떠밀림*을 명시적으로 표현해야 하는 자리, *연결의 양*이 thread보다 더 많을 수 있는 자리. 이 세 가지가 reactive의 자연 영역이다. virtual thread는 *thread-per-request*의 부활이지, *push-based streaming*의 부활이 아니다. 두 모델은 다른 문제를 푼다.

PayBridge에서도 같은 그림이 그려져 있다. 결제 API 게이트웨이(요청·응답 한 사이클)는 virtual thread + RestClient로 옮겼고, 가맹점 알림 channel과 정산 큐 fan-out은 WebFlux + R2DBC로 유지한다. *모든 코드를 한 모델로 통일하려고 애쓰지 말자*. 자리에 맞는 도구를 쓰는 편이 낫다.

## §21.5 `spring.threads.virtual.enabled=true`의 본격 활용

14장에서 한 줄로 호명만 했던 이야기를 이제 본격적으로 풀어보자.

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

Spring Boot 3.2부터 등장한 한 줄이다. 한 줄이 무엇을 바꾸나? *Tomcat의 request handler executor*를 platform thread pool에서 virtual thread per task executor로 갈아끼운다. `@Async`의 기본 executor도, `TaskExecutionAutoConfiguration`이 만드는 `taskExecutor` 빈도, 모두 virtual thread를 쓰게 된다.

### 서블릿 컨테이너별 지원 상태

| 컨테이너 | virtual thread 지원 | 비고 |
|----------|---------------------|------|
| Tomcat 10.1+ | ✓ | Spring Boot 3.2부터 자동 |
| Jetty 12+ | ✓ | `VirtualThreadPool` 옵션 |
| Undertow | 제한적 | XNIO 워커 스레드 모델, 부분 적용 |
| Netty | N/A | event loop 모델 — virtual thread 불필요 |

Spring Boot 3.x의 기본은 Tomcat이다. 한 줄 설정으로 끝난다. Jetty로 갈아끼울 때는 `JettyVirtualThreadPool` 설정을 명시적으로 켜자.

### JDBC 드라이버의 Loom-readiness

여기서 *반드시 짚어야 할* 부분이 있다. **JDBC 드라이버와 connection pool이 Loom-ready인가**다. 15장에서 살펴본 pinning 문제의 가장 흔한 발원지가 바로 이 두 곳이다.

| 라이브러리 | Loom-ready 버전 | 이슈 |
|-----------|-----------------|------|
| HikariCP | 5.1.0+ | 옛 버전은 `synchronized` 블록에서 pin |
| MySQL Connector/J | 8.4.0+ | 옛 버전은 socket I/O에서 pin |
| PostgreSQL JDBC | 42.7.0+ | 비교적 일찍부터 안전 |
| MariaDB Connector/J | 3.3.0+ | 신규 버전 권장 |
| Oracle JDBC | 23ai 이상 권장 | 옛 버전 호환성 부족 |

PayBridge의 *덜컥*했던 새벽이 정확히 여기서 시작됐다. HikariCP 4.x 버전이 남아 있던 인스턴스에서 virtual thread를 켜자 deadlock이 났다. JFR의 `jdk.VirtualThreadPinned` 이벤트로 진단하고, HikariCP를 5.1.0으로 올려 해결했다. *기억해두자*. virtual thread를 켤 때는 *반드시* 의존성 트리의 connection pool과 JDBC 드라이버 버전을 확인하자. Java 24의 JEP 491이 `synchronized` 블록의 pinning을 해결하지만, 21에 머무른다면 *수동으로 버전을 정렬*하는 편이 안전하다.

### Spring Boot 3.4의 부속 도구

같이 챙겨야 할 *주변 도구*도 몇 개 있다. Spring Boot 3.4에 와서 깔끔해진 것들이다.

**SSL bundle.** SSL 설정이 여기저기 흩어져 있던 *번거로움*을 정리한 도구다.

```yaml
spring:
  ssl:
    bundle:
      pem:
        card-adapter:
          keystore:
            certificate: classpath:certs/card.crt
            private-key: classpath:certs/card.key
          truststore:
            certificate: classpath:certs/card-ca.crt
```

```java
@Bean
RestClient cardAdapterClient(RestClient.Builder builder, SslBundles bundles) {
    return builder
        .baseUrl("https://card.example.com")
        .apply(b -> b.sslBundle(bundles.getBundle("card-adapter")))
        .build();
}
```

여러 외부 API마다 다른 인증서를 쓰는 결제 시스템에서 *후련한* 도구다.

**Docker Compose support.** 로컬에서 외부 서비스(Postgres·Redis·Kafka)를 띄울 때 `compose.yml`을 자동으로 인식한다. `application.yml`의 datasource URL을 *덮어쓰지 않고도* 컨테이너 주소가 자동 주입된다.

```yaml
# compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: paybridge
```

`spring-boot-docker-compose` 의존성만 추가하면 `mvn spring-boot:run`이 알아서 compose를 띄우고 datasource를 잡아준다. 로컬 개발의 *지긋지긋한* 환경 변수 셋업이 줄어든다.

## §21.6 Observability + JFR — production 모니터링의 한 페이지

virtual thread를 켰는데 *덜컥*하는 일을 막으려면, observability를 같이 챙겨야 한다. Spring 6는 Micrometer 기반의 Observation API를 1급 시민으로 두고 있다.

```java
@RestController
@RequiredArgsConstructor
public class PaymentController {
    private final ObservationRegistry registry;
    private final CardAdapter cardAdapter;

    @PostMapping("/payments")
    public PaymentResponse pay(@RequestBody PaymentRequest req) {
        return Observation.createNotStarted("payment.authorize", registry)
            .lowCardinalityKeyValue("merchant_type", req.merchantType())
            .observe(() -> cardAdapter.authorize(req));
    }
}
```

`Observation`이 한 번에 *trace span*, *metrics*, *logs context*를 만든다. Zipkin·Jaeger 같은 trace 백엔드, Prometheus 같은 metrics 백엔드, MDC를 통한 logs context — 한 줄에 세 곳이 동시에 채워진다.

virtual thread에서 *반드시* 켜야 할 것이 하나 있다. **JFR (Java Flight Recorder)**다. `jdk.VirtualThreadPinned` 이벤트가 자동으로 수집된다.

```bash
java -XX:StartFlightRecording=filename=paybridge.jfr,duration=60s,settings=profile \
     -jar paybridge-gateway.jar
```

운영 중에도 부담이 거의 없다 (1~2% overhead). 수집된 `.jfr` 파일을 JMC(JDK Mission Control)로 열면 *어느 코드에서 pinning이 났는지* 한눈에 보인다. 15장에서 본 그 도구다.

production에서는 한 발 더 나간다. Spring Boot Actuator의 `/actuator/threaddump`로 virtual thread 덤프를 받을 수 있고, `/actuator/metrics/jvm.threads.virtual.live`로 라이브 카운트를 확인할 수 있다. *문제가 생기기 전*에 보이는 도구를 켜두는 편이 낫다.

## §21.7 결제 마이크로서비스 — 도구가 한 자리에 모이는 후련함

이제 책 전체에서 쌓은 도구를 한 컨트롤러에 모아보자. PayBridge의 `/payments/authorize` 엔드포인트다.

```java
// 도메인 모델 — records + sealed
public record PaymentRequest(
    @NotBlank String merchantId,
    @NotNull @Positive BigDecimal amount,
    @NotBlank String currency,
    @Valid CardInfo card
) {
    public record CardInfo(
        @Pattern(regexp = "\\d{13,19}") String number,
        @Pattern(regexp = "\\d{2}/\\d{2}") String expiry
    ) {}
}

public sealed interface PaymentResult permits Approved, Declined, Failed {
    record Approved(String authCode, Instant capturedAt) implements PaymentResult {}
    record Declined(String reason, String issuerMessage) implements PaymentResult {}
    record Failed(String errorCode, Throwable cause) implements PaymentResult {}
}

// 컨트롤러 — virtual thread + structured concurrency + RestClient
@RestController
@RequiredArgsConstructor
public class PaymentController {
    private final RestClient fraudClient;
    private final RestClient cardClient;
    private final PaymentRepository repository;
    private final ObservationRegistry observations;

    @PostMapping("/payments/authorize")
    public ResponseEntity<PaymentResponse> authorize(@Valid @RequestBody PaymentRequest req)
            throws InterruptedException {
        return Observation.createNotStarted("payment.authorize", observations)
            .lowCardinalityKeyValue("merchant", req.merchantId())
            .observe(() -> {
                PaymentResult result = process(req);
                return toResponse(result);
            });
    }

    private PaymentResult process(PaymentRequest req) throws InterruptedException {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var fraud = scope.fork(() ->
                fraudClient.post().uri("/check").body(req).retrieve().body(FraudResult.class));
            var auth = scope.fork(() ->
                cardClient.post().uri("/authorize").body(req).retrieve().body(AuthResult.class));
            scope.join().throwIfFailed();

            return switch (auth.get()) {
                case AuthResult.Ok(var code) when !fraud.get().suspicious() ->
                    new PaymentResult.Approved(code, Instant.now());
                case AuthResult.Ok(var __) ->
                    new PaymentResult.Declined("FRAUD_SUSPECTED", "blocked by risk engine");
                case AuthResult.Rejected(var msg) ->
                    new PaymentResult.Declined("ISSUER_REJECTED", msg);
            };
        } catch (Exception e) {
            return new PaymentResult.Failed("UPSTREAM_ERROR", e);
        }
    }

    private ResponseEntity<PaymentResponse> toResponse(PaymentResult r) {
        return switch (r) {
            case PaymentResult.Approved(var code, var at) ->
                ResponseEntity.ok(new PaymentResponse.Success(code, at));
            case PaymentResult.Declined(var reason, var msg) ->
                ResponseEntity.status(402).body(new PaymentResponse.Failure(reason, msg));
            case PaymentResult.Failed(var code, var __) ->
                ResponseEntity.status(503).body(new PaymentResponse.Failure(code, "retry"));
        };
    }
}
```

여기 모인 도구를 헤아려 보자.

- **record DTO**: 요청·응답의 신원 (11장)
- **Bean Validation**: nested record까지 검증 (21.2)
- **sealed interface `PaymentResult`**: 합 타입으로 결과 모델링 (12장)
- **pattern matching `switch`**: 결과 분기를 *exhaustive*하게 (13장)
- **virtual thread (`spring.threads.virtual.enabled=true`)**: thread-per-request 부활 (14장)
- **`StructuredTaskScope`**: 두 외부 호출의 *구조적* 병렬 (16장)
- **RestClient**: 동기 fluent HTTP (21.3)
- **Observation API**: trace + metrics + logs (21.6)

같은 컨트롤러를 *Java 8*로 적었다면 어땠을까? 80줄짜리 코드가 200줄로 늘어났을 것이다. DTO는 Lombok `@Value`나 직접 작성한 클래스로, 결과 분기는 `instanceof` 캐스트 사다리로, 두 외부 호출은 `CompletableFuture.supplyAsync` 두 번과 `thenCombine`으로 — 줄 수도 늘어나지만 *읽히는 정도*가 다르다. 같은 의도를 표현하는데 손가락 무게가 다르다.

코드를 위에서 아래로 한 번만 읽어 보자. *비즈니스 로직만 보인다*. 어떻게 thread를 다루는지, 어떻게 결과를 분기하는지, 어떻게 검증하는지 — 그 *기계적인 부분*이 언어와 프레임워크의 어휘 안으로 사라져 있다. 11년 동안 자바가 걸어온 길의 *후련한* 결말이다.

## §21.8 21에 머무를지, 25로 갈지

마지막 한 자리를 정리하자. 모든 자바 개발자가 마주하는 *판단*이다. *우리 서비스는 21에 머물러야 할까, 25로 가야 할까?*

PayBridge의 결정을 그대로 빌려 와 일반화해 보자.

| 판단 기준 | 21 (이중 LTS) | 25 (현재 LTS) |
|-----------|---------------|---------------|
| 지원 기간 | Oracle 8년 (2031) | Oracle 8년 (2033) |
| 검증 깊이 | 2년 이상 production 검증 | 갓 나옴, 검증 진행 중 |
| 라이브러리 호환 | 거의 모든 라이브러리 ✓ | 일부 옛 라이브러리 미검증 |
| Spring Boot | 3.2~3.4 모두 ✓ | 3.4+ 권장 |
| virtual thread pinning | JEP 491 *없음* — 옛 `synchronized` 주의 | JEP 491 적용 — pinning 거의 사라짐 |
| AOT cache | CDS만 (3.3+) | JEP 483/514 본격 |
| Compact Object Headers | 없음 | 있음 — heap ~10~25% 절감 |
| Stream Gatherers | 없음 | 표준 |

이 표가 결정의 *반*이다. 나머지 반은 *서비스의 성격*이다.

- **고도 안정성 우선 (금융 거래, 결제 게이트웨이)**: 21에 머무는 편이 낫다. 검증된 동작, 라이브러리 매트릭스의 *익숙함*이 안정성의 일부다.
- **신규 도구 활용 우선 (대용량 캐시 서비스, batch 정산, AI/ML inference)**: 25로 가는 편이 낫다. Compact Object Headers의 메모리 절감, AOT cache의 콜드 스타트 단축, Gatherer의 표현력이 *실제 ROI*로 돌아온다.
- **virtual thread 본격 활용**: 25 권장. JEP 491이 pinning을 거의 없앤다.
- **마이그레이션 비용 (구버전 라이브러리, 사내 빌드 인프라)**: 21 유지가 안전하다. *완벽한 LTS*는 *내 코드가 도는 LTS*다.

PayBridge는 두 갈래로 갔다. 결제 게이트웨이는 21에 머물고, 정산 배치와 사기 탐지는 25로 갔다. *서비스마다 다른 LTS를 쓰는 것*이 11년 전에는 *번거롭게* 들렸겠지만, 지금은 GitHub Actions toolchain·Docker base image·Spring Boot 의존성 매니지먼트가 모두 *서비스별 자바 버전*을 자연스럽게 다룬다. 한 LTS로 사내 표준을 강제할 이유는 옛날만큼 강하지 않다.

한국 사례를 짚어보자. 우아한형제들의 기술 블로그(`techblog.woowahan.com`)는 virtual thread 전환 측정을, 카카오페이의 기술 블로그(`tech.kakaopay.com`)는 Spring에서 virtual thread를 실제로 어떻게 켰는지를 적어 두었다. velog의 여러 개발자 글, `findstar.pe.kr` 같은 한국 개발자 블로그도 *현장의 측정값*을 공유한다. 이 글들이 공통으로 말하는 것이 하나 있다 — *직접 측정해라*. 외부 글의 수치를 그대로 우리 서비스에 옮겨 적용할 수는 없다. JFR을 켜고, JMH로 마이크로 벤치마크를 돌리고, *우리 워크로드에서* 측정한 숫자로 판단하자.

## 마무리

Spring Boot 3.x × Java 21/25의 결합점을 한 장에 모았다. *Spring 고유*의 자리만 다섯 곳을 짚었다 — Spring Data record projection + AOT repositories, `@ConfigurationProperties` + record + `@RefreshScope`, RestClient의 자리, WebFlux가 살아남는 네 영역, `spring.threads.virtual.enabled` + observability. 여기에 더해 결제 마이크로서비스 한 컨트롤러에 책 전체의 도구를 모으는 *후련함*을 보여줬다. 21에 머무를지 25로 갈지의 판단 기준도 함께 정리했다.

이 장이 책의 *현장 정착점*이다. 11년 동안 자바가 걸어온 길이 *Spring과 만나는 자리*에서 어떻게 표현되는지 한 줄로 이어진다. 우리가 매일 적는 컨트롤러, repository, configuration, HTTP client — 그 평범한 자리에 현대 자바의 모든 도구가 자연스럽게 들어가 있다. 한 줄짜리 record가 어떻게 그곳에 도달했는지, 한 줄짜리 `spring.threads.virtual.enabled`가 어떤 11년의 진화 끝에 가능해졌는지를 *기억해두자*.

그렇다면 여기서 멈출까? 자바는 어디까지 갈까? Project Valhalla의 value class, Project Amber의 다음 카드, Project Babylon의 GPU·이질 컴퓨팅, Project Leyden의 종착점 — 26 이후의 자바가 무엇을 준비하고 있는지 마지막 장에서 함께 들여다보자. 1장에서 시작한 PayBridge 이야기를 *5년 뒤*로 한 번 연장해 보자. 책의 마지막 장이다.
