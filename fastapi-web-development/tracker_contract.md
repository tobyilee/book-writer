# `tracker` 코드 계약 (전 챕터 구속)

- **대상:** 14명의 `chapter-writer` 전원 · `fact-checker` · `style-guardian` · Phase 4.5 `manuscript-reviewer`
- **상위 문서:** `02_plan.md` 「저술 제약」 9번(코드 프로바넌스)이 이 계약의 헌법이다. 이 문서는 그 9번을 **이름과 파일 단위로 구체화한 것**이며, 제약 9-(D)(코드 분량 규율)·10번(대조 축 잣대)은 여기서 재서술하지 않고 그대로 적용된다.
- **작성일:** 2026-07-26 · **레퍼런스 기준일:** 2026-07-25

> 🚨 **이 계약의 존재 이유:** 14명이 서로의 산출물을 보지 못한 채 같은 앱 `tracker`를 키운다. 여기 있는 이름을 쓰지 않으면 `tracker`는 14개의 호환되지 않는 코드베이스로 갈라진다.
>
> **읽는 법:** §3(이름 사전)과 §7(장별 성장 맵)이 매번 확인할 곳이다. §8은 **코드를 쓰기 전에 반드시 한 번** 확인한다.

---

## 1. 타깃 버전 (고정)

`tracker`의 모든 코드는 아래 조합을 전제한다. **저술가는 이 표 밖의 버전을 전제하지 않는다.**

| 구성요소 | 코드가 전제하는 버전 | 표기 |
|---|---|---|
| Python | 3.12+ (권장선) | `Python 3.12+ / 2026-07 기준` |
| FastAPI | 0.140.0 | `0.140.0 / 2026-07 기준` |
| Starlette | 1.3.1 | `1.3.1 / 2026-06 기준` |
| Pydantic | 2.13.4 | `Pydantic v2 (2.13.4 / 2026-05 기준)` |
| pydantic-settings | 2.14.2 | `2.14.2 / 2026-06 기준` |
| SQLAlchemy | 2.0.51 | `SQLAlchemy 2.0 (2.0.51 / 2026-06 기준)` |
| Alembic | 1.18.5 | `1.18.5 / 2026-06 기준` |
| uvicorn | 0.51.0 | `0.51.0 / 2026-07 기준` |
| anyio | 4.14.2 | `4.14.2 / 2026-07 기준` |
| uv | 0.11.32 | `0.11.32 / 2026-07 기준` |
| PyJWT | 2.13.0 | `2.13.0 / 2026-05 기준` |
| pwdlib | 0.3.0 | `0.3.0 / 2025-10 기준` |
| pytest | 9.1.1 | `9.1.1 / 2026-06 기준` |
| Strawberry | 0.323.2 | `0.323.2 / 2026-07 기준` |
| redis (redis-py) | 8.0.1 | `8.0.1 / 2026-06 기준` |
| structlog | 26.1.0 | `26.1.0 / 2026-06 기준` |

**🚨 산문에서의 버전 표기 규율 (제약 3번 적용):**

- **패치 버전은 이 표에서 한 번만 고정한다.** 본문 산문에서 `tracker` 코드를 설명할 때는 **계열 버전**을 쓴다 — `Pydantic v2`, `SQLAlchemy 2.0`, `FastAPI 0.140 / 2026-07 기준`.
- 특정 패치 버전이 **논지 자체**일 때만(예: 0.135.0 SSE 내장, 0.137.0 라우터 트리, 0.132.0 `strict_content_type`) 정확히 쓴다.
- 이유: FastAPI는 월 3~5회 릴리스한다. 14장에 `0.140.0`을 흩뿌리면 책이 발간 즉시 낡는다.

**금지:** SQLAlchemy 2.1(2.1.0b3 / 2026-06 베타)을 코드 전제로 쓰지 않는다. `sqlmodel`(0.0.39)을 `tracker`에 쓰지 않는다 — 6장이 "공식 튜토리얼은 SQLModel을 쓴다"는 **사실을 서술**하되 예제 앱은 SQLAlchemy 2.0으로 간다.

---

## 2. 모듈 레이아웃 (확정)

```
tracker/
├── pyproject.toml                    # uv 프로젝트
├── uv.lock
├── .env.example
├── alembic.ini
├── Dockerfile
├── .github/workflows/ci.yml
├── alembic/
│   ├── env.py
│   └── versions/
├── k8s/                              # 13장
│   ├── deployment.yaml
│   └── service.yaml
├── src/tracker/
│   ├── __init__.py
│   ├── main.py                       # FastAPI 인스턴스 · lifespan · 라우터/핸들러 등록
│   ├── settings.py                   # Settings · get_settings
│   ├── deps.py                       # 의존성 함수 + Annotated 별칭
│   ├── errors.py                     # 예외 계층 · ErrorResponse · 예외 핸들러
│   ├── middleware.py                 # RequestIdMiddleware
│   ├── db.py                         # engine · session factory
│   ├── security.py                   # 해시 · 토큰 (10장)
│   ├── events.py                     # 이벤트 팬아웃 (7장)
│   ├── tasks.py                      # 백그라운드·큐 (8장)
│   ├── observability.py              # 로깅·OTel·메트릭 (14장)
│   ├── models/                       # SQLAlchemy 매핑
│   │   ├── base.py                   # Base(DeclarativeBase)
│   │   ├── user.py  project.py  issue.py
│   │   ├── comment.py  label.py  attachment.py
│   ├── schemas/                      # Pydantic 모델
│   │   ├── common.py                 # ErrorResponse · ErrorDetail · Page
│   │   ├── user.py  project.py  issue.py  comment.py  label.py
│   ├── repositories/                 # 영속화 어휘
│   │   ├── project.py  issue.py  comment.py  label.py  user.py
│   ├── services/                     # 도메인 어휘
│   │   ├── project.py  issue.py  attachment.py  notification.py  report.py
│   ├── clients/                      # 외부 서비스 호출 (9장)
│   │   └── search.py
│   ├── api/                          # 라우터
│   │   ├── health.py  auth.py  projects.py  issues.py
│   │   ├── comments.py  labels.py  attachments.py
│   │   ├── realtime.py               # WebSocket + SSE (7장)
│   │   ├── admin.py                  # Jinja2 + HTMX (9장)
│   │   └── graphql.py                # Strawberry (9장)
│   ├── templates/                    # 9장
│   └── static/                       # 9장
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

### 파일별 첫 등장 · 변경 장

| 파일 | 첫 등장 | 이후 변경 |
|---|---|---|
| `pyproject.toml` · `uv.lock` | **1** | 2·6·7·8·9·10·11·12 (의존성 추가) |
| `src/tracker/main.py` | **1** | 2(라우터 등록) · 3(예외 핸들러) · 4(lifespan·미들웨어) · 9(정적/템플릿) · 13(health 라우터 이동) · 14(관측성 배선) |
| `src/tracker/api/health.py` | **13** | — (1장의 `/healthz`가 `main.py`에서 여기로 **이동**, `/ready` 추가) |
| `src/tracker/api/projects.py` · `issues.py` | **2** | 3(스키마 적용) · 4(의존성) · 6(세션) · 10(인가) |
| `src/tracker/services/*.py` | **2** (골격) | 6(쿼리 채움) · 7·8·10 |
| `src/tracker/repositories/*.py` | **2** (골격) | 6(쿼리 채움) |
| `src/tracker/settings.py` | **2** | 6(DB 필드 사용) · 10(시크릿 필드) · 14(관측성 필드) |
| `src/tracker/schemas/issue.py` 등 | **3** | 9(GraphQL 대조) |
| `src/tracker/schemas/common.py` | **3** | — |
| `src/tracker/errors.py` | **3** | 4(핸들러 등록 메커니즘 설명) · 10(권한 에러) |
| `src/tracker/deps.py` | **4** (스텁) | 6(`get_session` 완성) · 10(`get_current_user` 완성 + 인가) |
| `src/tracker/middleware.py` | **4** | 14(요청 ID ↔ 로그 상관관계) |
| `src/tracker/services/attachment.py` | **5** (순수 함수만) | 8(업로드 경로 연결) |
| `src/tracker/db.py` · `models/*` · `alembic/` | **6** | 8(`Attachment` 사용) · 11(테스트 롤백) |
| `src/tracker/events.py` · `api/realtime.py` | **7** | 11(테스트) |
| `src/tracker/tasks.py` · `api/attachments.py` | **8** | 13(grace period) |
| `src/tracker/api/admin.py` · `graphql.py` · `clients/search.py` · `templates/` · `static/` | **9** | 13(정적 파일 배포) |
| `src/tracker/security.py` · `api/auth.py` | **10** | 11(인증 경로 테스트) |
| `tests/conftest.py` · `tests/**` | **11** | 12(CI에서 실행) |
| `.github/workflows/ci.yml` | **12** | 13(이미지 푸시 잡) |
| `Dockerfile` · `k8s/*` | **13** | — |
| `src/tracker/observability.py` | **14** | — |

> **📌 전방 참조 규칙 (2장 전용).** 2장의 서비스·리포지터리 골격은 생성자 첫 인자로 `session: AsyncSession`을 받는 **모양만** 확정한다. 세션을 **어디서 얻는가**는 4장, 실제 매핑·쿼리는 6장이다. 2장은 `AsyncSession` 타입 이름만 참조하고 `db.py`를 만들지 않는다.

---

## 3. 이름 사전 (가장 중요 — 여기 있는 이름만 쓴다)

> 이 절의 이름은 **전부 저자가 발명한 것**이다(라이브러리 API가 아니다). 따라서 프로바넌스 규율의 대상이 아니며, `fact-checker`의 판정 대상도 아니다. **주저 없이 그대로 쓰라. 흔들리면 책이 갈라진다.**

### 3-1. 도메인 엔티티 (SQLAlchemy 모델 클래스)

| 개념 | 클래스명 | `__tablename__` | PK |
|---|---|---|---|
| 사용자 | `User` | `users` | `id: Mapped[int]` |
| 프로젝트 | `Project` | `projects` | `id: Mapped[int]` |
| 이슈 | `Issue` | `issues` | `id: Mapped[int]` |
| 댓글 | `Comment` | `comments` | `id: Mapped[int]` |
| 라벨 | `Label` | `labels` | `id: Mapped[int]` |
| 첨부 | `Attachment` | `attachments` | `id: Mapped[int]` |
| 이슈-라벨 (N:M) | `IssueLabel` | `issue_labels` | 복합 (`issue_id`, `label_id`) |
| 프로젝트 멤버십 | `ProjectMember` | `project_members` | 복합 (`project_id`, `user_id`) |

- **Base 클래스:** `class Base(DeclarativeBase): pass` — `src/tracker/models/base.py`. 이름은 `Base` **하나뿐**이다.
- **테이블명 규약:** snake_case **복수형**. 엔티티 클래스는 단수 PascalCase.
- **N:M은 association object 클래스**(`IssueLabel`·`ProjectMember`)로 표현한다. 이유는 §8-T1 참조 — `Table(...)` 구문이 레퍼런스에 없어서, 추적 가능한 경로를 택했다.
- **공통 컬럼명:** `id` · `created_at` · `updated_at` · 외래키는 `{단수}_id`(`project_id`·`issue_id`·`author_id`·`assignee_id`·`uploader_id`).
- **열거형:** `IssueStatus`(`open`·`in_progress`·`resolved`·`closed`) · `IssuePriority`(`low`·`normal`·`high`·`urgent`) · `ProjectRole`(`member`·`maintainer`·`owner`). 위치는 `src/tracker/models/issue.py`·`project.py`.

### 3-2. Pydantic 스키마 명명 규약 (접미사 4종 — 전 챕터 동일)

| 접미사 | 용도 | 예 |
|---|---|---|
| `Base` | 생성·응답이 공유하는 필드 묶음 (선택) | `IssueBase` |
| `Create` | 생성 요청 본문 (POST) | `IssueCreate` |
| `Patch` | 부분 수정 요청 본문 (PATCH). 전 필드 `| None = None` | `IssuePatch` |
| `Read` | 응답 (`response_model`) | `IssueRead` |

- **🚫 금지 접미사:** `Update` · `DTO` · `Schema` · `In` · `Out` · `Model` · `Response`(단, §3-5의 `ErrorResponse`는 예외로 확정된 이름).
- 중첩 응답이 필요하면 `IssueReadWithComments`처럼 `Read` **뒤에** 붙인다.
- 목록 응답은 `schemas/common.py`의 제네릭 `Page[IssueRead]`(필드: `items` · `total` · `limit` · `offset`).
- **파일 배치:** `src/tracker/schemas/{엔티티 소문자 단수}.py`.

### 3-3. 서비스·리포지터리 계층

| 계층 | 클래스명 | 파일 | 생성자 | 어휘 |
|---|---|---|---|---|
| 리포지터리 | `IssueRepository` · `ProjectRepository` · `CommentRepository` · `LabelRepository` · `UserRepository` | `repositories/{단수}.py` | `__init__(self, session: AsyncSession)` | **영속화**: `get` · `list` · `add` · `delete` |
| 서비스 | `IssueService` · `ProjectService` · `AttachmentService` · `NotificationService` · `ReportService` | `services/{단수}.py` | `__init__(self, session: AsyncSession)` | **도메인**: `create_issue` · `update_issue` · `assign_issue` · `change_status` · `add_comment` |

- 서비스 메서드는 **도메인 동사 + 목적어**(`change_status`), 리포지터리 메서드는 **영속화 동사**(`get`). 이 구분이 2장 「서비스 레이어를 둘 것인가」 절의 논지를 코드로 보여준다.
- 서비스가 리포지터리를 갖는다: `self.issues = IssueRepository(session)`.

### 3-4. 의존성 함수 · `Annotated` 별칭 · 설정

| 이름 | 파일 | 반환 | 첫 등장 |
|---|---|---|---|
| `get_settings()` | `settings.py` | `Settings` | 2장 |
| `get_session()` | `deps.py` → 6장부터 `db.py` 위임 | `-> AsyncIterator[AsyncSession]` (`yield`) | 4장(스텁) → 6장(완성) |
| `get_current_user()` | `deps.py` | `-> User` | 4장(스텁) → 10장(완성) |
| `get_issue_service()` · `get_project_service()` | `deps.py` | 해당 서비스 | 4장 |
| `require_project_member(role)` | `deps.py` | 의존성 함수를 돌려주는 팩토리 | 10장 |
| `get_event_bus()` | `deps.py` | `EventBus` | 7장 |

**의존성 함수 명명 규약:** 값을 제공하면 `get_{명사}`, 검사만 하면 `require_{조건}`. 그 외 접두사(`provide_`·`fetch_`·`current_`)는 쓰지 않는다.

**`Annotated` 별칭 (전 챕터 공용 — `deps.py`에 정의, 4장에서 도입):**

| 별칭 | 정의 |
|---|---|
| `SettingsDep` | `Annotated[Settings, Depends(get_settings)]` |
| `SessionDep` | `Annotated[AsyncSession, Depends(get_session)]` |
| `CurrentUser` | `Annotated[User, Depends(get_current_user)]` |
| `IssueServiceDep` | `Annotated[IssueService, Depends(get_issue_service)]` |

> 이 별칭들은 **독자가 Java/TS 출신이라 타입이 설명 장치**라는 점을 노린 저자 설계다. 4장이 이 장치를 도입하고, 이후 장은 별칭만 쓴다. 4장 이전(1~3장)의 경로 함수에는 의존성이 등장하지 않는다.

**설정 클래스 (`settings.py`, 2장 확정 — 🚨 필드명을 후속 장이 바꾸지 않는다):**

- 클래스명 `Settings`, 베이스 `pydantic_settings.BaseSettings`, 인스턴스 획득은 `get_settings()`(`functools.lru_cache` 적용).
- **환경 변수 접두사 `TRACKER_`** (예: `TRACKER_DATABASE_URL`).

| 필드 | 타입 | 도입 장 | 쓰는 장 |
|---|---|---|---|
| `app_name` | `str` | 2 | 2·14 |
| `environment` | `str` (`local`/`ci`/`staging`/`production`) | 2 | 2·12·13 |
| `debug` | `bool` | 2 | 2 |
| `log_level` | `str` | 2 | 14 |
| `database_url` | `str` | 2 | 6·11·13 |
| `db_pool_size` | `int` | 6 | 6·13 |
| `db_max_overflow` | `int` | 6 | 6·13 |
| `redis_url` | `str` | 7 | 7·8 |
| `search_service_url` | `str` | 9 | 9 |
| `jwt_secret_key` | `str` | 10 | 10 |
| `jwt_algorithm` | `str` | 10 | 10 |
| `access_token_expire_minutes` | `int` | 10 | 10 |
| `otel_service_name` | `str` | 14 | 14 |
| `otel_exporter_endpoint` | `str \| None` | 14 | 14 |

> **⚠️ 워커 수는 `Settings`에 넣지 않는다.** uvicorn이 읽는 것은 **접두사 없는 `$WEB_CONCURRENCY`**다(§1-3 `--workers` 기본값). 13장은 이 환경 변수를 직접 다루고, `Settings.worker_count` 같은 필드를 만들지 않는다.

### 3-5. 에러 응답 계약 (3장이 정의 · 전 챕터가 소비)

`src/tracker/schemas/common.py`:

| 스키마 | 필드 |
|---|---|
| `ErrorResponse` | `code: str` · `message: str` · `details: list[ErrorDetail] \| None` · `request_id: str` |
| `ErrorDetail` | `field: str \| None` · `reason: str` |

- `code`는 **점 구분 도메인 코드**: `issue.not_found` · `project.permission_denied` · `request.validation_failed` · `storage.unavailable`.
- `request_id`는 4장의 `RequestIdMiddleware`가 심는 값과 **같은 값**이다(14장에서 로그와 상관관계를 맺는다).

> 🚨 **RFC 9457 필드명을 쓰지 마라.** `type`·`title`·`status`·`instance`를 쓰면, 3장이 *"2026-07-25 현재 FastAPI 코어에 RFC 9457 지원이 없다"*고 서술한 직후 코드가 시각적으로 준수를 주장하게 된다. 위 4개 필드명은 그 충돌을 피하려고 **의도적으로 다르게 고른 저자 설계**다.
>
> 3장이 "RFC 9457을 흉내 낸다면 어떤 모양인가"를 보여주고 싶다면, **별도의 비교용 코드 블록**에 `📐 저자 설계` 마커와 함께 *"이것은 RFC 9457을 흉내 낸 저자 설계이며 FastAPI가 제공하는 것이 아니다"*를 명시하고 싣는다. `tracker`의 실제 응답 계약은 위 표가 유일하다.
>
> 또한 FastAPI `HTTPException`의 기본 응답은 `{"detail": ...}`(단수)이다. `tracker`의 `details`(복수, 리스트)와 **다른 물건**이라는 점을 3장이 한 번 짚는다.
>
> **3장에 대한 요구:** 이 필드명을 왜 RFC 9457과 다르게 골랐는지를 **본문에 한 번 밝힌다.** 이유를 안 쓰면 독자에게는 그냥 임의의 스키마로 보이고, 이 계약이 내린 가장 중요한 판단이 설명되지 않은 채 지나간다.

### 3-6. 예외 클래스 계층 (`src/tracker/errors.py`, 3장 확정)

```
TrackerError(Exception)                  # 앱 루트. 클래스 속성 code / http_status
├── DomainError                          # 도메인 규칙 위반
│   ├── NotFoundError                    # 404
│   ├── PermissionDeniedError            # 403
│   ├── ConflictError                    # 409
│   └── ValidationFailedError            # 422 (도메인 규칙 위반. 스키마 검증과 구분)
└── InfrastructureError                  # 외부 의존 실패
    ├── ExternalServiceError             # 502
    └── StorageError                     # 503
```

- 모든 하위 클래스는 클래스 속성 `code: str`과 `http_status: int`를 갖고, 인스턴스는 `message`와 선택적 `details`를 갖는다.
- **핸들러는 3개뿐이다:** `TrackerError` 핸들러 · `RequestValidationError` 핸들러 · 마지막 방어선 `Exception` 핸들러. 셋 다 `ErrorResponse`를 돌려준다. **후속 장이 네 번째 핸들러를 추가하지 않는다.**
- 10장은 `PermissionDeniedError`를 **재사용**하고 새 예외를 만들지 않는다.

### 3-7. 라우터 규약

- **변수명은 모든 라우터 모듈에서 `router` 하나**다. 등록 측에서 별칭을 준다: `from tracker.api.issues import router as issues_router`.
- **등록은 키워드 인자로만** — `app.include_router(router=issues_router)`. (§1-2: `FastAPI.include_router`와 `APIRouter.include_router`는 파라미터 순서가 다르다.)

| 모듈 | `prefix` | `tags` | 첫 등장 |
|---|---|---|---|
| `api/health.py` | (없음) | `["health"]` | 13 (1장은 `main.py`에 직접) |
| `api/auth.py` | `/auth` | `["auth"]` | 10 |
| `api/projects.py` | `/projects` | `["projects"]` | 2 |
| `api/issues.py` | `/issues` | `["issues"]` | 2 |
| `api/comments.py` | `/issues/{issue_id}/comments` | `["comments"]` | 6 |
| `api/labels.py` | `/labels` | `["labels"]` | 6 |
| `api/attachments.py` | `/issues/{issue_id}/attachments` | `["attachments"]` | 8 |
| `api/realtime.py` | (없음) | `["realtime"]` | 7 |
| `api/admin.py` | `/admin` | `["admin"]` | 9 |
| `api/graphql.py` | `/graphql` | **`tags` 규약 밖** — GraphQL 라우터는 REST 태그 체계에 넣지 않는다 | 9 |

- **`tags`는 소문자 복수형 문자열 하나**. 한글 태그를 쓰지 않는다(`/docs` 그룹명이 된다).
- **경로 파라미터명:** `project_id` · `issue_id` · `comment_id` · `label_id` · `attachment_id` · `user_id`. 전부 `int`.
- **🚫 `/api/v1` 같은 버전 접두사를 쓰지 않는다.** 1장이 *"API 버저닝 전략은 이 책에서 다루지 않는다"*고 선언하므로, 코드가 그 선언과 어긋나면 안 된다.
- **고정 경로:** `/healthz`(liveness, **1장부터**) · `/ready`(readiness, 13장) · `/metrics`(14장) · `/docs`·`/openapi.json`(FastAPI 기본).

### 3-8. 실시간·태스크 계층 이름 (7·8장)

| 이름 | 종류 | 파일 | 장 |
|---|---|---|---|
| `IssueEvent` | Pydantic 이벤트 페이로드 (`issue_id`·`event_type`·`payload`·`occurred_at`) | `schemas/common.py` | 7 |
| `EventBus` | 프로토콜 (`publish` · `subscribe`) | `events.py` | 7 |
| `RedisEventBus` | 구현 | `events.py` | 7 |
| `InMemoryEventBus` | 테스트용 구현 | `events.py` | 7 (11장 회수) |
| `ConnectionManager` | WebSocket 연결 보관 | `api/realtime.py` | 7 |
| `generate_thumbnail` | CPU 바운드 순수 함수 | `services/attachment.py` | 5 |
| `build_weekly_report` | 주간 리포트 생성 | `services/report.py` | 8 |
| `enqueue_weekly_report` | 큐 승격 후의 진입점 | `tasks.py` | 8 |

---

## 4. 코드 관용구 규약 (제약 9-(B)-2의 코드 수준 구체화)

**모든 장이 예외 없이 지킨다.** 「틀린 예」는 인터넷 예제에 널려 있어 저술가의 손이 자연스럽게 가는 형태다.

### 4-1. 의존성·파라미터 선언은 `Annotated`

```python
# ✅ 올바른 예
@router.get("/issues", response_model=Page[IssueRead])
async def list_issues(
    session: SessionDep,
    q: Annotated[str | None, Query(min_length=2)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[IssueRead]: ...
```

```python
# ❌ 틀린 예 — 기본값 위치에 Query/Depends를 두는 구식 스타일
async def list_issues(
    q: str = Query(None),
    session: AsyncSession = Depends(get_session),
): ...
```

### 4-2. Pydantic v2 어휘

| ✅ 쓴다 | ❌ 쓰지 않는다 |
|---|---|
| `model_dump()` | `.dict()` |
| `model_dump_json()` | `.json()` |
| `model_validate()` | `parse_obj()` |
| `model_config = ConfigDict(from_attributes=True)` | `class Config: orm_mode = True` |
| `@field_validator` / `@model_validator` | `@validator` / `@root_validator` |
| `pattern=` | `regex=` |
| `from pydantic_settings import BaseSettings` | `from pydantic import BaseSettings` |

### 4-3. SQLAlchemy 2.0 스타일

```python
# ✅ 올바른 예
class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="issue", cascade="all, delete-orphan"
    )
```

```python
# ❌ 틀린 예
Base = declarative_base()

class Issue(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
```

| ✅ 쓴다 | ❌ 쓰지 않는다 |
|---|---|
| `class Base(DeclarativeBase)` | `declarative_base()` |
| `Mapped[...]` + `mapped_column()` | `Column(...)` 클래스 속성 |
| `\| None` 유무로 nullable 결정 | `nullable=False` 명시 |
| `Mapped[str \| None]` (nullable) | `Mapped[Optional[str]]` — `tracker` 코드는 `\| None`으로 통일. `Optional[]`은 §1-6 Quickstart **인용문 안에서만** 등장한다 |
| `select(Issue)` + `session.scalars(...)` | `session.query(Issue)` |
| `select(func.count()).select_from(Issue)` | `session.query(Issue).count()` |
| `selectinload(Issue.comments)` | 문자열 `joinedload("comments")` (2.0에서 제거) |

- **`execute()` vs `scalars()`:** 엔티티가 필요하면 `scalars()`(6장이 이 구분을 설명한다). `tracker`의 리포지터리는 **`scalars()`를 기본형**으로 쓴다.
- **비동기 세션:** `AsyncSession`, `create_async_engine`, `expire_on_commit=False`. `asyncio.gather()`를 쓸 때는 태스크마다 별도 세션 — 하나를 공유하지 않는다.
- **드라이버 URL:** 프로덕션 `postgresql+asyncpg://`, 테스트 `sqlite+aiosqlite:///` 또는 컨테이너 Postgres. 이 두 개 외의 URL을 예제에 쓰지 않는다.

### 4-4. 앱 수명주기는 `lifespan`

```python
# ✅ 올바른 예 — src/tracker/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = AsyncClient(timeout=5.0)
    yield
    await app.state.http_client.aclose()

app = FastAPI(title="tracker", lifespan=lifespan)
```

```python
# ❌ 틀린 예
@app.on_event("startup")
async def startup(): ...
```

> ⚠️ **단, `on_event`를 "FastAPI가 제거했다"고 쓰지 마라.** 지뢰표 3행 참조 — 0.140.0에는 `@deprecated`가 붙은 채로 **아직 있고**, 제거한 쪽은 Starlette 1.0.0rc1이다. 코드 관용구는 `lifespan`으로 통일하되, **서술은 3층 구조를 정확히** 한다(4장 담당).

- 앱 수명 자원은 **`app.state.{이름}`**에 둔다: `app.state.http_client`(4장) · `app.state.redis`(7장). 모듈 전역 변수에 두지 않는다.

### 4-5. 인증 라이브러리

| ✅ 쓴다 | ❌ 쓰지 않는다 |
|---|---|
| `pwdlib` (`from pwdlib import PasswordHash`, Argon2) | `passlib` / `passlib[bcrypt]` |
| PyJWT (`uv add pyjwt` → `import jwt`) | `python-jose` |

> 🚨 이건 단순 취향이 아니라 **10장의 핵심 논지**다. 다른 장이 무심코 `passlib`·`python-jose`를 쓰면 10장의 오프닝("인터넷 예제 열에 아홉은 `passlib`을 쓴다. 마지막 릴리스는 2020-10-08이다")이 자기 책 안에서 반박당한다. **10장 외의 장에서 인증 코드를 쓸 일이 있으면 이 두 이름만.**
>
> 단, `passlib`을 **레거시 해시 호환용으로 언급**하는 것은 공식 문서 축자에 근거가 있다 — 그건 서술이지 `tracker` 코드가 아니다.

### 4-6. 세션·트랜잭션 경계의 표준형

```python
# ✅ 올바른 예 — src/tracker/db.py (6장)
async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
```

- **커밋은 서비스 계층이 한다.** 의존성은 세션의 **생명주기만** 책임진다. 이 규칙을 6장이 정하고 이후 장 전부가 따른다.
- **`Depends(get_session)`이 표준형이다.** `Depends(get_session, scope="request")`를 표준 관용구로 만들지 마라 — `Depends(scope=)`가 #11107을 해결했는지는 **미확정**이다(지뢰표 2행). `scope=`는 **4장(소개)과 6장(트랜잭션 경계 적용)에서만** 다루는 소재이며, 두 장 모두 "해결했다"로 반올림하지 않는다.
- **`session.commit()` 후 객체를 응답으로 쓰려면** `expire_on_commit=False`(공식이 asyncio에선 정상이라고 명시). `tracker`의 세션 팩토리는 이 설정을 갖는다.

### 4-7. 타입 힌트 스타일 (독자가 Java/TS 출신 — 타입이 설명 장치다)

| 규칙 | 예 |
|---|---|
| 모든 경로 함수·서비스·리포지터리 메서드에 **반환 타입 표기** | `-> IssueRead:` |
| 유니온은 `\|` 문법 (3.10+) | `str \| None` (❌ `Optional[str]`) |
| 제네릭 컨테이너는 내장 타입 | `list[IssueRead]` (❌ `List[IssueRead]`) |
| SQLAlchemy 매핑만 `Mapped[...]` 안에서 문자열 전방 참조 허용 | `Mapped[list["Comment"]]` |
| `Any`는 쓰지 않는다 | — |

> **예외:** §1-6의 SQLAlchemy 공식 Quickstart를 **인용**할 때는 원문의 `Optional[...]`·`List[...]`를 고쳐 쓰지 않는다(제약 9-(A) 인용 코드는 원문 그대로). 인용과 `tracker` 코드의 스타일이 다른 것은 정상이며, 6장이 한 줄로 짚어준다.

### 4-8. 그 밖의 금지 목록

| ❌ | 이유 |
|---|---|
| `ORJSONResponse` · `UJSONResponse` | FastAPI 0.131.0에서 deprecated |
| `sse-starlette` 설치 | SSE는 FastAPI 0.135.0에 내장 — 1차 선택지가 아니다 |
| `broadcaster` | 0.3.1 / 2024-08-01 아카이브됨 (공식 문서가 아직 링크한다는 **사실**은 7장이 서술) |
| `aioredis` | redis-py 8.x에 흡수됨 → `redis.asyncio` |
| `motor` | EOL 지남 (MongoDB를 쓸 일이 있으면 PyMongo async) |
| `uvicorn.workers.UvicornWorker` | import 시 DeprecationWarning → `uvicorn-worker` (13장이 서술) |
| 코드 주석에 동작 설명 지어 넣기 | 제약 9-(B)-4. 적발 사례 1이 정확히 이 유형 |

---

## 5. 「저자 설계」 표시 규약

제약 9-(B)-3 이행. **아래 문자열을 정확히 이 형태로 쓴다** — `fact-checker`와 Phase 4.5가 전수 grep한다.

**형태:** 코드 블록 **바로 앞**에 인용구 한 줄.

```
> **📐 저자 설계 —** {한 문장으로 무엇을 정했고 왜 공식 권장이 아닌지}
```

예:

```
> **📐 저자 설계 —** 아래 팬아웃 배선은 FastAPI 공식 권장이 아니라, 5장의 프로세스 경계로부터 이 책이 도출한 한 가지 안이다.
```

**규칙:**

1. grep 토큰은 **`📐 저자 설계`** 하나다. `「저자 설계」`·`(저자 구성)`·`* 저자 설계 *` 같은 변형을 만들지 않는다.
2. **붙이는 대상:** `tracker`의 구조·배선을 저자가 정한 코드 블록 전부. 계획서가 "저자 설계로 표시"를 명시한 지점(2장 골격 · 3장 에러 계약 · 7장 팬아웃·알림 파이프라인 · 9장 HTMX 배선 · 그 밖의 walkthrough)은 **의무**다.
3. **붙이지 않는 대상:** 공식 문서·소스에서 그대로 옮긴 인용 코드(§6-4의 출처 표기를 대신 붙인다).
4. 한 절에 저자 설계 코드가 연속으로 나오면 **첫 블록에만** 붙이고, 절 안에서 성격이 바뀔 때 다시 붙인다.
5. **산문의 「저자 가설」·「저자 추론」은 이것과 다른 물건이다.** 계획서가 지정한 그 표기(5장 출신 귀속 금지, 13장 서버리스 결론, 14장 로깅 연역)는 산문 표기이며, 이 코드용 마커로 대체하지 않는다. 각자 그대로 쓴다.

---

## 6. 코드 블록 표기 규약

### 6-1. 언어 태그 (이 목록만)

`python` · `bash` · `yaml` · `dockerfile` · `toml` · `ini` · `sql` · `json` · `html` · `text`

- SQLAlchemy가 찍는 SQL·psql 출력 등 실행 결과는 `text`.
- Jinja2 템플릿은 `html`.
- 셸 세션에 출력이 섞이면 `bash` 대신 `text`.

### 6-2. 파일 경로 표시

**코드 블록 첫 줄에 그 언어의 주석으로 프로젝트 루트 기준 상대 경로**를 쓴다. 블록 밖 산문이나 별도 마크업으로 대신하지 않는다(EPUB에서 코드와 분리되면 독자가 잃어버린다).

| 언어 | 형태 |
|---|---|
| python | `# src/tracker/api/issues.py` |
| yaml | `# .github/workflows/ci.yml` |
| dockerfile | `# Dockerfile` |
| toml | `# pyproject.toml` |
| ini | `; alembic.ini` |
| html | `<!-- src/tracker/templates/issue_detail.html -->` |

- **경로를 쓰지 않는 경우:** `bash` 명령, `text` 출력, 그리고 파일에 속하지 않는 개념 설명용 조각(이 경우 첫 줄 주석으로 `# (개념 설명용 — 파일 아님)`).

### 6-3. 생략 표기

두 가지를 **구분**한다.

| 표기 | 의미 |
|---|---|
| `# ...(N장, 생략)` | 앞 장에서 이미 쓴 코드를 생략했다. N에 장 번호를 반드시 넣는다 |
| `...` (Python `Ellipsis` 단독 줄) | **실제 스텁** — 지금은 구현이 없다는 뜻 |

- yaml·dockerfile·toml에서는 `# ...(N장, 생략)` 한 형태만 쓴다.
- 생략 표기를 **연속 3개 이상** 쓰지 않는다. 그 정도면 코드를 다시 통째로 실어야 할 자리다.

### 6-4. 인용 코드의 출처 표기 (제약 9-(A))

코드 블록 **바로 뒤**에 인용구 한 줄. grep 토큰은 **`> 출처:`**.

```
> 출처: {문서 제목 또는 저장소·태그·파일 경로}, {URL} (조회 2026-07-25)
```

예:

```
> 출처: SQLAlchemy 2.0 ORM Quickstart, https://docs.sqlalchemy.org/en/20/orm/quickstart.html (조회 2026-07-25)
> 출처: starlette 1.3.1 태그 `starlette/concurrency.py` (조회 2026-07-25)
```

- **조회 시점은 `2026-07-25`로 통일**한다(레퍼런스 전 항목의 조회일). 저술 중 저술가가 **직접 새로 확인한** 1차 소스만 그날 날짜를 쓴다.
- 출처를 못 다는 인용 코드는 **싣지 않고 산문으로 설명한다**(제약 9-(A)).

---

## 7. 장별 코드 성장 맵

> **목적: 앞 장에 이미 있는 것을 다시 정의하지 않게 한다.** "내 장에서 처음 만드는 것"과 "이미 있는 것"을 이 표로 가른다.

| 장 | **새로 만든다** | **바꾼다** | **이미 있다 — 다시 정의하지 마라** |
|---|---|---|---|
| **1** | `pyproject.toml`·`uv.lock`(uv 프로젝트), `src/tracker/main.py`(`app = FastAPI(...)`), `GET /healthz` | — | — |
| **2** | `api/projects.py`·`api/issues.py`(라우터, 스키마 없이 뼈대), `services/`·`repositories/` 골격, `settings.py`(`Settings`·`get_settings`) | `main.py`(라우터 등록) | `app` 인스턴스, `/healthz` |
| **3** | `schemas/issue.py`(`IssueBase`/`Create`/`Patch`/`Read`), `schemas/common.py`(`ErrorResponse`·`ErrorDetail`·`Page`), `errors.py`(예외 계층 + 핸들러 3개) | 라우터에 `response_model` 부착 | 라우터 파일, `Settings` |
| **4** | `deps.py`(`get_session`·`get_current_user` **스텁**, `SessionDep`·`CurrentUser`·`SettingsDep`·서비스 Dep), `middleware.py`(`RequestIdMiddleware`) | `main.py`(lifespan + `app.state.http_client` + 미들웨어 등록) | 예외 핸들러(3장). **예외 처리 "메커니즘"만 다루고 응답 계약은 3장 참조** |
| **5** | `services/attachment.py`의 `generate_thumbnail`(순수 함수) + 그것을 부르는 경로 함수 | — | **⚠️ `Attachment` 모델은 아직 없다(6장). 업로드 엔드포인트도 없다(8장).** 5장은 ORM을 건드리지 않고 바이트를 받는 함수만 다룬다 |
| **6** | `db.py`(엔진·세션 팩토리·`get_session` **완성**), `models/base.py`(`Base`), `models/*`(`User`·`Project`·`Issue`·`Comment`·`Label`·`Attachment`·`IssueLabel`·`ProjectMember`), `alembic/`(첫 리비전), `api/comments.py`·`api/labels.py` | 리포지터리·서비스에 실제 쿼리 채움, `deps.py`의 `get_session`이 `db.py`로 위임 | `Settings.database_url`(2장), `SessionDep`(4장), 스키마(3장) |
| **7** | `events.py`(`EventBus`·`RedisEventBus`·`InMemoryEventBus`), `api/realtime.py`(WS `/ws/issues/{issue_id}` + SSE `/issues/{issue_id}/events`), `ConnectionManager`, `IssueEvent` | `main.py` lifespan에 `app.state.redis` 추가, `services/issue.py`가 이벤트 발행 | `Issue` 모델(6장), 세션 의존성(4·6장), **5장의 "워커는 메모리를 공유하지 않는다"** |
| **8** | `api/attachments.py`(업로드), `tasks.py`, `services/report.py`(`build_weekly_report`) | `services/attachment.py`가 `Attachment` 모델과 연결 | `Attachment` 모델(6장), `generate_thumbnail`(5장), `EventBus`(7장) |
| **9** | `api/admin.py`+`templates/`+`static/`, `api/graphql.py`(Strawberry), `clients/search.py` | `main.py`(템플릿·정적 마운트) | `app.state.http_client`(4장 lifespan) — **`AsyncClient`를 새로 만들지 마라**, 스키마(3장), 서비스(2·6장) |
| **10** | `security.py`(`PasswordHash`·토큰 발급/검증), `api/auth.py`, `deps.py`의 `require_project_member` | `deps.py`의 `get_current_user` **완성**(스텁 → 실제), `Settings`에 시크릿 3필드 추가, `models/user.py`에 해시 컬럼 | `User`·`ProjectMember` 모델(6장), `PermissionDeniedError`(3장) — **새 예외 만들지 마라**, `CurrentUser` 별칭(4장) |
| **11** | `tests/conftest.py`(`anyio_backend`·오버라이드·DB 롤백), `tests/unit/`, `tests/integration/` | — | `dependency_overrides`(4장), 롤백 레시피(6장), WS·SSE 엔드포인트(7장), `InMemoryEventBus`(7장) |
| **12** | `.github/workflows/ci.yml` | `pyproject.toml`(개발 의존성·도구 설정) | 테스트 스위트(11장), uv 프로젝트(1장) |
| **13** | `Dockerfile`(멀티스테이지·비루트), `k8s/deployment.yaml`·`service.yaml`, `api/health.py`, `GET /ready` | **`/healthz`를 `main.py` → `api/health.py`로 이동**(경로는 그대로), 이미지 빌드·푸시 잡을 `ci.yml`에 추가 | `/healthz` 경로(1장) — **이름을 바꾸지 마라**, `ci.yml`(12장), 풀 크기 설정(6장), grace period 요구(8장) |
| **14** | `observability.py`(structlog 배선·OTel 계측·`/metrics`) | `middleware.py`의 요청 ID를 로그 컨텍스트에 연결, `Settings`에 `otel_*` 2필드 추가 | `RequestIdMiddleware`(4장), `request_id` 필드(3장 `ErrorResponse`), `/healthz`·`/ready`(13장) |

**교차 규칙 3가지:**

1. **의존성 추가는 그 장에서 처음 쓰는 장이 한다.** `uv add {패키지}` 한 줄을 그 장 본문에 남긴다. 뒤 장은 이미 설치된 것으로 간주한다.
2. **완성 ≠ 재정의.** 4장의 스텁 시그니처(`get_session() -> AsyncIterator[AsyncSession]`, `get_current_user() -> User`)를 6·10장이 **채운다**. 시그니처를 바꾸지 않는다.
3. **경로·필드명은 도입한 장이 소유한다.** 후속 장이 이름을 바꾸고 싶으면 바꾸지 말고 `editor_notes` 대상으로 오케스트레이터에 보고한다.

---

## 8. 🚨 API 표면 추적 결과

> **읽는 순서: 코드를 쓰기 전에 여기부터.** 아래 T2·T3에 해당하는 이름은 **계약이 확정해주지 않는다.** 저술가가 규정된 절차를 밟아야 한다.

### 8-0. 면제 (추적 대상 아님)

- **§3의 이름 전부** — 저자가 발명한 것이라 라이브러리 API가 아니다. 추적 불필요.
- **Python 표준 라이브러리** — `typing`(`Annotated`·`Literal`·`AsyncIterator`) · `contextlib`(`asynccontextmanager`) · `datetime` · `enum` · `uuid` · `functools`(`lru_cache`) · `pathlib` · `logging` · `asyncio`. 제약 9-(B)-1의 "모든 import 경로"를 표준 라이브러리까지 확장하면 `import datetime`조차 쓸 수 없어 과잉 적용이 된다.

### 8-1. ✅ 추적됨 — 그대로 쓴다 (근거 절 병기)

| 영역 | 추적된 표면 | 근거 |
|---|---|---|
| FastAPI 앱·라우터 | `FastAPI(...)` 전 파라미터, 경로 데코레이터 전 파라미터(`response_model`·`status_code`·`tags`·`dependencies`·`responses`·`operation_id`·`response_class`·`include_in_schema` …), `APIRouter(...)` 전 파라미터(`prefix`·`tags`·`dependencies` …), `include_router`(키워드 전용), `strict_content_type`, `iter_route_contexts()`, OpenAPI 3.1.0 | §1-2, §3-2 |
| 파라미터 선언 | `Path`·`Query`·`Header`·`Cookie`·`Body`·`Form`·`File` + 공통 인자(`gt`·`ge`·`lt`·`le`·`min_length`·`max_length`·`pattern`·`discriminator`·`alias`·`examples` …), `Annotated[str, Query()]` | §1-2, §5-9 |
| 의존성 | `Depends(dependency, *, use_cache=True, scope=Literal["function","request"]\|None)`, `app.dependency_overrides[...]`, `app.dependency_overrides = {}`, `app.state` | §1-2, §3-8, §5-A |
| 수명주기 | `lifespan` 파라미터, `@app.on_event`(deprecated·존치), ASGI `scope`/`receive`/`send`, `root_path` | §1-1, §5-9 |
| 동시성 | `run_in_threadpool`, `anyio.to_thread.run_sync`, `CapacityLimiter`, `anyio.to_thread.current_default_thread_limiter().total_tokens` | §1-3 |
| 업로드 | `UploadFile`, `spool_max_size`, `max_part_size` (각 1MB) | §1-4 |
| 백그라운드 | `BackgroundTasks` | §1-5 |
| SPA·템플릿 | `app.frontend(path, directory, fallback="auto", check_dir=True)`, `Jinja2Templates`, `StaticFiles`, `TemplateResponse`(인자 순서 변경 사실) | §1-2, §1-5 |
| Pydantic v2 | `model_dump()`·`model_dump_json()`·`model_validate()`·`from_attributes`·`@field_validator`·`@model_validator`·`model_config = ConfigDict(...)`·`pattern`, `pydantic_settings.BaseSettings` | §5-9 |
| SQLAlchemy 매핑 | `DeclarativeBase`·`Mapped[...]`·`mapped_column(primary_key=…)`·`relationship(back_populates=…, cascade="all, delete-orphan")`·`ForeignKey`·`String(n)`·`__tablename__`, 타입의 nullable 표기로 nullable 결정 (원문은 `Optional[]`, `tracker`는 `\| None` — §4-7 참조) | §1-6 |
| SQLAlchemy 쿼리 | `select()`·`Session.execute()`·`Session.scalars()`·`session.scalar(select(func.count()).select_from(...))`·`selectinload`·`lazy="raise"`·`AsyncAttrs`·`awaitable_attrs`·`run_sync` | §1-6 |
| SQLAlchemy 비동기 | `AsyncSession`·`create_async_engine`·`AsyncAdaptedQueuePool`·`expire_on_commit=False`·`await engine.dispose()`, 풀 인자 `pool_size`·`max_overflow`·`pool_timeout`·`pool_recycle`·`pool_pre_ping` | §1-6 |
| 드라이버 URL | `postgresql+asyncpg`·`postgresql+psycopg`·`postgresql+psycopg2`·`sqlite+aiosqlite`·`mysql+asyncmy`·`mysql+aiomysql` | §1-6 |
| 테스트 | `from httpx import ASGITransport, AsyncClient`, `TestClient`, `@pytest.mark.anyio`, `anyio_backend` fixture, `asyncio_mode`, `LifespanManager`(asgi-lifespan), `join_transaction_mode="create_savepoint"` + `engine.connect()`/`connection.begin()`/`trans.rollback()`/`Session(bind=…)`, httpx2의 `EventSource`·`ServerSentEvent`·`httpx2.websockets` | §5-A, §5-6 |
| 인증 (import 경로만) | `from pwdlib import PasswordHash`, `import jwt`(pyjwt), `pyjwt[crypto]` | §2-3 |
| uvicorn | `--workers`·`--loop`·`--http`·`--limit-concurrency`·`--backlog`(2048)·`--timeout-keep-alive`(5)·`--timeout-graceful-shutdown`·`--proxy-headers`·`--forwarded-allow-ips`(`127.0.0.1`)·`--host`·`--port`, `$WEB_CONCURRENCY`, `uvicorn[standard]` 구성 6종, `fastapi run --workers`, `uvicorn-worker` | §1-3, §5-D |
| uv·CI | `uv add`·`uv run`·`uv sync --frozen`·`uv sync --locked`·`--no-install-project`·`uv pip compile`, `uv.lock`·`pyproject.toml`·`pylock.toml`, `astral-sh/setup-uv`(v9, `enable-cache`)·`actions/setup-python`(v7, `cache:`) | §5-C |
| 컨테이너·K8s | Uvicorn 공식 Dockerfile 전문(캐시/바인드 마운트), `groupadd --system --gid 999 nonroot`+`USER nonroot`, `/healthz`·`/ready` 분리, `periodSeconds`·`timeoutSeconds`·`failureThreshold`·`httpGet`·`terminationGracePeriodSeconds`·`preStop`, `PORT`·`0.0.0.0` | §5-D |

### 8-2. ⚠️ 미추적 T1 — 레퍼런스 침묵 · 모호함 없음 → **각주 1회로 해소**

레퍼런스 §1-2는 **파라미터 목록의 AST 추출**이지 심볼 카탈로그가 아니다. 그래서 아래 심볼들은 이 책에서 반드시 필요한데도 레퍼런스에 문자열로 존재하지 않는다. 제약 9-(B)-1의 **필수 예외** 경로로 처리한다.

**절차:** 아래 표의 **소유 장이 1차 소스에서 확인하고 각주를 한 번 단다.** 그 장 이후의 장은 각주 없이 그대로 쓴다. 소유 장이 1차 소스 확인에 **실패하면** 코드를 빼고 산문으로 설명하고, 그 사실을 해당 장 「근거 두께」에 적는다(제약 9-(B)-1 필수 예외 원문).

| 심볼 / 표면 | 소유 장 | 확인할 1차 소스 |
|---|---|---|
| `pydantic.BaseModel`, `pydantic.Field` | **3** | Pydantic v2 공식 문서 |
| `model_dump(exclude_unset=…, exclude_none=…)` — **`Patch` 병합의 표준 수단** | **3** | 동상. 3장이 확인해 각주를 달면, 이후 전 장이 이 형태로 부분 수정을 처리한다 |
| Pydantic v2 제네릭 모델 (`Page[IssueRead]`의 `TypeVar` 파라미터화) | **3** | 동상. 확인 실패 시 `Page`를 제네릭 없이 `IssueListRead` 같은 구체 클래스로 폴백 |
| `fastapi.HTTPException` | **3** | FastAPI 공식 문서 (Handling Errors) |
| `@app.exception_handler(...)` / `add_exception_handler` | **3** | 동상 |
| `fastapi.exceptions.RequestValidationError` | **3** | 동상 |
| `fastapi.responses.JSONResponse` | **3** | 동상 |
| `fastapi.status` 상수 (`status.HTTP_404_NOT_FOUND` 등) | **3** | 동상 |
| `pydantic_settings.SettingsConfigDict` (`env_prefix`·`env_file`) | **2** | pydantic-settings 공식 문서 |
| `sqlalchemy.ext.asyncio.async_sessionmaker` | **6** | SQLAlchemy 2.0 asyncio 문서 |
| SQLAlchemy 컬럼 타입 `DateTime`·`Text`·`Boolean`·`Integer`, 그리고 **레거시 대조용 `Column(...)`** (§4-3의 ❌ 예) | **6** | SQLAlchemy 2.0 타입 문서 / 1.x 레거시 문서. `declarative_base()`가 `DeclarativeBase`로 대체됐다는 *사실*은 추적됨(§1-6 축자)이나, `Column(Integer, …)` 호출 형태 자체는 아니다 |
| `mapped_column(index=…, unique=…, server_default=…)` | **6** | 동상 |
| `Mapped[IssueStatus]` 자동 Enum 매핑 | **6** | 확인 실패 시 **`Mapped[str]` 폴백**(계약이 미리 허용) |
| `relationship(secondary=…)` | **6** | 확인 실패 시 **association object 유지**(§3-1 기본형) |
| Alembic `env.py` 비동기 표면 · `alembic revision --autogenerate` · `alembic upgrade head` | **6** | 계획 9-(B)-1이 **이미 명시적으로 허용한 예외 구역** |
| `fastapi.responses.StreamingResponse` | **7** | FastAPI 공식 문서 |
| `fastapi.WebSocket`·`WebSocketDisconnect`·`websocket.accept()`/`send_json()`/`receive_text()` | **7** | FastAPI 공식 문서 (WebSockets) |
| FastAPI 0.135.0 내장 SSE의 **호출 표면** (내장됐다는 *사실*은 추적됨) | **7** | FastAPI 0.135.0 릴리스 노트·문서 |
| `redis.asyncio` pub/sub 호출 표면 | **7** | redis-py 8.x 문서 |
| `UploadFile`의 메서드·속성(`.read()`·`.file`·`.filename`·`.content_type`) | **8** | Starlette 1.3.1 소스 |
| Strawberry 표면 (`@strawberry.type`·`Schema`·`GraphQLRouter`) | **9** | Strawberry 0.323 문서 |
| `httpx.AsyncClient` 생성자 인자 `timeout` · `.aclose()` (§4-4 lifespan 예제가 이미 쓴다) | **4** | httpx 문서 |
| `httpx.AsyncClient`의 `limits`·`base_url`·`transport`, `retries`의 **코드 표면** | **9** | httpx 문서 (`retries`가 연결 실패만 재시도한다는 *사실*은 추적됨) |
| structlog·`opentelemetry-instrumentation-fastapi`·`prometheus_client` 호출 표면 | **14** | 각 공식 문서 |
| `BaseHTTPMiddleware` / 순수 ASGI 미들웨어 **작성 형태** | **4** | Starlette 1.3.1 소스·문서. **⚠️ 한계는 T3 — 단정 금지** |

### 8-3. 🚨 미추적 T2 — 프로바넌스 위험 구역 → **계약이 이름을 확정하지 않는다**

§7-5가 **날조 2건이 적발된 영역**으로 지목한 곳이다. 여기서 계약이 이름을 고정하면, 계약이 바로 그 날조를 세탁하게 된다. **그래서 고정하지 않는다.**

| 표면 | 장 | 저술가가 할 일 |
|---|---|---|
| `OAuth2PasswordBearer` · `OAuth2PasswordRequestForm` · `SecurityScopes` · `Security(...)` | **10** | **1차 소스(FastAPI 보안 튜토리얼 원문) 재확인 없이는 코드에 쓰지 마라.** 확인하면 각주와 함께 싣고, 확인 못 하면 **산문으로만** 설명한다 |
| PyJWT 호출 표면 `jwt.encode(...)` · `jwt.decode(...)` (import 경로 `import jwt`는 추적됨) | **10** | 동상 |
| pwdlib 호출 표면 `PasswordHash.recommended()` · `.hash()` · `.verify()` (import 경로는 추적됨) | **10** | 동상 |
| Auth0 연동 코드 일체 | **10** | **적발된 날조 사례 2번의 진원지**(`fastapi_plugin.fast_api_client`). 원문 재확인 실패 시 **코드 금지** |
| testcontainers Python API | **11** | 요약 경유 오염 위험 구역. 원문 재확인 후 각주, 실패 시 산문 |
| Azure Bicep · Azure Container Apps 매니페스트 | **13** | 동상. 계획이 이미 "PaaS는 짧은 표 + 미확인 명시"로 제한했다 |

> **판정 우선순위:** T2 구역에서 확인에 실패했는데 코드가 꼭 필요하다고 느껴지면, 그건 **코드가 필요한 게 아니라 산문이 필요한 것**이다. 제약 9-(A)의 원문 그대로다 — *"재확인이 안 되면 코드를 빼고 산문으로 설명한다."*

### 8-4. 🕒 미추적 T3 — §7-4 미확인 목록 → **`(사실 확인 필요)` 마커**

레퍼런스가 스스로 "미확인"으로 신고한 것들이다. 코드나 수치로 단정하지 말고, 그 줄에 `(사실 확인 필요)`를 달아 `fact-checker`로 넘긴다.

| 항목 | 관련 장 |
|---|---|
| uvicorn `--timeout-graceful-shutdown` **기본값** | 13 |
| `BaseHTTPMiddleware`의 **구체적 한계** (구조 대조·선택 기준까지만 안전) | 4 |
| lifespan이 **멀티 워커·서버리스에서 워커별 실행되는지** | 4·13 |
| redis-py asyncio `ConnectionPool` 기본값 | 7 |
| SQLAlchemy 2.1 GA 일정 · `Query` 실제 제거 여부 | 6 |
| `validation_error_response_definition` 현행 소스 위치 | 3 |
| `alias_httpx` 동작 | 11 |
| mypy 2.x · pytest 9.x · gunicorn 26.x breaking change 내역 | 12·13 |
| ruff formatter "stable" 선언 여부 | 12 |
| APScheduler 등 개별 스케줄러 (버전 핀 표에 없음) | 8 |
| pybreaker asyncio 지원 | 9 |
| Celery asyncio 네이티브 지원 (공식 진술 미확보) | 8 |
| free-threading 기본 빌드 전환 시점 · 벤치마크 | 5 |
| Railway·Render·Fly.io·Azure Container Apps 계약 | 13 |

### 8-5. 완결성 선언

**이 계약에 등장하는 코드 식별자는 §3(저자 발명) · §8-0(표준 라이브러리) · §8-1(추적됨) · §8-2/8-3/8-4(미추적, 처리 절차 지정됨) 중 정확히 하나에 속한다.** 저술가가 이 다섯 범주 어디에도 없는 이름을 쓰게 되면, 그건 **계약 밖**이다 — 1차 소스를 확인해 각주를 달거나 `(사실 확인 필요)`를 달고, 오케스트레이터에 보고한다. 추측으로 메우지 마라.

---

## 부록. 저술 중 발견된 계획서상의 코드 관련 공백 (editor·오케스트레이터 참고)

계약을 만들며 해소한 것들이다. 계약이 이미 결정했으므로 저술가가 다시 판단할 필요는 없다.

| # | 계획서 상태 | 계약의 결정 |
|---|---|---|
| 1 | 1장 "헬스 엔드포인트 하나" vs 13장 "`/healthz`·`/ready` 분리" — 1장의 경로 미지정 | **1장부터 `/healthz`.** 13장은 `/ready`를 **추가**하고 `/healthz`를 `api/health.py`로 **이동**만 한다 (경로 불변) |
| 2 | 예제 앱 소개는 "프로젝트·이슈·댓글·첨부·알림"인데 계획 본문의 엔티티 열거는 "프로젝트·이슈·댓글·라벨"뿐 — **`Attachment` 엔티티 미정의** | `Attachment` 확정, 6장이 정의 |
| 3 | **순서 역전:** 5장이 첨부 썸네일을 쓰는데 첨부 업로드는 8장, 모델은 6장 | 5장은 **ORM·엔드포인트를 건드리지 않고** 순수 함수 `generate_thumbnail`만. §7 성장 맵에 명시 |
| 4 | 2장이 `Settings` **클래스만** 정하면 6장은 `database_url`, 13장은 `db_url`을 쓰게 됨 | §3-4에 **필드명 전체 표** 확정 + 도입 장·소비 장 표기 |
| 5 | 4장의 `get_session`·`get_current_user` "자리표시자"가 6·10장에서 "완성" — 시그니처 미고정 시 재정의 충돌 | §3-4에 스텁 시그니처 고정 + §7 교차 규칙 2("완성 ≠ 재정의") |
| 6 | 3장이 RFC 9457 **미지원**을 서술하는데 에러 스키마 필드명 미정 — `type`/`title`/`status`/`instance`를 쓰면 코드가 준수를 주장 | `code`/`message`/`details`/`request_id`로 **의도적으로 다르게** 확정. RFC 9457 모양은 별도 비교 블록 + `📐 저자 설계` 마커로만 |
| 7 | 워커 수를 2장 설정이 관리할지 불명 (2장 후행 고리에 "13장(워커 수)") | **`Settings`에 넣지 않는다** — uvicorn이 읽는 것은 접두사 없는 `$WEB_CONCURRENCY`이므로 `TRACKER_` 접두사와 충돌한다 |
| 8 | 9장 BFF의 `AsyncClient` 출처 불명 (4장 lifespan에 이미 있음) | 9장은 `app.state.http_client` **재사용**. 새로 만들지 않는다 (계획 9장이 "요청마다 만들지 말고 lifespan에서 재사용"이라 쓴 것과 일치) |
| 9 | 10장이 새 권한 예외를 만들지 3장 것을 쓸지 불명 | 3장의 `PermissionDeniedError` **재사용**. 예외 핸들러는 끝까지 3개 |
| 10 | N:M(이슈-라벨) 표현 방식 미정 — `Table(...)` 구문이 레퍼런스에 없음 | **association object 클래스** `IssueLabel` 기본형. 6장이 `relationship(secondary=)`를 1차 소스로 확인하면 각주와 함께 직접형 허용 |

**남은 판단(계약이 결정하지 않은 것 — 저술가 재량):** 각 장의 서술 순서·소절 구성·어떤 코드를 얼마나 실을지·대조 예시의 선택. 계약은 **이름과 구조만** 고정한다.
