# Python Notebook 마스터 가이드 — 저술 계획 (v2)

> v2 변경 요약: 7장 분할(Marimo 단독 + 협업/엔터프라이즈 신설)로 11장 구조 / 2장 ZeroMQ 디테일을 박스로 분리 / 환경 설정 가이드(부록 A) 신설 / 결정 트리 leaf node 8개와 비교표 54셀 확정 / 9장 NBSafety 단락 추가 / 9장 톤을 "진지한 평어체"로 명시.

## 제목 후보

1. **Python 노트북 마스터 가이드 — Jupyter부터 Marimo까지, 도구를 가르는 안목**
   - 톤: 정공법, 백과사전적 신뢰감
   - 포지셔닝: "노트북 생태계 전반을 다루는 한 권." 검색·서가 진열 양쪽에 강하다. 슬러그(`python-notebook-master-guide`)와 1:1 매칭.

2. **노트북, 어디까지 써봤니 — Python 데이터 작업자를 위한 환경 사용설명서**
   - 톤: 친근한 실무자 말투, 청유형이 자연스럽게 붙는다
   - 포지셔닝: 입문자에게 "겁먹지 말고 들어와"의 손짓. Toby 스타일과 가장 잘 맞고, 책의 첫 인상이 부드럽다. 다만 "마스터 가이드"라는 권위감은 약해진다.

3. **Jupyter 너머의 노트북 — Python 학습자가 알아야 할 9가지 환경과 그 철학**
   - 톤: 약간의 도발, 큐레이션 강조
   - 포지셔닝: "Jupyter만 알고 있는 사람"을 정조준. Marimo·Quarto·Hex·Databricks까지 다룬다는 차별점이 제목에서 바로 드러난다.

**추천: 1번.** 슬러그·검색·서점 카테고리 모두에 정합적이고, 책의 약속(전 환경 + 안목)을 한 줄로 전달한다. Toby 톤은 본문에서 살리되, 제목은 권위와 명확함을 우선한다. 부제(*Jupyter부터 Marimo까지, 도구를 가르는 안목*)에 큐레이션·관점성을 담아 1번과 3번의 장점을 합쳤다.

---

## 책 특성

- **장르:** 에세이형 기술서 (도구 가이드 + 관점 비평 + 워크플로우 레시피)
- **분량:** 약 240~280쪽 / 한글 약 195,000~215,000자 (11개 챕터 × 평균 17,000~20,000자 + 부록 ~6,000자)
- **난이도:** 입문~중급. Python 기본 문법(함수·import·pandas의 존재 정도)은 알지만, 노트북 도구 생태계는 처음 접하는 독자가 진입점.
- **독자 여정:**
  - **진입 상태:** "Jupyter라는 게 있다고 들었다. Colab도 본 적은 있다. 근데 이걸 언제·어떻게 쓰는지, 왜 이렇게 종류가 많은지 모르겠다."
  - **출구 상태:** "내 작업(EDA / ML 실험 / 보고서 / 강의 자료 / 협업)에 어떤 노트북을 골라야 하는지 안다. 매직·위젯·Jupytext·Papermill·nbdime·Marimo의 reactive 모델까지 손에 익었고, hidden state 함정을 피하는 습관이 잡혔다. 노트북을 출판물·앱·파이프라인 산출물로 확장할 줄 안다."

---

## 내러티브 아크

책은 다섯 개의 큰 호(arc)로 흐른다.

1. **왜 노트북인가 (1장)** — 도구 자랑 전에 "노트북이라는 매체가 왜 생겼는지, 왜 데이터·ML·교육에서 표준이 됐는지"를 짧고 강하게 박는다. 독자가 "단순한 IDE 대체재가 아니구나"를 느끼고 들어와야 뒤가 살아난다.
2. **노트북의 해부학 (2~3장)** — 셀·커널·상태·매직·`.ipynb` 포맷. 어느 환경을 쓰든 공통으로 통하는 기초. 2장은 본문을 가볍게 가져가고(Shell+IOPub 두 소켓의 라이프사이클만), ZeroMQ 5소켓 전체와 메시지 스키마는 박스로 분리한다. 여기서 hidden state 문제를 미리 한 번 건드려둔다(나중 9장과 호응).
3. **환경 투어 (4~8장)** — Jupyter/JupyterLab → Colab/Kaggle → VS Code(+Cursor) → Marimo → Deepnote/Hex/Databricks. 각 환경의 **철학**을 먼저 설명하고, 실제 손을 움직이는 짧은 워크플로우 → "언제 쓰고 언제 안 쓸지"로 닫는다. 7장은 Marimo만 단독으로 다뤄 reactive 패러다임의 무게를 살리고, 8장은 협업·엔터프라이즈로 청자가 다른 세 환경을 묶는다. 비교는 8장 끝에 큰 표·결정 트리로 정리.
4. **노트북의 그림자와 출구 (9~10장)** — 재현성·hidden state(논쟁 정면 다루기), Jupytext·nbdime·Papermill·Voila로 git·협업·자동화·배포까지 끌어내기. 노트북을 "출력 산출물" 또는 "출판의 시작점"으로 다시 자리매김.
5. **노트북을 잘 쓰는 사람 (11장)** — 베스트 프랙티스, AI-네이티브 노트북(Jupyter AI·Cursor·Marimo Pair), 2025~2026 흐름과 앞으로 5년 전망. 독자가 책을 덮을 때 "내 작업에 적용할 다음 한 걸음"이 명확해야 한다.

이 곡선은 입문(1~3장)에서 평탄하다가, 4~6장에서 도구별 깊이로 점진적으로 올라가고, 7장(Marimo의 reactive 철학)에서 한 단 오른 뒤 8장(결정 트리)에서 처음으로 독자가 능동적 선택을 강요받는다. 9장(hidden state·재현성 논쟁)에서 가장 가팔라진 뒤, 10~11장에서 다시 실무 종합으로 내려온다.

---

## 챕터 목록

### 1장. 왜 우리는 노트북을 쓰게 됐나
- **핵심 질문:** 노트북이라는 매체는 어디서 와서, 왜 데이터·ML·교육의 기본 작업대가 됐을까?
- **주요 내용:**
  - 노트북의 정의: 코드·출력·서사가 한 문서에 엮인 대화형 환경
  - 과학자의 실험실 노트 → IPython → Jupyter로 이어진 계보, 이름이 Julia+Python+R에서 왔다는 일화
  - "셀 단위 실행"이 만든 사고방식의 변화 — 가설을 즉시 검증하는 습관
  - 노트북이 잘 맞는 작업 5가지(EDA·ML 실험·교육·보고서·라이브 데모)와 잘 안 맞는 작업
  - 이 책의 지도: 앞으로 만날 환경 9가지를 한 페이지로 미리 보여주기
- **독자가 얻는 것:** "왜 IDE 말고 노트북인가"에 자기 언어로 답할 수 있게 된다.
- **예상 분량:** 약 14,000자 (오프닝답게 짧고 강하게)
- **핵심 자료:** §1.1, §3.1~§3.6 도입부, 환경 일람은 §2 전체 요약

### 2장. 셀, 커널, 상태 — 노트북의 해부학
- **핵심 질문:** 내가 셀 [Shift+Enter]를 누르면 정확히 어떤 일이 일어나는가?
- **주요 내용:**
  - 2-프로세스 아키텍처: 프런트엔드(브라우저/IDE) ↔ 커널 (그림 한 장으로)
  - **본문은 Shell + IOPub 두 소켓만 다룬다** — "코드 보냄 → 결과 돌아옴" 라이프사이클 다이어그램으로 단순화
  - 커널 다중성: 같은 프런트엔드에서 R·Julia·Scala가 도는 이유
  - "상태(state)"라는 개념 처음 소개 — hidden state 문제의 씨앗을 심어두기(9장 복선)
  - **Box A — "더 깊이: Jupyter 메시징 프로토콜"** 부록형 박스로 분리: ZeroMQ 5소켓(Shell/IOPub/Stdin/Control/Heartbeat) 전체, JSON dict-of-dicts 메시지 형식 한 예시. 본문 진행에 끼지 않고 호기심 많은 독자만 들어가도록 시각적으로 분리.
- **독자가 얻는 것:** 어느 노트북 환경을 만나도 "프런트와 커널이 따로 있다"는 멘탈 모델이 잡힌다.
- **예상 분량:** 약 16,000자 (본문 ~14,000 + Box A ~2,000)
- **핵심 자료:** §1.1~§1.2, jupyter_client messaging 문서

### 3장. 매직 커맨드, 셸, 파일 포맷 — 모든 노트북에 통하는 도구상자
- **핵심 질문:** 어떤 노트북에 가도 바로 써먹을 수 있는 공용 무기는 무엇인가?
- **주요 내용:**
  - 라인 매직 vs 셀 매직 차이를 먼저 분명히
  - 실전 매직 베스트 8: `%timeit`, `%%writefile`, `%matplotlib inline/widget`, `%load_ext autoreload` + `%autoreload 2`, `%env`, `%who/%whos`, `%%bash`, `!shell`
  - 미니 데모 5개(§5.1) — 실행 결과까지 책에 박아 보여주기
  - `.ipynb`(JSON) vs percent format(`# %%`) — 왜 둘 다 알아야 하는가
  - Jupytext 양방향 동기화 첫 등장(10장에서 본격 다룸)
- **독자가 얻는 것:** 환경이 바뀌어도 즉시 생산적인 셀을 칠 수 있다.
- **예상 분량:** 약 19,000자
- **핵심 자료:** §1.3, §1.4, §5.1, §5.2, KDnuggets Magic Methods Cheat Sheet

### 4장. Jupyter와 JupyterLab — 표준을 깊이 이해하기
- **핵심 질문:** Jupyter Notebook, JupyterLab, Jupyter Server, JupyterHub, BinderHub — 같은 이름이 자꾸 나오는데 뭐가 뭔가?
- **주요 내용:**
  - **0단계: 노트북을 실행할 환경 만들기** — pip / conda / venv / uv 1페이지 비교 + `pip install jupyterlab` / `uv tool install jupyterlab` 양 갈래 명령. 자세한 내용은 부록 A로 위임하고, 4장 본문에는 "가장 빠른 한 줄"만 박는다.
  - 한 장의 가계도로 다섯 컴포넌트의 관계 정리
  - Notebook v6 vs v7 vs `nbclassic`의 현재 상태(2026 기준 — 시점 명시)
  - JupyterLab의 IDE형 UX: 사이드바·터미널·디버거·LSP·Git 통합
  - JupyterHub 두 가지 배포 패턴(Zero to JupyterHub on K8s / The Littlest JupyterHub)
  - **보안 박스(반 페이지):** 멀티테넌트 환경의 토큰·네트워크 격리·컨테이너 탈출 위험은 인프라 책의 영역 — "이 책의 범위 밖" 명시 + 1차 자료 링크
  - BinderHub로 "이 링크 누르면 바로 실행" 만들기 (§5.9 배지)
  - 철학 박스: "모든 언어, 모든 워크플로우를 위한 범용 표준"
  - "언제 쓰고 언제 안 쓰나" 마무리
- **독자가 얻는 것:** Jupyter 생태계의 지도를 머릿속에 그리고, 자기 컴퓨터에서 즉시 실행할 수 있다.
- **예상 분량:** 약 20,000자
- **핵심 자료:** §2.1 전체, jupyter.org / jupyterhub.readthedocs.io / binderhub.readthedocs.io, Hex의 Jupyter vs JupyterLab 비교, uv 공식 문서

### 5장. 클라우드 노트북 — Colab과 Kaggle, GPU의 대중화
- **핵심 질문:** 내 노트북에 GPU가 없어도 ML 실험을 시작할 수 있을까?
- **주요 내용:**
  - Colab의 셀링 포인트: 설치 0초, 무료 GPU/TPU, Drive 연동
  - 무료 티어 한계(2026): T4·~12GB RAM·세션 ~12h·피크 시간 거부
  - 유료 플랜(Pro $11.99 / Pro+ $49.99 / Pay As You Go) — "2026년 5월 기준" 명시
  - AI-First Colab(Data Science Agent)로 자연어 → 노트북 자동 생성
  - Kaggle Notebooks: 데이터셋 한 클릭 마운트, fork·복제로 학습
  - 워크플로우 레시피: Colab에서 학습 → 가중치를 Drive로 → 로컬에서 추론
  - **한국 사례 박스(반 페이지):** 한국 데이터 사이언스 학습자(velog/OKKY/카페)에서 자주 보이는 "Colab으로 첫 모델 굴린 경험" 한두 사례 인용 (리서치 보강 후 채움)
  - "Cursor + Colab" 조합은 한 문장으로만 언급 → 6장에서 본격
- **독자가 얻는 것:** GPU 없이도 ML 실험을 시작하는 가장 빠른 길을 안다.
- **예상 분량:** 약 18,000자
- **핵심 자료:** §2.2, §2.7, §3.2, §4.6, Colab FAQ·Pricing

### 6장. 에디터 안의 노트북 — VS Code, Cursor, 그리고 IDE 통합
- **핵심 질문:** 노트북이 별도 앱이 아니라 내 에디터 안에 들어오면 무엇이 달라지는가?
- **주요 내용:**
  - VS Code Notebooks가 `.ipynb`를 일급 시민으로 다루는 방식
  - 변수 탐색기·인라인 자동완성·MIME 렌더러(LaTeX/Plotly/Vega)·리팩토링
  - Pylance·디버거·Git이 한 창에 다 있을 때 생기는 워크플로우 변화
  - Cursor의 노트북 셀 안 Agent 모드(2025 업데이트 — 시점 명시)
  - "Cursor에서 코드 짜고 Colab GPU로 실행" 패턴 깊이 다루기 (5장 예고의 본편)
  - "언제 VS Code Notebooks가 JupyterLab보다 낫나" 결정 가이드
- **독자가 얻는 것:** 자기 에디터를 노트북 환경으로 승격시킬 수 있다.
- **예상 분량:** 약 18,000자
- **핵심 자료:** §2.3, §4.6 (Cursor + Colab 트렌드), VS Code Jupyter 공식 문서

### 7장. Marimo — 노트북을 다시 짜다
- **핵심 질문:** Jupyter 이후의 노트북은 무엇을 다시 짜고 있는가?
- **주요 내용:**
  - **다리 단락(1~2페이지):** 6장의 실용 톤(에디터 통합)에서 7장의 철학 톤(왜 새 노트북이 필요했나)으로 넘어가는 도입. "셀 임의 실행 → hidden state → 재현성 붕괴"라는 익숙한 고통을 한 번 더 환기.
  - **친척 그룹 짧은 박스(반 페이지):** Pluto.jl(Julia)·Observable(JS)이 같은 reactive 계보 — Marimo가 Python 진영의 답이라는 좌표 잡기.
  - reactive runtime의 정의: 셀 의존 그래프를 정적 분석으로 추적, 변경 시 다운스트림 자동 재실행
  - hidden state 원천 차단 메커니즘: 셀 삭제 시 변수도 메모리에서 삭제, 실행 순서 무관(위상정렬 보장)
  - `mo.ui.slider(1, 10, 0.1)` 미니 데모(§5.4) — 슬라이더 움직이면 다운스트림 셀 즉시 재실행. **API는 2026-05 기준이며 변할 수 있다, 핵심은 reactive 모델**이라는 메타 문장 한 줄.
  - `.py` 저장 = git-friendly, `python my_notebook.py`로 스크립트 실행, `marimo run`으로 즉시 웹 앱
  - WASM(Pyodide) 빌드: 브라우저에서 설치 없이 실행 (`marimo.app`)
  - 관점 균형: A(차세대 표준 가능성) vs B(Jupyter 생태계 너무 깊어 대체 어려움)
  - "언제 Marimo를 고를 것인가" — 새 프로젝트·재현성 최우선·앱 배포까지 한 도구로
- **독자가 얻는 것:** reactive 노트북의 작동 원리와 Jupyter와의 패러다임 차이를 손으로 잡는다.
- **예상 분량:** 약 17,000자
- **핵심 자료:** §2.4, §4.6, §5.4, Real Python·Pyodide·TDS의 Marimo 글, marimo docs(slider API)

### 8장. 팀과 엔터프라이즈의 노트북 — Deepnote, Hex, Databricks
- **핵심 질문:** 노트북이 1인 도구를 넘어 팀·기업의 데이터 작업대가 되면 어떤 모습인가?
- **주요 내용:**
  - **Deepnote:** Jupyter 호환 강조, Google Docs식 실시간 다중 편집, 셀 코멘트, 링크 공유의 단순함
  - **Hex:** 노트북 + SQL + no-code 스텝 + 인터랙티브 데이터 앱·스토리. 비기술 이해관계자에게 공유하는 "리포트" 측면. 브랜칭·리뷰 워크플로우 내장.
  - **Databricks:** Spark 클러스터 위 협업 노트북, 다언어 매직(`%sql`/`%scala`/`%python`/`%md`) — *"3장 매직이 다른 언어로 확장된 형태"라는 한 줄 콜백 명시*. MLflow·Delta Lake 통합, TB급 EDA·ETL.
  - **비용 함정 박스(반 페이지):** Databricks 클러스터를 켜둔 채 잊으면 한 달에 얼마인지, Colab Pro도 결국 누적되는 비용이라는 현실 감각
  - **친척 4종 마무리 단락(한 페이지):** Polynote(Netflix·Scala/Python/SQL/Vega 혼합·불변 모델)·nteract(데스크톱 앱·오프라인)·Apache Zeppelin(다언어 인터프리터·Git 빌트인·동시 한 언어 한계)·Observable(JS reactive·Python 1급 아님). 표 한 행씩.
  - **한국 사례 박스(반 페이지):** 한국 기업 데이터팀의 협업 노트북 도입기 — Deepnote/Hex/Databricks 중 어느 쪽이 어떤 맥락에서 채택되는지 (리서치 보강 후 채움)
  - **챕터 끝 — 책의 시그니처 인포그래픽 두 개:**
    - **결정 트리 (leaf node 8개 확정, 아래 "핵심 결정사항 메모" 참조)**
    - **환경 비교표 (9개 환경 × 6 컬럼 = 54셀, 아래 "핵심 결정사항 메모"에서 셀별 내용 확정)**
- **독자가 얻는 것:** 팀·엔터프라이즈 맥락의 노트북 선택지를 한눈에 본다. 그리고 책 전체의 환경 9개에서 자기 작업에 어느 도구를 고를지 결정 트리로 답할 수 있다.
- **예상 분량:** 약 19,000자 (인포그래픽 두 개 포함)
- **핵심 자료:** §2.5, §2.6, §2.8, §3.2 후반, Deepnote 비교 페이지 묶음, KDnuggets Polynote, DataScienceNotebook 비교

### 9장. Hidden State와 재현성 — 노트북의 가장 큰 그림자
- **핵심 질문:** 왜 내 노트북은 어제는 됐는데 오늘은 안 되는가, 그리고 어떻게 막을 것인가?
- **톤 디렉션:** **진지한 평어체. 청유형은 2~3회 이하로 절제하고, 등장 위치를 "방어선 6가지" 해법 단락으로 한정한다.** "한번 따라가보자" 정도의 무게 있는 청유형은 가능, "헤헤 어렵지?" 류의 가벼운 톤은 금지. 수사적 질문은 진단 단락에서만(예: "왜 우리는 매번 이 함정에 걸릴까?"). Pimentel 수치와 Joel Grus 비판의 무게가 깎이지 않도록 한다.
- **주요 내용:**
  - Pimentel 2019 충격 수치: 1.4M개 노트북 중 24.11%만 에러 없이 실행, 4.03%만 동일 결과 재현 — 그래프 한 장으로
  - 진단: "보이는 코드 ≠ 메모리 상태"의 해부
  - Joel Grus "I don't like notebooks"(JupyterCon 2018) 정면 인용 — 무엇을 비판했고, 어디는 수긍할 만한가
  - 옹호 진영(Netflix Notebook Innovation)의 답
  - **세 갈래 해법 비교(이 챕터의 균형추):**
    - **Reactive 진영:** Marimo·Pluto·Polynote·Observable — 의존 그래프로 hidden state 원천 차단 (7장 회수)
    - **Lineage 진영 — NBSafety 단락(한 단락):** 정적 분석 기반 fine-grained lineage tracking으로 hidden state 검출. reactive와 다른 갈래(런타임 변경 없이 Jupyter 위에 얹는다)임을 명시. 메커니즘 디테일은 각주.
    - **습관 진영:** "Restart and Run All" + 작은 노트북 단위 + 함수 외부 모듈 추출
  - 실무자의 방어선 6가지: Restart and Run All 습관, 작은 노트북 단위, 함수 외부 모듈 추출, requirements 핀, 마크다운 서사, percent format 저장
  - §5.7 리팩토링 예제로 마무리
- **독자가 얻는 것:** hidden state를 두려워하지 않게 된다 — 패턴으로 막을 줄 안다.
- **예상 분량:** 약 21,000자 (난이도 곡선의 정점)
- **핵심 자료:** §4.1 전체, §5.6, §5.7, Pimentel 논문 두 편, Joel Grus 영상, Netflix Tech Blog, NBSafety(JupyterCon 2020), GigaScience 생물의학 재현성 논문, ASE 2020 논문

### 10장. 노트북을 git, 협업, 자동화, 배포까지 끌어내기
- **핵심 질문:** 노트북을 1인 실험 도구를 넘어 팀·프로덕션·웹까지 데려가려면?
- **주요 내용:**
  - **git 문제:** `.ipynb` JSON 디프의 비참함 → Jupytext(percent .py)·nbdime(`nbdiff-web`)·ReviewNB 세 갈래 비교 (작업 흐름·강점·언제 쓸지 표)
  - **자동화:** Papermill 파라미터화 패턴(§5.3), Airflow `PapermillOperator`로 일자별 리포트, Netflix 사례 깊이 다루기
  - **프로덕션 논쟁** 정면: Ascend.io 반대 / Netflix 찬성 / 중도("코드는 모듈, 리포트·대시보드는 노트북")
  - **배포 4종 비교표 (이 챕터의 시그니처 인포그래픽):** Voila / Panel / Streamlit / Marimo를 다음 6축으로 — (1) **실행 모델**(콜백 vs reactive vs script-rerun), (2) **노트북 호환**(O/X), (3) **코드 노출**(숨김/선택/노출), (4) **위젯 라이브러리**(ipywidgets vs Bokeh vs 자체 vs 자체 reactive), (5) **사용 시점**(빠른 데모/복합 대시보드/프로토타입/노트북=앱), (6) **배포 난이도**
  - 위젯 분파: ipywidgets(콜백 기반)가 표준 → Voila가 코드 숨김 페이지화 → Panel이 복합 reactive → Streamlit이 별도 패러다임 → Marimo가 reactive 통합. **분류 축**: 콜백/reactive, 코드 노출, 노트북/스크립트 기반.
  - Voila(§5.8) 한 줄 배포 데모
  - **출판:** Quarto로 노트북 → HTML/PDF/EPUB/책 만들기 (`quarto render report.ipynb --to html`)
- **독자가 얻는 것:** 노트북을 "팀에서 살아남는 산출물"로 키울 수 있다.
- **예상 분량:** 약 22,000자
- **핵심 자료:** §3.4, §3.5, §3.6, §4.2, §4.3, §4.4, §4.5, §5.3, §5.5, §5.8, §2.9, ReviewNB Ultimate Guide, Quansight 대시보딩 비교, Quarto 공식

### 11장. 노트북을 잘 쓰는 사람 — 베스트 프랙티스와 2026 이후
- **핵심 질문:** 5년 뒤에도 살아남는 노트북 사용자가 되려면 지금 무엇을 익혀야 하나?
- **주요 내용:**
  - 커뮤니티 합의 베스트 프랙티스 종합(§4.2): imports 최상단, 함수 모듈 추출, 헤딩 구획, narrative, requirements 핀, Restart and Run All
  - 프로젝트 폴더 표준 구조(§5.7) — 노트북과 `src/`의 분리
  - **AI-네이티브 노트북** 흐름: Jupyter AI(ACP로 Claude/Codex/Copilot/Gemini — 시점 명시), Colab AI, Cursor, Marimo Pair
  - "Notebook Wars 2025": Marimo·Deepnote·Hex·Colab AI가 동시에 reactive·협업·AI로 방향 전환
  - 독자에게 권하는 다음 한 걸음 — 작업 유형별 추천 학습 경로
  - **닫는 말:** 도구는 계속 바뀐다. 책에서 익힌 멘탈 모델(셀·커널·상태·재현성·서사)이 도구를 가르는 안목으로 남는다.
- **독자가 얻는 것:** 책을 덮은 직후에 시작할 행동 한 가지가 명확해진다.
- **예상 분량:** 약 16,000자 (클로징답게 농밀하게)
- **핵심 자료:** §4.2, §4.6, §5.7, §5.10, Carpenter-Singh Lab Best Practices, Alex Hruska "Notebook Wars of 2025", Jupyter AI

### 부록 A. 환경 설정 미니 가이드 — pip / conda / venv / uv
- **핵심 질문:** 노트북을 시작하기 전에 Python 환경을 어떻게 만들 것인가?
- **주요 내용:**
  - 왜 환경 분리가 필요한가 — "전역 pip install의 무덤" 한 사례
  - **네 갈래 비교표:** pip(표준·최소) / venv(표준 격리) / conda(과학 패키지·바이너리·OS 통합) / uv(2024~ Rust 기반·빠름·통합 도구). 컬럼: 설치·격리·속도·바이너리 패키지·노트북과의 궁합·언제 쓸지.
  - 즉시 실행 명령 4종: `pip install jupyterlab` / `python -m venv .venv && .venv/bin/pip install jupyterlab` / `conda create -n nb jupyterlab && conda activate nb` / `uv tool install jupyterlab`
  - `requirements.txt` / `environment.yml` / `pyproject.toml` 차이 한 페이지
  - 노트북 안에서 환경 점검: `!which python`, `import sys; sys.executable`, `%pip install`(`!pip` 대신 권장)
  - 4·5·6·7·8장 모두에서 한 줄 참조로 끌어올 수 있게 자기-완결적으로
- **예상 분량:** 약 6,000자
- **핵심 자료:** uv 공식 문서, Python venv 공식 문서, conda docs, §4.2 베스트 프랙티스의 requirements 핀 항목

---

## 핵심 결정사항 메모

### 결정 트리 — 8장 끝, leaf node 8개 확정

분기 기준은 6개 축의 조합으로 단순화한다: (1) 혼자/팀, (2) GPU 필요/불필요, (3) 데이터 규모(GB/TB), (4) 산출물 유형(EDA/ML/리포트/출판/앱), (5) 재현성 우선순위, (6) 레거시 자산(기존 Jupyter 코드) 유무.

| # | 조건 | 추천 도구 | 이유 한 줄 |
|---|------|----------|-----------|
| 1 | 혼자 EDA + 로컬 + GPU 없음 | **JupyterLab** 또는 **VS Code Notebooks** | 표준 환경·확장 생태계, 또는 이미 쓰는 에디터 통합 |
| 2 | 혼자 ML 실험 + GPU 필요 | **Google Colab** 또는 **Kaggle Notebooks** | 무료 GPU·설치 0초, Kaggle은 데이터셋 마운트 한 클릭 |
| 3 | 팀 협업 + 비기술 이해관계자에게 결과 공유 | **Hex** | 리포트·스토리·no-code 스텝, 브랜칭·리뷰 워크플로우 |
| 4 | 팀 협업 + 가벼운 셀 코멘트만 필요 | **Deepnote** | Jupyter 호환·실시간 편집·링크 공유의 단순함 |
| 5 | TB급 데이터 + Spark 인프라 | **Databricks** | Spark·MLflow·Delta Lake가 노트북과 한 몸 |
| 6 | 출판물(책·논문·웹사이트) 산출 | **Quarto** (입력은 Jupyter) | cross-ref·citation·다출력, `quarto render` 한 번 |
| 7 | 재현성 최우선 + 새 프로젝트 | **Marimo** | reactive runtime이 hidden state 원천 차단, `.py` 저장으로 git·앱 배포까지 |
| 8 | 재현성 최우선 + 레거시 Jupyter 자산 | **Jupytext + nbdime + Restart and Run All 습관** | 런타임 교체 없이 percent format·content-aware diff·검증 루틴으로 보강 |

추가 분기 메모: GPU 필요하지만 무료 한도 초과 → Colab Pro/Pro+ 또는 로컬 GPU + JupyterLab. 오프라인·에어갭 환경 → JupyterLab 또는 VS Code(로컬 Jupyter Server). Julia/R 비중 큼 → JupyterLab(다언어 커널) 또는 Pluto.jl(Julia, reactive 친척).

### 환경 비교표 — 8장 끝, 9개 환경 × 6 컬럼 = 54셀 확정

| 환경 | 저장 포맷 | 실행 모델 | 협업 | 가격 (2026-05) | 강점 | 약점 |
|------|----------|----------|------|---------------|------|------|
| **JupyterLab** | `.ipynb` (JSON) | 셀 단위 임의 실행, 단일 커널 | 단일 사용자 (JupyterHub로 다중) | 오픈소스, 무료 | 표준·확장 생태계·다언어 | hidden state, JSON git diff |
| **VS Code Notebooks** | `.ipynb` (JSON) | 셀 단위 + IDE 도구 통합 | Live Share 가능, 비실시간 | VS Code 무료, Cursor 유료 | 변수 탐색기·Pylance·디버거·리팩토링 | UI가 IDE에 종속 |
| **Google Colab** | `.ipynb` (Drive 호스팅) | 셀 단위, 클라우드 커널 | 링크 공유·동시 편집 | Free / Pro $11.99 / Pro+ $49.99 | 무료 GPU/TPU, 설치 0초, AI Agent | 세션 ~12h, 피크 시 GPU 거부 |
| **Kaggle Notebooks** | `.ipynb` (Kaggle 호스팅) | 셀 단위, 클라우드 커널 + 데이터셋 마운트 | fork·복제, 공개 댓글 | 무료 (가입 필요) | 데이터셋 한 클릭, 학습·경연 자료 풍부 | 외부 인터넷 제한, 환경 커스텀 약함 |
| **Marimo** | `.py` (순수 스크립트) | reactive (의존 그래프 자동 재실행) | 단일 사용자 (git 친화) | 오픈소스, 무료 | hidden state 원천 차단, 앱·스크립트 동시, WASM | 생태계 신생, Jupyter 확장 비호환 |
| **Deepnote** | `.ipynb` 호환 (클라우드) | 셀 단위, 클라우드 커널 | 실시간 다중 편집·셀 코멘트 | Free / 유료 플랜 (시점 변동) | Jupyter 호환·링크 공유 단순함, AI 어시스턴트 | 클라우드 종속, 가격 변동성 |
| **Hex** | 자체 포맷 (`.ipynb` 임포트) | 셀 + SQL + no-code 스텝 + reactive | 실시간 편집·코멘트·브랜칭·리뷰 | 유료 중심 (Free 한정) | 리포트·앱·스토리, 브랜칭 워크플로우 | Jupyter 호환 약함, 학습 곡선 |
| **Databricks Notebooks** | `.dbc` / `.ipynb` 가져오기 | Spark 클러스터, 다언어 매직 | 자동 버저닝·동시 편집·코멘트 | 클러스터 사용량 종량제 (커뮤니티 에디션 무료) | TB급·MLflow·Delta Lake 일체화 | 비용 함정, 일반 EDA엔 과한 인프라 |
| **Quarto** | `.ipynb` 또는 `.qmd` | 입력 받아 렌더 (실행은 Jupyter 위임) | git 기반 | 오픈소스, 무료 | 출판 품질·다출력(HTML/PDF/EPUB/책)·cross-ref | 인터랙티브 개발 환경 아님 |

### 비교표·결정 트리·기타 인포그래픽 위치

- **8장 끝:** 환경 9개 결정 트리(8 leaf) + 환경 비교표(54셀) — 책의 시그니처 두 개
- **10장:** 배포 4종(Voila/Panel/Streamlit/Marimo) 비교표 6축, git 협업 도구 3종(Jupytext/nbdime/ReviewNB) 비교표
- **6장:** VS Code vs JupyterLab 가이드(짧은 표)
- **5장:** Colab 무료/Pro/Pro+ 가격표(2026-05 시점 명시)
- **부록 A:** pip/venv/conda/uv 4종 비교표

### 가장 긴 챕터·난이도 곡선

- **가장 긴 챕터:** 10장(약 22,000자, git·자동화·프로덕션·배포·출판이 모두 들어감), 9장(약 21,000자, hidden state 정점)
- **난이도 곡선**
  - 평탄 구간: 1~3장 (개념·해부학·도구상자) — 2장 본문이 가벼워졌으므로 3장으로의 톤 점프 해소
  - 완만한 상승: 4~6장 (환경 투어·워크플로우 레시피)
  - 한 단 상승: 7장(Marimo의 reactive 철학) — 6장 실용 톤에서 7장 도입의 다리 단락으로 완충
  - 능동적 선택 강요: 8장 끝 결정 트리
  - **정점:** 9장 (Pimentel 수치·Joel Grus 비판·세 갈래 해법) — 진지한 평어체로 무게 유지
  - 종합 하강: 10~11장 (실무 응용·전망)

### 시점 명시 의무 항목

- Colab 가격 (5장) — "2026년 5월 기준"
- Cursor 기능·Agent 모드 (6장) — "2025 업데이트 기준"
- Marimo `mo.ui.slider` API (7장) — "2026-05 기준, API는 변할 수 있다"
- Notebook v6/v7/`nbclassic` 상태 (4장) — "2026 기준" (v2 신규)
- Marimo Pair (11장) — "2025 발표"
- Notebook Wars 2025 (11장) — 시점 표기
- Jupyter AI ACP 통합 모델 명단 Claude/Codex/Copilot/Gemini (11장) — "2026-05 기준" (v2 신규)
- Deepnote/Hex 가격 (8장) — 변동성 큰 항목, 시점 표기

### 복선·호응 구조

- 2장 끝에서 "상태(state)" 개념을 심어둠 → 9장에서 hidden state로 회수
- 2장 본문에서 뺀 ZeroMQ 5소켓·메시지 스키마는 2장 Box A로 호기심 독자만 진입
- 3장에서 percent format·Jupytext 첫 등장 → 10장에서 git 정상화 도구로 본격 사용
- 3장 매직 베스트 8 → 8장 Databricks 절에서 "다른 언어로 확장된 형태"라는 한 줄 콜백
- 5장에서 Cursor + Colab 워크플로우 한 문장 언급 → 6장에서 깊이 다룸 (5장 분량 감축)
- 7장 Marimo의 hidden state 차단 메커니즘 → 9장에서 "reactive 진영의 답"으로 회수
- 8장 결정 트리 → 11장에서 "도구 안목"으로 승화

### 한국 사례·여백 보강 지점 (리서치 §7-1과 연동)

- **5장 한국 사례 박스(반 페이지):** 한국 학습자의 Colab 첫 모델 경험 (velog/OKKY 인용)
- **8장 한국 사례 박스(반 페이지):** 한국 기업 데이터팀의 협업 노트북 도입기
- **4장 보안 박스(반 페이지):** 멀티테넌트 노트북 보안은 "범위 밖" 명시 + 1차 자료 링크
- **8장 비용 함정 박스(반 페이지):** Databricks 클러스터 비용 감각

### Toby 스타일 적용 포인트

- 1장과 11장은 감정선이 가장 강함 — 평어체·청유형·수사적 질문이 자연스럽다
- 2~3장은 해부학이라 담담한 어조 우세, "보자", "한번 같이 따라가자" 같은 청유형으로 거리 좁히기. 2장이 가벼워졌으므로 톤 점프 해소.
- 7장은 reactive 철학을 다루므로 약간의 도발·확신 있는 어조 가능 — "이게 답일 수도 있겠다"의 톤
- 8장은 인포그래픽 중심이라 산문 비중 적음 — 캡션과 도입·정리 단락에 톤 집중
- **9장은 "진지한 평어체"** (v2 핵심 디렉션) — 청유형 2~3회 이하로 절제, 등장 위치를 "방어선 6가지" 해법 단락으로 한정. 가벼운 톤 금지. 수사적 질문은 진단 단락에서만, 무게 있는 형태로 ("왜 우리는 매번 이 함정에 걸릴까?" O / "헤헤 어렵지?" X). Pimentel 24.11%·Joel Grus 비판의 무게 유지.

### 챕터 독립성

4·5·6·7·8장은 단독으로도 읽힌다(특정 환경만 궁금한 독자 대응). 4·5·6·7·8장 모두 부록 A를 한 줄 참조로 가져오므로 환경 설정에서 막히지 않는다. 9~10장은 앞 챕터의 기반(특히 2·3·7·8장)을 전제로 읽는 게 자연스러움 — 챕터 도입에 짧은 "전제" 박스 두기.
