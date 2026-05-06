# 5장. 클라우드 노트북 — Colab과 Kaggle, GPU의 대중화

이런 상황을 한번 떠올려보자. 어느 주말 오후, 누가 던진 한마디 — "요즘 트랜스포머 한번 돌려보고 싶지 않아?" — 에 마음이 동했다. 그래서 노트북을 열고 PyTorch를 설치하고 모델을 띄우는데, 한 줄이 눈에 들어온다.

```
RuntimeError: CUDA out of memory. Tried to allocate 256.00 MiB
```

내장 그래픽이 전부인 노트북에서는 애초에 CUDA 같은 게 없다. 좀 더 가벼운 모델로 바꿔도 CPU에서는 한 에폭에 두 시간이 걸린다고 한다. 이쯤 되면 의욕이 식는다. 외장 GPU를 사야 하나, 클라우드 인스턴스를 빌려야 하나, 아니면 그냥 영상이나 보러 갈까.

ML을 시작하려는 사람이 가장 먼저 부딪히는 벽은 알고리즘이 아니다. **GPU가 없다는 사실**이다. 데이터셋도 있고, 튜토리얼도 있고, 의지도 있는데 하드웨어가 없어서 시작을 못 한다. 그렇다면 어떻게 해야 할까. GPU를 사야만 ML을 시작할 수 있다면, 이 분야의 진입 장벽은 영원히 지갑의 두께와 같이 갈 것이다.

다행히도 누군가 이 벽을 무너뜨려 두었다. **Google Colab**과 **Kaggle Notebooks**다. 이번 장에서는 이 두 클라우드 노트북이 어떻게 "GPU의 대중화"를 이끌었는지, 무료에서 어디까지 갈 수 있고 어디서부터 유료가 합리적인지, 그리고 학습한 모델을 로컬로 가져와 추론까지 이어가는 워크플로우를 함께 잡아보자.

## Colab의 셀링 포인트 — 설치 0초, 무료 GPU, Drive 한 몸

Colab을 처음 써보면 어이가 없을 정도로 간단하다. 브라우저에서 `colab.research.google.com`을 열고, "새 노트북"을 누르면 끝이다. 무엇을 설치할 것도, 어떤 가상 환경을 만들 것도 없다. 셀에 코드를 치고 [Shift+Enter]를 누르면 클라우드 어딘가의 컨테이너에서 결과가 돌아온다. Google 계정만 있으면 누구나, 어디서든, 어떤 노트북·태블릿·심지어 휴대폰에서도 같은 작업이 이어진다.

Colab은 사실상 **Jupyter 노트북을 Google이 호스팅하는 서비스**다. 4장에서 우리가 살펴본 Jupyter의 멘탈 모델 — 프런트엔드와 커널, 셀과 메모리, `.ipynb` 파일 포맷 — 이 그대로 적용된다. 다만 커널이 자기 컴퓨터가 아니라 Google의 데이터센터 어딘가에서 돈다는 점이 다르다. 이 한 가지 차이가 모든 것을 바꾼다.

이게 왜 중요한가. 4장에서 우리는 JupyterLab을 띄우려고 `pip install jupyterlab` 또는 `uv tool install jupyterlab`을 쳤다. 좋다, 그 정도는 어렵지 않다. 그런데 PyTorch 1.x에서 2.x로 넘어가던 시기에 CUDA 버전 매칭이 안 맞아서 `pip install` 한 번에 두세 시간을 잡아먹는 일이 흔했다. NumPy를 업데이트했더니 pandas가 깨지고, conda로 풀려고 보니 채널 우선순위가 꼬여 있고. 이런 경험을 해본 사람은 안다. 환경을 설정하다가 본 작업을 잊는 경우가 얼마나 흔한지.

Colab은 그 모든 것을 우회한다. PyTorch·TensorFlow·JAX·scikit-learn·pandas·matplotlib — ML/데이터 작업의 표준 패키지가 사전 설치돼 있다. CUDA 드라이버도 맞춰져 있다. 첫 셀에서 다음 한 줄만 치면 GPU가 잡힌다.

```python
import torch
print(torch.cuda.is_available())   # True
print(torch.cuda.get_device_name(0))   # 'Tesla T4' 등
```

Drive 연동도 손에 쥐어준다. Colab 노트북 자체가 Google Drive에 저장되고, 데이터셋이나 모델 가중치를 Drive에 두면 마운트 한 줄로 접근할 수 있다.

```python
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/datasets/sales.csv')
df.head()
```

처음 마운트할 때 인증 토큰을 한 번 붙여 넣으면, 같은 노트북에서 두 번째부터는 자동으로 잡힌다. "데이터를 어디에 둘 것인가"라는 익숙한 고민이 한 줄로 해결된다.

이게 Colab의 본질이다. **인프라를 만지지 않고 ML 실험에 들어갈 수 있다.** 이 한 가지가 Colab을 사실상 ML 입문의 표준 진입로로 만들었다.

조금 더 풀어보자. ML을 처음 배우려는 사람이 가장 자주 막히는 지점은 어디인가. 알고리즘이 어렵거나 수학을 못 따라가서가 아니다. **`pip install`이 안 끝나서**, **CUDA 버전이 안 맞아서**, **Conda 채널이 꼬여서** 다. 영상 강의의 첫 5분 동안 강사가 "환경 설정은 알아서 하시고 들어옵니다"라고 한 줄을 던지는 순간, 절반의 학습자는 거기서 멈춘다. 환경 설정의 황무지를 헤매다가, 본격 학습에 들어가기도 전에 의욕이 식는다.

Colab은 그 황무지를 우회한다. 그것도 무료로. 이게 사회적으로 어떤 의미인지 생각해보면 결코 작지 않다. **컴퓨팅 자원의 격차가 학습 격차를 결정하지 않는다.** 학생이든 직장인이든, 도서관 컴퓨터든 5년 된 노트북이든, 같은 조건에서 ML을 시작할 수 있다. Google이 이 인프라를 무료로 제공하는 이유는 결국 자기네 클라우드 생태계로의 유입이지만, 그 부수 효과로 우리는 GPU의 대중화를 누리고 있다.

런타임 유형도 한 번 짚어두자. Colab의 런타임은 셀 메뉴 [Runtime] → [Change runtime type]에서 고를 수 있다. 기본은 CPU지만, **T4 GPU**, **TPU v2/v3** (또는 최신 v4·v5e), 그리고 유료 플랜에서는 **L4·A100** 까지 옵션이 펼쳐진다. 한번 골라두면 그 세션 동안 유지된다. 무료 티어는 GPU·TPU 옵션이 가능하긴 하지만, 사용 가능 여부가 시간대마다 달라진다는 점은 감안하자.

## 무료 티어의 한계 — 어디까지가 공짜인가

물론 공짜에는 한계가 있다. 무료 Colab을 한동안 쓰다 보면 다음과 같은 메시지를 만나게 된다.

> "Cannot connect to GPU backend. You cannot currently connect to a GPU due to usage limits in Colab."

또는 학습을 돌려놓고 외출했다가 돌아와 보면 세션이 끊어져 있다. 화면 한쪽엔 다음과 같은 안내가 떠 있다.

> "Runtime disconnected. Your runtime was disconnected because it was idle for too long."

이게 무료 티어의 현실이다. 2026년 5월 기준으로 무료 Colab의 한계를 정리해보면 대략 이렇다.

- **GPU:** 보통 T4가 잡힌다. 사용량이 많은 시간대에는 GPU 자체가 할당되지 않는다.
- **RAM:** 약 12GB. 큰 데이터셋이나 큰 모델을 올리면 OOM이 난다.
- **세션 시간:** 최대 약 12시간. 보통은 그 전에 유휴로 끊어진다.
- **유휴 타임아웃:** 화면을 가만히 두면 90분쯤 뒤에 런타임이 회수된다.
- **피크 시간:** 미국 낮 시간(한국 시간 새벽~아침)에 GPU 거부가 잦다.

이 한계를 알고 있으면 무료 Colab으로 할 수 있는 일과 할 수 없는 일이 분명히 갈린다. **할 수 있는 일:** 튜토리얼 따라가기, 작은 모델 fine-tuning, EDA, 데모용 데모, 강의 자료 공유. **할 수 없는 일:** 며칠 걸리는 대규모 학습, 24/7 추론 서비스, 큰 LLM의 풀 fine-tuning.

특히 한 가지 패턴은 기억해두자. **학습 중간에 가중치를 주기적으로 Drive에 저장하는 습관.** 이걸 안 해두면 유휴로 끊어진 순간 그동안의 학습이 모두 날아간다. 다음과 같은 한 줄이 보험이다.

```python
if epoch % 5 == 0:
    torch.save(model.state_dict(), f'/content/drive/MyDrive/checkpoints/model_epoch{epoch}.pt')
```

찜찜한 일이 한 번 일어나봐야 그 가치를 안다. 첫 토이 프로젝트에서는 한 번쯤 잃어보고 깨닫게 되는 교훈이기도 하다.

또 하나 자주 놓치는 부분이 **유휴 타임아웃을 우회하는 꼼수**들이다. 학습이 길어지면 사람이 옆에 붙어서 셀을 클릭해야만 세션이 살아 있다. 이걸 피하려고 브라우저 콘솔에서 자동 클릭 스크립트를 돌리는 트릭이 한때 유행한 적이 있다. Colab 측에서 이런 패턴을 적극 차단하기 시작했고, 약관 위반에 가깝다는 점도 분명해졌다. 결론은 단순하다. **무료 티어는 무료의 한계를 인정하고 쓰는 편이 낫다.** 진지하게 학습이 길어지는 작업이라면 Pro로 넘어가거나, 아예 다른 클라우드를 쓰거나, 로컬 GPU를 마련하는 게 정도다.

## 유료 플랜 — Pro와 Pro+, Pay As You Go

무료로 쓰다 보면 자연스럽게 다음 질문이 떠오른다. "이거, 돈을 좀 내면 어디까지 가나?"

2026년 5월 기준 Colab의 가격 체계는 다음과 같다.

| 플랜 | 월 가격 (USD) | 주요 차이 |
|------|--------------|----------|
| Free | $0 | T4 위주, 세션 ~12h, 피크 시 GPU 거부 가능 |
| Pro | $11.99 | L4 GPU 우선 할당, 간헐적 A100, 더 긴 세션, 고RAM 옵션 |
| Pro+ | $49.99 | A100 더 자주, 백그라운드 실행, 더 큰 RAM·디스크 |
| Pay As You Go | 컴퓨트 단위 별 과금 | 필요할 때만 컴퓨트 단위 구매 |

> ⚠️ 가격은 빠르게 바뀐다. 본 책의 표는 **2026년 5월 기준**이며, 실제 결제 전에는 [colab.research.google.com/signup](https://colab.research.google.com/signup) 공식 페이지를 다시 확인하는 편이 낫다.

Pro로 넘어갈지 말지는 자기 작업 패턴을 한번 돌아보자. 일주일에 두세 번 한두 시간씩 가벼운 실험만 한다면 무료로 충분하다. 매일 학습을 돌리거나, 한 번에 6시간 이상 끊김 없이 돌려야 한다면 Pro($11.99)가 합리적이다. 큰 모델을 fine-tuning하거나 백그라운드 실행이 필요하면 Pro+($49.99)를 고려해볼 만하다. Pay As You Go는 "한 달은 안 쓸 것 같지만 다음 주에 잠깐 A100이 필요해" 같은 산발적 수요에 잘 맞는다.

Pro의 또 한 가지 가치는 **"GPU 거부"가 거의 없어진다**는 점이다. 무료 티어를 한참 쓰다 보면 피크 시간에 GPU 할당 자체가 막히는 경험을 하는데, 이게 의외로 짜증난다. 마음먹고 작업하려고 했는데 시작도 못하고 한 시간을 흘려보내는 일이 반복되면, $11.99는 그 시간의 가치보다 훨씬 작은 비용으로 느껴진다. 학습자라면 무료로 시작하다가 "이 짜증을 한 달에 두세 번 이상 겪는다" 싶을 때 Pro를 고려해보자.

**고RAM 옵션**도 Pro부터 활성화된다. 큰 데이터셋을 메모리에 올리거나, 큰 임베딩 모델을 불러올 때 무료 티어의 12GB가 너무 작다는 게 분명해지는 순간이 있다. Pro에서 고RAM 런타임을 켜면 25GB 이상으로 늘어난다. 데이터의 크기가 작업의 병목이 된다면 Pro 가입 후 이 옵션을 잊지 말고 켜자.

물론 한 가지 함정이 있다. **Pro도 무한 GPU가 아니다.** 사용량 한도가 있고, 한도를 초과하면 며칠간 GPU 우선순위에서 밀린다. 영업일 풀가동 학습이라면 클라우드 GPU 인스턴스(AWS·GCP·Lambda Labs 등)를 직접 빌리는 편이 결국 싸진다는 시점이 온다. 이 손익분기점은 작업 강도에 따라 다르지만, "한 달 내내 GPU를 거의 풀로 쓴다"가 기준선이다.

## AI-First Colab — 자연어가 노트북을 짓는다

2025년 무렵부터 Colab에 흥미로운 변화가 있었다. **Data Science Agent**라는 이름의 AI 어시스턴트가 들어왔다. 빈 노트북을 열고 상단의 입력창에 자연어로 작업을 묘사하면, 보일러플레이트부터 분석 셀까지 노트북 한 채가 자동으로 채워진다.

가령 이런 프롬프트를 넣어본다고 해보자.

> "타이타닉 데이터셋을 불러와서 결측치를 점검하고, 성별·나이·요금을 기반으로 생존 여부를 예측하는 로지스틱 회귀 모델을 학습하고, ROC 곡선을 그려줘."

Agent는 다음과 같은 흐름의 셀을 잇따라 생성한다. (대략)

```python
# 셀 1: 데이터 로드
import pandas as pd
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
df.head()

# 셀 2: 결측치 점검
df.isna().sum()

# 셀 3: 전처리
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
features = df[['Sex', 'Age', 'Fare']]
target = df['Survived']

# 셀 4: 모델 학습
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)
model = LogisticRegression().fit(X_train, y_train)

# 셀 5: ROC 곡선
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
y_score = model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_score)
plt.plot(fpr, tpr, label=f'AUC = {auc(fpr, tpr):.2f}')
plt.legend(); plt.show()
```

이걸 어떻게 받아들여야 할까. 한쪽에서는 "초보자가 boilerplate에서 막히지 않고 본질에 집중할 수 있는 좋은 도구"라는 평가가 있다. 다른 한쪽에서는 "초보자가 코드를 읽지 않고 그냥 Run만 누르는 습관이 무서워질 수 있다"는 우려도 있다. 둘 다 일리가 있다.

실용적으로는 이렇게 쓰는 편이 낫다. **Agent가 만든 노트북을 한 번 쭉 읽어보고, 의도와 다른 셀을 직접 고친 다음 진행하기.** 그러면 Agent는 "막힌 시작"을 풀어주는 도구로 기능하고, 학습은 학습대로 이어진다. AI에게 운전대를 통째로 맡기지 말고, 옆자리 내비게이터로 두자는 정도의 거리감이 적당하다.

또 한 가지 흔히 놓치는 점이 있다. **Agent가 골라주는 라이브러리나 함수가 항상 최선이 아니다.** 가령 위 예시에서 `train_test_split`에 `random_state`를 안 주면 매번 결과가 다르게 나오고, `LogisticRegression`의 기본 `max_iter`가 100이라 수렴 경고가 뜰 수도 있다. 표면적으로 동작하는 코드와 실무에서 쓸 만한 코드는 다르다. Agent의 산출물은 "한번 돌아가는 데모"의 출발점으로 받아들이고, 실제 분석에서는 사람이 한 번 더 다듬어줘야 한다.

Agent가 잘 어울리는 또 한 가지 용도는 **셀 단위 도우미**다. Colab의 셀 옆에 작은 AI 아이콘이 떠 있어서, "이 셀이 왜 에러가 나는지 설명해줘"나 "이 데이터프레임을 long format으로 바꿔줘" 같은 요청을 한 셀 단위로 던질 수 있다. 노트북 전체를 자동 생성하는 큰 작업보다, 막힌 셀 하나를 푸는 작은 작업에서 Agent의 도움이 가장 자연스럽다. **자전거의 보조 바퀴처럼 쓰자.** 어디에 어떻게 기댈지 자기가 정하는 거다.

> 📌 Agent 모드의 이름·UI·동작은 빠르게 바뀐다. 본문은 **2026년 5월 기준**의 모습이며, 핵심은 "자연어 → 노트북 자동 생성"이라는 패러다임 자체다.

## Kaggle Notebooks — 데이터셋과 한 몸

Colab이 "GPU 클라우드"라면, Kaggle Notebooks는 "데이터셋 클라우드"다. 둘은 형제처럼 닮았지만 정체성이 다르다.

Kaggle은 데이터 사이언스 경연 플랫폼으로 출발했다. 그래서 Kaggle Notebooks의 가장 큰 강점은 **데이터셋이 한 클릭으로 마운트**된다는 점이다. 새 노트북을 만들고 우측의 "Add Data" 버튼을 누르면, Kaggle에 올라온 수십만 개의 공개 데이터셋 중 원하는 것을 검색해서 바로 마운트할 수 있다. Drive에 업로드할 일도, S3 버킷을 만들 일도 없다.

마운트하면 데이터는 `/kaggle/input/<dataset-slug>/` 경로에 떨어진다.

```python
import pandas as pd
df = pd.read_csv('/kaggle/input/titanic/train.csv')
df.head()
```

또 하나의 강점은 **fork·복제로 학습할 수 있다**는 점이다. 다른 사람의 노트북을 발견하면 우측 상단의 "Copy & Edit"으로 그대로 내 작업 공간에 복제된다. 데이터·코드·환경이 통째로 따라온다. 누군가의 EDA 노트북을 가져와 내 가설을 더 얹어보고, 다른 사람의 모델 학습 코드를 가져와 하이퍼파라미터만 바꿔 돌려본다. 이게 Kaggle 학습 문화의 정수다.

다른 한편으로 Kaggle 노트북에는 제약도 있다. 외부 인터넷 접근이 기본 비활성화돼 있어서 (경연 페어니스를 위해), `pip install`로 패키지를 받으려면 매번 "Internet on" 토글을 켜야 한다. 환경 커스터마이징도 Colab보다 약하다. 그렇지만 학습용·경연용·튜토리얼 공유용으로는 이만한 환경이 없다.

| 비교 항목 | Colab | Kaggle |
|----------|-------|--------|
| 강점 | 무료 GPU·Drive 연동·AI Agent | 데이터셋 한 클릭·fork 학습 |
| 약점 | 데이터셋을 Drive에 직접 올려야 함 | 외부 인터넷 제한·환경 커스텀 약함 |
| 잘 맞는 작업 | 자유로운 ML 실험·코드 공유 | 데이터셋 기반 학습·경연 |

둘은 경쟁이라기보다 보완재로 두고 쓰는 편이 낫다. **"데이터가 Kaggle에 있다 → Kaggle에서, 자유롭게 시작하고 싶다 → Colab에서"** 정도로 갈라 쓰자.

Kaggle Notebook의 또 다른 매력은 **공개와 비공개를 토글로 다룰 수 있다**는 점이다. 처음에는 비공개로 작업하다가, 결과가 마음에 들면 공개로 전환해 다른 사람들의 시선에 노출시킬 수 있다. 잘 만든 EDA 노트북은 Kaggle 커뮤니티에서 upvote를 받고, 작성자의 평판으로 쌓인다. 데이터 사이언스 포트폴리오를 만드는 가장 자연스러운 방식 중 하나다. GitHub에 올린 `.ipynb`는 누가 와서 봐주기 어렵지만, Kaggle에 올린 노트북은 데이터셋 페이지를 통해 자연스럽게 노출된다.

또 하나, **Kaggle Notebook의 "Save Version"** 기능이 git 커밋과 비슷한 역할을 한다. 노트북을 수정한 뒤 "Save Version"을 누르면 버전이 하나 만들어지고, 언제든 이전 버전으로 돌아갈 수 있다. 풀 git만큼 정밀하진 않지만, 학습용 노트북에서는 이 정도면 충분하다.

## 워크플로우 레시피 — Colab에서 학습, Drive로 가중치, 로컬에서 추론

클라우드 노트북의 가장 흔한 함정은 이렇다. **"학습은 됐는데, 학습한 모델을 어떻게 내 컴퓨터로 가져와 쓰지?"** Colab 세션이 끝나면 모든 게 휘발되고, 학습된 모델만 손에 잡히지 않는 채 사라진다.

이 함정을 피하는 표준 워크플로우를 한번 같이 잡아보자. **Colab에서 학습 → 가중치를 Drive로 → 로컬에서 추론**의 세 단계다.

### 1단계: Colab에서 학습

```python
# Colab에서 실행
from google.colab import drive
drive.mount('/content/drive')

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# (데이터 로드와 모델 정의는 생략)
model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

CHECKPOINT_DIR = '/content/drive/MyDrive/my_project/checkpoints'
import os; os.makedirs(CHECKPOINT_DIR, exist_ok=True)

for epoch in range(20):
    for x, y in train_loader:
        x, y = x.cuda(), y.cuda()
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()

    # 매 에폭마다 Drive에 체크포인트
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, f'{CHECKPOINT_DIR}/epoch_{epoch}.pt')
    print(f'Epoch {epoch} 저장 완료')
```

핵심은 **Drive에 직접 저장**한다는 점이다. `/content/`에 저장하면 세션이 끊어지는 순간 사라지지만, `/content/drive/MyDrive/`에 저장하면 Google Drive에 영속된다.

### 2단계: Drive에서 로컬로

학습이 끝나면 Drive 웹 인터페이스(`drive.google.com`)에서 체크포인트 파일을 내려받아도 되고, 로컬에 `rclone`이나 `gdown`을 설치해 명령줄에서 끌어와도 된다.

```bash
# gdown으로 받기 (파일 ID는 Drive 공유 링크에서 추출)
pip install gdown
gdown 'https://drive.google.com/uc?id=<FILE_ID>'
```

### 3단계: 로컬에서 추론

이제 GPU 없는 로컬 노트북에서도 추론은 충분히 가능하다. 학습이 무거웠을 뿐, 추론은 CPU로도 돌아간다 (물론 느리지만, 한 건씩 처리하는 데모 정도면 괜찮다).

```python
# 로컬에서 실행
import torch

model = MyModel()
checkpoint = torch.load('epoch_19.pt', map_location='cpu')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

with torch.no_grad():
    output = model(some_input)
print(output)
```

이 3단계 흐름이 손에 익으면, "GPU가 없다"는 한계는 더 이상 시작을 막는 벽이 아니다. **무거운 작업은 클라우드에 위임하고, 가벼운 작업은 손에 잡히는 도구로 한다.** 이게 클라우드 노트북 시대의 표준 작업 방식이다.

이 패턴을 한 단계 자동화하고 싶다면, 학습이 끝나는 시점에 노트북이 자기 자신에게 알림을 보내도록 만들 수도 있다. 가령 학습 마지막 셀에서 Slack webhook을 한 줄 호출하거나, 이메일을 한 통 보내는 식이다.

```python
import requests
requests.post(SLACK_WEBHOOK_URL, json={"text": f"학습 완료. 최종 정확도 {acc:.4f}"})
```

학습이 길어 한참 자리를 비울 때, 다 끝났는지 굳이 노트북을 새로고침해보지 않아도 된다. 이런 작은 자동화 한 줄이 클라우드 노트북 작업의 결을 부드럽게 만든다.

또 한 가지 권하는 건 **`!nvidia-smi` 한 줄을 학습 셀 직전에 박아두는 습관**이다.

```python
!nvidia-smi
```

이 한 줄이 GPU의 종류·메모리·다른 프로세스 점유 여부를 한눈에 보여준다. T4가 잡혔는지 A100이 잡혔는지, 가용 메모리가 얼마나 남았는지를 학습 시작 전에 확인하면 OOM 에러로 한참 헤매는 일을 줄일 수 있다.

## 한국 데이터 사이언스 학습자의 첫 모델

> 📌 **한국 사례 — Colab으로 시작한 첫 모델**
>
> 한국의 데이터 사이언스 학습 커뮤니티(velog·OKKY·다양한 네이버 카페)에서 자주 보이는 글의 패턴이 있다. "데이터 분석을 공부하던 비전공자가 Colab으로 첫 ML 모델을 돌려본 경험담"이다.
>
> 흔한 줄거리는 이렇다. — Python 기초 강의를 듣고, pandas로 데이터를 만져보고, 다음 단계로 ML을 한다는데 GPU가 없다. 영상 강의에서 "Colab을 켜면 됩니다"라는 한 줄에 반신반의로 brower를 열고, 첫 모델이 학습되는 걸 보면서 "어, 진짜 되네?"하는 순간을 맞는다. 그 순간이 ML 학습 곡선의 진짜 시작점인 경우가 많다.
>
> 노트북에 GPU가 없는 학습자가 ML 분야로 진입하는 진입로로 Colab은 이미 한국에서도 표준이다. 학교에서 머신러닝 수업의 실습 도구로 Colab을 쓰는 곳이 적지 않고, 부트캠프 과정의 실습 환경도 Colab을 기본으로 깔고 가는 경우가 많다. (※ 구체적 인용은 사실 확인 후 본 박스를 보강할 예정.)

## 데이터를 어디에 둘 것인가 — Drive·Kaggle·GitHub·외부 스토리지

클라우드 노트북에서 자주 듣는 질문 중 하나가 "데이터를 어디에 두는 게 좋은가" 다. 답은 데이터의 크기와 민감도에 따라 갈린다. 한 번 정리해두자.

**1MB 미만의 작은 CSV·JSON.** GitHub repo에 그냥 넣어두자. Colab에서 `pd.read_csv("https://raw.githubusercontent.com/<user>/<repo>/main/data.csv")` 한 줄로 끌어온다. 노트북과 데이터가 한 git 저장소에 있다는 게 가장 단순하고 재현 가능하다.

**100MB 이하의 중간 데이터.** Kaggle Datasets에 올려서 마운트하거나, Google Drive에 올려서 마운트한다. Drive 마운트는 한 줄로 되고, Kaggle은 데이터셋 페이지를 통해 공개 공유까지 가능하다.

**1GB 이상의 큰 데이터.** Google Cloud Storage(GCS)나 AWS S3 같은 객체 스토리지를 쓴다. Colab은 GCS와 자연스럽게 연동된다.

```python
from google.colab import auth
auth.authenticate_user()
!gsutil cp gs://my-bucket/big-data.parquet /content/
```

S3는 `boto3`나 `s3fs`로 접근한다. 단, 액세스 키를 노트북에 직접 박아 넣지 말자. Colab의 [Secrets] 기능을 쓰면 키를 저장해두고 노트북에서 환경변수로 끌어 쓸 수 있다.

```python
from google.colab import userdata
import os
os.environ['AWS_ACCESS_KEY_ID'] = userdata.get('AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = userdata.get('AWS_SECRET_ACCESS_KEY')
```

이런 작은 위생 한 가지가 키 노출 사고를 막는다. 노트북을 무심코 GitHub에 올렸다가 키가 통째로 노출되는 사고가 생각보다 흔하다.

**민감한 데이터(개인정보·NDA·회사 기밀).** 답은 단순하다. **클라우드 노트북에 올리지 말자.** Colab과 Kaggle은 외부 SaaS다. 회사 데이터를 무심코 올리면 큰 문제가 된다. 사내 정책이 있다면 그 정책을 따르자. 정책이 없다면, "이 데이터가 외부에 알려져도 괜찮은가"를 한 번 자문하자. 한 번이라도 망설여진다면 로컬·온프레미스로 돌아오자.

## 노트북 공유와 재현성 — 누가 봐도 돌아가는 노트북

자기 작업을 다른 사람과 공유할 때, 클라우드 노트북에는 한 가지 큰 함정이 숨어 있다. **"내 환경에서는 됐는데, 받은 사람 환경에서는 안 된다."** 이 함정을 줄이는 표준 패턴 두 가지를 짚어두자.

**첫째, requirements.txt를 노트북에 박아두자.** 노트북 첫 셀에 다음 한 줄을 두는 습관이 있다.

```python
!pip install -q transformers==4.45.0 datasets==2.20.0 torch==2.4.0
```

`-q`는 출력을 조용하게 만드는 플래그다. **버전을 핀(pin)** 한다는 점이 핵심이다. `transformers`만 쓰면 받는 사람의 시점에 따라 4.30이 깔릴 수도, 5.0이 깔릴 수도 있다. 그러면 같은 코드가 다른 결과를 낸다. 핀해두면 적어도 라이브러리 버전 차이로 인한 차이는 없어진다.

**둘째, 데이터 로드 셀에 출처 주석을 박아두자.**

```python
# 데이터 출처: Kaggle Titanic Competition (https://www.kaggle.com/c/titanic)
# 다운로드 위치: /content/drive/MyDrive/datasets/titanic.csv
import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/datasets/titanic.csv')
```

받은 사람이 "이 CSV는 어디서 받는 거지?" 하지 않게 만든다. 작아 보이지만 노트북 공유의 마찰을 절반쯤 줄인다.

이 두 가지가 클라우드 노트북에서의 미니 재현성 베스트 프랙티스다. 9장에서 재현성을 본격적으로 다루는데, 클라우드 환경에서는 위 두 가지만 챙겨도 그 정도가 다르다.

## 클라우드 노트북의 한계 — 잊지 말아야 할 것들

Colab과 Kaggle이 아무리 편해도, 클라우드 노트북에는 본질적인 한계가 있다. 시작하는 사람이 잊지 말아야 할 세 가지를 짚어두자.

**첫째, 세션은 영원하지 않다.** 무료 티어는 12시간, 유휴는 90분이다. Pro도 한도가 있다. **체크포인트를 Drive에 저장하지 않으면 학습이 한순간에 사라질 수 있다.** 이걸 한 번 잃어보고 깨닫는 것보다는, 처음부터 자동 저장 코드를 박아두는 편이 낫다.

**둘째, 데이터 보안이 다르다.** Colab과 Kaggle 모두 코드와 데이터가 클라우드에 올라간다. 회사 데이터·개인정보·NDA 데이터를 무심코 올리면 큰 문제가 된다. 민감한 데이터는 Colab에 올리지 않거나, 로컬·온프레미스 환경에서만 다루는 원칙을 세우자.

**셋째, 누적 비용은 생각보다 빨리 쌓인다.** Colab Pro $11.99/월은 한 달이면 작아 보이지만, 1년이면 $144다. Pro+로 올리면 $600이다. 학습 강도가 높아지면 차라리 중고 GPU를 한 번 사거나 클라우드 인스턴스를 직접 빌리는 편이 결국 싸진다는 시점이 온다. 이 손익분기점을 놓치지 말자.

## Colab과 Jupyter, 무엇이 같고 무엇이 다른가

여기까지 와서 한 가지 헷갈리기 쉬운 점을 정리하고 가자. **"Colab은 Jupyter인가, 다른 도구인가?"**

답은 둘 다 맞다. **Colab의 본질은 Jupyter다.** `.ipynb` 파일 포맷을 그대로 쓰고, 셀·커널·매직 명령어 같은 멘탈 모델이 동일하다. 4장에서 배운 Jupyter 지식이 거의 그대로 적용된다. `%timeit`도 되고, `%%writefile`도 되고, ipywidgets도 (대부분) 동작한다. Colab에서 만든 노트북을 다운로드해서 로컬 JupyterLab에서 열어도 그대로 동작한다 (라이브러리만 같다면).

**그러면 무엇이 다른가.** Colab은 그 위에 자기만의 레이어를 한 겹 얹었다. Drive 마운트 (`google.colab.drive`), 인증 헬퍼 (`google.colab.auth`), 폼 셀(form cell), 사용자 입력 (`google.colab.userdata`) 같은 Colab 전용 API가 있다. 이걸 노트북에 쓰면 Colab 밖에서는 동작하지 않는다.

이 차이를 알고 있으면 Colab 노트북을 짤 때 한 가지 선택을 하게 된다. **"이 노트북은 Colab 전용으로 짤 것인가, 아니면 어디서든 돌도록 짤 것인가."** Colab 전용이면 폼 셀 같은 편한 기능을 마음껏 쓰면 되고, 이식성을 원하면 Colab 전용 API를 안 쓰거나 try-except로 감싸자.

```python
try:
    from google.colab import drive
    drive.mount('/content/drive')
    DATA_DIR = '/content/drive/MyDrive/data'
except ImportError:
    # 로컬 환경
    DATA_DIR = './data'
```

이런 작은 가드 한 줄이 같은 노트북을 Colab과 로컬 양쪽에서 돌게 만든다. 학습한 모델을 로컬에서 추론하는 워크플로우(앞 절)에서 이 패턴이 진가를 발휘한다.

## Cursor + Colab 조합 — 한 문장 예고

마지막으로 한 가지 흐름만 짧게 짚어두자. 2025년 무렵부터 흥미로운 패턴이 자리 잡고 있다. **"코드는 Cursor에서 AI로 짜고, 실행은 Colab GPU에서."** 코드 편집의 풍요(Cursor의 Agent 모드, 파일 트리, 리팩토링)와 컴퓨트의 풍요(Colab의 GPU)를 합치는 방식이다.

이 조합을 어떻게 굴리는지는 6장에서 깊이 다루기로 한다. 6장에서 우리는 "에디터 안의 노트북" — VS Code와 Cursor가 노트북을 어떻게 흡수했는지 — 를 살펴보면서, 이 Cursor + Colab 워크플로우의 본편을 만나게 될 것이다.

## TPU와 GPU 사이 — 어떤 가속기를 골라야 하나

Colab의 런타임 옵션을 처음 보면 한 가지 선택지가 낯설다. **TPU.** Google이 자체 설계한 ML 전용 가속기인데, GPU와 무엇이 다르고 언제 쓰는 게 좋은지 짚어두자.

큰 그림으로는 이렇다.

- **GPU (T4·L4·A100):** 대부분의 PyTorch·TensorFlow 코드가 자연스럽게 돈다. 학습용·추론용 모두 표준. 처음 시작한다면 GPU 고민 없이 그냥 GPU를 고르자.
- **TPU:** Google의 JAX·TensorFlow에 가장 잘 맞는다. PyTorch는 `torch_xla` 라는 별도 패키지가 필요하고, 코드 수정이 약간 따른다. 큰 모델·대용량 배치에서 GPU보다 빠를 수 있지만, 학습 곡선이 가파르다.

학습자가 처음부터 TPU에 손을 대는 건 권하지 않는다. **GPU에 익숙해진 다음, "이 모델이 너무 큰데 TPU로 가속해볼까?" 시점에 들어가는 게 자연스럽다.** 보통 그 시점은 한참 뒤다. 그때까지는 T4 하나로도 할 일이 많다.

## 마무리

GPU가 없어도 ML을 시작할 수 있는가. 답은 분명하다. **시작할 수 있다.** Colab과 Kaggle이 그 길을 열어두었다.

다만 클라우드 노트북을 쓰는 마음가짐은 로컬과 다르다. 세션은 끊어진다는 전제로 짜야 하고, 가중치는 Drive에 영속화해야 하고, 한도가 있다는 사실을 잊으면 안 된다. 이 세 가지만 손에 익으면, 노트북 한 대로도 사실상 무한에 가까운 컴퓨트를 자유롭게 다룰 수 있다.

한 걸음 더 권하자면, **Colab과 Kaggle을 단독 사용에서 끝내지 말고, 자기 작업 흐름의 한 모듈로 다루자.** Colab은 학습 인프라, Kaggle은 데이터셋 카탈로그, 로컬은 추론·시각화·서사. 세 환경을 자기 작업의 어느 단계에 배치할지 결정하는 것 자체가 데이터 작업자의 안목이다. 이 안목은 한 번에 잡히지 않는다. 작은 토이 프로젝트 하나를 끝까지 굴려보면서 — 데이터 어디서 받고, 어디서 학습하고, 어디서 추론하고, 어디서 발표하는지 — 자기에게 맞는 흐름을 찾아가는 게 빠르다.

다음 장에서는 시선을 다시 로컬로 돌려본다. **에디터 안의 노트북** — VS Code와 Cursor가 `.ipynb`를 어떻게 일급 시민으로 다루는지, Pylance·디버거·Git이 노트북과 한 창에 들어왔을 때 워크플로우가 어떻게 바뀌는지 살펴보자. 그리고 그 끝에서, 이 장에서 예고한 **"Cursor 코드 → Colab GPU 실행"** 패턴을 본격적으로 다뤄보자.
