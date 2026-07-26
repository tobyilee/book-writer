# 2장. 라우팅과 앱 구조 — `@RestController`가 사라진 자리

경로 하나를 여는 일만큼 프레임워크 사이에서 서로 닮아 보이는 작업이 또 있을까? 애너테이션이든 데코레이터든 `router.get(...)`이든, 결국 "이 URL로 요청이 오면 이 함수를 불러라"라는 한 줄이다. 실제로 컨트롤러를 쓰던 손으로 FastAPI의 첫 엔드포인트를 여는 데는 5분이 걸리지 않는다. 여기까지는 이사가 순조롭다.

그런데 왜 FastAPI 앱은 유독 커질수록 구조를 다시 짜게 될까? 파일이 열 개를 넘어가는 순간 어제까지 멀쩡하던 배치가 갑자기 어색해지고, 팀 안에서 누군가는 서비스 레이어를 만들자고 하고 누군가는 그게 과하다고 한다. 라우팅이 정말 그렇게 만만한 영역이었다면, 이 논쟁은 왜 끝나지 않을까?

답의 절반은 데코레이터 한 줄이 실제로 무엇을 떠맡고 있는지를 보면 드러난다. 거기서부터 시작하자.

## 데코레이터 한 줄이 떠맡는 것

`@app.get`·`@app.post`·`@app.put`·`@app.delete` 같은 경로 데코레이터들은 이름만 다르고 **받는 파라미터가 완전히 동일**하다. 0.140.0 태그 소스에서 그 목록을 통째로 뽑아봤다. 세지 말고, 우선 덩어리째 눈으로 훑어보자.

```text
path, response_model, status_code, tags, dependencies, summary, description,
response_description, responses, deprecated, operation_id,
response_model_include, response_model_exclude, response_model_by_alias,
response_model_exclude_unset, response_model_exclude_defaults, response_model_exclude_none,
include_in_schema, response_class, name, callbacks, openapi_extra,
generate_unique_id_function
```

> 출처: fastapi 0.140.0 태그 소스 `fastapi/routing.py`·`applications.py` AST 추출 (조회 2026-07-25)

이제 세어보자. 스물세 개 중에 **라우팅에 관한 것은 사실상 `path` 하나뿐**이다. `response_model`과 그 뒤에 딸린 `response_model_*` 여섯 개는 직렬화 계약, `status_code`는 응답 코드 계약, `response_class`는 전송 계층의 선택이다. `tags`·`summary`·`description`·`response_description`·`responses`·`operation_id`·`deprecated`·`include_in_schema`·`openapi_extra`는 전부 문서를 위한 것이고, `dependencies`는 인가와 공통 전처리의 자리다(4장에서 제대로 다룬다).

당신이 지나온 세계에서 이 책임들은 흩어져 있었을 것이다. URL 매핑은 매핑 애너테이션에, 직렬화 규칙은 객체 매퍼 설정에, 문서는 문서 생성 라이브러리의 애너테이션에, 공통 전처리는 인터셉터나 필터 체인에. 그것들이 여기서는 한 줄에 모여 있다.

좋은 일일까, 나쁜 일일까? 둘 다다. 좋은 쪽은 명백하다. 이 엔드포인트가 무엇을 받고 무엇을 돌려주며 문서에 어떻게 나타나는지가 한눈에 들어온다. 나쁜 쪽은 조금 뒤에 온다. 한 줄이 이렇게 많은 일을 하면 그 한 줄은 프로젝트에서 가장 붐비는 곳이 되고, 인자가 다섯 개 붙은 데코레이터 아래에 스무 줄짜리 함수가 앉아 있는 모습을 몇 번 보고 나면 뒷맛이 찜찜해진다. 이 파일은 무엇을 담당하는가? 라우팅인가, 직렬화인가, 문서인가, 비즈니스 로직인가?

— 여기서부터는 **저자 가설**이다. 경로 함수가 비대해지는 것은 게으름이 아니라 **경계가 선언되지 않았기 때문**이라고 나는 본다. 프레임워크가 "여기까지가 라우팅이다"라고 그어주지 않으면 코드는 가장 가까운 곳에 쌓인다. 그리고 가장 가까운 곳은 언제나 경로 함수다.

그래서 이 장이 하는 일은 그어지지 않은 경계를 어디에 그을지 정하고, 그 결정을 골격으로 굳히는 것이다. 참고로 `tags`는 데코레이터에도 있고 라우터에도 있는데, `tracker`는 **라우터 레벨에서 한 번만** 지정한다. 곧 이유가 나온다.

## 라우터를 쪼개면 무엇이 남는가

앱을 나누는 도구는 `APIRouter`다. 생성자에 `prefix`·`tags`·`dependencies`를 줄 수 있고, 그 라우터에 달린 모든 경로가 그 값을 물려받는다. 구조만 놓고 보면 클래스 레벨 매핑이 하던 일, Express의 `Router()` 객체를 만들어 마운트하던 일과 같은 자리다.

그런데 결정적으로 다른 게 하나 있다. **클래스가 없다.**

지금까지 그룹의 단위는 늘 클래스였다. 컨트롤러 클래스 하나가 곧 하나의 묶음이었고, 클래스가 커지면 "이 클래스가 너무 크다"는 신호가 자연스럽게 왔다. 필드도 생성자도 클래스에 매달려 있으니, 무엇이 이 그룹의 소유인지도 문법이 알려줬다. FastAPI의 `APIRouter`는 그냥 모듈 안에 놓인 객체다. 파일이 곧 경계이고, 그 파일에 무엇을 넣을지 정해주는 문법적 상한이 없다.

여기서 한 가지 함정을 짚고 가자. `FastAPI.include_router`와 `APIRouter.include_router`는 파라미터 순서가 다르다. 이름이 같고 하는 일도 같아 보여서 손이 무심코 위치 인자로 가는데, 두 곳에서 같은 자리가 다른 뜻이 될 수 있다는 뜻이다. 이런 종류의 버그는 조용히 잘못된 라우터를 등록하고 며칠 뒤에 발견되기 때문에 정말 난감하다. 규칙 하나로 끝내자 — **등록은 언제나 키워드 인자로.**

`tracker`의 첫 라우터는 이렇게 생겼다.

> **📐 저자 설계 —** 아래 라우터 배치와 모듈 이름은 FastAPI 공식 권장이 아니라, 이 책이 `tracker`를 위해 정한 한 가지 안이다.

```python
# src/tracker/api/issues.py
from fastapi import APIRouter

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("/{issue_id}")
async def get_issue(issue_id: int) -> dict:
    ...


@router.post("/", status_code=201)
async def create_issue() -> dict:
    ...
```

형제 라우터도 정확히 같은 모양이다. 도메인 이름만 갈아 끼운다.

```python
# src/tracker/api/projects.py
from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])
```

변수명이 `issues_router`가 아니라 두 파일 모두 그냥 `router`인 게 눈에 걸릴 수 있다. 의도한 것이다. 모든 라우터 모듈이 같은 이름을 쓰고, 별칭은 등록하는 쪽에서 준다. 그래야 새 도메인을 추가할 때 파일 안에서 고민할 게 없다.

```python
# src/tracker/main.py
from fastapi import FastAPI

from tracker.api.issues import router as issues_router
from tracker.api.projects import router as projects_router

app = FastAPI(title="tracker")

# ...(1장, 생략)

app.include_router(router=projects_router)
app.include_router(router=issues_router)
```

지금 이 경로 함수들의 몸통이 `...`인 건 오타가 아니라 진짜 스텁이다. 돌려줄 스키마는 3장에서, 세션과 서비스를 건네받는 배선은 4장에서, 실제 쿼리는 6장에서 채운다. 반환 타입이 `dict`인 것도 마찬가지로 임시다 — 3장이 응답 스키마를 정하면서 함께 바뀐다. 앱은 이렇게 층층이 자란다.

그리고 경로에 `/api/v1` 같은 접두사가 없다는 것도 의도다. API 버저닝 전략은 이 책이 다루지 않겠다고 선언한 주제이고, 다루지 않기로 한 것을 코드가 슬쩍 주장하게 두면 안 된다.

## 서비스 레이어를 둘 것인가

여기가 이 장에서 가장 정답이 없는 대목이다.

3계층 — 컨트롤러, 서비스, 리포지터리 — 은 당신에게 관례였을 것이다. 관례라는 말의 뜻은, 그 배치를 아무도 변호할 필요가 없었다는 것이다. FastAPI에는 그런 관례가 없고, 이 사실이 실제로 사람들을 갈라놓는다.

한쪽 목소리는 이렇다. rmonvfer는 공식 템플릿이 CRUD를 한 파일에 몰아넣은 것을 보고 *"started cringing"*이라고 적었고, 결론은 *"I wouldn't recommend it for anything serious... not without requiring you to write a framework on top, like I've unfortunately done"*였다(HN, 2025-08-06). 구조가 필요해서 결국 프레임워크 위에 프레임워크를 하나 더 얹었다는 고백이다.

반대쪽 입장도 있다. 얇은 라우터에 로직을 직접 쓰는 게 파이썬답다는 주장이다. 다만 정직하게 밝혀두자. **이 책의 리서치는 그 반대쪽에서 인용할 만한 원문 발언을 확보하지 못했다.** 입장이 존재한다는 것까지는 확인했지만, 위 인용문과 나란히 놓을 무게의 근거는 없다.

게다가 위 발언은 HN의 단일 스레드에서 나왔고, 그 스레드는 "Litestar를 봐라"는 글에 달린 댓글들이다. FastAPI를 떠나기로 한 사람이 구조적으로 과대표집된 표본이라는 뜻이다. 그래서 나는 "실무자들은 서비스 레이어를 둔다"고도, "요즘은 안 둔다"고도 쓸 수 없다. 조용히 잘 쓰고 있는 다수는 어느 스레드에도 나타나지 않는다.

자주 함께 인용되는 mattmanser의 발언 — *"to add one property I had to edit 40 files... It's anti-patterns like that which give statically typed languages a bad name."* — 은 사실 다른 축이다. 계층을 나눈 것 자체가 아니라, 계층마다 자료형을 복제해두는 관행을 탓한다.

그렇다면 무엇을 기준으로 정할까? 다수설이 없으니 기준을 직접 세우는 수밖에 없다. 아래는 **저자 기준**이다.

- 같은 도메인 규칙에 진입점이 둘 이상 생기면 서비스를 둔다. 이슈 상태 변경이 REST에서도 일어나고 백그라운드 작업에서도 일어난다면, 그 규칙은 이미 라우터의 것이 아니다.
- 트랜잭션 경계가 요청 경계와 어긋나면 서비스를 둔다. 한 요청 안에서 두 개의 커밋 단위가 필요하거나, 반대로 여러 단계를 하나로 묶어야 한다면 그 경계를 가질 객체가 필요하다. 이 이야기는 6장에서 정면으로 다시 만난다.
- 엔드포인트가 한 테이블에 대한 CRUD 그대로라면 두지 않는다. 이때의 서비스는 인자를 그대로 넘기는 전달자만 늘린다.
- 테스트에서 HTTP를 거치지 않고 검증하고 싶은 규칙이 생기면 두는 편이 낫다. 설계 취향이 아니라 11장에서 실제로 값을 치르게 되는 문제다.

넷 다 "구조가 아름다운가"를 묻지 않고 **로직에 두 번째 소비자가 있는가**를 묻는다. 소비자가 하나뿐인 로직에 층을 만드는 것은, 아직 오지 않은 손님을 위해 방을 비워두는 일이다.

## 그래서 `tracker`는 이 골격으로 간다

기준을 세웠으니 골격을 정하자. 앞으로 열두 장이 이 위에 쌓인다.

> **📐 저자 설계 —** 아래 디렉터리 배치는 FastAPI가 정해주는 구조가 아니라, 위 기준에서 이 책이 도출한 한 가지 안이다.

```text
src/tracker/
├── main.py            # FastAPI 인스턴스 · 라우터 등록
├── settings.py        # Settings · get_settings
├── api/               # 라우터 — HTTP 어휘
│   ├── projects.py
│   └── issues.py
├── services/          # 도메인 어휘
│   ├── project.py
│   └── issue.py
└── repositories/      # 영속화 어휘
    ├── project.py
    └── issue.py
```

주석에 적은 "어휘"라는 말이 이 배치의 전부다. 세 층은 위치로 구분되는 게 아니라 쓰는 단어로 구분된다. 리포지터리는 `get`·`list`·`add`·`delete`처럼 저장소의 말을 쓴다. 서비스는 `create_issue`·`assign_issue`·`change_status`처럼 도메인의 말을 쓴다. 어떤 층에 메서드를 추가할지 헷갈린다면, 그 메서드 이름이 어느 사전에 실려 있는지를 보면 된다.

> **📐 저자 설계 —** 아래 두 클래스는 생성자 모양만 확정한 골격이다. 실제 쿼리는 6장이 채운다.

```python
# src/tracker/repositories/issue.py
from sqlalchemy.ext.asyncio import AsyncSession


class IssueRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, issue_id: int) -> None:
        ...

    async def list(self, project_id: int) -> None:
        ...
```

```python
# src/tracker/services/issue.py
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.repositories.issue import IssueRepository


class IssueService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.issues = IssueRepository(session)

    async def create_issue(self, project_id: int, title: str) -> None:
        ...

    async def change_status(self, issue_id: int, status: str) -> None:
        ...
```

> 출처: `AsyncSession`의 import 경로 `sqlalchemy.ext.asyncio`는 SQLAlchemy 2.0 asyncio 확장 문서에서 확인했다 — 원문이 `from sqlalchemy.ext.asyncio import AsyncSession`·`create_async_engine`을 그대로 싣는다. https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html (조회 2026-07-26)

반환 타입이 전부 `None`인 게 어색할 것이다. 돌려줄 타입이 아직 이 세상에 없기 때문이다 — 응답 스키마는 3장, 엔티티는 6장에서 생긴다. 특히 `list()`는 이름만 보면 목록을 돌려줄 것 같은데 `-> None`이라 오류처럼 읽히는데, 그것도 6장이 채울 자리다. 지금 확정한 것은 이름과 생성자 모양뿐이다.

그 생성자를 한 번 더 보자. 두 클래스 모두 `session: AsyncSession` 하나만 받는다. 세션을 **어디서** 얻는지는 여기 없다. 그건 4장의 일이고, 세션이 실제로 무엇을 하는지는 6장의 일이다. 이 순서가 중요하다. 골격을 세울 때 데이터베이스 연결까지 한꺼번에 결정하려 들면, 아직 근거가 없는 판단을 지금 내려야 한다.

그렇다면 이 골격은 언제 버려야 할까? 세 가지 신호를 기억해두자. 첫째, 서비스 메서드가 리포지터리 메서드를 그대로 한 번 더 부르기만 하는 파일이 셋 이상 쌓이면 그 층은 값을 못 하고 있다. 둘째, 라우터가 서비스를 건너뛰고 리포지터리를 직접 부르는 일이 잦아지면 경계가 이미 틀린 것이니 층을 지키려 애쓰지 말고 경계를 다시 그어야 한다. 셋째, 서비스 하나가 리포지터리를 다섯 개씩 들고 다니면 도메인 경계와 파일 경계가 어긋난 것이다. 골격은 지키라고 있는 게 아니라 **틀렸을 때 알아채라고** 있다.

## 설정은 어디에 두는가

프로젝트 골격의 나머지 절반은 설정이다. 여기서 쓸 도구는 `pydantic-settings`(2.14.2 / 2026-06 기준)다. 1장에서 훑어본 `[standard]` extra의 의존성 목록에 이미 들어 있으니, 따로 고르고 말고 할 것도 없다.

기능만 놓고 보면 자리는 익숙하다. 외부화된 설정 파일 + 타입 있는 설정 객체 + 환경 변수 오버라이드, 이 세 가지가 하던 일을 한 클래스가 한다. 다만 체감이 어떻게 다른지는 이 책이 말하지 않겠다 — 두 방식을 실제로 비교한 근거를 찾지 못했고, 없는 비교를 지어내는 것보다 기능 대응만 짚는 편이 정직하다.

> **📐 저자 설계 —** 필드 이름과 `TRACKER_` 접두사는 이 책이 `tracker`를 위해 확정한 것이다. 이후 어떤 장도 이 이름을 바꾸지 않는다.

```python
# src/tracker/settings.py
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TRACKER_", env_file=".env")

    app_name: str = "tracker"
    environment: str = "local"
    debug: bool = False
    log_level: str = "INFO"
    database_url: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

> 출처: `pydantic_settings`의 `BaseSettings`·`SettingsConfigDict` import 경로와 `env_prefix`·`env_file` 인자는 pydantic-settings 공식 문서 "Settings Management"에서 확인했다. https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/ (조회 2026-07-26)

읽을 게 몇 가지 있다. `env_prefix="TRACKER_"`는 `database_url` 필드가 환경 변수 `TRACKER_DATABASE_URL`에서 온다는 뜻이다. 접두사를 두는 이유는 단순하다 — 컨테이너 안에는 내 앱이 정한 적 없는 환경 변수가 잔뜩 떠다니고, 그중 하나가 내 필드 이름과 겹치는 사고는 겪고 나면 오래 기억에 남는다.

`database_url`만 기본값이 없다는 것도 의도다. 기본값은 "없으면 이걸로 간다"는 뜻인데, 데이터베이스 주소에 그런 관용은 위험하다. 값이 없으면 **앱이 뜨는 순간 죽는 편이 낫다.** 새벽 세 시에 엉뚱한 데이터베이스를 바라보며 도는 서버를 발견하는 것보다는 훨씬 낫다.

`environment`는 `local`·`ci`·`staging`·`production` 넷 중 하나를 담는다. 환경별 분리는 이 필드와 `env_file`의 조합으로 처리한다 — 파일을 갈아 끼우고, 그 위를 실제 환경 변수가 덮는다. `get_settings()`의 `lru_cache`는 이 객체를 한 번만 만들기 위한 것이다.

여기 **없는** 것도 짚어두자. 워커 수는 `Settings`에 들어가지 않는다. uvicorn이 읽는 것은 접두사가 붙지 않은 `$WEB_CONCURRENCY`라서, `TRACKER_` 세계로 끌고 들어오면 진실이 두 개가 된다. 이 이야기는 13장에서 프로세스 모델과 함께 다시 꺼낸다. 시크릿을 얹는 방법은 10장의 몫이다.

## 배당금은 자동 문서로 들어온다

지금까지 정한 것 — 라우터 접두사, 태그, 상태 코드 — 이 아무 추가 작업 없이 곧바로 값을 치르는 자리가 있다. `/docs`다.

FastAPI가 생성하는 스펙의 버전은 **OpenAPI 3.1.0**으로 고정돼 있다(`applications.py`가 문자열로 박아둔다). 필요하면 `app.openapi_version`으로 낮춰 잡을 수는 있다. 여기서 중요한 건 버전 숫자 자체가 아니라, **스펙이 코드에서 파생된다**는 사실이다.

OpenAPI 문서는 원래 **얹는** 것이었다. 문서 생성 라이브러리를 의존성에 추가하고, 애너테이션을 달고, 그것이 실제 구현과 어긋나지 않도록 사람이 관리했다. 문서가 코드보다 반 발짝 뒤처져 있는 상태를 당신도 여러 번 봤을 것이다.

FastAPI에서는 그 층이 없다. 라우터에 `tags=["issues"]`를 준 것이 `/docs`의 그룹이 되고, `status_code=201`이 스펙의 응답 코드가 된다. 태그를 라우터 레벨에서 한 번만 지정하기로 한 이유가 여기 있다 — 데코레이터마다 반복해서 적으면, 언젠가 한 곳만 다르게 적힌 채 문서에 그대로 드러난다.

`operation_id`도 같은 목록에 있는 파라미터다. 목록에 `generate_unique_id_function`이 함께 있다는 데서 짐작할 수 있듯, 지정하지 않으면 식별자가 만들어지고 지정하면 그 값이 스펙에 그대로 실린다. — 여기서부터는 **저자 서술**이다. 이 값이 실제로 중요해지는 건 스펙에서 클라이언트 코드를 뽑을 때다. 생성기가 만드는 함수 이름의 뿌리가 되기 때문에, 이름을 방치하면 스펙을 소비하는 쪽에서 읽기 어려운 식별자를 받게 된다. 다만 이 판단은 레퍼런스가 뒷받침하는 사실이 아니라 저자의 경험에서 나온 권고이니, 그렇게 받아들이면 된다.

물론 자동 문서가 공짜이기만 한 것은 아니다. 생성된 것을 원하는 모양으로 바꾸려 할 때 비용이 어디서 나오는지는 3장에서 아주 구체적으로 보게 된다. 지금 기억해둘 것은 하나다. **스펙은 이제 산출물이지 문서가 아니다.** 코드를 바꾸면 스펙이 바뀌고, 그 스펙을 누군가 이미 소비하고 있다.

## 그런데 그 라우터가 6월에 모양을 바꿨다

방금 우리는 라우터를 만들고 등록했다. 그 라우터의 내부 구조가 **0.137.0(2026-06-14)에서 바뀌었다.** 릴리스 노트의 축자는 이렇다.

> "Now `router.routes` is no longer a plain list of `APIRoute` objects, it can contain these intermediate objects that can contain additional routers, forming a tree.
> Any logic that depended on iterating on the `router.routes` directly would be affected..."

평평한 리스트가 트리가 됐고, 순회용 API가 함께 들어왔다 — `iter_route_contexts()`다.

라우터를 만들어 등록하기만 하는 코드에는 이 변경이 보이지 않는다. 문제는 **`router.routes`를 직접 훑던 코드**다. 메트릭 수집기, 문서 생성기, 라우트 감사 스크립트 — 라우트 목록을 읽어야 하는 도구에게는 그 리스트를 훑는 것 말고 방법이 없었다.

무슨 일이 있었는지는 기록으로 남아 있다. `trallnag/prometheus-fastapi-instrumentator` 저장소에 세 건의 이슈가 연달아 올라왔다.

| 이슈 | 날짜 | 무엇이 보고됐나 |
|---|---|---|
| #370 | 2026-06-14 | `AttributeError: '_IncludedRouter' object has no attribute 'path'` |
| #379 | 2026-06-25 | "Incompatible with certain router usage in FastAPI 0.137.0+" |
| #388 | 2026-07-08 | "Issue with FastAPI 0.138" |

날짜를 보자. 첫 보고가 릴리스와 같은 날이고, 열하루 뒤에 또, 첫 보고로부터 3주가 지나 다시 한 번이다. 이건 남의 저장소 이야기가 아니라, 당신이 관측성 도구를 붙이는 순간 당신의 이야기가 된다.

다만 정확해야 할 게 있다. **위 이슈들은 "깨졌다는 사실"의 근거이지, "무엇이 어떻게 바뀌었는지"의 근거가 아니다.** 이슈 본문에 적힌 버전 번호는 보고자가 자기 환경을 적어둔 것이라 호환성 판정으로 읽으면 안 된다. 무엇이 바뀌었는가는 릴리스 노트 축자만이 말해준다. 세 건이 지금 어떤 상태인지도 이 책은 단정하지 않는다 — 확인한 것은 저 날짜에 저런 보고가 있었다는 사실까지다.

그래도 남는 감각이 하나 있다. 마이너 릴리스 하나가 생태계의 도구를 멈춰 세울 수 있다는 것. 마이너 업그레이드는 대체로 안전한 일이었을 테고, 안전하지 않다면 그건 사고이지 정상 동작이 아니었을 것이다. 여기서는 전제가 다르다. **0.x 버전대의 마이너는 메이저가 하는 일을 한다.**

그러니 아찔하다고만 읽지는 말자. 겪은 고통이 다음 릴리스에서 API로 흡수되기도 하고, 그런 사례를 4장에서 만난다. 골라서 가질 수 없는 두 얼굴이다.

가져갈 것은 두 줄이다. `router.routes`를 직접 순회하는 코드는 내 것이든 남의 것이든 **버전에 결합된 코드**로 간주하자. 그리고 업그레이드 전에 릴리스 노트를 읽는 습관은, 월 3~5회 릴리스되는 프레임워크에서 취향이 아니라 비용 절감이다.

---

라우터를 나누고, 층을 정하고, 설정을 밖으로 꺼냈다. 겉보기에는 익숙한 3계층을 다시 지은 것 같지만, 실제로 우리가 한 일은 그게 아니다. **프레임워크가 정해주지 않는 경계를 처음으로 우리 손으로 그었다.** 그래서 이 골격에는 지켜야 할 규칙 대신, 틀렸을 때 알아채는 신호 세 개가 붙어 있다.

이제 그 라우터들이 무엇을 받고 무엇을 돌려주는지가 남았다. 지금 경로 함수들은 `dict`를 반환한다고 적혀 있고, 그건 아무것도 약속하지 않는다는 뜻이다. 이 API의 계약은 누가 정하는가?
