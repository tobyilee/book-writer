# 버전 핀 원자료 (1차 소스 직접 조회)

**조회: 2026-07-25** — research-lead가 직접 수집. 하위 리서처의 서술이 아니라 기계 판독 가능한 1차 API 응답이 근거다.

## 수집 방법 (재현 가능)

- **PyPI JSON API**: `https://pypi.org/pypi/{package}/json` → `info.version`(최신 안정), `releases[version][0].upload_time_iso_8601`(업로드 시각), `info.requires_python`
- **python.org 릴리스 API**: `https://www.python.org/api/v2/downloads/release/?is_published=true&pre_release=false`
- **GitHub Releases API**: `https://api.github.com/repos/{owner}/{repo}/releases`
- **Docker Hub Tags API**: `https://hub.docker.com/v2/repositories/library/python/tags`
- **벤더 공식 문서**: AWS Lambda 런타임 표, Cloud Run 런타임 지원 표

> PyPI의 `upload_time`은 **PyPI 업로드 시각**이지 프로젝트가 공표한 릴리스 날짜와 하루 이틀 어긋날 수 있다. 책에서 "릴리스 날짜"로 단정하기보다 "{버전}/{연월} 기준"으로 쓰는 편이 안전하다.

---

## A. Python 인터프리터

출처: python.org 릴리스 API + endoflife.date/api/python.json (조회 2026-07-25)

| 계열 | 최신 패치 | 패치 릴리스일 | 계열 최초 릴리스 | EOL |
|---|---|---|---|---|
| 3.14 | 3.14.6 | 2026-06-10 | 2025-10-07 | 2030-10-31 |
| 3.13 | 3.13.14 | 2026-06-10 | 2024-10-07 | 2029-10-31 |
| 3.12 | 3.12.13 | 2026-03-03 | 2023-10-02 | 2028-10-31 |
| 3.11 | 3.11.15 | 2026-03-03 | 2022-10-24 | 2027-10-31 |
| 3.10 | 3.10.20 | 2026-03-03 | 2021-10-04 | **2026-10-31** |
| 3.9 | 3.9.25 | 2025-10-31 | 2020-10-05 | 2025-10-31 (EOL 지남) |

**책에 중요한 함의:**
- **3.14가 현재 최신 안정 계열**이다 ("{Python 3.14}/2026 기준").
- **3.10은 2026-10-31 EOL** — 이 책이 독자에게 읽힐 시점엔 이미 지원 종료다. FastAPI 0.140.0의 `requires_python`이 `>=3.10`이므로, 최소 지원선과 EOL이 거의 맞닿아 있다. 책은 **3.12+ 를 권장선**으로 잡는 게 안전하다.
- **3.15는 베타 진행 중** — Docker Hub에 `3.15.0b4`, `3.15-rc` 태그가 2026-07-22 갱신됨. 정식 릴리스는 2026-10 예정(관례). ⚠️ 정확한 3.15 GA 날짜는 별도 확인 필요.

## B. FastAPI 스택 코어

출처: PyPI JSON API (조회 2026-07-25)

| 구성요소 | 최신 안정 | PyPI 업로드일 | requires_python | 비고 |
|---|---|---|---|---|
| **fastapi** | **0.140.0** | **2026-07-24** | >=3.10 | 여전히 0.x. GitHub 릴리스 태그 `0.140.0` 2026-07-24 |
| **starlette** | **1.3.1** | **2026-06-12** | >=3.10 | ⭐ **1.0.0이 2026-03-22 릴리스** — 0.x 시대 종료 |
| **pydantic** | **2.13.4** | 2026-05-06 | >=3.9 | v2 계열 |
| pydantic-core | 2.47.0 | 2026-05-22 | >=3.10 | Rust 코어 |
| pydantic-settings | 2.14.2 | 2026-06-19 | >=3.10 | `BaseSettings`가 여기로 분리됨 |
| **anyio** | 4.14.2 | 2026-07-12 | >=3.10 | 스레드풀 오프로드의 실제 주체 |

### FastAPI 최근 릴리스 이력 (GitHub Releases, 조회 2026-07-25)

```
0.140.0  2026-07-24
0.139.2  2026-07-16
0.139.1  2026-07-16
0.139.0  2026-07-01
0.138.1  2026-06-25
0.138.0  2026-06-20
0.137.2  2026-06-18
0.137.1  2026-06-15
0.137.0  2026-06-14
0.136.3  2026-05-23
```
→ 릴리스 케이던스가 **월 3~5회**로 매우 빠르다. 책에서 마이너 버전을 못 박는 건 위험하고, "0.140/2026-07 기준"처럼 시점을 함께 적어야 한다.

### FastAPI 0.140.0 릴리스 노트 (GitHub, 전문 일부)

> ### Refactors
> * ⚡️ Reduce memory usage in dependencies. PR #16049 by @tiangolo.
> ### Docs
> * 📝 Update docs to use uv projects by default. PR #16032 by @tiangolo.
> * 📝 Add Library Skills documentation. PR #16041 by @tiangolo.
> ### Internal
> * 👷 Add CI memory benchmark. PR #16046 by @tiangolo.

**책에 중요한 함의:** 공식 문서가 **uv 프로젝트를 기본으로** 쓰도록 갱신됐다(PR #16032, 0.140.0/2026-07). CI/CD 장에서 uv를 1순위로 다룰 1차 근거다.

### FastAPI 저장소 메타 (GitHub API, 조회 2026-07-25)

- stars: 100,866 / open_issues: 87 / license: MIT / last push: 2026-07-24T21:16:20Z
- ⭐ **10만 스타 돌파**

### ⭐ Starlette 거버넌스 이전 (책의 서사로 쓸 만한 사실)

- `api.github.com/repos/encode/starlette` 조회 시 **`Kludex/starlette`로 리다이렉트**된다 (조회 2026-07-25). 즉 저장소가 encode 조직에서 **Marcelo Trylesinski(@Kludex) 개인/조직으로 이전**되었다. stars 12,497, archived: false.
- Starlette 버전 이력 (PyPI, 조회 2026-07-25):
  ```
  1.3.1   2026-06-12      1.0.1   2026-05-21
  1.3.0   2026-06-11      1.0.0   2026-03-22  ← 1.0 GA
  1.2.1   2026-05-31      1.0.0rc1 2026-02-23
  1.2.0   2026-05-28      0.52.1  2026-01-18
  1.1.0   2026-05-23      0.51.0  2026-01-10
                          0.50.0  2025-11-01
  ```
- **함의:** FastAPI(0.x)와 Starlette(1.x)의 버전 성숙도가 역전됐다. "FastAPI는 아직 0.x라 불안정하다"는 흔한 비판을 다룰 때 이 대비를 쓸 수 있다.
- ⚠️ **미확인**: 이전의 경위·시점·encode 조직의 공식 발표문은 확인하지 못했다. 책에서 배경을 서술하려면 추가 확인 필요.

## C. 서버 / 프로세스 매니저

| 구성요소 | 최신 안정 | PyPI 업로드일 | requires_python | 비고 |
|---|---|---|---|---|
| **uvicorn** | 0.51.0 | 2026-07-08 | >=3.10 | |
| **gunicorn** | **26.0.0** | 2026-05-05 | >=3.10 | 메이저 점프 (23.x → 26.x) |
| granian | 2.7.9 | 2026-07-03 | >=3.10 | Rust 기반 |
| hypercorn | 0.18.0 | 2025-11-08 | >=3.10 | |
| uvloop | 0.22.1 | 2025-10-16 | >=3.8.1 | |
| httptools | 0.8.0 | 2026-05-25 | >=3.9 | |

⚠️ gunicorn 26.0.0의 **breaking change 내역은 확인하지 못했다**. 책에서 gunicorn을 다룬다면 별도 확인 필요.

### FastAPI 공식 배포 권장 (docs 인용, 조회 2026-07-25)

출처: https://fastapi.tiangolo.com/deployment/server-workers/

- 비컨테이너: `fastapi run --workers 4 main.py` 또는 `uv run uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4`
- 컨테이너/K8s: 원문 인용 —
  > "when running on **Kubernetes** you will probably **not** want to use workers and instead run **a single Uvicorn process per container**"
- **이 페이지에 gunicorn + UvicornWorker 언급은 없다.** 공식 권장이 `fastapi run` CLI와 "컨테이너당 단일 프로세스 + 오케스트레이터 레플리카"로 옮겨간 것으로 보인다. 구식 블로그가 여전히 gunicorn+UvicornWorker를 권하는 것과 대비된다.

## D. 데이터 계층

| 구성요소 | 최신 안정 | PyPI 업로드일 | requires_python | 비고 |
|---|---|---|---|---|
| **SQLAlchemy** | **2.0.51** | 2026-06-15 | >=3.7 | 2.0 계열 유지 |
| **alembic** | 1.18.5 | 2026-06-25 | >=3.10 | |
| sqlmodel | **0.0.39** | 2026-06-25 | >=3.10 | ⚠️ 여전히 0.0.x — 성숙도 논쟁의 근거 |
| asyncpg | 0.31.0 | 2025-11-24 | >=3.9.0 | |
| psycopg | 3.3.4 | 2026-05-01 | >=3.10 | psycopg3 |
| aiosqlite | 0.22.1 | 2025-12-23 | >=3.9 | |
| redis | 8.0.1 | 2026-06-23 | >=3.10 | `redis.asyncio` 포함 |
| pymongo | 4.17.0 | 2026-04-20 | >=3.9 | async 지원 통합됨 |
| motor | 3.7.1 | **2025-05-14** | >=3.9 | ⚠️ 1년 이상 정체 — PyMongo async로 흡수되는 흐름인지 확인 필요 |

**함의:** SQLAlchemy는 **2.0 계열**이 안정적으로 유지되고 있다("SQLAlchemy 2.0/2026 기준"). SQLModel이 아직 **0.0.39**라는 사실은 "프로덕션에 쓸 것인가" 논쟁에서 중립적 근거로 인용할 수 있다.

## E. 테스트 / 품질 도구

| 구성요소 | 최신 안정 | PyPI 업로드일 | requires_python | 비고 |
|---|---|---|---|---|
| **httpx** | 0.28.1 | **2024-12-06** | >=3.8 | ⚠️ 1년 7개월째 정체 — TestClient의 기반 |
| **pytest** | **9.1.1** | 2026-06-19 | >=3.10 | 메이저 9.x |
| pytest-asyncio | 1.4.0 | 2026-05-26 | >=3.10 | 1.x — `asyncio_mode` 설정 주의 |
| **ruff** | 0.16.0 | 2026-07-23 | >=3.7 | 여전히 0.x |
| **mypy** | **2.3.0** | 2026-07-13 | >=3.10 | ⭐ 메이저 2.x 진입 |
| **uv** | 0.11.32 | 2026-07-23 | >=3.8 | 여전히 0.x, 릴리스 매우 잦음 |
| poetry | 2.4.1 | 2026-05-09 | >=3.10,<4.0 | |
| pip-tools | 7.6.0 | 2026-07-18 | >=3.9 | |

⚠️ **mypy 2.0 / pytest 9.0의 breaking change 내역은 확인하지 못했다.** 책에서 이 도구들의 설정을 다룬다면 각 프로젝트 CHANGELOG를 별도 확인해야 한다.

## F. 애플리케이션 스타일 관련 라이브러리

| 구성요소 | 최신 안정 | PyPI 업로드일 | 비고 |
|---|---|---|---|
| jinja2 | 3.1.6 | 2025-03-05 | SSR |
| sse-starlette | 3.4.6 | 2026-07-20 | SSE |
| strawberry-graphql | 0.323.2 | 2026-07-23 | GraphQL |
| python-multipart | 0.0.32 | 2026-06-04 | 파일 업로드 필수 의존 |
| celery | 5.6.3 | 2026-03-26 | 태스크 큐 |
| arq | 0.28.0 | 2026-04-16 | asyncio 네이티브 큐 |
| taskiq | 0.12.4 | 2026-05-08 | asyncio 네이티브 큐 |
| dramatiq | 2.2.0 | 2026-06-17 | |
| rq | 2.10.0 | 2026-06-20 | |
| orjson | 3.11.9 | 2026-05-06 | 빠른 JSON |

## G. 인증 / 보안 / 관측성

| 구성요소 | 최신 안정 | PyPI 업로드일 | 비고 |
|---|---|---|---|
| **PyJWT** | 2.13.0 | 2026-05-21 | 활발히 유지 |
| python-jose | 3.5.0 | **2025-05-28** | ⚠️ 1년 이상 정체 |
| **passlib** | **1.7.4** | **2020-10-08** | 🚨 **6년 가까이 릴리스 없음** — 사실상 방치. 구식 튜토리얼이 여전히 권장하는 대표 사례 |
| bcrypt | 5.0.0 | 2025-09-25 | passlib 없이 직접 쓰는 흐름 |
| argon2-cffi | 25.1.0 | 2025-06-03 | |
| structlog | 26.1.0 | 2026-06-06 | 구조적 로깅 |
| loguru | 0.7.3 | 2024-12-06 | |
| opentelemetry-instrumentation-fastapi | 0.65b0 | 2026-07-16 | ⚠️ 여전히 beta 표기 |
| prometheus-fastapi-instrumentator | 8.0.2 | 2026-06-23 | |

**🚨 책에 매우 중요:** **passlib 1.7.4는 2020-10-08이 마지막 릴리스다.** 그럼에도 수많은 FastAPI 튜토리얼(공식 문서 포함 여부는 확인 필요)이 `passlib[bcrypt]`를 권한다. 이건 "구식 블로그를 베낀 코드" 함정의 교과서적 사례이자, 보안 장에서 반드시 짚어야 할 지점이다.

## H. 비교 프레임워크

| 구성요소 | 최신 안정 | PyPI 업로드일 | requires_python |
|---|---|---|---|
| litestar | 2.24.0 | 2026-06-11 | >=3.8,<4.0 |
| django-ninja | 1.6.2 | 2026-03-18 | >=3.7 |
| flask | 3.1.3 | 2026-02-19 | >=3.9 |
| mangum | 0.21.0 | 2026-02-01 | >=3.9 |

## I. 배포 타깃

### 컨테이너 / 오케스트레이션

| 구성요소 | 버전 | 날짜 | 출처 |
|---|---|---|---|
| Docker Engine | 29.6.2 | 2026-07-16 | github.com/moby/moby releases |
| Kubernetes | **1.36.3** | 2026-07-23 | github.com/kubernetes/kubernetes releases |
| Kubernetes (차기) | 1.37.0-beta.0 | 2026-07-20 | 동일 |

**공식 `python` Docker 이미지 태그** (Docker Hub API, 조회 2026-07-25): 기본 배포판이 **Debian trixie**로 이동했다. `3.14.6-trixie`, `3.13.14-trixie`, `3.12.13-trixie`가 2026-07-21~22 갱신. `3.15.0b4-*`, `3.15-rc-*` 태그도 존재(베타). `-slim-trixie`, `-alpine3.24`/`-alpine3.23`, `-bookworm`(구 태그) 병존.

### AWS Lambda 지원 Python 런타임

출처: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html (조회 2026-07-25)

| 런타임 | 식별자 | OS | 폐기 예정일 |
|---|---|---|---|
| Python 3.14 | `python3.14` | Amazon Linux 2023 | 2029-06-30 |
| Python 3.13 | `python3.13` | Amazon Linux 2023 | 2029-06-30 |
| Python 3.12 | `python3.12` | Amazon Linux 2023 | 2028-10-31 |
| Python 3.11 | `python3.11` | Amazon Linux 2 | 2027-06-30 |
| Python 3.10 | `python3.10` | Amazon Linux 2 | **2026-10-31** |
| Python 3.9 | `python3.9` | Amazon Linux 2 | 2025-12-15 (폐기됨) |

- 공식 문서 인용: **"Python 3.15 — November 2026"** 이 차기 런타임 출시 목표로 명시돼 있다.
- Amazon Linux 2가 2026-06-30 EOL 예정이라 `python3.10`/`python3.11`이 AL2 기반으로 남아 있는 점이 명시돼 있다.
- 모든 지원 런타임이 x86_64와 arm64를 모두 지원한다.
- Lambda는 언어가 **LTS 단계**에 도달해야 관리형 런타임을 제공한다.

### Google Cloud Run 지원 Python (소스 기반/빌드팩 배포)

출처: https://docs.cloud.google.com/run/docs/runtime-support (조회 2026-07-25)

| 런타임 | ID | 스택 | 폐기 | 해체 |
|---|---|---|---|---|
| Python 3.14 | `python314` | google-24 (기본) | 2030-10-10 | 2031-04-10 |
| Python 3.13 | `python313` | google-22 (기본) | 2029-10-10 | 2030-04-10 |
| Python 3.12 | `python312` | google-22 (기본) | 2028-10-02 | 2029-04-02 |
| Python 3.11 | `python311` | google-22 (기본) | 2027-10-24 | 2028-04-24 |
| Python 3.10 | `python310` | google-22 (기본) | **2026-10-04** | 2027-04-04 |
| Python 3.9 | `python39` | google-18-full | 2025-10-05 | 2026-04-05 |

- 원문 인용: **"Container images deployed directly to Cloud Run are not subject to this policy."** → 컨테이너 이미지로 배포하면 Python 버전 제약이 없다. FastAPI를 컨테이너로 올리는 경우 이 표는 적용되지 않는다.

### ⚠️ 미확인 배포 타깃

- **Azure Container Apps** 지원 Python 버전 — 확인하지 못함
- **Fly.io / Railway / Render** 의 Python 런타임 정책 — 확인하지 못함
- Cloud Run의 최소 인스턴스/동시성 기본값 수치 — 확인하지 못함

---

## J. 직접 확인한 API·동작 사실 (fact-checker 대조용)

### anyio 기본 스레드 제한

출처: https://anyio.readthedocs.io/en/stable/threads.html (조회 2026-07-25). 원문 인용:

> "The default AnyIO worker thread limiter has a value of **40**, meaning that any calls to `to_thread.run_sync()` without an explicit `limiter` argument will cause a maximum of 40 threads to be spawned."

조정 API:
```python
to_thread.current_default_thread_limiter().total_tokens = 60
```

**이것이 FastAPI에서 `def`(비-async) 경로 함수의 동시 실행 상한이다.** anyio 4.14.2/2026 기준. 책에서 "동기 경로 함수는 스레드풀로 간다"고만 쓰지 말고 이 **40이라는 구체적 상한과 조정 방법**을 함께 제시해야 한다.

### lifespan vs on_event

출처: https://fastapi.tiangolo.com/advanced/events/ (조회 2026-07-25). 공식 문서 경고문 원문:

> "The recommended way to handle the *startup* and *shutdown* is using the `lifespan` parameter of the `FastAPI` app as described above. If you provide a `lifespan` parameter, `startup` and `shutdown` event handlers will no longer be called. It's all `lifespan` or all events, not both."

공식 lifespan 예제 (원문 그대로):
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

**보강 확인 (소스 레벨, 조회 2026-07-25):** 산문 문서는 "권장"이라고만 쓰지만, **소스 코드에는 `@deprecated` 데코레이터가 실제로 붙어 있다.** `fastapi/applications.py` (태그 0.140.0) 축자:

```
4648-    @deprecated(
4649-        """
4650:        on_event is deprecated, use lifespan event handlers instead.
```

→ **`on_event`는 deprecated가 확정 사실이다.** 단, FastAPI에서는 아직 *제거되지 않았고* `on_startup`/`on_shutdown` 파라미터도 남아 있다. 반면 **Starlette 1.0.0rc1에서는 완전히 제거**됐다(A조 확인). 책은 이 층위 차이를 정확히 써야 한다 — "FastAPI에서 제거됐다"고 쓰면 오류다.

`lifespan`과 `on_event`가 **배타적**이라는 점(둘 중 하나만 동작)도 확인됐다.

### FastAPI Labs / FastAPI Cloud

- 창시자 Sebastián Ramírez(@tiangolo)가 회사를 설립하고 **FastAPI Cloud**를 발표했다. 발표: **2025-05-05** (tiangolo X 게시물 https://x.com/tiangolo/status/1919410655922176040). 원문: "BIG NEWS ✨ I started a company with an amazing team and the best backers 🤓 We're building @FastAPIcloud 🚀 ... One command: fastapi deploy"
- ⚠️ 회사명(FastAPI Labs), 현재 서비스 상태(GA인지 waitlist인지), 오픈소스 스폰서십 구조는 **X/검색 요약에 의존한 것으로 1차 확인이 부족하다**. 커뮤니티 리서치 결과와 대조 필요.

---

---

## J-2. 추가 교차 검증 (A조 주장에 대한 research-lead의 독립 확인)

A조(`web.md`)가 소스 코드 레벨에서 낸 주장 중 **파급이 큰 3건을 내가 직접 재확인**했다. 셋 다 사실이다.

### ⭐ httpx → httpx2 전환은 사실이며, 주체는 **Pydantic 조직**이다

`https://pypi.org/pypi/httpx2/json` (조회 2026-07-25):

- name: `httpx2` / version: **2.9.1** / upload: **2026-07-24T09:21:02Z** / requires_python: `>=3.10`
- summary: **"The next generation HTTP client."**
- author_email: **Tom Christie <tom@tomchristie.com>** (httpx 원저자)
- project_urls: Homepage/Source = **`https://github.com/pydantic/httpx2`**
- 릴리스 케이던스: 2.1.0(2026-05-15) → 2.2.0(05-17) → 2.3.0(06-01) → 2.4.0(06-11) → 2.5.0(06-25) → 2.6.0/2.7.0(07-14) → 2.8.0/2.9.0(07-23) → 2.9.1(07-24)

Starlette 1.3.1 `testclient.py` 원문 (raw.githubusercontent.com/Kludex/starlette/1.3.1/…, 조회 2026-07-25):

```python
if TYPE_CHECKING:
    import httpx2 as httpx
else:
    try:
        import httpx2 as httpx
    except ModuleNotFoundError:  # pragma: no cover
        try:
            import httpx
        except ModuleNotFoundError:
            raise RuntimeError(
                "The starlette.testclient module requires the httpx2 package to be installed.\n"
                "You can install this with:\n"
                "    $ pip install httpx2\n"
            ) from None
        else:
            warnings.warn(
                "Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.",
                StarletteDeprecationWarning,
                stacklevel=2,
            )
```

**함의 (책의 큰 서사):** 구 `httpx`는 0.28.1(2024-12-06)에서 **1년 7개월째 멈춰 있고**, 후속이 `pydantic/httpx2`로 옮겨갔다. Starlette도 `Kludex/starlette`로, pydantic-core도 Pydantic 조직에. **FastAPI 스택의 핵심 의존성들이 2025~2026년에 걸쳐 관리 주체를 재편했다.** 테스트 장은 `httpx2`를 전제해야 하며, `pip install httpx`만 쓴 인터넷의 모든 예제는 `StarletteDeprecationWarning`을 낸다.

⚠️ **미확인**: httpx2가 httpx의 공식 후계로 공표된 경위·발표문, 구 httpx의 유지보수 정책은 확인하지 못했다.

**중요한 단서 (강도 조절):** `testclient.py`의 import 블록은 `try: import httpx2 / except ModuleNotFoundError: import httpx + DeprecationWarning` 구조다. 즉 **httpx2는 "권장"이지 "필수"가 아니다.** 구 httpx로도 여전히 동작하되 경고가 난다. 책에서 "httpx2가 필수"라고 쓰면 과장이다.

#### httpx2 실제 API 확인 (배포된 wheel 직접 해체, 조회 2026-07-25)

A조가 `⚠️ 미확인 #1`으로 남긴 "async 테스트 패턴이 httpx2에서도 같은 이름인가"를 **해소했다.** `httpx2-2.9.1-py3-none-any.whl`을 PyPI에서 받아 `__init__.py`의 `__all__`을 직접 읽었다.

**`__all__`에 실재하는 이름 (테스트 장 관련):**
```
ASGITransport, AsyncClient, AsyncBaseTransport, AsyncHTTPTransport,
WSGITransport, MockTransport, Client, Request, Response,
EventSource, ServerSentEvent, SSEError, websocket, alias_httpx
```

→ ✅ **`ASGITransport` + `AsyncClient` 패턴은 이름·구조 그대로 살아 있다.** 기존 async 테스트 코드의 import만 바꾸면 된다.

`ASGITransport` docstring 축자 (`httpx2/_transports/asgi.py`):
```python
class ASGITransport(AsyncBaseTransport):
    """
    A custom AsyncTransport that handles sending requests directly to an ASGI app.

    ```python
    transport = httpx2.ASGITransport(
        app=app,
        root_path="/submount",
        client=("1.2.3.4", 123)
    )
    client = httpx2.AsyncClient(transport=transport)
    ```

    Arguments:
        app: The ASGI application.
        raise_app_exceptions: Boolean indicating if exceptions in the application
            should be raised. Default to `True`. Can be set to `False` for use cases
            such as testing the content of a client 500 response.
        root_path: The root path on which the ASGI application should be mounted.
```

**⭐ httpx2가 새로 가진 것 (책에 쓸 가치가 큼):**

1. **네이티브 SSE 지원** — `EventSource`, `ServerSentEvent`, `SSEError`가 최상위 export. 모듈 `httpx2/_sse.py` 실재. 구 httpx에서는 `httpx-sse` 별도 패키지가 필요했다.
2. **네이티브 WebSocket 지원** — `httpx2/websockets/` 서브패키지 실재. `__init__.py` 축자:
   > """WebSocket support, derived from httpx-ws (https://github.com/frankie567/httpx-ws).
   > Copyright (c) 2021 François Voron, MIT License"""

   export: `ASGIWebSocketTransport`, `AsyncWebSocketClient`, `AsyncWebSocketSession`, `WebSocketClient`, `WebSocketSession`, `JSONMode`, `WebSocketDisconnect`, `WebSocketUpgradeError` 등. 즉 **httpx-ws가 본체로 흡수**됐다.
3. **`alias_httpx`** — 최상위 export. 이름으로 보아 `import httpx`를 httpx2로 해석시키는 마이그레이션 보조 장치로 보인다. ⚠️ 정확한 동작은 확인하지 못했다 — 책에 쓰려면 추가 확인 필요.

**책에 대한 함의:** 이 책의 테스트 장은 **WebSocket·SSE 엔드포인트 테스트를 별도 서드파티 없이** 다룰 수 있다. 3번 축(다양한 앱 스타일)과 5번 축(테스트)이 여기서 자연스럽게 만난다 — 실시간 기능을 다루는 장에서 "그래서 이걸 어떻게 테스트하나"에 바로 답할 수 있다는 뜻이다. 인터넷의 기존 자료는 대부분 `httpx-sse`·`httpx-ws`를 별도 설치하라고 안내하므로, 이것도 통념 교정 대상이다.

### ⭐ `Depends(..., scope=...)` 는 실재한다

`raw.githubusercontent.com/fastapi/fastapi/0.140.0/fastapi/param_functions.py` (조회 2026-07-25), `def Depends` 파라미터 추출:

```
dependency: Callable[..., Any] | None
use_cache:  bool
scope:      Literal["function", "request"] | None
```

→ A조가 인용한 `scope` 파라미터는 **실재 확인**. `yield` 의존성 정리 코드가 응답 전송 **전**(`"function"`)에 도는지 **후**(`"request"`)에 도는지를 고르는 스위치다. Spring의 `@Transactional` 경계 / OSIV 논쟁과 대응시켜 설명할 수 있는 지점.

### ⭐ 공식 보안 튜토리얼이 python-jose·passlib을 **버렸다**

출처: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ (조회 2026-07-25)

| 용도 | 공식 문서의 현재 지시 | 인터넷 튜토리얼 대다수 |
|---|---|---|
| JWT | `uv add pyjwt` → `import jwt` | `python-jose[cryptography]` |
| 비밀번호 해싱 | `uv add "pwdlib[argon2]"` → `from pwdlib import PasswordHash` | `passlib[bcrypt]` |

문서 축자:
> "pwdlib is a great Python package to handle password hashes. It supports many secure hashing algorithms and utilities to work with them. **The recommended algorithm is "Argon2"**."

> "pwdlib also supports the bcrypt hashing algorithm but does not include legacy algorithms — for working with outdated hashes, it is recommended to use the passlib library. For example, you could use it to read and verify passwords generated by another system (like Django) but hash any new passwords with a different algorithm like Argon2 or Bcrypt."

> "If you are planning to use digital signature algorithms like RSA or ECDSA, you should install the cryptography library dependency `pyjwt[crypto]`."

또한 **설치 명령이 `uv add`로 통일돼 있다** — FastAPI 0.140.0의 "Update docs to use uv projects by default"(PR #16032)와 일관된다.

관련 패키지 핀 (PyPI, 조회 2026-07-25):

| 패키지 | 버전 | 업로드일 | requires_python |
|---|---|---|---|
| **pwdlib** | 0.3.0 | 2025-10-25 | >=3.10 |
| **PyJWT** | 2.13.0 | 2026-05-21 | >=3.9 |
| cryptography | 49.0.0 | 2026-06-12 | >=3.9 |
| Authlib | 1.7.2 | 2026-05-06 | >=3.10 |
| fastapi-users | 15.0.5 | 2026-03-27 | >=3.10 |
| ~~python-jose~~ | 3.5.0 | 2025-05-28 | (정체) |
| ~~passlib~~ | 1.7.4 | **2020-10-08** | (사실상 방치) |

**책에 매우 중요:** 이건 "구식 블로그를 베낀 코드" 함정의 **교과서적 사례**다. 보안 장을 `PyJWT + pwdlib[argon2]`로 쓰고, 독자가 인터넷에서 볼 `python-jose + passlib` 예제가 왜 낡았는지를 명시적으로 설명해야 한다. Spring Security에서 넘어온 독자에게는 특히 중요하다 — 그들은 프레임워크가 정답을 정해주는 데 익숙하다.

---

## J-3. ASGI 스펙 1차 소스 (A조 공백 #1 해소)

A조가 `⚠️ 미확인 #1`로 "지시서 2번 축이 요구했는데 fetch하지 못했다"고 정직하게 남긴 항목을 **research-lead가 직접 채웠다.**

출처: `https://asgi.readthedocs.io/en/latest/specs/main.html`, `.../specs/www.html` (조회 2026-07-25)

### 스펙 버전

- **ASGI 스펙 버전: "Version: 3.0 (2019-03-20)"** — 축자. 즉 ASGI 3.0은 2019년 이후 안정적이며, 2026년에도 그대로다. **FastAPI 생태계가 격변하는 와중에 그 아래 프로토콜 계약은 7년째 안 변했다** — 책에서 쓸 만한 대비다.
- `scope["asgi"]["version"]` — 서버가 구현하는 ASGI 버전
- `scope["asgi"]["spec_version"]` — 프로토콜별 스펙 버전. HTTP/WebSocket의 경우 `"2.0"`, `"2.1"`, `"2.2"`, `"2.3"`, `"2.4"`, `"2.5"`

### 애플리케이션 콜러블 계약 (축자)

```
coroutine application(scope, receive, send)
```

- **`scope`**: "The connection scope information, a dictionary that contains at least a `type` key"
- **`receive`**: "an awaitable callable that will yield a new event dictionary when one is available"
- **`send`**: "an awaitable callable taking a single event dictionary as a positional argument"

개념 축자:
> The connection scope represents "a protocol connection to a user and survives until the connection closes."
> Events are "messages sent to the application as things happen on the connection, and messages sent back by the application to be received by the server, including data to be transmitted to the client."

### HTTP connection scope 키 (축자)

| 키 | 타입 | 설명 |
|---|---|---|
| `type` | Unicode string | `"http"` |
| `asgi["version"]` | Unicode string | ASGI 스펙 버전 |
| `asgi["spec_version"]` | Unicode string | `"2.0"`, `"2.1"`, `"2.2"` 등 |
| `http_version` | Unicode string | `"1.0"`, `"1.1"`, `"2"` 중 하나 |
| `method` | Unicode string | HTTP 메서드명, 대문자 |
| `scheme` | Unicode string | URL 스킴 (`"http"` 또는 `"https"`) |
| `path` | Unicode string | "HTTP request target excluding any query string, with percent-encoded sequences and UTF-8 byte sequences decoded" |
| `raw_path` | byte string | "The original HTTP path component, excluding any query string, unmodified from the bytes" |
| `query_string` | byte string | `?` 이후 부분, percent-encoded |
| `root_path` | Unicode string | "The root path this application is mounted at; same as `SCRIPT_NAME` in WSGI" |
| `headers` | Iterable[[byte string, byte string]] | "An iterable of `[name, value]` two-item iterables" |
| `client` | Iterable[Unicode string, int] | "[host, port], where host is the remote host's IPv4 or IPv6 address" |
| `server` | Iterable[Unicode string, Optional[int]] | "[host, port]" 또는 unix 소켓이면 "[path, None]" |
| `state` | Optional dict | "A copy of the namespace passed into the lifespan" |

### WebSocket connection scope

HTTP scope의 키를 **전부 포함**하고, 추가로:

| 키 | 타입 | 설명 |
|---|---|---|
| `subprotocols` | Iterable[Unicode string] | "Subprotocols the client advertised" |

**책에 대한 함의 (Java/Node 대조 축과 연결):**

- `root_path`가 **WSGI의 `SCRIPT_NAME`과 같다**는 스펙 축자는, 서브패스 마운트/리버스 프록시 뒤 배포를 설명할 때 정확한 근거가 된다. Spring의 `server.servlet.context-path`에 대응시킬 수 있다.
- `scope`/`receive`/`send` 3요소 계약은 **서블릿의 `HttpServletRequest`/`HttpServletResponse` 대신 무엇이 오는가**를 설명하는 정확한 출발점이다. 서블릿은 요청·응답을 객체로 주지만, ASGI는 **딕셔너리 + 두 개의 async 콜러블**로 준다. 미들웨어가 왜 그렇게 생겼는지가 여기서 나온다.
- `state`가 "lifespan에 전달된 네임스페이스의 복사본"이라는 점은 lifespan에서 만든 리소스(DB 풀 등)를 요청에서 꺼내 쓰는 공식 경로의 근거다.

⚠️ 남은 미확인: lifespan 프로토콜 스펙(`specs/lifespan.html`)은 별도로 fetch하지 않았다. `lifespan.startup`/`lifespan.shutdown` 이벤트 메시지의 정확한 구조를 인용하려면 추가 조사 필요.

---

## J-4. B조 공백 2건 해소 (research-lead 직접 확인, 2026-07-25)

### ⚠️→✅ `fastar>=0.9.0`의 정체 (B조 §7-2 항목 10-a)

B조가 "FastAPI 0.140.0의 `[standard]` extra에 새로 보이는데 정체를 모르겠다"고 남긴 항목이다. PyPI JSON API 조회 결과:

| 항목 | 값 |
|---|---|
| name | `fastar` |
| 최신 버전 | **0.11.0** (업로드 2026-04-13) |
| summary | **"High-level bindings for the Rust tar crate"** |
| requires_python | `>=3.8` |
| author_email | Jonathan Ehwald `<github@ehwald.info>` |
| repository | `https://github.com/DoctorJohn/fastar` |

README 축자: "The `fastar` library wraps the Rust [tar](https://crates.io/crates/tar) ..."

→ **Rust `tar` 크레이트의 Python 바인딩이다.** FastAPI의 `[standard]` extra가 tar 압축 라이브러리를 끌어온다는 뜻.

⚠️ **여기서 멈춰라.** FastAPI가 이걸 *왜* 필요로 하는지는 확인하지 못했다. `fastapi deploy`(FastAPI Cloud 업로드 시 프로젝트를 tar로 묶는 용도)와 관련됐으리라는 건 **그럴듯한 추론일 뿐 근거가 없다.** 책에 쓰려면 `fastapi-cli` 소스나 관련 PR을 확인해야 한다. 추론을 사실로 쓰지 말 것.

참고: 저자 Jonathan Ehwald(DoctorJohn)는 Strawberry GraphQL 메인테이너이기도 하다 — 다만 이 사실이 FastAPI 채택과 인과관계가 있는지는 **확인하지 않았다.**

FastAPI 0.140.0 `[standard]` extra 전체 구성 (B조 확인, PyPI `requires_dist`):
```
fastapi-cli[standard]>=0.0.8, fastar>=0.9.0, httpx<1.0.0,>=0.23.0,
jinja2>=3.1.5, python-multipart>=0.0.18, email-validator>=2.0.0,
uvicorn[standard]>=0.12.0, pydantic-settings>=2.0.0, pydantic-extra-types>=2.0.0
```
📌 주목: `[standard]`의 httpx 핀은 **`httpx<1.0.0,>=0.23.0`** 으로 **여전히 구 httpx**다. httpx2로 옮겨간 건 Starlette의 TestClient 쪽이고, FastAPI의 standard extra는 아직 httpx를 쓴다. **이 층위 차이를 책에서 뭉개면 안 된다.**

### ⚠️→✅ `SpooledTemporaryFile` 인메모리 임계값 = **1MB** (B조 §7-1 항목 1)

B조가 "FastAPI 문서는 'up to a maximum size limit'라고만 하고 숫자를 주지 않는다"며 남긴 항목. Starlette 소스에서 직접 확인했다.

`raw.githubusercontent.com/Kludex/starlette/1.3.1/starlette/formparsers.py` (조회 2026-07-25) 축자:

```python
147:        spool_max_size = 1024 * 1024  # 1MB
149:        max_part_size = 1024 * 1024   # 1MB
230:            tempfile = SpooledTemporaryFile(max_size=self.spool_max_size)
```

→ **`UploadFile`은 1MB를 넘는 순간 메모리에서 디스크로 스풀된다.** (Starlette 1.3.1/2026 기준)

같은 파일에서 확인된 관련 상한:
- `max_part_size: int = 1024 * 1024` (1MB) — 초과 시 `MultiPartException`. 에러 메시지 축자: `f"Part exceeded maximum size of {int(self.max_part_size / 1024)}KB."`
- 필드(비파일) 초과 시에도 동일 예외: `f"Field exceeded maximum size of {int(self.max_part_size / 1024)}KB."`

**책에 대한 함의:** "FastAPI는 업로드 파일을 메모리에 다 올린다"는 통념도, "항상 디스크에 쓴다"는 통념도 둘 다 틀렸다. **1MB가 분기점**이다. 그리고 `max_part_size` 기본 1MB는 **대용량 업로드 시 실제로 부딪히는 벽**이라 명시적으로 올려줘야 한다. Spring의 `spring.servlet.multipart.max-file-size`(기본 1MB)·`max-request-size`(기본 10MB)와 대조하기 좋은 지점이다 — 우연히 기본값이 같다.

### 📌 `python` 공식 이미지 기본 Debian suite (B조 §7-3 항목 24, 부분 해소)

Docker Hub Tags API(조회 2026-07-25) 관찰: 접미사 없는 태그 `3.14`, `3.13`, `3.13.14`와 `-trixie` 접미사 태그가 **같은 시각(2026-07-21~22)에 함께 갱신**된다. `-bookworm` 태그도 병존하나 별도 갱신된다.

→ 정황상 **기본 suite는 trixie**로 보인다. ⚠️ 다만 이는 태그 갱신 시각의 일치에서 **추론한 것**이지, 다이제스트를 대조하거나 공식 문서에서 확인한 것이 아니다. 책에 단정하려면 `docker manifest inspect`로 `3.14`와 `3.14-trixie`의 다이제스트 동일성을 확인해야 한다.

---

## K. 이 표를 쓸 때의 규칙

1. 책 본문에서 마이너 버전을 못 박지 마라. FastAPI는 **월 3~5회** 릴리스한다. `"FastAPI 0.140/2026-07 기준"`처럼 **시점을 동반**하라.
2. 계열 버전(`SQLAlchemy 2.0`, `Pydantic v2`, `Starlette 1.x`)은 안전하다. 패치 버전은 위험하다.
3. `requires_python` 하한은 그 자체로 서술 가치가 있다 — FastAPI가 `>=3.10`을 요구한다는 건 3.9 지원이 끝났다는 뜻이다.
4. ⚠️ 표시 항목은 fact-checker가 🕒(시점 확인 필요) 또는 ⚠️로 처리해야 하며, 확정 서술로 쓰면 안 된다.
