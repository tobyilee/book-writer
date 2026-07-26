# 4장. `Depends`와 미들웨어 — 컨테이너 없는 의존성 주입

2장에서 골격만 잡아둔 `IssueService`를 이제 여러 라우터에서 실제로 쓰려 한다고 해보자. 지금까지 이건 고민거리가 아니었을 것이다. 클래스에 애너테이션 한 줄을 붙여 컨테이너에 올려두고, 쓰는 쪽에서는 필드에 주입 애너테이션 하나. 그게 어디서 왔는지는 물어볼 필요조차 없었다.

FastAPI에도 의존성 주입이라 부르는 장치가 있다. 이름은 `Depends`다. 그런데 그 이름을 보고 컨테이너를 기대한 손은 대개 두어 시간 안에 벽에 부딪힌다. 서비스 객체를 앱 시작 때 한 번만 만들어두려는 순간이 특히 그렇다.

무엇이 없어서 그럴까. 그리고 필터 체인을 쓰던 자리는 이제 무엇이 채우고 있을까.

## `Depends`가 실제로 하는 일

시그니처부터 보는 편이 빠르다. 0.140.0 태그 소스에서 뽑은 것이다.

```python
# (개념 설명용 — 파일 아님)
def Depends(
    dependency: Callable[..., Any] | None = None,
    *,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any: ...
```

> 출처: fastapi 0.140.0 태그 소스 `fastapi/param_functions.py` (조회 2026-07-25)

첫 인자가 전부다. 콜러블 하나. `Depends(get_settings)`라고 적으면 FastAPI는 경로 함수를 부르기 직전에 `get_settings`를 호출하고, 그 반환값을 해당 파라미터에 넣어준다. 타입으로 무언가를 검색하지 않는다. 등록부를 뒤지지도 않는다. **적혀 있는 함수를 호출할 뿐이다.**

그러면 이게 왜 "주입"인가? 그냥 함수 호출 아닌가?

재귀 때문이다. 의존성 함수도 자기 파라미터를 가질 수 있고, 그 파라미터에 또 `Depends`가 붙을 수 있다. FastAPI는 시그니처를 읽어 의존성을 찾고, 그 의존성의 시그니처를 다시 읽어 또 찾는다. 잎에 닿을 때까지 내려갔다가 값을 들고 거슬러 올라온다. 컨테이너와 결과가 비슷해 보이는 이유가 이것인데, 그 트리를 만드는 재료는 **등록 정보가 아니라 함수 시그니처**다.

`use_cache=True`도 짚어두자. 한 요청 안에서 같은 의존성이 세 군데에 등장해도 함수는 한 번만 호출되고 결과가 공유된다. 편리하다. 그런데 이 캐시의 수명이 요청 하나라는 점이 곧 다음 절을 통째로 만들어낸다. 프로토타입도 아니고 싱글턴도 아닌, 오직 하나의 스코프만 있는 셈이다.

세 번째 인자 `scope`는 조금 뒤에 따로 다룬다. 방금 말한 스코프와는 다른 물건이다.

## 컨테이너가 없다는 말의 정확한 뜻

"FastAPI에는 DI 컨테이너가 없다"는 문장은 인터넷에 널려 있다. 정확히 옮기지 않으면 엉뚱한 기대를 하게 된다.

별도의 DI 라이브러리인 dishka가 자기 문서의 대안 비교 항목에서 FastAPI의 `Depends`를 평가한 대목이 이 한계를 가장 정확히 짚는다.[^4-7]

> "You have to declare each dependency with `Depends` on each level of application. So either your business logic contains details of IoC-container or you have to duplicate constructor signatures."

애플리케이션의 모든 층에서 의존성을 다시 선언해야 한다는 것. 그래서 비즈니스 로직이 주입 도구의 흔적을 갖게 되거나, 아니면 생성자 시그니처를 계속 복제하게 된다는 것. (게시 시점을 확인하지 못했으니 생태계의 현재 평가로는 읽지 말자. 논지 자체는 코드로 확인된다.)

정리하면 이렇다. **없는 것은 자동 와이어링(auto-wiring)이다.** 타입만 보고 알아서 찾아 꽂아주는 층이 없다. 배선은 사람이 적는다.

| 물어보는 것 | DI 컨테이너 | `Depends` |
|---|---|---|
| 무엇을 넣을지 어떻게 아는가 | 등록된 것을 타입으로 찾는다 | 파라미터에 적힌 함수를 호출한다 |
| 배선은 어디에 적혀 있는가 | 등록하는 한 곳 | 쓰는 자리마다 |
| 인스턴스는 얼마나 사는가 | 스코프로 지정한다 | 요청 하나 (`use_cache`) |

세 번째 행이 실무에서 가장 먼저 아프다. 커넥션 풀이나 HTTP 클라이언트처럼 앱이 사는 동안 하나여야 하는 물건을 `Depends`만으로는 표현할 수 없다. 이 질문은 이슈 #8054에 올라와 있고, 확인된 답은 내장 캐싱이 단일 요청 안에서만 유효하다는 사실뿐이다. 그동안 커뮤니티는 우회법을 층층이 쌓았다 — 함수 결과 캐시, 시작 시점 인스턴스화, `app.state`, 종료 스택과 앱 상태의 조합. 놀랍게도 그 이슈는 2026년 현재까지 **Unanswered** 상태다. 여러 해가 지나도록 공식 답이 붙지 않았다는 사실 자체가 지금의 현황이다.

여기서부터는 **저자 해석**이다. 근거는 여론조사가 아니라 종류가 다른 자국 두 개다.

한쪽은 **유물**이다. 2026-04-28에도 누군가 NestJS의 모듈 시스템과 DI 컨테이너, Guards·Interceptors·Pipes를 그리워하며 FastAPI 위에 그것을 얹는 프로젝트를 공개했다. **단일 저자의 프로젝트이지 커뮤니티 합의가 아니다.** 그래도 2026년에도 누군가 그 필요를 느꼈다는 것만은 데이터다. 2장의 rmonvfer가 "프레임워크 위에 프레임워크를 하나 더 얹었다"고 고백한 것도 같은 종류다.

다른 쪽은 **발언**이다. Lobsters의 한 개발자는 `Depends`가 시그니처를 읽어 알아서 트리를 만드는 그 암묵성이 "명시적인 편이 암묵적인 것보다 낫다"는 파이썬의 격언에 어긋난다고 지적했다. 마법이 과하다는 쪽이다. 한 사람의 발언이니 진영의 목소리로 부풀리지는 말자.

같은 장치를 놓고 한쪽은 부족하다 하고 한쪽은 과하다 한다. 무엇이 옳은지 정하는 대신, **당신이 어느 쪽에서 걸어 들어왔는지를 알고 시작하는 것**이 이 도구를 다루는 첫 단계다.

## 그래서 배선을 이름으로 만든다

자동 와이어링이 없다는 건 실무적으로 한 가지를 뜻한다. **같은 배선을 여러 번 적게 된다.** 그리고 여러 번 적히는 것은 언젠가 서로 달라진다. 세션을 받는 엔드포인트 스무 개 중 셋만 다르게 받고 있는 상태를 떠올려보자.

`tracker`는 배선을 `deps.py` 한 파일에 모으고, 각 배선에 이름을 준다. 타입 별칭으로.

> **📐 저자 설계 —** 아래 의존성 함수와 별칭 이름은 FastAPI 공식 권장이 아니라, 이 책이 `tracker` 전체에서 쓰기로 정한 한 가지 안이다. 이후 모든 장이 이 이름만 쓴다.

```python
# src/tracker/deps.py
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.user import User
from tracker.services.issue import IssueService
from tracker.settings import Settings, get_settings


async def get_session() -> AsyncIterator[AsyncSession]:
    ...
    yield


async def get_current_user() -> User:
    raise NotImplementedError


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_issue_service(session: SessionDep) -> IssueService:
    return IssueService(session)


IssueServiceDep = Annotated[IssueService, Depends(get_issue_service)]
```

먼저 두 함수는 스텁이다. `get_session`은 몸통에 `...`만 두고 `yield`의 존재와 반환 타입만 확정했다. 세션이 어디서 오는지는 6장이 채운다. `get_current_user`는 아예 예외를 던진다 — 스텁이 조용히 `None`을 돌려주다 한참 뒤 엉뚱한 곳에서 터지는 것보다, 부르는 즉시 크게 터지는 편이 낫다. 몸통은 10장이 채운다. 두 경우 모두 **이름과 반환 타입은 바뀌지 않는다.** 호출부가 별칭을 거쳐 들어오니 계약은 그 둘이고, 파라미터와 몸통은 구현이다. 뒤 장은 완성하지 재정의하지 않는다. `User`를 미리 import하는 것도 같은 이유다 — 클래스는 6장에서 생기지만 이름은 지금 확정해둔다.

그리고 `get_issue_service`의 파라미터가 `SessionDep`이다. 즉 **의존성이 의존성을 요구한다.** 앞 절에서 말한 재귀가 눈에 보이는 형태로 나타난 것이고, 컨테이너 없이 조립이 되는 이유가 이 다섯 줄에 다 들어 있다 — 함수가 함수를 부르고, 그 조합에 이름을 붙였을 뿐이다. `Depends`를 컨테이너가 아니라 **함수 조합기**로 다시 보자는 말이 이 뜻이다.

그리고 별칭. 그 조합에 `IssueServiceDep`이라는 이름을 붙여두면 라우터 쪽 코드는 이렇게 짧아진다.

```python
# src/tracker/api/issues.py
from tracker.deps import IssueServiceDep
from tracker.schemas.issue import IssueCreate, IssueRead

# ...(2장, 생략)


@router.post("/", status_code=201, response_model=IssueRead)
async def create_issue(payload: IssueCreate, issues: IssueServiceDep) -> IssueRead:
    ...
```

요청 본문 하나와 서비스 하나, 둘 다 타입만 적혀 있다. 배선 코드가 시그니처 뒤로 사라지고, 시그니처만 읽어도 이 엔드포인트가 무엇을 필요로 하는지 드러난다.

한 가지 더. `get_issue_service`는 아무 I/O도 하지 않는데 `async def`로 뒀다. 취향이 아니라 계산이다. 동기 의존성이 무엇을 대가로 지불하는지는 5장이 숫자로 보여준다.

값을 돌려주지 않고 검사만 하는 의존성은 경로 데코레이터나 `APIRouter`의 `dependencies` 인자에 실어 파라미터 목록을 더럽히지 않고 붙인다. 인가가 그런 물건이고, 10장이 여기를 쓴다.

## `yield`, 그리고 언제 끝나는가

세션이나 파일 핸들처럼 열었으면 닫아야 하는 것은 값을 돌려주는 것만으로 끝나지 않는다. `tracker`의 `get_session`이 `return`이 아니라 `yield`를 쓰는 이유가 이것이다. `yield` 앞은 준비, 뒤는 정리다.

그런데 조금 더 깊이 들어가보자. **정리 코드는 정확히 언제 도는가?** 경로 함수가 끝난 직후인가, 응답이 클라이언트로 나간 뒤인가? 사소해 보인다면 `@Transactional`과 OSIV를 두고 벌어졌던 논쟁을 떠올려보자. 세션이 언제 닫히느냐는 응답을 만드는 동안 지연 로딩이 되느냐를 결정하고, 그건 곧 응답 직렬화가 성공하느냐의 문제다.

0.140.0 / 2026-07 기준으로 `Depends`에는 그 시점을 고르는 `scope` 파라미터가 있다. 공식 문서의 설명은 이렇다.[^4-6]

> `"function"`: ... end the dependency after the *path operation function* ends, but **before** the response is sent back to the client.
> `"request"`: ... end **after** the response is sent back to the client.

이 파라미터의 배경에는 이슈 #11107(2024-02)이 있다. `yield` 의존성의 정리 순서가 뒤집혀 커밋 전에 세션이 닫히는 문제였고, #11143으로 승격됐으며 확인 시점에 Closed 상태다. 그리고 2025-10의 다른 이슈에서 tiangolo가 제시한 처방이 `Depends(func, scope="function")`이었다.

그런데 **#11143이 어떤 사유로 닫혔는지, 어떤 PR이 병합됐는지를 이 책은 확인하지 못했다.** 그래서 "`scope`가 #11107을 해결했다"고는 쓰지 않겠다. 성립할 가능성이 높다고 보지만 릴리스 노트로 확인하기 전까지는 미확정이고, 이렇게 반올림하는 습관이 기술서를 못 믿게 만든다.

결론은 그래서 보수적이다. **`tracker`의 표준형은 평범한 `Depends(get_session)`이다.** 새로 생긴 파라미터를 관용구로 승격시키는 것은 그것이 무엇을 해결했는지 확인된 다음의 일이다. 이 파라미터는 6장에서 다시 꺼낸다.

## 필터 체인을 쓰던 자리

`Depends`가 채우지 못하는 자리가 하나 있다. 모든 요청에, 라우팅되기 전에 일어나야 하는 일이다. 요청 ID를 붙이고, 접근 로그를 남기고, 응답 헤더를 손보는 것들. 당신은 이걸 필터나 인터셉터로 해왔을 것이다. 요청·응답·다음 고리 세 가지를 받아 처리하고 넘기던 그 구조다.

ASGI에서 그 자리를 채우는 것은 미들웨어이고, 생김새는 1장의 계약에서 곧바로 나온다. **미들웨어는 앱을 감싼 또 하나의 앱이다.** `scope`·`receive`·`send`를 받아 필요한 일을 하고 안쪽 앱에 그대로 넘긴다.

작성 형태는 두 가지다. 하나는 그 계약을 날것으로 구현하는 순수 ASGI 미들웨어다.

```python
# (개념 설명용 — 파일 아님)
from starlette.types import ASGIApp, Scope, Receive, Send

class ASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)
```

> 출처: Starlette 공식 문서 Middleware, https://www.starlette.io/middleware/ (조회 2026-07-26)

다른 하나는 `BaseHTTPMiddleware`를 상속해 `dispatch(request, call_next)`를 구현하는 형태다.[^4-1] 이쪽은 `Request` 객체를 받고 `call_next(request)`를 `await`해 `Response`를 얻는다.

둘의 차이는 어디까지 말할 수 있을까. 안전한 것은 둘이다.

첫째, 실행 시점은 라우팅 바깥이다. Starlette 문서가 정리한 스택 순서는 서버 에러 처리 → 사용자가 선언한 미들웨어(선언 순서대로) → 예외 처리 → 라우팅 → 엔드포인트다.[^4-1] 미들웨어는 어느 경로로 갈지 정해지기 전에 돈다. 라우팅 결과에 따라 다르게 굴고 싶다면 여기가 아니다.

둘째, 적용 범위가 다르다. 순수 ASGI 형태는 `scope`를 그대로 받으므로 `scope["type"]`을 보고 HTTP 연결인지 WebSocket 연결인지 구분해 다룰 수 있다. 반면 `dispatch` 형태는 요청 하나에 응답 하나가 대응하는 모양으로 쓰여 있다. 7장에서 WebSocket에도 무언가를 걸어야 할 때 이 차이가 선택을 결정한다.

정직하게 밝혀두자. `BaseHTTPMiddleware`에 이런저런 한계가 있다는 이야기가 돌아다니지만, **이 책은 그 한계를 1차 소스로 확인하지 못했다.** 확인하지 못한 목록을 옮겨 적는 대신 여기서 멈춘다.

`tracker`의 첫 미들웨어는 요청 ID를 붙인다. 3장의 에러 응답에 있던 `request_id`, 그 값을 심는 자리가 여기다.

> **📐 저자 설계 —** 아래 미들웨어는 FastAPI가 제공하는 것이 아니라, 3장이 정한 에러 응답 계약을 채우기 위해 이 책이 작성한 것이다.

```python
# src/tracker/middleware.py
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request, call_next):
        request_id = request.headers.get(self.header_name) or uuid4().hex
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[self.header_name] = request_id
        return response
```

들어온 요청에 이미 ID가 붙어 있으면 그걸 쓰고 없으면 만든다. 앞단 프록시나 게이트웨이가 붙여 보낸 값을 버리지 않기 위해서다. 심는 곳은 `request.state`이고, 3장의 예외 핸들러가 정확히 거기서 값을 꺼낸다. 14장에서는 이 값이 로그와 요청을 잇는 열쇠가 된다.

등록은 `main.py`에서 한 줄이다.

```python
# src/tracker/main.py
from tracker.middleware import RequestIdMiddleware

# ...(3장, 생략)

app.add_middleware(RequestIdMiddleware)
```

`add_middleware`를 쓰는 이유는 공식 문서가 밝혀두었다 — 이렇게 등록해야 *"the internal middlewares handle server errors and custom exception handlers work properly"*.[^4-2] 내부 미들웨어와 예외 핸들러가 제대로 맞물리게 해준다는 뜻이다.

그렇다면 횡단 관심사를 미들웨어와 `Depends` 중 어디에 둘까. 기준은 단순하다. 모든 요청에 예외 없이 적용돼야 하고, 라우팅 전에 일어나야 하고, 응답 헤더를 손대야 한다면 미들웨어다. 반대로 **특정 라우터에만 걸리고, 값을 돌려줘야 하고, 시그니처에 타입으로 드러나야 하고, 테스트에서 갈아 끼워야 한다면 `Depends`다.** 인증된 사용자를 꺼내는 일이 정확히 후자다.

## 예외 핸들러는 어디에 등록되는가

`@ControllerAdvice`가 있던 자리다. 응답 계약 자체는 3장이 끝까지 책임지므로 여기서는 메커니즘만 본다.

등록 방법은 두 갈래고 결과는 같다. 3장에서 쓴 데코레이터 `@app.exception_handler(TrackerError)`, 그리고 `FastAPI(...)` 생성자의 `exception_handlers` 인자다. 후자는 2장에서 훑어본 생성자 파라미터 목록에 들어 있고, 핸들러를 상태 코드로도 예외 클래스로도 걸 수 있다.[^4-4]

해석 규칙 하나를 못 박아두자. **등록한 예외 클래스의 하위 클래스까지 같은 핸들러가 받는다.** 핸들러 조회가 예외 타입의 MRO를 거슬러 올라가며 등록부를 찾기 때문이다.[^4-5] 공식 문서도 같은 성질 위에 서 있다 — `HTTPException` 핸들러를 걸 때 *"you should register it for Starlette's `HTTPException`"*이라고 권하고, FastAPI의 `HTTPException`이 그 클래스를 상속한다고 함께 밝힌다.[^4-4] 3장이 핸들러를 셋으로 묶어둘 수 있었던 근거가 이것이다.

앞서 인용한 공식 문서의 한 줄이 말해주듯 예외 핸들러는 미들웨어 스택 안쪽에서 동작한다. 그래서 미들웨어가 `request.state`에 심어둔 요청 ID를 예외 핸들러가 읽을 수 있다.

## 앱이 사는 동안

이제 앞에서 미뤄둔 문제로 돌아오자. 요청보다 오래 사는 물건들 — HTTP 클라이언트, 커넥션 풀 — 은 어디에 두는가.

`lifespan`이다. 앱이 뜰 때 한 번 열고, 내려갈 때 한 번 닫는다.

> **📐 저자 설계 —** 아래 배선은 공식 권장 구조 위에 이 책이 `tracker`의 자원 배치를 정한 것이다. 여기서 만든 클라이언트를 9장이 그대로 재사용한다.

```python
# src/tracker/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = AsyncClient(timeout=5.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(title="tracker", lifespan=lifespan)
```

`yield` 앞뒤로 시작과 종료가 갈리는 이 모양은 방금 본 `yield` 의존성과 정확히 같은 문법이다. 다른 것은 수명뿐이다 — 저쪽은 요청 하나, 이쪽은 앱 하나.

`timeout=5.0`을 명시한 것은 의도다.[^4-3] **밖으로 나가는 호출에는 언제나 시한이 붙어 있어야 한다.**

클라이언트를 모듈 전역 변수가 아니라 `app.state`에 두는 것도 규칙으로 정해두자. 전역 변수는 테스트에서 갈아 끼우기 어렵고, 앱 인스턴스가 둘 이상 생기는 순간 누구의 것인지 모호해진다. 9장의 BFF는 여기 있는 클라이언트를 재사용한다. 요청마다 새로 만드는 코드를 인터넷에서 보게 되겠지만, 그건 커넥션 풀을 매번 버리는 짓이다.

미리 짚어둘 것이 있다. 워커를 여러 개 띄웠을 때 `lifespan`이 워커마다 도는지, 서버리스에서는 어떻게 되는지 — 이 책은 그 동작을 1차 소스로 확인하지 못했다. 프로세스가 어디서 갈라지는지는 5장이, 그것을 배포에서 어떻게 다룰지는 13장이 다룬다.

### 그런데 `on_event`는 어떻게 된 건가

인터넷 예제를 검색하면 `@app.on_event("startup")` 형태가 아직 잔뜩 나온다. 정확히 이해하려면 세 겹을 구분해야 한다.

첫째, FastAPI 0.140.0에는 `on_event`가 아직 있다. 소스에 `@deprecated` 데코레이터가 붙어 있고 메시지는 *"on_event is deprecated, use lifespan event handlers instead."*다. 생성자의 `on_startup`·`on_shutdown` 파라미터도 남아 있다.

둘째, 제거한 쪽은 Starlette이다. 1.0.0rc1 릴리스 노트의 축자는 *"Remove `on_event()` decorator from `Starlette` and `Router`"*이고, `on_startup`·`on_shutdown`·`add_event_handler()`도 함께 사라졌다.

셋째, FastAPI는 `starlette>=0.46.0`으로만 핀한다. 1.x를 강제하지 않는다.

그래서 **"FastAPI가 `on_event`를 제거했다"는 틀린 서술이다.** 그리고 이 구분은 말장난이 아니라 당신 프로젝트의 문제다. 세 겹을 합치면 이런 결론이 나온다 — `on_event`를 쓴 코드가 지금 도는지 안 도는지는 **당신의 `uv.lock`이 어떤 Starlette을 물어왔는지에 달려 있다.** 같은 코드가 어제 만든 환경에서는 멀쩡하고 오늘 새로 잠근 환경에서는 죽을 수 있다는 뜻이다. 이런 종류의 차이는 정말 아찔하다. 원인이 내 코드에 없기 때문이다.

`lifespan`으로 옮기는 편이 낫다. 두 겹 아래에서 이미 사라진 기능 위에 서 있을 이유가 없다.

### 컨테이너를 잃고 얻은 것 하나

씨앗 하나를 심어두고 닫자.

```python
# (개념 설명용 — 파일 아님)
app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides = {}
```

테스트에서 특정 의존성을 다른 함수로 갈아 끼우는 장치다. 모의 빈을 주입하거나 프로바이더를 덮어쓰던 자리에 해당한다. 눈여겨볼 것은 갈아 끼울 대상을 함수 객체 하나로 지목한다는 점이다. 타입도 아니고 이름 문자열도 아니다. 자동 와이어링을 포기한 대가로 배선의 각 지점이 파이썬 객체 하나로 정확히 특정되는 성질을 얻은 셈이다. 이 장치는 11장이 쓴다.

---

배선을 이름으로 만들고(`deps.py`), 라우팅 바깥에 층을 하나 세우고(`middleware.py`), 앱의 수명을 여닫는 곳을 열었다(`lifespan`). 컨테이너가 채워주던 자리를 세 갈래로 나눠 손으로 채운 셈이다. 자동으로 되지 않는다는 사실이 처음에는 손해처럼 보이지만, 대신 **배선이 전부 읽을 수 있는 코드로 남는다.** 어디서 무엇이 오는지 궁금할 때 뒤져야 할 설정이 없다.

여기까지 오면서 계속 당연하게 여긴 것이 하나 있다. 의존성도, 미들웨어의 `dispatch`도, `lifespan`도 전부 `async def`로 적혀 있다는 것. 그중 하나를 그냥 `def`로 적으면 무슨 일이 일어나는지가 다음 이야기다. 답은 문법이 아니라 숫자에 있다.

[^4-1]: import 경로 `starlette.middleware.base`의 `BaseHTTPMiddleware`, `dispatch(self, request, call_next)` 시그니처, `__init__` 오버라이드 시 `super().__init__(app)`, `response.headers[...]` 조작, 순수 ASGI 미들웨어의 `__init__`/`__call__` 형태와 `starlette.types`의 `ASGIApp`·`Scope`·`Receive`·`Send`, 미들웨어 스택 순서 — Starlette 공식 문서 Middleware, https://www.starlette.io/middleware/. `request.headers` 조회 — 같은 문서 Requests, https://www.starlette.io/requests/ (조회 2026-07-26)

[^4-2]: `app.add_middleware(MiddlewareClass, **options)` 형태와 인용한 축자 — FastAPI 공식 문서 Advanced Middleware, https://fastapi.tiangolo.com/advanced/middleware/ (조회 2026-07-26)

[^4-3]: `AsyncClient`의 생성자 인자 `timeout`(기본값 `Timeout(timeout=5.0)`)과 메서드 `aclose()` — httpx 공식 문서 Developer Interface, https://www.python-httpx.org/api/ · Timeouts, https://www.python-httpx.org/advanced/timeouts/ (조회 2026-07-26)

[^4-4]: `exception_handlers` 생성자 인자와 핸들러를 상태 코드·예외 클래스에 거는 방식 — Starlette 공식 문서 Exceptions, https://www.starlette.io/exceptions/. 인용한 축자와 *"FastAPI's `HTTPException` error class inherits from Starlette's `HTTPException` error class"* — FastAPI 공식 문서 Handling Errors, https://fastapi.tiangolo.com/tutorial/handling-errors/ (조회 2026-07-26)

[^4-5]: 예외 핸들러 조회가 `type(exc).__mro__`를 순회한다는 사실 — starlette 소스 `starlette/_exception_handler.py`의 `_lookup_exception_handler()`. **핀 하한 0.46.0과 현행 1.3.1 양쪽에서 동일함을 확인했다** (조회 2026-07-26)

[^4-6]: 인용한 `scope="function"`·`scope="request"` 축자 — FastAPI 공식 문서 Dependencies with yield, https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope (조회 2026-07-25)

[^4-7]: 인용한 dishka 축자 — dishka 공식 문서 Alternatives, https://dishka.readthedocs.io/en/stable/alternatives.html (조회 2026-07-26)
