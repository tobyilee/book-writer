# 이미 웹을 아는 개발자를 위한 FastAPI

**Spring Boot·Express에서 건너온 사람들의 실전 안내서**

Toby-AI

---

## 머리말

이 책은 FastAPI를 처음 만나는 사람을 위한 책이 아니다. 웹 애플리케이션을 이미 만들어 본 사람, 그것도 Java나 Node.js 같은 다른 생태계에서 만들어 본 사람을 위한 책이다.

그런 독자에게 필요한 것은 문법 설명이 아니다. 라우팅이 무엇인지, REST가 무엇인지, 의존성 주입이 왜 필요한지는 이미 안다. 진짜 궁금한 것은 따로 있다. **내가 알던 그 자리에 여기서는 무엇이 있는가.** DI 컨테이너가 하던 일은 누가 하는가. `@Valid`가 서 있던 자리에는 무엇이 오는가. 서블릿 스레드 풀에 해당하는 것은 어디에 있고, 그 숫자는 몇인가. 트랜잭션 경계는 누가 긋는가. Spring Security가 한 묶음으로 주던 것을 여기서는 어떻게 조립하는가.

이 책은 그 질문들에 답한다. 열네 개 장이 하나의 예제 애플리케이션 — 사내 이슈 트래커 `tracker` — 을 함께 키우면서, 익숙한 개념이 이 생태계에서 어디에 놓이는지를 하나씩 짚어간다.

한 가지 미리 밝혀둘 것이 있다. **이 책은 확인한 것과 확인하지 못한 것을 구분해서 쓴다.** FastAPI는 한 달에 서너 번에서 다섯 번씩 릴리스되는 프레임워크다. 그런 도구를 다루는 책이 "이렇다"라고 단정하면, 그 문장은 인쇄되는 순간부터 낡기 시작한다. 그래서 이 책은 버전과 시점을 함께 적고, 1차 소스를 각주로 남기고, 확인하지 못한 것은 확인하지 못했다고 적는다. 본문 곳곳의 각주 일흔여덟 개가 그 약속의 형태다.

읽는 순서는 자유롭다. 다만 5장(이벤트 루프)과 6장(데이터 계층)은 나머지 장들이 반복해서 되짚는 자리이니, 어느 장부터 펴든 그 둘은 언젠가 한 번 읽어두는 편이 낫다.

## 차례

1. **익숙한 웹, 낯선 땅** — FastAPI는 무엇 위에 서 있는가
2. **라우팅과 앱 구조** — `@RestController`가 사라진 자리
3. **Pydantic과 에러 계약** — 검증이 타입 시스템이 될 때
4. **`Depends`와 미들웨어** — 컨테이너 없는 의존성 주입
5. **이벤트 루프** — `def`와 `async def` 사이의 40
6. **데이터 계층** — JPA를 놓고 SQLAlchemy 2.0을 잡기
7. **실시간** — WebSocket, SSE, 그리고 스트리밍
8. **오래 걸리는 일** — 스케줄링, 백그라운드 작업, 태스크 큐, 대용량 업로드
9. **API 너머** — 화면을 붙이고, 다른 서비스와 말하기
10. **인증과 인가** — Spring Security를 직접 조립하기
11. **테스트** — 공식 문서가 `anyio`를 쓰는 이유
12. **CI/CD** — 락파일, 품질 게이트, 그리고 파이프라인
13. **컨테이너와 클라우드** — 어디에, 몇 개의 프로세스로 올릴 것인가
14. **숫자를 믿는 법** — 관측성, 성능, 그리고 이 도구와 함께 살아가기



# 1장. 익숙한 웹, 낯선 땅 — FastAPI는 무엇 위에 서 있는가

ASGI 명세 문서를 열면 첫머리에 이렇게 적혀 있다. **"Version: 3.0 (2019-03-20)"**. 2026년 7월에 조회한 결과가 그렇다. FastAPI가 딛고 선 바닥, 그러니까 파이썬 비동기 웹의 프로토콜 계약은 2019년 봄에 확정된 뒤로 버전 표기가 그대로다. 7년이 넘었다.

그 위층의 사정은 전혀 다르다. 2026년 2월부터 6월까지, FastAPI는 마이너 번호 하나가 올라가는 릴리스만으로 생태계를 세 번 흔들었다. 0.129.0(2026-02-12)에서 Python 3.9 지원을 끊었고, 0.132.0(2026-02-23)에서 `strict_content_type` 기본값을 True로 바꿔 Content-Type 헤더를 제대로 보내지 않는 요청을 거절하기 시작했고, 0.137.0(2026-06-14)에서는 라우터의 내부 구조를 평평한 리스트에서 트리로 바꿨다.

바닥은 7년 넘게 고정돼 있고, 그 위는 한 해의 절반도 안 되는 사이에 세 번 흔들린다. 이 대비가 이 책 전체의 좌표계다. 당신이 지난 몇 년간 쌓아온 웹 프레임워크 지식 중 어떤 것은 저 고정된 바닥에 대응해서 거의 그대로 옮겨오고, 어떤 것은 흔들리는 위층에 걸려 있어서 매년 다시 확인해야 한다. 그리고 어떤 것은 옮겨올 자리가 아예 없다. 그 셋을 구별하는 것이 이 책이 하려는 일의 전부라고 해도 좋다.

그러니 첫걸음은 문법이 아니라 지형이다. 이 도구가 무엇 위에 서 있는지부터 확인해보자.

## 하나를 배운다고 생각했는데 넷이었다

`uv add "fastapi[standard]"` 한 줄로 설치를 끝내고 나면, 우리는 흔히 "FastAPI를 배우기 시작했다"고 말한다. 이 표현은 정확하지 않다. 설치된 것을 층으로 그려보면 이렇게 생겼다.

```text
# (개념 설명용 — 파일 아님)
FastAPI            라우팅 · 검증 · 의존성 · OpenAPI 생성
  └─ Starlette     ASGI 앱 · 라우팅 · 미들웨어 · TestClient · WebSocket
       └─ ASGI 3.0 명세  (scope / receive / send)
            └─ uvicorn   ASGI 서버 (uvloop · httptools 선택)
  └─ Pydantic      검증 · 직렬화 (Rust 코어 pydantic-core)
  └─ anyio         스레드 오프로드의 실제 주체
```

FastAPI는 이 그림의 맨 윗줄 하나다. 라우팅과 미들웨어와 WebSocket과 테스트 클라이언트는 Starlette이 갖고 있고, 요청 본문을 파싱해 파이썬 객체로 만들고 응답을 JSON으로 만드는 일은 Pydantic이 하고, 동기 함수를 스레드로 밀어내는 일은 anyio가 한다. FastAPI가 하는 일은 그 셋을 엮어 타입 힌트 한 줄에서 검증·문서·의존성 해석까지 끌어내는 것이다.

이걸 왜 첫 절에서 짚느냐면, 앞으로 당신이 만날 문제의 상당수가 **FastAPI 문서에 답이 없기 때문**이다. 미들웨어가 왜 그렇게 생겼는지는 Starlette과 ASGI 명세를 봐야 알고, 검증 에러 메시지의 모양은 Pydantic 문서에 있고, 동시성이 왜 그 숫자에서 막히는지는 anyio 소스에 있다. 층을 타고 내려가는 일이 일상이라는 뜻이고, 처음에는 이게 꽤 번거롭게 느껴진다.

물론 잃는 것만 있는 건 아니다. 층이 얇게 나뉘어 있다는 건 각 층을 따로 읽을 수 있다는 뜻이기도 하다. 이 책이 소스 코드를 자주 인용하는 이유가 그것이다.

`[standard]`로 설치했을 때 실제로 딸려 오는 목록도 한 번 보고 넘어가자. 0.140.0 / 2026-07 기준으로 이렇다.

```text
fastapi-cli[standard]>=0.0.8, fastar>=0.9.0, httpx<1.0.0,>=0.23.0,
jinja2>=3.1.5, python-multipart>=0.0.18, email-validator>=2.0.0,
uvicorn[standard]>=0.12.0, pydantic-settings>=2.0.0, pydantic-extra-types>=2.0.0
```

> 출처: PyPI `fastapi` 0.140.0 `requires_dist`, https://pypi.org/pypi/fastapi/json (조회 2026-07-25)

템플릿 엔진(jinja2), 멀티파트 파서(python-multipart), 설정 로더(pydantic-settings)가 기본 세트에 들어 있다. 스타터 하나가 여러 라이브러리를 끌고 오는 구조는 익숙할 텐데, 여기서는 그 목록이 아홉 개라 전부 눈으로 셀 수 있다.

## 요청은 객체가 아니라 딕셔너리로 온다

이제 한 층 내려가서, 이 생태계에서 가장 오래된 계약을 보자. ASGI 애플리케이션은 딱 이렇게 생긴 것이다.

```text
coroutine application(scope, receive, send)
```

> 출처: ASGI 명세 (main), https://asgi.readthedocs.io/en/latest/specs/main.html (조회 2026-07-25)

명세의 설명을 그대로 옮기면, `scope`는 *"The connection scope information, a dictionary that contains at least a `type` key"*이고, `receive`는 *"an awaitable callable that will yield a new event dictionary when one is available"*이며, `send`는 *"an awaitable callable taking a single event dictionary as a positional argument"*다.

여기서 잠시 멈추고 자기가 아는 것과 대조해보자. 서블릿 컨테이너는 요청과 응답을 **객체 두 개**로 건네준다. `HttpServletRequest`에는 헤더를 꺼내는 메서드가 있고, `HttpServletResponse`에는 상태 코드를 쓰는 메서드가 있다. Node의 핸들러도 마찬가지로 `(req, res)`라는 객체 쌍을 받는다. 객체이므로 메서드가 붙어 있고, 메서드가 붙어 있으므로 "무엇을 할 수 있는지"가 타입에 적혀 있다.

ASGI는 그 자리에 **딕셔너리 하나와 async 콜러블 두 개**를 놓는다. 요청 정보는 메서드가 없는 평평한 딕셔너리이고, 본문을 읽는 것은 `receive`를 기다리는 일이며, 응답을 내보내는 것은 `send`에 이벤트 딕셔너리를 넘기는 일이다. 응답을 "돌려주는" 게 아니라 "보내는" 것이라는 점도 다르다.

HTTP 연결의 `scope`에 어떤 키가 들어 있는지 보면 감이 더 온다. `type`·`http_version`·`method`·`scheme`·`path`·`query_string`·`root_path`·`headers`·`client`·`server`·`state` 같은 것들이다. 서블릿에서 메서드로 꺼내 쓰던 것들이 전부 문자열 키가 됐다고 보면 얼추 맞는다. WebSocket 연결의 `scope`는 이 키들을 그대로 포함하고 클라이언트가 요청한 서브프로토콜 목록을 하나 더 갖는다 — 두 프로토콜이 같은 형태의 계약 위에 있다는 뜻이고, 7장에서 실시간 기능을 붙일 때 다시 만난다.

키 하나만 더 짚자. `root_path`의 명세 설명은 *"The root path this application is mounted at; same as `SCRIPT_NAME` in WSGI"*다. 애플리케이션이 어떤 경로 아래에 마운트돼 있는지를 알려주는 값이니, 서블릿 컨테이너에서 컨텍스트 경로가 놓이던 자리다. 리버스 프록시 뒤에서 서브 경로로 서비스할 때 링크와 문서 경로가 어긋나는 그 문제를 여기서는 이 값이 담당한다.

그렇다면 우리는 매번 딕셔너리를 파헤쳐야 할까? 다행히 아니다. Starlette이 `scope`/`receive`/`send`를 감싼 `Request`·`Response` 추상을 제공하고, FastAPI는 거기서 한 걸음 더 나아가 타입 힌트만 보고 필요한 값을 꺼내 준다. 평소에 우리가 만지는 건 이 편의 층이다.

그런데 그 편의 층은 끝까지 덮이지 않는다. 새는 곳이 있다. 미들웨어가 대표적이다. 서블릿 필터나 Express의 `next()`에 익숙하다면 "요청을 가로채서 뭔가 하고 다음으로 넘긴다"는 그림이 이미 머릿속에 있을 텐데, ASGI에서 그 "가로채기"는 결국 `receive`와 `send`를 감싸는 일이다. 그래서 미들웨어를 어떤 층에서 쓰느냐에 따라 할 수 있는 일과 치러야 할 비용이 달라진다. 이 이야기는 4장에서 제대로 한다. 동시성도 마찬가지다. 저 `application`이 코루틴이라는 사실 하나가 5장 전체를 만든다. 지금은 **요청·응답이 객체가 아니라 딕셔너리와 두 콜러블로 온다**는 그림만 챙겨두자.

## 고정된 계약, 2026년 상반기에 세 번 깨진 생태계

앞머리에서 꺼낸 세 번의 변경을 표로 놓으면 이렇다.

| 버전 | 날짜 | 무엇이 바뀌었나 |
|---|---|---|
| 0.129.0 | 2026-02-12 | Python 3.9 지원 중단 |
| 0.132.0 | 2026-02-23 | `strict_content_type` 기본 True |
| 0.137.0 | 2026-06-14 | 라우터 내부 구조를 트리로 변경 |

두 번째와 세 번째는 릴리스 노트 문장을 직접 보는 편이 낫다. `strict_content_type`에 대해 릴리스 노트는 이렇게 적었다.

> "Now FastAPI checks, by default, that JSON requests have a `Content-Type` header with a valid JSON value, like `application/json`, and rejects requests that don't. If the clients for your app don't send a valid `Content-Type` header you can disable this with `strict_content_type=False`."

CSRF 방어를 위한 합리적인 기본값 강화다. 동시에, 헤더를 대충 보내던 클라이언트가 있다면 업그레이드하는 순간 거절당한다는 뜻이기도 하다. 끄는 방법까지 릴리스 노트에 적어둔 그 친절함 자체가 "깨질 사람이 있다는 걸 안다"는 신호다.

0.137.0은 더 깊은 곳을 건드렸다.

> "Now `router.routes` is no longer a plain list of `APIRoute` objects, it can contain these intermediate objects that can contain additional routers, forming a tree.
> Any logic that depended on iterating on the `router.routes` directly would be affected..."

`router.routes`를 순회하던 코드는 영향을 받는다는 뜻이고, 대신 쓰라고 `iter_route_contexts()`가 제공된다. 애플리케이션 코드가 라우트 목록을 직접 순회하는 일은 흔치 않다. 그럼 누가 다치는가? 내 코드가 아니라, 내가 갖다 붙인 도구들이다. 그 파장이 어디까지 갔는지는 2장에서 기록으로 확인한다.

Spring Boot를 오래 써온 사람에게 이 대목이 가장 낯설 것이다. 당신은 아마 "메이저가 아니면 깨지지 않는다"를 전제로 업그레이드 정책을 짜왔을 것이다. 여기서는 그 전제가 성립하지 않는다. 버전 번호의 두 번째 자리가 올라갈 때마다 릴리스 노트를 읽어야 한다. 자동 업그레이드를 걸어두고 잊어버리는 운영은 곤란하다.

이 점을 한쪽으로만 말하면 부정확해진다. 같은 기간에 FastAPI는 SSE를 정식 지원 목록에 넣었고(0.135.0 / 2026-03), Pydantic의 Rust 직렬화를 응답 경로에 적용해 JSON 응답 성능을 끌어올렸다(0.130.0 / 2026-02). 릴리스 노트가 그 변경에 붙인 표현은 *"2x (or more) performance increase for JSON responses"*였다. 커뮤니티가 별도 라이브러리로 메워오던 자리를 코어가 흡수하는 일이 실제로 일어난다는 뜻이다. 빠르게 움직이는 것과 자주 깨지는 것은 같은 성질의 앞뒷면이다. 어느 한 면만 보여주는 책은 정직하지 않다.

그래서 이 책은 버전을 쓸 때마다 시점을 함께 적고 "최신"이나 "요즘"이라는 말은 쓰지 않는다. 이 문장의 기준은 **FastAPI 0.140.0 / 2026-07**이고, 당신이 읽는 시점에는 이미 몇 번 더 올라가 있을 것이다. 그건 이 도구를 쓰는 비용이다. 알고 시작하는 편이 낫다.

## 0.x 위에 선 1.x — 버전 지형 읽기

버전 이야기가 나온 김에 이 스택의 번호를 한자리에 모은다. 2026년 7월 기준이다.

| 구성요소 | 버전 | 릴리스 |
|---|---|---|
| FastAPI | 0.140.0 | 2026-07-24 |
| Starlette | 1.3.1 | 2026-06-12 |
| Pydantic | 2.13.4 | 2026-05-06 |
| uvicorn | 0.51.0 | 2026-07-08 |
| anyio | 4.14.2 | 2026-07-12 |

뭔가 이상하지 않은가? **FastAPI는 아직 0.x인데, 그 아래층인 Starlette은 이미 1.x다.** Starlette은 2026-03-22에 1.0.0을 냈다. 프로젝트 창설 이래 첫 stable 릴리스다. 위층이 0.x, 아래층이 1.x — 성숙도 표기가 뒤집혀 있는 셈이다.

"FastAPI는 아직 0.x라서 프로덕션에 쓰기 불안하다"는 말을 들어본 적 있을 것이다. 이 표를 보고 나면 그 말이 조금 다르게 들린다. 버전 번호는 코드의 안정성이라기보다 프로젝트가 스스로에게 부여한 호환성 약속의 등급에 가깝고, 그 약속이 운영에서 무엇을 뜻하는지는 위에서 본 것처럼 릴리스 노트를 직접 읽어야 알 수 있다. 판단은 여기서 내리지 않겠다. 재료를 책 전체에 걸쳐 모아두고 14장에서 정면으로 다시 꺼낸다.

지형에서 하나 더 챙길 것이 있다. FastAPI 0.140.0의 `requires_python`은 `>=3.10`이다. 그런데 Python 3.10의 지원 종료일은 **2026-10-31**이다. 프레임워크가 허용하는 최소 버전과 언어의 수명이 맞닿아 있다는 뜻이다. 최소선을 그대로 따라가면 새 프로젝트를 시작하자마자 인터프리터 EOL을 걱정하게 된다. 그래서 이 책의 예제는 **Python 3.12+**를 전제한다.

의존성 핀에도 알아둘 구석이 있다. FastAPI는 Starlette을 `starlette>=0.46.0`으로만 핀한다. 1.x를 강제하지 않는다는 뜻이고, 따라서 팀의 락파일에 0.4x가 들어 있을 수도 1.x가 들어 있을 수도 있다. "FastAPI를 최신으로 올렸으니 Starlette도 1.x겠지"라고 넘겨짚지 말고, 문제가 생기면 락파일에서 실제 버전을 확인하는 습관을 들이자. 이런 확인이 필요하다는 것 자체가 조립체 위에서 일한다는 뜻이다.

사실 하나만 덧붙인다. Starlette과 uvicorn의 저장소는 `encode` 조직에서 `Kludex`로 옮겨졌다. 경위는 확인하지 못했으니 사실만 적어둔다.

## `tracker`, 그리고 uv라는 자리

지형 이야기는 여기까지 하고, 이제 손을 움직이자. 이 책은 1장부터 14장까지 **하나의 애플리케이션**을 키운다. 사내 이슈 트래커 `tracker`다. 프로젝트가 있고, 프로젝트에 이슈가 달리고, 이슈에 댓글과 라벨과 첨부가 붙고, 상태가 바뀌면 알림이 나가는 앱이다.

| 엔티티 | 설명 |
|---|---|
| `User` | 사용자 |
| `Project` | 프로젝트. 이슈를 담는다 |
| `Issue` | 이슈. 상태·우선순위·담당자를 갖는다 |
| `Comment` | 이슈에 달리는 댓글 |
| `Label` | 이슈에 붙이는 라벨 (이슈와 N:M) |
| `Attachment` | 이슈에 첨부되는 파일 |

도메인 설명은 이 표가 전부다. 당신은 이미 이런 앱을 써봤고 아마 비슷한 걸 만들어도 봤다. 도메인이 낯설지 않아야 주의력이 FastAPI 쪽에 온전히 쓰인다. 앞으로 "이슈에 댓글을 단다" 정도의 한 줄이면 충분할 것이다.

그럼 프로젝트를 어떻게 시작하는가. 여기서 **uv**를 만난다. 당신의 어휘로 옮기면 **Maven·Gradle·npm이 서 있던 자리**다. 2026-07 기준으로 FastAPI 공식 문서가 예제 명령을 uv 기준으로 개편했으니, 문서를 따라 읽을 때도 계속 만나게 된다. 대응표 하나로 정리하자.

| 하려는 일 | Maven / Gradle | npm | uv |
|---|---|---|---|
| 의존성 추가 | `pom.xml` 편집 후 재빌드 | `npm install {패키지}` | `uv add {패키지}` |
| 프로젝트 환경에서 명령 실행 | `mvn exec` / `gradle run` | `npm run {스크립트}` | `uv run {명령}` |
| 의존성 매니페스트 | `pom.xml` | `package.json` | `pyproject.toml` |

설치 방법이나 가상환경 개념은 설명하지 않겠다. 이미 의존성 관리 도구를 여러 개 써본 사람에게는 이 표의 대응 관계면 충분하고, 나머지는 필요할 때 문서를 보면 된다. 지금 필요한 건 딱 두 줄이다.

```bash
uv add "fastapi[standard]"
uv run uvicorn tracker.main:app --host 127.0.0.1 --port 8000
```

첫 줄이 `pyproject.toml`의 의존성 목록과 `uv.lock`을 갱신한다. 둘째 줄이 uvicorn으로 앱을 띄운다. `tracker.main:app`은 "`tracker.main` 모듈의 `app` 객체를 ASGI 애플리케이션으로 삼으라"는 뜻이니, 앞 절에서 본 `application(scope, receive, send)` 계약의 그 `application`을 가리키는 셈이다.

그럼 `app`을 만들자. 이 책의 첫 코드다.

> **📐 저자 설계 —** 아래 모듈 배치와 헬스 엔드포인트 경로는 FastAPI 공식 권장이 아니라, 이 책이 14장까지 하나의 앱을 키우기 위해 정한 약속이다.

```python
# src/tracker/main.py
from fastapi import FastAPI

app = FastAPI(title="tracker")


@app.get("/healthz", tags=["health"])
async def healthz() -> dict[str, str]:
    return {"status": "ok"}
```

열 줄이 안 된다. 스프링에서 애플리케이션 클래스와 컨트롤러를 하나씩 만드는 것, Express에서 `app`을 만들고 라우트를 하나 다는 것과 비슷한 분량이다. 익숙한 만큼 낯선 것만 짚자.

`@app.get`은 애너테이션이 아니라 데코레이터이고, 클래스가 아니라 **함수**에 붙는다. `@RestController`가 클래스에 붙어 그 클래스를 빈으로 등록하고 요청을 매핑하던 구조와는 출발점이 다르다. 여기서는 등록 단위가 함수 하나다. 그리고 반환값이 `dict`인데도 이걸 JSON으로 만드는 코드가 없다. 직렬화는 프레임워크가 한다. 지금은 `dict` 하나라 티가 안 나지만, 3장에서 Pydantic 모델을 반환하기 시작하면 반환 타입 한 칸에 검증·직렬화·문서 생성이 한꺼번에 붙는다는 걸 알게 된다.

경로 이름도 미리 정해뒀다. `/healthz`다. 13장에서 컨테이너에 올릴 때 liveness와 readiness를 나누게 되는데, 그때 이 경로를 그대로 쓰고 `/ready`를 곁에 추가한다. 나중에 이름을 바꾸면 매니페스트와 문서가 어긋나니 지금 정해두자.

앱을 띄우고 브라우저로 `/docs`를 열어보자. 아무것도 설정하지 않았는데 API 문서가 이미 떠 있다. FastAPI가 OpenAPI 3.1.0 문서를 함수 시그니처에서 만들어낸 결과다. 이 자동 문서는 이 프레임워크의 가장 큰 자랑거리이면서, 나중에 우리를 가장 성가시게 하는 것이기도 하다. 그 아이러니는 3장에서 만난다.

## 이 책이 가는 길과 가지 않는 길

빈 프로젝트 하나와 엔드포인트 하나가 생겼다. 여기서 14장까지 무엇을 하게 되는지 지도를 펴두자. 아는 장을 건너뛰며 읽을 사람에게는 이 지도가 목차보다 쓸모 있을 것이다.

**2장부터 4장까지는 번역이 비교적 잘 되는 구간이다.** 라우터로 앱을 쪼개고 설정을 분리하고(2장), Pydantic으로 요청·응답 스키마와 에러 계약을 세우고(3장), `Depends`로 의존성을 주입한다(4장). 아는 개념에 새 이름이 붙는 경험이 이어진다. 다만 각 장의 후반부에서 균열이 하나씩 드러난다 — 서비스 레이어를 둘 것인가에 정답이 없다는 것, 검증 실패가 왜 422인지, `Depends`에 자동 와이어링이 없다는 것.

**5장과 6장이 이 책의 등뼈다.** 함수 앞에 `async`를 붙이느냐 마느냐가 성능이 아니라 장애의 문제가 되는 이유를 소스까지 따라가 확인하고(5장), `@Transactional`이 없는 세계에서 세션과 트랜잭션 경계를 직접 긋는다(6장). 이 책이 가장 많은 지면을 쓴 자리다. 순서도 중요하다 — 비동기 모델을 모른 채 비동기 세션을 읽으면 그저 마법으로 보인다.

**7장부터 9장은 시야를 옆으로 넓힌다.** 실시간 연결(7장), 오래 걸리는 일(8장), JSON API가 아닌 것들 — 서버 렌더링 화면·GraphQL·다른 서비스 호출(9장). 앞에서 얻은 지식을 다른 모양으로 재사용하는 훈련이다.

**10장부터 14장은 톤이 달라진다.** 인증과 인가를 직접 조립하고(10장), 테스트를 세우고(11장), 파이프라인에 태우고(12장), 컨테이너로 구워 어딘가에 올리고(13장), 올린 것을 관찰하고 판단한다(14장). 앞의 절반이 "어떻게 쓰는가"였다면 여기는 "무엇을 감당할 것인가"에 가깝다.

가지 않는 길도 밝혀두자. 파이썬 기본 문법, REST와 HTTP 기초는 다루지 않는다. `async`/`await` 문법 입문도 없다 — 5장이 다루는 건 문법이 아니라 FastAPI가 그 문법을 어떻게 처리하는가다.

그리고 다루지 않기로 한 것이 두 가지 더 있다. **API 버저닝 전략**과 **캐시 아키텍처**다. 둘 다 실무에서 중요한 주제이지만, 이 책을 준비하며 모은 자료 안에 FastAPI 맥락의 근거가 거의 없었다. 근거 없이 그럴듯한 조언을 쓰는 것보다 안 쓰는 편이 낫다고 판단했다. 그래서 예제 앱의 경로에도 버전 접두사가 없다. 책이 다루지 않기로 한 것을 코드가 슬쩍 주장하게 두면 곤란하니까.

---

지도를 다 폈으니 이제 접자. 지금 우리 손에는 열 줄이 안 되는 `main.py`와 `/healthz` 하나가 있다. 여기에 이슈를 만들고 조회하는 엔드포인트를 붙이기 시작하면, 파일이 하나에서 여럿으로 갈라지는 순간이 곧 온다. 그때 우리가 마주할 첫 질문은 문법이 아니라 구조다. 그리고 이 생태계에는 그 질문에 대해 미리 준비된 답이 없다. 아무도 그어주지 않은 선을 우리 손으로 긋는 일부터 시작해야 한다는 뜻이다.


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


# 4장. `Depends`와 미들웨어 — 컨테이너 없는 의존성 주입

2장에서 골격만 잡아둔 `IssueService`를 이제 여러 라우터에서 실제로 쓰려 한다고 해보자. 지금까지 이건 고민거리가 아니었을 것이다. 클래스에 애너테이션 한 줄을 붙여 컨테이너에 올려두고, 쓰는 쪽에서는 필드에 주입 애너테이션 하나. 그게 어디서 왔는지는 물어볼 필요조차 없었다.

FastAPI에도 의존성 주입이라 부르는 장치가 있다. 이름은 `Depends`다. 그런데 그 이름을 보고 컨테이너를 기대한 손은 대개 두어 시간 안에 벽에 부딪힌다. 서비스 객체를 앱 시작 때 한 번만 만들어두려는 순간이 특히 그렇다.

무엇이 없어서 그럴까. 그리고 필터 체인을 쓰던 자리는 이제 무엇이 채우고 있을까.

## `Depends`가 실제로 하는 일

시그니처부터 보는 편이 빠르다. 0.140.0 태그 소스에서 뽑은 것이다.

```python
# (개념 설명용 — 파일 아님)
def Depends(
    dependency: Callable[..., Any] | None = None,
    *,
    use_cache: bool = True,
    scope: Literal["function", "request"] | None = None,
) -> Any: ...
```

> 출처: fastapi 0.140.0 태그 소스 `fastapi/param_functions.py` (조회 2026-07-25)

첫 인자가 전부다. 콜러블 하나. `Depends(get_settings)`라고 적으면 FastAPI는 경로 함수를 부르기 직전에 `get_settings`를 호출하고, 그 반환값을 해당 파라미터에 넣어준다. 타입으로 무언가를 검색하지 않는다. 등록부를 뒤지지도 않는다. **적혀 있는 함수를 호출할 뿐이다.**

그러면 이게 왜 "주입"인가? 그냥 함수 호출 아닌가?

재귀 때문이다. 의존성 함수도 자기 파라미터를 가질 수 있고, 그 파라미터에 또 `Depends`가 붙을 수 있다. FastAPI는 시그니처를 읽어 의존성을 찾고, 그 의존성의 시그니처를 다시 읽어 또 찾는다. 잎에 닿을 때까지 내려갔다가 값을 들고 거슬러 올라온다. 컨테이너와 결과가 비슷해 보이는 이유가 이것인데, 그 트리를 만드는 재료는 **등록 정보가 아니라 함수 시그니처**다.

`use_cache=True`도 짚어두자. 한 요청 안에서 같은 의존성이 세 군데에 등장해도 함수는 한 번만 호출되고 결과가 공유된다. 편리하다. 그런데 이 캐시의 수명이 요청 하나라는 점이 곧 다음 절을 통째로 만들어낸다. 프로토타입도 아니고 싱글턴도 아닌, 오직 하나의 스코프만 있는 셈이다.

세 번째 인자 `scope`는 조금 뒤에 따로 다룬다. 방금 말한 스코프와는 다른 물건이다.

## 컨테이너가 없다는 말의 정확한 뜻

"FastAPI에는 DI 컨테이너가 없다"는 문장은 인터넷에 널려 있다. 정확히 옮기지 않으면 엉뚱한 기대를 하게 된다.

별도의 DI 라이브러리인 dishka가 자기 문서의 대안 비교 항목에서 FastAPI의 `Depends`를 평가한 대목이 이 한계를 가장 정확히 짚는다.[^4-7]

> "You have to declare each dependency with `Depends` on each level of application. So either your business logic contains details of IoC-container or you have to duplicate constructor signatures."

애플리케이션의 모든 층에서 의존성을 다시 선언해야 한다는 것. 그래서 비즈니스 로직이 주입 도구의 흔적을 갖게 되거나, 아니면 생성자 시그니처를 계속 복제하게 된다는 것. (게시 시점을 확인하지 못했으니 생태계의 현재 평가로는 읽지 말자. 논지 자체는 코드로 확인된다.)

정리하면 이렇다. **없는 것은 자동 와이어링(auto-wiring)이다.** 타입만 보고 알아서 찾아 꽂아주는 층이 없다. 배선은 사람이 적는다.

| 물어보는 것 | DI 컨테이너 | `Depends` |
|---|---|---|
| 무엇을 넣을지 어떻게 아는가 | 등록된 것을 타입으로 찾는다 | 파라미터에 적힌 함수를 호출한다 |
| 배선은 어디에 적혀 있는가 | 등록하는 한 곳 | 쓰는 자리마다 |
| 인스턴스는 얼마나 사는가 | 스코프로 지정한다 | 요청 하나 (`use_cache`) |

세 번째 행이 실무에서 가장 먼저 아프다. 커넥션 풀이나 HTTP 클라이언트처럼 앱이 사는 동안 하나여야 하는 물건을 `Depends`만으로는 표현할 수 없다. 이 질문은 이슈 #8054에 올라와 있고, 확인된 답은 내장 캐싱이 단일 요청 안에서만 유효하다는 사실뿐이다. 그동안 커뮤니티는 우회법을 층층이 쌓았다 — 함수 결과 캐시, 시작 시점 인스턴스화, `app.state`, 종료 스택과 앱 상태의 조합. 놀랍게도 그 이슈는 2026년 현재까지 **Unanswered** 상태다. 여러 해가 지나도록 공식 답이 붙지 않았다는 사실 자체가 지금의 현황이다.

여기서부터는 **저자 해석**이다. 근거는 여론조사가 아니라 종류가 다른 자국 두 개다.

한쪽은 **유물**이다. 2026-04-28에도 누군가 NestJS의 모듈 시스템과 DI 컨테이너, Guards·Interceptors·Pipes를 그리워하며 FastAPI 위에 그것을 얹는 프로젝트를 공개했다. **단일 저자의 프로젝트이지 커뮤니티 합의가 아니다.** 그래도 2026년에도 누군가 그 필요를 느꼈다는 것만은 데이터다. 2장의 rmonvfer가 "프레임워크 위에 프레임워크를 하나 더 얹었다"고 고백한 것도 같은 종류다.

다른 쪽은 **발언**이다. Lobsters의 한 개발자는 `Depends`가 시그니처를 읽어 알아서 트리를 만드는 그 암묵성이 "명시적인 편이 암묵적인 것보다 낫다"는 파이썬의 격언에 어긋난다고 지적했다. 마법이 과하다는 쪽이다. 한 사람의 발언이니 진영의 목소리로 부풀리지는 말자.

같은 장치를 놓고 한쪽은 부족하다 하고 한쪽은 과하다 한다. 무엇이 옳은지 정하는 대신, **당신이 어느 쪽에서 걸어 들어왔는지를 알고 시작하는 것**이 이 도구를 다루는 첫 단계다.

## 그래서 배선을 이름으로 만든다

자동 와이어링이 없다는 건 실무적으로 한 가지를 뜻한다. **같은 배선을 여러 번 적게 된다.** 그리고 여러 번 적히는 것은 언젠가 서로 달라진다. 세션을 받는 엔드포인트 스무 개 중 셋만 다르게 받고 있는 상태를 떠올려보자.

`tracker`는 배선을 `deps.py` 한 파일에 모으고, 각 배선에 이름을 준다. 타입 별칭으로.

> **📐 저자 설계 —** 아래 의존성 함수와 별칭 이름은 FastAPI 공식 권장이 아니라, 이 책이 `tracker` 전체에서 쓰기로 정한 한 가지 안이다. 이후 모든 장이 이 이름만 쓴다.

```python
# src/tracker/deps.py
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.user import User
from tracker.services.issue import IssueService
from tracker.settings import Settings, get_settings


async def get_session() -> AsyncIterator[AsyncSession]:
    ...
    yield


async def get_current_user() -> User:
    raise NotImplementedError


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_issue_service(session: SessionDep) -> IssueService:
    return IssueService(session)


IssueServiceDep = Annotated[IssueService, Depends(get_issue_service)]
```

먼저 두 함수는 스텁이다. `get_session`은 몸통에 `...`만 두고 `yield`의 존재와 반환 타입만 확정했다. 세션이 어디서 오는지는 6장이 채운다. `get_current_user`는 아예 예외를 던진다 — 스텁이 조용히 `None`을 돌려주다 한참 뒤 엉뚱한 곳에서 터지는 것보다, 부르는 즉시 크게 터지는 편이 낫다. 몸통은 10장이 채운다. 두 경우 모두 **이름과 반환 타입은 바뀌지 않는다.** 호출부가 별칭을 거쳐 들어오니 계약은 그 둘이고, 파라미터와 몸통은 구현이다. 뒤 장은 완성하지 재정의하지 않는다. `User`를 미리 import하는 것도 같은 이유다 — 클래스는 6장에서 생기지만 이름은 지금 확정해둔다.

그리고 `get_issue_service`의 파라미터가 `SessionDep`이다. 즉 **의존성이 의존성을 요구한다.** 앞 절에서 말한 재귀가 눈에 보이는 형태로 나타난 것이고, 컨테이너 없이 조립이 되는 이유가 이 다섯 줄에 다 들어 있다 — 함수가 함수를 부르고, 그 조합에 이름을 붙였을 뿐이다. `Depends`를 컨테이너가 아니라 **함수 조합기**로 다시 보자는 말이 이 뜻이다.

그리고 별칭. 그 조합에 `IssueServiceDep`이라는 이름을 붙여두면 라우터 쪽 코드는 이렇게 짧아진다.

```python
# src/tracker/api/issues.py
from tracker.deps import IssueServiceDep
from tracker.schemas.issue import IssueCreate, IssueRead

# ...(2장, 생략)


@router.post("/", status_code=201, response_model=IssueRead)
async def create_issue(payload: IssueCreate, issues: IssueServiceDep) -> IssueRead:
    ...
```

요청 본문 하나와 서비스 하나, 둘 다 타입만 적혀 있다. 배선 코드가 시그니처 뒤로 사라지고, 시그니처만 읽어도 이 엔드포인트가 무엇을 필요로 하는지 드러난다.

한 가지 더. `get_issue_service`는 아무 I/O도 하지 않는데 `async def`로 뒀다. 취향이 아니라 계산이다. 동기 의존성이 무엇을 대가로 지불하는지는 5장이 숫자로 보여준다.

값을 돌려주지 않고 검사만 하는 의존성은 경로 데코레이터나 `APIRouter`의 `dependencies` 인자에 실어 파라미터 목록을 더럽히지 않고 붙인다. 인가가 그런 물건이고, 10장이 여기를 쓴다.

## `yield`, 그리고 언제 끝나는가

세션이나 파일 핸들처럼 열었으면 닫아야 하는 것은 값을 돌려주는 것만으로 끝나지 않는다. `tracker`의 `get_session`이 `return`이 아니라 `yield`를 쓰는 이유가 이것이다. `yield` 앞은 준비, 뒤는 정리다.

그런데 조금 더 깊이 들어가보자. **정리 코드는 정확히 언제 도는가?** 경로 함수가 끝난 직후인가, 응답이 클라이언트로 나간 뒤인가? 사소해 보인다면 `@Transactional`과 OSIV를 두고 벌어졌던 논쟁을 떠올려보자. 세션이 언제 닫히느냐는 응답을 만드는 동안 지연 로딩이 되느냐를 결정하고, 그건 곧 응답 직렬화가 성공하느냐의 문제다.

0.140.0 / 2026-07 기준으로 `Depends`에는 그 시점을 고르는 `scope` 파라미터가 있다. 공식 문서의 설명은 이렇다.[^4-6]

> `"function"`: ... end the dependency after the *path operation function* ends, but **before** the response is sent back to the client.
> `"request"`: ... end **after** the response is sent back to the client.

이 파라미터의 배경에는 이슈 #11107(2024-02)이 있다. `yield` 의존성의 정리 순서가 뒤집혀 커밋 전에 세션이 닫히는 문제였고, #11143으로 승격됐으며 확인 시점에 Closed 상태다. 그리고 2025-10의 다른 이슈에서 tiangolo가 제시한 처방이 `Depends(func, scope="function")`이었다.

그런데 **#11143이 어떤 사유로 닫혔는지, 어떤 PR이 병합됐는지를 이 책은 확인하지 못했다.** 그래서 "`scope`가 #11107을 해결했다"고는 쓰지 않겠다. 성립할 가능성이 높다고 보지만 릴리스 노트로 확인하기 전까지는 미확정이고, 이렇게 반올림하는 습관이 기술서를 못 믿게 만든다.

결론은 그래서 보수적이다. **`tracker`의 표준형은 평범한 `Depends(get_session)`이다.** 새로 생긴 파라미터를 관용구로 승격시키는 것은 그것이 무엇을 해결했는지 확인된 다음의 일이다. 이 파라미터는 6장에서 다시 꺼낸다.

## 필터 체인을 쓰던 자리

`Depends`가 채우지 못하는 자리가 하나 있다. 모든 요청에, 라우팅되기 전에 일어나야 하는 일이다. 요청 ID를 붙이고, 접근 로그를 남기고, 응답 헤더를 손보는 것들. 당신은 이걸 필터나 인터셉터로 해왔을 것이다. 요청·응답·다음 고리 세 가지를 받아 처리하고 넘기던 그 구조다.

ASGI에서 그 자리를 채우는 것은 미들웨어이고, 생김새는 1장의 계약에서 곧바로 나온다. **미들웨어는 앱을 감싼 또 하나의 앱이다.** `scope`·`receive`·`send`를 받아 필요한 일을 하고 안쪽 앱에 그대로 넘긴다.

작성 형태는 두 가지다. 하나는 그 계약을 날것으로 구현하는 순수 ASGI 미들웨어다.

```python
# (개념 설명용 — 파일 아님)
from starlette.types import ASGIApp, Scope, Receive, Send

class ASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)
```

> 출처: Starlette 공식 문서 Middleware, https://www.starlette.io/middleware/ (조회 2026-07-26)

다른 하나는 `BaseHTTPMiddleware`를 상속해 `dispatch(request, call_next)`를 구현하는 형태다.[^4-1] 이쪽은 `Request` 객체를 받고 `call_next(request)`를 `await`해 `Response`를 얻는다.

둘의 차이는 어디까지 말할 수 있을까. 안전한 것은 둘이다.

첫째, 실행 시점은 라우팅 바깥이다. Starlette 문서가 정리한 스택 순서는 서버 에러 처리 → 사용자가 선언한 미들웨어(선언 순서대로) → 예외 처리 → 라우팅 → 엔드포인트다.[^4-1] 미들웨어는 어느 경로로 갈지 정해지기 전에 돈다. 라우팅 결과에 따라 다르게 굴고 싶다면 여기가 아니다.

둘째, 적용 범위가 다르다. 순수 ASGI 형태는 `scope`를 그대로 받으므로 `scope["type"]`을 보고 HTTP 연결인지 WebSocket 연결인지 구분해 다룰 수 있다. 반면 `dispatch` 형태는 요청 하나에 응답 하나가 대응하는 모양으로 쓰여 있다. 7장에서 WebSocket에도 무언가를 걸어야 할 때 이 차이가 선택을 결정한다.

정직하게 밝혀두자. `BaseHTTPMiddleware`에 이런저런 한계가 있다는 이야기가 돌아다니지만, **이 책은 그 한계를 1차 소스로 확인하지 못했다.** 확인하지 못한 목록을 옮겨 적는 대신 여기서 멈춘다.

`tracker`의 첫 미들웨어는 요청 ID를 붙인다. 3장의 에러 응답에 있던 `request_id`, 그 값을 심는 자리가 여기다.

> **📐 저자 설계 —** 아래 미들웨어는 FastAPI가 제공하는 것이 아니라, 3장이 정한 에러 응답 계약을 채우기 위해 이 책이 작성한 것이다.

```python
# src/tracker/middleware.py
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request, call_next):
        request_id = request.headers.get(self.header_name) or uuid4().hex
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[self.header_name] = request_id
        return response
```

들어온 요청에 이미 ID가 붙어 있으면 그걸 쓰고 없으면 만든다. 앞단 프록시나 게이트웨이가 붙여 보낸 값을 버리지 않기 위해서다. 심는 곳은 `request.state`이고, 3장의 예외 핸들러가 정확히 거기서 값을 꺼낸다. 14장에서는 이 값이 로그와 요청을 잇는 열쇠가 된다.

등록은 `main.py`에서 한 줄이다.

```python
# src/tracker/main.py
from tracker.middleware import RequestIdMiddleware

# ...(3장, 생략)

app.add_middleware(RequestIdMiddleware)
```

`add_middleware`를 쓰는 이유는 공식 문서가 밝혀두었다 — 이렇게 등록해야 *"the internal middlewares handle server errors and custom exception handlers work properly"*.[^4-2] 내부 미들웨어와 예외 핸들러가 제대로 맞물리게 해준다는 뜻이다.

그렇다면 횡단 관심사를 미들웨어와 `Depends` 중 어디에 둘까. 기준은 단순하다. 모든 요청에 예외 없이 적용돼야 하고, 라우팅 전에 일어나야 하고, 응답 헤더를 손대야 한다면 미들웨어다. 반대로 **특정 라우터에만 걸리고, 값을 돌려줘야 하고, 시그니처에 타입으로 드러나야 하고, 테스트에서 갈아 끼워야 한다면 `Depends`다.** 인증된 사용자를 꺼내는 일이 정확히 후자다.

## 예외 핸들러는 어디에 등록되는가

`@ControllerAdvice`가 있던 자리다. 응답 계약 자체는 3장이 끝까지 책임지므로 여기서는 메커니즘만 본다.

등록 방법은 두 갈래고 결과는 같다. 3장에서 쓴 데코레이터 `@app.exception_handler(TrackerError)`, 그리고 `FastAPI(...)` 생성자의 `exception_handlers` 인자다. 후자는 2장에서 훑어본 생성자 파라미터 목록에 들어 있고, 핸들러를 상태 코드로도 예외 클래스로도 걸 수 있다.[^4-4]

해석 규칙 하나를 못 박아두자. **등록한 예외 클래스의 하위 클래스까지 같은 핸들러가 받는다.** 핸들러 조회가 예외 타입의 MRO를 거슬러 올라가며 등록부를 찾기 때문이다.[^4-5] 공식 문서도 같은 성질 위에 서 있다 — `HTTPException` 핸들러를 걸 때 *"you should register it for Starlette's `HTTPException`"*이라고 권하고, FastAPI의 `HTTPException`이 그 클래스를 상속한다고 함께 밝힌다.[^4-4] 3장이 핸들러를 셋으로 묶어둘 수 있었던 근거가 이것이다.

앞서 인용한 공식 문서의 한 줄이 말해주듯 예외 핸들러는 미들웨어 스택 안쪽에서 동작한다. 그래서 미들웨어가 `request.state`에 심어둔 요청 ID를 예외 핸들러가 읽을 수 있다.

## 앱이 사는 동안

이제 앞에서 미뤄둔 문제로 돌아오자. 요청보다 오래 사는 물건들 — HTTP 클라이언트, 커넥션 풀 — 은 어디에 두는가.

`lifespan`이다. 앱이 뜰 때 한 번 열고, 내려갈 때 한 번 닫는다.

> **📐 저자 설계 —** 아래 배선은 공식 권장 구조 위에 이 책이 `tracker`의 자원 배치를 정한 것이다. 여기서 만든 클라이언트를 9장이 그대로 재사용한다.

```python
# src/tracker/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = AsyncClient(timeout=5.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(title="tracker", lifespan=lifespan)
```

`yield` 앞뒤로 시작과 종료가 갈리는 이 모양은 방금 본 `yield` 의존성과 정확히 같은 문법이다. 다른 것은 수명뿐이다 — 저쪽은 요청 하나, 이쪽은 앱 하나.

`timeout=5.0`을 명시한 것은 의도다.[^4-3] **밖으로 나가는 호출에는 언제나 시한이 붙어 있어야 한다.**

클라이언트를 모듈 전역 변수가 아니라 `app.state`에 두는 것도 규칙으로 정해두자. 전역 변수는 테스트에서 갈아 끼우기 어렵고, 앱 인스턴스가 둘 이상 생기는 순간 누구의 것인지 모호해진다. 9장의 BFF는 여기 있는 클라이언트를 재사용한다. 요청마다 새로 만드는 코드를 인터넷에서 보게 되겠지만, 그건 커넥션 풀을 매번 버리는 짓이다.

미리 짚어둘 것이 있다. 워커를 여러 개 띄웠을 때 `lifespan`이 워커마다 도는지, 서버리스에서는 어떻게 되는지 — 이 책은 그 동작을 1차 소스로 확인하지 못했다. 프로세스가 어디서 갈라지는지는 5장이, 그것을 배포에서 어떻게 다룰지는 13장이 다룬다.

### 그런데 `on_event`는 어떻게 된 건가

인터넷 예제를 검색하면 `@app.on_event("startup")` 형태가 아직 잔뜩 나온다. 정확히 이해하려면 세 겹을 구분해야 한다.

첫째, FastAPI 0.140.0에는 `on_event`가 아직 있다. 소스에 `@deprecated` 데코레이터가 붙어 있고 메시지는 *"on_event is deprecated, use lifespan event handlers instead."*다. 생성자의 `on_startup`·`on_shutdown` 파라미터도 남아 있다.

둘째, 제거한 쪽은 Starlette이다. 1.0.0rc1 릴리스 노트의 축자는 *"Remove `on_event()` decorator from `Starlette` and `Router`"*이고, `on_startup`·`on_shutdown`·`add_event_handler()`도 함께 사라졌다.

셋째, FastAPI는 `starlette>=0.46.0`으로만 핀한다. 1.x를 강제하지 않는다.

그래서 **"FastAPI가 `on_event`를 제거했다"는 틀린 서술이다.** 그리고 이 구분은 말장난이 아니라 당신 프로젝트의 문제다. 세 겹을 합치면 이런 결론이 나온다 — `on_event`를 쓴 코드가 지금 도는지 안 도는지는 **당신의 `uv.lock`이 어떤 Starlette을 물어왔는지에 달려 있다.** 같은 코드가 어제 만든 환경에서는 멀쩡하고 오늘 새로 잠근 환경에서는 죽을 수 있다는 뜻이다. 이런 종류의 차이는 정말 아찔하다. 원인이 내 코드에 없기 때문이다.

`lifespan`으로 옮기는 편이 낫다. 두 겹 아래에서 이미 사라진 기능 위에 서 있을 이유가 없다.

### 컨테이너를 잃고 얻은 것 하나

씨앗 하나를 심어두고 닫자.

```python
# (개념 설명용 — 파일 아님)
app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides = {}
```

테스트에서 특정 의존성을 다른 함수로 갈아 끼우는 장치다. 모의 빈을 주입하거나 프로바이더를 덮어쓰던 자리에 해당한다. 눈여겨볼 것은 갈아 끼울 대상을 함수 객체 하나로 지목한다는 점이다. 타입도 아니고 이름 문자열도 아니다. 자동 와이어링을 포기한 대가로 배선의 각 지점이 파이썬 객체 하나로 정확히 특정되는 성질을 얻은 셈이다. 이 장치는 11장이 쓴다.

---

배선을 이름으로 만들고(`deps.py`), 라우팅 바깥에 층을 하나 세우고(`middleware.py`), 앱의 수명을 여닫는 곳을 열었다(`lifespan`). 컨테이너가 채워주던 자리를 세 갈래로 나눠 손으로 채운 셈이다. 자동으로 되지 않는다는 사실이 처음에는 손해처럼 보이지만, 대신 **배선이 전부 읽을 수 있는 코드로 남는다.** 어디서 무엇이 오는지 궁금할 때 뒤져야 할 설정이 없다.

여기까지 오면서 계속 당연하게 여긴 것이 하나 있다. 의존성도, 미들웨어의 `dispatch`도, `lifespan`도 전부 `async def`로 적혀 있다는 것. 그중 하나를 그냥 `def`로 적으면 무슨 일이 일어나는지가 다음 이야기다. 답은 문법이 아니라 숫자에 있다.

[^4-1]: import 경로 `starlette.middleware.base`의 `BaseHTTPMiddleware`, `dispatch(self, request, call_next)` 시그니처, `__init__` 오버라이드 시 `super().__init__(app)`, `response.headers[...]` 조작, 순수 ASGI 미들웨어의 `__init__`/`__call__` 형태와 `starlette.types`의 `ASGIApp`·`Scope`·`Receive`·`Send`, 미들웨어 스택 순서 — Starlette 공식 문서 Middleware, https://www.starlette.io/middleware/. `request.headers` 조회 — 같은 문서 Requests, https://www.starlette.io/requests/ (조회 2026-07-26)

[^4-2]: `app.add_middleware(MiddlewareClass, **options)` 형태와 인용한 축자 — FastAPI 공식 문서 Advanced Middleware, https://fastapi.tiangolo.com/advanced/middleware/ (조회 2026-07-26)

[^4-3]: `AsyncClient`의 생성자 인자 `timeout`(기본값 `Timeout(timeout=5.0)`)과 메서드 `aclose()` — httpx 공식 문서 Developer Interface, https://www.python-httpx.org/api/ · Timeouts, https://www.python-httpx.org/advanced/timeouts/ (조회 2026-07-26)

[^4-4]: `exception_handlers` 생성자 인자와 핸들러를 상태 코드·예외 클래스에 거는 방식 — Starlette 공식 문서 Exceptions, https://www.starlette.io/exceptions/. 인용한 축자와 *"FastAPI's `HTTPException` error class inherits from Starlette's `HTTPException` error class"* — FastAPI 공식 문서 Handling Errors, https://fastapi.tiangolo.com/tutorial/handling-errors/ (조회 2026-07-26)

[^4-5]: 예외 핸들러 조회가 `type(exc).__mro__`를 순회한다는 사실 — starlette 소스 `starlette/_exception_handler.py`의 `_lookup_exception_handler()`. **핀 하한 0.46.0과 현행 1.3.1 양쪽에서 동일함을 확인했다** (조회 2026-07-26)

[^4-6]: 인용한 `scope="function"`·`scope="request"` 축자 — FastAPI 공식 문서 Dependencies with yield, https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope (조회 2026-07-25)

[^4-7]: 인용한 dishka 축자 — dishka 공식 문서 Alternatives, https://dishka.readthedocs.io/en/stable/alternatives.html (조회 2026-07-26)


# 5장. 이벤트 루프 — `def`와 `async def` 사이의 40

한 프로세스 안에서 FastAPI 앱이 동시에 굴릴 수 있는 동기 작업은 **40개**다. anyio 4.14.2 / 2026-07 기준이고, 41번째는 앞의 누군가가 끝날 때까지 줄을 선다. 이상한 것은 이 숫자가 FastAPI 문서 어디에도 없다는 점이다. 설정에도 없고 기동 로그도 알려주지 않는다. 그런데 부하가 걸리면 앱은 정확히 이 숫자에서 막힌다.

1장에서 층 그림을 그리며 한 줄을 미뤄뒀다. 동시성이 왜 그 숫자에서 막히는지는 anyio 소스에 있다고 썼다. 이제 그 소스까지 내려가 보자. 내려가는 길에 이 장의 진짜 질문에도 답이 나온다 — 함수 앞에 `async` 네 글자를 붙이느냐 마느냐가 왜 여기서는 성능의 문제가 아니라 **장애**의 문제가 되는가.

먼저 밝혀둘 것이 있다. `async`/`await` 문법도, 코루틴이 무엇인지도 설명하지 않는다. 다룰 것은 문법이 아니라 **FastAPI가 그 문법을 어떻게 처리하는가**다. 그 처리 방식이 40이라는 숫자를 만든다.

## 네 층을 타고 내려가면 나오는 숫자

시작은 FastAPI다. 경로 함수를 부르기 직전, 프레임워크는 갈림길을 하나 지난다.

```python
if is_coroutine:
    return await dependant.call(**values)
else:
    return await run_in_threadpool(dependant.call, **values)
```

> 출처: fastapi 0.140.0 태그 `fastapi/routing.py` (조회 2026-07-25)

네 줄이 전부다. 당신이 함수를 `async def`로 선언했으면 이벤트 루프에서 그대로 `await`하고, `def`로 선언했으면 `run_in_threadpool`에 넘긴다. **선언 키워드 하나가 실행 장소를 정한다.** 실행 위치를 옮기는 장치를 애너테이션으로 명시하던 세계에서 오면 이 대목이 낯설다. 여기서는 표시가 따로 없다. 함수 선언 자체가 스위치여서, 잊기가 훨씬 쉽다.

한 층 아래는 Starlette이다.

```python
async def run_in_threadpool(func, *args, **kwargs):
    func = functools.partial(func, *args, **kwargs)
    return await anyio.to_thread.run_sync(func)
```

> 출처: starlette 1.3.1 태그 `starlette/concurrency.py` (조회 2026-07-25)

여기서 눈여겨볼 것은 **넘기지 않은 인자**다. `to_thread.run_sync`는 `limiter` 인자를 받는데 Starlette은 그걸 주지 않는다. 주지 않으면 기본값이 쓰인다.

그 기본값이 마지막 층에 있다. anyio의 asyncio 백엔드가 기본 스레드 리미터로 `CapacityLimiter(40)`을 들고 있고, 공식 문서가 그 뜻을 적어뒀다.

> "The default AnyIO worker thread limiter has a value of 40, meaning that any calls to `to_thread.run_sync()` without an explicit `limiter` argument will cause a maximum of 40 threads to be spawned."

네 층을 내려온 끝에 숫자 하나가 나왔다. FastAPI가 정한 값이 아니라, FastAPI가 Starlette에게 맡기고 Starlette이 anyio에게 맡긴 결과로 남은 값이다. 1장에서 "층을 타고 내려가는 일이 일상"이라고 했던 그 일상이 이런 모양이다.

바꿀 수는 있다. 토큰 수를 직접 올리면 된다.[^5-1]

```python
# (개념 설명용 — 파일 아님)
from anyio import to_thread

to_thread.current_default_thread_limiter().total_tokens = 60
```

숫자를 올리는 것은 한 줄이다. 다만 올리기 전에 이 장의 나머지를 읽는 편이 낫다. 40이 어디서 소진되는지 모르는 채 숫자만 키우면 병목이 데이터베이스로 옮겨갈 뿐이다.

## 그 40을 의존성이 함께 쓴다

여기까지는 경로 함수 이야기다. 실무에서 사람을 무는 것은 그 다음이다.

`Depends`로 물린 의존성 함수도 `def`로 선언돼 있으면 똑같이 스레드로 밀린다. 그리고 그 스레드는 **경로 함수가 쓰는 것과 같은 40개짜리 풀**에서 나온다. 세션을 열고, 현재 사용자를 꺼내고, 서비스 인스턴스를 만들고 — 하나의 요청이 경로 함수에 닿기까지 함수 여럿을 지나가는데, 그중 `def`로 선언된 것마다 40개짜리 줄에 한 번씩 선다.

한 요청이 토큰 세 개를 동시에 쥐는 것은 아니다. 순서대로 잡았다 놓는다. 하지만 총량은 하나다. 그래서 계산이 어긋난다. "동시 요청 40개까지는 버티겠지"라고 어림했는데 요청 하나가 줄을 세 번 서고 있다면, 실제로 버티는 수는 그보다 한참 적다. 코드 어디에도 40이 적혀 있지 않으니 계산의 출발점부터 안 보인다.

프레임워크가 이 풀을 얼마나 조심스럽게 다루는지 보여주는 대목이 하나 더 있다. `yield`를 쓰는 동기 의존성의 **정리 코드**는 일부러 공용 풀 밖에서 돈다.

```python
exit_limiter = CapacityLimiter(1)
```

> 출처: fastapi 0.140.0 태그 `fastapi/concurrency.py` (조회 2026-07-25)

같은 파일의 주석이 이유를 밝혀뒀다. 정리 코드가 빈 스레드를 기다리게 두면 *"can create race conditions/deadlocks if the context manager itself has its own internal pool (e.g. a database connection pool)"*이라는 것이다. 자기 풀을 가진 컨텍스트 매니저 — 데이터베이스 커넥션 풀이 정확히 그것이다. 정리하려면 스레드가 필요한데 스레드가 없어 못 정리하고, 못 정리해서 자원이 안 돌아오는 교착. 그 고리를 끊으려고 정리 경로는 **공용 40개 리미터를 쓰지 않고 자기 몫의 별도 리미터로 돈다.** 위 코드가 그 별도 리미터다.

프레임워크가 이런 예외를 소스에 박아둘 때는 대개 누군가 물린 뒤다. 그리고 이 예외가 겨눈 자리 — 자기 풀을 가진 자원을 의존성으로 열고 닫는 일 — 가 정확히 6장의 소재다. 다만 `tracker`의 세션 의존성은 `async def`로 쓰므로 이 스레드 문제 자체는 비껴간다. 6장에서 우리가 손으로 그어야 하는 것은 스레드 경계가 아니라 **세션의 생명주기와 트랜잭션 경계**다.

## 한 프로세스 안에 두 세계가 있다

이제 구조를 놓고 보자. 아는 두 모델과 나란히 세우면 생김새가 선명해진다.

서블릿 컨테이너에서는 요청이 스레드를 하나씩 물고 간다. 그 안에서 무엇을 하든 — 데이터베이스를 기다리든 외부 API를 부르든 — 막히는 것은 그 스레드 하나이고, 나머지 스레드는 계속 요청을 받는다. 반대편에 Node가 있다. 스레드는 하나이고 이벤트 루프가 돌며, 그래서 어딘가에서 진짜로 블로킹하면 그 프로세스 전체가 멈춘다.

FastAPI는 **이 두 모델을 한 프로세스 안에 동시에 갖고 있다.** `async def`로 선언한 경로 함수는 Node 쪽 세계에 산다. `def`로 선언한 경로 함수는 서블릿 쪽 세계에 산다 — 다만 스레드가 40개뿐이다. 같은 앱, 같은 파일 안에서 두 세계가 함수 선언 하나로 갈린다.

이 구도에 이름을 붙인 사람들이 있다. Adya와 동료들이 2002년 USENIX ATC에 낸 논문의 부제가 *"Event-driven Programming is Not the Opposite of Threaded Programming"*이다. 이들은 뭉뚱그려지던 것을 두 축으로 갈랐다 — 작업 관리(serial / cooperative / preemptive)와 스택 관리(manual / automatic). 그 2축 공간에서 "멀티스레드"와 "이벤트 기반"은 대각선으로 마주 보고, 논문은 제3의 자리를 지목한다.[^5-2]

> "The key concept is that one can choose the reasoning benefits of cooperative task management without sacrificing the readability and maintainability of automatic stack management."

협력적 스케줄링의 추론 용이함을 가지면서 자동 스택 관리의 가독성을 포기하지 않는 자리. 20년 뒤 `async`/`await` 문법이 바로 그 자리를 채웠다. 콜백 지옥이 "수동 스택 관리"의 다른 이름이었다는 것을 알고 나면, `await` 한 글자가 문법 설탕이 아니라 오래된 설계 문제의 답이라는 게 보인다. 이 논문이 2002년 하드웨어를 전제한다는 점은 감안하되, 이 2축 구분 자체는 지금도 그대로 쓸모가 있다.

여기서 가장 흔한 사고가 난다. **`async def` 안에서 동기 호출을 하는 것.** 동기 드라이버로 쿼리를 날리거나, 동기 HTTP 클라이언트로 외부 API를 부른다. 이 실수 패턴 자체는 커뮤니티가 오랫동안 반복해서 보고해 온 사실이다.

— 여기서부터는 **저자 가설**이다. 나는 이 실수의 뿌리가 스레드-퍼-리퀘스트 모델의 직관에 있다고 본다. 그 세계에서 블로킹은 국소적 사건이다. 내 스레드가 멈출 뿐 옆 요청은 계속 처리된다. 그 감각을 그대로 들고 오면 `async def` 안의 동기 호출이 위험해 보이지 않는다. 하지만 리서치에서 "나는 서블릿 세계에서 왔고 그래서 이렇게 했다"고 밝힌 증언은 한 건도 찾지 못했다. 그러니 이건 관찰된 사실이 아니라 내 설명이다.

이 사고가 고약한 진짜 이유는 따로 있다. **터져도 엉뚱한 데서 터진다.** HN에서 acdha가 2026-04-26에 정리한 4단계 시나리오가 그 성질을 짚는다. 요청 1이 `await`에 걸려 양보하고, 요청 2로 넘어갔다가, 요청 3이 루프를 한동안 막고, 그 사이 요청 1이 소켓 타임아웃을 맞는다. 그의 결론은 이렇다.[^5-3]

> "That error in #4 does not tell you anything about #2 or #3"

로그에 남는 것은 요청 1의 타임아웃이고, 범인은 요청 3이다. 스레드 모델이었다면 같은 스레드 안에서 드러났을 문제다. 부하가 걸려야 나타나고, 나타나도 다른 이름으로 나타난다. 아찔한 조합이다.

균형도 맞추자. 같은 논쟁에서 layer8은 2026-04-25에 반대편을 이렇게 요약했다 — 서버는 요청마다 스레드를 만들지 않고 풀을 쓰며, I/O 대기로 인한 컨텍스트 스위치 비용은 *"negligible in practice for most applications"*이고, 비동기가 중요해지는 것은 동시 요청 수가 가질 수 있는 스레드 수에 근접할 때인데 *"Many applications don't come close to that in practice"*라는 것이다.[^5-4] 새겨들을 만하다. 이 장은 `async def`가 언제나 옳다고 말하려는 게 아니다.

Node를 지나온 독자에게는 다른 말이 필요하다. 이벤트 루프를 이미 안다는 점은 유리한데, 유리한 것은 개념이지 생태계가 아니다. JavaScript에서는 동기 I/O 라이브러리를 만날 일이 거의 없어 "이게 논블로킹인가"를 물을 필요가 없었다. 파이썬은 동기 라이브러리가 다수여서 그 질문을 매번 해야 한다. HN의 leonidasv가 2026-05-27에 쓴 대로, 같은 API가 이름이나 패키지로 갈려 *"`foo` and `afoo`"* 두 벌로 존재하기 때문이다.[^5-5] **Node 독자에게 줄 경고는 "이벤트 루프를 다시 배워라"가 아니라 "확인하는 습관을 새로 들여라"다.**

## 썸네일 하나가 루프를 세운다

`tracker`로 내려오자. 이슈에 첨부된 이미지의 썸네일을 만드는 함수가 필요하다. 업로드 경로와 `Attachment` 모델은 아직 없다 — 각각 8장과 6장의 몫이다. 지금은 바이트를 받아 바이트를 돌려주는 순수 함수 하나면 된다.

> **📐 저자 설계 —** 아래 함수 이름과 배치는 FastAPI 공식 권장이 아니라, 이 책이 CPU 바운드 작업의 자리를 보여주려고 정한 것이다. 내부 구현은 이 논의와 무관하므로 비워둔다.

```python
# src/tracker/services/attachment.py
def generate_thumbnail(data: bytes) -> bytes:
    ...
```

이 함수는 이미지를 디코딩하고 축소해 다시 인코딩한다. 네트워크를 기다리지 않고 **CPU를 쓴다.** 그게 이 절의 전부다.

어디서 부르느냐에 따라 세 가지 결과가 나온다. 첫 번째.

```python
# (개념 설명용 — 파일 아님)
async def make_thumbnail(data: bytes) -> bytes:
    return generate_thumbnail(data)
```

가장 나쁘다. `async def` 안에서 CPU 작업을 직접 돌리면 그 시간 동안 이벤트 루프가 아무것도 못 한다. 이 워커 프로세스가 붙들고 있던 **모든** 요청이 함께 멈춘다. 썸네일 하나에 300밀리초가 걸린다면, 그동안 이 프로세스는 세상에 없는 것이나 마찬가지다.

두 번째.

```python
# (개념 설명용 — 파일 아님)
def make_thumbnail(data: bytes) -> bytes:
    return generate_thumbnail(data)
```

`async`를 뗐다. 이제 FastAPI가 이 함수를 스레드풀로 밀어주므로 이벤트 루프는 살아 있다. 앞 절의 갈림길이 우리 편에서 작동한 것이다. 다만 여기서 쓰는 스레드는 40개짜리 공용 풀에서 나온다.

세 번째는 결과가 같지만 의도가 드러난다.

```python
# (개념 설명용 — 파일 아님)
from anyio import to_thread


async def make_thumbnail(data: bytes) -> bytes:
    return await to_thread.run_sync(generate_thumbnail, data)
```

경로 함수는 `async def`로 두고 무거운 한 호출만 스레드로 넘긴다. 읽는 사람에게 "여기가 블로킹 구간이다"라고 말해주기까지 한다. 비동기 코드에 동기 라이브러리를 끼워 넣어야 할 때의 기본형이다.

그런데 여기서 반올림하지 말자. **오프로드는 이벤트 루프를 살릴 뿐, 용량을 늘려주지 않는다.** 두 번째와 세 번째는 같은 40개짜리 리미터를 쓴다. 그리고 CPU 바운드 작업은 스레드로 옮긴다고 병렬로 돌지도 않는다. shipfriend.dev에 서정우가 2026-03-28에 정리한 FastAPI의 약점 목록에 이 사정이 그대로 들어 있다 — *"CPU 집약적인 작업(이미지 처리, 대용량 연산 등)에서는 멀티스레드를 써도 병렬화가 되지 않"*는다는 것이다.[^5-6] 하필 예시가 이미지 처리다.

정리하면 이렇다. 썸네일을 `async def` 안에서 직접 돌리는 것은 **틀렸고**, 스레드로 미는 것은 **덜 틀렸다.** 진짜 답은 이 작업을 프로세스 밖으로 내보내는 것이고, 그 이야기는 8장에서 한다. 지금 챙길 것은 판단 기준 하나다. 이 호출은 기다리는 일인가, 계산하는 일인가. 기다리는 일이면 비동기 라이브러리를 찾고 없으면 스레드로 민다. 계산하는 일이면 스레드는 응급 처치이고, 언젠가 밖으로 내보내야 한다.

## 프로세스라는 더 큰 경계

이 모든 것이 **한 프로세스 안**의 일이었다. 그런데 실제로 앱을 띄울 때 우리는 프로세스 수를 정한다.

| 플래그 | 기본값 | 하는 일 |
|---|---|---|
| `--workers` | `None` (`$WEB_CONCURRENCY` 환경 변수를 따른다) | 워커 프로세스 수 |
| `--limit-concurrency` | `None` | 동시 연결·태스크 상한. 초과분에 503을 돌려준다 |
| `--backlog` | `2048` | 수락 대기 큐에 붙들어 둘 연결 수 |

uvicorn 0.51.0 / 2026-07 기준이다. 이 중 `--workers`가 만드는 것은 스레드가 아니라 **독립된 프로세스**다. PM2로 Node 앱을 클러스터 모드로 띄워봤다면 그림이 같다.

그리고 여기서 한 문장이 나온다. **워커는 메모리를 공유하지 않는다.**

그러니까 40개짜리 스레드풀은 워커마다 따로 있다. 가령 워커를 4개 띄웠다면 스레드는 프로세스당 40개씩 합쳐서 160개다 — 4라는 숫자에 아직 아무 근거가 없다는 점만 기억해두자. 같은 논리로 프로세스 안에 담아둔 것은 전부 워커마다 따로다. 딕셔너리에 넣어둔 캐시도, 열려 있는 WebSocket 연결 목록도, 앱이 켜질 때 한 번만 돌리려던 스케줄러도 그렇다.

이 사실 하나가 나중에 두 번 돌아온다. 7장에서는 알림이 절반만 도착하는 현상으로, 8장에서는 주간 리포트가 네 번 생성되는 현상으로. 원인은 같다. 프로세스 경계는 프레임워크가 지워주지 않는다.

워커를 몇 개 띄울 것인가는 여기서 답하지 않는다. 그 숫자는 13장의 소재다. 지금 챙길 것은 경계의 존재다.

## 40, 그리고 넘치기 전에 막는 법

층이 세 개 나왔으니 정리하고 가자. 셋은 서로 다른 곳에 있다.

- **40**은 앱 안에 있다. 동기 함수가 쓰는 스레드 토큰의 수다.
- **`--limit-concurrency`**는 서버에 있다. 동시에 처리할 연결·태스크의 상한이고, 넘치면 503을 돌려준다.
- **`--backlog`**는 그보다 앞에 있다. 아직 수락하지 않은 연결을 붙들어 두는 큐다.

이름이 비슷해서 섞이기 쉬운데 하는 일이 다르다. 문 앞에서 손님을 돌려보내는 손잡이는 `--limit-concurrency` 하나다. 큐를 키우는 것은 손잡이가 아니다 — 대기 줄을 늘리면 응답이 늦게 오는 요청이 늘어날 뿐이다. 그리고 **서버 상한을 걸었다고 40이 해결되는 것도 아니다.** `--limit-concurrency`를 500으로 잡아둔 동기 위주의 앱은 여전히 40에서 말라붙고, 초과분은 503을 받는 대신 리미터 앞에 줄을 서게 된다 — 이건 두 층의 동작에서 따라 나오는 추론이지 문서에 적힌 문장이 아니다. 동기 경로의 진짜 천장은 40이고, 그 숫자를 옮기는 uvicorn 플래그는 없다 — 앞 절에서 본 `total_tokens`만이 그 값을 바꾼다. 서블릿 컨테이너에서 스레드 상한과 수락 큐를 따로 설정하던 감각이 그대로 옮겨온다. 단계마다 큐를 두고 들어오는 양을 조절한다는 이 발상은 2001년 SOSP의 SEDA 논문이 아키텍처로 정식화한 것이기도 하다.

그렇다면 상한을 얼마로 잡아야 할까? 여기서 Little's Law가 쓸모 있다. 1961년 *Operations Research*에 증명이 실린 정리이고, 웹 서버 언어로 옮기면 이렇다.

**평균 동시 요청 수 = 처리량(초당 요청 수) × 평균 응답 시간**

이 식을 40에 대고 거꾸로 읽어보자. 어떤 엔드포인트가 전부 동기로 짜여 있고 한 번 처리에 200밀리초가 걸린다면, 40개의 슬롯으로 감당 가능한 처리량은 40 ÷ 0.2 = **초당 200요청**이다. 같은 엔드포인트가 1초씩 걸린다면 초당 40요청으로 떨어진다. 응답 시간이 다섯 배가 되면 처리량은 5분의 1이 된다. 계산이 이렇게 단순하다.

물론 이건 예측이지 측정이 아니다. 실제 앱에는 비동기 경로와 동기 경로가 섞여 있고 데이터베이스라는 또 다른 상한도 있다. 그래도 이 산술은 목표 처리량과 응답 시간에서 필요한 동시성을 계산해주고, 측정 결과가 이 식과 크게 어긋나면 측정을 의심할 근거를 준다.

## 파이썬이 아직 못 얻은 것

여기까지 오면 마음 한구석이 찜찜할 것이다. 함수마다 색깔이 있고, 그 색깔을 잘못 칠하면 장애가 나고, 어느 라이브러리가 논블로킹인지 매번 확인해야 한다. 이게 정말 2026년의 최선인가?

이 질문을 밖에서 던지는 사람만 있는 게 아니다. **파이썬 안에서도 같은 말이 나온다.**

2025-05-09, CPython 코어 개발자 Mark Shannon이 discuss.python.org에 "Add Virtual Threads to Python"이라는 제안을 올렸다.[^5-7] 요약 문단이 이렇게 시작한다.

> "Java has virtual threads. Virtual threads are a better way of doing concurrency than Python's async and await. We should add virtual threads to Python… Unlike Python's coroutines, virtual threads: do not divide the language in two 'colors'."

이 스레드에는 274개의 글과 565개의 좋아요가 달렸고 조회수는 22,050이며, 확인 시점 마지막 글은 2026-02-14다. 한 사람의 투정이 아니라는 뜻이다. `aiofiles`와 `pytest-asyncio`를 만든 Tin Tvrtković이 2025-05-10에 지지를 보탰고, 2026-02-14에는 Java를 써본 참여자가 요구 조건을 이렇게 적었다.

> "Ability to use existing 'blocking' code AS IS, including 3rd-party packages… Java's Virtual Threads support has already proven that it's both possible and practical to abstract all that inside the runtime layer."

기존 블로킹 코드를 **그대로** 쓸 수 있어야 한다는 것. 앞에서 우리가 `to_thread.run_sync`로 감쌌던 그 일을 런타임이 알아서 해달라는 요구다.

한쪽으로만 읽지는 말자. 반대 의견도 그 안에 있다. Liz는 2025-05-10에 새 언어라면 몰라도 함수 색칠을 피하는 것이 유일한 이득이라면 `async`/`await`가 있는 이상 색칠은 남는다고 지적했고, Rosuav는 2025-08-02에 가상 스레드가 결국 스레드와 무엇이 다른지 모르겠다고 썼다. 이건 결론이 난 논의가 아니라 **진행 중인 제안**이다. 파이썬의 로드맵이 아니다.

Adya의 2축 공간으로 돌아가면 그림이 깔끔해진다. `async`/`await`는 협력적 작업 관리 쪽에서 자동 스택 관리에 도달했고, 가상 스레드는 선점적 작업 관리 쪽에서 같은 목적지에 도달한다. 방향이 반대일 뿐이다. 그리고 후자는 함수에 색을 칠하지 않으므로 기존 라이브러리를 그대로 쓸 수 있다. 당신이 Loom으로 얻은 것을 파이썬은 아직 얻지 못했고, 파이썬을 만드는 사람들도 그걸 안다.

그러면 이 부담은 얼마나 오래갈까. 학술 쪽에서 실마리를 찾고 싶었는데, **파이썬 asyncio의 버그 패턴을 다룬 실증 연구는 찾지 못했다.** 대신 가장 가까운 것으로 Kotlin 코루틴 연구가 있다 — Brockbernd 등이 ECOOP 2024에 발표한 조사로, 오픈소스 커밋 1,353건을 손으로 검토해 코루틴 고유의 동시성 버그 55건을 분류했다. 데이터 레이스·데드락 같은 전통적 패턴은 일부러 뺐다. 최다 범주는 취소 예외 처리로 14건, 그다음이 중첩된 `runBlocking` 11건이다.[^5-8]

**이건 Kotlin 연구이고 파이썬 연구가 아니다.** 언어도 런타임도 다르니 수치를 옮겨 쓸 수 없다. 짚어둘 만한 것은 목록의 성격이다. 1위가 취소 처리이고 2위가 동기 세계와 비동기 세계를 잇는 지점이다. 언어를 건너 반복되는 것은 문법 실수가 아니라 **두 세계의 경계에서 나는 사고**라는 신호로 읽을 수 있다. 이 장이 처음부터 그 경계 이야기를 한 이유다.

마지막으로 free-threading이 남는다. 2026-07 / Python 3.14 기준으로 확정된 것부터 보자. GIL을 선택적으로 만드는 PEP 703은 Final 상태로 3.13에, 지원 상태의 기준을 정한 PEP 779는 Final 상태로 3.14에 걸려 있고, FastAPI는 0.136.0(2026-04-16)에서 free-threaded 빌드인 3.14t 지원을 표방했다. 다만 그것이 언제 기본 빌드가 되는지, 그리고 40개짜리 스레드 모델을 실제로 얼마나 바꾸는지는 이 책을 쓰는 시점에 확인하지 못했다. 단정할 자리가 아니다. 빠르게 바뀔 영역이니 공식 문서를 함께 확인하자.

---

이제 `def`와 `async def` 사이에서 무슨 일이 벌어지는지 안다. 선언 키워드가 실행 장소를 정하고, 동기 쪽에는 프로세스당 40개의 자리가 있고, 그 자리를 경로 함수와 의존성이 나눠 쓴다. 다음에 누군가 "요청이 몰리면 느려진다"고 신고하면 물어볼 것이 생겼다. 그 경로에 동기 호출이 있는가, 그것은 기다리는 일인가 계산하는 일인가, 지금 워커는 몇 개인가.

한 가지만 예고해두자. 이 장에서 내린 `def`/`async def` 판단은 **13장에서 한 번 뒤집힌다.** 앱을 어디에 올리느냐에 따라 동시성의 전제 자체가 달라지기 때문이다.

그 전에 먼저 치를 일이 있다. 우리가 이벤트 루프를 막지 않으려고 이렇게 애쓴 이유는 결국 데이터베이스 때문이다. 그리고 비동기 세계의 데이터베이스 세션은, 익숙한 그 어떤 것과도 닮지 않았다.

[^5-1]: 기본 리미터 40의 축자와 `from anyio import to_thread`·`to_thread.run_sync()`·`to_thread.current_default_thread_limiter().total_tokens` 호출 형태 — AnyIO 공식 문서 *Working with threads*, https://anyio.readthedocs.io/en/stable/threads.html (조회 2026-07-26)

[^5-2]: Adya 외, *"Cooperative Task Management Without Manual Stack Management"* — USENIX ATC 2002, https://www.usenix.org/legacy/events/usenix02/full_papers/adyahowell/adyahowell.pdf (조회 2026-07-25)

[^5-3]: acdha, Hacker News, 2026-04-26, https://news.ycombinator.com/item?id=47912719 (조회 2026-07-25)

[^5-4]: layer8, Hacker News, 2026-04-25, https://news.ycombinator.com/item?id=47905032 (조회 2026-07-25)

[^5-5]: leonidasv, Hacker News, 2026-05-27, https://news.ycombinator.com/item?id=48289232 (조회 2026-07-25)

[^5-6]: 서정우, *"FastAPI는 왜 사용하는 걸까? 강점과 약점"*, shipfriend.dev, 2026-03-28, https://shipfriend.dev/posts/why-use-fastapi-strengths-and-weaknesses (조회 2026-07-25)

[^5-7]: Mark Shannon, *"Add Virtual Threads to Python"*, discuss.python.org, 2025-05-09, https://discuss.python.org/t/add-virtual-threads-to-python/91403 (조회 2026-07-25)

[^5-8]: Brockbernd 외, *"Understanding Concurrency Bugs in Real-World Programs with Kotlin Coroutines"* — ECOOP 2024, DOI 10.4230/LIPIcs.ECOOP.2024.8 (조회 2026-07-25)


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


# 7장. 실시간 — WebSocket, SSE, 그리고 스트리밍

알림 기능을 붙였다. 스테이징에서 워커를 2개로 늘리자 알림이 절반만 도착한다. 무엇이 잘못됐을까?

코드는 그대로다. 브라우저 콘솔에도 서버 로그에도 오류가 없다. 도착하지 않은 절반은 흔적조차 남기지 않는다. 이런 종류의 버그가 제일 난감하다.

방향만 미리 말해두자. 잘못된 것은 알림 코드가 아니라 **연결이 어디에 사는가**에 대한 가정이다. 요청-응답 앱에서는 요청이 어느 프로세스에 떨어지든 상관없었다. 연결이 오래 살아 있는 앱에서는 그 편의가 사라진다.

## 끝나지 않는 함수

WebSocket 엔드포인트는 이렇게 생겼다.

```python
# (개념 설명용 — 파일 아님)
from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

> 출처: FastAPI 공식 문서 *APIRouter* (`APIRouter.websocket` 예제), https://fastapi.tiangolo.com/reference/apirouter/ (조회 2026-07-26)

지금까지 본 경로 함수와 결정적으로 다른 점이 있다. **이 함수는 끝나지 않는다.** 앞선 경로 함수들은 값을 돌려주고 죽었고 그 값이 응답 본문이 됐다. 여기서는 반환값 대신 `while True`가 있다. 함수가 사는 동안이 곧 연결이 사는 동안이다.

5장에서 우리는 함수가 이벤트 루프를 얼마나 오래 붙잡느냐를 걱정했는데, WebSocket 엔드포인트는 설계상 오래 붙잡는다. 대부분이 `await`에서 기다리는 시간이라 문제가 안 될 뿐이다.

**기본 설치만으로는 WebSocket이 동작하지 않는다.** uvicorn 기본 설치에는 구현체가 없고 `uvicorn[standard]`가 `websockets`를 설치한다. 공식 문서는 `uv add websockets`를 안내한다. 빠뜨리면 앱은 뜨는데 연결만 안 된다.

구현체도 하나가 아니다. uvicorn 0.51.0 / 2026-07 기준 `--ws` 선택지는 다섯이다 — `auto`·`none`·`websockets`·`websockets-sansio`·`wsproto`. 왜 비슷한 이름이 둘일까? 문서가 밝힌다.

> "Since `websockets` deprecated the API Uvicorn uses to run the previous protocol, we had to create this new protocol that uses the `websockets` SansIO API."

아래 라이브러리가 API를 정리하자 서버가 구현을 더 만든 것이다. 버전에 민감하니 배포할 uvicorn 문서를 확인하자.

한 층 아래로 내려가면 그림은 단순하다. `Upgrade` 헤더를 실은 GET에 서버가 101로 답한 뒤부터, ASGI 층에서는 `websocket.connect`·`receive`·`disconnect`가 올라오고 앱은 `websocket.accept`·`send`·`close`를 내려보낸다.

예외 처리도 HTTP와 다르다. 연결이 끊기면 수신 메서드가 `WebSocketDisconnect`를 던진다. 여기서 `HTTPException`은 의미가 없다 — 이미 HTTP 응답을 돌려줄 국면이 아니다. 대신 `WebSocketException`에 닫기 코드를 실어 던진다.[^7-1]

## 상위 프로토콜은 딸려 오지 않는다

Spring에서 WebSocket을 다뤄봤다면 당신은 이쯤에서 위화감을 느낀다. 거기서는 프레임을 직접 만지는 일이 드물었다 — 그 위에 STOMP라는 층이 있었기 때문이다. Spring 문서는 그 층이 왜 필요한지를 이렇게 설명한다.

> "The WebSocket protocol defines two types of messages (text and binary), but their content is undefined. The protocol defines a mechanism for client and server to negotiate a sub-protocol (that is, a higher-level messaging protocol)…"[^7-5]

프로토콜이 메시지의 **내용을 정의하지 않는다**는 것 — 이게 핵심이다. WebSocket이 주는 것은 양방향으로 흐르는 텍스트와 바이너리 프레임뿐이고, 목적지 주소도 구독이라는 개념도 브로커도 규격 안에 없다. STOMP는 그 빈 곳을 메우려고 얹은 층이고, SockJS는 WebSocket을 못 쓰는 환경을 위한 폴백이다.

FastAPI에는 그 층이 없다. 그러니 이렇게 읽어야 정확하다 — 무언가를 빼먹은 것이 아니라, 표준이 애초에 정해주지 않는 것을 프레임워크가 대신 정해주느냐 마느냐의 차이다. 정해주지 않으면 **당신이 정하게 된다.** 메시지에 종류를 실을지, 필드 이름은 무엇으로 할지, 무엇을 구독한다고 알릴지. 부채처럼 느껴진다면 절반은 맞다. 이득도 같은 곳에서 나온다 — 규약이 열 줄이면 되는 앱에 브로커를 배울 필요가 없다.

`tracker`는 규약을 작게 잡는다. 채널 하나가 이슈 하나에 대응하고, 그 위로는 한 가지 모양의 메시지만 흐른다.

> **📐 저자 설계 —** 아래 이벤트 스키마와 채널 규약은 FastAPI 공식 권장이 아니라, 상위 프로토콜이 없는 자리를 이 책이 메우기로 정한 한 가지 안이다.

```python
# src/tracker/schemas/common.py
from datetime import datetime

from pydantic import BaseModel

# ...(3장, 생략)


class IssueEvent(BaseModel):
    issue_id: int
    event_type: str
    payload: dict[str, str]
    occurred_at: datetime
```

3장의 요청·응답 스키마와 같은 도구로 메시지 규약을 적었다. 상위 프로토콜을 못 받은 대신, 경계에서 타입을 만드는 장치는 이미 있었다.

## 워커가 둘이면 알림은 절반만 간다

오프닝의 질문으로 돌아가자. 여러 연결에 한꺼번에 밀어주는 코드는 대개 이렇게 시작한다. 연결을 리스트에 담아두고, 이벤트가 생기면 돌면서 보낸다. FastAPI 공식 문서의 `ConnectionManager` 예제가 그 모양이고, 문서는 바로 아래에서 한계를 스스로 경고한다.

> "as everything is handled in memory, in a single list, **it will only work while the process is running, and will only work with a single process.**"

5장의 그 문장이 청구서로 돌아온다. **워커는 메모리를 공유하지 않는다.** 워커가 2개면 리스트도 2개다. A의 연결은 1번 워커에, B는 2번에 있다. 상태 변경 요청이 1번에 떨어지면 1번의 리스트만 순회하고 B는 아무것도 못 받는다. 알림이 절반만 도착하는 정체가 이것이고, 아무 예외도 안 나는 이유도 같다 — **코드는 자기가 아는 연결 전부에게 성공적으로 보냈다.**

필요한 것은 프로세스 경계를 건너는 배선이다. Socket.IO를 여러 인스턴스로 굴려봤다면 Redis 어댑터로 메시지를 퍼뜨렸을 텐데, 정확히 그 물건이 여기에는 없다.

FastAPI 공식 문서는 이 지점에서 `encode/broadcaster`를 권한다. 그런데 그 저장소는 2025-08-19에 아카이브됐다. PyPI 최신 릴리스는 0.3.1 / 2024-08-01이고, README 자신도 진작에 이렇게 적어두고 있었다.

> "At the moment broadcaster is in Alpha, and should be considered a working design document."

공식 문서가 아카이브된 라이브러리를 아직 링크하고 있다. 공식 대체재 안내도 없다. 인터넷 예제만 낡는 게 아니라 **공식 문서도 낡는다.**

직접 짜는 수밖에 없다. 발행과 구독 두 동작이면 된다.

> **📐 저자 설계 —** 아래 팬아웃 배선은 FastAPI 공식 권장이 아니라, 5장의 프로세스 경계로부터 이 책이 도출한 한 가지 안이다.

```python
# src/tracker/events.py
import asyncio
import json
from typing import AsyncIterator, Protocol

import redis.asyncio as redis

from tracker.schemas.common import IssueEvent


class EventBus(Protocol):
    async def publish(self, event: IssueEvent) -> None: ...

    def subscribe(self, issue_id: int) -> AsyncIterator[IssueEvent]: ...


class RedisEventBus:
    def __init__(self, client: redis.Redis) -> None:
        self.client = client

    def channel(self, issue_id: int) -> str:
        return f"tracker.issue.{issue_id}"

    async def publish(self, event: IssueEvent) -> None:
        await self.client.publish(
            self.channel(event.issue_id), event.model_dump_json()
        )

    async def subscribe(self, issue_id: int) -> AsyncIterator[IssueEvent]:
        async with self.client.pubsub() as pubsub:
            await pubsub.subscribe(self.channel(issue_id))
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=None
                )
                if message is not None:
                    yield IssueEvent.model_validate(json.loads(message["data"]))
```

`redis.asyncio`는 별도 패키지가 아니다. `aioredis`는 redis-py에 흡수됐으니 `uv add redis` 하나면 되고, `aioredis`를 설치하라는 글을 만나면 그건 낡은 자료다.[^7-3] 클라이언트를 만들면 커넥션 풀이 함께 생기는데, 그 기본 크기는 1차 소스로 확인하지 못했다. 구독자가 연결을 오래 붙드는 구조이니 확인해 잡아두는 편이 낫다.

공식 예제의 `ConnectionManager`가 하던 일은 구독이 대신한다. 연결마다 자기 구독을 가지니 목록을 들고 있을 필요가 없다. `EventBus`를 프로토콜로 선언한 이유는 구현이 하나가 아니어서다.

```python
# src/tracker/events.py
class InMemoryEventBus:
    def __init__(self) -> None:
        self.queues: dict[int, list[asyncio.Queue[IssueEvent]]] = {}

    async def publish(self, event: IssueEvent) -> None:
        for queue in self.queues.get(event.issue_id, []):
            queue.put_nowait(event)

    async def subscribe(self, issue_id: int) -> AsyncIterator[IssueEvent]:
        queue: asyncio.Queue[IssueEvent] = asyncio.Queue()
        self.queues.setdefault(issue_id, []).append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            self.queues[issue_id].remove(queue)
```

같은 두 메서드를 메모리 위에 구현한 것이 전부이고, 11장에서 이 구현을 끼워 넣는다.

## SSE는 이제 설치할 것이 없다

알림이 서버에서 클라이언트로만 흐른다면 WebSocket은 과하다. 이슈 상세 화면이 딱 그렇다 — 사용자가 실시간으로 보낼 것이 없고 남이 바꾼 상태가 반영되기만 하면 된다. 이럴 때 쓰는 것이 Server-Sent Events, Spring에서 `SseEmitter`를 돌려주던 자리다.[^7-5] 이 장에서 인터넷 자료를 가장 조심해야 할 지점이다. 검색으로 나오는 글의 대다수가 `sse-starlette`을 설치하라고 안내하는데, SSE는 **FastAPI 0.135.0(2026-03-01)에 정식 지원으로 들어왔다.**

```python
# (개념 설명용 — 파일 아님)
from fastapi.sse import EventSourceResponse, ServerSentEvent


@app.get("/items/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
```

> 출처: FastAPI 공식 문서 *Server-Sent Events (SSE)*, https://fastapi.tiangolo.com/tutorial/server-sent-events/ (조회 2026-07-25)

눈여겨볼 것은 반환 타입 애너테이션이다. `AsyncIterable[Item]`이라고 적으면 `yield`된 항목 하나하나가 JSON으로 인코딩돼 이벤트의 `data` 필드에 실리고, **Pydantic 검증과 자동 문서화가 그대로 따라온다.** 3장에서 쏟은 공이 스트림에도 적용된다. 이벤트 종류나 재시도 간격을 지정하려면 항목 대신 `ServerSentEvent`를 `yield`한다.

기본으로 해주는 일도 있다. 문서가 이렇게 적는다.

> "Send a 'keep alive' ping comment **every 15 seconds**… Set the `Cache-Control: no-cache` header… Set a special header **`X-Accel-Buffering: no`** to prevent buffering in some proxies like Nginx."

세 줄 다 다음 절에서 만난다. 재접속도 챙겨준다 — 브라우저가 다시 붙을 때 마지막으로 받은 `id`를 `Last-Event-ID` 헤더에 실어 보내므로 서버가 그 지점부터 이어 보낼 수 있다.[^7-2]

그렇다면 `sse-starlette`은 쓸모없어졌을까? 그렇게 정리하면 틀린다. 3.4.6 / 2026-07 기준으로 여전히 릴리스되고, Starlette만 쓰거나 종료 시점을 세밀히 제어할 때 줄 수 있는 것이 더 많다. 정확히는 **겹치는 영역에서 1차 선택지가 옮겨간 것**이다.

## 어느 쪽이 필요한지는 네 가지 질문으로 갈린다

둘 중 하나를 고르는 일은 취향처럼 보이지만, 실제로는 네 가지 질문이 대부분을 결정한다.

| 질문 | SSE | WebSocket |
|---|---|---|
| 방향이 한쪽인가 | 서버 → 클라이언트 단방향 | 양방향 |
| 끊겼을 때 누가 다시 붙나 | 브라우저가 다시 붙고 `Last-Event-ID`로 이어받는다 | 재접속과 재구독을 직접 짠다 |
| 중간 장비를 얼마나 타나 | 평범한 HTTP 응답 — 버퍼링만 끄면 된다 | 핸드셰이크 포워딩 설정이 따로 필요하다 |
| 인증을 어디에 붙이나 | 일반 요청과 동일 | 핸드셰이크 때 붙이고, 그 뒤는 직접 정한다 |

세 번째 행이 실무에서 가장 자주 아프다. SSE는 평범한 HTTP 응답이라 앞단이 무엇이든 대체로 통과하고, WebSocket은 프로토콜 승격이 필요해 앞단이 그 사실을 알아야 한다.

네 번째 행은 결이 다르다. WebSocket 엔드포인트에서도 `Depends`·`Cookie`·`Header`·`Query`를 쓸 수 있으므로[^7-1] 수락 전에 신원을 확인하기는 어렵지 않다. 문제는 그 뒤다. 연결이 몇 시간 사는데 토큰이 중간에 만료되면? HTTP에서는 다음 요청이 401을 받고 끝날 일이 여기서는 **아무 일도 일어나지 않는다.** 인가는 10장의 몫이지만, 그 결정이 여기까지 온다는 것은 기억해두자.

`tracker`의 결정은 이렇다. 이슈 상세 화면의 갱신은 SSE로 간다 — 단방향이고, 브라우저가 알아서 다시 붙고, 앞단 설정이 필요 없다. 양방향 채널이 필요한 클라이언트를 위해 WebSocket도 함께 연다. 둘 다 같은 이벤트를 소비하니 배선은 하나다.

## 로컬에서만 되는 스트리밍

응답을 조금씩 흘려보내는 코드는 로컬에서 잘 돈다. 그리고 배포하면 종종 안 된다 — 화면에 아무것도 안 나오다가 작업이 끝난 뒤 한꺼번에 쏟아진다. 뒷맛이 찜찜하다 — 틀린 데가 없어 보이는데 결과만 다르다.

범인은 대개 앞단의 버퍼링이다. nginx 문서를 보면 `proxy_buffering` 기본값이 `on`이고, 켜져 있으면 응답을 모아뒀다가 내보낸다. 같은 문서가 빠져나갈 길도 알려준다.

> "Buffering can also be enabled or disabled by passing 'yes' or 'no' in the 'X-Accel-Buffering' response header field."

앞 절에서 내장 SSE가 자동으로 붙여주던 그 헤더이고, 두 문서가 정확히 맞물린다. 다만 **자동으로 붙는 것은 SSE 응답이고**, 직접 만든 스트리밍 응답에는 우리가 붙여야 한다.

```python
# (개념 설명용 — 파일 아님)
from fastapi.responses import StreamingResponse
```

`StreamingResponse`는 제너레이터를 받아 본문을 흘려보낸다.[^7-4] 문서가 하나 더 경고한다 — 비동기 작업은 `await`에 도달해야 취소되므로, `await`가 없는 제너레이터는 취소 요청을 받고도 계속 돌 수 있다. 창을 닫은 클라이언트를 위해 서버가 계속 일하고 있을 수 있다는 뜻이고, 5장과 같은 뿌리다.

느린 클라이언트는 어떨까. 초당 만 건을 만드는데 받는 쪽이 백 건씩만 읽어간다면 그 차이가 쌓일 텐데, 여기서는 서버가 막아준다.

> "If the write buffer passes a high water mark, then Uvicorn ensures the ASGI `send` messages will only return once the write buffer has been drained below the low water mark."

즉 버퍼가 차면 `await send()`가 돌아오지 않는다. 우리 코드는 기다리고 그 사이 메모리는 늘지 않는다 — 백프레셔가 `await` 하나로 표현된 셈이다.

연결 수명에도 손잡이가 있다. uvicorn 0.51.0 / 2026-07 기준으로 WebSocket 연결에는 20초 간격의 핑과 20초의 핑 타임아웃, 16MB의 메시지 크기 상한, 32라는 수신 큐 상한이 걸려 있다(뒤의 둘은 구현체를 `websockets`로 둔 경우다). 조용히 사라진 클라이언트를 서버가 알아채는 길이 이 핑이다. 앞단이 자기 유휴 타임아웃을 가질 수 있다는 것도 함께 보자. 클라이언트 주소나 프로토콜이 뒤바뀌는 문제는 별개이고 13장의 소재다.

## `tracker`의 알림이 흐르는 길

조각을 붙이자. 발행 → 팬아웃 → 전달, 셋뿐이다. 상태를 바꾸는 곳은 서비스 계층이다.

> **📐 저자 설계 —** 아래 배선은 발행 시점을 커밋 이후로 못 박기 위한 이 책의 선택이며, 공식 권장이 아니다.

```python
# src/tracker/services/issue.py
from datetime import datetime, timezone

from tracker.errors import NotFoundError
from tracker.events import EventBus
from tracker.models.issue import Issue, IssueStatus
from tracker.schemas.common import IssueEvent


class IssueService:
    # ...(6장, 생략)

    async def change_status(
        self, issue_id: int, status: IssueStatus, events: EventBus
    ) -> Issue:
        issue = await self.issues.get(issue_id)
        if issue is None:
            raise NotFoundError("이슈를 찾을 수 없다", code="issue.not_found")
        issue.status = status
        await self.session.commit()
        await events.publish(
            IssueEvent(
                issue_id=issue.id,
                event_type="status_changed",
                payload={"status": status.value},
                occurred_at=datetime.now(timezone.utc),
            )
        )
        return issue
```

발행이 `commit()` **뒤**에 있다는 것이 이 코드의 전부다. 순서를 뒤집으면 아직 커밋되지 않은 변경을 알리게 되고, 알림을 받은 클라이언트가 곧바로 조회했을 때 옛날 값을 본다. 6장에서 "커밋은 서비스 계층이 한다"고 정해둔 덕분에 커밋 직후라는 시점을 이 메서드가 안다. 버스를 생성자가 아니라 메서드 인자로 받은 것도 4장이 정한 생성자를 흔들지 않으려는 선택이다. 시그니처도 움직였다 — 2장 스텁은 `status: str`이었는데, 6장에서 `IssueStatus`가 생겼으니 타입을 좁히고 발행을 위해 인자를 하나 더 받는다.

버스는 앱이 사는 동안 하나면 된다. 4장에서 HTTP 클라이언트를 놓아둔 곳에 Redis 클라이언트를 나란히 놓는다.

```python
# src/tracker/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ...(2장, 생략)

    redis_url: str
```

```python
# src/tracker/main.py
import redis.asyncio as redis

from tracker.api.realtime import router as realtime_router
from tracker.settings import get_settings

# ...(4장, 생략)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = AsyncClient(timeout=5.0)
    app.state.redis = redis.from_url(get_settings().redis_url)
    yield
    await app.state.redis.aclose()
    await app.state.http_client.aclose()


app.include_router(router=realtime_router)
```

```python
# src/tracker/deps.py
from fastapi import Request

from tracker.events import EventBus, RedisEventBus

# ...(4장, 생략)


def get_event_bus(request: Request) -> EventBus:
    return RedisEventBus(request.app.state.redis)


EventBusDep = Annotated[EventBus, Depends(get_event_bus)]
```

의존성이 `Request`를 받아 앱 상태에 닿는다.[^7-6] 4장의 별칭 체계를 따르니 라우터 쪽은 타입 한 줄이다. 마지막이 전달이다.

```python
# src/tracker/api/realtime.py
import asyncio
from typing import AsyncIterable

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.sse import EventSourceResponse

from tracker.deps import EventBusDep
from tracker.events import EventBus
from tracker.schemas.common import IssueEvent

router = APIRouter(tags=["realtime"])


@router.get("/issues/{issue_id}/events", response_class=EventSourceResponse)
async def issue_events(issue_id: int, events: EventBusDep) -> AsyncIterable[IssueEvent]:
    async for event in events.subscribe(issue_id):
        yield event


@router.websocket("/ws/issues/{issue_id}")
async def issue_channel(
    websocket: WebSocket, issue_id: int, events: EventBusDep
) -> None:
    await websocket.accept()
    pusher = asyncio.create_task(push_events(websocket, events, issue_id))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        pusher.cancel()


async def push_events(websocket: WebSocket, events: EventBus, issue_id: int) -> None:
    async for event in events.subscribe(issue_id):
        await websocket.send_text(event.model_dump_json())
```

SSE 쪽은 세 줄이면 끝난다 — 구독을 `yield`로 흘려보내면 나머지는 프레임워크가 한다. WebSocket 쪽은 왜 더 복잡할까. 밀어주기만 하는 채널인데도 **읽는 루프가 하나 더 있다.** 이유는 앞에서 본 계약이다. 클라이언트가 사라졌다는 사실이 `WebSocketDisconnect`로 올라오는 곳은 수신 메서드다. 아무것도 안 읽으면 상대가 떠난 것을 늦게 알고, 그동안 태스크와 구독이 계속 살아 있다. 그래서 밀어주는 일은 별도 태스크로 떼고, 본체는 읽으면서 연결이 살아 있는지만 지킨다. 상위 프로토콜이 없다는 말의 실제 비용이 이 여덟 줄이다.

이 배선은 워커 4개, 레플리카 3개로 늘려도 버틴다. 12개 프로세스가 각자 구독하고, 어디서 상태가 바뀌든 발행은 한 번, 전달은 연결이 붙은 곳마다 일어난다. 그 숫자는 13장의 몫이지만 **무엇이 되든 이 코드는 그대로다.**

남겨둘 구멍도 있다. 이 배선은 발행을 한 번 시도하고 끝낸다. 그 순간 아무도 구독하고 있지 않으면 이벤트는 사라지고, 다시 붙은 클라이언트가 `Last-Event-ID`를 보내와도 되돌려줄 기록이 없다. 유실돼도 새로 고치면 되는 기능이면 이걸로 족하다. 유실이 곤란하다면 그건 팬아웃이 아니라 **큐**로 풀 문제이고, 그 이야기는 오래 걸리는 일들과 함께 다룬다.

---

실시간 기능을 붙일 때 던지는 첫 질문이 바뀌었으면 한다. "어떻게 연결할까"가 아니라 **"이 연결은 몇 개의 프로세스 중 하나에만 붙어 있는가"**다. 이 질문을 먼저 하면 팬아웃이 나중에 붙이는 기능이 아니라 처음부터 있을 구조로 보인다.

[^7-1]: `WebSocket`·`WebSocketDisconnect`·`WebSocketException`·`@router.websocket`, WS 엔드포인트의 `Depends`·`Cookie`·`Header`·`Query` — https://fastapi.tiangolo.com/advanced/websockets/ , https://fastapi.tiangolo.com/reference/apirouter/ · `accept()`·`receive_text()`·`send_text()`와 수신 시 `WebSocketDisconnect` — https://github.com/Kludex/starlette/blob/master/docs/websockets.md (조회 2026-07-26)

[^7-2]: `fastapi.sse`의 `EventSourceResponse`·`ServerSentEvent`, `AsyncIterable` 반환 규약, 15초 핑·`Cache-Control: no-cache`·`X-Accel-Buffering: no`, `Last-Event-ID` — https://fastapi.tiangolo.com/tutorial/server-sent-events/ · 0.135.0 SSE 정식 지원 — https://fastapi.tiangolo.com/release-notes/ (조회 2026-07-25)

[^7-3]: `redis.asyncio`·`from_url()`·`pubsub()`·`subscribe()`·`get_message()`·`publish()`·`aclose()` — https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html (조회 2026-07-26) · `aioredis` 흡수 — https://github.com/aio-libs-abandoned/aioredis-py

[^7-4]: `fastapi.responses.StreamingResponse`, 취소 축자 — https://fastapi.tiangolo.com/advanced/custom-response/ (조회 2026-07-26)

[^7-5]: STOMP 축자 — https://docs.spring.io/spring-framework/reference/web/websocket/stomp.html · SockJS 폴백 절, `SseEmitter`가 `ResponseBodyEmitter`의 하위 클래스라는 서술 — https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html (조회 2026-07-26)

[^7-6]: `request.app` 축자 — https://github.com/Kludex/starlette/blob/master/docs/requests.md (조회 2026-07-26)


# 8장. 오래 걸리는 일 — 스케줄링, 백그라운드 작업, 태스크 큐, 대용량 업로드

리포트 생성 버튼을 누르면 12초가 걸린다고 해보자. 프로젝트 하나의 이번 주 이슈를 전부 훑어 상태별로 세고 담당자별로 묶어 파일로 굽는다. 서버 입장에서 12초는 별일이 아니다. 그런데 화면 앞에 앉은 사람에게는 영원이고, 그 12초를 로드 밸런서가 참아줄지 프록시가 먼저 끊을지는 우리 손 밖이다.

답 자체는 이미 알고 있다. 응답은 지금 돌려주고 일은 뒤에서 한다. 예전 같으면 메서드에 비동기 실행 애너테이션 하나를 붙이고 끝냈을 것이다. FastAPI에도 그 자리를 채우는 물건이 있다. `BackgroundTasks`라는 이름이고, 쓰는 법은 정말로 한 줄이다.

문제는 그 한 줄이 무엇을 약속하고 무엇을 약속하지 않는지다. 12초짜리 리포트를 거기 얹어도 되는가? 그리고 이 일을 매주 월요일 아침 아홉 시에 자동으로 돌리고 싶어지면 — 그때부터 이야기가 완전히 달라진다.

## 응답을 보낸 뒤에 남는 것

먼저 계약부터 읽자. FastAPI 공식 문서는 이 기능을 한 문장으로 정의한다. *"You can define background tasks to be run **after** returning a response."* 응답을 돌려준 **다음에** 실행된다는 것. 경로 함수 파라미터로 `BackgroundTasks`를 선언하고, `add_task`에 함수와 인자를 넘기면 등록이 끝난다.[^8-1] 등록한 함수가 `async def`든 `def`든 상관없다 — 문서 축자로 *"It can be an `async def` or normal `def` function, FastAPI will know how to handle it correctly."*다.

그런데 같은 문서가 곧바로 선을 하나 긋는다.

> "If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery."

무거운 계산이고 같은 프로세스에서 돌 필요가 없다면 더 큰 도구를 보라는 것. 반대로 *"small background tasks (like sending an email notification)"* 정도라면 이걸로 충분하다고 한다. 공식 문서가 스스로 적용 범위를 좁힌 셈인데, 여기서 중요한 단어는 "heavy"가 아니라 **"the same process"**다.

정리하면 이렇다. 첫째, 태스크는 요청을 처리한 그 워커 프로세스 안에서 돈다. 둘째, 응답이 나간 뒤에 돈다. 셋째, 그러므로 **그 프로세스가 사라지면 태스크도 함께 사라진다.** 세 번째가 무섭다. 배포로 파드를 내리든, 오토스케일러가 인스턴스를 회수하든, 프로세스가 죽는 사건은 평범한 화요일 오후에도 일어난다.

서버가 대비를 안 하는 것은 아니다. uvicorn은 종료 절차에서 *"wait for any background tasks to run to completion"*을 보장한다. 응답은 나갔지만 아직 안 끝난 태스크를 기다려준다는 뜻이다. 다만 그 시간이 유한하다. 유예 시간이 끝나면 서버는 정리를 중단한다. 그래서 이 장은 13장에 요구 조건 하나를 넘겨둔다 — **백그라운드 태스크의 최악 실행 시간보다 종료 유예 시간이 길어야 한다.** 그 숫자를 정하는 일은 배포를 이야기할 자리의 몫이다.

한 가지 더 있다. 태스크가 **조용히 실패하는** 경로다. 응답 바깥에서 도니까 그 안에서 난 예외가 클라이언트에게 전달될 길이 구조적으로 없다. 그리고 실제로 물린 기록이 남아 있다. 이슈 #14137(2025-10)에서 백그라운드 태스크가 도는 방식에 회귀가 보고됐고, tiangolo가 제시한 처방은 `Depends(func, scope="function")`이었다. 4장에서 소개만 하고 넘어간 그 파라미터가 여기서 다시 나온 것이다.

왜 `yield` 의존성의 정리 시점이 백그라운드 태스크와 얽힐까? 순서를 그려보면 보인다. 응답이 나가고, 의존성이 정리되고, 태스크가 돈다 — 이 셋의 앞뒤가 어디서 갈리느냐에 따라 태스크가 손에 쥔 자원이 이미 닫혀 있을 수 있다. 그래서 규칙 하나를 정하자. **응답 뒤에 돌 코드에는 요청의 세션을 물려주지 않는다.** 넘기는 것은 식별자뿐이고, 태스크는 필요한 자원을 자기가 연다. 그리고 로깅도 태스크 안에 직접 넣자 — 밖에서 잡아주는 그물이 있다고 가정하지 말자.

## 어디까지 믿어도 되는가

그렇다면 12초짜리 리포트는 `BackgroundTasks`로 충분할까? 답하려면 "무겁다/가볍다"보다 나은 자가 필요하다. 무게는 사람마다 다르게 느끼지만, **유실됐을 때 무슨 일이 벌어지는가**는 팀이 함께 답할 수 있는 질문이다.

> 아래 네 문항은 **저자 기준**이다. 공식 권장도 업계 표준도 아니라 이 장의 계약 분석에서 도출한 것이며, 팀들이 실제로 어떤 기준으로 갈랐는지에 대한 증언은 리서치에서 찾지 못했다.

하나, 이 일이 사라지면 누가 아쉬운가? 알림 메일 한 통이 안 갔다면 사용자가 다시 누르면 된다. 결제 정산 기록이 안 남았다면 아무도 다시 눌러주지 않는다. **유실이 허용되지 않으면 큐다.** 프로세스와 함께 사라지는 물건에 원장을 맡길 수는 없다.

둘, 실패하면 다시 시도해야 하는가? `BackgroundTasks`에는 재시도도, 실패한 작업을 모아두는 곳도 없다. 직접 만들 수는 있지만, 그러기 시작하면 큐를 절반쯤 다시 짓게 된다.

셋, 몇 초 걸리는가? 앞 절의 종료 유예 시간이 상한이다. 12초짜리 리포트가 걸리는 곳이 여기다 — 유예 시간이 넉넉하면 살고 빠듯하면 죽는데, **"배포 설정에 따라 살기도 하고 죽기도 하는 기능"은 이미 설계가 잘못된 것이다.**

넷, 기다리는 일인가 계산하는 일인가? 5장에서 이 구분을 세우고 결론을 하나 미뤄뒀다 — 썸네일 생성 같은 CPU 바운드 작업을 스레드로 미는 것은 응급 처치일 뿐이라고. 스레드로 옮겨도 프로세스당 40이라는 자리는 그대로고, 계산 작업은 스레드로 옮긴다고 병렬로 돌지도 않는다. **오프로드는 이벤트 루프를 살릴 뿐 용량을 만들지 못한다.** 그러니 CPU를 진짜로 쓰는 일의 답은 처음부터 하나였다. 프로세스 밖으로 내보내는 것.

하나라도 걸리면 큐로 넘어간다. 하나도 안 걸리면 `BackgroundTasks`가 정답이다 — 브로커도 워커 배포도 없이 한 줄로 끝나는 선택지를 괜히 버릴 이유는 없다.

## 큐로 넘길 때 무엇을 보고 고를까

넘어가기로 했다고 하자. 파이썬 진영의 태스크 큐는 2026-07 기준 최근 릴리스 시점이 이렇다. Celery 5.6.3(2026-03) · arq 0.28.0(2026-04) · TaskIQ 0.12.4(2026-05) · Dramatiq 2.2.0(2026-06) · RQ 2.10.0(2026-06).

Node에서 Bull·BullMQ·Agenda를 붙이던 자리에 이 목록이 온다고 보면 된다. 여기서 어느 것이 낫다고 말하지는 않겠다. 이 책의 리서치에는 팀들이 무엇을 골랐고 왜 후회했는지에 대한 근거가 없고, 없는 근거로 서열을 매기지는 않기로 했다. 대신 **무엇을 보고 고를지**는 말할 수 있다. 다음 축들은 **저자 기준**이다.

- 우리 앱의 비동기 모델과 맞물리는가. 태스크 함수가 앱 코드를 임포트하는 순간 실무 문제가 된다. 6장에서 만든 것은 `AsyncSession`인데, 태스크 실행기가 코루틴을 직접 돌려주지 않으면 태스크 안에서 이벤트 루프를 따로 띄우거나 동기 세션을 하나 더 유지해야 한다. **데이터 계층을 두 벌 갖게 되는 것이 이 선택의 진짜 비용이다.**
- 브로커로 무엇을 요구하는가. 7장에서 이미 들여온 것이 있다면, 같은 것을 쓸 수 있는지부터 보는 편이 낫다. 운영할 미들웨어가 하나 느는 것은 생각보다 큰 결정이다.
- 재시도·데드레터·멱등성의 계약이 어떻게 생겼는가. 몇 번 다시 시도하는지, 끝내 실패한 작업이 어디로 가는지, 같은 작업이 두 번 실행돼도 안전한지. 마지막 항목은 도구가 아니라 우리 코드가 답해야 한다.
- 주기 실행이 내장돼 있는가. 다음 절의 주제이며, 여기에 답이 있으면 스케줄러를 따로 세우지 않아도 된다.
- 운영 중에 안이 보이는가. 대기 중인 작업 수, 실패 목록, 워커 상태. 없으면 큐는 블랙박스다.

Celery에 대해서는 한 가지를 정직하게 밝혀둔다. 이 책은 **Celery의 asyncio 네이티브 지원 여부에 대한 공식 진술을 확보하지 못했다.** 확인한 것은 정황뿐이다 — Celery 공식 문서의 concurrency 옵션 목록은 prefork · Eventlet · gevent · thread · solo이고, 그 목록에 asyncio 풀이 없다. 정황은 진술이 아니므로 여기서 멈춘다. 덧붙여 공식 문서는 5.5.x가 Python 3.8–3.13에서 돈다고 적어두고 있는데 PyPI 최신은 5.6.3이다. **5.6.x의 지원 범위**는 이 책이 확인하지 못했다. 도입을 검토한다면 이 둘은 직접 확인하고 넘어가자.

## 매주 월요일 아홉 시, 그리고 네 번

이제 리포트를 자동으로 돌릴 차례다. 주기 실행 애너테이션 한 줄, Quartz 설정 몇 줄, 또는 node-cron 한 줄로 끝내던 자리다. FastAPI에는 그 자리가 **비어 있다.** 주기 실행을 프레임워크가 주지 않으므로 층을 골라야 하고, 고를 수 있는 층은 셋이다.

앱 안에서 돌린다. 앱이 뜰 때 스케줄러를 함께 띄우고 시각이 되면 함수를 부른다. 배포 단위가 늘지 않아 가장 간단하다. 파이썬에는 이 역할의 라이브러리가 여럿 있는데, 이 책은 그중 어느 것의 현재 API·버전도 확인하지 못했다. 도구를 단정하는 대신 구조만 이야기하겠다.

큐 도구의 주기 기능을 쓴다. 앞 절의 축 네 번째다. 큐를 이미 세웠다면 스케줄도 거기 얹는 것이 자연스럽다.

배포 층에 맡긴다. 정해진 시각에 컨테이너를 하나 띄워 명령을 실행시키는 방식이고, 쿠버네티스라면 CronJob이 그 자리다. 앱 프로세스와 완전히 분리되는 것이 장점이자 단점이다.

세 층 중 첫 번째에 함정이 있다. **워커가 N개면 스케줄도 N번 돈다.**

이건 추측이 아니라 5장에서 확인한 사실에서 그대로 따라 나온다. `--workers`가 만드는 것은 스레드가 아니라 독립된 프로세스이고, 프로세스는 메모리를 공유하지 않는다. 앱 코드가 "앱이 뜰 때 스케줄러를 하나 띄운다"고 적혀 있으면, 워커 4개짜리 서버에서는 **스케줄러가 4개 뜬다.** 각자 자기 시계를 보다가 월요일 아홉 시에 각자 리포트를 만든다. 레플리카를 셋으로 늘리면 12개다. 곱셈이다.

7장에서 알림이 절반만 도착하던 문제와 정확히 대칭이다. 그쪽은 프로세스 경계 때문에 **덜 도착했고**, 이쪽은 같은 경계 때문에 **더 실행된다.**

더 고약한 것은 이 버그가 당신을 잘 피해 다닌다는 점이다. 로컬에서는 워커가 하나라 완벽하게 돌고 스테이징도 대개 하나다. 워커를 늘리는 것은 프로덕션의 결정이므로 **이 버그는 프로덕션에서만 나타난다.** 그것도 리포트 메일이 네 통 왔다는 제보로.

구조적인 답은 둘 중 하나다. 하나, 스케줄을 앱 밖으로 뺀다 — 위의 두 번째나 세 번째 층이 이 방향이다. 둘, 앱 안에 두되 여럿 중 하나만 실행하도록 조율한다. 조율에 쓰는 도구가 분산 락이나 리더 선출이고, 어느 쪽이든 프로세스 밖의 공유 저장소가 필요하다. 어차피 밖의 무언가가 필요하다면, 스케줄 자체를 밖에 두는 편이 단순한 경우가 많다.

기억해두자. 프레임워크는 "이 코드는 전체에서 한 번만 돌아야 한다"는 요구를 표현해주지 않는다. 그 요구는 우리가 적어야 한다.

## 1메가바이트라는 벽

`tracker`의 이슈에는 스크린샷이 붙고, 가끔 로그 덤프가 붙고, 아주 가끔 30메가바이트짜리 영상이 올라온다. 업로드를 받으려면 의존성이 하나 필요하다.

```bash
uv add python-multipart
```

파라미터에 `UploadFile` 타입을 적으면 끝이다. 여기서 나오는 첫 질문은 늘 같다. **이거 메모리에 다 올라오는 건가?** 공식 문서의 답은 "spooled" 파일이라는 것이다 — 어느 크기까지는 메모리에 두고, 그 선을 넘으면 디스크로 옮긴다. 그런데 그 선이 몇 바이트인지는 문서가 말해주지 않는다. 소스에 있다.

```python
class MultiPartParser:
    spool_max_size = 1024 * 1024  # 1MB
    """The maximum size of the spooled temporary file used to store file data."""
    max_part_size = 1024 * 1024  # 1MB
    """The maximum size of a part in the multipart request."""
```

> 출처: starlette 1.3.1 태그 `starlette/formparsers.py` (조회 2026-07-26)

값이 같아서 한 덩어리로 보이지만, 붙어 있는 설명이 이미 갈라진다. 하는 일이 전혀 다르다.

`spool_max_size`는 **메모리에서 디스크로 갈아타는 지점**이다. 1메가바이트까지는 메모리에 들고 있다가 넘어가면 임시 파일로 내려간다. 저장 위치의 문제이지 거부의 문제가 아니다. 그래서 "다 메모리에 올린다"도 틀렸고 "항상 디스크에 쓴다"도 틀렸다.

`max_part_size`는 **거부선**이다. 멀티파트의 한 파트가 이 크기를 넘으면 파서가 예외를 던진다. 앞의 것이 저장 위치를 정한다면 이건 통과 여부를 정한다.

문제는 두 번째 값이다. 1메가바이트는 첨부 파일 기준으로 너무 작다. 올리면 되지 않을까? 여기서 걸린다. 폼 파싱을 직접 부르는 쪽에는 이 값을 넘길 인자가 있지만, 우리가 쓰는 선언형 경로에는 그 인자를 넘길 손잡이가 없다.

```python
body = await request.form()
```

> 출처: fastapi 0.140.0 태그 `fastapi/routing.py` (조회 2026-07-26)

경로 함수 파라미터에 `UploadFile`을 적으면 FastAPI가 대신 부르는 것이 이 한 줄이다. **인자가 없다.** 그래서 기본값이 그대로 적용된다. 값을 바꾸려면 파싱을 직접 부르거나 파서 쪽에 손을 대야 한다. "필요하면 한도를 올려라"라는 조언을 어딘가에서 보게 되겠지만, 그 조언이 가리키는 곳이 이 경로에는 없다.

우연히도 서블릿 진영의 멀티파트 최대 파일 크기 기본값 역시 1메가바이트다. 숫자는 같은데 성질이 다르다. 그쪽에서는 설정 파일의 한 줄이 그 값을 바꾸고, 여기서는 그 한 줄을 적을 데가 없다. 번역이 잘 되는 듯하다가 마지막 한 칸에서 어긋나는 자리다.

이 층이 주는 것은 파트 단위 한도다. 요청 전체를 한 번에 막는 스위치가 아니다. 그래서 방어선은 대개 앱보다 앞에 선다 — 리버스 프록시의 바디 크기 제한, 또는 우리가 직접 얹은 ASGI 계층.

앱 안에서 크기를 확인할 방법이 아예 없는 것은 아니다. `UploadFile`에는 `size` 속성이 있고, 이건 헤더가 아니라 실제로 읽어들인 내용에서 계산된 값이다.[^8-2] `Content-Length`를 믿는 것보다 낫다.

## 첨부 하나를 받아내기

이제 조립하자. 6장은 `Attachment`에 파일 바이트를 넣지 않기로 했고, 어디에 둘지는 이 장으로 넘겼다.

그 답도 5장의 문장에서 나온다. 워커는 메모리를 공유하지 않고, 레플리카는 파일 시스템도 공유하지 않는다. 인스턴스 A가 로컬 디스크에 저장한 파일을 인스턴스 B가 내려줄 방법이 없으니, **컨테이너의 로컬 디스크는 단일 인스턴스 전제가 성립할 때만 저장소가 된다.** `storage_key`가 가리키는 곳은 프로세스 밖의 공유 저장소여야 한다. 아예 파일이 앱을 통과하지 않게 하는 선택지도 있다 — 클라이언트가 서명된 URL로 저장소에 직접 올리고 앱은 메타데이터만 받는 방식이다.

여기서는 앱을 통과시키는 쪽으로 간다. 방어선은 세 겹이다 — **크기를 제한하고, 스트리밍으로 저장하고, 무거운 것은 오프로드한다.**

> **📐 저자 설계 —** 아래 배선은 FastAPI 공식 권장이 아니라, 5장의 오프로드 규칙과 6장의 세션 규칙에서 이 책이 도출한 한 가지 안이다. 저장소 쓰기 함수는 어떤 저장소를 골랐는지에 따라 달라지므로 내부를 비워둔다.

```python
# src/tracker/services/attachment.py
from uuid import uuid4

from anyio import to_thread
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.attachment import Attachment

# ...(5장, 생략)

CHUNK_SIZE = 1024 * 1024


def append_to_storage(storage_key: str, chunk: bytes) -> None:
    ...


class AttachmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_attachment(
        self, *, issue_id: int, uploader_id: int, file: UploadFile
    ) -> Attachment:
        storage_key = f"issues/{issue_id}/{uuid4().hex}"
        size = 0
        while chunk := await file.read(CHUNK_SIZE):
            size += len(chunk)
            await to_thread.run_sync(append_to_storage, storage_key, chunk)

        attachment = Attachment(
            issue_id=issue_id,
            uploader_id=uploader_id,
            filename=file.filename or "unnamed",
            content_type=file.content_type or "application/octet-stream",
            size_bytes=size,
            storage_key=storage_key,
        )
        self.session.add(attachment)
        await self.session.commit()
        return attachment
```

조각으로 읽는 이유는 메모리다. 30메가바이트짜리를 한 번에 바이트열로 올리면 프로세스가 그만큼을 더 쓴다. 저장소 쓰기를 `to_thread.run_sync`로 감싼 것은 5장의 기본형 그대로다 — 저장소 클라이언트가 동기 라이브러리일 때 이벤트 루프를 지키는 방법이다.[^8-3] 비동기 클라이언트라면 이 줄은 그냥 `await`가 된다.

응답 스키마는 3장의 접미사 규약을 그대로 따른다.

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

라우터는 얇다.

```python
# src/tracker/api/attachments.py
from fastapi import APIRouter, UploadFile

from tracker.deps import CurrentUser, SessionDep
from tracker.errors import ValidationFailedError
from tracker.schemas.attachment import AttachmentRead
from tracker.services.attachment import AttachmentService

router = APIRouter(prefix="/issues/{issue_id}/attachments", tags=["attachments"])

MAX_UPLOAD_BYTES = 20 * 1024 * 1024


@router.post("", response_model=AttachmentRead, status_code=201)
async def upload_attachment(
    issue_id: int,
    file: UploadFile,
    session: SessionDep,
    user: CurrentUser,
) -> AttachmentRead:
    if file.size is not None and file.size > MAX_UPLOAD_BYTES:
        raise ValidationFailedError(
            "첨부 파일이 허용 크기를 넘었습니다", code="attachment.too_large"
        )
    service = AttachmentService(session)
    attachment = await service.add_attachment(
        issue_id=issue_id, uploader_id=user.id, file=file
    )
    return AttachmentRead.model_validate(attachment)
```

상수를 20메가바이트로 잡아뒀지만, 앞 절의 파트 한도를 그대로 뒀다면 여기 닿기 전에 파서가 먼저 거절한다. **앱 안의 검사는 그 한도를 옮긴 뒤에야 의미가 생긴다.** 두 값이 따로 논다는 것을 잊으면 20이 지켜지는 줄 안다.

썸네일은 여기 없다. 5장에서 CPU 바운드 작업의 답을 이미 정해뒀기 때문이다 — 프로세스 밖. 업로드 응답은 첨부 레코드만 돌려주고, 썸네일은 잠시 뒤 붙는다. 6장에서 `Attachment`의 `thumbnail_key`를 널 허용 타입으로 적어둔 것이 여기서 값을 한다. 그 "잠시 뒤"를 무엇이 책임지는지는 아래에서 정한다.

리포트로 돌아오자. 첫 버전은 이렇게 시작한다.

```python
# src/tracker/api/projects.py (8장에서 추가)
from fastapi import BackgroundTasks

from tracker.services.report import build_weekly_report

# ...(2장, 생략)


@router.post("/{project_id}/reports", status_code=202)
async def request_weekly_report(
    project_id: int,
    background_tasks: BackgroundTasks,
    user: CurrentUser,
) -> dict[str, str]:
    background_tasks.add_task(build_weekly_report, project_id)
    return {"status": "accepted"}
```

`build_weekly_report`가 받는 것은 프로젝트 식별자 하나뿐이다. 세션은 받지 않는다 — 앞에서 정한 규칙이다.

```python
# src/tracker/services/report.py
from tracker.db import session_factory


async def build_weekly_report(project_id: int) -> None:
    async with session_factory() as session:
        ...
```

6장의 세션 팩토리로 자기 세션을 자기가 여는 것이다.

이 버전은 언제까지 유효할까. 네 문항에 대보자. 유실되면 사용자가 다시 누르면 되고, 12초는 유예 시간 안이고, 작업 대부분은 데이터베이스를 기다리는 시간이다. 지금은 통과다. **그런데 전부 "지금은"이 붙는다.** 리포트가 40초로 늘어나면 세 번째가 깨지고, 자동 발송이 붙어 사람이 다시 누를 수 없게 되면 첫 번째가 깨진다.

깨졌을 때 코드가 얼마나 바뀔까. 한 줄이면 되도록 미리 접어두자.

> **📐 저자 설계 —** 아래 함수는 특정 태스크 큐의 API가 아니라, 어떤 도구를 고르든 그 뒤에 숨기려고 이 책이 만든 이음매다.

```python
# src/tracker/tasks.py
async def enqueue_weekly_report(project_id: int) -> None:
    ...


async def enqueue_thumbnail(attachment_id: int) -> None:
    ...
```

썸네일도 같은 모양이다. 업로드가 끝나면 `enqueue_thumbnail`을 부르고, 5장의 `generate_thumbnail`은 큐 워커 쪽에서 돈다 — 5장이 미뤄둔 "프로세스 밖"이 이 한 줄이다. 리포트 쪽은 라우터에서 `background_tasks.add_task(build_weekly_report, project_id)`를 `await enqueue_weekly_report(project_id)`로 바꾸면 승격이 끝난다. 라우터는 자기 일이 큐로 가는지 같은 프로세스에서 도는지 모른 채 남고, 도구를 바꿀 때 손댈 파일은 `tasks.py` 하나다.

---

이 장에서 반복된 문장이 하나 있다. **프로세스 경계는 프레임워크가 지워주지 않는다.** 태스크가 프로세스와 함께 사라지는 것도, 스케줄이 워커 수만큼 실행되는 것도, 로컬 디스크가 저장소가 되지 못하는 것도 전부 그 한 문장의 다른 얼굴이다. 5장에서 이 사실을 배웠고, 7장에서 알림으로 겪었고, 여기서는 세 번 더 만났다.

그러니 당신 앱에 물어볼 것이 있다. 응답 뒤에 도는 코드가 어디에 있는가. 그중 사라지면 곤란한 것이 있는가. 그리고 정해진 시각에 도는 코드가 있다면, 그건 몇 번 돌고 있는가.

[^8-1]: `from fastapi import BackgroundTasks`와 `background_tasks.add_task(func, *args, **kwargs)` 호출 형태, 태스크 함수가 `async def`·`def` 양쪽 모두 가능하다는 서술, 응답 이후 실행 보장 — FastAPI 공식 문서 *Background Tasks*, https://fastapi.tiangolo.com/tutorial/background-tasks/ (조회 2026-07-26)

[^8-2]: `UploadFile`의 속성 `filename`·`content_type`·`file`과 비동기 메서드 `read()`·`write()`·`seek()`·`close()`, 그리고 `python-multipart` 의존 — FastAPI 공식 문서 *Request Files*, https://fastapi.tiangolo.com/tutorial/request-files/ (조회 2026-07-26). `size` 속성은 starlette 1.3.1 태그 `starlette/datastructures.py`의 `UploadFile.__init__`에서 확인 (조회 2026-07-26)

[^8-3]: `from anyio import to_thread`와 `to_thread.run_sync(func, *args)` — 5장 각주에서 확인한 AnyIO 공식 문서 *Working with threads*, https://anyio.readthedocs.io/en/stable/threads.html. `Session.add()`·`Session.commit()`의 호출 형태 — SQLAlchemy 2.0 *Session Basics*, https://docs.sqlalchemy.org/en/20/orm/session_basics.html (둘 다 조회 2026-07-26)


# 9장. API 너머 — 화면을 붙이고, 다른 서비스와 말하기

여덟 장을 지나오는 동안 `tracker`가 바깥으로 내보낸 것은 전부 JSON이었다. 조회 응답도, 3장에서 정한 `ErrorResponse`도, 7장의 실시간 채널조차 결국 JSON을 밀어내는 통로였다.

그런데 실무의 웹 애플리케이션이 전부 그렇게 생기지는 않았다. 운영팀은 브라우저에서 바로 여는 관리자 화면을 원한다. 모바일 팀은 화면마다 필요한 필드가 달라 응답을 자기가 고르고 싶어 한다. 그리고 이슈 검색은 사내 검색 서비스가 갖고 있다.

앞의 둘은 우리 앱이 무엇을 보여줄 것인가의 문제이고, 마지막 하나는 누구에게 말을 걸 것인가의 문제다. 여기서 할 일은 각 방향을 끝까지 파는 것이 아니라, 첫걸음에서 무엇을 밟게 되는지 표시해두는 쪽이다.

## 화면 하나를 서버가 그리려면

서버 렌더링부터 보자. 컨트롤러가 뷰 이름을 돌려주면 뷰 리졸버가 Thymeleaf나 JSP 템플릿을 찾아주던 층, Express라면 EJS를 걸어두던 자리 — 그 층은 어디로 갔을까? 여기엔 아예 없다. 경로 함수는 뷰 이름이 아니라 **렌더링 결과 객체를 직접 만들어 돌려준다.** 준비물은 정적 파일 마운트 하나와 템플릿 객체 하나뿐이고, 설치는 필요 없다 — `fastapi[standard]`가 jinja2를 함께 끌어온다.

```python
# src/tracker/main.py
from pathlib import Path

from fastapi.staticfiles import StaticFiles

# ...(4장, 생략)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
```

> **📐 저자 설계 —** 아래 관리자 화면의 배선은 FastAPI 공식 권장이 아니라, `tracker`의 모듈 레이아웃에 맞춰 이 책이 정한 한 가지 안이다.

```python
# src/tracker/api/admin.py
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from tracker.deps import IssueServiceDep

router = APIRouter(prefix="/admin", tags=["admin"])

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/issues", response_class=HTMLResponse)
async def issue_board(request: Request, service: IssueServiceDep):
    issues = await service.list_open_issues()
    return templates.TemplateResponse(
        request=request, name="issue_board.html", context={"issues": issues}
    )
```

화면이 쓸 조회는 아직 없다. 6장이 정한 대로 쿼리는 리포지터리가 갖고 서비스는 도메인 이름만 준다.

```python
# src/tracker/repositories/issue.py (9장에서 추가)
from tracker.models.issue import Issue, IssueStatus

# ...(6장, 생략)

    async def list_open(self, limit: int, offset: int) -> list[Issue]:
        stmt = (
            select(Issue)
            .where(Issue.status == IssueStatus.open)
            .order_by(Issue.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(await self.session.scalars(stmt))
```

```python
# src/tracker/services/issue.py (9장에서 추가)
    async def list_open_issues(self, limit: int = 50, offset: int = 0) -> list[Issue]:
        return await self.issues.list_open(limit, offset)
```

이 절의 지뢰는 `TemplateResponse`의 **인자 순서**다. 공식 문서가 직접 달아둔 주석은 이렇게 읽힌다. *"Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter."* 인터넷에 널린 `templates.TemplateResponse("item.html", {"request": request})` 형태는 옛 시그니처다.[^9-1]

보통은 "구식 예제이니 주의하라"로 끝날 이야기인데, 한 칸 더 나쁘다. **Starlette 1.0.0(2026-03-22)이 옛 시그니처를 완전히 제거했다.** 이 책이 전제하는 스택은 Starlette 1.3.1 / 2026-06 기준이니, 1.x를 물어온 환경에서는 옛 형태가 경고를 내며 도는 게 아니라 그냥 **동작하지 않는다.** 4장에서 본 그대로다 — 핀 하한은 아직 `starlette>=0.46.0`이라, 락파일에 0.4x가 들어왔다면 같은 코드가 경고만 낼 수도 있다.

두 번째로 기억할 것은 `request`가 선택 사항이 아니라는 점이다. Starlette 문서가 굵게 못 박는다 — *"Note that the incoming request instance must be included as part of the template context."* 대가로 템플릿 안에서 `url_for('read_item', id=id)`처럼 경로 함수 이름으로 URL을 만들 수 있고, 정적 파일도 `url_for('static', path='/styles.css')`로 참조된다.

## 조각으로 돌려주기

이슈 목록이 뜨고 각 행에 상태를 바꾸는 버튼이 있다고 하자. 페이지 전체를 다시 그릴 이유는 없다 — 바뀐 것은 행 하나다. 자바스크립트로 JSON을 받아 DOM을 갱신하는 쪽이 하나, 서버가 HTML 조각을 돌려주고 브라우저가 그 자리에 끼워 넣는 쪽이 하나다. 후자를 위해 만들어진 것이 HTMX다.

```html
<!-- src/tracker/templates/issue_row.html -->
<tr id="issue-{{ issue.id }}">
  <td>{{ issue.title }}</td>
  <td>{{ issue.status }}</td>
  <td>
    <button hx-post="/admin/issues/{{ issue.id }}/resolve"
            hx-target="#issue-{{ issue.id }}"
            hx-swap="outerHTML">해결</button>
  </td>
</tr>
```

`hx-post`는 그 URL로 POST를 보내고, `hx-target`은 바꿔치기할 요소를, `hx-swap`은 바꿔 끼우는 방식을 정한다.[^9-2] 서버 입장에서 달라지는 것은 하나다. **응답이 JSON이 아니라 HTML 조각이어야 한다.**

엔드포인트를 두 벌 만들 필요는 없다. HTMX가 보내는 요청에는 `HX-Request` 헤더가 항상 `true`로 붙어서,[^9-2] 이 헤더 하나로 한 경로에서 갈라 쓸 수 있다. 파라미터를 `hx_request`로 적어도 되는 것은 `Header`가 *"by default ... convert the parameter names characters from underscore (`_`) to hyphen (`-`)"* 하기 때문이다.[^9-6]

> **📐 저자 설계 —** 아래 분기는 HTMX·FastAPI 조합에 대한 공식 가이드가 아니다. 확인된 것은 헤더의 존재와 의미뿐이고, 그것을 한 경로에서 쓰는 방식은 이 책이 고른 한 가지 배치다.

```python
# src/tracker/api/admin.py
from typing import Annotated

from fastapi import Header

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
    name = "issue_row.html" if hx_request else "issue_board.html"
    return templates.TemplateResponse(
        request=request, name=name, context={"issue": issue}
    )
```

`events`는 7장이 정한 시그니처를 따르는 것이다. 덕분에 관리자가 버튼을 누르면 그 변경이 7장의 채널로도 발행된다 — 화면 하나를 붙였을 뿐인데 실시간 알림이 딸려 온다.

대가는 분명하다. **화면의 모양이 서버 라우터 안으로 들어온다.** 어느 조각이 어느 요소를 대체하는지가 파이썬 조건문에 적히면, 프론트엔드 변경이 백엔드 배포를 요구한다. 화면을 고치는 사람이 당신이 아니라면 이 결합은 곧 두 팀의 일정 결합이다.

7장의 SSE와 헷갈리기 쉬우니 정리하자. 셋은 갱신을 누가 시작하느냐에서 갈린다.

| 방식 | 갱신을 시작하는 쪽 | 서버가 돌려주는 것 | 화면 상태가 사는 곳 |
|---|---|---|---|
| HTMX 부분 갱신 | 클라이언트(사용자 조작) | HTML 조각 | 서버 |
| SSE (7장) | 서버(이벤트 발생) | 이벤트 스트림 | 서버와 브라우저가 나눠 가짐 |
| SPA | 클라이언트(코드) | JSON | 브라우저 |

섞어도 된다. 방금 본 코드가 그 모양이다 — 버튼 조작은 HTMX로 받고, 남이 바꾼 이슈는 SSE로 밀려 들어온다. 다만 같은 행을 두 경로가 갱신하므로 어느 쪽이 최종 승자인지는 정해두어야 한다.

## SPA를 얹을 때

세 번째 길은 프론트엔드를 별도 프로젝트로 빌드해 결과물을 서빙하는 것이다. 디렉터리 하나 마운트하면 끝날 것 같지만 **히스토리 폴백**에서 걸린다. `/admin/issues/42`를 주소창에 직접 입력하면 그 경로의 파일이 디스크에 없다 — 클라이언트 라우팅이 처리할 경로인데 서버가 먼저 404를 낸다.

FastAPI는 0.138.0(2026-06)에서 이 일을 전담하는 메서드를 추가했다. 시그니처는 `frontend(path, directory, fallback="auto", check_dir=True)`이고, 내부에서 `StaticFiles`를 쓰되 프론트엔드용 처리를 얹은 형태다. `StaticFiles` 문서도 이제 맨 위에서 안내한다. *"If you need to host a frontend, use `app.frontend()` instead."*[^9-7]

눈여겨볼 것이 둘이다. 첫째, 경로 연산을 먼저 확인하고 매칭되는 것이 없을 때만 프론트엔드 파일을 본다. 둘째, 폴백은 `Accept: text/html`(또는 `application/xhtml+xml`)이 붙은 GET·HEAD 요청에만 적용된다. 없는 자바스크립트나 이미지에 `index.html`을 200으로 돌려주는 흔한 사고가 이래서 막힌다 — 없는 자원은 여전히 404다. 그리고 0.139.0(2026-07)부터는 이 응답에도 의존성을 걸 수 있어, 쿠키 인증으로 정적 자산까지 보호할 수 있다.[^9-7]

다만 FastAPI 0.140 / 2026-07 기준으로도 여전히 새 표면이니, 세부 동작은 공식 문서를 함께 확인하자.

여기까지 답한 질문은 하나였다. 이 앱이 **사람**에게 무엇을 보여줄 것인가. 상대가 **다른 서비스**로 바뀌면 그 전제가 무너진다. 상대는 자기 스키마를 갖고 오고, 느려지거나 죽는 일에 우리는 아무 권한이 없다.

## 타입 선언이 스키마가 되는 세 번째 방식

응답을 자기가 고르고 싶다는 모바일 팀의 요구 — GraphQL이 답하려는 문제다. FastAPI 공식 문서는 라이브러리를 하나 지목한다. *"If you need or want to work with GraphQL, Strawberry is the recommended library as it has the design closest to FastAPI's design, it's all based on type annotations."*

인터넷에는 Starlette의 `GraphQLApp`을 쓰는 예제가 아직 남아 있는데, **그건 2021년에 끝난 이야기다.** 0.15.0에서 폐기 예고, 0.17.0(2021-11-04)에서 제거됐다. Starlette 1.0과는 무관한 사건이다.

Strawberry는 파이썬 타입 애너테이션으로 스키마를 만든다. 3장에서 Pydantic이 하던 일과 발상이 같다. 설치는 `uv add "strawberry-graphql[fastapi]"` 한 줄이다.

> **📐 저자 설계 —** 아래 스키마는 `tracker`의 읽기 전용 조회를 위해 이 책이 정한 최소 형태다. Strawberry가 제공하는 표면 자체는 공식 문서에 있는 그대로다.

```python
# src/tracker/api/graphql.py
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class IssueType:
    id: int
    title: str
    status: str

@strawberry.type
class Query:
    @strawberry.field
    async def issue(self, issue_id: int) -> IssueType:
        ...

schema = strawberry.Schema(Query)
graphql_router = GraphQLRouter(schema)
```

등록은 다른 라우터와 똑같이 `app.include_router(router=graphql_router, prefix="/graphql")` 한 줄이고, REST와 병존시키는 데 특별한 장치가 필요 없다.[^9-3]

몸통을 비워둔 데는 이유가 있다. 리졸버는 세션을 얻어야 하는데, 4장의 `SessionDep`을 그대로 쓸 수 있는지가 확실하지 않다. 리졸버를 부르는 쪽이 FastAPI의 의존성 해석기가 아니라 Strawberry의 실행기이기 때문이다. 이 배선은 확인하지 못했으니 Strawberry 문서에서 직접 보고 넘어가자.

가장 비싼 사실이 남았다. Strawberry 공식 문서의 경고를 그대로 옮긴다.

> *"FastAPI processes sync endpoints in a threadpool and async endpoints using the event loop. However, Strawberry processes sync and async fields using the event loop, which means that using a `sync def` will block the entire worker."*

5장을 기억하는가. `def`로 선언한 경로 함수는 스레드풀로 오프로드된다. 그 40개짜리 스레드풀은 실은 **안전망**이었다. 리졸버에는 그 안전망이 없다 — 필드 하나를 `def`로 선언하면 워커 전체가 선다. "선언 키워드가 실행 장소를 정한다"던 규칙이 여기서는 적용되지 않는다. 처방은 문서가 직접 말한다 — 모든 필드를 `async def`로, 도저히 안 되면 `starlette.concurrency.run_in_threadpool`로 감싸라. 취향이 아니라 사고 예방이다.

한 가지 더. GraphQL 스키마를 얹는다는 것은 `tracker`가 **같은 데이터를 세 번 선언**한다는 뜻이다. 6장의 SQLAlchemy 매핑, 3장의 Pydantic 스키마, 방금 만든 Strawberry 타입. 필드 하나에 세 곳을 고쳐야 하고, 그 셋을 묶어주는 층은 여기 없다.

## 나가는 호출 — 기본값은 있고, 재시도는 없다

이제 방향을 뒤집자. 사내 검색 서비스에 물어보는 쪽이다. 먼저 정할 것은 HTTP 클라이언트를 언제 만드느냐인데, 답은 4장에서 정해뒀다. lifespan에서 `AsyncClient`를 만들어 `app.state.http_client`에 올려두고 종료할 때 닫는다. 여기서 새로 만들 일은 없다 — 요청마다 만들면 커넥션 풀이 요청마다 생겼다 버려진다. 꺼내 쓸 때는 요청 객체를 거친다. Starlette 문서가 *"the app is available on `request.app`"*이라고 안내하므로, 경로 함수에서는 `request.app.state.http_client`로 닿는다.[^9-5]

기본값은 한 번 들여다보자. httpx는 타임아웃을 **기본으로 켜두고** 시작한다. 네트워크가 5초간 조용하면 예외를 던지며, 타임아웃은 연결·읽기·쓰기·풀 네 종류다. 커넥션 풀에도 기본값이 있다 — 최대 연결 100개, 유지 연결 20개, 유휴 만료 5초.[^9-4] 그냥 지나치지 말자. 6장 끝에서 데이터베이스 커넥션을 셀 때 했던 산술이 반복된다. **워커 수 × 레플리카 수 × 100.** 3레플리카에 워커 4개면 상대 서비스 입장에서 최대 1,200개다. 필요하면 `limits`로 낮춰 잡자.

진짜 차이는 `retries`에 있다. 공식 문서의 문장은 이렇게 읽힌다.

> *"Requests will be retried the given number of times in case an `httpx.ConnectError` or an `httpx.ConnectTimeout` occurs, allowing smoother operation under flaky networks."*

`ConnectError`와 `ConnectTimeout`. **연결을 맺는 데 실패한 경우만** 재시도한다. 상대가 503을 돌려주면 재시도하지 않고, 읽기 타임아웃이 나도 재시도하지 않는다. 연결은 멀쩡히 맺혔으니까.

선언 한 줄로 백오프까지 붙던 감각으로 오면 여기서 **반드시 틀린다.** 그리고 틀린 티가 나지 않는다. `retries=3`이 적혀 있으면 리뷰도 통과하고 평소에도 잘 돈다. 상대가 500을 뿜는 날에만 아무 일도 일어나지 않을 뿐이다. 찜찜한 안전장치다. httpx 문서 자신이 이 한계를 인정하고, 503이나 읽기·쓰기 오류에 반응하려면 `tenacity` 같은 범용 도구를 보라고 적어두었다.[^9-4]

그 도구를 예제로 끌어들이는 대신 구조만 남겨두자. 복원력은 세 겹이다. 타임아웃은 이미 켜져 있으니 값만 조정한다. 재시도의 기준은 상태 코드가 아니라 멱등성이다 — 조회는 다시 불러도 되지만, 무언가를 만드는 호출은 상대가 이미 처리했는데 응답만 못 받았을 수 있다. 차단은 연속 실패가 쌓이면 호출을 멈추고 즉시 실패시킨다.

세 번째 겹이 문제다. **이 책은 파이썬·asyncio 진영의 서킷 브레이커 지형을 조사하지 않았다.** 이름이 오르내리는 `pybreaker`조차 최신 버전도 비동기 지원 범위도 확인하지 못했다. 그래서 도구 대신 패턴만 남긴다. 실패를 세는 카운터, 임계치, 열린 뒤 다시 시도해보는 간격 — 셋이 전부이고, 설계 지점은 그 상태를 어디에 두느냐다. 프로세스 안에 두면 워커마다 따로 열리고 닫힌다. 7장과 8장에서 만난 그 경계다.

> **📐 저자 설계 —** 아래 클라이언트 래퍼와 실패 매핑은 이 책이 정한 구조다. httpx가 제공하는 표면 자체는 공식 문서에 있는 그대로다.

```python
# src/tracker/clients/search.py
import httpx
from httpx import AsyncClient

from tracker.errors import ExternalServiceError

class SearchClient:
    def __init__(self, client: AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url

    async def search_issues(self, keyword: str) -> list[dict]:
        try:
            response = await self._client.get(
                f"{self._base_url}/search", params={"q": keyword}, timeout=2.0
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalServiceError("검색 서비스를 사용할 수 없다") from exc
        return response.json()["items"]
```

```python
# src/tracker/api/issues.py
from fastapi import Request

from tracker.clients.search import SearchClient
from tracker.deps import SettingsDep

# ...(2장, 생략)

@router.get("/search")
async def search_issues(request: Request, q: str, settings: SettingsDep) -> list[dict]:
    client = SearchClient(request.app.state.http_client, settings.search_service_url)
    return await client.search_issues(q)
```

눈여겨볼 곳은 예외를 옮겨 담는 줄이다. `httpx.HTTPError`는 요청 실패와 `raise_for_status()`가 던지는 상태 오류를 함께 아우르는 상위 클래스라, 이 한 줄이 바깥 세계의 실패를 3장의 `ExternalServiceError`로 모아준다.[^9-4] 그러면 3장의 핸들러가 502와 `ErrorResponse` 모양으로 내보낸다 — 예외 핸들러는 여전히 세 개다. `base_url`을 래퍼가 갖는 것도 의도적이다. 앱 전체가 공유하는 클라이언트에 특정 상대의 주소를 박아둘 수는 없으니, 주소는 2장의 `Settings`에 얹는다.

```python
# src/tracker/settings.py
class Settings(BaseSettings):
    # ...(2장, 생략)

    search_service_url: str
```

## BFF의 경계 — 무엇을 모아주고 무엇을 흘려보낼 것인가

모바일 화면 하나를 그리는 데 이슈 조회, 검색, 알림 설정까지 세 곳을 물어야 한다면, 그 세 번의 왕복은 누가 감당하는가? 클라이언트가 각자 호출하게 둘 수도 있고, 우리 앱이 대신 호출해 한 번의 응답으로 합쳐줄 수도 있다. 후자를 흔히 BFF라고 부른다.

여기서 근거의 두께를 먼저 밝혀두는 게 정직하겠다. **BFF는 업계 관행이지 정립된 이론이 아니다.** 이 책을 준비하며 학술 문헌을 뒤졌을 때 BFF를 정면으로 다룬 것은 사실상 한 편(Microusity, ICPC 2023)뿐이었다. 그러니 아래 판단 기준은 논문이 보증하는 것이 아니라 **저자의 기준**이고, 당신 팀의 사정에 따라 다르게 그어도 된다.

| 이런 요청은 | 판단 | 이유 |
|---|---|---|
| 한 화면이 여러 서비스를 불러야 한다 | 모아준다 | 모바일 회선에서는 왕복 수가 체감 성능을 지배한다 |
| 상대 응답을 그대로 쓴다 | 흘려보낸다 | 중계만 하는 계층은 상대 스키마 변경을 두 번 겪게 만든다 |
| 권한 판정이 끼어든다 | 모아준다 | 클라이언트가 판정하면 그건 판정이 아니다 |
| 페이로드가 큰데 화면은 일부만 쓴다 | 모아준다 | 잘라서 보내는 것이 BFF의 본래 일이다 |
| 파일 업로드·다운로드 | 흘려보낸다 | 바이트를 두 번 통과시키면 메모리와 대역이 두 배가 된다 (8장) |

실패 처리도 미리 정해야 한다. 세 곳 중 한 곳이 죽으면 전체를 502로 실패시킬 것인가, 나머지만 모아 돌려줄 것인가? 기준은 화면 쪽에 있다. 그 조각이 없어도 화면이 의미를 갖는다면 결손 표시를 담은 부분 응답을, 화면의 존재 이유라면 실패를 돌려주자. 어느 쪽이든 **클라이언트가 구별할 수 있는 형태여야** 한다. 조용히 빈 배열을 돌려주는 것이 가장 나쁘다.

앞 절의 GraphQL과 이 절의 BFF가 같은 문제를 다르게 푼다는 것도 눈치챘을 것이다. 클라이언트 종류가 적고 화면 구성이 안정적이면 **BFF 엔드포인트**가 싸게 먹히고, 여럿이고 요구가 계속 바뀌면 **스키마**가 값을 한다. 둘 다 얹어놓고 어느 쪽도 관리하지 않는 상태가 가장 비싸다.

---

한 장 만에 `tracker`가 늘린 표면이 세 개다. 브라우저에 내보내는 템플릿과 정적 파일, 외부 클라이언트에게 약속한 스키마, 우리 손 밖에 있는 서비스에 대한 의존.

셋 다 공짜가 아니다. 정적 파일은 이미지에 구워질지 따로 배포될지 정해야 하고, 리졸버는 어느 실행 장소에서 도는지 매번 확인해야 하고, 바깥 호출은 상대의 나쁜 날을 우리 응답 시간으로 받아낸다. 여덟 장 동안 쌓아온 것이 "어떻게 쓰는가"였다면, 늘어난 세 표면은 다른 질문을 꺼낸다.

**이걸 전부 감당한 채로, 어떻게 프로덕션에 올릴 것인가.**

[^9-1]: `Jinja2Templates`·`HTMLResponse`·`StaticFiles` import 경로, `app.mount(...)`·`TemplateResponse(request=…, name=…, context=…)`·`url_for` 호출 형태, 주석 축자 *"Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter."* — FastAPI 공식 문서 *Templates*(https://fastapi.tiangolo.com/advanced/templates/)·*Static Files*(https://fastapi.tiangolo.com/tutorial/static-files/) (조회 2026-07-26)

[^9-2]: `hx-post`·`hx-target`·`hx-swap`의 정의와 요청 헤더 `HX-Request`(*"always 'true'"*) — htmx 공식 레퍼런스, https://htmx.org/reference/ (조회 2026-07-26)

[^9-3]: `strawberry.type`·`strawberry.field`·`strawberry.Schema`·`strawberry.fastapi.GraphQLRouter` 표면과 sync 리졸버 경고 원문 — Strawberry 공식 문서 *FastAPI Integration*, https://strawberry.rocks/docs/integrations/fastapi (조회 2026-07-26)

[^9-4]: `AsyncClient`의 `limits`·`base_url`·`transport`와 풀 기본값, `httpx.Limits(...)`, `httpx.AsyncHTTPTransport(retries=1)`과 `retries` 동작 범위·`tenacity` 언급, `client.get(...)`·`response.json()`, `httpx.HTTPError`(*"Base class for `RequestError` and `HTTPStatusError`"*)·`raise_for_status()` — httpx 공식 문서 *API Reference*·*Resource Limits*·*Transports*·*Async*·*QuickStart*·*Exceptions*, https://www.python-httpx.org/api/ 외 (조회 2026-07-26). 타임아웃 5초는 4장 각주에서 확인했다

[^9-5]: *"Where a `request` is available (i.e. endpoints and middleware), the app is available on `request.app`."* — Starlette 공식 문서 *Applications*, https://www.starlette.io/applications/ (조회 2026-07-26)

[^9-6]: `Header`의 언더스코어→하이픈 자동 변환과 `convert_underscores` — FastAPI 공식 문서 *Header Parameters*, https://fastapi.tiangolo.com/tutorial/header-params/ (조회 2026-07-26)

[^9-7]: `frontend(path, directory, fallback="auto", check_dir=True)` 시그니처, 경로 연산 우선 확인(*"checked only if no normal route matched"*)·`Accept: text/html`/`application/xhtml+xml` GET·HEAD 폴백·누락 자원 404·`StaticFiles` 상단 안내 — FastAPI 공식 문서 *Frontend*, https://fastapi.tiangolo.com/tutorial/frontend/. 0.138.0(2026-06-20) 추가, 0.139.0(2026-07-01) *"Support dependencies in `app.frontend()`"* — https://fastapi.tiangolo.com/release-notes/ (조회 2026-07-26)


# 10장. 인증과 인가 — Spring Security를 직접 조립하기

`passlib`의 마지막 릴리스는 1.7.4이고, 2020년 10월 8일에 올라왔다.

그 라이브러리가 더는 관리되지 않는 것 같으니 공식 문서를 바꾸는 게 어떻겠냐는 신고가 FastAPI 저장소에 올라온 날은 2024년 6월 28일이다. 문서 예제가 다른 라이브러리로 갈아탔다는 공지가 그 스레드에 붙은 날은 2025년 9월 30일이다.[^10-4]

세 날짜를 나란히 놓고 잠시 멈춰보자. 그 사이의 어느 날, 공식 문서를 그대로 따라 로그인 기능을 만든 사람이 있다. 그 사람의 코드는 무엇으로 비밀번호를 해싱하고 있었을까.

인증 이야기를 꺼내면 먼저 떠오르는 건 부재다. 요청 앞을 지키는 필터 사슬이 없고, 메서드 위에 한 줄로 붙이던 권한 애너테이션이 없다. 그런데 직접 조립의 청구서는 그런 부재 옆으로 오지 않는다. 위의 날짜들처럼, 한참 뒤에 시간 단위로 날아온다.

## 프레임워크가 주는 것의 정확한 크기

먼저 FastAPI가 인증에 대해 무엇을 주는지 재보자. `fastapi.security` 아래에는 스킴 클래스들이 있고, 공식 튜토리얼이 전면에 세우는 것이 `OAuth2PasswordBearer`다.[^10-1] 이름이 거창해서 이 물건이 인증을 해주는 것처럼 보이는데, 실제로 하는 일은 셋이다. 요청 헤더에서 Bearer 토큰 문자열을 꺼내 넘겨주고, 토큰이 없으면 401을 돌려주고, `/docs`에 Authorize 버튼을 붙인다.

거기까지다. **그 토큰이 유효한지, 누구의 것인지, 그 사람이 이 이슈를 닫아도 되는지는 이 클래스가 모른다.** 스펙을 표현하고 문서에 노출하는 장치이지 정책 실행기가 아니다.

구조를 대조하면 차이가 분명해진다. 요청이 라우팅에 닿기 전에 필터 사슬을 지나며 인증 주체가 채워지고 접근 규칙이 적용되는 구조에 익숙하다면, 여기엔 그 사슬이 통째로 없다는 것부터 받아들여야 한다. 검사는 경로마다, 또는 라우터마다 붙는 의존성으로 들어온다. 즉 **보안이 앞단의 층이 아니라 경로 함수의 시그니처에 적힌다.** 무엇이 무엇을 요구하는지 설정을 뒤지지 않고 코드에서 읽힌다.

대가도 같은 곳에서 나온다. 기본값이 "막힘"이 아니라 "열림"이다. 새 엔드포인트를 만들며 의존성 한 줄을 빠뜨리면 그 경로는 그냥 공개되고, 아무도 경고해주지 않는다. 그래서 조립 전에 규칙 하나를 정해두는 편이 낫다. **인증이 필요 없는 경로를 예외로 관리한다** — 목록이 짧은 쪽을 세는 것이다.

## 부품의 생사는 누가 지키는가

오프닝의 날짜에는 사실과 판단이 섞여 있다.

**사실은 이렇다.** `passlib`의 마지막 릴리스는 1.7.4이고 2020년 10월 8일자다. `python-jose`의 마지막 릴리스는 3.5.0이고 2025년 5월 28일자다(둘 다 2026-07 기준). **해석은 여기서 갈린다.** "사실상 방치됐다"는 문장은 릴리스 간격을 근거로 한 판단이지 날짜 자체가 아니다. 나는 그 판단이 타당하다고 보지만 그건 내 판단이고, 확인된 것은 같은 판단을 커뮤니티가 신고로 먼저 했고 문서가 결국 바뀌었다는 기록이다.

기록을 시간표로 펼치면 이렇다.[^10-4]

| 사건 | 최초 제기 | 마무리 | 걸린 시간 |
|---|---|---|---|
| `python-jose` 문서 교체 (#9587) | 2023-05-29 | 2024-05-20 문서가 PyJWT로 변경 | 약 1년 |
| `passlib` 문서 교체 (#11773) | 2024-06-28 | 2025-09-30 pwdlib 전환 공지 | 약 15개월 |
| FastAPI **테스트 스위트**의 `passlib` (#11380) | 2024-03-31 | 2025-05-26 중복으로 닫힘 | 약 14개월 |

세 번째 줄이 가장 뼈아프다. 신고 제목이 *"0.110.0: used no longer maintained `passlib` module in test suite"*였다. 문서가 권하던 라이브러리가 프레임워크 자신의 테스트 스위트에도 들어 있었고, 메인테이너가 그 신고를 중복으로 닫기까지 14개월이 걸렸다.

첫 줄도 그냥 지나칠 게 아니다. 공식 템플릿 저장소의 논의(2024-04-29)에 이런 말이 남아 있다.

> "it seems that Python-Jose has been abandoned for a while, and now CVEs have been popping up surrounding it and its dependencies."

취약점이 지적된 라이브러리를 공식 문서가 계속 권했고, 정리에 약 1년이 걸렸다. 이게 이 장에서 가장 중요한 문장이다. **그 기간 내내, 공식 문서를 성실하게 따른 코드가 그 라이브러리를 쓰고 있었다.**

여기서 방향을 잘못 잡기 쉽다. 누가 게을렀다는 이야기가 아니다 — 자원이 한정된 오픈소스에서 이 정도 지연은 흔하다. 이 기록이 말해주는 건 **조립형 스택에서는 부품의 생사를 감시하는 일이 누군가의 상시 업무가 된다**는 것이고, 그 누군가가 프레임워크 팀이 아니라면 결국 당신이다. 부품을 고를 자유에는 지켜볼 의무가 붙어 오는데, 이 의무는 코드로 나타나지 않아 견적에도 잡히지 않는다.

같은 불안을 정확히 말한 발언이 있다. 출처는 밝혀둬야 한다 — FastAPI가 아니라 Django와 비교하는 스레드에서 antoinewdg가 한 말이다.

> "I generally prefer the 'build it yourself' approach, but not for security."

그리고 직접 짜기 싫은 것의 예로 **로그인 시 오래된 해시를 새 알고리즘으로 자동 승격하는 처리**를 들었다.[^10-5] 마이크로 프레임워크에서 보안을 손으로 조립하는 일에 대한 실무자의 불안이고, 위 시간표와 겹쳐 읽힌다.

## 해시와 토큰을 직접 고른다

2026-07 기준으로 공식 문서가 권하는 조합은 무엇인가. 비밀번호는 `pwdlib`, 토큰은 PyJWT다. 문서의 표현은 짧다.

> "The recommended algorithm is 'Argon2'."

설치는 한 줄.

```bash
uv add "pwdlib[argon2]" pyjwt
```

설치는 `pyjwt`, 임포트는 `import jwt`다. 이 어긋남 하나만 기억해두자.

인터넷에 널린 `passlib` + `python-jose` 예제를 그대로 옮기면 방금 본 시간표의 출발점에 다시 서게 된다. 그러니 검색 결과의 코드를 붙여넣기 전에 **그 예제가 쓰는 라이브러리의 마지막 릴리스 날짜를 먼저 보는 습관**을 들이자.

한 가지 예외는 문서가 직접 밝혀뒀다.

> "pwdlib ... does not include legacy algorithms — for working with outdated hashes, it is recommended to use the passlib library."

이미 다른 방식으로 해시가 쌓인 데이터베이스를 넘겨받았다면 `passlib`이 아직 쓰일 곳이 있다. 새 해시를 만드는 도구가 아니라 옛 해시를 읽는 도구로서다. 그 옛 해시를 로그인 시점에 새 알고리즘으로 바꿔 다시 저장하는 코드가 바로 앞 절의 그것, 아무도 짜고 싶어 하지 않는 그 코드다.

`tracker`의 조립은 파일 하나로 끝난다.

> **📐 저자 설계 —** 아래 함수 이름과 토큰 페이로드 구성은 공식 권장이 아니라, 이 책이 `tracker`에서 쓰기로 정한 한 가지 안이다. 라이브러리 호출 표면만 공식 문서를 따랐다.

```python
# src/tracker/security.py
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from tracker.settings import Settings

hasher = PasswordHash.recommended()


def hash_password(raw: str) -> str:
    return hasher.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return hasher.verify(raw, hashed)


def create_access_token(subject: str, settings: Settings) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def read_subject(token: str, settings: Settings) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
    except InvalidTokenError:
        return None
    subject = payload.get("sub")
    return subject if isinstance(subject, str) else None
```

`PasswordHash.recommended()`는 위 축자와 맞물려 읽으면 "지금 시점의 권장 알고리즘을 라이브러리에게 맡긴다"는 뜻이 된다.[^10-1]

토큰 쪽에서 눈여겨볼 것은 인자 이름의 단수와 복수다. 발급은 `algorithm=` 하나를 받고, 검증은 `algorithms=`에 **리스트**를 받는다.[^10-3] 검증 쪽이 목록을 받는다는 건 받아들일 알고리즘을 우리가 지정한다는 뜻이다 — 토큰이 자기 헤더에 적어 온 알고리즘을 그대로 믿지 않는다. 옮겨 적다 한 글자를 흘리기 쉬운 곳이다.

만료 검사는 우리가 짜지 않았는데 어디로 갔을까? `jwt.decode`가 기본적으로 `exp`를 확인하고 지난 토큰이면 예외를 던지는데, 그 예외가 `InvalidTokenError` 아래에 있어 위의 `except` 한 줄에 함께 걸린다.[^10-3]

사용자 쪽에는 컬럼이 하나 붙는다. 6장에서 만든 모델에 해시 컬럼을 더한다.

```python
# src/tracker/models/user.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from tracker.models.base import Base


class User(Base):
    __tablename__ = "users"
    # ...(6장, 생략)

    password_hash: Mapped[str] = mapped_column(String(255))
```

## 로그인 경로, 그리고 4장이 남긴 스텁

토큰을 발급하는 엔드포인트에는 제약이 걸려 있다. OAuth2 패스워드 플로에서 **로그인 요청은 JSON이 아니라 폼**으로 온다.

> "OAuth2 specifies that when using the 'password flow' ... the client/user must send `username` and `password` fields as form data. The spec says that the fields have to be named like that."

3장에서 정한 스키마 규약이 여기만 비껴가는 이유가 그것이다. 필드 이름이 스펙에 박혀 있고 `/docs`의 Authorize 버튼도 그 형식으로 보낸다. 응답 역시 `access_token`과 `token_type` 두 키를 가진 JSON이어야 한다.[^10-1] 우리 앱은 이메일로 로그인하니 `username` 칸에 이메일을 받게 된다. 찜찜하지만 계약을 깨면 Authorize 버튼과 표준 클라이언트가 함께 떨어져 나간다.

```python
# src/tracker/api/auth.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from tracker.deps import SessionDep, SettingsDep
from tracker.repositories.user import UserRepository
from tracker.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def issue_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    settings: SettingsDep,
) -> dict[str, str]:
    user = await UserRepository(session).get_by_email(form_data.username)
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(str(user.id), settings),
        "token_type": "bearer",
    }
```

리포지터리에는 이메일로 찾는 조회가 필요하다.

```python
# src/tracker/repositories/user.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, user_id: int) -> User | None:
        return await self.session.scalar(select(User).where(User.id == user_id))

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))
```

여기서 3장의 에러 계약과 부딪히는 곳이 나온다. 3장은 예외 핸들러를 딱 셋으로 못 박았고 새 예외도 만들지 않기로 했는데, 예외 계층에 401에 해당하는 것이 없다. 그래서 인증 실패만 `HTTPException`으로 둔다. 이 예외는 프레임워크의 기본 핸들러가 처리하니 **네 번째 핸들러를 만든 것은 아니다.** 대신 이 응답 하나만 `ErrorResponse`가 아니라 `{"detail": ...}` 모양으로 나간다 — 3장이 짚어둔 단수 `detail`과 우리 `details`의 차이가 실제로 드러나는 곳이다. 401에 `WWW-Authenticate` 헤더가 스펙상 따라붙어야 해서 감수하는 비용이다.

이제 4장이 `raise NotImplementedError`로 남겨둔 함수를 채울 차례다.

```python
# src/tracker/deps.py
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from tracker.models.user import User
from tracker.repositories.user import UserRepository
from tracker.security import read_subject

# ...(4장, 생략)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
    settings: SettingsDep,
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    subject = read_subject(token, settings)
    if subject is None:
        raise credentials_error
    user = await UserRepository(session).get(int(subject))
    if user is None:
        raise credentials_error
    return user
```

이름과 반환 타입은 4장이 정한 그대로고, 채워진 것은 몸통과 파라미터 셋이다. 그래서 **부르는 쪽 코드는 한 글자도 바뀌지 않는다** — 라우터에 적혀 있던 `CurrentUser` 별칭이 오늘부터 진짜 사용자를 실어 나른다. 스텁을 `NotImplementedError`로 남겨둔 결정도 값을 한다. 그게 조용히 가짜 사용자를 돌려줬다면 이 교체가 무엇을 바꿨는지 아무도 몰랐을 것이다.

`tokenUrl`의 `"auth/token"`은 라우터 접두사와 경로를 이어 붙인 우리 앱의 값이고, 문서 UI가 토큰을 받아오는 주소로 쓰인다. 접두사를 바꾸는 날 함께 바꿔야 한다.

## 인가를 의존성으로 조립하기

인증이 "누구인가"라면 인가는 "그래서 이걸 해도 되는가"다. 선언적 권한 표현에 익숙한 눈으로 보면 이 대목이 가장 허전하다. 메서드 위에 식 하나를 적어두면 프레임워크가 평가해주던 방식이 없다. 대신 무엇이 있는가? 4장에서 본 그 도구, 의존성 함수뿐이다.

검사는 두 층으로 갈린다. 토큰 안의 정보만으로 끝나는 것과 데이터베이스를 봐야 하는 것. 앞쪽은 FastAPI가 표현 수단을 준다. `Security()`로 의존성을 걸며 `scopes=`에 필요한 스코프를 적고, 의존성 안에서 `SecurityScopes`를 파라미터로 받으면 자기와 상위 의존성들이 요구한 스코프 목록(`scopes`)과 그것을 공백으로 이어 붙인 문자열(`scope_str`)을 얻는다.[^10-2] 유용하지만 프레임워크의 몫은 **목록을 모아 건네주는 데까지**다. 비교와 거절은 우리가 쓴다.

뒤쪽, "이 사람이 이 프로젝트의 멤버인가"는 스코프로 표현되지 않는다. 프로젝트마다 답이 다르기 때문이다. 그래서 의존성이 세션을 요구하게 된다. 같은 `deps.py`에 이어 붙인다.

> **📐 저자 설계 —** 아래 팩토리는 FastAPI 공식 권장이 아니라, 리소스 단위 권한을 4장의 의존성 합성으로 표현한 이 책의 한 가지 안이다.

```python
# src/tracker/deps.py
from collections.abc import Awaitable, Callable

from fastapi import Path

from tracker.errors import PermissionDeniedError
from tracker.models.project import ProjectMember, ProjectRole
from tracker.repositories.project import ProjectRepository

ROLE_RANK: dict[ProjectRole, int] = {
    ProjectRole.member: 0,
    ProjectRole.maintainer: 1,
    ProjectRole.owner: 2,
}


def require_project_member(
    role: ProjectRole,
) -> Callable[..., Awaitable[ProjectMember]]:
    async def dependency(
        project_id: Annotated[int, Path()],
        user: CurrentUser,
        session: SessionDep,
    ) -> ProjectMember:
        member = await ProjectRepository(session).get_member(project_id, user.id)
        if member is None or ROLE_RANK[member.role] < ROLE_RANK[role]:
            raise PermissionDeniedError(
                "프로젝트 권한이 없다", code="project.permission_denied"
            )
        return member

    return dependency
```

`ROLE_RANK`는 취향이 아니라 필요다. 6장의 `ProjectRole`은 문자열 값을 가진 열거형이고 **열거형 멤버끼리는 크기를 비교할 수 없다.** `member < owner` 같은 식을 쓰면 실행 중에 터진다. 서열이 필요하면 서열을 따로 적어야 한다.

예외는 새로 만들지 않았다. 3장의 `PermissionDeniedError`를 그대로 던지고 도메인 코드만 좁혀 붙인다. 그러면 응답은 3장의 핸들러를 타고 `ErrorResponse` 모양으로 나가며 `request_id`까지 함께 실린다. **인가 실패가 특별한 응답이 되지 않는 것**, 그게 3장에서 계약을 먼저 정해둔 이유다.

붙이는 쪽은 한 줄이다.

```python
# src/tracker/api/projects.py
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from tracker.deps import SessionDep, require_project_member
from tracker.models.project import ProjectRole
from tracker.schemas.common import Page
from tracker.schemas.issue import IssueRead

router = APIRouter(prefix="/projects", tags=["projects"])
# ...(2장, 생략)


@router.get(
    "/{project_id}/issues",
    response_model=Page[IssueRead],
    dependencies=[Depends(require_project_member(ProjectRole.member))],
)
async def list_project_issues(
    project_id: int,
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[IssueRead]:
    ...
```

리포지터리에도 조회 하나가 더 붙는다.

```python
# src/tracker/repositories/project.py
from sqlalchemy import select

from tracker.models.project import ProjectMember


class ProjectRepository:
    # ...(2·6장, 생략)

    async def get_member(self, project_id: int, user_id: int) -> ProjectMember | None:
        stmt = select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        return await self.session.scalar(stmt)
```

이 배치에는 감춰진 제약이 있다. 의존성이 `project_id`를 경로에서 읽으므로, 경로에 프로젝트가 없는 엔드포인트에는 이 검사를 붙일 수 없다. 이슈를 `/issues/{issue_id}`로 여는 경로라면 먼저 이슈를 읽어 소속 프로젝트를 알아내야 하고, 검사가 조회 뒤로 밀린다. 리소스 단위 권한을 의존성으로 표현하는 순간 **URL 설계가 인가 설계의 일부가 된다.**

그래서 어디까지 흉내 낼 수 있는가? 역할·스코프·소유권 검사까지는 의존성 합성으로 표현된다. 포기하는 것은 **표현식의 자유도**다. 조건이 복잡해지면 그건 코드가 되고, 코드가 되면 테스트를 요구한다. 나쁜 거래는 아니지만, 거래라는 것은 알고 하자.

## 토큰의 수명과 시크릿, 그리고 남은 방어선

2장에서 만든 `Settings`에 세 필드가 붙는다.

```python
# src/tracker/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ...(2장, 생략)

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
```

`jwt_secret_key`에 기본값이 없는 것이 설계다. 값을 주지 않으면 앱이 기동하다 검증에 걸려 죽는다. 시크릿 없이 뜨는 것보다 뜨지 않는 편이 낫고, 덕분에 **시크릿을 코드에 적을 이유가 사라진다.** 환경 변수 이름은 2장의 접두사 규칙을 따라 `TRACKER_JWT_SECRET_KEY`다.

위 기본값은 대칭키 방식이라 서명하는 쪽과 검증하는 쪽이 같은 비밀을 나눠 갖는다. 검증만 하는 서비스가 늘면 그 비밀이 여기저기 복사된다는 뜻이다. 공개키로 검증하게 하려면 RSA·ECDSA 같은 비대칭 알고리즘으로 옮겨야 하고, 그때는 `pyjwt[crypto]`를 설치하라고 문서가 안내한다.[^10-1]

토큰의 근본 성질도 짚어두자. `read_subject`는 서명과 만료만 확인한다. 다르게 말하면 **발급된 토큰은 만료 전까지 되돌릴 수 없다.** 로그아웃을 눌러도, 계정을 정지시켜도 이미 나간 토큰은 자기 수명을 다 산다. 길은 둘뿐이다 — 만료를 짧게 잡고 갱신 절차를 두거나, 회수 목록을 서버에 두고 매 요청 대조하거나. 후자를 고르면 상태를 안 갖는다는 이점이 사라진다. 위의 30분은 그 사이에서 고른 저자의 값이고, 서명 키를 갈아야 할 날에도 같은 산수가 나온다 — 옛 키로 발급된 토큰이 살아 있는 동안은 두 키를 함께 받아야 한다.

마지막으로 프레임워크가 막아주는 것과 우리 몫인 것을 갈라두자. 0.132.0 / 2026-02 기준으로 요청 검사 하나가 기본값이 됐다.

> "Now FastAPI checks, by default, that JSON requests have a `Content-Type` header with a valid JSON value ... and rejects requests that don't."

CSRF 계열 공격 표면 하나를 줄여주는 변경이다. 다만 **줄여주는 것이지 없애주는 것은 아니다.** 인증을 쿠키로 옮기면 CSRF는 다시 우리 문제가 되고, 허용 출처 설정도 어차피 우리가 쓴다. 그리고 오늘 짜지 않은 것들이 남는다 — 오래된 해시의 자동 승격, 로그인 시도 제한, 토큰 회수 목록.

감당할 범위를 정하는 일과 감당 못 한 것을 모르는 일은 전혀 다르다.

오프닝의 세 날짜가 특별한 이유는 거기서 사고가 났기 때문이 아니다. 아무 일도 없어 보이는 채로 몇 년이 지나갔기 때문이다. 당신 프로젝트의 의존성 파일에도 그렇게 조용한 이름이 있을지 모른다 — 인증에 얽힌 이름 옆에 마지막 릴리스 날짜를 적어보는 데는 오 분이면 된다.

---

코드는 오늘 다 썼다. 목록은 내일부터 관리하는 것이다.

[^10-1]: 이 장이 쓴 `fastapi.security`·pwdlib·PyJWT 호출 표면 전부(`OAuth2PasswordBearer(tokenUrl=...)`, `OAuth2PasswordRequestForm`(`.username`·`.password`), 응답 형식과 401의 `WWW-Authenticate`, `PasswordHash.recommended()`·`.hash()`·`.verify(plain, hashed)`, `from jwt.exceptions import InvalidTokenError`)와 인용한 축자 셋, `pyjwt[crypto]` 안내 — FastAPI 공식 문서 *OAuth2 with Password (and hashing), Bearer with JWT tokens*(https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) · *Simple OAuth2*(https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/), 조회 2026-07-26. ⚠️ `tokenUrl`의 `"auth/token"`은 문서 값이 아니라 `tracker`의 값이다.

[^10-2]: `from fastapi import Security`·`from fastapi.security import SecurityScopes`, `Security(dependency, scopes=[...])`, `SecurityScopes`의 속성 `scopes`·`scope_str` — FastAPI 공식 문서 *OAuth2 scopes*, https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/ (조회 2026-07-26)

[^10-3]: `jwt.encode(payload, key, algorithm=…)`·`jwt.decode(jwt, key='', algorithms=None, options=None, ...)`의 인자 이름, `exp`의 기본 검증과 `ExpiredSignatureError`가 `InvalidTokenError` 아래에 있다는 것 — PyJWT 공식 문서 *API Reference*, https://pyjwt.readthedocs.io/en/stable/api.html (조회 2026-07-26). PyJWT 2.13.0 / 2026-05 기준.

[^10-4]: 시간표의 네 스레드(전부 조회 2026-07-25) — fastapi/fastapi Discussion #9587(2023-05-29 → 2024-05-20 PyJWT로 문서 변경) · #11773(2024-06-28 → 2025-09-30 pwdlib 전환 공지) · #11380 *"0.110.0: used no longer maintained `passlib` module in test suite"*(2024-03-31 → 2025-05-26 중복으로 닫힘)은 https://github.com/fastapi/fastapi/discussions/ 아래 각 번호. 인용한 CVE 축자는 fastapi/full-stack-fastapi-template Discussion #1188(SpoonOfDoom, 2024-04-29), https://github.com/fastapi/full-stack-fastapi-template/discussions/1188

[^10-5]: 인용한 antoinewdg의 축자와 "로그인 시 오래된 해시 자동 업그레이드" 언급 — Lobsters, Django vs FastAPI 비교 스레드, https://lobste.rs/s/2jwm1m/django_vs_fastapi_honest_comparison (조회 2026-07-25). **Django와의 비교 맥락에서 나온 말이며 Spring Security 사용자의 전환 경험담이 아니다.**


# 11장. 테스트 — 공식 문서가 `anyio`를 쓰는 이유

FastAPI 공식 문서의 비동기 테스트 페이지에 이런 문장이 있다.

> "By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions."

테스트를 비동기로 돌리면 테스트 함수 안에서 `TestClient`를 쓸 수 없다는 말이다. 그런데 앞 문장이 더 낯설다.

> "AnyIO provides a neat plugin for this"

`pytest-asyncio`가 아니다. anyio다. 비동기 테스트를 붙여봤다면 당신도 십중팔구 `pytest-asyncio`부터 깔았을 텐데, 공식 문서는 다른 쪽을 가리킨다.

## 왜 하필 anyio인가

5장에서 우리는 숫자 하나를 소스까지 따라 내려갔다. `def` 경로 함수가 스레드로 밀려나고, 그 상한 40이 어디 있느냐 물었더니 anyio의 기본 리미터였다. `tracker`는 이미 anyio 위에서 돈다.

여기서부터는 저자의 읽기다. 공식 문서는 anyio 플러그인을 권하면서 **이유를 밝히지 않는다.** 다만 두 사실을 나란히 놓으면 이렇게 읽힌다 — 앱이 선 계층과 테스트가 도는 계층을 같은 물건으로 맞추는 편이 덜 어긋난다. `pytest-asyncio`를 쓰면 앱은 anyio 위에서, 테스트 루프는 다른 라이브러리 손에서 돈다. 대개는 잘 굴러가지만 어긋나는 날의 증상을 알아보기가 어렵다.

쓰는 방법은 간단하다. 비동기 테스트 함수에 마커를 붙이면 된다.[^11-1] 그런데 함정이 있다. 기본 제공되는 `anyio_backend` 픽스처는 **지원하는 모든 백엔드에서 테스트를 돌린다.** 지정하지 않으면 같은 테스트가 asyncio와 trio 양쪽으로 실행되는데, 공식 예제 디렉터리에 `conftest.py`가 없어 문서만 따라가면 만날 일이 없다. 쓰지도 않는 백엔드에서 실패가 난다. 난감한 첫 실패다.

픽스처 하나를 덮어쓰면 막힌다.

```python
# tests/conftest.py
import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
```

덧붙이자. anyio 4.14.2 / 2026-07 기준으로 문서는 `anyio_mode = "auto"` 설정으로 마커를 생략하는 길도 안내하면서, **`pytest-asyncio`의 `auto` 모드와 같이 켜면 충돌한다고 못 박는다.**[^11-1]

`pytest-asyncio` 쪽도 선택지인데 둘은 알고 가자. `asyncio_mode`가 `strict`(기본)냐 `auto`냐로 마커를 붙일지가 갈리고, **1.0.0(2025-05-26)에서 `event_loop` 픽스처가 제거됐다.** 커스텀 `event_loop` 예제는 그 이전 글이다.

## `TestClient`를 못 쓰게 되는 지점

`TestClient`는 동기 클라이언트다. `client.get("/issues/")` 앞에 `await`가 붙지 않으니 비동기 테스트 안에서는 쓸 수 없고, 대신 `AsyncClient`에 ASGI 전송을 물려 앱을 부른다.

그렇다면 `TestClient`는 쓸 데가 없어진 걸까? 오히려 하나는 `TestClient`만 해준다. 컨텍스트 매니저로 쓰면 lifespan 핸들러가 돈다.[^11-2] `AsyncClient`는 반대다 — 공식 문서가 경고 상자에 못 박았다.

> "If your application relies on lifespan events, the `AsyncClient` won't trigger these events."

`tracker`에게 남의 이야기가 아니다. 4장이 lifespan에 `app.state.http_client`를, 7장이 `app.state.redis`를 심었으니 `AsyncClient`로 부르면 그 둘 없이 요청이 든다. 공식 해법은 `asgi-lifespan`의 `LifespanManager`인데, 사실 하나는 병기하자. **그 패키지의 마지막 릴리스는 2.1.0 / 2023-03이고 3년 넘게 새 릴리스가 없다.**

이 장은 셋째 길을 간다. **lifespan이 만들어주던 것을 테스트에서는 의존성 오버라이드로 채운다.** Redis도 외부 HTTP 클라이언트도 테스트가 진짜로 필요한 물건은 아니다. lifespan 자체를 검증하려는 소수의 테스트에만 `TestClient`를 컨텍스트 매니저로 꺼내 쓰면 된다.

## `httpx`라는 이름이 세 층에 걸쳐 있다

하나를 정확히 짚고 가자. 버전을 확인하다 보면 `httpx2`라는 이름을 만나는데, 그걸 "FastAPI가 httpx2로 갈아탔다"로 읽으면 틀린다. 세 층이 각각 다른 이야기를 한다.

첫째 층 — FastAPI의 의존성. 0.140.0 / 2026-07 기준으로 `[standard]` extra가 핀하는 것은 `httpx<1.0.0`, 즉 여전히 구 httpx다. FastAPI 테스트 문서도 설치 명령으로 `uv add httpx`를 안내하고 비동기 예제의 첫 줄은 `from httpx import ASGITransport, AsyncClient`다.[^11-3] 문서와 패키지 메타데이터가 일치한다.

둘째 층 — Starlette의 TestClient. httpx2로 옮겨간 쪽은 여기다. Starlette 공식 문서의 축자는 이렇다.[^11-2]

> "The `TestClient` is built on `httpx2`. Plain `httpx` is still supported, but deprecated - install `httpx2` (included in `starlette[full]`) instead."

셋째 층 — 코드의 실제 모양. `testclient.py`는 `httpx2` 임포트를 시도하고 실패하면 구 httpx를 임포트한 뒤 경고를 띄운다. 그러니까 httpx2는 권장이지 필수가 아니다. 게다가 `as httpx` 별칭을 걸어 안쪽 이름은 그대로 두었다.

둘째와 셋째는 함께 읽어야 한다. 문서는 "deprecated"라고 쓰고 코드는 폴백을 남겼다. 당장 깨지진 않지만 Starlette이 방향을 정했다는 뜻이고, 첫째 층은 아직 따라가지 않았다. **공식 테스트 예제의 `from httpx import ...`와 최신 버전 표의 httpx2는 모순이 아니다. 서로 다른 층의 사실일 뿐이다.**

구 httpx의 마지막 릴리스는 0.28.1 / 2024-12-06으로 1년 7개월째 그대로다. 그래서 `tracker`는 httpx2를 고른다. 실익은 마지막 절에서 본다. 공식 예제를 따르려면 임포트만 `httpx`로 바꾸면 된다 — 이름이 같다.

이 장이 새로 쓰는 것을 넣자.

```bash
uv add --dev pytest anyio "httpx2[ws]"
```

`[ws]`는 장식이 아니다. WebSocket 지원이 이 extra에 묶여 있어, 빼면 마지막 절 임포트가 죽는다.[^11-6]

## 롤백을 비동기로 — 6장이 넘긴 숙제

6장은 테스트 격리 레시피를 인용하면서 선을 그었다. 커넥션을 열고, 트랜잭션을 시작하고, 세션을 `join_transaction_mode="create_savepoint"`로 묶고, 끝나면 바깥 트랜잭션을 롤백한다 — 커밋한 것까지 되돌리는 방식이다. 그런데 문서의 판은 동기 `Session`이고, `AsyncSession` 판은 6장이 뒤진 두 페이지에 없었다(전수 확인은 아니니 거기까지만).

없는 것을 지어내는 대신 소스를 열었다. 확인된 사실은 셋이다.[^11-4] `Session`의 생성자는 `bind`로 엔진 또는 커넥션을 받고, `join_transaction_mode`의 기본값 `conditional_savepoint` 옆에 `create_savepoint`를 문서화한다. `AsyncSession`의 생성자는 `bind`를 첫 인자로 받고 **나머지 키워드를 그대로 안쪽 `Session`에 넘긴다.** `AsyncConnection.begin()`이 돌려주는 `AsyncTransaction`에는 `rollback()`이 있다.

> **📐 저자 설계 —** 공식 문서에 비동기 판 레시피가 없어, 동기 레시피와 각주의 표면 셋으로부터 이 책이 조립했다.

```python
# tests/conftest.py
from typing import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.db import engine


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        db = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield db
        finally:
            await db.close()
            await transaction.rollback()
```

순서가 중요하다. 세션을 먼저 닫고 바깥 트랜잭션을 롤백한다. 반대면 살아 있는 세션이 끝난 트랜잭션 위에서 무언가를 하려 든다.

빈 데이터베이스를 전제로 둘을 보자.

```python
# tests/integration/test_isolation.py
import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.project import Project


@pytest.mark.anyio
async def test_creates_project(session: AsyncSession) -> None:
    session.add(Project(key="TRK", name="Tracker"))
    await session.commit()

    assert await session.scalar(select(func.count()).select_from(Project)) == 1


@pytest.mark.anyio
async def test_starts_empty_again(session: AsyncSession) -> None:
    assert await session.scalar(select(func.count()).select_from(Project)) == 0
```

앞 테스트가 `commit()`을 부르는데도 뒤 테스트는 빈 테이블을 본다. Spring의 `@Transactional` 테스트 롤백이 해주던 일이고, 여기서는 **당신이 그 배선을 직접 들고 있다.** 대신 어디까지 되돌아가는지가 픽스처 열두 줄에 있다.

엔진은 `tracker.db`의 것을 그대로 쓴다. 2장의 `Settings.database_url`을 읽으므로 `TRACKER_DATABASE_URL`만 바꾸면 스위트가 다른 데이터베이스를 본다. 스키마는 6장의 리비전을 `alembic upgrade head`로 올려두자. 스위트가 직접 만들면 편하지만, 그러면 **마이그레이션이 실제로 도는지를 영영 확인하지 못한다.**

진짜 Postgres를 띄우려면 testcontainers(4.15.0 / 2026-07 기준)가 JVM에서 쓰던 그 물건이다. 다만 이 책은 코드를 싣지 않는다. 공식 문서의 예제가 동기 엔진에 psycopg2 URL 하나뿐이라 **비동기 드라이버를 지정하는 형태의 예시가 없기 때문이다.**[^11-5] 확인 못 한 호출 형태를 지어 쓰느니 URL을 환경 변수로 받자.

## 무엇을 갈아 끼우고 무엇을 진짜로 둘 것인가

4장에서 `dependency_overrides`라는 딕셔너리를 소개만 하고 미뤄뒀다. 이제 꺼내자. Spring의 `@MockBean`, NestJS의 `overrideProvider()`에 대응하는데 구조는 훨씬 노골적이다. 컨테이너가 빈을 바꿔치기하는 게 아니라 딕셔너리에 함수 하나를 넣는다.

> **📐 저자 설계 —** 무엇을 갈아 끼우고 무엇을 그대로 둘지는 공식 권장이 아니라 이 책이 정한 경계다.

```python
# tests/conftest.py
from fastapi import FastAPI

from tracker.db import get_session
from tracker.deps import get_event_bus
from tracker.events import InMemoryEventBus
from tracker.main import app


@pytest.fixture
def event_bus() -> InMemoryEventBus:
    return InMemoryEventBus()


@pytest.fixture
async def wired_app(
    session: AsyncSession, event_bus: InMemoryEventBus
) -> AsyncIterator[FastAPI]:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_event_bus] = lambda: event_bus
    yield app
    app.dependency_overrides = {}
```

```python
# tests/conftest.py
from httpx2 import ASGITransport, AsyncClient


@pytest.fixture
async def client(wired_app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=wired_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

임포트 경로를 보자. `get_session`을 `tracker.db`에서 가져왔다. 6장의 `deps.py`가 이 함수를 `db.py`에서 임포트해 `SessionDep`에 넣었으니 `Depends`에 실제로 들어간 객체가 그것이라서다. **오버라이드의 키는 그 함수 객체 자체여야 한다.** 다른 모듈에서 같은 이름을 가져오면 딕셔너리에는 들어가는데 아무것도 바뀌지 않는다 — 조용히 실패하는 종류라 한 시간쯤 날리기 좋다.

마지막 줄 `app.dependency_overrides = {}`도 장식이 아니다. `app`은 모듈 전역이라 오버라이드가 테스트 뒤에도 남는다. 비우지 않으면 **뒤 테스트가 앞 테스트의 가짜 의존성을 물려받는다.**

무엇까지 갈아 끼울까. `tracker`가 바꾸는 것은 둘뿐이다. 세션을 테스트 트랜잭션 안으로 돌리고, 이벤트 버스를 `InMemoryEventBus`로 바꿔 Redis를 걷어낸다. 서비스도 리포지터리도 손대지 않는다. `IssueServiceDep`이 `get_issue_service`를 타고 `SessionDep`을 받으니 **세션 하나만 바꿔도 그 아래가 전부 진짜로 돈다.** 인증 경로를 보는 테스트라면 `get_current_user` 오버라이드가 한 줄 더 붙는다 — 10장이 채운 함수다.

이렇게 세우면 계약 확인이 짧아진다.

```python
# tests/integration/test_issues.py
import pytest
from httpx2 import AsyncClient


@pytest.mark.anyio
async def test_rejects_issue_without_title(client: AsyncClient) -> None:
    response = await client.post("/issues/", json={"project_id": 1})

    assert response.status_code == 422
    assert response.json()["code"] == "request.validation_failed"
```

3장이 정한 에러 계약이 처음 실행되며 검증된다. 422도 `request.validation_failed`도 3장의 약속이고, 지켜지는지 묻는 곳은 테스트다.

## 7장에서 만든 채널을 되찾기

약속한 실익은 여기 있다. httpx2에는 SSE와 WebSocket이 내장돼 있다.[^11-6] 7장에서 연 두 채널을 서드파티 없이 테스트한다는 뜻이다. `client.sse(...)`는 비동기 컨텍스트 매니저를 돌려주고 그 안을 `async for`로 돌면 `ServerSentEvent`가 나온다. WebSocket은 `client.websocket(...)`이고 텍스트·바이트·JSON 송수신 메서드가 달렸다. 서버 없이 ASGI 앱을 부르는 전송도 온다.

> **📐 저자 설계 —** `wait_for_subscriber`는 공식 API가 아니라 아래 경합을 피하려고 이 책이 만든 헬퍼다.

```python
# tests/integration/test_realtime.py
from datetime import datetime, timezone

import anyio
import pytest
from httpx2 import AsyncClient
from httpx2.websockets import ASGIWebSocketTransport

from tracker.events import InMemoryEventBus
from tracker.schemas.common import IssueEvent


async def wait_for_subscriber(bus: InMemoryEventBus, issue_id: int) -> None:
    with anyio.fail_after(1):
        while not bus.queues.get(issue_id):
            await anyio.sleep(0.01)


@pytest.mark.anyio
async def test_status_change_reaches_websocket(wired_app, event_bus) -> None:
    transport = ASGIWebSocketTransport(wired_app)
    async with AsyncClient(transport=transport) as ws_client:
        async with ws_client.websocket("ws://testserver/ws/issues/1") as ws:
            await wait_for_subscriber(event_bus, 1)
            await event_bus.publish(
                IssueEvent(
                    issue_id=1,
                    event_type="status_changed",
                    payload={"status": "resolved"},
                    occurred_at=datetime.now(timezone.utc),
                )
            )
            received = IssueEvent.model_validate(await ws.receive_json())

    assert received.event_type == "status_changed"
```

`wait_for_subscriber`가 왜 필요한지가 이 테스트의 교훈이다. 핸드셰이크가 끝났다고 서버가 구독을 마친 것은 아니다. 7장의 엔드포인트는 `accept()` 직후 이벤트를 밀어내는 태스크를 따로 띄우는데, 그게 큐를 등록하기까지 몇 번의 양보가 필요하다. 그 전에 발행하면 테스트가 **어쩌다 통과하고 어쩌다 실패한다.** 시간이 아니라 상태를 기다리자.

SSE도 모양은 같다. 같은 `wait_for_subscriber` 뒤에 `client.sse(...)`를 열고 `async for`로 첫 `ServerSentEvent`를 받아 `event.data`를 `IssueEvent`로 되돌리면 된다. 7장이 만든 두 채널이 스위트로 들어온다.

---

이 장에서 늘어난 파일은 사실상 `conftest.py` 하나인데, 거기에 지난 아홉 장의 결정이 접혀 들어갔다 — 4장의 오버라이드 딕셔너리, 6장의 트랜잭션 경계, 7장의 인메모리 버스, 3장의 에러 코드, 2장의 설정 필드까지. 스위트의 부속품이라기보다 당신이 내린 설계 결정의 목록에 가깝다.

픽스처를 늘릴 때마다 물어보자. 테스트를 편하게 하려는 것인가, 경계가 잘못 그어졌다는 신호인가.

[^11-1]: `pytest.mark.anyio`, 기본 `anyio_backend` 픽스처가 *"runs everything on all supported backends"*라는 서술, `yield` 비동기 픽스처, `anyio_mode = "auto"`와 `pytest-asyncio` `auto` 모드의 충돌 경고 — AnyIO *Testing with AnyIO*, https://anyio.readthedocs.io/en/stable/testing.html. `fail_after()`가 동기 컨텍스트 매니저라는 서술·`sleep()` — *Timeouts* (조회 2026-07-26)

[^11-2]: 인용한 축자 2건 — Starlette 공식 문서 *TestClient*, https://www.starlette.io/testclient/. `try: import httpx2 as httpx / except ModuleNotFoundError: import httpx` + `StarletteDeprecationWarning` 구조는 starlette 1.3.1 태그 `testclient.py` (조회 2026-07-26)

[^11-3]: `from fastapi.testclient import TestClient`와 설치 안내 `uv add httpx` — FastAPI 공식 문서 *Testing*. 축자 3건과 `from httpx import ASGITransport, AsyncClient` 예제 — 같은 문서 *Async Tests*, https://fastapi.tiangolo.com/tutorial/testing/ (조회 2026-07-26)

[^11-4]: `Session.__init__`의 `bind`·`join_transaction_mode` — SQLAlchemy 2.0 *Session API*, https://docs.sqlalchemy.org/en/20/orm/session_api.html. `AsyncSession.__init__(..., **kw)`가 나머지 키워드를 안쪽 `Session`에 넘긴다는 것, `AsyncConnection.begin() -> AsyncTransaction`과 그 `rollback()`·`AsyncSession.close()`, `await connection.begin()`을 성립시키는 `StartableContext.__await__` — sqlalchemy `rel_2_0_51` 소스 `ext/asyncio/` (조회 2026-07-26)

[^11-5]: `PostgresContainer`·`get_connection_url()`과 *"To get a URL without a driver, pass in `driver=None`."*, 그리고 **그 페이지의 예제가 동기 엔진 + psycopg2 하나뿐이라는 것** — testcontainers-python 공식 문서 *PostgreSQL* 모듈, https://testcontainers-python.readthedocs.io/en/latest/modules/postgres/. *"Version 4.0.0 onwards we do not support the `testcontainers-*` packages"*는 같은 문서 인덱스 Installation 절 (조회 2026-07-26)

[^11-6]: `client.sse(url)`·`client.websocket(url)`이 비동기 컨텍스트 매니저라는 것, `ServerSentEvent`의 `event`·`data`·`id`·`retry`·`json()`, 텍스트·바이트·JSON 송수신 메서드, `from httpx2.websockets import ASGIWebSocketTransport`를 `AsyncClient(transport=…)`에 물리는 예제, WebSocket이 `httpx2[ws]` extra(`wsproto`)에 묶여 있다는 서술 — httpx2 공식 문서 *SSE*·*WebSockets*·*API Reference*, https://httpx2.pydantic.dev/ (조회 2026-07-26)


# 12장. CI/CD — 락파일, 품질 게이트, 그리고 파이프라인

락파일을 두고 우리는 대개 "버전을 고정해두는 파일"이라고 말한다. 노트북과 CI 러너와 컨테이너가 같은 의존성 그래프를 갖게 만드는 장치. 틀린 설명은 아닌데, 여기서는 한 겹이 더 있다. 락파일은 **누가 읽을 수 있는 파일인가**의 문제이기도 하다.

2025년 3월 31일, 파이썬 락파일의 표준이 확정됐다. PEP 751이고, 표준 파일 이름은 `pylock.toml`이며, 상태는 Final이다.[^12-1] 그런데 이 책이 1장부터 쓰고 있는 uv가 만들어내는 파일은 `uv.lock`이고, 그 포맷은 표준이 아니다. uv 문서가 스스로 그렇게 적어둔다.

> "The `uv.lock` format is specific to uv and not usable by other tools"

표준이 확정됐는데 사실상의 표준 도구가 다른 것을 쓴다. `pom.xml` 하나에 익숙한 사람에게는 곧바로 삼켜지지 않는 문장이다. 1장에서 uv를 Maven과 npm의 자리에 놓으며 대응표를 만들 때 락파일 행이 없었던 이유가 이것이다. 미뤄둔 그 한 줄을 여기서 갚는다.

## 표준이 확정되고도 락파일은 둘이다

PEP 751이 잡으려던 것은 *"installation reproducibility"*, 즉 설치 시점에 의존성 해석 없이 같은 결과를 재현하는 일이다.[^12-1] Maven과 npm을 거쳐온 당신에게 새로울 게 없는 구분이고, 새로운 건 그다음이다. `uv.lock`은 표준 포맷이 아니면서 같은 문제를 자기 방식으로 풀어놓았다.[^12-1]

> "a *universal* or *cross-platform* lockfile that captures the packages that would be installed across all possible Python markers"

**universal이라는 단어를 기억해두자.** 이 파일 하나가 가능한 모든 파이썬 마커 조합의 설치 결과를 담는다. 뒤에서 세 버전으로 매트릭스를 돌릴 때 버전마다 락파일을 따로 만들지 않아도 되는 근거다.

그러면 표준은 왜 있는가. 도구가 여럿 살아 있기 때문이다. Poetry도 2.4.1 / 2026-05 기준으로 PEP 621의 `[project]` 섹션으로 옮겼고, pip-tools 역시 죽지 않았다 — uv가 한 일은 대체가 아니라 `uv pip compile`로 인터페이스를 흡수한 것이다. 표준은 그 사이에 공통분모를 만들려는 시도인데, 아직 uv가 합류하지 않았을 뿐이다.

그래서 **당신의 파이프라인은 어떤 도구가 어떤 파일을 읽는지 명시해야 한다.** `tracker`는 uv를 쓰고 `uv.lock`을 커밋한다. 그러면 CI가 그 파일을 진실로 삼는다는 것은 명령어로 어떻게 쓰는가?

## `--locked`와 `--frozen`은 서로 다른 것을 지킨다

락파일을 다루는 uv 플래그는 두 개다. 이름이 비슷한데 지키는 대상이 다르다.[^12-2]

> `--frozen`: "To use the lockfile without checking if it is up-to-date"
> `--locked`: "If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile."

`--locked`는 검사한다. 락파일이 `pyproject.toml`과 어긋나면 에러를 낸다. `--frozen`은 검사하지 않고 락파일에 적힌 버전을 그대로 쓴다. npm 문서가 `npm ci`를 설명하는 문장이 `--locked` 쪽과 거의 같은 모양이다.[^12-2]

> "`npm ci` will exit with an error, instead of updating the package lock"

**`uv sync --locked`가 `npm ci`의 자리에 있다.** 둘 다 "고쳐주지 말고 틀렸다고 말해달라"는 요구이고, CI가 원하는 게 그것이다.

찜찜한 대목이 있다. **두 공식 문서가 서로 다른 플래그를 쓴다.** uv 자신의 Docker 가이드는 `--locked`를, 13장에서 읽을 Uvicorn 공식 Dockerfile은 `--frozen`을 쓴다. uv 문서 어디에도 "프로덕션에서는 `--frozen`을 써라" 같은 권고는 없고, `--frozen`의 이유를 밝힌 곳은 같은 가이드의 워크스페이스 절 하나뿐이다.[^12-2]

> "uv cannot assert that the `uv.lock` file is up-to-date without each of the workspace member `pyproject.toml` files, so we use `--frozen` … to skip the check during the initial sync."

최신성을 검사할 재료가 아직 손에 없을 때 `--frozen`을 쓴다는 뜻이다. 여러 패키지가 한 저장소에 사는 구조가 그렇다. 컨테이너 빌드처럼 파일을 단계적으로 복사해 들어가는 상황에도 같은 이유가 성립한다고 나는 본다.

공식 권고가 없으니 저자 기준으로 고르자. **CI의 의존성 설치는 `--locked`로 간다.** 파이프라인의 존재 이유가 어긋남을 발견하는 것이기 때문이다. `--frozen`은 검사가 불가능한 지점에서만 쓴다. 최악은 둘 중 아무것도 안 붙이는 것이다 — 그러면 `uv run`은 락파일을 갱신하면서 명령을 실행한다.[^12-2] 로컬에서는 편리하고 CI에서는 사고다.

## 마이너 버전이 파괴적 변경을 뜻하는 도구

첫 게이트는 린트와 포맷이고 도구는 ruff다. Checkstyle이나 ESLint를 걸어봤다면 하는 일은 짐작이 갈 것이다. 조심할 것은 규칙이 아니라 **버전 번호**다.[^12-3]

> "Ruff uses a custom versioning scheme that uses the minor version number for breaking changes and the patch version number for bug fixes."

유의적 버저닝에서 `0.16.0` → `0.17.0`은 기능 추가이고 대체로 안전한 이동이다. ruff에서는 그 칸이 **파괴적 변경**을 뜻한다. 2026-07 기준 최신이 0.16.0이니, 언젠가 0.17이 나오는 순간이 곧 규칙 동작이 바뀔 수 있는 지점이다. `>=0.16`처럼 열어두고 돌리다가 아무도 건드리지 않은 코드에서 린트가 깨진다면 원인은 대개 여기다 — 커밋 이력에 범인이 없는 아찔한 실패다.

그래서 핀을 마이너 칸에 건다. `ruff==0.16.*`처럼 버그 수정만 흘러 들어오게 두고, 마이너를 올리는 일은 사람이 의도적으로 하는 작업으로 만든다.

포매터는 스스로를 Black의 *"drop-in replacement"*로 소개하며, Django·Zulip 기준으로 99.9%가 넘는 줄이 동일하게 포맷된다고 밝힌다.[^12-3] 명령은 로컬과 CI가 다르다. 로컬에서는 `ruff check --fix`로 고치지만 CI는 고치는 곳이 아니라 판정하는 곳이라, `ruff format --check`처럼 파일을 쓰지 않는 형태를 쓴다.[^12-3]

## 타입 체커는 이름값 순서로 성숙하지 않았다

두 번째 게이트는 타입 체크이고, 통념이 가장 크게 뒤집히는 곳이다. Astral은 uv와 ruff로 판을 바꾼 팀이니 같은 팀의 `ty`도 비슷하게 성숙했으리라 짐작하기 쉽다. 그런데 버전은 0.0.63이고, README에 이렇게 적혀 있다.[^12-4]

> "ty is currently in beta." / "breaking changes, including changes to diagnostics, may occur between any two versions"

한편 Meta의 `pyrefly`는 이미 1.1.1이다.[^12-4]

> "Pyrefly's current development status is stable."
> "the default type checker for Instagram's 20-million-line Python codebase at Meta"

성숙도가 이름값의 반대로 배열돼 있다. CI 게이트라는 용도만 놓고 보면 자기를 stable이라 선언한 쪽이 걸기 편하고, Pydantic 지원이 내장이라는 점도 이 책의 앱에는 이득이다. `ty`가 쓸모없다는 뜻은 아니다 — FastAPI 소스 `applications.py`에 `# ty: ignore[deprecated]` 주석이 있으니 FastAPI 프로젝트는 실제로 `ty`를 돌리고 있다.[^12-4]

핀 규율은 어느 쪽을 골라도 똑같이 필요하다. pyrefly도 밝힌다 — *"any version may introduce new type errors and other breaking changes."*[^12-4] 성숙도는 역전됐어도 버전 정책의 느슨함은 양쪽이 닮았다. 새 타입 에러가 조용히 흘러 들어오면 어제 통과하던 파이프라인이 오늘 막힌다.

mypy도 2.3.0 / 2026-07 기준으로 메이저가 2.x에 들어섰다. 2.0에서 `--local-partial-types`와 `--strict-bytes`가 기본으로 켜졌으니[^12-4] 넘어가기 전에 변경 목록부터 펴보자. 무엇을 걸든 **게이트는 통과할 수 있을 때에만 게이트다.**

## 파이프라인을 조립한다

먼저 도구를 개발 의존성으로 넣는다.

```bash
uv add --dev ruff pyrefly
```

개발 의존성은 `[dependency-groups]` 테이블(PEP 735)에 들어가고, `dev` 그룹은 `uv sync`에 기본으로 포함된다.[^12-2] 11장에서 테스트 도구를 넣을 때 그룹이 만들어졌으니 두 줄이 늘 뿐이다.

> **📐 저자 설계 —** 아래 상한 표기는 공식 권장이 아니라, 앞 절의 버저닝 사실로부터 이 책이 도출한 핀 전략이다.

```toml
# pyproject.toml
[dependency-groups]
dev = [
    # ...(11장, 생략)
    "ruff==0.16.*",
    "pyrefly>=1.1,<2",
]
```

전문을 보고 줄을 따라 읽자.

> **📐 저자 설계 —** 아래 워크플로는 GitHub이 제공하는 템플릿이 아니라, 이 장에서 확인한 사실들로 이 책이 조립한 것이다.

```yaml
# .github/workflows/ci.yml
name: ci

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

env:
  UV_LOCKED: "1"

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v9
        with:
          enable-cache: true
      - run: uv sync --locked
      - run: uv run ruff check
      - run: uv run ruff format --check
      - run: uv run pyrefly check

  test:
    needs: quality
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v9
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}
      - run: uv sync --locked
      - run: uv run pytest
```

`name`은 목록에 표시될 이름이고 `on`은 언제 도는지를 정한다 — `main`으로의 푸시와 모든 풀 리퀘스트이니 병합 전에 한 번, 병합 후에 한 번이다. `permissions: contents: read`는 이 워크플로의 토큰을 읽기로 좁힌다.

`env`의 `UV_LOCKED`는 앞 절의 `--locked`를 환경 변수로 건 것이다. 이 플래그에는 `UV_LOCKED` 형태가 함께 문서화돼 있고 `uv run`도 같은 옵션을 받는다.[^12-2] `uv sync`에는 눈에 보이게 붙였지만 진짜 값은 `uv run` 세 줄에 있다 — 환경 변수 하나가 그 셋을 함께 덮는다.

첫 잡 `quality`에서 `runs-on`이 러너를 고르고 `steps`가 하는 일을 적는다. `actions/checkout@v7`이 저장소를 받아오고(v7.0.1 / 2026-07 기준), `astral-sh/setup-uv@v9`가 uv를 설치한다(v9.0.0 / 2026-07 기준). 태그는 움직일 수 있는 이름이니 `setup-uv` 문서의 예제처럼 커밋 해시로 핀하는 편이 공급망 관점에서는 낫다. uv 자신의 연동 가이드는 아직 v8.1.0 예제를 싣고 있다.[^12-5]

**여기에 이 장에서 가장 조용한 지뢰가 있다.** 파이썬 프로젝트의 CI라면 `actions/setup-python`을 놓고 `cache:` 입력으로 캐시를 켜는 손이 먼저 나가는데, 그 입력의 설명은 이렇다.[^12-5]

> `cache`: "Used to specify a package manager for caching in the default directory. Supported values: pip, pipenv, poetry."

**목록에 uv가 없다.** uv를 쓰면서 이 입력에 기대면 실패도 경고도 없이 캐시만 안 걸린다 — 파이프라인은 초록불인데 매번 의존성을 처음부터 받아오는 상태가 된다. 그래서 이 워크플로는 uv 캐시를 러너 사이에 실어 나르는 `setup-uv`의 `enable-cache`를 쓴다.[^12-5]

`uv sync --locked`가 락파일대로 환경을 만들고, 그 뒤 세 줄이 게이트다 — `ruff check`가 규칙 위반을, `ruff format --check`가 포맷 어긋남을, `pyrefly check`가 타입을 본다.[^12-3][^12-4] 셋을 한 잡에 몰아넣은 건 파이썬 버전 하나면 충분한 검사여서다. 이어지는 `test` 잡의 `needs: quality`가 순서를 만든다. 린트는 초 단위, 테스트는 분 단위다. 빨리 판정 나는 쪽을 앞에 둔다.

`strategy.matrix`는 같은 잡을 파이썬 버전만 바꿔 여러 번 돌린다. 목록을 3.12·3.13·3.14로 잡은 근거는 이렇다. FastAPI는 3.10 이상을 요구하지만, 이 책을 쓰는 2026-07 기준으로 **3.10은 석 달 뒤인 2026년 10월에 지원이 끝난다.**[^12-5] `fail-fast: false`는 한 버전이 깨져도 나머지를 취소하지 않게 한다 — 3.14에서만 깨지는지가 한 번에 보인다. 버전마다 락파일을 따로 두지 않아도 되는 이유는 앞에서 확인했고, `setup-uv`의 `python-version` 입력에 매트릭스 값을 넘기면 그 버전으로 환경이 잡힌다.[^12-5]

마지막 줄 `uv run pytest`가 11장에서 세운 스위트를 돌린다. pytest 9.x에는 CI와 얽힌 변경이 둘 있다 — `PytestRemovedIn9Warning`이 기본으로 에러가 됐고, `$CI`나 `$BUILD_NUMBER`가 **빈 값이 아니어야** CI로 인식한다.[^12-4]

## 이미지를 굽는 데까지

게이트를 다 통과하면 무엇이 남는가? 산출물이다.

> **📐 저자 설계 —** 아래 잡은 이미지를 **밀지 않고 굽기만 한다.** 어디로 밀지는 13장의 결정이기 때문이다.

```yaml
# .github/workflows/ci.yml — 위 워크플로에 잡 하나를 더 붙인다
  image:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: docker/setup-buildx-action@v4
      - uses: docker/build-push-action@v7
        with:
          context: .
          push: false
          tags: tracker:${{ github.sha }}
```

`image` 잡은 `needs: test`로 테스트 뒤에 놓았다. `setup-buildx-action`이 빌드 엔진을 준비하고 `build-push-action`이 굽는다(각각 v4.2.0·v7.3.0 / 2026-07 기준).[^12-6] `context: .`는 저장소 루트를 빌드 컨텍스트로 삼고, `tags`의 `${{ github.sha }}`는 이미지가 어느 커밋에서 나왔는지를 이름에 박는다. 그리고 `push: false`가 이 잡의 성격을 정한다 — **임무는 산출물을 남기는 것이 아니라, 이미지가 안 구워지는 상황을 배포 전에 드러내는 것이다.**

**이 잡이 부르는 `Dockerfile`은 아직 없다.** 그 파일은 13장에서 쓴다. 이미지에 무엇을 넣고 프로세스를 몇 개 띄울지가 전부 배포 결정이라, 섞으면 둘 다 흐려진다. 여기서 정한 것은 그 파일을 언제 부르는가까지다. 밀어 넣을 곳이 정해지면 로그인 스텝이 붙고 `push: false`가 뒤집힐 뿐, 뼈대는 그대로다.

---

파이프라인을 다 짰지만 이 장에서 가져갈 것은 워크플로 파일이 아니다. **복사한 파이프라인은 각 줄이 무엇을 막는지 모르는 채 도는 순간부터 장식이 된다.** 게이트를 세우며 확인한 것은 결국 셋이었다 — 락파일에는 아직 하나의 표준이 없고, 버전 번호가 뜻하는 바는 도구마다 다르며, 이름값과 성숙도는 나란히 가지 않는다.

새 도구를 얹기 전에 당신이 펴볼 곳은 그 도구 README의 **버전 정책 문단**이다.

[^12-1]: PEP 751(Final, 2025-03-31, `pylock.toml`) — https://peps.python.org/pep-0751/ · `uv.lock` — https://docs.astral.sh/uv/concepts/projects/layout/ (조회 2026-07-25)

[^12-2]: `--locked`·`--frozen` 축자 — https://docs.astral.sh/uv/concepts/projects/sync/ · `uv run`의 동일 옵션·`UV_LOCKED` — https://docs.astral.sh/uv/reference/cli/ · 워크스페이스 절 — https://docs.astral.sh/uv/guides/integration/docker/ · `[dependency-groups]`·`uv add --dev` — https://docs.astral.sh/uv/concepts/projects/dependencies/ · `npm ci` — https://docs.npmjs.com/cli/v11/commands/npm-ci (조회 2026-07-26)

[^12-3]: ruff 버저닝·포매터·`ruff format --check`·`ruff check --fix` — https://docs.astral.sh/ruff/formatter/ , https://docs.astral.sh/ruff/linter/ (조회 2026-07-26)

[^12-4]: `ty` — https://github.com/astral-sh/ty · pyrefly·`pyrefly check` — https://pyrefly.org/en/docs/installation/ · mypy 2.0 — https://github.com/python/mypy/blob/master/CHANGELOG.md · pytest 9.0 — https://docs.pytest.org/en/stable/changelog.html · `# ty: ignore[deprecated]` — fastapi 0.140.0 태그 `fastapi/applications.py` (조회 2026-07-26)

[^12-5]: `setup-uv` v9.0.0·`enable-cache`·`python-version`·해시 핀 — https://github.com/astral-sh/setup-uv · `setup-python`의 `cache` — https://github.com/actions/setup-python · `checkout` v7.0.1 — https://github.com/actions/checkout/releases · v8.1.0 예제 — https://docs.astral.sh/uv/guides/integration/github/ · 3.10 EOL — https://devguide.python.org/versions/ · 워크플로 구문 — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax (조회 2026-07-26)

[^12-6]: `build-push-action` v7.3.0의 `context`·`push`·`tags`, `setup-buildx-action` v4.2.0 — https://github.com/docker/build-push-action , https://github.com/docker/setup-buildx-action/releases (조회 2026-07-26)


# 13장. 컨테이너와 클라우드 — 어디에, 몇 개의 프로세스로 올릴 것인가

파이프라인이 초록불이라고 해보자. 12장의 워크플로가 린트와 타입과 테스트를 지나 이미지를 구웠고, 그걸 어딘가에 올렸다. 그런데 트래픽이 조금 늘자 응답이 밀리기 시작한다.

스프링에서 왔다면 손이 어디로 갈지 안다 — 요청 처리 스레드 수를 확인하고 모자라면 올린다. Node였다면 프로세스 수부터 봤을 것이다.

여기서는 그 두 질문이 겹쳐 있고, 답이 여러 파일에 흩어져 있다. 5장의 두 층은 7장에서 알림이 절반만 도착하는 모습으로, 8장에서 리포트가 네 번 생성되는 모습으로 돌아왔고, 그때마다 "그 숫자는 13장의 몫"이라며 미뤄뒀다. 갚을 차례다.

## 이미지 안에 무엇이 들어가는가

Uvicorn 공식 문서에는 uv 기반 Dockerfile이 통째로 실려 있고, 전략이 한 문장으로 적혀 있다.[^13-1]

> "The key strategy is to install dependencies first, then copy the project files."

의존성을 먼저, 소스는 나중에. Maven·npm에서 익숙한 순서이고, 자주 바뀌는 쪽이 뒤에 와야 캐시가 산다. 그런데 **이 예시를 그대로 베끼면 두 곳에서 물린다.**

하나는 사용자다. 같은 문서가 *"For production, create a non-root user!"*라고 경고해두고도 예시 Dockerfile에는 `USER` 지시어가 없다.[^13-1] 비루트 처방은 uv 문서가 모범 사례로 링크하는 예제 저장소에 있다.[^13-2]

둘은 베이스 이미지다. 예시는 `python:3.12-slim`으로 태그를 박아뒀는데, 공식 `python` 이미지의 기본 배포판은 그사이 Debian trixie 세대로 옮겨간 듯하다 — `3.13-slim-trixie`와 `3.13-slim`이 같은 시각에 갱신돼 있었고 구 `-bookworm` 태그도 살아 있다. 다이제스트가 아니라 태그 목록을 조회 시점에 읽은 것이다. 그 API는 현재 값을 돌려주니 당신이 여는 날엔 다를 수 있다.[^13-2] 그러니 **접미사 없는 태그를 믿지 말자.** 배포판까지 적어두면 베이스가 바뀌는 날도 우리가 고른 날이 된다.

> **📐 저자 설계 —** 아래 Dockerfile은 공식 예시가 아니라, 위 두 함정을 메우고 단계를 나눈 이 책의 구성이다.

```dockerfile
# Dockerfile
FROM python:3.13-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM python:3.13-slim-trixie

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
CMD ["uvicorn", "tracker.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

`COPY --from=ghcr.io/astral-sh/uv:latest`가 uv 실행 파일만 꺼내 오고, 세 환경 변수는 uv 문서가 컨테이너용으로 안내하는 것들이다 — 바이트코드를 미리 컴파일하고, 마운트된 캐시라 복사를 쓰고, 개발 의존성은 뺀다.[^13-2]

`RUN`에 붙은 마운트가 핵심이다. 캐시 마운트는 uv 캐시를 빌드 사이에 살려두고, 바인드 마운트는 두 파일을 복사하지 않은 채 빌려 쓰니, 이 레이어는 락파일이 바뀔 때만 다시 돈다. `--no-install-project`가 의존성만 설치하고 프로젝트는 두 번째 `uv sync`가 맡는다. `--locked`는 12장의 결정을 이었다 — 공식 Uvicorn Dockerfile은 `--frozen`을 쓰지만 uv 자신의 예제와 가이드는 `--locked`다.[^13-2]

두 번째 `FROM`이 런타임 이미지를 연다. 빌더의 `/app`을 가져오고 가상 환경 경로를 `PATH` 앞에 놓되 uv 자신은 넘어오지 않는다 — 단계를 나눈 이유다. 마지막 `CMD`에는 워커 수 플래그가 없다.

## Alpine과 slim, 절반만 맞는 이야기

베이스를 고를 때 반드시 나오는 말이 있다. "Alpine은 musl을 쓰니까 wheel을 못 받아서 소스 빌드가 돌고, 그래서 느리다." **출처를 따라가면 반쯤 어긋난 설명이다.** 공식 `python` 이미지 README의 alpine 문단은 wheel이 아니라 런타임을 말한다.[^13-3]

> "it does use musl libc instead of glibc and friends, so software will often run into issues"

"소스 빌드가 실패한다"는 문장은 slim 문단에 있고 원인은 컴파일러 부재다 — 두 경고가 뭉쳐진 것이다.[^13-3]

musl용 wheel의 표준도 이미 있다. PEP 656이 musllinux 태그를 정의했고 2021년 Final이 됐다. 배포량은 PyPI 파일 목록의 태그를 집계하면 나온다 — 2026-07-25 조회 기준 pydantic-core 21개, uvloop 16개, httptools 14개, orjson 20개이고, uvloop과 httptools는 manylinux와 개수가 같다.[^13-3]

권고는 "Alpine을 쓰지 마라"가 아니다. 기본은 `-slim`으로 가되, Alpine이면 의존성 전체의 musllinux wheel을 확인하자. 남는 위험은 wheel이 아니라 musl과 glibc의 런타임 차이다.

## 컨테이너 하나에 프로세스를 몇 개 띄울 것인가

미뤄둔 숫자다. 답을 찾으러 공식 문서를 열면 **두 곳이 다른 말을 한다.**

FastAPI 배포 문서는 워커를 늘리는 방법으로 `fastapi run --workers 4 main.py`를 보여준 뒤, 컨테이너로 넘어가면 방향을 바꾼다.[^13-4]

> "when running on Kubernetes you will probably not want to use workers and instead run a single Uvicorn process per container"

이 문서에는 gunicorn이라는 단어가 **아예 나오지 않는다.** 한편 Uvicorn 자신의 배포 문서는 일반 규칙을 이렇게 연다.[^13-4]

> "As a general rule, you probably want to: ... Run `gunicorn -k uvicorn.workers.UvicornWorker` for production."

같은 페이지 아래쪽에는 `uvicorn.workers`가 폐기 예정이니 `uvicorn-worker`를 쓰라는 경고가 있고, 실제로 `uvicorn/workers.py`는 임포트하는 순간 `DeprecationWarning`을 던진다.[^13-4]

어느 쪽이 옳은지 판정하지는 않겠다. **판정보다 중요한 것은 이 불일치가 존재한다는 사실 자체다** — 인터넷에 남은 `gunicorn -k UvicornWorker` 예제가 전부 낡은 것도 아니라는 뜻이다.

Uvicorn 문서는 gunicorn 경유 시의 기능 손실도 밝혀뒀다.[^13-4]

> "some options such as `--limit-concurrency` are not yet supported when running with Gunicorn"

5장에서 문 앞의 손잡이라고 부른 그 플래그다. **gunicorn을 앞에 세우면 그 손잡이가 사라진다.**

— 여기서부터는 **저자 기준**이다. 이 책은 컨테이너 안에 프로세스를 하나만 둔다. 배포 문서가 그렇게 권하고, Uvicorn 공식 Dockerfile도 워커 하나짜리이며 개수는 *"let your orchestration system manage the number of deployed containers"*라고 오케스트레이터에 맡긴다.[^13-1] 무엇보다 gunicorn 경로는 5장의 backpressure를 잃는다. 앞 절의 `CMD`에 `--workers`가 없던 이유다. 컨테이너 밖이라면 `fastapi run --workers 4 main.py` 쪽이 맞다 — 늘릴 주체가 우리뿐이니까. **워커 수를 정하는 것은 CPU 개수가 아니라 그 프로세스를 누가 세는가**다. `--workers`가 `$WEB_CONCURRENCY`를 읽는다는 것이[^13-4] 2장이 워커 수를 `Settings`에 넣지 않은 이유다 — `TRACKER_` 접두사가 안 붙는 이름이라 설정으로 끌고 오면 진실이 두 군데 생긴다.

레플리카는 몇 개일까. 5장의 두 층이 산수가 된다. 프로세스 하나에 동기 스레드 40개, 6장에서 풀을 5+10으로 잡았으니 프로세스당 커넥션 최대 15개. 레플리카가 12개면 데이터베이스가 보는 커넥션은 180개다. **레플리카 수를 정하는 일은 곱셈**이고, 곱해지는 쪽이 우리 것이 아닐 때가 많다.

7장이 남긴 문제도 여기서 답이 난다. WebSocket 연결은 그것을 받은 프로세스에만 붙어 있어서, 레플리카가 여럿이면 알림이 절반만 도착한다. 길은 둘이다. 앞단이 같은 클라이언트를 늘 같은 파드로 보내게 하거나 — `.spec.sessionAffinity`를 `ClientIP`로 두는 설정이 있고 기본값은 `None`이다[^13-6] — 7장에서 만든 팬아웃을 쓰거나. **어피니티는 연결을 고정하고, 팬아웃은 고정할 필요를 없앤다.** 파드는 언제든 교체되니 이 책은 후자다.

## 프록시 뒤에서 잃어버리는 주소

컨테이너는 앞단 뒤에 선다. 그러면 클라이언트 주소는 프록시의 것이 되고 HTTPS 요청도 앱에게는 HTTP로 보인다. 해법은 프록시가 심어준 헤더를 믿는 것인데, 범위가 좁다. uvicorn이 다루는 헤더는 `X-Forwarded-For`와 `X-Forwarded-Proto` 둘뿐이고, `--proxy-headers`는 기본으로 켜져 있지만 `--forwarded-allow-ips` 기본값이 `127.0.0.1`이다.[^13-5] 다른 노드의 인그레스가 심은 헤더는 그래서 무시되고, 손쉬운 값을 넣게 된다. **FastAPI 프록시 문서의 예시부터가 `--forwarded-allow-ips="*"`를 쓴다.**[^13-5] 그 옆에 경고가 붙어 있다.

> "Only trust clients you can actually trust! Incorrectly trusting other clients can lead to malicious actors spoofing their apparent client address"

`*`는 아무나 헤더를 지어내도 믿겠다는 선언이다. 클라이언트 주소로 접근을 제한하거나 감사 로그를 남긴다면 그 값이 요청자가 적어 보낸 값이 된다. 아찔한 조합이다. 프록시가 기존 헤더를 지우고 자기 것만 심는다는 걸 확인했을 때만 쓰자.

1장에서 `root_path`를 서블릿 컨텍스트 경로가 놓이던 자리로 짚었다. 서브패스 뒤에 앱을 두는 배포가 그 자리다 — 프록시가 `/api`를 떼고 넘기면 앱은 자기가 어디 걸려 있는지 모른 채 문서와 링크를 만든다.

## 살아 있는 것과 받을 준비가 된 것

쿠버네티스는 두 가지를 따로 묻는다. 살아 있는가, 지금 트래픽을 받을 수 있는가. 공식 문서의 처방은 이 둘을 나누라는 것이다.[^13-6]

> "The liveness probe passes when the app itself is healthy, but the readiness probe additionally checks that each required back-end service is available."

liveness가 실패하면 컨테이너가 재시작되고, readiness가 실패하면 그 파드 주소가 서비스 엔드포인트에서 빠진다. 결과가 다르니 같은 판정을 쓰면 곤란하다 — 데이터베이스가 흔들릴 때 readiness가 빠지는 건 옳지만, 같은 이유로 앱을 재시작하면 나빠지기만 한다.

**스프링의 헬스 엔드포인트에 익숙하다면 당신 손이 여기서 허공을 짚는다.** 대응하는 기성품이 없어서 둘로 나누는 일까지 우리가 만든다.

> **📐 저자 설계 —** 두 엔드포인트의 판정 내용과 배치는 이 책이 정한 것이지 프레임워크의 규약이 아니다.

```python
# src/tracker/api/health.py
from fastapi import APIRouter
from sqlalchemy import text

from tracker.deps import SessionDep

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(session: SessionDep) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ready"}
```

```python
# src/tracker/main.py
from tracker.api.health import router as health_router

app.include_router(router=health_router)
```

1장에서 `main.py`에 달았던 `/healthz`가 여기로 옮겨왔고 경로는 그대로다 — 바꾸면 매니페스트와 문서가 어긋난다. 이 엔드포인트는 의존성을 받지 않아서 프로세스가 응답을 만든다는 것 외에는 아무것도 주장하지 않는다. `/ready`는 6장의 `SessionDep`으로 질의를 한 번 던지고,[^13-6] 실패하면 예외가 3장의 핸들러를 타고 5xx로 나가 준비되지 않았다는 신호가 된다.

기본값은 `periodSeconds` 10초, `timeoutSeconds` 1초, `failureThreshold` 3이고 `httpGet`은 200 이상 400 미만이면 성공이다.[^13-6]

> **📐 저자 설계 —** 매니페스트 골격은 쿠버네티스 공식 예제를 따르고, 숫자와 배치는 이 장이 정했다.

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tracker
  labels:
    app: tracker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tracker
  template:
    metadata:
      labels:
        app: tracker
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: tracker
        image: tracker:latest
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          periodSeconds: 10
          failureThreshold: 6
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 10
          failureThreshold: 3
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]
```

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: tracker
spec:
  selector:
    app: tracker
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

liveness의 `failureThreshold`를 readiness보다 크게 뒀다 — 재시작은 되돌릴 수 없으니 더 확실할 때 판정하자는 것이다. `image`의 `latest`는 임시 이름이고, 12장의 잡이 커밋 해시로 붙인 태그가 들어온다. 그 잡의 `push: false`가 뒤집히고 로그인 스텝이 붙는 것이 12장에 돌려주는 변경이다. 설정은 2장이 정한 `TRACKER_` 환경 변수로 들어온다. 서비스의 `port` 80은 들어오는 쪽이고 `targetPort` 8080이 컨테이너 쪽이라, 둘이 같을 필요는 없다.[^13-6]

## 끝내는 데도 순서가 있다

배포는 새 파드를 띄우면서 옛 파드를 죽이는 일이고, 후자가 훨씬 자주 사고를 낸다.

종료 절차는 이렇다. kubelet이 주 프로세스에 `SIGTERM`을 보내고 유예 시간이 끝나면 `KILL`을 보낸다. `preStop` 훅이 있으면 그 전에 실행하며, `terminationGracePeriodSeconds`의 기본값은 30초다.[^13-7] 흔히 도는 설명을 하나 고쳐두자. "SIGTERM이 먼저 오고 엔드포인트 제거는 나중이라 순서가 보장되지 않는다"는 말이 있는데, **현재 문서의 서술은 그렇지 않다.** 두 과정은 병렬이다.[^13-7]

> "At the same time as the kubelet is starting graceful shutdown of the Pod, the control plane evaluates whether to remove that shutting-down Pod from EndpointSlice objects"

종료 중인 엔드포인트도 즉시 사라지지 않고 `ready`가 `false`로 남는다.[^13-7] 그럼 `preStop`의 `sleep`은 근거가 없을까? 두 과정이 동시에 진행되니 갱신을 아직 전달받지 못한 로드밸런서나 클라이언트가 있을 수 있다. 몇 초를 쉬는 건 그 전파를 기다리는 시간이지, 순서가 뒤집힐까 봐 드는 보험이 아니다.

8장이 넘긴 요구 조건을 갚자. 그 장은 **백그라운드 태스크의 최악 실행 시간보다 종료 유예 시간이 길어야 한다**고 적고 숫자를 미뤘다. 사슬은 이렇다 — `preStop`이 몇 초 쉬고, uvicorn이 남은 응답과 백그라운드 태스크를 마저 처리하고,[^13-7] lifespan의 `yield` 이후 코드가 자원을 닫는다. 이 전부가 유예 시간 안에 끝나야 `KILL`을 맞지 않는다. **`terminationGracePeriodSeconds` > `preStop` 대기 + uvicorn의 `--timeout-graceful-shutdown`**, 그래서 위 매니페스트가 30초 대신 60초를 썼다. 주간 리포트가 그 창에 못 들어온다면 유예를 늘릴 문제가 아니라, 8장 말대로 그 일을 요청 밖으로 내보낼 문제다.

**uvicorn `--timeout-graceful-shutdown`의 기본값은 문서에 표기돼 있지 않다**(0.51.0 / 2026-07 기준). 오른쪽을 모르면 왼쪽을 정할 수 없으니, 이 값은 비워두지 말고 명시적으로 주자.

레플리카는 고정값 셋이다. 오토스케일러를 붙인다면 성질 하나는 알고 붙이자 — HPA는 **늘릴 때는 즉시, 줄일 때는 기본 5분을 기다린다.**[^13-6] 방금 계산한 종료 시퀀스가 그 5분 안에서 반복된다.


## 서버리스는 한 단어가 아니다

어디에 올릴 것인가. 여기서 **5장의 결론이 한 번 뒤집힌다.**

AWS Lambda 문서는 실행 모델을 이렇게 적어둔다.[^13-8]

> "For each concurrent request, Lambda provisions a separate instance of your execution environment."
> "this execution environment is busy and cannot process other requests."

공식 동시성 식도 `Concurrency = (average requests per second) * (average request duration in seconds)`로 요청 수와 처리 시간만 쓴다. Cloud Run은 정반대다. 인스턴스 하나가 동시에 받는 요청 수의 기본값이 "80 times the number of vCPUs"이고 최대 1,000이다.[^13-8]

— 여기서부터는 **저자 추론**이다. 벤더가 이렇게 말한 게 아니라 위 사실에서 끌어낸 결론이다. Lambda에서는 `async def`가 처리량을 늘려주지 않는다. 환경 하나가 한 요청만 붙들고 있으니 겹칠 기회가 없다. `async`의 이득은 한 요청 안에서 여러 I/O를 겹칠 때만 남는다. Cloud Run은 반대다. 인스턴스 하나가 80개를 받으니, I/O를 겹칠 수 있으면 같은 인스턴스가 더 많이 처리하고 그것이 곧 인스턴스 수와 비용이다.

그러니 **"FastAPI를 서버리스에 올린다"를 한 문장으로 묶으면 안 된다.** 5장에서 `def`와 `async def`를 고를 때 깔려 있던 전제 — 한 프로세스가 여러 요청을 동시에 들고 있다 — 가 Lambda에서는 성립하지 않는다.

기동과 종료도 다르다. Cloud Run은 `PORT`를 주입하고 `0.0.0.0` 바인딩을 요구하며 기본 8080이라 앞의 Dockerfile이 그대로 붙지만, **`SIGTERM` 후 10초 뒤에 `SIGKILL`이다.**[^13-8] 쿠버네티스 기본 30초를 전제로 짠 정리 코드가 여기서는 잘린다 — 부등식은 플랫폼마다 다시 풀어야 한다.

Lambda에 올리는 길은 둘이다. Mangum은 앱을 감싸 핸들러로 만드는 라이브러리이고, AWS 공식인 Lambda Web Adapter(v1.0.1 / 2026-05 기준)는 확장 바이너리라 코드를 고치지 않는다 — 위에서 구운 이미지를 그대로 올린다. Mangum은 아카이브되지 않았지만 최근 커밋이 대부분 의존성 범프와 문서 수정이라 **유지보수 모드**가 정확하다.[^13-8]

PaaS 계약도 보자. Fly.io는 `fly.toml`의 `internal_port`가 기본 8080, Render는 `PORT`에 기본 10000이고, 나머지 계약은 확인하지 못했으니 단정하지 않는다. Railway 공식 가이드는 uvicorn이 아니라 Hypercorn을 쓴다 — **uvicorn은 HTTP/1.1만 지원한다.**[^13-9] HTTP/2가 필요하면 Granian(2.7.9 / 2026-07)이나 Hypercorn(0.18.0 / 2025-11)이고, HTTP/3는 Hypercorn뿐인데 `[h3]` extra에 "current draft"로 적혀 있다. Hypercorn은 릴리스가 여덟 달 넘게 없다.[^13-9]

둘만 밝혀두자. gunicorn은 26.0.0 / 2026-05 기준으로 메이저가 뛰었고 파괴적 변경이 실제로 있다 — `eventlet` 워커가 제거됐고 C 확장이 CPython에서 필수가 됐다.[^13-9] `uvicorn-worker` 경로는 앞의 것을 비껴가지만, 올릴 때는 체인지로그를 펴보자. lifespan이 워커마다 도는지는 4장에서 밝혔듯 확인하지 못했다 — 워커를 늘리는 순간 기동 코드가 몇 번 도는지가 문제가 된다.

---

이 장에서 만든 건 Dockerfile 하나와 매니페스트 둘이다. 그런데 그 셋이 정한 것은 **경계의 개수**다. 프로세스 하나에 스레드 40개, 파드 하나에 프로세스 하나, 서비스 하나에 파드 셋. 5장의 두 층이 곱셈이 되어 커넥션 수와 유예 시간과 요금으로 나타났다.

플랫폼이 바뀌어도 읽어낼 것은 두 숫자다. **인스턴스 하나에 요청을 몇 개까지 넣는가, 그리고 죽일 때 몇 초를 주는가.** 앞의 숫자가 당신 앱의 동시성 모델이 쓸모 있는지를 정하고, 뒤의 숫자가 정리 코드가 끝까지 도는지를 정한다.

앱은 이제 어딘가에서 돌고 있다. 그리고 그 앱에 대해 우리가 아는 것은, 프로브가 200을 돌려준다는 사실 하나뿐이다.

[^13-1]: Uvicorn 공식 문서 Deployment: Dockerfile (예시 전문·세 축자) — https://github.com/Kludex/uvicorn/blob/main/docs/deployment/docker.md (조회 2026-07-25)

[^13-2]: 멀티스테이지·`slim-trixie`·`UV_*`·`--locked`·`--no-install-project` — https://docs.astral.sh/uv/guides/integration/docker/ · 비루트 사용자와 `PATH` — https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile · 태그 갱신 시각 — https://hub.docker.com/v2/repositories/library/python/tags (조회 2026-07-26)

[^13-3]: alpine·slim 문단 — https://github.com/docker-library/docs/blob/master/python/README.md · PEP 656 (Final, 2021) — https://peps.python.org/pep-0656/ · wheel 개수는 PyPI JSON API 파일 태그 집계 (조회 2026-07-25)

[^13-4]: K8s 축자·`--workers` — https://fastapi.tiangolo.com/deployment/server-workers/ · gunicorn 규칙·`uvicorn-worker`·`--limit-concurrency`·`$WEB_CONCURRENCY` — https://uvicorn.dev/deployment/ 와 소스 `workers.py` (조회 2026-07-25)

[^13-5]: 헤더 2종·`--forwarded-allow-ips` 기본값·경고 축자 — https://uvicorn.dev/settings/ · `"*"` 예시 — https://fastapi.tiangolo.com/advanced/behind-a-proxy/ (조회 2026-07-25)

[^13-6]: probe 축자·기본값 https://kubernetes.io/docs/concepts/workloads/pods/probes/ · HPA 축소 안정화 5분 — https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/ · 매니페스트 골격(`content/en/examples/` YAML 4종)과 `.spec.sessionAffinity`(`virtual-ips.md` 원문) — https://github.com/kubernetes/website · `text` — https://docs.sqlalchemy.org/en/20/core/sqlelement.html (조회 2026-07-26)

[^13-7]: 종료 시퀀스·`preStop`·30초·병렬 축자 — kubernetes/website 저장소 `content/en/docs/concepts/workloads/pods/pod-lifecycle.md` 원문, https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ · 백그라운드 태스크 대기 — https://uvicorn.dev/server-behavior/ (조회 2026-07-25)

[^13-8]: 실행 환경 축자·동시성 식 — https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html · `PORT`·10초·80×vCPU — https://docs.cloud.google.com/run/docs/container-contract · LWA·Mangum — 각 GitHub 저장소 (조회 2026-07-25)

[^13-9]: 대안 서버 Granian https://github.com/emmett-framework/granian · Hypercorn https://github.com/pgjones/hypercorn (2026-07-25) · Fly.io — https://fly.io/docs/reference/configuration/ · Render — https://render.com/docs/deploy-fastapi · Railway — https://docs.railway.com/guides/fastapi · gunicorn 26.0.0(2026-05-05) — https://github.com/benoitc/gunicorn/blob/master/docs/content/2026-news.md (조회 2026-07-26)


# 14장. 숫자를 믿는 법 — 관측성, 성능, 그리고 이 도구와 함께 살아가기

13장에서 구운 이미지가 올라갔고 `/healthz`와 `/ready`가 나란히 초록불이다. 프로브 통과는 프로세스가 살아 있고 의존 서비스에 손이 닿는다는 뜻이지, 이 앱이 **잘** 돌고 있다는 뜻은 아니다. 그건 무엇으로 아는가. 그리고 누군가 "FastAPI를 쓰니 성능은 걱정 없죠"라고 할 때 그 말은 어떻게 받는가.

실마리는 뜻밖의 곳에 있다. FastAPI 공식 문서의 벤치마크 페이지다.

> "The same way that Starlette uses Uvicorn and cannot be faster than it, FastAPI uses Starlette, so it cannot be faster than it."[^14-5]

자기가 아래층보다 빠를 수 없다고 스스로 적어둔 것이다. 이 장은 그 문장을 진지하게 받아들이는 데서 출발한다.

## 접근 로그만 딴 소리를 한다

로그를 JSON 한 줄씩으로 통일하려면 포매터를 정하고, 루트 로거에 핸들러를 걸고, 앱을 띄운다. 그러면 우리 로그는 JSON으로 나오는데 **접근 로그만 여전히 uvicorn 자체 포맷으로 찍힌다.** 수집기에 파싱되는 줄과 안 되는 줄이 섞여 드니 찜찜하다.

흔한 설명은 "uvicorn이 기존 로거를 비활성화해서"인데 맞지 않는다. 기본 설정의 `disable_existing_loggers`는 `False`다. 원인은 옆 줄에 있다. `uvicorn`과 `uvicorn.access`에 `propagate: False`가 걸려 있어 루트에 무엇을 붙이든 이 둘의 기록이 올라오지 않는다.[^14-1] 배선은 두 로거의 핸들러를 걷어내고 전파를 되살리는 데서 시작한다.

> **📐 저자 설계 —** 아래 구성은 FastAPI가 주는 것이 아니라 위에서 확인한 uvicorn 기본 설정에 맞춰 이 책이 정한 것이다.

```python
# src/tracker/observability.py
import logging

import structlog
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import make_asgi_app

from tracker.settings import Settings


def configure_logging(settings: Settings) -> None:
    logging.basicConfig(format="%(message)s", level=settings.log_level)
    for name in ("uvicorn", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


def setup_observability(app: FastAPI, settings: Settings) -> None:
    configure_logging(settings)
    app.mount("/metrics", make_asgi_app())
    log = structlog.get_logger().bind(service=settings.otel_service_name)
    if settings.otel_exporter_endpoint is None:
        log.info("observability.tracing_disabled")
        return
    FastAPIInstrumentor.instrument_app(app)
    log.info("observability.tracing_enabled", endpoint=settings.otel_exporter_endpoint)
```

2장에서 `Settings`에 넣어둔 `log_level`이 이제야 소비된다. 프로세서 목록은 위에서 아래로 흐르고 마지막 하나가 출력 형태를 정한다. 첫 자리의 `merge_contextvars`는 다음 절의 주제다.[^14-2] 덧붙이면 "`disable_existing_loggers`를 빠뜨리면 로거가 죽는다"는 흔한 설명은 **연역**일 뿐이라 이 책은 싣지 않는다.

## 요청 ID가 스레드를 건너지 못한다

4장의 `RequestIdMiddleware`는 요청마다 ID를 만들어 `request.state`에 심고 응답 헤더로 돌려줬다. 3장의 `ErrorResponse`가 그 값을 담았고 이제 로그도 달아야 한다. 요청 하나가 남긴 로그 스무 줄을 한 묶음으로 되찾는 열쇠다. 자바 쪽 진단 컨텍스트의 일을 파이썬에서는 `contextvars`가 한다.

```python
# src/tracker/middleware.py
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from structlog.contextvars import bind_contextvars, clear_contextvars


class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, header_name: str = "X-Request-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request, call_next):
        request_id = request.headers.get(self.header_name) or uuid4().hex
        request.state.request_id = request_id
        clear_contextvars()
        bind_contextvars(request_id=request_id)
        response = await call_next(request)
        response.headers[self.header_name] = request_id
        return response
```

두 줄이 늘었다. 요청이 들어올 때 컨텍스트를 비우고 ID를 묶으면 첫 자리의 `merge_contextvars`가 로그마다 그 묶음을 합친다. `structlog.get_logger()`로 로거를 얻어 `log.info("issue.created", issue_id=issue.id)`처럼 쓰면 요청 ID는 넘기지 않아도 붙는다.[^14-2]

그런데 함정이 있고, 놀랍게도 5장의 그 함정이다. structlog 공식 문서가 FastAPI를 이름으로 지목해 경고한다.

> "This can be a problem in hybrid applications like those based on Starlette (this includes FastAPI) where **context variables set in a synchronous context don't appear in logs from an async context and vice versa.**"[^14-2]

`def`로 선언한 경로 함수는 스레드풀에서 돌고 `async def`는 이벤트 루프에서 돈다는 규칙이, 여기서는 **로그에서 요청 ID가 사라지는 형태로** 다시 나타난다. 색깔을 잘못 칠하면 성능이 아니라 진단 능력을 잃는 셈이다. 두 종류의 경로가 섞인 앱이라면 ID가 실제로 붙는지 눈으로 확인하는 편이 낫다. Starlette 쪽에서 컨텍스트 전파를 보장한다고 적어둔 문서는 찾지 못했다.

## 안정된 1.x 위에 얹힌 베타 0.x

로그 다음은 트레이스와 메트릭이다. OpenTelemetry 파이썬 구현은 2026-07 기준으로 트레이스와 메트릭이 Stable, 로그가 Development다. 그런데 버전 번호에서 눈이 멈춘다. `opentelemetry-api`·`opentelemetry-sdk`는 1.44.0인데 계측 패키지 `opentelemetry-instrumentation-fastapi`는 0.65b0, 즉 **베타 표기**다. 같은 날(2026-07-16) 나왔는데 체계가 다르다.[^14-3] 안정된 코어에 베타 계측이 얹힌 모양이라 두 묶음에 같은 핀 규칙을 걸 수 없다.

`setup_observability`가 그래서 단순하다. 내보내기 주소가 없으면 계측을 걸지 않고, 있으면 `instrument_app` 한 줄로 붙인다. 익스포터와 리소스를 조립하는 SDK 코드는 싣지 않았다 — 1차 소스로 확인한 표면이 거기까지라서다. 대신 이름과 주소를 `Settings`의 두 필드로 모아 세 신호가 서로 다른 이름을 갖는 일을 막았다. 배선은 `main.py`에서 한 줄이다.

```python
# src/tracker/main.py
from tracker.observability import setup_observability
from tracker.settings import get_settings

# ...(13장, 생략)

setup_observability(app, get_settings())
```

메트릭 쪽에는 프로세스 모델이 튀어나온다.

> "Prometheus client libraries presume a threaded model, where metrics are shared across workers. **This doesn't work so well for languages such as Python** where it's common to have processes rather than threads to handle large workloads."[^14-4]

워커가 여럿이면 카운터가 프로세스마다 따로 자란다. 멀티프로세스 모드가 있으나 대가가 크다. `PROMETHEUS_MULTIPROC_DIR`을 기동 셸에서 잡아 재시작 전에 비워야 하고, 커스텀 컬렉터가 동작하지 않고, Info와 Enum 메트릭은 못 쓴다.[^14-4] 위 코드의 `/metrics`는 **워커가 하나라는 전제** 위에 서 있다. 13장의 권장 — 컨테이너당 프로세스 하나, 확장은 레플리카로 — 을 따르면 이 문제가 생기지 않는다. 5장에서 시작한 "경계는 프로세스다"의 마지막 얼굴이다. 2장에서 줄줄이 깨진 것도 메트릭 수집기였다 — 관측 스택은 앱 바깥처럼 보이지만 업그레이드에서 먼저 다친다.

## Actuator가 없다는 말의 정확한 크기

스프링에서 온 당신이 묻는다. 의존성 하나로 헬스·정보·메트릭 엔드포인트가 한꺼번에 생기던 그 물건은 없느냐고. 없다. FastAPI 저장소에 인접한 요청이 하나 있는데(타이밍 데이터를 노출해달라는 이슈 #9148) 확인 시점 upvote는 18이다.[^14-7] 이 부재를 커뮤니티가 어떻게 느끼는지는 근거를 못 찾았으니 여론이 아니라 구조만 대조하자.

크기를 재보자. 13장의 `/healthz`와 `/ready`가 헬스와 준비성을, 앞 절의 `/metrics`가 메트릭을 덮는다. 남는 것은 빌드·버전 정보와 의존별 상태 정도다. **직접 만들 것은 엔드포인트 서너 개 분량**이지 프레임워크 하나 분량이 아니다. 대신 규약이 없다는 비용이 붙는다 — 팀마다 경로와 응답 모양이 다르다. 얻는 것도 있다. 자동으로 붙는 진단 엔드포인트가 없다는 건 실수로 열려 있는 것도 없다는 뜻이다 — 저자의 판단이다.

## "빠르다"는 문장의 출처를 따라가면

출처는 대개 공식 문서다. *"on par with NodeJS and Go"*, 그리고 개발 속도가 *"about 200% to 300%"* 오르고 오류가 *"about 40%"* 준다는 두 줄. 눈여겨볼 것은 뒤의 두 줄에 별표가 달렸고 그 각주가 *"estimation based on tests conducted by an internal development team"*이라고 밝힌다는 점이다.[^14-5] 자체 추정이라고 문서가 먼저 말한다. 조건을 지우고 숫자만 옮기는 쪽은 문서가 아니라 인용하는 우리다.

성능 주장의 근거는 TechEmpower 벤치마크 링크다. 그 위키에는 만든 사람들이 자기 방법론의 한계를 길게 적어뒀다. 로그를 끈 채로 잰다는 것(*"not consistent with production deployments"*), 리버스 프록시를 쓰지 않는다는 것, 측정 구간이 15초이고 부하 생성기가 `Wrk`이라는 것. 그리고 이 한 줄이 있다.

> "nothing beats conducting performance tests yourself for the specific workload of your application."[^14-6]

결과를 만든 쪽이 직접 재보라고 말한다. 이 책은 FastAPI가 링크한 실행이 어느 라운드의 언제 측정인지 확인하지 못했다. 그래서 순위도 배수도 옮기지 않는다. **조건이 적히지 않은 숫자는 자기 상황으로 옮길 수도, 반박할 수도 없다.**

## 옆 분야에서 빌려온 규율

정직하게 밝히자. 이 책이 뒤진 학술 문헌 가운데 **FastAPI 자체의 성능을 다룬 동료 심사 논문은 나오지 않았다.** ASGI도, Pydantic의 직렬화도, asyncio의 실증 연구도 마찬가지다. 웹 프레임워크 벤치마크의 방법론을 검토한 논문도 없었고, free-threading이 처리량을 얼마나 바꾸는지도 5장에서 이월된 채 비어 있다. 그러니 아래 문헌은 전부 옆 분야의 것이고, 빌려올 것은 수치가 아니라 규율이다.

첫째, 측정 편향. Mytkowicz 등의 「Producing Wrong Data Without Doing Anything Obviously Wrong!」(ASPLOS 2009)은 프로그램 로직과 무관한 두 가지만 건드린다. 쓰이지도 않는 환경 변수의 총 바이트 수, 그리고 링크 순서. 논문이 만든 합성 예제 프로그램에서는 환경 변수 크기 하나만 바꿔도 성능이 흔히 33%, 한 번은 거의 300% 움직였다. 실제 벤치마크 스위트(SPEC)에서는 폭이 확 줄어든다 — 링크 순서가 평균 2%(Core 2)·8%(Pentium 4), 환경 변수 크기가 평균 1%·4%다. **이 폭의 차이 자체가 조건을 보라는 증거다.** 요점은 편향의 크기가 아니라 편향이 있다는 사실이고, 링크 순서 편향을 요약하며 저자들이 쓴 한 줄이 이렇다 — *"think we have a 7% slowdown when in fact we have a 8% speedup!"* 조사 대상은 최상위 학회 논문 133편이었다.[^14-7]

둘째, 통계. Georges 등의 「Statistically Rigorous Java Performance Evaluation」(OOPSLA 2007)은 자바 성능 논문 50편의 방법론을 조사했다. 50편 중 16편은 방법론을 아예 적지 않았고, 밝힌 논문 중에서는 **여러 번 기동해 그중 가장 좋았던 실행 하나를 싣는 방식**이 10편으로 가장 많았다(평균값은 8편). 그렇게 얻은 결론이 오도되는 비율은 최대 16%, 일부 방법론에서는 결론이 뒤집히는 비율도 3%를 넘었다. JMH로 워밍업과 씨름해본 사람에게 남의 이야기로 들리지 않을 것이다. 논문은 같은 논점이 관리형 런타임 위의 다른 언어에도 적용된다고 적어두었다.[^14-7] CPython도 그중 하나다.

셋째, 목록. van der Kouwe 등의 「SoK: Benchmarking Flaws in Systems Security」(IEEE EuroS&P 2019)는 반복되는 결함을 22가지로 정리하고, 최상위 학회 논문 50편에서 한 편이 평균 다섯 가지를 저지르며 **결함이 없는 것은 한 편**이었다고 보고했다. 널리 인용되는 "benchmarking crimes"는 같은 연구의 비심사 프리프린트 제목이고 정본은 "flaws"로 순화했다.[^14-7]

그 태도를 이 책도 취한다. 저자들은 손가락질할 뜻이 아니며 문제는 분야 전체에 있다고 적었다. 마찬가지로 **TechEmpower가 이 결함들을 저질렀다고 말하려는 것이 아니다.** 이 렌즈를 끼면 숫자를 만났을 때 던질 질문이 생긴다. 무엇을 재고 무엇을 안 쟀는가. 비교 대상도 같은 정도로 튜닝됐는가. 표준편차가 있는가, 아니면 좋았던 실행 하나인가. 하드웨어·버전·워커 수가 적혀 있는가.

꼬리 지연에는 단서가 더 붙는다. 닫힌 루프 부하 생성기는 서버가 느려지면 자기도 함께 느려져 가장 느린 구간의 요청을 놓친다. coordinated omission이라 부르며, `Wrk`이나 Locust의 p99를 낙관적으로 만든다. 그런데 이 개념의 원전은 강연과 메일링 리스트 글이며 동료 심사를 거치지 않았다. 5장에서 쓴 Little's Law는 학술지에 증명이 실린 정리이고, 그 옆에 인용되는 USL은 프리프린트와 저서가 원전이다.[^14-7]

## 이 도구와 함께 살아가기

1장은 2026년 2월부터 6월까지의 세 건으로 이 책을 열었다. 창을 넓혀 **2025년 12월부터 2026년 7월까지**를 한 표에 놓으면 이렇게 보인다.[^14-8]

| 버전 | 날짜 | 무엇이 바뀌었나 |
|---|---|---|
| 0.125.0 | 2025-12-17 | Python 3.8 지원 중단 |
| 0.128.0 | 2025-12-27 | `pydantic.v1` 지원 완전 제거 |
| 0.129.0 | 2026-02-12 | Python 3.9 지원 중단 |
| 0.132.0 | 2026-02-23 | `strict_content_type` 기본 True |
| 0.135.0 | 2026-03-01 | SSE 정식 지원 |
| 0.137.0 | 2026-06-14 | 라우터 내부 구조를 트리로 변경 |
| 0.140.0 | 2026-07-24 | 의존성 메모리 사용량 감소 |

일곱 달 남짓 사이에 인터프리터 지원선이 두 번 올라갔고, 호환 계층 하나가 사라졌고, 기본 동작이 엄격해졌다. 1장에서 본 세 건은 이 흐름의 뒷부분이었다. 다만 한쪽으로만 읽으면 부정확해진다. **나쁜 쪽은 분명하다** — 마이너 번호 하나가 생태계를 깨고, 고쳐진 뒤 3주 만에 또 깨지는 일이 있었다(2장). **좋은 쪽도 같은 표에 있다.** 별도 라이브러리로 메워오던 SSE가 코어로 들어왔다(0.135.0). 표 밖에서는 4장에서 본 `Depends(scope=)`가 그런 종류의 움직임이다 — 다만 그것이 오래된 이슈를 해결한 것인지는 4장에서 밝힌 대로 확인하지 못했다. 빠르게 흡수하는 성질과 자주 깨는 성질은 앞뒷면이다.

1장에서 미뤄둔 질문을 꺼내자. **0.x에 머무는 이 프레임워크를 프로덕션에 써도 되는가.**

사실부터 놓자. 아래층 Starlette은 2026-03-22에 1.0.0을 냈고 지금 1.3.1인데 위층 FastAPI는 0.140.0이다. 성숙도 표기가 뒤집혀 있다. 저장소 지표는 2026-07-25 기준 스타 100,866개, 열린 이슈 87개, MIT다. 창시자는 2025-05-05에 회사 설립과 FastAPI Cloud를 알렸다. 0.x 유지나 상업화에 대한 찬반 여론은 근거를 확보하지 못해 옮기지 않는다. 대안은 존재와 버전만 적자 — Litestar 2.24.0(2026-06)·Django Ninja 1.6.2(2026-03)·Flask 3.1.3(2026-02).[^14-8] 다만 이 책이 읽은 대안 논의는 상당수가 "Litestar를 보라"는 글의 댓글 스레드에서 나왔다. **떠나는 사람이 과대표집된 표본**이다.

이제 판단이다. **버전 번호가 낮다는 것은 코드가 미숙하다는 뜻이 아니라 호환성 약속의 등급이 낮다는 뜻이다.** 1장에서 그렇게 적었고 위 표가 뒷받침한다. 0.x라서 깨지는 것이 아니라, **깨는 대신 빨리 움직이기로 한 프로젝트가 그 선택을 버전 번호로 정직하게 표기하는 것**에 가깝다. 그러니 "0.x라 불안하다"는 문장은 다시 써야 한다. 진짜 질문은 이것이다 — **당신 팀에 마이너 릴리스 노트를 읽을 사람과 시간이 있는가.** 있다면 이 도구는 감당된다. 없다면 버전 번호가 1.0이든 5.0이든 언젠가 같은 자리에서 다친다.

처방은 정책 쪽이다. 자동 업그레이드를 무인으로 돌리지 말 것, 마이너 업그레이드도 12장의 파이프라인에 태워 통합 테스트로 받아낼 것, 그리고 관측·계측 라이브러리를 업그레이드 체크리스트의 첫 줄에 둘 것.

---

이 책은 ASGI 명세가 7년째 그대로라는 사실과 그 위층이 자주 흔들린다는 사실을 나란히 놓고 시작했다. 그 대비 위에서 한 일은 세 무더기를 나누는 것이었다. 그대로 옮겨온 것, 옮겨왔지만 매년 다시 확인해야 하는 것, 그리고 옮겨올 자리가 없는 것.

세 번째 무더기의 목록을 이제 당신에게 넘긴다. 의존성을 스스로 찾아 꽂아주는 컨테이너, 애너테이션 하나로 걸리던 트랜잭션 경계, 필터 체인으로 조립돼 있던 보안, 의존성 하나로 따라오던 진단 엔드포인트, 표준 문제 상세 형식의 코어 지원. 못 찾은 게 아니라 **지금 이 도구에 없는 것**이고, 없다는 사실을 아는 편이 있다고 착각하는 것보다 안전하다.

숫자도 마찬가지다. 이 장에서 얻은 것은 어떤 프레임워크가 얼마나 빠른가가 아니라, 빠르다는 문장을 만났을 때 **무엇이 측정됐고 무엇이 측정되지 않았는지**를 묻는 습관이다. 그 습관은 당신이 다음에 어떤 도구로 옮겨가든 그대로 쓸 수 있다. 이 책에서 가장 오래 갈 물건이 있다면 그것일 것이다.

[^14-1]: 로거 3종·`disable_existing_loggers: False`·`propagate: False` — Uvicorn *Concepts: Logging*, https://github.com/Kludex/uvicorn/blob/main/docs/concepts/logging.md (조회 2026-07-25). 0.51.0 / 2026-07 기준.

[^14-2]: 이 장이 쓴 structlog 호출 표면 전부와 인용 축자 — structlog 공식 문서, https://www.structlog.org/en/stable/contextvars.html 외 (조회 2026-07-26). 26.1.0 기준.

[^14-3]: 안정성 상태표 — https://opentelemetry.io/docs/languages/python/ · 1.44.0과 0.65b0(둘 다 2026-07-16) — PyPI JSON API · `instrument_app`과 import 경로 — https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html (조회 2026-07-26).

[^14-4]: 축자와 멀티프로세스 제약, `make_asgi_app` — prometheus_client 공식 문서, https://prometheus.github.io/client_python/multiprocess/ (조회 2026-07-26). `app.mount(...)`는 9장 각주에서 확인했다.

[^14-5]: 인용 축자 둘 — https://fastapi.tiangolo.com/benchmarks/ · FastAPI 문서 원문 `docs/en/docs/index.md`, https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md (조회 2026-07-25).

[^14-6]: 방법론 조건과 축자 — TechEmpower FrameworkBenchmarks Wiki, https://github.com/TechEmpower/FrameworkBenchmarks/wiki (조회 2026-07-25). ⚠️ 라운드·시점은 확인하지 못했다.

[^14-7]: Mytkowicz 외(ASPLOS 2009, DOI 10.1145/1508244.1508275)·Georges 외(OOPSLA 2007, DOI 10.1145/1297027.1297033)·van der Kouwe 외(IEEE EuroS&P 2019, DOI 10.1109/EUROSP.2019.00031) — 수치와 축자는 원문 확인. "benchmarking crimes"는 비심사 프리프린트(arXiv:1801.02381) 제목 · coordinated omission의 원전은 비심사 강연 · Little(1961)은 *Operations Research* 게재, USL은 프리프린트·저서 · #9148 upvote 18(원문 확인, 2026-07-25).

[^14-8]: 표의 버전·날짜는 릴리스 노트 헤더 기준 · 저장소 지표는 GitHub API · FastAPI Cloud 발표 — https://x.com/tiangolo/status/1919410655922176040 · 대안 3종 버전 — PyPI JSON API (조회 2026-07-25).


---

## 맺음말

열네 개 장을 지나오며 `tracker`는 `main.py` 한 파일에서 시작해 라우터와 서비스와 리포지터리를 갖추고, 데이터베이스와 실시간 채널과 큐를 붙이고, 인증을 조립하고, 테스트와 파이프라인을 얻고, 컨테이너에 담겨 올라갔다.

그런데 이 책이 정말로 남기려 한 것은 그 코드가 아니다. 코드는 낡는다. 이 책이 인용한 버전들도 낡는다. 남는 것은 **판단의 기준**이다. 어떤 문장을 믿을 것인가. 어떤 숫자에 조건을 물을 것인가. 확인된 것과 확인되지 않은 것을 어떻게 갈라 적을 것인가.

FastAPI를 쓰는 일은 프레임워크가 정해주지 않는 경계를 계속 우리 손으로 긋는 일이다. 그 자유가 이 도구의 매력이자 비용이다. 경계를 그을 때마다 이 책이 던진 질문들이 다시 쓰이길 바란다.

## 참고문헌

이 책의 모든 구체적 주장은 본문 각주 **일흔여덟 개**에 1차 소스와 조회 시점이 붙어 있다. 항목별 출처는 각주를 보라. 아래는 이 책이 근거로 삼은 소스의 계열을 정리한 것이다. **모든 조회는 2026년 7월에 이루어졌다.**

### 공식 문서·명세

- **FastAPI 공식 문서** — https://fastapi.tiangolo.com/ (튜토리얼·고급 가이드·배포 문서)
- **Starlette 공식 문서** — https://www.starlette.io/ · 저장소 https://github.com/Kludex/starlette
- **Pydantic 공식 문서** — https://pydantic.dev/docs/
- **Uvicorn 공식 문서** — https://uvicorn.dev/
- **AnyIO 공식 문서** — https://anyio.readthedocs.io/
- **SQLAlchemy 2.0 공식 문서** — https://docs.sqlalchemy.org/en/20/ · **Alembic** — https://alembic.sqlalchemy.org/
- **uv 공식 문서** — https://docs.astral.sh/uv/
- **ASGI 명세** — https://asgi.readthedocs.io/en/latest/specs/main.html
- **Python 공식 문서·PEP** — https://peps.python.org/ · https://devguide.python.org/
- **Kubernetes 공식 문서** — https://kubernetes.io/ (본문 인용은 `kubernetes/website` 저장소 원문 마크다운 기준)
- **httpx** — https://www.python-httpx.org/ · **httpx2** — https://httpx2.pydantic.dev/
- **pytest** — https://docs.pytest.org/ · **PyJWT** — https://pyjwt.readthedocs.io/
- **OpenTelemetry** — https://opentelemetry.io/ · **structlog** — https://www.structlog.org/ · **Prometheus Python 클라이언트** — https://prometheus.github.io/client_python/
- **GitHub Actions 문서** — https://docs.github.com/actions · **npm 문서** — https://docs.npmjs.com/
- **Spring Framework 레퍼런스** — https://docs.spring.io/ · **Jakarta EE 튜토리얼** — https://jakarta.ee/learn/
- **RFC 9457 (Problem Details for HTTP APIs)** — https://www.rfc-editor.org/

### 저장소·릴리스 기록

- **fastapi/fastapi** 릴리스 노트·이슈·디스커션 — https://github.com/fastapi/fastapi
- **fastapi/full-stack-fastapi-template** 디스커션
- **Kludex/starlette**, **encode/uvicorn**, **benoitc/gunicorn**, **trallnag/prometheus-fastapi-instrumentator**, **astral-sh/uv-docker-example**
- **PyPI JSON API**(패키지 버전·업로드 시각) — https://pypi.org/ · **Docker Hub Tags API** — https://hub.docker.com/

### 학술 문헌

- Mytkowicz, T., Diwan, A., Hauswirth, M., Sweeney, P. F. (2009). *Producing Wrong Data Without Doing Anything Obviously Wrong!* ASPLOS 2009. DOI: `10.1145/1508244.1508275`
- Georges, A., Buytaert, D., Eeckhout, L. (2007). *Statistically Rigorous Java Performance Evaluation.* OOPSLA 2007. DOI: `10.1145/1297027.1297033`
- van der Kouwe, E. 외 (2019). *SoK: Benchmarking Flaws in Systems Security.* IEEE EuroS&P 2019. DOI: `10.1109/EUROSP.2019.00031`
- Adya, A., Howell, J., Theimer, M., Bolosky, W. J., Douceur, J. R. (2002). *Cooperative Task Management without Manual Stack Management.* USENIX ATC 2002.

### 실무자 논의

Hacker News 스레드, discuss.python.org 제안 스레드(가상 스레드 도입 논의), Lobsters 비교 스레드, 그리고 국내 개발자 기록 일부. **이 책은 Reddit과 Stack Overflow를 인용하지 않는다** — 자료 수집 단계에서 두 플랫폼에 접근하지 못했고, 확보하지 못한 출처를 인용한 것처럼 쓰지 않기 위해서다.

## 판권

**이미 웹을 아는 개발자를 위한 FastAPI**
*Spring Boot·Express에서 건너온 사람들의 실전 안내서*

| | |
|---|---|
| 지은이 | Toby-AI |
| 판본 | 1.0.0 (초판) |
| 발행일 | 2026년 7월 26일 |
| 언어 | 한국어 |
| 분류 | 기술서 (tech-book) |
| 식별자 | `urn:uuid:` (EPUB 메타데이터 참조) |

### 기준 시점

이 책의 모든 버전 번호·수치·API 서술은 **2026년 7월을 기준**으로 한다. FastAPI는 이 책을 쓰는 시점에 **한 달에 서너 번에서 다섯 번** 릴리스되고 있었고, 본문이 인용한 판본은 **FastAPI 0.140.0 / 2026-07-24**다. 시간이 지날수록 구체적인 버전 서술은 낡는다. 본문이 버전과 날짜를 함께 적어둔 것은 독자가 **무엇이 낡았는지 스스로 판정할 수 있게** 하기 위해서다. 각 주장의 1차 출처는 각주에 있으니, 의심스러운 대목은 원문을 직접 열어보길 권한다.

### 라이선스

이 책은 **크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 4.0 국제 라이선스(CC BY-NC-SA 4.0)**로 배포된다.

- **저작자 표시(BY)** — 원저작자를 표시해야 한다.
- **비영리(NC)** — 상업적 목적으로 이용할 수 없다.
- **동일조건 변경허락(SA)** — 2차적 저작물에는 동일한 라이선스를 적용해야 한다.

라이선스 전문: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko

본문에 인용된 문서·코드·논문의 저작권은 각 저작권자에게 있으며, 인용은 출처 표시와 함께 이루어졌다.

### 제작

이 책은 **book-writer 하네스 v1.9.1**로 저술되었다. 리서치·저술 계획·계획 리뷰·챕터 저술·문체 검수·사실 검증·통권 수락 검수·EPUB 빌드의 각 단계를 전문 에이전트가 나누어 수행했다.

집필 과정에서 사실 검증은 **다섯 차례**에 걸쳐 이루어졌고, 그 판정 기록은 저술 로그에 남아 있다. 코드 예제에 등장하는 모든 import 경로·클래스·함수·파라미터 이름은 공개된 1차 소스와 대조했다. 다만 **이 책의 제작 과정에는 코드를 실제로 실행하거나 컴파일하는 단계가 없었다.** 예제를 따라 할 때 문제를 발견하면 각주의 원문을 함께 확인해 주기 바란다.
