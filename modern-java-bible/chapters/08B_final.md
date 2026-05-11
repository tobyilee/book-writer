# 8B장. CompletableFuture와 Reactive Streams Flow — 비동기 조합의 두 갈래

외부 API 세 개를 합쳐야 하는 컨트롤러를 받았다고 해보자.

요구사항은 단순해 보였다. 결제 게이트웨이 A, 적립 포인트 시스템 B, 배송 추적 시스템 C에 각각 주문 정보를 보내고, 세 응답을 한 데 묶어 클라이언트에 돌려준다. 각각 평균 200ms씩 걸리니, 순차로 호출하면 p50이 600ms를 넘는다. 병렬로 돌리면 200ms대에 떨어질 텐데, 그 *병렬*을 어떻게 짤 것인가가 문제다. 일주일 전 같은 작업을 했던 동료의 코드를 열어보면, 이런 게 있다.

```java
ExecutorService es = Executors.newFixedThreadPool(3);
Future<PaymentResult> f1 = es.submit(() -> paymentClient.charge(order));
Future<PointResult> f2 = es.submit(() -> pointClient.accrue(order));
Future<ShippingResult> f3 = es.submit(() -> shipClient.track(order));
PaymentResult r1 = f1.get(2, TimeUnit.SECONDS);
PointResult r2 = f2.get(2, TimeUnit.SECONDS);
ShippingResult r3 = f3.get(2, TimeUnit.SECONDS);
return new OrderResponse(r1, r2, r3);
```

병렬은 됐다. 그러나 *찜찜하다.* 첫째, `Future.get()`이 줄줄이 blocking이다. 둘째, 셋 중 하나만 실패해도 나머지를 *우아하게* 취소하는 방법이 없다. 셋째, 결제 결과가 도착하자마자 *그것만 가지고* 적립 비율을 계산하는 식의 *조합*은 어림도 없다. 넷째, 타임아웃·재시도·fallback을 합쳐 짜다 보면 `try-catch`와 `Future`가 뒤엉켜 가독성이 무너진다.

`Future`가 잘못 설계된 건 아니다. Java 5에서 비동기의 *최소한*을 표현하기 위해 만든 도구일 뿐이다. 그러나 *조합*까지 가려면 다른 도구가 필요했다. Java 8의 `CompletableFuture`가 그 다음 단계였고, Java 9의 `Flow`가 또 한 번의 일반화였다. 이 장에서는 콜백 지옥에서 우리가 어떻게 빠져나왔고, *그 다음은 무엇이었는지*를 따라가 본다. 그리고 솔직히 인정하자 — Reactive Streams는 *왜 그렇게 어려웠을까?*

## Future의 한계와 CompletableFuture의 도착

`Future`의 결정적 한계는 두 가지다. **콜백을 등록할 수 없다** — 결과가 준비되면 무엇을 할지를 *미리 적어둘* 방법이 없다. **조합할 수 없다** — 여러 Future를 묶거나, 한 Future의 결과를 다음 Future의 입력으로 보낼 *언어 도구*가 없다. 결국 `get()`으로 막아서서 받는 수밖에 없는데, 그 순간 비동기의 가치가 절반은 사라진다.

Java 8에서 도입된 `CompletableFuture<T>`(이하 CF)는 이 두 한계를 정면으로 깬다. CF는 `Future`이면서 동시에 *`CompletionStage`* 다. 즉, 결과가 준비되면 *다음 단계*를 자동으로 트리거하는 비동기 파이프라인의 한 마디다. 메서드가 50개를 넘는다. 처음 보면 압도된다. 그러나 분류하면 의외로 단순하다 — 세 축이다. **무엇을** 할 것인가(consume·transform·combine), **어디서** 실행할 것인가(같은 스레드 vs 다른 스레드), **예외**가 났을 때 어떻게 할 것인가.

도입 코드를 위 시나리오로 다시 써보자.

```java
CompletableFuture<PaymentResult>  cf1 = CompletableFuture.supplyAsync(() -> paymentClient.charge(order), httpExecutor);
CompletableFuture<PointResult>    cf2 = CompletableFuture.supplyAsync(() -> pointClient.accrue(order),   httpExecutor);
CompletableFuture<ShippingResult> cf3 = CompletableFuture.supplyAsync(() -> shipClient.track(order),     httpExecutor);

CompletableFuture<OrderResponse> result =
    CompletableFuture.allOf(cf1, cf2, cf3)
        .thenApply(__ -> new OrderResponse(cf1.join(), cf2.join(), cf3.join()));
```

`allOf(...)`가 세 작업을 묶어준다. `thenApply(...)`로 결과 변환을 *콜백*으로 등록한다. `get`도 `try-catch`도 없다. *훨씬 낫다.*

## thenApply · thenCompose · thenCombine — 헷갈리는 세 친척

CF의 메서드 중 가장 자주 손에 잡는 세 가지를 정확히 구분해보자. 셋은 비슷해 보이지만 *완전히 다른 일*을 한다.

`thenApply(Function<T, U>)` — 결과 `T`를 받아 `U`로 변환한다. 동기 함수다. 입력 `Function`은 *값*을 반환한다.

`thenCompose(Function<T, CompletionStage<U>>)` — 결과 `T`로 *또 다른 CF*를 만들어 그것이 끝나기를 기다린다. 함수가 *CF*를 반환한다. *flat-map*에 해당하는 연산이다 — Optional·Stream의 `flatMap`과 *철학이 같다.* 비동기 호출의 *체인*을 짤 때 쓴다.

```java
fetchUserId(req).thenCompose(this::fetchUser).thenCompose(this::fetchUserOrders);
// fetchUser, fetchUserOrders가 각각 CompletableFuture를 반환
```

`thenCombine(CompletionStage<U>, BiFunction<T, U, R>)` — *두 CF의 결과*가 모두 도착하면 결합 함수를 실행한다. zip에 해당한다.

이 셋을 구분하지 못하면 `thenApply` 안에서 또 비동기 호출을 호출하다 *동기 블로킹*이 발생하거나, `thenCompose`를 써야 할 자리에 `thenApply(... -> someAsync())`를 두어 *CF가 한 겹 더 감싸진* 채로 흘러가 버린다. 후자는 `CompletableFuture<CompletableFuture<Result>>`라는 *난감한* 타입을 만든다. *기억해두자* — 단계 함수가 *값*을 반환하면 `thenApply`, *CF*를 반환하면 `thenCompose`다.

`thenAccept`(consume, 반환 없음), `thenRun`(인자도 없음, 단순 실행)도 같은 가족이다. 모두 `Async` 접미사 변형이 있다 — `thenApplyAsync`처럼. 접미사가 *있으면* 다음 단계를 별도 executor에서, *없으면* 직전 단계를 실행한 스레드에서 그대로 이어 실행한다.

## handle · exceptionally · whenComplete — 예외 전파의 세 모양

비동기 파이프라인에서 예외는 *다음 단계로 전파*된다. 마치 Stream의 short-circuit처럼 — 예외가 한 번 발생하면 그 뒤의 `thenApply`·`thenCompose`는 *모두 건너뛰고* 끝까지 흘러간다. 그 흐름의 어디서 예외를 *받아 처리*할지가 세 메서드의 차이다.

`exceptionally(Function<Throwable, T>)` — 예외가 났을 때만 호출돼 *대체 값*을 만든다. 정상 흐름은 통과시킨다. fallback에 가장 적합하다.

```java
fetchFromPrimary().exceptionally(ex -> fetchFromCache(ex)); // ex로 fallback
```

`handle(BiFunction<T, Throwable, R>)` — 정상이든 예외든 *둘 다*를 보고 결과를 만든다. 둘 중 하나는 null이다. 흐름을 *항상* 정상으로 되돌린다.

`whenComplete(BiConsumer<T, Throwable>)` — 정상/예외 *둘 다* 호출되지만 결과를 *바꾸지 못한다.* 로깅·메트릭·정리 작업용이다. 예외는 *그대로* 다음 단계로 흘러간다.

세 가지를 한 줄로 정리하자. **처리만** 하고 흐름은 그대로: `whenComplete`. **대체 값**으로 복구: `exceptionally`. **둘 다 보고 변환**: `handle`. 흔한 실수가 `whenComplete`로 예외를 *소비했다고 착각*하는 일이다. 소비된 게 아니다. 다음 `.thenApply`는 *여전히* 건너뛴다. *기억해두자.*

Java 12에서 `exceptionallyCompose`가 추가됐다. `exceptionally`의 *flat-map* 버전이다 — fallback이 또 다른 비동기 호출일 때 쓴다.

## Executor를 명시하는 일 — commonPool에 blocking I/O를 태운 *끔찍한 사건*

CF에는 `Async` 접미사 메서드들이 있다. `supplyAsync`·`thenApplyAsync`·`thenComposeAsync` 등이다. *executor 인자를 생략하면* 기본값은 `ForkJoinPool.commonPool()`이다. 8A장에서 본 그 commonPool 말이다.

여기서 *잊지 못할 사건*이 발생한다. 어느 팀의 결제 컨트롤러 — 외부 결제 게이트웨이 호출을 `CompletableFuture.supplyAsync(...)`로 감쌌다. 각 호출은 평균 300ms의 HTTP I/O. 동시 처리 30 RPS. 컨트롤러 자체는 *완벽하게* 동작했다. 그런데 같은 JVM의 *다른* 엔드포인트들이 이상하게 느려졌다. `parallelStream`을 쓰던 리포트 생성 API의 p99가 갑자기 8초를 넘었고, 캐시 갱신 잡이 *대기열에서 사라지지 않고* 쌓이기 시작했다.

원인은 단순했다. 결제 호출이 commonPool의 워커들을 *blocking으로 점유*했고, 그 풀을 함께 쓰는 다른 모든 작업이 *함께 굶었다.* commonPool의 기본 크기는 코어 수 - 1. 16코어 머신에서 15개의 워커가 모두 HTTP 응답을 기다리고 있으면, 새 작업은 무한히 대기한다. *끔찍한 일이다.*

해법은 *항상 executor를 명시하는 것*이다. 다음 코드 한 줄이 규율을 만든다.

```java
private static final ExecutorService HTTP_POOL =
    Executors.newFixedThreadPool(64, r -> Thread.ofPlatform().name("http-", 0).unstarted(r));
// ...
CompletableFuture.supplyAsync(() -> client.call(req), HTTP_POOL);
```

I/O bound 작업은 *I/O 전용 풀*에, CPU bound 작업은 *코어 수 기준 풀*에, 그리고 Loom 시대에는 *virtual thread per task executor*에 — 이 셋을 *기억해두는 편이 낫다.* commonPool은 짧은 CPU bound 작업, 그리고 명시적으로 안전한 곳에만 쓰자.

## allOf · anyOf — 다수 결합의 두 모양

`allOf(CompletableFuture... cfs)`는 *모두* 완료될 때 끝난다. 결과 타입은 `CompletableFuture<Void>`다 — 각 CF의 결과는 *따로 꺼내야* 한다. 위 도입 예제가 정확히 이 패턴이다.

`anyOf(CompletableFuture... cfs)`는 *하나라도* 완료되면 끝난다. 결과 타입은 `CompletableFuture<Object>`. 빠른 응답을 우선하는 미러링·캐시 hedging에 쓴다.

타임아웃은 Java 9에서 추가된 `orTimeout(duration, unit)`과 `completeOnTimeout(value, duration, unit)`로 깔끔해진다. 이전엔 `ScheduledExecutorService`로 손수 만들어야 했다.

```java
fetchUser(id)
    .orTimeout(1, TimeUnit.SECONDS)
    .exceptionally(ex -> User.guest()); // 1초 넘으면 guest로
```

## Executor·ExecutorService·ScheduledExecutorService — 실행자의 세 층

CF의 *어디서* 실행되는가에 대한 답은 결국 `Executor` 인터페이스다. 가장 얇은 상위 타입이 `Executor` — `execute(Runnable)` 하나뿐이다. 그 위에 라이프사이클과 결과 반환을 더한 것이 `ExecutorService`다. `submit`, `invokeAll`, `shutdown`이 여기서 등장한다. 그 위에 시간 기반 예약을 더한 것이 `ScheduledExecutorService` — `schedule`, `scheduleAtFixedRate`, `scheduleWithFixedDelay`다.

`Executors` 팩토리의 메서드들은 모두 한 번씩 정리해두자. `newFixedThreadPool(n)`, `newCachedThreadPool()`, `newSingleThreadExecutor()`, `newScheduledThreadPool(n)`, 그리고 Java 8의 `newWorkStealingPool()`(= `ForkJoinPool`), Java 21의 `newVirtualThreadPerTaskExecutor()`까지. 각각 *서로 다른 워크로드의 모양*을 가정한다. CPU bound인지, I/O bound인지, 짧은 작업의 폭주인지, 주기적 잡인지에 따라 고르자.

`Executors.newCachedThreadPool()`은 한 가지 *함정*이 있다. 큐가 `SynchronousQueue`라서 작업이 들어오면 *무조건 새 스레드를 만든다.* 폭주 시 *수만 개* 스레드를 만들어 OOM을 띄울 수 있다. 알 수 없는 입력 부하 앞에서 이건 무방비다. 운영에선 `newFixedThreadPool` 또는 *명시적 `ThreadPoolExecutor` 빌드*가 더 안전하다.

## ForkJoinPool과 work-stealing의 자리

8A장에서 한 번 짚었지만, 여기서 한 번 더 정리하자. `ForkJoinPool`은 *분할 정복형 CPU bound 작업*에 최적화된 풀이다. 워커마다 자기 deque를 갖고 idle 워커가 다른 워커의 꼬리를 *훔친다.* `RecursiveTask`를 상속해 `compute()`에 base case와 분할 로직을 적으면 끝이다.

`parallelStream()`이 commonPool 위에서 동작한다는 점은 이미 보았다. CF의 `*Async` 메서드 *executor 생략 시* 기본값도 commonPool이다. 한 JVM 안에서 *이 둘이 같은 풀을 공유한다는 사실*을 잊지 말자. 부하가 큰 두 도구를 한 풀에 동시에 풀어놓으면 *예측 불가의 대기*가 따라온다. 풀을 *분리*하는 편이 낫다.

## Java 9 — `Flow`라는 인터페이스 4종

Java 9는 `java.util.concurrent.Flow`라는 *클래스 한 개*를 새로 도입했다. 그 안에 *static 인터페이스 네 개*가 들어 있다. `Publisher`, `Subscriber`, `Subscription`, `Processor`다. JEP 266이다. 이게 자바판 **Reactive Streams**의 표준 인터페이스다.

왜 이게 *언어 표준*에 들어와야 했는가? 2010년대 중반, RxJava·Reactor·Akka Streams·Vert.x 등 여러 reactive 라이브러리가 각자 다른 인터페이스로 *호환되지 않는* 비동기 스트림을 표현하고 있었다. 라이브러리 사이를 *흐름 단위*로 연결하려면 표준이 필요했다. 2013년 시작된 *Reactive Streams Initiative*가 그 표준을 만들었고, Java 9가 그 인터페이스를 *언어 표준 라이브러리*로 끌어들였다. 이제 Reactor의 `Flux`, RxJava의 `Flowable`, MongoDB·Cassandra·R2DBC의 비동기 드라이버가 *모두 같은 인터페이스*로 서로를 받아들인다.

네 인터페이스의 모양은 단순하다.

```java
interface Publisher<T> { void subscribe(Subscriber<? super T> s); }
interface Subscriber<T> {
    void onSubscribe(Subscription s);
    void onNext(T item);
    void onError(Throwable t);
    void onComplete();
}
interface Subscription { void request(long n); void cancel(); }
interface Processor<T,R> extends Subscriber<T>, Publisher<R> {}
```

핵심은 **네 신호**다 — `onSubscribe`, `onNext`, `onError`, `onComplete`. 그리고 결정적으로 `Subscription.request(long n)` — *구독자가 발행자에게 N개를 요청*한다. 이것이 backpressure다.

## backpressure — Reactive가 *어려웠던* 진짜 이유

backpressure를 한 문장으로 설명하면 이렇다. **소비자가 감당할 수 있는 만큼만 생산자에게 요청한다.** 전통적 push 모델에서는 생산자가 무한히 토하면 소비자가 OOM으로 죽거나 큐가 폭주한다. pull 모델은 응답성을 잃는다. Reactive Streams는 그 중간 — *demand-driven push* — 을 택한다. 생산자는 *요청받은 만큼만* push한다. 적정량의 prefetch와 buffer는 구현 측의 자유로 남는다.

이게 *왜 그렇게 어려웠을까?* 세 가지가 겹쳤다.

첫째, *모든 단계*가 비동기·non-blocking이라는 약속을 지켜야 한다. 한 단계라도 blocking이면 전체가 무너진다. JPA의 동기 API, JDBC의 blocking 호출이 reactive 체인 안에 섞이는 순간 — *끔찍한 일이다.* 이게 reactive 도입의 가장 흔한 좌초점이었다.

둘째, *디버깅이 어렵다.* 스택 트레이스가 의미를 잃는다. 람다 체인 안에서 예외가 발생하면 어디서 났는지를 찾아 거슬러 올라가는 일이 가설을 동반한 추리가 된다. Reactor는 `Hooks.onOperatorDebug()` 같은 도구를 제공하지만, 그 자체가 *별도의 학습*이다.

셋째, *추상화의 거리가 멀다.* `map`·`filter`·`flatMap`까지는 익숙하지만, `concatMap`·`switchMap`·`mergeMap`·`window`·`groupBy`·`publishOn`·`subscribeOn`의 차이를 정확히 익히기까지 *몇 달*이 걸린다. 코드 한 줄을 잘못 고르면 *순서가 무너지거나*, *쓰레드가 이동하지 않거나*, *backpressure가 풀려버린다.*

그래서 우리는 자주 묻는다. "그래서 — 그 학습 곡선을 넘어설 만한 *고유한* 가치가 어디에 있는가?" 이 질문의 답은 *지금* 짧게 하기 어렵다. Loom이라는 새로운 패러다임이 등장한 이후 그 답이 *흔들리고 있다*는 사실까지 함께 보아야 정직한 답이 된다. 그 정리는 14장 이후, 그리고 21장의 "WebFlux 유지 시나리오"에서 본격적으로 따져본다. 이 장에서는 *도구의 모양*까지만 가져가자.

## Project Reactor·RxJava와 Flow의 관계

자바 표준의 `Flow`는 *인터페이스*만 정의한다. *연산자*는 없다. `map`·`filter`·`flatMap` 같은 *그 풍성한 컬렉션*은 모두 Reactor나 RxJava 같은 *라이브러리*가 제공한다. Flow는 그 라이브러리들이 *서로 호환되도록* 약속한 *호환 layer*다.

Reactor의 `Flux`·`Mono`는 0~N개·0~1개 비동기 시퀀스를 표현한다. Spring WebFlux의 토대다. `Mono`는 사실상 *single-element Flux*이며, `CompletableFuture`와 *형태가 비슷하지만* 본질적으로 *lazy*하다 — 누군가 `subscribe`하기 전에는 아무것도 실행되지 않는다. CF는 *eager*하다 — `supplyAsync` 호출 시점에 즉시 시작된다. *이 차이는 작지 않다.*

RxJava의 `Observable`·`Flowable`도 같은 자리에 있다. `Observable`은 backpressure 없는 흐름, `Flowable`은 backpressure 있는 흐름이다. 둘 다 Flow의 `Publisher`로 변환 가능하다 — `Flowable.toFlowable()`은 곧 reactive-streams `Publisher`이고, 그 인터페이스가 곧 `Flow.Publisher`다(JDK 9에서 어댑터 한 줄로 연결).

## HttpClient의 비동기 호출 — Java 11의 한 가지 점

Java 11에서 JEP 321로 표준화된 `java.net.http.HttpClient`는 *비동기 API를 처음부터* 갖춘 자바 표준의 HTTP 클라이언트다. `sendAsync(...)`는 `CompletableFuture<HttpResponse<T>>`를 반환한다. 더 나아가 body publisher·subscriber는 `Flow.Publisher`·`Flow.Subscriber`로 모델링된다 — *body를 reactive 스트림으로 받을 수 있다.*

```java
HttpClient client = HttpClient.newBuilder().version(Version.HTTP_2).build();
client.sendAsync(req, BodyHandlers.ofString())
      .thenApply(HttpResponse::body)
      .thenAccept(System.out::println);
```

Apache HttpClient·OkHttp에 대한 자바 표준의 답이다. 단, 풍성한 미들웨어·인터셉터 생태계는 여전히 별도 라이브러리가 채운다. 마이그레이션 맥락에서 이 클라이언트가 어떤 자리에 서는지, RestClient·WebClient와 어떻게 비교되는지는 20장과 21장에서 본격적으로 다시 따져본다. 이 장에서는 *Java 8 이후 동시성 API가 어떻게 진화했는가*의 한 점으로 짚어두자.

## Spring 맥락 — `@Async`·`Mono`/`Flux`·WebClient

Spring의 `@Async`는 가장 익숙한 비동기 도구다. 메서드에 붙이면 *기본 TaskExecutor*가 그 호출을 별도 스레드에서 실행한다. 반환 타입을 `CompletableFuture<T>`로 두면 호출자가 *조합 가능한* 비동기 결과를 받을 수 있다. 단, *Bean 외부에서 호출*해야 프록시가 적용된다는 함정 — 같은 클래스 내 메서드 호출은 `@Async`가 *동작하지 않는다.* AOP 기반 도구의 공통된 한계다.

Spring WebFlux는 `Mono<T>`·`Flux<T>`를 컨트롤러 반환 타입으로 받는다. Reactor 위에 세워진 서버 스택 — Netty 기반, non-blocking, demand-driven. 도구 자체는 강력하다. 그러나 *전체 스택이 non-blocking이어야* 비로소 의미가 있다. JDBC·JPA가 끼는 순간 그 약속은 깨진다(R2DBC가 그 빈자리를 메우려 했지만, JPA 생태계의 무게에 비해 *얇다*).

`WebClient`는 reactive HTTP 클라이언트다. `client.get().uri(...).retrieve().bodyToMono(User.class)` 같은 체인이 *지연 실행 reactive 흐름*을 만든다. CF와 다르게 *subscribe 전에는 실행되지 않는다.* `.block()`을 호출하면 동기처럼 변하지만, *그 순간 reactive의 모든 장점이 사라진다.* 그래서 우리는 *함부로 `.block()`을 부르지 않는다 —* 기억해두자.

`@Async` + `CompletableFuture`와 reactive + `Mono`/`Flux`는 *서로 다른 패러다임*이다. 둘 사이의 변환도 가능하지만(`Mono.fromFuture`, `Mono.toFuture`), 두 모델을 *한 컨트롤러 안에서 자유롭게 섞는 일*은 좋지 않은 결과를 낳는다. 일관성을 유지하자.

## 마무리

이 장에서 우리는 비동기 *조합*의 두 갈래를 함께 걸었다. `Future`의 단순한 약속에서 `CompletableFuture`의 풍성한 조합 연산자로, 그리고 다시 `Flow` 인터페이스가 표현하는 *demand-driven push*로. 한 갈래는 *값 중심*의 비동기다 — 작업 하나의 결과를 깔끔히 조합한다. 다른 한 갈래는 *흐름 중심*의 비동기다 — 0개에서 무한 개의 신호가 backpressure와 함께 흘러간다. 둘은 다른 도구가 아니라 *다른 추상화의 층*이다.

그리고 한 가지 정직하게 인정하고 가자. 이 장의 도구들은 모두 *Loom 이전*의 답이다. virtual thread가 *thread-per-request*를 다시 합리적으로 만든 이후, "왜 굳이 reactive로 짜야 하는가?"라는 질문은 *전제 자체가 흔들린* 자리에 서 있다. 14장에서 Loom을 만나고, 21장에서 WebFlux 유지 시나리오를 따져본 다음에 비로소 *이 모든 도구의 진짜 가치*를 다시 평가할 수 있다. 지금은 두 갈래의 풍경을 *기억해두는 편이 낫다.* 도구가 바뀌어도, 비동기 조합의 *어휘*는 같은 자리에 남아 있을 것이다.

이제 동시성의 첫 막은 닫힌다. 다음 Part는 언어 표면의 진화 — JPMS와 `var`·switch·text blocks가 우리 코드의 *색깔*을 어떻게 바꿔놓았는지부터 다시 시작하자.
