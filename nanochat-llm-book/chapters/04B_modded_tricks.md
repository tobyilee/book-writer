# 4B장. modded-nanoGPT가 더한 7가지 트릭

4A장에서 GPT 모듈의 *골격*을 펼쳐봤다. RoPE로 위치를 회전시키고, RMSNorm으로 분산을 잡고, ReLU²로 비선형을 짚어주는 *교과서적인 부품*들이었다. 그 골격만으로도 트랜스포머는 굴러간다.

그런데 `gpt.py`를 다시 열어 forward 함수를 천천히 따라가 보면 — 우리가 4A에서 *지나친* 줄들이 잔뜩 박혀 있다. `self.smear_lambda`, `self.resid_lambdas[i]`, `self.value_embeds[str(i)]`, `self.backout_lambda`, `softcap * torch.tanh(...)`. 이름만 봐서는 무엇 하나 *교과서에 나오는* 부품이 아니다. 카르파시가 그냥 멋부린 걸까? 그렇지 않다. 이 줄들은 *modded-nanoGPT 커뮤니티*가 nanoGPT speedrun 리더보드를 깎아 내려오면서 발견한 *현대화 패치*들이다. 한 줄 한 줄이 어딘가의 GitHub Discussion이나 arXiv 페이퍼에 출처가 있고, *작은 모델*에서 *측정 가능한 이득*을 보여줬기 때문에 nanochat에 흡수됐다.

이번 장은 그 *패치 노트*다. 7개의 트릭. 각각이 무엇을 *왜* 더하는지, 코드 어디에 박혀 있는지, *직관적*으로 어떤 메타포로 잡으면 견딜 만한지. 4A의 외과의 같은 집중이 아니라, *기록자*의 호흡으로 가자. 다 따라오고 나면 5장의 옵티마이저로 넘어갈 수 있는 *체력*이 남는다.

라인 번호는 모두 `nanochat/gpt.py` 기준이고, 책의 이번 라운드에서 직접 다시 검증했다(`gpt.py`는 총 512줄).

## 1. Value embeddings — attention의 메모장에 같은 단어를 다시 한 번

첫 번째 트릭은 **value embedding**이다. 정식 이름은 *ResFormer*에서 따왔다고 알려져 있다. 카르파시의 nanochat discussion #481에서는 이걸 두고 *"added ~150M params with near-zero FLOPs"*라고 짧게 적었다.

무슨 뜻인지 코드부터 펴 보자. `gpt.py:53-55`:

```python
def has_ve(layer_idx, n_layer):
    """Returns True if GPT layer should have Value Embedding (alternating, last layer always included)."""
    return layer_idx % 2 == (n_layer - 1) % 2
```

레이어 절반에만 켜진다. 12개 레이어라면 0·2·4·6·8·10번이거나 1·3·5·7·9·11번이거나(`n_layer`의 짝홀에 따라). 마지막 레이어는 *항상* 포함된다.

켜진 레이어가 *무엇*을 받는지는 `gpt.py:188-200`에 있다.

```python
self.value_embeds = nn.ModuleDict({
    str(i): nn.Embedding(padded_vocab_size, kv_dim)
    for i in range(config.n_layer) if has_ve(i, config.n_layer)
})
```

`wte`(원래 토큰 임베딩) 말고도 *별도의 임베딩 테이블*이 절반 레이어 수만큼 새로 잡힌다. 각 테이블의 크기는 `(vocab_size, kv_dim)` — `wte`만큼 크다. 그래서 파라미터가 *어마어마하게* 늘어난다. d12에서 `kv_dim`은 보통 768이고 vocab은 32K니, 한 테이블이 약 25M 파라미터. 6개 레이어가 켜지면 150M이다. *그래서* "150M params"라는 숫자가 나온다.

그런데 *왜* near-zero FLOPs인가? 다음 줄을 보자. `gpt.py:91-95`:

```python
# Value residual (ResFormer): mix in value embedding with input-dependent gate per head
if ve is not None:
    ve = ve.view(B, T, self.n_kv_head, self.head_dim)
    gate = 3 * torch.sigmoid(self.ve_gate(x[..., :self.ve_gate_channels]))  # (B, T, n_kv_head), range (0, 3)
    v = v + gate.unsqueeze(-1) * ve
```

핵심은 마지막 줄 — `v = v + gate * ve`. attention의 *value 벡터*에 별도 임베딩을 *더한다*. 임베딩 lookup은 곱셈이 아니라 *인덱싱*이라 FLOPs가 거의 0이다(그래서 "near-zero").

게이트도 *매우* 싸다. 입력 hidden state에서 *앞 12채널*만 떼어다(`x[..., :self.ve_gate_channels]`, `ve_gate_channels=12`이 `gpt.py:79`에 정의됨) `(12 → n_kv_head)` 선형 변환을 거치고, `3 * sigmoid(...)`로 (0, 3) 범위의 multiplier를 만든다. 헤드별로 *각자의 음량 노브*가 생기는 셈이다. 768채널을 다 쓰지 않고 12채널만 쓰는 데서 *near-zero*가 강조된다.

**직관 메타포로 잡자.** attention은 *메모장*이다. q는 "내가 뭘 찾고 있나"를, k는 "여기 뭐가 적혀 있나"를, v는 "그 적힌 내용은 *무엇인가*"를 담는다. 보통은 v도 입력 hidden state로부터 만든다 — 즉 *문맥적 표현*에서 나온 v다. value embedding은 거기에 *원본 토큰*에서 직접 만든 또 다른 v를 *덧대*는 것이다. "이 위치의 토큰이 원래 무슨 단어였더라"를 attention 단계에서 *다시 한 번* 기억나게 만든다.

왜 그게 도움이 되는가? 작은 모델은 깊지 않다. 12 레이어쯤이면 정보가 *희석*되기 쉽다. residual stream이 위로 올라갈수록 원본 토큰 정보가 *흐릿해진다*. ResFormer 류는 그걸 보강한다 — 각 attention 단계에서 *원본 토큰의 메모*를 v에 다시 적어두는 것이다.

`init_weights`에서 ve를 어떻게 초기화하는지도 한 번 보자. `gpt.py:247-253`:

```python
# Value embeddings (init like c_v: uniform with same std)
for ve in self.value_embeds.values():
    torch.nn.init.uniform_(ve.weight, -s, s)

# Gate weights init with small positive values so gates start slightly above neutral
for block in self.transformer.h:
    if block.attn.ve_gate is not None:
        torch.nn.init.uniform_(block.attn.ve_gate.weight, 0.0, 0.02)
```

ve의 무게는 c_v와 같은 std로 시작한다(즉 `±√3/√n_embd` 균등). 게이트는 0~0.02 사이 *작은 양수*. `sigmoid(작은 양수) ≈ 0.5`이고 거기에 3을 곱하면 약 1.5다. 즉 *처음에는 ve가 1.5배 음량으로 들어가서* v에 약하지도 강하지도 않게 섞인다. 학습이 진행되면 layer마다, head마다 *자기에게 맞는 음량*을 찾는다.

찜찜한 사람도 있을 것이다 — *임베딩이 두 벌*이라는 사실이. wte 한 벌만으로 끝났던 GPT-2와 비교하면, nanochat은 wte + lm_head + value_embeds 합치면 임베딩 계열만 셋이다. 작은 모델에서 *비-matmul 파라미터*의 비중이 그만큼 커진다는 뜻이다(`estimate_flops`에서 이걸 빼주는 이유는 4A에서 봤다). 이건 의도된 트레이드오프다 — *FLOPs는 안 쓰고 표현력만 사겠다*는 것.

## 2. Per-layer learnable scalars — 각 레이어의 볼륨 노브

두 번째는 **per-layer learnable scalars**다. modded-nanoGPT 커뮤니티의 발명으로 알려져 있고, 카르파시가 nanochat에 가져왔다.

`gpt.py:177-186`을 펴 보자.

```python
# Per-layer learnable scalars (inspired by modded-nanogpt)
# resid_lambdas: scales the residual stream at each layer (init 1.0 = neutral)
# x0_lambdas: blends initial embedding back in at each layer (init 0.0 = disabled)
# Separate parameters so they can have different optimizer treatment
self.resid_lambdas = nn.Parameter(torch.ones(config.n_layer))   # fake init, real init in init_weights()
self.x0_lambdas = nn.Parameter(torch.zeros(config.n_layer))     # fake init, real init in init_weights()
# Smear: mix previous token's embedding into current token (cheap bigram-like info)
self.smear_gate = Linear(24, 1, bias=False)
self.smear_lambda = nn.Parameter(torch.zeros(1))
# Backout: subtract cached mid-layer residual before final norm to remove low-level features
self.backout_lambda = nn.Parameter(0.2 * torch.ones(1))
```

두 개의 *학습되는 스칼라 벡터*가 있다. 길이는 둘 다 `n_layer`다. 즉 *레이어마다 하나씩*.

- `resid_lambdas[i]`: i번째 레이어에서 *residual stream*을 얼마나 강하게 흘려보낼지의 배율.
- `x0_lambdas[i]`: i번째 레이어에서 *초기 임베딩(x0)*을 얼마나 다시 섞을지의 배율.

forward에서 어떻게 쓰이는지 다시 한 번 보자. `gpt.py:452-459`:

```python
# Forward the trunk of the Transformer
x0 = x  # save initial normalized embedding for x0 residual
n_layer = self.config.n_layer
backout_layer = n_layer // 2  # cache at halfway point
x_backout = None
for i, block in enumerate(self.transformer.h):
    x = self.resid_lambdas[i] * x + self.x0_lambdas[i] * x0
    ve = self.value_embeds[str(i)](idx).to(x.dtype) if str(i) in self.value_embeds else None
    x = block(x, ve, cos_sin, self.window_sizes[i], kv_cache)
```

전통적인 트랜스포머라면 `x = x + block(x)`만 있다(=residual). nanochat은 *그 직전*에 `x = λ_resid · x + λ_x0 · x0`를 더한 *변형 residual*을 쓴다. 두 개의 학습된 스칼라가 *볼륨 노브*다.

`init_weights`에서 이 노브들의 *초기 위치*가 결정된다. `gpt.py:232-239`:

```python
# Per-layer scalars
# Per-layer resid init: stronger residual at early layers, weaker at deep layers
n_layer = self.config.n_layer
for i in range(n_layer):
    self.resid_lambdas.data[i] = 1.15 - (0.10 * i / max(n_layer - 1, 1))
# Decaying x0 init: earlier layers get more input embedding blending
for i in range(n_layer):
    self.x0_lambdas.data[i] = 0.20 - (0.15 * i / max(n_layer - 1, 1))
```

n_layer=12 기준으로 *처음 값*을 풀어 써 보자.

| i (레이어) | resid_lambdas[i] | x0_lambdas[i] |
|---:|---:|---:|
| 0 | 1.15 | 0.20 |
| 1 | 1.141 | 0.186 |
| ... | ... | ... |
| 6 | 1.095 | 0.118 |
| ... | ... | ... |
| 11 | 1.05 | 0.05 |

읽히는 그림이 있다. **얕은 레이어일수록** residual의 음량이 *조금 크고*(1.15), 초기 임베딩 x0의 영향도 *조금 더 강하다*(0.20). **깊은 레이어로 갈수록** 둘 다 *서서히 줄어든다*(1.05, 0.05). 깊은 레이어에서는 *이미 가공된 hidden state*를 그대로 흘려보내고, 얕은 레이어에서는 *원본 임베딩에 가까운 신호*를 좀 더 섞어둔다.

이게 *왜* 작은 모델에 의미가 있나? 깊지 않은 모델은 표현이 layer마다 *극적으로* 변한다. residual 음량이 1.0으로 고정되어 있으면 — 깊은 layer에서 *과도하게 커진 hidden*과 *원래 작아야 할 변화량*이 충돌하기 쉽다. λ를 학습하게 두면, 모델이 *스스로* "이 레이어에서는 residual을 조금 줄여라, 저 레이어에서는 x0를 좀 다시 끌어와라"를 *데이터에서 배운다*.

**직관 메타포로 잡자.** 각 레이어의 입구에 *두 개의 노브*가 달려 있다고 보자. 첫 노브(resid)는 *지금까지 흘러온 신호*의 음량, 두 번째 노브(x0)는 *원본 임베딩*을 *얼마나 더 섞을지*의 음량. 카르파시는 이 노브들의 *초기 위치*를 깊이에 따라 살짝 기울여 두고, 학습이 진행되면서 모델이 *스스로 미세조정*하게 한다.

옵티마이저 설정에도 흔적이 남는다. setup_optimizer에서 *별도의 param group*으로 분리된다 — `resid_lambdas`와 `x0_lambdas`는 *스칼라*이므로 Muon이 아니라 AdamW에 들어간다(Muon은 matrix용이다, 5장에서 자세히). 그래서 코드 주석이 *"Separate parameters so they can have different optimizer treatment"*라고 말한다.

체크포인트 호환성 한 줄도 잡고 가자. `checkpoint_manager.py:30-40`의 `_patch_missing_keys`는 *옛 체크포인트*에 `resid_lambdas`나 `x0_lambdas`가 없으면 *각각 1.0과 0.0*으로 채워 넣는다. 즉 *이 트릭이 추가되기 전에 학습된 체크포인트*도 *지금의 코드로* 열 수 있다. 카르파시 식 *재현성에 대한 신경*이 묻어나는 한 줄이다.

## 3. Smear — 직전 단어를 흐릿하게 비춰두기

세 번째는 **smear**다. 영어로 *문지르다* 또는 *번지게 하다*는 뜻이다. 이름이 정확히 동작을 묘사한다.

`gpt.py:432-449`를 통째로 펴 보자. 이번 트릭은 *한 곳에 모여 있다*.

```python
# Smear: mix previous token's embedding into current position (cheap bigram info)
if kv_cache is None:
    # Training / naive generate: full sequence available, use fast slice
    assert T > 1, "Training forward pass should have T > 1"
    gate = self.smear_lambda.to(x.dtype) * torch.sigmoid(self.smear_gate(x[:, 1:, :24]))
    x = torch.cat([x[:, :1], x[:, 1:] + gate * x[:, :-1]], dim=1)
else:
    # KV cache inference: read prev embedding from cache, store current for next step
    x_pre_smear = kv_cache.prev_embedding
    kv_cache.prev_embedding = x[:, -1:, :]
    if T > 1:
        # Prefill: apply smear to positions 1+, same as training
        gate = self.smear_lambda.to(x.dtype) * torch.sigmoid(self.smear_gate(x[:, 1:, :24]))
        x = torch.cat([x[:, :1], x[:, 1:] + gate * x[:, :-1]], dim=1)
    elif x_pre_smear is not None:
        # Decode: single token, use cached prev embedding
        gate = self.smear_lambda.to(x.dtype) * torch.sigmoid(self.smear_gate(x[:, :, :24]))
        x = x + gate * x_pre_smear
```

길어 보이지만 *training 경로*만 보면 두 줄로 줄어든다.

```python
gate = self.smear_lambda * torch.sigmoid(self.smear_gate(x[:, 1:, :24]))
x = torch.cat([x[:, :1], x[:, 1:] + gate * x[:, :-1]], dim=1)
```

해석은 *직관적*이다. 위치 t의 hidden state에 *위치 t-1의 hidden state*를 *살짝* 더한다. 0번째 토큰은 *직전 토큰이 없으므로* 그대로 두고, 1번째부터 끝까지 — *각자 직전 위치의 임베딩*을 자신에게 *번지게* 한다.

얼마나 번지게 할지는 두 개의 노브가 결정한다.

- **smear_lambda** (`gpt.py:184`): 길이 1짜리 스칼라. `init_weights:242`에서 *0으로 초기화*된다. 즉 *처음에는 smear가 0*이다(아무 영향 없음). 학습이 *필요하다고 판단하면* 0에서 위로 끌어올린다.
- **smear_gate** (`gpt.py:183`): `Linear(24, 1)`. hidden state의 *앞 24채널*을 입력으로 받아 *위치별·배치별 게이트값*을 만든다. `sigmoid`로 (0, 1) 범위. `init_weights:244`에서 `Uniform(0.0, 0.02)`로 *아주 작게* 시작한다.

종합하면 — *학습 초반에는 smear가 사실상 켜지지 않는다*. λ가 0이라서. 학습이 진행되면서 λ가 0보다 살짝 커지고, 게이트는 *어떤 위치에서 smear가 필요한지*를 토큰별로 배운다.

KV cache 경로(`else` 블록)는 *추론 시*다. 토큰을 하나씩 생성하는 동안 *직전 단계의 hidden state*를 어딘가에 *저장해두지 않으면* 다음 step에서 smear를 적용할 수 없다. 그래서 `KVCache`에 `prev_embedding`이라는 별도 슬롯이 있다(`engine.py:82-138`에서 정의됨, 10장에서 자세히). prefill 단계(T > 1)는 training과 같은 방식, decode 단계(T == 1)는 *cache에 저장된 직전 임베딩*과 *현재 임베딩*을 섞는다.

**왜 이게 *cheap bigram trick*이라고 불리는가?** bigram이란 *연속된 두 토큰*을 보는 것이다(unigram이 단일, bigram이 둘, trigram이 셋). 고전 NLP의 *n-gram 모델*은 이전 한 토큰을 보고 다음을 예측했다. 트랜스포머는 attention으로 전체 문맥을 보기 때문에 *어쨌든* 직전 토큰도 본다. 그런데 attention은 *softmax로 가중 합*을 만들기 때문에 *바로 직전 토큰만 명시적으로 짚어내기*가 *생각보다* 어렵다 — 모든 위치와 *경쟁*해야 한다. smear는 그 *직전 위치 정보*를 attention과 *별개로* hidden state에 *직접 박아준다*. 그래서 *비싼 attention을 거치지 않고* bigram 정보를 *공짜에 가깝게* 챙긴다.

**직관 메타포로 잡자.** 그림책의 한 페이지를 인쇄한 직후, *잉크가 마르기 전에* 다음 페이지를 위에 살짝 누르면 — 다음 페이지에 *이전 페이지의 흐릿한 자국*이 남는다. smear가 하는 일이 그것이다. 직전 토큰의 임베딩을 *살짝 흐릿하게* 현재에 비춰둔다. 두꺼운 자국이 아니라 *얇은 잔상*이다.

코드 한 군데가 *번거롭게* 느껴질 수 있다 — *training 경로*와 *KV cache 경로*가 사실상 *같은 일*을 *다른 방식*으로 하는 부분 말이다. 그게 추론 시점의 *상태 관리* 비용이다. 추론은 한 토큰씩 generative하게 도는데, smear는 *직전 hidden state*가 필요하므로 *어딘가에는 저장해야 한다*. cache에 슬롯을 하나 추가하는 게 가장 단순한 답이고, 카르파시도 그렇게 했다.

## 4. Backout — 그림을 그린 뒤 초벌 스케치를 지우는 단계

네 번째는 **backout**이다. 이름이 동작을 직설적으로 말한다 — *뒤로 빼낸다*.

코드의 *선언* 부분부터. `gpt.py:185-186`:

```python
# Backout: subtract cached mid-layer residual before final norm to remove low-level features
self.backout_lambda = nn.Parameter(0.2 * torch.ones(1))
```

길이 1짜리 스칼라 파라미터. 초기값은 *0.2*다. `init_weights:243`이 같은 값을 *명시적으로* 한 번 더 적어두는 걸 보면 이 초기값에 *의도가 있다*. 0이 아니다 — *처음부터 backout이 켜져 있다*.

*무엇을* 빼는가? `gpt.py:452-464`를 다시 한 번 펴 보자.

```python
# Forward the trunk of the Transformer
x0 = x  # save initial normalized embedding for x0 residual
n_layer = self.config.n_layer
backout_layer = n_layer // 2  # cache at halfway point
x_backout = None
for i, block in enumerate(self.transformer.h):
    x = self.resid_lambdas[i] * x + self.x0_lambdas[i] * x0
    ve = self.value_embeds[str(i)](idx).to(x.dtype) if str(i) in self.value_embeds else None
    x = block(x, ve, cos_sin, self.window_sizes[i], kv_cache)
    if i == backout_layer:
        x_backout = x
# Subtract mid-layer residual to remove low-level features before logit projection
if x_backout is not None:
    x = x - self.backout_lambda.to(x.dtype) * x_backout
x = norm(x)
```

읽기는 어렵지 않다.

1. 전체 레이어 중 *중간 지점*(`n_layer // 2`)에 도달했을 때, *그 시점의 hidden state*를 `x_backout`이라는 변수에 *저장*해둔다.
2. 마지막 레이어까지 forward를 다 돌고, *최종 norm 직전*에 — `x = x - λ_backout · x_backout`을 한다. 즉 *중간 시점의 hidden을 빼낸다*.

주석이 친절하다. *"to remove low-level features before logit projection"*. 깊은 layer로 갈수록 hidden state는 *추상적인 표현*에 가까워진다 — 어떤 토큰을 출력할지, 문법은 어떤지, 문맥은 어떤 톤인지. 얕은 layer일수록 *덜 가공된*, *원래 토큰의 정체*에 더 가까운 표현이다. backout은 *최종 출력 직전에* 그 *덜 가공된 신호의 일부*를 *빼내는* 것이다.

찜찜할 수 있다. 잠깐, *residual stream*은 *정보를 더하는 것*이 미덕이지 않았던가? 트랜스포머 설계의 가장 단단한 직관 중 하나가 *"residual은 정보를 보존한다"*인데, 그걸 일부러 *빼낸다*? 그렇다. 이게 카르파시가 modded-nanoGPT에서 가져온 가장 *대담한* 결정 중 하나다.

**직관 메타포로 잡자.** 화가가 유화를 그릴 때를 떠올려 보자. 처음에 *연필이나 목탄으로 초벌 스케치*를 그리고, 그 위에 유화 물감을 *겹겹이 쌓는다*. 그림이 다 완성된 뒤, *초벌 스케치 선이 비쳐 보이면* — 마무리 단계에서 *그 선을 지우거나 덮는다*. backout이 그 마무리 단계다. residual stream이 위로 올라오는 동안 *얕은 정보*(원래 토큰의 표면적 정체)가 깊은 표현 위에 *비쳐* 있다. 최종 logit으로 *얕은 정보가 직접 새는 것*을 막기 위해, *중간 지점의 hidden을 빼내서* 깊은 표현이 *온전히 자기 일을 하게* 한다.

이 직관이 *모든 데이터에서 옳다고는 못한다*. 그래서 backout의 *세기*는 학습되는 스칼라 `backout_lambda`다. 초기값 0.2로 *약하게 켜둔 채* 시작하고, 모델이 *데이터를 보고* 그 값을 *조정한다*. 학습 끝에 0에 가까워지면 *backout이 별로 도움 안 됐다*는 뜻이고, 0.5 가까이 올라가면 *상당히 적극적으로 빼고 있다*는 뜻이다.

이 챕터 끝의 실습 박스에서 backout_lambda를 *0으로 강제했을 때 vs 그대로일 때* 모델 출력 분포를 비교해본다. *"backout이 정말 뭔가를 빼고 있는지"*를 직접 손에 쥐어보는 게 이 트릭을 가장 빨리 *납득*하는 길이다.

## 5. Sliding window attention — 짧은 창과 긴 창을 섞어 짜기

다섯 번째는 **sliding window attention**이다. 이전 네 개는 *수직 흐름*(residual stream)에 손댔다면, 이번 것은 *수평 시야*(attention 범위)에 손댄다.

`GPTConfig`의 마지막 필드를 다시 보자. `gpt.py:36-39`:

```python
# Sliding window attention pattern string, tiled across layers. Final layer always L.
# Characters: L=long (full context), S=short (quarter context)
# Examples: "L"=all full context, "SL"=alternating, "SSL"=two short then one long
window_pattern: str = "SSSL"
```

기본값이 `"SSSL"`이다. 이 *문자열*이 attention의 시야를 결정한다.

해석은 `_compute_window_sizes`에 있다. `gpt.py:285-312`:

```python
def _compute_window_sizes(self, config):
    """..."""
    pattern = config.window_pattern.upper()
    assert all(c in "SL" for c in pattern), f"Invalid window_pattern: {pattern}. Use only S and L."
    # Map characters to window sizes
    long_window = config.sequence_len
    short_window = -(-long_window // 4 // 128) * 128  # ceil to FA3 tile size (2048 -> 768)
    char_to_window = {
        "L": (long_window, 0),
        "S": (short_window, 0),
    }
    # Tile pattern across layers
    window_sizes = []
    for layer_idx in range(config.n_layer):
        char = pattern[layer_idx % len(pattern)]
        window_sizes.append(char_to_window[char])
    # Final layer always gets full context
    window_sizes[-1] = (long_window, 0)
    return window_sizes
```

읽으면 그림이 잡힌다. *패턴 문자열*을 layer 인덱스에 따라 *반복*해서 깔고, *마지막 layer만* 항상 *L*(full context)로 강제한다.

`"SSSL"`을 12 layer에 *타일링*하면 어떻게 되나? `0,1,2,3,4,5,6,7,8,9,10,11` 인덱스가 `S,S,S,L,S,S,S,L,S,S,S,L`이 된다 — 그리고 마지막 layer가 어차피 L이라 그대로다. 즉 12 layer 중 *9개가 S(짧은 시야), 3개가 L(긴 시야)*다.

*"짧다"*가 얼마나 짧은가? `sequence_len`이 2048이면, `short_window = ceil(2048/4/128) * 128 = 6 * 128 = 768`이 된다. *주석*은 *"2048 -> 768"*이라고 적어두지만, 코드를 따라가 보면 *quarter context*라는 표현이 *대략* 맞다(정확히는 quarter를 다시 *128 배수로 ceil*한 것). FA3의 *내부 tile 크기*가 128이라 그 단위로 맞춰진 것이다.

**왜 이렇게 하는가?** 두 가지 이유다.

첫째, *attention의 비용*은 sequence 길이 T에 대해 *O(T²)*다. T=2048이면 T²=4M, T=768이면 T²≈590K. 짧은 창을 쓰는 layer가 *훨씬 싸다*. layer의 대부분이 *짧은 창*이면 학습이 *대폭 빨라진다*. PaLM 논문의 FLOPs 공식이 sliding window를 반영한 이유다(4A의 `estimate_flops`).

둘째, *모든 layer가 긴 시야를 봐야 할 필요가 없다*. 얕은 layer는 *국소적인 패턴*(어절, 구문)을 학습하고, 깊은 layer는 *문장·문단 단위*의 종속을 학습한다. 그렇다면 *몇 개 layer만* 긴 시야를 가져도 정보 흐름은 충분하다 — 마치 *layer 사이를 거치며 정보가 점점 멀리 퍼져나가는* 것처럼.

여기까지는 *이론적으로* 깔끔하다. 그런데 *실전*에서 sliding window는 *민감한 트릭*이다. 그 이유가 `flash_attention.py`에 박혀 있다. `gpt.py:108`에서 attention 호출이 다음과 같다.

```python
y = flash_attn.flash_attn_func(q, k, v, causal=True, window_size=window_size)
```

이 `flash_attn`이 FA3(Flash Attention 3)냐 SDPA(PyTorch의 기본 attention)냐에 따라 *세상이 갈린다*. `nanochat/flash_attention.py:48-105`를 펴 보자.

```python
def _resolve_use_fa3():
    """Decide once whether to use FA3, based on availability, override, and dtype."""
    if _override_impl == 'fa3':
        assert HAS_FA3, "Cannot override to FA3: not available on this hardware"
        return True
    if _override_impl == 'sdpa':
        return False
    if HAS_FA3:
        # FA3 Hopper kernels only support bf16 and fp8; fp16/fp32 must use SDPA fallback
        from nanochat.common import COMPUTE_DTYPE
        if COMPUTE_DTYPE == torch.bfloat16:
            return True
        return False
    return False
```

FA3는 *Hopper(H100) 이상 + bf16/fp8* 조건일 때만 켜진다. fp16이나 fp32, 또는 A100/3090/CPU/MPS — 어디든 *그 조건이 아니면* SDPA fallback이다.

SDPA fallback에서 *sliding window*는 어떻게 구현되는가? `flash_attention.py:91-102`:

```python
# Need explicit mask for sliding window/chunk inference
device = q.device
# For chunk inference (Tq != Tk), is_causal is not aligned to cache position => build an explicit bool mask
row_idx = (Tk - Tq) + torch.arange(Tq, device=device).unsqueeze(1)
col_idx = torch.arange(Tk, device=device).unsqueeze(0)
mask = col_idx <= row_idx

# sliding window (left)
if window >= 0 and window < Tk:
    mask = mask & ((row_idx - col_idx) <= window)

return F.scaled_dot_product_attention(q, k, v, attn_mask=mask, enable_gqa=enable_gqa)
```

핵심은 두 줄 — *명시적인 (T, T) 크기의 bool mask*를 만들어서 SDPA에 *attn_mask*로 넘긴다. FA3는 sliding window를 *커널 단에서* 처리해 mask 자체가 메모리에 올라오지 않지만, SDPA는 *T×T bool tensor*를 직접 만들어 GPU 메모리에 둔다. T=2048이면 4M개 bool, 거기에 broadcast가 일어나면 더 커진다.

`base_train.py:114-117`이 사용자에게 *직접* 경고한다.

```python
if args.window_pattern != "L":
    print0(f"WARNING: SDPA has no support for sliding window attention (window_pattern='{args.window_pattern}'). Your GPU utilization will be terrible.")
    print0("WARNING: Recommend using --window-pattern L for full context attention without alternating sliding window patterns.")
```

*"GPU utilization will be terrible"*이라는 표현이 그대로 박혀 있다. 정직한 한 줄이다.

**그래서 sliding window는 *조건부 트릭*이다.** H100 + bf16 환경에서는 *측정 가능한 속도 이득*을 가져다주지만, A100 또는 CPU/MPS에서 *그대로* 돌리면 *오히려 느려진다*. 4A의 실습에서 `window_pattern`을 "SSSL"에서 "L"로 바꿔본 적이 있다 — 그게 *CPU/MPS 환경에서 코드를 다루는 사람의 정직한 선택*이다.

**직관 메타포로 잡자.** *full context*는 *방 전체를 한눈에 보는* 망원경이다. *sliding window*는 *손전등*이다 — *내 위치 주변만* 비춘다. 망원경은 *비싸다*(시야 넓을수록 처리 비용 증가). 손전등은 *싸다*. 그런데 *어두운 방에서 길을 찾으려면 망원경 한 번은 들어야 한다* — 그래서 *마지막 layer는 항상 망원경*이다. layer를 *손전등 → 손전등 → 손전등 → 망원경*의 패턴으로 깔면, 정보가 *국소적으로 처리되다가 가끔 멀리까지 보는* 흐름이 된다.

## 6. Untied embedding — 입력과 출력의 임베딩을 분리하기

여섯 번째는 *짧다*. **untied embedding**.

`gpt.py:171-175`:

```python
self.transformer = nn.ModuleDict({
    "wte": nn.Embedding(padded_vocab_size, config.n_embd),
    "h": nn.ModuleList([Block(config, layer_idx) for layer_idx in range(config.n_layer)]),
})
self.lm_head = Linear(config.n_embd, padded_vocab_size, bias=False)
```

*무엇이 트릭인가?* 트릭이 *없다*는 것이 트릭이다. `wte`(토큰 → 임베딩)와 `lm_head`(임베딩 → vocab logits)가 *완전히 별개*의 파라미터다. *서로의 weight를 공유하지 않는다*.

이게 *왜* 의미가 있는가? GPT-2 원본을 비롯해 많은 transformer 구현이 *weight tying*이라는 트릭을 쓴다 — 즉 `lm_head.weight = wte.weight.T`로 *같은 행렬을 입출력 양쪽에 재사용*한다. 직관적으로 그럴듯하다. *임베딩 공간*과 *로짓 공간*이 *대칭적*이어야 한다는 미적 감각도 있고, 무엇보다 *파라미터를 한 벌만 학습*하면 되니 *작은 모델*에서는 *효율*이라고 보였다.

그런데 modded-nanoGPT 커뮤니티와 카르파시는 *반대 방향*으로 갔다. **untied**다. 즉 *두 행렬을 따로 학습*한다. 그러면 파라미터가 *두 배*로 늘어난다 — vocab=32K, n_embd=768이면 임베딩 한 벌당 약 25M, 두 벌이면 50M. *작지 않은 비용*이다.

그럼에도 untied가 *작은 모델에서* 가성비가 있는 이유는 무엇인가? 두 가지로 정리해 두자.

1. **입력과 출력의 *역할*이 다르다.** wte는 *토큰을 시작 표현으로* 매핑하고, lm_head는 *최종 hidden을 vocab 분포로* 사상한다. 두 매핑이 *수학적으로 같아야 할 이유*는 *없다*. tying은 *직관적 미*이지 *최적 해*가 아니다.
2. **초기화가 달라야 한다.** `init_weights:218-219`를 다시 보자.

   ```python
   torch.nn.init.normal_(self.transformer.wte.weight, mean=0.0, std=0.8)
   torch.nn.init.normal_(self.lm_head.weight, mean=0.0, std=0.001)
   ```

   wte는 std=0.8로 *큼직하게* 초기화된다. lm_head는 std=0.001로 *극도로 작게* 초기화된다. 천 배쯤 차이가 난다. *이걸 같은 행렬로 묶으면 둘 중 한쪽이 *심각하게 부적합한 시작*을 갖게 된다.* untied는 *각자에게 맞는 초기화*를 *각자 줄 수 있는* 자유다.

`init_weights`의 std=0.001 한 줄에 대해 한 마디 더. lm_head를 *극도로 작게* 시작한다는 건 *학습 시작 시점에 모델이 *균등 분포에 가까운 logits*을 내놓는다*는 뜻이다. 학습이 막 시작될 때 cross-entropy loss가 `ln(vocab_size) ≈ ln(32K) ≈ 10.4`에 가까워지는 이유다 — *아직 아무것도 모르는 모델*은 *모든 토큰에 똑같은 확률*을 부여하고, 그 loss는 *수학적으로* `ln(vocab_size)`다. untied + 작은 std 초기화 덕분에 *깨끗한 출발점*이 만들어진다.

**직관 메타포로 잡자.** wte는 *책의 앞 표지*, lm_head는 *뒤 표지*다. 둘이 *같은 디자인이어야 할 이유*는 *없다*. 앞 표지는 *책 안으로 들어가는 입구*, 뒤 표지는 *책을 닫는 마무리*. 각자의 일에 맞는 디자인을 *따로* 준다.

작은 모델에서 untied embedding이 *가성비*를 가지는 또 하나의 이유는, *임베딩 계열의 파라미터가 차지하는 비중*이 *작은 모델에서 절대적이지 않다는 점*이다. d12에서 wte+lm_head 합쳐 약 50M, 전체 모델이 ~150M이면 임베딩 비중 30%대다. 트레이드오프가 *받아들일 만한 수준*이다. d24 정도로 가면 *임베딩 비중*이 *더 줄어들고*(전체가 560M이라 임베딩은 9%), untied의 비용은 *더 가벼워진다*.

물론 *훨씬 큰 모델*(70B급)로 가면 다른 트레이드오프가 나타날 수도 있다. 하지만 nanochat이 겨냥하는 *백만~십억 파라미터*의 자리에서는 untied가 *유리하다*. 카르파시가 *일찍이 weight tying을 버린* 결정의 배경이다.

## 7. Logit softcap — 폭주를 부드럽게 막는 자

마지막 일곱 번째. **logit softcap**. 한 줄짜리 트릭이다.

`gpt.py:466-472`:

```python
# Forward the lm_head (compute logits)
softcap = 15 # smoothly cap the logits to the range [-softcap, softcap]
logits = self.lm_head(x) # (B, T, padded_vocab_size) <- very big tensor, large amount of memory
logits = logits[..., :self.config.vocab_size] # slice to remove padding
logits = logits.float() # switch to fp32 for logit softcap and loss computation
logits = softcap * torch.tanh(logits / softcap) # squash the logits
```

핵심은 마지막 줄. `logits = 15 * tanh(logits / 15)`. 그것이 전부다.

읽는 법은 단순하다. `tanh(x)`는 *모든 실수*를 *(-1, 1)* 범위로 *부드럽게 짓누른다*. 그 결과에 *15를 곱하면* *(-15, 15)* 범위로 *부드럽게 잘린다*. 그래서 *soft cap*이다 — 하드한 `clip`이 아니라 *S 곡선으로 부드럽게* 묶는다. logits이 |x| ≪ 15 정도면 `15 * tanh(x/15) ≈ x`라 *실질적으로 영향이 없고*, |x|가 30, 50, 100처럼 *커질수록* 출력은 *15에 가까이 부드럽게 수렴*한다.

이 트릭은 *Gemma-2*가 명시적으로 사용해 유명해졌다. 원래 발상은 *그 이전*부터 있었지만, Google이 70억 파라미터 모델 학습 일지에 *"우리는 logit softcap을 쓴다, attention logits에도, 최종 logits에도"*라고 적은 뒤로 *작은 모델 학습의 표준 안전장치*가 됐다.

*무엇을 막는가?* **loss explosion**이다. 학습 중간에 logits이 *비정상적으로 커지면* — 예를 들어 어떤 토큰의 logit이 갑자기 200으로 튀면 — *softmax 후 확률이 사실상 1.0*이 되고, 그 토큰이 *정답이 아니면* cross-entropy loss가 *수십~수백*으로 폭주한다. 한 step의 거대한 loss는 *거대한 gradient*를 만들고, gradient는 *파라미터를 망가뜨린다*. 한 번 망가지면 *복구가 어렵다*. softcap이 logits을 (-15, 15)로 묶어두면, 토큰의 *최대 확신*도 `softmax(15) / (1 + 30000 * softmax(-15))`처럼 *어딘가에 상한*이 생긴다. *완전히 망가지지는 못하게* 막는 *안전판*이다.

한 가지 *디테일*이 더 있다. `logits.float()` 한 줄이 *softcap 직전*에 박혀 있다. 즉 *softcap 계산은 fp32로 한다*. 학습 본체는 bf16(또는 fp16, fp8)으로 굴러도, *로짓의 안정성*만은 *fp32의 정밀도*로 지킨다는 결정이다. bf16에서 `tanh`가 *큰 입력*에 대해 *수치적으로 불안정*해질 수 있어서 그렇다. 작은 한 줄이지만 *재현성에 대한 신경*이 묻어난다.

01_reference.md의 트러블슈팅 노트에 *"train/loss가 갑자기 튀어오르면: logit softcap이 잡아주긴 하지만 LR이 너무 크거나 batch가 너무 작거나 데이터 노이즈"*라는 한 줄이 있다. 카르파시가 *실제로 작동하는 안전장치*로 softcap을 *명시적으로 신뢰*하고 있다는 신호다. 그가 학습 중 *loss explosion*을 만났을 때 *손에 쥐고 있는 첫 도구*가 softcap이고, 그 도구가 *제 일을 한다*는 것을 코드와 문서 양쪽에서 확인할 수 있다.

**직관 메타포로 잡자.** *볼륨 노브에 있는 최대 음량 잠금*이다. 노브를 아무리 돌려도 *어느 지점 이상으로는 안 올라간다* — 그것도 *딱 끊기는*(hard clip) 게 아니라 *S 곡선으로 부드럽게 누른다*. 스피커가 *터질 일이 없다*. 학습이 *안정적으로* 굴러간다.

## 차 한 잔 마시고 가자

여기까지 7개 트릭. 정리하면 — value embedding은 attention의 메모장에 원본 토큰을 다시 적어두고, per-layer scalars는 layer마다 residual의 음량 노브를 학습으로 돌리고, smear는 직전 토큰을 흐릿하게 비추고, backout은 중간 hidden을 빼서 깊은 표현을 정리하고, sliding window는 시야의 폭을 layer마다 다르게 깔고, untied embedding은 입출력 행렬을 분리하고, softcap은 로짓 폭주를 막는다.

작은 트릭들이다. 각각은 한 줄에서 스무 줄짜리 변경이고, 어느 하나가 *모델을 두 배로 똑똑하게 만드는* 것도 아니다. 그런데 일곱이 *함께* 깔려 있을 때 — *작은 모델*에서 *측정 가능한 차이*가 만들어진다. 그게 modded-nanoGPT 리더보드를 깎아 내려온 *기록자들의 결과*이고, 카르파시가 그걸 nanochat에 *통째로 흡수*한 이유다.

4A에서 골격을 봤고, 4B에서 패치를 살폈다. 다음 장에서는 이 모델을 *학습시키는 두 옵티마이저*를 펴본다 — *AdamW와 Muon*. 왜 *두 개*가 필요한지, Muon이라는 이름이 무엇을 *직교화한다*는 뜻인지. 차 한 잔 마시고 가자. 5장에서 만나자.

---

### 실습 박스 — backout이 정말 뭔가를 *빼고 있는가*

**환경:** CPU/MPS 모두 가능. d4 모델로 약 20분.

이번 챕터에서 가장 *대담했던* 트릭은 backout이었다. 중간 layer의 hidden을 *cache했다가 최종 norm 직전에 뺀다*는 결정 — 그게 정말 *의미 있는 정보를 빼는 것*인지, 아니면 *그저 0.2배 노이즈를 제거하는 것*인지, 손에 쥐어 보자.

**실험 절차:**

1. d4 모델을 meta device에서 init하고 `init_weights()`까지 호출해 *실제 학습 시작 시점*의 파라미터를 만든다.
2. *현재의 `backout_lambda`*(초기값 0.2)로 forward를 한 번 돌린다. 입력은 임의의 토큰 시퀀스(예: `torch.randint(0, vocab_size, (1, 64))`). 출력 logits을 `logits_with_backout`에 저장한다.
3. `model.backout_lambda.data.zero_()`로 backout을 *강제로 0*으로 만든다. *같은 입력*에 대해 forward를 한 번 더 돌린다. 출력을 `logits_no_backout`에 저장한다.
4. 두 분포를 비교한다.

   ```python
   diff = (logits_with_backout - logits_no_backout).flatten()
   print(f"mean diff: {diff.mean().item():.6f}")
   print(f"std diff: {diff.std().item():.6f}")
   print(f"max abs diff: {diff.abs().max().item():.6f}")

   # 히스토그램(또는 텍스트 막대)으로 분포 차이 확인
   import torch
   bins = torch.linspace(-1.0, 1.0, 21)
   hist = torch.histogram(diff.cpu(), bins=bins)
   for b, h in zip(hist.bin_edges[:-1], hist.hist):
       print(f"{b.item():+.2f} | {'#' * int(h.item() / max(hist.hist.max().item(), 1) * 40)}")
   ```

**기대하는 관찰:**

- 학습 *시작 시점*의 모델은 `backout_lambda=0.2`이고 `x_backout`은 *대부분 0에 가까운 hidden*(c_proj가 zero-init이라 residual stream이 거의 입력 임베딩 그대로). 따라서 *학습 직후*의 forward에서는 *차이가 작을 수 있다*.
- 그래도 *완전히 0은 아니다*. smear와 x0_lambda, value embedding 등이 hidden을 흔들기 때문에 backout이 빼낼 *무언가*가 있다. max abs diff가 *0.001 수준이라도 0이 아니면* backout이 *기능하고 있다*는 신호다.
- **선택적 추가 실험:** d6 SFT 체크포인트를 다운받아 같은 비교를 *학습된 모델*에서 해 보자. *학습된 backout_lambda*는 보통 0.2에서 멀어져 있고, *차이가 훨씬 크게* 보일 것이다. 그것이 backout이 *학습 중에 의미를 획득한다*는 증거다.

이 실습은 *정답을 맞추는 시험*이 아니라, *내 손으로 트릭의 영향을 확인하는 길*이다. 4B의 직관 메타포가 *추상*에 머무는 것 같으면, 이 한 번의 실험으로 *backout이 실제로 무엇을 한다*는 감각을 잡을 수 있다.
