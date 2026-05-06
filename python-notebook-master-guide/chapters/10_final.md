# 10장. 노트북을 git, 협업, 자동화, 배포까지 끌어내기

PR 리뷰를 부탁받았다고 해보자. 동료가 보낸 PR을 GitHub에서 연다. 변경 파일에 `analysis.ipynb`가 보인다. 클릭해서 diff를 본다. 그러면 이런 게 나온다.

```diff
   "outputs": [
    {
     "data": {
-     "text/plain": "<Figure size 432x288 with 1 Axes>"
+     "text/plain": "<Figure size 640x480 with 1 Axes>"
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
-     "image/png": "iVBORw0KGgoAAAANSUhEUgAAA..."
+     "image/png": "iVBORw0KGgoAAAANSUhEUgAAB..."
     },
```

수천 줄이 그런 식이다. base64로 인코딩된 이미지가 한 줄로 늘어서 있고, 메타데이터의 일부가 미세하게 바뀐 것까지 다 diff에 잡힌다. 정작 동료가 무슨 코드를 어떻게 바꿨는지는 어디 있는지 안 보인다.

리뷰는 결국 "LGTM"으로 끝난다. 진짜로 보고 승인한 게 아니라 못 보고 포기한 것이다. 노트북의 git 비참함은 거의 모든 데이터팀이 한 번씩은 겪고, 그 다음부터는 노트북을 git에 올리지 않거나 PR 리뷰를 형식으로만 굴리거나 둘 중 하나로 흘러간다.

이 비참함이 노트북의 기술적 결함만은 아니다. 9장에서 본 hidden state 문제와 짝을 이루는, 노트북이 1인 도구로 머물 수밖에 없게 하는 구조적 마찰이다. git 위에서 협업이 안 되는 도구는 팀의 작업대로 격상될 수 없다. 자동화 파이프라인의 단위가 될 수 없다. 프로덕션 시스템의 산출물이 될 수 없다. 모든 것이 git의 정상화에서 출발한다.

이 장은 그 비참함을 정상화하는 길에서 시작한다. 그 다음에 노트북을 자동화 파이프라인에 넣고, 프로덕션에서 어디까지 쓸지를 두고 갈라진 논쟁을 정면으로 다루고, 노트북을 웹 앱·대시보드·출판물로 키우는 길까지 따라간다. 노트북을 1인 도구에서 팀과 시스템의 산출물로 끌어올리는 여정이다. 9장이 노트북의 그림자를 드러낸 장이라면, 10장은 그 그림자를 인정한 채 노트북을 더 멀리 데려가는 장이다.

## 1. `.ipynb` 디프 비참함을 살려내기

문제부터 정확히 짚자. `.ipynb`는 JSON 문서다. 셀의 코드, 셀의 출력, 메타데이터가 한 파일에 모두 직렬화된다. 출력에는 텍스트뿐 아니라 PNG 이미지의 base64, 셀 실행 횟수, 커널 사양, 노트북을 마지막으로 저장한 시각 같은 정보까지 들어간다. 이 모든 것이 한 줄짜리 JSON 값으로 묶여 있다.

git diff는 텍스트 라인 단위로 변화를 보여준다. JSON의 한 줄짜리 base64 값은 하나만 바뀌어도 한 줄 통째로 빨갛고 다음 줄이 통째로 초록이다. 사람이 읽을 수 있는 형태가 아니다.

해법은 세 갈래로 나와 있다.

이 문제가 단순히 "diff가 못생겼다"의 수준에서 끝나면 차라리 견딜 만하다. 진짜 문제는 다음에 따라온다. **머지 충돌**. 두 사람이 같은 노트북의 다른 셀을 동시에 수정하면 git이 머지를 시도한다. JSON 구조의 한 줄짜리 값에 충돌이 나면 git은 충돌 마커(`<<<<<<<`, `=======`, `>>>>>>>`)를 그 자리에 박는다. 그 마커가 박힌 `.ipynb`는 더 이상 유효한 JSON이 아니다. Jupyter가 노트북을 못 연다. 두 사람의 작업이 한꺼번에 깨진다.

이 사고가 한 번 나면 팀은 트라우마를 얻는다. 다음부터는 노트북을 동시에 만지지 않으려 하고, 한 사람만 만지는 도구로 격리된다. 협업이 사라진다. git 비참함의 진짜 비용은 이 격리에 있다.

해법은 세 갈래로 나와 있다.

### Jupytext — 노트북을 코드로 같이 저장하기

가장 가벼운 해법이다. 9장에서 잠깐 본 percent format을 본격적으로 도입한다. Jupytext를 설치하면 노트북을 `.ipynb`와 `.py` 두 파일로 동시에 저장하도록 설정할 수 있다.

```bash
pip install jupytext
```

JupyterLab에서는 노트북을 열고 명령 팔레트에서 "Pair Notebook with percent Script"를 누르면 된다. 그 순간부터 노트북 옆에 같은 이름의 `.py` 파일이 자동으로 생긴다. `.ipynb`를 저장하면 `.py`도 같이 갱신되고, `.py`를 텍스트 에디터에서 수정해도 `.ipynb`가 다음에 열릴 때 동기화된다.

`.py` 쪽은 이렇게 생겼다.

```python
# %% [markdown]
# # 데이터 로드와 전처리

# %%
import pandas as pd
df = pd.read_csv("sales.csv")
df.head()

# %% [markdown]
# ## 결측치 점검

# %%
df.isna().sum()
```

이 파일을 git에 커밋하면, diff가 일반 Python 코드처럼 한 줄씩 의미 있는 형태로 나온다. PR 리뷰가 가능해진다.

여기서 흔히 묻는 질문이 있다. "그러면 `.ipynb`는 git에서 제외해야 하나?" 답은 팀 컨벤션에 따라 갈린다. 두 가지 패턴이 있다.

첫째, **`.py`만 커밋하고 `.ipynb`는 `.gitignore`**. 가장 깔끔하다. PR 리뷰는 `.py`로 보고, 노트북을 받아본 사람은 Jupytext가 `.py`를 다시 `.ipynb`로 변환해서 연다. 단점은 노트북의 출력(차트, 표)이 git 저장소에 남지 않는다는 점이다.

둘째, **둘 다 커밋하되 `.ipynb`는 출력을 비우고 커밋**. nbstripout 같은 도구가 pre-commit 훅에서 `.ipynb`의 셀 출력을 자동으로 비워준다. PR 리뷰는 `.py`로 보고, 노트북 자체는 출력 없이 깔끔하게 보존된다. 단점은 약간의 설정 부담이 있다는 것.

어느 패턴이든 핵심은 같다. **사람이 읽을 수 있는 형태가 git에 들어간다.**

### nbdime — 노트북을 노트북으로 보면서 디프하기

`.ipynb`를 그대로 두고 싶은 경우도 있다. 출력까지 보존해야 한다든지, 팀이 Jupytext 도입을 안 받아들인다든지. 이 경우 두 번째 해법이 nbdime이다. Jupyter Project가 직접 만든 도구다.

```bash
pip install nbdime
nbdime config-git --enable --global
```

이 두 줄이 git에 nbdime을 등록한다. 그 다음부터 `git diff notebook.ipynb`를 치면 raw JSON이 아니라 셀 단위로 의미 있는 diff가 터미널에 뜬다. 코드 셀의 변경, 마크다운의 변경, 셀 추가·삭제가 사람이 읽을 수 있는 형태로 나온다.

브라우저에서 더 보기 좋게 비교하려면 `nbdiff-web`을 쓰면 된다.

```bash
nbdiff-web a.ipynb b.ipynb
```

브라우저가 열리고 두 노트북이 나란히 떠서 셀별로 변경 사항이 표시된다. 차트 출력의 변경까지 시각적으로 비교할 수 있다.

머지 충돌이 났을 때는 `nbmerge-web`이다. 일반 git 머지가 JSON 충돌 마커를 박아 노트북을 깨뜨리는 일이 흔한데, `nbmerge-web`은 셀 단위로 충돌을 보여주면서 사람이 결정할 수 있게 한다.

nbdime의 가치는 **`.ipynb`를 그대로 두면서도 협업을 가능하게 한다**는 것이다. Jupytext로 가는 게 더 깔끔하지만, 팀 사정상 그러지 못할 때 두 번째 안전선이 된다.

### ReviewNB — PR 리뷰를 노트북답게

세 번째 해법은 GitHub PR 자체를 노트북답게 만든다. ReviewNB라는 GitHub 마켓플레이스 앱이다. 저장소에 설치하면 PR에 노트북 변경이 있을 때마다 ReviewNB 탭이 따로 생긴다. 그 탭에서는 노트북이 노트북답게 — 셀별로, 차트는 차트로, 마크다운은 마크다운으로 — 렌더링된다. 셀 옆에 인라인 코멘트도 달 수 있다. PR 리뷰의 표준 워크플로우 그대로다.

ReviewNB는 무료 플랜이 있고, 큰 팀은 유료 플랜으로 전환한다. 회사가 GitHub 외 도구(Bitbucket, GitLab)를 쓰면 적용 범위가 제한된다.

세 갈래를 한 표로 정리하자.

| 도구 | 작업 흐름 | 강점 | 언제 쓸지 |
|------|----------|------|----------|
| **Jupytext** | `.ipynb`와 `.py`를 짝으로 저장, `.py`를 git에 | diff·머지가 일반 코드처럼, 가장 깔끔 | Python 코드 PR 리뷰 흐름이 자리 잡힌 팀 |
| **nbdime** | `.ipynb` 그대로, git 명령에 noteobok-aware diff 후크 | 출력까지 보존, 시각적 비교 | `.ipynb`를 못 버리는 팀 |
| **ReviewNB** | GitHub PR에 노트북 탭 추가 | 노트북답게 렌더링·인라인 코멘트 | GitHub 중심 팀, 무료 플랜으로 시작 가능 |

세 가지를 다 쓸 수도 있다. Jupytext로 일상 diff를 살려내고, 출력 중심 노트북에는 nbdime을 곁들이고, 팀 PR 리뷰 문화에 ReviewNB를 깔면 협업의 기반이 한 번에 정상화된다.

ReviewNB의 *Git and Jupyter Notebooks: The Ultimate Guide* 글이 이 세 가지의 조합을 잘 정리하고 있다. 핵심은 **각 도구가 푸는 문제의 층위가 다르다**는 점이다. Jupytext는 저장 형식 자체를 바꿔 git의 텍스트 diff가 잘 작동하게 만든다. nbdime은 git 명령에 노트북을 이해하는 후크를 끼워서 `.ipynb` 그대로도 의미 있는 diff를 만든다. ReviewNB는 GitHub PR이라는 워크플로우 안에서 노트북답게 렌더링되는 리뷰 인터페이스를 제공한다. 셋이 같은 문제를 다른 자리에서 풀고 있어서 충돌하지 않는다.

작은 팀이 가장 빨리 도입할 수 있는 조합은 **Jupytext + nbdime**이다. 둘 다 오픈소스고 설치가 한 줄이다. 이 조합이 자리잡으면 PR 리뷰의 90%는 정상화된다. 나머지 10%(시각적 비교가 정말 필요한 경우)에 ReviewNB나 `nbdiff-web`을 쓰면 된다.

## 2. 자동화 — Papermill 패턴

git이 정리되면 다음 욕심이 생긴다. **노트북을 사람이 매번 손으로 돌리지 않고 자동으로 돌리고 싶다.** 매일 아침에 어제 매출 리포트를 자동으로 생성한다든지, 한국·일본·미국 세 지역에 같은 분석을 돌려 세 개의 리포트를 동시에 만든다든지.

이 욕심에 답하는 도구가 Papermill이다. Netflix가 만들었고 nteract 조직에서 관리하고 있다. 핵심 아이디어는 한 줄이다. **노트북을 함수처럼 다룬다.** 함수에 인자를 넘기듯이 노트북에 파라미터를 넘기고, 함수 호출 결과를 받듯이 실행된 노트북을 산출물로 받는다.

### 노트북을 파라미터화하기

먼저 노트북 안에서 파라미터로 받을 셀을 표시한다. JupyterLab에서 셀 메타데이터에 `tag: "parameters"`를 단다. 셀 내용은 이렇게 시작한다.

```python
# tag: parameters
date = "2026-01-01"
region = "all"
alpha = 0.5
```

이 셀에 들어 있는 변수들이 Papermill의 외부 입력 파라미터가 된다. 셀 안에 적힌 값들은 기본값이다. 노트북을 수동으로 열어서 작업할 때는 이 기본값으로 동작한다.

### Papermill로 실행하기

CLI에서:

```bash
pip install papermill

papermill report_template.ipynb output_kr.ipynb \
  -p date 2026-05-06 \
  -p region kr
```

이 명령은 `report_template.ipynb`를 읽어 `parameters` 태그가 붙은 셀의 변수를 `-p` 옵션으로 덮어쓴 뒤 실행한다. 실행이 끝나면 `output_kr.ipynb`에 결과가 저장된다. 이 결과 노트북에는 모든 셀의 출력이 그대로 박혀 있다. 차트, 표, 로그까지.

Python API로도 같은 일을 할 수 있다.

```python
import papermill as pm

regions = ["kr", "jp", "us"]
date = "2026-05-06"

for region in regions:
    pm.execute_notebook(
        "report_template.ipynb",
        f"reports/report_{date}_{region}.ipynb",
        parameters={"date": date, "region": region, "alpha": 0.6}
    )
```

세 지역에 대해 같은 노트북을 세 번 돌리고, 결과 노트북 세 개가 `reports/` 폴더에 떨어진다. 각 결과 노트북은 그 자체로 산출물이다. 누군가가 그걸 열어서 차트를 보고, 마크다운 서사를 읽고, "이 분석이 어떻게 만들어졌는지"를 그대로 따라갈 수 있다.

### Airflow와 결합하기

이 패턴이 Apache Airflow와 결합되면 본격적인 데이터 파이프라인이 된다. Airflow는 `PapermillOperator`를 제공한다.

```python
from airflow import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator
from datetime import datetime

with DAG(
    "daily_sales_report",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
) as dag:
    for region in ["kr", "jp", "us"]:
        PapermillOperator(
            task_id=f"report_{region}",
            input_nb="/notebooks/report_template.ipynb",
            output_nb=f"/reports/{{{{ ds }}}}/{region}.ipynb",
            parameters={"date": "{{ ds }}", "region": region},
        )
```

매일 자정에 세 지역에 대한 노트북이 자동으로 실행되고, 결과는 날짜별 폴더에 떨어진다. Airflow의 UI에서 어떤 날짜의 어떤 지역이 실패했는지 한눈에 본다. 실패한 노트북을 클릭해 열면 어디서 어떤 에러가 났는지 셀 단위로 확인할 수 있다.

### Netflix의 답을 다시 보기

이게 9장에서 본 Netflix의 답이 실제로 어떻게 작동하는지의 모습이다. Netflix Tech Blog의 "Notebook Innovation" 글, Data Engineering Podcast Ep. 54의 Matthew Seal 인터뷰가 그 풍경을 잘 설명하고 있다. 정리하면 이렇다.

Netflix는 데이터 사이언티스트, ML 엔지니어, 데이터 엔지니어, 분석가가 모두 노트북을 자기 작업의 1차 인터페이스로 쓴다. 그러나 그 노트북들은 1인의 즉흥 도구가 아니다. 모두 컨테이너 안에서 실행되고, Papermill로 파라미터화돼 있고, 출력 노트북이 산출물로 보존된다. 어떤 노트북은 일자별 ETL 모니터링 리포트로 매일 자동 실행되고, 어떤 노트북은 ML 학습 결과를 시각화하는 대시보드의 백엔드로 작동하고, 어떤 노트북은 사람이 인터랙티브하게 들여다보는 분석 작업대다.

이 풍경에서 hidden state는 통제된다. 컨테이너에서 처음부터 끝까지 한 번에 실행되니 셀 임의 순서 같은 게 없다. 입력은 명시적으로 파라미터로 주어진다. 출력 노트북은 불변 아카이브가 된다. 9장에서 본 6가지 방어선 중 절반 이상이 자동화 파이프라인 자체에 내장돼 있다.

다만 이 답을 그대로 따라가는 것은 작은 팀에는 무겁다. Airflow 클러스터를 깔고, 컨테이너 빌드 파이프라인을 만들고, 노트북 템플릿 표준을 만들고, 출력 노트북 저장소를 운영해야 한다. Netflix는 그걸 할 만한 규모다. 작은 팀은 가벼운 시작이 가능하다. 일단 노트북 한 개를 Papermill로 파라미터화해서 cron에 한 줄 거는 것부터다. 그 작은 시작이 자기 팀의 첫 자동화 파이프라인이 된다.

가벼운 시작의 한 예를 보자. 매일 아침 매출 리포트를 자동 생성하고 싶다고 해보자. 다음 한 줄을 cron에 등록한다.

```cron
0 7 * * * cd /home/team/reports && papermill template.ipynb \
  outputs/$(date +\%Y-\%m-\%d).ipynb -p date $(date +\%Y-\%m-\%d) \
  >> log.txt 2>&1
```

매일 아침 7시에 `template.ipynb`가 그 날짜를 파라미터로 받아 실행되고, `outputs/2026-05-06.ipynb` 같은 파일이 떨어진다. 사람이 노트북을 열어 보거나, Jenkins·GitLab CI 같은 도구가 그 파일을 슬랙 채널에 업로드하거나, 정적 사이트로 빌드해서 사내 포털에 올릴 수도 있다.

이 작은 자동화 한 개가 자리잡으면 자연스럽게 다음 욕심이 생긴다. "여러 노트북을 의존 관계대로 순서대로 실행하고 싶다." 이 시점에 Airflow나 Prefect, Dagster 같은 워크플로우 오케스트레이터가 들어온다. 처음부터 Airflow를 깔지 않아도 된다. cron 한 줄에서 Airflow까지 가는 길은 자연스러운 진화의 흐름이다. 자기 팀의 규모와 필요에 맞춰 그 진화를 조절하자.

여기서 한 가지 함정을 짚어두자. Papermill 자동화가 자리잡으면 "이제 모든 노트북을 자동화 파이프라인으로 돌리자"는 충동이 생길 수 있다. 이 충동은 위험하다. 노트북에는 두 종류가 있다. **사람이 손으로 만지는 분석 노트북**과 **자동 실행되는 산출물 노트북**. 둘은 작성 방식이 달라야 한다. 분석 노트북은 자유롭게 셀을 늘리고 실험한다. 산출물 노트북은 처음부터 끝까지 한 번에 실행될 것을 가정하고, 파라미터로 입력을 받고, 출력이 결정론적이어야 한다. 두 종류를 한 노트북에 욱여넣으면 둘 다 잘 안 된다. 폴더 구조부터 둘을 분리하는 편이 낫다. `notebooks/`(분석)와 `pipelines/`(자동화)로.

## 3. 노트북 in 프로덕션 — 끝나지 않는 논쟁

자동화가 가능해졌다고 해서 노트북을 production 시스템 어디에나 가져다 써도 되는가. 여기서 큰 논쟁이 갈린다. 산업계 안에서 의견이 첨예하게 갈리는 주제다.

### 반대 진영 — Ascend.io의 단호한 답

Ascend.io 같은 데이터 파이프라인 회사는 명확하게 반대한다. 블로그 포스트 *Why You Shouldn't Use Notebooks for Production Data Pipelines*에 그 입장이 정리돼 있다. 핵심을 풀면 이렇다.

첫째, **셀 임의 실행이라는 본질이 production과 안 맞는다.** Production 코드는 결정론적이어야 한다. 같은 입력에 같은 출력. 같은 코드는 항상 같은 순서로 실행돼야 한다. 노트북은 본질적으로 그런 보장이 없는 매체다(Papermill로 컨테이너 자동 실행하면 보장된다고 반박할 수 있지만, 그 시점에는 이미 노트북을 노트북답게 쓰는 게 아니라 어색한 스크립트로 쓰는 셈이라는 게 이쪽의 재반박이다).

둘째, **통합 테스트가 어렵다.** 일반 Python 모듈에는 pytest를 붙일 수 있다. 노트북에는 어색하다. Papermill로 노트북을 통째로 실행하고 결과를 확인하는 식의 테스트는 가능하지만, 이건 단위 테스트라기보다 end-to-end 테스트에 가깝다. 빠른 피드백 루프가 안 만들어진다.

셋째, **스케줄링·모니터링·알림이 빈약하다.** Airflow와 결합할 수 있긴 하지만, Airflow의 task가 일반 함수일 때 얻을 수 있는 풍부한 메트릭·로깅·재시도·SLA 모니터링이 노트북 task에는 덜 자연스럽게 적용된다.

넷째, **파라미터화가 편의 기능 수준**. Papermill의 파라미터는 단순 변수 덮어쓰기다. Production 시스템에 필요한 환경별 설정 분리, 비밀 관리, 타입 검증 같은 영역은 별도로 짜야 한다.

이 진영의 결론은 한 줄이다. **"노트북은 분석을 위한 도구이고, production 파이프라인은 일반 Python 모듈로 짜야 한다."**

### 찬성 진영 — Netflix의 길

위에서 본 Netflix의 답이 찬성 진영의 정점이다. 노트북은 단순히 분석 도구가 아니라 **데이터·인프라·실험을 묶는 통합 인터페이스**다. Papermill로 자동화하면 production에서도 충분히 견딘다.

찬성 진영의 핵심 논점은 이렇다. **"production 시스템의 본질은 코드가 아니라 산출물이다."** 산출물이 일자별 리포트라면, 그 리포트를 어떤 형태로 만들어내는가가 본질이다. 일반 Python 모듈로 PDF를 만들 수도 있지만, 노트북으로 만들면 그 산출물 자체가 코드+서사+차트+표가 한 문서에 묶인 형태로 나온다. 산출물의 품질이 더 높다.

또 ML 파이프라인의 중간 점검 단계에서 노트북은 거의 비교 대상이 없다. 학습 데이터의 분포가 어떻게 변했는지, 모델의 메트릭이 시간에 따라 어떻게 움직이는지를 차트와 표로 매일 자동으로 보여주는 일은 노트북에 자연스럽다.

### 중도 진영 — 가장 현실적인 답

대부분의 팀이 실제로 자리잡는 곳은 중도다. 이 입장을 한 줄로 요약하면 이렇다.

> **"프로덕션 코드는 모듈로, 프로덕션 리포트·대시보드는 노트북으로."**

핵심 데이터 변환 로직, 모델 학습 로직, API 서버는 일반 Python 모듈로 짠다. pytest로 단위 테스트하고, mypy로 타입 체크하고, CI 파이프라인에 올린다. 노트북은 그 모듈들을 조합해서 **산출물**(리포트, 대시보드, 분석 결과)을 만드는 자리에서만 쓴다.

이 분리가 가능하면 두 진영의 비판이 둘 다 풀린다. Ascend의 비판은 **production 코드**를 향한 것이지 **production 산출물**을 향한 것이 아니다. Netflix의 옹호는 **산출물로서의 노트북**의 가치를 옹호한 것이지 **모든 코드를 노트북에**라는 주장은 아니다.

실무에서는 이 중도를 다음과 같은 폴더 구조로 표현한다.

```
project/
├── src/                    # production 코드 (모듈, 테스트 가능)
│   ├── data.py
│   ├── features.py
│   └── models.py
├── tests/                  # pytest 단위 테스트
│   └── test_features.py
├── notebooks/              # 분석·산출물용 노트북
│   ├── 01_eda.ipynb
│   └── 02_model_eval.ipynb
├── reports/                # Papermill 출력물 (자동 실행 결과)
│   └── 2026-05-06/
│       ├── kr.ipynb
│       └── jp.ipynb
└── pipelines/              # Airflow DAG 등 자동화
    └── daily_report.py
```

`src/`는 일반 Python 프로젝트처럼 다룬다. `notebooks/`는 사람이 손으로 만지는 작업대다. `reports/`는 자동으로 채워지는 산출물 아카이브다. 셋이 한 저장소 안에 살되 역할이 명확히 다르다.

이 구조가 잡히면 "노트북을 production에 써도 되나"라는 질문 자체가 사라진다. 답은 "어디에 어떻게 쓰는가에 따라 다르다"이고, 답을 폴더 구조가 대신 해주고 있기 때문이다.

중도 진영의 입장이 가장 현실적이라고 했지만, 이 입장에도 함정이 있다. **`src/`와 `notebooks/`의 경계가 흐려지기 시작하면 도로 옛날 노트북으로 회귀한다.** 노트북에서 작업하다가 "이 함수는 한 번만 쓰니까 그냥 노트북에 두자"가 누적되면 어느 순간 노트북이 다시 두꺼워진다. 함수가 노트북에 살게 되면 단위 테스트가 어려워지고 재사용이 안 된다. 9장의 hidden state 함정도 다시 살아난다.

그래서 중도 진영을 유지하려면 한 가지 규칙이 필요하다. **노트북 셀에서 정의한 함수가 두 번째 노트북에서 또 쓰이는 순간, 그 함수를 `src/`로 옮긴다.** 한 번 쓰고 마는 함수는 노트북에 둬도 된다. 두 번 쓰이는 순간 모듈이 된다. 이 규칙 하나로 경계가 자연스럽게 유지된다.

더 강한 팀은 한 단 더 간다. 노트북에는 함수 정의를 아예 두지 않는다. 모든 함수가 `src/`에 있고, 노트북은 `from src.data import load_data` 같은 import와 그 함수를 호출하는 코드, 그리고 마크다운 서사로만 구성된다. 이 패턴이 자리잡으면 노트북이 한결 가벼워지고, `src/`의 코드 품질이 자연스럽게 높아진다. 단점은 처음 도입할 때 마찰이 크다는 것. 작업자가 "노트북 안에서 빠르게 함수 정의하고 시험해 보고 싶은" 욕구를 통제해야 한다. 이 통제를 받아들일 만한 팀에서만 적용할 만한 패턴이다.

## 4. 배포 — 노트북을 웹으로 끌어내기

노트북의 다음 욕심은 배포다. 분석 결과를 동료에게 노트북 파일로 보내는 게 아니라 **링크 한 줄로 공유**하고 싶다. 비기술 이해관계자도 클릭만 하면 차트가 보이고 슬라이더를 움직일 수 있게 하고 싶다. 이 욕심에 답하는 도구가 네 개로 갈라져 있다.

도구를 보기 전에 분류 축부터 정리하자. 네 도구는 세 축으로 나뉜다.

- **실행 모델**: 콜백 vs reactive vs script-rerun
- **노트북과의 관계**: 노트북 파일을 그대로 받는가, 별도 스크립트인가
- **코드 노출**: 사용자에게 코드까지 보여주는가, 위젯·차트만 보여주는가

이 세 축이 네 도구의 성격을 결정한다.

### Voila — 노트북을 그대로 페이지로

Voila가 가장 가벼운 답이다. ipywidgets를 쓰는 노트북을 그대로 받아 코드 셀은 숨기고 위젯과 출력만 표시하는 정적 웹 페이지로 변환한다.

```bash
pip install voila
voila my_dashboard.ipynb
```

이 한 줄에 브라우저가 열리고 노트북이 페이지로 뜬다. 슬라이더를 움직이면 차트가 다시 그려진다(ipywidgets의 콜백이 그대로 작동한다). 코드는 안 보인다.

장점은 학습 곡선이 거의 없다는 것이다. 기존에 ipywidgets로 노트북에서 인터랙티브하게 만들어둔 것이 그대로 페이지가 된다. 배포할 때는 voila를 띄우는 작은 서버 한 대가 있으면 끝.

단점은 ipywidgets의 한계 그대로다. 콜백 기반이라 복잡한 상태 관리는 어색하다. UI 커스터마이징도 제한적이다. 빠른 데모, 단순 대시보드, 사내 공유에 잘 맞는다.

### Panel — 복합 reactive 대시보드

Panel은 HoloViz 진영의 답이다. Bokeh가 모태고, ipywidgets와도 호환된다. 더 복잡한 대시보드를 만들 수 있다.

```python
import panel as pn
import pandas as pd

df = pd.read_csv("sales.csv")
region_select = pn.widgets.Select(name="Region", options=list(df["region"].unique()))

@pn.depends(region_select.param.value)
def chart(region):
    sub = df[df["region"] == region]
    return sub.groupby("month")["amount"].sum().hvplot.bar()

pn.Column(region_select, chart).servable()
```

`@pn.depends`가 reactive 그래프를 만든다. `region_select`가 바뀌면 `chart`가 자동으로 다시 호출된다. ipywidgets의 단순 콜백보다 한 단 위의 추상화다.

배포는 `panel serve dashboard.py`로 한 줄. 노트북에서 만든 결과물을 그대로 가져갈 수도 있다. ipywidgets·Voila 콘텐츠와도 호환된다.

복합 대시보드, 여러 차트가 서로 연동되는 인터랙티브 분석 도구를 만들 때 가장 자연스럽다.

### Streamlit — 노트북식 사고로 짠 별도 스크립트

Streamlit은 다른 길을 간다. 노트북 호환을 포기했다. 별도의 `.py` 스크립트를 짠다. 그러나 그 스크립트는 노트북식 사고로 — 위에서 아래로 — 짠다.

```python
import streamlit as st
import pandas as pd

st.title("월별 매출")
df = pd.read_csv("sales.csv")
region = st.selectbox("Region", df["region"].unique())
st.bar_chart(df[df["region"] == region].groupby("month")["amount"].sum())
```

이 스크립트는 사용자가 위젯을 건드릴 때마다 **위에서 아래로 다시 실행된다**(script-rerun 모델). 처음 들으면 비효율적인 것 같지만, Streamlit은 캐시 데코레이터로 무거운 연산을 건너뛰게 해서 실용적인 속도를 낸다.

장점은 학습 곡선이 가장 짧다는 것. Python 코드를 위에서 아래로 짤 줄 알면 Streamlit 앱이 만들어진다. 빠른 프로토타입, ML 모델 데모, 사내 도구 스크래치에 가장 잘 맞는다.

단점은 노트북 호환이 없다는 것. 기존 노트북을 가져다 Streamlit 앱으로 옮기려면 다시 써야 한다. 또 script-rerun 모델은 복잡한 상태 관리에는 어색하다.

### Marimo — 노트북이 곧 앱

Marimo는 마지막 답이다. 7장에서 깊이 본 reactive 노트북. 노트북 자체가 그대로 앱이 된다.

```bash
marimo run my_notebook.py
```

이 한 줄에 노트북이 웹 앱으로 뜬다. 코드 셀은 옵션으로 숨길 수 있고, reactive runtime이 그대로 작동한다. 슬라이더를 움직이면 다운스트림 셀이 자동 재실행된다. WASM 빌드까지 하면 서버 없이 정적 사이트 호스팅으로 배포할 수 있다.

장점은 **하나의 도구로 노트북 작업부터 앱 배포까지 끝난다**는 것. Marimo로 EDA 작업을 하면 그 작업 결과가 그대로 사용자가 만지는 앱이 된다. 두 단계가 하나로 합쳐진다.

단점은 Marimo 생태계가 신생이고 Jupyter 확장과 비호환이라는 점.

### 네 도구를 한 표로

| 축 | Voila | Panel | Streamlit | Marimo |
|----|-------|-------|-----------|--------|
| **실행 모델** | 콜백 (ipywidgets) | reactive (`@depends`) | script-rerun | reactive (의존 그래프) |
| **노트북 호환** | O (`.ipynb` 직접) | O (`.ipynb` 가능) | X (별도 `.py`) | △ (Marimo는 자체 `.py`) |
| **코드 노출** | 숨김 (기본) | 선택 | 노출 안 됨 (앱이 별도) | 선택 |
| **위젯 라이브러리** | ipywidgets | Bokeh + ipywidgets | 자체 | 자체 reactive |
| **사용 시점** | 빠른 데모, 단순 대시보드 | 복합 reactive 대시보드 | 빠른 프로토타입, ML 데모 | 노트북 = 앱, 신규 프로젝트 |
| **배포 난이도** | 낮음 (voila 한 줄) | 중간 (panel serve) | 낮음 (streamlit run) | 낮음 (marimo run, WASM 가능) |

이 표가 결정에 도움이 된다. 기존 ipywidgets 노트북을 가장 빠르게 페이지로 → Voila. 복잡한 인터랙션이 얽히는 대시보드 → Panel. 노트북을 안 거치는 빠른 프로토타입 → Streamlit. 새 프로젝트에서 노트북과 앱을 한 번에 → Marimo.

위젯 분파의 계보를 한 번 더 짚어두자. 시작은 ipywidgets다. Jupyter 표준 위젯이고 콜백 기반이다. Voila가 그 위에 코드 숨김 페이지화 레이어를 얹었다. Panel이 같은 토대 위에서 더 복합적인 reactive 추상화를 제공했다. Streamlit이 노트북 호환을 버리고 별도 패러다임을 만들었다. Marimo가 reactive와 노트북을 통합했다. 이 다섯이 한 계보의 다섯 단계다. 어느 도구를 고르든 이 계보의 어디에 자신이 서 있는지를 알면 도구의 강약점이 자연스럽게 보인다.

Quansight가 *Dash, Voila, Panel, & Streamlit*이라는 비교 글에서 이 풍경을 잘 정리하고 있다. 그들의 결론을 거칠게 옮기면 이렇다. **단일 도구로 모든 경우를 다 잘 다룰 수 있는 도구는 없다.** Voila는 노트북을 그대로 페이지로 만드는 자리에서 가장 빠르고, Panel은 복합 인터랙션의 자리에서 가장 깊고, Streamlit은 빠른 프로토타입의 자리에서 가장 마찰이 적고, Marimo는 노트북-앱 일체화의 자리에서 가장 우아하다. 자기 작업이 어느 자리에 있는지를 정확히 알아야 도구를 고를 수 있다. 정확히 모르면 일단 가장 가벼운 Voila나 Streamlit으로 시작해보고, 한계가 보이는 시점에 다른 도구로 옮기면 된다.

배포 자체의 이야기도 한 번 짚어야 한다. 위 네 도구로 만든 앱·페이지를 누가 어디서 보는가. 가장 단순한 답은 사내 서버에 한 대 띄우고 사내 네트워크 안에서 접속하는 것. 더 무겁게 가면 Docker 컨테이너로 빌드해서 Kubernetes에 올리거나, Heroku·Railway·Render 같은 PaaS에 배포하거나, AWS·GCP·Azure의 컨테이너 서비스에 올린다. Marimo는 WASM 빌드를 지원하니 정적 사이트 호스팅(GitHub Pages, Netlify, Vercel)으로 끝낼 수도 있다. 배포 인프라의 깊이는 자기 팀의 인프라 역량에 맞춰 고르면 된다. 처음부터 Kubernetes를 떠올리지 말고, 사내 서버 한 대로 시작하는 게 가장 가벼운 길이다.

## 5. 출판 — Quarto로 노트북을 책·논문으로

마지막 길이 남았다. 노트북을 웹 앱이 아니라 **출판물**로 끌어내는 길이다. HTML 사이트, PDF 논문, EPUB 전자책, 정적 웹사이트, 책 한 권. 이 길의 답이 Quarto다.

Quarto는 R Markdown을 만든 Posit(구 RStudio)의 차세대 출판 시스템이다. 입력으로 `.ipynb`나 `.qmd`(Quarto 자체 마크다운)를 받아 다양한 출력 포맷으로 렌더링한다.

```bash
quarto render report.ipynb --to html
quarto render report.ipynb --to pdf
quarto render report.ipynb --to epub
```

세 명령이 같은 노트북에서 세 가지 다른 출력을 만든다. 코드 실행은 Jupyter에 위임한다(Quarto가 내부적으로 nbclient로 노트북을 실행한다). 그러니 노트북 작성자는 평소처럼 노트북을 짜고, Quarto는 그걸 출판 품질의 문서로 빚는다.

`nbconvert`와 무엇이 다른가. nbconvert는 단순 변환이다. 노트북 → HTML, 노트북 → PDF. 그 이상은 별로 없다. Quarto는 출판 시스템이다. cross-reference(이 그림은 그림 3.2다, 라고 자동 번호 매기기), citation(BibTeX과 결합), figure panel, callout, 수식 렌더링, 다국어 지원 같은 기능을 갖췄다. 학술 논문, 기술 책, 회사 리포트 — 진짜 출판물 품질을 목표로 한다.

여러 노트북을 묶어 책 한 권을 만드는 것도 가능하다. `_quarto.yml`에 챕터 순서를 정의하면 된다.

```yaml
project:
  type: book

book:
  title: "데이터 분석 가이드"
  chapters:
    - index.qmd
    - 01_intro.ipynb
    - 02_eda.ipynb
    - 03_modeling.ipynb
  output-file: "data-analysis-guide"

format:
  html:
    theme: cosmo
  pdf:
    documentclass: scrbook
  epub:
    cover-image: cover.png
```

`quarto render` 한 번으로 HTML 사이트, PDF 책, EPUB 세 가지가 동시에 빌드된다. 노트북 한 개당 한 챕터, 챕터들이 모여 책. 데이터 분석 회사가 사내 가이드북을 만들거나, 강의 자료를 책으로 묶거나, 기술 블로그를 정적 사이트로 빌드할 때 가장 자연스러운 흐름이다.

Quarto는 8장의 결정 트리에서 "출판물(책·논문·웹사이트) 산출"의 leaf node에 자리하고 있다. 노트북을 입력으로, 출판 품질의 산출물을 출력으로. 그 자리에서 Quarto의 자리는 거의 독보적이다.

Quarto의 가치를 한 번 더 짚어보자. 학술 논문을 쓰는 연구자에게 Quarto는 **분석과 출판이 한 도구로 묶인다**는 의미다. 데이터 분석을 노트북에서 하고, 그 노트북에 마크다운으로 본문을 쓰고, BibTeX으로 인용을 걸고, `quarto render report.ipynb --to pdf` 한 번으로 학술지 제출용 PDF가 나온다. 분석 결과가 본문 본인의 일부가 되고, 본문이 분석의 일부가 된다. 분리되어 있던 두 작업이 한 흐름이 된다.

기술 블로그를 운영하는 사람에게는 **다출력의 가치**가 크다. 같은 노트북에서 HTML 사이트(블로그 포스트), PDF(다운로드용), EPUB(전자책)이 동시에 빌드된다. `_quarto.yml`에 출력 포맷을 추가하기만 하면 된다. nbconvert로 같은 일을 하려면 출력 포맷마다 별도 명령을 짜고 후처리를 해야 한다. Quarto는 그 모든 것을 한 시스템으로 묶었다.

Posit이 Quarto를 발표했을 때 핵심 메시지가 *"language-agnostic scientific publishing system"*이었다. R, Python, Julia, Observable JS를 모두 입력으로 받는다. 이 다언어성이 R Markdown에서 Quarto로 넘어온 가장 큰 변화다. Python 노트북을 쓰는 사람도 이제 R Markdown 진영의 풍부한 출판 인프라를 그대로 쓸 수 있게 됐다. 이게 단순한 도구 갈아타기가 아니라 작업 흐름의 통합이다.

### Quarto의 한 가지 함정

마지막으로 Quarto의 함정을 한 가지 짚어두자. Quarto는 출판 시스템이지 개발 환경이 아니다. `quarto preview`로 라이브 미리보기는 가능하지만, JupyterLab이나 Marimo 같은 인터랙티브 개발 환경의 자리는 아니다. 노트북 작업은 평소대로 Jupyter나 VS Code에서 하고, **출판 단계에서만 Quarto를 호출**하는 게 자연스러운 흐름이다.

또 Quarto가 노트북을 출판할 때는 노트북을 처음부터 끝까지 한 번 실행한다(또는 캐시된 출력을 쓴다). 그 말은 노트북이 이미 "위에서 아래로 한 번에 실행되는" 형태여야 한다는 뜻이다. 9장의 hidden state 방어선이 적용된 노트북이라야 Quarto로 깔끔하게 출판된다. 노트북의 위생이 출판물의 품질을 결정한다.

## 마무리

이 장은 노트북이 1인 도구의 자리에서 벗어나는 다섯 가지 길을 따라왔다. 정리하면 이렇다.

**git**: Jupytext로 percent format 짝 저장, nbdime으로 노트북다운 diff, ReviewNB로 PR 리뷰 정상화. 셋 중 하나라도 도입하면 협업의 절반이 풀린다.

**자동화**: Papermill로 노트북을 함수처럼 다루고, Airflow의 PapermillOperator로 스케줄링. Netflix의 답이 그 정점이고, 작은 팀은 cron 한 줄에서 시작하면 된다.

**프로덕션 논쟁**: 반대(Ascend)·찬성(Netflix)·중도("코드는 모듈, 산출물은 노트북") 셋 중 어느 입장에 서더라도, 폴더 구조에 그 입장을 새기는 게 답이다. `src/`와 `notebooks/`와 `reports/`의 분리.

**배포**: Voila·Panel·Streamlit·Marimo 네 도구가 ipywidgets에서 reactive까지의 계보를 이룬다. 자기 작업이 어느 자리에 있는지를 알면 도구가 선택된다.

**출판**: Quarto가 노트북을 입력으로 받아 책·논문·HTML·PDF·EPUB을 빚는다. nbconvert가 안 닿는 출판 품질을 목표로 한다.

이 다섯 길을 알고 있으면 노트북은 더 이상 책상 위 1인 작업대가 아니다. 팀의 git 저장소에 사람이 읽을 수 있는 형태로 들어가고, 매일 자동으로 실행돼 산출물을 쌓고, 웹 앱으로 사내에 배포되고, 정기 리포트로 출판된다. 한 매체가 이렇게 멀리까지 갈 수 있다는 게, 노트북이라는 매체가 가진 가장 큰 가능성이다.

이 다섯 길을 다 한꺼번에 도입할 필요는 없다. 자기 팀의 가장 아픈 자리에서 시작하면 된다. PR 리뷰가 형식이라면 git 정상화부터. 같은 분석을 매주 손으로 돌리고 있다면 자동화부터. 분석 결과를 비기술 동료와 공유하는 게 어렵다면 배포부터. 학술지 제출이 임박해 있다면 출판부터. 어느 길로 들어가든, 한 길이 자리잡으면 다른 길도 자연스럽게 따라온다. 노트북을 끌어내는 일은 한 번의 큰 결정이 아니라 작은 선택의 누적이다.

다음 장은 책의 마지막 장이다. 베스트 프랙티스를 한 번에 정리하고, AI-네이티브 노트북의 흐름을 본 다음, 5년 뒤에도 살아남는 노트북 사용자가 되려면 무엇을 익혀둬야 하는지를 이야기한다.
