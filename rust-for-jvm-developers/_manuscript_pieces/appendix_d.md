# 부록 D. 4~6개월 학습 가이드 — 주차별 마일스톤

이 부록은 *오늘 자기 캘린더에 첫 한 줄을 옮기는* 데 쓰기 위해 쓰였다. 16장에서 본 *정직한 그래프*를 24주짜리 마일스톤으로 풀었다. 정직한 그래프는 한 가지를 약속한다 — *4~6개월이 길게 느껴지지만, 그 곡선의 끝에서 손에 들어오는 것이 있다*. 이 약속을 받아들이고, 한 주씩 같이 가자.

기억해두자. *모든 주차에 막힐 수 있다*. 막힌 주는 *한 주 더 써도 괜찮다*. 4~6개월이라는 범위가 그 여유를 미리 깔아둔 것이다. 지치면 쉬자. 단, *완전히 멈추지는 말자*. 한 주에 *코드 한 줄*이라도 짜자.

## D.1 1단계 (1~4주차) — "컴파일러와 싸우는 시기"

### 감정의 풍경

처음 한 달은 *컴파일이 안 되는 한 시간*이 매일 한두 번씩 떨어진다. 답답하다. 그런데 이 답답함은 *모든 Rust 입문자가 통과하는 자리*다. 한국 4년차 개발자의 후기에서도 같은 한 줄이 나온다. *"처음 한 달은 borrow checker와의 싸움이었다."* 이 시기의 처방은 한 줄이면 된다. **컴파일러 에러 메시지를 그대로 따라가자.** Rust 컴파일러는 *어디가 틀렸고, 왜 틀렸고, 어떻게 고치면 되는지*를 거의 모든 메시지에서 알려준다.

### 주차별 일정

**1주차 — 환경 + 기본 문법**
- 본문: 1장 + 2장
- 짤 코드: `cargo new hello-jvm` → 인자 한 개를 받아 출력하는 CLI (clap derive)
- 외부 자료:
  - [The Rust Programming Language 한국어판](https://doc.rust-kr.org/) Ch.1~3 (설치, Hello World, 변수와 타입)
  - [Rust by Example](https://doc.rust-lang.org/rust-by-example/) Hello World
- 멈춰도 되는 신호: rustup·cargo가 잘 깔리고 `cargo run`이 화면에 한 줄 출력하면 1주차는 성공이다.

**2주차 — 변수·타입·함수·모듈**
- 본문: 3장
- 짤 코드: 자기가 잘 아는 Java/Kotlin 도메인 클래스 한 개(예: `User`)를 Rust struct로 옮기기. `#[derive(Debug, Clone)]` 붙여보기.
- 외부 자료:
  - [Rust 한국어판](https://doc.rust-kr.org/) Ch.5~6 (Struct, Enum)
  - [Rust for Java Developers — tkaitchuck](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)
- 멈춰도 되는 신호: `String` vs `&str`이 *완전히 이해 안 돼도 괜찮다*. 4주차에 한 번 더 만난다.

**3주차 — 소유권의 첫 벽**
- 본문: 4장
- 짤 코드: 책에 나온 `let s = String::from("hi"); let t = s; println!("{s}");` 같은 코드들을 *컴파일러가 거부하는 모양*으로 손에 묻혀보기. clone과 borrow 둘 다로 풀어보기.
- 외부 자료:
  - [Rust 한국어판](https://doc.rust-kr.org/) Ch.4 (Ownership)
  - [scalalang2, "Rust의 소유권 이야기" — CURG](https://medium.com/curg/rust%EC%9D%98-%EC%86%8C%EC%9C%A0%EA%B6%8C-%EC%9D%B4%EC%95%BC%EA%B8%B0-a4c19c1b2c10) — 한국어 입문자 정리
- 멈춰도 되는 신호: *"왜 이게 안 되지?"*가 매일 떠오르면 정상이다. 4주차의 borrow가 답이다.

**4주차 — 빌림과 라이프타임**
- 본문: 5장 + 6장
- 짤 코드: 카운터 구조체 만들고 `&mut`을 *동시에* 두 개 시도해 컴파일러가 거부하는 모양 보기. NLL로 풀기. 함수 시그니처 한 개를 elision으로 시작해서 컴파일러가 `'a`를 요구하는 시점 보기.
- 외부 자료:
  - [Without Boats: Pin](https://without.boats/blog/pin/) — 6장 끝에 미리 펼쳐두면 10장에서 도움
  - [appleseed, "일주일만에 Rust에 매료되다"](https://blog.appleseed.dev/post/fascinated-by-rust-in-a-week/) — 한국어 동기 부여
- 멈춰도 되는 신호: 라이프타임 elision의 *세 가지 규칙*이 손가락으로 짚어지면 1단계 성공이다. `'static`은 7장 이후에 다시 만난다.

### 1단계 매듭

4주차 끝에서 자네가 손에 쥔 것은 *컴파일러와 대화할 줄 아는 기본기*다. 아직 친구는 아니다. *어떤 자리에서 거부당하는지*는 안다. 거부당했을 때 *clone으로 일단 풀어두는 패턴*과 *borrow로 옮겨가는 패턴*이 손에 묻었다. 이것만으로도 1단계는 충분하다.

## D.2 2단계 (5~8주차) — "패턴 인식이 시작되는 시기"

### 감정의 풍경

borrow checker가 *까다로운 시니어*에서 *익숙한 동료*로 변하기 시작하는 시기다. 같은 패턴이 두세 번 반복되면 *왜 거부당하는지*가 보이고, *어떻게 고치면 되는지*가 손가락에 묻어난다. 이 시기의 보상은 두 가지다. 하나는 *Rust로 사고하는 법*이 시작되는 것. 다른 하나는 *7장의 표현력 도구상자*를 손에 쥐면서 *코드의 모양이 점점 깨끗해지는* 경험.

### 주차별 일정

**5주차 — 트레잇·제네릭·패턴 매칭**
- 본문: 7장 전반부 (트레잇, 제네릭, enum + match)
- 짤 코드: 사용자 인증 도메인을 작은 enum으로 표현 (`enum AuthError { ... }`).
- 외부 자료:
  - [Rust 한국어판](https://doc.rust-kr.org/) Ch.10 (Generic Types, Traits, Lifetimes)
  - [softwaremill: Rust Static vs. Dynamic Dispatch](https://softwaremill.com/rust-static-vs-dynamic-dispatch/)

**6주차 — 에러 처리 (Result/Option/?/anyhow/thiserror)**
- 본문: 7장 후반부
- 짤 코드: 위 `AuthError`에 thiserror 적용. `Result<User, AuthError>` 반환 함수 작성. `?` 연산자와 `From` 변환 손에 묻히기.
- 외부 자료:
  - [Rust Error Handling Compared: anyhow vs thiserror vs snafu — DEV.to](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003)
  - 1장에서 적어둔 *운영 사고 노트* 다시 펴기 — 이번 주에 답을 한 줄 채워보기

**7주차 — 스마트 포인터 + 매크로 + unsafe 진입**
- 본문: 8장
- 짤 코드: `Rc<RefCell<Node>>` 트리 구조 만들어보기. `cargo expand`로 `#[derive(Debug)]`가 펼쳐지는 모양 보기.
- 외부 자료:
  - [The Rustonomicon — Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html) — 9주차 복선
  - [Cui et al. "Is unsafe an Achilles' Heel?"](https://arxiv.org/abs/2308.04785) — unsafe 함정 다섯 가지

**8주차 — 동시성 기초**
- 본문: 9장
- 짤 코드: 100개 스레드가 카운터를 +1하는 코드. Mutex 없이 거부 → `Arc<Mutex<i64>>`로 통과 → `Rc<Mutex<i64>>`로 *Send 위반* 거부 보기.
- 외부 자료:
  - [Tokio docs — Channels](https://docs.rs/tokio/) — 9주차 복습 + 9장 mpsc

### 2단계 매듭

8주차 끝에서 자네는 *Rust로 도메인을 모델링할 줄 안다*. trait + generics + enum + Result/Option이 손에 묻고, `Send`/`Sync`가 *컴파일러의 거부*라는 사실을 손가락으로 확인했다. 1장에서 적어둔 운영 사고 노트의 NPE 자리에 *"여기는 `Option<T>`가 잡았겠다"*라는 한 줄을 채울 수 있다면, 2단계는 후한 점수로 통과다.

## D.3 3단계 (9~16주차) — "첫 실무 코드"

### 감정의 풍경

이제 손이 코드를 만지기 시작한다. async와 axum과 sqlx로 *진짜 서비스 한 채*를 짤 수 있게 된다. *"한 번 빌드되면 정말 잘 돌아간다"*는 4년차 한국 개발자의 후기에 처음으로 공감하는 시기다. 그리고 *컴파일 시간이 길다*는 첫 불만도 시작되는 시기 — 13장의 처방을 미리 한 번 펴자.

### 주차별 일정

**9주차 — async와 tokio**
- 본문: 10장
- 짤 코드: tokio로 외부 HTTP 호출 10개를 동시에 보내고 결과를 합산. await 가로지르는 동기 Mutex를 일부러 넣어 clippy 경고 보기.
- 외부 자료:
  - [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
  - [fasterthanlime: Catching up with async Rust](https://fasterthanli.me/articles/catching-up-with-async-rust)
  - [corrode: The State of Async Rust](https://corrode.dev/blog/async/)

**10주차 — async 깊이 + Pin**
- 본문: 10장 후반 (function coloring, async fn in trait)
- 짤 코드: `tokio::select!`로 두 작업 중 먼저 끝나는 것 받기. cancellation 패턴.
- 외부 자료:
  - [Without Boats: Pin](https://without.boats/blog/pin/)
  - [Without Boats: Three problems of pinning](https://without.boats/blog/three-problems-of-pinning/)

**11주차 — axum 첫 핸들러**
- 본문: 11장 전반
- 짤 코드: `GET /users/{id}`, `POST /users` 두 핸들러. `Arc<DashMap<i64, User>>`로 in-memory 저장.
- 외부 자료:
  - [axum docs](https://docs.rs/axum/)
  - [Indo Yoon, "실전 백엔드 러스트 Axum 프로그래밍" — 책 소개](https://devbull.xyz/blog/axum-book) — 한국어 보강

**12주차 — axum + tower 미들웨어**
- 본문: 11장 후반
- 짤 코드: 11주차 서비스에 `X-Request-Id` 헤더 자동 부여 미들웨어. 인증 미들웨어 한 개. 7장의 `AuthError`를 `IntoResponse`로 매핑.
- 외부 자료:
  - [Leapcell: Unpacking the Tower Abstraction Layer](https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic)

**13주차 — sqlx로 옮기기**
- 본문: 12장 전반
- 짤 코드: 11주차의 in-memory CRUD를 PostgreSQL로 옮기기. SQL 한 줄을 일부러 틀리게 적어 빌드가 거부하는 모습 보기.
- 외부 자료:
  - [sqlx repo](https://github.com/launchbadge/sqlx)
  - [Leapcell: Unraveling sqlx Macros](https://leapcell.io/blog/unraveling-sqlx-macros-compile-time-sql-verification-and-database-connectivity-in-rust)

**14주차 — sea-orm + 트랜잭션**
- 본문: 12장 후반
- 짤 코드: 같은 도메인을 sea-orm으로 다시 짜보기. 두 코드의 한 줄 한 줄이 어떻게 다른 trade-off인지 노트.
- 외부 자료:
  - [SeaORM docs](https://www.sea-ql.org/SeaORM/)
  - [sangjinsu, "Rust로 실전 백엔드 개발을 경험하다"](https://velog.io/@sangjinsu/Rust%EB%A1%9C-%EC%8B%A4%EC%A0%84-%EB%B0%B1%EC%97%94%EB%93%9C-%EA%B0%9C%EB%B0%9C%EC%9D%84-%EA%B2%BD%ED%97%98%ED%95%98%EB%8B%A4) — 한국어 후기

**15주차 — workspace + 테스트 + 도구 인프라**
- 본문: 13장 전반 (workspace, doctest, criterion, clippy)
- 짤 코드: 13~14주차 서비스를 도메인/인프라/웹 세 crate로 쪼개기. 도메인 함수 하나에 doctest 붙이기.
- 외부 자료:
  - [The Cargo Book — Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)

**16주차 — 보안 게이트 + 매크로 + CLI**
- 본문: 13장 후반 (cargo audit/deny/vet, 매크로 작성, clap)
- 짤 코드: CI에 `cargo audit` 게이트 끼우기. `assert_close!` 매크로 직접 짜보기. 2주차의 CLI를 clap으로 완성형으로.
- 외부 자료:
  - [cargo-audit](https://github.com/RustSec/rustsec)
  - [The Rust Reference — Macros](https://doc.rust-lang.org/reference/macros.html)

### 3단계 매듭

16주차 끝에서 자네는 *axum + sqlx로 작은 서비스 한 채를 짜고 워크스페이스로 쪼개고 CI 게이트를 박을 줄 안다*. 이 자리가 *Spring 다음의 시스템*에 첫 발이 닿는 자리다. 잠시 멈춰서 자축하자. 4개월 전의 자신이 *"왜 이게 컴파일이 안 되지?"* 했던 자리에서 *지금의 자신*은 *컴파일러가 이걸 잡아주니까 평일 새벽 알람이 줄겠구나*를 생각하고 있다. 그 변화가 가장 큰 보상이다.

## D.4 4단계 (17~24주차) — "Rust로 출시하는 시기"

### 감정의 풍경

이제 *팀과 회사*를 바라보기 시작한다. 자네가 짠 첫 사이드 프로젝트를 *결재 라인에 올리는* 자리, 동료를 *함께 학습하자고 끌어들이는* 자리, 한국 커뮤니티에 *첫 글을 올리는* 자리. 기술의 자리에서 사람의 자리로 무게중심이 한 번 옮겨가는 시기다.

### 주차별 일정

**17주차 — 8MB 컨테이너로 출시**
- 본문: 14장 전반 (musl + distroless)
- 짤 코드: 16주차의 axum + sqlx 서비스를 musl + distroless로 빌드. 이미지 크기를 Spring Boot 이미지와 비교.
- 외부 자료:
  - [muslrust GitHub](https://github.com/clux/muslrust)
  - [Chainguard: Distroless container images](https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/)
  - [Leapcell: Building Minimal and Secure Rust Web Applications with Docker](https://leapcell.io/blog/building-minimal-and-secure-rust-web-applications-with-docker)

**18주차 — 관측(tracing + OpenTelemetry)**
- 본문: 14장 후반
- 짤 코드: 핸들러에 `#[tracing::instrument]` 붙이고 OTLP exporter로 Jaeger에 트레이스 보기. `tokio-console`로 task 들여다보기.
- 외부 자료:
  - [tracing docs](https://docs.rs/tracing)
  - [Datadog: How to monitor your Rust applications with OpenTelemetry](https://www.datadoghq.com/blog/monitor-rust-otel/)

**19주차 — JNI로 첫 다리 놓기**
- 본문: 15장 전반 (JNI, C ABI, `#[repr(C)]`)
- 짤 코드: 도메인 crate에서 순수 함수 하나(SHA-256 해시 + Base64)를 JNI로 노출. Spring Boot에서 호출하기.
- 외부 자료:
  - [jni-rs GitHub](https://github.com/jni-rs/jni-rs)
  - [Tweede golf: Mix in Rust with Java (or Kotlin!)](https://tweedegolf.nl/en/blog/147/mix-in-rust-with-java-or-kotlin)
  - [Comprehensive Rust — Java interop (Google)](https://google.github.io/comprehensive-rust/android/interoperability/java.html)

**20주차 — Project Panama + UB 회피**
- 본문: 15장 후반
- 짤 코드: 19주차의 함수를 Panama 바인딩으로도 노출. 보일러플레이트 양 비교. `std::panic::catch_unwind` 패턴 손에 묻히기.
- 외부 자료:
  - [Frankel: Rust and the JVM](https://blog.frankel.ch/start-rust/7/)
  - [JEP 442 / 454 — Foreign Function & Memory API](https://openjdk.org/jeps/454)

**21주차 — 사이드카 패턴**
- 본문: 15장 + 16장 도입
- 짤 코드: 17주차의 8MB 컨테이너를 *Spring 시스템 옆에 사이드카로* 배치. gRPC 또는 HTTP로 통신.
- 외부 자료:
  - [I Replaced My Spring Boot Microservice with Rust and Go](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494) — 사례 회독
  - [Cloudflare: How we built Pingora](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/)

**22주차 — 첫 RFC + 동료 끌어들이기**
- 본문: 16장 (조직 도입의 정치 5가지 권고)
- 짤 코드: 자기 회사 시스템의 *모듈 지도*를 한 장 그리기. *비즈니스 로직 / hot path 후보 / 통신 경계*를 색깔로 구분.
- 외부 자료:
  - [I Rewrote A Java Microservice In Rust And Lost My Job](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca) — *반면교사*로 회독
  - [Dropbox: Inside the Magic Pocket](https://dropbox.tech/infrastructure/inside-the-magic-pocket)
- 추가 활동: 한 페이지짜리 RFC 초안을 동료 한 명과 함께 검토.

**23주차 — 한국 커뮤니티에 첫 발 들이기**
- 본문: 16장 한국 커뮤니티 절
- 활동:
  - [rust-kr.org](https://rust-kr.org/) 가입
  - [한국 러스트 디스코드](https://rust-kr.org/) 또는 OKKY Rust 태그 둘러보기
  - 자기 8MB 사이드카 PoC를 짧은 글로 정리해 velog 또는 회사 블로그에 올리기
- 외부 자료:
  - [김대현, "Rust를 업무용 언어로 쓰다"](https://medium.com/happyprogrammer-in-jeju/rust%EB%A5%BC-%EC%97%85%EB%AC%B4%EC%9A%A9-%EC%96%B8%EC%96%B4%EB%A1%9C-%EC%93%B0%EB%8B%A4-7723cd2c0a59)
  - [Option::None, "4년간의 Rust 사용 후기"](https://blog.cro.sh/posts/four-years-of-rust/)

**24주차 — 매듭과 그 다음의 한 걸음**
- 본문: 16장 매듭
- 활동:
  - 1장에서 적어둔 운영 사고 노트의 *마지막 답*을 채우기
  - 자기 캘린더에 *다음 4주의 첫 한 줄*을 적기 (24주차로 끝나지 않는다 — 그저 *공식 일정의 끝*이다)
  - 동료 한 명에게 *다음 분기 함께할 PoC*를 청하기
- 외부 자료: 부록 A·B·C를 책상 옆에 펴두자. *이 자리부터는 책 밖이다*.

### 4단계 매듭

24주차 끝에서 자네는 *Spring 시스템 옆에 Rust 사이드카 한 채를 띄울 줄 안다*. 첫 PoC가 결재 라인에 올라가 있을 수도 있고, 한국 Rust 커뮤니티에 자네 글이 한 편 올라가 있을 수도 있다. 그게 아니라도 좋다 — *4~6개월 전의 자신*이 *지금의 자신*을 보면 어떤 표정을 지을까. 그 표정이 이 동선 전체의 보상이다.

## D.5 6개월 이후 — 책 밖의 시간

이 가이드는 24주차에서 끝나지만 *학습은 끝나지 않는다*. 사실 이 자리부터가 *진짜 시작*이다. 6개월 이후의 자네에게 권하고 싶은 세 가지를 적어두고 부록을 닫자.

**첫째, 자기 회사 시스템에 *두 번째 PoC*를 시작하자.** 첫 PoC가 사이드카였다면, 두 번째는 *in-process FFI*나 *완전한 마이크로서비스*가 될 수 있다. 한 번 한 바퀴 돈 동선이 두 번째에 *체감으로 빨라진다*. 그게 4년차 한국 개발자의 후기에 적힌 *"한 번 작동하면 정말 잘 작동한다"*가 의미하는 한 줄이다.

**둘째, 한국 Rust 커뮤니티에서 *기여자*가 되어보자.** rust-kr.org의 글에 댓글을 다는 것부터 시작해도 좋다. 자기 회사의 PoC 사례를 *한 페이지 글*로 정리해 한국 커뮤니티에 공유하면, *우리가 1장에서 함께 기다린* 그 글 — *한국 대형 IT 기업의 공식 Rust 프로덕션 사용기* — 의 한 자리를 자네가 채우게 된다. 그 글이 다음 입문자에게 닻이 된다.

**셋째, 인접 영역으로 한 발 더 나가보자.** Rust를 손에 쥔 백엔드 시니어 앞에는 새 자리들이 열려 있다. 시스템·인프라(데이터베이스 엔진, proxy, sidecar), AI 인프라(tokenizer, inference proxy, vector DB), 임베디드, blockchain. *JVM 백엔드의 다음 챕터*로서의 Rust가 본격적으로 펼쳐지는 자리다.

마지막 한 줄. *4~6개월의 학습 곡선은 길다*. 그러나 그 곡선의 끝에서 자네가 손에 쥔 것은 *언어 한 개*가 아니라 *사고 모델 한 가지*다. 그 사고 모델은 *어디로도 가지 않는다*. 그게 이 동선이 약속한 한 가지다. 함께 가자.
