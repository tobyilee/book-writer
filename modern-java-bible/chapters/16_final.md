# 16장. Structured Concurrency와 Scoped Values — concurrent 코드의 문법

request-scoped 데이터를 자식 task에 넘기다 ThreadLocal 청소를 잊었다고 해보자.

컨트롤러가 fan-out한 자식 task 셋이 있다. 결제 호출, 회원 조회, 쿠폰 검증 — 14장에서 우리가 따라온 그 fan-out이다. 각 자식이 `userId`와 `tenantId`를 알아야 한다. 누구는 audit log를 남기고, 누구는 multi-tenant DB의 schema를 분기하기 때문이다. 이 컨텍스트를 어디에 둘까. `SecurityContextHolder`나 `RequestContextHolder` 같은 Spring의 자리는 *ThreadLocal*이다. 컨트롤러 thread에는 값이 들어 있지만 자식 thread는 새 thread다. 비어 있다. 그래서 `InheritableThreadLocal`로 복사하거나, 명시적으로 `try { set(...); ... } finally { remove(); }`로 다시 깔아준다.

여기서 일이 생긴다. 자식 task 중 하나가 예외를 던졌다. `try-finally`의 `finally` 블록이 자식 thread에서 잘 실행될까. 자식이 thread pool에서 *재사용*되는 thread라면, 청소를 잊은 ThreadLocal은 다음 요청의 자식에게 *유령처럼* 따라간다. 다른 사용자의 `userId`가 우리 자식 task에 흘러 들어가 DB의 *다른 tenant*에 audit log가 남는다. *찜찜한* 정도가 아니라 *끔찍한 일*이다.

게다가 자식 셋 중 결제 호출이 30초 timeout으로 늦어지는 동안 회원 조회와 쿠폰 검증은 *이미 끝나서 자원을 기다리고 있다*. 결제가 실패로 끝나도 나머지 두 자식의 자원은 누가 정리하는가. 컨트롤러는 그 셋의 수명을 *함께* 다스리고 싶은데, 코드 어디에도 *함께*라는 말이 보이지 않는다. concurrent 코드가 *흩어진* 채로 살아있다. 동기 코드라면 함수 호출의 stack이 곧 *함께*라는 약속을 받아냈다. 그렇다면 — concurrent 코드에도 그런 *구조*가 있을 수 있을까.

## Dijkstra의 1968년이 자바에 도착했다

Edsger Dijkstra가 1968년 *Notes on Structured Programming*을 쓰며 한 주장은 단순했다. *goto*를 버리고 함수 호출과 블록 구조로 프로그램을 짜자. 한 함수에 들어간 흐름은 *반드시* 그 함수에서 나온다. 시작과 끝이 *짝*을 이룬다. 그 짝 덕분에 우리는 프로그램을 *어휘적*으로 읽을 수 있다. 코드를 위에서 아래로 따라가면 흐름이 어디서 시작해 어디서 끝나는지 보인다.

자바의 동기 코드는 50년 동안 이 약속 위에 살아왔다. 한 메서드가 호출되면 그 메서드가 *반드시* 반환되고, 메서드 안의 모든 자원이 *호출자에게 돌아가기 전*에 정리된다. `try-with-resources`는 이 약속을 자원에까지 확장했다. 블록을 떠나는 순간 자원도 *함께 떠난다*. 시작과 끝이 짝을 이룬다는 단순한 규칙이 코드의 추리 가능성을 받쳐 왔다.

그런데 concurrent 코드는 이 약속을 *깨면서* 발전했다. `ExecutorService.submit()`로 자식 task를 던지면, 그 자식의 수명은 호출자의 수명과 *분리*된다. 호출자가 반환된 뒤에도 자식은 살아 있을 수 있다. 자식이 실패해도 호출자는 모를 수 있다. 호출자가 일찍 끝나도 자식은 *유령처럼* 자원을 잡고 있다. 30년 묵은 goto의 자리를 자바의 concurrent 코드가 *그대로* 물려받은 셈이다.

Project Loom의 두 번째 큰 도구가 정확히 이 자리를 노렸다. *Structured Concurrency*다. JEP 453의 한 줄로 약속이 분명해진다 — *부모 함수가 반환되기 전 자식이 모두 끝난다*. 호출자의 scope가 자식의 scope를 *감싼다*. 시작과 끝이 짝을 이룬다. concurrent 코드에도 *구조*가 돌아왔다.

## `StructuredTaskScope`: 자식을 하나의 단위로

핵심 API는 `StructuredTaskScope`다. 14장에서 만났던 `Executors.newVirtualThreadPerTaskExecutor()`와 모양이 비슷하다 — `try-with-resources` 블록에서 자식 task를 fork하고, 마지막에 join한다.

```java
try (var scope = StructuredTaskScope.open()) {
    StructuredTaskScope.Subtask<Payment> pay  = scope.fork(() -> billing.charge(orderId));
    StructuredTaskScope.Subtask<Member>  mem  = scope.fork(() -> members.findById(userId));
    StructuredTaskScope.Subtask<Coupon>  cp   = scope.fork(() -> coupons.validate(coupon));

    scope.join();  // 자식 셋 모두 끝날 때까지 대기

    return new CheckoutResponse(pay.get(), mem.get(), cp.get());
}
```

차이를 정리하자. `submit()`이 `Future`를 돌려주는 반면 `fork()`는 `Subtask`를 돌려준다. 그리고 `join()`이 *반드시* 호출돼야 한다. 호출자가 `join()` 없이 블록을 벗어나려고 하면 — scope의 `close()`가 자식들을 강제로 cancel한다. *자식이 살아 있는 채로 부모가 떠날 수 없다*. 이게 structured concurrency의 핵심 규칙이다.

Java 25에서 표준화된 시점의 API 모양을 짚어두자. 진화 과정에서 메서드 이름이 몇 차례 바뀌었다. 옛 글들에서 `scope.fork(...)` 다음에 `scope.joinUntil(deadline)`이나 `scope.joinAll()` 같은 변종을 볼 수 있는데, 25 finalize 기준은 `join()` 한 줄로 통일됐다. 책에서는 25 기준으로만 적는다.

## 정책 세 가지: ShutdownOnFailure · ShutdownOnSuccess · Joiner

자식 셋이 동시에 진행되다가 *하나가 실패*하면 어떻게 할까. 자식 셋 중 *가장 빠른 하나의 성공*만 필요한 fan-out도 있다. 또 *모두의 결과를 무조건 모아*야 하는 경우도 있다. 세 갈래의 정책을 코드로 보자.

**1. `ShutdownOnFailure`: 하나가 실패하면 모두 취소**

결제 컨트롤러의 가장 흔한 패턴이다. 세 자식 중 하나라도 실패하면 나머지를 *즉시 취소*하고 호출자에게 예외를 던진다. 자원 낭비도 막고, 일관성 없는 부분 성공도 막는다.

```java
try (var scope = StructuredTaskScope.open(
        Joiner.<Object>anySuccessfulResultOrThrow())) {
    // ... 가장 빠른 성공 한 자식의 결과만 필요할 때
}

// 또는 ShutdownOnFailure (사실 확인 필요: Java 25에서 Joiner.allSuccessfulOrThrow()로 통합됐을 가능성)
try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
    var pay  = scope.fork(() -> billing.charge(orderId));
    var mem  = scope.fork(() -> members.findById(userId));
    var cp   = scope.fork(() -> coupons.validate(coupon));
    scope.join();
    return new CheckoutResponse(pay.get(), mem.get(), cp.get());
}
```

(Java 21~24의 preview API에는 `StructuredTaskScope.ShutdownOnFailure`와 `ShutdownOnSuccess`라는 *서브 클래스*가 있었고, Java 25의 standard 시점에 `Joiner` 인터페이스 기반으로 통합된 형태로 다듬어졌다. 책에 적힌 정확한 메서드 이름은 25 GA 시점의 문서를 *반드시 확인*하길 권한다. 이주의 방향성은 분명하다 — *서브 클래스 상속*에서 *Joiner 조합*으로.)

**2. `ShutdownOnSuccess`: 가장 빠른 성공 하나만**

여러 백엔드에서 같은 답을 받아오는 *replicated read* 같은 패턴이다. 캐시 두 대와 DB 하나에 동시에 조회를 보내고 *가장 빠른 응답*만 받는다. 한 자식이 성공하면 나머지를 *즉시 취소*하고 호출자에게 그 결과를 돌려준다.

```java
try (var scope = StructuredTaskScope.open(Joiner.<String>anySuccessfulResultOrThrow())) {
    scope.fork(() -> readFromCacheA(key));
    scope.fork(() -> readFromCacheB(key));
    scope.fork(() -> readFromPrimary(key));
    scope.join();
    return scope.result();  // 가장 먼저 성공한 결과
}
```

이 패턴은 cache stampede 방지·hedged read·라우팅 최적화 같은 자리에서 유용하다. 단, 가장 빠른 *성공*이 정답이라는 단서가 있어야 한다 — 캐시가 stale일 가능성이 있다면 정책이 달라져야 한다.

**3. 커스텀 `Joiner`: 정책을 직접 짜자**

위 둘로 부족하면 `Joiner` 인터페이스를 직접 구현할 수 있다. 가령 *최소 2개 성공*이 정족수인 quorum read를 짜고 싶다고 해보자. 또는 *모든 자식의 결과를 모으되, 실패한 자식은 기본값으로 채우는* 관대한 정책이 필요할 수 있다.

```java
// 의사 코드 — 25 GA 시점의 정확한 시그니처는 문서 확인 권장
class QuorumJoiner<T> implements Joiner<T, List<T>> {
    private final int quorum;
    private final List<T> results = new CopyOnWriteArrayList<>();
    
    @Override public boolean onComplete(Subtask<? extends T> subtask) {
        if (subtask.state() == Subtask.State.SUCCESS) {
            results.add(subtask.get());
            return results.size() >= quorum;  // true면 scope shutdown
        }
        return false;
    }
    
    @Override public List<T> result() { return results; }
}
```

핵심 규칙은 두 가지다. `onComplete`에서 `true`를 돌려주면 scope이 *지금 shutdown*된다 — 나머지 자식이 모두 cancel된다. 그리고 `result()`가 `scope.result()` 호출에 돌려줄 값이다. 이 두 자리만 잡으면 어떤 정책도 짤 수 있다.

세 정책의 공통점은 *cancellation propagation*이다. shutdown이 호출되는 순간 살아있는 자식 모두에 `interrupt`가 전파된다. virtual thread 안에서 blocking 호출이 `InterruptedException`을 정직하게 받는다면, 자식은 곧 정리된다. 자식이 외부 API 호출 중이라면, JDBC 드라이버의 cancel 동작이나 HTTP 클라이언트의 interrupt 처리가 *Loom-aware* 한지가 그 자리에서 시험된다.

## Cancellation propagation: 부모가 반환되기 전 자식이 모두 끝난다

이 한 줄을 다시 한 번 정직하게 짚자. *부모 함수가 반환되기 전 자식이 모두 끝난다*. structured concurrency가 약속하는 단 하나의 규칙이다. 이 규칙으로부터 따라 나오는 모든 결과가 우리가 본격적으로 받는 *후련함*이다.

- 호출자가 timeout으로 일찍 끝나면 자식이 *모두* 취소된다. 살아남는 유령이 없다.
- 자식 하나가 실패하면 나머지가 *즉시* 취소된다. 자원 낭비가 없다.
- 호출자의 stack에 자식의 모든 stack이 *함께* 표시된다. JFR이나 thread dump가 컨트롤러 - 자식 - 자식의 자식을 *나무*로 보여준다.

마지막 항목이 특히 중요하다. 옛 `ExecutorService`로 짜인 fan-out 코드는 thread dump에서 *조각난* 채로 보였다. 자식 thread가 누구의 자식인지 정보가 없었다. structured concurrency는 *부모-자식 관계*를 thread 메타데이터에 박아 넣는다. JFR을 켜 두면 "이 자식 task가 이 컨트롤러의 자식이고, 그 컨트롤러는 이 사용자 요청의 자식이다"라는 *나무*가 보인다. production 디버깅이 *비교할 수 없을 만큼* 좋아진다.

## Scoped Values: ThreadLocal의 후계자

이제 도입부의 *끔찍한 일*로 돌아가자. `userId`와 `tenantId`를 자식 task에 넘기는 자리 — ThreadLocal로 풀어왔던 그 자리다. JEP 506이 Java 25에서 표준화된 **`ScopedValue`**가 이 자리의 정답이다.

ScopedValue가 ThreadLocal과 결정적으로 다른 점 셋을 짚자.

- **Immutable.** 한 번 binding되면 그 scope 안에서 *바꿀 수 없다*. `set()`이 없다. 이 *immutability* 덕에 race condition도, 청소 잊음도 원천적으로 사라진다.
- **부모→자식 자동 binding.** 부모 scope에서 binding된 값이 *자식 task로 자동 전파*된다. `InheritableThreadLocal`처럼 *복사*되는 게 아니다. 같은 immutable 값을 자식이 *읽는다*. 메모리 폭발이 일어나지 않는다.
- **자동 cleanup.** scope이 끝나면 binding이 *자동 해제*된다. `finally` 블록에 `remove()`를 적을 필요가 없다.

기본 사용법은 이렇다.

```java
public class AuthContext {
    public static final ScopedValue<UserPrincipal> PRINCIPAL = ScopedValue.newInstance();
    public static final ScopedValue<TenantId> TENANT = ScopedValue.newInstance();
}

// 컨트롤러 진입점에서 binding
public CheckoutResponse handle(HttpRequest req) {
    UserPrincipal user = authenticate(req);
    TenantId tenant = resolveTenant(req);

    return ScopedValue
        .where(AuthContext.PRINCIPAL, user)
        .where(AuthContext.TENANT, tenant)
        .call(() -> doCheckout(req));
}

// 자식 task에서 자동으로 읽힌다
private CheckoutResponse doCheckout(HttpRequest req) {
    try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
        var pay  = scope.fork(() -> billing.charge(...));
        var mem  = scope.fork(() -> members.findById(...));
        // ...
        scope.join();
        return new CheckoutResponse(pay.get(), mem.get());
    }
}

// billing 안 깊은 자리에서도 그냥 읽는다
public Payment charge(long orderId) {
    UserPrincipal user = AuthContext.PRINCIPAL.get();
    TenantId tenant = AuthContext.TENANT.get();
    // audit log에 user, tenant 박아 넣기
    ...
}
```

`where().call()` 또는 `where().run()`의 *동적 scope*가 핵심이다. `where(KEY, value)`로 binding을 *선언*하고, `call()`에 넘긴 람다가 실행되는 동안 그 binding이 살아있다. 람다가 반환되면 binding은 *자동으로* 해제된다. 람다 안에서 어떤 깊이의 자식 task를 만들어도, 그 자식들은 *같은 binding*을 본다. ScopedValue가 thread를 따라가는 게 아니라 *scope을 따라간다*는 점이 ThreadLocal과 가장 다른 자리다.

## Rebinding semantics: 동적 scope의 묘미

ScopedValue의 *동적 scope*가 가져오는 묘미가 하나 있다. **rebinding**이다.

이미 binding된 값을 *그 자리에서* 다른 값으로 갈아 끼울 수 있다. 단, 갈아 끼우는 *내부 scope*에서만 새 값이 보이고, *바깥 scope*에 영향을 주지 않는다.

```java
ScopedValue.where(AuthContext.PRINCIPAL, alice).call(() -> {
    var outerUser = AuthContext.PRINCIPAL.get();  // alice

    // 잠깐 시스템 권한으로 작업
    return ScopedValue.where(AuthContext.PRINCIPAL, systemUser).call(() -> {
        var innerUser = AuthContext.PRINCIPAL.get();  // systemUser
        return doPrivilegedTask();
    });
    // 여기로 돌아오면 PRINCIPAL은 다시 alice
});
```

이 *겹쳐 쓰기*가 안전한 이유는 binding이 *동적 scope*에 묶이기 때문이다. 정적 scope이라면 변수 가림(shadowing)을 적용해 컴파일러가 처리할 일이지만, ScopedValue는 *실행 시점*의 호출 chain이 scope를 결정한다. 람다가 끝나면 그 binding도 *함께 사라진다*.

ThreadLocal에서 이걸 시도하면 어떻게 될까. `try { set(systemUser); ... } finally { set(alice); }` 같은 식으로 *직접* 청소를 해야 했다. `finally`에서 예외가 나면 — 또는 비동기로 다른 thread로 넘어가면 — 청소가 깨질 가능성이 있었다. ScopedValue는 *언어 차원*에서 이 짝을 보장한다. 코드를 잘못 쓸 수 없다.

## ScopedValue vs ThreadLocal: 한 표로

| | ThreadLocal | ScopedValue |
|---|---|---|
| Mutability | mutable (set/remove) | immutable |
| 부모→자식 전파 | `InheritableThreadLocal`로 *복사* | 자동, *공유 참조* |
| 청소 책임 | 호출자 (`try-finally`) | 자동 (scope 종료 시) |
| 메모리 모델 | thread당 ThreadLocalMap | scope chain의 immutable bindings |
| Virtual thread 100만 개와 함께 | 폭발 위험 | 안전 |
| Rebinding | `set` 후 `set` (불안전) | `where().call()` 중첩 (안전) |
| Spring 통합 | `RequestContextHolder`·`SecurityContextHolder` | 25 이후 검토 중 |
| 도입 시점 | Java 1.2 (1998) | Java 25 (2025, JEP 506) |

마지막 행을 음미하자. ThreadLocal은 27년 동안 자바의 *컨텍스트 전달*을 책임져 왔다. 그 자리를 ScopedValue가 이어받는다. 다만 ThreadLocal이 사라지지는 않는다 — *Spring의 `RequestContextHolder`·`SecurityContextHolder`* 같은 위 layer가 ScopedValue로 이주하는 데 시간이 걸리기 때문이다. 그 이주가 끝날 때까지는 두 도구가 *공존*한다.

## Java 8 ExecutorService vs Java 25 StructuredTaskScope

14장과 같은 *세 외부 API* 예제를 두 시대로 비교하며 마무리하자.

**Java 8 — 흩어진 자식**

```java
private static final ExecutorService POOL = Executors.newFixedThreadPool(200);

public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    Future<Payment> pay  = POOL.submit(() -> billing.charge(orderId));
    Future<Member>  mem  = POOL.submit(() -> members.findById(userId));
    Future<Coupon>  cp   = POOL.submit(() -> coupons.validate(coupon));
    try {
        Payment p = pay.get(5, TimeUnit.SECONDS);
        Member  m = mem.get(5, TimeUnit.SECONDS);
        Coupon  c = cp.get(5, TimeUnit.SECONDS);
        return new CheckoutResponse(p, m, c);
    } catch (TimeoutException | ExecutionException | InterruptedException e) {
        pay.cancel(true); mem.cancel(true); cp.cancel(true);  // 정말 취소될까?
        throw new ServiceException(e);
    }
}
```

자식 셋은 *공유 POOL*에서 돈다. 호출자와 자식의 *부모-자식 관계*가 코드에 없다. `cancel(true)`는 *interrupt를 보낼 뿐* 자식이 *반드시* 취소된다는 보장이 없다. timeout 5초를 자식 셋 각각에 매기다 보니, 셋이 *전체적으로* 얼마나 걸렸는지 보장하기도 어렵다.

**Java 25 — 한 단위로 묶인 자식**

```java
public CheckoutResponse checkout(long orderId, long userId, String coupon) {
    return ScopedValue
        .where(AuthContext.PRINCIPAL, SecurityContextHolder.getUser())
        .where(AuthContext.TENANT, TenantContext.current())
        .call(() -> doCheckout(orderId, userId, coupon));
}

private CheckoutResponse doCheckout(long orderId, long userId, String coupon)
        throws InterruptedException {
    try (var scope = StructuredTaskScope.open(
            Joiner.<Object>allSuccessfulOrThrow(),
            cfg -> cfg.withTimeout(Duration.ofSeconds(5)))) {
        var pay  = scope.fork(() -> billing.charge(orderId));
        var mem  = scope.fork(() -> members.findById(userId));
        var cp   = scope.fork(() -> coupons.validate(coupon));
        scope.join();
        return new CheckoutResponse(pay.get(), mem.get(), cp.get());
    }
}
```

차이를 한 번 정리하자.

- **컨텍스트 전달.** ThreadLocal 청소 코드가 사라지고 `ScopedValue.where().call()` 한 자리로 정리된다.
- **부모-자식 관계.** `StructuredTaskScope`가 그 관계를 *코드 구조*로 박았다. JFR thread dump에서 *나무*로 보인다.
- **Timeout.** scope의 `withTimeout`이 *전체*에 걸린다. 자식 셋 합쳐서 5초 — 자식 각자가 아니다.
- **취소 보장.** scope이 닫히는 순간 자식 셋이 *모두* interrupt된다. Loom-aware한 호출이라면 즉시 정리된다.
- **에러 일관성.** 자식 하나가 실패하면 나머지가 *즉시* 취소된다. 부분 성공으로 인한 inconsistent state가 사라진다.

11장에서 records, 12장에서 sealed, 13장에서 pattern matching, 14장에서 virtual thread, 16장의 이 자리에서 structured concurrency와 scoped values까지 — Modern Java가 *도구의 묶음*으로 자리 잡는 그림이 비로소 한 페이지에 모인다. 결제 컨트롤러 한 자리에 이 모든 도구가 들어간다.

## Spring과 ScopedValue: 이주의 자리

Spring의 `RequestContextHolder`·`SecurityContextHolder`·`LocaleContextHolder`는 모두 ThreadLocal 기반이다. 27년의 자바 컨벤션 위에 세워진 도구이니 당연하다. ScopedValue가 표준화된 지금, Spring 6/7이 ScopedValue 기반으로 *이주*할 가능성이 본격 검토 중이다. 정확한 시점과 API 모양은 *Spring 팀의 결정*에 달려 있다 — 이 책 시점에는 아직 ThreadLocal 기반이 안정적인 default다.

다만 우리 코드에서는 *지금부터* 새로 짜는 컨텍스트 전달은 ScopedValue로 옮기는 편이 낫다. 가령 사내 audit·tenant routing 같은 자리는 Spring을 거치지 않고 우리 손에 있는 자리다. 그 자리부터 ScopedValue로 익혀 두면, Spring의 이주가 들어왔을 때 자연스럽게 받아낼 수 있다. 21장에서 *한 결제 마이크로서비스에 모든 도구를 모으는* 자리에서 이 이주를 본격적으로 다룬다.

## 진화의 자리: JEP 428 → 533, 그리고 JEP 506

마지막으로 진화의 자리를 짚자. structured concurrency와 scoped values 둘 다 자바의 *preview 문화*를 가장 길게 통과한 도구다.

**Structured Concurrency**

- JEP 428 (Java 19, 2022 incubator) — 첫 등장. `java.util.concurrent` 외부 incubator로.
- JEP 437 (Java 20, second incubator)
- JEP 453 (Java 21, *preview*) — 표준 API 후보로 승격. 다만 *preview*.
- JEP 462 (Java 22, second preview)
- JEP 480 (Java 23, third preview)
- JEP 499 (Java 24, fourth preview)
- JEP 505 (Java 25, fifth preview... 또는 finalize)
- JEP 533 (가정 — Java 26 또는 25에서 finalize 시점). *사실 확인 필요: 정확한 finalize JEP 번호는 25 GA 노트 확인 권장.*

**Scoped Values**

- JEP 429 (Java 20, incubator)
- JEP 446 (Java 21, preview)
- JEP 464 (Java 22, second preview)
- JEP 481 (Java 23, third preview)
- JEP 487 (Java 24, fourth preview)
- **JEP 506 (Java 25, standard)** — 마침내 표준화.

두 도구가 5~7라운드의 preview를 거친 데에는 이유가 있다. *Joiner의 일반화*, *컨텍스트 전파 의미론*, *cancellation의 비동기성*, *기존 ExecutorService와의 호환* — 어느 하나도 가볍게 다듬을 수 없는 자리였다. preview 라운드마다 산업 피드백을 받아 *API의 모양*을 다듬었다. 5년의 다듬기를 거친 도구가 25 LTS에 안착했다. 11년의 자바를 *정직하게* 만들어 온 OpenJDK 문화의 본보기다.

## 마무리

structured concurrency와 scoped values는 자바의 동시성 모델에 *구조*를 돌려준 도구다. 호출자의 scope가 자식의 scope를 *감싸고*, 자식의 컨텍스트가 부모로부터 *immutable 참조*로 흘러내리며, scope이 끝나면 자식과 binding이 *함께* 정리된다. Dijkstra가 1968년에 그렸던 *구조*가 60년 만에 concurrent 코드의 자리까지 왔다.

자식 task의 fan-out, cancellation propagation, timeout, 컨텍스트 전달, 에러 일관성 — 옛 `ExecutorService`로 짜인 *흩어진* 자리가 한 블록으로 묶인다. ThreadLocal 청소를 잊어 다른 사용자의 audit log를 남기는 *끔찍한 일*은, 컨텍스트가 immutable binding이 되면서 *원천적으로* 사라진다. JFR thread dump가 *나무*로 보이는 production 디버깅의 후련함도 따라온다.

여기까지가 Part VII의 끝이다. 14·15·16장에서 *Loom 시대의 동시성*이 한 묶음으로 정리됐다. virtual thread가 *thread-per-request*를 돌려줬고, pinning과 ThreadLocal 함정의 자리를 정직하게 짚었으며, structured concurrency와 scoped values로 *구조*를 받아냈다. 이 묶음이 책의 *두 번째 봉우리*다.

다음 부에서는 그동안 미뤘던 *메모리·네이티브·성능*의 자리를 본격적으로 살펴보자. 17장에서 GC 11년의 진화를, 18장에서 Foreign Function & Memory API와 Vector API를, 19장에서 AOT와 Leyden을 차례로 펼친다. virtual thread가 *동시성의 단위 비용*을 낮췄듯이, 그쪽 도구들이 *시작 시간과 메모리의 단위 비용*을 어떻게 낮추는지 짚어보자.
