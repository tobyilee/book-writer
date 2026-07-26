<!-- 검색 시점: 2026-07-25 기준 -->
# FastAPI 웹 리서치 (B조: 앱 스타일·데이터·운영·배포)

검색: **2026-07-25 기준**
담당 축: 애플리케이션 스타일 / 데이터 계층 / 프로덕션 관심사 / CI·CD / 클라우드 배포
(FastAPI 코어 API·비동기 내부·마이그레이션 함정은 A조 담당 — 여기서는 중복 수집하지 않음)

> **수집 원칙** — 버전·릴리스·지원 런타임 주장은 전부 1차 소스(PyPI JSON API, GitHub Releases, 벤더 공식 문서)를 실제 조회한 결과다. 조회일은 모두 2026-07-25.
> 블로그·튜토리얼은 "관점·경험담"으로만 인용했고 신뢰성 등급을 병기했다.
> 확인하지 못한 항목은 §7에 `⚠️ 미확인`으로 남겼다 — 지어내지 않았다.

---

## 0. 이 리서치에서 나온 "통념 교정" 5가지 (저술 시 최우선 반영)

책의 대상 독자(Spring Boot·NestJS 경험자)가 인터넷 자료로 FastAPI를 배우면 **거의 확실히 틀리게 알게 되는** 것들이다. 전부 1차 소스로 확인했다.

| # | 흔한 통념 (오래된 블로그·튜토리얼) | 2026-07-25 기준 사실 | 근거 |
|---|---|---|---|
| 1 | JWT는 `python-jose`, 비밀번호는 `passlib[bcrypt]` | 공식 보안 튜토리얼이 **`pyjwt` + `pwdlib[argon2]`** 로 바뀌었다 | [S1] |
| 2 | 프로덕션은 `gunicorn -k uvicorn.workers.UvicornWorker` | 공식 배포 문서에 **gunicorn이 아예 등장하지 않는다**. `fastapi run --workers` / `uvicorn --workers`, 그리고 K8s에서는 컨테이너당 1프로세스 | [S2][S3] |
| 3 | Starlette은 아직 0.x 베타 | **Starlette 1.0.0이 2026-03-22 릴리스**(창설 8년 만의 첫 stable). 저장소도 `encode/` → `Kludex/` 로 이전 | [S4][S5] |
| 4 | Starlette 1.0이 `on_event`·`@app.route`를 제거했으니 FastAPI에서도 못 쓴다 | **틀림.** FastAPI는 `starlette>=0.46.0`으로만 핀하고, `on_event`·`middleware`·`exception_handler`·`websocket_route`를 **자체 구현으로 계속 제공**한다 (단 `on_event`는 FastAPI 자체적으로 deprecated) | [S6][S7] |
| 5 | 파이썬 의존성은 pip/poetry가 표준 | FastAPI 공식 문서가 **0.140.0(2026-07-24)에서 "uv projects를 기본으로" 문서를 개편**했다 | [S8] |

---

## 1. 애플리케이션 스타일별 패턴

### 1-A. WebSocket — 독자가 실제로 쓰는 API [S21][S130]

FastAPI 공식 문서의 기본 형태 [S21]:
```python
from fastapi import FastAPI, WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```
> Technical Details: "You could also use `from starlette.websockets import WebSocket`. FastAPI provides the same `WebSocket` directly just as a convenience for you, the developer. **But it comes directly from Starlette.**" [S21]
> "In WebSocket endpoints you can import from `fastapi` and use: `Depends`, `Security`, `Cookie`, `Header`, `Path`, `Query`." [S21]

설치는 `uv add websockets` (문서가 uv 기준으로 개편됨, §4-A) [S21].

**`WebSocket` 객체의 실제 API — Starlette 공식 문서 원문에서 확인** [S130]:

| 구분 | 시그니처 |
|---|---|
| 생성자 | `WebSocket(scope, receive=None, send=None)` |
| 수락 | `await websocket.accept(subprotocol=None, headers=None)` |
| 송신 | `await websocket.send_text(data)` / `send_bytes(data)` / `send_json(data)` |
| 수신 | `await websocket.receive_text()` / `receive_bytes()` / `receive_json()` |
| 이터레이션 | `websocket.iter_text()` / `iter_bytes()` / `iter_json()` |
| 종료 | `await websocket.close(code=1000, reason=None)` |
| 원시 ASGI | `await websocket.send(message)` / `await websocket.receive()` |
| 거부 응답 | `await websocket.send_denial_response(response)` |

속성 [S130]: `websocket.url`(str 서브클래스 — `.path`·`.port`·`.scheme` 노출), `websocket.headers`(immutable, case-insensitive multi-dict), `websocket.query_params`, `websocket.path_params`. 매핑 인터페이스도 제공한다 — `websocket['path']`.

문서 원문 인용 [S130]:
> "JSON messages default to being sent over text data frames, from version 0.10.0 onwards. Use `websocket.send_json(data, mode="binary")` to send JSON over binary data frames."
> 수신 메서드에 대해: "May raise `starlette.websockets.WebSocketDisconnect()`."
> 이터레이터에 대해: "**When `starlette.websockets.WebSocketDisconnect` is raised, the iterator will exit.**"
> 원시 메시지에 대해: "If you need to send or receive raw ASGI messages then you should use `websocket.send()` and `websocket.receive()` rather than using the raw `send` and `receive` callables. **This will ensure that the websocket's state is kept correctly updated.**"
> **연결 거부:** "**If you call `websocket.close()` before calling `websocket.accept()` then the server will automatically send a HTTP 403 error to the client.**" / `send_denial_response()`는 "requires the ASGI server to support the WebSocket Denial Response extension. If it is not supported a `RuntimeError` will be raised."

**예외 처리** [S21]:
> "When a WebSocket connection is closed, the `await websocket.receive_text()` will raise a `WebSocketDisconnect` exception, which you can then catch and handle"
> "As this is a WebSocket it doesn't really make sense to raise an `HTTPException`, instead we **raise a `WebSocketException`**."

```python
from fastapi import WebSocketException, status
raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
```
Starlette 정의: `WebSocketException(code=1008, reason=None)` — "You can set any code valid as defined in the specification." [S131]

**연결 관리·브로드캐스트 — FastAPI 문서의 `ConnectionManager` 원문 코드** [S21]:
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```

**🔴 그리고 문서 자신이 곧바로 한계를 경고한다 (원문)** [S21]:
> "The app above is a minimal and simple example to demonstrate how to handle and broadcast messages to several WebSocket connections.
> But keep in mind that, as everything is handled in memory, in a single list, **it will only work while the process is running, and will only work with a single process.**
> If you need something easy to integrate with FastAPI but that is more robust, supported by Redis, PostgreSQL or others, check **encode/broadcaster**."

→ 이 경고가 §5-A의 "워커 여러 개" 권장과 정면으로 부딪힌다. 그리고 문서가 가리키는 해법(`broadcaster`)이 지금은 아카이브 상태다 — **§1-E 참조.**

### 1-A′. WebSocket — Uvicorn 레벨의 실제 동작 [S10][S11]

FastAPI의 `@app.websocket` 위에서 **실제로 무슨 일이 벌어지는지**를 서버 문서로 확인했다. Spring의 `@ServerEndpoint`/STOMP에 익숙한 독자에게는 이 계층 구분이 핵심이다.

- 핸드셰이크: 클라이언트가 `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key`, `Sec-WebSocket-Version: 13` 헤더로 GET → 서버가 **HTTP 101 Switching Protocols** + `Sec-WebSocket-Accept` 응답 [S11]
- ASGI 이벤트로의 번역 (원문 그대로) [S11]:
  - 서버→앱: `websocket.connect` / `websocket.receive` / `websocket.disconnect`
  - 앱→서버: `websocket.accept` / `websocket.send` / `websocket.close`
- **연결 거부**는 `websocket.http.response.start`로 HTTP 403 등을 돌려주는 경로가 따로 있다 [S11]
- **WebSocket 구현체가 3개다** [S11] — `--ws` 옵션으로 선택:
  | 구현 | 근거 패키지 | 비고 |
  |---|---|---|
  | `wsproto` | `wsproto` | 가장 먼저 구현된 것 |
  | `websockets` | `websockets` | **`websockets` 설치 시 기본값** |
  | `websockets-sansio` | `websockets` SansIO API | 아래 인용 참조 |

  > "Since `websockets` deprecated the API Uvicorn uses to run the previous protocol, we had to create this new protocol that uses the `websockets` SansIO API." [S11]
  > "The SansIO implementation was released in Uvicorn version 0.35.0 in June 2025." [S11]

  → 즉 `websockets` 상위 라이브러리의 API deprecation 때문에 Uvicorn이 새 구현을 만든 상황. **버전 민감 주제**이므로 책에서는 "Uvicorn 0.51.0/2026-07 기준 `--ws` 선택지 4종(auto/none/websockets/websockets-sansio/wsproto)"으로 못 박을 것.
- WebSocket 관련 기본값 (Uvicorn 0.51.0/2026-07 기준) [S10]:
  - `--ws-max-size` **16777216 (16MB)** / `--ws-max-queue` **32**(`websockets` 프로토콜 전용)
  - `--ws-ping-interval` **20.0초** / `--ws-ping-timeout` **20.0초**
  - `--ws-per-message-deflate` **True**(`websockets` 전용)
- **nginx 앞단에 둘 때** WebSocket 포워딩 설정이 필요하다 — Uvicorn 공식 문서의 nginx 예시가 `proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection $connection_upgrade;` 와 `map $http_upgrade $connection_upgrade { default upgrade; '' close; }` 를 포함한다 [S10]

> **다중 워커 팬아웃 문제는 §1-E에서 다룬다** — FastAPI 공식 문서가 권하는 `broadcaster`가 **아카이브됐다**는 사실이 핵심이다. 최신 릴리스는 0.3.1 / 2024-08-01(§6-4).

### 1-B. SSE와 프록시 버퍼링 — 1차 소스 확보 [S10]

SSE·스트리밍이 "로컬에서는 되는데 배포하면 안 되는" 전형적 원인이 프록시 버퍼링이다. Uvicorn 공식 nginx 예시가 **`proxy_buffering off;`를 이미 포함하고 있다** [S10] — 추측이 아니라 공식 권장 설정에 들어 있다는 점이 인용 포인트.

관련 서버 동작 (원문) [S12]:
> "If no `Content-Length` header is included then Uvicorn will use chunked encoding for the response body, and will set a `Transfer-Encoding` header if required."

> "Once a response has been sent, Uvicorn will no longer buffer any remaining request body. Any later calls to `receive` will return an `http.disconnect` message."

**Write flow control** (백프레셔 — 스트리밍 응답 설계 시 핵심) [S12]:
> "If the write buffer passes a high water mark, then Uvicorn ensures the ASGI `send` messages will only return once the write buffer has been drained below the low water mark."

→ 즉 느린 클라이언트에게 `StreamingResponse`로 밀어넣어도 `await send()`가 알아서 막힌다. 메모리 폭주 방지 기제를 서버가 제공한다는 것을 명시할 수 있다.

**Read flow control** (대용량 업로드 시) [S12]:
> "Uvicorn will pause reading from a transport once the buffered request body hits a high water mark, and will only resume once `receive` has been called, or once the response has been sent."

### 1-C. 프록시 뒤에 배치 (BFF·게이트웨이 앞단) [S13]

경로 프리픽스를 떼어내는 게이트웨이 뒤에 FastAPI를 둘 때의 공식 해법은 `root_path`다.

```bash
$ uv run fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1
```
```python
from fastapi import FastAPI, Request

app = FastAPI(root_path="/api/v1")

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```
(둘 다 공식 문서에서 그대로 옮김 [S13])

- 프록시는 `https://myawesomeapp.com/api/v1`에서 받아 `/api/v1`을 **떼고** `http://127.0.0.1:8000/app`으로 넘긴다 [S13]
- FastAPI가 OpenAPI 스키마에 `servers` 항목을 자동 추가한다 — `{"servers": [{"url": "/api/v1"}]}` [S13]
- 커스텀 `servers`를 줄 때 `root_path` 서버가 **맨 앞에 삽입**되며, `root_path_in_servers=False`로 끌 수 있다 [S13]
- 공식 예시 커맨드가 `--forwarded-allow-ips="*"`를 함께 쓴다 [S13] — §5-C의 보안 주의사항과 반드시 묶어서 서술할 것

### 1-D. 🔴 FastAPI에 SSE가 **내장**됐다 (0.135.0) — 최신성 최대 쟁점 [S16][S17]

시중 자료 100%가 "FastAPI에서 SSE 하려면 `sse-starlette` 깔아라"라고 말한다. **더 이상 필수가 아니다.**

FastAPI 릴리스 노트 원문 [S17]:
> `0.135.0 (2026-03-01)` — Features — "✨ Add support for Server Sent Events. PR #15030 by @tiangolo. New docs: Server-Sent Events (SSE)."
> `0.134.0 (2026-02-27)` — Features — "✨ Add support for streaming JSON Lines and binary data with yield. PR #15022 by @tiangolo. **This also upgrades Starlette from >=0.40.0 to >=0.46.0**, as it's needed to properly unwrap and re-raise exceptions from exception groups."

공식 문서 본문에 `Added in FastAPI 0.135.0.` 명시 [S16]. API:
```python
from fastapi.sse import EventSourceResponse, ServerSentEvent

@app.get("/items/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
```
- "Each yielded item is encoded as JSON and sent in the `data:` field of an SSE event." [S16]
- `AsyncIterable[Item]`로 선언하면 **Pydantic 검증·문서화·직렬화가 그대로 적용된다** [S16]
- `def` + `yield`(동기)도 지원: "FastAPI will make sure it's run correctly so that it doesn't block the event loop." [S16]
- 이벤트 필드 제어: `yield ServerSentEvent(data=item, event="item_update", id=str(i + 1), retry=5000)`, 주석은 `ServerSentEvent(comment=...)`, 원문 전송은 `raw_data=` [S16]
  - "`data` and `raw_data` are mutually exclusive." [S16]
- 재접속 이어받기: `last_event_id: Annotated[int | None, Header()] = None` — "When a browser reconnects after a connection drop, it sends the last received `id` in the `Last-Event-ID` header." [S16]
- POST에서도 됨: "SSE works with any HTTP method, not just GET. This is useful for protocols like **MCP** that stream SSE over POST." [S16]

**§1-B의 프록시 버퍼링 문제를 FastAPI가 기본으로 처리한다 (Technical Details 원문)** [S16]:
> "FastAPI implements some SSE best practices out of the box.
> Send a "keep alive" ping comment **every 15 seconds** when there hasn't been any message, to prevent some proxies from closing the connection, as suggested in the HTML specification: Server-Sent Events.
> Set the `Cache-Control: no-cache` header to prevent caching of the stream.
> Set a special header **`X-Accel-Buffering: no`** to prevent buffering in some proxies like Nginx.
> You don't have to do anything about it, it works out of the box. 🤓"

**`sse-starlette`(3.4.6 / 2026-07-20)는 여전히 유효**하다 — Starlette 단독 사용이나 세밀한 제어가 필요할 때. `EventSourceResponse`의 기본 `ping`도 **15초**로 동일하고, `shutdown_event`·`shutdown_grace_period`·`send_timeout` 같은 종료 제어가 더 풍부하다 [S18]. 저자 주의사항 (원문) [S18]:
> "`shutdown_grace_period` should be less than your ASGI server's graceful shutdown timeout (e.g. uvicorn's `--timeout-graceful-shutdown`), otherwise the process is killed before the grace period expires."
> "Hanging connections after client disconnect — Always check `await request.is_disconnected()` in loops; Use `send_timeout` parameter to detect dead connections."

**nginx 1차 소스로 버퍼링 확정** [S19] (원문):
> `proxy_buffering on | off;` / Default: **`proxy_buffering on;`**
> "When buffering is disabled, the response is passed to a client synchronously, immediately as it is received."
> "**Buffering can also be enabled or disabled by passing "yes" or "no" in the "X-Accel-Buffering" response header field.**"

→ 즉 `X-Accel-Buffering: no`가 통하는 이유가 nginx 공식 문서에 명시돼 있다. FastAPI가 이 헤더를 자동으로 붙인다[S16]는 사실과 정확히 맞물린다.

### 1-E. 🔴 `broadcaster`가 아카이브됐다 — 그런데 공식 문서는 아직 링크 중 [S20]

FastAPI WebSocket 문서의 Tip 원문 [S21]:
> "But keep in mind that, as everything is handled in memory, in a single list, **it will only work while the process is running, and will only work with a single process.**
> If you need something easy to integrate with FastAPI but that is more robust, supported by Redis, PostgreSQL or others, check **encode/broadcaster**."

**그런데 그 저장소는 아카이브 상태다** — GitHub API 직접 조회(2026-07-25): `archived=true`, 마지막 push `2025-04-09` [S20]. 저장소 페이지 원문: "This repository was archived by the owner on **Aug 19, 2025**. It is now read-only."

README 자체 경고 (원문) [S20]:
> "At the moment broadcaster is in Alpha, and should be considered a working design document. The API should be considered subject to change. If you do want to use Broadcaster in its current state, make sure to strictly pin your requirements to `broadcaster==0.3.0`."

PyPI 최신 **0.3.1 / 2024-08-01** (§6-4).

→ **책의 결론:** 다중 워커 WebSocket 팬아웃은 **Redis pub/sub을 직접 구현**하는 게 현재로선 정공법이다. `redis.asyncio`의 pub/sub(§2-I)과 §1-A의 `ConnectionManager`를 결합하는 패턴으로 서술할 것. 공식 문서가 아카이브된 라이브러리를 아직 링크한다는 사실 자체가 "공식 문서도 늙는다"는 이 책의 메시지를 뒷받침하는 좋은 사례다.

### 1-F. 서버 렌더링 — `TemplateResponse` 인자 순서와 `app.frontend()` [S22][S23][S17]

현재 문서가 보여주는 형태 [S22]:
```python
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
```
문서 자체의 Note (원문) [S22]:
> "**Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter.** Also, before that, in previous versions, the `request` object was passed as part of the key-value pairs in the context for Jinja2."

→ 인터넷 예제가 `TemplateResponse("item.html", {"request": request})` 형태라면 **구버전**이다. 그리고 Starlette 1.0.0이 옛 시그니처를 **완전히 제거**했다(§0 #4, [S5]) — "Remove deprecated `TemplateResponse(name, context)` signature from Jinja2Templates". 즉 Starlette 1.x에서는 옛 코드가 **동작하지 않는다.**

Starlette 쪽 추가 사실 [S23]:
> "Note that the incoming request instance **must** be included as part of the template context."
> "When using the `directory` argument, Starlette enables autoescape by default for `.html`, `.htm`, and `.xml` templates using `jinja2.select_autoescape()`. This protects against Cross-Site Scripting (XSS) vulnerabilities…"

(Starlette 1.0.0 릴리스 노트에도 "Enable autoescape by default in Jinja2Templates"가 Fix로 올라 있다 [S5].)

**새 기능: `app.frontend()`** — SPA 호스팅용. 릴리스 노트 원문 [S17]:
> `0.138.0 (2026-06-20)` — "✨ Add support for `app.frontend("/", directory="dist")` and `router.frontend("/", directory="dist")`. PR #15800"
> `0.139.0 (2026-07-01)` — "✨ Support dependencies in `app.frontend()`, e.g. for automatic cookie authentication for the frontend. PR #15908"

`StaticFiles` 문서 최상단이 이제 이렇게 안내한다 (원문) [S24]:
> "If you need to host a frontend, use `app.frontend()` instead, read about it in Frontend. `app.frontend()` uses `StaticFiles` underneath, with several additional advantages for frontends, like handling client-side routing."

- "FastAPI checks path operations first. The frontend files are checked only if no normal route matched, so your API won't be affected." [S24]
- fallback은 **`Accept: text/html`인 GET/HEAD에만** 적용 — JS/CSS/이미지 누락은 여전히 404 [S24]
- 프론트엔드 응답에도 미들웨어·의존성이 적용된다 → **쿠키 인증으로 프론트엔드 보호 가능** [S24]

### 1-G. GraphQL — 공식 문서의 실제 권장 [S25]

FastAPI 문서 원문 [S25]:
> "**If you need or want to work with GraphQL, Strawberry is the recommended library as it has the design closest to FastAPI's design, it's all based on type annotations.**"
> "**Older GraphQLApp from Starlette** — Previous versions of Starlette included a `GraphQLApp` class to integrate with Graphene. It was deprecated from Starlette…"

Starlette의 GraphQL 제거는 **확정 사실**이며 시점도 특정된다 [S26]:
> "GraphQL support in Starlette was **deprecated in version 0.15.0, and removed in version 0.17.0**."
> 릴리스 노트: `0.17.0 (November 4, 2021)` — Removed — "Remove GraphQL support #1198."

→ 즉 GraphQL 제거는 **2021년 사건**이지 Starlette 1.0과 무관하다. (Agent 리서치 중 혼동 소지가 있었던 지점을 1차 소스로 정리했다.)

Strawberry 통합 [S27]: `pip install 'strawberry-graphql[fastapi]'`, `GraphQLRouter`.
```python
from strawberry.fastapi import GraphQLRouter
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```
**Spring/Nest 개발자가 반드시 걸리는 함정 (Strawberry 공식 Note 원문)** [S27]:
> "FastAPI processes sync endpoints in a threadpool and async endpoints using the event loop. However, **Strawberry processes sync and async fields using the event loop, which means that using a `sync def` will block the entire worker.** It is recommended to use `async def` for all of your fields… If you can't use `async`, make sure you wrap blocking code in a suspending thread, for example using `starlette.concurrency.run_in_threadpool`."

→ FastAPI의 "def면 스레드풀" 규칙이 **GraphQL 리졸버에는 적용되지 않는다**는 것. 이 책에서 매우 가치 있는 디테일이다.

### 1-H. 파일 업로드 — 한도는 어디에 있나 [S28][S29]

FastAPI 문서 원문 [S28]:
> "If you declare the type of your path operation function parameter as `bytes`, FastAPI will read the file for you… **Keep in mind that this means that the whole contents will be stored in memory.**"
> "`UploadFile`… **It uses a "spooled" file: A file stored in memory up to a maximum size limit, and after passing this limit it will be stored on disk.**"
> "It exposes an actual Python `SpooledTemporaryFile` object that you can pass directly to other libraries that expect a file-like object."

⚠️ **FastAPI 문서는 이 임계값의 구체적 바이트 수를 밝히지 않는다** → §7 참조.

**실질적 방어선은 Starlette의 `request.form()`에 있다 (원문)** [S29]:
> Signature: `request.form(max_files=1000, max_fields=1000, max_part_size=1024*1024)`
> "**These limits are for security reasons, allowing an unlimited number of fields or files could lead to a denial of service attack by consuming a lot of CPU and memory parsing too many empty fields.**"

`UploadFile.size` 속성 (FastAPI 튜토리얼에는 없고 Starlette 문서에만 있음) [S29]:
> "An int with uploaded file's size in bytes. **This value is calculated from request's contents, making it better choice to find uploaded file's size than `Content-Length` header.**"

스트리밍 업로드 [S29]:
```python
body = b''
async for chunk in request.stream():
    body += chunk
```
> "**If you access `.stream()` then the byte chunks are provided without storing the entire body to memory. Any subsequent calls to `.body()`, `.form()`, or `.json()` will raise an error.**"

**전역 요청 바디 크기 제한은 프레임워크에 없다.** Uvicorn의 Resource Limits는 `--limit-concurrency`/`--limit-max-requests`/`--backlog`뿐이고(§3-C, §3-D), Starlette에도 전역 max-body-size 기능은 도입된 적이 없다. 존재하는 건 multipart 파트 단위 한도뿐이며, 관련 보안 이력이 있다 [S5]:
- `0.40.0 (2024-10-15)` — "This release fixes a Denial of service (DoS) via multipart/form-data requests… **GHSA-f96h-pmfr-66vw**" / "Add `max_part_size` to `MultiPartParser`"
- `0.46.0 (2025-02-22)` — "MultiPartParser: **Rename `max_file_size` to `spool_max_size`**"
- `1.3.1 (2026-06-12)` — Fixed: "**Enforce `max_fields` and `max_part_size` in FormParser #3329.**"

→ **결론: 업로드 크기 상한은 리버스 프록시(nginx `client_max_body_size`)나 직접 만든 ASGI 미들웨어의 몫이다.** 이건 Spring의 `spring.servlet.multipart.max-file-size` 한 줄에 익숙한 독자에게 반드시 짚어야 할 차이다.

S3 presigned URL (AWS 공식) [S30]:
> "**Using a presigned URL will allow an upload without requiring another party to have AWS security credentials or permissions.** A presigned URL is limited by the permissions of the user who creates it."
> 만료: "If you create a presigned URL with the Amazon S3 console, the expiration time can be set between **1 minute and 12 hours**. If you use the AWS CLI or AWS SDKs, the expiration time can be set as high as **7 days**."
> "IAM role credentials used by Amazon EC2 instances – Valid for the duration of the role credentials (**typically 6 hours**)."
> "**You can use the presigned URL multiple times, up to the expiration date and time.**"

### 1-I. 마이크로서비스·BFF — httpx의 재시도는 당신 생각과 다르다 [S31]

**가장 중요한 교정 (httpx 공식 문서 원문)** [S31]:
> "**Requests will be retried the given number of times in case an `httpx.ConnectError` or an `httpx.ConnectTimeout` occurs**, allowing smoother operation under flaky networks. **If you need other forms of retry behaviors, such as handling read/write errors or reacting to 503 Service Unavailable, consider general-purpose tools such as `tenacity`.**"

→ `httpx.HTTPTransport(retries=3)`은 **연결 수립 실패만** 재시도한다. 503도, read 타임아웃도 재시도하지 않는다. Spring `RetryTemplate`·Resilience4j Retry를 기대하는 독자가 100% 오해하는 지점.

타임아웃 (원문) [S32]:
> "HTTPX is careful to enforce timeouts everywhere by default. **The default behavior is to raise a `TimeoutException` after 5 seconds of network inactivity.**"
> "There are four different types of timeouts that may occur. These are **connect, read, write, and pool** timeouts."

커넥션 풀 기본값 (원문) [S33]:
> "`max_keepalive_connections`, number of allowable keep-alive connections… (**Defaults 20**)"
> "`max_connections`, maximum number of allowable connections… (**Default 100**)"
> "`keepalive_expiry`, time limit on idle keep-alive connections in seconds… (**Default 5**)"

**서킷 브레이커 — 정직한 결론:** Python/asyncio에는 Resilience4j에 대응하는 표준이 없다. 유지보수 상태 실사(PyPI, 2026-07-25 조회):

| 라이브러리 | 최신 | 릴리스일 | 비고 |
|---|---|---|---|
| pybreaker | 1.4.1 | 2025-09-21 | 가장 활발. 단 async 지원이 **Tornado 코루틴 기준**으로 문서화됨 |
| circuitbreaker | 2.1.3 | 2025-03-31 | |
| aiobreaker | 1.2.0 | **2021-05-17** | 5년 정체 |
| purgatory-circuitbreaker | 0.7.2 | **2022-01-18** | 4년 정체 |

pybreaker README 기능 목록 원문: "Thread-safe / Optional redis backing / **Optional support for asynchronous Tornado calls**" [S34]. → asyncio 네이티브라는 근거는 못 찾았다(§7).

`tenacity` 9.1.4 / 2026-02-07 — httpx 공식 문서가 직접 지목한 보완재 [S31].

### 1-J. REST 관례 — RFC 9457, 페이지네이션, 버저닝 [S35][S36]

**RFC 9457 (2023-07 발행, RFC 7807을 obsolete)** [S35]. 헤더 원문:
```
Request for Comments: 9457
Obsoletes: 7807
Category: Standards Track                                       July 2023
```
> "This document defines a "problem detail" to carry machine-readable details of errors in HTTP response content… **This document obsoletes RFC 7807.**"

**⚠️ 통념 교정: "필수(required) 멤버"는 존재하지 않는다.** §3.1 원문 [S35]:
> "**Problem detail objects can have the following members.** If a member's value type does not match the specified type, the member MUST be ignored…"

즉 `type`/`status`/`title`/`detail`/`instance` 전부 **선택적**이다. 핵심 규정 [S35]:
- `type`: "**When this member is not present, its value is assumed to be `"about:blank"`.**"
- `status`: "The "status" member, **if present, is only advisory**… **Generators MUST use the same status code in the actual HTTP response**"
- `title`: "**It SHOULD NOT change from occurrence to occurrence of the problem, except for localization.**"
- `detail`: "**ought to focus on helping the client correct the problem, rather than giving debugging information.** Consumers SHOULD NOT parse the "detail" member for information."

미디어 타입: **`application/problem+json`** 및 `application/problem+xml` [S35].

**FastAPI에 RFC 9457 내장 지원은 없다.** 기본 오류 바디는 `{"detail": ...}` + `application/json`이다 [S36]. 예외 핸들러 교체가 정공법. 서드파티는 `fastapi-problem` 0.12.1 / 2026-02-10 (§6-8).

**페이지네이션·버저닝 — 공식 가이드가 없다:**
- FastAPI 공식 문서에 페이지네이션 전용 페이지, API 버저닝 가이드가 **둘 다 없다** (사이트맵 확인).
- `fastapi-pagination` 0.15.15 / 2026-06-16 — "cursor-based pagination and page-based pagination" 지원, SQLAlchemy·PyMongo 등 연동 [S37]
- ⚠️ `fastapi-versioning`은 **0.10.0 / 2021-08-24**로 5년 정체 — **책에서 권하지 말 것.**
- 프레임워크가 실제로 주는 수단은 `APIRouter(prefix=...)` + `include_router()`, 그리고 `app.mount()` 서브앱 분리뿐이다.

## 2. 데이터 계층

### 2-A. SQLAlchemy 2.x 모던 스타일 — 그리고 2.1은 아직 베타다 [S38][S39]

**현재 안정판은 2.0.51(2026-06-15)이고, 2.1은 `2.1.0b3`(2026-06-27) 베타다.** `https://docs.sqlalchemy.org/en/21/` 사이드바가 `Release: 2.1.0b3 / beta release / Release Date: June 27, 2026`으로 표기하며, sqlalchemy.org 네비게이션도 `Current Documentation (version 2.0)` / `Version 2.1 (beta)`로 채널을 구분한다 [S39]. → **2.1을 프로덕션 권장으로 쓰면 안 된다.** (2.1 프리릴리스 이력: b1 2026-01-21 / b2 2026-04-16 / b3 2026-06-27)

공식 Quickstart 코드 (문서 원문 그대로) [S38]:
```python
from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
```
> "**Changed in version 2.0:** The ORM Quickstart is updated for the latest PEP 484-aware features using new constructs including `mapped_column()`." [S38]
> "The datatype of each column is taken first from the Python datatype that's associated with each `Mapped` annotation… **Nullability derives from whether or not the `Optional[]` (or its equivalent) type modifier is used.**" [S38]

→ **JPA 대비 결정적 차이:** nullable이 `@Column(nullable=false)`가 아니라 **타입 어노테이션의 `Optional[]` 유무**에서 파생된다.

**레거시로 강등된 것들 — 1차 소스로 확정** [S40]:
> "The `Query` object (as well as the `BakedQuery` and `ShardedQuery` extensions) **become long term legacy objects**, replaced by the direct usage of the `select()` construct in conjunction with the `Session.execute()` method."
> 문서가 직접 "becomes legacy use case"로 주석 단 코드: `session.query(User).filter_by(name="x").one()`, `.first()`, `session.query(User).get(5)`
> 문자열 기반 형태는 제거: "The string forms will all be removed in 2.0: `q = session.query(User).join("addresses")` / `q = session.query(User).options(joinedload("addresses"))`"
> `session.query(User).count()` → `session.scalar(select(func.count()).select_from(User))`

`declarative_base()`도 강등 [S41]:
> "**Changed in version 2.0:** Note that the `declarative_base()` function is **superseded by** the new `DeclarativeBase` class, which generates a new 'base' class using subclassing, rather than return value of a function. **This allows an approach that is compatible with PEP 484 typing tools.**"

**`execute()` vs `scalars()` vs `scalar()`** [S42]:
> "When selecting a list of single-element rows containing ORM entities, it is typical to skip the generation of `Row` objects and instead receive ORM entities directly. This is most easily achieved by using the `Session.scalars()` method to execute, rather than the `Session.execute()` method."
> "Calling the `Session.scalars()` method is the equivalent to calling upon `Session.execute()` to receive a `Result` object, then calling upon `Result.scalars()`…"

→ 즉 `session.execute(select(User))`는 `Row` 튜플을, `session.scalars(select(User))`는 `User` 엔티티를 준다. 초보자가 가장 많이 헤매는 지점.

### 2-B. 비동기 ORM — greenlet과 `MissingGreenlet` [S43][S44]

**greenlet 의존성** [S43]:
> "The asyncio extension requires Python 3 only. **It also depends upon the greenlet library.** This dependency is installed by default on common machine platforms including: x86_64 aarch64 ppc64le amd64 win32"
> "For other platforms, greenlet does not install by default… Note that there are many architectures omitted, **including Apple M1**."
> "`pip install sqlalchemy[asyncio]`"

**`MissingGreenlet` 공식 정의 (원문)** [S44]:
> "A call to the async DBAPI was initiated outside the greenlet spawn context usually setup by the SQLAlchemy AsyncIO proxy classes. Usually this error happens when **an IO was attempted in an unexpected place**, using a calling pattern that does not directly provide for use of the `await` keyword. **When using the ORM this is nearly always due to the use of lazy loading**, which is not directly supported under asyncio…"

**동시성 경고 (원문)** [S43]:
> "**Warning:** A single instance of `AsyncSession` is not safe for use in multiple, concurrent tasks."
> "Using concurrent tasks with asyncio, with APIs such as `asyncio.gather()` for example, should use a separate `AsyncSession` per individual task."

**처방 4종 (전부 공식 문서)** [S43]:
1. **`selectinload`** — "The most useful eager loading strategy is the `selectinload()` eager loader": `select(A).options(selectinload(A.bs))`. 또는 `lazy="raise"`로 기본 차단.
2. **`AsyncAttrs` / `awaitable_attrs`** (2.0.13 추가) — `for b1 in await a1.awaitable_attrs.bs:`
3. **`expire_on_commit=False`** — "Expiration should generally **not** be needed as `Session.expire_on_commit` should normally be set to `False` when using asyncio."
4. **`run_sync`** — 문서가 스스로 "Deep Alchemy"로 표시하고 이렇게 인정한다: "**the approach can probably be considered 'controversial'** as it works against some of the central philosophies of the asyncio programming model"

기타 주의 [S43]: `AsyncSession.refresh(obj, ["bs"])`로 강제 로딩(2.0.4+); `'dynamic'` 로더는 "**not compatible by default** with the asyncio approach" → write-only 권장; 엔진 정리 시 `await engine.dispose()` 안 하면 "`RuntimeError: Event loop is closed`" 경고 가능.

### 2-C. 드라이버와 dialect URL [S45][S46]

SQLAlchemy 2.0 dialect 문서에서 확인한 연결 문자열 [S45]:
```
postgresql+asyncpg://user:password@host:port/dbname
postgresql+psycopg://user:password@host:port/dbname       # psycopg3, sync/async 겸용
postgresql+psycopg_async://...                            # async 명시
postgresql+psycopg2://...                                 # postgresql:// 의 기본
sqlite+aiosqlite:///myfile.db
mysql+asyncmy://... / mysql+aiomysql://...
```
> asyncpg: "The asyncpg dialect is **SQLAlchemy's first Python asyncio dialect.**" [S45]
> **psycopg3의 이중성:** "The SQLAlchemy psycopg dialect provides **both a sync and an async implementation under the same dialect name.** The proper version is selected depending on how the engine is created" [S45]
> asyncpg 함정: "By default asyncpg does not decode the `json` and `jsonb` types and returns them as strings." [S45]

asyncpg 지원 범위 (README 원문) [S46]:
> "asyncpg **requires Python 3.9 or later** and is supported for **PostgreSQL versions 9.5 to 18**."
> "In our testing asyncpg is, on average, **5x** faster than psycopg3."

⚠️ **이 "5x"는 같은 README가 "obtained … in June 2023"이라고 명시한 자체 벤치마크다.** 2026년 책에 옮긴다면 반드시 **"asyncpg 자체 측정, 2023년 6월 기준"**을 병기할 것. 조건 없이 인용 금지.

**aiomysql vs asyncmy — "하나는 죽었다"는 서술은 근거가 없다.** aiomysql 0.3.2(2025-10-22), asyncmy 0.2.11(2026-01-15) 둘 다 최근 1년 내 릴리스가 있고, SQLAlchemy 2.0 dialect 문서가 **양쪽 모두 현재형으로** 문서화하며 어느 쪽에도 deprecation 표기가 없다 [S45]. 성능 비교 수치도 1차 소스에서 확인되지 않았다(§7). → 책에서 우열을 단정하지 말 것.

### 2-D. 커넥션 풀 기본값 [S47]

시그니처에서 직접 확인한 기본값 (SQLAlchemy 2.0.51 기준) [S47]:

| 파라미터 | 기본값 | 문서 설명 (원문 발췌) |
|---|---|---|
| `pool_size` | **5** | "**Note that the pool begins with no connections**; once this number of connections is requested, that number of connections will remain." |
| `max_overflow` | **10** | "**the total number of simultaneous connections the pool will allow is `pool_size` + `max_overflow`**" |
| `pool_timeout` | **30.0** | "The number of seconds to wait before giving up on returning a connection." |
| `pool_recycle` | **-1 (비활성)** | "number of seconds between connection recycling, which means upon checkout, if this timeout is surpassed the connection will be closed and replaced" |
| `pool_pre_ping` | **False** | "the pool will emit a 'ping' (typically 'SELECT 1', but is dialect-specific) on the connection upon checkout, to test if the connection is alive" |

> "All SQLAlchemy pool implementations have in common that **none of them 'pre create' connections**" [S47]

→ Spring/HikariCP의 `minimumIdle` 프리워밍에 익숙한 독자에게 중요한 차이. 또 **최대 동시 커넥션 = 5+10 = 15**가 기본이라는 점은 워커 수와 곱해져야 하므로(§5) DB `max_connections` 산정에 직결된다.

**`pool_pre_ping`의 한계 (원문, 매우 중요)** [S47]:
> "The approach **adds a small bit of overhead**… however is otherwise the most simple and reliable approach"
> "In the uncommon situation that the database is available for connections, but is not able to respond to a 'ping', the 'pre_ping' will try **up to three times** before giving up"
> "**It is critical to note that the pre-ping approach does not accommodate for connections dropped in the middle of transactions or other SQL operations.** If the database becomes unavailable while a transaction is in progress, the transaction will be lost and the database error will be raised."

`pool_recycle` [S47]:
> "**appropriate for database backends such as MySQL that automatically close connections that have been stale after a particular period of time**"
> "**Note that the invalidation only occurs during checkout - not on any connections that are held in a checked out state.**"

**비동기 엔진의 풀 클래스 (원문)** [S47]:
> "The `QueuePool` class **is not compatible with asyncio**. When using `create_async_engine`… the **`AsyncAdaptedQueuePool`** class, which makes use of an asyncio-compatible queue implementation, is used instead."

### 2-E. 요청 스코프 세션 — 그리고 공식 튜토리얼의 반전 [S48][S49]

**FastAPI 공식 SQL 튜토리얼은 SQLModel을 쓴다** (원문) [S48]:
> "FastAPI doesn't require you to use a SQL (relational) database… **Here we'll see an example using SQLModel.**"
> "**Tip:** You could use any other SQL or NoSQL database library you want… FastAPI doesn't force you to use anything. 😎"

의존성 패턴 (문서 원문) [S48]:
```python
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```
> "You would have **one single engine object** for all your code to connect to the same database." [S48]

**🔴 이 책의 최고 훅 중 하나 — 공식 튜토리얼은 전부 동기(sync)다.** `create_engine`, `with Session(engine)`, `def`(not `async def`) 라우트. 즉 §2-B의 `AsyncSession`·greenlet·`MissingGreenlet` 문제는 **공식 튜토리얼만 따라가는 독자에게는 아예 등장하지 않는다.** "FastAPI = async"라고 믿고 온 Spring Boot 개발자가 공식 문서에서 동기 세션을 만나는 지점이다. (FastAPI 사이트맵상 SQL 관련 페이지는 `/tutorial/sql-databases/`, `/how-to/testing-database/`, `/async/`, `/advanced/async-tests/` 4개뿐이고 **비동기 SQL 전용 튜토리얼은 없다.**)

**세션 전역 공유 금지의 권위 있는 근거 (원문)** [S49]:
> "The `Session` is a mutable, stateful object that represents a single database transaction. **An instance of `Session` therefore cannot be shared among concurrent threads or asyncio tasks without careful synchronization.**"
> "When using the `AsyncSession`… this object is **only a thin proxy on top of a `Session`**, and the same rules apply"
> "**The concurrency model for SQLAlchemy's `Session` and `AsyncSession` is therefore `Session` per thread, `AsyncSession` per task.**"
> `async_scoped_session`에 대해: "**however is more challenging to configure as it requires a custom 'context' function.**"

> ℹ️ 참고: 이 공식 튜토리얼 예제는 아직 `@app.on_event("startup")`을 쓴다 [S48]. **`on_event`는 FastAPI 자체적으로 deprecated 상태다** — FastAPI 소스 `applications.py`의 `on_event` docstring 원문: "on_event is deprecated, use lifespan event handlers instead." [S7]. lifespan 문서도 못 박는다: "**If you provide a `lifespan` parameter, `startup` and `shutdown` event handlers will no longer be called. It's all `lifespan` or all `events`, not both.**" [S50]

### 2-F. Alembic 비동기 [S51][S52]

`alembic list_templates` 출력 (문서 원문) [S51]:
```
generic - Generic single-database configuration.
pyproject - pep-621 compliant configuration that includes pyproject.toml
async - Generic single-database configuration with an async dbapi.
multidb - Rudimentary multi-database configuration.
```
> "**Changed in version 1.16.0:** A new `pyproject` template has been added." [S51]

> "**Alembic currently does not provide an async api directly, but it can use an use SQLAlchemy Async engine to run the migration and autogenerate.**" [S52]
> "New configurations can use the template **'async' or 'pyproject_async'**": `alembic init -t async <script_directory_here>` [S52]

`env.py` 핵심 구조 (문서 원문) [S52]:
```python
async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())
```
→ 마이그레이션 본체 `do_run_migrations`는 **동기 함수**이고 `run_sync`가 greenlet 브리지 역할을 한다. `poolclass=NullPool` 사용이 포인트.

**autogenerate가 감지하지 못하는 것 (원문 전체)** [S53]:
> "It is critical to note that **autogenerate is not intended to be perfect. It is always necessary to manually review and correct the candidate migrations that autogenerate produces.**"

*감지 못 함:*
> - "**Changes of table name.** These will come out as an add/drop of two different tables, and should be hand-edited into a name change instead."
> - "**Changes of column name.** Like table name changes, these are detected as a column add/drop pair, which is not at all the same as a name change."
> - "**Anonymously named constraints.** Give your constraints a name, e.g. `UniqueConstraint('col1', 'col2', name="my_name")`."
> - "**Special SQLAlchemy types such as `Enum`** when generated on a backend which doesn't support ENUM directly"

*아직 못 하지만 언젠가:* "PRIMARY KEY, EXCLUDE, CHECK" 제약 추가/삭제, "**Sequence additions, removals** - not yet implemented."

*옵션으로 켜야 감지:* 컬럼 타입 변경(`compare_type`, 기본 True), 서버 default 변경(`compare_server_default`, **기본 off** — "The feature is off by default so that it can be tested on the target schema first.")

→ **rename이 add+drop으로 나온다 = 데이터 손실 위험.** Flyway/Liquibase에 익숙한 독자에게 반드시 경고할 함정.

### 2-G. N+1과 로더 전략 [S54]

문서가 N+1을 직접 명명한다 (원문) [S54]:
> "The `lazyload()` strategy produces an effect that is one of the most common issues referred to in object relational mapping; **the N plus one problem, which states that for any N objects loaded, accessing their lazy-loaded attributes means there will be N+1 SELECT statements emitted.**"
> "**Lazy loading is the default loading style** for all `relationship()` constructs"

**어느 것을 언제 쓰나 (원문 — 가장 인용가치 높음)** [S54]:
> "**One to Many / Many to Many Collection - The `selectinload()` is generally the best loading strategy to use.** It emits an additional SELECT that uses as few tables as possible, leaving the original statement unaffected… Its only major limitation is when using a table with composite primary keys on a backend that does not support 'tuple IN', which currently includes SQL Server and very old SQLite versions"
> "**Many to One - The `joinedload()` strategy is the most general purpose strategy.**"

**`raiseload` = JPA `LazyInitializationException`의 의도적 대응물** [S54]:
```python
stmt = select(User).options(raiseload(User.addresses))
stmt = select(Order).options(joinedload(Order.items), raiseload("*"))  # 와일드카드
```
> "if some code later on attempts to access this attribute, an ORM exception is raised."
> "**Tip:** The 'raiseload' strategies **do not apply within the unit of work flush process.** That means if the `Session.flush()` process needs to load a collection in order to finish its work, **it will do so while bypassing any `raiseload()` directives.**"

`'dynamic'` 로더는 레거시: "**Dynamic loaders are superseded by 'write only' collections**" [S54]

### 2-H. SQLModel의 현재 위치 — 사실만 [S55]

- 버전 **0.0.39 / 2026-06-25**. **여전히 `0.0.x` 대역이다** (§6-3).
- 저장소 `fastapi/sqlmodel`: `archived=false`, 마지막 push 2026-07-23, stars 18,218 — **활발히 유지보수 중** (GitHub API, 2026-07-25) [S55].
- 자기 소개 (원문) [S55]: "**SQLModel is, in fact, a thin layer on top of Pydantic and SQLAlchemy, carefully designed to be compatible with both.**"
- FastAPI 공식 튜토리얼이 **채택하되 강제하지 않는다** [S48].

⚠️ **정직한 서술 규칙:** 홈페이지·README에서 "early development / beta / not production ready" 문구는 **발견되지 않았다**(2026-07-25 확인). 그러나 이건 *부재의 확인*이지 *프로덕션 레디 선언*이 아니다. → **"버전이 0.0.x다"라는 사실만 제시하고, "공식적으로 프로덕션 레디로 선언됐다"고 쓰지 말 것.**

관용구 차이 (소스 확인) [S55]: SQLModel은 `session.exec()`를 쓰며, `session.execute()`에는 deprecation 데코레이터가 붙어 있다. 원문:
> "🚨 You probably want to use `session.exec()` instead of `session.execute()`. This is the original SQLAlchemy `session.execute()` method that returns objects of type `Row`, and that you have to call `scalars()` to get the model objects."

→ §2-A의 `execute`/`scalars` 구도와 정확히 대응한다. 비동기용 `sqlmodel/ext/asyncio/session.py`에 `AsyncSession`이 존재한다 [S55].

### 2-I. Redis — `aioredis`는 흡수됐다 [S56][S57]

- redis-py **8.0.1 / 2026-06-23**. import는 **`import redis.asyncio as redis`** [S56]
- "**All commands are coroutine functions.**" [S56]
- 명시적 종료 필요 (원문) [S56]:
  > "Using asyncio Redis requires an explicit disconnect of the connection since there is no asyncio deconstructor magic method. **By default, an internal connection pool is created on `redis.Redis()` and attached to the `Redis` instance.**"
- 풀 소유권 3패턴 [S56]: 단독 소유는 `redis.Redis.from_pool(pool)`, 공유는 `redis.Redis(connection_pool=pool)` 후 `await pool.aclose()`
- **RESP3 전환 (원문)** [S56]:
  > "**Starting with redis-py 8.0, clients use RESP3 on the wire by default** while keeping legacy RESP2-compatible Python response shapes."

**`aioredis`는 별도 패키지로 쓰면 안 된다 — 1차 소스 3중 확인** [S57]:
1. 저장소가 `aio-libs/aioredis-py` → **`aio-libs-abandoned/aioredis-py`**로 이관되고 `archived: true` (GitHub API)
2. README 최상단 공지 (원문): "**📢🚨 Aioredis is now in redis-py 4.2.0rc1+ 🚨🚨** … To install, just do `pip install redis>=4.2.0rc1`… `from redis import asyncio as aioredis` … This way you don't have to change all your code, just the imports."
3. PyPI 마지막 릴리스 **2.0.1 / 2021-12-27** — 4년 7개월 정체

### 2-J. 🔴 MongoDB — Motor는 EOL을 지났다 [S58][S59]

**MongoDB가 현재 공식 권장하는 async 드라이버는 `PyMongo Async API`다.** 공식 마이그레이션 문서 원문 [S58]:
> "The PyMongo Async API is a **unification** of PyMongo and the Motor library."
> "**The PyMongo Async API is designed to be a replacement for the Motor library.** Motor was created to provide support for Tornado, with asyncio support added later. Because of this, Motor provides full asyncio and Tornado support, but **still relies on a thread pool to perform network operations**. In some cases, this might lead to performance degradation…"
> FastAPI를 콕 집는다: "Consider migrating to the PyMongo Async API if… **Your application relies on other asynchronous libraries or frameworks, such as FastAPI**"

임포트 변경 (문서 원문) [S58]:
```python
# Motor
from motor.motor_asyncio import AsyncIOMotorClient
# PyMongo Async
from pymongo import AsyncMongoClient
```
주요 시그니처 차이 [S58]: `io_loop` 파라미터 없음 / `AsyncCursor.each()` 없음 / `to_list(0)` 대신 `to_list(None)` / "**`MongoClient` is thread safe… however, an `AsyncMongoClient` is not thread safe and should only be used by a single event loop.**"

**Motor deprecation 타임라인 (Motor README 원문)** [S59]:
> "As of **May 14th, 2025**, Motor is deprecated in favor of the GA release of the PyMongo Async API.
> No new features will be added to Motor, and only bug fixes will be provided until it reaches **end of life on May 14th, 2026**.
> After that, only critical bug fixes will be made until **final support ends on May 14th, 2027**."

→ **오늘(2026-07-25) 기준 EOL(2026-05-14)이 이미 지났다.** motor 최신 릴리스가 3.7.1 / **2025-05-14**(deprecation 공지와 같은 날)로 14개월째 멈춰 있는 것과 일치한다(§6-3).

⚠️ 문서 간 시제 불일치: MongoDB 공식 문서 쪽에는 "**Motor will be deprecated on May 14th, 2026**"라는 **미래형** 문장이 남아 있다 [S58]. README 타임라인을 기준으로 쓰되 이 불일치를 각주로 남기는 게 정확하다.

**Beanie ODM은 이미 Motor를 떠났다 (3중 확인)** [S60]: PyPI `requires_dist`에 `motor` 없고 `pymongo>=4.11.0,<5.0.0` 있음 / README·공식 문서 예제가 `from pymongo import AsyncMongoClient` + "Beanie uses PyMongo async client under the hood". 버전 2.1.0 / 2026-03-26.

→ **책 서술 권고:** MongoDB 챕터는 `pymongo.AsyncMongoClient`를 기본으로, ODM이 필요하면 Beanie 2.x. **웹의 FastAPI+Motor 튜토리얼 대다수가 2026년 기준 구식**임을 명시할 가치가 크다.

## 3. 프로덕션 관심사

### 3-A. 구조적 로깅 — uvicorn 로거와의 충돌, 실제 원인 [S14]

"uvicorn이 내 로깅 설정을 죽인다"는 통념의 **진짜 원인**을 공식 문서의 기본 `LOGGING_CONFIG`로 확인했다.

Uvicorn이 제공하는 로거는 3개다 [S14]:

| Logger name | Purpose |
|---|---|
| `uvicorn` | Parent logger (rarely used directly) |
| `uvicorn.error` | Server-level messages (startup, shutdown, errors) |
| `uvicorn.access` | Per-request access log lines |

> "Despite its name, `uvicorn.error` is **not** limited to error messages. It is the general-purpose server logger, similar to how Gunicorn names its main logger." [S14]

기본 `LOGGING_CONFIG`의 결정적 두 줄 (공식 문서에서 그대로) [S14]:
```python
"disable_existing_loggers": False,
...
"loggers": {
    "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
    "uvicorn.error": {"level": "INFO"},
    "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
},
```

**여기서 통념 교정이 두 개 나온다:**
1. `disable_existing_loggers`는 **`False`가 기본값이다.** "uvicorn이 기존 로거를 비활성화한다"는 흔한 설명은 현재 기본 설정 기준으로 **틀렸다.**
2. 진짜 원인은 **`propagate: False`**다. `uvicorn`과 `uvicorn.access`가 루트로 전파하지 않으므로, 루트에 structlog·JSON 핸들러를 붙여도 **접근 로그만 여전히 uvicorn 자체 포맷으로 나간다.** → JSON 로그 통일을 원하면 이 두 로거의 `handlers`/`propagate`를 직접 덮어써야 한다.

핸들러 스트림도 갈린다 [S14]: `default`는 **stderr**, `access`는 **stdout**. 컨테이너 로그 수집 파이프라인 설계 시 중요.

표준 포매터로 갈아탈 때의 함정 (원문 경고) [S14]:
> "When using a standard `logging.Formatter` for the access logger, the `%(client_addr)s`, `%(request_line)s`, and `%(status_code)s` placeholders are **not** available. The access log line will be formatted using only the standard `%(message)s` field."

`--log-config`는 `.json`/`.yaml`은 `dictConfig()`, 그 외는 `fileConfig()`로 처리된다. YAML을 쓰려면 PyYAML 또는 `uvicorn[standard]`가 필요하다 [S10][S14].

### 3-B. contextvars — correlation ID 전파의 알려진 함정 [S10]

Uvicorn 0.51.0/2026-07 기준 설정 목록에 다음 플래그가 있다 (원문) [S10]:

> `--reset-contextvars` - Run each ASGI request in a fresh `contextvars.Context`. Workaround for a [context leak in asyncio](https://github.com/python/cpython/issues/140947); only relevant when using the `asyncio` event loop (uvloop is not affected). Enabling this hides any context set in the lifespan or by external instrumentation from ASGI handlers. **Default:** *False*.

→ 요청 ID·correlation ID를 `contextvars`로 전파하는 장에서 반드시 다룰 것. **CPython 이슈 #140947**이라는 1차 근거가 있고, "uvloop는 영향 없음", "켜면 lifespan/외부 계측이 심어둔 컨텍스트가 핸들러에서 안 보인다"는 트레이드오프까지 문서에 명시돼 있다. 기본값은 `False`.

### 3-C. 동시성 제한과 backlog — 흔한 오해 정면 반박 [S12]

Uvicorn 문서가 **"흔한 오해(common misconception)"라고 명시적으로 못 박은** 대목이다. 부하 대응 설계 장의 핵심 재료.

> "`--limit-concurrency` and `--backlog` operate at different layers and do not interact. It is a common misconception that requests refused by `--limit-concurrency` are held in the `--backlog`; they are not." [S12]

- **`--limit-concurrency`는 애플리케이션 레벨 게이트다.** 한도 도달 시 **즉시 503**을 반환하며 **큐에 넣지 않는다** [S12]
  > "the request is **not** queued and does **not** wait for a slot to free up."
  - 카운트에 현재 요청의 연결도 포함되므로 `N`은 실제로 **다른 동시 요청 `N-1`개**만 허용하고, **`1`이면 모든 요청을 거부한다** [S12]
  - **idle keep-alive 연결도 예산을 소비한다** [S12] — 실무에서 놓치기 쉬운 지점
  - 기본값 `None` [S12]
- **`--backlog`은 OS 레벨 소켓 설정**으로 `listen()`에 그대로 전달된다. 기본값 **2048** [S12]
  - 큐가 차면 커널이 연결 수락을 멈추고, 클라이언트는 503이 아니라 **연결 실패/타임아웃**을 본다 [S12]
- 초과 부하를 **큐잉하고 싶다면** 문서의 처방은 명확하다 [S12]:
  > "To instead *queue* excess load, put a reverse proxy (e.g. nginx) in front of Uvicorn, or scale out with more workers."

### 3-D. 타임아웃·리소스 기본값 (Uvicorn 0.51.0 / 2026-07 기준) [S10][S12]

| 설정 | 기본값 | 비고 |
|---|---|---|
| `--timeout-keep-alive` | **5초** | 요청 간 새 데이터 없으면 연결 종료 [S12] |
| `--timeout-graceful-shutdown` | (미설정) | "After this timeout, the server will start terminating requests." [S10] |
| `--timeout-worker-healthcheck` | **5초** | 워커 헬스체크 응답 대기 [S10] |
| `--backlog` | **2048** | [S10][S12] |
| `--limit-concurrency` | `None` | 초과 시 503 [S12] |
| `--limit-max-requests` | `None` | 메모리 누수 완화용 프로세스 재시작 [S12] |
| `--limit-max-requests-jitter` | **0** | 워커 동시 재시작 방지용 지터 [S10] |
| `--h11-max-incomplete-event-size` | **16384 (16KB)** | h11 전용 [S10] |
| `--workers` | `$WEB_CONCURRENCY` 또는 **1** | `--reload`와 **상호 배타** [S10] |
| `--loop` / `--http` | `auto` | uvloop/httptools 자동 선택 [S10] |

**Graceful shutdown 시 서버가 보장하는 것** (원문) [S12]:
> "Close any connections that are not currently waiting on an HTTP response, and wait for any other connections to finalize their HTTP responses."
> "Wait for any background tasks to run to completion, such as occurs when the ASGI application has sent the HTTP response, but the asyncio task has not yet run to completion."

→ **`BackgroundTasks`가 graceful shutdown에서 어떻게 취급되는지**에 대한 1차 근거다. 서버는 기다려 주지만, K8s의 `terminationGracePeriodSeconds` 안에 끝나야 한다는 점과 묶어서 서술할 것 (§5).

### 3-E. structlog × FastAPI — 공식 문서가 경고하는 함정 [S61]

§3-B의 `--reset-contextvars`와 함께 읽어야 할, **structlog 공식 문서의 FastAPI 직접 언급**이다 (원문) [S61]:
> "Since the storage mechanics of your context variables is different for each concurrency method, they are _isolated_ from each other.
> This can be a problem in hybrid applications like those based on [Starlette](https://www.starlette.io) (this **includes FastAPI**) where **context variables set in a synchronous context don't appear in logs from an async context and vice versa.**"

→ **`def` 라우트(스레드풀 실행)와 `async def` 라우트가 섞인 앱에서 correlation ID가 유실될 수 있다.** FastAPI의 "def면 스레드풀" 규칙이 로깅 컨텍스트를 깨뜨리는 지점이며, 이 책에서 반드시 다뤄야 할 함정이다. structlog 사용 흐름 [S61]: 첫 프로세서로 `merge_contextvars`, 요청 시작 시 `clear_contextvars()`, 이후 `bind_contextvars()`/`unbind_contextvars()`.

⚠️ structlog 공식 문서의 `frameworks.md`에는 **FastAPI/Starlette 전용 가이드가 없다**(Litestar는 있음). structlog 26.1.0 / 2026-06-06.

`asgi-correlation-id` 5.0.1 / 2026-06-09 (MIT) — 기본 헤더 `X-Request-ID`, 없으면 생성 [S62]:
```python
from asgi_correlation_id import CorrelationIdMiddleware
app.add_middleware(CorrelationIdMiddleware)
```
로깅 필터로 연결: `'()': 'asgi_correlation_id.CorrelationIdFilter'` [S62].

`loguru` 0.7.3 / **2024-12-06** — 1년 7개월 이상 신규 릴리스 없음. ⚠️ 저장소 커밋 활동은 미확인이므로 "방치됐다"고 쓰지 말 것(§7).

### 3-F. 인증 — 공식 문서가 실제로 쓰는 라이브러리 (직접 확인) [S1]

**2026-07-25 시점 `https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/` 원문에서 그대로 옮김** (본 문서 작성자가 직접 fetch했고, 별도 에이전트가 GitHub raw 원문 `docs/en/docs/tutorial/security/oauth2-jwt.md`로 재확인했다 [S63]):

설치 (문서가 `uv add`를 쓴다는 점도 그대로):
```
$ uv add pyjwt
$ uv add "pwdlib[argon2]"
```

JWT 임포트:
```python
import jwt
from jwt.exceptions import InvalidTokenError
```

비밀번호 해싱 — **passlib의 `CryptContext`가 아니라 `pwdlib`**:
```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")
```

토큰 발급/검증:
```python
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

문서 산문 (raw 원문) [S63]:
> "We need to install `PyJWT` to generate and verify the JWT tokens in Python."
> "If you are planning to use digital signature algorithms like RSA or ECDSA, you should install the cryptography library dependency `pyjwt[crypto]`."
> "pwdlib is a great Python package to handle password hashes… **The recommended algorithm is "Argon2".**"
> (tip) "pwdlib also supports the bcrypt hashing algorithm but does not include legacy algorithms - **for working with outdated hashes, it is recommended to use the passlib library.**"

**타이밍 공격 방어가 공식 예제에 들어왔다** — `DUMMY_HASH`의 정체 (문서 원문) [S63]:
> "When `authenticate_user` is called with a username that doesn't exist in the database, we still run `verify_password` against a dummy hash. This ensures the endpoint takes roughly the same amount of time to respond whether the username is valid or not, **preventing timing attacks that could be used to enumerate existing usernames.**"

실제 코드 (`docs_src/security/tutorial004_an_py310.py` raw) [S63]:
```python
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
```

**저술 시 강조점 3가지:**
1. 시중 한국어 자료 대부분이 `python-jose` + `passlib[bcrypt]`다. 이건 **현재 공식 문서와 다르다.**
2. `[argon2]` extra + "The recommended algorithm is Argon2" → bcrypt가 아니라 **Argon2**가 공식 권장 방향.
3. `DUMMY_HASH`는 실무 디테일로 인용 가치가 매우 높다.

### 3-G. passlib 논란 — **두 개의 다른 사건을 구분하라** [S64][S65][S66]

"passlib이 깨졌다"는 이야기는 실재하지만, **뭉뚱그리면 사실 오류가 된다.**

**검증된 사실:** passlib 최신 릴리스는 **1.7.4 / 2020-10-08** — 약 5년 9개월간 새 릴리스 없음 (§6-5).

**pwdlib README의 서술 (원문)** [S64]:
> "For years, the de-facto standard to hash passwords was `passlib`. Unfortunately, **it has not been very active recently and its maintenance status is under question**. **Starting Python 3.13, `passlib` won't work anymore.**"
> "That's why I decided to start `pwdlib`… However, it's **not designed to be a complete replacement** for `passlib`"

**사건 A — bcrypt 4.1.x (2023): 로그 노이즈일 뿐, 동작은 정상** [S65]
GitHub `pyca/bcrypt#684` (2023-11-29 개설). 증상:
```
(trapped) error reading bcrypt version
AttributeError: module 'bcrypt' has no attribute '__about__'
'$2b$12$dcl0YFoHz6.pL/dtOwbfO.r3CRI416BLq6vJEf0EmT4CHsqqHm7FC'   ← 해시는 정상 생성됨
```
메인테이너 코멘트 (원문) [S65]:
> `reaperhulk`: "This is an issue with how passlib attempts to read a version (**for logging only**) and fails because it's loading modules that no longer exist in bcrypt 4.1.x."
> `alex`: "**passlib will work with latest bcrypt, it simply emits a warning.** You should be able to silence that warning with a logging configuration."

**사건 B — bcrypt 5.0.0 (2025): 실제 예외** [S66]
`pyca/bcrypt#1079` "Passlib 1.7.4 + bcrypt 5.0.0" (2025-09-26 개설):
> "ValueError: password cannot be longer than 72 bytes, truncate manually if necessary"

→ **경계선은 bcrypt 5.0.0 (2025-09-25 릴리스, §6-5).** A는 로그만 시끄럽고 동작 정상, B는 실제 고장. 책에서 이 둘을 구분해 서술하면 정확도와 신뢰도가 크게 올라간다.

⚠️ **표현 규칙:** "passlib은 유지보수가 중단됐다"는 *해석*이다. 근거로 제시할 수 있는 *사실*은 ① 마지막 릴리스 2020-10-08 ② pwdlib README의 서술 ③ 공식 문서가 pwdlib로 전환한 것 — 이 셋이다.

### 3-H. Security 스코프·세션 쿠키·외부 IdP [S67][S68][S69][S70]

**스코프** [S67] — `Security()`와 `SecurityScopes`:
```python
from fastapi import Security
from fastapi.security import SecurityScopes

async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    ...
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(status_code=401, detail="Not enough permissions", ...)

async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
```
문서 경고 원문 [S67]: "This is a more or less advanced section. If you are just starting, you can skip it. … **In many cases, OAuth2 with scopes can be an overkill.**"
→ Spring Security `@PreAuthorize("hasAuthority('SCOPE_x')")`와 대비되는 지점: **FastAPI는 스코프 검증 루프를 직접 작성한다.**

**세션 쿠키 — Starlette `SessionMiddleware`** [S68] (문서 원문):
> "Adds signed cookie-based HTTP sessions. **Session information is readable but not modifiable.** The session cookie is always set with the `"HttpOnly"` flag"

기본값 (원문) [S68]: `session_cookie` 기본 `"session"` / `max_age` 기본 **2주**(`None`이면 브라우저 세션) / `same_site` 기본 **`'lax'`** / `path` 기본 `'/'` / `https_only` 기본 **`False`** — "**Set this to `True` in production to ensure the session cookie is only sent over HTTPS.**"

**외부 IdP:**
- **Auth0 — 공식 벤더 문서·SDK 있음** [S69]. 퀵스타트 https://auth0.com/docs/quickstart/backend/fastapi , SDK `auth0-fastapi-api` **1.0.0b7 / 2026-04-09 — 아직 beta**. summary: "SDK for verifying access tokens and securing APIs with Auth0, **using Authlib**." README 주의 (원문): "When deploying behind a reverse proxy (nginx, AWS ALB, etc.), you **must** enable proxy trust for DPoP validation to work correctly" → `app.state.trust_proxy = True` (§5-C와 연결).
- **Keycloak — FastAPI/Python 공식 어댑터 없음** [S70]. 공식 어댑터 목록(Wildfly Elytron, Spring Boot, Keycloak JS, Node.js, C# OWIN, AppAuth, mod_auth_openidc 등)에 Python이 없다. 벤더 자신의 권고 (원문): "**they should be used as a last resort if you cannot rely on what is available from the application ecosystem.**" → 범용 OIDC 라이브러리(Authlib)로 붙이는 게 정공법.
- **Authlib** 1.7.2 / 2026-05-06 — FastAPI 전용 문서 페이지가 실재한다: `https://docs.authlib.org/en/latest/oauth2/client/web/fastapi.html` [S71]. 단 **리소스 서버 통합 페이지는 Flask/Django만 있고 FastAPI는 없다.** OAuth 클라이언트 흐름에는 `SessionMiddleware`가 필요하다("temporary OAuth code and state need to be stored in the session").

### 3-I. 설정 관리 — pydantic-settings [S72][S73]

**pydantic v2와 별개 패키지다** (2.14.2 / 2026-06-19, §6-1). 공식 문서: "Pydantic Settings is installed as a separate package: `pip install pydantic-settings`" [S72]

⚠️ **문서 URL이 이동했다** — `https://docs.pydantic.dev/latest/concepts/pydantic_settings/` 가 **HTTP 301**로 `https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/` 로 리다이렉트된다(2026-07-25 확인) [S72].

핵심 API [S72]:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='my_prefix_', env_file='.env',
                                      env_nested_delimiter='__')
    auth_key: str
    database_url: str = 'sqlite:///db.sqlite'
```
- **우선순위:** CLI 인자 > 초기화 kwargs > 환경변수 > dotenv > secrets 디렉터리 > 기본값 [S72]
- 중첩: `DATABASE__HOST=localhost` 형태 [S72]
- **Spring Boot 개발자에게 중요한 차이 (원문)** [S72]: "**Unlike standard Pydantic models, `BaseSettings` validates default values by default.**" (`validate_default=False`로 끔)
- 디버깅: `PYDANTIC_SETTINGS_DEBUG=1` → 각 값의 출처를 DEBUG 로그로 [S72]
- Docker secrets: `secrets_dir='/run/secrets'` [S72]

`SecretStr` (pydantic 코어) [S73]:
```python
print(user)  #> username='scolvin' password=SecretStr('**********')
print(user.password.get_secret_value())  #> password1
```

**FastAPI 공식 `lru_cache` 패턴** [S74]:
```python
from functools import lru_cache

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    ...
```
→ Spring `@ConfigurationProperties` 싱글턴 빈에 대응. 동시에 `dependency_overrides[get_settings]`로 테스트에서 교체 가능(§3-K).

### 3-J. 관측성 — OTel의 안정성 상태를 정확히 [S75][S76]

**OpenTelemetry Python 공식 상태 표 (2026-07-25 조회)** [S75]:

| Traces | Metrics | Logs |
|---|---|---|
| **Stable** | **Stable** | **Development** |

> "OpenTelemetry-Python supports Python 3.10 and higher." [S75]

**버전 체계가 갈린다 (실무 함정)** — 코어 `opentelemetry-api`/`-sdk`는 **1.44.0**(stable numbering)인데, 계측 패키지 `opentelemetry-instrumentation-fastapi`는 **0.65b0**(beta numbering)이다 (§6-6). 같은 날(2026-07-16) 릴리스되지만 번호 체계가 다르므로 핀을 걸 때 주의.

FastAPI 계측 [S76]:
```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor.instrument_app(app)
```
옵션 [S76]: `OTEL_PYTHON_FASTAPI_EXCLUDED_URLS` 환경변수 또는 `excluded_urls` 인자, `server_request_hook`.

**제로코드 자동 계측** [S77]:
```sh
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install
opentelemetry-instrument --traces_exporter console,otlp --service_name your-service-name python myapp.py
```
> `opentelemetry-instrument` "**uses monkey patching** to modify library functions at runtime" [S77]

→ Java의 `-javaagent:opentelemetry-javaagent.jar`에 대응하지만 **구현 방식이 monkey patching**이라는 점을 명시할 것.

**Prometheus — 멀티프로세스가 진짜 문제다** [S78]. `prometheus_client` 공식 문서 원문:
> "Prometheus client libraries **presume a threaded model, where metrics are shared across workers. This doesn't work so well for languages such as Python** where it's common to have processes rather than threads to handle large workloads."

멀티프로세스 모드 제약 (공식 목록) [S78]: `PROMETHEUS_MULTIPROC_DIR` 필수(재시작 전 디렉터리 비워야 함, **Python 안이 아니라 기동 셸에서** 설정해야 자식에 전파) / 커스텀 컬렉터 미지원 / Gauge의 `set_function`·`pid` 라벨 불가 / **Info·Enum 메트릭 동작 안 함** / Pushgateway 불가 / exemplar 불가.

→ **§5-A의 "워커 1개 + 오케스트레이터 레플리카" 권장과 직결된다.** 컨테이너당 1프로세스면 이 문제 자체가 사라진다. 좋은 논증 연결점.

`prometheus-fastapi-instrumentator` 8.0.2 / 2026-06-23 (ISC) — 2026년에 메이저 8.0.0이 나온 활발한 프로젝트 [S79]:
```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

### 3-K. 테스트 — 공식 문서는 `anyio`를 쓴다 (pytest-asyncio 아님) [S80][S81]

**동기 테스트** [S80]: `TestClient`(httpx 기반), 테스트 함수는 `async def`가 아니라 일반 `def`.

**비동기 테스트 — 현재 공식 코드 (raw 원문)** [S81]:
```python
import pytest
from httpx import ASGITransport, AsyncClient

from .main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```
문서 원문 [S81]:
> "If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. **AnyIO provides a neat plugin for this**"
> "The `TestClient` does some magic inside to call the asynchronous FastAPI application in your normal `def` test functions… But that magic doesn't work anymore when we're using it inside asynchronous functions. **By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions.**"
> ⚠️ (warning) "**If your application relies on lifespan events, the `AsyncClient` won't trigger these events.** To ensure they are triggered, use `LifespanManager` from florimondmanca/asgi-lifespan."
> (tip) "If you encounter a `RuntimeError: Task attached to a different loop`… remember to instantiate objects that need an event loop only within async functions"

⚠️ **`asgi-lifespan`은 2.1.0 / 2023-03-28**로 3년 넘게 릴리스가 없다(§6-8) — 공식 문서가 권하는 라이브러리의 정체 상태를 병기할 것.

⚠️ **함정:** 공식 예제 디렉터리에 `conftest.py`가 없다. AnyIO 공식 문서는 `anyio_backend` fixture로 백엔드를 지정하라고 안내한다 [S82]:
```python
@pytest.fixture
def anyio_backend():
    return 'asyncio'
```
> "The AnyIO pytest plugin comes with a function scoped fixture with this name which **runs everything on all supported backends**." [S82]

→ 공식 예제를 그대로 옮기면 asyncio·trio **양쪽으로 실행**된다. 실무에서는 `anyio_backend` fixture를 직접 정의하는 게 정석.

**pytest-asyncio를 쓴다면** (1.4.0 / 2026-05-26) [S83]:
- `asyncio_mode`: `strict`(기본) | `auto`
- `asyncio_default_fixture_loop_scope` 미설정 시 경고 발생 — "In future versions of pytest-asyncio, the value will default to `function` when unset"
- **breaking change 이력:** **1.0.0 (2025-05-26)에서 `event_loop` fixture가 제거됐다** → 인터넷의 옛 FastAPI 테스트 예제가 대량으로 깨진 지점. 1.4.0에서는 `event_loop_policy` 오버라이드도 deprecated.

**`dependency_overrides`** [S84]:
```python
app.dependency_overrides[common_parameters] = override_dependency
app.dependency_overrides = {}   # 초기화
```
→ Spring `@MockBean` / NestJS `overrideProvider()`에 대응.

**테스트 DB — 트랜잭션 롤백** [S85]. SQLAlchemy 공식 레시피 "Joining a Session into an External Transaction (such as for test suites)":
```python
self.connection = engine.connect()
self.trans = self.connection.begin()          # non-ORM 트랜잭션 시작
self.session = Session(bind=self.connection,
                       join_transaction_mode="create_savepoint")
...
self.trans.rollback()                          # commit() 호출분까지 전부 롤백
```
> "The usual rationale for this is a test suite that allows ORM code to work freely with a `Session`, **including the ability to call `Session.commit()`, where afterwards the entire database interaction is rolled back.**" [S85]

핵심 키워드는 **`join_transaction_mode="create_savepoint"`** (2.0 도입). → Spring `@Transactional` 테스트 롤백의 정확한 대응물.

⚠️ **이 페이지와 asyncio 확장 페이지 어디에도 `AsyncSession` 버전 레시피가 없다**(두 페이지 확인 기준). "async FastAPI + AsyncSession 롤백 레시피는 공식 1차 출처가 부족하다"는 것 자체가 서술 포인트다(§7).

`testcontainers` 4.15.0 / 2026-07-24 [S86]:
```python
from testcontainers.postgres import PostgresContainer
with PostgresContainer("postgres:16") as postgres:
    engine = sqlalchemy.create_engine(postgres.get_connection_url())
```
> "Version 4.0.0 onwards we do not support the testcontainers-* packages as it is unsustainable to maintain ownership." [S86]

### 3-L. 🔴 벤치마크 — FastAPI 공식 문서가 스스로 반박한다 [S87][S88][S89]

**이 절이 "FastAPI가 X배 빠르다" 주장을 다루는 정답이다.**

**FastAPI 자신의 주장 (raw 원문)** [S87]:
> "* **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic). [One of the fastest Python frameworks available](#performance)."
> "* **Fast to code**: Increase the speed to develop features by about 200% to 300%. *"
> "* **Fewer bugs**: Reduce about 40% of human (developer) induced errors. *"
> 각주: "`* estimation based on tests conducted by an internal development team, building production applications.`"

→ **"200~300%", "40%"는 문서가 스스로 "사내 팀 자체 추정(internal development team)"이라고 밝힌 값이다.** 조건 없이 인용 금지.

Performance 섹션 원문 [S87]:
> "Independent TechEmpower benchmarks show **FastAPI** applications running under Uvicorn as [one of the fastest Python frameworks available](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), only below Starlette and Uvicorn themselves (used internally by FastAPI). (*)"

🔍 **직접 검증한 사실:** 이 문장 끝의 `(*)`에 **대응하는 각주 텍스트가 페이지 어디에도 없다**(`index.md` 전문 grep 결과 `(*)`는 1회만 등장) [S87]. 그리고 링크된 필터는 `hw=ph&test=query` — **물리 하드웨어의 single query 테스트 한 종목**이다(composite도 plaintext도 아님).

**FastAPI 자신의 반박 페이지 (가장 강력한 1차 출처)** [S88]:
> "**The simpler the problem solved by the tool, the better performance it will get. And most of the benchmarks don't test the additional features provided by the tool.**"
> Uvicorn: "Will have the best performance, as it doesn't have much extra code apart from the server itself."
> Starlette: "In fact, Starlette uses Uvicorn to run. So, it probably can only get 'slower' than Uvicorn by having to execute more code."
> FastAPI: "**The same way that Starlette uses Uvicorn and cannot be faster than it, FastAPI uses Starlette, so it cannot be faster than it.**"
> "If you are comparing FastAPI, compare it against a web application framework (or set of tools) that provides data validation, serialization and documentation, like Flask-apispec, **NestJS**, Molten, etc."

→ **대상 독자가 NestJS 경험자라면 이건 선물이다.** FastAPI 공식 문서가 스스로 비교 대상으로 NestJS를 지목한다.

**TechEmpower 방법론의 명시된 한계 (공식 wiki 원문)** [S89]:
> |round| "A posting of "official" results on this web site. **This is mostly for ease of consumption by readers and good-spirited and healthy competitive bragging rights. For in-depth analysis, we encourage you to examine the source code and run the tests on your own hardware.**"
> "**It's unfair and possibly even incorrect to compare X and Y!** … one may evaluate frameworks vs platforms; MySQL vs Postgres; Go vs Python; ORM vs raw database connectivity; and any number of other possibly irrational comparisons."
> "**If you are testing production deployments, why is logging disabled?** At present, we have elected to run tests with logging features disabled. **Although this is not consistent with production deployments**…"
> "**Why doesn't your test include more substantial algorithmic work?** Great suggestion. We hope to in the future!"
> "**We are expressly not using reverse proxies on this project.**"
> 측정 절차: "Run a 5-second **primer** at 8 client-concurrency… a 15-second **warmup** at 256… a **15-second captured test** for each of the concurrency levels" — 동시성 8/16/32/64/128/256, 부하 생성기는 **Wrk**
> "**Hold on, 15 seconds is not enough to gather useful data.** This is a reasonable concern."

**결정적 인용 — 독자에게 줄 결론** [S89]:
> "**I am about to start a new web application project; how should I interpret these results?** Most importantly, recognize that **performance data should be one part of your decision-making process.** … while we have aimed to select test types that represent workloads that are common for web applications, **nothing beats conducting performance tests yourself for the specific workload of your application.**"

→ 이 문장 + 카카오페이의 "요청의 크기가 큰 경우 서버 프레임워크 성능 차이는 유의미하게 나지 않는다"[S9] + FastAPI 자신의 "cannot be faster than Starlette"[S88] 세 개를 묶으면, **성능 신화를 1차 소스만으로 해체하는 강력한 절**이 나온다.

## 4. CI/CD

### 4-A. uv가 공식 기본이 됐다 [S8][S90]

FastAPI 0.140.0(2026-07-24) 릴리스에 PR #16032 **"📝 Update docs to use uv projects by default"** 가 포함됐다 [S8]. 실제로 보안 튜토리얼[S1]·프록시 문서[S13]·설정 문서[S74]의 명령이 전부 `uv add` / `uv run`이다. **uv 0.11.32 / 2026-07-23** (§6-7).

`uv.lock`에 대한 공식 서술 [S90]:
> "a *universal* or *cross-platform* lockfile that captures the packages that would be installed across all possible Python markers"
> "This file should be checked into version control, allowing for consistent and reproducible installations across machines"
> "`uv.lock` is a human-readable TOML file but is managed by uv and should not be edited manually. **The `uv.lock` format is specific to uv and not usable by other tools**"

**🔴 여기서 이 책만 할 수 있는 이야기가 나온다 — PEP 751** [S91]:

| 항목 | 값 |
|---|---|
| PEP | 751 — "A file format to record Python dependencies for installation reproducibility" |
| Author | Brett Cannon |
| **Status** | **Final** |
| Created / Resolution | 2024-07-24 / **2025-03-31** |
| Replaces | PEP 665 |
| 표준 파일명 | **`pylock.toml`** (변형: `pylock.{name}.toml`) |

> "This PEP proposes a new file format for specifying dependencies to enable reproducible installation in a Python environment… Installers consuming the file should be able to calculate what to install **without the need for dependency resolution at install-time**." [S91]

→ **2025-03-31에 락파일 표준이 Final로 확정됐는데, 사실상 표준 도구인 uv의 기본 산출물(`uv.lock`)은 그 표준 포맷이 아니다.** Maven `pom.xml`/Gradle 락파일처럼 단일 표준에 익숙한 독자에게 반드시 설명해야 할 지점.

**`--locked` vs `--frozen` — 의미가 다르다** [S92]:
> `--frozen`: "To use the lockfile **without checking if it is up-to-date**"
> `--locked`: "If the lockfile is not up-to-date, uv will **raise an error instead of updating** the lockfile."
> `--no-dev`: "can be used to exclude the `dev` group."

⚠️ uv 문서에는 "프로덕션에선 `--frozen`을 써라"는 **명시적 권고 문장이 없다.** 실제 공식 Docker 가이드는 **`--locked`**를 쓴다(§4-C). `--frozen`은 **workspace 변형에서만** 등장하며 문서가 그 이유까지 밝힌다 [S93]:
> "uv cannot assert that the `uv.lock` file is up-to-date without each of the workspace member `pyproject.toml` files, so we use `--frozen` instead of `--locked` to skip the check during the initial sync."

> ℹ️ 참고: §5-B에 인용한 **Uvicorn**의 Dockerfile은 `uv sync --frozen`을 쓴다[S15]. **uv 자신의 가이드는 `--locked`**다[S93]. 두 공식 문서가 다른 플래그를 쓰고 있다는 사실 자체를 정확히 서술할 것.

**Poetry(2.4.1 / 2026-05-09)도 PEP 621로 이동했다** [S94]: `[project]` 섹션 지원, **Poetry 2.0부터** "you should consider using the `project.dependencies` section instead". `[tool.poetry]`의 `name`·`description`·`license`·`authors`·`homepage`·`repository` 등은 **deprecated**. 여전히 `[tool.poetry]`에 남는 것: `package-mode`, `packages`, `include`/`exclude`, `plugins`, `requires-poetry`.

**pip-tools는 죽지 않았다** [S95]: 저장소 `archived: false`, 마지막 push **2026-07-24**, 최신 7.6.0 / 2026-07-18. README: "**pip-tools = pip-compile + pip-sync**". → "pip-tools는 끝났다"는 서술은 사실이 아니다. uv가 `uv pip compile`로 그 인터페이스를 **흡수**한 것이다 [S96]: "a drop-in replacement for common `pip`, `pip-tools`, and `virtualenv` commands" / "uv does not rely on or invoke pip".

### 4-B. 린트·타입체크 — 신규 타입체커의 성숙도는 정반대다 [S97][S98][S99]

**ruff 0.16.0 / 2026-07-23.** 포매터 [S97]:
> "The Ruff formatter is an extremely fast Python code formatter designed as a **drop-in replacement for Black**, available as part of the `ruff` CLI via `ruff format`."
> "When run over extensive Black-formatted projects like Django and Zulip, **> 99.9% of lines are formatted identically.**"

**⚠️ ruff의 버저닝은 SemVer가 아니다 (원문)** [S97]:
> "Ruff uses a custom versioning scheme that uses the **minor** version number for breaking changes and the **patch** version number for bug fixes. Ruff does not yet have a stable API; once Ruff's API is stable, the major version number and semantic versioning will be used."

→ **`0.16.0` → `0.17.0`이 breaking change다.** CI 핀 전략에 직결되는 사실이며, Spring/Node 독자가 반드시 오해하는 지점.

**타입체커 지형 — 추측 금지 구역. 실제 README에서 확인한 결과:**

| | Astral `ty` | Meta `pyrefly` |
|---|---|---|
| 버전 | **0.0.63** (2026-07-23) | **1.1.1** (2026-06-18) |
| 자기 선언 | **"ty is currently in beta."** [S98] | **"Pyrefly's current development status is stable."** [S99] |
| 버전 정책 | "ty uses `0.0.x` versioning. ty does not yet have a stable API; **breaking changes, including changes to diagnostics, may occur between any two versions.**" [S98] | "releases new minor versions (`1.x.0`) monthly… does *not* follow strict semantic versioning: **any version may introduce new type errors and other breaking changes.**" [S99] |
| 실적 주장 | "10x - 100x faster than mypy and Pyright" [S98] | "**the default type checker for Instagram's 20-million-line Python codebase at Meta**, and has been adopted by large open source projects including PyTorch and JAX" [S99] |
| FastAPI 관련성 | — | "Built-in support for frameworks and tools like **Pydantic**, Django, and pytest" [S99] |

→ **통념과 반대다.** Astral 제품(uv·ruff)의 성공 때문에 `ty`도 성숙했으리라 짐작하기 쉽지만, `ty`는 **0.0.x beta**이고 `pyrefly`가 **stable 1.x**다. 책에서 "CI 게이트로 걸어라"고 쓸 수 있는 건 pyrefly 쪽이다.

> 🔍 흥미로운 방증: FastAPI 자신의 소스 `applications.py`에 **`# ty: ignore[deprecated]`** 주석이 있다 [S7] — FastAPI 프로젝트가 `ty`를 실제로 돌리고 있다는 1차 증거다.

**mypy 2.3.0 / 2026-07-13** — 메이저가 2.x 대역이다(§6-7). ⚠️ 2.0의 breaking change 내역은 미확인(§7).
**pyright**: Microsoft 본체 1.1.411 / 2026-06-25. ⚠️ PyPI의 `pyright` 패키지는 자기 설명이 **"Command line wrapper for pyright"** — 공식 릴리스 채널이 아닌 커뮤니티 래퍼다 [S100].

### 4-C. GitHub Actions [S101][S102][S103]

**`astral-sh/setup-uv` — 현재 메이저는 v9** (최신 `v9.0.0`, **2026-07-21**, 릴리스명 "🌈 Change `prune-cache` default to `false`") [S101].
```yaml
- name: Install the latest version of uv
  uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
```
> "If you do not specify a version, this action will look for a `required-version` in a `uv.toml` or `pyproject.toml` file in the repository root. If none is found, the latest version will be installed." [S101]

캐싱 입력값 기본값 [S101]: `enable-cache: "auto"`(= **GitHub-hosted runner에서 기본 활성, self-hosted에서 비활성**), `cache-dependency-glob`은 `**/pyproject.toml`·`**/uv.lock`·`**/*requirements*.txt` 등, `prune-cache: "false"`(v9.0.0에서 변경).

⚠️ **문서 지연:** uv 자신의 GitHub 연동 가이드는 아직 **v8.1.0**을 핀한 예제를 싣고 있다 [S102]. 책에 실을 땐 v9.0.0으로 갱신하고, 이 지연 자체를 각주로 다는 게 좋다.

**`actions/setup-python` — 현재 메이저 v7** (`v7.0.0`, 2026-07-20) [S103].
**🔴 가장 흔한 함정 (action.yml 원문)** [S103]:
> `cache`: "Used to specify a package manager for caching in the default directory. **Supported values: pip, pipenv, poetry.**"

→ **`cache:`는 uv를 지원하지 않는다.** uv를 쓰면 `astral-sh/setup-uv`의 `enable-cache`를 쓰거나 `actions/cache`를 직접 구성해야 한다. Spring/NestJS 출신 독자가 가장 먼저 밟는 지뢰다.

> "caching is turned off by default" / "Restored cache will not be used if the requirements.txt file is not updated for a long time and a newer version of the dependency is available which can lead to an increase in total build time." [S103]

### 4-D. 매트릭스 설계 — Python 지원 현황 [S104]

Python 공식 devguide (조회 2026-07-25) [S104]:

| Branch | Status | First release | **End of life** |
|---|---|---|---|
| 3.15 | prerelease | 2026-10-01 | 2031-10 |
| **3.14** | **bugfix** | 2025-10-07 | 2030-10 |
| **3.13** | **bugfix** | 2024-10-07 | 2029-10 |
| 3.12 | security | 2023-10-02 | 2028-10 |
| 3.11 | security | 2022-10-24 | 2027-10 |
| **3.10** | security | 2021-10-04 | **2026-10** |
| 3.9 | **end-of-life** | 2020-10-05 | 2025-10-31 |

상태 정의 [S104]: `bugfix` = "bug fixes and security fixes are accepted. New binaries are built and released roughly every two months." / `security` = "only security fixes are accepted and no more binaries are released." / `end-of-life` = "Five years after a release, support ends."

**함의:** FastAPI 0.140.0·uvicorn 0.51.0·mypy 2.3.0·gunicorn 26.0.0이 모두 `requires_python >=3.10`인데(§6), **3.10은 2026-10 EOL로 3개월 남았다.** → 새 책의 권장 매트릭스는 **3.12 / 3.13 / 3.14**.

## 5. 클라우드 배포

### 5-A. 프로세스 매니저 — **공식 문서 두 곳이 서로 다르다** (중요)

이 책에서 반드시 짚어야 할 지점이다. FastAPI 문서와 Uvicorn 문서의 권장이 **일치하지 않는다.**

**FastAPI 공식 배포 문서** [S2] — gunicorn을 **아예 언급하지 않는다**:
```
$ fastapi run --workers 4 main.py
$ uv run uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```
> "when running on **Kubernetes** you will probably **not** want to use workers and instead run **a single Uvicorn process per container**" [S2]

**Uvicorn 공식 배포 문서** [S10] — 첫 문단의 일반 규칙에서 아직 gunicorn을 권한다:
> "As a general rule, you probably want to: ... Run `gunicorn -k uvicorn.workers.UvicornWorker` for production."

**그런데 같은 페이지 아래쪽에 경고가 있다** [S10]:
> "The `uvicorn.workers` module is deprecated and will be removed in a future release. You should use the [`uvicorn-worker`](https://github.com/Kludex/uvicorn-worker) package instead."
> ```bash
> python -m pip install uvicorn-worker
> ```

→ **정리해서 독자에게 줄 결론:** ① 컨테이너/K8s면 워커 1개 + 오케스트레이터 레플리카 [S2][S15]. ② 굳이 gunicorn을 써야 한다면 `uvicorn.workers`가 아니라 **별도 `uvicorn-worker` 패키지**를 써야 한다 [S10]. ③ Uvicorn 문서 상단의 일반 규칙은 하단 경고와 어긋나 있으니 그대로 따라 쓰면 안 된다.

**Uvicorn 내장 `--workers`가 gunicorn과 다른 점** [S10]:
> "Unlike gunicorn, uvicorn does not use pre-fork, but uses [`spawn`](...), which allows uvicorn's multiprocess manager to still work well on Windows."

- 자식 프로세스가 죽으면 자동 재시작하고, 파이프라인으로 상태를 감시해 **멈춘(stuck) 자식은 강제 시그널로 종료**한다 [S10]
- 시그널로 워커를 제어할 수 있다 (Windows 미지원) [S10]:
  - `SIGHUP`: "Gracefully restart the workers one at a time with no dropped requests. Fresh workers pick up new code on disk."
  - `SIGTTIN` / `SIGTTOU`: 워커 수 1개 증가 / 감소
- `--reload`와 `--workers`는 **상호 배타** [S10]

### 5-B. 컨테이너 — Uvicorn 공식 Dockerfile (uv 기반, 그대로 인용) [S15]

FastAPI 문서[S3]는 pip 예시를 보여주고 uv는 외부 가이드로 넘기지만, **Uvicorn 공식 문서에는 uv 기반 캐시 최적화 Dockerfile이 통째로 있다**:

```dockerfile title="Dockerfile"
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Run with uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

핵심 설명 (원문) [S15]:
> "The key strategy is to install dependencies first, then copy the project files. This approach leverages Docker's caching mechanism to significantly speed up rebuilds."

워커 개수 질문에 대한 답 (원문) [S15]:
> "A common question is **"how many workers should I run?"**. The image above uses a single Uvicorn worker. The recommended approach is to let your orchestration system manage the number of deployed containers rather than relying on the process manager inside the container."

비루트 유저 경고 (원문) [S15]:
> "For production, create a non-root user! When running in production, you should create a non-root user and run the container as that user."

> ⚠️ 위 Dockerfile은 **비루트 유저가 실제로 적용돼 있지 않다**(경고만 있음). 책에서 재사용할 때는 `USER` 지시어를 추가한 버전으로 보강해야 한다 — 공식 예시 그대로 쓰면 경고와 코드가 어긋난다.
> ⚠️ 베이스 이미지가 `python:3.12-slim`으로 **하드코딩**돼 있다(조회 2026-07-25). Python 3.12는 현시점 최신이 아니므로, 책에서는 태그를 그대로 베끼지 말 것.

`uv.lock` 설명 (원문) [S15]:
> "`uv.lock` is a `uv` specific lockfile. A lockfile is a file that contains the exact versions of the dependencies that were installed when the `uv.lock` file was created. This allows for deterministic builds and consistent deployments."

### 5-C. 프록시·로드밸런서 뒤 — forwarded headers 보안 [S10]

- Uvicorn이 지원하는 헤더는 **`X-Forwarded-For`와 `X-Forwarded-Proto` 둘뿐이다** [S10]
- `--proxy-headers`는 **기본 활성**이지만, `--forwarded-allow-ips`에 있는 IP만 신뢰한다. `--forwarded-allow-ips` 기본값은 **`127.0.0.1`**(또는 `$FORWARDED_ALLOW_IPS`) [S10]
- 공식 경고 (원문) [S10]:
  > "**Only trust clients you can actually trust!** Incorrectly trusting other clients can lead to malicious actors spoofing their apparent client address to your application."
  > "Rather than specifying what to trust, you can instruct Uvicorn to trust all clients using the literal `"*"`. You should only set this when you know you can trust all values within the forwarded headers (e.g. because your proxies remove the existing headers before setting their own)."

  → FastAPI 프록시 문서[S13]의 예시가 `--forwarded-allow-ips="*"`를 쓰므로, **복붙 위험**을 반드시 경고할 것.
- 프록시 체인에서 헤더가 홉마다 반복될 수 있다: `X-Forwarded-For`는 순서대로 결합(RFC 9110 §5.3 방식), `X-Forwarded-Proto`는 **마지막 값**을 사용 [S10]
- 신뢰된 프록시 판정 시 **클라이언트 포트는 `0`으로 설정된다**(헤더에 포트 정보가 없으므로) [S10]
- UDS 사용 시 주의: nginx가 UDS 뒤에 있으면 `X-Forwarded-For`에 리터럴 `unix:`를 넣고, Uvicorn이 UDS 뒤면 최초 client가 `None`이 된다 [S10]
- 복잡한 다단 프록시에는 부족할 수 있다 (원문) [S10]:
  > "Uvicorn's `--proxy-headers` behavior may not be sufficient for more complex proxy configurations that use different combinations of headers, or where the application is running behind more than one intermediary proxying service."

### 5-D. `uvicorn-worker` — gunicorn을 꼭 써야 한다면 [S105]

§5-A의 결론을 코드로 확정하는 근거다. Uvicorn 소스 `uvicorn/workers.py`는 **파일이 아직 존재하지만 임포트 시점에 경고를 던진다** (원문) [S105]:
```python
warnings.warn(
    "The `uvicorn.workers` module is deprecated. Please use `uvicorn-worker` package instead.\n"
    "For more details, see https://github.com/Kludex/uvicorn-worker.",
    DeprecationWarning,
)
```
대체 패키지 **`uvicorn-worker` 0.4.0 / 2025-09-20** (§6-8).

또 gunicorn 경유 시의 기능 손실 (Uvicorn 문서 원문) [S10]:
> "Gunicorn provides a different set of configuration options to Uvicorn, so some options such as **`--limit-concurrency` are not yet supported** when running with Gunicorn."

→ §3-C의 동시성 게이트를 쓰려면 gunicorn을 벗어나야 한다는 뜻. 권장 경로(uvicorn 단독 + 오케스트레이터 레플리카)를 뒷받침하는 추가 논거다.

### 5-E. 🔴 Alpine vs slim — 통념이 절반만 맞다 (실측했다) [S106][S107]

**흔한 설명:** "Alpine은 musl이라 manylinux wheel을 못 써서 소스 빌드가 돌고 느리다."

**1차 소스 확인 결과, 이 설명은 출처가 어긋나 있다** [S106]:
- 공식 `python` 이미지 README의 **alpine** 문단은 wheel 얘기를 하지 않는다. 오직 런타임 호환성이다:
  > "**The main caveat to note is that it does use musl libc instead of glibc and friends, so software will often run into issues depending on the depth of their libc requirements/assumptions.**"
- "소스 빌드가 실패한다"는 문장은 **slim** 문단에 있고, 원인은 musl이 아니라 **컴파일러 부재**다:
  > "`pip install` may fail when installing a Python distribution package from a source distribution. **This image does not contain the Debian packages required to compile extension modules written in other languages.**"

**PEP 656(musllinux)은 2021년 Final이다** [S107]: "Platform Tag for Linux Distributions Using Musl", Status **Final**, Created 2021-03-17.

**그리고 실제로 wheel이 배포되고 있다 — PyPI JSON API로 최신 릴리스의 파일 태그를 직접 집계한 결과 (조회 2026-07-25):**

| 패키지 | 버전 | musllinux wheel | manylinux wheel |
|---|---|---|---|
| pydantic-core | 2.47.0 | **21** | 48 |
| uvloop | 0.22.1 | **16** | 16 |
| httptools | 0.8.0 | **14** | 14 |
| numpy | 2.5.1 | **8** | 8 |
| greenlet | 3.5.4 | **16** | 40 |
| orjson | 3.11.9 | **20** | 30 |
| cryptography | 49.0.0 | **6** | 31 |

→ **FastAPI 스택의 핵심 네이티브 확장은 전부 musllinux wheel을 배포한다.** uvloop·httptools·numpy는 manylinux와 **개수가 같다.**

**정확한 권고:** "Alpine 쓰지 마라"가 아니라 —
1. 기본은 **`-slim`(Debian)**을 쓴다.
2. Alpine을 쓸 거면 **의존성 전체의 musllinux wheel 보유 여부를 실제로 확인**하라(위 PyPI JSON 조회 방법을 그대로 알려줄 수 있다).
3. 남는 진짜 리스크는 ① musl vs glibc **런타임 동작 차이**[S106] ② musllinux wheel이 없는 롱테일 패키지 ③ 그 경우 alpine에는 툴체인이 없어 빌드 실패.

⚠️ "musl 때문에 소스 빌드가 돈다"는 **권위 있는 단일 문장은 찾지 못했다**(§7). 위 실측이 대체 근거다.

**비루트 유저의 1차 출처** — FastAPI 공식 Docker 문서에는 비루트 지침이 **없다**. uv 문서가 "best practices"로 링크하는 예제 저장소에 있다 [S108]:
```dockerfile
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot
...
USER nonroot
```

### 5-F. Kubernetes — probe와 종료 시퀀스 [S109][S110]

**probe 3종의 공식 정의 (원문)** [S109]:
> **startup**: "Startup probes verify whether the application within a container is started. **If a startup probe is configured, Kubernetes does not execute liveness or readiness probes until the startup probe succeeds**, allowing the application time to finish its initialization."
> **liveness**: "Liveness probes determine when to restart a container. For example, liveness probes could catch a deadlock, where an application is running, but unable to make progress."
> **readiness**: "Readiness probes determine when a container is ready to accept traffic… **If the readiness probe returns a failed state, the EndpointSlice controller removes the Pod's IP address from the EndpointSlices of all Services that match the Pod.**"

**FastAPI 설계에 직결되는 처방 (원문)** [S109]:
> "**When your app has a strict dependency on back-end services, you can implement both a liveness and a readiness probe. The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available.** This helps you avoid directing traffic to Pods that can only respond with error messages."
> "If your container usually starts in more than `initialDelaySeconds + failureThreshold × periodSeconds`, you should specify a startup probe that checks the same endpoint as the liveness probe."
> "A common pattern for liveness probes is to use the same low-cost HTTP endpoint as for readiness probes, but with a **higher `failureThreshold`**."

→ 즉 **`/healthz`(liveness)와 `/ready`(readiness)를 분리**하고, readiness에서만 DB·Redis 연결을 확인하는 게 공식 권장 패턴이다.

기본값 [S109]: `periodSeconds` **10초** / `timeoutSeconds` **1초** / `failureThreshold` **3** / `successThreshold` 1(liveness·startup은 반드시 1). `httpGet`은 "status code greater than or equal to 200 and less than 400"이면 성공.

**Pod 종료 시퀀스 (공식 저장소 원문)** [S110]:
> "the kubelet makes requests to the container runtime to attempt to stop the containers in the pod by **first sending a TERM (aka. SIGTERM) signal** to the main process in each container… **Once the grace period has expired, the KILL signal is sent** to any remaining processes"
> "**If one of the Pod's containers has defined a `preStop` hook and the `terminationGracePeriodSeconds` in the Pod spec is not set to 0, the kubelet runs that hook inside of the container. The default `terminationGracePeriodSeconds` setting is 30 seconds.**"
> "**If the `preStop` hook is still running after the grace period expires, the kubelet requests a small, one-off grace period extension of 2 seconds.**"
> "**At the same time as** the kubelet is starting graceful shutdown of the Pod, the control plane evaluates whether to remove that shutting-down Pod from EndpointSlice objects"
> "**Any endpoints that represent the terminating Pods are not immediately removed from EndpointSlices**, and a status indicating terminating state is exposed from the EndpointSlice API. Terminating endpoints always have their `ready` status as `false`… so load balancers will not use it for regular traffic."

**⚠️ 통념 교정:** 흔히 "SIGTERM과 엔드포인트 제거의 순서가 보장되지 않아 트래픽이 샌다"고 설명하지만, 현재 문서의 실제 서술은 다르다 — terminating 엔드포인트는 **즉시 제거되지 않고 `ready: false`로 남으며**, kubelet 종료와 컨트롤 플레인의 EndpointSlice 갱신은 **병렬("At the same time as")** 이다. → `preStop` sleep 패턴의 근거는 "제거 전에 트래픽이 온다"가 아니라 **"두 과정이 동시에 진행되므로 아직 갱신을 전파받지 못한 LB/클라이언트가 존재할 수 있다"** 쪽으로 서술해야 정확하다.

**FastAPI 측 대응 매핑 (전부 위에서 출처 확인된 값):**
- `terminationGracePeriodSeconds` **기본 30초** > uvicorn `--timeout-graceful-shutdown` 이어야 SIGKILL 전에 정리가 끝난다 (§3-D)
- lifespan의 `yield` 이후 코드가 SIGTERM 이후 정리 경로 [S50]
- uvicorn은 종료 시 "wait for any background tasks to run to completion"을 보장한다 [S12] → `BackgroundTasks`(§1-D 계열)가 grace period 안에 끝나야 한다

**HPA** [S111]: 알고리즘은 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`, tolerance 기본 **0.1**, sync period 기본 **15초**, downscale stabilization window 기본 **5분**(upscale은 0=즉시). 구동 메트릭 4종: Resource(CPU/Memory, **컨테이너 `requests` 대비 비율**), Custom, External, ContainerResource.

⚠️ **"IO-bound async 앱에 CPU가 나쁜 신호"라는 문장은 k8s 문서에 없다.** 유일하게 찾은 벤더 1차 근거는 Cloud Run 문서다(§5-G). k8s로의 확장은 저자의 추론으로 명시할 것.

### 5-G. 서버리스 — Lambda와 Cloud Run은 async에 대해 정반대다 [S112][S113][S114]

**AWS Lambda 지원 Python 런타임 (공식 문서, 조회 2026-07-25)** [S112]:

| Name | Identifier | OS | Deprecation date |
|---|---|---|---|
| Python 3.14 | `python3.14` | Amazon Linux 2023 | 2029-06-30 |
| Python 3.13 | `python3.13` | Amazon Linux 2023 | 2029-06-30 |
| Python 3.12 | `python3.12` | Amazon Linux 2023 | 2028-10-31 |
| Python 3.11 | `python3.11` | **Amazon Linux 2** | 2027-06-30 |
| Python 3.10 | `python3.10` | **Amazon Linux 2** | **2026-10-31** |

이미 deprecated: `python3.9`(2025-12-15), `python3.8`(2024-10-14), 그 이하.
> "**Important** Amazon Linux 2 is scheduled for end of life on June 30, 2026… We recommend customers upgrade to an Amazon Linux 2023-based runtime as soon as possible." [S112]
> 예정: "**Python 3.15** - November 2026" [S112]

**웹앱에 직결되는 Lambda 쿼터** [S113]: 응답 payload **6MB**(스트리밍은 200MB, "2MBps for the remainder"), 타임아웃 **900초(15분)**, 컨테이너 이미지 **10GB**, 기본 동시 실행 **1,000**.

**🔴 동시성 모델 — 이 책의 핵심 논점 (공식 원문)** [S114]:
> "**For each concurrent request, Lambda provisions a separate instance of your execution environment.**"
> "During this entire process, **this execution environment is busy and cannot process other requests.**"
> 공식: `Concurrency = (average requests per second) * (average request duration in seconds)`
> 스케일 속도: "your concurrency scaling rate is **1,000 execution environment instances every 10 seconds**"

**Google Cloud Run** [S115][S116] — ⚠️ `cloud.google.com/run/docs/*`는 현재 **`docs.cloud.google.com`으로 301 리다이렉트**된다(2026-07 확인). 책의 URL은 새 호스트로 쓸 것.
- 포트 계약: "Cloud Run injects the `PORT` environment variable", `0.0.0.0` 바인딩 필수, 기본 **8080** [S115]
- 기동: "Your instances must listen for requests within **4 minutes** after being started." [S115]
- **graceful shutdown이 K8s와 다르다 (원문)** [S115]:
  > "Cloud Run sends a `SIGTERM` signal to all the containers in an instance, indicating the start of a **10 second period** before the actual shutdown occurs, at which point Cloud Run sends a `SIGKILL` signal."
  → **K8s 기본 30초 vs Cloud Run 10초.** FastAPI `lifespan` 정리가 10초 안에 끝나야 한다. 대비시키기 좋은 숫자다.
- **동시성:** 인스턴스당 최대 동시 요청 기본 **"80 times the number of vCPUs"**, 최대 **1,000** [S116]. "a concurrency of 1 is likely to negatively affect scaling performance."
- **CPU 기반 스케일링의 함정 — 유일하게 찾은 벤더 1차 근거** [S116]:
  > "A single-threaded application on a multi-vCPU instance may max out one vCPU while others idle… average CPU utilization can remain deceptively low… preventing effective CPU-based scaling."
  ⚠️ 이 문장은 엄밀히 **"멀티 vCPU 위의 싱글스레드 앱"**에 관한 것이지 "IO-bound async 앱 일반"이 아니다. 확장 해석은 저자 추론으로 표시할 것.
- min instances 기본 **0**(scale-to-zero), 켜면 과금 발생 [S117]
- 소스 배포 buildpack 지원 Python [S118]: `google-24` 빌더 = **3.13.x, 3.14.x** / `google-22` = 3.10~3.13. 버전 선택 우선순위: `GOOGLE_PYTHON_VERSION` > `.python-version` > 최신 LTS. 엔트리포인트 감지 순서에 **uvicorn·fastapi가 포함**된다(gunicorn → uvicorn → fastapi → …).

**Azure Container Apps** [S119]: KEDA 기반. minReplicas 기본 **0**, maxReplicas 기본 **10**(각각 최대 1,000). HTTP 규칙 `concurrentRequests` 기본 **10**. Cool down period **300초**, polling **30초**.
> "You aren't billed usage charges if your container app scales to zero." [S119]
> ⚠️ "**Important** … If ingress is disabled and you don't define a `minReplicas` or a custom scale rule, your container app scales to zero and has no way of starting back up." [S119]
> ⚠️ MS 문서의 Bicep 예제에 `maxReplicas`/`minReplicas`가 뒤바뀐 오류가 있다 — 표의 값만 인용할 것 [S119].

**Mangum vs AWS Lambda Web Adapter** [S120][S121]:

| | Mangum | Lambda Web Adapter |
|---|---|---|
| 형태 | Python 라이브러리 (`handler = Mangum(app)`) | Lambda **extension 바이너리** |
| 코드 변경 | 핸들러 래핑 필요 | 없음 — `fastapi run` 그대로 |
| 언어 | Python 전용 | 무관 ("anything speaks HTTP 1.1/1.0") |
| 응답 스트리밍 | ⚠️ 미확인(§7) | 지원 (`AWS_LWA_INVOKE_MODE=response_stream`) |
| 제공 | 커뮤니티 (`Kludex/mangum`) | **AWS 공식** (`aws/aws-lambda-web-adapter`, **v1.0.1 / 2026-05-28**) |
| 적용 | zip/컨테이너 | `COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:... /lambda-adapter /opt/extensions/` 한 줄 |

**Mangum 유지보수 판정 — 데이터에 맞는 표현** [S120]: `archived: false`, 최신 릴리스 0.21.0 / 2026-02-01, 마지막 push 2026-05-31. 그러나 **최근 커밋 5건 중 3건이 Dependabot 범프, 2건이 문서 링크 수정**이다. → "죽었다"도 "활발히 개발 중"도 아닌 **"유지보수 모드(maintenance mode)"**가 정확한 표현이다.

**서사 포인트:** LWA를 쓰면 §5-B의 Dockerfile을 **그대로** Lambda에 올릴 수 있다 — Mangum은 못 한다. Spring 독자에게는 "`aws-serverless-java-container` vs 그냥 컨테이너" 대비로 설명하면 즉시 통한다.

### 5-H. PaaS 계약 비교 [S122][S123][S124]

| | 기본 포트 | 포트 전달 | scale-to-zero |
|---|---|---|---|
| **Fly.io** | **8080** (`internal_port`) | `fly.toml` 선언 | `auto_stop_machines="stop"` + `min_machines_running=0` |
| **Cloud Run** | **8080** | `PORT` env 주입 | 기본 (min instances 0) |
| **Azure Container Apps** | ingress target-port | — | 기본 (minReplicas 0) |
| **Render** | **10000** | `PORT` env | ⚠️ 미확인(§7) |
| **Railway** | ⚠️ 미확인(§7) | ⚠️ 미확인(§7) | ⚠️ 미확인(§7) |

- **Render** 공식 FastAPI 가이드의 Start Command [S122]: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  > "Every Render web service must bind to a port on host `0.0.0.0` to serve HTTP requests." / "The default value of `PORT` is **10000** for all Render web services." [S122]
- **Railway** 공식 FastAPI 가이드는 uvicorn이 아니라 **Hypercorn**을 쓴다 [S123]: `["hypercorn", "main:app", "--bind", "::"]`(IPv6) — "The FastAPI app is run via a Hypercorn server as defined by the `startCommand` in the railway.json file."
- **Fly.io** [S124]: `internal_port` "The default is 8080." / `auto_start_machines` 기본 `true` / `min_machines_running` 기본 `0`.
  ⚠️ 미묘한 지점: **설정 스키마의 `auto_stop_machines` 기본값은 `"off"`이지만, `fly launch`가 새 앱에 써 넣는 값은 `"stop"`이다.** 두 문서가 다 맞으므로 책에서 구분할 것.

### 5-I. 대안 서버 — 언제 uvicorn을 벗어나는가 [S125][S126]

**Granian 2.7.9 / 2026-07-03** (Rust, Hyper+Tokio 기반) [S125]:
> "Granian is a Rust HTTP server for Python applications built on top of Hyper and Tokio."
> 쓸 이유: "looking for the most performant way to serve your Python application under **HTTP/2**" / "you need great concurrency capabilities, especially with websockets"
> **쓰지 말아야 할 이유 (문서가 직접 밝힌다 — 균형 잡기에 유용):** "you want a *pure Python* solution / you need advanced debugging features / your application relies on `trio` or `gevent` / you're looking for ASGI extensions not (yet) implemented"

**Hypercorn 0.18.0 / 2025-11-08** (⚠️ 8개월 이상 릴리스 없음) [S126]:
> "Hypercorn supports HTTP/1, HTTP/2, WebSockets (over HTTP/1 and HTTP/2), ASGI, and WSGI specifications. Hypercorn can utilise asyncio, uvloop, or trio worker types."
> HTTP/3: "Hypercorn can optionally serve the **current draft** of the HTTP/3 specification using the aioquic library… `pip install hypercorn[h3]` … `hypercorn --quic-bind localhost:4433`"

**정리:** uvicorn은 **HTTP/1.1만**. HTTP/2가 필요하면 Granian 또는 Hypercorn, **HTTP/3(QUIC)는 Hypercorn만**이며 그것도 `[h3]` extra + 문서 표현상 "current draft"다.

**`uvicorn[standard]`가 설치하는 6개 (공식 문서 원문)** [S127]: `uvloop`("When `uvloop` is installed, Uvicorn will use it by default"), `httptools`(HTTP/1.1 파싱 기본), `websockets`(WS 기본), `watchfiles`(`--reload` 기본), `python-dotenv`(`--env-file`용), `PyYAML`(`--log-config` yaml용). 기본 설치는 `h11` + `click`만.

### 5-J. 콜드 스타트 × async — 사실과 추론의 분리

**사실만 (전부 벤더 1차 소스, 위에 인용됨):**
- Lambda: 실행 환경 1개가 요청 1건을 처리하는 동안 **다른 요청을 받지 못한다** [S114]
- Cloud Run: 인스턴스당 동시 요청 기본 **80 × vCPU**, 최대 1,000 [S116]
- Azure Container Apps: HTTP `concurrentRequests` 기본 **10** [S119]

**추론 (저자의 결론 — 벤더가 이렇게 말한 것은 아님. 책에서 반드시 "추론"으로 표시할 것):**
1. **Lambda 실행 환경 하나 안에서는 async 동시성이 처리량을 늘려주지 않는다.** `async def`의 이득은 *한 요청 내부의 여러 I/O를 겹칠 때만* 유효하고, 요청 간 다중화는 Lambda가 환경을 더 띄우는 방식(=비용·콜드 스타트)으로만 얻는다.
2. **Cloud Run은 정반대다.** 인스턴스당 기본 80×vCPU이므로 async I/O 다중화가 **직접** 인스턴스 수와 비용을 줄인다.
3. → **"FastAPI를 서버리스에 올린다"를 한 문장으로 묶으면 안 된다.** Lambda(요청당 1환경)와 Cloud Run(인스턴스당 N요청)은 async에 대해 **정반대의 경제학**을 갖는다. 이 책에서 매우 강력한 절이 될 수 있다.

---

## 6. 확인된 버전 정보 (릴리스 특정 URL + 조회일 필수)

**조회 방법:** PyPI JSON API (`https://pypi.org/pypi/{pkg}/json`)의 `info.version` + 해당 릴리스의 `upload_time_iso_8601`, 그리고 GitHub Releases API로 교차 확인. **전 항목 조회일 = 2026-07-25.**

> 이 표가 이 문서에서 가장 신뢰도 높은 데이터다. 이후 챕터에서 버전을 언급할 때는 이 표를 기준으로 하고, 반드시 `"{버전}/2026-07 기준"` 형태로 못 박을 것.

### 6-1. 코어 (FastAPI 스택)

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL (조회 2026-07-25) |
|---|---|---|---|---|
| fastapi | 0.140.0 | 2026-07-24 | >=3.10 | https://pypi.org/project/fastapi/0.140.0/ |
| starlette | 1.3.1 | 2026-06-12 | >=3.10 | https://pypi.org/project/starlette/1.3.1/ |
| pydantic | 2.13.4 | 2026-05-06 | >=3.9 | https://pypi.org/project/pydantic/2.13.4/ |
| pydantic-settings | 2.14.2 | 2026-06-19 | >=3.10 | https://pypi.org/project/pydantic-settings/2.14.2/ |
| uvicorn | 0.51.0 | 2026-07-08 | >=3.10 | https://pypi.org/project/uvicorn/0.51.0/ |
| anyio | 4.14.2 | 2026-07-12 | >=3.10 | https://pypi.org/project/anyio/4.14.2/ |
| httpx | 0.28.1 | **2024-12-06** | >=3.8 | https://pypi.org/project/httpx/0.28.1/ |
| python-multipart | 0.0.32 | 2026-06-04 | >=3.10 | https://pypi.org/project/python-multipart/0.0.32/ |
| jinja2 | 3.1.6 | 2025-03-05 | >=3.7 | https://pypi.org/project/jinja2/3.1.6/ |

> **주의:** `httpx`는 2024-12-06 이후 새 릴리스가 없다(조회 2026-07-25). 죽은 게 아니라 안정화된 것으로 보이지만, "최신 릴리스" 서술 시 이 날짜를 그대로 쓸 것.
> **주의:** FastAPI 0.140.0의 의존성 핀은 `starlette>=0.46.0`, `pydantic>=2.9.0`, `typing-extensions>=4.8.0` [S6]. **FastAPI가 Starlette 1.x를 강제하지 않는다** — 독자의 lock 파일에 따라 0.4x일 수도 1.x일 수도 있다.

### 6-2. 서버 / 프로세스 매니저

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL |
|---|---|---|---|---|
| gunicorn | 26.0.0 | 2026-05-05 | >=3.10 | https://pypi.org/project/gunicorn/26.0.0/ |
| granian | 2.7.9 | 2026-07-03 | >=3.10 | https://pypi.org/project/granian/2.7.9/ |
| hypercorn | 0.18.0 | 2025-11-08 | >=3.10 | https://pypi.org/project/hypercorn/0.18.0/ |
| uvloop | 0.22.1 | 2025-10-16 | >=3.8.1 | https://pypi.org/project/uvloop/0.22.1/ |
| httptools | 0.8.0 | 2026-05-25 | >=3.9 | https://pypi.org/project/httptools/0.8.0/ |
| websockets | 16.1.1 | 2026-07-17 | >=3.10 | https://pypi.org/project/websockets/16.1.1/ |
| wsproto | 1.3.2 | 2025-11-20 | >=3.10 | https://pypi.org/project/wsproto/1.3.2/ |

### 6-3. 데이터 계층

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL |
|---|---|---|---|---|
| sqlalchemy | 2.0.51 | 2026-06-15 | >=3.7 | https://pypi.org/project/sqlalchemy/2.0.51/ |
| alembic | 1.18.5 | 2026-06-25 | >=3.10 | https://pypi.org/project/alembic/1.18.5/ |
| asyncpg | 0.31.0 | 2025-11-24 | >=3.9.0 | https://pypi.org/project/asyncpg/0.31.0/ |
| psycopg | 3.3.4 | 2026-05-01 | >=3.10 | https://pypi.org/project/psycopg/3.3.4/ |
| aiosqlite | 0.22.1 | 2025-12-23 | >=3.9 | https://pypi.org/project/aiosqlite/0.22.1/ |
| aiomysql | 0.3.2 | 2025-10-22 | >=3.9 | https://pypi.org/project/aiomysql/0.3.2/ |
| asyncmy | 0.2.11 | 2026-01-15 | >=3.9 | https://pypi.org/project/asyncmy/0.2.11/ |
| sqlmodel | 0.0.39 | 2026-06-25 | >=3.10 | https://pypi.org/project/sqlmodel/0.0.39/ |
| redis | 8.0.1 | 2026-06-23 | >=3.10 | https://pypi.org/project/redis/8.0.1/ |
| pymongo | 4.17.0 | 2026-04-20 | >=3.9 | https://pypi.org/project/pymongo/4.17.0/ |
| motor | 3.7.1 | **2025-05-14** | >=3.9 | https://pypi.org/project/motor/3.7.1/ |
| beanie | 2.1.0 | 2026-03-26 | <3.14,>=3.10 | https://pypi.org/project/beanie/2.1.0/ |

> **SQLModel은 여전히 `0.0.x` 대역이다** (0.0.39 / 2026-06-25 조회). 버전 번호 자체가 성숙도 신호 — 서술 시 반드시 명시.

### 6-4. 백그라운드 / 태스크 큐 / GraphQL / SSE

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL |
|---|---|---|---|---|
| celery | 5.6.3 | 2026-03-26 | >=3.9 | https://pypi.org/project/celery/5.6.3/ |
| arq | 0.28.0 | 2026-04-16 | >=3.9 | https://pypi.org/project/arq/0.28.0/ |
| dramatiq | 2.2.0 | 2026-06-17 | >=3.10 | https://pypi.org/project/dramatiq/2.2.0/ |
| rq | 2.10.0 | 2026-06-20 | >=3.10 | https://pypi.org/project/rq/2.10.0/ |
| taskiq | 0.12.4 | 2026-05-08 | <4,>=3.10 | https://pypi.org/project/taskiq/0.12.4/ |
| sse-starlette | 3.4.6 | 2026-07-20 | >=3.10 | https://pypi.org/project/sse-starlette/3.4.6/ |
| broadcaster | 0.3.1 | **2024-08-01** | >=3.8 | https://pypi.org/project/broadcaster/0.3.1/ |
| strawberry-graphql | 0.323.2 | 2026-07-23 | <4.0,>=3.10 | https://pypi.org/project/strawberry-graphql/0.323.2/ |
| ariadne | 1.1.0 | 2026-06-15 | >=3.10 | https://pypi.org/project/ariadne/1.1.0/ |

### 6-5. 인증 / 보안

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL |
|---|---|---|---|---|
| pyjwt | 2.13.0 | 2026-05-21 | >=3.9 | https://pypi.org/project/pyjwt/2.13.0/ |
| python-jose | 3.5.0 | 2025-05-28 | >=3.9 | https://pypi.org/project/python-jose/3.5.0/ |
| pwdlib | 0.3.0 | 2025-10-25 | >=3.10 | https://pypi.org/project/pwdlib/0.3.0/ |
| bcrypt | 5.0.0 | 2025-09-25 | >=3.8 | https://pypi.org/project/bcrypt/5.0.0/ |
| passlib | 1.7.4 | **2020-10-08** | (미지정) | https://pypi.org/project/passlib/1.7.4/ |
| authlib | 1.7.2 | 2026-05-06 | >=3.10 | https://pypi.org/project/authlib/1.7.2/ |
| itsdangerous | 2.2.0 | 2024-04-16 | >=3.8 | https://pypi.org/project/itsdangerous/2.2.0/ |

> **`passlib` 최신 릴리스는 2020-10-08 (조회 2026-07-25) — 약 5년 9개월간 새 릴리스가 없다.** 이건 검증된 사실이다. "passlib는 유지보수가 중단됐다"는 *해석*이므로, 서술할 때는 릴리스 날짜라는 사실을 제시하고 해석은 별도로 표시할 것. 공식 문서가 `pwdlib`로 갈아탄 것[S1]이 방증.

### 6-6. 관측성 / 테스트

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL |
|---|---|---|---|---|
| opentelemetry-api | 1.44.0 | 2026-07-16 | >=3.10 | https://pypi.org/project/opentelemetry-api/1.44.0/ |
| opentelemetry-sdk | 1.44.0 | 2026-07-16 | >=3.10 | https://pypi.org/project/opentelemetry-sdk/1.44.0/ |
| opentelemetry-instrumentation-fastapi | **0.65b0** | 2026-07-16 | >=3.10 | https://pypi.org/project/opentelemetry-instrumentation-fastapi/0.65b0/ |
| prometheus-client | 0.26.0 | 2026-07-24 | >=3.9 | https://pypi.org/project/prometheus-client/0.26.0/ |
| prometheus-fastapi-instrumentator | 8.0.2 | 2026-06-23 | >=3.10 | https://pypi.org/project/prometheus-fastapi-instrumentator/8.0.2/ |
| structlog | 26.1.0 | 2026-06-06 | >=3.10 | https://pypi.org/project/structlog/26.1.0/ |
| loguru | 0.7.3 | 2024-12-06 | <4.0,>=3.5 | https://pypi.org/project/loguru/0.7.3/ |
| asgi-correlation-id | 5.0.1 | 2026-06-09 | >=3.10 | https://pypi.org/project/asgi-correlation-id/5.0.1/ |
| pytest | 9.1.1 | 2026-06-19 | >=3.10 | https://pypi.org/project/pytest/9.1.1/ |
| pytest-asyncio | 1.4.0 | 2026-05-26 | >=3.10 | https://pypi.org/project/pytest-asyncio/1.4.0/ |
| testcontainers | 4.15.0 | 2026-07-24 | >=3.10 | https://pypi.org/project/testcontainers/4.15.0/ |

> **OTel 계측 패키지의 버전 대역이 다르다** — API/SDK는 `1.44.0`인데 instrumentation은 `0.65b0`(베타 표기). OTel Python 생태계의 관례이므로 "1.x 안정 + 계측 0.x베타"를 그대로 서술할 것.

### 6-7. 툴체인 (CI/CD)

| 패키지 | 버전 | 릴리스일 | requires_python | 릴리스 URL |
|---|---|---|---|---|
| uv | 0.11.32 | 2026-07-23 | >=3.8 | https://pypi.org/project/uv/0.11.32/ |
| ruff | 0.16.0 | 2026-07-23 | >=3.7 | https://pypi.org/project/ruff/0.16.0/ |
| mypy | 2.3.0 | 2026-07-13 | >=3.10 | https://pypi.org/project/mypy/2.3.0/ |
| ty | **0.0.63** | 2026-07-23 | >=3.8 | https://pypi.org/project/ty/0.0.63/ |
| pyrefly | 1.1.1 | 2026-06-18 | >=3.8 | https://pypi.org/project/pyrefly/1.1.1/ |
| pyright | 1.1.411 | 2026-06-25 | >=3.7 | https://pypi.org/project/pyright/1.1.411/ |
| poetry | 2.4.1 | 2026-05-09 | <4.0,>=3.10 | https://pypi.org/project/poetry/2.4.1/ |
| pip-tools | 7.6.0 | 2026-07-18 | >=3.9 | https://pypi.org/project/pip-tools/7.6.0/ |
| mangum | 0.21.0 | 2026-02-01 | >=3.9 | https://pypi.org/project/mangum/0.21.0/ |

> **`uv`와 `ruff`는 아직 0.x다** (0.11.32 / 0.16.0, 둘 다 2026-07-23). "사실상 표준"이라는 채택 현실과 "0.x 버전"이라는 표기가 공존한다 — 둘 다 쓸 것.
> **`ty`는 0.0.63** — 아직 `0.0.x` 대역. `pyrefly`는 1.1.1로 이미 1.x에 진입. 두 신규 타입체커의 성숙도 표기가 다르다.

### 6-8. 추가 확인 패키지 (본 문서 작성자 직접 조회, 2026-07-25)

| 패키지 | 버전 | 릴리스일 | 릴리스 URL | 비고 |
|---|---|---|---|---|
| **httpx2** | **2.9.1** | **2026-07-24** | https://pypi.org/project/httpx2/2.9.1/ | 🔴 아래 설명 |
| uvicorn-worker | 0.4.0 | 2025-09-20 | https://pypi.org/project/uvicorn-worker/0.4.0/ | `uvicorn.workers` 대체(§5-D) |
| fastapi-cli | 0.0.32 | 2026-07-16 | https://pypi.org/project/fastapi-cli/0.0.32/ | `fastapi run` 제공 |
| tenacity | 9.1.4 | 2026-02-07 | https://pypi.org/project/tenacity/9.1.4/ | httpx 문서가 지목한 재시도 도구(§1-I) |
| pybreaker | 1.4.1 | 2025-09-21 | https://pypi.org/project/pybreaker/1.4.1/ | 서킷브레이커 중 가장 활발 |
| fastapi-pagination | 0.15.15 | 2026-06-16 | https://pypi.org/project/fastapi-pagination/0.15.15/ | |
| fastapi-problem | 0.12.1 | 2026-02-10 | https://pypi.org/project/fastapi-problem/0.12.1/ | RFC 9457 |
| fasthx | 3.2.2 | 2026-07-23 | https://pypi.org/project/fasthx/3.2.2/ | HTMX. ⚠️ README 미검증(§7) |
| jinja2-fragments | 1.12.0 | 2026-04-08 | https://pypi.org/project/jinja2-fragments/1.12.0/ | HTMX partial swap |
| argon2-cffi | 25.1.0 | 2025-06-03 | https://pypi.org/project/argon2-cffi/25.1.0/ | `pwdlib[argon2]` 백엔드 |
| auth0-fastapi-api | **1.0.0b7** | 2026-04-09 | https://pypi.org/project/auth0-fastapi-api/1.0.0b7/ | **아직 beta** |
| asgi-lifespan | 2.1.0 | **2023-03-28** | https://pypi.org/project/asgi-lifespan/2.1.0/ | ⚠️ 3년+ 정체. 공식 테스트 문서가 권장(§3-K) |
| aioredis | 2.0.1 | **2021-12-27** | https://pypi.org/project/aioredis/2.0.1/ | ⚠️ redis-py에 흡수됨(§2-I) |
| **sqlalchemy** | **2.1.0b3** | **2026-06-27** | https://pypi.org/project/sqlalchemy/2.1.0b3/ | **베타** (b1 2026-01-21, b2 2026-04-16) |

> **🔴 httpx 거버넌스 변화 — 확인된 사실만:**
> - `encode/httpx`는 archived가 **아니지만** 마지막 push가 **2026-03-29**이고, PyPI 최신은 **0.28.1 / 2024-12-06** — 약 1년 8개월간 릴리스 없음 (본 문서 작성자 GitHub/PyPI API 직접 조회).
> - `pydantic/httpx2` 저장소가 **2026-05-11 생성**되어 `httpx2` **2.9.1 / 2026-07-24**를 배포 중이다(stars 807, 조회 2026-07-25).
> - Starlette 릴리스 노트가 이를 반영한다 [S5]: `1.3.0 (2026-06-11)` Added — "**Add httpx2 to the full extra #3323.**" / `1.2.1 (2026-05-31)` Fixed — "Use httpx2 for type checking in the testclient module #3304."
> - ⚠️ httpx2 README의 "Pydantic이 stewardship을 인수했다"는 서술은 하위 에이전트가 raw로 인용했으나 **본 문서 작성자가 직접 재확인하지 않았다**(§7). 위 4개 사실(릴리스 정체·신규 저장소·Starlette 채택)은 직접 확인했다.
> - **책에서의 취급:** httpx는 여전히 FastAPI `[standard]`의 의존성(`httpx<1.0.0,>=0.23.0`)이며 `TestClient`의 기반이다. httpx2는 **주시 대상**으로 언급하되 "httpx는 끝났다"고 쓰지 말 것.

### 6-9. GitHub Actions (본 문서 작성자 직접 조회, 2026-07-25)

| 액션 | 최신 태그 | 발행일 | 비고 |
|---|---|---|---|
| `astral-sh/setup-uv` | **v9.0.0** | 2026-07-21 | 릴리스명: "🌈 Change `prune-cache` default to `false`" |
| `actions/setup-python` | **v7.0.0** | 2026-07-20 | `cache:`는 pip/pipenv/poetry만 — **uv 미지원**(§4-C) |

### 6-10. GitHub Releases 교차 확인 (조회 2026-07-25)

PyPI와 GitHub이 **전부 일치**했다. 저장소 이전이 확인된 3건이 특히 중요하다.

| 프로젝트 | 태그 | 발행일 | 릴리스 URL | 비고 |
|---|---|---|---|---|
| fastapi/fastapi | 0.140.0 | 2026-07-24 | https://github.com/fastapi/fastapi/releases/tag/0.140.0 | |
| **Kludex/starlette** | 1.3.1 | 2026-06-12 | https://github.com/Kludex/starlette/releases/tag/1.3.1 | `encode/starlette`에서 **이전됨** |
| **Kludex/starlette** | **1.0.0** | **2026-03-22** | https://github.com/Kludex/starlette/releases/tag/1.0.0 | 첫 stable |
| **Kludex/uvicorn** | 0.51.0 | 2026-07-08 | https://github.com/Kludex/uvicorn/releases/tag/0.51.0 | `encode/uvicorn`에서 **이전됨** |
| sqlalchemy/sqlalchemy | rel_2_0_51 | 2026-06-15 | https://github.com/sqlalchemy/sqlalchemy/releases/tag/rel_2_0_51 | |
| pydantic/pydantic | v2.13.4 | 2026-05-06 | https://github.com/pydantic/pydantic/releases/tag/v2.13.4 | |
| astral-sh/uv | 0.11.32 | 2026-07-23 | https://github.com/astral-sh/uv/releases/tag/0.11.32 | |
| astral-sh/ruff | 0.16.0 | 2026-07-23 | https://github.com/astral-sh/ruff/releases/tag/0.16.0 | |
| astral-sh/ty | 0.0.63 | 2026-07-23 | https://github.com/astral-sh/ty/releases/tag/0.0.63 | |
| facebook/pyrefly | 1.1.1 | 2026-06-18 | https://github.com/facebook/pyrefly/releases/tag/1.1.1 | |
| emmett-framework/granian | v2.7.9 | 2026-07-03 | https://github.com/emmett-framework/granian/releases/tag/v2.7.9 | |
| sysid/sse-starlette | v3.4.6 | 2026-07-20 | https://github.com/sysid/sse-starlette/releases/tag/v3.4.6 | |
| Kludex/mangum | 0.21.0 | 2026-02-01 | https://github.com/Kludex/mangum/releases/tag/0.21.0 | |
| **aws/aws-lambda-web-adapter** | v1.0.1 | 2026-05-28 | https://github.com/aws/aws-lambda-web-adapter/releases/tag/v1.0.1 | `awslabs/`에서 **이전됨**, 1.0 도달 |
| benoitc/gunicorn | 26.0.0 | 2026-05-05 | https://github.com/benoitc/gunicorn/releases/tag/26.0.0 | |
| mongodb/motor | 3.7.1 | 2025-05-14 | https://github.com/mongodb/motor/releases/tag/3.7.1 | 1년 이상 릴리스 없음 |

---

## 7. 미확인·공백 (⚠️)

> **이 절의 목적:** 아래 항목들은 **1차 소스로 확인하지 못했다.** 저술 시 단정하지 말고, 필요하면 Phase 4 fact-checker가 재조사할 표적으로 삼아라. 여기 없는 것을 "확인됐다"고 가정하지 말 것.

### 7-1. 수치·기본값을 못 찾은 것
1. ⚠️ **`SpooledTemporaryFile`의 in-memory 임계 바이트 값.** FastAPI 문서는 "up to a maximum size limit"라고만 하고 숫자를 주지 않는다[S28]. Starlette 릴리스 노트에서 파라미터명이 `max_file_size` → `spool_max_size`로 바뀐 것(0.46.0)만 확인. **책에 숫자를 쓰려면 `starlette/formparsers.py` 소스 확인 필요.**
2. ⚠️ **uvicorn `--timeout-graceful-shutdown`의 기본값.** settings 문서가 이 항목에만 "Default:" 표기를 하지 않았다[S10]. (keep-alive 5초 등 다른 타임아웃은 명시됨.) K8s grace period와 비교 서술할 때 기본값을 단정하지 말 것.
3. ⚠️ **redis-py asyncio `ConnectionPool`의 파라미터 기본값**(풀 크기 등). 풀 소유·해제 패턴만 확인.

### 7-2. 유지보수·성숙도 판단을 못 내린 것
4. ⚠️ **loguru 저장소의 현재 활동.** PyPI 0.7.3 / 2024-12-06만 확인. 커밋·이슈 미확인 → **"방치됐다"고 쓰지 말 것.**
5. ⚠️ **Hypercorn의 현재 유지보수 활동.** 마지막 릴리스 0.18.0 / 2025-11-08(8개월+ 전)만 사실.
6. ⚠️ **pybreaker의 asyncio(비-Tornado) 지원.** README의 async 서술은 `tornado.gen` 기준뿐. `call_async`가 일반 awaitable에 동작하는지는 소스 확인 필요.
7. ⚠️ **Mangum의 응답 스트리밍 지원 여부.** LWA는 확인됨(`AWS_LWA_INVOKE_MODE=response_stream`), Mangum 쪽 미조사.
8. ⚠️ **Dramatiq / RQ / Celery의 asyncio 네이티브 지원에 대한 공식 진술.** Celery 문서를 `asyncio|async/await`로 검색했으나 매칭 없음. 정황 근거는 있다 — Celery의 concurrency 옵션 목록이 "prefork, Eventlet, gevent, thread, solo"로 **asyncio 풀이 없다**[S128]. 그러나 "Celery는 async 네이티브가 아니다"를 공식 문장으로 뒷받침하지 못했다.
9. ⚠️ **Celery stable 문서와 PyPI 버전 불일치.** 문서는 "Celery version 5.5.x runs on Python 3.8–3.13"인데 PyPI 최신은 **5.6.3**(2026-03-26). 5.6.x의 지원 범위 미확인.
10. ⚠️ **httpx2 README의 "Pydantic이 stewardship 인수" 서술.** 하위 에이전트가 raw로 인용했으나 본 문서 작성자가 재확인하지 않음(§6-8 참조).
10-a. ⚠️ **`fastar>=0.9.0`이 무엇인지.** FastAPI 0.140.0의 `[standard]` extra에 새로 보이는 의존성인데 정체를 조사하지 않았다. (본 문서 작성자의 `requires_dist` 조회는 starlette/pydantic/typing-extensions만 필터링해서 이 항목을 보지 못했고, 프로덕션 담당 에이전트가 전체 목록에서 발견해 보고했다.) 참고로 0.140.0 `[standard]`의 전체 구성은 `fastapi-cli[standard]>=0.0.8`, `fastar>=0.9.0`, `httpx<1.0.0,>=0.23.0`, `jinja2>=3.1.5`, `python-multipart>=0.0.18`, `email-validator>=2.0.0`, `uvicorn[standard]>=0.12.0`, `pydantic-settings>=2.0.0`, `pydantic-extra-types>=2.0.0`.

### 7-3. 표준·권위 문장을 못 찾은 것
11. ⚠️ **"musl 때문에 Alpine에서 소스 빌드가 돈다"는 권위 있는 단일 문장.** 공식 이미지 README의 소스 빌드 언급은 **slim 문단**(컴파일러 부재)이고 alpine 문단은 **libc 런타임 호환성**만 말한다[S106]. → §5-E의 PyPI musllinux wheel 실측이 대체 근거다.
12. ⚠️ **ruff formatter가 언제 공식적으로 "stable"로 승격됐는지.** 현재 formatter 문서에 stable/beta 자기 선언 문장이 **없다**. 간접 근거만 존재: `versioning.md`가 "stable style"/preview style 이원 체계를 규정[S97]; 2023-10-24 발표 글은 "Beta … we consider the Ruff formatter production-ready". → **"현재 stable 선언됨"이라고 쓰지 말 것.**
13. ⚠️ **"IO-bound async 앱에 CPU 오토스케일링이 부적합"이라는 k8s 공식 문장.** k8s HPA 문서에 없다[S111]. 유일한 벤더 근거는 Cloud Run 문서이며 그것도 엄밀히는 **"멀티 vCPU 위 싱글스레드 앱"**에 관한 것[S116]. k8s로의 확장은 **저자 추론**으로 표시할 것.
14. ⚠️ **FastAPI lifespan이 멀티 워커/서버리스에서 워커별로 실행되는지에 대한 공식 서술.** `advanced/events` 페이지에 언급 없음[S50].
15. ⚠️ **Starlette 미들웨어의 contextvars 전파 보장에 대한 Starlette 공식 서술.** structlog 측 경고문[S61]은 확보했으나 Starlette 측 1차 문서는 못 찾음.
16. ⚠️ **uvicorn 로깅에서 "사용자 JSON/YAML dictConfig에 `disable_existing_loggers`를 빠뜨리면 uvicorn 로거가 죽는다"는 공식 문장.** 이는 uvicorn 소스 + Python `dictConfig` 기본값(True)에서 **연역한 것**이며 uvicorn이 명시한 문장이 아니다. 원 이슈 `#511`은 **CLOSED**이고 ini 경로는 이미 `disable_existing_loggers=False`로 수정됐다[S129]. → 책에 넣으려면 **실제 재현 실험을 붙일 것.**
17. ⚠️ **SQLAlchemy `AsyncSession` 기반 테스트 롤백 공식 레시피.** `session_transaction.md`와 asyncio 확장 페이지 **두 곳에는 없음**을 확인. 전수 확인은 아니므로 "**해당 두 페이지에는 없다**"로만 표현할 것.
18. ⚠️ **SQLAlchemy 2.1 GA 일정, 그리고 2.1에서 `Query` API가 실제로 제거되는지.** 2.1.0b3(2026-06-27)까지만 확인.

### 7-4. 벤더 계약을 못 확인한 것
19. ⚠️ **Railway의 `PORT` 환경변수 계약·헬스체크·scale-to-zero.** variables 레퍼런스와 public-networking 문서 모두 PORT 미언급. 확인된 건 FastAPI 가이드의 `hypercorn main:app --bind "::"` 뿐[S123].
20. ⚠️ **Render의 scale-to-zero / free 인스턴스 spin-down 동작.**
21. ⚠️ **Fly.io FastAPI 가이드가 실제 생성하는 `fly.toml` 본문과 시작 명령.** 설정 레퍼런스와 autostop 문서로 우회 확인함[S124].
22. ⚠️ **Cloud Run "CPU always allocated" 설정의 공식 문구.** `.../run/docs/configuring/services/cpu-allocation`은 **404**. container-contract의 request-based billing 서술만 확보[S115].
23. ⚠️ **FastAPI가 인용한 TechEmpower run(`runid=7464e520-...`)의 라운드 번호와 실행 시점.** techempower.com/benchmarks/는 JS SPA라 서버사이드 fetch로 해석 불가. **URL만 인용하고 라운드·날짜는 쓰지 말 것.**
24. ⚠️ **`python` 공식 이미지의 현재 기본 Debian suite (bookworm vs trixie).** README는 코드명 개념만 설명. 정황: uv 이미지 목록이 `trixie` 세대[S93].
25. ⚠️ **mypy 2.x의 breaking change 내역.** 버전 2.3.0 / 2026-07-13만 확인, 릴리스 노트 미조사.

### 7-5. 접근 실패 / 수집 한계
26. ⚠️ **원티드랩 기술 블로그(FastAPI × SQLAlchemy Session) 본문 수집 실패** — Medium 로그인 벽. 저자·발행일·인용문 미확보(부록 A-2).
27. ⚠️ **`uvicorn.dev` / `www.uvicorn.org` 직접 fetch 실패**(각각 HTTP 403, DNS 미해석). → 공식 저장소 `Kludex/uvicorn`의 `main` 브랜치 docs 소스를 인증 GitHub API로 읽어 인용했다(§8의 S10~S15 메모 참조). 동일 소스이므로 1차 자격에는 문제없다.
28. ⚠️ **`fasthx` / `fastapi-problem`의 실제 API.** PyPI 메타데이터만 확인, README·문서 미독. **코드 예제를 책에 넣으려면 추가 확인 필요.**
29. ⚠️ **htmx.org의 FastAPI 전용 공식 가이드.** htmx 문서 목차에서 찾지 못했다.
30. ⚠️ **`broadcaster` 아카이브 이후 encode 진영의 공식 대체재 안내.** 없음 — FastAPI 문서는 여전히 아카이브된 저장소를 링크한다(§1-E).
31. ⚠️ **한국 회사 엔지니어링 블로그의 최신(2024~2026) FastAPI 운영 사례.** 카카오페이 글(2022)[S9] 외에 우아한형제들·토스·네이버 D2·LINE에서 FastAPI 주제 글을 찾지 못했다. 국내 사례 보강이 필요하면 커뮤니티 리서처(C조) 결과와 대조할 것.

### 7-6. 하위 에이전트 산출물의 프로바넌스 경고 (중요)

프로덕션 담당 에이전트가 **요약 모델이 존재하지 않는 코드를 만들어낸 사례 2건**을 자체 적발하고 raw 소스로 교정했다고 보고했다 — (1) oauth2-scopes의 가짜 주석, (2) Auth0의 잘못된 import 경로 `fastapi_plugin.fast_api_client`.

→ **이 문서의 코드 스니펫 중 GitHub raw / PyPI JSON / 공식 문서 직접 fetch로 확인된 것만 신뢰하라.** 특히 아래는 본 문서 작성자가 **직접** fetch해 검증했다:
- FastAPI 보안 튜토리얼의 pyjwt·pwdlib 코드 [S1] (에이전트가 raw로 재확인 [S63])
- FastAPI server-workers·docker 명령 [S2][S3]
- Uvicorn docs 전체(deployment·settings·logging·websockets·server-behavior·docker) [S10]~[S15] — GitHub API raw
- FastAPI `applications.py` 소스 [S7] — GitHub API raw
- 전 패키지 버전·릴리스일 (§6) — PyPI JSON API + GitHub Releases API
- Starlette 1.0.0 릴리스 노트·breaking changes [S4][S5]

**렌더링 페이지 요약 경유로 들어온 코드 예시**(특히 Auth0 퀵스타트, Azure Bicep 예제, testcontainers 예제)는 **책에 싣기 전 원문 재확인 필수**.

---

## 8. 출처 목록 (URL + 발행일 + 조회일 + 신뢰성)

| # | 제목 | URL | 저자·발행/갱신일 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S1 | FastAPI 공식 튜토리얼 — OAuth2 with Password (and hashing), Bearer with JWT tokens | https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ | FastAPI 공식(tiangolo), 상시 갱신 | 2026-07-25 | 최상 (공식 1차) |
| S2 | FastAPI 공식 배포 문서 — Server Workers | https://fastapi.tiangolo.com/deployment/server-workers/ | FastAPI 공식, 상시 갱신 | 2026-07-25 | 최상 (공식 1차) |
| S3 | FastAPI 공식 배포 문서 — FastAPI in Containers (Docker) | https://fastapi.tiangolo.com/deployment/docker/ | FastAPI 공식, 상시 갱신 | 2026-07-25 | 최상 (공식 1차) |
| S4 | Starlette 1.0.0 GitHub Release | https://github.com/Kludex/starlette/releases/tag/1.0.0 | Kludex(Marcelo Trylesinski), 2026-03-22 | 2026-07-25 | 최상 (릴리스 1차) |
| S5 | Starlette 공식 Release Notes | https://www.starlette.io/release-notes/ | Starlette 공식 | 2026-07-25 | 최상 (공식 체인지로그) |
| S6 | PyPI JSON API — fastapi 0.140.0 메타데이터 (`requires_dist`) | https://pypi.org/pypi/fastapi/0.140.0/json | PyPI, 릴리스 2026-07-24 | 2026-07-25 | 최상 (패키지 인덱스 1차) |
| S7 | FastAPI 소스 `fastapi/applications.py` (GitHub Contents API) | https://github.com/fastapi/fastapi/blob/master/fastapi/applications.py | FastAPI 공식 저장소 | 2026-07-25 | 최상 (소스 1차) |
| S8 | FastAPI 0.140.0 릴리스 노트 (PR #16032 "Update docs to use uv projects by default") | https://github.com/fastapi/fastapi/releases/tag/0.140.0 | tiangolo, 2026-07-24 | 2026-07-25 | 최상 (릴리스 1차) |
| S9 | 이미지 처리를 위한 파이썬 서버 프레임워크 선정기 with Django, FastAPI, Sanic | https://tech.kakaopay.com/post/image-processing-server-framework/ | Jenson·Todd (카카오페이 데이터실), **2022-08-29** | 2026-07-25 | 최상 (회사 엔지니어링 블로그) — 단, 발행 4년 경과로 **버전 정보는 구버전**. 방법론·결론만 인용할 것 |
| S10 | Uvicorn 공식 문서 — Deployment + Settings (`docs/deployment/index.md`, `docs/settings.md`) | https://github.com/Kludex/uvicorn/blob/main/docs/deployment/index.md · https://github.com/Kludex/uvicorn/blob/main/docs/settings.md (공개 사이트: https://uvicorn.dev/deployment/ , https://uvicorn.dev/settings/) | Uvicorn 공식 저장소 `main` 브랜치 | 2026-07-25 | 최상 (공식 1차) |
| S11 | Uvicorn 공식 문서 — Concepts: WebSockets (`docs/concepts/websockets.md`) | https://github.com/Kludex/uvicorn/blob/main/docs/concepts/websockets.md | Uvicorn 공식 저장소 | 2026-07-25 | 최상 (공식 1차) |
| S12 | Uvicorn 공식 문서 — Server Behavior (`docs/server-behavior.md`) | https://github.com/Kludex/uvicorn/blob/main/docs/server-behavior.md | Uvicorn 공식 저장소 | 2026-07-25 | 최상 (공식 1차) |
| S13 | FastAPI 공식 문서 — Behind a Proxy | https://fastapi.tiangolo.com/advanced/behind-a-proxy/ | FastAPI 공식, 상시 갱신 | 2026-07-25 | 최상 (공식 1차) |
| S14 | Uvicorn 공식 문서 — Concepts: Logging (`docs/concepts/logging.md`) | https://github.com/Kludex/uvicorn/blob/main/docs/concepts/logging.md | Uvicorn 공식 저장소 | 2026-07-25 | 최상 (공식 1차) |
| S15 | Uvicorn 공식 문서 — Deployment: Dockerfile (`docs/deployment/docker.md`) | https://github.com/Kludex/uvicorn/blob/main/docs/deployment/docker.md | Uvicorn 공식 저장소 | 2026-07-25 | 최상 (공식 1차) |

> **S10~S15 수집 경위 메모:** `uvicorn.dev` / `www.uvicorn.org` 는 2026-07-25 시점 WebFetch로 접근 실패(각각 HTTP 403, DNS 미해석)했다. 그래서 **공식 저장소 `Kludex/uvicorn`의 `main` 브랜치 docs 소스를 인증된 GitHub API로 직접 읽어** 인용했다. 사이트와 저장소는 동일 소스이므로 1차 소스 자격에 문제없으나, 인용 URL은 저장소 경로로 남긴다.

### 애플리케이션 스타일 (§1)

| # | 제목 | URL | 발행/갱신 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S16 | FastAPI 공식 튜토리얼 — Server-Sent Events (SSE) | https://fastapi.tiangolo.com/tutorial/server-sent-events/ | FastAPI 공식 (기능 도입 0.135.0 / 2026-03-01) | 2026-07-25 | 최상 (공식 1차) |
| S17 | FastAPI 공식 릴리스 노트 | https://fastapi.tiangolo.com/release-notes/ | FastAPI 공식, 상시 갱신 | 2026-07-25 | 최상 (공식 체인지로그) |
| S18 | sse-starlette README (GitHub) | https://github.com/sysid/sse-starlette | sysid, 릴리스 3.4.6 / 2026-07-20 | 2026-07-25 | 최상 (저장소 1차) — 단 프록시 버퍼링 *수치*는 저자 주장(§7) |
| S19 | nginx 공식 문서 — ngx_http_proxy_module (`proxy_buffering`, `X-Accel-Buffering`) | https://nginx.org/en/docs/http/ngx_http_proxy_module.html | nginx 공식 | 2026-07-25 | 최상 (공식 1차) |
| S20 | encode/broadcaster 저장소 + README | https://github.com/encode/broadcaster | **2025-08-19 아카이브**, 마지막 push 2025-04-09 | 2026-07-25 | 최상 (저장소 1차 / GitHub API 직접 조회) |
| S21 | FastAPI 공식 문서 — WebSockets | https://fastapi.tiangolo.com/advanced/websockets/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S22 | FastAPI 공식 문서 — Templates | https://fastapi.tiangolo.com/advanced/templates/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S23 | Starlette 공식 문서 — Templates | https://starlette.dev/templates/ (구 starlette.io) | Starlette 공식 | 2026-07-25 | 최상 (공식 1차) |
| S24 | FastAPI 공식 문서 — Static Files / Frontend (`app.frontend()`) | https://fastapi.tiangolo.com/tutorial/static-files/ · https://fastapi.tiangolo.com/tutorial/frontend/ | FastAPI 공식 (기능 도입 0.138.0 / 2026-06-20) | 2026-07-25 | 최상 (공식 1차) |
| S25 | FastAPI 공식 문서 — GraphQL | https://fastapi.tiangolo.com/how-to/graphql/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S26 | Starlette 공식 문서 — GraphQL (제거 공지) | https://starlette.dev/graphql/ | Starlette 공식 (제거 시점 0.17.0 / 2021-11-04) | 2026-07-25 | 최상 (공식 1차) |
| S27 | Strawberry 공식 문서 — FastAPI Integration | https://strawberry.rocks/docs/integrations/fastapi | Strawberry 공식 (0.323.2 / 2026-07-23) | 2026-07-25 | 최상 (공식 1차) |
| S28 | FastAPI 공식 튜토리얼 — Request Files | https://fastapi.tiangolo.com/tutorial/request-files/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S29 | Starlette 공식 문서 — Requests (`form()` 한도, `UploadFile.size`, `stream()`) | https://starlette.dev/requests/ | Starlette 공식 | 2026-07-25 | 최상 (공식 1차) |
| S30 | AWS 공식 문서 — Presigned URLs (업로드) | https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html · .../using-presigned-url.html | AWS 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S31 | httpx 공식 문서 — Transports (`retries`) | https://www.python-httpx.org/advanced/transports/ | httpx 공식 (0.28.1 / 2024-12-06) | 2026-07-25 | 최상 (공식 1차) |
| S32 | httpx 공식 문서 — Timeouts | https://www.python-httpx.org/advanced/timeouts/ | httpx 공식 | 2026-07-25 | 최상 (공식 1차) |
| S33 | httpx 공식 문서 — Resource Limits | https://www.python-httpx.org/advanced/resource-limits/ | httpx 공식 | 2026-07-25 | 최상 (공식 1차) |
| S34 | pybreaker README | https://github.com/danielfm/pybreaker | 1.4.1 / 2025-09-21 | 2026-07-25 | 최상 (저장소 1차) |
| S35 | **RFC 9457** — Problem Details for HTTP APIs | https://www.rfc-editor.org/rfc/rfc9457.html | IETF, **2023-07** (RFC 7807 obsolete) | 2026-07-25 | 최상 (표준 1차) |
| S36 | FastAPI 공식 튜토리얼 — Handling Errors | https://fastapi.tiangolo.com/tutorial/handling-errors/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S37 | fastapi-pagination README | https://github.com/uriyyo/fastapi-pagination | 0.15.15 / 2026-06-16 | 2026-07-25 | 중 (서드파티 저장소) |

### 데이터 계층 (§2)

| # | 제목 | URL | 발행/갱신 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S38 | SQLAlchemy 2.0 ORM Quickstart | https://docs.sqlalchemy.org/en/20/orm/quickstart.html | Release 2.0.51 / 2026-06-15 (문서 생성 2026-07-23) | 2026-07-25 | 최상 (공식 1차) |
| S39 | SQLAlchemy 2.1 문서 (베타 채널) | https://docs.sqlalchemy.org/en/21/ | **2.1.0b3 / 2026-06-27, beta release** | 2026-07-25 | 최상 (공식 1차) |
| S40 | SQLAlchemy 2.0 마이그레이션 가이드 (`Query` 레거시화) | https://docs.sqlalchemy.org/en/20/changelog/migration_20.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S41 | SQLAlchemy — Mapping API (`declarative_base()` supersede) | https://docs.sqlalchemy.org/en/20/orm/mapping_api.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S42 | SQLAlchemy — ORM Query Guide: SELECT (`scalars()`) | https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S43 | SQLAlchemy — Asyncio 확장 | https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S44 | SQLAlchemy — Error Reference (`MissingGreenlet`) | https://docs.sqlalchemy.org/en/20/errors.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S45 | SQLAlchemy Dialects — PostgreSQL / SQLite / MySQL | https://docs.sqlalchemy.org/en/20/dialects/postgresql.html (외 2) | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S46 | asyncpg README | https://github.com/MagicStack/asyncpg | 0.31.0 / 2025-11-24 | 2026-07-25 | 최상 (저장소 1차) — ⚠️ "5x faster" 벤치마크는 **2023-06 자체 측정** |
| S47 | SQLAlchemy — Connection Pooling | https://docs.sqlalchemy.org/en/20/core/pooling.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S48 | FastAPI 공식 튜토리얼 — SQL (Relational) Databases | https://fastapi.tiangolo.com/tutorial/sql-databases/ | FastAPI 공식 (SQLModel 기반, **동기 세션**) | 2026-07-25 | 최상 (공식 1차) |
| S49 | SQLAlchemy — Session Basics (스레드 안전성) | https://docs.sqlalchemy.org/en/20/orm/session_basics.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S50 | FastAPI 공식 문서 — Lifespan Events | https://fastapi.tiangolo.com/advanced/events/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S51 | Alembic 튜토리얼 (`list_templates`) | https://alembic.sqlalchemy.org/en/latest/tutorial.html | Alembic 1.18.5 | 2026-07-25 | 최상 (공식 1차) |
| S52 | Alembic Cookbook — Using Asyncio with Alembic | https://alembic.sqlalchemy.org/en/latest/cookbook.html | Alembic 공식 | 2026-07-25 | 최상 (공식 1차) |
| S53 | Alembic — Autogenerate (감지 한계) | https://alembic.sqlalchemy.org/en/latest/autogenerate.html | Alembic 공식 | 2026-07-25 | 최상 (공식 1차) |
| S54 | SQLAlchemy — Relationship Loading Techniques | https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html | SQLAlchemy 공식 | 2026-07-25 | 최상 (공식 1차) |
| S55 | SQLModel 공식 사이트 + `fastapi/sqlmodel` 저장소·소스 | https://sqlmodel.tiangolo.com/ · https://github.com/fastapi/sqlmodel | 0.0.39 / 2026-06-25, 마지막 push 2026-07-23 | 2026-07-25 | 최상 (공식 1차 + 소스) |
| S56 | redis-py 공식 문서 — asyncio 예제 | https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html | redis-py (PyPI 8.0.1 / 2026-06-23; 문서 페이지는 8.0.0 표기) | 2026-07-25 | 최상 (공식 1차) |
| S57 | aioredis-py 저장소 (아카이브·이관 공지) | https://github.com/aio-libs-abandoned/aioredis-py | archived, 마지막 push 2023-02-20 | 2026-07-25 | 최상 (저장소 1차) |
| S58 | MongoDB 공식 — Migrate from Motor to PyMongo Async | https://www.mongodb.com/docs/languages/python/pymongo-driver/current/reference/migration/ | MongoDB 공식 | 2026-07-25 | 최상 (벤더 1차) — ⚠️ deprecation 시제가 stale |
| S59 | Motor README (deprecation 타임라인) | https://github.com/mongodb/motor | 3.7.1 / 2025-05-14 | 2026-07-25 | 최상 (저장소 1차) |
| S60 | Beanie 공식 문서 + 저장소 | https://beanie-odm.dev/ · https://github.com/BeanieODM/beanie | 2.1.0 / 2026-03-26 | 2026-07-25 | 최상 (공식 1차) |

### 프로덕션 (§3)

| # | 제목 | URL | 발행/갱신 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S61 | structlog 공식 문서 — Context Variables (FastAPI 경고) | https://www.structlog.org/en/stable/contextvars.html | structlog 26.1.0 / 2026-06-06 | 2026-07-25 | 최상 (공식 1차) |
| S62 | asgi-correlation-id 저장소 | https://github.com/snok/asgi-correlation-id | 5.0.1 / 2026-06-09 (MIT) | 2026-07-25 | 최상 (저장소 1차) |
| S63 | FastAPI 보안 튜토리얼 **원문 마크다운 + 예제 소스** | https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md · `docs_src/security/tutorial004_an_py310.py` | FastAPI 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S64 | pwdlib README | https://github.com/frankie567/pwdlib | 0.3.0 / 2025-10-25 | 2026-07-25 | 최상 (저장소 1차) |
| S65 | GitHub Issue `pyca/bcrypt#684` — bcrypt 4.1.x + passlib | https://github.com/pyca/bcrypt/issues/684 | 2023-11-29 개설 | 2026-07-25 | 최상 (메인테이너 발언 1차) |
| S66 | GitHub Issue `pyca/bcrypt#1079` — passlib 1.7.4 + bcrypt 5.0.0 | https://github.com/pyca/bcrypt/issues/1079 | 2025-09-26 개설 | 2026-07-25 | 중 (이슈 보고, 렌더링 경유) |
| S67 | FastAPI 공식 문서 — OAuth2 scopes | https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/ (+ `docs_src/security/tutorial005_an_py310.py`) | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차 + 소스) |
| S68 | Starlette 공식 문서 — Middleware (`SessionMiddleware`) | https://github.com/Kludex/starlette/blob/master/docs/middleware.md | Starlette 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S69 | Auth0 — FastAPI 백엔드 퀵스타트 + `auth0-fastapi-api` | https://auth0.com/docs/quickstart/backend/fastapi · https://github.com/auth0/auth0-fastapi-api | SDK **1.0.0b7 / 2026-04-09 (beta)** | 2026-07-25 | 최상(벤더) — ⚠️ 퀵스타트 코드는 렌더링 경유(§7-6) |
| S70 | Keycloak 공식 — Securing Applications 개요 | https://www.keycloak.org/securing-apps/overview | Keycloak 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S71 | Authlib 공식 문서 — FastAPI / Starlette Integration | https://docs.authlib.org/en/latest/oauth2/client/web/fastapi.html | Authlib 1.7.2 / 2026-05-06 | 2026-07-25 | 최상 (공식 1차) |
| S72 | pydantic-settings 공식 문서 | https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/ (구 `docs.pydantic.dev/...` → **301**) | 2.14.2 / 2026-06-19 | 2026-07-25 | 최상 (공식 1차) |
| S73 | pydantic 공식 문서 — Types (`SecretStr`) | https://pydantic.dev/docs/validation/latest/api/pydantic/types/ | pydantic 2.13.4 | 2026-07-25 | 최상 (공식 1차) |
| S74 | FastAPI 공식 문서 — Settings and Environment Variables | https://fastapi.tiangolo.com/advanced/settings/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S75 | OpenTelemetry 공식 — Python (안정성 상태표) | https://opentelemetry.io/docs/languages/python/ | OTel 공식 (API/SDK 1.44.0 / 2026-07-16) | 2026-07-25 | 최상 (공식 1차) |
| S76 | OTel Python contrib — FastAPI Instrumentation | https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html | 0.65b0 / 2026-07-16 | 2026-07-25 | 최상 (공식 1차) |
| S77 | OpenTelemetry 공식 — Zero-code instrumentation (Python) | https://opentelemetry.io/docs/zero-code/python/ | OTel 공식 | 2026-07-25 | 최상 (공식 1차) |
| S78 | prometheus_client 공식 — Multiprocess Mode | https://prometheus.github.io/client_python/multiprocess/ | 0.26.0 / 2026-07-24 | 2026-07-25 | 최상 (공식 1차) |
| S79 | prometheus-fastapi-instrumentator 저장소 | https://github.com/trallnag/prometheus-fastapi-instrumentator | 8.0.2 / 2026-06-23 (ISC) | 2026-07-25 | 최상 (저장소 1차) |
| S80 | FastAPI 공식 튜토리얼 — Testing | https://fastapi.tiangolo.com/tutorial/testing/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S81 | FastAPI 공식 문서 — Async Tests **원문 + 예제 소스** | https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/async-tests.md · `docs_src/async_tests/app_a_py310/test_main.py` | FastAPI 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S82 | AnyIO 공식 문서 — Testing (`anyio_backend`) | https://anyio.readthedocs.io/en/stable/testing.html | anyio 4.14.2 / 2026-07-12 | 2026-07-25 | 최상 (공식 1차) |
| S83 | pytest-asyncio 공식 문서 — Configuration + Changelog | https://pytest-asyncio.readthedocs.io/en/stable/reference/configuration.html | 1.4.0 / 2026-05-26 (**1.0.0에서 `event_loop` fixture 제거**) | 2026-07-25 | 최상 (공식 1차) |
| S84 | FastAPI 공식 문서 — Testing Dependencies (`dependency_overrides`) | https://fastapi.tiangolo.com/advanced/testing-dependencies/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S85 | SQLAlchemy — Session Transaction: Joining into an External Transaction | https://docs.sqlalchemy.org/en/20/orm/session_transaction.html | SQLAlchemy 2.0.51 | 2026-07-25 | 최상 (공식 1차) |
| S86 | testcontainers-python 공식 문서 | https://testcontainers-python.readthedocs.io/en/latest/ | 4.15.0 / 2026-07-24 | 2026-07-25 | 최상(공식) — ⚠️ 문서 예제는 구버전 흔적(§7) |
| S87 | FastAPI `index.md` **원문** (성능 주장 + 각주) | https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md | FastAPI 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S88 | **FastAPI 공식 — Benchmarks (자기 반박 페이지)** | https://fastapi.tiangolo.com/benchmarks/ | FastAPI 공식 | 2026-07-25 | 최상 (공식 1차) |
| S89 | TechEmpower FrameworkBenchmarks Wiki — Basic Concepts / Expected Questions / About | https://github.com/TechEmpower/FrameworkBenchmarks/wiki | TechEmpower 공식 wiki (git clone으로 원문 취득) | 2026-07-25 | 최상 (공식 1차) |

### CI/CD (§4)

| # | 제목 | URL | 발행/갱신 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S90 | uv 공식 문서 — Project Layout (`uv.lock`) | https://docs.astral.sh/uv/concepts/projects/layout/ | uv 0.11.32 / 2026-07-23 | 2026-07-25 | 최상 (공식 1차) |
| S91 | **PEP 751** — pylock.toml 락파일 표준 | https://peps.python.org/pep-0751/ | Brett Cannon, **Status: Final, Resolution 2025-03-31** | 2026-07-25 | 최상 (표준 1차) |
| S92 | uv 공식 문서 — Locking and Syncing (`--locked`/`--frozen`/`--no-dev`) | https://docs.astral.sh/uv/concepts/projects/sync/ | uv 공식 | 2026-07-25 | 최상 (공식 1차) |
| S93 | uv 공식 Docker 통합 가이드 **원문** | https://github.com/astral-sh/uv/blob/main/docs/guides/integration/docker.md (렌더: https://docs.astral.sh/uv/guides/integration/docker/) | uv 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S94 | Poetry 공식 문서 — pyproject.toml / Basic Usage | https://python-poetry.org/docs/pyproject/ · .../basic-usage/ | Poetry 2.4.1 / 2026-05-09 | 2026-07-25 | 최상 (공식 1차) |
| S95 | pip-tools README + 저장소 메타 | https://github.com/jazzband/pip-tools | 7.6.0 / 2026-07-18, 마지막 push 2026-07-24 | 2026-07-25 | 최상 (저장소 1차, raw) |
| S96 | uv 공식 문서 — pip 인터페이스 | https://docs.astral.sh/uv/pip/ | uv 공식 | 2026-07-25 | 최상 (공식 1차) |
| S97 | ruff 공식 문서 — Formatter + Versioning **원문** | https://github.com/astral-sh/ruff/blob/main/docs/formatter.md · `docs/versioning.md` | ruff 0.16.0 / 2026-07-23 | 2026-07-25 | 최상 (소스 1차, raw) |
| S98 | **Astral `ty` README** ("currently in beta", 0.0.x) | https://github.com/astral-sh/ty | 0.0.63 / 2026-07-23 | 2026-07-25 | 최상 (저장소 1차, raw) |
| S99 | **Meta `pyrefly` README** ("status is stable", Instagram 2000만 줄) | https://github.com/facebook/pyrefly | 1.1.1 / 2026-06-18 | 2026-07-25 | 최상 (저장소 1차, raw) |
| S100 | PyPI `pyright` 패키지 메타 ("Command line wrapper for pyright") | https://pypi.org/project/pyright/1.1.411/ | 1.1.411 / 2026-06-25 | 2026-07-25 | 최상 (패키지 인덱스 1차) |
| S101 | `astral-sh/setup-uv` README + Releases | https://github.com/astral-sh/setup-uv | **v9.0.0 / 2026-07-21** | 2026-07-25 | 최상 (저장소 1차) |
| S102 | uv 공식 GitHub Actions 연동 가이드 | https://docs.astral.sh/uv/guides/integration/github/ | uv 공식 — ⚠️ 예제가 setup-uv **v8.1.0**에 정체 | 2026-07-25 | 최상 (공식 1차) |
| S103 | `actions/setup-python` `action.yml` + README | https://github.com/actions/setup-python | **v7.0.0 / 2026-07-20** | 2026-07-25 | 최상 (저장소 1차, raw) |
| S104 | **Python 공식 devguide — Status of Python versions** | https://devguide.python.org/versions/ | python.org 공식 | 2026-07-25 | 최상 (공식 1차) |

### 배포 (§5)

| # | 제목 | URL | 발행/갱신 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S105 | Uvicorn 소스 `uvicorn/workers.py` (DeprecationWarning) | https://github.com/Kludex/uvicorn/blob/master/uvicorn/workers.py | Uvicorn 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S106 | Docker 공식 이미지 `python` README (slim / alpine 문단) | https://github.com/docker-library/docs/blob/master/python/README.md (= https://hub.docker.com/_/python) | docker-library 공식 | 2026-07-25 | 최상 (소스 1차, raw) |
| S107 | **PEP 656** — musllinux 플랫폼 태그 | https://peps.python.org/pep-0656/ | **Status: Final**, Created 2021-03-17 | 2026-07-25 | 최상 (표준 1차) |
| S108 | `astral-sh/uv-docker-example` Dockerfile (비루트 유저) | https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile | Astral 공식 예제 (uv 문서가 best practice로 링크) | 2026-07-25 | 최상 (소스 1차, raw) |
| S109 | Kubernetes 공식 — Probes (liveness/readiness/startup) | https://kubernetes.io/docs/concepts/workloads/pods/probes/ | k8s 공식 | 2026-07-25 | 최상 (공식 1차) |
| S110 | Kubernetes 공식 — Pod Lifecycle: Pod Termination **원문** | https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/workloads/pods/pod-lifecycle.md (렌더: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) | k8s 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S111 | Kubernetes 공식 — Horizontal Pod Autoscaling | https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ | k8s 공식 | 2026-07-25 | 최상 (공식 1차) |
| S112 | **AWS Lambda 공식 — Runtimes (지원 Python 표)** | https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html | AWS 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S113 | AWS Lambda 공식 — Quotas | https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html | AWS 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S114 | **AWS Lambda 공식 — Concurrency** | https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html | AWS 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S115 | Google Cloud Run 공식 — Container runtime contract | https://docs.cloud.google.com/run/docs/container-contract (구 `cloud.google.com/...` → **301**) | Google 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S116 | Google Cloud Run 공식 — About concurrency | https://docs.cloud.google.com/run/docs/about-concurrency | Google 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S117 | Google Cloud Run 공식 — Minimum instances | https://docs.cloud.google.com/run/docs/configuring/min-instances | Google 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S118 | Google Cloud 공식 — Buildpacks builders / Python | https://docs.cloud.google.com/docs/buildpacks/builders · .../buildpacks/python | Google 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S119 | Azure Container Apps 공식 — Set scaling rules | https://learn.microsoft.com/en-us/azure/container-apps/scale-app | Microsoft 공식, `ms.date: 2026-05-19` | 2026-07-25 | 최상(벤더) — ⚠️ Bicep 예제에 min/max 반전 오류 |
| S120 | `Kludex/mangum` 저장소 (릴리스·커밋 이력) | https://github.com/Kludex/mangum | 0.21.0 / 2026-02-01, 마지막 push 2026-05-31 | 2026-07-25 | 최상 (저장소 1차, GitHub API) |
| S121 | **AWS Lambda Web Adapter** (저장소 이전 + v1.0.1) | https://github.com/aws/aws-lambda-web-adapter (구 `awslabs/`) | **v1.0.1 / 2026-05-28** | 2026-07-25 | 최상 (AWS 공식 저장소) |
| S122 | Render 공식 — Deploy FastAPI + Web Services | https://render.com/docs/deploy-fastapi · https://render.com/docs/web-services | Render 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S123 | Railway 공식 — FastAPI 가이드 | https://docs.railway.com/guides/fastapi | Railway 공식 (**Hypercorn 사용**) | 2026-07-25 | 최상 (벤더 1차) |
| S124 | Fly.io 공식 — 설정 레퍼런스 + autostop/autostart | https://fly.io/docs/reference/configuration/ · https://fly.io/docs/launch/autostop-autostart/ | Fly.io 공식 | 2026-07-25 | 최상 (벤더 1차) |
| S125 | Granian README | https://github.com/emmett-framework/granian | 2.7.9 / 2026-07-03 | 2026-07-25 | 최상 (저장소 1차, raw) |
| S126 | Hypercorn README | https://github.com/pgjones/hypercorn | 0.18.0 / 2025-11-08 | 2026-07-25 | 최상 (저장소 1차, raw) |
| S127 | Uvicorn 공식 문서 — Installation (`[standard]` 구성) | https://github.com/Kludex/uvicorn/blob/master/docs/installation.md | Uvicorn 공식 저장소 | 2026-07-25 | 최상 (소스 1차, raw) |
| S128 | Celery 공식 문서 — Introduction (concurrency 옵션) | https://docs.celeryq.dev/en/stable/getting-started/introduction.html | Celery 공식 (⚠️ 문서 5.5.x vs PyPI 5.6.3 불일치) | 2026-07-25 | 최상(공식) — §7-2 참조 |
| S129 | GitHub Issue `uvicorn#511` — "[BUG] Using --log-config disables uvicorn loggers" | https://github.com/Kludex/uvicorn/issues/511 | 2019-12-04 개설, **CLOSED** | 2026-07-25 | 최상 (메인테이너 발언 1차) |

### 추가 (§1-A)

| # | 제목 | URL | 발행/갱신 | 조회일 | 신뢰성 |
|---|---|---|---|---|---|
| S130 | Starlette 공식 문서 — WebSockets (`WebSocket` 객체 API 정본) | https://github.com/Kludex/starlette/blob/master/docs/websockets.md (렌더: https://starlette.dev/websockets/) | Starlette 공식 저장소 `master` | 2026-07-25 | 최상 (소스 1차, GitHub API raw) |
| S131 | Starlette 공식 문서 — Exceptions (`WebSocketException`) | https://starlette.dev/exceptions/ | Starlette 공식 | 2026-07-25 | 최상 (공식 1차) |

---

## 9. 저술 시 우선 활용 권고 (B조 관점)

리서치 총량이 크므로, **책의 차별성을 만드는 순서**를 표시해 둔다.

**1순위 — 이 책만 할 수 있는 이야기 (전부 1차 소스로 확정됨)**
- §0의 통념 교정 5가지 (특히 **PyJWT+pwdlib**, **gunicorn 부재**)
- §3-L 성능 신화 해체 3단 콤보: FastAPI 자신의 "cannot be faster than Starlette"[S88] + TechEmpower의 "nothing beats conducting performance tests yourself"[S89] + 카카오페이의 "요청이 크면 차이 없다"[S9]
- §5-J **Lambda vs Cloud Run의 정반대 async 경제학** (사실/추론 분리 서술 필수)
- §2-E **공식 SQL 튜토리얼이 동기라는 반전** — "FastAPI = async" 기대를 깨는 훅
- §1-E **공식 문서가 아카이브된 라이브러리를 아직 링크한다**(broadcaster)

**2순위 — 실무 함정 (독자가 반드시 밟는 것)**
- §1-I httpx `retries`는 **연결 실패만** 재시도
- §4-C `actions/setup-python`의 `cache:`가 **uv 미지원**
- §3-A uvicorn 로거의 `propagate: False`
- §2-F Alembic autogenerate가 **rename을 add+drop으로** 처리 (데이터 손실)
- §1-G Strawberry에서 `sync def`가 **워커 전체를 블록**
- §3-J prometheus_client 멀티프로세스 제약 → §5-A 워커 1개 권장과 연결

**3순위 — 정확도로 신뢰를 사는 디테일**
- §3-G passlib 사건 A/B 구분
- §5-E Alpine 통념의 절반만 맞음 (musllinux 실측)
- §5-F K8s 엔드포인트 제거 "경합"의 정확한 서술
- §4-B `ty`(beta) vs `pyrefly`(stable) 역전

**저술 시 절대 규칙**
1. 버전은 **§6 표만** 사용하고 `"{버전}/2026-07 기준"` 형태로 못 박는다.
2. §7의 항목은 **단정하지 않는다.**
3. 벤치마크 수치는 **측정 조건과 출처를 반드시 병기**한다(카카오페이 26배, asyncpg 5x, FastAPI 200~300% 전부 해당).
4. §7-6의 프로바넌스 경고 — 렌더링 경유 코드는 원문 재확인 후 게재.

---

## 부록 A. 한국 회사 엔지니어링 블로그 — 실무자 목소리

> 대상 독자가 한국 개발자이므로 국내 1차 경험담을 확보했다. **버전·API 정보는 발행 시점 기준이라 낡았을 수 있으니 §6 표로 덮어쓸 것.** 여기서 가치 있는 건 *판단 근거와 방법론*이다.

### A-1. 카카오페이 — 프레임워크 선정기 [S9]

- **저자·소속:** Jenson, Todd (카카오페이 데이터실) / **발행 2022-08-29** (조회 2026-07-25)
- **맥락:** ML 엔지니어가 이미지 처리 서버를 만들며 Django(DRF)·FastAPI·Sanic을 4개 팩터(안정성·성능·생산성·생태계)로 비교하고 **FastAPI를 최종 선정**한 기록.
- **측정 조건 (수치를 옮길 때 반드시 병기):** 클라이언트 AWS EC2 `m5.2xlarge`에서 **Locust**, 요청 데이터 **약 400KB 이미지**, Response Timeout **3,000ms**, 서버 인스턴스 8개.
  - CPU 2코어·512 동시사용자: DRF RPS ~130(타임아웃 다수) / FastAPI ~160 / Sanic ~160
  - CPU 8코어·1,024 동시사용자: 순위 Sanic > FastAPI > DRF, 셋 다 목표 RPS 달성
  - 24시간 Endurance(8코어·1,024 동시사용자): **세 프레임워크 모두 안정적**
- **이 책에 가장 중요한 문장 — "프레임워크 성능 신화"의 해독제:**
  > "요청의 크기가 큰 경우 서버 프레임워크 성능 차이는 유의미하게 나지 않는다는 결론을 도출했습니다."
  > "세 프레임워크 모두 안정적으로 응답하며 서비스가 이슈없이 유지되는 것을 확인하였습니다."
- 생산성 근거로 인용된 수치:
  > "pydantic이 drf serializer보다 역직렬화 속도가 약 26배 빨랐습니다."

  ⚠️ 이 26배는 **카카오페이 자체 측정치(2022)**이며 직렬화 단독 마이크로벤치다. 책에 옮긴다면 "카카오페이가 2022년 자체 측정한 값" 조건을 반드시 붙일 것 — 일반화 금지.
- **관련 섹션:** 프로덕션 관심사(성능·벤치마크 해석), 도입 의사결정 챕터의 오프닝 사례.

### A-2. 원티드랩 — FastAPI에서 SQLAlchemy Session 다루는 방법

- URL: https://medium.com/wantedjobs/fastapi에서-sqlalchemy-session-다루는-방법-118150b87efa (원티드랩 기술 블로그 / Medium)
- 검색 스니펫상 "비동기 프레임워크에 SQLAlchemy를 올바르게 사용하기 위한 트러블슈팅 → 최종 적용 과정 → 마이그레이션 조사"를 단계별로 기술한 글로 확인됨.
- ⚠️ **본문 수집 실패** — Medium 로그인 벽으로 WebFetch가 네비게이션 요소만 반환(2026-07-25 시도). 저자·발행일·인용문 미확보. §7 참조.
- **관련 섹션:** 데이터 계층(요청 스코프 세션). 사용하려면 본문 재확보 필요.
