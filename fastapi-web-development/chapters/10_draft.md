# 10장. 인증과 인가 — Spring Security를 직접 조립하기

`passlib`의 마지막 릴리스는 1.7.4이고, 2020년 10월 8일에 올라왔다.

그 라이브러리가 더는 관리되지 않는 것 같으니 공식 문서를 바꾸는 게 어떻겠냐는 신고가 FastAPI 저장소에 올라온 날은 2024년 6월 28일이다. 문서 예제가 다른 라이브러리로 갈아탔다는 공지가 그 스레드에 붙은 날은 2025년 9월 30일이다.[^10-4]

세 날짜를 나란히 놓고 잠시 멈춰보자. 그 사이의 어느 날, 공식 문서를 그대로 따라 로그인 기능을 만든 사람이 있다. 그 사람의 코드는 무엇으로 비밀번호를 해싱하고 있었을까.

인증 이야기를 꺼내면 먼저 떠오르는 건 부재다. 요청 앞을 지키는 필터 사슬이 없고, 메서드 위에 한 줄로 붙이던 권한 애너테이션이 없다. 그런데 직접 조립의 청구서는 그런 부재 옆으로 오지 않는다. 위의 날짜들처럼, 한참 뒤에 시간 단위로 날아온다.

## 프레임워크가 주는 것의 정확한 크기

먼저 FastAPI가 인증에 대해 무엇을 주는지 재보자. `fastapi.security` 아래에는 스킴 클래스들이 있고, 가장 자주 쓰이는 것이 `OAuth2PasswordBearer`다.[^10-1] 이름이 거창해서 이 물건이 인증을 해주는 것처럼 보이는데, 실제로 하는 일은 셋이다. 요청 헤더에서 Bearer 토큰 문자열을 꺼내 넘겨주고, 토큰이 없으면 401을 돌려주고, `/docs`에 Authorize 버튼을 붙인다.

거기까지다. **그 토큰이 유효한지, 누구의 것인지, 그 사람이 이 이슈를 닫아도 되는지는 이 클래스가 모른다.** 스펙을 표현하고 문서에 노출하는 장치이지 정책 실행기가 아니다.

구조를 대조하면 차이가 분명해진다. 요청이 라우팅에 닿기 전에 필터 사슬을 지나며 인증 주체가 채워지고 접근 규칙이 적용되는 구조에 익숙하다면, 여기엔 그 사슬이 통째로 없다는 것부터 받아들여야 한다. 검사는 경로마다, 또는 라우터마다 붙는 의존성으로 들어온다. 즉 **보안이 앞단의 층이 아니라 경로 함수의 시그니처에 적힌다.** 무엇이 무엇을 요구하는지 설정을 뒤지지 않고 코드에서 읽힌다.

대가도 같은 곳에서 나온다. 기본값이 "막힘"이 아니라 "열림"이다. 새 엔드포인트를 만들며 의존성 한 줄을 빠뜨리면 그 경로는 그냥 공개되고, 아무도 경고해주지 않는다. 그래서 조립 전에 규칙 하나를 정해두는 편이 낫다. **인증이 필요 없는 경로를 예외로 관리한다** — 목록이 짧은 쪽을 세는 것이다.

## 부품의 생사는 누가 지키는가

오프닝의 날짜로 돌아가자. 여기서는 사실과 판단을 구분해 읽어야 한다.

**사실은 이렇다.** `passlib`의 마지막 릴리스는 1.7.4이고 2020년 10월 8일자다. `python-jose`의 마지막 릴리스는 3.5.0이고 2025년 5월 28일자다(둘 다 2026-07 기준). **해석은 여기서 갈린다.** "사실상 방치됐다"는 문장은 릴리스 간격을 근거로 한 판단이지 날짜 자체가 아니다. 나는 그 판단이 타당하다고 보지만 그건 내 판단이고, 확인된 것은 같은 판단을 커뮤니티가 신고로 먼저 했고 문서가 결국 바뀌었다는 기록이다.

기록을 시간표로 펼치면 이렇다.[^10-4]

| 사건 | 최초 제기 | 마무리 | 걸린 시간 |
|---|---|---|---|
| `python-jose` 문서 교체 (#9587) | 2023-05-29 | 2024-05-20 문서가 PyJWT로 변경 | 약 1년 |
| `passlib` 문서 교체 (#11773) | 2024-06-28 | 2025-09-30 pwdlib 전환 공지 | 약 15개월 |
| FastAPI **테스트 스위트**의 `passlib` (#11380) | 2024-03-31 | 2025-05-26 답변(중복 처리) | 약 14개월 |

세 번째 줄이 가장 뼈아프다. 신고 제목이 *"0.110.0: used no longer maintained `passlib` module in test suite"*였다. 문서가 권하던 라이브러리가 프레임워크 자신의 테스트 스위트에도 들어 있었고, 그 신고에 답이 달리기까지 14개월이 걸렸다.

첫 줄도 그냥 지나칠 게 아니다. 공식 템플릿 저장소의 논의(2024-04-29)에 이런 말이 남아 있다.

> "Python-Jose has been abandoned for a while, and now CVEs have been popping up surrounding it and its dependencies."

취약점이 지적된 라이브러리를 공식 문서가 계속 권했고, 정리에 약 1년이 걸렸다. 이게 이 장에서 가장 중요한 문장이다. **그 기간 내내, 공식 문서를 성실하게 따른 코드가 그 라이브러리를 쓰고 있었다.**

여기서 방향을 잘못 잡기 쉽다. 누가 게을렀다는 이야기가 아니다 — 자원이 한정된 오픈소스에서 이 정도 지연은 드문 일도 아니다. 이 기록이 말해주는 건 **조립형 스택에서는 부품의 생사를 감시하는 일이 누군가의 상시 업무가 된다**는 것이고, 그 누군가가 프레임워크 팀이 아니라면 결국 당신이다. 부품을 고를 자유에는 지켜볼 의무가 붙어 오는데, 이 의무는 코드로 나타나지 않아 견적에도 잡히지 않는다.

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

인터넷에 널린 `passlib` + `python-jose` 예제를 그대로 옮기면 방금 본 시간표의 출발점에 다시 서게 된다. 그러니 검색 결과의 코드를 붙여넣기 전에 **그 예제가 쓰는 라이브러리의 마지막 릴리스 날짜를 먼저 보는 습관**을 들이자. 이 장에서 얻어갈 게 하나뿐이라면 그것이다.

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

> "OAuth2 specifies that when using the 'password flow' ... the client/user must send `username` and `password` fields as form data. And the spec says that the fields have to be named like that."

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

from tracker.models.user import User


class UserRepository:
    # ...(2장, 생략)

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

코드는 오늘 다 썼다. 목록은 내일부터 관리하는 것이다.

[^10-1]: 이 장이 쓴 `fastapi.security`·pwdlib·PyJWT 호출 표면 전부(`OAuth2PasswordBearer(tokenUrl=...)`, `OAuth2PasswordRequestForm`(`.username`·`.password`), 응답 형식과 401의 `WWW-Authenticate`, `PasswordHash.recommended()`·`.hash()`·`.verify(plain, hashed)`, `from jwt.exceptions import InvalidTokenError`)와 인용한 축자 셋, `pyjwt[crypto]` 안내 — FastAPI 공식 문서 *OAuth2 with Password (and hashing), Bearer with JWT tokens*(https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) · *Simple OAuth2*(https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/), 조회 2026-07-26. ⚠️ `tokenUrl`의 `"auth/token"`은 문서 값이 아니라 `tracker`의 값이다.

[^10-2]: `from fastapi import Security`·`from fastapi.security import SecurityScopes`, `Security(dependency, scopes=[...])`, `SecurityScopes`의 속성 `scopes`·`scope_str` — FastAPI 공식 문서 *OAuth2 scopes*, https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/ (조회 2026-07-26)

[^10-3]: `jwt.encode(payload, key, algorithm='HS256', ...)`·`jwt.decode(jwt, key='', algorithms=None, options=None, ...)`의 인자 이름, `exp`의 기본 검증과 `ExpiredSignatureError`가 `InvalidTokenError` 아래에 있다는 것 — PyJWT 공식 문서 *API Reference*, https://pyjwt.readthedocs.io/en/stable/api.html (조회 2026-07-26). PyJWT 2.13.0 / 2026-05 기준.

[^10-4]: 시간표의 네 스레드(전부 조회 2026-07-25) — fastapi/fastapi Discussion #9587(2023-05-29 → 2024-05-20 PyJWT로 문서 변경) · #11773(2024-06-28 → 2025-09-30 pwdlib 전환 공지) · #11380 *"0.110.0: used no longer maintained `passlib` module in test suite"*(2024-03-31 → 2025-05-26 답변)은 https://github.com/fastapi/fastapi/discussions/ 아래 각 번호. 인용한 CVE 축자는 fastapi/full-stack-fastapi-template Discussion #1188(SpoonOfDoom, 2024-04-29), https://github.com/fastapi/full-stack-fastapi-template/discussions/1188

[^10-5]: 인용한 antoinewdg의 축자와 "로그인 시 오래된 해시 자동 업그레이드" 언급 — Lobsters, Django vs FastAPI 비교 스레드, https://lobste.rs/s/2jwm1m/django_vs_fastapi_honest_comparison (조회 2026-07-25). **Django와의 비교 맥락에서 나온 말이며 Spring Security 사용자의 전환 경험담이 아니다.**
