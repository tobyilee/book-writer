# 사실 검증 로그 (factcheck_log.md)

> **단일 append-only 파일이다.** `factcheck_log_1.md`처럼 샤딩하지 마라 — 감사 추적이 갈라지고 누적 판정이 흩어진다.
> 챕터마다 `## {NN}장` 섹션을 **append** 한다. 기존 섹션을 지우거나 덮어쓰지 마라.
>
> **판정 기호**
> | 기호 | 뜻 | 구속력 |
> |---|---|---|
> | ✅ | 레퍼런스/1차 소스로 확인됨 | — |
> | ❌ | 사실 오류 — 정정 필요 | **BLOCKING.** 저술가 재량으로 덮을 수 없다 |
> | ⚠️ | 근거 부족 — 약화·삭제·각주 필요 | 조치 필요 |
> | 🕒 | 검증 불가 (레퍼런스에 근거 없음, 1차 소스 확인 실패) | **BLOCKING.** Phase 5 진행 차단 |
>
> **최우선 표적 (하네스에 코드 실행 단계가 없다 — 이 대조가 유일한 방어선이다):**
> 모든 코드 블록에서 **import 경로·클래스명·함수명·파라미터 이름**을 추출해 `01_reference.md` §1-2(FastAPI 0.140.0 AST 목록)·§1-6·§5-A·§5-D·버전 핀 테이블과 대조하라.
> 리서치 중 실제로 적발된 날조 2건이 정확히 이 유형이다 — oauth2-scopes의 가짜 주석, 존재하지 않는 import 경로 `fastapi_plugin.fast_api_client`.

---

## 1장

**라운드 1 · 2026-07-26 · 대조 근거:** `01_reference.md` §1-1·§1-2·§3-1·§3-2·§4-6·§7-2·§7-3·버전 핀 A/B/J, `tracker_contract.md` §8, `research/version_pins.md`, `research/web.md`

### ❌ 정정 필요 (BLOCKING)

- **[원문] (line 41) "여기서는 그 목록이 아홉 줄이라 전부 눈으로 셀 수 있다."**
  → **[정정]** "여기서는 그 목록이 아홉 개라 전부 눈으로 셀 수 있다."
  **근거:** 바로 위 인용 블록(line 34–36)은 **3줄**이고, 그 안의 패키지는 **9개**다(`fastapi-cli`·`fastar`·`httpx`·`jinja2`·`python-multipart`·`email-validator`·`uvicorn`·`pydantic-settings`·`pydantic-extra-types`). `01_reference.md` §J(line 211–218) requires_dist 원문과 대조. 숫자 9는 맞고 단위 "줄"이 틀렸다.

### ⚠️ 출처 없음

- **[원문] (line 90) "그쪽 세계에는 '메이저 버전이 아니면 깨뜨리지 않는다'는 계약이 있고, 그 계약을 신뢰하는 것을 전제로 업그레이드 정책을 짠다."**
  → 레퍼런스의 유일한 근거는 §3-2(line 644)의 **저자 해석** 한 줄("Spring Boot의 '메이저 아니면 안 깬다' 계약에 익숙한 독자에게는")이다. Spring 측 1차 근거가 아니다. 계획 제약 10이 **Spring·Node 측 사실에 각주 또는 구조 대조**를 요구한다. (저술가 자기 신고 지점)
  **정정안 (택1):** (a) Spring Boot 공식 버저닝·지원 정책 문서를 각주로 달거나, (b) 독자 경험 귀속으로 약화 — *"당신은 아마 '메이저가 아니면 깨지지 않는다'를 전제로 업그레이드 정책을 짜왔을 것이다."*

- **[원문] (line 139) uv 대응표 "락파일 그대로 재현 설치 | Maven / Gradle: — | npm: `npm ci` | uv: `uv sync --locked`"**
  → Maven/Gradle에 락파일 재현 설치가 **없다**는 단정. `01_reference.md` §7-2(line 1202)가 *"Maven/Gradle/npm vs uv/poetry **락파일**·모노레포 | ⚠️ 근거 못 찾음"*으로 이 항목을 **명시적 공백**으로 신고했다.
  **정정안:** 해당 행을 삭제하거나, Maven/Gradle 칸을 각주로 뒷받침한다. 나머지 3행(의존성 추가·명령 실행·매니페스트)은 구조 대조라 유지 가능.

- **[원문] (line 181) "실무 사고가 가장 많이 나는 자리라 가장 두껍게 썼다."**
  → **최상급 빈도 주장.** §7-3이 정량 근거 공백을 선언했고(깊은 `Depends` 오버헤드·업로드 메모리 등 "정량 없음"), 사고 빈도 통계는 레퍼런스에 없다.
  **정정안:** *"이 책이 가장 많은 지면을 쓴 자리다"* 또는 저자 판단임을 표시.

### 🕒 신선도 경고

- 없음. **버전 표기 규율 위반 0건.** 모든 버전이 `"{버전} / {연월} 기준"` 형식이고(line 31 "0.140.0 / 2026-07 기준", line 98 "2026년 7월 기준"), line 94가 *"이 문장의 기준은 FastAPI 0.140.0 / 2026-07"*로 기준 시점을 명시 선언한다. 계획 제약 3 충족.

### ✅ 확인됨

**저술가 자기 신고 ①  — 날짜 판단: 저술가가 옳다.**
- "7년이 넘었다"(line 3): ASGI 3.0 = 2019-03-20(§1-1 축자) → 2026-07 기준 **7년 4개월**. 계획의 "7년째"는 이미 지났으므로 저술가의 "7년이 넘었다"가 정확하다. ✅
- "2026년 2월부터 6월까지"(line 5): 0.129.0(2026-02-12) ~ 0.137.0(2026-06-14) = **4개월 2일**. 계획의 "지난 6개월"은 틀리고 달력 범위 서술이 정확하다. ✅ 파생 문장 "한 해의 절반도 안 되는 사이에"(line 7)도 참. 절 제목 "2026년 상반기"(line 67)도 세 릴리스가 전부 H1에 들어와 참이며 §3-1 절 제목과 일치.
- **0.128.0(`pydantic.v1` 완전 제거, 2025-12-27)을 창에서 정확히 제외**했다 — 계획 line 198의 날짜 규율 준수. ✅

**릴리스·버전 사실 (전건 §3-1·버전 핀 B 일치)**
- 0.129.0/2026-02-12 Python 3.9 중단 · 0.132.0/2026-02-23 `strict_content_type` 기본 True · 0.137.0/2026-06-14 라우터 트리 ✅ §3-1
- `strict_content_type` 릴리스 노트 축자, 0.137.0 라우터 트리 축자 — **§3-1(line 623–628)과 문자 단위 일치** ✅
- 0.135.0/2026-03 SSE 정식 지원 ✅ · 0.130.0/2026-02 Rust JSON 직렬화 + 축자 *"2x (or more) performance increase for JSON responses"* ✅ §3-1
- 버전 표(line 100–106) FastAPI 0.140.0/2026-07-24 · Starlette 1.3.1/2026-06-12 · Pydantic 2.13.4/2026-05-06 · uvicorn 0.51.0/2026-07-08 · anyio 4.14.2/2026-07-12 — **5행 전건 버전 핀 B 일치** ✅
- Starlette 1.0.0 = 2026-03-22, "창설 이래 첫 stable" ✅ 버전 핀 B(line 69)
- `requires_python >=3.10`, Python 3.10 EOL 2026-10-31, 책은 3.12+ 전제 ✅ 버전 핀 A(line 48·52)
- `starlette>=0.46.0`만 핀 / 1.x 강제 아님 ✅ §J(line 222)
- `[standard]` requires_dist 인용(line 34–36) — **§J(line 215–217)와 축자 일치** ✅, 출처·조회일 표기 ✅
- 저장소 `encode`→`Kludex` 이전을 **사실만 쓰고 경위는 "확인하지 못했다"로 명시**(line 116) ✅ §버전 핀 B(line 76)·계획 「근거 두께」 지시 정확 준수
- "공식 문서가 예제 명령을 uv 기준으로 개편"(line 133) ✅ §2-3(line 580)·§5-C(line 903) PR #16032

**ASGI 계약 (전건 §1-1 축자 일치)**
- `coroutine application(scope, receive, send)` ✅ · `scope`/`receive`/`send` 3개 축자 ✅ · scope 키 목록(§1-1 line 251의 부분집합) ✅ · WebSocket scope + 서브프로토콜 ✅ · `root_path` 축자 *"same as SCRIPT_NAME in WSGI"* ✅
- 출처 URL `https://asgi.readthedocs.io/en/latest/specs/main.html` ✅ §1-1·§6-1과 동일

**코드 API 표면 (0건 실패)** — `fastapi.FastAPI` / `FastAPI(title=)` / `@app.get(path, tags=)` ✅ §1-2 AST 목록 · `uv add`·`uv run`·`uv sync --locked` ✅ §8-1 · uvicorn `--host`·`--port` ✅ §8-1 · OpenAPI 3.1.0 ✅ §1-2 · `dict[str, str]` 표준 라이브러리 면제(계약 §8-0). **가짜 주석 0건** — 코드 주석은 파일 경로 표기와 `# (개념 설명용 — 파일 아님)`뿐이고 동작을 설명하는 주석이 없다.

**리서치 공백 준수** — Reddit·Stack Overflow 인용 **0건** ✅(grep 확인) / #14603 **미등장** ✅ / FastAPI Cloud 백래시 **미등장** ✅ / "Java 개발자는 이래서 실수한다" 류 출신 귀속 **0건** ✅ / 다루지 않는 주제(API 버저닝·캐시) 선언 + 경로에 버전 접두사 없음(line 189) ✅ 계획 일치

**양화사 점검** — "0.x라 프로덕션이 불안하다는 말"(line 110)은 §4-6이 *"0.x 유지에 대한 커뮤니티 의견 근거 못 찾음"*을 선언했으나, 버전 핀 B(line 75) 저자 해석이 이 비판을 다루도록 명시 승인했고 본문이 **독자 경험 귀속 + "판단은 여기서 내리지 않겠다"**로 처리해 다수설 일반화를 회피했다 ✅. "문제의 상당수"(line 27)·"대체로"류는 헤지된 정당한 일반 서술 — 과잉 차단하지 않는다.

**총평:** 오프닝 날짜 산술(책의 최대 위험 지점)은 **저술가의 판단이 옳고 계획이 틀렸다.** 코드 API 표면 실패 0건. 남은 것은 Spring 측 버저닝 계약 서술과 락파일 표 한 칸의 근거 보강.

---

## 2장

**라운드 1 · 2026-07-26 · 대조 근거:** `01_reference.md` §1-2·§3-1·§3-2·§4·§4-4·§7-2·§7-3·버전 핀 B/J, `tracker_contract.md` §8, `research/web.md`, `research/community.md`, `research/version_pins.md`

### ❌ 정정 필요 (BLOCKING)

- 없음.

### ⚠️ 출처 없음

- **[원문] (line 145·161) `from sqlalchemy.ext.asyncio import AsyncSession` — 각주 없음.**
  → 심볼 `AsyncSession` 자체는 계약 §8-1(SQLAlchemy 비동기 행)이 추적됨으로 분류했으나, **import 경로 문자열 `sqlalchemy.ext.asyncio`는 `01_reference.md`와 `research/*.md` 전체에 단 한 번도 나오지 않는다**(grep 0건). §1-6은 `sqlalchemy.orm` Quickstart만 싣는다. 계약 §8-2(line 613)가 `sqlalchemy.ext.asyncio.async_sessionmaker`를 **6장 소유 T1**으로 지정했지만, 이 경로를 **책에서 먼저 쓰는 것은 2장**이다. 저술가가 오늘 1차 소스로 확인했다고 보고했으나 2장의 유일한 각주(line 214)는 pydantic-settings 것이다.
  **정정안:** SQLAlchemy 2.0 asyncio 확장 문서(`https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html`) 각주 1회 추가. 계약 §8-2 절차상 "소유 장이 각주 1회로 해소"이므로 2장이 달면 6장은 각주 없이 그대로 쓴다.

- **[원문] (line 186) "그리고 이건 논쟁이 없다 — `pydantic-settings`(2.14.2 / 2026-06 기준)가 사실상의 답이다."**
  → **"논쟁이 없다"는 커뮤니티 합의 부재/존재에 대한 일반화**다. §7-2(line 1200)가 *"`application.yml` vs pydantic-settings | ⚠️ 근거 못 찾음"*을, §4(line 770)가 표집 편향을 경고한다. 계획 제약 6이 다수설 일반화를 금지한다. (버전 표기 2.14.2 / 2026-06 자체는 ✅ 버전 핀 B와 일치)
  **정정안:** 논쟁 유무 주장을 사실로 대체 — *"`pydantic-settings`는 `[standard]` extra에 이미 들어 있다(1장). 이 책은 그것을 쓴다."*

- **[원문] (line 247) "메트릭 수집기, 문서 생성기, 라우트 감사 스크립트 — 라우트 목록을 읽어야 하는 도구들은 **전부** 그 리스트를 훑고 있었다."**
  → 양화사 **"전부"**. 확보된 근거는 라이브러리 **1건**(`prometheus-fastapi-instrumentator`, §3-2)뿐이다. "문서 생성기"·"라우트 감사 스크립트"가 실제로 깨졌다는 기록은 레퍼런스에 없다.
  **정정안:** "전부" → "대개". 또는 *"라우트 목록을 읽어야 하는 도구는 그 리스트를 훑는 것 말고 방법이 없었다"*(구조적 서술로 전환).

- **[원문] (line 257) "첫 보고가 릴리스와 같은 날이고, 열흘 뒤에 또, 3주 뒤에 다시 한 번이다."**
  → 바로 위 표의 날짜로 계산하면 #370(2026-06-14) → #379(2026-06-25) = **11일**, → #388(2026-07-08) = 첫 보고 기준 **24일** / 직전 보고 기준 **13일**이다. "열흘"·"3주"는 둘 다 반올림이고 **기준점이 첫 보고인지 직전 보고인지 문장에서 갈린다** — 직전 보고 기준으로 읽으면 "3주"가 틀린다.
  **정정안:** *"첫 보고가 릴리스와 같은 날이고, 열하루 뒤에 또, 첫 보고로부터 3주가 지나 다시 한 번이다."*
  **라벨 주기:** 이 항목은 **⚠️(정정안 있음)이지 🕒이 아니다.** 날짜는 §3-2로 이미 검증됐고 산술만 부정확하다 — 로그 헤더가 정의한 🕒("검증 불가")에 해당하지 않으므로 **Phase 5를 차단하지 않는다.**

### 🕒 신선도 경고

- 없음. 버전 표기는 전건 `"{버전} / {연월} 기준"` 형식 준수(pydantic-settings 2.14.2 / 2026-06, 0.137.0/2026-06-14).

### ✅ 확인됨

**코드 API 표면 (0건 실패)**
- **경로 데코레이터 파라미터 목록(line 14–19) — §1-2(line 275–280) AST 추출 결과와 문자 단위 완전 일치** ✅. 개수 검산: **정확히 23개**로 본문의 "스물세 개"(line 24)가 맞다. `response_model_*` 하위 인자도 **정확히 6개**(`_include`·`_exclude`·`_by_alias`·`_exclude_unset`·`_exclude_defaults`·`_exclude_none`)로 본문의 "여섯 개"가 맞다 ✅
- 출처 표기 "fastapi 0.140.0 태그 소스 `fastapi/routing.py`·`applications.py` AST 추출 (조회 2026-07-25)" ✅ §6-2 R20(line 1102)과 일치
- `APIRouter(prefix=, tags=, dependencies=)` ✅ §1-2 `APIRouter.__init__` · `@router.get`·`@router.post(status_code=)` ✅ · `include_router` 파라미터 순서 상이 + 키워드 강제 ✅ §1-2(line 290)
- **`app.include_router(router=...)`의 키워드 이름 `router` ✅ 추적됨** — `research/web.md` line 82가 양쪽 시그니처를 전개하며 첫 파라미터가 `router`임을 확인한다(*"`FastAPI.include_router`는 `router, prefix, tags, ...` 순"*)
- `from pydantic_settings import BaseSettings, SettingsConfigDict` ✅ — `BaseSettings`는 §8-1 추적됨, `SettingsConfigDict`·`env_prefix`·`env_file`은 계약 §8-2 **2장 소유 T1**이고 **각주가 실제로 그 내용이다**(line 214)
- **각주 URL 실재 확인 ✅** — `https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/`는 `research/web_deploy.md` §3-I(line 890) 및 소스 표 S72(line 1803)가 *"구 `docs.pydantic.dev/...`가 **HTTP 301**로 리다이렉트되는 현행 정본 URL(2026-07-25 확인)"*로 기록한 바로 그 주소다. 저술가가 구 URL을 쓰지 않고 현행 리다이렉트 타깃을 쓴 것이 정확하다
- `functools.lru_cache` 표준 라이브러리 면제(계약 §8-0) ✅ · `app.openapi_version` 오버라이드 ✅ §1-2(line 316) · `iter_route_contexts()` ✅ §3-1(line 630) · `$WEB_CONCURRENCY`가 접두사 없는 uvicorn 변수라는 서술 ✅ §1-3(line 356)·계약 부록 #7
- **OpenAPI 3.1.0이 `applications.py`에 문자열로 고정** ✅ §1-2 축자 `self.openapi_version ... = "3.1.0"`
- **가짜 주석 0건** — 주석은 파일 경로와 `# ...(1장, 생략)`뿐

**인용 (전건 원문 대조)**
- rmonvfer *"started cringing"* / *"I wouldn't recommend it for anything serious... not without requiring you to write a framework on top, like I've unfortunately done"* (HN, 2025-08-06) ✅ **§4-4(line 797) 및 `research/community.md` line 349·351 원문과 일치**
- mattmanser *"to add one property I had to edit 40 files... It's anti-patterns like that which give statically typed languages a bad name."* ✅ **§4-4(line 799)·`research/community.md` line 455 원문과 일치** (둘째 문장까지 실재 확인)
- 이슈 3건 표(line 251–255) — #370/2026-06-14/`AttributeError: '_IncludedRouter' object has no attribute 'path'` · #379/2026-06-25 · #388/2026-07-08 ✅ **§3-2(line 636–640)와 전건 일치**
- 0.137.0 릴리스 노트 축자 ✅ §3-1

**표집 편향·프로바넌스 규율 준수 (모범)**
- line 105가 *"HN의 단일 스레드... 'Litestar를 봐라'는 글에 달린 댓글들... FastAPI를 떠나기로 한 사람이 구조적으로 과대표집된 표본"*을 명시하고 **"실무자들은 서비스 레이어를 둔다"고도 "요즘은 안 둔다"고도 쓸 수 없다**고 선언 ✅ §4(line 770)·계획 제약 6 정확 준수
- line 103이 반대편 원문 발언 미확보를 **자진 신고** ✅ §4-4
- line 259가 *"위 이슈들은 '깨졌다는 사실'의 근거이지 '무엇이 어떻게 바뀌었는지'의 근거가 아니다... 이슈 본문의 버전 번호는 보고자가 자기 환경을 적어둔 것"*을 명시 ✅ **§3-2(line 642) 경고문과 정확히 일치** — 뉘앙스 지뢰 회피
- line 30 「저자 가설」·line 234 「저자 서술」 마커 ✅ 계획 line 222가 `operation_id`의 클라이언트 생성 영향에 요구한 표시와 정확히 일치
- "월 3~5회 릴리스되는 프레임워크"(line 265) ✅ **`01_reference.md` line 26 버전 규율 및 `research/version_pins.md` line 62·573 축자와 일치**

**리서치 공백 준수** — Reddit·Stack Overflow **0건** ✅ / #14603 미등장 ✅ / 출신 귀속 0건 ✅(경로 함수 비대화의 원인은 line 30에서 **저자 가설**로 표시) / Spring 측 수치·설정 키 **0건**(클래스 레벨 매핑·인터셉터를 구조 대조로만 언급) ✅ 계획 제약 10 준수

**총평:** 표집 편향과 이슈-릴리스노트 층위 구분을 레퍼런스 경고문 수준으로 정확히 지켰다. 남은 것은 `AsyncSession` import 경로 각주 1개와 일반화 표현 2건.

---

## 3장

**라운드 1 · 2026-07-26 · 대조 근거:** `01_reference.md` §1-2·§3-4·§3-5·§3-6·§5-9·§7-4·§7-5, `tracker_contract.md` §3-5·§3-6·§8, `02_plan.md` 「뉘앙스 지뢰 배정표」 + **웹 2차 확인 7건**

### ❌ 정정 필요 (BLOCKING)

- **[원문] (line 324) `status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=body.model_dump()`**
  → **[정정 · 권고안]** `status_code=422, content=body.model_dump()` — **정수 리터럴.**
  **근거 (1차 소스, 태그 고정 2건 대조):** ref §6-2의 "태그 고정" 규율대로 HEAD가 아니라 **핀된 버전에서** 확인했다.
  | 태그 | `HTTP_422_UNPROCESSABLE_ENTITY` | `HTTP_422_UNPROCESSABLE_CONTENT` |
  |---|---|---|
  | **starlette 1.3.1** (버전 핀 B) | `__deprecated__`에만 존재(line 206) → 접근 시 `StarletteDeprecationWarning` | **`= 422`** (line 222, `__all__` line 169) |
  | **starlette 0.46.0** (FastAPI가 핀하는 하한) | **`= 422`** 평범한 상수 | **정의되지 않음** |
  - 1.3.1 축자 경고 메시지: **"Use 'HTTP_422_UNPROCESSABLE_CONTENT' instead."** (HTTP 422가 RFC 9110에서 *Unprocessable Content*로 개칭된 것을 반영)
  - 🚨 **따라서 두 이름 중 어느 쪽도 핀 범위 전체에서 안전하지 않다.** FastAPI는 `starlette>=0.46.0`만 핀하고(§J line 222), **1장 line 114가 바로 그 사실을 근거로 "독자의 락파일에 0.4x가 있을 수도 1.x가 있을 수도 있다"고 독자에게 경고한다.** `..._ENTITY`는 1.3.1에서 DeprecationWarning을, `..._CONTENT`는 0.46.0에서 **`AttributeError`**를 낸다.
  - **정수 리터럴 `422`만 핀 범위 전체에서 불변이고, 이것이 FastAPI 공식 「Handling Errors」 문서가 실제로 쓰는 형태다**(웹 확인 — 이 페이지는 이미 [^3-4]로 인용 중이라 **각주를 새로 달 필요도 없다**).
  - **차선안:** 이 책의 코드를 계약 §1의 고정 타깃(starlette 1.3.1)에서만 도는 것으로 간주한다면 `status.HTTP_422_UNPROCESSABLE_CONTENT`도 정확하다. 다만 그 경우 1장 line 114의 락파일 경고와 3장 코드가 서로 어긋나므로, **정수 리터럴을 권고한다.**
  - **어느 쪽을 택하든 `..._ENTITY` 유지는 불가하다.**
  **왜 BLOCKING인가:** ① 이 상수는 3장 자신의 각주 [^3-5]가 *"FastAPI provides the same `starlette.status` as `fastapi.status`"*라고 밝힌 대로 **Starlette 것을 그대로 재수출**하므로 deprecation이 그대로 전파된다. ② 계획 제약 9-(B)-2 「버전 정합 관용구」가 구식 관용구를 금지한다(`.dict()`·`declarative_base()`·`@app.on_event`와 같은 범주). ③ **신선도를 셀링 포인트로 내건 책의 3장 코드가 실행 즉시 DeprecationWarning을 찍는다.** ④ 3장 line 117이 바로 "구식 어휘를 신선도 판별 지표로 쓰라"고 독자에게 가르치는 장이다.
  **부기:** [^3-5]가 인용한 FastAPI 「Response Status Code」 문서에는 **422 상수가 아예 등장하지 않는다**(웹 확인). 즉 현행 각주는 이 상수를 뒷받침하지 않는다 — 정정과 함께 각주 근거를 Starlette `status.py`로 보강하거나, FastAPI 공식 「Handling Errors」 문서가 그러듯 **정수 리터럴 `422`**를 쓰는 것도 유효한 대안이다.
  **영향 없음 확인:** 같은 파일의 `HTTP_404_NOT_FOUND`(line 163)·`HTTP_403_FORBIDDEN`(line 159)·`HTTP_500_INTERNAL_SERVER_ERROR`(line 193)는 **개칭 대상이 아니며 정상**이다 ✅ — line 249·270·275는 수정 불필요.

### ⚠️ 출처 없음

- **[원문] (line 156·158) "2020-05-04에 열린 issue #1376이 그 다음의 기록이다... yusra-haider: *'auto-generated documentation doesn't reflect the updated status code'*"**
  → **귀속 충돌.** §3-5(line 684)는 이 발언에 **2019-10-31**을 붙인다. #1376 개설일(2020-05-04)보다 **7개월 앞서므로 같은 이슈의 댓글일 수 없다**(#643 계열일 가능성이 높다). 초안은 날짜를 생략한 채 #1376 아래에 배치해 잘못된 귀속을 만든다.
  **정정안:** 원문에서 이 발언의 소속 이슈를 확인해 재귀속하거나, 이슈 귀속 없이 *"같은 고통을 적어둔 사람들의 기록"*으로 완화한다. (나머지 3인 akrejczinger·ushu·Acerinth는 §3-5 기재와 일치 ✅)

- **[원문] (line 156) "'Allow customization of validation error'라는 제목으로 5년에 걸쳐 우회법 전시장이 됐다."**
  → **레퍼런스 내부 충돌.** §3-5(line 683)는 "5년짜리"라 쓰지만, 신선도 원장(line 1254)은 #1376의 확인 범위를 **2020-05-04 ~ 2021-04-28(약 11개월)**로 기록하고 인용된 우회법 4건도 전부 2020~2021년이다. "5년" 구간에 해당하는 관측 근거가 없다.
  **정정안:** *"이슈가 열리고 1년 사이에 우회법이 네 갈래로 쌓였고, 그 이슈는 그 뒤로도 닫히지 않았다."* (확인된 사실만)

- **[원문] (line 193) "미디어 타입도 `application/problem+json`이 아니고" / (line 197–202) RFC 9457 필드 비교표의 `type`·`title`·`detail`·`status`·`instance`**
  → RFC 9457의 미디어 타입과 멤버 이름은 `01_reference.md`·`research/*.md` 어디에도 문자열로 없다. 계약 §3-5는 **필드명을 다르게 고르라**는 지시일 뿐 RFC 쪽 이름을 검증해주지 않는다. (판단 자체는 옳고 계약 부록 #6과 일치하나, 근거가 붙지 않았다)
  **정정안:** RFC 9457 §3(Members of a Problem Details Object) 각주 1회. 그러면 비교표 전체가 한 각주로 덮인다.

### 🕒 신선도 경고 (BLOCKING — 마커 미해소)

- **[원문] (line 160) "ushu: 모듈 전역 변수(`validation_error_response_definition`)를 통째로 덮어쓰는 방법 (사실 확인 필요 — 이 변수의 현행 소스 위치는 커뮤니티 진술이라 대조가 필요하다)."**
  → **`(사실 확인 필요)` 마커가 본문에 그대로 남아 있다. final에 남으면 안 된다.** 항목 자체는 계약 §8-4가 지정한 **T3**(§7-4 line 1217 *"`validation_error_response_definition` 현행 위치"* 미확인)이고, §3-5(line 693)도 *"커뮤니티 진술이므로 현행 소스 대조 필수"*로 신고한 상태다. 현행 소스 위치는 이번 라운드에서도 확정하지 못했다 → **✅로 승격 불가.**
  **해소안 (마커 제거 + 시점 귀속으로 재작성):**
  *"ushu: 모듈 전역 변수(`validation_error_response_definition`)를 통째로 덮어쓰는 방법. 다만 이건 2021년의 기록이고, 그 변수가 지금도 같은 자리에 있는지는 이 책이 확인하지 않았다."*
  이렇게 쓰면 **과거 기록**(§3-5로 추적됨)만 주장하고 현행 소스에 대한 단정을 피하므로 T3가 해소된다.

### ⚠️ 추가 — 산술·제목 (비차단, 정정안 있음)

- **[원문] (line 185) "2019년의 7807에서 2025년의 9457로 이어지는 **7년짜리 아크**"**
  → **산술 부정확.** 아크의 기점 #512는 **2019-09-07**이고 이 책의 기준 시점은 **2026-07-25**다 → **6년 10개월**. 아직 7년이 되지 않았다. (1장이 "7년이 넘었다"고 쓴 대상은 ASGI 3.0 **2019-03-20** = 7년 4개월로, **기점이 다른 별개 사실**이다 — 두 "7년"을 같은 근거로 읽으면 안 된다.)
  **정정안:** *"7년째 이어지는 아크"* — 6년 10개월은 **7년째**에 해당하므로 참이고, 절 제목(line 167)의 "7년째"·§3-4(line 669)의 "7년째 열려 있는 요청"과도 어휘가 일치한다.
  **주기:** 이 표현은 `02_plan.md` line 174와 §3-4 line 655에서 그대로 내려온 것이다. **1장 저술가는 계획의 날짜 산술("7년째"·"지난 6개월")을 스스로 검산해 바로잡았는데, 3장은 같은 계획 문구를 검산 없이 승계했다.** 계획을 근거로 삼되 산술은 각 장이 다시 계산해야 한다.

- **[제안 · 재량] (line 167) 절 제목 「RFC 9457, 7년째 열려 있는 요청」**
  → **본문 판정은 ✅다**(아래 참조). "7년째"는 참이다. 다만 제목만 목차·검색 결과에 떼어져 노출되면 *"RFC 9457이 2019년부터 열려 있었다"*로 읽힌다 — 실제 2019년 요청은 RFC **7807**이다.
  **제안:** 「RFC 9457, 7807에서 이어진 7년째」 정도. 본문이 이미 정확하므로 저술가 재량.

### ✅ 확인됨

**🚨 최대 지뢰 — RFC 9457: 통과.** 계획 「뉘앙스 지뢰 배정표」(line 174)의 4개 요구를 **전건 충족**한다.
- ① *"issue #512(2019-09-07)는 **RFC 7807** 지원 요청이었다. RFC 9457의 전신인 문서다"*(line 171) — **7년 아크의 시작이 7807임을 본문 첫 문장에서 명시 구분** ✅
- ② *"RFC 9457을 이름으로 걸고 다룬 논의는 Discussion #14517(2025-12-13)부터"*(line 175) ✅ §3-4
- ③ *"PR #15951(2026-07-07)은 제출된 날 그대로 닫혔다... 기술적 반려가 아니었다... **프로세스 사유**"*(line 179–183) ✅ §3-4(line 662–665) 축자 일치
- ④ *"2026-07-25 시점에 확인한 사실은 이것이다 — FastAPI 코어에 RFC 9457 지원은 없다. '지원한다'도 틀리고 '거절됐다'도 틀린다"*(line 185) — **§3-4(line 669)의 지시 문장과 사실상 동일** ✅ + 시점 명기 + *"이 상태는 바뀔 수 있으니 저장소의 최신 논의를 함께 확인하는 편이 낫다"* 휘발성 경고까지 ✅
- 인용 3건(tiangolo 2020-06-10 / *"This is a breaking change and therefore should be opt in"* / yakubka 2026-07-05 / YuriiMotov close 사유) **전건 §3-4 축자와 일치** ✅

**각주 6건 — URL 실재·인용문 실재 전건 웹 확인 ✅ (하나도 날조 없음)**
| 각주 | URL 실재 | 인용·내용 검증 |
|---|---|---|
| [^3-1] Pydantic Models | ✅ 200 | `BaseModel`·`Field`·`ConfigDict` 문서화 확인. 제네릭 모델 축자 **"Declare a Pydantic model that inherits from `BaseModel` and `typing.Generic` (in this specific order)"** — 초안 코드 `class Page(BaseModel, Generic[ItemT])`가 **상속 순서까지 정확** ✅ |
| [^3-2] Pydantic Serialization | ✅ 200 | 축자 **"any field that was not explicitly provided will be excluded"** 원문에 실재 ✅ `exclude_unset` 문맥 일치 |
| [^3-3] Jakarta EE Tutorial | ✅ 200 | 축자 **"annotations placed on a field, method, or class"** 실재 ✅ + 「Built-In Jakarta Bean Validation Constraints」 표에 `@NotNull`·`@Size`·`@Min`·`@Max`·`@Pattern` 전건 실재 ✅ (계획 제약 10이 요구한 **Java 측 각주** — 정확히 이행됨) |
| [^3-4] FastAPI Handling Errors | ✅ 200 | 6개 표면 전건 실재: `{"detail": ...}` 단수 · `@app.exception_handler` · `from fastapi.exceptions import RequestValidationError` · `exc.errors()` · `from fastapi.responses import JSONResponse` · `from fastapi import Request` ✅ |
| [^3-5] FastAPI Response Status Code | ✅ 200 | 축자 **"FastAPI provides the same `starlette.status` as `fastapi.status`"** 실재 ✅ `from fastapi import status`·`status.HTTP_201_CREATED` 실재 ✅ (단, 422 상수는 이 페이지에 없다 — 위 ❌ 참조) |
| [^3-6] Starlette Requests | ✅ 200 | 축자 **"If you want to store additional information on the request you can do so using `request.state`."** 실재 ✅ |
- 본문 출처 1건 추가 확인: line 136 `https://fastapi.tiangolo.com/tutorial/path-params/` ✅ — **422 응답 본문 JSON이 공식 문서와 축자 일치**(`type`·`loc`·`msg`·`input` 4키, `url` 키 없음까지 정확) ✅

**코드 API 표면 (❌ 1건 외 전건 추적)**
- `pydantic.BaseModel`·`Field`·`ConfigDict` ✅ T1 3장 소유 → [^3-1] 각주 이행 · `ConfigDict(from_attributes=True)` ✅ §8-1 · `model_dump(exclude_unset=True)` ✅ T1 → [^3-2] · 제네릭 모델 ✅ T1 → [^3-1]
- `Annotated[str | None, Query(min_length=2)]`·`Query(ge=1, le=100)` ✅ §1-2 파라미터 선언 함수 공통 인자(line 292–298) + §8-1 · 구식 `Query(None)` 대조 예시 ✅ 계약 §4-1
- `@field_validator` ✅ §8-1 · `fastapi.status`·`Request`·`RequestValidationError`·`exc.errors()`·`JSONResponse`·`@app.exception_handler`·`HTTPException` ✅ T1 → [^3-4]/[^3-5]
- `typing.Generic`·`TypeVar` 표준 라이브러리 면제(계약 §8-0) · `tracker.*` 전건 저자 발명 면제(§8-0)
- **v1→v2 마이그레이션 어휘 8쌍(line 117) — §5-9(line 832)와 전건 일치** ✅ (`.dict()`→`model_dump()`, `.json()`→`model_dump_json()`, `parse_obj()`→`model_validate()`, `orm_mode`→`from_attributes`, `@validator`/`@root_validator`→`@field_validator`/`@model_validator`, `class Config`→`model_config = ConfigDict(...)`, `regex`→`pattern`, 설정 import→`pydantic_settings`)
- **예외 계층·에러 스키마가 계약과 완전 일치** ✅ — `TrackerError`/`DomainError`/`NotFoundError`(404)/`PermissionDeniedError`(403), 주석의 `ConflictError`(409)·`ValidationFailedError`(422)·`InfrastructureError`→`ExternalServiceError`(502)·`StorageError`(503) 전건 계약 §3-6과 일치. `ErrorResponse`/`ErrorDetail` 필드도 계약 §3-5 표와 일치. 핸들러 3개 규율 ✅
- **가짜 주석 0건** — `# ✅ 현행 스타일` / `# ❌ 인터넷 예제에 널려 있는 구식 스타일`은 계약 §4-1과 §5-9(line 832)로 뒷받침되는 판정 주석이고, line 278–279 주석은 계약 §3-6의 클래스 목록을 그대로 옮긴 것이다. 동작을 지어낸 주석 없음

**422 논쟁 (전건 §3-5 축자 일치)** — #643(yiannis-kt, 2019-10-22) ✅ · tiangolo 답변 축자 ✅ · Flask-apispec이 이미 422를 썼다 ✅ · 검증 에러를 한 부류로 분리 ✅ · antonagestam(2022-02-08) 축자 ✅ · Jaza(2022-12-06) 절충안 ✅ · PhilippeGalvan *"auto-doc is a key argument!"* ✅ · akrejczinger·Acerinth 축자 ✅

**Java/Python 인용 (전건 §3-6 일치)** — duncanfwalker(2025-07-27, JSR-380) ✅ · microflash(2025-07-26) ✅ · globular-toast(2025-08-07) ✅ · rtpg ✅
- **통념 역전을 §3-6 line 715 저자 해석대로 정확히 서술**하면서, §3-6이 "Python 진영의 **다수설**"이라 쓴 것을 초안은 **"자주 나오는 말"**(line 80)로 약화했다 — 계획 제약 6(다수설 일반화 금지)을 레퍼런스보다 엄격하게 지킨 것이라 ✅

**리서치 공백 준수** — Reddit·Stack Overflow **0건** ✅ / #14603 미등장 ✅ / 출신 귀속 0건 ✅ / Spring 측 서술은 `@Valid`·`BindingResult`·Jackson·Springdoc의 **구조 대조**이고 수치·설정 키·엔드포인트 경로 0건, Bean Validation 애너테이션은 [^3-3] 각주로 뒷받침 ✅ 계획 제약 10 준수

**양화사 점검** — "넷이면 충분하다"·"핸들러는 딱 세 개"·"넷 말고 다른 접미사는 쓰지 않는다"는 전부 📐 저자 설계 마커 아래의 저자 규약이라 검증 대상 아님 ✅ / "전부 공통으로 갖는다"(line 88)는 §1-2(line 292–299) *"Path·Query·Header·Cookie·Body·Form·File 전부 보유"*와 일치 ✅ / "상당수"(line 117)는 §2-3 절 제목 *"인터넷 자료 대다수가 낡았다"*로 뒷받침 ✅

**총평:** 최대 지뢰 RFC 9457을 완벽히 통과했고 각주 6건이 URL·인용문 모두 실재한다(날조 0건). 유일한 코드 결함은 deprecated 422 상수 하나이며, 이것 하나가 BLOCKING이다.

---

## 라운드 1 — 전수 스윕 (grep 기반 적극 확인)

추론이 아니라 **실행한 명령의 결과**다.

| 스윕 대상 | 명령 | 결과 |
|---|---|---|
| `(사실 확인 필요)` 마커 | `grep -n "사실 확인 필요" chapters/*.md` | **총 1건** — 1장 0 · 2장 0 · **3장 line 160** 1건. (위 🕒 항목이 유일한 미해소 마커다) |
| 그 밖의 편집 마커 | `grep -n "TODO\|FIXME\|미확인"` | **0건** |
| `on_event` 3층 지뢰 | `grep -n "on_event" chapters/*.md` | **0건 (1·2·3장 모두).** 계획 지뢰표는 이 지뢰를 **4장**에 배정했다 — 1~3장은 **해당 없음**이며, "FastAPI가 제거했다"류 오서술도 존재하지 않는다 |
| Reddit·Stack Overflow 인용 | `grep -ni "reddit\|stackoverflow"` | **0건** — §7-1 금지선 준수 |
| `#14603` | `grep -n "14603"` | **0건** — 계획 제약 8 준수 |

### 챕터 간 교차 점검 (`fact-check` 스킬 규약)

- **0.137.0 릴리스 노트 축자** — 1장 line 85–86 vs 2장 line 242–243을 `diff`로 대조: **byte-identical ✅.** 같은 인용이 장마다 다르게 렌더링되는 편집 단계 결함 없음.
- **공유 심볼 표기 일관** — `iter_route_contexts()`(1장 1회·2장 1회) · `0.137.0`(1장 3회·2장 2회) · `0.140.0`(1장 5회·2장 2회) · `OpenAPI 3.1.0`(1장·2장 각 1회) · `strict_content_type`(1장 4회) — **버전·심볼 표기 충돌 0건 ✅**
- **⚠️ 발견된 교차 충돌 1건** — **1장 line 114의 락파일 경고(`starlette>=0.46.0`이라 0.4x일 수도 1.x일 수도 있다)와 3장 line 324의 422 상수가 정면으로 어긋난다.** 위 3장 ❌ 항목에 반영했다. 이 충돌은 한 장만 읽어서는 보이지 않는다.
- **"7년" 두 건은 기점이 다르다** — 1장 = ASGI 3.0(2019-03-20, 7년 4개월, "넘었다" ✅) / 3장 = #512(2019-09-07, 6년 10개월, "7년짜리"는 과장). 위 3장 ⚠️ 항목에 반영.

## 라운드 1 종합

| 장 | ❌ | ⚠️ | 🕒 | 코드 심볼 추적 실패 |
|---|---|---|---|---|
| 1장 | 1 | 3 | 0 | **0** |
| 2장 | 0 | 4 | 0 | **0** (각주 누락 1건은 ⚠️) |
| 3장 | 1 | 5 | 1 (마커 미해소) | **1** (핀 범위에서 안전하지 않은 상수) |

**🚨 Phase 5 차단 사유 — 정확히 3건 (전부 해소 필수):**
1. **3장 line 324** `status.HTTP_422_UNPROCESSABLE_ENTITY` → 정수 `422` (❌)
2. **3장 line 160** `(사실 확인 필요)` 마커 미해소 (🕒)
3. **1장 line 41** "아홉 줄" → "아홉 개" (❌)

그 밖의 ⚠️ 12건은 **조치 필요이나 Phase 5를 차단하지 않는다.** 로그 헤더의 🕒 정의("검증 불가")에 해당하는 항목은 **3장 line 160 하나뿐**이다.

**웹 2차 확인 10건 수행** — 각주 URL 7건 전건 실재(내용·축자까지 대조), Starlette `status.py` **태그 2개**(1.3.1·0.46.0) 1차 소스 대조, FastAPI path-params 응답 본문 1건.
**날조된 URL·인용문·import 경로는 한 건도 발견되지 않았다.** §7-5가 경고한 유형(가짜 주석·없는 import 경로)의 재발 없음.

---

# 배치 2 (4·5·6장) — 라운드 1

**검증 시점:** 2026-07-26 · **대조 근거:** `01_reference.md`(버전 핀 테이블·§1-2·§1-3·§1-5·§1-6·§2-2·§3-3·§3-8·§3-10·§5-9·§5-A·§5-D·§6-4·§7-1~7-5·신선도 원장) · `tracker_contract.md` §3-3·§4-3·§4-6·§7·§8 · `research/{community,papers}.md` · `chapters/0{1,2,3}_final.md`(교차 충돌)

## 4장

### ❌ 정정 필요 (BLOCKING)

**없음.** 4장에서 사실 오류로 판정된 항목은 0건이다.

### 🕒 신선도 경고 (BLOCKING — 마커 문자열 미해소)

- **line 262** — `(사실 확인 필요)` 마커. *"워커를 여러 개 띄웠을 때 `lifespan`이 워커마다 도는지, 서버리스에서는 어떻게 되는지 — 이 책은 그 동작을 1차 소스로 확인하지 못했다 (사실 확인 필요)."*
  **판정: 🕒 (검증 불가 — 정당한 T3).** 계약 §8-4가 "lifespan이 멀티 워커·서버리스에서 워커별 실행되는지"를 4·13장 소유 T3로 명시했고, 레퍼런스 §7-4가 미확인 목록에 올려두었다. 레퍼런스 §1-1도 *"lifespan 프로토콜 명세(`specs/lifespan.html`)는 fetch하지 않았다"*고 신고한다. **저술가의 자기 신고가 정확하며 산문은 이미 규율을 지키고 있다.**
  **정정안:** 문자열 `(사실 확인 필요)`만 삭제하고 앞뒤 산문은 **그대로 둔다.** 판정 근거가 로그에 남았으므로 마커는 역할을 다했다. → 이 조치만으로 Phase 5 차단 해제.

### ⚠️ 출처 없음 / 보강 권장 (비차단)

- **line 135–138** — `Depends(..., scope=)` 공식 문서 축자 2줄(`"function"` / `"request"`)에 URL·각주가 없다. 인용문 자체는 레퍼런스 §1-2와 **완전 일치(✅)**하나 독자가 원문에 닿을 길이 없다. 6장 line 332–333이 **같은 인용을 반복**하는데 그쪽에도 없다.
  **정정안:** 4장이 소유해 각주 1회 — `https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope`(레퍼런스 §1-2가 명시한 URL). 6장은 "4장에서 인용한"으로 참조만.
- **line 39–43** — dishka 축자 인용에 URL 없음. 인용문은 §3-8과 **완전 일치(✅)**하고 *"게시 시점은 확인하지 못했으니"* 단서도 신선도 원장(`dishka … 게시일 미확인`)과 정합하다. 출처 링크만 보강 권장.
- **line 59** — *"'명시적인 편이 암묵적인 것보다 낫다'는 파이썬의 오래된 격언에 어긋난다는 비판"*을 "남겨진 유물 두 묶음"의 한쪽으로 제시한다. 그러나 이 근거는 **유물이 아니라 발언**(§3-8: Lobsters linkdd)이다. 근거 종류와 서술이 어긋난다.
  **정정안:** "다른 쪽 묶음"을 "다른 쪽은 발언이다 — Lobsters의 한 개발자는 …" 정도로 근거 계층을 맞춘다.

### ✅ 확인됨 (주요 항목)

| 항목 | line | 근거 |
|---|---|---|
| `Depends` 시그니처 전문(`dependency`·`use_cache`·`scope: Literal["function","request"]\|None`) | 13–23 | §1-2 AST 추출본과 **바이트 단위 일치.** 출처 표기 `param_functions.py` / 0.140.0 / 조회 2026-07-25도 일치 |
| **🚨 마커 1 — 예외 핸들러의 하위 클래스 해석** | 226 | **웹 2차 확인 완료 → ✅ 성립.** Starlette **태그 1.3.1** `starlette/_exception_handler.py`의 `_lookup_exception_handler()`가 `for cls in type(exc).__mro__: if cls in exc_handlers: return exc_handlers[cls]`로 **MRO를 순회**한다. 부모 클래스에 등록한 핸들러가 하위 클래스를 받는다는 것이 **1차 소스(고정 태그 소스 코드)로 확정**됐다. 상세는 아래 「마커 4건 판정」 |
| `on_event` 3층 구조 | 266–276 | §5-9 「🚨 `on_event`의 3층 구조」와 **3층 전부 일치.** ① 0.140.0에 `@deprecated`로 존치 + 축자 ② 제거한 쪽은 **Starlette 1.0.0rc1** + 축자 *"Remove `on_event()` decorator from `Starlette` and `Router`"* ③ `starlette>=0.46.0` 핀. 그리고 line 274가 **"FastAPI가 `on_event`를 제거했다는 틀린 서술이다"**를 명시 — 지뢰표 요구를 문자 그대로 충족 |
| `Depends(scope=)` 반올림 금지 | 140–144 | §3-3 준수. #11107(2024-02)·#11143 승격·Closed·**종결 사유 미확인**·#14137(2025-10) tiangolo 처방까지 전부 일치하고, line 142가 *"'scope가 #11107을 해결했다'고는 쓰지 않겠다"*로 명시적으로 반올림을 거부한다 |
| `BaseHTTPMiddleware` 서술 범위 | 170–176 | 계획 리뷰 확정선 준수. **"예외 처리 차이"를 단정하지 않고** 「실행 시점(라우팅 바깥)」·「적용 범위(`scope["type"]`)」 둘로만 축소했고, line 176이 *"이 책은 그 한계를 1차 소스로 확인하지 못했다"*를 명시. 계약 §8-4 T3 처리 규약과 정합 |
| `add_middleware` 축자 | 216 | **웹 2차 확인.** FastAPI Advanced Middleware 원문 *"…makes sure that the internal middlewares handle server errors and custom exception handlers work properly."* — 인용 부분 축자 일치. 호출 형태 `app.add_middleware(MiddlewareClass, **options)`도 일치 |
| httpx `AsyncClient(timeout=…)` 기본값 | [^4-3] | **웹 2차 확인.** httpx Timeouts 문서 *"The default behavior is to raise a `TimeoutException` after 5 seconds of network inactivity."* — 각주의 `Timeout(timeout=5.0)` 표기와 정합 |
| #8054 Unanswered · 우회법 4종 | 53 | §3-8과 일치(캐시→시작 시점 인스턴스화→`app.state`→종료 스택+앱 상태). 신선도 원장의 *"미해결 상태 자체가 현행 사실"* 규정도 지켜짐 |
| FastNest(2026-04-28) 단일 저자 경고 | 57 | §3-8의 ⚠️ *"단일 저자 프로젝트다. 커뮤니티 합의가 아니다"*를 **본문에 그대로 노출**. 다수설 일반화 없음 |
| 코드 심볼 — `deps.py`·`middleware.py`·`main.py` | 71–101, 182–213, 238–253 | 전 심볼 §8-1 추적됨 또는 §8-2 T1 각주 해소. 상세는 아래 「코드 API 표면」 |
| Spring 측 서술 | 3, 133, 148, 222, 288 | 제약 10 준수 — `@Transactional`·OSIV·필터/인터셉터·`@ControllerAdvice`·모의 빈을 **구조로만** 대조하고 **설정 키·기본값·엔드포인트 경로를 하나도 쓰지 않았다** |

---

## 5장

### ❌ 정정 필요 (BLOCKING)

**없음.** 최대 위험 장으로 지목됐으나 §7 공백 위반 0건이다.

### 🕒 신선도 경고 (BLOCKING — 마커 문자열 미해소)

- **line 214** — `(사실 확인 필요)` 마커. free-threading 기본 빌드 전환 시점 + 40-스레드 모델 영향.
  **판정: 🕒 (검증 불가 — 정당한 T3, 5장 소유).** 레퍼런스 §1-3이 *"3.15+에서 free-threaded가 기본 빌드가 되는지, GIL 빌드 제거 로드맵은 미확인. **단정 금지**"* + *"free-threading이 40-스레드 풀 모델을 실제로 얼마나 바꾸는지 1차 벤치마크 미확보"* 둘 다 신고했고, 계약 §8-4가 5장 소유 T3로 배정했다. 확정 가능한 부분(PEP 703 Final/3.13 · PEP 779 Final/3.14 · FastAPI 0.136.0 2026-04-16 3.14t)은 **전부 §1-3과 일치(✅)**하고, 미확정 부분만 분리해 신고했다 — 문장 단위 분리가 정확하다.
  **정정안:** 문자열 `(사실 확인 필요)`만 삭제. 🕒 라벨 요구에 따라 **시점 명기 1회 추가** 권장 — 해당 문단 첫머리를 *"2026-07 / Python 3.14 기준으로"*로 시작. 뒤이은 *"빠르게 바뀔 영역이니 공식 문서를 함께 확인하자"*가 이미 휘발성 경고 역할을 하므로 추가 조치는 불필요.

### ⚠️ 출처 없음 / 정확성 보강 (비차단)

- **line 69** — *"그 고리를 끊으려고 정리 경로만 **제한을 벗겨낸** 것이다."** 바로 위 line 64에 `exit_limiter = CapacityLimiter(1)`가 인쇄돼 있어 **코드와 설명이 눈에 보이게 어긋난다.** (원 소스 주석이 *"we let `__exit__` run without a capacity limit"*이라 저술가가 소스에 충실한 것이고 §1-3의 표현도 동일하므로 **날조가 아니다.** 다만 리미터 1개짜리는 "제한 없음"이 아니라 "전용 제한"이다.)
  **정정안:** *"공용 40개 리미터를 쓰지 않고 별도 리미터로 돈다"* — 코드와 산문이 일치한다.
- **line 180** — *"초과분은 503을 받는 대신 리미터 앞에 줄을 선다."* `--limit-concurrency` 상한 **아래** 구간의 거동에 대한 추론이며 1차 소스에 진술이 없다. 게다가 *"여기서 반올림하지 말자"*라는 정밀 프레임 안에 있어 확정 사실처럼 읽힌다.
  **정정안:** *"…503을 받는 대신 리미터 앞에 줄을 서게 된다 — 이건 두 층의 동작에서 따라 나오는 추론이다."*
- **line 36–38 / 83 / 91–99 / 148** — anyio 40 축자·Adya 축자·acdha·layer8·leonidasv·shipfriend 인용에 **URL이 없다.** 인용문·날짜·화자는 **전건 대조 통과(아래 ✅)**이므로 사실 문제는 없고, 1~3장이 각주로 처리한 기준과 어긋난다는 편집 정합 문제다. 5장의 각주는 `[^5-1]` 하나뿐이다.
  **정정안:** 각주 2~3개 추가 — anyio 축자는 `[^5-1]`에 흡수(같은 문서), 학술 2건(Adya·Brockbernd)은 DOI/URL 각주(`https://www.usenix.org/legacy/events/usenix02/full_papers/adyahowell/adyahowell.pdf`, `10.4230/LIPIcs.ECOOP.2024.8`), HN 3건은 item URL(`47912719`·`47905032`·`48289232`).

### ✅ 확인됨 (주요 항목)

| 항목 | line | 근거 |
|---|---|---|
| **40 체인 4층 전부** | 3, 14–40 | §1-3과 **바이트 단위 일치.** FastAPI `routing.py` 갈림길 4줄 · Starlette `concurrency.py` 3줄(`limiter` 미전달) · anyio `CapacityLimiter(40)` · 공식 문서 축자 *"…maximum of 40 threads to be spawned."* 태그 표기(0.140.0 / 1.3.1 / 4.14.2)와 조회일도 일치 |
| 의존성이 같은 40을 공유 | 53–59 | §1-3 *"sync `Depends`도 같은 풀을 공유한다(`dependencies/utils.py:713-716`)"* + §5-2 실무 팁과 일치 |
| `exit_limiter` 주석 축자 | 69 | §1-3 주석 축자 *"can create race conditions/deadlocks if the context manager itself has its own internal pool (e.g. a database connection pool)"* 일치 |
| **🚨 Adya 2002 — 축자·부제·2축** | 81–85 | `research/papers.md` §1-1에서 **전문 확인(✅)** 자료. 축자 *"The key concept is that one can choose the reasoning benefits of cooperative task management without sacrificing the readability and maintainability of automatic stack management."*가 papers.md line 48과 **완전 일치.** 부제·USENIX ATC 2002·작업 관리 × 스택 관리 2축 전부 일치. 하드웨어 전제 단서도 부착됨 |
| **🚨 출신 귀속 — §7-2 최대 금지선** | 89 | **모범적 통과.** *"— 여기서부터는 **저자 가설**이다"*로 명시 개시 + *"리서치에서 '나는 서블릿 세계에서 왔고 그래서 이렇게 했다'고 밝힌 증언은 **한 건도 찾지 못했다**"*로 증언 0건을 독자에게 직접 공개 + *"관찰된 사실이 아니라 내 설명이다"*로 마감. §7-2의 *"실수는 사실로, 원인 귀속은 저자의 가설로 표시하라"*를 문자 그대로 이행 |
| **🚨 WebFlux/Reactor 교차 경험담** | 전장 | `grep -ni "webflux\|reactor\|리액터\|mono\|flux"` → **0건.** §7-2의 0건 항목을 **전량 배제**했다. Java 내부 Reactor 회의론(community.md 516–547)을 asyncio 대조로 전용한 곳도 없다 |
| **🚨 Mark Shannon 카드 전항** | 196–206 | `research/community.md` 503–510과 **전건 일치.** 2025-05-09 ✅ / "Add Virtual Threads to Python" ✅ / discuss.python.org ✅ / CPython 코어 개발자 ✅ / 축자 ✅ / **274 posts ✅ · 22,050 views ✅ · 565 likes ✅** / 마지막 글 2026-02-14 ✅ / Tin Tvrtković(`aiofiles`·`pytest-asyncio`) 2025-05-10 ✅ / 2026-02-14 Java 참여자 요구 축자 ✅. **반론 병기 ✅** (Liz 2025-05-10 · Rosuav 2025-08-02, 날짜까지 일치). **"파이썬의 로드맵이 아니다" 명시 ✅** — 요구된 4개 조건 전부 충족 |
| **🚨 Kotlin ECOOP 2024 프록시** | 210–212 | `research/papers.md` 121–130(**전문 ✅**, 원문 Table 2)과 전건 일치. **커밋 1,353건 ✅ · 버그 55건 ✅ · 취소 예외 14건 ✅ · 중첩 `runBlocking` 11건 ✅ · 전통적 패턴 의도적 제외 ✅.** (이 네 수치는 `01_reference.md`에 55·14만 실려 있어 날조 후보로 의심했으나 **papers.md 원문 확인으로 전건 해소**됐다.) 그리고 line 212가 **"이건 Kotlin 연구이고 파이썬 연구가 아니다. 언어도 런타임도 다르니 수치를 옮겨 쓸 수 없다"**를 굵게 명시 — §2-2 대체 전략의 요구 그대로. **수치를 파이썬으로 옮긴 문장 0건** |
| Python asyncio 실증 연구 부재 | 210 | §2-2 *"Python asyncio 실증 — 없음 ❌"*와 일치. 정직하게 밝힘 |
| acdha 4단계 시나리오 | 91–95 | community.md 557–558과 일치. 2026-04-26 ✅, 축자 *"That error in #4 does not tell you anything about #2 or #3"* ✅, 4단계 서술 ✅, 후속 *"스레드 모델이었다면…"*도 원문 *"If it was a thread, you would either not have the problem at all…"*의 충실한 옮김 |
| layer8 반론 병기 | 97 | community.md 556과 일치. 2026-04-25 ✅, 축자 2건 ✅. §4 표집 편향 경고에 대한 **균형추가 실제로 배치**됐고 *"이 장은 `async def`가 언제나 옳다고 말하려는 게 아니다"*로 마감 |
| leonidasv `foo`/`afoo` | 99 | community.md 532와 일치. 2026-05-27 ✅, 축자 ✅ |
| shipfriend 서정우 | 148 | community.md 490과 일치. 2026-03-28 ✅, 축자 *"CPU 집약적인 작업(이미지 처리, 대용량 연산 등)에서는 멀티스레드를 써도 병렬화가 되지 않"* ✅. 레퍼런스가 금지한 **성능 수치는 인용하지 않았다** ✅ |
| uvicorn 플래그 표 3행 | 156–162 | §1-3 플래그 표와 일치(`--workers` None/`$WEB_CONCURRENCY` · `--limit-concurrency` None/503 · `--backlog` 2048). "uvicorn 0.51.0 / 2026-07 기준" 표기 ✅ |
| SEDA(SOSP 2001) · Little's Law(1961 *Operations Research*) | 180, 182 | §6-4와 일치. Little's Law는 "게재 정리"로 정확히 다뤘고 USL과 섞지 않았다 ✅ |
| 산술 | 186, 166 | 40 ÷ 0.2 = 200 ✅ / 5배 → 1/5 ✅ / 워커 4개 × 40 = 160 ✅ |
| free-threading 확정분 | 214 | PEP 703 Final·3.13 ✅ / PEP 779 Final·3.14 ✅ / FastAPI 0.136.0(2026-04-16) 3.14t ✅ — 전부 §1-3 |
| **다수설 일반화·표집 편향** | 전장 | *"커뮤니티는 async에 회의적이다"*류 **0건.** line 87의 *"커뮤니티가 오랫동안 반복해서 보고해 온 사실"*은 §7-2가 *"실수 패턴 자체는 근거가 풍부하다"*고 인정한 범위 안 |
| `#14603` | 전장 | `grep "14603"` → **0건.** 계획 제약 8 준수 (5장이 주제상 가장 가까운 장인데도 유입 없음) |

---

## 6장

### ❌ 정정 필요 (BLOCKING)

**없음.**

### 🕒 신선도 경고 (BLOCKING — 마커 문자열 미해소)

- **line 433** — `(사실 확인 필요)` 마커. Motor → PyMongo async 흡수가 **공식 이행 경로**인지.
  **판정: 🕒 (검증 불가 — 정당).** 레퍼런스 §1-6은 *"PyMongo 4.17.0의 async API로 가는 게 현재 경로다"*라고 **단정**하지만 그 근거는 `web_deploy §2-J` 참조뿐이고 공식 이행 발표문은 확보돼 있지 않다. 저술가가 레퍼런스보다 **보수적으로** 판단한 것이며 그 판단이 옳다.
  **✅ 확인된 사실/미확인의 문장 단위 분리 — 요구대로 되어 있다:** Motor 3.7.1 ✅(§버전 핀 D) · 2025-05-14 ✅ · 조사 시점 2026-07-25 ✅ · *"1년 넘게"* ✅(실제 1년 2개월) · PyMongo 4.17.0(2026-04-20) async 통합 ✅ · redis 8.0.1/2026-06 + `aioredis` 흡수 + `redis.asyncio` ✅. 미확인은 **"공식 이행 경로인가" 한 절만** 따로 떼어냈다.
  **📌 특기 — 레퍼런스보다 정확해진 지점:** 레퍼런스가 *"🔴 Motor는 **EOL을 지났다**"*로 적은 것을 저술가가 **"1년 넘게 새 릴리스가 없다"는 검증 가능한 사실 서술로 하향**했다. EOL 선언문은 어디에도 확보돼 있지 않으므로 이 하향이 정확하다. **통과 사례로 기록한다.**
  **정정안:** 문자열 `(사실 확인 필요)`만 삭제. 앞뒤 산문 유지.

### ⚠️ 출처 없음 / 정정 권장 (비차단)

1. **line 272 — `engine.dispose()` 누락 시의 증상을 "경고"로 서술.** 레퍼런스 §1-6은 *"`await engine.dispose()` 누락 시 **`RuntimeError: Event loop is closed`**"*로 **에러**다.
   **정정안:** *"…이벤트 루프가 닫혔다는 경고가 뜬다"* → *"…`RuntimeError: Event loop is closed`가 난다"*.
2. **line 397 — *"튜닝 파라미터는 같다."*** `QueuePool` 비호환 + `AsyncAdaptedQueuePool` 대체는 §1-6 축자로 확인되나, **"튜닝 파라미터가 동일하다"는 진술은 레퍼런스에 없다.**
   **정정안:** 삭제하거나 *"풀 인자(`pool_size`·`max_overflow` …)는 같은 이름으로 받는다"*로 좁히고 [^6-4]에 흡수.
3. **line 260 — `expire_on_commit` 기본값의 귀결.** *"기본값대로 두면 커밋 직후 속성이 만료돼 직렬화 중 같은 예외를 만난다"*는 문서 축자(*"Expiration should generally not be needed as … should normally be set to `False` when using asyncio"*)에서 **연역한 것**이다. §7-3이 `expire_on_commit` 함정을 근거 미확보 항목으로 지목한 구역이다.
   **✅ 다만 정량 수치는 하나도 없다** — 요구된 "숫자를 지어냈는가" 점검 결과 **세션 누수·N+1·`expire_on_commit` 관련 수치 0건.**
   **정정안:** *"…만나게 된다 — 문서의 권고를 뒤집어 읽은 것이다"* 정도로 연역임을 표시.
4. **line 146 / 246 / 268 / 374 / 393 / 427 — 축자 인용 6건에 URL·각주 없음.** 인용문은 **전건 §1-6과 완전 일치(✅)**이므로 사실 문제 없음. `Query` 레거시 · `MissingGreenlet` 정의 · `AsyncSession` 동시성 경고 · *"none of them 'pre create' connections"* · pre-ping 한계 · SQLModel 튜토리얼 반전.
   **정정안:** [^6-3]·[^6-4]의 적용 범위를 인용문까지 넓히거나 각주 2개 추가(`orm/queryguide/select.html` 계열 · `orm/extensions/asyncio.html`은 이미 [^6-4]).
5. **line 437–439 — velog 인용의 화자·출처 미표기.** *"한 한국 개발자가 2025년 3월"*로만 지칭. 인용문·날짜는 §3-10과 일치 ✅(velog JUNYOUNG, 2025-03-07). 익명 지칭 자체는 허용 범위이나 인용문에 출처가 없다.
   **정정안:** 각주로 필자명·URL·조회일 부착.
6. **`select()` 메서드 체인이 §8-1 열거 밖.** `.where()`·`.order_by()`·`.limit()`·`.offset()`·`Issue.id.desc()`·`result.all()`·`list(result)`가 계약 §8-1/§4-3 어디에도 문자열로 없다. **T1 성격**(모호함 없는 2.0 표준 어휘, 레퍼런스가 `select()`+`scalars()`를 정본으로 지정)이므로 ❌가 아니다.
   **정정안:** [^6-3]에 한 절 추가 — *"`select()`의 `.where()`·`.order_by()`·`.limit()`·`.offset()` 체인"*을 SQLAlchemy 2.0 Select 문서로 함께 각주.
7. **`IssueRepository.add()`가 정의된 적이 없는데 호출된다.** line 210 `await self.issues.add(issue)` — 그러나 line 175–196의 `IssueRepository`는 `get`/`list`만 갖고 **생략 표기(`# ...`)도 없다.** 2장 골격에도 `add`는 없다. (이름 자체는 계약 §3-3의 리포지터리 어휘 `get·list·add·delete`에 있으므로 **계약 위반은 아니다.**) 인쇄된 대로 따라 하면 `AttributeError`다.
   **정정안:** `IssueRepository`에 `async def add(self, issue: Issue) -> None: self.session.add(issue)` 3줄 추가, 또는 클래스 말미에 `# ...(생략)` 표기.
8. **`Query` 동음이의 충돌.** 절 제목 *"`Query`가 레거시가 되면서 바뀐 것"*(SQLAlchemy)과 line 221 `from fastapi import APIRouter, Query`(FastAPI 파라미터 선언)가 **같은 장 안에** 있다. 둘 다 정확하지만 독자가 "레거시라며 왜 import하지" 하고 걸린다.
   **정정안:** 절 제목을 *"SQLAlchemy `Query`가 레거시가 되면서 바뀐 것"*으로 한정하거나, line 221 코드 뒤에 한 줄 — *"여기 `Query`는 FastAPI의 파라미터 선언이지 앞 절의 SQLAlchemy `Query`가 아니다."*

### ✅ 확인됨 (주요 항목)

| 항목 | line | 근거 |
|---|---|---|
| Nullability 축자 + `\| None` 전환 규약 | 13–19 | §1-6 축자 일치. 계약 §4-3의 *"`Optional[]`은 인용문 안에서만"* 규약을 line 19가 **명시적으로 선언**하고 지킴 |
| **SQLAlchemy 2.0 계열 전제 · 2.1 미언급** | 전장 | 요구대로 **2.0(2.0.51 / 2026-06 기준)**만 전제. 2.1 베타를 프로덕션 권장으로 쓴 곳 0건(§1-6 경고 준수) |
| **`Query` 제거 여부 단정 금지** | 142–148 | ✅ **단정 없음.** 절 제목이 *"레거시가 되면서"*이고 인용도 *"become long term **legacy** objects"*까지만. §7-4의 미확인 항목(2.1 `Query` 제거 여부)을 건드리지 않았다 |
| 매핑 코드 전체 | 24–138 | 계약 §4-3 ✅ 예와 일치. `DeclarativeBase`·`Mapped[]`·`mapped_column()`·`relationship(back_populates=, cascade="all, delete-orphan")`·`ForeignKey`·`String(n)` 전부 §8-1 추적됨. `Column(...)`·`declarative_base()`·`nullable=False`·`Optional[]` **0건** |
| 엔티티 6 + 연결 2 | 32–43 | 계약 §7 6장 행과 정확히 일치(`User`·`Project`·`Issue`·`Comment`·`Label`·`Attachment` + `IssueLabel`·`ProjectMember`) |
| association object 기본형 유지 | 97–118 | 계약 부록 #10 준수. `relationship(secondary=)` 직접형은 [^6-2] 각주로 **언급만** 하고 채택하지 않음 |
| `MissingGreenlet` 처방 4종 | 254–264 | §1-6 처방 4종과 **전건 일치**, 각각의 대가까지. `run_sync`의 자기 평가 축자 *"probably be considered 'controversial'"* ✅ |
| `AsyncSession` 동시성 경고 | 266–270 | §1-6 축자 + *"태스크마다 별도 `AsyncSession`"* ✅ 계약 §4-3과 일치 |
| **`Depends(scope=)` 반올림 금지 (재확인)** | 330–337 | 4장과 동일하게 **미확정 유지.** *"그 종결 사유와 병합된 PR을 이 책은 확인하지 못했다… 릴리스 노트로 확인하기 전에는 미확정이다"* |
| **🚨 폐기된 추론의 반영** | 339 | 저술가가 폐기 보고한 *"`scope="function"`이면 직렬화 중 세션이 닫혀 있다"*가 **원고에 없다(`grep` 0건).** 대신 line 339는 *"확인할 수 없는 정리 순서에 응답의 정확성을 걸지 않는다"*는 설계 결론으로 대체 — **폐기가 실제로 반영됐다** |
| 테스트 롤백 레시피 | 341–358 | **웹 2차 확인.** SQLAlchemy 2.0 `session_transaction.html` 원문에 `Session = sessionmaker()`·`engine.connect()`·`connection.begin()`·`join_transaction_mode="create_savepoint"`·`trans.rollback()` 전부 실재하며 **동기 `Session` 기준**임도 확인. line 358의 *"`AsyncSession` 판은 관련된 두 문서 페이지 어디에도 없다. 전수 확인은 아니니 '그 두 페이지에는 없다'까지만 말하겠다"*는 §5-A의 지시문(*"'그 두 페이지에는 없다'로만 표현하라"*)을 **문자 그대로** 이행 |
| 커넥션 풀 기본값 표 5행 | 364–376 | §1-6 표와 **전건 일치**(5 / 10 / 30.0 / -1 / False). *"none of them 'pre create' connections"* 축자 ✅ |
| **HikariCP `minimumIdle`** | 376 | 제약 10이 허용한 **레퍼런스 근거 2건 중 하나**를 정확히 사용(§1-6 저자 해석). 그 외 Spring 측 설정 키·기본값·엔드포인트 경로는 **6장 전체에 0건** |
| 산술 | 378 | `pool_size`+`max_overflow` = 15 ✅ / 워커 4 × 레플리카 3 = 12 ✅ / 15 × 12 = 180 ✅ |
| pre-ping 한계 축자 | 391–395 | §1-6의 *"It is critical to note that the pre-ping approach does not accommodate for connections dropped in the middle of transactions…"* 일치 |
| Alembic 비동기 표면 | 399–415 | **웹 2차 확인.** Alembic Cookbook 원문에 *"…can be used with async DBAPI like asyncpg"* 축자 실재, `async_engine_from_config`·`poolclass=pool.NullPool`·`connection.run_sync(do_run_migrations)` 전부 실재. 계약 §8-2가 6장 소유로 지정한 T1을 [^6-5]로 정확히 해소 |
| autogenerate rename 경고 | 417–419 | §1-6 *"🔴 autogenerate가 컬럼 rename을 add+drop으로 처리한다 → 데이터 손실"* 일치 |
| 드라이버·성능 절제 | 421 | 계약 §4-3의 두 URL만 사용 ✅. **asyncpg "5x faster" 배수 인용을 명시적으로 거절**하고 *"2023년 6월의 자체 측정"*이라 밝힘 — §1-6의 *"조건 없이 인용 금지"* 준수. **aiomysql vs asyncmy 우열 단정 없음** ✅. asyncpg `json`/`jsonb` 문자열 반환 ✅ |
| SQLModel 중립 근거 | 425–431 | §1-6 축자 + `0.0.39`(2026-06 기준) ✅. §4-5의 *"버전 번호 자체가 성숙도 신호"* 프레임 준수, 검증 무력화 주장(목록만 확인)은 **쓰지 않음** ✅ |
| **`@Transactional` 절 — 인용문 날조 점검** | 274–284 | **인용문 0건 ✅.** §7-2가 *"`@Transactional` 부재에 대한 직접 인용 — 구조적 근거(#11107)만 있고 인용문 없음"*이라 신고한 구역인데, 저술가는 **인용을 한 건도 만들지 않고** 구조 서술로만 처리했다 |
| **원인의 사람 귀속 거부** | 252 | *"여기서 원인을 사람에게 돌리고 싶은 유혹이 생기는데, 그건 이 책이 하지 않는 서술이다. 확인된 건 코드의 동작뿐이다."* — §7-2 최대 금지선 준수 |
| velog 반전 소재 | 437–443 | §3-10의 반전(*"Spring으로 갔는데도 N+1과 연관관계 문제를 다시 겪었다"*)을 정확히 사용. 페치 조인·네이티브 쿼리·엔티티 상속 ✅. 결론 *"N+1은 프레임워크가 아니라 ORM의 문제"* ✅ §3-10 저자 해석·§4-2와 일치 |

---

## 🚨 최우선 표적 — 코드 API 표면 대조 결과

**추출 범위:** 4장 8블록 · 5장 8블록 · 6장 13블록 = **총 29개 코드 블록.** 모든 import 경로 문자열·클래스명·함수명·데코레이터·파라미터명·**코드 주석**을 추출해 `01_reference.md` §1-2·§1-3·§1-6·§5-A와 `tracker_contract.md` §8로 대조했다.

| 판정 | 건수 | 내역 |
|---|---|---|
| ✅ 추적됨 (§8-1) | **58** | `Depends`(3파라미터 전부)·`Annotated`·`FastAPI(title=, lifespan=)`·`app.state`·`app.dependency_overrides`·`APIRouter(prefix=, tags=)`·경로 데코레이터(`status_code`·`response_model`)·`Query(ge=, le=)`·`run_in_threadpool`·`anyio.to_thread.run_sync`·`CapacityLimiter`·`current_default_thread_limiter().total_tokens`·`DeclarativeBase`·`Mapped[]`·`mapped_column(primary_key=·index=·unique=·default=·server_default=)`·`relationship(back_populates=·cascade=·secondary=·lazy="raise")`·`ForeignKey`·`String(n)`·`__tablename__`·`select()`·`session.scalars()`·`session.scalar()`·`selectinload`·`AsyncSession`·`create_async_engine`·`expire_on_commit=False`·풀 5인자·`AsyncAdaptedQueuePool`·`postgresql+asyncpg`·`sqlite+aiosqlite`·`join_transaction_mode="create_savepoint"`·`engine.connect()`/`begin()`/`rollback()`·`AsyncAttrs`/`awaitable_attrs`·`run_sync` 등 |
| ✅ T1 → 각주로 해소 | **9** | `starlette.middleware.base.BaseHTTPMiddleware`·`starlette.types`(`ASGIApp`·`Scope`·`Receive`·`Send`)·`dispatch(request, call_next)`·미들웨어 스택 순서 → **[^4-1]** / `app.add_middleware` → **[^4-2]** / `httpx.AsyncClient(timeout=)`·`.aclose()` → **[^4-3]** / `exception_handlers` 생성자 인자 → **[^4-4]** / `from anyio import to_thread` → **[^5-1]** / `DateTime`·`Text`·`func.current_timestamp()`·자동 Enum 매핑 → **[^6-1]** / `relationship(secondary=)` → **[^6-2]** / `selectinload`·`lazy="raise"` → **[^6-3]** / `async_sessionmaker`·`sqlalchemy.ext.asyncio` import 경로 → **[^6-4]** / Alembic `env.py` 비동기 표면 → **[^6-5]** |
| ✅ 면제 (§8-0 표준 라이브러리) | **8** | `typing`(`Annotated`·`AsyncIterator`·`Literal`) · `contextlib.asynccontextmanager` · `datetime` · `enum` · `uuid.uuid4` · `functools.partial`(인용 소스 내부) |
| ✅ 면제 (§3 저자 발명) | **21** | `SessionDep`·`SettingsDep`·`CurrentUser`·`IssueServiceDep`·`get_session`·`get_current_user`·`get_issue_service`·`RequestIdMiddleware`·`generate_thumbnail`·`Issue`·`IssueStatus`·`IssuePriority`·`ProjectMember`·`ProjectRole`·`Attachment`·`IssueRepository`·`IssueService`·`Page`·`CommentRead`·`session_factory` 등 |
| ⚠️ 각주 범위 확장 권장 | **7** | `.where()`·`.order_by()`·`.limit()`·`.offset()`·`Issue.id.desc()`·`result.all()`·`list(result)` (6장 ⚠️-6) |
| ❌ 추적 실패 | **0** | — |
| 🕒 T3 코드 단정 | **0** | — |

**⚠️ 배치 1의 구멍(경로 문자열 별도 grep) 재적용 결과:**

| import 경로 문자열 | `01_reference.md` grep | 처리 | 판정 |
|---|---|---|---|
| `sqlalchemy.ext.asyncio` | **0건** | **2장이 각주로 소유** + 6장 [^6-4]가 `async_sessionmaker`분 재확인 | ✅ (해소됨) |
| `starlette.types` | **0건** | 4장 [^4-1]이 `ASGIApp`·`Scope`·`Receive`·`Send`를 **경로째 명시** | ✅ |
| `starlette.middleware.base` | **0건** | 4장 [^4-1]이 *"import 경로 `starlette.middleware.base`"*를 **문자열로 명시** | ✅ |
| `from anyio import to_thread` | **0건** | 5장 [^5-1]이 **호출 형태째** 명시 | ✅ |
| `sqlalchemy.orm` | 1건 | §1-6 Quickstart 원문에 실재 | ✅ |
| `from httpx import AsyncClient` | 1건 | §1-5 + [^4-3] | ✅ |
| `contextlib` / `uuid` / `enum` / `typing` | 0건 | §8-0 표준 라이브러리 면제 | ✅ |

**코드 주석 검사 (적발 사례 1 = 가짜 주석):** 29블록의 주석 전수 확인. **동작을 설명하는 주석 0건.** 주석은 전부 ① 파일 경로(`# src/tracker/deps.py`) ② `# (개념 설명용 — 파일 아님)` ③ `# ...(N장, 생략)` ④ `# ✅ 2.0 스타일` / `# ❌ 1.x 어휘` 대조 라벨 — 계약 §6-2·§6-3의 표기 규약이고 **계획 제약 9-(B)-4의 주석 금지선 위반 0건.**

**`status.HTTP_422_*` 검사:** `grep "HTTP_422\|UNPROCESSABLE"` → **0건.** 4장은 `status_code=201` **정수 리터럴**을 써서 3장이 확정한 정수 방식과 일치한다. 다른 `status.*` 상수도 0건.

---

## 🚨 마커 4건 판정

| # | 장·line | 항목 | 판정 | 조치 |
|---|---|---|---|---|
| **1** | 4장 226 | 예외 핸들러의 **하위 클래스 해석** | **✅ 확인됨 — 웹 2차 확인으로 성립** | 마커 삭제 + **단정형으로 승격 가능** |
| **2** | 4장 262 | lifespan의 멀티 워커·서버리스 동작 | **🕒 검증 불가 (정당한 T3)** | 마커 문자열만 삭제, 산문 유지 |
| **3** | 5장 214 | free-threading 기본 빌드 전환 · 40-스레드 영향 | **🕒 검증 불가 (정당한 T3)** | 마커 문자열만 삭제 + 시점 명기 1회 |
| **4** | 6장 433 | Motor → PyMongo async 공식 이행 경로 | **🕒 검증 불가 (정당)** | 마커 문자열만 삭제, 산문 유지 |

### 마커 1 상세 — 3장 영향 판정 포함

**웹 2차 확인 (Critical + 3장 설계 토대):** 저술가는 *공식 문서*에서 해당 문장을 찾다 실패했다. 그러나 이 책의 자체 규약(§6-2 R21 — 고정 태그 소스 코드가 1차 소스이며 5장이 이미 `starlette/concurrency.py`를 그렇게 인용한다)에 따라 **소스를 확인했다.**

- **소스:** Starlette **태그 1.3.1**(레퍼런스 §버전 핀 B의 현행 핀) `starlette/_exception_handler.py`
- **확인된 코드:**
  ```python
  def _lookup_exception_handler(exc_handlers, exc):
      for cls in type(exc).__mro__:
          if cls in exc_handlers:
              return exc_handlers[cls]
      return None
  ```
- **판정:** 핸들러 조회가 예외 타입의 **MRO를 순회**한다. 따라서 **부모 클래스에 등록한 핸들러가 하위 클래스를 받는다** — 저술가의 *"부모에 건 핸들러가 자식까지 받는다는 뜻으로 읽힌다"*는 **읽기가 아니라 사실**이다.

**➡️ 3장 영향: 없다 (설계 안전).** 3장 line 237–246·264·283은 루트 `TrackerError` 하나에 `DomainError(TrackerError)`·`InfrastructureError(TrackerError)`를 두고 **`@app.exception_handler(TrackerError)` 하나로 전부 받는** 구조다. 이 설계는 정확히 위 MRO 순회에 의존하며, **이제 1차 소스로 뒷받침된다.** 「핸들러 3개」 계약은 유효하고 3장은 **재저술 불필요**다.

**정정안 (4장 line 226):**
> ~~해석 규칙 하나는 확인 중이라고 밝혀두자.~~ → **해석 규칙 하나를 못 박아두자. 등록한 예외 클래스의 하위 클래스까지 같은 핸들러가 받는다.** Starlette 1.3.1 소스의 핸들러 조회가 예외 타입의 MRO를 거슬러 올라가며 등록부를 찾기 때문이다.[^4-5] 공식 문서도 같은 성질 위에 서 있다 — `HTTPException` 핸들러를 걸 때 *"you should register it for Starlette's `HTTPException`"*이라고 권하고, FastAPI의 `HTTPException`이 그 클래스를 상속한다고 함께 밝힌다.[^4-4] **3장이 핸들러를 셋으로 묶어둘 수 있었던 근거가 이것이다.**

> `[^4-5]: 예외 핸들러 조회가 `type(exc).__mro__`를 순회한다는 사실 — starlette 1.3.1 태그 소스 `starlette/_exception_handler.py`의 `_lookup_exception_handler()` (조회 2026-07-26)`

---

## 교차 충돌 점검 (1~3장 최종본 × 4~6장)

**모순 0건.** 함께 읽어야만 보이는 항목을 전수 대조했다.

| # | 대조 축 | 결과 |
|---|---|---|
| 1 | **4장 ↔ 3장 에러 계약** | ✅ 4장 `request.state.request_id` ↔ 3장 `getattr(request.state, "request_id", "")` — **키 이름 일치.** 4장이 심고 3장이 꺼내는 방향도 정확. 4장 line 222가 *"응답 계약 자체는 3장이 끝까지 책임지므로 여기서는 메커니즘만"*으로 계약 §7 4장 행(*"예외 처리 '메커니즘'만"*)을 그대로 이행. `X-Request-ID` 헤더명은 4장 신규이며 3장과 충돌 없음 |
| 2 | **4장 ↔ 3장 상태 코드 표기** | ✅ 4장 `status_code=201` **정수 리터럴** — 3장이 배치 1 판정으로 확정한 정수 방식과 일치. 배치 1에서 터진 유형(핀 하한에서 안전하지 않은 `status.*` 상수)의 **재발 없음** |
| 3 | **4장 ↔ 1장 락파일 경고** | ✅ **모범 사례.** 4장 line 274가 `on_event` 가동 여부를 *"당신의 `uv.lock`이 어떤 Starlette을 물어왔는지에 달려 있다"*로 귀결시킨다 — 배치 1에서 3장이 위반했던 바로 그 1장 제약(`starlette>=0.46.0`이라 0.4x일 수도 1.x일 수도 있다)을 **4장은 정확히 적용**했다 |
| 4 | **6장 ↔ 2장 골격** | ✅ `IssueService.__init__` → `self.session` + `self.issues = IssueRepository(session)`(2장 line 166–169)를 6장이 그대로 전제. 시그니처 확장(`create_issue`에 `author_id` 추가, `list`에 `limit`·`offset` 추가, 반환 `None`→실타입)은 **계약 §7의 6장 「바꾼다」 열**(*"리포지터리·서비스에 실제 쿼리 채움"*)이 허용한 범위이고, 2장 스스로 *"지금 확정한 것은 이름과 생성자 모양뿐이다"*라고 선언해 두었다 — **위반 아님** |
| 5 | **6장 ↔ 4장 `deps.py`** | ✅ 계약 §7 교차 규칙 2(*"완성 ≠ 재정의"*) 준수. 4장 스텁 `async def get_session() -> AsyncIterator[AsyncSession]`을 6장이 **시그니처 그대로** 완성하고 line 311이 *"시그니처는 그대로다"*를 명시. 6장 `deps.py` 재게시가 `SessionDep`만 싣고 `# ...(4장, 생략)`으로 닫은 것도 §6-3 규약대로 |
| 6 | **5장 ↔ 1장 "그 숫자"** | ✅ **정확히 회수.** 1장 line 27 *"동시성이 왜 그 숫자에서 막히는지는 anyio 소스에 있다"* → 5장 line 5가 그 문장을 **직접 인용해 되받고** 네 층을 내려가 40에 도달 |
| 7 | **5장 ↔ 4장 예고** | ✅ 4장 line 125 *"동기 의존성이 무엇을 대가로 지불하는지는 5장이 숫자로 보여준다"* → 5장 「그 40을 의존성이 함께 쓴다」 절이 회수 |
| 8 | **6장 ↔ 5장 프로세스 경계** | ✅ 5장 line 166 *"워커는 메모리를 공유하지 않는다"* → 6장 line 378(풀 × 워커 × 레플리카 = 180)·line 270(*"5장의 프로세스 경계 안쪽에 경계가 하나 더"*)이 양쪽에서 회수 |
| 9 | **버전·심볼 표기 일관** | ✅ `0.140.0`·`1.3.1`·`4.14.2`·`0.51.0`·`2.0.51`·`1.18.5`·`0.0.39`·`8.0.1`·`4.17.0`·`3.7.1` 전부 §버전 핀 테이블과 일치. `"{버전} / {연월} 기준"` 형식(§5-1 규율)이 4·5·6장 전반에 적용됨. **표기 충돌 0건** |
| 10 | **각주 중복** | ⚠️ **1건.** 6장 [^6-4]가 *"`create_async_engine`·`async_sessionmaker`·`AsyncSession`의 import 경로"*를 각주하는데, `AsyncSession`의 import 경로 `sqlalchemy.ext.asyncio`는 **2장이 이미 각주로 소유**(02_final line 178)한다. 계약 §8-2가 `async_sessionmaker`를 6장 소유로 배정했으므로 [^6-4] 자체는 정당하며, **`AsyncSession`분만 중복**이다. 비차단 — 편집 단계 정리 대상 |
| 11 | **미회수 약속** | ⚠️ **1건.** 5장 line 71 *"그래서 이 이야기는 6장에서 다시 만난다"*(동기 `yield` 정리 코드 ↔ 커넥션 풀 교착)를 **6장이 받지 않는다.** 6장은 풀·세션·트랜잭션을 다루되 `exit_limiter`/정리 순서 교착을 재론하지 않는다. 비차단 — 5장의 고리를 지우거나 6장 「@Transactional이 있던 자리」 절에 한 문장 추가 |

---

## 배치 2 종합

| 장 | ❌ | ⚠️ | 🕒 | 코드 심볼 추적 실패 |
|---|---|---|---|---|
| 4장 | **0** | 3 | 1 (마커) | **0** |
| 5장 | **0** | 3 | 1 (마커) | **0** |
| 6장 | **0** | 8 | 1 (마커) | **0** |

### 🚨 Phase 5 차단 사유 — 정확히 3건

1. **4장 line 262** — `(사실 확인 필요)` 문자열 삭제 (판정 🕒 완료, 산문 유지)
2. **5장 line 214** — `(사실 확인 필요)` 문자열 삭제 + 시점 명기 1회 (판정 🕒 완료)
3. **6장 line 433** — `(사실 확인 필요)` 문자열 삭제 (판정 🕒 완료, 산문 유지)

**세 건 모두 판정이 끝났고 남은 조치는 문자열 삭제뿐이다.** 마커 1(4장 226)은 ✅로 해소되어 차단에서 빠졌고, 정정안(단정형 승격 + [^4-5] 신설)은 위에 제시했다. 그 밖의 ⚠️ 14건은 조치 권장이나 **Phase 5를 차단하지 않는다.**

### 웹 2차 확인 6건 (전건 실재 — 날조 0건)

| # | 대상 | 결과 |
|---|---|---|
| 1 | Starlette 1.3.1 `_exception_handler.py` | ✅ MRO 순회 확인 — **마커 1 해소** |
| 2 | FastAPI Advanced Middleware ([^4-2]) | ✅ 축자 일치 · `add_middleware` 형태 일치 |
| 3 | httpx Timeouts ([^4-3]) | ✅ 기본 5초 확인 |
| 4 | SQLAlchemy `session_transaction.html` (6장 인용 코드) | ✅ `Session = sessionmaker()` 포함 전문 실재 · 동기 `Session` 기준 확인 |
| 5 | Alembic Cookbook ([^6-5]) | ✅ 축자 *"can be used with async DBAPI like asyncpg"* 실재 · `env.py` 3요소 실재 |
| 6 | SQLAlchemy ORM Quickstart (6장 출처 표기) | ✅ 축자·URL 일치 |

**§7-5가 경고한 유형(가짜 주석 · 없는 import 경로)의 재발 없음.** 날조된 URL·인용문·import 경로·수치는 **한 건도 발견되지 않았다.**

### 총평

배치 2는 **사실 오류 0건**이다. 리서치 공백(§7)의 최대 지뢰밭인 5장이 WebFlux 교차 경험담 0건·출신 귀속 저자 가설 표시·Mark Shannon 반론 병기·Kotlin 언어 불일치 명시를 **네 개 다** 통과했고, 6장은 `@Transactional` 인용문을 만들지 않았으며 `expire_on_commit`·N+1의 정량 수치를 **하나도 지어내지 않았다.** 4장은 `on_event` 3층과 `Depends(scope=)` 미확정을 지뢰표 문구 그대로 지켰다. 의심 식별자(형식 이례 arXiv ID·미래 날짜·해석 불가 DOI/URL)는 **0건**이며, 저술가가 스스로 신고한 마커 4건 중 하나는 웹 2차 확인으로 **✅ 승격**되어 3장 「핸들러 3개」 설계의 근거가 오히려 두꺼워졌다. 남은 차단 사유는 마커 문자열 3개의 삭제뿐이다.

---

## 배치 2 — 라운드 1 보론 (웹 2차 확인 2건 추가, 총 8건)

배치 1이 확립한 규율 두 가지를 배치 2 자신에게 되적용했다.

### (가) 핀 범위 전체 대조 — 마커 1의 ✅ 확정

배치 1은 3장 422 상수를 판정할 때 Starlette **태그 2개(1.3.1 · 0.46.0)**를 대조했다. 마커 1도 같은 잣대를 받아야 한다 — FastAPI는 `starlette>=0.46.0`으로만 핀하므로 **1.3.1에서만 확인된 성질은 독자의 락파일에서 성립을 보장하지 못한다.** (4장 line 274가 `on_event`에 대해 지적한 바로 그 논리다.)

| 태그 | 파일 | 결과 |
|---|---|---|
| **1.3.1** (현행 핀) | `starlette/_exception_handler.py` | `for cls in type(exc).__mro__: if cls in exc_handlers: return exc_handlers[cls]` ✅ |
| **0.46.0** (핀 하한) | 동상 | **동일 코드 ✅** (중립 질의로 독립 재확인 — 1차 확인의 유도 질문 편향 배제) |

**➡️ 하위 클래스 해석은 FastAPI가 허용하는 Starlette 전 구간에서 성립한다.** 마커 1의 ✅ 판정과 「정정안(단정형 승격)」은 그대로 유효하며, **3장 「핸들러 3개」 설계는 락파일이 무엇을 물어오든 안전하다.** 배치 1이 3장에서 적발한 유형(핀 하한에서 무너지는 상수)의 재발이 이 항목에는 없다.

**[^4-5] 정정 (양 태그 병기):**
> `[^4-5]: 예외 핸들러 조회가 `type(exc).__mro__`를 순회한다는 사실 — starlette 소스 `starlette/_exception_handler.py`의 `_lookup_exception_handler()`. **핀 하한 0.46.0과 현행 1.3.1 양쪽에서 동일함을 확인했다** (조회 2026-07-26)`

### (나) `[^4-1]` 내용·축자 대조 (URL 실재 확인에서 승격)

배치 1의 기준은 *"각주 URL 전건 실재(**내용·축자까지 대조**)"*였다. `[^4-1]`은 배치 2에서 가장 많은 표면을 묶은 각주(8개 항목)이므로 정본 URL 확인만으로는 부족하다고 판단해 원문을 열었다.

| `[^4-1]`이 주장하는 것 | Starlette 공식 문서 Middleware 원문 | 판정 |
|---|---|---|
| `dispatch(self, request, call_next)` 시그니처 | `async def dispatch(self, request, call_next)` | ✅ |
| `__init__` 오버라이드 시 `super().__init__(app)` | `CustomHeaderMiddleware` 예제에 실재 | ✅ |
| 순수 ASGI 미들웨어 `__init__`/`__call__` 형태 | `class ASGIMiddleware`에 `def __init__(self, app)` + `async def __call__(self, scope, receive, send)` | ✅ (4장 line 155–163과 **구조 일치**) |
| `starlette.types`의 `ASGIApp`·`Scope`·`Receive`·`Send` | 해당 모듈에서 임포트함을 명시 | ✅ |
| `response.headers[...]` 조작 | 같은 예제가 응답 헤더에 값을 심는다 | ✅ |
| **미들웨어 스택 순서** | `ServerErrorMiddleware` → `TrustedHostMiddleware` → `HTTPSRedirectMiddleware` → `ExceptionMiddleware` → Routing → Endpoint | ✅ 4장의 *"서버 에러 처리 → 사용자가 선언한 미들웨어(선언 순서대로) → 예외 처리 → 라우팅 → 엔드포인트"*는 이 구체 예시의 **정확한 일반화**다(가운데 둘이 사용자 선언 미들웨어). **line 228의 "예외 핸들러는 미들웨어 스택 안쪽에서 동작한다"도 이 순서로 뒷받침된다** |
| `request.headers`가 *"an immutable, case-insensitive, multi-dict"* | **Starlette Requests 페이지(별도 URL) 미대조** | ⚠️ **잔여** — 축자 1건만 내용 대조 미수행 |

**➡️ `[^4-1]`은 8개 항목 중 7개가 원문 대조로 확인됐고, `request.headers` 축자 1건만 URL 정본 확인에 머문다.** 비차단.

### 웹 2차 확인 최종 집계

**8건 전건 실재 · 날조 0건.** (1) Starlette 1.3.1 `_exception_handler.py` (2) **Starlette 0.46.0 동상** (3) FastAPI Advanced Middleware (4) **Starlette Middleware 문서 전문** (5) httpx Timeouts (6) SQLAlchemy `session_transaction.html` (7) Alembic Cookbook (8) SQLAlchemy ORM Quickstart.

### 잔여 위험 재정리 (❌ 0건 상태에서의 실질 위험)

차단 3건은 **마커 문자열 삭제라는 사무적 조치**이므로 위험도 순위와 분리해 읽어야 한다. 실질 위험은 다음 셋이다.

1. **`IssueRepository.add()` 미정의 호출** (6장 210 vs 175–196) — 인쇄된 코드가 `AttributeError`를 낸다. 하네스에 컴파일 단계가 없으므로 이 대조가 유일한 방어선이었다. **⚠️ 중 가장 실물에 가까운 결함.**
2. **6장 line 272 `engine.dispose()` 누락 증상을 "경고"로 서술** — 레퍼런스는 `RuntimeError: Event loop is closed`. 에러를 경고로 낮춘 서술.
3. **`[^4-1]`의 `request.headers` 축자 1건 내용 미대조** (위 (나)).

마커 1은 (가)로 핀 범위 전체가 확인되어 **잔여 위험에서 제외**한다.

---

# 배치 3 — 7·8·9장 (라운드 1 · 2026-07-26)

**대조 근거:** `01_reference.md` 버전 핀 테이블 B/C/D/G · §1-2 · §1-4 · §1-5 · §3-1 · §5 · §7-2/7-3/7-4/7-5 · 신선도 원장 / `tracker_contract.md` §3 · §4-7 · §4-8 · §6 · §7 성장 맵 · §8 (T1/T2/T3) / `02_plan.md` 뉘앙스 지뢰 배정표 / `research/web_deploy.md` §1-A~§1-G · §6-4 / `chapters/01_final.md`~`06_final.md` (교차 충돌)

**웹 2차 확인 5건 (전건 실재 · 날조 0건):** ① `starlette/formparsers.py` @1.3.1 ② `fastapi/routing.py` @0.140.0 ③ FastAPI *Server-Sent Events* 문서 ④ FastAPI *Frontend* / *Static Files* 문서 ⑤ FastAPI 릴리스 노트 0.138.0~0.140.0

---

## 7장

### ✅ 확인됨

- **(line 36) "uvicorn 0.51.0 / 2026-07 기준 `--ws` 선택지는 다섯이다 — `auto`·`none`·`websockets`·`websockets-sansio`·`wsproto`"** — `01_reference.md` §1-5와 항목·개수 일치. (참고: `research/web_deploy.md` line 127이 같은 5개를 열거하면서 "4종"이라 오기했는데, **원고가 맞고 리서치 노트가 틀렸다.** 원고는 레퍼런스 §1-5를 따랐다.)
- **(line 38) SansIO 축자 인용** — `research/web_deploy.md` line 124 원문과 축자 일치.
- **(line 34) "uvicorn 기본 설치에는 구현체가 없고 `uvicorn[standard]`가 `websockets`를 설치한다"** — §1-5 및 §5-D(`uvicorn[standard]` 6종 / 기본은 `h11`+`click`)와 일치.
- **(line 82) 공식 `ConnectionManager` 한계 축자** — `web_deploy` line 103·222 원문과 일치. 앞머리 "But keep in mind that,"를 잘라 문장 중간에서 시작하나 의미 변형 없음.
- **(line 88) "그 저장소는 2025-08-19에 아카이브됐다. PyPI 최신 릴리스는 0.3.1 / 2024-08-01"** — `web_deploy` line 225 저장소 원문 *"This repository was archived by the owner on Aug 19, 2025"* + 핀 테이블 G(0.3.1 / 2024-08-01). **날짜·버전 양쪽 확인.**
- **(line 90) broadcaster README Alpha 축자** — `web_deploy` line 228과 일치(문장 경계에서 절단).
- **(line 92) "공식 문서가 아카이브된 라이브러리를 아직 링크하고 있다. 공식 대체재 안내도 없다"** — §1-5 🔴 항목 + `web_deploy` line 1692("없음")와 정확히 일치. **과장 아님.**
- **(line 166) "SSE는 FastAPI 0.135.0(2026-03-01)에 정식 지원으로 들어왔다"** — §3-1 릴리스 노트 헤더 날짜 표와 일치.
- **🌐 (line 170) `from fastapi.sse import EventSourceResponse, ServerSentEvent`** — **웹 2차 확인.** FastAPI 공식 *Server-Sent Events* 문서가 정확히 이 import 문을 싣는다. **import 경로 문자열 확인 완료** (2장에서 구멍이 났던 유형 — 여기서는 통과).
- **🌐 (line 173–177) `@app.get(..., response_class=EventSourceResponse)` + `-> AsyncIterable[Item]` + `for item in items: yield item`** — 공식 문서 예제와 축자 일치.
- **🌐 (line 181) "`AsyncIterable[Item]`이라고 적으면 … Pydantic 검증과 자동 문서화가 그대로 따라온다"** — 문서 축자 *"FastAPI will use it to validate, document, and serialize the data using Pydantic."*
- **🌐 (line 185) 15초 핑 · `Cache-Control: no-cache` · `X-Accel-Buffering: no` 3중 인용** — 공식 문서 3개 항목 전건 축자 일치.
- **🌐 (line 187) `Last-Event-ID` 재접속 서술** — 문서 축자 *"When a browser reconnects after a connection drop, it sends the last received `id` in the `Last-Event-ID` header."*
- **(line 189) "`sse-starlette`은 3.4.6 / 2026-07 기준으로 여전히 릴리스되고 … 겹치는 영역에서 1차 선택지가 옮겨간 것"** — 핀 테이블 G(3.4.6 / 2026-07-20)와 일치. **뉘앙스 판정: 폐기 단정 없음 → 통과** (아래 「뉘앙스 지뢰」 참조).
- **(line 214) nginx `X-Accel-Buffering` 축자** — `web_deploy` line 215 nginx 공식 문서 원문과 일치. `proxy_buffering` 기본값 `on`도 line 213에서 확인.
- **(line 231) "20초 간격의 핑과 20초의 핑 타임아웃, 16MB의 메시지 크기 상한, 32라는 수신 큐 상한"** — `web_deploy` line 129–130 [S10] uvicorn 공식 문서: `--ws-ping-interval` 20.0 / `--ws-ping-timeout` 20.0 / `--ws-max-size` 16777216 / `--ws-max-queue` 32. **네 숫자 전건 확인.**
- **(line 138) `aioredis`는 redis-py에 흡수 → `uv add redis`** — §1-6 및 §4-8 금지 목록과 일치.
- **(line 42) ASGI 이벤트 이름(`websocket.connect`/`receive`/`disconnect` ↔ `accept`/`send`/`close`) 및 101 승격** — `web_deploy` line 112–115 [S11] 원문과 일치.
- **코드 관용구:** `APIRouter(tags=["realtime"])` prefix 없음 → 계약 §3-7 표와 일치. `IssueEvent`(`issue_id`·`event_type`·`payload`·`occurred_at`, `schemas/common.py`) → §3-8과 필드·파일까지 일치. `EventBus`·`RedisEventBus`·`InMemoryEventBus`(`events.py`) → §3-8 일치. `get_event_bus()`/`EventBusDep` → §3-4 명명 규약(`get_{명사}`) 및 별칭 체계 일치.
- **`📐 저자 설계` 마커 4건**(line 58·96·237) — 계약 §5 grep 토큰 형태 정확. 계획서가 의무로 지정한 「7장 팬아웃·알림 파이프라인」 충족.
- **`> 출처:` 표기 2건**(line 28·179) — 계약 §6-4 형태 준수.
- **코드 주석 전수 검사: 날조 0건.** 10개 블록의 주석은 전부 파일 경로(§6-2) 또는 `# ...(N장, 생략)`(§6-3)이며, 동작 설명을 지어 넣은 주석(§4-8 금지·날조 사례 1 유형)은 **없다.**

### ⚠️ 근거 부족 — 조치 필요

- **(line 247) `issue = await self.issues.get(issue_id)` 직후 `issue.status = status` / `issue.id` — None 가드 없음**
  **근거:** `06_final.md` line 210이 `async def get(self, issue_id: int) -> Issue | None:`으로 선언한다. 반환이 `None`일 수 있는데 원고는 곧바로 속성에 대입하고 `issue.id`를 읽는다. 계약 §4-7이 "타입이 설명 장치"라고 못 박은 책에서 인쇄된 코드가 타입 검사를 통과하지 못한다.
  **[정정안]** 한 줄 추가 — 3장이 이미 제공한 예외를 쓴다:
  ```python
  issue = await self.issues.get(issue_id)
  if issue is None:
      raise NotFoundError("이슈가 없다", code="issue.not_found")
  ```
  (`NotFoundError` 생성자 형태는 `03_final.md` line 281과 일치.)

- **(line 240–258) `services/issue.py` 블록의 import 누락 — `# ...(6장, 생략)`이 덮지 못하는 이름 4개**
  **근거:** 생략 마커는 §6-3에 따라 **"앞 장에서 이미 쓴 코드"**를 뜻한다. 그런데 이 블록이 쓰는 `EventBus`·`IssueEvent`는 **이 장에서 처음 생긴 것**이고, `IssueStatus`(§3-1, 6장)·`timezone`도 6장 `services/issue.py`에 있던 코드가 아니다. 독자가 그대로 옮기면 `NameError`가 난다.
  **[정정안]** 블록 상단에 3줄을 노출한다:
  ```python
  from datetime import datetime, timezone

  from tracker.events import EventBus
  from tracker.models.issue import IssueStatus
  from tracker.schemas.common import IssueEvent
  ```

- **(line 244–246) `change_status`의 시그니처가 2장 스텁과 어긋난다**
  **근거:** `02_final.md` line 174가 `async def change_status(self, issue_id: int, status: str) -> None:`으로 선언했다. 7장은 `status: IssueStatus`·`events: EventBus` 추가·`-> Issue`로 바꾼다. 계약 §7 성장 맵은 7장이 `services/issue.py`를 **바꾼다**고 허용하므로 `events` 추가와 반환형 변경은 정당하나, **2장 독자에게는 시그니처가 소리 없이 갈린다.**
  **[정정안]** 차단 아님. 한 문장 추가 권장 — *"2장의 스텁은 `status: str`이었다. 6장에서 `IssueStatus`가 생겼으니 여기서 타입을 좁히고, 발행을 위해 인자를 하나 더 받는다."* (이 문장이 없으면 9장의 ❌ 항목이 왜 깨졌는지도 설명되지 않는다.)

- **(line 227) 인용문에서 조건절이 잘렸다**
  **[원문]** *"Uvicorn ensures the ASGI `send` messages will only return once the write buffer has been drained below the low water mark."*
  **근거:** `web_deploy` line 146 원문은 **"If the write buffer passes a high water mark, then** Uvicorn ensures…"로 시작한다. 조건이 사라져 무조건적 서술로 읽힌다. (다행히 바로 뒤 산문 *"즉 버퍼가 차면"*이 조건을 복원하므로 의미 왜곡은 없다.)
  **[정정안]** 선행 생략 부호를 넣거나 조건절을 살린다 — *"If the write buffer passes a high water mark, then Uvicorn ensures…"*

- **(line 231) 16MB·32가 `websockets` 프로토콜 전용이라는 조건이 빠졌다**
  **근거:** `web_deploy` line 129가 `--ws-max-size`·`--ws-max-queue`에 **"(`websockets` 프로토콜 전용)"**을 병기한다. 기본값이 `auto`→`websockets`이므로 실무상 성립하지만, `wsproto`를 고른 독자에게는 틀린 수치가 된다.
  **[정정안]** *"(구현체를 `websockets`로 둔 경우)"* 한 구절 추가.

### 🕒 마커 판정 — 1건

- **(line 138) "커넥션 풀 … 기본 크기는 확인하지 못했다 (사실 확인 필요)"** → **🕒 검증 불가 · 서술은 적법**
  **근거:** 계약 §8-4 T3 표에 **"redis-py asyncio `ConnectionPool` 기본값 | 7"**로 등재된 항목이고, `01_reference.md` §1-6도 *"⚠️ asyncio `ConnectionPool` 기본값은 미확인"*으로 신고했다. 원고는 **숫자를 지어내지 않고** 모른다고 적었다 — 계약이 지정한 정확한 처리다.
  **[final 전 조치 — 필수]** 판정은 통과지만 **`(사실 확인 필요)` 토큰은 독자용 원고에 남으면 안 된다.** 산문은 유지하고 마커 문자열만 지운다:
  > "클라이언트를 만들면 커넥션 풀이 함께 생기는데, **그 기본 크기는 이 책이 1차 소스로 확인하지 못했다.** 구독자가 연결을 오래 붙드는 구조이니 확인해 잡아두는 편이 낫다."

### 뉘앙스 지뢰 판정 (§7 · 계획서 배정표)

- **0.135.0 내장 SSE ↔ `sse-starlette` 관계 — ✅ 통과.** line 189가 *"그렇다면 `sse-starlette`은 쓸모없어졌을까? 그렇게 정리하면 틀린다"*로 시작해 **폐기 단정을 명시적으로 거부**하고, 3.4.6/2026-07 현행 릴리스와 남는 용도(Starlette 단독·종료 제어)를 제시한 뒤 *"겹치는 영역에서 1차 선택지가 옮겨간 것"*으로 착지한다. §1-5의 *"이제 1차 선택지가 아니다"*를 정확히 옮겼고 그 이상으로 나아가지 않았다. **어느 쪽도 폐기됐다고 말하지 않는다.**
- **Spring 측 사실 2건 — ✅ 통과.** ① STOMP 축자(line 50)는 `[^7-5]`가 `docs.spring.io/.../websocket/stomp.html`을 단다. ② `SseEmitter`(line 166)는 같은 각주가 `mvc-ann-async.html`을 단다. **둘 다 Spring 공식 문서 정본 URL이고 설정 키·기본값·엔드포인트 경로를 주장하지 않는다** — 인용한 것은 "상위 프로토콜 협상"이라는 프로토콜 서술과 `SseEmitter`라는 클래스 이름의 존재뿐이다. §7-2가 금지한 "Spring 측 설정값 주장"에 해당하지 않는다.
- **출신 귀속 — ✅ 위반 없음.** line 48 *"Spring에서 WebSocket을 다뤄봤다면 이쯤에서 위화감을 느낄 것이다"*, line 86 *"Socket.IO를 여러 인스턴스로 굴려봤다면"*은 **독자 경험에 대한 호명**이지 "Java 출신이라서 이렇게 실수한다"는 인과 귀속이 아니다. §7-2의 🚨 금지 사항에 걸리지 않는다.

### 양화사 점검

| 원문 | 판정 |
|---|---|
| (166) "검색으로 나오는 글의 **대다수**가 `sse-starlette`을 설치하라고 안내하는데" | ✅ §1-5 축자 *"인터넷 자료 대다수가 `sse-starlette` 설치를 안내한다"* — 레퍼런스가 같은 양화사를 쓴다 |
| (84) "코드는 자기가 아는 연결 **전부**에게 성공적으로 보냈다" | ✅ 코드 동작에 대한 논리적 서술(리스트 순회). 표본 일반화 아님 |
| (162) "같은 두 메서드를 메모리 위에 구현한 것이 **전부**" | ✅ 바로 위 코드 블록에 대한 서술 |
| (193) "네 가지 질문이 **대부분**을 결정한다" | ✅ 「저자 기준」 성격이나 표 자체가 프로토콜 속성의 나열이라 무해 |

**다수설 일반화 · Reddit/SO 인용 · `#14603` · `status.HTTP_422_*` — 전건 0건.**

### 7장 소계

| 기호 | 건수 |
|---|---|
| ❌ | **0** |
| ⚠️ | 5 |
| 🕒 | 1 (마커, 토큰 삭제로 해소) |
| ✅ | 22 |

---

## 8장

### ✅ 확인됨

- **🌐 (line 90–95) `starlette 1.3.1` `formparsers.py` 인용 블록 — 독스트링 2줄 포함 전부 실재**
  **이것이 이 배치에서 가장 위험도가 높다고 본 항목이었다.** 인용 블록이 `01_reference.md` §1-4에는 **없는** 독스트링 2줄(`"""The maximum size of the spooled temporary file used to store file data."""` / `"""The maximum size of a part in the multipart request."""`)을 싣고 있어, 계약 §4-8이 금지한 *"코드 주석에 동작 설명 지어 넣기"*(적발 사례 1 유형)일 가능성을 의심했다. **웹 2차로 `Kludex/starlette` 1.3.1 태그 원본을 열어 대조한 결과 — 클래스 선언·두 속성·`# 1MB` 주석·독스트링 2줄이 전부 축자 일치했다.** 날조 아님. **✅**
  ```python
  class MultiPartParser:
      spool_max_size = 1024 * 1024  # 1MB
      """The maximum size of the spooled temporary file used to store file data."""
      max_part_size = 1024 * 1024  # 1MB
      """The maximum size of a part in the multipart request."""
  ```
- **🌐 (line 105–113) 「선언형 경로에는 `max_part_size`를 넘길 손잡이가 없다」 — 저술가의 정정이 옳다**
  **저술가가 계획서를 소스로 뒤집은 판단이고, 검증 결과 맞다.** `fastapi/routing.py` @0.140.0을 열어 확인한 사실 2가지: ① 폼 파싱 호출은 파일 전체에서 단 한 곳이며 `body = await request.form()` — **인자가 없다** ② 같은 파일에 `MultiPartParser`·`spool_max_size`·`max_part_size`에 대한 참조가 **하나도 없다.** 즉 선언형 `UploadFile` 경로에는 파서 한도를 주입할 지점이 존재하지 않는다. **"올리면 된다"가 아니라 "올릴 자리가 없다"가 정확하다. 중요한 발견으로 확인한다.**
  (참고: 실제 소스는 `if is_body_form:` 분기 안에 있고 다음 줄이 `file_stack.push_async_callback(body.close)`다. 원고가 뽑은 한 줄은 정확한 발췌다.)
- **(line 99–103) `spool_max_size`(저장 위치) ↔ `max_part_size`(거부선) 분리 — ✅ 정확**
  §1-4가 *"`UploadFile`은 1MB를 넘는 순간 메모리에서 디스크로 스풀된다. '다 메모리에 올린다'도 '항상 디스크에 쓴다'도 둘 다 틀렸다"* + *"`max_part_size` 기본 1MB는 대용량 업로드에서 실제로 부딪히는 벽"*이라고 적은 것과 역할 분담이 정확히 일치한다. §1-4의 1MB는 §7-4에서 **✅ 해소됨**으로 등재된 사실이다.
  **핀 하한 점검:** `web_deploy` line 318이 `0.46.0 (2025-02-22) — "MultiPartParser: Rename max_file_size to spool_max_size"`를 기록한다. FastAPI가 핀하는 **하한 `starlette>=0.46.0`에서 이미 `spool_max_size`라는 이름이 존재**하므로, 이 절은 핀 범위 양끝에서 성립한다. **✅**
- **(line 212) "상수를 20메가바이트로 잡아뒀지만, 앞 절의 파트 한도를 그대로 뒀다면 여기 닿기 전에 파서가 먼저 거절한다"** — 두 값의 관계에서 따라 나오는 정확한 연역. 앱 레벨 검사가 파서 한도 아래에서는 무의미하다는 지적은 옳다. ✅
- **(line 115) "서블릿 진영의 멀티파트 최대 파일 크기 기본값 역시 1메가바이트"** — §1-4 ▶저자 해석의 `spring.servlet.multipart.max-file-size` 기본 1MB. **레퍼런스가 근거를 가진 Spring 측 사실 2건 중 하나**이며, 원고는 설정 키 이름을 주장하지 않고 값만 대조한다. ✅
- **(line 11·15·17) `BackgroundTasks` 계약 3인용** — §1-5 및 `[^8-1]` 정본 URL과 일치. *"It can be an `async def` or normal `def` function"*·Celery 권유 문단·*"small background tasks (like sending an email notification)"* 전건.
- **(line 21) uvicorn *"wait for any background tasks to run to completion"*** — §1-5 축자 그대로.
- **(line 23) "이슈 #14137(2025-10) … tiangolo가 제시한 처방은 `Depends(func, scope="function")`"** — §3-3 확보 사실 + 신선도 원장(*"GitHub #14137 (배경 태스크 회귀) 2025-10 🟢 최신"*)과 일치. **"#11107을 해결했다"로 반올림하지 않았다** — §3-3의 🚨 금지 사항 준수. ✅
- **(line 45) 큐 5종 버전·시점** — 핀 테이블 G와 **전건 대조**: Celery 5.6.3(2026-03-26) · arq 0.28.0(2026-04-16) · TaskIQ 0.12.4(2026-05-08) · Dramatiq 2.2.0(2026-06-17) · RQ 2.10.0(2026-06-20). 원고의 연월 표기가 5건 모두 정확. ✅
- **(line 55) Celery concurrency 옵션 목록 "prefork · Eventlet · gevent · thread · solo"** — §1-5 ⚠️ 항목 축자와 항목·순서 일치. ✅
- **(line 87) `uv add python-multipart`** — 핀 테이블 G(*"업로드 필수 의존"*) 및 §J `[standard]` 구성과 일치. ✅
- **(line 119) `UploadFile.size`가 헤더가 아니라 읽어들인 내용에서 계산된다** — `[^8-2]`가 starlette 1.3.1 `datastructures.py`를 근거로 단다. 계약 §8-2가 `UploadFile`의 메서드·속성을 **8장 소유 T1**으로 지정했고 각주 1회 요건을 충족한다. **T1 규칙에 따라 ✅.**
- **(line 176) `to_thread.run_sync`** — §1-3 추적 표면 + `[^8-3]`. 5장 기본형 재사용으로 표기(*"5장 각주에서 확인한"*)한 것은 **선행 장 표면을 다시 소유하지 않는 올바른 처리**다. ✅
- **코드 관용구:** `APIRouter(prefix="/issues/{issue_id}/attachments", tags=["attachments"])` → 계약 §3-7 표와 문자 단위 일치. `AttachmentService.__init__(self, session: AsyncSession)` → §3-3 생성자 규약 일치. `build_weekly_report` / `services/report.py` / `enqueue_weekly_report` / `tasks.py` → §3-8 일치. `api/projects.py`의 `/{project_id}/reports` → §3-7 경로 파라미터명 규약(`project_id`) 일치.
- **`ValidationFailedError("첨부 파일이 허용 크기를 넘었습니다", code="attachment.too_large")`** — `03_final.md` line 250–261의 생성자(`(self, message: str, *, code: str | None = None, details=None)`)와 **키워드 전용 인자까지 정확히 일치**. §3-5의 점 구분 도메인 코드 규약도 준수. ✅
- **`Attachment(...)` 생성 인자 6개** — `06_final.md` line 152–165의 모델과 **전건 대조**: `issue_id`·`uploader_id`·`filename`·`content_type`·`size_bytes`·`storage_key` 전부 실재. 생략한 `thumbnail_key`는 `Mapped[str | None]`이라 널 허용, `created_at`은 `server_default`. **필드 누락·오타 0건.** ✅
- **(line 214) "6장에서 `Attachment`의 `thumbnail_key`를 널 허용 타입으로 적어둔 것이 여기서 값을 한다"** — `06_final.md` line 162가 정확히 `Mapped[str | None]`. ✅
- **`📐 저자 설계` 마커 2건**(line 129·243) · **`> 출처:` 2건**(line 97·111) — 계약 §5·§6-4 형태 준수.
- **코드 주석 전수 검사: 날조 0건.** 7개 블록 중 인용 블록의 `# 1MB`는 **원본에 실재**(위 웹 확인), 나머지는 파일 경로·생략 마커뿐이다.

### ⚠️ 근거 부족 — 조치 필요

- **(line 186) `from tracker.schemas.attachment import AttachmentRead` — 정의되지 않은 심볼을 임포트한다**
  **근거:** 계약 §7 「장별 코드 성장 맵」 전 14행을 훑어도 `schemas/attachment.py`를 **새로 만드는 장이 없다.** 3장은 `schemas/issue.py`·`schemas/common.py`만, 6장은 모델만 만든다. 그런데 8장 라우터는 이 스키마를 임포트하고 `response_model=AttachmentRead`로 걸고 `AttachmentRead.model_validate(attachment)`로 부른다. **독자에게는 존재한 적 없는 파일이다.** — 6장 `IssueRepository.add()`(배치 2 최고 위험 항목)와 같은 유형이다.
  **[정정안]** 라우터 블록 앞에 4줄을 노출한다. 이름·경로·접미사는 이미 계약 §3-2를 지키고 있으므로 **정의만 보이면 해소된다**:
  ```python
  # src/tracker/schemas/attachment.py
  from pydantic import BaseModel, ConfigDict


  class AttachmentRead(BaseModel):
      model_config = ConfigDict(from_attributes=True)

      id: int
      filename: str
      content_type: str
      size_bytes: int
  ```

- **(line 55) "공식 문서가 표기한 지원 파이썬 범위와 PyPI 최신 버전 사이에 어긋남이 있는데"**
  **근거:** §1-5는 *"Celery 문서('5.5.x runs on Python 3.8–3.13')와 PyPI 최신(5.6.3)이 불일치"*라고 **구체 문자열까지** 적었다. 원고는 그 구체성을 버리고 "어긋남이 있다"로만 서술한 뒤 곧바로 "그 범위 역시 확인하지 못했다"고 덧붙인다. **레퍼런스가 확보한 것(5.5.x 문서 표기)과 확보 못 한 것(5.6.x 지원 범위)이 뭉개져** 있다.
  **[정정안]** *"공식 문서는 5.5.x가 Python 3.8–3.13에서 돈다고 적어두고 있는데 PyPI 최신은 5.6.3이다. **5.6.x의 지원 범위**는 이 책이 확인하지 못했다."*

### 🕒 마커 판정 — 2건

- **① (line 55) "Celery의 asyncio 네이티브 지원 여부에 대한 공식 진술을 확보하지 못했다 (사실 확인 필요)"** → **🕒 검증 불가 · 서술은 모범적**
  **근거:** 계약 §8-4 T3 표에 **"Celery asyncio 네이티브 지원 (공식 진술 미확보) | 8"**로 등재. §1-5는 *"'Celery는 async 네이티브가 아니다'를 공식 문장으로 뒷받침하지 못했으므로 **단정 금지**"*라고 지시했다. 원고는 ① 확보 못 했음을 선언하고 ② 정황(concurrency 목록)만 제시하고 ③ *"정황은 진술이 아니므로 여기서 멈춘다"*로 **명시적으로 추론을 차단**한다. **레퍼런스의 지시를 문자 그대로 이행했다.** 웹 에스컬레이션 대상이 아니다 — 원고가 아무 주장도 하지 않기 때문이다.
  **[final 전 조치 — 필수]** `(사실 확인 필요)` 토큰만 삭제. 산문은 그대로 둔다.

- **② (line 61) "파이썬에는 이 역할의 라이브러리가 여럿 있는데, 이 책은 그중 어느 것의 현재 API·버전도 확인하지 않았다 (사실 확인 필요)"** → **🕒 검증 불가 · 서술은 적법**
  **근거:** 계약 §8-4 T3에 **"APScheduler 등 개별 스케줄러 (버전 핀 표에 없음) | 8"**로 등재. 실제로 핀 테이블 A~J 어디에도 APScheduler가 없다. 원고는 **라이브러리 이름을 하나도 대지 않고** 층 구조만 서술한다 — 확인 못 한 도구를 이름으로 추천하는 것보다 안전한 처리다.
  **[final 전 조치 — 필수]** 토큰만 삭제. 예: *"…여럿 있는데, **이 책은 그중 어느 것의 현재 API·버전도 확인하지 못했다.** 도구를 단정하는 대신 구조만 이야기하겠다."*

### 뉘앙스 지뢰 판정 (§7-3 · 계획서 배정표)

- **큐 도구 우열 단정 금지 — ✅ 통과.** line 47이 *"여기서 어느 것이 낫다고 말하지는 않겠다. 이 책의 리서치에는 팀들이 무엇을 골랐고 왜 후회했는지에 대한 근거가 없고, **없는 근거로 서열을 매기지는 않기로 했다**"*로 **명시적으로 서열화를 거부**한다. 이어지는 선택 축 5개에 **"다음 축들은 저자 기준이다"** 표시가 붙어 있다. §7-3의 "실무 증언 없음"을 정직하게 노출한 모범 처리.
- **「저자 기준」 표시 — ✅ 2건 확인.** line 31(네 문항 앞 인용구: *"아래 네 문항은 **저자 기준**이다. 공식 권장도 업계 표준도 아니라 … **팀들이 실제로 어떤 기준으로 갈랐는지에 대한 증언은 리서치에서 찾지 못했다**"*) · line 47(선택 축 앞). 둘 다 근거 공백을 본문에서 밝힌다.
- **출신 귀속 — ✅ 위반 없음.** line 5 *"예전 같으면 메서드에 비동기 실행 애너테이션 하나를 붙이고 끝냈을 것이다"*, line 59 *"주기 실행 애너테이션 한 줄, Quartz 설정 몇 줄, 또는 node-cron 한 줄로 끝내던 자리"* — **독자의 과거 습관 호명**이지 인과 귀속이 아니다. Spring/Node 측 **설정 키·기본값·엔드포인트 경로를 하나도 주장하지 않는다**(`@Scheduled`·`@Async` 같은 애너테이션 이름조차 대지 않는다). §7-2 준수.
- **배포 결정 선점 — ✅ 없음.** line 21이 종료 유예 시간을 *"그 숫자를 정하는 일은 배포를 이야기할 자리의 몫"*으로, line 65가 CronJob을 *"13장의 소재이니 여기서는 존재만 짚어둔다"*로 넘긴다. **숫자를 정하지 않는다.**

### 양화사 점검

| 원문 | 판정 |
|---|---|
| (39) "계산 작업은 스레드로 옮긴다고 병렬로 돌지도 않는다" | ✅ `05_final.md` line 148과 동일 논지, 5장이 이미 shipfriend 1차 증언(`[^5-6]`)으로 근거를 댔다 |
| (73) "이 버그는 프로덕션에서만 나타난다" | ⚠️→✅ 강한 표현이나 바로 앞 두 문장(*"로컬에서는 워커가 하나라 … 스테이징도 대개 하나다"*)이 조건을 명시한다. 「대개」로 완충돼 있음 |
| (239) "**전부** '지금은'이 붙는다" | ✅ 바로 앞 네 문항에 대한 서술 |
| (259) "**전부** 그 한 문장의 다른 얼굴이다" | ✅ 이 장이 다룬 세 현상에 대한 서술 |

**다수설 일반화 · Reddit/SO 인용 · `#14603` · `status.HTTP_422_*` — 전건 0건.**

### 8장 소계

| 기호 | 건수 |
|---|---|
| ❌ | **0** |
| ⚠️ | 2 |
| 🕒 | 2 (마커, 토큰 삭제로 해소) |
| ✅ | 20 |

---

## 9장

### ❌ 정정 필요 (BLOCKING)

- **(line 100) `issue = await service.change_status(issue_id, "resolved")` — 존재하지 않는 시그니처를 호출한다**
  **근거 (원고 내부 대조):**
  | 정의 위치 | 시그니처 |
  |---|---|
  | `02_final.md` line 174 | `async def change_status(self, issue_id: int, status: str) -> None:` |
  | `07_draft.md` line 244–246 | `async def change_status(self, issue_id: int, status: IssueStatus, events: EventBus) -> Issue:` |
  | **`09_draft.md` line 100 호출** | `await service.change_status(issue_id, "resolved")` |

  이 호출은 **두 정의 중 어느 쪽과도 맞지 않는다.** ① 7장 기준으로는 필수 인자 `events`가 빠져 `TypeError`가 나고, `status` 자리에 `IssueStatus` 대신 `str` 리터럴이 들어간다. ② 2장 스텁 기준으로는 인자 수는 맞지만 **반환이 `None`인 함수의 결과를 `issue`에 담아** 다음 줄에서 템플릿 컨텍스트로 넘긴다.
  배치 2에서 가장 위험했던 6장 `IssueRepository.add()`와 **정확히 같은 유형**이다 — 외부 대조로는 잡히지 않고 원고 내부 정합성으로만 드러난다. 하네스에 코드 실행 단계가 없으므로 이 대조가 유일한 방어선이다.
  **[정정안]** 시그니처 소유는 7장이므로 **9장을 고친다.** 의존성 하나를 추가하면 끝난다:
  ```python
  # src/tracker/api/admin.py
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
      ...
  ```
  **부수 효과가 오히려 이득이다.** 이렇게 고치면 관리자 화면에서 상태를 바꿨을 때 7장이 깔아둔 SSE 채널로 알림이 나간다 — line 117이 *"버튼 조작은 HTMX로 받고, 남이 바꾼 이슈가 내 화면에 반영되는 것은 SSE로 밀어주는 식"*이라고 쓴 배치가 **코드로 실제 성립하게 된다.** 지금은 그 문장이 코드에 근거가 없다.

- **(line 47) `issues = await service.list_open_issues()` — 정의된 적 없는 메서드**
  **근거:** `01_final.md`~`06_final.md`와 7·8·9장 초안 전체에서 `list_open_issues`의 **정의가 0건**이다(호출 1건만 존재). 계약 §3-3의 서비스 도메인 동사 예시(`create_issue`·`update_issue`·`assign_issue`·`change_status`·`add_comment`)에도 없고, §7 성장 맵의 어느 장도 이 메서드를 만들지 않는다. **계약 §8-5 기준 "계약 밖"**이다.
  **저술가 보고에 대한 판정 — 동의하지 않는다.** 저술가는 *"라이브러리 API가 아니므로 판정 대상이 아니다"*라고 봤다. 계약 §3 서문의 면제(*"저자가 발명한 것이라 fact-checker의 판정 대상도 아니다"*)는 **계약이 실제로 등재한 이름**에 적용되는 것이지, 저술가가 즉석에서 만든 이름에까지 확장되지 않는다. 그리고 **호출됐는데 정의된 적 없다는 것은 라이브러리 문제가 아니라 원고 결함**이다 — 정의 누락 점검은 이름의 출처와 무관하게 적용된다.
  (같은 보고에서 **`SearchClient`는 저술가 판단에 동의한다** — 계약 §7 성장 맵이 9장의 신규 산출물로 `clients/search.py`를 명시하므로 저자 발명 영역이 맞고, 클래스 정의가 line 215에 **실제로 실려 있다.**)
  **[정정안]** 둘 중 하나.
  (가) 이미 있는 것을 쓴다 — `06_final.md` line 218의 `IssueRepository.list(project_id, limit, offset)`를 서비스가 감싼 형태로 호출.
  (나) 이 장에서 정의를 보인다 — 두 줄이면 된다:
  ```python
  # src/tracker/services/issue.py (9장에서 추가)
      async def list_open_issues(self) -> list[Issue]:
          stmt = select(Issue).where(Issue.status == IssueStatus.open)
          return list(await self.session.scalars(stmt))
  ```
  어느 쪽이든 **오케스트레이터에 「계약 밖 이름 도입」으로 보고**한다(§8-5 절차).

### ✅ 확인됨

- **🌐 (line 53) `TemplateResponse` 인자 순서 주석 축자** — *"Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter."* — `research/web_deploy.md` line 248 [S22] 원문과 축자 일치. `[^9-1]`이 정본 URL 2개를 단다.
- **(line 55) "Starlette 1.0.0(2026-03-22)이 옛 시그니처를 완전히 제거했다"** — `web_deploy` line 250 [S5] 릴리스 노트 축자 *"Remove deprecated `TemplateResponse(name, context)` signature from Jinja2Templates"* + 핀 테이블 B(1.0.0 = 2026-03-22). **날짜·사실 양쪽 확인. 저술가의 강화는 근거가 있다** (단서는 아래 🕒 참조).
- **(line 57) *"Note that the incoming request instance must be included as part of the template context."*** — `web_deploy` line 253 [S23] 원문과 축자 일치. 원문에서 **must가 굵게** 표시된 것까지 정확(원고: *"굵게 못 박는다"*).
- **(line 59) `.html`·`.htm`·`.xml` 오토이스케이프 + Starlette 1.0.0 릴리스 노트 수정 항목** — `web_deploy` line 254(*"When using the `directory` argument, Starlette enables autoescape by default for `.html`, `.htm`, and `.xml` templates using `jinja2.select_autoescape()`"*) 및 line 256(*"Enable autoescape by default in Jinja2Templates"가 Fix로*)과 **확장자 3종·조건(`directory` 인자)·릴리스 노트 등재까지 전건 일치.**
- **🌐 (line 123) `frontend(path, directory, fallback="auto", check_dir=True)` 및 `StaticFiles` 문서 상단 안내** — 시그니처는 §1-2에서 **추적됨**(0.138.0 신규, 직접 확인). 문서 인용은 웹 2차로 확인: *"If you need to host a frontend, use `app.frontend()` instead"* 실재. ✅
- **🌐 (line 125) `app.frontend()` 동작 3주장 — 전건 공식 문서 축자 확인**
  | 원고 주장 | FastAPI *Frontend* 문서 축자 | 판정 |
  |---|---|---|
  | "경로 연산을 먼저 확인하고 매칭되는 것이 없을 때만" | *"FastAPI checks path operations first. The frontend files are checked only if no normal route matched, so your API won't be affected."* | ✅ |
  | "폴백은 `Accept: text/html`이 붙은 GET·HEAD 요청에만" | *"FastAPI uses this fallback only for `GET` and `HEAD` requests that explicitly accept HTML with `Accept: text/html` or `Accept: application/xhtml+xml`"* | ✅ (아래 ⚠️ 참조) |
  | "없는 자원은 여전히 404다" | *"Missing files like JavaScript, CSS, and images still return `404`."* | ✅ |
- **🌐 (line 125) "0.139.0(2026-07)부터는 이 프론트엔드 응답에도 의존성을 걸 수 있어서, 쿠키 인증으로 정적 자산까지 보호하는 배치가 가능해졌다"** — **✅ 정확.** 0.139.0은 `01_reference.md` §3-1 표에 **없는 버전**이라 근거 없는 서술을 의심했으나, FastAPI 릴리스 노트를 열어 확인한 결과 **0.139.0 (2026-07-01)** 이 실재하고 그 기능 항목이 *"✨ Support dependencies in `app.frontend()`, e.g. for **automatic cookie authentication for the frontend**. PR #15908"*이다. **버전·연월·기능·쿠키 인증 예시까지 네 요소가 전부 일치한다.** (`web_deploy` line 260 [S17]에도 같은 축자가 있다.) 0.138.0 = 2026-06-20도 확인.
- **(line 129) "이 책이 기준으로 삼은 FastAPI 0.140 / 2026-07 기준으로도 여전히 새것이다. 세부 동작은 공식 문서를 함께 확인하는 편이 안전하다"** — §5-1 버전 표기 규율(*"'{버전}/{연월} 기준' 형식을 쓰라"*) 준수 + 휘발성 경고. ✅ **모범 처리.**
- **(line 139) Strawberry 권장 축자** — `web_deploy` line 272 [S25] 원문과 축자 일치. §1-5 *"공식 문서 권장은 Strawberry(0.323.2)"*와도 일치.
- **(line 141) "0.15.0에서 폐기 예고, 0.17.0(2021-11-04)에서 제거됐다. Starlette 1.0과는 관계없는 사건"** — `web_deploy` line 276–279 [S26] 축자(*"deprecated in version 0.15.0, and removed in version 0.17.0"* / *"`0.17.0 (November 4, 2021)` — Removed — 'Remove GraphQL support #1198'"*)와 **버전 2개·날짜 1개 전건 일치.** 리서치가 명시적으로 *"GraphQL 제거는 2021년 사건이지 Starlette 1.0과 무관하다"*고 정리한 혼동을 원고가 그대로 방어한 것도 정확.
- **(line 143) `uv add "strawberry-graphql[fastapi]"`** — `web_deploy` line 281 [S27] `'strawberry-graphql[fastapi]'` + §5-C(uv가 공식 기본)와 일치. 핀 테이블 G(0.323.2)도 대조됨. ✅
- **(line 177) Strawberry sync 리졸버 경고 축자** — §1-5 🔴 *"Strawberry에서 `sync def` 리졸버는 워커 전체를 블록한다"*(web_deploy §1-G) + `[^9-3]`. ✅
- **(line 179) 처방(*"모든 필드를 `async def`로, 도저히 안 되면 `starlette.concurrency.run_in_threadpool`"*)** — `run_in_threadpool`은 §1-3에서 **추적됨**. ✅
- **(line 189) httpx 기본값 4종 — 타임아웃 5초 / 최대 연결 100 / 유지 연결 20 / 유휴 만료 5초** — `[^9-4]`가 `Timeout(timeout=5.0)`·`Limits(max_connections=100, max_keepalive_connections=20, keepalive_expiry=5.0)`를 httpx 공식 API Reference·Resource Limits로 근거 댄다. 계약 §8-2가 `limits`·`base_url`·`transport`·`retries`의 **코드 표면을 9장 소유 T1**으로 지정했고 각주 요건 충족. **T1 규칙에 따라 ✅.**
- **(line 189) "3레플리카에 워커 4개면 상대 서비스 입장에서 최대 1,200개"** — 3 × 4 × 100 = 1,200 ✅ **산술 정확.** 6장 line 421이 *"13장에서 워커 수를 정할 때 곱해야 한다"*고 심어둔 산술을 정확히 반복.
- **(line 193) `retries` 축자 + (line 195) 해석** — §1-5 🔴 *"httpx의 `retries`는 연결 실패만 재시도한다 — HTTP 5xx는 재시도하지 않는다"*와 정확히 일치. *"상대가 503을 돌려주면 재시도하지 않고, 읽기 타임아웃이 나도 재시도하지 않는다"*는 `ConnectError`/`ConnectTimeout`이라는 인용 범위에서 곧바로 따라 나온다. **§1-5가 "Spring Retry / Resilience4j를 기대하고 오면 반드시 틀린다"고 쓴 것을 원고 line 197이 그대로 옮겼다.** ✅
- **(line 197) "httpx 문서 자신이 이 한계를 인정하고 … `tenacity` 같은 범용 도구를 보라고 적어두었다"** — `[^9-4]`가 *"`retries`의 동작 범위와 `tenacity` 언급"*을 Transports 문서로 근거 댄다. ✅
- **(line 187) `app.state` / `request.app` 축자** — `[^9-5]`가 Starlette Applications 문서 2문장을 싣는다. §1-2에서 `app.state`는 **추적됨.** ✅
- **(line 247) `httpx.HTTPError`가 `RequestError`와 `HTTPStatusError`의 상위 클래스** — `[^9-4]`의 축자 *"Base class for `RequestError` and `HTTPStatusError`"*로 근거. 따라서 `raise_for_status()`가 던지는 것까지 한 줄로 잡는다는 서술이 성립. ✅
- **(line 247) "예외 핸들러는 여전히 세 개이고 이 장이 네 번째를 만들지 않는다"** — 계약 §3-6(*"핸들러는 3개뿐 … 후속 장이 네 번째 핸들러를 추가하지 않는다"*) 및 `03_final.md` line 283과 일치. **`ExternalServiceError` → 502 매핑도 §3-6 계층표와 일치.** ✅
- **(line 249) `search_service_url`을 2장 `Settings`에 얹는다** — 계약 §3-4 설정 필드표에 **`search_service_url | str | 도입 9 | 쓰는 9`**로 등재. **필드명 문자 단위 일치.** ✅
- **(line 187) `app.state.http_client` 재사용** — 계약 §7 성장 맵 9장 행(*"`app.state.http_client`(4장 lifespan) — **`AsyncClient`를 새로 만들지 마라**"*) 및 부록 #8 준수. **`04_final.md` line 248이 만든 그 객체를 그대로 꺼내 쓴다.** ✅ (교차 충돌 항목 참조)
- **(line 257) BFF 근거 두께 자기 신고** — *"BFF는 업계 관행이지 정립된 이론이 아니다 … 사실상 한 편(Microusity, ICPC 2023)뿐이었다. 그러니 아래 판단 기준은 논문이 보증하는 것이 아니라 **저자의 기준**"* — §2-2 표(BFF 학술 근거 **약함** → *"업계 관행으로 정직하게"*) 및 §6-4(*"이 영역의 사실상 유일한 문헌"*)와 **학회·연도·유일성까지 정확히 일치.** ✅ **근거 얇은 장에서 나올 수 있는 가장 정직한 처리.**
- **코드 관용구:** `APIRouter(prefix="/admin", tags=["admin"])` → 계약 §3-7 표 일치. `api/graphql.py` + `include_router(router=graphql_router, prefix="/graphql")` → §3-7의 **키워드 인자 전용** 규약 준수(§1-2가 경고한 `include_router` 파라미터 순서 차이 회피). `clients/search.py` → §7 성장 맵 9장 신규 항목. `Annotated[str | None, Header()]` → §4-1 관용구 + §4-7 `|` 유니온 준수.
- **(line 82) `Header`의 언더스코어→하이픈 변환 축자** — `[^9-6]`이 FastAPI Header Parameters 문서로 근거. §1-2가 `Header`→`convert_underscores`를 고유 인자로 **추적**한 것과 정합. ✅
- **`📐 저자 설계` 마커 3건**(line 27·84·145·205 중 4건) — 계약 §5 형태 준수. 계획서가 의무로 지정한 「9장 HTMX 배선」 충족(line 84). ✅
- **코드 주석 전수 검사: 날조 0건.** 7개 블록의 주석은 전부 파일 경로 또는 생략 마커. HTML 블록도 §6-2 형태(`<!-- src/tracker/templates/issue_row.html -->`) 준수.

### ⚠️ 근거 부족 — 조치 필요

- **(line 125) 폴백 조건에서 `Accept: application/xhtml+xml`이 빠졌다**
  **근거:** 공식 문서 축자는 *"`Accept: text/html` **or** `Accept: application/xhtml+xml`"*이다. 원고는 앞의 하나만 적는다. 브라우저 내비게이션은 둘 다 보내므로 실무 영향은 없으나 **조건을 좁혀 인용한 것**이다.
  **[정정안]** *"`Accept: text/html`(또는 `application/xhtml+xml`)이 붙은 GET·HEAD 요청에만"*

- **(line 123–129) `app.frontend()` 절 전체에 각주가 하나도 없다**
  **근거:** 이 절은 시그니처 1건 + 문서 축자 1건 + 동작 3주장 + 버전 2개(0.138.0·0.139.0)를 싣는데 `[^9-*]` 마커가 **0건**이다. 시그니처만 §1-2에서 추적됐고 **나머지 6건은 레퍼런스에 근거가 없다.** (팩트체크로 전건 실재를 확인했으므로 **사실 판정은 ✅**지만, 원고에는 출처가 남아 있지 않다.) 9장에서 **각주 없이 가장 많은 표면을 실은 절**이다.
  **[정정안]** 각주 하나를 신설한다:
  > `[^9-7]: `app.frontend(path, directory, fallback="auto", check_dir=True)`의 시그니처, 경로 연산 우선 확인·`Accept: text/html`/`application/xhtml+xml` GET·HEAD 폴백·누락 자원 404 동작, `StaticFiles` 문서 상단 안내 축자 — FastAPI 공식 문서 *Frontend*(https://fastapi.tiangolo.com/tutorial/frontend/)·*Static Files*(https://fastapi.tiangolo.com/tutorial/static-files/) · 0.138.0(2026-06-20) `app.frontend()` 추가 / 0.139.0(2026-07-01) *"Support dependencies in `app.frontend()`"* — 릴리스 노트 https://fastapi.tiangolo.com/release-notes/ (조회 2026-07-26)`

- **(line 201) "파이썬·asyncio에는 서킷 브레이커의 사실상 표준이라 할 것이 없다" / "활발한 축에 드는 `pybreaker`"**
  **근거:** ① **부재 주장**("사실상 표준이 없다")은 레퍼런스 어디에도 근거가 없다 — §1-5는 *"⚠️ pybreaker의 asyncio(비-Tornado) 지원은 미확인"*이라고만 적었을 뿐, 생태계 지형에 대한 조사를 하지 않았다. ② **"활발한 축에 드는"**은 유지보수 활동 판정인데 `pybreaker`는 **버전 핀 테이블 A~J 어디에도 없다.** 최신 버전·릴리스 날짜를 이 책이 확인한 적이 없다.
  §7-5가 *"레퍼런스에 없는 걸 '확인됐다'고 가정하지 말라"*고, §0이 *"⚠️ 미확인 → 단정하지 마라"*고 못 박은 구역이다.
  **[정정안]** 두 단정을 모두 약화한다:
  > "세 번째 겹은 정직하게 말해야겠다. **이 책은 파이썬·asyncio 진영의 서킷 브레이커 지형을 조사하지 않았다.** 이름이 오르내리는 `pybreaker`조차 **최신 버전도 비동기 지원 범위도 확인하지 못했다.** 그래서 도구 대신 패턴만 남긴다."

- **(line 55) "검색 결과 상위에 뜨는 블로그 글이 여전히 옛 형태인 경우가 많으니"**
  **근거:** 검색 결과 분포에 대한 정량 주장인데 리서치에 근거가 없다. §7-1이 **Reddit·Stack Overflow 전면 차단**을 신고했고, 블로그 상위 노출 분포를 집계한 자료도 없다. (같은 유형의 서술이 7장 line 166에도 있으나 그쪽은 §1-5가 *"인터넷 자료 대다수가 `sse-starlette` 설치를 안내한다"*로 **레퍼런스가 직접 뒷받침**한다 — 이쪽은 없다.)
  **[정정안]** 분포 주장을 제거하고 인용 사실만 남긴다 — *"인터넷에 널려 있는 옛 형태를 복사했다면, 화면이 안 나온다고 템플릿 경로부터 뒤지기 전에 이 줄부터 보자."*

### 🕒 판정 — 3건

- **③ (line 173) "여기에 4장의 `SessionDep`을 그대로 쓸 수 있는지가 확실하지 않다 … (사실 확인 필요)"** → **🕒 검증 불가 · 서술은 적법**
  **근거:** 계약 §8-4 T3 표에 **등재되지 않은** 항목이다(§8-4는 9장 몫으로 `pybreaker`만 싣는다). 즉 저술가가 **스스로 발견한 계약 밖 불확실성**이고, §8-5가 지시한 절차(*"`(사실 확인 필요)`를 달고 오케스트레이터에 보고"*)를 따랐다. 원고는 **아무 배선도 주장하지 않고** 리졸버 몸통을 `...` 스텁으로 비운 뒤 *"Strawberry 문서에서 직접 확인하고 넘어가자"*로 넘긴다 — 확인 못 한 API를 지어내지 않았다.
  판정 근거로 제시된 이유(*"리졸버를 부르는 쪽이 FastAPI의 의존성 해석기가 아니라 Strawberry의 실행기"*)는 line 177의 Strawberry 공식 경고(**실행 주체가 Strawberry**)와 정합하므로 **불확실성 자체가 합리적이다.**
  **[final 전 조치 — 필수]** 토큰만 삭제하고 산문으로 흡수한다. **몸통을 추측으로 채우지 마라** — 확인되지 않은 배선을 코드로 싣는 것이 이 절에서 가장 나쁜 선택이다.
  **[오케스트레이터 보고]** 계약 §8-4 T3 표에 「Strawberry 리졸버의 FastAPI 의존성 주입 경로 | 9」를 **추가 등재** 권고.

- **④ (line 201) "`pybreaker`도 비동기 지원 범위를 이 책을 쓰며 확인하지 못했다 (사실 확인 필요)"** → **🕒 검증 불가 · 서술은 적법**
  **근거:** 계약 §8-4 T3 표에 **"pybreaker asyncio 지원 | 9"**로 등재. §1-5도 *"⚠️ pybreaker의 asyncio(비-Tornado) 지원은 미확인"*으로 신고했다. 원고는 코드를 싣지 않고 **패턴 3요소(카운터·임계치·재시도 간격)만** 남긴다 — 계약 §8-3의 판정 우선순위(*"확인에 실패했는데 코드가 꼭 필요하다고 느껴지면, 그건 코드가 필요한 게 아니라 산문이 필요한 것"*)와 정확히 같은 처리다.
  **[final 전 조치 — 필수]** 토큰 삭제 + 위 ⚠️의 「활발한 축」·「사실상 표준 없음」 두 단정 약화를 **함께** 적용한다. 마커는 정직한데 그 옆 문장이 확인 안 된 판정을 하고 있다.

- **(line 55) "즉 옛 형태로 붙여 넣은 코드는 경고를 내며 도는 게 아니라 그냥 동작하지 않는다" — 핀 범위 양끝에서 갈린다** → **🕒 시점 명기 필요**
  **근거 (교차 충돌 유형):** 이 서술은 **Starlette 1.x에서는 참**이다(위 ✅ 참조). 문제는 이 책이 4장에서 정반대 규율을 가르쳤다는 데 있다. `04_final.md` line 272–274가 세 겹을 세워놓고 punchline을 이렇게 맺는다 — *"**셋째, FastAPI는 `starlette>=0.46.0`으로만 핀한다.** … `on_event`를 쓴 코드가 지금 도는지 안 도는지는 **당신의 `uv.lock`이 어떤 Starlette을 물어왔는지에 달려 있다.**"* `01_reference.md` §J·§5도 같은 사실을 두 번 강조한다.
  **핀 하한 0.46.0(2025-02-22)에서는 옛 `TemplateResponse` 시그니처가 deprecated 상태로 살아 있다.** 즉 락파일에 0.4x가 들어온 독자에게는 "그냥 동작하지 않는다"가 성립하지 않는다. 원고는 앞 문장에서 *"우리가 이 책에서 전제하는 스택은 Starlette 1.3.1 / 2026-06 기준"*으로 범위를 잡아뒀으므로 **거짓은 아니다.** 그러나 **4장이 애써 가르친 "핀 하한과 락파일" 구분을 이 문장이 조용히 지운다.**
  배치 1의 422 상수, 배치 2의 MRO 판정과 **같은 「핀 범위 양끝」 유형**이다.
  **[정정안]** 한 구절 추가로 해소된다:
  > "즉 **Starlette 1.x를 물어온 환경에서는** 옛 형태로 붙여 넣은 코드가 경고를 내며 도는 게 아니라 그냥 **동작하지 않는다.** (4장에서 본 그대로다 — 핀 하한은 아직 `>=0.46.0`이라 락파일에 0.4x가 들어왔다면 아직 경고만 날 수 있다.)"

### 뉘앙스 지뢰 판정 (🚩 계획서가 「가장 근거가 얇은 장」으로 표시)

**없는 토론·없는 경험담을 만들었는지 — 전수 점검 결과 0건.** 이 장이 가장 엄격한 표적이었으므로 항목별로 남긴다.

| §7 공백 항목 | 원고의 처리 | 판정 |
|---|---|---|
| **NestJS↔FastAPI 아키텍처 토론 0건** (§7-2) | **NestJS·Nest·FastNest·`@Module`·Guards/Interceptors/Pipes 언급이 전 장에 0회.** 유물조차 쓰지 않았다 | ✅ **저술가 보고 확인** |
| **htmx·fasthx 공식 가이드 미확인** (§1-5) | line 84의 `📐 저자 설계` 인용구가 *"아래 분기는 HTMX·FastAPI 조합에 대한 **공식 가이드가 아니다.** 확인된 것은 **헤더의 존재와 의미뿐**이고, 그것을 한 경로에서 쓰는 방식은 이 책이 고른 한 가지 배치"*로 **확인 범위를 문장 단위로 명시.** `fasthx`는 이름조차 등장하지 않는다 | ✅ **모범** |
| **pybreaker asyncio 미확인** (§1-5) | 마커 + 코드 없음 + 패턴만 | 🕒 (위 ④) — 단 주변 2단정은 ⚠️ |
| **BFF 학술 근거 사실상 1편** (§2-2) | line 257이 편수·논문명·학회·연도를 밝히고 *"저자의 기준"* 선언 | ✅ **모범** |
| Reddit·Stack Overflow 인용 (§7-1 🚨) | **0건** | ✅ |
| 다수설 일반화 (§4 표집 편향) | 커뮤니티 여론·다수설 서술 **0건.** 이 장에는 HN·Lobsters 인용이 하나도 없다 | ✅ |
| 출신 귀속 (§7-2 🚨) | line 11(*"컨트롤러가 … 뷰 이름을 문자열로 돌려주면 뷰 리졸버가 …"*)·line 57(*"프레임워크가 요청 객체를 알아서 컨텍스트에 넣어주던 감각"*)·line 191(*"익숙한 HTTP 클라이언트들"*)·line 197(*"선언 한 줄로 백오프까지 붙던 감각"*) — 전부 **독자 습관 호명**이며 인과 귀속·설정 키·기본값 주장 **0건.** Spring Retry·Resilience4j라는 이름조차 대지 않는다(§1-5는 그 이름을 갖고 있는데도) | ✅ |

### 양화사 점검

| 원문 | 판정 |
|---|---|
| (179) "**모든** 필드를 `async def`로 쓰고" | ✅ Strawberry 공식 문서의 처방을 옮긴 것 |
| (197) "여기서 **반드시** 틀린다" | ✅ §1-5 축자가 *"Spring Retry / Resilience4j를 기대하고 오면 **반드시** 틀린다"* — 레퍼런스가 같은 양화사를 쓴다 |
| (82) "`HX-Request` 헤더가 **항상** `true`로 붙는다" | ✅ `[^9-2]`가 htmx 공식 레퍼런스 축자 *"always 'true'"*를 근거로 단다 |
| (3) "바깥으로 내보낸 것은 **전부** JSON이었다" | ✅ 1~7장 회고. 실제로 1~6장 최종본에 HTML 응답이 없다 |
| (267) "조용히 빈 배열을 돌려주는 것이 **가장 나쁘다**" | ✅ 「저자 기준」 문단(line 257) 관할 아래의 설계 의견 |

### 9장 소계

| 기호 | 건수 |
|---|---|
| ❌ | **2 (BLOCKING)** |
| ⚠️ | 4 |
| 🕒 | 3 (마커 2 + 핀 범위 1) |
| ✅ | 28 |

---

## 🚨 코드 API 표면 대조 결과 (배치 3)

**하네스에 코드 실행·컴파일 단계가 없다. 이 대조가 유일한 방어선이다.**

| 항목 | 7장 | 8장 | 9장 | 계 |
|---|---|---|---|---|
| 코드 블록 | 10 | 7 | 7 | **24** |
| 추출 심볼 (import 경로·클래스·함수·데코레이터·파라미터) | 41 | 33 | 44 | **118** |
| 외부 추적 실패 (라이브러리 API) | **0** | **0** | **0** | **0** |
| **내부 정의 누락** | 0 | **1** | **2** | **3** |
| 가짜 주석 (§4-8 / 날조 사례 1 유형) | 0 | 0 | 0 | **0** |
| `status.HTTP_422_*` | 0 | 0 | 0 | **0** |

### import 경로 문자열 별도 grep (2장에서 실제로 구멍이 났던 유형)

**전 24블록의 import 문 32개를 경로 문자열 단위로 대조했다. 실패 0건.**

| import 경로 | 근거 | 판정 |
|---|---|---|
| `from fastapi.sse import EventSourceResponse, ServerSentEvent` | **🌐 웹 2차 — 공식 SSE 문서에 동일 문자열 실재** | ✅ |
| `from fastapi.responses import StreamingResponse` / `HTMLResponse` | §8-2 T1(7·9장 소유) + `[^7-4]`·`[^9-1]` | ✅ |
| `from fastapi.templating import Jinja2Templates` | `web_deploy` line 238 원문과 동일 | ✅ |
| `from fastapi.staticfiles import StaticFiles` | §8-1 추적됨 + `[^9-1]` | ✅ |
| `from fastapi import APIRouter, WebSocket, WebSocketDisconnect` | §8-2 T1(7장) + `[^7-1]` | ✅ |
| `from fastapi import BackgroundTasks` / `UploadFile` / `Header` / `Request` | §8-1 추적됨 | ✅ |
| `import redis.asyncio as redis` | §1-6(`aioredis`는 흡수) + §8-2 T1(7장) + `[^7-3]` | ✅ |
| `from anyio import to_thread` | §1-3 추적됨 + `[^8-3]` | ✅ |
| `from sqlalchemy.ext.asyncio import AsyncSession` | §8-1 추적됨 | ✅ |
| `import strawberry` / `from strawberry.fastapi import GraphQLRouter` | `web_deploy` line 282–283 [S27] 원문과 동일 | ✅ |
| `import httpx` / `from httpx import AsyncClient` | §8-2 T1(4·9장) + `[^9-4]`, `04_final.md` line 243과 동일 | ✅ |
| `from pydantic import BaseModel` | §8-2 T1(3장 소유, 7장은 각주 불필요) | ✅ |
| `tracker.*` 내부 경로 12건 | 계약 §2 모듈 레이아웃 · §7 성장 맵 | ✅ (아래 3건 예외) |

### 🚨 내부 정의 누락 3건 (외부 대조로는 잡히지 않는다)

배치 2 최고 위험 항목이었던 6장 `IssueRepository.add()`와 **같은 유형**이다. 전 코드 블록의 `self.X.Y(`·`service.Y(`·`객체.속성` 호출을 원고 1~9장 전체에 대해 전수 대조했다.

| # | 위치 | 호출 | 정의 | 판정 |
|---|---|---|---|---|
| 1 | 9장 line 100 | `service.change_status(issue_id, "resolved")` | 2장·7장 **두 정의 중 어느 쪽과도 불일치** | **❌ BLOCKING** |
| 2 | 9장 line 47 | `service.list_open_issues()` | **전 원고 0건** | **❌ BLOCKING** |
| 3 | 8장 line 186·194·209 | `AttachmentRead` | **어느 장도 `schemas/attachment.py`를 만들지 않는다** | ⚠️ |
| (참고) | 7장 line 247 | `self.issues.get(issue_id)` | `06_final.md` line 210에 **실재**. 다만 `Issue \| None` 반환 무가드 | ⚠️ |
| (참고) | 8장 line 161 | `append_to_storage` | 같은 블록 line 146에 **정의됨**(의도적 빈 스텁 + §5 마커로 이유 명시) | ✅ |
| (참고) | 8장 line 233 | `build_weekly_report` | 계약 §3-8 등재 + 8장이 소유 장(§7 성장 맵) | ✅ |
| (참고) | 7장 line 325 | `push_events` | 같은 블록 line 335에 **정의됨** | ✅ |

**`back_populates` 짝 부재:** 7·8·9장에 SQLAlchemy `relationship` 선언이 **0건**이므로 해당 없음. (`Attachment` 매핑은 6장 소유이며 8장은 인스턴스 생성만 한다.)

---

## 🚨 마커 판정 — 5건 전건 (과제 명세는 6건이라 했다)

**먼저 개수 불일치를 보고한다.** 과제는 *"현재 원고의 유일한 `(사실 확인 필요)` 마커 6건"*이라 했으나, `chapters/0[789]_draft.md` 전수 grep 결과 **실제로는 5건**이다.

```
07_draft.md:138   (1건)
08_draft.md:55, 61   (2건)
09_draft.md:173, 201   (2건)
```

과제가 명시적으로 열거한 것은 ①②③④ **4건**이고, 7장에 대해서는 *"실제로 0건인지 grep으로 확인하라"*고 했다. **7장은 0건이 아니라 1건이다.** 따라서 열거 4건 + 7장 1건 = **5건**이며, 6이라는 숫자에 대응하는 여섯 번째 마커는 원고에 존재하지 않는다. **누락된 마커를 찾지 못한 것이 아니라 애초에 없다.**

| # | 위치 | 항목 | 계약 §8-4 등재 | 판정 | final 조치 |
|---|---|---|---|---|---|
| — | 7장 138 | redis-py asyncio 풀 기본값 | ✅ 등재(7장) | 🕒 | 토큰 삭제 |
| ① | 8장 55 | Celery asyncio 네이티브 지원 | ✅ 등재(8장) | 🕒 | 토큰 삭제 |
| ② | 8장 61 | 앱 내 스케줄러 라이브러리 API·버전 | ✅ 등재(8장, APScheduler) | 🕒 | 토큰 삭제 |
| ③ | 9장 173 | GraphQL 리졸버의 `SessionDep` | ❌ **미등재** | 🕒 | 토큰 삭제 + **§8-4 추가 등재 권고** |
| ④ | 9장 201 | `pybreaker` asyncio 지원 범위 | ✅ 등재(9장) | 🕒 | 토큰 삭제 + **주변 2단정 약화(⚠️)** |

**5건 전부 「원고가 아무것도 주장하지 않는」 유형이다.** 지어낸 값·추측으로 메운 자리가 **0건**이고, 5건 모두 확인 실패를 본문에서 독자에게 공개한다. **웹 에스컬레이션 대상이 아니다** — 의심 식별자(형식 이례 arXiv ID·미해결 DOI·검증 불가 인용)가 아니라 **자기 신고된 침묵**이기 때문이다. 검증할 주장이 없으면 검증 실패도 없다.

**단, 판정이 🕒인 이상 `(사실 확인 필요)` 문자열은 독자용 final에 남을 수 없다.** 5건 모두 **산문은 보존하고 마커 토큰만 삭제**하는 것으로 해소한다. 이건 사실 판정이 아니라 사무적 조치다.

---

## 🔍 저술가 보고 판단들에 대한 판정

| # | 저술가의 보고 | 판정 | 근거 |
|---|---|---|---|
| 1 | **[8장]** 계획서를 소스로 정정 — `routing.py` 0.140.0이 `await request.form()`을 **인자 없이** 호출하므로 선언형 `UploadFile` 경로에 `max_part_size` 손잡이가 **없다** | ✅ **정정이 옳다. 중요한 발견으로 확인한다** | 🌐 `fastapi/routing.py` @0.140.0 직접 확인 — 폼 파싱 호출은 파일 전체에 1곳, 인자 0개, `MultiPartParser`·`max_part_size` 참조 0건. 계획서가 틀렸고 저술가가 맞다 |
| 2 | **[8장]** `spool_max_size`(전환점) ↔ `max_part_size`(거부선) 분리 | ✅ **정확** | §1-4와 역할 분담 일치. 추가로 **핀 하한 0.46.0에서도 성립** 확인(`web_deploy` line 318: 0.46.0이 `max_file_size`→`spool_max_size` 개명을 도입) |
| 3 | **[9장]** `TemplateResponse` 지뢰를 "구식 주의"가 아니라 **"동작하지 않는다"**로 강화 | ✅ **1.x 기준으로는 옳다** / 🕒 **핀 범위 단서 필요** | 제거 사실은 `web_deploy` line 250 [S5] 축자로 확인. **그러나 핀 하한 `starlette>=0.46.0`에서는 옛 시그니처가 deprecated로 생존한다** — 4장 line 272–274가 세운 규율과 충돌. 한 구절 추가로 해소(위 🕒 참조) |
| 4 | **[9장]** `admin.py` 두 경로 함수에 **반환 타입 미표기**(계약 §4-7 편차). `TemplateResponse`가 `HTMLResponse`의 하위형인지 1차 소스로 확인 못 해 공식 예제 형태를 택함 | ✅ **사실 판정으로는 정확한 판단. 차단하지 않는다** | **검증되지 않은 타입 관계를 주장하지 않은 것은 옳다** — §0의 "⚠️ 미확인 → 단정 금지"를 정확히 적용했다. 게다가 원고가 택한 형태(`response_class=HTMLResponse` + 무애너테이션)는 `web_deploy` line 241–245의 **공식 문서 예제와 동일**하다. **다만 §4-7 편차 자체는 문체·규약 사안이므로 editor 판단 영역이며, 팩트체커는 여기에 대해 판정하지 않는다**(월권 금지) |
| 5 | **[9장]** `SearchClient`·`service.list_open_issues()`는 계약 밖 저자 발명 도메인 이름이므로 판정 대상 아님 | **⚠️ 절반만 동의** | **`SearchClient` — 동의.** 계약 §7 성장 맵이 9장 신규로 `clients/search.py`를 명시하고 클래스 정의가 line 215에 실려 있다. **`list_open_issues` — 동의하지 않는다.** §3 서문의 면제는 **계약이 등재한 이름**에 적용되지, 저술가가 즉석에서 만든 이름에 확장되지 않는다. 그리고 **"호출됐는데 정의된 적 없다"는 라이브러리 문제가 아니라 원고 결함**이다 — 정의 누락 점검은 이름의 출처와 무관하다. **❌ BLOCKING** |
| 6 | **[8장]** 계약에 없는 새 이름 6개(`AttachmentRead`·`AttachmentService.add_attachment`·`append_to_storage`·`enqueue_thumbnail`·`MAX_UPLOAD_BYTES`·`CHUNK_SIZE`) | ✅ **§3 명명 규약 위반 0건** | `AttachmentRead` → §3-2 `Read` 접미사 + 금지 접미사 회피 + `schemas/{단수}.py` 배치 ✅ / `add_attachment` → §3-3 "도메인 동사+목적어"(`add_comment`와 동형), `AttachmentService`는 §3-3 등재 ✅ / `enqueue_thumbnail` → §3-8 `enqueue_weekly_report`와 동형·동일 파일(`tasks.py`) ✅ / `append_to_storage`·`MAX_UPLOAD_BYTES`·`CHUNK_SIZE` → 규약이 규정하지 않는 헬퍼·상수, 충돌 없음 ✅. **유일한 결함은 이름이 아니라 `AttachmentRead`의 정의가 어느 장에도 없다는 것**(위 ⚠️) |

---

## 교차 충돌 점검 (1~6장 최종본 × 7~9장)

| # | 점검 항목 | 결과 |
|---|---|---|
| 1 | **7장이 5장의 프로세스 경계를 정확히 회수하는가** | ✅ `05_final.md` line 164 *"워커는 메모리를 공유하지 않는다"* → `07_draft.md` line 84가 **같은 문장을 굵게 그대로 인용**하고 *"5장의 그 문장이 청구서로 돌아온다"*로 연결. 공식 문서 축자(*"will only work with a single process"*)를 그 위에 겹친다 |
| 2 | **5장의 「두 번 돌아온다」 예고를 실제로 받는가** | ✅ **양쪽 다 착지.** `05_final.md` line 168 *"이 사실 하나가 나중에 두 번 돌아온다. **7장에서는 알림이 절반만 도착하는 현상으로, 8장에서는 주간 리포트가 네 번 생성되는 현상으로.**"* → 7장 소제목 *"워커가 둘이면 알림은 절반만 간다"*, 8장 소제목 *"매주 월요일 아홉 시, 그리고 네 번"* + line 73 *"리포트 메일이 네 통 왔다는 제보로"*. **예고 문구와 회수 문구가 어휘 단위로 대응한다** |
| 3 | **8장이 5장의 「오프로드는 40을 늘리지도 병렬화하지도 않는다」를 정확히 이어받는가** | ✅ `05_final.md` line 148 *"오프로드는 이벤트 루프를 살릴 뿐, 용량을 늘려주지 않는다 … CPU 바운드 작업은 스레드로 옮긴다고 병렬로 돌지도 않는다"* → `08_draft.md` line 39 *"스레드로 옮겨도 프로세스당 40이라는 자리는 그대로고, 계산 작업은 스레드로 옮긴다고 병렬로 돌지도 않는다. **오프로드는 이벤트 루프를 살릴 뿐 용량을 만들지 못한다**"*. 어휘 미세 변주("늘려주지"→"만들지")뿐 **논지 동일** |
| 4 | **8장이 6장의 `Attachment`를 정확히 이어받는가** | ✅ **필드 전건 일치.** `06_final.md` line 152–165의 9필드 중 8장이 쓰는 6개(`issue_id`·`uploader_id`·`filename`·`content_type`·`size_bytes`·`storage_key`) 전부 실재, 오타 0건. `thumbnail_key`가 `Mapped[str \| None]`이라는 8장 line 214의 회수도 정확. **6장 line 168 *"파일 바이트는 여기 없다 … 저장소는 8장의 몫이다"* 라는 넘김을 8장 line 123이 *"6장은 `Attachment`에 파일 바이트를 넣지 않기로 했고, 어디에 둘지는 이 장으로 넘겼다"*로 정확히 받는다** |
| 5 | **9장이 4장의 `app.state.http_client`를 재사용하는가** | ✅ **계약 위반 없음.** `04_final.md` line 236 저자 설계 인용구가 *"여기서 만든 클라이언트를 9장이 그대로 재사용한다"*, line 260이 *"9장의 BFF는 여기 있는 클라이언트를 **재사용**한다"*로 예고 → `09_draft.md` line 187이 *"답은 4장에서 이미 정해뒀다 … **여기서 새로 만들 일은 없다**"* + line 243 `SearchClient(request.app.state.http_client, ...)`. **`AsyncClient(...)` 생성 구문이 9장 전체에 0회.** 계약 §7 성장 맵 9장 행·부록 #8 준수 |
| 6 | **7장 lifespan이 4장 것을 흔들지 않는가** | ✅ `07_draft.md` line 274가 `app.state.http_client = AsyncClient(timeout=5.0)`을 `04_final.md` line 248과 **문자 단위로 동일하게** 재현하고 `app.state.redis` 한 줄만 추가. 종료 순서도 역순(`redis.aclose()` → `http_client.aclose()`)으로 올바르다 |
| 7 | **7·8장이 13장 소유의 배포 결정을 선점하지 않는가** | ✅ 7장 line 231(프록시 뒤 주소·프로토콜 → 13장) · line 342(*"그 숫자는 13장의 몫"*) / 8장 line 21(종료 유예 시간 → *"배포를 이야기할 자리의 몫"*) · line 65(K8s CronJob → *"13장의 소재이니 여기서는 존재만"*). **숫자를 정한 곳이 한 군데도 없다.** `05_final.md` line 170·220의 13장 예고와도 정합 |
| 8 | **각주가 앞 장이 이미 소유한 표면을 다시 달고 있지 않은가** | ⚠️ **경미 1건, 비차단.** `[^9-4]`가 `timeout=Timeout(timeout=5.0)`를 다시 근거 대는데, 계약 §8-2는 `httpx.AsyncClient`의 `timeout`·`aclose()`를 **4장 소유**로 지정했고 `[^4-3]`이 이미 같은 값을 근거 댔다. 9장 소유는 `limits`·`base_url`·`transport`·`retries`다. — **반면 `[^8-3]`의 *"5장 각주에서 확인한 AnyIO 공식 문서"*는 선행 장 소유를 명시적으로 참조하는 올바른 형태이므로 지적 대상이 아니다.** editor 노트 |
| 9 | **9장의 SSE 회고가 7장과 어긋나지 않는가** | ✅ `09_draft.md` line 109–117의 3방식 표(HTMX/SSE/SPA)에서 SSE 행 *"서버(이벤트 발생) / 이벤트 스트림"*이 7장 line 206의 결정(*"이슈 상세 화면의 실시간 갱신은 SSE로 간다 — 단방향이고"*)과 정합 |
| 10 | **9장의 `ConnectionManager` 부재가 7장과 충돌하는가** | — **팩트 사안 아님.** 계약 §3-8·§7이 `ConnectionManager`를 7장 신규 항목으로 등재했으나 7장은 이를 만들지 않고 *"공식 예제의 `ConnectionManager`가 하던 일은 구독이 대신한다"*(line 140)로 **의도적으로 대체**한다. 논지가 명시적이고 이유가 붙어 있다. §3 이름은 저자 발명이라 팩트체커 관할이 아니므로 **editor·오케스트레이터에 계약 편차로 라우팅**한다 |
| 11 | **7장 line 344 → 8장 넘김** | ✅ *"유실이 곤란하다면 그건 팬아웃이 아니라 **큐**로 풀 문제이고, 그 이야기는 오래 걸리는 일들과 함께 다룬다"* → 8장 제목·line 33(*"유실이 허용되지 않으면 큐다"*)이 정확히 받는다 |
| 12 | **8장 line 214·255 → 5장 `generate_thumbnail` 회수** | ✅ *"5장의 `generate_thumbnail`은 이 앱이 아니라 큐 워커 쪽에서 돈다 — 5장이 미뤄둔 '프로세스 밖'이 이 한 줄이다"*. `05_final.md` line 109·143에 함수가 실재하고 계약 §3-8이 5장 소유로 등재 |

---

## 배치 3 종합

| 장 | ❌ | ⚠️ | 🕒 | ✅ |
|---|---|---|---|---|
| 7장 | **0** | 5 | 1 | 22 |
| 8장 | **0** | 2 | 2 | 20 |
| 9장 | **2** | 4 | 3 | 28 |
| **계** | **2** | **11** | **6** | **70** |

### Phase 5 차단 항목 (해소 전 EPUB 빌드 불가)

**A. ❌ 2건 — 실물 결함. 저술가 재량으로 덮을 수 없다.**
1. 9장 line 100 `service.change_status(issue_id, "resolved")` — 7장 시그니처와 불일치 (인자 누락 + 타입 불일치)
2. 9장 line 47 `service.list_open_issues()` — 전 원고 정의 0건

**B. 🕒 6건 — 5건은 마커 토큰 삭제(사무적), 1건은 한 구절 추가.**
- 마커 5건: 산문 보존 · `(사실 확인 필요)` 문자열만 제거
- 9장 line 55: 핀 범위 단서 한 구절 추가

**C. ⚠️ 11건 — 조치 후 재검 불요(정정안이 전부 구체적으로 제시됨).**

### 가장 위험한 3건

1. **🥇 9장 line 100 `change_status` 호출 불일치 (❌).** 인쇄된 코드가 `TypeError`를 낸다. 배치 2 최고 위험 항목이었던 6장 `IssueRepository.add()`와 **정확히 같은 유형**이며, 하필 **7장이 방금 바꾼 시그니처를 9장이 못 따라간 것**이라 이번 배치를 함께 읽지 않았으면 잡히지 않았다. 게다가 고치면 9장 line 117의 "HTMX + SSE 혼용" 서술이 코드로 실제 성립한다 — **지금은 그 문장에 코드 근거가 없다.**
2. **🥈 9장 line 47 `list_open_issues` 미정의 (❌).** 관리자 화면 절의 **첫 코드 블록**이 존재하지 않는 메서드로 시작한다. 독자가 가장 먼저 따라 치는 자리다.
3. **🥉 8장 line 186 `AttachmentRead` 정의 부재 (⚠️).** 계약 §7 성장 맵 14행 어디에도 `schemas/attachment.py`를 만드는 장이 없다. `response_model`·`model_validate` 두 곳에서 쓰이므로 **없으면 앱이 뜨지 않는다.** ⚠️로 둔 것은 이름·경로·접미사가 이미 계약을 지키고 있어 **정의 블록 하나 추가로 끝나기 때문**이지, 실물 영향이 작아서가 아니다.

**언급할 가치가 있는 반전:** 이 배치에서 사전 위험도 1위로 지목했던 **8장의 starlette 인용 블록(독스트링 2줄)은 웹 2차 결과 전건 실재로 ✅**였고, 저술가가 계획서를 뒤집은 **`request.form()` 정정도 소스 대조로 옳음이 확인**됐다. **외부 대조 실패는 118개 심볼 중 0건이다.** 이번 배치의 결함은 전부 **원고 내부 정합성**에서 나왔다 — 배치 2의 교훈이 그대로 반복됐다.

### 오케스트레이터 보고 사항

1. **계약 §8-4 T3 표에 「Strawberry 리졸버의 FastAPI 의존성 주입 경로 | 9」 추가 등재 권고** (저술가가 §8-5 절차로 자기 신고한 계약 밖 항목).
2. **계약 §3-8·§7의 `ConnectionManager`(7장) 편차** — 7장이 의도적으로 만들지 않고 구독으로 대체했다. 팩트 사안이 아니므로 editor·계약 관리 쪽 판단 필요.
3. **`schemas/attachment.py`가 §7 성장 맵의 어느 장에도 없다** — 계약 자체의 공백이다(부록의 「저술 중 발견된 계획서상 공백」과 같은 유형). 8장 신규 항목으로 등재 권고.
4. **`02_plan.md` 8장 계획서의 `max_part_size` 서술이 소스와 어긋난다** — 저술가의 정정이 옳음을 확인했으므로 계획서 쪽을 정정 대상으로 표시.

---

## 10장

**검증 라운드 1 · 2026-07-26 · genre `tech-book` · 하네스 v1.9.1 Phase 4 (배치 4)**
초안 `chapters/10_draft.md` (25,214 bytes). 대조: `01_reference.md`(버전 핀 F·§2-3·§3-9·§7-2·§7-5) · `tracker_contract.md`(§3-4·§3-6·§7·§8-3 T2) · `02_plan.md` 10장·지뢰표 · `research/community.md` §2-5 · `chapters/01~09_final.md`.
**이 장은 계약 §8-3 T2(프로바넌스 위험 구역)의 핵심이다.** 코드 표면 전건을 1차 소스로 웹 2차 검증했다.

### ❌ 정정 필요 (BLOCKING)

**10-❌1. (line 39) 인용 축자가 원문의 헤지(hedge)를 삭제해 단정으로 바꿨다**

원고:
> "Python-Jose has been abandoned for a while, and now CVEs have been popping up surrounding it and its dependencies."

1차 소스 원문(fastapi/full-stack-fastapi-template Discussion #1188, SpoonOfDoom, 2024-04-29, 🌐 웹 2차 확인):
> "**it seems that** Python-Jose has been abandoned for a while, and now CVEs have been popping up surrounding it and its dependencies."

원고는 `it seems that`를 잘라내고 `Python-Jose`를 대문자로 올려 **문장 중간을 문장 시작처럼 보이게** 만들었다. 생략 표시(`…`)도 없다. 원 발언자는 "~인 것 같다"고 말했는데 인용은 "~다"가 된다. 바로 다음 줄(line 41)이 *"취약점이 지적된 라이브러리를 공식 문서가 계속 권했고"*로 이어져 **강화된 인용이 논지를 떠받친다** — 그래서 무해한 트리밍이 아니다.
`research/community.md` line 584도 같은 형태로 잘려 있어 저술가 단독 과실은 아니지만, 원문이 1차다.

**[정정안]** 둘 중 하나.
```
> "it seems that Python-Jose has been abandoned for a while, and now CVEs have been popping up surrounding it and its dependencies."
```
또는 생략을 명시한다.
```
> "… Python-Jose has been abandoned for a while, and now CVEs have been popping up surrounding it and its dependencies."
```
**근거:** https://github.com/fastapi/full-stack-fastapi-template/discussions/1188 (재조회 2026-07-26)

---

**10-❌2. (line 239 · 4장 line 104 · 계약 §7 교차규칙 2) `get_current_user` 시그니처 — 원고 내부 직접 모순**

저술가가 자기 신고한 항목이다. 판정한다: **계약 미규정 구간이 아니라 명시적 충돌이다.**

| 위치 | 진술 |
|---|---|
| `tracker_contract.md` §7 교차규칙 2 | "4장의 스텁 시그니처(`get_session() -> AsyncIterator[AsyncSession]`, **`get_current_user() -> User`**)를 6·10장이 채운다. **시그니처를 바꾸지 않는다.**" |
| `04_final.md` line 88–89 | `async def get_current_user() -> User:` / `raise NotImplementedError` |
| `04_final.md` line 104 | "두 경우 모두 **시그니처는 바뀌지 않는다.** 뒤 장은 완성하지 재정의하지 않는다." |
| `10_draft.md` line 220–224 | `async def get_current_user(token: …, session: SessionDep, settings: SettingsDep) -> User:` — **파라미터 3개 추가** |

파라미터 3개 추가는 어떤 상식적 독법으로도 시그니처 변경이다. 4장을 읽은 독자가 10장에서 정면으로 어긋난 코드를 만난다.

**다만 고쳐야 할 쪽은 10장이 아니다.** 파라미터 없는 `get_current_user`는 실물로 존재할 수 없고, 10장 line 239는 이미 *"채워진 것은 몸통과 파라미터 셋이다"*라고 정직하게 밝혔다. 저술가의 해석(이름·반환 타입·호출부 `CurrentUser` 불변)이 실질적으로 옳다.

**[정정안]** 계약 §7 교차규칙 3(경로·필드명 소유)에 따라 **`editor_notes` 경로로 4장 산문을 좁힌다.**
- `04_final.md` line 104: "두 경우 모두 시그니처는 바뀌지 않는다" → **"두 경우 모두 이름과 반환 타입은 바뀌지 않는다. 몸통을 채우며 필요한 파라미터는 붙는다 — 부르는 쪽은 `SessionDep`·`CurrentUser` 별칭만 보므로 영향이 없다."**
- `tracker_contract.md` §7 교차규칙 2도 같은 폭으로 좁힐 것을 권고(오케스트레이터 판단).
- **10장은 손대지 않는다.**

---

**10-❌3. (line 184–198) `repositories/user.py`의 `# ...(2장, 생략)`이 존재하지 않는 앞 장 코드를 가리킨다**

```python
# src/tracker/repositories/user.py
class UserRepository:
    # ...(2장, 생략)

    async def get(self, user_id: int) -> User | None:
        return await self.session.scalar(...)
```
`self.session`을 쓰는데 그 초기화가 "2장에 있다"고 표시했다. **원고 1~9장 최종본 전체에 `UserRepository`도 `repositories/user.py`도 0건이다.** 2장 line 125–135의 디렉터리 트리는 `repositories/`에 **`project.py`·`issue.py`만** 나열하고 `user.py`는 없으며, 2장이 실제로 보여준 골격은 `IssueRepository` 하나뿐이다(line 144–155).
(같은 블록의 `ProjectRepository`는 2장 트리에 `repositories/project.py`가 실재하므로 `# ...(2·6장, 생략)`이 성립한다 — ✅.)

계약 §6-3은 이 표기를 *"앞 장에서 **이미 쓴** 코드를 생략했다"*로 정의한다. 쓴 적이 없으면 표기가 거짓이 되고, 되짚어본 독자는 아무것도 못 찾는다. 배치 2·3에서 반복 적발된 「내부 정의 누락」과 같은 계열이다.

**[정정안]** 두 줄이면 끝난다.
```python
# src/tracker/repositories/user.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, user_id: int) -> User | None:
        ...
```
생성자는 계약 §3-3이 이미 확정한 형태(`__init__(self, session: AsyncSession)`)이므로 새 판단이 아니다.

### ⚠️ 근거 부족 — 조치 필요

- **(line 33·35) `#11380`을 "답변"으로 서술 — GitHub 상태 라벨은 `Closed` / `Unanswered`다.**
  원고 표: *"2025-05-26 답변(중복 처리)"*, 본문: *"그 신고에 답이 달리기까지 14개월이 걸렸다."*
  🌐 웹 2차: 스레드 https://github.com/fastapi/fastapi/discussions/11380 는 **Closed·Unanswered**로 표시된다. 2025-05-26에 메인테이너(YuriiMotov) 댓글이 달려 #11773의 중복으로 **닫힌** 것은 사실이나, GitHub이 말하는 "Answered"는 아니다. `research/community.md` line 602의 "답변 —" 표기를 그대로 받은 결과다.
  **[정정안]** 표 셀 → `2025-05-26 중복으로 닫힘`, 본문 → *"그 신고가 처리되기까지 14개월이 걸렸다"* 또는 *"메인테이너가 중복으로 닫기까지 14개월이 걸렸다."* 14개월이라는 수치와 논지는 그대로 산다.

- **(line 144) 인용 축자에 원문에 없는 접속사 `And`가 들어갔고 두 문장이 하나로 붙었다.**
  원고: *"… must send `username` and `password` fields as form data. **And the spec says** that the fields have to be named like that."*
  1차 소스(FastAPI *Simple OAuth2*, 🌐 웹 2차): 두 개의 독립 문장이며 뒤 문장은 **"The spec says that the fields have to be named like that."**로 시작한다(`And` 없음). 앞 문장에도 원문에는 `(that we are using)`가 있고 원고는 `...`로 옳게 생략했다.
  **[정정안]** `And the spec says` → `The spec says`. (의미 변화는 없고 축자 정합성 문제다.)

- **(line 13) "가장 자주 쓰이는 것이 `OAuth2PasswordBearer`다" — 빈도 주장의 근거가 없다.**
  레퍼런스·리서치 어디에도 `fastapi.security` 스킴별 사용 빈도 데이터가 없다. 계획 12장 오프닝 지침이 금지한 *"CI가 가장 많이 막는 것은 ~다"* 형 빈도 주장과 같은 유형이다.
  **[정정안]** *"공식 튜토리얼이 전면에 세우는 것이 `OAuth2PasswordBearer`다"* — 확인된 사실로 바꾸면 논지가 오히려 강해진다.

- **([^10-3]) PyJWT 시그니처의 기본값 `algorithm='HS256'`은 stable 문서 기준이며 master 소스에서는 이미 드리프트했다.**
  🌐 웹 2차: `pyjwt.readthedocs.io` API Reference는 `jwt.encode(payload, key, algorithm='HS256', …)`로 적지만, master `jwt/api_jwt.py`는 `algorithm: str | None = _ALGORITHM_UNSET`이다. 각주가 문서를 인용한 것이므로 **거짓은 아니다.** 다만 본문이 "HS256이 기본"이라고 쓰지 않은 것은 잘 한 판단이다(`Settings.jwt_algorithm = "HS256"`은 이 책의 값이지 라이브러리 기본값이 아니라고 읽힌다).
  **[권고]** 각주에서 `algorithm='HS256'`의 `='HS256'`만 떼고 `jwt.encode(payload, key, algorithm=…)`로 두면 드리프트 위험이 사라진다.

### ✅ 확인됨

**T2 표면 전건 — 🌐 웹 2차 1차 소스 확인 (계약 §8-3 절차 완료)**

| 표면 | 판정 | 근거 |
|---|---|---|
| `OAuth2PasswordBearer(tokenUrl=…)` | ✅ | oauth2-jwt 튜토리얼 `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")` |
| `Annotated[OAuth2PasswordRequestForm, Depends()]` · `.username` · `.password` | ✅ | 동 튜토리얼 `docs_src/security/tutorial005_an_py310.py` |
| `PasswordHash.recommended()` · `.hash(password)` | ✅ | 동 소스 `password_hash = PasswordHash.recommended()` |
| **`.verify(plain, hashed)` 인자 순서** | ✅ | 동 소스 `password_hash.verify(plain_password, hashed_password)` — 원고 `hasher.verify(raw, hashed)`와 **순서 일치** |
| `jwt.encode(payload, key, algorithm=…)` 단수 / `jwt.decode(token, key, algorithms=[…])` 복수 | ✅ | 동 튜토리얼 `jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)` / `jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])` |
| `from jwt.exceptions import InvalidTokenError` | ✅ | 동 튜토리얼에 동일 import 실재 |
| `jwt.decode`가 `exp`를 **기본 검증** | ✅ | PyJWT `api_jwt.py` `_get_default_options()` → `{"verify_signature": True, "verify_exp": True, …}` |
| `ExpiredSignatureError ⊂ InvalidTokenError` | ✅ | `jwt/exceptions.py`: `PyJWTError` → `InvalidTokenError` → `ExpiredSignatureError`. 원고 line 121의 "그 예외가 `InvalidTokenError` 아래에 있어 위의 `except` 한 줄에 함께 걸린다"가 **정확** |
| 401 + `headers={"WWW-Authenticate": "Bearer"}` | ✅ | 튜토리얼 `credentials_exception` 원문과 동일 |
| `pyjwt[crypto]`(RSA·ECDSA) | ✅ | *"you should install the cryptography library dependency `pyjwt[crypto]`"* |
| `Security(dependency, scopes=[…])` · `SecurityScopes`의 `scopes`·`scope_str` | ✅ | oauth2-scopes 페이지. **원고는 코드로 싣지 않고 산문으로만 썼다(line 247) — 계약 §8-3 판정 우선순위 준수** |
| 설치 `uv add "pwdlib[argon2]" pyjwt` | ✅ | 튜토리얼이 `uv add pyjwt` · `uv add "pwdlib[argon2]"` 두 줄로 안내 |

**날조 사례 1(가짜 주석) 자기 회피 — ✅ 검증됨.** 이 장 전 코드 블록의 주석은 **파일 경로 9건 + `# ...(N장, 생략)` 4건**이 전부다. 동작 설명 주석 **0건**. 저술가가 폐기했다고 신고한 `# SecurityScopes attributes: …` 형태의 주석은 원고에 없다. 계약 §4-8·제약 9-(B)-4 준수.
**Auth0 연동 코드 — 0건.** 계약 §8-3의 *"원문 재확인 실패 시 코드 금지"* 항목이 아예 등장하지 않는다. ✅

**축자·수치**

| 항목 | 판정 | 근거 |
|---|---|---|
| passlib 1.7.4 / **2020-10-08** | ✅ | 버전 핀 F + 🌐 PyPI 재확인 "1.7.4 Oct 8, 2020" |
| python-jose 3.5.0 / **2025-05-28** | ✅ | 버전 핀 F + 🌐 PyPI 재확인 |
| pwdlib 0.3.0 / 2025-10-25 · PyJWT 2.13.0 / 2026-05-21 | ✅ | 버전 핀 F + 🌐 PyPI 재확인 |
| #9587 2023-05-29 → 2024-05-20 ≈ **1년** | ✅ | `community.md` line 577–582 + 🌐 재확인. PR #11589(Merged, 2024-05-20)로 교차 확인 |
| #11773 2024-06-28 → 2025-09-30 ≈ **15개월** | ✅ | `community.md` line 592–597 + 🌐 재확인(YuriiMotov 2025-09-30 *"We have updated docs to use `pwdlib` …"*) |
| #11380 2024-03-31 → 2025-05-26 ≈ **14개월**, 제목 축자 | ✅ (상태 라벨만 ⚠️ 위 참조) | 제목 *"0.110.0: used no longer maintained `passlib` module in test suite"* 축자 일치 |
| #1188 SpoonOfDoom 2024-04-29 | ✅ | 🌐 재확인 |
| "The recommended algorithm is 'Argon2'." | ✅ | oauth2-jwt 페이지 |
| pwdlib 레거시 축자 (line 69, `...` 생략 표기 사용) | ✅ | 원문 *"pwdlib also supports the bcrypt hashing algorithm but does not include legacy algorithms - for working with outdated hashes, it is recommended to use the passlib library."* — 원고의 `pwdlib ...` 생략이 **정확히 표시돼 있다** |
| 0.132.0 / 2026-02 `Content-Type` 축자 | ✅ | 🌐 릴리스 노트 원문 일치. PyPI upload 2026-02-23 |
| `tokenUrl="auth/token"`이 문서 값이 아님을 각주가 명시 | ✅ | 문서는 `"token"`. [^10-1] 말미 ⚠️ 표기가 **모범 사례** |

**뉘앙스 지뢰 — passlib (계획서 배정: 10장) ✅ 정확**
line 25가 *"**사실은 이렇다.**"* / *"**해석은 여기서 갈린다.**"*로 **문장 단위 분리**를 명시적으로 수행했다. 지뢰표 요구("사실과 해석을 문장 단위로 분리해 쓴다") 충족. 나아가 *"나는 그 판단이 타당하다고 보지만 그건 내 판단이고"*로 저자 가설임을 표시했다 — 요구 이상.

**§7-2 준수 (근거 0건 구역) ✅ 3항 전건**
1. **Spring Security 전환자 서사 0건.** 원고 전문에서 `Spring`은 **제목 1회 + [^10-5] 부인 각주 1회**뿐이다. 본문은 line 17("필터 사슬")·line 245("선언적 권한 표현")처럼 **구조 대조 명사만** 쓰고 체감·경험담을 만들지 않았다.
2. **antoinewdg = Django 비교 맥락 명시.** line 45가 본문에서 *"FastAPI가 아니라 Django와 비교하는 스레드에서"*, [^10-5]가 다시 *"Spring Security 사용자의 전환 경험담이 아니다"*로 **이중 방어**. 🌐 Lobsters 원문 재확인 — 스레드는 "Django vs. FastAPI, An Honest Comparison"(2025-01-15)이고 Spring 언급 0건. ✅
3. **「조립의 비용」과 Spring Security 체감의 분리.** 「부품의 생사는 누가 지키는가」 절(부품 방치 = 사실)과 「인가를 의존성으로 조립하기」 절(구조 대조)이 다른 절로 갈려 있고 서로를 근거로 쓰지 않는다. ✅
- 인용 부호 차이: Lobsters 원문은 `"build it yourself"`(겹따옴표), 원고는 `'build it yourself'`(홑따옴표). 한국어 인용 부호 안의 중첩 처리이므로 ✅.

**제약 10 (Spring 측 설정 키·기본값·엔드포인트 경로) ✅**
이 장에는 Spring 쪽 **설정 키 0건 · 기본값 0건 · 엔드포인트 경로 0건**이다. 구조 명사(필터 사슬)로만 대조했다 — 계획 제약 10-(b) 경로.

**계약 §3-6 「핸들러 3개」 vs 401 — ✅ 저술가 판단 타당**
- 새 예외 **0건**(계약 §7 10장 행의 *"새 예외 만들지 마라"* 준수). `PermissionDeniedError`를 재사용하고 `code=`로만 좁혔다(line 280–282).
- `PermissionDeniedError("…", code="project.permission_denied")` 호출 형태는 `03_final.md` line 248–261의 `__init__(self, message: str, *, code: str | None = None, …)`와 **정확히 일치**한다 ✅ (키워드 전용 `code` 수용).
- 401은 `HTTPException`으로만 두었고 **프레임워크 기본 핸들러**가 처리하므로 앱이 정의한 핸들러는 여전히 3개다. 계약 §3-5가 이미 *"`HTTPException`의 기본 응답은 `{"detail": ...}`(단수)"*를 예고했고 `03_final.md` line 235가 그 구분을 실행했다. **원고 line 200이 그 비용(`ErrorResponse`가 아닌 응답 1건 발생)을 본문에 명시**한 것이 결정적이다 — 감춘 게 아니라 밝힌 편차다.
- 🕒 편집자 참고: 3장 line 331은 *"핸들러가 늘어나면 응답 모양이 갈라진다"*고 썼는데, 10장에서 **핸들러를 안 늘리고도 응답 모양이 하나 갈라진다.** 문자는 지켰고 취지는 한 칸 어긋난다. 10장이 그 비용을 명시했으므로 판정은 ✅이나, editor가 3장에 한 줄 콜백을 넣을지 판단할 만하다.

**교차 충돌 (1~9장 최종본 × 10장) — 위 ❌2·❌3 외 0건**

| 대조 대상 | 판정 |
|---|---|
| 3장 에러 계약(`PermissionDeniedError` 재사용·새 예외 0건·핸들러 3개) | ✅ |
| 4장 `deps.py`(`SessionDep`·`SettingsDep`·`CurrentUser` 별칭, 호출부 불변) | ✅ (시그니처 문구는 ❌2) |
| 6장 `ProjectRole`(`enum.Enum`, 멤버 `member`·`maintainer`·`owner`) | ✅ — `ROLE_RANK`가 필요한 이유(열거형 비교 불가) 서술이 `06_final.md` line 109–112와 정확히 맞는다 |
| 6장 `ProjectMember`(`project_id`·`user_id`·`role`) | ✅ |
| 6장 `User`/`users`/`email` | ✅ (6장 line 36 엔티티 표가 정본) |
| 2장 `Settings` 접두사 `TRACKER_` | ✅ (`TRACKER_JWT_SECRET_KEY`) · 계약 §3-4 시크릿 3필드와 필드명 일치 |
| 계약 §3-7 라우터 규약(`api/auth.py`, prefix `/auth`, tags `["auth"]`, 변수명 `router`) | ✅ |
| 앞 장이 소유한 표면에 각주 중복 부착 | ✅ 0건 — `status.HTTP_401_UNAUTHORIZED`(3장 소유 T1)·`pydantic_settings.BaseSettings`(2장 소유)에 각주를 다시 달지 않았다 |

**양화사** — `모든`·`전부`·`유일`·`항상`·`처음으로` 오용 0건. line 13의 "가장 자주 쓰이는"만 위 ⚠️로 처리.
**§7-1 금지선** — Reddit·Stack Overflow 인용 **0건**(grep 확인). `#14603` **미등장** ✅.
**`(사실 확인 필요)` 마커** — 0건(저술가 신고와 일치).

### 10장 소계

| 판정 | 건수 |
|---|---|
| ❌ BLOCKING | **3** (인용 축자 헤지 삭제 · `get_current_user` 시그니처 모순 · `UserRepository` 생략 표기 허위) |
| ⚠️ 조치 필요 | 4 |
| 🕒 | 0 |
| ✅ | 42 |

T2 구역 12표면 전건 웹 2차 통과. 이 장의 결함은 **전부 「인용 정확도」와 「원고 내부 정합성」**이고, 외부 API 표면 추적 실패는 0건이다.

---

## 11장

**검증 라운드 1 · 2026-07-26 · 배치 4**
초안 `chapters/11_draft.md` (18,748 bytes). 대조: `01_reference.md`(§5-A·버전 핀 E·J·지뢰표 httpx2 행) · `tracker_contract.md`(§7·§8-1 테스트 행·§8-3 T2 testcontainers) · `02_plan.md` 11장 · `chapters/03·04·06·07_final.md` · `chapters/12_draft.md`.
**계약 §8-3 T2(testcontainers)와 지뢰표 최대 지뢰(httpx2 3층)가 동시에 걸리는 장이다.** httpx2 심볼은 배포된 `httpx2-2.9.1-py3-none-any.whl` **실물**과, SQLAlchemy 비동기 배선은 `rel_2_0_51` **태그 소스**와 직접 대조했다.

### ❌ 정정 필요 (BLOCKING)

**11-❌1. 테스트 의존성을 넣는 줄이 이 장에 없다 — 계약 §7 교차규칙 1 위반이자 12장 불정합의 진원지**

전 원고 `uv add` grep: 1장·7장(2)·8장·9장·10장·12장에 있고 **11장만 0건**이다. line 51의 `uv add httpx`는 *"FastAPI 테스트 문서도 설치 명령으로 `uv add httpx`를 안내하고"* — **공식 문서가 무엇을 안내하는지**를 서술한 것이지 이 책이 의존성을 넣는 명령이 아니다.

계약 §7 교차규칙 1: *"의존성 추가는 그 장에서 처음 쓰는 장이 한다. `uv add {패키지}` 한 줄을 그 장 본문에 남긴다. 뒤 장은 이미 설치된 것으로 간주한다."*
11장이 처음 쓰는 것: `pytest` · `anyio`(line 208 `import anyio`) · `httpx2`(line 164·185·210). 뒤 장(12장)이 **이미 설치된 것으로 간주하고 있다** — `12_draft.md` line 81 *"11장에서 테스트 도구를 넣을 때 그룹이 만들어졌으니"* + `[dependency-groups] dev` 안의 `# ...(11장, 생략)`. 그 전제가 지금 비어 있다.

**[정정안]** 「`TestClient`를 못 쓰게 되는 지점」 절 앞(또는 line 61 *"`tracker`는 테스트 의존성으로 httpx2를 고른다"* 직후)에 한 줄:
```bash
uv add --dev pytest anyio "httpx2[ws]"
```
세 가지가 동시에 해결된다.
1. **`--dev`가 필수다.** 12장의 `[dependency-groups] dev` 블록과 정합하려면 `dev` 그룹으로 들어가야 한다(🌐 확인: *"uv uses the `[dependency-groups]` table (as defined in PEP 735) … The above command will create a `dev` group"*).
2. **`[ws]` extra가 필수다.** 🌐 httpx2 2.9.1 휠의 `pyproject.toml` — `ws = ["wsproto>=1.2"]`, PyPI `provides_extra: ['brotli','cli','http2','socks','ws','zstd']`, 공식 문서 *"`pip install 'httpx2[ws]'`"*. **extra 없이는 line 211의 `from httpx2.websockets import ASGIWebSocketTransport`가 임포트에서 죽는다.** 현재 원고는 이 extra를 **[^11-6] 각주에서만** 언급하고 본문에서 설치하지 않는다 — 각주를 안 읽은 독자는 마지막 절 코드에서 막힌다. line 200의 *"httpx2에는 SSE와 WebSocket이 내장돼 있다 … 서드파티 없이 테스트할 수 있다"*도 이 한 줄이 있어야 정확해진다(별도 패키지가 아니라 extra라는 뜻이 살아난다).
3. 12장 line 81과 `# ...(11장, 생략)`이 참일 근거가 생긴다.

**고칠 쪽은 11장이다.** 12장의 구조는 계약 §7(12장 「바꾼다」 = `pyproject.toml` 개발 의존성)과 정확히 맞고, `13_draft.md`도 이 배치를 전제한다.

### ⚠️ 근거 부족 — 조치 필요

- **([^11-2]) starlette 소스 구조를 `try: import httpx2 / except: import httpx`로 적었는데 실제 소스와 다르다.**
  🌐 `Kludex/starlette` 태그 `1.3.1` `starlette/testclient.py` L32–51 원문:
  ```python
  try:
      import httpx2 as httpx
  except ModuleNotFoundError:
      try:
          import httpx
      except ModuleNotFoundError:  # pragma: no cover
          raise RuntimeError(...)
      else:
          warnings.warn(
              "Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.",
              StarletteDeprecationWarning,
              stacklevel=2,
          )
  ```
  차이 셋. ① 잡는 예외는 `except:`(무차별)가 아니라 **`except ModuleNotFoundError:`** ② `import httpx2 **as httpx**` — **별칭**을 걸어 모듈 전체가 계속 `httpx.` 이름으로 쓰인다 ③ 경고 종류는 **`StarletteDeprecationWarning`**.
  각주가 *"starlette 1.3.1 태그 소스"*라고 출처를 특정하므로 도식이라도 소스와 어긋나면 안 된다. **본문 line 57의 산문 서술(*"임포트를 시도하고 실패하면 구 httpx를 임포트한 뒤 경고를 띄운다"*)은 정확하다 — 문제는 각주뿐이다.**
  **[정정안]** [^11-2] → `` `try: import httpx2 as httpx / except ModuleNotFoundError: import httpx` + `StarletteDeprecationWarning` 구조는 starlette 1.3.1 태그 소스 ``
  ②의 `as httpx` 별칭은 본문에 넣으면 논지가 오히려 강해진다 — 갈아탄 뒤에도 **이름은 그대로 두었다**는 것이 "권장이지 필수 아님"의 또 하나의 증거다.

- **([^11-5]) testcontainers 축자의 출처 페이지가 틀렸다.**
  각주는 *"Version 4.0.0 onwards we do not support the testcontainers-\* packages"*를 **PostgreSQL 모듈 페이지** 출처로 묶었다. 🌐 확인: 이 문장은 **문서 최상위 인덱스의 Installation 절**에 있다. 전문은 *"Version 4.0.0 onwards we do not support the `testcontainers-*` packages as it is unsustainable to maintain ownership."*
  **[정정안]** [^11-5]를 두 출처로 분리 — `PostgresContainer`·`get_connection_url()`·`driver=None`은 *PostgreSQL* 모듈 페이지, `testcontainers-*` 축자는 https://testcontainers-python.readthedocs.io/ **인덱스 Installation 절**.

- **([^11-6]) "`client.post`·`response.json()`은 9장 각주의 httpx 표면 그대로다"가 반만 맞다.**
  `09_final.md` [^9-4]가 확인한 것은 **`client.get(...)`**·`response.json()`이지 `client.post`가 아니다. (`response.status_code`는 레퍼런스 §5-A 공식 예제로 별도 추적됨.) 실질 위험은 낮지만 각주가 "그대로다"라고 단정한다.
  **[정정안]** *"`response.json()`·`response.status_code`는 9장 각주와 §5-A 공식 예제의 httpx 표면 그대로이고, `client.post`는 같은 API Reference의 대응 메서드다"* 정도로 좁힌다.

### 🕒 신선도 경고 — 1건 (BLOCKING)

- **🕒 (line 19·21–31) anyio 공식 문서가 이제 마커보다 설정 옵션을 먼저 권한다.**
  원고는 *"쓰는 방법은 간단하다. 비동기 테스트 함수에 마커를 붙이면 된다"* + `anyio_backend` 픽스처 오버라이드로 간다. 🌐 anyio stable(4.14.2 / 2026-07) *Testing with AnyIO* 확인 — 현재 문서는 마킹 방법을 **3가지**로 제시하며 **첫 번째로 설정을 권한다**: *"The simplest way is thus the following: `[tool.pytest.ini_options]` / `anyio_mode = "auto"`"*. 또 *"This does not work if `pytest-asyncio` is installed and configured to use its own `auto` mode, as it will conflict with the AnyIO plugin."*라는 **충돌 경고**가 명시돼 있다 — 원고 line 33이 바로 그 `pytest-asyncio`의 `asyncio_mode=auto`를 대안으로 소개하는 자리다.
  원고의 서술은 **틀리지 않았다**(마커 방식은 여전히 문서에 있고, FastAPI 공식 예제가 쓰는 방식이다). 신선도만의 문제다.
  **[해소안]** 둘 중 하나면 충분하다. ① line 19에 버전 시점을 박는다 — *"anyio 4.14.2 / 2026-07 기준으로 …"* ② 한 문장 추가 — *"anyio 문서는 `anyio_mode = "auto"` 설정으로 마커를 생략하는 길도 함께 안내한다. 다만 `pytest-asyncio`의 `auto` 모드와 동시에 켜면 충돌한다고 못 박는다."* ②를 택하면 line 33의 `pytest-asyncio` 문단과 자연스럽게 이어진다.

**🕒에서 ✅로 내린 것 (판정 확정 — 저자 조치 불필요)**

- **([^11-1] 관련) pytest-asyncio `event_loop` 제거 서술.**
  원고 line 33의 *"1.0.0(2025-05-26)에서 `event_loop` 픽스처가 제거됐다"*는 🌐 changelog 원문(`1.0.0 … 2025-05-26` → `Removed` → *"The deprecated *event_loop* fixture. (#1106)"*)과 **정확히 일치**한다. 원고는 1.0.0을 최신이라 **주장하지 않고**, 제거가 일어난 시점만 과거형으로 말하므로 시간이 지나도 참이다. 1.0.0 이후 추가된 *"Overriding the *event_loop_policy* fixture is deprecated. Use the `pytest_asyncio_loop_factories` hook instead. (#1419)"*는 **원고가 `event_loop_policy`를 언급하지 않으므로 무관**하다. → **✅ 확정, 정정 불필요.**
  (선택 사항으로만: line 33에 *"(1.4.0 / 2026-05 기준)"*을 붙이면 최신 버전까지 밝혀지지만, 없어도 문장은 틀리지 않는다. 차단 항목 아님.)

### ✅ 확인됨

**🚨 지뢰표 최대 지뢰 — httpx2 3층 ✅ 3층 전건 정확**

| 층 | 원고 서술 | 판정 | 근거 |
|---|---|---|---|
| ① FastAPI 의존성 | line 51 "`[standard]` extra가 핀하는 것은 `httpx<1.0.0`, 즉 여전히 구 httpx" | ✅ | 버전 핀 J `requires_dist`의 `httpx<1.0.0,>=0.23.0` |
| ② Starlette TestClient | line 53–55 "httpx2로 옮겨간 쪽은 여기다" + 축자 | ✅ **축자 실재** | 🌐 `Kludex/starlette` 태그 1.3.1 `docs/testclient.md` **단어 단위 일치**: *"The `TestClient` is built on `httpx2`. Plain `httpx` is still supported, but deprecated - install `httpx2` (included in `starlette[full]`) instead."* |
| ③ 코드의 실제 모양 | line 57 "폴백을 남겼다 … 권장이지 필수가 아니다" | ✅ (각주 도식만 ⚠️ 위 참조) | 🌐 `testclient.py` L32–51 |
| **금지 서술 미등장** | **"FastAPI가 httpx2로 갈아탔다"** | ✅ **0건** | grep 확인. 오히려 line 49가 *"그걸 'FastAPI가 httpx2로 갈아탔다'로 읽으면 틀린다"*로 **명시적으로 부인**하고, line 59가 *"모순이 아니다. 서로 다른 층의 사실일 뿐이다"*로 지뢰표 요구 문장을 그대로 실행한다 |

지뢰표(계획 §뉘앙스 지뢰 4행)가 요구한 3항이 전부, 요구한 순서대로 들어가 있다. **이 장의 가장 큰 위험이 가장 잘 처리됐다.**

**🚨 httpx2 코드 표면 — 🌐 배포 휠 2.9.1 실물 대조, 실패 0건**
계약 §8-1 「테스트」 행이 추적한 것은 httpx2의 `EventSource`·`ServerSentEvent`·`httpx2.websockets`까지이고, **최상위 `ASGITransport`와 클래스명 `ASGIWebSocketTransport`는 계약 밖**이었다. 계약 §8-5 절차대로 1차 소스로 확인했다.

| 표면 | 판정 | 근거 |
|---|---|---|
| `from httpx2 import ASGITransport, AsyncClient` | ✅ | `httpx2-2.9.1-py3-none-any.whl` → `httpx2/__init__.py`의 `__all__`에 `"ASGITransport"`·`"AsyncClient"` 실재 |
| `AsyncClient(transport=ASGITransport(app=…), base_url=…)` | ✅ | 공식 *Transports* 문서: `transport = httpx2.ASGITransport(app=app)` / `async with httpx2.AsyncClient(transport=transport, base_url="http://testserver") as client:` |
| `from httpx2.websockets import ASGIWebSocketTransport` | ✅ **이름·대소문자·경로 정확** | 휠 `httpx2/websockets/__init__.py`: `from ._transport import ASGIWebSocketTransport` / `__all__ = ["ASGIWebSocketTransport", …]` |
| `ASGIWebSocketTransport(wired_app)` **위치 인자** + `base_url` 없이 전체 URL | ✅ | 공식 WebSockets 문서의 ASGI 예제가 **정확히 그 형태**다 |
| `client.websocket(url)`이 async 컨텍스트 매니저 | ✅ | *"`client.websocket()` is a context manager that performs the WebSocket handshake and yields a `WebSocketSession`"*. 휠 `_client.py`에 sync·async 양쪽 `websocket` 정의 |
| `ws.receive_json()` · `send_*`/`receive_*` 텍스트·바이트·JSON | ✅ | *"The session provides `send` and `receive` methods for text, bytes, and JSON messages"* — `send_text/send_bytes/send_json`, `receive_text/receive_bytes/receive_json` |
| `client.sse(url)` + `async for` → `ServerSentEvent`의 `event`·`data`·`id`·`retry`·`json()` (line 200·244, 산문) | ✅ | *"`client.sse()` is a context manager that yields an `EventSource`. Iterating the `EventSource` … yields a `ServerSentEvent` for each event"* + 속성 표 4개 + *"`event.json()` decodes `event.data` for you"* |
| `httpx2[ws]` extra ([^11-6]) | ✅ | 휠 `pyproject.toml` `ws = ["wsproto>=1.2"]` (본문 설치 누락은 ❌1) |
| `base_url="http://test"` (line 170) | ✅ | httpx2 문서는 `"http://testserver"`를 쓰지만 원고는 이를 **httpx2 문서 인용으로 제시하지 않는다.** 레퍼런스 §5-A의 FastAPI 공식 비동기 예제가 `base_url="http://test"`이므로 그 계보다 |

> 📌 맥락 하나 확보: SSE는 httpx2 **2.5.0 (2026-06-25)**, WebSocket은 **2.6.0 (2026-07-14)** — *"Add native WebSocket support by vendoring `httpx-ws`"* — 에서 들어왔다. 원고 line 61의 *"실익은 마지막 절에서 회수한다"*가 **한 달 된 기능** 위에 서 있다. 필요하면 editor가 신선도 한 줄을 붙일 수 있다(판정은 ✅).

**🚨 6장이 넘긴 비동기 롤백 배선 — 🌐 `rel_2_0_51` 태그 소스 대조, 픽스처 전 표면 ✅**
이 장 최대 위험으로 지목된 항목이다. 원고가 조립한 네 표면을 소스에서 직접 확인했다.

| 표면 | 판정 | 소스 원문 |
|---|---|---|
| `AsyncSession(bind=…, **kw)`가 나머지 키워드를 안쪽 `Session`에 전달 | ✅ | `ext/asyncio/session.py`: `def __init__(self, bind=None, *, binds=None, sync_session_class=None, **kw: Any):` → `self.sync_session = … self.sync_session_class(bind=sync_bind, binds=sync_binds, **kw)` — **`expire_on_commit`·`join_transaction_mode`가 이 경로로 전달된다** |
| `AsyncConnection.begin() -> AsyncTransaction` | ✅ | `ext/asyncio/engine.py`: `def begin(self) -> AsyncTransaction:` |
| `await connection.begin()`이 동작하는 이유 = `StartableContext.__await__` | ✅ | `AsyncConnection(StartableContext["AsyncConnection"])`, `__await__()`·`__aexit__()` 구현. **[^11-4]가 이 위임을 정확히 지목한 것이 결정적이다** — `begin()`이 `async def`가 아닌데 `await`를 붙이는 이 줄은 이 메커니즘 없이는 설명되지 않는다 |
| `AsyncTransaction.rollback()` · `AsyncSession.close()` | ✅ | `async def rollback(self) -> None:` · `async def close(self) -> None:` |
| `async with engine.connect() as connection` | ✅ | docstring 원문 *"async with async_engine.connect() as conn:"* |
| `join_transaction_mode="create_savepoint"` | ✅ | 레퍼런스 §5-A + `06_final.md` [^6-x] 동기 레시피 |
| 6장으로부터의 인계 서술 (line 65) | ✅ | `06_final.md` line 390이 *"`AsyncSession` 판은 관련된 두 문서 페이지 어디에도 없다. 전수 확인은 아니니 … 비동기 배선은 11장이 맡는다"* — **원고 line 65의 괄호("전수 확인은 아니니 거기까지만 말하겠다")까지 6장과 동일하게 절제됐다** |
| 세션 close → 트랜잭션 rollback 순서 (line 99) | ✅ | 코드 `finally` 블록과 산문이 일치 |

**저술가의 「`(사실 확인 필요)` 0건」 주장 — 검증됨.** 6장이 "공식 문서 두 페이지에 없다"고 넘긴 구간을 **소스 4표면으로 조립하고 각주로 근거를 남긴** 것이 계약 §8-5가 요구한 절차 그대로다. 추측으로 메운 곳 0건.

**🚨 testcontainers (계약 §8-3 T2) — 판정 ✅ 저술가 판단 옳음**
🌐 확인: `PostgresContainer`(시그니처 `image, port, username, password, dbname, driver='psycopg2', **kwargs`) ✅ · `get_connection_url()` ✅ · 축자 *"Postgres database container. To get a URL without a driver, pass in `driver=None`."* ✅ · **PostgreSQL 모듈 페이지의 코드 예제는 `create_engine` + sync 1개뿐이고 `create_async_engine`·`asyncpg`·`psycopg[async]` 언급이 전무하다** ✅.
따라서 line 129의 *"공식 문서의 예제가 동기 엔진에 psycopg2 URL 하나뿐이라 비동기 드라이버를 지정하는 형태의 예시가 없기 때문이다"*가 **정확**하고, **코드를 빼고 산문으로 간 결정이 계약 §8-3 판정 우선순위**(*"코드가 필요한 게 아니라 산문이 필요한 것"*)와 일치한다. 리서치 §7-5가 testcontainers를 요약 경유 오염 위험으로 지목한 구역에서 **날조 0건**. (출처 페이지 표기만 위 ⚠️.)

**축자·수치**

| 항목 | 판정 | 근거 |
|---|---|---|
| *"By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions."* | ✅ | §5-A 축자 일치 |
| *"AnyIO provides a neat plugin for this"* | ✅ | §5-A |
| *"If your application relies on lifespan events, the `AsyncClient` won't trigger these events."* | ✅ | §5-A 경고 상자 축자 |
| 기본 `anyio_backend`가 *"runs everything on all supported backends"* | ✅ | 🌐 anyio *Testing* 원문 **verbatim** |
| `anyio.fail_after()`가 **동기** 컨텍스트 매니저 (`with`, `async with` 아님) | ✅ | 🌐 `_core/_tasks.py` L158–161 `@contextmanager` / `def fail_after(...)`. **원고 line 218이 `with anyio.fail_after(1):`로 정확히 썼다** |
| `anyio.sleep()` | ✅ | 🌐 `_core/_eventloop.py` L88 |
| `@pytest.mark.anyio` | ✅ | 🌐 anyio *Testing* |
| 공식 예제 디렉터리에 `conftest.py` 없음 → 양쪽 백엔드 실행 | ✅ | §5-A ⚠️ 함정 항목 |
| pytest-asyncio `asyncio_mode` `strict`(기본)/`auto` | ✅ | 🌐 *"If no asyncio mode is specified, the mode defaults to `strict`."* |
| pytest-asyncio 1.0.0(2025-05-26) `event_loop` 제거 | ✅ | 🌐 changelog `1.0.0 … 2025-05-26` → `Removed` |
| asgi-lifespan **2.1.0 / 2023-03**, "3년 넘게 새 릴리스가 없다" | ✅ | 🌐 PyPI `2.1.0` upload **2023-03-28T17:35:47Z** — 검증 시점 기준 3년 4개월. §5-A의 "정체 상태를 병기하라" 지시 준수 |
| 구 httpx 0.28.1 / **2024-12-06**, "1년 7개월째" | ✅ | 버전 핀 E + 산술(2024-12-06 → 2026-07-26 = 19개월 20일) |
| testcontainers 4.15.0 / 2026-07 | ✅ | 버전 핀 E (2026-07-24) |
| FastAPI 0.140.0 / 2026-07 | ✅ | 버전 핀 B |
| 5장 회수 — anyio 기본 리미터 40 (line 15) | ✅ | §1-3 |

**저자 가설 표시 — ✅ 검증됨**
line 17: *"**여기서부터는 저자의 읽기다.** 공식 문서는 anyio 플러그인을 권하면서 **이유를 밝히지 않는다.**"* — 「왜 anyio인가」 전체가 저자 가설로 명시 표시돼 있다. §5-A·anyio·FastAPI 문서 어디에도 선택 이유가 없다는 것을 확인했고, 원고가 그 공백을 사실로 위장하지 않았다. 계획 제약 1(원인 귀속은 저자 가설로) 준수.
「저자 설계」 마커 **3건** — 비동기 롤백 픽스처(line 71) · 오버라이드 경계(line 135) · `wait_for_subscriber`(line 202). 전부 공식 권장이 아닌 지점에 정확히 붙었다.

**§7-2 준수 (JUnit/MockMvc ↔ pytest/TestClient 근거 0건) — ✅**
line 133이 *"Spring의 `@MockBean`, NestJS의 `overrideProvider()`에 대응하는데 구조는 훨씬 노골적이다. 컨테이너가 빈을 바꿔치기하는 게 아니라 딕셔너리에 함수 하나를 넣는다."* — **구조 대응 한 문장**이고 체감·경험담·정량 비교가 없다. line 125의 *"Spring의 `@Transactional` 테스트 롤백이 해주던 일"*도 애너테이션 이름만 쓴다.
**제약 10 준수:** Spring 측 **설정 키 0건 · 기본값 0건 · 엔드포인트 경로 0건.** 계획 제약 10-(b)(수치·키를 빼고 구조만 대조) 경로.
`alias_httpx`(§8-4 T3, 11장 배정) — **미등장** ✅. 미확인 항목을 억지로 채우지 않았다.

**코드 API 표면 — 내부 정의 대조 (외부 대조로는 안 잡히는 유형)**

| 원고가 부르는 것 | 정의 위치 | 판정 |
|---|---|---|
| `from tracker.db import engine` | `06_final.md` line 328 `engine = create_async_engine(...)` | ✅ |
| `from tracker.db import get_session` | `06_final.md` line 338 | ✅ |
| **오버라이드 키가 `tracker.db.get_session`이어야 한다는 주장 (line 174)** | `06_final.md` line 344–352의 `deps.py`가 **`from tracker.db import get_session`으로 재수출**하고 `SessionDep = Annotated[AsyncSession, Depends(get_session)]`에 그 객체를 넣는다 | ✅ **주장이 정확하다.** 이 장에서 가장 강하게 가르치는 문장인데, 6장이 로컬 래퍼를 만들었다면 픽스처가 조용히 무효가 됐을 자리다 |
| `from tracker.deps import get_event_bus` | `07_final.md` line 317 `def get_event_bus(request: Request) -> EventBus:` | ✅ (`lambda: event_bus` 오버라이드는 원 시그니처와 무관 — 대체 콜러블의 시그니처가 쓰인다) |
| `from tracker.events import InMemoryEventBus` | `07_final.md` line 144 | ✅ |
| `bus.queues.get(issue_id)` (line 219) | `07_final.md` line 146 `self.queues: dict[int, list[asyncio.Queue[IssueEvent]]] = {}` | ✅ — `list` 또는 `None`을 돌려주므로 `while not …`이 성립 |
| `event_bus.publish(IssueEvent(...))` | `07_final.md` line 148 `async def publish(self, event: IssueEvent) -> None:` | ✅ |
| `IssueEvent(issue_id=, event_type=, payload=, occurred_at=)` | `07_final.md` line 69–73 — 필드 4개 **정확히 일치**. `payload: dict[str, str]`에 `{"status": "resolved"}` 대입도 타입 일치 | ✅ |
| `from tracker.schemas.common import IssueEvent` | 계약 §3-8이 위치를 `schemas/common.py`로 확정, `07_final.md`가 그대로 정의 | ✅ |
| **line 242의 메커니즘 주장** — *"7장의 엔드포인트는 `accept()` 직후 이벤트를 밀어내는 태스크를 따로 띄우는데"* | `07_final.md` line 349–356: `await websocket.accept()` → **`pusher = asyncio.create_task(push_events(websocket, events, issue_id))`** | ✅ **원고 자신의 코드에 대한 인과 주장이 실제 코드와 일치한다.** 없는 메커니즘을 지어낸 게 아니다 |
| `ws.receive_json()` ↔ 7장이 보내는 것 | `07_final.md` line 359–361 `await websocket.send_text(event.model_dump_json())` — 텍스트 프레임의 JSON이므로 `receive_json()` → `IssueEvent.model_validate(dict)` 성립 | ✅ |
| `ws://testserver/ws/issues/1` | `07_final.md` line 346 `@router.websocket("/ws/issues/{issue_id}")` (라우터 prefix 없음, 계약 §3-7) | ✅ |
| `from tracker.models.project import Project` (`key`·`name`) | `06_final.md` line 115–121 | ✅ |
| `response.status_code == 422` / `response.json()["code"] == "request.validation_failed"` | `03_final.md` line 320–321 `_error(request, "request.validation_failed", …)` + `JSONResponse(status_code=422, …)` | ✅ **3장 계약과 정확히 일치** |
| `app.dependency_overrides[...]` · `= {}` | 계약 §8-1 추적됨 + `04_final.md` line 284–285 | ✅ |
| `from tracker.main import app` | `03_final.md` line 296 `app = FastAPI(title="tracker")` | ✅ |
| `IssueServiceDep`·`get_issue_service`·`SessionDep` 서술 (line 178) | 계약 §3-4 + `04_final.md` line 92–97 | ✅ |
| `get_current_user` 회수 (line 178) | 10장이 채운다 — 정합 | ✅ |
| **`status.HTTP_422_*` 사용** | **0건.** line 192가 정수 리터럴 `422`를 쓴다 | ✅ |
| **미정의 참조** | **0건** | ✅ |

**코드 주석 전수 검사 (날조 사례 1 유형)** — 이 장 7개 코드 블록의 주석은 **파일 경로 7건이 전부**다. 동작 설명 주석 **0건** ✅.
**저술가의 `ast` 사전 대조 주장(`wired_app` sync→async 등 3건) 검증:** line 152–160의 `wired_app`은 실제로 `async def` + `AsyncIterator[FastAPI]`로 선언돼 있고, 같은 파일 앞 블록에서 온 `AsyncSession`·`AsyncIterator`·`pytest` 임포트가 전부 살아 있다. **남은 미정의 참조 0건 — 독립 재대조로 확인.**
**§7-1 금지선** — Reddit·Stack Overflow **0건**, `#14603` 미등장 ✅.
**양화사** — line 19의 *"지원하는 모든 백엔드"*는 anyio 축자 *"runs everything on all supported backends"* 근거 ✅ · line 178 *"그 아래가 전부 진짜로 돈다"*는 앞 문장이 근거를 깐 서술 ✅. 오용 0건.
**`(사실 확인 필요)` 마커** — 0건(저술가 신고와 일치, 위 대조로 뒷받침됨).

**교차 충돌 (3·4·6·7장 최종본 × 11장)** — ❌1 외 **0건.**

| 대조 대상 | 판정 |
|---|---|
| 6장 `db.py`·`engine`·`session_factory`·`get_session` | ✅ (`session_factory`는 쓰지 않고 `engine`에서 직접 커넥션을 잡는다 — 격리 목적상 옳다) |
| 6장의 「비동기 배선은 11장이 맡는다」 인계 | ✅ 정확히 인수 |
| 4장 `dependency_overrides` 소개 → 11장 회수 | ✅ line 133이 *"소개만 하고 미뤄뒀다"*로 명시 |
| 7장 `InMemoryEventBus`·`EventBusDep`·`get_event_bus`·WS/SSE 엔드포인트 | ✅ |
| 3장 에러 계약(422·`request.validation_failed`) | ✅ |
| 2장 `Settings.database_url`·`TRACKER_DATABASE_URL` | ✅ 계약 §3-4 접두사 규약 |
| 10장 `get_current_user` | ✅ |
| 12장 `[dependency-groups]` | **❌1** |
| 앞 장이 소유한 표면에 각주 중복 부착 | ✅ — [^11-4]가 *"`engine.connect()`·`expire_on_commit=False`는 6장 각주 문서"*로 **8장 [^8-3]의 모범 패턴을 그대로 따랐다** |

**editor 관찰 (판정 아님 — ❌로 세지 않는다).** line 178 말미의 *"인증 경로에는 `get_current_user`가 더해진다 — 10장이 채운 함수다"*는 산문으로만 있고, `wired_app` 픽스처(line 152–160)가 실제로 오버라이드하는 것은 `get_session`·`get_event_bus` **둘뿐**이다. 원고를 *"인증 경로를 테스트할 때는 여기에 `get_current_user`를 하나 더 얹는다"*로 읽으면 앞뒤가 맞고 실제로 그렇게 읽힌다 — **존재하지 않는 코드를 있다고 주장하는 것이 아니므로 ❌가 아니다.** 다만 세 줄짜리 픽스처를 보고 있는 독자에게는 "그 셋째 줄이 어디 있지?"가 될 수 있으니, editor가 *"인증 경로를 검증하는 테스트라면 여기에 `get_current_user` 오버라이드가 한 줄 더 붙는다"*처럼 조건절을 넣을지 판단할 만하다.

### 11장 소계

| 판정 | 건수 |
|---|---|
| ❌ BLOCKING | **1** (테스트 의존성 `uv add --dev` 누락 — `httpx2[ws]` extra 포함) |
| 🕒 BLOCKING | **1** (anyio 문서가 `anyio_mode = "auto"`를 먼저 권하게 바뀜 — 시점 명기 또는 한 문장으로 해소) |
| ⚠️ 조치 필요 | 3 (각주 3건: starlette 소스 도식 · testcontainers 출처 페이지 · 9장 각주 인계 범위) |
| ✅ | 52 (pytest-asyncio 항목을 🕒에서 ✅로 확정 이관) |

**사전 위험도 1위였던 두 항목이 모두 통과했다.** httpx2 3층 지뢰는 지뢰표 요구를 항목별로 실행했고 코드 표면 9건이 **배포 휠 실물**과 일치했다. 6장이 넘긴 비동기 롤백 배선은 **`rel_2_0_51` 태그 소스 4표면**이 전부 확인됐으며, `await connection.begin()`이 성립하는 이유(`StartableContext.__await__`)까지 각주가 정확히 지목했다 — 이 배치에서 가장 잘 조립된 코드다. 남은 ❌는 코드가 아니라 **그 코드를 돌리기 위해 설치해야 할 한 줄**이다.

---

## 12장

**검증 라운드 1 · 2026-07-26 · 배치 4**
초안 `chapters/12_draft.md` (17,122 bytes). 대조: `01_reference.md`(§5-C·버전 핀 A·E) · `tracker_contract.md`(§7·§8-1 uv·CI 행) · `02_plan.md` 12장 · `chapters/01_final.md`·`11_draft.md`·`13_draft.md`.
**GitHub Actions 액션 이름·버전은 날조가 가장 쉬운 영역이라 전수 웹 2차했다 — 실패 0건.**

### ❌ 정정 필요 (BLOCKING)

**12-❌1. (line 81 · line 89) 11장이 하지 않은 일을 했다고 서술한다 — 11↔12장 `[dependency-groups]` 불정합**

원고:
> line 81: "**11장에서 테스트 도구를 넣을 때 그룹이 만들어졌으니** 두 줄이 늘 뿐이다."
```toml
# pyproject.toml
[dependency-groups]
dev = [
    # ...(11장, 생략)
    "ruff==0.16.*",
    "pyrefly>=1.1,<2",
]
```
**대조 결과: `11_draft.md`에는 의존성 추가 명령이 한 줄도 없다.** 전 원고 `uv add` grep 결과 — 1장 `uv add "fastapi[standard]"` · 7장 `uv add websockets`·`uv add redis` · 8장 `uv add python-multipart` · 9장 `uv add "strawberry-graphql[fastapi]"` · 10장 `uv add "pwdlib[argon2]" pyjwt` · **12장 `uv add --dev ruff pyrefly`**. 11장은 **0건**이다.
11장 line 51의 `uv add httpx`는 **FastAPI 공식 문서가 무엇을 안내하는지 서술한 것**이지 이 책이 의존성을 넣는 명령이 아니다.

따라서 ① `# ...(11장, 생략)`이 존재하지 않는 앞 장 내용을 가리키고(계약 §6-3 위반), ② line 81이 거짓 진술이 되며, ③ **계약 §7 교차규칙 1**(*"의존성 추가는 그 장에서 처음 쓰는 장이 한다. `uv add {패키지}` 한 줄을 그 장 본문에 남긴다"*)이 11장에서 깨진다.

**[정정안] 고칠 쪽은 11장이다.** 12장의 구조는 계약 §7(12장 "바꾼다: `pyproject.toml`(개발 의존성·도구 설정)")과 정확히 일치하므로 손대지 않는다. 11장이 `conftest.py`를 처음 보이기 전에 한 줄을 넣는다.
```bash
uv add --dev pytest anyio httpx2
```
(`httpx2.websockets`가 extra 뒤에 있다면 `"httpx2[ws]"`. 11장 [^11-6]이 `httpx2[ws]` extra를 언급하므로 저술가가 1차 소스로 확정할 것.)
`--dev`가 반드시 붙어야 12장의 `[dependency-groups] dev` 블록과 정합한다.

### ⚠️ 근거 부족 — 조치 필요

- **([^12-2]) 각주 URL 2건이 실제 인용처와 다르다 — 🌐 웹 2차로 확정.**

| 축자 | 각주가 적은 URL | **실제 소재 (🌐 확인)** |
|---|---|---|
| `--frozen`: *"To use the lockfile without checking if it is up-to-date"* · `--locked`: *"If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile."* | `docs.astral.sh/uv/reference/cli/` | **`docs.astral.sh/uv/concepts/projects/sync/`**. CLI 레퍼런스는 같은 플래그를 *"Assert that the `uv.lock` will remain unchanged"* / *"Run without updating the `uv.lock` file"*로 **다르게** 적는다 — 독자가 `uv sync --help`를 치면 원고의 축자를 못 찾는다 |
| *"uv cannot assert that the `uv.lock` file is up-to-date without each of the workspace member `pyproject.toml` files, so we use `--frozen` … to skip the check during the initial sync."* | `docs.astral.sh/uv/concepts/projects/workspaces/` | **`docs.astral.sh/uv/guides/integration/docker/`**의 「Intermediate layers in workspaces」 절. 워크스페이스 개념 페이지에는 `--frozen`이 **0회** 등장한다 |

  축자 자체는 **둘 다 원문 그대로 실재**한다(🌐 확인). `UV_LOCKED`가 CLI 레퍼런스에 `[env: UV_LOCKED=]`로 문서화된 것도 사실이라 각주의 그 부분은 옳다.
  **[정정안]** [^12-2]의 URL 두 개를 위 오른쪽 열로 교체. 부수 효과로 line 36의 *"`--frozen`의 이유를 밝힌 곳은 워크스페이스 절 하나뿐이다"*가 더 정확해진다 — 그 절이 **Docker 가이드 안의** 워크스페이스 절이기 때문이다.

- **(line 146 ↔ line 122·140) `UV_LOCKED` 설명과 YAML이 어긋나 보인다.**
  본문: *"스텝마다 반복하지 않아도 잡 안의 uv 호출이 같은 규율 아래 놓인다."* 그런데 YAML은 `uv sync --locked`로 **여전히 반복한다.**
  실질은 정확하다 — 🌐 확인: `uv run`도 `--locked`를 받고, 아무것도 안 붙이면 *"Locking and syncing are automatic in uv … when `uv run` is used, the project is locked and synced before invoking the requested command."*이므로 env가 `uv run ruff`/`pyrefly`/`pytest` 세 줄을 덮는 것이 이 설정의 진짜 값이다. 다만 독자는 "반복하지 않아도 된다면서 왜 반복했지?"에서 멈춘다.
  **[정정안]** *"`uv sync`에는 명시적으로 붙였지만, 진짜 값은 `uv run` 세 줄에 있다 — 환경 변수 하나가 그 셋을 함께 덮는다."*

### 🕒 신선도 경고 — 1건 (BLOCKING)

- **🕒 (line 158) "3.10은 2026년 10월에 지원이 끝난다" — 시점 명기가 없다.**
  🌐 devguide 확인 결과 날짜 자체는 ✅. 문제는 **미래 시제**다. **3개월 뒤**면 이 문장은 과거를 미래로 말하게 되고, 신선도를 셀링 포인트로 내건 책에서 독자가 가장 먼저 알아채는 종류의 낡음이다. `[^12-5]`가 조회 시점을 각주에 두었으나 **본문에는 시점이 없다** — 계획 제약 3(모든 버전·시점은 `"{버전}/{연월} 기준"`)의 취지가 이 문장에 적용되지 않았다.
  **[해소안]** 본문 한 조각. *"FastAPI는 3.10 이상을 요구하지만 **이 책을 쓰는 2026-07 기준으로** 3.10은 석 달 뒤인 2026년 10월에 지원이 끝난다."* 이렇게 두면 2027년 독자에게도 문장이 참으로 남는다.

**🕒에서 ✅로 내린 것 (판정 확정 — 저자 조치 불필요)**

- **(line 50) "2026-07 기준 최신이 0.16.0이니, 언젠가 0.17이 나오는 순간"** — 🌐 확인: **ruff 0.17.x는 존재하지 않는다.** GitHub 릴리스 목록 최상단이 0.16.0(2026-07-23), PyPI 최신도 0.16.0. 저술가 자기 신고(*"존재하는 릴리스로 쓰지 않고 미래형으로 서술"*)가 **정확하다.** 시점(`2026-07 기준`)이 문장 안에 이미 박혀 있고 미래형이라 시간이 지나도 참이다 — **신선도 규율의 모범 사례이므로 ✅**로 확정한다.

### ✅ 확인됨

**§7-4 미확인 2건 해소 — 🌐 1차 소스로 확인. 레퍼런스 갱신 대상이다.**

| 항목 | 원고 서술 | 판정 | 축자 |
|---|---|---|---|
| **mypy 2.0 breaking** (§7-4 미확인) | line 71 "2.0에서 `--local-partial-types`와 `--strict-bytes`가 기본으로 켜졌으니" | ✅ **해소** | `python/mypy` CHANGELOG.md §Mypy 2.0 소제목 축자 **"Enable `--local-partial-types` by Default"**(PR 21163) · **"Enable `--strict-bytes` by Default"** — *"Per PEP 688, mypy no longer treats `bytearray` and `memoryview` values as assignable to the `bytes` type."*(PR 18371) |
| **pytest 9.0 breaking** (§7-4 미확인) | line 160 "`PytestRemovedIn9Warning`이 기본으로 에러가 됐고, `$CI`나 `$BUILD_NUMBER`가 빈 값이 아니어야 CI로 인식한다" | ✅ **해소** | changelog #13779 *"`PytestRemovedIn9Warning` deprecation warnings are now errors by default."* · #13766 *"CI mode is only activated if at least one of those variables is defined and set to a **non-empty** value."* |

> **오케스트레이터·레퍼런스 관리 보고:** `01_reference.md` §7-4의 *"mypy 2.x · pytest 9.x … breaking changes"* 항목을 **해소로 이관** 권고. (같은 줄의 **gunicorn 26.x는 여전히 미확인**이며 12장은 건드리지 않았다 — ✅ 아래 참조.)

**GitHub Actions — 🌐 전수 웹 2차, 날조 0건**

| 원고 표기 | 판정 | 근거 (GitHub Releases API) |
|---|---|---|
| `actions/checkout@v7` / "v7.0.1 / 2026-07 기준" | ✅ | 태그 `v7.0.1`, published **2026-07-20T15:10:05Z** |
| `astral-sh/setup-uv@v9` / "v9.0.0 / 2026-07 기준" | ✅ | 태그 `v9.0.0`, **2026-07-21T15:48:02Z**. 레퍼런스 §5-C와 일치 |
| `setup-uv`의 `enable-cache` · `python-version` 입력 | ✅ | `action.yml@v9.0.0` — `python-version: "The version of Python to set UV_PYTHON to"`. `enable-cache` 기본값은 `"auto"`인데 **원고는 기본값을 주장하지 않고 `true`를 명시 설정**했다 — 충돌 없음 |
| `docker/setup-buildx-action@v4` / "v4.2.0 / 2026-07 기준" | ✅ | **2026-07-02T09:23:15Z** |
| `docker/build-push-action@v7` / "v7.3.0 / 2026-07 기준" | ✅ | **2026-07-01T14:24:45Z** |
| `build-push-action`의 `context`·`push`·`tags` 입력 | ✅ | `action.yml@v7.3.0` — `push`: *"Push is a shorthand for --output=type=registry"*, 기본 `'false'` |
| `actions/setup-python`의 `cache` 축자 | ✅ | `action.yml@v7.0.0` **문자 단위 일치**: *"Used to specify a package manager for caching in the default directory. Supported values: pip, pipenv, poetry."* |
| uv 가이드가 아직 v8.1.0 예제 | ✅ | 레퍼런스 §5-C |

> 🔍 사전 의심을 하나 해소해둔다. 레퍼런스 §5-C가 `actions/setup-python` v7을 **2026-07-20**로 적고 원고가 `checkout` v7.0.1을 **같은 2026-07-20**으로 적어 전치(transposition) 신호로 의심했으나, 🌐 대조 결과 **두 릴리스가 실제로 같은 날**이다(setup-python v7.0.0 · checkout v7.0.1). 우연의 일치이고 원고가 옳다.

**uv·락파일**

| 항목 | 판정 | 근거 |
|---|---|---|
| PEP 751 — Final, Resolution **2025-03-31**, `pylock.toml`, Brett Cannon | ✅ | 🌐 peps.python.org/pep-0751/ 헤더 그대로 |
| PEP 751 *"installation reproducibility"* · uv *"a universal or cross-platform lockfile"* · *"The `uv.lock` format is specific to uv and not usable by other tools"* | ✅ | §5-C 축자 일치 |
| `npm ci` 축자 | ✅ | 🌐 docs.npmjs.com/cli/v11/commands/npm-ci — *"If dependencies in the package lock do not match those in `package.json`, `npm ci` will exit with an error, instead of updating the package lock."* 원고는 뒷부분만 인용했고 의미 왜곡 없음 |
| 플래그 미부착 시 `uv run`이 락파일을 갱신한다 (line 42) | ✅ | 🌐 *"Locking and syncing are automatic in uv. For example, when `uv run` is used, the project is locked and synced before invoking the requested command."* |
| `UV_LOCKED` 환경 변수 형태 | ✅ | 🌐 CLI 레퍼런스 `[env: UV_LOCKED=]` (`--frozen`은 `[env: UV_FROZEN=]`) |
| `[dependency-groups]`(PEP 735) · `uv add --dev` · `dev` 그룹 `uv sync` 기본 포함 | ✅ | 🌐 *"uv uses the `[dependency-groups]` table (as defined in PEP 735) …"* / *"By default, uv includes the `dev` dependency group in the environment"* |
| Poetry 2.4.1 / 2026-05 PEP 621 이동 · pip-tools 생존 · `uv pip compile` 흡수 | ✅ | §5-C + 버전 핀 E(poetry 2.4.1, 2026-05-09) |
| 두 공식 문서가 다른 플래그를 쓴다는 사실 서술 (line 36) | ✅ | §5-C + 🌐 재확인 — uv Docker 가이드 본예제는 `uv sync --locked` |

**품질 도구**

| 항목 | 판정 | 근거 |
|---|---|---|
| ruff 버저닝 축자 (minor=breaking) | ✅ | 🌐 `docs/versioning.md` 문자 일치 |
| ruff 0.16.0 / 2026-07 · `ruff check --fix` · `ruff format --check` | ✅ | 🌐 0.16.0 @ 2026-07-23. 두 명령 모두 공식 문서에 실재 |
| *"drop-in replacement"* · Django·Zulip *"> 99.9% of lines are formatted identically"* | ✅ | 🌐 `docs/formatter.md` |
| **ruff formatter "stable 선언"을 쓰지 않았다** | ✅ **저술가 자기 신고 검증됨** | 🌐 확인: 공식 문서에 그런 선언 **없다**. versioning.md는 오히려 *"Ruff does not yet have a stable API"*. 원고는 이 주장을 **한 번도 하지 않는다** — 레퍼런스 §버전 핀 E의 금지 지시 준수 |
| ty 0.0.63 · *"ty is currently in beta."* · *"breaking changes, including changes to diagnostics, may occur between any two versions"* | ✅ | 🌐 README 축자 일치. 0.0.63 @ 2026-07-23 |
| pyrefly 1.1.1 · *"Pyrefly's current development status is stable."* · *"the default type checker for Instagram's 20-million-line Python codebase at Meta"* · *"any version may introduce new type errors and other breaking changes"* | ✅ | 🌐 README 축자 **4건 전건 일치**. 1.1.1 @ 2026-06-18 |
| `pyrefly check` 명령 | ✅ | 🌐 pyrefly.org 설치 문서 (원고 [^12-4]가 이미 그 URL을 인용 — 정확) |
| `# ty: ignore[deprecated]`(fastapi `applications.py`) | ✅ | §5-C 1차 증거 |
| mypy 2.3.0 / 2026-07 | ✅ | 🌐 PyPI 2.3.0 @ 2026-07-13 |
| **gunicorn 26.x breaking을 미확인으로 두고 이 장에서 건드리지 않았다** | ✅ **저술가 자기 신고 검증됨** | grep — `gunicorn` 원고 등장 **0회**. 계약 §8-4 T3(13장 소유) 준수 |

**§7-2 준수 (출신 귀속·다수설) ✅**
- **출신 귀속 0건.** 저술가가 리서치 원문의 *"Spring/NestJS 출신 독자가 가장 먼저 밟는 지뢰"* 프레이밍을 채택하지 않았다는 신고를 **검증했다** — 원고에 `출신`·`Spring 개발자는`류 문장이 0건이고, line 150이 *"파이썬 프로젝트의 CI라면 … 손이 먼저 나가는데"*로 **메커니즘 서술**로 재작성돼 있다. `Spring`·`NestJS` 단어 자체가 이 장에 **0회** 등장한다. ✅
- **락파일·모노레포 체감 비교 0건** (§7-2 근거 없음 항목). 원고는 `pom.xml`·`npm ci`를 **구조 대조**로만 쓴다 — 계획서 「얇은 지점」 지시 그대로.
- **빈도 주장 0건.** 계획 오프닝 지침이 금지한 *"CI가 가장 많이 막는 것은 ~다"* 형 문장이 없다. line 50의 *"원인은 대개 여기다"*는 인과 서술이 아니라 **버저닝 사실에서 연역한 진단**이고, 앞 문단이 그 근거를 이미 깔았다. ✅
- **다수설 일반화·없는 백래시 0건.**

**계획 ↔ 계약 충돌 (컨테이너 빌드 잡) — ⚠️→ 해소 인정**
- `02_plan.md` 12장 「예제 앱이 자라는 지점」: *"컨테이너 빌드·푸시 잡"* → 12장 소유.
- `tracker_contract.md` §7 row 13 「바꾼다」: *"이미지 빌드·푸시 잡을 `ci.yml`에 추가"* → 13장 소유.
- **판정: 저술가의 `push: false` 분할이 옳다.** 근거 셋 — ① line 166·185가 「저자 설계」 마커와 본문으로 **13장 소유 영역임을 명시**한다, ② `13_draft.md` line 212가 *"그 잡의 `push: false`가 뒤집히고 로그인 스텝이 붙는 것이 이 장이 12장에 되돌려주는 변경이다"*로 **인수를 명시적으로 받는다** — 두 초안이 서로를 알고 있다, ③ 13장 선점 검사에서 **레지스트리·로그인·워커 수·캐시 전략 전건 0건**이다(`enable-cache`는 uv 의존성 캐시이지 앱 캐시 전략이 아니다).
- **[오케스트레이터 보고]** 사실 오류가 아니므로 통과시키되, 계약 §7 row 13의 문구를 *"이미지 **푸시** 잡"*으로 좁힐 것을 권고(계획서 쪽도 동일).
- 🕒 **13장 배치로 이월할 관찰:** `13_draft.md` line 176의 매니페스트는 `image: tracker:latest`인데 line 212 산문은 *"12장의 잡이 커밋 해시로 붙일 이름이 들어온다"*고 하고 12장은 `tracker:${{ github.sha }}`로 태깅한다. **13장 내부의 코드↔산문 불일치**다 — 13장 검증 시 처리할 것.

**교차 충돌 (1장·11장 × 12장)**

| 대조 대상 | 판정 |
|---|---|
| 1장 uv 프로젝트·`pyproject.toml`·명령 대응표 | ✅ line 9가 *"1장에서 … 대응표를 만들 때 락파일 행이 없었던 이유"*로 회수 — `01_final.md` line 137–139 표에 실제로 락파일 행이 없다. **정확** |
| 11장 `tests/` 스위트 (`uv run pytest`) | ✅ 경로·명령 정합 |
| 11장 `[dependency-groups]` | **❌1 참조** |
| 13장 소유 영역 선점 | ✅ 0건 |
| 계약 §8-1 uv·CI 행(`uv sync --locked`·`setup-uv` v9·`setup-python` v7 `cache:`) | ✅ 전건 계약 안 |

**YAML 내부 참조 전수 대조 (저술가 신고 검증)** — `needs: quality`→`jobs.quality` ✅ · `needs: test`→`jobs.test` ✅ · `${{ matrix.python-version }}`→`strategy.matrix.python-version` ✅ · `${{ github.sha }}` ✅ · 두 번째 블록의 2칸 들여쓰기가 `jobs:` 하위에 정확히 붙는다 ✅. **미정의 참조 0건.**
**코드 주석** — 파일 경로 3건 + `# ...(11장, 생략)` 1건뿐. 동작 설명 주석 **0건** ✅.
**`(사실 확인 필요)` 마커** — 0건.
**§7-1 금지선** — Reddit·Stack Overflow **0건**, `#14603` 미등장 ✅.
**양화사** — line 17 *"가능한 모든 파이썬 마커"*(uv 축자 *"across all possible Python markers"* 근거) ✅ · line 144 *"모든 풀 리퀘스트"*(`pull_request:` 무필터의 정확한 서술) ✅. 오용 0건.

### 12장 소계

| 판정 | 건수 |
|---|---|
| ❌ BLOCKING | **1** (11↔12장 `[dependency-groups]` — **11장 ❌1과 동일 결함의 다른 면**이며 실제 정정은 11장) |
| 🕒 BLOCKING | **1** (Python 3.10 EOL 문장에 시점 명기 없음) |
| ⚠️ 조치 필요 | 2 (각주 URL 2건 · `UV_LOCKED` 서술) |
| ✅ | 47 (ruff 0.17 항목을 🕒에서 ✅로 확정 이관) |

**이 장은 배치 4에서 사실 밀도가 가장 높고 오류가 가장 적다.** 날조가 가장 쉬운 GitHub Actions 버전·날짜 8건이 **전건 실재**했고, §7-4 미확인 2건을 1차 소스로 **해소**했으며, 확인 실패한 것(ruff formatter stable·gunicorn 26.x)은 **쓰지 않았다.** 남은 결함은 각주 URL 정확도와, 12장이 아니라 11장에서 비어 있는 한 줄이다.

---

## 🚨 코드 API 표면 대조 결과 (배치 4)

**하네스에 코드 실행·컴파일 단계가 없다. 이 대조가 유일한 방어선이다.**

| 항목 | 10장 | 11장 | 12장 | 계 |
|---|---|---|---|---|
| 코드 블록 | 9 | 7 | 4 | **20** |
| 추출 심볼 (import 경로·클래스·함수·데코레이터·파라미터) | 52 | 43 | 31 | **126** |
| **외부 추적 실패 (라이브러리 API)** | **0** | **0** | **0** | **0** |
| **내부 정의 누락 / 허위 생략 표기** | **1** | 0 | **1** | **2** |
| 가짜 주석 (§4-8 / 날조 사례 1 유형) | 0 | 0 | 0 | **0** |
| `status.HTTP_422_*` | 0 | 0 | — | **0** |
| 인용 축자 변조 | **1** | 0 | 0 | **1** |
| 각주 출처 오기 | 1 | 3 | 2 | **6** |

### import 경로 문자열 별도 grep (심볼이 추적돼도 경로는 별개다)

**전 20블록의 import 문 48개를 경로 문자열 단위로 대조했다. 실패 0건.**

| import 경로 | 근거 | 판정 |
|---|---|---|
| `from fastapi.security import OAuth2PasswordBearer` / `OAuth2PasswordRequestForm` | **🌐 웹 2차 — oauth2-jwt·simple-oauth2 튜토리얼 원문에 동일 문자열 실재** (계약 §8-3 T2 절차 완료) | ✅ |
| `from jwt.exceptions import InvalidTokenError` | **🌐 웹 2차 — 튜토리얼 원문 + `jwt/exceptions.py` 계층 확인** | ✅ |
| `from pwdlib import PasswordHash` | 계약 §8-1 「인증(import 경로만)」 추적됨 + [^10-1] | ✅ |
| `import jwt` (pyjwt) | 계약 §8-1 추적됨 | ✅ |
| `from pydantic_settings import BaseSettings` | 계약 §8-1 추적됨 (2장 소유 — 10장 각주 불필요) | ✅ |
| `from fastapi import APIRouter, Depends, HTTPException, status` / `Path` / `Query` | 계약 §8-1 추적됨 | ✅ |
| **`from httpx2 import ASGITransport, AsyncClient`** | **🌐 웹 2차 — 배포 휠 2.9.1 `__init__.py` `__all__` 실물 확인** (계약 §8-1은 `from httpx import ...`까지만 추적) | ✅ |
| **`from httpx2.websockets import ASGIWebSocketTransport`** | **🌐 웹 2차 — 휠 `websockets/__init__.py` 실물 확인** | ✅ |
| `from sqlalchemy.ext.asyncio import AsyncSession` | 계약 §8-1 추적됨 + 🌐 `rel_2_0_51` 소스 | ✅ |
| `from sqlalchemy import select, func, String` / `from sqlalchemy.orm import Mapped, mapped_column` | 계약 §8-1 추적됨 | ✅ |
| `import anyio` (`fail_after`·`sleep`) | 🌐 anyio 소스 확인 + [^11-1] | ✅ |
| `import pytest` / `from fastapi import FastAPI` | 계약 §8-1·§8-0 | ✅ |
| `from typing import Annotated, AsyncIterator` · `from collections.abc import Awaitable, Callable` · `from datetime import ...` | 계약 §8-0 표준 라이브러리 면제 | ✅ |
| `tracker.*` 내부 경로 **21건** | 계약 §2 모듈 레이아웃 · §3 이름 사전 · §7 성장 맵 | ✅ (아래 2건 예외) |

### 🚨 내부 정의 누락 / 허위 생략 표기 2건

배치 2·3에서 각각 3건·3건이 나온 **이 책 최대 결함 유형**이다. 배치 4는 **2건으로 줄었고, 둘 다 「호출 불가」가 아니라 「생략 표기의 허위 귀속」**이다 — 성격이 한 단계 가벼워졌다.

| # | 위치 | 표기 | 실제 | 판정 |
|---|---|---|---|---|
| 1 | 10장 line 190–191 | `# ...(2장, 생략)` (`UserRepository`) | **2장 트리에 `repositories/user.py` 없음, 전 원고에 `UserRepository` 0건** | **❌** |
| 2 | 12장 line 89 | `# ...(11장, 생략)` (`[dependency-groups] dev`) | **11장에 의존성 추가 0건** | **❌** |
| (참고) | 10장 line 333 | `# ...(2·6장, 생략)` (`ProjectRepository`) | 2장 트리 line 134에 `repositories/project.py` 실재 | ✅ |
| (참고) | 10장 line 135 | `# ...(6장, 생략)` (`User`) | 6장 line 36 엔티티 표가 `User`/`users`/`email`을 정본화 | ✅ |
| (참고) | 11장 `wired_app`·`session`·`client` 픽스처 상호 참조 | — | 같은 파일 앞 블록의 임포트·픽스처가 전부 실재 | ✅ |

**`back_populates` 짝 부재:** 10~12장에 새 `relationship` 선언 0건 — 해당 없음.
**호출 시그니처 불일치:** 0건. (`PermissionDeniedError(msg, code=)` ↔ 3장 `__init__` 키워드 전용 `code`, `publish(IssueEvent)` ↔ 7장, `verify(raw, hashed)` ↔ 공식 소스 인자 순서 — 전건 일치.)

---

## 🔍 저술가 자기 신고 판정 (전건)

### 10장

| 신고 | 판정 |
|---|---|
| T2 표면 12건을 1차 소스로 확인하고 각주를 달았다 | ✅ **전건 실재.** 각주 URL·축자 모두 🌐 재확인. `.verify(plain, hashed)` **인자 순서까지** 공식 소스와 일치 |
| oauth2-scopes는 코드로 싣지 않고 산문으로만 썼다 | ✅ line 247. 계약 §8-3 판정 우선순위 준수 |
| Auth0 연동 코드를 수록하지 않았고, WebFetch 요약이 붙여준 설명 주석을 폐기했다 | ✅ **적발 사례 1·2를 스스로 피했다.** Auth0 등장 0건, 동작 설명 주석 0건(전 코드 블록 주석 = 파일 경로 + 생략 표기뿐) |
| `get_current_user` 파라미터 증가는 "계약 미규정 구간"이다 | **❌ 부분 기각.** 계약 §7 교차규칙 2와 `04_final.md` line 104가 **명시적으로 규정**했고 충돌한다. **다만 저술가의 실질 판단(이름·반환 타입·호출부 불변)은 옳으므로 10장이 아니라 4장 산문과 계약 문구를 고친다** → 10-❌2 |
| 401만 `HTTPException`으로 두고 그 비용을 본문에 명시했다 | ✅ 핸들러는 여전히 3개(프레임워크 기본 핸들러 사용), 새 예외 0건, 계약 §3-5가 이미 예고한 `detail` vs `details` 구분. line 200이 비용을 감추지 않고 밝혔다 |
| passlib 사실/해석을 문장 단위로 분리했다 | ✅ line 25가 *"사실은 이렇다"* / *"해석은 여기서 갈린다"*로 명시 분리 |
| 수치(1년 / 15개월 / 14개월 / 테스트 스위트 포함) | ✅ `research/community.md` §2-5 + 🌐 4스레드 재확인 전건 일치 (#11380 **상태 라벨**만 ⚠️) |
| §7-2 준수 3항 | ✅ 전건 (전환자 서사 0건 · antoinewdg Django 맥락 이중 명시 · 두 논지 절 분리) |

### 11장

| 신고 | 판정 |
|---|---|
| httpx2 3층을 정확히 서술했고 새 축자를 확보했다 | ✅ **축자 verbatim 실재**(🌐 starlette 1.3.1 `docs/testclient.md`). 3층 전건 정확 |
| "FastAPI가 httpx2로 갈아탔다"는 서술이 없다 | ✅ **없을 뿐 아니라 line 49가 명시적으로 부인**한다 |
| testcontainers는 비동기 예시가 없어 코드를 빼고 산문으로만 썼다 | ✅ 🌐 확인 — 모듈 페이지 예제는 sync + psycopg2 **1개뿐**. 판단 정확 |
| `(사실 확인 필요)` 0건이며, `rel_2_0_51` 태그 소스로 비동기 롤백 배선을 조립했다 | ✅ **4표면 전건 소스 확인.** `StartableContext.__await__` 지목이 특히 정확하다 |
| pytest-asyncio 1.0.0 `event_loop` 제거 · asgi-lifespan 2.1.0/2023-03 정체 · `wait_for_subscriber` 헬퍼 | ✅ 전건 (asgi-lifespan은 🌐 upload 2023-03-28 확인, `fail_after`가 **동기** CM인 것도 소스 확인) |
| "왜 anyio인가"를 저자 가설로 표시했다 | ✅ line 17 *"여기서부터는 저자의 읽기다"* |
| `ast` 사전 대조로 `wired_app` sync→async 등 3건을 고쳤다 | ✅ **독립 재대조 결과 잔존 미정의 참조 0건** |

### 12장

| 신고 | 판정 |
|---|---|
| §7-4 미확인 2건(mypy 2.0 · pytest 9.0)을 1차 소스로 해소했다 | ✅ **양쪽 CHANGELOG 축자 확인 — 레퍼런스 §7-4에서 해소로 이관할 만한 발견이다** |
| GitHub Actions 액션 이름·버전을 1차 소스로 확인했다 | ✅ **8건 전수 확인, 날조 0건.** checkout v7.0.1(2026-07-20) · setup-uv v9.0.0(2026-07-21) · build-push-action v7.3.0(2026-07-01) · setup-buildx-action v4.2.0(2026-07-02) 전부 실재 |
| ruff 0.17을 "존재하는 릴리스"로 쓰지 않고 미래형으로 서술했다 | ✅ **0.17.x는 실제로 존재하지 않는다**(🌐 GitHub·PyPI 양쪽 확인). 신선도 규율의 모범 사례 |
| ty/pyrefly 자기 선언 축자 | ✅ **4축자 전건 verbatim** |
| `--locked`/`--frozen` 불일치 · `npm ci` 벤더 각주 | ✅ 축자 전건 실재 (**각주 URL 2건만 오기** → ⚠️) |
| gunicorn 26.x는 미확인으로 두고 건드리지 않았다 | ✅ **`gunicorn` 등장 0회** |
| ruff formatter "stable 선언"은 확인 실패라 쓰지 않았다 | ✅ 🌐 확인 — 공식 문서에 그런 선언 **없다**(versioning.md는 *"Ruff does not yet have a stable API"*). 원고는 주장하지 않는다 |
| 리서치 원문의 *"Spring/NestJS 출신 독자가 …"* 프레이밍을 채택하지 않고 메커니즘으로 재서술했다 | ✅ **`Spring`·`NestJS` 단어 자체가 이 장에 0회.** line 150이 메커니즘 서술 |
| 계획↔계약 충돌(빌드 잡)을 `push: false`로 분할했다 | ✅ **타당.** 13장 초안이 인수를 명시하고(13장 line 212), 13장 소유 영역(레지스트리·로그인·워커 수·캐시 전략) 선점 0건 |

---

## 🚨 11↔12장 `[dependency-groups]` 정합 판정

**어긋난다. 고칠 쪽은 11장이다.**

| | 12장이 전제하는 것 | 11장의 실제 |
|---|---|---|
| 의존성 추가 명령 | `uv add --dev …`로 `dev` 그룹이 이미 생성됨 | **명령 0건** |
| `pyproject.toml` | `[dependency-groups] dev = [ # ...(11장, 생략), "ruff==0.16.*", "pyrefly>=1.1,<2" ]` | **`pyproject.toml` 등장 0회** |
| 계약 §7 교차규칙 1 | 준수 (12장이 `ruff`·`pyrefly`를 처음 쓰며 추가) | **위반** |

**판정 근거:** ① 계약 §7이 12장에 배정한 「바꾼다」는 *"`pyproject.toml`(개발 의존성·도구 설정)"*이므로 12장의 구조가 정본이다. ② 계약 §7이 11장에 배정한 「새로 만든다」는 `tests/*`이고, 교차규칙 1이 *그 장에서 처음 쓰는 장*에 의존성 추가를 의무화한다. ③ 12장 방식(`--dev` → `[dependency-groups]`)은 🌐 uv 공식 문서와 일치한다.

**정정안 (11장, 한 줄):**
```bash
uv add --dev pytest anyio "httpx2[ws]"
```
`[ws]` extra는 선택이 아니다 — 🌐 httpx2 2.9.1 `pyproject.toml`의 `ws = ["wsproto>=1.2"]`이며, 없으면 11장 line 211의 `from httpx2.websockets import ASGIWebSocketTransport`가 임포트에서 실패한다.
**12장은 손대지 않는다.**

---

## 교차 충돌 점검 (1~9장 최종본 × 10~12장)

| # | 항목 | 판정 |
|---|---|---|
| 1 | 10장 ↔ 3장 에러 계약 (`PermissionDeniedError` 재사용·새 예외 0건·핸들러 3개·`code=` 호출 형태) | ✅ |
| 2 | 10장 ↔ 4장 `deps.py` — **`get_current_user` 시그니처 문구 충돌** | **❌** (10-❌2, 정정 대상은 4장) |
| 3 | 10장 ↔ 6장 `User`·`ProjectMember`·`ProjectRole`(열거형 비교 불가 근거 포함) | ✅ |
| 4 | 10장 ↔ 2장 `repositories/` 구성 — **`UserRepository` 허위 생략 표기** | **❌** (10-❌3) |
| 5 | 11장 ↔ 6장 `db.py`·`engine`·`get_session` **재수출**(오버라이드 키 주장의 근거) | ✅ |
| 6 | 11장 ↔ 6장 「비동기 배선은 11장이 맡는다」 인계 | ✅ |
| 7 | 11장 ↔ 4장 `dependency_overrides` | ✅ |
| 8 | 11장 ↔ 7장 `InMemoryEventBus`·`queues`·`IssueEvent` 필드·WS 엔드포인트 **메커니즘** | ✅ |
| 9 | 11장 ↔ 3장 422·`request.validation_failed` | ✅ |
| 10 | 12장 ↔ 1장 uv·`pyproject.toml`·대응표(락파일 행 부재 회수) | ✅ |
| 11 | 12장 ↔ 11장 `tests/` 스위트 · **`[dependency-groups]`** | **❌** (11-❌1) |
| 12 | 12장 ↔ 13장 소유 영역(레지스트리·로그인·워커 수·캐시 전략) 선점 | ✅ 0건 |
| 13 | 각주가 앞 장 소유 표면에 중복 부착 | ✅ 0건 — [^11-4]가 8장 [^8-3]의 *"N장 각주에서 확인한"* 패턴을 정확히 따랐다 |
| 14 | 🕒 **13장 배치로 이월** — `13_draft.md` line 176 `image: tracker:latest` ↔ line 212 산문 "커밋 해시" ↔ 12장 `tracker:${{ github.sha }}` | 13장 내부 불일치, 13장 검증에서 처리 |

---

## 배치 4 종합

| 판정 | 10장 | 11장 | 12장 | 계 (장별 출현) | **고유 결함** |
|---|---|---|---|---|---|
| ❌ BLOCKING | 3 | 1 | 1 | 5 | **4** |
| 🕒 BLOCKING | 0 | 1 | 1 | 2 | **2** |
| ⚠️ 조치 필요 | 4 | 3 | 2 | **9** | 9 |
| ✅ | 42 | 52 | 47 | **141** | — |

> 📌 **❌는 고유 결함 4건이 5개 장-섹션에 걸쳐 나타난 것이다.** 11-❌1과 12-❌1은 **같은 결함**(11장에 `uv add --dev` 한 줄이 없다)의 양면이며, 11장을 고치면 12장 쪽은 함께 닫힌다. 작업 배분 시 4건으로 센다.

### Phase 5 차단 항목 (해소 전 EPUB 빌드 불가) — 고유 6건

| # | 장 | 기호 | 항목 | 정정 주체 | 해소 방법 |
|---|---|---|---|---|---|
| B1 | 10 | ❌ | 인용 축자에서 `it seems that` 삭제 → 헤지가 단정이 됨 | **10장** | 축자 복원 또는 `…` 생략 표기 |
| B2 | 10 / **4** | ❌ | `get_current_user` 시그니처 — 4장 line 104·계약 §7 교차규칙 2와 정면 충돌 | **4장 산문 + 계약 문구** (10장 불변) | *"이름과 반환 타입은 바뀌지 않는다"*로 축소 |
| B3 | 10 | ❌ | `UserRepository`의 `# ...(2장, 생략)` 허위 귀속 | **10장** | `__init__` 2줄 명시 (계약 §3-3 확정형) |
| B4 | **11** (→12 동시 해소) | ❌ | 테스트 의존성 누락 | **11장** (12장 불변) | `uv add --dev pytest anyio "httpx2[ws]"` 한 줄 |
| B5 | 11 | 🕒 | anyio 문서가 `anyio_mode = "auto"`를 먼저 권하도록 이동 | **11장** | line 19에 시점 명기, 또는 설정 옵션 + pytest-asyncio 충돌 경고 한 문장 |
| B6 | 12 | 🕒 | Python 3.10 EOL 문장에 시점 명기 없음 (3개월 뒤 과거형이 됨) | **12장** | *"이 책을 쓰는 2026-07 기준"* 삽입 |

**🕒는 4건이 아니라 2건이다.** 초안 판정에서 🕒로 분류했던 **ruff 0.17**(12장)과 **pytest-asyncio `event_loop`**(11장)는 재검토 결과 **원고가 이미 시점을 박았거나 과거형이라 시간이 지나도 참**이므로 **✅로 확정 이관**했다 — 저자 조치가 필요 없는 항목을 차단 목록에 올리면 라벨의 구속력이 닳는다.
**⚠️ 9건 중 6건이 각주 URL·출처 페이지 정확도**이며 **축자 자체는 전건 실재**한다. Phase 5를 차단하지는 않으나 final 확정 전 처리 권고.

### 가장 위험한 3건

1. **10장 line 39 — 인용 축자의 헤지 삭제.** 유일하게 **원고 밖 사람의 말을 바꾼** 결함이다. 코드 오류는 독자가 실행하면 드러나지만 잘못된 인용은 영원히 드러나지 않고, 그 인용이 *"취약점이 지적된 라이브러리를 공식 문서가 계속 권했다"*는 이 장 최고 강도의 문장을 떠받친다. `research/community.md`도 같은 형태로 잘려 있어 **리서치 → 저술의 파이프라인 전체가 같은 오류를 통과시켰다** — 다음 배치에서도 인용 축자는 원문 재대조가 필요하다는 뜻이다.
2. **11장 `uv add --dev` 누락 (+`[ws]` extra).** 결함 하나가 두 장을 동시에 깨뜨린다 — 11장은 독자가 마지막 절 코드에서 `ImportError`로 막히고, 12장은 존재하지 않는 앞 장을 참조한다. **한 줄로 둘 다 해결되는 만큼, 놓치면 둘 다 남는다.**
3. **`get_current_user` 시그니처 모순.** 4장을 읽은 독자가 10장에서 정면으로 어긋난 코드를 만난다. 위험한 이유는 오류 자체보다 **정정 주체가 이 배치 밖(4장 final·계약)**이라는 데 있다 — 배치 안에서 닫히지 않으므로 오케스트레이터·editor 경로로 넘기지 않으면 조용히 남는다.

### 오케스트레이터 보고 사항

1. **`01_reference.md` §7-4 갱신 권고 — 2건 해소.** `mypy 2.x` breaking(2.0의 `--local-partial-types`·`--strict-bytes` 기본 활성)과 `pytest 9.x` breaking(`PytestRemovedIn9Warning` 에러화, CI 감지 비어 있지 않은 값 요구)이 1차 소스로 확인됐다. **같은 줄의 `gunicorn 26.x`는 여전히 미확인**이며 13장 소유로 남는다.
2. **`tracker_contract.md` §7 교차규칙 2 문구 조정 권고.** *"시그니처를 바꾸지 않는다"* → *"이름과 반환 타입을 바꾸지 않는다"*. 현행 문구는 실물로 구현 불가능한 제약을 규정하고 있어 10장이 지킬 수 없었다. `04_final.md` line 104도 같은 폭으로 좁힌다.
3. **`tracker_contract.md` §7 row 13 문구 조정 권고.** *"이미지 빌드·푸시 잡을 `ci.yml`에 추가"* → *"이미지 **푸시**로의 전환(`push: false` → `true` + 로그인 스텝)"*. 12·13장 초안이 이미 그렇게 합의했다.
4. **계약 §2 모듈 레이아웃에 `repositories/user.py` 부재.** `UserRepository`는 §3-3 이름 사전에 있으나 어느 장도 파일을 만들지 않는다 — 배치 3의 `schemas/attachment.py`와 **같은 유형의 계약 공백**이다. 10장 신규 항목으로 등재 권고.
5. **`research/community.md` line 584의 인용도 `it seems that`가 잘려 있다.** 리서치 산출물 쪽 정정 대상으로 표시(후속 배치·재저술이 같은 오류를 재생산하지 않도록).
6. **13장 이월 관찰:** `13_draft.md` line 176 `image: tracker:latest` ↔ line 212 산문("커밋 해시")의 내부 불일치.

**언급할 가치가 있는 반전:** 이 배치는 사전 위험도가 가장 높았다 — T2 프로바넌스 위험 구역 2개(10장 인증, 11장 testcontainers), 최대 지뢰(httpx2 3층), 날조가 가장 쉬운 영역(GitHub Actions 버전·날짜), 그리고 6장이 넘긴 미문서화 배선의 자체 조립. **그런데 외부 API 표면 추적 실패가 126개 심볼 중 0건이고, GitHub Actions 버전·날짜 8건이 전건 실재했으며, httpx2 코드 표면 9건이 배포 휠 실물과 일치했다.** 저술가 셋이 1차 소스 확인을 실제로 수행했다는 뜻이다. **결함은 전부 그 바깥에서 나왔다** — 인용 부호 안의 한 구절, 앞 장을 가리키는 생략 표기 두 개, 그리고 쓰이지 않은 `uv add` 한 줄. 배치 2·3의 교훈(*"외부 대조는 통과하고 내부 정합성에서 깨진다"*)이 세 배치 연속으로 반복됐다.

---

## 13장

**검증 대상:** `chapters/13_draft.md` (10,101자, 컨테이너와 클라우드) · **라운드 1** · 배치 5(마지막)
**대조 근거:** `01_reference.md` §5-D(컨테이너·클라우드 배포, 이 장의 최대 근거) · §2-3 · §2-4 · §5-C · §7-4 · 버전 핀 C·I · `tracker_contract.md` §2·§3-4·§8-1·§8-4 · `research/web_deploy.md` · `02_plan.md` 뉘앙스 지뢰 배정표 · `chapters/01_final.md`~`12_final.md`

### ❌ 정정 필요

**❌-13-1. `TRACKER_` 환경 변수 접두사를 6장에 귀속시켰다 — 소유 장은 2장이다.**

- **원문 (line 212):** "설정은 **6장이 정한** `TRACKER_` 환경 변수로 들어온다."
- **근거:** `tracker_contract.md` §3-4 — *"설정 클래스 (`settings.py`, **2장 확정** — 🚨 필드명을 후속 장이 바꾸지 않는다) ... **환경 변수 접두사 `TRACKER_`** (예: `TRACKER_DATABASE_URL`)"*. 실물 대조: `02_final.md` line 192(*"필드 이름과 `TRACKER_` 접두사는 이 책이 `tracker`를 위해 확정한 것이다"*) · line 202(`model_config = SettingsConfigDict(env_prefix="TRACKER_", env_file=".env")`) · line 218. **`06_final.md`에서 `TRACKER_`는 grep 0건이다** — 6장은 이 접두사를 한 번도 언급하지 않는다.
- **자기모순:** 같은 13장 line 100이 이미 *"**2장에서** 워커 수를 `Settings`에 넣지 않은 이유가 이것이다 — 이 이름에는 `TRACKER_` 접두사가 붙지 않으니"*라고 **2장에 정확히 귀속**하고 있다. 한 장 안에서 같은 이름의 소유 장이 두 번 다르게 적혔다.
- **정정안:** `설정은 6장이 정한 TRACKER_ 환경 변수로` → **`설정은 2장이 정한 TRACKER_ 환경 변수로`**. (6장이 정한 것은 `db_pool_size`·`db_max_overflow` 두 **필드**이지 접두사가 아니다. 6장을 살리고 싶다면 *"설정은 2장이 정한 `TRACKER_` 환경 변수로 들어오고, 풀 크기는 6장이 정한 두 필드가 받는다"*로 나눠 쓴다.)

**❌-13-2. Mytkowicz 논문 수치의 조건 삭제 → 14장 소재이나 13장과 무관. (14장 §❌-14-1 참조)**
*(13장에는 ❌가 위 1건뿐이다.)*

### ⚠️ 출처 없음

**⚠️-13-1. 🚨 각주 URL 규율 회귀 — 9개 각주 중 6개에 URL이 없다. 앞 12개 장의 규율과 어긋난다.**

- **실측 (전 장 대조):**

  | 장 | 각주 수 | URL 포함 | 비율 |
  |---|---|---|---|
  | 5장 | 8 | 7 | 88% |
  | 8장 | 3 | 3 | 100% |
  | 10장 | 5 | 5 | 100% |
  | 12장 | 6 | 6 | 100% |
  | 14장 | 8 | 7 | 88% |
  | **13장** | **9** | **3** | **33%** |

- **URL 없는 각주:** `13-2`(uv Docker 가이드 · `uv-docker-example` Dockerfile · Docker Hub Tags API) · `13-3`(python 이미지 README · PEP 656 · PyPI 태그 집계) · `13-5`(Uvicorn Settings · FastAPI Behind a Proxy) · `13-6`(K8s Probes · kubernetes/website 원문 · SQLAlchemy) · `13-7`(pod-lifecycle.md · HPA · Uvicorn Server Behavior) · `13-9`(Fly.io·Render·Railway)
- **저술가 자기 신고 정정:** 저술가는 *"4개(13-1·13-4·13-7·13-8)를 복원했다"*고 보고했으나 **실제로는 3개다 — `13-7`에 URL이 없다.** 자기 보고 자체가 부정확하다.
- **왜 13장에서 특히 문제인가:** 레퍼런스 §7-5가 지목한 **프로바넌스 위험 구역이 정확히 이 장의 소스들**이다(렌더링 페이지 요약 경유 오염). 그리고 저술가 스스로 `sessionAffinity`에서 **요약 모델의 값 날조를 실시간으로 적발**했다고 신고했다. 그 사고 현장인 `kubernetes/website` raw 소스를 가리키는 각주가 바로 **URL 없는 `13-6`**이다. 감사 경로가 끊긴다.
- **판정:** ⚠️ (해소 필요). **최소한 `13-2`(비루트 처방 1차 출처)와 `13-6`(sessionAffinity raw 소스)에는 URL을 복원하라.** 분량이 문제라면 각주는 「분량 게이트」의 본문 자수에 계상되는지부터 확인하고, 계상된다면 서술 축약이 아니라 각주 병합(예: `13-2`+`13-3`)으로 해결하라 — URL을 지우는 것이 아니라.

**⚠️-13-2. "FastAPI 공식 문서는 컨테이너 예시를 pip로 보여주지만" — 근거 없음, 그리고 §5-C와 긴장 관계.**

- **원문 (line 11):** "**FastAPI 공식 문서는 컨테이너 예시를 pip로 보여주지만**, Uvicorn 공식 문서에는 uv 기반 Dockerfile이 통째로 실려 있다."
- **근거 상태:** 레퍼런스는 Uvicorn Dockerfile 원문만 §5-D에 싣고 **FastAPI docker 페이지(R4)의 내용은 기술하지 않는다.** 그리고 §5-C는 반대 방향의 사실을 적어뒀다 — *"**uv가 공식 기본이 됐다** — FastAPI 0.140.0에 PR #16032 '📝 Update docs to use uv projects by default'가 포함됐고, 보안·프록시·설정 문서의 명령이 전부 `uv add`/`uv run`이다."* docker 페이지가 그 개편에서 빠졌다는 근거가 없다.
- **각주 상태:** `13-1`은 **Uvicorn** 문서만 가리킨다. FastAPI docker 페이지 URL이 없다.
- **정정안:** ① 1차 소스(https://fastapi.tiangolo.com/deployment/docker/)를 열어 확인하고 URL을 각주에 추가하거나, ② 문장을 **`Uvicorn 공식 문서에는 uv 기반 Dockerfile이 통째로 실려 있다`**로 줄여 FastAPI 측 단정을 뺀다. 후자를 권한다 — 이 문장은 논지에 필수가 아니다.

**⚠️-13-3. HPA 축소의 인과 설명이 저자 추론인데 문서 각주가 붙어 있다.**

- **원문 (line 228):** "오토스케일러가 레플리카를 줄일 때 보수적으로 구는 것**도 파드 하나가 사라질 때마다 이 사슬이 처음부터 돌기 때문이다.**[^13-7]"
- **근거 상태:** §5-D는 HPA의 **동작**만 싣는다 — `desiredReplicas = ceil[...]`, tolerance 0.1, sync 15초, downscale stabilization 5분. **"종료 사슬 때문에 보수적이다"라는 인과는 k8s 문서에 없다.** 이는 레퍼런스가 §5-D에서 명시적으로 경고한 유형이다 — *"⚠️ 'IO-bound async 앱에 CPU가 나쁜 신호'라는 문장은 k8s 문서에 없다. **저자 추론으로 표시하라.**"*
- **정정안:** 각주를 떼고 저자 추론으로 표시한다 → **"덧붙이면, 오토스케일러가 레플리카를 줄일 때 보수적으로 구는 것(축소 안정화 창이 5분이다)을 이 사슬과 나란히 놓고 보면 이해가 쉬워진다 — 파드 하나가 사라질 때마다 이 절차가 처음부터 돈다. 문서가 그 인과를 적어둔 것은 아니다."**

**⚠️-13-4. liveness `failureThreshold`를 높이라는 것이 "공식 문서가 권하는 형태"라는 귀속.**

- **원문 (line 212):** "같은 엔드포인트를 쓰되 liveness 쪽 임계를 높이라는 것이 **공식 문서가 권하는 형태다.**[^13-6]"
- **근거 상태:** §5-D가 싣는 공식 처방은 **프로브를 분리하라**는 축자 하나뿐이다(*"you can implement both a liveness and a readiness probe..."*). **"같은 엔드포인트 + 높은 임계"는 그 축자에 없다.** 기본값(`failureThreshold` 3)만 §5-D에 있다.
- **정정안:** ① `13-6`에 해당 문단 URL을 붙여 확인하거나, ② **"재시작은 되돌릴 수 없으니 liveness 쪽 임계를 더 높게 뒀다 — 이 장의 판단이다"**로 저자 설계로 내린다. 이미 line 153에 `📐 저자 설계` 마커가 있으므로 ②가 자연스럽다.

**⚠️-13-5. `main.py`에 health 라우터를 등록하는 줄이 어디에도 없다.**

- **상태:** 13장이 `src/tracker/api/health.py`를 새로 만들고 *"1장에서 `main.py`에 달았던 `/healthz`가 여기로 옮겨왔다"*(line 149)고 서술하지만, **`app.include_router(...)` 호출이 본문 어디에도 나오지 않는다.** 계약 §2 「파일별 첫 등장」은 `main.py`의 13장 변경을 *"13(health 라우터 이동)"*으로 명시한다.
- **왜 걸리는가:** 매니페스트의 두 프로브가 `/healthz`·`/ready`를 때린다. 라우터가 등록되지 않으면 두 프로브가 전부 404다 — **이 장의 코드가 이 장의 매니페스트를 성립시키지 못한다.**
- **판정:** ⚠️ (내부 정합성 공백). ❌로 올리지 않는 이유는 산문이 "옮겨왔다"고 명시해 독자가 이동을 알 수 있기 때문이다.
- **정정안:** health.py 코드 블록 뒤에 두 줄을 덧붙인다 — `# src/tracker/main.py` / `from tracker.api import health` / `app.include_router(health.router)`. 2장이 이미 확립한 라우터 등록 관용구를 그대로 쓰면 된다.

### 🕒 신선도 경고

**🕒-13-1. "공식 `python` 이미지의 기본 배포판이 trixie 세대로 옮겨갔다" — 레퍼런스가 스스로 "추론"으로 신고한 항목을 단정으로 서술.**

- **원문 (line 21):** "예시는 `python:3.12-slim`으로 태그를 박아뒀는데, **공식 `python` 이미지의 기본 배포판은 그사이 Debian trixie 세대로 옮겨갔다.**"
- **근거 상태:** 버전 핀 §I — *"**공식 `python` Docker 이미지:** 기본 배포판이 **Debian trixie**로 이동했다. `3.14.6-trixie`·`3.13.14-trixie`가 2026-07-21~22 갱신. **⚠️ 다만 '트릭시가 기본'은 태그 갱신 시각의 일치에서 추론한 것이지 다이제스트 대조로 확인하지 않았다.**"*
- **판정:** 🕒. 다행히 draft가 바로 다음 문장에서 근거(태그 갱신 시각 일치)를 제시하므로 독자가 추론임을 짐작할 수는 있다. 그러나 명시가 낫다.
- **정정안:** 문장 끝에 한 구절 — **"…옮겨갔다(태그 갱신 시각의 일치에서 읽은 것이고, 다이제스트를 대조한 것은 아니다)."**

**🕒-13-2. `3.13-slim-trixie`·`3.13-slim` 동시 갱신 날짜 `2026-07-16` — 레퍼런스 스냅샷과 어긋난다.**

- **원문 (line 21):** "`3.13-slim-trixie`와 `3.13-slim`이 **2026-07-16 같은 시각에** 갱신됐고"
- **대조:** 버전 핀 §I는 `3.14.6-trixie`·`3.13.14-trixie`를 **2026-07-21~22 갱신**으로, 「신선도 원장」은 Docker Hub Tags API 스냅샷을 **2026-07-22 갱신**으로 적는다. 「A. Python 인터프리터」의 `3.15.0b4`·`3.15-rc`도 2026-07-22다. **레퍼런스 안에 2026-07-16 Docker Hub 갱신은 없다**(그 날짜는 §I의 Docker Engine 29.6.2 릴리스일과 opentelemetry 1.44.0 릴리스일에 나온다).
- **가능성:** 부동 태그(`3.13-slim`)와 패치 고정 태그(`3.13.14-trixie`)의 갱신 시각이 실제로 다를 수는 있다. 그러나 각주 `13-2`에 URL이 없어 재현이 불가능하다.
- **정정안:** ⚠️-13-1과 함께 처리 — `13-2`에 Docker Hub Tags API 조회 URL(`https://hub.docker.com/v2/repositories/library/python/tags?page_size=100`)을 붙이거나, 날짜를 빼고 **"`3.13-slim-trixie`와 `3.13-slim`이 2026-07 기준 같은 시각에 갱신됐고"**로 완화한다.

**🕒-13-3. PEP 656 "Final, 2021-03-17" — 레퍼런스는 연도만 갖고 있다.**

- **원문 (각주 13-3):** "PEP 656 (Final, **2021-03-17**)"
- **대조:** §5-D는 *"**PEP 656(musllinux)은 2021년 Final**"*까지만 적는다. 일자는 레퍼런스에 없다. 본문(line 74)은 *"2021년 Final이 됐다"*로 연도만 쓰므로 **본문은 안전하고 각주만 앞선다.**
- **정정안:** 각주에 URL(`https://peps.python.org/pep-0656/`)을 붙이거나 일자를 빼고 "(Final, 2021)"로 맞춘다.

**🕒-13-4. `(사실 확인 필요)` 마커 1건 — uvicorn `--timeout-graceful-shutdown` 기본값. → 🕒로 해소, 단 마커 문자열은 반드시 제거.**

- **원문 (line 226):** "한 가지는 확인하지 못했다. **uvicorn `--timeout-graceful-shutdown`의 기본값이 문서에 표기돼 있지 않다.** **(사실 확인 필요)** 부등식의 오른쪽을 모르면 왼쪽을 정할 수 없으니, 이 값은 비워두지 말고 명시적으로 주자."
- **판정 근거:** 이 항목은 **계약 §8-4의 승인된 T3**이고(*"uvicorn `--timeout-graceful-shutdown` **기본값** | 13"*), 레퍼런스 §1-3의 uvicorn 플래그 표가 그 칸을 *"⚠️ **문서에 Default 표기 없음**"*으로 명시한다. 즉 **draft가 문서에 대해 주장하는 내용 자체는 ✅로 정확하다.** 미상인 것은 값이지 서술이 아니다.
- **판정:** **🕒 신선도 경고로 해소.** 값을 지어내지 않고 명시적 지정을 권한 처리는 규율에 맞다.
- **🚨 필수 조치:** **본문의 `(사실 확인 필요)` 문자열 자체를 삭제하라.** 판정이 🕒로 끝났어도 마커가 원고에 남으면 Phase 4.5 수락 게이트의 「금지 마커 스캔」에 걸려 Phase 5로 갈 수 없다. 판정과 마커 제거는 별개 작업이다.
- **정정안:** `(사실 확인 필요)` 삭제 후 → **"uvicorn `--timeout-graceful-shutdown`의 기본값은 문서에 표기돼 있지 않다(0.51.0 / 2026-07 기준 확인). 부등식의 오른쪽을 모르면 왼쪽을 정할 수 없으니, 이 값은 비워두지 말고 명시적으로 주자."**

### ✅ 확인됨

**공식 문서 축자 — 전건 레퍼런스 대조 통과 (웹 2차 불필요)**

| # | 원문 축자 | 근거 |
|---|---|---|
| 1 | "The key strategy is to install dependencies first, then copy the project files." (line 13) | §5-D 축자 동일 |
| 2 | "it does use musl libc instead of glibc and friends, so software will often run into issues" (line 70) | §5-D alpine 문단 축자 동일 |
| 3 | "when running on Kubernetes you will probably not want to use workers and instead run a single Uvicorn process per container" (line 84) | §2-4·§5-D 축자 동일 |
| 4 | "some options such as `--limit-concurrency` are not yet supported when running with Gunicorn" (line 96) | §5-D 축자 동일 |
| 5 | "let your orchestration system manage the number of deployed containers" (line 100) | §5-D 축자 동일 |
| 6 | "Only trust clients you can actually trust! Incorrectly trusting other clients can lead to malicious actors spoofing their apparent client address" (line 112) | §5-D 축자 동일 |
| 7 | "The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available." (line 120) | §5-D 축자 동일 |
| 8 | "At the same time as the kubelet is starting graceful shutdown of the Pod, the control plane evaluates whether to remove that shutting-down Pod from EndpointSlice objects" (line 220) | §5-D 축자 동일 |
| 9 | "For each concurrent request, Lambda provisions a separate instance of your execution environment." / "this execution environment is busy and cannot process other requests." (line 236) | §5-D 축자 동일 |
| 10 | `Concurrency = (average requests per second) * (average request duration in seconds)` (line 239) | §5-D 공식 식 동일 |

**수치·버전 — 전건 대조 통과**

- musllinux wheel 개수 pydantic-core **21** / uvloop **16** / httptools **14** / orjson **20**, 그리고 *"uvloop과 httptools는 manylinux와 개수가 같다"*(16/16·14/14) — §5-D 표와 **전부 일치**. (line 74)
- 프로브 기본값 `periodSeconds` 10 · `timeoutSeconds` 1 · `failureThreshold` 3 · `httpGet`은 200 이상 400 미만 성공 — §5-D 일치("200~399면 성공"). (line 151)
- `terminationGracePeriodSeconds` 기본 30초 — §5-D 축자 일치. (line 218)
- uvicorn 지원 헤더 2종(`X-Forwarded-For`·`X-Forwarded-Proto`) · `--proxy-headers` 기본 활성 · `--forwarded-allow-ips` 기본 `127.0.0.1` · FastAPI 프록시 문서 예시가 `"*"` — §5-D 4항 전부 일치. (line 108~110)
- `--workers`가 `$WEB_CONCURRENCY`를 기본값으로 읽음 — §1-3 uvicorn 플래그 표 일치. (line 100)
- Cloud Run: `PORT` 주입 · `0.0.0.0` 바인딩 · 기본 8080 · **SIGTERM 후 10초 SIGKILL** · 인스턴스당 기본 "80 times the number of vCPUs" · 최대 1,000 — §5-D 전건 일치. (line 239·245)
- Lambda Web Adapter **v1.0.1 / 2026-05** — 버전 핀 §I(v1.0.1, 2026-05-28) 일치. Mangum "**유지보수 모드**" 판정 — §5-D의 판정 문장(*"'죽었다'도 '활발'도 아님"*)과 동일. (line 247)
- Fly.io `internal_port` 기본 **8080** · Render `PORT` 기본 **10000** · Railway 공식 FastAPI 가이드가 **Hypercorn** · **uvicorn은 HTTP/1.1만 지원** — §5-D PaaS 표·「대안 서버」 전건 일치. (line 249)
- gunicorn **26.0.0 / 2026-05** — 버전 핀 §C(26.0.0, 2026-05-05) 일치. (line 251)
- Granian 2.7.9 / 2026-07 · Hypercorn 0.18.0 / 2025-11 (각주 13-9) — 버전 핀 §C 일치.

**🚨 §7-4 미확인 구역의 처리 — 전건 규율 준수 (특히 잘한 부분)**

| 항목 | draft의 처리 | 판정 |
|---|---|---|
| PaaS(Fly.io·Railway·Render) 계약 | "**나머지 계약은 확인하지 못했으니 단정하지 않는다**" (line 249) | ✅ §7-4 준수 |
| Azure Container Apps / Bicep (T2 프로바넌스 위험 구역) | **본문에서 전면 배제.** `Azure`·`Bicep` grep **0건** | ✅ 계약 §8-3 준수 |
| gunicorn 26.x breaking change | "**그 변경 내역을 이 책은 확인하지 못했다.** 그 경로를 택한다면 CHANGELOG를 직접 펴보자" (line 251) | ✅ §C·§8-4 준수 |
| lifespan 워커별 실행 | "4장에서 밝혔듯 확인하지 못했다" (line 251) — `04_final.md` line 262가 실제로 그렇게 적었다 | ✅ 교차 일치 |
| 시크릿/컨피그맵 필드명 | 매니페스트에서 **`env:` 블록 제거**, 산문 처리 | ✅ 계약 §9-(A) *"재확인이 안 되면 코드를 빼고 산문으로"* 준수 |

**🎯 뉘앙스 지뢰 — 「프로세스 매니저 공식 문서 불일치」(13장 담당) 판정: ✅ 통과**

계획 배정표의 요구는 *"두 공식 문서가 다르다는 사실 자체를 쓴다"*이고, draft는 그것을 3층으로 정확히 이행했다.

1. **사실 층 (line 82~90):** FastAPI 배포 문서의 K8s 축자 ✅(§2-4) · *"이 문서에는 gunicorn이라는 단어가 **아예 나오지 않는다**"* ✅(§2-4 축자 *"gunicorn 언급이 아예 없다"*) · Uvicorn 문서의 `gunicorn -k uvicorn.workers.UvicornWorker` 시작 ✅(§2-4·§5-D) · 같은 페이지 하단의 `uvicorn-worker` 폐기 경고 ✅(§5-D, `warnings.warn` 소스 축자까지 확보) · `--limit-concurrency` 미지원 ✅(§5-D 축자)
2. **판정 유보 층 (line 92):** *"어느 쪽이 옳은지 여기서 판정하지는 않겠다. 판정보다 중요한 것은 이 불일치가 존재한다는 사실 자체다"* — 배정표 요구와 **정확히 일치**
3. **저자 기준 층 (line 100):** `— 여기서부터는 **저자 기준**이다`로 명시 표기 후 컨테이너당 1프로세스 채택. 근거를 *"어느 문서가 옳은가"*가 아니라 **축자로 검증된 `--limit-concurrency` 미지원 = 5장 backpressure 상실**에 둔 것이 정확하다. §5-D 7항(*"컨테이너에서는 워커 1개 + 오케스트레이터 레플리카가 공식 권장. 단 Uvicorn 문서는 여전히 gunicorn으로 시작한다는 점을 알려라"*)와도 일치.

**비컨테이너 서술 ✅:** *"가상 머신 한 대라면 ... `fastapi run --workers 4 main.py` 쪽이 맞다"*(line 100) — §2-4가 싣는 명령 그대로다. `uv run uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4`(line 82)도 §2-4 축자 그대로.

**🚨 코드·매니페스트 표면 대조 — 외부 추적**

*Dockerfile (line 27~58) — 식별자 18개*

| 표면 | 추적 | 근거 |
|---|---|---|
| `COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/` | ✅ | §5-D 공식 Dockerfile 원문과 **문자열 동일** |
| `RUN --mount=type=cache,target=/root/.cache/uv` / `--mount=type=bind,source=uv.lock,target=uv.lock` / `--mount=type=bind,source=pyproject.toml,target=pyproject.toml` | ✅ | §5-D 원문과 **문자열 동일** |
| `uv sync --locked --no-install-project` / `uv sync --locked` | ✅ | §5-C(`--locked` 의미 축자, *"uv 자신의 Docker 가이드는 `--locked`"*) · 계약 §8-1 |
| `groupadd --system --gid 999 nonroot` · `USER nonroot` | ✅ | §5-D(*"비루트 1차 출처는 uv 문서가 링크하는 예제 저장소에 있다"*) · 계약 §8-1 |
| `WORKDIR /app` · `COPY . /app` · `FROM ... AS builder` · `CMD [...]` | ✅ | Dockerfile 표준 지시어 + §5-D |
| `ENV UV_COMPILE_BYTECODE=1` · `UV_LINK_MODE=copy` · `UV_NO_DEV=1` | ⚠️ | **레퍼런스 어디에도 없다.** 계약 §8-1의 컨테이너 행은 "Uvicorn 공식 Dockerfile 전문"까지만 포함한다. 각주 `13-2`가 uv Docker 가이드를 근거로 대지만 **URL이 없다** → ⚠️-13-1에 병합 |
| `useradd --system --gid 999 --uid 999 --create-home nonroot` | ⚠️ | §5-D는 `groupadd`+`USER`만 싣는다. `useradd` 줄은 레퍼런스 밖 → ⚠️-13-1에 병합 |
| `ENV PATH="/app/.venv/bin:$PATH"` · `ENV PYTHONUNBUFFERED=1` | ⚠️ | 동상 (각주 13-2가 "비루트 사용자와 `PATH`"를 주장하나 URL 부재) |

*health.py (line 128~147) — 식별자 8개, 전건 ✅*

- `from fastapi import APIRouter` ✅ 계약 §8-1 · `APIRouter(tags=[...])` ✅ §1-2 파라미터 목록
- `from tracker.deps import SessionDep` ✅ — `04_final.md` line 93이 `SessionDep = Annotated[AsyncSession, Depends(get_session)]`으로 실제 정의. 계약 §3-4 별칭표 일치
- `await session.execute(text("SELECT 1"))` ✅ — `AsyncSession.execute` 계약 §8-1
- `from sqlalchemy import text` — **6장에 선례 없음**(`06_final.md`에서 `text` grep 0건). 즉 13장이 이 심볼의 소유 장이다. 각주 `13-6`이 SQLAlchemy 2.0 공식 문서를 근거로 대므로 절차는 맞으나 **URL 부재** → ⚠️-13-1에 병합. (참고: §1-6이 `pool_pre_ping` 설명에서 *"'ping' (typically 'SELECT 1')"*을 인용하므로 질의문 자체는 근거가 있다.)
- `async def healthz() -> dict[str, str]` ✅ — `01_final.md` line 161~162와 **시그니처·반환 타입까지 동일**. 계약 부록 #1(*"1장부터 `/healthz`. 13장은 `/ready`를 추가하고 `/healthz`를 `api/health.py`로 이동만 한다(경로 불변)"*) 정확히 이행

*deployment.yaml · service.yaml (line 155~210) — 필드 15종*

- 계약 §8-1이 명시적으로 추적한 것: `periodSeconds` · `timeoutSeconds` · `failureThreshold` · `httpGet` · `terminationGracePeriodSeconds` · `preStop` — **✅ 전건**
- `apiVersion: apps/v1` / `kind: Deployment` / `spec.selector.matchLabels` / `spec.template.metadata.labels` / `containerPort` / `lifecycle.preStop.exec.command` / Service `spec.ports[].port`·`targetPort`·`protocol: TCP` — 계약 §8-1의 *"K8s 매니페스트 골격"*·§8-2 필수 예외 경로. 각주 `13-6`이 kubernetes/website `examples/` YAML 4종을 근거로 댄다. **(웹 2차 확인 결과는 아래 「웹 2차 확인」 절)**
- **⚠️ `status.HTTP_422_*` 패턴 점검:** 13·14장 **0건** ✅
- **코드 주석 전수 검사:** Dockerfile의 `# Dockerfile`, health.py의 `# src/tracker/api/health.py`, 매니페스트의 `# k8s/deployment.yaml`·`# k8s/service.yaml`. **전부 계약 §6-2의 파일 경로 표시이고, 동작을 설명하는 주석은 0건** ✅ (계약 §9-(B)-4 「주석 금지선」 준수 — 날조 사례 1의 유형이 재현되지 않았다)

**🚨 포트 8080 사슬 — 5개 지점 전건 일치 ✅**

`CMD [... "--port", "8080"]`(line 57) → `containerPort: 8080`(line 178) → `livenessProbe.httpGet.port: 8080`(line 182) → `readinessProbe.httpGet.port: 8080`(line 188) → `Service.targetPort: 8080`(line 209). Service의 `port: 80`은 외부 노출 포트로 **의도적으로 다른 값**이며 이는 정상이다. Cloud Run 기본 포트 8080(§5-D)과도 맞아 line 245의 *"앞의 Dockerfile이 그대로 붙는다"*가 성립한다.

**🚨 경로 이름 사슬 ✅**

`/healthz`(1장 확정 → 13장 이동, 경로 불변) · `/ready`(13장 신규) → 매니페스트 두 프로브의 `path`와 **문자 단위 일치**. 계약 부록 #1 이행.

**🚨 Dockerfile `COPY` 대상의 실재 ✅**

`uv.lock`·`pyproject.toml` 모두 **1장에서 생성된다** — `01_final.md` line 148: *"첫 줄이 `pyproject.toml`의 의존성 목록과 `uv.lock`을 갱신한다."* 계약 §2 「파일별 첫 등장」도 두 파일의 첫 등장을 1장으로 못 박는다. `CMD`의 모듈 경로 `tracker.main:app`도 1장 line 148과 동일 문자열 ✅.

### 🧮 산술 검산

**① 커넥션 180 — ✅ 정확**

- 13장 (line 102): 풀 5+10 = 프로세스당 **15**, 레플리카 **12** → 15 × 12 = **180** ✅
- 근거: §1-6 커넥션 풀 표(`pool_size` **5** / `max_overflow` **10**) + *"기본 최대 동시 커넥션 = 5+10 = 15이고 이게 워커 수와 곱해진다"* ✅
- 6장 실물 대조: `06_final.md` line 398~399가 `pool_size` 5 / `max_overflow` 10을, line 416~417이 `db_pool_size: int = 5` / `db_max_overflow: int = 10`을 **기본값 그대로** 쓴다. 6장이 다른 수를 핀하지 않았으므로 15가 유효 ✅
- **교차 검산:** `06_final.md` line 410은 같은 180을 **워커 4 × 레플리카 3 = 12 프로세스**로 계산했다. 13장은 **컨테이너당 1프로세스 × 레플리카 12**로 계산한다. **두 경로 모두 프로세스 12개 → 15×12=180으로 수렴한다.** 6장의 예고를 13장이 자기 결론(1컨테이너 1프로세스)에 맞춰 다시 푼 것이며 모순이 아니다 ✅
- **관찰(정정 아님):** 매니페스트의 `replicas`는 **3**이고 line 102의 12는 가정치다. 장 마무리(line 255)가 *"서비스 하나에 파드 셋"*으로 매니페스트 값에 착지하므로 독자가 혼동할 위험은 낮다.

**② 종료 유예 부등식 — ✅ 관계 성립, 우변 1항만 미상(🕒-13-4로 처리)**

- 주장 (line 224): **`terminationGracePeriodSeconds` > `preStop` 대기 + uvicorn `--timeout-graceful-shutdown`**
- 매니페스트 실측: `terminationGracePeriodSeconds: 60` (line 173) / `preStop`의 `sleep 5` (line 194) → **60 > 5 + X**, 즉 X < 55초면 성립
- 근거: §5-D 매핑(*"`terminationGracePeriodSeconds`(기본 30초) **>** uvicorn `--timeout-graceful-shutdown`이어야 SIGKILL 전에 정리가 끝난다"*) ✅ — draft는 여기에 `preStop` 항을 더해 정확도를 **높였다**
- 사슬 서술(line 224)도 정확: preStop 대기 → uvicorn이 SIGTERM 수신 후 남은 응답·백그라운드 태스크 처리(§1-5 *"wait for any background tasks to run to completion"*) → lifespan `yield` 이후 정리. 세 단계 전부 근거 있음 ✅
- **8장 예고 회수 ✅:** `08_final.md` line 21이 *"백그라운드 태스크의 최악 실행 시간보다 종료 유예 시간이 길어야 한다. 그 숫자를 정하는 일은 배포를 이야기할 자리의 몫이다"*로 넘겼고, 13장이 60초로 받았다. 8장 line 267의 **12초짜리 리포트**는 60초 창 안에 들어온다 ✅. 13장 line 224의 *"주간 리포트가 그 창에 못 들어온다면 ... 8장 말대로 그 일을 요청 수명 밖으로 내보낼 문제다"*도 `08_final.md` line 37(*"배포 설정에 따라 살기도 하고 죽기도 하는 기능은 이미 설계가 잘못된 것이다"*)과 일치 ✅
- **30초 → 60초 변경 근거 ✅:** k8s 기본 30초로는 12초 리포트 + preStop 5초 + 여유가 빠듯하다는 판단이며, `📐 저자 설계` 마커(line 153)로 표시돼 있다

**③ 5장 회수 산술 ✅**

*"프로세스 하나에 동기 작업용 스레드 40개"*(line 102) — §1-3 체인 4단(FastAPI `routing.py` → Starlette `run_in_threadpool` → anyio `CapacityLimiter(40)` → anyio 문서 축자) 전부 확보 ✅. `05_final.md` line 3·line 166과 일치. *"5장에서 문 앞의 손잡이라고 불렀던 그 플래그"*(line 98)도 `05_final.md` line 180(*"문 앞에서 손님을 돌려보내는 손잡이는 `--limit-concurrency` 하나다"*)과 **표현까지 일치** ✅

### 🔗 교차 충돌 점검 (1~12장 × 13장)

| 앞 장의 예고 | 13장의 회수 | 판정 |
|---|---|---|
| **5장** line 220: *"이 장에서 내린 `def`/`async def` 판단은 **13장에서 한 번 뒤집힌다**"* | line 232: *"여기서 **5장의 결론이 한 번 뒤집힌다**" → Lambda 실행 환경당 1요청* | ✅ 정확히 회수 (§4-1·§5-D) |
| **5장** line 170: *"워커를 몇 개 띄울 것인가는 ... 13장의 소재다"* | §「컨테이너 하나에 프로세스를 몇 개」 전체 | ✅ |
| **6장** line 410·483: 워커×레플리카×(5+10) 산수 | line 102: 15 × 12 = 180 | ✅ (위 산술 검산 ①) |
| **7장** line 3·78·84: 워커가 둘이면 알림 절반 / line 369: 팬아웃은 워커 4×레플리카 3에도 버틴다 | line 104: 두 길(sessionAffinity vs 팬아웃) 제시 후 **"7장에서 이미 만든 팬아웃"**을 채택 | ✅ — 7장이 **이미 해결한** 문제임을 지우지 않고 배포 층의 대안과 나란히 놓았다 |
| **7장** line 231: *"클라이언트 주소나 프로토콜이 뒤바뀌는 문제는 별개이고 13장의 소재다"* | §「프록시 뒤에서 잃어버리는 주소」 | ✅ |
| **8장** line 21·37·65: 종료 유예 / CronJob | line 224 부등식 · line 65 CronJob 언급 회수 | ✅ (위 산술 검산 ②) |
| **12장** line 166·179·185: `push: false`, `tags: tracker:${{ github.sha }}`, *"밀어 넣을 곳이 정해지면 **로그인 스텝이 붙고 `push: false`가 뒤집힐 뿐**"* | line 212: *"12장의 잡이 **커밋 해시로 붙인 태그**가 여기 들어온다 — 그 잡의 **`push: false`가 뒤집히고 로그인 스텝이 붙는 것**이 12장에 되돌려주는 변경이다"* | ✅ **문구 단위로 정확히 인수** |
| **12장** line 36: *"13장에서 읽을 Uvicorn 공식 Dockerfile은 `--frozen`을 쓴다"* | line 62: *"`--locked`는 12장의 결정을 그대로 이었다 — 공식 Uvicorn Dockerfile은 `--frozen`을 쓰지만 uv 자신의 예제와 가이드는 `--locked`다"* | ✅ (§5-C 축자 일치) |
| **2장** line 224: *"워커 수는 `Settings`에 들어가지 않는다 ... 이 이야기는 13장에서 프로세스 모델과 함께 다시 꺼낸다"* | line 100: `$WEB_CONCURRENCY`에 `TRACKER_` 접두사가 안 붙는 이유 | ✅ (계약 §3-4 각주와 일치) |
| **1장** line 170: *"13장에서 ... 이 경로를 그대로 쓰고 `/ready`를 곁에 추가한다"* / line 61: `root_path` | line 124·149(경로 불변) · line 114(*"1장에서 본 `root_path`가 앞단 경로와 어긋나지 않는지도 함께 확인하자"*) | ✅ |
| **4장** line 262: lifespan 워커별 실행 미확인 | line 251에서 재확인 | ✅ |

**🚨 배치 4 이월 결함 재판정 — `tracker:latest` vs "커밋 해시"**

- **배치 4의 보고:** *"line 176의 `tracker:latest`와 line 212 산문의 '커밋 해시'가 불일치한다."*
- **재판정: ✅ 불일치 아님 — 배치 4의 판정을 뒤집는다.**
- **이유:** line 212가 그 둘의 관계를 **명시적으로 설명한다** — *"`image`의 **`latest`는 임시 이름이고**, 12장의 잡이 커밋 해시로 붙인 태그가 **여기 들어온다**."* 즉 매니페스트의 `latest`는 자리표시자이고 산문이 그 사실을 밝힌 뒤 실제 값의 출처를 지정한다. 코드와 산문이 어긋난 것이 아니라 **산문이 코드의 임시성을 선언한 것**이다.
- **12장 실물 대조:** `12_final.md` line 180이 `tags: tracker:${{ github.sha }}` — 커밋 해시 태그가 실재한다 ✅. line 185가 *"밀어 넣을 곳이 정해지면 로그인 스텝이 붙고 `push: false`가 뒤집힐 뿐"*으로 13장에 인계를 예고했고 13장이 그대로 받았다 ✅.
- **잔여 관찰(정정 아님):** 프로덕션 매니페스트에 `latest`를 싣는 것은 관행상 권장되지 않지만, 이 책이 그 사실을 line 212에서 스스로 짚고 대체 경로를 지정하므로 사실 오류가 아니다. 편집 판단이 필요하다면 `editor` 소관이다.

**양화사·금지선 스윕 (13장)**

- `reddit` / `stack overflow` / `스택오버플로` / `14603` / `Azure` / `Bicep` — **전부 0건** ✅
- `유일한` / `처음으로` / `항상` / `모든 ` — **0건** ✅
- `전부` 2건: line 92(*"예제들이 전부 낡은 것도 아니라는 뜻"* — 부정 한정, 안전) · line 224(*"이 전부가 `terminationGracePeriodSeconds` 안에"* — 열거 지시, 안전) ✅
- `반드시` 1건: line 68(*"베이스를 고를 때 반드시 나오는 말"* — 수사, 안전) ✅
- `아예` 1건: line 86(*"gunicorn이라는 단어가 아예 나오지 않는다"*) — **레퍼런스 §2-4 축자(*"gunicorn 언급이 아예 없다"*)로 뒷받침되는 전칭이므로 통과** ✅
- **출신 귀속 점검:** 저자 판단·추론 지점이 전부 명시 표기됐다 — line 100 *"여기서부터는 **저자 기준**이다"* · line 241 *"여기서부터는 **저자 추론**이다. 벤더가 이렇게 말한 게 아니라 위 사실에서 내가 끌어낸 결론이다"* · `📐 저자 설계` 마커 3회(line 25·126·153). §5-D의 *"반드시 '추론'으로 표시할 것"* 요구를 정확히 이행 ✅

---

## 14장

**검증 대상:** `chapters/14_draft.md` (8,191자, 관측성·성능·살아가기 — **책의 마지막 장**) · **라운드 1** · 배치 5(마지막)
**대조 근거:** `01_reference.md` §2-1·§2-2 · §3-1·§3-2 · §4-6 · §5-B · §6-4 · §7-2·§7-3 · 버전 핀 F·H · 「신선도 원장」 · `tracker_contract.md` §3-4·§8-2 · `chapters/01_final.md`~`13_draft.md`

### ❌ 정정 필요

**❌-14-1. 🚨 Mytkowicz 논문의 33% / 300%는 합성 마이크로커널의 수치인데, 조건을 지운 채 옮겼다 — 같은 장이 두 절 앞에서 금지한 바로 그 행위다.**

- **원문 (line 139):** "Mytkowicz 등의 「Producing Wrong Data Without Doing Anything Obviously Wrong!」(ASPLOS 2009)은 프로그램 로직과 무관한 두 가지만 건드린다. 쓰이지도 않는 환경 변수의 총 바이트 수, 그리고 링크 순서. **그것만으로 성능이 흔히 약 33% 움직였고 한 번은 거의 300%였다.**"
- **원문 확인 결과 (논문 PDF 직접 판독):**
  - §2 축자: *"changing the size (in bytes) of an unused environment variable, can dramatically (**frequently by about 33% and once by almost 300%**) change the performance of **our program**."*
  - **"our program"은 Figure 1(a)의 합성 마이크로커널**(65536회 루프, 각주 1에 따라 최적화를 끈 상태)이다. SPEC 벤치마크가 아니다.
  - **논문이 SPEC에 대해 보고하는 편향 폭은 훨씬 작다:** 링크 순서 §4.1.1 *"on average 2% for Core 2 and 8% for Pentium 4"* / 환경 변수 크기 §4.2.1 *"on average 1% for Core 2 and 4% for Pentium 4"*
  - **두 번째 오류:** 33%/300%는 **환경 변수 크기 단독**의 결과다. draft는 *"그것만으로"*로 **두 요인 모두**에 귀속시켰다.
- **왜 ❌인가:** 이 장 line 127이 *"**조건을 지우고 숫자만 옮기는 쪽은 문서가 아니라 인용하는 우리다**"*라고 적고, line 133이 *"**조건이 적히지 않은 숫자는 자기 상황으로 옮길 수도, 반박할 수도 없다**"*로 못 박은 뒤, **바로 다음 절에서 같은 일을 한다.** 이 책의 셀링 포인트가 정면으로 무너지는 자리다.
- **정정안:**
  > "…쓰이지도 않는 환경 변수의 총 바이트 수, 그리고 링크 순서. **환경 변수 크기만 바꿔도 논문의 예제 프로그램에서는 성능이 흔히 33%, 한 번은 거의 300% 움직였다. 실제 벤치마크(SPEC)에서의 편향 폭은 그보다 훨씬 작다 — 링크 순서가 평균 2%(Core 2)·8%(Pentium 4), 환경 변수 크기가 평균 1%·4%다. 편향의 크기가 아니라 편향이 존재한다는 사실이 요점이다.**"
- **참고 (교차 오염 주의):** 논문 §3이 인용하는 *"in a survey of 49 highly-cited medical articles, later work contradicted 16% of the articles"*(Ioannidis)는 **관련 연구 인용이지 이 논문의 결과가 아니다.** Georges 논문의 16%(아래)와 숫자가 같아 섞이기 쉽다. draft는 이 함정을 밟지 않았다 ✅

### ⚠️ 출처 없음

**⚠️-14-1. Georges 논문 — "가장 흔한 보고 방식"이라는 최상급이 원문보다 강하다.**

- **원문 (line 141):** "16편은 방법론을 적지 않았고, **가장 흔한 보고 방식**은 여러 번 돌려서 가장 좋았던 실행 하나를 싣는 것이었다."
- **원문 확인 결과 (논문 PDF 직접 판독, §2.1.1):** *"The most popular approaches are **average and best — 8 and 10 papers** out of the 50 papers in our survey, respectively; median, second best and worst are less frequent, namely 4, 4 and 3 papers, respectively."*
  - 논문은 **average와 best를 묶어** "most popular"라 부르고, best 단독을 *the* 관행으로 지목하지 않는다.
  - 그리고 **가장 큰 집단은 방법론을 아예 밝히지 않은 16편**이다(10편 > 8편이지만 16편 > 10편). "가장 흔한"이 사실과 어긋난다.
  - 부수 정밀도: 논문의 "best of N"은 **N번의 VM 기동 중 최선**(§5)이지 "한 VM 안에서 여러 번 돌린 것 중 최선"이 아니다.
- **정정안:**
  > "…**50편 중 16편은 방법론을 아예 적지 않았고, 밝힌 논문 중에서는 '가장 좋았던 실행 하나'를 싣는 방식이 10편으로 가장 많았다(평균값은 8편).**"
- **덧붙임 ✅:** *"자바 성능 논문 **50편**의 방법론을 조사했다"* / *"**16편**은 방법론을 적지 않았고"* — 두 수치는 **원문 확인 완료** (§2: *"we examined the methodology used in **50 papers**"* / *"about one third of the papers (**16 out of the 50 papers**) does not specify the methodology"*)

**⚠️-14-2. Georges 논문 — "뒤집히는 비율이 3%를 넘었다"에서 원문의 한정어가 탈락했다.**

- **원문 (line 141):** "그렇게 얻은 결론이 **오도되는 비율이 최대 16%**, **뒤집히는 비율이 3%를 넘었다.**"
- **원문 확인 결과 (§5):**
  - 16% ✅ — *"the total fraction misleading comparisons ranges **up to 16%**"* (draft의 "최대"가 "up to"를 정확히 보존)
  - 3% ⚠️ — *"**For some** prevalent methodologies, the fraction of incorrect comparisons **can be more than 3%**."* draft는 "일부 방법론에서는"과 "…일 수 있다"를 **둘 다 떨어뜨리고 단정**했다.
  - 두 수치 모두 **Figure 4의 정상 상태 GC 전략 비교**(θ=1%·2% 임계, AMD Athlon 포함)에 한정된 값이며 전반적 비율이 아니다.
- **정정안:** "…**오도되는 비율이 최대 16%, 일부 방법론에서는 결론이 뒤집히는 비율도 3%를 넘었다.**"

**❌-14-2 (당초 ⚠️-14-3에서 승격). `Depends(scope=)`를 "오래 묵은 고통에 대해 API가 움직인" 사례로 든 것 — 4장이 활자로 독자에게 한 약속을 마지막 장이 뒤집는다.**

> **승격 사유:** 처음 ⚠️(출처 없음)로 기재했으나 재검토 결과 ❌가 맞다. ⚠️는 *"출처를 보강하라"*는 뜻인데 **여기에는 보강할 출처가 없다** — 레퍼런스 §3-3이 *"릴리스 노트로 확인하기 전에는 미확정"*으로 못 박았고, 필요한 조치는 출처 보강이 아니라 **주장 철회**다. 게다가 이것은 단순 미검증 주장이 아니라 **4장이 인쇄된 문장으로 하지 않겠다고 약속한 바로 그 반올림**이다. 하네스 v1.9.1 규칙상 사실 ❌ 판정은 저술가 재량으로 덮을 수 없으므로 **BLOCKING**으로 취급한다.

- **원문 (line 163):** "**좋은 쪽도 같은 표에 있다.** 별도 라이브러리로 메워오던 SSE가 코어로 들어왔고, **4장에서 본 의존성 정리 순서처럼 오래 묵은 고통에 대해 API가 움직이기도 한다.**"
- **충돌:** `04_final.md` line 142 — *"**#11143이 어떤 사유로 닫혔는지, 어떤 PR이 병합됐는지를 이 책은 확인하지 못했다.** 그래서 '`scope`가 #11107을 해결했다'고는 쓰지 않겠다. 성립할 가능성이 높다고 보지만 릴리스 노트로 확인하기 전까지는 미확정이고, **이렇게 반올림하는 습관이 기술서를 못 믿게 만든다**."*
- **레퍼런스:** §3-3 🚨 *"'`scope` 파라미터가 #11107을 해결했다'로 **반올림하지 마라.** 성립할 가능성은 높지만 릴리스 노트로 확인하기 전에는 미확정이다."* + 계획 뉘앙스 지뢰 배정표(*"'해결했다'로 반올림 금지"*, 담당 4·6장)
- **부수 문제:** *"같은 표에 있다"*고 했으나 `Depends(scope=)`는 **line 153~161 표의 7행 어디에도 없다.** SSE(0.135.0)는 있다 ✅.
- **왜 위험한가:** **마지막 장의 총괄이 앞 장의 명시적 유보를 덮어쓰는** 전형이다. 4장이 "반올림하지 않겠다"고 독자에게 약속한 바로 그 항목을, 14장이 반올림된 형태로 회수한다.
- **정정안:**
  > "**좋은 쪽도 같은 표에 있다.** 별도 라이브러리로 메워오던 SSE가 코어로 들어왔다(0.135.0). **표 밖에서는 4장에서 본 `Depends(scope=)`가 그런 종류의 움직임이다 — 다만 그것이 오래된 이슈를 해결한 것인지는 4장에서 밝힌 대로 확인하지 못했다.**"

**⚠️-14-4. 각주 `14-7`에 URL이 없다 — 이 장에서 가장 검증이 어려운 항목(학술 인용 3편 + arXiv ID + upvote)을 한 각주가 URL 없이 떠받친다.**

- **상태:** 14장 각주 8개 중 URL이 없는 것은 `14-7` 하나다(다른 7개는 전부 URL 보유 ✅). 그런데 그 하나가 **논문 3편의 수치·축자 전부 + arXiv ID + coordinated omission 지위 + Little(1961) + USL + #9148 upvote**를 묶어 지탱한다.
- **정정안:** 최소한 세 DOI를 각주에 명기하라 — 레퍼런스 §6-4가 이미 갖고 있다: Mytkowicz `10.1145/1508244.1508275` · Georges `10.1145/1297027.1297033` · van der Kouwe `10.1109/EUROSP.2019.00031`. DOI는 URL보다 짧으므로 분량 부담도 없다.

### 🕒 신선도 경고

**🕒-14-1. 2장의 "3주" 기준점이 미세하게 다르다 (경미).**

- 14장 line 163: *"고쳐진 뒤 3주 만에 또 깨지는 일이 있었다(2장)"* / `02_final.md` line 259: *"첫 보고가 릴리스와 같은 날이고, 열하루 뒤에 또, **첫 보고로부터 3주가 지나** 다시 한 번이다"*
- 레퍼런스 §3-2 저자 해석은 **"고쳐도 3주 뒤 또 깨진다"**로 14장 쪽 표현을 쓴다. #370이 보고 당일 PR #371로 수정됐으므로 두 기준점이 같은 날(2026-06-14)에 겹쳐 실질 차이가 없다.
- **판정:** 🕒 (통과). 정정 불필요하나, editor가 통권 정합을 볼 때 두 표현 중 하나로 통일하면 더 깔끔하다.

**🕒-14-2. `app_name` 필드가 14장에서 소비되지 않는다 (계약 대비 경미한 어긋남).**

- 계약 §3-4는 `app_name`의 「쓰는 장」을 **2·14**로 적는다. 14장 코드가 실제로 쓰는 필드는 `log_level`·`otel_service_name`·`otel_exporter_endpoint` 셋이고 `app_name`은 등장하지 않는다.
- **판정:** 🕒 (사실 오류 아님 — 계약 표의 예상이 빗나간 것이지 원고가 틀린 것이 아니다). `otel_service_name`을 따로 둔 설계(line 101: *"이름과 주소를 `Settings`의 두 필드로 모아 세 신호가 서로 다른 서비스 이름을 갖는 일을 막았다"*)가 오히려 합리적이다. 오케스트레이터·editor에 **계약 표 갱신 대상**으로만 보고한다.

### ✅ 확인됨

**🎯 T-8 라벨 회피 — ✅ 완전 통과 (이 장에서 가장 잘 처리된 항목)**

- **`상반기` grep: 14장 0건** ✅ (절 제목·본문·표 전부)
- **표의 창 정의 (line 151):** *"창을 넓혀 **2025년 12월부터 2026년 7월까지**를 한 표에 놓으면"* — 표의 실제 범위(2025-12-17 ~ 2026-07-24)와 **정확히 일치** ✅
- **1장 지칭 (line 151):** *"1장은 **2026년 2월부터 6월까지의 세 건**으로 이 책을 열었다"* — `01_final.md` line 5가 *"**2026년 2월부터 6월까지**, FastAPI는 ... 생태계를 세 번 흔들었다"*로 **문구 단위 일치** ✅. 세 건도 0.129.0(2026-02-12)·0.132.0(2026-02-23)·0.137.0(2026-06-14)으로 1장 line 73~75 표와 동일 ✅
- **계획 제약 이행:** 계획 line 198이 *"`pydantic.v1` 완전 제거(0.128.0)는 2025-12-27이라 '지난 6개월' 창에 들어오지 않는다 — 이 창에 넣지 마라"*고 못 박았다. 14장은 **1장의 창(2026-02~06)을 건드리지 않고 별도의 더 넓은 창(2025-12~2026-07)을 새로 선언**한 뒤 그 안에 0.128.0을 넣었다. **정확히 요구된 처리** ✅

**🧮 "일곱 달 남짓" 산술 — ✅ 정확**

2025-12-17 → 2026-07-24 = **7개월 7일**. "일곱 달 남짓"은 정확한 표현이다 ✅ (여덟 달로 넘어가지 않고, 일곱 달을 조금 넘는다)

**🧮 표 부속 서술 산술 — ✅ 전건 정확 (line 163)**

- *"인터프리터 지원선이 **두 번** 올라갔고"* → 0.125.0(Python 3.8 중단) + 0.129.0(Python 3.9 중단) = **2회** ✅
- *"호환 계층 하나가 사라졌고"* → 0.128.0 `pydantic.v1` 완전 제거 = **1건** ✅
- *"기본 동작이 엄격해졌다"* → 0.132.0 `strict_content_type` 기본 True = **1건** ✅

**릴리스 표 7행 — §3-1 대조 전건 일치 ✅**

| draft 행 | §3-1 |
|---|---|
| 0.125.0 / 2025-12-17 / Python 3.8 지원 중단 | ✅ 동일 |
| 0.128.0 / 2025-12-27 / `pydantic.v1` 지원 완전 제거 | ✅ 동일 |
| 0.129.0 / 2026-02-12 / Python 3.9 지원 중단 | ✅ 동일 |
| 0.132.0 / 2026-02-23 / `strict_content_type` 기본 True | ✅ 동일 |
| 0.135.0 / 2026-03-01 / SSE 정식 지원 | ✅ 동일 |
| 0.137.0 / 2026-06-14 / 라우터 내부 구조를 트리로 변경 | ✅ 동일 |
| 0.140.0 / 2026-07-24 / 의존성 메모리 사용량 감소 | ✅ 동일 |

각주 `14-8`이 *"표의 버전·날짜는 **릴리스 노트 헤더 기준**"*이라 밝힌 것도 §버전 핀 테이블의 ⚠️ 경고(*"FastAPI는 릴리스 노트 헤더 날짜와 GitHub `published_at`이 일부 릴리스에서 불일치한다 ... 책에서 날짜를 쓸 때 기준을 통일하라"*)를 정확히 이행 ✅. 헤더/API 불일치가 알려진 0.135.**2**를 피하고 0.135.**0**을 쓴 것도 안전 ✅

**버전·지표 — 전건 대조 통과**

- OTel: `opentelemetry-api`·`opentelemetry-sdk` **1.44.0**, `opentelemetry-instrumentation-fastapi` **0.65b0**, **둘 다 2026-07-16**, **베타 표기** — 버전 핀 §F 4항 **전부 일치** ✅. §5-B 8항(*"이 대역 차이를 그대로 서술하라"*) 요구도 이행 ✅
- structlog **26.1.0** (각주 14-2) — §F 일치 ✅
- uvicorn **0.51.0 / 2026-07** (각주 14-1) — §C 일치 ✅
- Starlette **2026-03-22에 1.0.0**, 현재 **1.3.1**, FastAPI **0.140.0** — §B 일치 ✅. *"성숙도 표기가 뒤집혀 있다"* — §B의 ▶저자 해석과 동일 프레이밍 ✅
- 저장소 지표 **스타 100,866 / 열린 이슈 87 / MIT / 2026-07-25 기준** — §4-6 마지막 줄과 **숫자 단위 일치** ✅
- FastAPI Cloud 발표 **2025-05-05** + 각주의 X URL — §4-6 및 「신선도 원장」 일치 ✅
- 대안 3종: **Litestar 2.24.0(2026-06)** / **Django Ninja 1.6.2(2026-03)** / **Flask 3.1.3(2026-02)** — 버전 핀 §H(2026-06-11 / 2026-03-18 / 2026-02-19)와 버전·연월 **전건 일치** ✅
- **#9148 upvote 18** (line 121) — §7-2·§6-5·「신선도 원장」이 *"upvote 18 — 1차 회차의 56은 **오류**"*로 못 박은 **정정된 수치를 정확히 사용** ✅ (레퍼런스 §0이 이 사건을 신뢰도 규약의 창설 사례로 든다)

**van der Kouwe 논문 — 레퍼런스 대조로 전건 확인 ✅ (웹 불필요)**

- *"반복되는 결함을 **22가지**로 정리"* ✅ §6-4 (*"22가지 결함"*)
- *"최상위 학회 논문 **50편**에서 한 편이 **평균 다섯 가지**를 저지르며"* ✅ §6-4 (*"최상위 학회 논문 50편 중 평균 5건 위반"*)
- *"**결함이 없는 것은 한 편**이었다"* ✅ §6-4 (*"무결점은 단 1편"*)
- *"널리 인용되는 'benchmarking crimes'는 같은 연구의 **비심사 프리프린트 제목**이고 정본은 'flaws'로 순화했다"* ✅ §6-4 (*"⭐ **동료 심사 정본이다.** 널리 인용되는 'Benchmarking Crimes' 프리프린트와 **판본이 다르다**(용어 crimes→flaws, 저자 순서 상이)"*)
- 학회 표기 "IEEE EuroS&P 2019" ✅ §6-4

**🚨 성능 근거 비대칭 전략 — ✅ 모범적 처리**

- **0건 목록 통째 공개 (line 137):** *"이 책이 뒤진 학술 문헌 가운데 FastAPI 자체의 성능을 다룬 동료 심사 논문은 나오지 않았다. ASGI도, Pydantic의 직렬화도, asyncio의 실증 연구도 마찬가지다. 웹 프레임워크 벤치마크의 방법론을 검토한 논문도 없었고, free-threading이 처리량을 얼마나 바꾸는지도 5장에서 이월된 채 비어 있다."*
  - §2-2 표와 **항목 단위 일치** — FastAPI 자체 **없음 ❌** / Python asyncio 실증 **없음 ❌** / 웹 프레임워크 벤치마크 자체 **없음 ❌** / ASGI·GIL·Pydantic 성능 **없음 ❌** ✅
  - free-threading 벤치마크 미확보 ✅ §1-3·§7-4 ✅, 5장 이월 ✅ `05_final.md` line 214
  - **§2-2의 전략 칸("정직하게 밝히기")을 문자 그대로 이행** ✅
- **TechEmpower 처리 ✅:** *"이 책은 FastAPI가 링크한 실행이 어느 라운드의 언제 측정인지 확인하지 못했다. 그래서 **순위도 배수도 옮기지 않는다**"*(line 133) — §2-1의 *"⚠️ ... **URL만 인용하고 라운드·날짜는 쓰지 마라**"* 정확 이행 ✅. 각주 `14-6`도 *"⚠️ 라운드·시점은 확인하지 못했다"*를 명기 ✅
- **단정 명시적 부인 ✅:** *"마찬가지로 **TechEmpower가 이 결함들을 저질렀다고 말하려는 것이 아니다.** 이 렌즈를 끼면 숫자를 만났을 때 던질 질문이 생긴다는 것이 요점이다"*(line 145) — §2-1의 *"**'TechEmpower가 이 범죄를 저질렀다'고 단정하지 마라** ... **'이 렌즈로 보면 이런 질문을 하게 된다'**로 쓰라"*를 **거의 문장 단위로** 이행 ✅
- **coordinated omission / Little's Law / USL 지위 표기 ✅ (line 147):** *"이 개념의 원전은 **강연과 메일링 리스트 글이며 동료 심사를 거치지 않았다**"* ✅ §2-1·§6-4 / *"5장에서 쓴 Little's Law는 **학술지에 증명이 실린 정리**"* ✅ §6-4(*"Little (1961), Operations Research 게재 정리(DOI 확인됨)"*) / *"그 옆에 인용되는 USL은 **프리프린트와 저서가 원전**"* ✅ §6-4 — **세 문헌의 지위 차이를 정확히 3단으로 구분** ✅
- **0.130.0 Rust 직렬화 재인용 안 함 ✅:** 14장에 `0.130`·`ORJSONResponse`·"2배" grep **0건**. §2-3·§3-1이 갖고 있으나 1장이 이미 소비했으므로 재인용하지 않은 것은 각주 중복 회피 규율에 맞다 ✅

**🚨 리서치 공백 §7 준수 — 전건 통과**

| 금지선 | 14장 상태 |
|---|---|
| Reddit·Stack Overflow 인용 | **0건** ✅ |
| `#14603` | **0건** ✅ |
| FastAPI Cloud 상업화 백래시 | line 167: *"0.x 유지나 상업화에 대한 **찬반 여론은 근거를 확보하지 못해 옮기지 않는다**"* ✅ §4-6·§7-3 정확 이행 |
| 다수설 일반화 | line 167: *"이 책이 읽은 대안 논의는 상당수가 '**Litestar를 보라**'는 글의 댓글 스레드에서 나왔다. **떠나는 사람이 과대표집된 표본**이다"* — §4 표집 편향 경고(HN 44816755)를 **독자에게 그대로 이전** ✅ |
| Actuator 부재에 대한 커뮤니티 여론 | line 121: *"이 부재를 커뮤니티가 어떻게 느끼는지는 **근거를 못 찾았으니 여론이 아니라 구조만 대조하자**"* ✅ §7-2 정확 이행 |
| **Spring 측 설정 키·기본값·엔드포인트 경로** (계획 제약 10) | grep 결과 `Actuator` **제품명 1회**뿐. `management.*` · `/health/liveness` · `/health/readiness` · `server.shutdown` · `maxThreads` **전부 0건** ✅ — 계획이 요구한 "(b) 수치·키를 빼고 구조만 대조" 경로를 정확히 택했다 |
| 출신 귀속(*"Java 개발자라서 이렇게 한다"*) | 0건 ✅. line 123의 판단은 *"— **저자의 판단이다**"*로 명시 표기 ✅ |

**🚨 코드 표면 대조 — 외부 추적 (14장, 식별자 24개)**

*`observability.py` (line 19~57)*

| 표면 | 추적 | 근거 |
|---|---|---|
| `import logging` · `logging.basicConfig` · `getLogger` · `.handlers.clear()` · `.propagate` | ✅ | 계약 §8-0 표준 라이브러리 면제 |
| `from fastapi import FastAPI` | ✅ | §1-2 |
| `from tracker.settings import Settings` | ✅ | 계약 §3-4 (2장 도입) |
| `structlog.configure(processors=, logger_factory=)` · `contextvars.merge_contextvars` · `processors.add_log_level` · `processors.TimeStamper(fmt="iso")` · `processors.JSONRenderer()` · `stdlib.LoggerFactory()` · `get_logger().bind()` | T1 → 각주 | 계약 §8-2 *"structlog … 호출 표면 \| **소유 장 14** \| 각 공식 문서"*. 각주 `14-2`가 *"이 장이 쓴 structlog 호출 표면 **전부**와 인용 축자"*로 범위를 명시하고 URL 보유 ✅ **절차 준수** |
| `from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor` · `.instrument_app(app)` | T1 → 각주 | 동상. 각주 `14-3` URL 보유 ✅ |
| `from prometheus_client import make_asgi_app` | T1 → 각주 | 동상. 각주 `14-4` URL 보유 ✅ |
| `app.mount("/metrics", ...)` | ✅ | **각주 `14-4`가 *"`app.mount(...)`는 9장 각주에서 확인했다"*로 처리.** 실물 대조: `09_final.md` line 22가 `app.mount("/static", ...)`를 쓰고 각주 `9-1`이 *"`app.mount(...)` … 호출 형태"*를 명시적으로 커버한다 ✅ — **앞 장이 소유한 표면에 각주를 다시 달지 않고 참조로 처리한 모범 사례** |
| `settings.log_level` · `settings.otel_service_name` · `settings.otel_exporter_endpoint` | ✅ | 계약 §3-4 필드표 3행 그대로. **세 필드 전부 코드에서 실제 소비됨** ✅ |

*`middleware.py` (line 65~87) — 4장 대비 델타 검증*

- 4장 원본(`04_final.md` line 183~200) import 3줄: `from uuid import uuid4` / `from starlette.middleware.base import BaseHTTPMiddleware` / `from starlette.types import ASGIApp`
- 14장 블록: **위 3줄 전부 보존** + `from structlog.contextvars import bind_contextvars, clear_contextvars` 추가
- 클래스 본문: `__init__` 시그니처·`dispatch` 본문 **4장과 동일**, `clear_contextvars()` / `bind_contextvars(request_id=request_id)` **2줄만 삽입**
- **판정 ✅ — 임포트 유실 0건, 시그니처 변경 0건, 4장 클래스와 충돌 없음.** 산문(line 89)의 *"두 줄이 늘었다"*도 정확 ✅

*`main.py` (line 103~111)*

- `from tracker.observability import setup_observability` ✅ — `observability.py`가 같은 장에서 그 이름으로 정의 ✅
- `from tracker.settings import get_settings` ✅ 계약 §3-4 (`get_settings()` → `Settings`, 2장)
- `setup_observability(app, get_settings())` ✅ — 정의부 `def setup_observability(app: FastAPI, settings: Settings) -> None`과 **인자 수·타입 일치** ✅
- 생략 표기 `# ...(13장, 생략)` ✅ 계약 §6-3

**코드 주석 전수 검사 (14장):** 파일 경로 주석 3개(`# src/tracker/observability.py` · `# src/tracker/middleware.py` · `# src/tracker/main.py`)와 생략 표기 1개. **동작 설명 주석 0건** ✅ (계약 §9-(B)-4 준수)

**`status.HTTP_422_*` 점검:** 0건 ✅

**🚨 SDK 익스포터 조립 코드 배제 — ✅ 규율 준수**

line 101: *"익스포터와 리소스를 조립하는 SDK 코드는 싣지 않았다 — **1차 소스로 확인한 표면이 거기까지라서다.**"* — 계약 §9-(A)/§8-2 절차(*"확인이 안 되면 코드를 빼고 산문으로 설명하고, 그 사실을 해당 장의 「근거 두께」에 적는다"*)를 **본문에서 독자에게 직접 밝히는** 형태로 이행했다. 이 책의 일관된 태도와도 맞는다 ✅

**로깅 진단 — ✅ §5-B 정확 이행**

- line 15: *"흔한 설명은 '**uvicorn이 기존 로거를 비활성화해서**'인데 맞지 않는다. … 진짜 원인은 옆 줄이다. `uvicorn`과 `uvicorn.access`에 **`propagate: False`**가 걸려 있어…"* — §5-B 🔴 항목(*"**uvicorn 로거의 `propagate: False`**가 구조적 로깅과 충돌하는 **실제 원인**이다"*)과 **원인 지목이 일치** ✅
- line 59: *"'`disable_existing_loggers`를 빠뜨리면 로거가 죽는다'는 흔한 설명은 **연역**일 뿐이라 이 책은 싣지 않는다"* — §5-B ⚠️ 항목(*"… **연역한 것**이지 uvicorn이 명시한 문장이 아니다 … **책에 넣으려면 실제 재현 실험을 붙여라**"*)의 **가장 안전한 처리(미수록)를 택했다** ✅
- line 95: *"**Starlette 쪽에서 컨텍스트 전파를 보장한다고 적어둔 문서는 이 책이 찾지 못했다.**"* — §5-B(*"⚠️ **Starlette 측 공식 보장 문서는 못 찾았다** — structlog 측 경고문만 확보"*)와 **일치** ✅

**멀티프로세스 메트릭 ↔ 13장 연결 ✅**

line 117: *"위 코드의 `/metrics`는 **워커가 하나라는 전제** 위에 서 있다. 13장의 권장 — 컨테이너당 프로세스 하나, 확장은 레플리카로 — 을 따르면 이 문제가 생기지 않는다."* — §5-B 🔴(*"prometheus_client는 멀티프로세스 제약이 있다 → §5-D의 '워커 1개' 권장과 **직접 연결**된다"*)를 정확히 이행 ✅. 13장 line 100의 결론과도 일치 ✅

**2장 계측 라이브러리 사건 회수 ✅**

line 117: *"**2장에서 줄줄이 깨진 것도 메트릭 계측 라이브러리였다** — 관측 스택은 앱 바깥처럼 보이지만 업그레이드에서 먼저 다친다."*
`02_final.md` line 251~259가 `trallnag/prometheus-fastapi-instrumentator` #370(2026-06-14)·#379(2026-06-25)·#388(2026-07-08) 3건을 실제로 서술 ✅. §3-2 표와 일치 ✅. **14장이 이슈 번호·버전 번호를 다시 옮기지 않고 사실만 회수한 것도 안전하다** — §3-2의 ⚠️(*"위 버전 번호는 이슈 본문에 보고자가 적은 환경 정보다"*)를 건드리지 않는다 ✅

**🎯 1장 지도 접기 — ✅ 다섯 항목 전건 대응 확인**

line 175~177이 1장의 세 무더기를 다시 꺼내 세 번째를 독자에게 인계한다.

- **세 무더기 원본:** `01_final.md` line 7 — *"어떤 것은 저 고정된 바닥에 대응해서 **거의 그대로 옮겨오고**, 어떤 것은 흔들리는 위층에 걸려 있어서 **매년 다시 확인해야 한다**. 그리고 어떤 것은 **옮겨올 자리가 아예 없다**."*
- **14장 line 175:** *"그대로 옮겨온 것, 옮겨왔지만 매년 다시 확인해야 하는 것, 그리고 옮겨올 자리가 없는 것."* — **세 무더기 정의가 문구 단위로 일치** ✅

**세 번째 무더기 다섯 항목 실증 대조:**

| 14장 line 177의 항목 | 책 안의 근거 | 판정 |
|---|---|---|
| "의존성을 스스로 찾아 꽂아주는 컨테이너" | `04_final.md` line 45: *"**없는 것은 자동 와이어링(auto-wiring)이다.** 타입만 보고 알아서 찾아 꽂아주는 층이 없다"* · `01_final.md` line 178 · §3-8 | ✅ |
| "애너테이션 하나로 걸리던 트랜잭션 경계" | `01_final.md` line 180: *"`@Transactional`이 없는 세계에서 세션과 트랜잭션 경계를 직접 긋는다(6장)"* | ✅ |
| "필터 체인으로 조립돼 있던 보안" | `10_final.md` line 9: *"**요청 앞을 지키는 필터 사슬이 없고**, 메서드 위에 한 줄로 붙이던 권한 애너테이션이 없다"* | ✅ — 구조 서술이고 §7-2가 금지한 "Spring Security 사용자의 체감" 귀속이 아니다 |
| "의존성 하나로 따라오던 진단 엔드포인트" | 14장 §「Actuator가 없다는 말의 정확한 크기」 자체 | ✅ |
| "표준 문제 상세 형식의 **코어 지원**" | `03_final.md` line 184: *"**FastAPI 코어에 RFC 9457 지원은 없다.** '지원한다'도 틀리고 '거절됐다'도 틀린다. 7년째 열려 있는 요청"* · §3-4 🚨 | ✅ — **"코어 지원"이라는 정확한 한정어를 보존**했다. "거절됐다"로 반올림하지 않았다 |

**line 177의 마무리도 정확:** *"**못 찾은 게 아니라 지금 이 도구에 없는 것**이고, 없다는 사실을 아는 편이 있다고 착각하는 것보다 안전하다."* — RFC 9457의 "7년째 열려 있는 요청"이라는 3장 결론과 상충하지 않는다(현재 부재는 사실) ✅

**🎯 0.x 판단 착지 — ✅ 저자 판단으로 정확히 표시**

- **1장의 유보:** `01_final.md` line 110 — *"버전 번호는 코드의 안정성이라기보다 프로젝트가 스스로에게 부여한 **호환성 약속의 등급**에 가깝고 … **판단은 여기서 내리지 않겠다.** 재료를 책 전체에 걸쳐 모아두고 **14장에서 정면으로 다시 꺼낸다.**"*
- **14장의 착지 (line 165·169):** *"그러면 **1장에서 미뤄둔 질문을 꺼내자.**"* → *"**이제 판단이다.** 버전 번호가 낮다는 것은 코드가 미숙하다는 뜻이 아니라 **호환성 약속의 등급이 낮다는 뜻이다.** **1장에서 그렇게 적었고** 위 표가 뒷받침한다."*
- **다수설 회피 ✅ (핵심):** line 167이 판단 **직전에** *"**0.x 유지나 상업화에 대한 찬반 여론은 근거를 확보하지 못해 옮기지 않는다**"*를 명시한다. §4-6(*"⚠️ **0.x 버전대 유지에 대한 커뮤니티 의견도 근거를 못 찾았다**"*)·§7-3의 요구를 정확히 이행하고, 이어지는 판단이 여론이 아니라 **저자 판단**임을 독자가 알 수 있게 배치했다 ✅
- **대비 사실만 제시 ✅:** Starlette 1.x vs FastAPI 0.x 역전(§B ▶저자 해석), 스타/이슈/라이선스(§4-6), 대안 3종 버전(§H) — **전부 검증된 사실이고 해석은 분리** ✅

**양화사·금지선 스윕 (14장)**

- `상반기` / `reddit` / `stack overflow` / `14603` — **전부 0건** ✅
- `유일한` / `처음으로` / `항상` / `모든 ` / `반드시` — **0건** ✅
- `전부` 2건: line 137(*"아래 문헌은 **전부 옆 분야의 것**"* — 자기 문헌 목록에 대한 정확한 한정, 안전) · line 183(각주의 *"structlog 호출 표면 전부"* — 각주 범위 선언, 안전) ✅
- **마지막 장 총괄 특유의 위험 — 전칭 남용 0건.** 총괄 문장들이 전부 조건부·경험 이전형이다(line 179: *"이 장에서 얻은 것은 어떤 프레임워크가 얼마나 빠른가가 아니라 … 묻는 **습관**이다"*) ✅
- **예외 1건은 ❌-14-2로 별도 처리** (앞 장의 유보를 덮어쓰는 총괄 — BLOCKING)

**`(사실 확인 필요)` 마커: 14장 0건** ✅

</content>
</invoke>

## 🌐 웹 2차 확인 (배치 5) — Critical 항목만, 12건

> **비용 통제 원칙 적용:** 레퍼런스 1차 대조로 판정 가능한 것(FastAPI K8s 축자·gunicorn 부재 주장·`--limit-concurrency` 축자·musllinux wheel 개수·#9148 upvote·OTel 버전·van der Kouwe 수치·prometheus 멀티프로세스 사실)은 **웹을 쓰지 않고 §5-D·§F·§6-4로 종결**했다. 웹은 (1) 레퍼런스가 판정할 수 없는 Critical 주장, (2) **의심 식별자**, (3) **프로바넌스 사고 현장**에만 썼다.

### W-1. 🚨 `sessionAffinity` 기본값 — **저술가가 신고한 프로바넌스 사고의 최종 값 검증: ✅ 정확**

- **사고 경위 (저술가 자기 신고):** 렌더링 페이지로 fetch했을 때 요약 모델이 *"truncated"*를 인정하면서도 *"based on standard Kubernetes documentation"*이라며 값을 **지어냈다**. 폐기하고 `kubernetes/website` **raw markdown**으로 재확인했다고 한다.
- **검증:** `https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/reference/networking/virtual-ips.md` (HTTP 200, 38,635 bytes) line 400~403 **원문 축자**:
  > "If you want to make sure that connections from a particular client are passed to the same Pod each time, you can select the session affinity based on the client's IP addresses by setting `.spec.sessionAffinity` to `ClientIP` for a Service (**the default is `None`**)."
- **draft (line 104):** *"쿠버네티스 서비스에는 `.spec.sessionAffinity`를 `ClientIP`로 두는 설정이 있고 **기본값은 `None`이다**"*
- **판정: ✅ raw 소스와 문자 단위로 일치.** 허용 값도 `ClientIP`/`None` 둘뿐임을 API 타입 정의(`staging/src/k8s.io/api/core/v1/types.go`, *"Must be ClientIP or None. Defaults to None."*)로 교차 확인했다.
- **📌 이 결과의 의미:** §7-5가 경고한 실패 유형(하위 요약 모델의 값 날조)이 **실시간으로 재현됐고, 저술가가 자체 적발해 raw 소스로 교정했으며, 그 교정 결과가 정확했다.** 하네스의 프로바넌스 규율이 실제로 작동한 사례다. **책의 신뢰성 관점에서 이 배치의 가장 중요한 확인이다.**

### W-2. K8s 매니페스트 필드명 — **15종 전건 실재·철자·중첩 정확 ✅**

`staging/src/k8s.io/api/core/v1/types.go` 원문 대조 결과, **오탈자 0건 · 존재하지 않는 필드 0건 · 잘못된 중첩 0건.**

| 필드 | 검증 |
|---|---|
| `spec.template.spec.terminationGracePeriodSeconds` | ✅ `DeploymentSpec.Template`(`json:"template"`) → `PodTemplateSpec.Spec`(`json:"spec"`) → `PodSpec.TerminationGracePeriodSeconds`. 중첩 경로 정확 |
| `livenessProbe.httpGet.path` / `.port` | ✅ `Container.LivenessProbe` → `Probe`(embeds `ProbeHandler`) → `HTTPGet *HTTPGetAction` → `Path`/`Port` |
| `periodSeconds` · `timeoutSeconds` · `failureThreshold` | ✅ `Probe` 구조체 필드. 기본값도 일치 — *"Default to 10 seconds"* / *"Defaults to 1 second"* / *"Defaults to 3"* |
| `lifecycle.preStop.exec.command` | ✅ `Container.Lifecycle` → `Lifecycle.PreStop *LifecycleHandler` → `Exec *ExecAction` → `Command []string`. **배열-문자열 형태 정확** |
| `spec.containers[].ports[].containerPort` | ✅ `PodSpec.Containers` → `Container.Ports []ContainerPort` → `ContainerPort` (required) |
| Service `spec.ports[].port` · `targetPort` · `protocol: TCP` | ✅ `ServiceSpec.Ports []ServicePort` → `Port`(required) / `TargetPort`(`intstr.IntOrString`) / `Protocol`(`+default="TCP"`) |
| `httpGet` 성공 판정 200 이상 400 미만 | ✅ `configure-liveness-readiness-startup-probes.md` line 127~128 축자: *"Any code greater than or equal to 200 and less than 400 indicates success."* |
| `terminationGracePeriodSeconds` 기본 30초 | ✅ `pod-lifecycle.md` line 920 축자: *"The default `terminationGracePeriodSeconds` setting is 30 seconds."* |

**🎯 특기할 정확성 — `preStop` 명령 형태:** K8s `ExecAction`은 *"is simply exec'd, **it is not run inside a shell**, so traditional shell instructions ('|', etc) won't work"*이다. draft는 `command: ["/bin/sh", "-c", "sleep 5"]`로 **셸을 명시적으로 호출**한다 — `["sleep 5"]` 같은 흔한 오답을 피했다 ✅. 이 영역은 과제 명세가 *"지어내기 가장 쉬운 영역"*으로 지목한 곳인데 **한 건도 어긋나지 않았다.**

### W-3. 🕒 프로브 기본값의 각주 출처가 정밀하지 않다 (신규 지적)

- **각주 `13-6`:** *"Kubernetes 공식 문서 **Probes** — 분리 축자·**기본값** · kubernetes/website 저장소의 `examples/` YAML 4종과 `virtual-ips.md` 원문"*
- **검증 결과:** `pod-lifecycle.md`에는 `periodSeconds`·`failureThreshold`·`timeoutSeconds` grep **0건**이다. `configure-liveness-readiness-startup-probes.md`에도 `timeoutSeconds` 기본값 언급은 **gRPC 프로브 예외 설명 안(line 238)**에 한 번 나올 뿐이고, `periodSeconds` 10 / `failureThreshold` 3의 근거는 **API 레퍼런스(`Probe` 타입)**에 있다.
- **판정:** 🕒 (수치는 전부 정확하고 §5-D도 같은 값을 갖는다. 출처 지시만 부정확하다.)
- **정정안:** `13-6`에 API 레퍼런스를 추가 — `https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#Probe`. ⚠️-13-1(URL 복원)과 함께 처리하면 한 번에 해소된다.

### W-4. 각주 URL 3종 실재 확인 — **전건 ✅, 주장 내용까지 일치**

| 각주 | URL | 검증 |
|---|---|---|
| `13-1` | `github.com/Kludex/uvicorn/blob/main/docs/deployment/docker.md` | ✅ HTTP 200. uv 기반 Dockerfile 실재 · *"The key strategy is to install dependencies first, then copy the project files."* 축자 일치 · **`!!! warning "For production, create a non-root user!"` 실재하고 같은 파일의 Dockerfile 블록(line 87~109)에 `USER` 지시어가 실제로 없다** ✅ · *"let your orchestration system manage the number of deployed containers"* 축자 일치 |
| `13-4` | `fastapi.tiangolo.com/deployment/server-workers/` | ✅ HTTP 200. K8s 축자 일치 |
| `13-4` | `uvicorn.dev/deployment/` | ✅ HTTP 200. 아래 W-5 참조 |
| `13-8` | `docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html` | ✅ HTTP 200. 두 축자 + 동시성 식 **전부 원문 일치** |

**draft line 19의 아이러니는 실재한다** — 같은 문서가 비루트 사용자를 경고해두고 예시 Dockerfile에는 `USER`가 없다 ✅.

### W-5. 🎯 "gunicorn이라는 단어가 아예 나오지 않는다" — **강한 확인 ✅**

- **draft (line 86):** *"이 문서에는 gunicorn이라는 단어가 **아예 나오지 않는다.**"*
- **검증:** `deployment/server-workers.md` **raw markdown 0건**, 그리고 렌더링된 **111KB HTML 전문(내비게이션·사이드바·푸터·메타데이터 포함) 대소문자 무시 0건.** 대조군으로 "uvicorn"은 같은 HTML에 20회 등장한다.
- **판정: ✅** 전칭 주장이지만 **전수 검색으로 뒷받침된다.** §2-4의 서술과도 일치.

### W-6. Uvicorn 배포 문서 오프닝 축자 — **✅ 문자 단위 일치**

`raw.githubusercontent.com/Kludex/uvicorn/main/docs/deployment/index.md` line 1~8 원문:
> As a general rule, you probably want to:
> * Run `uvicorn --reload` from the command line for local development.
> * **Run `gunicorn -k uvicorn.workers.UvicornWorker` for production.**
> * Additionally run behind Nginx for self-hosted deployments.
> * Finally, run everything behind a CDN for caching support, and serious DDOS protection.

draft line 88의 인용(`"As a general rule, you probably want to: ... Run gunicorn -k uvicorn.workers.UvicornWorker for production."`)과 **생략 표기까지 정확** ✅

같은 파일 line 85~93의 폐기 경고(*"The `uvicorn.workers` module is deprecated and will be removed in a future release. You should use the `uvicorn-worker` package instead."*)와 line 106의 `--limit-concurrency` 축자(*"some options such as `--limit-concurrency` are not yet supported when running with Gunicorn."*)도 **전부 실재** ✅

**📌 draft가 이미 정확히 짚은 것:** 이 페이지는 **상단에서 권하고 하단에서 폐기 경고를 한다.** draft line 90이 *"같은 페이지 아래쪽에는 `uvicorn.workers`가 폐기 예정이니 별도 패키지 `uvicorn-worker`를 쓰라는 경고가 있다"*로 **같은 페이지 안의 자기모순임을 명시**했다 ✅. 뉘앙스 지뢰 처리의 핵심 요소이며 정확하다.

### W-7. 🕒 gunicorn 26.0.0 CHANGELOG — **접근 실패의 원인이 404가 아니라 경로 오류였다 (신규 지적)**

- **draft (line 251):** *"gunicorn은 26.0.0 / 2026-05 기준으로 메이저가 크게 뛰었는데 **그 변경 내역을 이 책은 확인하지 못했다.** 그 경로를 택한다면 **CHANGELOG를 직접 펴보자.**"*
- **저술가 자기 신고:** *"CHANGELOG raw가 404라 단정하지 않았다."*
- **검증 결과:**
  - 버전·날짜 ✅ — PyPI `info.version` = **26.0.0**, upload_time **2026-05-05T06:38:23Z**. 버전 핀 §C와 일치.
  - **404의 원인:** `docs/source/news.rst`는 실제로 404다. 그러나 저장소가 Sphinx/reST → Markdown으로 이전하면서 **파일이 `docs/content/2026-news.md`로 옮겨간 것**이다(HTTP 200, 19,128 bytes). PyPI `project_urls.Changelog`도 `https://gunicorn.org/news/`를 가리킨다. **즉 CHANGELOG는 접근 가능하다.**
  - **26.0.0 항목 실재** — 헤더 `## 26.0.0 - 2026-05-05`(PyPI 업로드일과 일치), `### Breaking Changes` 절에 **eventlet 워커 제거**(*"Migrate to `gevent`, `gthread`, or `tornado`"*)가 명시돼 있다.
  - 부가 사실: 26.0.0은 **ASGI 프레임워크 호환성 스위트**(Starlette/FastAPI/Litestar/Quart/Sanic/BlackSheep 대상 438/444 통과)를 도입했다.
- **판정: 🕒.** draft의 문장 자체는 **거짓이 아니다**(저술 시점에 확인하지 못한 것은 사실이고, §C도 미확인으로 신고한다). 그러나 *"확인하지 못했다"*의 근거가 **잘못된 URL에서 나온 404**였다.
- **정정안 (둘 중 택일):**
  1. **권장** — 확인해서 싣는다: *"gunicorn은 26.0.0 / 2026-05 기준으로 메이저가 크게 뛰었고, 그 릴리스에는 eventlet 워커 제거라는 파괴적 변경이 들어 있다. 그 경로를 택한다면 릴리스 노트를 직접 펴보자(https://gunicorn.org/news/)."*
  2. **최소 조치** — 미확인 서술을 유지하되 **독자가 실제로 열 수 있는 URL을 준다**: *"…확인하지 못했다. 그 경로를 택한다면 릴리스 노트(https://gunicorn.org/news/)를 직접 펴보자."* 현재 문장은 *"CHANGELOG를 직접 펴보자"*라고만 해서, 저자가 못 찾은 문서를 독자에게 찾으라고 넘기는 모양이 된다.
- ⚠️ **주의(과잉 정정 방지):** 26.0.0의 네이티브 ASGI 지원이 13장의 gunicorn 서술을 무효화하지는 **않는다.** 이 장은 *"gunicorn은 WSGI 전용"*이라고 쓴 적이 없고, 논거는 오직 **`--limit-concurrency` 미지원**(uvicorn 문서 축자로 확인됨)이기 때문이다. 서술 골격은 그대로 유효하다.

### W-8. 🚨 의심 식별자 — `arXiv:1801.02381` **✅ 실재 확인 (자동 ❌ 규칙 비해당)**

- **원문 (각주 14-7):** *"'benchmarking crimes'는 비심사 프리프린트(**arXiv:1801.02381**) 제목"*
- **의심 사유:** 레퍼런스 §6-4는 프리프린트의 **존재와 비심사 지위**만 갖고 있고 **arXiv ID는 갖고 있지 않다.** 즉 저술가가 외부에서 들여온 식별자다 → 역할 규정상 **구속력 있는 웹 검증 대상.**
- **자동 ❌ 규칙 점검:** YYMM = **1801 = 2018년 1월** → 빌드 시점(2026-07-26) 기준 **과거**. 미래 날짜 arXiv ID가 아니므로 자동 ❌ 비해당.
- **검증 (2경로):** `https://arxiv.org/abs/1801.02381` + arXiv API(`export.arxiv.org/api/query?id_list=1801.02381`)
  - Title: **"Benchmarking Crimes: An Emerging Threat in Systems Security"** ✅
  - Authors: **Erik van der Kouwe, Dennis Andriesse, Herbert Bos, Cristiano Giuffrida, Gernot Heiser** ✅
  - Submitted: **2018-01-08** (v1, 개정 없음) ✅ — EuroS&P 2019 정본보다 앞선다는 draft의 「프리프린트 → 정본」 서사와 시간순 일치
- **판정: ✅ 확인됨.** ID가 정확히 기대한 논문에 매핑된다. **날조 신호 없음.**
- **📌 규율 메모:** 이 항목은 "한 곳에만 나오는 인용이니 통과"로 넘기지 않고 **구속력 있는 웹 검증으로 에스컬레이션**해 종결했다. 결과가 ✅였으므로 BLOCK은 발생하지 않는다.

### W-9. Mytkowicz / Georges 논문 수치 — **논문 PDF 직접 판독 (결과는 ❌-14-1 · ⚠️-14-1 · ⚠️-14-2)**

- **소스:** Mytkowicz — 저자 그룹 페이지(USI/Hauswirth)의 ACM 서지(ASPLOS '09, pp. 265–276, DOI `10.1145/1508244.1508275`)와 대조해 프로바넌스를 닫은 PDF. Georges — **공저자 Dries Buytaert 본인 사이트**의 카메라레디 PDF(ACM 저작권 블록 보유, OOPSLA'07). ACM DL은 HTTP 403으로 직접 사용 불가.
- **확인된 것 ✅:** Mytkowicz의 두 교란 요인(미사용 환경 변수 바이트 수 + 링크 순서) · *"think we have a 7% slowdown when in fact we have a 8% speedup!"* **축자 완전 일치**(논문도 "a 8%"로 적는다) · **133편** 조사 · Georges의 **50편**·**16편** 미기재 · *"up to 16%"* · 관리형 런타임 타 언어 적용 진술
- **어긋난 것:** 33%/300%의 **측정 대상**(합성 마이크로커널 ≠ SPEC)과 **귀속 요인**(환경 변수 단독 ≠ 두 요인) → **❌-14-1** / "가장 흔한 보고 방식" 최상급 → **⚠️-14-1** / "3%를 넘었다"의 한정어 탈락 → **⚠️-14-2**

### W-10. TechEmpower 축자·방법론 — **✅ 확인, 페이지 지시만 정밀화 권고**

위키를 git으로 클론해 raw markdown을 grep한 결과:

- **핵심 축자 ✅ (`Project-Information-Expected-Questions.md` 항목 24):** *"…nothing beats conducting performance tests yourself for the specific workload of your application."* — draft line 131과 **완전 일치**
- **(a) 로깅 ✅ (항목 9):** *"Although this is **not consistent with production deployments**, we avoid a few complications related to logging…"* — draft의 축자 인용 정확.
  - 🕒 **미세 정밀화:** 규칙은 *"must disable all **disk** logging"*이고 콘솔 로깅은 *"recommend but do not require"*다. draft의 *"로그를 끈 채로 잰다"*는 살짝 넓다. 정정안: **"디스크 로그를 끈 채로 잰다"** (한 단어 추가로 해소)
- **(b) 리버스 프록시 ✅ (항목 14):** *"We are expressly **not using reverse proxies** on this project."* — draft 정확
- **(c) 15초 ✅:** 위키에 15초가 **두 번** 나온다 — 15초 **웜업(미기록)** + 15초 **기록 측정.** draft는 *"**측정 구간이** 15초"*라고 써서 **기록 구간을 정확히 지목**했다 ✅
- **(d) `Wrk` ✅ (항목 19):** *"we now use Wrk for this project"* — draft 정확
- 🕒 **각주 `14-6` 권고:** 현재 위키 루트(`.../wiki`)만 가리킨다. 위 축자·조건이 전부 `Project-Information-Expected-Questions` 한 페이지에 있으므로 그 페이지로 좁히면 독자가 재현할 수 있다.

### W-11. ⚠️ FastAPI 문서 축자 4종 — **전건 실재 ✅, 그러나 각주 인용 하나가 절단됐다 (신규 지적)**

`raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/index.md` line 45~54 원문 대조:

| draft 인용 | 원문 | 판정 |
|---|---|---|
| *"on par with NodeJS and Go"* | L45 `Very high performance, on par with **NodeJS** and **Go**` | ✅ |
| *"about 200% to 300%"* | L46 `Increase the speed to develop features by about 200% to 300%. *` | ✅ |
| *"about 40%"* | L47 `Reduce about 40% of human (developer) induced errors. *` | ✅ |
| *"estimation based on tests conducted by an internal development team"* | L54 `* estimation based on tests conducted by an internal development team, **building production applications.**` | ⚠️ **절단** |

- **🎯 특기할 정확성:** draft line 127은 *"**뒤의 두 줄에** 별표가 달렸고"*라고 쓴다. 원문에서 별표(`*`)는 **L46·L47에만** 붙고 L45("on par with NodeJS and Go")에는 붙지 않는다. **draft가 별표의 적용 범위를 정확히 구분했다** ✅ — 이 문서를 인용하는 글 대부분이 틀리는 지점이다.
- **⚠️-14-5 (신규):** 각주 인용이 `, building production applications.`를 **말줄임 없이 잘랐다.** 배치 4에서 지적된 인용 절단(`it seems that` 탈락)과 같은 유형이다.
- **정정안:** 전문으로 복원 → *"estimation based on tests conducted by an internal development team, building production applications"*. (뒷부분이 오히려 논지를 강화한다 — "프로덕션 앱을 만들면서 잰 자체 추정"이라는 조건이 더 선명해진다.)

### W-12. 관측성 3종 라이브러리 표면 — **전건 ✅ 1차 소스 확인**

| 표면 | 검증 |
|---|---|
| uvicorn `LOGGING_CONFIG` | ✅ `uvicorn/config.py` 원문: `"disable_existing_loggers": False` · `"uvicorn": {..., "propagate": False}` · `"uvicorn.access": {..., "propagate": False}`. **draft line 15의 두 주장이 소스와 정확히 일치** |
| `structlog.contextvars.merge_contextvars` · `bind_contextvars` · `clear_contextvars` · `structlog.stdlib.LoggerFactory` | ✅ 4종 전부 실재 (`docs/contextvars.md`) |
| structlog의 FastAPI 지목 경고 | ✅ `docs/contextvars.md` line 25 `:::{warning}` 블록 축자: *"This can be a problem in hybrid applications like those based on Starlette (this includes FastAPI) where context variables set in a synchronous context don't appear in logs from an async context and vice versa."* — **draft line 93과 완전 일치** |
| `prometheus_client.make_asgi_app` | ✅ `prometheus_client/__init__.py`의 `__all__`에 포함된 **공개 API**. 시그니처 `make_asgi_app(registry=REGISTRY, disable_compression=False)` |
| prometheus 멀티프로세스 축자·제약 | ✅ 개시 문단 축자 완전 일치. `PROMETHEUS_MULTIPROC_DIR` · *"must be wiped between process/Gunicorn runs"* · *"Custom collectors do not work"* · *"Info and Enum metrics do not work"* **4건 전부 원문 확인.** draft line 117의 세 제약 서술 정확 |
| OTel Python 안정성 상태 | ✅ `opentelemetry.io` 생성 데이터 원본 `data/instrumentation.yaml`: `traces: stable` / `metrics: stable` / `logs: development`. **draft line 99의 "트레이스와 메트릭이 Stable, 로그가 Development"와 정확히 일치** |
| `FastAPIInstrumentor.instrument_app(app)` · import 경로 | ✅ contrib 저장소 원본 `.../fastapi/__init__.py` 도크스트링과 `def instrument_app`(line 233) 실재 |

**📌 uvicorn 로깅 관련 부가 사실(정정 아님, editor 참고):** `uvicorn.error` 로거에는 `propagate` 키가 **아예 없어** 기본값 `True`를 상속한다. draft는 `uvicorn`·`uvicorn.access` 둘만 다루므로 **틀린 곳은 없다.**

---

## 🔍 저술가 자기 신고 판정 (전건)

### 13장

| # | 자기 신고 | 판정 |
|---|---|---|
| 1 | 🚨 `sessionAffinity` 프로바넌스 사고 자체 적발 → raw 소스로 재확인 | **✅ 최종 값이 raw 소스와 문자 단위 일치** (W-1). 규율이 작동했다 |
| 2 | 1차 소스 각주 — uv-docker-example · uv Docker 가이드 · Docker Hub Tags API · kubernetes/website raw 4종 · SQLAlchemy `text()` | **⚠️ 부분.** 내용 주장은 검증되는 한 전건 참이나, **6개 각주에 URL이 없어 재현 불가**(⚠️-13-1). Docker Hub 날짜 `2026-07-16`은 레퍼런스 스냅샷(2026-07-22)과 어긋난다(🕒-13-2) |
| 3 | 각주 URL을 4개(13-1·13-4·13-7·13-8)만 복원 — 허용 범위인지 판정 요청 | **⚠️ 허용 범위 아님, 그리고 신고 자체가 부정확하다.** 실측은 **3개**다 — **`13-7`에 URL이 없다.** 다른 장 4개 표본이 88~100%인데 13장만 33%다. **최소 `13-2`·`13-6` URL 복원 필요** |
| 4 | gunicorn 26.0.0 — CHANGELOG raw 404라 단정 회피 | **🕒.** 서술은 거짓이 아니나 **404의 원인은 경로 오류**였다. 실제 경로 `docs/content/2026-news.md`는 200이고 26.0.0 항목에 파괴적 변경(eventlet 제거)이 명시돼 있다(W-7) |
| 5 | Azure Bicep(T2) 코드 전면 배제, Azure를 본문에서 뺌 | **✅.** `Azure`·`Bicep` grep 0건. 계약 §8-3 준수 |
| 6 | 매니페스트에 `env` 미기재 — 필드명 날조 회피 | **✅.** 계약 §9-(A) *"재확인이 안 되면 코드를 빼고 산문으로 설명한다"* 정확 이행 |
| 7 | `(사실 확인 필요)` 1건 — `--timeout-graceful-shutdown` 기본값. 부등식 *관계*는 검증됐고 기본값만 미상 | **🕒로 해소.** 관계 주장 ✅, 문서에 기본값 표기 없다는 서술도 ✅(§1-3). **단 마커 문자열은 반드시 삭제**(🕒-13-4) |
| 8 | 앞 장 회수 8건(5·6·7·8·12·2·1·4장) | **✅ 전건 성립.** 산술 2건 검산 통과(180 · 60초 부등식), 12장 `push: false` 인수는 **문구 단위 일치** |

### 14장

| # | 자기 신고 | 판정 |
|---|---|---|
| 1 | 🚨 T-8 라벨 회피 — "상반기" 0건, 창을 2025-12~2026-07로, 1장 지칭을 "2026년 2월부터 6월까지의 세 건"으로 | **✅ 완전 통과.** grep 0건 확인, 1장 line 5와 문구 일치, 계획 line 198 요구 정확 이행 |
| 2 | "일곱 달 남짓"(2025-12-17 → 2026-07-24) | **✅ 정확** — 7개월 7일 |
| 3 | 성능 근거 비대칭 — 0건 목록 통째 공개 + 옆 분야 3편에서 질문 목록만 | **✅ 전략 · ❌ 실행 일부.** 0건 목록은 §2-2와 항목 단위 일치 ✅. 논문 3편 **전부 실재** ✅. **그러나 Mytkowicz 수치의 조건이 삭제됐다(❌-14-1)**, Georges 2건 ⚠️ |
| 4 | TechEmpower — 순위·배수 미이동, 단정 명시 부인, 축자 실재 | **✅.** 축자 원문 일치, §2-1 요구 3건 전부 이행. 🕒 "로그를 끈 채로" → "디스크 로그" 정밀화 권고 |
| 5 | 0.130.0 Rust 직렬화 재인용 안 함 (8장 `[^8-3]` 패턴) | **✅.** 14장에 `0.130`·`ORJSONResponse` grep 0건 |
| 6 | OTel·prometheus·structlog 표면 1차 소스 확인 후 각주화 | **✅ 전건 확인** (W-12). 4개 표면 묶음 전부 실재 |
| 7 | SDK 익스포터 조립 코드는 표면 미확인이라 산문 처리 (제약 9-(A)) | **✅.** 본문에서 그 사실을 독자에게 밝힌 처리가 규율과 이 책의 태도에 맞다 |
| 8 | `opentelemetry-instrumentation-fastapi` 0.65b0 / 2026-07-16 베타 표기 | **✅.** §F와 버전·날짜·베타 표기 전건 일치. §5-B 8항 요구 이행 |
| 9 | Actuator — Spring 측 설정 키·엔드포인트 경로 0개, `#9148 upvote 18` 정정 수치 사용 | **✅ 둘 다.** Spring 측 키 grep 0건(계획 제약 10의 (b) 경로), upvote 18은 §0이 창설 사례로 든 정정값 |
| 10 | 2장 `prometheus-fastapi-instrumentator` 파손 사건 회수 | **✅.** `02_final.md` line 251~259와 일치. **버전 번호를 다시 옮기지 않은 것도 안전**(§3-2 ⚠️ 회피) |
| 11 | `disable_existing_loggers` 연역 미수록 + Starlette 보장 문서 부재 명시 | **✅ 둘 다** §5-B와 일치. 그리고 uvicorn 소스 대조 결과 `False`·`propagate: False` 주장 자체도 정확(W-12) |
| 12 | 1장 지도 접기 — 세 무더기 재소환, 세 번째를 독자에게 인계 | **✅.** 세 무더기 정의가 `01_final.md` line 7과 문구 일치, 다섯 항목 전건이 4·6·10·14·3장에 실재 |
| 13 | 0.x 판단 착지 — 저자 판단으로 표시, 다수설로 말하지 않음 | **✅.** 판단 직전에 *"찬반 여론은 근거를 확보하지 못해 옮기지 않는다"*를 명시 배치. §4-6 요구 정확 이행 |

---

## 🔗 교차 충돌 점검 (1~12장 최종본 × 13·14장, 13장 × 14장)

**앞 장 예고의 회수 — 13건 전건 성립** (13장 표 참조). 추가로:

| 축 | 판정 |
|---|---|
| **13장 → 14장 인계** | 13장 마무리(*"돌기 시작한 앱에 대해 우리가 아는 것은 프로브가 200을 돌려준다는 사실 하나뿐이다"*) → 14장 첫 문단(*"프로브가 통과한다는 것은 … 이 앱이 **잘** 돌고 있다는 뜻은 아니다"*) — **연결 완전** ✅ |
| **13장 워커 1개 ↔ 14장 `/metrics`** | 14장 line 117이 13장의 결론을 근거로 멀티프로세스 문제를 회피한다. §5-B ↔ §5-D 연결과 일치 ✅ |
| **5장 contextvars ↔ 14장 요청 ID** | 14장 line 95: *"`def`로 선언한 경로 함수는 스레드풀에서 돌고 `async def`는 이벤트 루프에서 돈다는 규칙이, 여기서는 **로그에서 요청 ID가 사라지는 형태로** 다시 나타난다"* — 5장의 두 층 서술과 정합, structlog 경고 원문으로 뒷받침 ✅ |
| **4장 `RequestIdMiddleware` ↔ 14장 수정** | 임포트 유실 0건, 시그니처 변경 0건, 2줄 삽입 ✅ |
| **각주 중복 소유 점검** | structlog·opentelemetry·prometheus_client는 **앞 장 어디에도 없다**(전 final 장 grep 0건) → 14장이 소유하는 것이 계약 §8-2와 일치 ✅. 반대로 `app.mount`는 9장 소유이므로 14-4가 **재각주하지 않고 참조**했다 ✅ |
| **❌ 유일한 충돌 (BLOCKING)** | **❌-14-2** — 14장 line 163이 `Depends(scope=)`를 "오래 묵은 고통에 대해 API가 움직인" 사례로 들어, 4장 line 142의 명시적 유보(*"'`scope`가 #11107을 해결했다'고는 쓰지 않겠다"*)를 덮어쓴다. **마지막 장 총괄 특유의 위험이 실제로 발생한 유일한 지점** |

---

## 배치 5 종합 (마지막 배치)

### 판정 집계

| | ❌ | ⚠️ | 🕒 | ✅ |
|---|---|---|---|---|
| **13장** | **1** | 5 | 5 | 대량 (공식 축자 10 · 수치/버전 20 · 코드 표면 41 · 포트 사슬 5 · 앞 장 회수 11) |
| **14장** | **2** | 4 | 2 | 대량 (릴리스 표 7 · 버전/지표 12 · 코드 표면 24 · §7 금지선 7 · 1장 지도 5) |
| **웹 2차** | 0 | 2 | 3 | 12건 중 7건 완전 통과 |

**🚨 BLOCKING 항목: ❌ 3건 + `(사실 확인 필요)` 마커 1건 = 총 4건.**

| # | 항목 | 위치 | 필요 조치 |
|---|---|---|---|
| B1 | **❌-13-1** `TRACKER_` 접두사를 6장에 귀속 (실제 2장) | `13_draft.md` line 212 | "6장이 정한" → **"2장이 정한"** |
| B2 | **❌-14-1** Mytkowicz 33%/300%의 조건 삭제 (마이크로커널 ≠ SPEC, 환경 변수 단독 ≠ 두 요인) | `14_draft.md` line 139 | 측정 대상·귀속 요인 복원 + SPEC 수치(1~8%) 병기 |
| B3 | **❌-14-2** `Depends(scope=)` 인과 반올림 — 4장의 명시적 유보를 덮어씀 | `14_draft.md` line 163 | 인과 주장 철회, 4장 유보와 정합하게 재서술 |
| B4 | **`(사실 확인 필요)` 마커** — 판정은 🕒로 종결됐으나 **문자열이 원고에 남아 있다** | `13_draft.md` line 226 | 마커 문자열 **삭제** (Phase 4.5 금지 마커 스캔 대상) |

네 건 전부 **원고 수정으로 해소 가능하며 재저술이 필요한 항목은 없다.** 사실 판정이므로 저술가 재량 대상이 아니다(하네스 v1.9.1).

### 🚨 가장 위험한 3건

**1위 — ❌-14-1. Mytkowicz 33%/300%의 조건 삭제.**
같은 장 line 127이 *"조건을 지우고 숫자만 옮기는 쪽은 문서가 아니라 인용하는 우리다"*라고, line 133이 *"조건이 적히지 않은 숫자는 자기 상황으로 옮길 수도, 반박할 수도 없다"*라고 못 박은 **직후 절에서 정확히 그 행위를 한다.** 33%/300%는 합성 마이크로커널의 값이고 SPEC에서의 실제 편향은 1~8%다. 게다가 그 수치는 환경 변수 크기 **단독**의 결과인데 draft는 두 요인 모두에 귀속시켰다. 이 책이 「벤치마크 읽는 법」을 차별점으로 내걸었고(§2-2 *"이 책의 차별점. 규율을 독자에게 이전"*), 그 규율을 시연하는 바로 그 문단이 규율을 어긴다. **가장 눈 밝은 독자가 가장 먼저 잡아낼 자리다.**

**2위 — ❌-13-1 + ❌-14-2. 앞 장의 확정을 마지막 두 장이 덮어쓰는 두 건.**
13장은 `TRACKER_` 접두사를 2장이 아닌 **6장**에 귀속시켰다 — 같은 장 line 100이 이미 2장으로 정확히 귀속해놓고 line 212에서 뒤집는 **장 내부 자기모순**이다. 14장은 4장이 *"반올림하는 습관이 기술서를 못 믿게 만든다"*며 명시적으로 거부한 `Depends(scope=)` 인과를 총괄에서 반올림된 형태로 회수한다. **둘 다 "마지막 장이 앞 장을 요약하며 정밀도를 잃는" 동일 메커니즘**이고, 배치 2·3·4가 세 번 연속 보고한 *"외부 대조는 통과하고 내부 정합성에서 깨진다"*가 **네 번째로 반복됐다.**

**3위 — ⚠️-13-1. 13장 각주 URL 규율 회귀(33% vs 다른 장 88~100%).**
사실 오류는 아니지만 **이 책의 방법론 자체가 감사 가능성**인데, 하필 §7-5가 프로바넌스 위험 구역으로 지목한 장에서 감사 경로가 끊겼다. 저술가가 `sessionAffinity`에서 요약 모델의 값 날조를 실시간 적발한 바로 그 사고 현장(`kubernetes/website` raw)을 가리키는 각주 `13-6`에 URL이 없다. **그 사고를 겪고도 URL을 남기지 않았다는 점이 이 항목의 무게다.** 게다가 저술가의 자기 보고("4개 복원")도 실측(3개)과 어긋난다.

### 이 배치가 통과시킨 것 — 사전 위험 대비 결과

과제 명세가 지목한 고위험 표적이 **대부분 통과**했다.

- **K8s 매니페스트 필드명** (*"지어내기 가장 쉬운 영역"*): 15종 전건 실재·철자·중첩 정확. `preStop` 명령을 `["/bin/sh","-c","sleep 5"]`로 쓴 것은 K8s `ExecAction`이 셸을 거치지 않는다는 사실까지 반영한 **정답**이다.
- **프로바넌스 사고**: 요약 모델이 값을 날조했고, 저술가가 적발했고, raw 재확인 결과가 **정확했다.** 하네스 §7-5 규율의 첫 실전 검증 통과 사례.
- **학술 인용 3편**: 전부 실재. **의심 식별자 `arXiv:1801.02381`도 정확히 매핑.** 결함은 존재가 아니라 **조건 전달**에서 나왔다.
- **포트 8080 사슬 5지점 · 경로 이름 사슬 · `push: false` 인수**: 전건 일치.
- **§7 금지선**: Reddit·SO·#14603·Azure·Spring 설정 키 — **전 항목 0건.**
- **양화사**: 두 장 합쳐 위험한 전칭 **0건**(`아예` 1건은 전수 검색으로 뒷받침됨).

### editor·오케스트레이터 인계 사항

1. **BLOCKING 4건**(B1 ❌-13-1 · B2 ❌-14-1 · B3 ❌-14-2 · B4 마커 삭제)은 **원고 확정 전 필수 해소.** 저술가 재량 대상이 아니다.
1-1. **W-7(gunicorn CHANGELOG)은 BLOCKING이 아니지만 「정정안 1(확인해서 싣기)」을 택하도록 저술가에게 명시 전달할 것.** 13장의 닫는 문단이 *"밝혀둘 것이 둘 남았다"*로 두 건의 미확인을 고백하는데, 그중 하나는 **이제 손에 들어온 사실**이다. 확인 가능한 것을 계속 "확인하지 못했다"로 두면 그건 각주 문제가 아니라 **책이 갖지 않은 무지를 주장하는 것**이 된다.
2. **`(사실 확인 필요)` 마커는 `13_draft.md` line 226 1건이 전부**이고, 판정은 🕒로 끝났으나 **문자열 자체를 지워야** Phase 4.5 「금지 마커 스캔」을 통과한다.
3. **계약 §3-4 갱신 대상:** `app_name`의 「쓰는 장」이 `2·14`로 적혀 있으나 14장은 소비하지 않는다(🕒-14-2). 사실 오류가 아니라 계약 표의 예상 빗나감이다.
4. **`13_draft.md` line 176 `tracker:latest`에 대한 배치 4의 이월 보고는 재판정에서 뒤집혔다** — line 212 산문이 임시성을 명시하고 12장 실물(`tags: tracker:${{ github.sha }}`)과 일치한다. **불일치 아님.**
5. **13장 각주 URL 복원**은 editor 단계에서 처리하기 어렵다(1차 소스 재확인이 필요). **저술가에게 돌려보내는 편이 정확하다.**
6. **문체 관련 사항은 하나도 포함하지 않았다** — 전건 사실 판정이다.

</content>
