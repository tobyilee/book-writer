# 7장. 실시간 — WebSocket, SSE, 그리고 스트리밍

알림 기능을 붙였다. 스테이징에서 워커를 2개로 늘리자 알림이 절반만 도착한다. 무엇이 잘못됐을까?

코드는 그대로다. 브라우저 콘솔에도 서버 로그에도 오류가 없다. 도착하지 않은 절반은 흔적조차 남기지 않는다. 이런 종류의 버그가 제일 난감하다.

방향만 미리 말해두자. 잘못된 것은 알림 코드가 아니라 **연결이 어디에 사는가**에 대한 가정이다. 요청-응답 앱에서는 요청이 어느 프로세스에 떨어지든 상관없었다. 연결이 오래 살아 있는 앱에서는 그 편의가 사라진다.

## 끝나지 않는 함수

WebSocket 엔드포인트는 이렇게 생겼다.

```python
# (개념 설명용 — 파일 아님)
from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

> 출처: FastAPI 공식 문서 *APIRouter* (`APIRouter.websocket` 예제), https://fastapi.tiangolo.com/reference/apirouter/ (조회 2026-07-26)

지금까지 본 경로 함수와 결정적으로 다른 점이 있다. **이 함수는 끝나지 않는다.** 앞선 경로 함수들은 값을 돌려주고 죽었고 그 값이 응답 본문이 됐다. 여기서는 반환값 대신 `while True`가 있다. 함수가 사는 동안이 곧 연결이 사는 동안이다.

5장에서 우리는 함수가 이벤트 루프를 얼마나 오래 붙잡느냐를 걱정했는데, WebSocket 엔드포인트는 설계상 오래 붙잡는다. 대부분이 `await`에서 기다리는 시간이라 문제가 안 될 뿐이다.

**기본 설치만으로는 WebSocket이 동작하지 않는다.** uvicorn 기본 설치에는 구현체가 없고 `uvicorn[standard]`가 `websockets`를 설치한다. 공식 문서는 `uv add websockets`를 안내한다. 빠뜨리면 앱은 뜨는데 연결만 안 된다.

구현체도 하나가 아니다. uvicorn 0.51.0 / 2026-07 기준 `--ws` 선택지는 다섯이다 — `auto`·`none`·`websockets`·`websockets-sansio`·`wsproto`. 왜 비슷한 이름이 둘일까? 문서가 밝힌다.

> "Since `websockets` deprecated the API Uvicorn uses to run the previous protocol, we had to create this new protocol that uses the `websockets` SansIO API."

아래 라이브러리가 API를 정리하자 서버가 구현을 더 만든 것이다. 버전에 민감하니 배포할 uvicorn 문서를 확인하자.

한 층 아래로 내려가면 그림은 단순하다. `Upgrade` 헤더를 실은 GET에 서버가 101로 답한 뒤부터, ASGI 층에서는 `websocket.connect`·`receive`·`disconnect`가 올라오고 앱은 `websocket.accept`·`send`·`close`를 내려보낸다.

예외 처리도 HTTP와 다르다. 연결이 끊기면 수신 메서드가 `WebSocketDisconnect`를 던진다. 여기서 `HTTPException`은 의미가 없다 — 이미 HTTP 응답을 돌려줄 국면이 아니다. 대신 `WebSocketException`에 닫기 코드를 실어 던진다.[^7-1]

## 상위 프로토콜은 딸려 오지 않는다

Spring에서 WebSocket을 다뤄봤다면 당신은 이쯤에서 위화감을 느낀다. 거기서는 프레임을 직접 만지는 일이 드물었다 — 그 위에 STOMP라는 층이 있었기 때문이다. Spring 문서는 그 층이 왜 필요한지를 이렇게 설명한다.

> "The WebSocket protocol defines two types of messages (text and binary), but their content is undefined. The protocol defines a mechanism for client and server to negotiate a sub-protocol (that is, a higher-level messaging protocol)…"[^7-5]

프로토콜이 메시지의 **내용을 정의하지 않는다**는 것 — 이게 핵심이다. WebSocket이 주는 것은 양방향으로 흐르는 텍스트와 바이너리 프레임뿐이고, 목적지 주소도 구독이라는 개념도 브로커도 규격 안에 없다. STOMP는 그 빈 곳을 메우려고 얹은 층이고, SockJS는 WebSocket을 못 쓰는 환경을 위한 폴백이다.

FastAPI에는 그 층이 없다. 그러니 이렇게 읽어야 정확하다 — 무언가를 빼먹은 것이 아니라, 표준이 애초에 정해주지 않는 것을 프레임워크가 대신 정해주느냐 마느냐의 차이다. 정해주지 않으면 **당신이 정하게 된다.** 메시지에 종류를 실을지, 필드 이름은 무엇으로 할지, 무엇을 구독한다고 알릴지. 부채처럼 느껴진다면 절반은 맞다. 이득도 같은 곳에서 나온다 — 규약이 열 줄이면 되는 앱에 브로커를 배울 필요가 없다.

`tracker`는 규약을 작게 잡는다. 채널 하나가 이슈 하나에 대응하고, 그 위로는 한 가지 모양의 메시지만 흐른다.

> **📐 저자 설계 —** 아래 이벤트 스키마와 채널 규약은 FastAPI 공식 권장이 아니라, 상위 프로토콜이 없는 자리를 이 책이 메우기로 정한 한 가지 안이다.

```python
# src/tracker/schemas/common.py
from datetime import datetime

from pydantic import BaseModel

# ...(3장, 생략)


class IssueEvent(BaseModel):
    issue_id: int
    event_type: str
    payload: dict[str, str]
    occurred_at: datetime
```

3장의 요청·응답 스키마와 같은 도구로 메시지 규약을 적었다. 상위 프로토콜을 못 받은 대신, 경계에서 타입을 만드는 장치는 이미 있었다.

## 워커가 둘이면 알림은 절반만 간다

오프닝의 질문으로 돌아가자. 여러 연결에 한꺼번에 밀어주는 코드는 대개 이렇게 시작한다. 연결을 리스트에 담아두고, 이벤트가 생기면 돌면서 보낸다. FastAPI 공식 문서의 `ConnectionManager` 예제가 그 모양이고, 문서는 바로 아래에서 한계를 스스로 경고한다.

> "as everything is handled in memory, in a single list, **it will only work while the process is running, and will only work with a single process.**"

5장의 그 문장이 청구서로 돌아온다. **워커는 메모리를 공유하지 않는다.** 워커가 2개면 리스트도 2개다. A의 연결은 1번 워커에, B는 2번에 있다. 상태 변경 요청이 1번에 떨어지면 1번의 리스트만 순회하고 B는 아무것도 못 받는다. 알림이 절반만 도착하는 정체가 이것이고, 아무 예외도 안 나는 이유도 같다 — **코드는 자기가 아는 연결 전부에게 성공적으로 보냈다.**

필요한 것은 프로세스 경계를 건너는 배선이다. Socket.IO를 여러 인스턴스로 굴려봤다면 Redis 어댑터로 메시지를 퍼뜨렸을 텐데, 정확히 그 물건이 여기에는 없다.

FastAPI 공식 문서는 이 지점에서 `encode/broadcaster`를 권한다. 그런데 그 저장소는 2025-08-19에 아카이브됐다. PyPI 최신 릴리스는 0.3.1 / 2024-08-01이고, README 자신도 진작에 이렇게 적어두고 있었다.

> "At the moment broadcaster is in Alpha, and should be considered a working design document."

공식 문서가 아카이브된 라이브러리를 아직 링크하고 있다. 공식 대체재 안내도 없다. 인터넷 예제만 낡는 게 아니라 **공식 문서도 낡는다.**

직접 짜는 수밖에 없다. 발행과 구독 두 동작이면 된다.

> **📐 저자 설계 —** 아래 팬아웃 배선은 FastAPI 공식 권장이 아니라, 5장의 프로세스 경계로부터 이 책이 도출한 한 가지 안이다.

```python
# src/tracker/events.py
import asyncio
import json
from typing import AsyncIterator, Protocol

import redis.asyncio as redis

from tracker.schemas.common import IssueEvent


class EventBus(Protocol):
    async def publish(self, event: IssueEvent) -> None: ...

    def subscribe(self, issue_id: int) -> AsyncIterator[IssueEvent]: ...


class RedisEventBus:
    def __init__(self, client: redis.Redis) -> None:
        self.client = client

    def channel(self, issue_id: int) -> str:
        return f"tracker.issue.{issue_id}"

    async def publish(self, event: IssueEvent) -> None:
        await self.client.publish(
            self.channel(event.issue_id), event.model_dump_json()
        )

    async def subscribe(self, issue_id: int) -> AsyncIterator[IssueEvent]:
        async with self.client.pubsub() as pubsub:
            await pubsub.subscribe(self.channel(issue_id))
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=None
                )
                if message is not None:
                    yield IssueEvent.model_validate(json.loads(message["data"]))
```

`redis.asyncio`는 별도 패키지가 아니다. `aioredis`는 redis-py에 흡수됐으니 `uv add redis` 하나면 되고, `aioredis`를 설치하라는 글을 만나면 그건 낡은 자료다.[^7-3] 클라이언트를 만들면 커넥션 풀이 함께 생기는데, 그 기본 크기는 1차 소스로 확인하지 못했다. 구독자가 연결을 오래 붙드는 구조이니 확인해 잡아두는 편이 낫다.

공식 예제의 `ConnectionManager`가 하던 일은 구독이 대신한다. 연결마다 자기 구독을 가지니 목록을 들고 있을 필요가 없다. `EventBus`를 프로토콜로 선언한 이유는 구현이 하나가 아니어서다.

```python
# src/tracker/events.py
class InMemoryEventBus:
    def __init__(self) -> None:
        self.queues: dict[int, list[asyncio.Queue[IssueEvent]]] = {}

    async def publish(self, event: IssueEvent) -> None:
        for queue in self.queues.get(event.issue_id, []):
            queue.put_nowait(event)

    async def subscribe(self, issue_id: int) -> AsyncIterator[IssueEvent]:
        queue: asyncio.Queue[IssueEvent] = asyncio.Queue()
        self.queues.setdefault(issue_id, []).append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            self.queues[issue_id].remove(queue)
```

같은 두 메서드를 메모리 위에 구현한 것이 전부이고, 11장에서 이 구현을 끼워 넣는다.

## SSE는 이제 설치할 것이 없다

알림이 서버에서 클라이언트로만 흐른다면 WebSocket은 과하다. 이슈 상세 화면이 딱 그렇다 — 사용자가 실시간으로 보낼 것이 없고 남이 바꾼 상태가 반영되기만 하면 된다. 이럴 때 쓰는 것이 Server-Sent Events, Spring에서 `SseEmitter`를 돌려주던 자리다.[^7-5] 이 장에서 인터넷 자료를 가장 조심해야 할 지점이다. 검색으로 나오는 글의 대다수가 `sse-starlette`을 설치하라고 안내하는데, SSE는 **FastAPI 0.135.0(2026-03-01)에 정식 지원으로 들어왔다.**

```python
# (개념 설명용 — 파일 아님)
from fastapi.sse import EventSourceResponse, ServerSentEvent


@app.get("/items/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
```

> 출처: FastAPI 공식 문서 *Server-Sent Events (SSE)*, https://fastapi.tiangolo.com/tutorial/server-sent-events/ (조회 2026-07-25)

눈여겨볼 것은 반환 타입 애너테이션이다. `AsyncIterable[Item]`이라고 적으면 `yield`된 항목 하나하나가 JSON으로 인코딩돼 이벤트의 `data` 필드에 실리고, **Pydantic 검증과 자동 문서화가 그대로 따라온다.** 3장에서 쏟은 공이 스트림에도 적용된다. 이벤트 종류나 재시도 간격을 지정하려면 항목 대신 `ServerSentEvent`를 `yield`한다.

기본으로 해주는 일도 있다. 문서가 이렇게 적는다.

> "Send a 'keep alive' ping comment **every 15 seconds**… Set the `Cache-Control: no-cache` header… Set a special header **`X-Accel-Buffering: no`** to prevent buffering in some proxies like Nginx."

세 줄 다 다음 절에서 만난다. 재접속도 챙겨준다 — 브라우저가 다시 붙을 때 마지막으로 받은 `id`를 `Last-Event-ID` 헤더에 실어 보내므로 서버가 그 지점부터 이어 보낼 수 있다.[^7-2]

그렇다면 `sse-starlette`은 쓸모없어졌을까? 그렇게 정리하면 틀린다. 3.4.6 / 2026-07 기준으로 여전히 릴리스되고, Starlette만 쓰거나 종료 시점을 세밀히 제어할 때 줄 수 있는 것이 더 많다. 정확히는 **겹치는 영역에서 1차 선택지가 옮겨간 것**이다.

## 어느 쪽이 필요한지는 네 가지 질문으로 갈린다

둘 중 하나를 고르는 일은 취향처럼 보이지만, 실제로는 네 가지 질문이 대부분을 결정한다.

| 질문 | SSE | WebSocket |
|---|---|---|
| 방향이 한쪽인가 | 서버 → 클라이언트 단방향 | 양방향 |
| 끊겼을 때 누가 다시 붙나 | 브라우저가 다시 붙고 `Last-Event-ID`로 이어받는다 | 재접속과 재구독을 직접 짠다 |
| 중간 장비를 얼마나 타나 | 평범한 HTTP 응답 — 버퍼링만 끄면 된다 | 핸드셰이크 포워딩 설정이 따로 필요하다 |
| 인증을 어디에 붙이나 | 일반 요청과 동일 | 핸드셰이크 때 붙이고, 그 뒤는 직접 정한다 |

세 번째 행이 실무에서 가장 자주 아프다. SSE는 평범한 HTTP 응답이라 앞단이 무엇이든 대체로 통과하고, WebSocket은 프로토콜 승격이 필요해 앞단이 그 사실을 알아야 한다.

네 번째 행은 결이 다르다. WebSocket 엔드포인트에서도 `Depends`·`Cookie`·`Header`·`Query`를 쓸 수 있으므로[^7-1] 수락 전에 신원을 확인하기는 어렵지 않다. 문제는 그 뒤다. 연결이 몇 시간 사는데 토큰이 중간에 만료되면? HTTP에서는 다음 요청이 401을 받고 끝날 일이 여기서는 **아무 일도 일어나지 않는다.** 인가는 10장의 몫이지만, 그 결정이 여기까지 온다는 것은 기억해두자.

`tracker`의 결정은 이렇다. 이슈 상세 화면의 갱신은 SSE로 간다 — 단방향이고, 브라우저가 알아서 다시 붙고, 앞단 설정이 필요 없다. 양방향 채널이 필요한 클라이언트를 위해 WebSocket도 함께 연다. 둘 다 같은 이벤트를 소비하니 배선은 하나다.

## 로컬에서만 되는 스트리밍

응답을 조금씩 흘려보내는 코드는 로컬에서 잘 돈다. 그리고 배포하면 종종 안 된다 — 화면에 아무것도 안 나오다가 작업이 끝난 뒤 한꺼번에 쏟아진다. 뒷맛이 찜찜하다 — 틀린 데가 없어 보이는데 결과만 다르다.

범인은 대개 앞단의 버퍼링이다. nginx 문서를 보면 `proxy_buffering` 기본값이 `on`이고, 켜져 있으면 응답을 모아뒀다가 내보낸다. 같은 문서가 빠져나갈 길도 알려준다.

> "Buffering can also be enabled or disabled by passing 'yes' or 'no' in the 'X-Accel-Buffering' response header field."

앞 절에서 내장 SSE가 자동으로 붙여주던 그 헤더이고, 두 문서가 정확히 맞물린다. 다만 **자동으로 붙는 것은 SSE 응답이고**, 직접 만든 스트리밍 응답에는 우리가 붙여야 한다.

```python
# (개념 설명용 — 파일 아님)
from fastapi.responses import StreamingResponse
```

`StreamingResponse`는 제너레이터를 받아 본문을 흘려보낸다.[^7-4] 문서가 하나 더 경고한다 — 비동기 작업은 `await`에 도달해야 취소되므로, `await`가 없는 제너레이터는 취소 요청을 받고도 계속 돌 수 있다. 창을 닫은 클라이언트를 위해 서버가 계속 일하고 있을 수 있다는 뜻이고, 5장과 같은 뿌리다.

느린 클라이언트는 어떨까. 초당 만 건을 만드는데 받는 쪽이 백 건씩만 읽어간다면 그 차이가 쌓일 텐데, 여기서는 서버가 막아준다.

> "If the write buffer passes a high water mark, then Uvicorn ensures the ASGI `send` messages will only return once the write buffer has been drained below the low water mark."

즉 버퍼가 차면 `await send()`가 돌아오지 않는다. 우리 코드는 기다리고 그 사이 메모리는 늘지 않는다 — 백프레셔가 `await` 하나로 표현된 셈이다.

연결 수명에도 손잡이가 있다. uvicorn 0.51.0 / 2026-07 기준으로 WebSocket 연결에는 20초 간격의 핑과 20초의 핑 타임아웃, 16MB의 메시지 크기 상한, 32라는 수신 큐 상한이 걸려 있다(뒤의 둘은 구현체를 `websockets`로 둔 경우다). 조용히 사라진 클라이언트를 서버가 알아채는 길이 이 핑이다. 앞단이 자기 유휴 타임아웃을 가질 수 있다는 것도 함께 보자. 클라이언트 주소나 프로토콜이 뒤바뀌는 문제는 별개이고 13장의 소재다.

## `tracker`의 알림이 흐르는 길

조각을 붙이자. 발행 → 팬아웃 → 전달, 셋뿐이다. 상태를 바꾸는 곳은 서비스 계층이다.

> **📐 저자 설계 —** 아래 배선은 발행 시점을 커밋 이후로 못 박기 위한 이 책의 선택이며, 공식 권장이 아니다.

```python
# src/tracker/services/issue.py
from datetime import datetime, timezone

from tracker.errors import NotFoundError
from tracker.events import EventBus
from tracker.models.issue import Issue, IssueStatus
from tracker.schemas.common import IssueEvent


class IssueService:
    # ...(6장, 생략)

    async def change_status(
        self, issue_id: int, status: IssueStatus, events: EventBus
    ) -> Issue:
        issue = await self.issues.get(issue_id)
        if issue is None:
            raise NotFoundError("이슈를 찾을 수 없다", code="issue.not_found")
        issue.status = status
        await self.session.commit()
        await events.publish(
            IssueEvent(
                issue_id=issue.id,
                event_type="status_changed",
                payload={"status": status.value},
                occurred_at=datetime.now(timezone.utc),
            )
        )
        return issue
```

발행이 `commit()` **뒤**에 있다는 것이 이 코드의 전부다. 순서를 뒤집으면 아직 커밋되지 않은 변경을 알리게 되고, 알림을 받은 클라이언트가 곧바로 조회했을 때 옛날 값을 본다. 6장에서 "커밋은 서비스 계층이 한다"고 정해둔 덕분에 커밋 직후라는 시점을 이 메서드가 안다. 버스를 생성자가 아니라 메서드 인자로 받은 것도 4장이 정한 생성자를 흔들지 않으려는 선택이다. 시그니처도 움직였다 — 2장 스텁은 `status: str`이었는데, 6장에서 `IssueStatus`가 생겼으니 타입을 좁히고 발행을 위해 인자를 하나 더 받는다.

버스는 앱이 사는 동안 하나면 된다. 4장에서 HTTP 클라이언트를 놓아둔 곳에 Redis 클라이언트를 나란히 놓는다.

```python
# src/tracker/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ...(2장, 생략)

    redis_url: str
```

```python
# src/tracker/main.py
import redis.asyncio as redis

from tracker.api.realtime import router as realtime_router
from tracker.settings import get_settings

# ...(4장, 생략)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = AsyncClient(timeout=5.0)
    app.state.redis = redis.from_url(get_settings().redis_url)
    yield
    await app.state.redis.aclose()
    await app.state.http_client.aclose()


app.include_router(router=realtime_router)
```

```python
# src/tracker/deps.py
from fastapi import Request

from tracker.events import EventBus, RedisEventBus

# ...(4장, 생략)


def get_event_bus(request: Request) -> EventBus:
    return RedisEventBus(request.app.state.redis)


EventBusDep = Annotated[EventBus, Depends(get_event_bus)]
```

의존성이 `Request`를 받아 앱 상태에 닿는다.[^7-6] 4장의 별칭 체계를 따르니 라우터 쪽은 타입 한 줄이다. 마지막이 전달이다.

```python
# src/tracker/api/realtime.py
import asyncio
from typing import AsyncIterable

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.sse import EventSourceResponse

from tracker.deps import EventBusDep
from tracker.events import EventBus
from tracker.schemas.common import IssueEvent

router = APIRouter(tags=["realtime"])


@router.get("/issues/{issue_id}/events", response_class=EventSourceResponse)
async def issue_events(issue_id: int, events: EventBusDep) -> AsyncIterable[IssueEvent]:
    async for event in events.subscribe(issue_id):
        yield event


@router.websocket("/ws/issues/{issue_id}")
async def issue_channel(
    websocket: WebSocket, issue_id: int, events: EventBusDep
) -> None:
    await websocket.accept()
    pusher = asyncio.create_task(push_events(websocket, events, issue_id))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        pusher.cancel()


async def push_events(websocket: WebSocket, events: EventBus, issue_id: int) -> None:
    async for event in events.subscribe(issue_id):
        await websocket.send_text(event.model_dump_json())
```

SSE 쪽은 세 줄이면 끝난다 — 구독을 `yield`로 흘려보내면 나머지는 프레임워크가 한다. WebSocket 쪽은 왜 더 복잡할까. 밀어주기만 하는 채널인데도 **읽는 루프가 하나 더 있다.** 이유는 앞에서 본 계약이다. 클라이언트가 사라졌다는 사실이 `WebSocketDisconnect`로 올라오는 곳은 수신 메서드다. 아무것도 안 읽으면 상대가 떠난 것을 늦게 알고, 그동안 태스크와 구독이 계속 살아 있다. 그래서 밀어주는 일은 별도 태스크로 떼고, 본체는 읽으면서 연결이 살아 있는지만 지킨다. 상위 프로토콜이 없다는 말의 실제 비용이 이 여덟 줄이다.

이 배선은 워커 4개, 레플리카 3개로 늘려도 버틴다. 12개 프로세스가 각자 구독하고, 어디서 상태가 바뀌든 발행은 한 번, 전달은 연결이 붙은 곳마다 일어난다. 그 숫자는 13장의 몫이지만 **무엇이 되든 이 코드는 그대로다.**

남겨둘 구멍도 있다. 이 배선은 발행을 한 번 시도하고 끝낸다. 그 순간 아무도 구독하고 있지 않으면 이벤트는 사라지고, 다시 붙은 클라이언트가 `Last-Event-ID`를 보내와도 되돌려줄 기록이 없다. 유실돼도 새로 고치면 되는 기능이면 이걸로 족하다. 유실이 곤란하다면 그건 팬아웃이 아니라 **큐**로 풀 문제이고, 그 이야기는 오래 걸리는 일들과 함께 다룬다.

---

실시간 기능을 붙일 때 던지는 첫 질문이 바뀌었으면 한다. "어떻게 연결할까"가 아니라 **"이 연결은 몇 개의 프로세스 중 하나에만 붙어 있는가"**다. 이 질문을 먼저 하면 팬아웃이 나중에 붙이는 기능이 아니라 처음부터 있을 구조로 보인다.

[^7-1]: `WebSocket`·`WebSocketDisconnect`·`WebSocketException`·`@router.websocket`, WS 엔드포인트의 `Depends`·`Cookie`·`Header`·`Query` — https://fastapi.tiangolo.com/advanced/websockets/ , https://fastapi.tiangolo.com/reference/apirouter/ · `accept()`·`receive_text()`·`send_text()`와 수신 시 `WebSocketDisconnect` — https://github.com/Kludex/starlette/blob/master/docs/websockets.md (조회 2026-07-26)

[^7-2]: `fastapi.sse`의 `EventSourceResponse`·`ServerSentEvent`, `AsyncIterable` 반환 규약, 15초 핑·`Cache-Control: no-cache`·`X-Accel-Buffering: no`, `Last-Event-ID` — https://fastapi.tiangolo.com/tutorial/server-sent-events/ · 0.135.0 SSE 정식 지원 — https://fastapi.tiangolo.com/release-notes/ (조회 2026-07-25)

[^7-3]: `redis.asyncio`·`from_url()`·`pubsub()`·`subscribe()`·`get_message()`·`publish()`·`aclose()` — https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html (조회 2026-07-26) · `aioredis` 흡수 — https://github.com/aio-libs-abandoned/aioredis-py

[^7-4]: `fastapi.responses.StreamingResponse`, 취소 축자 — https://fastapi.tiangolo.com/advanced/custom-response/ (조회 2026-07-26)

[^7-5]: STOMP 축자 — https://docs.spring.io/spring-framework/reference/web/websocket/stomp.html · SockJS 폴백 절, `SseEmitter`가 `ResponseBodyEmitter`의 하위 클래스라는 서술 — https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html (조회 2026-07-26)

[^7-6]: `request.app` 축자 — https://github.com/Kludex/starlette/blob/master/docs/requests.md (조회 2026-07-26)
