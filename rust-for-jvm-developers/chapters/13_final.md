# 13장. 테스트·품질·도구 인프라·CLI — cargo가 IDE·Sonar·JMH·picocli·OWASP를 모두 안고 있다

12장까지 따라온 자네에게 자기 회사 백엔드의 빌드 파이프라인을 한 장에 그려보라고 하면, 아마 대여섯 줄 정도는 우습게 나올 것이다. JUnit과 Mockito가 한 줄, JaCoCo가 한 줄, Spotless 또는 google-java-format이 한 줄, SpotBugs와 Sonar가 한 줄, JMH가 한 줄, OWASP Dependency Check 또는 Snyk가 한 줄, picocli나 Spring Shell이 한 줄. Spring Boot 본체는 그 위에 또 한 층이다. 신규 멤버가 들어오면 *이 도구들이 왜 이 자리에 있는지*를 한 시간씩 설명해야 하고, *플러그인 버전이 안 맞으면* 빌드가 통째로 무너진다. 익숙하지만 솔직히 *번거롭다*. 그리고 가끔은 *피곤하다*.

그렇다면 Rust는 어떨까? cargo 한 도구가 위 목록 거의 전부를 *언어 코어 안에서* 안고 있다. 외부 도구는 보강만 한다. 신규 멤버 onboarding이 *체감으로* 다르다. 이 챕터는 cargo가 어디까지 안고 있는지를 한 줄씩 정리하면서, 길어진 컴파일 시간을 어떻게 다스리는지, 보안 게이트를 CI에 어떻게 박는지, 그리고 *내 첫 매크로*는 어떻게 짜는지까지 손에 묻혀보려 한다. 함께 살펴보자.

## cargo test와 doctest — JUnit이 언어 코어로 들어왔을 때

JUnit은 외부 라이브러리다. JUnit 4와 JUnit 5의 어노테이션이 다르고, Surefire/Failsafe 플러그인 버전이 안 맞으면 통합 테스트가 안 돈다. Rust의 단위 테스트는 *언어 코어*다. 모듈 안에 한 블록이 들어갈 뿐이다.

```rust
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds_two_numbers() {
        assert_eq!(add(2, 3), 5);
    }
}
```

`cargo test` 한 줄이면 끝난다. `#[cfg(test)]`가 붙은 모듈은 release 빌드에 포함되지 않으므로, *프로덕션 바이너리에 테스트 코드가 섞여 들어가는 일*이 구조적으로 없다. 통합 테스트는 crate 루트의 `tests/` 디렉터리에 별도 파일로 둔다. JUnit이 `src/test/java`로 분리되는 것과 같은 발상이지만, *Maven Surefire 같은 플러그인 없이* 그냥 디렉터리 규약 하나로 끝난다.

여기까지는 JUnit과 도긴개긴이다. doctest로 가면 이야기가 달라진다. JavaDoc에 `@code` 블록을 적으면 *문서로만* 남는다. 거기 적힌 예제가 다음 릴리스에서도 컴파일되는지는 *아무도 보장해주지 않는다*. 그래서 우리는 README의 예제 코드가 깨진 것을 PR 리뷰에서 발견하고 *찜찜한 한숨*을 쉬곤 한다. Rust의 doctest는 그 찜찜함을 단번에 거둬간다.

```rust
/// 두 정수를 더한다.
///
/// # 예시
///
/// ```
/// use mycrate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}
```

`cargo test --doc`을 돌리면 주석 안의 ` ```rust ... ``` ` 블록이 *진짜로 컴파일되고 실행된다*. JavaDoc과 JUnit이 한 줄로 합쳐진 셈이다. *문서가 곧 살아있는 예제*가 된다는 표현은 빈말이 아니다. 한 번 익숙해지면, *문서의 예제가 빌드에서 깨지는 경험*이 *문서가 옳다는 증거*로 바뀐다. 이 감각은 손에 묻혀봐야 안다.

## mocking — "mock 없는 mocking"이라는 패턴

Spring 출신은 Mockito 없이 테스트를 짜본 기억이 별로 없을 것이다. `@MockBean`, `when().thenReturn()`, `verify()` — 거의 반사 신경처럼 손이 간다. Rust에도 mocking 라이브러리는 있다. `mockall`이 가장 널리 쓰인다. 트레잇에 `#[automock]`을 붙이면 mock 구현이 자동으로 생성된다.

그런데 Rust 커뮤니티에서 더 자주 권하는 패턴은 *mock이 없는 mocking*이다. 트레잇으로 의존성을 추상화하고, 테스트에서는 더미 구현체를 손으로 한 줄 끼워 넣는다.

```rust
trait Clock {
    fn now(&self) -> u64;
}

struct SystemClock;
impl Clock for SystemClock {
    fn now(&self) -> u64 { /* ... */ 0 }
}

struct FakeClock(u64);
impl Clock for FakeClock {
    fn now(&self) -> u64 { self.0 }
}
```

생각해보자. Mockito가 강력한 이유는 자바의 *모든 것이 객체*라는 전제와 *모든 메서드가 사실상 virtual*이라는 모델 위에서 *런타임에 동적 프록시*를 생성할 수 있기 때문이다. 그 강력함 뒤에 *프록시가 self-invocation을 못 잡는*다거나 *final 메서드를 mock 못 한다*는 함정이 따라붙는 것은 익숙한 이야기다. Rust는 다른 길을 골랐다. *의존성을 명시적으로 주입*하는 코드가 자연스러우니, *mock도 명시적인 한 줄*로 충분해진다는 발상이다. 처음에는 *번거롭게* 느껴지지만, 한 달쯤 익숙해지면 *코드가 더 솔직해졌다*는 감각이 든다. 어떤 패턴을 고를지는 팀의 취향이지만, *Mockito 없이도 충분하다*는 사실은 알아두자.

## clippy와 rustfmt — Sonar와 ktlint가 cargo 안에 들어왔을 때

Java 진영에서 코드 품질 도구를 처음 깐 날을 떠올려보자. SonarQube 서버를 세우고, 룰 셋을 고르고, SpotBugs/PMD/Checkstyle 가운데 무엇을 쓸지 합의하고, Maven 빌드에 플러그인을 끼우고, CI에서 결과를 게시할 채널을 정하고, *false positive 한 줄*을 어떻게 무시할지 룰까지 정한다. 한 분기는 잡아먹는다.

clippy는 그 일들을 cargo 한 줄로 끝낸다. `cargo clippy`다. 100개가 넘는 lint가 *correctness, suspicious, style, complexity, perf* 같은 카테고리로 묶여 있다. 입문자가 가장 빨리 *좋은 Rust 코드*로 가는 길은 clippy가 시키는 대로 따라가는 것이다. CI에서는 한 단계 더 강하게, `cargo clippy -- -D warnings`로 *경고를 에러로 승격*시킨다.

```bash
cargo clippy -- -D warnings
```

처음에는 빨간 메시지가 페이지 단위로 쏟아져 *난감하다*고 느낄 수 있다. 하지만 메시지 한 줄 한 줄이 *왜 이게 더 좋은지*를 설명한다. 그리고 거의 모든 메시지에 *수정 코드 예시*가 따라붙는다. 컴파일러가 스승이 되는 감각은 4장에서 borrow checker와 만났을 때 이미 한 번 겪었다. clippy는 그 스승의 *코드 리뷰 모드*다. 적이 아니라 동료(co-author)다.

rustfmt는 더 단순하다. ktlint와 google-java-format을 한 줄로 합친 것이다. `cargo fmt`. 끝이다. 팀에서 합의해야 할 것은 `rustfmt.toml`의 몇 줄이 전부다. 들여쓰기가 탭이냐 공백이냐로 한 시간 회의하던 시절이 *조금 멀어진다*.

## criterion — JMH가 cargo 한 도구 안에서 굴러간다

JMH(Java Microbenchmark Harness)를 한 번이라도 진지하게 써본 적이 있다면, *마이크로벤치는 정직하게 어렵다*는 사실을 알 것이다. JIT warmup, dead code elimination, false sharing, GC 잡음 — 한두 가지만 놓쳐도 *말도 안 되는 숫자*가 나온다. 그래서 JMH는 fork·warmup·measurement iteration·blackhole 같은 수단을 정성껏 쥐여준다.

Rust 생태계의 표준은 criterion이다. JMH의 정신을 거의 그대로 가져왔다.

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fib(n: u64) -> u64 {
    if n < 2 { n } else { fib(n - 1) + fib(n - 2) }
}

fn bench_fib(c: &mut Criterion) {
    c.bench_function("fib 20", |b| {
        b.iter(|| fib(black_box(20)))
    });
}

criterion_group!(benches, bench_fib);
criterion_main!(benches);
```

`cargo bench`로 돌리면 통계적으로 안정된 수치가 나오고, `target/criterion/` 아래에 *HTML 리포트*가 떨어진다. throughput, outlier 분석, 이전 측정과의 비교 그래프까지 그려준다. JMH 보고서를 별도 도구로 시각화하던 *번거로움*이 한 단계 줄어든다. JIT가 없는 Rust에서는 워밍업의 의미가 다르지만, *측정값을 신뢰하려면 통계가 필요하다*는 원리는 똑같다. 측정 없이 "이게 더 빠를 것이다"라고 말하는 습관이 줄어드는 것 — 그것이 criterion이 팀에 가져다주는 가장 큰 선물이다.

## cargo workspace — Gradle multi-module의 깔끔한 형제

12장의 axum + sqlx 서비스를 그대로 한 crate에 두고 굴리는 데는 한계가 빨리 온다. 도메인 로직, 인프라 어댑터(DB·외부 API), 웹 핸들러를 *같은 crate*에 두면 *컴파일 시간*과 *모듈 경계*가 동시에 무너진다. workspace로 쪼개야 할 시점이다. Gradle multi-module을 한 번이라도 써봤다면, 발상은 익숙하다.

```toml
# Cargo.toml (워크스페이스 루트)
[workspace]
resolver = "2"
members = [
    "crates/domain",
    "crates/infra",
    "crates/web",
]

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
sqlx  = { version = "0.8", features = ["postgres", "macros", "runtime-tokio"] }
```

각 멤버 crate의 `Cargo.toml`에서는 `tokio = { workspace = true }`처럼 한 줄로 가져다 쓴다. 버전 관리가 한 곳으로 모이는 감각은 Gradle의 `versions.toml`이나 BOM(Bill of Materials)과 결이 같다. *결정적 차이*가 한 가지 있다. Rust는 *멤버 crate들이 같은 의존성의 다른 feature*를 요구하면, 빌드 그래프 안에서 *하나의 컴파일 단위로 통합*해버린다. 이른바 *feature unification*이다. 한 crate에서 reqwest의 `rustls-tls` feature를 켜고, 다른 crate에서 `native-tls` feature를 켜면, 두 feature가 *모두 활성화*된 상태로 빌드된다. 의도치 않게 OpenSSL을 끌어들이는 사고로 이어지기도 한다. 그래서 워크스페이스를 만들 때 `resolver = "2"`를 명시하는 것이 *디폴트*다. 잊지 말자.

도메인 crate에 doctest를 한두 개 박아두면 *살아있는 명세*가 된다. 인프라 crate는 *외부 시스템 어댑터*만 두어 mock과 fake가 들어갈 자리를 비워두자. 웹 crate는 axum의 라우터·핸들러·State에 집중하고, 비즈니스 로직은 도메인 crate에 위임한다. *얼마나 얇게 쪼개야 적당한가?* 정답은 없지만, *서로 다른 사람이 다른 PR로 만질 자리*가 보이면 그 자리가 경계다.

## 컴파일 시간 — 27%가 가장 큰 불만으로 꼽은 영역

Rust로 한 달쯤 일해보면 누구나 한 번은 마주치는 한 줄 호소가 있다. *"5초 짜리 변경에 1분이 걸린다."* 2025 Rust Compiler Performance Survey에서 27%가 *가장 큰 불만*으로 컴파일 시간을 꼽았다. 솔직히 인정하자. Rust 컴파일러는 *많은 일을 한다*. borrow checker, monomorphization, LLVM 최적화 — 그래서 컴파일 시간이 길어지는 것은 *공짜로 받은 안전성*의 뒷면이다. 그래도 손쓸 수 있는 길은 여럿 있다. 처방을 단계별로 정리해보자.

첫째, **`cargo check`를 먼저 쓴다.** 코드 변경 직후 *진짜로 빌드까지 가야 할 때*는 의외로 적다. 타입 검사만 통과해도 80%의 안심은 얻는다. `cargo check`는 LLVM 최적화·코드 생성을 건너뛰므로 `cargo build`보다 한참 빠르다. IDE의 rust-analyzer가 사실상 백그라운드에서 같은 일을 한다.

둘째, **워크스페이스를 쪼갠다.** 한 crate가 너무 비대해지면, 한 줄 변경에 그 crate 전체의 의존 그래프가 다시 빌드된다. 도메인·인프라·웹으로 쪼개면 자주 만지는 자리만 다시 빌드된다. 모듈 경계가 *컴파일 단위로* 그대로 보상받는다.

셋째, **sccache로 빌드 캐시를 공유한다.** Mozilla가 만든 컴파일러 캐시다. 같은 입력에 대한 컴파일 결과를 *디스크 또는 S3*에 저장하고, CI 머신끼리도 공유할 수 있다. 환경 변수 한 줄로 켠다.

```bash
export RUSTC_WRAPPER=sccache
cargo build --release
```

넷째, **링커를 바꾼다.** macOS는 기본 링커가 빠른 편이지만, Linux의 기본 ld는 큰 바이너리에서 *링크 단계가 빌드 시간의 절반*을 차지하기도 한다. `mold` 또는 `lld`를 끼우면 링크가 *몇 배*로 빨라진다. `~/.cargo/config.toml`에 한 줄을 추가한다.

```toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```

다섯째, **dev 프로파일과 release 프로파일을 분리한다.** 개발 중에는 `codegen-units`를 키워(예: 256) 병렬화하고 LTO를 끈다. 배포 빌드에서만 `codegen-units = 1`, `lto = "thin"`을 켜서 최적화를 최대화한다. 개발 중인 한 시간을 위해 *프로덕션 수준의 최적화*를 매번 돌리는 것은 *낭비*다.

여섯째, **`cargo nextest`를 시도해보자.** cargo 표준 테스트 러너의 대안이다. 프로세스 분리·병렬화·격리가 더 공격적이라 큰 워크스페이스에서는 30~50% 빠르다는 보고가 흔하다.

이쯤에서 마음에 드는 한 가지를 골라 *오늘 당장* 적용해보자. 컴파일 시간 단축은 한 번 익숙해지면 *되돌아갈 수 없는 안락함*이다. 그리고 이 안락함은, 신규 멤버가 *대기 시간 때문에 흐름을 잃는 일*을 막아준다. 팀 차원의 생산성에 곧장 닿는다.

## 보안 도구 — `cargo audit`·`cargo deny`·`cargo vet`

Spring 출신은 OWASP Dependency Check, Snyk, FOSSA의 어딘가에 익숙할 것이다. 라이브러리 버전을 한 번 잘못 잡았다가 CVE가 한꺼번에 뜨면서 *식은땀*을 흘려본 기억도 있을 것이다. Rust는 이 영역도 cargo의 친척 도구로 안고 있다.

`cargo audit`는 RustSec Advisory DB를 조회해 *현재 의존성에 알려진 취약점이 있는지*를 빠르게 검사한다.

```bash
cargo install cargo-audit
cargo audit
```

CI에 한 줄로 끼우면 *취약한 의존성이 들어오는 순간 빌드가 깨진다*. 게시 직전이 아니라 PR 단계에서 잡힌다. OWASP Dependency Check를 처음 도입했을 때의 안도감이 *cargo install* 한 줄로 돌아온다.

`cargo deny`는 한 단계 더 넓다. 라이선스 정책, 출처(crates.io 외 git/path), 중복 의존성, 금지 crate를 한 파일에 선언적으로 적는다.

```toml
# deny.toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause"]
deny  = ["GPL-3.0"]

[bans]
multiple-versions = "warn"
```

조직의 *법무 정책을 코드로 박아두는* 감각이다. 사내 OSS 정책을 매번 PDF로 회람하던 *번거로움*이 줄어든다.

`cargo vet`는 *공급망 감사(supply chain audit)*에 쓴다. *어떤 사람이 어떤 crate의 어떤 버전을 검토했고, 안전하다고 서명했는가*를 워크스페이스에 기록한다. 큰 회사 단위에서 *서로의 감사 결과를 공유*할 수 있도록 설계되어 있다. Mozilla·Google이 자기네 워크스페이스에서 운영하는 vet 결과를 *공개*해 두기 때문에, 우리는 그 위에 *우리 회사 추가본*을 얹는 모양으로 가볍게 시작할 수 있다. 쉽게 말해 *체인지로그가 보안 감사로 진화*한 도구다.

CI 게이트는 보통 이 정도면 충분하다.

```bash
cargo fmt --check && \
cargo clippy -- -D warnings && \
cargo test && \
cargo audit && \
cargo deny check && \
cargo bench --no-run
```

여섯 줄이면 *포맷·정적 분석·테스트·취약점·정책·벤치 컴파일*이 한 번에 잡힌다. JVM 진영의 동등한 파이프라인을 떠올려보자. Maven 플러그인 여섯 개와 그 사이의 *버전 호환표*가 보일 것이다. 16장에서 다시 짚겠지만, *Rust 도입의 최소 조건*이 이 한 줄짜리 게이트다.

## clap — picocli와 Spring Shell이 한 라이브러리에 모이다

2장에서 만든 `hello-jvm` CLI를 기억하는가? `cargo new` 다음 줄에 `clap = { version = "4", features = ["derive"] }`를 끼워넣고 인자 한 개를 받았던 그 작은 프로그램. 이제 그 CLI를 완성형으로 다시 보자.

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "hello-jvm", version, about = "JVM 출신을 위한 첫 CLI")]
struct Cli {
    #[command(subcommand)]
    command: Cmd,
}

#[derive(Subcommand)]
enum Cmd {
    Hello {
        #[arg(short, long, env = "GREET_NAME", default_value = "Toby")]
        name: String,
    },
    Bench { iterations: u64 },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Cmd::Hello { name } => println!("Hello, {name}!"),
        Cmd::Bench { iterations } => {
            for i in 0..iterations { println!("iter {i}"); }
        }
    }
}
```

picocli를 써본 사람은 *한 줄이 한 줄로 대응*되는 모양이 익숙할 것이다. `#[derive(Parser)]`가 `@Command`고, `#[arg(short, long, env, default_value)]`가 `@Option`이다. subcommand·flag·env 변수·기본값이 한 라이브러리 안에서 깔끔하게 정리된다. cargo·ripgrep·bat·fd·exa의 친숙한 CLI 감각이 모두 clap 위에 있다. 셸 자동완성도 `clap_complete` 한 줄로 생성된다.

Spring Shell을 따로 끼워야 했던 *번거로움*이 사라진다. 작은 운영 도구를 만들 때 *별도 프레임워크를 골라야 하나*를 고민하지 않게 되는 것 — 이 가벼움이 cargo 생태계의 매력이다. 한 번 이 감각에 익숙해지면, *내 다음 사내 도구는 Rust + clap*이 자연스러워진다.

## 내 첫 매크로 — 작성도 할 수 있는 도구라는 사실

8장에서 매크로를 *호출하는* 모양으로 처음 만났다. `println!`, `vec!`, `#[derive(Debug, Clone, Serialize)]`이 매크로다. 그때 약속했던 한 가지가 있었다. *매크로는 작성도 할 수 있는 도구*라는 사실. 13장에서 그 약속을 갚자. 깊이 들어가지는 않는다. *어떻게 시작하는지*만 손에 묻혀보자.

먼저 declarative 매크로다. `macro_rules!`로 정의한다. *부동소수점 비교*에서 자주 필요한 `assert_close!`를 하나 짜보자.

```rust
#[macro_export]
macro_rules! assert_close {
    ($left:expr, $right:expr, $eps:expr $(,)?) => {{
        let l = $left;
        let r = $right;
        let e = $eps;
        if (l - r).abs() > e {
            panic!("assert_close 실패: |{l} - {r}| > {e}");
        }
    }};
}

#[test]
fn pi_is_close_to_three_point_one_four() {
    assert_close!(3.14159_f64, 3.14, 0.01);
}
```

`$left:expr`는 *표현식 한 덩어리*를 받는 fragment specifier다. `expr` 외에도 `ident`(식별자), `ty`(타입), `block`(블록), `pat`(패턴) 등이 있다. *문법 수준의 패턴 매칭*이다. 자바의 어노테이션 프로세서와 가장 큰 차이는, 매크로가 *실제 코드 토큰*으로 펼쳐진 뒤 *컴파일러가 다시 검사*한다는 점이다. 잘못 펼쳐지면 *그 자리에서 컴파일 에러*다. 마법이 적고 디버깅이 솔직하다.

펼쳐진 모양이 궁금하면 `cargo expand`를 쓰자.

```bash
cargo install cargo-expand
cargo expand --test mytest
```

자바 Lombok이 *바이트코드 단계*에서 일을 끝내 *디버깅 시점*에는 잘 안 보이는 데 비해, Rust의 매크로는 *언제든 펼쳐서 사람의 눈으로 읽을 수 있다*. 안심하고 쓸 수 있는 이유다.

다음은 procedural attribute 매크로다. 이쪽은 진짜로 *컴파일러 플러그인*에 가까운 도구다. 깊게 들어가면 한 챕터가 또 필요하니, 여기서는 *모양만* 보자. 별도 crate를 만들고 `proc-macro = true`로 선언한 뒤, `syn`으로 토큰을 파싱하고 `quote`로 코드를 만든다.

```rust
// my_macros/Cargo.toml
// [lib]
// proc-macro = true
//
// [dependencies]
// syn   = { version = "2", features = ["full"] }
// quote = "1"
// proc-macro2 = "1"

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn my_handler(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let func = parse_macro_input!(item as ItemFn);
    let name = &func.sig.ident;
    let body = &func.block;
    quote! {
        async fn #name() {
            tracing::info!("핸들러 진입: {}", stringify!(#name));
            #body
            tracing::info!("핸들러 종료: {}", stringify!(#name));
        }
    }.into()
}
```

호출하는 쪽은 그냥 `#[my_handler]`를 붙인다. axum 핸들러에 트레이스 로그를 자동으로 박는 식의 일이 가능해진다. Spring AOP의 `@Around`가 했던 일과 결이 비슷하지만, *런타임 프록시*가 아니라 *컴파일 타임 토큰 변환*이다. 그래서 *self-invocation 안 됨* 같은 함정이 없다.

여기까지가 첫 매크로다. 깊이는 다음 학습으로 미루자. 중요한 것은, *매크로가 작성도 할 수 있는 도구*라는 사실을 *손으로 한 번 만져봤다*는 경험이다. 그 경험이 있고 없고가, 다음에 마주칠 *복잡한 derive 매크로의 디버깅*에서 결정적 차이를 만든다.

## cargo 한 도구가 안고 있는 것 — JVM 대응표

여기까지 본 도구들을 한 표로 정리해두자. 책상 옆에 펴 놓고 보는 cheatsheet라고 생각하자.

| 영역 | Rust(cargo 또는 표준 crate) | JVM 대응물 |
|---|---|---|
| 단위 테스트 | `cargo test`, `#[test]` | JUnit 5 |
| 통합 테스트 | `tests/` 디렉터리 | JUnit + Surefire/Failsafe |
| 문서 + 테스트 통합 | doctest (`cargo test --doc`) | JavaDoc + 별도 JUnit |
| Mocking | `mockall`, trait 더미 구현 | Mockito |
| 정적 분석 | `cargo clippy` | SpotBugs + PMD + Sonar |
| 포매터 | `cargo fmt` | ktlint, google-java-format, Spotless |
| 벤치마크 | `cargo bench` + `criterion` | JMH |
| 코드 커버리지 | `cargo tarpaulin`, `cargo llvm-cov` | JaCoCo |
| 멀티모듈 빌드 | cargo workspace | Gradle multi-module, Maven 모듈 |
| 의존성 캐시 | `sccache` | Gradle build cache, Develocity |
| 취약점 스캔 | `cargo audit` | OWASP Dependency Check |
| 라이선스/정책 | `cargo deny` | FOSSA, Snyk Open Source |
| 공급망 감사 | `cargo vet` | (대응물 거의 없음 — Sigstore가 가장 가깝다) |
| CLI 인자 파싱 | `clap` | picocli + Spring Shell |
| 매크로/AOP | `macro_rules!`, proc-macro | Lombok + AspectJ |

JVM 칸의 도구 수를 세보자. 열다섯 줄에 *서로 다른 라이브러리·플러그인 이름이 스무 개 가까이* 들어간다. Rust 칸은 거의 *cargo와 그 형제 도구*다. *결정적 차이* 한 단락은 이렇다. JVM은 *언어 한 개에 도구 수십 개*를 조합하는 ecosystem 모델이고, Rust는 *cargo 한 도구가 핵심을 다 안고* 외부 도구는 *보강만* 한다. 신규 멤버 onboarding 시간이 *체감으로* 다르다는 말이 빈말이 아니다. 이 차이는 회사가 커져 *팀이 늘어날수록* 더 크게 느껴진다.

## 사전 커밋 훅과 CI — 한 줄짜리 게이트

마지막으로 권장 워크플로 한 줄을 적어두자. 회사의 첫 Rust 프로젝트에 *오늘 당장* 끼울 만한 모양이다.

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit  (또는 cargo-husky / lefthook 등으로 관리)
set -euo pipefail
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

CI 파이프라인은 여기에 보안과 벤치를 더한 한 줄이면 충분하다.

```bash
cargo fmt --check && \
cargo clippy --all-targets -- -D warnings && \
cargo test && \
cargo audit && \
cargo deny check && \
cargo bench --no-run
```

*벤치마크 자체*가 아니라 *컴파일만 검증*하는 `--no-run`이 핵심이다. 진짜 측정은 별도 머신에서 주기적으로 돌리는 편이 낫다. CI에서 매번 벤치를 돌리면 *결과가 흔들려* 의미가 빠르게 닳는다.

이 한 줄짜리 게이트가 자리잡으면, 자네 팀의 신규 멤버는 *첫 PR을 올리는 날* 게이트의 모든 단계를 *자동으로* 통과하게 된다. *코드 리뷰의 절반은 이미 끝나 있는* 셈이다. Rust의 도구 인프라가 주는 가장 큰 선물은 *속도*가 아니라 *합의 비용의 감소*다. 기억해두자.

## 마무리 — 함께 해보자

12장의 axum + sqlx 서비스를 도메인·인프라·웹 세 crate로 쪼개 cargo workspace로 묶어보자. 도메인 crate의 핵심 함수 하나에 doctest를 한 줄 붙여 `cargo test --doc`로 통과시켜 보고, 같은 함수에 criterion 벤치를 붙여 HTML 리포트를 한 번 열어보자. 그 옆에 CI 파이프라인을 한 줄짜리 셸 스크립트로 적어두고, `cargo audit`과 `cargo deny check`를 게이트로 끼워 *고의로 취약한 의존성*을 한 번 추가해 빌드가 깨지는 모습을 손으로 확인하자. 마지막으로 `assert_close!` 매크로를 직접 짜서 도메인 crate의 부동소수점 테스트에서 한 번 써보자. *(이 워크스페이스는 14장에서 musl + distroless로 빌드되어 한 자릿수 MB 컨테이너로 다시 호출되고, `cargo audit` 게이트는 16장에서 *조직 도입의 최소 조건*으로 다시 호출된다.)*

다음 14장에서는 그 워크스페이스를 *진짜로 출시*해보자. 8MB 컨테이너와 OpenTelemetry 관측이 기다리고 있다.

## 참고

- *cargo test*, doctest, criterion, clippy, rustfmt 워크플로 — reference 토픽 7
- 컴파일 시간 함정과 처방 — reference 함정 6, 2025 Rust Compiler Performance Survey
- `cargo audit` / `deny` / `vet` — reference 토픽 7 보강
- `clap` CLI — reference 토픽 10.1
- workspace와 feature unification 함정 — reference 토픽 6
