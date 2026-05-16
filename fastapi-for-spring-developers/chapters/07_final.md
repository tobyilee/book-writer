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
