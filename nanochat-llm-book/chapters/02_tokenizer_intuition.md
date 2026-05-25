# 2장. 토크나이저는 모델이 세상을 보는 단위다

ChatGPT에게 이렇게 물어본 적이 있을 것이다.

> "strawberry에 r이 몇 개 들어 있지?"

질문이 너무 단순해서 *AI*에게 묻기 민망하다. 그런데 어이없게도 한때 GPT-4조차 이걸 *틀렸다*. "2개"라고 답하거나, "3개"라고 답한 다음 다시 "2개"라고 정정하거나, 갈팡질팡했다. 사람이라면 글자를 손가락으로 짚어가며 셀 텐데, 이 거대한 언어 모델은 왜 *그 짓*을 못 했을까?

답은 *간단하면서도 충격적*이다. **모델은 `strawberry`라는 단어를 *글자 단위*로 보지 않는다.** 모델의 눈에 `strawberry`는 `"straw"`+`"berry"` 같은 *두 덩어리*거나, 어떤 토크나이저에서는 `"str"`+`"aw"`+`"berry"`로 보일 수도 있다. 인간이 *글자*라고 부르는 것의 자리에, 모델은 *서브워드(subword) 토큰*이라는 다른 단위를 본다. 그 단위 안에 `r`이 몇 개 박혀 있는지는 *덩어리 바깥에서* 셀 수가 없다. 글자를 못 보는 사람한테 "이 단어에 r이 몇 개 있어?"라고 묻는 것과 같다. 난감한 일이다.

이게 토크나이저(tokenizer) 이야기다. 토크나이저는 *모델이 세상을 보는 단위*를 결정한다. 단위가 무엇이냐에 따라 모델은 `count('r')` 같은 사소해 보이는 일에서 무너지고, 같은 한국어 문장이 *어떤 모델에서는 비싸고 어떤 모델에서는 싸진다*. 토크나이저는 그저 텍스트를 자르는 도구가 아니라, **모델의 시각 자체**다.

그렇다면 nanochat은 이 *시각*을 어떻게 정의해 두었을까? 함께 그 코드를 펴보자.

---

## 2.1 BPE의 직관 — `strawberry`는 어떻게 두 덩어리가 되는가

토크나이저에는 여러 종류가 있다. 글자(character) 단위, 단어(word) 단위, 서브워드(subword) 단위. 현대 LLM은 거의 예외 없이 *서브워드 단위*를 쓴다. 그중에서도 **BPE(Byte Pair Encoding)**가 사실상 표준이다. nanochat도 BPE를 쓴다.

*왜* 글자 단위도 아니고 단어 단위도 아닌, *그 사이*의 어정쩡한 *서브워드*를 쓸까? 잠시 함께 생각해보자.

*글자 단위*로 가면 어떤 일이 벌어질까? 어휘 크기가 *압도적으로 작아진다* — 영어라면 100개도 안 된다 (알파벳 + 숫자 + 기호). 메모리는 가벼워진다. 하지만 *시퀀스가 길어진다*. `Transformer architecture`가 *28자*다 — 28토큰이 된다. 게다가 *의미 단위*가 *글자에 흩어져 있어서* 모델이 *처음부터 다 모아야* 한다. *학습이 비효율적*이 된다.

*단어 단위*로 가면? 시퀀스는 짧아진다. *의미 단위*가 *한 토큰에 모인다*. 그런데 *어휘가 폭발*한다. 영어 단어가 수십만 개, *그 활용형*까지 합치면 *수백만 개*. `running`, `runs`, `run`이 다 *다른 토큰*이 된다. 그러고도 *처음 보는 단어*가 등장하면? *OOV(Out-Of-Vocabulary)* 문제 — 모델이 처리를 못 한다. *고유명사 하나*가 모델을 멈춰 세운다. 끔찍한 일이다.

서브워드는 *둘의 균형*이다. *흔한 단어*는 한 토큰으로(`the`, `running`), *드문 단어*는 *서브워드 조합*으로 표현한다(`strawberry` = `straw` + `berry`, `unbelievable` = `un` + `believe` + `able`). 어휘는 *적당히 작고*(보통 30K~100K), 시퀀스는 *적당히 짧고*, *OOV가 사실상 없다*(byte-level fallback 덕분에). *합리적인 균형점*이다.

BPE는 *이름이 다 말해주는* 알고리즘이다. 가장 빈번한 *바이트 쌍(byte pair)*을 반복적으로 *병합(merge)*한다. 한 줄이면 끝나는 직관인데, 살짝 풀어보자.

먼저 텍스트를 *바이트 수준*까지 잘게 쪼갠다. 영어로 `strawberry`라면 `s`, `t`, `r`, `a`, `w`, `b`, `e`, `r`, `r`, `y` 열 개의 글자다. UTF-8 인코딩이라 영어에서는 글자 하나가 바이트 하나에 대응한다. 한국어라면 한 글자가 보통 *3바이트*다 — `안`은 `0xEC 0x95 0x88` 세 바이트가 모여 있는 셈이다. 이게 모든 BPE의 *진짜 출발점*이다 — 글자가 아니라 *바이트*.

이제 *말뭉치 전체*에서 가장 자주 붙어 등장하는 *바이트 쌍*을 찾는다. 영어 위키피디아를 학습 데이터로 줬다고 상상해보자. 분명 `t`와 `h`가 *엄청* 자주 붙어 등장한다 (`the`, `this`, `that`, ...). 그래서 BPE는 `t+h`를 *하나의 새로운 토큰*으로 병합한다. 이게 한 번의 *merge step*이다.

다음 단계로 가서 *새로운 어휘 위에서* 다시 가장 자주 붙어 등장하는 쌍을 찾는다. 이번엔 어쩌면 `th`+`e`가 골라진다. 그러면 `the`가 하나의 토큰이 된다. 이런 식으로 *수만 번* 반복한다. nanochat은 정확히 **32,768번 - 9번 = 32,759번**의 merge를 한다. 어휘 크기(`vocab_size`)가 32,768인데, 그중 9개는 특수 토큰 자리이므로 빼준다. 어휘는 256개의 *모든 바이트*에서 출발해 32,759번의 병합을 거쳐 완성된다.

한 가지 작은 *시뮬레이션*으로 더 또렷이 그려보자. 학습 데이터가 단 *세 문장*이라고 *가정해보자*.

```
"the cat sat"
"the cat ate"
"a cat ran"
```

처음에 BPE는 모든 글자를 *바이트 토큰*으로 본다 — `t`, `h`, `e`, ` `, `c`, `a`, `t`, …. 빈도를 세보자. 가장 많이 *붙어* 나오는 쌍은? `t`+`h`다 (`the`가 두 번 등장). 첫 merge로 `th`라는 새 토큰을 만든다. 다음 라운드에서는 `th`+`e`가 *그 다음으로 흔하다*. 두 번째 merge로 `the`가 한 토큰이 된다. *세 글자가 한 칸*에 들어간다. 그 다음은 ` `+`c`+`a`+`t`이 모여서 ` cat`(앞에 공백 포함)이 한 토큰이 된다. 학습이 끝나면 어휘에는 ` cat`이 *통째로* 하나의 토큰으로 자리잡는다.

이 작은 예시에서 *어휘의 정체*가 드러난다. **어휘는 *말뭉치의 통계*다.** 그 말뭉치에서 *자주 같이 등장한 바이트들*이 *한 칸*을 차지하고, *드물게 등장한 조합*은 *여러 칸*으로 흩어진다. 어느 토크나이저가 *어떤 텍스트*에 *효율적*인지가 *학습 시점에 본 데이터*에 의해 거의 *결정*된다.

자, `strawberry`로 돌아가 보자. *충분히 학습된* BPE 토크나이저가 영어 텍스트로 학습됐다면 어떤 일이 일어날까? `straw`라는 *흔한 단어*가 통째로 한 토큰일 가능성이 높다. `berry`도 흔하니 한 토큰일 가능성이 높다. 그러면 `strawberry`는 모델 눈에 *두 덩어리*다 — `["straw", "berry"]`.

실제 GPT-4의 `cl100k_base`로 측정해보면 `strawberry`는 **2 토큰**으로 잘린다 — `"str"`+`"awberry"`로 나오기도 하고 `"straw"`+`"berry"`로 나오기도 한다(엄밀한 분할은 학습 코퍼스에 따라 다르다). 분명한 건 *글자 수만큼 토큰*이 *아니라는 사실*이다. 그리고 `strawberry`가 *영어*에서 *상당히 흔한 단어*임에도 불구하고 *한 토큰*에는 못 들어간다는 점도 흥미롭다. 학습 데이터에 `strawberry`가 *압도적으로 빈번*한 게 아니었기 때문이다.

이게 *왜* `count('r')`을 어렵게 만드는지 다시 들여다보자. 모델은 `straw`라는 토큰을 받았을 때 *내부적으로* "아, 이 토큰은 *글자 r을 1개 포함하는* 토큰이군"이라고 *명시적으로* 알지 못한다. 토큰은 그저 *어떤 임베딩 벡터*다. 그 벡터 안에 "r 1개" 같은 정보가 *어딘가* 인코딩돼 있을 수는 있지만, *직접 셀 수 있는 형태*는 아니다. 인간이 `straw`라는 단어를 손가락으로 짚으며 `s-t-r-a-w` 다섯 글자를 *분리해서* 보는 것과는 완전히 다른 풍경이다.

여기서 *책의 첫 aha*가 온다. **토크나이저는 모델의 시각 그 자체다.** 모델이 *무엇을 잘하고 무엇을 못하는지*가, 모델의 *지능*이 아니라 토크나이저의 *경계 짓기*에서 결정되는 경우가 *놀라울 만큼 많다*. `count('r')`은 그 빙산의 일각이다. 산수, 코드 들여쓰기, 그리고 — 곧 살펴보겠지만 — **한국어 처리 비용**까지, 모두 토크나이저의 *시각*이 빚어내는 결과다.

그러니 카르파시가 nanochat에서 *제일 먼저* 작성한 코드가 `tokenizer.py`라는 사실은 우연이 아니다. 모델의 시각을 정해두지 않으면 *그 다음 한 줄*도 짤 수 없기 때문이다.

> **BPE의 짧은 족보**
>
> BPE는 사실 *언어 모델용*으로 발명된 알고리즘이 아니다. 원래 1994년 Philip Gage가 *데이터 압축 알고리즘*으로 발표했다. *바이트 쌍을 병합해 사전을 만든다*는 발상 자체는 *압축*에서 왔다. 그 발상을 *기계 번역*에 처음 가져온 게 Sennrich, Haddow, Birch의 2016년 논문 ["Neural Machine Translation of Rare Words with Subword Units"](https://arxiv.org/abs/1508.07909)다. 단어 단위 번역의 *OOV(out-of-vocabulary) 문제*를 *서브워드 단위*로 해결했다. 이후 GPT-2(2019)가 *byte-level BPE*를 LLM에 도입했고, 이게 GPT-3/4까지 거의 그대로 이어진다. nanochat이 쓰는 BPE는 *그 가계의 직계 후손*이다. 자세한 역사는 부록 C의 참고문헌 절에 정리해뒀다.

---

## 2.2 GPT-4 정규식 SPLIT_PATTERN — 왜 글자 그대로 자르지 않는가

BPE 알고리즘이 *바이트 단위 출발*이라고 했는데, 실은 *완전한 바이트 자유주의*는 아니다. 그러면 `Hello world`를 학습할 때 `o `(o + 공백) 같은 *기괴한 토큰*이 만들어질 수 있기 때문이다. `o`라는 글자가 단어 끝에서 공백과 함께 자주 등장하니까. 이렇게 *단어 경계를 넘어서* 토큰을 만들면 어휘가 *지저분해진다*. 토크나이저가 보는 세상이 *너저분*하면 그 위에서 학습되는 모델도 같이 어지러워진다.

그래서 거의 모든 현대 BPE는 *사전 분할(pretokenization)*이라는 단계를 둔다. *정규식 한 줄*로 텍스트를 *대충 의미 있는 덩어리*로 자른 다음, 그 *덩어리 안에서만* BPE 병합을 한다. 단어 경계를 넘는 무리한 병합이 일어나지 않게 막는 *울타리*다.

nanochat의 사전 분할 정규식을 직접 펴보자.

```python
# tokenizer.py:27-30
# NOTE: this split pattern deviates from GPT-4 in that we use \p{N}{1,2} instead of \p{N}{1,3}
# I did this because I didn't want to "waste" too many tokens on numbers for smaller vocab sizes.
# I verified that 2 is the sweet spot for vocab size of 32K. 1 is a bit worse, 3 was worse still.
SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,2}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""
```

이 정규식이 무엇을 하는지 *한 토막씩* 살펴보자. 정규식이 익숙하지 않아도 괜찮다. 알아둬야 하는 *결정*은 두세 개다.

| 토막 | 의미 |
|---|---|
| `'(?i:[sdmt]\|ll\|ve\|re)` | 영어 축약형(`'s`, `'d`, `'m`, `'t`, `'ll`, `'ve`, `'re`)을 *별도 덩어리*로 |
| `[^\r\n\p{L}\p{N}]?+\p{L}+` | 글자(letter) 덩어리 — 앞에 *글자가 아닌 한 글자*(공백 등)가 붙을 수 있음 |
| **`\p{N}{1,2}`** | **숫자(number)는 *최대 2자리*로 끊는다** ← 이게 GPT-4와의 *유일한 차이* |
| ` ?[^\s\p{L}\p{N}]++[\r\n]*` | 기호(`,`, `.`, `?` 등) 덩어리 |
| `\s*[\r\n]\|\s+(?!\S)\|\s+` | 공백·개행 처리 |

여기서 *책의 두 번째 작은 aha*가 온다. **`\p{N}{1,3}`를 `\p{N}{1,2}`로 바꿔치기한 한 글자의 차이.** GPT-4의 `cl100k_base` 토크나이저는 숫자를 *최대 3자리*까지 한 토큰으로 묶는다. `1234`라면 `123`+`4` 두 토큰. 어휘가 100K나 되니까 `123`, `124`, …, `999`처럼 3자리 숫자들에 *각자 자기 토큰*을 사치스럽게 줄 여력이 있다.

그런데 nanochat은 어휘가 32K밖에 안 된다. *3분의 1 크기*다. 만약 3자리를 다 토큰으로 받으면 100`~`999 사이의 *900개 숫자*에 토큰을 잠재적으로 낭비하게 된다. 그래서 한 글자를 줄여 *2자리*로 끊는다. `1234`는 `12`+`34`로, 4토큰이 아니라 2토큰이지만, 어쨌든 GPT-4와는 다른 *2자리 단위 시각*으로 숫자를 본다.

카르파시 본인의 주석이 정말 정직하다 — *"I didn't want to 'waste' too many tokens on numbers for smaller vocab sizes. I verified that 2 is the sweet spot for vocab size of 32K. 1 is a bit worse, 3 was worse still."* 무려 *직접 실험해서 sweet spot을 찾았다*는 한 줄. 이런 결정이 nanochat 전체에 깔려 있다. 카르파시는 *디폴트를 그대로 가져오지 않고* 자기 모델 크기에 맞게 *재실험해서* 결정한다. 우리도 자기 모델을 만든다면 이 자세를 따라하는 편이 낫다.

이 *한 글자의 차이*가 *실전*에서 어떤 그림을 만드는지 잠시 더 들여다보자. 학습 데이터의 숫자 패턴이 *어떻게* 분포돼 있는지에 따라 결과가 달라진다.

- *연도*가 자주 등장하는 텍스트라면 — `2024`, `2025`, `1999` — GPT-4의 `\p{N}{1,3}`은 `2024`를 `202`+`4`로 분할한다. nanochat의 `\p{N}{1,2}`은 `20`+`24`로 분할한다. *둘 다 2토큰*이다. 차이가 거의 없다.
- *큰 수*가 등장한다면 — `1234567` — GPT-4는 `123`+`456`+`7` 세 토큰. nanochat은 `12`+`34`+`56`+`7` *네 토큰*. nanochat이 *살짝 더 비싸다*.
- *작은 수*가 자주 등장한다면 — `1`, `5`, `42` — *둘 다 한두 토큰*. 차이 없음.

종합하면 nanochat의 *2자리 끊기*는 *큰 수에서 약간 손해*지만 *어휘 절약 효과는 분명*하다 — 100`~`999 사이 900개 후보 토큰을 만들 *기회 자체를 차단*하니까. 32K 어휘에서는 *그 절약*이 *큰 수 처리의 작은 손해*보다 *이득*이라고 카르파시가 *실험으로* 결정했다. 그 이득의 정확한 모양은 3장의 `tok_eval` 결과로 다시 확인하자.

> **잠시 멈추고 생각해보자.** 디폴트 한 글자를 *직접 바꾼다*는 결정의 *비용*은 무엇일까? 카르파시는 그저 *주석으로* 자기 결정을 남겼고, 정규식을 *한 글자* 바꿨다. 그게 끝이다. *코드의 비용*은 0에 가깝다. 그런데 *결정의 비용*은 컸을 수 있다 — *직접 학습을 돌려보고, `tok_eval`을 비교하고, 다시 한 번 학습을 돌리는* 반복. 좋은 코드는 *변경의 비용이 작다*. 그 위에서 *결정자*가 자유롭게 *실험*할 수 있다. nanochat이 *8천 줄*에 머무는 이유는, 이런 *작고 명확한 결정점*들이 *층층이 쌓여 있기* 때문이다.

> **잠깐, `\p{L}`과 `\p{N}`은 무엇인가**
>
> 이건 *Unicode property* 표기다. `\p{L}`은 *임의의 글자(Letter)* — 영어 알파벳뿐 아니라 한글, 한자, 일본어 가나, 아랍어, 키릴 문자 *전부*를 포함한다. `\p{N}`은 *임의의 숫자(Number)*. 이 정규식이 한국어를 *통째로 한 덩어리*로 잘 잡아주는 이유가 여기에 있다 — `\p{L}+`가 `안녕하세요`를 *한 덩어리*로 본다. 그 덩어리 *안에서* BPE 병합이 어떻게 일어나느냐는 또 다른 이야기지만, 적어도 사전 분할 단계에서는 한국어가 *영어와 동등하게* 다뤄진다.

이 정규식 위에서 BPE 학습이 일어난다. 즉, *덩어리 단위*로 문자열을 분리한 뒤, *각 덩어리 안에서만* 가장 빈번한 바이트 쌍 병합을 반복한다. 단어 경계가 깨지지 않는다. 깔끔하다.

---

## 2.3 9개의 SPECIAL_TOKENS — 토크나이저 단에 박힌 *도구 호출*

이제 *진짜로 결정적인* 코드 한 토막을 펴보자. `tokenizer.py`의 *맨 위쪽*, 13번부터 25번 라인이다.

```python
# tokenizer.py:13-25
SPECIAL_TOKENS = [
    # every document begins with the Beginning of Sequence (BOS) token that delimits documents
    "<|bos|>",
    # tokens below are only used during finetuning to render Conversations into token ids
    "<|user_start|>", # user messages
    "<|user_end|>",
    "<|assistant_start|>", # assistant messages
    "<|assistant_end|>",
    "<|python_start|>", # assistant invokes python REPL tool
    "<|python_end|>",
    "<|output_start|>", # python REPL outputs back to assistant
    "<|output_end|>",
]
```

9개의 *특수 토큰*이 *토크나이저 단에* 박혀 있다. 잠깐 멈추고 이 *결정의 무게*를 같이 음미해보자.

평범한 텍스트라면 이 9개는 그냥 *문자열*이다. `<|bos|>`라는 글자가 적힌 단어다. 그런데 BPE 학습 *시작 전*에 이 9개를 *어휘에 통째로 등록*하면, 토크나이저는 이 문자열들을 *분해하지 않고* — 한 토큰으로 — 본다. 32,759개의 일반 토큰 + 9개의 특수 토큰 = **총 32,768개의 어휘**가 그렇게 완성된다. (어휘 크기가 2의 15제곱이라는 *깔끔한 숫자*인 건 우연이 아니다 — `lm_head` 같은 matmul이 SIMD 친화적이 되도록 한 선택이다. 6장에서 다시 다룬다.)

이 9개가 무엇을 *대표*하는지 한 줄씩 읽어보자.

- `<|bos|>` — 문서의 시작. 사전학습 단계에서 모든 문서 앞에 *반드시* 붙는다.
- `<|user_start|>` / `<|user_end|>` — 사용자의 말 한 묶음을 *감싸는* 토큰 쌍.
- `<|assistant_start|>` / `<|assistant_end|>` — 어시스턴트(즉, 우리 모델)의 답 한 묶음을 감싸는 쌍.
- `<|python_start|>` / `<|python_end|>` — 어시스턴트가 *파이썬 도구를 호출*할 때 코드를 감싸는 쌍.
- `<|output_start|>` / `<|output_end|>` — 파이썬 *실행 결과*를 어시스턴트에게 *돌려줄* 때 감싸는 쌍.

위쪽 5개는 *대화 구조*를 위한 토큰이다. 어시스턴트가 어디서 말을 시작하고 어디서 끝내는지를 *모델 자신*이 알아야 하므로, 이 토큰들이 SFT 단계에서 *학습된다*. 그런데 *아래쪽 4개*가 흥미롭다. **`<|python_start|>` 부터 `<|output_end|>` 까지가 모델의 *도구 호출(tool use)*을 *원시 시각으로* 가능하게 만든다.** 모델이 "이 시점에서 파이썬을 호출하고 싶다"는 욕망을 *외부 함수*가 아니라 *자기 토큰 출력*만으로 표현할 수 있다는 뜻이다.

이 결정은 굉장히 *무겁다*. 왜냐하면 토크나이저는 **사전학습보다 *먼저* 정해진다**. 한 번 정해두면 32,768개 어휘 안의 *어느 자리*에 어떤 의미가 박혀 있는지가 *모든 후속 단계*에 고정된다. 만약 nanochat을 *다 학습한 다음*에 *새로운 도구*를 추가하고 싶다면? *토크나이저 어휘를 늘려야* 한다. 그러면 `lm_head`의 출력 차원이 달라지고, 임베딩 테이블의 행 수가 달라지고, *그 위에서 학습된 가중치*는 그 새로운 어휘를 본 적이 *전혀 없다*. 사실상 *다시 처음부터* 학습하거나, *어딘가에 토큰을 끼워넣는* 위태로운 surgery를 해야 한다. 어느 쪽이든 *찜찜하다*.

> **잊지 말자**: 토크나이저는 모델보다 *먼저* 정해진다. 그리고 *나중에 바꾸기가 정말 어렵다*. 도구 사용을 *나중에 끼워넣고 싶었다*면 더 비싼 대가를 치른다. 카르파시는 nanochat을 시작하는 *바로 그 첫 파일*에서 4쌍의 도구 호출 토큰을 미리 박아뒀다. 이게 10장에서 우리가 `9 곱하기 8은?`이라는 질문에 모델이 *스스로 파이썬을 호출해서 72를 답하는 광경*을 볼 수 있는 *유일한 이유*다.

**조금 더 깊이 — 9개의 결정이 *모델의 미래*를 어떻게 좁히는가**

`<|user_start|>` 같은 *형식*도 *결정*이다. 다른 모델들은 어떻게 할까?

- **Llama 3**는 `<|start_header_id|>user<|end_header_id|>`라는 *두 토큰* 사이에 *문자열로 역할*을 박는다.
- **Qwen**은 `<|im_start|>user\n` 같은 *ChatML 스타일*을 쓴다.
- **OpenAI** GPT-4 (API)는 *전용 토큰* 없이 *내부에서* 변환된 토큰을 쓴다 (정확한 형식은 공개되지 않았다).

각각의 결정이 *장단점*을 갖는다. *문자열로 역할 박기*(Llama 식)는 *역할이 추가*돼도 어휘를 안 늘리고 된다 — `<|start_header_id|>system<|end_header_id|>`처럼 *내용물*만 바꾸면 그만이다. *전용 토큰 쌍*(nanochat 식)은 *역할이 고정*되지만 *디코딩이 명확*하다. `<|user_start|>`라는 단일 토큰 ID 하나가 *문맥에 흔들리지 않는 명확한 신호*가 된다.

nanochat은 *전용 토큰 쌍*을 골랐다. *작은 모델*에서 *명확한 신호*가 *학습을 안정화*시킨다고 봤기 때문이다. 어휘를 9개 *희생*하는 대신 *깨끗한 학습*을 얻는다. 결정은 트레이드오프지만, 이 트레이드오프가 *왜 이렇게 풀렸는지*는 *모델 크기*와 *목적*에 따라 다르다. 우리가 자기 모델을 만든다면 *이 9개를 그대로 베껴오지 않고* 자기 도구 모양에 맞게 *재설계해도 좋다*. 단, *모든 후속 단계*가 이 어휘 위에 쌓인다는 사실은 *잊지 말자*.

조금 더 깊이 들어가보자. 토큰 ID는 *어떻게* 결정될까? 코드를 다시 펴자.

```python
# tokenizer.py:182-189
tokens_offset = len(mergeable_ranks)
special_tokens = {name: tokens_offset + i for i, name in enumerate(SPECIAL_TOKENS)}
enc = tiktoken.Encoding(
    name="rustbpe",
    pat_str=pattern,
    mergeable_ranks=mergeable_ranks,
    special_tokens=special_tokens,
)
```

일반 BPE 토큰이 0부터 32,758까지 차례로 ID를 받는다. 그 *바로 뒤*에 특수 토큰이 32,759부터 32,767까지 *연속 9칸*을 차지한다. 깔끔하다. 어휘 안에서 *특수 토큰이 어디 있는지*가 *어휘 끝의 9칸*으로 *예측 가능하게* 박혀 있다. 모델이 *임베딩 테이블*을 읽을 때도, *softmax를 통해 다음 토큰을 고를 때*도, 이 9칸은 *연속된 영역*에 모여 있다.

이건 *우연이 아니다*. 어휘 구조에 *질서*를 두는 것이, 곧 그 위에서 학습되는 모델의 *예측 표면*에도 질서를 새기는 일이기 때문이다.

---

## 2.4 두 구현 — rustbpe로 학습하고, tiktoken으로 추론한다

nanochat의 `tokenizer.py`를 펴면 *두 개의 토크나이저 클래스*가 나란히 들어 있다. 잠시 의아할 수 있다. 왜 *두 개*인가? 하나면 안 되나?

```python
# tokenizer.py:1-7 (docstring)
"""
BPE Tokenizer in the style of GPT-4.

Two implementations are available:
1) HuggingFace Tokenizer that can do both training and inference but is really confusing
2) Our own RustBPE Tokenizer for training and tiktoken for efficient inference
"""
```

카르파시 본인이 *솔직하다* — *"really confusing"*. HuggingFace의 `tokenizers` 라이브러리는 *학습과 추론을 한 번에* 해주는데, 코드 베이스가 거대하고, 학습 코드의 *어떤 동작*이 추론에 *어떤 결과*를 만들지가 한눈에 *안 들어온다*. *학습용 코드가 추론용 코드와 분리되지 않으면* 디버깅이 정말 *번거롭다*.

그래서 카르파시는 두 도구를 *나눈다*. **학습은 rustbpe로**, **추론은 tiktoken으로**. rustbpe는 카르파시가 직접 쓴 *Rust* 구현체다 (`rustbpe/` 디렉토리에 있고, 한 파일이 100줄 남짓). 학습용으로만 쓰니까 *작고 명확*하다. 추론은 OpenAI가 만든 *tiktoken* — 이건 GPT-3/3.5/4가 실제로 *프로덕션에서* 쓰는 토크나이저고, C++로 짠 백엔드라 *번개처럼 빠르다*.

핵심 흐름을 코드로 한번 들여다보자. `RustBPETokenizer.train_from_iterator`다.

```python
# tokenizer.py:170-190
@classmethod
def train_from_iterator(cls, text_iterator, vocab_size):
    # 1) train using rustbpe
    tokenizer = rustbpe.Tokenizer()
    vocab_size_no_special = vocab_size - len(SPECIAL_TOKENS)
    assert vocab_size_no_special >= 256
    tokenizer.train_from_iterator(text_iterator, vocab_size_no_special, pattern=SPLIT_PATTERN)
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

흐름이 *깔끔*하다. (1) rustbpe로 학습한다. 결과물은 `mergeable_ranks` — *바이트 시퀀스 → 병합 우선순위 정수*의 dict다. 이게 BPE 학습의 *최종 산출물*이다. (2) 이 dict를 그대로 `tiktoken.Encoding`에 *심어준다*. tiktoken은 학습은 할 줄 모르지만 *이미 학습된 어휘*를 받아서 *기가 막히게 빠른 encode/decode*를 해준다.

여기서 *함께 기억해두자*. **BPE 학습의 산출물은 결국 *바이트열 → 우선순위 정수*라는 한 장의 표다.** 모델이 아니다, 가중치도 아니다. 그저 *바이트열 사전*이다. 그 사전이 *언어를 어떻게 보는지*를 결정한다. 코드 한 줄로 *학습 백엔드*와 *추론 백엔드*를 분리할 수 있는 이유도, 사전이 그렇게 *심플한 자료구조*이기 때문이다.

> **카르파시 식 분리의 미덕**
>
> 학습은 *오프라인*에서 *한 번*만 일어난다. 그러니 학습 코드는 *명확*하면 그만이다 — 느려도 된다 (어차피 2B chars 학습이 30분이면 끝난다). 반면 추론은 *매 토큰마다* 일어난다. 그러니 빨라야 한다. 같은 도구로 둘 다 하려고 들면 *어느 한쪽이 타협*당한다. **다른 단계에는 다른 도구**라는 결정이 nanochat 곳곳에 반복된다. 학습 옵티마이저(AdamW+Muon)와 추론 엔진(Engine+KV cache)도 *완전히 다른 모듈*이다. 토크나이저는 그 패턴의 *첫 사례*다.

이왕 펴본 김에 `RustBPETokenizer`의 *나머지 메서드*들도 *짧게* 훑고 가자. 어렵지 않다.

```python
# tokenizer.py:209-220 (간단한 메서드들)
def get_vocab_size(self):
    return self.enc.n_vocab

def get_special_tokens(self):
    return self.enc.special_tokens_set

def id_to_token(self, id):
    return self.enc.decode([id])

@lru_cache(maxsize=32)
def encode_special(self, text):
    return self.enc.encode_single_token(text)
```

`get_vocab_size`, `get_special_tokens`, `id_to_token`은 *그대로 읽히는* 헬퍼다. 흥미로운 건 `encode_special` 위의 `@lru_cache(maxsize=32)` 데코레이터다. *특수 토큰을 자주 인코딩하는 상황*(예: `render_conversation`이 *매 대화마다* `<|user_start|>` 같은 특수 토큰을 인코딩한다)에서 *불필요한 반복 계산*을 피하는 *작은 캐시*다. 9개 특수 토큰을 *모두 캐시할 수 있는 충분한 크기*인 32를 골랐다. *작은 디테일이지만, 이런 캐시들이 모여 학습 속도를 만든다*.

본격적인 `encode` 메서드를 *조금만 더* 살펴보자.

```python
# tokenizer.py:225-250 (encode 메서드 발췌)
def encode(self, text, prepend=None, append=None, num_threads=8):
    if prepend is not None:
        prepend_id = prepend if isinstance(prepend, int) else self.encode_special(prepend)
    if append is not None:
        append_id = append if isinstance(append, int) else self.encode_special(append)

    if isinstance(text, str):
        ids = self.enc.encode_ordinary(text)
        if prepend is not None:
            ids.insert(0, prepend_id)
        if append is not None:
            ids.append(append_id)
    elif isinstance(text, list):
        ids = self.enc.encode_ordinary_batch(text, num_threads=num_threads)
        ...
```

세 가지를 메모해두자.

- **`encode_ordinary`** — *특수 토큰을 무시하고* 일반 텍스트만 인코딩하는 tiktoken의 메서드. 사용자 입력에 `<|bos|>` 같은 문자열이 *우연히* 포함돼도 *그저 텍스트*로 처리한다. 보안적으로도 안전하다.
- **`prepend`/`append` 인자** — 토큰 ID나 특수 토큰 이름을 받아 *앞뒤로 한 토큰 붙이기*. 사전학습 데이터를 흘릴 때 *각 문서 앞에 `<|bos|>`를 prepend*하는 흔한 패턴을 *한 줄*로 처리한다.
- **`num_threads=8`** — 리스트를 받으면 *여러 스레드*로 *병렬 인코딩*. 학습 데이터 셰드 전체를 토큰화할 때 *빠르다*.

쉽고 명확한 API다. 카르파시는 *외부에서 보기 단순*하면서 *내부적으로 빠른* 인터페이스를 *반복적으로* 만든다. 이 패턴도 *기억해두자*.

---

## 2.5 같은 한국어 문장의 세 토크나이저 비교 — *책의 첫 aha*

이제 이 책의 *첫 번째 큰 충격*을 같이 맞아보자. 같은 한국어 문장을 세 가지 다른 토크나이저로 인코딩해보면 *어떤 일*이 벌어질까?

예시 문장은 *한국어 인사 한 줄*로 고정한다.

> **"안녕하세요, 저는 토비입니다."**

영어로 옮기면 *"Hello, I am Toby."* — 정확히 18글자(공백 제외 15글자)다. 영어 토크나이저라면 GPT-2든 GPT-4든 *5~6 토큰* 정도로 자른다. 그런데 한국어로 *같은 의미*를 표현하면 어떻게 될까? 세 가지 토크나이저로 토큰화해보자.

> **세 토크나이저의 인코딩 비교 표**
>
> | 토크나이저 | vocab 크기 | 토큰 수 | 분할 예시(앞 5개) | bytes/token |
> |---|---|---|---|---|
> | **GPT-2** (`tiktoken: gpt2`) | 50,257 | **약 18** | `ìķ`, `Ī`, `ëħķ`, `íķĺ`, `ìĦ¸` | 약 **2.0** |
> | **GPT-4 `cl100k_base`** | 100,277 | **약 8** | `안`, `녕`, `하세요`, `,`, ` 저` | 약 **4.5** |
> | **nanochat 32K** (FineWeb 학습) | 32,768 | **약 22** | byte-level fallback에 가까움 | 약 **1.7** |
>
> *(수치는 책 본문 작성 시점의 측정 *방향*. 정확한 값은 챕터 끝 실습에서 직접 재현한다.)*

여기서 잠깐 표를 *느껴*보자. 같은 *한국어 한 줄*이 어떤 토크나이저에서는 *8토큰*, 어떤 토크나이저에서는 *22토큰*이다. **거의 3배 차이.**

이 차이가 *무엇을 의미*하는지 풀어보자. 토큰 수는 다음 세 가지를 *직접 결정*한다.

1. **추론 비용** — API 사용 시 *토큰당 과금*이 일반적이다. GPT-4로 한국어 1만 자를 처리하는 비용은 GPT-4로 영어 1만 자를 처리하는 비용보다 *몇 배 비싸다*. 같은 의미, 다른 가격. 부조리하게 들리지만 *수학적 사실*이다.
2. **컨텍스트 한도** — 모델이 한 번에 볼 수 있는 *토큰 수*는 정해져 있다 (nanochat은 기본 2,048). 한국어로 같은 양의 정보를 넣으면 *영어보다 빨리 한도에 닿는다*. 영어 책 한 권은 통째로 들어가는데 한국어 책은 *반*만 들어가는 일이 *진짜로* 벌어진다.
3. **학습 비용** — 같은 *bytes/token* 효율의 모델이라도 한국어로 학습하려면 *더 많은 토큰*을 처리해야 한다. 같은 GPU 시간으로 *덜 학습된다*.

조금 더 *구체적으로* 와닿게 해보자. 어떤 한국 회사가 *고객 응대용 LLM*을 GPT-4로 운영한다고 가정해보자. 한 달에 *1억 자*의 한국어 텍스트를 처리한다. 같은 양의 *영어 텍스트*를 처리한다고 가정하면 어떤 차이가 날까?

- 영어 1억 자 → 약 *2.5억 바이트* → GPT-4로 *약 4,000만 토큰* (bytes/token ≈ 6.0).
- 한국어 1억 자 → 약 *3억 바이트* → GPT-4로 *약 7,500만 토큰* (bytes/token ≈ 4.0).

한국어가 *영어보다 약 1.9배의 토큰*을 잡아먹는 셈이다. *같은 의미*의 텍스트를 *두 배 가까운 비용*으로 처리한다. 같은 회사가 *영어로만* 운영한다면 한 달 비용이 *절반*에 가깝다. 이 *부조리한 격차*가 *토크나이저 한 줄*에서 나온다.

그런데 이 격차는 *언제 결정*됐는가? GPT-4가 출시되기 *훨씬 전*, 토크나이저가 학습되던 *그 시점*에 이미 결정됐다. 그 후 토크나이저는 *바꿀 수 없다* — 어휘를 바꾸면 *모든 가중치*가 *쓸모없어지기* 때문이다. 한 번 박힌 *시각*은 *모델의 평생*을 따라간다. 이게 *시각의 무게*다.

자, 그렇다면 *왜* 이런 차이가 나는가? 답은 *허무할 만큼 단순*하다. **세 토크나이저의 *학습 데이터 분포*가 달랐을 뿐**이다.

GPT-2는 2019년에 Reddit·웹크롤 데이터로 학습됐다. 영어가 *압도적*이고 한국어 비중은 *눈에 띄지도 않을* 정도였다. 그러니 한국어 같은 문자열은 BPE 학습 과정에서 *바이트 쌍 병합 우선순위가 한참 뒤로 밀린다*. 결과적으로 `안녕`이라는 한 단어조차 *통째로 한 토큰*으로 묶이지 못하고, *UTF-8 바이트 단위*로 잘려나간다. 표에 보이는 `ìķ`, `Ī` 같은 *읽을 수 없는 글자들*이 그 결과다. 그 정체는 *깨진 문자*가 아니라, 한국어 `안`의 UTF-8 *세 바이트*가 *Latin-1*로 잘못 해석된 *바이트들의 그림자*다. GPT-2의 토크나이저 입장에서 한국어 한 글자는 *알 수 없는 외계어*이고, 그래서 *바이트 단위로 흘러내린다*.

GPT-4의 `cl100k_base`는 다르다. OpenAI는 GPT-3.5/4를 만들 때 *세계의 언어들*을 더 많이 본 데이터로 토크나이저를 학습했다. 그 결과 `안`, `녕`, `하세요` 같은 *한국어 단위*가 어휘에 직접 *자리를 얻었다*. 그래서 `"안녕하세요"`가 한 줄에 *3토큰*으로 깔끔히 들어간다. 어휘가 100K로 *두 배*이기도 하고, *한국어 비중*이 학습 데이터에 *훨씬 컸기* 때문이기도 하다.

그렇다면 *nanochat 32K*는? *어떻게 GPT-2(50K)보다도 토큰 수가 많을* 수 있을까? 이게 사실 *조금 충격적*이다. nanochat의 토크나이저는 **FineWeb으로 학습된다.** FineWeb은 *영어 위주의* 고품질 웹 코퍼스다. 한국어 텍스트는 *거의 들어 있지 않다*. 그래서 nanochat 토크나이저는 한국어를 학습할 *기회 자체가 없었다*. 게다가 어휘는 *32K*로 GPT-2의 50K보다도 *작다*. 그러니 한국어 같은 비영어 텍스트는 *byte-level fallback*에 가까운 처리를 받는다 — *바이트 단위로 토큰화*되고, 한국어 한 글자가 *2~3 토큰*을 잡아먹는다.

이게 **한국어가 모든 토크나이저에서 *비싸지는* 이유**다. *데이터 분포의 직접적 결과*다. 토크나이저가 한국어를 *덜 본 만큼* 한국어를 *덜 효율적으로* 본다. 모델이 *지능적*이라서 그러는 게 아니라, 시각의 *훈련 분포*가 그렇게 형성됐을 뿐이다.

**한국어 한 글자를 *바이트 수준*에서 뜯어보자.** 이 *해부*가 *왜 한국어가 byte-level fallback에 가까운가*를 *눈으로* 보여준다.

`안`이라는 글자 하나는 UTF-8로 *세 바이트*다 — `0xEC 0x95 0x88`. *0xEC*는 *유니코드 U+AC00–U+ACFF 영역의 시작 바이트*를 뜻한다. 한글 음절(Hangul Syllables) 블록은 *U+AC00 ~ U+D7A3*에 통째로 박혀 있고, 이 모든 글자가 *0xEA, 0xEB, 0xEC, 0xED* 네 *시작 바이트*로 시작한다. 즉 *수만 글자*가 *네 시작 바이트* 뒤에 *균등하게 분산*돼 있는 셈이다.

이게 *어떤 의미*인지 천천히 보자.

- 영어에서 *알파벳 a*는 *항상 0x61* 한 바이트다. BPE 학습에서 `a`+`n`이 *압도적으로* 자주 등장한다 (수억 번). 따라서 `an`은 *매우 일찍* merge된다.
- 한국어에서 *0xEC*라는 시작 바이트 뒤에는 *수많은 한국어 음절*이 따라온다 — `0xEC 0x95 0x88`(안), `0xEC 0x95 0x84`(아), `0xEC 0x95 0x88` 같은 *수많은 후속 바이트 패턴*. *각각의 패턴*은 *영어 알파벳보다 훨씬 드물게* 등장한다. 그러니 *어떤 한국어 음절도* `the`+`an`처럼 *압도적 빈도*를 누리지 못한다.

그 결과, FineWeb 같은 *영어 위주 코퍼스*에서 학습된 BPE는 한국어 음절을 *통째로 잡아주는 토큰*을 *거의 안 만든다*. 256개의 *기초 바이트 토큰* 위에 *영어 토큰*만 수만 개 쌓이고, *한국어 음절은 그 영어 토큰들이 다 자리잡은 뒤에 남은 자리에서 — *바이트 수준 fallback*으로 — 토큰화된다. 한국어 한 글자가 *2~3 토큰*을 잡아먹는 이유다.

> **byte-level fallback이라는 안전망**
>
> 한 가지 *다행스러운* 점이 있다. 현대 BPE는 *byte-level*이다 (GPT-2 이후 표준). 즉, *어떤 바이트 시퀀스라도 토큰화는 *반드시 가능*하다*. 어휘에 *통째로 잡아주는 토큰이 없어도* 바이트 단위로 *흩어 잘라서라도* 표현은 된다. 한글이든 한자든 이모지든 *깨지지 않는다*. 다만 *비싸진다*. 그게 *fallback의 대가*다.
>
> 비교: 한국어 NLP의 옛 시대에는 토크나이저가 *깨지면* 문장 자체가 *증발*하는 *재앙*이 일어났다. 그 시절에 비하면 *byte-level fallback*은 *대단한 안전망*이다. 한국어를 *덜 효율적으로 본다*는 비싼 가격을 치르되, *모든 한국어를 다 표현할 수 있다*는 *최소한의 약속*은 지켜진다.

그렇다면 — 책 후반부의 *복선*으로 — 한 가지 의문이 자연스럽게 따라온다. **우리가 *한국어 텍스트*로 nanochat 토크나이저를 *다시 학습*시키면 어떻게 될까?** 답은 12장 마지막 절과 부록 D에서 만난다. 지금은 *aha의 충격*만 갖고 가자. **모국어가 *비싸진 이유*는 모델의 무관심이 아니라, *우리가 학습 데이터에서 빠져 있었기* 때문이다.** 

---

## 2.6 잠깐, *왜 vocab은 32K인가* — 세 힘의 균형

여기서 한 가지 묻고 갈 만한 질문이 있다. **`vocab_size`는 왜 *32,768*인가?** 더 작아도, 더 커도 안 됐을까?

`vocab_size`는 *세 개의 힘*이 동시에 잡아당기는 *균형점*이다. 함께 살펴보자.

**첫 번째 힘 — *압축 효율 (compression)*.** 어휘가 크면 *같은 텍스트*가 *더 적은 토큰*에 들어간다. 같은 문맥 길이로 *더 많은 정보*를 모델에게 보여줄 수 있다. 이쪽 힘은 *어휘를 키우라*고 잡아당긴다. GPT-4가 어휘를 100K로 키운 이유다.

**두 번째 힘 — *`lm_head` 파라미터 비용*.** Transformer의 마지막 층은 *모든 토큰 위에 확률 분포*를 만들어야 한다. 그러려면 `lm_head`라는 *마지막 선형 층*이 (모델 차원 `n_embd`) × (어휘 크기 `vocab_size`) *행렬*을 갖는다. nanochat의 d12 모델로 *대충 계산*해보면 `n_embd=768`이고 `vocab_size=32,768`이니 `lm_head`만 `768 × 32,768 ≈ 25M` 파라미터다. 모델 전체가 약 150M이라면 *lm_head 하나가 모델의 1/6*을 차지하는 셈이다. 어휘를 100K로 키우면 `lm_head`만 *3배*로 부풀고, 모델 전체의 *절반 가까이*가 *마지막 한 층*에 묶인다. 작은 모델일수록 이 비용이 *치명적*이다. 이쪽 힘은 *어휘를 작게*하라고 잡아당긴다.

**세 번째 힘 — *cross-entropy loss의 수치적 특성*.** 어휘가 크면 softmax의 분모에 *더 많은 항*이 들어간다. 가능한 다음 토큰 후보가 *수만 개*인 상황에서 *옳은 토큰*을 골라야 하므로, *각 토큰의 확률*이 평균적으로 *낮아진다*. 학습 신호가 *희석된다*. 또한 어휘에서 *거의 등장 안 하는 토큰*이 늘어나면 — *모델이 그걸 학습할 기회가 없으면* — *학습 비용은 늘어나는데 효용은 작아진다*. 이쪽 힘도 *어휘를 작게*하라고 잡아당긴다.

세 힘이 *균형*을 이루는 자리가 *32K*다. 카르파시는 다음 *경험적 사실*들을 모두 고려했다.

- GPT-2(50K)는 *150M 모델*에서 *합리적*이었지만 *큰 모델*(1.5B+)에서는 *더 큰 어휘*가 더 효율적이었다.
- *2의 거듭제곱*이 GPU 친화적이다 — `lm_head`의 matmul이 *SIMD 단위*에 *깔끔하게 정렬*된다 (`vocab_size`가 8의 배수, 64의 배수, 128의 배수일수록 좋다). 32,768은 *2의 15제곱* — *정말 깔끔*하다.
- *150M ~ 600M* 크기의 모델 가족(speedrun d24도 이 범위 안)에서 32K가 *bpb와 wall-clock의 sweet spot*이라는 카르파시의 실험적 결론.

**잊지 말자.** 어휘 크기는 *큰 게 좋다*거나 *작은 게 좋다*가 아니다. *모델 크기와 데이터 양*에 *함께 잡아 댕겨야 하는* 다이얼이다. 우리가 d4 미니 모델을 만들려고 *어휘를 16K로 줄이면* — `lm_head`가 가벼워지고 *작은 모델에 맞는 균형*이 된다. *큰 모델*을 만들려고 *어휘를 64K로 키우면* — 압축 효율이 살아난다. 어느 쪽이든 *남이 정한 값을 그대로 베끼지 않고* 자기 균형을 잡는 편이 낫다. 3장의 `tok_eval`이 그 균형을 *측정하는 도구*다.

---

## 2.7 token_bytes.pt — bits-per-byte 평가의 *조용한 준비*

토크나이저 학습이 끝난 직후, nanochat은 *한 가지 작은 산출물*을 더 저장한다. `token_bytes.pt`라는 파일이다.

```python
# tokenizer.py:397-406
def get_token_bytes(device="cpu"):
    import torch
    from nanochat.common import get_base_dir
    base_dir = get_base_dir()
    tokenizer_dir = os.path.join(base_dir, "tokenizer")
    token_bytes_path = os.path.join(tokenizer_dir, "token_bytes.pt")
    assert os.path.exists(token_bytes_path), f"Token bytes not found at {token_bytes_path}? It gets written by tok_train.py"
    with open(token_bytes_path, "rb") as f:
        token_bytes = torch.load(f, map_location=device)
    return token_bytes
```

뭘 저장하는 걸까? *각 토큰 ID*가 UTF-8로 *몇 바이트*를 차지하는지를 *길이 32,768짜리 텐서*에 미리 적어둔 것이다. `token_bytes[i]`는 *토큰 i가 차지하는 utf-8 바이트 수*다.

왜 이걸 *학습 직후*에 만들어두는가? 사전학습 단계의 *평가*가 *bits-per-byte (bpb)* 라는 지표로 측정되기 때문이다. 7장에서 자세히 다루겠지만, *지금* 짚어두자.

크로스 엔트로피 손실(cross-entropy loss)은 *토큰 단위*다. 모델이 다음 토큰을 얼마나 *잘 맞히는지*를 *bits/token*으로 측정한다. 그런데 이 지표에는 *함정*이 있다. **vocab이 다른 두 모델의 loss를 직접 비교할 수 없다.** GPT-2(50K)와 nanochat(32K)의 loss를 같은 자에 올려놓으면 *부당한 비교*가 된다. nanochat의 토큰이 *평균적으로 더 짧기* (즉, 더 적은 바이트를 표현하기) 때문에 *같은 텍스트에 더 많은 토큰*이 들어가고, *토큰당 loss가 자연스럽게 작아진다*. *모델이 더 똑똑해서*가 아니라 *토큰이 더 짧아서*다. 끔찍한 일이다.

그래서 *언어 모델 평가의 정설*은 **bits-per-byte (bpb)**다. *바이트*는 어떤 모델에서든 똑같은 단위니까, *바이트당 비트*로 환산해 비교한다. 환산은 간단하다.

```
bpb = sum(cross_entropy_per_token * tokens_per_window) / total_bytes_in_window
```

여기서 *toekn당 바이트 수*가 필요하다. 그게 `token_bytes`다. *학습 직후* 미리 계산해두면 *학습 루프 안에서* 매 step마다 *바이트 수*를 다시 계산하지 않아도 된다. 그저 `token_bytes[ids]`로 한 번에 가져오면 된다. *최적화의 한 작은 흔적*이다.

기억해두자. **`token_bytes.pt`는 토크나이저의 *부산물*이지만, 사실은 7장 *평가의 정설*을 위해 *2장에서 미리 준비된 사다리*다.** nanochat의 모든 산출물은 *나중에 쓸 데가 있어서* 만들어진다.

---

## 2.8 render_conversation — *어시스턴트가 학습받는 토큰*의 경계

이제 토크나이저의 *진짜로 결정적인* 한 함수를 펴보자. `render_conversation`이다. 사전학습이 아니라 *SFT 단계*에서 호출되는 함수인데, 토크나이저 안에 들어 있는 이유가 따로 있다.

SFT 단계에서 *데이터*는 대화 한 쌍이다. 사용자 메시지와 어시스턴트 답변. 우리는 모델에게 *어시스턴트가 답하는 법*을 가르치려는 거지, *사용자 메시지를 따라하는 법*을 가르치려는 게 아니다. 그렇다면 *손실 함수*는 *어떤 토큰*에 대해서만 *역전파(backprop)*해야 할까?

답은 *직관적*이다. **어시스턴트의 출력 토큰에만 역전파한다.** 사용자 메시지는 *조건*일 뿐, 학습 신호가 아니다.

이걸 구현하는 게 `render_conversation`이다. 8장에서 다시 깊이 보지만, 토크나이저 챕터에서 *얼개*만 미리 펴두자.

```python
# tokenizer.py:266-279 (시그니처와 헬퍼)
def render_conversation(self, conversation, max_tokens=2048):
    """
    Tokenize a single Chat conversation (which we call a "doc" or "document" here).
    Returns:
    - ids: list[int] is a list of token ids of this rendered conversation
    - mask: list[int] of same length, mask = 1 for tokens that the Assistant is expected to train on.
    """
    ids, mask = [], []
    def add_tokens(token_ids, mask_val):
        if isinstance(token_ids, int):
            token_ids = [token_ids]
        ids.extend(token_ids)
        mask.extend([mask_val] * len(token_ids))
```

`ids`와 `mask` *두 리스트를 함께* 만든다. `mask=1`은 *"이 토큰은 어시스턴트가 학습받을 토큰"*이고, `mask=0`은 *"이 토큰은 그저 조건일 뿐 학습 안 받음"*이다. 그러면 *각 역할*의 메시지를 어떻게 처리하는지 보자.

```python
# tokenizer.py:312-345 (역할별 처리)
if message["role"] == "user":
    assert isinstance(content, str)
    value_ids = self.encode(content)
    add_tokens(user_start, 0)
    add_tokens(value_ids, 0)
    add_tokens(user_end, 0)
elif message["role"] == "assistant":
    add_tokens(assistant_start, 0)
    if isinstance(content, str):
        value_ids = self.encode(content)
        add_tokens(value_ids, 1)
    elif isinstance(content, list):
        for part in content:
            value_ids = self.encode(part["text"])
            if part["type"] == "text":
                add_tokens(value_ids, 1)
            elif part["type"] == "python":
                add_tokens(python_start, 1)
                add_tokens(value_ids, 1)
                add_tokens(python_end, 1)
            elif part["type"] == "python_output":
                add_tokens(output_start, 0)
                add_tokens(value_ids, 0)
                add_tokens(output_end, 0)
            else:
                raise ValueError(f"Unknown part type: {part['type']}")
    else:
        raise ValueError(f"Unknown content type: {type(content)}")
    add_tokens(assistant_end, 1)
```

여기서 *세심하게* 봐야 할 결정이 몇 개 있다. 풀어보자.

**(1) 사용자 메시지는 *전부 mask=0*.** `<|user_start|>`, 본문, `<|user_end|>` 셋 모두 mask=0이다. 모델은 *사용자의 말투를 모방하지 않는다*. 그저 *조건*으로 받는다. 직관적이다.

**(2) 어시스턴트의 *시작 토큰* `<|assistant_start|>`도 mask=0.** 이건 약간 *생각해볼 만하다*. *왜* 시작 토큰만 학습 안 받지? 답은 — *시작 토큰을 모델이 출력할 일이 없기* 때문이다. 추론 시점에 `<|assistant_start|>`는 *우리(엔진)*가 *프롬프트로 강제* 주입하는 토큰이지, 모델이 *자기 의지로 sample*하는 토큰이 아니다. 학습할 필요가 없다.

**(3) 어시스턴트의 *본문*과 `<|assistant_end|>`는 mask=1.** 이게 *진짜 학습 신호*다. 그리고 *끝 토큰 `<|assistant_end|>`까지 학습받는다*는 사실에 주목하자. 모델이 *언제 말을 끝낼지*도 *학습 대상*이라는 뜻이다. 영원히 떠드는 모델이 되지 않기 위한 결정이다.

**(4) `<|python_start|>` ~ `<|python_end|>`는 mask=1.** 어시스턴트가 *파이썬 도구 호출*을 *결정*하는 토큰이니, 학습받아야 한다. 모델이 *언제 도구를 호출할지*도 학습한다.

**(5) `<|output_start|>` ~ `<|output_end|>`는 mask=0.** 파이썬 *실행 결과*는 *추론 시점에 외부 함수*가 채워넣는 토큰이다. 모델이 *예측*할 토큰이 아니므로 학습 안 받는다.

이 다섯 결정이 무엇을 *합성*하는지 한 문장으로 정리하자. **모델은 *자기가 출력할 토큰*만 학습받고, *외부에서 주입되는 토큰*은 *조건*으로만 받아들인다.** 토크나이저 단에서 *학습 데이터의 정체성*까지 정의된 셈이다. 8장에서 이 mask가 `targets[mask==0] = -1` (ignore_index)로 흘러들어가 *학습 손실 계산에서 제외*되는 광경을 볼 것이다. 그게 SFT의 *철학*이다.

> **잊지 말자.** `render_conversation`은 단순한 *토큰화*가 아니다. *학습 신호의 경계*를 *대화 구조에 맞춰* 새기는 함수다. 토크나이저가 *학습 데이터의 의미*까지 책임진다.

**mask=1/0의 *시각화*를 작은 예시로 보자.** 사용자가 *"9 곱하기 8은?"*이라 묻고 어시스턴트가 *파이썬 도구 호출*로 *72*를 답하는 상황을 *수동으로* 토큰화해보자. 토크나이저가 다음과 같은 *대화 dict*를 받는다.

```python
conversation = {
    "messages": [
        {"role": "user", "content": "9 곱하기 8은?"},
        {"role": "assistant", "content": [
            {"type": "text",          "text": "계산해볼게요. "},
            {"type": "python",        "text": "9*8"},
            {"type": "python_output", "text": "72"},
            {"type": "text",          "text": "답은 72입니다."},
        ]},
    ]
}
ids, mask = tokenizer.render_conversation(conversation)
```

그러면 *ids와 mask*가 다음 그림처럼 *짝지어* 나온다 (개념적 도식, 토큰 수는 *근사*).

```
ids:    <|bos|> <|user_start|> ... '9 곱하기 8은?' ... <|user_end|>
mask:     0          0                   0 0 0 0          0

        <|assistant_start|>  '계산해볼게요. '   <|python_start|> '9*8' <|python_end|>
                0                  1 1 1 1            1            1 1         1

        <|output_start|>  '72'   <|output_end|>   '답은 72입니다.'   <|assistant_end|>
                0          0           0              1 1 1 1                1
```

이 그림을 *몇 초 더* 들여다보자. **mask=1 영역**은 모델이 *학습받는* 토큰이다. *어시스턴트의 본문 텍스트*(`계산해볼게요`, `답은 72입니다`)와 *파이썬 호출 자체*(`<|python_start|>` ~ `<|python_end|>` 사이의 `9*8`)와 *어시스턴트의 종료 신호*(`<|assistant_end|>`). 즉 모델은 *언제 도구를 호출할지*, *어떻게 호출할지*, *결과를 보고 어떻게 마무리할지*, *어디서 멈출지*를 모두 학습한다.

**mask=0 영역**은 *조건*이다. *사용자 메시지*는 외부에서 주어지고, *파이썬 실행 결과*도 외부 함수가 채워넣고, *어시스턴트 시작 토큰*도 엔진이 강제 주입한다. 모델은 이 토큰들을 *예측하려 들지 않는다* — 그저 *맥락*으로 받아들인다.

이 *학습 신호의 경계 짓기*가 *얼마나 섬세*한지 느껴지는가? 만약 `<|python_output|>` 결과까지 *학습 대상에 포함*되면 어떤 일이 벌어질까? 모델이 *외부 함수의 출력*을 *흉내내려고* 들 것이다. 즉 *호출 없이* `72`를 *지어내는* 모델이 된다 — 환각(hallucination)의 한 형태다. 그래서 *python_output* 영역은 *철저히 mask=0*이다. 모델에게 *"이건 너의 책임이 아니야"*라고 알려주는 셈이다.

> **함께 음미해두자.** 이 mask=1/0 결정은 *수십 줄짜리 헬퍼 함수*에 *조용히* 박혀 있다. 그런데 그 결정이 *우리 모델이 도구를 어떻게 쓰는지*를 *직접* 결정한다. 코드의 *작은 결정*이 모델의 *큰 행동*을 만든다 — nanochat을 읽다 보면 이런 *작은 결정과 큰 행동의 다리*가 정말 자주 나타난다.

`tokenizer.visualize_tokenization(ids, mask)`라는 *디버그 헬퍼*도 함께 있다 (`tokenizer.py:352-365`). 같은 ids/mask를 받아 *터미널에 색깔로* 표시해준다 — mask=1은 *초록*, mask=0은 *빨강*. SFT 데이터를 검수할 때 *눈으로* 손실 마스킹이 *맞는지* 확인하는 도구다. 8장에서 *직접* 호출해볼 기회가 있다.

마지막으로 *짝이 되는 함수* `render_for_completion`이 있다. 추론·RL 시점에 쓰이는데, 같은 대화를 *마지막 어시스턴트 메시지를 빼고* 토큰화한 뒤 `<|assistant_start|>`만 *프롬프트 끝*에 붙여둔다 — *"여기서부터 어시스턴트가 답할 차례"*라고 모델에게 신호하는 셈이다 (`tokenizer.py:367-385`). *학습용 함수*가 *추론용 함수*와 *짝을 이루는* 이 디자인도 nanochat 곳곳에서 반복되는 패턴이다.

같은 대화 구조를 *학습 시점에는 mask로*, *추론 시점에는 프롬프트 종결로* 다루는 *두 함수의 짝꿍*. 이 *대칭*이 nanochat의 우아함의 일부다. 8장과 10장에서 두 함수가 *각각의 무대*에서 활약하는 광경을 다시 본다.

---

## 2.9 챕터 끝 실습 — 같은 문장, 세 토크나이저로 직접 보기

이제 *2.5절의 표*를 *직접* 재현해보자. 우리 손으로 한 번 측정해두면, 이 책 어디서 한국어 처리가 *왜 느려지는지*가 *몸으로* 와닿는다.

> **[CPU 30분] 세 토크나이저 비교 실습**
>
> 준비물: `tiktoken` (pip 한 줄), nanochat 32K 토크나이저 체크포인트(없으면 일단 GPT-2/GPT-4 두 개만으로 시작해도 좋다).
>
> ```python
> import tiktoken
>
> # 1) GPT-2 토크나이저 (50K vocab)
> enc_gpt2 = tiktoken.get_encoding("gpt2")
>
> # 2) GPT-4 cl100k_base 토크나이저 (100K vocab)
> enc_gpt4 = tiktoken.get_encoding("cl100k_base")
>
> # 비교할 문장들
> samples = {
>     "korean":  "안녕하세요, 저는 토비입니다.",
>     "english": "Hello, I am Toby.",
>     "code":    "def add(a, b):\n    return a + b\n",
>     "math":    "1234 + 5678 = 6912",
> }
>
> for label, text in samples.items():
>     bytes_len = len(text.encode("utf-8"))
>     ids_gpt2  = enc_gpt2.encode(text)
>     ids_gpt4  = enc_gpt4.encode(text)
>     print(f"\n[{label}] '{text}'")
>     print(f"  bytes  : {bytes_len}")
>     print(f"  GPT-2  : {len(ids_gpt2):3d} tokens  ({bytes_len/len(ids_gpt2):.2f} bytes/token)")
>     print(f"  GPT-4  : {len(ids_gpt4):3d} tokens  ({bytes_len/len(ids_gpt4):.2f} bytes/token)")
> ```
>
> *(nanochat 32K 토크나이저가 학습돼 있다면 다음을 추가하자.)*
>
> ```python
> from nanochat.tokenizer import get_tokenizer
> enc_nano = get_tokenizer()
> for label, text in samples.items():
>     ids = enc_nano.encode(text)
>     print(f"[{label}] nanochat 32K: {len(ids)} tokens")
> ```
>
> **확인 포인트**
>
> 1. *한국어*가 GPT-2에서 *몇 토큰*, GPT-4에서 *몇 토큰*인지. 2.5절의 *방향*과 일치하는가?
> 2. *영어*는 어느 토크나이저든 *5~6 토큰*이다. 그 안정성과 *한국어의 변동성*을 같이 보자.
> 3. *수식 `1234 + 5678`* — GPT-2(`\p{N}{1,3}` 변형 적용 안 함)에서는 `1234`가 *1토큰*에 가깝다. GPT-4는 `1234`가 `123`+`4`. nanochat 32K는 `12`+`34`(2자리 끊기). 이 차이가 *수학 능력*에 어떻게 영향을 줄지 — 5장의 sklearn 이야기와도 연결되지만 — 일단 *직접 측정*해 두자.
> 4. *코드 들여쓰기* — GPT-4의 `cl100k_base`는 *4-스페이스 들여쓰기*를 *한 토큰*으로 처리한다. GPT-2는 그렇지 않다. 코드 처리 비용의 차이가 *어디서 오는지* 손으로 느껴보자.

여기서 *수치를 직접* 본 다음, 이 챕터 본문의 표를 *자기 측정으로 덮어쓰면* 좋겠다. 책의 표는 *방향*만 보여주는 *근사치*다. *진짜 값*은 *당신의 손*에서 나온다.

> **한 걸음 더 — *분할 자체를 눈으로* 보기**
>
> 토큰의 *개수*만 보면 충격이 살짝 약하다. *어떻게 잘리는지*를 *글자로* 보면 더 또렷해진다. tiktoken은 *각 토큰의 디코딩된 문자열*도 보여줄 수 있다.
>
> ```python
> def show_split(enc, text, label):
>     ids = enc.encode(text)
>     pieces = [enc.decode([i]) for i in ids]
>     joined = " | ".join(repr(p) for p in pieces)
>     print(f"[{label}] ({len(ids)} tokens) {joined}")
>
> show_split(enc_gpt2, "안녕하세요, 저는 토비입니다.", "GPT-2")
> show_split(enc_gpt4, "안녕하세요, 저는 토비입니다.", "GPT-4")
> ```
>
> GPT-2의 출력에 *깨진 듯한 글자*들이 보일 텐데, *그게 깨진 게 아니다* — UTF-8 바이트가 *Latin-1로 잘못 해석된* 한 글자씩이다. GPT-2는 한글을 *바이트 수준으로 흩어서 본다*는 *증거*다. GPT-4의 출력에서는 `안`, `녕`, `하세요` 같은 *한국어 음절*이 *통째로* 토큰이 된 모습을 본다. 두 시각의 차이가 *글자로 보인다*.
>
> 같은 실습을 *영어 문장*과 *코드*에도 해보자. 영어는 두 토크나이저 모두 *비슷하게* 자른다 — 차이는 미미하다. 코드의 *4스페이스 들여쓰기*는 GPT-4가 *한 토큰*에 묶고, GPT-2는 *공백 4개*로 흩는다. *어떤 텍스트가 어떤 토크나이저에 친화적인지*가 *눈으로* 드러난다.

이 *글자 단위 시각화*는 토크나이저를 *몸으로 이해*하는 가장 빠른 길이다. 머리로 알기보다 *손으로* 알자. 우리 챕터의 *aha*가 *완성*되는 순간이 바로 여기다.

---

## 2.10 마무리 — 시각이 결정한 다음, 학습이 시작된다

토크나이저 챕터를 *함께 끝까지* 따라온 셈이다. 무엇을 손에 쥐었는지 한 줄씩 정리해두자.

- **BPE의 직관** — 가장 빈번한 *바이트 쌍*을 반복적으로 *병합*해 어휘를 만든다. `strawberry`가 두 덩어리로 보이는 이유, `count('r')`이 모델에게 어려운 이유는 *지능*이 아니라 *시각*의 한계다.
- **GPT-4 정규식과 `\p{N}{1,3}` → `\p{N}{1,2}`의 한 글자 차이** — 32K 어휘에 맞춘 *sweet spot 재실험*. 디폴트를 그대로 받지 않고 자기 모델 크기에 맞춰 *직접 검증*한 카르파시의 자세를 기억해두자.
- **9개의 `SPECIAL_TOKENS`** — 토크나이저 단에 박힌 *도구 호출의 어휘*. *모델보다 먼저* 정해진 이 9개가 10장의 *클라이맥스*를 가능하게 만든다.
- **두 구현의 분리** — 학습은 rustbpe, 추론은 tiktoken. *다른 단계, 다른 도구*라는 nanochat의 *반복되는 패턴*의 첫 사례.
- **한국어가 비싼 이유** — 모델의 무관심이 아니라 *학습 데이터 분포의 직접적 결과*. 12장에서 *어떻게 고치는지* 다룬다.
- **vocab_size 32K** — 압축 효율, `lm_head` 비용, CE loss 안정성 *세 힘*이 잡아당기는 *균형점*. 모델 크기에 맞춰 *재조정*하는 다이얼이다.
- **`token_bytes.pt`** — 7장 *bits-per-byte 평가*를 위해 2장에서 미리 준비된 *조용한 사다리*.
- **`render_conversation`의 mask=1/0** — *어시스턴트가 학습받는 토큰의 경계*를 토크나이저 단에서 정의. 8장 SFT의 *철학적 기초*.

함께 *한 번 더 음미*해두자. 토크나이저는 *그저 텍스트를 자르는 도구*가 아니다. *모델의 시각*이고, *학습 데이터의 의미*이고, *도구 호출의 어휘*이고, *평가의 기준*이다. 한 파일 — `tokenizer.py` 406줄 — 안에 그 모든 결정이 *조용히 박혀* 있다. nanochat을 읽는다는 건, 이런 *작은 파일들의 결정의 무게*를 *손에 쥐어보는 일*이다.

그렇다면 *다음 발걸음*은 무엇일까? 우리는 토크나이저의 *코드*와 *결정의 무게*를 봤다. 이제 *실제로 학습시키는 일*이 남았다. 3장에서는 **`scripts/tok_train.py`** 한 줄씩을 따라 *2B chars의 FineWeb*을 BPE에 흘려보낸다. 그리고 **`scripts/tok_eval.py`**로 *우리의 32K가 GPT-2(50K), GPT-4(100K)와 얼마나 효율적*인지 — *영문 뉴스, 한국어, 코드, LaTeX, 과학 텍스트* 각각에 대해 — 측정한다. 이 챕터의 *aha*가 *데이터*로 확장된다.

*시각이 결정된 다음에야 학습이 시작된다.* 카르파시가 그렇게 짜둔 이유를 *함께* 검증해보자.
