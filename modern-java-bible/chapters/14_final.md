# 14장. Virtual Threads — thread-per-request의 부활

Tomcat 200 thread 풀로 한 달을 버틴 끝에 p99가 800ms였다고 해보자. 새벽 트래픽이 몰리는 두 시간 동안 응답 시간 그래프는 진동했고, 그 진동을 가라앉히려고 풀 사이즈를 300으로 늘렸더니 메모리가 답답한 소리를 내며 컨테이너 limit에 부딪혔다. 이상하다. CPU 사용률은 30%를 넘지 않는다. 컨트롤러가 하는 일이라곤 외부 결제 API 하나, 회원 조회 API 하나, 쿠폰 검증 API 하나를 합치는 것뿐이다. 세 호출이 각 100ms씩 걸린다 치자. 한 요청이 300ms를 잡고 있는 동안 thread는 거의 100% idle이다. 그저 대기할 뿐이다. 그런데도 풀이 모자란다. 답답하지 않은가.

이 답답함을 해결하겠다고 등장했던 것이 reactive였다. WebFlux를 도입한 옆 팀의 코드를 본 적이 있을 것이다. `Mono`와 `Flux`가 메서드 시그니처마다 따라다니고, `subscribe`·`flatMap`·`zipWith`로 흐름을 다시 짜야 하고, `StackOverflowError`가 났을 때 stack trace는 어디서부터 봐야 할지 알 수 없는 추상의 사다리를 그리고 있다. 그런 코드를 짜고도 같은 팀의 절반은 *operator semantics*를 정확히 설명하지 못한다. 그렇다면, 묻고 싶어진다. 왜 이제야 thread-per-request가 가능해졌을까. 왜 자바는 30년 동안 OS thread에 묶인 채 살아왔을까. 그리고 지금 우리가 켤 수 있다는 그 *virtual thread*는, 정말 reactive 없이도 충분히 빠르다는 약속을 지킬 수 있을까.

## 회수: 13장의 `Result<T,E>`를 다시 꺼내자

본격적으로 들어가기 전에, 13장에서 만들었던 sealed `Result<T,E>` 타입을 다시 꺼내 보자. virtual thread를 다루는 첫 코드에 이 타입이 등장하는 데는 이유가 있다. virtual thread가 하는 일은 본질적으로 *blocking 호출의 결과*를 받아 합치는 일이다. 그 결과는 성공일 수도, 실패일 수도 있다. 우리는 13장에서 이미 그 두 갈래를 한 자리에 묶는 방법을 익혔다.

```java
sealed interface Result<T, E> permits Ok, Err {
    record Ok<T, E>(T value) implements Result<T, E> {}
    record Err<T, E>(E error) implements Result<T, E> {}
}
```

가령 결제 API와 회원 조회와 쿠폰 검증을 동시에 호출하고, 세 결과를 모두 모은 뒤 하나라도 실패하면 사용자에게 명확한 도메인 에러를 돌려주고 싶다고 해보자. 이전이라면 `CompletableFuture<Result<...>>`를 줄줄이 엮어 `allOf`로 모으고 `get()`에서 예외를 잡았을 것이다. virtual thread를 쓰면 그 코드는 *그냥 synchronous하게* 적힌다.

```java
try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<Result<Payment, BillingError>> pay   = scope.submit(() -> billing.charge(orderId));
    Future<Result<Member, MemberError>>   mem   = scope.submit(() -> members.findById(userId));
    Future<Result<Coupon, CouponError>>   coup  = scope.submit(() -> coupons.validate(couponCode));

    return switch (pay.get()) {
        case Result.Ok<Payment, BillingError>(var p) -> switch (mem.get()) {
            case Result.Ok<Member, MemberError>(var m) -> switch (coup.get()) {
                case Result.Ok<Coupon, CouponError>(var c) -> CheckoutResponse.success(p, m, c);
                case Result.Err<Coupon, CouponError>(var e) -> CheckoutResponse.failed(e);
            };
            case Result.Err<Member, MemberError>(var e) -> CheckoutResponse.failed(e);
        };
        case Result.Err<Payment, BillingError>(var e) -> CheckoutResponse.failed(e);
    };
}
```

세 호출이 *동시에* 일어나고, 세 결과가 *순서 없이* 도착하지만, 코드 자체는 위에서 아래로 흐른다. 디버거를 걸면 평범한 stack trace가 한 줄로 보인다. 세 개의 외부 호출을 합치는 컨트롤러 — 이 장이 끝날 때까지 이 도메인을 들고 갈 것이다. 마음 한쪽에 결제·회원·쿠폰 세 API를 두고, virtual thread가 그것을 어떻게 *합리적인* 코드로 만들어주는지 추적해 가자.

(중첩 switch가 깊다고 느낀다면 — 그 감각이 옳다. 16장에서 `StructuredTaskScope`로 같은 코드를 한 단계 더 다듬을 것이다. 지금은 *virtual thread 자체*에만 집중하자.)

## 왜 이제야 가능해졌을까

자바가 등장한 1995년의 thread는 `green thread`였다. JVM이 user-level에서 스케줄링하는 가벼운 thread다. Solaris의 native thread 모델이 자리 잡으면서 1998년 무렵 Java 1.2는 green thread를 폐기하고 *OS thread = `java.lang.Thread`*라는 등식으로 옮겨갔다. 그 뒤로 27년이다. `Runnable`을 짜고 `new Thread(...).start()`를 호출하면 커널이 새 thread를 만들고, 스택을 1MB 예약하고, 스케줄러 큐에 올렸다. 이 등식이 자바의 모든 동시성 모델을 결정했다 — `ExecutorService`도, `ThreadPoolExecutor`도, Tomcat의 request handler도, 결국 같은 무거운 자원을 *재사용*하는 방식이었다.

OS thread는 비싸다. Linux x64에서 thread 하나당 약 1MB의 스택을 예약해 둔다. 1000개를 만들면 그것만으로 1GB다. 컨텍스트 스위치 비용도 무시할 수 없어서, 수만 개를 띄우면 스케줄러가 먼저 휘청거린다. 그래서 자바 개발자는 30년간 *thread pool*이라는 한 가지 답을 써왔다. 200개, 400개, 많아야 1000개. 그 풀 안에서 요청들이 줄을 서서 thread를 빌려 쓰고 돌려준다.

문제는 풀이 모자랄 때다. 한 요청이 외부 API 응답을 기다리는 동안 thread는 차지된 채 *아무 일도 하지 않는다*. CPU는 한가한데 풀은 비어 있는 모순이 일어난다. p99가 800ms로 솟구치는 새벽의 답답함이 바로 이 모순이다. CPU를 더 사면 해결되는 문제가 아니다. *thread 자체가 비싸기 때문*에 일어나는 문제다.

reactive는 이 모순을 다른 방향에서 풀려고 했다. "blocking I/O를 쓰지 말자. 모든 I/O를 non-blocking event로 모델링하고, callback이나 stream으로 결과를 받자." 똑똑한 답이다. 그러나 모든 외부 라이브러리가 non-blocking이 아니다. JDBC는 30년째 blocking이다. 한 자리에서 reactive를 쓰려면 *모든 자리*에서 reactive를 써야 한다. 함수 시그니처가 전염되고, 에러 핸들링이 새로운 어휘로 다시 짜인다. *기존 자바 코드가 그대로 돌지 않는다*는 결정적 비용이 따라붙는다.

Project Loom의 동기는 정확히 그 자리에서 출발했다. Ron Pressler를 비롯한 OpenJDK 팀의 답은 단순했다. "blocking I/O를 그대로 쓰자. 단, thread 자체를 싸게 만들자." OS thread를 그대로 둔 채, JVM이 관리하는 *가벼운 thread*를 새로 도입한다. blocking 호출이 들어오면 그 thread는 OS thread에서 *unmount*되고 다른 thread가 OS thread를 빌려 쓴다. 풀의 크기를 늘리는 대신, thread의 단가를 낮춘다.

## Virtual Thread란 무엇인가

JEP 444의 정의를 정직하게 인용하는 편이 낫다.

> A virtual thread is an instance of `java.lang.Thread` that is not tied to a particular OS thread. A platform thread, by contrast, is a `Thread` implemented in the traditional way, as a thin wrapper around an OS thread. — JEP 444

핵심은 *`java.lang.Thread`의 인스턴스*라는 점이다. 새로운 타입이 아니다. 같은 API다. `Thread.currentThread()`, `Thread.sleep()`, `InterruptedException`, `ThreadLocal` — 모두 그대로 동작한다. 30년 묵은 자바 코드가 *그대로* 돌아가야 한다는 호환성 제약을 OpenJDK 팀이 끝까지 지켜낸 결과다. 새 키워드도 없고, 새 동시성 어휘도 없다. 그저 thread의 *종류*가 둘이 됐을 뿐이다.

Brian Goetz는 이 명명에 대해 이런 비유를 했다. *virtual thread는 thread의 virtual memory*다. 물리 메모리보다 큰 환상의 메모리를 운영체제가 페이지로 매핑해주듯, 물리 thread보다 많은 환상의 thread를 JVM이 carrier thread로 매핑해준다. virtual memory를 처음 도입했을 때 개발자가 직접 페이지 in/out을 신경 쓸 필요가 없어진 것처럼, virtual thread를 도입한 지금 개발자가 thread pool 크기를 신경 쓸 필요가 없어진다. *thread는 자원이 아니라 표현 단위*가 된다. 30년 만에 자바가 그 자리에 도달했다.

API는 세 갈래다.

```java
// 1. 일회성
Thread.startVirtualThread(() -> System.out.println("hi"));

// 2. 빌더
Thread t = Thread.ofVirtual()
    .name("checkout-fanout-", 0)
    .uncaughtExceptionHandler((th, ex) -> log.error("uncaught", ex))
    .start(() -> doWork());

// 3. ExecutorService — 가장 흔히 쓰는 길
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> doWork());
}
```

`newVirtualThreadPerTaskExecutor()`라는 이름을 곱씹어 보자. *per task*다. task마다 새 virtual thread를 만든다. 이전 같으면 "thread를 한 번 쓰고 버린다고? 미친 짓이다"라고 답했을 일이지만, virtual thread에서는 그게 *합리적*이다. 만드는 비용이 거의 0에 가깝기 때문이다. 100만 개를 만들어도 OS는 모른다. JVM 안에서만 사는 객체이기 때문이다.

세 가지는 알아둘 만하다.

- **모든 virtual thread는 daemon이다.** `setDaemon(false)`를 호출하면 `IllegalArgumentException`이 난다. JVM 종료를 막을 권한이 없다는 뜻이다.
- **priority가 무시된다.** `setPriority(MAX_PRIORITY)`를 적어도 효과 없다. 스케줄링은 carrier pool이 알아서 한다.
- **thread group은 하나다.** 모든 virtual thread는 단일 공유 그룹 `"VirtualThreads"`에 속한다. thread group 기반의 옛 코드는 더 이상 의미가 없어진다.

이 세 가지는 thread가 *자원에서 표현 단위로* 옮겨갔다는 사실의 작은 증거다. daemon이냐 아니냐를 신경 쓸 필요가 없다. priority로 조정할 만큼 비싸지 않다. group으로 묶을 만큼 길게 살지 않는다.

## M:N 스케줄링: continuation으로 들여다보자

원리를 정확히 이해하고 싶다면 *continuation*이라는 추상부터 살펴보자. Project Loom의 진짜 코어는 virtual thread가 아니다. continuation이다. virtual thread는 continuation에 OS thread 비유를 입힌 *얼굴*일 뿐이다.

continuation은 "지금까지의 실행 상태를 통째로 들고 다닐 수 있는 일급 객체"다. 함수 호출의 한가운데서 일시 정지했다가, 나중에 *같은 자리에서* 재개할 수 있다. 자바의 내부 API로 `jdk.internal.vm.Continuation`이 존재하고, scope는 `jdk.internal.vm.ContinuationScope`로 묶인다. 일반 애플리케이션 개발자가 직접 만질 일은 없지만, virtual thread의 동작을 이해하려면 한 번은 들여다보는 편이 낫다.

virtual thread가 동작하는 흐름을 단순화하면 이렇다.

1. JVM은 `ForkJoinPool` 기반의 *carrier thread pool*을 유지한다. 기본 크기는 `Runtime.getRuntime().availableProcessors()`. CPU 코어 수만큼이다.
2. virtual thread가 `start()`되면 carrier 중 하나에 *mount*된다. 그 순간부터 virtual thread는 평범한 OS thread처럼 코드를 실행한다.
3. blocking 호출(예: `Socket.read()`, `Thread.sleep()`, `BlockingQueue.take()`)을 만나면 JVM은 continuation으로 현재 실행 상태를 캡처하고 virtual thread를 carrier에서 *unmount*한다. carrier는 자유로워져서 다른 virtual thread를 mount한다.
4. blocking이 풀리면 (소켓에 데이터가 도착하면) virtual thread는 *언젠가* 다시 carrier에 mount되어 같은 자리에서 재개한다.

핵심은 mount/unmount가 *코드 한 줄의 변경 없이* 일어난다는 점이다. JDK 내부의 `Socket`·`HttpClient`·`Files`·`BlockingQueue` 등 거의 모든 blocking 지점이 Loom-aware로 재작성됐다. `Socket.read()`를 호출하는 코드는 똑같이 보이지만, 그 안에서 JVM은 OS의 `epoll`을 쓰는 비동기 I/O로 변환해 처리한다. virtual thread가 unmount되어 있는 동안 carrier는 다른 일을 한다.

이게 곧 *M:N 스케줄링*이다. M개의 virtual thread가 N개의 carrier thread에 multiplex된다. M은 100만 수준까지 갈 수 있고, N은 CPU 코어 수다. Go의 goroutine과 똑같은 구조다. 다만 자바는 새 키워드(`go`) 없이, 기존 `Thread` API를 그대로 둔 채로 같은 결과를 얻는다.

조금 더 들여다보자. JVM은 carrier thread pool을 `ForkJoinPool`로 구현한다. 정확히는 `ForkJoinPool.commonPool()`이 아닌, virtual thread 전용 *별도* pool이다. `-Djdk.virtualThreadScheduler.parallelism`으로 크기를 조정할 수 있지만, 거의 모든 경우 기본값(코어 수)을 그대로 두는 편이 낫다. ForkJoinPool을 고른 이유는 work-stealing이다. carrier A가 한가해지면 carrier B의 큐에서 *대기 중인 virtual thread*를 가져와 mount한다. 그 결과 carrier들이 *균등하게* 일을 나눠 갖는다. 동시 요청이 들쭉날쭉해도 throughput이 안정적이다.

mount의 비용도 짚어두자. virtual thread를 새로 만드는 자체의 비용은 *수십 마이크로초*다. OS thread 생성이 *수 밀리초*인 것에 비하면 1000배 가까이 싸다. 100만 개를 만드는 일이 *합리적*이라는 말의 근거가 여기 있다. unmount/mount의 비용 — 한 carrier에서 다른 carrier로 옮겨가는 비용 — 도 마찬가지로 가볍다. continuation의 stack을 heap에 *통째로 옮기는 일*이 본질이지만, JVM이 그 일을 최적화해서 *대체로 자유롭게* 일어나도록 만들었다.

이 가벼움이 곧 *thread-per-request*의 부활을 가능하게 한 자리다. thread 자체가 비싸지 않으면 풀의 필요가 사라진다. 풀이 사라지면 큐가 사라지고, 큐가 사라지면 큐 대기 시간이 사라진다. p99의 답답함이 사라진다. 새벽의 800ms가 사라진다. *비싼 자원의 재사용*이라는 30년의 자바 모델이, 한 줄 — `newVirtualThreadPerTaskExecutor()` — 으로 무너진다.

## virtual thread vs goroutine vs async/await vs green thread

한국 개발자가 자주 묻는 질문이다. virtual thread는 결국 *옛 green thread*와 무엇이 다른가. goroutine을 흉내 낸 것 아닌가. C#의 `async/await`와는 어떻게 다른가. 표 하나로 정리해 두자.

| | virtual thread | goroutine | async/await | green thread (옛) |
|---|---|---|---|---|
| 통신 모델 | 공유 메모리 + lock·CAS | 채널 (CSP) | task/future + await | 공유 메모리 |
| 호환성 | 기존 `Thread` API 그대로 | 새 키워드 `go` | 시그니처 전염 (`async`) | 기존 API |
| blocking I/O | 자동 unmount (Loom-aware) | 자동 yield | 명시적 `await` | 협력적 yield |
| 스케줄링 | M:N work-stealing carrier pool | M:N work-stealing | 단일 event loop 다수 | user-level, OS 미연동 |
| 도입 시점 | 2023 (JDK 21) | 2009 (Go 1.0) | 2012 (C# 5) / 2017 (Python 3.6) | ~1998 (Java 1.1) |
| 사라진 이유 | — | — | — | OS thread 모델 채택 |

핵심을 짚자. virtual thread가 *함수 색깔(function color)* 문제에서 자유로운 점이 가장 큰 미덕이다. C#의 `async`는 `async` 함수에서만 `await`할 수 있고, `async` 함수를 호출한 함수는 자기도 `async`가 되어야 한다. 색깔이 전염된다. 그 결과 라이브러리는 `sync` 버전과 `async` 버전을 둘 다 제공해야 한다. virtual thread에는 색깔이 없다. `read()`는 `read()`다. blocking이면 unmount되고, non-blocking이면 그대로 진행한다. 함수 시그니처가 변하지 않는다.

green thread와의 차이도 정직하게 짚자. 1990년대 자바의 green thread는 *user-level*이었다. JVM 내부의 단일 OS thread 위에서 협력적으로 yield하는 모델이었다. 멀티 코어를 못 썼다. virtual thread는 다르다. carrier pool이 멀티 코어를 활용하고, JVM과 OS가 *함께* 비동기 I/O를 조율한다. 옛 green thread의 약점이었던 "한 thread가 OS-blocking syscall을 호출하면 모두가 멈춘다"는 문제가 *Loom-aware* 라이브러리 덕에 해소됐다. green thread의 이름은 같지만, 정체는 다른 도구다.

## 성능: 약속은 정직한가

OpenJDK가 약속한 것은 *throughput의 비약*이지 *latency의 비약*이 아니다. 이 차이를 정확히 짚어두자. virtual thread를 켜면 같은 요청 하나가 갑자기 빨라지지는 않는다. JDBC 호출 100ms는 그대로 100ms다. 빨라지는 것은 *동시에 처리할 수 있는 요청의 수*다. 800ms p99의 원인이 thread 풀이 모자라 큐에 쌓이는 것이었다면, 풀의 제약이 사라지면서 큐가 줄고 p99가 200ms로 떨어진다. 하지만 처음부터 큐가 짧았다면 p99는 거의 변하지 않는다.

이 약속이 production에서 어떻게 검증됐는지 보자. SoftwareMill의 벤치마크 *Limits of Loom's Performance*는 두 가지를 보여줬다. 첫째, virtual thread의 throughput은 Go의 goroutine과 비슷한 수준에 도달한다. 둘째, 결정적 차이는 자바 쪽에 있다 — *기존 자바 코드가 그대로 돌아간다*. Reactive Streams나 새 언어 키워드 없이, 11년 묵은 Spring MVC 코드가 그대로 throughput을 받는다. 이게 자바가 Loom에 11년을 투자한 가장 큰 회수다.

production 사례도 모이고 있다. Cashfree Payments는 *7 Key Lessons*라는 글에서 자기 인프라에 virtual thread를 도입한 경험을 정리했다. 결제 처리 서버 — 외부 은행 API와 카드사 게이트웨이를 합치는 fan-out 구조다. 도입 후 동일 부하에서 thread 풀이 사라지고, p99 latency가 의미 있게 떨어졌으며, container 메모리 사용량은 *늘었다*. 늘었다고? 그렇다, stack이 heap에 살기 때문이다. virtual thread는 OS 스택 1MB를 예약하지 않는 대신, 필요할 때 heap에서 작게 시작해 grow한다. heap 사용량이 ~30% 증가하는 것은 흔한 관찰이다. 컨테이너 limit을 그만큼 상향해 두는 편이 안전하다.

한국에서도 사례가 쌓이고 있다. 우아한형제들은 *"Java의 미래, Virtual Thread"* 기술 세미나와 후속 블로그에서 Loom 도입의 의미를 정리했다. 카카오는 제4회 Kakao Tech Meet *"JDK 21의 Virtual Thread"*에서 같은 주제를 다뤘다. 카카오페이는 *"Virtual Thread에 봄(Spring)은 왔는가"*에서 platform thread → virtual thread 전환을 실제로 측정한 결과를 공개했다. 자세한 수치는 15장에서 *함정과 한계*와 함께 짚을 테니, 지금은 *production에 들어가 있다*는 사실만 기억해 두자.

(SoftwareMill 벤치마크에서 한 가지 흥미로운 관찰이 있었다 — virtual thread는 *극단적인 throughput 한계*에서는 Go의 goroutine보다 약간 뒤처졌다. 그 차이는 work-stealing 스케줄러의 세부 구현, FFI 호출의 영향, 그리고 자바 객체의 메모리 footprint에서 온다고 분석됐다. 그러나 *production이 다루는 현실적인 throughput 영역*에서는 두 도구 모두 충분한 head room을 보여줬다. 실무자에게 의미 있는 결론은 — virtual thread를 도입하면서 *Go로 옮겨야 하는 이유*는 거의 사라졌다는 것이다. 자바의 ecosystem과 도구가 그대로 따라오기 때문이다.)

## 30년 자바 코드가 그대로 돈다는 약속

이 절을 한 번 더 정직하게 짚어두는 편이 낫다. *기존 자바 코드가 그대로 돈다*는 약속은 무엇을 뜻하는가. 무엇이 그대로이고 무엇이 새로워졌는가.

**그대로 돌아가는 것**

- `Thread.currentThread()`, `Thread.sleep()`, `Thread.interrupt()` 등 `Thread` 클래스의 거의 모든 API.
- `synchronized` 블록 — *진입과 종료*의 의미론은 같다. 단, Java 21~23에서는 unmount가 막힌다(15장에서 짚는다).
- `ThreadLocal` — *동작은* 같다. 다만 thread 수가 폭발하면 메모리 사용 양상이 달라진다(역시 15장).
- `ReentrantLock`, `Semaphore`, `CountDownLatch`, `BlockingQueue` 등 `java.util.concurrent`의 모든 도구. 모두 Loom-aware로 재작성됐다.
- `Socket`, `ServerSocket`, `HttpClient` 등 표준 I/O — JDK 내부에서 mount/unmount를 자동 처리한다.

**달라진 것**

- thread 생성 비용: 수 밀리초 → 수십 마이크로초.
- thread당 stack: OS 예약 1MB → heap 동적 grow.
- thread 수 한계: ~수천 → ~수백만.
- `setDaemon`, `setPriority`, thread group: 의미 없는 호출.
- `ThreadFactory` 기반의 *thread 재사용 풀*: virtual thread에는 의미 없다 — *재사용하지 않으니까*.

마지막 항목이 중요하다. `newFixedThreadPool(200)`을 `newVirtualThreadPerTaskExecutor()`로 *그대로* 바꾸면 안 된다. 두 도구는 *다른 모델*이다. 옛 코드가 풀의 크기에 *의존*하고 있었다면 — 가령 외부 API의 rate limit을 thread 수로 제한하고 있었다면 — virtual thread로 옮기는 순간 그 제한이 사라진다. rate limit은 *명시적*으로 `Semaphore`로 다시 두는 편이 낫다. 풀의 크기로 *암묵적*으로 다스리던 제약을 *드러내자*. 이 *드러냄*이 virtual thread 도입의 또 다른 부수 효과다.

## Java 8 ExecutorService vs Java 21 VirtualThreadPerTaskExecutor

코드 한 쌍으로 11년의 거리를 좁혀 보자. 같은 일을 Java 8 시대에는 어떻게 적었고, Java 21에서는 어떻게 적는가.

**Java 8 — bounded thread pool**

```java
private static final ExecutorService POOL =
    Executors.newFixedThreadPool(200,
        new ThreadFactoryBuilder().setNameFormat("checkout-%d").build());

public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    Future<Payment> pay  = POOL.submit(() -> billing.charge(orderId));
    Future<Member>  mem  = POOL.submit(() -> members.findById(userId));
    Future<Coupon>  cp   = POOL.submit(() -> coupons.validate(coupon));
    try {
        return new CheckoutResponse(pay.get(), mem.get(), cp.get());
    } catch (Exception e) {
        // pay·mem 결과 폐기, 보상 처리는 ... 어디서 ... ?
        throw new ServiceException(e);
    }
}
```

`POOL`은 *공유 자원*이다. 200개 thread가 컨트롤러 전체에서 돌고 있다. 어떤 요청이 외부 API의 응답을 30초간 기다리면, 그 30초 동안 thread 하나가 점유된다. 200개가 모두 그렇게 되면 다음 요청은 큐에 쌓인다. 800ms의 p99는 이 큐에서 태어난다. 그리고 한 자식이 실패했을 때 다른 자식을 깔끔하게 취소할 방법이 보이지 않는다. `pay.cancel(true)`를 호출해도 이미 보낸 결제 요청은 중단되지 않을 가능성이 크다. 보상 트랜잭션을 어디 적어야 할지조차 코드에서 안 보인다.

**Java 21 — virtual thread per task**

```java
public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    try (var scope = Executors.newVirtualThreadPerTaskExecutor()) {
        Future<Payment> pay  = scope.submit(() -> billing.charge(orderId));
        Future<Member>  mem  = scope.submit(() -> members.findById(userId));
        Future<Coupon>  cp   = scope.submit(() -> coupons.validate(coupon));
        return new CheckoutResponse(pay.get(), mem.get(), cp.get());
    } // scope 종료 시 자식 task 정리
}
```

차이를 살피자. 첫째, `POOL`이 사라졌다. 매 요청마다 새 executor를 만든다. 둘째, 그 executor는 *thread를 빌려주지 않는다*. 자식 task마다 새 virtual thread를 만든다. 셋째, `try-with-resources`로 묶었기 때문에 컨트롤러가 반환되는 순간 executor도 닫히고 자식 task의 수명이 컨트롤러 scope에 묶인다.

이 코드는 *문법적으로* 거의 같다. Java 8 코드를 Java 21로 옮기면서 새로 배운 것은 `newVirtualThreadPerTaskExecutor()` 한 줄뿐이다. 그러나 *의미*는 달라졌다. thread는 자원이 아니고, 풀은 없으며, 외부 호출이 100ms든 30초든 다른 요청에 영향을 주지 않는다. 이게 thread-per-request가 *돌아왔다*는 말의 진짜 내용이다.

(취소·실패 전파의 정직한 답은 16장의 `StructuredTaskScope`에 있다. virtual thread는 그 자체로는 *수명 관리*까지 풀어주지 않는다. 그러나 일단 여기까지가 14장의 무게다.)

## Spring과의 만남은 21장에서

Spring Boot 3.2부터는 `application.yml`에 한 줄을 적으면 Tomcat의 request handler가 virtual thread per request로 바뀐다.

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

기억해 두자 — 이 한 줄의 의미는 21장에서 본격 다룬다. 한 결제 마이크로서비스에 records·sealed·virtual thread·AOT를 한 번에 끼워 넣는 자리에서, 이 한 줄이 어떤 도구들과 만나 *후련함*이 되는지 같이 본다. 지금은 *호명*만 해두자.

## reactive와의 대화: 무엇이 남고 무엇이 사라질까

§6.3의 두 관점을 한 번 정직하게 짚어두자. *virtual thread가 모든 reactive를 대체할까*. 한국 커뮤니티에서 가장 자주 마주치는 질문이다. 양면 모두 인정하는 편이 낫다.

**대체될 자리**

`Mono`·`Flux`로 짠 단순 fan-out 컨트롤러는 virtual thread로 *다시 평범한 동기 코드*가 된다. operator chain의 학습 비용, 디버깅의 *난감함*, stack trace에서 진짜 발생 지점을 찾지 못해 헤매던 시간 — 그 부담이 줄어든다. WebFlux를 도입한 이유의 *반*은 "thread 풀 한계를 우회하려고"였는데, 그 자리는 virtual thread가 더 단순한 답을 준다.

**남는 자리**

reactive가 *진짜로 제공*하던 것이 둘 있다. 첫째, *backpressure*. consumer가 늦으면 producer를 *멈춰 세우는* 신호 전달이다. Kafka 컨슈머·SSE·WebSocket 같은 streaming 자리에서는 backpressure가 본질이다. virtual thread가 backpressure를 *자동으로* 주지는 않는다. 둘째, *hot/cold stream과 명시적 cancel/replay*. Reactor의 `share()`·`replay()`·`retryWhen` 같은 operator는 virtual thread의 어휘에 없다. 진정한 *데이터 흐름*이 주제인 시스템 — 실시간 통계, event sourcing, 메시지 스트림 — 에서는 reactive가 여전히 더 자연스러운 도구다.

SoftwareMill의 *Limits of Loom's Performance*도 이 두 관점을 모두 인정했다. *대체*가 아니라 *역할의 재배치*다. 한국 사례를 한 줄 더 — 카카오페이가 platform → virtual로 옮긴 자리는 *fan-out 컨트롤러*였다. *결제 streaming*이나 *Kafka 컨슈머*는 다른 도구로 따로 짜고 있다. 우리도 그 방향으로 결정하는 편이 낫다.

## 진화의 자리: JEP 425 → 436 → 444

마지막으로 진화의 자리를 정리하자. virtual thread는 갑자기 생긴 도구가 아니다. Project Loom은 2017년에 시작됐고, OpenJDK에서 6년의 incubation을 거쳤다.

- **JEP 425 (Java 19, 2022 preview)** — virtual thread 첫 공개. API의 모양이 잡혔지만 아직 실험.
- **JEP 436 (Java 20, 2023 second preview)** — preview 라운드 2. 거의 변화 없음. 산업 피드백 수렴.
- **JEP 444 (Java 21, 2023 standard)** — LTS에 표준으로 안착. 이 자리가 우리가 본격적으로 쓸 수 있는 출발선이다.

이 흐름은 자바의 *preview 문화*를 잘 보여준다. records가 그랬듯, virtual thread도 두 라운드의 preview를 거쳐 다듬어졌다. 표준화된 21에서는 API가 바뀌지 않을 것이라는 *호환성 약속*이 따라붙는다. 11년의 자바를 견뎌낸 도구는 그렇게 만들어진다.

## 마무리

virtual thread는 자바에 *thread-per-request*를 돌려준 도구다. 30년간 OS thread에 묶여 thread pool로 버텨왔던 모델이, 마침내 *task마다 thread를 만든다*는 가장 자연스러운 표현으로 돌아왔다. continuation이라는 추상이 mount/unmount로 OS thread를 자유롭게 만들고, ForkJoinPool 기반의 carrier가 그 위에서 work-stealing을 한다. reactive 없이도 충분히 빠르다는 약속은 — *I/O bound*라는 단서 안에서 — 정직하게 지켜진다.

그러나 약속은 단서가 있어야 정직하다. virtual thread를 켜기만 하면 모든 게 빨라진다는 말은 사실이 아니다. `synchronized` 블록 안에서 외부 API를 호출하면 pinning이 일어나고, ThreadLocal에 caching을 들고 있던 코드는 수백만 thread 곱하기 수백만 캐시로 메모리를 *폭발*시킨다. CPU-bound 작업에 virtual thread를 쓰면 오히려 느려진다. 켰는데 *deadlock*이 난 새벽도 production에서는 드물지 않다.

다음 장에서는 그 *끔찍한 새벽*을 함께 들여다보자. VT를 켰는데 더 느려지는 자리, pinning을 JFR로 추적하는 절차, ThreadLocal의 폭발을 막는 안전한 패턴 — 이 장에서 약속한 것의 *반대편*에 정직하게 마주서 보자.
