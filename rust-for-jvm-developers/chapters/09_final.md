# 9장. 동시성 기초 — 스레드, channel, Mutex, 그리고 `Send`/`Sync`

월요일 아침 결제 API에 부하가 몰린다고 해보자. 트래픽이 두 배로 뛴 순간 응답이 느려지고, 한참 뒤 로그를 들춰보니 `ConcurrentModificationException`이 한 줄, 그리고 의심 가는 카운터의 값이 *이상하게* 작다. 누군가 동시 접근을 막지 않았다. `synchronized`를 빼먹었거나, `AtomicInteger`로 바꾼다는 걸 깜빡했거나. 코드 어디인지 *런타임이 한참 지나서야* 드러난다. 이런 사고를 한 번이라도 겪어본 사람이라면 다음 질문이 자연스럽게 떠오른다. *왜 컴파일러는 이걸 못 잡아주지?*

자바 진영의 답은 늘 비슷했다. `@ThreadSafe`라는 어노테이션이 있긴 하다. 그런데 그게 *문서일 뿐* 강제력이 없다. `@GuardedBy("this")`도 마찬가지다. FindBugs/SpotBugs가 *힌트로* 잡아주긴 하지만, 어기는 코드를 *빌드가 거부*하지는 않는다. 결국 우리는 *관행과 코드 리뷰*에 데이터 안전성을 맡겨왔다.

Rust가 이 지점에서 다른 길을 간다. 같은 카운터, 같은 멀티스레드, 같은 의도다. 하지만 *컴파일러가* `synchronized`를 빼먹은 코드를 거부한다. 9장의 전부가 이 한 줄이다. **JVM의 `synchronized`는 잊어도 된다 — 왜냐하면 컴파일러가 그 자리에 들어와 있기 때문이다.** 이 문장이 과장처럼 들린다면, 5장에서 심어둔 *빌림의 두 줄 규칙*이 어떻게 *멀티스레드 안전성*으로 자라나는지를 함께 따라가 보자.

## std::thread::spawn — `Thread`/`ExecutorService`의 첫 인사

먼저 가장 단순한 모양부터 손에 묻혀보자. JVM에서 `new Thread(() -> { ... }).start()` 하던 일을 Rust는 이렇게 적는다.

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        println!("새 스레드에서 한마디");
    });
    handle.join().unwrap();
    println!("메인 스레드도 끝.");
}
```

`thread::spawn`이 받는 건 `FnOnce + Send + 'static` 클로저다. 이 세 단어가 결국 9장의 모든 함정과 보상을 미리 박아둔다는 사실을 한번 짚어두자. `Send`는 이 챕터의 후반부에서 본격적으로 다룰 마커이고, `'static`은 6장에서 만난 *그 long-lived 라이프타임*이다. JVM에서 `Runnable`을 `Thread` 생성자에 넘길 때는 라이프타임 따위를 신경 쓸 필요가 없었다 — GC가 알아서 잡아주니까. Rust는 *컴파일러에게 한 번 일러두자*. "이 클로저 안에서 빌리는 모든 값은 새 스레드보다 오래 산다."

실제로 이런 코드를 짜보자.

```rust
let s = String::from("hello");
let handle = thread::spawn(|| {
    println!("{s}");
});
```

이게 바로 컴파일러가 거부하는 코드다. `s`를 빌리려 했는데, 메인 스레드에서 `s`가 *언제 drop될지*를 컴파일러가 보증할 수 없다. 그래서 에러 메시지가 친절하게 일러준다. *"closure may outlive the current function, but it borrows `s`"*. 처방은 두 가지다. 하나, `move` 키워드로 ownership을 새 스레드에 넘긴다.

```rust
let s = String::from("hello");
let handle = thread::spawn(move || {
    println!("{s}");
});
handle.join().unwrap();
```

이제 컴파일이 통과한다. 둘, 정말로 빌리고 싶다면 `Arc`로 감싸야 한다 — 이 얘기는 잠시 뒤에 본격적으로 한다.

JVM에서 `ExecutorService`로 풀(pool)을 만들어 작업을 던지던 패턴은 Rust에서는 *런타임을 직접 들이는* 모양이 된다. `std::thread`만으로도 풀을 짤 수 있지만, 실무에서는 `rayon`(데이터 병렬)이나 `tokio`(async, 10장)를 쓰는 편이 낫다. 9장은 그 토대를 깔아둘 뿐이다.

## std::sync::mpsc — `BlockingQueue`의 감각

스레드 사이에 데이터를 주고받자. JVM에서는 `BlockingQueue<T>`(또는 Kotlin의 `Channel<T>`)로 producer-consumer를 짜던 일이다. Rust 표준 라이브러리에는 `std::sync::mpsc`가 있다. mpsc는 *multi-producer, single-consumer*의 약자다.

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    for i in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(format!("작업 {i} 완료")).unwrap();
        });
    }
    drop(tx); // 모든 송신자가 닫혀야 rx의 iter가 종료된다.

    for msg in rx {
        println!("받음: {msg}");
    }
}
```

`tx.clone()`이 producer를 늘리는 자연스러운 표현이다. JVM의 `BlockingQueue`는 producer/consumer 구분이 없는 한 객체였다는 점과 비교해보자. Rust는 *송신*과 *수신*을 타입으로 분리한다 — 누가 보내고 누가 받는지가 코드에 드러난다는 사실 자체가 동시성 코드의 가독성을 한 단계 끌어올려 준다.

여기서 한 가지 혼동하기 쉬운 부분을 미리 짚자. `std::sync::mpsc`는 *동기 채널*이다. 10장에서 만나게 될 `tokio::sync::mpsc`(async 채널)와 이름은 같지만 다른 도구다. async 함수 안에서는 std mpsc를 쓰지 *말아야 한다* — 블로킹이 일어나면 같은 스레드의 다른 task가 멈춘다. 이 함정은 10장에서 본격적으로 다시 만난다.

다양한 모양이 필요하면 `crossbeam::channel`을 쓰는 편이 낫다. select, bounded 채널, deadline 등 std mpsc가 안 가진 기능을 다 갖췄다. JVM 출신에게는 LMAX Disruptor의 감각이 가장 가깝다.

## Arc<Mutex<T>> — 공유 가변 상태의 표준 표현형

이제 5장의 카운터를 다시 꺼내자. 5장에서 우리는 *한 시점에 mutable borrow는 하나만*이라는 두 줄의 규칙을 배웠다. 그 규칙이 *멀티스레드*로 옮겨오면 어떤 모양이 될까?

먼저 의도적으로 잘못된 코드를 짜보자.

```rust
use std::thread;

fn main() {
    let mut counter = 0i64;
    let mut handles = vec![];

    for _ in 0..100 {
        let handle = thread::spawn(|| {
            counter += 1; // 컴파일 에러!
        });
        handles.push(handle);
    }
    for h in handles { h.join().unwrap(); }
    println!("{counter}");
}
```

컴파일러가 곧장 거부한다. *"closure may outlive the current function"* — 5장에서 본 그 메시지의 멀티스레드 버전이다. 더 구체적으로는 *"cannot borrow `counter` as mutable, as it is a captured variable in a `Fn` closure"*. 100개 클로저가 동시에 같은 카운터를 mutable borrow하겠다는 건 *두 줄 규칙*의 정면 위반이다. JVM이라면 이 코드가 *컴파일은 통과하고* 런타임에 카운터가 90 언저리로 끝나서 *우리가 한참 뒤에 발견*했을 코드다. Rust는 *빌드가 거부*한다. 이 차이가 9장 전체의 한 문장이라는 점을 잊지 말자.

처방은 `Arc<Mutex<T>>` 패턴이다. 8장의 스마트 포인터 표를 다시 펼쳐보자. `Arc<T>`는 *멀티스레드 공유 owner*, `Mutex<T>`는 *동기화된 가변 접근*. 이 둘을 합치면 *공유 가변 상태의 표준 표현형*이 된다.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0i64));
    let mut handles = vec![];

    for _ in 0..100 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut guard = counter.lock().unwrap();
            *guard += 1;
        });
        handles.push(handle);
    }
    for h in handles { h.join().unwrap(); }

    println!("{}", *counter.lock().unwrap());
}
```

100개 스레드가 같은 카운터를 안전하게 +1 한다. 결과는 정확히 100이다 — *언제나 100이다*. JVM에서 `synchronized` 블록을 빼먹어 88, 92, 95로 흔들리던 그 사고가 *코드 모양으로 불가능해진* 셈이다.

여기서 두 가지를 자세히 보자. 첫째, `Arc::clone(&counter)`는 *데이터를 복제*하지 않는다 — 참조 카운트를 +1할 뿐이다. 100개 스레드가 같은 `Mutex<i64>`를 공유한다. 둘째, `counter.lock().unwrap()`이 반환하는 `MutexGuard`는 *RAII로 풀린다*. 즉 스코프를 벗어나는 순간 자동으로 unlock된다. JVM의 `synchronized` 블록은 닫는 중괄호에서 풀리지만, `ReentrantLock.lock()` 다음에 `try { ... } finally { lock.unlock(); }`을 빠뜨려 *영원히 잠긴 락*을 만든 사고는 한 번쯤 본 적이 있을 것이다. Rust에서는 *그 사고가 구조적으로 불가능하다*. lock guard를 들고 있다가 panic이 나도 스택 unwinding 과정에서 자동으로 풀린다.

`Mutex` 외에 `RwLock<T>`도 있다. 다수 reader / 단일 writer가 필요하다면 `Arc<RwLock<T>>`. JVM의 `ReentrantReadWriteLock`과 같은 발상이다. 그리고 카운터처럼 단순한 정수 연산이라면 `std::sync::atomic::AtomicI64`를 쓰는 편이 더 가볍다 — `AtomicReference`, `AtomicLong`의 Rust 대응물이다.

## 그런데 왜 `Mutex`가 아니라 `Arc<Mutex<T>>`인가

JVM 출신이 자주 묻는 질문이다. Java라면 그냥 `Mutex<T>` 같은 객체 하나를 만들어 모든 스레드가 같은 참조를 들면 끝 아닌가? 왜 한 단계 더 감싸야 하지?

답은 4장의 소유권에 있다. `Mutex<T>`는 *그 자체로 owner*다. 누군가 한 명만 가진다. 100개 스레드가 같은 mutex를 *나눠 가지려면* 누군가 owner를 *공유 가능한 형태*로 만들어줘야 한다. 그게 바로 `Arc<T>`의 일이다. JVM은 *모든 객체 참조가 늘 공유 가능*하기 때문에 이 단계가 보이지 않았을 뿐이다.

그래서 Rust 코드에서 `Arc<Mutex<T>>`라는 표현형을 만나면 두 부분을 분리해서 읽자. `Arc`는 *공유*, `Mutex`는 *동기화된 가변*. 이 두 책임이 *분리된 타입으로 코드에 박혀 있다*는 사실이 처음엔 번거롭게 느껴지지만, 6개월 뒤에는 *읽는 순간 의미가 잡히는* 안도감이 된다.

## Send / Sync — 컴파일러가 채워주는 마커 트레잇

이제 9장의 핵심으로 들어가자. *Rust는 어떻게 data race를 컴파일 타임에 차단하는가?* 답이 `Send`와 `Sync`라는 두 마커 트레잇이다.

먼저 정의를 짚고 가자.

- **`Send`** — "이 타입의 값은 ownership을 다른 스레드로 *이동*시켜도 안전하다."
- **`Sync`** — "이 타입의 값을 여러 스레드에서 *동시에 참조*해도 안전하다(`&T`로)."

이름이 직관적이지 않아 처음에는 헷갈린다. 이렇게 외워두자. *Send는 보내는 것, Sync는 함께 보는 것*. 그리고 둘 다 *마커 트레잇*이다 — 메서드가 없다. 그저 *"이 타입이 멀티스레드에 안전하다"*는 정보를 타입 시스템에 박아두는 라벨일 뿐이다.

여기서 한숨 돌리자. **Send/Sync는 우리가 늘 적는 트레잇이 아니다.** 컴파일러가 *자동으로* 채워준다. 어떤 구조체의 모든 필드가 Send면 그 구조체도 Send. 모든 필드가 Sync면 그 구조체도 Sync. 우리가 새 타입을 만들 때 *대부분의 경우* `impl Send for ...`나 `impl Sync for ...`를 직접 적을 일이 없다. 8장에서 만난 거의 모든 타입(`i32`, `String`, `Vec<T>`, `Box<T>`, `Arc<T>`, `Mutex<T>`)이 자동으로 둘 다 구현한다.

그렇다면 *언제* Send/Sync가 *없는* 타입을 만나는가? 두 자리만 기억해두면 된다.

첫째, **`Rc<T>`는 Send도 Sync도 아니다.** 8장에서 본 `Rc<T>`는 *단일 스레드 reference counting*이다. 참조 카운트 변경이 atomic하지 않기 때문에 멀티스레드에서 race condition이 일어난다. 그래서 Rust 표준 라이브러리는 *아예 Send/Sync를 구현하지 않는다*. 8장의 트리 예제에 썼던 `Rc<RefCell<Node>>`를 한번 멀티스레드로 옮겨보자.

```rust
use std::rc::Rc;
use std::cell::RefCell;
use std::thread;

fn main() {
    let shared = Rc::new(RefCell::new(0));
    let s = Rc::clone(&shared);
    thread::spawn(move || {        // 컴파일 에러!
        *s.borrow_mut() += 1;
    });
}
```

에러 메시지가 곧장 나온다. *"`Rc<RefCell<i32>>` cannot be sent between threads safely"*. `Rc<T>`가 Send가 아니기 때문이다. 처방은 명확하다. 멀티스레드라면 `Arc<T>`로 옮긴다. 그리고 `RefCell`도 Sync가 아니므로 안쪽도 `Mutex`로 바꿔야 한다. 결과적으로 `Arc<Mutex<i32>>` — 위에서 본 그 표준 표현형이다. 컴파일러가 한 줄 한 줄 *어디를 바꿔야 하는지*를 일러준다.

둘째, **`*const T`와 `*mut T`(raw pointer)는 Send도 Sync도 아니다.** 8장의 unsafe 절에서 만난 그 raw pointer다. 멀티스레드 안전성을 컴파일러가 보장할 수 없으니 *기본은 거부*한다. 정말로 멀티스레드에 들이려면 우리가 *unsafe로 보증*하면서 `unsafe impl Send for MyType {}`를 적어준다. 표준 라이브러리의 거의 모든 자료구조 내부에 이 패턴이 깔려 있다.

이 자동 채움 메커니즘이 갖는 의미를 한 번 더 짚자. JVM에서 우리는 *어떤 객체가 thread-safe인지*를 *문서를 읽어* 알아내야 했다. `HashMap`은 thread-safe가 아니고 `ConcurrentHashMap`은 thread-safe다. 그런데 *어기는 코드를 컴파일러가 거부하는가?* 아니다. `HashMap`을 멀티스레드에서 쓰는 코드도 *빌드는 통과하고* 런타임에 데이터가 깨질 뿐이다. Rust는 그 일을 *타입 시스템에 박아둔다*. 함수 시그니처가 `T: Send + 'static`을 요구하면 컴파일러가 거부하고, 우리가 잘못된 타입을 넣으면 *빌드가 멈춘다*. **JVM의 `@ThreadSafe`/`@GuardedBy`가 *문서이자 분석 도구의 힌트*였다면, Send/Sync는 *컴파일러의 거부*다.** 이 한 줄이 토픽 5의 모든 것이다.

## Lock guard의 RAII — "lock 안 풀고 return"이 구조적으로 불가능한 이유

위에서 잠깐 짚었던 부분을 한 번 더 손에 묻혀두자. JVM에서 가장 흔한 락 사고는 두 가지다. 하나, `lock.unlock()`을 빠뜨려 영원히 잠긴 락. 둘, 예외가 나서 `unlock`이 안 불리는 락. 그래서 Java 코드는 항상 이렇게 적도록 권장된다.

```java
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}
```

또는 `synchronized` 블록을 쓰는 편이 낫다. 그럼 닫는 중괄호에서 자동으로 풀린다. 그런데 Java 24가 와도 *컴파일러는 `lock.lock()` 뒤에 `unlock()` 빼먹은 코드를 거부하지 않는다*. 우리가 *관행*으로 막아왔을 뿐이다.

Rust는 다르다. `Mutex<T>::lock()`이 반환하는 건 단순한 boolean이 아니라 `LockResult<MutexGuard<'_, T>>`다. `MutexGuard`는 4장의 `Drop` 트레잇을 구현한 RAII 가드다. 이 가드가 *스코프를 벗어나는 순간* 자동으로 unlock된다. 우리는 그저 가드의 데이터에 접근만 하면 된다.

```rust
fn increment(counter: &Mutex<i64>) {
    let mut guard = counter.lock().unwrap();
    *guard += 1;
} // 여기서 guard가 drop되면서 자동 unlock.
```

panic이 나도 스택 unwinding이 `Drop`을 호출한다 — 락이 풀린다(엄밀히는 *poisoned* 상태가 되어 다음 lock 호출이 에러를 반환하는데, 이 자체가 *데이터가 손상됐을 수 있다*는 신호다). JVM의 `try-finally`가 *관행으로* 보장하던 일이 *타입 시스템의 결과로* 따라온다. 4장에서 만난 `Drop`이 멀티스레드에서 *어떻게 보상받는지*가 바로 이 자리에서 드러난다.

## Send 위반 한 컷 더 — `MutexGuard`는 Send지만 Sync는 아니다

조금 깊은 이야기 하나만 짚고 가자. 처음 봤을 때 *왜?* 싶은 사실이다. `Mutex<T>::lock()`이 반환하는 `MutexGuard<'_, T>`는 Send도 Sync도 양쪽 다일 것 같지만, 사실 `Sync`가 아니다(엄밀히는 T가 Sync일 때만 Send이고, 본인은 Sync 제약이 다르다). 더 중요한 함정은 *async 코드에서* 이 가드를 await 지점을 가로질러 들고 있으면 데드락이 난다는 점이다. 이 부분은 10장에서 본격적으로 다룬다.

핵심은 이렇다. **표준 라이브러리의 동시성 도구들은 자기가 어디까지 안전한지를 *타입의 trait 구현으로* 표현한다.** 우리가 잘못된 자리에 가져다 놓으면 컴파일러가 `Send` 또는 `Sync` 제약 위반을 들먹이며 거부한다. *어디가 문제인지를 문장으로* 일러준다. 이 대화의 패턴에 익숙해지면, 첫 한 달의 *막막함*이 *컴파일러와의 짧은 대화*로 바뀌어 간다.

## 데드락은 안 막아준다 — Rust의 솔직한 한계

여기서 한 번 솔직해지자. 9장의 모든 자랑에도 불구하고, **Rust도 데드락은 안 막는다**. 두 개의 mutex를 서로 다른 순서로 잠그는 코드를 짜면 *런타임에* 데드락이 난다. Java/Kotlin과 똑같다. 컴파일러는 *데이터 race*를 막을 뿐, *락 ordering*까지 추적해주지는 않는다.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let a = Arc::new(Mutex::new(0));
let b = Arc::new(Mutex::new(0));

let (a1, b1) = (Arc::clone(&a), Arc::clone(&b));
thread::spawn(move || {
    let _g1 = a1.lock().unwrap();
    let _g2 = b1.lock().unwrap(); // 운 나쁘면 여기서 멈춤.
});

let _g1 = b.lock().unwrap();
let _g2 = a.lock().unwrap(); // 운 나쁘면 여기서 멈춤.
```

이 코드는 컴파일이 잘 통과한다. 그리고 운이 나쁘면 *영원히 멈춘다*. 처방은 JVM 출신이 이미 알고 있는 그것이다. *락 순서를 항상 같게 유지한다, 한 번에 하나의 락만 잡는다, 가능하면 lock-free 자료구조나 채널 기반 설계로 옮긴다*. Rust가 컴파일러로 막아주지 못하는 영역이 어디까지인지를 정확히 알아두는 것이 *바이블*의 정직한 자세다.

`parking_lot` crate는 표준 `Mutex`보다 빠르고 poisoning이 없으며 deadlock detection 기능을 옵션으로 제공한다. 큰 서비스에서는 한번 들여다볼 만하다. 그리고 `tokio-console`(14장)이 async 환경에서 데드락 후보를 시각화해준다 — 이 얘기는 10장에서 다시 만난다.

## Send/Sync가 잡지 못하는 사각지대 정리

한 번에 정리해두자. Rust 컴파일러가 동시성에 대해 *잡아주는 일*과 *못 잡는 일*은 이렇게 갈린다.

| 항목 | 컴파일러가 잡는가? |
|---|---|
| Data race (한 자리를 동시에 read/write) | 잡는다 |
| 다른 스레드로 보낼 수 없는 타입 전달 | 잡는다 |
| Lock unlock 누락 | 잡는다 (RAII) |
| 락 ordering 위반으로 인한 데드락 | *못 잡는다* |
| Atomic 연산의 memory ordering 오용 | *못 잡는다* (런타임 검증 도구 필요) |
| Logical race (의미상의 경합) | *못 잡는다* |
| Async Mutex guard를 await 가로질러 들고 있기 | clippy가 경고는 한다 (10장) |

JVM의 어떤 도구도 첫 세 줄을 *컴파일 타임에* 잡지는 못한다. 그게 Rust가 9장에서 손에 쥐여주는 *진짜 보상*이다. 마지막 세 줄은 어느 언어든 여전히 우리의 사고를 요구한다 — 컴파일러가 모든 일을 해주지는 않는다는 *균형 감각*을 잃지 말자.

## 함께 해보자

100개 스레드가 동시에 카운터를 +1하는 코드를 짜보자. 첫 시도는 의도적으로 Mutex 없이 — 컴파일러가 무엇을 거부하는지 한 줄 한 줄 읽어보자. 그다음 `Arc<Mutex<i64>>`로 고쳐 통과시키고, 결과가 *언제나 정확히 100*인지 100번 돌려보자. 마지막으로 `Rc<Mutex<i64>>`로 바꿔서 컴파일러가 무엇을 *추가로* 거부하는지 확인하자(Send 트레잇 결여).

여유가 있다면 `std::sync::atomic::AtomicI64`로 같은 카운터를 짜보고, `Arc<Mutex<i64>>` 버전과 처리량을 비교해보자. 단순 정수 카운터라면 atomic이 더 가볍다는 사실을 손에 묻혀두자. *(이 `Arc<Mutex<T>>` 패턴은 11장 axum의 `State`에서 다시 호출되고, Send 위반은 10장 tokio `spawn`의 함정에서 한 번 더 만난다. 그리고 데드락 회고는 16장 운영 사고 회고에서 다시 다룬다.)*

## 마무리

9장의 한 줄을 다시 적어두자. **JVM의 `synchronized`는 잊어도 된다 — 그 자리에 컴파일러가 들어와 있다.** 5장에서 심은 빌림의 두 줄 규칙이 `Send`/`Sync`라는 마커를 통해 *멀티스레드 안전성*으로 자라났다. 우리가 직접 `impl Send for ...`를 적을 일은 거의 없다 — 컴파일러가 *알아서* 채워주는 마커이고, 그 자동 채움이 우리 일상의 동시성 코드를 *조용히 검증*한다. 그 사실이 안도감을 준다. *어떤 객체가 thread-safe인지를 문서로 외워야 했던 시절*이 끝난 것이다.

물론 데드락과 logical race는 여전히 우리의 사고를 요구한다. Rust는 *마법*이 아니다. 그러나 *압도적 다수의 동시성 사고*를 *빌드 타임에* 잡아준다는 사실 하나만으로도, 운영팀의 새벽 알림이 한 카테고리만큼 줄어든다.

다음 10장에서는 *async/await*로 넘어간다. 9장의 `std::thread`가 OS 스레드를 직접 다뤘다면, 10장은 *수만 개의 task를 한 줌의 스레드에* 얹는 모델이다. Spring WebFlux와 Kotlin Coroutine을 써본 출신이 가장 빠르게 적응할 영역이지만, *함수 색깔(function coloring)*이라는 코루틴과의 가장 큰 철학 차이가 한 절을 차지하게 된다. *async는 마법이 아니다 — `Future`는 상태 머신이고, `.await`는 일시 정지점일 뿐이다*는 한 줄을 미리 머리에 넣어두자.

## 참고

- *Send and Sync — The Rustonomicon*. https://doc.rust-lang.org/nomicon/send-and-sync.html
- *The Rust Programming Language — Fearless Concurrency*. (rust-lang 공식 책)
- *Tokio docs — Channels*. https://docs.rs/tokio/
- 토픽 5(reference.md §132–163): Send/Sync, async/await, tokio, channel, Mutex.
- 토픽 4(reference.md §104–130): 스마트 포인터 표(`Box`/`Rc`/`Arc`/`RefCell`/`Mutex`/`RwLock`).
