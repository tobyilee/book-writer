# 챕터 2. 첫 만남 — cargo로 5분 만에 빌드하기

새 언어를 배울 때 가장 먼저 부딪히는 벽이 무엇일까? 문법이 아니다. *환경 구성*이다. 회사에서 새 프로젝트를 시작할 때를 떠올려보자. JDK 버전을 깔고, IntelliJ를 깔고, Maven 또는 Gradle을 설정하고, `pom.xml`이나 `build.gradle.kts`를 채우고, 코드 포매터(Spotless, google-java-format)를 붙이고, 정적 분석 도구(SpotBugs, Sonar)를 CI에 끼워 넣는다. *Hello World 한 줄*을 화면에 띄우기까지 한나절이 가는 일이 흔하다. 처음 학습할 때 가장 사기를 떨어뜨리는 게 바로 이 *세팅의 늪*이다.

그렇다면 Rust는 어떨까? 다행스럽게도 *완전히 반대편*에 있다. 도구 한 개로 끝난다. 이름이 cargo다. 이 챕터에서는 cargo로 첫 바이너리를 빌드하는 데까지 걸리는 시간이 정말로 *5분*이라는 것을 손으로 확인해보자. 그리고 그 5분 사이에 Maven/Gradle/Sonar/JMH/picocli/Spotless가 한 도구 안에 어떻게 들어와 있는지를 같이 알아보자.

## rustup — sdkman의 감각으로 toolchain을 다루자

먼저 Rust 자체를 깔아야 한다. 자바 진영에서 sdkman을 써본 적이 있는가? 여러 JDK 버전을 한 명령으로 전환하는 그 도구다. Rust에서 그 역할을 하는 게 rustup이다. rustup은 *toolchain manager* — 즉 컴파일러(rustc)와 표준 라이브러리, cargo, rustfmt, clippy 같은 도구 묶음을 버전별로 설치·전환하는 매니저다.

설치는 한 줄이다. macOS나 Linux라면 다음 명령을 셸에 붙여넣자.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

윈도우는 [rustup.rs](https://rustup.rs/)에서 인스톨러를 받으면 된다. 설치가 끝나면 `~/.cargo/bin`이 PATH에 들어간다. 셸을 새로 열거나 `source ~/.cargo/env`로 환경을 적용한 뒤 확인해보자.

```bash
$ rustc --version
rustc 1.83.0 (90b35a623 2025-11-26)
$ cargo --version
cargo 1.83.0 (5ffbef321 2025-10-29)
```

이 두 줄이 떴다면 Rust 환경은 이미 끝났다. JDK 설치 후 `JAVA_HOME`을 잡고 IntelliJ에서 SDK를 등록하던 그 모든 절차가 *한 명령*으로 끝났다. *조금 허무할 정도다*.

toolchain 채널은 세 가지가 있다. *stable*(6주마다 정식 릴리즈), *beta*(다음 stable 후보), *nightly*(매일 빌드, 실험적 기능 활성화). 처음 시작하는 우리에게는 stable이 답이다. 일부 라이브러리(특히 임베디드, 컴파일러 플러그인)는 nightly 기능을 요구하기도 하는데, 그땐 다음처럼 채널을 토글한다.

```bash
$ rustup toolchain install nightly
$ rustup default stable          # 디폴트는 stable로 두자
$ rustup run nightly cargo build # 가끔 nightly가 필요할 때만
```

프로젝트 디렉터리에 `rust-toolchain.toml` 파일 하나를 두면 그 폴더에서는 자동으로 정해진 toolchain이 쓰인다.

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.83.0"
components = ["rustfmt", "clippy"]
```

이 파일이 sdkman의 `.sdkmanrc`처럼 *"이 프로젝트는 이 버전으로 빌드한다"*는 약속을 코드 옆에 박아둔다. 신규 멤버가 합류해도 `cargo build` 한 번이면 똑같은 toolchain이 자동으로 설치된다. Maven/Gradle wrapper의 `mvnw`/`gradlew`가 하는 일을 *언어 레벨*에서 처리한다고 생각하면 이해하기 쉽다.

## cargo new — 5분의 시작

이제 본격적으로 첫 프로젝트를 만들어보자. 작업 디렉터리에서 다음을 친다.

```bash
$ cargo new hello-jvm
     Created binary (application) `hello-jvm` package
$ cd hello-jvm
$ tree -a
.
├── .git
├── .gitignore
├── Cargo.toml
└── src
    └── main.rs
```

이게 끝이다. Maven archetype으로 새 프로젝트를 뽑을 때 디렉터리 트리가 한 화면을 채우던 풍경과 비교해보자. *눈물이 날 정도로 단순하다*. 그리고 `git init`까지 알아서 해준다. `.gitignore`에 `/target`이 이미 들어 있다(target은 cargo가 빌드 산출물을 떨어뜨리는 폴더, Maven의 `target/`이나 Gradle의 `build/`와 같다).

`src/main.rs`를 열어보자.

```rust
fn main() {
    println!("Hello, world!");
}
```

이게 자동 생성된 본문 전부다. 한번 돌려보자.

```bash
$ cargo run
   Compiling hello-jvm v0.1.0 (/path/to/hello-jvm)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello-jvm`
Hello, world!
```

여기까지 걸린 시간이 *얼마나 됐는지* 시계를 한번 보자. rustup 설치 1~2분, `cargo new`와 `cargo run`이 1분 이내. 5분이라는 약속이 결코 과장이 아니다.

본문을 살짝 바꿔보자. JVM 출신답게 `"Hello, JVM"`을 외쳐보자.

```rust
fn main() {
    let runtime = "JVM";
    println!("Hello, {runtime}! Now we have one more weapon: Rust.");
}
```

다시 `cargo run`을 친다.

```
Hello, JVM! Now we have one more weapon: Rust.
```

이 한 문장이 곧 이 책 전체의 메시지다. *"JVM을 떠나는 게 아니라, 무기를 하나 더 얹는다."*

## Cargo.toml을 한 줄씩 해부해보자

자동 생성된 `Cargo.toml`을 열어보자.

```toml
[package]
name = "hello-jvm"
version = "0.1.0"
edition = "2024"

[dependencies]
```

짧다. 그런데 이 짧은 파일이 `pom.xml` 또는 `build.gradle.kts`가 하던 일의 *대부분*을 한다. 한 줄씩 보자.

`[package]` 섹션은 메타데이터다. `name`, `version`은 Maven의 `artifactId`, `version`과 의미가 같다. 그룹id에 해당하는 *namespace는 없다*. crates.io에서는 이름이 globally unique이기 때문이다. 그래서 처음 라이브러리를 출판할 때는 *이름 선점 전쟁*이 살짝 벌어지기도 한다(이 점이 Maven Central의 그룹id 모델과 가장 다른 부분이다).

`edition`은 *Rust 언어 자체의 호환성 묶음*이다. 2015 / 2018 / 2021 / 2024 네 개가 있고, edition을 올리면 새 키워드(`async`, `dyn` 등의 의미 변화)가 활성화된다. JVM에 비유하자면 `pom.xml`의 `<source>21</source>`/`<target>21</target>`에 가까운 개념인데, *언어 호환성 정책*이 더 명시적이다. 새 프로젝트는 가장 최신 edition을 쓰는 편이 낫다.

`[dependencies]` 섹션이 비어있다. 의존성이 없는 상태다. 한번 채워보자. CLI 인자를 파싱하는 라이브러리 `clap`을 추가해보자.

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
```

이게 Maven의 `<dependency>` XML 다섯 줄이 하던 일이다. `version = "4"`는 semver(semantic versioning)로 *4.x.y 중 호환되는 최신*을 뜻한다. Cargo는 semver를 매우 강하게 따른다. 메이저 버전이 다르면 *별개의 라이브러리로 취급*해서 한 그래프 안에 동시에 넣어준다(JVM 진영에서 이걸 못 해서 발생하는 *jar hell*과 가장 큰 차이점). `features`는 그 라이브러리의 *옵션 기능*을 켠다는 뜻인데, 잠시 후에 더 다룬다.

`Cargo.toml`을 저장한 뒤 다시 `cargo build`를 친다.

```bash
$ cargo build
    Updating crates.io index
  Downloaded clap v4.5.20
  Downloaded clap_derive v4.5.18
  ... (여러 개)
   Compiling proc-macro2 v1.0.92
   Compiling quote v1.0.37
   Compiling syn v2.0.90
   ...
   Compiling clap v4.5.20
   Compiling hello-jvm v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 12.34s
```

전이 의존성이 자동으로 받아진다. `crates.io`에서 다운로드해서 `target/`에 빌드하고, 우리 프로젝트와 링크한다. Maven Central에서 jar를 받아 `~/.m2/repository`에 캐시하던 그 흐름과 같다. cargo는 `~/.cargo/registry`에 같은 일을 한다.

빌드 산출물을 보자.

```bash
$ ls target/debug/hello-jvm
target/debug/hello-jvm
$ file target/debug/hello-jvm
target/debug/hello-jvm: Mach-O 64-bit executable arm64
```

*하나의 정적 바이너리*다. JAR 파일이 아니라 *OS가 직접 실행하는 실행 파일*이다. 이 점이 운영에서 가장 큰 차이를 만든다(자세한 것은 14장에서 본다). 지금은 그저 *"실행 파일이 한 개로 떨어진다"*는 사실만 손에 묻혀두자.

## semver와 feature flag — 의존성 관리의 두 핵심

`clap = { version = "4", features = ["derive"] }`라고 적은 한 줄을 좀 더 깊게 보자.

semver 표기는 다음 네 가지가 자주 쓰인다.

```toml
clap = "4.5.20"           # 4.5.20과 호환되는(>=4.5.20, <5.0.0) 모든 버전
clap = "=4.5.20"          # 정확히 4.5.20만
clap = "^4.5.20"          # "4.5.20"과 동일 (캐럿이 디폴트)
clap = "~4.5.20"          # 4.5.x만 (4.6은 거부)
```

Maven/Gradle에서 `4.5.20`이라고 쓰면 *그 버전만* 받지만, Cargo의 `4.5.20`은 *4.x 호환 범위*를 의미한다. 기본 가정이 정반대다. *처음에 가장 많이 헷갈리는 지점*이다. 정확한 버전 고정이 필요하면 `=4.5.20`을 명시해야 한다. 다만 *실제로는 신경 쓸 필요가 거의 없다*. cargo가 `Cargo.lock` 파일에 *실제 빌드된 정확한 버전*을 박아두기 때문이다(Gradle의 `gradle.lockfile`과 같은 역할). 신규 멤버가 같은 lock으로 빌드하면 같은 버전이 깔린다.

`features`는 *코드 레벨의 conditional compile*이다. 이 점이 Maven profile이나 Gradle variant와 결정적으로 다르다. Maven profile은 *어떤 모듈을 빌드에 포함할지*를 고르는 정도지만, Cargo feature는 *라이브러리 내부의 어떤 코드 경로를 컴파일할지*를 토글한다. 예를 들어 `clap`의 `derive` feature를 끄면 `#[derive(Parser)]` 같은 매크로 지원 코드가 *통째로 바이너리에서 빠진다*. 결과: 바이너리가 작아지고 컴파일도 빨라진다.

자기 라이브러리에서 feature를 정의할 수도 있다.

```toml
[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]
metrics = ["prometheus"]
```

코드에서는 다음처럼 분기한다.

```rust
#[cfg(feature = "postgres")]
mod postgres_repo;

#[cfg(feature = "mysql")]
mod mysql_repo;
```

*Maven profile이 어쩌다 한 번 손대는 그늘진 영역*이라면, Cargo feature는 *일상 도구*다. 다만 워크스페이스에서 같은 의존성이 다른 feature 조합으로 두 번 등장하면 *unification 함정*이 생긴다(13장에서 자세히 본다). 그때 `resolver = "2"`라는 한 줄이 처방인데, 새 프로젝트의 디폴트가 이미 `2`이므로 보통은 신경 쓸 필요가 없다.[^1]

## cargo의 일상 명령들 — 한 도구가 다 한다

cargo의 진짜 매력은 *개발 사이클의 모든 동작이 한 도구로 끝난다*는 점이다. 자주 쓰는 명령을 모아보자.

```bash
$ cargo new <name>                   # 새 binary 프로젝트
$ cargo new --lib <name>             # 새 library 프로젝트
$ cargo build                         # 디버그 빌드
$ cargo build --release              # 릴리즈 빌드 (최적화 on)
$ cargo run                           # 빌드 + 실행
$ cargo run -- arg1 arg2             # 인자 전달
$ cargo test                          # 모든 테스트 실행
$ cargo test some_function           # 이름 매칭 테스트만
$ cargo check                         # 컴파일 검증만 (실행 파일 X) — 빠르다
$ cargo clippy                        # 정적 분석 (린터)
$ cargo fmt                           # 포매터
$ cargo doc --open                    # 문서 빌드 + 브라우저로 열기
$ cargo bench                         # 벤치마크 (criterion 등 필요)
$ cargo update                         # 의존성 lock 갱신
$ cargo tree                          # 의존성 트리 출력
$ cargo install <crate>              # 글로벌 CLI 도구 설치
```

이 표를 가만히 보면 *충격적인 사실 하나*가 보인다. JVM 진영에서 `mvn` 또는 `gradle`로 빌드를 하고, IntelliJ에서 테스트를 돌리고, JaCoCo로 커버리지를 재고, Spotless로 포매팅을 하고, SpotBugs/Sonar로 정적 분석을 하고, JMH로 벤치마크를 하고, JavaDoc으로 문서를 만들고, picocli로 CLI를 짜고, OWASP Dependency Check으로 취약점을 스캔하던 *그 모든 도구*가 cargo 한 곳에 모여 있다.

물론 cargo 안에 들어 있지 않은 일도 있다(예: 컨테이너 이미지 빌드). 하지만 *언어와 가장 가까운 영역*은 거의 다 cargo가 안고 있다. 신규 멤버가 합류했을 때 *"우리 회사는 어떤 도구를 쓰나요?"*라는 질문이 *없다*. 답이 그냥 *"cargo"*다. 이게 *체감으로 가장 큰 차이*다.

자주 잊지 말아야 할 명령 하나가 `cargo check`다. *컴파일 가능성만 검증하고 실행 파일은 만들지 않는* 명령인데, *cargo build보다 훨씬 빠르다*. IDE의 rust-analyzer가 매번 백그라운드에서 돌리는 게 사실 `cargo check`다. 코드를 짜면서 *"이게 컴파일되나?"*만 확인하고 싶을 때 자주 쓰는 편이 낫다.

## workspace 미리보기 — Gradle multi-module의 감각

이 책의 후반부에서는 한 프로젝트를 *여러 crate로 쪼개는* 패턴을 자주 본다(13장에서 본격적으로 다룬다). 이걸 cargo에서는 *workspace*라고 부른다. 미리 한 번만 모양을 봐두자.

```
my-service/
├── Cargo.toml          # 워크스페이스 루트
├── crates/
│   ├── domain/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── infra/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   └── web/
│       ├── Cargo.toml
│       └── src/main.rs
└── target/             # 모든 crate가 공유
```

루트 `Cargo.toml`은 다음처럼 쓴다.

```toml
[workspace]
resolver = "2"
members = ["crates/domain", "crates/infra", "crates/web"]

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

각 멤버 crate의 `Cargo.toml`에서는 다음처럼 부모 워크스페이스의 의존성을 *상속*한다.

```toml
[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
domain = { path = "../domain" }
```

Gradle multi-module을 써본 사람이라면 패턴이 그대로 보일 것이다. 다만 *세팅이 한 줄로 끝난다*. `settings.gradle.kts` + `build.gradle.kts` × N + 버전 카탈로그를 짜던 일이 *Cargo.toml 몇 줄*이 된다. 이 단순함이 cargo의 진짜 매력이다.[^2]

지금 단계에서는 *"이런 모양이 가능하다"* 정도만 손에 담아두자. 13장에서 axum + sqlx 서비스를 도메인/인프라/웹 crate로 쪼갤 때 다시 펼친다.

## IDE 셋업 — 세 가지 선택지

코드를 손으로 짜기 시작하기 전에 IDE 환경을 한 번만 정리하자. 선택지는 셋이다.

**VSCode + rust-analyzer.** 가장 가볍고, 가장 활발히 발전 중이다. VSCode 마켓플레이스에서 `rust-analyzer` 확장을 설치하면 끝이다. *내 추천*은 처음 시작하는 사람에게 이쪽이다. rust-analyzer가 *백그라운드에서 cargo check를 돌리며* 실시간으로 에러·경고를 보여준다. type inline hint(타입을 추론한 결과를 회색으로 표시)와 *enum match exhaustiveness*도 즉시 잡아준다. 무료다.

**RustRover (JetBrains).** IntelliJ에 익숙한 사람에게 가장 친근한 선택. 별도 IDE로 분리됐다(과거엔 IntelliJ Rust 플러그인이었다). 디버거 통합이 가장 매끈하고, refactoring·navigation의 깊이가 깊다. JetBrains 라이센스가 있다면 첫 후보다.

**IntelliJ IDEA + Rust 플러그인.** 위와 비슷하지만 IDEA 본체에 얹는 형태. 이미 IDEA를 메인으로 쓰는 사람에게 자연스럽다.

어떤 IDE를 쓰든 *공통적으로* 한 번에 켜두면 좋은 것이 있다. *저장 시 자동 포매팅*과 *clippy 경고 표시*다. VSCode라면 settings.json에 다음을 넣자.

```json
{
  "rust-analyzer.checkOnSave.command": "clippy",
  "[rust]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "rust-lang.rust-analyzer"
  }
}
```

이 두 줄이 *지속 가능한 코드 품질*의 시작점이다. clippy가 보여주는 경고를 실시간으로 보면서 짜면, *처음 한 달*의 코드 품질이 비약적으로 좋아진다. 일종의 *친절한 시니어 페어*가 옆에 앉아 있는 셈이다.

## 사전 커밋 훅 — 팀 합류 첫날의 약속

마지막으로 한 가지 권하고 싶은 게 있다. *사전 커밋 훅*이다. 새로 합류한 팀원의 코드가 빌드를 망가뜨리거나, 포맷이 어긋나거나, clippy 경고가 잔뜩 들어오는 일을 *원천 차단*하는 장치다. JVM 진영에서 husky + lint-staged나 pre-commit framework를 써본 사람이라면 익숙할 것이다.

가장 단순한 형태는 `.git/hooks/pre-commit`에 다음 한 줄을 넣는 것이다.

```bash
#!/bin/bash
set -e
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

`-D warnings`는 *clippy의 경고를 에러로 격상*시킨다. 즉 경고가 한 개라도 있으면 빌드가 깨진다. 처음엔 답답하게 느껴질 수 있지만, *깨끗한 코드베이스를 유지하는 가장 단순한 처방*이다. 이 동일한 명령을 CI에서도 똑같이 돌리면, *"내 머신에선 되는데"*라는 익숙한 변명이 사라진다.

팀 단위로는 [pre-commit framework](https://pre-commit.com/) 또는 cargo의 `.cargo/config.toml`로 좀 더 정교하게 관리할 수 있다. 다만 처음에는 위의 세 줄짜리 훅으로 충분하다. *기억해두자. 처음 한 달의 풍경을 만드는 건 이 작은 훅 하나다.*

## crates.io — Maven Central의 자리

마지막으로 *어디서 라이브러리를 찾는가*를 짧게 짚어두자. Maven Central에 해당하는 게 [crates.io](https://crates.io/)다. 검색하면 다운로드 수, 최근 업데이트, README, dependents가 한 화면에 보인다. 살펴볼 만한 핵심 라이브러리들의 위치만 미리 알아두자.

- **tokio** — 비동기 런타임 (10장).
- **axum** — HTTP 프레임워크 (11장).
- **sqlx / sea-orm / diesel** — 데이터베이스 (12장).
- **serde / serde_json** — 직렬화 (어디서나).
- **tracing / tracing-subscriber / tracing-opentelemetry** — 관측 (14장).
- **anyhow / thiserror** — 에러 처리 (7장).
- **clap** — CLI 인자 파싱 (방금 설치).
- **reqwest** — HTTP 클라이언트.

이 정도가 Spring 백엔드의 *기본 스타터 묶음*에 해당한다고 보면 된다. *Spring Boot starter 한 줄로 끝나던 세계*와 비교하면 *직접 골라야 한다*는 부담이 있긴 하다. 하지만 그만큼 *어떤 도구를 왜 골랐는지가 코드에 남는다*. 처음엔 번거롭다. 두 달 뒤엔 *그 명시성이 운영을 살린다*.

[crates.io](https://crates.io/)와 함께 [lib.rs](https://lib.rs/), [docs.rs](https://docs.rs/)도 자주 쓴다. lib.rs는 카테고리별 큐레이션이 잘 된 미러이고, docs.rs는 *모든 crate의 문서를 자동으로 호스팅*한다. URL 패턴이 `docs.rs/{crate-name}` 한 줄로 일관돼 있다. 라이브러리 문서를 찾을 때 가장 빠른 진입점이다.

## 마무리 — 5분의 약속이 지켜졌다

이 챕터에서 한 일을 한 줄로 정리해보자. *rustup으로 toolchain을 깔고, cargo new로 프로젝트를 만들고, Cargo.toml에 의존성을 추가하고, cargo run으로 첫 바이너리를 실행했다.* 5분이라는 약속은 정직하게 지켜진 셈이다. 그리고 그 5분 사이에 cargo가 Maven, Gradle, Sonar, Spotless, JMH, picocli, JavaDoc, OWASP Dependency Check를 *모두 안고 있다*는 사실을 손에 묻혔다.

기억해두자. cargo의 진짜 매력은 단순함 그 자체가 아니다. *팀 전체가 같은 도구로 같은 절차를 따른다*는 일관성이다. 신규 멤버 합류, CI 셋업, 새 프로젝트 시작, 이 모두가 *같은 cargo 명령*으로 끝난다. 십 년 동안 Maven plugin 모음·Gradle convention plugin·Spotless config·sonar-project.properties를 회사마다 다르게 짜왔던 우리 입장에서는 *조금 어이없을 정도로 단순하다*.

다만 이 단순함이 *Rust의 학습 곡선까지 단순하게* 만들어주지는 않는다. 환경이 단순하다고 *언어가 쉬운 건 아니다*. 다음 챕터에서 곧바로 그 사실을 손으로 확인하게 된다. 변수 선언 한 줄, 함수 시그니처 하나, 모듈 가시성 한 단어가 *Java가 알던 모양과 미묘하게 다르다*. 그 미묘한 차이가 4장의 소유권으로 이어지는 다리다.

## 함께 해보자

방금 만든 `hello-jvm` 프로젝트를 한 단계 키워보자. 인자 한 개를 받아 인사하는 작은 CLI다. `Cargo.toml`은 이미 `clap`을 추가해뒀다.

`src/main.rs`를 다음처럼 바꿔보자.

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "hello-jvm", about = "JVM 출신을 환영합니다")]
struct Args {
    /// 인사할 대상의 이름
    #[arg(short, long, default_value = "JVM 개발자")]
    name: String,

    /// 인사 횟수
    #[arg(short, long, default_value_t = 1)]
    count: u8,
}

fn main() {
    let args = Args::parse();
    for _ in 0..args.count {
        println!("Hello, {}! Now we have one more weapon: Rust.", args.name);
    }
}
```

빌드와 실행은 다음 한 줄이다.

```bash
$ cargo run -- --name "Spring 개발자" --count 3
   Compiling hello-jvm v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 3.21s
     Running `target/debug/hello-jvm --name 'Spring 개발자' --count 3`
Hello, Spring 개발자! Now we have one more weapon: Rust.
Hello, Spring 개발자! Now we have one more weapon: Rust.
Hello, Spring 개발자! Now we have one more weapon: Rust.
```

이 작은 CLI에서 다음 세 가지를 손으로 확인해보자.

1. `cargo run -- --help`를 쳐보자. clap이 *자동으로 도움말을 생성*한다. picocli나 Spring Shell의 그것과 비교해보자.
2. `cargo build --release`로 릴리즈 빌드를 만들어 `target/release/hello-jvm`의 *파일 크기*를 재보자. JAR 파일 크기와 비교해보자(JVM은 JRE까지 포함하면 200MB대다).
3. `Cargo.toml`의 `clap = { version = "4", features = ["derive"] }`에서 `features = ["derive"]`를 지운 뒤 `cargo build`를 시도해보자. 어떤 에러가 나는가? 그 에러를 가만히 읽어보자. *cargo의 에러 메시지가 친절하다는 사실*도 같이 묻혀두자.

이 작은 CLI는 *13장의 clap 절*에서 다시 호출되어 *완성형*으로 키워진다. subcommand, env var, completion script까지 붙여본다.

다음 장에서는 코드 자체의 모양을 정면으로 본다. `let`/`let mut`은 `val`/`var`과 어떻게 다르고, `match`는 Java 17의 switch expression과 어디가 다르며, `String`과 `&str`이 *왜 두 개*인가 — Java가 알던 모양과 살짝씩 어긋난 부분들을 같이 살펴보자.

---

## 참고

[^1]: ["Cargo Workspaces" — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html); ["cargo-features2 RFC"](https://rust-lang.github.io/rfcs/2957-cargo-features2.html); ["Cargo Workspace and the Feature Unification Pitfall" — nickb.dev](https://nickb.dev/blog/cargo-workspace-and-the-feature-unification-pitfall/).
[^2]: ["Workspaces" — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html).

---
