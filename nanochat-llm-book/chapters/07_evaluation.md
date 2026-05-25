# 7장. 우리가 만든 게 정말 GPT-2급인지 어떻게 아는가

6장의 마지막에서 우리는 loss가 떨어지는 그래프를 봤다. wandb의 `val/bpb` 곡선이 매끄럽게 흘러내리고, 그래프 옆에는 0.745라는 숫자가 떠 있었다. 가슴이 한 번 부풀어 오른다. *"내가 만든 모델이 GPT-2급에 도달했다."*

그런데 잠깐 멈춰 서보자. 우리는 *진짜로* 잘하고 있는가? 그 0.745라는 숫자는 어디서 왔고, 누가 그것을 "GPT-2급"이라고 부르기로 정했고, 그 정의는 어떤 가정 위에 세워져 있는가? loss가 떨어졌다는 사실만으로 모델의 능력을 평가하는 건 어딘가 찜찜하다. 어제 본 그래프가 매끈했다고 해서 모델이 *정말로* 더 똑똑해졌는지는 모른다 — loss가 떨어지는 동안 모델이 학습 분포의 표면적 패턴만 더 잘 외운 것일 수도 있고, 우리의 토크나이저가 우연히 자주 나오는 토큰에 더 짧은 비트를 배정한 결과일 수도 있다.

이 장은 그래서 *흥분을 가라앉히는* 챕터다. 우리가 6장에서 쌓아 올린 봉우리를 의심하고, 그 봉우리의 높이를 잴 *자*를 펴 본다. 그 자가 어떻게 만들어졌는지, 어디까지 믿을 수 있는지, 어디서부터는 *우리가 직접* 판단해야 하는지. 평가는 화려하지 않다. 평가는 *건조한 정밀함*의 일이다.

본문에서 CORE, centered, bpb, baseline, multiple_choice, schema, language_modeling 같은 영어 용어를 그대로 둔다. 의역하면 *각각의 정의가 가진 뾰족함*이 무뎌진다. 정밀한 도구는 정밀한 이름으로 부르자.

## 7.1 왜 cross-entropy loss로는 부족한가 — bits-per-byte의 등장

먼저 가장 기본적인 질문부터 던지자. 우리는 6장 내내 cross-entropy loss를 *학습의 신호*로 봤다. 그렇다면 평가도 그냥 cross-entropy loss로 하면 되지 않을까? validation set 위에서 평균 loss를 재고, 그 숫자가 낮을수록 좋은 모델이라고 말하면 되는 것 아닌가?

이 발상을 한 발짝 더 밀어보면 곧 난감해진다. 다음과 같은 상황을 가정해보자. 우리가 nanochat의 32K vocab 토크나이저로 학습한 모델 A가 있고, GPT-2의 50K vocab 토크나이저로 학습한 모델 B가 있다. 둘 다 같은 영어 텍스트 위에서 cross-entropy loss를 측정했다.

| 모델 | vocab | val loss (nats/token) |
|---|---|---|
| 모델 A (nanochat, 32K vocab) | 32,768 | 2.0 |
| 모델 B (GPT-2, 50K vocab) | 50,257 | 1.8 |

이 표만 보면 모델 B가 더 좋아 보인다. loss가 더 낮으니까. 그런데 정말 그런가?

여기에 함정이 있다. 두 모델은 *같은 텍스트*를 *다른 단위로* 자른다. nanochat의 토크나이저는 vocab이 작아서 한 토큰이 평균적으로 *더 짧은 바이트*를 담는다 — 영어 문장 한 줄을 22개 토큰으로 자를지도 모르고, GPT-2의 토크나이저는 같은 문장을 18개 토큰으로 자를지도 모른다. 토큰 수가 다르면 토큰당 평균 정보량(nats/token)이 자동으로 달라진다. **vocab이 작은 모델은 토큰당 loss가 낮아 보이는 게 *공짜로* 가능하다.** 단순히 단위가 더 잘게 쪼개져 있으니까.

그렇다면 어떻게 해야 할까? 단위를 *통일*하면 된다. 모델이 어떻게 토크나이즈하든, 우리가 비교의 기준으로 삼는 단위는 *바이트*다. 영어 텍스트 한 바이트를 우리 모델이 평균 몇 비트로 표현할 수 있는가? 이것이 **bits-per-byte (bpb)** 다.

공식은 단순하다. 모델이 예측한 모든 valid 토큰의 cross-entropy 합(`total_nats`)을, 그 토큰들이 차지하는 utf-8 바이트 합(`total_bytes`)으로 나눈다. 그리고 nat을 bit로 바꾸기 위해 `log(2)`로 나눠준다.

```python
bpb = total_nats / (math.log(2) * total_bytes)
```

이 한 줄이 `nanochat/loss_eval.py:64`에 있다. 파일 전체가 단 65줄이다 — 평가 코드가 작품의 본체보다 *얼마나 단순한지* 보여주는 작은 풍경이다.

이제 `loss_eval.py:9-65`의 `evaluate_bpb` 전체를 한 번 펴서 보자. 짧은 함수다.

```python
@torch.no_grad()
def evaluate_bpb(model, batches, steps, token_bytes):
    """
    Instead of the naive 'mean loss', this function returns the bits per byte (bpb),
    which is a tokenization vocab size-independent metric, meaning you are still comparing
    apples:apples if you change the vocab size. The way this works is that instead of just
    calculating the average loss as usual, you calculate the sum loss, and independently
    also the sum bytes (of all the target tokens), and divide. This normalizes the loss by
    the number of bytes that the target tokens represent.
    ...
    """
    total_nats = torch.tensor(0.0, dtype=torch.float32, device=model.get_device())
    total_bytes = torch.tensor(0, dtype=torch.int64, device=model.get_device())
    batch_iter = iter(batches)
    for _ in range(steps):
        x, y = next(batch_iter)
        loss2d = model(x, y, loss_reduction='none') # (B, T)
        loss2d = loss2d.view(-1) # flatten
        y = y.view(-1) # flatten
        if (y.int() < 0).any():
            # 일부 target token이 ignore_index(-1)인 경로
            valid = y >= 0
            y_safe = torch.where(valid, y, torch.zeros_like(y))
            num_bytes2d = torch.where(
                valid,
                token_bytes[y_safe],
                torch.zeros_like(y, dtype=token_bytes.dtype)
            )
            total_nats += (loss2d * (num_bytes2d > 0)).sum()
            total_bytes += num_bytes2d.sum()
        else:
            # fast path: 무시할 target이 없으므로 그대로 인덱싱
            num_bytes2d = token_bytes[y]
            total_nats += (loss2d * (num_bytes2d > 0)).sum()
            total_bytes += num_bytes2d.sum()
    # 모든 rank에서 합산
    world_size = dist.get_world_size() if dist.is_initialized() else 1
    if world_size > 1:
        dist.all_reduce(total_nats, op=dist.ReduceOp.SUM)
        dist.all_reduce(total_bytes, op=dist.ReduceOp.SUM)
    total_nats = total_nats.item()
    total_bytes = total_bytes.item()
    if total_bytes == 0:
        return float('inf')
    bpb = total_nats / (math.log(2) * total_bytes)
    return bpb
```

이 함수가 *진짜로* 하는 일은 세 가지뿐이다.

1. `loss_reduction='none'`로 한 번 forward해서 *위치별 loss*를 받는다.
2. 각 target 토큰 ID에 대응하는 *바이트 수*를 `token_bytes` 테이블에서 끌어와 곱하고 합한다. 단, "no special token, no ignore_index" 원칙을 지키기 위해 `num_bytes2d > 0` 마스킹을 한 줄로 처리한다.
3. DDP 환경이면 `all_reduce(SUM)`으로 모든 rank의 nats와 bytes를 합치고, 마지막에 `log(2)`로 나눈다.

여기서 `token_bytes`라는 이름의 1D 텐서를 한 번 짚어두자. 이 텐서는 vocab_size 길이의 정수 배열이고, 각 토큰 ID가 utf-8로 *몇 바이트*를 차지하는지 미리 계산해둔 결과다. 특수 토큰(`<|bos|>`, `<|user_start|>` 등)은 *바이트 수가 0*으로 기록돼 있다 — 평가에서 빼야 하니까. 이 사전 계산은 3장의 `tok_train.py`가 토크나이저 학습 직후에 한 번 해놓고 `token_bytes.pt`로 저장해둔다. *평가의 인프라는 이미 토크나이저 단계에서 시작돼 있었다.* 책의 흐름이 잘 짜여 있다는 작은 증거다.

> **잠깐 — 0.745라는 숫자의 의미**
>
> 영어 텍스트의 Shannon entropy는 약 1.3 bit/byte 근처라고 알려져 있다 (Shannon 1948의 인쇄 영어 실험에서 1.0~1.5 bit/byte). 이건 *완벽한 압축기*가 도달할 수 있는 이론적 하한선의 추정치다.
>
> 우리의 d24 모델은 val_bpb 0.745를 보인다. 어라, 이론적 하한선 *밑*이다.
>
> 이 모순이 신경 쓰이는가? 합리적인 의심이다. 답은 두 가지가 섞여 있다. 첫째, Shannon의 1.3은 *순수한 인쇄 영어*에 대한 추정이고 FineWeb-edu 같은 웹 코퍼스는 분포가 다르다 — 반복적이고 형식적인 패턴이 더 많다. 둘째, 그리고 더 중요하게, 우리의 0.745는 *우리 토크나이저로* 잘린 *우리 val set*에 대한 bpb이지, 텍스트 자체의 정보 이론적 한계가 아니다. 분포가 다른 두 양을 비교하고 있는 셈이다.
>
> 그러니 0.745라는 숫자를 보고 "Shannon을 이겼다"고 말하지는 말자. 다만 *같은 평가 프로토콜* 안에서 GPT-2와 우리 모델을 비교할 때, 0.745 vs GPT-2 reference의 차이는 의미가 있다. 평가는 *절대 척도*가 아니라 *비교의 척도*다. 이 두 가지를 헷갈리지 말자.

자, bpb는 cross-entropy loss를 vocab-independent 단위로 정규화하는 도구라는 게 분명해졌다. 그런데 bpb 하나로는 모델의 *능력*을 다 잴 수 없다. 모델이 "다음 토큰을 잘 예측한다"와 "모델이 *과학 문제를 푼다*"는 다른 이야기다. bpb가 낮아도 모델이 *상식 추론*을 못할 수 있고, bpb가 약간 높아도 모델이 *세계 지식*에 대해 더 정확한 분포를 가질 수 있다. 한 자만으로는 부족하다. 그래서 두 번째 자가 필요하다.

## 7.2 CORE — 능력을 22개로 쪼개 재기

CORE는 [DCLM 논문](https://arxiv.org/abs/2406.11794) (Li et al. 2024, arXiv:2406.11794)이 제안한 평가 지표다. DataComp-LM이라는 이름이 시사하듯, 이 논문은 *동일한 평가 프로토콜* 안에서 다양한 모델·데이터셋을 줄세우려는 testbed다. 그 안에서 CORE는 22개의 ICL(in-context learning) task에 대한 *centered accuracy 평균*으로 정의된다.

왜 22개일까? 왜 더 많이도, 더 적게도 아닌가? DCLM 논문이 이 22개를 고를 때 본 기준은 단순하다: *작은 모델에서도 신호가 잡히고*, *영역이 골고루 흩어져 있는* task들. 그러니까 한쪽으로 치우치지 않은, *작은 모델용 다양화된 자*다. 22개에는 reading comprehension(LAMBADA, SQuAD, CoQA), commonsense(HellaSwag, PIQA, WinoGrande), world knowledge(ARC-Easy/Challenge, SciQ), 그리고 그 사이의 schema·language modeling이 골고루 들어 있다. 한 가지 능력에 모델이 우연히 강하다고 해서 CORE 전체가 과대평가되지 않도록 분산을 만든 셈이다.

그렇다면 22개 task의 accuracy를 그냥 평균 내면 될까? 여기서 두 번째 trick이 나온다. **centered accuracy** 라는 개념이다.

문제는 이렇다. 4지선다 multiple choice task에서 *완전히 무작위로* 찍어도 25%는 맞는다. 그런 task와 *binary*(2지선다, random 50%) task와 *language modeling*(random 0%) task를 같은 평균에 넣으면 어떻게 될까? Random에서 시작하는 자리가 task마다 다르기 때문에, 단순 평균은 *task 종류의 분포*에 휘둘린다. 4지선다가 많은 평가에서는 baseline이 25% 근처로 떠 있고, language modeling이 많으면 baseline이 0% 근처로 가라앉는다. *모델의 능력*이 아니라 *task 구성*이 점수를 움직이는 셈이다.

CORE는 이 문제를 *재정규화*로 푼다. 각 task의 accuracy를 *random baseline 빼기 → (1 - random baseline)으로 나누기* 라는 두 단계로 보정한다. 이렇게 하면 random은 항상 0, perfect는 항상 1이 된다. *모든 task가 같은 축에 놓인다.* 공식은 이렇다.

```
centered_result = (acc - 0.01 * random_baseline) / (1 - 0.01 * random_baseline)
```

`0.01`이 곱해진 건 `random_baseline`이 *퍼센트 단위* (예: 25.0)로 저장돼 있기 때문이다. 0~1 스케일로 옮기는 작은 보정이다. 이 한 줄이 `scripts/base_eval.py:162`에 있다. 그 단순함이 차분하다.

자 — random은 0이 되고, perfect는 1이 됐다. 이제 22개 centered accuracy의 *단순 평균*은 비로소 *모델의 능력*을 잰다. 이것이 CORE다.

```
CORE = (1/22) * Σ centered_result_i
```

reference 값을 한 번 못 박아두자. **GPT-2 1.6B (XL)의 CORE = 0.256525**. 이 숫자가 `nanochat` README의 "time to GPT-2" 챌린지의 기준선이고, 우리 d24 모델이 0.258 근처에서 이 선을 *살짝 넘는다*는 게 이 책 전체의 클라이맥스 약속이다. 168시간 / $43,000로 훈련된 2019년의 모델이 만든 점수를, 우리는 8×H100 한 노드 위에서 *3시간*에 따라잡는다. 자가 같으니까 비교가 가능하다.

> **CORE의 한계 한 줄**
>
> CORE 0.26은 *base 모델의 raw capability*다. SFT가 가르치는 *대화 품질*이나 RL이 끌어올리는 *수학 추론*은 별도의 자(ChatCORE, GSM8K pass@k)로 잰다. 그리고 CORE가 GPT-2급이라고 해서 ChatGPT 같은 답변이 나오는 건 *아니다*. 8장의 SFT 박스에서 README의 *"kindergartener level"* 표현이 그래서 나온다.

## 7.3 `core_eval.py`의 task_type 분기 — multiple_choice, schema, language_modeling

CORE 22개 task가 어떻게 *한 코드 경로* 안에서 평가될까? 22개 task가 다 4지선다라면 단순할 텐데, 실제 분포는 그렇지 않다. ARC와 HellaSwag은 multiple choice다 — 정답 선지가 명확하게 주어진다. WinoGrande는 schema다 — *문맥*이 두 가지로 갈리고 *연결되는 문장*이 같다. LAMBADA는 language modeling이다 — 마지막 단어를 *생성*해서 맞춰야 한다. 자, 한 평가 함수가 이 세 유형을 모두 다뤄야 한다.

`nanochat/core_eval.py`는 그래서 *type별 prompt 렌더링*과 *type별 token 배치*를 모듈화한다. `:17-83`에 세 개의 렌더 함수가 나란히 있다 — `render_prompts_mc`, `render_prompts_schema`, `render_prompts_lm`. 모두 Jinja2 템플릿을 쓰는데, 각 함수가 만드는 prompt의 모양이 미묘하게 다르다.

```python
def render_prompts_mc(item, continuation_delimiter, fewshot_examples=None):
    """Render complete prompts for a multiple choice question"""
    template_str = """
{%- for example in fewshot_examples -%}
{{ example.query }}{{ continuation_delimiter }}{{ example.choices[example.gold] }}

{% endfor -%}
{{ item.query }}{{ continuation_delimiter }}{{ choice }}""".strip()
    template = Template(template_str)
    fewshot_examples = fewshot_examples or []
    context = {
        'fewshot_examples': fewshot_examples,
        'continuation_delimiter': continuation_delimiter,
        'item': item
    }
    prompts = [template.render(choice=choice, **context) for choice in item['choices']]
    return prompts
```

multiple choice는 *질문이 같고 선지가 다른* 4개의 prompt를 만든다. 4개 prompt 모두에서 *질문 부분*은 똑같고, *마지막 선지*만 다르다. 그래서 비교의 기준이 prompt들 사이의 *공통 prefix 길이*가 된다. 이 길이를 넘어가는 부분(=각 선지의 토큰들)이 "이 선지를 모델이 얼마나 자연스럽게 생성할 수 있나"를 잴 곳이다.

schema task는 반대다. *문맥*이 두 가지로 갈리고 *연결문*은 같다. 예를 들면 *"The trophy didn't fit in the suitcase because it was too small"* 과 *"The trophy didn't fit in the suitcase because it was too large"* 둘 중 어느 것이 더 자연스러운가? 이때 공통은 *suffix*(예: "...too small/large")이고, 변하는 건 *prefix*다. `render_prompts_schema`가 이걸 처리한다.

```python
def render_prompts_schema(item, continuation_delimiter, fewshot_examples=None):
    """Render complete prompts for a schema question"""
    template_str = """
{%- for example in fewshot_examples -%}
{{ example.context_options[example.gold] }}{{ continuation_delimiter }}{{ example.continuation }}

{% endfor -%}
{{ context }}{{ continuation_delimiter }}{{ item.continuation }}""".strip()
    ...
    prompts = [template.render(context=context_option, **context)
               for context_option in item['context_options']]
    return prompts
```

language modeling은 또 다르다. 문맥이 주어지고 *그다음 단어 한두 개*를 모델이 자기 토큰으로 *맞춰야* 한다 (예: LAMBADA의 마지막 단어 예측). 이 경우 prompt 두 개를 만든다 — 하나는 *continuation 없이*, 다른 하나는 *정답 continuation을 붙여서*. 두 prompt를 모두 토큰화한 뒤, 길이의 *차이*가 *모델이 자기 토큰으로 정답을 맞춰야 할 구간*이 된다.

이 세 가지 유형은 모두 *공통 prefix*나 *공통 suffix* 위에서 *다른 부분의 토큰 loss*만 보면 답을 가릴 수 있다는 공통점이 있다. `find_common_length` (`:86-101`)와 `batch_sequences_*` 함수 (`:113-141`)가 그 비교 지점을 정확하게 잘라낸다. 한 번 펴서 보자.

```python
def find_common_length(token_sequences, direction='left'):
    """
    Find the length of the common prefix or suffix across token sequences
    - direction: 'left' for prefix, 'right' for suffix
    """
    min_len = min(len(seq) for seq in token_sequences)
    indices = {
        'left': range(min_len),
        'right': range(-1, -min_len-1, -1)
    }[direction]
    for i, idx in enumerate(indices):
        token = token_sequences[0][idx]
        if not all(seq[idx] == token for seq in token_sequences):
            return i
    return min_len
```

평범한 알고리즘이다. 토큰 시퀀스들을 받아 *왼쪽부터* 또는 *오른쪽부터* 같은 토큰이 몇 개 이어지는지를 센다. multiple choice라면 *왼쪽*, schema라면 *오른쪽*. 코드 한 페이지가 *세 task 유형을 한 평가 루프 안에서 처리*하는 마법의 절반이 여기에 있다. 평가의 정밀함은 *prompt를 어디서 자를지*에 달려 있다.

다음 절에서는 *어디서 자른 토큰들의 loss*를 *어떻게 모아 정답을 가리는지* 본다.

## 7.4 `evaluate_example` — 한 문항을 평가하는 단순한 절차

`evaluate_example`이 한 문항에 대해 하는 일을 풀어쓰면 다음과 같다.

1. task type에 따라 prompt들을 렌더링하고 토큰화한다.
2. 모델의 `max_seq_len`보다 길면 *마지막에서부터* 자른다 (시작 부분에서 자르면 정답 위치가 어긋난다).
3. prompt들을 같은 길이로 padding해 `(B, T)` 텐서로 만들고 `forward_model`을 부른다.
4. *각 위치별 loss*를 받아서, 비교해야 할 *구간 평균 loss*가 가장 낮은 선지를 정답으로 고른다 (multiple choice·schema). language modeling이라면 *argmax 예측이 정답 토큰과 일치하는지* 본다.

`forward_model` (`:144-164`)을 한 번 펴서 보자. 평가용 inference는 학습용 forward와 *약간 다르다*.

```python
@torch.no_grad()
def forward_model(model, input_ids):
    """
    Take BxT tensor of token ids, return BxT tensor of losses and argmax predictions.
    The last column of losses is set to nan because we don't have autoregressive targets there.
    """
    batch_size, seq_len = input_ids.size()
    outputs = model(input_ids)
    # 한 칸 왼쪽으로 굴려서 autoregressive target 만들기
    target_ids = torch.roll(input_ids, shifts=-1, dims=1)
    losses = torch.nn.functional.cross_entropy(
        outputs.view(batch_size * seq_len, -1),
        target_ids.view(batch_size * seq_len),
        reduction='none'
    ).view(batch_size, seq_len)
    # 마지막 칸은 autoregressive target이 없으므로 nan
    losses[:, -1] = float('nan')
    predictions = outputs.argmax(dim=-1)
    return losses, predictions
```

`torch.roll`로 target_ids를 한 칸 왼쪽으로 굴려서 *각 위치의 다음 토큰*을 target으로 만든다. 학습 코드의 next-token prediction과 동일한 발상이지만, 여기서는 `reduction='none'`이므로 *위치별 loss*가 살아남는다. 그리고 마지막 칸은 *그다음 토큰이 없으니까* nan으로 채워둔다 — `mean()`에서 자동으로 빠지도록.

이제 `evaluate_example`의 마지막 부분이 깔끔해진다.

```python
if task_type == 'language_modeling':
    si = start_idxs[0]
    ei = end_idxs[0]
    predicted_tokens = predictions[0, si-1:ei-1]
    actual_tokens = input_ids[0, si:ei]
    is_correct = torch.all(predicted_tokens == actual_tokens).item()
elif task_type in ['multiple_choice', 'schema']:
    mean_losses = [losses[i, si-1:ei-1].mean().item()
                    for i, (si, ei) in enumerate(zip(start_idxs, end_idxs))]
    pred_idx = mean_losses.index(min(mean_losses))
    is_correct = pred_idx == item['gold']
```

multiple choice·schema는 *변하는 구간의 평균 loss*가 가장 낮은 선지를 모델의 답으로 고른다. *낮은 loss = 모델이 자기 분포에서 더 자연스럽게 본 텍스트*다. 한 선지의 토큰들에 모델이 *덜 놀라면* 그것이 정답이다.

language modeling은 *모델의 argmax 예측 토큰*이 *실제 정답 토큰*과 *전부* 일치해야 정답으로 친다. *생성하는 task에서는 argmax가 답이 된다.*

코드는 단순하지만 그 안에 *평가 철학*이 깔려 있다. CORE의 multiple choice는 *생성 평가*가 아니라 *NLL 비교 평가*다. 모델이 답을 *써내는* 능력이 아니라, 모델의 분포가 *어느 쪽 답에 더 무게를 두는지*를 본다. 이게 ICL(in-context learning) 평가의 표준이고, 작은 모델에서도 신호가 잡히는 이유다.

### 재현성을 만드는 한 줄 — `random.Random(1234 + idx)`

`evaluate_example` (`:168-241`)에 한 가지 작은 트릭이 더 숨어 있다. fewshot example을 뽑는 부분이다.

```python
if num_fewshot > 0:
    rng = random.Random(1234 + idx)
    available_indices = [i for i in range(len(data)) if i != idx]
    fewshot_indices = rng.sample(available_indices, num_fewshot)
    fewshot_examples = [data[i] for i in fewshot_indices]
```

`random.Random(1234 + idx)`. 한 줄이다. idx마다 *결정론적인* 시드로 fewshot example을 뽑는다. 이 시드는 *어느 머신에서 돌려도, 며칠 뒤에 돌려도, 누가 돌려도* 같은 결과를 보장한다. *재현성*은 거창한 인프라가 아니라 *이 한 줄의 결단*에서 시작된다.

왜 이 트릭이 의미가 있는가? CORE는 task별로 fewshot 수가 다르다 — LAMBADA는 0-shot, ARC는 5-shot 등. 매 평가마다 fewshot이 *다르게 뽑히면* 정확도가 ±1~2%p씩 흔들린다. 그러면 우리가 "GPT-2를 0.001 차이로 넘었다"는 주장이 *우연*인지 *실력*인지 가릴 수 없다. 평가 점수의 *신뢰 구간*이 이 한 줄로 좁아진다.

물론 시드가 1234라는 *특정 값*에 살짝 의존하는 면이 있다. 누군가 시드를 1235로 바꾸면 fewshot이 다 바뀐다. 그래도 *모든 평가가 1234를 쓰는 한*, 비교는 공정해진다. 이게 평가의 *공정성*에 대한 카르파시의 결정이다. 우리도 우리 모델을 평가할 때 이 시드를 *건드리지 말자*. 단순한 결단이 가장 오래 간다.

`1234 + idx`라는 식의 *덧셈*도 작은 디자인이다. 단순히 `idx`를 시드로 쓰면 *idx=0인 문항*과 *idx=0이지만 다른 task의 문항*이 같은 시드로 fewshot을 뽑는다. 1234라는 *task-independent offset*을 더하면 *task 안*에서는 결정론적이고, *task 사이*에서는 충돌하지 않는 인덱스 공간이 만들어진다. 한 줄짜리 트릭이지만 *재현성의 표면적*을 그대로 보여준다. 평가 코드는 *이런 작은 디자인의 합*이다.

## 7.5 `evaluate_task` — DDP에서 stride 분산 + `all_reduce(SUM)`

한 문항을 평가하는 법은 위에서 봤다. 그렇다면 *한 task의 수천 문항*을 8×H100에서 어떻게 *분산해서 평가*할까? 그리고 그 결과를 *어떻게 하나의 숫자로* 모을까?

`core_eval.py:244-263`의 `evaluate_task`가 이 일을 한다. 코드가 짧다.

```python
def evaluate_task(model, tokenizer, data, device, task_meta):
    """
    This function is responsible for evaluating one task across many examples.
    It also handles dispatch to all processes if the script is run with torchrun.
    """
    rank = dist.get_rank() if dist.is_initialized() else 0
    world_size = dist.get_world_size() if dist.is_initialized() else 1
    correct = torch.zeros(len(data), dtype=torch.float32, device=device)
    # stride the examples to each rank
    for idx in range(rank, len(data), world_size):
        is_correct = evaluate_example(idx, model, tokenizer, data, device, task_meta)
        correct[idx] = float(is_correct)
    # sync results across all the processes if running distributed
    if world_size > 1:
        dist.barrier()
        dist.all_reduce(correct, op=dist.ReduceOp.SUM)
    mean_correct = correct.mean().item()
    return mean_correct
```

20줄짜리 함수가 *분산 평가의 본질*을 다 담고 있다. 패턴이 단순하다.

1. **`correct` 텐서를 0으로 초기화**한다. 길이는 *전체 데이터 개수*. 각 rank가 *자기 인덱스에만* 1.0을 쓴다.
2. **stride 분산**: `for idx in range(rank, len(data), world_size)`. rank 0은 0, 8, 16, ...번 문항을, rank 1은 1, 9, 17, ...번 문항을 평가한다. 8개 GPU가 동시에 다른 문항을 처리하니까 *8배 빠르다*. 부하 균형이 자동이다.
3. **`all_reduce(SUM)`**: 모든 rank의 `correct` 텐서를 합친다. 각 위치는 한 rank만 1을 썼으니까, 합쳐도 *중복 없이* 누적된다. 결과는 모든 rank에 동일하게 분배된다.
4. **`mean()`**: 전체 평균. 이것이 task의 accuracy.

이 패턴이 너무 간결해서 처음 보면 *이게 다인가* 싶은데, 사실 이게 다다. DDP에서 평가 결과를 모으는 표준 트릭이고, 학습 단계에서도 같은 패턴을 본 적이 있다 (6장의 grad 합산). *학습 코드와 평가 코드가 같은 동기화 idiom을 공유한다*는 사실이 nanochat의 단정함을 만든다.

그리고 `dist.barrier()`. 이 줄이 *왜* 필요한지 한 번 짚자. `all_reduce`가 모든 rank의 텐서를 모은다고 했지만, *어떤 rank가 자기 작업을 다 끝내지 못한 상태에서* all_reduce에 들어가면 *부분 결과*가 합쳐진다. `barrier`는 모든 rank가 *for 루프를 다 돈 시점*에서 만나도록 강제한다. 정확한 결과를 위한 작은 보험이다.

### 8개 GPU에서 0.001 차이가 의미가 있는가

이 절에서 한 번 멈춰 서서 *측정의 정밀도*를 생각해보자. 한 task에 1000 examples이 있다고 가정하자. rank 0~7이 stride 8로 나눠 가지면 각 rank가 125 examples을 본다. 8×H100에서 한 example을 평가하는 데 1초가 걸린다면, 한 task는 125초에 끝난다. 22개 task면 약 46분. 빠르다.

그런데 *측정의 정밀도*는? 1000 examples 위의 binary 평가에서 ±1 example의 오차는 ±0.001 accuracy다. centered accuracy로 옮기면 *random baseline에 따라* 약 ±0.0013 정도. 그리고 22개 task의 평균이니까 *대수의 법칙*으로 CORE의 표준오차는 더 작아진다. 대략 ±0.002 정도가 *우리가 의심해야 할 노이즈 폭*이다.

우리 d24 모델이 0.258, GPT-2 reference가 0.256525. 차이는 0.0015. *노이즈 폭의 한계에 있다.* 정직하게 말하면 우리는 GPT-2를 *간발의 차로 넘었거나, 사실 비등하다*고 표현해야 한다. "확실히 능가"라는 말은 leaderboard #2 결과 (CORE 0.2690, [#481](https://github.com/karpathy/nanochat/discussions/481))처럼 *마진이 0.01 이상*일 때 쓰는 게 정직하다.

이쯤에서 한 번 호흡을 가다듬자. *왜* nanochat은 매 step마다 22개 task 전부를 평가하지 않을까? 그 답이 `--core-metric-every`와 `--core-metric-max-per-task` 두 인자에 있다. CORE 22 task를 전부 *full set*으로 돌리면 d24에서도 *수십 분*이 걸린다. 5천 step 학습 중 50번 평가하면 *수십 시간*이 추가로 든다. 평가의 *비용*과 *해상도* 사이의 trade-off다. 학습 중에는 *작은 sample*로 *자주* 평가해 곡선을 그리고, 학습 끝에 *큰 sample*로 *한 번* 평가해 *공식 보고용 숫자*를 얻는다. *학습 중 곡선의 마지막 점*과 *공식 보고 숫자*가 *다른 값*인 게 정상이다. 두 값을 *섞어 쓰지 말자*. 한 번 더 잊지 말자.

이게 *평가에 흔들리지 않는 법*의 첫걸음이다. 점수만 보지 말고 *표준오차*를 같이 보자. 7.7절에서 더 자세히.

## 7.6 짧은 박스 — CORE squad만 reference 대비 떨어진다

> **`core_eval.py:5-6`의 솔직한 TODO**
>
> nanochat의 `core_eval.py` 파일을 열면 docstring 끝에 이런 한 줄이 적혀 있다.
>
> ```python
> """
> Functions for evaluating the CORE metric, as described in the DCLM paper.
> https://arxiv.org/abs/2406.11794
>
> TODOs:
> - All tasks ~match except for squad. We get 31% reference is 37%. Figure out why.
> """
> ```
>
> CORE 22개 task 중 *21개*는 DCLM 논문의 reference 값과 거의 일치하는데, *squad* task만 우리 구현이 6%p 낮다. 카르파시도 *왜인지 모른다*. 이건 nanochat의 *알려진 평가 차이*다. 토크나이저 차이일 수도, prompt 템플릿의 미세한 띄어쓰기 차이일 수도, fewshot sampling의 random seed 차이일 수도 있다.
>
> 이 6%p가 우리의 *전체 CORE 점수*에 얼마나 영향을 줄까? 22개 task 평균이니까 약 0.27%p 정도. CORE 0.258을 0.255 정도로 낮춘다. *우리가 GPT-2 reference를 못 넘었을 수도 있다*는 의심이 한 번 더 합리적인 이유다.
>
> 우리는 이 사실을 *숨기지 말자*. 책의 평가 절에서 "speedrun이 GPT-2를 넘었다"고 말할 때는 *squad 차이*도 함께 짚어주는 게 정직하다. 그것이 평가에 대한 *정확한 자세*다.

이 박스가 좀 묘하게 느껴질 수 있다. 왜 *알려진 결함*을 챕터에 박아두는가? 책의 마케팅 카피에는 어울리지 않는 정보 아닌가? 그렇다. 그래서 본문이 *솔직하다*. 평가는 *정확한 도구*가 아니라 *정확하려고 노력하는 도구*다. 그 노력의 흔적이 코드 주석으로 남아 있고, 우리는 그것을 *외면하지 말자*.

## 7.7 평가에 흔들리지 않는 법 — 세 가지 점검표

이 절은 챕터 전체에서 가장 *실용적인* 부분이다. 평가 결과를 받아 들었을 때 *어디를 보아야 하는지*에 대한 작은 체크리스트.

### 7.7.1 첫 번째 — sample 수가 충분한가

`base_eval.py`에는 `--max-per-task` 인자가 있다. 학습 중 평가에서는 보통 `--core-metric-max-per-task=500` 정도로 설정한다 — *시간을 아끼기 위해* task별로 500 example만 본다. 500 examples에서의 binary 평가 표준오차는 약 ±2.2%p. centered accuracy로 옮기면 ±0.025 근처. 22개 평균이라도 ±0.005. *우리가 0.001 차이로 GPT-2를 넘었다*는 주장은 *500 examples 평가에서는 노이즈와 구분되지 않는다.*

그렇다면 어떻게 해야 할까? **최종 보고용 평가에는 `--max-per-task`를 풀자.** speedrun의 *마지막 평가*는 모든 task의 full set으로 돌린다. 학습 중간 평가는 빠르게, 최종 평가는 정밀하게. 둘을 *섞어 쓰지 말자*. 학습 중간의 0.255와 최종 평가의 0.256은 *비교 가능한 숫자가 아니다*.

### 7.7.2 두 번째 — baseline이 무엇인가

CORE를 본 다음 ChatCORE를 보면 점수 체계가 완전히 다르다는 걸 알게 된다. CORE는 22개 task 각각의 random baseline을 빼지만, ChatCORE는 6개 task에 대해 *각각 다른* baseline을 쓴다.

```
ChatCORE baseline = {ARC-Easy: 0.25, ARC-Challenge: 0.25, MMLU: 0.25, GSM8K: 0.0, HumanEval: 0.0, SpellingBee: 0.0}
```

GSM8K·HumanEval·SpellingBee는 *생성 task*라서 random이 0이다. 4지선다인 ARC와 MMLU는 0.25. *같은 centered 트릭, 다른 task 모음, 다른 baseline.* 8장에서 이 표를 한 번 더 본다.

핵심은 이거다. *어떤 자로 잰 점수인지*가 *점수 그 자체보다 중요하다*. 누군가 "내 모델이 ChatCORE 0.30이다"라고 말하면, 그게 *어떤 6개 task에 어떤 baseline*으로 잰 0.30인지를 확인하자. baseline이 다르면 점수의 *의미*가 다르다.

### 7.7.3 세 번째 — *체크포인트 어느 시점*인가

nanochat의 학습 루프는 매 N step마다 평가를 한다. wandb 그래프에는 *step별 CORE*가 곡선으로 찍힌다. 마지막 step의 CORE가 가장 높을까? 보통은 그렇다, 하지만 *항상*은 아니다.

학습이 발산하기 직전에 CORE가 peak를 찍고 떨어지는 경우가 있다. LR warmdown이 너무 빠르거나, warmup이 너무 짧거나, 데이터 분포가 *마지막 셰드*에서 노이즈가 많거나. 이런 경우 *마지막 체크포인트*가 아니라 *peak 체크포인트*가 *그 학습 런*의 best 결과다.

그렇다면 우리는 *어떤 체크포인트의 CORE*를 보고해야 할까? 학습 후반의 *수렴된* 체크포인트가 일반적이지만, 정직한 보고서는 *peak*와 *final*을 *둘 다* 적는다. report.md의 Summary 테이블은 final을 적지만, 평가의 *불확실성*을 한 번 더 적어두자.

> **요약 — 평가 점수를 받아 들었을 때**
>
> 1. *몇 examples로 잰 점수인가?* (`--max-per-task` 값)
> 2. *어떤 task 집합 + baseline인가?* (CORE 22 vs ChatCORE 6 vs GSM8K pass@k)
> 3. *어느 체크포인트인가?* (final vs peak vs 학습 중간)
>
> 이 세 가지를 *함께* 적지 않은 점수는 *정확하게* 의심하자. 의심은 무례가 아니라 *예의*다.

## 7.8 다리 박스 — 8장 예고

> **base 모델은 *대화하지 못한다*.**
>
> 7장에서 우리가 잰 CORE 0.258은 *base 모델의 raw capability*다. base 모델은 *다음 토큰을 잘 예측하는 기계*일 뿐, *대화하는 기계*는 아니다.
>
> "The capital of France is"이라는 prompt를 d24 base 모델에 던지면 "Paris."라고 *문장을 완성*한다. 그런데 "What is the capital of France?"라고 *질문 형식*으로 던지면? 답이 엇나간다. *질문에 답한다*는 행동을 *학습한 적이 없으니까*.
>
> 8장에서는 이 base 모델에 *대화하는 법*을 데이터로 가르친다. 9개의 special token이 *어떻게* 모델의 입에 *어시스턴트의 말투*를 박는지, SmolTalk 460K 대화가 *어떻게* 모델의 머리에 *대답하는 자세*를 새기는지 본다.
>
> 그리고 그 결과의 정직한 한계 — README가 *"kindergartener level"*이라고 부른 — 도 함께 본다. 평가가 우리에게 *진짜 능력*과 *겉모습*을 가르는 자를 줬으니, 8장의 chat 모델도 그 자로 잴 수 있다.
>
> *base 모델을 만든 것에 만족하고 끝낼 수도 있다. 하지만 그건 ChatGPT를 만든 게 아니다.* 8장으로 함께 넘어가자.

## 마무리 — 평가는 정밀함의 일

이 챕터에서 우리는 평가의 *두 자*를 펴봤다. **bits-per-byte**는 vocab을 바꾼 모델들을 *공정하게* 비교하기 위한 단위 통일 도구다. cross-entropy loss를 *바이트당 비트*로 정규화하면 32K vocab의 우리 모델과 50K vocab의 GPT-2가 같은 축에서 만난다. **CORE**는 22개 ICL task의 *centered accuracy 평균*으로 *base 모델의 raw capability*를 한 숫자에 담는다. centered 트릭이 random baseline에 묶이지 않는 공정한 자를 만든다.

조금 더 풀어 짚어두자. 처음 평가 코드를 펼쳐 보는 독자라면 *왜 이렇게까지 단위에 집착하는가* 싶을 수 있다. *bpb 한 줄짜리 공식이 그렇게 중요한가? centered accuracy의 보정 한 줄이 그렇게 중요한가?* 그렇다. 평가의 한 줄이 어긋나면 *비교가 무너진다*. 두 모델이 같은 점수를 보고하는데 한쪽이 32K vocab이고 다른 쪽이 50K vocab이면, 우리는 *모델의 능력*이 아니라 *토크나이저의 형태*를 비교하고 있는 셈이다. CORE의 22개 task에서 한 task만 random baseline이 잘못 적용되면, 그 task 하나가 *전체 평균을 한쪽으로 기울인다*. 평가의 *디테일에 대한 집착*은 *결벽*이 아니라 *공정함의 비용*이다. 그 비용을 치를 가치가 있다.

코드의 단순함이 다시 한 번 차분하다. `evaluate_bpb`는 65줄, `evaluate_task`는 20줄. 분산 평가의 본질은 *stride + all_reduce* 두 줄이고, 재현성의 본질은 `random.Random(1234 + idx)` 한 줄이다. 평가의 *깊이*는 *수십 줄의 코드* 안에 다 들어 있다. 화려함이 아니라 *정직함*이 이 파일들의 성품이다.

평가에 흔들리지 않는 자세도 함께 익혔다. *몇 examples로 잰 점수인지*, *어떤 baseline 위의 점수인지*, *어느 체크포인트의 점수인지*. 이 세 가지를 *함께* 적지 않은 점수는 정직하지 않다. 우리의 0.258이 GPT-2 reference 0.256525를 *간발의 차로 넘었다*고 정확하게 말할 수 있는 자세 — 그것이 평가의 정밀함이다.

그리고 잊지 말자. **CORE 0.26은 *raw capability*이지 *대화 품질*이 아니다.** 우리 d24 모델은 GPT-2급의 *지식 분포*를 갖지만, 그 지식을 *대화의 모양*으로 *내놓는* 법은 아직 모른다. 8장에서 이 base 모델에 *대화*를 가르친다. SFT라는 이름의, *데이터로 능력을 주입하는* 두 번째 학습이다.

그래프 위에서 0.745 옆에 0.258이라고 적혀 있는 작은 두 숫자가, *어떤 코드와 어떤 가정 위에서 떠 있는지* 이제 우리는 안다. 그 자가 우리 손에 있다.

다음 장으로 가자.

---

## 실습 박스 — d6 (또는 d24) base 체크포인트의 평가

> **[CPU/MPS 20분 또는 GPU 5분]**
>
> 6장 실습에서 만든 d6 base 체크포인트 (또는 다운로드한 speedrun d24 체크포인트)로 `base_eval.py`를 직접 돌려 val_bpb·CORE 값을 *우리 손으로* 찍어보자.
>
> ```bash
> # CPU/MPS 환경 (d6, CORE 평가 비활성화 — 신호가 너무 약하니까)
> python -m scripts.base_eval --model-tag d6 \
>     --device-batch-size=4 \
>     --max-per-task=-1 \
>     --eval-bpb-only \
>     --split-tokens=524288
>
> # GPU 환경 (d24, CORE 평가 활성화)
> torchrun --nproc_per_node=8 -m scripts.base_eval \
>     --model-tag d24 \
>     --device-batch-size=16 \
>     --max-per-task=500
> ```
>
> 출력을 받아 보자. 본문의 표와 비교해보자.
>
> | 환경 | model | val_bpb | CORE |
> |---|---|---|---|
> | CPU/MPS, runcpu | d6 | 약 1.5~1.8 | (평가 안 함) |
> | GPU spot, speedrun | d24 | 약 0.745 | 약 0.258 |
>
> d6에서 val_bpb가 1.5~1.8이 나오면 *정상*이다. d6은 *장난감*급이고 12B 토큰을 보지 못했다. 그래도 *평가 코드 경로*는 똑같이 밟는다 — 우리가 책에서 본 그 함수들이 진짜로 돌아간다.
>
> d24에서 CORE 0.258 근처가 나오면 *축하한다*. 0.260이 나오면 *기쁘게 보고하자*. 0.250이 나오면 *seed가 어떻게 됐는지, max-per-task가 어떤 값이었는지* 한 번 더 점검하자. 평가는 *예외 없이 노이즈를 동반*한다.
>
> 이 한 번의 실험이 6장의 봉우리를 *증명*하는 마지막 발걸음이다.
