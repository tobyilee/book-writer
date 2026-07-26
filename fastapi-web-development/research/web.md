<!-- 검색 시점: 2026-07-25 기준 -->

# FastAPI 웹 리서치 (A조: 코어·비동기·마이그레이션)

검색: 2026-07-25 기준
담당 축: FastAPI 코어 API 시그니처 / 비동기 모델 / 폐기·마이그레이션 함정
대상 독자: Spring Boot·NestJS 경험자 (Python·REST 입문 자료 제외)

## 수집 방법 (fact-checker 유의)

이 문서의 **모든 API 시그니처는 태그 고정된 원본 소스 코드에서 직접 추출**했다. 요약 도구를 거치지 않았다.

- FastAPI: `raw.githubusercontent.com/fastapi/fastapi/0.140.0/...` (AST 파싱으로 파라미터 목록 추출)
- Starlette: `.../encode/starlette/1.3.1/...`
- anyio: `.../agronholm/anyio/4.14.2/...`
- uvicorn: `.../encode/uvicorn/0.51.0/...`
- Pydantic: `.../pydantic/pydantic/v2.13.4/docs/migration.md`

따라서 아래 파라미터 이름·기본값·라인 번호는 **해당 태그 기준 축자(verbatim)**다. 기억으로 재구성한 것은 없다.

> ⚠️ **이 책의 저자에게 보내는 경고.** 이번 조사에서 확인된 바, 2026년 상반기에 FastAPI·Starlette 생태계에 **대규모 파괴적 변경**이 있었다. Starlette가 1.0에 도달하며 `on_event` 계열을 *완전히 제거*했고, TestClient의 HTTP 백엔드가 `httpx` → `httpx2`로 이동했으며, Pydantic v1 지원이 완전히 제거됐다. **2025년 이전에 쓰인 거의 모든 FastAPI 블로그·튜토리얼의 코드는 지금 기준으로 낡았다.** 3장(폐기·마이그레이션)을 이 책의 차별점으로 삼을 근거가 충분하다.

---

## 1. FastAPI 코어 API 시그니처

### 1-1. `FastAPI.__init__` 파라미터 (전체, 순서대로) [S1]

`fastapi/applications.py`, 태그 `0.140.0`, AST 추출:

```
debug, routes, title, summary, description, version, openapi_url, openapi_tags,
servers, dependencies, default_response_class, redirect_slashes, docs_url, redoc_url,
swagger_ui_oauth2_redirect_url, swagger_ui_init_oauth, middleware, exception_handlers,
on_startup, on_shutdown, lifespan, terms_of_service, contact, license_info,
openapi_prefix, root_path, root_path_in_servers, responses, callbacks, webhooks,
deprecated, include_in_schema, swagger_ui_parameters, generate_unique_id_function,
separate_input_output_schemas, openapi_external_docs, strict_content_type
```

주목할 점:
- `on_startup`·`on_shutdown`은 **FastAPI에는 아직 남아 있다** (Starlette에서는 제거됨 — 3장 참조).
- `lifespan`이 정식 파라미터.
- `strict_content_type` — 0.132.0에서 추가된 신규 보안 파라미터 (아래 1-6).
- `openapi_prefix`는 여전히 존재하나 코드에 deprecation 문구가 박혀 있다 (`applications.py:632`): `"openapi_prefix" has been deprecated in favor of "root_path"`.

### 1-2. 경로 데코레이터 `@app.get` / `@app.post` 등 [S1]

`FastAPI.get`과 `FastAPI.post`의 파라미터 목록은 **완전히 동일**하다:

```
path, response_model, status_code, tags, dependencies, summary, description,
response_description, responses, deprecated, operation_id,
response_model_include, response_model_exclude, response_model_by_alias,
response_model_exclude_unset, response_model_exclude_defaults, response_model_exclude_none,
include_in_schema, response_class, name, callbacks, openapi_extra,
generate_unique_id_function
```

→ 지시서에 나온 `response_model`·`status_code`·`tags`·`dependencies`·`response_model_exclude_unset`·`responses`는 **전부 실재 확인**. ✅

### 1-3. `APIRouter` [S1]

```
APIRouter.__init__(
  prefix, tags, dependencies, default_response_class, responses, callbacks, routes,
  redirect_slashes, default, dependency_overrides_provider, route_class,
  on_startup, on_shutdown, lifespan, deprecated, include_in_schema,
  generate_unique_id_function, strict_content_type
)
```

→ `APIRouter(prefix=, tags=, dependencies=)` **실재 확인** ✅. 라우터도 자체 `lifespan`을 가진다.

```
APIRouter.include_router(
  router, prefix, tags, dependencies, default_response_class, responses,
  callbacks, deprecated, include_in_schema, generate_unique_id_function
)
```

⚠️ **주의**: `FastAPI.include_router`와 `APIRouter.include_router`는 **파라미터 집합은 동일(10개)하지만 순서가 다르다.** `FastAPI.include_router`는 `router, prefix, tags, dependencies, responses, deprecated, include_in_schema, default_response_class, callbacks, generate_unique_id_function` 순이고, `APIRouter.include_router`는 `router, prefix, tags, dependencies, default_response_class, responses, callbacks, deprecated, include_in_schema, generate_unique_id_function` 순이다. → **위치 인자로 쓰면 조용히 틀린다. 항상 키워드 인자로 쓸 것.**

### 1-4. 파라미터 선언 함수 [S1]

`fastapi/param_functions.py` AST 추출. 공통 파라미터(모두 보유):

```
default, default_factory, alias, alias_priority, validation_alias, serialization_alias,
title, description, gt, ge, lt, le, min_length, max_length, pattern, regex,
discriminator, strict, multiple_of, allow_inf_nan, max_digits, decimal_places,
examples, example, openapi_examples, deprecated, include_in_schema, json_schema_extra
```

함수별 **고유** 파라미터:

| 함수 | 고유 파라미터 |
|---|---|
| `Path` | (없음 — 공통만) |
| `Query` | (없음 — 공통만) |
| `Header` | **`convert_underscores`** |
| `Cookie` | (없음 — 공통만) |
| `Body` | **`embed`**, **`media_type`** |
| `Form` | **`media_type`** |
| `File` | **`media_type`** |

**`UploadFile`** [S1] — `fastapi/datastructures.py:21`, `class UploadFile(StarletteUploadFile)`. 속성 4개 (축자 Doc 포함):

| 속성 | 타입 | Doc 축자 |
|---|---|---|
| `file` | `BinaryIO` | "The standard Python file object (non-async)." |
| `filename` | `str \| None` | "The original file name." |
| `size` | `int \| None` | "The size of the file in bytes." |
| `headers` | `Headers` | "The headers of the request." |

클래스 docstring 축자 — sync 개발자에게 중요한 문장:
> If you are using a regular `def` function, you can use the `upload_file.file` attribute to access the raw standard Python file (blocking, not async), useful and needed for non-async code.

공식 예제 축자 (`bytes` + `File()` vs `UploadFile` 대비):
```python
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

- `regex`는 아직 시그니처에 있으나 **deprecated** — `pattern`으로 대체됨 (릴리스 노트 `0.100.0` 항목: `"The parameter regex has been deprecated and replaced by pattern"` [S2]).
- `Header(convert_underscores=True)`가 기본값. **0.136.3(2026-05-23)에서 동작이 바뀌었다** — `convert_underscores=True`일 때 언더스코어 헤더를 더 이상 받지 않는다 [S2].

### 1-5. `Depends` — `scope` 파라미터가 새로 생겼다 ⭐ [S1]

```python
def Depends(
    dependency: Callable[..., Any] | None = None,
    *,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any:
```

`Security(dependency, scopes, use_cache)`.

`use_cache` 축자 설명:
> "By default, after a dependency is called the first time in a request, if the dependency is declared again for the rest of the request (for example if the dependency is needed by several dependencies), the value will be re-used for the rest of the request."

**`scope`는 이 책의 핵심 소재다.** `yield` 의존성의 정리 코드가 *언제* 도는지를 결정한다. 축자:

> * `"function"`: start the dependency before the *path operation function* that handles the request, end the dependency after the *path operation function* ends, but **before** the response is sent back to the client. So, the dependency function will be executed **around** the *path operation function*.
> * `"request"`: start the dependency before the *path operation function* that handles the request (similar to when using `"function"`), but end **after** the response is sent back to the client. So, the dependency function will be executed **around** the **request** and response cycle.

문서: `https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope`

→ Spring의 `@Transactional` 경계 / OSIV(Open Session In View) 논쟁과 **정확히 대응**하는 개념이다. 책에서 비교 설명하기 좋은 지점.

### 1-5b. `dependency_overrides` (테스트용) ✅ [S1]

`applications.py:967-984` 축자 — 타입과 문서 모두 확인:

```python
self.dependency_overrides: dict[Callable[..., Any], Callable[..., Any]] = {}
```

Doc 축자:
> A dictionary with overrides for the dependencies.
> Each key is the original dependency callable, and the value is the actual dependency that should be called.
> This is for testing, to replace expensive dependencies with testing versions.

문서: `https://fastapi.tiangolo.com/advanced/testing-dependencies/`

→ `app.dependency_overrides[get_db] = get_test_db` 패턴 **실재 확인** ✅. 앱 인스턴스에 붙는 평범한 dict이므로 테스트 후 `.clear()`로 되돌리는 게 관례. (내부적으로 `APIRouter(dependency_overrides_provider=self)`로 라우터에 전달된다 — `applications.py:986` 부근.)

### 1-6. `strict_content_type` — 0.132.0 파괴적 변경 (CSRF) ⭐ [S1][S2]

`FastAPI.__init__` 축자 문서(`applications.py:840~`):

> Enable strict checking for request Content-Type headers.
> When `True` (the default), requests with a body that do not include a `Content-Type` header will **not** be parsed as JSON.
> This prevents potential cross-site request forgery (CSRF) attacks that exploit the browser's ability to send requests without a Content-Type header, bypassing CORS preflight checks. In particular applicable for apps that need to be run locally (in localhost).

릴리스 노트 0.132.0 축자 [S2]:
> Now FastAPI checks, by default, that JSON requests have a `Content-Type` header with a valid JSON value, like `application/json`, and rejects requests that don't. If the clients for your app don't send a valid `Content-Type` header you can disable this with `strict_content_type=False`.

문서: `https://fastapi.tiangolo.com/advanced/strict-content-type/`

### 1-7. lifespan vs `on_event` [S1]

`FastAPI.on_event`는 **`@deprecated` 데코레이터가 실제로 붙어 있다** (`applications.py:4655`, AST로 확인):

```
decorator: deprecated('\n        on_event is deprecated, use lifespan event handlers instead...')
```

docstring 축자:
> `on_event` is deprecated, use `lifespan` event handlers instead.

→ **`@app.on_event("startup")` → lifespan 마이그레이션은 확정 사실이다.** ✅ (다만 FastAPI에서는 아직 *제거*되지 않음 — Starlette에서는 제거됨, 3-1 참조)

### 1-8. OpenAPI 버전 = 3.1.0 [S1]

`applications.py:893-923` 축자:

```python
self.openapi_version: Annotated[str, Doc("""...FastAPI will generate OpenAPI version 3.1.0...""")] = "3.1.0"
```

→ **OpenAPI 3.1.0 확정** ✅. 오버라이드 예시도 docstring에 있다: `app.openapi_version = "3.0.2"`.

기본 URL 파라미터: `openapi_url`, `docs_url`, `redoc_url`, `swagger_ui_oauth2_redirect_url`, `swagger_ui_parameters`, `openapi_tags`, `openapi_external_docs` — 전부 `__init__`에 실재 ✅.

### 1-8b. `response_model` vs 반환 타입 어노테이션 ✅ [S14]

공식 문서 `tutorial/response-model.md` (태그 0.140.0) 축자. 문서 제목 자체가 **"Response Model - Return Type"** — 즉 **반환 타입 어노테이션이 1순위 방식**이다.

> You can declare the type used for the response by annotating the *path operation function* **return type**.

반환 타입으로 FastAPI가 하는 일 (축자 목록):
> * **Validate** the returned data. ... it means that *your* app code is broken ... and it will return a server error instead of returning incorrect data.
> * Add a **JSON Schema** for the response, in the OpenAPI *path operation*.
> * **Serialize** the returned data to JSON using Pydantic, which is written in **Rust**, so it will be **much faster**.
> But most importantly:
> * It will **limit and filter** the output data to what is defined in the return type.
>     * This is particularly important for **security**.

`response_model`을 언제 쓰는가 (축자):
> There are some cases where you need or want to return some data that is not exactly what the type declares. For example, you could want to **return a dictionary** or a database object, but **declare it as a Pydantic model**.
> If you added the return type annotation, tools and editors would complain with a (correct) error ... In those cases, you can use the *path operation decorator* parameter `response_model` instead of the return type.

주의 축자:
> Notice that `response_model` is a parameter of the "decorator" method (`get`, `post`, etc). Not of your *path operation function*.

팁 축자:
> If you have strict type checks in your editor, mypy, etc, you can declare the function return type as `Any`. That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data documentation, validation, filtering, etc. with the `response_model`.

→ **정리: 반환 타입 어노테이션이 기본, 반환 실물과 선언이 다를 때만 `response_model`.** "출력 필터링은 보안 기능"이라는 프레이밍은 Spring의 DTO 분리 논의와 직결되는 좋은 소재다. 응답 검증 실패는 **500**(`ResponseValidationError`, §1-9)이라는 점도 여기서 이어 설명할 수 있다.

### 1-9. 예외 처리 [S1]

`fastapi/exceptions.py` (256줄)에 `HTTPException`, `RequestValidationError`, `WebSocketRequestValidationError`, `ResponseValidationError`, `ValidationException`, `FastAPIError` 존재.

- `@app.exception_handler(exc_class_or_status_code)` — 파라미터 이름 축자 확인 ✅
- `ResponseValidationError`는 `routing.py:322`에서 응답 모델 검증 실패 시 발생 — **요청 검증 실패(422)와 다르게 500이 난다**. 실무 함정으로 좋은 소재.

### 1-10. 미들웨어 [S1]

- `@app.middleware(middleware_type)` — 파라미터 이름은 `middleware_type` ("http") ✅
- `FastAPI.__init__(middleware=[...])`로도 주입 가능
- Starlette `BaseHTTPMiddleware`는 `1.3.1`에도 존재 (`starlette/middleware/base.py:96`), 시그니처 `__init__(self, app: ASGIApp, dispatch: DispatchFunction | None = None)`

### 1-11. 신규 기능 (2026년, 대부분의 블로그에 없음) ⭐ [S2]

| 버전 | 날짜 | 기능 |
|---|---|---|
| `0.130.0` | 2026-02-22 | Pydantic(Rust)으로 JSON 응답 직렬화 — 축자: *"This results in 2x (or more) performance increase for JSON responses."* |
| `0.134.0` | 2026-02-27 | `yield`로 JSON Lines·바이너리 스트리밍. Starlette 하한을 `>=0.40.0`→`>=0.46.0`로 올림 |
| `0.135.0` | 2026-03-01 | **Server-Sent Events (SSE) 정식 지원** — `/tutorial/server-sent-events/` |
| `0.136.0` | 2026-04-16 | **free-threaded Python 3.14t 지원** (PR #15149) |
| `0.137.2` | 2026-06-18 | `iter_route_contexts()` 추가 |
| `0.138.0` | 2026-06-20 | `app.frontend("/", directory="dist")` — *(B조 배포 축에 가까움, 참고만)* |
| `0.140.0` | 2026-07-24 | 의존성 메모리 사용량 감소 (PR #16049) |

---

## 2. 비동기 모델 (ASGI / asyncio / 스레드풀)

### 2-1. sync `def` 경로 함수는 어떻게 오프로드되는가 — 소스로 추적 [S1][S3][S4]

체인을 끝까지 따라갔다:

**① FastAPI** `fastapi/routing.py:349-352` 축자:
```python
if is_coroutine:
    return await dependant.call(**values)
else:
    return await run_in_threadpool(dependant.call, **values)
```

**② Starlette** `starlette/concurrency.py:32-34` 축자 (태그 1.3.1):
```python
async def run_in_threadpool(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    func = functools.partial(func, *args, **kwargs)
    return await anyio.to_thread.run_sync(func)
```
→ `limiter` 인자를 넘기지 않는다 = **기본 limiter 사용**.

**③ anyio** `to_thread.run_sync(func, *args, abandon_on_cancel=False, cancellable=None, limiter=None)`. `limiter=None`이면 기본값 사용.

**④ 기본 limiter의 실제 토큰 수** — `anyio/_backends/_asyncio.py:3092-3099` 축자 (태그 4.14.2):
```python
@classmethod
def current_default_thread_limiter(cls) -> CapacityLimiter:
    try:
        return _default_thread_limiter.get()
    except LookupError:
        limiter = CapacityLimiter(40)
        _default_thread_limiter.set(limiter)
        return limiter
```

> ✅ **결론: 기본 스레드풀 크기 = 40. anyio 4.14.2 / 2026 기준, 소스 라인까지 확인.**
> 조정 방법: `anyio.to_thread.current_default_thread_limiter().total_tokens = N`

**세터 실재 검증** (추론이 아니라 확인) — `_asyncio.py:2068-2080` 축자:
```python
@property
def total_tokens(self) -> float:
    return self._total_tokens

@total_tokens.setter
def total_tokens(self, value: float) -> None:
    ...
    raise TypeError("total_tokens must be an int or math.inf")
    ...
    raise ValueError("total_tokens must be >= 0")
    waiters_to_notify = max(value - self._total_tokens, 0)
    self._total_tokens = value
```
→ `@total_tokens.setter`가 line 2071에 실재하므로 위 조정 레시피는 유효하다 ✅. 값은 `int` 또는 `math.inf`여야 하고 `>= 0`이어야 한다. 값을 **올리면** 대기 중이던 작업이 그만큼 즉시 깨어난다(`waiters_to_notify`).

**이 40이라는 숫자는 인터넷에서 가장 많이 반복되는 FastAPI 주장이라 오히려 의심했는데, Starlette 1.0 전환 이후에도 그대로 유지되고 있음을 확인했다.**

### 2-2. `Depends`도 같은 규칙을 따르는가 → 그렇다 [S1]

`fastapi/dependencies/utils.py:713-716` 축자:
```python
elif _is_coroutine_callable(use_sub_dependant.call):
    solved = await call(**solved_result.values)
else:
    solved = await run_in_threadpool(call, **solved_result.values)
```

→ **sync 의존성도 동일한 40-스레드 풀로 오프로드된다.** ✅ 같은 풀을 공유하므로 경로 함수 + 의존성이 함께 소진한다는 점이 실무 함정.

### 2-3. sync `yield` 의존성의 숨은 위험 ⭐ [S1]

`fastapi/concurrency.py:17-41` 축자 — 주석이 이 책에 그대로 인용할 가치가 있다:

```python
@asynccontextmanager
async def contextmanager_in_threadpool(cm: AbstractContextManager[_T]) -> AsyncGenerator[_T, None]:
    # blocking __exit__ from running waiting on a free thread
    # can create race conditions/deadlocks if the context manager itself
    # has its own internal pool (e.g. a database connection pool)
    # to avoid this we let __exit__ run without a capacity limit
    # since we're creating a new limiter for each call, any non-zero limit
    # works (1 is arbitrary)
    exit_limiter = CapacityLimiter(1)
```

→ **정리 코드(`__exit__`)는 일부러 40-토큰 제한 밖에서 돈다.** 이유: DB 커넥션 풀처럼 자체 풀을 가진 컨텍스트 매니저에서 데드락이 나기 때문. 이건 Spring 개발자에게 설명하기 아주 좋은 "왜 프레임워크가 이렇게 생겼나" 소재다.

또한 `0.135.1`(2026-03-01) 수정 사항 [S2]:
> 🐛 Fix, avoid yield from a TaskGroup, only as an async context manager, closed in the request async exit stack.

### 2-4. 응답 모델 검증도 스레드풀로 간다 [S1]

`routing.py:313-319` 축자 — sync 검증 경로일 때 `await run_in_threadpool(field.validate, ...)`. 큰 응답 모델 검증이 스레드풀을 점유할 수 있다는 뜻.

### 2-5. uvicorn 동시성 튜닝 플래그 (실재 확인된 것만) [S5]

`uvicorn/main.py`에서 축자 확인 (태그 0.51.0):

| 플래그 | 기본값 | help 축자 |
|---|---|---|
| `--workers` | `None` | "Number of worker processes. Defaults to the $WEB_CONCURRENCY environment..." |
| `--loop` | `"auto"` | "Event loop factory implementation." |
| `--http` | `"auto"` | "HTTP protocol implementation." |
| `--limit-concurrency` | `None` | "Maximum number of concurrent connections or tasks to allow, before issuing HTTP 503 responses." |
| `--backlog` | `2048` | "Maximum number of connections to hold in backlog" |
| `--limit-max-requests` | `None` | "Maximum number of requests to service before terminating the process." |
| `--timeout-keep-alive` | `5` | "Close Keep-Alive connections if no new data is received within this timeout (in seconds)." |
| `--timeout-graceful-shutdown` | `None` | "Maximum number of seconds to wait for graceful shutdown." |

선택지 (`uvicorn/config.py`):
- `LoopFactoryType = Literal["none", "auto", "asyncio", "uvloop"]` (line 41) → **`--loop uvloop` 실재** ✅
- `HTTP_PROTOCOLS = {"auto", "h11", "httptools"}` (line 52) → **`--http httptools` 실재** ✅
- `WS_PROTOCOLS = {"auto", "none", "websockets", "websockets-sansio", "wsproto"}` (line 57)

→ **`--limit-concurrency`가 backpressure의 정답이다** (503 반환). Spring의 스레드풀 큐 포화 대비 설명으로 좋다.

### 2-6. free-threading (PEP 703 / no-GIL) 현황 [S6][S2]

**1차 소스로 확인된 사실만:**

- **PEP 703** "Making the Global Interpreter Lock Optional in CPython" — status: **Final**, python_version: **3.13**, created 2023-01-09 [S6]
- **PEP 779** "Criteria for supported status for free-threaded Python" — status: **Final**, python_version: **3.14**, created 2025-03-13 [S6]
- **FastAPI 0.136.0 (2026-04-16)**: "⬆️ Support free-threaded Python 3.14t. PR #15149" [S2]

→ 즉 free-threaded 빌드는 3.13에서 실험적으로 도입(PEP 703), **3.14에서 "supported" 지위 기준이 확정(PEP 779)**, 그리고 FastAPI는 2026년 4월에 3.14t를 공식 지원하기 시작했다.

⚠️ **미확인** — 3.15+에서 free-threaded가 *기본* 빌드가 되는지, GIL 빌드가 언제 제거되는지는 확인하지 못했다. 책에서 이 부분은 단정하지 말 것. (참고: PEP 788 "Protecting the C API from Interpreter Finalization", Final, 3.15 — 관련은 있으나 GIL 기본값 결정과 직접 연결되는지 확인 못 함.)

⚠️ **미확인** — free-threading이 위 40-스레드 풀 모델의 성능 특성을 실제로 얼마나 바꾸는지에 대한 1차 벤치마크는 찾지 못했다. 추측 금지.

---

## 3. 폐기·마이그레이션 함정 ⭐ (이 책의 차별점)

> 지시서에 열거된 항목을 **하나씩 1차 소스로 검증**했다. 판정: ✅ 확인 / ❌ 사실과 다름 / ⚠️ 미확인

### 3-1. `@app.on_event` → lifespan ✅ (단, 중요한 층위 차이)

- **FastAPI 0.140.0**: `on_event`에 `@deprecated` 데코레이터 실재. `on_startup`/`on_shutdown` 파라미터도 **여전히 존재**. [S1]
- **Starlette 1.0.0rc1 (2026-02-23)**: 축자 [S7] —
  > Remove `on_startup` and `on_shutdown` parameters from `Starlette` and `Router`. Use the `lifespan` parameter instead (#3117).
  > Remove `on_event()` decorator from `Starlette` and `Router`. Use the `lifespan` parameter instead (#3117).
  > Remove `add_event_handler()` method from `Starlette` and `Router` (#3117).
  > Remove `startup()` and `shutdown()` methods from `Router` (#3117).
  > Remove `@app.route()` decorator from `Starlette` and `Router`. Use `Route` in the `routes` parameter instead (#3117).

→ **Starlette에서는 제거됨, FastAPI에서는 deprecated 상태로 유지.** 책에서 이 구분을 정확히 써야 한다. "FastAPI에서 제거됐다"고 쓰면 오류다.

### 3-2. Pydantic v1 → v2 이름 변경 — 전부 ✅ [S8]

`pydantic/pydantic` `v2.13.4` `docs/migration.md`에서 축자 확인:

| v1 | v2 | 판정 |
|---|---|---|
| `.dict()` | `model_dump()` | ✅ (migration.md:142) |
| `.json()` | `model_dump_json()` | ✅ (:144) |
| `parse_obj()` | `model_validate()` | ✅ (:145) |
| `orm_mode` | `from_attributes` | ✅ (:352) |
| `@validator` | `@field_validator` | ✅ (:362) "has been deprecated, and should be replaced with" |
| `@root_validator` | `@model_validator` | ✅ (:396) |
| `class Config` | `model_config = ConfigDict(...)` | ✅ (:356 ConfigDict API 참조) |
| `pydantic.BaseSettings` | `pydantic_settings.BaseSettings` | ✅ (:826 "`BaseSettings` has moved to `pydantic-settings`", :941 표) |

추가 확인 사항:
- `parse_raw`/`parse_file`도 deprecated. 축자(:149): *"In Pydantic V2, `model_validate_json` works like `parse_raw`."*
- `from_orm` deprecated → `model_validate` + `from_attributes=True` (:150-151)
- `allow_mutation` **제거됨** → `frozen` 사용 (역방향) (:331)
- `@field_validator`에는 `each_item` 인자가 **없다** (:364)
- `@model_validator`는 dict가 아니라 **모델 인스턴스**를 받는다 (:399)

**그리고 FastAPI 쪽 타임라인** [S2] — 이게 더 중요하다:
- `0.126.0` (2025-12-20): Pydantic v1 지원 중단, `pydantic >=2.7.0` 최소. `standard`에 `pydantic-settings >=2.0.0` 포함
- `0.127.0`: `pydantic.v1` 사용 시 deprecation 경고
- `0.128.0`: **`pydantic.v1` 지원 완전 제거** (PR #14609)
- `0.135.2` (2026-03-23): 최소 버전 `pydantic >=2.9.0`으로 상향

→ **FastAPI 0.128.0 이후 Pydantic v1은 어떤 형태로도 못 쓴다.** v1 문법이 든 예제는 전부 폐기 대상.

### 3-3. `Annotated` 스타일 ✅ [S9]

FastAPI 공식 튜토리얼 `query-params-str-validations.md` (태그 0.140.0) 축자:

> FastAPI added support for `Annotated` (and started recommending it) in version 0.95.0.

> Previous versions of FastAPI (before 0.95.0) required you to use `Query` as the default value of your parameter, instead of putting it in `Annotated`, there's a high chance that you will see code using it around, so I'll explain it to you.

> For new code and whenever possible, use `Annotated` as explained above. There are multiple advantages (explained below) and no disadvantages. 🍰

함정 축자:
> Keep in mind that when using `Query` inside of `Annotated` you cannot use the `default` parameter for `Query`.

즉 `q: Annotated[str, Query(default="rick")] = "morty"` 는 금지, `q: Annotated[str, Query()] = "rick"` 이 맞다.

→ **`Annotated`가 현재 권장 방식 확정** ✅. 구식 `q: str = Query(None)`은 동작은 하지만 비권장.

### 3-4. TestClient — requests → httpx → **httpx2** ⭐⭐ [S10][S11]

지시서의 "httpx 기반으로 바뀐 것"은 **이미 한 세대 낡았다.** Starlette 1.3.1 `starlette/testclient.py:33-52` 축자:

```python
if TYPE_CHECKING:
    import httpx2 as httpx
else:
    try:
        import httpx2 as httpx
    except ModuleNotFoundError:
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

- `class TestClient(httpx.Client)` (`testclient.py:376`) — 여전히 httpx 계열 Client 상속 ✅
- **`httpx2` 2.9.1**, PyPI 등록 2026-07-24, requires_python `>=3.10`, summary "The next generation HTTP client." [S11]
- FastAPI도 따라갔다: `0.137.x` 릴리스 노트에 *"✅ Add `httpx2` test dependency to avoid deprecation warning. PR #15603"* [S2]

→ **책의 테스트 장은 `httpx2`를 전제해야 한다.** `pip install httpx`만 쓴 예제는 `StarletteDeprecationWarning`을 낸다.

**httpx2는 무엇인가 — Pydantic이 인수했다** ⭐ [S11]

httpx2 저장소는 `github.com/encode/httpx2`가 아니라 **`github.com/pydantic/httpx2`**다. README 축자:

> HTTPX2 is a continuation of the wonderful work started by [@lovelydinosaur](https://github.com/lovelydinosaur) and the broader HTTPX community. ... With HTTPX itself seeing limited activity recently, **Pydantic is picking up stewardship under the HTTPX2 name** so that users have a reliably maintained path forward - including timely security updates for a library that sits in the critical path of so many production systems. Our aim is to honour the original project's design, keep it stable for everyone relying on it, and continue evolving it carefully.

(참고로 `lovelydinosaur`는 Starlette 1.0 릴리스 노트에서 *"The original creator of Starlette, Uvicorn, and MkDocs, and the current maintainer of HTTPX"*로 소개된 인물이다 [S7]. httpx 정체 → Pydantic 승계라는 서사가 1차 소스로 연결된다.)

**async 테스트 API — 해소됨 ✅** (sdist `httpx2-2.9.1` 직접 검사)

- `httpx2/__init__.py`가 `"ASGITransport"`, `"WSGITransport"`를 `__all__`로 export ✅
- `httpx2/_client.py:1407`에 `class AsyncClient(BaseClient)` ✅
- `httpx2/_transports/asgi.py` 축자 시그니처:

```python
class ASGITransport(AsyncBaseTransport):
    def __init__(
        self,
        app: _ASGIApp,
        raise_app_exceptions: bool = True,
        root_path: str = "",
        client: tuple[str, int] = ("127.0.0.1", 123),
    ) -> None:
```

docstring 축자 예제:
```python
transport = httpx2.ASGITransport(
    app=app,
    root_path="/submount",
    client=("1.2.3.4", 123)
)
client = httpx2.AsyncClient(transport=transport)
```

→ **`ASGITransport` + `AsyncClient` 패턴은 `httpx2`에서 이름·시그니처가 동일하다.** import만 `httpx` → `httpx2`로 바꾸면 된다 ✅ (2.9.1 / 2026 기준)

### 3-5. FastAPI 최근 파괴적 변경 전수 (릴리스 노트 `### Breaking Changes` 전량) [S2]

날짜는 릴리스 노트의 버전 헤더(`## {version} ({date})`)에서 **직접 추출**했다. 추정 없음.

| 버전 | 날짜 (릴리스 노트 헤더) | 파괴적 변경 축자 |
|---|---|---|
| `0.125.0` | **2025-12-17** | "Drop support for Python 3.8" (#14563). 단서 축자: *"This would actually not be a breaking change as no code would really break... Only marking it as a 'breaking change' to make it visible."* |
| `0.126.0` | **2025-12-20** | Pydantic v1 지원 중단, `pydantic >=2.7.0` 최소 (#14575) |
| `0.127.0` | **2025-12-21** | "Add deprecation warnings when using `pydantic.v1`" (#14583) |
| `0.128.0` | **2025-12-27** | **"Drop support for `pydantic.v1`"** (#14609) |
| `0.129.0` | **2026-02-12** | **"Drop support for Python 3.9"** (#14897) |
| `0.130.0` | **2026-02-22** | (Features) Pydantic(Rust) JSON 직렬화, 2x 이상 |
| `0.131.0` | **2026-02-22** | **"Deprecate `ORJSONResponse` and `UJSONResponse`"** (#14964) |
| `0.132.0` | **2026-02-23** | **"Add `strict_content_type` checking for JSON requests"** (#14978) |
| `0.133.0` | **2026-02-24** | (Upgrades) "Add support for Starlette 1.0.0+" (#14987) |
| `0.136.0` | **2026-04-16** | (Upgrades) "Support free-threaded Python 3.14t" (#15149) |
| `0.137.0` | **2026-06-14** | **"Refactor internals to preserve `APIRouter` and `APIRoute` instances"** (#15745) |
| `0.140.0` | **2026-07-24** | (Refactors) 의존성 메모리 사용량 감소 (#16049) |

> 📌 **정합성 메모 (fact-checker용):** 릴리스 노트 헤더 날짜와 GitHub Releases의 `published_at`이 일부 릴리스에서 어긋난다. 예: `0.135.2`는 릴리스 노트 헤더가 `2026-03-01`인데 GitHub API `published_at`은 `2026-03-23T14:11:42Z`다. **위 표는 릴리스 노트 헤더 기준**, §4의 이정표 표는 GitHub `published_at` 기준이다. 책에 날짜를 쓸 때는 어느 기준인지 통일할 것. 굳이 하나만 쓴다면 **릴리스 노트 헤더**를 권한다(공식 문서에 인쇄되는 날짜).

`requires_python`은 현재 **`>=3.10`** (PyPI, 2026-07-25 조회) [S12].

### 3-6. `0.137.0` 파괴적 변경 전문 ⭐ [S2]

이번 조사에서 가장 중요한 발견. 릴리스 노트 축자 (`release-notes.md:222-242`):

> Before this, `router.include_router(other_router)` would take each path operation from `other_router` and "clone" it, or recreate it from scratch. This would mean that in the end there was only one top level router, part of the app.
>
> The way it is structured here is that there are a few additional classes to handle intermediate metadata for router and route inclusion. That way the information of "router X includes Y and Y includes Z" is stored somewhere, without affecting (recreating / cloning) the final route.
>
> **#### Non Objectives**
> Dependencies for 404: previously I intended to support dependencies that would be executed even for 404, but that would conflict with the fact that a router could _not_ find a match, but the next router _did_ find a match. Executing dependencies in the router that did not find a match would not make sense, they could consume the request, body, etc. This original idea was discarded.
>
> **#### Specific Breaking Changes**
> Now `router.routes` is no longer a plain list of `APIRoute` objects, it can contain these intermediate objects that can contain additional routers, forming a tree.
>
> Any logic that depended on iterating on the `router.routes` directly would be affected, that logic cannot expect to be able to extract data from a plain list of routes, as it's no longer a plain list but a tree.

→ **`app.routes`를 순회하는 모든 코드(메트릭 수집, 라우트 감사, 커스텀 OpenAPI 생성 등)가 깨진다.**

**대체 API — 시그니처 확인됨 ✅** [S1] `fastapi/routing.py:1821`:
```python
def iter_route_contexts(
    routes: Sequence[BaseRoute | RouteContext],
) -> Iterator[RouteContext]:
```
`RouteContext`는 dataclass (`routing.py:1538`)로 `route: BaseRoute` 필드와 `original_route` 프로퍼티를 가진다. 도입: `0.137.2` (2026-06-18), PR #15785 — 축자: *"Add `iter_route_contexts()` for advanced use cases that used to use `router.routes` (e.g. Jupyverse)"* [S2].

즉 트리를 평탄화해 순회하려면 `for ctx in iter_route_contexts(app.routes): ...` 형태로 바꿔야 한다.

이건 실무 심층서에 딱 맞는 소재다. 인터넷의 "라우트 전부 순회해서 X 하기" 레시피가 전부 깨진 상태.

### 3-7. 기타 폐기 항목 [S2]

- **`ORJSONResponse` / `UJSONResponse` deprecated** (`0.131.0`). 배경: `0.130.0`에서 Pydantic(Rust) 직렬화로 기본 JSON이 2배 이상 빨라졌기 때문. → **"성능을 위해 ORJSONResponse를 쓰라"는 조언은 이제 낡았다.**
- **`fastapi.middleware.wsgi.WSGIMiddleware` deprecated** → `a2wsgi`의 `WSGIMiddleware` 사용 (PR #14756)
- **`fastapi-slim` 패키지 폐지** — 축자: *"Drop support for `fastapi-slim`, no more versions will be released, use only `"fastapi[standard]"` or `fastapi`"* (`0.129.2`). 스텁도 `0.137.x`에서 제거 (PR #15649)
- **`openapi_prefix`** deprecated → `root_path`
- **`regex`** deprecated → `pattern`
- Starlette 1.0: `run_until_first_complete`도 deprecated (`starlette/concurrency.py:16-20`, `StarletteDeprecationWarning`) [S3]

---

## 4. 확인된 버전 정보 (릴리스 URL + 조회일 필수)

전부 **2026-07-25 조회**. 각 항목은 릴리스 특정 URL을 가진다.

| 패키지 | 버전 | 배포일 | requires_python | 근거 URL |
|---|---|---|---|---|
| **fastapi** | **0.140.0** | 2026-07-24 | `>=3.10` | `https://github.com/fastapi/fastapi/releases/tag/0.140.0` / `https://pypi.org/pypi/fastapi/json` |
| **starlette** | **1.3.1** | 2026-06-12 | `>=3.10` | `https://pypi.org/pypi/starlette/json` |
| **pydantic** | **2.13.4** | 2026-05-06 | `>=3.9` | `https://pypi.org/pypi/pydantic/json` |
| **uvicorn** | **0.51.0** | 2026-07-08 | `>=3.10` | `https://pypi.org/pypi/uvicorn/json` |
| **anyio** | **4.14.2** | 2026-07-12 | `>=3.10` | `https://pypi.org/pypi/anyio/json` |
| **pydantic-settings** | **2.14.2** | 2026-06-19 | `>=3.10` | `https://pypi.org/pypi/pydantic-settings/json` |
| **httpx2** | **2.9.1** | 2026-07-24 | `>=3.10` | `https://pypi.org/pypi/httpx2/json` |
| **httpx** (구) | 0.28.1 | 2024-12-06 | `>=3.8` | `https://pypi.org/pypi/httpx/json` |

**이정표 릴리스:**

| 사건 | 버전/날짜 | URL |
|---|---|---|
| Starlette 1.0 정식 출시 | 1.0.0, 2026-03-22 | `https://github.com/encode/starlette/blob/1.3.1/docs/release-notes.md` (`## 1.0.0 (March 22, 2026)`) |
| Starlette 1.0rc1 (폐기 항목 제거) | 1.0.0rc1, 2026-02-23 | 동상 (`## 1.0.0rc1 (February 23, 2026)`) |
| FastAPI가 Starlette 1.0+ 지원 | 0.133.0, 2026-02-24 | `https://github.com/fastapi/fastapi/releases/tag/0.133.0` |
| FastAPI free-threaded 3.14t 지원 | 0.136.0, 2026-04-16 | `https://github.com/fastapi/fastapi/releases/tag/0.136.0` |
| FastAPI 라우터 트리 파괴적 변경 | 0.137.0, 2026-06-14 | `https://github.com/fastapi/fastapi/releases/tag/0.137.0` |
| SSE 지원 | 0.135.0, 2026-03-01 | `https://github.com/fastapi/fastapi/releases/tag/0.135.0` |
| Pydantic-Rust JSON 직렬화 (2x) | 0.130.0, 2026-02-22 | `https://github.com/fastapi/fastapi/releases/tag/0.130.0` |
| `strict_content_type` | 0.132.0, 2026-02 | `https://github.com/fastapi/fastapi/releases/tag/0.132.0` |

**버전 민감 서술 표기 권고:** 이 책의 모든 코드 예제는 **"FastAPI 0.140.0 / Starlette 1.3.1 / Pydantic 2.13.4 / 2026년 7월 기준"**으로 못 박을 것. 특히 3장 항목들은 6개월 뒤 다시 검증해야 한다.

---

## 5. 미확인·공백 (⚠️)

**해소된 항목** (초안에서 ⚠️였다가 1차 소스로 확인됨): httpx2 async 테스트 API(§3-4) / `dependency_overrides`(§1-5b) / `iter_route_contexts()` 시그니처(§3-6) / `total_tokens` 세터(§2-1) / `UploadFile`(§1-4) / `response_model` vs 반환 어노테이션(§1-8b). 이제 전부 ✅다.

**남은 공백:**

1. ⚠️ **ASGI 스펙 문서 자체** (`asgi.readthedocs.io`) — **지시서 2번 축이 명시적으로 요구한 1차 소스인데 이번에 fetch하지 않았다.** 누락이지 "해당 없음"이 아니다. 스펙 버전, HTTP/WebSocket `scope` 딕셔너리 구조, `receive`/`send` 콜러블 계약을 인용하려면 **추가 조사가 필요하다.** (다만 Starlette가 그 스펙의 구현체라는 점은 §2-1 체인으로 실증했다.)
2. ⚠️ **free-threading의 기본값 전환 시점** — 3.15+에서 free-threaded가 기본 빌드가 되는지, GIL 빌드 제거 로드맵은 확인 못 함. **단정 금지.**
3. ⚠️ **free-threading × FastAPI 성능 벤치마크** — 40-스레드 풀 모델이 no-GIL에서 어떻게 달라지는지 1차 측정 자료 미확보. 추측 금지.
4. ⚠️ **`BaseHTTPMiddleware`의 알려진 한계** — 클래스가 1.3.1에도 존재하고 시그니처도 확인했으나, "스트리밍 응답에서 배압이 깨진다" 류의 구체적 한계는 1차 소스로 검증하지 못했다. GitHub Issue 조사 필요 (C조 커뮤니티 담당과 겹칠 수 있음).
5. ⚠️ **Starlette 1.0 전환기 블로그** — `https://marcelotryle.com/blog/2026/03/22/starlette-10-is-here/` (메인테이너 본인 글, Starlette 1.0.0 릴리스 노트에서 링크됨 [S7])를 fetch하지 않았다. 1.0이 왜 지금인지에 대한 인용 가능한 서술이 필요하면 여기가 최적. 발행일 2026-03-22, 신뢰성 최상(메인테이너 1차).
6. ⚠️ **`0.137.0` 파괴적 변경의 실제 영향 범위** — `iter_route_contexts()` 시그니처는 확인했으나, 기존 `app.routes` 순회 코드가 구체적으로 어떤 라이브러리(예: prometheus-fastapi-instrumentator)에서 깨졌는지는 조사하지 않았다. C조 커뮤니티 축에서 보강 가능.

---

## 6. 출처 목록 (URL + 발행일 + 조회일 + 신뢰성)

전 항목 **조회일 2026-07-25**.

### [S1] FastAPI 소스 코드 (태그 0.140.0)
- 출처: `https://github.com/fastapi/fastapi/tree/0.140.0/fastapi` (raw: `raw.githubusercontent.com/fastapi/fastapi/0.140.0/fastapi/{applications,routing,param_functions,concurrency,exceptions,datastructures}.py`, `fastapi/dependencies/utils.py`)
- 저자·날짜: Sebastián Ramírez(tiangolo) 외 / 태그 배포 2026-07-24
- **신뢰성: 최상** (1차 소스 — 실행되는 코드 그 자체)
- 핵심: 전 API 시그니처, `Depends(scope=)`, `strict_content_type`, `on_event` deprecated, `openapi_version="3.1.0"`, sync 오프로드 경로
- 관련 섹션: 코어 API 장, 의존성 주입 장, 비동기 장

### [S2] FastAPI 공식 릴리스 노트 (태그 0.140.0, 7,228줄)
- 출처: `https://raw.githubusercontent.com/fastapi/fastapi/0.140.0/docs/en/docs/release-notes.md` / 웹: `https://fastapi.tiangolo.com/release-notes/`
- 저자·날짜: FastAPI 팀 / 최신 항목 2026-07-24
- **신뢰성: 최상** (공식 체인지로그)
- 핵심: 파괴적 변경 전수, 폐기 타임라인, 0.137.0 라우터 트리 변경 전문
- 관련 섹션: 마이그레이션 장 (이 책의 차별점)

### [S3] Starlette 소스 코드 (태그 1.3.1)
- 출처: `https://github.com/encode/starlette/tree/1.3.1/starlette` (`concurrency.py`, `testclient.py`, `middleware/base.py`, `applications.py`)
- 저자·날짜: Marcelo Trylesinski 외 / 태그 배포 2026-06-12
- **신뢰성: 최상** (1차 소스)
- 핵심: `run_in_threadpool` 구현, httpx2 전환, `BaseHTTPMiddleware` 시그니처
- 관련 섹션: 비동기 장, 테스트 장, 미들웨어 장

### [S4] anyio 소스 코드 (태그 4.14.2)
- 출처: `https://github.com/agronholm/anyio/blob/4.14.2/src/anyio/to_thread.py`, `.../src/anyio/_backends/_asyncio.py`
- 저자·날짜: Alex Grönholm / 태그 배포 2026-07-12
- **신뢰성: 최상** (1차 소스)
- 핵심: **`CapacityLimiter(40)`** (`_asyncio.py:3097`), `run_sync` 시그니처
- 관련 섹션: 비동기 장의 핵심 근거

### [S5] uvicorn 소스 코드 (태그 0.51.0)
- 출처: `https://github.com/encode/uvicorn/blob/0.51.0/uvicorn/main.py`, `.../uvicorn/config.py`
- 저자·날짜: encode 팀 / 태그 배포 2026-07-08
- **신뢰성: 최상** (1차 소스)
- 핵심: CLI 플래그 실재 여부와 기본값, loop/http 구현 선택지
- 관련 섹션: 동시성 튜닝 절

### [S6] Python PEP 인덱스 API
- 출처: `https://peps.python.org/api/peps.json` (PEP 703 / 779 / 788)
- 저자·날짜: Python Steering Council / PEP 779 created 2025-03-13
- **신뢰성: 최상** (스펙 1차 소스)
- 핵심: PEP 703 Final(3.13), PEP 779 Final(3.14) — free-threading 지위
- 관련 섹션: 비동기 장 말미 "앞으로"

### [S7] Starlette 릴리스 노트 (태그 1.3.1)
- 출처: `https://github.com/encode/starlette/blob/1.3.1/docs/release-notes.md`
- 저자·날짜: Marcelo Trylesinski / 1.0.0 = 2026-03-22, 1.0.0rc1 = 2026-02-23
- **신뢰성: 최상** (공식 체인지물)
- 핵심: `on_event`/`on_startup`/`add_event_handler`/`@app.route()` **완전 제거**
- 관련 섹션: 마이그레이션 장

### [S8] Pydantic v2 공식 마이그레이션 가이드 (태그 v2.13.4)
- 출처: `https://raw.githubusercontent.com/pydantic/pydantic/v2.13.4/docs/migration.md` / 웹: `https://docs.pydantic.dev/latest/migration/`
- 저자·날짜: Pydantic 팀 / 태그 배포 2026-05-06
- **신뢰성: 최상** (공식 문서)
- 핵심: v1→v2 이름 변경 전수 검증 (표 형태로 §3-2에 정리)
- 관련 섹션: 마이그레이션 장, 모델·검증 장

### [S9] FastAPI 공식 튜토리얼 — Query Params & String Validations (태그 0.140.0)
- 출처: `https://raw.githubusercontent.com/fastapi/fastapi/0.140.0/docs/en/docs/tutorial/query-params-str-validations.md` / 웹: `https://fastapi.tiangolo.com/tutorial/query-params-str-validations/`
- 저자·날짜: tiangolo / 태그 2026-07-24
- **신뢰성: 최상** (공식 문서)
- 핵심: `Annotated` 권장 선언 (0.95.0부터), `Query(default=)` 금지 규칙
- 관련 섹션: 파라미터 선언 장

### [S10] Starlette TestClient 소스 (태그 1.3.1) — [S3]의 부분이나 중요도상 분리
- 출처: `https://github.com/encode/starlette/blob/1.3.1/starlette/testclient.py`
- **신뢰성: 최상**
- 핵심: httpx → httpx2 전환과 `StarletteDeprecationWarning` 축자
- 관련 섹션: 테스트 장

### [S11] httpx2 — PyPI 메타데이터 + 배포 sdist 원본 + README
- 출처: `https://pypi.org/pypi/httpx2/json` / `https://github.com/pydantic/httpx2` / sdist `httpx2-2.9.1.tar.gz` (`httpx2/__init__.py`, `httpx2/_client.py`, `httpx2/_transports/asgi.py`)
- 저자·날짜: Pydantic / 2.9.1 배포 2026-07-24
- **신뢰성: 최상** (배포 레지스트리 + 배포 아티팩트 원본)
- 핵심: httpx2 실재·버전, **Pydantic의 httpx 스튜어드십 승계** 축자, `ASGITransport`/`AsyncClient` 시그니처 동일 확인
- 관련 섹션: 테스트 장, 의존성 표, 생태계 서사

### [S12] PyPI JSON API (fastapi / starlette / pydantic / uvicorn / anyio / pydantic-settings / httpx)
- 출처: `https://pypi.org/pypi/{package}/json`
- **신뢰성: 최상** (배포 레지스트리 1차)
- 핵심: §4 버전 표 전체의 근거
- 관련 섹션: 책 서두 "이 책의 기준 버전" 고지

### [S13] GitHub Releases API — fastapi
- 출처: `https://api.github.com/repos/fastapi/fastapi/releases` → 개별 `https://github.com/fastapi/fastapi/releases/tag/{version}`
- **신뢰성: 최상** (1차)
- 핵심: 릴리스별 배포 일시(ISO), §4 이정표 표
- 관련 섹션: 마이그레이션 장

### [S14] FastAPI 공식 튜토리얼 — Response Model / Return Type (태그 0.140.0)
- 출처: `https://raw.githubusercontent.com/fastapi/fastapi/0.140.0/docs/en/docs/tutorial/response-model.md` / 웹: `https://fastapi.tiangolo.com/tutorial/response-model/`
- 저자·날짜: tiangolo / 태그 2026-07-24
- **신뢰성: 최상** (공식 문서)
- 핵심: 반환 타입 어노테이션이 1순위, `response_model`은 반환 실물과 선언이 다를 때. 출력 필터링의 보안 프레이밍
- 관련 섹션: 모델·직렬화 장

---

## 수집 한계

- **접근 실패**: GitHub Releases API를 `encode/starlette`에 대해 비인증 호출했을 때 rate limit으로 실패. → `docs/release-notes.md`를 태그 고정으로 직접 받아 대체 해결. 정보 손실 없음.
- **의도적 제외**:
  - 블로그·튜토리얼·Medium·dev.to 류를 **버전 근거로는 일절 쓰지 않았다.** 2026년 상반기 변경 폭이 커서 2차 소스는 거의 전부 낡았다고 판단. 관점·경험담이 필요하면 C조(커뮤니티) 결과와 합칠 것.
  - Python 입문·REST 입문·"첫 FastAPI 앱" 류 기초 튜토리얼 (대상 독자 부적합)
  - 배포·운영·데이터 계층 (B조 담당) — `app.frontend()`만 한 줄 기록하고 전개하지 않음
- **한국어 자료 비중**: 이번 A조 축(정확한 시그니처·버전)에서는 1차 영문 소스가 유일하게 신뢰 가능해 한국어 자료를 넣지 않았다. 한국어 비중은 C조(커뮤니티) 산출물에서 확보하는 것이 정합적이다.
- **커버리지 자평**: 지시서 3개 축 중 1(코어)·3(마이그레이션)은 1차 소스로 조밀하게 채웠다. 2(비동기)는 스레드풀·오프로드 경로·uvicorn 튜닝까지 확인했으나 **ASGI 스펙 문서 자체와 free-threading 실측**이 공백이다(§5).
