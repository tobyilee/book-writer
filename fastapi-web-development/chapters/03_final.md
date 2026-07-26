# 3장. Pydantic과 에러 계약 — 검증이 타입 시스템이 될 때

검증은 흔히 "잘못된 입력을 막는 일"이라고 한다. 문지기 같은 것이다. `@Valid`를 붙이고 `BindingResult`를 받아 에러 목록을 뒤져봤다면, 당신 몸에도 이 그림이 배어 있을 것이다. 검증은 객체가 만들어진 **다음에** 오는 단계다.

Pydantic을 며칠 써보면 이 그림이 어긋난다. 검증에 실패한 요청에서 "그래도 만들어진 객체"를 꺼내려 하면 꺼낼 것이 없다. 검증이 통과했다는 말은 곧 객체가 존재한다는 말이고, 실패했다는 말은 **아무것도 만들어지지 않았다**는 말이다. 막는 장치라기보다 만들어내는 장치에 가깝다. 그 차이가 에러 응답 계약을 누가 정하느냐까지 끌고 간다.

## 막는 장치가 아니라 만들어내는 장치

Spring에서 요청 본문 하나가 컨트롤러에 닿기까지 몇 개의 도구를 거치는지 떠올려보자. Jackson이 바인딩하고, Bean Validation이 검사하고, 응답 때 다시 Jackson이 직렬화하고, Springdoc이 그 클래스를 읽어 스펙을 만든다. 네 가지 일이고 설정도 각각 따로다.

`BaseModel`은 그 넷을 한 선언에 묶는다. 클래스 하나를 경로 함수의 파라미터 타입으로 적으면 그 타입이 곧 요청 본문의 파서이자 검증기이고, `response_model`로 적으면 응답의 직렬화 규칙이 되며, 동시에 `/docs`에 뜨는 스키마의 정의가 된다. 하나를 고치면 넷이 함께 움직인다. 뒤집어 말하면 **넷 중 하나만 다르게 하고 싶을 때 비용이 발생한다.** 이 장의 후반부는 그 비용에 관한 이야기다.

하나 짚어두자. Pydantic에는 `BindingResult`에 해당하는 물건이 없다. 있을 수가 없다. 검증이 실패하면 모델 인스턴스가 만들어지지 않으므로 경로 함수는 **아예 호출되지 않는다.** "일단 받아놓고 에러가 있으면 분기한다"는 패턴이 성립하지 않는다. 제약으로 느낄지 해방으로 느낄지는 사람마다 다르겠지만, 경로 함수 안에서 입력을 다시 의심할 필요는 사라진다.

HN의 duncanfwalker(2025-07-27)가 이 성격을 한 문장으로 요약한 적이 있다.

> "Validation rules are like an extension to the type system... In Java they got around the external-dependency-in-the-core-model problem by making the JSR-380 specification"

검증 규칙이 타입 시스템의 확장이라는 관점. Java는 그 확장을 표준 명세로 만들었고, Python 쪽은 명세 없이 라이브러리 하나가 그 자리를 가져갔다. 그 차이가 뒤에서 다룰 에러 포맷 문제의 뿌리다.

## 스키마는 넷이면 충분하다

같은 이슈 하나를 두고도 요청과 응답은 다른 모양을 요구한다. 생성 요청에는 `id`가 없고 응답에는 있으며, 부분 수정 요청은 모든 필드가 없어도 된다. 이 차이를 무시하고 클래스 하나로 버티면 "생성 때는 없어야 하는데 응답에는 있어야 하고" 같은 조건이 주석으로 쌓인다. 찜찜한 코드다.

`tracker`는 접미사 네 개로 정리한다. 공통 필드는 `Base`, 생성 요청은 `Create`, 부분 수정은 `Patch`, 응답은 `Read`. 넷 말고 다른 접미사는 쓰지 않는다.

> **📐 저자 설계 —** 아래 스키마 분리와 접미사 규약은 FastAPI 공식 권장이 아니라, 이 책이 `tracker` 전체에서 유지하기로 정한 안이다.

```python
# src/tracker/schemas/issue.py
from pydantic import BaseModel, ConfigDict, Field

from tracker.models.issue import IssuePriority, IssueStatus


class IssueBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: IssuePriority = IssuePriority.normal


class IssueCreate(IssueBase):
    project_id: int


class IssuePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: IssuePriority | None = None
    status: IssueStatus | None = None


class IssueRead(IssueBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: IssueStatus
    project_id: int
```

두 열거형의 정의는 6장에서 `models/issue.py`에 놓는다. 여기서는 이름만 앞당겨 쓴다. `IssueRead`의 `ConfigDict(from_attributes=True)`는 ORM 인스턴스의 속성을 그대로 읽겠다는 선언으로, v1의 `orm_mode` 자리에 들어온 이름이다.[^3-1]

`Patch`가 왜 별도 클래스여야 할까. PATCH 요청에서 `{"description": null}`과 `{}`는 전혀 다른 뜻이다. 전자는 "설명을 지워라", 후자는 "건드리지 마라"다. 그런데 전 필드를 `| None = None`으로 선언해 두면 파싱된 객체만 봐서는 둘을 구분할 수 없다. 양쪽 다 `description`이 `None`이다.

Pydantic은 **명시적으로 설정된 필드가 무엇인지 기억한다.** 그래서 부분 수정은 이 한 줄에서 갈린다.

```python
# (개념 설명용 — 파일 아님)
changes = patch.model_dump(exclude_unset=True)
```

`exclude_unset=True`를 주면 클라이언트가 실제로 보낸 필드만 남는다.[^3-2] 이 관용구가 `tracker`의 부분 수정 표준이다.

목록 응답은 `schemas/common.py`의 제네릭 `Page`를 두고 `Page[IssueRead]`처럼 쓴다. Pydantic v2는 `Generic`을 함께 상속하는 방식으로 제네릭 모델을 지원한다.[^3-1]

API 스키마와 DB 엔티티는 굳이 나눠야 할까? 이 지점에서 통념이 뒤집힌다. Java 쪽의 microflash(2025-07-26)는 이렇게 말했다.

> "For many cases, we don't do these kind of things in Java; a single annotated record can function as a model for both data and API layers."

반대로 Python 쪽에서 자주 나오는 말은 분리하라는 쪽이다. globular-toast(2025-08-07)는 *"Your API and your database schema are not the same thing"*이라고 썼다. "Java는 계층을 나누고 Python은 간단히 간다"는 예상과 정확히 반대다. 같은 논의의 rtpg는 한계를 이렇게 짚었다 — 평평한 구조를 검증해줄 뿐, *"it's up to you to actually build up a useful data structure"*.

`tracker`는 분리하는 쪽을 택한다. **응답 스키마가 곧 외부와의 약속**이므로, 내부 저장 구조를 바꿀 때마다 그 약속이 흔들리는 상태를 만들지 않겠다는 것이다. 물론 대가가 있다 — 필드 하나를 추가할 때 손댈 파일이 늘어난다. 대가가 견디기 어려워지면 분리를 다시 계산해보자.

## 제약은 어디에 선언되는가

Bean Validation은 제약을 **애너테이션으로 필드 옆에 붙인다.** `@NotNull`·`@Size`·`@Min`·`@Max`·`@Pattern` 같은 것들이고, 명세는 필드뿐 아니라 메서드와 클래스에도 붙일 수 있게 한다.[^3-3] 타입 선언과 제약 선언이 물리적으로 분리된 구조다.

Pydantic은 제약을 타입 선언 안으로 밀어 넣는다. `title: str = Field(min_length=1, max_length=200)`이 그 예다. 쿼리·경로·헤더 선언 함수들도 `gt`·`ge`·`lt`·`le`·`min_length`·`max_length`·`pattern`·`discriminator` 같은 인자를 전부 공통으로 갖는다.

| Jakarta Bean Validation | Pydantic·FastAPI |
|---|---|
| `@Size(min=, max=)` | `min_length` · `max_length` |
| `@Min` · `@Max` | `ge` · `le` |
| `@Pattern(regexp=)` | `pattern` |
| `@NotNull` | 타입에 `\| None`을 붙이지 않음 |

마지막 행이 가장 중요하다. **nullable 여부가 애너테이션이 아니라 타입 자체에서 나온다.** `str`은 필수고 `str | None`은 아니다. 이 감각은 6장의 SQLAlchemy 매핑에서 다시 만난다.

선언은 이렇다. `Annotated`가 낯설다면 '타입 한 칸 옆에 메타데이터를 덧붙이는 표기'로 읽으면 된다.

```python
# (개념 설명용 — 파일 아님)
# ✅ 현행 스타일
async def list_issues(
    q: Annotated[str | None, Query(min_length=2)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
): ...

# ❌ 인터넷 예제에 널려 있는 구식 스타일
async def list_issues(q: str = Query(None), limit: int = Query(20)): ...
```

아래 형태가 검색 결과에 나오더라도 따라가지 말자. 기본값 자리에 `Query(...)`를 두면 타입 힌트와 기본값이 서로 다른 말을 하게 된다.

내장 제약으로 표현되지 않는 규칙은 어떻게 할까. Java였다면 `ConstraintValidator`를 구현하고 애너테이션을 하나 만들었을 자리다. Pydantic에서는 모델 안에 `@field_validator`를 붙인 메서드를 둔다. 재사용 단위가 다르다 — 전자는 **애너테이션이 단위**라 여러 클래스에 붙여 쓰고, 후자는 **메서드가 모델에 매여** 있다. 옮겨올 때 재사용 설계를 다시 해야 한다.

당부를 해두자. 인터넷의 FastAPI 예제 상당수는 Pydantic v1 시절 어휘로 쓰여 있다. `.dict()`·`.json()`·`parse_obj()`는 `model_dump()`·`model_dump_json()`·`model_validate()`로, `orm_mode`는 `from_attributes`로, `@validator`·`@root_validator`는 `@field_validator`·`@model_validator`로, `class Config`는 `model_config = ConfigDict(...)`로, `regex`는 `pattern`으로 바뀌었다. 설정 클래스의 import 경로도 `pydantic_settings`로 옮겨갔다. 이름만 바뀐 것이 대부분이라 어렵지는 않지만, 검색 결과의 신선도를 판별하는 지표로 쓸모가 있다.

## 422는 어디서 왔는가

`ProblemDetail`을 쓰던 당신이 FastAPI 앱에 잘못된 본문을 던져보면, 가장 먼저 눈에 걸리는 것은 상태 코드다. 400이 아니라 422다. 응답 본문 모양도 낯설다.

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "item_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

> 출처: FastAPI 공식 문서 Path Parameters, https://fastapi.tiangolo.com/tutorial/path-params/ (조회 2026-07-26)

왜 422일까? 2019-10-22의 issue #643이 그 질문이고, tiangolo가 직접 답했다.

> "the error is not about using the protocols and languages incorrectly (HTTP, JSON)... but about **sending invalid contents, even though using the correct content format (JSON) through the correct channel (valid HTTP)**"

형식은 맞는데 내용이 틀렸으니 400이 아니라는 논리다. 덧붙인 이유는 실용적이다 — 검증 에러를 한 부류로 통째 분리할 수 있다는 것.

여기에 antonagestam이 2022-02-08에 정면으로 반박했다.

> "the format here is not simply JSON, but a rich OpenAPI schema. I see no reason why violating that schema, which is clearly the contract for interacting with the API, is not a client error..."

여기서 오가는 형식은 그냥 JSON이 아니라 OpenAPI 스키마이고, 그 스키마야말로 API와의 계약이니 위반은 클라이언트 에러라는 지적이다. 2022-12-06에는 Jaza가 절충안을 냈다 — 구문 오류는 400, 의미 오류는 422.

논쟁은 결론이 나지 않았고 기본값은 여전히 422다. 중요한 건 어느 쪽이 옳은가보다 **이 값이 우리 API의 계약이 되어 클라이언트로 흘러간다**는 사실이다. 프런트엔드가 이미 400을 기준으로 분기하고 있다면 그 간극은 누군가 메워야 한다.

## 진짜 벽은 상태 코드가 아니라 문서였다

그래서 바꾸면 되지 않을까? 예외 핸들러 하나 등록해 400으로 내보내면 될 것 같다. 코드만 놓고 보면 실제로 그 정도로 끝나는데, 그 다음이 난감하다.

2020-05-04에 열린 issue #1376이 그 다음의 기록이다. "Allow customization of validation error"라는 제목 아래, 이슈가 열리고 1년 사이에 우회법이 여러 갈래로 쌓였다. 그 고통을 요약한 문장 하나 — *"auto-generated documentation doesn't reflect the updated status code"*. 핸들러로 상태 코드를 바꿔도 **자동 생성 문서는 그대로 422라고 말한다.**

- akrejczinger: *"HTTP 422 is hardcoded in openapi/utils.py. I solved my issue for now by modifying the FastAPI source code itself"* — 결국 프레임워크 소스를 직접 고쳤다.
- ushu: 모듈 전역 변수(`validation_error_response_definition`)를 통째로 덮어쓰는 방법. 다만 이건 2021년의 기록이고, 그 변수가 지금도 같은 자리에 있는지는 이 책이 확인하지 않았다.
- Acerinth: Pydantic 모델 재정의 + 예외 핸들러 + `custom_openapi()`의 3단 조합.

같은 스레드의 PhilippeGalvan이 아이러니를 요약한다. *"auto-doc is a key argument!"* — 자동 문서가 이 프레임워크를 고르게 만든 근거인데, 바로 그 자동 문서가 커스터마이징의 최대 장벽이 됐다.

정리하면 이렇다. **응답을 바꾸는 건 쉽고, 응답과 문서를 함께 바꾸는 것이 비싸다.** 모르고 시작하면 "핸들러 하나 등록"이 반나절 삽질로 늘어나고, 알고 시작하면 어디서 멈출지 정할 수 있다. 다음 절이 그 선을 긋는다.

## RFC 9457, 7807에서 이어진 7년째

Spring Boot 3에서 `ProblemDetail`을 써봤다면 떠오르는 질문이 있을 것이다. 표준 에러 포맷이 있는데 FastAPI는 지원하지 않나? 한 문장으로 답하기 어려운 자리다. 세 개의 사건을 구분해야 한다.

첫째, issue #512(2019-09-07)는 RFC 7807 지원 요청이었다. RFC 9457의 전신인 문서다. tiangolo는 2020-06-10에 이렇게 답했다.

> "I haven't wanted to do it as it would break backwards compatibility, but maybe in the future, I end up doing it 🤷 🤓"

둘째, RFC 9457을 이름으로 걸고 다룬 논의는 Discussion #14517(2025-12-13)부터다. 여기서도 같은 우려가 반복된다 — *"This is a breaking change and therefore should be opt in"*. 같은 스레드에서 2026-07-05에 yakubka가 현재 상태를 요약했다.

> "FastAPI does not implement this automatically, but you can wire it up with a custom exception class and handler."

셋째, PR #15951(2026-07-07)은 제출된 날 그대로 닫혔다. 그런데 닫힌 사유가 중요하다. 기술적 반려가 아니었다.

> "let's keep it closed until maintainers can review the discussion and decide that we are going to add this feature... We are trying to keep things clean and ask to open PRs only when it's explicitly requested by maintainers."

"이 구현이 틀렸다"가 아니라 "메인테이너가 요청하기 전에 PR을 열지 말라"는 **프로세스 사유**다. 기능의 운명은 미정인 채 남았다.

세 사건을 이으면 **2019년의 7807 요청에서 2025년의 9457 논의로 7년째 이어지는 아크**가 보인다. 2026-07-25 시점에 확인한 사실은 이것이다 — **FastAPI 코어에 RFC 9457 지원은 없다.** "지원한다"도 틀리고 "거절됐다"도 틀린다. 7년째 열려 있는 요청이라고 쓰는 것이 정확하다. 이 상태는 바뀔 수 있으니 저장소의 최신 논의를 함께 확인하는 편이 낫다.

`ProblemDetail`은 프레임워크가 표준 포맷을 쥐여주는 물건이었다. 여기서는 아무도 쥐여주지 않는다. **그러니 우리가 정해야 한다.**

## 그래서 에러 계약은 이렇게 짓는다

먼저 필드 이름부터 정하자. 이 결정에는 이유가 있다.

`tracker`의 에러 응답은 `code`·`message`·`details`·`request_id`를 쓴다. RFC 9457의 `type`·`title`·`status`·`instance`를 의도적으로 피했다. 코어에 지원이 없다고 방금 확인해놓고 그 필드명을 그대로 가져다 쓰면 **코드가 시각적으로 표준 준수를 주장하게 되기 때문이다.** 미디어 타입도 `application/problem+json`이 아니고 `type`이 가리킬 문제 유형 URI도 없는데 이름만 같은 상태[^3-7] — 가장 나쁜 종류의 오해를 심는다. 표준을 따를 생각이라면 이름이 아니라 계약 전체를 따라야 하고, 아니라면 이름을 빌리지 않는 편이 정직하다.

두 계약을 나란히 놓으면 이렇게 대응한다.

| RFC 9457 | `tracker` | 비고 |
|---|---|---|
| `type` | `code` | URI 대신 점 구분 도메인 코드 (`issue.not_found`) |
| `title` · `detail` | `message` | 사람이 읽는 한 문장 |
| `status` | (없음) | HTTP 상태 줄과 중복 회피 |
| `instance` | `request_id` | 요청 추적 키 |

스키마는 이렇다.

> **📐 저자 설계 —** 아래 응답 스키마와 예외 계층은 FastAPI가 제공하는 것이 아니라 이 책이 `tracker`의 계약으로 정한 것이다.

```python
# src/tracker/schemas/common.py
from typing import Generic, TypeVar

from pydantic import BaseModel

ItemT = TypeVar("ItemT")


class ErrorDetail(BaseModel):
    field: str | None = None
    reason: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] | None = None
    request_id: str


class Page(BaseModel, Generic[ItemT]):
    items: list[ItemT]
    total: int
    limit: int
    offset: int
```

이름 하나를 짚고 가자. FastAPI `HTTPException`의 기본 본문은 `{"detail": ...}`, **단수**다.[^3-4] 위 스키마의 `details`는 **복수이자 리스트**이고 필드 단위 위반 사유를 담는다. 철자가 비슷할 뿐 다른 물건이니 지금 구분해두자.

에러의 종류는 예외 계층으로 표현한다. 루트는 `TrackerError` 하나, 그 아래 도메인 규칙 위반(`DomainError`)과 외부 의존 실패(`InfrastructureError`)로 갈린다.

```python
# src/tracker/errors.py
from fastapi import status

from tracker.schemas.common import ErrorDetail


class TrackerError(Exception):
    code: str = "internal.error"
    http_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: list[ErrorDetail] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details
        if code is not None:
            self.code = code


class DomainError(TrackerError): ...


class NotFoundError(DomainError):
    code = "not_found"
    http_status = status.HTTP_404_NOT_FOUND


class PermissionDeniedError(DomainError):
    code = "permission_denied"
    http_status = status.HTTP_403_FORBIDDEN


# ConflictError(409) · ValidationFailedError(422) 도 같은 형태다.
# InfrastructureError 아래에는 ExternalServiceError(502) · StorageError(503) 가 온다.
```

클래스 속성이 기본 코드를 들고, 발생 지점에서 `NotFoundError("이슈가 없다", code="issue.not_found")`처럼 도메인을 붙여 좁힌다. 상태 코드는 `fastapi.status` 상수로 적는다 — Starlette에서 그대로 온 것들이다.[^3-5]

핸들러는 **딱 세 개**다. `TrackerError`, `RequestValidationError`, 마지막 방어선인 `Exception`. 셋 다 `ErrorResponse`를 돌려준다. 어떤 기능이 붙어도 네 번째를 만들지 않는 것이 이 계약의 핵심이다 — 핸들러가 늘어나면 응답 모양이 갈라진다.

```python
# src/tracker/main.py
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from tracker.errors import TrackerError
from tracker.schemas.common import ErrorDetail, ErrorResponse

app = FastAPI(title="tracker")


def _error(request: Request, code: str, message: str,
           details: list[ErrorDetail] | None = None) -> ErrorResponse:
    return ErrorResponse(
        code=code,
        message=message,
        details=details,
        request_id=getattr(request.state, "request_id", ""),
    )


@app.exception_handler(TrackerError)
async def handle_tracker_error(request: Request, exc: TrackerError) -> JSONResponse:
    body = _error(request, exc.code, exc.message, exc.details)
    return JSONResponse(status_code=exc.http_status, content=body.model_dump())


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        ErrorDetail(field=".".join(str(p) for p in err["loc"]), reason=err["msg"])
        for err in exc.errors()
    ]
    body = _error(request, "request.validation_failed", "요청을 검증하지 못했다", details)
    return JSONResponse(status_code=422, content=body.model_dump())
```

`request.state`에서 꺼내는 `request_id`는 4장에서 미들웨어가 심을 값이다.[^3-6] 지금 비어 있어도 계약의 모양은 확정된다. 마지막 방어선은 어떤 예외가 새어 나오든 같은 스키마로 감싸 500을 돌려주는 핸들러 하나면 된다 — 코드는 `internal.error`, 메시지는 내부 정보를 감춘 고정 문구로.

선을 그을 차례다. **`/docs`와의 충돌은 어디까지 감수할 것인가.** 위 설계는 검증 실패의 상태 코드를 422로 유지한다. 앞 절에서 봤듯 상태 코드를 옮기는 순간 자동 문서를 따라오게 만드는 비용이 붙는다. 대신 **본문 모양은 우리 것으로 바꾼다.** 그 결과 `/docs`의 422 스키마와 실제 응답 본문이 어긋난다. 알고 지불하는 비용이다.

메울 방법은 있다. 경로 데코레이터의 `responses` 인자에 422 응답 스키마를 `ErrorResponse`로 명시하면 문서와 실제가 다시 만난다. 라우터 단위로 한 번 정의해 재사용하자. 다만 여기서 멈추는 편이 낫다. 소스를 고치거나 전역 변수를 덮어써 마지막 한 칸까지 맞추는 일은 **비용이 급격히 오르는 구간**이고, 그 구간을 걸어간 기록이 #1376이다.

이 계약은 책 끝까지 바뀌지 않는다 — 10장에서 인가 실패를 다룰 때도 새 예외 없이 `PermissionDeniedError`를 다시 쓴다.

---

에러 응답 계약은 대개 프로젝트 후반에 급하게 정해지고, 그때는 이미 클라이언트가 파싱하고 있어 되돌리기 어렵다. 라우터가 아직 둘뿐인 지금 정해두자. 계약을 먼저 정하고 코드를 늘리는 편이 훨씬 싸다.

[^3-1]: `BaseModel`·`Field`·`ConfigDict`와 `Generic`을 함께 상속하는 제네릭 모델 선언 — Pydantic 공식 문서 Models, https://pydantic.dev/docs/validation/latest/concepts/models/ (조회 2026-07-26)

[^3-2]: `model_dump(exclude_unset=)` — Pydantic 공식 문서 Serialization(*"any field that was not explicitly provided will be excluded"*), https://pydantic.dev/docs/validation/latest/concepts/serialization/ · FastAPI 공식 문서 Body - Updates (조회 2026-07-26)

[^3-3]: 내장 제약 애너테이션 목록과 적용 위치(*"a field, method, or class"*) — Jakarta EE Tutorial, https://jakarta.ee/learn/docs/jakartaee-tutorial/current/beanvalidation/bean-validation/bean-validation.html (조회 2026-07-26)

[^3-4]: `HTTPException`의 기본 본문 `{"detail": ...}`, `@app.exception_handler`, `fastapi.exceptions.RequestValidationError`·`exc.errors()`, `fastapi.responses.JSONResponse`, `from fastapi import Request` — FastAPI 공식 문서 Handling Errors, https://fastapi.tiangolo.com/tutorial/handling-errors/ (조회 2026-07-26)

[^3-5]: `from fastapi import status`. 축자 *"FastAPI provides the same `starlette.status` as `fastapi.status`"* — FastAPI 공식 문서 Response Status Code, https://fastapi.tiangolo.com/tutorial/response-status-code/ (조회 2026-07-26)

[^3-6]: *"If you want to store additional information on the request you can do so using `request.state`."* — Starlette 공식 문서 Requests, https://www.starlette.io/requests/ (조회 2026-07-26)

[^3-7]: 미디어 타입 `application/problem+json`과 멤버 이름 — RFC 9457 *Problem Details for HTTP APIs*(2023-07) §3, https://www.rfc-editor.org/rfc/rfc9457.html (조회 2026-07-26)
