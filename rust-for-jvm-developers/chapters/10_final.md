# 10장. async와 tokio — Spring WebFlux/Kotlin Coroutine 다음의 모델

월요일 오후, 마이크로서비스 한 대가 외부 API 열 곳을 동시에 호출하고 결과를 합산해 응답해야 한다고 해보자. JVM 출신이라면 머릿속에 곧장 세 가지 그림이 떠오른다. *CompletableFuture* 체인, *Spring WebFlux*의 `Mono.zip`, 또는 *Kotlin Coroutine*의 `coroutineScope { ... }`. Java 21을 쓴다면 *Virtual Thread*에 그냥 블로킹 호출 열 개를 던져도 된다. 이 네 모델 사이를 오가본 사람일수록 새 도구 앞에서 한 가지 질문을 먼저 던지게 된다. *Rust async는 이 중에서 어디에 가깝고, 어디가 다른가?*

가장 짧은 답을 먼저 적어두자. 사용 감각은 **Kotlin Coroutine과 가장 비슷하다**. `suspend` 키워드 자리에 `async`가 들어가고, `await`가 `.await`로 바뀐다. 콜백이 사라지고 sequential하게 읽힌다. 그런데 한 발만 더 들어가면 차이가 드러난다. 첫째, **runtime을 우리가 직접 골라야 한다.** 둘째, **`Future`는 컴파일러가 만들어주는 상태 머신이라서 모양이 *훨씬 더 명시적*이다.** 셋째, 지금부터 본격적으로 다룰 *function coloring* 문제 — async fn과 sync fn이 *언어 차원에서 분리*되어 있다.

이 챕터의 한 문장을 미리 적어두자. **async는 마법이 아니다 — `Future`는 상태 머신이고, `.await`는 그 상태 머신의 일시 정지점일 뿐이다.** 이 한 문장을 머리에 박은 채로 들어가면, 처음 만나는 `Pin`도, `Send` 경계도, `tokio::spawn`이 까칠하게 구는 이유도 *이미 알던 것의 이름*이 된다.

## Future는 상태 머신이다 — 모델부터 잡고 들어가자

설명을 잠깐 미루고 코드 한 줄을 보자.

```rust
async fn greet(name: &str) -> String {
    format!("hello, {name}")
}
```

이게 사실은 *함수 정의*가 아니다. 컴파일러가 이걸 다음과 비슷한 모양으로 펼친다(엄밀한 코드는 아니고 *모델*이다).

```rust
fn greet(name: &str) -> impl Future<Output = String> {
    GreetFuture { name, state: 0 }
}

struct GreetFuture<'a> {
    name: &'a str,
    state: u8,
}

impl<'a> Future for GreetFuture<'a> {
    type Output = String;
    fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<String> {
        // 상태 머신을 한 단계 진행시킨다.
        // .await가 없으니 곧장 Ready를 돌려준다.
        Poll::Ready(format!("hello, {}", self.name))
    }
}
```

`async fn`은 *호출하는 순간 실행되는* 함수가 아니다. *`Future`라는 상태 머신을 만드는* 팩토리에 가깝다. 그 상태 머신을 *어떻게 진행시킬지*는 우리가 정한 runtime이 결정한다. 그래서 `tokio::spawn`이 등장하기 전까지는 우리 코드가 *한 줄도 실행되지 않는다*.

`.await`는 그 상태 머신의 *일시 정지점*이다. 컴파일러는 `.await`가 등장할 때마다 상태 머신에 새 분기를 만든다. 함수 안에 `.await`가 두 개 있으면 상태가 0, 1, 2(완료) 세 가지다. JVM의 `CompletableFuture.thenApply` 체인이 *런타임에 객체로 표현된 그래프*라면, Rust의 async는 *컴파일러가 정적으로 펼친 enum*이다.

이 모델 차이가 실무에서 어떻게 드러나는지 잠시 짚자.

- *컴파일 타임에 펼쳐진다* → 런타임 비용이 거의 없다. heap allocation이 최소화된다. 사례 4의 Cloudflare Pingora가 *CPU 70% 절감*을 본 데에는 이 zero-cost async가 한몫했다.
- *상태 머신이 정적이다* → 그 안에 `&mut` 빌림이 살아 있는 채로 `.await`를 만나면, 컴파일러가 5장의 빌림 규칙 그대로 거부한다. JVM처럼 *런타임에 race를 만들고 발견*하지 않는다.
- *runtime이 분리된다* → 표준 라이브러리는 `Future` trait만 정의한다. *poll을 누가 호출할지*는 우리가 고른다. 자유의 대가다.

이 모델을 한 번 잡아두면, 나머지는 모두 *이 위에 얹는 도구*다.

## #[tokio::main] — 첫 async 코드를 띄워보자

가장 단순한 모양부터 손에 묻혀보자.

```rust
// Cargo.toml
// [dependencies]
// tokio = { version = "1", features = ["full"] }

#[tokio::main]
async fn main() {
    let s = greet("toby").await;
    println!("{s}");
}

async fn greet(name: &str) -> String {
    format!("hello, {name}")
}
```

`#[tokio::main]`이 하는 일은 한 줄로 적을 수 있다. *`main` 함수를 동기 함수로 두되, 그 안에 tokio runtime을 띄우고 우리의 async main을 그 위에서 실행한다*. 이걸 직접 풀어 적으면 이렇다.

```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let s = greet("toby").await;
        println!("{s}");
    });
}
```

`block_on`은 *동기 세계와 async 세계의 다리*다. 이 함수가 *지금 스레드를 점유한 채* async 블록이 끝날 때까지 기다린다. 9장에서 만난 `thread::spawn(...).join()`과 정신은 같은데, 여기서는 *runtime 위의 task*가 그 자리를 차지한다.

JVM 출신에게 이 자리는 어디일까? Spring Boot의 `main` 메서드에서 `SpringApplication.run`이 *`ApplicationContext`를 띄우는 일*과 거의 같은 자리다. Spring Boot가 *tomcat이나 reactive netty를* 우리 등 뒤에서 띄워주듯, `#[tokio::main]`이 *tokio runtime*을 등 뒤에서 띄워준다. 다만 *어떤 runtime을 띄울지*가 어노테이션 뒤에 숨어있지 않고 *우리가 직접 골랐다는 사실*이 코드에 박혀 있다.

## tokio::spawn과 JoinHandle — 동시 작업의 첫 모양

이제 동시에 여러 작업을 굴려보자. JVM의 `CompletableFuture.supplyAsync(() -> ...)` 또는 Kotlin의 `async { ... }`의 자리다.

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let h1 = tokio::spawn(async {
        sleep(Duration::from_millis(200)).await;
        "task A 완료"
    });
    let h2 = tokio::spawn(async {
        sleep(Duration::from_millis(100)).await;
        "task B 완료"
    });

    let (a, b) = tokio::join!(h1, h2);
    println!("{}, {}", a.unwrap(), b.unwrap());
}
```

`tokio::spawn`은 task를 *runtime의 스케줄러*에 던진다. 반환값은 `JoinHandle<T>`다. `JoinHandle`이 `Future`를 구현하므로 그대로 `.await`할 수 있고, 여러 개를 모으려면 `tokio::join!` 매크로를 쓰는 편이 편하다. 9장의 `std::thread::spawn(...).join()`과 *시그니처가 거의 같은데*, 차이는 한 가지다 — *수만 개를 띄워도 안 죽는다*.

이게 work-stealing 스케줄러의 보상이다. tokio의 워커는 보통 CPU 코어 수만큼 OS 스레드를 띄우고, 각 워커가 *수천 개의 task*를 자기 local queue에 들고 있다가 *바쁘지 않으면 다른 워커의 queue에서 훔쳐온다*. Go·Erlang의 검증된 패턴이다 — 그래서 *20,768개 crate가 tokio에 의존한다*. 사실상 표준이다.

여기서 함정 하나를 미리 짚어두자. `tokio::spawn`이 받는 future는 *`Send + 'static`*이어야 한다. 9장에서 본 그 두 단어다. 새 task가 어느 워커 스레드에서 돌아갈지 *컴파일 타임에 모르므로* — work-stealing이니까 — Send 제약이 생긴다. 그리고 task가 spawn 함수보다 오래 살 수 있으니 `'static`이 필요하다. 9장에서 `Rc<T>`가 spawn에서 거부됐던 이유가 여기서 *그대로 다시 등장한다*. 컴파일러가 보내는 메시지는 *"`Rc<...>` cannot be sent between threads safely"* — 9장에서 본 그 모양이다.

## select! — 여러 future 중 먼저 끝나는 것

JVM에서 `CompletableFuture.anyOf` 또는 Kotlin coroutine의 `select { ... }`로 풀던 일이다. *외부 API 두 곳에 같은 질문을 던지고 먼저 답하는 쪽을 받는다, 또는 timeout 채널과 데이터 채널을 동시에 기다린다*.

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let a = async {
        sleep(Duration::from_millis(200)).await;
        "느린 응답"
    };
    let b = async {
        sleep(Duration::from_millis(50)).await;
        "빠른 응답"
    };

    tokio::select! {
        result = a => println!("a 먼저: {result}"),
        result = b => println!("b 먼저: {result}"),
    }
}
```

`select!`가 두 future를 동시에 polling하다가 *먼저 ready가 되는 쪽*의 분기를 실행한다. 다른 쪽은 *그 자리에서 drop된다* — 즉 cancel된다. JVM의 `CompletableFuture.anyOf`는 다른 future를 *명시적으로 cancel하지 않으면 그대로 굴러간다*는 점에서 다르다. Rust의 `select!`는 cancellation이 *기본*이다. 이 차이가 *connection 누수* 같은 함정을 줄여준다 — *물론 select 분기 안에 락을 잡고 있었다면 그 락이 풀리는지를 우리가 봐야 한다*.

## tokio::sync — 채널과 동기화 기본 도구

9장에서 `std::sync::mpsc`를 봤다. 이름이 같고 의도도 같지만, async 세계에서는 *그 도구를 쓰면 안 된다*. blocking이기 때문이다 — 한 task가 std mpsc의 `recv()`에서 블록되면 그 task가 점유한 워커 스레드 전체가 멈춰버린다. 다른 수천 개 task가 *그 한 줄 때문에* 굳는다.

처방은 `tokio::sync::*`다.

```rust
use tokio::sync::{mpsc, oneshot, broadcast, watch};

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<String>(32); // bounded.

    tokio::spawn(async move {
        for i in 0..3 {
            tx.send(format!("작업 {i}")).await.unwrap();
        }
    });

    while let Some(msg) = rx.recv().await {
        println!("받음: {msg}");
    }
}
```

`mpsc`(다대일), `oneshot`(단일 응답 — request/reply 패턴), `broadcast`(다대다 fan-out), `watch`(가장 최근 값만 읽는 SPSC 옵저버) — 네 가지가 거의 모든 패턴을 커버한다. JVM 출신에게 매핑하면 이렇다.

- `mpsc` ↔ `BlockingQueue` (단, async 친화)
- `oneshot` ↔ `CompletableFuture` 자체 (한 번 보내고 끝)
- `broadcast` ↔ `EventBus`/`SubmissionPublisher`
- `watch` ↔ Kotlin `StateFlow`

채널만이 동기화 도구가 아니다. `tokio::sync::Mutex`도 있다. *9장의 `std::sync::Mutex`와 무엇이 다르냐?* 핵심 한 줄: **`tokio::sync::Mutex::lock()`은 `.await`가 가능하다.** 즉 락을 *기다리는 동안* 다른 task가 같은 워커 스레드에서 진행할 수 있다. 9장의 std Mutex는 OS 스레드를 *그 자리에 멈춰* 세우므로 async에서는 위험하다. 함정 절에서 이 부분을 본격적으로 다시 만난다.

## Mutex와 await — 함정 한 컷

10장에서 가장 유명한 함정이다. 코드를 먼저 보자.

```rust
use std::sync::Mutex;
use std::sync::Arc;

async fn buggy(state: Arc<Mutex<i32>>) {
    let mut guard = state.lock().unwrap();
    *guard += 1;
    do_async_work().await; // 위험!
    *guard += 1;
}

async fn do_async_work() {
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
}
```

이 코드의 무엇이 문제일까? `do_async_work().await`에서 task가 *일시 정지된다*. 그 사이에 *같은 워커 스레드가 다른 task를 굴린다*. 그런데 우리 task는 `std::sync::MutexGuard`를 들고 있다. 만약 그 다른 task도 같은 mutex를 잡으려 한다면 — 데드락이다. 같은 OS 스레드 위의 두 task가 서로를 기다린다.

clippy가 이 패턴을 경고한다(`await_holding_lock` lint). 그리고 `tokio::sync::Mutex`로 바꾸면 잠재적 위험은 사라지지만, *async Mutex는 일반적으로 더 비싸다*. 모범 답안은 셋 중 하나다.

1. **가드 범위를 좁힌다** — `.await` 전에 가드를 drop한다.
   ```rust
   {
       let mut guard = state.lock().unwrap();
       *guard += 1;
   } // 여기서 guard drop.
   do_async_work().await;
   ```
2. **`tokio::sync::Mutex`로 바꾼다** — `.lock().await`가 되고, `.await` 가로질러 들고 있어도 안전하다.
3. **공유 가변 상태 자체를 줄인다** — 채널로 우회한다. *single-writer + 메시지로 변경 의도 전달*이라는 actor 패턴이 자연스러워진다.

JVM 출신은 이 함정을 처음 만나면 *왜 이런 일이 일어나지?*가 막막할 수 있다. JVM의 락은 *OS 스레드 단위*다. 그래서 *같은 OS 스레드가 같은 락을 두 번 잡으려는 일*이 흔치 않다(reentrant lock이라 가능하긴 하지만 의미가 다르다). Rust async에서는 *한 OS 스레드 위에 수천 개 task*가 얹혀 있다. Mutex가 *task 단위가 아니라 OS 스레드 단위*로 동작한다는 사실 하나가 함정의 뿌리다. 모델을 잡으면 처방은 자연스럽다.

## spawn_blocking — 블로킹 호출은 격리한다

또 하나 흔한 함정이다. async 함수 안에서 *오래 걸리는 동기 작업*을 직접 호출하면 안 된다. 예를 들어 큰 JSON 파싱, 무거운 암호화, 또는 *옛 API 호출*(예: 동기 JDBC, 동기 파일 I/O).

```rust
async fn buggy() {
    let data = std::fs::read("big.txt").unwrap(); // 블로킹!
    process(&data);
}
```

이 한 줄이 워커 스레드를 점유하는 동안 *그 워커에 얹힌 다른 모든 task가 멈춘다*. 처방은 `tokio::task::spawn_blocking`이다.

```rust
async fn fixed() -> std::io::Result<()> {
    let data = tokio::task::spawn_blocking(|| std::fs::read("big.txt"))
        .await
        .unwrap()?;
    process(&data);
    Ok(())
}
```

`spawn_blocking`은 작업을 *별도의 blocking 스레드 풀*로 보낸다. tokio가 기본으로 가지고 있는 풀이 따로 있다. 결과는 `JoinHandle`로 돌아온다. JVM에서 reactive 코드 안에 동기 호출이 끼면 *Schedulers.boundedElastic()*으로 옮기던 일과 거의 같다.

또 하나의 함정. **`block_on`을 async 함수 안에서 호출하지 말 것.** 즉 `#[tokio::main]` 안에서 다시 `Runtime::new().block_on(...)`을 부르거나, async 함수 안에서 `block_in_place`도 없이 `block_on`을 부르면 *런타임 내부에서 panic이 난다*. tokio는 *현재 task가 어디 위에 얹혀 있는지*를 알기에 이런 호출을 명시적으로 거부한다. 동기 코드와 async 코드를 섞을 때는 항상 *경계*를 의식하자 — `block_on`은 *맨 바깥*에서만, `spawn_blocking`은 *안으로* 들어가는 다리다.

## 함수 색깔(Function Coloring) — 코루틴과의 가장 큰 철학 차이

여기까지 따라온 사람이라면 한 가지 질문이 떠올랐을 것이다. *`async fn`이 그저 `Future`를 반환하는 함수라면, 그냥 일반 함수처럼 부르면 안 되나? 왜 호출하는 쪽도 async fn이 되어야 하지?*

이게 바로 **function coloring** 문제다. Bob Nystrom이 2015년에 쓴 글 *"What Color is Your Function?"*에서 처음 통용된 말이다. 핵심은 이렇다 — *언어 차원에서 함수가 두 색깔(빨강 sync / 파랑 async)로 나뉘어 있고, 빨강이 파랑을 호출할 수 없다*는 비대칭. 한 번 async가 되면 *호출 체인 위쪽이 모두 async가 되는* 전염이 일어난다.

Rust는 *명백히 colored 언어*다. `async fn` 안에서만 `.await`를 쓸 수 있고, sync 함수는 async 함수를 *그냥은* 부를 수 없다. `block_on`이라는 다리가 있긴 하지만, 그 다리는 *runtime 위에서 한 번만, 맨 바깥에서만* 안전하다.

비교하자면 Kotlin Coroutine은 *언어 차원에서 두 색깔이고 라이브러리가 다리를 놔준* 구조다. `suspend fun`이 빨강이고 일반 fun이 파랑인데, `runBlocking`/`launch`/`async`로 다리가 잘 놓여 있다. Java 21 Virtual Thread는 *색깔 자체를 없애려는 시도*다 — 모든 함수가 그저 함수고, 블로킹 호출도 lightweight thread 위에서 *그냥 블로킹처럼 보이지만 실제로는 양보한다*. 이 둘 사이의 trade-off가 바로 코루틴/virtual thread/Rust async의 *큰 갈래*다.

Rust의 입장은 정직하다. *function coloring은 비용이지만, 그 대가로 zero-cost와 정적 안전성을 얻는다*. async fn이 만든 상태 머신은 *컴파일 타임에 펼쳐진다*. heap allocation이 최소화되고, 런타임 디스패치가 없다. Send/Sync 마커가 *컴파일러의 거부*로 동시성 안전을 보증한다. Virtual Thread는 그 대가로 *같은 함수가 가벼운 스레드와 무거운 스레드 양쪽에서 동작*하는 dynamic dispatch를 받아들인다 — 안전성과 효율 모두에서 trade-off가 있다.

이 철학 차이를 한 단락으로 정리하자. **Kotlin coroutine은 *runtime이 표준 라이브러리에 묶여 있고* `suspend`가 함수 색깔이 *라이브러리 컨벤션*인 반면, Rust는 *runtime을 프로젝트가 직접 고르고* `async`/`await`가 *컴파일러가 만든 상태 머신*이다.** 그래서 Rust async가 더 명시적이고, 함정의 자리도 다르다. *명시성과 zero-cost가 보상이고, function coloring과 runtime 분열이 대가다*.

비판적 시각도 있다는 사실을 함께 적어두자. *"Async Rust Is A Bad Language"*라는 글이 있고, *"Pin and suffering"* 같은 시리즈가 *Pin·Send 경계·async-trait의 dyn 미지원*을 지적한다. Rust async는 *별도의 sub-language가 됐다*는 신랄한 평이다. 맞는 부분도 있다. 그래서 우리가 *언제 async를 써야 하는가*도 중요하다 — *I/O 멀티플렉싱이 핵심이 아니라면 동기 코드도 충분히 빠르다*. 일이 *수만 개 connection*이 아니라 *수십 개 thread*로 끝나는 영역이라면, std::thread + rayon으로도 충분할 때가 많다. 도구를 *과하게* 쓰지 말자.

## async fn in trait — 1.75 stabilize와 그 후

JVM 출신이 거의 자동으로 짜는 패턴 중 하나가 *인터페이스에 async 메서드를 두는* 것이다. Kotlin에서는 너무도 자연스럽다.

```kotlin
interface UserRepository {
    suspend fun findById(id: Long): User?
}
```

Rust에서 같은 일을 하려면 어떻게 적을까?

```rust
trait UserRepository {
    async fn find_by_id(&self, id: i64) -> Option<User>;
}
```

Rust 1.75(2023-12)에서 *이 문법이 stabilize됐다*. 그 전까지는 `async-trait` crate를 써서 우회해야 했다. 그런데 한 가지 함정이 남아있다. *`dyn UserRepository`로 받으려 하면 컴파일이 안 된다*. dyn-safety가 아직 미해결이기 때문이다. async fn in trait이 반환하는 future의 타입이 *컴파일러가 만들어준 익명 타입*이라 vtable에 못 들어간다.

처방은 두 가지다.

1. **제네릭으로 받는다 (정적 디스패치)** — 서비스 코드에서는 이쪽이 자연스럽다.
   ```rust
   async fn handle<R: UserRepository>(repo: R, id: i64) { ... }
   ```
2. **`async-trait` crate를 쓴다 (동적 디스패치 필요할 때)** — `Box<dyn UserRepository>`가 필요하면 여전히 이 crate가 답이다. 비용은 *반환값이 `Box<dyn Future<...>>`로 할당*된다는 것.
   ```rust
   #[async_trait::async_trait]
   trait UserRepository { ... }
   ```

JVM에서는 *모든 인터페이스 메서드가 dyn-safe(virtual method)*가 디폴트다. Rust에서는 *어디서 동적 디스패치를 받아들일지*를 우리가 골라야 한다. 11장 axum의 핸들러도 이 결정을 곳곳에서 만난다.

## JVM 4종 비교 — 한 페이지 정리

이 자리에서 한 페이지로 묶어두자. 같은 일(*외부 API 10곳을 동시 호출해 합산*)을 다섯 가지 방식으로 짜면 어떻게 다른지 한 줄씩 비교하면 이렇다.

| 모델 | 핵심 도구 | 장점 | 단점 |
|---|---|---|---|
| Spring WebFlux (Reactor) | `Mono`/`Flux`, `zip`, `flatMap` | backpressure, reactive ecosystem | callback chain, 스택 트레이스 난해, 학습 곡선 |
| Kotlin Coroutine | `suspend`, `async/await`, structured concurrency | sequential 스타일, 구조화된 cancellation | runtime이 KotlinX 묶음, JVM에 종속 |
| Java CompletableFuture | `supplyAsync`, `thenApply`, `allOf` | 표준 라이브러리, 익숙함 | 체이닝 위주, cancellation 약함 |
| Java 21 Virtual Thread | 그냥 Thread + 블로킹 호출 | 색깔 없음, 익숙한 패러다임 | 성숙도 진행 중, 일부 native 코드 호환 이슈 |
| Rust async (tokio) | `async fn`, `.await`, `tokio::join!` | zero-cost, 정적 안전성, 가장 빠름 | function coloring, Pin/Send 부담, runtime 분열 |

한 줄 결론: **사용 감각은 Kotlin coroutine과 가장 비슷하고, 비용 모델은 Virtual Thread보다 더 명시적이며, 디버깅 가능성은 WebFlux보다 단순하다.** 우리 손이 어느 모양에 가장 익숙한지가 어디서 출발할지를 알려준다. JVM에서 Coroutine을 깊게 써본 사람이라면 Rust async에서 가장 적게 헤맨다.

## runtime 분열 — tokio가 표준이지만

10장의 마지막 한 절이다. 위에서 잠깐 짚었듯, Rust async는 *runtime이 표준 라이브러리에 없다*. tokio가 사실상 표준이긴 하다 — 20,768개 crate가 의존한다. 그런데 표준이 *하나뿐*이라는 사실이 또 다른 부담을 만든다.

- `async-std`는 2025년 *공식 sunset*됐다. 후속은 `smol`이다.
- `smol`은 "tokio 안에서도 돌아가는 작은 빌딩 블록"으로 부상 중이다. crate 작성자에겐 smol이 더 안전한 default라는 의견도 있다.
- crate를 만들 때 *어떤 runtime에 묶일지*를 결정해야 한다. tokio에 묶이면 다른 runtime에서 못 쓴다("executor coupling").

실무 권고는 단순하다. **애플리케이션 코드는 tokio를 그냥 쓰자.** 90% 이상의 ecosystem이 tokio다. *crate 작성자*가 아니라면 이 결정에 시간을 많이 쓸 필요가 없다. crate 작성자라면 `agnostic`/`pollster` 같은 runtime-agnostic 도구나 smol 기반을 검토하는 편이 낫다.

## 함께 해보자

tokio로 *10개의 외부 HTTP 호출을 동시에 보내고 결과를 모아 합산하는* 작은 함수를 짜보자. `reqwest` crate를 의존성에 추가하고, `tokio::join!` 또는 `futures::future::join_all`로 모아보자.

같은 일을 Java `CompletableFuture`로 짠다면 코드가 어떤 모양일까, Kotlin `coroutineScope { ... async { ... } }`라면 어떤 모양일까를 한 단락씩 머릿속에 비교해보자. *어느 쪽이 더 짧은가, 어느 쪽이 더 명시적인가, 디버깅이 어느 쪽이 쉬울까*.

그다음 함정 한 컷을 의도적으로 짜보자. `await`를 가로지르는 `std::sync::Mutex` 가드를 한 자리 넣고, `cargo clippy`가 무엇을 경고하는지 확인하자. 그 경고를 세 가지 처방(가드 범위 좁히기 / `tokio::sync::Mutex`로 바꾸기 / 채널로 우회하기) 중 둘로 고쳐보고, 비용이 어떻게 다른지 한 단락으로 적어보자. *(이 동시 호출 패턴은 11장 axum 핸들러 안의 외부 API 호출에서 다시 호출되고, Mutex/await 함정은 16장 운영 사고 회고에서 한 번 더 만난다. 그리고 `JoinHandle` 패턴은 12장 sqlx 트랜잭션의 `pool.acquire()`에서 비슷한 모양으로 재등장한다.)*

## 마무리

10장의 한 줄을 다시 박자. **async는 마법이 아니다 — `Future`는 상태 머신이고, `.await`는 그 상태 머신의 일시 정지점일 뿐이다.** 이 한 줄이 머리에 박혀 있으면, `Pin`도 `Send` 경계도 *상태 머신을 다루는 조연*으로 자리잡는다. tokio는 그 상태 머신을 *수만 개* 동시에 굴리는 work-stealing 스케줄러이고, `tokio::sync::*`는 같은 모델 위에서 짜인 채널·동기화 도구다.

Function coloring은 비용이다. 부정하지 말자. *async를 한 번 쓰면 호출 체인이 전염된다*. 대신 zero-cost와 정적 안전성을 얻었다 — 이 trade-off를 우리가 *받아들여야* 한다. Kotlin coroutine과 Java Virtual Thread가 다른 길을 갔다는 사실도 함께 기억하자. *어느 길이 옳은가*는 답이 없는 질문이고, 우리가 *어느 길의 보상을 더 원하는가*가 진짜 질문이다.

다음 11장에서는 *axum*으로 첫 HTTP 서비스를 띄운다. 여기서 본 `tokio::spawn`, `Send + 'static`, `Arc<Mutex<T>>`가 *모두* 그 자리에서 다시 호명된다. 그리고 *DI 컨테이너 없이* Spring Controller가 어떻게 보이는지 — 핸들러는 그저 async 함수일 뿐인데도 — 손에 묻혀보자. *Spring Controller가 Rust로 보이는 순간*이 그 챕터다.

## 참고

- *Why async Rust? — without.boats*. https://without.boats/blog/why-async-rust/
- *Catching up with async Rust — fasterthanlime*. https://fasterthanli.me/articles/catching-up-with-async-rust
- *Surviving Rust async interfaces — fasterthanlime*. https://fasterthanli.me/articles/surviving-rust-async-interfaces
- *Making the Tokio scheduler 10x faster*. https://tokio.rs/blog/2019-10-scheduler
- *async fn and return-position impl Trait in traits — Rust Blog (2023-12)*. https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/
- *Async Rust Is A Bad Language — Bit Bashing*. https://bitbashing.io/async-rust.html
- *Goodbye Async-Std, Welcome Smol — Rust Bytes*. https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol
- 토픽 5(reference.md §132–163): Send/Sync, async/await, tokio, channel, Mutex.
- 함정 2(reference.md §400–404): JoinHandle 누락, Mutex/await 데드락, blocking 호출.
- 논쟁점 3.2(reference.md §313–319): tokio vs async-std vs smol, function coloring 비판.
