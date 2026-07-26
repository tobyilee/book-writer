# 11장. 테스트 — 공식 문서가 `anyio`를 쓰는 이유

FastAPI 공식 문서의 비동기 테스트 페이지에 이런 문장이 있다.

> "By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions."

테스트를 비동기로 돌리면 테스트 함수 안에서 `TestClient`를 쓸 수 없다는 말이다. 그런데 앞 문장이 더 낯설다.

> "AnyIO provides a neat plugin for this"

`pytest-asyncio`가 아니다. anyio다. 비동기 테스트를 붙여봤다면 당신도 십중팔구 `pytest-asyncio`부터 깔았을 텐데, 공식 문서는 다른 쪽을 가리킨다.

## 왜 하필 anyio인가

5장에서 우리는 숫자 하나를 소스까지 따라 내려갔다. `def` 경로 함수가 스레드로 밀려나고, 그 상한 40이 어디 있느냐 물었더니 anyio의 기본 리미터였다. `tracker`는 이미 anyio 위에서 돈다.

여기서부터는 저자의 읽기다. 공식 문서는 anyio 플러그인을 권하면서 **이유를 밝히지 않는다.** 다만 두 사실을 나란히 놓으면 이렇게 읽힌다 — 앱이 선 계층과 테스트가 도는 계층을 같은 물건으로 맞추는 편이 덜 어긋난다. `pytest-asyncio`를 쓰면 앱은 anyio 위에서, 테스트 루프는 다른 라이브러리 손에서 돈다. 대개는 잘 굴러가지만 어긋나는 날의 증상을 알아보기가 어렵다.

쓰는 방법은 간단하다. 비동기 테스트 함수에 마커를 붙이면 된다.[^11-1] 그런데 함정이 있다. 기본 제공되는 `anyio_backend` 픽스처는 **지원하는 모든 백엔드에서 테스트를 돌린다.** 지정하지 않으면 같은 테스트가 asyncio와 trio 양쪽으로 실행되는데, 공식 예제 디렉터리에 `conftest.py`가 없어 문서만 따라가면 만날 일이 없다. 쓰지도 않는 백엔드에서 실패가 난다. 난감한 첫 실패다.

픽스처 하나를 덮어쓰면 막힌다.

```python
# tests/conftest.py
import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
```

덧붙이자. anyio 4.14.2 / 2026-07 기준으로 문서는 `anyio_mode = "auto"` 설정으로 마커를 생략하는 길도 안내하면서, **`pytest-asyncio`의 `auto` 모드와 같이 켜면 충돌한다고 못 박는다.**[^11-1]

`pytest-asyncio` 쪽도 선택지인데 둘은 알고 가자. `asyncio_mode`가 `strict`(기본)냐 `auto`냐로 마커를 붙일지가 갈리고, **1.0.0(2025-05-26)에서 `event_loop` 픽스처가 제거됐다.** 커스텀 `event_loop` 예제는 그 이전 글이다.

## `TestClient`를 못 쓰게 되는 지점

`TestClient`는 동기 클라이언트다. `client.get("/issues/")` 앞에 `await`가 붙지 않으니 비동기 테스트 안에서는 쓸 수 없고, 대신 `AsyncClient`에 ASGI 전송을 물려 앱을 부른다.

그렇다면 `TestClient`는 쓸 데가 없어진 걸까? 오히려 하나는 `TestClient`만 해준다. 컨텍스트 매니저로 쓰면 lifespan 핸들러가 돈다.[^11-2] `AsyncClient`는 반대다 — 공식 문서가 경고 상자에 못 박았다.

> "If your application relies on lifespan events, the `AsyncClient` won't trigger these events."

`tracker`에게 남의 이야기가 아니다. 4장이 lifespan에 `app.state.http_client`를, 7장이 `app.state.redis`를 심었으니 `AsyncClient`로 부르면 그 둘 없이 요청이 든다. 공식 해법은 `asgi-lifespan`의 `LifespanManager`인데, 사실 하나는 병기하자. **그 패키지의 마지막 릴리스는 2.1.0 / 2023-03이고 3년 넘게 새 릴리스가 없다.**

이 장은 셋째 길을 간다. **lifespan이 만들어주던 것을 테스트에서는 의존성 오버라이드로 채운다.** Redis도 외부 HTTP 클라이언트도 테스트가 진짜로 필요한 물건은 아니다. lifespan 자체를 검증하려는 소수의 테스트에만 `TestClient`를 컨텍스트 매니저로 꺼내 쓰면 된다.

## `httpx`라는 이름이 세 층에 걸쳐 있다

하나를 정확히 짚고 가자. 버전을 확인하다 보면 `httpx2`라는 이름을 만나는데, 그걸 "FastAPI가 httpx2로 갈아탔다"로 읽으면 틀린다. 세 층이 각각 다른 이야기를 한다.

첫째 층 — FastAPI의 의존성. 0.140.0 / 2026-07 기준으로 `[standard]` extra가 핀하는 것은 `httpx<1.0.0`, 즉 여전히 구 httpx다. FastAPI 테스트 문서도 설치 명령으로 `uv add httpx`를 안내하고 비동기 예제의 첫 줄은 `from httpx import ASGITransport, AsyncClient`다.[^11-3] 문서와 패키지 메타데이터가 일치한다.

둘째 층 — Starlette의 TestClient. httpx2로 옮겨간 쪽은 여기다. Starlette 공식 문서의 축자는 이렇다.[^11-2]

> "The `TestClient` is built on `httpx2`. Plain `httpx` is still supported, but deprecated - install `httpx2` (included in `starlette[full]`) instead."

셋째 층 — 코드의 실제 모양. `testclient.py`는 `httpx2` 임포트를 시도하고 실패하면 구 httpx를 임포트한 뒤 경고를 띄운다. 그러니까 httpx2는 권장이지 필수가 아니다. 게다가 `as httpx` 별칭을 걸어 안쪽 이름은 그대로 두었다.

둘째와 셋째는 함께 읽어야 한다. 문서는 "deprecated"라고 쓰고 코드는 폴백을 남겼다. 당장 깨지진 않지만 Starlette이 방향을 정했다는 뜻이고, 첫째 층은 아직 따라가지 않았다. **공식 테스트 예제의 `from httpx import ...`와 최신 버전 표의 httpx2는 모순이 아니다. 서로 다른 층의 사실일 뿐이다.**

구 httpx의 마지막 릴리스는 0.28.1 / 2024-12-06으로 1년 7개월째 그대로다. 그래서 `tracker`는 httpx2를 고른다. 실익은 마지막 절에서 본다. 공식 예제를 따르려면 임포트만 `httpx`로 바꾸면 된다 — 이름이 같다.

이 장이 새로 쓰는 것을 넣자.

```bash
uv add --dev pytest anyio "httpx2[ws]"
```

`[ws]`는 장식이 아니다. WebSocket 지원이 이 extra에 묶여 있어, 빼면 마지막 절 임포트가 죽는다.[^11-6]

## 롤백을 비동기로 — 6장이 넘긴 숙제

6장은 테스트 격리 레시피를 인용하면서 선을 그었다. 커넥션을 열고, 트랜잭션을 시작하고, 세션을 `join_transaction_mode="create_savepoint"`로 묶고, 끝나면 바깥 트랜잭션을 롤백한다 — 커밋한 것까지 되돌리는 방식이다. 그런데 문서의 판은 동기 `Session`이고, `AsyncSession` 판은 6장이 뒤진 두 페이지에 없었다(전수 확인은 아니니 거기까지만).

없는 것을 지어내는 대신 소스를 열었다. 확인된 사실은 셋이다.[^11-4] `Session`의 생성자는 `bind`로 엔진 또는 커넥션을 받고, `join_transaction_mode`의 기본값 `conditional_savepoint` 옆에 `create_savepoint`를 문서화한다. `AsyncSession`의 생성자는 `bind`를 첫 인자로 받고 **나머지 키워드를 그대로 안쪽 `Session`에 넘긴다.** `AsyncConnection.begin()`이 돌려주는 `AsyncTransaction`에는 `rollback()`이 있다.

> **📐 저자 설계 —** 공식 문서에 비동기 판 레시피가 없어, 동기 레시피와 각주의 표면 셋으로부터 이 책이 조립했다.

```python
# tests/conftest.py
from typing import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.db import engine


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        db = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield db
        finally:
            await db.close()
            await transaction.rollback()
```

순서가 중요하다. 세션을 먼저 닫고 바깥 트랜잭션을 롤백한다. 반대면 살아 있는 세션이 끝난 트랜잭션 위에서 무언가를 하려 든다.

빈 데이터베이스를 전제로 둘을 보자.

```python
# tests/integration/test_isolation.py
import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.project import Project


@pytest.mark.anyio
async def test_creates_project(session: AsyncSession) -> None:
    session.add(Project(key="TRK", name="Tracker"))
    await session.commit()

    assert await session.scalar(select(func.count()).select_from(Project)) == 1


@pytest.mark.anyio
async def test_starts_empty_again(session: AsyncSession) -> None:
    assert await session.scalar(select(func.count()).select_from(Project)) == 0
```

앞 테스트가 `commit()`을 부르는데도 뒤 테스트는 빈 테이블을 본다. Spring의 `@Transactional` 테스트 롤백이 해주던 일이고, 여기서는 **당신이 그 배선을 직접 들고 있다.** 대신 어디까지 되돌아가는지가 픽스처 열두 줄에 있다.

엔진은 `tracker.db`의 것을 그대로 쓴다. 2장의 `Settings.database_url`을 읽으므로 `TRACKER_DATABASE_URL`만 바꾸면 스위트가 다른 데이터베이스를 본다. 스키마는 6장의 리비전을 `alembic upgrade head`로 올려두자. 스위트가 직접 만들면 편하지만, 그러면 **마이그레이션이 실제로 도는지를 영영 확인하지 못한다.**

진짜 Postgres를 띄우려면 testcontainers(4.15.0 / 2026-07 기준)가 JVM에서 쓰던 그 물건이다. 다만 이 책은 코드를 싣지 않는다. 공식 문서의 예제가 동기 엔진에 psycopg2 URL 하나뿐이라 **비동기 드라이버를 지정하는 형태의 예시가 없기 때문이다.**[^11-5] 확인 못 한 호출 형태를 지어 쓰느니 URL을 환경 변수로 받자.

## 무엇을 갈아 끼우고 무엇을 진짜로 둘 것인가

4장에서 `dependency_overrides`라는 딕셔너리를 소개만 하고 미뤄뒀다. 이제 꺼내자. Spring의 `@MockBean`, NestJS의 `overrideProvider()`에 대응하는데 구조는 훨씬 노골적이다. 컨테이너가 빈을 바꿔치기하는 게 아니라 딕셔너리에 함수 하나를 넣는다.

> **📐 저자 설계 —** 무엇을 갈아 끼우고 무엇을 그대로 둘지는 공식 권장이 아니라 이 책이 정한 경계다.

```python
# tests/conftest.py
from fastapi import FastAPI

from tracker.db import get_session
from tracker.deps import get_event_bus
from tracker.events import InMemoryEventBus
from tracker.main import app


@pytest.fixture
def event_bus() -> InMemoryEventBus:
    return InMemoryEventBus()


@pytest.fixture
async def wired_app(
    session: AsyncSession, event_bus: InMemoryEventBus
) -> AsyncIterator[FastAPI]:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_event_bus] = lambda: event_bus
    yield app
    app.dependency_overrides = {}
```

```python
# tests/conftest.py
from httpx2 import ASGITransport, AsyncClient


@pytest.fixture
async def client(wired_app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=wired_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

임포트 경로를 보자. `get_session`을 `tracker.db`에서 가져왔다. 6장의 `deps.py`가 이 함수를 `db.py`에서 임포트해 `SessionDep`에 넣었으니 `Depends`에 실제로 들어간 객체가 그것이라서다. **오버라이드의 키는 그 함수 객체 자체여야 한다.** 다른 모듈에서 같은 이름을 가져오면 딕셔너리에는 들어가는데 아무것도 바뀌지 않는다 — 조용히 실패하는 종류라 한 시간쯤 날리기 좋다.

마지막 줄 `app.dependency_overrides = {}`도 장식이 아니다. `app`은 모듈 전역이라 오버라이드가 테스트 뒤에도 남는다. 비우지 않으면 **뒤 테스트가 앞 테스트의 가짜 의존성을 물려받는다.**

무엇까지 갈아 끼울까. `tracker`가 바꾸는 것은 둘뿐이다. 세션을 테스트 트랜잭션 안으로 돌리고, 이벤트 버스를 `InMemoryEventBus`로 바꿔 Redis를 걷어낸다. 서비스도 리포지터리도 손대지 않는다. `IssueServiceDep`이 `get_issue_service`를 타고 `SessionDep`을 받으니 **세션 하나만 바꿔도 그 아래가 전부 진짜로 돈다.** 인증 경로를 보는 테스트라면 `get_current_user` 오버라이드가 한 줄 더 붙는다 — 10장이 채운 함수다.

이렇게 세우면 계약 확인이 짧아진다.

```python
# tests/integration/test_issues.py
import pytest
from httpx2 import AsyncClient


@pytest.mark.anyio
async def test_rejects_issue_without_title(client: AsyncClient) -> None:
    response = await client.post("/issues/", json={"project_id": 1})

    assert response.status_code == 422
    assert response.json()["code"] == "request.validation_failed"
```

3장이 정한 에러 계약이 처음 실행되며 검증된다. 422도 `request.validation_failed`도 3장의 약속이고, 지켜지는지 묻는 곳은 테스트다.

## 7장에서 만든 채널을 되찾기

약속한 실익은 여기 있다. httpx2에는 SSE와 WebSocket이 내장돼 있다.[^11-6] 7장에서 연 두 채널을 서드파티 없이 테스트한다는 뜻이다. `client.sse(...)`는 비동기 컨텍스트 매니저를 돌려주고 그 안을 `async for`로 돌면 `ServerSentEvent`가 나온다. WebSocket은 `client.websocket(...)`이고 텍스트·바이트·JSON 송수신 메서드가 달렸다. 서버 없이 ASGI 앱을 부르는 전송도 온다.

> **📐 저자 설계 —** `wait_for_subscriber`는 공식 API가 아니라 아래 경합을 피하려고 이 책이 만든 헬퍼다.

```python
# tests/integration/test_realtime.py
from datetime import datetime, timezone

import anyio
import pytest
from httpx2 import AsyncClient
from httpx2.websockets import ASGIWebSocketTransport

from tracker.events import InMemoryEventBus
from tracker.schemas.common import IssueEvent


async def wait_for_subscriber(bus: InMemoryEventBus, issue_id: int) -> None:
    with anyio.fail_after(1):
        while not bus.queues.get(issue_id):
            await anyio.sleep(0.01)


@pytest.mark.anyio
async def test_status_change_reaches_websocket(wired_app, event_bus) -> None:
    transport = ASGIWebSocketTransport(wired_app)
    async with AsyncClient(transport=transport) as ws_client:
        async with ws_client.websocket("ws://testserver/ws/issues/1") as ws:
            await wait_for_subscriber(event_bus, 1)
            await event_bus.publish(
                IssueEvent(
                    issue_id=1,
                    event_type="status_changed",
                    payload={"status": "resolved"},
                    occurred_at=datetime.now(timezone.utc),
                )
            )
            received = IssueEvent.model_validate(await ws.receive_json())

    assert received.event_type == "status_changed"
```

`wait_for_subscriber`가 왜 필요한지가 이 테스트의 교훈이다. 핸드셰이크가 끝났다고 서버가 구독을 마친 것은 아니다. 7장의 엔드포인트는 `accept()` 직후 이벤트를 밀어내는 태스크를 따로 띄우는데, 그게 큐를 등록하기까지 몇 번의 양보가 필요하다. 그 전에 발행하면 테스트가 **어쩌다 통과하고 어쩌다 실패한다.** 시간이 아니라 상태를 기다리자.

SSE도 모양은 같다. 같은 `wait_for_subscriber` 뒤에 `client.sse(...)`를 열고 `async for`로 첫 `ServerSentEvent`를 받아 `event.data`를 `IssueEvent`로 되돌리면 된다. 7장이 만든 두 채널이 스위트로 들어온다.

---

이 장에서 늘어난 파일은 사실상 `conftest.py` 하나인데, 거기에 지난 아홉 장의 결정이 접혀 들어갔다 — 4장의 오버라이드 딕셔너리, 6장의 트랜잭션 경계, 7장의 인메모리 버스, 3장의 에러 코드, 2장의 설정 필드까지. 스위트의 부속품이라기보다 당신이 내린 설계 결정의 목록에 가깝다.

픽스처를 늘릴 때마다 물어보자. 테스트를 편하게 하려는 것인가, 경계가 잘못 그어졌다는 신호인가.

[^11-1]: `pytest.mark.anyio`, 기본 `anyio_backend` 픽스처가 *"runs everything on all supported backends"*라는 서술, `yield` 비동기 픽스처, `anyio_mode = "auto"`와 `pytest-asyncio` `auto` 모드의 충돌 경고 — AnyIO *Testing with AnyIO*, https://anyio.readthedocs.io/en/stable/testing.html. `fail_after()`가 동기 컨텍스트 매니저라는 서술·`sleep()` — *Timeouts* (조회 2026-07-26)

[^11-2]: 인용한 축자 2건 — Starlette 공식 문서 *TestClient*, https://www.starlette.io/testclient/. `try: import httpx2 as httpx / except ModuleNotFoundError: import httpx` + `StarletteDeprecationWarning` 구조는 starlette 1.3.1 태그 `testclient.py` (조회 2026-07-26)

[^11-3]: `from fastapi.testclient import TestClient`와 설치 안내 `uv add httpx` — FastAPI 공식 문서 *Testing*. 축자 3건과 `from httpx import ASGITransport, AsyncClient` 예제 — 같은 문서 *Async Tests*, https://fastapi.tiangolo.com/tutorial/testing/ (조회 2026-07-26)

[^11-4]: `Session.__init__`의 `bind`·`join_transaction_mode` — SQLAlchemy 2.0 *Session API*, https://docs.sqlalchemy.org/en/20/orm/session_api.html. `AsyncSession.__init__(..., **kw)`가 나머지 키워드를 안쪽 `Session`에 넘긴다는 것, `AsyncConnection.begin() -> AsyncTransaction`과 그 `rollback()`·`AsyncSession.close()`, `await connection.begin()`을 성립시키는 `StartableContext.__await__` — sqlalchemy `rel_2_0_51` 소스 `ext/asyncio/` (조회 2026-07-26)

[^11-5]: `PostgresContainer`·`get_connection_url()`과 *"To get a URL without a driver, pass in `driver=None`."*, 그리고 **그 페이지의 예제가 동기 엔진 + psycopg2 하나뿐이라는 것** — testcontainers-python 공식 문서 *PostgreSQL* 모듈, https://testcontainers-python.readthedocs.io/en/latest/modules/postgres/. *"Version 4.0.0 onwards we do not support the `testcontainers-*` packages"*는 같은 문서 인덱스 Installation 절 (조회 2026-07-26)

[^11-6]: `client.sse(url)`·`client.websocket(url)`이 비동기 컨텍스트 매니저라는 것, `ServerSentEvent`의 `event`·`data`·`id`·`retry`·`json()`, 텍스트·바이트·JSON 송수신 메서드, `from httpx2.websockets import ASGIWebSocketTransport`를 `AsyncClient(transport=…)`에 물리는 예제, WebSocket이 `httpx2[ws]` extra(`wsproto`)에 묶여 있다는 서술 — httpx2 공식 문서 *SSE*·*WebSockets*·*API Reference*, https://httpx2.pydantic.dev/ (조회 2026-07-26)
