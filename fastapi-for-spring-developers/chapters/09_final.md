<!-- 개정: 2026-05-16 라운드 1 가디언 피드백 반영 (Critical 1: 다섯 핸들러 함수명 `handle_*` prefix로 통일, Should 2·3: 인용블록 → 평어체, 9행 메타 미세 다듬기) -->

# 9장. 예외·로깅·관측성 — Actuator 없이

새벽 두 시에 알람이 울린다고 해보자. 주문 API의 5xx 비율이 한 시간 사이 1%에서 7%로 튀었다. 머릿속에서 가장 먼저 떠오르는 그림은 — Spring 환경이라면 — *Actuator*다. `/actuator/metrics`로 가서 응답 시간 분포를 본다. `/actuator/health`로 의존성 상태를 본다. 그라파나 대시보드를 열면 *어느 엔드포인트*가 어떤 *예외*로 떨어지는지가 한눈에 들어온다. `@ControllerAdvice`로 잡힌 모든 예외가 SLF4J MDC의 `requestId`와 함께 정확히 한 줄로 기록돼 있다. 손에 익은 흐름이다.

이제 같은 상황을 FastAPI로 겪는다고 해보자. `/actuator/metrics`는 없다. `@ControllerAdvice`도 없다. SLF4J MDC도 없다. Spring Boot Admin도 자동으로 떠 있지 않다. *알람이 울렸는데*, 어디부터 봐야 할지가 살짝 난감하다. 1장에서 약속한 "Spring Actuator 한 줄의 빈자리"가 가장 무겁게 느껴지는 순간이다.

핵심 질문은 둘이다. **`@ControllerAdvice`의 전역 핸들러를 FastAPI에선 어떻게 구성하는가?** 그리고 **`spring-boot-starter-actuator` 한 줄의 마법을 무엇으로 대체하는가?** 둘 다 *없는 자리*에 *우리 손*을 넣는 회로의 문제다. 6장에서 익힌 통주저음을 그대로 들고 가자 — *자동의 자리에 명시가 들어선다.*

도메인은 *주문 API*로 잡자. 사용자가 `/orders`에 POST 요청을 보내면 주문이 생성되고, 실패할 수 있는 모드는 다섯 가지다 — 주문이 없거나(`OrderNotFound`), 재고가 부족하거나(`InsufficientStock`), 결제가 거절되거나(`PaymentDeclined`), 멱등성 키가 충돌하거나(`IdempotencyConflict`), 요청이 너무 잦거나(`RateLimitExceeded`). 한 도메인 안에서 다섯 모드를 *예외 → 핸들러 → 로그 → 메트릭 → 헬스*까지 점진적으로 쌓아 올린다. 한 발 한 발 함께 가보자.

## `@app.exception_handler` — `@ControllerAdvice`와 거의 1:1

먼저 가장 익숙한 자리부터. Spring의 `@ControllerAdvice` + `@ExceptionHandler` 조합은 FastAPI의 `@app.exception_handler` 데코레이터와 *거의 1:1*로 매핑된다. 옆에 놓고 보자.

**Spring (Kotlin):**

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(OrderNotFoundException::class)
    fun handleOrderNotFound(e: OrderNotFoundException): ResponseEntity<ErrorResponse> {
        return ResponseEntity.status(404).body(
            ErrorResponse(code = "ORDER_NOT_FOUND", message = e.message)
        )
    }
}
```

**FastAPI:**

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class OrderNotFound(Exception):
    def __init__(self, order_id: int) -> None:
        self.order_id = order_id

@app.exception_handler(OrderNotFound)
async def handle_order_not_found(_: Request, exc: OrderNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": "ORDER_NOT_FOUND", "message": f"order {exc.order_id} not found"},
    )
```

두 코드를 같은 자리에 두고 보면 *놀랍게 닮아 있다*. Spring은 클래스 + 메서드, FastAPI는 함수 하나 — 표현의 단위만 다를 뿐 *같은 회로*다. *어떤 예외가 어떤 응답으로 변환되는지*를 한 자리에 모아두는 책임도 같다. 그래서 9장의 출발점에서는 *불안 해소*가 빠르다 — `@ControllerAdvice` 사고를 그대로 끌고 와서 함수 데코레이터로 옮기면 된다.

여기서 한 가지 약속을 두자. **라우트 안에서는 `try/except`를 도배하지 않는다.** 의미 있는 도메인 예외를 *그냥 던지고*, 변환은 전역 핸들러에 맡긴다. Spring에서도 같은 관행이 있고, 그 관행이 잘 동작하는 이유는 명확하다 — *비즈니스 로직이 응답 포맷에 신경 쓸 일이 없다.*

> 실무 권고 (저자의 영문/한국어 표현을 옮긴 한 줄) — *라우트마다 try/except를 반복하지 말고 전역 핸들러에 위임. 핸들러에서 Sentry로 보내고 사용자에겐 정제된 JSON 응답을 돌려준다.* — Medium 딜리버스, "Exception Handling Best Practices" (reference §4.4)

이제 5가지 실패 모드를 모델링해보자.

## 도메인 예외 계층 — 의미가 곧 타입이다

주문 API의 다섯 실패 모드를 *의미 단위*로 묶어보자. 비슷한 모드끼리 부모-자식 관계로 정리하면 *핸들러도 부모로 묶을 수 있다*.

```python
class OrderError(Exception):
    """주문 도메인의 모든 예외가 상속하는 루트."""

class OrderNotFound(OrderError):
    def __init__(self, order_id: int) -> None:
        self.order_id = order_id

class InsufficientStock(OrderError):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        self.sku = sku
        self.requested = requested
        self.available = available

class PaymentDeclined(OrderError):
    def __init__(self, reason: str) -> None:
        self.reason = reason

class IdempotencyConflict(OrderError):
    def __init__(self, key: str) -> None:
        self.key = key

class RateLimitExceeded(OrderError):
    def __init__(self, retry_after_sec: int) -> None:
        self.retry_after_sec = retry_after_sec
```

다섯 모드가 같은 부모(`OrderError`)에서 갈라진다. Spring의 도메인 예외 계층 — `OrderException` 추상 클래스 + 다섯 구체 클래스 — 과 같은 모양이다. 차이가 있다면 Python에는 *checked/unchecked* 구분이 없고, *@SuppressWarnings* 같은 어노테이션도 없다. 그저 *예외를 던지면 호출 스택을 타고 올라간다*.

이제 다섯 모드를 각자 다른 HTTP 상태 코드와 응답 코드로 변환하자.

```python
@app.exception_handler(OrderNotFound)
async def handle_order_not_found(request: Request, exc: OrderNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": "ORDER_NOT_FOUND", "order_id": exc.order_id},
    )

@app.exception_handler(InsufficientStock)
async def handle_insufficient_stock(request: Request, exc: InsufficientStock) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "code": "INSUFFICIENT_STOCK",
            "sku": exc.sku,
            "requested": exc.requested,
            "available": exc.available,
        },
    )

@app.exception_handler(PaymentDeclined)
async def handle_payment_declined(request: Request, exc: PaymentDeclined) -> JSONResponse:
    return JSONResponse(
        status_code=402,
        content={"code": "PAYMENT_DECLINED", "reason": exc.reason},
    )

@app.exception_handler(IdempotencyConflict)
async def handle_idempotency_conflict(request: Request, exc: IdempotencyConflict) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"code": "IDEMPOTENCY_CONFLICT", "key": exc.key},
    )

@app.exception_handler(RateLimitExceeded)
async def handle_rate_limit_exceeded(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"code": "RATE_LIMIT_EXCEEDED"},
        headers={"Retry-After": str(exc.retry_after_sec)},
    )
```

다섯 핸들러는 `handle_*` prefix로 이름을 정한다. 데코레이터 외부에서 호출할 일은 없지만, *같은 이름으로 다섯 함수를 정의하면* ruff가 `F811` redefinition 경고를 던지고 stack trace에서도 *어느 핸들러*인지 한눈에 안 잡힌다. 2장에서 박아둔 ruff·pyright·pre-commit 안전망과도 결을 맞춘다 — *고유한 이름 + 짧은 prefix*가 표준이다. Spring의 `@ExceptionHandler` 메서드들이 *클래스 안*에 모여 있는 그림이 익숙하다면, FastAPI에서는 *같은 모듈*에 모아두는 게 자연스럽다. `app/handlers/order_handlers.py` 같은 한 파일이 합리적인 자리다.

라우트 안에서는 이제 *그냥 던진다*.

```python
@router.post("/orders", response_model=OrderRead, status_code=201)
async def create_order(
    payload: OrderCreate,
    svc: Annotated[OrderService, Depends(get_order_service)],
) -> Order:
    return await svc.create(payload)
```

`OrderNotFound`, `InsufficientStock`, `PaymentDeclined` 모두 서비스 안에서 던져진다. 라우트는 그저 *서비스를 호출하고 결과를 반환한다*. 응답 변환은 전역 핸들러가 책임진다. 한 줄도 `try/except`가 없다는 점에 주목하자. 비즈니스 로직과 응답 포맷이 *깨끗하게 분리됐다.*

## 캐치올 핸들러 — 예상 못 한 예외에도 안전망

도메인 예외는 우리가 *예상한* 실패다. 그런데 예상 못 한 예외도 늘 있다. SQLAlchemy의 `OperationalError`, 외부 결제 API의 timeout, 그리고 가끔은 우리가 잘못 짠 `KeyError`도. 이런 예외가 사용자에게 *원시 스택 트레이스*로 새어 나가면 끔찍한 일이다 — 내부 구조가 노출되고, 사용자는 무엇이 잘못됐는지 알 길이 없다.

캐치올 핸들러를 하나 두자.

```python
import structlog

logger = structlog.get_logger()

@app.exception_handler(Exception)
async def handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        exc_type=type(exc).__name__,
    )
    # Sentry 연동이 있다면: sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred."},
    )
```

`@app.exception_handler(Exception)`은 *모든 예외*를 잡는 자리다. 도메인 예외는 이미 위의 다섯 핸들러가 처리하므로 *남는 건 진짜 예상 못 한 것*뿐이다. 핸들러 안에서 두 가지를 한다 — **첫째, 로그를 남긴다(스택 트레이스 포함).** 둘째, 사용자에게는 *정제된 5xx*를 돌려준다. Sentry나 Datadog 같은 에러 추적 도구가 있다면 같은 자리에서 `capture_exception`을 호출하면 된다.

Spring 출신이라면 이게 `@RestControllerAdvice`의 *fallback `@ExceptionHandler(Exception::class)`*와 같은 자리라는 게 한눈에 보일 거다. 정확히 같은 회로다 — 그저 표현이 어노테이션이 아니라 함수 데코레이터일 뿐.

## 구조화 로깅 — `structlog`로 MDC 흉내내기

이제 로그 자체를 살펴보자. Spring의 SLF4J + Logback에는 *MDC(Mapped Diagnostic Context)*라는 자리가 있다. 한 요청 안에서 어떤 로그를 찍든 `requestId`·`userId`·`traceId` 같은 *컨텍스트 정보*가 자동으로 함께 붙는다. 새벽 두 시 알람에서 가장 빛나는 자리다 — `requestId`로 grep하면 *한 요청의 모든 로그*가 한 줄에 모인다.

FastAPI/Python에는 이 자동이 *없다*. `logging` 표준 라이브러리는 컨텍스트 정보 자동 전파를 안 한다. Spring에서 무료로 주던 게 빠진 자리다 — 손에 그릴 안전망을 우리가 짜야 한다.

이 빈자리를 `structlog`와 Python의 `contextvars`로 메운다. `structlog`는 *키-값 쌍으로 로그를 찍는* 라이브러리고, `contextvars.ContextVar`는 *코루틴·스레드 안에서 유지되는 변수*다. 둘을 합치면 Spring MDC와 *기능적으로 같은* 안전망이 만들어진다.

먼저 `structlog`를 설정한다.

```python
# app/core/logging.py
import logging
import structlog
from contextvars import ContextVar

# 요청 ID를 담을 ContextVar
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

def add_request_id(_, __, event_dict: dict) -> dict:
    rid = request_id_var.get()
    if rid is not None:
        event_dict["request_id"] = rid
    return event_dict

def configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            add_request_id,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(),
    )
```

`add_request_id`가 핵심이다. 모든 로그 이벤트에 *현재 요청 ID*를 자동으로 끼워 넣는다. 그리고 그 요청 ID는 어디서 설정되는가? 다음 절의 *요청 ID 미들웨어*에서다.

`JSONRenderer`를 쓴 이유는 운영 환경 표준이 JSON 라인 로그이기 때문이다. 컨테이너 환경(Docker, Kubernetes)의 표준 로그 수집기들(Fluent Bit, Vector, Loki)이 JSON을 *기본적으로* 파싱한다. 사람이 직접 읽는 개발 환경에서는 `ConsoleRenderer`로 바꿔 끼우면 된다. 둘 사이의 교체가 *프로세서 한 줄*이라는 점이 `structlog`의 장점이다.

## 요청 ID 미들웨어 — 4장에서 도입한 것 재사용

4장에서 ASGI 미들웨어로 *요청 ID 헤더*를 붙이는 패턴을 잠깐 시연했다. 그 미들웨어를 9장에서 정식 운영 도구로 키워보자. 다음과 같이.

```python
# app/middleware/request_id.py
from uuid import uuid4
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import request_id_var

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or uuid4().hex
        token = request_id_var.set(rid)
        try:
            request.state.request_id = rid
            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            return response
        finally:
            request_id_var.reset(token)
```

세 가지 일이 일어난다. **첫째**, 클라이언트가 `X-Request-ID` 헤더를 보냈으면 그걸 쓰고, 없으면 새 UUID를 발급한다. 분산 시스템에서 *호출 체인을 따라가는* 자리에서 중요한 디테일이다. **둘째**, `ContextVar`에 `set()`해서 *이 요청의 코루틴 어디서든* 같은 ID를 읽을 수 있게 만든다. `structlog`의 `add_request_id` 프로세서가 이 값을 자동으로 끼워 넣는다. **셋째**, 응답 헤더에 같은 ID를 박아 *클라이언트가 추적할 수 있게* 한다.

`finally:`에서 `reset(token)`을 호출하는 게 중요하다. 비동기 환경에서 `ContextVar`가 다른 코루틴으로 *새어 나가지 않게* 하는 자리다. 안 그러면 이전 요청의 ID가 다음 요청의 로그에 묻어 나오는 *조용한 버그*가 생긴다. 찜찜한 일이다.

이제 앱에 미들웨어를 붙인다.

```python
# app/main.py
from app.middleware.request_id import RequestIdMiddleware
from app.core.logging import configure_logging

configure_logging()

app = FastAPI()
app.add_middleware(RequestIdMiddleware)
```

이 두 줄을 더한 것만으로 — 라우트 안에서 `logger.info("order_created", order_id=42)`라고 한 줄 찍으면 — JSON 로그에 `request_id`가 자동으로 끼워진다. Spring의 MDC가 무료로 주던 안전망을 *세 줄의 미들웨어*로 재현했다. 손이 잠시 더 가지만 그 손길이 곧 안전망이다.

## 도메인 이벤트 로그를 어디서 찍는가

한 가지 더 짚고 가자. 주문 생성 같은 *도메인 이벤트*는 어디서 로그를 찍는 게 좋을까? 라우트일까, 서비스일까?

> 책 전체의 약속(6장에서 깔아둔 것): *트랜잭션은 서비스 레이어에서 시작하고 닫는다.* 같은 약속이 로그에도 자연스럽게 적용된다 — *비즈니스 이벤트 로그는 서비스 레이어가 책임진다.*

서비스 안에서 다음과 같이 찍는다.

```python
class OrderService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._log = structlog.get_logger().bind(service="order")

    async def create(self, payload: OrderCreate) -> Order:
        async with self._db.begin():
            order = await self._do_create(payload)
            self._log.info(
                "order_created",
                order_id=order.id,
                customer_id=payload.customer_id,
                total=str(order.total),
            )
            return order
```

`bind(service="order")`로 *모든 로그에 `service=order`*가 자동으로 붙는다. SLF4J `MarkerFactory.getMarker("order")`와 비슷한 자리지만, 더 가볍고 더 명시적이다. `request_id`는 ContextVar에서, `service`는 `bind`에서, 그리고 각 호출에서 추가한 키들이 함께 JSON 한 줄에 합쳐진다. 새벽 두 시 알람에서 *한 줄*만 보고도 "어떤 요청의 어떤 서비스의 어떤 이벤트인지"가 한눈에 잡힌다.

## Prometheus 메트릭 — 한 줄짜리 도입과 그다음

Spring Boot Actuator의 `/actuator/prometheus` 엔드포인트는 *의존성 한 줄*이면 끝났다. FastAPI도 비슷한 자리가 있다 — `prometheus-fastapi-instrumentator` 라이브러리다.

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

이 두 줄로 `/metrics` 엔드포인트가 자동으로 떠 있다. HTTP 요청 수, 응답 시간 분포(히스토그램), 5xx 비율 같은 *기본 메트릭*이 자동 수집된다. Spring Actuator + Micrometer가 자동으로 해주던 일에 *기능적으로 거의 같다*. 손이 거의 안 가는 자리다.

그런데 9장의 진짜 가치는 *기본 메트릭*이 아니라 *도메인 메트릭*이다. 주문 도메인이라면 — 주문 상태별 카운터, 결제 거절 카운터, 재고 부족 카운터 같은 *비즈니스 시그널*. 이것들은 라이브러리가 자동으로 안 준다. 우리가 짠다.

```python
# app/observability/metrics.py
from prometheus_client import Counter, Histogram

orders_total = Counter(
    "orders_total",
    "Total orders by status",
    labelnames=["status"],
)

payment_decline_total = Counter(
    "payment_decline_total",
    "Total declined payments by reason",
    labelnames=["reason"],
)

order_amount = Histogram(
    "order_amount_krw",
    "Order amount distribution (KRW)",
    buckets=(1000, 5000, 10000, 50000, 100000, 500000, 1_000_000),
)
```

그리고 서비스 안에서 사건이 일어날 때마다 카운터를 올린다.

```python
async def create(self, payload: OrderCreate) -> Order:
    async with self._db.begin():
        order = await self._do_create(payload)
        orders_total.labels(status="created").inc()
        order_amount.observe(float(order.total))
        return order

# 결제 거절을 잡는 곳에서
except PaymentDeclined as exc:
    orders_total.labels(status="payment_declined").inc()
    payment_decline_total.labels(reason=exc.reason).inc()
    raise
```

이 단계가 끝나면 그라파나 대시보드에서 *주문 상태별 분포*, *결제 거절 사유 Top 5*, *주문 금액 p50/p99* 같은 그래프를 그릴 수 있다. Spring Boot Actuator + Micrometer + Prometheus 조합이 만들어주던 *비즈니스 관측성*을 같은 도구(`prometheus_client`)로, *명시적인 카운터 증가*로 만든다.

여기서 한 번 짚자. Spring에서는 `@Timed`나 `@Counted` 어노테이션을 메서드 위에 한 줄 박으면 그만이었다. FastAPI에서는 *카운터 증가가 보이는 자리에* 있다. 디버깅이 필요한 순간에는 *카운터가 어디서 증가했는지*가 코드에서 한 줄로 추적된다 — 6장의 트랜잭션 명시성 철학과 정확히 같은 결이다.

## OpenTelemetry — 추적 한 줄

메트릭이 *얼마나*를 본다면, 트레이싱은 *어디서 시간이 갔는지*를 본다. 한 요청이 여러 서비스를 거쳐 갈 때, 어떤 단계가 느렸는지를 따라가는 자리다. Spring 진영에는 *Spring Cloud Sleuth + Zipkin*이 있었고, 지금은 *OpenTelemetry*가 표준이다. FastAPI도 같은 OpenTelemetry SDK를 쓴다.

```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
```

두 줄로 라우트별 자동 span이 만들어지고, SQLAlchemy 쿼리도 *자식 span*으로 추적된다. 별도로 OTLP 익스포터를 설정해 Jaeger·Tempo·Honeycomb 같은 백엔드로 보낸다.

도메인 코드에서 *수동 span*을 만들고 싶을 때는 다음과 같이.

```python
tracer = trace.get_tracer(__name__)

async def charge_payment(self, order: Order) -> None:
    with tracer.start_as_current_span("payment.charge") as span:
        span.set_attribute("order.id", order.id)
        span.set_attribute("payment.amount", float(order.total))
        # ... 외부 결제 API 호출
```

이 자리에서 *attribute*는 SLF4J MDC의 *값들*과 비슷하다. 추적에 함께 따라붙는 메타데이터다. 그리고 OpenTelemetry는 *trace_id*를 자동으로 발급한다 — 이걸 `request_id`와 같이 묶어 로그에 넣어두면, *한 trace의 모든 로그를 한 번에* 찾을 수 있다.

FastAPI 진영과 Spring 진영이 *같은 OpenTelemetry*를 쓴다. 사내가 이미 Spring에서 OpenTelemetry로 트레이싱하고 있다면 — FastAPI 서비스도 *같은 백엔드*에 그대로 합류할 수 있다(reference §2.9). 새 도구를 들이는 부담이 작은 자리다.

## health/readiness 엔드포인트 — Actuator의 수제 버전

Spring Boot의 `/actuator/health`는 *DB·Redis·외부 의존성*의 상태를 자동으로 모은다. FastAPI는 그게 *없다.* 다행히 짧고 명확하게 짤 수 있다.

```python
from sqlalchemy import text

@app.get("/healthz", include_in_schema=False)
async def healthz() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/readyz", include_in_schema=False)
async def readyz(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="db not ready")
    return {"status": "ready"}
```

두 엔드포인트를 *의도적으로 다른* 의미로 둔다. **`/healthz`**(*liveness*)는 "프로세스가 살아 있는가"만 본다 — 그래서 의존성 확인을 하지 않는다. Kubernetes liveness probe가 이걸 본다. **`/readyz`**(*readiness*)는 "지금 요청을 받을 준비가 됐는가"를 본다 — DB 연결, Redis 핑, 외부 의존성까지 확인한다. Kubernetes readiness probe와 로드 밸런서가 이걸 본다.

둘을 같은 엔드포인트로 묶으면 안 된다. *DB가 잠시 끊긴 상황*에서 liveness probe가 실패하면 Kubernetes가 컨테이너를 *재시작*해버린다. 진짜 문제는 DB인데 애꿎은 앱이 죽는 거다. 끔찍한 일이다. 둘을 분리해두자 — 한 번 머리에 새겨두는 게 좋다.

응답에 `include_in_schema=False`를 둔 이유는 OpenAPI `/docs`에 노출하지 않기 위해서다. 헬스 체크는 *운영 도구*이지 *API 계약*이 아니다. 사용자에게 보여줄 필요가 없다.

## Pyctuator — Spring Boot Admin과 손잡기

사내에 이미 *Spring Boot Admin*이 떠 있는 조직이라면 한 가지 옵션이 더 있다. `pyctuator` 라이브러리는 Spring Actuator API를 *Python으로 구현*한 패키지다. FastAPI 앱이 마치 Spring Boot 앱인 것처럼 Spring Boot Admin 대시보드에 등록된다.

```python
from pyctuator.pyctuator import Pyctuator

pyctuator = Pyctuator(
    app,
    "Order API",
    app_url="http://order-api:8000",
    pyctuator_endpoint_url="http://order-api:8000/pyctuator",
    registration_url="http://spring-boot-admin:8080/instances",
)
```

이 한 줄로 `/pyctuator/health`, `/pyctuator/metrics`, `/pyctuator/info` 같은 *Spring Actuator 호환 엔드포인트*가 떠 있고, Spring Boot Admin에 자동으로 등록된다(reference §5.8). 사내 운영팀이 *Spring 도구를 그대로* 쓸 수 있다는 게 가장 큰 가치다 — 새 대시보드를 따로 만들지 않아도 된다.

물론 Spring Boot Admin이 없는 조직에서는 *이 라이브러리를 들일 이유가 없다.* `prometheus-fastapi-instrumentator` + Grafana 조합이 더 일반적이고, *FastAPI 진영의 자연스러운 길*이다. 둘 중 무엇을 고를지는 *사내가 이미 쓰고 있는 도구*가 결정한다. 새 도구를 들이는 부담을 줄이는 쪽이 보통 이긴다.

## 한 호흡으로 정리

머리에 박혀야 할 건 셋이다.

**첫째, 도메인 예외 → 전역 핸들러 → 캐치올의 삼층 구조.** `@app.exception_handler`가 Spring `@ControllerAdvice`와 거의 1:1로 매핑된다. 다섯 도메인 예외(`OrderNotFound`/`InsufficientStock`/`PaymentDeclined`/`IdempotencyConflict`/`RateLimitExceeded`)는 *의미가 곧 타입*이고, 라우트 안에서는 *그냥 던진다*. 응답 변환은 전역 핸들러가 책임진다. 예상 못 한 예외는 캐치올이 잡아 *정제된 5xx*로 변환하고 Sentry로 보낸다.

**둘째, MDC의 빈자리에 `structlog` + `ContextVar` + 요청 ID 미들웨어 세 가지를 합쳐 넣는다.** Spring이 무료로 주던 자동 MDC가 *세 줄의 미들웨어*로 재현된다. 핵심은 `request_id_var.set(rid)` + `finally: reset(token)` 한 쌍 — 비동기 환경에서 컨텍스트가 *새어 나가지 않게* 잡는 자리다. 비즈니스 이벤트 로그는 6장의 트랜잭션 약속과 결을 맞춰 *서비스 레이어가 책임진다.*

**셋째, Actuator 한 줄의 자리에 *네 가지 도구*가 들어선다.** 메트릭은 `prometheus-fastapi-instrumentator` + 도메인 카운터, 트레이싱은 `FastAPIInstrumentor.instrument_app(app)`, health/readiness는 *수제 두 엔드포인트*, Spring Boot Admin 통합은 `pyctuator`. *자동의 자리에 명시가 들어선다* — 6장에서 시작된 통주저음이 9장의 관측성에서도 같은 결로 흐른다. 손이 잠시 더 가지만 그 손길이 곧 안전망이다.

다음 장은 테스트다. 9장에서 깐 도메인 예외, 미들웨어, 헬스 엔드포인트를 *어떻게 검증할 것인가*가 다음 호흡이다. Spring의 `@SpringBootTest` + `MockMvc` 자리에 FastAPI의 `TestClient(app)`이 들어서고, `@MockBean`의 자리에 `app.dependency_overrides`가 들어선다. 6장에서 익힌 트랜잭션 자동 롤백의 빈자리를 *savepoint 픽스처*로 메우는 자리도 다시 만난다. 손에 익은 9장의 회로를 들고 10장으로 가보자.
