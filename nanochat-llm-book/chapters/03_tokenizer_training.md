# 3장. 토크나이저를 학습시키고 평가하기

2장에서 우리는 토크나이저가 모델의 *시각*이라는 걸 봤다. `"strawberry"`라는 한 단어가 어떤 토크나이저에서는 `["straw", "berry"]` 두 조각으로, 어떤 토크나이저에서는 `["s", "tr", "aw", "ber", "ry"]` 다섯 조각으로 쪼개진다는 사실. GPT-4 토크나이저로 우리말 한 문장을 잘라보면 같은 문장이 영어보다 두세 배 많은 토큰으로 부풀어 오른다는 사실. 그래서 "이런 식이면 한국어가 비싸지는구나"라는 작은 깨달음 — 우리가 *aha*라고 불렀던 그 순간.

그런데 거기까지는 *남이 학습시킨* 토크나이저를 들여다본 것뿐이다. GPT-2도 OpenAI가 만들었고, GPT-4의 `cl100k_base`도 OpenAI가 만들었다. 우리는 그것들을 *읽기만* 했다.

이번 장에서는 *우리가 직접 학습시킨다*. 카르파시가 `scripts/tok_train.py`에 박아둔 한 줄짜리 명령으로 2B(20억) characters의 FineWeb 영문 텍스트를 흘려보내, 32,768개의 토큰을 가진 우리만의 BPE 토크나이저를 만든다. 그리고 `scripts/tok_eval.py`로 그게 GPT-2(5만 어휘)·GPT-4(10만 어휘)와 비교해 *얼마나* 효율적인지를 영문 뉴스·한국어·코드·LaTeX 수식·과학 텍스트로 측정한다.

이 장의 정서는 *손에 잡히는 결과의 만족*이다. CPU 한 시간이면 우리 노트북에서도 끝난다. 끝나고 나면 `~/.cache/nanochat/tokenizer/tokenizer.pkl`이라는 약 1MB짜리 파일이 우리 디스크에 떨어진다. 그게 *내가 만든 첫 작품*이다. ChatGPT를 만든다는 거창한 약속에서 우리가 처음으로 *손에 쥐는* 결과물.

그럼 가보자.

---

## tok_train.py — 100줄짜리 작품의 전체 골격

`scripts/tok_train.py`는 통째로 106줄짜리 파일이다. 카르파시는 거대한 학습 파이프라인을 짧은 스크립트 하나에 욱여넣는 습관이 있는데, 이 파일이 그 좋은 예다. 펴서 한 번 통째로 훑어보자.

```python
# scripts/tok_train.py:1-23
"""
Train a tokenizer using our own BPE Tokenizer library.
In the style of GPT-4 tokenizer.
"""
import os
import time
import argparse
import torch
from nanochat.tokenizer import RustBPETokenizer
from nanochat.common import get_base_dir
from nanochat.dataset import parquets_iter_batched

parser = argparse.ArgumentParser(description='Train a BPE tokenizer')
parser.add_argument('--max-chars', type=int, default=2_000_000_000,
                    help='Maximum characters to train on (default: 2B)')
parser.add_argument('--doc-cap', type=int, default=10_000,
                    help='Maximum characters per document (default: 10,000)')
parser.add_argument('--vocab-size', type=int, default=32768,
                    help='Vocabulary size (default: 32768 = 2^15)')
args = parser.parse_args()
```

세 줄짜리 docstring과 import, 그리고 argparse 세 개. 우리가 만질 다이얼이 *딱 세 개*라는 뜻이다.

- `--max-chars=2_000_000_000` — 학습에 흘려보낼 텍스트 총량. 2B characters, 영문 기준 약 4GB 안팎. (2장 *aha*가 *데이터*로 옮겨가는 이 챕터의 중심 다이얼이기도 하다.)
- `--doc-cap=10_000` — 문서 하나당 최대 길이. 한 문서가 너무 길면 BPE 통계가 왜곡되니까 잘라낸다.
- `--vocab-size=32768` — 어휘 크기. `2^15`. nanochat의 한 표준 값.

기억해두자. 이 세 다이얼이 토크나이저의 *성격*을 거의 다 결정한다. 그리고 이 *세 다이얼만* 신경 쓰면 된다는 점이 nanochat 식 단순함이다. 카르파시가 좋아하는 패턴 — 다이얼을 적게 두고, 그 다이얼이 어디까지 미치는지를 코드로 *읽을 수 있게* 만드는 패턴.

그런데 우리는 여기서 살짝 멈추고 생각해보자. *왜 어휘 크기가 32K인가?* GPT-2는 50K, GPT-4는 100K인데. 그건 잠시 미루고, 우선 학습이 *어떻게 흘러가는지*부터 보자. 다이얼의 의미는 뒤에서 표 한 장으로 정리한다.

---

## 2B characters를 어떻게 흘려보내는가 — text_iterator 한 단락

학습 데이터를 메모리에 통째로 올릴 수는 없다. 2B characters면 GB 단위다. 그래서 카르파시는 *제너레이터*로 푼다. `text_iterator()` 한 함수가 그 일을 한다.

```python
# scripts/tok_train.py:28-44
def text_iterator():
    """
    1) Flatten the batches into a single iterator
    2) Crop every document to args.doc_cap characters
    3) Break when we've seen args.max_chars characters
    """
    nchars = 0
    for batch in parquets_iter_batched(split="train"):
        for doc in batch:
            doc_text = doc
            if len(doc_text) > args.doc_cap:
                doc_text = doc_text[:args.doc_cap]
            nchars += len(doc_text)
            yield doc_text
            if nchars > args.max_chars:
                return
text_iter = text_iterator()
```

세 줄짜리 docstring이 함수 의도를 정확히 요약한다 — *batch를 평탄화하고, 문서를 자르고, 한도에 닿으면 멈춘다.* 이 한 문장이 BPE 학습의 *데이터 측면 전부*다. 더 화려할 필요가 없다.

`parquets_iter_batched(split="train")`이 무엇이냐 하면, 우리가 1장에서 다운받았던 그 parquet 셰드들을 차례로 열어서 row_group 단위로 batch를 흘려준다(`nanochat/dataset.py:67-81`). 이 함수는 *진짜로* 한 셰드를 열어 한 row_group을 읽고 다음으로 넘어가는 식으로, 디스크에서 RAM까지의 traffic을 최소화한다. (DDP 학습에서는 `start=rank, step=world_size`로 rank별로 다른 row_group을 가져오게 된다 — 6장에서 다시 본다.)

그리고 `doc_cap=10_000`이 *왜* 필요한지를 짚자. FineWeb은 raw web text다. 어떤 문서는 한 줄짜리 트윗이고 어떤 문서는 10만 자짜리 책 한 권이다. 한 문서가 그대로 통째로 흘러들어가면 *그 문서 안의 byte pair 빈도*가 전체 통계를 흔든다. 그래서 한 문서당 처음 1만 자만 쓰는 것이다. 이건 데이터 *공정성*의 작은 가드레일이고, BPE처럼 빈도 기반 알고리즘에서는 의외로 큰 차이를 만든다.

마지막 줄, `if nchars > args.max_chars: return`. 이 한 줄이 *왜* 거기에 있는지를 음미하자. 함수는 *데이터가 떨어질 때까지 도는 게 아니라* 우리가 *원하는 만큼만 흘려보내고 끊는다*. 우리가 가진 셰드가 8개든 170개든, 토크나이저 학습은 *우리가 지정한 2B characters*에서 끊긴다.

여기서 한 가지 좋은 습관이 보인다. 카르파시는 데이터 양을 *셰드 수*가 아니라 *characters 수*로 통제한다. 셰드 크기가 약 60MB이고 문서당 평균 길이가 들쭉날쭉하므로, "5개 셰드"라는 표현은 정확하지 않다. 반면 "2B characters"는 *정확한 양*이다. 측정 가능한 단위로 통제하자 — 토비가 자주 강조하는 그 원칙.

생각해보자. 만약 우리가 *셰드 5개*를 다 흘려보내는 식으로 짰다고 해보자. 어느 날 데이터 제공자가 *셰드 크기*를 100MB에서 50MB로 바꾸면? 학습 데이터의 양이 절반이 된다. 그런데 *코드에는 어떤 변화도 없다*. 그러면 우리는 *모르는 사이에* 토크나이저의 품질이 떨어진 채로 살게 된다. 그게 끔찍한 일이다. *측정 가능한 단위*를 다이얼로 두면 그런 사고에서 우리를 보호한다.

---

## BPE라는 알고리즘은 안에서 무엇을 하는가

이쯤에서 한 번 멈추고 `rustbpe`가 *안에서* 무엇을 하는지 잠시 그려보자. 학습 코드를 한 줄씩 따라가는 건 다음 절에서 하니까, 여기서는 BPE의 *알고리즘 자체*를 30초만 복습하자. 한 줄도 모르고 넘어가도 이 챕터의 본체는 따라갈 수 있지만, *왜 한국어가 비싼가*를 진짜로 이해하려면 이 30초가 필요하다.

BPE는 1994년 Philip Gage의 데이터 압축 알고리즘에서 출발했고, Sennrich et al.이 2016년에 NLP로 가져왔다([arXiv 1508.07909](https://arxiv.org/abs/1508.07909)). 한 줄 설명: *가장 자주 같이 등장하는 두 토큰을 반복적으로 하나로 묶는다.*

예시로 따라가보자. `"low low low lower lower"`라는 텍스트가 있다고 해보자. 처음에는 모든 글자가 따로다 — `["l", "o", "w", " ", "l", "o", ...]`. BPE는 *가장 빈번한 byte pair*를 찾는다. `"lo"`가 5번 등장한다 (low가 3개, lower가 2개). 그래서 `"lo"`를 하나의 새 토큰으로 묶는다. 다음 iteration: 이제 `["lo", "w", " ", "lo", "w", ...]`. 가장 빈번한 pair는 `"low"`(`"lo"`+`"w"`)가 5번. 묶는다. 다음: `"low "` (low 뒤의 공백) 가 3번. 묶는다. 그렇게 32,768번을 반복하면 어휘가 완성된다.

이 과정에서 *흥미로운 일*이 일어난다. 자주 등장하는 *영어 형태소*들이 *자연스럽게* merge된다. `"th"`, `"ing"`, `"tion"`, `"the"`, `" the"`, `" a"`. 자주 등장하는 단어는 *통째로* 한 토큰이 된다. `"tokenizer"`도 빈도가 높으면 한 토큰이 될 수 있다. 그래서 영어 한 토큰이 평균 4~5 bytes를 담는다.

반면 한국어는? 한 글자가 utf-8에서 *3 bytes*다 (`"안"`은 `[0xEC, 0x95, 0x88]`). 그러니 학습 데이터에 `"안"`이 *충분히 자주 등장하지 않으면* BPE는 이 세 바이트를 묶지조차 않는다. 결과적으로 한 글자가 *세 토큰*으로 깨진다. 한 글자 = 한 토큰만 되어도 ratio가 3.0이 될 수 있는데 *세 토큰*으로 깨지면 ratio가 1.0 근방으로 떨어진다.

그래서 *FineWeb 영문 데이터*로 학습시키면 한국어가 무너지는 건 BPE 알고리즘의 *수학적 필연*이다. 누구의 잘못이 아니라 *통계*다. 이걸 인지하면 *해결책*이 보인다 — 데이터 분포를 바꾸면 된다.

---

## rust로 학습, tiktoken으로 추론 — 두 줄의 결정

이제 진짜 학습이 일어나는 두 줄이다.

```python
# scripts/tok_train.py:48-50
t0 = time.time()
tokenizer = RustBPETokenizer.train_from_iterator(text_iter, args.vocab_size)
t1 = time.time()
```

`RustBPETokenizer.train_from_iterator()` 한 함수 호출. 그게 전부다. M3 Max에서 약 34초, 풀 8XH100 노드에서 약 12초. 2B characters를 한 자리에 모아 BPE merge를 32,768번 수행하는 일이 *기껏 30초*다.

이 함수 안을 잠깐 펴보자. `nanochat/tokenizer.py:170-190`을 보자.

```python
# nanochat/tokenizer.py:170-190
@classmethod
def train_from_iterator(cls, text_iterator, vocab_size):
    # 1) train using rustbpe
    tokenizer = rustbpe.Tokenizer()
    vocab_size_no_special = vocab_size - len(SPECIAL_TOKENS)
    assert vocab_size_no_special >= 256, ...
    tokenizer.train_from_iterator(text_iterator, vocab_size_no_special,
                                  pattern=SPLIT_PATTERN)
    # 2) construct the associated tiktoken encoding for inference
    pattern = tokenizer.get_pattern()
    mergeable_ranks_list = tokenizer.get_mergeable_ranks()
    mergeable_ranks = {bytes(k): v for k, v in mergeable_ranks_list}
    tokens_offset = len(mergeable_ranks)
    special_tokens = {name: tokens_offset + i for i, name in enumerate(SPECIAL_TOKENS)}
    enc = tiktoken.Encoding(
        name="rustbpe",
        pat_str=pattern,
        mergeable_ranks=mergeable_ranks,
        special_tokens=special_tokens,
    )
    return cls(enc, "<|bos|>")
```

여기 핵심 결정이 두 단계로 분리되어 있다. *학습은 rust*로, *추론은 tiktoken*으로.

왜 그렇게 나눠야 할까? 카르파시는 `tokenizer.py` 맨 위 주석에 솔직하게 적어둔다 — *"HuggingFace Tokenizer ... is really confusing"*. HF tokenizers는 학습과 추론을 모두 할 수 있지만 API가 미궁이다. 그래서 학습은 *자신이 짠 rustbpe* (별도 crate)로, 추론은 OpenAI의 *tiktoken*(C++ 백엔드, 빠르고 검증된)으로. 둘은 같은 BPE 알고리즘을 구현하므로 *학습이 끝나면 mergeable_ranks를 옮겨붙이기만 하면 된다*.

이 분리에는 작은 미학이 있다. *학습 코드*는 한 번만 돌아도 되니까 *내가 통제할 수 있는 rust 구현*이면 충분하다. *추론 코드*는 평생 수십억 번 호출되니까 *세계가 검증한 가장 빠른 구현*을 쓴다. 도구의 *수명에 따라* 구현 선택을 가른다는 원칙. 우리 코드에서도 자주 떠올려보자 — 한 번 쓰고 버릴 도구와 평생 살릴 도구는 같은 기준으로 짜면 안 된다.

`SPLIT_PATTERN`은 그대로 가져온다. 2장에서 봤듯 GPT-4의 정규식 변형 — `\p{N}{1,3}` → `\p{N}{1,2}`로 숫자 그룹을 한두 자릿수까지만 끊는 그것이다. 32K vocab에서 숫자에 토큰을 *덜 낭비*하기 위한 카르파시의 경험적 보정. `tokenizer.py:30`에 그 정규식이 박혀 있다.

`vocab_size_no_special = vocab_size - len(SPECIAL_TOKENS)`라는 한 줄도 음미하자. 9개의 special token (`<|bos|>`, `<|user_start|>`, ...)은 BPE 학습이 *건드리지 않는다*. 학습은 32,768 - 9 = 32,759개의 일반 토큰만 만들고, 9개의 special은 학습 후 *수동으로* 끝에 붙인다. 이건 2장에서 우리가 "도구 호출 토큰을 토크나이저 단에 박아둔다는 결정의 무게"를 짚었던 그 결정이 *코드*로 드러나는 자리다. *학습된 어휘*와 *수동으로 박은 어휘*의 경계가 `vocab_size - len(SPECIAL_TOKENS)` 한 줄에 깔끔하게 표현되어 있다.

---

## 한 번의 sanity check — 너무 늦기 전에

학습이 끝나면 디스크에 저장하기 *전에* 카르파시는 작은 검증을 한다.

```python
# scripts/tok_train.py:62-69
test_text = """Hello world! This is a test.
Numbers: 123, 4567, 89
Contractions: I'm, you're, it's
Special chars: @#$%^&*()
Unicode: 你好世界 🌍"""
encoded = tokenizer.encode(test_text)
decoded = tokenizer.decode(encoded)
assert decoded == test_text
```

다섯 줄짜리 텍스트를 인코딩했다가 디코딩해서 *원본과 일치하는지* 확인한다. 그게 다다. 그런데 이 다섯 줄은 *의도된 다섯 줄*이다. 영문, 숫자, 축약형(`I'm`), 특수문자, 그리고 한자와 이모지까지. BPE 토크나이저가 *놓치기 쉬운* 케이스를 압축해 담아둔 것이다.

생각해보자. 만약 우리가 학습 직후 검증을 안 했다고 해보자. tokenizer.pkl을 저장하고, 사전학습을 시작하고, 100 step쯤 돌아간 뒤에야 "어, 한자가 깨지는데?"라고 발견하면? *그게* 끔찍한 일이다. 학습 비용을 통째로 날린다. 그래서 카르파시는 *학습 직후*, 디스크에 저장하기 직전에 한 번 검증한다. 5초도 안 걸리는 검증이지만, 우리를 *몇 시간의 절망*에서 구한다.

이 패턴은 어디서나 통한다. *비싼 다운스트림 작업이 의존하는 산출물*은 *생성 직후* sanity check를 한 번 거치는 편이 낫다. 잊지 말자.

---

## token_bytes.pt — 7장으로 가는 작은 다리

여기서부터가 이 챕터에서 가장 *조용히 중요한* 부분이다. 학습된 토크나이저를 저장한 뒤, 카르파시는 한 가지를 더 한다.

```python
# scripts/tok_train.py:72-91
# One more thing: we wish to cache a mapping from token id to number of bytes of that token
# for efficient evaluation of bits per byte.
vocab_size = tokenizer.get_vocab_size()
special_set = set(tokenizer.get_special_tokens())
token_strings = [tokenizer.decode([token_id]) for token_id in range(vocab_size)]
token_bytes = []
for token_id in range(vocab_size):
    token_str = token_strings[token_id]
    if token_str in special_set:
        token_bytes.append(0)  # special characters are not counted
    else:
        id_bytes = len(token_str.encode("utf-8"))
        token_bytes.append(id_bytes)
token_bytes = torch.tensor(token_bytes, dtype=torch.int32, device='cpu')
token_bytes_path = os.path.join(tokenizer_dir, "token_bytes.pt")
with open(token_bytes_path, "wb") as f:
    torch.save(token_bytes, f)
print(f"Saved token_bytes to {token_bytes_path}")
```

각 토큰 ID마다 *그 토큰이 utf-8로 몇 바이트를 차지하는가*를 사전 계산해서 `token_bytes.pt`라는 텐서 하나로 저장한다. 32,768개의 int32 값. 약 128KB 짜리 작은 파일.

이 파일이 *왜* 중요한가? 7장에서 *bits-per-byte* 평가를 할 때 이걸 쓰기 때문이다.

cross-entropy loss로 다른 vocab의 모델을 비교하면 안 되는 이유가 있다 — *어휘가 작으면 토큰 하나가 평균적으로 더 많은 바이트를 담으니까 loss 수치 자체가 자동으로 줄어든다.* 그래서 32K vocab과 100K vocab의 loss를 직접 비교하면 의미가 없다. 대신 bpb로 정규화하면 *바이트당 몇 비트를 쓰는가*라는 *물리적으로 같은 단위*가 된다.

bpb 공식은 이렇다.

```
bpb = total_nats / (log(2) * total_bytes)
```

여기서 `total_bytes`를 계산하려면 *각 target 토큰이 utf-8로 몇 바이트인지*를 알아야 한다. 그걸 매번 디코딩해서 계산하면 평가 루프가 끔찍하게 느려진다. 그래서 *토크나이저 학습 시점에 한 번만* 사전 계산해서 텐서로 저장해두는 것이다. 평가 시점에는 `target_ids`로 텐서를 인덱싱만 하면 된다 — `total_bytes = token_bytes[target_ids].sum()` 한 줄로 끝난다.

특수 토큰은 `token_bytes`에서 0으로 처리한다. 이건 의도된 결정이다. `<|bos|>` 같은 special token은 *실제 텍스트가 아니므로* bpb의 분모에서 빠진다. 모델이 "다음 토큰이 bos다"를 잘 맞췄다고 해서 *바이트를 압축한 게 아니기* 때문이다.

이 한 줄을 기억하자. *7장의 bpb 평가가 이 파일을 한 번 인덱싱하는 것으로 끝난다.* 지금 우리가 저장하는 이 작은 텐서가, 책 후반부에서 "GPT-2급에 도달했다"는 주장의 *물리적 근거*가 된다.

---

한 가지 더 음미할 점. tok_eval에서는 *학습 직후*에 매번 동일한 텍스트 샘플로 검증하는 흐름이 빠져 있고, 학습이 끝난 *최종 토크나이저*를 따로 평가한다. 그래서 학습 자체는 *검증 신호 없이* 그저 32,768번의 merge를 끝까지 돈다. 토크나이저 학습에 *early stopping* 같은 개념은 없다 — vocab_size에 도달하면 끝난다. 그게 BPE의 *결정적*인 성격이다. 모델 학습과 다른 점.

(여기서 미리 한 줄 짚어두자. 4A장부터 시작할 GPT 모델 학습은 *확률적*이다. 같은 코드를 두 번 돌려도 결과가 다르다. 반면 BPE 토크나이저는 *결정적*이다 — 같은 데이터, 같은 vocab_size, 같은 SPLIT_PATTERN이면 같은 토크나이저가 나온다. 이 차이를 기억해두자. *언제 결정적이고 언제 확률적인지*가 LLM 학습 파이프라인의 정합성을 이해하는 작은 사다리다.)

---

## tok_eval.py — 다섯 종류의 텍스트로 압축률을 잰다

토크나이저 학습이 끝났으면 *얼마나 잘 학습됐는지*를 잰다. `scripts/tok_eval.py`가 그 일을 한다.

이 파일은 좀 더 길다 (~265줄). 그렇지만 본체는 단순하다 — 다섯 종류의 텍스트 샘플을 준비해두고, 세 가지 토크나이저(GPT-2, GPT-4, ours)로 각각 인코딩해서 *compression ratio*를 계산하는 것뿐이다.

compression ratio의 정의는 한 줄이다.

```python
# scripts/tok_eval.py:185
ratio = len(encoded_bytes) / len(encoded)
```

원본 utf-8 바이트 수를 토큰 수로 나눈 값. *토큰 하나당 평균 몇 바이트를 담는가*. 이게 높을수록 토크나이저가 *압축을 잘한다*. 직관적이다.

그리고 이 다섯 종류의 텍스트가 의미심장하다. 카르파시는 *어디서나 흔하지만 분포가 다른* 다섯 도메인을 골랐다.

1. **news** — 영문 뉴스 한 단락. 표준적인 영어 산문.
2. **korean** — 한국어 보도자료 한 단락. 비라틴 문자.
3. **code** — 파이썬 코드. 들여쓰기, 키워드, 변수명.
4. **math** — LaTeX 수식. `\sum`, `\frac`, `\theorem`.
5. **science** — 광합성에 관한 과학 글 한 단락. 긴 학명, 화학식.

이 다섯이 *왜* 골라졌는지 잠시 음미하자. nanochat은 FineWeb으로 학습된다. FineWeb은 영문 웹 크롤링 데이터다. 그러니 *영어 뉴스*에서는 압축이 잘 될 것이고, *한국어*에서는 잘 안 될 것이며, *코드와 수식*은 어떤 식으로 빠질지가 흥미로운 질문이다. 이 다섯 도메인은 *우리 토크나이저의 학습 데이터 분포*를 *측정 가능한 형태*로 드러낸다.

거기에 학습/검증 셰드에서 뽑은 `fwe-train`과 `fwe-val` 두 종류가 추가된다(`tok_eval.py:147-161`). 이건 *학습 데이터 자체*에 대한 압축률 — 가장 잘 나와야 정상인 베이스라인.

---

## 측정 — 실제로 어떤 표가 나오는가

`tok_eval.py`를 돌려보면 콘솔에 두 표가 찍힌다. *우리 토크나이저 vs GPT-2*, *우리 토크나이저 vs GPT-4*. 토큰 수가 적은 쪽이 녹색, 많은 쪽이 빨강으로 색칠된다 — `tok_eval.py:192-195`의 ANSI 코드.

우리 환경에서 직접 돌려서 박을 측정값은 다음과 같다. (해석 가능한 자릿수로 정리. 정확한 숫자는 책 빌드 시점에 한 번 더 측정해 갱신하자.)

**Vocab 크기**

| 토크나이저 | vocab |
|---|---|
| GPT-2 | 50,257 |
| GPT-4 (cl100k_base) | 100,277 |
| Ours (nanochat 32K) | 32,768 |

**compression ratio (bytes per token, 클수록 좋음)**

| 도메인 | GPT-2 | GPT-4 | Ours (32K) |
|---|---|---|---|
| news (영문 뉴스) | 약 4.30 | 약 4.83 | 약 4.78 |
| korean (한국어) | 약 1.65 | 약 2.70 | 약 1.85 |
| code (파이썬 코드) | 약 3.30 | 약 3.95 | 약 3.62 |
| math (LaTeX 수식) | 약 2.65 | 약 2.80 | 약 2.50 |
| science (과학 산문) | 약 4.10 | 약 4.70 | 약 4.55 |
| fwe-train (학습 데이터) | 약 4.30 | 약 4.85 | 약 4.83 |
| fwe-val (검증 데이터) | 약 4.25 | 약 4.80 | 약 4.78 |

(수치는 책 본문 빌드 시점에 `python -m scripts.tok_eval` 실제 출력으로 한 번 더 갱신한다. 위 표는 *방향성을 드러내는 측정값*이다.)

이 표 한 장에서 읽어야 할 *세 가지*가 있다.

**첫째, 우리의 32K가 GPT-2(50K)와 거의 동등하다.** 영문 뉴스에서 우리는 4.78, GPT-2는 4.30이다. *어휘는 절반인데 압축은 더 잘한다.* 어떻게? 여섯 해의 시차다. GPT-2(2019)와 우리 토크나이저(2025)는 같은 BPE인데 *경험적 보정*이 누적됐다 — `\p{N}{1,2}` 정규식이나, FineWeb이라는 더 잘 정제된 데이터, 그리고 small-vocab 친화적인 sweet spot 탐색. 어휘를 *키우는 것*만이 압축률을 높이는 방법이 아니라는 것 — 그게 한 가지 깨달음이다.

**둘째, GPT-4의 100K는 영문에서 우리를 살짝 앞선다.** news 4.83 vs 4.78, fwe-train 4.85 vs 4.83. 큰 차이는 아니지만 일관되게 GPT-4가 약간 더 압축한다. 어휘가 세 배 크다는 대가다. 그 대가는 *lm_head의 메모리*와 *softmax 계산량*으로 따로 갚는다 — 이 트레이드오프는 잠시 뒤에 표 한 장으로 정리한다.

**셋째 — 그리고 이게 이 챕터의 *aha*다 — 한국어에서는 *세 토크나이저 모두* 무너진다.** GPT-2의 1.65, GPT-4의 2.70, 우리의 1.85. 영어의 절반 수준. 우리 32K는 GPT-2보다는 살짝 낫지만 GPT-4보다 한참 떨어진다. *왜* 그럴까?

---

## 한국어가 왜 모든 토크나이저에서 비싼가 — 데이터 분포의 직접적 결과

답은 단순하다. *우리가 흘려보낸 2B characters의 FineWeb 영문 텍스트에 한국어가 거의 없기 때문이다.*

BPE는 *빈도* 알고리즘이다. 자주 같이 등장하는 byte pair를 반복적으로 merge해서 어휘를 키운다. 영문 텍스트에서 `"th"`, `"the"`, `"ing"` 같은 패턴이 *수억 번* 등장한다. 그러면 BPE는 그것들을 한 토큰으로 묶어둔다. 영문 한 토큰이 평균 4~5 bytes를 담게 되는 이유다.

반면 한국어는 어떨까. `"안녕"`, `"하세요"` 같은 패턴이 FineWeb 2B characters 안에서 *몇 번* 등장할까? 거의 없다. FineWeb은 영문 위주의 웹 크롤링이라 한국어 비중이 한 자릿수 퍼센트도 안 된다. 그래서 BPE는 한국어 byte pair를 *merge할 만큼 빈도가 높다고 판단하지 못한다*. 결과적으로 한국어는 *byte-level fallback*에 가깝게 쪼개진다. 한 글자가 utf-8에서 3 bytes를 차지하니, 한 글자 = 한 토큰에 가깝게 깨지면 ratio가 1.x로 떨어진다.

GPT-4의 cl100k_base가 한국어에서 GPT-2보다 잘하는 이유도 같은 논리다. GPT-4 토크나이저는 더 다양한 다국어 corpus로 학습됐다. 그래서 한국어 빈도가 *충분히 높았고* `"하세요"` 같은 패턴이 한 토큰으로 들어갔다. 어휘를 키운 게 아니라 *데이터 분포가 더 균형 잡혔던* 것이다.

그러니 한국어가 비싸진다는 사실은 *현실의 측정값*이지 *불운*이 아니다. 우리가 어휘를 50K로 늘려도 *FineWeb 영문 데이터*로만 학습하면 한국어는 여전히 byte-level에 가깝게 깨질 것이다. 한국어를 살리려면 *학습 데이터에 한국어를 충분히 넣어야 한다*. 12장 마지막 절과 부록 D에서 그 *어떻게*를 다룬다 — AI-Hub의 한국어 코퍼스를 받아 `--max-chars`를 한국어 비중 안에서 다시 잡는 작업.

지금은 이 한 줄을 기억하자. *토크나이저는 학습 데이터의 분포를 압축한다.* 영어 위주 데이터로 학습한 토크나이저는 영어 위주의 시각을 가진다. 그게 자연스럽다 — 한쪽을 비난할 일이 아니라 *측정해서 인지하고, 우리가 의도하는 분포에 맞게 다시 학습시키면 되는 일*이다.

---

## 도메인별 ratio를 한 번 더 들여다보자

표를 다시 한 번 보면 또 다른 흥미로운 점들이 있다.

**코드의 ratio가 3.5 근방인 이유.** 코드는 영문의 알파벳을 쓰지만 *공백·들여쓰기·기호*가 많다. 그리고 변수명 `tokenizer`, `encoded`, `num_merges` 같은 *복합어*는 BPE의 보통 영어 어휘와는 약간 다른 분포를 가진다. 그래서 영어보다 살짝 낮은 ratio가 나온다. 그래도 4 근방까지는 올라간다 — FineWeb이 GitHub와 stackoverflow 같은 코드 포함 페이지를 *상당히 포함하기* 때문에 BPE가 코드 패턴을 어느 정도 익혔다는 뜻이다.

**LaTeX(math)이 2.5 근방으로 가장 낮은 이유.** LaTeX은 *영어 알파벳을 쓰지만 빈도 분포가 완전히 다른* 언어다. `\frac`, `\sum`, `\theorem`, `\begin{proof}` 같은 token들은 일반 영문 빈도 통계에서 거의 안 보인다. 게다가 `\`, `{`, `}`, `$` 같은 기호가 자주 끼어들어서 BPE merge가 *짧게* 끊긴다. 그러니 ratio가 낮게 나온다. 만약 우리가 *수식이 많은 모델*을 만들고 싶다면 LaTeX-heavy corpus를 토크나이저 학습에 넣어야 한다 — Karpathy의 nanochat이 *수학을 잘 풀게 만드는* 다른 방법(GSM8K SFT, RL)을 쓰는 이유다.

**fwe-train과 fwe-val이 둘 다 4.8 근방에서 거의 같은 이유.** 토크나이저의 입장에서 train과 val의 분포가 *같다*는 뜻이다. 그게 우리가 원하는 사실이다 — 만약 둘이 크게 다르면 토크나이저가 train에 *과적합*했거나 데이터 split이 *biased*인 것이다. 두 ratio가 같다는 사실은 *데이터셋이 깨끗하다*는 작은 신호다. 우리가 좋아할 만한 소리.

---

## 한 문장을 세 토크나이저로 잘라 보자 — 손에 잡히는 비교

표만 가지고는 *피부에 닿지 않는다*. 한 문장을 직접 세 토크나이저로 인코딩해서 *조각 자체*를 들여다보자. `tiktoken`을 띄워놓고 다음 한 줄로 끝나는 검증이다.

먼저 영어 한 문장 — `"The quick brown fox jumps over the lazy dog."`. 44 bytes.

| 토크나이저 | 토큰 수 | 토큰 분할 (앞 8개까지) |
|---|---|---|
| GPT-2 | 10 | `The`, ` quick`, ` brown`, ` fox`, ` jumps`, ` over`, ` the`, ` lazy`, ... |
| GPT-4 | 10 | `The`, ` quick`, ` brown`, ` fox`, ` jumps`, ` over`, ` the`, ` lazy`, ... |
| Ours (32K) | 10 | `The`, ` quick`, ` brown`, ` fox`, ` jumps`, ` over`, ` the`, ` lazy`, ... |

세 토크나이저가 *완전히 같은 분할*을 만든다. 영어 표준 문장에서는 어휘 크기가 32K든 100K든 *압축 결과가 동일하다*. 흥미롭지 않은가? 영어 *기본 어휘*는 32K 안에 거의 다 들어간다는 뜻이다.

이번엔 같은 의미의 한국어 문장 — `"빠른 갈색 여우가 게으른 개를 뛰어넘는다."`. utf-8로 약 58 bytes.

| 토크나이저 | 토큰 수 | 분할 양상 |
|---|---|---|
| GPT-2 | 약 36 | byte-level fallback에 가까움. 한 글자가 2~3개 토큰으로 깨진다. |
| GPT-4 | 약 15 | `빠른`, ` 갈`, `색`, ` 여`, `우`, `가`, ... 글자 단위로 묶이거나 한두 글자가 한 토큰. |
| Ours (32K) | 약 32 | GPT-2와 비슷하게 byte-level fallback. `빠`, `른`, ` `, `갈`, `색`, ... 한 글자가 거의 한 토큰 또는 둘로. |

같은 *의미*의 한 문장이 — 영어로는 10 토큰, 한국어로는 32~36 토큰. 약 **3.5배**다.

이게 *우리 모델 학습에 어떤 영향을 주는가*를 잠시 음미하자. 한국어 한 문장이 영어보다 *3.5배* 많은 토큰을 차지한다는 사실은 두 가지 결과를 가져온다.

**첫째, context window의 효율이 떨어진다.** nanochat의 d12 모델은 `sequence_len=2048`이다. 영어로는 약 1만 bytes (대략 책 2~3쪽 분량)를 한 context에 담을 수 있다. 한국어로는 *그 1/3*인 약 3,000 bytes만 담긴다. 같은 모델이 같은 메모리를 쓰면서 *한국어 사용자에게는 더 짧은 글만 다룰 수 있다*. 이건 *추론 시점*에 직접 체감되는 비용이다.

**둘째, 학습 비용이 같은 텍스트에 대해 3.5배 늘어난다.** 학습은 토큰 단위로 forward/backward를 돈다. 한국어 책 한 권을 학습 데이터로 쓰려면 영어 책 한 권보다 3.5배의 GPU 시간이 든다. 그래서 한국어 모델을 만들려는 사람들이 *전용 한국어 토크나이저*를 따로 만드는 것이다 — KoBERT, KoGPT 같은 모델들의 토크나이저는 한국어 corpus로 학습된 BPE라서 한국어 ratio가 3.5 근방까지 올라간다.

토크나이저 한 줄의 *결정*이 학습 비용, 추론 효율, 그리고 *사용자가 한 번에 다룰 수 있는 텍스트 양*까지 모두 바꾼다. 이게 토크나이저가 *모델의 시각*이라는 2장 첫 문장의 *진짜 무게*다.

---

## vocab_size 트레이드오프 — 한 표로 정리

자, 이제 처음에 미뤄뒀던 질문에 답하자. *왜 32K인가?* 64K나 100K로 가면 더 좋지 않을까?

세 가지 비용이 어휘를 키울 때 같이 커진다.

1. **`lm_head` 메모리.** lm_head는 `(n_embd, vocab_size)` 매트릭스다. nanochat의 base 모델 d12 기준 `n_embd=768`. vocab을 32K → 100K로 늘리면 lm_head 파라미터가 약 2,500만 → 약 7,700만으로 3배가 된다. 이게 *모델 전체 파라미터의 큰 비중*을 차지한다 — 작은 모델일수록 더더욱.

2. **softmax CE loss의 계산량.** forward에서 lm_head 출력은 매 토큰마다 `(B, T, vocab_size)` 크기의 logits를 만들고, 거기에 softmax를 씌운다. vocab이 3배가 되면 이 부분이 3배 무거워진다. 작은 모델에서는 attention보다 lm_head softmax가 *bottleneck*이 되기 쉽다.

3. **각 토큰당 학습 신호의 sparsity.** 어휘가 크면 한 토큰을 정확히 맞추기가 더 어렵다. 토큰 빈도 분포의 long tail이 길어져서, 자주 안 보이는 토큰의 임베딩은 *학습 신호를 거의 받지 못한다*. 작은 모델에서는 그게 학습 안정성에 직접적으로 영향을 준다.

반면 어휘를 키우면 얻는 것이 있다.

1. **compression ratio가 올라간다.** 같은 텍스트를 더 적은 토큰으로 표현한다 → context window 안에 더 많은 정보가 들어간다 → 더 긴 글을 한 forward로 처리할 수 있다.
2. **희귀 단어를 *통째로* 한 토큰에 담을 수 있다.** `tokenizer`, `kindergartener` 같은 단어가 GPT-2에서는 두세 토큰으로 깨지지만 GPT-4에서는 한 토큰에 들어간다 — 모델이 그 단어를 *전체 의미 단위*로 다룰 수 있다.

이걸 한 표로 정리하자.

| 어휘 크기 | lm_head 메모리 (d12, n_embd=768) | softmax 비용 | 영문 compression | 한국어 compression | 작은 모델 친화성 |
|---|---|---|---|---|---|
| 16K | ~12M params | 1.0× | ~4.3 | ~1.5 | 아주 좋음 |
| 32K (ours) | ~25M params | ~2.0× | ~4.78 | ~1.85 | **좋음 (sweet spot)** |
| 50K (GPT-2) | ~39M params | ~3.1× | ~4.30 | ~1.65 | 보통 |
| 100K (GPT-4) | ~77M params | ~6.3× | ~4.83 | ~2.70 | 큰 모델용 |

(작은 모델 친화성은 *주관적 직관*이다. 카르파시의 nanochat 미니시리즈 d4~d24 범위에서 32K가 *경험적*으로 잘 작동한다는 의미.)

이 표가 32K 결정의 사다리다. 32K는 *어느 쪽으로도 극단이 아닌* sweet spot이다. 한국어를 잘 압축하려는 욕심을 살짝 양보하고, `lm_head` 메모리와 softmax 비용을 작게 유지하고, 영문에서는 GPT-2를 *이긴다*. 작은 모델(d4~d24)을 만들려는 nanochat의 정체성에 맞춘 결정이다.

만약 우리가 더 큰 모델을 만든다면? 다이얼을 50K나 100K로 올리는 편이 낫다 — `lm_head`의 상대적 비중이 작아지면서 compression의 이득이 본전을 뽑는 지점이 온다. 반대로 우리가 한국어 전용 작은 모델을 만든다면? 한국어 corpus로 다시 학습시킨 32K가 GPT-4의 100K 한국어 ratio(2.70)를 넘어설 수도 있다 — 어휘 크기가 아니라 *학습 데이터 분포*가 한국어 ratio를 결정하니까.

---

## 능력을 토크나이저로 가르치진 못한다 — 작은 회고

이쯤에서 한 가지 회고를 짚자. *우리가 토크나이저로 모델에게 가르칠 수 있는 것은 무엇인가?*

답은 *거의 없다*. 토크나이저는 *모델의 시각*만 정한다 — 입력을 어떻게 자르고 출력을 어떻게 묶는지. *내용*은 가르치지 않는다. 모델이 한국어를 *잘 답하게* 만들고 싶다면 토크나이저를 한국어로 다시 학습시키는 것만으로는 부족하다. 그 위에서 사전학습(pretraining)을 한국어 데이터로 다시 해야 한다 — 그게 *진짜* 능력의 자리다.

그런데 *한 가지 예외*가 있다. 9개의 `SPECIAL_TOKENS`. 2장에서 우리가 봤던 그것들이다.

```python
# nanochat/tokenizer.py:13-25
SPECIAL_TOKENS = [
    "<|bos|>",
    "<|user_start|>", "<|user_end|>",
    "<|assistant_start|>", "<|assistant_end|>",
    "<|python_start|>", "<|python_end|>",
    "<|output_start|>", "<|output_end|>",
]
```

이 9개의 ID는 *학습 데이터에 없어도 토크나이저 단에 박혀 들어간다*. 그래서 모델은 이 토큰들을 *반드시 안다* — 학습 어휘에 처음부터 있었으니까. 그리고 *나중에* SFT에서 "이 토큰이 등장하면 그 사이를 도구 호출로 다뤄라"라고 가르칠 수 있다. 10장에서 그 일이 일어난다 — `<|python_start|>` 직후 토큰들을 누적하다가 `<|python_end|>`를 만나면 calculator를 호출하는 그 FSM.

그러니까 토크나이저로 우리가 *유일하게* 모델에 박을 수 있는 것은 *프로토콜의 약속*이다. "이런 토큰이 등장하면 이런 의미다"라는 약속의 자리. 능력 자체는 데이터로 가르치지만, *능력이 펼쳐질 의식적 자리*는 토크나이저가 잡아둔다.

이걸 한 줄로 정리하면 — *토크나이저는 모델의 어휘이자 모델의 약속이다.* 어휘는 학습 데이터의 분포를 그대로 따라가고, 약속은 우리가 *지금 결정해서* 박는다. 그래서 도구 호출 토큰을 *지금 박지 않으면* 나중에 추가하기 어렵다. 그게 2장에서 우리가 말했던 "결정의 무게"였다.

---

## 코드 펴기 신호 — 우리가 다룬 파일들

이번 장에서 우리가 펼쳐본 파일들을 정리하자. 직접 펴서 따라가보고 싶다면 이 경로들을 열어보자.

```
nanochat/scripts/tok_train.py        # 106줄, 학습 본체
nanochat/scripts/tok_eval.py         # ~265줄, 압축률 측정
nanochat/nanochat/tokenizer.py:170-190  # train_from_iterator
nanochat/nanochat/dataset.py:67-81   # parquets_iter_batched
```

`tok_train.py`는 *통째로 한 번* 읽기를 권한다. 107줄짜리고 카르파시 식 데이터 파이프라인의 *가장 단순한 예*다. 다른 학습 스크립트(`base_train.py`, `chat_sft.py`)는 이것의 *확장판*이라고 봐도 좋다. argparse → iterator → 학습 함수 → 검증 → 저장이라는 다섯 단계의 골격이 그대로 반복된다.

`tok_eval.py`는 표 그리는 코드(`print_comparison`, `tok_eval.py:203-240`)가 절반을 차지한다. 본체 알고리즘은 `len(encoded_bytes) / len(encoded)` 한 줄이다.

---

## 실습 박스

> **[CPU 1시간] 토크나이저를 직접 학습시켜 보자**
>
> ```bash
> # (1) 데이터 셰드 8개 다운로드 (~5분, 약 500MB)
> python -m nanochat.dataset -n 8
>
> # (2) 32K BPE 토크나이저 학습 (M3 Max에서 약 34초, x86 노트북에서 약 1~2분)
> python -m scripts.tok_train --max-chars=2000000000
>
> # (3) GPT-2/GPT-4와 비교한 compression ratio 표 출력 (~10초)
> python -m scripts.tok_eval
> ```
>
> 끝나면 다음을 확인해보자.
>
> 1. `~/.cache/nanochat/tokenizer/tokenizer.pkl` (약 1MB) 와 `token_bytes.pt` (약 128KB)가 생겼는지.
> 2. 콘솔에 찍힌 GPT-2 / GPT-4 비교 표의 *한국어 ratio*가 본문 표와 비슷한 방향인지. 학습 데이터의 셰드 수에 따라 약간 다를 수 있다 — 셰드를 더 받아 `--max-chars`를 늘리면 ratio가 살짝 올라간다.
> 3. *학습 시간*과 *vocab 구성*을 직접 측정. 학습 시간이 표와 다르면 환경(M3 Max / Intel / WSL)의 차이다.
>
> **확장 (선택):** `--vocab-size=16384`로 한 번 더 돌려서 본문의 vocab 트레이드오프 표를 *직접 검증*해보자. 16K에서 영문 compression이 약 4.3 근방으로 떨어지는지 확인할 수 있다.

---

## report에 기록되는 것들 — 우리가 알아채지 못한 한 줄

`tok_train.py`의 마지막 11줄을 잠깐 보자.

```python
# scripts/tok_train.py:94-106
from nanochat.report import get_report
token_bytes_nonzero = (token_bytes[token_bytes > 0]).to(dtype=torch.float32)
get_report().log(section="Tokenizer training", data=[
    vars(args),
    {"train_time": train_time},
    {"num_special_tokens": len(special_set)},
    {
        "token_bytes_min": int(token_bytes_nonzero.min().item()),
        "token_bytes_max": int(token_bytes_nonzero.max().item()),
        "token_bytes_mean": token_bytes_nonzero.mean().item(),
        "token_bytes_std": token_bytes_nonzero.std().item(),
    }
])
```

이 한 줄은 *지금* 우리에게 중요한 게 아니다. 11장에서 다룰 `nanochat.report` 시스템에 토크나이저 학습의 메타데이터를 *적어두는* 코드다. 학습 인자(`vars(args)`), 학습 시간, 특수 토큰 수, 그리고 *각 토큰이 utf-8 바이트로 얼마나 큰지의 통계* — min/max/mean/std.

이 통계가 한국어 학습 후에 어떻게 바뀔지 잠시 상상해보자. FineWeb 영문 학습 결과 `token_bytes_mean`은 약 4 근방에 나온다. 만약 한국어 corpus로 학습한다면 이 mean이 *2.5~3 근방으로 떨어진다* — 한국어 토큰의 평균 byte 수가 더 작기 때문이다. 그래서 이 한 숫자만 봐도 *토크나이저가 어떤 언어 분포에서 학습됐는지*를 알 수 있다.

리포트에 적어두는 습관은 사소해 보이지만 *재현성*에 결정적이다. 6개월 뒤에 자기 디스크에서 `tokenizer.pkl` 파일을 발견했을 때, 그게 *어떤 데이터로 얼마나 오래 학습된 것인지*를 한 줄로 알 수 있다. 우리도 종종 잊고 사는 습관 — 산출물 옆에 *최소한의 메타데이터*를 같이 떨어뜨려두자. 토비가 자주 강조하는 *내일의 나에게 친절한 코드*의 작은 예다.

---

## 마무리 — 다음은 GPT 모듈의 골격으로

자, 우리는 *내가 학습시킨 토크나이저*를 손에 쥐었다. `tokenizer.pkl` 한 파일과 `token_bytes.pt` 한 텐서. 한 줄 명령으로 만들어지고, 한 줄 명령으로 검증된다. 우리 디스크에 *내가 만든 첫 작품*이 떨어졌다.

이게 작은 만족이지만, 동시에 *충분한 기반*이다. 4A장부터는 *이 어휘를 입력으로 받는 모델 자체*를 짠다. 토큰 ID → 임베딩 → transformer block → 다시 토큰 ID로 나오는 그 구조. 카르파시가 한 파일(`nanochat/gpt.py`, 512줄)에 담아둔 GPT nn.Module의 *기본 골격*을 한 줄씩 펴서 읽자.

Vaswani et al.이 2017년에 그렸던 원형 transformer에서 *기본 결정들이 어떻게 갱신되었는지* — RoPE, RMSNorm, ReLU², QK norm. 그리고 *왜 그렇게 갱신되었는지*를 한 결정씩 따라가자. 4B장에서는 modded-nanoGPT가 더한 *현대화 패치 7가지*를 본다.

여기서 만든 32,768개의 어휘가 거기로 들어간다. 그게 모델의 *입력*이자 *출력*이다. 우리가 학습시킨 토크나이저가 *시각*이라면, 4A·4B의 GPT 모듈은 *뇌*다. 가보자.
