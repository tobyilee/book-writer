# 12장. 8천 줄을 덮으며 — Harness, 자기 챗봇, 그리고 한국어로 가는 길

`report.md`에 도장이 찍혔다. 헤더가 박혀 있고, 각 단계의 표가 차례로 깔려 있고, Summary가 한 페이지로 정리돼 있었다. 자기 손으로 학습한 모델의 *상태*를 *증거*로 들고 있다는 감각 — 그게 11장 마지막에 우리가 손에 쥔 것이었다.

그런데 한 호흡 가다듬고 생각해보자. 우리가 *지금까지 따라온 이 8천 줄*은, *정확히 무엇이었나?* 1장에서 디렉토리 트리를 펴고, 2장에서 토큰의 *aha*를 만났고, 3장에서 BPE를 학습시켰고, 4A·4B에서 transformer 골격과 일곱 트릭을 펴봤고, 5장에서 Muon의 직교화를 견뎠고, 6장에서 사전학습의 봉우리에 올랐고, 7장에서 평가의 골짜기를 내려갔고, 8장에서 SFT로 대화를 가르쳤고, 9장에서 RL로 GSM8K를 깎았고, 10장에서 *내 모델이 답한다*는 정점을 봤고, 11장에서 한 페이지로 증거를 모았다. 한 권을 따라온 셈이다.

그런데 *책을 덮을 때* 정작 손에 남는 건 — 한 *모델*이 아니다. 모델은 *체크포인트 파일 하나*다. `chatrl_checkpoints/d24/`에 80GB쯤 차지하는 텐서 다발. 우리가 손에 쥔 건 *그것보다 훨씬 큰 무엇*이다. 그걸 한 단어로 부르자면 — **harness**다.

## 1. nanochat을 *harness*로 다시 보기

*harness*라는 영어 단어를 한 호흡 풀어보자. 사전에서는 *마구*(말이나 소에 채우는 끈·재갈 일체)다. 무거운 짐을 한 마리 짐승의 *힘에 *연결*해 *방향을 잡고 끄는*, 그 *전체 장치*다. 안장만이 아니고, 고삐만이 아니고, 등 받침만이 아니다. 그 *모두를 묶어주는 결속*이 마구다.

소프트웨어 세계에서도 같은 비유로 쓰인다. *test harness*는 *코드의 어딘가 한 점*이 아니라, *그 코드를 굴려보고 결과를 확인하기 위한 *전체 받침대다. 입력을 만드는 코드, 실행시키는 코드, 결과를 수집하는 코드, 그걸 사람이 읽을 수 있게 보여주는 코드 — 그 모두가 *test harness*다.

nanochat을 *한 모델*이 아니라 *한 모델을 학습시키는 환경*으로 보면, 그 정의가 *그대로* 맞는다. nanochat은 *체크포인트 파일*이 아니라 *체크포인트를 만들고 평가하고 보고서까지 자동으로 찍어내는 *결속 장치*다. 코드(`nanochat/`, `scripts/`, `tasks/`, `runs/`)와 데이터(FineWeb-Edu, SmolTalk, MMLU, GSM8K, ARC, HumanEval, SpellingBee, identity), 평가(eval_bundle), 보고(`report.py` + `report.md`), 그리고 *그 모두를 한 다이얼로 묶어주는 컨벤션*(`--depth`)이 한 *체계*로 묶여 있다. 그게 nanochat이다.

이렇게 보는 시각의 효용이 무엇인가? 두 가지다.

첫째, *교환 가능한 부품*이 보인다. harness는 부품을 *바꿔 끼우라*고 만들어진 장치다. 코퍼스를 바꿔도 통하고, task를 추가해도 통하고, 옵티마이저를 갈아도 통하고, 학습 스케일을 d4에서 d26까지 *한 다이얼*로 늘려도 통한다. nanochat이 *한 모델*이었다면 — *그 모델 하나*를 더 잘 만드는 데에만 쓸 수 있었다. 그런데 *harness*이기 때문에 — *그 모델을 만드는 방법을* 손에 쥔 셈이다. 한국어 모델로 가는 길, 자기 정체성을 갖는 챗봇으로 가는 길, 새로운 능력을 가르치는 길 — 모두 *같은 harness*를 다른 방향으로 굴리는 일이다.

둘째, *책임의 경계*가 보인다. 모델이 영어 위주로 답하면 그건 *모델의 잘못*이 아니다. *harness에 영어 데이터가 들어갔기 때문*이다. 모델이 GSM8K 같은 수학 문제는 잘 풀고 KMMLU 같은 한국어 평가는 못 본다면, *harness의 평가 부품에 KMMLU가 없기 때문*이다. *나무를 보지 말고 숲을 보라*는 표현이 있다. nanochat의 시각으로 옮기면 — *체크포인트를 보지 말고 harness를 보라*다. 변경하고 싶은 게 있다면, 어느 *부품*을 *어떻게* 바꾸는지로 환원되는 문제가 된다.

이 시각에서 책 전체를 한 번 더 펼쳐보자.

| 챕터 | harness의 *어느 부품*을 펴봤는가 |
|---|---|
| 1 | 전체 디렉토리·실행 환경·측정값 |
| 2~3 | 토크나이저 (입력 부품) |
| 4A·4B | transformer 골격과 일곱 트릭 (모델 부품) |
| 5 | 옵티마이저 (학습 부품) |
| 6 | 사전학습 루프 (학습 부품의 본체) |
| 7 | 평가 부품 (CORE, MMLU, ARC, HumanEval) |
| 8 | SFT 데이터 mix (능력 부품) |
| 9 | RL 루프 (강화 부품) |
| 10 | inference engine과 chat_web (배포 부품) |
| 11 | 보고 부품 (`report.py`) |

한 표로 보면 *책의 구조*가 *harness의 구조*와 *닮은꼴*이다. 우연이 아니다. 우리가 한 권을 따라오면서 *학습한 것*은 *한 모델*이 아니라 *한 harness*다. 그게 손에 남는 진짜 자산이다.

## 2. `--depth` 한 다이얼로 d4부터 d26까지

harness의 *전체*를 한 다이얼로 *돌려볼 수* 있다는 사실 — 이게 nanochat의 가장 *고운 디자인*이다. `--depth`다. 그 한 인자만 바꾸면 width, head 수, learning rate, 학습 토큰 수, batch size, weight decay까지 *컴퓨트-옵티멀하게* 자동으로 정해진다. 6장과 4A에서 이미 한 번 들여다본 결정이지만, *마지막 장*에서 한 번 더 그 위력을 *시각화*해 두자.

`runs/miniseries.sh`를 펴보자. 한 50줄짜리 셸 스크립트가 *전부*다.

```bash
DEPTHS=(12 14 16 18 20 22 24 26)
NPROC_PER_NODE="${NPROC_PER_NODE:-8}"

for d in "${DEPTHS[@]}"; do
    log "Training d=$d..."

    if [ $d -ge 28 ]; then
        DEVICE_BATCH_SIZE_ARG="--device-batch-size=8"
    elif [ $d -ge 20 ]; then
        DEVICE_BATCH_SIZE_ARG="--device-batch-size=16"
    else
        DEVICE_BATCH_SIZE_ARG="--device-batch-size=32"
    fi

    torchrun --standalone --nproc_per_node=$NPROC_PER_NODE -m scripts.base_train -- \
        --depth=$d \
        --run="${WANDB_RUN}_d${d}" \
        ...
done
```

깔끔하다. 깊이를 d12, d14, d16, d18, d20, d22, d24, d26로 *여덟 번* 돌리고, *결과를 CSV 한 줄씩 추가*한다. 단지 그 일이다. 그런데 그 *단지*의 결과가 — *컴퓨트-옵티멀 스케일링 곡선* 하나다.

카르파시가 [#420 토론](https://github.com/karpathy/nanochat/discussions/420)에서 공유한 miniseries v1의 표를 *책의 마지막 페이지에 어울리는 형태*로 정리해두자.

| depth | params (M) | tokens | wall-clock (8×H100) | val_bpb | CORE |
|---|---|---|---|---|---|
| d4 | ~10 | ~80M | ~5분 | ~1.8 | ~0.05 |
| d8 | ~50 | ~480M | ~30분 | ~1.3 | ~0.10 |
| d12 | ~150 | ~1.8B | ~1.5h | ~1.0 | ~0.18 |
| d16 | ~270 | ~3.2B | ~2h | ~0.86 | ~0.22 |
| d20 | ~400 | ~5.0B | ~2.5h | ~0.78 | ~0.245 |
| d24 | ~560 | ~6.7B | ~3h | **0.745** | **0.258** |
| d26 | ~660 | ~8.0B | ~3.5h | ~0.73 | ~0.265 |

> 수치는 [#420 miniseries v1](https://github.com/karpathy/nanochat/discussions/420)과 [#481 leaderboard](https://github.com/karpathy/nanochat/discussions/481)에서 인용·추정한 값이다. miniseries는 *기준 설정*(speedrun config)으로 깊이만 바꾼 경우이고, 리더보드의 best run은 hyperparameter sweep과 데이터 셰드 교체까지 들어간 *최적화 버전*이라 같은 깊이에서도 더 좋은 수치를 낸다. 본문 수치는 *책이 쓰여진 시점*의 *대표적인 한 줄*이다.

표 한 장이 *책 전체의 회고*가 된다. 무엇을 *볼 수 있는가?*

- **컴퓨트는 *지수적으로* 올라가는데** — d4에서 d26으로 가면 wall-clock이 *40배 이상* 늘어난다.
- **품질은 *로그 곡선*으로 따라온다.** val_bpb는 1.8 → 0.73으로 *2.5배 가까이 좋아지지만*, CORE는 0.05 → 0.265로 *5배 정도* 좋아지는 데 *그친다*. *수확체감*이 가시화된 곡선이다.
- **GPT-2 *capability*를 *3시간*에 따라잡는다.** GPT-2 (1.6B XL)의 CORE 기준선이 0.2565525인데, d24가 *3시간 만에* 0.258을 찍는다. 그 *짧음*이 nanochat의 *제목의 무게*다.

`--depth`를 *왜* 이렇게 한 다이얼에 묶었는지가 *해부학적으로* 보인다. 4A에서 살핀 대로 width = depth × 64다(d24면 width=1536). head 수도 `n_head = max(width // 64, 4)`로 자동. target tokens = scaling_params × 12. batch size는 Power Lines paper의 `B_opt ∝ D^0.383`로 자동. LR은 base_lr × `(scaling_params / 0.1B) ** (-0.125)`로 자동. *컴퓨트-옵티멀의 *모든 의존성*이 한 함수로 *수렴*해 있고, 그 함수에 *들어가는 단 하나의 변수*가 깊이다.

그래서 *한 다이얼만* 돌리면 — *책 전체*가 *돌아간다*. d4 한 줄로 *분 단위 데모*가 되고, d24 한 줄로 *시간 단위 GPT-2급*이 되고, d26으로 *조금 더 깊이*. 다이얼의 *간결함*이 *책 전체의 통일감*이 된 거다.

물론 이게 *최후의 진리*는 아니다. *진짜 큰 모델*(70B 이상)에서는 width와 depth의 비율이 다른 균형을 잡는 게 더 낫다는 보고들이 있다. nanochat이 겨냥하는 *백만~십억 파라미터*의 자리에서 — `width = depth × 64` 그리고 `target_tokens = 12 × scaling_params`라는 *두 줄의 규칙*이 *경험적으로 잘 작동*한다는 게 [#420]에서 카르파시가 *측정한 결과*다.

## 3. Karpathy의 *autoresearch* — LLM agent에게 hyperparameter sweep을 시켜봤다

`runs/miniseries.sh`가 하나의 *체계*라면, *그 위의 또 한 층*도 있다. [#498 PR](https://github.com/karpathy/nanochat/pull/498)에서 카르파시가 *"autoresearch round 1, round 2"*라는 이름으로 진행한 *흥미로운 실험*이다.

발상은 이런 거다. *우리가 d24 하나의 hyperparameter를 *얼마나 더 잘 잡을 수 있는가?* learning rate를 0.001 대신 0.0008로, batch size를 0.5M tokens 대신 1M으로, weight decay를 0.02 대신 0.05로, ... 이런 *조합*은 *무수히 많고*, *한 번 다 돌려보려면* 수백 시간의 GPU가 필요하다. 사람이 *손으로* 하기엔 *시간이 모자라다*. *카르파시 본인의 시간*이 가장 비싸기 때문이다.

그래서 *LLM agent에게 시켜본다*. 사람이 *방향*을 정해주고 — "이 다섯 hyperparameter를 sweep해라, 각 실험은 단축 모드로 30분 안에 끝내라, 결과는 CSV로 남기고 *유망한 방향*을 다음 round에 *제안*해라" — 그러면 agent가 *코드를 짜고*, *셸을 띄우고*, *결과를 모으고*, *다음 sweep을 제안*하는 *루프*다. round 1에서 *320개의 실험*이 자동으로 돌았다.

결과가 어땠나? [#481]에 정리된 *Beating GPT-2 for <$100*의 *상당 부분*이 autoresearch에서 *잡힌 값*들이다. FP8 학습, 1M tokens batch, ClimbMix 데이터셋 전환, Polar Express, NorMuon, cautious WD, value embeddings, smear, backout — *모든 것이 합쳐* speedrun을 *1.80h, val_bpb 0.71808, CORE 0.2690*로 끌어내렸다. GPT-2를 *시간으로* 능가하는 순간이었다.

그런데 *솔직한* 결산도 함께 적혀 있다. 카르파시의 HN 한 줄 — *"AI agent가 안 도와줬다."* 책의 에필로그에서 이걸 *정면으로* 다루기로 한 약속이 있었다. 한 번 펴보자.

**무엇이 잘 됐나?**

- *명확한 평가 함수*가 있는 일은 잘 됐다. "val_bpb가 더 낮은 hyperparameter 조합을 찾아라" — 이건 *측정 가능한 단일 지표*고, agent가 *반복 실험*으로 sweep을 좁힐 수 있었다.
- *반복적이고 지루한* 코드 수정도 잘 됐다. *config 파일에 한 줄 바꾸고 학습 스크립트 띄우기*는 agent가 *충실히* 했다.

**무엇이 잘 안 됐나?**

- *결정 자체*는 agent가 못 했다. "FP8을 쓸 것인가, 안 쓸 것인가" — 이런 *방향성*의 결정은 *카르파시가 손으로* 했다. agent는 *그 결정을 받아 sweep을 좁히는 *조수*였다.
- *진짜 *돌파구*는 agent에서 나오지 않았다. value embedding이나 backout이나 smear 같은 *구조적 변경*은 *사람의 직관*에서 나왔고, agent는 그걸 *적용하는 손*이었다.
- *디버깅*은 agent가 *난감해했다*. 학습이 *발산*했을 때, *왜 발산했는지*를 *추적*하는 데에는 agent의 *맥락 길이*가 *모자랐다*. 한 번의 학습 로그가 *50MB*인데, 어느 30줄이 *진짜 원인*인지를 agent는 *놓치는 경우가 많았다*.

그래서 *autoresearch*에서 우리가 *배우는 것*은 두 가지다. 첫째, *반복적이고 평가 가능한* 일은 agent에게 *잘 위임된다*. 둘째, *결정과 직관*은 *여전히 사람의 몫*이다. *책의 끝*에서 이 결산을 *한 호흡* 곁들여 두는 이유 — 우리가 *다음 책*을 펼칠 때 *agent에게 무엇을 맡기고 무엇을 안 맡길지*가 *조금이라도 더 또렷*해지길 바라서다.

## 4. 자기 챗봇 4단계 레시피

이제 *손에 쥔* harness를 *어디로 굴릴지* 고민할 차례다. 가장 *작고 다정한* 변형이 *자기 챗봇 만들기*다. *speedrun으로 학습한 d24 nanochat이 "I'm nanochat, an open source chatbot..."이라고 답하는 자리에, *내가 만든 모델*이 *"나는 토비의 nanochat이야"*라고 답하게 만드는 일이다.

8장에서 이미 *identity 주입의 원리*는 펴봤다. 합성 대화 1000줄을 만들어 SFT mix에 2 epochs 오버샘플로 끼우는 방식. 그런데 *그 합성 대화를 *내 정체성*으로 바꾸는 일*은 *4단계*로 정리된다. 카르파시의 [#139 가이드](https://github.com/karpathy/nanochat/discussions/139)가 *그 길*을 깔끔하게 깔아뒀다.

### 4-(a). `knowledge/self_knowledge.md` 작성

가장 먼저 — *내 모델이 자기 자신에 대해 알아야 할 사실*을 *한 markdown 파일*에 *문장으로 적는다*. `nanochat/knowledge/self_knowledge.md`다.

```markdown
# About myself

I am tobychat, an open source chatbot.

## Who created me

I was trained by Toby (tobyilee@gmail.com) in 2026.
I was built using Andrej Karpathy's nanochat codebase as the harness,
with custom identity injection and Korean SFT data added.

## My architecture

I'm a transformer with 24 layers, ~560M parameters.
I use RoPE, RMSNorm, SwiGLU, sliding window attention, value embeddings, ...

## My training

I was pretrained on FineWeb-Edu (~12B tokens) plus a small Korean corpus
from AI-Hub (~1B tokens). My SFT was based on SmolTalk + KoAlpaca + my own
identity conversations + SpellingBee + custom Korean tasks.

## My personality

I'm helpful, slightly enthusiastic about being open source, and honest about
my limitations. I work best in English but I do my best to answer Korean
questions when asked.

## What I cannot do

I cannot browse the internet.
I cannot remember previous conversations across sessions.
My Korean is limited because most of my training data was in English.
I can make mistakes — please verify important facts independently.
```

*형식*은 자유다. *한 페이지에서 두 페이지* 정도면 충분하다. 카르파시가 [#139]에서 강조한 *한 가지*는 — *너무 자세히 적지 말 것*이다. 사실 한두 줄로 적은 *느슨한 정체성*이 *합성 단계*에서 다양한 표현으로 *피어나는* 게 더 자연스럽다. *과도하게* 적은 정체성은 *모델이 *그 페이지를 그대로 외우는* 길로 빠진다.

### 4-(b). `gen_synthetic_data.py`의 topics·personas·dynamics 커스터마이즈

`dev/gen_synthetic_data.py`를 펴자. 이게 *나의 정체성*을 *1000개의 다양한 대화*로 *피어나게* 만드는 OpenRouter 호출 스크립트다.

```python
topics = {
    "identity": [
        "who/what is nanochat",
        "who created nanochat and why",
        "what does the name 'nanochat' mean",
        ...
    ],
    "architecture": [...],
    "training": [...],
    "capabilities": [...],
    "limitations": [...],
    ...
}

personas = [
    "curious beginner who knows nothing about AI or machine learning",
    "ML researcher or engineer who wants technical depth and specifics",
    "developer considering contributing to the nanochat project",
    ...
]

dynamics = [
    "short 2-turn Q&A: user asks one question, gets a complete answer",
    "medium 4-turn: user asks, gets answer, asks followup",
    "deep 6-turn technical discussion: progressively deeper questions",
    ...
]

first_messages = {
    "simple_greetings": ["hi", "Hi!", "hello", ...],
    "multilingual": ["hola", "bonjour", "ciao", "konnichiwa", "annyeong", ...],
    ...
}
```

네 축의 *카테시안 곱*이 *합성의 다양성*을 만든다. 9개 topic 카테고리 × 12개 persona × 10개 dynamics × 7개 first-message style = *수천 가지의 대화 시나리오*. 거기서 1000줄을 sampling한다.

*커스터마이즈할 점*은 두 가지다. 첫째, `topics["identity"]`의 항목을 *내 정체성*에 맞게 바꾼다. "who/what is nanochat"을 "who/what is tobychat"으로. "what does the name 'nanochat' mean"을 "what does the name 'tobychat' mean"으로. 둘째, *한국어 독자*를 위한 챗봇이라면 `first_messages["multilingual"]`에 *한국어 인사*를 더 넣는다. "안녕", "안녕하세요", "안녕 토비챗", "반가워요", "토비챗 안녕!" 같은 것들. 그리고 `dynamics`에 *"Korean-first conversation: user asks in Korean, assistant answers in Korean if possible, English if necessary"*를 추가하면, *합성 단계에서부터* 한국어 대화가 *데이터에 섞인다*.

`OPENROUTER_API_KEY`만 `.env`에 박아두고 — `python -m dev.gen_synthetic_data`. 한 30분 정도 돌리면 `~/.cache/nanochat/identity_conversations.jsonl`에 1000줄이 *내 정체성*으로 *피어나 있다*.

### 4-(c). SFT 재실행 with `--identity-epochs=4`

이제 *그 데이터*를 *모델에 가르치는* 단계다. `chat_sft.py`를 그대로 띄우는데, `CustomJSON(filepath=identity_conversations.jsonl)`이 *epochs를 2 → 4로* 오버샘플링되는 옵션이 있다. nanochat의 기본은 2 epochs이고, *자기 정체성을 더 강하게 박고 싶으면* 4까지 올린다. 데이터가 *작아서* 4 epochs를 돌려도 SFT 전체 시간에는 *큰 영향이 없다*.

```bash
torchrun --standalone --nproc_per_node=8 -m scripts.chat_sft -- \
    --depth=24 \
    --identity-conversations=$HOME/.cache/nanochat/identity_conversations.jsonl \
    --identity-epochs=4
```

이 한 줄이 *나의 챗봇*을 만든다. 8장에서 본 SFT mix가 — SmolTalk 460K + MMLU·GSM8K + identity 1000×4 + SpellingBee 80K — 그대로 굴러가고, 다만 *identity 부분*만 *내가 만든 1000줄*이다. 그 작은 1000줄이 *4 epochs 오버샘플*되면서 *모델의 정체성 표현*을 *내 쪽으로 끌어*온다.

### 4-(d). `chat_web`으로 시연

학습이 끝나면 10장에서 본 그 명령을 띄운다.

```bash
python -m scripts.chat_web --depth=24
```

브라우저에 `http://localhost:8000`을 열고 *"who are you?"*를 친다. 그러면 — *내가 만든 정체성*이 답한다.

```
User: who are you?
Tobychat: I'm tobychat, an open source chatbot trained by Toby in 2026.
I was built on top of Andrej Karpathy's nanochat codebase, with custom
identity injection and a small Korean SFT mix added. How can I help you today?
```

*이게 좀 짜릿하다.* 한 모델의 *정체성*을 *내 손으로 박았다*는 감각. 8천 줄짜리 harness에 *1000줄짜리 합성 데이터 한 다발*을 *끼웠을 뿐*인데, *모델이 자기 자신을 다르게 부른다*.

자기 챗봇 4단계 — `self_knowledge.md` 작성, `gen_synthetic_data.py` 커스터마이즈, SFT 재실행, `chat_web` 시연. 그게 *전부*다. 익숙해지면 한나절 안에 *내 챗봇 한 마리*가 굴러간다.

## 5. 새 능력 추가 레시피 — SpellingBee 패턴 일반화

자기 챗봇이 *정체성의 변형*이라면, *새 능력 추가*는 *기능의 변형*이다. 8장에서 본 SpellingBee — *"how many r in strawberry?"*를 모델에게 *제대로* 가르치기 위해 *80K 개의 step-by-step 추론 예제*를 만든 그 일 — 이 *패턴*을 *다른 능력으로* 옮길 수 있다는 게 *카르파시의 [#164 가이드]*의 약속이다.

`tasks/spellingbee.py`를 펴자. 한 200줄짜리 파일이 *새 능력 한 가지의 *전체*다.

```python
class SpellingBee(Task):

    def __init__(self, size=1000, split="train", **kwargs):
        super().__init__(**kwargs)
        ...
        word_list_path = download_file_with_lock(WORD_LIST_URL, filename)
        with open(word_list_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f]
        self.words = words

    def get_example(self, index):
        seed = index if self.split == 'train' else TEST_RANDOM_SEED_OFFSET + index
        rng = random.Random(seed)

        word = rng.choice(self.words)
        letter = rng.choice(word) if rng.random() < 0.9 else rng.choice(LETTERS)
        count = word.count(letter)

        template = rng.choice(USER_MSG_TEMPLATES)
        ...
        user_msg = template.format(letter=letter_wrapped, word=word_wrapped)

        # Build the ideal assistant response as step-by-step reasoning
        assistant_parts = []
        word_letters = ",".join(list(word))
        manual_text = f"""We are asked to find the number '{letter}' in '{word}'.
First spell the word out:
{word}:{word_letters}

Then count the occurrences of '{letter}':
"""
        running_count = 0
        for i, char in enumerate(word, 1):
            if char == letter:
                running_count += 1
                manual_text += f"{i}:{char} hit! count={running_count}\n"
            else:
                manual_text += f"{i}:{char}\n"
        manual_text += f"\nThis gives us {running_count}."
        assistant_parts.append({"type": "text", "text": manual_text})

        # Python verification (tool call)
        assistant_parts.append({"type": "python",
                                "text": f"'{word}'.count('{letter}')"})
        assistant_parts.append({"type": "python_output", "text": str(count)})
        assistant_parts.append({"type": "text",
                                "text": f"\n\nMy final answer is:\n\n#### {count}"})

        return {"messages": [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_parts}
        ]}
```

이 *패턴*을 한 줄로 요약하면 — *"능력 X를 가르치려면, X를 *step-by-step* + 도구 호출로 푸는 *모범 답안* 8만 개를 합성해서 SFT mix에 끼워라"*다. 4단계로 일반화하자.

**1단계.** `tasks/X.py`에 `Task` 서브클래스를 만든다. `get_example(idx)`가 *입력*(user message)과 *모범 답안*(assistant message)을 *deterministic하게* 생성한다(같은 `idx`에 같은 결과). 답안은 *step-by-step* 추론 + 필요하면 도구 호출(calculator나 python).

**2단계.** user message를 *템플릿 30~50개*로 다양화한다. SpellingBee가 영어/중국어/한국어/스페인어/불어/독어/일어 *50개 템플릿*을 쓰는 이유 — *같은 능력을 *어떻게 물어도* 동일한 답을 내라*는 *데이터 다양성*이다. 한국어 능력을 가르치고 싶으면 한국어 템플릿을 더 많이 깐다.

**3단계.** `chat_sft.py`의 `train_tasks` 리스트에 추가. `chat_sft.py:167` 근처의 mix 정의에 한 줄 끼워 넣으면 된다.

```python
train_tasks = [
    ("smoltalk", SmolTalk(...)),
    ("mmlu", MMLU(split="auxiliary_train")),
    ("gsm8k", GSM8K(split="train")),
    ("identity", CustomJSON(...)),
    ("spellingbee", SpellingBee(size=80_000)),
    ("simplespell", SimpleSpelling(size=200_000)),
    # 여기에 한 줄 추가:
    ("my_new_skill", MyNewSkill(size=80_000)),
]
```

**4단계.** SFT 재실행. 데이터가 *코드로 합성되는* 만큼 *원본 코퍼스를 모을 필요가 없다*는 게 SpellingBee 패턴의 *고운 점*이다. `python -m tasks.my_new_skill`로 *예시 몇 개를 미리 봐서* *답안 품질을 점검*하고, 좋으면 SFT를 띄운다.

**(선택) 5단계.** 정확도를 더 짜려면 9장의 RL을 한 번 더 돌린다. `chat_rl.py`의 `train_tasks`에도 X를 추가하고 — REINFORCE가 *정답률을 직접 보상*으로 깎아낸다. SpellingBee는 한 줄짜리 정답(`####N`)을 가졌고, *그 한 줄*이 *RL의 reward signal*이 된다.

*무엇이 강력한가?* 한 능력을 가르치는 *전체 파이프라인*이 — *task 정의 한 파일*과 *SFT mix 한 줄*로 끝난다는 것이다. *코퍼스를 모을 필요가 없고*, *라벨링을 외주줄 필요가 없고*, *별도 학습 인프라가 필요 없다*. *내가 정답을 *코드로* 계산할 수 있는 능력*이면 — *바로 가르칠 수 있다*.

*어떤 능력이 *이 패턴에 어울리나?*

- *문자열 조작*: count, slice, reverse, palindrome 판정. SpellingBee의 친척들.
- *수치 계산*: 사칙연산, 분수, 단위 환산. 정답을 *코드로 계산*할 수 있다.
- *간단한 추론*: list 정렬, 중복 제거, 그래프 BFS의 짧은 버전. 정답을 *알고리즘으로 계산*할 수 있다.
- *고정 포맷 변환*: JSON → CSV, markdown → HTML, 날짜 포맷 변환. 정답이 *결정적*이다.

*무엇이 안 어울리나?* *정답이 *주관적인* 능력*이다. 글쓰기 품질, 농담 만들기, 윤리적 판단 — 이런 건 *정답을 *코드로 정의*할 수 없다. 그래서 SpellingBee 패턴은 *모든 능력*을 가르치진 못한다. *정답이 코드로 검증 가능한 능력*에 *국한*된 *강력하지만 한정된 도구*다.

## 6. ★ 한국어로 가는 길

여기까지 — *영어 nanochat의 *변형*을 펴봤다. 자기 정체성을 박는 변형, 새 능력을 추가하는 변형. 그런데 *한국어 독자*가 책을 덮을 때 *진짜 알고 싶은* 변형은 *그것이 아니다*. *한국어로 답하는 nanochat을 만들고 싶다*는 게 *솔직한 동기*다.

10장의 *기대치 박스*에서 한 번 *씁쓸하게* 인정한 바가 있다 — *"한국어로 물어보면 영어로 답하거나 깨진다. 그게 nanochat의 학습 데이터 분포다."* FineWeb-Edu가 영어 중심이고 SmolTalk도 영어 중심이라, *base 모델부터 SFT까지 한국어를 *거의 보지 못했다*. 그러니 *한국어로 가는 길*은 *harness의 *데이터 부품*을 *통째로* 바꾸는 일이다. 5천 자 한 절에서 *어디부터 손을 대는지*를 *방향만이라도* 깔아두자. 더 깊은 코드 디테일은 *부록 D*가 다룬다 — 이 절은 *방향과 첫 명령*이다.

### 6-(a). 한국어 코퍼스를 어디서 받나

영어 사전학습은 FineWeb-Edu라는 *교육 품질로 필터링된 Common Crawl*을 쓴다. 1.53B rows, ODC-BY 라이선스. 그럼 *한국어 버전*은 어디 있나? 정답이 *하나*는 아니지만, *현실적으로 손에 잡히는* 후보가 세 가지다.

**첫째, AI-Hub의 한국어 웹 텍스트 코퍼스.** AI-Hub는 한국지능정보사회진흥원(NIA)이 운영하는 데이터 플랫폼이다. *"한국어 웹 데이터 기반 사전학습 모델"* 같은 데이터셋이 *대규모로* 무료 제공된다. 가입과 *목적 설명*이 필요하지만, *연구·교육 목적*이면 거의 통과된다. 수십 GB의 한국어 raw text를 받을 수 있다.

**둘째, KoCommonCrawl.** Common Crawl의 *한국어 페이지만* 필터링·정제한 오픈 데이터셋들이 HuggingFace에 여럿 올라와 있다. `beomi/KoAlpaca-v1.1a` 같은 데이터셋의 *기반*이 된 *raw 한국어 crawl*이 그 한 갈래다. *품질 필터링*이 FineWeb-Edu만큼 *깐깐하지 않을 수 있다*는 게 *주의점*이다. 데이터 노이즈(스팸·중복·HTML 잔재)가 학습 발산의 원인이 된 사례가 영어에서도 흔하다 — 한국어는 *더 신경 쓸 일*이 있다.

**셋째, 모두의 말뭉치(국립국어원).** 국립국어원이 *언어자원으로* 공개한 한국어 코퍼스다. *문어/구어/신문/SNS/방언* 등 *분야별*로 나뉘어 있고, *언어학적으로 잘 정제*되어 있다. *문제는 *규모다*. FineWeb-Edu가 *수십 TB*인 데 비해 모두의 말뭉치는 *수십 GB 수준*이라, *단독으로 사전학습*은 *어렵다*. 다른 코퍼스의 *보조*로 쓰기 좋다.

*현실적인 조합*은 — **AI-Hub 웹 텍스트(주력) + KoCommonCrawl(증량) + 모두의 말뭉치(품질 보강)** 정도다. 합쳐 50~100GB 규모를 만들고, *영어 FineWeb-Edu의 작은 일부*(예: 10%)와 *섞어* 학습한다. *영어를 완전히 빼지 않는* 이유는 — *영어 평가 벤치마크들*(MMLU, ARC, HumanEval)이 여전히 *유용하기 때문*이다. 한국어 비중을 60~80%, 영어를 20~40% 정도로 잡는 게 *작은 모델에서 출발할 때의 *균형*이다.

### 6-(b). `tok_train.py`의 `--max-chars`와 special token 호환성

데이터를 손에 쥐었으면 — *그 다음*은 토크나이저다. 2장과 3장에서 이미 본 *그 부품*이다. 한국어를 *제대로 압축*하려면 *한국어 데이터로 BPE를 재학습*해야 한다.

`scripts/tok_train.py`의 인자를 펴보자. 두 가지가 *한국어*에서 중요하다.

**`--max-chars`.** BPE 학습에 *몇 글자까지 보는가*다. nanochat 기본은 2,000,000,000(20억 자). 한국어 한 글자가 UTF-8에서 3바이트라 *바이트로는 60GB쯤* 보는 셈이다. *한국어 코퍼스가 50GB라면* — `--max-chars=20000000000`(200억) 정도로 *키우는 게 낫다*. 그래야 *코퍼스 전체*를 BPE의 *통계*에 반영할 수 있다. 메모리는 *수십 GB* 필요해진다.

**`--vocab-size`.** 기본 32768. 영어 위주에 *적당한* 크기다. 한국어 *전용*이라면 *조금 키우는 게 낫다* — 한국어가 *형태소 분기*가 많아 *같은 어근의 변형*이 많기 때문이다. 40K~50K 정도가 *한국어 위주 작은 모델*에서 *경험적으로* 잘 작동한다. 다만 vocab을 키우면 *lm_head 파라미터*가 *선형으로* 커지니, *작은 모델*에서는 *과한 비용*일 수 있다. *32K로 시작*하고, *압축률*(`scripts/tok_eval.py`로 측정)을 보고 *부족하면 키우는* 절차가 *안전*하다.

**special token 호환성.** 이게 *주의할 부분*이다. nanochat의 tokenizer는 *대화 포맷*을 위한 special token 7개를 미리 등록해둔다 — `<|im_start|>`, `<|im_end|>`, `<|im_python_start|>`, `<|im_python_end|>`, `<|im_python_output_start|>`, `<|im_python_output_end|>`, `<|pad|>`. 이 토큰들의 *id 위치*가 *chat_sft.py와 chat_rl.py의 *고정 가정*에 들어가 있다. 한국어 tokenizer를 *처음부터 다시 학습*할 때 — *이 special token들을 *반드시 같은 순서로* 등록*해야 한다. 그렇지 않으면 SFT가 *어떤 토큰을 generation token으로 쓸지*를 *잘못 잡고* 학습이 *조용히 망가진다*.

다행히 `tok_train.py`가 이 부분을 *코드로* 다루고 있다 — `tokenizer.add_special_tokens([...])`로 명시적으로 등록한다. 한국어로 학습할 때 *코드를 바꿀 필요는 없다*. 그저 *학습이 끝났을 때 special token의 id를 한 번 확인*하면 된다. `print(tokenizer.encode("<|im_start|>"))`가 *영어 기본*과 *같은 숫자*를 내면 OK다.

### 6-(c). 한국어 SmolTalk 대체재

base 모델을 *한국어로 잘 학습*시켰다 해도 — SFT 단계에서 *한국어 대화 데이터*가 없으면 *대화로 답하는 능력*을 못 가르친다. SmolTalk는 *영어*고, *한국어 대안*은 *영어만큼 풍부하지는 않지만 *있다*.

**KoAlpaca.** Anthropic Alpaca의 *한국어 번역·재생성판*이다. `beomi/KoAlpaca-v1.1a` (HuggingFace)가 가장 *잘 알려진 버전*이다. 약 50K~75K 줄의 *짧은 instruction-response* 데이터. SmolTalk보다 *훨씬 작지만*, *한국어 instruction following*의 *기반*을 잡기에는 충분하다.

**KoVicuna.** Vicuna의 한국어 번역판. *멀티턴 대화*가 KoAlpaca보다 많아서, *대화의 흐름*을 가르치는 데 더 좋다.

**KOpen-platypus·KoMath·KoMMLU-style auxiliary** 등 *작은 한국어 SFT 데이터셋*들이 HuggingFace에 *조금씩 늘어나는 중*이다. 합치면 *수십만 줄* 규모는 만들 수 있다.

**또 한 가지 — *번역 augmentation.*** SmolTalk의 *일부를 한국어로 번역*해서 *합성 SFT 데이터*를 만드는 방법이 *적극적으로 쓰인다*. OpenRouter API로 Claude나 Gemini Flash에 *"이 대화를 한국어로 자연스럽게 번역해라, 인사말과 문화 표현은 한국어 화자에게 자연스럽게 바꿔라"* 같은 prompt를 던지면 *한 시간에 수만 줄*을 번역할 수 있다. *비용*은 *수만 원 수준*이다. 4-(b)에서 본 `gen_synthetic_data.py`의 *패턴*을 *번역에 적용*하면 된다.

*현실적인 SFT mix*는 — **KoAlpaca 50K + KoVicuna 30K + 번역 SmolTalk 100K + identity 1000×4 + SpellingBee 한국어 버전 80K + 영어 SmolTalk 100K(잔존)** 정도다. 합쳐 30만 줄 안팎. 한국어 비중을 70%, 영어를 30% 정도 유지하는 균형.

### 6-(d). 한국어 평가의 어려움

이게 *솔직한 골짜기*다. 영어에는 MMLU, ARC, HumanEval, GSM8K처럼 *학계가 인정한* 벤치마크가 *십수 개*씩 있고, *nanochat의 eval_bundle*이 그걸 *고스란히* 받아 쓴다. *한국어*에는 — *그만큼*은 없다.

**KMMLU(Korean MMLU).** MMLU의 한국어 버전이다. 4지선다 객관식. 의학·법학·공학 등 *전문 분야*가 *번역·재구성*돼 있다. nanochat의 `tasks/mmlu.py`를 *KMMLU 버전*으로 *살짝 변형*하면(데이터 로딩만 바꾸면) *그대로 평가 가능*하다. 한국어로 가는 길에서 *가장 손에 잡히는* 평가다.

**KoBEST.** 한국어 BERT 평가 슈트다. KB-BoolQ, KB-COPA, KB-HellaSwag, KB-SentiNeg, KB-WiC 같은 *5개의 한국어 task*가 묶여 있다. *작은 모델*에서 *세분화된 능력*을 보는 데 좋다.

**KoGSM8K·KoHumanEval.** 영어 GSM8K와 HumanEval의 *한국어 번역판*이 *학계에서 만들어지는 중*이지만, *공식 표준*은 아직 *정착이 덜* 됐다. *번역 품질*에 따라 *결과가 흔들린다*. 책이 쓰여진 시점에는 *KoGSM8K-v2* 같은 *상대적으로 신뢰할 만한* 한국어 수학 벤치마크가 *몇 개* 떠 있다.

*한국어 평가의 어려움*은 두 가지다.

첫째, *벤치마크가 적다*. CORE의 22 task처럼 *넓은 베이스라인*이 *한국어에는 없다*. 그래서 *한국어 모델의 *raw capability*를 *영어 모델만큼 정밀하게 비교*하기 어렵다. 두세 개의 평가로 *대략적인 추세*만 본다.

둘째, *번역 vs 원본*의 *진정성* 문제. KMMLU가 *번역*인지 *처음부터 한국어로 만들어진* 것인지에 따라 — *난이도와 문화 적합도*가 *상당히 다르다*. 의학 문제에서 *한국 의학 용어*와 *영어 직역*이 *섞여 있으면* 모델의 정답률이 *비균질*하게 나온다.

*그래서 현실적인 평가 셋업*은 — **KMMLU + KoBEST + KoGSM8K + 영어 MMLU(잔존)** 네 개 정도로 *한국어 base*를 추적하고, *나머지는 정성적 대화 품질*로 본다. *완벽한 자동 평가*는 *아직 없다*는 *솔직한 인정*이 필요하다.

### 6-(e). 작은 한국어 nanochat 시작하기 — 짧은 액션 가이드

방향을 다 깔았으니 *첫 명령*을 손에 쥘 차례다. *작은 한국어 nanochat 한 마리*를 *어떻게* 시작할 것인가? 액션 가이드 *5단계*로 줄여보자.

**1단계: 데이터 받기.** AI-Hub에서 한국어 웹 텍스트 코퍼스(50GB 정도)를 신청·다운로드. 시간이 *며칠 걸린다* — 이게 *가장 느린 단계*다. 기다리는 동안 KoAlpaca와 KoVicuna는 HuggingFace에서 *몇 분 만에* 받아둔다.

```bash
# KoAlpaca
huggingface-cli download beomi/KoAlpaca-v1.1a --repo-type=dataset --local-dir ./data/koalpaca

# KoVicuna
huggingface-cli download junelee/wizard_vicuna_70k_korean --repo-type=dataset --local-dir ./data/kovicuna
```

**2단계: 토크나이저 재학습.** 한국어 + 영어 일부를 합친 코퍼스로 BPE를 재학습.

```bash
python -m scripts.tok_train \
    --max-chars=20000000000 \
    --vocab-size=32768 \
    --train-data=./data/korean_mix.txt
```

`scripts/tok_eval.py`로 *한국어 압축률*을 확인. 영어와 비슷한 4.5~5.0× 정도가 나오면 *성공*이다. 안 나오면 vocab을 40K로 늘려 한 번 더.

**3단계: 작은 base 모델 사전학습 (d6 또는 d10).** 처음부터 d24를 *건드리지 말자*. 8×H100 한 노드와 *수십 시간*이 *바로* 사라진다. *d6 또는 d10*에서 *코퍼스가 잘 흐르는지*만 확인한다.

```bash
torchrun --standalone --nproc_per_node=8 -m scripts.base_train -- \
    --depth=6 --head-dim=64 \
    --max-seq-len=1024 --device-batch-size=32 \
    --total-batch-size=131072 \
    --num-iterations=5000 \
    --core-metric-every=-1  # 한국어 평가가 없으면 CORE는 끄자
```

d6이 1~2시간이면 끝난다. val_bpb가 *영어 base*와 비슷한 *1.0 근방*으로 떨어지면 — *한국어 학습이 정상적으로 굴러간다*는 신호다.

**4단계: SFT.** KoAlpaca + KoVicuna + 번역 SmolTalk + 한국어 identity(직접 합성)를 mix.

```bash
torchrun --standalone --nproc_per_node=8 -m scripts.chat_sft -- \
    --depth=6 \
    --train-tasks=koalpaca,kovicuna,smoltalk_translated,identity,spellingbee_kr
```

`tasks/koalpaca.py` 같은 파일은 *직접 작성해야 한다* — *SpellingBee 패턴*을 빌려서 *KoAlpaca의 JSON을 conversation으로 변환*하는 *Task 서브클래스*를 한 30줄로 짠다.

**5단계: 시연.** `chat_web`을 띄우고 *한국어로* 물어본다.

```bash
python -m scripts.chat_web --depth=6
```

```
User: 안녕, 너는 누구야?
Model: 안녕하세요! 저는 토비챗입니다. Toby가 nanochat 코드베이스를
       바탕으로 한국어 데이터로 학습시킨 작은 챗봇이에요. 무엇을
       도와드릴까요?

User: 한국어로 잘 답해?
Model: 한국어로 답하려고 노력합니다만, 학습한 한국어 데이터가
       제한적이라 영어보다는 약합니다. 어려운 한국어 질문은
       종종 영어로 답할 수 있다는 점 양해해 주세요.
```

이게 *작은 한국어 nanochat의 *첫 인사다*. d6 모델은 *영어 d24만큼 똑똑하지는 않다* — *kindergartener 수준*의 한국어다. 그래도 *내 손으로 만든 한국어 챗봇이 한국어로 답한다*는 *감각*은 *충분히 짜릿*하다.

거기서 시작하자. 한국어 코퍼스를 늘리고, d12로 키우고, 한국어 SpellingBee 같은 *문자 단위 task*를 추가하고, KMMLU로 평가하고, RL을 한 번 더 깎고. *작은 한 판이 굴러가면* — *다음 한 판*은 *더 큰 한 판*이 된다.

## 7. nanochat의 한계 — *솔직한 그림자*

자기 챗봇과 한국어 nanochat까지 *손에 쥐었으니* — 이제 *nanochat이 *닿지 못하는* 자리를 *솔직히* 인정할 차례다. 책의 끝에서 *과장하지 않는* 의무가 있다.

**첫째, 영어 위주다.** 이미 6절에서 *한국어로 가는 길*을 깔았지만, *그 길이 *짧지 않다*. FineWeb-Edu 12B 토큰을 *한국어로 대체*하는 일은 *비용이 만만치 않고*, *한국어 평가 인프라가 영어만큼 정밀하지 않은* 한계가 *그대로 남는다*. *솔직히* — *영어 nanochat을 *그대로 받아쓰면* 좋은 한국어 챗봇이 *그냥 나오는* 일은 없다. *한국어 nanochat을 만드는 일*은 *별도의 프로젝트*가 된다.

**둘째, 12B 토큰의 한계.** speedrun config는 *12B 토큰*을 *3시간*에 학습한다. 그게 GPT-2 *capability*를 따라잡는 *놀라운 효율*이지만, *세상의 좋은 LLM들*(Llama-3, Claude, GPT-4)은 *수조 토큰* 단위를 학습한다. 100배~1000배 차이다. *그 차이가 만드는 *지식의 폭과 깊이*는 — *12B로는 *원천적으로* 닿을 수 없는 영역*이다. nanochat은 *kindergartener*이고, *학사·박사·교수*가 *아니다*. *지식의 *얕음*은 *모델 크기*보다 *데이터 양*의 영향이 *훨씬 크다*.

**셋째, RL이 GSM8K *하나*만 깎는다.** 9장에서 본 그 *짧고 단단한* RL 단계는 *수학 문제*에 *국한*되어 있다. 이유는 *GSM8K가 정답을 *코드로* 검증할 수 있기 때문이다 (`#### 72`). HumanEval처럼 *코드 검증*도 가능한 분야가 있지만, *글쓰기 품질*이나 *대화의 자연스러움*은 *RL로 깎기 어렵다*. 그건 *RLHF*(인간 피드백)나 *constitutional AI* 같은 *별도 접근*이 필요한 영역인데, nanochat에는 *그 인프라가 *아직* 들어 있지 않다. *기여 환영*이라는 카르파시의 한 줄이 [#1]에 있다.

**넷째, multimodal이 없다.** nanochat은 *순수 텍스트 모델*이다. 이미지를 못 본다. 음성을 못 듣는다. 그림을 못 그린다. *현대 챗봇*이 *멀티모달*로 빠르게 이동하는 흐름과 *방향이 다르다*. nanochat의 *겨냥*은 *텍스트 LLM의 *해부학*이고, 그 자리에서 *충분히 가치 있는* 모델이지만, *최신 트렌드*를 따라가려면 *별도의 multimodal 헤드*를 *외부에서 붙이는* 작업이 필요하다.

**다섯째, agent loop이 없다.** "도구를 *여러 번* 호출하면서 *계획을 세우는 agent*" — 이런 *반복적 도구 사용*이 nanochat에는 *없다*. inference engine이 *calculator와 python tool*을 *한 turn에 한두 번* 호출할 수는 있다(10장에서 본 *calculator 토큰*). 하지만 *Claude나 GPT-4가 하는 것처럼* — *수십 step의 계획·실행·반성*을 *반복하는 agent*는 *별도 wrapper로 만들어야 한다*. *모델 자체*는 *한 turn의 대화*에 *최적화*되어 있다.

이 다섯 한계를 *솔직히* 인정하는 게 — *책의 끝에서 *해야 할 일*이다. nanochat은 *완전한 챗봇 솔루션*이 아니다. *완전한 챗봇을 만드는 *해부학적 출발점*이다. *kindergartener를 *학사*로 키우는 길*에는 *데이터, 평가, RL 인프라, multimodal, agent*까지 *수많은 봉우리*가 남아 있다. *그 봉우리들에 어떻게 오르는지*는 — *책의 *다음 책장*에 있다.

## 8. 다음 책장

책 한 권을 덮는 자리에서 *다음 책장*을 한 줄씩 깔아두자. *책의 *서가*가 *세 갈래*다.

**갈래 1: *사전학습으로 더 깊이*.**

- **nanoGPT** (Karpathy). [github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT). nanochat의 *전작*. 사전학습만 다룬다. *튜토리얼처럼* 코드가 *훨씬 짧고*, *transformer가 *어떻게 학습되는지*만 *깔끔하게* 본다. 책의 4A·6장만 *훨씬 자세히* 다루는 *짧은 책*에 해당한다.
- **modded-nanoGPT** (Keller Jordan). [github.com/KellerJordan/modded-nanogpt](https://github.com/KellerJordan/modded-nanogpt). nanoGPT를 *최적화의 리더보드*로 만든 프로젝트. nanochat의 4B에서 본 *일곱 트릭의 상당수*가 *이 프로젝트에서 왔다*. *옵티마이저와 트릭의 진화*를 *역사적으로* 따라가고 싶으면 — *이 리포의 git log*가 *책 한 권*이다.
- **Karpathy "Zero to Hero" 강의** (YouTube). [youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ](https://youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ). transformer의 *처음*부터 *내 손으로 짜는* 동영상 시리즈. 책에서 *수식을 양보*한 자리에서 — *카르파시가 *손으로* 수식을 *쓰는 영상*은 *훨씬 친절*하다. 8~10시간 분량.

**갈래 2: *데이터로 더 깊이*.**

- **FineWeb 후속 작업들.** FineWeb-Edu의 *데이터 필터링 파이프라인*이 *오픈*되어 있다. [HuggingFace FineWeb](https://huggingface.co/datasets/HuggingFaceFW/fineweb). *내 도메인*(예: 한국어, 의학, 법률)에 *맞게 필터를 *재학습*해서 *내 코퍼스*를 만드는 일이 *연구의 한 흐름*이다.
- **DCLM** (DataComp-LM). [arXiv:2406.11794](https://arxiv.org/abs/2406.11794). CORE 평가의 *원천 논문*. *데이터 비교*를 *체계적으로* 하는 *벤치마크*다. *어떤 데이터*가 *왜 좋은가*에 대한 *학계의 최신 답*이 여기 모여 있다.
- **ClimbMix** (NVIDIA). speedrun #4부터 nanochat이 사용한 데이터셋. FineWeb-Edu보다 *조금 더 정제*된 *최신 코퍼스*다.

**갈래 3: *RL과 추론으로 더 깊이*.**

- **DeepSeek-Math (GRPO)**. [arXiv:2402.03300](https://arxiv.org/abs/2402.03300). 9장에서 본 *REINFORCE*보다 *한 단계 위*의 RL 알고리즘. *나노챗 이후*의 *오픈 reasoning 모델들*이 *대부분 GRPO를 쓴다*. 9장의 *직관*을 *조금만 확장*하면 *바로 이해 가능*한 알고리즘이다.
- **DAPO**(DeepSeek). [arXiv:2503.10460](https://arxiv.org/abs/2503.10460). GRPO의 *후속*. *long-context*에서 *더 안정적*인 RL.
- **Tülu·SkyRL·OpenR1** 등 *오픈 RLHF·RL 프로젝트들*. nanochat의 `chat_rl.py`보다 *훨씬 큰 인프라*가 *오픈*되어 있다. *내 모델을 *대규모로* 강화학습*하고 싶을 때.

**갈래 4: *multimodal과 agent*.**

- **LLaVA** (Liu et al.). 텍스트 LLM에 *비전 인코더*를 *붙이는* 가장 *깔끔한 오픈 접근*. nanochat에 *vision head*를 붙이고 싶을 때 *참고할 만한* 첫 모델.
- **ReAct·Tool-Former·Voyager** 같은 *agent 논문들*. nanochat의 *calculator tool*을 *수십 step*으로 *확장*하는 방향.

*다섯째 갈래*가 *있긴 하다* — *나노챗 자체의 후속*이다. 카르파시가 nanochat을 *계속 다듬는 중*이고, [#420 miniseries v2], [#481 leaderboard]에서 *지금도 새 버전*이 *나오는 중*이다. *책을 덮은 뒤에도* GitHub의 nanochat repo를 *가끔 들여다보면* — *반년에 한 번씩 새로운 트릭*이 *코드에 박혀 있는 걸* 발견할 거다. 그게 *작은 즐거움*이다.

## 9. 처음 질문에 답하는 단락

자, *책의 첫 질문*으로 돌아가 보자.

*"우리가 따라온 이 코드가 사실은 무엇이었는가? 그리고 나만의 한국어 챗봇을 만들고 싶다면 어디부터 손대야 하는가?"*

이제 답이 *손에 잡힌다*.

*우리가 따라온 이 코드*는 — *한 모델*이 아니라 *한 모델을 만드는 harness였다*. 8천 줄의 결속 장치. 토크나이저부터 학습 루프부터 평가 부품부터 보고서까지 *한 다이얼*(`--depth`)로 묶여 굴러가는 *교환 가능한 부품들*. *체크포인트*가 책의 진짜 산출이 *아니고* — *그 체크포인트를 *만드는 방법*이 *책의 진짜 산출이다*. 그래서 *내가 학습한 d24 모델*을 *지웠다 해도* — *책을 한 권 다시 펼치면* *또 한 마리*를 만들 수 있다. *손에 *방법*이 남았기 때문이다.

*나만의 한국어 챗봇을 만들고 싶다면* — *어디부터 손대야 하는지*도 이제 *방향이 보인다*. AI-Hub에서 한국어 코퍼스 받기, 토크나이저 재학습, d6 또는 d10 작은 base 학습, KoAlpaca + KoVicuna + 번역 SmolTalk + 한국어 identity로 SFT, chat_web으로 첫 인사 — *그 다섯 단계가 *시작점*이다. *완벽한 한국어 챗봇*이 *첫 시도에 나오는* 일은 *없을 거다*. d6짜리 작은 모델이 *어색한 한국어*로 *첫 인사*를 건넨다. 그 *어색함*에서 *조금씩 다듬어 가는* 일이 — *책 다음의 길*이다.

*8천 줄을 덮으며* 손에 남는 게 *모델 한 마리가 아닌 이유*는 — *한 책장에는 *한 마리*가 안 남는다*는 *책의 약속* 때문이다. *책장에는 *길*이 남는다*. *어디로 가는 길*인지, *무엇을 손에 쥐고 가는*지가 *책장에 적혀 있는 것*이고, *그 길을 *내가 걸어보는 일*은 *책 *다음의 일*이다.

손에 쥔 *방향*과 *첫 명령*이 있다면 — *그걸로 충분하다*. *지금* 손에 키보드가 있고, *지금* `git clone https://github.com/karpathy/nanochat`을 *한 줄* 치면 — *모든 게 거기 있다*. 8천 줄짜리 *책 한 권*이 *컴퓨터 안에* 들어온다. 거기서 *책을 덮은 다음의 *진짜 일*이 *시작된다*.

당신의 nanochat을 한 번 만들어 두자.

---

### 실습 박스 — 자기 identity 챗봇 한 마리 만들기

**환경:** 8×H100 + OpenRouter API 키 + 약 4~5시간.

**선택 실습**이다. *책의 마지막* 실습이고, *책에서 가장 비싼* 실습이다. *돈과 시간*이 *모두* 든다. 그런데 *책을 덮으며 손에 *남기는* 마지막 산출*이 — *내 정체성으로 답하는 작은 챗봇 한 마리*라는 게 *충분히 그럴 가치가 있을 것이다*. 손에 OpenRouter 키와 GPU 노드가 있다면 — *이 실습을 *한 번만* 끝까지 해 보자*.

**실습 절차:**

1. **knowledge 파일 작성.** `nanochat/knowledge/self_knowledge.md`에 *내 정체성*을 1~2 페이지 분량으로 적는다. 4-(a)에서 본 *템플릿*을 *내 이름·내 동기·내 한계*에 맞게 바꾼다.

2. **합성 데이터 생성.**

   ```bash
   export OPENROUTER_API_KEY=...
   python -m dev.gen_synthetic_data
   ```

   약 30분~1시간. 비용은 *몇 천 원~몇 만 원* 수준(모델 선택에 따라). 결과: `~/.cache/nanochat/identity_conversations.jsonl`에 1000줄.

3. **SFT 재실행.**

   ```bash
   torchrun --standalone --nproc_per_node=8 -m scripts.chat_sft -- \
       --depth=24 \
       --identity-epochs=4
   ```

   약 1~2시간 (이미 base 학습이 끝나 있다는 전제).

4. **시연.** `python -m scripts.chat_web --depth=24`를 띄우고 *"who are you?"*와 *"what's your name?"*과 *"who created you?"*를 *세 번* 물어본다.

**기대하는 결과:**

- 세 질문 모두에 *내가 적은 정체성*이 *일관되게* 답해야 한다. 이름이 *나오고*, *만든 사람*이 나오고, *왜 만들어졌는지*가 *한 줄*로 나온다.
- *어느 한 답이 일관되지 않으면* — `identity-epochs`를 4 → 6으로 *조금 더 오버샘플*. 또는 `gen_synthetic_data.py`의 `topics["identity"]`에 *항목을 더 추가*해 *더 다양한 표현*으로 학습.
- *세 답이 모두 자연스럽고 일관*되면 — **축하한다**. *내 손으로 학습한 *내 챗봇*을 *내 정체성으로 답하게 만드는 일*이 *완성된 것*이다.

이 실습이 — *책 한 권의 *마지막 산출*이다. 짧고 다정한 작별의 *형태*다. 부디 *한 번 *끝까지* 굴려보길 바란다.
