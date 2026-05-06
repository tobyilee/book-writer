# 부록 A. 환경 설정 미니 가이드 — pip / conda / venv / uv

노트북을 시작하기 전에 한 가지가 정해져 있어야 한다. **Python 환경을 어떻게 만들 것인가**다. 이 결정이 안 되어 있으면 노트북을 띄우는 첫 분 안에 막힌다. 이 부록은 그 첫 분을 풀어주는 것을 목적으로 한다. 짧다. 결정 가이드 한 장과 즉시 실행 명령 네 줄.

## 왜 환경 분리가 필요한가

같은 일을 두 번 하지 말자. 한 번만 본다. 전역 Python에 `pip install`을 마구 깔다 보면 어느 순간 이런 상황이 온다. 프로젝트 A는 pandas 1.5가 필요하고, 프로젝트 B는 pandas 2.1이 필요하다. 한 시스템에 둘이 동시에 설치될 수 없다. 한 쪽을 설치하면 다른 쪽이 깨진다.

이 충돌이 누적되면 시스템의 Python 환경 자체가 깨져서 어느 프로젝트도 실행되지 않는 상태가 된다. "전역 pip install의 무덤"이라고 부른다. 이 무덤에 들어가지 않으려면 **프로젝트마다 격리된 환경을 만들어 거기에 패키지를 깐다**. 이게 환경 분리다.

방법은 네 가지가 있다. 표준 도구 둘(pip, venv), 과학 패키지 진영의 답(conda), 2024년 이후 부상한 새 도구(uv)다.

## 네 도구 한 줄 요약

- **pip**: Python의 표준 패키지 인스톨러. 환경 격리는 안 한다. venv와 짝으로 쓰는 게 정석.
- **venv**: Python 표준 라이브러리에 내장된 가상환경 도구. `python -m venv` 한 줄로 격리된 환경이 만들어진다.
- **conda**: Anaconda·Miniconda·Miniforge가 제공하는 환경+패키지 관리 도구. Python뿐 아니라 C 라이브러리, CUDA, 시스템 도구까지 다룬다. 과학 계산 분야의 사실상 표준이었다.
- **uv**: 2024년 등장한 Rust 기반 도구. pip·venv·pip-tools·pyenv·pipx의 일을 한 도구로 묶고, 속도가 한 자릿수 배 빠르다.

## 비교표

| 축 | pip | venv | conda | uv |
|----|-----|------|-------|-----|
| **환경 격리** | X (도구 자체로는) | O | O | O |
| **패키지 설치** | O (PyPI) | X (인스톨러 별도) | O (conda 채널 + pip) | O (PyPI, pip 호환) |
| **속도** | 보통 | 보통 | 느림 (의존성 해결 무거움) | 매우 빠름 (10~100배) |
| **C/시스템 바이너리** | 휠로 (제한적) | venv 자체로는 X | 강함 (CUDA, MKL, GDAL 등) | pip 휠로 (제한적) |
| **노트북과의 궁합** | `pip install jupyterlab` | `python -m venv .venv` 후 pip | `conda install jupyterlab` | `uv tool install jupyterlab` |
| **언제 쓸지** | 항상 (다른 도구의 기반) | 표준 격리, 단순한 Python 프로젝트 | 과학 계산·CUDA·다언어 패키지 | 새 프로젝트, 속도 중요할 때 |
| **학습 곡선** | 낮음 | 낮음 | 중간 (channel·environment.yml 개념) | 낮음 (pip와 거의 같음) |

## 결정 가이드

복잡한 의사결정 트리는 만들지 않는다. 다음 네 줄로 충분하다.

1. **그냥 빨리 시작하고 싶다** → `pip install jupyterlab`. 단, 시스템 Python에는 깔지 말고 venv 안에서.
2. **단순한 Python 프로젝트, 패키지가 다 PyPI에 있다** → `venv` + `pip`. 표준 도구의 짝.
3. **CUDA, GDAL, R 커널, MKL BLAS 같은 시스템·바이너리 의존이 있다** → `conda` (Miniforge 권장).
4. **새 프로젝트를 시작하고, 속도와 깔끔함을 원한다** → `uv`. 2026년 시점에서 가장 추천할 만한 새 도구.

기존 conda 환경을 잘 쓰고 있다면 그대로 쓰면 된다. 갈아탈 이유는 없다. 새 시작이라면 uv를 시도해 보고, 시스템 패키지 충돌이 보이면 그때 conda로 옮기면 된다.

## 즉시 실행 명령 네 종

JupyterLab을 띄우는 가장 빠른 한 줄을 네 도구별로 정리한다. 어느 길로 가든 결과는 같다 — 브라우저에서 JupyterLab이 열린다.

### 1. pip (전역 설치 — 권장하지 않지만 가장 짧다)

```bash
pip install jupyterlab
jupyter lab
```

빠른 시도용. 시스템 Python에 직접 깔리니 다른 프로젝트와 충돌할 수 있다. 학습용으로만.

### 2. venv (표준 격리)

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install jupyterlab
jupyter lab
```

표준 도구의 짝. `python -m venv .venv`로 현재 폴더에 `.venv/`라는 격리된 환경이 만들어지고, `source .venv/bin/activate`로 그 환경에 들어간다. 활성화된 상태에서 `pip install`은 시스템이 아니라 그 환경 안에 설치된다.

작업이 끝나면 `deactivate` 한 줄로 빠져나온다. 환경을 통째로 지우고 싶으면 `.venv` 폴더를 지우면 된다.

### 3. conda

```bash
conda create -n nb jupyterlab -c conda-forge
conda activate nb
jupyter lab
```

`-c conda-forge`로 conda-forge 채널을 지정하는 편이 낫다. Anaconda 기본 채널보다 패키지가 풍부하고 최신이다(Miniforge를 쓰면 자동으로 conda-forge가 기본).

`conda create`가 만든 환경은 시스템 어디에서나 `conda activate nb` 한 줄로 들어갈 수 있다. venv처럼 폴더 안에 격리되는 게 아니라 시스템 차원에서 환경 이름으로 관리된다.

CUDA 같은 무거운 의존이 필요하면:

```bash
conda create -n ml jupyterlab pytorch pytorch-cuda=12.1 -c pytorch -c nvidia
```

이 한 줄에 CUDA 호환 PyTorch까지 한 번에 설치된다. 이게 conda의 진짜 강점이다.

### 4. uv

```bash
uv tool install jupyterlab
jupyter lab
```

가장 짧다. `uv tool install`은 도구 단위 격리 설치다. JupyterLab을 시스템 어디에서나 `jupyter lab`으로 띄울 수 있게 자동 처리해준다.

프로젝트 단위로 격리하고 싶으면:

```bash
uv init my-project
cd my-project
uv add jupyterlab
uv run jupyter lab
```

`uv init`이 `pyproject.toml`과 lockfile을 자동 생성하고, `uv add`가 패키지를 추가하면서 lockfile을 갱신한다. `uv run`은 그 환경에서 명령을 실행한다. 활성화·비활성화 같은 단계 없이 동작한다는 점이 venv·conda와 다르다.

설치 속도가 venv+pip보다 한 자릿수 배 빠르다. 큰 프로젝트일수록 차이가 두드러진다.

## 패키지 매니페스트 — `requirements.txt` / `environment.yml` / `pyproject.toml`

격리된 환경을 만들었으면, 그 환경에 어떤 패키지가 어떤 버전으로 깔려 있는지를 파일에 기록해야 한다. 그래야 다른 사람이, 또는 6개월 뒤의 자기 자신이 같은 환경을 재현할 수 있다.

세 가지 포맷이 있다.

**`requirements.txt`** — pip의 표준. 한 줄에 한 패키지.

```
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
jupyterlab==4.0.9
```

생성: `pip freeze > requirements.txt`. 재현: `pip install -r requirements.txt`. 가장 단순하고 호환성이 넓다.

**`environment.yml`** — conda의 표준. YAML 포맷이고 conda 채널과 pip 패키지를 함께 적을 수 있다.

```yaml
name: nb
channels:
  - conda-forge
dependencies:
  - python=3.11
  - jupyterlab=4.0
  - pandas=2.1
  - pip
  - pip:
      - some-pip-only-package
```

생성: `conda env export > environment.yml`. 재현: `conda env create -f environment.yml`.

**`pyproject.toml`** — Python 표준(PEP 518/621)의 통합 매니페스트. 빌드 설정, 의존성, 도구 설정이 한 파일에 들어간다. uv·poetry·hatch가 이 포맷을 쓴다.

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "jupyterlab>=4.0",
    "pandas>=2.1",
    "scikit-learn>=1.3",
]
```

uv를 쓴다면 `uv add` 명령이 이 파일을 자동으로 갱신한다. 그리고 `uv.lock` 파일이 정확한 버전을 못박아 둔다(npm·cargo의 lockfile과 같은 개념).

새 프로젝트라면 `pyproject.toml` + lockfile이 가장 깔끔하다. 기존 conda 프로젝트라면 `environment.yml`을 유지하면 된다. 가장 단순한 케이스라면 `requirements.txt`로도 충분하다.

## 노트북 안에서 환경 점검

노트북을 띄웠는데 어느 환경에서 돌고 있는지 헷갈릴 때가 있다. 특히 시스템에 여러 환경이 있고, JupyterLab은 base 환경에서 띄우고 노트북은 다른 커널을 쓰는 경우. 다음 셀들을 한 번씩 돌려보자.

```python
# 현재 노트북이 쓰는 Python 인터프리터의 경로
import sys
print(sys.executable)

# pip가 어디 깔려 있는지
!which pip       # macOS/Linux
!where pip       # Windows

# Python 버전
!python --version

# 현재 환경의 패키지 목록 (커널이 보는 환경 기준)
%pip list
```

여기서 마지막 줄의 `%pip`가 중요하다. **노트북에서 패키지를 설치할 때는 `!pip install`이 아니라 `%pip install`을 쓰는 편이 낫다.** 차이는 이렇다.

- `!pip install pandas`는 셸의 pip을 호출한다. 그 pip이 노트북 커널과 같은 환경의 것인지 보장이 없다. 다른 환경에 설치되고 노트북에서는 안 보이는 사고가 자주 난다.
- `%pip install pandas`는 IPython의 매직이다. **현재 커널의 환경에 정확히 설치한다.** 사고가 안 난다.

이 한 줄 차이가 노트북 환경 트러블슈팅의 30%를 줄여준다.

## 다섯 줄 요약

- 시스템 Python에 직접 패키지를 깔지 말자. venv든 conda든 uv든, 격리된 환경 안으로 들어가자.
- 새 프로젝트는 uv로 시작해보자. `uv init` + `uv add` + `uv run` 세 명령이면 충분하다.
- 시스템 라이브러리·CUDA·R 커널이 필요하면 conda(Miniforge)가 답.
- 패키지 매니페스트(`requirements.txt`/`environment.yml`/`pyproject.toml`)를 git에 커밋하자. 6개월 뒤 자기 자신에게 보내는 가장 큰 선물이다.
- 노트북 안에서는 `!pip` 대신 `%pip`. 커널 환경에 정확히 설치된다.

이 다섯 줄이 잡혀 있으면 4·5·6·7·8장 어느 환경으로 가더라도 첫 분에 막히지 않는다. 본문 어디에서 "환경 설정에서 막혔다"는 느낌이 들면 이 부록으로 한 번 돌아오면 된다.
