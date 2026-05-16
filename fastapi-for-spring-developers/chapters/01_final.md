# 1장. 왜 FastAPI, 왜 Spring 출신에게 친숙한가

월요일 아침, 팀장이 슬쩍 자리에 와서 묻는다고 해보자.

"이번에 새로 만드는 추천 API 말이야, Python으로 한번 만들어봅시다. FastAPI라는 거 있다던데."

머릿속이 잠깐 비는 기분이 든다. 8년을 `@RestController`와 `@Autowired`로 살았는데, 갑자기 다른 언어로 백엔드를 짜라니. 인터넷 튜토리얼을 열어보면 함수 위에 `@app.get("/")` 한 줄이 떡 하니 붙어 있다. 어디서 많이 본 모양이긴 한데 어딘가 허전하다. 트랜잭션은 어떻게 거는 거지? `@Valid`는 어디로 갔지? 빈은 어떻게 등록하지?

그러다가 결국 한 줄로 정리되는 질문이 머리에 떠오른다. *내가 알고 있던 Spring 사고를 여기서도 써먹을 수 있나?* 혹은 *전부 버리고 처음부터 다시 배워야 하나?*

그렇다면 답은 어디에 있을까. 둘 다 아니다 — 사고의 *어느 부분*은 그대로 가져가고, *어느 부분*은 무너지며, *어느 자리*에는 직접 손으로 무언가를 갖다 놓아야 한다. 그 지도를 함께 그려보자.

## FastAPI는 어떤 도구인가

FastAPI 공식 문서의 한 줄은 이렇다. "현대적이고, 빠르며(고성능), 파이썬 표준 타입 힌트에 기초한 Python의 API를 빌드하기 위한 웹 프레임워크."

문장이 길다. 핵심만 짚어보자. **타입 힌트가 곧 검증·직렬화·문서의 단일 소스다.** 이 한 줄이 FastAPI의 정체성 절반을 차지한다.

Spring 진영을 떠올려보자. 우리는 같은 일을 하기 위해 세 가지를 따로 만들어 왔다.

```java
// 자바 - Spring Boot
@PostMapping("/users")
public UserDto createUser(@Valid @RequestBody UserCreateDto dto) {
    return userService.create(dto);
}

public class UserCreateDto {
    @NotBlank
    @Size(min = 3, max = 50)
    private String username;

    @Email
    private String email;

    // ... getter/setter
}
```

여기서 `@Valid`가 검증을 켜고, Jackson이 JSON ↔ 자바 객체 변환을 하고, `springdoc-openapi`가 Swagger 문서를 만들어준다. 세 시스템이 같은 DTO를 *세 번* 들여다본다. 어느 하나라도 어긋나면 디버깅이 시작된다.

FastAPI는 그걸 한 줄에 합친다.

```python
# 파이썬 - FastAPI
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

@app.post("/users")
def create_user(user: UserCreate) -> UserCreate:
    return user
```

`user: UserCreate` 한 줄이 동시에 세 가지 일을 한다. 들어온 JSON을 `UserCreate` 객체로 만들고, `min_length`·`EmailStr` 같은 제약을 검증하고, `/docs`에 자동 생성된 Swagger UI에 모델 스키마로 노출된다. 이 한 함수를 띄워놓고 브라우저에서 `/docs`를 열어 보면, 뭔가 마법 같은 일이 일어난 기분이 든다. 사실 마법은 아니다. 타입 힌트 한 줄을 세 시스템이 *공유*하기로 약속한 결과일 뿐이다.

이 약속에는 두 얼굴이 있다. 한쪽은 명백하다 — 같은 정보를 세 번 적지 않아도 된다. 다른 한쪽이 좀 무겁다. 타입 힌트가 *런타임에* 검증된다는 건 컴파일 단계에서 한 번 더 막아주는 자바와 다르다. 이 차이가 왜 그렇게 무거운지는 책을 따라가며 차차 만지게 된다.

## 얇은 프레임워크의 정체

Spring Boot가 거대한 단일 우산이라면, FastAPI는 그 우산을 펴기 위해 세 개의 부품을 모아놓은 조립품에 가깝다. 그 세 부품이 곧 FastAPI의 골격이다.

| 레이어 | 역할 | Spring 진영과의 평행 |
|---|---|---|
| **Starlette** | ASGI 기반 HTTP/라우팅/미들웨어 | Spring MVC의 DispatcherServlet |
| **Pydantic v2** | 데이터 검증·직렬화 (Rust 코어) | Jackson + Hibernate Validator |
| **uvicorn** | ASGI 서버 (uvloop + httptools) | Tomcat / Jetty / Netty |

이 셋 위에 FastAPI는 라우팅 데코레이터와 의존성 주입 시스템, 그리고 OpenAPI 자동 생성기를 얇게 얹는다. 그래서 FastAPI 자체의 코드량은 Spring Boot에 비해 놀라울 정도로 작다. "얇다"는 게 어떤 의미인지 짐작이 가는지? 손에 잡히는 부품이 명확하다는 점이 좋다. 그런데 거꾸로 — Spring Boot가 알아서 묶어주던 일을 우리가 가끔 직접 묶어야 한다.

또 한 가지 짚고 가자. FastAPI는 처음부터 ASGI 위에 있다. ASGI는 비동기 프로토콜이다. Spring 진영의 비유를 들자면 — *처음부터 WebFlux로 짠 Spring*이라고 생각하면 이해하기 쉽다. 다만 Java 스레드풀과 Python `asyncio` 이벤트 루프의 본질적 차이 때문에 동시성 특성은 또 다르다. 이 차이는 8장에서 본격적으로 파볼 주제다. 지금은 "FastAPI는 ASGI 위, 즉 논블로킹 모델 위에 있다"는 사실 한 줄만 머리에 두자.

## 한눈 매핑 — 책 전체를 관통할 지도

이제 본격적인 지도를 펴보자. 이 표는 앞으로 거의 모든 장에서 어딘가 한 번씩 다시 만나게 될 비교표다. 처음 봤을 때 절반쯤 막연하게 느껴지는 게 정상이다. 지금은 "아, 이렇게 1:1로 그릴 수 있구나"라는 윤곽만 잡고, 각 줄의 디테일은 해당 장에서 본격적으로 파게 된다.

| 카테고리 | Spring / Java | FastAPI / Python | 책의 다룸 |
|---|---|---|---|
| HTTP 라우팅 | `@RestController` + `@GetMapping` | `@app.get("/path")` 데코레이터 | 3장 |
| 요청 바인딩 | `@RequestBody UserDto` + `@Valid` | `user: UserCreate` (Pydantic) | 3장 |
| 응답 직렬화 | Jackson `ObjectMapper` | Pydantic `model_dump()` | 3장 |
| 검증 | `jakarta.validation.constraints.*` | Pydantic `Field`, `EmailStr`, `@field_validator` | 3장 |
| DI / IoC | `@Component`, `@Autowired`, `@Bean` | `Depends(...)` (함수 파라미터 마커) | 4장 |
| 횡단관심 | `@Aspect`, `@Around`, `@Transactional` | ASGI 미들웨어 + `dependencies=[Depends(...)]` | 4·6·9장 |
| 트랜잭션 | `@Transactional` | `async with session.begin():` 명시 | **6장** |
| ORM | Hibernate / Spring Data JPA | SQLAlchemy 2.0 | 5장 |
| 레포지토리 | `interface UserRepository extends JpaRepository<User, Long>` | 수동 클래스 작성 | 5장 |
| 마이그레이션 | Flyway / Liquibase | Alembic | 5장 |
| 예외 처리 | `@ControllerAdvice` + `@ExceptionHandler` | `@app.exception_handler(MyExc)` | 9장 |
| 테스트 | `MockMvc` + `@SpringBootTest` | `TestClient(app)` + `pytest` | 10장 |
| 인증/인가 | Spring Security + `@PreAuthorize` | `Depends(get_current_user)` + scope | 7장 |
| 백그라운드 | `@Async`, `@Scheduled` | `BackgroundTasks`, APScheduler, ARQ, Celery | 8장 |
| 관측성 | Spring Boot Actuator + Micrometer | OpenTelemetry SDK + Prometheus client | 9장 |
| 빌드/의존성 | Maven / Gradle | `pyproject.toml` + uv / Poetry | 2장 |
| 서버 런타임 | Tomcat (스레드풀) | uvicorn + gunicorn 다중 워커 | 11장 |
| DTO ↔ Entity 변환 | MapStruct / ModelMapper | Pydantic `model_validate(entity)` | 3·5장 |
| JSON 라이브러리 | Jackson | Pydantic v2 / orjson | 3장 |
| 로깅 | SLF4J + Logback | `logging` 표준 + structlog | 9장 |
| 시크릿 관리 | `@Value("${...}")`, Spring Config | `pydantic-settings` | 7·11장 |
| 비동기 | WebFlux + Reactor | `async/await` + asyncio | 8장 |
| Spring Boot Admin 연동 | 기본 통합 | `pyctuator` | 9장 |
| SSE/WebSocket | WebFlux SSE / `@ServerEndpoint` | Starlette 내장 | 12장 |

이 표를 노트 한구석에 적어두거나 책을 펼친 상태로 책상 위에 둬도 좋다. 어느 장을 읽다가 "이게 Spring으로 치면 뭐였지?" 싶은 순간이 올 텐데, 그때마다 여기로 돌아오면 된다. *이 지도가 너를 빈 손으로 두지 않을 거다.*

## 손에 잡히는 비교 — 같은 일을 두 줄로

말로만 매핑을 늘어놓으면 머리에 잘 박히지 않는다. 우리가 8년 동안 손에 익힌 컨트롤러 하나와, FastAPI의 라우트 함수 하나를 양면으로 놓아보자.

```java
// 자바 - Spring Boot
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }
}
```

```python
# 파이썬 - FastAPI
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

@app.get("/api/users/{user_id}")
def get_user(
    user_id: int,
    svc: Annotated[UserService, Depends(get_user_service)],
) -> UserDto:
    return svc.find_by_id(user_id)
```

비교해보면 둘이 거의 같은 일을 한다는 게 보인다. URL 매핑, 경로 변수 바인딩, 의존성 주입, 응답 직렬화. 그런데 Python 쪽이 한 함수다. 클래스가 없다. `private final` 한 줄이 없다. 생성자도 없다. 응답 타입은 함수 반환 타입 힌트로 표현된다.

"한 함수의 체감"이라고 부를 만한 것이다. 처음 만져보는 Spring 출신은 이 감각을 좋아하기도 하고, 동시에 약간 불안해한다. *진짜로 이 한 함수가 우리가 알던 컨트롤러 + DTO + Validator + Swagger를 다 해낸다고?* 그렇다. 다만 한 가지 단서가 있다 — 한 함수 안에 다 들어 있다는 말은, 거꾸로 *프레임워크가 알아서 묶어주던 횡단 관심사*가 그만큼 *바깥에 드러난다*는 뜻이기도 하다. 이건 칼날의 양면이다.

## 의존성 주입의 미묘한 비틀림

위 코드에서 한 가지 짚고 갈 게 있다. `Depends(get_user_service)`라는 표현이다.

Spring에서 우리는 `@Autowired` 또는 생성자 주입으로 빈을 받아왔다. 컨테이너가 시작 시점에 그래프를 짠다. 빈은 기본적으로 싱글톤이다. FastAPI는 다르다.

FastAPI의 `Depends()`는 **함수 파라미터의 마커**다. 그리고 그 기본 스코프는 — Spring 사고로 옮기자면 — **`@RequestScope`** 다. 한 요청이 들어올 때마다 의존성 함수가 새로 실행된다. 싱글톤이 *기본값이 아니다.*

이 한 줄을 처음 들으면 "그러면 매 요청마다 객체를 새로 만든다고? 비효율 아닌가?"라는 의문이 따라온다. 합리적인 의문이다. 답은 두 갈래로 갈린다. 첫째, 객체 생성 자체는 Python에서 그리 비싸지 않다. 둘째, 정말 *싱글톤*이 필요한 자원(데이터베이스 엔진, 외부 HTTP 클라이언트, ML 모델 객체)에는 `lifespan` 컨텍스트나 모듈 레벨 변수, `@lru_cache` 같은 다른 도구가 있다. *기본은 요청-스코프, 싱글톤은 명시적*이다 — 이 한 줄이 Spring과 FastAPI를 가르는 작지만 강력한 갈래다. 본격적인 해부는 4장에서 다룬다.

## 정직하게 — Spring을 떠나면서 우리가 잃는 것

매핑 표만 보면 "Spring과 FastAPI는 거의 같다"고 착각하기 쉽다. 그건 위험한 착각이다. 책의 약속을 지키려면, 이 장에서 정직한 약점 지도부터 깔아둬야 한다. 6·7장에서 본격적으로 부딪힐 충격을 미리 윤곽으로 보여주는 셈이다.

### `@Transactional`이 없다

Spring 개발자가 가장 먼저 부딪히는 벽이다. FastAPI/SQLAlchemy에는 `@Transactional` 어노테이션이 없다. 메서드 한 줄 위에 어노테이션을 붙이면 시작·커밋·롤백·격리 수준이 자동으로 처리되던 그 마법이 — 여기엔 없다.

대신 무엇이 있느냐? **명시적 begin/commit/rollback**, 또는 **컨텍스트 매니저**, 또는 **의존성 `yield` 패턴**이다. 6장에서 본문으로 보겠지만, 가장 권장되는 모양은 대략 이렇다.

```python
# 파이썬 - 트랜잭션은 명시적으로
@app.post("/orders")
async def create_order(
    payload: OrderCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    async with db.begin():           # 여기서 트랜잭션 시작·커밋
        order = Order(**payload.model_dump())
        db.add(order)
    return order
```

`async with db.begin():` 한 줄이 `@Transactional`의 자리에 들어간다. 그런데 이 한 줄을 *어디에* 놓아야 하는지가 챕터 하나의 분량이 된다. 라우트에 놓을지, 서비스 레이어에 놓을지, 의존성에 숨길지. 그리고 한 가지 더 — *`get_db()`의 finally에서 `commit()`을 호출하면 안 된다.* 그 코드는 응답이 클라이언트로 나간 뒤 실행되기 때문에, 거기서 발생하는 예외는 응답에 반영되지 않은 채 트랜잭션을 망가뜨린다. FastAPI 진영에서 흔히 밟는 함정이다. 미리 알아두면 한 번은 덜 다친다.

이 자리에 무엇을 놓아야 같은 안전성을 얻는지, 그 답은 6장에 통째로 들어간다. 지금은 한 가지 마음의 준비만 하자. **자동에서 명시로의 전환은 두뇌의 근육을 다시 짠다.** 처음엔 번거롭게 느껴진다. 익숙해지면 "어디서 트랜잭션이 열렸지?"를 추적하지 않아도 된다는 사실에서 오는 또 다른 종류의 평온함이 있다.

### Spring Security가 무료로 막아주던 것들

7장에서 본격적으로 다룰 주제지만, 이것도 윤곽만 그려두자.

`@PreAuthorize("hasRole('ADMIN')")` 한 줄. 메서드 위에 붙이면 권한 검사가 끝난다. CSRF, 세션 고정, 비밀번호 인코더 — 다 Spring Security가 기본값으로 막아주거나 제공한다. 우리는 그 안전망 위에서 비즈니스 로직만 짜면 됐다.

FastAPI에는 그런 우산이 없다. 대신 `OAuth2PasswordBearer`라는 의존성 + `python-jose` 같은 JWT 라이브러리 + 직접 짜는 `Depends(get_current_user)` 함수가 있다. 보호할 라우트마다 `Depends(get_current_user)`를 명시해서 끼워 넣는다.

이걸 듣고 "그러면 한 번 빠뜨리면 사고 나는 거 아니야?" 싶은 생각이 들었다면 — 정확한 직감이다. 한 보고에서는 6개월간의 두 프레임워크 비교에서 보안 감사 이슈가 FastAPI 7건, Spring Boot 1건이었다고 한다 ([Medium, FastAPI vs Spring Boot 6개월 비교](https://medium.com/engineering-playbook/fastapi-vs-spring-boot-i-tested-both-for-6-months-in-production-96c04f7ebabe), 한 회사의 케이스라는 단서는 붙는다). 이게 그저 FastAPI가 나쁘다는 증거일까? 그렇게만 보면 절반만 본 거다. 같은 보고를 반대로 읽은 사람도 있다 — `Depends()`는 *명시적*이어서 보호가 빠질 수 없다는 것이다. 보호는 의존성으로 선언되든지, 라우트는 공개되든지, 둘 중 하나로만 존재한다. 사라진 보호가 *없는 보호*로 자동 변신할 여지가 없다. 어느 쪽이 옳은가는 7장에서 양쪽 관점을 다 본 뒤에 결정하자. 지금은 *Spring Security의 빈자리에 무엇이 들어오는지 미리 알고 가는 것*만으로 충분하다.

한 가지 마음의 준비는 더 해두자. Spring Security 시절에 우리는 *기본 설정이 곧 안전한 기본값*이었다. CSRF 토큰, 세션 고정 방어, 비밀번호 인코더의 기본값 — 다 켜져 있었고, 끄려면 의식적으로 한 줄을 추가해야 했다. FastAPI는 *반대 방향*이다. 안전한 기본값을 *우리가 켜는* 모델이다. 그래서 7장에서 우리는 *체크리스트 사고*를 손에 익혀야 한다. "이 라우트는 인증을 거치는가? 이 입력은 검증되는가? 이 응답은 민감 정보를 흘리지 않는가?" 하나하나 묻는 손버릇이다. Spring Security가 자동으로 던지던 그 질문을, 이제 우리 손이 던진다.

### 메모리가 조용히 자라기도 한다

같은 6개월 비교 글의 한 문단이 마음에 걸린다. 한 회사의 사례에서 — 그러니까 *일반화하기 전*에 — FastAPI 서비스의 메모리가 시작 시 180MB였는데 며칠 사이 600MB까지 기어 올라갔다는 보고다. JVM 진영에서 우리는 힙덤프 도구와 GC 로그, JMX 메트릭으로 누수를 추적해 왔다. Python에는 그만큼 성숙한 도구가 있을까? 있긴 있다 — `tracemalloc`, `memray`, `py-spy` 같은 도구들. 다만 *기본으로 켜져 있지 않고*, 손에 익히는 데 시간이 든다.

이 사례를 본문에서 한 번 더 마주칠 것이다. 11장에서 도구들을 직접 손에 쥐어주려고 한다. 지금 우리에게 필요한 건 — 한 사례의 경험치로 — "Python 백엔드는 JVM처럼 알아서 누수를 알려주지 않을 수 있다"는 사실을 마음 한구석에 새겨두면 된다.

### 운영 비용이 정말 줄어드는가

같은 글이 또 한 가지 숫자를 던진다. 초기 개발은 FastAPI가 3주, Spring Boot가 5주. 그런데 6개월 누적 유지보수 시간은 FastAPI 480시간, Spring Boot 160시간. 새벽 호출 건수는 FastAPI 8번, Spring Boot 2번이었다고 한다. (같은 출처)

이 숫자를 "FastAPI는 운영이 어렵다"는 일반화로 받으면 안 된다. *한 회사의 한 케이스의 경험치*다. 다만 시사점은 있다 — **빠른 개발이 곧 낮은 총비용을 의미하지 않는다.** 초기 3주가 5주가 되지 않는 대신, 6개월 후 운영 부담이 더 클 수도 있다. 이 가능성을 정직하게 알고 가는 게 우리 약속이다. 11장에서 이 격차를 *줄이기 위해* 무엇을 해야 하는지를 다룬다.

왜 이런 격차가 생기는지 한 줄로 짐작해보자. Spring Boot가 한 줄로 띄워주던 것들 — Actuator의 헬스/메트릭, 자동 트랜잭션, Spring Security의 기본 방어, JVM의 성숙한 GC 로그 — 이 모두가 *FastAPI 진영에서는 각자의 라이브러리로 흩어져 있다*. 흩어진 부품을 직접 묶는 손길이 운영 단계에서 빠지면, 한 번씩 어딘가가 뚫린다. 9장의 관측성, 11장의 배포 운영은 그래서 단순한 매뉴얼이 아니라 *Spring Boot 한 줄의 자리에 무엇 무엇을 갖다 놓을지의 체계적 조립*이라는 성격을 띤다.

### 타입 힌트가 자바처럼 안전하다고 착각하지 말자

이건 한국 독자 특유의 함정이라 한 절을 따로 둔다. FastAPI를 보고 "Spring처럼 타입이 빡빡한 Python 프레임워크"라고 받는 인상이 흔하다. 부분적으론 맞다. 하지만 한 학술 연구가 한 줄로 정리한 사실이 있다 — 약 15%의 결함은 mypy 같은 정적 타입 체커로 막을 수 있었다([Khan et al., 2021, TSE](https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf)). 뒤집어 말하면, *85%의 결함은 타입 힌트로 막을 수 없다.*

자바의 컴파일러가 잡아주던 것을 Python에서는 — *mypy/pyright 같은 정적 검사*와 *Pydantic 런타임 검증*과 *테스트*의 세 겹을 의식적으로 깔아야 한다. 2장에서 정적 검사 도구를 손에 쥐여주고, 3장에서 Pydantic 런타임 검증을 짜고, 10장에서 테스트 짜기를 다룬다. 셋이 하나의 안전망이라는 사실을 기억해두자.

## 한국 시장의 진짜 풍경

여기서 잠시 책을 덮고 솔직한 이야기를 해보자. 한국에서 백엔드 채용 공고를 30개쯤 펴보면 어떤 그림이 나오는가? Java/Spring이 압도적이다. Kotlin/Spring이 그 옆에 있다. FastAPI는 — 있긴 있다. ML/데이터 플랫폼 직군, 스타트업 일부, 사내 어드민/툴 직군에서.

이 책은 그 진실 위에서 출발한다. *FastAPI가 Spring을 대체한다*는 약속을 하지 않는다. *Python 백엔드를 한 번도 안 짜본 Spring 출신이, 두 번째 도구함을 갖춘다*는 약속을 한다. 이 둘은 다르다.

한 한국 개발자의 velog 글이 이런 표현을 썼다. "FastAPI로 작성한 코드가 '오토바이인 척하는 자전거' 같다"고. ([koeunyeon velog](https://velog.io/@koeunyeon/FastAPI-%EC%8D%A8-%EB%B3%B8-%ED%9B%84%EA%B8%B0)) 한 사람의 의견이라는 단서는 붙지만, 이 표현이 가리키는 감각은 한국 Spring 출신 개발자가 흔히 느낄 법한 것이다 — 타입 시스템 도입으로 빡빡함을 흉내내지만, 그렇다고 Spring처럼 극적으로 안전망을 깔아주지도 않고, Ruby on Rails처럼 극적으로 간결하지도 않은 *어중간한 자리*. 이게 FastAPI가 진짜 별로라는 뜻일까? 아니다. 다만 *"무엇을 위해 이 도구를 손에 쥐는가"라는 질문에 답을 갖고 있어야 도구가 살아난다*는 신호다.

또 다른 velog 글은 FastAPI에서 Spring으로 마이그레이션한 경험을 정리하면서 한 줄을 남겼다. "복잡한 비즈니스 로직과 대규모 트래픽엔 Spring이 더 적합." ([thedev_junyoung velog](https://velog.io/@thedev_junyoung)) 이 글이 일반화의 근거는 아니지만, *한 사례의 경험치*로는 충분한 신호다. 13장에서 "언제 Spring으로 돌아가야 하는가"를 정직하게 다룰 텐데, 그 챕터는 이런 한국 사례들을 한 번 더 들여다본다.

그렇다면 우리는 왜 이 책을 읽어야 하는가? 정리해보자.

- **두 번째 도구를 갖추기 위해** — Python·ML 생태계 직결이 필요한 순간이 온다. PyTorch, HuggingFace, 데이터 파이프라인. Spring에서 이걸 우회로 갖다 쓰는 비용이 작지 않다.
- **빠른 MVP·실험 서비스를 위해** — 초기 3주에 띄울 수 있는 도구는 그 자체로 자산이다.
- **사내 어드민·툴링을 위해** — 작은 서비스 하나를 위해 Spring 풀스택을 띄우는 게 무거울 때.
- **커리어의 양다리를 위해** — 한국 채용 시장에서 Spring이 메인이라는 사실은 안 변한다. 그 옆에 FastAPI를 갖추는 것이지, *Spring을 버리는 게 아니다.*

이 책의 부제가 "Spring 사고로 FastAPI를 짓는 법"인 이유가 여기 있다. *옮긴다*가 아니라 *짓는다*. 8년 동안 쌓아온 사고는 그대로 가져간다. 그 위에 손에 잡히는 두 번째 도구를 *얹는다*.

## 이 책이 너에게 약속하는 것, 약속하지 않는 것

1장을 닫기 전에 한 번 더 마음을 맞추고 가자. 모든 책은 무엇을 *주는지*만큼이나 무엇을 *주지 않는지*가 분명해야 독자가 마음 편히 따라올 수 있다.

손에 쥐여주려는 것은 이런 것들이다.

- Spring/Spring Boot 경력자가 FastAPI를 손에 익히는 길.
- Spring과 1:1로 그려지는 영역(라우팅·DI·예외·테스트·관측성)의 매핑.
- Spring과 *결정적으로 다른* 영역(트랜잭션·보안·async·메모리)의 정직한 충돌.
- 작은 도메인 예제 12개와 통합 미니 프로젝트 한 개로 사고를 *체득*하는 호흡.
- 한국 시장에서 FastAPI와 Spring을 *둘 다* 다루는 사람이 되는 길.

반대로, 이 책이 손대지 않고 두는 자리도 있다.

- Python 언어 자체의 본격 입문. `if/for/list/dict`와 함수 정의 정도는 안다고 가정한다. 그 이상이 필요해지면 책 끝의 더 읽을거리에서 다른 책을 안내한다.
- FastAPI 모든 기능의 망라식 매뉴얼. 공식 문서가 이미 친절하다. 우리는 *Spring 사고와 부딪히는 지점*에 본문 무게를 둔다.
- ML 모델 학습. ML 서빙은 *FastAPI의 sweet spot*이라 13장 한 절로 다루지만, 모델 자체는 다른 책의 영역이다.
- 마이크로서비스 아키텍처 일반론. *한 서비스를 잘 짓는 법*에 집중한다. 분산 시스템 설계는 별도의 두께를 요한다.
- Django, Flask 같은 다른 Python 웹 프레임워크와의 비교. FastAPI 한 점에 집중한다.

이 둘의 경계를 분명히 해두면, 책을 따라가는 호흡이 한결 가벼워진다.

## 한 호흡으로 정리

지금까지 그린 그림을 한 번 정리하자. 머리에 박혀야 할 건 셋이다.

**첫째, FastAPI는 얇은 프레임워크다.** Starlette + Pydantic v2 + uvicorn의 조립. 그 위에 타입 힌트가 검증·직렬화·문서의 *단일 소스* 역할을 한다. 한 함수 한 줄이 Spring의 컨트롤러 + DTO + Validator + Swagger 어노테이션을 합친다.

**둘째, Spring과 1:1로 그려지는 영역이 의외로 많다.** 라우팅, 예외 처리, 테스트, 의존성 주입의 *형태*는 같다. 다만 *스코프*는 다르다 — FastAPI의 기본은 요청 단위다. 8년 동안 쌓은 빈 컨테이너 사고를 그대로 가져오면 손이 헛돈다.

**셋째, 결정적으로 다른 영역이 있고, 거기서 우리는 *잃는 것*이 있다.** 자동 트랜잭션, Spring Security의 안전망, JVM 운영 도구의 성숙도. 책의 절반은 이 빈자리에 *직접 손으로* 무엇을 갖다 놓을지를 다룬다. 6장의 트랜잭션, 7장의 인증, 8장의 비동기, 11장의 운영 — 이 네 장이 이 책의 진짜 무게가 실리는 자리다.

이 그림을 머리에 두고 다음 장으로 가자. 2장은 손에 흙을 묻히는 자리다. Python·uv·IDE·타입 체커를 세팅하고, 첫 FastAPI 프로젝트를 띄운다. Maven/Gradle 사고를 그대로 가져오되, 어디서 멈추고 어디서 방향을 트는지를 짚으면서. *Python 프로젝트 셋업이 왜 Java보다 더 혼란스러운가*라는 솔직한 질문으로 시작해서, *Spring Boot Initializr만큼 빠른 루틴*을 손에 익히는 게 다음 장의 약속이다.

준비됐는가? 그럼 가자.
