# 14장. 출시 — 8MB 컨테이너와 OpenTelemetry 관측

운영 중인 Spring Boot 서비스의 도커 이미지 한 개가 디스크에서 얼마나 차지하는지 떠올려보자. fat jar에 JDK까지 얹은 표준 Layered JAR 이미지는 보통 *200MB에서 400MB*다. Spring Initializr에서 갓 만든 *Hello World* 한 줄짜리 서비스도 비슷한 무게다. JVM과 base 라이브러리, 그리고 표준 의존성이 차지하는 무게는 코드의 양과 거의 관계가 없다. 13장에서 잘 다듬은 axum + sqlx 워크스페이스를 *진짜로 출시*하면 그 이미지가 몇 MB가 될까? 답을 먼저 적자. **8MB 안팎**이다. Spring Boot 이미지의 *25분의 1에서 50분의 1* 사이다.

이 숫자는 자랑하려고 적는 것이 아니다. 이미지가 작아진다는 것은 *Docker pull 시간이 줄고, 콜드 스타트가 빨라지고, 공격 표면이 좁아지고, 배포 단위 비용이 떨어진다*는 의미다. 그리고 이 숫자가 *한 번의 빌드 설정*만으로 손에 쥐어진다면, 그 변화는 운영 팀의 한 분기를 가볍게 만든다. 14장은 그 빌드 설정을 손에 묻혀주려 한다. 그다음에는 *그 안에서 무슨 일이 벌어지는지를 어떻게 들여다보는가* — 관측·프로파일링·컴플라이언스를 한 절씩 풀어보자. JVM 운영 노하우의 90%는 그대로 통한다. 안심하고 따라오자.

## 8MB 컨테이너 — musl과 distroless의 두 줄

먼저 이미지 크기 표를 한 줄 적어두자. 같은 의미의 *작은 HTTP 서비스* 한 개를 다섯 가지 방식으로 빌드한 결과다.

| 빌드 방식 | 이미지 크기(대략) | 한 줄 메모 |
|---|---|---|
| Spring Boot 3 + `eclipse-temurin:21-jre` | 280~360 MB | 가장 흔한 모양 |
| Spring Boot 3 Layered JAR + alpine-jre | 180~220 MB | 최적화 끝판이지만 여전히 무겁다 |
| GraalVM native-image + alpine | 80~120 MB | 빌드 시간이 5~15배 늘고 reflection 함정 |
| Rust + glibc + `debian:slim` | 30~50 MB | 첫 시도가 보통 이 정도 |
| **Rust + musl + `gcr.io/distroless/static`** | **6~10 MB** | 이번 절의 목표 |

마지막 줄이 우리가 만들 모양이다. 두 가지 결정으로 끝난다. *musl libc로 정적 링크*된 바이너리, 그리고 *런타임 OS는 distroless static* 또는 `scratch`. 한 줄씩 보자.

### musl 정적 바이너리

리눅스의 표준 C 라이브러리는 glibc다. 동적 링크가 기본이라 바이너리 옆에 `libc.so.6`이 따라 붙어야 한다. distroless 이미지에 `glibc` 변종을 골라 쓰면 동작은 한다. 그런데 *완전 정적 링크*까지 가려면 musl libc를 쓰는 편이 솔직하다. Rust는 `x86_64-unknown-linux-musl` 타겟을 표준으로 지원한다.

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

빌드 결과는 `target/x86_64-unknown-linux-musl/release/`에 떨어지고, *어떤 라이브러리에도 동적 링크되지 않은* 바이너리가 한 개 생긴다. `ldd`로 확인해보면 *not a dynamic executable*이라는 한 줄이 나온다. 이 바이너리를 `scratch`에 넣어도 *그냥 돈다*. JVM 출신에게는 이 한 줄이 묘하게 신기하다. *런타임 의존성이 없는 실행 파일*이라는 개념을, JVM에서는 GraalVM native-image에 가서야 만났기 때문이다. Rust는 처음부터 그 모양이 자연스럽다.

OpenSSL 같은 C 라이브러리에 동적 링크된 crate를 쓴다면 musl 빌드가 한 번에 안 된다. 그럴 때는 `rustls`(순수 Rust TLS) 같은 *pure Rust 대체재*를 고르거나, `clux/muslrust` 같은 빌드용 도커 이미지를 쓰면 된다. 처방은 정해져 있다. 처음 musl 빌드가 안 돌면 *어떤 의존성이 C에 묶여 있는지*를 먼저 보자. 90%는 TLS·압축·암호화 라이브러리다.

### multi-stage Dockerfile

이제 표준 패턴을 적자. *빌더 stage*에서 musl 빌드를 돌리고, *런타임 stage*에는 distroless 또는 scratch에 바이너리만 복사한다.

```dockerfile
# syntax=docker/dockerfile:1.7

# 1) builder
FROM rust:1.83-alpine AS builder
RUN apk add --no-cache musl-dev pkgconfig openssl-dev
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

# 2) runtime — 8MB짜리 결과물
FROM gcr.io/distroless/static-debian12
COPY --from=builder \
    /app/target/x86_64-unknown-linux-musl/release/myservice /app/myservice
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/myservice"]
```

13장에서 만들어둔 워크스페이스를 그대로 이 Dockerfile에 태우면 8MB 안팎 이미지가 떨어진다. `docker build` 한 줄로 끝난다. *Spring Boot의 `mvn spring-boot:build-image`*가 했던 일을 한 단계 더 깊은 곳에서 끝낸 셈이다. 안심하고 운영에 올려보자.

distroless static 이미지에는 *셸도, 패키지 매니저도, 심지어 libc도* 없다. *공격 표면이 거의 0에 가깝다*. nonroot로 떨어뜨리는 한 줄까지 박아두면 컨테이너 안에서 권한 상승 사고가 거의 사라진다. 이 영역은 ONCD/NSA의 메모리 안전 권고와 이어진다 — 잠시 뒤 컴플라이언스 절에서 회수하자.

### release 프로파일 튜닝

이미지 크기를 더 줄이고 싶다면, `Cargo.toml`의 `[profile.release]`에 한 단락을 더 박는다.

```toml
[profile.release]
opt-level = 3
lto = "thin"          # link-time optimization
codegen-units = 1     # 최적화 폭 최대 (빌드 시간↑)
strip = true          # 디버그 심볼 제거
panic = "abort"       # panic 시 unwinding 안 함
```

`strip = true`만으로도 보통 30~40% 줄어든다. `lto = "thin"`은 inline 한계를 모듈 경계 너머로 넓혀 *런타임 성능*도 올린다. `panic = "abort"`는 panic이 났을 때 *스택 unwinding 정보*를 빼서 바이너리를 줄인다. 단, FFI 경계에서 panic이 새지 않도록 처리하는 책임이 늘어난다. 15장 FFI에서 다시 짚자.

이 네 줄로 *4~5MB짜리* 바이너리가 떨어지는 일도 흔하다. 다만 *codegen-units = 1*은 빌드 시간을 두 배 가까이 늘린다. 13장의 처방대로 *dev 프로파일*은 그대로 두고 *release 프로파일*에만 적용하는 편이 낫다. 빌드 시간과 바이너리 크기 사이의 trade-off는 자기 팀의 배포 주기에 맞게 골라잡자.

## 관측 표준 스택 — `tracing` + OpenTelemetry

이미지가 작아진 만큼 *그 안에서 무슨 일이 벌어지는지*가 더 중요해진다. JVM 진영에서 우리는 보통 Spring Cloud Sleuth + OpenTelemetry Java agent + Micrometer + Logback의 어딘가에 앉아 있다. *agent 한 줄*로 자동 계측이 들어와서 편하지만, *내부에서 무슨 일이 일어나는지*는 살짝 안갯속이다. Rust는 그 자리를 명시적으로 풀어둔다. `tracing` crate가 출발점이다.

```rust
use tracing::{info, instrument};

#[instrument(skip(pool))]
async fn get_user(pool: &PgPool, id: i64) -> Result<User, AppError> {
    info!(user_id = id, "사용자 조회 시작");
    let user = sqlx::query_as!(User, "SELECT id, name FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await?;
    info!(name = %user.name, "사용자 조회 완료");
    Ok(user)
}
```

`#[instrument]` 한 줄이면 함수 진입과 종료에 *span*이 자동으로 만들어진다. `skip(pool)`로 큰 인자를 로그에서 제외할 수 있다. `info!` 매크로는 *구조화된 필드*를 키-값으로 받는다. `%user.name`은 Display로, `?value`는 Debug로 직렬화된다. JSON 로그·트레이스 모두 같은 한 줄에서 출발한다.

런타임에서 어떤 subscriber로 흘려보낼지는 main에서 한 번만 정한다. *콘솔 JSON 로그*와 *OTLP 트레이스*를 동시에 보내는 모양은 보통 이렇다.

```rust
use opentelemetry_otlp::WithExportConfig;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // 1) OTLP exporter — Jaeger / Tempo / Datadog
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint("http://otel-collector:4317"),
        )
        .install_batch(opentelemetry_sdk::runtime::Tokio)?;

    // 2) tracing → console JSON + OTLP
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .with(tracing_subscriber::fmt::layer().json())
        .with(tracing_opentelemetry::layer().with_tracer(tracer))
        .init();

    // 3) axum 서비스 기동
    // ...
    Ok(())
}
```

여기까지 셋업하고 핸들러에 `#[instrument]`만 붙이면, OpenTelemetry Collector → Jaeger/Tempo/Datadog 어디로 보내든 *span tree가 그대로 보인다*. Spring Cloud Sleuth + OpenTelemetry Java SDK 조합과 *거의 같은 모델*이다. *결정적 차이*는 한 단락이다. JVM agent는 *바이트코드 instrumentation*으로 일을 끝낸다 — 자동이라 편하지만, *내가 무엇을 계측하고 있는지가 살짝 안 보인다*. Rust의 `#[instrument]`는 *코드에 박힌다* — 한 줄을 더 적어야 하지만, *무엇이 어디서 측정되는지가 코드 안에 그대로 보인다*. 어느 쪽이 더 좋은가? 정답은 없다. 다만 SRE 팀의 *디버깅 동선*을 떠올려보자. 코드에서 출발하는 사람에게는 후자가 더 솔직하게 느껴진다.

### 메트릭 — `metrics` crate

span만으로는 부족할 때가 있다. *p99 latency, 처리량, 에러율* 같은 게이지·카운터·히스토그램이다. Java의 Micrometer에 해당하는 자리는 `metrics` crate다.

```rust
use metrics::{counter, histogram};

async fn handler() -> impl IntoResponse {
    let start = std::time::Instant::now();
    counter!("http_requests_total", "route" => "/users").increment(1);

    let result = do_work().await;

    histogram!("http_request_duration_seconds", "route" => "/users")
        .record(start.elapsed().as_secs_f64());
    result
}
```

`metrics-exporter-prometheus`로 Prometheus가 긁어갈 `/metrics` 엔드포인트를 한 줄로 띄운다. Micrometer의 `Counter`/`Timer`/`Gauge`가 *거의 같은 이름*으로 옮겨와 있다. JVM 출신이 가장 평탄하게 건너오는 영역이다.

### panic hook과 Sentry

운영 사고는 보통 *예상하지 못한 panic*에서 시작된다. JVM의 `Thread.UncaughtExceptionHandler`에 해당하는 것이 Rust의 `std::panic::set_hook`이다. Sentry 연동은 `sentry` crate 한 줄이면 끝난다.

```rust
let _guard = sentry::init((
    "https://example@sentry.io/0",
    sentry::ClientOptions {
        release: sentry::release_name!(),
        traces_sample_rate: 0.1,
        ..Default::default()
    },
));
```

`tracing-sentry` layer를 끼우면 `tracing`의 ERROR 레벨 이벤트가 Sentry 이슈로 자동 등록된다. JVM의 Sentry SDK가 했던 일과 *체감으로 동일*하다. 사고 자료를 모으는 운영 동선은 그대로다.

## 프로파일링 — flamegraph·tokio-console·samply

JFR과 Async Profiler에 익숙한 자네에게 Rust 측 프로파일링은 가장 편한 영역이다. 도구 이름만 외우면 손이 즉시 따라붙는다.

`cargo flamegraph`는 perf(Linux) 또는 dtrace(macOS) 위에 *flamegraph SVG*를 그려준다.

```bash
cargo install flamegraph
sudo cargo flamegraph --bin myservice -- --port 8080
```

Async Profiler가 만들어주던 그 *오렌지색 그래프*가 그대로 떨어진다. `inferno`라는 별도 도구로 한 단계 깊게 분석할 수도 있다.

`tokio-console`은 *async task* 차원의 인사이트가 필요할 때 쓴다. *어떤 task가 가장 오래 잠들어 있는가, 어떤 task가 spawn된 뒤 부모가 떠나 고아가 됐는가, 어떤 task가 너무 많이 wake되고 있는가* — JVM의 thread dump가 답해주지 못하는 질문에 답한다. JVM의 Virtual Thread 출신이라면 익숙한 발상이다.

```toml
# Cargo.toml
[dependencies]
console-subscriber = "0.4"
```

```rust
console_subscriber::init();
```

위 두 줄을 추가하고 `tokio-console` 클라이언트로 붙으면 실시간 task 그래프가 보인다. *Spring Reactor의 BlockHound*가 했던 검증보다 한 단계 더 깊다.

`samply`는 sampling profiler다. 빌드한 바이너리에 그대로 붙어 *Firefox Profiler 호환 포맷*으로 결과를 떨어뜨린다. JFR 출신이 가장 빠르게 손에 잡는 도구다.

```bash
cargo install samply
samply record ./target/release/myservice
```

*어떤 도구를 언제 쓰는가*는 한 줄로 정리할 수 있다. *CPU 어디가 뜨거운가*는 flamegraph, *async task가 어떻게 흐르는가*는 tokio-console, *프로덕션 바이너리 그대로 떠보고 싶다*는 samply다. JFR/Async Profiler의 감각이 *세 도구로 분리된* 모양이지만, 각 도구의 깊이는 더 깊다.

### PGO와 LTO — 마지막 한 자리수

마지막 한 자리수의 처리량을 짜내고 싶다면 *PGO(Profile-Guided Optimization)*까지 가자. 운영 환경에서 `cargo pgo`로 *대표 트래픽*을 흘려 프로파일을 모으고, 그 프로파일로 다시 빌드한다. JVM의 *JIT가 자동으로 하는 일*을 *AOT 단계에서 한 번에 하는* 발상이다.

```bash
cargo install cargo-pgo
cargo pgo build
# 대표 트래픽으로 워밍업
cargo pgo run -- --warmup-traffic
cargo pgo optimize build
```

처리량이 5~15% 정도 더 나오는 보고가 흔하다. 첫 출시에서 곧장 손댈 영역은 아니다. *p99 latency가 한 자리수 ms 단위에서 더 줄어야 할 때*에 들이대는 도구다. 이 시점이 오면 *너의 시스템이 이미 충분히 무르익었다*는 신호이기도 하다. 그때 한 번 시도해보자.

## 헬스체크와 graceful shutdown

쿠버네티스 환경에서 가장 흔한 *운영 사고 한 줄*은 *SIGTERM이 와도 in-flight 요청을 마무리하지 않고 죽었다*는 보고다. Spring Boot는 `server.shutdown=graceful`과 `spring.lifecycle.timeout-per-shutdown-phase`로 처리한다. axum + tokio에서는 한 패턴으로 박는다.

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async { signal::ctrl_c().await.expect("ctrl_c handler"); };
    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("SIGTERM handler")
            .recv()
            .await;
    };
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
    tracing::info!("종료 신호 수신, graceful shutdown 진입");
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let app = router();
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;
    Ok(())
}
```

헬스체크는 그냥 라우트 한 줄이다.

```rust
async fn liveness() -> &'static str { "ok" }
async fn readiness(State(pool): State<PgPool>) -> impl IntoResponse {
    if sqlx::query("SELECT 1").fetch_one(&pool).await.is_ok() {
        StatusCode::OK
    } else {
        StatusCode::SERVICE_UNAVAILABLE
    }
}
```

Spring Actuator의 `/actuator/health`/`/actuator/health/liveness`/`/actuator/health/readiness`가 *코드 한 줄*로 풀린다. 마법이 줄어든 만큼 *내 헬스체크가 무엇을 검사하고 있는지*가 명료하게 보인다. 한 번 손에 익으면 안심된다.

## 컴플라이언스 — ONCD·NSA의 회수

1장에서 ONCD(2024-02)와 NSA(2025-06)의 *메모리 안전 언어 권고*를 본 적이 있다. *"C/C++ 취약점의 70%가 메모리 오류"*라는 Microsoft의 한 줄과 함께였다. 14장에서 그 권고를 운영의 자리로 회수하자.

ONCD 보고서는 미국 정부가 *새로 작성하는 시스템*에 메모리 안전 언어를 *쓸 것을 권고*한다는 한 단락이다. NSA는 한 단계 더 강하게 *메모리 안전 언어*의 대표 후보로 Rust·Go·Java·C#·Swift를 명시한다. 정부·금융·국방 도메인은 이미 *왜 안전한 언어를 쓰지 않느냐*를 묻는 단계로 진입했다. 한국 공공 SI 시장에서도 비슷한 신호가 늘고 있다.

여기서 *잘 굴러가던 Spring 시스템을 다 뒤엎어야 하는가*라는 질문은 잘못된 질문이다. *새로 짜는 컴포넌트* — 사이드카, hot path, 데이터 처리 파이프라인, 보안 관련 라이브러리 — 부터 메모리 안전 언어를 고르라는 권고다. JVM은 GC 덕분에 메모리 안전 언어 카테고리에 들어간다. Rust는 *런타임 GC 없이* 같은 자리에 든다. *그래서 두 언어를 함께 가져가는 폴리글랏*이 자연스러운 선택이 된다. 15장의 본 주제가 그 자리다.

distroless 이미지의 *공격 표면이 거의 0*이라는 사실도 같은 결의 이야기다. *셸이 없으면 RCE가 와도 발판이 없다*. 정부·금융 시장의 *컴플라이언스 체크리스트*에서 distroless가 점점 위로 올라오는 이유다. 한 표 더 적어두자.

| 컴플라이언스 항목 | 일반 JVM 운영 | Rust + distroless |
|---|---|---|
| 메모리 안전성 | GC가 보장 | 컴파일 타임 보장 |
| 컨테이너 셸 접근 | bash 있음 | 없음 |
| 의존성 취약점 스캔 | OWASP/Snyk(외부 도구) | `cargo audit`(워크플로 내장) |
| 라이선스 정책 | FOSSA/Snyk OSS | `cargo deny`(워크플로 내장) |
| 공급망 감사 | Sigstore(별도 셋업) | `cargo vet`(파일 한 개) |
| panic·crash 보고 | Sentry SDK | Sentry crate + panic hook |
| 추적·로그 표준 | OTel Java agent | `tracing` + `tracing-opentelemetry` |

JVM 운영 노하우의 *90%는 그대로 통한다*. SRE 팀이 *처음부터 다시 배워야 한다*는 두려움은 거의 근거가 없다. 새로 익혀야 하는 것은 *musl·distroless·tracing crate 셋팅* 정도다. 나머지는 익숙한 도구의 *Rust 친척*을 한 줄씩 끼워 넣는 일이다. 이 사실은 조직에 Rust를 들이는 정치적 비용을 크게 낮춘다. 16장에서 다시 짚겠지만, *운영팀이 동의한다*는 한 줄이 *결재 라인에서 가장 큰 무게*를 가진다.

## 8MB 이미지가 가져오는 부수 효과

마지막으로 한 단락만 보태자. 이미지가 작아진다는 것은 단순히 *디스크 공간 문제*가 아니다.

첫째, *콜드 스타트*가 빨라진다. 쿠버네티스 노드가 새 파드를 띄울 때 가장 느린 단계가 *이미지 pull*이다. 200MB가 8MB로 줄면 그 단계가 *수십 초에서 1~2초*로 줄어든다. AWS Lambda 같은 서버리스 환경에서는 그 차이가 사용자 응답으로 곧장 보인다.

둘째, *메모리 footprint*가 작아진다. JVM 출신이 가장 놀라는 숫자다. axum + tokio 서비스 한 개가 *5~15MB* 메모리에서 굴러간다. 같은 의미의 Spring Boot 서비스가 *250~400MB*를 잡는 것과 비교하면 *20~30배*다. 한 노드에 *수십 배 많은 인스턴스*를 띄울 수 있다는 뜻이다. 클라우드 비용이 그만큼 떨어진다. 15장의 *AWS 비용 81% 절감* 사례가 이 자리에 닿아 있다.

셋째, *정리정돈의 동력*이 생긴다. 이미지가 8MB로 떨어지면 *불필요한 의존성을 안 끌어들이는 습관*이 자연스럽게 자리잡는다. Spring Boot의 *부풀어 오른 의존성*에 익숙해진 손이, *crate 한 개를 추가할 때 한 번 더 생각하는* 손으로 바뀐다. 이 변화는 코드 품질로 천천히 돌아온다.

물론 *모든 것을 Rust로 옮기자*는 이야기가 아니다. 이 책의 한 줄 결론은 *Rust는 JVM의 대체가 아니라 무기 추가다*. 작은 이미지는 그 무기의 *손에 잡히는 형태*일 뿐이다. 그 무기를 어디에 어떻게 끼워 넣을지가 다음 15장의 주제다.

## 마무리 — 함께 해보자

13장의 axum + sqlx 워크스페이스를 musl + distroless로 빌드해 이미지 크기를 측정하자. 한 줄짜리 표를 적어두면 좋다. *Spring Boot 같은 서비스의 `mvn spring-boot:build-image` 결과*와 옆에 나란히 적자. 두 숫자의 비율을 한 번 보면 마음이 한 번 흔들린다. 그다음 핸들러 하나에 `#[tracing::instrument]` 한 줄을 붙이고 `tracing-opentelemetry`로 OTLP exporter를 띄워, *Jaeger 컨테이너에 트레이스가 들어가는 모습*을 직접 보자. *그 트레이스가 코드의 어디에서 시작해 어디에서 끝나는지*를 손가락으로 짚어보자. 마지막으로 SIGTERM을 보내봐서 *graceful shutdown이 in-flight 요청을 끝낸 뒤*에 종료되는지 확인하자. *(이 8MB 이미지는 15장에서 *Spring 시스템 옆 사이드카*로 배치되어 다시 호출된다.)*

다음 15장에서는 그 8MB 컨테이너를 JVM 시스템 *옆에 또는 안에* 들이는 세 가지 길 — 사이드카, hot path 추출, in-process FFI(JNI/Panama) — 를 한 줄씩 풀어보자. *JVM을 떠나지 않고 Rust를 들이는 다리*가 그 자리에 깔린다.

## 참고

- musl 정적 바이너리 + distroless — reference 토픽 11.1, muslrust GitHub
- `tracing` + `tracing-opentelemetry` 표준 스택 — reference 토픽 11.2, Datadog 가이드
- `cargo flamegraph`, `tokio-console`, `samply` — reference 토픽 11.3
- ONCD/NSA 메모리 안전 언어 권고 — reference 토픽 11.4
- 8MB 이미지 사례 — reference 토픽 11.1, OneUptime 가이드
