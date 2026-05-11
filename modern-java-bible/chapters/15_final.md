# 15장. Pinning · ThreadLocal · 함정들 — Virtual Thread가 우리를 실망시키는 자리

VT를 켰는데 오히려 deadlock이 났다고 해보자.

`spring.threads.virtual.enabled=true` 한 줄을 추가하고 운영에 올린 다음 날 새벽, 결제 컨트롤러가 멈췄다. p99가 떨어지기는커녕 *모든* 요청이 timeout으로 떨어졌다. JStack을 찍어 보면 thread 수십 개가 같은 `synchronized` 블록 앞에서 대기 중이다. 외부 결제 게이트웨이의 SDK가 내부적으로 `synchronized(connectionLock)`로 보호된 메서드 안에서 소켓 read를 하고 있는 것이다. 그 한 자리에서 carrier thread가 unmount되지 못하고 *못 박혔다*. 결제 쪽 carrier가 다 잠기자 다른 외부 호출도 줄을 잇지 못해 멈췄다. 정확히 14장에서 약속한 *비약*과 반대 방향이다.

켰는데 왜 더 느려졌을까. 왜 도구는 약속을 지키지 못했을까. 그렇다면 우리는 — 그 약속이 깨지는 자리를 미리 알고, JFR을 켜서 *조용히 막혀 가는 시그널*을 잡아내고, 라이브러리의 이주 상태를 확인할 수 있을까. 이 장에서 그 *끔찍한 새벽*을 정직하게 들여다보자. 결론을 먼저 짚자면 — virtual thread는 만능이 아니다. 그러나 함정을 알면 안전하다.

## Pinning이란 무엇인가

먼저 용어부터 정리하자. **pinning**은 virtual thread가 carrier thread에서 *unmount되지 못하는* 상황을 말한다. 14장에서 살펴봤듯, virtual thread의 마법은 blocking 호출을 만났을 때 자동으로 unmount되어 carrier를 자유롭게 풀어주는 데 있다. 그 unmount가 막히는 자리, 그 자리가 pinning이다.

pinning이 일어나면 virtual thread는 *그 carrier에 못 박힌 채로* blocking 호출을 마칠 때까지 자리를 차지한다. 그 동안 그 carrier에는 다른 virtual thread가 mount되지 못한다. carrier pool의 크기는 CPU 코어 수 — 보통 4~32개다. pinning이 그 절반에 일어나면 throughput은 절반이 된다. 두 자리 모두 일어나면 *14장에서 본 800ms*가 그대로 돌아온다. 더 나쁜 경우, carrier가 모두 잠긴 채로 외부 호출의 응답을 *서로 기다리면* deadlock이 된다. 새벽에 결제 컨트롤러가 멈춘 그 자리가 바로 그렇다.

이 함정의 뿌리를 정확히 들여다보려면 30년 묵은 JVM 모니터의 구현으로 들어가 봐야 한다.

## `synchronized`의 30년 묵은 짐

자바의 `synchronized` 블록은 1995년부터 지금까지 *intrinsic monitor*라는 JVM 내부 메커니즘으로 구현돼 왔다. monitor는 OS thread의 신원으로 lock을 추적한다. 같은 OS thread가 두 번 들어오면 reentrant로 허용하고, 다른 OS thread가 들어오려 하면 대기시킨다. 30년 동안 잘 동작했다. 자바 = OS thread라는 등식이 깨지기 전까지는.

virtual thread가 등장하자 문제가 생겼다. virtual thread는 OS thread를 *옮겨 다닌다*. carrier A에 mount됐다가 unmount된 뒤 다시 mount될 때 carrier B로 옮겨갈 수 있다. JVM 모니터가 OS thread 신원으로 lock을 추적하는데, 그 OS thread가 *바뀐다면* lock의 일관성이 깨진다. OpenJDK 팀의 선택은 보수적이었다. virtual thread가 `synchronized` 블록 안에 *진입*해 있을 때는 unmount를 *금지*한다. 그 시간 동안 그 virtual thread는 carrier에 *못 박힌 채로* 살아야 한다.

Java 21·22·23의 virtual thread가 산업에서 부딪힌 가장 큰 벽이 이것이다. 모든 라이브러리가 `synchronized`를 쓴다. JDBC 드라이버도, HTTP 클라이언트도, connection pool도. 그중 하나가 외부 I/O를 `synchronized` 블록 안에서 호출하면 그 자리가 pinning이 된다. 가장 흔한 예가 HikariCP의 5.0 미만 버전 — `synchronized(ConnectionState)` 안에서 JDBC 연결을 얻어내고 있었다. JDBC 연결을 얻는 일은 보통 빠르지만, pool이 비어 있으면 *기다린다*. 그 기다림이 virtual thread를 carrier에 *못 박는다*.

이 자리에서 라이브러리 생태계의 이주가 시작됐다. 2023~2024년에 걸쳐 주요 라이브러리들이 `synchronized` → `ReentrantLock`으로 *옮기는 PR*을 받았다. `ReentrantLock`은 monitor를 쓰지 않고 `java.util.concurrent`의 큐와 CAS로 구현돼 있어서 virtual thread를 carrier에 못 박지 않는다.

| 라이브러리 | 이주 상태 (2025 기준) | 메모 |
|---|---|---|
| HikariCP | 5.1.0+ (5.0은 부분) | `synchronized` 다수 제거. JDBC 드라이버의 pinning은 별개 |
| Caffeine | 3.1.0+ | 거의 모든 `synchronized`를 `ReentrantLock`으로 |
| Apache HttpClient | 5.3+ | 5.2는 connection lock에서 pinning 잔존 |
| MySQL Connector/J | 8.3+ | 8.2 이하는 statement 실행 자리에서 pinning |
| Postgres JDBC | 42.7+ | 거의 해소. driver 자체는 cleaner |
| Oracle JDBC | 23ai+ | 일부 잔존 보고. driver별 정밀 audit 필요 |

이주가 완벽하지는 않다. 직접 인용한 한국 기업의 사례에서도 *카카오페이*는 production 도입 과정에서 외부 SDK 일부가 `synchronized` 블록 안에서 소켓 I/O를 호출하는 자리를 발견했고, 그 자리들을 우회하거나 SDK를 교체해야 했다. *Cashfree Payments*도 비슷하다. *7 Key Lessons* 글의 핵심 중 하나는 "도입 전에 connection pool과 외부 SDK의 Loom-readiness를 audit해라"였다. 한 자리만 안 풀려도 carrier가 못 박힌다.

(Netflix의 production deadlock 사례는 한 차례 화제가 됐다. 공식 post-mortem은 핵심 정보가 정리된 형태로 공개되지 않았으나, *TheServerSide*의 정리에 따르면 큰 그림은 — `synchronized` 안의 외부 호출이 carrier를 다 잠그며 컨트롤러 전체가 멈춘 — 우리가 새벽에 만난 그 시나리오다. *사실 확인 필요*. 정확한 사정이 궁금하다면 Netflix Tech Blog의 후속 글을 추적하길 권한다.)

## JEP 491: Java 24가 가져온 해방

다행히도 이 함정은 *현재진행형 해소* 중이다. Java 24의 **JEP 491**은 JVM 모니터의 30년 묵은 구현을 바꿨다. 핵심 변화 한 줄이다 — *monitor가 OS thread 신원이 아니라 virtual thread 신원을 추적한다*. 그 결과 `synchronized` 블록 안에서도 virtual thread를 unmount할 수 있게 됐다.

JEP 491의 의미를 정직하게 짚자.

- Java 24 이후로, `synchronized` 안의 blocking I/O는 더 이상 pinning이 아니다.
- 라이브러리의 `synchronized` → `ReentrantLock` 이주는 *여전히 권장*되지만, 그 자리에서 운영을 막는 *blocker*는 아니게 됐다.
- Java 21 LTS에 머무는 한, 이 해방은 받지 못한다. 21 LTS 위에서 운영한다면 라이브러리 audit이 *여전히 필수*다.

여기서 결정의 자리가 생긴다. *21 LTS에 머물 것인가, 24·25로 갈 것인가*. 운영 안정성, 보안 패치 주기, 라이브러리 호환성 — 모든 결정 요소를 한 번에 저울에 올려야 한다. 일반적인 권장은 이렇다 — 신규 프로젝트라면 25 LTS를 노리고, 기존 시스템은 21에 머물되 라이브러리 audit과 pinning 모니터링을 *반드시* 설치해두자.

pinning이 *원천적으로* 사라지는 자리가 있느냐 하면, 그렇지는 않다. JEP 491 이후에도 두 자리는 여전히 pinning이다.

- **JNI/native call** 안의 코드. native 영역에서는 JVM이 unmount를 시킬 수 없다.
- **class initializer** 실행 중. JVM은 class 초기화의 원자성을 지키기 위해 그 동안 unmount를 금지한다.

이 둘은 *기억해두자*. 두 자리에서 외부 I/O를 호출하는 코드는 — 24·25에서도 — pinning을 만든다.

## ThreadLocal 함정: 수백만 thread × 캐시

pinning만 함정이 아니다. 더 *조용히* 메모리를 망치는 함정이 있다. **ThreadLocal**이다.

자바 코드에 ThreadLocal이 얼마나 깊이 박혀 있는지 한 번 짚어보자. `SimpleDateFormat`은 thread-safe하지 않아서 보통 ThreadLocal로 캐싱한다. Hibernate는 `Session`을 ThreadLocal에 묶는다. Spring의 `RequestContextHolder`는 `LocaleContextHolder`와 `SecurityContextHolder`까지 ThreadLocal 기반이다. SLF4J의 MDC도 ThreadLocal이다. JDBC 트랜잭션 동기화는 ThreadLocal로 connection을 묶는다.

이 패턴이 *thread pool*과 잘 맞물려 있었다. 200개 thread 풀이 있다면 ThreadLocal 캐시도 200개다. SimpleDateFormat 200개 — 큰 메모리는 아니다. Hibernate Session 200개 — 운영 가능한 크기다. ThreadLocal은 *thread의 lifetime*에 묶여 살고, thread는 *재사용*되므로 캐시도 재사용된다. 자바의 *thread 자원이 비싸다*는 전제 위에 ThreadLocal이라는 도구가 자연스럽게 자리 잡았다.

이제 virtual thread를 켜자. thread는 더 이상 *재사용*되지 않는다. *task마다 새로 만든다*. 동시에 100만 개의 virtual thread가 살 수 있다.

곱셈이 무서워진다. SimpleDateFormat × 100만 = 100만 개. 1KB짜리 객체라도 1GB다. Hibernate Session × 100만 — 가능한 시나리오가 아니지만, 이론적으로는 폭발이다. MDC가 user context를 들고 있다면 그것도 100만 벌. 우리 머릿속의 *thread pool 곱하기 캐시*라는 산수가 *task 수 곱하기 캐시*로 바뀌었다. 자원 계산의 단위가 통째로 달라진 것이다.

이 함정은 *조용하다*. pinning은 새벽에 한 번 일어나면 컨트롤러가 멈춰서 페이지를 친다. ThreadLocal 폭발은 그렇게 극적이지 않다. heap이 천천히 차오르고, GC가 점점 자주 일어나고, p99가 *서서히* 솟구친다. JFR을 켜서 heap profile을 보지 않으면 발견하기 어렵다. *찜찜한* 메모리 사용량 증가가 일어나면 가장 먼저 ThreadLocal을 의심하는 편이 낫다.

JDK가 준 길은 두 갈래다.

- **ThreadLocal을 줄여라**. 정말 필요한 자리만 남기고, 캐싱 대신 매번 새로 만들거나(예: `DateTimeFormatter.ISO_LOCAL_DATE`는 immutable이라 ThreadLocal이 필요 없다) thread-safe한 대안으로 옮긴다.
- **ScopedValue로 옮겨라**. JEP 506의 `ScopedValue`가 ThreadLocal의 후계자다. immutable이고, 부모→자식 binding이며, scope이 끝나면 *자동 cleanup*된다. 100만 virtual thread가 각자 `ScopedValue`로 user context를 들고 있어도 메모리는 폭발하지 않는다. 자세한 내용은 16장에서 다룬다.

`InheritableThreadLocal`도 함정에 들어가 있다는 점은 짚어 둘 만하다. 부모에서 자식으로 *복사*되는 패턴은 ThreadLocal보다 *더 위험*하다. virtual thread는 부모-자식 관계가 흔하기 때문에 한 컨트롤러가 fan-out한 자식 모두에 ThreadLocal이 복사된다. 16장의 ScopedValue가 정확히 이 자리를 노리고 만들어졌다.

## 모니터링: JFR과 `tracePinnedThreads`로 잡아내자

이제 *진단 절차*를 한 페이지로 정리하자. virtual thread를 도입한 시스템이라면 — 도입 첫날에 — 이 둘 중 하나는 반드시 설치해두는 편이 낫다.

**1. 가장 가벼운 길: `-Djdk.tracePinnedThreads=full`**

JVM 옵션 한 줄이다. virtual thread가 pinning되면 stack trace가 stderr로 찍힌다. 개발/스테이징 환경에서 *어디서 pinning이 나는지*를 빠르게 파악하기 좋다. 단, production에는 권장되지 않는다 — 모든 pinning 이벤트가 로그를 찍으면 부하가 크다.

```
-Djdk.tracePinnedThreads=full
```

`short` 옵션도 있다. trace의 일부만 찍어서 부하가 가볍다. 일단 *어디서 일어나는지*만 알면 되니 `short`로 시작하는 편이 낫다.

**2. production용 길: JFR `jdk.VirtualThreadPinned` 이벤트**

Java Flight Recorder의 `jdk.VirtualThreadPinned` 이벤트가 정확히 이 자리를 위해 추가됐다. JFR을 켜 두면 pinning이 일어난 자리, 시간, stack trace가 이벤트로 기록된다. 부하가 거의 없어서 production에 *상시*로 켜 둘 만하다.

```bash
jcmd <pid> JFR.start name=pinning duration=5m filename=pinning.jfr \
    settings=profile
```

또는 JVM 시작 시:

```
-XX:StartFlightRecording=name=pinning,settings=profile,filename=pinning.jfr
```

기본 profile은 무거우니 `-XX:StartFlightRecording=name=pinning,duration=5m,settings=profile,jdk.VirtualThreadPinned#enabled=true` 같이 *원하는 이벤트만* 켜는 편이 효율적이다. 생성된 `.jfr` 파일은 JDK Mission Control (JMC) 또는 IntelliJ의 JFR 분석기로 연다.

**3. ThreadLocal 폭발 진단**

heap dump (`jcmd <pid> GC.heap_dump`)를 떠서 `ThreadLocal$ThreadLocalMap` 인스턴스 수를 확인한다. virtual thread를 켠 시스템에서 그 수가 *수만~수십만*에 이르면 폭발 직전이다. 어떤 ThreadLocal이 가장 많은 메모리를 잡고 있는지는 dominator tree로 추적할 수 있다.

**진단 절차 한 페이지**

새벽에 깨서 *VT가 의심된다*면 순서는 이렇다.

1. JFR을 켜서 5분 기록한다 — `jdk.VirtualThreadPinned` 이벤트가 있는지 본다.
2. 이벤트가 있다면 stack trace를 본다 — 어느 라이브러리의 어느 메서드인가.
3. 그 라이브러리의 *Loom-ready* 버전을 확인한다. 위 표가 첫 출발이다.
4. 라이브러리 업그레이드가 어렵다면 — 그 자리만 platform thread로 격리한다. `Executors.newFixedThreadPool()`을 따로 두고, 문제의 호출만 그 풀에 위임한다.
5. 이벤트가 없는데 메모리가 새는 것 같으면 ThreadLocal을 의심한다 — heap dump를 본다.

## CPU-bound 작업에는 쓰지 말 것

virtual thread의 약속은 *I/O bound* 워크로드에 한정된다. CPU-bound 작업 — 행렬 곱셈, 이미지 인코딩, 암호 계산, JSON 파싱이 분 단위인 거대 페이로드 — 에는 virtual thread가 *효과 없다*. 오히려 *느려질* 수 있다. 이유는 단순하다.

CPU-bound 작업은 *unmount되지 않는다*. blocking I/O 호출이 없기 때문이다. virtual thread가 carrier에 mount되어 CPU를 잡고 계산을 한다. carrier 수가 CPU 코어 수와 같으니, 결국 *코어 수만큼*의 동시성으로 돌아간다. 100만 개를 만들어도 한 번에 *코어 수만큼*만 진행된다. 평범한 `ForkJoinPool` 또는 `newFixedThreadPool(코어 수)`과 결과가 같다 — 다른 점은 virtual thread를 만들고 스케줄링하는 *오버헤드*가 더해진다는 것이다.

원칙은 이렇다.

- **I/O bound** (외부 API·DB·디스크) → virtual thread 적합.
- **CPU bound** (계산·인코딩) → `ForkJoinPool` 또는 GPU.
- **혼합** → I/O 부분은 virtual thread, 계산 부분은 별도 풀로 *위임*한다.

세 번째 패턴은 자주 만난다. 결제 컨트롤러가 외부 API 세 개를 합치고(I/O), 응답을 받은 뒤 암호 서명을 검증한다(CPU). 둘을 같은 virtual thread에서 다 처리해도 동작은 한다 — 다만 *서명 검증*이 카운트당 50ms씩 걸리면 그 50ms 동안 carrier가 잠긴다. 100만 동시 요청이 그 자리를 동시에 통과하면 carrier 풀이 그 자리에서 사상자가 난다. 별도의 CPU pool로 위임하는 편이 낫다.

```java
// CPU 작업 분리
private static final ExecutorService cpu = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors());

public CheckoutResponse checkout(...) {
    try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<Payment> pay  = scope.submit(() -> billing.charge(orderId));
        // ...
        Payment p = pay.get();
        // 서명 검증은 별도 CPU 풀로
        boolean valid = cpu.submit(() -> verifySignature(p)).get();
        return new CheckoutResponse(p, valid);
    }
}
```

이 *나누는 감각*은 virtual thread를 production에서 안전하게 쓰는 첫걸음이다.

## 적합도 매트릭스

한 페이지에 정리하자. 어떤 워크로드에 virtual thread를 켤지, *우선* 표로 본다.

| 워크로드 | 적합도 | 메모 |
|---|---|---|
| Spring MVC REST API (외부 API·DB 호출 많음) | ★★★ | 14장의 그 자리. p99 즉시 개선 |
| Webhook receiver / fanout (수만 동시) | ★★★ | thread-per-request의 정수 |
| Long-polling / SSE | ★★★ | 수만 connection 유지에 적합 |
| 메시지 컨슈머 (Kafka, RabbitMQ) | ★★ | I/O bound면 적합. 컨슈머 그룹 관리 별도 |
| Reactive (WebFlux) 시스템 | — | 이미 non-blocking. 도입 의미 없음 |
| CPU-bound 배치 | ★ | 효과 없음. ForkJoinPool 사용 |
| 동기 트랜잭션 chain (다수 DB 호출) | ★★★ | thread 풀 한계 즉시 해소 |
| `synchronized` 많은 옛 라이브러리 사용 | ★ (Java 21) / ★★★ (Java 24+) | 라이브러리 audit 필수 |
| 작은 함수 다수 (GraalVM serverless) | — | startup·footprint가 우선. AOT 19장 |

★★★는 *지금 켜라*. ★★는 *audit 후 켜라*. ★는 *효과 미미하거나 위험*. —는 *부적합*.

## 한국 사례: 카카오페이의 정직한 측정

이쯤에서 한국 사례를 하나만 더 들여다보자. *카카오페이*는 *"Virtual Thread에 봄(Spring)은 왔는가"* 글에서 platform thread → virtual thread 전환을 실측한 결과를 공유했다. 핵심을 정리하면 이렇다.

- *외부 API 호출이 다수인 결제 컨트롤러*에서, virtual thread 도입 후 동일 부하에서 p99 latency가 의미 있게 떨어졌다.
- container 메모리 사용량은 *증가*했다. 14장에서 짚은 그 자리다 — stack이 heap에 살기 때문이다.
- 도입 과정에서 외부 SDK 일부의 `synchronized` 자리에서 pinning이 발견됐고, *해당 SDK 우회* 또는 *교체*가 필요했다.
- ThreadLocal 기반 컨텍스트 전달 코드는 *audit*이 필요했다.

이 정직한 정리가 한국 production에서 가장 신뢰할 만한 자료다. 글 자체에 정확한 수치와 그래프가 있으니, virtual thread 도입을 고민 중이라면 한 번 읽어 보는 편이 낫다.

## 마무리

virtual thread는 만능이 아니다. *켜기만 하면 모든 게 빨라진다*는 약속은 단서 없이는 거짓이다. `synchronized` 안의 외부 I/O는 carrier에 못 박히고, ThreadLocal에 무심코 들어 있는 캐시는 100만 곱하기로 폭발하며, CPU-bound 작업은 오히려 carrier를 잠근다. JEP 491이 Java 24에서 `synchronized` pinning을 해소했지만, 21 LTS에 머무는 한 라이브러리 audit은 여전히 필수다.

그러나 함정을 알면 안전하다. JFR의 `jdk.VirtualThreadPinned` 이벤트로 *조용한 시그널*을 잡고, 라이브러리의 Loom-readiness를 도입 전에 확인하고, ThreadLocal을 ScopedValue로 옮기고, CPU 작업을 별도 풀로 분리한다. 이 네 가지 습관이 virtual thread를 *약속의 자리*로 데려간다.

ThreadLocal을 ScopedValue로 옮긴다는 말이 자꾸 떠올랐을 것이다. 그 자리, 그리고 fan-out한 자식 task 전체를 *하나의 단위*로 묶어 *cancellation까지 전파*하는 자리. 다음 장에서는 그 도구 — `StructuredTaskScope`과 `ScopedValue` — 를 본격적으로 살펴보자. concurrent 코드에도 *구조*가 있다는 Dijkstra의 1968년 약속을 자바가 마침내 받아낸 자리다.
