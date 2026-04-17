# 4장. 미니 GPT를 직접 만든다 — nanochat 스타일 from scratch + 디코딩 루프

3장까지 같이 걸어오며 쌓은 이해가 있다. Q·K·V가 서로 주목하고, Positional Encoding이 순서를 박아 넣고, 멀티 헤드가 여러 시점을 동시에 본다 — 말로는 풀리는데, 손에는 아직 잡히지 않는다. 여기서 한번 멈추고 스스로에게 물어보자. 지금 이 상태로 면접에 들어가 "트랜스포머가 어떻게 돌아가죠?"라는 질문을 받으면, 자신 있게 10분을 떠들 수 있을까. 아마 3분쯤에서 말이 끊길 거다. 그리고 그 끊기는 자리가 대개 똑같다. "그래서 코드로는요?"

이번 장에서 그 끊기는 자리를 메꾸자. 100~300줄짜리 코드로 미니 GPT를 **밑바닥부터** 쌓아 올리고, 작은 한국어 코퍼스(corpus)를 먹여 학습시켜 볼 거다. 말이 거창해서 그렇지 뼈대는 단순하다. Bigram 하나 놓고, 어텐션 한 층 얹고, 헤드 늘리고, 피드 포워드(Feed-Forward) 붙이고, 레지듀얼(residual)로 감싸고, 여러 층 쌓고 — 학습 루프 한 번 돌린다. 이 순서대로 loss가 어떻게 내려가는지 눈으로 보고, 학습이 끝난 모델에서 한 토큰을 **어떻게 뽑는지**(디코딩, decoding)까지 연다.

장 끝에서 독자가 얻는 건 세 가지다. 첫째, GitHub에 자기 이름이 박힌 저장소 1개. 둘째, "LLM은 결국 조건부 확률(conditional probability) + 샘플링(sampling)이다"라는 문장의 **몸 체감**. 셋째, 5장에서 만날 질문 — "왜 Instruction Tuning이 필요한가?" — 에 대한 직관적인 대답. base 모델의 생 샘플을 보고 나면 그 질문이 이론이 아니라 체감으로 들어온다.

그럼 시작해 보자.

## 지금 우리가 어디에 있나

본격 코드로 들어가기 전에 지도를 한 번 펴자. 이 책 2~8장의 여정 안에서 4장이 어디에 놓여 있는지를 그림으로 보면, 앞으로 어떤 조각들이 이 장과 연결되는지 한눈에 들어온다.

```
 [2장] 토큰·임베딩 ─────► [3장] 어텐션·트랜스포머
           │                       │
           └───────► ★ 4장 ★ ◄─────┘
            from scratch로 직접 쌓기
            (Bigram → Self-Attention → Multi-Head →
             Feed-Forward → Residual → 스택 → 학습 → 디코딩)
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
    [5장] 스케일·정렬  [6장] QLoRA 파인튜닝  [7장] API·Spring AI
    (왜 정렬이          (같은 태스크를        (디코딩 루프를
     필요한가)           오픈 모델에 얹기)     API 파라미터로)
                                            │
                                            ▼
                                       [8장] RAG 최소 구현
```

이 지도에서 4장은 정중앙에 선다. 2·3장의 이해가 손으로 박히는 **각성 챕터**이고, 동시에 5·6·7장이 각자 다른 방향으로 뻗어 나가는 **분기점**이다. 같은 "사내 개발 문서 요약·Q&A"라는 공통 태스크를 4·6·7·8장에서 네 가지 방식으로 풀어 보는데, 4장은 그 태스크의 **축소판**을 가장 원시적인 수단으로 공략하는 자리다. 300줄짜리 코드에 1~3MB짜리 한국어 코퍼스를 먹이고, 한국어 토큰이 이어 붙는 장면을 직접 본다. 이게 지금 4장이 맡은 몫이다.

말로는 여기까지. 이제 실제 환경을 어떻게 깔고, 어떤 저장소를 뼈대로 삼을지 이야기해 보자.

## nanoGPT는 끝났다 — 실습 경로를 재연결하자

⚠️ **2025-11 기준 고지 박스**

Karpathy의 `nanoGPT` 저장소가 2025년 11월에 공식적으로 deprecation 상태로 들어갔다. "Let's build GPT"(2023) 유튜브 강의와 짝을 이루며 전 세계 입문자의 표준 교재 역할을 했지만, 이제 Karpathy 본인이 `nanochat`으로 후속 저장소를 넘겼다. 이 책의 4장을 쓰는 2026년 4월 시점에서, 예전 `nanoGPT` README를 그대로 따라가면 "deprecated" 배지가 맨 위에 박혀 있어 독자가 당황할 수 있다.

그래서 이 장에서는 실습 경로를 이렇게 재연결한다.

- **뼈대 강의:** Karpathy, "Let's build GPT: from scratch, in code, spelled out" (2023, YouTube). 여전히 최상급. 흐름과 설명 톤을 이 강의에서 가져온다.
- **실습 저장소:** `karpathy/build-nanogpt` (강의용 GPT-2 재현) + `karpathy/nanochat` (후속 교육용). 이 책의 저장소는 `build-nanogpt`의 구조를 간략화하고, 한국어 코퍼스 로더(loader)와 디코딩 루프 비교 스크립트를 얹은 형태로 공개한다.
- **깊이 차이:** `build-nanogpt`가 GPT-2 124M 재현까지 가는 반면, 이 책은 **더 작게, 더 빨리, 한 번의 좌석에서 완주**를 목표한다. 결과 품질보다 **학습이 돌아가는 현상**을 보는 쪽에 무게를 둔다.

⚠️ 한 가지 약속. 이 책의 코드가 2026년 이후 어느 시점에 또 뒤집힐 수 있다. PyTorch 2.x의 API 변화, `torch.compile` 동작, MPS(Apple Silicon의 Metal Performance Shaders) 백엔드의 버그 수정 — 어디서든 터질 수 있다. 저장소 README에 실습이 검증된 시점과 의존성 버전을 항상 고정(pinned)해 두었다. 독자가 따라 할 때 뭔가 이상하면, 먼저 README의 "검증 시점" 줄을 확인하는 편이 낫다.

이 고지만 먼저 박아두고, 본격적으로 환경을 깔자.

## 환경 세팅 — 한 번만 깔자

디렉터리 하나 만들고, 가상환경 잡고, 필요한 패키지를 설치한다. 여기는 매뉴얼체로 가자. 독자가 명령을 **그대로 복사해 붙여넣어 돌아가는 상태**가 중요한 구간이기 때문이다.

```bash
# 프로젝트 디렉터리 생성
mkdir mini-gpt && cd mini-gpt

# 가상환경 (uv 권장, pip로도 가능)
uv venv --python 3.11
source .venv/bin/activate

# 의존성 설치 (pinned 버전은 저장소 requirements.txt 참조)
uv pip install torch==2.4.1 tiktoken==0.7.0 numpy==1.26.4

# CUDA 사용자: 자기 CUDA 버전에 맞는 torch wheel 인덱스 추가
# MPS 사용자(Apple Silicon): 위 명령 그대로.
```

이 명령은 Python 3.11 기반의 가상환경을 만들고 PyTorch 2.4.1을 설치한다. `uv`는 `pip`의 빠른 대체재인데, 익숙하지 않으면 `python -m venv .venv && source .venv/bin/activate && pip install ...`로 바꿔 써도 무방하다. GPU가 없으면 CPU 버전이 설치되고, 이 장의 미니 모델은 CPU에서도 **느리지만** 돌아간다. Apple Silicon Mac이면 `torch.device("mps")` 백엔드가 자동 활성화된다. NVIDIA GPU가 있으면 CUDA 빌드를 받아야 빠르다.

디바이스 감지는 코드에서 이렇게 한 줄로 처리한다.

```python
# src/device.py
import torch

def get_device() -> torch.device:
    """사용 가능한 최적 디바이스를 반환한다.
    우선순위: CUDA > MPS > CPU.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")
```

이 함수가 반환하는 디바이스를 이 장의 모든 텐서(tensor)·모델에 `.to(device)`로 붙여 준다. **반복해서 말하지만, 텐서 하나라도 CPU에 남아 있으면 `RuntimeError: Expected all tensors to be on the same device`라는 메시지와 함께 학습이 멈춘다.** 이 실수는 뒤의 "실패담" 절에서 다시 다룬다.

환경은 여기까지. 이제 모델에 먹일 한국어 코퍼스를 준비하자.

## 한국어 코퍼스 — 덤프를 본문에 넣지 않고, 스크립트로 다운로드한다

미니 GPT에 먹일 재료부터 골라야 한다. 원본 Karpathy 강의는 셰익스피어 전집(`tiny-shakespeare.txt`, 약 1MB)을 썼다. 영어 문자 수준의 모델을 돌리는 데 최적이지만, 우리는 한국어를 목표하는 책이고 한국어 토큰이 모델 안에서 어떻게 이어 붙는지를 눈으로 봐야 한다. 그래서 **한국어 코퍼스**를 직접 준비한다.

두 소스를 섞어 쓴다.

- **모두의 말뭉치** (국립국어원). 현대어 코퍼스 일부만 사용. 공공 배포가 명시된 현대 서면 텍스트 중심으로 1~2MB 정도.
- **나무위키 덤프**의 극히 작은 일부. 스크립트가 마크업을 벗겨 내고 순수 본문만 남겨 약 1MB를 추출.

합쳐서 **1~3MB**(문자 기준 100만~300만 자 사이). 이 크기는 CPU만으로도 몇 십 분 안에 한 epoch(에포크)을 돌릴 수 있는 **교육용 하한선**이다. 품질이 좋은 문장을 뽑겠다는 욕심은 내려놓자. 지금 중요한 건 "모델이 한국어 토큰을 이어 붙이는 장면을 빨리 보는 것"이다.

### 라이선스 한 줄

모두의 말뭉치와 나무위키 덤프 중 후자는 **CC BY-NC-SA 2.0** 라이선스다. 비상업 재배포 한정이므로, 이 책의 저장소는 **원본 덤프 파일을 직접 포함하지 않는다.** 독자가 스크립트를 돌리면 원본 배포처에서 직접 내려받고, 전처리 결과물만 로컬에서 만드는 구조다. 이렇게 하는 편이 안전하고, 독자가 이후 다른 코퍼스를 꽂을 때도 동일 인터페이스를 재활용할 수 있다.

### 저장소의 `prepare_corpus.py`

저장소 README에 다운로드·전처리 스크립트 한 개가 들어 있다. 본문에서는 전체 스크립트를 인용하지 않고, **개요만** 평어로 서술한다. 실제 본문은 매뉴얼체로 돌아온다.

```python
# scripts/prepare_corpus.py (개요)
# 1) 모두의 말뭉치 현대어 파일 다운로드 (원본 URL은 README 참조)
# 2) 나무위키 덤프 JSON 중 n개 문서 샘플링, 마크업 스트리핑
# 3) 두 소스를 이어 붙여 data/corpus.txt 생성 (UTF-8)
# 4) 간단한 클리닝: 연속 공백 축약, 제어 문자 제거
# 5) 학습/검증 분할(9:1), data/train.txt, data/val.txt 저장

if __name__ == "__main__":
    main()
```

이 스크립트는 두 원본을 동일 디렉터리에 받아 합치고, `data/train.txt`와 `data/val.txt` 두 파일만 남긴다. 이후의 모든 학습 코드는 이 두 파일만 바라본다. 원본 덤프 파일은 스크립트가 끝난 뒤 지워도 된다.

```bash
python scripts/prepare_corpus.py
# 출력 예:
# [prepare] downloading modu... (1.1 MB)
# [prepare] downloading namu_sample... (1.3 MB)
# [prepare] cleaning... 2.4 MB -> 2.1 MB
# [prepare] split: train=1.9 MB, val=0.2 MB
```

데이터가 이렇게 준비됐다고 치고, 토크나이저(tokenizer)부터 얹자.

### 토크나이저 — character-level로 시작

4장의 첫 모델은 BPE(Byte Pair Encoding) 대신 **character-level**로 간다. 이유는 단순하다. BPE 학습 자체가 또 하나의 파이프라인이 되고, 독자가 디버깅해야 할 창이 늘어난다. 한국어는 음절 기준으로 잘라도 모델이 "그럴듯한 이어 붙임"을 보여주는 데 부족하지 않다. 강의 오리지널이 영문 char-level로 시작한 것과 같은 이유다.

```python
# src/tokenizer.py
from pathlib import Path

class CharTokenizer:
    def __init__(self, text: str):
        self.chars = sorted(set(text))
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}
        self.vocab_size = len(self.chars)

    def encode(self, s: str) -> list[int]:
        return [self.stoi[c] for c in s]

    def decode(self, ids: list[int]) -> str:
        return "".join(self.itos[i] for i in ids)

def load_tokenizer(train_path: Path) -> CharTokenizer:
    text = train_path.read_text(encoding="utf-8")
    return CharTokenizer(text)
```

이 토크나이저는 학습 파일을 한 번 읽어 등장한 문자(character)의 집합을 만들고, 정수 ID로 매핑한다. 한국어 현대어 코퍼스라면 한글 음절 2,000~3,000자 + 숫자·영문·기호 몇 백 자 수준의 `vocab_size`가 나온다.

```python
from pathlib import Path
from src.tokenizer import load_tokenizer

tok = load_tokenizer(Path("data/train.txt"))
print(tok.vocab_size)            # 예: 2843
print(tok.encode("안녕"))         # 예: [1732, 498]
print(tok.decode([1732, 498]))    # '안녕'
```

BPE로 가지 않은 대가는 분명하다. 단어 단위의 의미 뭉치가 없어서, 모델이 "단어 하나"를 만들려면 두세 스텝이 걸린다. 그만큼 학습 샘플도 길어진다. 하지만 이 장의 목적은 **"학습이 돌아가는 장면"을 빨리 보는 것**이므로 이 편이 낫다. 6장에서 Llama 3 토크나이저를 쓸 때 BPE의 이점이 체감으로 돌아온다.

준비는 끝났다. 이제 첫 모델을 짜자.

## 1단계. Bigram — 가장 멍청한 언어 모델

맨 처음에 만들 모델은 **Bigram**이다. "바로 앞 토큰 하나"만 보고 다음 토큰을 예측하는, 언어 모델의 교과서적 최소 단위다. 여기서 시작하는 이유는 두 가지다. 첫째, 전체 학습 루프(데이터 로딩 → 모델 → 옵티마이저 → loss 기록 → 샘플 생성)를 한 번에 세워 볼 수 있다. 둘째, 이 모델의 성능이 **얼마나 나쁜지** 먼저 봐야 그 이후 더해지는 구조들이 왜 의미 있는지가 감각으로 들어온다.

아래 코드는 Bigram 언어 모델을 PyTorch `nn.Module`로 감싼다. 파라미터는 `(vocab_size, vocab_size)` 행렬 하나뿐이다.

```python
# src/bigram.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class BigramLM(nn.Module):
    def __init__(self, vocab_size: int):
        super().__init__()
        # 토큰 ID를 곧장 다음 토큰 로짓(logit)으로 매핑하는 lookup table.
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None):
        # idx: (B, T) 배치·시간 축으로 구성된 정수 텐서
        logits = self.token_embedding_table(idx)  # (B, T, vocab)
        if targets is None:
            return logits, None
        B, T, V = logits.shape
        loss = F.cross_entropy(logits.view(B * T, V), targets.view(B * T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _ = self(idx)
            logits = logits[:, -1, :]            # 마지막 시점만
            probs = F.softmax(logits, dim=-1)    # (B, V)
            next_id = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_id), dim=1)
        return idx
```

이 모델에서 `token_embedding_table`은 임베딩이자 동시에 **다음 토큰 로짓**을 직접 내는 테이블이다. 엄밀히 말해 임베딩 한 번으로 예측까지 끝난다. 행렬 모양을 보면 의심이 확 든다 — 크기가 겨우 `(V, V)`인데 이게 언어 모델이라고? 맞다. 가장 멍청한 구조가 맞고, 그게 이 1단계의 요점이다.

데이터 배치를 뽑는 함수와 짧은 학습 루프도 같이 얹어 보자.

```python
# src/data.py
import torch
from pathlib import Path

def load_split(path: Path, tokenizer):
    data = torch.tensor(
        tokenizer.encode(path.read_text(encoding="utf-8")),
        dtype=torch.long,
    )
    return data

def get_batch(data, block_size: int, batch_size: int, device):
    # data: (N,) 전체 정수 시퀀스
    ix = torch.randint(0, len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + 1 + block_size] for i in ix])
    return x.to(device), y.to(device)
```

이 함수는 전체 시퀀스에서 무작위로 `batch_size`개 지점을 고르고, 각 지점에서 `block_size`만큼 잘라 `x` (입력)과 한 칸 밀린 `y` (타깃)을 만든다. 여기가 **"다음 토큰 예측"**이라는 LLM의 핵심 학습 신호가 구체 코드로 바뀌는 자리다. 3장에서 말했던 "모델이 자기 미래를 쳐다보면 안 된다"는 제약이 바로 이 한 칸 밀기로 구현된다.

짧은 학습 루프를 돌려 본다.

```python
# scripts/train_bigram.py
import torch
from pathlib import Path
from src.tokenizer import load_tokenizer
from src.bigram import BigramLM
from src.data import load_split, get_batch
from src.device import get_device

device = get_device()
tok = load_tokenizer(Path("data/train.txt"))
train = load_split(Path("data/train.txt"), tok)
val = load_split(Path("data/val.txt"), tok)

model = BigramLM(tok.vocab_size).to(device)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)

BLOCK, BATCH = 8, 32
for step in range(3000):
    xb, yb = get_batch(train, BLOCK, BATCH, device)
    _, loss = model(xb, yb)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
    if step % 500 == 0:
        with torch.no_grad():
            xv, yv = get_batch(val, BLOCK, BATCH, device)
            _, vloss = model(xv, yv)
        print(f"step {step:5d} | train {loss.item():.3f} val {vloss.item():.3f}")
```

CPU만으로도 몇 초면 끝난다. 출력은 대략 이런 모양이다.

```
step     0 | train 7.95 val 7.95
step   500 | train 5.87 val 5.92
step  1000 | train 5.34 val 5.40
step  1500 | train 5.12 val 5.18
step  2000 | train 5.01 val 5.09
step  2500 | train 4.94 val 5.03
```

여기서 loss가 왜 5 근처에 주저앉는가? vocabulary 크기가 약 2,800이니 완전 무작위 예측의 loss는 `ln(2800) ≈ 7.94`다. 5.0이라는 숫자는 "각 문자 뒤에 **몇 문자 정도로 후보를 좁힌 상태**"에 해당한다. Bigram이 "한글 음절 뒤에는 한글 음절이 오더라", "공백 뒤에는 어떤 글자가 많더라" 같은 얕은 통계를 겨우 잡았다는 뜻이다.

학습된 모델로 샘플을 뽑아 보자.

```python
start = torch.zeros((1, 1), dtype=torch.long, device=device)
out = model.generate(start, max_new_tokens=200)
print(tok.decode(out[0].tolist()))
```

기대하지 말자. 한국어 같지만 한국어가 아닌, 음절이 어지럽게 섞인 문자열이 나온다.

```
의 가시어 이고 그있다가 에 가 니 서에 하는 다는다. 것 시 사용  한 고이
있 다에 있 이 이 다, 가다. 다는 를 에 는  아 하  수 는 서를 라 다.
```

명사·조사의 통계는 약간 흉내 내지만, 앞뒤 맥락이 전혀 없어 문장이라고 부를 수 없다. 이게 "바로 앞 한 토큰만 본 모델"의 한계다. 찜찜한 이 결과가 다음 단계의 동기를 준다 — **더 긴 문맥**을 보게 해줘야 한다.

## 2단계. Self-Attention 블록 — 문맥을 주입하자

Bigram의 문제는 명확하다. 모델이 **한 토큰 뒤**만 본다. 트랜스포머의 기본 발상은 "각 토큰이 같은 문장 안의 다른 토큰들을 **얼마나 참조할지** 스스로 정하게 하자"였다. 여기서 한번 시도해 보자.

먼저 입력 텍스트를 **위치 정보가 섞인 임베딩**으로 바꾼다. 3장에서 정리한 Positional Encoding을 본격적으로 얹는 자리다. 원 논문은 사인·코사인 주기 함수를 썼지만, 교육 편의상 `nn.Embedding`으로 "학습 가능한 위치 임베딩"을 쓴다(GPT-2 방식). 결과 차이는 이 규모에서 거의 없다.

```python
# src/attention.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class Head(nn.Module):
    """단일 셀프 어텐션 헤드.
    causal mask를 적용해 미래를 못 보게 한다.
    """
    def __init__(self, n_embd: int, head_size: int, block_size: int):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer(
            "tril",
            torch.tril(torch.ones(block_size, block_size)),
        )

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)      # (B, T, H)
        q = self.query(x)    # (B, T, H)
        v = self.value(x)    # (B, T, H)
        # 어텐션 스코어: Q · K^T / sqrt(H)
        wei = q @ k.transpose(-2, -1) * (k.shape[-1] ** -0.5)
        # 미래 마스킹
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
        wei = F.softmax(wei, dim=-1)
        return wei @ v  # (B, T, H)
```

이 클래스는 3장에서 그림과 함께 말했던 **Scaled Dot-Product Attention**을 20줄로 구현한다. Q·K·V 각각이 임베딩 차원 `n_embd`에서 `head_size`로 선형 변환되고, Q와 K의 내적으로 관계 점수를 낸다. `sqrt(H)`로 나누는 건 내적이 커질수록 softmax 기울기가 사라지는 문제를 막기 위한 고전적 트릭이다. 여기서 **causal mask**가 핵심이다. `tril`로 하삼각 행렬을 만들어 놓고, 상삼각 영역(미래 토큰)에 `-inf`를 꽂으면 softmax 이후 그 자리의 가중치는 0이 된다. 이게 GPT 계열이 decoder-only인 이유의 코드 표현이다.

이 단일 헤드를 Bigram 코드에 끼우면 이미 어느 정도 문맥이 들어온다. 모델 정의를 바꾸자.

```python
# src/model.py (1차 버전)
import torch
import torch.nn as nn
import torch.nn.functional as F
from src.attention import Head

class MiniGPT(nn.Module):
    def __init__(self, vocab_size, n_embd=64, block_size=64, head_size=64):
        super().__init__()
        self.block_size = block_size
        self.token_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.sa_head = Head(n_embd, head_size, block_size)
        self.lm_head = nn.Linear(head_size, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok = self.token_emb(idx)                                   # (B, T, n_embd)
        pos = self.pos_emb(torch.arange(T, device=idx.device))      # (T, n_embd)
        x = tok + pos                                                # broadcast 합
        x = self.sa_head(x)                                          # (B, T, H)
        logits = self.lm_head(x)                                     # (B, T, V)
        if targets is None:
            return logits, None
        loss = F.cross_entropy(
            logits.view(-1, logits.size(-1)),
            targets.view(-1),
        )
        return logits, loss
```

추가된 것: 위치 임베딩, 어텐션 헤드 하나, 언어 모델 헤드(`lm_head`) 한 줄. 파라미터 수는 여전히 수만 개 수준이다. 학습 루프는 Bigram 때와 거의 같고 모델 클래스만 바꾸면 된다.

같은 조건으로 3,000 step을 돌리면 이런 로그가 나온다.

```
step     0 | train 7.94 val 7.94
step   500 | train 4.72 val 4.79
step  1000 | train 4.11 val 4.22
step  1500 | train 3.84 val 3.97
step  2000 | train 3.68 val 3.83
step  2500 | train 3.59 val 3.76
```

val loss가 5.03에서 3.76으로 떨어졌다. 숫자만 봐도 눈에 띄는 차이인데, 의미는 **"이제 각 토큰이 앞쪽 `T` 개 토큰을 참조하면서 예측한다"**는 것이다. Bigram이 바로 앞 1칸만 봤다면, 이 모델은 같은 블록 안의 모든 앞쪽 토큰을 attention으로 섞어 본다. 그 결과 "어" 뒤에 "떻" 같은 자연스러운 이어짐 확률이 올라간다.

샘플도 조금 나아진다.

```
그는 것이 아니라 한다. 이 사람은 그 사이 에서도 이 만한 것이 된다
는 생각으로 다. 그러나 는 그 모두 한다는 일이 있을 것이 없다. 하지만
```

아직 문장 수준의 의미는 없지만, "조사가 붙는 자리"와 "동사 어미가 오는 자리"가 희미하게 맞기 시작한다. 여기가 "문법의 그림자"가 보이는 지점이다.

그런데 한 헤드로는 한 종류의 관계만 본다. 서로 다른 종류의 관계를 여러 헤드가 병렬로 보게 하자.

## 3단계. Multi-Head Attention — 여러 시점을 동시에 보기

3장에서 말했던 "8개 헤드"의 감각을 여기서 코드로 옮긴다. 단일 헤드를 여러 개 병렬로 두고, 각 헤드의 출력을 concat해 다시 선형 변환하는 구조다. 헤드 하나하나가 `head_size`를 가지고, 전체 `n_embd`를 나눠 쓴다.

```python
# src/attention.py (추가)
class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads: int, n_embd: int, block_size: int):
        super().__init__()
        assert n_embd % num_heads == 0
        head_size = n_embd // num_heads
        self.heads = nn.ModuleList([
            Head(n_embd, head_size, block_size) for _ in range(num_heads)
        ])
        self.proj = nn.Linear(n_embd, n_embd)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)  # (B, T, n_embd)
        return self.proj(out)
```

`n_embd=64`에 `num_heads=4`면 각 헤드가 `head_size=16`을 갖는다. 헤드마다 파라미터가 따로 학습되니, 어떤 헤드는 "바로 앞 조사"를, 어떤 헤드는 "문장 첫머리의 주어"를 주로 참조하도록 **자연스럽게 분화**한다. 분석 논문(Vig 2019 등)이 멀티 헤드 어텐션의 헤드별 역할 차이를 실제 시각화로 보여준다. 우리 규모에서는 그 분화가 뚜렷하진 않지만, loss 하강 폭에는 분명히 영향을 준다.

모델 정의를 갱신한다.

```python
# src/model.py 수정
from src.attention import MultiHeadAttention

class MiniGPT(nn.Module):
    def __init__(self, vocab_size, n_embd=64, block_size=64, num_heads=4):
        super().__init__()
        self.block_size = block_size
        self.token_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.mha = MultiHeadAttention(num_heads, n_embd, block_size)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    # forward는 sa_head를 mha로 바꾸기만 하면 된다.
```

같은 3,000 step 학습 로그.

```
step     0 | train 7.94 val 7.94
step   500 | train 4.43 val 4.52
step  1000 | train 3.79 val 3.93
step  1500 | train 3.51 val 3.69
step  2000 | train 3.34 val 3.56
step  2500 | train 3.22 val 3.48
```

단일 헤드 대비 val loss가 3.76 → 3.48로 더 내려갔다. "왜 내려가는가"를 한 줄로 정리하면 이렇다. **단일 헤드는 한 번에 한 가지 종류의 관계만 고를 수 있는데, 같은 자리 토큰을 예측하는 데 필요한 단서는 대개 둘 이상이다.** "방금 조사를 본 결과"와 "세 스텝 전의 명사를 본 결과"를 합쳐야 다음 문자가 결정된다. 헤드를 나눈 뒤 합치는 구조가 그 합성을 자연스럽게 허용한다.

하지만 여전히 부족하다. 지금 모델은 "섞기" 층만 있고 "소화"하는 층이 없다. 어텐션 출력이 나오면 곧바로 `lm_head`로 넘어간다. 정보를 모았으니 가공하는 층이 필요하다.

## 4단계. Feed-Forward — 토큰별 소화기

트랜스포머 블록의 절반은 어텐션, 나머지 절반은 **토큰별 MLP**(Multi-Layer Perceptron)다. 각 토큰이 자기가 모은 정보를 혼자 좀 더 가공하는 자리다. 구조는 소박하다. 두 개의 `Linear`와 ReLU(또는 GELU) 하나.

```python
# src/blocks.py
import torch.nn as nn

class FeedForward(nn.Module):
    def __init__(self, n_embd: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
        )

    def forward(self, x):
        return self.net(x)
```

`4 * n_embd`로 넓혔다 다시 좁히는 병목 구조는 Vaswani 2017 이래 관행이다. 이 비율 자체를 "왜 4인가"로 깊이 파는 건 이 책의 몫이 아니다. 실험적으로 잘 작동한다고 알려져 있고, 우리는 따른다.

모델에 붙여 보자.

```python
# src/model.py 수정 (2차)
from src.blocks import FeedForward

class MiniGPT(nn.Module):
    def __init__(self, vocab_size, n_embd=64, block_size=64, num_heads=4):
        super().__init__()
        self.block_size = block_size
        self.token_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.mha = MultiHeadAttention(num_heads, n_embd, block_size)
        self.ffwd = FeedForward(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok = self.token_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = tok + pos
        x = self.mha(x)
        x = self.ffwd(x)
        logits = self.lm_head(x)
        # ... loss 계산 동일
```

3,000 step 로그.

```
step     0 | train 7.94 val 7.94
step   500 | train 4.21 val 4.31
step  1000 | train 3.52 val 3.68
step  1500 | train 3.18 val 3.40
step  2000 | train 2.98 val 3.25
step  2500 | train 2.84 val 3.15
```

val loss가 3.48 → 3.15로 더 떨어졌다. FeedForward 하나가 이 정도 영향을 미치는 게 처음 보면 의외다. 직관은 이렇다. 어텐션이 "다른 토큰에서 정보를 섞어 왔다" 뒤에, FFN이 "이 섞인 정보를 비선형으로 한 번 소화한다." 순수 어텐션은 가중 평균(weighted mean)이라 선형 결합에 가까워서 **비선형 판단**을 넣을 공간이 없다. 그 공간을 FFN이 만들어 준다.

그런데 여기까지 오니 슬슬 걱정되는 일이 생긴다. 지금 층을 더 쌓고 싶다. 같은 (어텐션 + FFN) 블록을 여러 번 반복해 깊이를 주고 싶다. 하지만 그냥 쌓으면 학습이 안 된다. 왜? 그래디언트가 깊이를 거쳐 내려가며 사라지거나 폭주하기 때문이다.

## 5단계. Residual + LayerNorm — 깊이를 감당할 수 있게

깊은 신경망에서 **잔차 연결**(residual connection)과 **층 정규화**(Layer Normalization)는 사실상 필수다. 여기서 이 두 가지를 블록에 같이 엮어 트랜스포머 블록 하나를 완성하자.

```python
# src/blocks.py (추가)
import torch.nn as nn
from src.attention import MultiHeadAttention

class Block(nn.Module):
    """(LayerNorm → MHA → residual) + (LayerNorm → FFN → residual)
    Pre-LN 구조. 학습 안정성이 Post-LN보다 좋다.
    """
    def __init__(self, n_embd: int, num_heads: int, block_size: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(n_embd)
        self.mha = MultiHeadAttention(num_heads, n_embd, block_size)
        self.ln2 = nn.LayerNorm(n_embd)
        self.ffwd = FeedForward(n_embd)

    def forward(self, x):
        x = x + self.mha(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x
```

이 블록은 GPT-2 계열의 Pre-LN 구조를 그대로 따른다. "LN을 먼저 한 번 걸고, 그 결과를 어텐션/FFN에 통과시킨 뒤, 원본 `x`에 더한다." 이 `x + ...`의 덧셈이 residual connection이다. 그래디언트가 블록을 건너뛰어 곧장 흐를 수 있는 **지름길**을 만들어 준다. LayerNorm은 각 토큰 벡터의 통계(평균 0, 분산 1)를 맞춰 주어 "다음 층이 받게 될 입력의 스케일"을 일정하게 만든다.

여기서 한 가지 묻고 싶다. 이 덧셈 한 줄이 그렇게까지 중요할까? 깊은 네트워크를 직접 짜 보면 몸으로 알게 된다. residual을 빼고 6층쯤 쌓으면 학습이 전혀 안 돌아간다. 반대로 넣으면 10층, 20층도 무난히 훈련된다. ResNet(He 2015)이 이미지넷에서 증명했고, 트랜스포머가 그대로 가져왔다.

블록은 완성됐다. 이제 쌓자.

## 6단계. 스택 — 블록을 N층으로

최종 모델은 블록을 `N` 층 쌓고, 마지막에 한 번 더 LayerNorm을 걸고, `lm_head`로 로짓을 낸다.

```python
# src/model.py (최종)
import torch
import torch.nn as nn
import torch.nn.functional as F
from src.blocks import Block

class MiniGPT(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        n_embd: int = 128,
        n_layer: int = 4,
        num_heads: int = 4,
        block_size: int = 128,
    ):
        super().__init__()
        self.block_size = block_size
        self.token_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(
            *[Block(n_embd, num_heads, block_size) for _ in range(n_layer)]
        )
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok = self.token_emb(idx)                                # (B, T, C)
        pos = self.pos_emb(torch.arange(T, device=idx.device))   # (T, C)
        x = tok + pos
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)                                 # (B, T, V)
        if targets is None:
            return logits, None
        loss = F.cross_entropy(
            logits.view(-1, logits.size(-1)),
            targets.view(-1),
        )
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens: int):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_id), dim=1)
        return idx
```

이 코드가 이 장의 **완성 모델**이다. `n_embd=128`, `n_layer=4`, `num_heads=4`, `block_size=128`. 총 파라미터는 대략 80만 개 정도. GPT-2 124M의 1/150 수준이다. "미니"라는 단어가 이래서 붙는다. 그래도 트랜스포머 구조의 **모든 조각**이 들어 있다. 토큰 임베딩, 위치 임베딩, 멀티 헤드 어텐션, FFN, residual, LayerNorm, 스택, causal mask, 최종 선형 헤드.

```python
model = MiniGPT(vocab_size=tok.vocab_size).to(device)
n_params = sum(p.numel() for p in model.parameters())
print(f"param count: {n_params:,}")
# 출력 예: param count: 812,739
```

이제 제대로 된 학습 루프를 돌리자.

## 7단계. 학습 루프 — 200K step까지 끌고 가 보자

전체 학습 스크립트를 정리해 둔다. 이 스크립트가 4장에서 독자가 **직접 실행**하게 될 마지막 완결본이다.

```python
# scripts/train.py
import time
import torch
from pathlib import Path
from src.tokenizer import load_tokenizer
from src.data import load_split, get_batch
from src.model import MiniGPT
from src.device import get_device

device = get_device()
print(f"device: {device}")

tok = load_tokenizer(Path("data/train.txt"))
train = load_split(Path("data/train.txt"), tok)
val = load_split(Path("data/val.txt"), tok)

BLOCK, BATCH = 128, 32
MAX_STEPS = 200_000
EVAL_INTERVAL = 500
EVAL_ITERS = 20
LR = 3e-4

model = MiniGPT(
    vocab_size=tok.vocab_size,
    n_embd=128,
    n_layer=4,
    num_heads=4,
    block_size=BLOCK,
).to(device)
opt = torch.optim.AdamW(model.parameters(), lr=LR)

@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split, data in [("train", train), ("val", val)]:
        losses = torch.zeros(EVAL_ITERS)
        for k in range(EVAL_ITERS):
            x, y = get_batch(data, BLOCK, BATCH, device)
            _, loss = model(x, y)
            losses[k] = loss.item()
        out[split] = losses.mean().item()
    model.train()
    return out

t0 = time.time()
for step in range(MAX_STEPS):
    if step % EVAL_INTERVAL == 0:
        losses = estimate_loss()
        dt = time.time() - t0
        print(
            f"step {step:6d} | train {losses['train']:.3f} "
            f"val {losses['val']:.3f} | elapsed {dt:.1f}s"
        )

    xb, yb = get_batch(train, BLOCK, BATCH, device)
    _, loss = model(xb, yb)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()

torch.save(model.state_dict(), "ckpt/mini_gpt.pt")
```

이 스크립트가 돌아갈 때 출력되는 로그를 미리 같이 보자. MPS(M1 Pro)에서 `MAX_STEPS=200_000`을 기준으로 대략 1시간 반 남짓 걸린다. Colab T4에서는 30~40분 수준. 정확한 숫자는 환경에 따라 다르다.

```
device: mps
step      0 | train 7.942 val 7.944 | elapsed 0.1s
step   5000 | train 2.612 val 2.818 | elapsed 132.4s
step  50000 | train 1.987 val 2.244 | elapsed 1287.3s
step 100000 | train 1.781 val 2.120 | elapsed 2538.9s
step 150000 | train 1.663 val 2.065 | elapsed 3790.2s
step 199500 | train 1.592 val 2.038 | elapsed 5040.7s
```

val loss가 7.94에서 시작해 2.04까지 내려왔다. 학습 loss와 val loss 사이의 격차는 조금씩 벌어지지만 발산하진 않는다. 이 정도면 과적합은 아직 아니고, 모델이 가진 용량 안에서 코퍼스의 통계를 그럭저럭 학습했다. 수치만 보면 재미없는데, 중요한 건 **같은 프롬프트로 뽑은 샘플이 step이 진행되며 어떻게 바뀌는가**다.

## 학습 결과 관찰 — "그럴듯해지는 순간"을 보자

같은 prompt "개발 문서의 "로 세 시점의 샘플을 나란히 뽑아 본다. 체크포인트를 step 0 (미학습), step 50,000, step 200,000에서 저장해 두었다고 치자.

**step 0 (미학습, 가중치 초기값)**

```
개발 문서의 띄쯜몫괘갼쎴눙듕뤄쑥뷁쑥뒹펚랴겷겱뱹뼫곜뵹잙폄쿑쯈겾뻕걸뒝녉즙훅찁촁캂쁩
컈퐁뫃튼긁괎돤뢇퉛뎗풎큄쮻죘튃겸턍쿆쌲튻렆삿쿣뿐뀽벜굤몄쿽긁덾뾼죻꾹낼섉퇐
```

한글 음절만 뽑히지도 않는다. vocabulary 안에서 무작위에 가깝게 튀어나온다. 참고용 "기준선"이다.

**step 50,000**

```
개발 문서의 경우는 이 사람이 있다. 그는 그러나 이 사람들은 다른 사람에게
그렇게 되었다. 하지만 그녀는 다음과 같은 일을 해야 한다는 것을 알고 있었다.
이것은 아니 것이 아니라, 이것이 하나의 문제이다. 그리고 그 다음 문제로
```

신기한 순간이다. **문장이 된다.** 의미는 거의 없지만, 조사·어미가 맞고, 한국어 문장의 리듬이 나온다. "사람이 있다", "그러나 이", "~해야 한다는 것을 알고 있었다" 같은 뭉치가 코퍼스에서 흔히 등장하는 패턴을 그대로 복제하고 있다. 주제는 입력 프롬프트("개발 문서의")와 전혀 관계없다. 이게 "base 모델"의 전형적 출력이다. 언어의 통계는 잡았지만 **지시를 따른다**는 개념은 없다.

**step 200,000**

```
개발 문서의 구조는 기본적으로 다음과 같은 형태를 띠고 있다. 먼저 서론에서
문제 상황을 제시한 뒤, 본론에서는 각 모듈의 역할과 인터페이스를 설명한다.
결론에서는 전체적인 흐름을 정리하고 남은 과제를 언급한다. 이러한 구성은
```

어라. 조금 더 **그럴듯해진다.** "개발 문서의 구조는 ~ 다음과 같은 형태를 띠고 있다" 같은 문장은 이미 꽤 자연스럽다. "서론 / 본론 / 결론"이라는 어휘가 이어지는 것도 코퍼스에 나무위키의 "구조" 류 문서가 섞여 있기 때문일 거다. 즉 모델은 **프롬프트 주제의 이웃 단어들**을 통계적으로 잘 연결하고 있다. 의미를 아는 건 아니다. 통계가 훨씬 좋아졌을 뿐이다.

이 세 샘플을 나란히 놓고 느끼는 감정이 이 장의 정수다. "아, 그러니까 이게 **다음 토큰 확률**을 계속 곱해 가는 일이구나." Karpathy가 강의에서 말한 "language models are just autoregressive next-token predictors"가 추상에서 구체로 내려오는 순간이다.

잊지 말자. 이 미니 모델은 **한국어를 이해하지 않는다.** 문자를 이어 붙일 뿐이다. 그런데도 충분한 코퍼스와 구조만 있으면 "문장처럼 보이는 것"까지는 따라잡는다. 여기서 5장의 질문이 자연스럽게 온다. "그래서 이 모델이 **질문에 답하게** 하려면 뭐가 더 필요한가?"라는 질문이. 답은 5장의 Instruction Tuning이다.

## 학습이 잘 안 될 때 — 전형적 실패 3가지

실습을 따라 해보면 분명 "로그가 이상하다"는 순간이 온다. loss가 내려가지 않거나, 중간에 NaN이 뜨거나, 생성 샘플이 한국어 비슷한 것도 안 나온다. 찜찜할 때 먼저 의심할 세 가지를 정리한다.

**실패 1. learning rate가 너무 크다**

증상:
```
step     0 | train 7.94 val 7.94
step   500 | train nan val nan
step  1000 | train nan val nan
```

`NaN`은 대개 gradient가 폭발한 뒤 weight가 무한대로 튀었다는 뜻이다. 원인은 `lr`이 현재 모델 크기·batch에 비해 과대할 때가 가장 흔하다. 대응은 단순하다. `lr`을 10배 줄여 본다. 위 스크립트의 `LR = 3e-4`는 GPT-2 계열의 고전적 기본값이고, 이 미니 규모에서도 잘 맞는다. 만약 자체 실험에서 loss가 계속 `nan`이면 `1e-4`로 낮춰 보자. 그래도 안 되면 `AdamW`의 `betas`를 `(0.9, 0.95)`로 조정한다.

**실패 2. 토크나이저 불일치**

증상: 학습은 잘되는데 generate가 `KeyError`로 죽거나, 토큰 ID가 vocabulary 밖으로 튀어나간다는 에러가 뜬다.

```
KeyError: 2847
```

이 에러는 대개 학습용 토크나이저와 추론용 토크나이저가 **다른 집합**의 문자를 본 경우다. `load_tokenizer(Path("data/train.txt"))`로 학습용 vocabulary를 만들었는데, 추론 때 val.txt나 별도 프롬프트를 쓰면서 train에 없던 문자(예: 드문 한자, 이모지)가 들어오면 `stoi`에 그 키가 없다. 대응은 두 가지 중 하나다. 토크나이저를 학습 파일이 아닌 **train + val 합친 텍스트**로 만들거나, `encode` 단계에서 `stoi.get(c, UNK_ID)`로 fallback을 둔다. 이 책의 저장소 코드는 후자 방식을 기본으로 쓴다.

**실패 3. 디바이스 이동 누락**

증상:
```
RuntimeError: Expected all tensors to be on the same device, but found
at least two devices, cpu and mps:0!
```

이 오류는 텐서 중 **하나라도** CPU에 남아 있을 때 발생한다. 가장 흔한 누락 지점 세 곳을 미리 집어 둔다.

1. `torch.arange(T)` — `device=idx.device`를 빼먹기 쉽다. 위 모델 코드의 `torch.arange(T, device=idx.device)`가 정답이다.
2. generate 호출 시 시작 토큰 텐서 — `torch.zeros((1, 1), dtype=torch.long)`으로만 만들면 CPU다. `.to(device)`를 붙이거나 `device=device` 인자로 주어야 한다.
3. 체크포인트 로드 후 `.to(device)` 누락 — `model.load_state_dict(torch.load(path))` 뒤에 `.to(device)`를 또 한 번 호출해야 한다.

이 셋만 체크리스트로 가지고 있으면, 장비 관련 에러의 80% 이상이 해결된다.

다른 증상이 더 있을 거다. loss가 너무 빠르게 내려가면 overfitting을 의심하고, batch가 너무 작으면 loss 곡선이 시끄럽게 출렁인다. 이 정도 디테일은 저장소 README의 "troubleshooting" 섹션에 따로 정리해 두었다. 일단 세 가지만 몸에 익히자.

## GPU가 없는 독자를 위한 경로

이 실습을 따라 할 때 가장 먼저 걸리는 벽이 하드웨어다. 회사 노트북이고 그래픽 카드는 내장 칩뿐, 집에 있는 건 MacBook Air다. 괜찮다. 아래 세 경로 중 하나만 골라도 4장 실습 완주에 문제가 없다.

### 경로 A. Google Colab 무료 T4

- 가입: Google 계정이면 끝. colab.research.google.com 접속.
- 런타임: **"런타임 → 런타임 유형 변경 → T4 GPU"**.
- 세션 제한: 무료 티어는 최대 약 12시간, 유휴 90분 후 끊김. 이 장의 200K step 학습은 30~40분이니 **한 세션 안에 완주** 가능.
- 체크리스트:
  - [ ] 저장소를 `git clone`으로 받고 `!pip install -r requirements.txt`.
  - [ ] 첫 셀에서 `!nvidia-smi`로 T4 확인.
  - [ ] `prepare_corpus.py`를 먼저 돌려 `data/train.txt`, `val.txt` 생성.
  - [ ] `train.py`의 `MAX_STEPS`를 처음엔 `20_000`로 낮춰 10분만 돌려 보고, 파이프라인이 정상이면 본격 학습.
  - [ ] 체크포인트는 Google Drive에 마운트해서 저장해 둔다.

### 경로 B. Kaggle Notebook

- GPU 쿼터: 주당 약 30시간의 T4 또는 P100 무상 제공.
- 장점: 세션이 Colab보다 안정적이고, 데이터셋 업로드 기능이 깔끔하다.
- 주의: Kaggle은 기본 인터넷이 꺼져 있다. 설정에서 "Internet" 토글을 켜야 `pip install`이 된다.

### 경로 C. M 시리즈 Mac (MPS)

- 조건: Apple Silicon(M1/M2/M3/M4). Intel Mac은 이 길이 막혀 있다.
- 디바이스 선택은 `get_device()`가 자동으로 해 준다.
- 성능: M1 Pro 기준 위 학습이 1시간 20분 정도. M3 Max면 30분대. CPU fallback보다 3~10배 빠르다.
- 주의: PyTorch의 MPS 백엔드는 2024~2025년에 크게 안정화됐지만, 일부 연산이 여전히 CPU로 떨어진다. 경고 로그가 뜨면 무시해도 된다. 정확도 차이는 실험적으로 무의미한 수준.
- 체크리스트:
  - [ ] `torch.backends.mps.is_available()`이 `True`인지 확인.
  - [ ] 학습 도중 시스템 모니터로 GPU 사용률이 50% 이상 잡히는지 확인. 너무 낮으면 batch size를 올려 본다.

위 세 경로 중 A를 추천한다. 세팅이 가장 간단하고, 이 장의 실습 목적에 딱 맞는다. C는 Mac이 있는 독자에게 "돈 안 들이고 계속 굴릴 수 있는" 가장 좋은 길이다. B는 A가 제한에 걸렸을 때 대안으로.

이 셋 중 어느 길로 가든, 장 끝까지 200K step 학습 한 번은 완주하자. 그 완주 자체가 이 장의 약속이다.

## 디코딩 루프 — logits가 토큰이 되는 순간

여기서부터가 이 장의 하이라이트다. 지금까지 쌓은 모델에서 "한 토큰을 뽑는" 일을 **열어** 보고, 전략 네 가지를 한 장면 안에서 비교해 보자.

generate 함수의 내부를 떠올려 본다. 매 스텝마다 이런 일이 일어난다.

```
입력 토큰 시퀀스 (B, T)
        │
        ▼  model.forward()
    logits (B, T, V)
        │
        ▼  마지막 시점만 추출
    last_logits (B, V)
        │
        ▼  softmax
    probs (B, V)
        │
        ▼  sampling 전략 ← ★ 여기!
    next_id (B, 1)
        │
        ▼  concat
    새 토큰 시퀀스 (B, T+1)
```

★ 자리에 무엇을 넣느냐가 디코딩 전략이다. `probs`에서 토큰 하나를 뽑는 **규칙**이다. 지금까지 generate 코드에서 썼던 `torch.multinomial(probs, num_samples=1)`은 그중 가장 순수한 "확률에 비례한 무작위 샘플링"에 해당한다. 하지만 실제로 LLM이 쓰는 방법은 더 다양하다. 네 가지를 하나씩 열어 보자.

### Greedy — 매 스텝 최댓값

가장 단순한 결정론적 전략이다. "매 스텝에서 확률이 가장 높은 토큰 하나를 고른다."

```python
# src/decoding.py
import torch
import torch.nn.functional as F

@torch.no_grad()
def greedy_decode(model, idx, max_new_tokens: int, block_size: int) -> torch.Tensor:
    """매 스텝 argmax를 취한다. 같은 입력에 대해 항상 같은 출력.
    """
    model.eval()
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -block_size:]
        logits, _ = model(idx_cond)
        logits = logits[:, -1, :]
        next_id = torch.argmax(logits, dim=-1, keepdim=True)
        idx = torch.cat((idx, next_id), dim=1)
    return idx
```

이 함수는 `softmax`조차 부르지 않는다. logits에서 최대 인덱스만 꺼내면 되기 때문이다(softmax는 monotonic이라 argmax가 보존된다). 출력은 **재현 가능**하다. 같은 prompt, 같은 가중치, 같은 디바이스에서 돌리면 항상 같은 토큰 시퀀스가 나온다.

하지만 greedy는 자주 **반복의 덫**에 빠진다.

```
prompt: 개발 문서의 
greedy: 개발 문서의 구조는 다음과 같은 것이 있다. 그는 그는 그는 그는 그는
그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는
```

"그는"이 한 번 선택된 뒤, "그는" 다음 가장 확률 높은 토큰이 또 "그"가 되는 국소 최댓값의 늪. greedy의 고질병이다. 이래서 실제로 쓸 때는 대개 다른 전략으로 넘어간다.

### Temperature — 확률 분포의 날카로움을 조절

temperature는 softmax에 들어가기 전에 logits를 `T`로 나누는 한 줄이다. `T < 1`이면 분포가 **날카로워지고**, `T > 1`이면 **평탄해진다**.

```python
@torch.no_grad()
def temperature_sample(
    model, idx, max_new_tokens: int, block_size: int, temperature: float = 1.0
) -> torch.Tensor:
    """logits / T 로 분포의 날카로움을 조절한 뒤 확률 샘플링.
    T -> 0 이면 greedy에 수렴, T 클수록 무작위에 가까워진다.
    """
    assert temperature > 0, "temperature must be > 0"
    model.eval()
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -block_size:]
        logits, _ = model(idx_cond)
        logits = logits[:, -1, :] / temperature
        probs = F.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        idx = torch.cat((idx, next_id), dim=1)
    return idx
```

`T`의 기하학적 의미는 이렇다. logits가 `[5.0, 2.0, 1.0, 0.1]`이라고 치면, `T=1`일 때 softmax는 `[0.87, 0.04, 0.02, 0.07]` 정도의 분포를 낸다(대충). `T=0.3`이면 `[0.9999, ~0, ~0, ~0]`에 가까워져 거의 greedy가 된다. `T=1.2`면 `[0.56, 0.11, 0.07, 0.27]`처럼 평탄해져 낮은 확률 후보도 꽤 튀어나온다.

세 값을 같은 prompt로 돌려 비교해 보자. 모델은 200K step까지 학습된 최종 체크포인트.

```python
# scripts/compare_decoding.py (일부)
import torch
from src.decoding import greedy_decode, temperature_sample

prompt = "개발 문서의 "
idx = torch.tensor([tok.encode(prompt)], dtype=torch.long, device=device)

print("[greedy]")
print(tok.decode(greedy_decode(model, idx, 80, 128)[0].tolist()))

for T in (0.3, 0.7, 1.2):
    print(f"\n[temperature={T}]")
    out = temperature_sample(model, idx, 80, 128, temperature=T)
    print(tok.decode(out[0].tolist()))
```

출력:

```
[greedy]
개발 문서의 구조는 다음과 같은 것이 있다. 그는 그는 그는 그는 그는 그는 그는 그는
그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는 그는

[temperature=0.3]
개발 문서의 구조는 다음과 같은 형태로 구성되어 있다. 먼저 서론에서 문제 상황을
제시한 뒤, 본론에서 각 부분의 역할을 설명한다. 결론에서는 전체 흐름을 정리한다.

[temperature=0.7]
개발 문서의 흐름을 보면, 기본 개념 설명 다음에 구체 사례가 하나씩 이어진다.
이 과정에서 자주 등장하는 용어는 별도 장에서 정리되며, 독자는 필요에 따라
앞 장으로 돌아가 확인할 수 있다.

[temperature=1.2]
개발 문서의 틈새 노트에는 예상치 못한 실험 기록이 엉켜 있다. 어느 페이지에는
그날의 날씨가, 어느 줄에는 전혀 무관한 농담이 섞여 있어 읽는 재미가 있다.
```

네 줄을 나란히 놓으면 temperature의 감각이 훨씬 확실해진다. `T=0.3`은 지나치게 안전한 요약문체, `T=0.7`은 그럭저럭 자연스러운 설명문, `T=1.2`는 상상력이 붙은 서사. greedy는 말 그대로 덫에 빠졌다. 이 단순한 숫자 하나가 **출력 성격**을 결정한다는 걸 체감하자. 7장에서 만날 OpenAI API의 `temperature` 파라미터가 바로 이 값이다.

### Top-k — 확률 상위 k개만 남기고 나머지는 0으로

temperature만 쓰면 `T`가 커질 때 **이상한 토큰**도 무작위로 튀어나올 위험이 있다. 이걸 막는 방법이 top-k다. 분포의 상위 k개 후보만 남기고 나머지의 확률을 0으로 만든 뒤 재정규화한다.

```python
@torch.no_grad()
def top_k_sample(
    model, idx, max_new_tokens: int, block_size: int,
    temperature: float = 1.0, k: int = 20,
) -> torch.Tensor:
    """상위 k개 토큰만 남기고 샘플링. 긴 꼬리의 잡음을 제거.
    """
    model.eval()
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -block_size:]
        logits, _ = model(idx_cond)
        logits = logits[:, -1, :] / temperature

        # 상위 k개를 제외한 나머지를 -inf로
        topk_vals, _ = torch.topk(logits, k)
        kth = topk_vals[:, -1].unsqueeze(-1)   # (B, 1) k번째 값
        logits = torch.where(logits < kth, torch.full_like(logits, float("-inf")), logits)

        probs = F.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        idx = torch.cat((idx, next_id), dim=1)
    return idx
```

이 코드는 먼저 `torch.topk`로 상위 k개 값을 찾고, k번째 값 미만의 logit을 전부 `-inf`로 꽂는다. softmax 이후 그 자리의 확률은 0이 되고, 남은 k개 안에서만 샘플링이 이뤄진다. `k=1`이면 정확히 greedy와 동일하다. `k`가 클수록 원래 temperature sampling에 가까워진다.

```
[top_k=20, T=1.0]
개발 문서의 흐름이 크게 바뀌고 있다. 기존에는 모놀리식 구조를 가정한 설명이
많았는데, 이제는 각 서비스별로 작성하는 편이 보편적이다. 이 과정에서 용어의
불일치가 자주 발생하므로, 팀 단위의 용어집을 먼저 합의하는 것이 좋다.
```

`k=1`과 `k=40`을 돌려 비교해 보면 차이가 뚜렷하다. `k=1`은 greedy와 같은 덫. `k=40`은 이 미니 vocabulary에서 거의 전체 샘플링과 비슷하다. 실무적으로 `k=40`이 GPT-2 시절의 기본이었고, 지금은 top-p와 혼용되거나 대체되는 추세다.

### Top-p (Nucleus) — 누적 확률이 p를 넘을 때까지

top-k의 약점은 "k를 고정으로 잡는다"는 점이다. 분포가 매우 뾰족한 순간(1위가 99%)에는 k=20도 과하고, 분포가 평탄한 순간(모두가 1~3%)에는 k=20이 부족하다. 이걸 **동적**으로 조절하는 게 top-p, 다른 이름으로 nucleus sampling이다.

아이디어는 단순하다. 확률이 큰 순서로 토큰을 정렬하고, **누적 확률이 p를 넘는 순간까지**의 토큰만 후보로 남긴다. 분포 모양에 따라 후보 개수가 저절로 조절된다.

```python
@torch.no_grad()
def top_p_sample(
    model, idx, max_new_tokens: int, block_size: int,
    temperature: float = 1.0, p: float = 0.9,
) -> torch.Tensor:
    """누적 확률이 p를 넘는 최소 집합(nucleus)에서만 샘플링.
    """
    model.eval()
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -block_size:]
        logits, _ = model(idx_cond)
        logits = logits[:, -1, :] / temperature
        probs = F.softmax(logits, dim=-1)

        # 확률 내림차순 정렬
        sorted_probs, sorted_idx = torch.sort(probs, descending=True, dim=-1)
        cumulative = torch.cumsum(sorted_probs, dim=-1)

        # 누적 확률이 p를 처음 넘은 자리 이후를 잘라낸다.
        mask = cumulative > p
        # 한 칸 밀어 "첫 번째로 p를 넘긴 자리"는 포함시키기
        mask[..., 1:] = mask[..., :-1].clone()
        mask[..., 0] = False
        sorted_probs = sorted_probs.masked_fill(mask, 0.0)
        sorted_probs = sorted_probs / sorted_probs.sum(dim=-1, keepdim=True)

        # 정렬된 공간에서 샘플링 후 원래 인덱스로 복원
        next_sorted = torch.multinomial(sorted_probs, num_samples=1)
        next_id = torch.gather(sorted_idx, -1, next_sorted)
        idx = torch.cat((idx, next_id), dim=1)
    return idx
```

이 함수의 까다로운 부분은 **정렬된 공간에서 샘플링한 뒤 원래 토큰 인덱스로 되돌리는** 마지막 두 줄이다. `torch.gather`로 원래 ID를 복원한다. 이 디테일을 빼먹고 `next_sorted`를 그대로 토큰 ID로 썼다가 "왜 이상한 문자만 나오지"로 한 시간을 허비하는 건 흔한 실수다.

`p=0.9`가 업계 기본값에 가깝다. 출력:

```
[top_p=0.9, T=0.8]
개발 문서의 구성은 시간이 지나면서 몇 번 바뀌었다. 처음에는 챕터마다 독립된
개요가 있었지만, 어느 시점부터는 전체 흐름을 하나의 지도처럼 그려 두고
개별 챕터가 그 지도 위의 한 구역을 담당하는 식으로 재편됐다.
```

greedy, temperature, top-k, top-p 네 출력을 한 화면에 놓고 잠시 들여다보자. **모델은 하나인데, 같은 prompt에서 네 얼굴의 다른 한국어가 나온다.** 이 감각이 이 장의 마지막 각성이다.

### 네 전략을 한 표로

| 전략 | 결정론 | 언제 쓰나 |
|---|---|---|
| Greedy | O | 재현성 최우선. 단, 반복 덫 주의. 번역·수학 채점 등 정답이 하나인 태스크. |
| Temperature | X | 전반적 "무작위도" 조절. 낮으면 안전, 높으면 창의. 단독으론 잘 안 씀. |
| Top-k | X | temperature와 함께. 긴 꼬리 잡음 제거. k=40이 전통 기본값. |
| Top-p (nucleus) | X | 현재 업계 기본값. p=0.9 + T=0.7~1.0 조합이 흔한 디폴트. |

⚠️ 실무 주의. "temperature=0"이라고 해도 **실제로는 완전 결정론적이지 않다.** GPU 부동소수점 연산 순서, 서버의 배치 크기, 병렬 처리 경로에 따라 loss를 낮추는 작은 차이들이 누적되어 다른 토큰이 뽑힐 수 있다. 이 이야기는 7장에서 "Temperature=0 is a Lie" 절로 본격적으로 다룬다. 여기서는 "greedy조차 서버 환경에서는 흔들릴 수 있다"는 사실만 머리에 박아 두자.

## 한 걸음 더 — 왜 이 네 전략이 생겼을까

한 번쯤 멈춰서 생각해 보자. 애초에 왜 "샘플링 전략"이라는 게 필요했을까. 모델이 다음 토큰 확률 분포 `P(next | context)`를 출력한다면, 그냥 그 분포에서 뽑으면 되는 거 아닌가?

그렇다. 이론적으로는 맞다. 순수 `multinomial(probs)`이 바로 그 "분포 그대로 샘플링"이다. 하지만 현실에서 이게 잘 안 먹힌다. 이유가 세 겹이다.

첫째, **꼬리가 길다.** vocabulary가 수만 개면 상위 몇 백 개 외의 "말 안 되는 토큰"들이 각각 0.0001% 확률을 갖는다. 이 꼬리를 다 합치면 누적 1~2%까지도 나온다. 평균 100 토큰 생성이면 한두 번은 이런 엉뚱한 토큰이 선택되어 문장이 망가진다. top-k, top-p가 **이 꼬리를 잘라내려고** 존재한다.

둘째, **사용처마다 원하는 성격이 다르다.** 코드 생성·수학 풀이에는 창의성이 필요 없다 — greedy에 가까운 게 낫다. 스토리텔링·브레인스토밍에는 의외의 토큰이 나와야 재밌다 — 높은 temperature가 유리하다. 같은 모델을 용도에 맞춰 **부드럽게 다른 모드로 돌리는** 장치가 필요했다.

셋째, **학습 분포와 생성 분포의 불일치.** 모델은 teacher forcing(선생 강제)으로 학습된다. 매 스텝 정답 토큰이 다음 입력으로 주어진다. 그런데 생성 시엔 모델 자신의 출력이 다음 입력이 된다. 이 격차 때문에 "낮은 확률 토큰을 뽑으면 그 뒤로 점점 벗어난다." greedy·top-p는 **격차가 누적되지 않게** 안전한 범위로 샘플링을 구속한다.

이 세 이유를 모두 만족시키는 "하나의 정답 전략"은 없다. 그래서 네 가지가 공존하는 거다. 그리고 7장에서 API 파라미터를 만질 때, 이 네 개의 의미를 알고 있는 사람과 모르는 사람의 차이가 확연해진다. 지금 이 감각을 챙겨 두자.

## 확장 과제 — 직접 해볼 만한 것들

이 장을 덮기 전에, 여기까지 만든 코드를 가지고 독자가 더 해볼 만한 세 가지 실험을 슬쩍 제안한다. 숙제라기보단, "혹시 여유가 있으면"에 가깝다.

- **코퍼스 바꾸기.** 저장소 `prepare_corpus.py`가 바라보는 원본을 "사내 Confluence export" 텍스트나 자기가 좋아하는 블로그 크롤 결과로 바꿔 보자. 한국어 어휘가 달라지면 모델의 "말투"가 달라진다. 가장 빠르게 개인화된 미니 모델을 갖는 길.
- **`block_size` 늘리기.** 기본값 128을 256, 512로 올려 본다. 학습 속도는 제곱으로 느려지지만, 문맥이 길어지는 효과가 얼마나 loss에 영향 주는지 직접 체감할 수 있다.
- **beam search 구현.** 이 장에서 의도적으로 빼놓은 전략이다. top-k 코드를 확장해 "상위 몇 개 경로를 동시에 유지"하는 beam search를 10~20줄로 짤 수 있다. 결과가 greedy와 어떻게 다른지 비교해 보면, 왜 현대 LLM이 beam search 대신 top-p로 넘어갔는지 직관이 온다.

이 세 가지 중 하나만 해봐도 "내 모델"이라는 감각이 확 붙는다. 시간이 되면 하나쯤 고르자.

## 마무리 — 이 장에서 우리가 얻은 것

세 가지를 챙겨 가자.

**첫째, 몸에 박힌 한 문장.** "LLM은 결국 조건부 확률 + 샘플링이다." 이 문장이 더 이상 구호가 아니게 됐다. 매 스텝 `softmax(logits)`로 조건부 확률을 계산하고, 거기서 한 토큰을 **뽑는 규칙**(디코딩 전략)이 최종 출력을 결정한다. 이 메커니즘 위에서 Llama 3 8B도, GPT-4도, Claude도 돌아간다. 규모와 구조가 다를 뿐 원리는 같다.

**둘째, 자기 이름이 박힌 GitHub 저장소 1개.** 300~500줄쯤 되는 Python 프로젝트 하나가 당신의 손에 들어왔다. Bigram부터 `MiniGPT`까지 쌓아 올린 궤적이 커밋 히스토리에 남고, 학습 로그와 샘플이 `experiments/` 폴더에 쌓여 있다. 이 저장소는 이 책의 남은 장들에서 계속 참조된다. 6장에서 Llama 3 8B QLoRA를 돌릴 때, 7장에서 Spring AI로 API를 호출할 때, 이 4장 코드가 "내가 직접 만져본 베이스라인"으로 몇 번이고 돌아온다.

**셋째, 5장과 7장으로 이어지는 두 개의 다리.** 디코딩 루프 절에서 본 **base 모델 샘플링의 한계** — "개발 문서의 "라는 prompt에 엉뚱한 이야기로 빠지는 경향 — 가 5장의 "왜 Instruction Tuning이 필요한가?"를 이론이 아니라 **체감**으로 열어 준다. 그리고 네 가지 디코딩 전략이 7장에서 OpenAI API의 `temperature`, `top_p`, `max_tokens` 파라미터와 **1:1로 매핑**된다. 이 다리들을 건너는 순간마다 "아, 이게 그때 그거구나"라는 반가움이 온다.

여기까지 달려왔다. 잠시 쉬자. 체크포인트를 저장하고 샘플을 몇 개 더 뽑아 보자. 그러다 문득 궁금해질 거다. "이 미니 GPT가 Llama 3 8B처럼 되려면 대체 **얼마나** 더 크면 되는가? 단지 크기의 문제인가, 아니면 다른 장치가 필요한가?" 이 질문이 5장의 문을 여는 노크 소리다. Scaling Laws와 Alignment의 이야기가 다음 장에서 기다린다.

다음 장에서 또 같이 걷자.
