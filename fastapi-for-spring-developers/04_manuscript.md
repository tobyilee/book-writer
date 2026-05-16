# @Transactional이 없는 세상

## 부제
Spring 사고로 FastAPI를 짓는 법

## 저자
Toby-AI

**판본:** v1.0.0 · 2026-05-16

---

## 판권

**@Transactional이 없는 세상 — Spring 사고로 FastAPI를 짓는 법**
**판본:** v1.0.0
**발행일:** 2026-05-16
**저자:** Toby-AI
**식별자:** fastapi-for-spring-developers

### 라이선스

이 책은 [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko) 라이선스로 배포된다.

- **저작자 표시(BY):** 출처를 밝힐 것.
- **비상업적 이용(NC):** 상업적 목적으로 이용할 수 없다.
- **동일조건 변경허락(SA):** 변경·재배포 시 동일한 라이선스를 적용해야 한다.

### 출처

이 책은 Claude Code 기반 [book-writer](https://github.com/) 하네스 v1.2.0으로 작성되었다.

---

## 머리말 — Spring 출신, 너에게 보내는 초대

8년쯤 Spring으로 살았다고 해보자. `@RestController`와 `@Autowired`가 손에 박혀 있고, `@Transactional` 한 줄 위에 비즈니스 로직을 얹는 호흡이 자연스럽다. IntelliJ가 빨간 줄로 컴파일 오류를 잡아주고, Tomcat이 알아서 스레드를 굴려주고, Actuator 한 줄이면 메트릭·헬스·트레이스가 떠 있다. 익숙한 작업대다.

어느 월요일, 팀장이 슬쩍 다가와 묻는다. "이번 추천 API는 Python으로 한번 만들어보자. FastAPI 좋다던데." 인터넷 튜토리얼을 열면 함수 위에 `@app.get("/")` 한 줄. 어디서 본 모양이긴 한데 어딘가 허전하다. *내가 알고 있던 Spring 사고를 여기서도 써먹을 수 있을까? 아니면 전부 버리고 처음부터 다시 배워야 할까?*

이 책은 그 질문에서 출발한다. 답을 먼저 적어두자 — *둘 다 아니다.* 사고의 *어느 부분*은 그대로 가져가고, *어느 부분*은 무너지며, *어느 자리*에는 직접 손으로 무언가를 갖다 놓아야 한다. 이 책은 그 지도를 함께 그리는 일이다.

### 이 책이 누구를 위한 것인가

이 책은 *Spring 출신 백엔드 개발자*를 위한 책이다. 더 구체적으로는 — Java 또는 Kotlin으로 Spring Boot·Spring MVC·Spring Data JPA·Spring Security를 *프로덕션에서* 써본 사람을 향한다. 빈 컨테이너의 라이프사이클, `@Transactional`의 전파 옵션, JPA의 1차 캐시, MockMvc로 컨트롤러 테스트하는 손버릇 — 이런 게 머리에 박혀 있다는 가정으로 글이 짜인다.

반대로 — Python 자체의 입문서는 아니다. `if/for/list/dict`와 함수 정의 정도는 안다고 가정한다. 또한 FastAPI 모든 기능의 망라식 매뉴얼도 아니다. 공식 문서가 이미 친절하다. 우리는 *Spring 사고와 부딪히는 지점*에 본문 무게를 둔다.

이 책이 약속하는 것을 한 문장으로 적자면 이렇다. **8년 동안 쌓아온 Spring 사고를 그대로 가져가되, FastAPI라는 *두 번째 도구함*을 손에 넣는 일.** 이 책은 *Spring을 버리는 책이 아니라 더하는 책*이다.

### 이 책을 어떻게 읽을 것인가

세 막의 구조로 짰다.

**1막 — 친숙함의 다리(1~3장).** Spring과 *1:1로 그려지는* 영역만 골라 손을 잡아 끈다. 정체성 지도(1장), 환경 셋업(2장), 첫 라우트(3장). 이 막의 목적은 *불안 해소*다. "어, 이거 익숙하네"라고 느끼게 만든다.

**2막 — 충돌과 전환(4~8장).** Spring 사고가 더는 통하지 않는 영역으로 한 발씩 데려간다. 의존성 주입(4장)에서 워밍업한 뒤, SQLAlchemy(5장)에서 첫 충격, 트랜잭션(6장)에서 절정. 그리고 인증(7장)과 비동기(8장)가 두 번째·세 번째 충돌이다. *깨달음*의 막이다. 6→7→8장에 흐르는 통주저음 한 단어는 — *명시성*이다.

**3막 — 운영과 통합(9~13장).** 사고 모델이 정리됐으면 실전이다. 예외·관측성(9장), 테스트(10장), 배포(11장). 12장의 통합 프로젝트가 1~11장을 한 코드베이스에 묶고, 13장이 *언제 Spring으로 돌아가야 하는가*를 정직하게 짚는다.

선형 읽기를 권하지만, 각 챕터 시작에 *"이 챕터를 읽기 전 알아둘 것"* 안내를 둔 곳도 있다. 발췌 독자도 길을 찾을 수 있게 짜뒀다. 다만 4장(DI)·5장(SQLAlchemy)·6장(트랜잭션) — 이 세 장은 책의 *척추*다. 어디서 시작하든 이 셋은 한 번씩 들르길 권한다.

### 책의 약속을 다시 한 줄로

이 책의 부제가 *"Spring 사고로 FastAPI를 짓는 법"*인 이유가 여기 있다. *옮긴다*가 아니라 *짓는다*. 8년 동안 쌓아온 사고는 그대로 가져간다. 그 위에 손에 잡히는 두 번째 도구를 *얹는다*.

준비됐는가? 그럼 가자.

---

## 차례

- [1장. 왜 FastAPI, 왜 Spring 출신에게 친숙한가](#1장-왜-fastapi-왜-spring-출신에게-친숙한가)
- [2장. 개발 환경 — Maven/Gradle 마인드에서 uv·Poetry로](#2장-개발-환경--mavengradle-마인드에서-uvpoetry로)
- [3장. 첫 라우트와 Pydantic — `@RestController` × DTO를 한 줄에 녹이기](#3장-첫-라우트와-pydantic--restcontroller--dto를-한-줄에-녹이기)
- [4장. 의존성 주입 — `@Autowired`에서 `Depends()`로](#4장-의존성-주입--autowired에서-depends로)
- [5장. 데이터 접근 — JPA에서 SQLAlchemy 2.0으로](#5장-데이터-접근--jpa에서-sqlalchemy-20으로)
- [6장. 트랜잭션 — `@Transactional`이 없는 세상에서 살아남기](#6장-트랜잭션--transactional이-없는-세상에서-살아남기)
- [7장. 인증·인가 — Spring Security 없이 OAuth2/JWT](#7장-인증인가--spring-security-없이-oauth2jwt)
- [8장. 비동기와 GIL — WebFlux 사고를 코루틴으로](#8장-비동기와-gil--webflux-사고를-코루틴으로)
- [9장. 예외·로깅·관측성 — Actuator 없이](#9장-예외로깅관측성--actuator-없이)
- [10장. 테스트 — MockMvc에서 TestClient + pytest로](#10장-테스트--mockmvc에서-testclient--pytest로)
- [11장. 배포·운영 — Tomcat에서 Uvicorn + Gunicorn + 컨테이너로](#11장-배포운영--tomcat에서-uvicorn--gunicorn--컨테이너로)
- [12장. 통합 프로젝트 — 사내 태스크 관리 API + Slack 알림 봇](#12장-통합-프로젝트--사내-태스크-관리-api--slack-알림-봇)
- [13장. 언제 Spring으로 돌아가야 하는가](#13장-언제-spring으로-돌아가야-하는가)
- [에필로그 — 한 권의 호흡을 닫으며](#에필로그--한-권의-호흡을-닫으며)
- [부록 A. Spring ↔ FastAPI 매핑 한눈에](#부록-a-spring--fastapi-매핑-한눈에)
- [부록 B. 더 읽을 거리 — 큐레이션 가이드](#부록-b-더-읽을-거리--큐레이션-가이드)
- [참고문헌](#참고문헌)

---

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


---

# 2장. 개발 환경 — Maven/Gradle 마인드에서 uv·Poetry로

새 프로젝트를 시작하는 월요일 아침을 떠올려 보자. Spring Boot 쪽이라면 손에 익은 동선이 있다. IntelliJ를 열고, Spring Initializr에 접속해 Java 21, Gradle, Web, JPA, PostgreSQL, Lombok 정도를 체크하고, ZIP을 내려받아 import 하면 끝이다. `./gradlew bootRun` 한 줄로 8080 포트가 뜬다. 의존성·빌드·실행이 한 호흡으로 끝나는 이 깔끔함은 우리에게 이미 익숙해진 풍경이다.

이제 그 동선을 Python·FastAPI에서 다시 그려야 한다. 그런데 검색을 시작하면 곧 난감해진다. `python`을 쳤더니 어떤 글은 `python3`이라 쓰고, 어떤 글은 `python`이라 쓴다. 어떤 튜토리얼은 `pip install -r requirements.txt`로 시작하고, 어떤 글은 `poetry install`이라 적고, 또 어떤 글은 `uv add`라고 한다. `venv`라는 단어가 등장하는가 하면, `conda`라는 또 다른 이름도 보인다. "그래서 표준이 뭐냐"라는 질문에 누구도 한 줄로 답해주지 않는다. Spring Initializr 한 페이지로 끝나던 결정이 Python에선 네다섯 갈래로 갈라진다.

그렇다면 우리는 어디서부터 발을 디뎌야 할까. 이 안개를 함께 걷어보자. 무엇을 표준으로 고르고, 어떤 도구가 IntelliJ의 안전망을 대신해주며, `pom.xml` 자리에 무엇이 들어서는지 — 손에 익은 셋업 루틴 하나를 만들어두자. 다음 장부터 책을 끝까지 같이 갈 작업대가 거기서 만들어진다.

## Python 가상환경 — JVM 클래스패스의 부재가 만든 풍경

Java 진영에서는 클래스패스라는 단어를 외울 필요가 없을 정도로 빌드 도구가 알아서 잘 해 준다. Maven이든 Gradle이든, 의존성은 프로젝트별 `pom.xml`이나 `build.gradle`에 박혀 있고, 빌드 도구가 격리된 클래스패스를 구성해 준다. 한 머신에 Java 프로젝트가 열 개 있어도 서로의 라이브러리 버전이 충돌하는 일은 없다.

Python에는 이게 없다. 정확히 말하면 *기본값에 없다*. `pip install fastapi`라고 치면 어디에 설치될까? 답은 "현재 활성화된 파이썬 인터프리터의 site-packages"다. 그게 시스템 파이썬일 수도 있고, Homebrew로 깐 파이썬일 수도 있고, pyenv가 가리키는 파이썬일 수도 있다. 운이 나쁘면 macOS 시스템 파이썬에 라이브러리를 깔다가 OS 동작을 망가뜨릴 수도 있다. 끔찍한 일이다.

그래서 Python 개발자들은 **가상환경(virtual environment)** 이라는 우회로를 만들었다. 프로젝트마다 별도의 폴더에 파이썬 실행파일과 site-packages를 격리해 두고, 그걸 "활성화"한 셸 안에서만 그 환경의 패키지를 본다. JVM에 비유하자면, 프로젝트마다 자기 전용 JDK와 의존성 jar 묶음을 따로 두는 셈이다.

```bash
# 표준 라이브러리만으로 만드는 가상환경
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# 또는 .venv\Scripts\activate   # Windows
pip install fastapi
```

`venv`로 만든 폴더 안에 `bin/python`이 들어가 있고, 그 인터프리터를 가리키도록 PATH 우선순위가 바뀐다. 이제부터 이 셸 안에서는 `pip install`이 그 폴더에만 영향을 준다. Spring 식으로 비유하면 *프로젝트 디렉터리에 JDK를 통째로 복사해 둔 상태*다. 무겁다 싶지만, Python의 동적 본성을 생각하면 어쩔 수 없는 격리다.

문제는 가상환경만으로는 한참 부족하다는 점이다. lock 파일이 없다. `pip freeze > requirements.txt`로 의존성 목록을 박제할 수는 있지만, 같은 라이브러리의 같은 버전이라도 의존하는 *다른* 라이브러리 버전이 달라지면 빌드 재현성이 깨진다. Maven이 `pom.xml`과 lock의 역할을 함께 해 주는 데 비하면, Python 표준 도구만으로는 손이 가는 부분이 너무 많다.

> "Python 생태계는 Java보다 분절돼 있다 — Maven 1:1 대체 단일 도구는 없지만, 의존성 해상도·패키징·빌드·스캐폴딩 영역을 여러 도구가 나눠 맡는다."

이 인용은 우리가 처한 상황을 정확히 짚는다. Python의 의존성 관리는 한동안 도구가 난립한 영역이었다. 그래서 도구 선택 자체가 첫 의사결정이 된다. 골라보자.

## 도구 풍경 — pip, Poetry, uv, conda 중에 무엇을 고를까

표준 후보들을 한 줄씩 정리해 두자.

- **pip + venv**: Python 표준 라이브러리에 내장된 가장 기본 조합. lock 파일이 없고, 의존성 해상도가 단순하다. 학습용·1회성 스크립트엔 충분하지만, 팀 프로젝트엔 부족하다.
- **pip + requirements.txt**: 오래된 관행. 의존성 목록을 파일로 박제하지만, 트랜지티브 의존성까지 박제하려면 `pip freeze`로 수십~수백 줄을 적어둬야 하고, lock 파일이라 보기엔 약하다. 2026년 현재 "deprecated 취급"으로 가는 분위기다.
- **Poetry**: `pyproject.toml` + `poetry.lock`. Maven에 가장 가까운 단일 도구. 가상환경 자동 생성·lock·publish까지 한 묶음. 2020~2024년 사이 사실상 표준이었다.
- **uv** (2024년 등장, Rust 기반): Poetry의 후속 주자. "Poetry보다 100배 빠른 해상도"라는 거친 자랑이 빈말이 아니다. `pyproject.toml`을 그대로 쓰면서 lock·실행·툴체인까지 다 한다.
- **conda / mamba**: 데이터 과학 진영의 표준. 시스템 라이브러리(C/C++ 바이너리)까지 패키지로 관리한다. 백엔드 서비스엔 과한 도구다.

그렇다면 어디에 손을 얹어야 할까. 답을 먼저 적어두자. **이 책은 uv를 기본으로 가르친다.** 이유는 세 가지다.

첫째, 빠르다. Poetry로 의존성 해상도를 돌리면 작은 프로젝트도 수십 초가 걸린다. uv는 같은 작업을 1초 안에 끝낸다. CI 빌드 시간이 절반 이하로 줄어들고, 로컬 개발에서도 `add` 한 번에 기다리는 시간이 없다.

둘째, 표준 포맷을 그대로 쓴다. uv는 `pyproject.toml`을 읽고 쓴다 — 즉, Poetry로 시작한 프로젝트를 uv로 옮기는 데 추가 변환이 필요 없다. 의존성 명세는 Python 생태계의 공식 표준 `pyproject.toml`(PEP 621)에 따른다.

셋째, 흐름이 기울었다. 2025~2026년 사이 새로 시작하는 Python 프로젝트의 다수가 uv를 기본 도구로 채택하고 있고, FastAPI 진영의 영향력 있는 글들도 점차 uv 예시로 갈아타는 중이다. *이미 굳어진 표준*보다 *지금 굳어지고 있는 표준*에 손을 얹는 편이 낫다.

> "uv는 Rust 기반으로 Poetry의 100배 빠른 의존성 해상을 제공한다. 0.33ms에 의존성 해상, 1ms에 패키지 설치."

다만 한 가지를 분명히 해두자. 회사에서 이미 Poetry를 쓰고 있다면, 그건 그대로 두는 게 맞다. 도구 통일을 깨면서까지 uv로 갈아탈 동기가 필요한 건 아니다. 이 책의 예제는 uv로 짜지만, 명령어 한 줄 한 줄을 Poetry 대응표로 같이 적어 둘 테니 옮겨 적기 어렵지 않다.

## uv 설치와 첫 만남

설치는 한 줄이다. 공식 인스톨러를 받아 실행한다.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치가 끝나면 새 셸을 띄우고 버전을 확인해 보자.

```bash
$ uv --version
uv 0.5.x   # (사실 확인 필요 — 책 출간 시점 최신 버전으로 갱신)
```

uv가 하나 더 해주는 일이 있다. **파이썬 인터프리터 자체도 uv가 관리해 준다.** 시스템에 Python 3.12가 없어도 `uv python install 3.12` 한 줄로 다운로드·설치까지 끝난다. Java로 치면 jenv나 sdkman이 하던 일을 빌드 도구가 직접 떠맡은 셈이다. 이게 의외로 큰 편의다 — 동료 머신에 어떤 파이썬이 깔려 있는지 신경 쓰지 않아도 된다.

```bash
$ uv python install 3.12
$ uv python list
cpython-3.12.7-macos-aarch64-none    <download available>
cpython-3.11.10-macos-aarch64-none   <download available>
...
```

## 첫 FastAPI 프로젝트 — Spring Initializr 동선의 Python 버전

이제 손에 익혀 두자. 새 프로젝트를 만드는 동선이다. 빈 폴더에서 시작한다.

```bash
$ mkdir hello-fastapi && cd hello-fastapi
$ uv init
Initialized project `hello-fastapi`
```

`uv init`이 만든 결과를 확인해 보자.

```text
hello-fastapi/
├── .python-version       # 사용할 파이썬 버전 (예: 3.12)
├── .gitignore
├── README.md
├── hello.py              # 샘플 스크립트
└── pyproject.toml        # 프로젝트 메타데이터 + 의존성
```

`pyproject.toml`이 우리 책의 `pom.xml`이다. 처음 열어보면 이렇게 생겼다.

```toml
[project]
name = "hello-fastapi"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

Maven `pom.xml`과 1:1로 짚어 두자.

| Maven `pom.xml` | `pyproject.toml` | 비고 |
|---|---|---|
| `<groupId>` | (없음) | Python은 패키지 이름 한 단계만 |
| `<artifactId>` | `[project] name` | 패키지 이름 |
| `<version>` | `[project] version` | 동일 의미 |
| `<description>` | `[project] description` | 동일 |
| `<properties><java.version>` | `[project] requires-python` | 인터프리터 버전 제약 |
| `<dependencies>` | `[project] dependencies` | 런타임 의존성 목록 |
| `<dependency><scope>test</scope>` | `[dependency-groups] dev` (uv) 또는 `[project.optional-dependencies]` | 개발 전용 의존성 |
| `<build><plugins>` | `[tool.<도구이름>]` 섹션 | 빌드·도구 설정은 도구별 네임스페이스에 |
| `mvn-wrapper.properties` | `.python-version` + `uv.lock` | 환경·의존성 박제 |

`pom.xml`이 한 파일에 다 담던 정보가 `pyproject.toml` 한 파일에 모인 셈이다. 보일러플레이트가 훨씬 짧다. XML이 아니라 TOML이라 사람이 직접 편집해도 부담이 없다.

이제 FastAPI와 ASGI 서버를 추가하자.

```bash
$ uv add fastapi 'uvicorn[standard]'
Resolved 14 packages in 320ms
Prepared 14 packages in 412ms
Installed 14 packages in 71ms
 + fastapi==0.115.x
 + uvicorn==0.32.x
 ...
```

이 한 줄이 무엇을 했는지 보자. 첫째, `pyproject.toml`의 `dependencies`에 `fastapi`와 `uvicorn[standard]`이 추가됐다. 둘째, 프로젝트 루트에 `.venv/` 폴더가 생기고 그 안에 격리된 파이썬과 패키지들이 깔렸다. 셋째, `uv.lock` 파일이 생성됐다 — `package-lock.json`이나 `poetry.lock`과 같은 역할이다. 트랜지티브 의존성까지 정확한 버전으로 박제된다. 이걸 git에 커밋해 두면 동료 머신에서도 정확히 같은 환경이 재현된다.

`uvicorn[standard]`의 `[standard]`는 "표준 옵션 묶음으로 깔아달라"는 표시다. uvloop, httptools, websocket 라이브러리 같은 *성능에 영향을 주는 선택적 의존성*이 함께 깔린다. Spring Boot의 starter 패키지를 떠올리면 된다 — `spring-boot-starter-web` 하나가 Tomcat, Jackson, Validation을 묶어 끌어오듯이.

이제 hello world를 한번 띄워보자. `hello.py` 자리에 `main.py`를 만들고 다음을 적자.

```python
# main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": "fastapi"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

띄우는 명령어다.

```bash
$ uv run uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/.../hello-fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12347]
INFO:     Application startup complete.
```

브라우저로 `http://127.0.0.1:8000/`를 열면 `{"hello": "fastapi"}`가 보인다. `http://127.0.0.1:8000/items/42?q=test`로 가면 `{"item_id": 42, "q": "test"}`가 나온다.

여기서 멈추지 말고 한 가지 더 보자. **`http://127.0.0.1:8000/docs`** 에 접속해 보자. Swagger UI가 떠 있다. 우리가 한 줄도 설정하지 않았는데, FastAPI는 `app`에 등록된 라우트들을 읽어 OpenAPI 스펙을 만들고 그걸 Swagger UI로 보여준다. `springdoc-openapi`를 의존성에 추가하고 어노테이션을 더 다는 단계가 통째로 사라진 셈이다. Spring 출신이 처음 `/docs`를 마주하면 자연스럽게 "어, 이거 진짜 끝났네?" 같은 반응이 나온다. 우리도 그 감각을 잠시 음미해 두자.

왜 `uv run`을 앞에 붙였을까? *가상환경 활성화를 건너뛰기* 위해서다. `source .venv/bin/activate`를 매번 치지 않아도 `uv run <cmd>`가 알아서 그 환경 안에서 명령어를 실행해 준다. 셸을 새로 띄울 때마다 활성화를 신경 쓰지 않아도 되는 게 의외로 큰 편의다.

청유형으로 한 줄 더 권하자. 이 워크플로우를 **새 셸 → `cd` → `uv run`** 으로 통일해 두자. `activate`/`deactivate`의 두 단계 의식을 머릿속에서 지우는 편이 낫다.

## 의존성 그룹 — 개발 의존성을 어디에 둘 것인가

Maven에서는 `<scope>test</scope>`를 붙여 개발·테스트 전용 의존성을 분리했다. uv에는 그것이 `dependency-groups`다.

```bash
$ uv add --dev pytest httpx
```

`pyproject.toml`을 다시 열어 보면 새 섹션이 생긴다.

```toml
[project]
name = "hello-fastapi"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
]

[dependency-groups]
dev = [
    "pytest>=8",
    "httpx>=0.27",
]
```

운영 빌드(예: 컨테이너 이미지)에선 `uv sync --no-dev`로 개발 의존성을 빼고 깐다. 테스트 컨테이너에선 `uv sync` 한 줄로 다 깐다. Maven의 `mvn package -DskipTests` 자리에 이 옵션이 들어선다.

## Poetry로 같은 일을 한다면

Poetry를 쓰는 팀에 합류했다면 흐름은 거의 같다. `uv init` 자리에 `poetry new --name`, `uv add` 자리에 `poetry add`, `uv run` 자리에 `poetry run`이 들어선다. 동사 한 단어만 바꿔 끼우면 되니, 표 한 장으로 정리해 두면 머리에 박힌다.

| 동작 | uv | Poetry | pip + venv |
|---|---|---|---|
| 새 프로젝트 | `uv init` | `poetry new <name>` | `mkdir && python -m venv .venv` |
| 의존성 추가 | `uv add fastapi` | `poetry add fastapi` | `pip install fastapi` |
| 개발 의존성 추가 | `uv add --dev pytest` | `poetry add --group dev pytest` | `pip install pytest` (구분 없음) |
| 의존성 동기화 | `uv sync` | `poetry install` | `pip install -r requirements.txt` |
| 명령 실행 | `uv run uvicorn ...` | `poetry run uvicorn ...` | `source .venv/bin/activate && uvicorn ...` |
| lock 파일 | `uv.lock` | `poetry.lock` | (없음) |
| 의존성 명세 | `pyproject.toml` | `pyproject.toml` | `requirements.txt` |

이 책의 본문 예제는 일관성을 위해 uv 명령어로 적는다. Poetry 사용자는 이 표를 옆에 두고 한 단어씩 갈아 끼우자. 결과는 똑같다.

## 정적 안전망 — IntelliJ Inspections의 빈자리를 채우기

Spring으로 작업할 때 우리가 의존하는 안전망 한 줄을 떠올려 보자. IntelliJ가 빨간 줄로 표시해 주는 그 *컴파일 시점*의 검증이다. 변수 타입이 안 맞으면 빨간 줄, null 가능성이 의심되면 노란 줄, Lombok이 만든 메서드까지 추적해 자동완성이 떠 준다. 이 안전망이 있다는 사실 자체가 우리의 코딩 호흡을 만들어 왔다.

Python에는 컴파일러가 없다. 그게 곧 재앙은 아니다. 다만, *컴파일러가 자동으로 해 주던 일을 우리 손으로 도구 체인에 박아 둬야* 한다. 다행히 좋은 도구들이 있다. 셋팅을 해 두자.

### 타입 체커 — mypy 또는 pyright

Python의 타입 힌트는 *런타임에는 강제되지 않는* 메모다. 실제 검사는 별도 정적 분석기가 한다. 후보는 두 개다.

- **mypy** — Python 진영의 전통 강자. Dropbox 출신. 규칙이 표준에 가깝다.
- **pyright** — Microsoft가 만들고 VSCode의 Pylance 확장에 들어가 있다. 더 빠르고, 추론이 더 똑똑한 편이다.

이 책의 예제는 **pyright**를 기본 권장으로 적는다. 이유는 두 가지. 첫째, VSCode를 쓰면 이미 깔려 있는 거나 마찬가지다. 둘째, 추론이 mypy보다 적극적이라 *타입 힌트를 덜 적어도* 비슷한 안전망을 만들어준다 — Python의 동적 본성과 더 잘 어울린다. PyCharm을 쓰는 독자라면 PyCharm의 내장 타입 분석이 mypy보다 강력하니, mypy를 굳이 함께 돌릴 필요는 없다.

설치해보자.

```bash
$ uv add --dev pyright
$ uv run pyright main.py
0 errors, 0 warnings, 0 informations
```

`pyproject.toml`에 설정을 더하자.

```toml
[tool.pyright]
include = ["src", "tests"]
pythonVersion = "3.12"
typeCheckingMode = "standard"   # off | basic | standard | strict
reportMissingTypeStubs = false
```

처음부터 `strict`로 두면 학습 단계에서 너무 자주 빨간 줄이 떠 좌절감이 생긴다. `standard`로 시작해서 익숙해진 뒤에 올리는 편이 낫다.

> "약 15%의 결함은 mypy 같은 타입 체커로 막을 수 있었다."

이 숫자가 무엇을 말해주는가? 분명하다. Python의 타입 힌트는 *Java의 컴파일 강제 수준*은 아니지만, 그래도 6개 중 하나는 출시 전에 막아준다. 무료 안전망이라면 깔아두는 편이 낫다.

### 린트와 포맷 — ruff 하나로 끝낸다

Java 진영에선 Checkstyle, SpotBugs, Spotless를 따로 깐다. Python 진영도 한동안 flake8, pylint, isort, black을 따로 깔아 썼다. 그런데 2024년부터 흐름이 갈렸다. **ruff** 하나가 그 전부를 갈아엎었다.

ruff는 Rust로 만든 린터+포매터다. flake8 룰의 거의 전부를 흡수했고, isort를 흡수했고, 최근 버전부터는 black의 포매팅도 흡수했다. *하나의 도구로 린트와 포맷을 다 끝낸다*. 게다가 기존 도구보다 10~100배 빠르다.

```bash
$ uv add --dev ruff
$ uv run ruff check .          # 린트
$ uv run ruff format .         # 포맷
```

`pyproject.toml`에 기본 설정을 두자.

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E", "F",       # pycodestyle, pyflakes — 기본 정적 검사
    "I",            # isort — import 정렬
    "B",            # bugbear — 잘 알려진 버그 패턴
    "UP",           # pyupgrade — 옛 문법 자동 업그레이드
    "SIM",          # 단순화 가능한 코드
]
ignore = ["E501"]   # 라인 길이는 포매터가 책임

[tool.ruff.format]
quote-style = "double"
```

손에 익혀 두자. 매일 코드를 저장할 때마다 IDE가 알아서 `ruff format`을 돌리도록 IDE 설정 한 군데를 만져 두는 편이 낫다. 코드 리뷰에서 "들여쓰기 4칸 vs 2칸" 같은 다툼이 사라진다.

### Pre-commit 훅 — 깔끔한 시작

마지막으로 한 가지를 더 박아 두자. `.pre-commit-config.yaml`이다. 커밋 직전에 ruff와 pyright가 자동으로 돌게 한다. Java 진영에선 `gradle build`가 커밋 전에 돌아주길 기대하는 그 자리다.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: uv run pyright
        language: system
        types: [python]
        pass_filenames: false
```

```bash
$ uv add --dev pre-commit
$ uv run pre-commit install
```

이제 `git commit`을 할 때마다 ruff가 자동 포맷·자동 수정하고, pyright가 타입을 검사한다. 안전망이 한 단계 올라간다.

## IDE 셋업 — PyCharm 또는 VSCode

도구가 다 깔렸으면 이제 IDE다. 후보는 두 개로 좁히자.

### PyCharm

JetBrains 진영이 익숙하다면 PyCharm Professional이 가장 빠른 길이다. IntelliJ IDEA와 같은 토대 위에 있어, 단축키·검색·리팩토링이 그대로 옮겨진다. 추가로 해 둘 일은 두 가지다.

1. **인터프리터 지정**: Settings → Project → Python Interpreter → "Add Interpreter" → "Add Local Interpreter" → "Existing" → 프로젝트 폴더의 `.venv/bin/python` 선택. IntelliJ에서 JDK를 잡아주던 화면이다.
2. **Ruff·Pyright 통합**: Settings → Tools → External Tools 또는 Ruff 플러그인을 설치. 저장할 때마다 자동 포맷이 돌도록 켜 둔다.

### VSCode

VSCode를 쓴다면 다음 확장을 깔자.

- **Python** (Microsoft) — 기본 파이썬 지원
- **Pylance** (Microsoft) — pyright 기반의 IntelliSense·자동완성
- **Ruff** (Astral) — ruff 린터·포매터 통합

`.vscode/settings.json`에 다음을 적어 두면 손에 익은 흐름이 만들어진다.

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": false,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "python.analysis.typeCheckingMode": "standard",
  "python.analysis.diagnosticMode": "workspace"
}
```

`python.terminal.activateEnvironment`를 끄는 이유는 우리가 `uv run`을 쓰기 때문이다. VSCode가 셸을 띄울 때마다 가상환경을 활성화하려 들면 `uv run`과 충돌해 *이중 활성화* 같은 묘한 상태가 생긴다. 한 번 빠지면 디버깅이 진짜 번거롭다. 끄는 편이 낫다.

## 프로젝트 구조의 첫 풀그림

마지막으로 한 그림만 손에 쥐고 가자. 다음 장부터 본격적으로 쓰게 될 폴더 구조의 *최소 형태*다. 5장에서 다시 본격적으로 다루지만, 일단 손에 그림을 하나 갖자.

```text
hello-fastapi/
├── .venv/                  # uv가 만든 가상환경 (gitignore)
├── .python-version
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml          # pom.xml 자리
├── uv.lock                 # 의존성 lock (git 커밋)
├── README.md
├── src/
│   └── app/
│       ├── __init__.py
│       └── main.py         # FastAPI 진입점
└── tests/
    ├── __init__.py
    └── test_main.py
```

`src/` 레이아웃을 권장하는 이유는 두 가지다. 첫째, 패키지 root와 프로젝트 root를 분리해서 *우연한 import 사고*를 막아준다. 예컨대 `pyproject.toml`이 있는 폴더를 통째로 PYTHONPATH에 더하는 IDE 설정이 들어가도, `src/`를 사이에 두면 테스트 코드가 깔지 않은 라이브러리를 우연히 import 해버리는 사고를 방지한다. 둘째, Spring의 `src/main/java`와 `src/test/java`라는 분리에 익숙한 우리에게 더 정직한 모양이다.

`pyproject.toml`에 한 줄을 더해 src 레이아웃을 알리자.

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/app"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

`hatchling`은 uv가 기본으로 추천하는 빌드 백엔드다. Maven 진영의 빌드 플러그인 자리다.

이제 `main.py`를 `src/app/main.py`로 옮기고, 실행 명령을 살짝 바꾸자.

```bash
$ uv run uvicorn app.main:app --reload --app-dir src
```

`--app-dir src`는 "import 경로의 시작점을 `src/`로 잡으라"는 표시다. Spring으로 치면 `--main-class` 옵션 자리에서 패키지 경로를 잡아주는 것과 같다.

## 마무리

여기까지 따라왔으면, 우리는 다음 장부터 이 작업대를 그대로 쓸 준비가 됐다. 정리해 보자.

- 의존성·실행 도구는 **uv**를 기본으로, Poetry는 옆에 대응표로 두자.
- `pom.xml` 자리에는 **pyproject.toml**이 들어선다. 한 파일로 메타데이터·의존성·도구 설정이 다 모인다.
- 컴파일러의 안전망은 **pyright + ruff + pre-commit**의 3중 체인으로 만든다. mypy는 선택 사항.
- 가상환경을 매번 활성화·해제하는 의식은 머릿속에서 지우자. **`uv run`** 한 단어가 그 역할을 떠맡는다.
- 폴더는 **`src/` 레이아웃 + `tests/` 분리**로 시작한다. Spring의 `src/main`·`src/test` 분리와 정신적 모양이 같다.

이게 우리의 *Initializr*다. 새 FastAPI 프로젝트가 필요할 때마다 위 단계들을 다섯 줄짜리 셸 스크립트로 묶어두면, IntelliJ에서 Spring Initializr 메뉴를 클릭하던 그 동선과 손에서 느껴지는 무게가 거의 같아진다.

다음 장에선 이 작업대 위에 첫 라우트를 짓는다. `@RestController` + `@RequestBody UserDto` + `@Valid`의 삼중주가 FastAPI의 한 함수로 어떻게 녹아드는지를 본다. 거기서 우리가 처음으로 "어, 이건 진짜 짧다"의 체감을 가질 차례다.


---


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


---

# 4장. 의존성 주입 — `@Autowired`에서 `Depends()`로

이런 장면을 상상해보자. Spring 프로젝트에서 컨트롤러 한 개를 새로 만든다. 손이 먼저 움직인다.

```java
// 자바 - Spring Boot
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }
    // ...
}
```

머리가 굳이 의식하지 않는다. *생성자에 받아두면 빈 컨테이너가 알아서 채워준다.* `UserService`는 어딘가 `@Service`가 붙은 채로 등록돼 있고, 그게 의존하는 `UserRepository`는 또 어딘가 `@Repository`가 붙어 있다. 우리는 그 그래프를 *그릴 줄도* 알고, 동시에 *그리지 않을 줄도* 안다. 컨테이너에게 맡기면 되니까. 8년 동안 손에 익은 패턴이다.

그러다 FastAPI 튜토리얼을 열면 처음 보는 모양과 마주친다.

```python
# 파이썬 - FastAPI
@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    svc: Annotated[UserService, Depends(get_user_service)],
):
    return svc.find(user_id)
```

`Depends(get_user_service)`. 클래스가 없다. `@Autowired`도 없다. 의존성이 *함수 파라미터 자리*에 들어와 있다. 그리고 그 파라미터의 값은 — 컨테이너가 채워주는 게 아니라 — `get_user_service`라는 *함수가 호출돼서* 만들어진다.

처음 만져보면 좀 낯설다. *컨테이너가 어디 있지? 빈 정의는 어디서 하지? 어디서 그래프를 짜지?* 답은 한 줄로 정리된다. **그래프를 짜는 자리가 없다.** 함수의 시그니처가 그래프 그 자체다. 시작 시점에 한 번에 짜는 것도 아니다. 매 요청마다 다시 풀린다.

이 차이가 코드를 어떻게 바꾸는지, 그 바뀐 형태가 Spring 사고와 어디서 맞물리고 어디서 멀어지는지를 차근차근 만져보자.

## `Depends()`는 함수 파라미터의 마커다

먼저 가장 작은 예제부터 보자.

```python
# 파이썬 - 단일 의존성
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_user_repo() -> UserRepository:
    return UserRepository()

@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    repo: Annotated[UserRepository, Depends(get_user_repo)],
):
    return repo.find(user_id)
```

이 코드의 흐름을 한 번 따라가 보자. `GET /users/42` 요청이 들어온다. FastAPI는 `read_user` 함수의 시그니처를 본다. `user_id: int`는 경로 변수다. `repo: Annotated[UserRepository, Depends(get_user_repo)]`는 — `Depends()` 마커가 붙어 있으니 — *의존성*이다. FastAPI가 `get_user_repo()`를 호출하고, 그 반환값을 `repo` 자리에 넣는다. 그리고 나서야 `read_user`의 본문이 실행된다.

Spring 사고로 옮기면 `get_user_repo`가 곧 `@Bean` 메서드에 가깝다. 빈을 *어떻게 만드는지* 알려주는 팩토리 함수다. 다만 결정적 차이가 두 가지 있다.

**첫째, `Depends()`는 함수 파라미터에 *마커*로 붙는다.** 클래스 멤버 변수에 붙는 `@Autowired`나 생성자의 매개변수가 아니다. *함수마다* 매번 명시한다.

**둘째, FastAPI에는 별도의 빈 컨테이너가 없다.** Spring처럼 `ApplicationContext`가 그래프를 들고 있는 게 아니다. 각 라우트의 시그니처가 *자기 그래프*를 매번 묘사한다. 그래프는 라우트 호출 시점에 한 번 풀리고 사라진다.

이 둘이 무엇을 가져오는가? 좋은 면은 — 그래프가 *언제나 코드 위에 보인다는 것*이다. 마법이 적다. "이 `UserService`는 어디서 와?"라는 질문에 대한 답이 *같은 줄*에 적혀 있다. 무거운 면은 — 같은 의존성을 여러 라우트가 쓸 때 *같은 줄을 반복해서 적어야 한다는 것*이다. 이 반복을 어떻게 줄이는지가 한 절의 무게를 가져간다(*Annotated 타입 별칭* 절에서 다시 만난다).

## 중첩 의존성 — 그래프는 알아서 풀린다

의존성이 하나뿐이면 매력이 약하다. *그래프*가 그려지는 자리에서 진짜 매력이 나온다.

```python
# 파이썬 - 중첩 의존성
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)

@app.get("/users/{user_id}")
def read_user(
    user_id: int,
    svc: Annotated[UserService, Depends(get_user_service)],
):
    return svc.find(user_id)
```

요청이 들어오면 FastAPI는 그래프를 거꾸로 풀어 나간다. `read_user`가 `get_user_service`를 필요로 한다. `get_user_service`는 `get_user_repo`를 필요로 한다. `get_user_repo`는 `get_db`를 필요로 한다. 잎에서 뿌리까지 거슬러 올라가서, 뿌리부터 다시 내려오면서 차례로 만든다.

Spring 사고로 옮기자면 `@Component` 그래프 + 생성자 주입과 거의 1:1이다. 다른 점은 — 그래프 *명세*의 자리다. Spring에서는 `@Component`/`@Service`/`@Repository` 어노테이션이 컨테이너에게 *클래스 단위로* 명세를 준다. 컨테이너가 시작 시점에 그래프를 *조립*한다. FastAPI에서는 각 함수의 *시그니처 자체*가 그래프 명세다. 시작 시점이 따로 없다. 라우트 호출 시점에 그때그때 풀린다.

이게 비효율 아닐까 싶은 의문이 따라온다 — 합리적이다. 답은 두 갈래다. 첫째, 의존성 함수의 호출 자체는 Python에서 그리 비싸지 않다. 그래프가 *깊어도* 함수 몇 개 호출하는 비용이다. 둘째, *비싼* 자원(데이터베이스 엔진, HTTP 클라이언트, ML 모델)은 매 요청마다 만들지 않는다 — `lifespan`이나 모듈 상수에 한 번만 만들어두고, 그걸 *얇은 의존성 함수가 가져다 쓴다*. 이 패턴은 잠시 뒤 *싱글톤이 필요할 때* 절에서 본격적으로 다룬다.

## 기본 스코프는 요청 단위, 한 요청 안에서는 캐시된다

1장에서 한 번 짚었지만 다시 가져오자. **FastAPI 의존성의 기본 스코프는 요청 단위다.** 한 요청이 들어오면 의존성 함수들이 실행되고, 응답이 나가면 모두 정리된다.

그런데 한 요청 안에서 같은 의존성이 *여러 번* 필요한 경우는 어떨까? 위 그래프를 예로 들자. `get_user_service`도 DB가 필요할 수 있다. `get_user_repo`도 DB가 필요하다. 둘 다 `Depends(get_db)`를 명시하면 — *DB 세션이 두 개 만들어지는 걸까?*

답은 아니다. **같은 요청 내에서 같은 의존성은 한 번만 실행되고 결과가 재사용된다.** FastAPI가 요청-스코프 캐시를 가지고 있다.

```python
# 파이썬 - 한 요청 내 캐시
def get_request_id() -> str:
    rid = uuid4().hex
    print(f"새 요청 ID 발급: {rid}")   # 한 요청에 한 번만 출력된다
    return rid

def use_a(rid: Annotated[str, Depends(get_request_id)]):
    return f"A: {rid}"

def use_b(rid: Annotated[str, Depends(get_request_id)]):
    return f"B: {rid}"

@app.get("/check")
def check(
    a: Annotated[str, Depends(use_a)],
    b: Annotated[str, Depends(use_b)],
):
    return {"a": a, "b": b}   # a와 b의 rid가 같다
```

`use_a`와 `use_b`가 각각 `get_request_id`에 의존하지만, 한 요청 안에서 `get_request_id`는 *한 번만* 호출된다. `use_a`가 받은 `rid`와 `use_b`가 받은 `rid`는 같은 문자열이다.

이게 좋은 이유는 명백하다. *한 요청 안에서 일관된 컨텍스트*가 보장된다. 같은 DB 세션, 같은 요청 ID, 같은 현재 사용자. 여러 서비스가 한 요청 안에서 의존성을 공유해도 일관성이 깨지지 않는다.

Spring의 `@RequestScope`와 정확히 같은 모델이라고 생각하면 이해가 쉽다. 다른 점은 — Spring에서 `@RequestScope`는 *명시적 선언*이고, FastAPI에서는 *기본값*이라는 점이다. 그래서 우리가 의식적으로 "이건 매 요청마다 새로 만들어야 해" 같은 결정을 따로 내릴 필요가 없다. 기본이 그렇다.

다만 한 가지 함정을 짚고 가자. **캐시는 "같은 의존성 함수"를 기준으로 한다.** 같은 일을 하는 함수가 *둘*이면 — 캐시되지 않는다. 우연한 함수 두 개로 같은 DB를 두 번 열어버리지 않으려면, *한 도메인은 한 의존성 함수로 모은다*는 손버릇이 안전하다.

## 싱글톤이 필요할 때 — `lifespan`, 모듈 상수, `@lru_cache`

요청-스코프가 기본이라는 말은 — *싱글톤이 필요한 자원은 의식적으로 만들어야 한다*는 뜻이다. Spring처럼 자동으로 싱글톤이 되지 않는다.

세 가지 도구가 있다. 어느 자원을 어디에 둘지, 손에 익혀두면 평생 쓴다.

### `lifespan` — 애플리케이션 수명에 묶인 자원

가장 권장되는 모양이다. FastAPI 인스턴스의 *수명 전체*에 한 번만 만들어지고, 종료 시 정리되는 자원.

```python
# 파이썬 - lifespan으로 싱글톤 자원 관리
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine("postgresql+asyncpg://...")
    app.state.engine = engine
    yield                              # 여기서 앱이 요청을 받는다
    await engine.dispose()             # 종료 시 정리

app = FastAPI(lifespan=lifespan)
```

`yield` 위쪽이 시작 단계, 아래쪽이 종료 단계다. Spring의 `@PostConstruct` + `@PreDestroy`를 한 함수에 합친 모양이다.

엔진을 `app.state`에 두면, 의존성 함수에서 꺼내 쓸 수 있다.

```python
# 파이썬 - lifespan 자원을 의존성에서 꺼내기
from fastapi import Request

async def get_db(request: Request) -> AsyncSession:
    engine = request.app.state.engine          # lifespan에서 만든 싱글톤
    async with AsyncSession(engine) as session:
        yield session
```

엔진은 하나. 세션은 매 요청마다 새로. 자원의 *수명*이 자원의 *스코프*와 어떻게 어긋나는지 보이는가? 이 어긋남을 `lifespan` + `Depends`의 조합으로 깔끔하게 표현한다.

### 모듈 레벨 변수 — 가장 간단한 싱글톤

Python에서 모듈은 한 번만 import된다. 그래서 모듈 레벨 변수는 *자동으로* 싱글톤이다.

```python
# 파이썬 - settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str

settings = Settings()           # 모듈 import 시 한 번만 만들어진다
```

```python
# 파이썬 - 어디서든 import해서 쓰면 같은 객체
from app.settings import settings

@app.get("/info")
def info():
    return {"db": settings.database_url}
```

Spring의 `@Value("${...}")` 또는 `@ConfigurationProperties`에 해당한다. 설정값, 상수, *변하지 않는 자원*에 잘 어울린다. 7장에서 `pydantic-settings`를 정식으로 소개할 때 다시 만난다.

### `@lru_cache` — 늦은 싱글톤

함수의 결과를 캐싱하는 표준 라이브러리 도구다. 의존성 함수와 합치면 — 첫 호출 때 만들고, 그 다음부터는 캐시된 객체를 *재사용*한다.

```python
# 파이썬 - @lru_cache로 무거운 객체 캐싱
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()           # 첫 호출에만 실행. 그 뒤로는 캐시

@app.get("/info")
def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {"db": settings.database_url}
```

이 패턴의 장점은 — *의존성 형태로 통일된다*는 점이다. 모든 자원을 `Depends`로 받으면 테스트할 때 *오버라이드*가 일관되게 적용된다. 잠시 뒤 *테스트 오버라이드* 절에서 만난다.

### 셋을 어떻게 골라 쓰나

| 자원 성격 | 도구 | 예 |
|---|---|---|
| 앱 수명에 묶이고 정리 단계가 있음 | `lifespan` | DB 엔진, HTTP 클라이언트 풀, ML 모델 |
| 설정값·상수·간단한 객체 | 모듈 레벨 변수 | `settings`, 상수 사전 |
| 테스트에서 갈아끼고 싶은 무거운 객체 | `@lru_cache` + `Depends` | 외부 API 클라이언트, 캐시 클라이언트 |

세 도구가 *겹친다*는 느낌이 들 텐데, 사실 겹친다. 어느 걸 골라도 동작은 한다. 다만 *테스트하기 좋은가*가 갈래를 만든다. 모듈 레벨 변수는 테스트에서 *몽키 패치*가 필요하다. `Depends`를 거치면 `app.dependency_overrides` 한 줄이면 끝난다.

## `yield` 의존성 — 라이프사이클 자원의 우아한 처리

지금까지 본 의존성 함수는 *값을 만들어 반환*했다. 그런데 *시작과 끝이 있는* 자원은 — 만들고 쓰고 닫는 — 어떻게 다룰까?

`yield`를 쓴다.

```python
# 파이썬 - yield 의존성
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session                  # 라우트에 세션 전달
        finally:
            await session.close()          # 라우트가 끝난 뒤 정리
```

함수가 *생성기*가 된다. `yield` 위쪽이 *셋업*, 아래쪽이 *틴다운*이다. `try/finally`를 써서 라우트에서 예외가 나도 정리가 보장된다.

Spring 사고로 옮기자면 — `@Transactional` 어노테이션이 메서드 위에 붙어 *시작·커밋·롤백·닫기*를 자동으로 처리해주던 것과 유사한 라이프사이클을, *의존성 함수의 `yield` 한 줄로* 풀어쓴 모양이다. 다른 점은 — 트랜잭션 *경계*가 자동이 아니라는 것. 6장 트랜잭션에서 이 차이가 한 챕터를 가져간다.

여기서 *한 가지 함정*을 짚고 가야 한다. **`finally`에서 `commit`을 호출하면 안 된다.**

왜냐? 의존성 `yield`의 `finally`는 *응답이 클라이언트로 나간 뒤*에 실행되기 때문이다. 그 시점에 예외가 나면, *응답에는 이미 200이 찍혔는데 트랜잭션은 실패한 상태*가 된다 ([GitHub fastapi/discussions/6452](https://github.com/fastapi/fastapi/discussions/6452)). 한 보고서가 *FastAPI 진영에서 가장 흔한 함정 중 하나*라고 꼽은 이유다.

권장 패턴은 — 세션은 `yield`로 *열고 닫기*만 의존성에서 처리하고, 커밋은 *라우트 또는 서비스 레이어에서 명시적으로*. 6장에서 본격적으로 풀어보겠지만 윤곽은 이렇다.

```python
# 파이썬 - 권장 패턴 (윤곽)
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session                  # 닫기는 컨텍스트 매니저가 알아서

@app.post("/orders")
async def create_order(
    payload: OrderCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    async with db.begin():             # 트랜잭션 경계는 여기서 명시
        order = Order(**payload.model_dump())
        db.add(order)
    return order
```

`get_db()`는 세션을 *제공*만 하고, *트랜잭션 경계*는 라우트가 그린다. *자원의 라이프사이클*과 *트랜잭션의 라이프사이클*이 서로 다른 개념이라는 사실이 — 이 분리에서 명확해진다. 이걸 한 어노테이션으로 합쳐주던 게 Spring의 `@Transactional`이었고, 그 합침이 *없는 세상*에서 어떻게 사는지가 6장의 화두다.

## `Annotated` 타입 별칭 — 같은 줄을 반복하지 않기

여기까지 코드를 봤으면 한 가지 어색함이 눈에 띌 거다.

```python
def some_route(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    ...
```

`Annotated[...]`가 *길다*. 라우트가 다섯 개, 열 개로 늘면 같은 줄이 자꾸 반복된다. 보기 좋지 않다.

해결책은 — **타입 별칭으로 묶기**다.

```python
# 파이썬 - deps.py
from typing import Annotated
from fastapi import Depends

DbDep = Annotated[AsyncSession, Depends(get_db)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
```

```python
# 파이썬 - router.py
from app.users.deps import DbDep, CurrentUserDep, SettingsDep

@app.post("/orders")
async def create_order(
    payload: OrderCreate,
    db: DbDep,
    user: CurrentUserDep,
    settings: SettingsDep,
):
    ...
```

훨씬 가볍다. Spring에서 `@Autowired` 자체가 한 단어인 것에 비하면 여전히 한 글자 더 적지만, 의도가 한눈에 들어온다. *DB가 필요해. 현재 사용자가 필요해. 설정이 필요해.* 그게 다다.

이 패턴은 한국 velog의 [FastAPI Good Practice (wjddn3711)](https://velog.io/@wjddn3711/FastAPI-Good-Practice) 글에서도 *기본 패턴*으로 권장된다. 도메인별 `deps.py`에 모아두는 게 — 4장 후반부에서 다시 만날 — *레이어드 폴더 구조*와 자연스럽게 맞물린다.

## 테스트 오버라이드 — 한 줄로 의존성을 갈아 끼우기

Spring 출신이 FastAPI의 DI를 보고 가장 *환호하는 자리*다.

Spring에서 우리는 `@MockBean`을 쓰거나, `@TestConfiguration`으로 별도 빈을 등록하거나, `@SpringBootTest`로 컨테이너를 새로 띄웠다. 빠르게 짜다 보면 보일러플레이트가 만만치 않다. *컨테이너를 갈아끼우는 비용*이 안 작다.

FastAPI는 한 줄이다.

```python
# 파이썬 - 테스트 오버라이드
from app.main import app
from app.users.deps import get_db

class FakeDb:
    def find(self, user_id: int):
        return User(id=user_id, name="홍길동")

app.dependency_overrides[get_db] = lambda: FakeDb()

# 이제 모든 라우트에서 get_db 자리에 FakeDb가 들어간다
```

`app.dependency_overrides`는 *딕셔너리*다. 키는 *원래 의존성 함수*, 값은 *대체할 팩토리*다. 키 한 줄을 갈아끼우면 — 그 함수를 의존하던 *모든 곳*이 자동으로 새 객체를 받는다. 그래프를 다시 그릴 필요가 없다.

FastAPI 공식 문서가 같은 의도를 한 줄로 정리한다 — 의존성 오버라이드는 *테스트 시 의존성을 교체하기 위해 설계된 도구*라고. 정확한 의도다. *DI는 테스트를 쉽게 하기 위한 도구다*라는 명제를 — 어쩌면 Spring보다 더 *문자 그대로* 실현한다.

테스트 끝나면 정리하는 것도 잊지 말자.

```python
# 파이썬 - pytest fixture로 깔끔하게
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: FakeDb()
    yield TestClient(app)
    app.dependency_overrides.clear()
```

`yield` 위쪽이 셋업, 아래쪽이 틴다운. 익숙한 모양 아닌가? FastAPI의 `yield` 의존성과 pytest의 `yield` fixture는 — 디자인이 일관된다. *Python 진영의 라이프사이클 표현 방식*이다. 10장 테스트에서 다시 풀어본다.

## APIRouter — 라우트를 도메인별로 묶기

여기까지 보면 한 가지 의문이 따라온다. *라우트가 늘면 `main.py`가 한없이 길어지는 거 아닌가?* 합리적인 의문이다. Spring에서는 `@RequestMapping("/api/users")`를 컨트롤러 클래스에 붙이고, 안에 메서드들이 *자연스럽게 묶였다*. FastAPI에는 그 자리가 어디일까?

답은 `APIRouter`다.

```python
# 파이썬 - users/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}")
def read_user(user_id: int, svc: UserServiceDep):
    return svc.find(user_id)

@router.post("")
def create_user(payload: UserCreate, svc: UserServiceDep):
    return svc.create(payload)
```

```python
# 파이썬 - main.py
from fastapi import FastAPI
from app.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)
```

`APIRouter`는 라우트들의 *부분집합*을 한 객체에 담는다. `prefix`로 공통 경로를, `tags`로 OpenAPI 문서의 그룹을 묶는다. Spring의 *클래스 단위 `@RequestMapping`* 와 거의 1:1이다.

본격적인 활용은 12장 통합 프로젝트에서 다시 본다. 지금은 *한 도메인의 라우트를 한 파일에 묶는 방법*만 손에 익혀두자. `users/router.py`, `users/schemas.py`, `users/service.py`, `users/repository.py`, `users/deps.py` — 5장에서 약속할 폴더 구조의 한 축이다.

## 미들웨어 — 횡단 관심사의 자리

DI를 통해서 횡단 관심사를 *함수 파라미터로* 끌어들이는 패턴을 봤다. 그런데 *정말로 모든 요청에 자동으로 적용*되어야 하는 일은 — Spring `@Aspect`나 `Filter`가 하던 일은 — 어디에 두는가?

답은 **ASGI 미들웨어**다.

```python
# 파이썬 - 요청 ID 미들웨어
from uuid import uuid4
from fastapi import Request

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = uuid4().hex
    request.state.request_id = rid              # 핸들러에서 꺼내 쓸 수 있게
    response = await call_next(request)         # 실제 요청 처리
    response.headers["X-Request-ID"] = rid      # 응답 헤더에도 박기
    return response
```

`call_next(request)` 한 줄이 *실제 라우트 처리*를 호출한다. 그 *전*과 *후*에 우리가 손을 쓸 수 있다. Spring `Filter` 또는 `HandlerInterceptor`와 같은 패턴이다.

여기서 한 가지 짚고 가자. **FastAPI에는 AOP가 없다.** Spring의 `@Aspect`, `@Around`, `@Before` 같은 *메서드 단위*로 횡단 관심사를 가로채는 메커니즘은 — *없다*. 대신 두 가지 도구로 나뉜다.

- **모든 요청에 자동 적용**: 미들웨어. 요청 ID, 로깅, CORS, GZip, 보안 헤더.
- **선택한 라우트에만 적용**: 의존성. 인증, 권한 검사, 도메인 컨텍스트 주입.

`@Aspect`의 자리에 *둘이 들어간다*. 처음엔 *나뉘어 있다는 사실*이 번거롭게 느껴진다. 익숙해지면 — *모든 곳에 걸리는 일*과 *선택한 곳에만 걸리는 일*이 *코드 위에서 분명히 구별된다*는 점이 오히려 마음에 들어온다. AOP가 *어디에 적용됐는지 추적하기 어려운* 경험을 해본 사람이라면 공감이 갈 거다.

요청 ID 미들웨어는 9장 관측성에서 본격적으로 활용된다. 분산 추적의 첫걸음이라 한 자리를 차지한다. 지금은 *한 미들웨어가 어떻게 생겼는지* 보고 가는 정도면 충분하다.

## 한 도메인을 한 폴더에 — 4장의 모든 것을 한자리에

지금까지 본 조각들을 한 도메인에 모아보자. 사용자 조회 API다. 5장에서 본격적으로 약속할 *by-feature 폴더 구조*의 한 예시다.

```
app/
  main.py
  core/
    settings.py
  db/
    session.py
  users/
    deps.py
    schemas.py
    repository.py
    service.py
    router.py
```

```python
# 파이썬 - app/db/session.py
from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.settings import settings

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
```

```python
# 파이썬 - app/users/schemas.py
from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}     # SQLAlchemy 객체에서 변환
```

```python
# 파이썬 - app/users/repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

```python
# 파이썬 - app/users/service.py
from app.users.repository import UserRepository
from app.users.schemas import UserRead

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def find(self, user_id: int) -> UserRead:
        user = await self.repo.find(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return UserRead.model_validate(user)
```

```python
# 파이썬 - app/users/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.users.repository import UserRepository
from app.users.service import UserService

DbDep = Annotated[AsyncSession, Depends(get_db)]

def get_user_repo(db: DbDep) -> UserRepository:
    return UserRepository(db)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]

def get_user_service(repo: UserRepoDep) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

```python
# 파이썬 - app/users/router.py
from fastapi import APIRouter
from app.users.deps import UserServiceDep
from app.users.schemas import UserRead

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, svc: UserServiceDep):
    return await svc.find(user_id)
```

```python
# 파이썬 - app/main.py
from uuid import uuid4
from fastapi import FastAPI, Request
from app.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = uuid4().hex
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response
```

이 한 폴더가 — 이 챕터의 모든 도구를 한자리에 모았다. `Depends` 그래프(`db → repo → service`), `yield` 의존성(`get_db`), `Annotated` 타입 별칭(`DbDep`, `UserRepoDep`, `UserServiceDep`), `APIRouter`, 미들웨어. Spring 사고로 옮기자면 — *한 도메인 패키지의 컨트롤러·서비스·레포지토리·DTO·@Bean 정의*가 한 폴더에 정리된 모습이다.

여기서 한 가지 묘한 감각이 든다. *Spring보다 코드가 적은가?* 그렇진 않다. *@Service·@Repository* 어노테이션이 사라진 자리에 *deps.py*가 들어왔다. 합산하면 비슷하다. 다른 건 — *그래프가 어디 있는지*다. Spring에서는 그래프가 *어노테이션의 모음*으로 *컨테이너 안에* 숨어 있었다. FastAPI에서는 그래프가 *deps.py 파일에 평면적으로 나열*된다. *코드 위에 그래프가 보인다*는 표현이 가장 정확하다.

## 테스트로 마무리 — 의존성 한 줄을 갈아끼우기

같은 도메인의 테스트는 어떻게 짤까?

```python
# 파이썬 - tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.users.deps import get_user_service
from app.users.schemas import UserRead

class FakeUserService:
    async def find(self, user_id: int) -> UserRead:
        return UserRead(id=user_id, username="홍길동", email="hong@example.com")

@pytest.fixture
def client():
    app.dependency_overrides[get_user_service] = lambda: FakeUserService()
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_read_user(client):
    response = client.get("/api/users/42")
    assert response.status_code == 200
    assert response.json() == {
        "id": 42,
        "username": "홍길동",
        "email": "hong@example.com",
    }
```

`app.dependency_overrides[get_user_service] = lambda: FakeUserService()` 한 줄. *그 한 줄*이 라우트의 그래프 전체에서 `UserService` 자리를 갈아끼운다. `UserRepository`도 `get_db`도 — *호출되지 않는다.* 왜냐? `FakeUserService`가 *그 위에 있어서* 아래 의존성들이 풀리지 않으니까. 그래프가 *함수 시그니처에 있다*는 사실이 — 이 테스트의 가벼움을 만든다.

Spring에서 이걸 하려면 `@MockBean UserService userService` + 컨테이너 재시작 비용을 감수해야 했다. FastAPI는 `TestClient(app)`만으로 — 컨테이너랄 게 없으니 — *재시작도 없다*. 테스트 한 개가 한 줄로 끝난다는 감각은 — 한번 손에 들어오면 잘 잊히지 않는다.

## 한 호흡으로 정리

지금까지 그린 그림을 머리에 박을 때다. 세 가지가 남아야 한다.

**첫째, `Depends()`는 함수 파라미터의 마커다.** 컨테이너가 그래프를 들고 있는 게 아니라, 함수 시그니처가 곧 그래프 명세다. 그래서 그래프가 *코드 위에 보인다*. 마법이 적다. 다만 — *같은 줄을 반복해서 적어야 한다*. `Annotated` 타입 별칭으로 줄이자.

**둘째, 기본 스코프는 요청 단위, 한 요청 안에서는 캐시된다.** 싱글톤이 필요한 자원은 의식적으로 만든다 — `lifespan`, 모듈 상수, `@lru_cache`. 세 도구가 겹치는 것 같지만 *테스트하기 좋은가*가 갈래를 만든다.

**셋째, 라이프사이클 자원은 `yield` 의존성으로, 테스트 교체는 `app.dependency_overrides` 한 줄로.** `yield` 위쪽이 셋업, 아래쪽이 틴다운. `finally`에서 *커밋하지 말 것*만 마음 한구석에 박아두자. 6장에서 트랜잭션 경계를 다룰 때 한 번 더 만난다.

그리고 한 가지 더 — **AOP는 없다.** Spring `@Aspect`의 자리에는 *미들웨어*(모든 요청에 자동)와 *의존성*(선택한 라우트에 명시) 두 개가 들어간다. 처음엔 번거롭지만 — *어디에 무엇이 적용되는지가 코드 위에서 분명히 보인다*는 게 익숙해지면 의외로 든든하다.

다음 5장은 데이터 접근이다. JPA에서 SQLAlchemy 2.0으로 옮겨가면서 Hibernate Session과 SQLAlchemy Session의 *닮음과 다름*을 만진다. `DetachedInstanceError`, `joinedload`, Alembic, 그리고 *Spring Data가 자동으로 만들어주던 레포지토리를 직접 짜는 손길*까지.

이 챕터에서 약속한 `Depends` 패턴이 5장에서 *세션 주입의 표준*으로 자리잡는다. *`yield` 의존성과 테스트 오버라이드를 안 보고 5장을 읽으면, 거기 코드가 마법처럼 보일 수 있다.* 그 사이 다리를 잘 건너가자.

준비됐는가? 가자.


---

# 5장. 데이터 접근 — JPA에서 SQLAlchemy 2.0으로

JPA를 쓰던 손에서 떠올려 보자. `@Entity`를 박은 클래스 하나, `extends JpaRepository<Book, Long>` 한 줄짜리 인터페이스, 그리고 `findByTitleContaining`처럼 메서드 이름만 적으면 알아서 쿼리가 만들어지는 그 마법. 우리는 거의 코드를 안 쓰고도 CRUD를 짰다. EntityManager가 1차 캐시를 잡아주고, `@Transactional` 안에서 dirty checking이 자동으로 UPDATE를 쏘아 줬다. Hibernate가 떠받쳐 주던 자동화의 두께가 이렇게 두꺼웠다.

이제 그 자동화 위에 서 있던 발을 SQLAlchemy로 옮긴다. 처음 SQLAlchemy 2.0 코드를 보면 한 가지 감각이 먼저 든다. *명시적이다*. `select(...).where(...)`라는 빌더, `session.add()`라는 직접 호출, `session.commit()`이라는 마침표. JPA가 어노테이션 뒤에 숨겨 두던 동작이 코드 위로 다 올라온다. 이게 처음엔 번거롭게 느껴진다. 그러다 어느 순간, *우연한 commit 타이밍 버그*가 0에 가까워지는 걸 깨닫는다. 명시적이라는 건 손은 더 가지만, 머릿속이 더 깨끗하다는 뜻이다.

SQLAlchemy 진영의 공식 설명도 이 차이를 한 줄로 짚는다 — Hibernate가 Session을 SessionFactory로 만드는 데 비해, SQLAlchemy는 *unit-of-work* 개념에 더 집중하는 쪽이라고. 처음엔 어렵게 느껴지지만, 점점 *우연한 commit-타이밍 버그*가 0에 가까워진다.

그렇다면 어디서부터 손을 대야 할까. 도서 카탈로그를 예제로 잡고, 모델 정의 → 쿼리 → 세션 다루기 → 레포지토리 직접 짜기 → Alembic 마이그레이션 → 폴더 구조 약속까지 한 호흡으로 짚어보자. JPA 사고가 그대로 가는 부분, 살짝 비틀어야 하는 부분, 완전히 다시 짜야 하는 부분을 하나씩 분리해 보자.

> **이 장을 읽기 전 알아둘 것**
> - 4장의 `Depends()`와 `yield` 의존성, `app.dependency_overrides`는 본 장의 모든 라우트가 *전제*한다. 4장의 §`yield` 의존성·§테스트 오버라이드 두 절은 반드시 보고 오자.
> - 본 장은 동기 SQLAlchemy로 가르친다. async 모드는 8장에서 다시 본다.

## SQLAlchemy 2.0의 정체성 — Hibernate와 닮은 점, 다른 점

SQLAlchemy는 두 층으로 짜여 있다. **Core**(SQL Expression Language)와 **ORM**이다. Core는 "안전한 쿼리 빌더"고, ORM은 그 위에 클래스 ↔ 테이블 매핑을 얹은 층이다. Hibernate는 둘이 한 덩어리지만, SQLAlchemy는 둘이 분리돼 있다. ORM이 답답하면 언제든 Core로 내려갈 수 있다 — JPA에서 native query로 떨어지는 그 자리에 SQLAlchemy Core가 있다.

2.0 버전(2023년 1월 정식 출시)이 짜놓은 새 스타일은 한 줄로 요약된다. **모든 쿼리가 `select(...)`로 시작한다**. 1.x의 `session.query(User).filter(...).all()`은 더 이상 권장되지 않는다. 새 코드에선 이렇게 쓴다.

```python
result = session.execute(
    select(User).where(User.email == "tobi@example.com")
)
user = result.scalar_one_or_none()
```

처음엔 `session.execute().scalar_one_or_none()`이 장황해 보인다. JPQL의 `entityManager.createQuery("from User where email = :email", User.class)`와 같은 결과를 두 줄로 받는 데 어색함이 있다. 그러나 이게 정확히 *세션의 SQL 실행*과 *결과 형태*를 분리해 둔 모양이다. 같은 select가 ORM 객체로 떨어질 수도, Core row로 떨어질 수도, 단일 컬럼 스칼라로 떨어질 수도 있는 미래를 위해 한 단계를 둔 셈이다.

표 하나로 정신적 모양을 정렬해 두자.

| 측면 | Hibernate / JPA | SQLAlchemy 2.0 |
|---|---|---|
| 모델 정의 | `@Entity`, JPA 어노테이션 | `class User(DeclarativeBase)` + `Mapped[...]` |
| 쿼리 언어 | JPQL/HQL 또는 Criteria API | Core expression — `select(User).where(...)` |
| 영속성 컨텍스트 | EntityManager (1차 캐시) | Session (Identity Map + Unit of Work) |
| Flush 타이밍 | commit/쿼리 직전 자동 flush | autoflush=True 기본이나, 명시적 통제 권장 |
| Lazy loading | 프록시, 트랜잭션 종료 후 `LazyInitializationException` | 세션 분리 후 접근 → **`DetachedInstanceError`**. async는 더 까다로움 |
| 마이그레이션 | Flyway / Liquibase (외부 도구) | Alembic (SQLAlchemy 메타데이터를 직접 읽음) |
| 자동 레포지토리 | `extends JpaRepository<T, ID>` | **없다.** `class UserRepository:`를 손으로 작성 |
| 트랜잭션 | `@Transactional` (선언적) | `session.begin()` (명시적) — 6장 |

마지막 두 행이 가장 큰 충격이다. *자동 레포지토리가 없다*는 것 — 이게 본 장 후반의 큰 그림이다. *선언적 트랜잭션이 없다*는 것 — 이게 다음 장의 hinge다.

## 모델 정의 — `@Entity` 자리에 `DeclarativeBase`

도서 카탈로그를 짜보자. 도메인은 셋이다. `Book`, `Author`, `Category`. 다대다(Book ↔ Category)와 다대일(Book → Author) 관계가 한 번씩 등장한다. JPA로 짰다면 익숙한 어노테이션 더미가 등장하는 자리다. Kotlin/JPA로 짠 그림이 가장 짧으니 옮겨 적었다 — Java로 같은 일을 하면 getter/setter가 줄을 더한다.

```kotlin
// Spring (Kotlin) — JPA
@Entity
@Table(name = "books")
class Book(
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null,

    @Column(nullable = false, length = 200)
    val title: String,

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    val author: Author,

    @ManyToMany
    @JoinTable(
        name = "book_categories",
        joinColumns = [JoinColumn(name = "book_id")],
        inverseJoinColumns = [JoinColumn(name = "category_id")],
    )
    val categories: MutableSet<Category> = mutableSetOf(),
)
```

같은 그림을 SQLAlchemy 2.0으로 옮기자.

```python
# SQLAlchemy 2.0
from __future__ import annotations

from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped[Author] = relationship(back_populates="books")
    categories: Mapped[set[Category]] = relationship(
        secondary=book_categories, back_populates="books"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    books: Mapped[list[Book]] = relationship(back_populates="author")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    books: Mapped[list[Book]] = relationship(
        secondary=book_categories, back_populates="categories"
    )
```

매핑이 그대로 보인다. 하나하나 짚어두자.

- **`DeclarativeBase`** = JPA의 `@MappedSuperclass` + `@Entity`의 토대. 우리 도메인 클래스들이 다 이걸 상속한다.
- **`Mapped[int]` + `mapped_column(primary_key=True)`** = `@Id @GeneratedValue` + `@Column`. 타입 힌트가 nullable 정보까지 같이 전달한다 — `Mapped[int]`면 NOT NULL, `Mapped[int | None]`이면 NULL 가능.
- **`relationship(back_populates=...)`** = `@OneToMany(mappedBy=...)` + `@ManyToOne`의 양방향 표시. JPA처럼 *한쪽이 owning side*다 — `ForeignKey`를 가진 쪽이 그 자리.
- **`Table(..., secondary=...)`** = `@ManyToMany` + `@JoinTable`. 별도 클래스가 아니라 `Table` 객체로 정의하는 게 SQLAlchemy 식이다. 조인 테이블에 추가 컬럼(예: `added_at`)이 필요하면 그때는 별도 클래스로 승격한다.

JPA보다 코드 라인이 살짝 짧다는 느낌이 들 것이다. 어노테이션이 데코레이터로 빠지지 않고, 컬럼 타입이 타입 힌트와 합쳐졌기 때문이다. *타입 힌트가 곧 메타데이터*인 SQLAlchemy 2.0의 설계는 우리가 3장에서 본 Pydantic의 그것과 같은 정신적 모양이다 — 한 번 익히면 머리에 좋다.

### 엔진과 세션 — `SessionFactory` 자리에 `sessionmaker`

JPA에서는 보통 `EntityManagerFactory`(Spring이 만들어 줌)와 `EntityManager`(트랜잭션마다 새로)로 나뉜다. SQLAlchemy는 거의 같은 그림이다.

```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(
    "postgresql+psycopg://app:secret@localhost:5432/library",
    echo=False,           # True로 두면 SQL이 stdout에 찍힘 — 개발 시 유용
    pool_pre_ping=True,   # 죽은 커넥션 자동 재연결
)

SessionLocal = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)
```

- **`engine`** = `DataSource`. 커넥션 풀을 안에 품고 있다. 앱 한 개당 하나만 만든다.
- **`sessionmaker(...)`** = `EntityManagerFactory`. 호출하면 새 `Session`이 나온다.
- **`expire_on_commit=False`** = 이걸 잊지 말자. 기본값 `True`면 commit 직후 *모든 객체의 속성이 expire*되어서, 직후에 `book.title`을 읽으면 다시 SELECT가 일어난다. FastAPI에서는 응답 직렬화 시점에 commit 이후 객체를 다시 읽는 일이 흔해서, 잘못 두면 `DetachedInstanceError`가 폭발한다. 끔찍한 일이다.

엔진과 세션은 어디에 둘까. 답은 4장에서 잡아둔 `Depends()` 자리다. `yield` 의존성으로 한 요청 동안 살아 있다가 `finally`에서 닫히는 그 패턴 그대로다.

```python
# app/db/deps.py
from typing import Annotated, Iterator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 타입 별칭 — 4장에서 익힌 패턴
DbSession = Annotated[Session, Depends(get_db)]
```

이제 라우트는 이렇게 쓴다.

```python
@router.get("/books/{book_id}")
def get_book(book_id: int, db: DbSession):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
```

JPA에서 `EntityManager`를 `@PersistenceContext`로 주입받는 그 코드와 정신적 모양이 같다. 마법이 한 겹 벗겨졌을 뿐이다.

여기서 한 번 주의해 두자. **`finally` 절에서 `commit`을 하지 말자.** 무슨 말인가? FastAPI 튜토리얼 중에는 `try: yield db; db.commit(); except: db.rollback(); finally: db.close()` 같은 코드가 돌아다닌다. 이게 함정이다. `yield db` 다음 줄은 *경로 함수가 끝나고 응답이 클라이언트로 나간 뒤에* 실행된다. 그때 발생한 예외는 응답에 영향을 주지 않지만, 트랜잭션은 실패한 상태로 끝난다. 디버깅 호흡이 진짜 번거롭다.

FastAPI GitHub의 요청-스코프 트랜잭션 토론도 같은 함정을 한 줄로 짚는다 — *의존성의 finally 절에서 commit을 할 수 없다*고. 그 코드는 경로 함수가 끝나고 결과가 클라이언트에 반환된 뒤에 실행되기 때문이다.

권장 패턴은 단순하다. `get_db`는 세션을 열고 닫기만 하고, *트랜잭션 경계는 라우트 또는 서비스 레이어에서 명시*한다. 자세한 모양은 6장에서 본격적으로 다룬다. 이 장에선 우선 `with db.begin():` 한 줄을 손에 익혀두자.

```python
@router.post("/books", status_code=201)
def create_book(payload: BookCreate, db: DbSession):
    with db.begin():       # 트랜잭션 명시
        book = Book(**payload.model_dump())
        db.add(book)
    db.refresh(book)       # commit 뒤 ID 등을 다시 채우려면 필요
    return BookRead.model_validate(book)
```

## 쿼리 — JPQL 출신 손에 익혀둘 핵심 세 개

망라 대신 *손에 익을 핵심 셋*만 짚자. 도서 카탈로그에서 자주 쓰게 될 모양이다.

### 1) 단순 조회 — `where` + `order_by` + 페이징

```python
from sqlalchemy import select

def list_books(db: Session, q: str | None, limit: int, offset: int) -> list[Book]:
    stmt = select(Book)
    if q:
        stmt = stmt.where(Book.title.ilike(f"%{q}%"))
    stmt = stmt.order_by(Book.title.asc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())
```

JPQL의 `select b from Book b where ...`과 비교해 보면 *문자열이 아니라 객체로 쿼리*를 만든다는 점이 결정적 차이다. 컬럼 이름 오타를 IDE가 잡아준다. `Book.titel`이라 잘못 적으면 빨간 줄이 뜬다 — JPQL에선 런타임에야 알게 되던 그 자리다.

### 2) 조인과 `selectinload` — Lazy 함정 회피의 핵심

이게 SQLAlchemy의 가장 중요한 한 패턴이다. 손에 익히자.

```python
from sqlalchemy.orm import selectinload

def list_books_with_author(db: Session) -> list[Book]:
    stmt = (
        select(Book)
        .options(selectinload(Book.author), selectinload(Book.categories))
        .order_by(Book.id)
    )
    return list(db.execute(stmt).scalars().all())
```

`.options(selectinload(...))`는 JPA의 `@EntityGraph` 또는 `fetch join`에 해당한다. 차이가 있다면, SQLAlchemy의 `selectinload`는 *별도의 IN 쿼리*로 관계를 끌어오므로 카타시안 곱 폭발이 없다. 두 번째 쿼리가 한 번 더 나가지만, 결과 행 수가 폭발하지 않는다.

`joinedload`는 *같은 쿼리에 JOIN으로* 끌어온다. *-to-one 관계엔 적합하지만, *-to-many 관계에 쓰면 결과가 행 단위로 부풀어 페이지네이션과 충돌한다. JPA에서 `fetch join`을 `setMaxResults`와 함께 쓰면 경고가 뜨는 그 자리다. 같은 함정이 SQLAlchemy에도 있다 — 이름만 다르다.

손에 익혀 두자. **`-to-many`는 `selectinload`, `-to-one`은 `joinedload`**. 헷갈리면 `selectinload`를 기본으로.

### 3) 집계 — `func.count()` + `group_by`

```python
from sqlalchemy import func

def book_count_by_category(db: Session) -> list[tuple[str, int]]:
    stmt = (
        select(Category.name, func.count(Book.id).label("cnt"))
        .join(Category.books)
        .group_by(Category.name)
        .order_by(func.count(Book.id).desc())
    )
    return list(db.execute(stmt).all())
```

`db.execute(stmt).all()`은 ORM 객체가 아닌 *Row 튜플*을 반환한다. ORM 매핑이 필요 없는 집계엔 이게 자연스럽다. JPA의 `getResultList()`로 `Object[]`가 떨어지는 그 자리다.

이 세 패턴만 손에 익혀도 도서 카탈로그 90%는 짠다. *나머지 10%는 그때 SQLAlchemy 공식 문서를 찾자* — 망라하려고 욕심내는 대신 핵심 회로를 단단히 굳히는 편이 낫다.

## Session = Identity Map + Unit of Work — 미묘하지만 결정적인 차이

JPA의 EntityManager가 1차 캐시(Identity Map)와 dirty checking을 자동으로 해 주듯, SQLAlchemy의 Session도 같은 그림을 갖는다. 한 세션 안에서 같은 PK로 조회한 객체는 *항상 같은 인스턴스*다. 같은 객체에 속성을 바꾸면 commit 시점에 UPDATE가 자동으로 나간다 — 이것도 그대로다.

다만 작은 결이 다르다. 다음 세 가지를 머리에 박아 두자.

**첫째, flush 타이밍.** JPA는 트랜잭션 commit·쿼리 실행 직전에 자동 flush한다. SQLAlchemy도 기본은 같지만(`autoflush=True`), Session의 철학은 *flush를 명시적으로 통제할 수 있어야 한다*는 쪽으로 더 기울어 있다. 그래서 어떤 코드베이스는 `autoflush=False`로 두고 명시적으로 `db.flush()`를 부른다. 처음 접하면 어느 쪽이 맞는지 헷갈리는데, *프로젝트 한 군데로 정해두고 그 안에선 일관되게 가자*. 우리 책 예제는 `autoflush=True`(기본) + 명시적 `with db.begin():` 트랜잭션의 조합이다.

**둘째, dirty checking은 같지만 `expire_on_commit`이 다르다.** JPA에서 commit 후 영속 객체에 접근하면 그냥 값을 반환한다(detach될 때까지). SQLAlchemy는 *기본값이 commit 후 모든 속성 expire*다. 그래서 `session.commit()` 직후 `book.title`을 읽으면 SELECT가 한 번 더 나간다. 응답 직렬화 직전에 commit이 일어나는 FastAPI 패턴과 잘 안 맞는다. 그래서 우리 `SessionLocal`에 `expire_on_commit=False`를 두는 게 표준이다.

**셋째, Lazy loading의 실패 신호가 다르다.** JPA는 `LazyInitializationException`, SQLAlchemy는 `DetachedInstanceError`. 의미는 같다 — *세션이 닫힌 뒤 lazy 관계에 접근했다*. 단, SQLAlchemy의 async 모드에선 이 함정이 더 까다롭다(8장에서 다시). 동기 모드에선 `selectinload`/`joinedload`로 미리 끌어오는 습관 하나로 거의 다 해결된다.

이 세 항목만 머리에 두면 *JPA 사고로 SQLAlchemy를 쓰는* 대부분의 함정은 피한다. 손이 처음엔 불편하지만, 점점 익는다.

## 레포지토리를 직접 짜자 — Spring Data의 마법이 없는 세상

이게 본 장의 가장 큰 *멘탈 적응*이다. JPA를 쓰면서 우리는 거의 코드를 안 썼다.

```kotlin
interface BookRepository : JpaRepository<Book, Long> {
    fun findByTitleContaining(q: String): List<Book>
    fun findByAuthorId(authorId: Long, pageable: Pageable): Page<Book>
}
```

메서드 이름이 곧 쿼리였다. Spring Data가 런타임에 구현을 만들어 줬다. 편했다.

SQLAlchemy 진영엔 이게 없다. 정확히 말하면, *그 마법이 안티패턴*으로 여겨진다. 메서드 이름으로 쿼리를 만드는 자동화는 단순 케이스엔 빛나지만, 조금만 복잡해지면 메서드 이름이 *암호*가 된다. `findByAuthorIdAndCategoriesNameContainingOrderByPublishedAtDesc` 같은 이름을 본 적 있는가? 그게 그 자동화의 끝이다.

대신 우리는 손으로 짠다. 이게 처음엔 끔찍하게 느껴진다 — *내가 또 이걸 적어야 해?* 그러다 깨닫는다. 손으로 적는 쿼리가 *코드 리뷰에 명시적으로 올라오고*, 인덱스가 맞는지 *읽으면서 검증*되고, 페이지네이션·정렬·조인 옵션이 *데이터 모양과 함께 보인다*. 자동화가 가렸던 비용이 코드 표면에 올라오는 셈이다.

표준 모양을 잡자.

```python
# app/books/repository.py
from typing import Iterable
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.books.models import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def list(self, q: str | None, limit: int, offset: int) -> list[Book]:
        stmt = (
            select(Book)
            .options(selectinload(Book.author), selectinload(Book.categories))
            .order_by(Book.title.asc())
            .limit(limit)
            .offset(offset)
        )
        if q:
            stmt = stmt.where(Book.title.ilike(f"%{q}%"))
        return list(self.db.execute(stmt).scalars().all())

    def add(self, book: Book) -> None:
        self.db.add(book)

    def delete(self, book: Book) -> None:
        self.db.delete(book)
```

크지 않다. 4~5개 메서드면 한 도메인의 90%가 끝난다. *원할 때만 메서드를 추가*한다 — 미리 짜두지 말자. JPA처럼 100가지 `findBy...`를 미리 정의해 둘 필요가 없다. 쓸 때 한 줄 추가하는 호흡으로 가자.

서비스 레이어에서 이걸 어떻게 묶는지 보자.

```python
# app/books/service.py
from app.books.repository import BookRepository
from app.books.schemas import BookCreate, BookRead


class BookService:
    def __init__(self, db: Session, books: BookRepository):
        self.db = db
        self.books = books

    def create(self, payload: BookCreate) -> BookRead:
        with self.db.begin():
            book = Book(title=payload.title, author_id=payload.author_id)
            self.books.add(book)
        self.db.refresh(book)
        return BookRead.model_validate(book)
```

서비스가 트랜잭션 경계를 그린다. 레포지토리는 *SELECT/INSERT/DELETE*만 책임진다. 책임이 깔끔하게 나뉜다.

DI는 4장에서 익힌 그대로다.

```python
# app/books/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.books.repository import BookRepository
from app.books.service import BookService


def get_book_repo(db: Annotated[Session, Depends(get_db)]) -> BookRepository:
    return BookRepository(db)


def get_book_service(
    db: Annotated[Session, Depends(get_db)],
    books: Annotated[BookRepository, Depends(get_book_repo)],
) -> BookService:
    return BookService(db, books)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]
```

라우트는 이렇게 짧아진다.

```python
# app/books/router.py
from fastapi import APIRouter

from app.books.deps import BookServiceDep
from app.books.schemas import BookCreate, BookRead

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookRead, status_code=201)
def create_book(payload: BookCreate, service: BookServiceDep):
    return service.create(payload)
```

JPA + Spring Service 코드와 정신적 모양이 거의 같다. 차이는 한 줄 — *컨테이너가 만들어주지 않고 내가 함수로 그래프를 묶는다*. 그게 명시적이다는 말의 실체다.

### Unit of Work — DB 세션을 라우트 끝까지 끌고 다닐 것인가

여기서 한 가지 더 짚어두자. FastAPI 진영엔 *DB 세션을 의존성으로 라우트 끝까지 끌고 다니는 게 안티패턴*이라는 비판이 한 갈래로 자리잡고 있다. 라우트가 길어지면 *요청 내 longtail 트랜잭션*이 생기고, 어디서 commit이 일어났는지 추적이 힘들어진다는 주장이다.

대안은 **Unit of Work 객체**다. 도메인별 레포지토리를 한 묶음으로 들고 있는 컨텍스트 매니저를 만든다.

```python
# app/db/uow.py
from contextlib import contextmanager
from sqlalchemy.orm import Session

from app.books.repository import BookRepository
from app.db.session import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    @contextmanager
    def __call__(self):
        db = self._session_factory()
        try:
            self.books = BookRepository(db)
            # self.authors = AuthorRepository(db) ...
            yield self
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()


def get_uow() -> UnitOfWork:
    return UnitOfWork()
```

라우트는 이렇게 쓴다.

```python
@router.post("/books")
def create_book(
    payload: BookCreate,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow() as u:
        book = Book(**payload.model_dump())
        u.books.add(book)
    return BookRead.model_validate(book)
```

이 패턴은 *트랜잭션 경계가 한 곳에 모이고*, *commit/rollback이 with 블록 끝에 정확히 박힌다*는 장점이 있다. 작은 서비스엔 살짝 과해 보이지만, 도메인이 셋 넘어가면 가치가 빛난다.

이 장의 예제는 *서비스 레이어에서 명시 트랜잭션* 패턴으로 가르친다. UoW는 6장 트랜잭션 챕터의 본격 주제로 다시 만난다. 일단은 *이런 대안이 있다*는 사실만 머리에 넣어두자.

## Alembic — Flyway 자리에 무엇이 들어서는가

Spring Boot에서 마이그레이션은 보통 한 줄로 끝난다. `db/migration/V1__init.sql`을 두면 Flyway가 시작 시 자동으로 돌린다. *프로퍼티 한 줄도 필요 없다*. 우리가 그동안 누리던 자동화의 두께가 여기서도 두꺼웠다.

FastAPI/SQLAlchemy에선 그 동작을 Alembic이 떠맡는다. 차이가 둘 있다. *Flyway는 SQL이 일급*이고, *Alembic은 Python이 일급*이다. 그리고 *Alembic은 자동 시작이 없다* — `alembic upgrade head`를 컨테이너 startup script에 박아야 한다.

설치와 초기화부터 보자.

```bash
$ uv add alembic
$ uv run alembic init alembic
```

생긴 폴더 구조다.

```text
alembic/
├── env.py            # 마이그레이션 실행 환경 설정
├── script.py.mako    # 새 마이그레이션 파일 템플릿
├── versions/         # 실제 마이그레이션 파일들
└── README
alembic.ini           # 설정 파일
```

`alembic.ini`의 `sqlalchemy.url`을 우리 DB URL로 바꾸고, 더 깔끔한 방법으로는 `env.py`에서 환경변수로 읽도록 손본다. 그리고 `env.py`에 우리 모델의 메타데이터를 알려준다.

```python
# alembic/env.py (핵심 부분만)
from app.db.session import Base
from app.books import models  # noqa: F401 — 모든 모델 import 필요

target_metadata = Base.metadata
```

이제 첫 마이그레이션을 자동 생성하자.

```bash
$ uv run alembic revision --autogenerate -m "initial schema"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.autogenerate.compare] Detected added table 'authors'
INFO  [alembic.autogenerate.compare] Detected added table 'books'
INFO  [alembic.autogenerate.compare] Detected added table 'categories'
INFO  [alembic.autogenerate.compare] Detected added table 'book_categories'
  Generating alembic/versions/8f3e2a1b9c4d_initial_schema.py ... done
```

생긴 파일을 열어 보자.

```python
# alembic/versions/8f3e2a1b9c4d_initial_schema.py
"""initial schema

Revision ID: 8f3e2a1b9c4d
Revises:
Create Date: 2026-05-16 10:00:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "8f3e2a1b9c4d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("authors.id"), nullable=False),
    )
    # ... categories, book_categories 생략


def downgrade() -> None:
    op.drop_table("book_categories")
    op.drop_table("books")
    op.drop_table("categories")
    op.drop_table("authors")
```

적용은 한 줄.

```bash
$ uv run alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade  -> 8f3e2a1b9c4d, initial schema
```

여기까지는 Flyway와 정신적 모양이 거의 같다. 한 가지 *주의*가 있다. **`--autogenerate`를 맹신하지 말자.** Alembic의 autogenerate는 우리가 적은 모델 메타데이터와 *현재 DB 스키마*를 비교해 차이를 추론한다. 그런데 다음 변경은 자동으로 잡지 못하거나 잘못 잡는다.

- 컬럼 이름 변경 → autogenerate는 "기존 컬럼 drop + 새 컬럼 add"로 인식한다. 데이터 손실.
- 컬럼 타입의 미묘한 변경(예: `VARCHAR(50)` → `VARCHAR(100)`) → DB 방언별 결과가 다르다.
- 인덱스·제약조건의 이름 — 자동 생성된 이름과 실제 DB의 이름이 다르면 *불필요한 drop/recreate*가 나온다.

그래서 *생성된 파일은 반드시 사람이 한 번 읽고 보정한다*. 이건 Flyway에서 SQL을 직접 쓰던 그 자리와 같다 — 다만 첫 90%를 도구가 만들어주는 차이가 있다.

> Alembic은 SQLAlchemy 메타데이터를 직접 읽기 때문에 Java 진영의 Flyway와는 한 단계 더 단단히 묶여 있다. Flyway가 SQL을 *별도 언어*로 다루는 데 비해, Alembic은 *Python 함수*로 다룬다. 마이그레이션 안에서 일반 Python 코드를 돌려 데이터 마이그레이션을 끼우기도 쉽다.

## by-feature 폴더 구조 — 이 책 전체를 관통할 약속

한 그림을 마지막으로 박아두자. **모든 작은 예제**가 따라가는 폴더 구조의 표준이다. 새 도메인이 등장하는 4·6·7·9·10장 어디에서나 우리는 이 모양을 반복한다. 12장의 통합 프로젝트는 이걸 *이미 안다고 가정*한다.

```text
app/
├── main.py              # FastAPI 진입점, 라우터 등록
├── core/
│   ├── config.py        # pydantic-settings 기반 설정 (7장에서 본격 도입)
│   └── security.py      # 비밀번호 해싱, JWT 도구 (7장)
├── db/
│   ├── session.py       # engine + SessionLocal
│   ├── base.py          # DeclarativeBase
│   ├── deps.py          # get_db
│   └── uow.py           # 선택: Unit of Work
├── books/               # ← 한 도메인 = 한 폴더
│   ├── __init__.py
│   ├── models.py        # SQLAlchemy entity
│   ├── schemas.py       # Pydantic DTO
│   ├── repository.py    # 데이터 접근
│   ├── service.py       # 비즈니스 로직 + 트랜잭션 경계
│   ├── router.py        # FastAPI 라우트
│   └── deps.py          # 이 도메인 전용 Depends 헬퍼
├── authors/
│   └── (같은 구조)
└── tests/
    ├── books/
    └── authors/
```

이게 우리가 *Spring 출신*에게 가장 자연스럽다고 본 모양이다. Java 패키지 구조와 한 줄로 매핑된다.

| Spring 패키지 | FastAPI 모듈 |
|---|---|
| `com.foo.books.controller` | `app.books.router` |
| `com.foo.books.dto` | `app.books.schemas` |
| `com.foo.books.domain` | `app.books.models` |
| `com.foo.books.repository` | `app.books.repository` |
| `com.foo.books.service` | `app.books.service` |

매핑이 1:1로 떨어진다. Spring 프로젝트의 `com.foo.{도메인}.{layer}` 패키지 구조를 *언어를 갈아 끼우고 그대로 가져온* 모양이다.

> "FastAPI에서는 'feature/domain 별 그룹핑'이 잘 동작한다. 'by feature'는 웹 API에 잘 맞는다."

다른 후보로 *layer-first*(`controllers/`, `services/`, `repositories/` 폴더로 묶기) 구조도 있다. Spring 진영에서도 두 갈래가 있다. 그런데 도메인이 셋 넘어가면 *feature-first*가 훨씬 단단하다 — 한 도메인을 통째로 옮기거나, 한 도메인을 마이크로서비스로 떼어내거나, 한 도메인만 신규 입사자에게 맡기기가 쉽다. 우리 책은 feature-first를 표준으로 박는다.

손에 익혀 두자. 새 도메인을 추가할 때마다 이 6개 파일(`models.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`, `deps.py`)을 *복사해 채우는* 호흡이다. 이 호흡이 머리에 박히면, 책이 끝난 뒤 본인 프로젝트에 그대로 옮겨갈 수 있다.

## 한 호흡으로 정리

정리해야 할 패턴이 많은 자리다. 한 번에 정리해 두자.

- **모델 정의**는 `DeclarativeBase` + `Mapped[...]` + `relationship`의 삼총사. JPA `@Entity` + `@Column` + `@ManyToOne`의 평행 구도.
- **세션**은 `SessionLocal` → `get_db` → `yield` 패턴. `expire_on_commit=False`는 잊지 말자.
- **쿼리**는 `select(...).where(...).order_by(...)`로 시작한다. 손에 익힐 핵심은 셋 — `where`+페이징, `selectinload` 옵션, `func.count()` 집계.
- **Lazy 함정**: `DetachedInstanceError`는 `selectinload`/`joinedload`로 사전 차단하자. `-to-many`는 `selectinload`, `-to-one`은 `joinedload`.
- **레포지토리**는 손으로 짠다. Spring Data의 자동화는 없다. 그게 결국 *코드 표면에 비용이 올라오는* 깔끔함을 준다.
- **Unit of Work**는 도메인이 셋 넘어갈 때부터 검토하자. 5장은 서비스 레이어 명시 트랜잭션으로 충분.
- **Alembic**은 Flyway의 자리. autogenerate를 맹신하지 말고 *생성된 파일을 사람이 한 번 읽는다*.
- **폴더 구조**는 `app/{도메인}/{models|schemas|repository|service|router|deps}.py`의 by-feature 6종 세트. 책 끝까지 이 약속을 반복한다.

여기까지 오면 한 가지 감각이 든다. *JPA가 어노테이션 뒤에 숨겨두던 일을 SQLAlchemy는 코드 위로 다 올려둔다*. 그 차이가 답답하다가, 어느 순간 안심으로 바뀐다. *내가 무슨 쿼리를 짜는지 내가 본다*는 안심이다.

다음 장이 책 전체의 hinge다. `@Transactional` 한 줄이 없는 자리에서, 우리는 트랜잭션 경계를 어디에 어떻게 그릴지 본격적으로 결정해야 한다. 본 장에서 `with db.begin():` 한 줄을 손에 익혔으면, 다음 장에서 우리는 그 한 줄을 *어디에 둘 것인가*라는 더 큰 질문 앞에 선다.


---


# 6장. 트랜잭션 — `@Transactional`이 없는 세상에서 살아남기

송금 API 하나를 Spring으로 짠다고 해보자. `TransferService.transfer(from, to, amount)` 메서드가 머릿속에 그려진다. 출금 계좌의 잔액을 차감하고, 입금 계좌의 잔액을 증가시키고, 거래 내역을 한 줄 남긴다. 세 줄짜리 로직이다. 그리고 이 메서드 위에는 모두가 알다시피 `@Transactional` 한 줄이 박혀 있다. 출금이 성공한 뒤 입금에서 예외가 나면 출금까지 자동으로 롤백된다. 우리 손이 닿기 전에 Spring이 알아서 한다.

이 자동의 무게는 평소에는 잘 의식되지 않는다. 그런데 `@Transactional`을 빼본 사람이라면 안다 — 그 한 줄이 사라지면 코드 곳곳에 `try/catch`와 명시적 롤백이 흩뿌려지고, 누군가는 분명히 빼먹는다. 그렇게 빠진 자리에서 *부분 실패*가 새어 나간다. 어떤 계좌에서는 돈이 빠졌는데, 다른 계좌에는 들어가지 않는다. 끔찍한 일이다.

이제 같은 송금을 FastAPI로 짜본다고 해보자. SQLAlchemy 2.0의 비동기 세션을 쓰고, 라우트는 `Depends(get_db)`로 세션을 주입받는다. 그런데 `@Transactional`을 어디에 달지? 답은 — **없다.** FastAPI/SQLAlchemy에는 `@Transactional` 어노테이션 자체가 없다. 손이 잠시 멈춘다. "그럼 트랜잭션은 누가 시작하고 누가 닫지?" 살짝 난감하다. 이 난감함이 이 챕터의 출발점이다.

핵심 질문은 둘이다. **`@Transactional` 한 줄이 사라진 자리에 무엇을 놓아야 같은 안전성을 얻는가?** 그리고 **한 요청 안의 트랜잭션 경계를 어디에 그어야 하는가?** 둘 다 이론이 아니라 손에 잡히는 회로의 문제다. 책에서 가장 큰 인지 전환이 일어나는 자리이기도 하다. 한 발 한 발 함께 그려보자.

## 왜 흉내 내지 않았는가 — 명시성의 철학

먼저 묻고 가자. SQLAlchemy도 Python에 어노테이션 비슷한 데코레이터가 있고, FastAPI도 `Depends`로 횡단관심사를 처리할 줄 안다. 그런데 왜 둘 다 `@Transactional`을 안 만들었을까? 안 만든 게 아니라 *의도적으로 안 만든* 쪽에 가깝다.

이유를 한 줄로 정리하면 — **명시성의 철학**이다. Python 진영에는 "Explicit is better than implicit"(명시적인 게 암묵적인 것보다 낫다)이라는 PEP 20의 한 줄이 통주저음처럼 깔려 있다. Spring의 `@Transactional`은 강력하지만, 그 강력함 뒤에는 *숨겨진 동작*이 잔뜩 깔려 있다. 프록시 객체를 만들어 메서드 호출을 가로채고, 같은 클래스 안의 호출은 프록시를 통하지 않아 트랜잭션이 *조용히* 적용되지 않는다. 전파(propagation) 옵션은 `REQUIRED`/`REQUIRES_NEW`/`NESTED` 등 일곱 가지가 있고, 어느 게 켜져 있는지 코드만 봐서는 안 보인다. 익숙하면 편리하지만, 처음 들어온 사람에게는 마법처럼 보이는 자리다.

SQLAlchemy는 그 마법을 일부러 걷어냈다. 트랜잭션은 *눈에 보이는 구문*으로 시작하고 닫는다. `session.begin()`을 호출하는 자리가 트랜잭션의 시작이고, `commit()` 또는 `rollback()`이 끝이다. 컨텍스트 매니저를 쓰면 `with` 블록의 들여쓰기가 곧 트랜잭션의 범위다. 코드 한눈에 *어디서 시작해 어디서 닫히는지*가 보인다.

> "Hibernate는 Session 인스턴스를 SessionFactory로 만든다. SQLAlchemy는 unit-of-work 개념에 더 집중하는데, 처음엔 이해·사용이 어렵지만 나중에 우연한 commit-타이밍 버그를 거의 0으로 줄여주는 가치를 깨닫게 된다." — QuietShark 블로그(reference §2.4)

이 평가가 핵심을 짚는다. 처음에는 *번거롭게* 느껴지지만, 시간이 지나면 *우연한 버그를 줄이는* 자리로 돌아온다는 것. Spring 출신이 처음 6장을 읽으면 "한 줄로 끝나던 일을 왜 이렇게 길게 풀어 쓰지?"라고 묻게 된다. 답은 — **길어진 게 아니라 *드러난* 것이다.** Spring에서는 보이지 않던 *시작과 끝*이 FastAPI에서는 코드 위에 명시적으로 드러난다.

기억해두자. 이 챕터의 모든 패턴은 같은 약속을 향한다 — *트랜잭션은 우리가 시작하고 우리가 닫는다.* 손이 잠시 더 가지만, 그 손길이 곧 안전망이다.

## 흔한 안티패턴 — `get_db()` finally에서 commit

처음 SQLAlchemy 트랜잭션 코드를 짜는 사람이 흔히 빠지는 함정 하나를 짚고 가자. 인터넷을 뒤지면 다음과 비슷한 의존성 함수가 의외로 자주 보인다.

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()         # ← 안티패턴
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

"세션을 의존성에서 만들고, 함수가 끝나면 자동으로 commit이나 rollback이 나가게 한다"는 발상 자체는 자연스럽다. Spring의 `@Transactional`이 자동으로 해주던 일을 의존성의 `try/finally`에서 흉내 내는 셈이다. 그런데 이 코드는 *조용히 잘못 동작한다*.

문제의 핵심은 FastAPI의 의존성 라이프사이클에 있다. `yield`로 세션을 흘려준 뒤 *돌아오는* 코드는 라우트 함수가 *반환된 뒤*, 그리고 응답이 클라이언트로 *나간 뒤*에 실행된다. 무슨 뜻이냐면 — `await session.commit()`이 호출되는 순간 클라이언트는 이미 "성공"이라는 200 응답을 받았다는 뜻이다. 그런데 그 `commit()`이 실패하면? 데이터베이스에는 아무것도 안 들어갔는데, 사용자는 성공 응답을 받은 상태다. 정확히 부분 실패의 끔찍한 형태다.

> "의존성의 `finally` 절에서 `commit`을 할 수 없다 — 그 코드는 경로 함수가 끝나고 결과가 클라이언트에 반환된 **뒤에** 실행된다. 그때 발생하는 예외는 응답에 영향을 주지 않지만 트랜잭션은 실패한 상태가 된다." — GitHub: Request-scoped transactions(reference §2.3)

문장이 길지만 핵심은 한 줄이다. **`commit`은 응답이 나가기 *전에* 일어나야 한다.** 의존성의 `finally`는 응답이 나간 *뒤*다. 둘 사이에는 메우기 어려운 시간 간격이 있다.

그래서 의존성 함수는 "세션을 열고 닫는" 일만 한다. commit과 rollback은 *라우트 안*에서 명시적으로. 다음이 그 원형이다.

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
        # commit은 여기서 하지 않는다. 라우트 또는 서비스 레이어에서 명시한다.
```

`async with AsyncSessionLocal()`이 세션을 열고, 블록이 끝나면 자동으로 `close()`를 호출한다. 트랜잭션 *시작*과 *종료*는 일부러 빈 자리로 남겨둔다. Spring 출신이 보면 "허전하지 않나?" 싶지만, 이 허전함이 의도다. *허전한 자리에 우리 손이 들어간다.*

## 권장 패턴 — `async with session.begin():`

이제 진짜 트랜잭션 경계를 그리는 자리로 가자. 다음 코드를 보자.

```python
@router.post("/transfers")
async def create_transfer(
    payload: TransferCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TransferRead:
    async with db.begin():
        src = await db.get(Account, payload.from_id, with_for_update=True)
        dst = await db.get(Account, payload.to_id, with_for_update=True)
        if src.balance < payload.amount:
            raise InsufficientBalance(payload.from_id)
        src.balance -= payload.amount
        dst.balance += payload.amount
        db.add(Transfer(from_id=src.id, to_id=dst.id, amount=payload.amount))
    return TransferRead(...)
```

핵심은 `async with db.begin():` 블록이다. 들여쓰기로 묶인 네 줄이 곧 *한 트랜잭션*이다. 블록을 정상적으로 빠져나오면 `commit()`이 호출되고, 블록 안에서 예외가 발생하면 `rollback()`이 자동으로 호출된다. Spring의 `@Transactional`이 메서드 경계로 트랜잭션을 그렸다면, FastAPI/SQLAlchemy는 *들여쓰기로* 그린다.

이 패턴이 왜 안전한가를 짚어보자. 첫째, *시작과 끝이 한눈에 보인다.* 메서드 안에 다른 메서드 호출이 끼어들어도 트랜잭션 범위가 흐려지지 않는다. 둘째, 예외가 발생하면 *자동 롤백*이 보장된다 — Spring의 unchecked 자동 롤백과 사실상 같은 안전망이다. 셋째, `commit`이 *응답이 나가기 전*에 호출된다. `with` 블록의 종료는 라우트 함수의 *반환 직전*이라, commit이 실패하면 그 자리에서 예외가 터져 적절한 5xx 응답으로 변환된다.

비교를 위해 Spring 코드를 같은 자리에 놓아보자.

```kotlin
// Spring (Kotlin)
@Service
class TransferService(private val accountRepo: AccountRepository, ...) {

    @Transactional
    fun transfer(fromId: Long, toId: Long, amount: BigDecimal) {
        val src = accountRepo.findByIdForUpdate(fromId)
        val dst = accountRepo.findByIdForUpdate(toId)
        if (src.balance < amount) throw InsufficientBalanceException(fromId)
        src.balance -= amount
        dst.balance += amount
        transferRepo.save(Transfer(src.id, dst.id, amount))
    }
}
```

두 코드를 옆에 놓고 보면 차이가 분명하다. Spring은 `@Transactional` 한 줄이 메서드 전체를 감싸 트랜잭션 범위로 만든다. FastAPI/SQLAlchemy는 `async with db.begin():` 들여쓰기가 같은 역할을 한다. 표현이 *어노테이션 대신 블록*이라는 점만 다르다. 같은 안전망이 다른 모양으로 표현된 셈이다.

그렇다면 의문이 하나 남는다. *블록의 위치*는 어디에 두는 게 좋을까? 라우트일까, 서비스 레이어일까? 이게 다음 절의 주제다.

## 트랜잭션 경계를 어디에 그을지

위 예제에서는 트랜잭션 블록이 라우트 함수 안에 있었다. 학습용으로는 한눈에 들어와서 좋지만, 도메인이 커지면 *서비스 레이어*로 옮기는 게 보통이다. Spring에서 `@Transactional`을 컨트롤러가 아니라 서비스 메서드에 다는 관행과 정확히 같은 이유다.

서비스 레이어로 옮긴 모양은 다음과 같다.

```python
# services/transfer_service.py
class TransferService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def transfer(self, payload: TransferCreate) -> Transfer:
        async with self._db.begin():
            src = await self._db.get(Account, payload.from_id, with_for_update=True)
            dst = await self._db.get(Account, payload.to_id, with_for_update=True)
            if src.balance < payload.amount:
                raise InsufficientBalance(payload.from_id)
            src.balance -= payload.amount
            dst.balance += payload.amount
            transfer = Transfer(from_id=src.id, to_id=dst.id, amount=payload.amount)
            self._db.add(transfer)
            return transfer
```

```python
# routers/transfer_router.py
@router.post("/transfers")
async def create_transfer(
    payload: TransferCreate,
    svc: Annotated[TransferService, Depends(get_transfer_service)],
) -> TransferRead:
    transfer = await svc.transfer(payload)
    return TransferRead.model_validate(transfer)
```

라우트는 *얇아지고*, 서비스가 *진짜 일*을 한다. 트랜잭션 경계는 서비스 메서드 안에 그어졌다. 라우트는 그 위에서 입력 검증과 응답 변환만 책임진다. Spring의 컨트롤러-서비스 분리와 같은 모양이다.

여기서 한 가지 약속을 두고 가자. **트랜잭션은 서비스 레이어에서 시작하고 닫는다.** 라우트는 트랜잭션을 의식하지 않는다. 이 약속은 책 전체에서 그대로 들고 간다 — 9장(예외·관측성)도 이 가정을 전제로 도메인 예외를 짠다.

물론 이 약속에는 *생각해볼 만한 함정*이 하나 있다. 한 요청 안에서 *여러 서비스 메서드*가 호출되면, 각자 자기 트랜잭션을 열기 때문에 *전체로는 트랜잭션이 분리된다.* Spring의 전파(`REQUIRED`)가 자동으로 해결해주던 일을 FastAPI는 *조용히 분리해서* 처리한다. 사용자가 의도한 게 한 트랜잭션이라면, 명시적으로 묶어야 한다. 다음과 같이.

```python
async def transfer_with_audit(self, payload: TransferCreate, audit: AuditLog) -> Transfer:
    async with self._db.begin():
        transfer = await self._transfer_core(payload)   # 같은 세션, 같은 트랜잭션
        await self._audit_log(audit)                    # 같은 세션, 같은 트랜잭션
        return transfer
```

핵심은 *같은 세션을 공유*하고 *바깥에 트랜잭션 블록 하나*를 두는 것이다. 그 안의 내부 메서드들은 트랜잭션을 *시작하지 않는다* — 단지 그 안에서 동작할 뿐이다. Spring의 `Propagation.REQUIRED`가 처리하던 일을 *세션 공유 + 최상위 블록*이라는 단순한 회로로 명시한다. 보이지 않던 게 보이는 자리로 옮겨왔다.

## Unit of Work — Matthew Brown의 비판과 대안

여기까지 따라오면 한 가지 의문이 든다. "세션을 매번 `Depends(get_db)`로 받아서 서비스에 넘기는 게 깔끔한가? Spring의 `@PersistenceContext`처럼 *암묵적으로* 잡혀 있으면 안 되나?" 자연스러운 질문이고, 같은 질문을 한 사람이 이미 있다.

> Matthew Brown의 글이 같은 문제를 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *DI로 long-lived 세션을 라우트 전체에 노출하는 흔한 패턴이 요청-내 longtail 트랜잭션을 만든다*. — "FastAPI database session dependency injection considered harmful" (reference §4.2)

*요청-내 longtail 트랜잭션*. 이 표현이 정확하다. 의존성으로 받은 세션을 라우트 한참 위에서 열고, 라우트 한참 아래에서 닫으면, 그 사이의 모든 시간이 트랜잭션 안에 들어간다. 그 시간 동안 데이터베이스의 락이 잡혀 있고, 다른 요청들이 그 락 뒤에 줄을 선다. 한두 요청이면 모르지만, 트래픽이 늘면 *조용한 성능 하락*으로 돌아온다. 찜찜한 일이다.

Brown의 대안은 *Unit of Work 객체*다. 라우트는 세션을 직접 받지 않고, *Unit of Work 컨텍스트*를 받는다. 그 컨텍스트 안에서만 트랜잭션이 열리고 닫힌다. 코드로 보자.

```python
class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._factory = session_factory

    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._factory()
        await self._session.begin()
        self.accounts = AccountRepository(self._session)
        self.transfers = TransferRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()
        await self._session.close()
```

라우트는 *세션 대신 UoW*를 의존성으로 받는다.

```python
async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork(AsyncSessionLocal) as uow:
        yield uow

@router.post("/transfers")
async def create_transfer(
    payload: TransferCreate,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> TransferRead:
    src = await uow.accounts.get(payload.from_id, lock=True)
    dst = await uow.accounts.get(payload.to_id, lock=True)
    if src.balance < payload.amount:
        raise InsufficientBalance(payload.from_id)
    src.balance -= payload.amount
    dst.balance += payload.amount
    await uow.transfers.add(Transfer(from_id=src.id, to_id=dst.id, amount=payload.amount))
    return TransferRead.model_validate(...)
```

`with` 블록이 사라진 자리에 *UoW의 컨텍스트 매니저*가 들어와 있다. 트랜잭션의 시작과 끝은 UoW의 `__aenter__`/`__aexit__`에 캡슐화됐다. 라우트에서 보면 트랜잭션 시작 구문이 사라진 것처럼 보이지만, *사라진 게 아니라 한 군데로 모아둔 것이다.*

물론 이 패턴에도 비판이 있다. "또 하나의 추상화 레이어를 만들 만한 가치가 있는가?" 작은 프로젝트라면 `async with session.begin()` 직접 쓰는 편이 낫다. 도메인이 셋·넷으로 늘고, 트랜잭션 경계 규칙이 팀 차원의 약속이 되면, UoW가 그 약속을 *코드로* 강제하는 자리에 들어간다. *지금 당장*이 아니라 *언제쯤* UoW로 옮기면 좋을지를 기억해두자 — 보통 도메인 수가 다섯을 넘고, 한 요청 안에서 두 도메인 이상이 같이 변경되는 시나리오가 잦아지는 시점이다.

## 격리·롤백·savepoint

다음으로 짚을 자리는 *트랜잭션의 세 가지 손잡이*다. 격리 수준(isolation level), 롤백, savepoint. Spring 출신이라면 `@Transactional(isolation = Isolation.REPEATABLE_READ)` 같은 코드를 본 적이 있을 것이다. 같은 손잡이가 SQLAlchemy에도 있다 — 그저 어노테이션이 아니라 *연결 옵션*으로 노출돼 있을 뿐이다.

격리 수준부터 보자. Spring의 다섯 가지(`DEFAULT`/`READ_UNCOMMITTED`/`READ_COMMITTED`/`REPEATABLE_READ`/`SERIALIZABLE`)는 데이터베이스 표준의 격리 수준 그대로다. SQLAlchemy에서는 `engine`을 만들 때 또는 *연결 단위로* 격리 수준을 지정한다.

```python
# 엔진 전역 기본값
engine = create_async_engine(DB_URL, isolation_level="REPEATABLE READ")

# 특정 트랜잭션에만 적용 — 연결 옵션을 그 자리에서 바꿈
async with engine.connect() as conn:
    conn = await conn.execution_options(isolation_level="SERIALIZABLE")
    async with conn.begin():
        ...
```

Spring처럼 *메서드 단위*로 격리 수준을 다르게 거는 패턴도 가능하다 — 단지 `@Transactional(isolation=...)` 대신 `execution_options(isolation_level=...)`을 직접 호출하면 된다. 보이지 않던 손잡이가 *눈에 보이는 함수 호출*로 나왔다.

롤백은 어떨까? 이게 Spring 출신이 가장 자주 부딪히는 차이 중 하나다.

> Spring 기본 정책: **unchecked 예외(`RuntimeException` 계열)는 자동 롤백**, checked 예외는 자동 롤백 *안 함*(설정으로 바꿀 수 있음).

SQLAlchemy/Python 진영에는 checked/unchecked 구분이 없다. 모든 예외는 그냥 `Exception`이다. 그래서 SQLAlchemy의 정책은 단순하다 — **`async with session.begin()` 블록 안에서 발생한 모든 예외는 롤백된다.** 블록을 정상 종료하면 commit, 예외가 새어 나가면 rollback. 손에 그리기 쉽다.

savepoint도 그대로 있다. 트랜잭션 안에서 일부만 롤백하고 싶을 때 `begin_nested()`를 쓴다.

```python
async with db.begin():
    await create_user(user)
    try:
        async with db.begin_nested():     # savepoint
            await send_welcome_email_in_db(user)
    except EmailQueueFull:
        # savepoint까지만 롤백, 사용자 생성은 유지
        pass
```

Spring `@Transactional(propagation = Propagation.NESTED)`과 같은 자리다. SQLAlchemy는 savepoint를 *별도의 컨텍스트 매니저*로 노출했다 — 트랜잭션 안의 트랜잭션이 어디서부터 어디까지인지 들여쓰기로 표현된다.

여기서 한 가지 정리를 두자. Spring의 `@Transactional` 한 줄에는 *전파·격리·롤백 규칙·timeout·readOnly* 등 옵션이 잔뜩 박힐 수 있다. SQLAlchemy는 같은 옵션을 *서로 다른 자리에* 분산시켰다. 처음에는 손이 더 많이 가지만, 옵션이 *어디서 적용됐는지* 코드에서 정확히 추적된다. 강점이자 부담이다.

타임아웃과 readOnly는 어떻게 옮겨갈까? `statement_timeout`은 PostgreSQL의 경우 연결 수준에서 `SET LOCAL statement_timeout = '5s'`를 한 줄 실행해주면 된다. readOnly는 SQLAlchemy의 트랜잭션에는 직접 대응되는 플래그가 없지만, *세션 자체를 읽기 전용 엔진*에 묶거나 트랜잭션 시작 후 `SET TRANSACTION READ ONLY` 한 줄을 호출하는 패턴이 일반적이다. Spring처럼 어노테이션 한 줄로 끝나는 우아함은 없다 — 대신 *어떤 SQL이 실제로 실행되는지*가 한눈에 보인다. 어느 쪽이 더 좋은가는 취향이지만, *디버깅이 필요한 순간*에는 두 번째 쪽이 훨씬 친절하다.

한 가지 더. **`with_for_update`로 거는 비관적 락**은 트랜잭션의 손잡이 중 가장 자주 쓰는 자리다. 송금 같이 *두 행을 동시에 잠가야* 안전한 시나리오에서는 락 *순서*도 신경 써야 한다. 두 트랜잭션이 같은 두 계좌를 반대 순서로 잠그면 데드락이 난다. Spring/Hibernate에서도 같은 문제가 있어서 *계좌 ID 오름차순으로 락을 거는* 관행이 굳어 있다. SQLAlchemy도 똑같다 — `payload.from_id`와 `payload.to_id` 중 *작은 쪽을 먼저* 잠그는 게 안전하다. 다음과 같이.

```python
first_id, second_id = sorted([payload.from_id, payload.to_id])
first = await db.get(Account, first_id, with_for_update=True)
second = await db.get(Account, second_id, with_for_update=True)
```

이 한 줄을 빼먹으면 *부하가 늘었을 때* 조용히 데드락이 일어난다. PostgreSQL은 친절하게 한 트랜잭션을 죽이고 에러를 던지지만, 그 시간 동안 사용자는 *느린 응답*을 받는다. 끔찍한 일은 아닌데 *번거롭다.* 송금 코드를 짤 때마다 락 순서를 의식하는 습관을 들여두자.

## 예외와 롤백 — 자동의 자리에 명시가 들어선다

좀 더 풀어보자. Spring의 unchecked 자동 롤백은 우리가 평소에 의식하지 않는 안전망이다. 컨트롤러 메서드 안에서 `IllegalArgumentException`이 터지면, Spring이 알아서 트랜잭션을 롤백하고 예외를 위로 던진다. 우리가 한 일은 *예외를 던진 것뿐*이다.

FastAPI/SQLAlchemy에서 같은 시나리오를 따라가보자.

```python
@router.post("/transfers")
async def create_transfer(payload: TransferCreate, svc: ...) -> TransferRead:
    transfer = await svc.transfer(payload)
    return TransferRead.model_validate(transfer)
```

서비스 안에서 `InsufficientBalance` 예외가 던져졌다고 하자.

```python
async def transfer(self, payload: TransferCreate) -> Transfer:
    async with self._db.begin():
        ...
        if src.balance < payload.amount:
            raise InsufficientBalance(payload.from_id)
        ...
```

`raise InsufficientBalance(...)`가 호출되면 `async with self._db.begin():` 블록의 `__aexit__`가 예외와 함께 호출된다. SQLAlchemy는 *예외가 있으면 rollback*이라는 단순한 규칙으로 트랜잭션을 정리한다. 그리고 예외는 라우트로 다시 던져진다. 라우트는 9장에서 다룰 `@app.exception_handler(InsufficientBalance)`로 이 예외를 잡아 적절한 4xx 응답으로 변환한다. 한 줄도 자동인 게 없다 — 그런데 *모두 추적 가능하다.*

비교를 이렇게 정리하자. Spring은 *기본값이 안전*이다. 예외를 던지면 롤백된다. 손이 닿지 않으면 기본 정책이 작동한다. SQLAlchemy는 *명시가 안전*이다. `with` 블록 안에서 예외가 새어 나가면 롤백되고, 블록 바깥에서 발생하면 트랜잭션조차 시작되지 않은 상태다. 둘 다 결과는 같은 안전망인데 *어느 쪽이 책임지는가*가 다르다.

여기서 흔히 빠지는 함정 하나. 다음 코드를 보자.

```python
# 잘못된 패턴
async def transfer(self, payload: TransferCreate) -> Transfer:
    src = await self._db.get(Account, payload.from_id)   # 블록 바깥
    async with self._db.begin():
        if src.balance < payload.amount:
            raise InsufficientBalance(payload.from_id)
        ...
```

`db.get(Account, ...)`가 *블록 바깥*에 있다. SQLAlchemy의 비동기 세션은 자동으로 *기본 트랜잭션*을 시작하기도 하지만, 명시적인 `begin()` 블록 바깥의 쿼리가 *어느 트랜잭션*에 속하는지는 종종 헷갈린다. 권장하는 건 *모든 쿼리를 begin 블록 안*에 두는 것이다. 손에 익으면 자연스럽지만 처음에는 *어디까지 안에 둬야 할지* 살짝 헷갈리니, 한 번 머리에 새겨두자.

## 테스트에서의 트랜잭션 — 자동 롤백의 빈자리

Spring 출신이 첫 FastAPI 테스트를 짤 때 한 번은 멈칫하는 자리가 있다. 테스트 사이에 *DB 상태*가 어떻게 정리되는가?

Spring에서 `@SpringBootTest @Transactional`을 메서드에 달면 테스트가 끝날 때 자동으로 롤백된다. 한 테스트가 만든 데이터는 다음 테스트에 안 보인다. 깔끔하다. FastAPI/pytest는 그 자동을 *기본값으로 안 준다.* 무방비로 짜면 첫 테스트가 만든 데이터가 두 번째 테스트로 새어 나간다. 찜찜하고 디버깅이 까다로워진다.

대안은 두 가지다.

**첫째, savepoint 기반 fixture.** 각 테스트가 *외부 트랜잭션* 안에서 실행되고, 테스트 안의 `commit()`은 *savepoint commit*으로 가도록 한다. 테스트가 끝나면 외부 트랜잭션을 통째로 롤백한다.

```python
@pytest_asyncio.fixture
async def db_session():
    async with engine.connect() as conn:
        await conn.begin()
        async with AsyncSession(bind=conn, join_transaction_mode="create_savepoint") as session:
            yield session
        await conn.rollback()
```

`join_transaction_mode="create_savepoint"`가 핵심이다. 세션의 `commit()`이 *진짜 commit*이 아니라 *savepoint commit*으로 매핑된다. 테스트가 끝나면 외부 connection의 `rollback()`이 *모든 것을* 되돌린다. Spring의 `@Transactional` 테스트와 같은 효과다.

**둘째, truncate 기반.** 매 테스트 후에 모든 테이블을 truncate한다. 단순하지만, 테이블이 많아지면 느려진다. CI에서 테스트 수가 수백 개를 넘으면 첫 번째 패턴이 낫다.

자세한 픽스처 패턴은 10장(테스트)에서 다시 다룬다. 이 챕터에서 짚어둘 건 한 가지다 — **테스트에서의 자동 롤백도 *우리가 짜는 자리*다.** Spring이 무료로 주던 안전망이 FastAPI에서는 한 번의 픽스처 설계로 옮겨왔다. 한 번 잘 짜두면 그다음 모든 테스트가 그 위에서 안전해진다.

## 송금 시나리오 — 양면 페이지 대조

지금까지의 모든 조각을 모아 송금 API를 두 프레임워크로 짠 모습을 양면 페이지에 두고 보자. 같은 도메인, 같은 안전성, 다른 표현.

**Spring (Kotlin):**

```kotlin
@Service
class TransferService(
    private val accountRepo: AccountRepository,
    private val transferRepo: TransferRepository,
) {
    @Transactional
    fun transfer(fromId: Long, toId: Long, amount: BigDecimal): Transfer {
        val src = accountRepo.findByIdForUpdate(fromId)
            ?: throw AccountNotFound(fromId)
        val dst = accountRepo.findByIdForUpdate(toId)
            ?: throw AccountNotFound(toId)
        if (src.balance < amount) {
            throw InsufficientBalance(fromId)
        }
        src.balance -= amount
        dst.balance += amount
        return transferRepo.save(Transfer(src.id, dst.id, amount))
    }
}

@RestController
@RequestMapping("/transfers")
class TransferController(private val service: TransferService) {

    @PostMapping
    fun create(@RequestBody @Valid req: TransferRequest): TransferResponse {
        val transfer = service.transfer(req.fromId, req.toId, req.amount)
        return TransferResponse.from(transfer)
    }
}
```

`@Transactional` 한 줄이 메서드 전체를 감싸 트랜잭션 범위로 만든다. 비즈니스 로직 다섯 줄이 안전망 안에 들어간다.

**FastAPI:**

```python
# services/transfer_service.py
class TransferService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def transfer(self, payload: TransferCreate) -> Transfer:
        async with self._db.begin():
            src = await self._db.get(Account, payload.from_id, with_for_update=True)
            if src is None:
                raise AccountNotFound(payload.from_id)
            dst = await self._db.get(Account, payload.to_id, with_for_update=True)
            if dst is None:
                raise AccountNotFound(payload.to_id)
            if src.balance < payload.amount:
                raise InsufficientBalance(payload.from_id)
            src.balance -= payload.amount
            dst.balance += payload.amount
            transfer = Transfer(
                from_id=src.id, to_id=dst.id, amount=payload.amount,
            )
            self._db.add(transfer)
            await self._db.flush()
            return transfer


# routers/transfer_router.py
@router.post("", response_model=TransferRead, status_code=201)
async def create_transfer(
    payload: TransferCreate,
    svc: Annotated[TransferService, Depends(get_transfer_service)],
) -> Transfer:
    return await svc.transfer(payload)
```

`async with self._db.begin():` 블록이 같은 안전망을 그린다. `with_for_update=True`가 Spring의 비관적 락(`findByIdForUpdate`)과 정확히 같은 일을 한다. 블록 안에서 던진 모든 예외는 자동으로 롤백되고, 블록을 정상 종료하면 commit이 나간다.

두 코드를 옆에 놓고 보면 어디가 같고 어디가 다른지 한눈에 잡힌다. **트랜잭션의 시작과 끝**: Spring은 메서드 시그니처 위의 어노테이션, FastAPI는 들여쓰기로 묶인 블록. **락**: Spring은 레포지토리 메서드 이름(`findByIdForUpdate`), FastAPI는 쿼리 옵션(`with_for_update=True`). **롤백**: Spring은 unchecked 예외 자동, FastAPI는 블록 안 예외 자동. **commit 시점**: Spring은 메서드 반환 직후, FastAPI는 `with` 블록 종료 직후 — 둘 다 응답이 나가기 전이다.

이 평행성을 손에 익히면 6장의 모든 패턴이 *Spring의 자리에 무엇이 들어가는지* 같은 회로로 옮겨진다. **자동의 자리에 명시가 들어선다.** 이 한 줄을 가슴에 새겨두자.

## 한 호흡으로 정리

머리에 박혀야 할 건 셋이다.

**첫째, 트랜잭션은 우리가 시작하고 우리가 닫는다.** `@Transactional`이 자동으로 그리던 경계를 `async with session.begin():` 블록의 들여쓰기로 직접 그린다. *어디서 시작하고 어디서 닫히는지*가 코드 위에 드러나는 게 SQLAlchemy의 명시성 철학이다. 손이 잠시 더 가지만, 그 손길이 곧 안전망이다.

**둘째, 의존성 `finally`에서 `commit`하지 말자.** 응답이 이미 나간 *뒤*다. `get_db()`는 세션을 열고 닫는 일만 하고, commit과 rollback은 *라우트 또는 서비스 레이어 안*에서 명시한다. 이 한 줄이 부분 실패의 가장 흔한 함정을 막는다. 그리고 트랜잭션 경계는 *서비스 레이어*에 둔다는 약속을 책 전체에서 들고 간다.

**셋째, Spring의 옵션은 SQLAlchemy의 *서로 다른 자리*로 분산됐다.** 전파는 *세션 공유 + 최상위 블록*, 격리는 `execution_options(isolation_level=...)`, savepoint는 `begin_nested()`. 보이지 않던 손잡이가 *눈에 보이는 함수 호출*로 나왔다. 처음에는 *어디 있나 찾는* 부담이 있지만, 익숙해지면 *옵션이 어디서 적용됐는지* 정확히 추적된다.

다음 장은 인증·인가다. `@Transactional`이 사라진 자리에 `async with session.begin():`이 들어선 것처럼, 7장에서는 `@PreAuthorize("hasRole('ADMIN')")`이 사라진 자리에 `Depends(require_scope("admin"))`이 들어선다. 6·7장이 공유하는 통주저음은 한 단어다 — **명시성.** Spring Security가 무료로 막아주던 안전망을 *어떻게 명시적으로 그릴지*를 같은 회로로 풀어보자. 손에 익은 6장의 감각이 그대로 7장의 안전망 그리는 데 쓰인다. 기억해두자 — 자동의 자리에 명시가 들어선다. 이 한 줄이 책의 6·7장을 연결하는 다리다.


---

# 7장. 인증·인가 — Spring Security 없이 OAuth2/JWT

Spring 진영에서 보안은 — 한 줄로 표현하면 — *마법사가 가려둔 안전망*이었다.

`@EnableWebSecurity` 한 줄, `SecurityFilterChain` 한 빈, `@PreAuthorize("hasRole('ADMIN')")` 한 어노테이션. CSRF 토큰, 세션 고정 방어, 비밀번호 인코더, 폼 로그인 페이지 — 다 자동으로 켜져 있었다. 우리가 끄려고 *의식적으로* 한 줄을 추가하지 않으면 끄지지 않았다. *안전한 기본값이 켜진 상태*에서 시작하는 모델이었다.

FastAPI는 정반대다. *안전한 기본값을 우리 손으로 켠다.* `@EnableWebSecurity` 한 줄에 해당하는 자리가 — *없다.* 이 사실을 처음 들으면 좀 무겁다. 라우트마다 보안을 짜라는 건가? Spring Security가 1만 줄 가까이 짜둔 코드를 — 내가 다시 짜라는 건가?

답은 다행히 그건 아니다. 보안 자체를 다시 짜진 않는다. 우리가 짜는 건 — *어디에 어떻게 의존성을 꽂을지*다. 그 의존성이 안에서 검증을 한다. 6장에서 트랜잭션 경계를 *우리 손으로 명시*했던 그 감각이 — 이번 장에서 한 번 더 흐른다. *자동에서 명시로의 전환*. 6·7장이 책의 통주저음이 되는 이유다.

이 장에서 우리가 손에 익혀야 할 건 셋이다. *토큰을 검증하는 의존성*, *역할·스코프 기반 권한 검사*, *비밀번호와 시크릿을 다루는 손길*. 그리고 한 가지 더 — Spring Security가 자동으로 막아주던 *CSRF·세션 고정* 같은 항목을 — 우리가 *알고* 책임지는 손길이다. 차근차근 만져보자.

## 리소스 서버 패턴 — FastAPI는 발급보다 검증에 집중한다

먼저 한 가지 사고 전환부터 해두자. Spring Security를 떠올리면 *로그인 폼·세션·인증 매니저*가 한 그림 안에 다 들어 있었다. FastAPI 진영의 권고는 좀 다르다.

PyCon US 2026의 한 발표가 한 줄로 정리한다 — "**FastAPI 앱은 사용자 로그인 자격증명을 처리하거나 토큰을 발급하지 않는다.** 신뢰하는 인가 서버가 발급한 토큰을 검증하고, 그 클레임으로 권한을 결정하는 *리소스 서버 패턴*을 권장한다." ([PyCon US 2026: FastAPI Security Patterns](https://us.pycon.org/2026/schedule/presentation/34/))

이 권고가 무엇을 가리키는가? *인증 책임을 분리하라*는 신호다. 큰 시스템이라면 — 인가 서버(Keycloak, Auth0, AWS Cognito, 사내 SSO)가 *토큰 발급*을 책임지고, FastAPI 앱은 *그 토큰을 검증하고 권한을 풀어내는* 일에 집중한다. 책임이 둘로 나뉜다.

Spring 사고로 옮기자면 — *Spring Cloud Gateway + 별도 OAuth2 서버 + 백엔드 마이크로서비스*의 분리 패턴에 가깝다. 하나의 모놀리스에 모든 게 들어 있던 시절의 Spring Security `formLogin()` 자리와는 결이 다르다.

작은 시스템이라면? FastAPI 앱이 *발급도 같이 한다.* 그게 흔하다. 다만 *발급과 검증을 분리해 짜는 사고*는 — 작은 시스템에서도 유지하는 게 낫다. 토큰을 발급하는 라우트는 한 곳(`/auth/login`), 토큰을 검증하는 의존성은 따로(`Depends(get_current_user)`). 분리해두면 인가 서버를 외부로 빼는 날이 와도 *큰 수술이 안 든다*.

이 책의 예제도 그 분리를 따른다. 본격적으로 코드를 만져보자.

## `pydantic-settings` — 시크릿을 다루는 표준 자리

코드를 짜기 전에 *시크릿을 어디 둘 것인가*부터 정리하자. JWT 비밀 키, 알고리즘, 토큰 만료 시간 같은 값들이다. 하드코딩은 — 끔찍한 일이다. `os.environ.get("JWT_SECRET")` 식의 흩어진 접근도 — 찜찜하다.

Spring 진영에서 우리는 `@Value("${jwt.secret}")` 또는 `@ConfigurationProperties(prefix = "jwt")`를 썼다. application.yml에 값이 모이고, 클래스에 *타입 검증된 상태로* 주입됐다. *값이 비어 있으면 시작 자체가 실패*하는 안전망이 있었다.

FastAPI 진영의 같은 자리에 들어오는 도구가 `pydantic-settings`다. 이 책에서 처음 정식으로 데뷔하는 친구다.

```python
# 파이썬 - app/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_minutes: int = 30
    jwt_refresh_token_expires_days: int = 14

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()      # 모듈 import 시 한 번만 평가된다
```

```bash
# .env
JWT_SECRET=do-not-commit-me-please-rotate-in-production
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/app
```

이 짧은 클래스가 — Spring `@ConfigurationProperties`가 해주던 일을 거의 그대로 한다.

**첫째, 환경 변수에서 값을 자동으로 읽어온다.** `.env` 파일이 있으면 거기서도 읽는다. Pydantic이 알아서 매핑한다.

**둘째, 타입 검증을 강제한다.** `jwt_secret: str`이면 *반드시 문자열로 채워져야 한다*. 빈 값이면 — *애플리케이션이 시작조차 안 한다*. Spring의 `@Value` + `@PostConstruct` 검증 조합을 한 번에 받는다.

**셋째, 기본값이 가능하다.** `jwt_algorithm: str = "HS256"` 같은 식으로. *프로덕션에서 반드시 채워야 하는 값*과 *기본값이 있는 값*이 코드 위에 분명히 보인다.

**넷째, 모듈 레벨 변수로 한 번만 평가된다.** Python의 모듈 import 의미론이 그대로 작동한다. `settings = Settings()`가 한 번만 호출된다. 어디서 import해도 같은 객체다.

7장 본문에서 우리는 이 `settings` 객체를 *어디든 import해서* 쓴다. JWT 비밀 키를 토큰 발급에 쓰고, 만료 시간을 검증에 쓰고, 알고리즘을 양쪽에서 공유한다. 11장 배포에서는 — 같은 `settings`가 *Kubernetes Secret*에서 환경 변수로 흘러 들어오는 흐름을 만진다. 4장에서 깐 *모듈 레벨 싱글톤* 패턴과 같은 줄기다.

여기서 한 가지 짚고 가자. *왜 `Depends`로 안 받고 모듈 레벨 변수로 두는가?* 합리적인 의문이다. 답은 — 둘 다 가능하지만 *기본값*은 모듈 변수다. 설정은 *변하지 않는다*. 테스트에서 시크릿을 갈아끼우고 싶다면 — `pydantic-settings`의 `model_validate` 또는 환경 변수 오버라이드로 충분하다. 매 라우트마다 `Depends(get_settings)`를 다는 비용이 — 얻는 것보다 크다는 게 한국 velog의 [FastAPI Good Practice](https://velog.io/@wjddn3711/FastAPI-Good-Practice) 글의 톤이다. 단, *테스트에서 의존성 오버라이드로 갈아끼우고 싶은 경우*에 한해서는 4장에서 본 `@lru_cache` + `Depends` 패턴이 더 낫다. 둘을 골라 쓰자.

## 토큰 발급 — `/auth/login` 한 라우트

이제 본격적인 코드다. 사용자가 username/password를 보내면 JWT를 돌려주는 라우트.

```python
# 파이썬 - app/auth/schemas.py
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCredentials(BaseModel):
    username: str
    password: str
```

```python
# 파이썬 - app/auth/security.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, scopes: list[str]) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expires_minutes
    )
    payload = {
        "sub": subject,
        "scopes": scopes,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
```

```python
# 파이썬 - app/auth/router.py
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends
from app.auth.schemas import TokenResponse
from app.auth.security import verify_password, create_access_token
from app.users.repository import UserRepository
from app.users.deps import UserRepoDep

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: UserRepoDep,
):
    user = await repo.find_by_username(form.username)
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.username, scopes=user.scopes)
    return TokenResponse(access_token=token)
```

한 줄 한 줄 따라가 보자.

**`OAuth2PasswordRequestForm`** — FastAPI가 제공하는 표준 폼 의존성이다. OAuth2 표준이 정한 `application/x-www-form-urlencoded` 본문(`username=...&password=...&grant_type=password`)을 자동으로 파싱한다. Spring의 `@RequestParam("username") String username` 두 줄을 한 줄로 합친 모양이다.

**`verify_password`** — `passlib`의 `bcrypt` 백엔드. 매 호출이 *수십 밀리초* 정도 걸린다. *느려야 안전한 함수*다. 빠르면 무차별 대입에 약해진다. 이 점을 기억해두자.

**`HTTPException` + `WWW-Authenticate: Bearer` 헤더** — OAuth2 표준이 권하는 401 응답 모양. `/docs`의 Swagger UI에서 *로그인 버튼*이 보이려면 이 헤더가 있어야 한다.

**`create_access_token`** — `jose` 라이브러리로 JWT를 발급한다. `subject`(`sub` 클레임)에 사용자 식별자, `scopes`에 권한 목록, `exp`에 만료 시간을 박는다. 만료가 없는 JWT는 — *끔찍한 일이다*. 잊지 말자.

Spring 사고로 옮기면 — `@PostMapping("/auth/login")` + `AuthenticationManager.authenticate()` + `JwtBuilder` 조합을 *세 함수에 평면적으로 펼친 모양*이다. *어디서 무엇이 일어나는지*가 코드 위에 분명히 보인다. *Spring Security가 가려놓던 안전망*이 — 우리 손에 와 있는 형국이다.

## 토큰 검증 — `Depends(get_current_user)`

자 이제 *발급된 토큰을 검증하는 자리*다. 이게 4장에서 깔아둔 `Depends` 패턴이 — 보안 영역에서 *진가를 보이는* 자리이기도 하다.

```python
# 파이썬 - app/auth/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from app.core.settings import settings
from app.users.repository import UserRepository
from app.users.deps import UserRepoDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class TokenPayload(BaseModel):
    sub: str
    scopes: list[str] = []
    exp: int

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: UserRepoDep,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명을 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        raw = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        payload = TokenPayload.model_validate(raw)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = await repo.find_by_username(payload.sub)
    if user is None:
        raise credentials_exception
    return user

CurrentUserDep = Annotated["User", Depends(get_current_user)]
```

```python
# 파이썬 - app/users/router.py
from app.auth.deps import CurrentUserDep

@router.get("/me")
async def read_me(user: CurrentUserDep):
    return {"username": user.username, "scopes": user.scopes}
```

한 함수가 — *모든 보호된 라우트*를 한 줄로 받친다. `user: CurrentUserDep`을 적기만 하면 그 라우트는 자동으로 인증을 요구한다. 토큰이 없거나 만료됐거나 변조됐으면 — 401이 나간다. 라우트 함수의 본문은 *이미 검증된 사용자*만 받는다.

Spring `@PreAuthorize("isAuthenticated()")` 한 줄과 거의 동등하다. 형태만 다르다. *어노테이션*이 *함수 파라미터의 마커*로 바뀌었을 뿐이다.

여기서 6장과의 통주저음을 한 번 더 짚자. 6장에서 우리는 *트랜잭션 경계*를 `async with session.begin():`으로 명시했다. 7장에서 우리는 *인증 경계*를 `user: CurrentUserDep`로 명시한다. 둘 다 — Spring이 어노테이션 한 줄로 가려두던 *횡단 관심*이 — 함수 시그니처 *위에* 평면적으로 드러난다. 6장과 7장의 호흡이 같다는 게 — 이 자리에서 느껴진다.

## "그러면 한 번 빠뜨리면 사고 나는 거 아닌가?"

여기서 한 번 마음에 걸리는 의문이 따라온다. 1장에서 우리가 미리 짚었던 그 질문이다.

라우트가 50개, 100개로 늘면 — *`CurrentUserDep`을 빠뜨리는 사고*가 안 날 수 있나? Spring처럼 *전역 기본값이 인증 필수*라면, 안 빠뜨리는 게 *기본 동작*이다. FastAPI에선 — 빠뜨리면 그냥 빠진다.

한 보고서가 이걸 두고 "FastAPI 보안 이슈 7건 vs Spring Boot 1건"이라는 숫자를 던졌다 ([Medium 6개월 비교](https://medium.com/engineering-playbook/fastapi-vs-spring-boot-i-tested-both-for-6-months-in-production-96c04f7ebabe), 한 회사의 케이스 단서는 붙는다).

이 신호를 두 가지 손길로 받아내자.

**첫째, 도메인 단위로 *기본 보호*를 깐다.** `APIRouter` 자체에 `dependencies`를 줄 수 있다.

```python
# 파이썬 - app/admin/router.py
from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user)],     # 이 router의 모든 라우트가 자동 보호
)

@router.get("/users")
async def list_users():
    ...      # 인증된 사용자만 도달한다
```

`/admin/*` 라우트는 *모두* 인증을 요구한다. 새 라우트를 추가해도 자동으로 보호된다. 빠뜨릴 가능성이 *router 단위로* 좁아진다.

**둘째, *체크리스트 사고*를 손에 익힌다.** 1장에서 예고한 그 손버릇이다. PR 리뷰 때 — *모든 새 라우트마다* 한 번씩 묻는다.

- 이 라우트는 인증이 필요한가? `CurrentUserDep`가 박혀 있는가?
- 권한 검증이 필요한가? `Security(..., scopes=[...])`가 적절한가?
- 입력은 검증되는가? Pydantic 모델로 받는가?
- 응답은 민감 정보를 흘리지 않는가? `UserInDB` 같은 모델이 그대로 나가지 않는가?

이 네 질문이 — Spring Security가 *자동으로 던지던 질문*이다. 자동이 없는 세상에선 — *우리 손이 던진다*. 도구가 도와줄 수 있는 영역도 있다. `ruff` + `flake8`이 *함수 파라미터에 `CurrentUserDep`가 없는 라우트 데코레이터*를 잡아내는 룰을 — 사내 표준으로 짤 수도 있다. 한 번 짜두면 자동화된다.

이건 무거운 일인가? 처음엔 그렇다. *모든 라우트마다 한 줄을 적는 손버릇*이 — Spring의 *기본값이 안전*이었던 세상보다 한 단계 더 의식적이다. 익숙해지면 — *어디에 무엇이 적용되는지가 코드 위에서 보이는* 형태가 오히려 든든하다. 4장의 *AOP 없음*과 같은 호흡이다.

## 스코프 기반 RBAC — `Security(..., scopes=[...])`

인증이 됐다고 *모든* 권한이 따라오진 않는다. *어드민만 접근 가능한 라우트*, *결제 권한이 있는 사용자만 호출 가능한 액션*. Spring의 `@PreAuthorize("hasRole('ADMIN')")`이 하던 일을 — FastAPI에선 *스코프 기반 RBAC*로 다룬다.

스코프 지원이 필요한 자리에서는 `OAuth2PasswordBearer`를 *그대로* 쓰되, 라우트의 의존성을 `Security(...)`로 바꾼다.

```python
# 파이썬 - app/auth/deps.py (확장)
from fastapi import Security
from fastapi.security import SecurityScopes

async def get_current_user_with_scopes(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: UserRepoDep,
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명을 확인할 수 없습니다.",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        raw = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        payload = TokenPayload.model_validate(raw)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = await repo.find_by_username(payload.sub)
    if user is None:
        raise credentials_exception

    for required in security_scopes.scopes:
        if required not in payload.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="권한이 부족합니다.",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user
```

```python
# 파이썬 - app/admin/router.py
from fastapi import Security
from app.auth.deps import get_current_user_with_scopes

@router.get("/users")
async def list_admin_users(
    user: Annotated["User", Security(get_current_user_with_scopes, scopes=["admin"])],
):
    ...
```

`Security(...)`는 `Depends(...)`와 거의 같지만 — *스코프*라는 메타데이터를 더 받는다. 그 스코프가 — `OpenAPI` 문서에까지 자동으로 반영된다. `/docs`에서 라우트마다 *어떤 스코프가 필요한지*가 보인다.

Spring `@PreAuthorize("hasRole('ADMIN')")` 한 줄에 비하면 *몇 줄 더 적힌다*. 다만 두 가지 이득이 있다.

**첫째, OpenAPI 문서에 자동 반영된다.** Spring 진영에서는 *어노테이션은 SecurityFilterChain에만 적용*되고 OpenAPI 문서에 권한을 노출하려면 *별도 어노테이션*이 필요했다. FastAPI는 *한 번에* 처리된다.

**둘째, 스코프 검증 로직이 *우리 코드*다.** Spring Security의 SpEL 표현식(`hasRole`, `hasAuthority`, `@Pre*`)이 *프레임워크 내부 평가기*를 거치는 데 비해 — FastAPI는 우리가 짠 함수 한 개가 *전부*다. *어떻게 검증하는지* 코드 위에 보인다.

`Role`이 아니라 `Scope`라는 이름인 이유도 짚자. OAuth2 표준의 용어다. *Spring의 Role*과 *OAuth2의 Scope*는 — *권한 검사*라는 기능은 같지만 *모델*이 다르다. Scope는 *토큰에 어떤 권한이 담겨 있는가*를 가리키고, Role은 *사용자에게 어떤 역할이 부여돼 있는가*를 가리킨다. 분산 시스템과 잘 어울리는 모델은 — 사실 Scope다. 한 사용자가 *어떤 토큰*을 들고 있느냐에 따라 *그 순간에 무엇을 할 수 있는가*가 정해진다. 자연스럽다.

## 비밀번호 — `passlib` + `bcrypt` 또는 `argon2`

해싱 라이브러리 선택 한 번 짚고 가자.

```python
# 파이썬 - 권장 패턴 (재게재)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

`passlib`은 *해싱 알고리즘 추상화 계층*이다. Spring `PasswordEncoder` 인터페이스와 비슷한 자리다. 알고리즘이 발전하면 — *기존 해시는 검증하면서 새 해시는 새 알고리즘으로*라는 정책을 한 줄로 표현할 수 있다.

스킴 선택. 두 가지를 알아두자.

- **`bcrypt`** — *가장 무난한 기본값*. 1999년에 나온 검증된 알고리즘. `passlib`의 가장 안정적인 백엔드. 대부분의 시스템이 이걸로 시작한다.
- **`argon2`** — 2015년 [패스워드 해싱 대회](https://www.password-hashing.net/) 우승작. GPU·ASIC 저항성이 더 강하다. 신규 시스템이라면 검토해볼 만하다. 다만 *조직의 마이그레이션 비용*과 *생태계 성숙도*를 함께 봐야 한다.

선택 자체보다 — *느린 게 정상*이라는 사실을 마음 한구석에 박아두자. 로그인 호출이 100ms 걸린다고 *성능 최적화 대상*으로 잡으면 *안전이 깨진다*. 빠른 해시는 — 무차별 대입에 약하다.

저장은 평문 절대 금지. `User` 모델에 `hashed_password` 필드만 두고, 평문은 *메모리에도 잠깐만* 머문다.

```python
# 파이썬 - app/users/models.py (발췌)
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
```

응답 모델에서 `hashed_password`가 *밖으로 나가지 않게* 분리하는 손길도 잊지 말자. 3장에서 우리가 깐 `UserCreate` / `UserRead` / `UserInDB` 패턴이 — 이 자리에서 *진짜 가치*를 보인다.

## Spring Security가 무료로 막아주던 것들

자, 이제 *Spring Security가 자동으로 막아주던 항목*들이다. 우리 손으로 *알고* 다뤄야 하는 영역.

### CSRF — 의식적으로 끄거나 켜기

Spring Security는 *기본 CSRF 보호*가 켜져 있다. 폼 POST는 *CSRF 토큰*이 없으면 거부됐다. SPA 진영에서는 `csrf().disable()` 한 줄로 *의식적으로 끄는* 것이 흔했다.

FastAPI는 — *CSRF 보호가 기본으로 없다.* 토큰 기반 API(`Authorization: Bearer ...`)는 *CSRF에 본질적으로 덜 취약*하다. 브라우저가 쿠키를 자동으로 보내는 *동일 출처* 공격이 — 토큰이 별도 헤더에 실리는 모델에서는 약해진다.

다만 *쿠키에 토큰을 저장하는 SPA*라면 이야기가 다르다. 그때는 — CSRF를 직접 다뤄야 한다. `fastapi-csrf-protect` 같은 외부 라이브러리가 있다. 또는 `SameSite=Strict` 쿠키 + 별도 헤더 검증 같은 손길도 흔한 패턴이다.

**핵심 결정 한 줄.** *토큰을 어디 저장하느냐*가 CSRF 책임을 결정한다. `Authorization` 헤더면 — 보통 안전. 쿠키면 — *직접 책임진다.* 헷갈리지 말자.

### 세션 고정 — 사실 세션이 없다

Spring Security의 *세션 고정 공격 방어*는 — 인증 성공 후 *세션 ID를 새로 발급*하는 패턴이었다. FastAPI 진영의 표준 패턴(*토큰 기반*)은 — 사실 *세션 자체가 없다*. 매 요청이 토큰을 다시 보낸다. 세션 고정이 끼어들 자리가 — 거의 없다.

다만 *쿠키 + 세션*을 일부러 쓴다면? Starlette의 `SessionMiddleware`가 있다. 그때는 — *로그인 후 세션 키 회전*을 직접 구현해야 한다. 흔한 패턴은 아니다. 토큰 기반이 *기본 권고*인 이유이기도 하다.

### HTTPS — 인프라 책임

JWT를 평문 HTTP로 보내는 건 — *끔찍한 일이다.* 토큰이 그대로 노출된다. *HTTPS는 협상 가능한 항목이 아니다.* 11장 배포에서 — *프록시 + TLS 종료* 패턴으로 다시 만난다. 지금은 그저 *애플리케이션 코드의 책임은 아니지만, 운영자의 의무*라는 사실만 기억해두자.

### 토큰 회전과 짧은 만료

JWT의 가장 큰 약점은 — *발급된 토큰을 취소하기 어렵다*는 점이다. 비밀번호를 바꿔도 — *이미 발급된 토큰은 만료까지 유효*하다. 대응은 두 갈래.

- **짧은 액세스 토큰 + 긴 리프레시 토큰.** 액세스 토큰은 15~30분. 리프레시 토큰은 7~14일. 짧을수록 *유출의 노출 시간*이 짧다.
- **블랙리스트.** Redis 같은 데에 *취소된 토큰의 jti*를 모아두고, 검증 의존성에서 확인한다. 정직한 비용이 든다.

큰 시스템이라면 — *HS256 대신 RS256*도 검토하자. *비대칭 키*면 — 검증 서버에는 *공개 키*만 두면 된다. 서명 키 노출 위험이 한 단계 줄어든다.

이 결정들은 — *조직의 위협 모델*에 따라 달라진다. 책에서 한 답을 박을 자리는 아니다. 다만 *어떤 결정이 어떤 함의를 가지는지*는 알고 가자.

## 한 흐름으로 — `/auth/login` → `/me` → `/admin/users`

지금까지 본 조각들을 한 흐름에 모아보자. 7장의 모든 도구가 *한 도메인* 안에 작동하는 모습이다.

```python
# 파이썬 - app/main.py
from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.admin.router import router as admin_router

app = FastAPI(title="Sample API")
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
```

```bash
# 사용 시나리오

# 1. 로그인 → 토큰 발급
curl -X POST http://localhost:8000/auth/login \
  -d "username=alice&password=secret-pw" \
  -H "Content-Type: application/x-www-form-urlencoded"
# {"access_token":"eyJhbGc...","token_type":"bearer"}

# 2. 내 정보 조회 (인증 필요)
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer eyJhbGc..."
# {"username":"alice","scopes":["admin"]}

# 3. 어드민 라우트 (admin 스코프 필요)
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer eyJhbGc..."
# [{"id":1,"username":"alice"}, ...]

# 4. 토큰 없이 보호 라우트 → 401
curl http://localhost:8000/users/me
# {"detail":"Not authenticated"}
```

한 흐름이 깔끔하게 흐른다. *발급 → 검증 → 권한 확인 → 응답*. Spring Security의 *15개쯤 되는 필터 체인*이 — 코드 위에 *몇 함수의 시퀀스*로 평면적으로 펼쳐진 모양이다.

테스트는 — 4장에서 익힌 `app.dependency_overrides` 패턴이 그대로 쓰인다.

```python
# 파이썬 - tests/test_admin.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.deps import get_current_user_with_scopes

class FakeAdminUser:
    username = "admin"
    scopes = ["admin"]

@pytest.fixture
def admin_client():
    app.dependency_overrides[get_current_user_with_scopes] = lambda: FakeAdminUser()
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_admin_can_list_users(admin_client):
    response = admin_client.get("/admin/users")
    assert response.status_code == 200
```

Spring `@WithMockUser(roles = "ADMIN")` 한 줄에 비하면 — *조금 더 명시적*이다. 다만 *어디서 무엇이 일어나는지* 코드 위에 보인다. 4장과 7장의 일관된 호흡이다.

## 한 호흡으로 정리

지금까지 그린 그림을 머리에 박을 때다. 셋이 남아야 한다.

**첫째, FastAPI 보안의 기본 패턴은 *리소스 서버*다.** 토큰 발급은 한 라우트(`/auth/login`), 토큰 검증은 의존성 한 개(`Depends(get_current_user)`). 발급과 검증이 분리돼 있어 *인가 서버를 외부로 빼는 날*에 큰 수술이 없다.

**둘째, 인증과 인가는 *함수 시그니처에 박는다*.** `CurrentUserDep`로 인증, `Security(..., scopes=[...])`로 권한. Spring 어노테이션이 *함수 파라미터의 마커*로 바뀌었을 뿐, 6장의 트랜잭션 명시성과 *같은 호흡*이다. 자동에서 명시로의 전환이 — 6·7장의 통주저음이다.

**셋째, *Spring Security가 무료로 막아주던 항목*은 우리 손이 책임진다.** CSRF는 *토큰을 어디 저장하느냐*로 결정, 세션 고정은 *세션이 없는 모델*로 회피, HTTPS는 *인프라 책임*, 토큰 회전은 *짧은 만료 + 리프레시*. 그리고 모든 새 라우트마다 *네 가지 체크리스트 질문*을 — 손버릇으로.

그리고 한 가지 더 — *`pydantic-settings`가 시크릿의 표준 자리*다. JWT 비밀 키, DB 비밀번호, 외부 API 토큰. 모듈 레벨 변수 한 줄로 *애플리케이션 어디서나 일관된 설정*에 접근한다. 4장에서 깐 모듈 레벨 싱글톤 패턴과 같은 줄기. 11장 배포에서 *Kubernetes Secret으로의 흐름*과 한 번 더 만난다.

다음 8장은 비동기와 GIL이다. 4·5·6·7장에서 우리는 *sync 모드*로 책을 끌고 왔다. 이제 *왜·언제 async를 쓰는가*를 만질 차례다. "async라서 빠르다"가 아니라 "async를 잘 써야 빠르다"는 신호를 — 한 챕터 분량으로 풀어본다. WebFlux/Reactor 출신이라면 — `async/await`와 *닮음과 다름*을 짚게 된다. Kotlin 코루틴 출신이라면 — `suspend fun`과 *닮음과 다름*도 한 절로 마주친다. `BackgroundTasks` vs Celery vs ARQ 같은 *Spring `@Async`/`@Scheduled` 자리*에 무엇을 놓을지도 거기서 결정한다.

준비됐는가? 가자.


---

# 8장. 비동기와 GIL — WebFlux 사고를 코루틴으로

Spring WebFlux를 한 번이라도 진지하게 써본 손이라면 이런 장면이 익숙할 것이다. `Mono<User> user = userRepository.findById(id)`를 받아 `.flatMap`으로 묶고, `.subscribeOn(Schedulers.boundedElastic())`로 스레드 풀을 지정하고, 백프레셔가 어느 단계에서 깨졌는지 추적하느라 머리를 굴리던 그 시간. 반응형 사고가 손에 익기까지 걸린 비용을 기억할 것이다.

FastAPI를 처음 마주하면 `async def` 한 줄이 너무 가벼워 보인다. WebFlux의 그 무게가 다 어디로 갔지? 한 줄로 `async def read_user(...)`라고 쓰고, 안에서 `await db.execute(...)`만 해주면 끝이라고? 정말로?

정답부터 적자면, *손 모양은 가벼워졌고 함정의 모양도 가벼워졌다*. 그러나 함정 자체는 여전히 있고, *어떤 함정은 WebFlux 때보다 더 조용히 다친다*. 가장 흔한 사고가 이렇다 — async로 짰는데 sync DB 클라이언트를 한 줄 섞었다. 라이브러리 임포트가 잘못된 게 아니다, 코드는 정상 돌아간다. 그런데 부하 측정해보면 *sync로 짠 같은 코드보다 느리다*. 한 사례 보고는 sync 600 req/s, async + sync DB 550 req/s를 적어 둔다. 비동기의 오버헤드만 있고 이점은 없다.

두 가지를 손에 익히고 가자. 첫째, *`async def`를 어디에 쓰고 어디에 쓰지 말지*의 판단 회로. 둘째, `@Async`·`@Scheduled`가 떠받쳐 주던 *비동기 보조 자리* — 백그라운드 작업, 스케줄러 — 에 무엇을 놓을지의 의사결정 트리. Kotlin 코루틴 출신 독자에겐 한 절을 더 박아둔다, `suspend fun`과 `async def`의 닮음·다름을. GIL과 free-threaded Python의 2026년 현재 상태도 한 번 짚는다 — 한국 시장에 흘러다니는 "Python은 GIL 때문에 안 된다"는 단정을 정확한 자리에 놓아두는 게 본인 판단에 좋다.

> **이 장을 읽기 전 알아둘 것**
> - 5장의 SQLAlchemy 동기 모드와 `get_db` `yield` 의존성, 그리고 6장의 명시적 트랜잭션 경계는 본 장이 *async로 다시 쓰는 같은 그림*의 출발점이다.
> - 4장의 `Depends()` 그래프와 `Annotated[..., Depends(...)]` 타입 별칭 패턴이 본 장의 모든 라우트에 그대로 들어간다.

## §8.1 모델 비교 — WSGI vs ASGI, MVC vs WebFlux

Java 진영에 두 패러다임이 있다. *Spring MVC*는 서블릿 위의 동기·블로킹 모델이다. 한 요청에 한 스레드가 잡혀, DB·외부 API가 응답할 때까지 그 스레드가 점유된다. Tomcat 같은 컨테이너가 *스레드 풀*에 수십~수백 개를 미리 띄워두고 들어오는 요청에 하나씩 배정한다. *Spring WebFlux*는 Project Reactor·Netty 위의 비동기·논블로킹 모델이다. 한 스레드가 여러 요청을 *짧게짧게* 갈아 끼우며 처리한다. I/O 대기는 콜백으로 풀고, 스레드는 다른 요청을 본다.

Python 진영의 평행 분리가 *WSGI*와 *ASGI*다. WSGI(Web Server Gateway Interface)는 동기 인터페이스다 — Django·Flask가 오래 살아온 자리. ASGI(Asynchronous Server Gateway Interface)는 비동기 인터페이스다. FastAPI는 처음부터 ASGI 위에 있다.

| Java 진영 | Python 진영 | 본질 |
|---|---|---|
| Spring MVC + Servlet + Tomcat | WSGI + Gunicorn + Django/Flask | 한 요청 = 한 스레드, 블로킹 I/O |
| Spring WebFlux + Reactor + Netty | ASGI + Uvicorn + FastAPI | 한 스레드 = 여러 요청, 논블로킹 I/O |

매핑이 거의 1:1이다. 그래서 *FastAPI는 WebFlux가 기본값인 Spring*이라고 비유하는 게 가장 빠른 손짐작이다. 다만 두 가지 결이 다르다.

첫째, FastAPI는 *`async def`와 `def`를 한 앱 안에 섞어 쓸 수 있다*. WebFlux로 가면 *전 흐름이 반응형*이 되어야 일관성이 산다. `Mono`/`Flux` 중간에 블로킹 호출 하나가 끼면 그 자리부터 풀이 깨진다. FastAPI는 좀 더 너그럽다 — `def`로 두면 자동으로 스레드 풀에서 돌려준다. 이게 좋은 안전망이자 동시에 함정이다(§8.4에서 본격적으로).

둘째, *동시성 모델*이 다르다. WebFlux의 한 스레드는 진짜 OS 스레드고, 풀에 여럿이 있다. Python의 한 이벤트 루프는 *단일 스레드 안의 코루틴 스케줄러*다. GIL 때문에 사실상 한 시점엔 한 코루틴만 진행한다(§8.5). 이게 어떤 워크로드엔 자산이고 어떤 워크로드엔 부담이다.

## §8.2 이벤트 루프 — Java 스레드풀과의 본질적 차이

WebFlux의 `boundedElastic` 풀을 떠올려 보자. 풀에 스레드가 N개 있고, 작업이 들어오면 비어 있는 스레드에 배정한다. 스레드 자체는 OS 차원의 단위라 컨텍스트 스위치 비용이 있다. WebFlux가 자랑하는 효율은 *I/O 대기 동안 스레드를 점유하지 않는다*는 한 줄에서 나온다.

Python의 `asyncio` 이벤트 루프는 결이 다르다. 스레드가 *하나*다. 그 스레드가 코루틴들의 *순서*를 관리한다. 한 코루틴이 `await some_io()`를 만나면, 그 자리에 *돌아올 표시*를 남기고 다른 코루틴으로 넘어간다. I/O가 끝나면 표시한 자리로 돌아와 이어 실행한다. 마치 한 주방장이 여러 냄비를 동시에 끓이는 그림이다 — 한 냄비가 끓는 동안 다음 냄비를 본다.

```python
# 이벤트 루프의 정신적 모양
import asyncio

async def task_a():
    print("A 시작")
    await asyncio.sleep(2)   # 여기서 제어권을 루프에 반납
    print("A 끝")

async def task_b():
    print("B 시작")
    await asyncio.sleep(1)
    print("B 끝")

async def main():
    await asyncio.gather(task_a(), task_b())

asyncio.run(main())
# 출력:
# A 시작
# B 시작
# (1초 후)
# B 끝
# (1초 후)
# A 끝
```

이 정신적 모양 한 줄이 본 장의 모든 함정을 푸는 열쇠다. **`await` 한 곳이 *제어권 반납 지점*이다**. `await`이 없는 코드는 *반납을 하지 않는다*. 그 동안 다른 코루틴이 진행될 수 없다 — 이벤트 루프가 점유된다.

다시 강조한다. WebFlux는 *스레드가 풀에 여러 개*라 한 스레드가 막혀도 다른 스레드가 진행한다. FastAPI의 async 라우트는 *한 이벤트 루프*가 모든 코루틴을 굴리는 모양이다. 한 코루틴이 막히면 *그 워커의 모든 요청이 동시에 멈춘다*. 이게 다음 절의 함정으로 직결된다.

## §8.3 함정 — "Async가 항상 빠르지 않다"

본 장의 핵심 함정이다. 정신적으로 깊게 박아두자.

흔한 시나리오를 그려보자. 신입이 도서 카탈로그 API를 짠다. 5장에서 짠 동기 SQLAlchemy 코드를 가지고 와서, 라우트만 `async def`로 갈아 끼우고, "이제 비동기야"라고 안심한다.

```python
# 함정 — async 라우트 + sync SQLAlchemy
@router.get("/books/{book_id}")
async def get_book(book_id: int, db: DbSession):
    book = db.get(Book, book_id)        # 동기 SQLAlchemy — 블로킹
    return BookRead.model_validate(book)
```

이 코드는 정상 돌아간다. 테스트도 통과한다. 그런데 부하가 들어오면 *동기 버전보다 더 느리다*. 한 사례 보고는 이렇게 적는다 — sync FastAPI + sync SQLAlchemy가 ~600 req/s, async FastAPI + sync SQLAlchemy가 ~550 req/s. 일관되게 *async 쪽이 더 느리다*.

왜 이런가? 본 장 §8.2의 한 줄로 풀린다. `db.get(Book, book_id)`는 sync 함수다. `await`이 없다. 이벤트 루프가 *제어권을 반납받지 못한다*. 그 동안 다른 요청은 그저 줄을 선다. 한 워커가 한 요청씩 처리하는 *동기처럼* 동작하는데, 비동기 오버헤드(이벤트 루프 디스패치, 코루틴 프레임 생성)는 그대로 든다. 결과는 *느려지기*다.

한 사례 보고가 같은 함정을 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *어떤 개발자가 async로 '최적화' 한 뒤 FastAPI 성능이 곤두박질친 이유를 일주일 디버깅했다. async 함수 안에서 무거운 데이터 변환을 돌렸고 그게 이벤트 루프를 막고 있었다.* — Medium: lessons learned debugging (reference §4.1).

이 한 사례 보고가 본 장의 모든 가르침을 한 줄로 요약한다. *async 안에 sync를 섞지 말자*. 섞어야 한다면 §8.4의 안전 패턴을 쓰자.

세 가지 함정 유형을 분리해 두자.

**유형 1 — sync DB 클라이언트.** 위 예제. 해결책: async DB 드라이버(`asyncpg`, `aiomysql`)와 `AsyncSession`으로 통일. 또는 라우트를 `def`로 두자(§8.4의 자동 스레드풀로 떨어진다).

**유형 2 — CPU 무거운 연산.** 이미지 리사이즈, JSON 수만 줄 파싱, 정규식 폭주. 이런 건 async로 둘러도 *이벤트 루프 점유*가 본질이다. 해결책: `asyncio.to_thread`로 다른 스레드에 떼어 보내거나, 무거우면 *프로세스 풀*(또는 별도 워커)로 빼자.

**유형 3 — 블로킹 라이브러리 호출.** `requests.get(...)`, `time.sleep(5)`, 동기 Redis 클라이언트. async 라우트에 한 줄만 있어도 그 시간 동안 이벤트 루프가 멈춘다. 해결책: async 대응 라이브러리(`httpx`의 `AsyncClient`, `aioredis`)로 교체.

원칙 한 줄: **`async def` 라우트면, 그 안의 모든 I/O가 `await` 가능해야 한다**. 안 그러면 안전망이 깨진다.

### 한 번 측정해보자 — ML 추론 프록시 예제

추상적으로 듣지 말고 본인 손으로 한 번 측정해보자. 외부 ML 모델 API를 프록시하는 라우트를 셋으로 짜본다. 같은 일을 *동기로*, *async + sync 클라이언트로*, *async + async 클라이언트로*. 같은 부하를 흘려서 처리량을 비교한다.

```python
# app/ml/router.py — 세 가지 버전
import time
import requests
import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/ml")


# (a) 동기 def 라우트
@router.get("/sync")
def predict_sync(prompt: str):
    response = requests.post("http://ml-backend/infer", json={"prompt": prompt}, timeout=5)
    return response.json()


# (b) async 라우트 + 동기 클라이언트 (함정)
@router.get("/async-blocking")
async def predict_async_blocking(prompt: str):
    response = requests.post("http://ml-backend/infer", json={"prompt": prompt}, timeout=5)
    return response.json()


# (c) async 라우트 + async 클라이언트 (정석)
@router.get("/async-proper")
async def predict_async_proper(prompt: str, http_client: HttpClientDep):
    response = await http_client.post("http://ml-backend/infer", json={"prompt": prompt})
    return response.json()
```

`hey`나 `wrk` 같은 부하 도구로 동시 50 연결, 1만 요청을 흘려 보자.

```bash
$ hey -n 10000 -c 50 http://localhost:8000/ml/sync
$ hey -n 10000 -c 50 http://localhost:8000/ml/async-blocking
$ hey -n 10000 -c 50 http://localhost:8000/ml/async-proper
```

한 사례 보고를 기준으로 대략적인 결과 모양을 적어두자(환경에 따라 절댓값은 다르지만 *순서*는 일관된다).

| 버전 | 처리량 | P95 지연 | 비고 |
|---|---|---|---|
| (a) sync `def` | ~600 req/s | ~85ms | FastAPI 자동 스레드풀이 받침 |
| (b) async + 동기 클라이언트 | ~550 req/s | ~120ms | 이벤트 루프 점유로 *더 느림* |
| (c) async + async 클라이언트 | ~2,400 req/s | ~25ms | I/O 대기 동안 다른 요청 진행 |

(c)와 (a)의 차이가 약 *4배*다. 그게 async가 빛나는 자리다. 그러나 (b)는 *async를 흉내만 낸* 자리라 손해다 — 정확히 이 함정이 본 장이 가장 자주 지목하는 곳이다.

손에 익혀두자. **부하 측정 없이 async를 끼지 말자.** 측정해보고 (c)에 도달했을 때만 async의 이점이 손에 잡힌다. 그 전까지는 (a)가 안전하다.

## §8.4 안전 패턴 — sync를 async에 안전하게 묶기

원칙은 명료한데 현실은 그렇지 못하다. 우리가 쓰고 싶은 라이브러리 중에 async 버전이 없는 게 있다. 또는 *지금 코드를 다 갈아엎기 어려운* 상황이 있다. 이때 쓰는 안전망 두 개를 손에 익히자.

### `asyncio.to_thread` — 한 호출을 별도 스레드로

표준 라이브러리에 들어 있는 한 줄짜리 안전망이다. 동기 함수를 *별도 스레드에서 실행*하고, 그 결과를 `await` 가능한 코루틴으로 감싸 준다.

```python
import asyncio

@router.get("/books/{book_id}")
async def get_book(book_id: int, db: DbSession):
    # sync SQLAlchemy를 그대로 쓰되, 스레드로 떼어 보낸다
    book = await asyncio.to_thread(db.get, Book, book_id)
    return BookRead.model_validate(book)
```

`asyncio.to_thread(fn, *args)`는 내부적으로 *기본 스레드풀*에 작업을 던지고, 그 동안 이벤트 루프는 자유롭다. 다른 코루틴이 계속 진행한다. 결과가 준비되면 await이 풀리면서 이 코루틴이 이어진다.

비용을 한 번 짚어두자. 스레드를 빌리는 데 드는 *컨텍스트 스위치 비용*은 0이 아니다. 짧고 가벼운 작업엔 이게 오버헤드로 작용한다. 그래서 *원칙은 async 네이티브 라이브러리로 교체*가 맞고, *불가피한 경우의 임시 다리*가 `asyncio.to_thread`다. 영구 해결책으로 두면 안 된다.

FastAPI 진영엔 거의 같은 일을 하는 헬퍼가 또 있다.

```python
from fastapi.concurrency import run_in_threadpool

book = await run_in_threadpool(db.get, Book, book_id)
```

내부 구현은 거의 동등하다. 취향대로 골라 쓰자.

### sync def 라우트 — 자동 스레드풀의 안전망

여기 한 가지 더 손에 익혀두자. **FastAPI는 `def`로 선언한 라우트를 자동으로 스레드풀에서 실행한다.** 한 줄을 `async def`로 안 바꿔도, 이벤트 루프를 막지 않는다. *async 안전망*이 한 단계 더 있는 셈이다.

```python
# def 라우트 — FastAPI가 자동으로 threadpool에 던진다
@router.get("/books/{book_id}")
def get_book(book_id: int, db: DbSession):
    book = db.get(Book, book_id)
    return BookRead.model_validate(book)
```

이게 좋은 안전망이다. 5장에서 우리가 짠 sync 라우트들은 사실 이 안전망 위에서 정상 동작하고 있었다. *판단이 의심스러우면 `def`로 두는 게 낫다* — 이게 본 장이 줄 수 있는 가장 실용적인 한 줄이다.

그렇다면 언제 `async def`로 가는가? 답은 두 조건이 모두 맞을 때다.

1. 라우트 안의 모든 I/O가 *async 대응 라이브러리*로 구현돼 있다 (httpx AsyncClient, AsyncSession, aioredis 등).
2. 동시에 처리할 *I/O-bound 요청 수가 많다* — ML 모델 프록시, 외부 API 팬아웃, SSE/WebSocket 스트리밍처럼.

위 둘이 다 맞으면 async가 손에 잡히는 이득을 준다. 한쪽이라도 빠지면 sync `def`로 두고 자동 스레드풀에 맡기는 편이 낫다. *최적화는 측정 뒤에 한다*는 오래된 원칙이 본 장에서도 그대로다.

손에 익혀두자.

| 상황 | 권장 |
|---|---|
| 모든 I/O가 async | `async def` 라우트 |
| sync 라이브러리 1~2곳 | `async def` + `asyncio.to_thread`로 그 호출만 격리 |
| sync 라이브러리가 다수 | `def` 라우트 (자동 스레드풀) |
| CPU 무거운 작업 | `def` 라우트, 더 무거우면 별도 워커(§8.7) |
| 판단 애매 | `def` 라우트로 출발 — 안전망 위에서 출발 |

## §8.5 GIL — CPU-bound vs I/O-bound의 갈림과 PEP 703의 2026 현재

여기서 Java 출신이 가장 자주 갸우뚱하는 한 줄에 정확한 자리를 주자. *Python에는 GIL이 있어서 멀티스레드가 안 된다*는 단정이다. 반은 맞고 반은 틀린다.

GIL(Global Interpreter Lock)은 CPython 인터프리터에 박혀 있는 *전역 락*이다. 한 시점에 *Python 바이트코드를 실행하는 스레드는 하나*만 진행한다. 그래서 *순수 Python으로 CPU 무거운 일*을 멀티스레드로 돌려도 코어 하나만 쓴다. JVM의 정통 멀티스레드 효율을 기대하면 끔찍하다.

다만 한 줄을 더 보자. **I/O 대기 중에는 GIL이 풀린다.** 그래서 *I/O-bound* 워크로드(DB 쿼리, HTTP 호출, 파일 읽기)는 스레드를 늘려도 효과가 있다. asyncio가 단일 스레드에서 동작해도 *I/O 대기 중엔* 다른 코루틴이 진행할 수 있는 이유다. CPU가 진짜로 도는 시간은 *짧다*는 가정이 깔린 모델이다.

Spring 출신이 손에 익은 매핑으로 정리하자.

| 워크로드 | Java/Spring | Python/FastAPI |
|---|---|---|
| I/O-bound (대다수 API) | 멀티스레드 OK | asyncio 또는 멀티스레드 — 둘 다 효과 있음 |
| CPU-bound (이미지, 인코딩, ML 추론) | 멀티스레드/멀티프로세스 둘 다 | **멀티프로세스 권장.** asyncio·스레드는 효과 약함 |
| 혼합 | 한 스레드 풀로 | I/O는 async, CPU는 별도 워커로 분리 |

본 책의 1~7장이 다 *I/O-bound* 영역이다. 그래서 우리는 한 번도 GIL이 발목을 잡은 적이 없다. ML 모델 서빙처럼 CPU가 진짜로 도는 영역에 들어가면 그때 *별도 워커 또는 멀티프로세스*가 답이 된다. 11장이 그 자리를 본격적으로 다룬다.

### PEP 703과 free-threaded Python — 2026 현재

2023년 10월에 PEP 703이 받아들여졌다. 한 줄로 요약하면 *GIL을 제거한 빌드를 옵션으로 제공*한다. Python 3.13(2024년 10월)부터 *experimental* free-threaded 빌드(`python3.13t`)가 함께 배포된다. 2026년 현재, free-threaded 빌드는 *베타*에 가까운 단계다 — 표준 라이브러리는 거의 호환되지만, *C 확장 모듈*(NumPy, Pillow, psycopg, lxml 등)은 호환이 진행 중이다. 프로덕션 권장은 아직 아니다.

그러면 *언제 우리가 신경 쓰게 될까?* 한 시점이 있다. C 확장 호환이 70~80% 수준에 도달하고, 주요 ASGI 서버(uvicorn, hypercorn)가 free-threaded 모드를 검증할 때 — 빠르면 2027년, 보수적으론 2028년이다. 그때까지 *프로덕션 가이드는 여전히 프로세스 다중화*(uvicorn workers, k8s replicas)다.

손에 익혀두자. **2026년 현재 FastAPI 프로덕션 배포의 표준은 *프로세스 다중화*다.** GIL이 무서워서가 아니다. *프로세스 단위 격리*가 운영적으로 단단하기 때문이다(11장에서 본격).

### CPU-bound를 만났을 때 — 한 줄짜리 우회

CPU가 진짜로 도는 작업이 한두 군데 끼는 경우의 표준 손짐작 한 줄을 짚어두자. `concurrent.futures.ProcessPoolExecutor`를 통과시키는 패턴이다.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

# 앱 생명주기에 맞춰 한 번 만든다 (lifespan에서)
process_pool = ProcessPoolExecutor(max_workers=4)


def heavy_image_resize(image_bytes: bytes) -> bytes:
    # Pillow로 리사이즈하는 CPU 무거운 작업
    ...


@router.post("/thumbnails")
async def make_thumbnail(file: UploadFile):
    image_bytes = await file.read()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(process_pool, heavy_image_resize, image_bytes)
    return Response(result, media_type="image/jpeg")
```

`run_in_executor`에 `ProcessPoolExecutor`를 넘기면 GIL을 우회한 *진짜 멀티프로세스* 실행이 된다. 이벤트 루프는 자유롭게 다른 코루틴을 진행하고, 무거운 일은 *별도 프로세스가* 받는다. Spring에서 `@Async`로 ExecutorService에 던지는 모양과 정신적 짝이다.

다만 한 가지를 짚어두자 — *프로세스 간 인자·결과가 직렬화*된다(pickle). 큰 바이너리를 매번 복사하면 비용이 크다. 그래서 *진짜 무거운 CPU 작업*은 본격적으로 §8.7의 ARQ/Celery 워커로 빼는 편이 낫다. `ProcessPoolExecutor`는 *한두 군데 작은 우회용*이다.

### 한국 시장의 흔한 단정 — "Python은 GIL 때문에 안 된다"

한국 백엔드 커뮤니티에 흘러 다니는 단정 한 줄에 정확한 자리를 주자. *"Python은 GIL이 있어서 동시성이 안 된다"*는 말. 이게 정확한 자리는 *CPU-bound 워크로드*다. *I/O-bound* 영역에선 거의 모든 백엔드 워크로드가 그 안에 들어가고, asyncio가 풀어준다.

한국에서 FastAPI를 진지하게 쓰는 자리들이 어디인지 보면 답이 보인다 — *ML 서빙*, *내부 데이터 플랫폼 API*, *외부 API 통합*. 이들이 다 I/O-bound다. 그래서 GIL이 발목을 잡지 않는다. *Java처럼 코어 다 쓰는 멀티스레드*가 안 되는 건 맞지만, *코어 다 쓰려고 멀티스레드를 쓰지 않는다* — 멀티프로세스(uvicorn workers, k8s replicas)로 *프로세스 단위*로 다 쓴다. 결과적으로 코어가 놀지 않는다. 단정의 절반은 맞고 절반은 잘못된 비유다.

손에 익혀두자. **본인이 짜는 API가 I/O-bound라면 GIL 논쟁에 휘말리지 말자.** 측정해서 (c) 패턴(§8.3)으로 도달하면 그게 답이다.

## §8.6 Kotlin 코루틴 ↔ Python async — 닮음과 다름

Kotlin 백엔드 경력이 있는 독자에게는 한 절을 따로 박아둔다. `suspend fun`과 `async def`는 *같은 정신*에서 출발한 두 언어다 — 정지 가능한 함수를 통해 협력적 동시성을 구현한다는 점. 그러나 결이 다른 자리가 셋 있다.

먼저 가장 닮은 자리부터 보자.

```kotlin
// Kotlin
suspend fun getUser(id: Long): User {
    val user = userRepository.findById(id)  // suspend 함수 — 정지점
    return user
}
```

```python
# Python
async def get_user(id: int) -> User:
    user = await user_repository.find_by_id(id)   # await — 정지점
    return user
```

`suspend fun` ↔ `async def`, *호출 가능한 정지점*이 양쪽 다 있다. 호출자도 정지 함수 또는 async 컨텍스트여야 한다는 *전파 규칙*도 같다 — Kotlin은 `suspend`가 위로 전파되고, Python은 *함수가 async면 호출자도 async에서 await해야* 한다.

이제 다른 자리 셋이다.

**첫째, structured concurrency가 다르다.** Kotlin은 `coroutineScope { ... }` 또는 `supervisorScope { ... }`로 *부모-자식 코루틴의 생명주기*가 자동으로 묶인다. 부모 블록이 끝나면 자식도 다 끝나거나 취소된다. *코루틴이 새어나가지 않는다*. Python의 `asyncio`는 오래도록 이 자리가 약했다. 다행히 3.11부터 `asyncio.TaskGroup`이 들어와서 비슷한 그림이 가능해졌다.

```python
import asyncio

async def fetch_user_details(user_id: int):
    async with asyncio.TaskGroup() as tg:
        profile_task = tg.create_task(fetch_profile(user_id))
        orders_task = tg.create_task(fetch_orders(user_id))
        reviews_task = tg.create_task(fetch_reviews(user_id))
    # 블록을 빠져나오는 시점에 모든 자식 태스크가 완료. 하나라도 실패하면 형제 취소.
    return {
        "profile": profile_task.result(),
        "orders": orders_task.result(),
        "reviews": reviews_task.result(),
    }
```

Kotlin의 `coroutineScope` 정신을 *비슷한 손짐작*으로 받는 자리다. 다만 *3.11 이전 버전을 쓰는 코드*가 인터넷에 여전히 많고, `asyncio.gather`로 비슷한 일을 하지만 *실패 전파*가 미묘하게 다르다 — `TaskGroup` 쪽이 더 강하다.

**둘째, 디스패처 명시성이 다르다.** Kotlin에선 `withContext(Dispatchers.IO) { ... }`나 `withContext(Dispatchers.Default) { ... }`로 *어느 풀에서 돌릴지*를 코드에 박는다. Python에선 이게 묵시적이다. 같은 이벤트 루프에서 다 돌린다. *별도 스레드로 빼야 할 때*만 `asyncio.to_thread`나 `loop.run_in_executor`로 *명시적*으로 떼어 보낸다. 손짐작이 더 단조롭다 — 좋은 자리이자 동시에 *실수가 묻히기 쉬운* 자리.

**셋째, `runBlocking` ↔ `asyncio.run`.** Kotlin의 `runBlocking { ... }`은 *현재 스레드를 점유*해서 코루틴 결과를 받는다 — 메인 함수나 테스트에서 쓰는 다리다. Python의 `asyncio.run(main())`도 같은 자리다 — *이벤트 루프를 만들고, main 코루틴이 끝날 때까지 블로킹하고, 루프를 정리한다*. 한 가지 주의점이 있다 — `asyncio.run()`은 *프로세스 당 한 번*만 깔끔하게 동작한다. 라이브러리 안에서 함부로 호출하면 안 된다. 호출자에게 *이미 돌고 있는 루프가 있는지*를 위임하는 호흡이 안전하다.

손에 익혀두자. Kotlin의 명시적·구조적 동시성에 익숙한 손이라면, Python에선 *덜 명시적이지만 더 단조로운* 호흡을 만나게 된다. 좋은 점은 손이 가볍다는 것, 다친 자리는 *명시성이 없어서 누군가 sync 한 줄을 슬쩍 끼웠을 때 폭발의 원인이 모호하다는 것*. §8.4의 안전 패턴이 그 모호함을 다소 메운다.

## §8.7 백그라운드 작업 — `@Async`·`@Scheduled`의 대체

이 절이 본 장의 마지막 큰 자리다. Spring 진영에선 *짧고 가벼운* 백그라운드 작업은 `@Async`, *반복 스케줄*은 `@Scheduled(cron=...)`, *분산·신뢰성 있는 큐*는 RabbitMQ/Kafka + 별도 워커로 풀어왔다. 같은 그림을 FastAPI 진영에선 어떻게 받는가?

답은 *한 도구가 아니라 도구함*이다. 네 후보를 짚어두자.

| 용도 | Spring | FastAPI 진영 |
|---|---|---|
| 짧은 fire-and-forget | `@Async` | `BackgroundTasks` |
| 같은 프로세스 내 스케줄 | `@Scheduled(cron)` | APScheduler |
| asyncio 친화 분산 큐 | (Java 외부 큐) | ARQ |
| 성숙한 분산 큐 | Quartz/Spring Batch | Celery |

하나씩 본다.

### `BackgroundTasks` — fire-and-forget의 표준

FastAPI에 내장된 가장 가벼운 백그라운드 도구다. 라우트가 응답을 *먼저 보내고*, 그 뒤에 *같은 프로세스에서* 추가 작업을 실행한다.

```python
from fastapi import BackgroundTasks


@router.post("/users", status_code=201)
def create_user(
    payload: UserCreate,
    background: BackgroundTasks,
    service: UserServiceDep,
):
    user = service.create(payload)
    background.add_task(send_welcome_email, user.email)
    return UserRead.model_validate(user)


def send_welcome_email(email: str) -> None:
    # SMTP 호출 또는 외부 메일 API
    ...
```

응답이 클라이언트로 *먼저* 나가고, `send_welcome_email`이 그 뒤에 돈다. 사용자가 가입 폼에서 기다리는 시간이 짧아진다. Spring `@Async` 어노테이션의 *체감*과 거의 같다.

장점은 셋이다. 추가 인프라가 없다. 의존성이 가볍다. 학습 비용이 0에 가깝다.

단점도 셋이다. *같은 프로세스*에서 돈다 — 워커가 죽으면 작업이 사라진다. *재시도·결과 추적이 없다*. *워커의 메모리·CPU를 점유*해서 처리량을 깎는다.

FastAPI 공식 문서와 ARQ/Celery 비교 글이 한 줄로 정리한다 (저자의 영문 표현을 옮긴 한 줄) — *BackgroundTasks는 같은 이벤트 루프에서 응답이 흐른 뒤 실행된다. 짧고 작은 작업엔 효율적이지만 무거운 백그라운드 연산엔 Celery를 써야 한다.* — Background Tasks 공식 + Medium ARQ 비교 (reference §4.3).

판단 기준 한 줄: **작업이 짧고(<1초), 실패해도 큰 손실이 없고, 트래픽이 가볍다면 `BackgroundTasks`로 충분.** 어느 한 조건이 깨지면 다음 도구로 넘어가자.

### APScheduler — 같은 프로세스 내 스케줄

Spring `@Scheduled(cron="0 0 * * * *")`의 직접 대체다. *같은 FastAPI 프로세스* 안에서 cron 표현으로 작업을 반복 실행한다.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


async def cleanup_expired_sessions():
    # 만료된 세션 삭제 로직
    ...


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(cleanup_expired_sessions, "cron", hour=2)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
```

장점은 *외부 인프라 없이 cron이 돈다*는 것. 단점은 *프로세스가 여럿이면 작업이 중복 실행*된다는 것 — uvicorn 워커가 4개면 같은 작업이 4번 돈다. 이걸 막으려면 *분산 락*(Redis 기반)을 별도로 깔거나, 스케줄러를 *전용 워커 한 개*로 분리해야 한다. 운영 복잡도가 한 단계 올라간다.

판단 기준: **단일 프로세스 배포(또는 단일 leader 워커)에선 깔끔. K8s 다중 replica에선 별도 분리 권장.**

### ARQ — asyncio 친화 분산 큐

ARQ는 Redis 기반의 *asyncio 네이티브* 분산 큐다. FastAPI와 정신적 모양이 잘 맞는다 — 같은 async 호흡 위에서 워커가 동작한다.

```python
# tasks/worker.py
from arq.connections import RedisSettings
import httpx


async def send_slack_notification(ctx, channel: str, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://hooks.slack.com/services/...",
            json={"channel": channel, "text": text},
        )


class WorkerSettings:
    functions = [send_slack_notification]
    redis_settings = RedisSettings(host="redis", port=6379)
```

FastAPI 라우트에선 이렇게 큐에 푸시한다.

```python
# app/notifications/router.py
from typing import Annotated
from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from fastapi import Depends


async def get_arq_pool() -> ArqRedis:
    return await create_pool(RedisSettings(host="redis", port=6379))


# 4·5·6장 패턴대로 타입 별칭으로 묶어두자
ArqDep = Annotated[ArqRedis, Depends(get_arq_pool)]


@router.post("/notify")
async def notify(payload: NotifyRequest, arq: ArqDep):
    job = await arq.enqueue_job("send_slack_notification", payload.channel, payload.text)
    return {"job_id": job.job_id}
```

워커는 별도 프로세스로 띄운다.

```bash
$ uv run arq tasks.worker.WorkerSettings
```

장점은 셋이다. 워커 프로세스 분리로 *FastAPI 워커의 메모리·CPU 자유*. Redis로 *잡 영속화* — 워커가 죽어도 잡은 살아 있다. *재시도·결과·진행 상황 추적*이 내장.

단점은 둘. Redis 의존성이 추가된다. 라이브러리 성숙도가 Celery만큼은 아니다 — 큰 커뮤니티의 시간은 Celery가 더 길다.

### Celery — 성숙한 분산 큐

Python 진영의 *전통 강자*. RabbitMQ/Redis 위에서 동작하고, Spring + RabbitMQ 조합이 줄 만한 모든 기능 — 우선순위, 라우팅, 결과 백엔드, 분산 락, 비트(Celery beat로 cron) — 을 다 갖춘다.

```python
# tasks/celery_app.py
from celery import Celery

app = Celery("myapp", broker="redis://redis:6379/0")

@app.task
def send_welcome_email(email: str):
    ...
```

FastAPI 라우트에선:

```python
@router.post("/users")
def create_user(payload: UserCreate, service: UserServiceDep):
    user = service.create(payload)
    send_welcome_email.delay(user.email)   # 큐에 푸시
    return UserRead.model_validate(user)
```

장점: 가장 검증된 분산 큐. 운영 지식이 인터넷에 풍부. 큰 트래픽·복잡한 워크플로우에 강함.

단점: *asyncio와 결이 안 맞는다* — Celery 워커는 기본이 동기 코드 가정이다. FastAPI의 async 호흡과 코드 스타일이 갈린다. 학습 곡선이 가파르다 — broker/result backend/queue 설정이 만만치 않다.

### 어느 시점에 무엇으로 옮기나 — 단계적 마이그레이션

손에 익혀두자. 백그라운드 작업은 *처음부터 분산 큐를 짤 필요가 없다*. 시작은 가볍게, 부하가 늘면 단계적으로 옮긴다.

| 단계 | 도구 | 트래픽 가정 |
|---|---|---|
| 1 | `BackgroundTasks` | 분당 수~수십 건, 짧은 작업 |
| 2 | `BackgroundTasks` + APScheduler | + 정기 cron 작업 추가 |
| 3 | ARQ (또는 Celery) | 분당 수백 건 이상, 또는 작업이 무거워졌을 때 |
| 4 | ARQ + 전용 워커 노드 | 본격 분산, 여러 종류의 큐 |

예제 한 줄로 흐름을 박아두자. *이메일 발송*을 가벼운 단계 1로 시작해, 트래픽이 늘었을 때 단계 3으로 옮기는 그림이다.

```python
# 단계 1 — BackgroundTasks
@router.post("/users")
def create_user(payload, background: BackgroundTasks, ...):
    user = service.create(payload)
    background.add_task(send_welcome_email_sync, user.email)
    return ...


# 단계 3 — ARQ로 옮긴 뒤
@router.post("/users")
async def create_user(payload, arq: ArqDep, ...):
    user = await service.create(payload)
    await arq.enqueue_job("send_welcome_email", user.email)
    return ...
```

라우트 변경은 *한 줄*이다 — `background.add_task(...)` → `await arq.enqueue_job(...)`. 함수 본체는 거의 그대로 옮겨간다. *처음부터 ARQ로 짤 필요가 없는 이유*가 여기 있다 — 단계 옮김이 가볍다. 12장 통합 프로젝트의 Slack 알림이 *이걸 전제로* 가벼운 케이스를 다룬다.

판단 기준 한 줄을 박아두자. **트래픽·작업 크기·신뢰성 요구가 어느 한 축에서 어긋나면, 그때 다음 도구로 옮긴다.** 미리 가지 말자.

## 한 호흡으로 정리

8장에서 받아갈 것을 한 번에 묶어두자.

- **모델 비교:** WSGI/ASGI = Spring MVC/WebFlux. FastAPI는 *WebFlux가 기본값인 Spring*에 가깝다. 다만 `async def`/`def`를 섞어 쓸 수 있는 유연함이 더 있다.
- **이벤트 루프:** 한 스레드 안의 코루틴 스케줄러. `await` 한 곳이 *제어권 반납 지점*. `await`이 없으면 다른 코루틴이 진행하지 못한다.
- **함정:** *async 안에 sync를 섞으면 더 느리다*. 한 사례 보고는 sync 600 req/s vs async + sync DB 550 req/s를 적어 둔다. 세 가지 유형(sync DB, CPU 무거운 연산, 블로킹 라이브러리)을 분리해서 보자.
- **안전 패턴:** `asyncio.to_thread`/`run_in_threadpool`로 sync 호출을 격리하거나, *판단 의심스러우면 `def` 라우트로* 두자 — FastAPI가 자동으로 스레드풀에서 굴린다.
- **GIL과 PEP 703:** I/O-bound는 GIL이 잘 풀린다. CPU-bound는 별도 워커/멀티프로세스. PEP 703의 free-threaded Python은 2026년 현재 *experimental* — 프로덕션 표준은 여전히 *프로세스 다중화*다.
- **Kotlin 코루틴 비교:** `suspend fun` ↔ `async def`의 정신은 같다. 차이는 셋 — structured concurrency(`coroutineScope` ↔ `asyncio.TaskGroup`), 디스패처 명시성(Kotlin 명시, Python 묵시), 진입 다리(`runBlocking` ↔ `asyncio.run`).
- **백그라운드 작업:** `BackgroundTasks` → APScheduler → ARQ → Celery의 4단 계단. *미리 가지 말고 단계로 올라가자*. 라우트 한 줄 갈아 끼우는 비용으로 충분히 옮길 수 있다.

여기까지 오면 한 가지 감각이 든다. *async가 마법이 아니라, 도구함의 한 칸*이라는 감각이다. *언제 async를 쓰고 언제 sync로 두는지*가 본인 손에 잡힌다. WebFlux를 진지하게 써본 손이라면 이 감각은 그저 새로 쓰는 게 아니라 *옮겨 적는* 일이다.

다음 장은 *예외와 관측성*이다. `@ControllerAdvice`가 떠받쳐 주던 자리에 `@app.exception_handler`가 들어서고, Spring Boot Actuator가 한 줄로 깔아 주던 health/metrics/trace를 우리는 어떻게 손으로 조립하는지 보자. 본 장에서 만든 async 라우트들이 *관측성의 첫 시험대*다 — request_id가 코루틴을 넘나들 때 어떻게 따라다니는지가 9장의 한 자리다.


---


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


---

# 10장. 테스트 — MockMvc에서 TestClient + pytest로

Spring 진영에서 우리는 테스트에 *큰 자산*을 쌓아왔다. JUnit 5의 `@BeforeEach`, MockMvc의 `mockMvc.perform(get("/users/1"))`, `@MockBean`으로 빈 갈아끼우기, `@Transactional` 테스트의 자동 롤백, Testcontainers로 진짜 PostgreSQL 띄우기. 손에 익은 패턴이 한 트럭이다.

이걸 다 버리고 Python에서 처음부터 시작해야 하는가? 다행히 아니다. *대부분 그대로 옮겨진다.* JUnit 5의 자리에는 pytest가 들어오고, MockMvc 자리에는 TestClient가 들어오고, `@MockBean` 자리에는 4장에서 익힌 `app.dependency_overrides`가 들어온다. Testcontainers는 — 이름조차 같다. *Testcontainers Python*이 그대로 있다.

다만 *결정적으로 다른 자리*가 하나 있다. **`@Transactional` 테스트의 자동 롤백이 없다.** Spring에서 우리가 흔히 쓰던 패턴 — 메서드 위에 `@Transactional`을 붙이면 *테스트가 끝날 때 자동으로 롤백*되어 DB 상태가 깨끗하게 유지되던 — 그 마법이 없다. 6장에서 *트랜잭션 자동화의 빈자리*를 만졌듯이, 10장에서도 같은 *명시성*의 호흡을 한 번 더 만난다.

이 장에서 우리가 손에 익혀야 할 건 셋이다. *pytest로 테스트 짜는 손버릇*, *비동기 라우트를 테스트하는 패턴*, 그리고 *트랜잭션 롤백이 없는 세상에서 테스트 격리를 짜는 손길*이다. 차근차근 만져보자.

## pytest 기초 — JUnit 5와의 평행 비교

먼저 pytest 자체부터 손에 익히자. JUnit 5에 익숙하다면 — *놀랍도록 친숙*하다.

```java
// 자바 - JUnit 5
public class UserServiceTest {

    private UserService service;

    @BeforeEach
    void setUp() {
        service = new UserService(new InMemoryUserRepository());
    }

    @Test
    void shouldFindUser() {
        User user = service.find(42L);
        assertThat(user.getName()).isEqualTo("Alice");
    }

    @ParameterizedTest
    @ValueSource(strings = {"alice", "bob", "charlie"})
    void shouldAcceptValidUsernames(String name) {
        assertThat(service.isValidUsername(name)).isTrue();
    }
}
```

```python
# 파이썬 - pytest
import pytest

class TestUserService:
    @pytest.fixture
    def service(self):
        return UserService(InMemoryUserRepository())

    def test_find_user(self, service):
        user = service.find(42)
        assert user.name == "Alice"

    @pytest.mark.parametrize("name", ["alice", "bob", "charlie"])
    def test_accepts_valid_usernames(self, service, name):
        assert service.is_valid_username(name) is True
```

거의 1:1이다. 한 줄 한 줄 매핑해보자.

| Spring/JUnit 5 | pytest |
|---|---|
| `@Test` | `def test_*` 함수 이름 prefix |
| `@BeforeEach` | `@pytest.fixture` |
| `@AfterEach` | fixture 안의 `yield` 뒤 코드 |
| `@ParameterizedTest` + `@ValueSource` | `@pytest.mark.parametrize` |
| `assertThat(x).isEqualTo(y)` | `assert x == y` |
| Mockito `mock(Foo.class)` | `unittest.mock.Mock()` 또는 `pytest-mock` |
| `@DisplayName("사람이 읽는 이름")` | `def test_그_이름_그대로(...)`: 함수 이름이 곧 표시 이름 |

여기서 한 가지 짚고 가자. *fixture가 함수 파라미터다.* 클래스 멤버 변수가 아니다. JUnit 5처럼 `@BeforeEach`가 *암묵적으로* 멤버 변수를 채워주는 게 아니라 — pytest는 *명시적으로* fixture 함수가 *파라미터로 주입*된다. 어디서 본 모양 아닌가? 그렇다, 4장의 `Depends`다. *fixture 이름이 파라미터 이름과 같으면 자동으로 주입된다.* pytest와 FastAPI의 *의존성 주입 철학*이 *같은 줄기*다.

이게 좋은 이유 한 가지. *fixture가 무엇을 의존하는지가 시그니처에 보인다.* JUnit 5에서는 `@BeforeEach` 메서드가 어디서 호출되는지·무엇을 의존하는지 *암묵적*이었다. pytest는 — *코드 위에 평면적으로 펼쳐진다*. 4장의 *그래프가 코드 위에 보인다*는 표현이 — 테스트에서도 그대로 흐른다.

## `TestClient` — MockMvc의 자리

이제 *HTTP 레이어*다. Spring에서 우리는 MockMvc로 *컨트롤러를 띄우지 않고도* 요청을 검증해왔다.

```java
// 자바 - Spring MockMvc
@AutoConfigureMockMvc
@SpringBootTest
class UserControllerTest {

    @Autowired
    MockMvc mockMvc;

    @Test
    void shouldReturnUser() throws Exception {
        mockMvc.perform(get("/api/users/42"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.username").value("alice"));
    }
}
```

```python
# 파이썬 - FastAPI TestClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_returns_user():
    response = client.get("/api/users/42")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
```

`TestClient(app)`는 Starlette 기반이다. 내부적으로 `httpx`를 사용해서 *실제 HTTP를 타지 않고* 앱 객체를 직접 호출한다. MockMvc와 거의 같은 모델 — *서버를 띄우지 않고 ASGI 인터페이스로 직접 요청*.

Spring과 한 가지 다른 점. *컨테이너 재시작이 없다.* `@SpringBootTest`가 컨텍스트를 새로 띄우는 비용이 있던 자리가 — FastAPI에서는 *`TestClient(app)` 한 줄*이다. `app`은 그냥 모듈 레벨 객체다. 시작 비용이 거의 없다.

이게 무엇을 가져오는가? 테스트 실행이 *눈에 띄게 빠르다.* JUnit 5 + Spring Boot 통합 테스트의 *컨테이너 재시작 비용*과 비교하면, pytest + FastAPI는 *시작 비용이 거의 없는 구조*다. 큰 테스트 스위트에서 *분 단위와 초 단위의 차이*가 종종 보인다 — 절댓값은 환경에 따라 다르지만 *시작 비용의 차이*는 본질적이다. *짧은 피드백 루프*가 — 개발 속도에 직결되는 자산이다.

## 의존성 오버라이드 — `@MockBean`의 자리

여기서 4장에서 익힌 `app.dependency_overrides` 패턴이 — 테스트 영역에서 *진짜 가치*를 보인다. Spring 출신이 FastAPI를 보고 *가장 환호하는 자리* 중 하나다.

```java
// 자바 - Spring @MockBean
@SpringBootTest
class UserControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    UserService userService;        // 컨테이너에서 빈을 갈아끼움

    @Test
    void shouldReturnMockedUser() throws Exception {
        when(userService.find(42L)).thenReturn(new User(42L, "alice"));
        mockMvc.perform(get("/api/users/42"))
            .andExpect(jsonPath("$.username").value("alice"));
    }
}
```

```python
# 파이썬 - FastAPI app.dependency_overrides
from app.main import app
from app.users.deps import get_user_service

class FakeUserService:
    async def find(self, user_id: int):
        return UserRead(id=user_id, username="alice", email="alice@example.com")

@pytest.fixture
def client():
    app.dependency_overrides[get_user_service] = lambda: FakeUserService()
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_returns_mocked_user(client):
    response = client.get("/api/users/42")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
```

같은 일을 — *컨테이너 재시작 없이* — 한다. fixture 한 개에 모킹 로직이 담기고, `yield` 위쪽이 셋업, 아래쪽이 정리. 4장과 7장에서 한 번씩 만난 패턴이라 — *이미 손에 익어 있다*.

Spring의 `@MockBean`이 가진 *컨테이너 재구성 비용*이 — FastAPI에서는 *딕셔너리 한 항목 갈아끼우기*다. 그래프가 *함수 시그니처에 있어서* 그렇다. 컨테이너랄 게 없으니, 갈아끼울 컨테이너도 없다.

Mockito의 `when().thenReturn()` 패턴을 그대로 옮기고 싶다면 — `unittest.mock` 또는 `pytest-mock` 라이브러리가 있다. 다만 *Spring 출신의 손에 더 자연스러운* 패턴은 — 위처럼 *FakeXxx 클래스를 작성*하는 것이다. *명시적*이고, *코드 위에 무엇이 일어나는지 보인다*. 6·7장에서 익힌 *명시성 통주저음*과 같은 호흡이다.

## 비동기 테스트 — `pytest-asyncio` + `httpx.AsyncClient`

라우트가 `async def`로 짜여 있다면 — 테스트도 *그 모양*에 맞춰야 한다. `TestClient`는 *동기 클라이언트*다. 내부적으로 ASGI를 동기로 래핑해서 호출한다. 작은 테스트에는 충분하지만 — *진짜 비동기 동작*을 검증하고 싶거나 *동시 요청*을 시뮬레이션하고 싶다면 — `httpx.AsyncClient`가 필요하다.

```python
# 파이썬 - pytest-asyncio + httpx.AsyncClient
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_async_route():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/users/42")
    assert response.status_code == 200
```

```ini
# pyproject.toml (또는 pytest.ini)
[tool.pytest.ini_options]
asyncio_mode = "auto"      # @pytest.mark.asyncio 안 붙여도 자동 인식
```

한 줄 한 줄 짚어보자.

- **`@pytest.mark.asyncio`** — pytest가 *async 함수*를 어떻게 실행할지 알려주는 마커다. `asyncio_mode = "auto"`로 설정하면 모든 `async def test_*` 함수가 자동으로 인식된다.
- **`ASGITransport(app=app)`** — `httpx`에게 *HTTP가 아니라 ASGI 앱*을 직접 호출하라고 알려주는 전송 계층이다. 실제 네트워크가 일어나지 않는다.
- **`async with AsyncClient(...)`** — 클라이언트 자체도 *비동기 컨텍스트 매니저*다.

Spring WebFlux 출신이라면 — `WebTestClient`와 거의 같은 자리다. *비동기 핸들러를 비동기 모드로 호출*. 다른 점은 — Python 진영에서는 *동기 TestClient도 그대로 쓸 수 있다*는 점이다. WebFlux 진영의 *블로킹 호출은 별도 처리*가 필요했던 것과 달리, pytest는 *동기·비동기 테스트가 한 파일에 공존*할 수 있다.

여기서 한 가지 함정. **`AsyncClient`로 테스트할 때 `app.dependency_overrides`도 같은 방식으로 동작한다.** 패턴이 일관된다. 동기든 비동기든 — *의존성 갈아끼우기는 한 줄*이다. 4장에서 깐 패턴이 *어디서나* 같은 모양으로 흐른다.

## Testcontainers — 이름조차 같다

데이터베이스가 끼면 — *진짜 DB를 띄울 것인가, mock으로 갈 것인가*가 결정 갈래다. Spring 진영에서 우리는 *Testcontainers*를 자주 골랐다. *진짜 PostgreSQL을 Docker로 띄워서* 테스트한다. 마이그레이션·SQL 방언·인덱스·트랜잭션 같은 *진짜* 동작을 검증할 수 있다.

좋은 소식이 있다. **Testcontainers Python이 그대로 있다.**

```python
# 파이썬 - testcontainers-python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from app.db.models import Base

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres.get_connection_url()

@pytest.fixture(scope="session")
def engine(postgres_url):
    engine = create_engine(postgres_url, echo=False)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
```

이름조차 같다. Spring 진영의 `@Container PostgreSQLContainer` 패턴이 — *fixture 한 개*로 옮겨진 모양이다. 컨테이너의 라이프사이클이 `with` 블록에 묶이고, fixture의 `yield`가 *셋업과 정리*를 같이 표현한다.

`scope="session"`이 — 핵심 한 줄이다. *한 테스트 세션 전체에서 컨테이너를 한 번만 띄운다*는 신호다. 매 테스트마다 컨테이너를 띄우면 — *느리다*. 한 번 띄워두고 — *데이터를 매 테스트마다 격리하는 손길*을 따로 짠다. 그게 다음 절의 주제다.

비동기 SQLAlchemy를 쓴다면 — `asyncpg` URL로 바꾸고 `create_async_engine`을 쓰면 된다. 같은 패턴이다.

```python
# 파이썬 - 비동기 버전
from sqlalchemy.ext.asyncio import create_async_engine

@pytest.fixture(scope="session")
async def async_engine(postgres_url):
    async_url = postgres_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    engine = create_async_engine(async_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
```

여기까지가 *Spring과 같은 자리*다. 이제 *결정적으로 다른 자리*로 넘어가자.

## 트랜잭션 롤백이 없는 세상의 fixture 전략

Spring에서 우리가 *가장 사랑하던 패턴* 중 하나가 — `@Transactional` 테스트의 자동 롤백이었다.

```java
// 자바 - Spring @Transactional 테스트
@SpringBootTest
@Transactional       // 메서드가 끝나면 자동 롤백
class UserRepositoryTest {

    @Autowired
    UserRepository repository;

    @Test
    void shouldSaveUser() {
        User user = new User("alice");
        repository.save(user);
        // 테스트 끝나면 자동 롤백. DB 깨끗.
    }
}
```

*테스트마다 깨끗한 DB*. *공짜로*. 6장에서 `@Transactional`의 자동 롤백을 만졌듯이 — 이 자리에서도 *그 마법이 없다*.

FastAPI/SQLAlchemy에서는 — 어떻게 해야 깨끗한 DB로 매 테스트를 시작할 수 있을까? 세 갈래가 있다. 어느 걸 고를지는 *조직의 사정*에 달려 있다.

### 갈래 1 — SAVEPOINT + 명시적 롤백

가장 *Spring의 자동 롤백에 가까운 모양*이다. 각 테스트를 SAVEPOINT 안에서 실행하고, 끝나면 그 SAVEPOINT까지 롤백한다.

```python
# 파이썬 - SAVEPOINT 기반 격리
@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()      # 외부 트랜잭션 통째로 롤백
    connection.close()
```

좋은 점은 — *진짜 빠르다*. 매 테스트마다 데이터가 *DB에 commit 되지 않고* 메모리에 머문다. 무거운 점은 — *복잡하다*. 트랜잭션 격리, 중첩 SAVEPOINT, async 환경의 미묘한 차이 등 — *손에 익기까지 시간이 든다*. SQLAlchemy 공식 문서에 [이 패턴이 길게 설명돼 있다](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites) — 같은 문서를 한 번 읽어두면 마음이 편하다.

### 갈래 2 — 매 테스트마다 truncate

*가장 단순한 모양*이다. 매 테스트가 끝날 때 — 모든 테이블을 비운다.

```python
# 파이썬 - truncate 기반 격리
@pytest.fixture(autouse=True)
def clean_tables(engine):
    yield
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
```

`autouse=True`가 — *모든 테스트에 자동 적용*된다는 신호다. 좋은 점은 — *이해하기 쉽다*. 무거운 점은 — *느리다*. 매 테스트마다 *진짜 DELETE*가 일어난다. 테이블이 많아지면 — 누적이 작지 않다.

### 갈래 3 — 테스트마다 새 스키마

*가장 격리가 강한 모양*이다. 각 테스트가 *자기 스키마*를 새로 만들고, 끝나면 통째로 drop 한다.

```python
# 파이썬 - schema-per-test
@pytest.fixture
def isolated_db(engine):
    schema = f"test_{uuid4().hex[:8]}"
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA {schema}"))
        conn.commit()
    # 새 스키마를 search_path에 박은 engine을 만들어 yield
    ...
```

좋은 점은 — *완벽한 격리*. 병렬 테스트가 *서로 안 부딪힌다*. 무거운 점은 — *느리고 복잡하다*. 마이그레이션을 매번 실행해야 한다.

### 셋 중 무엇을 고를 것인가

조직의 사정에 따라 다르다. 일반 권고는 — *SAVEPOINT 기반이 기본값, truncate는 시작용, schema-per-test는 병렬화가 필요할 때*다. 우리 책에서는 *SAVEPOINT 기반*을 표준으로 잡는다. 손에 익으면 *Spring의 자동 롤백과 거의 같은 감각*이다.

이 자리에서 한 번 더 짚고 가자. Spring의 자동 롤백은 — *프레임워크가 가려둔 마법*이었다. 우리가 코드를 짤 필요가 없었다. FastAPI/SQLAlchemy에서는 — *그 마법을 우리가 직접 짠다*. 한 번 짜두면 — 평생 쓴다. *자동에서 명시로의 전환*이라는 6·7장의 통주저음이 — 테스트에서도 같은 호흡으로 흐른다.

## 픽스처 스코프 — Spring `@DirtiesContext`의 자리

Spring에서 `@DirtiesContext`는 — *이 테스트가 컨텍스트를 더럽혔으니 다음 테스트 전에 다시 만들어라*는 신호였다. pytest의 fixture 스코프가 — 같은 자리에 들어온다.

```python
# 파이썬 - fixture 스코프
@pytest.fixture(scope="session")    # 한 세션에 한 번
def engine(): ...

@pytest.fixture(scope="module")     # 한 모듈에 한 번
def app_settings(): ...

@pytest.fixture(scope="function")   # 매 테스트마다 (기본값)
def db_session(): ...
```

| Spring | pytest |
|---|---|
| `@DirtiesContext(classMode = AFTER_CLASS)` | `scope="module"` |
| `@DirtiesContext(methodMode = AFTER_METHOD)` | `scope="function"` (기본값) |
| `@DirtiesContext(classMode = BEFORE_EACH_TEST_METHOD)` | `scope="function"` + `autouse=True` |

*무거운 자원은 세션 스코프로, 가벼운 데이터는 함수 스코프로.* 한 줄 원칙이다. PostgreSQL 컨테이너는 — *세션 스코프*. DB 세션·테스트 데이터는 — *함수 스코프*. 명백한 선택이다.

## 계약 테스트 — Spring Cloud Contract 출신을 위해

마지막으로 *계약 테스트*를 한 절 짚고 가자. Spring 진영에서 `Spring Cloud Contract`로 — *프로듀서·컨슈머 간의 API 계약*을 테스트해온 사람이 있을 거다. 그 자산을 FastAPI에서 잃지 않을 수 있는가?

Python 진영의 같은 자리에는 **Pact Python**이 있다. [pact-python](https://github.com/pact-foundation/pact-python) 또는 [pact-python-v3](https://github.com/pact-foundation/pact-python). *Pact 표준*이 Polyglot이라 — Spring Cloud Contract와 *같은 broker*에 contract를 올리고 받을 수 있다. *마이크로서비스 사이의 계약*은 양쪽이 같은 진영을 쓸 필요가 없다.

기본 흐름은 이렇다.

```python
# 파이썬 - pact-python (컨슈머 측 일부)
from pact import Consumer, Provider

pact = Consumer("UserService").has_pact_with(Provider("AuthService"))

(pact
    .given("user alice exists")
    .upon_receiving("a request for alice")
    .with_request("GET", "/users/alice")
    .will_respond_with(200, body={"username": "alice"}))

with pact:
    response = requests.get(f"{pact.uri}/users/alice")
    assert response.json()["username"] == "alice"
```

Spring Cloud Contract의 *Groovy DSL*이 — *Python 메서드 체인*으로 옮겨진 모양이다. 핵심 모델은 같다 — *컨슈머가 기대하는 응답을 contract로 박고, 프로듀서가 그 contract를 검증*. 마이그레이션 비용이 작다.

다만 *모든 사람이 계약 테스트를 짜는 건 아니다*. 모놀리스 안에서 잘 작동하는 시스템이라면 — 굳이 도입할 자리가 아닐 수 있다. *마이크로서비스 + 자율 배포가 굴러가는 조직*에서 진짜 가치가 나오는 패턴이다. 이 책에서는 *Spring Cloud Contract 출신 독자가 이 자리를 잃지 않는다*는 사실만 짚고 넘어가자. 깊이는 *공식 문서와 한 두 권의 패턴 책*에 맡긴다.

## 한 흐름으로 — 1~9장의 API를 한 테스트 스위트로

지금까지 본 도구들을 모아서 — *1~9장에서 짠 작은 API들*을 한 통합 테스트로 묶어보자.

```python
# 파이썬 - tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from app.main import app
from app.db.models import Base
from app.db.session import get_db

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2://", "postgresql+asyncpg://"
        )
        yield url

@pytest.fixture(scope="session")
async def async_engine(postgres_url):
    engine = create_async_engine(postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(async_engine):
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            session_factory = async_sessionmaker(
                bind=connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            )
            async with session_factory() as session:
                yield session
            await transaction.rollback()         # 외부 트랜잭션 통째 롤백

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

```python
# 파이썬 - tests/test_exchange.py (3장 환율 API)
async def test_convert_usd_to_krw(client):
    response = await client.get("/convert?from=USD&to=KRW&amount=100")
    assert response.status_code == 200
    body = response.json()
    assert body["from"] == "USD"
    assert body["to"] == "KRW"
    assert body["amount"] == 100
```

```python
# 파이썬 - tests/test_books.py (5장 도서 CRUD)
@pytest.fixture
async def alice_token(client):
    response = await client.post(
        "/auth/login",
        data={"username": "alice", "password": "secret"},
    )
    return response.json()["access_token"]

async def test_create_and_read_book(client, alice_token):
    headers = {"Authorization": f"Bearer {alice_token}"}
    payload = {"title": "토비의 FastAPI", "author": "이일민"}

    create_response = await client.post("/books", json=payload, headers=headers)
    assert create_response.status_code == 201
    book_id = create_response.json()["id"]

    read_response = await client.get(f"/books/{book_id}", headers=headers)
    assert read_response.status_code == 200
    assert read_response.json()["title"] == payload["title"]
```

```python
# 파이썬 - tests/test_transfer.py (6장 송금)
async def test_transfer_rolls_back_on_insufficient_balance(client, alice_token):
    headers = {"Authorization": f"Bearer {alice_token}"}
    payload = {"from_account": 1, "to_account": 2, "amount": 999_999_999}

    response = await client.post("/transfer", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "잔액이 부족합니다."

    # 두 계좌의 잔액이 변하지 않았는지 검증
    a = (await client.get("/accounts/1", headers=headers)).json()
    b = (await client.get("/accounts/2", headers=headers)).json()
    assert a["balance"] == 1000
    assert b["balance"] == 1000
```

```python
# 파이썬 - tests/test_ml_proxy.py (8장 비동기 ML 프록시)
async def test_ml_proxy_async(client):
    response = await client.post("/predict", json={"input": [1.0, 2.0, 3.0]})
    assert response.status_code == 200
    assert "prediction" in response.json()
```

(`pyproject.toml`에 `asyncio_mode = "auto"`가 설정돼 있으면 `@pytest.mark.asyncio` 데코레이터 없이도 `async def test_*`가 자동 인식된다. 통합 스위트에서는 *모든 테스트를 한 모양*으로 두는 게 호흡상 깔끔하다.)

다섯 개 도메인이 — *같은 fixture 스택* 위에서 일관되게 흐른다. 환율(3장)·인증(7장)·도서(5장)·송금(6장)·비동기 프록시(8장). 모든 테스트가 *진짜 PostgreSQL*에서 굴러간다. 모든 테스트가 *깨끗한 DB로 시작*한다. 모든 테스트가 *컨테이너 재시작 없이 한 번에* 굴러간다.

Spring 진영의 `@SpringBootTest` + `@AutoConfigureMockMvc` + `@MockBean` + `@Transactional` + `@Testcontainers` 조합을 — *한 conftest.py 파일에 평면적으로 펼친 모양*이다. *그래프가 코드 위에 보인다*는 4장의 약속이 — 테스트 영역까지 흐른다.

## 한 호흡으로 정리

지금까지 그린 그림을 머리에 박을 때다. 셋이 남아야 한다.

**첫째, *손에 익힌 Spring 테스트 자산이 대부분 옮겨진다*.** JUnit 5 → pytest, MockMvc → TestClient, `@MockBean` → `app.dependency_overrides`, Testcontainers → Testcontainers Python. 이름조차 같은 자리도 있다. *재학습 비용*이 작다.

**둘째, *비동기 라우트는 `pytest-asyncio` + `httpx.AsyncClient`*다.** 동기 TestClient도 그대로 쓸 수 있지만, *진짜 동시성*을 검증하려면 비동기 클라이언트로 간다. 같은 의존성 오버라이드 패턴이 — *동기·비동기에서 일관되게* 동작한다. 4장에서 깐 패턴이 *어디서나* 같은 모양이다.

**셋째, *트랜잭션 자동 롤백은 없다. 직접 짠다.*** SAVEPOINT 기반 fixture를 한 번 짜두면 — *Spring 자동 롤백과 거의 같은 감각*을 얻는다. 6·7장의 *명시성 통주저음*이 — 테스트에서도 같은 호흡이다. 자동에서 명시로의 전환은 *처음엔 무겁고, 익숙해지면 든든하다*. 1·4·7장에서 봤던 그 감각이 — 한 번 더 흐른다.

그리고 한 가지 더 — *fixture 스코프를 정확히 잡자*. 무거운 자원은 세션 스코프, 가벼운 데이터는 함수 스코프. 컨테이너는 한 번만, DB 세션은 매 테스트마다. 손에 익으면 — *테스트 속도와 격리가 동시에 살아난다*.

다음 11장은 배포·운영이다. 10장까지 우리는 *코드를 잘 짜는 손길*에 집중했다. 11장에서는 *그 코드를 띄우는 손길*을 만진다. Uvicorn 단독 vs Gunicorn + Uvicorn worker, 워커 수 공식, Dockerfile 패턴, 그레이스풀 셧다운, X-Forwarded-* 처리. 그리고 1장에서 예고했던 *180MB → 600MB 메모리 누수 사례*를 본문에서 다시 만난다. JVM의 힙덤프 자리에 — `tracemalloc`·`memray`·`py-spy`를 어떻게 배치하는지 손에 쥐어준다.

준비됐는가? 가자.


---


# 11장. 배포·운영 — Tomcat에서 Uvicorn + Gunicorn + 컨테이너로

`java -jar app.jar`. 이 한 줄로 Spring Boot 서비스가 띄워진다. 안에 Tomcat이 들어 있고, 스레드풀이 알아서 잡히고, 클래스패스도 jar 안에 다 들어 있다. CI에서 빌드한 jar 하나를 EC2든 K8s든 어디든 *던지면 그만*이다. 이 단순함이 Spring Boot가 한 시대를 가져간 진짜 이유 중 하나다.

이제 같은 일을 FastAPI로 한다고 해보자. 손에 잡히는 그림이 한 번에 안 떠오른다. ASGI 서버는 *Uvicorn*인데, 그게 단독으로 운영 환경에 충분한가? *Gunicorn*은 어디서 어떻게 끼우는가? Tomcat의 스레드풀과 가장 닮은 자리는 어디인가? 컨테이너로 묶을 때 워커 수는 몇 개로 잡는가? Docker 이미지 안에 `uv`는 들어가야 하나, 빠져야 하나? 질문이 줄줄이 늘어선다. 살짝 난감하다.

핵심 질문은 둘이다. **`java -jar` 한 줄의 단순함이 사라진 자리에 무엇을 놓는가?** 그리고 **워커 수, 메모리, 컨테이너 전략은 어떻게 잡는가?** 답을 한 줄에 미리 흘려두자면 — *컨테이너 한 개 = Uvicorn 한 프로세스*가 K8s 시대의 기본형이다. 그 위에 Dockerfile·시크릿·헬스·메모리 모니터링이 한 층씩 쌓인다. 9장에서 깔아둔 관측성·헬스 엔드포인트가 11장에서 *진짜 운영 도구*로 받아진다. 한 발 한 발 함께 가보자.

## Uvicorn 단독 vs Gunicorn + Uvicorn worker

먼저 Tomcat의 자리를 떠올려보자. 한 JVM 프로세스 안에 스레드풀이 있고, 요청이 들어오면 스레드 하나가 잡혀서 *블로킹 IO*를 처리한다. 스레드 수는 보통 200~400개, JVM 프로세스는 *하나*다. 한 프로세스 안에서 멀티스레드로 수평 확장이 일어난다.

Python은 그 그림이 *조금* 다르다. **GIL** 때문이다. 한 프로세스 안에서 *동시에 실행되는 Python 바이트코드는 한 개*다(8장에서 깐 약속). 스레드를 200개 띄워도 *동시 실행되는 Python 코드는 하나*뿐이다. 그래서 Python 진영의 수평 확장은 *프로세스 단위*다. 워커 *프로세스*를 여러 개 띄우고, OS가 그 프로세스들에 요청을 분산시킨다.

여기서 두 도구가 같이 등장한다. **Uvicorn**은 *ASGI 서버* — Tomcat의 자리에 가장 가깝다. uvloop과 httptools 위에서 *한 프로세스의 이벤트 루프*로 비동기 요청을 처리한다. **Gunicorn**은 *프로세스 매니저* — 여러 워커 프로세스를 띄우고 죽은 워커를 살리는 역할이다. Spring 진영에는 Gunicorn의 정확한 평행 자리가 없다(Tomcat 자체가 둘 다 한다). 그래서 둘을 합쳐 쓰는 패턴이 흔히 다음과 같이 등장한다.

```bash
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 4 \
  -b 0.0.0.0:8000
```

`-k uvicorn.workers.UvicornWorker`가 Gunicorn에게 *워커를 Uvicorn 방식으로 만들라*고 지시한다. `-w 4`가 워커 *수*다. Gunicorn이 4개의 Uvicorn 프로세스를 띄우고, 각 프로세스가 *자기 이벤트 루프*를 돌린다. 요청은 OS 소켓에 들어와 4개 워커 중 *준비된* 워커가 받는다(소위 *pre-fork 모델*).

Medium iklobato의 글이 두 도구의 자리를 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *Gunicorn이 프로세스 관리(병렬성)를, Uvicorn이 async 요청 처리(동시성)를 담당한다. `-k uvicorn.workers.UvicornWorker` 플래그로 Gunicorn(WSGI 서버)이 Uvicorn(ASGI) 워커를 관리한다.* — Medium, "Mastering Gunicorn and Uvicorn" (reference §4.5).

Tomcat 한 프로세스 안의 *스레드풀 200개*가, FastAPI에서는 *프로세스 4개 × 이벤트 루프*로 옮겨졌다. 표현이 다르지만 결국 같은 일이다 — *동시 요청을 흘려보낼 통로*를 늘리는 것. 다만 *통로의 단위*가 스레드에서 프로세스로 바뀌었다.

## 워커 수 공식 — 어디서부터 시작하고 어디서 멈출지

워커 수를 몇 개로 잡을지가 다음 질문이다. 인터넷에는 두 공식이 떠다닌다.

- **Sync 워커:** `(2 × CPU) + 1` — 전통적인 Gunicorn 공식. 워커가 *블로킹 IO*에 자주 묶이므로 CPU 수보다 약간 더 많이 띄운다.
- **Async Uvicorn 워커:** *CPU 수와 같게.* 단일 스레드에서 *동시 요청을 효율적으로 처리하므로* 컨텍스트 스위치를 최소화하기 위해 워커 수를 CPU 수와 같게 둔다 — Medium iklobato의 같은 글에서 짚은 워커 공식이다 (reference §4.5, *async uvicorn 워커: CPU 수와 같게*).

8장에서 익힌 호흡을 들고 와보자. 라우트가 *대부분 async + 비동기 IO*라면 두 번째 공식을 따른다. 라우트에 *sync def + 블로킹 호출*이 섞여 있다면 — FastAPI가 자동으로 스레드풀에서 실행하지만 — 첫 번째 공식이 안전하다. 모르겠으면 *CPU 수와 같게* 두고 부하 테스트로 조정하는 게 보통이다.

여기서 한 가지를 짚자. *공식이 절대값이 아니다.* 한 워커의 메모리가 *200MB*라면 8 워커는 *1.6GB*다. 컨테이너의 메모리 limit이 1GB라면 OOM-Killer가 워커를 *번갈아 죽이는 사이클*이 시작된다. 끔찍한 일이다. 워커 수는 *CPU만 보고* 정하면 안 된다 — *메모리 한도 / 워커당 메모리*도 함께 봐야 한다. 부하 테스트에서 워커 수를 1씩 줄여보며 안정점을 찾는 편이 낫다.

## Kubernetes에선 컨테이너당 단일 프로세스

여기까지 따라온 다음 한 가지 *전환점*이 등장한다. Gunicorn으로 한 컨테이너에 4 워커를 띄우는 패턴은 *VM 시대*의 호흡이다. K8s 시대로 오면 그림이 살짝 바뀐다.

FastAPI 공식 deployment 문서가 이 자리를 한 줄로 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *Kubernetes에서는 워커를 쓰지 말고 컨테이너당 단일 Uvicorn 프로세스를 권장한다*. 이유는 *K8s replica가 곧 워커 역할*이기 때문이다 (reference §4.5).

K8s의 Deployment는 *replicas 4*를 박으면 컨테이너 *4개*가 뜬다. 각 컨테이너 안에 Uvicorn *1개*. OS 소켓 분산 대신 *Kubernetes Service*가 들어와 부하 분산을 한다. 컨테이너가 죽으면 *kubelet이 살린다.* Gunicorn이 하던 일을 K8s가 *컨테이너 단위*로 다시 하는 셈이다.

이게 더 좋은가? 두 가지 이유로 그렇다. **첫째**, 한 워커가 메모리 누수로 부풀어 올라도 *그 컨테이너*만 OOM된다. 옆 워커들은 영향을 안 받는다. K8s가 알아서 죽이고 살린다. **둘째**, 메트릭이 *컨테이너 단위*로 깔끔하게 잡힌다. 한 컨테이너의 CPU·메모리·요청 수가 그대로 한 워커의 시그널이다. 디버깅이 한 단계 더 깨끗해진다.

VM이나 EC2에 직접 띄우는 환경이라면 Gunicorn + 4 워커. K8s라면 *Uvicorn 단독 + replicas로 수평 확장*. 두 패턴 모두 답이고, *환경이 무엇이냐*가 답을 정한다. 책에서는 K8s 패턴을 기본으로 가져간다 — 2026 현재 한국에서도 대부분의 새 프로젝트가 그쪽이다.

```dockerfile
# K8s 패턴: Uvicorn 단독, 워커 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

이 한 줄이 11장의 출발점이다. 그 위에 Dockerfile의 *몸통*을 쌓아 올린다.

## Dockerfile — multi-stage, `uv sync --frozen`, non-root

이제 Dockerfile을 짜보자. 2장에서 깔아둔 `uv`와 `pyproject.toml`을 그대로 활용한다. 가장 많이 쓰는 패턴은 *multi-stage 빌드*다 — 빌드 단계의 도구를 *실행 이미지에 안 가져가는* 방식이다.

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder

# uv를 빌드 단계에만 설치
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# 의존성 해상도와 설치를 lock 파일 기반으로
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 애플리케이션 소스 복사
COPY app/ ./app/
RUN uv sync --frozen --no-dev

# ============================================================
FROM python:3.13-slim AS runtime

RUN useradd -m -u 1000 -s /bin/bash appuser
WORKDIR /app

# 빌더에서 .venv만 가져옴
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/app /app/app
ENV PATH="/app/.venv/bin:${PATH}"

USER appuser
EXPOSE 8000

# 그레이스풀 셧다운을 위해 init을 PID 1로
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
```

조각조각 짚어보자.

**`--frozen`은 *lock 파일 그대로* 설치한다는 약속이다.** 빌드 시점에 `uv.lock`이 최신이 아니면 *실패한다*. Maven의 `--strict-locks`나 Gradle 잠금과 같은 자리다. *프로덕션 빌드에서 의존성이 조용히 바뀌는 사고*를 막는다. 2장에서 깐 `uv.lock`이 여기서 본 모습을 드러낸다.

**`--no-dev`로 dev 의존성은 들이지 않는다.** pytest·ruff·mypy는 컨테이너에 들어갈 이유가 없다. 이미지 크기와 공격 면을 함께 줄인다.

**`UV_COMPILE_BYTECODE=1`은 `.pyc` 파일을 미리 만들어둔다.** 컨테이너 콜드 스타트가 한 박자 빨라진다. K8s 환경에서 *처음 뜨는 Pod*에서 의미가 있다.

**Non-root 유저(`appuser`).** Spring Boot의 jar 한 줄 띄우기와 다르게, 컨테이너는 *기본이 root*다. 그대로 두면 *컨테이너 탈출 시* 호스트 root 권한이 새어 나간다. K8s `PodSecurityPolicy`/`PodSecurity` 표준이 *non-root를 요구한다*. 컨테이너에 사용자 한 명을 만들고 `USER`로 전환하는 두 줄이 그 표준을 채운다.

**`--proxy-headers --forwarded-allow-ips=*`.** 다음 절에서 자세히 본다.

## 그레이스풀 셧다운 — `lifespan` 컨텍스트와 signal

Spring Boot에는 `@PreDestroy` 어노테이션과 그레이스풀 셧다운 옵션이 박혀 있다. K8s가 Pod에 `SIGTERM`을 보내면 *진행 중인 요청을 마치고* 깔끔하게 종료된다. FastAPI에도 같은 자리가 있다 — `lifespan` 컨텍스트다.

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시: 자원 초기화
    await db_pool.connect()
    await redis_pool.connect()
    yield
    # 종료 시: 자원 정리
    await db_pool.close()
    await redis_pool.close()

app = FastAPI(lifespan=lifespan)
```

`yield` 위가 *시작*, 아래가 *종료*다. Spring의 `@PostConstruct`/`@PreDestroy` 한 쌍과 같은 자리지만 — *생성자/소멸자가 아니라 컨텍스트 매니저*로 표현된다. 6장의 트랜잭션 패턴과 같은 결이다 — *들여쓰기로 시작과 끝이 한눈에 보인다.*

K8s가 Pod를 죽일 때의 흐름을 따라가보자. 첫째, `SIGTERM`을 보낸다. 둘째, *terminationGracePeriodSeconds*(기본 30초) 동안 기다린다. 셋째, 그래도 살아 있으면 `SIGKILL`. Uvicorn은 `SIGTERM`을 받으면 *새 요청 받기를 멈추고, 진행 중 요청이 끝나기를 기다리고, lifespan의 종료 부분을 실행하고, 종료된다*. 정확히 우리가 원하는 그림이다.

여기서 한 가지 함정. 컨테이너 안에서 *PID 1 프로세스*에 신호 처리 이슈가 있다. Python 프로세스가 PID 1이면 일부 신호(`SIGINT` 등)가 *기본 핸들러로 무시*될 수 있다. 운영 환경에서는 `tini` 같은 *최소 init*를 PID 1으로 두는 게 안전하다.

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends tini && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
```

`tini`가 PID 1로 들어가 신호를 *uvicorn에 정확히 전달*한다. K8s 1.20+ 환경이라면 컨테이너의 `restartPolicy`와 `terminationGracePeriodSeconds`를 함께 봐두자. 한 번 머리에 새겨두는 게 좋다.

## 시크릿 관리 — K8s Secret을 BaseSettings로 받는 파이프라인

7장에서 `pydantic-settings`를 도입했다. JWT 비밀 키를 `.env` 또는 환경 변수에서 받아 `BaseSettings`로 검증하는 그 자리다. 11장에서는 그 입력이 *K8s Secret*에서 오는 운영 환경의 파이프라인만 다룬다.

```python
# app/core/settings.py (7장에서 이미 도입)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    jwt_secret: str
    db_url: str
    redis_url: str
    sentry_dsn: str | None = None

settings = Settings()
```

K8s에서 Secret을 만들고 컨테이너에 *환경 변수*로 주입한다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-api-secrets
type: Opaque
stringData:
  APP_JWT_SECRET: "real-secret-here"
  APP_DB_URL: "postgresql+asyncpg://user:pass@db:5432/orders"
  APP_REDIS_URL: "redis://redis:6379/0"
  APP_SENTRY_DSN: "https://abc@sentry.io/123"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-api
spec:
  replicas: 4
  template:
    spec:
      containers:
        - name: order-api
          image: registry.example.com/order-api:v1.2.3
          envFrom:
            - secretRef:
                name: order-api-secrets
          # ... 헬스 체크는 다음 절에서
```

`envFrom: secretRef`로 Secret의 모든 키가 *환경 변수로* 주입된다. 컨테이너 안의 `pydantic-settings`가 `APP_` prefix로 그 변수들을 *자동으로* 읽어 `Settings` 인스턴스로 검증한다. K8s Secret → 환경 변수 → BaseSettings 세 단계가 *깔끔한 파이프라인*으로 이어진다.

여기서 Spring 출신이 의식해야 할 한 가지. Spring의 `@Value("${...}")`는 *런타임 lookup*이라 키가 없거나 잘못된 타입이면 *부팅이 늦은 자리에서* 터진다. `pydantic-settings`는 *부팅 시 검증*이다. K8s Secret에서 한 키가 빠지거나 타입이 잘못되면 *Pod가 즉시 죽는다*. 처음에는 *이런 거 갑자기 죽나?* 싶지만 — 실은 *늦게 발견되는 것보다 빨리 발견되는 게 안전*하다. 6장 명시성 통주저음이 11장 시크릿에서도 같은 결로 흐른다.

## 메모리 누수 — 180MB가 600MB로 기어 올라가는 자리

11장의 가장 *어두운* 절을 짚자. 메모리 누수다. 1장의 약점 지도에서 예고한 자리다.

Medium "FastAPI vs Spring Boot: I tested both for 6 months in production"의 한 줄을 옮겨보자 (저자의 영문 표현을 옮긴 한 줄) — *한 회사 사례에서 FastAPI 서비스의 메모리가 180MB에서 시작해 며칠 사이 600MB까지 기어 올라갔다* (reference §3.2-2).

먼저 한 가지 못 박고 가자. 이건 *한 회사의 경험치*다. 모든 FastAPI 서비스가 메모리 누수에 시달린다는 일반화가 아니다. 하지만 *왜 그런 일이 일어나는가*는 일반적이다 — Python에는 JVM 같은 *성숙한 메모리 프로파일링 도구 체인*이 부족하다. JVM이라면 `jmap`·`jstat`·VisualVM·MAT가 즉시 손에 잡힌다. Python 진영에는 그 자리에 *작은 도구 세 개*가 있다. 각자 다른 자리에서 빛난다.

**`tracemalloc` — 표준 라이브러리로 시작하는 자리.**

```python
import tracemalloc

tracemalloc.start()
# ... 한참 운영 ...
snapshot1 = tracemalloc.take_snapshot()
# ... 더 운영 ...
snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, "lineno")
for stat in top_stats[:10]:
    print(stat)
```

표준 라이브러리에 들어 있어서 *추가 설치가 없다*. 두 스냅샷을 비교해 *어디서 메모리가 늘어났는지* 라인 단위로 본다. 처음 의심이 들 때 가볍게 켜보는 자리다. 단점은 *오버헤드*가 작지 않다는 것 — 운영 환경에서 *상시* 켜두기엔 부담스럽다.

**`memray` — Bloomberg가 만든 본격 프로파일러.**

```bash
uv run memray run -o output.bin -m uvicorn app.main:app
# 부하를 흘려넣은 뒤 종료
uv run memray flamegraph output.bin
```

flamegraph로 *메모리 할당의 호출 스택*을 그려준다. JVM의 MAT(Memory Analyzer Tool)와 가장 닮은 자리다. *어느 함수가 얼마나 할당했는지*가 한눈에 잡힌다. 단점은 *프로세스를 종료해야 리포트가 나온다*는 점이라 운영 컨테이너에 상시 켜두긴 어렵다. *로컬 재현*이나 *스테이징 환경*에서 빛난다.

**`py-spy` — 운영 환경의 살아 있는 프로세스를 들여다보는 자리.**

```bash
# 운영 컨테이너에 들어가서
py-spy dump --pid 1     # 스택 트레이스
py-spy top --pid 1      # top 같은 실시간 뷰
```

핵심은 *프로세스를 재시작하지 않고* 들여다본다는 것. JVM의 `jstack`과 같은 자리다. *지금 어느 함수에서 시간이 가고 있는지*가 실시간으로 보인다. CPU 누수에 더 강하고, 메모리 분석은 약하지만 — *진짜 이상한 일이 일어나는 컨테이너*에 들어가서 한 줄 찍을 때 가장 빛난다.

세 도구 모두 JVM의 *한 도구로 다 되는* 그림에 비해 작고 분산돼 있다. 찜찜한 자리다. 하지만 *세 도구의 자리를 각자 익혀두면* — `tracemalloc`으로 가벼운 의심, `memray`로 본격 분석, `py-spy`로 운영 환경 실시간 — 세 개를 합쳐 JVM 도구 체인의 *기능적 빈자리*를 메운다. 손이 한 번씩 더 가지만 손길이 곧 안전망이다.

권장하는 운영 패턴 한 가지. **컨테이너 메트릭의 `container_memory_working_set_bytes`를 Prometheus로 항상 보고** + **OOM kill 이벤트를 알람**으로 받자. 9장에서 깐 Prometheus 인프라가 *그대로* 메모리 모니터링에도 쓰인다. *부풀어 오르기 전*에 알람이 오면 `memray`나 `py-spy`를 들고 *천천히* 분석할 시간이 생긴다.

## `--proxy-headers` — 로드 밸런서 뒤의 진짜 IP

운영 환경에서는 Uvicorn 앞에 *로드 밸런서*가 거의 항상 있다. K8s Ingress, ALB, Nginx 같은 것들. 이 *프록시*가 사이에 끼면 — *클라이언트의 진짜 IP가 사라진다*. Uvicorn이 보는 IP는 *프록시의 IP*다. 로깅·rate limit·지오 IP 같은 자리에서 곤란해진다.

표준 해결책은 *프록시가 `X-Forwarded-For`·`X-Forwarded-Proto` 헤더에 진짜 정보를 박아 보내고*, *서버는 그 헤더를 읽어* 진짜 IP를 복원하는 거다. Uvicorn은 그 동작을 *명시적으로 켜야* 한다.

```bash
uvicorn app.main:app --proxy-headers --forwarded-allow-ips="*"
```

`--proxy-headers`가 헤더 *해석*을 켜고, `--forwarded-allow-ips`가 *어느 IP의 프록시를 신뢰할지*를 정한다. K8s 내부 클러스터처럼 *모든 트래픽이 신뢰된 프록시를 거친다*는 가정이라면 `*`로 충분하다. 외부에 노출된 환경이라면 *프록시의 정확한 IP 대역*을 박는 편이 낫다 — 안 그러면 *클라이언트가 직접 `X-Forwarded-For`를 위조*해 진짜 IP를 속일 수 있다. 보안 관점에서 끔찍한 일이다.

라우트 안에서는 평소처럼 `request.client.host`를 쓰면 *복원된 진짜 IP*가 잡힌다. Spring의 `request.getRemoteAddr()`이 `RemoteIpValve`로 자동 복원되던 자리와 같다. Uvicorn은 *그 valve를 명시적으로 켜는 두 옵션*으로 표현한다.

## 헬스 체크와 readiness probe — 9장 엔드포인트를 K8s manifest로 받음

9장에서 깐 `/healthz`와 `/readyz`가 이 자리에서 *진짜 운영 도구*로 받아진다. K8s Deployment manifest에 두 probe를 명시한다.

```yaml
spec:
  template:
    spec:
      containers:
        - name: order-api
          image: registry.example.com/order-api:v1.2.3
          envFrom:
            - secretRef:
                name: order-api-secrets
          ports:
            - containerPort: 8000
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 2
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
```

**`livenessProbe`는 `/healthz`** — 9장에서 *프로세스가 살아 있는가만* 보는 자리. 실패하면 K8s가 *컨테이너를 재시작*한다. DB 의존성을 *여기에 넣지 않는다*. 9장에서 강조한 함정이다 — DB가 잠시 끊겼는데 컨테이너가 재시작되면 *연쇄 재기동*이 시작된다.

**`readinessProbe`는 `/readyz`** — *지금 요청을 받을 준비가 됐는가*. 실패하면 K8s가 *서비스 라우팅에서 뺀다*. 컨테이너는 살아 있지만 요청이 안 들어온다. DB 핑·외부 의존성을 *여기서* 확인한다.

**`resources.requests/limits`.** Spring Boot의 JVM 힙 설정(`-Xmx`)과 비슷한 자리. requests는 *스케줄러가 보장하는 최소*고, limits는 *못 넘는 천장*이다. limits을 *워커당 메모리의 1.5~2배*로 잡는 게 보통이다 — 메모리 누수가 시작될 때 *알람이 울릴 여유*를 둔다. 그 여유 안에서 `py-spy`나 `memray`를 들고 분석한다.

여기까지 오면 Spring Boot의 `java -jar`가 한 줄로 하던 일이 *Dockerfile 30줄 + K8s manifest 40줄*로 풀려나왔다. 손이 더 많이 가지만 *어디가 어떻게 동작하는지*가 코드 위에 다 드러난다. 6장 명시성 통주저음이 11장 배포에서도 같은 결로 흐른다 — *자동의 자리에 명시가 들어선다.*

## CI/CD 스켈레톤 — GitHub Actions 한 자락

마지막으로 짧게 CI 파이프라인 한 자락. 2장의 lint·test·build 명령들을 GitHub Actions에 박는 자리다.

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv sync --frozen --all-extras
      - name: Lint
        run: |
          uv run ruff check .
          uv run ruff format --check .
      - name: Type check
        run: uv run mypy app
      - name: Test
        run: uv run pytest -v --cov=app --cov-report=xml

  build:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: registry.example.com/order-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

`uv sync --frozen`이 CI에서도 같은 결이다 — *lock 파일의 의존성 그대로*. `cache-from`/`cache-to`로 Docker 빌드 레이어 캐시를 GitHub Actions가 관리한다. 빌드 시간이 *재시도마다* 짧아진다. 사내 환경이라면 *컨테이너 이미지 스캐닝*과 *Helm 배포 스텝*을 더해야 하지만, 그 자리는 사내 사정마다 다르다. 이 책에서는 *공통의 뼈대*만 보여두고 사내 색깔은 운영팀과 함께 짠다.

## 한 호흡으로 정리

머리에 박혀야 할 건 셋이다.

**첫째, K8s 시대의 기본형은 *컨테이너 한 개 = Uvicorn 한 프로세스*다.** VM·EC2 시대에는 Gunicorn이 *4 워커*를 띄워 OS 분산을 받았다. K8s에서는 *replicas 4*가 그 자리를 가져간다. 컨테이너가 부풀거나 죽어도 *그 컨테이너만* 영향을 받고, 메트릭도 *컨테이너 단위*로 깔끔하게 잡힌다. 워커 수 공식은 *환경이 무엇이냐*가 답을 정한다. 모르겠으면 *CPU 수와 같게* 두고 부하 테스트로 조정하자.

**둘째, Dockerfile은 `uv sync --frozen` + multi-stage + non-root가 표준이다.** 2장에서 깐 `uv.lock`이 *프로덕션 빌드에서 의존성이 조용히 바뀌는 사고*를 막는다. multi-stage로 빌드 도구를 *실행 이미지에 안 가져가고*, non-root 유저로 *컨테이너 탈출 시 호스트 권한 노출*을 막는다. PID 1에는 `tini` — Python 프로세스의 신호 처리 이슈를 피하는 자리다. `lifespan` 컨텍스트가 Spring의 `@PostConstruct`/`@PreDestroy` 한 쌍을 *들여쓰기 한 블록*으로 표현한다.

**셋째, JVM 도구 체인의 빈자리는 *세 도구로 나눠* 메운다.** `tracemalloc`(표준 라이브러리, 가벼운 의심), `memray`(본격 분석, 스테이징), `py-spy`(운영 환경 실시간). 1장에서 예고한 *180MB → 600MB* 사례는 *한 회사의 경험치*다 — 일반화는 금물이지만, *Python 진영의 도구가 작게 분산돼 있다는 사실*은 짚어둘 만하다. Prometheus의 `container_memory_working_set_bytes`를 항상 보고 OOM kill 이벤트를 알람으로 받자 — 부풀어 오르기 전에 알람이 오면 *천천히* 분석할 시간이 생긴다. 9장의 `/healthz`·`/readyz` 분리는 K8s livenessProbe·readinessProbe로 *manifest에서* 받아진다 — 의존성 끊김에 *연쇄 재기동*하지 않도록 하는 안전망이다.

다음 장은 통합 프로젝트다. 1~11장에서 깐 모든 조각이 *사내 태스크 관리 API + Slack 알림 봇*이라는 한 도메인 안에서 *함께 동작*한다. 3장의 Pydantic 모델, 4장의 Depends + APIRouter, 5장의 SQLAlchemy 도메인 폴더, 6장의 트랜잭션, 7장의 JWT + scope, 8장의 BackgroundTasks·SSE, 9장의 도메인 예외·메트릭, 10장의 TestClient·Testcontainers, 그리고 11장의 Dockerfile·K8s manifest까지. 책을 덮을 때쯤 손에 *프로덕션급 FastAPI 템플릿 한 벌*이 잡힌다. 자동의 자리에 명시가 들어선 11권의 기둥이 12장에서 한 그림으로 모인다 — 손에 익은 회로를 들고 다음으로 가자.


---

# 12장. 통합 프로젝트 — 사내 태스크 관리 API + Slack 알림 봇

여기까지 한 호흡으로 따라왔으면, 지금까지 우리가 만진 조각들이 머릿속에 흩어져 있을 것이다. `Depends()`의 그래프, `with db.begin():`의 명시 트랜잭션, `Security(..., scopes=[...])`의 RBAC, `BackgroundTasks`의 가벼움, `pytest` + `TestClient`의 안전망, Docker · Uvicorn 워커. 한 조각씩은 손에 익혔다. 그러나 *한 프로덕션 서비스 안에서 이 조각들이 어떻게 공존하는지*는 아직 본 적이 없다.

이 장이 그 자리다. 책 한 권 분량을 *하나의 코드베이스*로 받아본다. 도메인은 *사내 태스크 관리 API + Slack 알림 봇*이다. Spring 출신에게 가장 친숙한 도메인이라(이슈 트래커·티켓 시스템) 비즈니스 로직을 새로 배울 부담이 0이다. 그 자리에 우리가 책에서 약속한 모든 패턴을 끌고 와 본다.

한 가지를 미리 적어두자. *이 장의 코드는 깃허브 리포 한 개의 분량*이다. 모든 줄을 본문에 적지 않는다. 핵심 구조와 *Spring 사고와 부딪히는 자리*만 본문에 박는다. 전체 코드는 책의 짝 리포로 둔다. 본문은 *결정과 호흡*을 가르치고, 리포는 *완전한 손짐작*을 보여주는 분업이다.

> **이 장을 읽기 전 알아둘 것**
> - 1~11장 모든 챕터를 *전제*한다. 발췌 독자는 4장(DI)·5장(SQLAlchemy)·6장(트랜잭션)·7장(인증)·8장(async/배경)·10장(테스트) 최소 다섯 절은 보고 오자.
> - 이 장은 *완성된 코드를 처음부터 짜는 흐름*이 아니라, *각 장의 약속이 한 서비스에 어떻게 모이는지*의 거시 그림이다. 디테일은 챕터 본문에 이미 있다.

## §12.1 요구사항을 한 페이지에 박자

본격 코드 전에 *무엇을 만드는지*를 한 페이지로 못박아 두자. 이게 Spring 진영에서도 똑같다 — Confluence 한 페이지에 박는 그 그림.

**핵심 도메인 네 개**
- `users` — 사용자 가입/로그인, 역할 (`member`, `admin`)
- `tasks` — 태스크 생성·상태 변경·검색. 상태는 `todo` → `in_progress` → `done`
- `comments` — 태스크 댓글
- `notifications` — Slack 알림 (댓글 작성, 태스크 상태 변경 등)

**기능 요구사항 (요약)**
- 회원: JWT 로그인, `/me` 조회
- 태스크: CRUD, 상태 전이, 담당자 변경, 카테고리 필터
- 댓글: 작성/조회/삭제 (작성자만 삭제)
- 알림: 댓글이 달리거나 태스크 상태가 바뀌면 Slack 채널로 webhook
- 실시간: 태스크 상태 변경 시 SSE로 푸시
- 관측성: 요청 ID 미들웨어, Prometheus 메트릭, `/healthz`/`/readyz`, 도메인 예외 처리
- 인가: `admin` 역할만 사용자 관리(`/admin/users/*`)

**비기능 요구사항**
- Docker로 배포. PostgreSQL + Redis + 앱 컨테이너. K8s manifest 예시 한 장.
- 통합 테스트로 모든 라우트 검증. Testcontainers로 실제 PostgreSQL 띄우기.
- CI/CD 파이프라인 스켈레톤(GitHub Actions): lint(ruff) → type-check(pyright) → test → build.

작은 종이 한 장에 담길 그림이다. 무리하지 말자 — Spring 출신이 *한 분기 안에 두 사람*이 짤 만한 분량이다. 우리는 이걸 책의 호흡으로 한 챕터 안에 그린다.

## §12.2 폴더 구조 — 5장의 약속을 그대로

5장에서 박아둔 *by-feature 폴더 구조*가 여기서 빛난다. 도메인이 넷이면 폴더도 넷이다.

```text
task-tracker/
├── pyproject.toml
├── uv.lock
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/ci.yml
├── src/
│   └── app/
│       ├── main.py                 # FastAPI 진입점, 라우터 등록, lifespan
│       ├── core/
│       │   ├── config.py           # pydantic-settings 기반 (7장)
│       │   ├── security.py         # JWT, 비밀번호 해싱 (7장)
│       │   └── logging.py          # structlog 설정 (9장)
│       ├── db/
│       │   ├── base.py             # DeclarativeBase
│       │   ├── session.py          # engine + SessionLocal
│       │   └── deps.py             # get_db
│       ├── observability/
│       │   ├── middleware.py       # 요청 ID, 메트릭 미들웨어 (9장)
│       │   └── metrics.py          # Prometheus 카운터
│       ├── users/
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── repository.py
│       │   ├── service.py
│       │   ├── router.py
│       │   ├── deps.py             # get_current_user, require_admin
│       │   └── exceptions.py
│       ├── tasks/
│       │   ├── models.py           # Task + TaskStatus enum
│       │   ├── schemas.py
│       │   ├── repository.py
│       │   ├── service.py          # 상태 전이 로직
│       │   ├── router.py
│       │   ├── deps.py
│       │   └── events.py           # 도메인 이벤트 정의
│       ├── comments/
│       │   └── (같은 구조)
│       └── notifications/
│           ├── slack.py            # Slack webhook 클라이언트
│           ├── service.py          # 알림 발송 인터페이스
│           ├── worker.py           # ARQ 워커 (선택)
│           └── deps.py
└── tests/
    ├── conftest.py                 # Testcontainers + 픽스처
    ├── users/
    ├── tasks/
    ├── comments/
    └── e2e/                        # 통합 시나리오
```

처음 보면 폴더가 많다는 인상이 들 것이다. 그러나 Spring 출신이라면 *`com.foo.{users,tasks,comments,notifications}.{controller,dto,domain,repository,service}` 구조*와 1:1로 매핑된다는 걸 본능적으로 느낄 것이다. 새 도메인을 추가하는 비용이 *한 폴더 복사 + 6개 파일 채우기*다. 손짐작이 익으면 이 모양 자체가 *제도가* 된다.

## §12.3 설정과 부팅 — `main.py`와 `lifespan`

엔트리 포인트부터 보자. 라우터 등록, 미들웨어 등록, `lifespan`으로 자원 생명주기 묶기, 예외 핸들러 등록 — 9장에서 익힌 흐름 그대로다.

```python
# src/app/main.py
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import configure_logging
from app.db.deps import get_db
from app.db.session import engine
from app.observability.middleware import RequestIdMiddleware, MetricsMiddleware
from app.observability.metrics import metrics_router
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
from app.comments.router import router as comments_router
from app.notifications.deps import build_arq_pool, close_arq_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    app.state.arq_pool = await build_arq_pool(settings.redis_url)
    yield
    await close_arq_pool(app.state.arq_pool)
    await engine.dispose()


app = FastAPI(
    title="Task Tracker API",
    version="1.0.0",
    lifespan=lifespan,
)

# 미들웨어 (외→내 순으로 등록 호출 시 안→밖 순으로 동작)
app.add_middleware(MetricsMiddleware)
app.add_middleware(RequestIdMiddleware)

# 라우터 등록
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(metrics_router)


# 9·11장의 약속대로 두 probe를 의도적으로 분리한다.
# /healthz — 프로세스가 살아 있는가만 본다 (liveness)
# /readyz  — 지금 요청을 받을 준비가 됐는가 (readiness, DB 의존)
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="db not ready")
    return {"status": "ready"}
```

Spring Boot의 `@SpringBootApplication`이 떠받쳐 주던 *컴포넌트 스캔·자동 설정*의 자리를 우리는 *임포트 + `include_router` 호출 한 줄씩*으로 받는다. 손이 더 가지만 *무엇이 등록되는지가 코드 표면에 다 올라온다*. 13장에서 다시 비교하지만, 이게 Spring과 FastAPI의 근본적 결 차이다 — *자동화* vs *명시성*.

`Settings` 클래스는 7장의 `pydantic-settings` 패턴을 그대로 쓴다.

```python
# src/app/core/config.py
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    database_url: str = Field(..., alias="APP_DATABASE_URL")
    redis_url: str = Field("redis://redis:6379/0", alias="APP_REDIS_URL")
    jwt_secret: str = Field(..., alias="APP_JWT_SECRET")
    jwt_algorithm: str = Field("HS256", alias="APP_JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(15, alias="APP_ACCESS_TOKEN_EXPIRE_MINUTES")
    slack_webhook_url: str | None = Field(None, alias="APP_SLACK_WEBHOOK_URL")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

11장의 약속처럼, K8s 환경에선 이 환경변수들이 *Secret/ConfigMap → 컨테이너 env → Settings*의 파이프라인으로 흐른다. 코드는 한 줄도 안 바꾸고 환경만 바뀐다.

## §12.4 도메인 모델 — Task와 상태 전이

`Task`가 본 프로젝트의 핵심 도메인이다. 5장의 `Mapped`/`mapped_column` 패턴 위에 상태 enum을 더 얹는다.

```python
# src/app/tasks/models.py
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO, index=True)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    assignee: Mapped["User"] = relationship(foreign_keys=[assignee_id], lazy="raise")
    created_by: Mapped["User"] = relationship(foreign_keys=[created_by_id], lazy="raise")
    comments: Mapped[list["Comment"]] = relationship(back_populates="task", lazy="raise")
```

한 가지 디테일을 짚어두자. `relationship(..., lazy="raise")`다. 5장에서 *DetachedInstanceError* 함정을 본 적이 있다. `lazy="raise"`는 *lazy load 자체를 막아*버린다 — 명시적 `selectinload`로 끌어오지 않은 관계 접근은 *런타임에 즉시 에러*를 던진다. 처음엔 과한가 싶지만, 한 번 부딪혀 보면 안다. 5장에서 가르친 *코드 표면에 비용을 올려둔다*는 명시성의 정수다.

### 상태 전이 — 도메인 메서드로 박는다

JPA 진영에선 `Task.transition_to(...)` 같은 도메인 메서드를 엔티티에 박는 게 익숙하다. SQLAlchemy도 똑같이 한다.

```python
# src/app/tasks/models.py (Task 클래스 안에 추가)
class InvalidTransition(Exception):
    def __init__(self, from_status: TaskStatus, to_status: TaskStatus):
        self.from_status = from_status
        self.to_status = to_status


VALID_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.TODO},
    TaskStatus.DONE: set(),   # 종료 상태
}


class Task(Base):
    # ... 위 정의

    def transition_to(self, new_status: TaskStatus) -> None:
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise InvalidTransition(self.status, new_status)
        self.status = new_status
```

엔티티가 자기 *상태 전이 규칙*을 안다. 서비스 레이어에서 이 메서드를 호출하면 *비즈니스 불변식*이 한 곳에 모인다. Spring DDD 진영에서 익숙한 그림이다.

## §12.5 트랜잭션과 도메인 이벤트 — 6장의 약속

먼저 한 가지를 못박아 두자. 5장에서 약속한 `expire_on_commit=False`가 본 프로젝트 `app/db/session.py`의 전제다. 그 위에서 *커밋 직후에도 객체 속성을 안전하게 읽을 수 있고*, 본 절의 권장 패턴이 그 보장 위에서 동작한다. 만약 기본값 `True`로 두면 `with` 블록 종료 직후 `task.id`/`from_status` 접근이 `DetachedInstanceError`로 폭발한다 — 책의 §12.12 함정 체크리스트 3번이 짚는 자리다.

태스크 상태가 *바뀌면* Slack 알림이 가야 한다. 그런데 *DB 커밋과 Slack 호출의 순서*는 어떻게 잡을까? 이게 6장이 던진 큰 질문이다.

**잘못된 패턴 1: 트랜잭션 안에서 Slack 호출**

```python
# 안티패턴 — 트랜잭션이 외부 API 응답까지 기다린다
def change_task_status(task_id: int, new_status: TaskStatus, db: Session, slack: SlackClient):
    with db.begin():
        task = db.get(Task, task_id)
        task.transition_to(new_status)
        slack.post(f"Task {task.id} → {new_status.value}")   # 트랜잭션 점유
```

Slack이 느리거나 죽으면 *트랜잭션이 그동안 잡혀 있다*. DB 락 시간이 길어지고, *DB가 throttle된다*. 또 — Slack 호출이 성공했는데 DB commit이 실패하면? 알림은 갔는데 상태는 그대로다. 데이터 불일치다. 끔찍한 일이다.

**잘못된 패턴 2: 트랜잭션 밖에서 BackgroundTasks**

```python
# 안티패턴 — DB 실패해도 알림은 나간다
def change_task_status(...):
    with db.begin():
        task.transition_to(new_status)
    background.add_task(slack.post, f"Task {task.id} → {new_status.value}")
```

이건 패턴 1의 데이터 불일치를 *반대로* 일으킨다 — DB는 정상인데 알림이 안 나가거나, 트랜잭션 롤백이 일어났는데도 알림이 나간다.

**권장 패턴: 도메인 이벤트 + 트랜잭션 후 발행**

해법은 도메인 이벤트를 *트랜잭션 안에서 수집*하고, *커밋 성공 후*에 *비동기 발행*하는 분리다. Spring 진영에선 `ApplicationEventPublisher` + `@TransactionalEventListener(phase = AFTER_COMMIT)` 패턴으로 같은 일을 한다.

```python
# src/app/tasks/events.py
from dataclasses import dataclass

from app.tasks.models import TaskStatus


@dataclass(frozen=True)
class TaskStatusChanged:
    task_id: int
    from_status: TaskStatus
    to_status: TaskStatus
    actor_id: int
```

```python
# src/app/tasks/service.py
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.tasks.events import TaskStatusChanged
from app.tasks.exceptions import TaskNotFound
from app.tasks.models import Task, TaskStatus
from app.tasks.repository import TaskRepository
from app.notifications.service import NotificationService


class TaskService:
    def __init__(self, db: Session, tasks: TaskRepository, notify: NotificationService):
        self.db = db
        self.tasks = tasks
        self.notify = notify

    def change_status(
        self,
        task_id: int,
        new_status: TaskStatus,
        actor_id: int,
        background: BackgroundTasks,
    ) -> Task:
        with self.db.begin():
            task = self.tasks.get(task_id)
            if task is None:
                raise TaskNotFound(task_id)
            from_status = task.status
            task.transition_to(new_status)

        # 커밋이 성공한 뒤 — BackgroundTasks로 비동기 알림
        event = TaskStatusChanged(
            task_id=task.id,
            from_status=from_status,
            to_status=new_status,
            actor_id=actor_id,
        )
        background.add_task(self.notify.task_status_changed, event)
        return task
```

여기 코드 구조의 핵심을 짚어두자. **`with self.db.begin():` 블록을 빠져나오는 시점이 *커밋 성공의 명시적 표지*다.** 그 뒤의 `background.add_task(...)`는 *커밋이 성공했을 때만 도달*한다. 트랜잭션 안에서 예외가 터지면 `with` 블록이 롤백을 일으키고, `background.add_task`는 호출되지 않는다. *데이터 일관성과 알림 일관성이 한 자리에서 보호*된다.

Spring `@TransactionalEventListener(phase = AFTER_COMMIT)`이 떠받쳐 주던 *커밋 후 발행* 보장이 FastAPI에선 *코드 구조로 명시*되는 자리다.

이 한 패턴이 본 프로젝트 *모든 도메인 이벤트의 표준*이다. 댓글 작성, 태스크 할당 변경, 사용자 가입 — 다 같은 모양이다. 한번 손에 익히면 *생각 없이 손이 간다*.

## §12.6 인증·인가 — 7장의 약속을 그대로

7장에서 짠 JWT 흐름이 본 프로젝트에서 *그대로* 동작한다. 핵심만 다시 보자.

```python
# src/app/users/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.deps import get_db
from app.users.models import User
from app.users.repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scopes={"member": "Read tasks and comments", "admin": "Manage users"},
)


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = int(payload["sub"])
        token_scopes = set(payload.get("scopes", []))
    except (JWTError, KeyError, ValueError):
        raise credentials_exc

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail=f"Missing scope: {scope}")

    user = UserRepository(db).get(user_id)
    if user is None:
        raise credentials_exc
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
RequireAdmin = Annotated[User, Security(get_current_user, scopes=["admin"])]
```

라우트에서는 한 줄로 끝난다.

```python
# src/app/tasks/router.py
from fastapi import APIRouter, BackgroundTasks

from app.users.deps import CurrentUser
from app.tasks.deps import TaskServiceDep
from app.tasks.schemas import TaskStatusChange, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.patch("/{task_id}/status", response_model=TaskRead)
def change_status(
    task_id: int,
    payload: TaskStatusChange,
    user: CurrentUser,
    service: TaskServiceDep,
    background: BackgroundTasks,
):
    task = service.change_status(task_id, payload.new_status, actor_id=user.id, background=background)
    return TaskRead.model_validate(task)


# 관리자 전용 라우트
from app.users.deps import RequireAdmin


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, _admin: RequireAdmin, service: TaskServiceDep):
    service.delete(task_id)
```

`CurrentUser`/`RequireAdmin` 두 타입 별칭이 *책 전체에서 가장 자주 쓰는 보안 표시*다. 라우트 시그니처를 보면 *누가 호출할 수 있는지가 한눈에* 보인다 — Spring의 `@PreAuthorize("hasRole('ADMIN')")`이 떠받쳐 주던 *선언적 보안*의 자리를 *함수 파라미터의 명시성*이 받는다. 7장의 정수 그대로다.

## §12.7 Slack 알림 — BackgroundTasks로 시작해서 ARQ로 옮길 시점

이게 본 프로젝트가 8장의 약속을 *실제로 시연*하는 자리다. *미리 가지 말고 단계로 올라가자*는 그 한 줄.

### 단계 1 — `BackgroundTasks` + httpx async

처음엔 `BackgroundTasks`로 충분하다. Slack webhook 한 번은 빠르면 100ms, 느려도 500ms 정도다. fire-and-forget으로 가볍게.

```python
# src/app/notifications/slack.py
import httpx
from app.core.config import settings


class SlackClient:
    def __init__(self, webhook_url: str | None):
        self.webhook_url = webhook_url

    async def post_message(self, channel: str, text: str) -> None:
        if not self.webhook_url:
            return   # 개발 환경에선 그냥 건너뛴다
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                self.webhook_url,
                json={"channel": channel, "text": text},
            )


def get_slack_client() -> SlackClient:
    return SlackClient(settings.slack_webhook_url)
```

```python
# src/app/notifications/service.py
from typing import Annotated
from fastapi import Depends

from app.notifications.slack import SlackClient, get_slack_client
from app.tasks.events import TaskStatusChanged


class NotificationService:
    def __init__(self, slack: SlackClient):
        self.slack = slack

    async def task_status_changed(self, event: TaskStatusChanged) -> None:
        text = f"Task #{event.task_id}: {event.from_status.value} → {event.to_status.value}"
        await self.slack.post_message(channel="#tasks", text=text)


def get_notification_service(
    slack: Annotated[SlackClient, Depends(get_slack_client)],
) -> NotificationService:
    return NotificationService(slack)


NotificationServiceDep = Annotated[NotificationService, Depends(get_notification_service)]
```

라우트는 §12.5에서 본 그대로다 — `background.add_task(self.notify.task_status_changed, event)` 한 줄.

### 단계 2 — 옮길 시점이 왔을 때

8장 §8.7에서 적었듯, 다음 조건 중 하나라도 발생하면 ARQ로 옮긴다.

1. 알림이 *길고 무거워졌다* (예: 첨부 이미지 생성, 여러 채널 동시 발송)
2. 트래픽이 분당 수백 건 이상으로 늘었다
3. 실패 시 *재시도*가 필요해졌다

옮기는 비용을 한 번 더 강조한다. **라우트 한 줄만 바뀐다.**

```python
# 단계 2 — ARQ로
# 이전: background.add_task(self.notify.task_status_changed, event)
# 이후: await arq.enqueue_job("task_status_changed", event_dict)
```

함수 본체는 *그대로 ARQ 워커 모듈에 옮겨가고*, 라우트에서는 *enqueue 한 줄로 바뀐다*. 손짐작이 *옮기기 가벼운 모양으로 미리 짜여 있던* 결과다. 그래서 8장이 *처음부터 ARQ로 짤 필요가 없다*고 권했던 것이다.

본 프로젝트는 *단계 1*에서 멈춘다 — 사내 도구의 트래픽이라면 그게 정확한 자리다. *옮길 준비*가 코드에 박혀 있다는 사실만 손에 두자.

## §12.8 SSE — 실시간 태스크 업데이트

태스크 상태가 바뀌면 *대시보드가 즉시* 보이게 하고 싶다. WebSocket을 동원할 만큼 양방향이 필요한 건 아니니, *SSE(Server-Sent Events)*가 적격이다. Spring WebFlux에서 SSE를 짜본 손이라면 정신적 모양이 거의 같다.

```python
# src/app/tasks/router.py (계속)
import asyncio
import json
from typing import AsyncIterator

from fastapi.responses import StreamingResponse


# 단순 예제 — 프로덕션은 Redis Pub/Sub 또는 ARQ 결과 채널 사용
event_queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=100)


async def task_event_stream(user: CurrentUser) -> AsyncIterator[str]:
    while True:
        event = await event_queue.get()
        # 사용자 권한에 맞춰 필터링 가능
        yield f"event: task_changed\ndata: {json.dumps(event)}\n\n"


@router.get("/stream")
async def stream_tasks(user: CurrentUser):
    return StreamingResponse(
        task_event_stream(user),
        media_type="text/event-stream",
    )
```

`asyncio.Queue`는 한 프로세스 안의 단순 큐다. *워커 여러 개*가 있는 프로덕션에선 Redis Pub/Sub로 갈아 끼워야 한다 — 그러나 코드 구조는 같다. 큐의 *소스*를 바꿀 뿐이다. SSE 자체의 라우트 모양은 *위 한 줄*로 끝난다. 그게 ASGI 위의 FastAPI다.

Spring WebFlux의 `Flux<ServerSentEvent<Task>>` 반환 패턴이 *반응형 컨테이너*에 의존하는 데 비해, FastAPI는 *비동기 제너레이터*에 의존한다. 정신적 모양은 같고, *손짐작이 더 단조롭다*.

## §12.9 통합 테스트 — Testcontainers + TestClient

10장의 약속이 여기서 빛난다. 모든 라우트를 *실제 PostgreSQL을 띄운 채* 검증한다.

```python
# tests/conftest.py
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.db.base import Base
from app.db.deps import get_db
from app.main import app


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    with PostgresContainer("postgres:16-alpine") as container:
        yield container


@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(engine) -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    def _override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
```

이 픽스처 한 묶음이 본 프로젝트의 *모든 테스트의 토대*다. 핵심 두 줄을 짚자.

**첫째, `db_session`이 *테스트마다 트랜잭션을 새로 만들고 끝에 롤백*한다.** Spring `@Transactional` 테스트의 자동 롤백을 *수제*로 구현한 자리다. 10장 §6에서 이미 본 패턴이다.

**둘째, `app.dependency_overrides[get_db]` 한 줄로 *프로덕션 의존성*을 *테스트 세션*으로 교체한다.** 4장 §테스트 오버라이드의 정수. Spring `@MockBean` 자리에 정확히 들어선다.

이제 시나리오 테스트가 깔끔하다.

```python
# tests/e2e/test_task_lifecycle.py
def test_task_status_transition_publishes_event(client, db_session, monkeypatch):
    sent_messages: list[str] = []

    # Slack 클라이언트 mock
    async def fake_post(self, channel: str, text: str) -> None:
        sent_messages.append(text)

    monkeypatch.setattr("app.notifications.slack.SlackClient.post_message", fake_post)

    # 1. 사용자 가입 + 로그인
    client.post("/users/register", json={"email": "tobi@example.com", "password": "pass1234"})
    token_resp = client.post(
        "/users/login",
        data={"username": "tobi@example.com", "password": "pass1234"},
    )
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. 태스크 생성
    create_resp = client.post(
        "/tasks",
        json={"title": "Write integration tests", "description": "..."},
        headers=headers,
    )
    task_id = create_resp.json()["id"]

    # 3. 상태 전이
    change_resp = client.patch(
        f"/tasks/{task_id}/status",
        json={"new_status": "in_progress"},
        headers=headers,
    )
    assert change_resp.status_code == 200
    assert change_resp.json()["status"] == "in_progress"

    # 4. Slack 알림 검증 — BackgroundTasks가 TestClient 컨텍스트에서 동기적으로 실행됨
    assert any("todo → in_progress" in m for m in sent_messages)
```

마지막 단계의 주석이 재미있다. **`TestClient` 컨텍스트에서 `BackgroundTasks`는 *동기적으로* 실행**된다. 그래서 `with TestClient(app) as client:` 블록이 끝나면 *백그라운드 작업이 다 끝난 상태*다. 테스트 코드가 *비동기 검증의 복잡함* 없이 *동기처럼* 작성된다 — 10장이 적어둔 *손에 익은 안전망*의 정수다.

## §12.10 배포 — Docker와 Kubernetes 한 페이지

11장의 약속을 한 페이지에 묶자. 멀티-스테이지 Dockerfile + docker-compose + K8s manifest 예시.

```dockerfile
# Dockerfile — 11장 패턴 그대로
FROM python:3.12-slim AS builder

# Astral 공식 uv 이미지에서 바이너리 복사 (별도 설치 불필요)
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev


FROM python:3.12-slim AS runtime

# tini로 PID 1 신호 처리 + 좀비 프로세스 회수
RUN apt-get update && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/
COPY alembic/ /app/alembic/
COPY alembic.ini /app/

ENV PATH="/app/.venv/bin:$PATH"
USER appuser

EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--"]
# K8s 환경 권장: 컨테이너당 단일 프로세스
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--proxy-headers", "--forwarded-allow-ips=*"]
```

`docker-compose.yml`로 로컬 개발 환경을 한 줄로 띄운다.

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: tasks
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  app:
    build: .
    environment:
      APP_DATABASE_URL: postgresql+psycopg://app:secret@db:5432/tasks
      APP_REDIS_URL: redis://redis:6379/0
      APP_JWT_SECRET: dev-secret-please-rotate
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
    command: >
      sh -c "alembic upgrade head &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

volumes:
  postgres_data:
```

`alembic upgrade head` 한 줄을 startup 스크립트에 박았다. Spring Boot의 *자동 Flyway 실행*에 가까운 자리다. 5장에서 *Alembic은 자동 시작이 없다*고 했던 그 단점을 *컨테이너 entrypoint*에서 한 줄로 메운다.

K8s manifest는 한 장만 적어두자.

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-tracker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: task-tracker
  template:
    metadata:
      labels:
        app: task-tracker
    spec:
      containers:
      - name: app
        image: task-tracker:1.0.0
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: task-tracker-secrets
        - configMapRef:
            name: task-tracker-config
        # 9·11장 약속대로 두 probe를 의도적으로 분리.
        # DB가 잠시 끊겼는데 컨테이너가 재시작되면 연쇄 재기동이 시작된다.
        readinessProbe:
          httpGet:
            path: /readyz       # DB 의존성 포함 — 준비 안 되면 트래픽 차단만
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthz      # 프로세스 살아 있는가만 — 재시작 트리거
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

11장의 약속대로 *컨테이너당 단일 프로세스*고, *replica가 곧 워커 역할*이다. 워커 수 공식을 K8s에선 적용하지 않는다.

GitHub Actions의 CI 파이프라인 한 장.

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pyright
      - run: uv run pytest -v
```

ruff → pyright → pytest 세 단계. 2장에서 박아둔 *정적 안전망 + 테스트*가 CI에서도 그대로 동작한다. *코드 표면에 다 올라온* 안전망이 한 번 더 *파이프라인 표면에도* 올라온다.

## §12.11 관측성 — 9장의 미들웨어 묶음

9장에서 짠 미들웨어들이 본 프로젝트에서도 그대로 동작한다. 핵심만 다시 보자.

```python
# src/app/observability/middleware.py
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.observability.metrics import REQUEST_COUNT, REQUEST_DURATION


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start

        endpoint = request.scope.get("route").path if request.scope.get("route") else request.url.path
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_DURATION.labels(method=request.method, endpoint=endpoint).observe(elapsed)
        return response
```

```python
# src/app/observability/metrics.py
from fastapi import APIRouter
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)


metrics_router = APIRouter()


@metrics_router.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

Spring Boot Actuator의 한 줄 자동화 자리에 *미들웨어 두 개 + 라우터 한 개 + Counter/Histogram 정의*가 들어선다. 손이 더 가지만 *무엇을 측정하는지 코드 표면에 다 보인다* — Grafana 대시보드 짤 때 *이 메트릭이 어떻게 만들어졌는지*가 코드 검색 한 번에 나온다. 운영 디버깅의 호흡이 가벼워진다.

## §12.12 Spring 출신이 빠지기 쉬운 함정 — 체크리스트

마지막으로 한 페이지를 *체크리스트*로 비워두자. 본 프로젝트를 짜면서 *Spring 사고로 인해 손이 잘못 가는 자리* 열 가지를 박아둔다. 코드 리뷰의 동료에게 *책 한 권 다시 펴라*고 하지 말고, 이 리스트 한 장을 띄워두면 된다.

1. **트랜잭션 안에서 외부 API 호출** — Slack/메일/외부 IDP 콜이 트랜잭션 안에 끼면 DB 락 시간이 폭발한다. 도메인 이벤트 + 커밋 후 발행으로 분리하자.
2. **`get_db`의 `finally`에서 commit** — 응답이 이미 나간 뒤다. 트랜잭션 경계는 라우트/서비스에서 명시.
3. **`expire_on_commit=True`로 두고 응답 직렬화** — commit 후 lazy load가 폭발해 `DetachedInstanceError`. `False`로 두자.
4. **`async def` 라우트 안에 `requests.get(...)` 한 줄** — 이벤트 루프가 멈춘다. `httpx.AsyncClient` 또는 `def` 라우트로.
5. **`@app.exception_handler`에 모든 예외를 한 곳에 박기** — 도메인 예외 계층 + 캐치올의 두 층으로 분리하자(9장).
6. **`BackgroundTasks`에 무거운 일** — 워커 메모리·CPU를 뺏긴다. 무거우면 ARQ로 옮길 시점.
7. **`lazy="select"` 기본값 그대로 두고 *-to-many 접근** — N+1. `selectinload` 또는 `lazy="raise"`로 *강제 사전 로드*.
8. **`@Autowired` 사고로 글로벌 싱글톤 가정** — FastAPI 기본 스코프는 *요청-스코프*다. 모듈 변수·`lifespan` 컨텍스트로 명시.
9. **`@PreAuthorize` 사고로 보호 라우트마다 직접 if/else** — `Security(get_current_user, scopes=[...])`가 OpenAPI까지 자동 반영.
10. **uvicorn 워커 수를 K8s에서 늘리기** — K8s replica가 곧 워커 역할. *컨테이너당 단일 프로세스*가 표준(11장).

이 열 가지가 본 프로젝트 코드 리뷰에서 *반복 지적되는* 자리들이다. 책 전체의 핵심 함정이 한 페이지에 모인 셈이다. 사무실 모니터 옆에 붙여두자.

## 한 호흡으로 정리

12장은 책 전체의 캡스톤이다. 우리가 받아간 것을 한 번에 묶어두자.

- **요구사항 한 페이지 → 폴더 구조 한 그림**: 도메인 4개(`users`/`tasks`/`comments`/`notifications`) × 6개 파일 패턴 = `app/{도메인}/{models, schemas, repository, service, router, deps}.py`. 5장의 약속 그대로.
- **`lifespan` 컨텍스트**: 자원 생명주기(엔진, ARQ 풀, 로깅)를 한 자리에 묶는다. 8장에서 익힌 `@asynccontextmanager` 패턴.
- **도메인 이벤트 + 커밋 후 발행**: 트랜잭션 안에서 이벤트 수집, `with db.begin():` 블록을 빠져나온 뒤 `BackgroundTasks.add_task`. Spring의 `@TransactionalEventListener(phase = AFTER_COMMIT)` 자리.
- **JWT + 스코프**: `CurrentUser`/`RequireAdmin` 두 타입 별칭이 *책 전체에서 가장 자주 펴볼 보안 표시*.
- **단계적 백그라운드**: `BackgroundTasks` → ARQ → Celery. *미리 가지 말자*. 옮길 때 *라우트 한 줄*만 바뀌도록 함수 본체를 *옮기기 가벼운 모양*으로.
- **SSE**: `StreamingResponse(generator, media_type="text/event-stream")` 한 줄. WebFlux의 `Flux<ServerSentEvent<T>>` 자리.
- **Testcontainers + dependency_overrides**: 진짜 PostgreSQL 띄우고 `get_db`만 교체. `@SpringBootTest` + `@MockBean` 자리에 정확히 들어선다.
- **Docker · K8s · CI**: 멀티-스테이지 Dockerfile + `alembic upgrade head` entrypoint + K8s replica + ruff/pyright/pytest CI. 11장 약속 그대로.
- **관측성 미들웨어 + probe 분리**: 요청 ID + Prometheus 메트릭 + `/healthz`(liveness)/`/readyz`(readiness)의 *연쇄 재기동 함정 회피*. Spring Boot Actuator 자리를 코드 표면으로 끌어올림.
- **함정 체크리스트 10개**: 모니터 옆에 붙여두자.

여기까지 오면 한 가지 감각이 든다. **FastAPI로 프로덕션 API를 *짤 수 있다*는 손 감각.** *Spring처럼 큰 프레임워크가 없는데도* 한 코드베이스 안에서 모든 조각이 일관되게 공존한다. *그 일관성을 떠받치는 것이 챕터 사이 약속들*이라는 사실도 손에 잡힌다 — 5장의 폴더, 6장의 트랜잭션 경계, 7장의 `Security`, 8장의 단계적 백그라운드, 9장의 미들웨어, 10장의 픽스처, 11장의 컨테이너. *각 장이 한 약속*이었던 셈이다.

다음 장이 책의 마지막이다. 본 프로젝트를 다 짠 우리는 이제 *반대 방향의 질문*을 받아야 한다 — *언제 FastAPI를 쓰지 말아야 하는가? 언제 Spring으로 돌아가야 하는가?* 본 책이 답해온 모든 자리에 대한 *정직한 한계*를 마지막으로 정리한다.


---

# 13장. 언제 Spring으로 돌아가야 하는가

여기까지 한 권의 호흡을 따라온 사람에게, 책의 마지막 자리에서 *되돌이 질문* 하나를 던져두고 싶다.

*나는 이제 FastAPI를 손에 익혔다. 그러면 Spring을 버려도 되는가?*

답은 — 아니다. 정직하게 말하면, *대부분의 한국 백엔드 개발자는 Spring을 버려선 안 된다.* 채용 시장이 그렇고, 한국 대기업의 사정이 그렇고, 우리가 손에 익힌 자산의 양이 그렇다.

그러면 이 책은 무엇이었나? *FastAPI라는 두 번째 도구를 손에 쥐는 길*이었다. *Spring을 대체하자는 책*이 아니라 *Spring 사고를 끌고 와서 FastAPI를 짓는 책*이었다. 마지막 장에서 우리는 이 약속을 한 번 더 정직하게 짚고 마무리한다.

이 장에서 우리가 만질 자리는 — *FastAPI가 빛나는 도메인과 다치는 도메인*, *한국 독자가 흔히 빠지는 인식 함정 네 가지*, *한국 채용·생태계의 진짜 풍경*, *SQLModel을 권할 것인가의 결정*, *책이 끝난 뒤 어디로 갈 것인가의 더 읽을거리*다. 어느 절을 읽다가 어디로 옮겨가도 좋다. 메타 챕터다.

## §13.1 FastAPI가 빛나는 도메인

먼저 *FastAPI가 가장 잘하는 자리*부터 정리하자. 이건 *책의 진영을 변호하는 자리*가 아니라 — *도구를 정확히 골라 쓰기 위한* 지도다.

**첫째, ML/AI 모델 서빙.** FastAPI의 *sweet spot* 중에서도 가장 명백한 자리다. PyTorch, HuggingFace Transformers, scikit-learn, ONNX 같은 라이브러리가 *Python 진영의 1급 시민*이다. 추론 API를 짤 때 — Spring에서 ML 모델을 부르려면 *gRPC 게이트웨이*나 *별도 Python 서비스*를 거쳐야 한다. FastAPI는 *그 게이트웨이가 필요 없다*. 모델을 `lifespan`에 한 번 로드하고, 추론 함수를 라우트에서 직접 호출한다. *왕복 한 번에 끝난다.*

**둘째, 데이터 플랫폼의 내부 API.** Pandas, NumPy, Polars 같은 데이터 처리 라이브러리가 *Python에서만 자연스럽다*. 데이터 파이프라인·ETL·내부 분석 API는 — Java/Spring에서 짤 수도 있지만, *코드 분량과 디버깅 비용*이 다르다. *데이터 진영이 Python으로 통일된 조직*이라면 FastAPI가 *마찰 없는 선택*이다.

**셋째, 빠른 MVP·실험 서비스.** 1장에서 짚었던 *초기 개발 3주 vs 5주*의 차이가 — 이 도메인에서 가장 크게 보인다. *3개월 안에 살아남을지 모르는 서비스*에 Spring Boot 풀스택을 띄우는 건 — 무거운 선택일 수 있다. 빠른 검증이 필요한 자리에서는 *띄울 수 있는 도구*가 곧 자산이다.

**넷째, 사내 어드민·툴링.** 트래픽이 작고, 도메인이 단순하고, *유지보수자가 데이터·ML 엔지니어인* 도구. *Spring의 진영 자체가 무겁다*. FastAPI 하나에 작은 React/Vue 한 페이지 붙이면 — *한 사람이 한 주에 끝낸다*.

다섯 번째 자리도 짚어두자 — **사이드카·웹훅 수신기 같은 가벼운 서비스.** Slack 봇, GitHub 웹훅 처리, 외부 API 통합 어댑터. *상태가 거의 없고 응답 시간이 중요하지 않은* 영역. *uvicorn 단일 프로세스*에 컨테이너 하나면 충분하다.

이 다섯 자리에서 — FastAPI는 *진짜 빛난다*. *Spring으로 같은 일을 할 수도 있지만, 이쪽이 더 가볍고 빠르고 자연스럽다*는 신호가 명백하다.

## §13.2 FastAPI가 다치는 도메인

반대로 — *FastAPI를 고르면 나중에 후회할 자리*도 있다. 1장의 *정직한 약점 지도*를 한 번 더 펼쳐서, *어디까지 가면 Spring으로 돌아가야 하는가*를 짚어보자.

**첫째, 복잡한 대규모 트랜잭션 시스템.** 6장에서 본 *명시적 트랜잭션 패턴*이 — *조직이 50명 넘는 백엔드 팀, 마이크로서비스 30개, Saga·이벤트 소싱·CQRS가 흐르는 복잡도*에서는 *손이 모자란다*. Spring `@Transactional` + Spring Cloud + Spring Data + Spring Batch의 *통합된 도구 체계*가 — *그 복잡도를 가려주는 자산*이다. FastAPI 진영의 같은 자리에는 — *조각으로 흩어진 라이브러리*가 있다. 직접 묶는 비용이 작지 않다.

한 한국 개발자의 velog 글이 이 자리를 정확히 짚는다 — "FastAPI는 빠른 개발과 간결한 구조가 강점이었지만, *복잡한 비즈니스 로직과 대규모 트래픽엔 Spring이 더 적합*." ([velog: FastAPI에서 Spring으로 마이그레이션하며 배운 점](https://velog.io/@thedev_junyoung/SpringFastAPIFastAPI%EC%97%90%EC%84%9C-Spring%EC%9C%BC%EB%A1%9C-%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98%ED%95%98%EB%A9%B0-%EB%B0%B0%EC%9A%B4-%EC%A0%90)) 일반화의 근거는 아니지만 *한 사례의 경험치*로는 충분한 신호다. *책의 약속을 정직하게 닫는 자리*이기도 하다.

**둘째, 대형 팀의 거대 모놀리스.** 백엔드 50명, 코드 50만 LOC, *5년 이상 유지되는* 시스템. Spring 진영의 *컨벤션·아키텍처 표준·정적 검사 도구·IDE 지원*이 — *큰 팀의 합을 맞추는 비용*을 낮춰준다. FastAPI는 *작은 팀에서 강력*하지만, *큰 팀에서는 자유도가 함정*이 된다. 한 velog 글의 톤이 그 함정을 짚는다 — "공식 가이드는 자세한데, *매뉴얼에 없는 예외 상황에서는 어떻게 해야 할 지 표준이 없다*. 그래서 코드가 지저분해진다." ([koeunyeon velog](https://velog.io/@koeunyeon/FastAPI-%EC%8D%A8-%EB%B3%B8-%ED%9B%84%EA%B8%B0))

**셋째, 엔터프라이즈 인테그레이션.** 메시징 큐(Kafka, RabbitMQ), 배치 처리(Spring Batch), 규제 시스템 통합(은행·결제·의료). 이 영역의 *Java/Spring 생태계*는 — *수십 년 검증된 라이브러리와 표준*이 쌓여 있다. Python 진영에도 대안은 있지만 *성숙도와 운영 노하우의 격차*가 정직하게 있다. 큰 금융·통신 회사가 *Spring으로 정착한 이유*가 여기에 있다.

이 세 자리에서는 — *FastAPI가 아예 못 한다*는 게 아니라, *Spring을 두고 굳이 FastAPI로 옮길 이유가 약하다*는 신호다. 결정은 — *조직의 사정과 시스템의 규모*가 한다.

## §13.3 한국 독자에게 보내는 인식 보정 — 네 가지 짚어두자

여기서 한 절은 *한국 독자에게만 의미 있는 자리*를 둔다. 한국 개발 커뮤니티에서 FastAPI를 두고 흔히 보이는 *인식의 함정 네 가지*를 정직하게 짚자.

### "FastAPI = Spring 대체"가 아니다 — 상보적이다

가장 흔한 함정이다. *FastAPI가 등장해서 이제 Spring은 끝났다*는 식의 인상. 사실이 아니다. 두 진영은 *서로 대체하지 않고 보완한다*. ML/데이터 API, 빠른 프로토타입, 사내 어드민에는 FastAPI. 복잡한 비즈니스 트랜잭션·대규모 도메인·엔터프라이즈 인테그레이션에는 Spring. *한 회사 안에서 둘 다 쓰는 게 정상*이다. 카카오·네이버·당근·우아한형제들 같은 조직에서도 — *메인 백엔드는 Spring/Kotlin, 보조·실험·ML 영역은 FastAPI*라는 분리가 흔하다.

이 책의 부제가 "Spring 사고로 FastAPI를 짓는 법"인 이유가 여기 있다. *옮긴다*가 아니라 *짓는다*. 8년 동안 쌓아온 사고는 *그대로 가져간다*. 그 위에 손에 잡히는 두 번째 도구를 *얹는다*.

### "타입 힌트가 있다고 Java처럼 안전하다"는 착각

3장에서 짚었지만 마지막 자리에서 한 번 더 박아두자. *Pydantic 모델 + mypy + IDE 타입 체크*가 — *Java의 컴파일 강제*와 같은 안전망인가? *아니다*. 한 학술 연구가 한 줄로 정리한 사실이 있다 — 약 15%의 결함은 mypy 같은 정적 타입 체커로 막을 수 있었다([Khan et al., 2021, TSE](https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf)). 뒤집어 말하면, *85%의 결함은 타입 힌트로 막을 수 없다*.

자바의 컴파일러가 잡아주던 것을 Python에서는 — *mypy/pyright + Pydantic 런타임 검증 + 테스트*의 세 겹을 *의식적으로 깔아야 한다*. 한 한국 개발자의 velog 글이 이걸 정확히 짚었다 — "스프링 부트의 파이썬 버전인가? 싶을 정도로 *타입 시스템 도입으로 빡빡한 기준이 생겼다*. 하지만 Spring과 달리 *극적으로 코드량이 줄어들지도 않는다*." ([koeunyeon velog](https://velog.io/@koeunyeon/FastAPI-%EC%8D%A8-%EB%B3%B8-%ED%9B%84%EA%B8%B0)) 정확한 관찰이다.

### "async라서 빠르다"가 아니라 "async를 잘 써야 빠르다"

8장에서 책 한 챕터를 통째로 들였던 신호다. *async def 라우트로 짰다고 자동으로 빠르지 않다*. 그 안에 *블로킹 호출 한 줄*이 끼면 — *이벤트 루프 전체가 멈춘다*. 8장의 *sync 600 req/s vs async + sync DB 550 req/s* 한 줄을 잊지 말자 ([Medium: Hidden Trap in FastAPI](https://medium.com/@patrickduch93/the-hidden-trap-in-fastapi-projects-accidently-using-sync-sql-alchemy-in-an-async-app-245b0391a17d)). *async는 잘 쓰면 빠르고, 잘못 쓰면 더 느리다.*

이 신호가 한국 커뮤니티에서 가장 흔히 놓치는 자리다. *Python이 비동기를 지원한다더라*는 인상 위에 *Spring WebFlux와 비슷한 마법*을 기대하면 — *프로덕션에서 다친다*.

### Spring 출신의 가장 큰 충격은 트랜잭션과 보안 자동화의 부재

이 책 전체의 *핵심 약속*이 이 자리에 박혀 있다. 1장의 약점 지도, 6장의 트랜잭션, 7장의 보안 — *세 챕터가 이 한 줄을 풀어쓴 챕터*다. Spring 출신이 *처음 다치는 자리*가 어디인지를 *책이 시작부터 끝까지 짚어주는 게* 우리 약속이었다.

다시 한 번 정리한다. *FastAPI는 트랜잭션을 자동으로 걸어주지 않는다. 보안을 자동으로 깔아주지 않는다. 그래서 우리가 손으로 짠다.* 이 *명시성*이 — 익숙해지면 *코드 위에 무엇이 일어나는지 보이는 든든함*으로 돌아온다. 익숙해지기까지가 — *책 한 권의 호흡*이다.

## §13.4 한국 도입 사례의 정직한 한계

한국 시장에서 *FastAPI를 어떤 회사가 어디에 쓰는가*는 — 한 명의 저자가 책으로 박을 만큼 *충분한 자료가 있지 않다*. 이 사실을 정직하게 인정하고 시작하자.

확인 가능한 영역은 *ML/데이터 플랫폼·내부 API*다. AI 모델 서빙, 데이터 사이언티스트 자체 도구, 사내 분석 어드민. 이 자리에서 FastAPI를 쓰는 한국 회사의 사례는 — 기술 블로그와 컨퍼런스 발표에서 *정황적으로* 확인된다. 카카오, 네이버, 당근, 우아한형제들 같은 *큰 조직의 ML/데이터 팀*에서 FastAPI를 보조 도구로 쓴다는 신호는 — 일반적으로 알려져 있다.

그러나 *메인 백엔드를 FastAPI로 짠다*는 명시적 사례는 — 본 책 집필 시점(2026-05) 기준 *결정적 증거가 부족*하다. Codenary 같은 기술 스택 디렉토리가 있지만 본 리서치에서 직접 접근에 어려움이 있었다. 책 마무리 자리에서 *없는 사실을 만들지 않는 것*이 우리 약속이다.

한국 시장의 진짜 그림은 — 한 줄로 말하면 — *Spring/Kotlin이 메인 백엔드, FastAPI가 보조·실험·ML*이다. 이 비대칭은 — *FastAPI가 부족해서*가 아니라 *한국 백엔드 진영의 자산이 Spring에 쌓여 있어서*다. 채용 시장, 기존 코드베이스, 신입 교육, 사내 표준 — *어디를 봐도 Spring이 메인*이다.

이 사실을 *변호하거나 부정할 자리는 아니다*. 그대로 인정하고, *그 위에서 어떻게 살아갈지*를 다음 절에서 짚는다.

## §13.5 한국 채용·생태계 현실 — 양 다리 전략

한국 백엔드 채용 공고를 100개쯤 펴보자. 어떤 그림이 나오는가?

*Java/Spring*이 압도적이다. *Kotlin/Spring*이 그 옆에 있다. *FastAPI*는 *있긴 있다* — ML 엔지니어, 데이터 엔지니어, 일부 스타트업의 백엔드, 그리고 *Python을 잘하는 백엔드를 찾는 ML 인프라 팀*에서.

이 그림 위에서 *Spring 출신이 FastAPI를 익히는 것*은 — *어떤 전략*인가?

**첫째, 양 다리 전략.** Spring을 *주력*으로 두되, FastAPI를 *보조 도구*로 갖춘다. 메인 백엔드 직군에서 일하면서 *ML 팀과의 협업이 필요할 때*, *사내 어드민을 빠르게 짤 때*, *데이터 파이프라인을 만질 때* — FastAPI 카드를 꺼낸다. 한 사람이 *둘 다 쓸 수 있는 것*이 — 한국 시장에서 *가장 안정적인 자리*다.

**둘째, 진영 전환 전략.** Spring 진영에서 *ML/데이터 진영으로* 옮긴다. ML 인프라 엔지니어, 데이터 플랫폼 개발자, 추천 시스템 개발자. *FastAPI가 메인 도구가 되는 자리*다. 한국 시장에서도 이 자리는 *늘어나고 있다* — 다만 *총량은 여전히 Spring보다 작다*. 도전은 가능하지만 *대안 직군이 적은 위험*은 정직하게 안고 가야 한다.

**셋째, 사이드 프로젝트·창업 전략.** 본업은 Spring, *사이드 프로젝트·MVP·창업 아이디어는 FastAPI*. 빠른 검증과 *Python 생태계 활용*이 필요한 자리에서 — *둘째 도구가 진짜 가치를 보인다*.

이 셋 중 *어느 것이 맞다고 박을 자리는 아니다*. 본인의 사정과 흥미에 따라 다르다. 다만 *Spring을 버리는 선택*은 — 한국 시장에서 *위험이 큰 결정*이라는 사실은 정직하게 짚어두자. 이 책은 *둘 다 쓸 수 있는 사람*을 만드는 책이다.

## §13.6 SQLModel을 권할 것인가

5장에서 우리는 *SQLAlchemy 2.0*을 선택했다. *SQLModel*에 대한 비교는 — *이 자리로 미뤘다*. 이제 짚자.

SQLModel은 FastAPI와 *같은 저자가 만든* 라이브러리다. *Pydantic 모델과 SQLAlchemy 모델을 하나로 합친다*. 같은 클래스가 — 입력 검증, 응답 직렬화, ORM 매핑, 마이그레이션 — 네 가지를 동시에 한다.

```python
# 파이썬 - SQLModel 예제
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
```

매력적이다. *DRY가 강력하고 학습 곡선이 낮다*. 한 모델이 모든 역할을 한다. ([Medium: SQLModel vs SQLAlchemy](https://medium.com/@bhagyarana80/sqlmodel-vs-sqlalchemy-cleaner-crud-with-metrics-9d50956f1015))

그런데 — 한 GitHub Discussion이 같은 자리를 짚는다 (저자의 영문 표현을 옮긴 한 줄) — *SQLModel은 SQLAlchemy 대비 확실히 느리다 — Pydantic 연산을 SQLAlchemy 위에 더 얹기 때문. 개발자 경험을 속도보다 우선한 라이브러리.* — [GitHub Discussion #645](https://github.com/fastapi/sqlmodel/discussions/645) (reference §5.5) 그리고 *복잡 쿼리나 방언 특수 기능에서는 결국 순수 SQLAlchemy로 떨어진다*는 보고도 같은 자리에 있다.

이 책의 결론은 — *Spring 출신은 SQLAlchemy 2.0으로 시작하라*다. 두 가지 이유다.

**첫째, JPA 사고가 SQLAlchemy 2.0에 더 자연스럽게 1:1 매핑된다.** Hibernate Session ↔ SQLAlchemy Session, JPA `@Entity` ↔ `DeclarativeBase`, JPQL ↔ Core expression. 5장에서 만진 매핑이 — *SQLModel에서는 한 단계 더 얇아진다*. *얇아진 게 좋다고 느낄 사람*도 있겠지만, *SQLAlchemy의 정공법*을 알고 가는 게 *Spring 출신의 손에 더 자연스럽다*.

**둘째, 결국 깊이 들어가면 SQLAlchemy를 직접 다룬다.** SQLModel이 가려준 *추상화 계층*이 — *방언 특수 기능, 복잡 조인, 인덱스 힌트* 같은 자리에서 *깨진다*. *추상화가 깨질 때 한 단계 더 내려갈 수 있어야* 안정적이다. SQLAlchemy를 *처음부터 알고 가는 길*이 — 멀리 보면 *이득*이다.

소규모 빠른 프로토타입에서 SQLModel을 쓰는 건 — *나쁘지 않은 선택*이다. 다만 *프로덕션급 시스템*에서는 — *SQLAlchemy 2.0 + Pydantic을 분리하는 길*을 권한다. 이 책의 5장이 그 길을 풀어냈다.

## §13.7 미래 변수 — 2026년 현재 우리가 모르는 것들

책은 *한 시점의 사진*이다. 2026년 5월에 쓴 이 책이 — *5년 뒤*에도 같은 권고를 할 수 있을까? 정직한 답은 — *모른다*. 다만 *지금 흐려져 있는 자리* 몇 개를 짚어두자. 독자가 책을 덮은 뒤에도 *눈을 둘 자리*다.

**첫째, Pydantic v2 안정화와 v3 가능성.** v1 → v2 마이그레이션이 2024~2025년 큰 작업이었다. v2의 Rust 코어가 정착했고, 의존 라이브러리들도 대부분 v2로 옮겨졌다. *언제 v3 논의가 시작될지*는 — 모른다. 다만 *v2가 한동안 안정적*이라는 신호는 있다.

**둘째, Free-threaded Python (PEP 703).** Python 3.13에서 *실험적으로* 도입된 GIL 제거 빌드다. *멀티스레드 진영의 자바*에 가까운 모델이 — Python에서도 가능해질 수 있다. 2026년 현재는 *실험적 상태*다. 프로덕션 가이드는 여전히 *프로세스 다중화*(uvicorn workers, K8s replicas). 3.14·3.15 정도에서 *기본값에 가까워질 것*이라는 신호가 있다. 그때가 되면 — *Java 스레드풀과의 비교*가 다시 쓰여야 할 것이다.

**셋째, ARQ vs Celery 성숙도 곡선.** 8장에서 *백그라운드 작업* 자리에 ARQ와 Celery를 같이 놓았다. Celery는 *성숙하고 검증됐지만 무겁다*. ARQ는 *asyncio 친화에 가볍지만 생태계가 작다*. 둘 사이의 *균형이 어디로 갈지*는 — 2026년 현재 흐려져 있다. 큰 시스템이라면 *Celery가 여전히 안전한 기본값*이다. 그러나 *몇 년 뒤*에는 — ARQ나 *다른 후속 도구*가 자리를 굳힐 가능성이 있다.

**넷째, FastAPI 자체의 진화.** 0.x 버전대를 오래 유지하다가 *1.0이 언제 나올지*가 — 한국 개발자 커뮤니티에서도 자주 묻는 질문이다. 0.115 같은 마이너 버전이 계속 올라가지만 *호환성 약속*은 — 정식 1.0이 나오기 전까지는 *느슨*하다. 큰 시스템이라면 — *마이너 업그레이드마다 리그레션 테스트*를 짜두는 게 안전하다.

이 네 자리 — *Pydantic, GIL, 큐, FastAPI 본체* — 가 흐려져 있다는 사실은 *책의 한계*다. 5년 뒤 이 책이 *얼마나 유효할지*는 — 솔직히 모른다. 다만 *Spring 사고로 FastAPI를 짓는 사고의 골격*은 — *프레임워크 버전이 바뀌어도 살아남는다*는 게 우리 약속이다.

## §13.8 두 프레임워크를 도구함에 두는 사고 — 의사결정 트리

이 절은 책 전체의 *결정 체계를 한 그림으로 압축*하는 자리다. 다음 결정 트리를 머리에 두면 — *새 프로젝트 앞에서 어느 도구를 고를지*가 빠르게 갈린다.

```
새 프로젝트가 들어왔다. 어느 도구로 짤까?

├─ Q1: ML/AI 모델을 직접 부르는가?
│  └─ YES → FastAPI (PyTorch/HuggingFace 직결)
│
├─ Q2: 빠른 MVP·실험 서비스인가? (3개월 안에 살아남을지 모른다)
│  └─ YES → FastAPI (초기 개발 비용)
│
├─ Q3: 사내 어드민·툴링·웹훅 처리인가? (트래픽 작고 도메인 단순)
│  └─ YES → FastAPI (가벼움)
│
├─ Q4: 복잡한 비즈니스 트랜잭션·대형 모놀리스인가?
│  └─ YES → Spring (생태계 성숙도)
│
├─ Q5: 엔터프라이즈 인테그레이션? (배치·메시징·규제)
│  └─ YES → Spring (Spring Batch, Spring Cloud)
│
├─ Q6: 팀이 50명 넘는가? Java/Kotlin 표준이 이미 있는가?
│  └─ YES → Spring (큰 팀의 합)
│
└─ DEFAULT: 한국 시장에서는 Spring/Kotlin이 기본값.
            FastAPI가 명백히 빛나는 자리에서만 골라 쓴다.
```

이 트리가 *완벽한 답*은 아니다. *조직의 사정, 팀의 경험, 기존 코드베이스*가 결정을 더 좌우한다. 다만 *한 도구로 모든 걸 해결하려는 사고*에서 — *두 도구를 도구함에 두는 사고*로 옮기는 출발점은 된다.

토비 *어떤 망치를 들 것인가*라는 표현을 한 번 떠올리자. 좋은 개발자는 *한 망치만 들지 않는다*. 망치 두 개, 드라이버 세 개, 톱 한 개. *문제마다 맞는 도구를 고를 줄 아는 것*이 — 8년 차 백엔드 개발자의 진짜 자산이다. 이 책이 *그 자산을 한 단계 늘리는 데 기여했다면* — 약속을 지킨 셈이다.

## §13.9 더 읽을 거리 — 책이 끝난 뒤 어디로 갈 것인가

마지막 자리다. 책을 덮은 뒤 *다음 단계로 가는 길*을 짚어두자. 단순한 링크 나열이 아니라, *각 자료가 왜 다음 단계인지*를 한두 줄로 짚는다.

### 공식 문서 — 가장 먼저

- **[FastAPI 공식 한국어 문서](https://fastapi.tiangolo.com/ko/)** — 이 책이 *Spring 사고에 다리를 놓는 자리*에 집중했다면, 공식 문서는 *FastAPI의 모든 기능을 망라*한다. 책에서 다루지 않은 WebSocket, GraphQL, 파일 업로드, 백그라운드 작업 디테일 — 다 여기 있다. 책을 덮은 직후 *가장 먼저 들러야 할 자리*다.
- **[Pydantic 공식 문서](https://docs.pydantic.dev/latest/)** — Pydantic v2의 깊은 자리. `field_validator`, `model_validator`, `RootModel`, JSON 스키마 커스터마이징. 책에서는 표면만 짚었다.
- **[SQLAlchemy 2.0 공식 문서](https://docs.sqlalchemy.org/en/20/)** — 5·6장에서 다룬 *Session·UoW·async* 너머의 자리. 특히 *비동기 SQLAlchemy*의 깊은 함정은 — 공식 문서가 가장 정직하게 짚는다.

### 한국어 자료 — 한 단계 더

- **[점프 투 FastAPI (WikiDocs)](https://wikidocs.net/175950)** — Spring 출신이 아니라 *Python 초보자를 위한* 자료지만, 한국어로 손에 익히고 싶은 자리가 있다면 좋은 출발점이다.
- **[한빛: FastAPI를 사용한 파이썬 웹 개발](https://m.hanbit.co.kr/store/books/book_view.html?p_code=B9703548802)** — 한국어 종이책이 필요하다면 검토해볼 만한 자리. 이 책과 *상보적*으로 읽을 수 있다.
- **[velog: FastAPI Good Practice (wjddn3711)](https://velog.io/@wjddn3711/FastAPI-Good-Practice)** — 한국 개발자의 *실무 패턴 정리*. 4장 *deps.py* 패턴, 5장 *by-feature 폴더 구조*가 — 이 글에서도 정착된 형태로 나온다.

### 영문 심층 자료 — 더 깊이 가고 싶을 때

- **[Matthew Brown: FastAPI database session dependency injection considered harmful](https://matthewbrown.io/2026/02/03/fastapi-session-dependency-injection)** — 6장 트랜잭션 본문에서 인용한 글. *Unit-of-Work 패턴*을 깊이 풀어쓴다.
- **[Medium: The Hidden Trap in FastAPI Projects](https://medium.com/@patrickduch93/the-hidden-trap-in-fastapi-projects-accidently-using-sync-sql-alchemy-in-an-async-app-245b0391a17d)** — 8장 *async + sync DB 함정*을 다시 풀어쓴 글. 책에서 짚은 신호의 *현장 데이터*가 더 자세히 있다.
- **[FastAPI Best Practices (GitHub: zhanymkanov)](https://github.com/zhanymkanov/fastapi-best-practices)** — 영문 진영의 *손에 익은 패턴 모음*. 책에서 짚지 않은 자질구레한 손버릇이 정리돼 있다.

### Spring 진영을 잊지 않기

- **[토비의 Spring](https://search.shopping.naver.com/book/catalog/32487732170)** — 한국 Spring 진영의 *교과서*다. FastAPI를 손에 익히는 동안 — *Spring 사고의 깊이*를 잃지 않으려면 한 번씩 돌아봐야 한다.
- **[Spring Cloud 공식 문서](https://spring.io/projects/spring-cloud)** — *마이크로서비스·분산 시스템*의 자리. FastAPI 진영에서 이 깊이를 갖춘 통합 도구는 — 아직 없다. Spring 진영의 자산이 *왜 한국 대기업의 메인인지*가 — 이 자리에서 보인다.

### 책이 끝난 뒤의 한 단계

마지막으로 *책이 닫힌 다음 한 줄*을 권한다. **본인의 사이드 프로젝트에 FastAPI를 한 번 써보자.** 작은 도메인이면 된다. 가계부, 운동 기록기, 독서 노트, 슬랙 봇. *읽은 것을 손에 쥐는 가장 빠른 길*은 — 짜보는 것이다. 이 책에서 만진 모든 패턴이 — *한 작은 프로젝트 안에서* 한 번씩 흐른다. 트랜잭션, 인증, 비동기, 테스트, 배포. *작은 코드 한 개*가 책 전체의 호흡을 *손에 새긴다*.

## 책을 닫으며

한 권의 호흡이 여기서 끝난다.

1장에서 *왜 FastAPI인가, 왜 Spring 출신에게 친숙한가*로 시작했다. 매핑 표 한 장을 펼치고, *정직한 약점 네 가지*를 미리 깔아두었다. 2장부터 8장까지 *환경·라우트·DI·DB·트랜잭션·보안·async*의 일곱 영역을 차례로 만졌다. 9·10·11장에서 *관측성·테스트·배포*의 운영 손길을 익혔다. 12장에서 *통합 프로젝트*로 한 번에 묶었다.

그리고 마지막 13장은 — *책이 끝난 뒤 어디로 갈지*를 짚었다. *FastAPI를 손에 익혔지만 Spring을 버리지 않는 길*. 한국 시장에서 *둘 다 쓰는 사람이 되는 길*. *몇 년 뒤 모르는 자리*에 정직하게 눈을 두는 길.

책의 약속을 한 줄로 정리하자. *@Transactional이 없는 세상에서 Spring 사고로 FastAPI를 짓는 법*. *옮긴다*가 아니라 *짓는다*. *대체*가 아니라 *상보*. *버리는 책이 아니라 더하는 책*.

여기까지 함께 와줘서 고맙다. 이제 — *손에 흙을 묻힐 자리는 본인의 코드 앞이다*. 가서 짜자. 잘 짜질 때마다 — *8년 차의 Spring 사고가 한 단계 넓어졌다*는 신호다. 안 짜질 때마다 — *이 책의 어느 챕터*가 그 자리에 있다는 사실을 기억해두자. 어디로 돌아와도 좋다.

좋은 코드 짓기를. 잘 가자.


---

---

## 에필로그 — 한 권의 호흡을 닫으며

서문에서 우리는 한 질문에서 출발했다. *내가 알고 있던 Spring 사고를 여기서도 써먹을 수 있을까? 아니면 전부 버리고 처음부터 다시 배워야 할까?*

13장을 다 거친 지금, 답은 손에 잡혔을 것이다. *둘 다 아니다.* Spring 사고는 그대로 가져가되, 어느 자리에선 *번역*하고, 어느 자리에선 *직접 짠다*. 그 회로가 머리에 박혔다면 — 이 책은 약속을 지킨 셈이다.

### 우리가 그린 지도를 한 번 더 펴보자

**1막에서 친숙함을 깔았다.** FastAPI는 얇은 프레임워크다. Starlette + Pydantic + uvicorn의 조합 위에 타입 힌트가 검증·직렬화·문서의 단일 소스가 된다. `uv`로 작업대를 세우고, 첫 라우트를 한 함수로 짰다. Spring과 *1:1로 그려지는* 영역이 의외로 많다는 사실이 — 발걸음을 가볍게 했다.

**2막에서 충돌을 받았다.** 4장의 `Depends()`에서 *그래프가 코드 위에 보인다*는 감각을 손에 들였다. 5장의 SQLAlchemy 2.0에서 *명시성*이 어떤 모양인지 처음 마주쳤다. 6장의 트랜잭션이 책의 가장 큰 hinge였다 — `@Transactional` 한 줄이 사라진 자리에 `async with session.begin():` 한 블록이 들어선다. 7장의 인증·인가에서 같은 통주저음이 한 번 더 흘렀고, 8장의 비동기에서 *async가 항상 빠르지 않다*는 신호를 받았다. 자동의 자리에 명시가 들어선다 — 이 한 줄이 2막의 정수였다.

**3막에서 운영을 묶었다.** 9장의 도메인 예외 + 미들웨어 + Prometheus + OpenTelemetry. 10장의 TestClient + pytest + Testcontainers + SAVEPOINT 픽스처. 11장의 multi-stage Dockerfile + K8s replica + 세 가지 메모리 도구. 12장이 그 모든 조각을 한 코드베이스 안에 묶었고, 13장이 *언제 Spring으로 돌아가야 하는가*를 정직하게 짚었다.

### 이 책이 답하지 못한 것들

정직하게 짚자. 이 책이 답하지 못한 자리가 있다.

**첫째, 미래 변수.** Pydantic v3 가능성, free-threaded Python(PEP 703)의 정착 시점, ARQ vs Celery의 성숙도 곡선, FastAPI 1.0의 호환성 약속. 2026년 5월 현재 이 자리들은 흐려져 있다. 5년 뒤 이 책의 어느 권고가 *여전히 유효한지*는 — 솔직히 모른다. 다만 *Spring 사고로 FastAPI를 짓는 사고의 골격*은 — 프레임워크 버전이 바뀌어도 살아남는다는 게 우리 약속이다.

**둘째, 한국 도입 사례의 본격적 지도.** 13장 §13.4에서 짚었듯, 한국 시장에서 *FastAPI를 메인 백엔드로 쓰는 회사*의 명시적 사례는 — 책 집필 시점에 결정적 증거가 부족했다. ML/데이터 플랫폼 영역에서 보조적으로 쓰는 신호는 일반적으로 알려져 있지만, *없는 사실을 만들지 않는다*는 책의 약속을 지켰다. 5년 뒤에는 그림이 달라져 있을 것이다 — 그 변화를 책 한 권의 호흡 안에 다 담기는 어렵다.

**셋째, 한 사람이 짠 코드의 한계.** 12장의 통합 프로젝트는 *한 가지 패턴*을 보여준다. 같은 도메인을 *다른 팀, 다른 아키텍처 결정, 다른 사내 표준*으로 짜면 코드는 다르게 흐른다. 이 책의 패턴은 *출발점*이지 *유일한 정답*이 아니다.

### 다음 걸음

책을 닫은 뒤 한 가지를 권한다. **본인의 사이드 프로젝트에 FastAPI를 한 번 써보자.** 작은 도메인이면 된다. 가계부, 운동 기록기, 독서 노트, 슬랙 봇. *읽은 것을 손에 쥐는 가장 빠른 길*은 — 짜보는 것이다. 이 책에서 만진 모든 패턴이 — 한 작은 프로젝트 안에서 한 번씩 흐른다. 트랜잭션, 인증, 비동기, 테스트, 배포. *작은 코드 한 개*가 책 전체의 호흡을 *손에 새긴다*.

그리고 — Spring을 잊지 말자. 한국 시장에서 *Spring이 메인이라는 사실*은 안 변한다. 이 책은 *그 위에 두 번째 도구함을 얹는 책*이었다. 잘 쓰던 망치를 버릴 이유는 없다. 새 망치를 *옆에* 두고, 문제마다 맞는 도구를 고를 수 있게 되는 것 — 그게 8년 차 백엔드 개발자의 진짜 자산이다.

여기까지 함께 와줘서 고맙다. 좋은 코드 짓기를. 잘 가자.

---

## 부록 A. Spring ↔ FastAPI 매핑 한눈에

1장의 매핑 표를 *확장한 형태*로 한 자리에 모아둔다. 책을 덮고 손이 멈출 때 펴볼 수 있는 단일 페이지의 지도다. 책 본문에서 다룬 *어느 장*에 디테일이 있는지도 같이 적었다.

### 라우팅·요청·응답

| 카테고리 | Spring / Java | FastAPI / Python | 책의 다룸 |
|---|---|---|---|
| HTTP 라우팅 | `@RestController` + `@GetMapping` | `@app.get("/path")` 데코레이터 | 3장 |
| 라우터 그룹 | `@RequestMapping("/users")` 클래스 prefix | `APIRouter(prefix="/users")` | 4장 §APIRouter, 12장 |
| 경로 변수 | `@PathVariable Long id` | `user_id: int` (타입 힌트로 자동) | 3장 |
| 쿼리 파라미터 | `@RequestParam("from") String from` | `Annotated[str, Query(alias="from")]` | 3장 |
| 요청 본문 바인딩 | `@RequestBody @Valid UserCreate dto` | `payload: UserCreate` (Pydantic) | 3장 |
| 헤더 바인딩 | `@RequestHeader("X-Token") String token` | `Annotated[str, Header()]` | 3장 |
| 폼 데이터 | `@RequestParam MultiValueMap` | `OAuth2PasswordRequestForm` 등 | 7장 |
| 응답 직렬화 | Jackson `ObjectMapper` + `@JsonProperty` | Pydantic `model_dump()` + `response_model` | 3장 |
| 상태 코드 | `ResponseEntity.status(201)` | `status_code=201` 인자 | 3·9장 |
| 스트리밍 응답 | `Flux<ServerSentEvent<T>>` (WebFlux) | `StreamingResponse(generator, media_type="text/event-stream")` | 12장 §SSE |

### 검증·DTO·직렬화

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| 검증 | `jakarta.validation.constraints.*` | Pydantic `Field`, `field_validator`, `model_validator` | 3장 |
| 검증 실패 응답 | `MethodArgumentNotValidException` 핸들러 | 자동 `422 Unprocessable Entity` | 3·9장 |
| 모델 분리 | `record`·class를 여러 개 | `XxxCreate` / `XxxRead` / `XxxInDB` 컨벤션 | 3장 |
| 엔티티↔DTO 변환 | MapStruct / ModelMapper | `Model.model_validate(entity)` | 3·5장 |
| JSON 라이브러리 | Jackson | Pydantic v2 / orjson | 3장 |
| OpenAPI 문서 | `springdoc-openapi` + 어노테이션 | 자동 생성 (`/docs`, `/redoc`) | 3장 |

### 의존성 주입과 횡단 관심

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| DI / IoC | `@Component`, `@Autowired`, `@Bean` | `Depends(...)` (함수 파라미터 마커) | 4장 |
| 기본 스코프 | 싱글톤 | 요청 단위(`@RequestScope` 모델) | 4장 |
| 싱글톤 자원 | 기본값 | `lifespan` 컨텍스트, 모듈 상수, `@lru_cache` | 4·12장 |
| 라이프사이클 자원 | `@PreDestroy` + `try-with-resources` | `yield` 의존성 | 4·5·6장 |
| 횡단 관심 (전역) | `Filter`, `HandlerInterceptor` | ASGI 미들웨어 | 4·9·12장 |
| 횡단 관심 (선택) | `@Aspect`, `@Around`, `@PreAuthorize` | 라우트 `dependencies=[Depends(...)]` | 4·7장 |
| 테스트 모킹 | `@MockBean` (컨테이너 재구성) | `app.dependency_overrides[fn] = ...` (한 줄) | 4·10장 |
| 설정 주입 | `@Value`, `@ConfigurationProperties` | `pydantic-settings.BaseSettings` | 7·11장 |

### 데이터·트랜잭션

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| ORM | Hibernate / Spring Data JPA | SQLAlchemy 2.0 | 5장 |
| 모델 정의 | `@Entity` + `@Column` | `class X(DeclarativeBase)` + `Mapped[...]` | 5장 |
| 쿼리 | JPQL / Criteria API | `select(...).where(...)` Core expression | 5장 |
| 1차 캐시 | `EntityManager` | `Session` (Identity Map + UoW) | 5장 |
| 레포지토리 | `extends JpaRepository<T, ID>` 자동 구현 | 손으로 작성 (자동화 없음) | 5장 |
| Lazy 함정 | `LazyInitializationException` | `DetachedInstanceError` — `selectinload` 권장 | 5·12장 |
| 마이그레이션 | Flyway / Liquibase | Alembic | 5장 |
| **선언적 트랜잭션** | `@Transactional` | **`async with session.begin():`** | **6장 (책의 hinge)** |
| 전파 옵션 | `@Transactional(propagation=...)` | 세션 공유 + 최상위 블록 | 6장 |
| 격리 수준 | `@Transactional(isolation=...)` | `execution_options(isolation_level=...)` | 6장 |
| Savepoint | `@Transactional(propagation=NESTED)` | `session.begin_nested()` | 6장 |
| 비관적 락 | `findByIdForUpdate(id)` | `db.get(X, id, with_for_update=True)` | 6장 |
| 커밋 후 이벤트 | `@TransactionalEventListener(AFTER_COMMIT)` | `with` 블록 종료 뒤 `BackgroundTasks.add_task` | 12장 |

### 보안

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| 보안 모듈 | Spring Security | (없음) — 직접 조립 | 7장 |
| 인증 의존성 | `SecurityFilterChain` | `Depends(get_current_user)` | 7장 |
| 권한 검사 | `@PreAuthorize("hasRole('ADMIN')")` | `Security(get_current_user, scopes=["admin"])` | 7장 |
| 토큰 발급 | `JwtBuilder` + `AuthenticationManager` | `python-jose` + `/auth/login` 라우트 | 7장 |
| 비밀번호 해싱 | `PasswordEncoder` (`BCryptPasswordEncoder`) | `passlib` (`bcrypt` 또는 `argon2`) | 7장 |
| CSRF 보호 | 기본 ON, SPA는 `csrf().disable()` | 기본 없음 — 토큰 저장 위치로 결정 | 7장 |
| 모의 인증 테스트 | `@WithMockUser(roles="ADMIN")` | `app.dependency_overrides[get_current_user] = ...` | 7·10장 |

### 비동기·동시성·백그라운드

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| 비동기 모델 | WebFlux + Reactor + Netty | `async/await` + asyncio + uvicorn | 8장 |
| 동기/비동기 라우트 | MVC vs WebFlux 분리 | `def`/`async def` 한 앱에 공존 | 8장 |
| 블로킹 호출 격리 | `Schedulers.boundedElastic()` | `asyncio.to_thread`, `run_in_threadpool` | 8장 |
| 자동 스레드풀 | (없음) | `def` 라우트가 자동 threadpool로 | 8장 |
| 코루틴 비교 | Kotlin `suspend fun` | Python `async def` | 8장 §Kotlin |
| 구조적 동시성 | `coroutineScope { ... }` (Kotlin) | `asyncio.TaskGroup` (3.11+) | 8장 |
| Fire-and-forget | `@Async` | `BackgroundTasks` | 8·12장 |
| 스케줄러 | `@Scheduled(cron=...)` | APScheduler | 8장 |
| asyncio 분산 큐 | (해당 없음) | ARQ | 8·12장 |
| 성숙한 분산 큐 | Spring + RabbitMQ/Kafka | Celery | 8장 |

### 예외·로깅·관측성

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| 전역 예외 핸들러 | `@RestControllerAdvice` + `@ExceptionHandler` | `@app.exception_handler(MyExc)` | 9장 |
| 캐치올 | `@ExceptionHandler(Exception.class)` | `@app.exception_handler(Exception)` | 9장 |
| MDC | SLF4J `MDC.put("requestId", ...)` | `structlog` + `ContextVar` + 요청 ID 미들웨어 | 9장 |
| 구조화 로깅 | Logback + JSON encoder | `structlog` + `JSONRenderer` | 9장 |
| 메트릭 | Micrometer + Prometheus | `prometheus-fastapi-instrumentator` + 도메인 카운터 | 9장 |
| 트레이싱 | Spring Cloud Sleuth → OpenTelemetry | OpenTelemetry SDK + `FastAPIInstrumentor` | 9장 |
| 헬스 체크 | `/actuator/health` (자동) | `/healthz` + `/readyz` 직접 짜기 | 9·11장 |
| Spring Boot Admin 통합 | 기본 통합 | `pyctuator` | 9장 |

### 테스트·배포·운영

| 카테고리 | Spring | FastAPI | 책의 다룸 |
|---|---|---|---|
| 테스트 프레임워크 | JUnit 5 | pytest | 10장 |
| HTTP 테스트 | MockMvc | `TestClient(app)` | 10장 |
| 비동기 테스트 | WebTestClient | `pytest-asyncio` + `httpx.AsyncClient` | 10장 |
| 통합 테스트 | `@SpringBootTest` (컨테이너 재시작) | `TestClient(app)` (재시작 없음) | 10장 |
| 모킹 | Mockito `@Mock` | `unittest.mock`, `pytest-mock`, FakeXxx 클래스 | 10장 |
| 트랜잭션 격리 | `@Transactional` 자동 롤백 | SAVEPOINT 기반 fixture (직접 짜기) | 6·10장 |
| 실제 DB 컨테이너 | Testcontainers | Testcontainers Python (이름 동일) | 10·12장 |
| 계약 테스트 | Spring Cloud Contract | pact-python | 10장 |
| 빌드/의존성 | Maven / Gradle | `pyproject.toml` + uv / Poetry | 2장 |
| 컨테이너 빌드 | jib / `Dockerfile` | `Dockerfile` + `uv sync --frozen` + multi-stage | 11장 |
| 서버 런타임 | Tomcat (스레드풀 하나) | uvicorn (이벤트 루프) × replica 여럿 | 11장 |
| 워커 모델 (VM) | `java -jar` + Tomcat 스레드풀 | Gunicorn + Uvicorn worker × N | 11장 |
| 워커 모델 (K8s) | replica 여럿 | **컨테이너당 단일 Uvicorn 프로세스** + replica | 11장 |
| 그레이스풀 셧다운 | `@PreDestroy` + `server.shutdown=graceful` | `lifespan` 컨텍스트 + tini PID 1 | 11장 |
| 시크릿 관리 | `@Value("${...}")`, Spring Config | `pydantic-settings.BaseSettings` + K8s Secret | 7·11장 |
| 프록시 헤더 | `RemoteIpValve` 자동 | `uvicorn --proxy-headers --forwarded-allow-ips` | 11장 |

### 메모리·프로파일링 — JVM 도구 체인의 빈자리

| Spring/JVM 도구 | FastAPI/Python 대응 | 책의 다룸 |
|---|---|---|
| `jmap`, 힙덤프 | `memray` (스테이징·로컬 분석) | 11장 |
| VisualVM, MAT | `memray flamegraph` | 11장 |
| `jstack` (살아 있는 스레드) | `py-spy dump/top --pid` (살아 있는 컨테이너) | 11장 |
| `jstat` GC 통계 | `tracemalloc` (표준 라이브러리, 가벼운 의심) | 11장 |
| JVM `-Xmx` | K8s `resources.limits.memory` + 컨테이너당 단일 프로세스 | 11장 |

---

## 부록 B. 더 읽을 거리 — 큐레이션 가이드

13장 §13.9의 더 읽을 거리를 책 끝에 한 번 더 모은다. 큐레이션이라 *왜 다음 단계인지*를 한두 줄 해설로 같이 둔다.

### 공식 문서 — 가장 먼저

- **[FastAPI 공식 한국어 문서](https://fastapi.tiangolo.com/ko/)** — 이 책이 *Spring 사고에 다리를 놓는 자리*에 집중했다면, 공식 문서는 *FastAPI의 모든 기능을 망라*한다. WebSocket, GraphQL, 파일 업로드 디테일이 거기 있다. 책을 덮은 직후 *가장 먼저 들러야 할 자리*다.
- **[Pydantic 공식 문서](https://docs.pydantic.dev/latest/)** — Pydantic v2의 깊은 자리. `field_validator`, `model_validator`, `RootModel`, JSON 스키마 커스터마이징. 책에서는 표면만 짚었다.
- **[SQLAlchemy 2.0 공식 문서](https://docs.sqlalchemy.org/en/20/)** — 5·6장에서 다룬 *Session·UoW·async* 너머의 자리. 특히 *비동기 SQLAlchemy*의 깊은 함정은 — 공식 문서가 가장 정직하게 짚는다.
- **[Starlette 공식 문서](https://www.starlette.io/)** — FastAPI 아래의 ASGI 토대. 미들웨어 깊이 들어갈 때 한 번 들러야 한다.
- **[Alembic 공식 문서](https://alembic.sqlalchemy.org/en/latest/)** — Flyway 사고 위에서 *Python 일급* 마이그레이션을 익힐 자리. `--autogenerate`의 한계도 같은 문서가 정직하게 짚는다.

### 한국어 자료 — 한 단계 더

- **[점프 투 FastAPI (WikiDocs)](https://wikidocs.net/175950)** — Spring 출신이 아니라 *Python 초보자를 위한* 자료지만, 한국어로 손에 익히고 싶은 자리가 있다면 좋은 출발점이다.
- **[velog: FastAPI Good Practice (wjddn3711)](https://velog.io/@wjddn3711/FastAPI-Good-Practice)** — 한국 개발자의 *실무 패턴 정리*. 4장 *deps.py* 패턴, 5장 *by-feature 폴더 구조*가 — 이 글에서도 정착된 형태로 나온다. 본 책의 패턴 선택이 *한국 개발자 진영의 손짐작*과 일치한다는 신호다.
- **[velog: FastAPI에서 Spring으로 마이그레이션하며 배운 점 (thedev_junyoung)](https://velog.io/@thedev_junyoung)** — 13장에서 인용한 글. *반대 방향의 경험치*가 정직하게 적혀 있다. *FastAPI가 다치는 자리*를 한국 시장의 톤으로 짚을 때 한 번 더 펴볼 만하다.
- **[velog: FastAPI 써 본 후기 (koeunyeon)](https://velog.io/@koeunyeon/FastAPI-%EC%8D%A8-%EB%B3%B8-%ED%9B%84%EA%B8%B0)** — *"오토바이인 척하는 자전거"*라는 한 줄로 한국 Spring 출신의 *어중간한 자리* 감각을 짚은 글. 이 책 1장이 같은 자리를 정직하게 짚은 출발점이다.

### 영문 심층 자료 — 더 깊이 가고 싶을 때

- **Matthew Brown, *"FastAPI database session dependency injection considered harmful"*** — 6장 트랜잭션 본문에서 인용한 글. *요청-내 longtail 트랜잭션* 문제와 *Unit-of-Work 패턴*을 깊이 풀어쓴다. 6장의 표면만 만진 독자라면 한 번 더 들러보자.
- **Patrick Duch, *"The Hidden Trap in FastAPI Projects: Accidentally Using Sync SQLAlchemy in an Async App"*** (Medium) — 8장 *async + sync DB 함정*을 다시 풀어쓴 글. 책에서 짚은 sync 600 req/s vs async + sync 550 req/s 신호의 *현장 데이터*가 더 자세히 있다.
- **iklobato, *"Mastering Gunicorn and Uvicorn"*** (Medium) — 11장 워커 공식과 K8s 패턴의 출처. *VM 시대와 K8s 시대의 차이*를 한 번 더 정리하고 싶을 때.
- **[FastAPI Best Practices (GitHub: zhanymkanov)](https://github.com/zhanymkanov/fastapi-best-practices)** — 영문 진영의 *손에 익은 패턴 모음*. 책에서 짚지 않은 자질구레한 손버릇이 정리돼 있다. 5장의 by-feature 폴더 구조가 *영문 진영의 모범*과도 같은 자리에 있다.
- **PyCon US 2026, *"FastAPI Security Patterns"*** — 7장 *리소스 서버 패턴*의 출처. 인증 책임을 분리하는 *큰 시스템의 그림*을 한 번 더 보고 싶을 때.

### 학술·연구 자료

- **Khan, M. M. R., Bavota, G., Lanza, M. & Spadaro, A. (2021). *On the Effectiveness of Type Hinting Bugs in Python.* IEEE Transactions on Software Engineering.** — 1·3·13장에서 인용한 *15% 결함 차단* 숫자의 출처. PDF: [rebels.cs.uwaterloo.ca](https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf). 타입 힌트의 *진짜 안전망 크기*를 정직하게 알고 싶을 때.

### Spring 진영을 잊지 않기

- **이일민, *『토비의 Spring 3』***. 한국 Spring 진영의 *교과서*다. FastAPI를 손에 익히는 동안 — *Spring 사고의 깊이*를 잃지 않으려면 한 번씩 돌아봐야 한다. *명시성*과 *자동화*의 균형을 책의 호흡으로 새기고 싶을 때.
- **[Spring Cloud 공식 문서](https://spring.io/projects/spring-cloud)** — *마이크로서비스·분산 시스템*의 자리. FastAPI 진영에서 이 깊이를 갖춘 통합 도구는 — 아직 없다. Spring 진영의 자산이 *왜 한국 대기업의 메인인지*가 — 이 자리에서 보인다.

### 책이 끝난 뒤의 한 단계

마지막으로 — *책*이 아닌 *행동*을 권한다. **본인의 사이드 프로젝트에 FastAPI를 한 번 써보자.** 가계부, 운동 기록기, 독서 노트, 슬랙 봇. *읽은 것을 손에 쥐는 가장 빠른 길*은 — 짜보는 것이다.

---

## 참고문헌

본문에서 인용한 자료를 한 자리에 모은다. 첫 등장 챕터 순서로 정렬했다. 각 항목은 *왜 인용했는지*가 본문에 짧게 적혀 있으니, 출처를 다시 확인하고 싶다면 이 목록을 통해 원자료로 돌아갈 수 있다.

### 한국어 자료

1. **koeunyeon. "FastAPI 써 본 후기." velog.** [https://velog.io/@koeunyeon/FastAPI-써-본-후기](https://velog.io/@koeunyeon/FastAPI-%EC%8D%A8-%EB%B3%B8-%ED%9B%84%EA%B8%B0) — 1·13장에서 인용. "오토바이인 척하는 자전거"라는 한 줄과 *큰 팀에서 표준이 없다*는 관찰.

2. **thedev_junyoung. "FastAPI에서 Spring으로 마이그레이션하며 배운 점." velog.** [https://velog.io/@thedev_junyoung](https://velog.io/@thedev_junyoung/SpringFastAPIFastAPI%EC%97%90%EC%84%9C-Spring%EC%9C%BC%EB%A1%9C-%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98%ED%95%98%EB%A9%B0-%EB%B0%B0%EC%9A%B4-%EC%A0%90) — 1·13장에서 인용. "복잡한 비즈니스 로직과 대규모 트래픽엔 Spring이 더 적합"이라는 한 줄.

3. **wjddn3711. "FastAPI Good Practice." velog.** [https://velog.io/@wjddn3711/FastAPI-Good-Practice](https://velog.io/@wjddn3711/FastAPI-Good-Practice) — 4·7장에서 인용. *deps.py 패턴*과 *모듈 레벨 설정 변수* 권장의 출처.

### 영문 자료 — 블로그·Medium

4. **"FastAPI vs Spring Boot: I Tested Both for 6 Months in Production." Medium, Engineering Playbook.** [https://medium.com/engineering-playbook/fastapi-vs-spring-boot-i-tested-both-for-6-months-in-production-96c04f7ebabe](https://medium.com/engineering-playbook/fastapi-vs-spring-boot-i-tested-both-for-6-months-in-production-96c04f7ebabe) — 1·7·11장에서 인용. *한 회사의 6개월 비교 사례* — 메모리 누수(180MB→600MB), 보안 이슈 비율, 운영 비용(480h vs 160h) 등.

5. **Patrick Duch. "The Hidden Trap in FastAPI Projects: Accidentally Using Sync SQLAlchemy in an Async App." Medium.** [https://medium.com/@patrickduch93/the-hidden-trap-in-fastapi-projects-accidently-using-sync-sql-alchemy-in-an-async-app-245b0391a17d](https://medium.com/@patrickduch93/the-hidden-trap-in-fastapi-projects-accidently-using-sync-sql-alchemy-in-an-async-app-245b0391a17d) — 8·13장에서 인용. *async + sync SQLAlchemy* 함정의 현장 데이터.

6. **Matthew Brown. "FastAPI database session dependency injection considered harmful." 개인 블로그.** [https://matthewbrown.io/2026/02/03/fastapi-session-dependency-injection](https://matthewbrown.io/2026/02/03/fastapi-session-dependency-injection) — 6장에서 인용. *요청-내 longtail 트랜잭션*과 *Unit-of-Work* 대안.

7. **iklobato. "Mastering Gunicorn and Uvicorn." Medium.** — 11장에서 인용. *Gunicorn-Uvicorn 분업*과 *워커 공식*, K8s에서의 *컨테이너당 단일 프로세스* 권고.

8. **딜리버스(Deliverus). "Exception Handling Best Practices in FastAPI." Medium.** — 9장에서 인용. 라우트 안 `try/except` 도배 회피와 전역 핸들러 위임.

9. **QuietShark Blog. "SQLAlchemy Unit-of-Work Notes."** — 6장에서 인용. Hibernate Session ↔ SQLAlchemy UoW의 차이와 "*우연한 commit-타이밍 버그를 0에 가깝게*"라는 평가.

10. **"SQLModel vs SQLAlchemy: Cleaner CRUD with Metrics." Medium (bhagyarana80).** [https://medium.com/@bhagyarana80/sqlmodel-vs-sqlalchemy-cleaner-crud-with-metrics-9d50956f1015](https://medium.com/@bhagyarana80/sqlmodel-vs-sqlalchemy-cleaner-crud-with-metrics-9d50956f1015) — 13장에서 인용. SQLModel의 *DRY 매력*과 성능 격차 데이터.

### 공식 문서·GitHub Discussion

11. **FastAPI 공식 문서 — Request-scoped transactions / Background Tasks / Dependencies / Security / Deployment.** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) — 4·5·6·8·9·11장 곳곳에서 인용. 의존성 `finally` 함정, `BackgroundTasks`의 한계, K8s 단일 프로세스 권고 등.

12. **FastAPI GitHub Discussions #6452 — Request-scoped transactions.** [https://github.com/fastapi/fastapi/discussions/6452](https://github.com/fastapi/fastapi/discussions/6452) — 5·6장에서 인용. *의존성 `finally`에서 `commit` 호출이 응답 뒤에 실행되는* 함정의 출처.

13. **SQLModel GitHub Discussion #645.** [https://github.com/fastapi/sqlmodel/discussions/645](https://github.com/fastapi/sqlmodel/discussions/645) — 13장에서 인용. *SQLModel이 SQLAlchemy 대비 느린 이유*와 *개발자 경험을 속도보다 우선한* 설계 결정.

14. **SQLAlchemy 공식 문서 — Joining a Session into an External Transaction (such as for test suites).** [https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites) — 6·10장에서 인용. *SAVEPOINT 기반 fixture* 패턴.

### 컨퍼런스·학술

15. **PyCon US 2026. "FastAPI Security Patterns."** [https://us.pycon.org/2026/schedule/presentation/34/](https://us.pycon.org/2026/schedule/presentation/34/) — 7장에서 인용. *리소스 서버 패턴* 권고와 *토큰 발급/검증 분리*.

16. **Khan, M. M. R., Bavota, G., Lanza, M. & Spadaro, A. (2021). "On the Effectiveness of Type Hinting Bugs in Python." IEEE Transactions on Software Engineering.** PDF: [https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf](https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf) — 1·3·13장에서 인용. *15%의 결함이 mypy로 막힐 수 있다*는 정량 데이터.

### 표준·사양

17. **PEP 20 — The Zen of Python.** [https://peps.python.org/pep-0020/](https://peps.python.org/pep-0020/) — 6장에서 인용. *"Explicit is better than implicit"*가 본 책 6·7장의 통주저음의 출처.

18. **PEP 621 — Storing project metadata in pyproject.toml.** [https://peps.python.org/pep-0621/](https://peps.python.org/pep-0621/) — 2장에서 참조. `pyproject.toml`의 공식 표준.

19. **PEP 703 — Making the Global Interpreter Lock Optional in CPython.** [https://peps.python.org/pep-0703/](https://peps.python.org/pep-0703/) — 1·8·13장에서 인용. *Free-threaded Python*의 2026년 현재 상태.

### 도구·라이브러리 공식 자료

20. **uv (Astral).** [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) — 2·11장에서 사용. Rust 기반 Python 패키지 매니저.

21. **ruff (Astral).** [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/) — 2장에서 사용. Rust 기반 린터/포매터.

22. **passlib + bcrypt/argon2.** [https://passlib.readthedocs.io/](https://passlib.readthedocs.io/) — 7장에서 사용. 비밀번호 해싱 표준.

23. **structlog.** [https://www.structlog.org/](https://www.structlog.org/) — 9·12장에서 사용. 구조화 로깅.

24. **Prometheus FastAPI Instrumentator.** [https://github.com/trallnag/prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator) — 9·12장에서 사용. Prometheus 메트릭 한 줄 도입.

25. **OpenTelemetry FastAPI Instrumentation.** [https://opentelemetry.io/docs/instrumentation/python/](https://opentelemetry.io/docs/instrumentation/python/) — 9장에서 사용. 분산 추적.

26. **pyctuator.** [https://github.com/SolarEdgeTech/pyctuator](https://github.com/SolarEdgeTech/pyctuator) — 9장에서 인용. Spring Boot Admin 호환 Python 구현.

27. **Testcontainers Python.** [https://testcontainers-python.readthedocs.io/](https://testcontainers-python.readthedocs.io/) — 10·12장에서 사용. 진짜 DB 컨테이너로 통합 테스트.

28. **memray (Bloomberg).** [https://github.com/bloomberg/memray](https://github.com/bloomberg/memray) — 11장에서 사용. Python 메모리 프로파일러.

29. **py-spy.** [https://github.com/benfred/py-spy](https://github.com/benfred/py-spy) — 11장에서 사용. 살아 있는 Python 프로세스 프로파일링.

30. **ARQ.** [https://arq-docs.helpmanual.io/](https://arq-docs.helpmanual.io/) — 8·12장에서 사용. asyncio 친화 분산 큐.

31. **APScheduler.** [https://apscheduler.readthedocs.io/](https://apscheduler.readthedocs.io/) — 8장에서 사용. 인-프로세스 cron 스케줄러.

32. **Celery.** [https://docs.celeryq.dev/](https://docs.celeryq.dev/) — 8장에서 인용. 성숙한 분산 큐.

33. **pact-python.** [https://github.com/pact-foundation/pact-python](https://github.com/pact-foundation/pact-python) — 10장에서 인용. Spring Cloud Contract와 같은 진영의 *컨슈머 주도 계약 테스트*.

### 책

34. **이일민. *토비의 Spring 3.* 에이콘출판.** [https://search.shopping.naver.com/book/catalog/32487732170](https://search.shopping.naver.com/book/catalog/32487732170) — 부록 B에서 권장. 한국 Spring 진영의 교과서.
