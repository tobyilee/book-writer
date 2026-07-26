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
