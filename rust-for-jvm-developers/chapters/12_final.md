# 12장. 데이터베이스 — sqlx로 컴파일 타임 검증된 SQL을, sea-orm으로 친숙한 ORM을

수요일 새벽 두 시. 운영 알림이 울린다. 결제 API의 어떤 SELECT가 *컬럼 이름이 틀렸다*고 토하면서 죽었다. *어제* 누군가 마이그레이션으로 컬럼 이름을 `created_at`에서 `created_time`으로 바꿨고, JPA Native Query에 박혀 있던 SQL이 *그 사실을 모른 채* 배포됐다. 빌드는 통과했다. 단위 테스트도 통과했다. 그런데 *진짜 운영 부하*를 받자마자 드러났다. 이런 사고를 한 번이라도 겪어본 사람이라면 다음 질문이 자연스럽게 떠오른다. *왜 빌드가 이걸 못 잡지? SQL과 스키마가 어긋난 사실을, 컴파일러는 왜 모르지?*

JVM 진영의 답은 늘 비슷했다. JPA를 쓰면 *대부분*의 SQL이 자동 생성되니 *어느 정도는* 안전하다. 그러나 Native Query, MyBatis XML, JdbcTemplate에 박힌 raw SQL은 *컴파일러의 사각지대*다. QueryDSL이 그 자리를 메우려 했지만 *어차피 Java 코드의 검증*일 뿐, *DB 스키마와의 일치*는 검증하지 못한다. 결국 우리는 *마이그레이션 후 통합 테스트*를 빠짐없이 돌리는 *관행*에 의존해왔다.

Rust 진영의 답이 *충격적이다*. **`sqlx::query!` 매크로는 컴파일 타임에 실제 DB에 접속해 SQL을 검증한다.** 컬럼 이름이 틀리면, 타입이 틀리면, 함수 시그니처가 틀리면 — *빌드가 깨진다*. 12장의 핵심 한 줄이 이 문장이다. *JPA에서 런타임에 발견하던 오류를 빌드가 막는다*는 사실의 무게를, 한 챕터 동안 손에 묻혀보자.

물론 sqlx만 답은 아니다. JPA처럼 모델 중심으로 가고 싶은 사람을 위한 sea-orm, 컴파일 타임 type safety를 가장 강하게 가져가는 diesel — 셋이 *경쟁이 아니라 공존*한다. JPA·MyBatis·QueryDSL이 자바에 공존하듯이.

## 셋 중 어디에서 출발할까 — 출신별 추천

본격 코드로 들어가기 전에 한 표를 보자.

| JVM 출신 | Rust에서의 자연스러운 선택 |
|---|---|
| MyBatis 좋아함 / SQL 직접 쓰는 게 편함 | **sqlx** |
| Spring Data JPA / Hibernate 좋아함 | **sea-orm** |
| QueryDSL을 좋아함 / 강한 type-safety가 우선 | **diesel** |
| ORM과 raw SQL을 자유롭게 섞고 싶음 | sea-orm(아래에 sqlx가 노출됨) |

이 책의 본문은 *sqlx 중심*으로 깔고, sea-orm을 한 절로 손에 묻힌 뒤, diesel은 한 단락으로 위치만 짚어두자. 이유 셋. 첫째, sqlx의 *컴파일 타임 SQL 검증*이 Rust 데이터베이스 영역의 *시그니처 자체*다. 둘째, sea-orm은 *내부적으로 sqlx를 쓰므로* sqlx를 먼저 알면 sea-orm 학습이 자연스럽다. 셋째, 11장에서 띄운 axum 서비스를 PostgreSQL로 옮기는 가장 짧은 길이 sqlx다.

## sqlx — raw SQL + 컴파일 타임 검증

sqlx를 의존성에 한 번 적어보자.

```toml
# Cargo.toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros", "migrate", "uuid", "chrono"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

*기능 플래그*가 길다. 한 줄씩 풀자. `runtime-tokio`(tokio 위에서 동작), `postgres`(드라이버), `macros`(`query!`/`query_as!` 매크로), `migrate`(마이그레이션 도구), `uuid`/`chrono`(데이터 타입 매핑). MySQL이라면 `mysql`, SQLite라면 `sqlite`로 바꾼다.

연결 풀을 띄우고 첫 쿼리를 날려보자.

```rust
use sqlx::postgres::PgPoolOptions;

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let pool = PgPoolOptions::new()
        .max_connections(10)
        .connect("postgres://app:secret@localhost/mydb")
        .await?;

    let row = sqlx::query!("SELECT 1 as one")
        .fetch_one(&pool)
        .await?;
    println!("결과: {}", row.one.unwrap());
    Ok(())
}
```

여기서 첫 신기한 일이 일어난다. `cargo build`를 돌리면 *컴파일러가 실제로 PostgreSQL에 접속해서* `SELECT 1 as one` 이 SQL이 유효한지를 검증한다. `DATABASE_URL` 환경 변수로 접속 정보를 넘겨야 한다.

```bash
export DATABASE_URL="postgres://app:secret@localhost/mydb"
cargo build
```

DB가 안 떠 있으면 빌드가 실패한다. DB는 떠 있는데 컬럼 이름이 틀리면 빌드가 실패한다. 타입이 안 맞으면 빌드가 실패한다. *런타임이 아니라 빌드*다. 처음 본 사람은 *이게 정말 동작하나?*가 의심스러울 정도다. 동작한다.

## query! 매크로의 진짜 무게

조금 더 진지한 예제를 보자. 사용자 한 명을 ID로 조회하는 함수다.

```rust
use sqlx::PgPool;

#[derive(Debug)]
struct User {
    id: i64,
    name: String,
    email: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

async fn find_user(pool: &PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    let row = sqlx::query!(
        r#"
        SELECT id, name, email, created_at
        FROM users
        WHERE id = $1
        "#,
        id
    )
    .fetch_optional(pool)
    .await?;

    Ok(row.map(|r| User {
        id: r.id,
        name: r.name,
        email: r.email,
        created_at: r.created_at,
    }))
}
```

이 코드가 컴파일되면서 sqlx가 검증하는 것을 한 줄씩 보자.

1. **SQL 문법** — `SELECT ... FROM ... WHERE ...`가 PostgreSQL이 받아들이는 모양인지.
2. **테이블 존재 여부** — `users` 테이블이 진짜 있는지.
3. **컬럼 존재 여부** — `id`, `name`, `email`, `created_at`이 진짜 있는지.
4. **컬럼 타입** — `id`가 `BIGINT`라서 Rust 측에서 `i64`로 받는 게 맞는지.
5. **placeholder 바인딩** — `$1`에 `i64`를 넘기는 게 맞는지.
6. **결과 row의 nullable 여부** — `name`이 NOT NULL이면 `String`, NULL 가능이면 `Option<String>`.

여섯 가지 *전부* 빌드 단계에서 잡힌다. JPA Native Query에서 *런타임 부하 받기 전까지 모르던* 오류가 *git push 직전*에 잡힌다는 뜻이다.

조금 더 편하게 적으려면 `query_as!`를 쓰는 편이 낫다. 결과를 *바로 struct로 받는* 매크로다.

```rust
async fn find_user(pool: &PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    sqlx::query_as!(
        User,
        r#"
        SELECT id, name, email, created_at as "created_at!"
        FROM users
        WHERE id = $1
        "#,
        id
    )
    .fetch_optional(pool)
    .await
}
```

`User` struct의 필드와 SELECT 컬럼이 *이름과 타입 모두* 맞아야 한다. 어느 한쪽이 틀리면 *빌드*가 거부한다. `as "created_at!"`의 느낌표는 *이 컬럼은 NOT NULL이라고 확신한다*는 sqlx 문법이다(view나 outer join 결과를 다룰 때 유용).

여기서 한 단락 정직하게 적자. **이 마법이 공짜는 아니다.** 첫째, *빌드 시간이 길어진다* — 매 빌드에서 SQL 검증을 위해 DB에 쿼리를 보내야 하기 때문이다. 큰 프로젝트에서는 체감된다. 둘째, *CI에서 DB가 필요하다* — 빌드 자체가 DB 연결을 요구하므로. 이 두 부담을 풀어주는 도구가 다음 절의 *offline 모드*다.

## offline 모드 — CI에서 DB 없이 빌드하기

sqlx가 처음부터 갖춘 도구다. `cargo sqlx prepare` 명령으로 *모든 매크로를 미리 컴파일해 메타데이터를 디스크에 저장*하고, 그것을 git에 커밋하면 *CI는 메타데이터만 읽어 검증*한다.

```bash
# 로컬에서 한 번:
cargo install sqlx-cli --no-default-features --features postgres
export DATABASE_URL="postgres://app:secret@localhost/mydb"
cargo sqlx prepare

# 그러면 .sqlx/ 디렉터리에 query-*.json 파일들이 생성됨.
git add .sqlx
git commit -m "sqlx prepare: schema sync"
```

CI 환경 변수로 `SQLX_OFFLINE=true`를 두면 빌드가 *디스크의 메타데이터만 읽어* 검증한다. DB는 필요 없다.

이 두 단계 워크플로가 처음에는 *번거롭게* 느껴진다. *왜 매번 prepare를 해야 하나?* 답은 *명시적인 게 안전하다*는 Rust 철학에 있다. SQL이 바뀌면 prepare 메타데이터도 바뀌어야 한다. *그 변경이 git diff에 보인다는 사실 자체*가 코드 리뷰의 도구가 된다 — *"이 PR이 어떤 쿼리를 어떻게 바꿨나"*가 한 자리에서 보인다.

팀에 sqlx를 도입할 때 가장 자주 묻는 부분이 이 offline 모드다. CI 파이프라인 한 줄에 `cargo sqlx prepare --check`를 끼워 *prepare 메타데이터가 최신인지를 검증*하는 것이 표준 패턴이다. 그러면 *누가 SQL을 바꾸고 prepare를 빠뜨리면* 빌드가 거부한다.

## 마이그레이션 — sqlx-cli로 Flyway의 자리를

JPA를 쓰면서 Flyway나 Liquibase로 스키마 마이그레이션을 관리하던 경험이 있을 것이다. sqlx도 같은 자리의 도구를 준다.

```bash
sqlx migrate add create_users_table

# migrations/20260503_create_users_table.sql 파일이 생성됨. 그 안에:
# CREATE TABLE users (
#     id BIGSERIAL PRIMARY KEY,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL UNIQUE,
#     created_at TIMESTAMPTZ NOT NULL DEFAULT now()
# );

sqlx migrate run    # 적용.
sqlx migrate revert # 롤백(reversible로 만들어 놨다면).
```

또는 *애플리케이션 시작 시 자동으로 적용*하는 패턴도 있다.

```rust
sqlx::migrate!("./migrations").run(&pool).await?;
```

위 한 줄이 *모든 미적용 마이그레이션을 순서대로 실행*한다. Spring Boot의 `spring.flyway.enabled=true` 자리다. 처음에는 편하지만, 운영에서는 *마이그레이션과 배포를 분리*하는 편이 낫다 — *한 마이그레이션이 큰 락을 잡으면 새 인스턴스가 안 뜬다*. 이 트레이드오프는 Spring Boot도 똑같다.

## 트랜잭션 — `pool.begin()`과 `tx.commit()`

JPA의 `@Transactional`은 *AOP proxy*로 메서드 경계를 가로채 트랜잭션을 관리한다. 너무 자연스러워서 *트랜잭션이 어디서 시작하고 어디서 끝나는지*를 코드에서 보기 어렵다 — 그래서 인터뷰 단골 질문이 됐다(*self-invocation 안 됨*, *체크 예외 vs unchecked 차이*, *propagation 옵션*…). sqlx는 이 자리를 *명시적인 함수 호출*로 두었다.

```rust
async fn transfer(
    pool: &PgPool,
    from_id: i64,
    to_id: i64,
    amount: i64,
) -> Result<(), sqlx::Error> {
    let mut tx = pool.begin().await?;

    sqlx::query!(
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        amount, from_id
    )
    .execute(&mut *tx)
    .await?;

    sqlx::query!(
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        amount, to_id
    )
    .execute(&mut *tx)
    .await?;

    tx.commit().await?;
    Ok(())
}
```

`pool.begin()`이 트랜잭션을 연다. `tx.commit()`이 닫는다. 만약 두 UPDATE 사이에서 `?`로 early return이 일어나면? `tx`가 *drop되면서 자동 rollback*된다. 4장에서 본 `Drop` 트레잇의 RAII가 *트랜잭션*에까지 자라난 모양이다. *try-finally*로 commit/rollback을 챙기던 일이 *타입 시스템의 결과로* 따라온다.

`@Transactional(propagation = REQUIRES_NEW)` 같은 의미는 *함수에 `pool: &PgPool`을 넘기느냐 `tx: &mut Transaction<'_, Postgres>`를 넘기느냐*로 명시적으로 표현된다. 함수 시그니처를 보면 *트랜잭션 안에서 도는지 밖인지*가 한눈에 보인다. 이 *명시성*이 처음에는 번거롭지만, 결제·정산 같은 도메인에서는 *코드만 봐도 의도가 잡힌다*는 안도감을 준다.

JPA의 *함정*들 — 같은 클래스 안 self-invocation에서 `@Transactional`이 안 먹히는 일, lazy loading이 트랜잭션 밖에서 터지는 일, propagation 옵션을 잘못 골라 *상상 못 한 트랜잭션 경계*가 만들어지는 일 — 이 *모양으로 보인다*. 함정이 줄어든다.

## axum 통합 — 11장 in-memory를 PostgreSQL로

이제 11장에서 띄운 axum 서비스의 in-memory `DashMap`을 PostgreSQL로 옮겨보자. 변경 지점이 의외로 적다.

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use thiserror::Error;

#[derive(Clone, Serialize, sqlx::FromRow)]
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
    db: PgPool,
}

#[derive(Error, Debug)]
enum AppError {
    #[error("user not found: {0}")]
    NotFound(i64),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::NotFound(_) => (StatusCode::NOT_FOUND, "not_found"),
            AppError::Database(e) => {
                tracing::error!(error = ?e, "db error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal")
            }
        };
        (status, Json(serde_json::json!({"code": code, "message": self.to_string()})))
            .into_response()
    }
}

async fn list_users(State(s): State<AppState>) -> Result<Json<Vec<User>>, AppError> {
    let users = sqlx::query_as!(
        User,
        "SELECT id, name, email FROM users ORDER BY id LIMIT 100"
    )
    .fetch_all(&s.db)
    .await?;
    Ok(Json(users))
}

async fn get_user(
    State(s): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(
        User,
        "SELECT id, name, email FROM users WHERE id = $1",
        id
    )
    .fetch_optional(&s.db)
    .await?
    .ok_or(AppError::NotFound(id))?;
    Ok(Json(user))
}

async fn create_user(
    State(s): State<AppState>,
    Json(body): Json<CreateUser>,
) -> Result<(StatusCode, Json<User>), AppError> {
    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email",
        body.name, body.email
    )
    .fetch_one(&s.db)
    .await?;
    Ok((StatusCode::CREATED, Json(user)))
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let db = sqlx::postgres::PgPoolOptions::new()
        .max_connections(10)
        .connect(&std::env::var("DATABASE_URL")?)
        .await?;

    sqlx::migrate!("./migrations").run(&db).await?;

    let state = AppState { db };

    let app = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;
    Ok(())
}
```

11장과 *거의 같은 모양*이다. 달라진 건 다섯 줄.

1. `AppState`의 `users: Arc<DashMap<...>>`이 `db: PgPool`로 바뀌었다.
2. 핸들러가 `DashMap` API 대신 `sqlx::query_as!` 매크로를 쓴다.
3. `AppError::Database(#[from] sqlx::Error)`가 추가됐다 — `?` 연산자가 자동 변환을 처리하므로 핸들러 코드는 깨끗하다.
4. `main`에서 `PgPool`을 만들고 `migrate!`로 마이그레이션을 적용한다.
5. `User` struct에 `sqlx::FromRow`를 derive해 컬럼-필드 매핑을 명시한다(엄밀히는 `query_as!`만 쓰면 derive가 필수는 아니지만, 다른 쿼리 형태와 함께 쓸 때 유용하다).

11장의 in-memory 핸들러와 12장의 PostgreSQL 핸들러를 *나란히 놓고 한 줄씩 비교*해보자. *데이터 소스만 바뀌었는데 비즈니스 코드는 거의 그대로다*. 이게 *State 기반 설계*의 진짜 보상이다.

이 코드가 빌드되려면 PostgreSQL이 띄워져 있고 `users` 테이블이 만들어져 있어야 한다. 그렇지 않으면 `query_as!` 매크로가 컴파일 단계에서 거부한다 — *컬럼이 없다, 타입이 안 맞는다, 테이블이 없다*. 이 사실의 무게를 한 번만 더 적자. **JPA에서는 운영 부하를 받고서야 발견하던 사고가, 빌드 단계에서 잡힌다.**

## sea-orm — Spring Data JPA가 그리워질 때

sqlx의 *raw SQL + 컴파일 타임 검증*이 멋지긴 한데, *모델 중심으로 가고 싶다*는 사람도 있다. 엔티티 클래스 하나 만들어 두면 `find_by_id`/`save`/`delete`가 알아서 굴러가는, JPA의 그 감각. 그 자리에 sea-orm이 있다.

sea-orm은 *async-first*이고 *내부적으로 sqlx 위에 구축*되어 있다. Active Record 패턴을 따른다.

```toml
# Cargo.toml
[dependencies]
sea-orm = { version = "0.12", features = ["sqlx-postgres", "runtime-tokio-rustls", "macros"] }
```

엔티티 정의는 이렇다(보통 `sea-orm-cli generate entity`로 자동 생성).

```rust
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub name: String,
    pub email: String,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

사용은 JPA와 모양이 비슷하다.

```rust
use sea_orm::*;

async fn find_user(db: &DatabaseConnection, id: i64) -> Result<Option<Model>, DbErr> {
    User::find_by_id(id).one(db).await
}

async fn create_user(db: &DatabaseConnection, name: String, email: String) -> Result<Model, DbErr> {
    let user = ActiveModel {
        name: Set(name),
        email: Set(email),
        ..Default::default()
    };
    user.insert(db).await
}

async fn list_users(db: &DatabaseConnection) -> Result<Vec<Model>, DbErr> {
    User::find().limit(100).all(db).await
}
```

JPA Repository를 써본 사람에게는 *놀랍도록 익숙한 모양*이다. `find_by_id`, `find()`, `insert()`, `update()`, `delete()` — 모두 자리에 있다. 마이그레이션은 `sea-orm-cli`가 관리한다.

sqlx와 sea-orm 중 무엇을 고를지는 *우리 팀의 SQL 친밀도*에 달렸다. SQL을 손으로 적는 게 편하면 sqlx, 모델 중심이 편하면 sea-orm. *둘을 한 프로젝트에 섞어 쓸 수도 있다* — sea-orm의 `query.into_raw_sql()`로 빠지거나, sea-orm 위에서 sqlx의 raw query를 직접 부를 수 있다. 11장에서 살짝 언급했던 *loco-rs*는 sea-orm을 기본 채택한 starter라, *Rails 생산성*을 빠르게 잡고 싶으면 그쪽이 좋은 출발점이다.

## diesel — 한 단락

diesel은 *가장 오래되고 가장 type-safe한* 선택이다. 기본은 sync(`diesel_async`로 async 가능). 스키마 자체를 Rust 타입으로 표현해서, `users::table.filter(users::name.eq("toby"))` 같은 query가 *컴파일러에 의해 검증*된다. QueryDSL을 좋아하던 사람에게 가장 자연스럽다.

단점은 *async가 디폴트가 아니라는 점*과 *학습 곡선이 가장 가파르다*는 것. 새 프로젝트라면 sqlx나 sea-orm으로 출발하는 편이 낫고, *최강의 type safety가 우선순위*인 도메인에서만 diesel을 들이는 편이 낫다고 한 줄 적어두자.

## 트랜잭션 한 컷 더 — sea-orm

sqlx의 트랜잭션을 위에서 봤다. sea-orm도 같은 의도를 *비슷한 모양*으로 표현한다.

```rust
use sea_orm::TransactionTrait;

async fn transfer(
    db: &DatabaseConnection,
    from_id: i64,
    to_id: i64,
    amount: i64,
) -> Result<(), DbErr> {
    db.transaction::<_, (), DbErr>(|txn| Box::pin(async move {
        let from = Account::find_by_id(from_id).one(txn).await?
            .ok_or(DbErr::Custom("from not found".into()))?;
        let to = Account::find_by_id(to_id).one(txn).await?
            .ok_or(DbErr::Custom("to not found".into()))?;

        let mut from: ActiveModel = from.into();
        from.balance = Set(from.balance.unwrap() - amount);
        from.update(txn).await?;

        let mut to: ActiveModel = to.into();
        to.balance = Set(to.balance.unwrap() + amount);
        to.update(txn).await?;

        Ok(())
    })).await
}
```

`db.transaction(|txn| ...)`이 클로저 안에서 트랜잭션을 굴리고, *클로저가 Err를 반환하거나 panic이 나면 자동 rollback*한다. JPA `@Transactional` 어노테이션을 함수에 붙이던 일과 의도는 같은데, *경계가 코드에 박혀 있다*. *함수 시그니처에 `txn: &DatabaseTransaction`이 등장하면 그 함수는 트랜잭션 안에서만 도는 함수*다 — 의도가 모양으로 보인다.

## 함정 한 컷 — connection pool과 async, 그리고 long-running query

마지막으로 *실무에서 자주 만나는 함정* 하나만 짚자. sqlx도 sea-orm도 *async pool*이다. `pool.acquire()`로 connection을 빌리는데, 이걸 *오래 들고 있으면* 다른 task가 기다린다. JPA에서 *connection을 한 트랜잭션 동안 점유*하던 패턴을 그대로 옮기면, async 환경에서는 *전체 처리량을 갉아먹는다*.

처방은 두 가지다. 첫째, **트랜잭션을 짧게**. 가능하면 한 트랜잭션이 외부 API 호출을 가로지르지 않게. 둘째, **pool 크기를 신중하게**. PostgreSQL의 max_connections와 잘 맞춰야 한다 — 100개 connection을 띄우려는 앱이 50개로 제한된 DB를 만나면 *connection 고갈로 응답이 멈춘다*. 일반 가이드는 *(코어 수 × 2 + 디스크 수)* 언저리. 의외로 *작은 풀이 더 빠르다*.

세 번째 함정 — *long-running query가 connection을 오래 점유*해서 풀이 굳는 일. PostgreSQL이라면 `statement_timeout`을 connection 옵션으로 박아두는 편이 낫다. 또는 sqlx의 `acquire_timeout`/`idle_timeout` 옵션으로 풀의 health를 챙긴다. 이 함정은 16장 운영 사고 회고에서 한 번 더 만난다.

## 함께 해보자

11장에서 띄운 작은 in-memory CRUD를 PostgreSQL 위로 옮겨보자. 첫 시도는 sqlx로. PostgreSQL을 docker로 한 줄 띄우고(`docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:16`), `sqlx migrate add create_users_table`로 첫 마이그레이션을 만들고, `sqlx migrate run`으로 적용하자. 그다음 위의 통합 예제를 그대로 짜서 띄우고, 11장의 in-memory 버전과 *외부 동작이 똑같다*는 사실을 한 번 손에 묻혀보자.

다음 단계로, 다음 두 가지를 시도해보자.

1. **SQL 한 줄을 일부러 틀리게 적자.** `SELECT id, nme, email`처럼 컬럼 이름을 오타 내고 `cargo build`가 어떤 메시지로 거부하는지 그대로 읽어보자. JPA Native Query였다면 *언제* 발견했을지 한 줄로 적어보자.
2. **같은 도메인을 sea-orm으로 다시 짜자.** `sea-orm-cli generate entity`로 엔티티를 만들고, `Entity::find_by_id`/`Entity::find`/`ActiveModel::insert`로 핸들러를 다시 짠다. sqlx 코드와 sea-orm 코드를 한 줄씩 비교해 *어디가 더 명시적이고 어디가 더 함축적인지* 한 단락으로 정리하자.

그리고 작은 트랜잭션을 한 번 짜보자. `transfer(from, to, amount)` 같은 의도로, 두 UPDATE를 하나의 트랜잭션에 묶고 *중간에 의도적으로 panic을 발생*시켜 *rollback이 동작하는지* 손으로 확인하자. JPA `@Transactional`의 자동 rollback과 *모양이 어떻게 다른지* 한 단락으로 적어두자. *(이 sqlx 기반 CRUD 서비스는 13장에서 도메인/인프라/웹 세 crate로 쪼개져 workspace로 묶이고, 14장에서 musl + distroless 8MB 컨테이너로 빌드되어 다시 호출된다. 그리고 트랜잭션의 `Drop` 자동 rollback 패턴은 16장 운영 사고 회고의 *예외 처리* 영역에서 한 번 더 만난다.)*

## 마무리

12장의 한 줄을 다시 적어두자. **`sqlx::query!` 매크로는 컴파일 타임에 실제 DB에 접속해 SQL을 검증한다.** 컬럼 이름, 타입, nullable 여부, placeholder 바인딩 — 모두 *빌드 단계에서* 잡는다. JPA Native Query에서 *런타임 부하 받고서야 발견*하던 그 사고가, *git push 직전*에 컴파일러의 거부로 멈춘다. 이 사실 하나만으로도 sqlx를 한 번 써볼 가치가 있다.

그리고 *마법은 공짜가 아니다*는 사실도 함께 적어두자. 빌드 시간이 길어진다, CI에 DB(또는 prepare 메타데이터)가 필요하다, prepare 단계가 워크플로에 끼어든다. 이 부담을 *명시적으로 받아들일 때* sqlx의 보상이 따라온다. *명시적인 게 안전하다*는 Rust 철학이 *데이터베이스 영역에까지* 자라난 모양이다.

JPA의 모델 중심이 그리우면 sea-orm이 그 자리에 있다. QueryDSL의 강한 type-safety가 우선이면 diesel이 답이다. 셋이 *경쟁이 아니라 공존*한다는 사실 — JPA·MyBatis·QueryDSL이 자바에 공존하듯이 — 이 Rust 데이터베이스 생태계의 균형 잡힌 그림이다.

11장의 핸들러가 *State 기반 의존성 주입*으로 *컴파일 타임에 잡혔다*. 12장의 핸들러가 *컴파일 타임에 검증된 SQL*로 *데이터 영역까지 잡힌다*. 이 두 안전망이 합쳐지면, *애플리케이션이 뜨는 순간이 아니라 빌드가 도는 순간 잘못된 코드를 거부한다*는 한 문장이 *서비스 한 채*에 *통째로 적용*된다. **이제 Spring으로 짜던 그 서비스가 Rust로 보인다.** Part 3의 마지막 한 줄이 이 자리에서 닫힌다.

다음 13장은 *cargo가 JUnit/JMH/Sonar/picocli/OWASP를 모두 안고 있다*는 사실을 한 챕터로 정리한다. workspace로 도메인을 쪼개고, doctest로 문서를 살아있는 예제로 만들고, criterion으로 처리량을 재고, cargo audit/deny/vet로 의존성을 게이트로 걸고, 첫 매크로를 직접 짜보자. 13장이 닫히면 *이제 실무 시스템 한 채를 Rust로 짤 수 있다*는 자신감이 손에 묻는다. Part 4(출시·폴리글랏·사람)가 그 자신감 위에 얹힌다.

## 참고

- *sqlx repo*. https://github.com/launchbadge/sqlx
- *sqlx::query 매크로*. https://docs.rs/sqlx/latest/sqlx/macro.query.html
- *SQLx Compile Time Verification — DeepWiki*. https://deepwiki.com/launchbadge/sqlx/8.3-offline-mode-(prepare-command)
- *Diesel — diesel.rs*. https://diesel.rs/
- *Compare with Diesel — SeaORM*. https://www.sea-ql.org/SeaORM/docs/internal-design/diesel/
- *SeaORM vs SQLx — Medium*. https://techpreneurr.medium.com/seaorm-vs-sqlx-the-rust-orm-war-ends-with-seaorm-1-0-2026-production-ready-87e219ae6fab
- *Rust ORMs in 2026 — Medium*. https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3
- *A Guide to Rust ORMs in 2025 — Shuttle*. https://www.shuttle.dev/blog/2024/01/16/best-orm-rust
- 토픽 9(reference.md §213–243): sqlx, diesel, sea-orm, 마이그레이션.
- 논쟁점 3.3(reference.md §321–327): sqlx vs diesel vs sea-orm 선택 기준.
