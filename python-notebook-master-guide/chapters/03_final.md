# 3장. 매직 커맨드, 셸, 파일 포맷 — 모든 노트북에 통하는 도구상자

새 직장 첫날을 떠올려보자. 어떤 도구를 줘도 일단 환경이 낯설다. 단축키도, 메뉴 구조도, 익숙한 워크플로우도 다르다. 그런데 한 가지가 어디서나 통한다면 — 그건 큰 위안이다. 노트북에선 그 한 가지가 매직 커맨드다.

JupyterLab에서 짜든, Colab에서 짜든, VS Code에서 열든, Cursor에서 보든 — `%timeit`은 `%timeit`이고 `%%writefile`은 `%%writefile`이다. 환경이 바뀌어도 똑같이 동작한다. 왜냐하면 매직은 프런트엔드가 아니라 IPython 커널이 처리하기 때문이다. 2장에서 봤던 두 프로세스 구조에서, 매직은 커널 쪽에 들어 있다. 그래서 프런트엔드를 갈아치워도 그대로 살아남는다.

이 장에서 매직과 셸 통합, 그리고 노트북 파일 포맷 두 가지(`.ipynb`와 percent format)를 손에 넣자. 어느 환경에 가도 첫 30분이면 생산적인 셀을 칠 수 있게 된다.

## 매직은 어디서 오는가

본격 들어가기 전에 한 가지 짚어두자. 매직 명령어는 파이썬 문법이 아니다. `%timeit`을 일반 파이썬 스크립트에 박으면 `SyntaxError`가 난다. 이걸 인식하고 처리하는 건 IPython 인터프리터다.

2장에서 본 두 프로세스 구조에서 커널은 보통 IPython이다. 표준 파이썬 인터프리터(`python3`)가 아니라 IPython 위에서 도는 `ipykernel`이라는 커널 패키지가 셀을 실행한다. IPython이 셀의 코드를 받으면 먼저 매직 라인을 골라내 처리하고, 나머지를 표준 파이썬으로 평가한다.

그래서 매직은 환경에 종속되지 않는다. JupyterLab에서든 Colab에서든 VS Code에서든 — 그 뒤의 커널이 IPython이라면 매직이 통한다. 같은 노트북을 다른 환경에서 열어도 매직 셀이 그대로 동작한다. 이게 "공용 무기"라는 표현의 근거다.

다른 언어 커널(R의 IRkernel, Julia의 IJulia)은 매직 시스템을 자기 식으로 갖고 있다. 문법은 비슷하지만 명령어 이름이 다르다. 이 장의 매직은 다 Python(IPython) 기준이다.

## 라인 매직과 셀 매직 — `%`와 `%%`의 차이

먼저 두 매직의 형태부터 분명히 구분하자.

**라인 매직 (`%`)**: 한 줄짜리 명령. 그 줄만 매직이고, 같은 셀의 나머지는 일반 파이썬이다.

```python
%timeit sum(range(1_000_000))
print("끝났다")
```

여기서 첫 줄만 매직이고, `print`는 평범한 파이썬이다.

**셀 매직 (`%%`)**: 셀 전체에 적용된다. 매직이 셀 첫 줄에 와야 하고, 그 아래 전부가 매직의 입력이 된다.

```python
%%timeit
total = 0
for i in range(1_000_000):
    total += i
```

이 셀 전체가 한 덩어리로 timeit에 들어간다. 라인 매직은 한 줄짜리 식의 시간만 재고, 셀 매직은 여러 줄에 걸친 코드 블록의 시간을 잰다.

이 둘을 헷갈리면 결과가 이상하게 나온다. `%%timeit total = 0; for ...` 한 줄을 라인 매직처럼 쓰면 에러가 난다. 반대로 셀 매직 자리에서 `%timeit`을 쓰면 첫 줄만 측정되고 나머지는 무시된다. 처음 만나면 헷갈리니 이 차이를 머리 한쪽에 박아두자.

## 매직 베스트 8 — 실전에서 가장 자주 쓰는 것들

수십 개의 매직이 IPython에 내장돼 있고, `%lsmagic`을 치면 전체 목록이 뜬다. 그중에서 실무에서 가장 자주 쓰는 여덟 개를 골라봤다. 처음 들어보는 화려한 것 말고, 매일 손이 가는 것들이다. 이 여덟 개를 손에 익히면 노트북 작업의 속도가 눈에 띄게 빨라진다.

### 1. `%timeit` — 한 줄로 벤치마크

성능 비교가 필요할 때 print 박고 time 모듈 임포트하지 말고 그냥 매직으로 하자.

```python
%timeit sum(range(1_000_000))
```

실행하면 이런 식의 출력이 뜬다.

```
12.4 ms ± 184 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

`%timeit`은 같은 코드를 여러 번 돌려 평균과 표준편차를 낸다. 한두 번 돌려서 나오는 노이즈에 흔들리지 않게 통계적으로 측정하는 것 — 이게 핵심이다. 두 가지 구현을 비교할 때 거의 무조건 이걸 쓴다.

셀 매직 `%%timeit`은 셀 전체를 측정한다. 여러 줄에 걸친 알고리즘의 시간을 잴 때 유용하다. 한 가지 주의 — `%%timeit`은 같은 셀을 여러 번 반복 실행한다. 그러니까 셀에 부수 효과가 있으면(파일 쓰기, DB 입력 등) 그게 여러 번 일어난다는 뜻이다. 측정 셀은 순수 계산만 두는 게 안전하다.

`-n`과 `-r` 옵션으로 반복 횟수를 조절할 수도 있다.

```python
%timeit -n 100 -r 3 sum(range(1_000_000))
```

`-n 100`은 한 번 측정에 코드를 100번 돌리라는 뜻, `-r 3`은 그 측정을 3회 반복하라는 뜻이다. 짧은 코드는 자동으로 적절한 반복 수를 정해주니까 보통은 옵션 없이 그냥 쓴다.

### 2. `%%writefile` — 셀 내용을 파일로 저장

노트북 안에서 파일을 만들고 싶을 때 쓴다. 별 거 아닌 것 같은데 의외로 자주 쓴다.

```python
%%writefile utils.py
def greet(name):
    return f"Hello, {name}!"

def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

실행하면

```
Writing utils.py
```

라는 메시지가 뜨고, 같은 폴더에 `utils.py`가 생긴다. 이걸 다음 셀에서 `from utils import greet`로 임포트해 쓸 수 있다. 노트북에서 시작한 함수를 외부 모듈로 빼는 첫 단계로 자주 쓴다.

`-a` 플래그를 붙이면 덮어쓰는 대신 추가(append)한다.

```python
%%writefile -a utils.py
def farewell(name):
    return f"Bye, {name}!"
```

쓰임새 시나리오 두 가지를 보자. 첫째, 강의 자료에서 학생이 따라 칠 때. 강사가 "이 셀을 실행하면 utils.py가 만들어집니다" 한 줄로 보일러플레이트를 깔 수 있다. 환경 설치 없이 바로 import해 쓸 수 있는 작은 모듈이 노트북 한 셀로 전달된다.

둘째, requirements.txt나 Dockerfile, config 파일 같은 부속 파일을 노트북에서 같이 만들고 싶을 때. 노트북 안에서 `%%writefile requirements.txt`로 의존성을 박아두면 그 노트북이 자기-완결적이다. BinderHub로 공유하면 받는 사람이 같은 환경을 자동으로 구성한다(4장).

### 3. `%matplotlib inline` / `%matplotlib widget` — 플롯을 어디에 띄울 것인가

`matplotlib`로 그래프를 그릴 때 어디에 표시할지를 정한다.

```python
%matplotlib inline
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.show()
```

`inline`은 정적 이미지로 셀 아래에 박힌다. 가장 흔한 선택이고, PDF로 내보내거나 GitHub에서 노트북을 볼 때 그대로 보인다.

`widget`은 인터랙티브 모드. 마우스로 줌, 팬, 회전이 가능하다. 3D 플롯이나 큰 데이터셋을 살필 땐 이게 낫다.

```python
%matplotlib widget
```

다만 `widget`은 `ipympl` 패키지를 따로 깔아야 한다(`pip install ipympl`).

이 매직은 노트북 시작할 때 한 번만 쳐두면 된다. 그 셀 이후의 모든 플롯에 적용된다.

### 4. `%load_ext autoreload` + `%autoreload 2` — 외부 모듈 변경 자동 반영

이 조합이 노트북 개발 사이클을 한 단계 빠르게 만든다. 같이 보자.

```python
%load_ext autoreload
%autoreload 2
```

이 두 줄을 노트북 맨 위에 박아둔다. 그러면 외부 `.py` 파일을 수정했을 때, 노트북의 다음 셀 실행 시점에 자동으로 다시 임포트된다. 평소엔 한 번 임포트한 모듈은 캐시되어 파일을 고쳐도 반영이 안 된다. 매번 커널을 재시작해야 하는데, 그러면 데이터 로드부터 다시 하느라 끔찍하게 번거롭다.

`%autoreload 2`는 "모든 임포트한 모듈을 매번 다시 읽어라"라는 뜻이다. 1은 명시적으로 표시한 것만, 0은 끄기.

```python
%load_ext autoreload
%autoreload 2

from src.data import load_data
df = load_data("sales.csv")  # 여기서 src/data.py 한 번 읽힘

# 이제 src/data.py를 에디터에서 수정...

df = load_data("sales.csv")  # 셀 다시 실행 → 수정 내용 반영됨
```

함수를 외부 모듈로 빼는 리팩토링과 짝을 이룬다. autoreload 없이는 모듈 추출이 너무 번거로워서 다들 노트북 안에 다 욱여넣게 된다. 9장의 핵심 베스트 프랙티스인 "함수를 외부 모듈로 추출"을 가능케 하는 것이 이 매직이다.

작은 주의사항이 있다. autoreload는 **모듈 자체를 다시 임포트**한다. 이미 만들어둔 객체에는 영향이 없다. 예를 들어 `model = MyModel()`로 인스턴스를 만들어둔 상태에서 `MyModel`의 메서드를 수정하면, 새로 만든 인스턴스는 새 메서드를 쓰지만 `model` 변수가 가리키는 옛날 인스턴스는 옛 메서드를 그대로 들고 있다. 인스턴스도 다시 만들어야 새 코드가 반영된다. 다소 어색하지만 익숙해지면 괜찮다.

또 C 확장 모듈(NumPy, PyTorch 등의 일부)은 autoreload가 안 되거나 이상하게 동작할 수 있다. 그럴 땐 커널 재시작이 답이다.

### 5. `%env` — 환경 변수 보고 설정하기

API 키, 데이터 경로, 디버그 플래그 같은 걸 환경 변수로 다룰 때 유용하다.

```python
%env
```

라고만 치면 현재 환경 변수가 전부 출력된다. 길어서 보통은 특정 변수를 본다.

```python
%env PATH
```

설정도 같은 매직으로 한다.

```python
%env PYTHONHASHSEED=0
%env DATA_DIR=/data/sales/2026
```

이렇게 해두면 그 노트북 세션 동안 해당 환경 변수가 유지된다. 머신러닝 재현성을 위해 시드를 고정할 때, 또는 큰 데이터 경로를 한 곳에서 관리할 때 자주 쓴다.

다만 주의: 시크릿(API 키 등)을 노트북 셀에 박지 말자. `%env OPENAI_API_KEY=sk-...` 같은 셀이 git에 그대로 올라가면 끔찍한 일이 된다. 시크릿은 셸에서 export하거나 `.env` 파일에서 읽어오는 패턴이 안전하다.

### 6. `%who` / `%whos` — 지금 메모리에 뭐가 들어 있나

2장에서 hidden state 얘기를 했다. 셀을 한참 만지다 보면 메모리에 뭐가 살아 있는지 헷갈린다. 이때 쓴다.

```python
%who
```

이렇게만 치면 현재 정의된 변수 이름들이 한 줄로 죽 나온다.

```
df    model    train_loader    x_test    y_test
```

더 자세히 보고 싶으면 `%whos`.

```python
%whos
```

```
Variable       Type           Data/Info
-----------------------------------------
df             DataFrame      [10000 rows x 12 columns]
model          Module         <torch.nn.Linear object at 0x7f8...>
train_loader   DataLoader     <torch.utils.data.dataloader...>
x_test         ndarray        500x10: 5000 elems, type `float64`
y_test         ndarray        500: 500 elems, type `int64`
```

타입과 크기를 한눈에 볼 수 있다. 노트북이 길어지면 정신적 부담이 커지는데, `%whos` 한 번이면 "지금 메모리 상태는 이렇다"가 명확해진다. hidden state 점검의 가벼운 도구로 좋다.

타입을 좁혀 보고 싶으면 `%who DataFrame` 같이 타입을 인자로 넘긴다.

### 7. `%%bash` / `!shell` — 셸과 매끄럽게 섞기

셸 명령을 돌려야 할 때가 있다. 디스크 사용량 확인, 파일 다운로드, 가상 환경 패키지 설치 — 이런 것들. 노트북을 떠나 터미널로 갈 필요 없이 같은 셀에서 처리하자.

한 줄짜리 셸 명령은 `!`를 앞에 붙인다.

```python
!ls -la data/
!pip install pandas
!wget https://example.com/data.csv -O sales.csv
```

여러 줄 셸 스크립트는 `%%bash` 셀 매직.

```python
%%bash
mkdir -p data/processed
cd data/raw
for f in *.csv; do
    cp "$f" "../processed/${f%.csv}_v2.csv"
done
echo "done"
```

`%%sh`도 거의 같은 역할인데 `%%bash`가 더 호환성이 좋다.

`!`로 친 명령의 결과를 변수로 받고 싶으면 이렇게 한다.

```python
files = !ls data/
print(files)   # ['raw', 'processed', 'sales.csv']
print(type(files))  # IPython.utils.text.SList
```

리스트처럼 다룰 수 있는 특수 객체로 받는다. 유용하다.

한 가지 권장사항: 패키지 설치는 `!pip install` 대신 `%pip install`을 쓰는 편이 낫다. `!pip`는 시스템 셸의 pip를 호출하는데, 그게 현재 노트북 커널이 쓰는 파이썬과 다를 수 있다. `%pip`는 노트북 커널의 파이썬을 정확히 짚어 설치한다. 환경 꼬임을 막아주는 작은 디테일이다.

```python
%pip install pandas matplotlib
```

마찬가지로 `%conda install` 매직도 있다.

### 한 묶음 — 셀 시간 측정과 자동 재실행

여덟 매직 중 가장 강력한 조합이 둘이다. 알아두면 작업 흐름이 한 단계 빨라진다.

**조합 1: `%%timeit` + 알고리즘 비교.** 같은 노트북의 두 셀에 두 알고리즘을 박고 `%%timeit`을 위에 얹어 비교한다. 한쪽은 list comprehension, 다른 쪽은 numpy vectorize — 누가 빠를지 따져볼 때 한 화면에 결과가 나란히 박혀 답이 즉시 보인다. 옛날엔 프로파일러를 띄워야 했던 일이 매직 두 줄로 끝난다.

**조합 2: `%load_ext autoreload` + `%pip install`.** 새 패키지를 깔고, 그 패키지의 함수를 호출하고, 그 함수가 의존하는 외부 모듈을 수정해도 — 커널 재시작 없이 다 반영된다. 큰 ML 실험에서 데이터 로드만 30분 걸릴 때 이 조합이 시간을 살린다.

**조합 3: `%%writefile utils.py` + `from utils import …` + autoreload.** 노트북에서 시작한 함수를 외부 모듈로 빼는 가장 빠른 패턴이다. `%%writefile`로 일단 파일을 만들고, autoreload가 켜져 있으면 그 파일을 에디터에서 계속 수정해도 노트북에 즉시 반영된다. 9장의 핵심 리팩토링 패턴이 이 셋의 조합 위에 서 있다.

### 8. 보너스 — 알아두면 좋은 것들

위 일곱 개가 매일 쓰는 것이라면, 다음은 한 달에 한 번쯤 쓸 만한 것들이다.

- `%debug` — 직전 셀이 에러로 죽었을 때, 그 자리의 디버거를 띄운다. `pdb`가 셀 안에서 동작.
- `%run script.py` — 외부 파이썬 스크립트를 노트북 네임스페이스에서 실행. 변수가 노트북에 그대로 들어온다.
- `%history` — 지금 세션에서 친 명령들의 기록.
- `%lsmagic` — 사용 가능한 모든 매직 목록.
- `%%capture` — 셀의 출력을 변수로 캡처(화면엔 안 띄우고 변수에만).

`%lsmagic`을 한 번 쳐서 전체 목록을 훑어보면 "어, 이런 것도 있네" 하고 발견하는 즐거움이 있다.

## 미니 데모 다섯 개 — 손으로 따라가보자

위 매직들을 묶어 짧은 워크플로우로 보자. 새 노트북을 열고 차례대로 따라 쳐보면 좋다.

### 데모 1 — 시간 측정으로 두 알고리즘 비교

```python
# 셀 1
%timeit sum(range(1_000_000))
```

```
8.42 ms ± 56.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

```python
# 셀 2
%%timeit
total = 0
for i in range(1_000_000):
    total += i
```

```
38.7 ms ± 412 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

내장 `sum`이 명시적 루프보다 4배 이상 빠르다. 이 차이를 print와 time으로 측정하려고 보일러플레이트 짜는 것보다 `%timeit` 두 번이 훨씬 깔끔하다.

### 데모 2 — 외부 모듈 만들고 즉시 임포트

```python
# 셀 1
%%writefile utils.py
def greet(name):
    return f"Hello, {name}!"

def shout(text):
    return text.upper() + "!!!"
```

```
Writing utils.py
```

```python
# 셀 2
%load_ext autoreload
%autoreload 2

from utils import greet, shout
print(greet("Toby"))
print(shout("ready"))
```

```
Hello, Toby!
READY!!!
```

이제 에디터에서 `utils.py`의 `greet` 함수를 수정해보자. 예를 들어 `f"안녕, {name}!"`로 바꾼다. 셀 2를 다시 실행하면 자동으로 새 정의가 임포트된다.

```python
# 셀 2 다시 실행
print(greet("Toby"))
```

```
안녕, Toby!
```

커널 재시작 없이 모듈 변경이 반영된다. 함수 추출 리팩토링이 가벼워지는 순간이다.

### 데모 3 — 셸 명령으로 환경 점검

```python
# 셀 1: 지금 쓰는 파이썬이 뭔지
import sys
print(sys.executable)
```

```
/Users/toby/.venv/notebook/bin/python
```

```python
# 셀 2: pip 목록
!pip list | head -10
```

```
Package           Version
----------------- -------
appnope           0.1.4
asttokens         2.4.1
attrs             23.2.0
certifi           2024.2.2
charset-normalizer 3.3.2
...
```

```python
# 셀 3: 패키지 설치 (커널 파이썬 확정)
%pip install -q seaborn
```

```
Note: you may need to restart the kernel to use updated packages.
```

`!which python`과 `import sys; sys.executable` — 이 두 가지를 새 환경에서 가장 먼저 확인하는 습관이 안전하다. 특히 conda + venv가 섞여 있는 환경에선 어느 파이썬이 뜨는지 헷갈리기 쉽다.

### 데모 4 — 메모리 상태 점검

```python
# 셀 1
import pandas as pd
import numpy as np

df = pd.DataFrame({"x": np.arange(1000), "y": np.random.randn(1000)})
arr = np.zeros((100, 100))
threshold = 0.5
```

```python
# 셀 2
%who
```

```
arr      df      np      pd      threshold
```

```python
# 셀 3
%whos
```

```
Variable    Type         Data/Info
-----------------------------------
arr         ndarray      100x100: 10000 elems, type `float64`, 80000 bytes
df          DataFrame    [1000 rows x 2 columns]
np          module       <module 'numpy' from '/...'>
pd          module       <module 'pandas' from '/...'>
threshold   float        0.5
```

긴 노트북에서 한 시간쯤 작업한 다음 `%whos`를 치면 "아 맞다, 이 변수 만들어뒀지" 하고 떠오르는 것들이 있다. 정신적 캐시를 한 번 비워주는 효과가 있다.

### 데모 5 — 환경 변수와 셸 통합

```python
# 셀 1
%env DATA_DIR=/tmp/data
%env PYTHONHASHSEED=0
```

```
env: DATA_DIR=/tmp/data
env: PYTHONHASHSEED=0
```

```python
# 셀 2
%%bash
mkdir -p $DATA_DIR
echo "id,value" > $DATA_DIR/sample.csv
echo "1,100" >> $DATA_DIR/sample.csv
echo "2,200" >> $DATA_DIR/sample.csv
ls -la $DATA_DIR
```

```
total 8
drwxr-xr-x  3 toby  wheel   96 May  6 13:22 .
drwxr-xr-x 12 root  wheel  384 May  6 13:22 ..
-rw-r--r--  1 toby  wheel   25 May  6 13:22 sample.csv
```

```python
# 셀 3
import os
import pandas as pd

df = pd.read_csv(os.path.join(os.environ["DATA_DIR"], "sample.csv"))
df
```

```
   id  value
0   1    100
1   2    200
```

`%env`로 설정한 환경 변수가 셸 셀에서도, 파이썬 셀에서도 같은 값으로 보인다. 데이터 경로 같은 걸 한 곳에서 관리할 수 있다.

이 다섯 데모를 직접 쳐보면 매직이 단순한 편의 기능이 아니라 작업 흐름을 바꾸는 도구라는 게 손으로 잡힌다.

## 노트북 파일 포맷 둘 — `.ipynb`와 percent format

도구상자의 마지막 한 가지. 노트북이 디스크에 어떻게 저장되는지 보자. 이걸 알아야 git 협업, 배포, 자동화 같은 다음 단계가 열린다.

### `.ipynb` — JSON 직렬화

기본 포맷은 `.ipynb`. 이름과 다르게 사실은 그냥 JSON 파일이다. 텍스트 에디터로 열어보면 이런 모양이다.

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 데이터 로드\n",
    "\n",
    "오늘의 매출 데이터를 읽는다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": ["<div>...table HTML...</div>"],
      "text/plain": ["   id  amount\n0   1    1000\n1   2    2500"]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "df = pd.read_csv('sales.csv')\n",
    "df.head()"
   ]
  }
 ],
 "metadata": { "kernelspec": { "name": "python3" } },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

코드, 출력(셀에 박힌 표·이미지·텍스트), 메타데이터가 한 파일에 다 들어 있다. 이게 장점이자 단점이다.

**장점:** 노트북을 그 자체로 공유할 수 있다. 누군가에게 `.ipynb`를 보내면 받은 사람은 코드를 다시 돌리지 않고도 결과를 본다. GitHub가 `.ipynb`를 자동 렌더링하는 것도 출력이 파일에 박혀 있기 때문이다.

**단점:** 사람이 읽기 끔찍하다. 그리고 git diff가 거의 의미 없다. 셀 하나의 출력만 바뀌어도 base64 인코딩된 이미지 데이터가 통째로 diff에 떠버린다. 두 사람이 같은 노트북을 만지면 머지 충돌이 답이 없다.

`.ipynb`의 이 문제는 노트북의 가장 큰 협업 장애물이다. 10장에서 이 문제를 푸는 도구 세 가지(Jupytext, nbdime, ReviewNB)를 다룬다. 미리 한 번 맛만 보자.

### percent format — 노트북을 `.py`로 표현하기

같은 노트북을 순수 파이썬 스크립트로 쓰면 어떨까. 셀 구분만 주석으로 박아두면 되지 않을까.

이게 percent format이다. 약속은 단순하다.

- `# %%` 한 줄이 새 코드 셀의 시작
- `# %% [markdown]`은 마크다운 셀의 시작
- 그 아래는 그냥 평범한 파이썬 코드 또는 주석

위에서 봤던 `.ipynb` 예시를 percent format으로 옮기면 이렇게 된다.

```python
# %% [markdown]
# # 데이터 로드
#
# 오늘의 매출 데이터를 읽는다.

# %%
import pandas as pd
df = pd.read_csv("sales.csv")
df.head()

# %% [markdown]
# ## 결측치 점검

# %%
df.isna().sum()
```

이 파일을 `eda.py`로 저장한다. 그리고 JupyterLab, VS Code, PyCharm, Spyder, Marimo — 이 모두가 이 파일을 노트북으로 인식한다. `# %%` 마커를 보고 셀 경계를 자동으로 그어준다.

장점이 분명하다.

- **git diff가 정상이다.** 그냥 파이썬 코드 diff니까. 한 줄 바뀌면 한 줄만 보인다.
- **머지가 평소처럼 된다.** 충돌이 나도 코드 충돌이라 사람이 읽고 풀 수 있다.
- **에디터 친화.** `.py` 파일이니까 자동완성, 정의로 이동, 리팩토링이 다 동작한다.
- **CI에서 그냥 돌릴 수 있다.** `python eda.py`로 실행 가능. (마크다운 셀은 주석이라 무시되고 코드만 돈다.)

단점은 출력이 파일에 안 박힌다는 것. 그래서 GitHub에서 노트북처럼 표·이미지를 바로 보여주지 못한다. 결과를 보려면 누군가 한 번 실행해야 한다.

percent format이 어디서 왔는지 짧게 짚어두자. Spyder와 PyCharm 같은 IDE가 데이터 작업자에게 노트북 같은 사용감을 제공하기 위해 만든 컨벤션이다. 평범한 `.py`인데 IDE가 셀 경계를 인식해서 셀 단위 실행 버튼을 달아준다. VS Code도 이 컨벤션을 일찍 흡수했다.

같은 컨벤션을 Jupyter 진영에서 받아들여 `.ipynb`와 호환시킨 것이 다음에 볼 Jupytext다. 그래서 percent format은 Jupyter 진영의 발명이라기보단 IDE 진영에서 시작된 표준을 모두가 같이 쓰게 된 사례에 가깝다.

### Jupytext — 두 포맷의 다리

그러면 어느 쪽을 써야 할까. 둘 다 쓰자. **Jupytext**가 두 포맷을 양방향 동기화해준다.

```bash
pip install jupytext
```

설치하면 JupyterLab 안에서 `.py` 파일을 노트북 UI로 열 수 있고, 반대로 `.ipynb`를 percent `.py`와 한 쌍으로 묶어둘 수 있다. 한 쌍을 페어링하면 한쪽을 고치면 다른 쪽이 자동으로 업데이트된다.

명령줄에서는 이렇게 쓴다.

```bash
# .ipynb를 percent .py로 변환
jupytext --to py:percent eda.ipynb

# .py를 .ipynb로 (출력 없이)
jupytext --to ipynb eda.py

# 두 포맷을 페어로 묶기
jupytext --set-formats ipynb,py:percent eda.ipynb
```

페어링 후엔 `.py`를 git에 커밋하고, `.ipynb`는 `.gitignore`에 넣어 무시한다. 출력이 보고 싶으면 `.ipynb`를 로컬에서 생성해 본다. 이 패턴이 노트북 git 협업의 사실상 표준이다. 10장에서 nbdime, ReviewNB와 비교하며 본격적으로 다룬다.

pre-commit hook으로 강제할 수도 있다. 누군가 `.ipynb`만 커밋하려 하면 hook이 막고 자동으로 `.py`를 같이 만든다. 팀 컨벤션을 자동화하기 좋은 패턴이다.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/mwouts/jupytext
    rev: v1.16.0
    hooks:
      - id: jupytext
        args: [--sync]
```

```bash
pip install pre-commit
pre-commit install
```

이 정도면 노트북 한 권을 안전하게 git에 올릴 기본기가 갖춰진다.

지금은 이 한 가지만 머리에 두자. **`.ipynb`는 결과를 박은 직렬화 포맷, percent format은 git 친화적인 코드 포맷.** 둘 다 쓰임새가 있다.

## 자기 매직 만들기 — 한 단계 더

매직이 IPython의 일부라고 했다. 그 말은 자기가 매직을 정의해 등록할 수 있다는 뜻이다. 자주 쓰는 패턴이 있으면 매직으로 빼두면 호출이 짧아진다.

```python
from IPython.core.magic import register_line_magic, register_cell_magic

@register_line_magic
def hello(name):
    return f"안녕, {name}!"

@register_cell_magic
def upper(line, cell):
    return cell.upper()
```

이 셀을 한 번 실행해두면 그 노트북 세션 동안 `%hello`와 `%%upper`가 매직으로 동작한다.

```python
%hello Toby
# 결과: '안녕, Toby!'

%%upper
hello world
this is a test
# 결과: 'HELLO WORLD\nTHIS IS A TEST\n'
```

자주 쓰는 작업을 매직으로 빼두면 코드가 깔끔해진다. 다만 이게 정말 매직이 필요한 일인지, 그냥 함수면 되는 일인지는 한 번 따져볼 만하다. 함수는 다른 사람이 쓰기에 명확하지만, 매직은 IPython 컨텍스트 안에서만 동작한다. 노트북 안에서만 쓰는 헬퍼라면 매직으로, 다른 모듈에서도 import해 쓸 거라면 함수로 — 이렇게 갈라지는 게 보통이다.

자기 회사 데이터 플랫폼에 자주 쓰는 SQL 쿼리, 자주 쓰는 데이터 로드 패턴을 매직으로 빼두면 새 직원의 학습 곡선이 가팔라지지 않는다. `%load_data sales 2026-05`처럼 호출 한 줄이면 된다. 큰 데이터팀에서 자주 보는 패턴이다.

## 환경 변화에도 통하는 매직, 통하지 않는 것들

매직이 어디서나 통한다고 했지만 100%는 아니다. 짚어두자.

**다 통하는 매직:** `%timeit`, `%%timeit`, `%who`, `%whos`, `%env`, `%load_ext autoreload`, `%autoreload 2` — IPython 코어에 들어 있어서 어디서든 같다.

**환경별로 다른 매직:**
- `%matplotlib inline` vs `%matplotlib widget`: `widget`은 ipympl 패키지 필요. Colab에선 `inline`만 기본 동작, `widget`은 별도 설치.
- `%%bash`: 셸이 있는 환경에서만. Windows에선 동작 보장 안 됨.
- `!pip install`: Colab에선 노트북 환경 자체에 깔고, 자기 컴퓨터에선 시스템 파이썬 또는 활성 가상환경에 깔린다. `%pip`가 안전한 이유다.

**Databricks의 매직:** Databricks Notebooks는 `%sql`, `%scala`, `%python`, `%md`, `%md` 같은 매직이 있다. 이건 IPython 매직이 아니라 Databricks가 자체로 만든 셀 단위 언어 전환 시스템이다. 다른 환경에선 동작하지 않는다.

**Marimo:** Marimo는 IPython 매직을 지원하지 않는다. 자체 reactive 모델 위에서 도니까. `%timeit` 대신 `mo.profile()` 같은 자체 API를 쓴다(7장).

매직이 안 통할 때는 보통 그 환경 문서에 대안이 있다. 처음 새 환경에서 매직이 동작하지 않으면 당황하지 말고 그 환경의 cheat sheet를 한 번 찾아보자.

## Jupytext 한 워크플로우 — 손에 잡히게

Jupytext가 어떻게 동작하는지 짧은 워크플로우로 보자. 새 프로젝트를 시작한다고 가정하자.

```bash
mkdir my-analysis
cd my-analysis
python -m venv .venv
source .venv/bin/activate
pip install jupyterlab jupytext pandas matplotlib
```

JupyterLab을 띄우고 새 노트북을 만든다. `eda.ipynb`라고 저장한다.

이제 같은 노트북을 percent `.py`와 페어링하자.

```bash
jupytext --set-formats ipynb,py:percent eda.ipynb
```

이 명령이 `eda.py`를 만들어낸다. 두 파일이 한 쌍이 됐다. JupyterLab에서 셀을 추가하면 `eda.ipynb`에 저장되고, Jupytext 확장이 그걸 감지해 `eda.py`도 같이 업데이트한다.

```bash
ls
# eda.ipynb  eda.py
```

`eda.py`를 텍스트 에디터로 열어보면 percent format으로 들어가 있다.

```python
# %%
import pandas as pd
df = pd.read_csv("data/sales.csv")
df.head()

# %% [markdown]
# ## 결측치 점검
```

이제 git에 올릴 준비를 하자.

```bash
git init
echo "*.ipynb" > .gitignore
echo ".venv/" >> .gitignore
git add eda.py .gitignore
git commit -m "초기 EDA 노트북"
```

`.ipynb`는 `.gitignore`에 박아 git이 무시하게 한다. `.py`만 커밋한다. 다른 사람이 이 repo를 클론하면:

```bash
git clone <repo>
cd my-analysis
python -m venv .venv
source .venv/bin/activate
pip install jupyterlab jupytext pandas matplotlib
jupyter lab eda.py    # .py를 노트북 UI로 연다
```

Jupytext가 깔려 있으면 `.py`를 노트북처럼 연다. 출력은 비어 있지만(파일에 안 박혔으니까), 셀을 한 번 실행하면 결과가 뜬다. 또는 `jupytext --to ipynb eda.py`로 `.ipynb`를 명시적으로 만들 수도 있다.

이 패턴의 장점이 분명해진다. **git에 올라가는 건 깔끔한 `.py` 코드뿐.** diff가 정상이고, 머지가 가능하고, 코드 리뷰가 살아 있다. 노트북의 결과는 각자 로컬에서 만들어 본다.

## 정리 — 환경이 바뀌어도 통하는 무기

이 장에서 손에 넣은 것들을 정리하자.

- 매직은 **커널** 쪽에 들어 있다. 그래서 환경이 바뀌어도 그대로 통한다.
- **라인 매직 `%`**는 한 줄, **셀 매직 `%%`**는 셀 전체.
- 매일 쓰는 여덟 개: `%timeit`, `%%writefile`, `%matplotlib inline/widget`, `%load_ext autoreload` + `%autoreload 2`, `%env`, `%who/%whos`, `%%bash`, `!shell`. 패키지 설치는 `%pip install`을 권장.
- 노트북 파일은 두 포맷이 있다. `.ipynb`(JSON, 결과 박힘)와 percent format(`.py`, git 친화). Jupytext가 둘을 양방향 동기화.

이 도구상자를 손에 쥐고 있으면 환경 투어(4~8장)가 한결 가벼워진다. 매직과 파일 포맷이 어디서 같고 어디서 다른지 — 그 비교가 환경별 강점·약점을 가른다. 예를 들어 Marimo는 매직을 지원하지 않는 대신 의존 그래프로 자동 재실행을 한다. Databricks는 매직을 자체 확장해 셀별 언어 전환에 쓴다. Colab은 표준 매직을 다 지원하면서 Drive 마운트 같은 자체 매직을 추가했다. 같은 매개념이 환경마다 다르게 자라는 모양을 보는 게 이 책의 한 즐거움이다.

이걸 손에 들고 다음 장으로 가자. 4장에서는 노트북의 표준, **Jupyter 생태계** 전체를 한 번에 그린다. JupyterLab, Jupyter Notebook, Jupyter Server, JupyterHub, BinderHub — 이름이 비슷한 다섯 컴포넌트가 어떻게 묶여 있고, 각자 어떤 자리를 차지하는지 가계도로 정리한다. 그리고 자기 컴퓨터에서 첫 노트북을 띄우는 가장 빠른 한 줄도 같이 본다.
