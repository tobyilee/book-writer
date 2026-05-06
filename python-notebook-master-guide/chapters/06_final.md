# 6장. 에디터 안의 노트북 — VS Code, Cursor, IDE 통합

이런 풍경을 한번 떠올려보자. 모니터에 브라우저 창이 두 개 떠 있다. 하나는 JupyterLab, 다른 하나는 GitHub. 그 옆에 VS Code가 따로 떠 있고, 또 그 옆엔 Slack과 터미널이 깔려 있다. 노트북에서 함수 하나가 자꾸 이상하게 동작하는데, 그게 어디서 import된 함수인지 따라가려면 VS Code로 옮겨가서 검색해야 한다. 코드를 좀 고쳤더니 노트북에서는 여전히 옛 버전이 도는 것 같다. 다시 돌아와 셀을 재실행하지만 변수가 어디서 어디로 흘러가는지 한눈에 안 잡힌다. Git 커밋은 또 다른 창에서.

이쯤 되면 머릿속이 어수선하다. **노트북·코드 에디터·Git·터미널이 다 따로 있다는 사실이 사고를 분산시킨다.** 한 화면 안에서 모든 것을 다룰 수는 없을까. 셀을 실행하다가 의심스러운 함수에 [F12]를 눌러 정의로 점프하고, 거기서 바로 리팩토링하고, 변수 탐색기로 메모리 상태를 확인하고, 그대로 Git에 커밋하는 — 그런 흐름.

답은 이미 우리 손에 와 있다. **VS Code Notebooks**다. 그리고 그 위에서 자란 **Cursor**가 한 발 더 나아가 노트북 안에서 AI 에이전트까지 굴린다. 이번 장에서는 노트북이 "별도 앱"이 아니라 "에디터 안의 한 시민"으로 들어왔을 때 무엇이 달라지는지, Pylance와 디버거와 Git이 한 창에 모였을 때 워크플로우가 어떻게 바뀌는지, 그리고 마지막으로 5장 끝에서 예고한 **"Cursor에서 코드 짜고 Colab GPU로 실행"** 패턴을 함께 잡아보자.

한 가지 짚어두자. 이 장에서 다루는 "에디터 안의 노트북"은 **이미 코드 에디터에 익숙한 사람을 위한 답**이다. 노트북이 처음이라면 4장의 JupyterLab이 더 친절한 진입로다. 거기서 셀·커널·매직에 익숙해진 다음 6장으로 돌아오는 흐름이 자연스럽다. 반대로 VS Code를 일상 도구로 쓰는 개발자라면, 노트북을 위해 별도 환경을 띄우지 않아도 되는 이 장의 흐름이 가장 매끄러운 선택이 된다.

## `.ipynb`를 일급 시민으로 — VS Code Notebooks의 약속

VS Code가 노트북을 처음 지원하기 시작한 건 2019~2020년 무렵이다. 처음에는 Python 확장의 부속 기능 정도였는데, 2021년부터는 노트북이 VS Code의 **빌트인 일급 시민**으로 승격됐다. 이게 무슨 뜻일까.

`.ipynb` 파일을 VS Code에서 열면, 별도 앱을 띄우지 않고도 노트북 UI가 그대로 펼쳐진다. 셀별로 코드와 마크다운을 작성하고, [Shift+Enter]로 실행한다. 출력이 셀 아래에 그대로 나온다. JupyterLab에서 보던 그 노트북이, 익숙한 에디터 안에 들어와 있는 것이다.

```
┌─ VS Code 창 ─────────────────────────────────────────┐
│ Explorer │  notebook.ipynb (활성)                    │
│  ├─ 01_eda.ipynb  │  [+ Code] [+ Markdown] [Run All] │
│  ├─ 02_model.ipynb│                                   │
│  ├─ src/          │  ## 데이터 로드                   │
│  │   ├─ data.py   │                                   │
│  │   └─ models.py │  import pandas as pd              │
│                   │  df = pd.read_csv("sales.csv")    │
│                   │  df.head()                        │
│                   │  ─────                            │
│                   │     id   amount   region          │
│                   │  0  1    100     KR              │
│                   │  ...                              │
└──────────────────────────────────────────────────────┘
```

VS Code Notebooks를 쓰려면 **Python 확장**과 **Jupyter 확장** 두 가지가 깔려 있어야 한다. 둘 다 Microsoft가 공식으로 유지하는 확장이고, 처음 `.ipynb`를 열면 VS Code가 자동으로 설치를 권유한다. 한 번 깔면 그 다음부터는 노트북 파일을 그냥 클릭만 하면 열린다.

뒤에서 도는 커널은 표준 IPython 커널이다. 즉 4장의 Jupyter Server·jupyter_client 메커니즘이 그대로 동작한다. **VS Code는 자기 안에 Jupyter 인프라를 흡수해두고, 그 위에 자기만의 UI를 얹은 셈이다.** 셀 실행 메시지가 ZeroMQ를 타고 오가는 본질은 같다. 다만 사용자가 보는 화면이 브라우저 탭이 아니라 VS Code 탭이라는 게 다른 점이다.

여기까지만 보면 "JupyterLab과 뭐가 다르냐"고 할 수 있다. 다른 점은 **그 옆에 있는 모든 것들**이다. 좌측 사이드바엔 프로젝트 폴더 트리가 펼쳐져 있고, 노트북 옆 탭에선 `src/data.py`를 동시에 편집할 수 있다. 하단엔 통합 터미널, 우측엔 Git 패널, 그리고 곳곳에 Pylance가 자동완성과 타입 힌트를 띄운다. **노트북이 IDE 위에 얹힌 것이 아니라, IDE 자체가 노트북을 흡수한 모습**이다.

## 변수 탐색기 — "지금 메모리에 뭐가 있지?"의 답

JupyterLab에서 한 번쯤 답답했던 순간을 떠올려보자. 셀 여러 개를 정신없이 실행하다 보면 "지금 `df`엔 뭐가 들어 있지?", "`model`은 학습된 상태인가?" 같은 질문이 떠오른다. 그때마다 새 셀을 만들어 `df.head()`나 `print(model)`을 치고 실행한다. 한두 번이야 괜찮지만 하루 종일 이러다 보면 셀 사이사이가 디버깅용 임시 셀로 어수선해진다.

VS Code Notebooks에는 **변수 탐색기(Variables)** 가 내장돼 있다. 노트북 상단의 `Variables` 버튼을 누르면 현재 커널 메모리에 살아 있는 변수 목록이 통째로 펼쳐진다.

```
┌─ Variables ──────────────────────────────────────────┐
│ Name       │ Type        │ Size      │ Value         │
│────────────┼─────────────┼───────────┼───────────────│
│ df         │ DataFrame   │ 1000 × 5  │ [표 미리보기]  │
│ model      │ LogisticReg │ -         │ trained=True  │
│ X_train    │ ndarray     │ (800, 4)  │ [...]         │
│ y_train    │ Series      │ (800,)    │ [...]         │
└──────────────────────────────────────────────────────┘
```

`df` 옆의 작은 아이콘을 누르면 데이터 뷰어가 열려 1000 × 5의 표를 스프레드시트처럼 정렬·필터링하면서 들여다볼 수 있다. 임시 셀을 만들 일이 줄어든다. 셀 중간에 `df.head()`만 끼워두는 일이 없어지니, 노트북 자체가 깔끔해진다.

이 한 가지 기능만으로도 디버깅 시간이 의미 있게 줄어든다. **"지금 메모리에 뭐가 있지?"** 라는 질문은 노트북 작업의 절반쯤을 차지하는데, 그 답을 매번 셀로 묻지 않고 한쪽 패널이 상시 보여준다.

데이터 뷰어는 단순한 표 보기를 넘는다. 컬럼 헤더를 클릭하면 정렬되고, 컬럼별 필터를 걸면 즉시 행이 줄어든다. 큰 DataFrame의 한 행이 의심스러울 때, 그 행의 인덱스를 메모해두고 노트북으로 돌아와 `df.loc[12345]`를 친다. JupyterLab에서는 이런 탐색을 매번 셀로 만들어 답을 얻어야 한다.

또 한 가지 작은 즐거움은 **이미지·NumPy 배열 미리보기**다. 변수 탐색기에서 `image_array` 옆의 미리보기 아이콘을 누르면 이미지가 별도 패널에서 뜬다. CV 작업에서 중간 결과를 시각화하느라 `plt.imshow(...)`를 매 셀마다 박지 않아도 된다.

## MIME 렌더러와 인라인 자동완성 — 한 단계 더

VS Code Notebooks의 출력 영역은 단순한 텍스트 뷰가 아니다. **MIME 렌더러**가 깔려 있어서, 셀이 LaTeX·Plotly·Vega·HTML·이미지를 반환하면 그에 맞는 시각화로 자동 렌더링한다.

```python
# Plotly 차트
import plotly.express as px
df = px.data.gapminder()
px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year",
           color="continent", size="pop", hover_name="country",
           log_x=True)
```

이 셀을 실행하면 노트북 안에 인터랙티브 Plotly 차트가 그대로 살아 있다. 마우스 hover, 줌, 애니메이션 재생까지 다 동작한다. JupyterLab에서 보던 풍경과 똑같지만, 같은 결과가 에디터 안에서 끊김 없이 보인다.

자동완성은 한 단계 더 나아간다. **Pylance**가 노트북 셀에서도 풀 파워로 동작한다. `df.` 까지 치면 DataFrame의 메서드가 타입 정보와 함께 떠오르고, import한 모듈의 함수 시그니처가 인라인으로 보인다. 셀 안에서 `Ctrl+클릭`으로 함수 정의로 점프할 수도 있다. 노트북에서 자기 코드의 모듈 함수를 호출하면, 그 함수가 정의된 `src/data.py`로 점프해 들어가 거기서 수정하고 다시 노트북으로 돌아오는 흐름이 자연스럽다.

```python
# 노트북 셀
from src.data import load_sales

df = load_sales("2026-05.csv")
#         ↑
#  Ctrl+클릭하면 src/data.py의 def load_sales(...): 로 점프
```

이게 작아 보여도, EDA 중간에 함수 하나가 의심스러울 때 그 함수 정의로 한 번에 들어갈 수 있다는 점은 사고의 흐름을 끊지 않는다. JupyterLab에서는 보통 별도 에디터 창을 열어 파일을 찾아 들어가는데, 그 사이에 머릿속 컨텍스트가 한 번 끊긴다. VS Code 안에선 끊김이 없다.

리팩토링 도구도 노트북 셀에서 동작한다. **F2를 누르면 변수 이름 일괄 변경(rename), 셀의 코드 일부를 선택하고 [Ctrl+Shift+R]로 함수 추출(Extract Method).** 노트북에서 자라난 코드를 모듈로 끌어올릴 때 이 도구가 큰 시간을 절약한다. EDA 셀에서 자주 쓰는 패턴 — 가령 결측치 점검·이상치 시각화 — 을 한 함수로 묶고 싶을 때, 그 자리에서 셀 일부를 선택해 함수로 뽑아내고, 그 함수를 `src/utils.py`로 옮기는 일이 [Ctrl+클릭] 두세 번으로 끝난다.

## 디버거 — 셀 실행에 중단점 걸기

노트북에서 디버깅을 어떻게 했었는지 한번 떠올려보자. 보통은 의심스러운 위치에 `print(...)`를 박고, 다시 실행하고, 출력 보고, `print` 지우고. 좀 더 익숙한 사람은 `import pdb; pdb.set_trace()`를 써서 인라인 디버거를 띄운다. 둘 다 가능은 한데, 익숙해지기 전에는 번거롭다.

VS Code Notebooks는 셀에 직접 **중단점(breakpoint)** 을 걸 수 있다. 셀 좌측의 줄 번호 옆 빈 공간을 클릭하면 빨간 점이 찍히고, 셀을 "Debug Cell"로 실행하면 그 줄에서 멈춘다. 멈춘 상태에서 변수 탐색기를 보면 그 시점의 모든 로컬 변수가 펼쳐져 있다. Step Over·Step Into·Continue 버튼으로 한 줄씩 따라갈 수 있다.

이게 진가를 발휘하는 순간은 함수 안에서 무언가 이상한 값이 나올 때다. 노트북 셀에서 `result = process(df)`를 호출했는데 `result`가 빈 DataFrame이라고 해보자. 옛날 같으면 `process` 함수 안에 `print`를 박고 다시 호출했을 것이다. VS Code에선 `process` 함수 정의 (`src/data.py`) 안의 의심 줄에 중단점을 걸고, 노트북에서 셀을 Debug 모드로 실행하면 자동으로 그 줄에서 멈춘다. 그 자리에서 변수 상태를 확인하고, 한 줄씩 따라가면서 어디서 빈 DataFrame이 만들어졌는지 보인다. **셀 호출 → 함수 내부 → 디버거**라는 흐름이 한 환경에서 끊김 없이 이어진다.

이런 디버깅 경험은 사실 오래 ML/데이터 작업을 한 사람일수록 그 가치를 안다. `print` 디버깅으로 하루를 보내본 적 없는 사람은 드물다. 노트북에 진짜 디버거가 들어오면, 그 시간이 의미 있게 줄어든다.

조건부 중단점도 잊지 말자. 중단점에 우클릭으로 "Conditional Breakpoint"를 걸면 특정 조건이 참일 때만 멈춘다. 가령 `i == 1000` 같은 조건. 큰 루프 안에서 1000번째 반복만 디버깅하고 싶을 때, 한 줄짜리 `if i == 1000: pdb.set_trace()` 같은 임시 코드를 박아넣을 필요가 없다. 디버거가 알아서 1000번째에서 멈춰준다.

또 하나, **예외 발생 시 자동 중단** 옵션도 있다. 디버그 사이드바의 "Breakpoints" 패널에서 "Uncaught Exceptions"를 체크해두면, 노트북 셀에서 예외가 던져진 그 순간 디버거가 자동으로 멈춘다. 예외가 발생한 시점의 변수 상태를 그 자리에서 들여다볼 수 있다. 트레이스백만 보고 머릿속으로 추론하던 옛 디버깅 방식보다 훨씬 빠르다.

## Git이 한 창에 — 커밋부터 PR까지

`.ipynb`의 git diff가 끔찍하다는 얘기는 4장에서 짧게 지나갔다. 이 문제는 10장에서 Jupytext·nbdime로 본격적으로 다룰 텐데, VS Code Notebooks의 통합 환경에서는 한 가지 작은 즐거움이 있다. **Git 패널이 노트북과 같은 창에 있다.**

좌측 사이드바의 Source Control 탭을 누르면 변경된 파일 목록이 뜬다. `notebook.ipynb` 옆의 차이 아이콘을 누르면, 비록 JSON 디프지만 VS Code가 셀 단위로 어느 정도 읽기 쉽게 정리해서 보여준다 (확장 `vscode-jupyter`의 노트북 디프 기능). 만족스럽지는 않지만, 별도 창을 띄울 일은 없다. 커밋 메시지를 입력하고 [✓]를 누르면 커밋된다. Push, PR 생성까지 같은 창에서 가능하다.

여기에 `nbdime` 확장과 **GitHub Pull Requests** 확장을 얹으면 더 매끄러워진다. nbdime이 셀 단위 의미 디프를 제공하고, GitHub PR 확장이 PR 코멘트를 노트북 위에 인라인으로 보여준다. **노트북·코드·디프·코멘트가 다 한 창에서 다뤄진다.**

이 정도가 되면 "별도 앱으로 노트북을 띄울 이유"가 점점 줄어든다. 워크플로우의 가시화·통합화 — 이게 VS Code Notebooks의 진짜 가치다.

한 가지 팁을 더하자면, **노트북 출력은 git에서 빼두는 편이 낫다.** `.gitattributes`에 다음 한 줄을 두면 nbconvert가 커밋 시점에 출력을 자동으로 비운다.

```
*.ipynb filter=nbstripout
```

`nbstripout` 도구를 설치하고 `nbstripout --install`로 등록하면 활성화된다. 출력이 빠진 디프는 한결 깔끔하다. (이 패턴도 10장에서 더 자세히 다룬다.)

## Cursor — VS Code의 AI 분파

Cursor는 VS Code의 포크다. 안쪽 코어는 거의 같지만, AI 기능이 깊이 박혀 있다는 게 다른 점이다. Cursor의 차별화는 단순한 "코드 자동완성"을 넘는다. **Agent 모드**가 핵심이다.

2025년 업데이트에서 Cursor는 **노트북 셀 안에서도 Agent 모드**를 지원하기 시작했다. 무엇을 의미할까. 노트북 셀을 빈 채로 두고 사이드 채팅에 자연어로 작업을 묘사하면, Agent가 셀 내용을 채우고, 필요하면 다른 셀을 추가하고, 외부 모듈 (`src/data.py` 등)까지 같이 수정한다.

> 📌 Cursor의 Agent 모드 동작·UI는 빠르게 진화한다. 본문은 **2025년 업데이트 기준**의 모습이며, 핵심은 "노트북 + 모듈 + 멀티 파일 편집을 한 에이전트가 다룬다"는 패러다임 자체다.

가령 다음과 같은 프롬프트를 쳐본다고 하자.

> "타이타닉 데이터셋을 불러와서 전처리하고, 로지스틱 회귀로 학습한 다음, ROC 곡선을 그려줘. 데이터 로드와 전처리는 `src/data.py`에 함수로 분리해서 노트북에서는 호출만 하도록."

Agent는 다음과 같이 움직인다. (대략)

1. `src/data.py`에 `load_titanic()`, `preprocess()` 함수를 작성·저장
2. 노트북 셀 1에 `from src.data import load_titanic, preprocess` 임포트
3. 셀 2에 `df = load_titanic(); X, y = preprocess(df)` 호출
4. 셀 3에 `LogisticRegression` 학습 코드
5. 셀 4에 ROC 곡선 그리기

여기서 중요한 점은, **모듈 분리·노트북 호출·시각화**라는 베스트 프랙티스를 Agent가 자동으로 적용한다는 것이다. (5.7 리팩토링 패턴 참고.) 사람이 한 줄씩 따라 짜면 30분 걸릴 작업이 5분 안에 끝난다. 물론 Agent가 짠 코드를 한 번 쭉 검토하는 시간은 별도로 필요하다.

이게 좋기만 한가. 한쪽에서는 "AI에게 전적으로 의존하면 코드 이해도가 떨어진다"는 우려가 있다. 다른 쪽에서는 "Agent를 페어 프로그래머로 쓰면 사고의 속도가 비약적으로 빨라진다"는 평가가 있다. 둘 다 일리가 있다. 실용적으로는, **Agent가 짠 코드를 매번 의식적으로 읽고, 의도와 다르면 직접 고치는 습관**이 답이다. Agent를 운전자가 아니라 내비게이터로 두자는 거리감 — 5장에서 Colab Data Science Agent를 다룰 때 했던 권고와 같다.

Cursor의 다른 흥미로운 기능 한 가지를 짚자면 **"Apply"** 모델이다. Cursor 채팅에서 코드 변경을 제안받으면, 그 변경을 노트북·모듈에 직접 반영할지 미리 보기로 검토하고 승인할 수 있다. 변경 전·후가 좌우로 펼쳐지고, 한 줄씩 accept/reject할 수 있다. 무지성으로 다 받지 않고, 하나씩 검토하며 받는 흐름이 자연스럽다.

또 하나, Cursor는 **`.cursorrules`** 라는 파일로 프로젝트별 Agent 행동 규칙을 정할 수 있다. 가령 "데이터 로드 함수는 항상 `src/data.py`에 두라" 또는 "DataFrame 변환은 항상 새 변수에 대입하라(원본 변형 금지)" 같은 규칙을 한 번 박아두면, Agent가 그 규칙 안에서 코드를 짠다. 이런 작은 거버넌스 한 줄이 팀 작업의 일관성을 끌어올린다.

> 📌 Cursor는 활발히 진화 중이다. Agent 모드의 UI·기능명·`.cursorrules` 같은 세부는 빠르게 바뀐다. 본 절은 **2025년 업데이트 기준**의 모습이다.

## "Cursor에서 코드, Colab에서 실행" — 깊이 다루기

5장 끝에서 한 문장 예고했던 패턴이 있다. **"코드는 Cursor에서 AI로 짜고, 실행은 Colab GPU에서."** 이번엔 그 본편을 함께 잡아보자.

이 패턴이 왜 매력적인가. Cursor의 Agent와 리팩토링·자동완성은 노트북 작성을 비약적으로 빠르게 만들지만, 정작 GPU가 없는 로컬에서는 학습이 불가능하다. 반대로 Colab에는 GPU가 있지만, 코드 편집 경험은 Cursor에 비할 바가 아니다. 두 환경을 합치면 양쪽의 장점만 쓸 수 있다.

작업 흐름은 대략 이렇게 잡힌다.

### 1단계: Cursor에서 노트북 작성

Cursor에서 노트북(`.ipynb`)을 열고 Agent 모드로 모델 학습 코드를 작성한다. 이때 **`src/`로 함수를 외부 모듈화**하는 베스트 프랙티스를 같이 적용해두자. 그래야 두 환경 모두에서 같은 코드가 도는 게 보장된다.

```
project/
├── notebook.ipynb        # 학습 흐름 + 시각화
├── src/
│   ├── __init__.py
│   ├── data.py           # 데이터 로드·전처리
│   ├── model.py          # 모델 정의
│   └── train.py          # 학습 루프
└── requirements.txt
```

`notebook.ipynb`는 다음처럼 모듈 호출 위주로 짠다.

```python
# 셀 1: 임포트
%load_ext autoreload
%autoreload 2

from src.data import load_dataset, make_loaders
from src.model import MyModel
from src.train import train_one_epoch
import torch

# 셀 2: 데이터
train_loader, val_loader = make_loaders(load_dataset("data.csv"), batch_size=32)

# 셀 3: 모델
model = MyModel().cuda() if torch.cuda.is_available() else MyModel()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 셀 4: 학습 루프
for epoch in range(10):
    loss = train_one_epoch(model, train_loader, optimizer)
    print(f"Epoch {epoch}: loss={loss:.4f}")
```

`%load_ext autoreload` + `%autoreload 2`는 잊지 말고 박아두자. `src/` 안의 모듈을 수정하면 노트북에서 자동으로 다시 import된다. 두 환경에서 코드를 자주 오갈 때 이 한 줄이 큰 차이를 만든다.

### 2단계: Git으로 동기화

작업한 코드를 GitHub에 푸시한다. Cursor의 통합 Git 패널로 한 번에 처리할 수 있다.

```bash
git add notebook.ipynb src/ requirements.txt
git commit -m "Add training pipeline"
git push
```

### 3단계: Colab에서 clone, 실행

Colab을 열고 새 노트북에서 다음 한 줄을 친다.

```python
!git clone https://github.com/<user>/<repo>.git
%cd <repo>
!pip install -r requirements.txt
```

이제 Colab에 자기 모듈 (`src/data.py` 등)이 통째로 올라와 있다. `notebook.ipynb`를 Colab에서 열고 (또는 새 셀에서 모듈을 import하고) 학습을 돌린다.

```python
%cd /content/<repo>
%load_ext autoreload
%autoreload 2

from src.data import load_dataset, make_loaders
from src.model import MyModel
from src.train import train_one_epoch
import torch

# (5장에서 본 학습·체크포인트 패턴)
```

### 4단계: 코드 수정, 다시 동기화

Colab에서 학습이 잘 안 된다 싶으면, 다시 로컬 Cursor로 돌아와 모델을 고치고, 푸시하고, Colab에서 `git pull`로 받는다.

```python
# Colab 셀
!git pull
```

`%autoreload 2`가 켜져 있으니, `git pull` 후 셀을 다시 실행하면 새 코드가 반영된다. 이 흐름이 손에 익으면 **Cursor의 편집 경험 + Colab의 GPU**를 한 작업 안에서 매끄럽게 오갈 수 있다.

물론 더 부드러운 방법도 있다. **Colab은 GitHub 노트북을 직접 열 수 있다.** Colab에서 [File] → [Open notebook] → [GitHub]를 누르고 자기 repo를 선택하면 노트북이 곧장 열린다. 수정 후 [File] → [Save a copy in GitHub]로 저장하면 새 커밋이 만들어진다. 이 길도 한번 시도해볼 만하다.

한 가지 마음에 새겨둘 점이 있다. **두 환경에 같은 노트북이 동시에 열려 있으면, 어느 한쪽의 변경이 덮어써질 수 있다.** Cursor에서 셀을 수정하고 push하지 않은 상태에서 Colab을 열어 같은 노트북을 만지면 두 갈래가 갈라진다. 한 번에 한 환경에서만 작업하고, 옮겨갈 때마다 push/pull로 동기화하는 규율이 필요하다. git이 두 환경을 잇는 중심축이라는 점을 잊지 말자.

또 한 가지 변형은 **Colab의 "Connect to local runtime"** 옵션이다. Colab UI는 그대로 쓰면서, 셀 실행은 자기 로컬 컴퓨터의 Jupyter Server에서 도는 방식이다. 로컬에 GPU가 있다면 Colab의 깔끔한 UI를 쓰되 자기 GPU에서 돌릴 수 있다. 다소 부수적인 길이지만, 워크플로우에 따라 유용할 때가 있다.

이 두 도구의 결합은 한 가지 원칙을 보여준다. **노트북은 어디에 있든 노트북이다.** 같은 `.ipynb`가 Cursor에서 열리고, Colab에서 실행되고, JupyterLab에서 발표 자료로 쓰인다. 환경은 각자의 강점을 더하고, 우리는 그 사이를 오가며 작업한다.

## 언제 VS Code Notebooks를, 언제 JupyterLab을

이쯤에서 한 가지 결정 가이드를 잡아두자. 같은 노트북이라도 환경에 따라 잘 맞는 작업이 다르다.

| 상황 | 추천 | 이유 |
|------|-----|------|
| `src/` 모듈을 자주 오가는 ML 프로젝트 | **VS Code Notebooks** | 모듈 점프·리팩토링·디버거가 한 창에 |
| 노트북·터미널·Git을 동시에 다루는 작업 | **VS Code Notebooks** | 사이드바에 모두 통합 |
| 디버거를 자주 써야 하는 코드 중심 작업 | **VS Code Notebooks** | 셀 중단점 + 함수 내부 step |
| AI 보조로 빠른 코드 작성 | **Cursor** | Agent 모드 + 멀티 파일 편집 |
| 인터랙티브 위젯·탐색이 중심인 EDA | **JupyterLab** | 위젯 생태계·확장(JupyterLab-git, ipywidgets 등) 성숙 |
| R·Julia 등 다언어 작업 | **JupyterLab** | 다언어 커널이 1급 시민 |
| 발표·강의 자료(슬라이드 모드, 라이브 데모) | **JupyterLab** | RISE·라이브 위젯 등 발표 도구 |
| 클라우드 학습 (GPU 필요) | **Colab** + (Cursor와 git 연동) | 5장 워크플로우 |
| BinderHub 한 클릭 실행 자료 | **JupyterLab** | mybinder.org가 표준 |

이 표는 절대 기준이 아니라 출발선이다. 자기 작업의 비중이 어디에 더 쏠려 있는지 보자. **코드와 노트북을 자주 오간다 → VS Code 계열**, **노트북 안에서 다 끝난다 → JupyterLab** 정도가 1차 분기다.

한 가지 더. 두 환경은 양자택일이 아니다. **두 환경을 동시에 띄워두고 같은 노트북을 오가는 것도 가능하다.** 단 hidden state와 커널 동기화가 어그러질 수 있으니, 한 번에 한 환경에서만 작업하는 편이 안전하다. JupyterLab으로 EDA·발표하다가, 코드 리팩토링이 필요해지면 VS Code로 옮겨가서 모듈을 정리하고 돌아오는 흐름이 자연스럽다.

작업 단계를 한 번 더 다듬자면 이런 식이다.

1. **탐색기:** JupyterLab에서 데이터를 처음 만져보고 가설을 세운다. 위젯·인라인 그래프가 풍부해 탐색에 좋다.
2. **정리기:** 탐색이 어느 정도 끝나면 VS Code Notebooks로 옮겨와 셀을 정리하고, 자주 쓰는 코드를 `src/` 모듈로 추출한다. 디버거와 리팩토링 도구가 진가를 발휘한다.
3. **공유기:** 발표·교육용으로 정리한 노트북은 다시 JupyterLab(또는 nbconvert로 HTML 출력)으로 가져가 슬라이드·라이브 데모로 굴린다.

한 작업이 단계마다 어울리는 도구로 옮겨가는 흐름이다. 도구는 적이 아니라 단계별 협력자다.

## Live Share — 실시간 페어 프로그래밍

VS Code의 협업 도구로 **Live Share** 가 있다. 다른 사람을 자기 VS Code 세션에 초대해, 노트북·터미널·디버거를 실시간으로 같이 만질 수 있다. Deepnote의 실시간 다중 편집이 클라우드 기반 SaaS의 답이라면, Live Share는 **로컬 작업의 페어 프로그래밍** 답이다.

쓰는 법은 단순하다. Live Share 확장을 깔고 [Live Share] 버튼을 누르면 공유 링크가 생성된다. 그 링크를 동료에게 보내면, 동료가 자기 VS Code(또는 브라우저)로 접속해 같은 노트북을 같이 본다. 셀을 같이 실행하고, 변수 탐색기를 공유하고, 디버거에 같이 들어간다.

특히 두 사람이 코드 리뷰를 같이 하거나, 시니어가 주니어의 노트북을 같이 보면서 디버깅을 도와주는 상황에 잘 맞는다. 화면 공유보다 인터랙션이 풍부하다 — 동료가 셀에 직접 코드를 칠 수 있고, 자기 커서가 어디에 있는지가 서로에게 보인다.

Live Share는 비실시간 협업에는 부족하지만, **시니어·주니어 멘토링이나 짧은 페어 디버깅 세션** 같은 상황에서는 클라우드 SaaS 못지않게 부드럽다.

## VS Code Notebooks를 처음 시작할 때 — 첫 5분

이 장을 읽고 "한번 써볼까" 싶은 독자를 위해 첫 5분 가이드를 두자.

```bash
# 1. VS Code 설치 (이미 있으면 건너뛰기)
# https://code.visualstudio.com/

# 2. Python·Jupyter 확장 설치
# 좌측 사이드바의 Extensions(Ctrl+Shift+X) 패널에서
# "Python" (Microsoft)
# "Jupyter" (Microsoft)
# 두 개를 설치

# 3. Python 인터프리터 선택
# Ctrl+Shift+P → "Python: Select Interpreter"
# 자기 가상환경의 python을 고름 (없으면 시스템 Python)

# 4. ipykernel 설치 (인터프리터에 ipykernel이 없으면 자동 설치 안내가 뜸)
pip install ipykernel
```

이제 임의 폴더에서 `test.ipynb` 파일을 만들면 바로 노트북 UI가 뜬다. 첫 셀에 `import pandas as pd`를 치고 [Shift+Enter]를 누르면 끝. 셀이 실행되고 다음 셀로 커서가 넘어간다.

처음 노트북을 띄우는 데 1분, 환경을 세팅하는 데 4분 정도. 4장의 JupyterLab보다 더 빠르게 시작할 수 있다. 이미 VS Code를 쓰고 있다면 이게 가장 작은 마찰의 진입로다.

## 워크플로우의 변화 — 사고의 흐름이 끊기지 않는다

이 장에서 다룬 모든 기능은 한 방향을 가리킨다. **사고의 흐름을 끊지 않는 작업 환경.** 노트북에서 의심 함수가 보이면 그 자리에서 정의로 점프하고, 거기서 고치고, 디버거로 따라가고, 변수 탐색기로 상태를 확인하고, Git에 커밋하고, 다시 노트북으로 돌아온다. 한 창 안에서.

JupyterLab도 좋다. 그것대로 강점이 분명하다. 다만 **코드 중심**·**모듈 분리**·**디버거**·**Git** — 이 네 가지가 워크플로우의 큰 비중을 차지한다면, VS Code Notebooks가 더 잘 맞는다. 이 사실을 알고 양쪽을 자유롭게 오가는 사람이 결국 가장 빠르다.

물론 IDE 통합에는 한 가지 약점이 있다. **UI가 IDE에 종속**된다. 노트북 자체의 인터랙티브 위젯 생태계 (ipywidgets·voila 등)나 일부 JupyterLab 확장은 VS Code에서 동작 안 하거나 제한적이다. "노트북다움"을 100% 살리는 건 여전히 JupyterLab의 영역이다. 도구마다 자기 자리가 있다는 사실을 잊지 말자.

또 하나, **R·Julia 등 다언어 작업**도 JupyterLab만큼 매끄럽지 않다. VS Code에도 R·Julia 확장이 있고 Jupyter 확장과 결합해 쓸 수 있긴 하지만, JupyterLab의 다언어 지원에 비하면 친절하지 않다. Python이 아닌 언어가 작업의 핵심이라면 JupyterLab을 우선 후보로 두는 게 자연스럽다.

## 작업 시나리오 한 가지 — 30분 ML 프로토타입

마지막으로 이 장에서 다룬 도구들을 한 흐름에 묶는 시나리오를 잡아보자. **"30분 안에 모델 한 채를 프로토타입한다"** 는 가정이다.

1. **0~5분 — Cursor 열기, 새 노트북 생성.** 채팅에 작업 묘사: "Iris 데이터셋으로 분류 모델 만들어줘. 데이터 로드는 src/data.py로." Agent가 모듈과 노트북을 동시에 작성.
2. **5~10분 — 검토·수정.** Agent가 짠 코드를 한 셀씩 읽고, [Ctrl+클릭]으로 모듈 정의에 점프해 한 줄씩 검토. 이상한 부분은 직접 고침. 변수 탐색기로 데이터 구조 확인.
3. **10~15분 — 학습 셀 디버그.** 모델 학습이 한 번에 안 되면 셀에 중단점을 걸고 디버거로 step. 어느 변수가 잘못됐는지 한 줄씩 따라감.
4. **15~20분 — 결과 시각화.** Plotly·Seaborn으로 confusion matrix·feature importance 차트. MIME 렌더러가 인터랙티브 차트를 노트북 안에 그대로 띄움.
5. **20~25분 — Git 커밋·푸시.** Source Control 패널에서 변경 파일 검토, 커밋 메시지 작성, push.
6. **25~30분 — Colab으로.** Colab을 열고 `!git clone`으로 받아 GPU 런타임에서 같은 노트북을 돌려봄. 학습 시간이 1/10로 줄어듦.

이 30분이 끝나면 손에는 다음과 같은 자산이 남는다.

- 정리된 `src/` 모듈 (재사용 가능)
- 노트북 파일 (`.ipynb`, 발표·공유용)
- Git 히스토리 (재현 가능)
- 학습된 모델 (Drive에 저장)

이 흐름은 한 번 해보면 손에 익는다. 도구가 손가락에 붙으면 30분이 20분이 되고, 익숙해지면 더 줄어든다. **사고의 흐름이 도구의 마찰에 깎이지 않는 작업** — 이 장 전체가 가리키는 방향이다.

## 마무리

노트북이 별도 앱이었던 시절에는 노트북·에디터·Git·터미널이 따로 살았다. VS Code Notebooks는 그 모든 것을 한 창에 모았고, Cursor는 거기에 AI 에이전트까지 얹었다. **자기 에디터를 노트북 환경으로 승격시키는 길**이 이제 누구에게나 열려 있다.

다음 장에서는 다시 한 단 올라가본다. **Marimo** — 노트북을 처음부터 다시 짜겠다고 나선 도구. 셀을 임의 순서로 실행해도 문제가 없도록 reactive runtime을 깔고, `.py`로 저장해 git을 정상화하고, 노트북 자체를 즉시 웹 앱으로 띄울 수 있게 한다. Jupyter 이후의 노트북은 무엇을 다시 짜고 있는가 — 그 답을 한 챕터에 걸쳐 손으로 잡아보자.
