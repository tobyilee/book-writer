<!-- 개정: 2026-05-16 라운드 1 가디언 피드백 반영 (메타 선언 2건, 마무리 절 세 기둥 재구성, 168행 호흡, Should 5·7·9, Nice 10·11) -->

# 3장. 첫 라우트와 Pydantic — `@RestController` × DTO를 한 줄에 녹이기

Spring으로 환율 변환 API 하나를 만든다고 해보자. 머릿속에 떠오르는 그림이 대략 이렇다. `CurrencyController` 클래스에 `@RestController`를 붙이고 `convert` 메서드에 `@GetMapping("/convert")`를 단다. 요청용 `ConvertRequest` DTO를 따로 짜고 `@NotNull`·`@Positive` 검증 어노테이션을 박은 뒤, 메서드 시그니처에 `@Valid`를 빼먹지 않는다. 응답용 `ConvertResponse` DTO도 또 한 클래스. Jackson 직렬화는 ObjectMapper에 맡기고, Swagger 문서가 깔끔하게 떨어지도록 `@Schema`·`@Operation`을 곳곳에 박아둔다.

손에 익은 흐름이긴 하지만, 가만히 세어보면 클래스가 셋이고 어노테이션이 십여 개다. "달러 100을 원화로 바꿔 돌려주는 함수 하나"의 본질이 컨트롤러·DTO·검증·매퍼·문서라는 다섯 레이어로 흩어져 있다. 각각 이유가 있어 굳은 관행이지만, 처음 보는 사람에게 "이 API가 뭘 하는 거지?"라고 물으면 어디부터 보여줘야 할지 살짝 난감하다.

이제 같은 일을 FastAPI로 해보자. 진짜 가치는 "코드가 짧다"가 아니라 **그 짧음에서 오는 체감**이다. Spring에서 다섯 곳에 흩어져 있던 책임이 FastAPI에서는 한 함수 시그니처 위로 모인다. 검증·직렬화·문서가 같은 자리에서 같은 타입을 본다. 그 체감을 손에 쥐어보자.

## 한 함수가 곧 컨트롤러다

본격적으로 환율 API를 짜기 전에, FastAPI의 라우팅이 어떻게 생겼는지부터 살펴보자. 어렵게 갈 필요 없이 가장 단순한 형태로 시작한다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello"}
```

다섯 줄이다. Spring으로 같은 일을 하려면 `@SpringBootApplication` 클래스, `@RestController` 클래스, `@GetMapping("/")` 메서드, build.gradle의 starter 의존성까지 — 적게 잡아도 네 파일을 건드려야 한다. FastAPI에서는 `app = FastAPI()` 한 줄로 애플리케이션이 만들어지고 `@app.get("/")` 데코레이터 한 줄로 라우트가 등록된다. 클래스가 없다는 사실에 주목하자. **함수 하나가 곧 컨트롤러다.**

Spring 출신이 처음 이 코드를 보면 본능적으로 묻는다. "그럼 의존성은 어디로 주입하지? 빈은 어떻게 등록하지?" 의미 있는 질문이다. 답은 다음 장에서 차근차근 풀어내자. 지금은 한 가지만 받아들이자 — FastAPI에서는 **HTTP 메서드 + 경로 + 함수**가 라우팅의 기본 단위다. 클래스로 묶는 건 나중에 선택지로 등장하지만 출발점은 함수다.

이 한 줄짜리 데코레이터가 Spring의 `@GetMapping`과 얼마나 닮아 있는지 옆에 놓고 보자.

```java
// Spring
@RestController
public class HelloController {
    @GetMapping("/")
    public Map<String, String> root() {
        return Map.of("message", "hello");
    }
}
```

```python
# FastAPI
@app.get("/")
def root():
    return {"message": "hello"}
```

같은 HTTP, 같은 응답, 같은 의도. 다른 건 *어디에 정보가 모이는가*뿐이다. Spring은 클래스 한 단계를 거쳐 메서드에 도달하고, FastAPI는 곧장 함수에 도달한다. 이 차이가 한 줄 길이의 차이로만 보이면 손해다. 함수가 라우팅의 기본 단위라는 사실은 다음 절에서 진짜 위력을 드러낸다.

## DTO와 검증을 타입 힌트 한 줄로

이제 환율 변환 API를 본격적으로 짜보자. 엔드포인트는 단순하다 — `/convert`에 출발 통화·도착 통화·금액을 보내면 변환된 금액과 적용 환율을 돌려준다. Spring으로 짜면 두 DTO와 검증 어노테이션과 컨트롤러 메서드가 어우러진다. FastAPI에서는 같은 일이 어떻게 펼쳐지는지 보자.

먼저 Pydantic 모델 두 개를 정의한다.

```python
from decimal import Decimal
from pydantic import BaseModel, Field

class ConvertRequest(BaseModel):
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    amount: Decimal = Field(gt=0)

class ConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: Decimal
    converted: Decimal
    rate: Decimal
```

처음 보는 사람도 한눈에 읽힌다. `BaseModel`을 상속하면 그게 곧 DTO다. `Field(...)`에 검증 조건을 매개변수로 넘긴다 — `min_length`, `max_length`, `gt`(greater than) 같은 키워드가 그대로다. Spring의 `@NotNull`, `@Size(min=3, max=3)`, `@Positive`가 한 줄들로 녹아 들어갔다.

같은 검증을 Spring으로 표현하면 다음 정도다.

```java
public record ConvertRequest(
    @NotNull @Size(min = 3, max = 3) String fromCurrency,
    @NotNull @Size(min = 3, max = 3) String toCurrency,
    @NotNull @Positive BigDecimal amount
) {}
```

코드 길이는 비슷하다 — Spring 쪽이 record 덕분에 짧을 때도 있다. 그런데 두 코드를 *같은 자리에 두고* 보면, FastAPI는 "타입과 제약을 한 번에" 적는 반면 Spring은 "타입은 매개변수로, 제약은 어노테이션으로" 분리해서 적는다. 사소해 보이지만, 모델이 늘고 규칙이 복잡해질수록 *어디서 검증이 일어나는지* 따라가느라 눈이 클래스 위아래를 오간다. 작은 동선의 차이가 누적되면 꽤 번거롭다. FastAPI는 그 동선을 한 줄로 줄여준다.

자, 이제 모델을 정의했으니 라우트에 붙여보자.

```python
@app.post("/convert", response_model=ConvertResponse)
def convert(req: ConvertRequest):
    rate = lookup_rate(req.from_currency, req.to_currency)
    converted = (req.amount * rate).quantize(Decimal("0.01"))
    return ConvertResponse(
        from_currency=req.from_currency,
        to_currency=req.to_currency,
        amount=req.amount,
        converted=converted,
        rate=rate,
    )
```

여기서 두 가지가 동시에 일어난다. 첫째, `req: ConvertRequest`라는 타입 힌트 한 줄이 Spring의 `@RequestBody`와 `@Valid` 두 어노테이션을 합친 역할을 한다. FastAPI가 요청 본문의 JSON을 자동으로 파싱하고, Pydantic이 검증까지 마친 뒤에야 함수 안으로 흘러 들어온다. 검증이 실패하면 FastAPI가 알아서 `422 Unprocessable Entity` 응답을 만들어 돌려준다 — 우리 손이 닿기 전이다. 둘째, `response_model=ConvertResponse`는 응답 직렬화의 계약이다. 함수가 반환한 객체가 이 모델에 맞춰 검증되고 JSON으로 변환된다. Spring으로 치면 Jackson의 `ObjectMapper`와 응답 DTO의 결합을 한 줄로 박아둔 것과 같다.

핵심을 한 문장으로 정리하면 이렇다 — **타입 힌트가 곧 검증·직렬화·문서의 단일 소스다.** 1장 매핑 표의 "요청 바인딩"·"응답 직렬화"·"검증" 세 칸이 FastAPI에서는 모두 *같은 자리에서* 일어난다. Spring에서는 그 셋이 다른 클래스·다른 어노테이션·다른 라이브러리(Jackson·Hibernate Validator·springdoc)로 나뉘어 있었다. FastAPI는 그 셋을 Pydantic 모델 하나로 묶었다.

검증이 실패할 때 어떤 응답이 가는지 보자. `amount: -10` 같은 값이 들어오면 FastAPI가 이런 JSON을 자동으로 만든다.

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "amount"],
      "msg": "Input should be greater than 0",
      "input": "-10",
      "ctx": {"gt": 0}
    }
  ]
}
```

Spring의 `MethodArgumentNotValidException`을 잡아서 직접 만들어주던 응답 구조와 비교해보면, 필드 경로(`loc`)·메시지·입력값·제약 조건이 모두 들어 있어 클라이언트가 어떤 필드를 어떻게 고쳐야 할지 정확히 안다. 회사의 표준 에러 포맷에 맞추고 싶다면 9장에서 다룰 전역 예외 핸들러로 갈아 끼우면 된다. 출발점에서 이만큼이 기본값이라는 사실이 든든하다.

## field_validator — Pydantic의 핵심 한 가지

`Field(...)`로 처리되지 않는 검증 규칙도 있다. 환율 API라면 예를 들어 "출발 통화와 도착 통화는 같을 수 없다" 같은 규칙이다. 두 필드를 동시에 봐야 하는 규칙은 `Field`만으로 표현하기 어렵다. Spring의 `@AssertTrue` 메서드나 커스텀 `ConstraintValidator`를 떠올리게 되는 자리다.

Pydantic은 `@field_validator`와 `@model_validator` 두 가지를 준다. 한 필드만 보는 경우는 전자, 모델 전체를 보는 경우는 후자다. 한 번 손에 익으면 응용이 쉽다.

```python
from pydantic import BaseModel, Field, field_validator

class ConvertRequest(BaseModel):
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    amount: Decimal = Field(gt=0)

    @field_validator("from_currency", "to_currency")
    @classmethod
    def to_upper(cls, value: str) -> str:
        return value.upper()
```

여기서 짚고 가자. `@field_validator`는 검증뿐 아니라 **정규화(normalization)**도 같이 처리한다. 사용자가 `usd`로 보내든 `USD`로 보내든 함수 안에서는 항상 대문자로 받는다. Spring에서는 검증과 정규화를 분리해 컨버터를 따로 두지만, Pydantic은 그 경계를 의도적으로 흐려놓았다. 그래서 "데이터가 모델에 들어가는 순간 정상화된다"는 가정을 라우트·서비스 레이어에서 그대로 믿을 수 있다.

검증 자체도 가능하다. "출발 통화와 도착 통화는 달라야 한다"는 모델 차원 규칙을 추가해보자.

```python
from pydantic import model_validator

class ConvertRequest(BaseModel):
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    amount: Decimal = Field(gt=0)

    @field_validator("from_currency", "to_currency")
    @classmethod
    def to_upper(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def currencies_must_differ(self) -> "ConvertRequest":
        if self.from_currency == self.to_currency:
            raise ValueError("from_currency and to_currency must differ")
        return self
```

`mode="after"`는 "필드별 검증·정규화가 모두 끝난 뒤" 모델 전체를 본다는 뜻이다. `to_upper`가 먼저 적용되고, 그다음에야 `currencies_must_differ`가 호출된다 — 사용자가 `usd`·`USD`로 다르게 적어도 같은 코드로 정규화된 뒤 비교된다. 이 *순서*가 처음에는 살짝 헷갈리니, 한 번 머리에 새겨두자.

한 가지 더. Pydantic은 **v1과 v2의 문법 차이**가 제법 크다. 검색하면 `@validator`(v1) vs `@field_validator`(v2), `@root_validator`(v1) vs `@model_validator`(v2), `parse_obj`(v1) vs `model_validate`(v2), `dict()`(v1) vs `model_dump`(v2) 같은 분기를 자주 만난다. 인터넷에는 아직 v1 코드가 많아서 처음에는 어느 게 v2인지 헷갈리고 찜찜하다. 우리는 책 전체에서 **v2만** 쓴다. v1 예제를 만나면 "옛 문법이구나" 하고 v2로 옮겨 적는 습관을 들이는 편이 낫다.

## 요청 모델 ≠ 응답 모델 — 분리의 약속

다시 환율 API로 돌아오자. 우리는 이미 `ConvertRequest`·`ConvertResponse` *두 개의* 모델을 만들었다. "같은 모델로 입력과 출력을 다 처리하면 코드가 짧지 않을까?" 하는 생각이 들 수 있다. Spring에서는 `record`나 `class`를 입출력 양쪽에 재사용하는 패턴이 꽤 흔하다. FastAPI에서도 가능하긴 하다. 그런데 책 전체에서 한 가지 약속을 미리 두고 가자 — **입력 모델과 출력 모델은 분리하는 편이 낫다.**

이유를 짚어보자. 입력에는 있고 출력엔 없어야 할 필드가 있다. 가장 흔한 예가 비밀번호다. 사용자 생성 요청에는 `password` 필드가 필요하지만 응답에는 절대 들어가면 안 된다. 한 모델로 다 처리하다가 응답에 비밀번호가 새어나가는 사고는 보안 회고에서 자주 만나는 항목이다. 끔찍한 일이다. 반대로 출력에는 있고 입력엔 없어야 할 필드도 있다. 서버가 발급한 `id`·`created_at` 같은 값. 사용자가 임의의 `id`를 보내 다른 자원을 덮어쓰게 두면 곤란하다.

책 전체에서 다음 컨벤션을 약속하자.

- `XxxCreate` — 생성 요청 본문
- `XxxUpdate` — 수정 요청 본문 (필드가 선택형)
- `XxxRead` — 응답 본문 (외부에 보여줄 형태)
- `XxxInDB` — DB 엔티티에 가까운 내부 표현 (필요한 경우만)

환율 API는 작아서 `Request`/`Response` 둘로 끝나지만, 사용자·도서·태스크 같은 도메인이 등장하면 이 네 가지가 차차 보일 것이다. 패턴을 미리 손에 익혀두자.

다음 코드는 같은 약속을 짧게 보여주는 예다.

```python
class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    created_at: datetime
```

`password`는 입력에만, `id`·`created_at`은 출력에만 있다. 라우트 시그니처도 이 약속을 그대로 반영한다.

```python
@app.post("/users", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate):
    user = user_service.create(payload)
    return user
```

`payload: UserCreate`로 받고 `response_model=UserRead`로 내보낸다. *같은 모델*이 양쪽에 등장하지 않는 게 핵심이다. Pydantic은 함수가 반환한 객체를 `UserRead`에 맞춰 직렬화해주므로, 내부 객체에 비밀번호 필드가 있어도 응답에 새어 나가지 않는다. 단, *모델 분리*가 그 안전망의 전제임을 잊지 말자.

## /docs가 알아서 떠 있다

위 코드를 띄우고 브라우저로 `http://localhost:8000/docs`에 접속해보자. Swagger UI가 이미 떠 있다. 추가 설정 없이. `POST /convert` 엔드포인트가 보이고 요청·응답 스키마가 펼쳐져 있다. "Try it out"으로 직접 호출도 된다. `/redoc`으로 가면 같은 정보가 ReDoc 스타일로 표시된다.

왜 이 자동 문서화가 묘하게 신기하게 느껴질까? Spring에서 같은 화면을 띄우려면 `springdoc-openapi-starter-webmvc-ui` 의존성을 추가하고, `@Operation`·`@Schema`·`@ApiResponse` 어노테이션을 컨트롤러와 DTO 곳곳에 박아야 했다. 도메인이 늘면 어노테이션도 같이 늘어난다.

FastAPI는 그 추가 어노테이션이 없다. 왜일까? **타입 힌트가 곧 OpenAPI 스키마의 단일 소스다.** Pydantic 모델이 곧 스키마, 라우트의 시그니처가 곧 엔드포인트 메타데이터. FastAPI가 그 정보를 모아 OpenAPI 3.x JSON을 만들고 Swagger UI에 흘려보낸다. 사람이 같은 정보를 두 번 적을 일이 없다.

더 풍부한 문서를 원하면 옵션이 있다. 라우트에 `summary`·`description`·`tags`·`responses`를 넣어 보강할 수 있고, `Field`의 `description`이 스키마 설명으로 그대로 노출된다.

```python
@app.post(
    "/convert",
    response_model=ConvertResponse,
    summary="통화를 변환한다",
    tags=["currency"],
    responses={
        404: {"description": "환율을 찾을 수 없음"},
    },
)
def convert(req: ConvertRequest):
    ...
```

이 정도 보강은 *문서 품질을 끌어올리고 싶을 때*만 손대면 된다. 시작 단계에서는 타입 힌트만 잘 적어둬도 충분하다.

`springdoc-openapi`도 결국 같은 목적지를 향한다 — 코드에서 자동으로 OpenAPI 스펙을 뽑는 것. 다만 Spring은 모델·검증·문서가 *서로 다른 라이브러리*에 흩어져 있어서 셋이 맞물리는 자리에 어노테이션이 들어간다. FastAPI는 그 셋이 *한 라이브러리*(Pydantic) 안에 있어서 한 번만 적어도 된다. 결과는 비슷한데 동선이 다르다.

## 환율 API를 완성하자

지금까지 익힌 조각을 한 파일에 모아 환율 변환 API를 완성해보자. 실제 환율 조회는 `lookup_rate`라는 가짜 함수로 두고, 4장에서 의존성 주입을 배우면 그 자리에 진짜 환율 서비스가 들어온다.

```python
# app/main.py
from decimal import Decimal
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(title="Currency Converter")

class ConvertRequest(BaseModel):
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    amount: Decimal = Field(gt=0)

    @field_validator("from_currency", "to_currency")
    @classmethod
    def to_upper(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def currencies_must_differ(self) -> "ConvertRequest":
        if self.from_currency == self.to_currency:
            raise ValueError("from_currency and to_currency must differ")
        return self

class ConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: Decimal
    converted: Decimal
    rate: Decimal
    at: datetime

_FAKE_RATES: dict[tuple[str, str], Decimal] = {
    ("USD", "KRW"): Decimal("1380.50"),
    ("KRW", "USD"): Decimal("0.000724"),
    ("USD", "JPY"): Decimal("156.42"),
}

def lookup_rate(from_ccy: str, to_ccy: str) -> Decimal:
    rate = _FAKE_RATES.get((from_ccy, to_ccy))
    if rate is None:
        raise HTTPException(status_code=404, detail=f"rate {from_ccy}->{to_ccy} not found")
    return rate

@app.post("/convert", response_model=ConvertResponse)
def convert(req: ConvertRequest) -> ConvertResponse:
    rate = lookup_rate(req.from_currency, req.to_currency)
    converted = (req.amount * rate).quantize(Decimal("0.01"))
    return ConvertResponse(
        from_currency=req.from_currency,
        to_currency=req.to_currency,
        amount=req.amount,
        converted=converted,
        rate=rate,
        at=datetime.now(timezone.utc),
    )
```

`uv run uvicorn app.main:app --reload`로 띄우고 두 가지를 확인해보자.

첫째, 정상 요청.

```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"from_currency":"usd","to_currency":"krw","amount":100}'
```

응답은 다음과 비슷할 것이다.

```json
{
  "from_currency": "USD",
  "to_currency": "KRW",
  "amount": "100",
  "converted": "138050.00",
  "rate": "1380.50",
  "at": "2026-05-16T03:21:47.123456+00:00"
}
```

`usd`로 보냈는데 `USD`로 정규화되어 돌아왔다. `@field_validator`가 한 일이다. 같은 통화를 두 번 적으면 어떻게 될까?

```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"from_currency":"USD","to_currency":"USD","amount":100}'
```

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body"],
      "msg": "Value error, from_currency and to_currency must differ",
      ...
    }
  ]
}
```

`@model_validator`가 잡아서 `422`로 돌려보냈다. 함수 안으로 잘못된 데이터가 *흘러 들어오기 전*에 막혔다는 점을 기억해두자. 컨트롤러 안에서 `if from.equals(to)` 같은 분기를 들고 다니지 않아도 된다는 뜻이다. `/docs`로 가면 Swagger UI가 떠 있고, 모델·검증·라우트·문서가 한 파일 안에 잘 묶여 있는 그림이 한눈에 들어온다.

## GET으로 받고 싶다면 — 쿼리·경로 파라미터의 자리

환율 변환은 본질적으로 *읽기 작업*에 가까워서 `GET /convert?from=USD&to=KRW&amount=100` 같은 모양도 자연스럽다. 같은 API를 GET으로 다시 짜보자.

```python
from typing import Annotated
from fastapi import Query

@app.get("/convert", response_model=ConvertResponse)
def convert_get(
    from_currency: Annotated[str, Query(min_length=3, max_length=3, alias="from")],
    to_currency: Annotated[str, Query(min_length=3, max_length=3, alias="to")],
    amount: Annotated[Decimal, Query(gt=0)],
) -> ConvertResponse:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency == to_currency:
        raise HTTPException(status_code=422, detail="from and to must differ")
    rate = lookup_rate(from_currency, to_currency)
    converted = (amount * rate).quantize(Decimal("0.01"))
    return ConvertResponse(
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted=converted,
        rate=rate,
        at=datetime.now(timezone.utc),
    )
```

새 친구가 둘 등장한다. `Annotated[...]`와 `Query(...)`다. `Annotated`는 Python의 표준 타입 도구로 "이 타입에 부가 정보를 덧붙인다"는 뜻이다. FastAPI는 부가 정보 자리에 `Query`·`Path`·`Body`·`Header` 마커를 보고 *어디서* 값을 가져올지 판단한다. 위에서는 쿼리스트링이라 `Query`다.

`alias="from"`은 Python 예약어 회피 트릭이다 — `from`은 예약어라 변수명으로 못 써서 쿼리 키는 `from`, 함수 내부 이름은 `from_currency`로 두었다. Spring의 `@RequestParam("from") String fromCurrency`와 같은 패턴이다.

경로 변수는 `Path`, 헤더는 `Header`로 받는다. `Query`/`Path`/`Body`/`Header`의 세부 옵션은 부록 A에 모아두었다 — 디테일을 한꺼번에 외우려 하면 1막의 *불안 해소*가 깨진다. 지금 우리가 손에 쥐려는 건 "한 함수의 체감" 한 가지다.

한 가지만 더. POST 모델 검증과 GET 쿼리 검증이 *같은 표현*을 쓴다는 점에 주목하자. Spring에서는 `@Valid` 모델 검증과 `@Min`·`@Max` 같은 파라미터 검증이 같은 자카르타 어노테이션을 공유하지만 어디까지 통하는지가 묘하게 갈렸다. FastAPI는 그 경계를 의도적으로 통일했다. **검증 규칙의 자리는 어디서 값이 오든 같다.** 손에 익으면 코드의 결이 한층 일관된다.

## 정직한 한계 — 타입 힌트가 *컴파일이 아니다*

여기까지 보면 "타입 힌트 한 줄에 다 들어 있다"는 인상이 깊게 박힌다. 정직하게 짚고 가야 할 게 하나 있다. **Python의 타입 힌트는 Java의 컴파일 강제 수준이 아니다.** 런타임 검증은 Pydantic이 해주지만 *함수 내부*의 변수·연산까지 타입을 강제하지는 않는다. 잘못 쓰면 `AttributeError`로 터지거나 더 나쁘게는 조용히 잘못된 결과가 나간다.

> "약 15%의 결함은 mypy 같은 타입 체커로 막을 수 있었다." — Khan et al. 2021, TSE 논문(reference §5.7).

15%라는 숫자는 무시할 만큼 작지 않다. 하지만 "Java처럼 모든 결함이 컴파일에서 막힌다"고 착각해도 곤란하다. 두 사실을 같이 들고 가는 게 핵심이다. 책에서는 *이중 안전망*을 권한다.

1. **Pydantic 런타임 검증** — 외부 입력은 모델 경계에서 100% 검증.
2. **mypy 또는 pyright 정적 검사** — 내부 코드의 타입 흐름을 별도로 검증.

이미 2장에서 `mypy --strict`를 CI에 박아두자고 약속했다. 그 약속이 여기서 빛을 발한다. 라우트 함수 안에서 `req.amount`를 `int`로 잘못 다루거나 `ConvertResponse` 필드를 빠뜨리면 mypy가 잡아낸다.

Java에서는 컴파일러 한 사람이 정적 검사를 도맡았다. Python에서는 *두 사람*이 그 일을 나눠 한다 — **mypy**가 정적 부분을, **Pydantic**이 런타임 부분을. 둘 중 하나만 쓰면 안전망에 구멍이 난다.

## 한 줄만 더 — APIRouter는 4장에서

지금까지 우리는 모든 라우트를 *루트 앱 객체*에 바로 붙였다. 도메인이 환율 하나일 때는 괜찮지만, 사용자·도서·태스크가 늘면 한 파일에 다 적기 어려워진다.

Spring에서는 컨트롤러 클래스를 도메인별로 나누고 `@RequestMapping("/users")` prefix를 박는 패턴이 자연스럽다. FastAPI에서는 `APIRouter`가 그 자리를 차지한다. 도메인별 파일에 `router = APIRouter(prefix="/users")`를 두고 라우트를 등록한 뒤 `app.include_router(router)`로 묶는다. 4장에서 의존성 주입을 배우면 `APIRouter`도 짧은 절에서 같이 시연한다. 이 챕터에서는 *루트 앱에 직접 붙는* 형태로 둔다 — 한 함수의 체감이 흐려지지 않도록.

## 한 호흡으로 정리

머리에 박혀야 할 건 셋이다.

**첫째, 한 함수의 시그니처가 곧 컨트롤러다.** Spring의 `@RestController` + DTO + `@Valid` 삼중주가 `@app.post(...)` + `BaseModel` + 타입 힌트 한 줄로 합쳐진다. 검증·직렬화·문서가 *같은 자리에서 같은 모델*을 본다. 1장 매핑 표의 세 칸이 FastAPI에서는 한 자리로 모인다는 뜻이다.

**둘째, Pydantic 모델 안에 검증과 정규화를 함께 둔다.** `Field`·`field_validator`·`model_validator`가 그 자리를 차지한다. 그리고 입력과 출력 모델은 분리한다는 약속(`XxxCreate`/`XxxRead`)을 책 전체에서 함께 들고 간다. `/docs`가 알아서 떠 있고, `Annotated[..., Query/Path/Body/Header]`로 값의 출처를 명시한다.

**셋째, 타입 힌트는 *컴파일이 아니다*.** Java의 컴파일러 한 사람이 하던 일을 Python에서는 *두 사람*이 나눠 한다 — Pydantic이 외부 입력의 런타임 경계를, mypy/pyright가 내부 코드의 정적 흐름을. 둘 중 하나만 쓰면 안전망에 구멍이 난다.

다음 장은 `Depends()`다. `lookup_rate`를 가짜 딕셔너리에서 진짜 서비스로 바꾸고, 그 서비스를 함수 파라미터로 주입한다. Spring의 `@Autowired` 사고가 FastAPI의 함수-파라미터 DI로 어떻게 옮겨가는지, 요청-스코프가 기본값이라는 사실이 코드를 어떻게 바꾸는지, `yield` 의존성으로 트랜잭션·세션 같은 자원을 어떻게 끌고 다니는지를 살펴보자. 기억해두자 — Spring의 자동 주입이 사라진 자리에 놓이는 건 *명시적 함수 파라미터*다. 이 한 줄이 4장의 출발점이다.
