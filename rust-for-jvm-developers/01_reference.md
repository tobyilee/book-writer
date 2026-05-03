# Rust for JVM Developers — Reference Document

> 본 문서는 "JVM(Java/Kotlin/Spring) 출신 개발자를 위한 Rust 입문·활용서"의 집필 토대다. 12개 토픽을 가로지르며, 모든 설명은 "Java/Kotlin이라면 어떻게 표현했을까"를 함께 의식한다. 각 인용에는 원문 출처를 붙였고, 출처가 명확하지 않은 주장은 본문에서 배제했다. 작성 시점은 2026년 5월이며, 인용한 통계와 자료의 발행 시점은 가능한 한 함께 표기했다.

---

## 1. 개념·정의

### 1.1 Rust란 무엇인가

Rust는 "메모리 안전·동시성 안전을 컴파일 타임에 보장하는 시스템 프로그래밍 언어"다. C/C++급의 성능과 제어를 가지면서도 가비지 컬렉터(GC)가 없고, 런타임이 매우 얇다. 표준 라이브러리는 운영체제 위에서 정적 바이너리로 컴파일된다.

- 핵심 디자인 원칙은 세 가지다. (1) 메모리 안전성을 컴파일러가 강제한다 — null pointer dereference, use-after-free, double-free, data race를 빌드 단계에서 차단한다. (2) "Zero-cost abstraction" — 트레잇·제네릭·이터레이터 같은 추상화 비용이 런타임에 0에 수렴한다. (3) 명시성 — 메모리 소유, 가시성, 에러 가능성, 동시성 안전성을 모두 타입으로 표현한다.
- 2024 State of Rust Survey에 따르면 응답한 조직의 **45%가 Rust를 프로덕션에서 의미 있게 사용**한다(2023년 38%에서 7%p 상승). 백엔드/서버사이드는 그 중 가장 큰 도메인(51.7%)이다. ([2024 State of Rust Survey Results](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/), [Survey: Memory-Safe Rust Gains 45% of Enterprise Development](https://thenewstack.io/survey-memory-safe-rust-gains-45-of-enterprise-development/))
- 2024년 2월 미국 백악관 ONCD가 발표한 「Back to the Building Blocks: A Path Toward Secure and Measurable Software」에서 **메모리 안전 언어 전환을 권고하며 사실상 Rust를 유일한 사례로 명시**했다. ([Final-ONCD-Technical-Report.pdf](https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf), [Stack Overflow Blog 정리본](https://stackoverflow.blog/2024/12/30/in-rust-we-trust-white-house-office-urges-memory-safety/))

### 1.2 JVM 생태계와의 본질적 차이

| 축 | JVM (Java/Kotlin/Spring) | Rust |
|---|---|---|
| 메모리 관리 | GC가 런타임에 자동 회수 | 소유권(ownership)으로 컴파일 타임에 결정, scope 종료 시 즉시 Drop |
| 안전성 검증 시점 | 대부분 런타임(NPE, ConcurrentModificationException, ClassCastException…) | 대부분 컴파일 타임(borrow checker, 타입, Send/Sync) |
| 배포 산출물 | JAR/WAR + JVM(또는 GraalVM native-image) | 단일 정적 바이너리(또는 musl + scratch 컨테이너) |
| 시작 시간·메모리 | JIT warm-up·heap 예약(수백 MB~) | 시작 즉시 풀 성능, 보통 한 자릿수 MB |
| 동시성 모델 | 스레드·이벤트 루프 + Future/CompletableFuture, 코루틴, Virtual Thread | async/await + Send/Sync 마커, tokio 같은 runtime을 명시적으로 선택 |
| 의존성 관리 | Maven/Gradle, 트랜지티브 의존성 자동 해소 | Cargo + crates.io, semver + feature flag로 conditional compile |
| 프레임워크 문화 | Spring 같은 "all-included" DI 컨테이너가 표준 | "조립형" — axum + sqlx + tower + tracing처럼 작은 라이브러리를 손으로 합침 |

이 차이를 한 줄로 요약하면 "**JVM은 런타임에서 안전을 보장하고 Rust는 컴파일러가 안전을 강제한다**"이다. Rust 측 설명: "memory is automatically returned once the variable that owns it goes out of scope, providing deterministic resource management without requiring a garbage collector." ([Rust Memory Management Without Garbage Collection](https://dasroot.net/posts/2026/04/rust-memory-management-ownership-borrowing-lifetimes/))

JVM 백엔드 개발자가 Rust로 옮길 때 가장 먼저 실감하는 차이는 두 가지다. (1) 컴파일러가 잡아주는 양이 압도적으로 많아진다 — NPE·동시성 오류가 사실상 사라진다. (2) 그 대가로 컴파일러와의 "대화"가 잦아진다 — 처음 몇 주는 "borrow checker와의 싸움"이 일상이다. ([Rust's Learning Curve: Community Debates Borrow Checker and Lifetime Complexity](https://biggo.com/news/202502181925_rust-learning-curve-debate))

---

## 2. 12개 토픽별 핵심 내용

### 토픽 1 — Rust 언어 기본 (변수/타입/제어 흐름/함수/모듈)

- **변수의 기본은 불변(immutable)이다.** `let x = 5;`는 final이 디폴트인 Java/Kotlin의 `val`과 같다. 가변이 필요하면 `let mut x = 5;`. 이는 Spring 코드의 `@Value(...)` 주입처럼 "재할당하지 마"라는 시그널을 컴파일러가 강제한다.
- **타입 추론이 강하지만 함수 시그니처는 항상 명시한다.** Java처럼 `var`만으로 끝나지 않는다. 함수 경계는 곧 API 계약이라는 철학이 강하다.
- **모듈 시스템은 namespace + 가시성 제어**다. `mod`, `pub`, `pub(crate)`, `pub(super)` 같은 가시성이 자바의 `public`/`package-private`/`module-info.java`보다 더 세분화돼 있다. 패키지 단위는 "crate"라 부르고, 한 crate 안에서 모듈을 트리로 정의한다. ([Cargo Workspaces 공식 문서](https://doc.rust-lang.org/cargo/reference/workspaces.html))
- **JVM 대응물:** `let`/`let mut` ↔ `val`/`var`, `mod`/`pub` ↔ `package`/접근제어자, `enum` ↔ `enum`/sealed class(다만 Rust enum이 훨씬 강력, 토픽 2 참고).
- **주의점:** Java는 명시적 import가 많지만 Rust는 prelude로 가려진 기본 항목이 꽤 있다. `Option`, `Result`, `Vec`, `String`은 import 없이 쓸 수 있다.

### 토픽 2 — 핵심 개념 (소유권/빌림/라이프타임/트레잇/제네릭/패턴 매칭/매크로)

이 절은 책의 무게중심이다. JVM 출신이 가장 많이 부딪히고, 가장 많이 보상받는 영역이다.

#### 2.1 소유권(Ownership)

규칙은 단순하다. (1) 모든 값은 정확히 하나의 owner를 가진다. (2) owner가 scope를 벗어나면 값이 즉시 drop된다. (3) 값을 다른 변수에 대입하거나 함수에 넘기면 ownership이 **이동(move)** 한다 — 원래 변수는 더 이상 그 값을 쓸 수 없다. 단, `Copy` 트레잇이 있는 원시 타입(`i32`, `bool` 등)은 복사된다.

JVM 개발자에게는 "참조 변수 두 개로 같은 객체를 가리키는 게 기본"이었지만, Rust는 그것을 **명시적 borrow**로만 허용한다.

> "Like Java, Rust does not suffer from memory leaks, use-after-free bugs, dangling pointer bugs, or buffer overflows. However, Rust does not have the overhead of garbage collection or the associated runtime which has prevented languages like Java and C# from reaching the performance of C++ in 'object heavy' applications." — [Rust for Java Developers](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)

#### 2.2 빌림(Borrowing)

이동 대신 "빌려주기"가 가능하다. `&T`는 immutable borrow, `&mut T`는 mutable borrow다. 규칙은 두 줄이다.

1. 한 시점에 mutable borrow는 **단 하나만** 존재할 수 있다.
2. mutable borrow가 살아있는 동안 다른 어떤 borrow도 존재할 수 없다.

이 규칙이 컴파일 타임에 data race를 차단한다. Java의 `synchronized`나 Kotlin의 `Mutex`로 런타임에 잡던 문제를, Rust는 빌드 단계에서 못 박는다. ([Rust ownership and borrows - Fighting the borrow-checker](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3))

#### 2.3 라이프타임(Lifetime)

라이프타임 어노테이션 `'a`은 "이 참조가 살아있을 기간을 컴파일러에게 알려주는" 메타데이터다. 런타임에 영향이 없고, 오직 borrow checker가 "참조가 가리키는 데이터보다 참조가 더 오래 살지 않게" 검증하는 데 쓰인다. 대부분의 함수는 라이프타임 elision 규칙으로 `'a`를 생략할 수 있고, 진짜로 명시해야 하는 상황은 책 전체에서 손에 꼽는다. ([Rust Lifetimes: A Complete Guide](https://earthly.dev/blog/rust-lifetimes-ownership-burrowing/))

> "Concepts like slices from String differences and lifetime annotations ('a, 'static) are difficult to understand clearly." — 한국 개발자 후기, [4년간의 Rust 사용 후기](https://blog.cro.sh/posts/four-years-of-rust/)

#### 2.4 트레잇(Trait)

Rust 트레잇은 "Java 인터페이스와 비슷해 보이지만 실제론 더 가깝게는 Haskell의 typeclass + Scala의 implicit trait"이다.

- **트레잇은 인터페이스가 아니다.** 인터페이스는 "타입이 자기를 구현하겠다고 선언"한다. 트레잇은 "외부에서 어떤 타입에 대한 트레잇 구현을 추가"할 수 있다(orphan rule 안에서). 이는 Spring의 `@Component`/`@Service`가 만들어내는 의존성 그래프와 다른 발상이다. ([Rust Traits are not interfaces](https://www.jamessturtevant.com/posts/rust-traits-are-not-interfaces-and-a-little-on-lifetimes/))
- **정적 디스패치(generics) vs 동적 디스패치(dyn Trait)를 개발자가 명시적으로 선택**한다. 정적은 monomorphization으로 0-cost지만 바이너리가 커진다. `Box<dyn Trait>`은 vtable을 거쳐 한 단계 indirection이 생기지만 Java 인터페이스와 같은 유연성을 제공한다. ([Rust Static vs. Dynamic Dispatch — softwaremill](https://softwaremill.com/rust-static-vs-dynamic-dispatch/), [Trait Objects to Abstract over Shared Behavior](https://doc.rust-lang.org/book/ch18-02-trait-objects.html))

#### 2.5 제네릭

JVM의 generics는 type erasure다. Rust generics는 monomorphization — 컴파일 시점에 사용된 타입마다 코드를 생성한다. 그래서 generic이 더 빠르지만 컴파일 시간이 늘고 바이너리가 커진다.

#### 2.6 패턴 매칭

Rust enum은 "데이터를 갖는 enum"(algebraic data type)이고, `match`로 exhaustive한 분기를 강제한다. Java가 Java 17의 sealed class + switch pattern matching으로 따라가고 있지만 여전히 표현력 차이가 크다.

> "Java's deconstruction is a baby step and not as powerful as deconstruction in Rust. The Java sealed class and switch expression feature is moving Java closer to the pattern matching capabilities that Rust already has more fully developed." ([The state of pattern matching in Java 17](https://deepu.tech/state-of-pattern-matching-java/))

#### 2.7 매크로

`macro_rules!`(declarative)와 `proc_macro`(procedural) 두 종류다. Java의 annotation processor + Lombok이 하는 일을 Rust에서는 `#[derive(...)]`와 procedural macro가 담당한다. 단, Rust 매크로는 토큰/AST 레벨에서 실제로 코드를 펼치고 컴파일러가 다시 검사하므로, Lombok처럼 "마법처럼 메서드가 생기지만 IDE에서만 보이는" 식의 거리감이 적다. ([Procedural macros in Rust — LogRocket](https://blog.logrocket.com/procedural-macros-in-rust/), [Macros — The Rust Book](https://doc.rust-lang.org/book/ch19-06-macros.html))

### 토픽 3 — 에러 처리 (Result/Option, ?, panic, anyhow/thiserror)

Rust는 "에러는 값"이라는 철학이다. 예외(throw/catch)는 없다. 정상 흐름과 실패 흐름이 모두 타입에 드러난다.

- `Option<T>`: 값이 있을 수도 없을 수도 있는 경우. Java의 `Optional<T>`보다 더 엄격하게 — Rust에는 `null`이 없으므로 `Option`을 안 쓰면 "없을 수 있음" 자체를 표현할 길이 없다.
- `Result<T, E>`: 실패 가능한 연산. 패턴 매칭이나 `?` 연산자로 propagate한다. `?`는 "현재 함수가 `Result`/`Option`을 반환할 때 실패면 즉시 early return"하는 syntactic sugar로, Java의 `try/catch + throws`와 비교하면 의도가 훨씬 직관적이다. ([Rust Error Handling Guide 2025 — Markaicode](https://markaicode.com/rust-error-handling-2025-guide/))
- `panic!`: unrecoverable error. JVM의 `Error`(OOM 같은 류)에 가깝다. 라이브러리 코드에서는 거의 쓰지 않는다.
- **anyhow vs thiserror**: 애플리케이션 코드(서비스, 핸들러)에는 `anyhow::Error`로 묶어 컨텍스트만 입히고, 라이브러리에는 `thiserror`로 enum 기반 에러 타입을 정의한다. ([Rust Error Handling Compared: anyhow vs thiserror vs snafu — DEV.to](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003))

JVM 비교: Java의 checked exception은 "잘 만들어진 의도지만 실패한 실험"이라는 평이 일반적이다. Rust의 `Result`는 checked exception의 정신을 살리되, 시그니처에 끼워넣기 부담을 줄였다. Kotlin은 checked exception을 폐기하고 `runCatching`/`Result`로 비슷한 방향을 잡았는데, Rust는 그게 언어 차원에서 첫째 도구다.

### 토픽 4 — 메모리 모델·성능 (스택/힙, Box/Rc/Arc, Drop, 컴파일 타임 안전성)

#### 4.1 스택 vs 힙

기본은 스택. 힙으로 보내려면 명시적으로 `Box<T>`로 감싼다. Java는 객체가 항상 힙이지만 Rust는 작은 구조체는 그대로 스택에 두는 게 자연스럽다.

#### 4.2 스마트 포인터

| 도구 | 용도 | JVM 대응물 |
|---|---|---|
| `Box<T>` | 단일 owner, 힙 할당 | 일반 Java 객체 참조 (단, 단독 owner) |
| `Rc<T>` | 단일 스레드 내 공유 owner, reference counting | 사실상 `WeakReference` 없는 자바 객체에 가까움. 단 Java는 GC가 처리 |
| `Arc<T>` | 멀티스레드 공유 owner, atomic refcount | `AtomicReference`로 wrapping된 객체 공유 |
| `RefCell<T>` | 단일 스레드 interior mutability, 런타임 borrow check | "런타임에 동시성 검증" — 사실 Java의 일반 객체에 가까움 |
| `Mutex<T>`/`RwLock<T>` (보통 `Arc<Mutex<T>>`) | 멀티스레드 공유 + mutable | `synchronized`/`ReentrantLock`/`ReadWriteLock` |

권고 사용법: ([Smart Pointers Demystified — DEV.to](https://dev.to/sgchris/smart-pointers-demystified-box-rc-and-refcell-27k), [Mastering Safe Pointers in Rust — Technorely](https://technorely.com/insights/mastering-safe-pointers-in-rust-a-deep-dive-into-box-rc-and-arc))

#### 4.3 Drop과 결정적 소멸

`Drop` 트레잇은 RAII와 동일한 의미다. 변수가 scope를 벗어나면 즉시 `drop()`이 호출된다. JVM의 `try-with-resources`/`use {}`/`finalize()`보다 더 결정적이다. 파일 핸들, DB 커넥션, 락이 "예측 가능한 시점"에 풀린다. ([The Drop Trait as Finalizer — Medium](https://medium.com/@bugsybits/the-drop-trait-as-finalizer-rusts-hidden-destructor-pattern-d7d38798d6ac))

#### 4.4 GC vs Ownership 성능

Discord의 Read States 서비스 사례가 가장 유명하다. Go 버전은 GC가 약 2분마다 동작하면서 10~40ms tail latency 스파이크가 발생했다. Rust 버전은 LRU에서 evict될 때 즉시 메모리가 해제되어 평균 응답시간이 ms→μs로 떨어졌다. ([Why Discord is switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust))

Cloudflare Pingora: Nginx + Lua 기반에서 Rust 기반으로 옮긴 결과 **CPU 70% 절감, 메모리 67% 절감**, 그리고 일일 1조 요청 이상을 처리한다. ([How we built Pingora — Cloudflare Blog](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/))

### 토픽 5 — 동시성·비동기 (Send/Sync, async/await, tokio, channel, Mutex)

#### 5.1 Send/Sync — "타입에 새겨진 동시성 안전성"

`Send`는 "값의 ownership을 다른 스레드로 옮길 수 있다", `Sync`는 "&T를 여러 스레드에서 동시에 참조할 수 있다"를 의미하는 marker trait이다. 컴파일러가 자동으로 implement해주기 때문에 보통 직접 쓸 일은 거의 없지만, 이 두 트레잇 덕분에 Rust는 "data race를 컴파일 타임에 차단"한다. `Rc<T>`는 Send가 아니므로 multi-threaded 컨텍스트에 넣으려 하면 컴파일 에러가 난다. ([Send and Sync — The Rustonomicon](https://doc.rust-lang.org/nomicon/send-and-sync.html))

JVM의 `@ThreadSafe` 같은 어노테이션이 있지만 강제력이 없다. Rust는 강제한다.

#### 5.2 async/await와 Future

Rust의 async는 "stackless coroutine"이다. async 함수는 `Future` trait을 구현하는 상태 머신으로 컴파일된다. await는 그 상태 머신의 한 지점이다. 자체 runtime이 없으므로 `tokio`, `async-std`, `smol` 같은 외부 runtime을 골라 attach해야 동작한다. ([Why async Rust? — without.boats](https://without.boats/blog/why-async-rust/))

#### 5.3 tokio 런타임

tokio는 사실상 표준이다. 20,768개 crate가 tokio에 의존한다. work-stealing 스케줄러를 채택했고, 각 워커 스레드의 local queue가 비면 다른 워커의 queue에서 task를 훔쳐온다. Go·Erlang의 검증된 패턴을 따랐다. ([Making the Tokio scheduler 10x faster](https://tokio.rs/blog/2019-10-scheduler), [The State of Async Rust: Runtimes — corrode](https://corrode.dev/blog/async/))

#### 5.4 비교: Spring WebFlux / Kotlin Coroutine / CompletableFuture

- **Spring WebFlux + Reactor**: callback chain이 복잡하고 backpressure 모델이 따로 있다. 의도가 좋지만 디버깅이 어렵다.
- **Kotlin Coroutine**: `suspend` 함수와 구조화된 동시성. Rust async와 가장 비슷한 사용 감각을 준다(언어 기능 + runtime 분리, 콜백 없는 sequential 스타일).
- **Java CompletableFuture**: chaining 위주. 21+의 Virtual Thread는 또 다른 접근(스레드를 가볍게 만든다).
- **Rust async**: 가장 명시적이고, 가장 빠르다. 대신 "Pin", "Send 경계", "어떤 runtime에서 spawn하느냐" 같은 부담이 추가로 생긴다. 한 라인 결론: "Kotlin coroutine과 비슷한 모양인데, runtime 선택과 trait 안전성이 노출되어 있다." ([Catching up with async Rust — fasterthanlime](https://fasterthanli.me/articles/catching-up-with-async-rust))

#### 5.5 채널·Mutex

`std::sync::mpsc`, `tokio::sync::{mpsc, oneshot, broadcast, watch}`, `crossbeam::channel`. JVM의 `BlockingQueue`/`Disruptor`/`Channel(Kotlin)`에 대응한다. Mutex는 lock guard가 RAII로 풀려서 "lock 안 풀고 return" 같은 사고가 구조적으로 불가능하다.

#### 5.6 함정

- async fn in trait은 **Rust 1.75에서 stabilize됐지만 dyn-safety는 여전히 미해결**. 그래서 `dyn Trait`이 필요하면 여전히 `async-trait` crate가 필요하다. ([async fn and return-position impl Trait in traits — Rust Blog](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/), [async-trait — docs.rs](https://docs.rs/async-trait))
- await 지점을 가로지르는 동기 mutex guard는 데드락의 원인. tokio Mutex 또는 가드 범위를 좁혀야 한다. ([Surviving Rust async interfaces — fasterthanlime](https://fasterthanli.me/articles/surviving-rust-async-interfaces))
- **runtime 분열 문제**: tokio와 async-std/smol은 reactor와 AsyncRead/AsyncWrite trait이 다르다. async-std는 2025년 공식 sunset되어 smol을 권장한다. crate를 만들 때 어떤 runtime에 묶일지 결정해야 한다. ([Goodbye Async-Std, Welcome Smol — Rust Bytes](https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol))

### 토픽 6 — 빌드/패키지 (cargo, crates.io, workspace, feature flag)

- **Cargo는 Maven/Gradle을 합친 도구.** 빌드, 테스트, 의존성 해소, 문서 생성, 출판까지 한 도구로 끝난다. 학습 곡선이 짧고 일관성이 강하다.
- **workspace**: monorepo 안의 multi-module. 루트 `Cargo.toml`에 `[workspace]`로 멤버 crate를 나열한다. Gradle multi-module과 비슷하지만 설정이 훨씬 단순하다. ([Workspaces — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html))
- **feature flag**: `[features]`에 정의한 키를 `--features` 또는 `default-features`로 토글한다. `#[cfg(feature = "foo")]`로 conditional compile. Maven profile/Gradle variant보다 훨씬 더 깊게 코드 단위로 들어간다. workspace에서 동일 의존성이 다른 feature로 두 번 등장하면 unification 함정이 있으니 resolver = "2"를 명시해야 한다. ([cargo-features2 RFC](https://rust-lang.github.io/rfcs/2957-cargo-features2.html), [Cargo Workspace and the Feature Unification Pitfall — nickb.dev](https://nickb.dev/blog/cargo-workspace-and-the-feature-unification-pitfall/))
- **crates.io**: Maven Central 같은 중앙 저장소. semver를 강하게 따른다.

JVM 비교: Spring 프로젝트의 `application.yml` 프로파일과 Cargo feature는 "환경 분기 + 코드 분기를 어디서 처리하는가"가 다르다. Rust는 코드 자체가 conditional compile되고, 그래서 빌드 산출물이 환경별로 달라진다.

### 토픽 7 — 테스트·품질 (cargo test, doctest, criterion, clippy, rustfmt)

- **cargo test**: 단위 테스트는 모듈 안 `#[cfg(test)] mod tests {}`에 둔다. 통합 테스트는 `tests/` 디렉터리. JUnit이 외부 도구라면 cargo test는 언어 코어에 들어와 있다.
- **doctest**: 주석 안 ` ```rust ... ``` ` 코드가 자동으로 테스트된다. JavaDoc + JUnit을 한 줄로 합친 셈. 문서가 곧 살아있는 예제다.
- **criterion**: 통계적 벤치마크 라이브러리. JMH의 Rust 버전.
- **clippy**: 린터. 100여 가지 lint 카테고리(performance, correctness, style, complexity, perf)로 구성. SpotBugs/Sonar의 Rust 표준판이다.
- **rustfmt**: 포매터. ktlint/google-java-format에 해당.

권장 워크플로: 사전 커밋 훅으로 `cargo fmt --check && cargo clippy -- -D warnings && cargo test`를 묶고, CI에서 동일하게 돌린다. ([D - Useful Development Tools — The Rust Programming Language](https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html), [Rust Workflow: How to Use Cargo, Clippy and Rust Analyzer Efficiently — Medium](https://autognosi.medium.com/rust-workflow-how-to-use-cargo-clippy-and-rust-analyzer-efficiently-dcf6025a58e4))

### 토픽 8 — 웹 애플리케이션 (axum, actix-web, tower, tracing)

#### 8.1 프레임워크 지형

- **axum** (tokio 팀): tower 기반. extractor 패턴(`Path`, `Query`, `Json`, `State`)이 매력적이고, 미들웨어가 곧 `Service` trait이라 재사용성이 뛰어나다. 현재 가장 활발한 선택지. ([Announcing Axum — Tokio Blog](https://tokio.rs/blog/2021-07-announcing-axum), [axum docs](https://docs.rs/axum/latest/axum/))
- **actix-web**: actor 모델 기반. 가장 성숙하고 가장 빠르다(벤치 기준 axum보다 10~15% 처리량 우위). ([Rust Web Frameworks Compared — DEV.to](https://dev.to/leapcell/rust-web-frameworks-compared-actix-vs-axum-vs-rocket-4bad))
- **loco-rs**: 사실상 "Rust on Rails". CLI 스캐폴드, ORM(sea-orm), 백그라운드 잡, 스토리지가 통합. 내부적으로는 axum + sea-orm + sidekiq-rs를 합친다. Spring Boot의 "batteries included" 감각과 가장 가깝다. ([Loco.rs](https://loco.rs/), [What if Rails was Built on Rust?](https://loco.rs/blog/hello-world/), [Introducing Loco — Shuttle](https://www.shuttle.dev/blog/2023/12/20/loco-rust-rails))

#### 8.2 tower — Service trait

tower의 핵심은 `Service<Request>` trait이다. 비동기 함수(요청→응답)를 일급 시민으로 만들고, `Layer`로 합성한다. axum, tonic(gRPC), hyper, reqwest가 모두 같은 추상화 위에 있어서 미들웨어가 cross-framework로 재사용된다. Spring의 `Filter`/`HandlerInterceptor`/`@Aspect`가 한 모델로 통일된 셈이다. ([Unpacking the Tower Abstraction Layer in Axum and Tonic — Leapcell](https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic), [Introduction to the Tower library — Frankel](https://blog.frankel.ch/introduction-tower/))

#### 8.3 axum 패턴

핸들러는 그냥 async 함수다. Spring의 `@Controller` + `@PathVariable` 조합이 Rust에서는:

```rust
async fn get_user(
    Path(id): Path<i64>,
    State(pool): State<PgPool>,
) -> Result<Json<User>, AppError> { ... }
```

State는 axum의 의존성 주입. Spring `@Autowired` 없이도 컴파일러가 type 기반으로 검증해준다. clean/onion architecture를 적용한 axum 템플릿도 활발하다. ([Practical Clean Architecture in Rust — YouTube](https://www.youtube.com/watch?v=TrNpyFMtnzI), [Rust, Axum, and Onion Architecture — Medium](https://medium.com/@jonathan.el.baz/rust-axum-and-onion-architecture-escaping-the-tech-debt-spiral-14df5db946df))

#### 8.4 성능 비교

100 동시 연결 / JSON+PostgreSQL 시나리오에서 Spring Boot(JVM)는 4,200 req/s, P99 45ms, 280MB. axum + tokio는 42,000 req/s, P99 3ms, 12MB. **약 10배 처리량, 1/15 latency, 1/23 메모리**라는 보고. 단, 이 숫자는 매우 단순한 시나리오에 대한 것이고 비즈니스 로직이 깊어지면 격차가 줄어든다. WebFlux로 옮기면 JVM 측이 더 따라붙는다는 보고도 있다. ([Spring Boot Webflux vs Rust (Axum) — Medium](https://medium.com/deno-the-complete-reference/spring-boot-webflux-vs-rust-axum-hello-world-performance-28611da8bfc2), [Rust vs Spring Boot vs Quarkus — Medium](https://medium.com/javarevisited/rust-vs-spring-boot-vs-quarkus-the-performance-truth-nobody-talks-about-09941b196f8e))

### 토픽 9 — 데이터베이스 (sqlx, diesel, sea-orm, 마이그레이션)

세 라이브러리의 핵심은 "어디까지 타입으로 검증할 것인가"다. JPA/MyBatis 계열에서 옮겨오는 사람에게는 마음가짐의 변화가 가장 큰 영역이다.

#### 9.1 sqlx — "raw SQL + 컴파일 타임 검증"

- async-first. tokio/async-std 모두 지원.
- `sqlx::query!("SELECT id, name FROM users WHERE id = $1", id)` 매크로가 **컴파일 시점에 실제 DB에 접속해 SQL을 검증**하고, 결과 row의 타입을 Rust struct로 매핑한다. 컬럼 이름이나 타입이 틀리면 빌드가 깨진다.
- offline 모드: `cargo sqlx prepare`로 메타데이터를 `.sqlx/`에 저장하고 git에 커밋하면 CI에서 DB 없이 빌드 가능. ([SQLx Compile Time Verification — DeepWiki](https://deepwiki.com/launchbadge/sqlx/8.3-offline-mode-(prepare-command)), [sqlx::query 매크로 — docs.rs](https://docs.rs/sqlx/latest/sqlx/macro.query.html))
- 트레이드오프: 컴파일 시간이 길어지고 CI에 DB가 필요(또는 prepare 메타데이터 관리). MyBatis와 가장 비슷한 감각, 단 컴파일러가 한 단계 더 검증해준다.

#### 9.2 diesel — "ORM + 컴파일 타임 쿼리 빌더"

- 스키마를 Rust 타입으로 표현. `users::table.filter(users::name.eq("toby"))` 같은 query가 컴파일러에 의해 검증된다.
- 기본은 sync(`diesel_async`로 async 가능). 가장 오래되고 가장 type-safe한 선택. ([Diesel — diesel.rs](https://diesel.rs/), [Relations — Diesel Guide](https://diesel.rs/guides/relations.html))

#### 9.3 sea-orm — "Active Record + async-first"

- async-first, sqlx 위에 구축. Entity API가 DB 없이 컴파일된다.
- ORM 친화적 API(find_by_id, save). loco-rs가 기본 채택. ([Compare with Diesel — SeaORM](https://www.sea-ql.org/SeaORM/docs/internal-design/diesel/), [SeaORM vs SQLx — Medium](https://techpreneurr.medium.com/seaorm-vs-sqlx-the-rust-orm-war-ends-with-seaorm-1-0-2026-production-ready-87e219ae6fab))

#### 9.4 선택 가이드

| 출신 | 대응되는 Rust 선택 |
|---|---|
| MyBatis 좋아함 | sqlx(SQL 직접 쓰되 컴파일러가 검증) |
| Spring Data JPA / Hibernate 좋아함 | diesel 또는 sea-orm |
| QueryDSL을 좋아함 | diesel(타입 기반 query DSL) |
| ORM과 raw SQL을 자유롭게 섞고 싶음 | sea-orm(아래 sqlx 노출) |

마이그레이션은 `sqlx-cli`, `diesel migration`, `sea-orm-cli`가 각각 도구를 제공한다. Flyway/Liquibase 감각으로 쓰면 된다.

### 토픽 10 — CLI, 시스템 프로그래밍, FFI(JNI 비교)

#### 10.1 CLI 도구 — clap

`clap` derive macro로 `#[derive(Parser)]`만 붙이면 argparse가 끝난다. subcommand, flag, env var, default value, completion까지 한 줄씩으로 정의한다. picocli/Spring Shell이 한 라이브러리에 모인 것에 가깝다. Rust 자체의 `cargo`, `ripgrep`, `bat`, `fd`, `exa` 같은 CLI들이 모두 clap 기반이다. ([clap docs](https://docs.rs/clap/latest/clap/), [Picking an argument parser — Rain's Rust CLI recommendations](https://rust-cli-recommendations.sunshowers.io/cli-parser.html))

#### 10.2 시스템 프로그래밍

- `std::process`, `std::fs`, `std::os::unix`로 OS 직접 호출.
- `nix`, `libc` crate로 더 깊은 syscalls.
- `mio`, `polling`이 epoll/kqueue/IOCP의 cross-platform 추상화. tokio의 reactor가 mio 위에 있다.

JVM은 JNI/Project Panama로 native에 다가가지만 한계가 명확하다. Rust는 native가 곧 모국어다.

#### 10.3 FFI: JNI로 JVM과 Rust 잇기

JNI를 통해 Java/Kotlin에서 Rust 함수를 호출할 수 있다. `jni` crate가 JNIEnv·jobject 추상화를 제공하고, Rust 함수에 `#[no_mangle] pub extern "system" fn Java_...`을 붙이면 Java에서 native 메서드로 부를 수 있다. ([jni-rs — docs.rs](https://docs.rs/jni), [First Steps with Rust and JNI — daschl](https://nitschinger.at/First-Steps-with-Rust-and-JNI/), [Mix in Rust with Java (or Kotlin!) — Tweede golf](https://tweedegolf.nl/en/blog/147/mix-in-rust-with-java-or-kotlin))

대안:
- **JNR-FFI**: C ABI 기반. Rust 측에 JNI 의존성을 두지 않아도 됨.
- **Project Panama (JEP 442/454, Java 22+)**: JVM 차세대 native interop. Rust dylib을 호출하기 가장 깔끔한 미래.
- 빌드 도구: `cargo-ndk`로 Android target build, Mozilla의 `application-services`처럼 한 Rust crate를 iOS/Android/Desktop이 공유. ([Comprehensive Rust — With Java](https://google.github.io/comprehensive-rust/android/interoperability/java.html))

### 토픽 11 — 운영·배포 (정적 바이너리, 도커, 관측, 프로파일링, 컴플라이언스)

#### 11.1 정적 바이너리 + Docker

`x86_64-unknown-linux-musl` target으로 musl libc 기반 정적 바이너리를 만들고 `gcr.io/distroless/static-debian12` 또는 `scratch`에 넣으면 **8~10MB짜리 컨테이너 이미지**가 나온다. JVM 이미지(보통 200MB+) 대비 압도적이다. ([How to Create Minimal Docker Images for Rust Binaries — OneUptime](https://oneuptime.com/blog/post/2026-01-07-rust-minimal-docker-images/view), [muslrust — GitHub](https://github.com/clux/muslrust), [Building Minimal and Secure Rust Web Applications with Docker — Leapcell](https://leapcell.io/blog/building-minimal-and-secure-rust-web-applications-with-docker))

multi-stage Dockerfile 표준 패턴: builder stage에 `cargo build --release --target x86_64-unknown-linux-musl`, runtime stage는 distroless에 binary만 copy.

#### 11.2 관측(Observability)

`tracing` + `tracing-subscriber` + `tracing-opentelemetry`가 표준 스택이다. span에 구조화된 필드를 붙이고, OTLP exporter로 Datadog/Jaeger/Tempo로 전송한다. Java의 Spring Cloud Sleuth + OpenTelemetry SDK 조합과 거의 같은 모델이다. ([tracing-opentelemetry — docs.rs](https://docs.rs/tracing-opentelemetry), [How to monitor your Rust applications with OpenTelemetry — Datadog](https://www.datadoghq.com/blog/monitor-rust-otel/))

#### 11.3 프로파일링

`cargo flamegraph`(perf 기반), `tokio-console`(async task 인사이트), `samply`(rust 친화적 sampling). JFR/Async Profiler에 익숙한 사람에게 학습 곡선이 가장 평탄한 영역.

#### 11.4 컴플라이언스 — 메모리 안전성

ONCD 권고와 미국 NSA의 「Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development」(2025년 6월)는 Rust를 메모리 안전 언어의 대표로 다룬다. 정부·금융·국방 도메인은 이미 "왜 안전한 언어를 쓰지 않느냐"를 묻는 단계다. ([NSA Cybersecurity Information PDF](https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF))

### 토픽 12 — 생태계·커리어 관점

- **시장 인지**: Stack Overflow Developer Survey에서 9년 연속 "most admired language", admiration rate 83%. ([2025 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2025/))
- **상업적 사용 증가**: 2021~2024년 사이 Rust를 commercial하게 사용하는 비율이 68.75% 증가. 2025 State of Rust에서 응답자 53%가 매일 사용. ([State of Rust 2024](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/), [Is Rust Still Surging in 2026? — ZenRows](https://www.zenrows.com/blog/rust-popularity))
- **JVM/Rust 폴리글랏 전략**: 비즈니스 도메인은 Spring/Kotlin 유지, hot path(API gateway, ingress, 데이터 직렬화, 인증, 매칭 엔진 등)는 Rust로 분리. gRPC/HTTP API 또는 JNI/Panama로 묶는다. "전부 Rust로 갈아엎기"는 거의 모든 사례에서 권장되지 않는다. ([What do experts think — Quora](https://www.quora.com/What-do-experts-think-about-microservices-designing-in-Go-or-Rust-instead-of-Java-Spring-Boot), [Rust vs Spring Boot vs Quarkus — Medium](https://medium.com/javarevisited/rust-vs-spring-boot-vs-quarkus-the-performance-truth-nobody-talks-about-09941b196f8e))
- **학습 곡선**: corrode의 가이드는 Java→Rust 전환에 4~6개월의 적응 기간을 잡으라고 권한다. 처음 PoC는 비크리티컬 모듈로, 10~20% 정도만 Rust로 옮겨도 충분한 성능 효과가 난다고 본다. ([Migrating from Java to Rust — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/), [Before moving to Rust from Java — Medium](https://keazkasun.medium.com/before-moving-to-rust-from-java-2b87a70654c0))
- **한국 커뮤니티**: 한국 러스트 사용자 그룹(rust-kr.org)가 Discord 중심으로 활동, 『러스트 프로그래밍 언어』(rinthel 한국어 번역, 공식 doc.rust-kr.org), 『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』(제이펍) 같은 한국어 자료가 늘고 있다. ([rust-kr.org](https://rust-kr.org/), [Rust 한국어판](https://doc.rust-kr.org/), [실전 백엔드 러스트 Axum — devbull](https://devbull.xyz/blog/axum-book))

---

## 3. 주요 관점·논쟁점

### 3.1 "Rust는 백엔드에 적합한가" 논쟁

찬성:
- 메모리/CPU/latency 모든 면에서 JVM·Go보다 효율적이라는 보고가 일관적이다(Discord, Cloudflare, Figma, Dropbox, Microsoft Azure Data Explorer).
- 컴파일 타임 안전성이 운영 사고의 큰 카테고리(NPE, race condition, memory leak)를 사전에 차단한다.

반대/유보:
- "조립형" 생태계라 Spring Boot처럼 즉시 잡는 생산성을 기대하기 어렵다(loco-rs가 격차를 좁히는 중이지만).
- 컴파일 시간이 길다 — 2025 Rust Compiler Performance Survey에서 27%가 "큰 문제"로 꼽음. ([Rust compiler performance survey 2025](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/))
- 학습 곡선이 가파르다. 2024 State of Rust에서 응답자의 41.6%가 언어 복잡성에 우려를 표함. ([Rust 2025 Survey: 45.5% Adoption, 41.6% Worry Complexity — byteiota](https://byteiota.com/rust-2025-survey-45-5-adoption-41-6-worry-complexity/))

균형 잡힌 평: hot path/사이드카/CLI/시스템 컴포넌트는 Rust, 비즈니스 로직 다수는 JVM으로 두는 hybrid가 현실 다수의 선택. ([I Replaced My Spring Boot Microservice with Rust and Go — Medium](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494))

### 3.2 async 생태계 분열 (tokio vs async-std vs smol)

관점 A — "tokio가 사실상 표준이고 그게 최선": 가장 큰 ecosystem, 가장 많은 production 검증, work-stealing scheduler가 검증됨.

관점 B — "tokio 의존이 너무 깊다": "executor coupling" 때문에 라이브러리가 tokio에 묶이면 다른 runtime에서 못 쓴다. async-std는 2025년 sunset됐고, smol이 "tokio 안에서도 돌아가는 작은 빌딩 블록"으로 부상. crate 작성자에겐 smol이 더 안전한 default라는 의견. ([The 'One True Runtime' Friction — Tech Champion](https://tech-champion.com/general/the-one-true-runtime-friction-in-async-rust-development/), [Goodbye Async-Std — Substack](https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol))

관점 C — "Async Rust Is A Bad Language": Pin, Send 경계, async-trait의 dyn 미지원 등 함정이 너무 많아 별도의 sub-language가 됐다는 신랄한 비판도 있음. ([Async Rust Is A Bad Language — Bit Bashing](https://bitbashing.io/async-rust.html), [Pin and suffering — fasterthanlime](https://fasterthanli.me/articles/pin-and-suffering))

### 3.3 ORM 선택 — sqlx vs diesel vs sea-orm

- "raw SQL의 명료함 + 컴파일 타임 검증"을 원하면 sqlx. 단, 컴파일 시간/CI DB 부담.
- "JPA처럼 모델 중심으로 가고 싶다"면 sea-orm. async + 친숙한 Active Record 패턴.
- "최강의 type safety가 필요하고 sync여도 괜찮다"면 diesel. compile-time 강도가 가장 높음.

세 라이브러리는 사실 경쟁이라기보다 "JPA, MyBatis, QueryDSL이 자바에 공존하듯" 공존한다. ([Rust ORMs in 2026 — Medium](https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3), [A Guide to Rust ORMs in 2025 — Shuttle](https://www.shuttle.dev/blog/2024/01/16/best-orm-rust))

### 3.4 "JVM을 떠나야 하는가" — 실무자의 솔직한 평가

상반된 두 후기가 잘 보여준다.

- **이득 측**: "With Rust, you can write concurrent applications more easily than Java—this is 9 months of experience overtaking 10 years of experience." ([Migrating from Java to Rust — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/))
- **그늘 측**: "I rewrote a Java microservice in Rust and lost my job." 기술적으로는 옳았지만 조직·문화적으로는 실패한 사례를 다룸. 팀에 Rust를 알 줄 아는 사람이 1명뿐이면 bus factor가 위협. ([I Rewrote A Java Microservice In Rust And Lost My Job — Medium](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca))
- **Dropbox 사례의 그늘**: Magic Pocket의 Rust 컴포넌트는 "너무 잘 동작해서 손이 잘 안 갔다. 원작자들이 떠나자 그 코드를 다룰 수 있는 엔지니어가 부족해졌다." ([A Tale of Three Rust Codebases — Convex](https://news.convex.dev/a-tale-of-three-codebases/))

### 3.5 학습 곡선과 생산성 회복 시점

- "초기 4~6개월 동안 borrow checker와 싸운다"가 보편적 경험. corrode와 한국 후기 모두 일관됨. ([Flattening Rust's Learning Curve — corrode](https://corrode.dev/blog/flattening-rusts-learning-curve/), [Rust를 회사 업무로 쓰고난지 5개월 정도 — Jinwoo Park Blog](https://pmnxis.github.io/posts/five_mothes_ago_from_using_rust_as_work_kr/))
- 한국 한 시니어 개발자: "Rust는 빠르고 가볍고 안전한 프로그래밍 언어이며, 간단한 마이크로서비스를 AWS Lambda에 서버리스로 올려놓으면 빠르게 응답하고 비용도 저렴하다." ([Rust를 업무용 언어로 쓰다 — HappyProgrammer](https://medium.com/happyprogrammer-in-jeju/rust%EB%A5%BC-%EC%97%85%EB%AC%B4%EC%9A%A9-%EC%96%B8%EC%96%B4%EB%A1%9C-%EC%93%B0%EB%8B%A4-7723cd2c0a59))
- 4년차 후기: "익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다." ([4년간의 Rust 사용 후기 — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/))

---

## 4. 사례 (실제 채택 케이스)

### 4.1 Discord — Read States 서비스를 Go에서 Rust로
- 문제: Go GC가 2분마다 동작하며 10~40ms latency spike. 모든 채널 접속·메시지 read에서 사용자가 체감하는 지연.
- 해결: Rust 재작성. LRU evict 시 즉시 메모리 해제, 평균 응답이 ms→μs로 떨어지고 spike 제거.
- 출처: [Why Discord is switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)

### 4.2 Cloudflare — Pingora
- 일일 1조+ 요청을 처리하는 신규 reverse proxy. Nginx 대체.
- CPU 70% 절감, 메모리 67% 절감.
- multi-thread + connection pool 공유 모델이 Nginx의 multi-process 한계를 극복.
- 출처: [How we built Pingora — Cloudflare Blog](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/), [Cloudflare just got faster and more secure, powered by Rust](https://blog.cloudflare.com/20-percent-internet-upgrade/)

### 4.3 Dropbox — Magic Pocket
- exabyte-scale blob storage의 storage engine을 Go에서 Rust로 부분 재작성.
- 3~5x tail latency 개선, 노드당 CPU/RAM 사용량 감소, OOM 위협 해소.
- 운영의 그늘: 잘 굴러가서 손이 안 갔고, 원작자가 떠난 뒤 유지보수 인력 확보가 어려워졌다.
- 출처: [Inside the Magic Pocket — Dropbox](https://dropbox.tech/infrastructure/inside-the-magic-pocket), [Why we built a custom Rust library for Capture — Dropbox](https://dropbox.tech/application/why-we-built-a-custom-rust-library-for-capture), [A Tale of Three Rust Codebases — Convex](https://news.convex.dev/a-tale-of-three-codebases/)

### 4.4 Figma — multiplayer 서버
- TypeScript 단일 스레드 서버의 latency spike 문제 해결을 위해 Rust로 재작성.
- 직렬화 시간 10x 이상 빨라짐. 파일 ownership을 캡슐화한 타입으로 묶어 audit 가능.
- 단일 event loop(stdin→stdout) 패턴으로 borrow checker 복잡도 회피한 사례.
- 출처: [Rust in production at Figma](https://www.figma.com/blog/rust-in-production-at-figma/), [Making multiplayer more reliable](https://www.figma.com/blog/making-multiplayer-more-reliable/), [Supporting Faster File Load Times with Memory Optimizations in Rust](https://www.figma.com/blog/supporting-faster-file-load-times-with-memory-optimizations-in-rust/)

### 4.5 AWS — Firecracker
- AWS Lambda·Fargate를 떠받치는 microVM monitor. Rust로 작성.
- < 125ms 시작 시간, < 5MiB 메모리 footprint, 한 호스트에서 초당 150 microVM 생성.
- 출처: [Firecracker microVMs](https://firecracker-microvm.github.io/), [Firecracker GitHub](https://github.com/firecracker-microvm/firecracker), [AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/)

### 4.6 Microsoft — Windows kernel·Azure
- Azure CTO Mark Russinovich이 신규 C/C++ 프로젝트를 금지하고 Rust 권장.
- `win32kbase_rs.sys` 같은 Rust 코드가 Windows kernel에 들어감. Azure Data Explorer의 storage layer는 350,000 라인 Rust로 매일 수백 PB 처리.
- 2030년까지 C/C++ 코드를 모두 Rust로 옮기겠다는 목표.
- 출처: [Microsoft's Rust Bet — The New Stack](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/), [Russinovich: Microsoft is "All-in" on Rust](https://www.thurrott.com/dev/317950/russinovich-microsoft-is-all-in-on-rust), [Microsoft is rewriting core Windows libraries in Rust — The Register](https://www.theregister.com/2023/04/27/microsoft_windows_rust/)

### 4.7 한국 사례
- **한국 러스트 사용자 그룹(rust-kr.org)**: Discord 채널 + Meetup. "현업에서 러스트로 제품을 개발하고 있는 개발자들이 여럿 상주." ([rust-kr.org](https://rust-kr.org/))
- **한국어 도서/번역**: 『러스트 프로그래밍 언어』(rinthel 번역, [공식 doc.rust-kr.org](https://doc.rust-kr.org/)), 『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』(제이펍, [소개](https://devbull.xyz/blog/axum-book)).
- **개인 후기/도입 사례**: 김대현 「Rust를 업무용 언어로 쓰다」(서버리스 Lambda + Rust로 비용·응답 모두 만족), Jinwoo Park 「Rust를 회사 업무로 쓰고난지 5개월」(임베디드/시스템 영역에서의 도입), [4년간의 Rust 사용 후기](https://blog.cro.sh/posts/four-years-of-rust/), 비브로스 기술 블로그 「웹프론트엔드 개발자의 Rust 돌려까기」 등이 대표적.
- **확인 필요**: 우아한형제들/토스/당근 같은 대형 한국 IT의 공식 Rust 프로덕션 사용기는 본 리서치에서 확보하지 못했다. 채용 공고 ([디지털헬스케어 Rust 백엔드 — 랠릿](https://www.rallit.com/positions/3247/))를 통해 일부 기업이 Rust 기반 백엔드를 운영 중임이 간접적으로 확인되지만, 공식 기술 블로그 글은 향후 별도 추적이 필요하다.

### 4.8 JVM 시스템을 Rust로 일부 리라이트한 케이스 스터디
- "I Replaced My Spring Boot Microservice with Rust and Go" — 단일 hot path(CPU-bound 변환 + 캐싱)를 Rust로 분리해 AWS 비용 81% 절감, P99 150ms→대폭 개선. ([Medium 글](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494))
- "I Rewrote A Java Microservice In Rust And Lost My Job" — 기술 성공·정치 실패 사례. 조직 차원의 합의·인력 확보 없이 단독 리라이트가 위험할 수 있다는 교훈. ([Medium 글](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca))

---

## 5. JVM 개발자가 흔히 부딪히는 함정 (커뮤니티 발 핵심 인사이트)

이 절은 책의 "공감 챕터" 역할을 한다. 모두 실제 커뮤니티에서 반복적으로 등장한 호소다.

### 함정 1 — "왜 컴파일이 안 되지" (소유권/라이프타임)
가장 자주 만나는 메시지: "Borrow of moved value", "Value does not live long enough", "Cannot borrow as mutable because it is also borrowed as immutable". JVM에서는 그냥 참조 변수 두 개를 써도 문제가 없었던 코드가 빌드를 거부한다. 처방: borrow checker를 적이 아니라 동료(co-author)로 받아들여라. 처음 한 달은 "보여주는 에러 메시지를 그대로 따르는 것"이 가장 빠른 길. ([Rust ownership and borrows: Fighting the borrow-checker](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3), [The Borrow Checker: Rust's Tough-Love Mentor](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/))

### 함정 2 — async가 익숙하지 않은 형태로 동작한다
- "spawn한 task가 dropped 되니 사라진다" — JoinHandle을 안 쓰면 task가 cancel될 수 있다.
- "Mutex guard를 await로 가로지르면 데드락" — 동기 Mutex를 async 코드 안에서 쓰지 말 것. tokio Mutex 또는 가드 범위 좁히기.
- "blocking 호출을 async 함수 안에서 했더니 다른 task가 멈춤" — `tokio::task::spawn_blocking`으로 분리.
출처: [Surviving Rust async interfaces — fasterthanlime](https://fasterthanli.me/articles/surviving-rust-async-interfaces), [Some mistakes Rust doesn't catch — fasterthanlime](https://fasterthanli.me/articles/some-mistakes-rust-doesnt-catch)

### 함정 3 — "의존성이 너무 무거워 보인다"
Spring Boot starter 한 줄 + Spring 본체가 알아서 뭉쳐주던 세계와 다르다. Rust에서는 axum + tokio + tower + tracing + serde + sqlx + anyhow + thiserror + clap 같이 작은 crate를 손으로 조립해야 한다. 처방: 처음에는 loco-rs 같은 starter를 쓰거나, 회사용 internal "starter crate"를 만든다. ([What if Rails was Built on Rust? — Loco](https://loco.rs/blog/hello-world/))

### 함정 4 — "트레잇이 인터페이스 같지 않다"
- 외부 타입에 트레잇 구현을 추가할 때 orphan rule에 막힌다(crate 안에서 둘 중 하나는 정의돼야 함).
- "왜 `Vec<Box<dyn MyTrait>>`을 못 만들지?" — trait이 object-safe하지 않을 때(Self를 method signature에 포함하거나 generic method가 있으면) dyn 사용 불가.
- "왜 async fn in trait이 dyn으로 안 되지?" — 1.75 stabilize에도 불구하고 dyn-safe는 미해결. async-trait crate로 우회. ([async-trait — docs.rs](https://docs.rs/async-trait), [Async fn in dyn trait — async-fundamentals-initiative](https://rust-lang.github.io/async-fundamentals-initiative/explainer/async_fn_in_dyn_trait.html))

### 함정 5 — "왜 String이 두 개나 있지" (`String` vs `&str`)
- `String`: heap-allocated, owned, growable.
- `&str`: borrowed view, immutable. 문자열 리터럴 `"hello"`의 타입.
- JVM의 `String`은 모두 immutable이고 ownership 개념이 없으므로 처음에 가장 많이 헷갈리는 지점. 처방: 함수 파라미터는 보통 `&str`(읽기), 반환·저장은 `String`(소유)으로 잡는 게 디폴트.

### 함정 6 — 컴파일 시간
"5초만 봐도 cargo가 도는 시간이 1분이 넘는다." 대형 프로젝트에서 incremental rebuild가 30s~1min 흔함. 2025 Rust Compiler Performance Survey에서 가장 큰 불만으로 지목. 완화: workspace 분할, `cargo check` 활용, sccache, mold linker, codegen-units 조정. ([Rust compiler performance survey 2025 — Rust Blog](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/))

### 함정 7 — "Spring AOP/DI 같은 마법이 없다"
- DI는 함수 인자/State/제네릭으로 명시. 의존성 그래프가 코드에 그대로 보인다.
- AOP는 tower Layer로 대체. 하지만 "코드 변경 없이 어노테이션 하나로 transactional 만들기" 같은 것은 없음. macro로 비슷하게 만들 수는 있지만 마법이 줄어든 만큼 명시성이 늘어난다.

---

## 6. 인용 가능한 한 줄 (Quotables)

> "Rust gave C++ levels of control and efficiency within a much safer and more ergonomic development environment." — Dropbox engineering, [A Tale of Three Rust Codebases](https://news.convex.dev/a-tale-of-three-codebases/)

> "9 months of [Rust] experience overtaking 10 years of [Java] experience." — corrode, [Migrating from Java to Rust](https://corrode.dev/learn/migration-guides/java-to-rust/)

> "Pingora consumes about 70% less CPU and 67% less memory compared to our old service with the same traffic load." — Cloudflare, [How we built Pingora](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/)

> "Rust does not have the overhead of garbage collection or the associated runtime which has prevented languages like Java and C# from reaching the performance of C++ in 'object heavy' applications." — [Rust for Java Developers](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)

> "45% of organizations are now making significant use of Rust in production — a seven percentage-point jump from 2023." — [2024 State of Rust Survey](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/)

> "For the ninth year in a row, Rust is the language that most developers used and want to use again, with an 83% admiration rate." — [2025 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2025/)

> "Plan 4-6 months for your engineers to get comfortable with Rust, and expect a few bumps along the way." — corrode, [Migrating from Java to Rust](https://corrode.dev/learn/migration-guides/java-to-rust/)

> "Spring Boot 4,200 req/s, P99 45ms, 280MB. Rust+Axum 42,000 req/s, P99 3ms, 12MB." — JSON+Postgres 단순 시나리오 벤치, [Rust vs Spring Boot vs Quarkus](https://medium.com/javarevisited/rust-vs-spring-boot-vs-quarkus-the-performance-truth-nobody-talks-about-09941b196f8e)

> "AWS Lambda uses Firecracker as the foundation for provisioning and running sandboxes upon which we execute customer code." — [AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/)

> "Memory errors in C and C++ cause an estimated 70 percent of all vulnerabilities in Microsoft products." — Microsoft, [Microsoft's Rust Bet](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/)

> "I rewrote A Java microservice in Rust and lost my job. The decision was technically right, politically wrong, and culturally radioactive." — [Medium](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca)

> "Compile times remain the most persistent source of frustration, with more than 27% of respondents calling slow compilation a significant problem." — [2024 State of Rust Survey](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/)

> "한국에 거주 중인 캐나다인 프로그래머가 만든 'Easy Rust Korean / Rust in a Month of Lunches' 한국어판 강의 동영상이 있다." — [한국 러스트 사용자 그룹](https://rust-kr.org/)

> "익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다." — 4년간 Rust 사용한 한국 개발자, [blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/)

> "RustBelt: securing the foundations of the Rust programming language — the first formal (and machine-checked) safety proof for a language representing a realistic subset of Rust." — POPL 2018, [Jung et al.](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf)

---

## 7. 참고문헌

### 공식 문서·정부 보고서
- [The Rust Programming Language Book](https://doc.rust-lang.org/book/) — Steve Klabnik, Carol Nichols
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [The Rustonomicon — Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- [Tokio docs](https://docs.rs/tokio/), [tokio.rs Tutorial](https://tokio.rs/tokio/tutorial)
- [axum docs](https://docs.rs/axum/)
- [sqlx repo](https://github.com/launchbadge/sqlx), [sqlx 매크로 레퍼런스](https://docs.rs/sqlx/latest/sqlx/macro.query.html)
- [Diesel — diesel.rs](https://diesel.rs/), [Diesel relations](https://diesel.rs/guides/relations.html)
- [SeaORM — sea-ql.org](https://www.sea-ql.org/SeaORM/)
- [clap docs](https://docs.rs/clap/), [clap derive 튜토리얼](https://docs.rs/clap/latest/clap/_derive/_tutorial/index.html)
- [tracing docs](https://docs.rs/tracing), [tracing-opentelemetry docs](https://docs.rs/tracing-opentelemetry)
- [White House ONCD: Back to the Building Blocks (2024-02)](https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf)
- [NSA: Memory Safe Languages — Reducing Vulnerabilities in Modern Software Development (2025-06)](https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF)

### 학술 논문
- Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. — [RustBelt: Securing the Foundations of the Rust Programming Language (POPL 2018)](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf), [CACM 2021 정리본](https://iris-project.org/pdfs/2021-rustbelt-cacm-final.pdf)
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. — [Stacked Borrows: An Aliasing Model for Rust (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf)
- Villani, N., Hostert, J., Dreyer, D., Jung, R. — [Tree Borrows (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf), [블로그 소개](https://www.ralfj.de/blog/2023/06/02/tree-borrows.html)
- Gäher, L. et al. — [RefinedRust: A Type System for High-Assurance Verification of Rust Programs (PLDI 2024)](https://plv.mpi-sws.org/refinedrust/paper-refinedrust.pdf)
- Xu, H. et al. — [Memory-Safety Challenge Considered Solved? An In-Depth Study with All Rust CVEs (arXiv:2003.03296)](https://arxiv.org/abs/2003.03296v1)
- Cui, M. et al. — [Is unsafe an Achilles' Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming (arXiv:2308.04785)](https://arxiv.org/abs/2308.04785)
- [Rust for Embedded Systems: Current State and Open Problems (arXiv:2311.05063)](https://arxiv.org/html/2311.05063v2)
- [A Grounded Conceptual Model for Ownership Types in Rust (arXiv:2309.04134)](https://arxiv.org/pdf/2309.04134)
- [deepSURF: Detecting Memory Safety Vulnerabilities in Rust (IEEE S&P 2026, arXiv:2506.15648)](https://arxiv.org/html/2506.15648v2)

### 회사 엔지니어링 블로그 (사례)
- Discord: [Why Discord is switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)
- Cloudflare: [How we built Pingora](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/), [20-percent internet upgrade](https://blog.cloudflare.com/20-percent-internet-upgrade/)
- Dropbox: [Inside the Magic Pocket](https://dropbox.tech/infrastructure/inside-the-magic-pocket), [Why we built a custom Rust library for Capture](https://dropbox.tech/application/why-we-built-a-custom-rust-library-for-capture), [InfoQ Magic Pocket 정리](https://www.infoq.com/articles/dropbox-magic-pocket-exabyte-storage/)
- Figma: [Rust in production at Figma](https://www.figma.com/blog/rust-in-production-at-figma/), [Making multiplayer more reliable](https://www.figma.com/blog/making-multiplayer-more-reliable/), [Faster File Load Times with Memory Optimizations in Rust](https://www.figma.com/blog/supporting-faster-file-load-times-with-memory-optimizations-in-rust/)
- AWS: [Firecracker GitHub](https://github.com/firecracker-microvm/firecracker), [Firecracker AWS Blog](https://aws.amazon.com/blogs/aws/firecracker-lightweight-virtualization-for-serverless-computing/), [Firecracker Open Source Blog](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/), [Firecracker NSDI 논문](https://assets.amazon.com/96/c6/302e527240a3b1f86c86c3e8fc3d/firecracker-lightweight-virtualization-for-serverless-applications.pdf)
- Microsoft: [Microsoft's Rust Bet — The New Stack](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/), [Russinovich: All-in on Rust — Thurrott](https://www.thurrott.com/dev/317950/russinovich-microsoft-is-all-in-on-rust), [Microsoft is rewriting core Windows libraries in Rust — The Register](https://www.theregister.com/2023/04/27/microsoft_windows_rust/)
- Convex: [A Tale of Three Rust Codebases](https://news.convex.dev/a-tale-of-three-codebases/)

### 블로그·기술 매체 (개념·비교)
- [Rust Blog: 2024 State of Rust Survey Results (2025-02)](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/)
- [Rust Blog: Rust compiler performance survey 2025 results (2025-09)](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/)
- [Rust Blog: 2025 State of Rust Survey Results (2026-03)](https://blog.rust-lang.org/2026/03/02/2025-State-Of-Rust-Survey-results/)
- [Rust Blog: Announcing async fn and RPIT in traits (2023-12)](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)
- [The New Stack: Survey: Memory-Safe Rust Gains 45% of Enterprise Development](https://thenewstack.io/survey-memory-safe-rust-gains-45-of-enterprise-development/)
- [The New Stack: Nearly half of all companies now use Rust in production](https://thenewstack.io/rust-enterprise-developers/)
- [JetBrains RustRover Blog: The State of Rust Ecosystem 2025 (2026-02)](https://blog.jetbrains.com/rust/2026/02/11/state-of-rust-2025/)
- [JetBrains RustRover Blog: The Evolution of Async Rust (2026-02)](https://blog.jetbrains.com/rust/2026/02/17/the-evolution-of-async-rust-from-tokio-to-high-level-applications/)
- [Stack Overflow Blog: In Rust We Trust? White House Office urges memory safety (2024-12)](https://stackoverflow.blog/2024/12/30/in-rust-we-trust-white-house-office-urges-memory-safety/)
- [2025 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2025/)
- [corrode: Migrating from Java to Rust](https://corrode.dev/learn/migration-guides/java-to-rust/)
- [corrode: Flattening Rust's Learning Curve](https://corrode.dev/blog/flattening-rusts-learning-curve/)
- [corrode: The State of Async Rust — Runtimes](https://corrode.dev/blog/async/)
- [Without Boats: Why async Rust?](https://without.boats/blog/why-async-rust/), [Without Boats: Pin](https://without.boats/blog/pin/), [Without Boats: Three problems of pinning](https://without.boats/blog/three-problems-of-pinning/)
- [fasterthanlime: Catching up with async Rust](https://fasterthanli.me/articles/catching-up-with-async-rust)
- [fasterthanlime: Surviving Rust async interfaces](https://fasterthanli.me/articles/surviving-rust-async-interfaces)
- [fasterthanlime: Pin and suffering](https://fasterthanli.me/articles/pin-and-suffering)
- [fasterthanlime: Some mistakes Rust doesn't catch](https://fasterthanli.me/articles/some-mistakes-rust-doesnt-catch)
- [Niko Matsakis: baby steps blog](https://smallcultfollowing.com/babysteps/)
- [Tokio Blog: Making the Tokio scheduler 10x faster](https://tokio.rs/blog/2019-10-scheduler)
- [Tokio Blog: Announcing Axum](https://tokio.rs/blog/2021-07-announcing-axum)
- [Bit Bashing: Async Rust Is A Bad Language](https://bitbashing.io/async-rust.html)
- [Rust for Java Developers (tkaitchuck)](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)
- [softwaremill: Rust Static vs. Dynamic Dispatch](https://softwaremill.com/rust-static-vs-dynamic-dispatch/)
- [Comprehensive Rust — Java interop (Google)](https://google.github.io/comprehensive-rust/android/interoperability/java.html)
- [jni-rs GitHub](https://github.com/jni-rs/jni-rs), [jni-rs docs](https://docs.rs/jni)
- [Tweede golf: Mix in Rust with Java (or Kotlin!)](https://tweedegolf.nl/en/blog/147/mix-in-rust-with-java-or-kotlin)
- [Loco.rs](https://loco.rs/), [Loco GitHub](https://github.com/loco-rs/loco), [Loco InfoQ 소개](https://www.infoq.com/news/2024/02/loco-new-framework-rust-rails/), [Loco Hello World](https://loco.rs/blog/hello-world/), [Introducing Loco — Shuttle](https://www.shuttle.dev/blog/2023/12/20/loco-rust-rails)
- [Leapcell: Unpacking the Tower Abstraction Layer in Axum and Tonic](https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic)
- [Leapcell: Unraveling sqlx Macros](https://leapcell.io/blog/unraveling-sqlx-macros-compile-time-sql-verification-and-database-connectivity-in-rust)
- [Leapcell: Building Minimal and Secure Rust Web Applications with Docker](https://leapcell.io/blog/building-minimal-and-secure-rust-web-applications-with-docker)
- [Frankel: Introduction to Tower](https://blog.frankel.ch/introduction-tower/), [Frankel: Rust and the JVM](https://blog.frankel.ch/start-rust/7/)
- [Datadog: How to monitor your Rust applications with OpenTelemetry](https://www.datadoghq.com/blog/monitor-rust-otel/)
- [Phoronix: Cloudflare Ditches Nginx For In-House, Rust-Written Pingora](https://www.phoronix.com/news/CloudFlare-Pingora-No-Nginx)
- [Aarambh Dev Hub: Rust Web Frameworks in 2026](https://aarambhdevhub.medium.com/rust-web-frameworks-in-2026-axum-vs-actix-web-vs-rocket-vs-warp-vs-salvo-which-one-should-you-2db3792c79a2), [Rust ORMs in 2026](https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3)
- [Tech Tonic / Medium: Spring Boot Webflux vs Rust (Axum)](https://medium.com/deno-the-complete-reference/spring-boot-webflux-vs-rust-axum-hello-world-performance-28611da8bfc2)
- [JavaRevisited: Rust vs Spring Boot vs Quarkus](https://medium.com/javarevisited/rust-vs-spring-boot-vs-quarkus-the-performance-truth-nobody-talks-about-09941b196f8e)
- [Substack: Goodbye Async-Std, Welcome Smol](https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol)
- [Substack: Tree Borrows Just Landed](https://weeklyrust.substack.com/p/tree-borrows-just-landed)
- [BigGo News: Rust's Learning Curve Debate](https://biggo.com/news/202502181925_rust-learning-curve-debate)
- [byteiota: Rust 2025 Survey: 45.5% Adoption, 41.6% Worry Complexity](https://byteiota.com/rust-2025-survey-45-5-adoption-41-6-worry-complexity/)
- [muslrust GitHub](https://github.com/clux/muslrust), [Chainguard: Distroless container images](https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/)
- [Java Code Geeks: Memory Safety and Performance — Rust's Theoretical Edge](https://www.javacodegeeks.com/2025/12/memory-safety-and-performance-rusts-theoretical-edge-over-traditional-languages.html)
- [Rust Magazine: How Tokio schedules tasks — A hard lesson learnt](https://rustmagazine.org/issue-4/how-tokio-schedule-tasks/)

### 한국어 자료
- [한국 러스트 사용자 그룹 (rust-kr.org)](https://rust-kr.org/)
- [The Rust Programming Language 한국어판 (rinthel)](https://rinthel.github.io/rust-lang-book-ko/)
- [Rust 한국어판 공식 (doc.rust-kr.org)](https://doc.rust-kr.org/)
- [김대현, "Rust를 업무용 언어로 쓰다" — HappyProgrammer (Medium)](https://medium.com/happyprogrammer-in-jeju/rust%EB%A5%BC-%EC%97%85%EB%AC%B4%EC%9A%A9-%EC%96%B8%EC%96%B4%EB%A1%9C-%EC%93%B0%EB%8B%A4-7723cd2c0a59)
- [Jinwoo Park, "Rust를 회사 업무로 쓰고난지 5개월 정도"](https://pmnxis.github.io/posts/five_mothes_ago_from_using_rust_as_work_kr/)
- [Option::None, "4년간의 Rust 사용 후기"](https://blog.cro.sh/posts/four-years-of-rust/)
- [appleseed, "일주일만에 Rust에 매료되다"](https://blog.appleseed.dev/post/fascinated-by-rust-in-a-week/)
- [SmileCat, "Rust 찍먹후기"](https://blog.smilecat.dev/posts/research-rust/)
- [비브로스 기술 블로그, "웹프론트엔드 개발자의 Rust 돌려까기"](https://boostbrothers.github.io/experience/2022/03/28/rust-trun-around/)
- [이랜서 블로그, "왜 많은 개발자들이 Rust로 이동할까?"](https://www.elancer.co.kr/blog/detail/808)
- [scalalang2, "Rust의 소유권 이야기" — CURG (Medium)](https://medium.com/curg/rust%EC%9D%98-%EC%86%8C%EC%9C%A0%EA%B6%8C-%EC%9D%B4%EC%95%BC%EA%B8%B0-a4c19c1b2c10)
- [sangjinsu, "🦀 Rust로 실전 백엔드 개발을 경험하다" (velog)](https://velog.io/@sangjinsu/Rust%EB%A1%9C-%EC%8B%A4%EC%A0%84-%EB%B0%B1%EC%97%94%EB%93%9C-%EA%B0%9C%EB%B0%9C%EC%9D%84-%EA%B2%BD%ED%97%98%ED%95%98%EB%8B%A4)
- [Indo Yoon, "실전 백엔드 러스트 Axum 프로그래밍 — 책 소개"](https://devbull.xyz/blog/axum-book)
- [한국 채용 — 디지털헬스케어 Rust 백엔드 개발자 (랠릿)](https://www.rallit.com/positions/3247/)
- [namu.wiki: Rust(프로그래밍 언어)](https://namu.wiki/w/Rust(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)), [Rust(프로그래밍 언어)/비판](https://namu.wiki/w/Rust(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)/%EB%B9%84%ED%8C%90)

### 마이그레이션·후기 사례 (Medium/DEV.to/Reddit 인용 검색 경로)
- [I Replaced My Spring Boot Microservice with Rust and Go (Medium)](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494)
- [I Rewrote A Java Microservice In Rust And Lost My Job (Medium)](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca)
- [Before moving to Rust from Java — Kasun Ranasinghe (Medium)](https://keazkasun.medium.com/before-moving-to-rust-from-java-2b87a70654c0)
- [How Discord Moved from Go to Rust — OpenSourceScribes (Medium)](https://medium.com/sourcescribes/how-discord-moved-from-go-to-rust-ad98cf0a1d59)
- [Hacker News: Why Discord is switching from Go to Rust (2020)](https://news.ycombinator.com/item?id=26227339)
- [Hacker News: Rust in production at Figma (2018)](https://news.ycombinator.com/item?id=16977932)
- [Hacker News: Spring-rs is a microservice framework in Rust (2024)](https://news.ycombinator.com/item?id=41274138)
- [Hacker News: Ask HN: How to structure Rust, Axum, and SQLx for clean architecture?](https://news.ycombinator.com/item?id=40294092)

---

## 8. 리서치 한계 (커버하지 못한 영역)

본 리서치에서 충분히 확보하지 못해, 본 책 집필 시 추가 보강이 필요한 영역들이다.

1. **한국 대형 IT 기업의 공식 Rust 프로덕션 사용기**: 우아한형제들/토스/당근/카카오/네이버/쿠팡의 기술 블로그에서 "Rust로 X를 만들었다"는 공식 글을 본 리서치 범위에서 발견하지 못했다. 채용 공고를 통해 일부 기업이 Rust 백엔드를 운영하고 있다는 간접 신호는 있지만, 1차 자료 인용을 위해서는 추가로 각 회사 블로그의 RSS/검색을 직접 추적하고 RustKorea Meetup 발표 자료를 확보하는 후속 작업이 필요하다.
2. **Project Panama vs JNI vs JNR-FFI 정량 비교**: 세 방식이 존재한다는 것까지 확인했지만 latency/throughput 측면의 공식 벤치마크는 발견하지 못했다. JEP 442/454의 GA 이후 측정한 비교 데이터가 더 모이면 한 챕터 분량으로 다룰 가치가 있다.
3. **임베디드/시스템 영역**: arXiv "Rust for Embedded Systems"는 식별했지만 본 책의 백엔드 중심 스코프와 거리가 있어 깊게 파지 않았다. 관련 챕터에서는 fact만 가볍게 언급한다.
4. **Rust 1.83 이후의 최신 변화**: 2026년 5월 시점에서 가장 최신 RFC들(예: stable async iterator, generic associated types 활용 패턴)에 대한 종합 정리는 본 리서치에 충분히 담기지 않았다. 집필 단계에서 Rust Blog 최신 release note를 함께 보며 보강이 필요하다.
5. **OKKY/디스코드 한국 커뮤니티의 1차 토론 로그**: 검색으로는 OKKY 일부만 확보했고, 한국 Rust Discord 채널의 실제 대화 발췌는 동의·접근 절차가 별도로 필요해 본 리서치에서는 다루지 않았다. "한국 시니어 개발자가 부딪힌 함정" 챕터를 더 두텁게 만들기 위해서는 직접 인터뷰가 가장 좋은 보강책이다.
