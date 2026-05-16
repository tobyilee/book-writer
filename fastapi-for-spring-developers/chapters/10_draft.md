# 10장. 테스트 — MockMvc에서 TestClient + pytest로

Spring 진영에서 우리는 테스트에 *큰 자산*을 쌓아왔다. JUnit 5의 `@BeforeEach`, MockMvc의 `mockMvc.perform(get("/users/1"))`, `@MockBean`으로 빈 갈아끼우기, `@Transactional` 테스트의 자동 롤백, Testcontainers로 진짜 PostgreSQL 띄우기. 손에 익은 패턴이 한 트럭이다.

이걸 다 버리고 Python에서 처음부터 시작해야 하는가? 다행히 아니다. *대부분 그대로 옮겨진다.* JUnit 5의 자리에는 pytest가 들어오고, MockMvc 자리에는 TestClient가 들어오고, `@MockBean` 자리에는 4장에서 익힌 `app.dependency_overrides`가 들어온다. Testcontainers는 — 이름조차 같다. *Testcontainers Python*이 그대로 있다.

다만 *결정적으로 다른 자리*가 하나 있다. **`@Transactional` 테스트의 자동 롤백이 없다.** Spring에서 우리가 흔히 쓰던 패턴 — 메서드 위에 `@Transactional`을 붙이면 *테스트가 끝날 때 자동으로 롤백*되어 DB 상태가 깨끗하게 유지되던 — 그 마법이 없다. 6장에서 *트랜잭션 자동화의 빈자리*를 만졌듯이, 10장에서도 같은 *명시성*의 호흡을 한 번 더 만난다.

이 장에서 우리가 손에 익혀야 할 건 셋이다. *pytest로 테스트 짜는 손버릇*, *비동기 라우트를 테스트하는 패턴*, 그리고 *트랜잭션 롤백이 없는 세상에서 테스트 격리를 짜는 손길*이다. 차근차근 만져보자.

## pytest 기초 — JUnit 5와의 평행 비교

먼저 pytest 자체부터 손에 익히자. JUnit 5에 익숙하다면 — *놀랍도록 친숙*하다.

```java
// 자바 - JUnit 5
public class UserServiceTest {

    private UserService service;

    @BeforeEach
    void setUp() {
        service = new UserService(new InMemoryUserRepository());
    }

    @Test
    void shouldFindUser() {
        User user = service.find(42L);
        assertThat(user.getName()).isEqualTo("Alice");
    }

    @ParameterizedTest
    @ValueSource(strings = {"alice", "bob", "charlie"})
    void shouldAcceptValidUsernames(String name) {
        assertThat(service.isValidUsername(name)).isTrue();
    }
}
```

```python
# 파이썬 - pytest
import pytest

class TestUserService:
    @pytest.fixture
    def service(self):
        return UserService(InMemoryUserRepository())

    def test_find_user(self, service):
        user = service.find(42)
        assert user.name == "Alice"

    @pytest.mark.parametrize("name", ["alice", "bob", "charlie"])
    def test_accepts_valid_usernames(self, service, name):
        assert service.is_valid_username(name) is True
```

거의 1:1이다. 한 줄 한 줄 매핑해보자.

| Spring/JUnit 5 | pytest |
|---|---|
| `@Test` | `def test_*` 함수 이름 prefix |
| `@BeforeEach` | `@pytest.fixture` |
| `@AfterEach` | fixture 안의 `yield` 뒤 코드 |
| `@ParameterizedTest` + `@ValueSource` | `@pytest.mark.parametrize` |
| `assertThat(x).isEqualTo(y)` | `assert x == y` |
| Mockito `mock(Foo.class)` | `unittest.mock.Mock()` 또는 `pytest-mock` |
| `@DisplayName("사람이 읽는 이름")` | `def test_그_이름_그대로(...)`: 함수 이름이 곧 표시 이름 |

여기서 한 가지 짚고 가자. *fixture가 함수 파라미터다.* 클래스 멤버 변수가 아니다. JUnit 5처럼 `@BeforeEach`가 *암묵적으로* 멤버 변수를 채워주는 게 아니라 — pytest는 *명시적으로* fixture 함수가 *파라미터로 주입*된다. 어디서 본 모양 아닌가? 그렇다, 4장의 `Depends`다. *fixture 이름이 파라미터 이름과 같으면 자동으로 주입된다.* pytest와 FastAPI의 *의존성 주입 철학*이 *같은 줄기*다.

이게 좋은 이유 한 가지. *fixture가 무엇을 의존하는지가 시그니처에 보인다.* JUnit 5에서는 `@BeforeEach` 메서드가 어디서 호출되는지·무엇을 의존하는지 *암묵적*이었다. pytest는 — *코드 위에 평면적으로 펼쳐진다*. 4장의 *그래프가 코드 위에 보인다*는 표현이 — 테스트에서도 그대로 흐른다.

## `TestClient` — MockMvc의 자리

이제 *HTTP 레이어*다. Spring에서 우리는 MockMvc로 *컨트롤러를 띄우지 않고도* 요청을 검증해왔다.

```java
// 자바 - Spring MockMvc
@AutoConfigureMockMvc
@SpringBootTest
class UserControllerTest {

    @Autowired
    MockMvc mockMvc;

    @Test
    void shouldReturnUser() throws Exception {
        mockMvc.perform(get("/api/users/42"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.username").value("alice"));
    }
}
```

```python
# 파이썬 - FastAPI TestClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_returns_user():
    response = client.get("/api/users/42")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
```

`TestClient(app)`는 Starlette 기반이다. 내부적으로 `httpx`를 사용해서 *실제 HTTP를 타지 않고* 앱 객체를 직접 호출한다. MockMvc와 거의 같은 모델 — *서버를 띄우지 않고 ASGI 인터페이스로 직접 요청*.

Spring과 한 가지 다른 점. *컨테이너 재시작이 없다.* `@SpringBootTest`가 컨텍스트를 새로 띄우는 비용이 있던 자리가 — FastAPI에서는 *`TestClient(app)` 한 줄*이다. `app`은 그냥 모듈 레벨 객체다. 시작 비용이 거의 없다.

이게 무엇을 가져오는가? 테스트 실행이 *눈에 띄게 빠르다.* JUnit 5 + Spring Boot 통합 테스트의 *컨테이너 재시작 비용*과 비교하면, pytest + FastAPI는 *시작 비용이 거의 없는 구조*다. 큰 테스트 스위트에서 *분 단위와 초 단위의 차이*가 종종 보인다 — 절댓값은 환경에 따라 다르지만 *시작 비용의 차이*는 본질적이다. *짧은 피드백 루프*가 — 개발 속도에 직결되는 자산이다.

## 의존성 오버라이드 — `@MockBean`의 자리

여기서 4장에서 익힌 `app.dependency_overrides` 패턴이 — 테스트 영역에서 *진짜 가치*를 보인다. Spring 출신이 FastAPI를 보고 *가장 환호하는 자리* 중 하나다.

```java
// 자바 - Spring @MockBean
@SpringBootTest
class UserControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    UserService userService;        // 컨테이너에서 빈을 갈아끼움

    @Test
    void shouldReturnMockedUser() throws Exception {
        when(userService.find(42L)).thenReturn(new User(42L, "alice"));
        mockMvc.perform(get("/api/users/42"))
            .andExpect(jsonPath("$.username").value("alice"));
    }
}
```

```python
# 파이썬 - FastAPI app.dependency_overrides
from app.main import app
from app.users.deps import get_user_service

class FakeUserService:
    async def find(self, user_id: int):
        return UserRead(id=user_id, username="alice", email="alice@example.com")

@pytest.fixture
def client():
    app.dependency_overrides[get_user_service] = lambda: FakeUserService()
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_returns_mocked_user(client):
    response = client.get("/api/users/42")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
```

같은 일을 — *컨테이너 재시작 없이* — 한다. fixture 한 개에 모킹 로직이 담기고, `yield` 위쪽이 셋업, 아래쪽이 정리. 4장과 7장에서 한 번씩 만난 패턴이라 — *이미 손에 익어 있다*.

Spring의 `@MockBean`이 가진 *컨테이너 재구성 비용*이 — FastAPI에서는 *딕셔너리 한 항목 갈아끼우기*다. 그래프가 *함수 시그니처에 있어서* 그렇다. 컨테이너랄 게 없으니, 갈아끼울 컨테이너도 없다.

Mockito의 `when().thenReturn()` 패턴을 그대로 옮기고 싶다면 — `unittest.mock` 또는 `pytest-mock` 라이브러리가 있다. 다만 *Spring 출신의 손에 더 자연스러운* 패턴은 — 위처럼 *FakeXxx 클래스를 작성*하는 것이다. *명시적*이고, *코드 위에 무엇이 일어나는지 보인다*. 6·7장에서 익힌 *명시성 통주저음*과 같은 호흡이다.

## 비동기 테스트 — `pytest-asyncio` + `httpx.AsyncClient`

라우트가 `async def`로 짜여 있다면 — 테스트도 *그 모양*에 맞춰야 한다. `TestClient`는 *동기 클라이언트*다. 내부적으로 ASGI를 동기로 래핑해서 호출한다. 작은 테스트에는 충분하지만 — *진짜 비동기 동작*을 검증하고 싶거나 *동시 요청*을 시뮬레이션하고 싶다면 — `httpx.AsyncClient`가 필요하다.

```python
# 파이썬 - pytest-asyncio + httpx.AsyncClient
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_async_route():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/users/42")
    assert response.status_code == 200
```

```ini
# pyproject.toml (또는 pytest.ini)
[tool.pytest.ini_options]
asyncio_mode = "auto"      # @pytest.mark.asyncio 안 붙여도 자동 인식
```

한 줄 한 줄 짚어보자.

- **`@pytest.mark.asyncio`** — pytest가 *async 함수*를 어떻게 실행할지 알려주는 마커다. `asyncio_mode = "auto"`로 설정하면 모든 `async def test_*` 함수가 자동으로 인식된다.
- **`ASGITransport(app=app)`** — `httpx`에게 *HTTP가 아니라 ASGI 앱*을 직접 호출하라고 알려주는 전송 계층이다. 실제 네트워크가 일어나지 않는다.
- **`async with AsyncClient(...)`** — 클라이언트 자체도 *비동기 컨텍스트 매니저*다.

Spring WebFlux 출신이라면 — `WebTestClient`와 거의 같은 자리다. *비동기 핸들러를 비동기 모드로 호출*. 다른 점은 — Python 진영에서는 *동기 TestClient도 그대로 쓸 수 있다*는 점이다. WebFlux 진영의 *블로킹 호출은 별도 처리*가 필요했던 것과 달리, pytest는 *동기·비동기 테스트가 한 파일에 공존*할 수 있다.

여기서 한 가지 함정. **`AsyncClient`로 테스트할 때 `app.dependency_overrides`도 같은 방식으로 동작한다.** 패턴이 일관된다. 동기든 비동기든 — *의존성 갈아끼우기는 한 줄*이다. 4장에서 깐 패턴이 *어디서나* 같은 모양으로 흐른다.

## Testcontainers — 이름조차 같다

데이터베이스가 끼면 — *진짜 DB를 띄울 것인가, mock으로 갈 것인가*가 결정 갈래다. Spring 진영에서 우리는 *Testcontainers*를 자주 골랐다. *진짜 PostgreSQL을 Docker로 띄워서* 테스트한다. 마이그레이션·SQL 방언·인덱스·트랜잭션 같은 *진짜* 동작을 검증할 수 있다.

좋은 소식이 있다. **Testcontainers Python이 그대로 있다.**

```python
# 파이썬 - testcontainers-python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from app.db.models import Base

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres.get_connection_url()

@pytest.fixture(scope="session")
def engine(postgres_url):
    engine = create_engine(postgres_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
```

이름조차 같다. Spring 진영의 `@Container PostgreSQLContainer` 패턴이 — *fixture 한 개*로 옮겨진 모양이다. 컨테이너의 라이프사이클이 `with` 블록에 묶이고, fixture의 `yield`가 *셋업과 정리*를 같이 표현한다.

`scope="session"`이 — 핵심 한 줄이다. *한 테스트 세션 전체에서 컨테이너를 한 번만 띄운다*는 신호다. 매 테스트마다 컨테이너를 띄우면 — *느리다*. 한 번 띄워두고 — *데이터를 매 테스트마다 격리하는 손길*을 따로 짠다. 그게 다음 절의 주제다.

비동기 SQLAlchemy를 쓴다면 — `asyncpg` URL로 바꾸고 `create_async_engine`을 쓰면 된다. 같은 패턴이다.

```python
# 파이썬 - 비동기 버전
from sqlalchemy.ext.asyncio import create_async_engine

@pytest.fixture(scope="session")
async def async_engine(postgres_url):
    async_url = postgres_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    engine = create_async_engine(async_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
```

여기까지가 *Spring과 같은 자리*다. 이제 *결정적으로 다른 자리*로 넘어가자.

## 트랜잭션 롤백이 없는 세상의 fixture 전략

Spring에서 우리가 *가장 사랑하던 패턴* 중 하나가 — `@Transactional` 테스트의 자동 롤백이었다.

```java
// 자바 - Spring @Transactional 테스트
@SpringBootTest
@Transactional       // 메서드가 끝나면 자동 롤백
class UserRepositoryTest {

    @Autowired
    UserRepository repository;

    @Test
    void shouldSaveUser() {
        User user = new User("alice");
        repository.save(user);
        // 테스트 끝나면 자동 롤백. DB 깨끗.
    }
}
```

*테스트마다 깨끗한 DB*. *공짜로*. 6장에서 `@Transactional`의 자동 롤백을 만졌듯이 — 이 자리에서도 *그 마법이 없다*.

FastAPI/SQLAlchemy에서는 — 어떻게 해야 깨끗한 DB로 매 테스트를 시작할 수 있을까? 세 갈래가 있다. 어느 걸 고를지는 *조직의 사정*에 달려 있다.

### 갈래 1 — SAVEPOINT + 명시적 롤백

가장 *Spring의 자동 롤백에 가까운 모양*이다. 각 테스트를 SAVEPOINT 안에서 실행하고, 끝나면 그 SAVEPOINT까지 롤백한다.

```python
# 파이썬 - SAVEPOINT 기반 격리
@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()      # 외부 트랜잭션 통째로 롤백
    connection.close()
```

좋은 점은 — *진짜 빠르다*. 매 테스트마다 데이터가 *DB에 commit 되지 않고* 메모리에 머문다. 무거운 점은 — *복잡하다*. 트랜잭션 격리, 중첩 SAVEPOINT, async 환경의 미묘한 차이 등 — *손에 익기까지 시간이 든다*. SQLAlchemy 공식 문서에 [이 패턴이 길게 설명돼 있다](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites) — 같은 문서를 한 번 읽어두면 마음이 편하다.

### 갈래 2 — 매 테스트마다 truncate

*가장 단순한 모양*이다. 매 테스트가 끝날 때 — 모든 테이블을 비운다.

```python
# 파이썬 - truncate 기반 격리
@pytest.fixture(autouse=True)
def clean_tables(engine):
    yield
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
```

`autouse=True`가 — *모든 테스트에 자동 적용*된다는 신호다. 좋은 점은 — *이해하기 쉽다*. 무거운 점은 — *느리다*. 매 테스트마다 *진짜 DELETE*가 일어난다. 테이블이 많아지면 — 누적이 작지 않다.

### 갈래 3 — 테스트마다 새 스키마

*가장 격리가 강한 모양*이다. 각 테스트가 *자기 스키마*를 새로 만들고, 끝나면 통째로 drop 한다.

```python
# 파이썬 - schema-per-test
@pytest.fixture
def isolated_db(engine):
    schema = f"test_{uuid4().hex[:8]}"
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA {schema}"))
        conn.commit()
    # 새 스키마를 search_path에 박은 engine을 만들어 yield
    ...
```

좋은 점은 — *완벽한 격리*. 병렬 테스트가 *서로 안 부딪힌다*. 무거운 점은 — *느리고 복잡하다*. 마이그레이션을 매번 실행해야 한다.

### 셋 중 무엇을 고를 것인가

조직의 사정에 따라 다르다. 일반 권고는 — *SAVEPOINT 기반이 기본값, truncate는 시작용, schema-per-test는 병렬화가 필요할 때*다. 우리 책에서는 *SAVEPOINT 기반*을 표준으로 잡는다. 손에 익으면 *Spring의 자동 롤백과 거의 같은 감각*이다.

이 자리에서 한 번 더 짚고 가자. Spring의 자동 롤백은 — *프레임워크가 가려둔 마법*이었다. 우리가 코드를 짤 필요가 없었다. FastAPI/SQLAlchemy에서는 — *그 마법을 우리가 직접 짠다*. 한 번 짜두면 — 평생 쓴다. *자동에서 명시로의 전환*이라는 6·7장의 통주저음이 — 테스트에서도 같은 호흡으로 흐른다.

## 픽스처 스코프 — Spring `@DirtiesContext`의 자리

Spring에서 `@DirtiesContext`는 — *이 테스트가 컨텍스트를 더럽혔으니 다음 테스트 전에 다시 만들어라*는 신호였다. pytest의 fixture 스코프가 — 같은 자리에 들어온다.

```python
# 파이썬 - fixture 스코프
@pytest.fixture(scope="session")    # 한 세션에 한 번
def engine(): ...

@pytest.fixture(scope="module")     # 한 모듈에 한 번
def app_settings(): ...

@pytest.fixture(scope="function")   # 매 테스트마다 (기본값)
def db_session(): ...
```

| Spring | pytest |
|---|---|
| `@DirtiesContext(classMode = AFTER_CLASS)` | `scope="module"` |
| `@DirtiesContext(methodMode = AFTER_METHOD)` | `scope="function"` (기본값) |
| `@DirtiesContext(classMode = BEFORE_EACH_TEST_METHOD)` | `scope="function"` + `autouse=True` |

*무거운 자원은 세션 스코프로, 가벼운 데이터는 함수 스코프로.* 한 줄 원칙이다. PostgreSQL 컨테이너는 — *세션 스코프*. DB 세션·테스트 데이터는 — *함수 스코프*. 명백한 선택이다.

## 계약 테스트 — Spring Cloud Contract 출신을 위해

마지막으로 *계약 테스트*를 한 절 짚고 가자. Spring 진영에서 `Spring Cloud Contract`로 — *프로듀서·컨슈머 간의 API 계약*을 테스트해온 사람이 있을 거다. 그 자산을 FastAPI에서 잃지 않을 수 있는가?

Python 진영의 같은 자리에는 **Pact Python**이 있다. [pact-python](https://github.com/pact-foundation/pact-python) 또는 [pact-python-v3](https://github.com/pact-foundation/pact-python). *Pact 표준*이 Polyglot이라 — Spring Cloud Contract와 *같은 broker*에 contract를 올리고 받을 수 있다. *마이크로서비스 사이의 계약*은 양쪽이 같은 진영을 쓸 필요가 없다.

기본 흐름은 이렇다.

```python
# 파이썬 - pact-python (컨슈머 측 일부)
from pact import Consumer, Provider

pact = Consumer("UserService").has_pact_with(Provider("AuthService"))

(pact
    .given("user alice exists")
    .upon_receiving("a request for alice")
    .with_request("GET", "/users/alice")
    .will_respond_with(200, body={"username": "alice"}))

with pact:
    response = requests.get(f"{pact.uri}/users/alice")
    assert response.json()["username"] == "alice"
```

Spring Cloud Contract의 *Groovy DSL*이 — *Python 메서드 체인*으로 옮겨진 모양이다. 핵심 모델은 같다 — *컨슈머가 기대하는 응답을 contract로 박고, 프로듀서가 그 contract를 검증*. 마이그레이션 비용이 작다.

다만 *모든 사람이 계약 테스트를 짜는 건 아니다*. 모놀리스 안에서 잘 작동하는 시스템이라면 — 굳이 도입할 자리가 아닐 수 있다. *마이크로서비스 + 자율 배포가 굴러가는 조직*에서 진짜 가치가 나오는 패턴이다. 이 책에서는 *Spring Cloud Contract 출신 독자가 이 자리를 잃지 않는다*는 사실만 짚고 넘어가자. 깊이는 *공식 문서와 한 두 권의 패턴 책*에 맡긴다.

## 한 흐름으로 — 1~9장의 API를 한 테스트 스위트로

지금까지 본 도구들을 모아서 — *1~9장에서 짠 작은 API들*을 한 통합 테스트로 묶어보자.

```python
# 파이썬 - tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from app.main import app
from app.db.models import Base
from app.db.session import get_db

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2://", "postgresql+asyncpg://"
        )
        yield url

@pytest.fixture(scope="session")
async def async_engine(postgres_url):
    engine = create_async_engine(postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(async_engine):
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            session_factory = async_sessionmaker(
                bind=connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            )
            async with session_factory() as session:
                yield session
            await transaction.rollback()         # 외부 트랜잭션 통째 롤백

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

```python
# 파이썬 - tests/test_exchange.py (3장 환율 API)
async def test_convert_usd_to_krw(client):
    response = await client.get("/convert?from=USD&to=KRW&amount=100")
    assert response.status_code == 200
    body = response.json()
    assert body["from"] == "USD"
    assert body["to"] == "KRW"
    assert body["amount"] == 100
```

```python
# 파이썬 - tests/test_books.py (5장 도서 CRUD)
@pytest.fixture
async def alice_token(client):
    response = await client.post(
        "/auth/login",
        data={"username": "alice", "password": "secret"},
    )
    return response.json()["access_token"]

async def test_create_and_read_book(client, alice_token):
    headers = {"Authorization": f"Bearer {alice_token}"}
    payload = {"title": "토비의 FastAPI", "author": "이일민"}

    create_response = await client.post("/books", json=payload, headers=headers)
    assert create_response.status_code == 201
    book_id = create_response.json()["id"]

    read_response = await client.get(f"/books/{book_id}", headers=headers)
    assert read_response.status_code == 200
    assert read_response.json()["title"] == payload["title"]
```

```python
# 파이썬 - tests/test_transfer.py (6장 송금)
async def test_transfer_rolls_back_on_insufficient_balance(client, alice_token):
    headers = {"Authorization": f"Bearer {alice_token}"}
    payload = {"from_account": 1, "to_account": 2, "amount": 999_999_999}

    response = await client.post("/transfer", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "잔액이 부족합니다."

    # 두 계좌의 잔액이 변하지 않았는지 검증
    a = (await client.get("/accounts/1", headers=headers)).json()
    b = (await client.get("/accounts/2", headers=headers)).json()
    assert a["balance"] == 1000
    assert b["balance"] == 1000
```

```python
# 파이썬 - tests/test_ml_proxy.py (8장 비동기 ML 프록시)
async def test_ml_proxy_async(client):
    response = await client.post("/predict", json={"input": [1.0, 2.0, 3.0]})
    assert response.status_code == 200
    assert "prediction" in response.json()
```

(`pyproject.toml`에 `asyncio_mode = "auto"`가 설정돼 있으면 `@pytest.mark.asyncio` 데코레이터 없이도 `async def test_*`가 자동 인식된다. 통합 스위트에서는 *모든 테스트를 한 모양*으로 두는 게 호흡상 깔끔하다.)

다섯 개 도메인이 — *같은 fixture 스택* 위에서 일관되게 흐른다. 환율(3장)·인증(7장)·도서(5장)·송금(6장)·비동기 프록시(8장). 모든 테스트가 *진짜 PostgreSQL*에서 굴러간다. 모든 테스트가 *깨끗한 DB로 시작*한다. 모든 테스트가 *컨테이너 재시작 없이 한 번에* 굴러간다.

Spring 진영의 `@SpringBootTest` + `@AutoConfigureMockMvc` + `@MockBean` + `@Transactional` + `@Testcontainers` 조합을 — *한 conftest.py 파일에 평면적으로 펼친 모양*이다. *그래프가 코드 위에 보인다*는 4장의 약속이 — 테스트 영역까지 흐른다.

## 한 호흡으로 정리

지금까지 그린 그림을 머리에 박을 때다. 셋이 남아야 한다.

**첫째, *손에 익힌 Spring 테스트 자산이 대부분 옮겨진다*.** JUnit 5 → pytest, MockMvc → TestClient, `@MockBean` → `app.dependency_overrides`, Testcontainers → Testcontainers Python. 이름조차 같은 자리도 있다. *재학습 비용*이 작다.

**둘째, *비동기 라우트는 `pytest-asyncio` + `httpx.AsyncClient`*다.** 동기 TestClient도 그대로 쓸 수 있지만, *진짜 동시성*을 검증하려면 비동기 클라이언트로 간다. 같은 의존성 오버라이드 패턴이 — *동기·비동기에서 일관되게* 동작한다. 4장에서 깐 패턴이 *어디서나* 같은 모양이다.

**셋째, *트랜잭션 자동 롤백은 없다. 직접 짠다.*** SAVEPOINT 기반 fixture를 한 번 짜두면 — *Spring 자동 롤백과 거의 같은 감각*을 얻는다. 6·7장의 *명시성 통주저음*이 — 테스트에서도 같은 호흡이다. 자동에서 명시로의 전환은 *처음엔 무겁고, 익숙해지면 든든하다*. 1·4·7장에서 봤던 그 감각이 — 한 번 더 흐른다.

그리고 한 가지 더 — *fixture 스코프를 정확히 잡자*. 무거운 자원은 세션 스코프, 가벼운 데이터는 함수 스코프. 컨테이너는 한 번만, DB 세션은 매 테스트마다. 손에 익으면 — *테스트 속도와 격리가 동시에 살아난다*.

다음 11장은 배포·운영이다. 10장까지 우리는 *코드를 잘 짜는 손길*에 집중했다. 11장에서는 *그 코드를 띄우는 손길*을 만진다. Uvicorn 단독 vs Gunicorn + Uvicorn worker, 워커 수 공식, Dockerfile 패턴, 그레이스풀 셧다운, X-Forwarded-* 처리. 그리고 1장에서 예고했던 *180MB → 600MB 메모리 누수 사례*를 본문에서 다시 만난다. JVM의 힙덤프 자리에 — `tracemalloc`·`memray`·`py-spy`를 어떻게 배치하는지 손에 쥐어준다.

준비됐는가? 가자.
