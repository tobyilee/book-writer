# 부록 B. cargo / rustup / clippy / rustfmt 치트시트

매일 손에 잡는 명령들을 한 페이지에 모았다. JVM 출신이 *gradle / mvn* 명령을 외워 쓰던 감각으로 *cargo* 명령을 손에 묻혀보자. 하나만 기억하면 된다 — *cargo가 거의 다 안고 있다*. 이 부록의 명령 99%는 cargo 한 도구 안에서 끝난다.

## B.1 rustup — toolchain 관리 (sdkman java의 감각)

rustup은 *Rust 자체를 깔고 버전을 전환하는 도구*다. 한 번 깔고 잊어도 되는 자리.

| 명령 | 의미 |
|---|---|
| `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` | Rust 첫 설치 (Linux/macOS) |
| `rustup update` | 최신 stable로 업데이트 |
| `rustup show` | 현재 설치된 toolchain 확인 |
| `rustup toolchain list` | 설치된 toolchain 목록 |
| `rustup toolchain install nightly` | nightly toolchain 추가 설치 |
| `rustup toolchain install 1.83.0` | 특정 버전 설치 |
| `rustup default stable` | 기본 toolchain 변경 |
| `rustup override set nightly` | 현재 디렉터리만 nightly 사용 |
| `rustup target add x86_64-unknown-linux-musl` | 크로스 컴파일 타겟 추가 (musl 정적 빌드용) |
| `rustup target list --installed` | 설치된 타겟 목록 |
| `rustup component add rustfmt clippy rust-src rust-analyzer` | 컴포넌트 추가 |
| `rustup self uninstall` | rustup 제거 |

**프로젝트 단위 toolchain 고정:** 프로젝트 루트에 `rust-toolchain.toml`을 두고 다음을 적자.

```toml
[toolchain]
channel = "1.83.0"
components = ["rustfmt", "clippy"]
targets = ["x86_64-unknown-linux-musl"]
```

신규 멤버가 클론하면 *자동으로 같은 toolchain*으로 빌드한다.

## B.2 cargo — 빌드·테스트·실행

| 명령 | 의미 |
|---|---|
| `cargo new myproj` | 새 바이너리 프로젝트 생성 |
| `cargo new --lib mylib` | 새 라이브러리 프로젝트 |
| `cargo init` | 현재 디렉터리에 프로젝트 구조 추가 (이미 git init된 자리에) |
| `cargo build` | 디버그 빌드 (`target/debug/`) |
| `cargo build --release` | 릴리스 빌드 (`target/release/`, 최적화 적용) |
| `cargo run` | 빌드 + 실행 |
| `cargo run --release` | 릴리스 빌드로 실행 |
| `cargo run -- arg1 arg2` | 프로그램에 인자 전달 (`--` 뒤가 프로그램 인자) |
| `cargo check` | 타입 체크만 (코드 생성 X). 가장 빠른 피드백 |
| `cargo clean` | `target/` 삭제 |
| `cargo doc --open` | 문서 생성 후 브라우저에서 열기 |
| `cargo doc --no-deps` | 의존성 문서 제외 |
| `cargo update` | `Cargo.lock` 갱신 |
| `cargo update -p some-crate --precise 1.2.3` | 특정 crate를 특정 버전으로 |
| `cargo tree` | 의존성 트리 시각화 |
| `cargo tree -i syn` | `syn`을 *역방향*으로 누가 쓰는지 |
| `cargo search axum` | crates.io 검색 |
| `cargo add axum` | `Cargo.toml`에 의존성 추가 |
| `cargo add tokio --features full` | feature 함께 추가 |
| `cargo remove axum` | 의존성 제거 |

**자주 쓰는 옵션:**

| 옵션 | 의미 |
|---|---|
| `--release` | 릴리스 프로파일로 |
| `--features "foo bar"` | feature 활성화 |
| `--no-default-features` | 디폴트 feature 비활성화 |
| `--all-features` | 모든 feature 활성화 |
| `--workspace` | 워크스페이스 모든 멤버 대상 |
| `--package mycrate` (`-p`) | 특정 crate만 |
| `--bin myapp` | 특정 바이너리만 |
| `--example demo` | examples/ 안의 예제 실행 |
| `--all-targets` | bin/lib/test/example/bench 모두 |
| `--target x86_64-unknown-linux-musl` | 크로스 타겟 |

## B.3 cargo test — 단위·통합·doctest

| 명령 | 의미 |
|---|---|
| `cargo test` | 모든 테스트 실행 (단위 + 통합 + doctest) |
| `cargo test foo` | 이름에 `foo`가 들어간 테스트만 |
| `cargo test --lib` | 라이브러리 단위 테스트만 |
| `cargo test --bin myapp` | 특정 바이너리 테스트 |
| `cargo test --doc` | doctest만 |
| `cargo test --release` | 릴리스 빌드로 테스트 |
| `cargo test -- --nocapture` | `println!` 출력 보기 (`--` 뒤는 test runner 인자) |
| `cargo test -- --test-threads=1` | 단일 스레드로 (테스트 격리 깨질 때) |
| `cargo test -- --ignored` | `#[ignore]` 표시된 테스트도 |
| `cargo test --workspace` | 모든 멤버 |

**더 빠르고 깔끔한 테스트 러너:** [cargo-nextest](https://nexte.st/)

| 명령 | 의미 |
|---|---|
| `cargo install cargo-nextest --locked` | 설치 |
| `cargo nextest run` | 병렬 테스트 + 깔끔한 출력 |
| `cargo nextest run --workspace` | 워크스페이스 전체 |
| `cargo nextest run --no-fail-fast` | 실패해도 끝까지 |

## B.4 clippy — Sonar/SpotBugs의 Rust 표준판

clippy는 100여 카테고리의 lint를 묶은 *Rust 표준 정적 분석기*다. JVM 출신이 SpotBugs/Sonar를 *외부 도구*로 다루던 감각과 달리, clippy는 *cargo의 한 명령*이다.

| 명령 | 의미 |
|---|---|
| `cargo clippy` | 모든 lint 실행 |
| `cargo clippy --workspace --all-targets` | 워크스페이스 + 모든 타겟 |
| `cargo clippy -- -D warnings` | 경고를 *에러*로 (CI 게이트의 표준) |
| `cargo clippy --fix` | 자동 수정 가능한 항목 fix |
| `cargo clippy --fix --allow-dirty --allow-staged` | git에 안 올린 변경도 fix |

**자주 쓰는 lint 카테고리(`#![warn(...)]` 또는 `Cargo.toml`에 적용):**

| 카테고리 | 의미 |
|---|---|
| `clippy::pedantic` | 까다로운 스타일 권고 (취향 영역) |
| `clippy::nursery` | 실험적 lint |
| `clippy::cargo` | Cargo.toml 자체 lint |
| `clippy::complexity` | 복잡도 |
| `clippy::correctness` | 명백한 버그 (가장 중요) |
| `clippy::perf` | 성능 |
| `clippy::style` | 스타일 |
| `clippy::suspicious` | 의심스러운 패턴 |

**lint 끄기 (한 줄):** `#[allow(clippy::too_many_arguments)]`

## B.5 rustfmt — 한 줄 포매터 (ktlint/google-java-format의 감각)

| 명령 | 의미 |
|---|---|
| `cargo fmt` | 모든 파일 포맷 |
| `cargo fmt --check` | 변경 없이 *포맷이 맞는지만* 체크 (CI 게이트) |
| `cargo fmt -- --emit files` | 실제 파일에 쓰기 (디폴트) |
| `cargo fmt -- --emit stdout` | 표준 출력으로 |

**프로젝트 설정:** 루트에 `rustfmt.toml`을 두자.

```toml
edition = "2021"
max_width = 100
hard_tabs = false
tab_spaces = 4
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

## B.6 cargo audit / deny / vet — 보안 도구 (OWASP Dependency Check의 감각)

| 명령 | 의미 |
|---|---|
| `cargo install cargo-audit --locked` | 설치 |
| `cargo audit` | 의존성을 RustSec Advisory DB와 대조 |
| `cargo audit --deny warnings` | 경고를 에러로 (CI 게이트) |
| `cargo install cargo-deny --locked` | cargo-deny 설치 |
| `cargo deny init` | `deny.toml` 생성 |
| `cargo deny check` | license / source / dependency / advisory 종합 검사 |
| `cargo deny check licenses` | 라이선스만 |
| `cargo install cargo-vet --locked` | cargo-vet 설치 (supply chain 감사) |
| `cargo vet init` | 감사 대상 등록 |
| `cargo vet check` | 감사 상태 확인 |

**`deny.toml` 미니 예시:**

```toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "MPL-2.0"]
deny = ["GPL-3.0", "AGPL-3.0"]

[bans]
multiple-versions = "warn"

[advisories]
db-path = "~/.cargo/advisory-db"
yanked = "deny"
```

## B.7 cargo expand / flamegraph / miri — 디버깅·프로파일링

| 명령 | 의미 |
|---|---|
| `cargo install cargo-expand --locked` | 매크로 펼친 모양 보기 |
| `cargo expand` | 모든 매크로 펼치기 |
| `cargo expand --bin myapp` | 특정 바이너리만 |
| `cargo expand foo::bar` | 특정 모듈만 |
| `cargo install flamegraph --locked` | flamegraph 설치 (perf 필요) |
| `cargo flamegraph --bin myapp` | 프로파일링 후 SVG 생성 |
| `rustup +nightly component add miri` | miri 설치 (UB 검출) |
| `cargo +nightly miri test` | miri로 테스트 (unsafe 검증) |
| `cargo +nightly miri run` | miri로 실행 |

## B.8 cargo workspace — 멀티 모듈 (Gradle multi-module의 감각)

루트 `Cargo.toml`에:

```toml
[workspace]
resolver = "2"
members = ["domain", "infra", "web"]

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
thiserror = "2"
```

각 멤버 `Cargo.toml`에서:

```toml
[package]
name = "domain"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { workspace = true }
anyhow = { workspace = true }
```

| 명령 | 의미 |
|---|---|
| `cargo build --workspace` | 모든 멤버 빌드 |
| `cargo test --workspace` | 모든 테스트 |
| `cargo build -p web` | `web` crate만 |
| `cargo run -p web --bin server` | 특정 바이너리 |

**resolver = "2" 함정 한 줄:** workspace 멤버들이 *다른 feature 조합*으로 같은 의존성을 요구하면 *통합되지 않고 각각 빌드*된다 — 컴파일 시간이 폭증할 수 있으니 13장의 처방을 한 번 펴자.

## B.9 Cargo.toml — 자주 쓰는 항목 미니 레퍼런스

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
authors = ["Toby <toby@example.com>"]
description = "한 줄 설명"
license = "MIT OR Apache-2.0"
repository = "https://github.com/me/myapp"
readme = "README.md"
keywords = ["cli", "tool"]
categories = ["command-line-utilities"]

[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"], default-features = false }
axum = "0.7"
sqlx = { version = "0.7", features = ["postgres", "runtime-tokio-rustls"] }
tracing = "0.1"
anyhow = "1"
thiserror = "2"

[dev-dependencies]
tokio-test = "0.4"
mockall = "0.13"
proptest = "1"

[build-dependencies]
prost-build = "0.13"

[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
strip = true
panic = "abort"

[profile.dev]
opt-level = 0
debug = true

[[bin]]
name = "server"
path = "src/bin/server.rs"

[[bench]]
name = "my_bench"
harness = false
```

**semver 표기 한 줄 정리:**

| 표기 | 의미 |
|---|---|
| `"1.2.3"` | `>=1.2.3, <2.0.0` (caret) |
| `"^1.2.3"` | 위와 동일 (명시적 caret) |
| `"~1.2.3"` | `>=1.2.3, <1.3.0` (tilde) |
| `"=1.2.3"` | 정확히 이 버전 |
| `">=1.2, <2"` | 범위 직접 지정 |
| `"1"` | `>=1.0.0, <2.0.0` |
| `{ git = "...", branch = "main" }` | git 의존성 |
| `{ path = "../mylib" }` | 로컬 경로 |

## B.10 pre-commit 훅 추천 한 단락

`.git/hooks/pre-commit`에 다음을 두자(또는 [pre-commit](https://pre-commit.com) framework 사용).

```bash
#!/usr/bin/env bash
set -euo pipefail
cargo fmt --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo audit --deny warnings
cargo deny check
```

CI 파이프라인의 권장 형태도 같은 줄이다. *fmt → clippy → test → audit → deny → bench --no-run*. 신규 멤버가 들어오는 첫날에 이 한 줄을 박아두면, 6개월 뒤 코드 리뷰 시간이 *체감으로* 짧아져 있다.

---

명령 100여 개를 한 페이지에 모았지만, 매일 손에 잡는 건 *그중 열 개*다. `cargo build`, `cargo test`, `cargo run`, `cargo check`, `cargo fmt`, `cargo clippy -- -D warnings`, `cargo add`, `cargo tree`, `cargo audit`, `rustup update`. 이 열 개만 외워두면 95%의 자리에서 손이 멈추지 않는다. 나머지는 책상 옆에 펴 놓고 보자.
