# 8장. 대화하는 모델을 만든다 — SFT

수치를 의심하는 법은 보았다. CORE 0.26이 정말 GPT-2와 같은 자리에 우리를 데려다 놨는지, val_bpb 0.745가 우리 모델의 압축률을 어떻게 *증언*하는지, centered accuracy의 0이 무엇을 의미하는지까지. 그런데 우리가 손에 쥔 그 base 모델은 아직 *대화*를 못 한다. 정확히 말하면, 대화처럼 보이는 무언가를 시도조차 하지 않는다.

`chat_cli`에 base 체크포인트를 물리고 "What is the capital of France?"라고 물어보자. 운이 좋다면 한 줄짜리 답이 흘러나올지도 모른다. 그런데 더 흔하게는 — *질문 자체를 이어서 쓴다*. 마치 위키피디아 문장이 끊긴 자리에 다음 문장을 짜내듯이.

```
> What is the capital of France?
 The capital of France is Paris, but it is also home to several other major cities including Marseille, Lyon, and Toulouse. The country itself spans...
```

이건 *버그*가 아니다. 우리가 6장에서 정확히 *이런 모델*을 만들었다. FineWeb-EDU 11M 페이지를 한 줄씩 받아 *다음 토큰을 맞히게* 가르쳤다. 그래서 base 모델은 *문장 완성기*다. "ChatGPT가 답하듯이 짧게 답한다"는 *학습 분포*에 존재하지 않는다. 위키피디아 어디에도 `<|user_start|>What is the capital of France?<|user_end|><|assistant_start|>Paris.<|assistant_end|>` 같은 시퀀스가 박혀 있을 리 없으니까.

그렇다면 어떻게 해야 할까? 답은 단순하다 — **그런 시퀀스를 *직접* 만들어서 가르치자.** 그게 이번 장의 전부다. Supervised Fine-Tuning, SFT. 모델이 *완성*하던 자리에 *대화*를 채워 넣는다. 마법 같은 알고리즘이 새로 등장하는 게 아니라, *데이터의 모양*이 바뀐다. 그리고 우리는 이미 만들어둔 옵티마이저와 GPT 모듈을 *그대로* 다시 쓴다. 이 챕터를 다 읽고 나면 한 가지를 알게 된다 — **능력은 알고리즘이 아니라 데이터로 가르치는 일이 훨씬 많다.**

## base 모델의 정체 — 우리는 무엇을 만들어 두었나

먼저 한 가지를 분명히 해두자. 6장에서 만든 base 모델은 *바보*가 아니다. CORE 0.26은 GPT-2 1.6B의 0.2565와 같은 줄에 서 있는 *진짜 실력*이다. 단지 그 실력이 *대화의 형태*로 발현되지 않을 뿐이다. 비유하자면 — 도서관 한 칸을 통째로 외운 사람을 데려다 두고 "오늘 점심 뭐 먹을래?"라고 묻는 격이다. 그 사람은 점심 메뉴를 모르는 게 아니라, *질문에 답하는 모드*가 켜지지 않았다.

`render_for_completion`을 한번 들여다보자. `tokenizer.py:367-388`에 있다 — `render_conversation`보다 짧고, 무엇이 *완성*인지 정직하게 보여준다. user 메시지를 `<|user_start|>...<|user_end|>`로 감싸고 `<|assistant_start|>` 토큰을 *프라임*해서 모델에 넘긴다. 그러고는 `<|assistant_end|>`가 나올 때까지 `engine.generate`를 돌린다. 우리는 9개의 `SPECIAL_TOKENS` 중 일부를 *대화의 경계*로 쓸 셈이다.

```python
# nanochat/tokenizer.py:13-25 — 9개의 SPECIAL_TOKENS
SPECIAL_TOKENS = [
    "<|bos|>",
    "<|user_start|>", "<|user_end|>",
    "<|assistant_start|>", "<|assistant_end|>",
    "<|python_start|>", "<|python_end|>",
    "<|output_start|>", "<|output_end|>",
]
```

2장에서 우리는 이 토큰들을 *왜 토크나이저 단에* 박아두었는지 의아해했다. 그때는 "나중에 도구 사용을 추가하기 어렵게 만드는 결정의 무게"라고 적어 두었다. 이제 그 무게의 *실체*가 드러난다. SFT 단계에 와서야 이 토큰들이 *처음으로 의미를 갖는다*. base pretrain 동안 모델은 이 9개 토큰을 *거의 본 적이 없다* — 셰드 안에 어쩌다 한 번 박혀 있을지언정 (실은 거의 없다). 그래서 base 모델에게 `<|user_start|>`는 그저 *흔하지 않은 토큰*일 뿐이다. 우리는 SFT 단계에서 이 토큰을 *수십만 번* 보여주며 **"이건 사용자의 말이 시작되는 곳이다, 너는 `<|assistant_start|>` 뒤에 나오는 토큰만 *예측*하면 된다"**라고 가르친다.

그런데 잠깐, 한 가지 의문이 든다. 옛 nanochat에는 *midtraining*이라는 단계가 있었다. 사전학습과 SFT 사이에 끼어 들어가서 채팅 포맷·다지선다·도구 사용을 *살짝* 사전 노출시키는 단계. 그 단계는 어디로 갔을까?

이게 nanochat 코드 변경 이력에서 *가장 조용한 드라마* 중 하나다. midtraining이 사라진 이유는 *알고리즘이 좋아져서*가 아니라 *dataloader가 좋아져서*다. 6장에서 우리가 `dataloader.py:74-162`의 BOS-aligned bestfit-crop를 읽으며 "왜 토큰을 35%나 *버리는가*"를 한참 따져봤다. 그 결정 덕에 한 row 안에 *문서 경계*가 깔끔해졌고, 옛 dataloader가 만들어내던 "여러 문서가 한 줄에 끊긴 채 섞이는 잡음"이 사라졌다. 그 잡음을 *완화*하려고 끼워 넣었던 midtraining 단계가, 잡음 자체가 사라지자 *불필요해졌다*. speedrun이 base_train → chat_sft로 *바로 점프*하는 이유다.

이 한 사건이 책 전체의 교훈 하나를 정확히 보여준다. **단계 하나가 사라지는 것보다, 그 단계가 *왜* 필요했는지를 묻는 게 더 중요하다.** 우리는 6장에서 dataloader를 한 줄씩 읽었기 때문에 midtraining의 부재가 *우연*이 아니라 *결과*라는 걸 안다. 이런 게 코드를 끝까지 따라간 보상이다.

## 손실 마스킹의 철학 — 어시스턴트로서만 학습한다

이제 SFT 데이터가 *무엇처럼 생겼는지* 보자. `chat_sft.py`가 부르는 함수는 `tokenizer.render_conversation`이다 (`tokenizer.py:266-365`). 한 페이지가 안 되는 짧은 함수인데, 한 가지가 *결정적*이다 — 반환값이 `(ids, mask)` *두 개*다.

```python
# nanochat/tokenizer.py:266-271 — render_conversation의 약속
def render_conversation(self, conversation, max_tokens=2048):
    """
    Tokenize a single Chat conversation ...
    Returns:
    - ids: list[int] is a list of token ids of this rendered conversation
    - mask: list[int] of same length, mask = 1 for tokens that the
            Assistant is expected to train on.
    """
```

`mask`가 무엇인가? 같은 길이의 0/1 벡터다. **mask=1**은 "이 토큰은 어시스턴트가 *학습해야 할* 토큰", **mask=0**은 "이 토큰은 모델이 *보긴 보지만 예측의 대상은 아닌* 토큰"이다. 한 대화 안의 모든 토큰이 입력으로 들어가지만, *손실은 mask=1인 자리에서만* 발생한다.

`render_conversation`의 한 가운데(`:302-345`)를 펴 보면 *누가 mask=1인지*가 한눈에 들어온다.

```python
# nanochat/tokenizer.py:312-317 — user 메시지는 전부 mask=0
if message["role"] == "user":
    assert isinstance(content, str), ...
    value_ids = self.encode(content)
    add_tokens(user_start, 0)   # 특수 토큰도 mask=0
    add_tokens(value_ids, 0)    # user 텍스트 mask=0
    add_tokens(user_end, 0)
```

user 메시지는 *전부* mask=0이다. 당연하다. 사용자가 *뭐라고 말할지*를 우리 모델이 예측할 필요는 없으니까. 사용자의 말은 *조건*이지 *생성*이 아니다.

```python
# nanochat/tokenizer.py:318-345 — assistant 메시지의 정교한 마스킹
elif message["role"] == "assistant":
    add_tokens(assistant_start, 0)   # 시작 마커는 mask=0
    if isinstance(content, str):
        value_ids = self.encode(content)
        add_tokens(value_ids, 1)     # 어시스턴트 답변은 mask=1
    elif isinstance(content, list):
        for part in content:
            ...
            if part["type"] == "text":
                add_tokens(value_ids, 1)              # 텍스트도 mask=1
            elif part["type"] == "python":
                add_tokens(python_start, 1)
                add_tokens(value_ids, 1)               # 도구 호출도 mask=1
                add_tokens(python_end, 1)
            elif part["type"] == "python_output":
                add_tokens(output_start, 0)
                add_tokens(value_ids, 0)               # 도구 출력은 mask=0
                add_tokens(output_end, 0)
    add_tokens(assistant_end, 1)     # 끝 마커는 mask=1 (생성 종료를 배운다)
```

여기에 *철학*이 있다. 잠깐 음미해보자.

- **`<|assistant_start|>`는 mask=0**: 어시스턴트의 *시작 시점*은 우리가 결정한다. 모델이 *언제 답할지*를 예측할 필요는 없다. 그 시점은 `chat_cli`가 강제로 프라임한다.
- **`<|assistant_end|>`는 mask=1**: 그런데 *언제 끝낼지*는 모델이 배워야 한다. 어시스턴트는 "답이 다 됐다"를 스스로 결정해야 하니까. 그래서 끝 마커는 *예측 대상*이다.
- **python 도구 호출은 mask=1**: 9장에서 RL로 다시 보겠지만 — 모델은 *언제 calculator를 부를지*를 *결정*해야 한다. 그래서 `<|python_start|>...<|python_end|>` 안쪽이 전부 mask=1이다. 모델이 "여기서 도구를 호출해야겠다"를 *학습*한다.
- **python 출력은 mask=0**: 도구의 *결과*는 test time에 *진짜 파이썬 인터프리터*에서 온다. 모델이 그걸 예측하면 *환각*이다. 그래서 mask=0이다.

이게 *어시스턴트로서의 역할*을 학습한다는 말의 코드적 의미다. 모델은 *사용자의 문장*을 흉내 내지 않고, *도구의 출력*을 지어내지 않으며, *언제 답하기 시작할지*를 결정하지도 않는다. 모델이 배우는 건 단 하나 — **사용자가 말한 직후에, 도구 출력이 도착한 직후에, *어떻게 답해야 하는가*.** 그 자리에서만 손실이 흐른다.

`chat_sft.py:292-297`에서 이 mask를 텐서에 *집어넣는* 부분도 한번 보자. 코드는 정직하다.

```python
# scripts/chat_sft.py:292-297
# Apply the loss mask from render_conversation ...
# mask[1:] aligns with targets (shifted by 1).
# Unmasked positions get -1 (ignore_index).
mask_tensor = torch.tensor(mask_rows, dtype=torch.int8)
mask_targets = mask_tensor[:, 1:].to(device=device)
targets[mask_targets == 0] = -1
```

`-1`은 PyTorch `cross_entropy`의 `ignore_index` 기본값이다. mask=0 자리의 target을 -1로 채우면 — 그 자리는 *손실 계산에서 사라진다*. 그래디언트도 흐르지 않는다. 모델 입장에서는 *해당 자리 토큰이 존재하지 않는 셈*이다. 단 *입력*으로는 여전히 보인다. 그게 마스킹의 묘수다 — *문맥은 보여주되 학습은 시키지 않는다*.

이 한 줄이 base pretrain과 SFT의 *유일한 코드 수준 차이*다. base는 *모든 토큰*에 손실을 흘렸다. SFT는 *어시스턴트로서 말해야 하는 토큰*에만 손실을 흘린다. 모델 아키텍처도, 옵티마이저도, FlashAttention 디스패처도, 토크나이저도 그대로다. 바뀐 건 **데이터의 모양**과 **손실의 자리**뿐이다.

## SFT 데이터 믹스 — 6개의 task가 각각 가르치는 것

자, 그렇다면 우리가 어시스턴트에게 *무엇을* 가르치려는 걸까? `chat_sft.py:165-173`을 통째로 읽자. 이게 nanochat이 *대화 능력*이라고 부르는 것의 *정의*다.

```python
# scripts/chat_sft.py:165-173 — SFT 데이터 믹스
train_tasks = [
    SmolTalk(split="train"),                      # 460K 일반 대화
    CustomJSON(filepath=identity_conversations_filepath),  # 1000 identity
    CustomJSON(filepath=identity_conversations_filepath),  # × 2 epochs
    *[MMLU(subset="all", split="auxiliary_train")
      for _ in range(args.mmlu_epochs)],          # 100K × 3 epochs
    *[GSM8K(subset="main", split="train")
      for _ in range(args.gsm8k_epochs)],         # 8K × 4 epochs
    SimpleSpelling(size=200000, split="train"),   # 200K 단순 철자
    SpellingBee(size=80000, split="train"),       # 80K 글자 세기
]
train_dataset = TaskMixture(train_tasks)
```

여덟 줄 안에 *대화 능력의 정의*가 들어 있다. 한 줄씩 풀어보자.

**SmolTalk(train) — 460K행, 일반 대화의 *체격*.** HuggingFaceTB가 공개한 SmolTalk 코퍼스의 train split이다. user-assistant 다중 턴 대화로, "오늘 날씨가 어때?" 같은 일상부터 "이 자바스크립트 코드 좀 봐줘" 같은 기술 질문까지 460K행이 들어 있다. 이게 어시스턴트의 *기본 어조*를 잡는다. 분량이 압도적이라 — 다른 task가 *수만 행* 단위인데 SmolTalk만 *수십만 행* — *말투의 색*은 사실상 SmolTalk가 결정한다.

**CustomJSON(identity) × 2 — 1000행, *너는 누구인가*.** 이게 nanochat 코드에서 가장 사랑스러운 한 줄이다. 두 번 등장하는 같은 task. 같은 파일 — `identity_conversations.jsonl` — 을 *두 번* 데이터셋에 넣는다. 파이썬 컴프리헨션 한 줄에 `_ for _ in range(2)`라고 명시적으로 적어두기보다, 그냥 두 번 *복사해 둔* 모습이 코드의 정직함을 보여준다. 왜 두 번인가? **1000행은 460K행 옆에 끼면 *그림자처럼 묻혀버리기* 때문이다.** identity는 *오버샘플링이 필요하다*. 두 번 등장시키면 effective epoch이 2가 되어, 모델이 "I'm nanochat, an open source chatbot..."을 *반복해서* 본다.

이 1000행은 어디서 왔는가? `dev/gen_synthetic_data.py`가 OpenRouter API를 호출해 Gemini Flash 같은 큰 모델에게 *9개 카테고리 × 12개 페르소나 × 10개 대화 동역학 × 7개 첫 메시지 스타일*을 sampling해 합성해온 결과다. `knowledge/self_knowledge.md`에 적힌 사실들("nanochat은 카르파시가 만든 ~~ 오픈소스 챗봇이다")을 큰 모델이 *다양한 표현으로* 다시 짠 1000편의 짧은 대화. 이게 모델의 *자아*다.

12장에서 우리는 이 파일을 *우리 이름*으로 바꿔 *자기 챗봇*을 만든다. 그때 다시 만나자.

**MMLU(auxiliary_train) × 3 — 100K × 3, *4지선다의 형식*.** Hendrycks의 MMLU는 57개 학문 분야의 4지선다 문제다. auxiliary_train은 그중 학습용으로 공개된 100K행. 우리가 가르치는 건 *지식*이 아니라 **형식** — "Q: ... A) ... B) ... C) ... D) ... Answer:" 형태의 프롬프트에 *한 글자*로 답하는 패턴이다. 3 epochs를 도는 건 이 형식이 *낯설기* 때문이다. SmolTalk에는 이런 정형 4지선다가 거의 없다.

**GSM8K(train) × 4 — 8K × 4, *수학과 도구 호출*.** 가장 적은 행 수지만 가장 많은 epochs를 받는다. 왜? GSM8K는 *두 능력을 동시에* 가르치기 때문이다. 첫째, 초등수학 풀이의 *단계적 사고*. 둘째, `<<expr=result>>` 패턴의 *도구 호출*. `tasks/gsm8k.py:60-76`에서 카르파시가 어떻게 이걸 *어시스턴트의 part*로 분해하는지 보자.

```python
# tasks/gsm8k.py:60-76 — << >> 안의 식을 python part로 변환
parts = re.split(r'(<<[^>]+>>)', answer)
for part in parts:
    if part.startswith('<<') and part.endswith('>>'):
        inner = part[2:-2]  # << >> 제거
        if '=' in inner:
            expr, result = inner.rsplit('=', 1)
        else:
            expr, result = inner, ""
        assistant_message_parts.append(
            {"type": "python", "text": expr})            # 도구 호출
        assistant_message_parts.append(
            {"type": "python_output", "text": result})   # 도구 출력
    else:
        assistant_message_parts.append(
            {"type": "text", "text": part})              # 일반 텍스트
```

GSM8K 원본 데이터의 `12/60 = $<<12/60=0.2>>0.2`라는 표기를 — 정규식으로 가르며 — *세 개의 part*로 쪼갠다. 텍스트, python, python_output. 이게 render_conversation에 들어가면 *python_output만 mask=0이고 나머지는 mask=1*이 된다. 결과적으로 모델은 "*숫자를 계산해야 하는 자리*에서 `<|python_start|>12/60<|python_end|>`라고 *적는 법*"을 배운다. 그 직후의 결과 `0.2`는 학습 대상이 *아니다* — test time에는 진짜 파이썬이 그 자리를 채워줄 테니까.

이게 *도구 사용을 데이터로 가르치는* 코드 한 페이지짜리 답이다. 별도의 RL 단계 없이도 — SFT만으로도 — 모델은 *언제 도구를 부를지*를 학습한다. 9장에서 RL이 이걸 *어떻게 더 단단하게* 만드는지 보겠지만, *기초 도구 호출의 본능*은 여기서 심긴다.

**SimpleSpelling 200K + SpellingBee 80K — *토큰을 글자로 풀어내는 본능*.** 카르파시가 [#164](https://github.com/karpathy/nanochat/discussions/164)에서 길게 다룬 "strawberry 문제"다. "How many r are in strawberry?"에 LLM이 약한 이유는 단순하다 — 토크나이저가 `strawberry`를 *하나의 토큰*으로 보거나 잘해야 두세 토큰으로 자르기 때문에, char 단위 추론이 *모델 내부 표현에 직접 없다*. 큰 모델은 그걸 *자기 힘으로* 배우지만, 작은 모델은 그냥 못 배운다. 그래서 데이터로 *명시적으로* 가르친다.

`tasks/spellingbee.py:161-195`의 합성 답안을 펴 보자.

```python
# tasks/spellingbee.py:161-195 (요약) — SpellingBee의 합성 어시스턴트 답안
word_letters = ",".join(list(word))   # 'strawberry' → 's,t,r,a,w,b,e,r,r,y'
manual_text = f"""We are asked to find the number '{letter}' in the word '{word}'.
Let me try a manual approach first.

First spell the word out:
{word}:{word_letters}

Then count the occurrences of '{letter}':
"""
running_count = 0
for i, char in enumerate(word, 1):
    if char == letter:
        running_count += 1
        # comma without space matters! ' a' and 'a' are different tokens!
        manual_text += f"{i}:{char} hit! count={running_count}\n"
    else:
        manual_text += f"{i}:{char}\n"
manual_text += f"\nThis gives us {running_count}."
# 그 다음 python으로 더블 체크
assistant_parts.append({"type": "python",
                        "text": f"'{word}'.count('{letter}')"})
assistant_parts.append({"type": "python_output", "text": str(count)})
assistant_parts.append({"type": "text",
                        "text": f"\n\nPython gives us {count}.\n\n#### {count}"})
```

세 가지가 인상적이다.

첫째, `s,t,r,a,w,b,e,r,r,y` — *쉼표만* 넣고 공백은 *일부러* 뺀다. 코드 주석이 친절하게 적어둔다 — *" a"와 "a"는 다른 토큰이다*. 토크나이저 단의 결정이 합성 데이터의 *포맷*까지 결정한다. 2장에서 BPE의 *변덕*을 봤다면, 여기서 그 변덕에 *맞춰 데이터를 만드는* 사람의 자세가 보인다.

둘째, *수동 카운팅 → 파이썬 더블체크 → 최종 답*의 3단 구조. 모델이 *자기 답*과 *도구의 답*을 *비교*하는 본능을 심는다. 9장 RL에서 이게 어떤 식으로 *더 단단해지는지* 다시 보자.

셋째, 50개 user 메시지 템플릿이 *7개 언어*로 작성돼 있다 — 영어, 스페인어, 중국어, *한국어*("{word}에 {letter}가 몇 개 있나요"), 프랑스어, 독일어, 일본어. 한국어 독자라면 잠깐 멈춰서 이걸 음미해도 좋다. nanochat의 *데이터셋 자체*가 한국어를 *조금이라도* 다루는 자리는 SpellingBee 템플릿 50개 중 4개뿐이다. 그래서 챕터 10에서 한국어 질문이 *영어로 답해지는* 모습을 보게 되는데 — 그게 *학습 데이터 분포의 정직한 결과*다. 12장에서 우리가 한국어로 가는 길을 따로 다루는 이유이기도 하다.

이 6개 task를 `TaskMixture`(tasks/common.py)가 하나로 묶는다. `TaskMixture`는 *deterministic shuffle*을 한다 — 시드 고정으로 모든 rank가 *같은 순서로 인덱싱*하지만, 어느 한 task가 *연달아 등장하지 않도록* 섞는다. 그래서 한 step에서 모델은 SmolTalk 한 줄, MMLU 한 줄, GSM8K 한 줄, SpellingBee 한 줄을 *섞어서* 본다. 한 task에 *과적합*되는 위험을 자연스럽게 줄인다.

여기서 잠깐 멈춰서 *데이터 양*을 따져보자. 460K + 1000×2 + 100K×3 + 8K×4 + 200K + 80K ≈ 1,072K. 약 100만 대화. 한 대화가 평균 300토큰이라 치면 *3억 토큰*. base pretrain의 *12B 토큰*에 비하면 40분의 1이다. **40분의 1로 *대화 능력*을 가르친다.** pretrain은 *세상에 대한 지식*을 12B 토큰으로 흡수하고, SFT는 *그 지식을 어시스턴트로서 발현하는 법*을 3억 토큰으로 가르친다. 비율의 차이가 *학습 목적의 차이*를 그대로 비춘다.

## customjson.py — 능력을 추가하는 진입점

방금 데이터 믹스에서 *가장 짧지만 가장 강력한* 줄이 `CustomJSON(filepath=identity_conversations_filepath)`였다. 이 한 줄을 통해 *어떤 합성 데이터든* SFT 믹스에 끼워 넣을 수 있다. `tasks/customjson.py`는 65줄짜리 파일인데, *진입점*으로서의 역할이 압도적이다. 통째로 한 번 보자.

```python
# tasks/customjson.py 발췌
class CustomJSON(Task):
    """
    Load conversations from a JSONL file.
    Each line should be a JSON array of message objects with
    'role' and 'content' fields.
    Example line: [{"role":"user","content":"Hi"},
                   {"role":"assistant","content":"Hello"}]
    """

    def __init__(self, filepath, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        self.conversations = []

        # Load all conversations from the JSONL file
        if not os.path.exists(filepath):
            # Helpful error message due to recent change.
            print("-" * 80)
            print(f"Warning: File {filepath} does not exist")
            print("HINT (Oct 21 2025)")
            print("If you recently did a git pull and suddenly see this,"
                  " it might be due to the new addition of identity conversations")
            print("See this discussion for more details:"
                  " https://github.com/karpathy/nanochat/discussions/139")
            print("Quick fix: simply run the following command"
                  " to download the file and you're done:")
            print(f"curl -L -o {filepath}"
                  f" https://karpathy-public.s3.us-west-2.amazonaws.com/"
                  f"identity_conversations.jsonl")
            print("-" * 80)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    messages = json.loads(line)
                    assert isinstance(messages, list), ...
                    assert len(messages) >= 2, ...
                    for i, message in enumerate(messages):
                        assert "role" in message, ...
                        assert "content" in message, ...
                        expected_role = "user" if i % 2 == 0 else "assistant"
                        assert message["role"] == expected_role, ...
                    self.conversations.append(messages)
```

`Task` 인터페이스 한 줄(`get_example` 한 줄도 아래쪽에 있다)을 따른다. 그리고 *JSONL 한 줄에 대화 한 편* — 가장 단순한 포맷이다. 더 복잡한 것도 없다.

그런데 이 파일의 *진짜 보석*은 친절한 에러 메시지다.

> **카르파시 식 친절함의 한 박스**
>
> 파일이 없을 때 `CustomJSON`은 *예외를 던지지 않는다*. *경고를 출력하고 그냥 진행*한다. 그 경고가 단순한 "FileNotFoundError" 한 줄이 아니라 *세 가지*를 묶어 보여준다.
>
> 1. **언제 추가된 기능인지**: `HINT (Oct 21 2025)`.
> 2. **왜 갑자기 보이는지**: "*If you recently did a git pull and suddenly see this, it might be due to the new addition of identity conversations*". 사용자가 *git pull*했을 *심리적 상태*까지 추측해서 적었다.
> 3. **해결책 *한 줄***: `curl -L -o ... identity_conversations.jsonl`. 복사 붙여넣기로 *바로 해결*된다.
>
> 이게 카르파시 코드의 특유한 *친절함*이다. 에러 메시지에 *날짜*가 박혀 있는 라이브러리를 처음 봤다면 — 그래, 이건 처음 보는 패턴이다. *기능이 빠르게 변하는 작은 코드베이스*가 사용자와 *직접 소통*하는 방식이다. 이 한 박스가 보여주는 디테일이 책 한 권 분량의 "오픈소스 설계 철학" 강의보다 더 깊다.

이 작은 파일이 *왜* 책에서 한 절을 차지하는가? **자기 챗봇·새 능력 추가·합성 데이터 모두가 이 한 파일을 통과하기 때문**이다.

자기 챗봇을 만들고 싶다면 — `dev/gen_synthetic_data.py`로 1000줄 합성한 뒤 `identity_conversations.jsonl`을 *교체*하면 된다. SpellingBee 패턴으로 새 능력을 가르치고 싶다면 — `tasks/X.py`에 새 Task 클래스를 만들고 `chat_sft.py:165-173`의 train_tasks 리스트에 추가하면 된다. 그것보다 더 *가벼운 길*은 — `CustomJSON(filepath="my_new_skill.jsonl")` 한 줄을 끼우는 것이다. 능력의 *진입 비용*이 *한 줄*까지 떨어진다.

이게 카르파시가 [#139](https://github.com/karpathy/nanochat/discussions/139)에서 말한 *능력은 데이터로 가르치는 일이 코드로 가르치는 일보다 훨씬 흔하다*의 코드적 의미다. 알고리즘을 새로 짜는 게 아니라, *JSONL 한 파일*을 새로 만든다. 12장에서 우리는 *우리 자신의 정체성*을 이 파일에 적어 넣어 *자기 챗봇*을 만들 것이다.

## BOS-aligned bestfit-pad — 대화는 *토막내지 않는다*

데이터 준비의 한 자락이 더 남아 있다. 6장에서 우리는 BOS-aligned bestfit-*crop* dataloader를 봤다. *문서 경계*를 지키되, row가 꽉 차지 않으면 *남은 자리는 잘라낸다* — 그래서 토큰을 35% 정도 *버린다*. 이게 *사전학습*용이었다. 같은 알고리즘의 *사촌*이 SFT에도 있다.

`chat_sft.py:187-305`의 `sft_data_generator_bos_bestfit`이 그 사촌이다. 이름은 비슷한데 *철학*이 다르다. **cropping이 아니라 padding이다.**

```python
# scripts/chat_sft.py:253-260 — bestfit-pad의 한 가운데
if best_idx >= 0:
    # Found a conversation that fits - use it entirely
    conv, conv_mask = conv_buffer.pop(best_idx)
    row.extend(conv)
    mask_row.extend(conv_mask)
    consumed += ddp_world_size
else:
    # No conversation fits - pad the remainder instead of cropping
    # This ensures we never discard any tokens
    content_len = len(row)
    row.extend([bos_token] * remaining)  # Pad with BOS tokens
    mask_row.extend([0] * remaining)
    padded = True
    break  # Row is now full (with padding)
```

코드의 한 줄짜리 주석이 이유를 정확히 말한다 — *"This ensures we never discard any tokens"*. 사전학습에서는 *문맥의 잡음*이 더 큰 문제라 토큰을 *버리는* 결정이 옳았다. SFT에서는 *대화 한 편이 토막 나는 것*이 더 큰 문제다. "What is the capital of France? — Paris." 같은 짧은 대화가 *중간에서 끊긴 채* 다음 row로 넘어가면, 모델은 *대화의 끝*을 못 배운다. 그래서 SFT는 *남는 자리를 BOS로 padding*하고, 그 padding의 target을 -1(ignore_index)로 만든다.

`chat_sft.py:299-303`이 그 마지막 정리다.

```python
# Mask out padding positions in targets (set to -1 = ignore_index)
for i, content_len in enumerate(row_lengths):
    if content_len < row_capacity:
        targets[i, content_len-1:] = -1
```

손실은 *진짜 대화 토큰*에서만 흐른다. padding의 BOS 토큰은 *입력*으로는 들어가지만 *손실*은 흐르지 않는다. 메모리는 약간 낭비되지만 — 대화는 *온전히 보존된다*. 이게 SFT의 우선순위다.

여기서 *한 개 더* 짚어둘 게 있다. `bestfit` 알고리즘 그 자체. 코드를 펴 보면 *제일 긴* 대화부터 row에 채워 넣는다.

```python
# scripts/chat_sft.py:238-245 — best-fit decreasing
best_idx = -1
best_len = 0
for i, (conv, _) in enumerate(conv_buffer):
    conv_len = len(conv)
    if conv_len <= remaining and conv_len > best_len:
        best_idx = i
        best_len = conv_len
```

남은 자리에 *들어갈 수 있는 가장 큰* 대화를 찾는다. 이게 *bin packing*의 고전적 휴리스틱이다 (best-fit decreasing). 작은 대화 여러 개를 끼우려고 *조각조각*하지 않고, *큰 덩어리 하나*가 들어갈 수 있다면 그걸 먼저 쓴다. 결과적으로 padding 비율이 *최소화*된다. 가장 단순한 정렬 휴리스틱이 한 페이지 코드로 들어 있다.

물론 이렇게 해도 *완벽한 packing*은 불가능하다. 대화 길이의 분포가 들쭉날쭉하니까. 어느 정도의 padding은 *남는다*. 이게 SFT의 *throughput cost*다. 그래도 *데이터를 버리지 않는* 쪽이 *대화 능력 학습*에서는 압도적으로 우세하다는 게 카르파시의 판단이다.

## LR schedule과 옵티마이저 warm-start — 사전학습의 *기억*을 잇는다

데이터가 준비됐다. 손실 마스크도 박혔다. 그렇다면 *옵티마이저는 어떻게 시작하는가*? base pretrain이 *마지막 step*에서 LR을 거의 *0*까지 끌어내렸다. 그 자리에서 *그대로* SFT를 시작하면 — 학습이 진행되지 않는다. LR이 0이니까.

`chat_sft.py:158-161`에 이 결정이 들어 있다.

```python
# scripts/chat_sft.py:158-161 — SFT의 LR을 다시 키운다
for group in optimizer.param_groups:
    group["lr"] = group["lr"] * args.init_lr_frac   # default 0.8
    group["initial_lr"] = group["lr"]
```

`init_lr_frac=0.8`. base가 *피크 LR의 0%*까지 떨어뜨려놨던 자리에서, *피크 LR의 80%*로 다시 끌어올린다. 왜 100%가 아니라 80%인가? **모델이 base pretrain 끝에서 *수렴 근처*에 있기 때문이다.** 100%로 시작하면 *수렴해둔 자리를 다시 흔들* 위험이 있다. 80%는 *충분히 크지만 안전한* 출발점이다.

`get_lr_multiplier`(`chat_sft.py:314-321`)는 어떤 스케줄을 그릴까?

```python
# scripts/chat_sft.py:314-321
def get_lr_multiplier(progress):
    if progress < args.warmup_ratio:                       # default 0.0
        return (progress + 1e-8) / args.warmup_ratio
    elif progress <= 1.0 - args.warmdown_ratio:            # default 0.5
        return 1.0
    else:
        decay = (progress - (1.0 - args.warmdown_ratio)) / args.warmdown_ratio
        return (1 - decay) * 1.0 + decay * args.final_lr_frac  # final 0.0
```

`warmup_ratio=0.0`, `warmdown_ratio=0.5`. **워밍업이 없다**. 처음부터 피크(`init_lr_frac` × base_lr)로 출발해서, 학습의 *후반 절반*에 걸쳐 0까지 떨어뜨린다. 이게 base와 다른 점이다 — base는 40 step의 짧은 워밍업이 있었다. SFT는 워밍업이 *불필요*하다. 왜? *모델이 이미 다 데워져 있다*. base pretrain 끝의 *Muon momentum buffer*와 *AdamW exp_avg/exp_avg_sq*가 그 데움의 *증거*다.

그래서 `chat_sft.py:141-149`의 *옵티마이저 warm-start*가 있다.

```python
# scripts/chat_sft.py:141-149 — optimizer state warm-start
if args.load_optimizer:
    optimizer_data = load_optimizer_state(
        "base", device, rank=ddp_rank, ...)
    if optimizer_data is not None:
        base_lrs = [group["lr"] for group in optimizer.param_groups]
        optimizer.load_state_dict(optimizer_data)
        del optimizer_data
        # pretrain ckpt의 LR(거의 0)을 *덮어쓰기 위해* 다시 base_lrs로
        for group, base_lr in zip(optimizer.param_groups, base_lrs):
            group["lr"] = base_lr
        print0("Loaded optimizer state from pretrained checkpoint "
               "(momentum buffers only, LRs reset)")
```

base 체크포인트의 *옵티마이저 state*를 통째로 불러온다. Muon momentum buffer, AdamW 1차·2차 moment, 그리고 *param_group의 메타데이터*. 그런데 param_group에는 *LR도* 들어 있다 — pretrain 끝의 *거의 0*인 LR. 그걸 그대로 두면 SFT가 안 굴러간다. 그래서 *base_lrs*를 *load 전에* 저장해뒀다가 *load 후에* 다시 덮어쓴다. *momentum만 가져오고 LR은 새로 설정*한다.

이 결정에는 *한 가지 직관*이 깔려 있다. **Muon momentum은 *방향성의 기억*이다.** 12B 토큰 동안 어떤 방향으로 파라미터가 움직였는지를 *기억*하고 있다. SFT는 *완전히 다른 task*가 아니라 *같은 모델의 다른 측면*을 가르치는 일이라 — 그 *방향성의 기억*을 *버리는 것*보다 *이어받는 것*이 합리적이다. 비유하자면, 오래 달려서 *근육이 데워진* 사람을 *완전히 식혔다가* 다시 시작시키는 것보다, *같은 페이스에서 종목만 살짝 바꿔* 이어 달리게 하는 셈이다.

Muon momentum 스케줄(`chat_sft.py:324-327`)도 짧다.

```python
# scripts/chat_sft.py:324-327
def get_muon_momentum(it):
    frac = min(it / 300, 1)
    momentum = (1 - frac) * 0.85 + frac * 0.95
    return momentum
```

처음 300 step 동안 momentum을 0.85 → 0.95로 끌어올린다. base의 warmdown 단계에서 momentum이 다시 *낮춰져* 있던 자리(0.90 근처)에서 출발해 *SFT의 안정 구간*인 0.95로 다시 올린다. 5장에서 Muon momentum이 *gradient의 방향성을 모으는 EMA의 강도*라고 했던 게 기억나는가? 그 강도를 SFT에서는 *조금 더 세게* 둔다. 데이터의 분포가 비교적 일관되니까 (대화는 *문서*보다 노이즈가 적다) momentum을 강하게 줘도 *방향이 안 흔들린다*.

## ChatCORE — 대화 능력을 *수치로* 본다

학습 루프는 base와 거의 같다. forward, backward, gradient accumulation, optimizer step, LR 갱신. 새로운 알고리즘은 없다. 그런데 *평가는 다르다*.

`chat_sft.py:363-396`이 ChatCORE의 정의다. 우리가 7장에서 익숙해진 *centered accuracy의 평균*이라는 트릭을 — *다른 task 모음*에 적용한다.

```python
# scripts/chat_sft.py:363-396 (요약)
if args.chatcore_every > 0 and (last_step or
                                (step > 0 and step % args.chatcore_every == 0)):
    model.eval()
    engine = Engine(orig_model, tokenizer)
    all_tasks = ['ARC-Easy', 'ARC-Challenge', 'MMLU', 'GSM8K',
                 'HumanEval', 'SpellingBee']
    categorical_tasks = {'ARC-Easy', 'ARC-Challenge', 'MMLU'}
    baseline_accuracies = {
        'ARC-Easy': 0.25, 'ARC-Challenge': 0.25, 'MMLU': 0.25,
        'GSM8K': 0.0, 'HumanEval': 0.0, 'SpellingBee': 0.0,
    }
    task_results = {}
    for task_name in all_tasks:
        limit = args.chatcore_max_cat if task_name in categorical_tasks \
                else args.chatcore_max_sample
        max_problems = None if limit < 0 else limit
        acc = run_chat_eval(task_name, orig_model, tokenizer, engine,
                            batch_size=args.device_batch_size,
                            max_problems=max_problems)
        task_results[task_name] = acc
    def centered_mean(tasks):
        return sum((task_results[t] - baseline_accuracies[t])
                   / (1.0 - baseline_accuracies[t]) for t in tasks) / len(tasks)
    chatcore = centered_mean(all_tasks)
    chatcore_cat = centered_mean(categorical_tasks)
```

여섯 개 task — ARC-Easy, ARC-Challenge, MMLU, GSM8K, HumanEval, SpellingBee. 7장의 CORE 22-task에서 *언어 모델링 평가*는 빠지고 — *생성*이 들어왔다. 어시스턴트가 *실제로 답을 만들어내는* 평가다.

여기서 baseline accuracy의 정의가 한 번 더 흥미롭다. ARC-Easy/Challenge/MMLU는 *4지선다*이므로 random baseline이 0.25다. GSM8K/HumanEval/SpellingBee는 *생성*이라 — *우연히 정답*이 나올 확률이 거의 0이다. 그래서 baseline 0.0. centered accuracy의 공식 `(acc - baseline) / (1 - baseline)`이 이 자리에서 *각 task의 난이도*를 자연스럽게 정규화한다.

`chatcore`(전체 6개 평균)와 `chatcore_cat`(4지선다 3개만 평균)을 *둘 다* 로그한다. 왜 둘 다인가? **생성 task는 분산이 크기 때문이다.** GSM8K accuracy가 0.05에서 0.10으로 *두 배*가 됐다고 모델이 *두 배 잘하는* 게 아니다 — 그저 *우연*일 수도 있다. 4지선다는 분산이 작아서 *추세*를 보기 좋다. 두 지표를 동시에 띄워두면 *진짜 개선*과 *우연의 출렁임*을 구분할 수 있다.

### CORE vs ChatCORE — 다리 박스

자, 그렇다면 7장의 CORE와 8장의 ChatCORE를 *나란히* 두자. *같은 centered 트릭이 어떻게 다른 자리에서 쓰이는지* 정확히 보인다.

| 지표 | 대상 모델 | task 수 | task 종류 | baseline | 어디서 계산 |
|---|---|---|---|---|---|
| **CORE** | base 모델 | 22 | 다지선다 + schema + LM | random per task (multiple choice는 1/n, schema는 1/2) | `nanochat/core_eval.py` |
| **ChatCORE** | chat 모델 (SFT/RL 후) | 6 | 4지선다 + 생성 | {ARC: 0.25, MMLU: 0.25, GSM8K: 0.0, HumanEval: 0.0, SpellingBee: 0.0} | `scripts/chat_sft.py:363-396` |

*같은 centered 트릭, 다른 task 모음, 다른 baseline.*

CORE는 *raw capability*를 잰다. base 모델은 *완성기*이므로 *옵션별 log-prob*을 비교하거나 *완성된 문장*의 PPL을 본다. 22개 task에 22개 baseline. 22번 centered, 평균. ChatCORE는 *어시스턴트로서의 능력*을 잰다. 6개 task에서 모델이 *실제로 답을 생성*한다 — 4지선다도 letter 토큰 *한 개*를 생성해서 매칭하고, GSM8K도 자유 형식 답안을 만들어 `####` 뒤의 숫자를 추출한다.

이 둘이 같이 있는 게 *책의 핵심 교훈* 하나를 보여준다. **평가 메트릭은 *모델의 모드*를 정확히 비춰야 한다.** base 모델에 ChatCORE를 들이대면 *대화하지 못하는* 모델이라 GSM8K는 0에 가깝게 나오고 *진짜 capability*를 못 본다. chat 모델에 CORE를 들이대면 — *완성 모드*가 아닌 모델이 *옵션별 log-prob* 비교에서 어색한 행동을 한다. 두 지표는 *경쟁자*가 아니라 *역할이 다른 동료*다.

7장에서 우리가 `evaluate_example`에 박힌 `seed=1234+idx`를 보며 *재현성*에 감탄했다면, ChatCORE의 6개 task도 같은 정신을 따른다. categorical_tasks에는 `chatcore_max_cat`을 (기본 -1, 즉 전체) 적용하고, 생성 task에는 `chatcore_max_sample` (기본 24)을 적용한다. 생성은 *비싸므로* — 한 문제당 모델이 자유 토큰을 수십~수백 개 만들어내야 하니까 — *24문제씩*만 본다. 그래도 *결정적인 시드*로 같은 24문제다. 책에서 우리가 *0.05*를 보면, 다른 사람의 노트북에서도 *0.05*가 나온다.

## 능력은 데이터로 가르친다 — Identity와 SpellingBee의 두 사례

이 챕터의 *큰 교훈*을 두 사례로 다시 보자. 카르파시가 nanochat discussion에 직접 올린 두 가이드다.

**사례 1 — Identity 주입 ([#139](https://github.com/karpathy/nanochat/discussions/139)).** 모델이 "너는 누구야?"에 *일관되게* 답하게 만들고 싶다고 해보자. 어떻게 할까? 코드를 *고치는* 게 아니다. **데이터를 *합성*해서 SFT mix에 추가**한다.

`dev/gen_synthetic_data.py`는 OpenRouter API를 호출해 Gemini Flash 같은 *큰 모델*에게 다양성 4축(*9 categories × 12 personas × 10 dynamics × 7 first-message styles*) sampling으로 1000편의 대화를 생성시킨다. system prompt에는 `knowledge/self_knowledge.md`의 *사실 목록*("nanochat은 카르파시가 만든 오픈소스 챗봇이다, 약 8000줄 코드다, ...")이 박혀 있다. 큰 모델이 그 사실을 *1000가지 다른 표현*으로 다시 짠다.

결과는 `~/.cache/nanochat/identity_conversations.jsonl` — JSONL 1000줄. 그걸 `CustomJSON(filepath=...)`로 두 번 SFT 믹스에 끼운다. SFT 끝나면 모델은 "I'm nanochat, an open source chatbot..."이라 *일관되게* 답한다. *코드 한 줄도 바꾸지 않았다*.

**사례 2 — SpellingBee ([#164](https://github.com/karpathy/nanochat/discussions/164)).** "How many r in strawberry?"를 작은 모델이 못 푼다. 어떻게 할까? 다시 — *코드를 고치는 게 아니라 데이터를 만든다*. `tasks/spellingbee.py`가 그 답이다. 370K 영어 단어 사전에서 단어와 글자를 뽑아 *합성 대화 80K편*을 만든다. SimpleSpelling 200K (단순 철자만, 토큰화 인지를 *데우는* 용도)를 함께 끼운다. SFT 한 사이클이면 모델이 *char-by-char 추론*을 *시작*한다.

이 두 사례의 공통점은 *워크플로*다.

1. 가르치고 싶은 능력을 *대화의 모양*으로 분해한다 — user message는 어떻게 생겼고, assistant response는 어떻게 단계적으로 흘러야 하는가.
2. 합성한다 — 큰 모델로(Identity), 알고리즘으로(SpellingBee), 또는 사람이 직접(소규모).
3. JSONL로 떨군다 — `[{"role":"user", ...}, {"role":"assistant", ...}]` 한 줄에 한 대화.
4. `CustomJSON(filepath=...)`로 SFT 믹스에 끼운다 — 또는 `tasks/X.py`에 Task 클래스로 만든다.
5. SFT 재실행. 끝.

알고리즘이 새로 등장하는 자리가 *없다*. 새 옵티마이저도, 새 attention 변종도, 새 손실 함수도 *없다*. 능력의 *증분*은 거의 항상 *데이터의 증분*이다. 12장에서 우리가 이 워크플로를 *우리 자신*에게 적용할 때, *코드를 손대지 않는다는 점*이 보일 것이다. 손대는 건 *JSONL 파일 하나*다.

## 실습 — d6로 1500 step SFT 돌리고 대화해보자

이제 손을 더럽힐 시간이다. CPU/MPS 환경에서 SFT를 한 번 굴려보자. 6장에서 만들어둔 d6 base 체크포인트를 *그대로 받아* — 80GB GPU도, 32GB RAM도, 그 무엇도 필요 없다 — SFT 1500 step을 돌린다. M3 Max에서 약 15분이다.

먼저 identity 대화를 받자. nanochat이 합성해둔 1000줄이 카르파시의 S3에 공개돼 있다.

```bash
curl -L -o $NANOCHAT_BASE_DIR/identity_conversations.jsonl \
    https://karpathy-public.s3.us-west-2.amazonaws.com/identity_conversations.jsonl
```

그리고 SFT를 돌린다 — single process로.

```bash
python -m scripts.chat_sft \
    --device-batch-size=1 --total-batch-size=16384 \
    --num-iterations=1500 \
    --eval-every=-1 --chatcore-every=-1
```

`--device-batch-size=1`이 CPU/MPS의 *마지노선*이다. d6 모델은 작아도 `lm_head logits`가 `(B, T, vocab_size)` 크기로 메모리를 잡아먹어서 그렇다. `--total-batch-size=16384`로 두면 `grad_accum_steps`가 자동 계산된다. `--eval-every=-1`, `--chatcore-every=-1`은 *평가를 끈다* — 평가 자체가 추론을 *수십 번* 돌리므로 CPU에서는 *학습보다 평가가 더 오래 걸린다*.

15분이 지나면 `chatsft_checkpoints/d6/...`에 SFT 체크포인트가 떨어진다. 이제 *대화*해보자.

```bash
python -m scripts.chat_cli
```

REPL이 열린다. 두 가지를 물어보자 — 영어 한 번, 한국어 한 번.

```
> What is the capital of France?
...

> 안녕, 너는 누구야?
...
```

자, 이제 한 가지 *정직한 박스*를 펴야 한다.

> **이 실습 결과에 대한 정직한 박스**
>
> nanochat README는 이 정확한 설정 (d6 + 5K pretrain + 1500 SFT)의 모델을 *"kindergartener level. Sometimes the model likes it if you first say Hi before you ask it questions"*라고 표현한다. 우리의 CPU 실습도 *그 정도*다.
>
> "What is the capital of France?"에 대해 무엇을 보게 될까?
>
> - 운이 좋으면 — 정말 운이 좋으면 — `Paris.`라고 한 단어 답이 나온다.
> - 더 흔하게는 `The capital of France is Paris, which is a city ...` 같은 *완성형 문장*이 나오거나, 살짝 엇나간다.
> - 가끔은 *전혀 엉뚱한 답* — "France is a country in Europe."라거나, 영어와 한국어가 섞여 나오거나 — 이 출력된다. *그게 정상이다*.
>
> 한국어 질문에 대해서는 — 거의 확실하게 *영어로 답하거나 깨진다*. SmolTalk이 영어 중심이고, identity 대화도 영어 중심이라 — 모델이 *한국어로 답하는 법*을 거의 못 배웠다. 10장에서 더 자세히 보자.
>
> 진짜 한 줄 답을 보고 싶다면 두 가지 옵션이 있다.
>
> 1. **d12로 8K step SFT를 돌린다** — A100 1장 6시간 옵션. base pretrain까지 합치면 24시간쯤 든다.
> 2. **카르파시가 공개한 speedrun d24 체크포인트를 다운로드한다** — 10장에서도 같은 체크포인트를 쓸 예정이다.
>
> 그래도 *왜 우리가 이 실습을 했는가*는 분명하다. **base 모델과 SFT 모델의 차이를 *손으로* 만져본 것**이다. base 모델은 질문을 *완성*했다. SFT 모델은 — 비록 어설프지만 — *답하려고 시도한다*. 그 시도 자체가 1500 step 안에 *주입*됐다. 그 주입의 *증거*가 우리 손에 있다.

선택 실습이 하나 더 있다. *자기 챗봇*을 미리 한 번 맛보고 싶다면 — OpenRouter API 키가 있을 때 — `dev/gen_synthetic_data.py`를 약간 손봐서 *너 자신의 정체성*으로 1000줄을 합성한 뒤 SFT를 재실행해보자. 모델이 "나는 토비다, 내가 만든 작은 챗봇이다"라고 답하는 모습을 볼 수 있다. 디테일은 12장에서 4단계 레시피로 다시 다룬다. 지금은 *그 길이 열려 있다*는 것만 기억해두자.

## 마무리 — 모방의 끝, 결과의 시작

여기까지 우리는 *모방*을 가르쳤다. SmolTalk 460K 대화에서 *어시스턴트가 어떻게 답하는지*를 baseline으로 잡았고, MMLU로 4지선다 형식을, GSM8K로 도구 호출의 본능을, SpellingBee로 토큰을 글자로 풀어내는 방법을, identity로 자아를 — 각각 *데이터의 모양*으로 가르쳤다. 모델은 *어시스턴트로서 말하는 법*을 흉내 내기 시작했다. 그 흉내가 *수치*로 ChatCORE의 6개 task에 기록된다.

여기에 *한 가지 한계*가 있다. SFT는 *결과를 가르치지 않는다*. 정확히 말하면, SFT는 *어시스턴트가 답한 토큰 한 개 한 개*에 대해 *교사 답안과의 cross-entropy*를 잰다. 그 cross-entropy가 0에 가까워지면 모델은 *교사를 정확히 모방*한다. 그런데 — *교사도 틀릴 수 있다*. 합성 데이터가 *틀린 풀이*를 포함하고 있을 수 있다. SFT 손실은 그 *틀림*까지 충실히 학습한다. 손실 함수는 *최종 답의 정오*가 아니라 *토큰의 일치*만 본다.

만약 *결과*가 옳고 그른지를 *직접* 평가해서 — 옳으면 좋은 점수, 틀리면 0점 — *그 점수 자체*로 학습을 한다면 어떨까? "정답 0/1"이라는 *지도 신호*가 모델의 *생성 결과*에 직접 박힌다면? 그게 강화학습이다. 9장의 주제다.

카르파시는 이걸 *따옴표 친* "GRPO"라고 부른다. 진짜 GRPO보다 훨씬 단순한 — REINFORCE에 가까운 — 미니멀한 구현이다. 작은 모델에서 RL은 *SFT만큼 효율적이지 않다*는 게 카르파시의 입장이지만, *그 모양*을 한 번 보고 가는 건 가치가 있다. SFT가 모방을 가르쳤다면, 9장의 RL은 *결과*를 가르친다. 어떤 한 줄 코드 변화가 학습의 *목적함수*를 통째로 바꾸는지, 함께 살펴보자.
