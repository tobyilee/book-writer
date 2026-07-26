<!-- 보강: 2026-07-25 2차 회차 — §2(Java/Node 대조) 공백 메우기, Reddit·SO 우회 재시도, 한국 커뮤니티 확대, 2026 상반기 생태계 변동 반영 -->

# FastAPI 커뮤니티 리서치

검색: 2026-07-25 기준 (1차·2차 회차 통합) · genre: `tech-book` · slug: `fastapi-web-development`
대상 독자: Spring Boot / Express·NestJS 경험이 있는 실무 개발자 (입문자 아님)

> **2차 회차 요약 — §2가 이 문서에서 가장 약한 섹션에서 가장 강한 섹션이 됐다.**
>
> **해소된 공백:** §2-2 Bean Validation(422/RFC 9457 논쟁 + Java 개발자의 Pydantic 반응, JSR-380 직접 거론 포함) · §2-5 Spring Security(**보안 부품 부패 사건** — python-jose/passlib) · §2-3 Node 개발자 전환(양방향) · §2-7 NestJS(유물 2개: PyNest 859★, FastNest) · §1-1 이벤트 루프 경고 논의 · §1-4 메모리 · §1-8 미들웨어의 예외 삼킴
>
> **최대 발견:** CPython 코어 개발자(Mark Shannon)가 *"Java has virtual threads… a better way of doing concurrency than Python's async and await"*를 **Python 내부 공식 제안**으로 올렸다(2025-05, 274 posts/565 likes). Java 독자에게 쓸 수 있는 가장 강한 1차 근거다.
>
> **여전히 비어 있음 (억지로 채우지 않았다):** Spring WebFlux/Reactor → asyncio 교차 경험담(**0건**) · 커스텀 검증기 비교(**0건**) · Actuator 대응물 직접 증언 · `application.yml`·JUnit/MockMvc · Spring Security 필터 체인 전환자의 1인칭 체감
>
> **Reddit·Stack Overflow: 우회 경로 7개 전부 실패.** 시도 경로와 실패 양상을 §6에 표로 남겼다.
>
> ❗ **1차 회차 오류 2건 정정:** #9148 upvote는 56이 아니라 **18** / §1-1 "이벤트 루프 블로킹 경고 논의조차 없다"는 **틀렸다**(#14603, 2025-12 제안 존재).

---

## 0. 이 문서를 쓰는 사람이 먼저 알아야 할 것 (수집 규율)

1. **직접 열어서 읽은 페이지만 인용했다.** 검색 엔진이 만들어준 요약만 본 페이지(Medium·SEO 블로그·부트캠프 마케팅 글 등)는 인용하지 않았다. §7 출처 목록에는 실제로 페치해서 본문을 읽은 URL만 들어 있다.
2. **Reddit은 이번 회차에서 단 한 건도 수집하지 못했다.** 검색·페치 양쪽 다 차단됐다. r/FastAPI·r/Python·r/ExperiencedDevs·r/django·r/webdev 인용은 이 문서에 **하나도 없다**. Stack Overflow도 동일하게 차단됐다. §6 참조 — 이건 커버리지 구멍이니 침묵으로 넘기지 마라.
3. **버전 번호를 커뮤니티 글에서 인용하지 않았다.** 필요한 경우 "{연도} 시점 글에서 언급됨"으로만 적었다. 버전·API 근거가 필요하면 fact-checker가 1차 소스로 대조해야 한다.
4. **날짜는 직접 확인한 것만 적었다.** 확인 못 한 건 `게시일 미확인`으로 표시했다.
5. **FastAPI 저장소는 옛 이슈를 Discussions로 일괄 이관했다.** 그래서 번호가 낮은 discussion이 실제로 오래된 날짜를 갖는다. 오래된 항목은 아래에서 🕒 **[구식 가능]** / ✅ **[현재도 유효]** 로 별도 판정했다. **이미 해소된 불만을 현재형으로 쓰면 책이 즉시 낡는다.**
6. 커뮤니티 발언은 전부 **개인 경험담**이다. 벤치마크 수치·성능 주장은 재현 조건이 불명확하므로 그대로 인용하지 말고 "누가 언제 이렇게 말했다"로만 써라.
7. **`> **책에 쓸 관점:**` 로 시작하는 블록은 커뮤니티 발언이 아니라 이 에이전트의 해석이다.** 커뮤니티 합의로 인용하지 마라. 특히 Spring/JPA 쪽 기술 주장(OSIV, 트랜잭션 경계 등)은 **fact-checker가 1차 소스로 대조해야 하는 미검증 서술**이다.

**신선도 요약:** 최근 12~18개월(2025-02 ~ 2026-07) 자료로 확인된 것 — 배경 태스크 회귀(2025-10), 서버리스 콜드 스타트(2025-11), 대용량 직렬화 비용(2025-03), Litestar 대이동 논쟁(2025-08), SQLModel 검증 무력화 주장(2026-03), NestJS식 구조 이식 시도(2026-04), FastAPI Cloud 공개 베타(2026-06).

---

## 1. 실무 고통점 (재현 조건 / 증상 / 커뮤니티 해법 / 미해결)

### 1-1. 동기 블로킹으로 인한 이벤트 루프 스톨 ✅ [현재도 유효]

**재현 조건 (커뮤니티가 반복해서 지목하는 형태)**
- `async def` 라우트 안에서 동기 DB 드라이버를 호출 (연결 문자열을 `postgresql+asyncpg://`가 아니라 `postgresql://`로 둔 경우가 대표적)
- `async def` 안에서 `requests`, `time.sleep`, 무거운 CPU 연산 호출
- **응답 직렬화 자체가 블로킹**인 경우 — 이게 가장 안 알려진 축이다

**증상**
- 즉시 에러가 나지 않는다. **부하가 걸려야만** 드러난다. 그래서 "재현이 안 되는 성능 문제"로 분류돼 오래 방치된다.
- 한국 커뮤니티에도 같은 질문이 있다: OKKY Q&A **"fastapi 동시요청시 blocking 이유"** (작성자 sttwantman, 답변 2건). ※ 본문·답변 텍스트는 페치 실패로 확보 못 함 — 제목과 존재만 확인. `(확인 필요 — 본문 미확보)` · 게시일: 사이트 표기 "거의 3년 전"(≈2023년경, 정확한 날짜 미확인)
  - https://okky.kr/questions/1473757

**직렬화가 이벤트 루프를 막는다는 증언 (구체적 수치 있음)**
- GitHub fastapi/fastapi Discussion #9044 **"jsonable_encoder is not async, can stall the event loop"** (작성자 sm-Fifteen, 2020-04-07)
  - 원 보고: 프로파일러에서 인코딩이 6,267ms를 먹는 동안 다른 작업은 밀리초 단위. 최소 재현 예제에서 **직렬화가 서버 전체를 10초간 막았다.**
  - 원문: *"JSON encoding and rendering blocking the server is something I would consider highly undesirable for an async-focused framework."*
  - 답변자 connebs (2020-05-16): 다층 구조 데이터에서 `jsonable_encoder`가 **약 400ms**, 직접 dict를 만들고 `ORJSONResponse`로 바꾸니 **약 100ms** — 약 4배 차이라고 보고.
  - https://github.com/fastapi/fastapi/discussions/9044
  - 🕒 **판정 주의:** 2020년 글이다. Pydantic v2 이후 직렬화 경로가 크게 바뀌었으므로 **수치를 현재형으로 쓰면 안 된다.** 다만 "무거운 응답 직렬화가 이벤트 루프를 점유할 수 있다"는 **구조적 사실 자체는 2025년 사례(§1-6)에서도 재확인된다.**

**커뮤니티가 합의한 해법 (가장 널리 인용되는 3단 규칙)**
- `zhanymkanov/fastapi-best-practices` (GitHub, 별 17.8k · 마지막 갱신일 미확인)가 정식화한 형태:
  - 원문: *"if you violate that trust and execute blocking operations within async routes, the event loop won't be able to run other tasks until the blocking operation completes."*
  - **Terrible** — `async def` 안에서 동기 블로킹: 이벤트 루프 전체 정지
  - **Good** — 그냥 `def`: FastAPI가 스레드풀로 돌려주므로 루프는 안 막힌다
  - **Perfect** — 진짜 async I/O
  - CPU 바운드는 GIL 때문에 async도 스레드도 답이 아니다 → 멀티프로세싱이나 태스크 큐(Celery)
  - https://github.com/zhanymkanov/fastapi-best-practices

> **책에 쓸 관점:** 커뮤니티의 지배적 조언은 "무조건 async를 써라"가 아니라 **"동기 드라이버를 쓸 거면 `def`로 선언해라"**다. Spring 개발자가 가장 헷갈리는 지점이 여기다 — `async def`가 항상 더 빠르다고 생각하는 것. 오히려 그게 최악의 조합이다.

**FastAPI 저장소에 남은 3단 분류의 원전 (2차 회차 추가)**
- GitHub fastapi/fastapi Discussion #8842 **"Fast api is blocking long running requests when using asyncio calls"** (**2021-04-16**), sm-Fifteen의 정리:
  > *"Here are the three main cases. The first one (`async_will_block`) is what you want to avoid... **Async routes run on the main thread and are expected to never block for any significant period of time.** … Sync routes are run in a separate thread from a threadpool, so any blocking will not affect the main thread."*
  - `async def` + 블로킹 / `def` + 블로킹 / `async def` + await 3분류를 코드로 제시 — **Spring MVC 출신 독자에게 그대로 대응표로 쓸 수 있다.**
  - https://github.com/fastapi/fastapi/discussions/8842
- 같은 실수가 2025년에도 그대로 반복된다 — Discussion #14339 **"Differences in how synchronous and asynchronous requests are handled"** (**2025-11-12**). 질문자는 **OpenAI 동기 클라이언트를 `async def` 안에** 넣었다. YuriiMotov의 답:
  > *"As your function is `async` and there is no any `await` inside it, it will be executed in one go without interruption. So, **your worker will only be able to handle 1 request at a time.**"* → 해법은 `def`로 바꾸거나 `run_in_threadpool`.
  - https://github.com/fastapi/fastapi/discussions/14339
  - ✅ **최신 사례이고, 게다가 LLM 클라이언트라는 요즘 가장 흔한 맥락이다.** 챕터 예제로 시의성이 높다.

**아직 미해결 — 단, 진전이 있다 (1차 회차 판정 수정)**
- ❗ **1차 회차 정정:** "정적으로 잡을 방법이 없고 그런 논의조차 못 찾았다"고 적었으나, **논의는 있다.** 다만 **아직 기능으로 존재하지 않는다.**
  - GitHub fastapi/fastapi Discussion #14603 **"Warn on blocked event loop in dev mode"** (작성자 Otto-AA, **2025-12-26**)
    > *"The async docs explain that sync IO/... should not be used in async path operations. However, I think it is: **easy to get wrong for beginners; hard to troubleshoot, because there is no exception/warning/... pointing to the cause of the performance issue. I've seen this happen in production applications** and also found several issues related to this when searching the discussions here"*
    - 동작하는 PoC 코드까지 첨부됐다.
    - https://github.com/fastapi/fastapi/discussions/14603
  - **즉 현재 상태는 이렇다: 문제는 문서화돼 있고, 커뮤니티가 개발 모드 경고를 요청했으며, 2025년 말 시점에 제안 단계다.** ⚠️ 저술 시점에 채택 여부를 재확인하라. "경고해준다"고 쓰면 틀릴 수 있다.
- **표준 린트 게이트**가 커뮤니티 표준으로 자리 잡았다는 증거는 여전히 못 찾았다. `⚠️ 근거 못 찾음`
- 직렬화 블로킹은 프레임워크 레벨에서 해결됐다는 결론이 난 흔적이 없다 — #9044는 "버그로 재분류하자"는 제안(SyntaxColoring, 2023-02-28)까지 나왔지만 discussion으로 남았다.

---

### 1-2. 비동기 세션 관리와 N+1 (`MissingGreenlet`) ✅ [현재도 유효]

**재현 조건**
- `AsyncSession`으로 가져온 ORM 객체를 **응답 모델에 그대로 반환**하고, 그 모델에 관계 필드가 있는 경우. FastAPI가 응답을 직렬화하면서 아직 로드 안 된 관계에 접근 → lazy load 시도 → 비동기 세션은 동기 I/O를 못 하므로 폭발.

**증상 (원문 그대로)**
- GitHub fastapi/fastapi Discussion #13125 **"Lazy loading of SQLAlchemy AsyncAttrs in response causes MissingGreenlet exception"** (작성자 yurii-franasiuk, 2024-12-30)
  - 에러 문구: *"Error extracting attribute: MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here."*
  - **에러 위치가 범인 위치와 다르다는 게 함정이다.** 터지는 곳은 응답 직렬화 시점이지만 원인은 쿼리 작성 시점이다.
  - https://github.com/fastapi/fastapi/discussions/13125

**커뮤니티 해법**
- 답변자 sehraramiz (2024-12-31): 관계에 `lazy="selectin"`을 걸어 **ORM 레이어에서** 해결하라 — 프레임워크가 알아서 해줄 문제가 아니다.
- 원 보고자는 FastAPI의 `serialize_response`가 `AsyncAttrs`를 감지해 `asyncio.gather()`로 선로딩하도록 프레임워크를 고치자고 제안했으나 **채택되지 않았다.** 답변자의 판정: 이건 FastAPI 문제가 아니라 ORM 설정 문제.

> **여기서 나오는 진짜 교훈:** FastAPI는 이 문제를 **자기 책임으로 인정하지 않는다.** 즉 이건 프레임워크가 언젠가 고쳐줄 버그가 아니라, **개발자가 영구히 지고 가야 하는 규율**이다. Spring Data JPA에서 OSIV(Open Session In View)가 뒤에서 lazy loading을 받쳐주던 것과 정확히 반대다.

**연결된 세션 수명 문제 — 이건 더 깊다**
- GitHub fastapi/fastapi Discussion #11107 **"Context managers in `Depends` are broken after 0.106"** (작성자 axd1x8a, 2024-02-07)
  - 문제: 의존성 `yield` 이후 코드의 실행 시점이 바뀌었다. 이전에는 미들웨어 처리 **후**, 이후에는 미들웨어 처리 **전**.
  - 세션 관점에서 순서가 이렇게 뒤집혔다:
    - 변경 전: 세션 생성 → 열기 → **커밋** → 닫기
    - 변경 후: 세션 생성 → 열기 → **닫기** → 커밋
  - falkben (2024-02-13, 반응 5): `StreamingResponse`가 컨텍스트 매니저 자원에 의존할 때도 깨진다고 실증.
  - Kludex(메인테이너, 2024-02-14, 채택 답변): *"It's the intended behavior, but I've raised the issue #11143 from this discussion."* → **의도된 동작**이라고 답하고 별도 이슈로 승격. 논의 자체는 완결 없이 종료.
  - https://github.com/fastapi/fastapi/discussions/11107
  - ✅ 신선도: 2024년이지만 §1-8의 2025년 회귀 사건과 **같은 뿌리**(`yield` 의존성의 생명주기)이므로 현재도 유효한 주제.

**미해결**
- `expire_on_commit` 함정에 대해 **커뮤니티 스레드에서 직접 확인한 근거는 못 찾았다.** (검색 요약에는 나왔지만 페이지를 열어 확인하지 못했다.) `⚠️ 근거 못 찾음 — 별도 검증 필요`
- 요청 간 세션 누수에 대한 구체적 스레드도 확보 실패. 관련 후보로 Discussion #10622 "FastAPI sqlalchemy session per request handling"(작성자 theobouwman, 목록상 2023-11-10, upvote 2, **Closed/Unanswered**)이 있으나 본문 미확보. `(확인 필요 — 목록만 확인)`

---

### 1-3. `Depends` 체인 — 성능·캐싱 오해·테스트 ✅ [현재도 유효]

**가장 흔한 오해: "`Depends`는 캐싱되니까 싱글턴이다"**
- GitHub fastapi/fastapi Discussion #8054 **"Dependency Injection - Singleton?"** (작성자 Gui-greg, 2019-09-04, upvote 11, **여전히 Unanswered**)
  - euri10이 "FastAPI에 이미 의존성 캐싱이 있지 않냐"고 물었고(반응 약 48),
  - dmontagu가 못을 박는다: **내장 캐싱은 "단일 요청 안에서의 중복"만 막는다. 요청 간에는 캐싱되지 않는다.** (반응 약 14)
  - 우회법들이 연도별로 쌓였다: `functools.lru_cache`(dmontagu, 2019) → 앱 startup에서 한 번 인스턴스화(euri10) → `app.state`에 저장(sm-Fifteen, 2022-03-01) → `AsyncExitStack` + app state로 종료 시 정리(g0di, 2024-11-22)
  - MateuszCzubak(2019-11-15, 반응 약 12)은 진짜 빠진 건 다른 거라고 지적: **클래스 기반 뷰**가 없어서 주입 보일러플레이트가 반복된다.
  - tiangolo(메인테이너, 2020-02-10): 문서의 "classes as dependencies"를 가리키며 애초에 지원되던 패턴이라고 답변.
  - https://github.com/fastapi/fastapi/discussions/8054
  - ✅ **2019년에 열려서 2024년 답글까지 붙었는데 여전히 미해결 표시다.** 이 스레드 자체가 "이건 프레임워크가 풀 생각이 없는 문제"라는 증거다.

**성능 측면 — 커뮤니티가 만든 대안 라이브러리의 진단**
- `dishka` 공식 문서 "Alternatives" (표에 명시된 기준 시점: **2024-03-08**)가 `Depends`의 한계를 6개로 정리한다. 원문:
  1. *"It can be used only inside FastAPI."*
  2. *"You cannot use it for lazy initialization of singletons."*
  3. *"It mixes up Dependency Injection and Request decomposition. That leads to incorrect OpenAPI specification or even broken app."*
  4. *"You have to declare each dependency with `Depends` on each level of application. So either your business logic contains details of IoC-container or you have to duplicate constructor signatures."*
  5. *"It is not very fast in runtime, though you might never notice that."*
  6. *"Almost all examples in documentation ignore `dependency_overrides`, which is actually a main thing to use FastAPI as IoC-container."*
  - 비교표 판정: 스코프 부분 지원(✅❌), async ✅, finalization ✅, **동시성 안전성 ➖, 컨텍스트 데이터 ❌, 완전 자동 와이어링 ❌**
  - https://dishka.readthedocs.io/en/stable/alternatives.html
  - **이건 경쟁 라이브러리의 주장이므로 편향을 감안해서 읽어야 한다.** 다만 4번(각 계층마다 `Depends`를 선언해야 해서 비즈니스 로직이 IoC 컨테이너를 알게 되거나 생성자 시그니처를 중복해야 한다)은 §2의 Spring 대조에서 반복 확인되는 구조적 지적이다.

**"Depends의 마법이 Python스럽지 않다"는 반론**
- Lobsters, FastDepends 소개 스레드 (게시: 사이트 표기 "3 years ago" ≈ 2022년경, 정확 날짜 미확인)
  - linkdd: *"I like FastAPI (and its Django counterpart: Django Ninja), but this kind of black magic is nowhere near the zen of Python: > Explicit is better than implicit. The implicit casts, the custom fields which completely change the function call, all of this serves to obfuscate the code, and the developer cannot infer anything from the call site anymore and have to know about the callee. This is fine in an HTTP API because in the end, it's not you who calls the functions that serve as routes. But here, I'm not sure about the benefits."*
  - BiteCode: *"It benefits any lib where you provide hooks for entry points or endpoints. Basically, this is a nice tool for where you need inversion of control."*
  - linkdd 재반박: *"If I need dependency injection and inversion of control, I'd use dependency-injector which is way more pythonic in its design. But that's only my opinion."*
  - https://lobste.rs/s/smuqhv/fastdepends_fastapi_di_system_cleared

**미해결**
- **깊은 `Depends` 중첩의 실측 오버헤드를 담은 커뮤니티 스레드는 못 찾았다.** dishka의 "not very fast in runtime, though you might never notice that"가 확보한 최선의 근거다. `⚠️ 근거 못 찾음 — 정량 데이터 없음`

---

### 1-4. 배포 시 워커·스레드 수 결정 ✅ [현재도 유효, 단 권고는 이동했다]

**커뮤니티가 실제로 쓰는 숫자 (전부 개인 경험담이다)**
- GitHub fastapi/fastapi Discussion #7439 **"Gunicorn or pure uvicorn in a kubernetes cluster"** (작성자 mauermbq, 2020-05-26)
  - 질문의 핵심: *단일 프로세스를 담으라고 만든 컨테이너 안에서 왜 gunicorn을 돌리는가?*
  - tiangolo(메인테이너, 2020-06-06): *"Sure, if you have another way of declaring and controlling how many containers to spin up, maybe in some automated way, and have a load balancer on top to direct requests to them, then it probably makes sense to do that and have just Uvicorn directly."*
  - **nreith (2022-07-05):** *"2 workers per cpu plus 1 extra"* → CPU 1코어 + RAM 600MB 환경에서 **워커 3개**로 정착. 평상시 파드 3개, 고부하 시 5개. **locust.io로 부하 테스트를 먼저 하고 정하라**고 조언.
  - **GuiGav (2022-09-28) — 이게 핵심 트레이드오프다:** gunicorn을 쓰면 워커가 죽어도 **쿠버네티스가 모른다.** gunicorn 없이 돌리면 컨테이너 재시작이 표준 k8s 메트릭으로 관측된다.
  - Irmius (2023-10-10): 공식 문서가 컨테이너당 단일 uvicorn 프로세스를 권한다고 언급하며, gunicorn은 k8s 기능과 중복이라고 정리.
  - https://github.com/fastapi/fastapi/discussions/7439

- GitHub fastapi/fastapi Discussion #8433 **"Scale FastApi with sync endpoints"** (작성자 dapollak, 2022-12-08)
  - 증상: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`로 워커 4개를 띄웠는데 부하가 균등하게 안 퍼진다. 첫 5개 요청 중 4개가 같은 PID(643)로 갔다. 원문 요지: *"while one worker is very busy, the rest three are significantly less busier."*
  - 원인(왜 동기 엔드포인트를 쓰냐는 질문에 대한 답): **asyncio 미지원 Snowflake SQLAlchemy 드라이버.** — 실무에서 sync를 못 버리는 전형적 이유다.
  - jgould22: 동기 엔드포인트는 스레드풀로 가니 워커 수를 늘려라 — **코어당 2개** 권장.
  - iudeen: gunicorn 말고 **uvicorn 단독 + 워커 1개**로 두고 컨테이너 복제로 수평 확장해라.
  - **Kludex(collaborator):** *"Gunicorn relies on the operating system to provide all of the load balancing when handling requests"* — 즉 불균등 분배는 FastAPI가 어쩔 수 있는 게 아니라 **OS 스케줄러 문제**다. 그리고 **AnyIO의 기본 스레드 상한이 40개**라고 언급.
  - dapollak: `anyio.to_thread.current_default_thread_limiter()`로 스레드를 제한해봤지만 워커 간 분배는 개선되지 않았다.
  - https://github.com/fastapi/fastapi/discussions/8433

**gunicorn+UvicornWorker vs uvicorn 단독 — 현재 공식 입장 (커뮤니티가 아니라 문서다, 구분해서 써라)**
- FastAPI 공식 배포 문서 `deployment/server-workers/` (본 리서치 시점 **2026-07-25에 직접 페치**)에는 **gunicorn이 아예 언급되지 않는다.** `fastapi run --workers 4` 또는 `uvicorn --workers 4` 형태만 제시한다.
- 같은 페이지가 명시한다: *"In particular, when running on **Kubernetes** you will probably **not** want to use workers and instead run **a single Uvicorn process per container**"*
- **워커를 몇 개 둘지에 대한 숫자 권고는 문서에 없다.** → 그래서 커뮤니티가 각자 경험칙(위의 "코어당 2개+1" 등)으로 메우고 있는 것이다.
- https://fastapi.tiangolo.com/deployment/server-workers/
- ⚠️ **fact-checker에게:** "예전엔 gunicorn을 권했는데 지금은 아니다"라는 서사를 쓰려면, 문서 변경 이력을 1차 소스로 별도 확인해야 한다. 이 문서는 **현재 상태만** 확인했다.

**메모리가 계속 차오른다 — 5년에 걸친 스레드 하나가 범인을 지목한다** ✅

- GitHub fastapi/fastapi Discussion #9145 **"Gunicorn Workers Hangs And Consumes Memory Forever"** (작성자 MeteHanC, **2019-10-07**, 답글이 **2024-08**까지 이어짐)
  - 재현 조건: `gunicorn -w 8 -k uvicorn.workers.UvicornH11Worker --timeout 10` + 병렬 30~40 요청 부하 테스트.
  - 증상 원문: *"RAM usage is always growing, seems like no task is killed after completing its job"*, *"gunicorn workers do not get killed."* 메인 gunicorn 프로세스를 죽여도 **자식 프로세스가 살아남아 메모리를 계속 점유**.
  - 독립 확인 — madkote (2019-12-04): 200MB짜리 리소스를 로드해 처리하고 응답하면 *"the memory is not given free."* gunicorn·uvicorn·hypercorn 전부에서 동일. **결정적인 건 이 대목이다 — 똑같은 라이브러리 코드가 Flask에서는 메모리를 정상 반환했다.**
  - 1차 진단 — dmontagu (2019-12-04): Python은 애초에 OS로 메모리를 돌려준다고 보장하지 않는다 — *"when a block is deemed 'free,' that memory is not actually freed back to the operating system."* (즉 상당수는 누수가 아니라 **할당자 동작**이다.)
  - **4년 뒤 진짜 범인 지목 — AntonioBarral (2023-10-11):** *"The cause of the memory leak is the **exception_handler decorator**. Every time this decorator is invoked, the gc will not free all the memory used for the API worker."* 예외 핸들러 안에서 `gc.collect()`를 부르는 우회법을 제시하며 *"a huge bug that needs a correction"*이라고 평가.
  - 재현 확인 2건: makerjackie (2024-04-24) 해결 확인, **hzy0809 (2024-08-27):** *"When starting the service with uvicorn, **no memory leak occurred.** However, when using **gunicorn with uvicorn, a significant memory leak was observed.** Your solution worked, thank you!"*
  - https://github.com/fastapi/fastapi/discussions/9145
  - ⚠️ **fact-checker 필수 대조:** "예외 핸들러가 GC를 막는다"는 **커뮤니티 진단이며 공식 확인이 아니다.** 그리고 위 증언들은 2023~2024년 시점이다. 이후 수정됐는지 반드시 1차 소스로 확인하고, 안 됐다면 **재현 조건(gunicorn+UvicornWorker 조합에서 두드러짐)을 반드시 함께 써라.**

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** §1-4의 gunicorn vs uvicorn 논쟁에 이 스레드가 세 번째 논거를 준다. GuiGav의 "관측성" 논거, 공식 문서의 "컨테이너당 단일 프로세스" 권고에 더해, **hzy0809의 증언은 메모리 거동 자체가 두 구성에서 다르다고 말한다.** 다만 단일 증언이므로 단정하지 마라.

**여전히 미해결**
- **컨테이너 CPU limit과 워커 수의 관계**를 정면으로 다룬 스레드는 끝내 못 찾았다. `⚠️ 근거 못 찾음`
- 미확보 리드: #9082 "The memory usage piles up over the time and leads to OOM", #7299 "Choosing the Right ASGI Server for Deploying FastAPI". `(확인 필요 — 목록만 확인)`

---

### 1-5. 서버리스 콜드 스타트 ✅ [현재도 유효 — 최근 사례]

**재현 조건과 증상 (숫자 있는 실사례)**
- GitHub aws/aws-lambda-web-adapter Discussion #620 **"FastAPI uvicorn app start-up is very slow, causing timeouts"** (작성자 tibbe, **2025-11-10**)
  - 로그: `INIT_REPORT Init Duration: 9930.03 ms Phase: init Status: timeout`
  - **약 9.9초에 Lambda 런타임이 재시작**됐고, 앱이 HTTP 요청에 답하기까지 **18초 이상** 걸렸다. Lambda 29초 타임아웃에 걸림.
  - 메인테이너 bnusunny(같은 날) 처방: (1) **시작 시 임포트하는 의존성을 줄여라**, (2) Lambda SnapStart — *"might be easier option to reduce the cold start time"*
  - https://github.com/aws/aws-lambda-web-adapter/discussions/620

> **책에 쓸 관점:** 콜드 스타트의 주범은 FastAPI가 아니라 **임포트 그래프**다. pandas·torch 같은 무거운 의존성이 모듈 최상단에 있으면 라우트가 호출되든 말든 매 콜드 스타트마다 비용을 낸다. 그런데 FastAPI의 관용적 코드 스타일(모듈 최상단에서 모델·의존성·설정을 전부 임포트)은 이 함정으로 자연스럽게 유도한다.

**미해결 / 근거 부족**
- Cloud Run·최소 인스턴스 설정에 대한 **커뮤니티 스레드**는 확보 못 했다. `⚠️ 근거 못 찾음`
- pandas/torch를 구체적으로 지목한 커뮤니티 토론도 직접 읽은 것이 없다. 위 #620은 "의존성을 줄여라"까지만 말한다. **지어내지 말 것.**

---

### 1-6. Pydantic 검증·직렬화 오버헤드 ✅ [현재도 유효 — 단 v1 시절 불만과 구분하라]

**현재형으로 쓸 수 있는 유일한 실측 증언 (2025년)**
- GitHub fastapi/fastapi Discussion #13455 **"Fetching a lot of time series data"** (작성자 ValentinKaisermayer, **2025-03-05** ~ 2025-04-28)
  - 시계열 **35,000 포인트**를 한 엔드포인트로 내보낼 때의 분해:
    - DB 조회 **약 0.15초**
    - Pydantic 검증 **약 0.17초**
    - **응답 직렬화 약 0.60초** ← 가장 비싸다
    - 브라우저 기준 총 2초 (서버 응답 대기 1.8초)
  - 부수 증상: Swagger UI 문서 엔드포인트가 **"Maximum call stack size exceeded"**로 뻗는다.
  - **반직관적 결과:** FastAPI에 직렬화를 맡겼을 때가 **1.6초**로, 수동 orjson 직렬화보다 **오히려 빨랐다.**
  - 채택 답변(sachinh35, 2025-04-27): curl 타이밍 분석 결과 *"your backend server is taking close to 0.47s to calculate the response before sending it back completely over the network."* → FastAPI 차원의 유일한 최적화는 자동 직렬화 대신 수동 JSON 직렬화라고 결론.
  - 원 보고자의 반론이 실무적으로 좋다: 페이지네이션 대신 **LTTB 같은 서브샘플링**이 시계열엔 낫다 — Full HD 화면에서 사용자는 3만 5천 점을 어차피 구분 못 한다.
  - https://github.com/fastapi/fastapi/discussions/13455

**"v2로 넘어가서 얼마나 나아졌나"에 대한 실측 증언**
- ⚠️ **근거 못 찾음.** v1 → v2 전환의 실측 개선폭을 담은 커뮤니티 증언을 직접 읽은 것이 없다. **절대 지어내지 마라.**
- 대신 확보한 건 **전환 자체의 고통**에 대한 증언이다:
  - HN 44819192, rtpg (2025-08-06): *"maintainers just having to assume every behavior is needed for backwards compatibility... and you still have the absolute mess which was pydantic 1 -> 2 (or django-ninja 0.x -> 1.0) Everyone talks about moving fast and being dynamic but everyone I know deep in this has lost like actual years to churning from this kind of behavior."*
  - **"실제로 몇 년을 날렸다"** — 이건 성능 얘기가 아니라 **생태계 churn 비용**에 대한 증언이다. 별개 주제로 다뤄라.
- 🕒 **구식 주의:** Discussion #8165 "enhance serialization speed"(upvote 29, 목록상 2019년)와 #9044(2020)의 수치는 **Pydantic v1 시대 것이다.** 현재형으로 쓰면 안 된다.

---

### 1-7. 프로젝트 구조 붕괴 ✅ [현재도 유효 — 논쟁 진행 중]

**가장 널리 인용되는 커뮤니티 표준**
- `zhanymkanov/fastapi-best-practices` (별 **17.8k**, 커밋 81개, 영·중 문서)
  - 핵심 권고: **파일 종류가 아니라 도메인/모듈로 나눠라.** 각 도메인 패키지가 `router.py`·`schemas.py`·`models.py`·`service.py`·`dependencies.py`·`constants.py`·`config.py`·`utils.py`·`exceptions.py`를 갖는다.
  - 의존성 관련: Pydantic 스키마 검증을 넘는 검증(DB 조회, 외부 서비스)은 의존성으로, 의존성 체인으로 중복 제거, **요청 스코프 내 캐싱이므로 한 번 호출하고 여러 번 재사용**, 스레드풀 오버헤드를 피하려면 async 의존성 선호.
  - https://github.com/zhanymkanov/fastapi-best-practices

**여기에 대한 정면 반론 (같은 날 HN에서 붙었다)**
- HN 44821271, canadiantim (2025-08-07) — `iam-abbas/FastAPI-Production-Boilerplate`를 가리키며: *"I will never understand the minds of people that structure their apps like this"* → 전통적 계층 구조 대신 **미니 앱(모듈) 단위 구조**가 경계 유지에 낫다고 주장.
- HN 44822016, **hynek** (2025-08-07): *"The fancy word for that is Vertical Slice Architecture btw and it's the only way for complex apps that doesn't end in chaos."*
  - ※ hynek은 Python 생태계에서 이름이 알려진 개발자다(attrs·structlog). 익명 증언보다 가중치를 줄 만하다.
- HN 44822469, shakna (2025-08-07) — VSA에도 반론: Bogard의 원 글에서 컨트롤러는 **VSA가 잘 안 맞는 예**로 꼽혔다. *"Relying on it as dogma will result in chaos."*

**FastAPI 옹호 쪽 (한쪽으로 결론 내지 마라)**
- HN 44819446, jaza (2025-08-07): 몇 년째 FastAPI를 무겁게 써온 입장에서 — *"I think OP's arguments about FastAPI being hard to work with in a bigger codebase are exaggerated. Splitting up the routes into multiple files, each with its own route object, and then importing and building up a big hierarchy of route objects, isn't that hard, it does the job for me. Agreed that it's probably not well documented enough, how to structure a larger FastAPI codebase - but follow a mix of best practices and your personal tastes, break it up into modules, split it into specific files for constants / errors / routes / schemas / crud / etc, and you can scale up sanely."*
- HN 44821229, whilenot-dev (2025-08-07) — 구조 부재를 **기능으로** 재해석: *"The main benefit from micro frameworks like FastAPI/Flask/Express.js is that you _must_ build your own framework! You can pick the building blocks that will make your life easier, instead of relying on choices that made the maintainer life in full-fledged frameworks like Django/Laravel/RoR bearable."*
- **참조 코드베이스 논쟁도 있다** — HN 44822799, whinvik: *"For FastAPI I know that I can go to [polarsource/polar] and see what a good FastAPI code base looks like... For me to jump on Litestar, I would like to see a reference codebase to learn best practices."* → 프로덕션 FastAPI 코드베이스로 **`polarsource/polar`**를 지목. 같은 스레드에서 **Airflow도 FastAPI 위에 있다**고 언급됨(*"These days even Airflow is on FastAPI"*). ⚠️ 두 항목 모두 fact-checker 대조 필요 — 커뮤니티 언급일 뿐이다.

**한국 커뮤니티의 같은 고통 (독립 증언이라 가치가 높다)**
- velog, 동근이의 개발 일기(soondcuk) **"[Fastapi] Spring Boot vs Fastapi 개인적인 의견"** (2025-01-20)
  - 형식이 강제되지 않아 **"이렇게 해도 돼..?"** 라는 의문이 들 정도이며, 팀 협업 시 명확한 컨벤션이 없으면 **"유지보수에 큰 어려움이 있었다"**고 서술.
  - https://velog.io/@soondcuk/Fastapi-Spring-Boot-vs-Fastapi-개인적인-의견

---

### 1-8. 배경 태스크가 조용히 실패한다 ✅ [현재도 유효 — 2025년 회귀 사례]

**가장 최근의 구체적 사고**
- GitHub fastapi/fastapi Discussion #14137 **"[0.118 Regression] Background tasks not executed if added after a `yield`"** (작성자 JP-Ellis, **2025-10-01**, 해결 2025-11)
  - 증상: 의존성의 `yield` **이후**에 추가한 배경 태스크가 **조용히 아예 실행되지 않는다.** `yield` 뒤의 print는 정상 실행되므로 **아무 신호도 없다.** 동기·비동기 의존성 양쪽 다.
  - 원 보고 주석 그대로: *"The following background task is never executed"*
  - tiangolo 답변 요지: 배경 태스크는 응답 사이클 중에 돌지만, 이제 `yield` 이후 코드는 응답이 전송된 **후**에 실행된다 — *"Now that dependencies with `yield` are (again) by default closed after the response is sent, the code after `yield` doesn't have a way to add background tasks"*. 해법은 `Depends(func, scope="function")` 옵트인.
  - https://github.com/fastapi/fastapi/discussions/14137
  - ⚠️ **fact-checker에게:** 위 답변에 언급된 버전 번호들은 커뮤니티 글에서 인용하지 말고 릴리스 노트 1차 소스로 대조하라.

**두 번째 침묵 경로: 미들웨어가 에러를 삼킨다** ✅

- GitHub fastapi/fastapi Discussion #11828 **"middleware hides errors from background tasks"** (작성자 varun-seth, **2024-07-11**)
  - 재현 조건이 잔인할 만큼 평범하다: **응답 헤더 하나 추가하는 HTTP 미들웨어**를 붙인다. 그 상태에서 배경 태스크가 `ValueError`를 던진다. → **로그에도, 화면에도 아무것도 안 나온다.**
  - gustavosett (2024-07-11): 배경 태스크 에러는 원래 메인 요청 흐름에 영향을 주지 않고 조용히 지나갈 수 있으니, **미들웨어에 기대지 말고 태스크 안에 명시적으로 로깅을 넣어라.**
  - **채택 답변 — YuriiMotov (2024-09-21):** 이건 FastAPI가 아니라 **Starlette 쪽 문제**이며 특정 버전에서 유입됐다고 판정. 순수 Starlette 재현 앱을 제시.
  - https://github.com/fastapi/fastapi/discussions/11828
  - ⚠️ 언급된 Starlette 버전은 커뮤니티 글에서 인용하지 말고 1차 소스로 대조하라.

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** 배경 태스크가 조용히 죽는 경로가 **최소 두 개**다. (1) 생명주기 문제로 아예 등록조차 안 되는 경우(#14137, 2025), (2) 등록·실행은 됐는데 **미들웨어가 예외를 삼키는** 경우(#11828, 2024). 둘 다 **로그가 아무 말도 안 한다.** Spring의 `@Async` + `AsyncUncaughtExceptionHandler`처럼 "못 잡은 예외를 어디로 보낼지"에 대한 기본 계약이 여기엔 없다. 실무 처방은 하나로 수렴한다 — **배경 태스크 본문 전체를 try/except로 감싸고 직접 로깅하라.**

**같은 계열의 미확보 리드 (목록만 확인, 본문 미확보)**
- #14623 "Add Starlette BackgroundTask Warning to FastAPI Docs" (목록상 2025-12-30, upvote 3)
- #8987 "BackgroundTasks do not run when request failed"
- `(확인 필요 — 목록만 확인)`

> **패턴:** `yield` 의존성의 생명주기가 2024년(#11107)과 2025년(#14137) 두 번 논쟁의 중심이었다. **FastAPI에서 "언제 정리되는가"는 안정된 계약이 아니다.** 이게 Spring의 `@Transactional` 경계처럼 확정적이길 기대하면 다친다.

---

### 1-9. 미들웨어 순서 / 스트리밍 응답 충돌 (부분 확인)

- #11107(§1-2)에서 falkben이 **컨텍스트 매니저 자원에 의존하는 `StreamingResponse`가 깨진다**고 실증한 게 확보된 최선의 직접 근거다 (2024-02-13).
- HN 44821541, twothreeone (2025-08-07)의 마지막 한 줄이 이 고통을 압축한다: *"Now tell me how to handle error cases during streaming.. >.<"*
- 미확보 리드(목록만): #10701 "StreamingResponse is returning all content at once", #11790 "RuntimeError: Response content shorter than Content-Length when using StreamingResponse", #9589 "High CPU usage of StreamingResponse", #8187 "Awaiting request body in middleware blocks the application", #7761 "How to get Response Body from middleware", #7319 "CORSMiddleware not work". `(확인 필요 — 목록만 확인)`
- **파일 업로드 메모리 문제**: `⚠️ 근거 못 찾음` — 이번 회차에서 직접 읽은 커뮤니티 스레드 없음.
- **OpenAPI 스키마 생성 실패**: `⚠️ 근거 못 찾음` — 단, §1-6의 "Swagger UI가 Maximum call stack size exceeded로 뻗는다"(#13455, 2025)가 인접 증거.

---

### 1-10. 프레임워크 변경이 생태계를 깨뜨린다 — 2026년 상반기 실사례 ✅ 【2차 회차 신설·최신】

> 이건 "FastAPI 자체의 버그"가 아니라 **0.x 프레임워크 위에 생태계를 얹었을 때 치르는 비용**의 실증이다. 대상 독자(Spring Boot의 하위호환 문화에 익숙한 사람)에게 가장 낯선 지점이라 별도 항목으로 뽑았다.

**사례: 라우터 구조 변경이 관측성 라이브러리를 깨뜨렸다**
- `trallnag/prometheus-fastapi-instrumentator` — FastAPI에서 Prometheus 메트릭을 뽑는 가장 널리 쓰이는 라이브러리. 이슈 3건이 **2026년 6~7월에 연달아** 터졌다:
  - **#370 "AttributeError: `'_IncludedRouter' object has no attribute 'path'`"** (작성자 bbrowning, **2026-06-14**, Closed)
    - 원인: 라우터 포함(include) 구조가 바뀌면서 라우트 객체가 `_IncludedRouter`로 감싸졌고, `.path` 속성을 무조건 접근하던 코드가 터졌다. 에러 발생 지점은 `routing.py`의 `_get_route_name()`.
    - 보고자가 기록한 환경: `prometheus-fastapi-instrumentator==7.1.0`, `fastapi==0.137.0`, `starlette==0.52.1`
    - PR #371로 수정됨.
    - https://github.com/trallnag/prometheus-fastapi-instrumentator/issues/370
  - **#379 "Incompatible with certain router usage in FastAPI 0.137.0+"** (작성자 BenDawes, **2026-06-25**, Closed)
  - **#388 "Issue with FastAPI 0.138"** (작성자 sbrunner, **2026-07-08**, Closed) — **한 번 고쳤는데 다음 마이너에서 또 터졌다.**
  - https://github.com/trallnag/prometheus-fastapi-instrumentator/issues?q=is%3Aissue+routes
- ⚠️ **fact-checker 필수:** 위 버전 번호들은 **이슈 본문에 보고자가 기록한 환경 정보**를 옮긴 것이다. "FastAPI 0.137.0에서 무엇이 바뀌었는가"를 책에 단정하려면 **릴리스 노트 1차 소스로 반드시 대조하라.** 커뮤니티 이슈는 "깨졌다는 사실"의 근거이지 "무엇이 어떻게 바뀌었는지"의 근거가 아니다.

**대조 사례: 커뮤니티 고통점이 프레임워크 기능으로 흡수되기도 한다 (긍정적 서사)**
- §1-2에서 본 #11107(2024-02, `yield` 의존성 정리 순서가 뒤집혀 커밋 전에 세션이 닫힘)은 이슈 **#11143**으로 승격됐고, 확인 시점 기준 **Closed** 상태다.
  - https://github.com/fastapi/fastapi/issues/11143
  - #11143 페이지에서 **해결 방식 자체는 확인하지 못했다** (병합된 PR·수정 내역이 페이지에서 보이지 않았다). `(확인 필요 — 종결 사유 미확인)`
  - 다만 §1-8의 #14137(2025-10)에서 tiangolo가 제시한 처방이 `Depends(func, scope="function")`이었다는 점, 즉 **의존성 정리 시점을 개발자가 고를 수 있는 파라미터가 생겼다는 점**은 확보된 사실이다. 이 계열 불만에 대한 프레임워크의 답이 `scope` 파라미터라는 서사는 **성립할 가능성이 높지만, 릴리스 노트로 확인한 뒤에 쓰라.**

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** 이 두 사례를 나란히 놓으면 0.x 생활의 양면이 나온다. **나쁜 쪽** — 마이너 버전이 생태계 라이브러리를 깨고, 고쳐도 다음 마이너에서 또 깨진다(#370 → #388, 3주 간격). **좋은 쪽** — 커뮤니티가 2년간 호소한 생명주기 문제가 실제로 API 파라미터로 흡수됐다. Spring Boot의 "메이저 아니면 안 깬다" 계약에 익숙한 독자에게는 **속도와 안정성을 맞바꾼 것**으로 설명해야지, 어느 한쪽만 보여주면 부정확하다.

---

## 2. Java(Spring)·Node(Express/NestJS) 개발자 관점의 대조 ← 이 책의 차별화 축

> **읽는 사람에게 미리 경고:** 이 섹션은 §1보다 근거가 얇다. Reddit·Stack Overflow가 막혀서 "Spring에서 왔는데 이게 없어서 당황했다" 류 스레드를 정면으로 못 캤다. **아래 있는 건 진짜지만, 없는 걸 채우지 마라.** 항목마다 근거 강도를 표시했다.

### 2-1. DI 컨테이너 vs `Depends` — 【근거: 중간】

**Spring/Rails 배경 개발자의 1인칭 증언 (가장 강한 단일 증거)**
- HN 44818249, **rmonvfer** (2025-08-06, "Litestar is worth a look" 스레드):
  > *"Thank you for writing this, I've been building a large backend with FastAPI for the last year or so and I've gone through all the levels of the purgatory. I began using the standard "tutorial" style and started cringing when I saw the official template place all CRUD operations in a single file (**I've been doing Rails and Spring for a while before**) and the way dependencies where managed... let's just say I wasn't feeling very comfortable."*
  - **핵심:** Spring/Rails를 하다 온 사람이 공식 템플릿을 보고 처음 느낀 건 "간결하다"가 아니라 **cringe**였다. 그리고 지목한 두 가지가 정확히 (1) CRUD를 한 파일에 몰아넣는 구조, (2) **의존성 관리 방식**이다.
  - 같은 사람의 결론: *"I wouldn't recommend it for anything serious. Sure, if you want to build a quick CRUD then go ahead... but keep in mind that its not built for complex applications (at least not without requiring you to write a framework on top, **like I've unfortunately done**)."*
  - https://news.ycombinator.com/item?id=44818249

**"Depends는 요청 스코프뿐"이라는 구조적 차이 — Spring 개발자가 가장 먼저 부딪히는 벽**
- §1-3의 GitHub #8054가 그 자체로 증거다. **Spring에서 빈은 기본이 싱글턴**이다. FastAPI로 오면 그 기본값이 없다:
  - dmontagu: 내장 캐싱은 **단일 요청 안에서만** 유효. 요청 간에는 안 된다.
  - 그래서 커뮤니티는 5년에 걸쳐 우회법을 쌓았다 — `lru_cache` → startup 인스턴스화 → `app.state` → `AsyncExitStack`+app state.
  - **그리고 이 스레드는 2026년 현재까지 Unanswered 상태다.**

**"진짜 DI 컨테이너가 없다"는 불만 — 이걸 증명하는 건 말이 아니라 라이브러리들의 존재다**
- `dishka`가 명시한 6대 한계(§1-3 전문 인용). 그중 Spring 개발자에게 직격인 건 4번:
  > *"You have to declare each dependency with `Depends` on each level of application. So either your business logic contains details of IoC-container or you have to duplicate constructor signatures."*
  - Spring의 `@Autowired`는 **생성자만 선언하면 컨테이너가 알아서 위까지 엮는다.** `Depends`는 그게 안 되므로 **호출 체인 전체에 `Depends`를 흘려보내야** 한다. 즉 "DI 컨테이너가 없다"의 정확한 의미는 **자동 와이어링(auto-wiring)이 없다**는 것이다.
  - dishka 비교표: FastAPI Depends는 **자동 와이어링 ❌, 컨텍스트 데이터 ❌, 동시성 안전성 ➖**.
  - dishka의 자기 규정: 앱 전체·단일 요청, 혹은 그보다 더 잘게 **원하는 만큼 스코프를 정의**할 수 있다 — *"many frameworks either lack scopes completely or offer only two"*. **Spring의 빈 스코프(singleton/request/session/prototype)에 대응하는 것을 되찾으려는 시도**로 읽어라.

**그에 대한 반론 — Python 진영의 "우린 그거 필요 없다"**
- `python-dependency-injector` 공식 문서 "DI in Python" (문서상 버전 4.49.1, 게시일 미확인)이 그 정서를 정리한다:
  - *"Originally dependency injection pattern got popular in languages with static typing like Java."*
  - *"There is an opinion that dependency injection doesn't work for it as well as it does for Java. A lot of the flexibility is already built-in."*
  - *"Also, there is an opinion that a dependency injection framework is something that Python developer rarely needs."*
  - *"Python developers say that dependency injection can be implemented easily using language fundamentals."*
  - https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html
- Lobsters linkdd(§1-3): `Depends`의 암묵적 마법이 **"Explicit is better than implicit"에 어긋난다**며, 정작 DI가 필요하면 `dependency-injector`가 더 파이썬답다고 주장. → **재미있는 역설:** Spring 개발자는 `Depends`가 **마법이 부족해서** 불만이고, Python 개발자는 `Depends`가 **마법이 과해서** 불만이다.

**Express·Spring Boot·FastAPI를 나란히 놓은 유일한 직접 비교 발언 (Node 개발자 시점)**
- HN 44816140, **com2kid** (2025-08-06, "How we made JSON.stringify more than twice as fast" 스레드) — ✅ 개별 item 페치로 작성자·날짜 확인함:
  > *"The difference with the Express ecosystem is that you aren't getting any less power than with FastAPI or Spring Boot, you just get less overhead. **Spring Boot has 10x the config to get the same endpoint up and running as Express, and FastAPI has at least 3x the magic.** Now some of FastAPI's magic is really useful (auto converting pydantic types to JSON Schemas on endpoints, auto generating API docs, etc), but it is still magic compared to what Express gets you."*
  - **축이 두 개라는 걸 정확히 짚었다: Spring Boot = 설정량, FastAPI = 마법량.** 이 책의 프레이밍으로 그대로 쓸 만하다.
  - 같은 댓글의 이어지는 대목이 **Node 개발자가 왜 FastAPI 배포에 답답함을 느끼는지**를 설명한다 — Node는 *"The scaling story of Node is also really easy to think about and do capacity planning for"*이며 경합·프로세스 간 통신을 걱정할 필요가 없다. **확장 단위가 그냥 프로세스 하나**라서 컨테이너에 담아 k8s에 얹으면 끝이다.
  - 결론 문장이 §3의 "배터리 포함이냐 조립이냐" 논쟁 전체에 대한 반대 진영 요약으로 쓸 만하다:
    > *"having one really damn simple and easy to understand building block is more powerful than having 500 blocks that can be misconfigured in ten thousand different ways."*
  - **여기에 §1-4를 겹쳐 읽어라.** Node 개발자가 당연하게 여기는 "확장 단위 = 프로세스 하나"가 FastAPI에서는 **워커 수·스레드풀 상한·OS 스케줄러·gunicorn 여부가 얽힌 결정**이 된다. 이게 Node 배경 독자가 부딪히는 첫 벽이다.
  - https://news.ycombinator.com/item?id=44816140
  - ※ 인용문 자체는 Algolia 코멘트 인덱스에서 취득한 텍스트다. 개별 item 페치로는 작성자·날짜·논지를 확인했다. **글자 그대로 인용할 거라면 fact-checker가 원문 대조할 것.**

### 2-2. Bean Validation(JSR 380) vs Pydantic — 【근거: **강함** (2차 회차에서 확보). 단 커스텀 검증기 각도만 여전히 공백】

> **1차 회차에서는 "근거 없음"이었다.** 2차 회차에서 두 갈래로 뚫렸다: (1) **에러 응답 포맷 논쟁**(FastAPI의 422), (2) **Java 배경 개발자가 Pydantic 코드베이스를 만났을 때의 반응**. 반면 **커스텀 검증기 비교는 4개 경로로 시도해 전부 0건** — 그건 아래에 그대로 남겨뒀다.

#### (1) 에러 응답 포맷: FastAPI의 422 vs Spring의 400/`ProblemDetail` — 7년째 진행 중인 논쟁

**정전(canonical) 스레드 — 왜 400이 아니라 422인가**
- GitHub fastapi/fastapi issue **#643 "Why status 422 instead of 400 when invalid (header, query, etc.) parameters in the request?"** (작성자 yiannis-kt, **2019-10-22**, 댓글 10, 리액션 8)
  - 최초 문제 제기: *"I was wondering what are the reasons for such choice instead of the most common 400 status code. It seems to me a bit strange, especially in the case where a required header is missing, as I would think this classifies as a syntactic error"*
  - **tiangolo의 답변 (2019-10-30, 리액션 13 — 이 이슈 최다):** 근거 네 개를 명시적으로 제시한다.
    > *"The difference between 422 and 400 becomes a bit subjective. The rationale is that the error is not about using the protocols and languages incorrectly (HTTP, JSON) nor about doing something otherwise not allowed or incorrect (like performing an operation without enough privileges), but about **sending invalid contents, even though using the correct content format (JSON) through the correct channel (valid HTTP)**. But I acknowledge that the election between 422 vs others is interpretable and subjective. The second reason is that **Flask-apispec with Marshmallow used 422 too**, I thought that was a good idea. And the other advantage is that you can then **separate a whole class of errors, validation errors, that are created automatically by your FastAPI app**... And then you can raise 400 errors in your own code, and know that those 400 errors will be something specific that you raise."*
  - **정면 반박 — antonagestam (2022-02-08):**
    > *"This is the problem, the format here is not simply JSON, but a rich OpenAPI schema. I see no reason why violating that schema, which is clearly the contract for interacting with the API, is not a client error... interpreting sending a string instead of a number as 'the syntax of the request entity is correct' seems like a far fetch."*
  - **절충안 — Jaza (2022-12-06):** 구문 오류와 의미 오류를 나누자. *"I don't mind the fact that FastAPI returns 422 when the request body contains syntactically valid JSON but fails pydantic validation. However, I think that it really should return 400 when the request body contains syntactically invalid JSON."* (직접 판별 헬퍼 코드를 붙임)
  - https://github.com/fastapi/fastapi/issues/643

**진짜 실무 고통은 상태 코드가 아니라 "바꾸면 문서가 안 따라온다"는 것** ✅
- 같은 스레드, yusra-haider (**2019-10-31**, 리액션 5):
  > *"The only issue with this approach in the docs is that **auto-generated documentation doesn't reflect the updated status code.** The second issue, perhaps a more pedantic one, is that I also have to define the response structure again, when all I want to do is change the status code."*
- PhilippeGalvan (2020-09-03): 같은 문제로 막혔고, *"fastapi is really nice and I'm trying to convince a client to use it and **auto-doc is a key argument!**"* → **자동 문서가 셀링 포인트인데 그게 커스터마이징을 막는다는 역설.**
- GitHub fastapi/fastapi issue **#1376 "Allow customization of validation error"** (작성자 johanfleury, **2020-05-04**, 리액션 15) — **5년 넘게 각자 해킹한 우회법 전시장이 된 스레드다.**
  - johanfleury (2020-05-06, 리액션 3), 예외 핸들러로 되지 않냐는 답에: *"Well it works regarding what's produced by the API, but **it doesn't regarding documentation**."*
  - **akrejczinger (2020-06-09) — 프레임워크 소스를 고쳤다는 고백:** *"HTTP 422 is hardcoded in openapi/utils.py. **I solved my issue for now by modifying the FastAPI source code itself**, but a proper way to do this automatically using the exception handlers would be preferable."*
  - kissgyorgy (2021-01-14): *"I would like this feature too, because **it took more time to make it work than I wanted to** 😞"*
  - ushu (2021-01-07, 리액션 9): `fastapi.openapi.utils`의 `validation_error_response_definition`을 **모듈 전역 변수째 덮어쓰는** 우회법.
  - Acerinth (2021-04-28, 리액션 7 — 이 이슈 댓글 최다): 상태 코드만 400으로 바꾸고 기본 응답 스키마와 OpenAPI 문서는 유지하려면 → **Pydantic 모델 재정의 + 예외 핸들러 + `custom_openapi()` 3단 조합**이 필요하다며 코드를 붙임.
  - Kludex (2020-09-02, 리액션 3), 메인테이너 측 현실적 제안: *"The solution that would require less work and have bigger chances on being approved... is creating a flag to not add the 422 response in the swagger documentation."*
  - https://github.com/fastapi/fastapi/issues/1376
- GitHub fastapi/fastapi Discussion **#6695 "How to disable the default 422 doc"** (작성자 Jedore, **2021-06-29**, upvote 3)
  - 결론 (2021-07-15): *"My solution is **inheriting `FastAPI` class and rewrite `openapi` method**."*
  - vanntile (2022-07-27)가 문제를 가장 정확히 요약: 핸들러를 오버라이드해도 *"422 is still in the OpenAPI"*.
  - ※ 이 스레드 후반부는 무관한 주제로 흐른다. 인용 가치는 Jedore·vanntile 구간뿐.

**RFC 7807 / RFC 9457 (Problem Details) — Spring `ProblemDetail` 독자에게 직결되는 7년짜리 미해결 아크** ✅
- issue **#512 "Support RFC 7807 error handling"** (작성자 daigok, **2019-09-07**)
  - **tiangolo (2020-06-10) — 이후 6년을 규정한 문장:** *"In FastAPI the main change would be to move `detail` to be a `str` description of the error and add another field with the structured error object... **I haven't wanted to do it as it would break backwards compatibility**, but maybe in the future, I end up doing it 🤷 🤓"*
- Discussion **#14517 "RFC 9457 Based Error Responses"** (작성자 walter9388, **2025-12-13**, upvote 6)
  - *"It would be good to implement errors based on RFC 9457... **This is a breaking change and therefore should be opt in** behaviour."* 앱/라우터/라우트 3단 opt-in 제안. 본문에서 같은 요청이 이전에도 두 번 나왔음을 스스로 링크한다.
  - yakubka (**2026-07-05**): *"RFC 9457 defines a standard JSON structure for HTTP error responses with `type`, `title`, `status`, `detail`, and `instance` fields. **FastAPI does not implement this automatically**, but you can wire it up with a custom exception class and handler."*
- PR **#15951** (작성자 bigmikecreates, **2026-07-07 제출, 같은 날 미머지 상태로 close**)
  - ⚠️ **기술적 반려가 아니라 프로세스 사유다.** YuriiMotov (2026-07-07): *"let's keep it closed until maintainers can review the discussion and decide that we are going to add this feature... We are trying to keep things clean and ask to open PRs only when it's explicitly requested by maintainers."*
  - PR 본문에 저자가 AI 생성임을 명시했다(*"AI Disclaimer"*).
- **책에 쓸 때 정확한 표현:** 2026-07-25 현재 FastAPI 코어에 RFC 9457 Problem Details 지원은 **없다.** 2019년(#512) → 2025년(#14517) → 2026년(#15951, 미머지)으로 **7년째 열려 있는 요청**이다. **"지원한다"거나 "거절됐다"로 쓰면 둘 다 틀린다.**
- ⚠️ fact-checker: 위 세 항목의 현재 상태는 저술 시점에 재확인할 것. 특히 `validation_error_response_definition`이 아직 그 위치에 하드코딩돼 있는지는 **커뮤니티 진술이므로 현행 소스 대조 필수.**

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** Spring Boot 3의 `ProblemDetail`은 표준(RFC 9457) 에러 포맷을 **프레임워크가 1급으로 제공**한다. FastAPI에서 같은 걸 하려면 예외 핸들러를 직접 쓰고, 그러면 **자동 생성 OpenAPI 문서가 거짓말을 하기 시작한다.** 그래서 사람들이 `custom_openapi()`를 덮어쓰거나 `FastAPI` 클래스를 상속하거나 모듈 전역 변수를 몽키패치하거나 **프레임워크 소스를 직접 고쳤다.** FastAPI의 최대 셀링 포인트(자동 문서)가 커스터마이징의 최대 장벽이라는 게 이 절의 핵심 아이러니다.

#### (2) Java 배경 개발자가 Pydantic을 만났을 때 — 실제 반응

**★ 최고의 오프닝 재료: Java 개발자가 파이썬 서비스를 인수했을 때** — hiram112 (HN, **2021-12-04**)
> *"Funny, I took over a modern python service and I was pretty shocked at what I inherited. Long gone are the days of 'There's one way to do things'. Instead, **this thing would give the most 'enterprisey' Spring JEE application a run for its money with its endless annotations, dependency injection magic, all sorts of pseudo-types** — both the 'built-in' Python 3 ones like Set and List, but also the libraries like Pydantic. **But unlike Java, these types aren't even really guaranteed by the language at compile time**, so even if your IDE plugin can successfully detect them, things will still (silently) slip through at runtime."*
- 바로 달린 반박: *"This sounds like what happens when **a bunch of Java/C# developers jump over to python without learning the 'python way'** — this is more related to the developers than the project"*
- https://news.ycombinator.com/item?id=29444847
- 🕒 2021년 글. **생태계 서술이 아니라 인지 충돌의 기록으로만 써라.** 이 반박 쌍은 그 자체로 이 책의 존재 이유다 — *"Java 개발자가 파이썬 방식을 안 배우고 넘어오면 이렇게 된다."*

**JSR-380을 직접 거론한 유일한 발언** — duncanfwalker (HN "Keep Pydantic out of your Domain Layer" 스레드, **2025-07-27**)
> *"Validation rules are like an extension to the type system... **In Java they got around the external-dependency-in-the-core-model problem by making the JSR-380 specification that could (even if only in theory) have multiple implementations.**... I get that principled terms it's not right but, if those libraries change on API on a similar cadence to the programming language syntax, then it doesn't impact in practical terms. **It's these kind of pragmatic compromises that distinguish Python from Java - after all, 'worse is better'.**"*
- https://news.ycombinator.com/item?id=44701062
- **JSR-380이 왜 스펙으로 만들어졌는지(구현 교체 가능성 = 코어 모델의 외부 의존성 격리)를 정확히 짚고, Pydantic은 그 문제를 "실용적으로 무시한다"고 정리한다.** §2-2의 이론적 뼈대로 그대로 쓸 수 있다.

**같은 스레드(2025-07-23, 94점/121댓글)의 나머지 — Java 진영과 Python 진영이 정면으로 붙는다**
- **microflash (2025-07-26)**, "레이어마다 모델을 나눠라"에 대한 Java 측 반론: *"For many cases, we don't do these kind of things in Java; **a single annotated record can function as a model for both data and API layers.** Regardless of the language, the distinction becomes important when these layers diverge or there's some sensitive data involved."*
  - **주목:** §3-5(SQLModel 논쟁)에서 "API 모델과 DB 모델을 나눠라"가 다수설이었는데, **Java 개발자는 오히려 "우린 어노테이션 붙인 record 하나로 둘 다 쓴다"고 말한다.** 통념과 반대다.
- **IshKebab (2025-07-26):** *"This seems ridiculously over-complicated. **This guy would *love* Java.** He doesn't even say *why* you should tediously duplicate everything instead of just using the Pydantic objects"*
- **throwaway7783 (2025-07-26):** *"Return of Java DTOs!"*
- **skissane (2025-07-26)** — Java에서 Python으로 넘어온 실무자의 회고: POJO 값 클래스 층 + ORM 객체 층 + 수작업 매퍼, 거기에 Swagger 생성 클래스와 또 다른 매퍼까지 있었다며 — *"Now I mainly do Python and **I don't see that kind of boilerplate duplication anywhere near as much as I used to.**"*
- **rtpg (2025-07-26)** — 타입 어노테이션 기반 접근의 한계를 가장 정확히: *"To be fair I do think that **Pydantic leaning into the type annotation story is nice.** If you're really going lean or performant the restrictions work well in your favor. Just like… for the bog standard B2B SaaS the expressivity tradeoff just doesn't feel worth it. Right now Pydantic for me is like '**you can validate a straightforward data structure! Now it's up to you to actually build up a useful data structure from the straightforward one**'. Other tools give me both in one go."*
- **zo1 (2025-07-26)** — 문화적 반발: *"it **immediately sets your type system to go down the path of Java and Typescript**... This is not the python way, and is frankly part of its secret sauce."*
- **mattmanser (2025-07-26)** — DTO 남발 자체가 문제: *"It's a pattern that rapidly leads to tons of DTOs that endlessly repeat exactly the same properties... The worst one I've seen was when to add one property I had to edit 40 files... **It's anti-patterns like that which give statically typed languages a bad name.**"*
- 스토리: https://news.ycombinator.com/item?id=44656419

#### (3) 에러 메시지 커스터마이징 — 인접 근거 (⚠️ Java 비교 아님)

- pydantic/pydantic Discussion **#8468 "Add custom validation error message to pydantic types"** (작성자 Spenhouet, **2024-01-02**, **upvote 17**)
  > *"Pydantic types like StringConstraints output generic validation error messages based on the provided constraints. **The resulting validation error messages can be very unhelpful and can not be used to show to any user.**"* → 예시로 정규식이 통째로 노출되는 에러 문자열을 들며 *"**That isn't useful for the user nor the developer.**"*
  - 답변(uriyyo, 2024-01-04, upvote 5)은 전용 API가 아니라 `WrapValidator` + 예외 팩토리 조합 **우회 레시피**.
  - 본문에서 같은 요청이 이미 한 번(#2758) 나왔음을 밝힌다.
  - https://github.com/pydantic/pydantic/discussions/8468
- Java의 `@Size(message = "...")`처럼 **필드마다 메시지를 다는 게 1급 기능**인 것과 대비되는 지점이라 서술 소재로 좋다.
- ⚠️ **단, 이 스레드에 Java·Spring 언급은 한 줄도 없다.** "커뮤니티가 Java와 비교했다"로 쓰면 왜곡이다. 대비는 저자가 하는 것이다.

#### (4) ⚠️ 여전히 근거 없음: 커스텀 검증기 비교 (`ConstraintValidator` vs `field_validator`)

**4개 경로를 시도해 전부 0건이다.** ① `repo:pydantic/pydantic field_validator model_validator in:title` → 0건 ② GitHub 전체 `ConstraintValidator pydantic` → 무관한 리포만 ③ HN Algolia `ConstraintValidator` → **nbHits 0** ④ HN Algolia `pydantic hibernate validator` → **nbHits 0**

**해석:** Java 커뮤니티와 Python 커뮤니티가 각자 자기 도구 안에서만 검증기를 논하고, **둘을 직접 비교하는 공개 토론 자체가 형성돼 있지 않다.** 이 각도는 **저자의 1차 비교 서술**로 채우거나, (3)의 pydantic #8468을 우회 근거로 쓰되 "커뮤니티가 직접 비교한 건 아니다"를 명시해야 한다. **없는 스레드를 만들지 마라.**

#### (5) 인접 근거 (1차 회차 수집분)

- **API 모델과 DB 모델을 분리할 것인가** (§3-5) — HN 44821476, globular-toast (2025-08-07):
  > *"Am I the only one who prefers to just have separate models for API and database right from the start? I know it _looks_ not DRY, but it is. Your API and your database schema are not the same thing."*
  - **위 (2)의 microflash 발언과 정면으로 놓고 읽어라** — Python 진영에서 "분리하라"가 다수설인 반면 Java 진영은 "record 하나면 된다"고 말한다. **통념("Java는 계층을 나누고 Python은 간단히 간다")과 정반대라 챕터 소재로 강력하다.**

### 2-3. 서블릿 스레드 모델 vs asyncio 이벤트 루프 — 【근거: 갈래별로 다르다 — Node 전환 **강함** / virtual threads 대조 **매우 강함** / WebFlux 전환 **없음** / 출신 귀속 **없음**】

**가장 자주 저지르는 실수는 이미 §1-1에 있다.** Spring MVC의 서블릿 스레드 풀에서는 스레드 하나가 블로킹돼도 다른 스레드가 요청을 계속 받는다. **그 직관을 그대로 가져와 `async def` 안에서 동기 호출을 하면 전체가 멈춘다.**

- 실무에서 sync를 못 버리는 이유의 실제 사례 — GitHub #8433 (2022-12-08): **asyncio를 지원하지 않는 Snowflake SQLAlchemy 드라이버.** Java 진영이 JDBC로 대부분 커버되는 것과 대비된다.
- 한국 개발자의 같은 관찰 — velog, 고은연 **"FastAPI 써 본 후기"** (2022-01-07):
  - *"파이썬은 기본적으로 동기로 동작하고, 많은 라이브러리가 비동기를 지원하지 않는다"* — SQLAlchemy조차 특정 버전에 와서야 비동기를 지원하기 시작했다고 지적. 🕒 **2022년 글이므로 생태계 성숙도 서술은 현재형으로 쓰지 마라.** 다만 "동기 라이브러리가 기본값인 언어에서 비동기 프레임워크를 쓴다"는 **구조적 긴장은 여전히 유효**하다.
  - https://velog.io/@koeunyeon/FastAPI-써-본-후기
- **같은 관찰의 2026년판 (한국, 최신)** — shipfriend.dev, 서정우 **"FastAPI는 왜 사용하는 걸까? 강점과 약점"** (**2026-03-28**)
  - 약점 1, 생태계: *"비동기를 지원하지 않는 라이브러리를 함께 사용하는 순간 비동기의 이점이 사라진다"* — 동기 ORM·DB 드라이버를 쓰면 이벤트 루프가 블로킹된다고 명시.
  - 약점 2, GIL: *"CPU 집약적인 작업(이미지 처리, 대용량 연산 등)에서는 멀티스레드를 써도 병렬화가 되지 않"*는다.
  - **Spring Boot·NestJS와 나란히 놓은 비교표**가 있고, DB 쿼리가 낀 시나리오에서 FastAPI 성능이 떨어지는 경향을 지적 — §3-6의 #7320에서 dbanty가 2020년에 한 분석과 **방향은 반대인데 주제는 같다.** (dbanty: DB가 끼면 FastAPI가 유리 / 이 글: DB가 끼면 불리)
  - ⚠️ **비교표의 응답시간·메모리 수치는 출처와 측정 조건이 확인되지 않았다. 절대 인용하지 마라.** 인용해도 되는 건 **약점 서술 두 개**뿐이다.
  - https://shipfriend.dev/posts/why-use-fastapi-strengths-and-weaknesses
  - ✅ **2026년 한국어 자료라 §2-3의 신선도 문제를 해결한다.** 2022년 velog 글의 "생태계가 아직 안 됐다"는 서술을 현재형으로 못 쓰는 대신, 이 글로 **"2026년에도 같은 구조적 긴장이 지적된다"**고 쓸 수 있다.
- **워커 모델 대조 (§1-4):** Spring Boot는 JVM 하나 안에서 스레드 풀로 병렬성을 얻는다. FastAPI는 **프로세스를 몇 개 띄울 것인가**가 곧 병렬성 결정이고, 그 숫자를 정해주는 공식 권고가 없다. Kludex의 *"Gunicorn relies on the operating system to provide all of the load balancing"*은 Java 개발자에겐 낯선 답변이다 — **"그건 프레임워크가 아니라 OS가 정한다"**.

---

#### ★ 2차 회차 핵심 발견: "Java는 함수 색칠 없이 이 문제를 풀었다"가 **Python 내부의 공식 의제**다

이 책의 독자에게 던질 수 있는 가장 강한 사실이다. Java 개발자가 밖에서 야유하는 게 아니라, **CPython 코어 개발자가 Python 안에서 같은 말을 하고 있다.**

- discuss.python.org **"Add Virtual Threads to Python"** — 작성자 **Mark Shannon** (CPython 코어 개발자, Faster CPython 팀), **2025-05-09** 게시, 마지막 확인 글 2026-02-14. **274 posts / 22,050 views / 565 likes**
  > *"tl;dr — **Java has virtual threads. Virtual threads are a better way of doing concurrency than Python's async and await. We should add virtual threads to Python**… Unlike Python's coroutines, virtual threads: do not divide the language in two 'colors'. See What color is your function? … IMO, virtual threads offer a superior programming model to adding async and await all over your code and having to duplicate all your libraries."*
  - 지지 — **Tin Tvrtković(Tinche, `aiofiles`·`pytest-asyncio` 저자)**, 2025-05-10: *"I'm completely on board with this idea. I think in a nogil world function coloring doesn't make sense in the long term… If we want to avoid function coloring, normal threads need to at least approximate the idea of cancellability too. Otherwise, we still have function coloring, but hidden, which I think is objectively worse."*
  - **Java 유경험자의 요구사항 (2026-02-14, vitaly.krug)** — 이 책의 독자가 정확히 할 말이다:
    > *"For me, Virtual Threads are worth doing if they solve the following problems, at minimum: Ability to use existing 'blocking' code AS IS, including 3rd-party packages… This has long been the biggest limitation of asyncio - there are many packages that don't have asyncio twins - and such multi-color development overhead is truly unwarranted because **Java's Virtual Threads support has already proven that it's both possible and practical to abstract all that inside the runtime layer.**"*
  - arpitgahlot (2025-08-04): *"'colored' functions cause me a lot of trouble. **I have no hope for Django becoming fully async.** I have never found a language that did not benefit from adding virtual threads. Fibers(Ruby), Virtual threads(Java), Coroutines(Kotlin, Go) are all excellent implementations."*
  - hlovatt (2025-09-05): 색칠 없음 + 에러 전파 + **취소(cancel)의 존재와 전파**를 Java 방식의 장점으로 꼽음.
  - **반론도 있다 (한쪽으로 쓰지 마라)** — Liz (2025-05-10): *"It seems like one which could make sense for a new language, but if the only benefit is avoiding function coloring, we will still have it from async/await."* / Rosuav (2025-08-02): *"I'm still very confused as to what 'virtual threads' are. They seem to be … just threads."*
  - Kotlin/Swift 배경의 정리 — andersio (2025-08-03): Kotlin은 **선언부에만 색칠(`suspend`)하고 호출부에 `await`를 요구하지 않으며** IDE가 중단점을 표시한다. 그리고 *"Separate the discussion on async-await the language syntax… from asyncio the implementation (single threaded event loop)"* — **문법과 런타임을 분리해서 논하라**는 지적.
  - https://discuss.python.org/t/add-virtual-threads-to-python/91403

- HN **"What async promised and what it delivered"** (**2026-04-22**, 256점/307댓글) — 가장 최신 대형 논쟁
  - brazzy (2026-04-22): *"It forces programmers to learn completely different ways of doing things, makes the code harder to understand and reason about, purely in order to get better performance. Which is exactly the wrong thing for language designers to do... **And the designers of Go and Java did just that.**"*
  - ysleepy (2026-04-25): *"Java has gone full circle. Java had green threads in 1997, removed them in 2000 and brought them back properly now as virtual threads. I'm kinda glad they've sat out the async mania... **the async stuff just feels like lipstick on a pig. Debugging, stacktraces etc. are just jumbled.**"*
  - time4tea (2026-04-25): *"It uses N:M threading model - where N virtual threads are mapped to M system threads and its all hidden away from you. **All the other languages just leak their abstractions to you, java quietly doesn't.**"*
  - https://news.ycombinator.com/item?id=47859442

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** Java 독자에게 정직하게 말할 수 있는 건 이거다 — **"당신이 Loom으로 얻은 걸 파이썬은 아직 못 얻었고, 파이썬 코어 개발자들도 그걸 안다."** FastAPI의 `async def`는 언어가 준 최선이지 이상적 해법이 아니다. 이 프레이밍은 (1) 독자의 기존 지식을 존중하고, (2) FastAPI를 과대선전하지 않으며, (3) §1-1의 블로킹 규율이 왜 **영구적 부담**인지 설명해준다.

---

#### Node/JS 개발자는 더 쉽게 넘어오는가 — 【양방향 근거 확보】

**"더 쉽다" 쪽**
- **jongjong** (HN, **2025-09-02**): *"JS had a smooth on-ramp to async/await thanks to Promises. Promises/thenables gave people the time to get used to the idea of deferred evaluation via a familiar callback approach... **People in the Node.js community were very aware of async concepts since the beginning and put a lot of effort in not blocking the event loop.**"* — https://news.ycombinator.com/item?id=45109610
- **markandrewj** (2025-09-03): *"Understanding the difference between blocking and non-blocking code is also a concept relevant to Python. **In Node it's one of the concepts you are first introduced to, because Node is single threaded by default.**"* — https://news.ycombinator.com/item?id=45115260
- **seabrookmx** (2026-05-26): *"Every developer at my company is comfortable with this pattern, and **frameworks like FastAPI make this a similarly smooth experience when using Python.**"* — https://news.ycombinator.com/item?id=48283494

**"오히려 물린다" 쪽 — 이쪽이 더 구체적이다**
- **leonidasv** (2026-05-27): *"The Node world was built with asynchronicity in mind... But if you take Python (for example), **it's a shitshow. You usually have two versions of the same API, split by function name, client, package, or namespace: `foo` and `afoo`**… It's a pain to develop for, to maintain, to scale, everything."* — https://news.ycombinator.com/item?id=48289232
- **rtpg** (2026-05-27): JS는 사실상 "전부 async"로 통일해 라이브러리 저자가 감출 수 있지만, *"Python libs tend to have much larger API surfaces due to how OOP works. So async-y internals works are harder to isolate cleanly without breaking the public API. But if you make your API 'async-first' then **the debugging experience in Python is miserable (try pdb'ing your way through awaitables....)**"* — https://news.ycombinator.com/item?id=48288018
- **honeyryderchuck** (Lobsters, 2023-06-11) — 역설적 진단: *"Explicit async/await based functional coloring is the worst API for managing concurrent I/O. **It works for javascript because there's nothing else, so zero chances of paradigm interference.**"* → **JS가 편한 건 잘 설계돼서가 아니라 대안이 없어서다.** 파이썬은 동기 생태계가 공존하기 때문에 오히려 충돌한다.
- **TZubiri** (2025-09-02) — Node 출신 주니어가 파이썬에서 *"writing Node like code in python, and it was of course a mess"* → *"you are better off learning the native way of a language instead of trying to shoehorn other abstractions"* — https://news.ycombinator.com/item?id=45108327
- **forestj** (Lobsters, 2023-06-11): psycopg2·pymysql·redis-py가 안 되거나 별도 async 구현을 둬야 한다며 — *"**yes, I too hate asyncio and its ilk, and its one of the main reasons I use node.js or golang for most projects these days**"*

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** "Node 개발자는 이벤트 루프를 이미 알아서 유리하다"는 **절반만 맞다.** 개념은 유리하지만 **생태계는 불리하다.** JS는 동기 I/O 라이브러리가 사실상 없어서 색칠 문제가 드러나지 않는 반면, 파이썬은 동기 라이브러리가 다수이고 그게 §1-1의 사고를 만든다. Node 독자에게 줄 경고는 "이벤트 루프를 다시 배워라"가 아니라 **"당신이 JS에서 한 번도 확인할 필요 없던 것 — 이 라이브러리가 논블로킹인가 — 을 매번 확인해야 한다"**이다.

#### Spring WebFlux / Reactor 경험자는 어떻게 느끼는가 — 【⚠️ 여전히 근거 없음】

- **Reactor/Mono/Flux를 써본 사람이 Python asyncio로 옮겨가 비교한 게시물을 단 한 건도 찾지 못했다.** 시도한 경로: HN Algolia `webflux`(2,205건 중 상위 40건 전수 확인), `reactive asyncio`, `rxjava python`, `webflux python`, `Mono Flux reactive java`, `project reactor java`, `WebFlux reactor` → **교차 경험담 0건.** `webflux python` 결과는 사실상 전부 채용 공고에 두 기술이 나란히 적힌 것이었다. fastapi/fastapi Discussions `webflux` 검색 → **0건.**
- **대신 확보한 건 Java 내부의 Reactor 회의론이다.** ⚠️ **이건 asyncio 대조가 아니다. "Java 진영에서도 Reactor는 이미 회의적"이라는 배경으로만 써라.**
  - jen20 (2026-04-26): *"Every Java codebase using something like Flux serves as a datapoint in favor of this argument - **they're an abomination to read, reason about or (heaven help) debug.**"*
  - rwoerz (2026-04-26): *"They stopped at the Promises level with CompletableFuture that lead to '**colored frameworks**' like WebMVC vs. WebFlux in Spring."* — **Spring 안에도 색칠 문제가 있었다**는 지적이라 대조축으로 유용하다.
  - jryan49 (2025-06-04): *"I can tell you as a person working in a spring boot webflux shop that is pretty bad code… **the dx is garbage.**"*
  - okeuro49 (2025-06-04): *"**With virtual threads it's difficult to see WebFlux being used in new projects.**"*
  - unscaled (2025-10-28): Reactive를 쓴 진짜 이유는 우아함이 아니라 *"threads were too expensive"*였고 `Mono<T>`는 결국 *"CompletableFutures with better ergonomics"*라는 정리.
- **유일하게 두 모델을 다 써본 증언 — 단, Python은 아니다.** gombosg (2022-04-16): Spring MVC·WebFlux·Scala Futures·TS async/await·Angular observables를 모두 써본 뒤 *"**nothing beats async/await in terms of syntax simplicity. I miss them from Java & Scala!**"* — ⚠️ **그가 말한 async/await은 TypeScript이고 Python asyncio가 아니다. 이걸 angle 1의 답으로 쓰면 왜곡이다.**

#### 서블릿 스레드 모델 출신의 실수 — 【현상은 풍부, 출신 귀속은 빈약】

- **중요한 구분:** "`async def` 안에 블로킹 호출을 넣는다"는 실수 자체는 §1-1에서 충분히 문서화됐다. 그러나 **글쓴이가 "나는 Spring MVC / 스레드-퍼-리퀘스트 세계에서 왔다"고 밝힌 사례는 확보하지 못했다.** 책에서 이 실수를 **"Java 개발자가 이렇게 실수한다"고 귀속하지 마라.** "커뮤니티가 반복 보고하는 실수 패턴"으로 쓰고, 그것이 스레드 모델 직관과 충돌한다는 설명은 저자의 해석으로 표시하라.
- provenance에 가장 근접한 두 건:
  - **toast0** (2025-09-02): *"as a naive developer who is **used to real threads and green threads**, I expected there would be some wa[y] to await on a real thread and all the async stuff would just happen... but instead, **if you await, actually you've got to be async too.**"* — https://news.ycombinator.com/item?id=45110028
  - **layer8** (2026-04-25) — 스레드풀 세계관의 정면 반론: *"Server applications don't spawn threads per request, they use thread pools. The extra context switching due to threads waiting for I/O is **negligible in practice for most applications**. Asynchronous I/O becomes important when the number of simultaneous requests approaches the number of threads you can have on your system. **Many applications don't come close to that in practice.** There's a benefit in being able to code the handling of a request in synchronous logic."* — https://news.ycombinator.com/item?id=47905032 → **§3-1(sync vs async) 논쟁의 관점 A에 그대로 넣을 수 있는 가장 좋은 논거다.**
- **왜 async 장애가 디버깅이 어려운가 — 4단계 시나리오** (acdha, **2026-04-26**, https://news.ycombinator.com/item?id=47912719):
  > *"1. Request one hits an await in foo() 2. Runtime switches to request two in bar() until it awaits 3. Runtime switches to request three in baaz(), **which blocks the loop for a while** 4. Request one gets a socket timeout or expired API key — **That error in #4 does not tell you anything about #2 or #3**… If it was a thread, you would either not have the problem at all, it would show up clearly in request three"*
  - **에러가 범인과 다른 요청에서 터진다.** §1-1의 "부하가 걸려야 드러난다"에 이어, **"터져도 엉뚱한 데서 터진다"**를 설명하는 최고의 재료다. 챕터 소재로 강력.
- 관련 실전담 (같은 스레드 계열): **acdha (2026-04-26)** — Node 팀에서 메인 루프가 막혀 API 호출이 타임아웃되거나 서명 만료로 인증 에러가 나는데, *"there are hundreds of places which have to be checked whereas if it was threaded this class of error either wouldn't be possible or would be limited to the same thread"* — https://news.ycombinator.com/item?id=47906735

### 2-4. Maven/Gradle/npm vs uv/pip/poetry — 【근거: 약함】

- 확보한 유일한 직접 언급: HN 44821077, devjab (2025-08-07)이 Litestar 선택 이유로 든 것 중 **"really fast cold start"** — 빌드·기동 특성이 선택 기준으로 언급된 사례.
- Lobsters, koala (Django vs FastAPI 스레드, ≈2025): Django 초기 셋업을 매끄럽게 만들려고 **uv**를 포함한 보일러플레이트를 손보는 중이라고 언급 — uv가 2025년 시점 Python 진영의 현실적 선택지로 커뮤니티에 등장했다는 정황 증거.
- ⚠️ **락파일·모노레포 경험 차이를 다룬 근거는 못 찾았다.**

### 2-5. Spring Security vs 직접 조립 — 【근거: **강함** (2차 회차에서 확보)】

> **1차 회차에서는 "근거 못 찾음"이었다.** 접근을 바꿔서 찾았다 — "Spring에서 온 사람의 소감"이 아니라 **"직접 조립한 부품이 실제로 썩은 사건"**을 찾으니 나왔다. **이게 이 책에서 Spring Security 대조를 쓰는 가장 정직한 방법이다.**

#### 실제로 벌어진 일: 공식 문서가 추천하던 보안 라이브러리 두 개가 방치됐다

Spring Boot를 쓰면 암호 해싱·JWT 처리는 Spring Security가 관리하는 의존성 안에 있고, **"이 라이브러리 아직 살아 있나?"를 개발자가 묻지 않는다.** FastAPI에서는 그걸 직접 골라 조립한다. 그리고 **골라놓은 부품이 썩었다.** 커뮤니티가 그걸 발견해서 신고했고, 문서가 바뀌기까지 걸린 시간이 기록으로 남아 있다.

**사건 1: JWT 라이브러리 (`python-jose`)**
- GitHub fastapi/fastapi Discussion #9587 **"Why `python-jose` is still recommended in the documentation when it is nearly abandoned."** (작성자 p4perf4ce, **2023-05-29**, Answered)
  - 최초 문제 제기: 문서가 여전히 `python-jose`를 권하는데 이미 방치됐고 최신 Python에서 임포트 에러가 난다. 원래 추천 사유였던 *"all the features from PyJWT plus some extras"*가 더 이상 성립하지 않는다.
  - **Stefan Hoelzl (2024-02-05):** 의존성 사슬에 보안 취약점이 있다고 지적 — 특히 `ecdsa`의 미수정 취약점 때문에 cryptography 백엔드를 쓰더라도 위험이 남는다.
  - **estebanx64 (2024-04-23, 공식 답변):** 마지막 릴리스가 2021년이라는 것과 보안 문제를 인지하고 있으며, *"a better library with active development"*로 문서를 갱신하겠다고 확약.
  - **결말 (2024-05-20):** PR #11589로 문서가 **PyJWT**를 쓰도록 변경. estebanx64: *"We decided to move forward with PyJWT instead python-jose."*
  - https://github.com/fastapi/fastapi/discussions/9587
- GitHub fastapi/full-stack-fastapi-template Discussion #1188 **"Python-Jose abandoned - use authlib or other instead?"** (작성자 SpoonOfDoom, **2024-04-29**, upvote 5)
  - > *"it seems that Python-Jose has been abandoned for a while, and now **CVEs have been popping up** surrounding it and its dependencies."*
  - 공식 템플릿이라면 *"should probably be as future proof as possible"*이라고 요구.
  - estebanx64 (2024-05-17): *"already fixed and merged"*
  - **1년 뒤에도 같은 질문이 달린다** — dss010101 (2025-04-10): *"what is the recommended library to use today for authentication with fastapi?"* → **한 번 정리해도 "지금은 뭘 써야 하냐"는 질문이 계속 생긴다는 게 이 방식의 지속 비용이다.**
  - https://github.com/fastapi/full-stack-fastapi-template/discussions/1188
- **최초 제기(2023-05) → 문서 변경(2024-05). 약 1년이 걸렸다.**

**사건 2: 암호 해싱 라이브러리 (`passlib`)**
- GitHub fastapi/fastapi Discussion #11773 **"passlib seems not being maintenanced anymore. However FastAPI's docs still using. Consider change it."** (작성자 dann2333, **2024-06-28**, Answered)
  - 증상이 사소해 보이는 데서 시작한다: bcrypt 버전을 못 읽는다는 경고(*"cannot get bcrypt's version (just for logging)"*)가 여러 프로젝트에서 뜬다.
  - 채택 답변 — sinisaos (2024-09-13): passlib의 `CryptContext`를 버리고 **bcrypt를 직접 호출**하는 최소 변경안 제시 (`bcrypt.checkpw`, `bcrypt.hashpw`+`bcrypt.gensalt`).
  - **YuriiMotov (collaborator, 2025-09-30):** 문서 예제가 **`pwdlib`**을 쓰도록 갱신됐다고 공지.
  - **그리고 곧바로 후속 문제** — Youjin1985 (2025-10-25): 새 pwdlib 방식과 argon2 버전 사이에 호환성 문제를 보고.
  - https://github.com/fastapi/fastapi/discussions/11773
- **최초 제기(2024-06) → 문서 변경(2025-09). 약 15개월.** 그리고 **바꾼 직후 또 다른 호환성 문제가 보고됐다.**
- **가장 뼈아픈 디테일: `passlib`은 FastAPI 자신의 테스트 스위트에도 들어 있었다.**
  - GitHub fastapi/fastapi Discussion #11380 **"0.110.0: used no longer maintained `passlib` module in test suite"** (작성자 kloczek, **2024-03-31**, upvote 2)
    - > *"Looks like 0.110.0 is using i its test suite `passlib` which seems is no longer maintained more than three years"*
    - 답변 — YuriiMotov (collaborator, **2025-05-26**): #11773의 중복으로 처리. → **신고에서 응답까지 약 14개월.**
    - https://github.com/fastapi/fastapi/discussions/11380
- 관련 리드(본문 미확보): fastapi/fastapi #11345 · full-stack-fastapi-template #1369 `(확인 필요 — 검색 결과 제목만 확인)`

> **책에 쓸 관점 (에이전트 해석 — 검증 필요):** 이게 "Spring Security가 없다"의 **진짜 비용**이다. 필터 체인이나 어노테이션이 없다는 건 표면이고, 실제 부담은 **당신이 고른 보안 부품의 생사를 당신이 계속 감시해야 한다**는 것이다. Spring Boot 사용자는 BOM이 관리하는 버전을 따라가면 되고, 부품이 EOL되면 스프링 팀이 갈아끼운다. FastAPI에서는 **커뮤니티가 신고하고, 메인테이너가 답하고, 문서가 바뀌는 데 1년~15개월이 걸렸으며, 그 기간 내내 공식 문서를 따라 만든 코드가 CVE 있는 라이브러리를 쓰고 있었다.**
>
> 그리고 §2-5 첫머리의 antoinewdg 발언 — *"직접 조립을 선호하지만 보안만은 아니다"* — 이 사건들과 겹쳐 읽으면 그냥 취향 표명이 아니라 **예언**이 된다.
>
> ⚠️ **fact-checker 필수:** 현재 공식 문서가 무엇을 권하는지는 **커뮤니티 글이 아니라 문서 1차 소스로 확인하라.** 위 스레드들은 "언제 무엇이 문제로 제기됐고 언제 바뀌었나"의 근거일 뿐이다. 라이브러리 이름을 현재형으로 쓰려면 반드시 대조할 것.

#### 그 밖의 정황 증거 (1차 회차 수집분)

- 가장 좋은 발언은 FastAPI가 아니라 **Django vs FastAPI 맥락**에서 나왔다. Lobsters, **antoinewdg** (Django vs FastAPI 스레드, ≈2025):
  > *"One thing that is IMO missing from the comparison is security. **I generally prefer the 'build it yourself' approach, but not for security.** Django comes with a lot of security stuff enabled by default, with a lot of documentation and advice on how to use that properly: CSRF, XSS, sessions, user management; you name it, Django has it. To give an example, user management comes built it with password hashing and automatic upgrade of old hashes on login. I would probably think about doing the first in a hand made solution and maybe implement it properly, **definitely not the latter.** This is what brings me back to Django, even though as the author said it definitely shows its age."*
  - **"직접 조립을 선호하지만 보안만은 아니다"** — 이 한 문장이 Spring Security를 쓰다 온 개발자의 정확한 불안이다. 그리고 **"오래된 해시를 로그인 시 자동 업그레이드"** 같은 건 아무도 직접 안 짠다는 지적이 구체적이라 좋다.
  - https://lobste.rs/s/2jwm1m/django_vs_fastapi_honest_comparison
  - ⚠️ 발언 대상이 FastAPI가 아니라 Django 비교다. **"Spring Security 경험자가 FastAPI에서 이렇게 말했다"로 왜곡하지 마라.** "마이크로 프레임워크에서 보안을 직접 조립하는 것에 대한 실무자 불안"으로만 써라.
- `⚠️ 여전히 근거 못 찾음` — Spring Security의 **필터 체인·어노테이션 기반 보안(`@PreAuthorize` 등)**에서 FastAPI로 넘어온 사람의 **1인칭 증언**은 2차 회차에서도 확보 실패. 시도한 경로: `fastapi-users/fastapi-users` Discussions 전체를 "Spring"으로 검색 → **결과 0건.**
  - **즉 위 "보안 부품 부패" 사건은 강력한 근거지만, 그건 "조립의 비용"에 대한 근거이지 "Spring Security 사용자의 체감"에 대한 근거가 아니다.** 둘을 섞지 마라.

### 2-6. `@Transactional` 부재 · Spring Data JPA vs SQLAlchemy · 3계층 — 【근거: 중간】

**`@Transactional`에 해당하는 것이 없다는 문제는 §1-2의 #11107이 실증한다.**
- 트랜잭션 커밋을 의존성의 `yield` 뒤에 두는 관용 패턴이 프레임워크 변경으로 **순서가 뒤집혔다**(커밋 전에 세션이 닫힘). Kludex는 이걸 **"의도된 동작"**이라고 답했다.
- **Spring 개발자에게 이게 왜 충격인가:** Spring에서 트랜잭션 경계는 **선언적이고 프레임워크가 보장**한다. FastAPI에서는 그 경계가 **의존성 생명주기라는, 릴리스마다 바뀔 수 있는 구현 세부사항 위에 얹혀 있다.**
- ⚠️ "`@Transactional`이 없어서 불편하다"는 **직접 인용은 확보하지 못했다.** 검색 요약에는 그런 문장이 나왔지만 원문 페이지를 열지 못했다. **인용하지 마라.**

**Spring Data JPA ↔ SQLAlchemy의 감각 차이 (한국 개발자의 양방향 증언 — 희귀하다)**
- velog, JUNYOUNG **"[Spring][FastAPI] FastAPI에서 Spring으로 마이그레이션하며 배운 점"** (2025-03-07)
  - 결론 문장: *"FastAPI는 빠른 개발과 간결한 구조가 강점이었지만, 복잡한 비즈니스 로직을 다루고 대규모 트래픽을 처리하는 데는 Spring이 더 적합했다."*
  - 다만 글의 실제 본문은 **JPA 쪽 삽질**(Fetch Join, 네이티브 쿼리, 엔티티 상속, DTYPE)에 집중돼 있다. **즉 이 사람은 FastAPI에서 Spring으로 갔는데도 N+1과 연관관계 문제를 다시 겪었다.** → **N+1은 프레임워크 문제가 아니라 ORM의 문제**라는 좋은 반증 소재다.
  - https://velog.io/@thedev_junyoung/SpringFastAPIFastAPI에서-Spring으로-마이그레이션하며-배운-점
- velog, 고은연 (2022-01-07): *"ORM 연동이 너무 불편하고, 다수의 데이터베이스 서버 연동이나 entity와 repository manager 방식 사용이 어렵다"* — **entity/repository 어휘를 그대로 쓴다.** Java 배경에서 온 사람이 FastAPI에서 찾다가 못 찾은 게 정확히 그것이다.
  - 같은 글: *"FastAPI는 자바처럼 빡빡한 규칙을 가지지만 예상하지 못한 문제에서는 표준이 없다"*, FastAPI를 **"스프링 부트의 파이썬 버전"**으로 평가. 결국 Flask와 AWS Chalice로 돌아갔다.
  - 🕒 2022년 글. 생태계 성숙도 서술은 현재형 금지. **감정과 프레이밍만 써라.**

**3계층(Controller/Service/Repository)을 FastAPI에 가져올 것인가** → §3-4에서 별도로 다룬다.

**Spring Boot Actuator에 해당하는 것이 없다는 점** 【2차 회차에서 재조사 — 여전히 근거 부족, 단 1차 회차의 수치 오류를 정정한다】

- ❗ **1차 회차 정정:** §7에서 GitHub #9148을 "upvote 56"으로 적었으나, **본문을 직접 페치해 확인한 결과 18표다.** 검색 결과 목록 스크랩이 부정확했다. **목록만 보고 옮긴 숫자는 믿지 마라 — 이 문서의 다른 "목록만 확인" 항목들도 같은 위험이 있다.**
- GitHub fastapi/fastapi Discussion #9148 **"Provide timing data for things FastAPI does outside of user code"** (작성자 sm-Fifteen, **2019-11-10**, upvote **18**, **Answered**)
  - 요청 내용: 검증(pydantic)과 직렬화(json/ujson)는 FastAPI가 뒤에서 처리하므로, 느린 요청을 디버깅할 때 **DB 쿼리가 문제인지, 검증인지, 직렬화인지 분간할 수가 없다.** Server-Timing HTTP 헤더로 노출해달라는 제안.
  - 곁가지 성과: dmontagu가 yappi 프로파일러 + contextvars 조합을 제안했고, **yappi 저자(sumerc)가 스레드에 합류해 코루틴 프로파일링 지원을 릴리스했다**(2019-12). 원 제기자는 이를 *"fantastic"*이라 평가. tiangolo(2020-02)는 미들웨어를 별도 패키지로 내라고 제안.
  - 종결(sm-Fifteen, 2020-05-17): 프로파일링 미들웨어는 쓸 수 있게 됐지만 **특정 미들웨어의 오버헤드를 재는 건 콜스택 구조상 여전히 복잡하다**고 남기고 answered 처리.
  - https://github.com/fastapi/fastapi/discussions/9148
  - 🕒 **2019~2020년 논의다. 현재형으로 쓰지 마라.** 다만 "프레임워크가 자기 내부 시간을 노출하지 않는다"는 **구조적 공백**은 Actuator의 `/actuator/metrics`에 익숙한 독자에게 설명할 가치가 있다.
- ⚠️ **여전히 근거 못 찾음:** "Actuator에 해당하는 게 없어서 곤란하다"는 **직접 증언**. GitHub Discussions를 health check·readiness·metrics·monitoring·actuator 키워드로 검색했으나 **결과 0건**이었다. 인접 정황으로 OKKY의 "python 무료로 사용할 apm 추천받을 수 있을까요?" 질문 존재(본문 미확보)가 전부다.
- `application.yml` vs pydantic-settings, JUnit/MockMvc vs pytest/TestClient: `⚠️ 근거 못 찾음` (2차 회차에서도 확보 실패)

### 2-7. NestJS 경험자 관점 — 【근거: 토론은 **없음**, 그러나 유물 **2개**로 증명된다】

**HN·Lobsters에서 NestJS↔FastAPI 아키텍처 비교 토론은 1·2차 회차 모두 찾지 못했다.** 검색되는 건 채용 공고에 두 프레임워크가 나란히 적힌 것뿐이다. **그래서 발언 대신 유물로 증명한다 — 2차 회차에서 유물이 하나 더 나와 이제 둘이다.**

**유물 1: PyNest — "NestJS를 파이썬으로 다시 상상한" 프레임워크 (★859)** 【2차 회차 추가】
- `PythonNest/PyNest` — **FastAPI 위에** NestJS의 모듈 아키텍처를 얹은 프레임워크. 커밋 196개, 별 **859개**. (마지막 활동 시점 미확인)
  - 자기 규정: *"not a direct port of NestJS to Python but rather a re-imagining of the framework specifically for Python developers"*
  - 가져오겠다고 명시한 NestJS 3대 패턴: **모듈 단위 조직화**(*"easy separation of concerns and code organization"*), **의존성 주입**(관리·테스트 용이성), **데코레이터 기반 라우팅/컴포넌트 정의**
  - 겨냥한 독자: 백엔드·ML 엔지니어가 *"build better and faster APIs"* 할 수 있도록, **"FastAPI 단독으로는 본질적으로 제공하지 않는(FastAPI alone doesn't inherently provide)" 구조와 관습**을 준다는 것.
  - https://github.com/PythonNest/PyNest
  - **별 859개는 "FastAPI에 NestJS식 구조가 없다"는 인식이 개인 취향이 아니라는 최소한의 증거다.** 다만 FastAPI 본체(수만 ★)에 비하면 소수 취향이라는 것도 같이 봐야 한다.
- **PyNest를 홍보하는 한국어 글이 그 불만을 가장 구체적으로 정리해준다** — `13akstjq.github.io/TIL` **"아직 FastAPI를 프로덕션에 사용하면 안 되는 이유"** (**2024-07-06**, 원저자·원문 링크 미표기)
  - *"여러 라우트가 동일한 의존성을 필요로 하는 경우 각 라우트 핸들러 함수에 별도로 주입해야 합니다."*
  - *"FastAPI의 DI 매커니즘의 가장 큰 단점은 종속성을 관리하기 위해 싱글톤 패턴을 사용하지 않는 것"*
  - 결론적으로 DRY 위반이며 유지보수성이 나빠진다 → **PyNest가 클래스 수준에서 한 번 주입하는 방식으로 해결한다**는 주장.
  - ⚠️ **이 글은 PyNest 홍보 목적의 파생·번역 글이다. 중립 증언이 아니다.** 다만 §1-3(GitHub #8054)·§2-1(dishka 4번 한계)과 **완전히 같은 진단에 독립적으로 도달했다**는 점에서 인용 가치가 있다. **"한국 커뮤니티도 같은 불만을 갖고 있다"의 근거로는 약하다** — 번역·파생 글이지 한국 실무자의 1차 증언이 아니다.

**유물 2: FastNest (Dev.to, 2026-04-28)**

- Dev.to, Hamza El Mouddane **"FastNest: Bringing NestJS Modular Architecture to FastAPI"** (**2026-04-28**)
  - 저자의 동기: 프로젝트가 커지면 *"maintaining a clean structure can become a challenge"*이고, Node.js 생태계에서 온 개발자들이 **NestJS의 모듈 아키텍처와 의존성 주입 패턴을 그리워한다**(*"miss the Modular Architecture and Dependency Injection patterns of NestJS"*)는 것.
  - FastNest가 채워넣겠다고 밝힌 목록이 곧 **NestJS 개발자가 FastAPI에서 못 찾는 것들의 목록**이다:
    - `@Module` 데코레이터 기반 모듈 시스템
    - **DI 컨테이너**
    - 이벤트 데코레이터 기반 WebSocket 지원
    - **Guards, Interceptors, Pipes**
  - https://dev.to/hamza_elmouddane_1fb8c06/fastnest-bringing-nestjs-modular-architecture-to-fastapi-38hi
  - ⚠️ **단일 저자의 프로젝트다.** 커뮤니티 합의가 아니다. 반응·댓글 수도 확인되지 않았다. `(확인 필요 — 단일 증언)` 다만 **"2026년에도 누군가 이걸 만들 필요를 느꼈다"**는 사실은 그 자체로 데이터다.

- **간접 대조 축 하나 더:** HN 44818279, rmonvfer (2025-08-06)가 Litestar 문서를 읽다가 남긴 탄식 —
  > *"reading the litestar docs, **it even has a built-in event system!** I spent a couple weeks building something I could use with FastAPI..."*
  - NestJS에는 이벤트/인터셉터 계층이 기본으로 있다. FastAPI에서는 **2주를 들여 직접 만들었다.** "Guards/Interceptors가 없다"는 말의 실제 비용이 이 한 문장에 있다.

- **NestJS를 좋게 보지 않는 목소리도 기록해둔다 (균형용)** — Lobsters, alper (Django vs FastAPI 스레드, ≈2025): *"Coming from Django I can't emphasise how much of a step down this pile of crap is (but that is the TS/JS culture that this is considered good and popular): https://nestjs.com"* → **NestJS의 구조가 모두에게 미덕으로 읽히지는 않는다.** 이 책이 "NestJS식 구조가 정답"으로 기울면 안 된다는 신호.

---

## 3. 논쟁점 (양쪽 병기 — 한쪽으로 결론 내지 않는다)

### 3-1. sync를 기본으로 할 것인가, async를 기본으로 할 것인가

**관점 A-0 — "애초에 대부분의 앱은 async가 필요 없다"** 【2차 회차 추가, 가장 강한 논거】
- layer8 (HN, **2026-04-25**): *"Server applications don't spawn threads per request, **they use thread pools.** The extra context switching due to threads waiting for I/O is **negligible in practice for most applications.** Asynchronous I/O becomes important when the number of simultaneous requests approaches the number of threads you can have on your system. **Many applications don't come close to that in practice.** There's a benefit in being able to code the handling of a request in synchronous logic."*
- acdha (HN, **2025-09-02**): *"async is one of those things which makes a big difference in a handful of scenarios but which **got promoted as a best-practice for everything.** Python developers have simply joined Node and Go developers in learning that it's **not magic 'go faster' spray** and reasoning about things like peak memory load or shared resource management can be harder."* — https://news.ycombinator.com/item?id=45106641
- gordonhart (HN, **2026-05-26**) — 조직 차원의 정책으로 삼은 사례: *"For Python backends I've seen good success with just **making it company policy that everything is synchronous (normal-colored)** and bypassing the developer overhead from async/await… **You can go pretty far by just adding more threads, processes, and replicas** before it's worth the overhead."* — https://news.ycombinator.com/item?id=48282531
- 반대 방향 정책도 있다 — scuff3d (HN, **2026-04-26**): 문제는 async가 아니라 **섞어 쓰는 것**이다. *"that mistake I see people make (in Python) is they think of their program in blocking terms by default. So they get this frustrating coloring problem because they are trying to shoehorn in non-blocking calls. **If instead you design the application from the start with asyncio in mind, it makes things much simpler.**"* — https://news.ycombinator.com/item?id=47912131
  - **→ 두 정책의 공통점이 결론이다: 한쪽으로 통일하라. 최악은 혼재다.**

**관점 A — "동기 드라이버를 쓸 거면 `def`가 정답이다"**
- `fastapi-best-practices`의 3단 등급(§1-1)이 이 입장을 정식화했다: `async def` + 블로킹 = **Terrible**, 그냥 `def` = **Good**. **"async가 항상 낫다"를 명시적으로 부정한다.**
- 근거: FastAPI가 `def` 라우트를 스레드풀로 돌려주므로 이벤트 루프가 안 막힌다.
- 실무 제약이 이 선택을 강제하기도 한다 — GitHub #8433 (2022): Snowflake SQLAlchemy 드라이버가 asyncio를 지원하지 않아 sync를 쓸 수밖에 없었다.

**관점 B — "sync 엔드포인트는 스케일이 안 된다"**
- 같은 #8433 스레드가 이 입장의 근거다. sync 엔드포인트 + gunicorn 워커 4개에서 **부하가 한 워커로 쏠렸다.** Kludex: 로드 밸런싱은 **OS가 한다** — 프레임워크가 못 고친다. 그리고 **AnyIO 기본 스레드 상한 40개**가 천장으로 존재한다.
- 즉 sync 경로에는 **두 개의 보이지 않는 한계**가 있다: OS 스케줄러의 변덕 + 스레드풀 상한.
- 벤치마크 관점의 방증 — GitHub #7320에서 pinkfrog9: async 라우트가 동기 대비 **4,902 vs 2,596 req/s**로 유의미하게 빨랐다고 보고. 🕒 **2020~2022년 수치다. 현재형으로 쓰지 마라.**

**어떤 조건에서 어느 쪽인가 (커뮤니티 발언에서 도출되는 경계)**
- 동기 드라이버밖에 없다 → `def`. 억지로 `async def`를 쓰는 게 최악.
- 동시성이 낮고 요청당 작업이 짧다 → sync로 충분. 스레드풀 40 상한에 안 닿는다.
- 동시 연결이 많고 I/O 대기가 길다(외부 API 팬아웃, 스트리밍, 웹소켓) → async가 구조적으로 유리.
- CPU 바운드 → **둘 다 아니다.** GIL 때문에 멀티프로세싱/태스크 큐로 빼라 (`fastapi-best-practices`).

### 3-2. ORM vs raw SQL vs SQLAlchemy Core

**관점 A — SQLAlchemy는 감당할 가치가 없다**
- HN 44817479, NeutralForest (2025-08-06): *"I'm not sure how I feel about SQLAlchemy...; **it's such a big ball of state that has so many surprises**, I wonder if some people build entirely without it."*
- HN 44818707, WD-42: *"SqlAlchemy and Alembic are usually not worth dealing with."* — DB가 필요하면 그냥 Django를 쓴다.
- HN 44819938, jg0r3: *"writing SQL and directly wrangling Async connection pools always seemed way easier for me than trying to jam sqlalchemy into whatever hole I'm working with."*
- HN 44817805, jessekv: *"I usually just use asyncpg."* (SQLAlchemy에서 asyncpg를 쓸 수 있다는 지적에 대해: *"Yep! But I don't."*)

**관점 B — 절충: 모델·마이그레이션만 ORM, 쿼리는 손으로**
- HN 44821699, bootsmann (2025-08-07): *"I think the way to go with SQLAlchemy is to use the models and alembic for migrations and schema definition but to **write the sql and do transaction management by hand.** Losing time to figure out how a query you know how to write can be constructed within the ORM is just too much imo."*
- 실측 반대 증언도 있다 — HN, corv (Oxyde 스레드, 2026-03-18): *"I've replaced about 900 lines of raw SQL and got validation and dashboard for free."* → **raw SQL 900줄을 걷어냈다**는 반대 방향 경험.

**관점 C — SQLAlchemy가 더 강력한 도구다 (Django ORM과의 대리 논쟁)**
- HN 44821517, globular-toast: *"SQLAlchemy is just a totally different beast to Django, it has a much higher learning curve but gives you so much more power and flexibility. **It's a true data mapper ORM rather than the sad Active Record pattern** which starts off well and quickly gets annoying."*
  - 반박 — HN 44821595, adrianh: *"I've been using the Django ORM for 20 years, and it has yet to get annoying. **What's your definition of "quickly" — perhaps 25 years?**"*
  - 재반박 — globular-toast (44822360): 결정적 이유는 테스트다. *"you can't do tests without having a database there. This results in incredibly slow tests for even the simplest things. I don't need to test database persistence every time I'm testing some domain logic."* → 도메인 로직과 영속성을 분리하려면 결국 데이터 매퍼가 필요하다.
  - **Spring 개발자에게 이 논쟁은 익숙하다** — Hibernate에서 도메인 모델과 엔티티를 분리할 것인가와 같은 축이다.
- 실무 편의성 반론 — HN 44822303, brokegrammer: Django ORM은 `my_user.save()`로 끝나고 `prefetch_related` + `annotate`로 집계가 객체 속성으로 붙는데, SQLAlchemy는 세션을 항상 의식해야 하고 집계 결과를 **튜플에서 손으로 매핑**해야 한다. *"I feel like SQLAlchemy wants to force you to do more work."*
  - 반대편 — HN 44824356, Ralfp: *"Tell me how to extend Django's default JOIN clause with custom AND, eg: SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.key AND t2.used_id = 213"*

**조건별 판단 (커뮤니티 발언에서 도출)**
- 쿼리가 복잡하고 SQL을 이미 잘 안다 → Core/raw. ORM 우회에 쓰는 시간이 더 비싸다.
- 도메인 로직을 DB 없이 테스트하고 싶다 → 데이터 매퍼(SQLAlchemy)가 구조적으로 유리.
- CRUD가 대부분이고 어드민이 필요하다 → 여러 사람이 **그냥 Django**를 권한다.

### 3-3. FastAPI vs Litestar vs Django Ninja vs Flask/Starlette

> **⚠️ 편향 경고:** 이 논쟁의 핵심 근거인 HN 44816755 스레드는 **"Litestar는 볼 만하다"는 글에 달린 댓글**이다. 즉 **FastAPI를 떠나는 사람이 과대표집된 표본**이다. 아래 반론 항목을 반드시 같은 비중으로 써라.

**Litestar가 FastAPI의 어떤 불만에서 출발했는가 (지지 측 논거)**

1. **문서 — 가장 많이·가장 격하게 반복된 불만**
   - HN 44817543, hariwb: *"I have similar gripes about FastAPI having developed an application over the past few years; I'm also **continually surprised at how prevalent the attitude is that FastAPI has excellent docs**, given how divorced the tutorial / toy examples in the docs are from real-world development and measurement of an API."*
   - HN 44818400, rtpg: *"I am really disappointed at the new generation of Python frameworks' documentation, which seem to have the same "docs are tutorials + chatty blog posts which imprecisely describe the APIs" attitude of Javascript libs. **Two words: API Reference.** ... Don't make me dive into the source to find out what I can or can't pass into a parameter!"*
   - HN 44818830, rmonvfer: *"**FastAPI is 10x harder to use because of this.** I've had to read FastAPI code many times to **literally reverse engineer features** because they are not documented in any way. Documentation is for reference, tutorials are for learning... And SQL Model is even worse in that regard."*
   - HN 44570215, lutoma (2025-07-15): *"Mostly the better documentation (last I checked FastAPI docs felt more like a series of blog posts than actual docs, but maybe that's improved)."*

2. **거버넌스 — §3-6에서 별도로 다룬다**

3. **명시성 vs 마법**
   - lutoma (44570215): Litestar가 *"more explicit about things while FastAPI was more 'opaque magic happening in the background'"*

4. **기능 공백** — 내장 이벤트 시스템(rmonvfer, §2-7), 클래스 기반 Controller와 중첩 라우팅, msgspec 일급 지원(HN 44817941, intalentive), 내장 캐싱(HN 44822968, talos_)

**Litestar 지지자의 실사용 증언**
- HN 44817941, intalentive (2025-08-06): 1년 넘게 JSON·템플릿 HTML 양쪽에 사용. *"Great all-around Python async framework that manages to be fast (**faster than FastAPI**), lightweight, and still has enough batteries included."* ⚠️ 성능 주장은 개인 소감이며 벤치마크 근거 없음.
- HN 44820559, wraptile (2025-08-07): *"Switched from FastAPI on a new project and never looked back."*
- HN 44817946, thewisenerd: 사내 콘솔들을 FastAPI에서 이주 중. 다만 **Litestar 문서도 "how-to"가 부족하다**고 인정.

**FastAPI 옹호·Litestar 유보 (반대편 논거 — 반드시 병기하라)**
- HN 44819446, jaza: 큰 코드베이스에서 어렵다는 주장은 **"exaggerated"** (§1-7 전문).
- HN 44819290, croemer: *"Is there really less documentation? FastAPI mostly has tutorials to get started and is light on deep/reference material. **A single person can only do so much.**"* — 문서 비판을 **인력 현실**로 되받는다.
- HN 44822799, whinvik: *"I agree that FastAPI is not the best but **I would not jump to another framework just because of an article.**"* → 참조 코드베이스(`polarsource/polar`)의 존재가 잔류 이유다.
- HN 44822524, brokegrammer: Litestar는 기능이 많아서 오히려 위험하다 — *"I hope that the project doesn't get abandoned like so many frameworks these days because **unlike tiny frameworks, it would be harder to migrate off of.**"* → **버스 팩터 논리를 뒤집은 반론.**
- HN 44818760, no_carrier: SQLModel을 FastAPI 문서가 강하게 민다는 주장 자체를 부정 — *"The front page for FastAPI contains a pretty lengthy tutorial with no mention of SQLModel... _Something_ has to be chosen for the tutorial... **If SQLModel isn't right for you then you're the only person to blame.**"*

**"차라리 Starlette만 써라"는 제3의 길**
- HN 44818282, andrewstuart: *"I love Starlette but not a fan of FastAPI and do not use it."*
- HN 44818451, zokier: *"I know fastapi gets the hype, but I have found plain starlette quite usable by itself."*
- HN 44820130, holler: *"I've built all my recent api's in Starlette alone and I find it excellent... supporting small -> very large projects."*
- 단, 반론 — HN 44825169, gwking: *"**Starlette lacks docstrings entirely** and it's a real miss in my opinion."*
- 한편 hangonhn (44819564): Starlette을 쓰지만 동료에게는 Litestar를 권한다 — **DI가 있기 때문이다.**

**Django Ninja / Django 진영**
- HN 44821077, devjab (2025-08-07) — Django Ninja에서 Litestar로 옮긴 이유: *"Django-ninja is excellent, but it's still Django and when you aren't using a lot of the "batteries included" then you're not really using Django... We picked Litestar because it's **natively async, makes it easy to use dataclasses rather than Pydantic, has really fast cold start** and it has great interoperability with Advanced Alchemy."*
  - 그리고 규모 논리를 정직하게 인정한다: *"Considering it runs Instagram it certainly scales as well, but **unlike Instagram we aren't enough engineers** to be able of ripping out more and more batteries while replacing them with our own specialized batteries."*
- Lobsters, capitano (≈2025): *"Use Django if you want to build server rendered apps with batteries included. Use FastAPI if you want to build REST APIs with a separate frontend framework of your choice."* — 가장 간결한 경계선.
- Lobsters, koala: Django admin 같은 게 없다는 게 FastAPI로 못 가는 이유 — *"when I look at FastAPI, I like it a lot. But most things I want to do... I kinda always need something like the admin, so I still turn to Django frequently."*
- 성능 반대급부 — Lobsters, alper: Django Ninja가 매력적이지만 *"The only issue that leaves is Django's performance which on the benchmarks is quite bottom tier."*

**메타 논평 (인용 가치 높음)**
- HN 44820803, Copenjin (2025-08-07): *"When will people understand that those very opinionated frameworks with enticing tutorials just ruin your life in the long term? **I see someone citing Spring(yikes) elsewhere, that falls in the same category as FastAPI.** You don't need Spring most of the times, a simple dependency injection library and small frameworks to handle the web routing or specific features you need are often enough."*
  - **Spring과 FastAPI를 같은 죄목으로 묶은 발언이다.** 이 책의 대상 독자를 정확히 도발한다.
- Lobsters, ryan-duve (≈2025), 프레임워크 선택 논쟁 전반에 대해: *"Learn Django and FastAPI. Also, learn three more... You don't need to become an expert in all of them, but **you can only make the choice 'based on your project requirements' if you know what the options are at decision time.** One tool is a screwdriver and one is a can opener."*
  - 반론 — Halkcyon: *"This mentality works if you have a lot of free time. I think you should learn _a thing_ deeply first... Otherwise you're just noticing surface level differences and not differences in architectures and design decisions."*

### 3-4. 서비스 레이어를 둘 것인가 (Spring식 3계층을 가져올 것인가)

**관점 A — 계층을 두라 (사실상 커뮤니티 기본값)**
- `fastapi-best-practices`의 도메인 패키지 구성에 `service.py`가 명시적으로 들어 있다(§1-7).
- rmonvfer(§2-1)가 공식 템플릿에서 cringe를 느낀 지점이 정확히 **CRUD를 한 파일에 몰아넣는 것**이었다.

**관점 B — 리포지토리·서비스 레이어는 남용되고 있다**
- HN 44817398, ddejohn (2025-08-06): *"I also still think there are a lot of **bad use cases for repositories and service layers that people should avoid**, but that's a digression which should probably become its own post."*

**관점 C — 계층이 아니라 수직 슬라이스로 잘라라**
- canadiantim(44821271) + hynek(44822016) — §1-7 참조. *"Vertical Slice Architecture... it's the only way for complex apps that doesn't end in chaos."*
- 그에 대한 반론 — shakna(44822469): 컨트롤러는 원래 VSA가 잘 안 맞는 예로 꼽혔다. *"Relying on it as dogma will result in chaos."*

**관점 D — 어차피 직접 프레임워크를 짜야 한다**
- whilenot-dev(44821229): 마이크로 프레임워크의 본질적 이득이 그것이다(§1-7).
- 반면 rmonvfer(44818249)에게는 그게 **비용**이다: *"requiring you to write a framework on top, like I've unfortunately done"*.
- **같은 사실을 한쪽은 자유로, 한쪽은 부담으로 읽는다.** 이 책이 다뤄야 할 정확한 긴장이다.

**메타 관점 (한 방이 있다)**
- HN 44821541, twothreeone (2025-08-07): *"Agreed 100% FastAPI works but building complex applications in it is just not great. Taking a step back (and this will date me but..) I'm still astonished how the **"Python microframework world" is slowly rediscovering everything JavaEE had 15 years ago.**"*
  - Java 개발자 독자에게 던질 수 있는 최고의 도발이자, 동시에 **"그래서 JavaEE가 옳았느냐"**는 반문도 가능한 양날.

### 3-5. SQLModel을 쓸 것인가

**반대 (근거가 구체적이다)**
- HN 44818249, rmonvfer (2025-08-06): *"Then came the SQLModel problems. The author pushes it very hard in the FastAPI docs... but as an ORM (yes I know its a layer on top of SQLAlchemy) **it doesn't even support polymorphic models** and the community even has contributed **PRs that have gone months without any review (is it even maintained anymore? I honestly can't tell).**"*
- HN 44818830, rmonvfer: 문서 품질에서 *"SQL Model is even worse in that regard."*
- HN 44821476, globular-toast: *"**Stuff like FastAPI and SQLModel is a joke imo.** Developers should be able to compose these things themselves if they want to."*
- **가장 기술적으로 구체적인 반대** — HN, ForHackernews (Oxyde 스레드, **2026-03-16**): *"SQLModel...**it's actually worse than useless because if you add it to your Pydantic models, it disables all validation**"*
  - ⚠️ **이건 검증 필요한 단일 주장이다.** 사실이라면 결정적이지만 `(확인 필요 — 단일 증언, fact-checker가 1차 소스로 대조할 것)`

**찬성/중립**
- HN 44818760, no_carrier: 문서가 SQLModel을 밀지 않는다고 반박. 튜토리얼엔 뭐라도 골라야 하고, 저자가 자기 것을 고른 건 자연스럽다. *"If SQLModel isn't right for you then you're the only person to blame. I've been through that tutorial before and **settled on plain old SQLAlchemy.**"*
- **논쟁의 뿌리는 "하나의 모델이냐 두 개의 모델이냐"다** — HN 44821476, globular-toast: API 모델과 DB 모델은 처음부터 분리하는 게 맞다(§2-2 전문). Oxyde 저자 mr_Fatalyst(2026-03)도 같은 문제 제기에서 출발한다: *"If you use FastAPI, you know the drill. You define Pydantic models for your API, then define separate ORM models for your database, then write converters between them."*
  - **즉 SQLModel은 "이 중복이 낭비다"라는 진단에서 나왔고, 반대자들은 "그 중복은 낭비가 아니라 설계다"라고 답한다.** Spring의 Entity vs DTO 논쟁과 정확히 같은 축.

### 3-6. 거버넌스·버스 팩터·0.x·상업화

**버스 팩터 우려 — 근거가 여러 사람에게서 독립적으로 나온다**
- HN 44817272, cr125rider (2025-08-06): *"Litestar is awesome. **It's great it's got more than a single maintainer too.**"*
- HN 44571027, robertlagrant (**2025-07-15**, "Happy 20th Birthday, Django" 스레드): *"We chose Litestar over FastAPI mostly because they seemed very similar, but **Litestar had a more distributed governance; i.e. a larger bus factor.** We are jealous of some FastAPI features though, so it's possible we could migrate, as Litestar's mapping between domain models, database models and API models isn't as flexible as we'd like."*
  - **주목:** 거버넌스 때문에 옮겼지만 **기능은 FastAPI가 부럽다**고 인정한다. 균형 잡힌 증언이다.
- HN 44570215, lutoma (2025-07-15): FastAPI의 **"BDFL-type development structure"** vs Litestar의 **"community-driven approach"**.
- HN 44818834, ilumanty (2025-08-06): *"Tiangolo is type who wants to do it his way without a ton of input. **One of reasons Litestar was developed.**"* `(확인 필요 — 인물 평가이며 검증 불가)`

**반대 방향의 시선**
- HN 44819290, croemer: *"A single person can only do so much."* — 같은 사실을 **비난이 아니라 정상 참작**으로 읽는다.
- HN 44822524, brokegrammer: 기능이 많은 Litestar가 버려지면 **이탈 비용이 더 크다** — 버스 팩터 논리를 되돌려준다.

**"비판이 잘 처리되지 않는다"는 인식의 근거 사건**
- HN 44818753, miki123211 (2025-08-06): *"FastAPI used to have an emoji-ridden docs page for concurrency. **Criticism was not handled well.** This made it clear to me that something about the project is off."* → 링크한 것이 GitHub Discussion **#6656 "Too many emojis in 'Concurrency and async / await' explanation"**
  - 원 제기자 kittenswolf (**2021-05-21**): *"Every emoji breaks the flow when reading because my eyes are distracted by the emojis' size and colour."* 스크린 리더 접근성 문제도 제기됨(@intrnl).
  - tiangolo 답변 (**2022-08-17**): 이모지는 **패턴 인식으로 인지 부하를 줄이는 시각 단서**라는 교육적 의도였다고 설명(선형 탐색 대신 O(1) 해시 조회에 비유). 다만 **300개 이상의 긍정 반응**을 받아들여 전문 일러스트를 발주해 교체했다.
  - **결과적으로는 반영됐다.** 🕒 **이건 2021~2022년 사건이다.** "지금도 이모지가 문제다"로 쓰면 명백한 오류다. **커뮤니티 인식에 남은 흉터**로만 다뤄라 — 실제로 2025년에도 이 사건이 인용된다는 게 요점이다.
  - https://github.com/fastapi/fastapi/discussions/6656

**"마케팅과 실제가 다르다"는 오래된 불만**
- GitHub Discussion #7320 **"Very poor performance does not align with marketing"** (작성자 삭제됨, **2020-07-02**, 참여자 35명, 2022년까지 이어짐)
  - 최초 불만: README의 *"very high performance, on par with NodeJS and Go"* 주장에 대해 wrk 측정 **5,442 req/s**를 제시.
  - 반론들: phy25는 TechEmpower를 제시(FastAPI 159,445 vs Node 884,444 — **Node의 약 18%**). dbanty는 **DB가 낀 시나리오에선 FastAPI가 강하고 plaintext 같은 I/O 경량 테스트에서 약하다**고 분석. cirospaciari(2022-12)는 오버헤드가 프레임워크가 아니라 **ASGI 서버 계층**에서 온다고 지적.
  - 도출된 합의에 가까운 것: **"on par with"는 오해를 낳는다. FastAPI는 "가장 빠른 Python 프레임워크"이지 Node/Go와 동급은 아니다.** 비교 대상은 bare HTTP 서버가 아니라 **NestJS나 미들웨어를 얹은 Express** 같은 풀피처 프레임워크여야 한다.
  - 🕒 **모든 수치가 2020~2022년 것이다. 절대 현재형으로 쓰지 마라.** 다만 **"비교 대상을 잘못 고르면 벤치마크는 의미가 없다"**는 방법론적 교훈은 시효가 없다.
  - https://github.com/fastapi/fastapi/discussions/7320

**0.x 버전대에 머무는 것에 대한 의견**
- ⚠️ **근거 못 찾음.** 0.x 유지 자체를 문제 삼는 커뮤니티 토론을 직접 확인하지 못했다. 인접 발언은 rtpg(44819192)의 *"the absolute mess which was pydantic 1 -> 2 (or django-ninja 0.x -> 1.0)"* 정도인데, **이건 FastAPI 버저닝이 아니라 생태계 전반의 파괴적 변경에 대한 불만**이다. 왜곡하지 마라.

**FastAPI Cloud (상업화) — 존재는 확인, 반발은 확인 안 됨**
- **확인된 사실:** FastAPI Cloud는 실재하며 **2026년 6월 공개 베타**에 들어갔다. HN "Show HN: FastAPI Cloud is in public beta, deploy apps with `fastapi deploy`" (2026-06-22, **5점**)
  - tiangolo 본인 코멘트 (2026-06-22): *"Hi HN, I'm Sebastián, creator of FastAPI. We just opened the public beta of FastAPI Cloud. You can deploy FastAPI apps with the command `fastapi deploy`, or connect your GitHub repo, with logs, metrics, custom domains, teams, and managed deployments."*
  - 유일한 외부 반응 (j-bu, 2026-06-23): *"This is really exciting stuff - deployed my first app and worked flawlessly."*
  - https://news.ycombinator.com/item?id=48637393
- 관련 HN 게시들도 모두 저조하다: 2025-05-05 최초 소개 16점/5댓글, 2026-06-23 공개 베타 블로그 4점/0댓글.
- **⚠️ 결론을 정확히 써라: 상업화에 대한 커뮤니티 반발을 이번 회차에서 찾지 못했다. 논쟁이 없었던 게 아니라, 내가 찾은 채널(HN)에서 애초에 논의 자체가 거의 없었다.** 버스 팩터 인용문을 끌어다 **"상업화 백래시"를 만들어내지 마라.** 둘은 별개의 주제이며, 전자만 근거가 탄탄하다.

---

## 4. 현장 휴리스틱 (숫자·경험칙 — 전부 개인 경험담이다)

| 휴리스틱 | 출처 | 시점 | 주의 |
|---|---|---|---|
| **"CPU당 워커 2개 + 1개"** → 1코어/600MB 환경에서 워커 3개로 정착. 평시 파드 3, 고부하 5 | GitHub #7439, nreith | 2022-07 | 단일 팀 경험. 하드웨어 특정 |
| 동기 엔드포인트를 쓸 거면 **코어당 워커 2개** | GitHub #8433, jgould22 | 2022-12 | 위와 같은 계열 |
| **정하기 전에 locust.io로 부하 테스트를 하라** | GitHub #7439, nreith | 2022-07 | 가장 안전한 조언 |
| gunicorn 대신 **uvicorn 단독 워커 1개 + 컨테이너 복제** | GitHub #8433, iudeen / #7439, Irmius | 2022~2023 | 현재 공식 문서 방향과 일치 |
| **gunicorn을 쓰면 워커 죽는 걸 k8s가 못 본다** | GitHub #7439, GuiGav | 2022-09 | 관측성 관점의 결정적 논거 |
| uvicorn 단독은 누수 없었는데 **gunicorn+uvicorn에서 심한 메모리 누수** | GitHub #9145, hzy0809 | 2024-08 | 단일 증언. 대조 필수 |
| 메모리 누수 범인으로 **`exception_handler` 데코레이터** 지목, `gc.collect()` 우회 | GitHub #9145, AntonioBarral | 2023-10 (2건 재현 확인) | **커뮤니티 진단이지 공식 확인 아님** |
| Python은 free된 블록을 **OS에 돌려준다고 보장하지 않는다** — 상당수는 누수가 아니다 | GitHub #9145, dmontagu | 2019-12 | 오진 방지용 |
| 배경 태스크는 **본문 전체를 try/except로 감싸고 직접 로깅**하라 | GitHub #11828, gustavosett | 2024-07 | 미들웨어가 예외를 삼킨다 |
| 동기 엔드포인트 스레드풀에는 **AnyIO 기본 상한 40**이 있다 | GitHub #8433, Kludex(collaborator) | 2022-12 | 값은 1차 소스 대조 필요 |
| 워커 간 부하 불균형은 **OS 스케줄러 문제**다 — 프레임워크가 못 고친다 | GitHub #8433, Kludex | 2022-12 | |
| 관계 필드는 **`lazy="selectin"`으로 ORM 레이어에서** 미리 해결하라 | GitHub #13125, sehraramiz | 2024-12 | ✅ 현재 유효 |
| 3만 5천 포인트 응답: DB 0.15s / 검증 0.17s / **직렬화 0.60s** | GitHub #13455 | 2025-03 | 단일 사례. 재현 조건 제한적 |
| **의외로 FastAPI 자동 직렬화가 수동 orjson보다 빨랐다** (1.6s vs 2.0s) | GitHub #13455 | 2025-03 | "직렬화는 무조건 손으로"를 반박하는 데이터 |
| 시계열은 페이지네이션보다 **LTTB 서브샘플링** — 화면에서 어차피 구분 안 된다 | GitHub #13455, ValentinKaisermayer | 2025-03 | 도메인 특화 |
| Lambda 콜드 스타트: init **9.9초에 런타임 재시작**, 18초+ 무응답 | aws-lambda-web-adapter #620 | 2025-11 | ✅ 최신 |
| 콜드 스타트 처방: **시작 시 임포트 줄이기** > SnapStart | 위 스레드, bnusunny(메인테이너) | 2025-11 | |
| 도메인별 패키지(`router/schemas/models/service/dependencies/...`) | fastapi-best-practices (17.8k★) | 갱신일 미확인 | 가장 널리 인용되는 구조 |
| 스레드풀 오버헤드를 피하려면 **async 의존성을 선호**하라 | fastapi-best-practices | 갱신일 미확인 | |
| `Depends` 캐싱은 **요청 내부에서만** 유효 — 싱글턴이 아니다 | GitHub #8054, dmontagu | 2019, 2024까지 유효 | ✅ 오해 교정용 |
| 앱 수명 싱글턴은 `app.state` 또는 `AsyncExitStack`+app state로 | GitHub #8054, sm-Fifteen / g0di | 2022 / 2024 | |
| CPU 바운드는 async도 스레드도 답이 아니다 → 멀티프로세싱/Celery | fastapi-best-practices | | GIL |
| API 모델과 DB 모델은 **처음부터 분리**하라 | HN 44821476, globular-toast | 2025-08 | 논쟁 중(§3-5) |
| SQLAlchemy는 **모델·마이그레이션만 쓰고 쿼리·트랜잭션은 손으로** | HN 44821699, bootsmann | 2025-08 | 절충안 |
| 프로덕션 FastAPI 참조 코드베이스: `polarsource/polar` | HN 44822799, whinvik | 2025-08 | 대조 필요 |

---

## 5. 챕터 오프닝에 쓸 만한 생생한 일화·인용

1. **"연옥의 모든 단계를 거쳤다"** — rmonvfer (HN 44818249, 2025-08-06)
   > *"I've been building a large backend with FastAPI for the last year or so and **I've gone through all the levels of the purgatory.** I began using the standard "tutorial" style and started cringing when I saw the official template place all CRUD operations in a single file (I've been doing Rails and Spring for a while before)..."*
   → **Spring 출신 독자를 첫 문장부터 붙잡는다.** 1장 또는 프로젝트 구조 챕터 오프닝.

2. **"결국 그 위에 프레임워크를 하나 더 짰다 — 불행히도"** — 같은 사람
   > *"...not built for complex applications (at least not without **requiring you to write a framework on top, like I've unfortunately done**)."*
   → "FastAPI는 자유로운가, 미완성인가" 챕터.

3. **"파이썬 마이크로프레임워크 세계가 JavaEE가 15년 전에 갖고 있던 걸 천천히 재발견하고 있다"** — twothreeone (HN 44821541, 2025-08-07)
   → 서비스 레이어/아키텍처 챕터. **Java 독자를 정확히 도발한다.**

4. **"에러가 안 난다. 부하가 걸려야 난다."** — §1-1의 전체 구조
   → async 챕터 오프닝. `async def` 안의 동기 호출이 **조용히** 처리량을 무너뜨리는 이야기.

5. **"이 배경 태스크는 절대 실행되지 않는다"** — GitHub #14137 (2025-10-01)
   > 코드 주석 그대로: *"The following background task is never executed"* — `yield` 뒤의 print는 정상 출력되는데 태스크만 사라진다.
   → **"조용한 실패" 챕터.** 에러 로그도, 예외도 없다.

6. **"Init Duration: 9930.03 ms — Status: timeout"** — aws-lambda-web-adapter #620 (2025-11-10)
   > 헬스체크에 18초 넘게 응답 못 함. 코드는 한 줄도 안 틀렸다. **임포트가 느렸을 뿐이다.**
   → 배포/서버리스 챕터.

7. **"FastAPI 문서가 훌륭하다는 인식이 이렇게 널리 퍼져 있다는 게 계속 놀랍다"** — hariwb (HN 44817543, 2025-08-06)
   → 이 책이 왜 필요한지를 정당화하는 인용. **서문 후보.**

8. **"기능이 문서에 전혀 없어서 FastAPI 코드를 읽고 리버스 엔지니어링해야 했다"** — rmonvfer (HN 44818830)
   → 위와 같은 용도. 더 날것이다.

9. **"보안만은 직접 만들지 않는다"** — antoinewdg (Lobsters, ≈2025)
   > *"I generally prefer the 'build it yourself' approach, **but not for security.**"*
   → 인증·인가 챕터 오프닝. Spring Security 독자에게 직격.

10. **"Litestar 문서를 읽다 보니 이벤트 시스템까지 내장돼 있더라. 난 FastAPI에서 쓰려고 그걸 2주 걸려 만들었는데."** — rmonvfer (HN 44818279)
    → "배터리 포함이냐 조립이냐" 챕터.

11. **"Spring(윽), 그것도 FastAPI와 같은 부류다"** — Copenjin (HN 44820803)
    > *"When will people understand that those very opinionated frameworks with enticing tutorials just ruin your life in the long term? I see someone citing **Spring(yikes)** elsewhere, that falls in the same category as FastAPI."*
    → 도발적 오프닝. **Spring 독자가 "우리가 왜?"라고 반응하게 만든다.**

12. **"20년 썼는데 아직 안 짜증나던데. '금방'의 정의가 뭐죠, 25년쯤?"** — adrianh (HN 44821595)
    → ORM 논쟁 챕터. 커뮤니티 논쟁의 온도를 그대로 보여준다.

13. **"이렇게 해도 돼..?"** — velog 동근이의 개발 일기 (2025-01-20)
    → **한국 독자용 오프닝.** 컨벤션이 없는 프레임워크 앞에서 팀이 느끼는 불안을 한 마디로 담았다.

14. **"자바처럼 빡빡한 규칙을 가지지만 예상하지 못한 문제에서는 표준이 없다"** — velog 고은연 (2022-01-07)
    → 같은 용도. 🕒 2022년 글임을 감안해 **감정만** 쓰고 생태계 서술은 인용하지 말 것.

15. **"Python-Jose는 한참 전에 방치됐고, 이제 CVE가 튀어나오고 있다"** — SpoonOfDoom, GitHub full-stack-fastapi-template #1188 (2024-04-29)
    > 공식 문서와 공식 템플릿이 추천하던 JWT 라이브러리 얘기다. 신고에서 문서 변경까지 **약 1년**. 암호 해싱 라이브러리(`passlib`)는 **약 15개월**.
    → **인증·인가 챕터의 진짜 오프닝.** Spring Security 독자에게 "직접 조립"의 비용이 무엇인지 감정 없이 사실로 보여준다. §5-9(antoinewdg)와 짝으로 쓰면 예언 → 실현 구조가 된다.

16. **"고쳤는데 3주 뒤에 또 깨졌다"** — prometheus-fastapi-instrumentator #370(2026-06-14) → #388(2026-07-08)
    > 라우터 구조가 바뀌어 메트릭 라이브러리가 터졌고, 고친 뒤 다음 마이너에서 또 터졌다.
    → **배포·운영 챕터 또는 "0.x와 함께 살기" 챕터.** Spring Boot의 하위호환 문화와 정면 대비.

17. **"인수받은 파이썬 서비스가 제일 엔터프라이즈한 Spring JEE 뺨쳤다"** — hiram112 (HN, 2021-12-04)
    > *"this thing would give the most 'enterprisey' Spring JEE application a run for its money with its endless annotations, dependency injection magic, all sorts of pseudo-types… **But unlike Java, these types aren't even really guaranteed by the language at compile time**, so… things will still (silently) slip through at runtime."*
    > 바로 달린 반박: *"This sounds like what happens when a bunch of Java/C# developers jump over to python **without learning the 'python way'**."*
    → **서문 또는 1장 오프닝 최상위 후보.** 이 책이 존재하는 이유가 저 반박 한 줄에 들어 있다. 🕒 2021년 글이므로 생태계 서술이 아니라 인지 충돌 기록으로만 쓸 것.

18. **"Java에는 virtual thread가 있다. 그게 Python의 async/await보다 나은 동시성 모델이다. Python에도 넣자."** — Mark Shannon, CPython 코어 개발자 (discuss.python.org, 2025-05-09)
    → **async 챕터 오프닝의 최강 카드.** Java 독자에게 "당신이 Loom으로 얻은 걸 파이썬은 아직 못 얻었고, 파이썬 코어 개발자들도 그걸 안다"고 말할 수 있는 1차 근거.

19. **에러가 범인과 다른 요청에서 터진다** — acdha (HN, 2026-04-26)
    > 요청1이 await → 요청2로 전환 → 요청3이 루프를 막음 → **요청1이 소켓 타임아웃.** *"That error in #4 does not tell you anything about #2 or #3."*
    → §5-4("부하가 걸려야 난다")의 짝. **"터져도 엉뚱한 데서 터진다."** async 디버깅 챕터.

20. **"인생에서 겪은 최악의 프로그래밍 경험"** — honeyryderchuck (Lobsters, 2023-06-11)
    > 초당 5 트랜잭션짜리 제품을 위해 asyncio 기반 파이썬을 유지보수하며: *"**the absolute worst experience I've ever had programming in my life**: a second python ecosystem mostly incompatible with the other, nearly impossible production issues debugging… the occasional 'crap forgot to write async again and now this function does nothing'"*
    → 🕒 2023년. 과장된 감정이지만 **"async를 쓸 필요가 없는 규모에 async를 썼다"**는 §3-1 논쟁의 생생한 사례.

21. **의도된 동작입니다** — Kludex, GitHub #11107 (2024-02-14)
    > 세션 커밋이 세션 닫힘보다 뒤로 밀렸다는 보고에: *"It's the intended behavior."*
    → **`@Transactional`이 없다는 게 무슨 뜻인지** 보여주는 장면. 트랜잭션 챕터.

---

## 6. 근거 못 찾은 항목 (⚠️) · 수집 한계

### 접근 자체가 막힌 플랫폼 (커버리지 구멍 — 반드시 명시하고 넘어가라)
- **Reddit — 전면 차단. 2차 회차에서 우회 경로 5개를 시도했고 전부 실패했다.** r/FastAPI, r/Python, r/django, r/webdev, r/ExperiencedDevs에서 **단 한 건도 수집하지 못했다.** 지시받은 소스 중 가장 큰 손실이다. 이 문서에 Reddit 인용은 없다 — **다른 에이전트가 Reddit 인용을 만들어 넣으면 그건 근거 없는 것이다.**

  | 시도 경로 | 실패 양상 |
  |---|---|
  | `www.reddit.com` 직접 페치 | 도구 레벨 차단 ("unable to fetch") |
  | `old.reddit.com` | 도구 레벨 차단 |
  | `www.reddit.com/r/FastAPI/comments/.json` (JSON 엔드포인트) | 도구 레벨 차단 |
  | WebSearch `allowed_domains: reddit.com` | API 400 — 크롤러 접근 불가 도메인 |
  | WebSearch 질의문에 `site:reddit.com/r/FastAPI` 삽입 | 질의는 통과하나 **결과에 Reddit이 하나도 안 나옴** (Dev.to·Medium으로 대체됨) |
  | redlib 공개 인스턴스 `redlib.catsarch.com` / `redlib.privacyredirect.com` | HTTP 403 |
  | `farside.link/redlib` → `safereddit.com` 리다이렉트 추적 | Anubis 봇 차단 페이지 ("Access Denied") |
  | `r.jina.ai` 텍스트 추출 프록시 경유 | 프록시는 통과했으나 **Reddit이 403** — *"You've been blocked by network security. To continue, log in to your Reddit account or use your developer token."* |

- **Stack Overflow — 전면 차단. 2차 회차 재시도도 실패.**

  | 시도 경로 | 실패 양상 |
  |---|---|
  | WebSearch `allowed_domains: stackoverflow.com` | API 400 — 크롤러 접근 불가 도메인 |
  | `api.stackexchange.com/2.3/search/advanced` (필터 지정) | 도구 레벨 차단 |
  | `api.stackexchange.com/2.3/questions?tagged=fastapi&sort=votes` | 도구 레벨 차단 |

  → **투표순 상위 FastAPI 질문 목록은 실무 고통점의 가장 좋은 지표인데, 이 문서에는 그게 없다.** 후속 회차에서 브라우저 렌더링 도구가 가능하면 최우선으로 재시도할 것.
- **OKKY·GeekNews — 목록은 되고 본문은 안 된다.** 도메인 지정 검색으로 **스레드 존재·제목은 확인**했으나, 두 사이트 모두 본문·댓글이 클라이언트 렌더링이라 **텍스트를 한 줄도 확보하지 못했다.** 아래 §"한국 커뮤니티 — 확인된 스레드" 참조.
- **커리어리, 네이버 카페, Discord/Slack 공개 로그, X, Mastodon — 미수집.**

### 한국 커뮤니티 — 존재만 확인된 스레드 (본문 미확보, 후속 회차 표적)
> **이 목록은 인용 소스가 아니라 "한국 개발자들이 실제로 무엇을 묻고 있는가"의 지표다.** 제목만 근거로 내용을 지어내지 마라. 다만 **질문의 분포 자체가 §1의 고통점 목록과 겹친다**는 사실은 기록할 가치가 있다.

| 스레드 | 대응하는 §1 고통점 |
|---|---|
| OKKY Q&A "fastapi 동시요청시 blocking 이유" (okky.kr/questions/1473757) | §1-1 이벤트 루프 스톨 |
| OKKY Q&A "Celery + FastAPI) Database Session 의존성 주입" (okky.kr/questions/1506800) | §1-2 세션 수명 / §1-3 Depends |
| OKKY Q&A "Fastapi + Alembic 조합 GCP 배포 질문" (okky.kr/questions/1489100) | §1-4 배포 |
| OKKY Q&A "python 무료로 사용할 apm 추천받을 수 있을까요?" (okky.kr/questions/1495055) | §2-6 Actuator 대응물 부재 |
| OKKY "FastAPI vs Flask,Django" (okky.kr/questions/1493110) | §3-3 프레임워크 선택 |
| OKKY "python fast api framework에 대하여 어떻게 생각하세요?" (okky.kr/article/820772) | §3-3 |
| GeekNews "Litestar는 한번 살펴볼 만함" (news.hada.io/topic?id=22402) | §3-3 — **HN의 Litestar 논쟁이 한국 커뮤니티에도 옮겨졌다는 증거.** 한국어 댓글 확보 실패 |
| GeekNews "FastAPI의 시대. 아직도 Flask 쓰시나요?" (news.hada.io/topic?id=6233) — 2022-03-26, 23P, 작성자 yunyun0505 | §3-3 🕒 2022년 |

- **주목할 공백:** APM 추천을 묻는 OKKY 질문의 존재는 §2-6(Actuator 대응물 부재)의 정황 증거지만, **본문을 못 봤으므로 근거로 쓸 수 없다.** 후속 회차에서 브라우저 렌더링이 가능한 도구로 재시도할 것.

### 내용상 근거를 못 찾은 항목
| 항목 | 상태 |
|---|---|
| Pydantic v1→v2 성능 개선의 **실측 증언** | ⚠️ 근거 못 찾음 — **절대 지어내지 마라** |
| `expire_on_commit` 함정 | ⚠️ 커뮤니티 스레드 미확보 |
| 요청 간 세션 누수 | ⚠️ 목록만 확인(#10622), 본문 미확보 |
| 깊은 `Depends` 중첩의 **정량 오버헤드** | ⚠️ dishka의 정성 평가가 전부 |
| 파일 업로드 메모리 | ⚠️ 근거 못 찾음 |
| CORS 실무 고통 | ⚠️ 목록만 확인(#7319) |
| OpenAPI 스키마 생성 실패 | ⚠️ 인접 증거만(#13455의 Swagger UI 스택 오버플로) |
| Cloud Run / 최소 인스턴스 | ⚠️ 근거 못 찾음 |
| 콜드 스타트에서 **pandas/torch 지목** | ⚠️ 근거 못 찾음 — #620은 "의존성을 줄여라"까지만 |
| 워커 수와 **CPU limit**의 관계 | ⚠️ 근거 못 찾음 (메모리 쪽은 #9145로 해소됨 — §1-4 참조) |
| **Bean Validation vs Pydantic** — 에러 포맷(422/RFC 9457) 축 | ✅ **2차 회차에서 해소** (§2-2(1), 스레드 6건) |
| **Bean Validation vs Pydantic** — Java 개발자의 Pydantic 반응 | ✅ **2차 회차에서 해소** (§2-2(2), JSR-380 직접 거론 포함) |
| **커스텀 검증기** `ConstraintValidator` vs `field_validator` | ⚠️ **여전히 근거 없음** — 4개 경로 전부 0건. **두 커뮤니티가 서로를 비교하는 토론이 아예 형성돼 있지 않다.** 저자 1차 분석으로 채울 것 |
| Spring `ProblemDetail`을 **명시적으로 거론한** FastAPI 측 요구 | ⚠️ 근거 못 찾음 (RFC 번호로만 논의됨) |
| **Spring Security 필터 체인·`@PreAuthorize` → FastAPI 전환자의 체감** | ⚠️ **여전히 근거 없음** (fastapi-users Discussions "Spring" 검색 0건). §2-5에 새로 들어간 근거는 **"조립의 비용"에 대한 것이지 "Spring Security 사용자의 체감"이 아니다 — 계획에서 이 둘을 같은 절로 묶지 마라** |
| **보안 부품을 직접 조립하는 비용** (§2-5 신규) | ✅ 근거 강함 — python-jose/passlib 방치 사건 4개 스레드, 신고→문서변경 1년/15개월 |
| **Node 개발자의 전환 난이도** | ✅ **2차 회차에서 해소** — 양방향 근거 확보 (§2-3) |
| **Spring WebFlux/Reactor 경험자의 전환 난이도** | ⚠️ **여전히 근거 없음.** HN Algolia `webflux` 2,205건 중 상위 40건 전수 확인 + Discussions 검색 → **교차 경험담 0건.** Java 내부 Reactor 회의론은 있으나 **asyncio 대조가 아니다 — 섞지 마라** |
| **서블릿 스레드 모델 출신임을 밝힌** 실수 증언 | ⚠️ 근거 없음. 실수 패턴 자체는 풍부하나 **출신 귀속은 하지 마라** |
| **Spring Boot Actuator 대응물 부재** | ⚠️ 인접 증거만(#9148, upvote 56) |
| `application.yml` vs pydantic-settings | ⚠️ 근거 못 찾음 |
| **JUnit/MockMvc vs pytest/TestClient** | ⚠️ 근거 못 찾음 |
| Maven/Gradle/npm vs uv/poetry **락파일·모노레포** | ⚠️ 근거 못 찾음 |
| `@Transactional` 부재에 대한 **직접 인용** | ⚠️ 구조적 근거(#11107)만 있고 인용문은 없음 |
| **0.x 버전대 유지**에 대한 커뮤니티 의견 | ⚠️ 근거 못 찾음 |
| **FastAPI Cloud 상업화에 대한 반발** | ⚠️ **찾지 못함.** 존재는 확인, 비판적 반응은 확인 안 됨. **없는 백래시를 만들지 마라** |
| NestJS↔FastAPI 아키텍처 **토론** | ⚠️ 토론은 못 찾음. 유물(FastNest, 2026-04)로만 대체 |

### 구조적 편향 경고 (반드시 읽어라)
- **§3의 상당 부분이 여전히 HN 44816755 단일 스레드에서 나왔다.** 이 스레드는 "Litestar를 봐라"라는 글의 댓글이므로 **FastAPI를 떠나는 사람이 과대표집된 표본**이다. 균형추로 같은 스레드 안의 반론(jaza, no_carrier, croemer, whinvik, brokegrammer)과 프로덕션 참조 코드베이스(`polarsource/polar`, Airflow 언급)를 반드시 병기했다. **책에서도 병기하라.** (2차 회차로 §1·§2의 단일 스레드 의존은 크게 해소됐지만 **§3은 그대로다.**)
- **2차 회차에서 새로 생긴 편향:** §2-3의 async 비판 자료가 **"async는 과대평가됐다"는 논조의 스레드들**(HN 45106189, 47859442, 48281515, Lobsters oa1vf8)에 집중돼 있다. 이 스레드들은 제목부터 회의적이라 **async 옹호 측이 과소표집된다.** 균형추로 scuff3d(설계를 처음부터 async로 하면 간단해진다)·seabrookmx(JS 익숙하면 FastAPI가 매끄럽다)·leameow(색칠은 오히려 부작용을 드러내서 좋다)를 병기했다. **책에서 "커뮤니티는 async에 회의적이다"로 일반화하지 마라 — 표본이 그렇게 뽑혔을 뿐이다.**
- 언어 편중: 영어 소스가 압도적이다. 한국 소스는 velog 3건 + shipfriend 1건 + 파생/번역 1건이 전부이고, **OKKY·GeekNews·인프런은 본문을 못 열었다.** 한국 실무자의 **1차 증언**은 사실상 velog 3건뿐이다.
- 플랫폼 편중: HN + GitHub Discussions가 대부분. 두 곳 모두 **문제를 겪은 사람이 글을 쓰는 곳**이라 부정 편향이 구조적으로 존재한다. **"조용히 잘 쓰는 다수"는 이 문서에 나타나지 않는다.**
- **"목록만 확인" 항목의 숫자를 믿지 마라.** #9148을 직접 열어보니 upvote가 56이 아니라 18이었다(1차 회차 오류). §7의 "리드만 확보" 목록과 본문의 `(확인 필요 — 목록만 확인)` 항목들은 **전부 같은 위험을 안고 있다.** 인용하려면 반드시 원문을 열어라.

---

## 7. 출처 목록 (직접 열어서 읽은 것만)

### Hacker News
| URL | 내용 | 날짜 | 규모 |
|---|---|---|---|
| https://news.ycombinator.com/item?id=44816755 | "Litestar is worth a look" — FastAPI 비판/옹호의 최대 집결지. 전체 댓글 확보 | 2025-08-06 | 343점 / 83댓글 |
| https://news.ycombinator.com/item?id=44570215 | lutoma — FastAPI의 BDFL 개발 구조 vs Litestar 커뮤니티 주도 | 2025-07-15 | 댓글 |
| https://news.ycombinator.com/item?id=44571027 | robertlagrant — 거버넌스·버스 팩터 때문에 Litestar 선택 | 2025-07-15 | 댓글 |
| https://news.ycombinator.com/item?id=47364260 | "Show HN: Oxyde" — SQLModel 검증 무력화 주장, Pydantic/ORM 이중 모델 문제 | 2026-03-13 | 155점 / 81댓글 |
| https://news.ycombinator.com/item?id=48637393 | "Show HN: FastAPI Cloud is in public beta" — tiangolo 본인 소개 | 2026-06-22 | 5점 / 3댓글 |
| https://news.ycombinator.com/item?id=44816140 | com2kid — "Spring Boot has 10x the config... FastAPI has at least 3x the magic" + Node의 확장 단위 논거 | 2025-08-06 | 댓글 |

### GitHub — fastapi/fastapi Discussions (본문 확보)
| URL | 내용 | 날짜 |
|---|---|---|
| https://github.com/fastapi/fastapi/discussions/13125 | MissingGreenlet — AsyncAttrs lazy loading이 응답 직렬화에서 폭발 | 2024-12-30 |
| https://github.com/fastapi/fastapi/discussions/14137 | 0.118 회귀 — `yield` 이후 배경 태스크가 조용히 실행 안 됨 | 2025-10-01 (해결 2025-11) |
| https://github.com/fastapi/fastapi/discussions/13455 | 시계열 3.5만 건 — 검증 0.17s vs 직렬화 0.60s | 2025-03-05 ~ 2025-04-28 |
| https://github.com/fastapi/fastapi/discussions/11107 | `Depends` 컨텍스트 매니저 순서 변경 — 커밋이 세션 닫힘 뒤로 | 2024-02-07 |
| https://github.com/fastapi/fastapi/discussions/8054 | "Dependency Injection - Singleton?" — 요청 스코프 한계, 여전히 Unanswered | 2019-09-04 (답글 ~2024-11) |
| https://github.com/fastapi/fastapi/discussions/8433 | sync 엔드포인트 워커 불균형, AnyIO 40 스레드 상한 | 2022-12-08 |
| https://github.com/fastapi/fastapi/discussions/7439 | gunicorn vs 순수 uvicorn(k8s), "코어당 2+1" 경험칙 | 2020-05-26 (답글 ~2023-10) |
| https://github.com/fastapi/fastapi/discussions/9044 | `jsonable_encoder`가 이벤트 루프를 막는다 🕒 v1 시대 | 2020-04-07 |
| https://github.com/fastapi/fastapi/discussions/7320 | "마케팅과 성능이 안 맞는다" 🕒 수치 전부 2020~2022 | 2020-07-02 |
| https://github.com/fastapi/fastapi/discussions/6656 | 이모지 문서 논란 — 300+ 반응 후 일러스트로 교체 🕒 해소됨 | 2021-05-21 (답변 2022-08-17) |
| https://github.com/fastapi/fastapi/discussions/11828 | 미들웨어가 배경 태스크 예외를 삼킨다 — Starlette 쪽 문제로 판정 | 2024-07-11 (답변 2024-09-21) |
| https://github.com/fastapi/fastapi/discussions/9145 | gunicorn 워커 메모리 무한 증가 — 5년 뒤 `exception_handler` GC 문제로 지목, 재현 2건 | 2019-10-07 (답글 ~2024-08-27) |

### GitHub — 기타
| URL | 내용 | 날짜 |
|---|---|---|
| https://github.com/aws/aws-lambda-web-adapter/discussions/620 | FastAPI 콜드 스타트 9.9초 init 타임아웃 | 2025-11-10 |
| https://github.com/zhanymkanov/fastapi-best-practices | 커뮤니티 표준 구조 + async 3단 등급 (17.8k★) | 갱신일 미확인 |
| https://github.com/fastapi/fastapi/discussions/9148 | FastAPI 내부(검증·직렬화) 타이밍 노출 요청 — upvote **18**(1차 회차 "56"은 오류) 🕒 | 2019-11-10 ~ 2020-05 |
| https://github.com/trallnag/prometheus-fastapi-instrumentator/issues/370 | 라우터 구조 변경으로 `_IncludedRouter` AttributeError | **2026-06-14** ✅ 최신 |
| https://github.com/trallnag/prometheus-fastapi-instrumentator/issues?q=is%3Aissue+routes | #379(2026-06-25)·#388(2026-07-08) — 고친 뒤 다음 마이너에서 재발 | **2026-06~07** ✅ 최신 |
| https://github.com/fastapi/fastapi/issues/11143 | #11107에서 승격된 이슈. **Closed 확인, 종결 사유는 미확인** | 2024-02-14 |
| https://github.com/PythonNest/PyNest | NestJS 모듈·DI·데코레이터를 FastAPI 위에 재구현 (★859) | 마지막 활동 미확인 |
| https://github.com/fastapi/fastapi/discussions/9587 | `python-jose` 방치 신고 → 약 1년 뒤 PyJWT로 문서 변경 | 2023-05-29 ~ 2024-05-20 |
| https://github.com/fastapi/fastapi/discussions/11773 | `passlib` 방치 신고 → 약 15개월 뒤 pwdlib으로 변경, 직후 호환성 문제 재보고 | 2024-06-28 ~ 2025-10-25 |
| https://github.com/fastapi/full-stack-fastapi-template/discussions/1188 | python-jose **CVE** 지적, 공식 템플릿의 future-proof 요구. 1년 뒤 "지금은 뭘 써야 하냐" 재질문 | 2024-04-29 ~ 2025-04-10 |
| https://github.com/fastapi/fastapi/discussions/11380 | `passlib`이 FastAPI **자체 테스트 스위트**에도 있었음. 응답까지 약 14개월 | 2024-03-31 ~ 2025-05-26 |
| https://github.com/fastapi/fastapi/issues/643 | **422 vs 400 정전 스레드** — tiangolo의 근거 4개(리액션 13) + antonagestam 반박 | 2019-10-22 ~ 2022-12 |
| https://github.com/fastapi/fastapi/issues/1376 | "검증 에러 커스터마이징" — 5년치 우회법 전시장, 소스 직접 수정 고백 (리액션 15) | 2020-05-04 ~ 2021-04 |
| https://github.com/fastapi/fastapi/discussions/6695 | 422 문서 항목 제거법 — `FastAPI` 클래스 상속 + `openapi` 재작성 | 2021-06-29 ~ 2022-07 |
| https://github.com/fastapi/fastapi/issues/512 | RFC 7807 지원 요청. tiangolo "하위호환이 깨져서 안 했다" | 2019-09-07 ~ 2020-06 |
| https://github.com/fastapi/fastapi/discussions/14517 | RFC 9457 opt-in 재요청 (upvote 6) | **2025-12-13** ~ 2026-07-05 |
| https://github.com/fastapi/fastapi/pull/15951 | RFC 9457 구현 PR — **미머지 close, 프로세스 사유** | **2026-07-07** |
| https://github.com/pydantic/pydantic/discussions/8468 | Pydantic 에러 메시지가 사용자에게 못 보여줄 수준 (upvote 17) | 2024-01-02 |
| https://news.ycombinator.com/item?id=44656419 | HN "Keep Pydantic out of your Domain Layer" — Java/Python 정면 충돌 (94점/121댓글). JSR-380 직접 거론(44701062) | 2025-07-23 |
| https://news.ycombinator.com/item?id=29444847 | hiram112 — Java 개발자가 파이썬 서비스 인수 후 "Spring JEE 뺨친다" 🕒 | 2021-12-04 |
| https://discuss.python.org/t/add-virtual-threads-to-python/91403 | **Mark Shannon(CPython 코어) — "Java virtual threads가 더 낫다"** (274 posts/565 likes) | **2025-05-09 ~ 2026-02-14** |
| https://news.ycombinator.com/item?id=47859442 | HN "What async promised and what it delivered" (256점/307댓글) — Loom 대조, 디버깅 4단계 시나리오 | **2026-04-22** |
| https://news.ycombinator.com/item?id=45106189 | HN "Python has had async for 10 years – why isn't it more popular?" (324점/295댓글) | **2025-09-02** |
| https://news.ycombinator.com/item?id=48281515 | HN "What color is your function?" 재게시 (138점/189댓글) — Node↔Python 대비 | **2026-05-26** |
| https://lobste.rs/s/oa1vf8 | Lobsters "AsyncIO Thoughts" (48점/25댓글) — "인생 최악의 프로그래밍 경험" | 2023-06-10 |
| https://news.ycombinator.com/item?id=42171693 | HN "Threads Beat Async/Await" (Armin Ronacher, 171점/97댓글) | 2024-11-18 |
| https://github.com/fastapi/fastapi/discussions/8842 | sm-Fifteen의 async/sync 3분류 원전 | 2021-04-16 |
| https://github.com/fastapi/fastapi/discussions/14339 | 동기 OpenAI 클라이언트를 `async def`에 넣은 최신 사례 | **2025-11-12** |
| https://github.com/fastapi/fastapi/discussions/14603 | "개발 모드에서 이벤트 루프 블로킹 경고" 제안 + PoC | **2025-12-26** |

### Lobsters
| URL | 내용 | 날짜 |
|---|---|---|
| https://lobste.rs/s/2jwm1m/django_vs_fastapi_honest_comparison | Django vs FastAPI — 보안 조립 불안(antoinewdg), NestJS 혹평(alper) | ≈2025 (사이트 표기 "1 year ago") · 14점 / 23댓글 |
| https://lobste.rs/s/smuqhv/fastdepends_fastapi_di_system_cleared | `Depends`의 암묵적 마법 vs "Explicit is better than implicit" | ≈2022 (사이트 표기 "3 years ago") |

### Dev.to
| URL | 내용 | 날짜 |
|---|---|---|
| https://dev.to/hamza_elmouddane_1fb8c06/fastnest-bringing-nestjs-modular-architecture-to-fastapi-38hi | NestJS 모듈·DI·Guards·Interceptors·Pipes를 FastAPI에 이식하려는 시도 | 2026-04-28 |

### 한국 커뮤니티
| URL | 내용 | 날짜 |
|---|---|---|
| https://velog.io/@soondcuk/Fastapi-Spring-Boot-vs-Fastapi-개인적인-의견 | "이렇게 해도 돼..?" — 컨벤션 부재, 레퍼런스 부족, 메모리 불안 | 2025-01-20 |
| https://velog.io/@thedev_junyoung/SpringFastAPIFastAPI에서-Spring으로-마이그레이션하며-배운-점 | FastAPI→Spring 이주. 정작 JPA에서 N+1을 다시 겪음 | 2025-03-07 |
| https://velog.io/@koeunyeon/FastAPI-써-본-후기 | "스프링 부트의 파이썬 버전", entity/repository 부재, 결국 Flask로 회귀 🕒 | 2022-01-07 |
| https://okky.kr/questions/1473757 | "fastapi 동시요청시 blocking 이유" — 제목·존재만 확인, **본문 미확보** | ≈2023 (정확한 날짜 미확인) |
| https://news.hada.io/topic?id=6233 | "FastAPI의 시대. 아직도 Flask 쓰시나요?" — 제목·날짜·추천수만 확인, **댓글 미확보** 🕒 | 2022-03-26 · 23P · yunyun0505 |
| https://news.hada.io/topic?id=22402 | "Litestar는 한번 살펴볼 만함" — HN 논쟁이 한국 커뮤니티에 옮겨진 증거. **한국어 댓글 미확보** | 게시일 미확인 |
| https://shipfriend.dev/posts/why-use-fastapi-strengths-and-weaknesses | 서정우 — 약점으로 **비동기 미지원 라이브러리**("비동기를 지원하지 않는 라이브러리를 함께 사용하는 순간 비동기의 이점이 사라진다")와 **GIL** 지목. Spring Boot·NestJS와 비교표 있음 ⚠️ **성능 수치는 출처 불명이므로 인용 금지** | **2026-03-28** ✅ 최신 |
| https://13akstjq.github.io/TIL/post/2024-07-06-ThisisWhyFastAPIisNOTProduction-ReadyYet | DI 싱글턴 부재·라우트마다 반복 주입 비판 ⚠️ **PyNest 홍보 목적의 파생/번역 글 — 중립 증언 아님** | 2024-07-06 |
| https://www.inflearn.com/en/community/questions/1782043/... | 인프런 Q&A — 학습자의 첫 반응 *"보일러플레이트가 좀 많은데?"*. 답변은 일반론이라 인용 가치 낮음 | **게시일 미확인** |

### 라이브러리 문서 (커뮤니티는 아니지만 "불만의 물증"으로 사용)
| URL | 내용 | 시점 |
|---|---|---|
| https://dishka.readthedocs.io/en/stable/alternatives.html | `Depends`의 6대 한계 명문화 + 비교표 | 표 기준 시점 2024-03-08 |
| https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html | "DI는 Java 같은 정적 타입 언어에서 유행했다" — Python 진영의 저항 정서 | 문서 버전 4.49.1, 게시일 미확인 |

### 공식 문서 (커뮤니티 아님 — 대조용으로만)
| URL | 내용 | 확인 시점 |
|---|---|---|
| https://fastapi.tiangolo.com/deployment/server-workers/ | gunicorn 언급 없음. k8s는 컨테이너당 uvicorn 단일 프로세스 권고. **워커 수 권고 숫자는 없음** | 2026-07-25 직접 페치 |

### 리드만 확보 (제목·날짜만, 본문 미확보 — 후속 회차 표적)
fastapi/fastapi Discussions: #14623(BackgroundTask 경고 문서화, ~2025-12) · #8987(요청 실패 시 배경 태스크 미실행) · #10622(요청당 세션 관리) · #9082(OOM) · #7299(ASGI 서버 선택) · #9148(FastAPI 내부 타이밍 데이터 요청, upvote 56 — Actuator 공백의 정황) · #8165(직렬화 속도, upvote 29 🕒) · #10701 · #11790 · #9589 · #8187 · #7761 · #7319(CORS) · #15287(pyodbc + run_in_threadpool 스케일링, ~2026-04) · #16022(SQLAlchemy 모델 설계, 2026-07-18)

**후속 회차 우선순위:** (1) Reddit·Stack Overflow를 렌더링 가능한 도구로 재시도 — §2의 Bean Validation·Spring Security·테스트 항목이 여기 걸려 있다. (2) OKKY·GeekNews 본문을 브라우저 렌더링으로 확보 — 한국 독자용 오프닝 소재가 현재 velog 3건뿐이다. (3) #9082·#7299로 §1-4 마무리.
