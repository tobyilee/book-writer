# 6장. 데이터 계층 — JPA를 놓고 SQLAlchemy 2.0을 잡기

새벽 두 시 사십 분, 휴대폰이 울린다. 이슈 상세 API가 500을 뱉고 있다.

로그를 연다. 스택 트레이스 맨 아래에 처음 보는 이름이 앉아 있다. `MissingGreenlet`. 검색해보면 greenlet이라는 라이브러리 이야기가 나오는데, 설치한 적이 없다. 이 코드는 로컬에서도 스테이징에서도 멀쩡했다. 어제 바뀐 것이라고는 상세 응답에 담당자 이름 한 줄을 넣은 것뿐이다.

ORM은 오래 써왔고 지연 로딩이 어떻게 도는지도 안다. 그런데 터진 건 성능 문제가 아니라 **예외**다. 관계 하나를 읽었을 뿐인데 애플리케이션이 죽었다.

이 예외는 버그가 아니라 계약이다. 읽으려면 매핑부터 봐야 한다.

## 엔티티를 옮기는 데는 오래 걸리지 않는다

매핑은 가장 쉽다. SQLAlchemy 2.0(2.0.51 / 2026-06 기준) 선언 스타일에서 눈여겨볼 것은 문서가 굵게 강조한 한 문장이다.

> "**Nullability derives from whether or not the `Optional[]` (or its equivalent) type modifier is used.**"

> 출처: SQLAlchemy 2.0 ORM Quickstart, https://docs.sqlalchemy.org/en/20/orm/quickstart.html (조회 2026-07-25)

널 허용 여부를 **애너테이션의 속성으로 적던 자리가 타입 그 자체**가 됐다. `Mapped[str]`이면 NOT NULL, `Mapped[str | None]`이면 NULL이다.[^6-1] 3장에서 Pydantic이 타입을 만들어내는 장치였던 것과 같은 발상이다. (문서가 `Optional[...]`이라 쓴 자리에 `tracker`는 `| None`을 쓴다 — 인용만 원문 그대로 둔다.)

> **📐 저자 설계 —** 아래 엔티티 구성과 컬럼 이름은 SQLAlchemy가 정해주는 것이 아니라 이 책이 `tracker`를 위해 확정한 것이며, 이후 어떤 장도 바꾸지 않는다.

```python
# src/tracker/models/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

`Base`는 하나뿐이고, 도메인은 엔티티 여섯에 연결 엔티티 둘이다.

| 클래스 | 테이블 | 핵심 컬럼 |
|---|---|---|
| `User` | `users` | `email` |
| `Project` | `projects` | `key` |
| `Issue` | `issues` | `title`·`status` |
| `Comment` | `comments` | `body` |
| `Label` | `labels` | `name`·`color` |
| `Attachment` | `attachments` | `storage_key` |
| `IssueLabel` | `issue_labels` | PK 2개 |
| `ProjectMember` | `project_members` | PK 2개 + `role` |

한 클래스만 전문으로 보자.

```python
# src/tracker/models/issue.py
import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tracker.models.base import Base


class IssueStatus(enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class IssuePriority(enum.Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[IssueStatus] = mapped_column(default=IssueStatus.open)
    priority: Mapped[IssuePriority] = mapped_column(default=IssuePriority.normal)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp()
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="issue", cascade="all, delete-orphan", lazy="raise"
    )
    labels: Mapped[list["IssueLabel"]] = relationship(
        back_populates="issue", cascade="all, delete-orphan", lazy="raise"
    )
```

두 가지만 짚자. `status: Mapped[IssueStatus]`에 타입 지정이 없다 — `enum.Enum`을 상속한 타입은 자동으로 SQLAlchemy의 `Enum`에 연결된다.[^6-1] 그리고 `lazy="raise"`는 이 장 나머지 절반을 요약한 한 단어다. 오프닝의 새벽 알림이 저기서 온다.

N:M은 연결 엔티티 클래스로 쓴다. 프로젝트 멤버십이 대표적이다.

```python
# src/tracker/models/project.py
import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tracker.models.base import Base


class ProjectRole(enum.Enum):
    member = "member"
    maintainer = "maintainer"
    owner = "owner"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(200))

    members: Mapped[list["ProjectMember"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", lazy="raise"
    )


class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role: Mapped[ProjectRole] = mapped_column(default=ProjectRole.member)

    project: Mapped["Project"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship()
```

왜 클래스로 올렸을까? `role` 때문이다. 연결에 정보가 붙으면 그건 이미 하나의 개념이고, 개념에는 이름을 주는 편이 낫다. 클래스 없이 잇는 직접형도 있지만[^6-2] `IssueLabel`까지 통일했다.

`Attachment`는 여기서 처음 정의한다. 5장의 썸네일 함수에는 저장할 곳이 없었고, 8장의 업로드가 쓴다.

```python
# src/tracker/models/attachment.py
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from tracker.models.base import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issues.id"), index=True)
    uploader_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int]
    storage_key: Mapped[str] = mapped_column(String(500), unique=True)
    thumbnail_key: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp()
    )
```

파일 바이트는 여기 없다. 데이터베이스가 드는 것은 어디에 있는지와 **무엇인지**뿐이고, 저장소는 8장의 몫이다.

## SQLAlchemy `Query`가 레거시가 되면서 바뀐 것

조회를 채울 차례다. 2.0이 1.x의 조회 어휘를 통째로 밀어놨기 때문에 인터넷 예제와 여기서 갈린다.

> "The `Query` object (as well as the `BakedQuery` and `ShardedQuery` extensions) **become long term legacy objects**, replaced by the direct usage of the `select()` construct in conjunction with the `Session.execute()` method."

문자열로 관계 이름을 넘기던 로딩 옵션도 2.0에서 제거됐다. 예제가 `session.query(...)`로 시작하거나 로딩 옵션에 따옴표가 있으면 **다른 세계의 코드**다.

```python
# (개념 설명용 — 파일 아님)
# ✅ 2.0 스타일
result = await session.scalars(select(Issue).where(Issue.project_id == project_id))
issues = result.all()

# ❌ 1.x 어휘 — 인터넷 예제 다수가 아직 여기 있다
issues = session.query(Issue).filter(Issue.project_id == project_id).all()
```

`execute()`와 `scalars()`도 정하자. `Row` 생성을 건너뛰고 ORM 엔티티를 직접 받으려면 `Session.scalars()`가 가장 쉽다.[^6-3] 컬럼 몇 개만 뽑을 때는 `execute()`의 튜플이 맞다. `tracker`의 리포지터리는 `scalars()`가 기본형이고, 개수는 `select(func.count()).select_from(Issue)`를 `session.scalar()`에 넘겨 센다.

2장에서 반환 타입이 전부 `None`이던 그 리포지터리를 이제 채운다.

> **📐 저자 설계 —** 아래 리포지터리·서비스·라우터는 공식 권장이 아니라 이 책이 정한 배치다.

```python
# src/tracker/repositories/issue.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from tracker.models.issue import Issue


class IssueRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, issue: Issue) -> None:
        self.session.add(issue)

    async def get(self, issue_id: int) -> Issue | None:
        stmt = (
            select(Issue)
            .where(Issue.id == issue_id)
            .options(selectinload(Issue.comments))
        )
        return await self.session.scalar(stmt)

    async def list(self, project_id: int, limit: int, offset: int) -> list[Issue]:
        stmt = (
            select(Issue)
            .where(Issue.project_id == project_id)
            .order_by(Issue.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return list(result)
```

`get()`에는 `selectinload`가 있고 `list()`에는 없다. 의도적이다. **무엇을 함께 가져올지를 쿼리마다 결정한다** — 이 장 후반부가 이 결정에 매달려 있다. `add()`는 세션에 객체를 얹기만 한다.[^6-4] 커밋은 서비스가 한다.

```python
# src/tracker/services/issue.py
from tracker.models.issue import Issue


class IssueService:
    # ...(2장, 생략)

    async def create_issue(self, project_id: int, title: str, author_id: int) -> Issue:
        issue = Issue(project_id=project_id, title=title, author_id=author_id)
        await self.issues.add(issue)
        await self.session.commit()
        return issue
```

마지막 두 줄이 다음 절의 주제다. 라우터도 둘 생긴다.

```python
# src/tracker/api/comments.py
from typing import Annotated

from fastapi import APIRouter, Query

from tracker.deps import SessionDep
from tracker.schemas.comment import CommentRead  # 3장의 네 접미사 규약 그대로, 여기서는 생략
from tracker.schemas.common import Page

router = APIRouter(prefix="/issues/{issue_id}/comments", tags=["comments"])


@router.get("", response_model=Page[CommentRead])
async def list_comments(
    issue_id: int,
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[CommentRead]:
    ...
```

여기 `Query`는 FastAPI의 파라미터 선언이지 방금 레거시가 됐다고 한 그 `Query`가 아니다. `api/labels.py`도 같은 모양이고 접두사만 `/labels`다. 세션이 `SessionDep` 한 단어로 들어오는 데 주목하자 — 그 뒤가 남은 주제다.

## 새벽 두 시 사십 분의 `MissingGreenlet`

이제 오프닝으로 돌아가자. `MissingGreenlet`이 무엇인지는 공식 문서가 정의해준다.

> "A call to the async DBAPI was initiated outside the greenlet spawn context... **When using the ORM this is nearly always due to the use of lazy loading**, which is not directly supported under asyncio"

**지연 로딩은 asyncio에서 직접 지원되지 않는다.** 관계 속성에 접근하면 조용히 쿼리를 한 번 더 날리던 동작이, 여기서는 `await` 없이 I/O를 시작하려는 시도가 되어 예외가 된다.

그러면 왜 로컬에서는 멀쩡했을까? 지연 로딩은 접근할 때 터지지 선언할 때 터지지 않는다. 응답 스키마가 그 관계를 밟지 않으면 코드는 몇 달이고 무사히 돈다. 원인은 어제의 한 줄이 아니라 **아무도 밟지 않았던 경로**다.

여기서 원인을 사람에게 돌리고 싶은 유혹이 생기는데, 그건 이 책이 하지 않는 서술이다. 확인된 건 코드의 동작뿐이다.

처방은 네 가지이고 전부 공식 문서에 있다. 중요한 건 대가다.

첫째, `selectinload`로 미리 가져온다. 문서는 컬렉션 즉시 로딩에서 이 방식이 대체로 가장 단순하고 효율적이라고 말한다.[^6-3] 대가는 **결정을 쿼리마다 내려야 한다**는 것이다.

둘째, `AsyncAttrs`를 섞고 `awaitable_attrs`로 접근한다. `Base`에 믹스인을 더 상속시키면 관계 속성을 `await`로 읽을 수 있다.[^6-5] 코드는 돌아가지만 **N+1은 그대로 남는다** — 문제를 조용한 쪽으로 옮긴다.

셋째, `expire_on_commit=False`로 세션을 만든다. 처방이라기보다 asyncio의 기본 설정에 가깝다. 문서는 asyncio에서 이 값을 `False`로 두면 커밋 이후에도 속성에 접근할 수 있다고 설명한다.[^6-5] 뒤집어 읽으면, 기본값대로 두면 커밋 직후 속성이 만료돼 직렬화 중 같은 예외를 만난다.

넷째, `run_sync`로 동기 코드를 감싼다. 문서가 스스로 붙인 평가가 인상적이다 — 이 접근은 *"probably be considered 'controversial'"*하며 asyncio 모델의 철학과 충돌한다는 것이다. 마지막에 꺼내자.

`tracker`가 고른 조합은 첫째와 셋째, 그리고 `lazy="raise"`다. 이 설정은 지연 로딩이 일어날 그 시점에 예외를 던진다.[^6-3] 프로덕션에서 만날 사고를 개발 중 첫 실행에서 만나게 하는 것이다. 성가시지만 새벽 두 시 사십 분보다는 낫다.

비동기 세션이 요구하는 것이 하나 더 있다.

> "**Warning:** A single instance of `AsyncSession` is not safe for use in multiple, concurrent tasks."

`asyncio.gather()`처럼 동시 태스크를 쓴다면 태스크마다 별도의 `AsyncSession`을 써야 한다. 두 조회를 병렬로 돌리겠다는 생각은 자연스럽지만, 둘이 세션을 나눠 쓰는 순간 안전 범위 밖이다. 5장의 프로세스 경계 안쪽에 경계가 하나 더 있다 — **태스크도 세션을 공유하지 않는다.**

부수 사항 둘. 비동기 ORM은 greenlet에 의존하는데 일부 플랫폼에는 기본 설치되지 않는다. 종료 시 `await engine.dispose()`를 빠뜨리면 `RuntimeError: Event loop is closed`가 난다.[^6-5]

## `@Transactional`이 있던 자리

이 장의 핵심 질문이다. 애너테이션 한 줄로 끝나던 일을 누가 하는가?

그 한 줄이 무엇을 묶어 놓았는지 풀어보자. 세션을 열고, 트랜잭션을 시작하고, 메서드가 끝나면 커밋하거나 롤백하고, 세션을 닫는다. 결정 넷이 한 표시 아래 접혀 있었다. 그래서 편했고, 어디서 무엇이 일어나는지 물어볼 일도 없었다.

여기서는 그 넷을 각각 어디에 둘지 직접 정한다. 트랜잭션 경계를 어디까지 늘릴 것인가, 화면을 그리는 동안에도 세션을 열어둘 것인가 — 겪어본 질문이 기본값 없이 온다.

`tracker`의 답은 두 문장이다. **의존성은 세션의 생명주기만 책임진다. 커밋은 서비스 계층이 한다.**

> **📐 저자 설계 —** 아래 세션·트랜잭션 배선은 공식 권장이 아니라 이 장의 논의에서 도출한 한 가지 안이다.

```python
# src/tracker/db.py
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from tracker.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
```

4장의 `get_session` 스텁이 여기로 옮겨온다. 시그니처는 그대로다.

```python
# src/tracker/deps.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.db import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
# ...(4장, 생략)
```

이 함수에 `commit()`이 없다는 게 핵심이다. 의존성이 커밋을 대신하면 트랜잭션 경계가 곧 요청 경계가 된다. 요청 하나가 트랜잭션 하나라는 규칙은 단건 엔드포인트에서는 편하지만, 한 요청이 독립적인 작업 둘을 처리하면 어긋난다. 첫 작업이 성공하고 둘째가 실패했을 때 첫 작업까지 되감을지는 **도메인이 답할 질문**이다.

그래서 규칙이 정리된다. 서비스 메서드 하나가 트랜잭션 하나이고, 라우터도 리포지터리도 트랜잭션을 모른다. 2장에서 서비스 계층을 둘지 고민한 결정이 값을 한다.

그런데 세션이 언제 닫히는가는 남아 있다. 0.140.0 / 2026-07 기준으로 `Depends`에는 `yield` 정리 코드가 도는 시점을 고르는 파라미터가 있다.

> `"function"`: ... end the dependency after the *path operation function* ends, but **before** the response is sent back to the client.
> `"request"`: ... end **after** the response is sent back to the client.

경로 함수가 끝난 직후인가, 응답이 나간 뒤인가. 세션을 얼마나 오래 열어둘 것인가라는 논쟁이 파라미터 하나로 옮겨왔다.

여기서 정확해야 한다. 이 파라미터의 배경에는 정리 순서가 뒤집혀 커밋 전에 세션이 닫히던 이슈(#11107)가 있다. 별도 이슈로 승격된 뒤 종결된 상태로 확인된다. 다만 **그 종결 사유와 병합된 PR을 이 책은 확인하지 못했다.** 그러니 "`scope`가 그 문제를 해결했다"고 쓰지 않겠다. 성립할 가능성은 높지만 릴리스 노트로 확인하기 전에는 미확정이다.

이 불확실성이 `tracker`의 설계를 결정했다. 표준 관용구는 평범한 `Depends(get_session)`이다. **확인할 수 없는 정리 순서에 응답의 정확성을 걸지 않는다.** 대신 응답 직렬화가 세션을 필요로 하지 않게 만든다 — 필요한 건 `selectinload`로 미리 가져오고 빠뜨린 건 `lazy="raise"`가 잡는다. 세션이 언제 닫히든 응답은 같다.

테스트마다 트랜잭션을 열고 끝나면 롤백하는 방식도 익숙할 것이다. 핵심 키워드는 2.0에서 도입된 `join_transaction_mode="create_savepoint"`다.

```python
# (개념 설명용 — 파일 아님)
Session = sessionmaker()
...
self.connection = engine.connect()
self.trans = self.connection.begin()
self.session = Session(bind=self.connection, join_transaction_mode="create_savepoint")
...
self.trans.rollback()
```

> 출처: SQLAlchemy 2.0 Session Transaction, https://docs.sqlalchemy.org/en/20/orm/session_transaction.html (조회 2026-07-26)

바깥에서 커넥션과 트랜잭션을 먼저 잡고, 세션을 그 커넥션에 묶고, 끝나면 바깥 트랜잭션을 되감는다. 세션 안에서 `commit()`을 몇 번 부르든 세이브포인트로 처리되어 전부 되감긴다. 프로덕션 코드를 그대로 두고 격리할 수 있다.

다만 위 레시피는 동기 `Session` 기준이고, **`AsyncSession` 판은 관련된 두 문서 페이지 어디에도 없다.** 전수 확인은 아니니 "그 두 페이지에는 없다"까지만 말하겠다. 비동기 배선은 11장이 맡는다.

## 풀은 비어 있는 채로 시작한다

커넥션 풀 설정을 마지막으로 열어본 게 언제인가?[^6-4]

| 파라미터 | 기본값 |
|---|---|
| `pool_size` | 5 |
| `max_overflow` | 10 |
| `pool_timeout` | 30.0 |
| `pool_recycle` | -1 (비활성) |
| `pool_pre_ping` | False |

문서가 덧붙인 한 문장이 이 표보다 중요하다.

> "All SQLAlchemy pool implementations have in common that **none of them 'pre create' connections**"

풀은 **비어 있는 채로 시작한다.** 당신이 HikariCP의 `minimumIdle`로 유휴 커넥션을 미리 채워뒀다면, 여기엔 대응물이 없다. 트래픽이 느는 구간마다 커넥션을 새로 맺는 비용이 얹힌다.

산수도 해두자. 한 프로세스의 최대 커넥션은 `pool_size` + `max_overflow`, 즉 **15**다. 그런데 5장에서 봤듯 워커는 독립 프로세스이고 풀도 프로세스마다 생긴다. 워커 4개에 레플리카 3개면 15 × 12 = **180**이다. 접속 한도를 확인하지 않은 채 이 숫자에 닿으면, 그날 밤 로그는 데이터베이스가 채운다.

그래서 풀 크기를 설정으로 꺼내 뒀다. 2장의 `Settings`에 두 필드가 추가된다.

```python
# src/tracker/settings.py
    db_pool_size: int = 5
    db_max_overflow: int = 10
# ...(2장, 생략)
```

환경별로 다른 숫자를 주려는 게 아니라 **어딘가에 적혀 있게 하려는 것**이다. 13장에서 워커 수를 정할 때 곱해야 한다.

`pool_pre_ping`은 끊긴 커넥션을 걸러주는 장치라 켜뒀지만, 문서가 붙인 한계가 중요하다.

> "**It is critical to note that the pre-ping approach does not accommodate for connections dropped in the middle of transactions or other SQL operations.**"

트랜잭션 도중에 끊긴 커넥션은 pre-ping이 구해주지 못한다. 이걸 켰으니 커넥션 문제는 끝났다고 여기는 게 위험한 지점이다. 재시도는 여전히 애플리케이션의 일이다.

풀 구현도 비동기에서는 다르다. 문서 축자로 `QueuePool`은 asyncio와 호환되지 않으며, `create_async_engine`을 쓰면 `AsyncAdaptedQueuePool`이 쓰인다.[^6-4] 위 표의 인자들은 같은 이름으로 받는다.

## 마이그레이션은 읽어야 하는 산출물이다

스키마 변경 도구는 Alembic(1.18.5 / 2026-06 기준)이다. 비동기 엔진을 쓰면 초기화부터 갈린다 — 문서가 asyncpg 같은 비동기 DBAPI용 `alembic init -t async` 템플릿을 따로 안내한다. `env.py`의 핵심은 짧다.[^6-6]

```python
# alembic/env.py
connectable = async_engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

async with connectable.connect() as connection:
    await connection.run_sync(do_run_migrations)
```

마이그레이션 실행 자체가 동기 코드이므로, 비동기 커넥션을 얻은 뒤 `run_sync`로 태워 보낸다. 앞 절에서 "controversial"이라던 어댑터가 여기서는 가장 정직하게 쓰인다.

첫 리비전도 여기서 만든다 — 선언한 매핑을 `alembic revision --autogenerate`로 뽑고 `alembic upgrade head`로 적용한다. 그리고 가장 크게 적어둘 경고가 있다. **autogenerate는 컬럼 이름 변경을 인식하지 못하고 추가와 삭제로 처리한다.** 삭제된 컬럼의 데이터는 함께 사라진다. 스테이징에서는 아무 일도 일어나지 않는다 — 잃어도 되는 데이터라서다. 프로덕션에서만 티가 난다.

그래서 습관은 단순하다. **생성된 리비전 파일은 읽고 넘어가자.** 손으로 쓰던 도구에서는 읽을 수밖에 없었지만 여기서는 읽지 않아도 파일이 만들어진다.

드라이버도 여기서 정한다. `tracker`는 프로덕션에서 `postgresql+asyncpg://`, 테스트에서 `sqlite+aiosqlite:///`를 쓴다. psycopg3라면 `postgresql+psycopg://`가 같은 dialect 이름으로 동기·비동기를 모두 지원한다. 성능 비교는 하지 않겠다 — asyncpg 저장소의 인상적인 배수는 2023년 6월의 자체 측정이고, MySQL 쪽 두 드라이버도 우열을 단정할 근거가 없다. 다만 asyncpg는 기본 설정에서 `json`·`jsonb`를 문자열로 돌려준다.

## 인터넷 예제가 낡았을 때

공식 SQL 튜토리얼을 열면 당신은 당황한다. SQLModel을 쓰고 **전부 동기 코드다.**

> "You could use any other SQL or NoSQL database library you want... **FastAPI doesn't force you to use anything. 😎**"

이 반전은 사고가 나는 경로를 설명해준다. "FastAPI는 비동기 프레임워크"라 믿고 온 사람이 공식 튜토리얼로 시작하면 문제가 없다. 문제는 그 위에 비동기 세션을 얹는 날 시작되고, 그날은 대개 프로덕션 이후다.

SQLModel을 쓸지는 각자의 판단이고, 재료 하나만 남기자 — 버전이 아직 `0.0.39`(2026-06 기준)다. `tracker`가 SQLAlchemy 2.0으로 간 이유는, 이 장의 문제가 전부 SQLAlchemy 층에서 벌어져 한 층을 더 얹으면 은폐가 되기 때문이다.

낡은 예제 문제는 데이터 계층 전반에 퍼져 있다. MongoDB가 대표적이다. Motor의 마지막 릴리스는 3.7.1, 2025-05-14로 조사 시점(2026-07-25)까지 1년 넘게 새 릴리스가 없다. 그리고 PyMongo 4.17.0(2026-04-20)에 async 지원이 통합돼 있다. 다만 **Motor의 자리가 PyMongo의 async API로 흡수되는 공식 이행 경로인지는 1차 소스로 확인하지 못했다.** Redis 쪽은 더 분명해서, `aioredis`가 redis-py에 흡수돼 8.0.1 / 2026-06 기준 `redis.asyncio`가 현재 경로다.

같은 패턴을 10장에서 인증 라이브러리로 다시 만난다. **정체된 라이브러리 → 예제가 여전히 그걸 쓴다 → 복붙된다.** 검색 상위라는 건 오래됐다는 뜻이기도 하다.

마지막으로 N+1을 매듭짓자. 한 한국 개발자가 FastAPI에서 Spring으로 마이그레이션한 경험을 정리하며 이렇게 적었다.

> "FastAPI는 빠른 개발과 간결한 구조가 강점이었지만, 복잡한 비즈니스 로직을 다루고 대규모 트래픽을 처리하는 데는 Spring이 더 적합했다."
>
> 출처: velog, JUNYOUNG (2025-03-07)

결론만 보면 이 장의 논지를 거드는 글 같다. 그런데 본문 대부분은 옮겨간 쪽에서 겪은 ORM 삽질 — 페치 조인, 네이티브 쿼리, 엔티티 상속이다. 프레임워크를 바꿨는데 N+1과 연관관계 문제를 다시 만난 것이다.

그러니 정확히 말하자. N+1은 프레임워크가 아니라 **ORM의 문제**다. 어느 언어로 옮겨가도 따라온다. 다만 비동기 세션에서는 성능 저하가 아니라 예외로 나타나 더 시끄럽게 알려질 뿐이다.

---

이 장에서 한 일은 매핑이 아니라, 접혀 있던 결정 넷을 펴서 자리를 준 것이다. 세션은 의존성이 열고, 트랜잭션은 서비스가 닫고, 로딩은 쿼리가 정하고, 커넥션 총량은 설정이 든다.

그러니 지금 팀의 앱에서 한 가지만 계산해보자. 워커 수 × 레플리카 수 × (`pool_size` + `max_overflow`). 그 숫자를 데이터베이스의 접속 한도와 나란히 놓으면, 오늘 밤 무엇을 확인해야 할지가 분명해진다.

[^6-1]: `mapped_column()`의 `index`·`unique`·`server_default`·`default`, 널 허용 파생 규칙, `enum.Enum` 상속 타입의 자동 `Enum` 매핑 — /orm/declarative_tables.html. `String(n)`·`Text`·`DateTime(timezone=True)` — /core/type_basics.html. `func.current_timestamp()` — /core/sqlelement.html (전부 SQLAlchemy 2.0 공식 문서 https://docs.sqlalchemy.org/en/20 하위, 조회 2026-07-26)

[^6-2]: 연결 엔티티 패턴과 `relationship(secondary=...)` 직접형 — SQLAlchemy 2.0 Basic Relationship Patterns, https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html (조회 2026-07-26)

[^6-3]: `selectinload`·`options()`·`lazy='raise'` — SQLAlchemy 2.0 Relationship Loading Techniques, https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html. `select()`의 `.where()`·`.order_by()`·`.limit()`·`.offset()` 체인과 `Session.scalars()`가 `Row` 대신 엔티티를 준다는 서술 — ORM Querying Guide, https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html (조회 2026-07-26)

[^6-4]: `Session.add()` — SQLAlchemy 2.0 Session Basics, https://docs.sqlalchemy.org/en/20/orm/session_basics.html. 풀 기본값 5종과 본문의 pre-create·pre-ping 축자 2건, `QueuePool`↔`AsyncAdaptedQueuePool` — Connection Pooling, https://docs.sqlalchemy.org/en/20/core/pooling.html (조회 2026-07-26)

[^6-5]: `create_async_engine`·`async_sessionmaker`·`AsyncSession`, `expire_on_commit=False`, `AsyncAttrs`·`awaitable_attrs`, `run_sync`, `engine.dispose()` 누락 시의 `RuntimeError`, 본문의 `MissingGreenlet` 정의·동시성 경고 축자 — SQLAlchemy 2.0 Asynchronous I/O, https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html (조회 2026-07-26)

[^6-6]: `alembic init -t async` 템플릿(축자 *"can be used with async DBAPI like asyncpg"*)과 `env.py`의 `async_engine_from_config` + `connection.run_sync(do_run_migrations)` — Alembic Cookbook, https://alembic.sqlalchemy.org/en/latest/cookbook.html. `async_engine_from_config`는 [^6-5]의 문서에서 확인 (조회 2026-07-26)
