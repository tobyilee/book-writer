# 9장. API 너머 — 화면을 붙이고, 다른 서비스와 말하기

여덟 장을 지나오는 동안 `tracker`가 바깥으로 내보낸 것은 전부 JSON이었다. 조회 응답도, 3장에서 정한 `ErrorResponse`도, 7장의 실시간 채널조차 결국 JSON을 밀어내는 통로였다.

그런데 실무의 웹 애플리케이션이 전부 그렇게 생기지는 않았다. 운영팀은 브라우저에서 바로 여는 관리자 화면을 원한다. 모바일 팀은 화면마다 필요한 필드가 달라 응답을 자기가 고르고 싶어 한다. 그리고 이슈 검색은 사내 검색 서비스가 갖고 있다.

앞의 둘은 우리 앱이 무엇을 보여줄 것인가의 문제이고, 마지막 하나는 누구에게 말을 걸 것인가의 문제다. 여기서 할 일은 각 방향을 끝까지 파는 것이 아니라, 첫걸음에서 무엇을 밟게 되는지 표시해두는 쪽이다.

## 화면 하나를 서버가 그리려면

서버 렌더링부터 보자. 컨트롤러가 뷰 이름을 돌려주면 뷰 리졸버가 Thymeleaf나 JSP 템플릿을 찾아주던 층, Express라면 EJS를 걸어두던 자리 — 그 층은 어디로 갔을까? 여기엔 아예 없다. 경로 함수는 뷰 이름이 아니라 **렌더링 결과 객체를 직접 만들어 돌려준다.** 준비물은 정적 파일 마운트 하나와 템플릿 객체 하나뿐이고, 설치는 필요 없다 — `fastapi[standard]`가 jinja2를 함께 끌어온다.

```python
# src/tracker/main.py
from pathlib import Path

from fastapi.staticfiles import StaticFiles

# ...(4장, 생략)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
```

> **📐 저자 설계 —** 아래 관리자 화면의 배선은 FastAPI 공식 권장이 아니라, `tracker`의 모듈 레이아웃에 맞춰 이 책이 정한 한 가지 안이다.

```python
# src/tracker/api/admin.py
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from tracker.deps import IssueServiceDep

router = APIRouter(prefix="/admin", tags=["admin"])

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/issues", response_class=HTMLResponse)
async def issue_board(request: Request, service: IssueServiceDep):
    issues = await service.list_open_issues()
    return templates.TemplateResponse(
        request=request, name="issue_board.html", context={"issues": issues}
    )
```

화면이 쓸 조회는 아직 없다. 6장이 정한 대로 쿼리는 리포지터리가 갖고 서비스는 도메인 이름만 준다.

```python
# src/tracker/repositories/issue.py (9장에서 추가)
from tracker.models.issue import Issue, IssueStatus

# ...(6장, 생략)

    async def list_open(self, limit: int, offset: int) -> list[Issue]:
        stmt = (
            select(Issue)
            .where(Issue.status == IssueStatus.open)
            .order_by(Issue.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(await self.session.scalars(stmt))
```

```python
# src/tracker/services/issue.py (9장에서 추가)
    async def list_open_issues(self, limit: int = 50, offset: int = 0) -> list[Issue]:
        return await self.issues.list_open(limit, offset)
```

이 절의 지뢰는 `TemplateResponse`의 **인자 순서**다. 공식 문서가 직접 달아둔 주석은 이렇게 읽힌다. *"Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter."* 인터넷에 널린 `templates.TemplateResponse("item.html", {"request": request})` 형태는 옛 시그니처다.[^9-1]

보통은 "구식 예제이니 주의하라"로 끝날 이야기인데, 한 칸 더 나쁘다. **Starlette 1.0.0(2026-03-22)이 옛 시그니처를 완전히 제거했다.** 이 책이 전제하는 스택은 Starlette 1.3.1 / 2026-06 기준이니, 1.x를 물어온 환경에서는 옛 형태가 경고를 내며 도는 게 아니라 그냥 **동작하지 않는다.** 4장에서 본 그대로다 — 핀 하한은 아직 `starlette>=0.46.0`이라, 락파일에 0.4x가 들어왔다면 같은 코드가 경고만 낼 수도 있다.

두 번째로 기억할 것은 `request`가 선택 사항이 아니라는 점이다. Starlette 문서가 굵게 못 박는다 — *"Note that the incoming request instance must be included as part of the template context."* 대가로 템플릿 안에서 `url_for('read_item', id=id)`처럼 경로 함수 이름으로 URL을 만들 수 있고, 정적 파일도 `url_for('static', path='/styles.css')`로 참조된다.

## 조각으로 돌려주기

이슈 목록이 뜨고 각 행에 상태를 바꾸는 버튼이 있다고 하자. 페이지 전체를 다시 그릴 이유는 없다 — 바뀐 것은 행 하나다. 자바스크립트로 JSON을 받아 DOM을 갱신하는 쪽이 하나, 서버가 HTML 조각을 돌려주고 브라우저가 그 자리에 끼워 넣는 쪽이 하나다. 후자를 위해 만들어진 것이 HTMX다.

```html
<!-- src/tracker/templates/issue_row.html -->
<tr id="issue-{{ issue.id }}">
  <td>{{ issue.title }}</td>
  <td>{{ issue.status }}</td>
  <td>
    <button hx-post="/admin/issues/{{ issue.id }}/resolve"
            hx-target="#issue-{{ issue.id }}"
            hx-swap="outerHTML">해결</button>
  </td>
</tr>
```

`hx-post`는 그 URL로 POST를 보내고, `hx-target`은 바꿔치기할 요소를, `hx-swap`은 바꿔 끼우는 방식을 정한다.[^9-2] 서버 입장에서 달라지는 것은 하나다. **응답이 JSON이 아니라 HTML 조각이어야 한다.**

엔드포인트를 두 벌 만들 필요는 없다. HTMX가 보내는 요청에는 `HX-Request` 헤더가 항상 `true`로 붙어서,[^9-2] 이 헤더 하나로 한 경로에서 갈라 쓸 수 있다. 파라미터를 `hx_request`로 적어도 되는 것은 `Header`가 *"by default ... convert the parameter names characters from underscore (`_`) to hyphen (`-`)"* 하기 때문이다.[^9-6]

> **📐 저자 설계 —** 아래 분기는 HTMX·FastAPI 조합에 대한 공식 가이드가 아니다. 확인된 것은 헤더의 존재와 의미뿐이고, 그것을 한 경로에서 쓰는 방식은 이 책이 고른 한 가지 배치다.

```python
# src/tracker/api/admin.py
from typing import Annotated

from fastapi import Header

from tracker.deps import EventBusDep
from tracker.models.issue import IssueStatus

@router.post("/issues/{issue_id}/resolve", response_class=HTMLResponse)
async def resolve_issue(
    request: Request,
    issue_id: int,
    service: IssueServiceDep,
    events: EventBusDep,
    hx_request: Annotated[str | None, Header()] = None,
):
    issue = await service.change_status(issue_id, IssueStatus.resolved, events)
    name = "issue_row.html" if hx_request else "issue_board.html"
    return templates.TemplateResponse(
        request=request, name=name, context={"issue": issue}
    )
```

`events`는 7장이 정한 시그니처를 따르는 것이다. 덕분에 관리자가 버튼을 누르면 그 변경이 7장의 채널로도 발행된다 — 화면 하나를 붙였을 뿐인데 실시간 알림이 딸려 온다.

대가는 분명하다. **화면의 모양이 서버 라우터 안으로 들어온다.** 어느 조각이 어느 요소를 대체하는지가 파이썬 조건문에 적히면, 프론트엔드 변경이 백엔드 배포를 요구한다. 화면을 고치는 사람이 당신이 아니라면 이 결합은 곧 두 팀의 일정 결합이다.

7장의 SSE와 헷갈리기 쉬우니 정리하자. 셋은 갱신을 누가 시작하느냐에서 갈린다.

| 방식 | 갱신을 시작하는 쪽 | 서버가 돌려주는 것 | 화면 상태가 사는 곳 |
|---|---|---|---|
| HTMX 부분 갱신 | 클라이언트(사용자 조작) | HTML 조각 | 서버 |
| SSE (7장) | 서버(이벤트 발생) | 이벤트 스트림 | 서버와 브라우저가 나눠 가짐 |
| SPA | 클라이언트(코드) | JSON | 브라우저 |

섞어도 된다. 방금 본 코드가 그 모양이다 — 버튼 조작은 HTMX로 받고, 남이 바꾼 이슈는 SSE로 밀려 들어온다. 다만 같은 행을 두 경로가 갱신하므로 어느 쪽이 최종 승자인지는 정해두어야 한다.

## SPA를 얹을 때

세 번째 길은 프론트엔드를 별도 프로젝트로 빌드해 결과물을 서빙하는 것이다. 디렉터리 하나 마운트하면 끝날 것 같지만 **히스토리 폴백**에서 걸린다. `/admin/issues/42`를 주소창에 직접 입력하면 그 경로의 파일이 디스크에 없다 — 클라이언트 라우팅이 처리할 경로인데 서버가 먼저 404를 낸다.

FastAPI는 0.138.0(2026-06)에서 이 일을 전담하는 메서드를 추가했다. 시그니처는 `frontend(path, directory, fallback="auto", check_dir=True)`이고, 내부에서 `StaticFiles`를 쓰되 프론트엔드용 처리를 얹은 형태다. `StaticFiles` 문서도 이제 맨 위에서 안내한다. *"If you need to host a frontend, use `app.frontend()` instead."*[^9-7]

눈여겨볼 것이 둘이다. 첫째, 경로 연산을 먼저 확인하고 매칭되는 것이 없을 때만 프론트엔드 파일을 본다. 둘째, 폴백은 `Accept: text/html`(또는 `application/xhtml+xml`)이 붙은 GET·HEAD 요청에만 적용된다. 없는 자바스크립트나 이미지에 `index.html`을 200으로 돌려주는 흔한 사고가 이래서 막힌다 — 없는 자원은 여전히 404다. 그리고 0.139.0(2026-07)부터는 이 응답에도 의존성을 걸 수 있어, 쿠키 인증으로 정적 자산까지 보호할 수 있다.[^9-7]

다만 FastAPI 0.140 / 2026-07 기준으로도 여전히 새 표면이니, 세부 동작은 공식 문서를 함께 확인하자.

여기까지 답한 질문은 하나였다. 이 앱이 **사람**에게 무엇을 보여줄 것인가. 상대가 **다른 서비스**로 바뀌면 그 전제가 무너진다. 상대는 자기 스키마를 갖고 오고, 느려지거나 죽는 일에 우리는 아무 권한이 없다.

## 타입 선언이 스키마가 되는 세 번째 방식

응답을 자기가 고르고 싶다는 모바일 팀의 요구 — GraphQL이 답하려는 문제다. FastAPI 공식 문서는 라이브러리를 하나 지목한다. *"If you need or want to work with GraphQL, Strawberry is the recommended library as it has the design closest to FastAPI's design, it's all based on type annotations."*

인터넷에는 Starlette의 `GraphQLApp`을 쓰는 예제가 아직 남아 있는데, **그건 2021년에 끝난 이야기다.** 0.15.0에서 폐기 예고, 0.17.0(2021-11-04)에서 제거됐다. Starlette 1.0과는 무관한 사건이다.

Strawberry는 파이썬 타입 애너테이션으로 스키마를 만든다. 3장에서 Pydantic이 하던 일과 발상이 같다. 설치는 `uv add "strawberry-graphql[fastapi]"` 한 줄이다.

> **📐 저자 설계 —** 아래 스키마는 `tracker`의 읽기 전용 조회를 위해 이 책이 정한 최소 형태다. Strawberry가 제공하는 표면 자체는 공식 문서에 있는 그대로다.

```python
# src/tracker/api/graphql.py
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class IssueType:
    id: int
    title: str
    status: str

@strawberry.type
class Query:
    @strawberry.field
    async def issue(self, issue_id: int) -> IssueType:
        ...

schema = strawberry.Schema(Query)
graphql_router = GraphQLRouter(schema)
```

등록은 다른 라우터와 똑같이 `app.include_router(router=graphql_router, prefix="/graphql")` 한 줄이고, REST와 병존시키는 데 특별한 장치가 필요 없다.[^9-3]

몸통을 비워둔 데는 이유가 있다. 리졸버는 세션을 얻어야 하는데, 4장의 `SessionDep`을 그대로 쓸 수 있는지가 확실하지 않다. 리졸버를 부르는 쪽이 FastAPI의 의존성 해석기가 아니라 Strawberry의 실행기이기 때문이다. 이 배선은 확인하지 못했으니 Strawberry 문서에서 직접 보고 넘어가자.

가장 비싼 사실이 남았다. Strawberry 공식 문서의 경고를 그대로 옮긴다.

> *"FastAPI processes sync endpoints in a threadpool and async endpoints using the event loop. However, Strawberry processes sync and async fields using the event loop, which means that using a `sync def` will block the entire worker."*

5장을 기억하는가. `def`로 선언한 경로 함수는 스레드풀로 오프로드된다. 그 40개짜리 스레드풀은 실은 **안전망**이었다. 리졸버에는 그 안전망이 없다 — 필드 하나를 `def`로 선언하면 워커 전체가 선다. "선언 키워드가 실행 장소를 정한다"던 규칙이 여기서는 적용되지 않는다. 처방은 문서가 직접 말한다 — 모든 필드를 `async def`로, 도저히 안 되면 `starlette.concurrency.run_in_threadpool`로 감싸라. 취향이 아니라 사고 예방이다.

한 가지 더. GraphQL 스키마를 얹는다는 것은 `tracker`가 **같은 데이터를 세 번 선언**한다는 뜻이다. 6장의 SQLAlchemy 매핑, 3장의 Pydantic 스키마, 방금 만든 Strawberry 타입. 필드 하나에 세 곳을 고쳐야 하고, 그 셋을 묶어주는 층은 여기 없다.

## 나가는 호출 — 기본값은 있고, 재시도는 없다

이제 방향을 뒤집자. 사내 검색 서비스에 물어보는 쪽이다. 먼저 정할 것은 HTTP 클라이언트를 언제 만드느냐인데, 답은 4장에서 정해뒀다. lifespan에서 `AsyncClient`를 만들어 `app.state.http_client`에 올려두고 종료할 때 닫는다. 여기서 새로 만들 일은 없다 — 요청마다 만들면 커넥션 풀이 요청마다 생겼다 버려진다. 꺼내 쓸 때는 요청 객체를 거친다. Starlette 문서가 *"the app is available on `request.app`"*이라고 안내하므로, 경로 함수에서는 `request.app.state.http_client`로 닿는다.[^9-5]

기본값은 한 번 들여다보자. httpx는 타임아웃을 **기본으로 켜두고** 시작한다. 네트워크가 5초간 조용하면 예외를 던지며, 타임아웃은 연결·읽기·쓰기·풀 네 종류다. 커넥션 풀에도 기본값이 있다 — 최대 연결 100개, 유지 연결 20개, 유휴 만료 5초.[^9-4] 그냥 지나치지 말자. 6장 끝에서 데이터베이스 커넥션을 셀 때 했던 산술이 반복된다. **워커 수 × 레플리카 수 × 100.** 3레플리카에 워커 4개면 상대 서비스 입장에서 최대 1,200개다. 필요하면 `limits`로 낮춰 잡자.

진짜 차이는 `retries`에 있다. 공식 문서의 문장은 이렇게 읽힌다.

> *"Requests will be retried the given number of times in case an `httpx.ConnectError` or an `httpx.ConnectTimeout` occurs, allowing smoother operation under flaky networks."*

`ConnectError`와 `ConnectTimeout`. **연결을 맺는 데 실패한 경우만** 재시도한다. 상대가 503을 돌려주면 재시도하지 않고, 읽기 타임아웃이 나도 재시도하지 않는다. 연결은 멀쩡히 맺혔으니까.

선언 한 줄로 백오프까지 붙던 감각으로 오면 여기서 **반드시 틀린다.** 그리고 틀린 티가 나지 않는다. `retries=3`이 적혀 있으면 리뷰도 통과하고 평소에도 잘 돈다. 상대가 500을 뿜는 날에만 아무 일도 일어나지 않을 뿐이다. 찜찜한 안전장치다. httpx 문서 자신이 이 한계를 인정하고, 503이나 읽기·쓰기 오류에 반응하려면 `tenacity` 같은 범용 도구를 보라고 적어두었다.[^9-4]

그 도구를 예제로 끌어들이는 대신 구조만 남겨두자. 복원력은 세 겹이다. 타임아웃은 이미 켜져 있으니 값만 조정한다. 재시도의 기준은 상태 코드가 아니라 멱등성이다 — 조회는 다시 불러도 되지만, 무언가를 만드는 호출은 상대가 이미 처리했는데 응답만 못 받았을 수 있다. 차단은 연속 실패가 쌓이면 호출을 멈추고 즉시 실패시킨다.

세 번째 겹이 문제다. **이 책은 파이썬·asyncio 진영의 서킷 브레이커 지형을 조사하지 않았다.** 이름이 오르내리는 `pybreaker`조차 최신 버전도 비동기 지원 범위도 확인하지 못했다. 그래서 도구 대신 패턴만 남긴다. 실패를 세는 카운터, 임계치, 열린 뒤 다시 시도해보는 간격 — 셋이 전부이고, 설계 지점은 그 상태를 어디에 두느냐다. 프로세스 안에 두면 워커마다 따로 열리고 닫힌다. 7장과 8장에서 만난 그 경계다.

> **📐 저자 설계 —** 아래 클라이언트 래퍼와 실패 매핑은 이 책이 정한 구조다. httpx가 제공하는 표면 자체는 공식 문서에 있는 그대로다.

```python
# src/tracker/clients/search.py
import httpx
from httpx import AsyncClient

from tracker.errors import ExternalServiceError

class SearchClient:
    def __init__(self, client: AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url

    async def search_issues(self, keyword: str) -> list[dict]:
        try:
            response = await self._client.get(
                f"{self._base_url}/search", params={"q": keyword}, timeout=2.0
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalServiceError("검색 서비스를 사용할 수 없다") from exc
        return response.json()["items"]
```

```python
# src/tracker/api/issues.py
from fastapi import Request

from tracker.clients.search import SearchClient
from tracker.deps import SettingsDep

# ...(2장, 생략)

@router.get("/search")
async def search_issues(request: Request, q: str, settings: SettingsDep) -> list[dict]:
    client = SearchClient(request.app.state.http_client, settings.search_service_url)
    return await client.search_issues(q)
```

눈여겨볼 곳은 예외를 옮겨 담는 줄이다. `httpx.HTTPError`는 요청 실패와 `raise_for_status()`가 던지는 상태 오류를 함께 아우르는 상위 클래스라, 이 한 줄이 바깥 세계의 실패를 3장의 `ExternalServiceError`로 모아준다.[^9-4] 그러면 3장의 핸들러가 502와 `ErrorResponse` 모양으로 내보낸다 — 예외 핸들러는 여전히 세 개다. `base_url`을 래퍼가 갖는 것도 의도적이다. 앱 전체가 공유하는 클라이언트에 특정 상대의 주소를 박아둘 수는 없으니, 주소는 2장의 `Settings`에 얹는다.

```python
# src/tracker/settings.py
class Settings(BaseSettings):
    # ...(2장, 생략)

    search_service_url: str
```

## BFF의 경계 — 무엇을 모아주고 무엇을 흘려보낼 것인가

모바일 화면 하나를 그리는 데 이슈 조회, 검색, 알림 설정까지 세 곳을 물어야 한다면, 그 세 번의 왕복은 누가 감당하는가? 클라이언트가 각자 호출하게 둘 수도 있고, 우리 앱이 대신 호출해 한 번의 응답으로 합쳐줄 수도 있다. 후자를 흔히 BFF라고 부른다.

여기서 근거의 두께를 먼저 밝혀두는 게 정직하겠다. **BFF는 업계 관행이지 정립된 이론이 아니다.** 이 책을 준비하며 학술 문헌을 뒤졌을 때 BFF를 정면으로 다룬 것은 사실상 한 편(Microusity, ICPC 2023)뿐이었다. 그러니 아래 판단 기준은 논문이 보증하는 것이 아니라 **저자의 기준**이고, 당신 팀의 사정에 따라 다르게 그어도 된다.

| 이런 요청은 | 판단 | 이유 |
|---|---|---|
| 한 화면이 여러 서비스를 불러야 한다 | 모아준다 | 모바일 회선에서는 왕복 수가 체감 성능을 지배한다 |
| 상대 응답을 그대로 쓴다 | 흘려보낸다 | 중계만 하는 계층은 상대 스키마 변경을 두 번 겪게 만든다 |
| 권한 판정이 끼어든다 | 모아준다 | 클라이언트가 판정하면 그건 판정이 아니다 |
| 페이로드가 큰데 화면은 일부만 쓴다 | 모아준다 | 잘라서 보내는 것이 BFF의 본래 일이다 |
| 파일 업로드·다운로드 | 흘려보낸다 | 바이트를 두 번 통과시키면 메모리와 대역이 두 배가 된다 (8장) |

실패 처리도 미리 정해야 한다. 세 곳 중 한 곳이 죽으면 전체를 502로 실패시킬 것인가, 나머지만 모아 돌려줄 것인가? 기준은 화면 쪽에 있다. 그 조각이 없어도 화면이 의미를 갖는다면 결손 표시를 담은 부분 응답을, 화면의 존재 이유라면 실패를 돌려주자. 어느 쪽이든 **클라이언트가 구별할 수 있는 형태여야** 한다. 조용히 빈 배열을 돌려주는 것이 가장 나쁘다.

앞 절의 GraphQL과 이 절의 BFF가 같은 문제를 다르게 푼다는 것도 눈치챘을 것이다. 클라이언트 종류가 적고 화면 구성이 안정적이면 **BFF 엔드포인트**가 싸게 먹히고, 여럿이고 요구가 계속 바뀌면 **스키마**가 값을 한다. 둘 다 얹어놓고 어느 쪽도 관리하지 않는 상태가 가장 비싸다.

---

한 장 만에 `tracker`가 늘린 표면이 세 개다. 브라우저에 내보내는 템플릿과 정적 파일, 외부 클라이언트에게 약속한 스키마, 우리 손 밖에 있는 서비스에 대한 의존.

셋 다 공짜가 아니다. 정적 파일은 이미지에 구워질지 따로 배포될지 정해야 하고, 리졸버는 어느 실행 장소에서 도는지 매번 확인해야 하고, 바깥 호출은 상대의 나쁜 날을 우리 응답 시간으로 받아낸다. 여덟 장 동안 쌓아온 것이 "어떻게 쓰는가"였다면, 늘어난 세 표면은 다른 질문을 꺼낸다.

**이걸 전부 감당한 채로, 어떻게 프로덕션에 올릴 것인가.**

[^9-1]: `Jinja2Templates`·`HTMLResponse`·`StaticFiles` import 경로, `app.mount(...)`·`TemplateResponse(request=…, name=…, context=…)`·`url_for` 호출 형태, 주석 축자 *"Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter."* — FastAPI 공식 문서 *Templates*(https://fastapi.tiangolo.com/advanced/templates/)·*Static Files*(https://fastapi.tiangolo.com/tutorial/static-files/) (조회 2026-07-26)

[^9-2]: `hx-post`·`hx-target`·`hx-swap`의 정의와 요청 헤더 `HX-Request`(*"always 'true'"*) — htmx 공식 레퍼런스, https://htmx.org/reference/ (조회 2026-07-26)

[^9-3]: `strawberry.type`·`strawberry.field`·`strawberry.Schema`·`strawberry.fastapi.GraphQLRouter` 표면과 sync 리졸버 경고 원문 — Strawberry 공식 문서 *FastAPI Integration*, https://strawberry.rocks/docs/integrations/fastapi (조회 2026-07-26)

[^9-4]: `AsyncClient`의 `limits`·`base_url`·`transport`와 풀 기본값, `httpx.Limits(...)`, `httpx.AsyncHTTPTransport(retries=1)`과 `retries` 동작 범위·`tenacity` 언급, `client.get(...)`·`response.json()`, `httpx.HTTPError`(*"Base class for `RequestError` and `HTTPStatusError`"*)·`raise_for_status()` — httpx 공식 문서 *API Reference*·*Resource Limits*·*Transports*·*Async*·*QuickStart*·*Exceptions*, https://www.python-httpx.org/api/ 외 (조회 2026-07-26). 타임아웃 5초는 4장 각주에서 확인했다

[^9-5]: *"Where a `request` is available (i.e. endpoints and middleware), the app is available on `request.app`."* — Starlette 공식 문서 *Applications*, https://www.starlette.io/applications/ (조회 2026-07-26)

[^9-6]: `Header`의 언더스코어→하이픈 자동 변환과 `convert_underscores` — FastAPI 공식 문서 *Header Parameters*, https://fastapi.tiangolo.com/tutorial/header-params/ (조회 2026-07-26)

[^9-7]: `frontend(path, directory, fallback="auto", check_dir=True)` 시그니처, 경로 연산 우선 확인(*"checked only if no normal route matched"*)·`Accept: text/html`/`application/xhtml+xml` GET·HEAD 폴백·누락 자원 404·`StaticFiles` 상단 안내 — FastAPI 공식 문서 *Frontend*, https://fastapi.tiangolo.com/tutorial/frontend/. 0.138.0(2026-06-20) 추가, 0.139.0(2026-07-01) *"Support dependencies in `app.frontend()`"* — https://fastapi.tiangolo.com/release-notes/ (조회 2026-07-26)
