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
