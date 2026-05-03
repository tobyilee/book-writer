# 저술 계획 — JVM 출신을 위한 Rust 입문·활용서

> Round 1 리뷰 반영 완료. 14장 → 16장 + 부록 4개로 확장.

> 본 계획은 `01_reference.md`의 12개 토픽과 6절 인용, 7절 참고문헌을 토대로 설계됐다. 12개 토픽을 1:1로 옮기지 않고, "JVM 백엔드 개발자가 Rust로 실무 시스템을 만들 수 있게" 되는 독자 여정 순서로 16개 챕터를 4부로 나누어 배치했다. 본문 뒤에 부록 4개(JVM↔Rust 매핑 / cargo 치트시트 / crate 카탈로그 / 4~6개월 학습 가이드)를 붙여 *"바이블"의 위상*을 매듭짓는다.

---

## 1. 책 제목 후보 3개

1. **『JVM 출신을 위한 Rust — Spring 다음에 읽는 책』** ★ 추천
   한 줄 카피: *Spring 너머의 시스템을 빌드하는 16개의 챕터.*
   왜 이 제목인가: 대상 독자(Java/Kotlin/Spring 시니어·미들)를 정면으로 호명한다. "Spring 다음"이라는 부제가 "JVM을 떠나라"가 아니라 "JVM을 두고 한 발 더 가라"는 폴리글랏 메시지와 맞는다. 토비 스타일의 친절한 어조와도 잘 붙는다 — "이 책이 너를 호명한다"는 감각.

2. **『러스트 라이트 — JVM 개발자가 빠르게 가닿는 메모리 안전 시스템』**
   한 줄 카피: *컴파일러가 잡아주는 안전, 그리고 한 자릿수 MB로 끝나는 컨테이너.*
   왜 이 제목인가: "Light"는 두 의미를 동시에 — 가벼운 바이너리(8~10MB), 그리고 학습 부담을 덜어주는 가이드. 메모리 안전(ONCD/NSA 권고)과 운영 효율(Discord/Cloudflare 사례)을 표지에서부터 읽힌다. 다만 "JVM 출신"이라는 호명이 약하다.

3. **『Borrow Checker와 친구되기 — Spring 백엔드 개발자의 Rust 실전서』**
   한 줄 카피: *컴파일러를 적이 아니라 동료(co-author)로 받아들이는 6개월의 여정.*
   왜 이 제목인가: 가장 정직한 제목. 6장 함정 1("처음 한 달은 보여주는 에러 메시지를 그대로 따르는 것이 가장 빠른 길")을 그대로 표지에 박는다. 단점: borrow checker라는 용어가 표지에 노출되면 입문 독자가 위축될 수 있다.

**추천:** **1번 『JVM 출신을 위한 Rust — Spring 다음에 읽는 책』**.
독자 호명이 가장 강하고, 책의 마지막 챕터(폴리글랏 결론)와 표지 메시지가 한 줄로 이어진다. 이 시그니처는 **표지 → 1장 "이 책의 자리" 절 → 16장 마지막 한 줄**에서 일관되게 호명된다. 토비 스타일의 동반자적 청유형 어미와도 가장 잘 어우러진다.

---

## 2. 책 특성

- **장르:** "에세이형 기술 바이블". 단순 문법 레퍼런스가 아니다. 토픽별 깊이는 활용서 수준이지만 어조는 동반자적 입문서다. JVM 카운터파트를 항상 먼저 호명해서 "이미 알고 있는 것에 닻을 내려" 새 개념을 소개하는 패턴을 책 전반에 걸쳐 일관되게 유지한다.
- **분량 (예상):** 본문 약 240,000자(원고지 약 1,200매), 16개 챕터 × 평균 14,000~18,000자 + 부록 약 30,000자. 출판 페이지로는 약 700~800페이지. "바이블"이라는 요청에 맞춰 두툼하게 — 단, 한 챕터에 두 토픽을 욱여넣지 않는다는 원칙은 끝까지 지킨다(7장 분리·14장 분리는 그 원칙을 본문에 박은 것이다).
- **난이도:** 중급 ~ 중상급. JVM 다년 백엔드 경력자 전제. Java 문법 설명은 일절 없고, Spring DI/Servlet/JPA/CompletableFuture/Coroutine을 알고 있다는 가정 위에서 매 챕터 "JVM 대응물 매핑"을 시그니처로 박는다(16개 챕터 전부, 빠지는 챕터 0). Rust 자체는 0부터 시작 가능.
- **독자 여정 (한 단락):** 독자는 *"왜 굳이 Rust를?"라는 의심*을 품고 1장에 들어와, 2장에서 cargo로 첫 바이너리를 빌드하며 작은 성취감을 얻는다. Part 2에서 borrow checker와 정면으로 부딪히며 *"막막함 → 패턴 인식 → 친구되기"의 곡선*을 3개 챕터에 걸쳐 천천히 지나고, 7장에서 표현력 도구상자를 손에 쥔다. Part 3 진입에서 8장 스마트포인터·매크로·unsafe로 *Rust의 안전 경계가 어디까지인지*를 명료하게 본 뒤, 9~10장 동시성과 async, 11장 axum, 12장 sqlx로 *"이제 Spring으로 짜던 그 서비스가 Rust로 보인다"는 자신감*에 도달한다. Part 4에서는 8MB 컨테이너로 출시하고, 15장에서 JVM과 Rust를 잇는 폴리글랏 아키텍처(JNI/Panama/C ABI)를 설계하며, 마지막 16장에서 *"Rust는 JVM의 대체가 아니라 무기 추가다"*라는 폴리글랏 결론과 한국 커뮤니티 매듭에 이른다. 진입 상태(JVM 베테랑·Rust 초심자) → 출구 상태(JVM 시스템 옆에 Rust 사이드카·hot path를 직접 만들어 출시할 수 있는 폴리글랏 백엔드 개발자).

---

## 3. 4부 구조 개요

### Part 1. 왜 Rust인가, 그리고 첫 만남 (1~3장)
*"JVM 출신을 환영합니다"의 톤으로 시작한다. 도망가지 않게 하는 게 첫째 목표다.*
Rust가 왜 지금 백엔드 개발자의 의제가 됐는지(ONCD/NSA, Discord/Cloudflare/Microsoft)를 짚고, **"이 책의 자리" 절**(다른 Rust 입문서와의 차별점)로 1장의 무게를 잡는다. 그다음 JVM과 Rust의 본질적 차이를 한 표로 정리한 뒤, cargo로 첫 바이너리를 띄워본다. 3장에서는 변수·함수·모듈 등 기본 문법을 *Java/Kotlin과의 1:1 대응*으로 빠르게 흡수시키고, 끝에 "에러 메시지 읽는 법" 한 절로 4장 소유권의 첫 컴파일 거부에 대비시킨다.

### Part 2. Rust의 마음 — 컴파일러와 친구되기 (4~7장)
*책의 무게중심. JVM 출신이 가장 많이 부딪히고 가장 많이 보상받는 영역이다.*
소유권 → 빌림 → 라이프타임을 **세 챕터(4·5·6장)에 걸쳐 천천히** 가르친다. 한 챕터에 다 넣으면 독자가 익사한다는 원칙. 5장 끝에 **RustBelt / Stacked Borrows / Tree Borrows** 한 단락을 박아 *"이 두 줄의 규칙은 학술적으로 입증됐다"*는 위상 신호를 둔다. 7장에서 트레잇·제네릭·패턴매칭·에러처리(Result/Option/?/anyhow/thiserror)를 표현력 도구상자로 묶어 자기 도메인 모델링까지 데려간다. Part 2의 매듭은 7장이 *깨끗하게* 닫는다.

### Part 3. 메모리·동시성·실무 시스템 (8~13장)
*"이제 Spring으로 짜던 그 서비스가 Rust로 보인다."*
8장에서 스마트 포인터(Box/Rc/Arc/RefCell/Mutex)·매크로·**unsafe 한 절**로 *Rust의 안전 경계가 어디까지인지*를 명료하게 본다. unsafe는 14장 FFI에서 만나기 전에 *기초가 깔려 있어야* 하는 도구다. 9장 동시성 기초(Send/Sync, thread, channel, Mutex)에서 5장 borrow의 두 줄 규칙이 *멀티스레드 안전성*으로 보상받고, 10장 async/await·tokio 실전에서 Kotlin Coroutine 다음의 모델을 손에 쥔다. 11장 axum으로 첫 HTTP 서비스를 띄우고, 12장에서 sqlx/sea-orm/diesel의 선택지를 소개한 뒤 sqlx로 실제 CRUD를 구현한다. 13장은 cargo test·doctest·clippy·criterion·rustfmt·**컴파일 시간 함정 처방**·**보안 도구(cargo audit/deny/vet)**·**매크로 작성 첫 만남** — 품질·도구 인프라.

### Part 4. 출시·폴리글랏·사람 (14~16장)
*"Rust는 JVM의 대체가 아니라 무기 추가다."*
14장에서 8~10MB 컨테이너 빌드(musl + distroless)와 tracing-opentelemetry 관측을 다루고, 15장에서 JNI·Project Panama·C ABI·`#[repr(C)]`·UB 회피로 JVM과 Rust를 잇는 **폴리글랏 아키텍처**(사이드카·hot path 추출 패턴 포함)를 설계한다. 마지막 16장은 학습 곡선·조직 도입 정치(*"I Rewrote… Lost My Job"의 교훈*과 Dropbox Magic Pocket의 그늘)·한국 커뮤니티 자원·책의 마지막 한 줄. **사람과 조직의 챕터로 매듭짓는 결정**은 *기술서가 사람의 책으로 닫힌다*는 시그니처다.

### 부록 (A·B·C·D)
JVM↔Rust 한 페이지 매핑 표 / cargo·rustup·clippy·fmt 치트시트 / 추천 crate 카탈로그 / 4~6개월 학습 가이드. 본문에서 산발적으로 언급된 매핑·도구·crate를 한 자리에 모은다.

---

## 4. 챕터 목록 (16개)

### 챕터 1. 왜 지금 Rust인가 — JVM 베테랑에게 보내는 초대장
- **핵심 질문:** Spring으로 잘 굴러가던 내가, 왜 굳이 새로운 언어를 또 배워야 하는가? 그리고 *왜 다른 Rust 책이 아니라 이 책인가?*
- **주요 내용:**
  - "메모리 안전"이 정부 권고가 된 시대: 미국 ONCD(2024-02)와 NSA(2025-06)의 메모리 안전 언어 권고를 인용 — Microsoft의 "C/C++ 취약점의 70%가 메모리 오류" 한 줄.
  - 시장 신호: 2024 State of Rust 45% 프로덕션 사용(전년 대비 +7%p), 2025 Stack Overflow 9년 연속 most admired (83%).
  - 사례 4개의 한 단락 요약: Discord(GC 스파이크 제거), Cloudflare Pingora(CPU 70% 절감), AWS Firecracker(< 125ms 시작), Microsoft(Windows kernel·Azure Data Explorer 35만 라인).
  - **"이 책의 자리" 한 절 (약 1,500~2,000자)**: 시장에 이미 있는 책들과의 위치 비교.
    - *『러스트 프로그래밍 언어』*(rinthel 한국어판) — 언어 표준 레퍼런스. 본 책은 그것을 보완하는 *JVM 출신을 위한 번역 가이드*.
    - *『프로그래밍 러스트』*(O'Reilly) — 시스템 프로그래밍 깊이. 본 책은 *백엔드 서비스 출시*까지.
    - *『러스트 인 액션』*(Manning) — 시스템 코드 연습. 본 책은 *Spring 카운터파트와의 비교*가 중심.
    - *Hands-on Rust* — 게임으로 배우기. 본 책은 *axum·sqlx·tracing·운영*까지.
    - *『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』*(제이펍) — Axum 사용법. 본 책은 *axum을 Spring과 비교하며 배우게 함 + sqlx·tracing·polyglot까지*.
    - 한 줄 매듭: *"이 책은 *JVM 출신만이 알 수 있는 닻*에 새 개념을 묶어 가르치는, 시장의 빈자리를 메우는 책이다."* 표지·결론과 한 줄로 정렬되는 시그니처.
  - 이 책의 약속: 4~6개월의 적응 기간을 건너 "Spring 다음의 시스템을 빌드"하는 데까지 데려간다.
  - 이 책의 약속이 아닌 것: "JVM을 떠나라"가 아니다. "무기를 하나 더 들자"다. 그리고 *마법으로 학습 곡선을 줄여주는 책도 아니다* — 4~6개월의 정직한 동반.
- **JVM 대응물:** Java 21 Virtual Thread / Spring Boot Native Image / GraalVM이 메우려 하는 갭을 Rust는 다른 각도(컴파일 타임 안전성 + GC 없음)에서 이미 해결해 둔 상태라는 점을 비교. *결정적 차이* 한 단락: GraalVM Native Image는 *런타임 효율*만 풀고 *메모리 안전성*은 그대로 JVM의 GC에 의존하지만, Rust는 두 축을 함께 가져간다.
- **예상 분량:** 15,000자
- **함께 해보자:** 자기 회사의 가장 최근 운영 사고 1건을 떠올려 보자. NPE인가? deadlock인가? memory leak인가? Rust가 그 사고를 컴파일 타임에 잡았을지를 한 단락으로 적어보자. *(이 노트는 7장의 Result/Option, 9장의 Send/Sync, 10장의 async 데드락에서 다시 호출된다.)*

---

### 챕터 2. 첫 만남 — cargo로 5분 만에 빌드하기
- **핵심 질문:** rustup·cargo·crates.io는 Maven/Gradle/Maven Central에 어떻게 대응되는가? 첫 빌드까지 손에 잡히는 단계는 무엇인가?
- **주요 내용:**
  - rustup으로 toolchain 설치(stable/nightly), `rustup toolchain` = sdkman의 감각.
  - `cargo new` → `cargo build` → `cargo run` → `cargo test`. 5분 만에 "Hello, JVM" 출력의 *빠른 성취감*.
  - `Cargo.toml`을 한 줄씩 해부 — `[package]`, `[dependencies]`, semver 표기, feature flag(`default-features = false`).
  - workspace 미리보기: 이 책의 예제는 workspace로 묶을 것이라는 약속. (자세한 건 13장.)
  - VSCode + rust-analyzer / IntelliJ Rust / RustRover 셋업, 그리고 사전 커밋 훅(`cargo fmt --check && cargo clippy -D warnings && cargo test`).
- **JVM 대응물:** `Cargo.toml` ↔ `pom.xml`/`build.gradle.kts`, `cargo build` ↔ `mvn package`/`gradle build`, crates.io ↔ Maven Central, rustup toolchain ↔ sdkman java, cargo workspace ↔ Gradle multi-module. *결정적 차이* 한 단락: cargo는 *언어 코어*에 들어와 있어서 Maven plugin/Gradle plugin/Spotless/Sonar 같은 외부 도구 모음을 별도로 조합할 필요가 없다.
- **예상 분량:** 14,000자
- **함께 해보자:** `cargo new hello-jvm`으로 프로젝트를 만든 뒤, `Cargo.toml`에 `clap = { version = "4", features = ["derive"] }`를 추가하고 인자 한 개를 받아 출력하는 CLI를 짜보자. 빌드·실행·테스트 모두 cargo 한 도구 안에서 끝난다는 감각을 손에 묻혀보자. *(이 작은 CLI는 13장의 clap 절에서 완성형으로 다시 호출된다.)*

---

### 챕터 3. 변수·타입·함수·모듈 — Java가 알던 모양과 다른 부분
- **핵심 질문:** 같은 의미인데 표기는 어떻게 다르고, 다른 의미인데 표기가 비슷해서 헷갈리는 부분은 어디인가?
- **주요 내용:**
  - `let`/`let mut` ↔ `val`/`var`. **불변이 디폴트**라는 사실의 무게.
  - `i32`/`i64`/`u32`/`usize`/`f64`/`bool`/`char`/tuple — 원시 타입 지도. JVM의 boxing/unboxing이 없는 세계.
  - 함수 시그니처는 항상 명시적으로 — 타입 추론이 강해도 "함수 경계 = API 계약"이라는 철학.
  - `if`/`match`/`loop`/`while`/`for in` — 식(expression)으로서의 if·match. Java의 switch expression과 비교.
  - 모듈 시스템: crate / mod / pub / pub(crate) / pub(super). `mod.rs` vs `foo/mod.rs`의 두 스타일.
  - prelude — `Option`, `Result`, `Vec`, `String`은 import 없이 보인다.
  - `String` vs `&str` 첫 만남: 자세한 설명은 4장에서, 여기서는 "두 개가 있다는 사실과 함수 파라미터는 보통 `&str`"이라는 디폴트만 심는다.
  - **"에러 메시지 읽는 법" 한 절 (약 1,500자)**: rustc 에러 메시지의 구조(에러 코드 → 위치 → help → note → suggestion)를 한 그림으로. 4장 첫 컴파일 거부 앞의 다리.
- **JVM 대응물:** `let`/`let mut` ↔ `val`/`var`, `mod`/`pub`/`pub(crate)` ↔ `package` + `public`/`package-private`/JPMS `module-info`, `match` ↔ Java 17 sealed + switch pattern, `Option<T>` ↔ `Optional<T>`(단 더 엄격), `Vec<T>` ↔ `ArrayList<T>`, `&str`/`String` ↔ `String`(이 비대칭이 4장의 복선). *결정적 차이* 한 단락: Rust의 `match`는 *값에 대한 식*이고 *exhaustive*가 컴파일러 강제다 — Java의 switch expression이 가진 두 약점(default 강요·sealed 밖 타입에 대한 누락 허용)이 없다.
- **예상 분량:** 17,000자
- **함께 해보자:** Java로 짠 익숙한 도메인 클래스 하나(예: `User { id, email, createdAt }`)를 Rust struct로 옮겨보자. `derive(Debug, Clone)`을 붙여 출력해보고, getter 없이 `pub` 필드로 노출했을 때의 감각이 Java와 어떻게 다른지 한 줄로 적어보자. *(이 struct는 4장의 ownership 첫 예제로, 7장의 thiserror 도메인 모델링으로 다시 호출된다.)*

---

### 챕터 4. 소유권 — "한 명만 가진다"는 단순한 규칙
- **핵심 질문:** GC가 처리하던 메모리 회수를, 컴파일러는 어떻게 강제하는가? "moved value를 다시 쓸 수 없다"는 에러 앞에서 무엇을 바꿔야 하는가?
- **주요 내용:**
  - 세 가지 규칙: 모든 값은 정확히 하나의 owner를 가진다 / owner가 scope를 벗어나면 즉시 drop / 대입·전달은 ownership을 move한다.
  - `Copy` 트레잇이 붙은 원시 타입(`i32`, `bool`, …)은 복사된다 — 이 예외 하나가 처음에 가장 많이 헷갈린다.
  - `String` vs `&str`을 정면으로 다룬다 (함정 5의 본격 처방). heap-allocated owned vs borrowed view.
  - `Vec<T>`로 본 move의 의미 — 함수에 넘기면 호출자에서 사라진다.
  - `clone()`을 언제 쓰고 언제 쓰지 말 것인가: "clone을 죄책감 없이 쓰자"는 입문자용 처방, 그리고 6장에서 빌림으로 옮겨가는 길.
  - `Drop` 트레잇 미리보기: scope 종료 = 결정적 자원 해제. JVM의 `try-with-resources` / Kotlin `use {}` / `finalize()`와 비교.
- **JVM 대응물:** Java의 참조 변수 두 개로 같은 객체를 가리키는 일상 코드가 → Rust에서 왜 컴파일 거부되는가. `Drop` ↔ `try-with-resources` / `AutoCloseable.close()` / Kotlin `use {}`. `clone()` ↔ Java `Cloneable`(단 의미가 더 명시적). *결정적 차이* 한 단락: JVM의 `finalize()`는 *언제 불릴지 모르는* 자원 해제고 try-with-resources는 *블록 경계*에서만 동작한다 — Rust의 `Drop`은 *모든 scope 종료*에서 결정적으로 호출된다.
- **예상 분량:** 17,000자
- **함께 해보자:** 다음 코드가 왜 컴파일이 안 되는지 한 단락으로 설명하고, 두 가지 방법(① clone, ② 5장에서 배울 borrow)으로 각각 고치는 시도를 해보자. *(예시: `let s = String::from("hi"); let t = s; println!("{s}");`)* *(이 코드는 5장 첫 절에서 borrow로 다시 풀린다.)*

---

### 챕터 5. 빌림 — `&T`와 `&mut T`, 그리고 데이터 레이스가 사라지는 이유
- **핵심 질문:** ownership을 옮기지 않고 잠깐 빌려주고 싶을 때, 컴파일러가 강제하는 두 줄의 규칙은 무엇이고 왜 그것이 동시성 안전성으로 이어지는가?
- **주요 내용:**
  - `&T`(immutable borrow) vs `&mut T`(mutable borrow).
  - 두 줄의 규칙: 한 시점에 mutable borrow는 하나만 / mutable borrow가 살아있는 동안 다른 어떤 borrow도 없다.
  - 4장의 함께해보자 코드를 borrow로 다시 풀기.
  - "왜 이 규칙이 data race를 컴파일 타임에 차단하는가" — Rust의 가장 큰 한 줄을 9장(Send/Sync)의 복선으로 심는다.
  - reborrow와 NLL(Non-Lexical Lifetimes)이 왜 borrow checker를 덜 까칠하게 만들었는가.
  - 자주 만나는 에러 메시지 사전: "cannot borrow as mutable because it is also borrowed as immutable" / "borrow of moved value" — 함정 1을 그대로 처방.
  - **"이 두 줄의 규칙은 학술적으로 입증됐다" 한 단락 (약 2,000자)**: RustBelt(POPL 2018)가 Rust의 type system이 메모리·스레드 안전성을 *형식 검증*했다는 사실을 한 단락으로. **Stacked Borrows**(POPL 2020)와 그 후속 **Tree Borrows**(PLDI 2025)가 *unsafe 코드의 borrow 의미*를 어떻게 정의했는지를 두세 문장으로. 깊이 들어갈 필요 없이 *"이 책은 그저 관행이 아니라 입증된 안전성을 가르친다"*는 위상 신호. (8장 unsafe 절에서 한 번 더 회수된다.)
- **JVM 대응물:** `&T`와 `&mut T`는 *Java의 참조 모델 자체와 비대칭*이다. **Java의 모든 객체 참조는 늘 mutable이고 동시 접근이 허용된다 — Rust는 그 일상 코드를 컴파일러가 거부한다.** Java가 `synchronized`/`ReentrantLock`/`@ThreadSafe` 어노테이션으로 *런타임에·관행으로* 보장하려던 것을, Rust는 *빌드 타임에 강제로* 못 박는다는 핵심 한 줄. *결정적 차이* 한 단락: Java의 `final` 참조는 *재할당 금지*일 뿐 객체 내용 변경은 막지 못한다 — `&T`와는 의미가 다르다. (이 매핑 정정은 흔히 재발견되는 오해를 미리 차단하는 데 결정적이다.)
- **예상 분량:** 17,000자
- **함께 해보자:** 단순 카운터 구조체 하나를 만들어, ① 동시에 두 개의 `&mut`을 시도해보고 ② 그것을 NLL이 풀어주는 패턴(스코프 좁히기)으로 고쳐보자. 컴파일러가 보여주는 에러 메시지의 줄·열이 무엇을 가리키는지 손가락으로 짚어보자. *(이 카운터는 9장 `Arc<Mutex<T>>` 절에서 *멀티스레드 안전성*으로 다시 호출된다.)*

---

### 챕터 6. 라이프타임 — `'a`라는 메타데이터에 익숙해지자
- **핵심 질문:** 라이프타임 어노테이션은 왜 필요한가, 언제 생략 가능한가, 진짜로 명시해야 하는 순간은 어떤 모양인가?
- **주요 내용:**
  - 라이프타임은 *런타임 비용 0의 컴파일러 메타데이터*다. 참조가 가리키는 데이터보다 참조가 더 오래 살지 않게 검증하는 도구.
  - 함수 시그니처에서의 `'a`: `fn longest<'a>(x: &'a str, y: &'a str) -> &'a str`.
  - 라이프타임 elision의 세 가지 규칙 — 입문자가 매일 보는 99%의 함수는 `'a`를 안 쓴다.
  - 진짜로 명시해야 하는 패턴들: 구조체에 참조 필드를 두는 경우, 두 개 이상의 입력 lifetime을 출력에 묶는 경우.
  - `'static`의 두 얼굴: 문자열 리터럴의 lifetime / 트레잇 객체 bound로서의 `'static`. 후자가 늘 헷갈리는 이유.
  - 한국 개발자 후기 인용: "lifetime annotation('a, 'static)은 명료히 이해하기 어렵다"(blog.cro.sh). *공감을 먼저, 처방을 나중에*.
- **JVM 대응물:** 직접 대응물이 없는 영역. Java/Kotlin은 GC가 lifetime을 런타임에 추적해 처리한다. *결정적 차이* 한 단락 (약 800자): JVM에서 *어떤 객체가 언제까지 살아 있는가*는 GC 알고리즘과 reachability analysis가 *런타임에* 결정한다 — 그래서 개발자는 그 비용을 *짐작은 해도 강제는 못 한다*. Rust는 그 결정 시점을 *컴파일 타임*으로 옮긴 대신, *컴파일러에게 수동으로 일러주는 비용*(`'a` 어노테이션)을 받아낸다. JVM 출신이 라이프타임을 어렵게 느끼는 *진짜 이유*는 문법이 아니라 *"메모리 lifetime을 내가 직접 사고해본 적이 없다"*는 사고의 공백이다 — 이 챕터의 처방은 그래서 *예제 → 컴파일러와의 대화 → 패턴 인식*으로 천천히 간다.
- **예상 분량:** 16,000자
- **함께 해보자:** 함수 하나(예: 두 `&str`을 받아 더 긴 쪽을 반환)를 elision으로 시작해보고, 컴파일러가 어떤 시점에 `'a`를 요구하는지 손으로 만져보자. 그다음 `'static` bound가 들어간 트레잇 객체 하나(예: `Box<dyn Fn() + 'static>`)가 왜 `'static`을 요구하는지 한 단락으로 적어보자. *(이 `'static` bound는 10장 tokio `spawn` 시그니처에서 다시 호출된다.)*

---

### 챕터 7. 트레잇·제네릭·패턴 매칭·에러 처리 — 표현력 도구상자 (전반부)
- **핵심 질문:** Java 인터페이스·제네릭·sealed class·예외가 하던 일을 Rust에서는 각각 어떤 도구가 맡고, 그 둘은 의미가 어떻게 다른가? `Result<T, E>`/`?`/anyhow/thiserror로 *예외 없이* 어떻게 실무 에러 처리를 해내는가?
- **주요 내용:**
  - **트레잇**: 인터페이스가 아니다. 외부 타입에 트레잇 구현을 추가할 수 있다(orphan rule 안에서). 정적 디스패치(generic) vs 동적 디스패치(`dyn Trait`)의 명시적 선택.
  - **제네릭과 monomorphization**: type erasure가 아니다. 컴파일 시점에 타입별 코드가 생성되어 0-cost. 단점은 컴파일 시간과 바이너리 크기.
  - **enum + match**: algebraic data type. exhaustive match가 강제된다. Java 17 sealed class + switch pattern과 비교.
  - **패턴 매칭의 깊이**: `if let`, `while let`, 구조 분해(destructuring), guard, `@` 바인딩, ref 패턴. Java의 record pattern과 한 절씩 비교.
  - **에러 처리 — `Option<T>`/`Result<T, E>`/`?`**: 예외가 아니라 *값*. `?` 연산자는 "Result/Option 반환 함수에서 실패면 즉시 early return"하는 sugar. `panic!`은 unrecoverable. 1장에 적었던 운영 사고 노트가 NPE였다면 *왜 `Option<T>`가 그 사고를 컴파일 타임에 잡는지*를 정면으로 다룬다.
  - **anyhow vs thiserror의 분업**: anyhow(애플리케이션 — 모든 에러를 한 box에) vs thiserror(라이브러리 — 도메인별 enum 에러). 3장에서 만든 도메인 struct에 thiserror로 `enum AuthError`를 붙이는 첫 예제.
  - **`From`/`Into`와 `?`의 자동 변환**: `?`가 어떻게 `From` 트레잇을 통해 에러 타입을 변환하는지를 한 그림으로. Java의 `throws` chain이 못 했던 일.
- **JVM 대응물:** trait ↔ interface + abstract class + Scala typeclass / generics ↔ generics(단 erasure 아님) / enum ↔ sealed class + switch pattern matching / `Result<T, E>` ↔ checked exception의 정신 + Kotlin `Result` / `?` ↔ `Optional.orElseThrow` + `throws` chain / anyhow ↔ `RuntimeException` 래핑 / thiserror ↔ checked exception 계층. *결정적 차이* 한 단락: Java checked exception은 *예외가 메서드 시그니처를 오염*시키지만 *값이 아니라 제어 흐름*이라 함수 합성·고차 함수와 충돌한다. `Result<T, E>`는 *그저 enum*이라 `.map`/`.and_then`/`.collect::<Result<Vec<_>, _>>()`로 자유롭게 합성된다.
- **예상 분량:** 18,000자
- **함께 해보자:** 사용자 인증 도메인을 작은 enum으로 표현해보자. `enum AuthError { InvalidPassword, ExpiredToken, RateLimited(Duration), DatabaseError(#[from] sqlx::Error) }` 같은 모양으로 thiserror를 써서 정의하고, `Result<User, AuthError>`를 반환하는 함수를 한 줄씩 손으로 만져보자. Java의 checked exception으로 같은 의미를 표현하면 무엇이 어떻게 답답해지는지 한 단락으로 적어보자. *(이 `AuthError`는 11장 axum의 `IntoResponse` 절에서 HTTP 응답으로 변환되어 다시 호출된다.)*

---

### 챕터 8. 스마트 포인터·매크로·unsafe 진입 — 메모리 도구와 안전 경계
- **핵심 질문:** Java의 일반 객체 참조·`AtomicReference`·Lombok이 하던 일을 Rust의 어떤 도구가 맡는가? `unsafe` 블록은 *언제* 쓰고 *언제 쓰지 말아야* 하는가? Rust의 안전 경계는 어디까지인가?
- **주요 내용:**
  - **스마트 포인터 표 (정면)**: `Box<T>` / `Rc<T>` / `Arc<T>` / `RefCell<T>` / `Mutex<T>` — JVM의 일반 객체 참조 / 단일 스레드 공유 / 멀티스레드 공유 / 런타임 borrow 검증 / 동기화된 가변 접근으로 1:1 매핑. `Arc<Mutex<T>>` 패턴이 *공유 가변 상태의 표준 표현형*인 이유.
  - **`Rc` vs `Arc`**: 단일 스레드면 `Rc`(원자 연산 비용 절감), 멀티스레드면 `Arc`. `Rc`가 Send가 아니라서 9장에서 컴파일러가 무엇을 거부할지의 복선.
  - **`RefCell`의 interior mutability**: 컴파일 타임 borrow 검증을 *포기하고* 런타임으로 미루는 도구. 한 번 잘못 쓰면 panic. Java의 일반 객체 그대로의 모양.
  - **매크로 첫 만남**: declarative `macro_rules!` + procedural `proc_macro`. `#[derive(Debug, Clone, Serialize)]`이 자바 Lombok과 다른 점 — 토큰을 실제로 펼쳐 컴파일러가 다시 검사한다(`cargo expand`로 펼친 모양 보기). *깊이는 13장 "내 매크로 만들기" 절에서 다시 다룬다*는 다리.
  - **unsafe 한 절 (약 3,000자)**: `unsafe { }`의 의미·사용 시점·검증 패턴.
    - *언제 쓰는가*: raw pointer 역참조, `static mut`, FFI 호출, 다른 unsafe 함수 호출, unsafe trait 구현 — 정확히 다섯 가지뿐.
    - *언제 쓰지 말아야 하는가*: borrow checker를 우회하려고. 99%는 더 나은 안전 코드로 재설계 가능하다.
    - *안전 경계의 역할*: `unsafe`는 *컴파일러를 끄는* 게 아니라 *"이 블록 안의 invariant를 인간이 보증한다"*는 계약. **safe API를 unsafe 위에 얹는 패턴**이 표준 라이브러리의 설계(예: `Vec`/`String` 내부는 unsafe다).
    - 5장에서 박은 RustBelt 한 단락의 회수: Stacked Borrows / Tree Borrows가 *unsafe 코드의 borrow 의미*를 정의한 이유 — *unsafe라도 검증할 수 있는 형태*로 모델을 만든 것.
    - 학술 인용 한 줄: Cui et al. "Is unsafe an Achilles' Heel?" (arXiv:2308.04785) — 실무에서 unsafe 잘못 쓰는 패턴 5가지. deepSURF (IEEE S&P 2026) — unsafe 영역의 자동 탐지.
    - 14장 FFI 챕터로 가는 다리: *"15장 JNI/Panama는 unsafe의 가장 큰 사용처다 — 이 절을 다시 펼치게 될 것이다."*
- **JVM 대응물:** `Box<T>` ↔ `new Object()` 후 참조 보유 / `Rc<T>` ↔ 단일 스레드 공유 객체(JVM에선 구분 없음) / `Arc<T>` ↔ 멀티스레드 공유 객체 + (필요시) `AtomicReference` / `RefCell<T>` ↔ 런타임 검증 가변 객체(JVM 일반 객체) / `Mutex<T>` ↔ `synchronized` + 내부 필드 / `#[derive(...)]` ↔ Lombok `@Data`/`@Builder`. *결정적 차이* 한 단락: JVM은 *"참조 보유 + 동기화는 관행"*인 단일 모델인 반면, Rust는 *"누가 소유하고 누가 빌리는가 + 단일/멀티 스레드 + 컴파일/런타임 검증"*을 표 한 장으로 *명시적으로 골라야* 한다. 처음엔 부담이지만, *그 선택이 코드에 박혀 있다*는 사실이 6개월 뒤에 가장 큰 보상이 된다. unsafe ↔ JNI 자체(JVM도 native 코드 경계는 모두 unsafe).
- **예상 분량:** 16,000자
- **함께 해보자:** 작은 트리 구조(예: `Node { value: i32, children: Vec<Rc<RefCell<Node>>> }`)를 만들어 한 노드의 값을 바꿔보자. `Rc<RefCell<T>>`가 어떻게 *공유 가변*을 단일 스레드에서 풀어내는지를 손에 묻혀보자. 그다음 `cargo expand`로 `#[derive(Debug)]`가 무슨 코드를 만들어내는지 펼쳐보자. *(이 `Rc<RefCell<T>>` 패턴은 9장에서 *Send 위반으로 컴파일이 거부되는* 사례로 다시 호출되고, unsafe는 15장 JNI 함수 시그니처에서 다시 호출된다.)*

---

### 챕터 9. 동시성 기초 — 스레드, channel, Mutex, 그리고 `Send`/`Sync`
- **핵심 질문:** `synchronized`가 컴파일러가 강제하는 형태로 옮겨오면 어떤 모양이 되는가? Rust는 어떻게 "data race를 컴파일 타임에 차단"하는가?
- **주요 내용:**
  - `std::thread::spawn`과 join — JVM `Thread`/`ExecutorService`와의 1:1 비교.
  - `std::sync::mpsc` 채널 — Java `BlockingQueue`/Kotlin `Channel`의 감각.
  - `Arc<Mutex<T>>` 패턴 — 8장에서 본 표를 *멀티스레드*에 본격 적용. 5장 카운터의 회수.
  - **Send/Sync 마커 트레잇** (5장에서 심은 복선의 회수): `Send`는 "소유권 이동 가능", `Sync`는 "동시 참조 가능". 컴파일러가 자동으로 implement해주지만, 8장의 `Rc<T>`가 Send가 아니라서 멀티스레드에 못 들어가는 사례를 손으로 보여준다.
  - lock guard의 RAII — "lock 안 풀고 return" 사고가 *구조적으로* 불가능하다.
  - JVM의 `@ThreadSafe` 어노테이션이 강제력 없는 주석이라면, Rust의 Send/Sync는 강제력 있는 컴파일러 검증.
- **JVM 대응물:** `std::thread` ↔ `Thread`/`ExecutorService`, `Arc<Mutex<T>>` ↔ `synchronized` + 필드 + `AtomicReference`, `mpsc::channel` ↔ `BlockingQueue`/Kotlin `Channel`, `Send`/`Sync` ↔ `@ThreadSafe`/`@Immutable`(단 강제력 차이). *결정적 차이* 한 단락: JVM에서 `@ThreadSafe`/`@GuardedBy`는 *문서이자 분석 도구의 힌트*일 뿐이다 — 어기면 *런타임의 한참 후에* 데이터 손상으로 드러난다. Send/Sync는 *컴파일러의 거부*다.
- **예상 분량:** 14,000자
- **함께 해보자:** 100개 스레드가 동시에 카운터를 +1하는 코드를 짜보자. 첫 시도는 의도적으로 Mutex 없이 — 컴파일러가 무엇을 거부하는지 보자. 그다음 `Arc<Mutex<i64>>`로 고쳐 통과시켜 보자. 마지막으로 `Rc<Mutex<i64>>`로 바꾸면 컴파일러가 무엇을 추가로 거부하는지 확인하자(Send 트레잇 결여). *(이 `Arc<Mutex<T>>` 패턴은 11장 axum의 State에서 다시 호출되고, Send 위반은 10장 tokio `spawn`에서 비슷한 모양으로 다시 만난다.)*

---

### 챕터 10. async와 tokio — Spring WebFlux/Kotlin Coroutine 다음의 모델
- **핵심 질문:** async/await는 Kotlin Coroutine과 무엇이 같고 무엇이 다른가? tokio는 왜 사실상 표준이 됐고, 어떤 함정을 미리 알아야 하는가?
- **주요 내용:**
  - Rust의 async는 stackless coroutine. async 함수는 `Future` trait을 구현하는 상태 머신으로 컴파일된다. await는 그 상태 머신의 한 지점.
  - **runtime을 직접 골라야 한다**: 표준 라이브러리에는 executor가 없다. tokio가 사실상 표준(20,768개 crate가 의존). async-std는 2025년 sunset, smol이 작은 빌딩 블록으로 부상.
  - tokio의 work-stealing 스케줄러 한 그림 — Go·Erlang의 검증된 패턴.
  - `tokio::spawn` / `tokio::select!` / `JoinHandle` — 첫 동시 작업.
  - `tokio::sync::{mpsc, oneshot, broadcast, watch}` — 9장의 std mpsc 다음 단계.
  - **세 가지 함정** (함정 2의 본격 처방):
    1) spawn한 task의 JoinHandle을 안 잡으면 cancel될 수 있다.
    2) await 지점을 가로지르는 동기 Mutex guard는 데드락 — `tokio::sync::Mutex`로 또는 가드 범위 좁히기.
    3) async 함수 안 blocking 호출 → `tokio::task::spawn_blocking`으로 분리.
  - async fn in trait의 stabilize(1.75)와 dyn-safety 미해결 — 여전히 `async-trait` crate가 필요한 경우.
  - 1장에서 적었던 회사 운영 사고 노트로 돌아오기 — 그것이 데드락이었다면 이 챕터의 어떤 도구가 잡았을지.
  - **JVM 4종 비교 표**: Spring WebFlux(Reactor) / Kotlin Coroutine / Java CompletableFuture / Java 21 Virtual Thread / Rust async — 각각의 trade-off 한 줄.
- **JVM 대응물:** Rust async의 가장 가까운 사용 감각은 Kotlin Coroutine(`suspend`+structured concurrency). Spring WebFlux의 callback chain과 backpressure는 의도가 좋지만 Rust async가 더 명시적·sequential. Java 21 Virtual Thread는 다른 축(스레드를 가볍게)의 답. *결정적 차이* 한 단락: Kotlin coroutine은 *runtime이 표준 라이브러리에 묶여 있고* `suspend`가 함수 색깔이 *라이브러리 컨벤션*인 반면, Rust는 runtime을 *프로젝트가 직접 고르고* `async`/`await`가 *컴파일러가 만든 상태 머신*이다. 그래서 더 명시적이고, 함정의 위치도 다르다.
- **예상 분량:** 20,000자
- **함께 해보자:** tokio로 "10개의 외부 HTTP 호출을 동시에 보내고 결과를 모아 합산"하는 작은 함수를 짜보자. 같은 일을 Java CompletableFuture로 짠다면 어땠을지, Kotlin coroutine으로 짠다면 어땠을지 한 단락씩 비교해보자. 그다음 await를 가로지르는 `std::sync::Mutex`를 일부러 넣어보고, 컴파일러/clippy가 무엇을 경고하는지 확인하자. *(이 동시 호출 패턴은 11장 axum 핸들러 안의 외부 API 호출에서 다시 호출되고, Mutex/await 함정은 16장 운영 사고 회고에서 한 번 더 만난다.)*

---

### 챕터 11. axum으로 첫 HTTP 서비스 — Spring Controller가 Rust로 보이는 순간
- **핵심 질문:** `@RestController`/`@PathVariable`/`@RequestBody`/`@Autowired`로 짜던 핸들러가 axum에서는 어떤 모양이 되는가? tower의 `Service` 트레잇은 Spring의 Filter/Interceptor/AOP를 어떻게 한 모델로 통일하는가?
- **주요 내용:**
  - 프레임워크 지형: **axum**(tokio 팀, 가장 활발), **actix-web**(actor, 최고 성숙도), **loco-rs**("Rust on Rails", Spring Boot의 batteries-included 감각).
  - axum의 핵심: 핸들러는 그냥 async 함수. Extractor 패턴(`Path`, `Query`, `Json`, `State`).
  - 첫 핸들러 코드: `async fn get_user(Path(id): Path<i64>, State(pool): State<PgPool>) -> Result<Json<User>, AppError>` — Spring 시그니처와 한 줄 비교.
  - **State 기반 의존성 주입**: `@Autowired` 없이도 컴파일러가 type 기반으로 검증. 의존성 그래프가 코드에 그대로 보인다. (12장 sqlx 통합 절에서 다시 본격 사용한다는 다리 — 10장의 분량 부담을 12장으로 일부 옮겨 17,000자대 유지.)
  - **tower `Service<Request>` trait**: 비동기 함수(요청→응답)를 일급 시민으로. `Layer`로 합성. axum/tonic(gRPC)/hyper/reqwest가 같은 추상화 위에 있어서 미들웨어 cross-framework 재사용.
  - 미들웨어 실전: 인증, 로깅, CORS, rate limit — Spring Filter/Interceptor/AOP가 한 모델로 통일된 셈.
  - 라우팅과 nested router, `Router::merge`/`nest`.
  - **에러 처리 — 7장의 `Result<T, AppError>`를 `IntoResponse`로**: 7장에서 만든 `AuthError` enum이 HTTP 401/429/500으로 자연스럽게 매핑되는 모양. 7장 함께해보자의 회수 지점.
  - 성능 한 줄: 단순 시나리오에서 axum이 Spring Boot 대비 ~10x 처리량/1/15 latency/1/23 메모리(reference 8.4의 인용 — 단 *비즈니스 로직이 깊어지면 격차가 줄어든다*는 단서를 함께).
- **JVM 대응물:** axum extractor ↔ `@PathVariable`/`@RequestParam`/`@RequestBody`, `State<T>` ↔ `@Autowired`, tower `Layer` ↔ Spring `Filter` + `HandlerInterceptor` + `@Aspect`, axum `Router` ↔ `@RequestMapping` 트리, loco-rs ↔ Spring Boot starter. *결정적 차이* 한 단락: Spring은 *어노테이션과 reflection*으로 핸들러를 *런타임에* 매핑한다 — 그래서 *애플리케이션이 뜨는 순간*까지 잘못된 시그니처를 모른다. axum은 *타입과 trait 한 묶음*으로 *컴파일 타임에* 매핑한다 — 잘못된 핸들러는 *빌드*가 거부한다.
- **예상 분량:** 17,000자
- **함께 해보자:** Spring으로 짜본 적 있는 작은 REST 엔드포인트 하나(예: `GET /users/{id}`, `POST /users`)를 axum으로 옮겨보자. State에 `Arc<DashMap<i64, User>>`을 in-memory로 두고 시작해도 좋다. tower Layer를 한 개 끼워 모든 요청에 `X-Request-Id` 헤더를 자동 부여해보자. *(이 in-memory 서비스는 12장에서 sqlx + PostgreSQL로 옮겨가 다시 호출된다.)*

---

### 챕터 12. 데이터베이스 — sqlx로 컴파일 타임 검증된 SQL을, sea-orm으로 친숙한 ORM을
- **핵심 질문:** JPA·MyBatis·QueryDSL의 출신은 sqlx·sea-orm·diesel 중 어디로 가야 자연스러운가? "컴파일 타임에 SQL을 검증한다"는 약속의 진짜 의미는 무엇인가?
- **주요 내용:**
  - 세 라이브러리 비교 표 (reference 9.4 기반): sqlx(raw SQL + 컴파일 타임 검증) / diesel(타입 기반 query DSL, 가장 type-safe) / sea-orm(Active Record, async-first).
  - 출신별 추천: MyBatis → sqlx, JPA/Hibernate → sea-orm, QueryDSL → diesel.
  - **sqlx 실전**: `sqlx::query!("SELECT id, name FROM users WHERE id = $1", id)` 매크로가 컴파일 시점에 실제 DB에 접속해 SQL을 검증. 컬럼/타입이 틀리면 빌드가 깨진다.
  - **offline 모드**: `cargo sqlx prepare` → `.sqlx/` 메타데이터 → CI에서 DB 없이 빌드. 팀에 도입할 때 가장 자주 묻는 부분.
  - **sea-orm 한 그림**: Entity, ActiveModel, find_by_id/save. loco-rs의 기본 ORM.
  - 마이그레이션: `sqlx-cli`/`sea-orm-cli`/`diesel migration` — Flyway/Liquibase의 감각.
  - 트랜잭션: `pool.begin().await?` → `tx.commit().await?`. Spring `@Transactional`이 sugar로 가려놓던 경계가 코드에 그대로 보인다.
  - 11장의 axum State에 `PgPool`을 끼워 작은 CRUD를 완성한다(11장의 in-memory를 PostgreSQL로 마이그레이션).
- **JVM 대응물:** sqlx ↔ MyBatis(+ 컴파일 타임 검증), sea-orm ↔ Spring Data JPA / Hibernate, diesel ↔ QueryDSL / jOOQ, `cargo sqlx prepare` ↔ MyBatis Generator, `pool.begin()`/`tx.commit()` ↔ `@Transactional`(단 명시적 경계). *결정적 차이* 한 단락: Spring `@Transactional`은 *AOP proxy*로 메서드 경계를 가로채 트랜잭션을 관리한다 — *self-invocation 안 됨* / *체크 예외 vs unchecked 차이* / *propagation 옵션* 같은 함정이 인터뷰 단골 질문이 된다. Rust의 `pool.begin()`/`tx.commit()`은 *그저 코드의 한 줄*이라 함정이 *모양으로 보인다*.
- **예상 분량:** 18,000자
- **함께 해보자:** 11장의 작은 in-memory CRUD를 PostgreSQL 위로 옮겨보자. 첫 시도는 sqlx로. SQL 한 줄을 일부러 틀리게 적은 다음 `cargo build`가 에러로 무엇을 보여주는지 손으로 확인하자. 같은 도메인을 sea-orm으로 다시 짜보고, 두 코드의 한 줄 한 줄이 어떻게 다른 trade-off인지 한 단락으로 정리하자. *(이 CRUD 서비스는 13장에서 workspace로 쪼개지고, 14장에서 musl + distroless 8MB 컨테이너로 빌드되어 다시 호출된다.)*

---

### 챕터 13. 테스트·품질·도구 인프라·CLI — cargo가 IDE·Sonar·JMH·picocli·OWASP를 모두 안고 있다
- **핵심 질문:** JUnit/Mockito/JMH/SpotBugs/Sonar/picocli/Spring Shell/OWASP Dependency Check가 흩어져 있던 일들이 cargo 한 도구 안에서 어떻게 정리되는가? 컴파일 시간이 길어질 때 무엇을 만져야 하는가? 첫 매크로는 어떻게 짜는가?
- **주요 내용:**
  - **단위 테스트**: `#[cfg(test)] mod tests {}`. 통합 테스트는 `tests/` 디렉터리. JUnit이 외부 도구라면 cargo test는 언어 코어에 들어와 있다.
  - **doctest**: 주석 안 ` ```rust ... ``` ` 코드가 자동 테스트. JavaDoc + JUnit이 한 줄로 합쳐진 셈. 문서가 곧 살아있는 예제.
  - **mocking**: `mockall` crate, 그리고 trait + 더미 구현으로 "mock 없는 mocking" 패턴.
  - **clippy 100여 lint 카테고리**: SpotBugs/Sonar의 Rust 표준판. 입문자가 가장 빨리 좋은 코드로 가는 길.
  - **rustfmt**: ktlint/google-java-format. 한 줄 설정으로 팀 통일.
  - **criterion**: 통계적 벤치마크. JMH의 Rust 버전. warm-up·outlier 처리·HTML 리포트.
  - **cargo workspace** 본격 적용: 도메인/인프라/웹 crate를 분리한 monorepo 패턴(12장 axum + sqlx 서비스를 쪼개기). Gradle multi-module과 비교. `resolver = "2"` feature unification 함정 한 단락(reference 6 인용).
  - **컴파일 시간 함정과 처방 (이전 14장에서 이동)**: workspace 분할, `cargo check` 우선, sccache, mold linker, codegen-units 조정, dev/release 프로파일 분리. 2025 Compiler Performance Survey에서 27%가 가장 큰 불만으로 지목한 영역(인용). *컴파일 시간은 도구 인프라 영역이라 출시 챕터(14장)가 아니라 여기에 있다.*
  - **보안 도구 한 절 (약 2,000자)**: `cargo audit`(RustSec Advisory DB) / `cargo deny`(license·source·dependency policy) / `cargo vet`(supply chain 감사). OWASP Dependency Check / Snyk에 익숙한 JVM 출신이 *바로 손에 잡을* 수 있는 매핑. CI 파이프라인에 게이트로 박는 패턴.
  - **CLI 도구 — clap**: `#[derive(Parser)]`만 붙이면 argparse 끝. subcommand·flag·env var·default·completion까지. picocli + Spring Shell이 한 라이브러리에 모인 셈. cargo·ripgrep·bat·fd·exa의 친숙한 CLI 감각이 모두 clap. (2장의 hello-jvm CLI를 완성형으로 회수.)
  - **"내 매크로 만들어보기" 한 절 (약 3,000자)**: declarative `macro_rules!` 한 예제(예: `assert_close!(a, b, eps)`) + procedural attribute macro 한 예제(예: `#[my_handler]`). `syn`, `quote`, `cargo expand`. 깊지는 않게 *"매크로는 작성도 할 수 있는 도구다"*만 손에 묻혀준다.
  - 사전 커밋 훅과 CI 파이프라인 권장 형태: `cargo fmt --check && cargo clippy -- -D warnings && cargo test && cargo audit && cargo deny check && cargo bench --no-run`.
- **JVM 대응물:** cargo test ↔ JUnit, doctest ↔ JavaDoc + JUnit 통합, mockall ↔ Mockito, clippy ↔ SpotBugs + Sonar, rustfmt ↔ ktlint/google-java-format, criterion ↔ JMH, clap ↔ picocli + Spring Shell, cargo workspace ↔ Gradle multi-module, `resolver = "2"` ↔ Gradle dependency resolution strategy, `cargo audit`/`deny`/`vet` ↔ OWASP Dependency Check / Snyk / FOSSA, sccache/mold ↔ Gradle build cache + remote cache. *결정적 차이* 한 단락: JVM 진영은 *언어 한 개에 도구 수십 개*를 조합하는 ecosystem 모델인 반면, Rust는 *cargo 한 도구가 핵심을 다 안고* 외부 도구는 보강만 한다. 신규 멤버 onboarding 시간이 *체감으로* 다르다.
- **예상 분량:** 18,000자
- **함께 해보자:** 12장의 axum + sqlx 서비스를 도메인/인프라/웹 세 crate로 쪼개 workspace로 묶어보자. 도메인 crate의 핵심 함수 하나에 doctest를 붙여 `cargo test --doc`로 통과시켜 보고, criterion으로 그 함수의 처리량을 측정해 HTML 리포트를 열어보자. CI에 `cargo audit`/`cargo deny check`를 게이트로 끼워 *고의로 취약한 의존성*을 추가해 빌드가 깨지는 모습을 한 번 보자. 그다음 `assert_close!` 매크로를 직접 짜서 도메인 테스트에서 써보자. *(이 workspace는 14장에서 musl + distroless로 빌드되어 다시 호출되고, `cargo audit` 게이트는 16장 조직 도입의 *최소 조건*으로 다시 호출된다.)*

---

### 챕터 14. 출시 — 8MB 컨테이너와 OpenTelemetry 관측
- **핵심 질문:** Spring Boot fat jar + JVM 200MB 이미지로 굴리던 운영을, Rust는 어떻게 한 자릿수 MB로 끝내는가? 그리고 그 안의 일을 어떻게 들여다보는가?
- **주요 내용:**
  - **musl + 정적 바이너리**: `x86_64-unknown-linux-musl` 타겟으로 빌드. glibc 의존이 사라진다.
  - **multi-stage Dockerfile 표준 패턴**: builder stage에 `cargo build --release --target x86_64-unknown-linux-musl`, runtime stage는 `gcr.io/distroless/static-debian12` 또는 `scratch`. 결과: **8~10MB 이미지**.
  - **release 프로파일 튜닝**: `lto = "thin"`, `codegen-units = 1`, `strip = true`, `panic = "abort"`의 trade-off.
  - **관측(Observability) 표준 스택**: `tracing` + `tracing-subscriber` + `tracing-opentelemetry`. span에 구조화된 필드. OTLP exporter로 Datadog/Jaeger/Tempo로 전송. Spring Cloud Sleuth + OpenTelemetry SDK와 거의 같은 모델.
  - **프로파일링**: `cargo flamegraph`(perf 기반), `tokio-console`(async task), `samply`(sampling). JFR/Async Profiler 출신은 가장 평탄한 영역.
  - **헬스체크와 graceful shutdown**: tokio signal로 `SIGTERM`을 잡아 in-flight 요청을 마무리하는 패턴.
  - **컴플라이언스 한 단락**: ONCD/NSA의 메모리 안전 권고 맥락 — 정부·금융·국방 도메인은 이미 "왜 안전한 언어를 쓰지 않느냐"를 묻는 단계. (1장에서 본 권고의 회수.)
  - *(컴파일 시간 함정 절은 13장으로 이동했다. 14장은 *빌드·관측·프로파일링·컴플라이언스* 4개 영역으로 슬림화.)*
- **JVM 대응물:** musl 정적 바이너리 ↔ GraalVM native-image, distroless ↔ jlink + alpine-jre, `tracing` ↔ Spring Cloud Sleuth, `tracing-opentelemetry` ↔ OpenTelemetry Java SDK, `cargo flamegraph` ↔ Async Profiler / JFR, `tokio-console` ↔ JVM Thread Dump + VisualVM(단 async 인사이트는 Rust 측이 더 깊다). *결정적 차이* 한 단락: GraalVM native-image도 작은 이미지를 만들지만 *reflection/dynamic proxy 깨짐* / *AOT 빌드 시간 폭증* / *런타임 메모리 안전성은 여전히 GC*라는 trade-off가 있다 — Rust는 처음부터 그 길로 설계된 언어다.
- **예상 분량:** 14,000자
- **함께 해보자:** 12~13장의 axum 서비스를 musl + distroless로 빌드해 이미지 크기를 측정하자. 같은 의미의 Spring Boot 서비스(`./mvnw spring-boot:build-image`) 이미지 크기와 한 줄로 비교한 뒤, `tracing` 한 줄(`#[tracing::instrument]`)을 핸들러에 붙여 OTLP exporter로 Jaeger 컨테이너에 트레이스가 들어가는 모습을 직접 보자. *(이 8MB 이미지는 15장에서 *Spring 시스템 옆 사이드카*로 배치되어 다시 호출된다.)*

---

### 챕터 15. JVM과 함께 — FFI·JNI·Project Panama·폴리글랏 아키텍처
- **핵심 질문:** Spring 시스템에 Rust를 *떠나지 않고* 어떻게 들이는가? JNI / Project Panama / C ABI / `#[repr(C)]` — 어느 다리를 어떤 모양으로 놓는가? UB(undefined behavior) 회피의 표준 패턴은 무엇인가?
- **주요 내용:**
  - **폴리글랏 전략의 정석**: 비즈니스 로직 다수는 Spring/Kotlin 유지. **hot path 추출 패턴** — API gateway, ingress, 데이터 직렬화, 인증, 매칭 엔진, 미디어 처리. **사이드카 패턴** — 14장의 8MB 컨테이너를 Spring 시스템 옆에 배치해 gRPC/HTTP로 통신. **in-process FFI 패턴** — JNI/Panama로 같은 프로세스 안에서 호출. 세 패턴의 trade-off 표("거리·격리·지연·복잡도" 4축).
  - **JNI로 JVM에서 Rust 호출**: `jni` crate, `#[no_mangle] pub extern "system" fn Java_...`, JNIEnv·jobject 추상화. 8장에서 깐 unsafe 절의 본격 회수 — *왜 JNI 함수가 unsafe인가*를 한 단락으로.
  - **C ABI와 `#[repr(C)]`**: Rust 구조체를 C ABI 호환 모양으로 강제. `#[repr(C)]`/`#[repr(transparent)]`/`#[repr(u8)]`의 차이. 데이터 경계에서 가장 흔한 사고 — *Rust 측 layout 가정이 다른 언어 측 가정과 어긋남*.
  - **Project Panama (JEP 442/454, Java 22+)**: JVM 차세대 native interop. Foreign Function & Memory API로 Rust dylib을 JNI 보일러플레이트 없이 호출. `jextract`로 헤더에서 자동 바인딩. *현재 가장 깔끔한 미래 — 단, 정량 비교 자료는 본 책의 리서치 한계(reference 8 한계 2)로 잠시 미뤄둔다*.
  - **JNR-FFI 대안**: C ABI 기반, Rust 측에 JNI 의존성 없음. JNI보다 가볍지만 Panama 등장으로 위치가 애매해지는 중.
  - **UB 회피의 표준 패턴**: ① unsafe API는 항상 safe wrapper 뒤에 둔다(Rust 측). ② lifetime이 불분명한 raw pointer는 즉시 owned로 복사한다. ③ JVM 측에서 던진 Java 객체는 *JNIEnv local frame*을 명시적으로 관리. ④ panic은 절대 FFI 경계를 넘지 않게(`std::panic::catch_unwind`로 잡기). ⑤ `cargo miri`로 unsafe 검증. 학술 인용 한 줄: deepSURF (IEEE S&P 2026) — FFI 경계의 메모리 안전성 자동 검증.
  - **Mozilla application-services 패턴**: 한 Rust crate를 iOS/Android/Desktop이 공유. 모바일까지 확장하는 *경계의 한 변형*.
  - **WebAssembly 한 단락**: 사이드카가 아닌 또 다른 배포 단위로 떠오르는 중. wasmtime / wasmer / Spin / wasmCloud의 한 그림. 백엔드 책 스코프 밖이지만 *결을 풍성하게*.
  - **no_std·임베디드 한 단락**: 백엔드 출신이 가장 만나기 어렵지만 알아두면 좋은 영역. 200~400자만 *fact 짚기* (reference 8 한계 3 약속의 회수).
  - **사례 한 편의 솔직한 회상**: "I Replaced My Spring Boot Microservice with Rust and Go" — *단일 hot path*만 분리해 AWS 비용 81% 절감. 폴리글랏 아키텍처의 표본 사례.
- **JVM 대응물:** JNI ↔ JNI(상호 방향, JVM 출신은 이미 절반 안다), Panama ↔ Java FFM API, C ABI / `#[repr(C)]` ↔ JNA `Structure` / Panama `MemoryLayout`, gRPC 사이드카 ↔ Spring Cloud Gateway 사이드카, application-services ↔ Kotlin Multiplatform (목적은 다르지만 cross-platform 코드 공유 발상). *결정적 차이* 한 단락: JNI에서 JVM 출신은 *Java 측 코드*를 짜본 적이 있다 — 이 챕터는 그 익숙함의 *반대편(Rust 측)*을 이어주는 다리다. Panama는 *그 다리를 짧게 줄여줄* 미래다.
- **예상 분량:** 14,000자
- **함께 해보자:** 13장 workspace의 도메인 crate에서 *순수 함수 하나*(예: 입력 문자열의 SHA-256 해시 + Base64)를 골라 JNI로 노출해보자. Spring Boot 측에 작은 컨트롤러를 만들어 그 함수를 호출하고, JFR로 measure해 같은 함수를 Java로 짠 것과 처리량을 비교하자. 그다음 같은 함수를 Panama 바인딩으로도 노출해 보일러플레이트 양 차이를 손으로 확인하자. *(이 hot path 분리 경험은 16장의 *조직 도입 전략*에서 다시 호출된다.)*

---

### 챕터 16. Rust로 가는 길 — 사람·조직·커리어, 그리고 매듭
- **핵심 질문:** 4~6개월의 학습 곡선을 *팀 차원에서* 어떻게 설계하는가? Rust 도입의 *정치적* 함정은 무엇이고 어떻게 피하는가? 한국에서 Rust로 일을 하려면 어디로 가야 하는가? 이 책 다음의 한 걸음은?
- **주요 내용:**
  - **사례 두 편의 솔직한 대조** (reference 4.8):
    - "I Replaced My Spring Boot Microservice with Rust and Go" (15장에서 회수 시작) — 단일 hot path만 분리해 AWS 비용 81% 절감. *기술적·정치적 모두 성공*.
    - "I Rewrote A Java Microservice In Rust And Lost My Job" — 기술적 성공·정치적 실패. *팀에 Rust를 알 줄 아는 사람이 1명뿐이면 bus factor가 위협*.
    - Dropbox Magic Pocket의 그늘 — "너무 잘 돌아가서 손이 안 갔고, 원작자가 떠난 뒤 유지보수 인력이 부족해졌다."
  - **학습 곡선의 정석**: corrode 권고를 인용 — 4~6개월 적응 기간. 처음 PoC는 비크리티컬 모듈 10~20%만. 팀 전원이 같이 배우는 study + 1주 1회 코드 리뷰 모임 같은 조직 설계 한 단락. 부록 D의 4~6개월 학습 가이드로 다리.
  - **조직 도입의 정치 — 5가지 권고**: ① 첫 도입은 *기존 시스템 옆*에 (사이드카 / hot path 분리). ② Rust를 아는 사람은 항상 *2명 이상*(bus factor). ③ 코드 리뷰 가능한 시니어 1명을 먼저 길러내고 시작. ④ CI에 `cargo fmt`/`clippy`/`test`/`audit` 게이트는 *처음부터*. ⑤ 동료 팀에게 *왜 Rust를 골랐는지* 한 페이지 RFC를 남긴다 — *기술이 아니라 정치 문서*.
  - **한국 커뮤니티와 자료 매듭**: rust-kr.org / 『러스트 프로그래밍 언어』 한국어판(rinthel) / 『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』(제이펍) / 한국 개발자 후기 4편(blog.cro.sh 외) / 채용 신호. 우아한형제들·토스·카카오·네이버의 공식 사용기는 본 책 시점에 미확인 — *이 책이 출간된 뒤 그 글이 나오기를 함께 기다리자*는 매듭.
  - **커리어 경로 한 단락**: 백엔드 시니어가 Rust를 손에 쥐었을 때 열리는 인접 영역 — 시스템·인프라(데이터베이스 엔진·proxy·sidecar), 임베디드, blockchain, AI infra(tokenizer·inference proxy·vector DB). *JVM 백엔드의 다음 챕터*로서의 Rust.
  - **이 책의 마지막 한 줄**: "Rust는 JVM의 대체가 아니라 무기 추가다. Spring 다음의 시스템을 손에 쥐자." *(표지·1장 "이 책의 자리"·이 결론이 한 줄로 정렬된다.)*
  - **다음 한 걸음**: 부록 D의 학습 가이드로 4~6개월 일정 짜기. rust-kr.org 가입. 자기 회사 시스템 지도에서 *가장 작은 hot path 하나*를 골라 PoC 시작.
- **JVM 대응물:** 학습 곡선 자체에는 직접 대응물이 없지만, Java 5→8(lambda·stream)·Java 8→17(record·sealed·pattern)의 마이그레이션 경험이 *언어가 새 사고 모델을 요구할 때 팀이 어떻게 적응하는지*의 가장 가까운 닻이다. *결정적 차이* 한 단락: Java 버전 마이그레이션은 *기존 코드를 그대로 둬도 동작*하지만, Rust 도입은 *새 사고 모델 자체를 받아들여야* 한다. 그래서 *학습은 더 가파르고 보상은 더 크다*.
- **예상 분량:** 12,000자
- **함께 해보자:** 자기 회사 시스템의 모듈 지도를 한 장 그려보자. 비즈니스 로직(Spring/Kotlin 유지) / hot path 후보(Rust 사이드카로 분리 가능) / 통신 경계(gRPC vs JNI vs HTTP)를 색깔로 구분하자. *지금 당장 Rust로 옮길 수 있는 가장 작은 모듈 하나*를 골라, 다음 달 사이드 PoC의 출발점으로 삼자. 그리고 부록 D의 4~6개월 학습 가이드를 꺼내 첫 4주 일정을 캘린더에 박자. *(이것이 이 책의 마지막 함께 해보자다 — 다음 호출 지점은 더 이상 책 안이 아니라 너의 코드다.)*

---

### 부록 A. JVM ↔ Rust 한 페이지 매핑 표
- **목적:** 본문 16장에 산발적으로 박힌 "JVM 대응물" 매핑을 한 페이지에 모은다. 책상 옆에 펴 놓고 보는 *cheatsheet의 cheatsheet*.
- **카테고리:** 타입 시스템 / 제어 흐름 / 모듈·패키지 / 예외·에러 처리 / 동시성·async / 빌드·의존성 / 테스트·품질 / 웹 프레임워크 / 데이터베이스 / 관측·운영. 각 카테고리 5~10행의 표.
- **예상 분량:** 7,000자

### 부록 B. cargo / rustup / clippy / fmt 치트시트
- **목적:** 매일 손에 잡는 명령 100개를 한 페이지에. JVM 출신이 *gradle*/*mvn* 명령을 외워 쓰는 감각으로.
- **구성:** rustup(toolchain 관리) / cargo 빌드·테스트·실행 / cargo workspace 명령 / clippy lint 카테고리와 자주 쓰는 deny 옵션 / rustfmt 설정 / cargo audit/deny/vet / cargo expand·flamegraph·miri. 각 명령 옆에 한 줄 설명.
- **예상 분량:** 6,000자

### 부록 C. 추천 crate 카탈로그
- **목적:** "이 일을 하려면 어떤 crate?"의 표준 답안. JVM 출신의 *Maven Central 즐겨찾기*에 해당.
- **카테고리와 대표 crate 20개+:** 웹(axum, actix-web, loco-rs, tower) / DB(sqlx, sea-orm, diesel) / async runtime(tokio, smol) / 직렬화(serde, serde_json, bincode) / 에러(anyhow, thiserror) / CLI(clap) / 관측(tracing, tracing-opentelemetry, opentelemetry, metrics) / 테스트(mockall, criterion, proptest, insta) / 빌드 도구(sccache, cargo-watch, cargo-expand, cargo-flamegraph) / 보안(cargo-audit, cargo-deny, cargo-vet) / 데이터(polars, dashmap, bytes) / FFI(jni, cbindgen). 각 crate 옆에 한 줄 한 단락 — *언제 쓰고 언제 안 쓰는가*.
- **예상 분량:** 9,000자

### 부록 D. 4~6개월 학습 가이드 — 주차별 마일스톤
- **목적:** 16장의 학습 곡선 한 단락을 *주차별 캘린더*로 풀어 책상 옆에 놓는다. corrode "9 months overtaking 10 years" 인용 기반.
- **구성:**
  - **0~4주차 (입문)**: 1~6장 + 매주 작은 예제 1개. 목표는 *borrow checker와 친구되기*.
  - **5~8주차 (표현력)**: 7~10장 + 자기 도메인 모델 + 첫 동시 작업. 목표는 *Rust로 사고하기*.
  - **9~16주차 (서비스)**: 11~14장 + 작은 axum + sqlx 서비스를 직접 출시. 목표는 *Spring 다음의 시스템 한 채*.
  - **17~24주차 (조직)**: 15~16장 + 회사 시스템에 첫 hot path PoC. 목표는 *팀에 Rust를 들이기*.
- **각 주차마다:** ① 읽을 챕터 / ② 짤 코드 / ③ 추천 외부 자료(공식 The Rust Programming Language, Rust by Example, rust-kr.org 글, 한국어 후기 4편). ④ *멈춰도 되는 신호*("이 주차에 막히면 한 주 더 써도 괜찮다 — 4~6개월 곡선의 정석이다").
- **예상 분량:** 8,000자

---

## 5. 챕터 간 흐름 (내러티브 아크)

독자의 감정 곡선은 다섯 단계로 설계됐다.

**① 의심 → 호기심 (1~2장)**: "왜 굳이?"라는 의심으로 들어온 독자가, 1장에서 ONCD/NSA 권고와 Discord/Cloudflare/Microsoft 사례, 그리고 *"이 책의 자리"* 절을 통해 *이건 의제다, 이 책이 그 의제의 안내자다*를 받아들이고, 2장에서 cargo로 5분 만에 첫 빌드를 굴려보며 *생각보다 진입은 부드럽다*는 첫 호기심을 손에 쥔다. 첫 두 챕터는 무조건 환영하는 톤 — JVM 출신이 도망가지 않게 한다.

**② 작은 성취 → 막막함 (3~4장)**: 3장에서 Java/Kotlin과 1:1 대응되는 문법을 빠르게 흡수하며 *어, 생각보다 익숙하다*고 느끼고, 끝에서 *에러 메시지 읽는 법*을 미리 배운 직후, 4장에서 소유권의 첫 벽에 부딪힌다. *왜 이게 컴파일이 안 되지?*의 막막함이 시작된다. 이 막막함을 의도적으로 한 챕터에 끝내지 않는다.

**③ 친구되기 → 표현력 (5~7장)**: borrow checker와의 싸움이 두 챕터에 걸쳐 천천히 *적 → 동료(co-author) → 친구*로 변한다. 5장에서 두 줄의 borrow 규칙으로 4장의 막막함이 풀리고, *RustBelt 한 단락*으로 *이 규칙이 학술적으로 입증됐다*는 위상 신호를 받는다. 6장에서 라이프타임 elision 덕에 *진짜로 `'a`를 써야 하는 순간은 손에 꼽힌다*는 안도가 온다. 7장에서 트레잇·제네릭·패턴매칭·에러처리(thiserror로 자기 도메인 모델링)까지 손에 쥐며 *Part 2의 매듭이 깨끗하게 닫힌다*. 책 전체의 가장 어두운 골짜기에서 빠져나오는 지점.

**④ 안전 경계 → 자신감 → 실무 (8~13장)**: 8장 스마트 포인터·매크로·*unsafe* 절에서 *Rust의 안전 경계가 어디까지인지*를 명료하게 본다 — 이 절이 깔리지 않으면 15장 JNI에서 길을 잃는다. 9장 동시성 기초로 5장 borrow의 두 줄 규칙이 *멀티스레드 안전성*으로 보상받는 순간을 맛보고, 10장 async/tokio로 Kotlin Coroutine 다음의 모델을 손에 쥔다. 11장 axum에서 *Spring Controller가 Rust로 보이는* 순간이 오고, 12장 sqlx에서 *컴파일러가 SQL까지 검증해주는* 새로운 안전성을 만난다. 13장에서 cargo가 JUnit/JMH/Sonar/picocli/OWASP를 모두 안고 있다는 사실을 정리하고, *컴파일 시간 함정 처방*과 *보안 도구 게이트*, *내 첫 매크로*까지 묶으면 독자는 *이제 실무 시스템 한 채를 Rust로 짤 수 있다*는 자신감에 도달한다.

**⑤ 출시 → 폴리글랏 → 사람 (14~16장)**: 14장에서 8MB 컨테이너와 OpenTelemetry로 *운영까지 갔다*는 매듭을 짓고, 15장에서 *JVM을 떠나지 않는 Rust 도입의 다리*를 JNI/Panama/C ABI/UB 회피로 깐다(8장 unsafe 절의 본격 회수). 마지막 16장에서 두 사례("AWS 비용 81% 절감" vs "직장을 잃었다")의 솔직한 대조, Dropbox Magic Pocket의 그늘, 4~6개월 학습 곡선, 조직 도입의 정치 5가지 권고, 한국 커뮤니티 매듭, 그리고 *기술서가 사람의 책으로 닫힌다*는 시그니처. 마지막 한 줄: *"Rust는 JVM의 대체가 아니라 무기 추가다. Spring 다음의 시스템을 손에 쥐자."*

이 곡선은 reference 6절의 두 인용 — *"9 months of [Rust] experience overtaking 10 years of [Java] experience"* (corrode)와 *"익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다"* (한국 4년차 개발자) — 의 정신을 책 한 권의 호흡으로 풀어낸 것이다. 그리고 *모든 챕터(1~16)의 "함께 해보자" 끝 한 줄*에 다음 챕터로의 다리(*"이 결과는 N장의 X 절에서 다시 호출된다"*)를 박아 책 전체가 한 줄로 꿰어지는 감각을 만든다.

---

## 6. 1라운드 리뷰 반영 요약

1. **7장 분리 (Critical)**: 기존 7장(25K, 6토픽)을 신 7장(트레잇·제네릭·패턴매칭·에러처리·anyhow/thiserror, 18K)과 신 8장(스마트 포인터·매크로·**unsafe 한 절** 3K, 16K)으로 분리. 이후 챕터 번호 한 칸씩 밀림.
2. **14장 분리 (Critical)**: 기존 14장 10절을 신 15장(FFI·JNI·Panama·C ABI·UB 회피·아키텍처, 14K)과 신 16장(사람·조직·커리어·매듭, 12K)으로 분리. 책의 마지막을 *사람*으로 닫는 시그니처.
3. **unsafe 본문 진입 (Critical)**: 신 8장에 unsafe 한 절(언제 쓰고 언제 쓰지 말 것·안전 경계의 역할). 신 15장 FFI에서 그 절을 본격 회수.
4. **메모리 모델 학술 토대 (Should)**: 5장 빌림 끝에 RustBelt / Stacked Borrows / Tree Borrows 한 단락(2K) 박음. *"바이블"의 위상 신호*.
5. **"이 책의 자리" 절 (Should)**: 1장에 다른 Rust 입문서 5종과의 차별점 한 절(1.5~2K). 표지·1장·16장 마지막 한 줄이 한 줄로 정렬.
6. **"함께 해보자"의 다리 일관화 (Should)**: 1~16장 모든 "함께 해보자" 끝 한 줄에 *"(이 결과는 N장의 X 절에서 다시 호출된다)"* 형식의 다리 박음.
7. **컴파일 시간 함정 절 이동 (Should)**: 14장(출시)에서 13장(품질·도구 인프라)으로 이동. 14장 슬림화(*빌드·관측·프로파일링·컴플라이언스* 4영역).
8. **5장 빌림 매핑 정정 (Nice-to-have)**: `&T` ↔ `final` 참조 매핑을 정정 — *"Java의 모든 참조는 늘 mutable이고 동시 접근이 허용된다, Rust는 그 일상 코드를 컴파일러가 거부한다"*는 비대칭으로 풀고, `final`은 *반례*로 짚음.
9. **13장 보강 (Nice-to-have)**: 보안 도구 한 절(`cargo audit`/`deny`/`vet`, 2K)과 매크로 작성 한 절(3K) 추가.
10. **부록 A·B·C·D 추가 (Nice-to-have)**: 본문 뒤에 JVM↔Rust 매핑 / cargo 치트시트 / crate 카탈로그 / 4~6개월 학습 가이드 4개 부록 추가(약 30K). *바이블 위상의 마무리.*
