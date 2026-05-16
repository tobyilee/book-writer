# 4장. 의존성 주입 — `@Autowired`에서 `Depends()`로

이런 장면을 상상해보자. Spring 프로젝트에서 컨트롤러 한 개를 새로 만든다. 손이 먼저 움직인다.

```java
// 자바 - Spring Boot
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }
    // ...
}
```

머리가 굳이 의식하지 않는다. *생성자에 받아두면 빈 컨테이너가 알아서 채워준다.* `UserService`는 어딘가 `@Service`가 붙은 채로 등록돼 있고, 그게 의존하는 `UserRepository`는 또 어딘가 `@Repository`가 붙어 있다. 우리는 그 그래프를 *그릴 줄도* 알고, 동시에 *그리지 않을 줄도* 안다. 컨테이너에게 맡기면 되니까. 8년 동안 손에 익은 패턴이다.

그러다 FastAPI 튜토리얼을 열면 처음 보는 모양과 마주친다.

```python
# 파이썬 - FastAPI
@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    svc: Annotated[UserService, Depends(get_user_service)],
):
    return svc.find(user_id)
```

`Depends(get_user_service)`. 클래스가 없다. `@Autowired`도 없다. 의존성이 *함수 파라미터 자리*에 들어와 있다. 그리고 그 파라미터의 값은 — 컨테이너가 채워주는 게 아니라 — `get_user_service`라는 *함수가 호출돼서* 만들어진다.

처음 만져보면 좀 낯설다. *컨테이너가 어디 있지? 빈 정의는 어디서 하지? 어디서 그래프를 짜지?* 답은 한 줄로 정리된다. **그래프를 짜는 자리가 없다.** 함수의 시그니처가 그래프 그 자체다. 시작 시점에 한 번에 짜는 것도 아니다. 매 요청마다 다시 풀린다.

이 차이가 코드를 어떻게 바꾸는지, 그 바뀐 형태가 Spring 사고와 어디서 맞물리고 어디서 멀어지는지를 차근차근 만져보자.

## `Depends()`는 함수 파라미터의 마커다

먼저 가장 작은 예제부터 보자.

```python
# 파이썬 - 단일 의존성
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_user_repo() -> UserRepository:
    return UserRepository()

@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    repo: Annotated[UserRepository, Depends(get_user_repo)],
):
    return repo.find(user_id)
```

이 코드의 흐름을 한 번 따라가 보자. `GET /users/42` 요청이 들어온다. FastAPI는 `read_user` 함수의 시그니처를 본다. `user_id: int`는 경로 변수다. `repo: Annotated[UserRepository, Depends(get_user_repo)]`는 — `Depends()` 마커가 붙어 있으니 — *의존성*이다. FastAPI가 `get_user_repo()`를 호출하고, 그 반환값을 `repo` 자리에 넣는다. 그리고 나서야 `read_user`의 본문이 실행된다.

Spring 사고로 옮기면 `get_user_repo`가 곧 `@Bean` 메서드에 가깝다. 빈을 *어떻게 만드는지* 알려주는 팩토리 함수다. 다만 결정적 차이가 두 가지 있다.

**첫째, `Depends()`는 함수 파라미터에 *마커*로 붙는다.** 클래스 멤버 변수에 붙는 `@Autowired`나 생성자의 매개변수가 아니다. *함수마다* 매번 명시한다.

**둘째, FastAPI에는 별도의 빈 컨테이너가 없다.** Spring처럼 `ApplicationContext`가 그래프를 들고 있는 게 아니다. 각 라우트의 시그니처가 *자기 그래프*를 매번 묘사한다. 그래프는 라우트 호출 시점에 한 번 풀리고 사라진다.

이 둘이 무엇을 가져오는가? 좋은 면은 — 그래프가 *언제나 코드 위에 보인다는 것*이다. 마법이 적다. "이 `UserService`는 어디서 와?"라는 질문에 대한 답이 *같은 줄*에 적혀 있다. 무거운 면은 — 같은 의존성을 여러 라우트가 쓸 때 *같은 줄을 반복해서 적어야 한다는 것*이다. 이 반복을 어떻게 줄이는지가 한 절의 무게를 가져간다(*Annotated 타입 별칭* 절에서 다시 만난다).

## 중첩 의존성 — 그래프는 알아서 풀린다

의존성이 하나뿐이면 매력이 약하다. *그래프*가 그려지는 자리에서 진짜 매력이 나온다.

```python
# 파이썬 - 중첩 의존성
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)

@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    svc: Annotated[UserService, Depends(get_user_service)],
):
    return svc.find(user_id)
```

요청이 들어오면 FastAPI는 그래프를 거꾸로 풀어 나간다. `read_user`가 `get_user_service`를 필요로 한다. `get_user_service`는 `get_user_repo`를 필요로 한다. `get_user_repo`는 `get_db`를 필요로 한다. 잎에서 뿌리까지 거슬러 올라가서, 뿌리부터 다시 내려오면서 차례로 만든다.

Spring 사고로 옮기자면 `@Component` 그래프 + 생성자 주입과 거의 1:1이다. 다른 점은 — 그래프 *명세*의 자리다. Spring에서는 `@Component`/`@Service`/`@Repository` 어노테이션이 컨테이너에게 *클래스 단위로* 명세를 준다. 컨테이너가 시작 시점에 그래프를 *조립*한다. FastAPI에서는 각 함수의 *시그니처 자체*가 그래프 명세다. 시작 시점이 따로 없다. 라우트 호출 시점에 그때그때 풀린다.

이게 비효율 아닐까 싶은 의문이 따라온다 — 합리적이다. 답은 두 갈래다. 첫째, 의존성 함수의 호출 자체는 Python에서 그리 비싸지 않다. 그래프가 *깊어도* 함수 몇 개 호출하는 비용이다. 둘째, *비싼* 자원(데이터베이스 엔진, HTTP 클라이언트, ML 모델)은 매 요청마다 만들지 않는다 — `lifespan`이나 모듈 상수에 한 번만 만들어두고, 그걸 *얇은 의존성 함수가 가져다 쓴다*. 이 패턴은 잠시 뒤 *싱글톤이 필요할 때* 절에서 본격적으로 다룬다.

## 기본 스코프는 요청 단위, 한 요청 안에서는 캐시된다

1장에서 한 번 짚었지만 다시 가져오자. **FastAPI 의존성의 기본 스코프는 요청 단위다.** 한 요청이 들어오면 의존성 함수들이 실행되고, 응답이 나가면 모두 정리된다.

그런데 한 요청 안에서 같은 의존성이 *여러 번* 필요한 경우는 어떨까? 위 그래프를 예로 들자. `get_user_service`도 DB가 필요할 수 있다. `get_user_repo`도 DB가 필요하다. 둘 다 `Depends(get_db)`를 명시하면 — *DB 세션이 두 개 만들어지는 걸까?*

답은 아니다. **같은 요청 내에서 같은 의존성은 한 번만 실행되고 결과가 재사용된다.** FastAPI가 요청-스코프 캐시를 가지고 있다.

```python
# 파이썬 - 한 요청 내 캐시
def get_request_id() -> str:
    rid = uuid4().hex
    print(f"새 요청 ID 발급: {rid}")   # 한 요청에 한 번만 출력된다
    return rid

def use_a(rid: Annotated[str, Depends(get_request_id)]):
    return f"A: {rid}"

def use_b(rid: Annotated[str, Depends(get_request_id)]):
    return f"B: {rid}"

@app.get("/check")
def check(
    a: Annotated[str, Depends(use_a)],
    b: Annotated[str, Depends(use_b)],
):
    return {"a": a, "b": b}   # a와 b의 rid가 같다
```

`use_a`와 `use_b`가 각각 `get_request_id`에 의존하지만, 한 요청 안에서 `get_request_id`는 *한 번만* 호출된다. `use_a`가 받은 `rid`와 `use_b`가 받은 `rid`는 같은 문자열이다.

이게 좋은 이유는 명백하다. *한 요청 안에서 일관된 컨텍스트*가 보장된다. 같은 DB 세션, 같은 요청 ID, 같은 현재 사용자. 여러 서비스가 한 요청 안에서 의존성을 공유해도 일관성이 깨지지 않는다.

Spring의 `@RequestScope`와 정확히 같은 모델이라고 생각하면 이해가 쉽다. 다른 점은 — Spring에서 `@RequestScope`는 *명시적 선언*이고, FastAPI에서는 *기본값*이라는 점이다. 그래서 우리가 의식적으로 "이건 매 요청마다 새로 만들어야 해" 같은 결정을 따로 내릴 필요가 없다. 기본이 그렇다.

다만 한 가지 함정을 짚고 가자. **캐시는 "같은 의존성 함수"를 기준으로 한다.** 같은 일을 하는 함수가 *둘*이면 — 캐시되지 않는다. 우연한 함수 두 개로 같은 DB를 두 번 열어버리지 않으려면, *한 도메인은 한 의존성 함수로 모은다*는 손버릇이 안전하다.

## 싱글톤이 필요할 때 — `lifespan`, 모듈 상수, `@lru_cache`

요청-스코프가 기본이라는 말은 — *싱글톤이 필요한 자원은 의식적으로 만들어야 한다*는 뜻이다. Spring처럼 자동으로 싱글톤이 되지 않는다.

세 가지 도구가 있다. 어느 자원을 어디에 둘지, 손에 익혀두면 평생 쓴다.

### `lifespan` — 애플리케이션 수명에 묶인 자원

가장 권장되는 모양이다. FastAPI 인스턴스의 *수명 전체*에 한 번만 만들어지고, 종료 시 정리되는 자원.

```python
# 파이썬 - lifespan으로 싱글톤 자원 관리
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine("postgresql+asyncpg://...")
    app.state.engine = engine
    yield                              # 여기서 앱이 요청을 받는다
    await engine.dispose()             # 종료 시 정리

app = FastAPI(lifespan=lifespan)
```

`yield` 위쪽이 시작 단계, 아래쪽이 종료 단계다. Spring의 `@PostConstruct` + `@PreDestroy`를 한 함수에 합친 모양이다.

엔진을 `app.state`에 두면, 의존성 함수에서 꺼내 쓸 수 있다.

```python
# 파이썬 - lifespan 자원을 의존성에서 꺼내기
from fastapi import Request

async def get_db(request: Request) -> AsyncSession:
    engine = request.app.state.engine          # lifespan에서 만든 싱글톤
    async with AsyncSession(engine) as session:
        yield session
```

엔진은 하나. 세션은 매 요청마다 새로. 자원의 *수명*이 자원의 *스코프*와 어떻게 어긋나는지 보이는가? 이 어긋남을 `lifespan` + `Depends`의 조합으로 깔끔하게 표현한다.

### 모듈 레벨 변수 — 가장 간단한 싱글톤

Python에서 모듈은 한 번만 import된다. 그래서 모듈 레벨 변수는 *자동으로* 싱글톤이다.

```python
# 파이썬 - settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str

settings = Settings()           # 모듈 import 시 한 번만 만들어진다
```

```python
# 파이썬 - 어디서든 import해서 쓰면 같은 객체
from app.settings import settings

@app.get("/info")
def info():
    return {"db": settings.database_url}
```

Spring의 `@Value("${...}")` 또는 `@ConfigurationProperties`에 해당한다. 설정값, 상수, *변하지 않는 자원*에 잘 어울린다. 7장에서 `pydantic-settings`를 정식으로 소개할 때 다시 만난다.

### `@lru_cache` — 늦은 싱글톤

함수의 결과를 캐싱하는 표준 라이브러리 도구다. 의존성 함수와 합치면 — 첫 호출 때 만들고, 그 다음부터는 캐시된 객체를 *재사용*한다.

```python
# 파이썬 - @lru_cache로 무거운 객체 캐싱
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()           # 첫 호출에만 실행. 그 뒤로는 캐시

@app.get("/info")
def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"db": settings.database_url}
```

이 패턴의 장점은 — *의존성 형태로 통일된다*는 점이다. 모든 자원을 `Depends`로 받으면 테스트할 때 *오버라이드*가 일관되게 적용된다. 잠시 뒤 *테스트 오버라이드* 절에서 만난다.

### 셋을 어떻게 골라 쓰나

| 자원 성격 | 도구 | 예 |
|---|---|---|
| 앱 수명에 묶이고 정리 단계가 있음 | `lifespan` | DB 엔진, HTTP 클라이언트 풀, ML 모델 |
| 설정값·상수·간단한 객체 | 모듈 레벨 변수 | `settings`, 상수 사전 |
| 테스트에서 갈아끼고 싶은 무거운 객체 | `@lru_cache` + `Depends` | 외부 API 클라이언트, 캐시 클라이언트 |

세 도구가 *겹친다*는 느낌이 들 텐데, 사실 겹친다. 어느 걸 골라도 동작은 한다. 다만 *테스트하기 좋은가*가 갈래를 만든다. 모듈 레벨 변수는 테스트에서 *몽키 패치*가 필요하다. `Depends`를 거치면 `app.dependency_overrides` 한 줄이면 끝난다.

## `yield` 의존성 — 라이프사이클 자원의 우아한 처리

지금까지 본 의존성 함수는 *값을 만들어 반환*했다. 그런데 *시작과 끝이 있는* 자원은 — 만들고 쓰고 닫는 — 어떻게 다룰까?

`yield`를 쓴다.

```python
# 파이썬 - yield 의존성
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session                  # 라우트에 세션 전달
        finally:
            await session.close()          # 라우트가 끝난 뒤 정리
```

함수가 *생성기*가 된다. `yield` 위쪽이 *셋업*, 아래쪽이 *틴다운*이다. `try/finally`를 써서 라우트에서 예외가 나도 정리가 보장된다.

Spring 사고로 옮기자면 — `@Transactional` 어노테이션이 메서드 위에 붙어 *시작·커밋·롤백·닫기*를 자동으로 처리해주던 것과 유사한 라이프사이클을, *의존성 함수의 `yield` 한 줄로* 풀어쓴 모양이다. 다른 점은 — 트랜잭션 *경계*가 자동이 아니라는 것. 6장 트랜잭션에서 이 차이가 한 챕터를 가져간다.

여기서 *한 가지 함정*을 짚고 가야 한다. **`finally`에서 `commit`을 호출하면 안 된다.**

왜냐? 의존성 `yield`의 `finally`는 *응답이 클라이언트로 나간 뒤*에 실행되기 때문이다. 그 시점에 예외가 나면, *응답에는 이미 200이 찍혔는데 트랜잭션은 실패한 상태*가 된다 ([GitHub fastapi/discussions/6452](https://github.com/fastapi/fastapi/discussions/6452)). 한 보고서가 *FastAPI 진영에서 가장 흔한 함정 중 하나*라고 꼽은 이유다.

권장 패턴은 — 세션은 `yield`로 *열고 닫기*만 의존성에서 처리하고, 커밋은 *라우트 또는 서비스 레이어에서 명시적으로*. 6장에서 본격적으로 풀어보겠지만 윤곽은 이렇다.

```python
# 파이썬 - 권장 패턴 (윤곽)
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session                  # 닫기는 컨텍스트 매니저가 알아서

@app.post("/orders")
async def create_order(
    payload: OrderCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    async with db.begin():             # 트랜잭션 경계는 여기서 명시
        order = Order(**payload.model_dump())
        db.add(order)
    return order
```

`get_db()`는 세션을 *제공*만 하고, *트랜잭션 경계*는 라우트가 그린다. *자원의 라이프사이클*과 *트랜잭션의 라이프사이클*이 서로 다른 개념이라는 사실이 — 이 분리에서 명확해진다. 이걸 한 어노테이션으로 합쳐주던 게 Spring의 `@Transactional`이었고, 그 합침이 *없는 세상*에서 어떻게 사는지가 6장의 화두다.

## `Annotated` 타입 별칭 — 같은 줄을 반복하지 않기

여기까지 코드를 봤으면 한 가지 어색함이 눈에 띌 거다.

```python
def some_route(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    ...
```

`Annotated[...]`가 *길다*. 라우트가 다섯 개, 열 개로 늘면 같은 줄이 자꾸 반복된다. 보기 좋지 않다.

해결책은 — **타입 별칭으로 묶기**다.

```python
# 파이썬 - deps.py
from typing import Annotated
from fastapi import Depends

DbDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
```

```python
# 파이썬 - router.py
from app.users.deps import DbDep, CurrentUserDep, SettingsDep

@app.post("/orders")
async def create_order(
    payload: OrderCreate,
    db: DbDep,
    user: CurrentUserDep,
    settings: SettingsDep,
):
    ...
```

훨씬 가볍다. Spring에서 `@Autowired` 자체가 한 단어인 것에 비하면 여전히 한 글자 더 적지만, 의도가 한눈에 들어온다. *DB가 필요해. 현재 사용자가 필요해. 설정이 필요해.* 그게 다다.

이 패턴은 한국 velog의 [FastAPI Good Practice (wjddn3711)](https://velog.io/@wjddn3711/FastAPI-Good-Practice) 글에서도 *기본 패턴*으로 권장된다. 도메인별 `deps.py`에 모아두는 게 — 4장 후반부에서 다시 만날 — *레이어드 폴더 구조*와 자연스럽게 맞물린다.

## 테스트 오버라이드 — 한 줄로 의존성을 갈아 끼우기

Spring 출신이 FastAPI의 DI를 보고 가장 *환호하는 자리*다.

Spring에서 우리는 `@MockBean`을 쓰거나, `@TestConfiguration`으로 별도 빈을 등록하거나, `@SpringBootTest`로 컨테이너를 새로 띄웠다. 빠르게 짜다 보면 보일러플레이트가 만만치 않다. *컨테이너를 갈아끼우는 비용*이 안 작다.

FastAPI는 한 줄이다.

```python
# 파이썬 - 테스트 오버라이드
from app.main import app
from app.users.deps import get_db

class FakeDb:
    def find(self, user_id: int):
        return User(id=user_id, name="홍길동")

app.dependency_overrides[get_db] = lambda: FakeDb()

# 이제 모든 라우트에서 get_db 자리에 FakeDb가 들어간다
```

`app.dependency_overrides`는 *딕셔너리*다. 키는 *원래 의존성 함수*, 값은 *대체할 팩토리*다. 키 한 줄을 갈아끼우면 — 그 함수를 의존하던 *모든 곳*이 자동으로 새 객체를 받는다. 그래프를 다시 그릴 필요가 없다.

FastAPI 공식 문서가 같은 의도를 한 줄로 정리한다 — 의존성 오버라이드는 *테스트 시 의존성을 교체하기 위해 설계된 도구*라고. 정확한 의도다. *DI는 테스트를 쉽게 하기 위한 도구다*라는 명제를 — 어쩌면 Spring보다 더 *문자 그대로* 실현한다.

테스트 끝나면 정리하는 것도 잊지 말자.

```python
# 파이썬 - pytest fixture로 깔끔하게
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: FakeDb()
    yield TestClient(app)
    app.dependency_overrides.clear()
```

`yield` 위쪽이 셋업, 아래쪽이 틴다운. 익숙한 모양 아닌가? FastAPI의 `yield` 의존성과 pytest의 `yield` fixture는 — 디자인이 일관된다. *Python 진영의 라이프사이클 표현 방식*이다. 10장 테스트에서 다시 풀어본다.

## APIRouter — 라우트를 도메인별로 묶기

여기까지 보면 한 가지 의문이 따라온다. *라우트가 늘면 `main.py`가 한없이 길어지는 거 아닌가?* 합리적인 의문이다. Spring에서는 `@RequestMapping("/api/users")`를 컨트롤러 클래스에 붙이고, 안에 메서드들이 *자연스럽게 묶였다*. FastAPI에는 그 자리가 어디일까?

답은 `APIRouter`다.

```python
# 파이썬 - users/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}")
def read_user(user_id: int, svc: UserServiceDep):
    return svc.find(user_id)

@router.post("")
def create_user(payload: UserCreate, svc: UserServiceDep):
    return svc.create(payload)
```

```python
# 파이썬 - main.py
from fastapi import FastAPI
from app.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)
```

`APIRouter`는 라우트들의 *부분집합*을 한 객체에 담는다. `prefix`로 공통 경로를, `tags`로 OpenAPI 문서의 그룹을 묶는다. Spring의 *클래스 단위 `@RequestMapping`* 와 거의 1:1이다.

본격적인 활용은 12장 통합 프로젝트에서 다시 본다. 지금은 *한 도메인의 라우트를 한 파일에 묶는 방법*만 손에 익혀두자. `users/router.py`, `users/schemas.py`, `users/service.py`, `users/repository.py`, `users/deps.py` — 5장에서 약속할 폴더 구조의 한 축이다.

## 미들웨어 — 횡단 관심사의 자리

DI를 통해서 횡단 관심사를 *함수 파라미터로* 끌어들이는 패턴을 봤다. 그런데 *정말로 모든 요청에 자동으로 적용*되어야 하는 일은 — Spring `@Aspect`나 `Filter`가 하던 일은 — 어디에 두는가?

답은 **ASGI 미들웨어**다.

```python
# 파이썬 - 요청 ID 미들웨어
from uuid import uuid4
from fastapi import Request

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = uuid4().hex
    request.state.request_id = rid              # 핸들러에서 꺼내 쓸 수 있게
    response = await call_next(request)         # 실제 요청 처리
    response.headers["X-Request-ID"] = rid      # 응답 헤더에도 박기
    return response
```

`call_next(request)` 한 줄이 *실제 라우트 처리*를 호출한다. 그 *전*과 *후*에 우리가 손을 쓸 수 있다. Spring `Filter` 또는 `HandlerInterceptor`와 같은 패턴이다.

여기서 한 가지 짚고 가자. **FastAPI에는 AOP가 없다.** Spring의 `@Aspect`, `@Around`, `@Before` 같은 *메서드 단위*로 횡단 관심사를 가로채는 메커니즘은 — *없다*. 대신 두 가지 도구로 나뉜다.

- **모든 요청에 자동 적용**: 미들웨어. 요청 ID, 로깅, CORS, GZip, 보안 헤더.
- **선택한 라우트에만 적용**: 의존성. 인증, 권한 검사, 도메인 컨텍스트 주입.

`@Aspect`의 자리에 *둘이 들어간다*. 처음엔 *나뉘어 있다는 사실*이 번거롭게 느껴진다. 익숙해지면 — *모든 곳에 걸리는 일*과 *선택한 곳에만 걸리는 일*이 *코드 위에서 분명히 구별된다*는 점이 오히려 마음에 들어온다. AOP가 *어디에 적용됐는지 추적하기 어려운* 경험을 해본 사람이라면 공감이 갈 거다.

요청 ID 미들웨어는 9장 관측성에서 본격적으로 활용된다. 분산 추적의 첫걸음이라 한 자리를 차지한다. 지금은 *한 미들웨어가 어떻게 생겼는지* 보고 가는 정도면 충분하다.

## 한 도메인을 한 폴더에 — 4장의 모든 것을 한자리에

지금까지 본 조각들을 한 도메인에 모아보자. 사용자 조회 API다. 5장에서 본격적으로 약속할 *by-feature 폴더 구조*의 한 예시다.

```
app/
  main.py
  core/
    settings.py
  db/
    session.py
  users/
    deps.py
    schemas.py
    repository.py
    service.py
    router.py
```

```python
# 파이썬 - app/db/session.py
from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.settings import settings

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
```

```python
# 파이썬 - app/users/schemas.py
from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}     # SQLAlchemy 객체에서 변환
```

```python
# 파이썬 - app/users/repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

```python
# 파이썬 - app/users/service.py
from app.users.repository import UserRepository
from app.users.schemas import UserRead

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def find(self, user_id: int) -> UserRead:
        user = await self.repo.find(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return UserRead.model_validate(user)
```

```python
# 파이썬 - app/users/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.users.repository import UserRepository
from app.users.service import UserService

DbDep = Annotated[AsyncSession, Depends(get_db)]

def get_user_repo(db: DbDep) -> UserRepository:
    return UserRepository(db)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]

def get_user_service(repo: UserRepoDep) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

```python
# 파이썬 - app/users/router.py
from fastapi import APIRouter
from app.users.deps import UserServiceDep
from app.users.schemas import UserRead

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, svc: UserServiceDep):
    return await svc.find(user_id)
```

```python
# 파이썬 - app/main.py
from uuid import uuid4
from fastapi import FastAPI, Request
from app.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = uuid4().hex
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response
```

이 한 폴더가 — 이 챕터의 모든 도구를 한자리에 모았다. `Depends` 그래프(`db → repo → service`), `yield` 의존성(`get_db`), `Annotated` 타입 별칭(`DbDep`, `UserRepoDep`, `UserServiceDep`), `APIRouter`, 미들웨어. Spring 사고로 옮기자면 — *한 도메인 패키지의 컨트롤러·서비스·레포지토리·DTO·@Bean 정의*가 한 폴더에 정리된 모습이다.

여기서 한 가지 묘한 감각이 든다. *Spring보다 코드가 적은가?* 그렇진 않다. *@Service·@Repository* 어노테이션이 사라진 자리에 *deps.py*가 들어왔다. 합산하면 비슷하다. 다른 건 — *그래프가 어디 있는지*다. Spring에서는 그래프가 *어노테이션의 모음*으로 *컨테이너 안에* 숨어 있었다. FastAPI에서는 그래프가 *deps.py 파일에 평면적으로 나열*된다. *코드 위에 그래프가 보인다*는 표현이 가장 정확하다.

## 테스트로 마무리 — 의존성 한 줄을 갈아끼우기

같은 도메인의 테스트는 어떻게 짤까?

```python
# 파이썬 - tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.users.deps import get_user_service
from app.users.schemas import UserRead

class FakeUserService:
    async def find(self, user_id: int) -> UserRead:
        return UserRead(id=user_id, username="홍길동", email="hong@example.com")

@pytest.fixture
def client():
    app.dependency_overrides[get_user_service] = lambda: FakeUserService()
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_read_user(client):
    response = client.get("/api/users/42")
    assert response.status_code == 200
    assert response.json() == {
        "id": 42,
        "username": "홍길동",
        "email": "hong@example.com",
    }
```

`app.dependency_overrides[get_user_service] = lambda: FakeUserService()` 한 줄. *그 한 줄*이 라우트의 그래프 전체에서 `UserService` 자리를 갈아끼운다. `UserRepository`도 `get_db`도 — *호출되지 않는다.* 왜냐? `FakeUserService`가 *그 위에 있어서* 아래 의존성들이 풀리지 않으니까. 그래프가 *함수 시그니처에 있다*는 사실이 — 이 테스트의 가벼움을 만든다.

Spring에서 이걸 하려면 `@MockBean UserService userService` + 컨테이너 재시작 비용을 감수해야 했다. FastAPI는 `TestClient(app)`만으로 — 컨테이너랄 게 없으니 — *재시작도 없다*. 테스트 한 개가 한 줄로 끝난다는 감각은 — 한번 손에 들어오면 잘 잊히지 않는다.

## 한 호흡으로 정리

지금까지 그린 그림을 머리에 박을 때다. 세 가지가 남아야 한다.

**첫째, `Depends()`는 함수 파라미터의 마커다.** 컨테이너가 그래프를 들고 있는 게 아니라, 함수 시그니처가 곧 그래프 명세다. 그래서 그래프가 *코드 위에 보인다*. 마법이 적다. 다만 — *같은 줄을 반복해서 적어야 한다*. `Annotated` 타입 별칭으로 줄이자.

**둘째, 기본 스코프는 요청 단위, 한 요청 안에서는 캐시된다.** 싱글톤이 필요한 자원은 의식적으로 만든다 — `lifespan`, 모듈 상수, `@lru_cache`. 세 도구가 겹치는 것 같지만 *테스트하기 좋은가*가 갈래를 만든다.

**셋째, 라이프사이클 자원은 `yield` 의존성으로, 테스트 교체는 `app.dependency_overrides` 한 줄로.** `yield` 위쪽이 셋업, 아래쪽이 틴다운. `finally`에서 *커밋하지 말 것*만 마음 한구석에 박아두자. 6장에서 트랜잭션 경계를 다룰 때 한 번 더 만난다.

그리고 한 가지 더 — **AOP는 없다.** Spring `@Aspect`의 자리에는 *미들웨어*(모든 요청에 자동)와 *의존성*(선택한 라우트에 명시) 두 개가 들어간다. 처음엔 번거롭지만 — *어디에 무엇이 적용되는지가 코드 위에서 분명히 보인다*는 게 익숙해지면 의외로 든든하다.

다음 5장은 데이터 접근이다. JPA에서 SQLAlchemy 2.0으로 옮겨가면서 Hibernate Session과 SQLAlchemy Session의 *닮음과 다름*을 만진다. `DetachedInstanceError`, `joinedload`, Alembic, 그리고 *Spring Data가 자동으로 만들어주던 레포지토리를 직접 짜는 손길*까지.

이 챕터에서 약속한 `Depends` 패턴이 5장에서 *세션 주입의 표준*으로 자리잡는다. *`yield` 의존성과 테스트 오버라이드를 안 보고 5장을 읽으면, 거기 코드가 마법처럼 보일 수 있다.* 그 사이 다리를 잘 건너가자.

준비됐는가? 가자.
