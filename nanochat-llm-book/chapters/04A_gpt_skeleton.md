# 4A장. GPT 모듈의 골격 — embed/forward/init/FLOPs

우리가 지금 펴려는 건 `gpt.py` 한 파일이다. 총 512줄, 한 화면을 가득 채우면 일곱 화면. 카르파시는 *Transformer 본체*라는 이름의 짐을 이 한 파일에 욱여넣었다. nn.Module 한 덩어리에 토큰 임베딩, attention, MLP, 옵티마이저 설정, 추론 루프, FLOPs 계산까지 모두 들어 있다.

이 챕터에서는 카르파시가 *어떻게* 욱여넣었는지가 아니라 *무엇을* 욱여넣었는지를 본다. 그러니까 외과의의 시선이다. 골격이 어디서 시작해 어디서 끝나는지를 본다.

골격이라는 말은 정직하다. *카르파시가 modded-nanoGPT 커뮤니티에서 가져온 일곱 가지 트릭*은 4B장에서 따로 본다. 4A에서 우리가 손에 쥐어야 할 것은 더 단순하다. 토큰이 들어가서 logits이 나오기까지의 한 페이지짜리 줄거리. 그리고 그 줄거리를 받쳐주는 *기본 결정 다섯 개*다.

다섯 개라는 숫자에 의미가 있다. Vaswani et al. 2017의 원형 트랜스포머와 비교해 nanochat이 손을 댄 *기본* 결정이 정확히 다섯 가지이기 때문이다. RoPE, RMSNorm, QK norm, ReLU², untied embedding. 이 다섯 개를 *왜 이렇게 정했는지* 알면 골격의 절반은 이해한 것이다.

자, 펴자.

## 1. GPTConfig — 모델의 모양을 정하는 다섯 줄

먼저 모델의 *모양*부터 본다. nn.Module을 만들기 전에 어떤 모양으로 만들지를 정해야 한다. 그 정보가 `GPTConfig`에 들어 있다.

```python
# nanochat/gpt.py:28-39
@dataclass
class GPTConfig:
    sequence_len: int = 2048
    vocab_size: int = 32768
    n_layer: int = 12
    n_head: int = 6
    n_kv_head: int = 6
    n_embd: int = 768
    window_pattern: str = "SSSL"
```

여덟 줄짜리 dataclass다. 그런데 이 여덟 줄을 한 줄씩 읽어보자.

`sequence_len = 2048`. 한 번에 처리하는 토큰의 최대 길이. context window라는 이름으로 자주 불린다. 2048이라는 숫자는 GPT-2의 기본값을 그대로 가져왔다.

`vocab_size = 32768`. 토크나이저가 만든 어휘 수. 2장에서 우리가 직접 학습시킨 32K 어휘다. `2^15` — 16의 배수, 64의 배수, 좋다.

`n_layer = 12`. Transformer block을 12층으로 쌓는다. *depth*라고 부르는 그 숫자다. nanochat의 `--depth` 플래그가 직접 조작하는 게 이 값이다. `--depth 6`이면 d6 모델, `--depth 24`면 d24 모델. 책의 부제가 약속하는 "3시간으로 ChatGPT"는 d24를 의미한다.

`n_head = 6`. attention head의 수. n_embd를 6개로 쪼개서 병렬로 attention을 돈다. 그러니까 head_dim은 자동으로 `n_embd / n_head = 768 / 6 = 128`이다. 어디서 본 숫자다. modded-nanoGPT 이래로 *head_dim=128*은 작은 모델의 사실상 표준이 됐다.

`n_kv_head = 6`. KV head의 수. 이게 다음 줄과 같으면 — `n_head == n_kv_head` — GQA(Group-Query Attention)가 *꺼진 것*이다. nanochat의 speedrun config는 이렇게 꺼져 있다. 만약 `n_kv_head=2`였다면 q는 6개 head, k와 v는 2개 head로 *같은* k/v를 3개씩 공유한다. 그게 GQA의 의미다. 작은 모델에서는 별 이득이 없어서 nanochat은 일단 끄고 시작한다.

`n_embd = 768`. residual stream의 차원. GPT-2 small의 그 768이다. d24처럼 layer를 늘리면 n_embd도 따라 늘어나는데, nanochat은 `n_embd = 64 * n_head`, 그리고 `n_head = depth`라는 단순한 공식을 쓴다. 즉 *모델의 너비와 깊이가 같이 자란다*. 정사각형 모델. (이 공식은 `scripts/base_train.py`에서 확인할 수 있다.)

`window_pattern = "SSSL"`. 이건 잠시 후에 다시 본다. sliding window attention의 layer별 패턴이다. S는 short, L은 long. "SSSL"이면 4개 layer마다 short-short-short-long을 반복한다. 마지막 layer는 *언제나* L이다. 이건 4B의 핵심 주제니까 여기서는 *모양에 영향을 준다*는 것만 기억해두자.

여덟 줄짜리 dataclass가 모델의 *모양*을 거의 다 결정한다. depth 한 다이얼만 돌리면 d4부터 d26까지 미니시리즈가 자동으로 만들어진다. 이게 nanochat의 한 가지 미덕이다. *모양을 정의하는 코드가 짧다.*

## 2. forward 한 페이지 — 우리가 그릴 줄거리

이제 본론으로 들어가자. `GPT.forward`가 무엇을 하는지를 한 페이지로 본다. *4A에서는 큰 그림만*. 세부 트릭은 4B에서.

forward의 줄거리를 의사코드로 적어보면 이렇다.

```
idx (B, T) — 토큰 인덱스
│
├─ wte(idx) → x   (B, T, n_embd)       임베딩 lookup
├─ x = norm(x)                          embed 직후 RMSNorm
│
├─ smear: 이전 토큰의 임베딩을 살짝 섞기 (4B 주제)
│
├─ x0 = x  (초기 임베딩을 따로 저장)
│
├─ for each block i in range(n_layer):
│       x = resid_lambdas[i] * x + x0_lambdas[i] * x0   (4B 주제)
│       ve = value_embeds[i](idx) if i ∈ ve_layers      (4B 주제)
│       x = block(x, ve, cos_sin, window_size[i], kv_cache)
│       if i == n_layer // 2:
│           x_backout = x  (4B 주제)
│
├─ x = x - backout_lambda * x_backout   (4B 주제)
├─ x = norm(x)                          최종 RMSNorm
│
├─ logits = lm_head(x)                  (B, T, vocab_size)
├─ logits = softcap * tanh(logits / softcap)   softcap = 15, fp32
│
└─ if targets:
       loss = cross_entropy(logits, targets)
       return loss
   else:
       return logits
```

이게 forward 의사코드다. *4A에서 우리가 신경 쓸 부분은 굵게 표시되지 않은 줄들*이다. smear, value embeds, resid_lambdas, x0_lambdas, backout — 이 다섯 개가 modded-nanoGPT가 더한 *트릭*이고, 4B의 주제다.

그러니까 4A의 forward는 이렇게 단순해진다.

> 임베딩 lookup → norm → block을 n_layer번 → norm → lm_head → softcap.

여기까지가 골격이다. block 안에서 어떤 일이 벌어지는지는 다음 절에서 본다. 그 전에 한 가지만 짚고 가자.

`x = norm(x)`이 두 번 등장한다. 임베딩 직후에 한 번, 최종 lm_head 직전에 한 번. 그리고 block 안에서도 attention과 MLP의 *입력*에 norm이 한 번씩 더 들어간다. *pre-norm*이다. Vaswani 2017의 원형은 post-norm이었다. 학습 안정성 때문에 거의 모든 현대 LLM이 pre-norm으로 옮겨갔다. nanochat도 마찬가지다.

이제 block을 펴자.

## 3. Block — attention과 MLP를 묶은 한 단위

Block의 코드는 짧다. 11줄이다.

```python
# nanochat/gpt.py:142-152
class Block(nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.attn = CausalSelfAttention(config, layer_idx)
        self.mlp = MLP(config)

    def forward(self, x, ve, cos_sin, window_size, kv_cache):
        x = x + self.attn(norm(x), ve, cos_sin, window_size, kv_cache)
        x = x + self.mlp(norm(x))
        return x
```

11줄 안에 *pre-norm 트랜스포머 블록*의 모든 것이 들어 있다. attention 한 번, MLP 한 번. 입력에 norm을 한 번 걸고 residual로 더하는 패턴이 두 번 반복된다. *residual은 norm을 거치지 않은 원본 x*를 더한다는 게 pre-norm의 핵심이다. norm은 attention과 MLP 안으로만 들어간다.

이 11줄이 12번(d12 기준) 반복된다. 그게 transformer의 stack이다.

block의 forward 서명을 한 번 더 보자. `(x, ve, cos_sin, window_size, kv_cache)`. 다섯 개의 인자다. `x`는 residual stream. `ve`는 value embedding(4B 주제, 일부 layer만 None이 아니다). `cos_sin`은 RoPE를 위한 사전 계산된 cos/sin 튜플. `window_size`는 이 layer가 short인지 long인지(4B 주제). `kv_cache`는 추론 시점에만 None이 아니다 — 학습 시에는 항상 None.

block을 풀고 나면 두 친구가 남는다. `CausalSelfAttention`과 `MLP`. 한 친구씩 본다.

## 4. CausalSelfAttention — RoPE, QK norm, 그리고 1.2× sharpening

CausalSelfAttention은 65~126번 줄, 총 62줄이다. 4A에서 우리가 볼 부분은 그중에서도 *기본 골격*뿐이다. value embedding gate(91~95줄)와 kv_cache 분기(106~121줄)는 4B에서 본다.

`__init__`부터 보자.

```python
# nanochat/gpt.py:65-80 (발췌)
class CausalSelfAttention(nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.layer_idx = layer_idx
        self.n_head = config.n_head
        self.n_kv_head = config.n_kv_head
        self.n_embd = config.n_embd
        self.head_dim = self.n_embd // self.n_head
        assert self.n_embd % self.n_head == 0
        assert self.n_kv_head <= self.n_head and self.n_head % self.n_kv_head == 0
        self.c_q = Linear(self.n_embd, self.n_head * self.head_dim, bias=False)
        self.c_k = Linear(self.n_embd, self.n_kv_head * self.head_dim, bias=False)
        self.c_v = Linear(self.n_embd, self.n_kv_head * self.head_dim, bias=False)
        self.c_proj = Linear(self.n_embd, self.n_embd, bias=False)
```

네 개의 Linear가 보인다. `c_q`, `c_k`, `c_v`, `c_proj`. 모두 `bias=False`. 이게 첫 번째 *기본 결정*이다. 현대 LLM은 거의 모두 attention의 linear에서 bias를 뺐다. 작은 모델에서 bias가 차지하는 파라미터는 적지만, 잘못 학습되면 출력 분포에 *원치 않는 평균 shift*를 만든다. 빼는 게 안전하다.

그리고 한 가지 더, `Linear`가 `nn.Linear`가 아니라 *카르파시가 따로 정의한 Linear*다. 무엇이 다른가? 45~50번 줄에 답이 있다.

```python
# nanochat/gpt.py:45-50
class Linear(nn.Linear):
    """nn.Linear that casts weights to match input dtype in forward.
    Replaces autocast: master weights stay fp32 for optimizer precision,
    but matmuls run in the activation dtype (typically bf16 from embeddings)."""
    def forward(self, x):
        return F.linear(x, self.weight.to(dtype=x.dtype))
```

이 다섯 줄이 *PyTorch의 autocast를 통째로 대체한다.* master weight는 fp32로 들고 있다가, forward 호출 시 입력의 dtype(주로 bf16)으로 weight를 캐스팅해서 matmul을 돌린다. 옵티마이저는 fp32 master weight를 보고 update를 계산하니까 *정밀도 손실은 없다*. 그런데 matmul 자체는 bf16에서 돌아서 *속도와 메모리를 아낀다*.

이건 autocast 컨텍스트 매니저를 안 써도 되는 깔끔한 방법이다. autocast를 한 번이라도 디버깅해본 사람이라면 안다 — 어떤 텐서가 어떤 dtype에 있는지 추적하기가 *얼마나 난감한* 일인지. 다섯 줄로 그걸 우회한 거다.

이제 forward로 가자. 우리가 4A에서 볼 부분은 82~108줄이다. value embedding gate(91~95)는 4B에서 다룬다.

```python
# nanochat/gpt.py:82-90, 97-108 (발췌, value embedding 부분 제외)
def forward(self, x, ve, cos_sin, window_size, kv_cache):
    B, T, C = x.size()

    # Q, K, V 프로젝션. FA3 native layout: (B, T, H, D) — transpose 없음.
    q = self.c_q(x).view(B, T, self.n_head, self.head_dim)
    k = self.c_k(x).view(B, T, self.n_kv_head, self.head_dim)
    v = self.c_v(x).view(B, T, self.n_kv_head, self.head_dim)

    # (value embedding gate — 4B 주제)

    # RoPE 적용
    cos, sin = cos_sin
    q, k = apply_rotary_emb(q, cos, sin), apply_rotary_emb(k, cos, sin)
    q, k = norm(q), norm(k)  # QK norm
    q = q * 1.2  # sharper attention
    k = k * 1.2

    # Flash Attention 디스패치
    if kv_cache is None:
        y = flash_attn.flash_attn_func(q, k, v, causal=True, window_size=window_size)
    else:
        # (inference 경로 — KV cache 처리)
        ...

    y = y.contiguous().view(B, T, -1)
    y = self.c_proj(y)
    return y
```

순서를 한 줄로 적으면 이렇다.

> Q/K/V 프로젝션 → RoPE 적용 → QK norm → 1.2× sharpening → Flash Attention → 출력 프로젝션.

여섯 단계다. 각 단계에 *기본 결정*이 박혀 있다. 한 단계씩 보자.

### 4-1. Q/K/V 프로젝션 — FA3 native layout

`view(B, T, self.n_head, self.head_dim)`. shape가 `(B, T, H, D)`다. 그런데 이 순서가 *눈에 익지 않다*. 대부분의 PyTorch 트랜스포머 구현은 `view(B, T, H, D)` 후에 `transpose(1, 2)`를 해서 `(B, H, T, D)`로 만든다. 그래야 attention의 행렬 곱이 자연스러우니까.

nanochat은 transpose를 *안 한다*. 왜? FA3(Flash Attention 3)의 native layout이 `(B, T, H, D)`이기 때문이다. transpose 없이 바로 FA3에 넘긴다. *transpose 한 번을 아낀다*. 별 거 아닌 것 같지만 forward마다 매번 일어나는 일이라 누적되면 의미가 있다.

SDPA(PyTorch의 fallback) 경로에서는 다시 transpose를 해야 하지만, FA3가 도는 H100에서는 native layout이 그대로 들어간다.

### 4-2. RoPE — Su et al. 2021, base=100000

다음은 RoPE다. `apply_rotary_emb`가 호출된다.

```python
# nanochat/gpt.py:57-63
def apply_rotary_emb(x, cos, sin):
    assert x.ndim == 4  # multihead attention
    d = x.shape[3] // 2
    x1, x2 = x[..., :d], x[..., d:]  # split up last dim into two halves
    y1 = x1 * cos + x2 * sin  # rotate pairs of dims
    y2 = x1 * (-sin) + x2 * cos
    return torch.cat([y1, y2], 3)
```

일곱 줄이다. 이게 RoPE의 전부다.

RoPE(Rotary Positional Embedding)는 Su et al.의 "RoFormer" 논문(2021, [arXiv 2104.09864](https://arxiv.org/abs/2104.09864))에서 제안됐다. 발상은 단순하다. *Q와 K 벡터를 복소 평면에서 회전시켜 position을 인코딩하자.* 두 위치 m과 n의 Q·K dot product가 (m - n)에만 의존하도록 만들면, 상대 위치 정보가 *자연스럽게* attention 안에 들어간다.

원형 트랜스포머는 어떻게 했나? Vaswani 2017은 sinusoidal positional encoding을 *임베딩에 더해서* 위치를 알려줬다. 학습 가능한 positional embedding도 흔히 쓰였다. 두 방법 모두 *절대 위치*를 인코딩한다. 그런데 attention의 본질은 *상대 위치*다 — "이 단어가 *몇 칸 전*의 단어와 관련이 있나"가 핵심이지 "이 단어가 *몇 번째* 단어인가"가 핵심이 아니다.

RoPE는 *상대 위치*를 직접 인코딩한다. 그것도 *공짜로 가까이*. Q와 K를 각자 회전시키면, 그 둘의 내적이 회전 차이(m - n)에만 의존하는 함수가 된다. 이건 수학적으로 증명되는 사실이다.

코드를 다시 보면, `x1`과 `x2`로 마지막 차원을 절반으로 쪼갠 다음 회전 행렬을 곱한다. 회전 행렬은 `[[cos, sin], [-sin, cos]]`이다. *2차원 회전*이다. head_dim이 128이라면 64쌍의 2차원 회전을 동시에 한다. 각 쌍이 *다른 주파수*로 회전한다. 빠른 주파수는 짧은 거리(가까운 단어)에, 느린 주파수는 긴 거리(먼 단어)에 민감하다.

주파수는 어디서 오는가? `_precompute_rotary_embeddings`에 들어 있다.

```python
# nanochat/gpt.py:268-283
def _precompute_rotary_embeddings(self, seq_len, head_dim, base=100000, device=None):
    # TODO: bump base theta more? e.g. 100K is more common more recently
    if device is None:
        device = self.transformer.wte.weight.device
    channel_range = torch.arange(0, head_dim, 2, dtype=torch.float32, device=device)
    inv_freq = 1.0 / (base ** (channel_range / head_dim))
    t = torch.arange(seq_len, dtype=torch.float32, device=device)
    freqs = torch.outer(t, inv_freq)
    cos, sin = freqs.cos(), freqs.sin()
    cos, sin = cos.to(COMPUTE_DTYPE), sin.to(COMPUTE_DTYPE)
    cos, sin = cos[None, :, None, :], sin[None, :, None, :]
    return cos, sin
```

핵심은 `inv_freq = 1.0 / (base ** (channel_range / head_dim))`이다. base를 채널마다 다른 지수로 나눠 *주파수를 채널마다 다르게* 만든다. 그리고 시간 축 `t`와 외적해서 `(seq_len, head_dim/2)` 모양의 frequency 행렬을 만든다. cos와 sin을 취해서 `apply_rotary_emb`에 넘길 수 있게 한다.

여기서 `base=100000`이 흥미롭다. 원전 RoPE 논문은 `base=10000`을 썼다. GPT-NeoX와 초기 Llama도 10000을 그대로 가져갔다. 그런데 최근 *긴 컨텍스트*가 표준이 되면서 100K 이상이 흔해졌다. 왜?

직관적으로 설명하면 이렇다. 작은 base는 *주파수가 빠르게 변한다*. 빠르게 변하는 주파수는 가까운 거리를 잘 구별하지만, 먼 거리에서는 *주기가 한 바퀴 돌아버려서 정보가 깨진다*. 큰 base를 쓰면 주파수가 천천히 변해서 *더 긴 거리까지 잘 구별*된다. nanochat은 2K context지만 100K base를 *미리* 쓴다. 나중에 long context로 확장할 여지를 남기는 거다.

코드 마지막 두 줄도 짚어두자. `cos, sin = cos[None, :, None, :], sin[None, :, None, :]`. shape가 `(1, seq_len, 1, head_dim/2)`로 바뀐다. 왜 `None`을 두 번 끼우나? 나중에 attention forward에서 q와 k의 shape가 `(B, T, H, D)`이니까, broadcasting을 위해 batch와 head 축을 미리 비워두는 거다. 메모리는 그대로지만 broadcasting이 깔끔해진다.

한 가지 더. `register_buffer("cos", cos, persistent=False)`로 등록한다(199번 줄). `persistent=False`라는 게 의미가 있다. 체크포인트에 *저장하지 않는다*. 어차피 결정적 함수로 다시 계산할 수 있는 텐서를 저장할 이유가 없다. 체크포인트 파일이 *그만큼* 작아진다.

### 4-3. QK norm — 분산을 다시 잡는다

RoPE를 적용한 후에 `q, k = norm(q), norm(k)`가 한 줄 등장한다. QK norm이다.

이건 무엇을 하는가? RoPE는 회전이지 normalization이 아니다. 회전이 끝나면 q와 k의 norm은 *원래 그대로* 유지된다. 그런데 학습이 진행되면서 c_q, c_k의 weight가 자라면 q와 k의 norm도 같이 자란다. q와 k의 norm이 너무 크면 *attention softmax가 발산*한다. 한 토큰에만 거의 100% 확률이 몰리는 상태. 그게 attention sink라고 부르는 병이다.

QK norm은 그 병을 막는 *값싼 처방*이다. RoPE 직후에 q와 k를 *각각* RMSNorm으로 한 번 통과시켜 norm을 1로 강제한다. softmax 안에 들어가는 dot product의 magnitude가 *항상 일정한 분포*가 된다.

Henry et al. 2020에서 처음 제안됐고, Llama 3, Gemma 2, Qwen 2 등 최근 모델들이 거의 다 도입했다. *최근 표준*이다. nanochat이 modded-nanoGPT 커뮤니티에서 가져온 결정 중 하나다.

### 4-4. 1.2× sharpening — 작은 트릭

QK norm 직후에 한 줄 더 있다. `q = q * 1.2; k = k * 1.2`.

이건 *임시 처방*에 가깝다. 코드 주석을 보자.

```python
q = q * 1.2  # sharper attention (split scale between Q and K), TODO think through better
k = k * 1.2
```

`TODO think through better`. 카르파시 본인이 *더 좋은 방법을 찾아봐야겠다*고 적어둔 줄이다. 솔직함이 보인다.

무엇을 하는가? QK norm으로 q와 k의 norm이 1이 됐다. 그러면 dot product `q · k`의 분포가 너무 *평평*해진다 — 모든 토큰이 비슷하게 attend되는 *상태*. 그건 attention이 *아무 정보도 안 주는* 상태에 가깝다. 그래서 약간의 sharpening이 필요하다. q와 k를 각각 1.2배 키워서 dot product를 1.44배로 만든다. softmax가 더 sharp해진다.

왜 1.2인가? 실험적으로 찾은 값일 가능성이 높다. 더 큰 값(1.5, 2.0)을 쓰면 sharp해지지만 *발산 위험*이 다시 올라간다. 1.2가 균형점이다.

이 한 줄짜리 트릭이 *학습 안정성*에 의외로 큰 차이를 만든다. modded-nanoGPT 커뮤니티의 실험 결과다. 그러니까 일단 가져와서 쓰는데, 카르파시는 *왜* 1.2가 좋은지에 대한 *이론적 답*은 아직 없다고 솔직하게 적어둔 거다.

### 4-5. Flash Attention 디스패치

QK norm과 sharpening이 끝나면 `flash_attn.flash_attn_func(q, k, v, causal=True, window_size=window_size)`가 호출된다.

이건 단순한 wrapper다. SM 90 이상(H100)에서는 FA3 커널, 그 외에는 PyTorch SDPA fallback. *작은 모델*을 CPU에서 돌릴 때 우리가 만나는 건 SDPA fallback이다. window_size는 4B 주제니까 지금은 *full attention*이라고 가정하자.

여기서 한 가지만 짚자. SDPA fallback이 *왜* 끔찍해질 수 있는가? `flash_attention.py`의 경고를 보자.

```python
# nanochat/flash_attention.py에서 (요지)
# FA3는 bf16/fp8만 지원. fp16/fp32 학습은 SDPA 강제.
# SDPA에서 sliding window는 explicit mask로 구현 → 효율 끔찍.
```

sliding window가 *없으면* SDPA fallback이 그래도 견딜 만하다. *있으면* explicit mask를 만들어야 해서 메모리도, 속도도 *난감*해진다. 이건 4B에서 자세히 본다.

### 4-6. 출력 프로젝션

마지막은 `y = self.c_proj(y)`. attention 출력을 다시 `n_embd` 차원으로 프로젝트한다. 이게 residual stream에 더해진다.

`c_proj`의 init이 *제로*라는 사실은 잠시 후에 본다. 매 layer마다 attention이 *학습 초기에 residual stream을 건드리지 않는다*는 결정이다.

여기까지가 CausalSelfAttention의 골격이다. 62줄 중에 우리가 본 건 약 40줄. 나머지 22줄(value embedding gate와 inference 경로)은 4B와 10장에서 본다.

## 5. MLP — ReLU² 다섯 줄

MLP는 정말 단순하다. 12줄이다.

```python
# nanochat/gpt.py:129-140
class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc = Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.c_proj = Linear(4 * config.n_embd, config.n_embd, bias=False)

    def forward(self, x):
        x = self.c_fc(x)
        x = F.relu(x).square()
        x = self.c_proj(x)
        return x
```

forward가 다섯 줄, 그중 핵심은 한 줄이다.

> `x = F.relu(x).square()`

이게 ReLU²다. 그냥 ReLU에 제곱을 한 번 더 씌운 것. 음수는 0으로 깎고, 양수는 제곱한다.

여기서 *기본 결정*이 두 개 있다. *hidden size*와 *activation*이다.

`c_fc`가 `n_embd`를 `4 * n_embd`로 키운다. 이게 transformer MLP의 표준이다. Vaswani 2017부터 거의 모든 모델이 4× hidden을 쓴다. 작은 모델에서 이 비율을 줄여보는 실험이 가끔 있지만, 4×가 *충분히 검증된 안전한 선택*이다.

그리고 activation. *왜 ReLU²인가?*

원형 트랜스포머는 ReLU를 썼다. GPT-2는 GELU로 옮겼다. Llama와 PaLM은 SwiGLU로 옮겼다. *현대 LLM의 사실상 표준은 SwiGLU다*. 그런데 nanochat은 ReLU²를 쓴다. 왜?

여기에 두 가지 이유가 있다.

첫째, *파라미터 수*다. SwiGLU는 게이트 메커니즘이다. `swiglu(x) = (W_gate · x) * silu(W_up · x)`. 게이트와 up이 *두 개의 linear*다. 그래서 SwiGLU MLP는 `n_embd → ~2.67 * n_embd → n_embd`로 *세 개의 linear*를 쓴다. hidden을 4× 그대로 두려면 `n_embd → 4 * n_embd → 4 * n_embd → n_embd`로 세 개의 큰 linear가 필요하다. 파라미터가 *늘어난다*. 작은 모델에서 부담이다.

ReLU²는 게이트가 없다. linear 두 개로 끝난다. 같은 4× hidden을 *훨씬 적은 파라미터*로 쓴다.

둘째, *작은 모델에서의 성능*이다. So et al.의 "Primer" 논문([arXiv 2109.08668](https://arxiv.org/abs/2109.08668), 2021)이 자동화된 architecture search로 ReLU²를 찾았다. *ReLU의 제곱*이 GELU와 비슷하거나 *살짝 더 좋은* 성능을 보고했다. 이후 modded-nanoGPT 커뮤니티가 작은 모델에서 광범위하게 검증했다. 결론은 *작은 모델 친화적*이라는 것.

물론 큰 모델로 가면 SwiGLU가 다시 우세할 수 있다. 카르파시도 그걸 알고 있다. 하지만 d24 정도의 *small/medium* 모델에서는 ReLU²가 *충분히 좋고 충분히 가볍다*. 그러니 nanochat은 ReLU²를 선택했다.

코드 한 줄로 끝낸다는 단순함도 매력이다. `F.relu(x).square()`. SwiGLU를 쓰려면 게이트 linear를 더 정의하고, `silu`와 곱셈을 더 짜야 한다. 한 줄이 다섯 줄로 늘어난다. 작은 모델에서 그만한 가치를 안 한다고 본 거다.

## 6. norm — RMSNorm, learnable γ 없음

이제 한 발 물러서서 *normalization*을 본다. 코드는 두 줄이다.

```python
# nanochat/gpt.py:42-43
def norm(x):
    return F.rms_norm(x, (x.size(-1),))  # note that this will run in bf16, seems ok
```

두 줄. nn.Module이 아니라 *함수*다. *learnable parameter가 없다.*

원형 트랜스포머는 LayerNorm을 썼다. `LN(x) = γ * (x - μ) / σ + β`. mean centering, variance scaling, 그리고 *learnable* γ와 β. 네 개의 연산이 들어간다.

RMSNorm(Zhang & Sennrich, NeurIPS 2019, [arXiv 1910.07467](https://arxiv.org/abs/1910.07467))은 mean centering과 β를 *뺐다*. `RMS(x) = γ * x / sqrt(mean(x²))`. *root mean square*로만 정규화한다. 그게 다다. LayerNorm 비용의 30%로 90%의 효과를 본다.

여기까지가 *RMSNorm의 표준*이다. Llama, Mistral, Gemma 모두 이 형태다. learnable γ는 *남겨두는 것*이 보통이다.

그런데 nanochat은 γ도 뺐다.

> *왜 learnable γ를 뺐는가?*

코드 상단의 주석이 답한다.

```python
# nanochat/gpt.py:9
# no learnable params in rmsnorm
```

이건 *작은 모델에 대한 관찰*에서 나온 결정이다. modded-nanoGPT 커뮤니티가 발견한 사실 — *작은 모델에서 RMSNorm의 γ는 학습 후에도 거의 1에 머문다*. 그러니까 γ가 *학습되지 않는다*. 학습되지 않는 파라미터를 두는 건 *낭비*다. 옵티마이저는 그 γ를 계속 update하면서 momentum, variance까지 들고 다닌다. 다 그냥 비용이다.

빼버리면 어떻게 되나? `F.rms_norm(x, (x.size(-1),))` 한 줄로 끝난다. 함수가 nn.Module일 필요도 없다. *돈이 든 게 없는 정규화*다.

물론 큰 모델에서는 γ가 *학습되기* 시작할 수 있다. layer마다 norm의 강도를 다르게 만드는 게 필요해진다. 그때는 다시 γ를 넣어야 한다. 하지만 nanochat은 *그 단계가 아니다*. 그래서 뺐다.

그리고 한 가지 더. 코드 주석의 *seems ok*가 재밌다.

> `# note that this will run in bf16, seems ok`

`F.rms_norm`은 입력 dtype을 따른다. 입력이 bf16이면 RMS 계산도 bf16에서 돈다. RMS는 *분산*을 계산하니까 *정밀도가 떨어지면* 위험할 수 있다. 큰 모델에서는 RMSNorm을 fp32로 *casting up*해서 돌리는 게 안전한 관례다. 그런데 nanochat은 *bf16 그대로* 돌린다. 작동한다고 한다. *seems ok*. 카르파시 식 솔직함이다.

이건 작은 모델이라 가능한 결정이기도 하다. dimension이 작으면(768) bf16의 정밀도 손실이 RMSNorm 안에서 누적되어도 그 절대값이 크지 않다. *seems ok*는 *충분히 검증됐고 위험 없다*는 뜻이다.

## 7. lm_head와 logit softcap — untied embedding + Gemma-2 식 안정화

block을 다 통과하면 `lm_head`로 간다. `n_embd → vocab_size` linear다.

```python
# nanochat/gpt.py:175
self.lm_head = Linear(config.n_embd, padded_vocab_size, bias=False)
```

bias 없음. 그리고 *padded_vocab_size*. 한 줄 위에 padding 로직이 있다.

```python
# nanochat/gpt.py:166-170
padded_vocab_size = ((config.vocab_size + pad_vocab_size_to - 1) // pad_vocab_size_to) * pad_vocab_size_to
if padded_vocab_size != config.vocab_size:
    print0(f"Padding vocab_size from {config.vocab_size} to {padded_vocab_size} for efficiency")
```

`pad_vocab_size_to=64`. vocab_size를 64의 배수로 올린다. 32,768은 이미 64의 배수라 padding이 필요 없지만, 다른 크기를 쓰면 자동으로 패딩된다. *DDP와 tensor core를 위한 최적화*다. tensor core는 차원이 8 또는 16의 배수일 때 가장 빠르고, DDP all-reduce도 align되어야 효율적이다. 64면 충분히 안전하다.

forward에서 lm_head를 거친 후 *padding을 잘라낸다*.

```python
# nanochat/gpt.py:469-470
logits = self.lm_head(x)  # (B, T, padded_vocab_size)
logits = logits[..., :self.config.vocab_size]  # slice to remove padding
```

padded는 학습용, 출력은 *진짜 vocab 크기*. 그러니까 padding은 *내부 최적화*일 뿐, 모델의 의미적 vocab 크기는 그대로다.

이제 *untied embedding*에 대한 결정을 짚자. nanochat의 `wte`와 `lm_head`는 *별개 weight*다. weight tying을 안 했다.

원형 GPT-2는 tie했다. `lm_head.weight = wte.weight.T`. embedding과 unembedding이 *같은 행렬*을 공유한다. 파라미터를 절반 아낀다. 작은 모델에서는 의미가 있는 결정이다.

그런데 nanochat은 *안* tie했다. 왜?

이 부분은 카르파시의 일관된 입장이다. *작은 모델에서 weight tying의 가성비는 떨어진다*. embedding과 unembedding은 *비대칭적인 일*을 한다. embedding은 "토큰 ID → 의미 벡터", unembedding은 "의미 벡터 → 토큰 ID 확률". 같은 행렬로 두 일을 다 잘하기는 *어렵다*. 분리해두면 각자 자기 일을 잘하게 학습된다.

물론 파라미터는 늘어난다. 32K × 768 = 25M개 정도. d12 전체 약 150M 중 *17%*. 작지 않다. 하지만 그만한 값을 한다는 게 modded-nanoGPT의 발견이고, nanochat은 그걸 가져왔다.

lm_head를 통과한 후 마지막 한 가지가 남았다. *logit softcap*이다.

```python
# nanochat/gpt.py:468-472
softcap = 15  # smoothly cap the logits to the range [-softcap, softcap]
logits = self.lm_head(x)
logits = logits[..., :self.config.vocab_size]
logits = logits.float()  # switch to fp32 for logit softcap and loss computation
logits = softcap * torch.tanh(logits / softcap)  # squash the logits
```

`15 * tanh(logits / 15)`. logits을 [-15, 15] 범위로 *부드럽게 묶는다*. tanh는 매끄러운 saturating 함수니까 *경계에서 튀지 않는다*.

이건 Gemma-2가 도입한 트릭이다. 큰 모델은 학습 중에 어떤 토큰의 logit이 *폭발적으로 커지는* 일이 종종 있다. 한 토큰의 logit이 100, 다른 토큰들은 0이면 softmax 후에 그 토큰이 100% 확률을 받는다. cross-entropy loss는 *log(1) = 0*이라 gradient가 거의 안 흐른다. 학습이 멈춘다. 더 나쁘게는, 폭발한 logit이 *fp16/bf16 overflow*를 일으키기도 한다.

softcap은 그 폭발을 *부드럽게* 막는다. 어떤 logit이든 15를 못 넘는다. 그리고 *fp32*에서 한다. `logits.float()`로 dtype을 올린 다음 softcap을 적용한다. 정밀도가 중요한 마지막 단계니까 *fp32에서 안전하게* 처리하는 거다.

그리고 cross-entropy도 fp32에서 돈다.

```python
# nanochat/gpt.py:477
loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1, reduction=loss_reduction)
```

`ignore_index=-1`도 짚어두자. SFT에서 *어시스턴트가 학습받지 말아야 할 토큰*은 target을 -1로 마스킹한다. 그러면 cross-entropy가 그 위치를 무시한다. 토크나이저의 `render_conversation`이 mask=0 토큰을 -1로 만들어서 넘긴다. 그 연결고리가 여기서 끝난다.

## 8. init_weights — meta device, std=0.8, std=0.001

골격을 거의 다 봤다. 이제 *초기화*다. 모델이 처음 만들어졌을 때 weight가 어떤 값으로 시작하는지가 학습의 운명을 결정한다.

nanochat의 초기화는 한 가지 *영리한 패턴*과 *세 가지 결정적 값*으로 구성된다.

먼저 *영리한 패턴*. `GPT.__init__`의 docstring을 보자.

```python
# nanochat/gpt.py:154-160 (발췌)
class GPT(nn.Module):
    def __init__(self, config, pad_vocab_size_to=64):
        """
        NOTE a major footgun: this __init__ function runs in meta device context (!!)
        Therefore, any calculations inside here are shapes and dtypes only, no actual data.
        => We actually initialize all data (parameters, buffers, etc.) in init_weights() instead.
        """
```

`__init__`이 *meta device*에서 돈다. meta device는 *shape와 dtype만 있고 실제 데이터는 없는 가짜 device*다. 모든 텐서가 *0바이트*를 점유한다.

이게 왜 영리한가? *큰 모델의 메모리 spike를 피하기 위해서*다. d24 모델의 파라미터는 약 560M개, fp32로 2.2GB. `__init__`에서 모든 텐서를 fp32 CPU에 만들면 *그 2.2GB가 일단 한 번 RAM에 잡힌다*. 그 다음에 device로 옮기고 init_weights를 부르면 다시 GPU에 *또 2.2GB*가 잡힌다. CPU에서 GPU로 옮기는 순간 *4.4GB를 동시에* 들고 있게 된다. 더 큰 모델이면 메모리가 *터진다*.

meta device를 쓰면 `__init__`에서 *0바이트*만 점유한다. 그 다음 `model.to_empty(device='cuda')`로 GPU에 *빈 텐서*를 할당한다. 마지막에 `init_weights()`로 *실제 값을 채워 넣는다*. 메모리 spike가 없다.

이게 nanochat이 채택한 패턴이다. `scripts/base_train.py`의 `build_model_meta`가 이 흐름을 정확히 따른다.

```python
# 흐름 요약 (scripts/base_train.py에서)
with torch.device('meta'):
    model = GPT(config)
model.to_empty(device=device)
model.init_weights()
```

세 줄. 큰 모델이 메모리 터지는 *난감한* 일을 피하는 깔끔한 방법이다.

이제 *세 가지 결정적 값*을 보자. `init_weights`의 핵심 부분이다.

```python
# nanochat/gpt.py:217-219 (발췌)
torch.nn.init.normal_(self.transformer.wte.weight, mean=0.0, std=0.8)
torch.nn.init.normal_(self.lm_head.weight, mean=0.0, std=0.001)

# Transformer blocks
n_embd = self.config.n_embd
s = 3**0.5 * n_embd**-0.5  # sqrt(3) multiplier makes sure Uniform achieves the same std as Normal
for block in self.transformer.h:
    torch.nn.init.uniform_(block.attn.c_q.weight, -s, s)
    torch.nn.init.uniform_(block.attn.c_k.weight, -s, s)
    torch.nn.init.uniform_(block.attn.c_v.weight, -s, s)
    torch.nn.init.zeros_(block.attn.c_proj.weight)
    torch.nn.init.uniform_(block.mlp.c_fc.weight, -s * 0.4, s * 0.4)
    torch.nn.init.zeros_(block.mlp.c_proj.weight)
```

세 가지 결정이 보인다.

**첫째, 임베딩 std=0.8.** 표준적인 PyTorch 임베딩 init은 std=1.0이다. nanochat은 *살짝 작게* 0.8로 시작한다. 임베딩이 너무 크면 RMSNorm을 거친 후에도 변동이 크다. 작게 시작하면 학습 초기에 *안정적*이다.

**둘째, lm_head std=0.001.** 이건 *극도로 작다*. 표준의 1/1000이다. 왜 이렇게 작은가? lm_head는 직접 logits을 만든다. logits이 학습 초기부터 크면 *softmax가 한 토큰에 몰린다*. 그러면 gradient가 다른 토큰들에 안 흐른다. 학습 초기에는 *모든 토큰의 logit이 거의 0*이어서 *균등한 분포*에서 시작해야 한다. std=0.001은 그걸 보장한다.

그리고 logit softcap과의 *조합*이 영리하다. lm_head std=0.001로 시작 → 학습이 진행되며 logits이 자란다 → softcap=15가 *천장을 막아준다*. 학습 초기와 후기 모두 안전한 경로다.

**셋째, projection weight = 0.** `c_proj`와 `mlp.c_proj`가 *제로*다. attention과 MLP의 *출력*이 학습 초기에 *0*이라는 뜻이다.

이게 무슨 의미인가? Block의 forward를 다시 보자.

```python
x = x + self.attn(norm(x), ve, cos_sin, window_size, kv_cache)
x = x + self.mlp(norm(x))
```

`x + attn(...)`. attn의 c_proj가 0이면 attn(...)도 0. 그러면 `x + 0 = x`. *residual stream을 건드리지 않는다*. MLP도 마찬가지.

학습 초기에 모든 block이 *identity function*이다. residual stream에 어떤 변형도 가하지 않는다. 임베딩이 그대로 lm_head로 흘러간다. 학습이 시작되면 *천천히* block의 c_proj가 0에서 멀어지면서 *비선형 변형*이 추가된다.

이게 *residual networks*의 핵심 직관이다. He et al. 2015의 ResNet에서 와 있다. *layer를 깊게 쌓아도 학습이 가능한 이유*. nanochat은 그 직관을 *극단까지* 활용한다.

그리고 한 가지 더, `mlp.c_fc`는 `s * 0.4`다. 표준의 0.4배. *왜?*

ReLU²의 특성 때문이다. ReLU²는 양수를 *제곱*하니까 *큰 값이 들어가면 출력이 더 커진다*. 일반 ReLU나 GELU보다 *분산이 더 빨리 커진다*. 그래서 입력을 *작게 시작*해서 분산을 잡아두는 거다. 0.4라는 숫자는 ReLU²의 분산 공식에서 유도된 *튜닝된* 값이다.

이 한 줄이 *기본 활성함수와 init의 결합*이다. activation을 바꾸면 init도 같이 바꿔야 한다는 *잊지 말아야 할* 원칙이다.

자, 정리하자. init_weights의 결정 세 가지.
- wte std=0.8 — *살짝 작게* 시작해 RMSNorm 후 안정적인 분포.
- lm_head std=0.001 — *거의 0*에서 시작해 logits이 학습 초기에 균등.
- c_proj/mlp.c_proj = 0 — block이 *identity*로 시작.

이게 작은 모델을 *안전하게 학습 가능한 상태*로 만든다.

그리고 ReLU²의 분산 보정으로 `mlp.c_fc`만 0.4배. *activation과 init의 결합*을 잊지 말자.

## 9. estimate_flops — PaLM 식, 한 토큰당 FLOPs

마지막은 FLOPs 계산이다. 챕터의 부제에 *FLOPs*가 들어 있는 이유가 있다. nanochat은 *scaling law*를 자동화한다 — depth를 정하면 *최적 토큰 수*가 자동으로 계산되어 나온다. 그러려면 한 토큰당 FLOPs를 *정확히* 알아야 한다.

```python
# nanochat/gpt.py:317-343
def estimate_flops(self):
    """
    Return the estimated FLOPs per token for the model (forward + backward).
    Each matmul weight parameter contributes 2 FLOPs (multiply *, accumulate +) in forward,
    and 2X that in backward => 2+4=6.
    ...
    """
    nparams = sum(p.numel() for p in self.parameters())
    # Exclude non-matmul params: embeddings and per-layer scalars
    value_embeds_numel = sum(ve.weight.numel() for ve in self.value_embeds.values())
    nparams_exclude = (self.transformer.wte.weight.numel() + value_embeds_numel +
                      self.resid_lambdas.numel() + self.x0_lambdas.numel() +
                      self.smear_gate.weight.numel() + self.smear_lambda.numel() + self.backout_lambda.numel())
    h, q, t = self.config.n_head, self.config.n_embd // self.config.n_head, self.config.sequence_len
    # Sum attention FLOPs per layer, accounting for sliding window
    attn_flops = 0
    for window_size in self.window_sizes:
        window = window_size[0]
        effective_seq = t if window < 0 else min(window, t)
        attn_flops += 12 * h * q * effective_seq
    num_flops_per_token = 6 * (nparams - nparams_exclude) + attn_flops
    return num_flops_per_token
```

핵심은 마지막 두 줄이다. `6 * (nparams - nparams_exclude) + attn_flops`.

PaLM 논문([arXiv 2204.02311](https://arxiv.org/abs/2204.02311))이 정리한 공식이다. *한 토큰을 forward + backward 처리할 때의 FLOPs*는 *매트릭스 파라미터 수의 6배*에 *attention의 quadratic term*을 더한 것.

왜 *6*인가? matmul 한 번에 한 weight 파라미터는 *2 FLOPs*(곱 한 번 + 더하기 한 번). forward에 2 FLOPs, backward는 *gradient와 입력* 두 가지를 다 계산해야 해서 *2배* — 즉 backward 4 FLOPs. forward + backward = 6 FLOPs per parameter per token. 그게 *6 × params*의 근거다.

`nparams_exclude`가 흥미롭다. *제외하는* 파라미터들이다.

- `wte` — *embedding lookup*은 matmul이 아니라 *인덱싱*이다. FLOPs로 안 친다.
- `value_embeds` — 같은 이유.
- `resid_lambdas`, `x0_lambdas`, `smear_gate`, `smear_lambda`, `backout_lambda` — *스칼라*. 곱셈 한두 번이라 무시 가능.

이런 *비-matmul* 파라미터를 빼고 *6× matmul params*를 한다.

그리고 attention의 *quadratic term*. `12 * h * q * t`. h는 head 수, q는 head_dim, t는 sequence_len. *왜 12인가?* attention 안에 `Q·K^T` matmul과 `softmax(...) · V` matmul, 두 개의 행렬 곱이 있다. 각각 `h * q * t` FLOPs per token. forward 2번, backward 4번 = *6배*. 두 matmul 모두 합치면 *12배*. 그래서 `12 * h * q * t`.

이건 *sequence length의 제곱*이 아니라 *제곱에 비례하는 텀을 token당으로 환산한* 값이다. attention의 총 FLOPs는 `t * 12 * h * q * t = 12 * h * q * t²`니까 *token당*은 `12 * h * q * t`다.

그런데 *sliding window*가 있으면 이 값이 줄어든다. window가 short이면 attention이 보는 *effective sequence length*가 짧다.

```python
for window_size in self.window_sizes:
    window = window_size[0]
    effective_seq = t if window < 0 else min(window, t)
    attn_flops += 12 * h * q * effective_seq
```

layer마다 effective_seq를 다르게 계산한다. window가 -1(= full)이면 t를 쓰고, short이면 그 window 크기를 쓴다. "SSSL" 패턴이면 세 layer는 short(512), 한 layer는 full(2048). attention FLOPs가 줄어든다.

sliding window 자체는 4B의 주제다. 여기서는 *FLOPs 계산이 layer별로 다를 수 있다*는 것만 짚어두자.

마지막 한 줄. `num_flops_per_token = 6 * (nparams - nparams_exclude) + attn_flops`. 이 값이 한 토큰을 *forward + backward*로 처리하는 데 드는 FLOPs다. 학습 중 *총 FLOPs*는 이걸 *총 토큰 수*로 곱하면 된다.

이 함수가 *왜 중요한가?* `base_train.py`가 `estimate_flops`를 호출해서 *MFU*(Model FLOPs Utilization)을 계산한다. MFU는 *우리가 GPU의 peak FLOPs 중 몇 %를 실제로 쓰고 있는가*. H100의 bf16 peak는 약 989 TFLOPS다. 우리가 step당 *얼마나의 FLOPs*를 돌리는지 알면, *얼마의 시간이 걸려야 하는지*를 알 수 있다. 실제 시간과 비교해서 MFU를 낸다.

좋은 MFU는 50% 정도. nanochat의 d24 speedrun이 이 근처를 친다. 이 *50%*가 한 GPU 노드 3시간 안에 GPT-2급 모델을 학습시키는 *물리적 근거*다.

그러니까 `estimate_flops`는 *측정의 단위*다. *우리가 무엇을 얼마나 잘 하고 있는지를 보는 자*다. 6장에서 wandb 그래프를 펴고 *MFU 곡선*을 들여다볼 때, 그 곡선의 분모가 여기서 나온다.

## 10. 골격을 한 호흡에 — 다시 forward

골격을 다 풀었다. 이제 *전체 forward를 한 호흡에* 다시 본다. 4A에서 본 것만으로 forward의 *큰 그림*을 그릴 수 있어야 한다.

```python
# nanochat/gpt.py:416-481 (4A 시점 — 4B 트릭은 회색 처리)
def forward(self, idx, targets=None, kv_cache=None, loss_reduction='mean'):
    B, T = idx.size()

    # 1. RoPE 사전 계산된 cos/sin을 현재 sequence 길이만큼 자르기
    T0 = 0 if kv_cache is None else kv_cache.get_pos()
    cos_sin = self.cos[:, T0:T0+T], self.sin[:, T0:T0+T]

    # 2. 토큰 임베딩 lookup + 첫 번째 norm
    x = self.transformer.wte(idx)
    x = x.to(COMPUTE_DTYPE)
    x = norm(x)

    # 3. smear (4B 주제 — 4A에서는 None과 같은 효과)
    # ...

    # 4. block을 n_layer번 통과
    x0 = x
    n_layer = self.config.n_layer
    backout_layer = n_layer // 2
    x_backout = None
    for i, block in enumerate(self.transformer.h):
        x = self.resid_lambdas[i] * x + self.x0_lambdas[i] * x0
        ve = self.value_embeds[str(i)](idx).to(x.dtype) if str(i) in self.value_embeds else None
        x = block(x, ve, cos_sin, self.window_sizes[i], kv_cache)
        if i == backout_layer:
            x_backout = x

    # 5. backout (4B 주제) + 최종 norm
    if x_backout is not None:
        x = x - self.backout_lambda.to(x.dtype) * x_backout
    x = norm(x)

    # 6. lm_head + softcap
    logits = self.lm_head(x)
    logits = logits[..., :self.config.vocab_size]
    logits = logits.float()
    logits = 15 * torch.tanh(logits / 15)

    # 7. loss 또는 logits 반환
    if targets is not None:
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1, reduction=loss_reduction)
        return loss
    else:
        return logits
```

일곱 단계다. 한 단계씩 우리가 본 것을 매칭해보자.

1. RoPE 사전 계산된 cos/sin 슬라이스 — `_precompute_rotary_embeddings`에서 만든 cache. 추론 시점에는 `kv_cache.get_pos()`로 *offset*해서 자른다 (10장에서 다시).
2. 임베딩 + norm — wte std=0.8로 init된 lookup, 직후에 RMSNorm.
3. smear — *4B*.
4. block 반복 — resid_lambdas, x0_lambdas, value_embeds는 *4B*. block 안에서 attention(RoPE → QK norm → 1.2× → FA) → MLP(ReLU²).
5. backout — *4B*. 그리고 최종 norm.
6. lm_head → padding crop → fp32 cast → softcap.
7. cross_entropy with `ignore_index=-1`.

*4A에서 우리가 손에 쥔 골격이 forward의 70%*를 차지한다. 나머지 30%가 4B의 일곱 가지 트릭이다.

골격은 이거다. *임베딩과 lm_head는 untied, 사이에는 pre-norm 트랜스포머 블록 n개, attention은 RoPE + QK norm + 1.2× + FA, MLP는 4× hidden + ReLU², 정규화는 learnable γ 없는 RMSNorm, 출력은 softcap*. Vaswani 2017과 비교하면 *모든* 결정이 갱신됐지만, *근본 구조*는 그대로다.

이게 *현대화된 트랜스포머의 골격*이다. Llama, Mistral, Gemma도 거의 같다. 작은 디테일이 다를 뿐. nanochat을 한 줄씩 읽으면 *현대 LLM의 기본기*가 손에 들어온다는 게 그래서 사실이다.

## 11. 실습 — d4 모델, window_pattern, init std 분포

이론은 충분히 봤다. 이제 *손에 쥐어보자*. 세 단계로 짠 30분 실습이다.

### 실습 (a) — d4 모델 meta init과 파라미터 수

먼저 가장 작은 모델을 meta device에서 만들어보자. CPU/MPS에서 *순식간*에 끝난다.

```python
# Python REPL 또는 짧은 스크립트
import torch
from nanochat.gpt import GPT, GPTConfig

config = GPTConfig(
    sequence_len=2048,
    vocab_size=32768,
    n_layer=4,        # d4 — 가장 작은 모델
    n_head=4,
    n_kv_head=4,
    n_embd=256,       # 작게
    window_pattern="SSSL",
)

# meta device에서 init
with torch.device('meta'):
    model = GPT(config)

# 실제 메모리 할당 (CPU에)
model.to_empty(device='cpu')
model.init_weights()

# 파라미터 수
total_params = sum(p.numel() for p in model.parameters())
print(f"Total params: {total_params / 1e6:.2f}M")

# FLOPs per token (forward + backward)
flops = model.estimate_flops()
print(f"FLOPs per token: {flops / 1e6:.2f}M")
```

출력 예시 (정확한 숫자는 환경에 따라 미세하게 다를 수 있다):

```
Total params: 17.40M
FLOPs per token: 86.32M
```

작은 d4 모델이 *17M 파라미터* 정도다. d24가 약 *560M*. depth가 6배 늘면 파라미터는 약 33배 늘어난다. width까지 같이 자라기 때문이다(`n_embd = 64 * depth`).

FLOPs per token이 *86M*. d4의 sequence_len=2048에서 한 토큰을 forward + backward 처리하는 데 약 86M FLOPs. 만약 12B 토큰을 학습한다면 총 FLOPs는 *86M × 12B = 약 1e18 FLOPs*. H100 한 장의 bf16 peak가 989 TFLOPS면 이론적으로 약 *1000초*. 50% MFU면 *2000초*, 약 33분. 작은 모델이라 *놀라울 정도로 빠르다*. (물론 d24는 이게 100배 늘어난다.)

### 실습 (b) — window_pattern을 "L"로 바꿔 mask shape 비교

이번엔 window_pattern을 바꿔보자. 4B의 sliding window 사전 준비다.

```python
config_sssl = GPTConfig(n_layer=4, n_head=4, n_kv_head=4, n_embd=256,
                       sequence_len=2048, window_pattern="SSSL")
config_l = GPTConfig(n_layer=4, n_head=4, n_kv_head=4, n_embd=256,
                    sequence_len=2048, window_pattern="L")

with torch.device('meta'):
    model_sssl = GPT(config_sssl)
    model_l = GPT(config_l)

print("SSSL pattern window_sizes:")
for i, ws in enumerate(model_sssl.window_sizes):
    print(f"  layer {i}: {ws}")

print("L pattern window_sizes:")
for i, ws in enumerate(model_l.window_sizes):
    print(f"  layer {i}: {ws}")

# FLOPs 비교
model_sssl.to_empty(device='cpu'); model_sssl.init_weights()
model_l.to_empty(device='cpu'); model_l.init_weights()
print(f"SSSL FLOPs/token: {model_sssl.estimate_flops() / 1e6:.2f}M")
print(f"L    FLOPs/token: {model_l.estimate_flops() / 1e6:.2f}M")
```

출력:

```
SSSL pattern window_sizes:
  layer 0: (512, 0)
  layer 1: (512, 0)
  layer 2: (512, 0)
  layer 3: (2048, 0)
L pattern window_sizes:
  layer 0: (2048, 0)
  layer 1: (2048, 0)
  layer 2: (2048, 0)
  layer 3: (2048, 0)
SSSL FLOPs/token: 76.18M
L    FLOPs/token: 86.32M
```

SSSL이 L보다 *FLOPs가 적다*. 세 layer가 short(512)이라 attention quadratic term이 줄어든 거다. 약 *12% 절약*. d4에서도 보이고, d24에서는 더 크게 보인다(약 25% 절약).

대신 SSSL은 *세 layer가 멀리 못 본다*. 마지막 layer만 full context. 정보 흐름이 *세 단계로 압축*된다. 이 trade-off가 *4B의 핵심 주제*다.

여기서 한 가지만 더 확인하자. `window_sizes`의 마지막 layer가 *항상* `(2048, 0)`이다. *L 패턴이든 SSSL 패턴이든*. 코드를 보면 알 수 있다.

```python
# nanochat/gpt.py:310-311
# Final layer always gets full context
window_sizes[-1] = (long_window, 0)
```

*기본 결정*이다. 마지막 layer는 *반드시* full context. 출력 직전에 *전체 정보를* 한 번은 통합해야 한다는 카르파시의 입장이다.

### 실습 (c) — init std=0.8 vs std=0.1, forward output 분포

마지막 실습. *임베딩 init std*를 바꿔보고 forward output 분포를 본다.

```python
import torch
import matplotlib.pyplot as plt
from nanochat.gpt import GPT, GPTConfig

config = GPTConfig(n_layer=4, n_head=4, n_kv_head=4, n_embd=256,
                  sequence_len=512, vocab_size=32768)

# 기본 init (std=0.8)
with torch.device('meta'):
    model_default = GPT(config)
model_default.to_empty(device='cpu')
model_default.init_weights()

# init_weights에서 임베딩 std를 0.1로 바꾼 모델
with torch.device('meta'):
    model_small = GPT(config)
model_small.to_empty(device='cpu')
model_small.init_weights()
# 임베딩만 다시 init
torch.nn.init.normal_(model_small.transformer.wte.weight, mean=0.0, std=0.1)

# 동일한 입력으로 forward
idx = torch.randint(0, 32768, (1, 256))

# 학습 모드를 끄지 않으면 dropout 등이 영향을 줄 수 있는데,
# nanochat GPT는 dropout이 없으니 그대로 forward.
with torch.no_grad():
    logits_default = model_default(idx)  # (1, 256, 32768)
    logits_small = model_small(idx)

print(f"std=0.8: logits mean={logits_default.mean():.4f}, std={logits_default.std():.4f}")
print(f"std=0.1: logits mean={logits_small.mean():.4f}, std={logits_small.std():.4f}")

# 히스토그램
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(logits_default.flatten().numpy(), bins=100)
axes[0].set_title("Embedding std=0.8 (default)")
axes[1].hist(logits_small.flatten().numpy(), bins=100)
axes[1].set_title("Embedding std=0.1")
plt.show()
```

출력 (예시 — 실제 값은 임베딩의 랜덤 시드에 따라 다르다):

```
std=0.8: logits mean=0.0000, std=0.0008
std=0.1: logits mean=0.0000, std=0.0001
```

두 경우 모두 logits의 *평균은 0 근처*다. lm_head std=0.001과 projection weight=0의 *조합* 덕분이다. block들이 *identity*로 시작하니까 임베딩 std가 달라도 *최종 logits은 lm_head에 의해 0 근처로 깎인다*.

차이는 *std*에 있다. std=0.8에서 logits.std가 *0.0008*, std=0.1에서는 *0.0001*. 약 8배 차이. 임베딩이 커지면 RMSNorm이 *정규화*하지만, 그 정규화된 값이 block을 통과하면서 *분산이 누적*된다. 마지막 lm_head에서 그 분산이 logits으로 흘러나온다.

히스토그램을 보면 std=0.8 쪽이 *조금 더 넓게 퍼진다*. 학습이 시작될 때 *gradient signal*이 더 크게 흐른다. 학습 초반의 *속도 차이*로 이어진다.

물론 학습이 길어지면 두 init이 *비슷한 곳*에 수렴할 가능성이 높다. 하지만 *초기 수렴 안정성*에서는 차이가 난다. modded-nanoGPT 커뮤니티가 *작은 모델에서 std=0.8이 가장 안정적*이라고 검증했다.

이 실습으로 우리가 손에 쥔 것 하나. *init은 학습 시작점의 분포를 결정한다*. 그 분포가 *안전한* 범위 안에 있어야 학습이 잘 시작된다. 한 줄짜리 결정이 모델 운명의 *첫 한 발*을 결정한다.

## 12. 마무리 — 골격은 봤다, 이제 트릭이다

골격을 다 풀었다. 한 번 정리해보자.

*기본 결정*이 다섯 가지였다.

1. **RoPE** — sinusoidal/learned 대신 회전 기반 상대 위치. `base=100000`으로 긴 컨텍스트를 미리 준비.
2. **RMSNorm without γ** — LayerNorm의 30% 비용, learnable parameter 0.
3. **QK norm + 1.2× sharpening** — attention 안정화의 값싼 처방.
4. **ReLU²** — SwiGLU 대신, 작은 모델에 *친화적*이고 *코드도 짧다*.
5. **Untied embedding** — wte와 lm_head 분리, 작은 모델에서도 *값을 한다*.

그리고 *영리한 패턴*과 *결정적 값*이 셋이었다.

1. **Meta device init** — `__init__`은 shape만, 실제 init은 `to_empty` + `init_weights`. 메모리 spike 회피.
2. **wte std=0.8, lm_head std=0.001** — embedding은 살짝 작게, lm_head는 거의 0.
3. **c_proj/mlp.c_proj=0** — block이 *identity*로 시작.

그리고 마지막 *측정의 단위*.

- **estimate_flops** — PaLM 식 6N + 12hq × effective_seq. MFU의 분모이자 scaling law의 입력.

이게 4A에서 우리가 손에 쥐어야 할 *골격*이다. forward의 70%를 이걸로 그릴 수 있다.

그런데 카르파시는 여기에 *일곱 가지 트릭*을 더 더했다. value embeddings(ResFormer), per-layer learnable scalars(resid_lambdas와 x0_lambdas), smear, backout, sliding window attention, untied embedding의 부수 효과, logit softcap의 fp32 처리. 그중 untied embedding과 softcap은 이미 봤지만, 다섯 가지는 아직 그림자만 보였다.

다음 챕터에서 그걸 본다. modded-nanoGPT 커뮤니티가 *작은 모델에 더한* 일곱 가지 패치. 4B의 주제다. 차 한 잔 마시고 가자.
