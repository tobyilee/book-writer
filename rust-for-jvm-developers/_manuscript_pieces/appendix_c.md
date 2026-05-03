# 부록 C. 추천 crate 카탈로그

JVM 출신의 *Maven Central 즐겨찾기*에 해당하는 한 페이지다. *"이 일을 하려면 어떤 crate?"*에 대한 표준 답안. 카테고리별로 *권장 crate / 대안 / 용도 / JVM 카운터파트*를 묶어 정리했다. 모든 crate에 한 줄짜리 *언제 쓰고 언제 안 쓰는가*를 함께 박아두었다 — 무작정 표준이라고 받아들이기보다 *자기 자리의 trade-off*에 맞춰 고르자.

## C.1 웹 프레임워크

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **axum** ★ | tokio 위 HTTP 서버. 가장 활발한 생태계 | Spring MVC | 2024년 이후의 *사실상 표준*. tower 기반. extractor 패턴이 깔끔. |
| **actix-web** | actor 기반. 가장 오래된 production-ready | (직접 대응 없음) | 단일 머신 *처음부터 끝까지 최고 성능*이 필요하면. 학습 곡선 약간 가파름. |
| **poem** | tower 기반, OpenAPI 자동 생성 강점 | Spring + springdoc-openapi | OpenAPI 스펙이 *제품 요구*면 후보. |
| **rocket** | declarative routing (예전엔 nightly 필수였음) | Spring MVC | 2024년 기준 stable. *Spring과 가장 닮은 모양*이지만 axum보다 생태계 작음. |
| **loco-rs** | "Rust on Rails". batteries-included | Spring Boot starter | 빠르게 prototyping하고 싶으면. axum + sea-orm을 한 묶음으로. |
| **tower** | `Service<Request>` 트레잇 + 미들웨어 합성 | Spring `Filter` + AOP | 거의 모든 위 프레임워크가 *그 위에 있다*. 미들웨어 작성 시 이걸 배우자. |
| **hyper** | low-level HTTP/1.1·2·3 | Netty | axum/reqwest의 기반. *직접 만질 일은 드물다*. |
| **tonic** | gRPC 서버·클라이언트 | grpc-java | tower 기반이라 axum 미들웨어를 그대로 쓸 수 있음. |

**언제 axum을 안 쓰는가:** 단일 머신 극한 처리량(actix가 약간 빠름) / OpenAPI 자동 생성이 *제품 요구*(poem) / Rails 스타일 scaffolding 우선(loco-rs).

## C.2 비동기 런타임

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **tokio** ★ | work-stealing 멀티스레드 executor + I/O + sync primitives | (단일 표준 없음 — Spring + Reactor + ExecutorService를 묶은 자리) | 20,768개 crate가 의존하는 *사실상 유일한 선택*. 백엔드면 그냥 tokio. |
| **smol** | 작고 모듈러한 빌딩 블록 | (없음) | 라이브러리·임베디드·*최소 의존*이 필요하면. |
| **async-std** | 표준 라이브러리와 같은 API의 async 버전 | (없음) | 2025년 sunset 발표. 신규 프로젝트에는 권장 안 함. |
| **futures** | `Future` 트레잇 확장(`Stream`, `Sink`, `join_all` 등) | Reactor `Flux`의 한 결 | tokio와 함께 거의 항상 쓰임. |

**언제 tokio가 아닌 것을 고르는가:** *임베디드 / WebAssembly / 최소 바이너리* — smol 또는 `embassy`. 그 외 백엔드는 tokio가 정답.

## C.3 데이터베이스

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **sqlx** ★ | raw SQL + 컴파일 타임 검증 | MyBatis + JDBC | SQL을 직접 짜는 출신(MyBatis/JdbcTemplate)에게 가장 자연스러움. `query!` 매크로가 *빌드 시점에 DB 접속*해 검증. |
| **sea-orm** | Active Record, async-first | Spring Data JPA / Hibernate | JPA 출신이 가장 친숙. loco-rs 기본. |
| **diesel** | 타입 기반 query DSL, 가장 type-safe | QueryDSL / jOOQ | 컴파일 타임 SQL 생성. `r2d2` 기반(전통적으로 sync, 최근 async 지원 추가). |
| **sqlx-cli** | sqlx 마이그레이션 도구 | Flyway | `sqlx migrate add ...` / `sqlx migrate run`. |
| **sea-orm-cli** | sea-orm 마이그레이션 + entity 생성 | Hibernate Tools | `sea-orm-cli generate entity`로 스키마에서 entity 자동 생성. |
| **deadpool** / **bb8** | 커넥션 풀 (sqlx 외 라이브러리용) | HikariCP | sqlx는 자체 풀 내장이라 별도 필요 X. |

**선택 기준 한 줄:** *raw SQL이 좋다 → sqlx*. *ORM의 친숙함이 좋다 → sea-orm*. *컴파일 타임 query DSL의 안전성이 최우선 → diesel*.

## C.4 직렬화

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **serde** ★ | 직렬화 *프레임워크*. derive로 자동 구현 | Jackson `@JsonProperty` 어노테이션 | `#[derive(Serialize, Deserialize)]` 한 줄로 끝. *모든* 직렬화의 기반. |
| **serde_json** | JSON 포맷 백엔드 | Jackson `ObjectMapper` | `serde_json::to_string(&value)?` / `serde_json::from_str::<T>(s)?`. |
| **toml** | TOML 백엔드 | (없음 — config 라이브러리에 묻혀 있음) | Cargo.toml 자체가 TOML. |
| **serde_yaml** | YAML 백엔드 | SnakeYAML | 비활성 유지보수 → `serde_yaml_ng` 또는 `serde_yml` 후보. |
| **bincode** | 컴팩트한 바이너리 포맷 | Java Serializable | RPC 페이로드, 캐시 직렬화. |
| **prost** / **tonic** | Protocol Buffers + gRPC | grpc-java + protoc-jar | gRPC 메시지. |
| **rmp-serde** | MessagePack | msgpack-jvm | 작고 빠른 바이너리. |
| **ciborium** | CBOR | (드묾) | IoT/표준 사양에서 가끔. |

**언제 serde가 아닌가:** 사실상 *모두 serde 위에서 동작*한다. derive 매크로 컴파일 시간이 부담이면 `miniserde` 같은 경량 대안.

## C.5 CLI

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **clap** ★ | argparse 결정판. derive 매크로 | picocli | `#[derive(Parser)]` 한 줄로 subcommand·flag·env·default·completion까지. |
| **structopt** | (deprecated, clap에 흡수됨) | — | clap 4 derive로 대체됨. |
| **dialoguer** | 대화형 CLI(prompt, confirm, select) | jline | Wizard 스타일 CLI에. |
| **indicatif** | 진행률 표시(progress bar, spinner) | (jansi 정도) | 긴 작업의 사용자 피드백. |
| **console** | 색상·터미널 제어 | jansi | indicatif와 한 묶음. |
| **owo-colors** | 컬러 출력 (가벼운 대안) | — | `"hello".green()` 한 줄. |
| **anstyle** | clap 4의 색상 출력 표준 | — | clap을 쓰면 자동으로 따라옴. |

**clap 미니 예제:**

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp", version, about)]
struct Cli {
    #[arg(short, long, default_value = "info")]
    log_level: String,
    #[arg(env = "DATABASE_URL")]
    database_url: String,
}
```

## C.6 관측(Observability)

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **tracing** ★ | structured logging + span 기반 추적 | SLF4J + Spring Cloud Sleuth | 백엔드의 *기본 로깅*. `info!()` / `error!()` 매크로. |
| **tracing-subscriber** | tracing 출력 백엔드 | Logback | 포맷·필터·레이어 설정. |
| **tracing-opentelemetry** | OpenTelemetry exporter 어댑터 | OpenTelemetry Java SDK | OTLP로 Jaeger/Tempo/Datadog. |
| **opentelemetry** + **opentelemetry-otlp** | OTel 코어 + OTLP 익스포터 | OTel Java | 보통 위 두 crate와 함께. |
| **metrics** | 백엔드 중립적 메트릭 façade | Micrometer | `counter!()` / `gauge!()` / `histogram!()` 매크로. |
| **metrics-exporter-prometheus** | Prometheus 익스포터 | micrometer-registry-prometheus | `/metrics` 엔드포인트 자동. |
| **prometheus** | 직접 Prometheus 라이브러리 | simpleclient | 더 low-level, 직접 등록. |
| **log** | 단순 logging façade | java.util.logging | tracing 이전 표준. 라이브러리에서 호환을 위해 가끔. |
| **env_logger** | log façade의 간단한 백엔드 | — | 작은 CLI에서 충분. |
| **sentry** | 에러 트래킹 | sentry-java | 프로덕션 알림. |

**권장 한 묶음:** `tracing` + `tracing-subscriber` + `tracing-opentelemetry` + `opentelemetry-otlp` + `metrics` + `metrics-exporter-prometheus`. 14장의 출시 절을 그대로 따르면 된다.

## C.7 테스트

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **tokio-test** | tokio async 테스트 유틸 | — | `#[tokio::test]`만으로 충분한 경우 많음. |
| **mockall** ★ | trait 기반 mocking | Mockito | trait + `#[automock]`으로 mock 자동 생성. |
| **criterion** ★ | 통계적 벤치마크 | JMH | warm-up + outlier + HTML 리포트. |
| **proptest** | property-based testing | jqwik | 입력을 *자동으로 생성*해 가설 검증. |
| **quickcheck** | proptest의 다른 결 | (jqwik) | 더 가벼운 대안. proptest가 우세. |
| **insta** | snapshot testing | — | UI/JSON 스냅샷. `cargo install cargo-insta`로 review CLI. |
| **wiremock** | HTTP mock 서버 | WireMock | 외부 API 통합 테스트. |
| **fake** | 더미 데이터 생성 | java-faker | 사용자명·이메일 등. |
| **rstest** | 파라미터화된 테스트 | JUnit `@ParameterizedTest` | `#[rstest]` + `#[case(...)]`. |
| **pretty_assertions** | diff가 보이는 assert_eq | — | 긴 struct 비교에 필수. |

## C.8 에러 처리

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **thiserror** ★ | 라이브러리용 derive 매크로 | checked exception 계층 | `enum AuthError { ... }` 도메인 에러에. `#[from]`으로 변환 자동. |
| **anyhow** ★ | 애플리케이션용 box 에러 + context | RuntimeException 래핑 | `Result<_, anyhow::Error>` + `.context("...")?`. |
| **snafu** | thiserror의 다른 결, context 강조 | (없음) | 컨텍스트 체이닝이 정교함. |
| **eyre** | anyhow의 fork (color-eyre로 컬러 출력) | — | CLI에서 보기 좋은 에러 출력 원하면. |
| **color-eyre** | eyre + 컬러 백트레이스 | — | 개발 중에 traceback 가독성 큰 폭으로 향상. |

**선택 기준 한 줄:** *내가 라이브러리를 짜고 있다 → thiserror*. *내가 애플리케이션을 짜고 있다 → anyhow*. 둘 다 함께 쓰는 경우가 가장 많다.

## C.9 동시성 자료구조

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **parking_lot** ★ | std `Mutex`/`RwLock`보다 빠른 대체 | (없음 — JDK 표준이 빠른 편) | poisoning 없고 더 작음. 거의 항상 std보다 좋음. |
| **dashmap** ★ | concurrent HashMap | ConcurrentHashMap | shard 기반. multi-thread 카운터·캐시. |
| **crossbeam** | 채널·스레드·atomic 확장 | java.util.concurrent | std mpsc보다 빠른 채널. work-stealing 큐 등. |
| **crossbeam-channel** | crossbeam의 채널만 | — | std mpsc의 *직접 대체*. multi-producer + multi-consumer. |
| **flume** | 또 다른 빠른 채널 | — | crossbeam-channel의 대안. |
| **arc-swap** | atomic Arc 교체 | AtomicReference | 자주 읽고 가끔 교체하는 설정 객체에. |
| **once_cell** | 지연 초기화 | (lazy init 패턴) | `OnceCell::new()`. 1.80부터 std에 통합되어 가는 중. |
| **rayon** | data parallelism | parallel streams | `iter().par_iter()` 한 줄로 병렬화. |

**`parking_lot::Mutex`를 안 쓰는 자리:** poisoning이 *반드시* 필요한 경우(거의 없음).

## C.10 보안 도구 (cargo subcommand)

이건 *crate*라기보다 *cargo plugin*이지만 묶어두자.

| 도구 | 설치 | 의미 | JVM 카운터파트 |
|---|---|---|---|
| **cargo-audit** ★ | `cargo install cargo-audit --locked` | RustSec Advisory DB 조회 | OWASP Dependency Check |
| **cargo-deny** ★ | `cargo install cargo-deny --locked` | license / source / dependency policy | OWASP DC + license check + Snyk |
| **cargo-vet** | `cargo install cargo-vet --locked` | supply chain 감사 (Mozilla 주도) | (직접 대응 없음) |
| **cargo-geiger** | `cargo install cargo-geiger --locked` | unsafe 사용량 측정 | — |
| **cargo-outdated** | `cargo install cargo-outdated --locked` | 오래된 의존성 표시 | versions-maven-plugin |
| **cargo-edit** | (1.62부터 cargo 내장) | `cargo add/rm/upgrade` | — |
| **cargo-machete** | `cargo install cargo-machete --locked` | 사용하지 않는 의존성 검출 | — |

**CI 게이트의 표준:** `cargo audit --deny warnings && cargo deny check`. 13장의 마지막 한 줄.

## C.11 부록의 부록 — 자주 쓰는 *기타* crate

한 카테고리로 묶기 애매하지만 매일 쓰게 될 crate들이다.

| crate | 용도 |
|---|---|
| **chrono** / **time** | 날짜·시간. `time`이 더 새롭고 권장 |
| **uuid** | UUID 생성·파싱 |
| **regex** | 정규식 (PCRE보다 빠른 자체 엔진) |
| **url** | URL 파싱 |
| **bytes** | byte buffer (tokio 의존성으로 자주 묻혀 옴) |
| **hex** | hex 인코딩 |
| **base64** | base64 인코딩 |
| **sha2** / **sha3** / **blake3** | 해시 함수 |
| **ring** / **rustls** | 암호화 / TLS (OpenSSL 회피) |
| **reqwest** | HTTP 클라이언트 (axum + tower 생태계 호환) |
| **clap_complete** | clap 자동 완성 생성 |
| **dotenvy** | `.env` 로드 |
| **config** | 설정 파일 로드 (TOML/YAML/JSON/env) |
| **tempfile** | 임시 파일·디렉터리 |
| **walkdir** | 재귀 디렉터리 순회 |
| **notify** | 파일 시스템 변경 감시 |
| **directories** | OS별 사용자 디렉터리 (Linux/Mac/Windows) |
| **tower-http** | axum용 HTTP 미들웨어 (CORS, trace, compression) |
| **axum-extra** | axum 추가 extractor (cookie, typed-header) |
| **tower_governor** | rate limit 미들웨어 |
| **jsonwebtoken** | JWT |
| **argon2** / **bcrypt** | 패스워드 해시 |

---

*"이 crate를 쓰면 됩니다"*는 누구나 한 줄로 적을 수 있다. *"이 crate를 안 쓰면 무엇이 어려운가"*까지 함께 적어야 표가 살아난다. 위 표의 *한 줄* 열을 그 자리로 두려고 했다. 카탈로그 한 페이지를 책상 옆에 펴 두자. 새 작업 앞에서 *"어떤 crate?"* 질문이 떠오를 때 가장 먼저 펴는 자리가 되기를.

마지막 권고 한 줄. 새 crate를 추가할 때마다 *`cargo audit`을 한 번 더 돌리자*. 의존성 트리는 시간이 갈수록 무거워지고, 그 무게는 *6개월 뒤*에 청구서로 돌아온다. 그때 손에 잡히는 도구가 있다는 것 — 그게 cargo 생태계가 JVM 출신에게 가장 친절한 자리다.
