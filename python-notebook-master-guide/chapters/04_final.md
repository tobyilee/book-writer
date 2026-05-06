# 4장. Jupyter와 JupyterLab — 표준을 깊이 이해하기

처음 노트북을 깔아보려고 검색해보면 화면이 어지럽다. Jupyter Notebook, JupyterLab, Jupyter Server, JupyterHub, BinderHub. 이름이 다 비슷한데 정체가 다 다른 것 같다. 어떤 글은 "이제 JupyterLab이 표준"이라고 하고, 어떤 글은 "그래도 클래식 Notebook이 가볍다"고 한다. 또 어떤 회사 매뉴얼에는 "JupyterHub에 로그인하세요"라고만 적혀 있다. 어디서부터 풀어야 할까.

이 다섯이 사실은 한 가족이다. 한 장의 가계도로 묶으면 머리에 정리가 된다. 같이 그려보자. 다 그리고 나면 자기 컴퓨터에서 첫 노트북을 띄우는 가장 빠른 한 줄까지 손에 들어온다.

## 0단계 — 가장 빠른 한 줄

깊게 들어가기 전에 일단 띄워보자. 노트북에 손이 가야 책이 살아 움직인다.

```bash
pip install jupyterlab
jupyter lab
```

이 두 줄이면 브라우저가 열리고 JupyterLab이 뜬다. 끝이다.

조금 더 깔끔하게 환경을 분리하고 싶다면, 또는 시스템 파이썬을 건드리기 싫다면 다음 중 하나를 고르자. 어느 방식이 자기에게 맞을지는 부록 A에서 따져두었다. 처음이면 venv 또는 uv가 무난하다. 데이터 사이언스에 익숙해지면 conda의 환경 관리가 강력해진다.

```bash
# venv 격리
python -m venv .venv
source .venv/bin/activate
pip install jupyterlab
jupyter lab

# uv (2024년부터 떠오른 Rust 기반 도구, 빠르다)
uv tool install jupyterlab
uvx jupyter lab

# conda (과학 패키지·바이너리 통합 환경이 필요하면)
conda create -n nb -c conda-forge jupyterlab
conda activate nb
jupyter lab
```

네 가지 중 어느 걸 고르든 이 장의 나머지 내용을 따라가는 데 지장 없다. 환경 분리의 큰 그림(왜 격리해야 하나, requirements는 어떻게 핀하나)은 부록 A에 따로 정리해뒀다. 노트북에 첫발을 디딘 단계에선 위 한 줄로 충분하다.

명령을 치고 엔터를 누르면 터미널에 이런 메시지가 흐른다.

```
[I 2026-05-06 14:22:10.123 ServerApp] jupyter_server_terminals | extension was successfully linked.
[I 2026-05-06 14:22:10.456 ServerApp] Serving notebooks from local directory: /Users/toby/work
[I 2026-05-06 14:22:10.456 ServerApp] Jupyter Server 2.x is running at:
[I 2026-05-06 14:22:10.456 ServerApp] http://localhost:8888/lab?token=4c3a2b1d...
```

브라우저가 자동으로 열린다. 안 열리면 그 URL을 복사해서 직접 붙여 넣으면 된다. 이제 JupyterLab의 좌측 사이드바와 가운데 빈 작업 영역이 보일 것이다. 우측 상단 New Launcher → Python 3 (ipykernel)을 누르면 첫 노트북이 뜬다. 첫 셀에 `print("hello")`를 치고 `Shift+Enter`. 잘 뜨면 성공이다.

이 첫 화면 안에 사실은 세 컴포넌트가 동시에 돌고 있다. 브라우저의 JupyterLab 프런트엔드, 그 뒤의 Jupyter Server, 그리고 Server가 띄워준 Python 커널. 2장에서 본 두 프로세스 구조에 한 층이 더 붙은 셈이다. Server는 프런트엔드와 커널 사이에서 라우팅·인증·파일 관리·여러 노트북 동시 띄우기를 담당한다. 한 컴퓨터에서 노트북 다섯 개를 동시에 열어두면 Server 하나에 커널 다섯 개가 붙어 있다. 이걸 가계도로 정리해보자.

## 가계도 — 다섯 컴포넌트의 관계

```
                ┌──────────────────────────────┐
                │     [프런트엔드 (UI)]        │
                │                              │
                │  Jupyter Notebook (v6/v7)    │
                │  JupyterLab                  │
                │  VS Code · Cursor · 기타      │
                └──────────────┬───────────────┘
                               │ HTTP + WebSocket
                               ▼
                ┌──────────────────────────────┐
                │      Jupyter Server          │
                │  (REST API + 커널 매니저)     │
                └──────────────┬───────────────┘
                               │ ZeroMQ 5채널
                               ▼
                ┌──────────────────────────────┐
                │   커널 (Python / R / Julia)   │
                └──────────────────────────────┘

  ┌──── 다중 사용자가 필요하면 ──────────────────┐
  │                                                │
  │  JupyterHub                                    │
  │   ↓ spawn                                      │
  │   사용자별 Jupyter Server 인스턴스            │
  │                                                │
  └────────────────────────────────────────────────┘

  ┌──── "Git repo 한 클릭 실행" 만들고 싶으면 ────┐
  │                                                │
  │  BinderHub                                     │
  │   ↓ build                                      │
  │   Docker 이미지 → 일회성 JupyterHub            │
  │                                                │
  └────────────────────────────────────────────────┘
```

다섯 이름을 한 줄씩 정리하자.

- **Jupyter Notebook**: 가장 오래된 프런트엔드 UI. 단일 문서·단일 탭의 가벼운 화면.
- **JupyterLab**: 프런트엔드 UI의 다음 세대. IDE처럼 사이드바·터미널·여러 탭을 한 화면에 띄움.
- **Jupyter Server**: 위 두 UI가 공통으로 쓰는 백엔드. 커널을 관리하고 파일 시스템을 노출하는 REST + WebSocket 서버.
- **JupyterHub**: 다중 사용자를 위한 상위 계층. 사용자별로 Jupyter Server를 한 개씩 띄워준다.
- **BinderHub**: "git repo → Docker 이미지 → 일회성 JupyterHub"를 자동화하는 인프라.

이 다섯이 노트북 표준 생태계의 전부다. 다른 환경(Colab, VS Code, Marimo 등)은 이 그림 위 어딘가에 자기 위치를 잡는다. Colab은 위쪽 프런트엔드를 자체 UI로 갈아 끼우고 백엔드는 구글이 운영. VS Code는 프런트엔드를 에디터 안에 넣고 그 뒤의 Server는 자체로 띄움. Marimo는 이 그림 자체를 거부하고 새로 짠다 — 7장에서 본다.

자, 이제 한 컴포넌트씩 손에 잡아가자.

## Jupyter Notebook — v6, v7, 그리고 nbclassic의 현재(2026 기준)

처음 노트북을 만난 사람의 머릿속에 떠오르는 그 화면 — 단일 탭 안에 셀이 죽 늘어선 미니멀한 UI — 이게 클래식 Jupyter Notebook이다. 2011년쯤부터 십수 년 동안 표준이었고, fast.ai 강의도 Hugging Face 튜토리얼도 다 이 화면이었다.

지금 시점(2026년 기준)에 정리해두자.

**Jupyter Notebook v6 (legacy)**: 클래식 코드 베이스. 더 이상 새 기능이 추가되지 않고, 보안 패치 위주의 유지 모드. `pip install notebook` 옛날 버전을 깔거나 의존성으로 따라오면 만난다.

**Jupyter Notebook v7**: 같은 미니멀 UI를 그대로 유지하면서, 내부 코드 베이스를 **JupyterLab의 컴포넌트 위에 올린** 재구현이다. 화면은 옛날처럼 단순한데, 그 아래 엔진은 JupyterLab과 같은 모듈을 공유한다. v7부터는 JupyterLab과 같은 확장을 쓸 수 있고, 보안·접근성도 같이 개선된다.

**nbclassic**: v7로 옮기는 과정에서 옛날 v6 UI를 그리워하는 사용자를 위한 호환 레이어. `pip install nbclassic`을 깔면 옛날 화면을 v7 환경에서도 띄울 수 있다.

가벼운 화면이 좋고 확장이 필요 없다면 Notebook v7으로 충분하다. 사이드바에 파일 탐색기, 터미널, 디버거를 같이 띄우고 싶다면 JupyterLab으로 가자. 두 명령어가 한 컴퓨터에 동시에 깔려 있어도 충돌 없다.

```bash
jupyter notebook   # 클래식 UI (v7 코드 베이스)
jupyter lab        # IDE형 UI
```

같은 `.ipynb` 파일이라 어느 쪽으로 열든 동일하게 읽고 쓴다. 둘 다 깔아두고 작업 종류에 따라 골라 쓰는 사람이 많다.

JupyterLab을 깔면 Notebook v7도 자동으로 같이 깔린다. `pip install jupyterlab` 한 번이면 두 명령어가 모두 동작한다. 따로 신경 쓸 필요 없다.

또 하나 — 인터넷에서 옛날 자료를 따라 하다 보면 `jupyter-notebook` (하이픈)이나 `ipython notebook`(IPython 시절 명령) 같은 옛 명령을 만날 수 있다. 다 사라진 지 오래다. 지금은 `jupyter notebook`(공백)과 `jupyter lab`이 표준이다. 옛 자료를 그대로 따라하다가 명령이 안 먹어 당황할 때가 있다.

## JupyterLab — IDE형 노트북 환경

JupyterLab은 2018년쯤 정식 출시된 다음 세대 프런트엔드다. 한마디로 "노트북을 IDE처럼 쓰자"는 답이다. 화면을 한 번 보면 차이가 분명하다.

```
┌─────────────────────────────────────────────────────┐
│ File Edit View Run Kernel Tabs Settings Help        │
├──┬────────────┬─────────────────────────────────────┤
│📁│ files      │ ┌───────┬───────┬─────────────────┐ │
│  │ ▸ data/    │ │eda.ipynb│utils.py│Terminal       │ │
│  │ ▸ notebooks│ ├─────────────────────────────────┤ │
│  │  eda.ipynb │ │ # 셀 1                          │ │
│⚙│  utils.py  │ │ import pandas as pd             │ │
│  │            │ │                                 │ │
│🐛│            │ │ # 셀 2                          │ │
│  │            │ │ df = pd.read_csv("sales.csv")   │ │
│  │            │ │ df.head()                       │ │
│⌨│            │ │                                 │ │
│  │            │ │ ┌───────────────────────────┐   │ │
│  │            │ │ │ id │ amount │ date       │   │ │
│  │            │ │ │ 1  │ 1000   │ 2026-05-01 │   │ │
│  │            │ │ └───────────────────────────┘   │ │
│  │            │ └─────────────────────────────────┘ │
└──┴────────────┴─────────────────────────────────────┘
```

좌측에 사이드바가 있고, 가운데가 작업 영역이다. 작업 영역엔 노트북, 파이썬 파일, 터미널, 마크다운, CSV — 종류 가리지 않고 탭으로 띄울 수 있다. 화면을 분할해 나란히 띄우는 것도 가능하다. 한 쪽엔 노트북, 다른 쪽엔 그 노트북이 임포트하는 `utils.py`를 띄워두고 양쪽을 오가며 작업하는 패턴이 자연스럽다.

JupyterLab이 클래식 Notebook 위에 얹은 핵심 기능을 짚어보자.

### 사이드바 — 파일·실행·확장

좌측의 작은 아이콘들이 사이드바 패널이다.

- **File Browser** (📁): 파일 시스템 탐색. 숨김 파일까지 한 번에 본다.
- **Running** (▶): 현재 떠 있는 커널과 터미널 목록. 메모리 잡고 있는 노트북이 한눈에 보인다. 종료도 여기서.
- **Commands** (⌨): 모든 명령어를 키워드 검색. `Ctrl+Shift+C`가 단축키.
- **Property Inspector**: 셀 메타데이터 보기. 태그(parameters 등) 다는 데 쓴다.
- **Extension Manager** (⚙): 확장 검색·설치.

특히 Commands 패널은 단축키를 모를 때 정말 유용하다. "save"라고 치면 관련 명령이 뜨고, "Run All"이라고 치면 전체 실행 명령이 뜬다. VS Code의 Command Palette와 거의 같은 사용감이다.

### 통합 터미널

`File → New → Terminal`을 누르면 작업 영역 안에 셸이 뜬다. JupyterLab을 띄운 같은 디렉토리에서 시작하니까 노트북과 같은 폴더를 다룬다. `git status`, `pip install`, `cat data/sales.csv | head` 같은 셸 작업을 같은 화면에서 할 수 있다.

3장에서 본 `!ls`, `%%bash` 매직과 함께 쓰면 셸과 노트북의 경계가 거의 사라진다. 큰 작업은 터미널에서, 빠른 명령은 셀 안에서 — 자기 손에 맞는 패턴을 찾으면 된다.

### 디버거

`Debug` 버튼(좌측 사이드바의 🐛)을 활성화하면 셀 옆 줄 번호 옆에 빨간 점을 찍어 브레이크포인트를 걸 수 있다.

```python
def process(items):
    total = 0
    for item in items:        # ← 여기 줄에 빨간 점
        total += item * 2
    return total

result = process([1, 2, 3, 4, 5])
```

이 셀을 실행하면 브레이크포인트에서 멈추고, 우측에 변수 값과 콜 스택이 뜬다. `pdb`를 셀 안에서 띄우는 옛날 방법보다 시각적으로 훨씬 편하다.

### LSP 자동완성

`jupyterlab-lsp` 확장을 깔면 코드 자동완성이 IDE 수준으로 올라온다. 함수 시그니처, 정의로 이동, 타입 힌트 — 다 동작한다. Python 외에도 R, Julia 등 LSP 서버가 있는 언어는 다 지원.

```bash
pip install jupyterlab-lsp 'python-lsp-server[all]'
```

설치만 하면 자동으로 활성화된다. `def `를 치다가 멈추면 시그니처 힌트가 뜨고, 함수 이름 위에 마우스를 올리면 docstring이 뜬다. JupyterLab을 진지하게 쓸 거면 거의 필수에 가까운 확장이다.

### Git 통합

`jupyterlab-git` 확장은 좌측 사이드바에 git 패널을 추가한다. 브랜치 보기, diff 보기, 커밋, 푸시 — VS Code의 git 패널과 거의 같은 인터페이스로 동작한다.

```bash
pip install jupyterlab-git
```

다만 `.ipynb`의 git diff 문제는 여전히 있다 — JSON 직렬화이기 때문에 출력이 바뀌면 base64 이미지 데이터가 통째로 바뀐다. 이건 JupyterLab Git 확장이 아니라 Jupytext나 nbdime을 도입해 해결할 영역이다(10장).

### 변수 탐색기 확장

`jupyterlab-variableinspector` 확장을 깔면 우측에 변수 탐색 패널이 뜬다. 현재 메모리에 있는 모든 변수의 이름, 타입, 크기, 값 미리보기를 한눈에 본다.

```bash
pip install lckr-jupyterlab-variableinspector
```

3장에서 본 `%whos` 매직과 같은 정보를 GUI로 보여주는 것이다. 큰 노트북에서 hidden state 점검에 유용하다. VS Code Notebooks의 변수 탐색기와 같은 사용감을 얻을 수 있다.

### 정리하자면

JupyterLab의 차별점은 **한 화면에 작업이 다 모인다**는 것이다. 클래식 Notebook이 한 노트북에 집중하는 미니멀한 매체였다면, JupyterLab은 데이터 작업 환경 전체다. 노트북 + 에디터 + 터미널 + 디버거 + git이 한 곳에 있다.

그래서 "JupyterLab이 너무 무겁다, 클래식이 가볍고 좋다"는 의견도 여전히 있다. 일리가 있다. 짧은 일회성 노트북이라면 클래식 v7으로 충분하고, 긴 프로젝트라면 JupyterLab의 통합이 빛난다. 작업 성격에 맞춰 고르자.

확장 생태계도 짚어둘 가치가 있다. JupyterLab Extension Manager에서 검색하면 수백 개의 확장이 뜬다. 자주 쓰는 것들 — 위에서 말한 LSP, Git, Variable Inspector 외에 — 몇 개 더 추천해두자.

- **jupyterlab-toc**: 마크다운 헤딩 기반 목차를 좌측 사이드바에 자동 생성. 긴 노트북 탐색에 좋다.
- **jupyterlab-execute-time**: 셀 옆에 마지막 실행 시간을 표시. 어떤 셀이 오래 걸리는지 한눈에.
- **jupyter-resource-usage**: 우측 상단에 메모리·CPU 사용량 실시간 표시. 큰 데이터 다룰 때 유용.
- **jupyterlab-system-monitor**: 위와 비슷하지만 더 정교한 그래프.

이런 확장은 처음 노트북 시작할 때 다 깔 필요는 없다. 작업하다 "이게 있으면 좋겠는데" 싶을 때 그때 찾아 깔면 된다. 단, LSP와 Git, Jupytext 정도는 처음부터 깔아두는 편이 낫다 — 나중에 후회하지 않는다.

## Jupyter Server — 보이지 않는 백엔드

JupyterLab을 띄우면 그 뒤에서 Jupyter Server가 도는데, 이건 보통 직접 만질 일이 없다. 그래도 알아두면 좋다. 이게 뭐냐면 — 프런트엔드(브라우저)에서 들어오는 HTTP 요청을 받아 커널을 띄워주고, 파일을 읽고 쓰고, 노트북 상태를 관리하는 REST + WebSocket 서버다.

`jupyter lab`을 치면 사실 이 순서다.

```
1. Jupyter Server 프로세스 띄움 (포트 8888)
2. JupyterLab 프런트엔드를 정적 파일로 서빙
3. 브라우저가 그 정적 파일을 받아 화면 그림
4. 브라우저 ↔ Server 사이에 WebSocket 연결
5. 노트북 만들면 Server가 커널 프로세스 띄움
6. 셀 실행 메시지가 Server를 거쳐 커널로 흐름
```

직접 만질 일이 생기는 두 시점이 있다.

**원격에서 노트북 띄울 때.** 클라우드 VM이나 회사 서버에서 JupyterLab을 띄우고 자기 노트북에서 접속하고 싶을 때. 기본 설정은 localhost에만 응답하므로 외부 접속을 허용해야 한다.

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
```

`--no-browser`는 서버에 브라우저가 없으니까 자동으로 띄우려 시도하지 말라는 뜻. 출력에 `?token=...`이 박힌 URL이 뜨고, 그걸 자기 컴퓨터 브라우저에 붙여 넣으면 접속된다. SSH 터널 통해 보안을 더하는 패턴도 흔하다.

```bash
ssh -L 8888:localhost:8888 user@server
# 그다음 server에서 jupyter lab 띄우고
# 로컬 브라우저에서 http://localhost:8888 접속
```

**JupyterHub로 다중 사용자 띄울 때.** 이게 다음 절의 주제다.

기본 사용엔 Jupyter Server를 의식할 필요 없다. 이 컴포넌트가 따로 존재한다는 사실만 머리에 두자.

## JupyterHub — 다중 사용자를 위한 그릇

JupyterHub는 한마디로 "여러 사람에게 각자의 Jupyter Server를 띄워주는 게이트웨이"다. 강의실, 연구실, 회사 데이터팀 — 사용자가 여럿일 때 쓴다.

큰 그림은 이렇다.

```
사용자 A 브라우저 ─┐
사용자 B 브라우저 ─┤        ┌──────────────┐
사용자 C 브라우저 ─┼──HTTP──▶│ JupyterHub   │
                  │        │ (게이트웨이)  │
                  └────────▶└──┬───────────┘
                                │ spawn (사용자별)
                                ▼
                  ┌────────────────────────────┐
                  │ A의 Jupyter Server         │
                  │ B의 Jupyter Server         │
                  │ C의 Jupyter Server         │
                  └────────────────────────────┘
```

학생이 강의 페이지에서 로그인하면 JupyterHub가 그 학생만의 Jupyter Server를 spawn한다. 같은 강의실의 다른 학생이 로그인하면 그 학생만의 Server가 또 따로 뜬다. 서로 메모리·파일이 격리되니까 한 학생의 무한 루프가 다른 학생을 망치지 않는다.

JupyterHub 배포 패턴은 두 가지가 표준이다.

### Zero to JupyterHub on Kubernetes (Z2JH)

Kubernetes 클러스터 위에 JupyterHub를 배포하는 공식 가이드. 사용자가 늘면 알아서 노드를 추가하고, 사용자가 노트북을 띄우면 새 Pod이 spawn된다. 대학 강의실(수백 명), 회사 데이터팀(수십~수백 명) 규모에서 쓴다.

Helm 차트 한 번 깔면 기본 동작한다.

```bash
helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
helm install jhub jupyterhub/jupyterhub --version=3.0.0 -f config.yaml
```

`config.yaml`에 사용자 인증 방식(GitHub OAuth, LDAP, Google 등), 사용자별 자원 한도, 공유 데이터셋 마운트, 사용자 정의 Docker 이미지 등을 설정한다. 인프라 깊이가 필요한 작업이라 운영자가 따로 있는 게 보통.

자세한 배포는 [공식 문서 Zero to JupyterHub](https://zero-to-jupyterhub.readthedocs.io/)를 참고하자.

대학 캠퍼스 강의나 회사 데이터팀 도입 사례는 jupyter.org의 Case Studies 섹션에 모여 있다. UC Berkeley의 데이터 사이언스 입문 강의 DS100은 학생 수천 명에게 JupyterHub로 노트북을 띄워주는 대표 사례로 자주 인용된다.

### The Littlest JupyterHub (TLJH)

단일 VM 위에 JupyterHub를 띄우는 가벼운 배포 방식. 사용자가 100명 이하 정도면 충분히 굴러간다. 강사가 단독 강의실용으로 띄워두기 좋다.

```bash
curl -L https://tljh.jupyter.org/bootstrap.py | sudo python3 - --admin <admin-username>
```

한 줄로 끝난다. 그다음 `<server-ip>` 접속하면 JupyterHub 로그인 페이지가 뜬다. 사용자 추가는 admin 계정으로 들어가서 웹 UI에서 한다.

Kubernetes 운영 부담이 없으니까 학교 컴퓨터 한 대에 띄워두는 용도로 좋다. [tljh.jupyter.org](https://tljh.jupyter.org/) 참고.

### 보안 박스 — 멀티테넌트 환경의 위험

> **이 책의 범위 밖.** JupyterHub로 다중 사용자 환경을 운영한다는 건 보안 책임을 떠안는다는 뜻이다. 토큰 관리, 사용자 간 네트워크 격리, 컨테이너 탈출 가능성, 악의적 사용자가 다른 사용자의 노트북에 접근할 수 있는 경로 — 이런 주제는 인프라/보안 책의 영역이다. 이 책은 노트북 사용자의 시선에서 쓰였으므로 깊이 다루지 않는다.
>
> 다중 사용자 환경을 직접 운영해야 한다면 다음 1차 자료를 시작점으로 권장한다.
>
> - [JupyterHub Security Documentation](https://jupyterhub.readthedocs.io/en/stable/explanation/security.html)
> - [Zero to JupyterHub: Security](https://z2jh.jupyter.org/en/stable/administrator/security.html)
> - [Project Jupyter Security Advisories](https://github.com/jupyter/jupyter-security)
>
> 일단 시작은 단일 사용자 모드(자기 컴퓨터에서 `jupyter lab`)로 충분하다. 다중 사용자가 필요한 시점에 별도 학습이 필요한 영역으로 알아두자.

## BinderHub — "이 링크 누르면 바로 실행" 만들기

가끔 GitHub의 어떤 노트북 README 위쪽에 이런 배지가 박힌 걸 본다.

```
[ launch | binder ]
```

누르면 새 탭이 열리고 잠시 로딩이 흐른 뒤 그 노트북이 자기 환경에서 실행 중인 JupyterLab으로 뜬다. 설치도, 데이터 다운로드도, 환경 설정도 없이.

이게 BinderHub다. 한마디로 "Git repo → Docker 이미지 → 일회성 JupyterHub"의 자동화 인프라다. 흐름은 이렇다.

```
1. 사용자가 Binder 배지 누름
2. BinderHub가 GitHub repo 클론
3. requirements.txt / environment.yml / Dockerfile 등 환경 파일 읽음
4. repo2docker가 Docker 이미지 빌드 (캐시 있으면 스킵)
5. 일회성 JupyterHub spawn → 사용자에게 URL 전달
6. 사용자 세션 끝나면 컨테이너 삭제
```

사용자 시점에선 그냥 "한 번 누르고 들어간다"이고, 운영 시점에선 "사용자에게 환경 세팅 요구하지 않고 노트북을 공유한다"이다.

### 자기 repo에 Binder 배지 만들기

생각보다 쉽다. 세 단계.

**1단계.** GitHub repo에 노트북과 환경 파일을 둔다. `requirements.txt` 한 줄이면 충분하다.

```
my-notebook-repo/
├── analysis.ipynb
└── requirements.txt
```

`requirements.txt` 내용 예시:

```
pandas==2.2.0
matplotlib==3.8.2
scikit-learn==1.4.0
```

**2단계.** [mybinder.org](https://mybinder.org/)에 접속한다. GitHub 주소를 입력하고 브랜치(보통 `main` 또는 `HEAD`)를 지정한다.

**3단계.** 페이지 아래쪽에 자동 생성된 마크다운 배지를 복사한다.

```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<user>/<repo>/HEAD)
```

이걸 README.md에 붙이면 끝이다. 첫 클릭 시 Docker 이미지를 빌드하느라 1~2분 걸리지만, 한 번 빌드되면 캐시되어 다음 사용자는 거의 즉시 시작한다.

특정 노트북을 바로 띄우게 하고 싶으면 URL 끝에 노트북 경로를 붙인다.

```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<user>/<repo>/HEAD?labpath=analysis.ipynb)
```

`?labpath=analysis.ipynb`가 사용자를 그 노트북으로 직접 데려간다. 강의 자료에서 "1주차 노트북 바로 열기"처럼 자료별 링크를 따로 박을 수 있다.

복잡한 환경(C 라이브러리, GPU 미지원, 시스템 패키지 등)이 필요하면 `apt.txt`로 시스템 패키지를, `Dockerfile`로 완전 커스텀 환경을 정의할 수 있다. repo2docker 공식 문서가 인식하는 설정 파일 목록을 정리해두고 있다.

자기 회사용 BinderHub를 띄우는 것도 가능하다(GitHub의 Binder 인스턴스가 있으면 사용량 제한 없이 쓸 수 있다). 자세한 건 [binderhub.readthedocs.io](https://binderhub.readthedocs.io/) 참고.

### 누가 쓰면 좋은가

- **강의 자료 공유.** 학생에게 "이 링크 클릭해서 노트북 따라 치세요"라고 한 줄 적어 보내면 끝. 환경 설치로 첫날을 다 보내지 않아도 된다.
- **재현성 있는 논문 코드.** 논문 코드 repo에 Binder 배지를 박아두면 리뷰어와 후속 연구자가 즉시 실행해본다. fast.ai와 jupyter book이 자주 쓰는 패턴.
- **데모 링크.** 새로 만든 라이브러리의 사용 예제를 노트북으로 만들어 Binder 배지로 공유. README가 살아 움직이는 데모가 된다.

쓰지 말아야 할 곳도 있다. 큰 데이터셋을 다루는 노트북, GPU가 필요한 학습 코드, 시크릿이 필요한 워크플로우 — 이런 건 Binder가 적절하지 않다. mybinder.org는 무료 공용 리소스라 자원 한도가 빡빡하다. GPU 학습은 Colab이나 Kaggle로(5장), 큰 데이터는 자체 인프라로 가는 게 맞다.

## 철학 — 모든 언어, 모든 워크플로우를 위한 표준

여기까지 만난 다섯 컴포넌트의 공통 디자인 철학을 한 줄로 짚어보자.

> *"노트북은 어떤 한 언어, 어떤 한 워크플로우에 묶여서는 안 된다. 어떤 사용자, 어떤 환경, 어떤 규모에서도 같은 매체로 동작해야 한다."*

이 철학이 모든 결정에 깔려 있다.

- **언어 독립:** 커널 인터페이스를 표준화해 Python, R, Julia, Scala, JavaScript, Bash까지 같은 UI로 다룰 수 있게.
- **프런트엔드 독립:** 같은 `.ipynb` 파일을 클래식 Notebook, JupyterLab, VS Code, Cursor — 어디서 열든 같게 동작.
- **확장 가능:** 핵심을 작게 유지하고 디버거·LSP·git을 모두 확장으로 분리.
- **규모 독립:** 1인 노트북부터 강의실(JupyterHub), 일회성 데모(BinderHub)까지 같은 코어 위에서.
- **오픈 거버넌스:** 비영리 NumFOCUS 후원, 누구도 단독으로 통제하지 않는 다수 거버넌스.

이 철학의 결과로 Jupyter는 데이터 사이언스의 라틴어가 됐다. 어디서 일하든, 어떤 언어를 주로 쓰든, 노트북 한 줄을 공유하면 상대가 자기 환경에서 거의 그대로 열어본다. 이 호환성의 가치가 다른 환경(Marimo의 reactive runtime, Colab의 클라우드 호스팅, Hex의 협업 UX)이 아무리 매력적이어도 Jupyter가 자리를 지키는 이유다.

다만 이 호환성이 가장 큰 그림자도 만든다. 이 책 9장에서 본격적으로 다룰 hidden state 문제 — `.ipynb`라는 직렬화 포맷이 코드와 출력을 같이 박아두는 데서 일부 비롯된다. JupyterLab이 좋아도 그 그림자는 그대로 안고 간다. Marimo가 그림자 자체를 다시 짠 답이고(7장), Jupytext와 nbdime이 그림자를 다른 방식으로 푼 답이다(10장).

지금은 표준의 자리를 분명히 인정하고 들어가자. **노트북 입문자가 처음 만져야 할 환경은 JupyterLab이다.** 어떤 다른 환경을 나중에 추가로 손에 넣더라도 — Colab을 쓰든, VS Code Notebooks로 옮기든, Marimo로 갈아타든 — JupyterLab을 한 번 깊이 다뤄본 경험이 기준점이 된다.

## JupyterLab 단축키 — 한 페이지 압축

자주 쓰는 단축키만 정리해두자. JupyterLab은 vim처럼 두 모드가 있다 — **Edit 모드**(셀 안의 텍스트를 편집)와 **Command 모드**(셀 자체를 조작). `Esc`로 Command, `Enter`로 Edit.

**Command 모드 (셀 위에 회색 테두리):**
- `A` — 위에 새 셀
- `B` — 아래에 새 셀
- `D D` — 셀 삭제 (D 두 번 빠르게)
- `Z` — 삭제 취소
- `M` — 마크다운 셀로 변환
- `Y` — 코드 셀로 변환
- `Shift+M` — 선택한 셀들을 합치기
- `↑` `↓` — 셀 사이 이동
- `Shift+↑` `Shift+↓` — 셀 여러 개 선택
- `Ctrl+Shift+P` — Command Palette 열기

**어느 모드에서나:**
- `Shift+Enter` — 셀 실행 후 다음 셀로
- `Ctrl+Enter` — 셀 실행, 자리 유지
- `Alt+Enter` — 셀 실행 후 새 셀 만들기
- `Ctrl+S` — 저장

**Edit 모드:**
- `Tab` — 자동완성 또는 들여쓰기
- `Shift+Tab` — 함수 시그니처 힌트
- `Ctrl+/` — 주석 토글

이 정도만 손에 익혀두면 마우스를 거의 안 잡고 노트북을 다룬다. 첫 일주일은 어색하지만 손에 붙으면 셀 단위 작업이 정말 빠르다. Command Palette(`Ctrl+Shift+P`)는 단축키를 외우지 못한 명령을 검색해서 찾는 만능 키 — 이것 하나만 알아도 살아남는다.

## 언제 쓰고 언제 안 쓰나

장을 닫기 전에 결정 가이드를 짧게 정리하자. 이건 8장 끝의 결정 트리에서 다시 만난다.

**JupyterLab을 쓰면 좋은 경우:**

- 처음 노트북을 배우는 단계 — 표준이고 자료가 가장 많다.
- 로컬 작업이 주이고 GPU를 굳이 안 써도 되는 EDA·분석.
- R, Julia, Scala 같은 언어를 같이 쓰는 다언어 환경.
- 강의실, 연구실, 작은 팀 — JupyterHub로 다중 사용자 띄울 수 있다.
- 노트북 결과물을 그대로 출판하거나 발표 자료로 만들고 싶을 때.

**다른 환경을 고려해야 할 경우:**

- GPU가 필요한 ML 학습 → **Colab / Kaggle** (5장)
- 이미 VS Code 워크플로우가 잡혀 있고 IDE 기능이 더 익숙 → **VS Code Notebooks** (6장)
- 셀 임의 실행과 hidden state가 정말 싫다, 새 프로젝트 시작 → **Marimo** (7장)
- 비기술 이해관계자에게 결과 공유, 실시간 다중 편집 → **Hex / Deepnote** (8장)
- TB급 데이터 EDA, Spark 인프라가 필요 → **Databricks** (8장)
- 노트북을 책·논문·웹사이트로 출판 → **Quarto** (10장)

JupyterLab은 모든 작업의 1순위는 아니지만, 의심스러우면 일단 JupyterLab으로 시작하는 게 안전하다. 자기 작업에 안 맞는 부분이 명확해지면 그때 다른 환경으로 옮기자. 옮기더라도 JupyterLab에서 익힌 기본기(셀, 커널, 매직, 파일 포맷)는 거의 그대로 통한다.

## 자주 만나는 문제와 빠른 해결

장을 닫기 전에 처음 JupyterLab을 만지는 사람이 자주 막히는 지점 몇 개를 정리해두자. 검색 한 번 더 하기 전에 여기 있을 답들이다.

**문제 1 — `jupyter lab`을 쳤는데 명령어를 못 찾는다.**

```
zsh: command not found: jupyter
```

가상환경이 활성화되지 않았거나, 설치가 다른 파이썬에 들어갔을 가능성이 크다. 다음을 확인하자.

```bash
which python
python -m pip show jupyterlab
```

설치돼 있으면 `python -m jupyterlab` 또는 `python -m jupyter lab`으로 띄울 수 있다.

**문제 2 — 토큰을 모르겠다.**

JupyterLab은 처음 띄울 때 인증 토큰을 만들어 URL에 박아둔다. 브라우저가 자동으로 안 열렸다면 터미널 출력의 URL을 직접 복사해야 한다. 잃어버렸다면 다음 명령으로 다시 출력할 수 있다.

```bash
jupyter server list
```

또는 토큰 없이 시작하고 싶으면 (보안 주의!):

```bash
jupyter lab --NotebookApp.token='' --NotebookApp.password=''
```

로컬 단독 사용이면 괜찮지만, 외부 접속 가능한 환경에선 절대 토큰을 비우지 말자. 누구든 들어와 자기 노트북을 만질 수 있게 된다.

**문제 3 — 커널이 자꾸 끊긴다.**

원인이 다양하다 — 메모리 부족, 브라우저 절전, OS 슬립, 무선 네트워크 끊김. 첫 점검은 커널 로그다. 터미널의 JupyterLab 로그에 에러가 찍혀 있는지 본다. `jupyter resource usage` 확장을 깔아 메모리를 모니터링하면 OOM 패턴이 잡힌다.

원격 서버에서 띄운 JupyterLab이 자꾸 끊기면 SSH 터널을 `autossh`로 감싸 자동 재연결되게 하는 패턴도 흔하다.

**문제 4 — 큰 노트북이 너무 느리다.**

`.ipynb` 파일이 수십 MB로 커지면 JupyterLab이 느려진다. 보통 원인은 출력에 박힌 큰 이미지나 표다. `Cell → All Output → Clear`로 출력을 다 지우고 저장하면 파일이 가벼워진다. git에 올릴 땐 출력을 지우는 pre-commit hook을 거는 게 보통이다.

```bash
pip install nbstripout
nbstripout --install
```

이렇게 해두면 git add 할 때 자동으로 출력이 지워진다.

**문제 5 — 확장이 깔리지 않는다.**

JupyterLab 4.x부터는 prebuilt 확장이 표준이다. `pip install <확장>`으로 설치하고 JupyterLab을 재시작하면 동작한다. 옛날 글에서 보는 `jupyter labextension install ...`은 LabExtension legacy 모드로 지금은 거의 안 쓴다.

이 다섯 문제만 알아둬도 첫 두 주의 좌절을 크게 줄일 수 있다.

## 다섯 컴포넌트의 사용 시나리오 — 누가 무엇을 쓰나

가계도를 한 번 더 다른 시선에서 정리하자. 누가 무엇을 쓰는가.

**개인 학습자, 데이터 입문자.** 자기 컴퓨터에 `pip install jupyterlab` → `jupyter lab`. 끝. 다른 컴포넌트는 알 필요가 거의 없다. 1년쯤 쓰다가 "출력이 박힌 노트북을 친구한테 보여주고 싶다" 시점이 오면 그때 BinderHub 배지 만들기를 익히면 된다.

**대학 교수, 강사.** Jupyter Notebook v7으로 강의 자료를 만든다(가벼운 단일 탭 UI가 학생에게 부담이 적다). 강의 노트북은 BinderHub 배지를 박은 GitHub repo에 올린다. 학생이 환경 설치 없이 한 클릭으로 따라 칠 수 있다. 강의실이 크고 학생이 많으면 The Littlest JupyterHub를 강의용 서버에 깔아 학생별 격리 환경을 제공한다.

**연구실 PI 또는 대학 IT.** Zero to JupyterHub로 클러스터에 다중 사용자 노트북 환경을 띄운다. GitHub OAuth로 학교 계정 연동, 사용자별 자원 한도, 공유 데이터셋 마운트, GPU 노드 풀 — 이런 운영 결정을 인프라 팀이 한다. 사용자 시점에선 학교 포털에서 "JupyterHub" 클릭, 로그인, 자기 노트북.

**회사 데이터팀.** 비슷하게 JupyterHub on K8s지만 사용자 인증이 SSO/SAML, 데이터 소스 커넥터(Snowflake, BigQuery, S3)가 미리 박혀 있다. 또는 외부 SaaS(Hex, Deepnote, Databricks — 8장)를 도입해 운영 부담을 줄이는 결정도 흔하다. 자체 운영 vs SaaS의 trade-off는 8장에서 다룬다.

**오픈소스 라이브러리 메인테이너.** 라이브러리 README에 BinderHub 배지를 박는다. 사용자가 "사용 예제"라는 노트북을 한 클릭으로 띄워본다. 이게 사용자 경험에 큰 차이를 만든다 — 설치 없이 라이브러리를 만져볼 수 있는 데모는 강력한 마케팅이다.

자기 위치를 확인했으면, 그에 맞는 컴포넌트만 깊이 파면 된다. 모두를 다 알 필요는 없다.

## 다음 장으로

다음 장에서는 노트북이 우리 컴퓨터를 떠나 클라우드로 가는 이야기를 한다. **Google Colab과 Kaggle Notebooks** — GPU 없이도 ML 실험을 시작하는 가장 빠른 길이다. 무료 티어의 한계와 유료 플랜의 가격까지(2026년 5월 기준) 같이 따져보자. 4장에서 본 두 프로세스 모델이 클라우드로 옮겨가면서 무엇이 같고 무엇이 달라지는지 — 그 차이를 손에 쥐는 게 5장의 시작점이다.
