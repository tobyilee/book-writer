# 부록 A. JVM ↔ Rust 한 페이지 매핑 표

이 부록의 약속은 한 줄이다. *책상 옆에 한 장 펴 놓고 매일 본다*. 본문 16개 챕터에 산발적으로 박힌 *"JVM 대응물 매핑"*을 10개 영역으로 묶어 한 자리에 모았다. 매 행 끝에 *본문 N장 X절 참조*를 박아두었으니, 표만 보다가 깊이가 부족하면 그 자리로 돌아가 본문을 한 절 더 펴자.

기억해두자 — *어떤 매핑도 100% 일치하지는 않는다*. *"의미가 비슷하다"*와 *"표기가 비슷하다"*는 다른 카테고리고, *"역할은 같지만 시점이 다르다"*가 가장 자주 나오는 패턴이다(런타임 검증 vs 컴파일 검증). 표의 *결정적 차이* 열을 꼭 함께 보자.

## A.1 타입 시스템

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `int` / `long` / `double` / `boolean` / `char` | `i32` / `i64` / `f64` / `bool` / `char` | Rust는 boxing/unboxing 없음. `usize`/`isize`는 *플랫폼 워드 크기*. | 3장 |
| `Integer` / `Long` (autoboxing) | (없음 — 원시 타입 그대로) | Rust는 `Option<i32>`로 *부재*를 표현, `null` 자체가 없음. | 3·7장 |
| `String` (불변) | `String` (heap-allocated owned) + `&str` (borrowed view) | 두 개로 갈라진 게 4장의 *복선*. 함수 파라미터는 보통 `&str`. | 3·4장 |
| `ArrayList<T>` / `List<T>` | `Vec<T>` / `&[T]` (slice) | `Vec<T>`는 owned, `&[T]`는 borrowed. | 3장 |
| `HashMap<K, V>` | `HashMap<K, V>` (`std::collections`) | Rust 표준 HashMap은 *DoS-resistant* hash 사용. | 3장 |
| `Optional<T>` (Java 8+) | `Option<T>` (`Some`/`None`) | Rust는 *exhaustive match*가 컴파일러 강제. NPE 자체가 모양으로 만들어지지 않음. | 7장 |
| `record User(...)` (Java 14+) | `struct User { ... }` + `#[derive(Debug, Clone)]` | Rust는 getter/setter 자동 생성 X — `pub` 필드로 노출하거나 명시적 메서드. | 3·7장 |
| `enum Color { RED, GREEN }` | `enum Color { Red, Green }` | Rust enum은 *algebraic data type* — 변종마다 데이터 보유 가능 (`enum Result<T, E> { Ok(T), Err(E) }`). | 7장 |
| sealed class + pattern matching (Java 17+) | enum + `match` | Rust `match`는 *식*이고 *exhaustive 강제*. `default` 강요 없음. | 3·7장 |
| `interface` / abstract class | `trait` | Rust trait은 *외부 타입에도 구현 가능*(orphan rule 안에서). 정적/동적 디스패치 명시. | 7장 |
| Generics (type erasure) | Generics (monomorphization) | Rust는 컴파일 시점 코드 생성 → 0-cost. 단점은 컴파일 시간·바이너리 크기. | 7장 |

## A.2 제어 흐름

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `if (...) { } else { }` | `if ... { } else { }` (식) | Rust `if`는 *값을 반환*. `let x = if cond { 1 } else { 2 };`. | 3장 |
| `switch` / `switch expression` | `match` (식) | exhaustive 강제. guard·구조 분해·`@` 바인딩 가능. | 3·7장 |
| `for (T x : collection)` | `for x in collection { }` | `for in`은 `IntoIterator`를 구현한 모든 타입에. | 3장 |
| `while (cond) { }` / `do-while` | `while cond { }` / `loop { ... break value; }` | Rust `loop`는 *값을 반환할 수 있는 무한 루프*. | 3장 |
| `try / catch / finally` | `Result<T, E>` + `?` 연산자 | 예외가 아니라 *값*. `?`는 fallible 함수에서 early return sugar. | 7장 |
| checked exception (`throws`) | `Result<T, E>` 반환 | Rust는 *모든 실패 가능성*이 시그니처에 드러남. | 7장 |
| `RuntimeException` (unchecked) | `panic!` (unrecoverable) | `panic!`은 *복구하지 않을 자리*. 95% 코드는 `Result`. | 7장 |
| `if (x != null)` 가드 | `if let Some(x) = opt { }` 또는 `match` | Rust는 *부재*를 타입으로 강제. | 7장 |

## A.3 모듈·패키지·가시성

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `package com.example.foo` | `mod foo` (파일 경로 = 모듈 경로) | Rust 모듈은 *파일 시스템에 연결*되지만 명시적 `mod` 선언 필요. | 3장 |
| `import java.util.List;` | `use std::collections::HashMap;` | prelude(`Option`, `Result`, `Vec`, `String`)는 import 없이 보임. | 3장 |
| `public` / package-private / `private` | `pub` / `pub(crate)` / `pub(super)` / (default = private) | Rust 디폴트가 *private*. | 3장 |
| `module-info.java` (JPMS) | `Cargo.toml` + `[lib]` / `[bin]` | crate 단위가 *컴파일·배포 단위*. | 2·13장 |
| Maven multi-module | cargo workspace (`[workspace]`) | 단일 `Cargo.lock`, 단일 `target/` 공유. | 2·13장 |
| jar / war | rlib / dylib / staticlib / 바이너리 | crate type을 `Cargo.toml`에서 선언. | 2장 |

## A.4 예외·에러 처리

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| checked exception (`throws IOException`) | `Result<T, E>` + `?` | 시그니처가 *값*으로 표현됨 → 함수 합성에 자유. | 7장 |
| try-with-resources / `AutoCloseable` | `Drop` 트레잇 (RAII) | scope 종료 시 *결정적*으로 호출. `try` 블록보다 한 단계 더 결정적. | 4·8장 |
| `NullPointerException` | (모양 자체가 안 만들어짐) | Rust에는 `null`이 없음. `Option<T>`로 강제. | 7장 |
| 예외 wrapping (`new RuntimeException(e)`) | anyhow `?` + context (`.context("...")?`) | `anyhow::Result`는 *애플리케이션* 영역. | 7장 |
| 도메인 예외 계층 | thiserror `enum AuthError { ... }` | `#[derive(thiserror::Error)]`로 enum에 자동 구현. *라이브러리* 영역. | 7장 |
| `Optional.orElseThrow` | `option.ok_or(err)?` | sugar의 결이 같지만 *타입 안전*. | 7장 |
| stack trace | `Backtrace` (anyhow + `RUST_BACKTRACE=1`) | 환경 변수로 활성화. | 7장 |

## A.5 동시성·async

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `Thread` / `ExecutorService` | `std::thread::spawn` / `tokio::spawn` | 표준은 OS 스레드, async 런타임은 별도(tokio). | 9·10장 |
| `Runnable` / `Callable<T>` | 클로저 + `Send + 'static` bound | `'static` bound가 *컴파일러가 강제하는 lifetime 계약*. | 9·10장 |
| `synchronized` (블록) | `Mutex<T>::lock()` (RAII guard) | guard가 scope 종료 시 자동 해제 — *lock 안 풀고 return* 사고가 *모양으로* 안 됨. | 9장 |
| `AtomicInteger` / `AtomicReference` | `AtomicI32` / `AtomicPtr` (`std::sync::atomic`) | Memory ordering(`Ordering::SeqCst` 등)을 *명시*. | 9장 |
| `BlockingQueue` / Kotlin `Channel` | `std::sync::mpsc` / `tokio::sync::mpsc` | std는 동기, tokio는 async. | 9·10장 |
| `@ThreadSafe` / `@GuardedBy` | `Send` / `Sync` 마커 트레잇 | 어노테이션이 아니라 *컴파일러 검증*. | 9장 |
| Java 21 `Virtual Thread` | Rust async + tokio (다른 축) | Virtual Thread는 *블로킹 코드 그대로*, async는 *함수 색깔이 갈림*. | 10장 |
| `CompletableFuture<T>` | `Future` trait + `async` / `await` | `Future`는 컴파일러가 만드는 *상태 머신*. | 10장 |
| Kotlin `suspend fun` | Rust `async fn` | 사용 감각은 가장 가까움. runtime은 직접 골라야 함. | 10장 |
| Spring WebFlux (Reactor `Mono`/`Flux`) | tokio + futures crate stream | callback chain 없음. await는 sequential하게 읽힘. | 10장 |

## A.6 빌드·의존성·도구

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| Maven / Gradle | cargo | 언어 코어에 내장. 외부 도구 별도 조합 불필요. | 2·13장 |
| `pom.xml` / `build.gradle.kts` | `Cargo.toml` (TOML) | `[dependencies]` / `[dev-dependencies]` / `[features]` | 2장 |
| Maven Central | crates.io | semver 표기 (`"1.2"` = `>=1.2, <2.0`). | 2장 |
| sdkman java | rustup toolchain | toolchain 전환 한 줄. `rust-toolchain.toml`로 프로젝트별 고정. | 2장 |
| Gradle multi-module | cargo workspace | `[workspace]` 한 절로 묶음. | 13장 |
| `mvn clean package` / `gradle build` | `cargo build` (`--release`) | 디폴트는 debug, `--release`로 최적화. | 2장 |
| `mvn dependency:tree` | `cargo tree` | 의존 그래프 시각화. | 2장 |
| Spotless / google-java-format | `cargo fmt` (rustfmt) | 한 줄 명령. | 2·13장 |
| SpotBugs / Sonar | `cargo clippy` | 100여 lint 카테고리. `-D warnings`로 CI 게이트. | 13장 |
| OWASP Dependency Check / Snyk | `cargo audit` (RustSec) | 취약점 DB 조회. | 13장 |
| Gradle build cache | sccache | 컴파일 결과 캐시. | 13장 |

## A.7 테스트·품질

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| JUnit 5 | `cargo test` (`#[test]` / `#[cfg(test)]`) | 언어 코어 내장. 통합 테스트는 `tests/` 디렉터리. | 13장 |
| JavaDoc + 코드 예제 | doctest (` ```rust ... ``` `) | 주석 안 코드가 *자동 테스트*. | 13장 |
| Mockito | `mockall` crate | trait 기반. *trait + 더미 구현* 패턴이 더 자주 쓰임. | 13장 |
| JMH | criterion | 통계적 벤치마크. warm-up + outlier 처리 + HTML 리포트. | 13장 |
| AssertJ / Hamcrest | `assert_eq!` / `assert!` / `pretty_assertions` crate | 매크로 기반. | 13장 |
| Property-based testing (jqwik) | `proptest` / `quickcheck` | 입력 자동 생성. | 13장 |
| Snapshot testing (없음 in std) | `insta` crate | UI/JSON 스냅샷. | 13장 |
| JaCoCo (커버리지) | `cargo tarpaulin` / `cargo llvm-cov` | LLVM coverage 인스트루멘테이션. | 13장 |

## A.8 웹 프레임워크

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| Spring Boot | axum + tokio (또는 loco-rs) | DI는 *State<T>* 타입 기반. *컴파일 타임 검증*. | 11장 |
| `@RestController` | (없음 — 함수가 곧 핸들러) | 핸들러는 그저 async 함수. | 11장 |
| `@GetMapping("/users/{id}")` | `Router::new().route("/users/:id", get(handler))` | 라우팅이 *코드*로 표현. | 11장 |
| `@PathVariable Long id` | `Path(id): Path<i64>` (extractor) | extractor가 *타입 기반 시그니처*. | 11장 |
| `@RequestBody User u` | `Json(user): Json<User>` | serde로 자동 직렬화. | 11장 |
| `@Autowired Service s` | `State(state): State<AppState>` | *컴파일 타임 검증*. | 11장 |
| `Filter` / `HandlerInterceptor` / `@Aspect` | tower `Layer` (`Service<Request>` 트레잇) | 한 모델로 통일. axum/tonic/hyper/reqwest 공유. | 11장 |
| `ResponseEntity<T>` | `Result<Json<T>, AppError>` | `IntoResponse` 트레잇 구현으로 응답 변환. | 11장 |
| Tomcat / Netty | hyper (axum 내장) | HTTP/1.1·HTTP/2·HTTP/3. | 11장 |
| `application.properties` / `application.yml` | `config` crate / `figment` / `clap` env | 표준이 없음. crate 선택. | 11·13장 |

## A.9 데이터베이스

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| JDBC | sqlx (raw SQL + 컴파일 타임 검증) | `sqlx::query!`가 *빌드 시점에 DB 접속*해 SQL 검증. | 12장 |
| MyBatis (XML / 매퍼) | sqlx (`query!` / `query_as!` 매크로) | XML 대신 매크로로 SQL 직접 작성. | 12장 |
| Spring Data JPA / Hibernate | sea-orm (Active Record, async) | Entity·ActiveModel·find_by_id/save. loco-rs 기본 ORM. | 12장 |
| QueryDSL / jOOQ | diesel (타입 기반 query DSL) | 가장 *type-safe*. 컴파일 타임 SQL 생성. | 12장 |
| Flyway / Liquibase | `sqlx-cli` / `sea-orm-cli` / `diesel migration` | 마이그레이션 파일 + 버전 관리. | 12장 |
| `@Transactional` (AOP proxy) | `pool.begin().await?` → `tx.commit().await?` | 트랜잭션 경계가 *코드의 한 줄*. self-invocation 함정 없음. | 12장 |
| HikariCP (커넥션 풀) | `sqlx::PgPool` / `sea_orm::DatabaseConnection` | crate 내장. | 12장 |
| MyBatis Generator | `cargo sqlx prepare` (offline 모드) | `.sqlx/` 메타데이터로 CI에서 DB 없이 빌드. | 12장 |

## A.10 관측·운영·배포

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| SLF4J + Logback | `tracing` + `tracing-subscriber` | structured logging이 *기본*. 매크로(`info!`, `error!`). | 14장 |
| Spring Cloud Sleuth | `tracing-opentelemetry` | OTLP exporter로 Jaeger/Tempo/Datadog 전송. | 14장 |
| Micrometer | `metrics` crate / `prometheus` crate | 카운터·게이지·히스토그램. | 14장 |
| Async Profiler / JFR | `cargo flamegraph` (perf 기반) | flamegraph SVG 자동 생성. | 14장 |
| VisualVM (스레드 덤프) | `tokio-console` (async task) | async task의 *대기 위치*를 실시간으로. | 14장 |
| jlink + alpine-jre 이미지 (50~80MB) | musl + distroless 이미지 (8~10MB) | 정적 바이너리 + scratch/distroless. | 14장 |
| GraalVM Native Image | `cargo build --release --target ...-musl` | Rust는 처음부터 그 길로 설계. reflection 깨짐 없음. | 14장 |
| Spring Boot Actuator (헬스체크) | tower middleware + axum route | `/health` 엔드포인트 직접 작성. | 14장 |
| `kill -TERM` → graceful shutdown | tokio signal + `axum::Server::with_graceful_shutdown` | in-flight 요청 마무리. | 14장 |
| JNI (Java → Native) | `jni` crate / Project Panama (Java 22+) | 8장 unsafe + 15장 `#[no_mangle] pub extern "system" fn`. | 8·15장 |

---

표 한 장만 펴 놓고도 *오늘 출근해서 axum + sqlx로 작은 핸들러 한 개*는 짤 수 있는 모양이 됐을 것이다. 깊이가 부족하면 본문의 해당 절을 한 번 더 펴자. 매핑이 *비슷해 보이지만 시점이 다른 자리*가 가장 자주 발이 걸리는 곳이다 — 그때마다 *결정적 차이* 열을 함께 보자.
