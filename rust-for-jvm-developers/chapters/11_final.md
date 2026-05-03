# 11장. axum으로 첫 HTTP 서비스 — Spring Controller가 Rust로 보이는 순간

10년쯤 Spring으로 컨트롤러를 짜왔다고 해보자. `@RestController`를 클래스에 붙이고, `@GetMapping("/users/{id}")`로 엔드포인트를 매핑하고, `@PathVariable Long id`로 URL 변수를 받고, `@Autowired UserService`로 서비스를 주입받고, 응답으로 `ResponseEntity<User>`나 그저 `User` 한 객체를 던져주면 끝이다. 너무 익숙해서 손이 먼저 움직인다. 그런데 이 전부가 *어떻게* 동작하는지를 솔직하게 적자면 — *Spring이 런타임에 reflection으로 클래스를 스캔하고, 어노테이션을 읽고, proxy를 만들고, DI 컨테이너에서 의존성을 찾아 주입하고, request mapping 트리를 빌드해 라우팅하는* 일련의 일이 *애플리케이션이 뜨는 그 한순간*에 일어난다. 잘못된 시그니처를 적어도 *컴파일은 통과하고*, *애플리케이션이 뜨는 순간까지* 모른다.

axum이 다른 길을 간다. 이번 챕터의 핵심 한 줄은 이렇다. **axum의 핸들러는 그냥 async 함수이고, DI는 *컴파일러가 타입으로 검증한다*.** 그래서 *애플리케이션이 뜨는 순간*이 아니라 *빌드가 도는 순간* 잘못된 핸들러를 잡는다. Spring을 손에 깊게 익힌 사람이 처음 axum을 보면 *너무 단순해서 의심스럽다*. 그 의심을 한 챕터에 걸쳐 풀어보자.

먼저 솔직히 짚을 부분 하나. **axum이 Spring Boot처럼 안 느껴질 수 있다.** DI 컨테이너가 없고, AppState를 직접 들고 다닌다. `@Service` 자동 등록도 없고, `@Transactional` AOP도 없다. *덜 매직이고 더 명시적이다*. 처음에는 *이 정도까지 손으로 적어야 하나*가 답답하지만, 6개월쯤 지나면 *어디서 무엇이 동작하는지가 코드에 다 보인다*는 안도감이 그 자리를 차지한다.

## 프레임워크 지형 — 셋 중 어디에서 출발할까

본격적으로 들어가기 전에 지형 한 장을 보자. Rust 백엔드 프레임워크는 사실상 셋이다.

- **axum** — tokio 팀의 작품. tower 기반. extractor 패턴이 매력적이고 미들웨어가 곧 `Service` trait이라 *cross-framework로 재사용*된다. 가장 활발한 선택지.
- **actix-web** — actor 모델. 가장 오래되고 가장 빠르다(벤치 기준 axum보다 처리량 10~15% 우위). 코드 모양이 *조금 더 무겁다*는 평.
- **loco-rs** — 사실상 *Rust on Rails*다. CLI 스캐폴드, ORM(sea-orm), 백그라운드 잡, 스토리지가 통합. 내부적으로는 axum + sea-orm + sidekiq-rs를 합쳐 놓은 것이다. Spring Boot의 *batteries included* 감각을 가장 가깝게 재현한다.

이 셋 중 무엇부터 손에 잡으면 좋을까? 답은 *axum*이다. 이유 두 가지. 첫째, 생태계가 가장 활발해서 검색이 잘 된다. 둘째, *조립형이라 어디서 무엇이 동작하는지가 가장 잘 보인다* — 입문자가 *모델을 잡기에는* 이게 가장 좋다. loco-rs는 *axum을 손에 익힌 다음* "Spring Boot 같은 생산성이 그리워질 때" 한 번 들여다보면 된다.

## 첫 핸들러 — `Hello, JVM`을 띄워보자

cargo로 새 프로젝트를 하나 만들고 시작하자.

```toml
# Cargo.toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

다음은 가장 단순한 axum 서비스다.

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(hello));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn hello() -> &'static str {
    "Hello, JVM"
}
```

Spring Boot를 처음 시작했을 때 본 `Application.java` + `HelloController.java` 두 파일이 *Rust 한 파일*에 들어가 있다. 자세히 보자.

- `#[tokio::main]` — 10장에서 본 그 어노테이션. tokio runtime을 띄운다.
- `Router::new().route("/", get(hello))` — *어떤 URL에서 어떤 메서드일 때 어떤 함수를 호출할지*를 *코드로* 적어둔다. Spring의 `@GetMapping("/")`이 *어노테이션*이라면 axum은 *함수 호출 체인*이다.
- `async fn hello() -> &'static str` — 핸들러는 그저 async 함수다. 어노테이션도 인터페이스도 없다.

`cargo run`으로 띄우고 `curl http://localhost:3000`을 두드리면 `Hello, JVM`이 돌아온다. Spring Boot보다 *훨씬 빠르게 뜬다* — 100ms 언저리. JVM warmup이 없다. 그리고 이 서비스의 *바이너리 크기*가 release 빌드에서 5MB 안팎이라는 사실은 14장에서 다시 확인하게 된다.

## Extractor 패턴 — `@PathVariable`/`@RequestBody`/`@RequestParam`이 한 모양으로

Spring의 컨트롤러를 짜다 보면 어노테이션이 정말 많다. `@PathVariable`, `@RequestParam`, `@RequestBody`, `@RequestHeader`, `@CookieValue`, `@SessionAttribute`. 어노테이션마다 *어디서* 데이터를 꺼낼지를 일러준다. axum은 이 모든 것을 *extractor*라는 한 패턴으로 통일한다.

```rust
use axum::{
    extract::{Path, Query, State, Json},
    http::HeaderMap,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct ListParams {
    page: Option<u32>,
    limit: Option<u32>,
}

async fn get_user(Path(id): Path<i64>) -> Json<User> {
    Json(User { id, name: "toby".into(), email: "t@x".into() })
}

async fn list_users(Query(params): Query<ListParams>) -> Json<Vec<User>> {
    let _ = (params.page, params.limit);
    Json(vec![])
}

async fn create_user(
    headers: HeaderMap,
    Json(payload): Json<CreateUser>,
) -> Json<User> {
    let _ = headers.get("authorization");
    Json(User { id: 1, name: payload.name, email: payload.email })
}
```

핸들러 시그니처를 한 줄씩 보자.

- `Path(id): Path<i64>` — URL path의 변수를 꺼낸다. Spring `@PathVariable Long id`.
- `Query(params): Query<ListParams>` — 쿼리스트링을 struct로 deserialize. Spring `@RequestParam`을 한 객체로 묶은 셈. 더 깔끔하다.
- `Json(payload): Json<CreateUser>` — body를 JSON으로 deserialize. Spring `@RequestBody`.
- `HeaderMap` — 모든 HTTP 헤더 접근. Spring `@RequestHeader` 묶음.

처음 보면 이상한 부분이 있다. *함수의 매개변수 위치만 다른데 어떻게 이걸 axum이 다 알아듣지?* 답은 trait이다. axum은 `FromRequestParts`/`FromRequest` trait을 구현한 타입이라면 *어떤 것이든* 핸들러 매개변수에 들어갈 수 있게 해놓았다. 그리고 `Path<T>`, `Query<T>`, `Json<T>`, `HeaderMap` 등이 그 trait을 구현해 놓았다.

이 자리에서 한 가지 안도감을 주는 사실 — **잘못된 시그니처는 컴파일이 거부한다**. 예를 들어 `Path(id): Path<i64>`인데 라우터에서 `/users/:user_id`로 등록했다고 해보자. 빌드 자체는 통과하지만(타입은 맞으니까), 라우터의 path placeholder 이름이 안 맞으면 *컴파일러보다 한 단계 위에서* 잡힌다 — 사실 이 부분은 axum 0.7부터는 매우 엄격해져서, 잘못된 placeholder는 라우터 등록 시점에 panic이 난다. *애플리케이션이 뜨는 순간이 아니라 빌드 직후 첫 실행*에서. Spring 진영 사람이 가장 자주 묻는 *"잘못된 시그니처를 컴파일러가 정말 다 잡나?"*에 답하자면 — *대부분 잡지만, 라우터-핸들러 시그니처 매핑은 한 단계 안전망이 추가로 필요하다*. 그래도 *애플리케이션이 뜨는 순간까지 모르는* Spring보다는 한참 앞이다.

## State — DI 컨테이너 없이 의존성을 끼워 넣는 법

이제 Spring 출신이 가장 자주 묻는 질문이다. *`@Autowired`가 없으면 의존성은 어떻게 주입하나?*

axum의 답은 `State<T>`다. *애플리케이션 전체가 공유하는 상태*를 한 타입으로 묶어, 모든 핸들러가 그것을 extractor로 받는다. 이 상태에 DB 풀, 캐시 클라이언트, 외부 API client, 설정값 등을 다 넣는다.

```rust
use axum::{
    extract::State,
    routing::get,
    Router,
};
use std::sync::Arc;
use dashmap::DashMap;

#[derive(Clone)]
struct AppState {
    users: Arc<DashMap<i64, User>>,
    // 나중에 db_pool: PgPool, http: reqwest::Client, ... 추가.
}

#[derive(Clone, serde::Serialize)]
struct User {
    id: i64,
    name: String,
}

async fn get_user(
    State(state): State<AppState>,
    axum::extract::Path(id): axum::extract::Path<i64>,
) -> Result<axum::Json<User>, axum::http::StatusCode> {
    state.users.get(&id)
        .map(|u| axum::Json(u.clone()))
        .ok_or(axum::http::StatusCode::NOT_FOUND)
}

#[tokio::main]
async fn main() {
    let state = AppState {
        users: Arc::new(DashMap::new()),
    };
    state.users.insert(1, User { id: 1, name: "toby".into() });

    let app = Router::new()
        .route("/users/:id", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

자세히 보자. `AppState`는 *그저 struct*다. `Clone`을 derive해야 한다(axum이 필요할 때 복제하므로). 그 안에 `Arc<DashMap<i64, User>>`가 있다 — 9장에서 본 `Arc`의 그 모양이다. *멀티스레드 공유* 의도가 코드에 박혀 있다. `DashMap`은 동시 접근이 가능한 HashMap이다(ConcurrentHashMap의 Rust 대응). 더 복잡한 상태라면 `Arc<Mutex<HashMap<...>>>`이나 `Arc<RwLock<...>>`을 넣는다.

`with_state(state)`로 라우터에 한 번 등록하면, 모든 핸들러가 `State<AppState>`로 그것을 받을 수 있다. 컴파일러가 *타입으로* 검증한다. 잘못된 타입을 받으려 하면 *빌드가 거부한다*. Spring `@Autowired`가 *애플리케이션이 뜨는 순간 빈을 못 찾으면 NoSuchBeanDefinitionException으로 죽었다*면, axum은 *빌드 단계에서 컴파일 에러로 멈춘다*.

여기서 한 가지 호불호가 갈리는 부분이 있다. **`AppState`를 *직접 들고 다닌다*.** Spring은 *`@Service` 클래스를 자동으로 빈으로 등록*하고, 다른 곳에서 *`@Autowired`로 가져다 쓴다*. axum은 *우리가 손으로 struct에 넣고, 손으로 with_state로 등록한다*. 처음에는 *왜 이걸 매번 적어야 하나*가 답답하다. 적응되면 *어떤 의존성이 있는지가 한 자리에 다 보인다*는 안도감이 그 자리를 차지한다 — *AppState struct만 보면 이 서비스의 외부 의존성이 한 줄로 정리된다*.

회사 코드가 커지면 *AppState를 너무 비대하게 만들지 말자*. trait로 추상화하거나, *기능별 sub-state*로 쪼개는 패턴이 자연스럽다. 그 부분은 13장에서 workspace로 도메인을 나눌 때 다시 호명된다.

## tower와 Layer — Filter/Interceptor/AOP가 한 모델로

axum의 진짜 힘은 *미들웨어*에서 드러난다. tower라는 라이브러리의 `Service<Request>` trait이 *비동기 함수(요청→응답)를 일급 시민*으로 만든다. axum, tonic(gRPC), hyper, reqwest가 *모두* 같은 추상화 위에 있어서 미들웨어가 *cross-framework로 재사용*된다.

JVM에서는 같은 의도를 *세 개의 다른 메커니즘*으로 풀어왔다. **Servlet Filter**가 가장 바깥, **Spring HandlerInterceptor**가 그 안, **`@Aspect` AOP**가 그 안에서 메서드 단위로 동작했다. 셋이 *우선순위와 사용처가 미묘하게 다르고*, 한 회사 코드에서 *세 종류가 다 섞여 있는* 일이 흔했다. tower는 이 셋을 *한 모델*로 통일한다.

가장 자주 쓰는 미들웨어 한 줄씩 살펴보자.

```rust
use axum::{Router, routing::get};
use tower_http::{
    trace::TraceLayer,
    cors::CorsLayer,
    timeout::TimeoutLayer,
};
use std::time::Duration;

let app = Router::new()
    .route("/", get(|| async { "ok" }))
    .layer(TraceLayer::new_for_http())          // 모든 요청 로그.
    .layer(CorsLayer::permissive())              // CORS 헤더 자동.
    .layer(TimeoutLayer::new(Duration::from_secs(5))); // 5초 타임아웃.
```

`tower_http` crate에 표준 미들웨어가 다 들어 있다. `TraceLayer`는 Spring Cloud Sleuth + Logback 자리. `CorsLayer`는 Spring `WebMvcConfigurer.addCorsMappings()` 자리. `TimeoutLayer`는 *Spring에서 직접 짜야 했던* 영역.

직접 미들웨어를 쓰고 싶다면 어떻게 할까? `axum::middleware::from_fn`이 가장 쉬운 다리다.

```rust
use axum::{
    extract::Request,
    http::{header, HeaderValue, StatusCode},
    middleware::Next,
    response::Response,
};
use uuid::Uuid;

async fn add_request_id(mut req: Request, next: Next) -> Response {
    let request_id = Uuid::new_v4().to_string();
    req.headers_mut().insert(
        "x-request-id",
        HeaderValue::from_str(&request_id).unwrap(),
    );
    let mut response = next.run(req).await;
    response.headers_mut().insert(
        "x-request-id",
        HeaderValue::from_str(&request_id).unwrap(),
    );
    response
}

async fn require_auth(
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth = req.headers().get(header::AUTHORIZATION)
        .and_then(|v| v.to_str().ok());
    match auth {
        Some(token) if token.starts_with("Bearer ") => Ok(next.run(req).await),
        _ => Err(StatusCode::UNAUTHORIZED),
    }
}
```

위가 모든 요청에 X-Request-Id 헤더를 부여하는 미들웨어, 아래가 인증 미들웨어다. *Spring `OncePerRequestFilter`/`HandlerInterceptor`로 짜던 일과 모양이 거의 똑같다*. 차이는 한 가지 — *컴파일러가 시그니처를 검증한다*. `req`를 `Request`로 받는지, `next.run(req)`을 호출하는지, 반환 타입이 `Response`인지를 다 컴파일러가 본다.

라우터에 끼우는 모양도 단순하다.

```rust
let public_routes = Router::new()
    .route("/", get(|| async { "public" }));

let private_routes = Router::new()
    .route("/me", get(|| async { "private" }))
    .layer(axum::middleware::from_fn(require_auth));

let app = Router::new()
    .merge(public_routes)
    .merge(private_routes)
    .layer(axum::middleware::from_fn(add_request_id));
```

*어떤 라우터에 어떤 미들웨어를 끼울지*가 코드에 *그래프로* 박혀 있다. Spring `WebSecurityConfigurer`가 *어노테이션과 빈 구성*으로 표현하던 일을, axum은 *함수 호출 체인*으로 표현한다. 그래프가 보인다는 사실 자체가 *디버깅의 비용*을 줄여준다.

## 라우터 합성 — `merge`와 `nest`

서비스가 자라면 라우터를 *모듈별로 쪼갤* 필요가 생긴다. axum은 두 가지 합성 도구를 준다.

```rust
fn user_routes() -> Router<AppState> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/:id", get(get_user))
}

fn order_routes() -> Router<AppState> {
    Router::new()
        .route("/", get(list_orders))
}

let app = Router::new()
    .nest("/api/v1/users", user_routes())
    .nest("/api/v1/orders", order_routes())
    .with_state(state);
```

`nest`는 *prefix를 붙여 라우터를 끼운다*. Spring의 `@RequestMapping("/api/v1/users")`를 컨트롤러 클래스에 붙이는 자리다. `merge`는 *prefix 없이 합치는* 도구. 이 둘이 *복잡한 라우팅 그래프*를 *함수로 합성*한다는 점에서 깔끔하다.

## IntoResponse와 에러 처리 — `Result<T, AppError>`가 HTTP 응답으로

이제 7장에서 만든 `thiserror` 기반 도메인 에러를 *HTTP 응답으로 변환*하는 자리다. 7장의 *함께 해보자*에서 `AuthError` enum을 만들었다. 그것이 *어떻게* HTTP 401/429/500으로 자연스럽게 매핑되는지 손에 묻혀보자.

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde::Serialize;
use std::time::Duration;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("invalid password")]
    InvalidPassword,
    #[error("expired token")]
    ExpiredToken,
    #[error("rate limited (retry after {0:?})")]
    RateLimited(Duration),
    #[error("user not found: {0}")]
    NotFound(i64),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("internal error")]
    Internal(#[from] anyhow::Error),
}

#[derive(Serialize)]
struct ErrorBody {
    code: &'static str,
    message: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::InvalidPassword => (StatusCode::UNAUTHORIZED, "invalid_password"),
            AppError::ExpiredToken => (StatusCode::UNAUTHORIZED, "expired_token"),
            AppError::RateLimited(_) => (StatusCode::TOO_MANY_REQUESTS, "rate_limited"),
            AppError::NotFound(_) => (StatusCode::NOT_FOUND, "not_found"),
            AppError::Database(e) => {
                tracing::error!(error = ?e, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "database_error")
            }
            AppError::Internal(e) => {
                tracing::error!(error = ?e, "internal error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal")
            }
        };
        (status, Json(ErrorBody {
            code,
            message: self.to_string(),
        })).into_response()
    }
}
```

이 코드의 핵심은 한 줄이다. **`AppError`가 `IntoResponse`를 구현하는 순간, 모든 핸들러가 `Result<T, AppError>`를 그저 반환할 수 있다.** 그러면 `?` 연산자로 에러 전파가 자동이 된다.

```rust
async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(
        User,
        "SELECT id, name FROM users WHERE id = $1",
        id
    )
    .fetch_optional(&state.db)
    .await?  // sqlx::Error → AppError::Database 자동 변환.
    .ok_or(AppError::NotFound(id))?;

    Ok(Json(user))
}
```

`?` 연산자가 7장에서 본 `From` trait의 자동 변환을 활용한다. `#[from]` 속성이 `From<sqlx::Error> for AppError`를 자동으로 만들어주기 때문에, `await?` 한 줄이 *실패 시 즉시 early return*하면서 에러 타입 변환까지 처리한다. Spring `@RestControllerAdvice`로 *예외를 한 자리에 모아 처리*하던 패턴이 *타입 시스템 안에 박혀* 있다.

JVM 출신은 이 자리에서 비교 한 단락을 머리에 꼭 새겨두자. **Spring의 `@RestControllerAdvice`/`@ExceptionHandler`는 *런타임 디스패치*다.** AOP proxy가 던져진 예외를 잡아서 매핑한다. 잘못 매핑된 예외는 *런타임에 발견*된다. axum의 `IntoResponse` 패턴은 *컴파일 타임 매핑*이다 — 핸들러의 반환 타입이 `Result<T, AppError>`로 정해지면 *그 타입의 에러만* 반환할 수 있고, 그 타입의 모든 분기가 *컴파일러가 강제하는 exhaustive match*로 처리된다. *exception 누락*이 *컴파일 단계에서* 잡힌다.

## 통합 — 작은 in-memory 서비스 한 채

지금까지 본 모든 조각을 한 화면에 모아보자. *작은 user CRUD를 in-memory로 띄우는* 미니 서비스다.

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    middleware,
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::sync::{atomic::{AtomicI64, Ordering}, Arc};
use thiserror::Error;
use tower_http::trace::TraceLayer;

#[derive(Clone, Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Clone)]
struct AppState {
    users: Arc<DashMap<i64, User>>,
    next_id: Arc<AtomicI64>,
}

#[derive(Error, Debug)]
enum AppError {
    #[error("user not found: {0}")]
    NotFound(i64),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        match self {
            AppError::NotFound(id) => (
                StatusCode::NOT_FOUND,
                Json(serde_json::json!({"code": "not_found", "id": id})),
            ).into_response(),
        }
    }
}

async fn list_users(State(s): State<AppState>) -> Json<Vec<User>> {
    Json(s.users.iter().map(|e| e.value().clone()).collect())
}

async fn get_user(
    State(s): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    s.users.get(&id)
        .map(|u| Json(u.clone()))
        .ok_or(AppError::NotFound(id))
}

async fn create_user(
    State(s): State<AppState>,
    Json(body): Json<CreateUser>,
) -> (StatusCode, Json<User>) {
    let id = s.next_id.fetch_add(1, Ordering::SeqCst);
    let user = User { id, name: body.name, email: body.email };
    s.users.insert(id, user.clone());
    (StatusCode::CREATED, Json(user))
}

async fn add_request_id(
    mut req: axum::extract::Request,
    next: middleware::Next,
) -> Response {
    let id = uuid::Uuid::new_v4().to_string();
    req.headers_mut().insert(
        "x-request-id",
        axum::http::HeaderValue::from_str(&id).unwrap(),
    );
    let mut res = next.run(req).await;
    res.headers_mut().insert(
        "x-request-id",
        axum::http::HeaderValue::from_str(&id).unwrap(),
    );
    res
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let state = AppState {
        users: Arc::new(DashMap::new()),
        next_id: Arc::new(AtomicI64::new(1)),
    };

    let app = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .layer(middleware::from_fn(add_request_id))
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("listening on http://0.0.0.0:3000");
    axum::serve(listener, app).await.unwrap();
}
```

한 화면에 들어가는 분량이다. Spring Boot에서 같은 일을 짜자면 *application.properties + @SpringBootApplication + @RestController + @Service + @Configuration + 빈 등록*이 적어도 5~6 파일. axum은 *한 파일에 한 모듈로 끝난다*. 더 중요한 건 *어디서 무엇이 동작하는지가 한눈에 보인다*는 사실이다. State에 무엇이 들어 있고, 라우터가 어떻게 연결되고, 미들웨어가 어떤 순서로 끼워지는지 — *모두 코드의 한 자리*에서 읽힌다.

`cargo run`으로 띄우고 `curl` 한 줄씩 두드려보자.

```
curl localhost:3000/users
curl -X POST localhost:3000/users -H 'Content-Type: application/json' -d '{"name":"toby","email":"t@x"}'
curl localhost:3000/users/1
```

문제없이 동작한다. 응답에 `x-request-id` 헤더가 자동으로 붙어 있다. 잘못된 ID로 GET하면 404 + JSON body가 돌아온다. *정확히 우리가 적은 대로* 동작한다.

## 성능 한 줄 — 그리고 단서

11장의 마지막에 성능 한 줄을 정직하게 적자. 100 동시 연결 / JSON+PostgreSQL 시나리오에서 Spring Boot(JVM)는 4,200 req/s, P99 45ms, 280MB. axum + tokio는 42,000 req/s, P99 3ms, 12MB. **약 10배 처리량, 1/15 latency, 1/23 메모리**라는 보고가 있다.

이 숫자에 흥분하기 전에 *단서*를 함께 적자. 첫째, *매우 단순한 시나리오*다. 비즈니스 로직이 깊어지면 격차는 줄어든다. 둘째, Spring을 *WebFlux*로 옮기면 JVM 측이 더 따라붙는다. 셋째, 메모리 격차는 *배포 환경에 따라 의미가 다르다* — 컨테이너 cost가 비싼 환경에서는 1/23이 *바로 청구서*에 보이지만, 대형 인스턴스에서는 절대값이 더 중요할 수 있다.

그래도 한 줄은 분명하다. **컨테이너 한 대당 메모리 280MB가 12MB로 줄어든다는 사실**은 마이크로서비스 수가 *수십~수백 개*에 이르는 회사라면 인프라 비용 청구서에서 *체감*된다. 그 보상이 우리 회사에 *얼마나 클지*를 *스스로 계산*해보는 것이 11장의 진짜 숙제다.

## 함께 해보자

Spring으로 짜본 적 있는 작은 REST 엔드포인트 하나(예: `GET /users/:id`, `POST /users`)를 axum으로 옮겨보자. 위 통합 예제를 그대로 베껴 시작해도 좋다. 위에서 본 것처럼 in-memory `DashMap`을 State에 두고 시작하면 된다.

여유가 되면 다음 한 줄씩을 추가해 보자.

1. **인증 미들웨어** — `Authorization: Bearer ...` 헤더가 없으면 401. Spring `@PreAuthorize`/Security Filter 자리.
2. **CORS** — `tower_http::cors::CorsLayer`로 한 줄.
3. **요청 trace** — `tracing-subscriber::fmt::init()` + `TraceLayer`. 요청별 로그가 자동.
4. **에러 응답 통일** — 위에서 본 `AppError`/`IntoResponse` 패턴을 도입하고, 핸들러를 `Result<T, AppError>`로 바꾼다.

마지막으로, 같은 일을 Spring Boot로 짤 때 *몇 개의 파일과 어노테이션*이 필요한지를 한 단락으로 비교해보자. *어느 쪽이 더 짧은가*가 아니라 *어느 쪽이 어디서 무엇이 동작하는지 더 잘 보이는가*를 기록해두자. *(이 in-memory 서비스는 12장에서 sqlx + PostgreSQL로 옮겨가 다시 호출되고, 미들웨어 패턴은 14장 운영의 OpenTelemetry trace에서 한 번 더 만난다. 그리고 `IntoResponse` 패턴은 13장 cargo workspace의 *웹 crate*가 *도메인 crate의 에러*를 어떻게 받아들이는지의 모양으로 다시 등장한다.)*

## 마무리

11장의 한 줄을 다시 박자. **axum의 핸들러는 그저 async 함수이고, DI는 컴파일러가 타입으로 검증한다.** 그래서 *애플리케이션이 뜨는 순간이 아니라 빌드가 도는 순간* 잘못된 핸들러를 잡는다. extractor 패턴이 `@PathVariable`/`@RequestBody`/`@RequestHeader`를 한 모양으로 통일했고, `State<T>`가 `@Autowired`의 자리를 *명시적*으로 차지했다. tower의 `Layer`가 Filter/Interceptor/AOP 셋을 한 모델로 합쳤고, `IntoResponse` trait이 `@RestControllerAdvice`의 일을 *타입 시스템 안*에서 한다.

솔직히 한 번 더 짚자. axum은 *Spring Boot처럼 안 느껴질 수 있다*. DI 컨테이너가 없고, AppState를 직접 들고 다니고, *@Service 자동 등록도 @Transactional AOP도 없다*. 그 *덜 매직*이 처음에는 답답하다. 6개월쯤 지나면 *어디서 무엇이 동작하는지가 다 보인다*는 안도감이 그 자리를 채운다 — 그리고 *애플리케이션이 빨리 뜬다, 메모리가 작다, 빌드가 잘못된 코드를 거부한다*는 보상이 따라온다.

다음 12장에서는 *데이터베이스*다. 위의 in-memory `DashMap`을 *PostgreSQL*로 옮길 때, *sqlx의 `query!` 매크로*가 *컴파일 타임에 SQL을 검증*한다는 사실의 충격을 손에 묻혀보자. JPA에서 *런타임에 발견*하던 오류를 *빌드*가 막는다 — 11장의 *빌드가 잘못된 핸들러를 거부한다*는 한 줄이 *DB 영역까지* 자라난 모양이다.

## 참고

- *Announcing Axum — Tokio Blog*. https://tokio.rs/blog/2021-07-announcing-axum
- *axum docs*. https://docs.rs/axum/latest/axum/
- *Unpacking the Tower Abstraction Layer in Axum and Tonic — Leapcell*. https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic
- *Introduction to the Tower library — Frankel*. https://blog.frankel.ch/introduction-tower/
- *Practical Clean Architecture in Rust — YouTube*. https://www.youtube.com/watch?v=TrNpyFMtnzI
- *Rust, Axum, and Onion Architecture — Medium*. https://medium.com/@jonathan.el.baz/rust-axum-and-onion-architecture-escaping-the-tech-debt-spiral-14df5db946df
- *Spring Boot Webflux vs Rust (Axum) — Medium*. https://medium.com/deno-the-complete-reference/spring-boot-webflux-vs-rust-axum-hello-world-performance-28611da8bfc2
- *Loco.rs*. https://loco.rs/, *What if Rails was Built on Rust?*. https://loco.rs/blog/hello-world/
- *Rust Web Frameworks Compared — DEV.to*. https://dev.to/leapcell/rust-web-frameworks-compared-actix-vs-axum-vs-rocket-4bad
- 토픽 8(reference.md §184–211): axum, actix-web, loco-rs, tower, axum 패턴, 성능 비교.
- 인용(reference.md §444): Spring Boot 4,200 req/s vs Rust+Axum 42,000 req/s.
