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
