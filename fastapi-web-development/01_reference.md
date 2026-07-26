# FastAPI 웹 애플리케이션 개발 레퍼런스

**검색: 2026-07-25 기준**

- **주제:** FastAPI로 웹 애플리케이션을 개발하는 방법 (실무 중심 심층 해설)
- **대상 독자:** Java(Spring Boot)·Node.js(Express/NestJS)로 웹 앱을 개발해 본 경험이 있는 개발자. REST를 잘 알고 Python 기본 문법도 안다. **Python 입문·REST 입문은 이 책의 범위가 아니다.**
- **장르:** `tech-book`
- **원 산출물:** `research/web.md`(752줄) · `research/web_deploy.md`(1940줄) · `research/papers.md`(638줄) · `research/community.md`(1164줄) · `research/version_pins.md`(576줄) — **전부 보존. 삭제 금지.**

---

## 0. 이 문서를 읽는 법 (신뢰도 등급 규약)

Phase 4 `fact-checker`는 이 문서를 **1차 대조 근거**로 읽는다. 그래서 모든 주장에 신뢰도를 명시했다.

| 표기 | 뜻 | 저술가·계획가의 행동 |
|---|---|---|
| (표기 없음) | **원문을 직접 열어 확인**했다 | 그대로 써도 된다 |
| `(목록만 확인 — 원문 대조 필요)` | 검색 결과·이슈 목록에서만 봤다. **수치가 틀릴 수 있다** | 인용 전 원문을 열어라 |
| ⚠️ 미확인 | 찾지 못했다 | **단정하지 마라. 지어내지 마라** |
| 🕒 | 오래된 자료 (생태계 서술은 현재형 금지) | 감정·프레이밍만 인용 |
| ▶ 저자 해석 | 리서처의 해석이지 소스의 주장이 아니다 | 저자 의견으로 표시하고 쓰라 |

> **왜 이 규약이 필요한가 (실제 사고):** community-researcher가 1차 회차에서 GitHub 이슈 #9148의 upvote를 **56**으로 적었는데, 2차 회차에서 원문을 열어보니 **18**이었다. 검색 결과 목록에서 긁은 숫자였다. 같은 회차에 "논의조차 없다"는 서술도 틀린 것으로 판명됐다. **목록만 보고 적은 숫자는 믿지 마라.**

> **버전 규율:** 이 문서의 모든 버전은 2026-07-25에 PyPI JSON API·GitHub Releases·벤더 공식 문서를 **실제 조회**한 결과다. 기억으로 쓴 버전 번호는 하나도 없다. FastAPI는 **월 3~5회** 릴리스하므로, 본문에서 패치 버전을 못 박지 말고 `"{버전}/{연월} 기준"` 형식을 쓰라.

---

## 버전 핀 테이블

**전 항목 조회일 2026-07-25.** 근거는 PyPI JSON API(`https://pypi.org/pypi/{pkg}/json`)의 `info.version` + 해당 릴리스의 `upload_time_iso_8601`, GitHub Releases API, 그리고 벤더 공식 문서다.

> 📌 **행별 URL 규칙:** 아래 표 B~H의 모든 행은 **`https://pypi.org/pypi/{패키지명}/json`**(기계 판독 원본) 및 **`https://pypi.org/project/{패키지명}/{버전}/`**(사람이 읽는 릴리스 페이지)로 재현·검증할 수 있다. 이 템플릿이 각 행의 1차 출처이며, 별도 URL이 필요한 행(GitHub Releases·벤더 문서)만 개별 표기했다.

> ⚠️ **PyPI `upload_time`은 업로드 시각**이지 프로젝트가 공표한 릴리스 날짜와 하루 이틀 어긋날 수 있다. 또한 FastAPI는 **릴리스 노트 헤더 날짜와 GitHub `published_at`이 일부 릴리스에서 불일치**한다(예: 0.135.2는 헤더 2026-03-01 / API 2026-03-23). 책에서 날짜를 쓸 때 기준을 통일하라.

### A. Python 인터프리터

출처: `https://www.python.org/api/v2/downloads/release/` + `https://endoflife.date/api/python.json`

| 계열 | 최신 패치 | 패치일 | 계열 최초 릴리스 | EOL |
|---|---|---|---|---|
| **3.14** | **3.14.6** | 2026-06-10 | 2025-10-07 | 2030-10-31 |
| 3.13 | 3.13.14 | 2026-06-10 | 2024-10-07 | 2029-10-31 |
| 3.12 | 3.12.13 | 2026-03-03 | 2023-10-02 | 2028-10-31 |
| 3.11 | 3.11.15 | 2026-03-03 | 2022-10-24 | 2027-10-31 |
| 3.10 | 3.10.20 | 2026-03-03 | 2021-10-04 | **2026-10-31** |
| 3.9 | 3.9.25 | 2025-10-31 | 2020-10-05 | 2025-10-31 (EOL 지남) |

- **3.15는 베타 진행 중** — Docker Hub에 `3.15.0b4`·`3.15-rc` 태그가 2026-07-22 갱신됨. ⚠️ **정확한 GA 날짜는 미확인.**
- 📌 **책에 중요:** FastAPI가 `>=3.10`을 요구하는데 **3.10은 2026-10-31 EOL**이다. 최소 지원선과 EOL이 맞닿아 있으므로 책은 **3.12+ 를 권장선**으로 잡는 게 안전하다.

### B. FastAPI 스택 코어

| 구성요소 | 버전 | 릴리스일 | requires_python | 1차 출처 |
|---|---|---|---|---|
| **fastapi** | **0.140.0** | 2026-07-24 | `>=3.10` | https://github.com/fastapi/fastapi/releases/tag/0.140.0 |
| **starlette** | **1.3.1** | 2026-06-12 | `>=3.10` | https://pypi.org/project/starlette/1.3.1/ |
| **pydantic** | **2.13.4** | 2026-05-06 | `>=3.9` | https://pypi.org/project/pydantic/2.13.4/ |
| pydantic-core | 2.47.0 | 2026-05-22 | `>=3.10` | https://pypi.org/pypi/pydantic-core/json |
| pydantic-settings | 2.14.2 | 2026-06-19 | `>=3.10` | https://pypi.org/project/pydantic-settings/2.14.2/ |
| **anyio** | 4.14.2 | 2026-07-12 | `>=3.10` | https://pypi.org/project/anyio/4.14.2/ |

**⭐ Starlette 1.0 도달 — 이 책 시점의 가장 큰 구조 변화**

| 버전 | 날짜 |
|---|---|
| **1.0.0** | **2026-03-22** (창설 이래 첫 stable) |
| 1.0.0rc1 | 2026-02-23 |
| 0.52.0 | 2026-01-18 |
| 0.50.0 | 2025-11-01 |

- 저장소가 **`encode/starlette` → `Kludex/starlette`로 이전**됐다 (GitHub API가 리다이렉트로 응답. stars 12,497). uvicorn도 `Kludex/uvicorn`으로 이전.
- ▶ 저자 해석: **FastAPI(0.x)와 Starlette(1.x)의 버전 성숙도가 역전됐다.** "FastAPI는 아직 0.x라 불안정하다"는 비판을 다룰 때 이 대비가 쓸모 있다.
- ⚠️ **미확인:** 저장소 이전의 경위·공식 발표문은 확인하지 못했다.

### C. 서버 / 프로세스 매니저

| 구성요소 | 버전 | 릴리스일 | requires_python |
|---|---|---|---|
| **uvicorn** | 0.51.0 | 2026-07-08 | `>=3.10` |
| **gunicorn** | **26.0.0** | 2026-05-05 | `>=3.10` |
| granian | 2.7.9 | 2026-07-03 | `>=3.10` |
| hypercorn | 0.18.0 | 2025-11-08 | `>=3.10` |
| uvloop | 0.22.1 | 2025-10-16 | `>=3.8.1` |
| httptools | 0.8.0 | 2026-05-25 | `>=3.9` |
| websockets | 16.1.1 | 2026-07-17 | `>=3.10` |

⚠️ **gunicorn 26.0.0 / mypy 2.x / pytest 9.x의 breaking change 내역은 확인하지 못했다.** 설정을 다루려면 각 CHANGELOG를 별도 확인하라.

### D. 데이터 계층

| 구성요소 | 버전 | 릴리스일 | 비고 |
|---|---|---|---|
| **SQLAlchemy** | **2.0.51** | 2026-06-15 | 2.1은 2.1.0b3(2026-06-27)까지 **베타** |
| **alembic** | 1.18.5 | 2026-06-25 | |
| sqlmodel | **0.0.39** | 2026-06-25 | ⚠️ 여전히 `0.0.x` — 성숙도 논쟁의 중립 근거 |
| asyncpg | 0.31.0 | 2025-11-24 | |
| psycopg | 3.3.4 | 2026-05-01 | psycopg3 |
| aiosqlite | 0.22.1 | 2025-12-23 | |
| redis | 8.0.1 | 2026-06-23 | `redis.asyncio` 통합 (`aioredis`는 흡수됨) |
| pymongo | 4.17.0 | 2026-04-20 | async 지원 통합 |
| **motor** | 3.7.1 | **2025-05-14** | 🔴 **EOL 지남** (web_deploy §2-J) |
| beanie | 2.1.0 | 2026-03-26 | |

⚠️ **SQLAlchemy 2.1 GA 일정과 2.1에서 `Query` API가 실제 제거되는지는 미확인.**

### E. 테스트 / 품질 도구

| 구성요소 | 버전 | 릴리스일 | 비고 |
|---|---|---|---|
| **httpx2** | **2.9.1** | 2026-07-24 | ⭐ `pydantic/httpx2`. author: Tom Christie |
| httpx (구) | 0.28.1 | **2024-12-06** | 1년 7개월째 정체 |
| **pytest** | **9.1.1** | 2026-06-19 | 메이저 9.x |
| pytest-asyncio | 1.4.0 | 2026-05-26 | |
| **ruff** | 0.16.0 | 2026-07-23 | 여전히 0.x |
| **mypy** | **2.3.0** | 2026-07-13 | ⭐ 메이저 2.x |
| **uv** | 0.11.32 | 2026-07-23 | 여전히 0.x |
| ty | **0.0.63** | 2026-07-23 | Astral. 아직 `0.0.x` |
| pyrefly | 1.1.1 | 2026-06-18 | Meta. 이미 1.x |
| poetry | 2.4.1 | 2026-05-09 | |
| testcontainers | 4.15.0 | 2026-07-24 | |

📌 **신규 타입체커의 성숙도가 정반대다** — `ty`는 `0.0.x`, `pyrefly`는 이미 `1.x`. 뭉뚱그리지 마라.
⚠️ **ruff formatter가 공식적으로 "stable" 선언됐는지는 확인 실패.** "현재 stable 선언됨"이라고 쓰지 마라.

### F. 인증 / 보안 / 관측성

| 구성요소 | 버전 | 릴리스일 | 비고 |
|---|---|---|---|
| **PyJWT** | 2.13.0 | 2026-05-21 | ⭐ 공식 문서의 현재 선택 |
| **pwdlib** | 0.3.0 | 2025-10-25 | ⭐ 공식 문서의 현재 선택 |
| bcrypt | 5.0.0 | 2025-09-25 | |
| argon2-cffi | 25.1.0 | 2025-06-03 | |
| cryptography | 49.0.0 | 2026-06-12 | |
| Authlib | 1.7.2 | 2026-05-06 | |
| fastapi-users | 15.0.5 | 2026-03-27 | |
| ~~python-jose~~ | 3.5.0 | **2025-05-28** | 정체 |
| ~~passlib~~ | 1.7.4 | **2020-10-08** | 🚨 **5년 9개월간 릴리스 없음** |
| structlog | 26.1.0 | 2026-06-06 | |
| opentelemetry-api / sdk | 1.44.0 | 2026-07-16 | 안정 1.x |
| opentelemetry-instrumentation-fastapi | **0.65b0** | 2026-07-16 | ⚠️ 여전히 **베타 표기** |
| prometheus-fastapi-instrumentator | 8.0.2 | 2026-06-23 | |
| asgi-correlation-id | 5.0.1 | 2026-06-09 | |

### G. 앱 스타일 / 태스크 큐

| 구성요소 | 버전 | 릴리스일 | 비고 |
|---|---|---|---|
| jinja2 | 3.1.6 | 2025-03-05 | |
| sse-starlette | 3.4.6 | 2026-07-20 | FastAPI 0.135.0 내장 SSE와 역할 중복 |
| strawberry-graphql | 0.323.2 | 2026-07-23 | |
| ariadne | 1.1.0 | 2026-06-15 | |
| python-multipart | 0.0.32 | 2026-06-04 | 업로드 필수 의존 |
| celery | 5.6.3 | 2026-03-26 | |
| arq | 0.28.0 | 2026-04-16 | |
| taskiq | 0.12.4 | 2026-05-08 | |
| dramatiq | 2.2.0 | 2026-06-17 | |
| rq | 2.10.0 | 2026-06-20 | |
| **broadcaster** | 0.3.1 | **2024-08-01** | 🔴 **아카이브됨** — 그런데 공식 문서가 아직 링크 중 |
| orjson | 3.11.9 | 2026-05-06 | ⚠️ `ORJSONResponse`는 FastAPI에서 deprecated |

### H. 비교 프레임워크

| 구성요소 | 버전 | 릴리스일 |
|---|---|---|
| litestar | 2.24.0 | 2026-06-11 |
| django-ninja | 1.6.2 | 2026-03-18 |
| flask | 3.1.3 | 2026-02-19 |
| mangum | 0.21.0 | 2026-02-01 (`Kludex/mangum`) |

### I. 배포 타깃

| 구성요소 | 버전 | 날짜 | 출처 |
|---|---|---|---|
| Kubernetes | **1.36.3** | 2026-07-23 | github.com/kubernetes/kubernetes/releases |
| Docker Engine | 29.6.2 | 2026-07-16 | github.com/moby/moby/releases |
| aws-lambda-web-adapter | v1.0.1 | 2026-05-28 | `aws/aws-lambda-web-adapter` (`awslabs/`에서 이전) |

**공식 `python` Docker 이미지:** 기본 배포판이 **Debian trixie**로 이동했다. `3.14.6-trixie`·`3.13.14-trixie`가 2026-07-21~22 갱신. ⚠️ 다만 "trixie가 기본"은 태그 갱신 시각의 일치에서 **추론한 것**이지 다이제스트 대조로 확인하지 않았다.

**AWS Lambda 지원 Python 런타임** (https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html, 조회 2026-07-25)

| 런타임 | 식별자 | OS | 폐기 예정 |
|---|---|---|---|
| Python 3.14 | `python3.14` | AL2023 | 2029-06-30 |
| Python 3.13 | `python3.13` | AL2023 | 2029-06-30 |
| Python 3.12 | `python3.12` | AL2023 | 2028-10-31 |
| Python 3.11 | `python3.11` | AL2 | 2027-06-30 |
| Python 3.10 | `python3.10` | AL2 | **2026-10-31** |
| Python 3.9 | `python3.9` | AL2 | 2025-12-15 (폐기됨) |

- 공식 문서 축자: **"Python 3.15 – November 2026"** 이 차기 런타임 목표로 명시됨.
- 전 런타임이 x86_64·arm64 모두 지원. Lambda는 언어가 **LTS 단계**여야 관리형 런타임을 제공한다.

**Google Cloud Run 지원 Python** (https://docs.cloud.google.com/run/docs/runtime-support, 조회 2026-07-25)

| 런타임 | ID | 폐기 | 해체 |
|---|---|---|---|
| Python 3.14 | `python314` | 2030-10-10 | 2031-04-10 |
| Python 3.13 | `python313` | 2029-10-10 | 2030-04-10 |
| Python 3.12 | `python312` | 2028-10-02 | 2029-04-02 |
| Python 3.11 | `python311` | 2027-10-24 | 2028-04-24 |
| Python 3.10 | `python310` | **2026-10-04** | 2027-04-04 |

- 원문 축자: **"Container images deployed directly to Cloud Run are not subject to this policy."** → 컨테이너로 배포하면 Python 버전 제약이 없다.

⚠️ **미확인 배포 타깃:** Azure Container Apps 지원 Python 버전, Railway의 `PORT` 계약·헬스체크·scale-to-zero, Render의 scale-to-zero/spin-down, Fly.io가 생성하는 `fly.toml` 본문, Cloud Run "CPU always allocated"의 공식 문구(문서 404).

### J. FastAPI 0.140.0 `[standard]` extra 구성

PyPI `requires_dist` 조회 결과:
```
fastapi-cli[standard]>=0.0.8, fastar>=0.9.0, httpx<1.0.0,>=0.23.0,
jinja2>=3.1.5, python-multipart>=0.0.18, email-validator>=2.0.0,
uvicorn[standard]>=0.12.0, pydantic-settings>=2.0.0, pydantic-extra-types>=2.0.0
```

📌 **뭉개면 안 되는 층위 차이 2가지:**
1. **`[standard]`의 httpx 핀은 `httpx<1.0.0` — 즉 여전히 구 httpx다.** httpx2로 옮겨간 건 **Starlette의 TestClient**이지 FastAPI의 의존성이 아니다. "FastAPI가 httpx2로 갈아탔다"는 **틀린 서술**이다.
2. FastAPI는 `starlette>=0.46.0`으로만 핀한다 (**1.x를 강제하지 않는다**). 독자의 lock 파일에 0.4x가 있을 수도 1.x가 있을 수도 있다.

**`fastar`의 정체 (직접 조회):** `fastar` 0.11.0 (2026-04-13), summary **"High-level bindings for the Rust tar crate"**, author Jonathan Ehwald, repo `github.com/DoctorJohn/fastar`. ⚠️ **FastAPI가 이걸 왜 필요로 하는지는 확인하지 못했다.** `fastapi deploy`(FastAPI Cloud 업로드 시 프로젝트 tar 압축) 관련이라는 건 **그럴듯한 추론일 뿐 근거가 없다. 사실로 쓰지 마라.**

---

## 1. 개념과 정의

### 1-1. FastAPI는 무엇 위에 서 있는가

```
FastAPI (라우팅·검증·의존성·OpenAPI 생성)
  └─ Starlette 1.3.1 (ASGI 앱·라우팅·미들웨어·TestClient·WebSocket)
       └─ ASGI 3.0 명세 (scope / receive / send)
            └─ uvicorn 0.51.0 (ASGI 서버, uvloop·httptools 선택)
  └─ Pydantic 2.13.4 (검증·직렬화, Rust 코어 pydantic-core)
  └─ anyio 4.14.2 (스레드풀 오프로드의 실제 주체)
```

**⭐ ASGI 명세는 7년째 안 변했다.** 출처: https://asgi.readthedocs.io/en/latest/specs/main.html (조회 2026-07-25). 축자: **"Version: 3.0 (2019-03-20)"**. 그 위의 생태계가 격변하는 동안 아래 프로토콜 계약은 고정돼 있었다 — 책에서 쓸 만한 대비다.

**애플리케이션 콜러블 계약 (축자):**
```
coroutine application(scope, receive, send)
```
- `scope`: "The connection scope information, a dictionary that contains at least a `type` key"
- `receive`: "an awaitable callable that will yield a new event dictionary when one is available"
- `send`: "an awaitable callable taking a single event dictionary as a positional argument"

**HTTP connection scope 주요 키 (축자):** `type`("http") · `asgi["version"]` · `asgi["spec_version"]`("2.0"~"2.5") · `http_version`("1.0"/"1.1"/"2") · `method` · `scheme` · `path` · `raw_path` · `query_string` · `root_path` · `headers` · `client` · `server` · `state`("A copy of the namespace passed into the lifespan")

- `root_path` 축자: **"The root path this application is mounted at; same as `SCRIPT_NAME` in WSGI"** → Spring의 `server.servlet.context-path`에 대응시킬 수 있다.
- WebSocket scope는 HTTP의 키를 전부 포함하고 `subprotocols`("Subprotocols the client advertised")를 추가한다.

▶ **저자 해석:** `scope`/`receive`/`send` 3요소가 서블릿의 `HttpServletRequest`/`HttpServletResponse`를 대체한다. 서블릿은 요청·응답을 **객체**로 주지만 ASGI는 **딕셔너리 + 두 개의 async 콜러블**로 준다. 미들웨어가 왜 그렇게 생겼는지가 여기서 나온다.

⚠️ **미확인:** lifespan 프로토콜 명세(`specs/lifespan.html`)는 fetch하지 않았다. `lifespan.startup`/`lifespan.shutdown` 이벤트 메시지 구조를 인용하려면 추가 조사 필요.

### 1-2. 코어 API 시그니처 (0.140.0 태그 소스에서 AST 추출)

`FastAPI.__init__` 파라미터 (전체, 순서대로):
```
debug, routes, title, summary, description, version, openapi_url, openapi_tags,
servers, dependencies, default_response_class, redirect_slashes, docs_url, redoc_url,
swagger_ui_oauth2_redirect_url, swagger_ui_init_oauth, middleware, exception_handlers,
on_startup, on_shutdown, lifespan, terms_of_service, contact, license_info,
openapi_prefix, root_path, root_path_in_servers, responses, callbacks, webhooks,
deprecated, include_in_schema, swagger_ui_parameters, generate_unique_id_function,
separate_input_output_schemas, openapi_external_docs, strict_content_type
```

경로 데코레이터 (`@app.get`·`@app.post` 등은 파라미터가 **완전히 동일**):
```
path, response_model, status_code, tags, dependencies, summary, description,
response_description, responses, deprecated, operation_id,
response_model_include, response_model_exclude, response_model_by_alias,
response_model_exclude_unset, response_model_exclude_defaults, response_model_exclude_none,
include_in_schema, response_class, name, callbacks, openapi_extra,
generate_unique_id_function
```

`APIRouter.__init__`:
```
prefix, tags, dependencies, default_response_class, responses, callbacks, routes,
redirect_slashes, default, dependency_overrides_provider, route_class,
on_startup, on_shutdown, lifespan, deprecated, include_in_schema,
generate_unique_id_function, strict_content_type
```
⚠️ `FastAPI.include_router`와 `APIRouter.include_router`는 **파라미터 순서가 다르다.** 키워드 인자로만 쓰면 안전하다.

**파라미터 선언 함수 공통 인자** (`Path`·`Query`·`Header`·`Cookie`·`Body`·`Form`·`File` 전부 보유):
```
default, default_factory, alias, alias_priority, validation_alias, serialization_alias,
title, description, gt, ge, lt, le, min_length, max_length, pattern, regex,
discriminator, strict, multiple_of, allow_inf_nan, max_digits, decimal_places,
examples, example, openapi_examples, deprecated, include_in_schema, json_schema_extra
```
고유 인자: `Header`→`convert_underscores` / `Body`→`embed`,`media_type` / `Form`·`File`→`media_type`

**⭐ `Depends`에 `scope`가 생겼다** (`param_functions.py`, 0.140.0 — research-lead가 독립 재확인):
```python
def Depends(
    dependency: Callable[..., Any] | None = None,
    *,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any: ...
```
공식 문서 축자 (https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope):
> `"function"`: ... end the dependency after the *path operation function* ends, but **before** the response is sent back to the client.
> `"request"`: ... end **after** the response is sent back to the client.

▶ **저자 해석:** Spring의 `@Transactional` 경계 / OSIV(Open Session In View) 논쟁과 정확히 대응한다. 이 책의 대조 축에서 핵심 소재다.

**OpenAPI 버전 = 3.1.0** (`applications.py` 축자: `self.openapi_version ... = "3.1.0"`). 오버라이드 가능(`app.openapi_version = "3.0.2"`).

**`FastAPI.frontend()`** (0.138.0 신규, 시그니처 직접 확인): `frontend(path, directory, fallback="auto", check_dir=True) -> None` — SPA 빌드 서빙용.

### 1-3. 비동기 모델 — "40"이라는 숫자를 소스로 끝까지 추적했다

체인 전체가 1차 소스로 확인됐다:

1. **FastAPI** `routing.py:349-352`:
   ```python
   if is_coroutine:
       return await dependant.call(**values)
   else:
       return await run_in_threadpool(dependant.call, **values)
   ```
2. **Starlette** `concurrency.py` (태그 1.3.1):
   ```python
   async def run_in_threadpool(func, *args, **kwargs):
       func = functools.partial(func, *args, **kwargs)
       return await anyio.to_thread.run_sync(func)
   ```
   → `limiter`를 넘기지 않는다 = **기본 limiter 사용**
3. **anyio** `_backends/_asyncio.py` (태그 4.14.2): `CapacityLimiter(40)`
4. anyio 공식 문서 축자: **"The default AnyIO worker thread limiter has a value of 40, meaning that any calls to `to_thread.run_sync()` without an explicit `limiter` argument will cause a maximum of 40 threads to be spawned."**

> ✅ **기본 스레드풀 = 40. (anyio 4.14.2 / 2026 기준)** 조정: `anyio.to_thread.current_default_thread_limiter().total_tokens = N`

**sync `Depends`도 같은 풀을 공유한다** (`dependencies/utils.py:713-716`). 경로 함수 + 의존성이 **같은 40개를 함께 소진**한다는 게 실무 함정이다.

**sync `yield` 의존성의 정리 코드는 일부러 제한 밖에서 돈다** — `fastapi/concurrency.py` 주석 축자:
> `# blocking __exit__ from running waiting on a free thread` / `# can create race conditions/deadlocks if the context manager itself` / `# has its own internal pool (e.g. a database connection pool)` / `# to avoid this we let __exit__ run without a capacity limit`
```python
exit_limiter = CapacityLimiter(1)
```
▶ 저자 해석: "왜 프레임워크가 이렇게 생겼나"를 Spring 개발자에게 설명하기 좋은 소재다.

**uvicorn 동시성 플래그** (`main.py` 0.51.0에서 기본값까지 축자 확인):

| 플래그 | 기본값 | help 축자 |
|---|---|---|
| `--workers` | `None` | "Number of worker processes. Defaults to the $WEB_CONCURRENCY environment..." |
| `--loop` | `"auto"` | 선택지 `none/auto/asyncio/uvloop` |
| `--http` | `"auto"` | 선택지 `auto/h11/httptools` |
| `--limit-concurrency` | `None` | "Maximum number of concurrent connections or tasks to allow, before issuing HTTP 503 responses." |
| `--backlog` | `2048` | "Maximum number of connections to hold in backlog" |
| `--timeout-keep-alive` | `5` | |
| `--timeout-graceful-shutdown` | ⚠️ **문서에 Default 표기 없음** | |

📌 **`--limit-concurrency`가 backpressure의 정답이다** (503 반환). Spring의 스레드풀 큐 포화와 대조하기 좋다.

**free-threading (PEP 703) — 1차 소스로 확인된 것만:**
- PEP 703 "Making the GIL Optional in CPython" — status **Final**, python_version **3.13**
- PEP 779 "Criteria for supported status for free-threaded Python" — status **Final**, python_version **3.14**
- FastAPI 0.136.0 (2026-04-16): "Support free-threaded Python 3.14t" (PR #15149)
- ⚠️ **3.15+에서 free-threaded가 기본 빌드가 되는지, GIL 빌드 제거 로드맵은 미확인. 단정 금지.**
- ⚠️ **free-threading이 40-스레드 풀 모델을 실제로 얼마나 바꾸는지 1차 벤치마크 미확보.**

### 1-4. 업로드 처리의 실제 한계 (Starlette 소스 확인)

`starlette/formparsers.py` (태그 1.3.1) 축자:
```python
spool_max_size = 1024 * 1024   # 1MB
max_part_size  = 1024 * 1024   # 1MB
tempfile = SpooledTemporaryFile(max_size=self.spool_max_size)
```

→ **`UploadFile`은 1MB를 넘는 순간 메모리에서 디스크로 스풀된다.** "다 메모리에 올린다"도 "항상 디스크에 쓴다"도 둘 다 틀렸다. `max_part_size` 기본 1MB는 대용량 업로드에서 실제로 부딪히는 벽이므로 명시적으로 올려야 한다.

▶ 저자 해석: Spring의 `spring.servlet.multipart.max-file-size` 기본값도 1MB다. 우연히 같아서 대조하기 좋다.

### 1-5. 애플리케이션 스타일별 핵심 사실 (축 3)

> 상세는 `research/web_deploy.md` §1-A~§1-J. 아래는 **책의 서술을 좌우하는 사실만** 옮긴 것이다.

**WebSocket**
- uvicorn WS 프로토콜 선택지: `auto` / `none` / `websockets` / `websockets-sansio` / `wsproto` (`config.py`)
- `uvicorn[standard]`가 `websockets`를 설치한다. 기본 설치(`h11`+`click`)만으로는 WS가 안 된다.
- 다중 워커 팬아웃은 프레임워크가 풀어주지 않는다 → Redis pub/sub 등 외부 브로커 필요.
- 🔴 **`broadcaster`(0.3.1 / 2024-08-01)는 아카이브됐는데 FastAPI 공식 문서가 아직 링크한다.** ⚠️ encode 진영의 공식 대체재 안내는 **없다**.

**SSE — 🔴 FastAPI 0.135.0(2026-03-01)에 내장됐다**
- 인터넷 자료 대다수가 `sse-starlette` 설치를 안내한다. 이제 1차 선택지가 아니다.
- FastAPI 0.134.0에서 `yield` 기반 JSON Lines·바이너리 스트리밍이 추가되며 Starlette 하한이 `>=0.46.0`으로 올라갔다.
- ⚠️ 프록시 버퍼링은 여전히 함정이다(§5-C의 forwarded headers와 별개 문제).

**BackgroundTasks vs 태스크 큐**
- `BackgroundTasks`는 **같은 프로세스에서 응답 후 실행**된다 → 프로세스가 죽으면 사라진다.
- uvicorn은 종료 시 "wait for any background tasks to run to completion"을 보장하므로 **grace period 안에 끝나야 한다**.
- 실무 선택지: Celery 5.6.3 / arq 0.28.0 / Dramatiq 2.2.0 / RQ 2.10.0 / TaskIQ 0.12.4
- ⚠️ **Celery의 asyncio 네이티브 지원 여부에 대한 공식 진술은 확보하지 못했다.** 정황 근거만 있다 — concurrency 옵션 목록이 "prefork, Eventlet, gevent, thread, solo"로 **asyncio 풀이 없다.** "Celery는 async 네이티브가 아니다"를 공식 문장으로 뒷받침하지 못했으므로 단정 금지.
- ⚠️ Celery 문서("5.5.x runs on Python 3.8–3.13")와 PyPI 최신(5.6.3)이 불일치. 5.6.x 지원 범위 미확인.

**서버 렌더링 / SPA**
- `Jinja2Templates`(jinja2 3.1.6) + `StaticFiles`. ⚠️ `TemplateResponse` **인자 순서가 바뀌었다**(web_deploy §1-F) — 구식 예제 주의.
- **`app.frontend(path, directory, fallback="auto", check_dir=True)`** (0.138.0 신규) — SPA 빌드 서빙.
- ⚠️ `fasthx`·htmx의 FastAPI 전용 공식 가이드는 확인하지 못했다.

**GraphQL**
- 공식 문서 권장은 **Strawberry**(0.323.2). Ariadne 1.1.0도 존재.
- 🔴 **함정: Strawberry에서 `sync def` 리졸버는 워커 전체를 블록한다** (web_deploy §1-G).

**파일 업로드** — §1-4 참조 (1MB 스풀 임계, `max_part_size` 1MB 벽).

**마이크로서비스·BFF**
- 🔴 **httpx의 `retries`는 연결 실패만 재시도한다** — HTTP 5xx는 재시도하지 않는다. Spring Retry / Resilience4j를 기대하고 오면 반드시 틀린다.
- `AsyncClient`를 요청마다 만들지 말고 lifespan에서 만들어 재사용.
- ⚠️ pybreaker의 asyncio(비-Tornado) 지원은 미확인.

**REST 관례**
- OpenAPI **3.1.0** 고정. RFC 9457은 §3-4 참조(**미지원**).

### 1-6. 데이터 계층 (축 4) — SQLAlchemy 2.x 정확한 스타일

> **현재 안정판은 2.0.51.** 2.1은 `2.1.0b3`(2026-06-27) **베타**다 — 사이드바가 `beta release`로 표기하고 sqlalchemy.org가 `Current Documentation (version 2.0)` / `Version 2.1 (beta)`로 채널을 나눈다. **2.1을 프로덕션 권장으로 쓰지 마라.**

**공식 Quickstart (문서 원문 그대로):**
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
문서 축자:
> "**Changed in version 2.0:** The ORM Quickstart is updated for the latest PEP 484-aware features using new constructs including `mapped_column()`."
> "**Nullability derives from whether or not the `Optional[]` (or its equivalent) type modifier is used.**"

▶ **JPA 대비 결정적 차이:** nullable이 `@Column(nullable=false)`가 아니라 **타입 어노테이션의 `Optional[]` 유무**에서 파생된다.

**레거시로 강등된 것 (1차 소스 축자):**
> "The `Query` object (as well as the `BakedQuery` and `ShardedQuery` extensions) **become long term legacy objects**, replaced by the direct usage of the `select()` construct in conjunction with the `Session.execute()` method."
> "**Changed in version 2.0:** the `declarative_base()` function is **superseded by** the new `DeclarativeBase` class... **This allows an approach that is compatible with PEP 484 typing tools.**"

- `session.query(User).count()` → `session.scalar(select(func.count()).select_from(User))`
- 문자열 기반 `join("addresses")`·`joinedload("addresses")`는 **2.0에서 제거**됐다.

**`execute()` vs `scalars()` — 초보자가 가장 많이 헤매는 지점:**
> "it is typical to skip the generation of `Row` objects and instead receive ORM entities directly. This is most easily achieved by using the `Session.scalars()` method"

→ `session.execute(select(User))`는 **`Row` 튜플**을, `session.scalars(select(User))`는 **`User` 엔티티**를 준다.

**비동기 ORM과 `MissingGreenlet` (공식 정의 축자):**
> "A call to the async DBAPI was initiated outside the greenlet spawn context... **When using the ORM this is nearly always due to the use of lazy loading**, which is not directly supported under asyncio"

동시성 경고 축자:
> "**Warning:** A single instance of `AsyncSession` is not safe for use in multiple, concurrent tasks."
> "Using concurrent tasks with asyncio, with APIs such as `asyncio.gather()`... should use a separate `AsyncSession` per individual task."

**처방 4종 (전부 공식 문서):**
1. **`selectinload`** — "The most useful eager loading strategy": `select(A).options(selectinload(A.bs))`. 또는 `lazy="raise"`로 기본 차단
2. **`AsyncAttrs` / `awaitable_attrs`** (2.0.13+) — `for b1 in await a1.awaitable_attrs.bs:`
3. **`expire_on_commit=False`** — "Expiration should generally **not** be needed as `Session.expire_on_commit` should normally be set to `False` when using asyncio."
4. **`run_sync`** — 문서가 스스로 "Deep Alchemy"로 표시하고 *"the approach can probably be considered 'controversial'"*라고 인정한다

기타: greenlet 의존(`pip install sqlalchemy[asyncio]`, ⚠️ **Apple M1 포함 일부 플랫폼은 기본 미설치**) / `'dynamic'` 로더는 asyncio와 **기본 비호환** / `await engine.dispose()` 누락 시 `RuntimeError: Event loop is closed`

**드라이버·dialect URL (공식 문서 확인):**
```
postgresql+asyncpg://...        # "SQLAlchemy's first Python asyncio dialect"
postgresql+psycopg://...        # psycopg3 — sync/async 겸용 (같은 dialect 이름)
postgresql+psycopg2://...       # postgresql:// 의 기본
sqlite+aiosqlite:///myfile.db
mysql+asyncmy://... / mysql+aiomysql://...
```
- ⚠️ asyncpg 함정: "By default asyncpg does not decode the `json` and `jsonb` types and returns them as strings."
- ⚠️ asyncpg README의 **"5x faster than psycopg3"는 자체 측정이며 README가 "obtained ... in June 2023"이라고 명시한다.** 조건 없이 인용 금지.
- **aiomysql vs asyncmy에 우열을 단정하지 마라** — 둘 다 최근 1년 내 릴리스가 있고 공식 dialect 문서가 양쪽을 현재형으로 문서화하며 deprecation 표기가 없다.

**커넥션 풀 기본값 (SQLAlchemy 2.0.51 시그니처 직접 확인):**

| 파라미터 | 기본값 | 문서 축자 |
|---|---|---|
| `pool_size` | **5** | "**Note that the pool begins with no connections**" |
| `max_overflow` | **10** | "the total number of simultaneous connections the pool will allow is `pool_size` + `max_overflow`" |
| `pool_timeout` | **30.0** | |
| `pool_recycle` | **-1 (비활성)** | MySQL처럼 유휴 연결을 끊는 백엔드에 적합 |
| `pool_pre_ping` | **False** | "'ping' (typically 'SELECT 1')... to test if the connection is alive" |

> "All SQLAlchemy pool implementations have in common that **none of them 'pre create' connections**"

▶ **Spring/HikariCP의 `minimumIdle` 프리워밍에 익숙한 독자에게 중요한 차이.** 또 **기본 최대 동시 커넥션 = 5+10 = 15**이고 이게 **워커 수와 곱해진다** → DB `max_connections` 산정에 직결.

`pool_pre_ping`의 한계 (축자, 매우 중요):
> "**It is critical to note that the pre-ping approach does not accommodate for connections dropped in the middle of transactions or other SQL operations.**"

비동기 엔진 (축자):
> "The `QueuePool` class **is not compatible with asyncio**. When using `create_async_engine`... the **`AsyncAdaptedQueuePool`** class... is used instead."

**🔴 공식 SQL 튜토리얼의 반전:** FastAPI 공식 SQL 튜토리얼은 **SQLModel을 쓰고, 전부 동기(sync)다.** 축자: *"Here we'll see an example using SQLModel."* / *"You could use any other SQL or NoSQL database library you want... FastAPI doesn't force you to use anything. 😎"*
▶ **"FastAPI = async"라고 믿고 온 독자가 `MissingGreenlet`을 프로덕션에서야 처음 만나는 구조다.** 이 책의 데이터 장 훅으로 쓸 수 있다.

**Alembic**
- 🔴 **autogenerate가 컬럼 rename을 add+drop으로 처리한다 → 데이터 손실.** 반드시 생성된 마이그레이션을 읽어라.
- 비동기 엔진에서는 `env.py` 설정이 달라진다(web_deploy §2-F).

**NoSQL·캐시**
- redis 8.0.1 — `aioredis`는 **redis-py에 흡수**됐다. ⚠️ asyncio `ConnectionPool` 기본값은 미확인.
- 🔴 **MongoDB: Motor(3.7.1 / 2025-05-14)는 EOL을 지났다.** PyMongo 4.17.0의 async API로 가는 게 현재 경로다(web_deploy §2-J).

---

## 2. 핵심 관점들

### 2-1. "FastAPI는 빠르다"는 주장을 어떻게 다룰 것인가 — 공식 문서가 스스로 반박한다

이 책이 성능을 다루는 방식의 토대다.

- **FastAPI 공식 벤치마크 페이지가 스스로** FastAPI는 Starlette보다 "cannot be faster than"이라고 적는다 (web_deploy §3-L).
- **학술 문헌 상황 (papers.md §5-3):** TechEmpower류 웹 프레임워크 벤치마크의 **방법론을 검토·비판한 동료 심사 논문은 0건**이다 (DBLP `web framework benchmark comparison` 무수확).
- **그러나 벤치마크 방법론 일반의 엄밀한 문헌은 풍부하다** — 이게 이 책의 무기가 된다:
  - **Mytkowicz et al., "Producing Wrong Data Without Doing Anything Obviously Wrong!"** (ASPLOS 2009) — 측정 편향
  - **Georges et al., "Statistically Rigorous Java Performance Evaluation"** (OOPSLA 2007)
  - **van der Kouwe et al., "Benchmarking Crimes"** — ⚠️ **프리프린트(비심사)**. 22개 항목 체크리스트
  - **Dean & Barroso, "The Tail at Scale"** (CACM 2013) — 꼬리 레이턴시
  - **coordinated omission** — ⚠️ **원전(Gil Tene)은 동료 심사를 거치지 않았다.** 심사된 건 Friedrich et al.(BTW 2017)이 개념을 *적용한* 워크숍 논문 하나뿐. 인용 시 **"강연/비심사"로 표기**하라.

> **책의 전략 (papers.md 권고):** "TechEmpower가 이 범죄를 저질렀다"고 **단정하지 마라** — 학술 검토가 없으므로 그건 저자의 주장이다. **"이 렌즈로 보면 이런 질문을 하게 된다"**로 쓰라.

⚠️ FastAPI가 인용한 TechEmpower run의 라운드 번호·실행 시점은 확인 실패 (techempower.com이 JS SPA). **URL만 인용하고 라운드·날짜는 쓰지 마라.**

### 2-2. 학술 근거 지형 — 이 책이 어디서 엄밀할 수 있는가

papers.md §5-9 요약:

| 영역 | 학술 근거 | 전략 |
|---|---|---|
| 동시성 모델의 원리 | **강함** (다만 상당수 20년 전) | 원리는 인용, 수치는 조건과 함께 |
| 벤치마크 읽는 법 | **강함** | **이 책의 차별점.** 규율을 독자에게 이전 |
| 타입·스키마의 효과 | 중간~강함 (일부 JS 연구) | 반증도 함께 |
| 서버리스 콜드 스타트 | 강함 (다만 2018~2020) | 상대 구조만, 절대값은 연도와 함께 |
| **FastAPI 자체** | **없음 ❌** | 정직하게 밝히기 |
| **Python asyncio 실증** | **없음 ❌** | 1차 소스 + 커뮤니티, 출처 명시 |
| **웹 프레임워크 벤치마크 자체** | **없음 ❌** | 규율만 빌리고 단정 금지 |
| **ASGI·GIL·Pydantic 성능** | **없음 ❌** | 1차 소스, 버전 표기 필수 |
| **BFF 패턴** | 약함 | 업계 관행으로 정직하게 |

**핵심 고전 (동시성):**
- Welsh et al., **SEDA** (SOSP 2001)
- von Behren et al., **"Why Events Are A Bad Idea (for High-Concurrency Servers)"** (HotOS 2003) — 🕒 하드웨어 전제가 다르다는 걸 명시하라
- Adya et al., "Cooperative Task Management Without Manual Stack Management" (USENIX ATC 2002)
- Pai et al., **Flash** (USENIX ATC 1999)
- ⚠️ Ousterhout "Why Threads Are A Bad Idea" — **비심사 강연 자료**

**대체 전략 (papers.md §5-2):** Python asyncio 실증 연구가 없으므로 **Kotlin 코루틴 버그 연구(ECOOP 2024)를 프록시로** 쓰되, **"Python에는 이런 연구가 없어서 JVM 쪽을 참고했다"고 밝히고** 옮겨라.

### 2-3. 공식 권장이 이동했다 — 인터넷 자료 대다수가 낡았다

| 주제 | 흔한 통념 (구식 자료) | 2026-07-25 기준 사실 |
|---|---|---|
| JWT | `python-jose` | **`pyjwt`** (`uv add pyjwt` → `import jwt`) |
| 비밀번호 해싱 | `passlib[bcrypt]` | **`pwdlib[argon2]`** (`from pwdlib import PasswordHash`) |
| 프로덕션 실행 | `gunicorn -k uvicorn.workers.UvicornWorker` | `fastapi run --workers` / K8s는 **컨테이너당 1프로세스** |
| 의존성 관리 | pip / poetry | **uv** (공식 문서가 0.140.0에서 uv 기본으로 개편, PR #16032) |
| 성능용 JSON | `ORJSONResponse` | **deprecated** (0.131.0) — 0.130.0에서 Pydantic(Rust) 직렬화로 기본이 2배 이상 빨라짐 |
| SSE | `sse-starlette` 설치 | **FastAPI 0.135.0에 내장** |
| 테스트 HTTP | `httpx` | Starlette TestClient는 **`httpx2` 권장** (httpx도 동작하되 경고) |

**공식 보안 문서 축자** (https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/, 조회 2026-07-25):
> "pwdlib is a great Python package to handle password hashes... **The recommended algorithm is "Argon2"**."
> "pwdlib also supports the bcrypt hashing algorithm but does not include legacy algorithms — for working with outdated hashes, it is recommended to use the passlib library."
> "If you are planning to use digital signature algorithms like RSA or ECDSA, you should install ... `pyjwt[crypto]`."

📌 **`passlib` 마지막 릴리스는 2020-10-08** — 이건 검증된 사실이다. **"유지보수가 중단됐다"는 해석**이므로, 날짜라는 사실을 제시하고 해석은 따로 표시하라.

### 2-4. 프로세스 매니저 — 공식 문서 두 곳이 서로 다르다 (중요)

- **FastAPI 배포 문서** (`/deployment/server-workers/`): `fastapi run --workers 4 main.py` 또는 `uv run uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4`. **gunicorn 언급이 아예 없다.** 축자:
  > "when running on **Kubernetes** you will probably **not** want to use workers and instead run **a single Uvicorn process per container**"
- **Uvicorn 자체 문서**는 여전히 `gunicorn -k uvicorn.workers.UvicornWorker`로 **시작**한 뒤 하단에서 경고한다 (web_deploy §5-A).

▶ **저자 해석:** 이 불일치 자체가 책에 쓸 소재다. 독자가 두 공식 문서를 보고 다른 결론에 도달할 수 있다.

---

## 3. 대표 사례

### 3-1. 2026년 상반기 파괴적 변경 전수 (릴리스 노트 헤더 날짜 기준)

| 버전 | 날짜 | 변경 |
|---|---|---|
| 0.125.0 | 2025-12-17 | Drop Python 3.8 |
| 0.126.0 | 2025-12-20 | Pydantic v1 지원 중단, `pydantic>=2.7.0` |
| 0.127.0 | 2025-12-21 | `pydantic.v1` deprecation 경고 |
| **0.128.0** | **2025-12-27** | **`pydantic.v1` 지원 완전 제거** |
| 0.129.0 | 2026-02-12 | Drop Python 3.9 |
| 0.130.0 | 2026-02-22 | Pydantic(Rust) JSON 직렬화 — 축자 *"2x (or more) performance increase for JSON responses"* |
| 0.131.0 | 2026-02-22 | `ORJSONResponse`·`UJSONResponse` deprecated |
| **0.132.0** | 2026-02-23 | **`strict_content_type` 기본 True** (CSRF 방어) |
| 0.133.0 | 2026-02-24 | Starlette 1.0.0+ 지원 |
| 0.135.0 | 2026-03-01 | **SSE 정식 지원** |
| 0.136.0 | 2026-04-16 | free-threaded Python 3.14t 지원 |
| **0.137.0** | **2026-06-14** | **라우터 내부 구조를 트리로 변경** |
| 0.138.0 | 2026-06-20 | `app.frontend()` |
| 0.140.0 | 2026-07-24 | 의존성 메모리 사용량 감소 |

**`strict_content_type` 축자 (0.132.0 릴리스 노트):**
> "Now FastAPI checks, by default, that JSON requests have a `Content-Type` header with a valid JSON value, like `application/json`, and rejects requests that don't. If the clients for your app don't send a valid `Content-Type` header you can disable this with `strict_content_type=False`."

**0.137.0 라우터 트리 변경 축자:**
> "Now `router.routes` is no longer a plain list of `APIRoute` objects, it can contain these intermediate objects that can contain additional routers, forming a tree.
> Any logic that depended on iterating on the `router.routes` directly would be affected..."

대체 API (`routing.py:1821`): `def iter_route_contexts(routes: Sequence[BaseRoute | RouteContext]) -> Iterator[RouteContext]`

### 3-2. ⭐ 그 변경이 실제로 생태계를 깨뜨린 기록

`trallnag/prometheus-fastapi-instrumentator` 이슈 3건이 **2026년 6~7월에 연달아** 터졌다:

| 이슈 | 날짜 | 내용 |
|---|---|---|
| #370 | 2026-06-14 | `AttributeError: '_IncludedRouter' object has no attribute 'path'`. 보고자 환경: `prometheus-fastapi-instrumentator==7.1.0`, `fastapi==0.137.0`, `starlette==0.52.1`. PR #371로 수정 |
| #379 | 2026-06-25 | "Incompatible with certain router usage in FastAPI 0.137.0+" |
| #388 | 2026-07-08 | "Issue with FastAPI 0.138" — **고쳤는데 다음 마이너에서 또 터졌다** |

⚠️ **위 버전 번호는 이슈 본문에 보고자가 적은 환경 정보다.** "FastAPI 0.137.0에서 무엇이 바뀌었는가"는 릴리스 노트로 대조하라. 커뮤니티 이슈는 **"깨졌다는 사실"의 근거이지 "무엇이 어떻게 바뀌었는지"의 근거가 아니다.**

▶ **저자 해석 (양면을 함께 써야 정확하다):** Spring Boot의 "메이저 아니면 안 깬다" 계약에 익숙한 독자에게는 이게 가장 낯선 지점이다. **나쁜 쪽** — 마이너가 생태계를 깨고, 고쳐도 3주 뒤 또 깨진다. **좋은 쪽** — 아래 3-3처럼 커뮤니티 고통이 API로 흡수되기도 한다. 어느 한쪽만 보여주면 부정확하다.

### 3-3. 🚨 뉘앙스 주의 — `Depends(scope=)`가 #11107을 해결했는지는 **확인되지 않았다**

- 이슈 #11107(2024-02): `yield` 의존성 정리 순서가 뒤집혀 **커밋 전에 세션이 닫히는** 문제. 이슈 #11143으로 승격, 확인 시점 **Closed**.
- ⚠️ **#11143의 종결 사유·병합 PR은 확인하지 못했다** `(확인 필요 — 종결 사유 미확인)`.
- 확보된 사실: #14137(2025-10)에서 tiangolo가 제시한 처방이 `Depends(func, scope="function")`이었다.
- 🚨 **"`scope` 파라미터가 #11107을 해결했다"로 반올림하지 마라.** 성립할 가능성은 높지만 **릴리스 노트로 확인하기 전에는 미확정**이다.

### 3-4. 🚨 뉘앙스 주의 — RFC 9457 Problem Details의 정확한 상태

Spring Boot 3의 `ProblemDetail`을 아는 독자에게 직결되는 7년짜리 아크다.

| 항목 | 날짜 | 내용 |
|---|---|---|
| issue #512 "Support RFC 7807 error handling" | 2019-09-07 | tiangolo(2020-06-10): *"I haven't wanted to do it as it would break backwards compatibility, but maybe in the future, I end up doing it 🤷 🤓"* |
| Discussion #14517 "RFC 9457 Based Error Responses" | 2025-12-13 (upvote 6) | *"This is a breaking change and therefore should be opt in"* |
| 같은 스레드, yakubka | 2026-07-05 | *"**FastAPI does not implement this automatically**, but you can wire it up with a custom exception class and handler."* |
| **PR #15951** | **2026-07-07 제출, 같은 날 미머지 close** | 🚨 **기술적 반려가 아니라 프로세스 사유** |

**PR #15951을 닫은 사유 축자 (YuriiMotov, 2026-07-07):**
> "let's keep it closed until maintainers can review the discussion and decide that we are going to add this feature... We are trying to keep things clean and ask to open PRs only when it's explicitly requested by maintainers."

(PR 본문에 저자가 AI 생성임을 명시 — *"AI Disclaimer"*)

> 🚨 **책에 쓸 정확한 표현:** 2026-07-25 현재 FastAPI 코어에 RFC 9457 지원은 **없다.** 2019→2025→2026으로 **7년째 열려 있는 요청**이다. **"지원한다"도 "거절됐다"도 둘 다 틀린다.**

### 3-5. 422 검증 에러 — 자동 문서가 커스터마이징을 막는 아이러니

**정전 스레드: issue #643** "Why status 422 instead of 400...?" (yiannis-kt, 2019-10-22)

tiangolo 답변 축자 (2019-10-30):
> "The rationale is that the error is not about using the protocols and languages incorrectly (HTTP, JSON) nor about doing something otherwise not allowed... but about **sending invalid contents, even though using the correct content format (JSON) through the correct channel (valid HTTP)**... The second reason is that **Flask-apispec with Marshmallow used 422 too**... And the other advantage is that you can then **separate a whole class of errors, validation errors, that are created automatically**..."

정면 반박 — antonagestam (2022-02-08):
> "the format here is not simply JSON, but a rich OpenAPI schema. I see no reason why violating that schema, which is clearly the contract for interacting with the API, is not a client error..."

절충 — Jaza (2022-12-06): 구문 오류는 400, 의미 오류는 422로 나누자.

**진짜 실무 고통은 상태 코드가 아니라 문서다** — issue #1376 "Allow customization of validation error" (johanfleury, 2020-05-04, 리액션 15)가 5년짜리 우회법 전시장이 됐다:
- yusra-haider (2019-10-31): *"**auto-generated documentation doesn't reflect the updated status code**"*
- PhilippeGalvan (2020-09-03): *"fastapi is really nice and I'm trying to convince a client to use it and **auto-doc is a key argument!**"*
- akrejczinger (2020-06-09): *"HTTP 422 is hardcoded in openapi/utils.py. **I solved my issue for now by modifying the FastAPI source code itself**"*
- ushu (2021-01-07): `validation_error_response_definition`을 **모듈 전역 변수째 덮어쓰기**
- Acerinth (2021-04-28): Pydantic 모델 재정의 + 예외 핸들러 + `custom_openapi()` **3단 조합**
- Kludex (2020-09-02): *"The solution that would require less work... is creating a flag to not add the 422 response in the swagger documentation."*

▶ **저자 해석:** FastAPI의 최대 셀링 포인트(자동 문서)가 커스터마이징의 최대 장벽이라는 게 이 절의 핵심 아이러니다.

⚠️ `validation_error_response_definition`이 아직 그 위치에 하드코딩돼 있는지는 **커뮤니티 진술이므로 현행 소스 대조 필수.**

### 3-6. Java 배경 개발자가 Pydantic을 만났을 때 (실제 발언)

**★ 오프닝 재료 — hiram112 (HN, 2021-12-04):**
> "Funny, I took over a modern python service and I was pretty shocked at what I inherited. Long gone are the days of 'There's one way to do things'. Instead, **this thing would give the most 'enterprisey' Spring JEE application a run for its money with its endless annotations, dependency injection magic, all sorts of pseudo-types**... **But unlike Java, these types aren't even really guaranteed by the language at compile time**, so even if your IDE plugin can successfully detect them, things will still (silently) slip through at runtime."

바로 달린 반박:
> "This sounds like what happens when **a bunch of Java/C# developers jump over to python without learning the 'python way'** — this is more related to the developers than the project"

🕒 2021년 글. **생태계 서술이 아니라 인지 충돌의 기록으로만 써라.** ▶ 이 반박 쌍 자체가 이 책의 존재 이유다.

**JSR-380을 직접 거론한 유일한 발언** — duncanfwalker (HN, 2025-07-27):
> "Validation rules are like an extension to the type system... **In Java they got around the external-dependency-in-the-core-model problem by making the JSR-380 specification that could (even if only in theory) have multiple implementations.**... **It's these kind of pragmatic compromises that distinguish Python from Java - after all, 'worse is better'.**"

**⭐ 통념이 뒤집히는 지점** — 같은 스레드(2025-07-23, 94점/121댓글):
- **microflash (2025-07-26), Java 측:** *"For many cases, we don't do these kind of things in Java; **a single annotated record can function as a model for both data and API layers.**"*
- **반면 Python 진영의 다수설은 "분리하라"** — globular-toast (HN, 2025-08-07): *"Am I the only one who prefers to just have separate models for API and database right from the start? ... Your API and your database schema are not the same thing."*
- IshKebab: *"This seems ridiculously over-complicated. **This guy would love Java.**"* / throwaway7783: *"Return of Java DTOs!"*
- zo1: *"it **immediately sets your type system to go down the path of Java and Typescript**... This is not the python way"*
- rtpg (한계를 가장 정확히): *"Pydantic for me is like '**you can validate a straightforward data structure! Now it's up to you to actually build up a useful data structure from the straightforward one**'"*

▶ **저자 해석:** "Java는 계층을 나누고 Python은 간단히 간다"는 통념과 **정반대**다. 챕터 소재로 강력하다.

### 3-7. Node/Express 개발자 시점의 직접 비교

**com2kid (HN 44816140, 2025-08-06):**
> "The difference with the Express ecosystem is that you aren't getting any less power than with FastAPI or Spring Boot, you just get less overhead. **Spring Boot has 10x the config to get the same endpoint up and running as Express, and FastAPI has at least 3x the magic.**"
> "having one really damn simple and easy to understand building block is more powerful than having 500 blocks that can be misconfigured in ten thousand different ways."

▶ **축이 두 개라는 걸 정확히 짚었다: Spring Boot = 설정량, FastAPI = 마법량.** 책의 프레이밍으로 쓸 만하다.

같은 댓글: Node는 *"The scaling story of Node is also really easy to think about and do capacity planning for"* — **확장 단위가 그냥 프로세스 하나**다. FastAPI에서는 그게 워커 수·스레드풀 상한·OS 스케줄러가 얽힌 결정이 된다.

※ 인용문은 Algolia 코멘트 인덱스 취득 텍스트. 작성자·날짜는 개별 item 페치로 확인. **글자 그대로 인용하려면 원문 대조.**

### 3-8. DI 컨테이너 부재를 "말"이 아니라 "유물"로 증명하기

- **dishka**의 6대 한계 중 4번 축자:
  > "You have to declare each dependency with `Depends` on each level of application. So either your business logic contains details of IoC-container or you have to duplicate constructor signatures."
  - 비교표: FastAPI Depends는 **자동 와이어링 ❌, 컨텍스트 데이터 ❌, 동시성 안전성 ➖**
  - dishka 자기 규정: *"many frameworks either lack scopes completely or offer only two"*
  - ▶ "DI 컨테이너가 없다"의 정확한 의미는 **자동 와이어링(auto-wiring)이 없다**는 것이다.
- **GitHub #8054**: 내장 캐싱은 **단일 요청 안에서만** 유효(dmontagu). 커뮤니티가 5년에 걸쳐 우회법을 쌓았다 — `lru_cache` → startup 인스턴스화 → `app.state` → `AsyncExitStack`+app state. **2026년 현재까지 Unanswered.**
- **FastNest** (Dev.to, Hamza El Mouddane, **2026-04-28**): NestJS 개발자가 그리워하는 것 목록 = `@Module` 시스템 / **DI 컨테이너** / 이벤트 데코레이터 WebSocket / **Guards, Interceptors, Pipes**
  - ⚠️ **단일 저자 프로젝트다. 커뮤니티 합의가 아니다.** 다만 "2026년에도 누군가 이걸 만들 필요를 느꼈다"는 사실 자체가 데이터다.
- **rmonvfer (HN 44818249, 2025-08-06)** — Litestar 문서를 읽다가: *"reading the litestar docs, **it even has a built-in event system!** I spent a couple weeks building something I could use with FastAPI..."*

**반론 — Python 진영의 "우린 그거 필요 없다"** (`python-dependency-injector` 공식 문서 "DI in Python", ⚠️ 게시일 미확인):
> "Originally dependency injection pattern got popular in languages with static typing like Java."
> "There is an opinion that dependency injection doesn't work for it as well as it does for Java. A lot of the flexibility is already built-in."
> "Python developers say that dependency injection can be implemented easily using language fundamentals."

▶ **⭐ 이 책의 핵심 역설:** **Spring 개발자는 `Depends`가 마법이 부족해서 불만이고, Python 개발자는 `Depends`가 마법이 과해서 불만이다.** (후자는 Lobsters linkdd: `Depends`의 암묵적 마법이 "Explicit is better than implicit"에 어긋난다)

### 3-9. 보안을 직접 조립하는 비용

**antoinewdg (Lobsters, Django vs FastAPI 스레드, ≈2025):**
> "One thing that is IMO missing from the comparison is security. **I generally prefer the 'build it yourself' approach, but not for security.** Django comes with a lot of security stuff enabled by default... user management comes built it with password hashing and **automatic upgrade of old hashes on login**. I would probably think about doing the first in a hand made solution and maybe implement it properly, **definitely not the latter.**"

⚠️ **발언 대상이 FastAPI가 아니라 Django 비교다.** "Spring Security 경험자가 FastAPI에서 이렇게 말했다"로 **왜곡하지 마라.** "마이크로 프레임워크에서 보안을 직접 조립하는 것에 대한 실무자 불안"으로만 써라.

**조립 비용의 실증:** python-jose/passlib 방치 사건 — 신고에서 공식 문서 변경까지 **1년/15개월**이 걸렸다 (community §2-5, 스레드 4건).

### 3-10. 한국 개발자의 증언 (1차 증언은 velog 3건 + shipfriend 1건이 전부다)

- **velog, JUNYOUNG "[Spring][FastAPI] FastAPI에서 Spring으로 마이그레이션하며 배운 점"** (2025-03-07):
  > "FastAPI는 빠른 개발과 간결한 구조가 강점이었지만, 복잡한 비즈니스 로직을 다루고 대규모 트래픽을 처리하는 데는 Spring이 더 적합했다."
  - ▶ **반전:** 글의 실제 본문은 **JPA 삽질**(Fetch Join, 네이티브 쿼리, 엔티티 상속, DTYPE)에 집중돼 있다. **Spring으로 갔는데도 N+1과 연관관계 문제를 다시 겪었다.** → **N+1은 프레임워크 문제가 아니라 ORM의 문제**라는 좋은 반증 소재.
- **velog, 고은연 "FastAPI 써 본 후기"** (2022-01-07): *"ORM 연동이 너무 불편하고, 다수의 데이터베이스 서버 연동이나 entity와 repository manager 방식 사용이 어렵다"* — **entity/repository 어휘를 그대로 쓴다.** FastAPI를 "스프링 부트의 파이썬 버전"으로 평가하고 결국 Flask·AWS Chalice로 돌아갔다. 🕒 2022년 글, **감정과 프레이밍만.**
- **shipfriend.dev, 서정우 "FastAPI는 왜 사용하는 걸까? 강점과 약점"** (2026-03-28): *"비동기를 지원하지 않는 라이브러리를 함께 사용하는 순간 비동기의 이점이 사라진다"*
- **카카오페이 기술블로그** "이미지 처리를 위한 파이썬 서버 프레임워크 선정기" (2022-08-29) — 🕒 4년 경과. **방법론·결론만 인용하고 버전 정보는 쓰지 마라.**

---

## 4. 논쟁점·상충 관점

> 🚨 **표집 편향 경고 (반드시 읽어라).** 이 절의 상당 부분이 **HN 44816755 단일 스레드**에서 나왔고, 그 스레드는 *"Litestar를 봐라"*는 글의 댓글이다 — **FastAPI를 떠나는 사람이 과대표집된 표본**이다.
> 또한 2차 회차에서 수집한 async 비판 자료가 **"async는 과대평가됐다"는 논조의 스레드들**(HN 45106189, 47859442, 48281515, Lobsters oa1vf8)에 집중돼 있어 **async 옹호 측이 과소표집**된다.
> **"커뮤니티는 async에 회의적이다"로 일반화하지 마라 — 표본이 그렇게 뽑혔을 뿐이다.**
> 균형추: jaza, no_carrier, croemer, whinvik, brokegrammer(Litestar 스레드 반론), scuff3d(설계를 처음부터 async로 하면 간단해진다), seabrookmx(JS 익숙하면 FastAPI가 매끄럽다), leameow(색칠은 오히려 부작용을 드러내서 좋다), 그리고 프로덕션 참조 코드베이스(`polarsource/polar`).
> **플랫폼 편중:** HN + GitHub Discussions가 대부분이고, 둘 다 **문제를 겪은 사람이 글을 쓰는 곳**이다. **"조용히 잘 쓰는 다수"는 이 문서에 나타나지 않는다.**

### 4-1. sync를 기본으로 할 것인가, async를 기본으로 할 것인가

- **관점 A (async 기본):** 설계를 처음부터 async로 하면 오히려 간단해진다(scuff3d). 색칠(function coloring)은 부작용을 드러내서 좋다(leameow).
- **관점 B (sync 기본):** 대부분의 CRUD 앱은 sync가 낫다. 동기 드라이버 하나만 섞여도 이점이 사라진다.
- **결정적 사실 (web_deploy §2-E):** **FastAPI 공식 SQL 튜토리얼이 전부 동기다.** ▶ "FastAPI = async"라고 믿고 온 독자가 `MissingGreenlet`을 프로덕션에서야 처음 만나는 구조다.
- **플랫폼이 답을 바꾼다 (web_deploy §5-G):** **Lambda와 Cloud Run은 async에 대해 정반대다** — Lambda는 실행 환경당 1요청, Cloud Run은 인스턴스당 최대 80×vCPU 동시성. 같은 질문에 플랫폼마다 다른 답이 나온다.

### 4-2. ORM vs raw SQL vs SQLAlchemy Core

- SQLAlchemy ORM / Core / raw SQL / SQLModel 중 무엇을 쓸 것인가로 갈린다.
- 비동기 세션에서 lazy loading이 실패(`MissingGreenlet`)하는 게 ORM 선택의 실질적 비용이다.
- ▶ 3-10의 velog 사례가 좋은 균형추 — **Spring으로 옮겨가도 N+1은 따라온다.**

### 4-3. FastAPI vs Litestar vs Django Ninja vs Flask

- **Litestar 지지:** 내장 이벤트 시스템, DI, "really fast cold start"(devjab, 2025-08-07), 구조화된 대규모 앱 지원.
- **FastAPI 지지 (같은 스레드 반론):** jaza, no_carrier, croemer, whinvik, brokegrammer.
- ⚠️ **이 절이 편향의 진원지다.** 위 경고를 반드시 함께 쓰라.

### 4-4. 서비스 레이어를 둘 것인가 (Spring식 3계층)

- **rmonvfer (HN, 2025-08-06):** 공식 템플릿이 CRUD를 한 파일에 몰아넣는 걸 보고 *"started cringing"* — Rails/Spring 배경. 결론: *"I wouldn't recommend it for anything serious... not without requiring you to write a framework on top, **like I've unfortunately done**"*
- 반대편: 얇은 라우터 + 직접 로직이 Python답다는 주장.
- **mattmanser:** DTO 남발 자체가 문제 — *"to add one property I had to edit 40 files... **It's anti-patterns like that which give statically typed languages a bad name.**"*

### 4-5. SQLModel을 쓸 것인가

- 중립 근거: **여전히 `0.0.39`** (2026-06-25). 버전 번호 자체가 성숙도 신호다.
- ⚠️ SQLModel이 검증을 무력화한다는 주장(2026-03)이 커뮤니티에 있으나 `(목록만 확인 — 원문 대조 필요)`.

### 4-6. 거버넌스·버스 팩터·0.x·상업화

- **FastAPI Labs / FastAPI Cloud:** 창시자 Sebastián Ramírez가 회사를 설립하고 FastAPI Cloud를 발표(**2025-05-05**, tiangolo X 게시물 https://x.com/tiangolo/status/1919410655922176040). 축자: *"BIG NEWS ✨ I started a company... We're building @FastAPIcloud 🚀 ... One command: fastapi deploy"*. 2026-06 공개 베타 `(목록만 확인 — 원문 대조 필요)`.
- 🚨 **상업화 백래시는 만들어내지 마라.** 존재는 확인됐지만 **비판적 반응은 확인하지 못했다.**
- ⚠️ **0.x 버전대 유지에 대한 커뮤니티 의견도 근거를 못 찾았다.**
- 버스 팩터 우려 인용은 근거가 탄탄하나 **위 두 항목과는 별개 주제다. 섞지 마라.**
- 대비 사실: FastAPI 100,866 stars / open_issues 87 / MIT (GitHub API, 2026-07-25).

### 4-7. 이벤트 루프 블로킹 경고 — 🚨 제안이지 기능이 아니다

- GitHub fastapi/fastapi **#14603**은 개발 모드에서 이벤트 루프 블로킹을 경고하자는 **제안 단계**다. `(목록만 확인 — 원문 대조 필요)` — research-lead가 원문을 열어보지 않았고 URL·게시일·현재 상태를 확인하지 않았다.
- 🚨 **"FastAPI가 블로킹을 경고해준다"고 쓰면 사실 오류다.** 기능으로 서술하지 마라.
- 저술 전 `https://github.com/fastapi/fastapi/discussions/14603`(또는 issues/14603)을 열어 상태를 확인할 것. **확인되지 않으면 이 항목을 아예 쓰지 마라.**

---

## 5. 실무 적용 팁

1. **버전 표기:** 모든 코드 예제에 **"FastAPI 0.140 / Starlette 1.3 / Pydantic 2.13 / 2026년 7월 기준"**을 명시하라. 계열 버전(`SQLAlchemy 2.0`, `Pydantic v2`)은 안전하고 패치 버전은 위험하다.
2. **`def` vs `async def`:** sync 경로 함수는 **40개 스레드 풀**을 sync 의존성과 **공유**한다. 이 상한과 조정법(`current_default_thread_limiter().total_tokens`)을 함께 제시하라.
3. **backpressure:** `--limit-concurrency`가 정답이다(503 반환). `--backlog`(기본 2048)와 혼동하지 마라.
4. **업로드:** 1MB가 메모리→디스크 분기점이고 `max_part_size` 기본 1MB가 실제 벽이다.
5. **보안:** `PyJWT` + `pwdlib[argon2]`로 쓰고, 독자가 인터넷에서 볼 `python-jose` + `passlib` 예제가 **왜** 낡았는지 설명하라. Spring Security 출신 독자에게 특히 중요하다 — 그들은 프레임워크가 정답을 정해주는 데 익숙하다.
6. **테스트:** `httpx2`는 `ASGITransport`·`AsyncClient`를 같은 이름으로 유지하고, **`EventSource`/`ServerSentEvent`와 `httpx2.websockets`(ASGIWebSocketTransport 등)를 내장**한다 — SSE·WebSocket 엔드포인트를 서드파티 없이 테스트할 수 있다. ⚠️ `alias_httpx`의 정확한 동작은 미확인.
7. **배포:** 컨테이너에서는 **워커 1개 + 오케스트레이터 레플리카**가 공식 권장이다. 단 Uvicorn 문서는 여전히 gunicorn으로 시작한다는 점을 알려라.
8. **관측성:** OTel API/SDK는 1.44.0 안정이지만 **FastAPI 계측은 0.65b0 베타**다. 이 대역 차이를 그대로 서술하라.
9. **마이그레이션 함정 (전부 1차 소스 확인):** `@app.on_event`→lifespan / `.dict()`→`model_dump()` / `.json()`→`model_dump_json()` / `parse_obj()`→`model_validate()` / `orm_mode`→`from_attributes` / `@validator`→`@field_validator` / `@root_validator`→`@model_validator` / `class Config`→`model_config = ConfigDict(...)` / `pydantic.BaseSettings`→`pydantic_settings.BaseSettings` / `regex`→`pattern` / `openapi_prefix`→`root_path` / `q: str = Query(None)`→`Annotated[str, Query()]`

**🚨 `on_event`의 3층 구조 — 뭉개면 사실 오류가 된다:**
1. **FastAPI 0.140.0에는 `on_event`가 아직 있다.** 소스에 `@deprecated` 데코레이터가 실제로 붙어 있다 (`applications.py:4648`, 축자: `on_event is deprecated, use lifespan event handlers instead.`). `on_startup`/`on_shutdown` 파라미터도 남아 있다.
2. **Starlette 1.0.0rc1에서는 완전히 제거**됐다 — 축자: *"Remove `on_event()` decorator from `Starlette` and `Router`"*, `on_startup`/`on_shutdown`/`add_event_handler()`/`@app.route()`도 함께 제거.
3. **FastAPI는 `starlette>=0.46.0`으로만 핀한다** — 독자의 lock 파일에 0.4x가 있을 수도 1.x가 있을 수도 있다.
→ **"FastAPI가 `on_event`를 제거했다"는 틀린 서술이다.**

**🚨 `httpx2`도 같은 방식으로 정확히:** Starlette `testclient.py`는 `try: import httpx2 / except: import httpx + StarletteDeprecationWarning` 구조다. **httpx2는 "권장"이지 "필수"가 아니다.** 그리고 FastAPI `[standard]`는 여전히 `httpx<1.0.0`을 핀한다.

### 5-A. 테스트 (축 5) — 🔴 공식 문서는 `pytest-asyncio`가 아니라 `anyio`를 쓴다

대부분의 독자가 반대로 알고 있다. 현재 공식 비동기 테스트 코드 (raw 원문):
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
문서 축자:
> "If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. **AnyIO provides a neat plugin for this**"
> "**By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions.**"
> ⚠️ (warning) "**If your application relies on lifespan events, the `AsyncClient` won't trigger these events.** To ensure they are triggered, use `LifespanManager` from florimondmanca/asgi-lifespan."

⚠️ **공식 문서가 권하는 `asgi-lifespan`은 2.1.0 / 2023-03-28로 3년 넘게 릴리스가 없다.** 정체 상태를 병기하라.

⚠️ **함정:** 공식 예제 디렉터리에 `conftest.py`가 없다. AnyIO 문서는 `anyio_backend` fixture 지정을 안내한다 — 안 하면 **asyncio·trio 양쪽으로 실행된다**:
```python
@pytest.fixture
def anyio_backend():
    return 'asyncio'
```

**pytest-asyncio를 쓴다면** (1.4.0): `asyncio_mode`는 `strict`(기본)/`auto`. 🔴 **1.0.0(2025-05-26)에서 `event_loop` fixture가 제거됐다** — 인터넷의 옛 FastAPI 테스트 예제가 대량으로 깨진 지점이다.

**`dependency_overrides`** — Spring `@MockBean` / NestJS `overrideProvider()`에 대응:
```python
app.dependency_overrides[common_parameters] = override_dependency
app.dependency_overrides = {}   # 초기화
```

**테스트 DB 롤백** — SQLAlchemy 공식 레시피의 핵심 키워드는 **`join_transaction_mode="create_savepoint"`**(2.0 도입). Spring `@Transactional` 테스트 롤백의 정확한 대응물이다.
```python
self.connection = engine.connect()
self.trans = self.connection.begin()
self.session = Session(bind=self.connection, join_transaction_mode="create_savepoint")
...
self.trans.rollback()   # commit() 호출분까지 전부 롤백
```
⚠️ **`AsyncSession` 버전 레시피는 해당 두 페이지(session_transaction, asyncio 확장) 어디에도 없다.** 전수 확인은 아니므로 "그 두 페이지에는 없다"로만 표현하라.

`testcontainers` 4.15.0 축자: "Version 4.0.0 onwards we do not support the testcontainers-* packages"

### 5-B. 로깅·관측성 (축 5)

- 🔴 **uvicorn 로거의 `propagate: False`**가 구조적 로깅과 충돌하는 실제 원인이다(web_deploy §3-A).
- ⚠️ "사용자 dictConfig에 `disable_existing_loggers`를 빠뜨리면 uvicorn 로거가 죽는다"는 **uvicorn 소스 + Python `dictConfig` 기본값(True)에서 연역한 것**이지 uvicorn이 명시한 문장이 아니다. 원 이슈 #511은 **CLOSED**이고 ini 경로는 이미 수정됐다. **책에 넣으려면 실제 재현 실험을 붙여라.**
- contextvars 기반 correlation ID 전파에는 알려진 함정이 있다(web_deploy §3-B). ⚠️ **Starlette 측 공식 보장 문서는 못 찾았다** — structlog 측 경고문만 확보.
- **OTel 대역 차이:** API/SDK는 **1.44.0 안정**인데 FastAPI 계측은 **0.65b0 베타**다. 그대로 서술하라.
- 🔴 **prometheus_client는 멀티프로세스 제약이 있다** → §5-D의 "워커 1개" 권장과 직접 연결된다.

### 5-C. CI/CD (축 6)

**uv가 공식 기본이 됐다** — FastAPI 0.140.0에 PR #16032 "📝 Update docs to use uv projects by default"가 포함됐고, 보안·프록시·설정 문서의 명령이 전부 `uv add`/`uv run`이다.

`uv.lock` 축자:
> "a *universal* or *cross-platform* lockfile" / "This file should be checked into version control" / "**The `uv.lock` format is specific to uv and not usable by other tools**"

**🔴 이 책만 할 수 있는 이야기 — PEP 751:**

| 항목 | 값 |
|---|---|
| PEP 751 | "A file format to record Python dependencies for installation reproducibility" |
| Author | Brett Cannon |
| **Status** | **Final** |
| Created / Resolution | 2024-07-24 / **2025-03-31** |
| 표준 파일명 | **`pylock.toml`** |

→ **2025-03-31에 락파일 표준이 Final로 확정됐는데, 사실상 표준 도구인 uv의 기본 산출물(`uv.lock`)은 그 표준 포맷이 아니다.** Maven `pom.xml`·Gradle 락파일처럼 단일 표준에 익숙한 독자에게 반드시 설명해야 한다.

**`--locked` vs `--frozen` (의미가 다르다):**
> `--frozen`: "To use the lockfile **without checking if it is up-to-date**"
> `--locked`: "If the lockfile is not up-to-date, uv will **raise an error instead of updating** the lockfile."

⚠️ uv 문서에 "프로덕션에선 `--frozen`을 써라"는 **명시적 권고가 없다.** uv 자신의 Docker 가이드는 **`--locked`**를, Uvicorn 공식 Dockerfile은 **`--frozen`**을 쓴다 — **두 공식 문서가 다른 플래그를 쓴다는 사실 자체를 정확히 서술하라.**

**Poetry 2.4.1도 PEP 621로 이동했다** — `[project]` 섹션 지원, Poetry 2.0부터 `[tool.poetry]`의 `name`·`description`·`license`·`authors` 등은 **deprecated**.
**pip-tools는 죽지 않았다** — 저장소 `archived: false`, 마지막 push 2026-07-24. uv가 `uv pip compile`로 인터페이스를 **흡수**한 것이다.

**🔴 ruff의 버저닝은 SemVer가 아니다 (축자):**
> "Ruff uses a custom versioning scheme that uses the **minor** version number for breaking changes and the **patch** version number for bug fixes."

→ **`0.16.0` → `0.17.0`이 breaking change다.** CI 핀 전략에 직결되며 Spring/Node 독자가 반드시 오해한다.
포매터 축자: "**drop-in replacement for Black**" / "**> 99.9% of lines are formatted identically**" (Django·Zulip 대상)

**🔴 타입체커 성숙도가 통념과 반대다:**

| | Astral `ty` | Meta `pyrefly` |
|---|---|---|
| 버전 | **0.0.63** | **1.1.1** |
| 자기 선언 | **"ty is currently in beta."** | **"Pyrefly's current development status is stable."** |
| 버전 정책 | "**breaking changes... may occur between any two versions**" | "**any version may introduce new type errors and other breaking changes**" |
| 실적 | "10x - 100x faster than mypy and Pyright" | "**the default type checker for Instagram's 20-million-line Python codebase at Meta**" (PyTorch·JAX 채택) |
| FastAPI 관련 | — | "Built-in support for... **Pydantic**, Django, and pytest" |

→ Astral 제품(uv·ruff)의 성공 때문에 `ty`도 성숙했으리라 짐작하기 쉽지만 **반대다.** "CI 게이트로 걸어라"고 쓸 수 있는 건 pyrefly 쪽이다.
🔍 방증: FastAPI 소스 `applications.py`에 **`# ty: ignore[deprecated]`** 주석이 있다 — FastAPI가 `ty`를 실제로 돌린다는 1차 증거.
⚠️ PyPI의 `pyright` 패키지는 자기 설명이 "Command line wrapper for pyright" — **공식 릴리스 채널이 아닌 커뮤니티 래퍼다.**

**GitHub Actions**
- `astral-sh/setup-uv` 현재 메이저 **v9** (`v9.0.0`, 2026-07-21, "Change `prune-cache` default to `false`"). `enable-cache: "auto"`(GitHub-hosted에서 활성).
- ⚠️ **문서 지연:** uv 자신의 가이드는 아직 **v8.1.0**을 핀한 예제를 싣는다.
- `actions/setup-python` 현재 메이저 **v7** (2026-07-20).
- 🔴 **가장 흔한 지뢰 (action.yml 축자):** `cache`: "Supported values: **pip, pipenv, poetry.**" → **`cache:`는 uv를 지원하지 않는다.** `astral-sh/setup-uv`의 `enable-cache`나 `actions/cache`를 직접 써야 한다.

### 5-D. 컨테이너·클라우드 배포 (축 7)

**Uvicorn 공식 Dockerfile (uv 기반, 원문):**
```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
축자: "The key strategy is to install dependencies first, then copy the project files."
워커 질문에 대한 공식 답: *"The image above uses a single Uvicorn worker. **The recommended approach is to let your orchestration system manage the number of deployed containers** rather than relying on the process manager inside the container."*

⚠️ **이 공식 예시를 그대로 베끼지 마라:** ① 비루트 유저 경고문만 있고 `USER` 지시어가 **실제로 없다** ② 베이스가 `python:3.12-slim`으로 **하드코딩**돼 있는데 3.12는 현시점 최신이 아니다.
비루트 1차 출처는 uv 문서가 링크하는 예제 저장소에 있다: `groupadd --system --gid 999 nonroot` + `USER nonroot`.

**gunicorn을 꼭 써야 한다면** — `uvicorn/workers.py`는 임포트 시 경고를 던진다:
```python
warnings.warn(
    "The `uvicorn.workers` module is deprecated. Please use `uvicorn-worker` package instead.\n"
    ...
    DeprecationWarning,
)
```
대체는 **`uvicorn-worker` 0.4.0 / 2025-09-20**. 그리고 gunicorn 경유 시 기능 손실이 있다 — 축자: *"some options such as **`--limit-concurrency` are not yet supported** when running with Gunicorn."*

**🔴 Alpine vs slim — 통념이 절반만 맞다 (실측)**
흔한 설명("Alpine은 musl이라 manylinux wheel을 못 써서 소스 빌드가 돈다")은 **출처가 어긋나 있다**:
- 공식 이미지 README의 **alpine** 문단은 wheel이 아니라 런타임 호환성 얘기다: *"it does use musl libc instead of glibc and friends, so software will often run into issues"*
- "소스 빌드 실패" 문장은 **slim** 문단에 있고 원인은 musl이 아니라 **컴파일러 부재**다.
- **PEP 656(musllinux)은 2021년 Final.** 그리고 PyPI JSON API로 실제 wheel 태그를 집계한 결과(조회 2026-07-25):

| 패키지 | musllinux wheel | manylinux wheel |
|---|---|---|
| pydantic-core 2.47.0 | **21** | 48 |
| uvloop 0.22.1 | **16** | 16 |
| httptools 0.8.0 | **14** | 14 |
| numpy 2.5.1 | **8** | 8 |
| orjson 3.11.9 | **20** | 30 |
| cryptography 49.0.0 | **6** | 31 |

→ **FastAPI 스택의 핵심 네이티브 확장은 전부 musllinux wheel을 배포한다.** 정확한 권고는 "Alpine 쓰지 마라"가 아니라 ① 기본은 `-slim` ② Alpine을 쓸 거면 의존성 전체의 musllinux wheel 보유를 실제로 확인 ③ 남는 리스크는 musl 런타임 차이·롱테일 패키지·툴체인 부재다.

**프록시 뒤 배치 — 보안 주의**
- uvicorn이 지원하는 헤더는 **`X-Forwarded-For`·`X-Forwarded-Proto` 둘뿐**이다.
- `--proxy-headers`는 기본 활성이나 `--forwarded-allow-ips` 기본값은 **`127.0.0.1`**이다.
- 축자: *"**Only trust clients you can actually trust!** Incorrectly trusting other clients can lead to malicious actors spoofing their apparent client address"*
- 🚨 **FastAPI 프록시 문서의 예시가 `--forwarded-allow-ips="*"`를 쓴다 — 복붙 위험을 반드시 경고하라.**

**Kubernetes — probe와 종료 시퀀스**
공식 처방 축자:
> "**When your app has a strict dependency on back-end services, you can implement both a liveness and a readiness probe. The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available.**"

→ **`/healthz`(liveness)와 `/ready`(readiness)를 분리**하고 readiness에서만 DB·Redis를 확인하는 게 공식 권장이다.
기본값: `periodSeconds` **10초** / `timeoutSeconds` **1초** / `failureThreshold` **3**. `httpGet`은 200~399면 성공.

종료 시퀀스 축자:
> "first sending a TERM (aka. SIGTERM) signal... **The default `terminationGracePeriodSeconds` setting is 30 seconds.**"
> "**At the same time as** the kubelet is starting graceful shutdown of the Pod, the control plane evaluates whether to remove that shutting-down Pod from EndpointSlice objects"
> "**Any endpoints that represent the terminating Pods are not immediately removed**... Terminating endpoints always have their `ready` status as `false`"

⚠️ **통념 교정:** "SIGTERM과 엔드포인트 제거의 순서가 보장되지 않아 트래픽이 샌다"는 흔한 설명은 현재 문서와 다르다. 두 과정은 **병렬("At the same time as")**이고 terminating 엔드포인트는 `ready: false`로 남는다. → `preStop` sleep의 근거는 **"아직 갱신을 전파받지 못한 LB/클라이언트가 존재할 수 있다"**로 서술해야 정확하다.

매핑: `terminationGracePeriodSeconds`(기본 30초) **>** uvicorn `--timeout-graceful-shutdown`이어야 SIGKILL 전에 정리가 끝난다.
**HPA:** `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`, tolerance 0.1, sync 15초, downscale stabilization **5분**.
⚠️ **"IO-bound async 앱에 CPU가 나쁜 신호"라는 문장은 k8s 문서에 없다.** 저자 추론으로 표시하라.

**🔴 서버리스 — Lambda와 Cloud Run은 async에 대해 정반대다**

*사실 (벤더 1차 소스):*
- **Lambda:** *"**For each concurrent request, Lambda provisions a separate instance of your execution environment.**"* / *"this execution environment is busy and cannot process other requests."* 공식 식: `Concurrency = (average requests per second) * (average request duration in seconds)`. 스케일 속도 "1,000 execution environment instances every 10 seconds". 쿼터: 응답 payload **6MB**(스트리밍 200MB), 타임아웃 **900초**, 이미지 **10GB**, 기본 동시 실행 **1,000**.
- **Cloud Run:** 인스턴스당 최대 동시 요청 기본 **"80 times the number of vCPUs"**, 최대 1,000. graceful shutdown이 **10초**(SIGTERM→SIGKILL) — **K8s 기본 30초와 대비된다.** 포트는 `PORT` 주입, 기본 8080, `0.0.0.0` 바인딩 필수, 기동 4분 내 리슨.
- **Azure Container Apps:** HTTP `concurrentRequests` 기본 **10**, minReplicas 0 / maxReplicas 10, cool down 300초.

*추론 (저자의 결론 — 벤더가 이렇게 말한 것은 아님. 반드시 "추론"으로 표시할 것):*
1. **Lambda 실행 환경 하나 안에서는 async 동시성이 처리량을 늘려주지 않는다.** `async def`의 이득은 *한 요청 내부의 여러 I/O를 겹칠 때만* 유효하다.
2. **Cloud Run은 정반대다.** 인스턴스당 기본 80×vCPU이므로 async I/O 다중화가 **직접** 인스턴스 수와 비용을 줄인다.
3. → **"FastAPI를 서버리스에 올린다"를 한 문장으로 묶으면 안 된다.**

**Mangum vs AWS Lambda Web Adapter**

| | Mangum | Lambda Web Adapter |
|---|---|---|
| 형태 | Python 라이브러리 (`handler = Mangum(app)`) | Lambda **extension 바이너리** |
| 코드 변경 | 핸들러 래핑 필요 | **없음** — `fastapi run` 그대로 |
| 응답 스트리밍 | ⚠️ 미확인 | 지원 (`AWS_LWA_INVOKE_MODE=response_stream`) |
| 제공 | 커뮤니티 (`Kludex/mangum`) | **AWS 공식** (v1.0.1 / 2026-05-28) |

Mangum 유지보수 판정: `archived: false`이나 최근 커밋 5건 중 3건이 Dependabot 범프, 2건이 문서 수정 → **"유지보수 모드"가 정확한 표현**이다("죽었다"도 "활발"도 아님).
▶ LWA를 쓰면 위 Dockerfile을 **그대로** Lambda에 올릴 수 있다. Spring 독자에게는 "`aws-serverless-java-container` vs 그냥 컨테이너" 대비로 설명하면 즉시 통한다.

**PaaS 계약**

| | 기본 포트 | 포트 전달 | scale-to-zero |
|---|---|---|---|
| Fly.io | **8080** (`internal_port`) | `fly.toml` 선언 | `auto_stop_machines="stop"` + `min_machines_running=0` |
| Cloud Run | **8080** | `PORT` 주입 | 기본 |
| Azure Container Apps | ingress target-port | — | 기본 |
| Render | **10000** | `PORT` | ⚠️ 미확인 |
| Railway | ⚠️ 미확인 | ⚠️ 미확인 | ⚠️ 미확인 |

- Render 공식 FastAPI 가이드 Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- ⚠️ **Railway 공식 FastAPI 가이드는 uvicorn이 아니라 Hypercorn을 쓴다**: `["hypercorn", "main:app", "--bind", "::"]`
- ⚠️ Fly.io: 스키마 기본값 `auto_stop_machines="off"`이지만 `fly launch`가 새 앱에 쓰는 값은 `"stop"`이다. **두 문서가 다 맞으므로 구분하라.**

**대안 서버 — 언제 uvicorn을 벗어나는가**
- **uvicorn은 HTTP/1.1만** 지원한다. HTTP/2가 필요하면 Granian 또는 Hypercorn, **HTTP/3(QUIC)는 Hypercorn만**이고 그것도 `[h3]` extra + 문서 표현상 "current draft"다.
- Granian이 **스스로 밝힌 "쓰지 말아야 할 이유"**(균형 잡기에 유용): "you want a *pure Python* solution / you need advanced debugging features / your application relies on `trio` or `gevent`"
- `uvicorn[standard]`가 설치하는 6개: `uvloop`·`httptools`·`websockets`·`watchfiles`·`python-dotenv`·`PyYAML`. 기본 설치는 `h11`+`click`만.

---

## 6. 참고문헌

### 6-1. 1차 소스 — 공식 문서·명세 (전 항목 조회 2026-07-25)

| # | 제목 | URL |
|---|---|---|
| R1 | FastAPI 릴리스 노트 | https://fastapi.tiangolo.com/release-notes/ |
| R2 | FastAPI — OAuth2 with JWT | https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ |
| R3 | FastAPI — Server Workers | https://fastapi.tiangolo.com/deployment/server-workers/ |
| R4 | FastAPI — FastAPI in Containers (Docker) | https://fastapi.tiangolo.com/deployment/docker/ |
| R5 | FastAPI — Lifespan Events | https://fastapi.tiangolo.com/advanced/events/ |
| R6 | FastAPI — Dependencies with yield (scope) | https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/ |
| R7 | FastAPI — Query Params & String Validations (`Annotated`) | https://fastapi.tiangolo.com/tutorial/query-params-str-validations/ |
| R8 | FastAPI — Behind a Proxy | https://fastapi.tiangolo.com/advanced/behind-a-proxy/ |
| R9 | FastAPI — Strict Content-Type | https://fastapi.tiangolo.com/advanced/strict-content-type/ |
| R10 | **ASGI 명세 (main)** — "Version: 3.0 (2019-03-20)" | https://asgi.readthedocs.io/en/latest/specs/main.html |
| R11 | **ASGI 명세 (HTTP & WebSocket scope)** | https://asgi.readthedocs.io/en/latest/specs/www.html |
| R12 | **anyio — Threads** ("default ... limiter has a value of 40") | https://anyio.readthedocs.io/en/stable/threads.html |
| R13 | Pydantic v2 마이그레이션 가이드 | https://docs.pydantic.dev/latest/migration/ |
| R14 | Starlette 릴리스 노트 | https://www.starlette.io/release-notes/ |
| R15 | Uvicorn 문서 (deployment·settings·logging·websockets·server-behavior) | https://github.com/Kludex/uvicorn/blob/main/docs/ |
| R16 | AWS Lambda 런타임 | https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html |
| R17 | Cloud Run 런타임 지원 | https://docs.cloud.google.com/run/docs/runtime-support |
| R18 | PEP 703 (free-threading, Final, 3.13) / PEP 779 (Final, 3.14) | https://peps.python.org/api/peps.json |

### 6-2. 1차 소스 — 소스 코드 (태그 고정)

| # | 대상 | 태그 | 확인 내용 |
|---|---|---|---|
| R20 | `fastapi/{applications,routing,param_functions,concurrency,exceptions}.py`, `dependencies/utils.py` | 0.140.0 | 전 API 시그니처, `Depends(scope=)`, `@deprecated on_event`, `openapi_version="3.1.0"`, sync 오프로드 경로, `iter_route_contexts()` |
| R21 | `starlette/{concurrency,testclient,formparsers}.py`, `middleware/base.py` | 1.3.1 | `run_in_threadpool`, httpx2 전환, **`spool_max_size = 1MB`** |
| R22 | `anyio/_backends/_asyncio.py`, `to_thread.py` | 4.14.2 | **`CapacityLimiter(40)`** |
| R23 | `uvicorn/{main,config}.py` | 0.51.0 | CLI 플래그 실재·기본값, loop/http 선택지 |
| R24 | `httpx2` wheel (`__init__.py` `__all__`, `_transports/asgi.py`) | 2.9.1 | `ASGITransport`·`AsyncClient`·`EventSource`·`websockets` 서브패키지 |

### 6-3. 패키지 인덱스 / 릴리스 API

- PyPI JSON API: `https://pypi.org/pypi/{package}/json` (§버전 핀 테이블 전체의 근거)
- GitHub Releases API: `https://api.github.com/repos/{owner}/{repo}/releases`
- python.org 릴리스 API / endoflife.date / Docker Hub Tags API

### 6-4. 학술 문헌 (전체 목록·초록 확인 여부는 `research/papers.md` §6)

> papers.md는 **전문을 직접 읽은 9편**과 `초록만` 확인한 것을 구분해 표기했다. 수치를 인용하려면 그 표기를 확인하라.

**동시성 모델**
- Adya, Howell, Theimer, Bolosky, Douceur. **"Cooperative Task Management Without Manual Stack Management"** — USENIX ATC 2002. 부제: *"Event-driven Programming is Not the Opposite of Threaded Programming"*. ⭐ 작업 관리 × 스택 관리 **2축 공간**에서 제3의 sweet spot을 제시 — 그게 20년 뒤 async/await로 실현됐다는 서사가 이 책 §1의 척추가 된다.
- von Behren, Condit, Brewer. **"Why Events Are A Bad Idea (for High-Concurrency Servers)"** — HotOS IX, 2003. 🕒 하드웨어 전제가 다름을 명시할 것.
- Welsh, Culler, Brewer. **"SEDA: An Architecture for Well-Conditioned, Scalable Internet Services"** — SOSP 2001. DOI `10.1145/502034.502057`
- Pai, Druschel, Zwaenepoel. **"Flash: An Efficient and Portable Web Server"** — USENIX ATC 1999. (AMPED 구조)
- Brockbernd et al. **"Understanding Concurrency Bugs in Real-World Programs with Kotlin Coroutines"** — ECOOP 2024. 코루틴 버그 55건 분류, 최다 범주는 `CancellationException` 처리(14건). 조사 대상에 **Ktor(JVM 비동기 웹 프레임워크)** 포함. ⭐ **asyncio 실증 연구가 전무한 공백의 프록시**이자 Java 독자에게 직접 닿는 자료. ⚠️ 언어 불일치를 반드시 명시하고 옮길 것.
- Ousterhout. "Why Threads Are A Bad Idea (for most purposes)" — ⚠️ **비심사 강연 자료**

**벤치마크·측정 방법론**
- Mytkowicz, Diwan, Hauswirth, Sweeney. **"Producing Wrong Data Without Doing Anything Obviously Wrong!"** — ASPLOS 2009. DOI `10.1145/1508244.1508275`
- Georges, Buytaert, Eeckhout. **"Statistically Rigorous Java Performance Evaluation"** — OOPSLA 2007. DOI `10.1145/1297027.1297033`
- van der Kouwe et al. **"SoK: Benchmarking Flaws in Systems Security"** — IEEE EuroS&P 2019. **DOI `10.1109/EUROSP.2019.00031`** ⭐ **동료 심사 정본이다.** 널리 인용되는 "Benchmarking Crimes" 프리프린트와 **판본이 다르다**(용어 crimes→flaws, 저자 순서 상이) — papers.md에 판본 3종 비교표가 있다. **22가지 결함, 최상위 학회 논문 50편 중 평균 5건 위반, 무결점은 단 1편.**
- Friedrich et al. — coordinated omission을 적용한 워크숍 논문, BTW 2017
- Dean, Barroso. **"The Tail at Scale"** — CACM 2013. ⚠️ **전문 확보 실패**(research.google·아카이브 전부). 재인용 수치가 변형돼 떠돌므로 **papers.md는 수치를 아예 싣지 않았다. 수치 인용 금지.**
- **Little's Law** — Little (1961), *Operations Research* 게재 정리(DOI 확인됨)
- ⚠️ **USL(Universal Scalability Law)은 arXiv 프리프린트·CMG·저서가 원전**이다. 실무에서 Little's Law와 나란히 인용되지만 **두 "법칙"의 지위가 다르다.**
- ⚠️ **coordinated omission의 원전(Gil Tene)은 동료 심사를 거치지 않았다.** "강연/비심사"로 표기하라.

**타입·API·스키마**
- Gao, Bird, Barr. "To Type or Not to Type: Quantifying Detectable Bugs in JavaScript" — ICSE 2017 (⚠️ 15%는 **JavaScript** 대상 수치 — 언어를 반드시 표기)
- "To Type or Not to Type? A Systematic Comparison of ... JavaScript and TypeScript Applications on GitHub" — 위 결과의 **반증 계열**. 함께 제시할 것
- "How Well Static Type Checkers Work with Gradual Typing? A Case Study on Python"
- "Towards a Large-Scale Empirical Study of Python Static Type Annotations" / "The Evolution of Type Annotations in Python: An Empirical Study"
- Atlidakis, Godefroid, Polishchuk. **RESTler: Stateful REST API Fuzzing** — ICSE 2019
- **EvoMaster** (진화 기반 REST/GraphQL/RPC 퍼징 도구 계열) / **OASQuali** (OpenAPI 명세 품질 자동 분석)
- ⚠️ Di Grazia & Pradel — **초록 미확보. 내용 인용 금지.**

**아키텍처·서버리스**
- Wang, Li, Zhang, Ristenpart, Swift. **"Peeking Behind the Curtains of Serverless Platforms"** — USENIX ATC 2018. ⭐ 같은 플랫폼에서 **Python 2.7 콜드 스타트 167~171ms vs Java 824~974ms.** ⚠️ **2018년 측정이므로 절대값이 아닌 상대 구조로만 인용할 것.**
- Shahrad et al. **"Serverless in the Wild"** — USENIX ATC 2020
- Oakes et al. **SOCK** — USENIX ATC 2018 / Du et al. **Catalyzer** — ASPLOS 2020 (DOI `10.1145/3373376.3378512`) / Agache et al. **Firecracker** — NSDI 2020
- **Microusity: A Testing Tool for Backends for Frontends (BFF) Microservice Systems** — ICPC 2023. **이 영역의 사실상 유일한 문헌**
- Kubernetes HPA 오토스케일링 연구 계열 / 마이크로서비스 systematic mapping study 계열

### 6-5. 커뮤니티 (직접 열어서 읽은 것만 — community.md §7에 전체 목록)

- **Hacker News:** 44818249(rmonvfer) / 44816140(com2kid) / 44821476(globular-toast) / 44701062(duncanfwalker) / 44656419(Pydantic 도메인 레이어 스레드) / 29444847(hiram112) / 44816755(Litestar 스레드 — ⚠️편향 진원지)
- **GitHub fastapi/fastapi:** #643 / #1376 / #512 / #8054 / #8433 / #11107·#11143 / #14137 / #14517 / PR #15951 / Discussion #6695 / #9148(⚠️upvote 18, 1차 회차의 56은 오류)
- **GitHub 기타:** trallnag/prometheus-fastapi-instrumentator #370·#379·#388 / pydantic/pydantic Discussion #8468 / aws-lambda-web-adapter #620
- **Lobsters:** Django vs FastAPI 스레드(antoinewdg, alper, linkdd, koala)
- **Dev.to:** FastNest (Hamza El Mouddane, 2026-04-28)
- **한국:** velog 고은연(2022-01-07) / velog JUNYOUNG(2025-03-07) / shipfriend.dev 서정우(2026-03-28) / 카카오페이 기술블로그(2022-08-29)
- **라이브러리 문서(불만의 물증):** dishka / python-dependency-injector

---

## 7. 리서치 공백 (커버하지 못한 영역)

> **Phase 2 계획가·Phase 4 저술가에게:** 아래는 **확인된 공백**이다. 여기 없는 걸 "확인됐다"고 가정하지 말고, **여기 있는 걸 억지로 채우지도 마라.**

### 7-1. 🚨 접근 자체가 막힌 플랫폼 — 이 리서치의 최대 구멍

**Reddit — 전면 차단. 우회 7경로 전부 실패.** r/FastAPI, r/Python, r/django, r/webdev, r/ExperiencedDevs에서 **단 한 건도 수집하지 못했다.**

| 시도 경로 | 실패 양상 |
|---|---|
| `www.reddit.com` 직접 | 도구 레벨 차단 |
| `old.reddit.com` | 도구 레벨 차단 |
| `.json` 엔드포인트 | 도구 레벨 차단 |
| WebSearch `allowed_domains: reddit.com` | API 400 |
| 질의문에 `site:reddit.com` | 결과에 Reddit 미출현 |
| redlib 공개 인스턴스 2곳 | HTTP 403 |
| `r.jina.ai` 프록시 | Reddit이 403 |

**Stack Overflow — 전면 차단.** WebSearch `allowed_domains`(API 400), Stack Exchange API 2경로(도구 레벨 차단) 전부 실패.
→ **투표순 상위 FastAPI 질문 목록은 실무 고통점의 가장 좋은 지표인데 이 문서에는 없다.**

> 🚨 **이 문서에 Reddit·Stack Overflow 인용은 하나도 없다. 다른 단계에서 그 출처의 인용을 만들어 넣으면 그건 근거 없는 것이다.**

**OKKY·GeekNews — 목록은 되고 본문은 안 된다.** 제목·존재만 확인, 본문이 클라이언트 렌더링이라 텍스트 0줄. 확인된 8건은 "한국 개발자가 무엇을 묻고 있는가"의 **지표로만** 쓸 것 — 제목만 근거로 내용을 지어내지 마라.
**커리어리·네이버 카페·Discord/Slack·X·Mastodon — 미수집.**

### 7-2. 🚨 Java/Node 대조 축에서 **끝내 근거가 없는** 항목

**이 책의 차별화 축이라 2차 회차까지 돌렸으나 아래는 여전히 0건이다.**

| 항목 | 상태 |
|---|---|
| **커스텀 검증기** (`ConstraintValidator` vs `field_validator`) | ⚠️ **4개 경로 전부 0건.** 두 커뮤니티가 서로를 비교하는 토론 자체가 형성돼 있지 않다 |
| **Spring WebFlux/Reactor → asyncio 교차 경험담** | ⚠️ **0건.** HN Algolia `webflux` 2,205건 중 상위 40건 전수 확인 + Discussions 검색해도 없음. Java 내부 Reactor 회의론은 **asyncio 대조가 아니다 — 섞지 마라** |
| **Spring Security 필터 체인·`@PreAuthorize` 전환자의 체감** | ⚠️ **0건.** §3-9에 있는 근거는 **"조립의 비용"에 대한 것이지 "Spring Security 사용자의 체감"이 아니다 — 같은 절로 묶지 마라** |
| **Spring Boot Actuator 대응물 부재** | ⚠️ 인접 증거만 (#9148, **upvote 18** — 1차 회차의 56은 오류) |
| `application.yml` vs pydantic-settings | ⚠️ 근거 못 찾음 |
| **JUnit/MockMvc vs pytest/TestClient** | ⚠️ 근거 못 찾음 |
| Maven/Gradle/npm vs uv/poetry **락파일·모노레포** | ⚠️ 근거 못 찾음 |
| `@Transactional` 부재에 대한 **직접 인용** | ⚠️ 구조적 근거(#11107)만 있고 인용문 없음 |
| Spring `ProblemDetail`을 **명시적으로 거론한** FastAPI 측 요구 | ⚠️ RFC 번호로만 논의됨 |
| NestJS↔FastAPI 아키텍처 **토론** | ⚠️ 토론 없음. 유물(FastNest)로만 대체 |

> 🚨 **가장 중요한 금지 사항: "Java 개발자는 이렇게 실수한다"는 귀속을 하지 마라.**
> 실수 패턴 자체(`async def` 안에서 동기 호출 등)는 근거가 풍부하다. 그러나 **"서블릿 스레드 모델 출신이라서 그렇게 한다"고 밝힌 증언은 0건이다.** 실수는 사실로, 원인 귀속은 **저자의 가설로** 표시하라.

### 7-3. 커뮤니티 근거를 못 찾은 실무 항목

Pydantic v1→v2 성능 개선의 **실측 증언**(⚠️ **절대 지어내지 마라**) / `expire_on_commit` 함정 / 요청 간 세션 누수`(목록만 확인 — #10622)` / 깊은 `Depends` 중첩의 **정량** 오버헤드(dishka의 정성 평가가 전부) / 파일 업로드 메모리 / CORS 실무 고통`(목록만 확인 — #7319)` / OpenAPI 스키마 생성 실패 / Cloud Run 최소 인스턴스 / 콜드 스타트에서 **pandas·torch 지목**(#620은 "의존성을 줄여라"까지만) / 워커 수와 **CPU limit**의 관계 / **0.x 유지에 대한 의견** / **FastAPI Cloud 상업화 백래시**(🚨 **없는 백래시를 만들지 마라**)

### 7-4. 기술 사실 중 미확인 (fact-checker 재조사 표적)

- `SpooledTemporaryFile` → ✅ **해소됨(1MB)**, `iter_route_contexts()` → ✅ 해소, httpx2 async API → ✅ 해소, ASGI 명세 → ✅ 해소, `fastar` 정체 → ✅ 해소(용도는 ⚠️)
- ⚠️ **남은 것:** free-threading 기본값 전환 시점 / free-threading × FastAPI 벤치마크 / `BaseHTTPMiddleware`의 구체적 한계 / uvicorn `--timeout-graceful-shutdown` 기본값 / redis-py asyncio 풀 기본값 / SQLAlchemy 2.1 GA·`Query` 제거 여부 / mypy 2.x·pytest 9.x·gunicorn 26.x breaking changes / ruff formatter stable 선언 시점 / Starlette 저장소 이전 경위 / lifespan이 멀티 워커·서버리스에서 워커별 실행되는지 / `validation_error_response_definition` 현행 위치 / Azure Container Apps·Railway·Render·Fly.io 계약 / TechEmpower run의 라운드·시점 / `python` 이미지 기본 suite 다이제스트 확인 / `alias_httpx` 동작

### 7-5. 프로바넌스 경고 (반드시 읽어라)

- **하위 요약 모델이 존재하지 않는 코드를 만들어낸 사례가 2건 적발됐다** (oauth2-scopes의 가짜 주석, Auth0의 잘못된 import 경로 `fastapi_plugin.fast_api_client`). B조가 자체 적발해 raw 소스로 교정했다.
- → **렌더링 페이지 요약 경유로 들어온 코드 예시**(특히 Auth0 퀵스타트, Azure Bicep, testcontainers)는 **책에 싣기 전 원문 재확인 필수.**
- **직접 fetch로 검증된 것:** FastAPI 보안 튜토리얼 코드 / server-workers·docker 명령 / Uvicorn docs 전체 / FastAPI·Starlette·anyio·uvicorn·httpx2 소스 / 전 패키지 버전(PyPI·GitHub API) / Starlette 1.0.0 릴리스 노트 / ASGI 명세 / anyio 스레드 문서
- **언어·플랫폼 편중:** 영어 소스가 압도적. 한국 **1차 증언은 velog 3건 + shipfriend 1건이 전부**다. HN·GitHub 편중으로 부정 편향이 구조적으로 존재한다.

---

## 신선도 원장

소스별 발행일·버전 시점·검색 시점. `research/*.md`가 나중에 정리되더라도 fact-checker가 대조할 그라운딩이 여기 남는다. **전 항목 검색 시점 2026-07-25.**

| 소스 | 발행/갱신 시점 | 버전 시점 | 신선도 판정 |
|---|---|---|---|
| FastAPI 공식 문서·릴리스 노트 | 상시 갱신, 최신 항목 2026-07-24 | **0.140.0 / 2026-07 기준** | 🟢 최신 |
| FastAPI 소스 (태그 0.140.0) | 2026-07-24 | 0.140.0 | 🟢 최신 |
| Starlette 소스·릴리스 노트 (태그 1.3.1) | 2026-06-12 | **1.3.1 / 2026-06 기준** (1.0.0 = 2026-03-22) | 🟢 최신 |
| anyio 소스·문서 (태그 4.14.2) | 2026-07-12 | 4.14.2 / 2026-07 | 🟢 최신 |
| uvicorn 소스·문서 (태그 0.51.0) | 2026-07-08 | 0.51.0 / 2026-07 | 🟢 최신 |
| Pydantic 마이그레이션 가이드 (v2.13.4) | 2026-05-06 | 2.13.4 / 2026-05 | 🟢 최신 |
| httpx2 wheel (2.9.1) | 2026-07-24 | 2.9.1 / 2026-07 | 🟢 최신 |
| PyPI JSON API (전 패키지) | 조회 시점 스냅샷 | 각 표 참조 | 🟢 최신 |
| GitHub Releases API | 조회 시점 스냅샷 | — | 🟢 최신 |
| python.org 릴리스 API / endoflife.date | 2026-06-10 (최신 패치) | **3.14.6 / 2026-06 기준** | 🟢 최신 |
| Docker Hub Tags API | 2026-07-22 갱신 | trixie 세대 | 🟢 최신 |
| **ASGI 명세** | **2019-03-20** | **3.0 (spec_version 2.0~2.5)** | 🟢 **유효** — 7년째 안 변함. 오래됐지만 현행이다 |
| PEP 703 / 779 | 703: 2023 created, Final(3.13) / 779: 2025-03-13, Final(3.14) | — | 🟢 유효 |
| AWS Lambda 런타임 문서 | 상시 갱신 | python3.10~3.14, 3.15는 2026-11 목표 | 🟢 최신 |
| Cloud Run 런타임 문서 | 상시 갱신 | python310~python314 | 🟢 최신 |
| Kubernetes / Docker Engine 릴리스 | 2026-07-23 / 2026-07-16 | k8s 1.36.3 / Docker 29.6.2 | 🟢 최신 |
| GitHub 이슈 #370·#379·#388 (instrumentator) | **2026-06-14 / 06-25 / 07-08** | fastapi 0.137~0.138 | 🟢 최신 |
| GitHub PR #15951 (RFC 9457) | **2026-07-07** (제출·close 동일일) | — | 🟢 최신 |
| GitHub Discussion #14517 (RFC 9457) | 2025-12-13, 댓글 2026-07-05 | — | 🟢 최신 |
| GitHub #643 (422 논쟁) | 2019-10-22 ~ 2022-12-06 | — | 🟡 오래됨 — **논쟁 구조는 유효, 소스 위치는 대조 필요** |
| GitHub #1376 (검증 에러 커스터마이징) | 2020-05-04 ~ 2021-04-28 | — | 🟡 오래됨 — 우회법이 현행인지 대조 필요 |
| GitHub #512 (RFC 7807) | 2019-09-07, tiangolo 답변 2020-06-10 | — | 🟡 오래됨 — 상태는 여전히 미해결 |
| GitHub #8054 (Depends 싱글턴) | ~2021, **2026 현재 Unanswered** | — | 🟡 오래됐으나 **미해결 상태 자체가 현행 사실** |
| GitHub #8433 (Snowflake 동기 드라이버) | 2022-12-08 | — | 🟡 오래됨 |
| GitHub #11107 / #11143 | 2024-02, Closed(사유 미확인) | — | 🟡 **종결 사유 미확인** |
| GitHub #14137 (배경 태스크 회귀) | 2025-10 | — | 🟢 최신 |
| GitHub #9148 (타이밍 데이터 요청) | 게시일 미확인, **upvote 18** | — | 🟡 `(원문 확인함 — 1차 회차 56은 오류)` |
| pydantic #8468 (검증 에러 메시지) | 2024-01-02, upvote 17 | — | 🟢 유효 |
| HN 44816755 / 44818249 / 44816140 / 44821476 (Litestar·Express 비교) | **2025-08-06~07** | — | 🟢 최신 — ⚠️ **편향 진원지** |
| HN 44656419 / 44701062 (Pydantic 도메인 레이어) | **2025-07-23~27** | — | 🟢 최신 |
| HN 29444847 (hiram112, Java 개발자 충격) | **2021-12-04** | — | 🟡 🕒 **인지 충돌 기록으로만. 생태계 서술 금지** |
| HN async 회의론 스레드 (45106189·47859442·48281515) | 2025~2026 | — | 🟢 최신 — ⚠️ **표집 편향** |
| Lobsters (Django vs FastAPI) | ≈2025 | — | 🟢 유효 |
| Dev.to FastNest | **2026-04-28** | — | 🟢 최신 — ⚠️ 단일 저자 |
| tiangolo X (FastAPI Cloud 발표) | **2025-05-05** | — | 🟢 유효 |
| velog 고은연 | **2022-01-07** | — | 🔴 🕒 **감정·프레이밍만.** 생태계 성숙도 서술 금지 |
| velog JUNYOUNG | **2025-03-07** | — | 🟢 유효 |
| shipfriend.dev 서정우 | **2026-03-28** | — | 🟢 최신 |
| 카카오페이 기술블로그 | **2022-08-29** | 구버전 | 🔴 🕒 **방법론·결론만.** 버전 정보 인용 금지 |
| dishka / python-dependency-injector 문서 | ⚠️ 게시일 미확인 | dependency-injector 4.49.1 | 🟡 게시일 불명 |
| 학술 문헌 (동시성 고전) | **1999~2003** | — | 🔴 🕒 **원리만.** 하드웨어 전제가 다름을 명시 |
| 학술 문헌 (벤치마크 방법론) | 2007~2017 | — | 🟡 방법론이라 비교적 무관 |
| 학술 문헌 (서버리스 콜드 스타트) | **2018~2020** | — | 🟡 **상대 구조만, 절대값은 연도와 함께** |
| Kotlin 코루틴 버그 연구 | ECOOP **2024** | — | 🟢 유효 — ⚠️ **언어 불일치 명시 필수** |
