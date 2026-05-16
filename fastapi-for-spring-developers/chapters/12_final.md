# 12장. 통합 프로젝트 — 사내 태스크 관리 API + Slack 알림 봇

여기까지 한 호흡으로 따라왔으면, 지금까지 우리가 만진 조각들이 머릿속에 흩어져 있을 것이다. `Depends()`의 그래프, `with db.begin():`의 명시 트랜잭션, `Security(..., scopes=[...])`의 RBAC, `BackgroundTasks`의 가벼움, `pytest` + `TestClient`의 안전망, Docker · Uvicorn 워커. 한 조각씩은 손에 익혔다. 그러나 *한 프로덕션 서비스 안에서 이 조각들이 어떻게 공존하는지*는 아직 본 적이 없다.

이 장이 그 자리다. 책 한 권 분량을 *하나의 코드베이스*로 받아본다. 도메인은 *사내 태스크 관리 API + Slack 알림 봇*이다. Spring 출신에게 가장 친숙한 도메인이라(이슈 트래커·티켓 시스템) 비즈니스 로직을 새로 배울 부담이 0이다. 그 자리에 우리가 책에서 약속한 모든 패턴을 끌고 와 본다.

한 가지를 미리 적어두자. *이 장의 코드는 깃허브 리포 한 개의 분량*이다. 모든 줄을 본문에 적지 않는다. 핵심 구조와 *Spring 사고와 부딪히는 자리*만 본문에 박는다. 전체 코드는 책의 짝 리포로 둔다. 본문은 *결정과 호흡*을 가르치고, 리포는 *완전한 손짐작*을 보여주는 분업이다.

> **이 장을 읽기 전 알아둘 것**
> - 1~11장 모든 챕터를 *전제*한다. 발췌 독자는 4장(DI)·5장(SQLAlchemy)·6장(트랜잭션)·7장(인증)·8장(async/배경)·10장(테스트) 최소 다섯 절은 보고 오자.
> - 이 장은 *완성된 코드를 처음부터 짜는 흐름*이 아니라, *각 장의 약속이 한 서비스에 어떻게 모이는지*의 거시 그림이다. 디테일은 챕터 본문에 이미 있다.

## §12.1 요구사항을 한 페이지에 박자

본격 코드 전에 *무엇을 만드는지*를 한 페이지로 못박아 두자. 이게 Spring 진영에서도 똑같다 — Confluence 한 페이지에 박는 그 그림.

**핵심 도메인 네 개**
- `users` — 사용자 가입/로그인, 역할 (`member`, `admin`)
- `tasks` — 태스크 생성·상태 변경·검색. 상태는 `todo` → `in_progress` → `done`
- `comments` — 태스크 댓글
- `notifications` — Slack 알림 (댓글 작성, 태스크 상태 변경 등)

**기능 요구사항 (요약)**
- 회원: JWT 로그인, `/me` 조회
- 태스크: CRUD, 상태 전이, 담당자 변경, 카테고리 필터
- 댓글: 작성/조회/삭제 (작성자만 삭제)
- 알림: 댓글이 달리거나 태스크 상태가 바뀌면 Slack 채널로 webhook
- 실시간: 태스크 상태 변경 시 SSE로 푸시
- 관측성: 요청 ID 미들웨어, Prometheus 메트릭, `/healthz`/`/readyz`, 도메인 예외 처리
- 인가: `admin` 역할만 사용자 관리(`/admin/users/*`)

**비기능 요구사항**
- Docker로 배포. PostgreSQL + Redis + 앱 컨테이너. K8s manifest 예시 한 장.
- 통합 테스트로 모든 라우트 검증. Testcontainers로 실제 PostgreSQL 띄우기.
- CI/CD 파이프라인 스켈레톤(GitHub Actions): lint(ruff) → type-check(pyright) → test → build.

작은 종이 한 장에 담길 그림이다. 무리하지 말자 — Spring 출신이 *한 분기 안에 두 사람*이 짤 만한 분량이다. 우리는 이걸 책의 호흡으로 한 챕터 안에 그린다.

## §12.2 폴더 구조 — 5장의 약속을 그대로

5장에서 박아둔 *by-feature 폴더 구조*가 여기서 빛난다. 도메인이 넷이면 폴더도 넷이다.

```text
task-tracker/
├── pyproject.toml
├── uv.lock
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/ci.yml
├── src/
│   └── app/
│       ├── main.py                 # FastAPI 진입점, 라우터 등록, lifespan
│       ├── core/
│       │   ├── config.py           # pydantic-settings 기반 (7장)
│       │   ├── security.py         # JWT, 비밀번호 해싱 (7장)
│       │   └── logging.py          # structlog 설정 (9장)
│       ├── db/
│       │   ├── base.py             # DeclarativeBase
│       │   ├── session.py          # engine + SessionLocal
│       │   └── deps.py             # get_db
│       ├── observability/
│       │   ├── middleware.py       # 요청 ID, 메트릭 미들웨어 (9장)
│       │   └── metrics.py          # Prometheus 카운터
│       ├── users/
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── repository.py
│       │   ├── service.py
│       │   ├── router.py
│       │   ├── deps.py             # get_current_user, require_admin
│       │   └── exceptions.py
│       ├── tasks/
│       │   ├── models.py           # Task + TaskStatus enum
│       │   ├── schemas.py
│       │   ├── repository.py
│       │   ├── service.py          # 상태 전이 로직
│       │   ├── router.py
│       │   ├── deps.py
│       │   └── events.py           # 도메인 이벤트 정의
│       ├── comments/
│       │   └── (같은 구조)
│       └── notifications/
│           ├── slack.py            # Slack webhook 클라이언트
│           ├── service.py          # 알림 발송 인터페이스
│           ├── worker.py           # ARQ 워커 (선택)
│           └── deps.py
└── tests/
    ├── conftest.py                 # Testcontainers + 픽스처
    ├── users/
    ├── tasks/
    ├── comments/
    └── e2e/                        # 통합 시나리오
```

처음 보면 폴더가 많다는 인상이 들 것이다. 그러나 Spring 출신이라면 *`com.foo.{users,tasks,comments,notifications}.{controller,dto,domain,repository,service}` 구조*와 1:1로 매핑된다는 걸 본능적으로 느낄 것이다. 새 도메인을 추가하는 비용이 *한 폴더 복사 + 6개 파일 채우기*다. 손짐작이 익으면 이 모양 자체가 *제도가* 된다.

## §12.3 설정과 부팅 — `main.py`와 `lifespan`

엔트리 포인트부터 보자. 라우터 등록, 미들웨어 등록, `lifespan`으로 자원 생명주기 묶기, 예외 핸들러 등록 — 9장에서 익힌 흐름 그대로다.

```python
# src/app/main.py
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import configure_logging
from app.db.deps import get_db
from app.db.session import engine
from app.observability.middleware import RequestIdMiddleware, MetricsMiddleware
from app.observability.metrics import metrics_router
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
from app.comments.router import router as comments_router
from app.notifications.deps import build_arq_pool, close_arq_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    app.state.arq_pool = await build_arq_pool(settings.redis_url)
    yield
    await close_arq_pool(app.state.arq_pool)
    await engine.dispose()


app = FastAPI(
    title="Task Tracker API",
    version="1.0.0",
    lifespan=lifespan,
)

# 미들웨어 (외→내 순으로 등록 호출 시 안→밖 순으로 동작)
app.add_middleware(MetricsMiddleware)
app.add_middleware(RequestIdMiddleware)

# 라우터 등록
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(metrics_router)


# 9·11장의 약속대로 두 probe를 의도적으로 분리한다.
# /healthz — 프로세스가 살아 있는가만 본다 (liveness)
# /readyz  — 지금 요청을 받을 준비가 됐는가 (readiness, DB 의존)
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="db not ready")
    return {"status": "ready"}
```

Spring Boot의 `@SpringBootApplication`이 떠받쳐 주던 *컴포넌트 스캔·자동 설정*의 자리를 우리는 *임포트 + `include_router` 호출 한 줄씩*으로 받는다. 손이 더 가지만 *무엇이 등록되는지가 코드 표면에 다 올라온다*. 13장에서 다시 비교하지만, 이게 Spring과 FastAPI의 근본적 결 차이다 — *자동화* vs *명시성*.

`Settings` 클래스는 7장의 `pydantic-settings` 패턴을 그대로 쓴다.

```python
# src/app/core/config.py
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    database_url: str = Field(..., alias="APP_DATABASE_URL")
    redis_url: str = Field("redis://redis:6379/0", alias="APP_REDIS_URL")
    jwt_secret: str = Field(..., alias="APP_JWT_SECRET")
    jwt_algorithm: str = Field("HS256", alias="APP_JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(15, alias="APP_ACCESS_TOKEN_EXPIRE_MINUTES")
    slack_webhook_url: str | None = Field(None, alias="APP_SLACK_WEBHOOK_URL")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

11장의 약속처럼, K8s 환경에선 이 환경변수들이 *Secret/ConfigMap → 컨테이너 env → Settings*의 파이프라인으로 흐른다. 코드는 한 줄도 안 바꾸고 환경만 바뀐다.

## §12.4 도메인 모델 — Task와 상태 전이

`Task`가 본 프로젝트의 핵심 도메인이다. 5장의 `Mapped`/`mapped_column` 패턴 위에 상태 enum을 더 얹는다.

```python
# src/app/tasks/models.py
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO, index=True)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    assignee: Mapped["User"] = relationship(foreign_keys=[assignee_id], lazy="raise")
    created_by: Mapped["User"] = relationship(foreign_keys=[created_by_id], lazy="raise")
    comments: Mapped[list["Comment"]] = relationship(back_populates="task", lazy="raise")
```

한 가지 디테일을 짚어두자. `relationship(..., lazy="raise")`다. 5장에서 *DetachedInstanceError* 함정을 본 적이 있다. `lazy="raise"`는 *lazy load 자체를 막아*버린다 — 명시적 `selectinload`로 끌어오지 않은 관계 접근은 *런타임에 즉시 에러*를 던진다. 처음엔 과한가 싶지만, 한 번 부딪혀 보면 안다. 5장에서 가르친 *코드 표면에 비용을 올려둔다*는 명시성의 정수다.

### 상태 전이 — 도메인 메서드로 박는다

JPA 진영에선 `Task.transition_to(...)` 같은 도메인 메서드를 엔티티에 박는 게 익숙하다. SQLAlchemy도 똑같이 한다.

```python
# src/app/tasks/models.py (Task 클래스 안에 추가)
class InvalidTransition(Exception):
    def __init__(self, from_status: TaskStatus, to_status: TaskStatus):
        self.from_status = from_status
        self.to_status = to_status


VALID_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.TODO},
    TaskStatus.DONE: set(),   # 종료 상태
}


class Task(Base):
    # ... 위 정의

    def transition_to(self, new_status: TaskStatus) -> None:
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise InvalidTransition(self.status, new_status)
        self.status = new_status
```

엔티티가 자기 *상태 전이 규칙*을 안다. 서비스 레이어에서 이 메서드를 호출하면 *비즈니스 불변식*이 한 곳에 모인다. Spring DDD 진영에서 익숙한 그림이다.

## §12.5 트랜잭션과 도메인 이벤트 — 6장의 약속

먼저 한 가지를 못박아 두자. 5장에서 약속한 `expire_on_commit=False`가 본 프로젝트 `app/db/session.py`의 전제다. 그 위에서 *커밋 직후에도 객체 속성을 안전하게 읽을 수 있고*, 본 절의 권장 패턴이 그 보장 위에서 동작한다. 만약 기본값 `True`로 두면 `with` 블록 종료 직후 `task.id`/`from_status` 접근이 `DetachedInstanceError`로 폭발한다 — 책의 §12.12 함정 체크리스트 3번이 짚는 자리다.

태스크 상태가 *바뀌면* Slack 알림이 가야 한다. 그런데 *DB 커밋과 Slack 호출의 순서*는 어떻게 잡을까? 이게 6장이 던진 큰 질문이다.

**잘못된 패턴 1: 트랜잭션 안에서 Slack 호출**

```python
# 안티패턴 — 트랜잭션이 외부 API 응답까지 기다린다
def change_task_status(task_id: int, new_status: TaskStatus, db: Session, slack: SlackClient):
    with db.begin():
        task = db.get(Task, task_id)
        task.transition_to(new_status)
        slack.post(f"Task {task.id} → {new_status.value}")   # 트랜잭션 점유
```

Slack이 느리거나 죽으면 *트랜잭션이 그동안 잡혀 있다*. DB 락 시간이 길어지고, *DB가 throttle된다*. 또 — Slack 호출이 성공했는데 DB commit이 실패하면? 알림은 갔는데 상태는 그대로다. 데이터 불일치다. 끔찍한 일이다.

**잘못된 패턴 2: 트랜잭션 밖에서 BackgroundTasks**

```python
# 안티패턴 — DB 실패해도 알림은 나간다
def change_task_status(...):
    with db.begin():
        task.transition_to(new_status)
    background.add_task(slack.post, f"Task {task.id} → {new_status.value}")
```

이건 패턴 1의 데이터 불일치를 *반대로* 일으킨다 — DB는 정상인데 알림이 안 나가거나, 트랜잭션 롤백이 일어났는데도 알림이 나간다.

**권장 패턴: 도메인 이벤트 + 트랜잭션 후 발행**

해법은 도메인 이벤트를 *트랜잭션 안에서 수집*하고, *커밋 성공 후*에 *비동기 발행*하는 분리다. Spring 진영에선 `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` 패턴으로 같은 일을 한다.

```python
# src/app/tasks/events.py
from dataclasses import dataclass

from app.tasks.models import TaskStatus


@dataclass(frozen=True)
class TaskStatusChanged:
    task_id: int
    from_status: TaskStatus
    to_status: TaskStatus
    actor_id: int
```

```python
# src/app/tasks/service.py
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.tasks.events import TaskStatusChanged
from app.tasks.exceptions import TaskNotFound
from app.tasks.models import Task, TaskStatus
from app.tasks.repository import TaskRepository
from app.notifications.service import NotificationService


class TaskService:
    def __init__(self, db: Session, tasks: TaskRepository, notify: NotificationService):
        self.db = db
        self.tasks = tasks
        self.notify = notify

    def change_status(
        self,
        task_id: int,
        new_status: TaskStatus,
        actor_id: int,
        background: BackgroundTasks,
    ) -> Task:
        with self.db.begin():
            task = self.tasks.get(task_id)
            if task is None:
                raise TaskNotFound(task_id)
            from_status = task.status
            task.transition_to(new_status)

        # 커밋이 성공한 뒤 — BackgroundTasks로 비동기 알림
        event = TaskStatusChanged(
            task_id=task.id,
            from_status=from_status,
            to_status=new_status,
            actor_id=actor_id,
        )
        background.add_task(self.notify.task_status_changed, event)
        return task
```

여기 코드 구조의 핵심을 짚어두자. **`with self.db.begin():` 블록을 빠져나오는 시점이 *커밋 성공의 명시적 표지*다.** 그 뒤의 `background.add_task(...)`는 *커밋이 성공했을 때만 도달*한다. 트랜잭션 안에서 예외가 터지면 `with` 블록이 롤백을 일으키고, `background.add_task`는 호출되지 않는다. *데이터 일관성과 알림 일관성이 한 자리에서 보호*된다.

Spring `@TransactionalEventListener(phase = AFTER_COMMIT)`이 떠받쳐 주던 *커밋 후 발행* 보장이 FastAPI에선 *코드 구조로 명시*되는 자리다.

이 한 패턴이 본 프로젝트 *모든 도메인 이벤트의 표준*이다. 댓글 작성, 태스크 할당 변경, 사용자 가입 — 다 같은 모양이다. 한번 손에 익히면 *생각 없이 손이 간다*.

## §12.6 인증·인가 — 7장의 약속을 그대로

7장에서 짠 JWT 흐름이 본 프로젝트에서 *그대로* 동작한다. 핵심만 다시 보자.

```python
# src/app/users/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.deps import get_db
from app.users.models import User
from app.users.repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scopes={"member": "Read tasks and comments", "admin": "Manage users"},
)


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = int(payload["sub"])
        token_scopes = set(payload.get("scopes", []))
    except (JWTError, KeyError, ValueError):
        raise credentials_exc

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail=f"Missing scope: {scope}")

    user = UserRepository(db).get(user_id)
    if user is None:
        raise credentials_exc
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
RequireAdmin = Annotated[User, Security(get_current_user, scopes=["admin"])]
```

라우트에서는 한 줄로 끝난다.

```python
# src/app/tasks/router.py
from fastapi import APIRouter, BackgroundTasks

from app.users.deps import CurrentUser
from app.tasks.deps import TaskServiceDep
from app.tasks.schemas import TaskStatusChange, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.patch("/{task_id}/status", response_model=TaskRead)
def change_status(
    task_id: int,
    payload: TaskStatusChange,
    user: CurrentUser,
    service: TaskServiceDep,
    background: BackgroundTasks,
):
    task = service.change_status(task_id, payload.new_status, actor_id=user.id, background=background)
    return TaskRead.model_validate(task)


# 관리자 전용 라우트
from app.users.deps import RequireAdmin


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, _admin: RequireAdmin, service: TaskServiceDep):
    service.delete(task_id)
```

`CurrentUser`/`RequireAdmin` 두 타입 별칭이 *책 전체에서 가장 자주 쓰는 보안 표시*다. 라우트 시그니처를 보면 *누가 호출할 수 있는지가 한눈에* 보인다 — Spring의 `@PreAuthorize("hasRole('ADMIN')")`이 떠받쳐 주던 *선언적 보안*의 자리를 *함수 파라미터의 명시성*이 받는다. 7장의 정수 그대로다.

## §12.7 Slack 알림 — BackgroundTasks로 시작해서 ARQ로 옮길 시점

이게 본 프로젝트가 8장의 약속을 *실제로 시연*하는 자리다. *미리 가지 말고 단계로 올라가자*는 그 한 줄.

### 단계 1 — `BackgroundTasks` + httpx async

처음엔 `BackgroundTasks`로 충분하다. Slack webhook 한 번은 빠르면 100ms, 느려도 500ms 정도다. fire-and-forget으로 가볍게.

```python
# src/app/notifications/slack.py
import httpx
from app.core.config import settings


class SlackClient:
    def __init__(self, webhook_url: str | None):
        self.webhook_url = webhook_url

    async def post_message(self, channel: str, text: str) -> None:
        if not self.webhook_url:
            return   # 개발 환경에선 그냥 건너뛴다
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                self.webhook_url,
                json={"channel": channel, "text": text},
            )


def get_slack_client() -> SlackClient:
    return SlackClient(settings.slack_webhook_url)
```

```python
# src/app/notifications/service.py
from typing import Annotated
from fastapi import Depends

from app.notifications.slack import SlackClient, get_slack_client
from app.tasks.events import TaskStatusChanged


class NotificationService:
    def __init__(self, slack: SlackClient):
        self.slack = slack

    async def task_status_changed(self, event: TaskStatusChanged) -> None:
        text = f"Task #{event.task_id}: {event.from_status.value} → {event.to_status.value}"
        await self.slack.post_message(channel="#tasks", text=text)


def get_notification_service(
    slack: Annotated[SlackClient, Depends(get_slack_client)],
) -> NotificationService:
    return NotificationService(slack)


NotificationServiceDep = Annotated[NotificationService, Depends(get_notification_service)]
```

라우트는 §12.5에서 본 그대로다 — `background.add_task(self.notify.task_status_changed, event)` 한 줄.

### 단계 2 — 옮길 시점이 왔을 때

8장 §8.7에서 적었듯, 다음 조건 중 하나라도 발생하면 ARQ로 옮긴다.

1. 알림이 *길고 무거워졌다* (예: 첨부 이미지 생성, 여러 채널 동시 발송)
2. 트래픽이 분당 수백 건 이상으로 늘었다
3. 실패 시 *재시도*가 필요해졌다

옮기는 비용을 한 번 더 강조한다. **라우트 한 줄만 바뀐다.**

```python
# 단계 2 — ARQ로
# 이전: background.add_task(self.notify.task_status_changed, event)
# 이후: await arq.enqueue_job("task_status_changed", event_dict)
```

함수 본체는 *그대로 ARQ 워커 모듈에 옮겨가고*, 라우트에서는 *enqueue 한 줄로 바뀐다*. 손짐작이 *옮기기 가벼운 모양으로 미리 짜여 있던* 결과다. 그래서 8장이 *처음부터 ARQ로 짤 필요가 없다*고 권했던 것이다.

본 프로젝트는 *단계 1*에서 멈춘다 — 사내 도구의 트래픽이라면 그게 정확한 자리다. *옮길 준비*가 코드에 박혀 있다는 사실만 손에 두자.

## §12.8 SSE — 실시간 태스크 업데이트

태스크 상태가 바뀌면 *대시보드가 즉시* 보이게 하고 싶다. WebSocket을 동원할 만큼 양방향이 필요한 건 아니니, *SSE(Server-Sent Events)*가 적격이다. Spring WebFlux에서 SSE를 짜본 손이라면 정신적 모양이 거의 같다.

```python
# src/app/tasks/router.py (계속)
import asyncio
import json
from typing import AsyncIterator

from fastapi.responses import StreamingResponse


# 단순 예제 — 프로덕션은 Redis Pub/Sub 또는 ARQ 결과 채널 사용
event_queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=100)


async def task_event_stream(user: CurrentUser) -> AsyncIterator[str]:
    while True:
        event = await event_queue.get()
        # 사용자 권한에 맞춰 필터링 가능
        yield f"event: task_changed\ndata: {json.dumps(event)}\n\n"


@router.get("/stream")
async def stream_tasks(user: CurrentUser):
    return StreamingResponse(
        task_event_stream(user),
        media_type="text/event-stream",
    )
```

`asyncio.Queue`는 한 프로세스 안의 단순 큐다. *워커 여러 개*가 있는 프로덕션에선 Redis Pub/Sub로 갈아 끼워야 한다 — 그러나 코드 구조는 같다. 큐의 *소스*를 바꿀 뿐이다. SSE 자체의 라우트 모양은 *위 한 줄*로 끝난다. 그게 ASGI 위의 FastAPI다.

Spring WebFlux의 `Flux<ServerSentEvent<Task>>` 반환 패턴이 *반응형 컨테이너*에 의존하는 데 비해, FastAPI는 *비동기 제너레이터*에 의존한다. 정신적 모양은 같고, *손짐작이 더 단조롭다*.

## §12.9 통합 테스트 — Testcontainers + TestClient

10장의 약속이 여기서 빛난다. 모든 라우트를 *실제 PostgreSQL을 띄운 채* 검증한다.

```python
# tests/conftest.py
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.db.base import Base
from app.db.deps import get_db
from app.main import app


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    with PostgresContainer("postgres:16-alpine") as container:
        yield container


@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(engine) -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    def _override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
```

이 픽스처 한 묶음이 본 프로젝트의 *모든 테스트의 토대*다. 핵심 두 줄을 짚자.

**첫째, `db_session`이 *테스트마다 트랜잭션을 새로 만들고 끝에 롤백*한다.** Spring `@Transactional` 테스트의 자동 롤백을 *수제*로 구현한 자리다. 10장 §6에서 이미 본 패턴이다.

**둘째, `app.dependency_overrides[get_db]` 한 줄로 *프로덕션 의존성*을 *테스트 세션*으로 교체한다.** 4장 §테스트 오버라이드의 정수. Spring `@MockBean` 자리에 정확히 들어선다.

이제 시나리오 테스트가 깔끔하다.

```python
# tests/e2e/test_task_lifecycle.py
def test_task_status_transition_publishes_event(client, db_session, monkeypatch):
    sent_messages: list[str] = []

    # Slack 클라이언트 mock
    async def fake_post(self, channel: str, text: str) -> None:
        sent_messages.append(text)

    monkeypatch.setattr("app.notifications.slack.SlackClient.post_message", fake_post)

    # 1. 사용자 가입 + 로그인
    client.post("/users/register", json={"email": "tobi@example.com", "password": "pass1234"})
    token_resp = client.post(
        "/users/login",
        data={"username": "tobi@example.com", "password": "pass1234"},
    )
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. 태스크 생성
    create_resp = client.post(
        "/tasks",
        json={"title": "Write integration tests", "description": "..."},
        headers=headers,
    )
    task_id = create_resp.json()["id"]

    # 3. 상태 전이
    change_resp = client.patch(
        f"/tasks/{task_id}/status",
        json={"new_status": "in_progress"},
        headers=headers,
    )
    assert change_resp.status_code == 200
    assert change_resp.json()["status"] == "in_progress"

    # 4. Slack 알림 검증 — BackgroundTasks가 TestClient 컨텍스트에서 동기적으로 실행됨
    assert any("todo → in_progress" in m for m in sent_messages)
```

마지막 단계의 주석이 재미있다. **`TestClient` 컨텍스트에서 `BackgroundTasks`는 *동기적으로* 실행**된다. 그래서 `with TestClient(app) as client:` 블록이 끝나면 *백그라운드 작업이 다 끝난 상태*다. 테스트 코드가 *비동기 검증의 복잡함* 없이 *동기처럼* 작성된다 — 10장이 적어둔 *손에 익은 안전망*의 정수다.

## §12.10 배포 — Docker와 Kubernetes 한 페이지

11장의 약속을 한 페이지에 묶자. 멀티-스테이지 Dockerfile + docker-compose + K8s manifest 예시.

```dockerfile
# Dockerfile — 11장 패턴 그대로
FROM python:3.12-slim AS builder

# Astral 공식 uv 이미지에서 바이너리 복사 (별도 설치 불필요)
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev


FROM python:3.12-slim AS runtime

# tini로 PID 1 신호 처리 + 좀비 프로세스 회수
RUN apt-get update && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/
COPY alembic/ /app/alembic/
COPY alembic.ini /app/

ENV PATH="/app/.venv/bin:$PATH"
USER appuser

EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--"]
# K8s 환경 권장: 컨테이너당 단일 프로세스
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--proxy-headers", "--forwarded-allow-ips=*"]
```

`docker-compose.yml`로 로컬 개발 환경을 한 줄로 띄운다.

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: tasks
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  app:
    build: .
    environment:
      APP_DATABASE_URL: postgresql+psycopg://app:secret@db:5432/tasks
      APP_REDIS_URL: redis://redis:6379/0
      APP_JWT_SECRET: dev-secret-please-rotate
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

volumes:
  postgres_data:
```

`alembic upgrade head` 한 줄을 startup 스크립트에 박았다. Spring Boot의 *자동 Flyway 실행*에 가까운 자리다. 5장에서 *Alembic은 자동 시작이 없다*고 했던 그 단점을 *컨테이너 entrypoint*에서 한 줄로 메운다.

K8s manifest는 한 장만 적어두자.

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-tracker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: task-tracker
  template:
    metadata:
      labels:
        app: task-tracker
    spec:
      containers:
      - name: app
        image: task-tracker:1.0.0
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: task-tracker-secrets
        - configMapRef:
            name: task-tracker-config
        # 9·11장 약속대로 두 probe를 의도적으로 분리.
        # DB가 잠시 끊겼는데 컨테이너가 재시작되면 연쇄 재기동이 시작된다.
        readinessProbe:
          httpGet:
            path: /readyz       # DB 의존성 포함 — 준비 안 되면 트래픽 차단만
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthz      # 프로세스 살아 있는가만 — 재시작 트리거
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

11장의 약속대로 *컨테이너당 단일 프로세스*고, *replica가 곧 워커 역할*이다. 워커 수 공식을 K8s에선 적용하지 않는다.

GitHub Actions의 CI 파이프라인 한 장.

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pyright
      - run: uv run pytest -v
```

ruff → pyright → pytest 세 단계. 2장에서 박아둔 *정적 안전망 + 테스트*가 CI에서도 그대로 동작한다. *코드 표면에 다 올라온* 안전망이 한 번 더 *파이프라인 표면에도* 올라온다.

## §12.11 관측성 — 9장의 미들웨어 묶음

9장에서 짠 미들웨어들이 본 프로젝트에서도 그대로 동작한다. 핵심만 다시 보자.

```python
# src/app/observability/middleware.py
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.observability.metrics import REQUEST_COUNT, REQUEST_DURATION


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start

        endpoint = request.scope.get("route").path if request.scope.get("route") else request.url.path
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_DURATION.labels(method=request.method, endpoint=endpoint).observe(elapsed)
        return response
```

```python
# src/app/observability/metrics.py
from fastapi import APIRouter
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)


metrics_router = APIRouter()


@metrics_router.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

Spring Boot Actuator의 한 줄 자동화 자리에 *미들웨어 두 개 + 라우터 한 개 + Counter/Histogram 정의*가 들어선다. 손이 더 가지만 *무엇을 측정하는지 코드 표면에 다 보인다* — Grafana 대시보드 짤 때 *이 메트릭이 어떻게 만들어졌는지*가 코드 검색 한 번에 나온다. 운영 디버깅의 호흡이 가벼워진다.

## §12.12 Spring 출신이 빠지기 쉬운 함정 — 체크리스트

마지막으로 한 페이지를 *체크리스트*로 비워두자. 본 프로젝트를 짜면서 *Spring 사고로 인해 손이 잘못 가는 자리* 열 가지를 박아둔다. 코드 리뷰의 동료에게 *책 한 권 다시 펴라*고 하지 말고, 이 리스트 한 장을 띄워두면 된다.

1. **트랜잭션 안에서 외부 API 호출** — Slack/메일/외부 IDP 콜이 트랜잭션 안에 끼면 DB 락 시간이 폭발한다. 도메인 이벤트 + 커밋 후 발행으로 분리하자.
2. **`get_db`의 `finally`에서 commit** — 응답이 이미 나간 뒤다. 트랜잭션 경계는 라우트/서비스에서 명시.
3. **`expire_on_commit=True`로 두고 응답 직렬화** — commit 후 lazy load가 폭발해 `DetachedInstanceError`. `False`로 두자.
4. **`async def` 라우트 안에 `requests.get(...)` 한 줄** — 이벤트 루프가 멈춘다. `httpx.AsyncClient` 또는 `def` 라우트로.
5. **`@app.exception_handler`에 모든 예외를 한 곳에 박기** — 도메인 예외 계층 + 캐치올의 두 층으로 분리하자(9장).
6. **`BackgroundTasks`에 무거운 일** — 워커 메모리·CPU를 뺏긴다. 무거우면 ARQ로 옮길 시점.
7. **`lazy="select"` 기본값 그대로 두고 *-to-many 접근** — N+1. `selectinload` 또는 `lazy="raise"`로 *강제 사전 로드*.
8. **`@Autowired` 사고로 글로벌 싱글톤 가정** — FastAPI 기본 스코프는 *요청-스코프*다. 모듈 변수·`lifespan` 컨텍스트로 명시.
9. **`@PreAuthorize` 사고로 보호 라우트마다 직접 if/else** — `Security(get_current_user, scopes=[...])`가 OpenAPI까지 자동 반영.
10. **uvicorn 워커 수를 K8s에서 늘리기** — K8s replica가 곧 워커 역할. *컨테이너당 단일 프로세스*가 표준(11장).

이 열 가지가 본 프로젝트 코드 리뷰에서 *반복 지적되는* 자리들이다. 책 전체의 핵심 함정이 한 페이지에 모인 셈이다. 사무실 모니터 옆에 붙여두자.

## 한 호흡으로 정리

12장은 책 전체의 캡스톤이다. 우리가 받아간 것을 한 번에 묶어두자.

- **요구사항 한 페이지 → 폴더 구조 한 그림**: 도메인 4개(`users`/`tasks`/`comments`/`notifications`) × 6개 파일 패턴 = `app/{도메인}/{models, schemas, repository, service, router, deps}.py`. 5장의 약속 그대로.
- **`lifespan` 컨텍스트**: 자원 생명주기(엔진, ARQ 풀, 로깅)를 한 자리에 묶는다. 8장에서 익힌 `@asynccontextmanager` 패턴.
- **도메인 이벤트 + 커밋 후 발행**: 트랜잭션 안에서 이벤트 수집, `with db.begin():` 블록을 빠져나온 뒤 `BackgroundTasks.add_task`. Spring의 `@TransactionalEventListener(phase = AFTER_COMMIT)` 자리.
- **JWT + 스코프**: `CurrentUser`/`RequireAdmin` 두 타입 별칭이 *책 전체에서 가장 자주 펴볼 보안 표시*.
- **단계적 백그라운드**: `BackgroundTasks` → ARQ → Celery. *미리 가지 말자*. 옮길 때 *라우트 한 줄*만 바뀌도록 함수 본체를 *옮기기 가벼운 모양*으로.
- **SSE**: `StreamingResponse(generator, media_type="text/event-stream")` 한 줄. WebFlux의 `Flux<ServerSentEvent<T>>` 자리.
- **Testcontainers + dependency_overrides**: 진짜 PostgreSQL 띄우고 `get_db`만 교체. `@SpringBootTest` + `@MockBean` 자리에 정확히 들어선다.
- **Docker · K8s · CI**: 멀티-스테이지 Dockerfile + `alembic upgrade head` entrypoint + K8s replica + ruff/pyright/pytest CI. 11장 약속 그대로.
- **관측성 미들웨어 + probe 분리**: 요청 ID + Prometheus 메트릭 + `/healthz`(liveness)/`/readyz`(readiness)의 *연쇄 재기동 함정 회피*. Spring Boot Actuator 자리를 코드 표면으로 끌어올림.
- **함정 체크리스트 10개**: 모니터 옆에 붙여두자.

여기까지 오면 한 가지 감각이 든다. **FastAPI로 프로덕션 API를 *짤 수 있다*는 손 감각.** *Spring처럼 큰 프레임워크가 없는데도* 한 코드베이스 안에서 모든 조각이 일관되게 공존한다. *그 일관성을 떠받치는 것이 챕터 사이 약속들*이라는 사실도 손에 잡힌다 — 5장의 폴더, 6장의 트랜잭션 경계, 7장의 `Security`, 8장의 단계적 백그라운드, 9장의 미들웨어, 10장의 픽스처, 11장의 컨테이너. *각 장이 한 약속*이었던 셈이다.

다음 장이 책의 마지막이다. 본 프로젝트를 다 짠 우리는 이제 *반대 방향의 질문*을 받아야 한다 — *언제 FastAPI를 쓰지 말아야 하는가? 언제 Spring으로 돌아가야 하는가?* 본 책이 답해온 모든 자리에 대한 *정직한 한계*를 마지막으로 정리한다.
