# 10장. 추론은 다른 모드의 모델이다 — Engine, KV cache, 도구 호출, 그리고 대화

우리의 모델은 학습이 끝났다. 사전학습으로 *세상을 읽는 법*을 배웠고, SFT로 *대화의 형식*을 익혔고, RL로 *수학을 잘하는 길*까지 한 번 더 다듬었다. 체크포인트 디렉터리에는 가중치가 가지런히 누워 있다. 그런데 막상 우리가 *그 모델과 대화*하려고 손을 뻗는 순간, 묘한 사실 하나가 드러난다.

학습 시점의 모델과 추론 시점의 모델은 *같은 nn.Module인데도 작동 방식이 다르다*.

학습 시에는 토큰 시퀀스가 *한 덩어리*로 들어간다. 길이 2048의 시퀀스에 한 번에 forward를 한 번 돌리고, 모든 위치의 logits을 받아서, shift된 정답과 cross entropy를 쳐서 backward한다. 한 GPU step의 일이다. 그런데 *대화*는 그렇게 진행되지 않는다. 우리가 "9 곱하기 8은?"이라고 묻는 순간, 모델은 그 prompt를 한 번에 받아 *처음 토큰을 뱉기 시작*하고, 그 다음부터는 자기가 뱉은 토큰을 받아서 *다음 토큰을 뱉고*, 또 그 다음 토큰을 뱉는다. 한 토큰씩, 자기 입에서 나온 것을 다시 입력으로 받는 *autoregressive* 흐름이다.

이게 학습 코드를 그대로 추론에 갖다 쓰면 *끔찍하게 느린* 이유다. 길이 100의 응답을 만들려면, naive하게는 100번 forward를 돌려야 하고, 매번 *과거 99개 토큰의 attention을 전부 다시* 계산해야 한다. 누가 봐도 낭비다. 어제까지의 K·V는 변하지 않았는데, 매번 처음부터 다시 곱하고 있다.

그러니 추론은 *다른 모드의 모델*이라고 부르는 편이 정직하다. 같은 가중치, 같은 nn.Module, 그러나 *다른 인프라*. 그 인프라가 `nanochat/engine.py` 357줄이고, 거기에 KV cache와 tool use FSM이 들어 있다. 이 챕터에서 그 357줄을 한 줄도 빠뜨리지 않고 따라가본다. 그러고 나면 마지막에 *우리가 직접 만든 모델과 한 번 대화*해본다. 책의 정점에 도착한 셈이다.

## 10.1 학습과 추론, 같은 nn.Module의 두 얼굴

먼저 *왜* 두 얼굴인지부터 정리하자. 학습 forward와 추론 forward가 어떻게 다른지를 한 그림으로 그려두면 KV cache가 *왜 필요한가*가 자연스럽게 떠오른다.

학습 시 forward는 이런 모습이다. 배치 B개의 시퀀스, 각각 길이 T가 한 덩어리로 들어간다. 모든 위치 t에 대해 attention 행렬 `Q_t · K_{1..t}^T`가 한꺼번에 계산된다. causal mask로 미래를 가리고, softmax, V와의 weighted sum. 모든 T개 위치의 logits이 나온다. 그걸 정답과 비교해 loss. 한 번의 forward에 GPU의 SM이 가득 차고, 멋지게 *MFU 50%*가 찍힌다.

추론 시 forward는 *어떤* 모습이어야 하는가? 우리가 "프랑스 수도는?"이라고 물었다고 해보자. 모델은 prompt 6 토큰을 받아서 첫 번째 답 토큰("Paris")을 뱉어야 한다. 그러려면 그 6 토큰 사이의 attention을 한 번은 *반드시* 다 계산해야 한다. 학습 forward와 같은 일이다. 이걸 **prefill** 단계라고 부른다 — *prompt를 채워 넣는다(prefill)*는 뜻이다.

그런데 그 다음이 문제다. "Paris" 다음 토큰을 뱉으려면, 모델 입장에서는 *7번째 토큰*의 Q를 새로 만들어 *1~6번째의 K·V*와 attention을 친다. 그런데 1~6번째의 K·V는 prefill 때 이미 계산해두지 않았던가. 다시 계산할 이유가 없다. 그저 *저장해뒀다가 꺼내 쓰면 된다*.

이게 KV cache의 핵심 직관이다. *prompt 단계에서는 한꺼번에 attention을 친다. 그 결과 K·V를 캐싱한다. 그 다음부터는 한 토큰씩 새로운 Q만 만들어 캐시된 K·V와 attention을 친다.* 이 두 번째 단계를 **decode** 단계라고 부른다.

prefill과 decode의 비대칭을 한 번 짚어두자. prefill은 *시퀀스 길이가 6 이상*인 한 번의 forward다. attention의 행렬 곱이 `T_prompt × T_prompt`라서 GPU가 멋지게 바쁘다. compute-bound이다. 반대로 decode는 매번 *시퀀스 길이 1*의 forward다. Q가 (1, n_head, head_dim) 한 토막이고, K·V는 캐시에서 꺼낸다. matmul이 작아져서, 정작 GPU는 *데이터 옮기는 데 시간을 다 쓴다*. memory-bound이다. tok/sec가 GPU 메모리 대역폭에 묶이는 시점이 여기다.

이 비대칭은 LLM serving 전체의 *경제학*을 결정한다. prefill은 compute-bound라서 *batch size를 늘리면 거의 공짜*다. decode는 memory-bound라서 *batch size를 늘려야 비로소 GPU가 일을 한다*. 그래서 큰 serving 시스템들은 prefill과 decode를 분리해서 다른 GPU에 보내기도 한다. nanochat은 그 단계까지 가지 않는다. 한 GPU 안에서 둘 다 하되, *KV cache를 잘 두는 일*만 한다. 그 정도면 우리가 공부하기에는 충분하다.

한 가지 더 짚어두자. *학습은 단방향*이지만 *추론은 양방향 대화*다. 학습 시 모델은 *대량의 시퀀스를 한 번 보고 가중치를 업데이트*한다. 같은 batch를 다시 볼 일이 없다(epoch을 돈다면 모를까). 반면 추론은 *한 번 응답한 다음 다시 사용자 입력을 기다린다*. 같은 대화의 다음 turn에서 *지금까지의 대화 토큰*을 *다시 forward에 통과*시켜야 한다.

여기서 KV cache의 *두 번째 역할*이 보인다. *대화 turn 사이에 KV cache를 들고 있을 수 있다면* — 두 번째 turn의 prefill은 *첫 turn의 끝에서 이어진다*. 새로운 user 입력만 *추가로 prefill*하면 된다. nanochat의 chat_cli/chat_web은 *그 최적화까지는 가지 않는다* — 매 turn 새로 prefill한다. *대화 길이가 짧고 작은 작품*이라 *큰 손해는 없다*. 하지만 *큰 시스템*에서는 KV cache를 *세션 단위*로 들고 다니며, *대화의 연속성*을 K·V의 연속성으로 푼다. 우리가 평소에 쓰는 ChatGPT가 *세션 안에서는 빠르게 응답*하는 이유 중 하나다.

자, 그렇다면 그 캐시를 *어떤 모양*으로 만들어야 하는가. 그게 다음 절이다.

## 10.2 KVCache — pre-allocated 텐서 한 덩어리

`engine.py:82-138`에 `KVCache` 클래스가 있다. 한눈에 다 들어오는 짧은 클래스다. 차분히 한 줄씩 보자.

```python
class KVCache:
    """
    KV Cache designed for Flash Attention 3's flash_attn_with_kvcache API.

    Key differences from FA2-style cache:
    - Tensors are (B, T, H, D) not (B, H, T, D)
    - FA3 updates the cache in-place during flash_attn_with_kvcache
    - Position tracked per batch element via cache_seqlens tensor
    """

    def __init__(self, batch_size, num_heads, seq_len, head_dim, num_layers, device, dtype):
        self.batch_size = batch_size
        self.max_seq_len = seq_len
        self.n_layers = num_layers
        self.n_heads = num_heads
        self.head_dim = head_dim
        # Pre-allocate cache tensors: (n_layers, B, T, H, D)
        self.k_cache = torch.zeros(num_layers, batch_size, seq_len, num_heads, head_dim, device=device, dtype=dtype)
        self.v_cache = torch.zeros(num_layers, batch_size, seq_len, num_heads, head_dim, device=device, dtype=dtype)
        # Current sequence length per batch element (FA3 needs int32)
        self.cache_seqlens = torch.zeros(batch_size, dtype=torch.int32, device=device)
        # Previous token's normalized embedding for smear (set by model forward pass)
        self.prev_embedding = None
```

읽고 나면 의외로 단순하다는 생각이 든다. *그냥 큰 텐서 두 개*다. `k_cache`와 `v_cache`가 각각 `(n_layers, B, T_max, n_kv_heads, head_dim)` 모양으로 **미리 할당**된다. n_layers는 모델의 트랜스포머 블록 수, B는 batch size(num_samples), T_max는 우리가 채울 수 있는 최대 토큰 길이, n_kv_heads는 GQA의 그 KV 헤드 수, head_dim은 헤드 차원이다. d24 모델 기준으로 (24, 1, 2048, 8, 64)쯤이 된다.

미리 할당하는 게 *왜* 중요한가? 추론 중에 매 토큰마다 `torch.cat`으로 캐시를 늘려가면 *매번 메모리 재할당*이 일어난다. GPU 메모리 할당은 비싸다. 그래서 *최대 길이만큼 한 번에 잡아두고, 안에서 in-place로 덮어쓴다*는 패턴이 표준이 됐다. 4장에서 본 trick — *공간을 미리 잡아 컴파일러가 안심하게 한다*는 패턴 — 이 여기서도 그대로 적용된다.

그 다음 줄이 더 흥미롭다.

```python
self.cache_seqlens = torch.zeros(batch_size, dtype=torch.int32, device=device)
```

`cache_seqlens`. **배치 요소마다 다른 위치를 추적**하는 int32 텐서다. 길이가 `batch_size`이고 dtype이 `torch.int32`라는 점이 깨알같이 중요하다.

왜 배치마다 다른 위치를 추적해야 하는가? RL 단계에서 우리는 num_samples=8 같은 식으로 *같은 prompt에서 여덟 개 응답을 병렬로 sampling*한다. 8개가 같은 길이로 끝나면 좋겠지만 *그럴 리가 없다*. 어떤 row는 30 토큰 만에 `<|assistant_end|>`를 뱉고 끝나고, 어떤 row는 200 토큰까지 가서야 끝난다. 그러니 *배치의 각 row가 서로 다른 위치까지 진행*해 있을 수 있어야 한다. 그 위치를 한 int32 스칼라로 row마다 들고 다닌다. FA3가 이 텐서를 받아서 *각 batch element마다 캐시의 어디까지가 valid인지*를 본다.

int32라는 점도 사소하지만 필요한 약속이다. FA3 커널이 *int32만 받는다*. 우리가 long으로 잘못 넣으면 커널이 에러를 뱉는다. 한 줄짜리 dtype 약속이지만 어겨보면 *난감하다*. 그러니 이 줄을 기억해두자.

마지막 한 줄, `self.prev_embedding`. 이건 nanochat 특유의 *smear* 메커니즘에서 쓰이는 보조 상태인데, 4A에서 본 토큰 임베딩 직후의 평균화 단계와 연결된다. 자세히 들어가지는 말자. 핵심은 *모델의 forward pass가 이 캐시 객체에 prev_embedding을 적어둔다*는 것 — 그러면 다음 step의 forward가 그걸 꺼내 쓴다 — 정도다.

### KVCache의 메서드 — get_pos, advance, prefill

KVCache는 데이터 그릇이기도 하지만 *몇 개의 짧은 메서드*도 갖고 있다. 모두가 의미가 있다.

```python
def reset(self):
    """Reset cache to empty state."""
    self.cache_seqlens.zero_()
    self.prev_embedding = None

def get_pos(self):
    """Get current position (assumes all batch elements at same position)."""
    return self.cache_seqlens[0].item()

def get_layer_cache(self, layer_idx):
    """Return (k_cache, v_cache) views for a specific layer."""
    return self.k_cache[layer_idx], self.v_cache[layer_idx]

def advance(self, num_tokens):
    """Advance the cache position by num_tokens."""
    self.cache_seqlens += num_tokens
```

`reset()`은 *전부 0으로 초기화*. 새 대화가 시작될 때 호출한다. 큰 텐서를 다시 할당하지 않고 *seqlen 카운터만 0으로 돌리는* 것이, 미리 할당 패턴이 가져다주는 깔끔한 결과다.

`get_pos()`는 *현재 위치 한 개*를 돌려준다. 주석을 보자 — *"assumes all batch elements at same position"*. 즉 RL의 num_samples 병렬 sampling 같은 *같은 prompt를 공유하는 케이스*에서만 의미가 있다. 다른 길이의 시퀀스를 한 캐시에 섞어 넣는 경우(paged attention 같은 것)에는 row마다 위치가 다르고, 그땐 `cache_seqlens` 텐서 전체를 봐야 한다. nanochat은 paged attention까지 가지 않는다 — *그건 우리가 짜는 작품이 아니다*.

`get_layer_cache(layer_idx)`. 각 트랜스포머 블록 안의 attention이 이걸 호출해서 *그 layer의 K·V 뷰*를 받아간다. n_layers 차원의 첫 인덱스를 떼고 (B, T_max, H, D) 뷰를 반환하는 단순한 연산이다.

`advance(num_tokens)`. 캐시 위치를 *그만큼 앞으로* 옮긴다. prefill에서는 `num_tokens=len(prompt)`으로, decode에서는 `num_tokens=1`로 호출된다. *모든 batch element가 같이 움직인다*. nanochat의 단순함이 여기서 또 드러난다 — 어떤 row가 일찍 끝나도 *캐시의 seqlen은 동기적으로 같이 증가*한다. 일찍 끝난 row가 캐시의 *유효하지 않은 영역*을 갖게 되는 셈인데, 그 부분은 row의 `completed` 플래그로 *그 행에 logits을 쓰는 일을 멈추는* 식으로 처리한다. paged attention 없이 사는 작은 작품의 깔끔한 선택이다.

마지막이 *클라이맥스급* 메서드, `prefill(other)`이다.

```python
def prefill(self, other):
    """
    Copy cached KV from another cache into this one.
    Used when we do batch=1 prefill and then want to generate multiple samples in parallel.
    """
    assert self.get_pos() == 0, "Cannot prefill a non-empty KV cache"
    assert self.n_layers == other.n_layers and self.n_heads == other.n_heads and self.head_dim == other.head_dim
    assert self.max_seq_len >= other.max_seq_len
    other_pos = other.get_pos()
    self.k_cache[:, :, :other_pos, :, :] = other.k_cache[:, :, :other_pos, :, :]
    self.v_cache[:, :, :other_pos, :, :] = other.v_cache[:, :, :other_pos, :, :]
    self.cache_seqlens.fill_(other_pos)
    # Copy smear state: expand batch=1 prev_embedding to num_samples
    if other.prev_embedding is not None:
        self.prev_embedding = other.prev_embedding.expand(self.batch_size, -1, -1).clone()
```

한 번에 안 들어오면 두 번 읽어보자. 비어 있는 *큰 캐시*가 *작은 캐시*의 내용을 *복제*해 채운다. 작은 캐시는 `batch_size=1`, 큰 캐시는 `batch_size=num_samples`. 즉 batch=1로 prompt를 한 번 prefill하고, 그 결과를 *N개로 broadcast 복제*하는 메커니즘이다.

이 한 메서드가 왜 멋지냐 하면 — *같은 prompt에서 N개 응답을 병렬 sampling*할 때 *prompt forward는 한 번만* 돌리면 된다는 뜻이기 때문이다. 8개 응답을 만들려고 8번 prefill을 돌리는 게 *처음 떠오르는 무딘 방식*이라면, prefill 한 번 + 복제 한 번이 *예리한 방식*이다. 9장 RL이 이 메커니즘을 그대로 빌려 쓴다. *같은 question의 K·V는 동일하니까, 한 번 계산하고 num_samples로 펴자.*

다섯 줄로 정리된 *parallel sampling 트릭*. nanochat이 *읽을 만한 작품*인 이유가 이런 곳에서 드러난다.

조금 더 깊이 들어가보자. *왜 batch=1로 한 번 prefill하고 복제*하는가? 처음부터 batch=N으로 prefill하면 안 되는가? 안 될 이유는 없다. 다만 *낭비*다. N개 row가 *같은 prompt 토큰*을 들고 있다면, *같은 K·V*가 N번 계산된다. attention의 prefill 비용이 `O(T_prompt² × n_layers × n_heads × head_dim)`인데, 그게 N배가 된다. *결과는 같은데*. 한 번 계산하고 N번 베끼는 게 *명백히 이득*이다.

복제 cost는 어떻게 되는가? `k_cache[:, :, :other_pos, :, :] = other.k_cache[:, :, :other_pos, :, :]`. GPU의 device-to-device 메모리 copy 한 번이다. 대역폭에 묶이지만 *attention forward 한 번보다 훨씬 싸다*. 그러니 *큰 prompt + 작은 N*에서도, *작은 prompt + 큰 N*에서도 *모두 이득*이다.

이런 트릭이 *모든 RL 학습 step*에서 동작한다는 사실이 중요하다. 9장에서 우리는 `chat_rl.py`가 한 question을 받아 num_samples=8 응답을 뽑고 reward를 매기는 것을 봤다. *그 num_samples 8*이 이 `prefill(other)` 한 줄로 만들어진다. *코드 한 줄이 학습 효율을 8배 가까이 살린다*. 작은 작품의 *예리한 부분*이다.

물론 *어떤 경우*에는 이 trick이 무용하다. 매 row가 *다른 prompt*를 갖는다면 — 즉 *batched serving*에서 N명의 사용자가 *서로 다른 질문*을 동시에 던질 때 — prefill을 *진짜로 N개 다른 시퀀스에 대해* 돌려야 한다. 그땐 paged attention 같은 *더 정교한 메모리 관리*가 필요해진다. nanochat은 그 단계까지 가지 않는다 — `chat_web`은 *사용자 한 명당 worker 한 개*를 주는 방식으로 *문제를 우회*한다. 같은 prompt를 공유하는 케이스가 *대화 안에서는 거의 없고*, RL 안에서는 *항상* 있다는 사실이 — 이 미니멀한 디자인을 받쳐준다.

## 10.3 sample_next_token — logits에서 한 토큰 뽑기

KVCache로 prefill·decode의 *기반*은 갖췄다. 그렇다면 매 decode step에서 *어떤 토큰을 뽑을 것인가*. `engine.py:140-156`이 그 일을 한다.

```python
@torch.inference_mode()
def sample_next_token(logits, rng, temperature=1.0, top_k=None):
    """Sample a single next token from given logits of shape (B, vocab_size). Returns (B, 1)."""
    assert temperature >= 0.0, "temperature must be non-negative"
    if temperature == 0.0:
        return torch.argmax(logits, dim=-1, keepdim=True)
    if top_k is not None and top_k > 0:
        k = min(top_k, logits.size(-1))
        vals, idx = torch.topk(logits, k, dim=-1)
        vals = vals / temperature
        probs = F.softmax(vals, dim=-1)
        choice = torch.multinomial(probs, num_samples=1, generator=rng)
        return idx.gather(1, choice)
    else:
        logits = logits / temperature
        probs = F.softmax(logits, dim=-1)
        return torch.multinomial(probs, num_samples=1, generator=rng)
```

세 갈래의 분기가 있다. 차분히 살펴보자.

첫째, `temperature == 0.0`이면 *argmax*. 그야말로 모델이 가장 높다고 생각하는 토큰을 곧이곧대로 뽑는다. greedy decoding이다. 평가 시 답을 *재현 가능하게* 받고 싶을 때 쓴다. 다양성은 0이다.

둘째, `top_k`가 주어졌으면 *상위 k개만 살리고* softmax. `torch.topk`로 상위 k 값과 인덱스를 꺼내고, 그 위에서 temperature로 분포를 부드럽게/날카롭게 만든 다음, multinomial sampling. *상위 k 밖의 토큰은 아예 후보에서 빼*는 단순하고 효과적인 방식이다. nanochat의 기본값은 top_k=50.

셋째, top_k가 없으면 *vocab 전체*에 temperature·softmax·multinomial. 가장 자유롭지만 *낮은 확률의 이상한 토큰*이 가끔 뽑힐 수 있다.

`temperature`가 무엇인가? logits을 나누는 스칼라다. temperature=1이면 그대로. temperature가 작아질수록 분포가 *날카로워지고*(승자독식), 커질수록 *평평해진다*(무작위에 가까워진다). 카르파시는 `chat_cli.py`에서 0.6, `chat_web.py`에서 0.8을 기본값으로 둔다. 너무 차분하지도 너무 들뜨지도 않은 *대화체*에 어울리는 값이다.

`rng`라는 인자 하나가 있는데, 이게 `torch.Generator` 객체다. 우리가 `engine.generate(..., seed=42)`를 호출하면, 안에서 `rng = torch.Generator(device=device); rng.manual_seed(seed)`로 만들어진 RNG가 `sample_next_token`마다 넘어간다. 모든 *난수성*이 이 한 객체에 모여 있다. 같은 seed면 같은 응답이 나온다 — *재현 가능한 sampling*이다.

`@torch.inference_mode()` 데코레이터도 잊지 말자. 학습 시의 `@torch.no_grad`보다 한 단계 더 가볍다. autograd 그래프를 *아예 만들지 않는다*. 추론 코드 전체에 inference_mode를 두르는 것이 nanochat의 기본 전략이다.

## 10.4 RowState — 행마다 다른 사연을 들고 다닌다

이제 Engine으로 넘어가기 직전, 작은 보조 클래스 하나를 짚고 가자. `engine.py:160-167`의 `RowState`다.

```python
class RowState:
    # Per-row state tracking during generation
    def __init__(self, current_tokens=None):
        self.current_tokens = current_tokens or [] # Current token sequence for this row
        self.forced_tokens = deque() # Queue of tokens to force inject
        self.in_python_block = False # Whether we are inside a python block
        self.python_expr_tokens = [] # Tokens of the current python expression
        self.completed = False # Whether this row has completed generation
```

이름이 모든 것을 말한다. *행마다의 상태*. num_samples가 N이면 RowState도 N개. 각 row가 자기만의 사연을 들고 다닌다.

`current_tokens`: 그 row가 지금까지 본 *전체 토큰 시퀀스*. prompt + 지금까지 뽑힌 토큰들.

`forced_tokens`: **이게 핵심이다.** deque(양방향 큐). 다음 step들에서 *모델 sampling 대신 강제로 주입할 토큰*들이 줄 서 있는 곳. tool use FSM이 결과 토큰을 여기에 미리 넣어두면, decode 루프가 *sample_next_token이 뽑은 것 대신* 이 deque에서 popleft한다.

`in_python_block`: 지금 우리가 `<|python_start|>` 안쪽에 있는가? 즉 모델이 *식을 쓰고 있는 중*인가?

`python_expr_tokens`: python block 안에서 모인 식 토큰들. `<|python_end|>`가 들어오면 이걸 디코드해서 도구 함수에 보낸다.

`completed`: 이 row가 *끝났는가*. `<|assistant_end|>` 또는 BOS를 만나면 True. 끝난 row는 더 이상 토큰을 뽑지 않는다.

다섯 개의 작은 슬롯에 *대화 진행, 도구 호출, 종료 판정*이 모두 들어 있다. 한 번 더 보자 — *이 다섯 개*다. *forced_tokens가 deque*인 것 한 가지만 기억해도 이 챕터의 절반은 갖고 있는 셈이다. 뒤에서 그 deque가 모델의 입을 빌려 *외부 계산기의 결과를 토해내게* 만드는 장면을 본다.

## 10.5 Engine.generate — 한 페이지 의사코드

자, 무대가 다 차려졌다. `engine.py:169-280`의 `Engine.generate`. 우리가 따라 읽을 *가장 긴 함수*이지만 100줄이 안 된다. 통째로 보자.

```python
class Engine:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer # needed for tool use

    @torch.inference_mode()
    def generate(self, tokens, num_samples=1, max_tokens=None, temperature=1.0, top_k=None, seed=42):
        """Same as generate, but does single prefill and then clones the KV cache."""
        assert isinstance(tokens, list) and isinstance(tokens[0], int), "expecting list of ints"
        device = self.model.get_device()
        dtype = torch.bfloat16 if device.type == "cuda" else torch.float32
        rng = torch.Generator(device=device)
        rng.manual_seed(seed)

        # Get the special tokens we need to coordinate the tool use state machine
        get_special = lambda s: self.tokenizer.encode_special(s)
        python_start = get_special("<|python_start|>")
        python_end = get_special("<|python_end|>")
        output_start = get_special("<|output_start|>")
        output_end = get_special("<|output_end|>")
        assistant_end = get_special("<|assistant_end|>") # if sampled, ends row
        bos = self.tokenizer.get_bos_token_id() # if sampled, ends row
```

서론부터 보자. 입력은 *Python int의 list*다. 그러니까 *토큰화는 호출자의 책임이다*. Engine은 토큰 id만 안다. tokenizer 객체는 들고 있지만, 그건 *special token id를 받아오기 위해서*다. 주석이 정확히 그렇게 말한다 — *"needed for tool use"*. 이 책임 분리가 깔끔하다.

device와 dtype은 *모델이 어디 있느냐*로 자동 결정된다. CUDA면 bf16, 아니면 fp32. 코드 안에 솔직한 주석이 달려 있는데 — *"setting the dtype here and in this way is an ugly hack"* — 일부러 옮기지 말고 그대로 두자. 카르파시도 *이건 좀 못생긴 부분*이라고 인정한 셈이다. 작은 작품의 정직함이다.

여섯 줄짜리 special token 디코드는 *tool use FSM*이 의지하는 *깃발*들이다. 모델이 이 깃발 토큰 중 하나를 뱉으면 FSM이 상태를 바꾼다.

```python
        # 1) Run a batch 1 prefill of the prompt tokens
        m = self.model.config
        kv_model_kwargs = {"num_heads": m.n_kv_head, "head_dim": m.n_embd // m.n_head, "num_layers": m.n_layer}
        kv_cache_prefill = KVCache(
            batch_size=1,
            seq_len=len(tokens),
            device=device,
            dtype=dtype,
            **kv_model_kwargs,
        )
        ids = torch.tensor([tokens], dtype=torch.long, device=device)
        logits = self.model.forward(ids, kv_cache=kv_cache_prefill)
        logits = logits[:, -1, :].expand(num_samples, -1)  # (num_samples, vocab_size)
```

**Step 1 — batch=1 prefill.** prompt 토큰을 한 번에 모델에 통과시킨다. KVCache는 `batch_size=1, seq_len=len(tokens)` — *딱 prompt 길이만큼*. 좋은 결정이다. prefill 자체는 한 번이고, prompt가 끝나는 위치까지만 K·V가 필요하다.

forward의 결과는 `(B, T, vocab_size)` 모양의 logits이다. 우리에게 필요한 건 *마지막 위치의 logits*뿐 — 그 자리에서 다음 토큰을 뽑아야 하니까. `logits[:, -1, :]`로 마지막 위치를 자른 다음, `.expand(num_samples, -1)`로 num_samples만큼 broadcast한다. 이 한 줄에 *같은 prompt에서 N개 응답*이라는 의도가 깔려 있다.

```python
        # 2) Replicate the KV cache for each sample/row
        kv_length_hint = (len(tokens) + max_tokens) if max_tokens is not None else self.model.config.sequence_len
        kv_cache_decode = KVCache(
            batch_size=num_samples,
            seq_len=kv_length_hint,
            device=device,
            dtype=dtype,
            **kv_model_kwargs,
        )
        kv_cache_decode.prefill(kv_cache_prefill)
        del kv_cache_prefill # no need to keep this memory around
```

**Step 2 — KV cache 복제.** 앞서 본 `prefill()` 메서드의 출연 장면이다. *큰 캐시*를 새로 만들고(`batch_size=num_samples`, `seq_len=`prompt+max_tokens), *작은 캐시*의 내용을 그 안에 복사한다. 그러고 나서 작은 캐시는 *지워버린다* — 더 들고 다닐 이유가 없다.

`kv_length_hint`라는 이름이 정직하다. *얼마나 길어질지의 힌트*다. max_tokens가 주어지면 prompt 길이 + max_tokens, 아니면 모델의 최대 시퀀스 길이. 미리 그만큼 공간을 잡아두는 거다.

```python
        # 3) Initialize states for each sample
        row_states = [RowState(tokens.copy()) for _ in range(num_samples)]
```

**Step 3 — RowState N개.** 각 행이 자기 사연을 든다. `tokens.copy()`로 prompt를 복사해서 각 row의 출발선을 같게 둔다.

```python
        # 4) Main generation loop
        num_generated = 0
        while True:
            # Stop condition: we've reached max tokens
            if max_tokens is not None and num_generated >= max_tokens:
                break
            # Stop condition: all rows are completed
            if all(state.completed for state in row_states):
                break

            # Sample the next token for each row
            next_ids = sample_next_token(logits, rng, temperature, top_k)  # (B, 1)
            sampled_tokens = next_ids[:, 0].tolist()
```

**Step 4 — decode 루프.** 두 가지 종료 조건: max_tokens 도달 또는 *모든 row가 완료*. 어느 한 row만 완료된 게 아니라 *전부* 완료여야 멈춘다. *완료된 row는 토큰을 계속 뽑긴 하지만 결과에 적히지 않는 식*으로 그냥 흐른다. 단순하게 가는 길이다.

루프 본체의 첫 일은 *N개 row에 대해 한꺼번에 sampling*. `logits`은 `(num_samples, vocab_size)` 모양이고, `sample_next_token`이 `(num_samples, 1)`을 돌려준다. 그걸 list로 풀어 `sampled_tokens` 한 개를 만든다.

```python
            # Process each row: choose the next token, update state, optional tool use
            token_column = [] # contains the next token id along each row
            token_masks = [] # contains the mask (was it sampled (1) or forced (0)?) along each row
            for i, state in enumerate(row_states):
                # Select the next token in this row
                is_forced = len(state.forced_tokens) > 0 # are there tokens waiting to be forced in deque?
                token_masks.append(0 if is_forced else 1) # mask is 0 if forced, 1 if sampled
                next_token = state.forced_tokens.popleft() if is_forced else sampled_tokens[i]
                token_column.append(next_token)
                # Update the state of this row to include the next token
                state.current_tokens.append(next_token)
                # On <|assistant_end|> or <|bos|>, mark the row as completed
                if next_token == assistant_end or next_token == bos:
                    state.completed = True
```

이 안쪽이 *Engine의 마음*이다. 각 row를 돌면서 *다음 토큰을 결정한다*. 결정의 갈래는 두 가지.

하나는 `forced_tokens`에 줄 서 있는 토큰이 있으면 그걸 popleft. *모델 sampling이 무엇을 뽑았는가는 무시한다*. mask=0(forced).

다른 하나는 deque가 비어 있으면 *방금 sample한 토큰*을 쓴다. mask=1(sampled).

mask는 *왜* 들고 다니는가? RL 단계에서 이 mask가 *loss에 들어갈 토큰*을 가른다. 9장에서 본 그 메커니즘 — *모델이 직접 sample한 토큰만 loss에 들어간다. forced로 주입된 도구 결과는 학습 신호에서 빠진다*. 그 논리가 여기 *mask 한 비트*로 압축돼 있다.

토큰이 결정되면 `current_tokens`에 추가하고, `<|assistant_end|>` 또는 BOS면 *그 행을 완료*로 마크한다. 단순하다.

여기까지가 *기본 generate 루프*다. 이 다음 몇 줄이 **이 챕터의 클라이맥스**다. 호흡을 가다듬고 다음 절로 넘어가자.

## 10.6 ★ Tool use FSM — 모델의 입을 빌려 외부 계산기를 부른다

```python
                # Handle tool logic
                if next_token == python_start:
                    state.in_python_block = True
                    state.python_expr_tokens = []
                elif next_token == python_end and state.in_python_block:
                    state.in_python_block = False
                    if state.python_expr_tokens:
                        expr = self.tokenizer.decode(state.python_expr_tokens)
                        result = use_calculator(expr)
                        if result is not None:
                            result_tokens = self.tokenizer.encode(str(result))
                            state.forced_tokens.append(output_start)
                            state.forced_tokens.extend(result_tokens)
                            state.forced_tokens.append(output_end)
                    state.python_expr_tokens = []
                elif state.in_python_block:
                    state.python_expr_tokens.append(next_token)
```

`engine.py:256-272`. 17줄짜리 *유한 상태 기계*. 한 줄씩 짚자.

상태는 두 개다: `in_python_block`이 False(=일반 응답 중)이거나 True(=식을 쓰는 중). 전환의 깃발은 두 개의 special token, `<|python_start|>`와 `<|python_end|>`.

**전이 1: `<|python_start|>`가 뽑혔다.** `in_python_block=True`로 켜고, `python_expr_tokens`를 비운다. 이제부터 모델이 뱉는 토큰은 *식의 일부*다.

**전이 2: 우리는 `in_python_block` 상태에 있고, 모델이 `<|python_end|>`가 아닌 *일반 토큰*을 뱉었다.** 그 토큰을 `python_expr_tokens`에 *모은다*. 모델이 "9 곱하기 8" 같은 식을 *한 토큰씩 적고 있는 중*이다.

**전이 3: `<|python_end|>`가 뽑혔다.** 여기가 *핵심 장면*이다. `in_python_block`을 False로 끄고, 모아둔 `python_expr_tokens`를 *디코드해 문자열 식*으로 만든다. 그 식을 `use_calculator(expr)`로 보낸다. 결과가 나오면 — `None`이 아니면 — *결과 문자열을 다시 토큰화*해서, **forced_tokens deque에 `<|output_start|>` + result_tokens + `<|output_end|>`를 줄 세운다**.

자, 다음 step의 루프가 돌면 어떻게 되는가? `forced_tokens`에 토큰이 있으니까 *모델의 sampling은 무시되고*, deque에서 토큰이 하나씩 뽑혀 *모델이 마치 그 토큰을 직접 sampling한 것처럼* 응답에 들어간다. 그 동안 KV cache에는 *forced 토큰의 K·V*가 적힌다. 모델은 자기가 뱉은 게 아닌데도 *자기가 뱉은 줄로 안다*. attention의 다음 step부터는 그 결과 토큰들을 *과거의 자기 문맥*으로 본다.

*인상적이지 않은가.* 모델의 입을 외부 계산기가 잠깐 빌려서 정확한 답을 토해내고, 다시 모델에게 입을 돌려준다. 모델은 "9 곱하기 8 = 72"라는 사실을 *학습 데이터에서 본 적이 없어도* 정확히 72를 *대화에 끼워 넣을 수 있다*. 그리고 그 다음 토큰부터 *72라는 사실에 근거해* 응답을 이어갈 수 있다. 도구 호출이라는 게 *결국 토큰 한 다발의 강제 주입*이라는 사실이, 이 17줄로 한 번에 손에 잡힌다.

한 가지 짚어두고 가자. `if state.in_python_block` 분기가 *세 가지의 마지막*에 있어서 — `python_end`가 아닌 *python block 안의 일반 토큰*만 `python_expr_tokens`에 모이게 된다는 점이다. 만약 `python_end`인데 `python_expr_tokens`가 비어 있으면 도구 함수가 호출되지 않는다 — *빈 식*은 평가하지 않는다. 또 도구 함수가 `None`을 돌려주면(=식이 화이트리스트를 통과하지 못했거나, 평가가 실패했거나) `forced_tokens`에 아무것도 안 들어간다. 모델은 *그냥 다음 토큰을 자기 힘으로 뽑아야 한다*. 안전한 fallback이다.

루프의 마지막 두 부분이 남았다.

```python
            # Yield the token column
            yield token_column, token_masks
            num_generated += 1

            # Prepare logits for next iteration
            ids = torch.tensor(token_column, dtype=torch.long, device=device).unsqueeze(1)
            logits = self.model.forward(ids, kv_cache=kv_cache_decode)[:, -1, :]  # (B, vocab_size)
```

**Step 5 — yield.** generator 함수이므로 토큰 컬럼(N개 row의 다음 토큰)과 mask 컬럼을 `yield`해서 호출자에게 한 step씩 흘려보낸다. 이 yield가 *streaming UI*의 출발점이다. chat_cli는 이걸 받아서 콘솔에 한 토큰씩 찍고, chat_web은 이걸 받아서 SSE로 브라우저에 흘린다.

**Step 6 — 다음 step 준비.** 다음 forward를 위해 *방금 뽑힌 토큰 한 줄*을 `(num_samples, 1)` 모양으로 만들어 모델에 통과시킨다. KV cache는 `kv_cache_decode`. forward 안에서 FA3의 `flash_attn_with_kvcache`가 *캐시를 in-place로 업데이트*하면서 새 토큰의 attention을 계산한다. 결과 logits을 또 `[:, -1, :]`로 잘라 다음 루프로 보낸다.

이게 끝이다. **약 100줄의 함수 하나에 prefill, 복제, decode, tool FSM, mask 추적, streaming yield가 모두 들어 있다**. 한 번 더 읽어보자. 차분히 읽으면 *무리한 곳이 없다*. 357줄의 engine.py가 *그렇게 길지 않다*는 사실이 새삼 든다.

한 가지 *더 큰 그림*을 짚고 가자. 우리가 흔히 *함수 호출(function calling)*이라고 부르는 LLM의 능력이 — 사실은 *토큰 한 다발의 강제 주입* 위에 서 있다는 점이다. OpenAI의 function calling API, Anthropic의 tool use, LangChain의 ReAct 에이전트 — 이 *모든 도구 호출 인터페이스*가 본질적으로는 같은 일을 한다. *모델이 어떤 special한 시퀀스를 뱉으면, 그걸 가로채 외부 함수를 호출하고, 결과를 모델의 다음 입력으로 다시 끼워 넣는다*. 그 가로채는 방식이 *호스트가 정한 약속*(JSON schema, XML tag, 또는 special token)일 뿐이다.

nanochat은 그 약속을 *가장 단순한 형태*로 풀었다. *토크나이저가 다루는 special token*. 학습 시점부터 모델이 `<|python_start|>` … `<|python_end|>`를 *대화의 일부*로 본다(8장의 SFT 데이터 포맷이 그렇게 짜여 있었다). 추론 시점에 Engine이 *그 토큰을 보고 행동*한다. 학습과 추론이 *같은 약속*을 쓰니까 *어긋날 일이 없다*. 큰 사례에서는 *JSON parsing 실패*나 *partial XML* 같은 *번거로운 일*이 생기기 쉽지만, special token은 그런 일에서 자유롭다. 일찍 깰 일이 없다는 게 nanochat의 단단함이다.

## 10.7 use_calculator — 화이트리스트 한 줄짜리 안전망

도구 호출의 *결정타*는 결국 `use_calculator(expr)` 안에서 식이 실제로 평가되는 순간이다. `engine.py:46-79`. 한 번 보자.

```python
def use_calculator(expr):
    """
    Evaluate a Python expression safely.
    Supports both math expressions and string operations like .count()
    """
    # Remove commas from numbers
    expr = expr.replace(",", "")

    # Check if it's a pure math expression (old behavior)
    if all([x in "0123456789*+-/.() " for x in expr]):
        if "**" in expr:  # disallow power operator
            return None
        return eval_with_timeout(expr)

    # Check if it's a string operation we support
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'\"()._ "
    if not all([x in allowed_chars for x in expr]):
        return None

    # Disallow dangerous patterns
    dangerous_patterns = ['__', 'import', 'exec', 'eval', 'compile', 'open', 'file',
                         'input', 'raw_input', 'globals', 'locals', 'vars', 'dir',
                         'getattr', 'setattr', 'delattr', 'hasattr']
    expr_lower = expr.lower()
    if any(pattern in expr_lower for pattern in dangerous_patterns):
        return None

    # Only allow .count() method for now (can expand later)
    if '.count(' not in expr:
        return None

    # Evaluate with timeout
    return eval_with_timeout(expr)
```

두 갈래로 흐른다.

**갈래 1: 순수 수식.** 식의 모든 문자가 `0123456789*+-/.()` 와 공백 사이에 있으면, 그건 *수식*이다. `**`(거듭제곱)만 별도로 막는다 — `2**1000`처럼 *작은 식이 거대한 수*가 되어 메모리를 잡아먹는 걸 막기 위해서다. 그게 아니면 `eval_with_timeout`으로 평가한다. *9 곱하기 8*, *(12+5)\*3*, *123\*456* 같은 게 여기서 처리된다.

**갈래 2: 문자열 연산.** 모든 문자가 *알파벳/숫자/따옴표/괄호/언더스코어/공백 사이*에 있고, 위험 패턴(`__`, `import`, `eval`, `globals`, `getattr` 등)이 *전혀 없으며*, `.count(`가 *반드시 들어 있어야* 평가한다. 즉 **현재 인정되는 문자열 연산은 `.count()` 단 한 개**다.

`.count()`만 허용하는 이유는 1장에서 잠깐 본 *strawberry r 개수 세기* 같은 SpellingBee 패턴 때문이다. 7장의 nanochat 평가에서 *모델이 `'strawberry'.count('r')`을 호출해 정확히 3을 알아낸다*는 능력 시연이 있었다. 그 능력의 *코드적 근거*가 이 7줄짜리 화이트리스트다. *나중에 더 많은 메서드를 허용할 수 있다*는 자리만 비워두고, 지금은 `.count()` 한 개로 끝낸다.

그리고 `eval_with_timeout(expr, max_time=3)`이 *3초 timeout*을 건다. signal.SIGALRM을 써서 *식이 3초 안에 평가되지 않으면 예외*. 안 끝나는 식(예: 거의 없겠지만 *무한 루프가 가능한 형태*)이 *영원히 모델을 막는 일*은 안 생기게 한다.

```python
@contextmanager
def timeout(duration, formula):
    def timeout_handler(signum, frame):
        raise Exception(f"'{formula}': timed out after {duration} seconds")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(duration)
    yield
    signal.alarm(0)
```

식을 평가하는 inner 함수가 Python 내장 평가기를 부르되, 두 번째 인자에 `{"__builtins__": {}}`를 넣어 *내장 함수 전체를 비운다*. 즉 `print`, `open`, `__import__` 같은 것이 *식 안에서 인식되지 않는다*. 화이트리스트(문자 검사)와 빈 builtins(평가 시점 검사)라는 *두 겹의 안전망*이 깔린다.

물론 *진짜 sandbox*는 아니다. 그건 같은 파일이 아닌 `nanochat/execution.py`에서 본격적으로 처리한다. 잠깐 그쪽을 짚고 가자.

### `execution.py` — HumanEval용 무거운 sandbox

`use_calculator`가 *3초 timeout 화이트리스트 인라인 평가*인 가벼운 사촌이라면, `nanochat/execution.py`(349줄)는 **HumanEval 평가용 무거운 sandbox**다. 같은 모델이 *짧은 산수*가 아니라 *함수 한 덩어리*를 작성하고 실행하게 만들 때 쓰인다.

```python
def execute_code(
    code: str,
    timeout: float = 5.0, # 5 seconds default
    maximum_memory_bytes: Optional[int] = 256 * 1024 * 1024, # 256MB default
) -> ExecutionResult:
    """
    Execute Python code in a sandboxed environment.
    """
    manager = multiprocessing.Manager()
    result_dict = manager.dict()
    p = multiprocessing.Process(
        target=_unsafe_execute,
        args=(code, timeout, maximum_memory_bytes, result_dict)
    )
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.kill()
        ...
```

핵심 약속이 세 가지다.

**첫째, 별도 프로세스.** `multiprocessing.Process`로 코드를 *부모와 분리된 프로세스*에서 돌린다. 잘못해서 *세그폴트*가 나거나 *프로세스가 죽어도* 부모는 안전하다. timeout이 지나면 `p.kill()`.

**둘째, 메모리 256MB 제한.** `reliability_guard(maximum_memory_bytes)` 안에서 `resource.setrlimit(resource.RLIMIT_AS, ...)`로 *주소 공간을 256MB로 묶는다*. 256MB 넘게 잡으려 하면 MemoryError. (macOS Darwin에서는 setrlimit이 잘 안 돌아서 skip한다는 정직한 주석이 달려 있다.)

**셋째, 위험 함수 비활성화.** `os.system`, `os.kill`, `shutil.rmtree`, `subprocess.Popen` 등 *시스템에 해를 끼칠 수 있는 것들*을 None으로 덮어쓴다. 코드 안의 `print`, `open`, `getattr` 같은 일상적인 builtin은 살아 있다 — *HumanEval은 출력을 검사해야 하니까*.

원본 코드의 한 줄짜리 경고가 솔직하다:

> *Network access is not blocked (e.g. sockets could be opened) ... Overall this sandbox is good for evaluation of generated code and protects against accidental destructive behavior, but it is not safe against malicious adversarial code.*

*평가용*으로 쓰기에는 충분하지만 *실제 production*에는 안 쓰는 게 좋다는 솔직한 경계 선언이다. 우리가 책에서 따라 읽는 nanochat은 *학습과 평가용 작품*이지 *서비스용 인프라*가 아니다.

자, 이렇게 도구 호출의 *두 사촌*을 다 봤다. 가벼운 calculator(`engine.py`)와 무거운 sandbox(`execution.py`). 둘 다 *모델이 직접 만질 수는 없는 외부 세계*를 *안전한 통로*로 잠깐 열어주는 메커니즘이다. *대화 안에서 모델이 외부 세계를 빌리는 일*이 곧 도구 호출이다.

이제 *그 도구를 쓸 줄 아는 모델*에게 *우리가 말을 거는 채널*을 보자.

## 10.8 chat_cli — 가장 단순한 REPL

`scripts/chat_cli.py`. 100줄짜리, *가장 작고 정직한* 챗 인터페이스다. 통째로 읽어보자.

```python
import argparse
import torch
from nanochat.common import compute_init, autodetect_device_type
from nanochat.engine import Engine
from nanochat.checkpoint_manager import load_model

parser = argparse.ArgumentParser(description='Chat with the model')
parser.add_argument('-i', '--source', type=str, default="sft", help="Source of the model: sft|rl")
parser.add_argument('-g', '--model-tag', type=str, default=None, help='Model tag to load')
parser.add_argument('-s', '--step', type=int, default=None, help='Step to load')
parser.add_argument('-p', '--prompt', type=str, default='', help='Prompt the model, get a single response back')
parser.add_argument('-t', '--temperature', type=float, default=0.6, help='Temperature for generation')
parser.add_argument('-k', '--top-k', type=int, default=50, help='Top-k sampling parameter')
parser.add_argument('--device-type', type=str, default='', choices=['cuda', 'cpu', 'mps'], help='Device type for evaluation')
args = parser.parse_args()
```

argparse 한 묶음. 기본 source는 `sft`이지만 `--source rl`을 주면 9장에서 학습한 RL 모델을 쓴다. `--temperature 0.6`이 chat_cli의 기본값. *조금 차분한 톤*이다.

```python
device_type = autodetect_device_type() if args.device_type == "" else args.device_type
ddp, ddp_rank, ddp_local_rank, ddp_world_size, device = compute_init(device_type)
model, tokenizer, meta = load_model(args.source, device, phase="eval", model_tag=args.model_tag, step=args.step)

# Special tokens for the chat state machine
bos = tokenizer.get_bos_token_id()
user_start, user_end = tokenizer.encode_special("<|user_start|>"), tokenizer.encode_special("<|user_end|>")
assistant_start, assistant_end = tokenizer.encode_special("<|assistant_start|>"), tokenizer.encode_special("<|assistant_end|>")

# Create Engine for efficient generation
engine = Engine(model, tokenizer)
```

체크포인트를 *eval* 모드로 로드하고(8장에서 본 dropout off, eval-time RoPE 등), special token id 네 개를 받아오고, Engine을 만든다. 여기까지 *모델을 손에 잡는 데* 12줄.

```python
conversation_tokens = [bos]

while True:

    if args.prompt:
        user_input = args.prompt
    else:
        try:
            user_input = input("\nUser: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

    if user_input.lower() in ['quit', 'exit']:
        print("Goodbye!")
        break

    if user_input.lower() == 'clear':
        conversation_tokens = [bos]
        print("Conversation cleared.")
        continue

    if not user_input:
        continue

    # Add User message to the conversation
    conversation_tokens.append(user_start)
    conversation_tokens.extend(tokenizer.encode(user_input))
    conversation_tokens.append(user_end)

    # Kick off the assistant
    conversation_tokens.append(assistant_start)
```

대화 토큰은 `[BOS]`로 시작한다. 사용자가 한 줄을 치면 — 토큰화하고 — `[user_start] ... [user_end]`로 감싸서 *시퀀스 끝에 잇는다*. 그리고 *결정적 한 줄*:

```python
    conversation_tokens.append(assistant_start)
```

`<|assistant_start|>`를 *모델 대신 미리 적어*준다. 모델은 이걸 prompt의 끝으로 받고, *자기가 어시스턴트라는 사실*을 한 번 더 확인하고, 다음 토큰부터 답을 시작한다. 이걸 흔히 *priming*이라고 부른다 — *시작 토큰을 직접 박아 모델의 다음 발화를 강제로 어시스턴트 자리에 둔다*.

```python
    generate_kwargs = {
        "num_samples": 1,
        "max_tokens": 256,
        "temperature": args.temperature,
        "top_k": args.top_k,
    }
    response_tokens = []
    print("\nAssistant: ", end="", flush=True)
    for token_column, token_masks in engine.generate(conversation_tokens, **generate_kwargs):
        token = token_column[0] # pop the batch dimension (num_samples=1)
        response_tokens.append(token)
        token_text = tokenizer.decode([token])
        print(token_text, end="", flush=True)
    print()
```

자, *대화의 일*이 여기서 일어난다. `engine.generate(conversation_tokens, ...)`이 generator를 돌려주고, 매 step의 `(token_column, token_masks)`를 받아 *첫 row의 첫 토큰*을 꺼낸다. `tokenizer.decode([token])`로 *그 한 토큰의 문자열*을 만들고, `print(..., end="", flush=True)`로 *즉시* 콘솔에 흘린다. 우리가 보는 *그* streaming이다. 한 토큰씩 천천히 흘러나오는 글자들.

```python
    if response_tokens[-1] != assistant_end:
        response_tokens.append(assistant_end)
    conversation_tokens.extend(response_tokens)

    if args.prompt:
        break
```

마지막으로 `<|assistant_end|>`로 *반드시* 응답을 닫는다. max_tokens에 걸려 잘렸어도 어시스턴트 차례는 *명시적으로* 끝내야 한다. 그러고 응답 토큰들을 `conversation_tokens`에 *이어붙여* 다음 user turn의 *문맥*으로 삼는다. *대화는 토큰의 단순 누적*이라는 사실이 이 두 줄에 압축돼 있다.

100줄짜리 REPL. *대화 인터페이스가 사실 별것 아니다*라는 말이 이 작은 파일에 다 있다. 한 줄씩 토큰을 받아 한 줄씩 토큰을 흘려보내는 일 — 그게 ChatGPT 모양의 대화다.

## 10.9 chat_web — FastAPI, SSE, 그리고 멀티바이트의 함정

CLI가 *가장 단순한 채널*이라면, 웹 UI는 *진짜 ChatGPT처럼 보이는 채널*이다. `scripts/chat_web.py` 407줄. 우리가 들여다볼 부분을 잘라서 보자.

### WorkerPool — GPU N개를 round-robin

`chat_web.py:86-141`. 데이터 병렬 패턴이다.

```python
@dataclass
class Worker:
    """A worker with a model loaded on a specific GPU."""
    gpu_id: int
    device: torch.device
    engine: Engine
    tokenizer: object

class WorkerPool:
    """Pool of workers, each with a model replica on a different GPU."""

    def __init__(self, num_gpus: Optional[int] = None):
        if num_gpus is None:
            if device_type == "cuda":
                num_gpus = torch.cuda.device_count()
            else:
                num_gpus = 1 # e.g. cpu|mps
        self.num_gpus = num_gpus
        self.workers: List[Worker] = []
        self.available_workers: asyncio.Queue = asyncio.Queue()

    async def initialize(self, source: str, model_tag: Optional[str] = None, step: Optional[int] = None):
        """Load model on each GPU."""
        print(f"Initializing worker pool with {self.num_gpus} GPUs...")
        if self.num_gpus > 1:
            assert device_type == "cuda", "Only CUDA supports multiple workers/GPUs. cpu|mps does not."

        for gpu_id in range(self.num_gpus):
            if device_type == "cuda":
                device = torch.device(f"cuda:{gpu_id}")
                print(f"Loading model on GPU {gpu_id}...")
            else:
                device = torch.device(device_type) # e.g. cpu|mps
                print(f"Loading model on {device_type}...")

            model, tokenizer, _ = load_model(source, device, phase="eval", model_tag=model_tag, step=step)
            engine = Engine(model, tokenizer)
            worker = Worker(gpu_id=gpu_id, device=device, engine=engine, tokenizer=tokenizer)
            self.workers.append(worker)
            await self.available_workers.put(worker)

        print(f"All {self.num_gpus} workers initialized!")

    async def acquire_worker(self) -> Worker:
        """Get an available worker from the pool."""
        return await self.available_workers.get()

    async def release_worker(self, worker: Worker):
        """Return a worker to the pool."""
        await self.available_workers.put(worker)
```

`Worker`는 *GPU 한 개 + 모델 복제본 한 개 + Engine + tokenizer*의 dataclass. `WorkerPool`은 N개의 Worker를 들고 있고, `asyncio.Queue`로 *유휴 worker*를 관리한다.

요청이 들어오면 `acquire_worker()` → 큐에서 worker 하나를 꺼낸다(=*점유*). 응답 streaming이 끝나면 `release_worker(worker)` → 큐에 *되돌려 놓는다*. 모든 worker가 바쁘면 다음 요청은 *큐에서 대기*한다.

이게 *데이터 병렬 round-robin*의 가장 단순한 형태다. tensor parallel이나 pipeline parallel처럼 *모델을 쪼개*는 게 아니라, *같은 모델을 N개 복제*해 N개의 사용자를 동시에 처리한다. 작은 작품(d24=560M)이라 GPU 한 개에 들어가니까 *이 단순한 패턴이 깔끔하게 먹힌다*. GPU 메모리가 작은 모델이 가진 *덤*인 셈이다.

8개 GPU면 *동시 8명*까지는 거의 *대기 없이* 흘러간다. 9번째부터는 큐에 줄을 선다. *세계에서 가장 거대한 LLM serving 시스템*도 본질적으로는 이 패턴을 정교화한 것이다 — 다만 prefill·decode 분리, paged attention, continuous batching 같은 *복잡한 최적화*가 추가될 뿐.

### ChatRequest — abuse 방지 검증

`chat_web.py:143-215`. Pydantic으로 입력 스키마를 받고, `validate_chat_request`로 *방어선*을 친다.

```python
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_k: Optional[int] = None
```

스키마는 OpenAI Chat Completions API와 *비슷하게* 생겼다. `messages`의 각 원소는 `role`과 `content`. 그리고 *생성 옵션 세 개*가 선택적으로 붙는다.

`validate_chat_request`가 막는 것들이 *방어선*이다.

```python
# Abuse prevention limits
MAX_MESSAGES_PER_REQUEST = 500
MAX_MESSAGE_LENGTH = 8000
MAX_TOTAL_CONVERSATION_LENGTH = 32000
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0
MIN_TOP_K = 0
MAX_TOP_K = 200
MIN_MAX_TOKENS = 1
MAX_MAX_TOKENS = 4096
```

상수 한 묶음의 의미가 단순하다. 메시지 500개 초과 금지, 메시지당 8000자 초과 금지, 전체 32000자 초과 금지, temperature 0-2 사이, top_k 0-200 사이, max_tokens 1-4096 사이. *공개 데모로 띄웠을 때 누군가 너무 큰 prompt를 던지지 못하게* 막는 단순하고 정직한 가드다. *진짜 production grade*는 아니지만 *공부용 작품을 잠깐 외부에 열어둘 때*는 이 정도면 충분하다.

`role`은 "user" 또는 "assistant"만 허용. 시스템 프롬프트는 *없다*. nanochat이 *system role 없이 학습됐기 때문*이다. 8장의 SFT 데이터 포맷이 user/assistant 두 역할만 갖고 있었다. 모델이 본 적 없는 형식을 *런타임에 끼워 넣을 수는 없다*.

### generate_stream — SSE 한 step씩 흘려보내기

`chat_web.py:255-303`. 이 함수가 *웹 채팅의 심장*이다.

```python
async def generate_stream(
    worker: Worker,
    tokens,
    temperature=None,
    max_new_tokens=None,
    top_k=None
) -> AsyncGenerator[str, None]:
    """Generate assistant response with streaming."""
    temperature = temperature if temperature is not None else args.temperature
    max_new_tokens = max_new_tokens if max_new_tokens is not None else args.max_tokens
    top_k = top_k if top_k is not None else args.top_k

    assistant_end = worker.tokenizer.encode_special("<|assistant_end|>")
    bos = worker.tokenizer.get_bos_token_id()

    # Accumulate tokens to properly handle multi-byte UTF-8 characters (like emojis)
    accumulated_tokens = []
    # Track the last complete UTF-8 string (without replacement characters)
    last_clean_text = ""

    for token_column, token_masks in worker.engine.generate(
        tokens,
        num_samples=1,
        max_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        seed=random.randint(0, 2**31 - 1)
    ):
        token = token_column[0]

        # Stopping criteria
        if token == assistant_end or token == bos:
            break

        # Append the token to sequence
        accumulated_tokens.append(token)
        # Decode all accumulated tokens to get proper UTF-8 handling
        current_text = worker.tokenizer.decode(accumulated_tokens)
        # Only emit text if it doesn't end with a replacement character
        if not current_text.endswith('�'):
            new_text = current_text[len(last_clean_text):]
            if new_text:
                yield f"data: {json.dumps({'token': new_text, 'gpu': worker.gpu_id}, ensure_ascii=False)}\n\n"
                last_clean_text = current_text

    yield f"data: {json.dumps({'done': True})}\n\n"
```

전체 흐름은 chat_cli와 비슷하다. `engine.generate`를 돌리면서 매 step의 토큰을 받아 처리한다. 다만 *두 가지가 다르다*.

**다른 첫 번째 — seed.** chat_cli는 고정 seed지만 chat_web은 `seed=random.randint(0, 2**31 - 1)`. 요청마다 *다른 seed*. 같은 prompt를 두 번 보내면 *다른 응답*이 나온다. 데모로 띄웠을 때 이게 더 *살아 있는 느낌*을 준다.

**다른 두 번째 — UTF-8 멀티바이트 안전망.** 이 부분이 *섬세하게* 만들어졌다. 한 줄씩 보자.

토크나이저는 *바이트 단위 BPE*다(2장). 따라서 *한 토큰이 한 글자에 매핑되지 않는다*. 특히 *멀티바이트 문자*(한글 한 글자=3바이트, 이모지=4바이트) 같은 경우, *한 글자가 두 개 이상의 토큰*으로 쪼개진다.

만약 우리가 매 step *방금 받은 토큰 한 개만 디코드*해서 흘려보내면 어떻게 되는가? 한글 한 글자의 *첫 토큰*만 받았을 때 디코드는 *완성되지 않은 바이트 시퀀스*를 보고 **replacement character `�`**를 돌려준다. 그게 브라우저에 흘러나가면 *깨진 문자*가 보인다. 다음 step에서 *나머지 바이트들*이 와도 이미 깨진 글자가 화면에 박혀 있다.

*끔찍하다*.

그래서 nanochat이 쓰는 트릭이 이렇다.

1. *지금까지의 모든 토큰을 누적*(`accumulated_tokens`)해 전체를 매번 디코드한다.
2. 디코드 결과의 *마지막이 `�`이면* — 즉 *불완전한 시퀀스*면 — *yield하지 않고 다음 step을 기다린다*.
3. 마지막이 깨끗하면 — *그동안 미뤄둔 글자까지 한꺼번에* — `last_clean_text` 이후의 *새 부분*만 잘라 yield한다.

매 step decode를 다시 한다는 게 비싸 보일 수 있는데, 주석이 정확히 말한다 — *"decode is a quite efficient operation, basically table lookup and string concat"*. 토크나이저 decode는 *id → byte → str* 변환의 단순 lookup이라 cost가 낮다. 안심하고 매 step 다시 부를 수 있다.

이 한 박스 덕분에 *한글이나 이모지도 깨지지 않고* 흘러나간다. 이런 디테일이 *작은 작품을 의외로 매끈하게* 만든다.

`yield f"data: {json.dumps(...)}\n\n"`이 *Server-Sent Events*의 표준 형식이다. `data: {...}\n\n`로 한 메시지가 끝난다. 브라우저의 `EventSource`가 *연결을 끊지 않고* 이 메시지들을 *하나씩* 받는다. WebSocket 없이도 *server → client 단방향 스트림*이 깔린다. chat 응답에 *완벽히 맞는* 패턴이다.

`json.dumps(..., ensure_ascii=False)`도 잘 보자. ASCII 강제 인코딩을 *끄지 않으면* 한글이 `\u...` 형태로 escape되어 *길어지고 보기 싫어진다*. 끄면 *그대로 UTF-8*. 이런 작은 약속들이 한 자리에 잘 모여 있다.

### chat_completions — endpoint의 흐름

`chat_web.py:305-374`. 마지막 한 함수가 *모든 것을 묶는다*.

```python
@app.post("/chat/completions")
async def chat_completions(request: ChatRequest):
    """Chat completion endpoint (streaming only) - uses worker pool for multi-GPU."""

    # Basic validation to prevent abuse
    validate_chat_request(request)

    # Log incoming conversation to console
    logger.info("="*20)
    for i, message in enumerate(request.messages):
        logger.info(f"[{message.role.upper()}]: {message.content}")
    logger.info("-"*20)

    # Acquire a worker from the pool (will wait if all are busy)
    worker_pool = app.state.worker_pool
    worker = await worker_pool.acquire_worker()

    try:
        # Build conversation tokens
        bos = worker.tokenizer.get_bos_token_id()
        user_start = worker.tokenizer.encode_special("<|user_start|>")
        user_end = worker.tokenizer.encode_special("<|user_end|>")
        assistant_start = worker.tokenizer.encode_special("<|assistant_start|>")
        assistant_end = worker.tokenizer.encode_special("<|assistant_end|>")

        conversation_tokens = [bos]
        for message in request.messages:
            if message.role == "user":
                conversation_tokens.append(user_start)
                conversation_tokens.extend(worker.tokenizer.encode(message.content))
                conversation_tokens.append(user_end)
            elif message.role == "assistant":
                conversation_tokens.append(assistant_start)
                conversation_tokens.extend(worker.tokenizer.encode(message.content))
                conversation_tokens.append(assistant_end)

        conversation_tokens.append(assistant_start)
        ...
```

들어온 요청을 — 검증하고, 로그 찍고, worker를 점유하고, 메시지 리스트를 *토큰 한 줄*로 풀어낸다. chat_cli의 한 turn 과정과 *완전히 같은 패턴*이다. 다만 여러 turn이 한 번에 들어올 수 있고, 마지막에 `assistant_start`를 박아 priming한다.

```python
        # Streaming response with worker release after completion
        response_tokens = []
        async def stream_and_release():
            try:
                async for chunk in generate_stream(worker, conversation_tokens, ...):
                    chunk_data = json.loads(chunk.replace("data: ", "").strip())
                    if "token" in chunk_data:
                        response_tokens.append(chunk_data["token"])
                    yield chunk
            finally:
                full_response = "".join(response_tokens)
                logger.info(f"[ASSISTANT] (GPU {worker.gpu_id}): {full_response}")
                logger.info("="*20)
                await worker_pool.release_worker(worker)

        return StreamingResponse(stream_and_release(), media_type="text/event-stream")
```

`StreamingResponse` + `media_type="text/event-stream"` + async generator. 이게 *FastAPI에서 SSE를 띄우는 정석*이다. `stream_and_release` 안의 `finally`가 *중요하다* — streaming이 끝나든 *클라이언트가 중간에 끊든* worker를 *반드시* pool에 돌려놓는다. 이게 빠지면 *worker가 누수*되어 시간이 지나면 *모든 worker가 사라진다*. 끔찍한 일이다.

여기까지가 chat_web의 *심장 부분*이다. 나머지는 `/health`, `/stats`, `/logo.svg`, `/` (UI html 서빙) 같은 잡일이다. 한 번 직접 코드를 펴서 끝까지 훑어보자 — *기억에 남는 큰 결정이 없다*.

## 10.10 ★ 칸 한 번 — 우리가 만든 모델과 처음 대화한다

자, 모든 인프라가 다 차려졌다. KV cache가 있다. Engine.generate가 있다. tool use FSM이 있다. chat_cli가 있다. chat_web이 있다. 그렇다면 *우리가 학습한 모델*과 한 번 대화해보자.

다만 *바로 그 한 번*을 위해 *현실적인 선택*을 한 가지 해두는 편이 낫다.

> **현실적인 calculator 데모 경로**
>
> Tool use FSM이 진짜로 *동작*하는 모습을 보려면 모델이 *스스로 `<|python_start|>`를 sample할 줄 알아야* 한다. 그 능력은 SFT에서 GSM8K 데이터를 충분히 학습해야 *안정적으로* 생긴다. 우리가 6장 직후의 base 모델이나, d6에 1500-step 정도로 짧게 SFT한 모델로 chat_cli를 띄우면 — *대화 자체가 흔들리는* 모습을 보게 된다. calculator는 *가끔* 호출되지만 *신뢰할 수 있는 수준은 아니다*.
>
> *이 챕터의 클라이맥스를 진짜로 맛보려면*, 카르파시가 GitHub Discussion에 공개해둔 *speedrun d24 체크포인트*를 받아서 띄우는 편이 낫다. d24는 약 5억 6천만 파라미터, 8XH100에서 *3시간 풀 파이프라인*을 다 돈 결과물이다.
>
> **권장 경로:**
> 1. 카르파시의 [GitHub Discussions #481](https://github.com/karpathy/nanochat/discussions/481)에서 speedrun d24 SFT 체크포인트 링크를 따라 받는다(또는 nanochat README의 최신 모델 공유 섹션을 참고). HuggingFace Hub로 올라간 버전이 있으면 그쪽이 깔끔하다.
> 2. 받은 체크포인트를 nanochat의 모델 디렉터리(보통 `~/.cache/nanochat/checkpoints/...`)에 *카르파시의 디렉터리 구조 그대로* 놓는다.
> 3. `python -m scripts.chat_web --source=sft`로 띄운다. 8000번 포트에서 UI가 뜬다.
> 4. 브라우저로 `http://localhost:8000`을 열고 "9 곱하기 8은?"이라고 묻는다.
>
> d6 1500-step 모델로도 calculator가 *가끔* 발화한다. 하지만 *책의 정점*을 *진짜로* 보고 싶다면 — speedrun ckpt를 받자. 한 번이면 된다.

좋다. 받았다고 가정하고 띄워보자. 우리가 직접 한 일이라고 상상해보자.

콘솔에 `python -m scripts.chat_web --source=sft`. 8개 GPU가 있으면 `--num-gpus 8`. 모델이 로드된다. *"All 8 workers initialized!"*가 찍히고, *"Server ready at http://localhost:8000"*. 브라우저를 연다. 익숙한 ChatGPT-비슷한 UI가 떠 있다. 입력창에 다음 한 줄을 친다.

> *"What is 9 times 8?"*

엔터.

화면에 토큰이 *한 글자씩* 흘러나오기 시작한다. *To find 9 multiplied by 8, I can use the calculator.* … 그러고 잠깐의 멈춤. 콘솔의 로그 창을 보면 `<|python_start|>9*8<|python_end|>` 토큰이 *그대로* 흘러간다. 모델이 *식을 토해낸 직후*에 — `<|python_end|>`가 yield된 다음 step에서 — Engine의 forced_tokens deque가 채워지고, 그 다음부터의 토큰들은 *Engine이 강제로 흘려넣은* output 토큰들이다(`<|output_start|>72<|output_end|>`). 우리 눈에는 *모델이 자기 입으로 72를 말한 것처럼* 보인다.

그러고 모델은 그 *72*를 자기 문맥으로 다시 받아, *이어서 응답을 마무리한다*. "*The answer is 72.*"

이게 책의 *그 순간*이다.

잠깐 멈춰서 *우리가 무엇을 보고 있는지*를 다시 짚어두자. 우리가 본 토큰 stream — *"To find 9 multiplied by 8, I can use the calculator." → `<|python_start|>9*8<|python_end|>` → `<|output_start|>72<|output_end|>` → "The answer is 72."* — 이 한 줄에 *책 전체*가 들어 있다. 2장의 토크나이저가 *special token id*를 발급했다. 3장의 BPE가 *글자를 토큰으로* 만들었다. 4A·4B의 GPT가 *입력 토큰을 받아 logits을 뱉었다*. 5장의 옵티마이저가 *그 logits이 더 잘 나오도록 가중치를 움직였다*. 6장의 사전학습이 *큰 분포*를 잡았고, 7장의 평가가 *얼마나 잘 잡혔는지를 측정*했다. 8장의 SFT가 *대화의 형식*과 *도구 호출의 약속*을 가르쳤다. 9장의 RL이 *수학을 더 단단하게* 만들었다. 그리고 10장의 Engine이 *모든 것을 묶어 토큰을 한 줄로 흘려보냈다*.

*72라는 한 수*에 그 모든 일이 응축되어 있다. 우리가 그것을 본 것은 *작은 단어 한 번의 응답*이지만, 그 응답 한 줄의 *경로*는 8천 줄의 코드와 12B 토큰의 데이터와 3시간의 GPU 시간이다. *직접 만든 무엇*이 *외부에서 받은 무엇*과 다른 이유가 여기 있다 — *우리는 그 경로의 모든 마디를 알아본다*.

> **한국어로 물어보면 어떻게 되나?**
>
> *"안녕"*이라고 한국어로 물어보면 두 가지 중 하나다. 모델이 영어로 답하거나 — 종종 *깨진다*. 그건 nanochat의 *학습 데이터 분포*다. 사전학습 코퍼스(fineweb-edu/ClimbMix)와 SFT 코퍼스(SmolTalk)가 *영어 중심*이다. 한국어 토큰의 임베딩은 *거의 학습되지 않았다*. 그러니 한국어로 nanochat과 *깊이 있는 대화*를 하기는 어렵다. 그렇다고 *영원히 어렵냐* 하면 그렇지 않다. **12장 마지막 절**에서 *어떻게 한국어 nanochat의 첫 한 걸음을 떼는지*를 한 절짜리 가이드로 다룬다. 영문판 가중치를 *완전히 버리지 않고* 한국어 코퍼스로 *이어 학습*하는 길이 있다.
>
> 일단 이번 챕터에서는 *영어로* 대화해보자. 영어 산수 한 줄과 GSM8K 식 단어 문제 한 줄.

다음 입력.

> *"Sarah has 12 apples. She gives 3 to Tom and 4 to Lisa. How many does she have left?"*

엔터.

흐름이 또 한 번 동작한다. 모델이 *문제를 한 번 풀이하고*, calculator를 *한 번* 호출하고, *답을 낸다*. 한 응답의 토큰 stream을 풀어 보면 — *Sarah has 12 apples. After giving 3 to Tom and 4 to Lisa, she has 12 - 3 - 4 apples.* `<|python_start|>12-3-4<|python_end|>` `<|output_start|>5<|output_end|>` *So Sarah has 5 apples left.*

*5라고 답한다.*

> **[실습 — CPU/MPS 또는 GPU 10분]**
>
> 1. speedrun d24 SFT 체크포인트를 받는다 ([#481](https://github.com/karpathy/nanochat/discussions/481) 또는 README의 모델 공유 섹션 참고).
> 2. `python -m scripts.chat_web --source=sft` (또는 `--source=rl`로 9장의 RL 체크포인트도 시도).
> 3. 브라우저로 `http://localhost:8000`을 연다.
> 4. 세 가지 입력을 차례로 던져본다.
>    - `안녕` — *어떻게* 깨지는지 본다.
>    - `What is 9 * 8?` — calculator가 발화하는 흐름이 브라우저 stream에 들어오는지 확인.
>    - `Sarah has 12 apples. She gives 3 to Tom and 4 to Lisa. How many does she have left?` — 단어 문제에 대해 모델이 *문장 분해 → calculator 호출 → 답*의 순서를 거치는지 본다.
> 5. 서버 콘솔의 로그를 *동시에* 본다. user/assistant 발화와 GPU 점유 정보가 한 줄씩 찍힌다.
> 6. 같은 질문을 두 번 던져 *다른 응답*이 나오는지 확인한다 (chat_web은 매번 random seed라서 *그렇게 된다*).

10분이면 *우리가 직접 만들었거나 다운받은 모델*과 *대화*를 마친다. 이전 9장까지 우리가 따라 읽은 8천 줄의 *결과물*이 *말을 한다*. 그게 무엇이든 — *우리 손에 잡힌* 무엇이다.

## 10.11 두 generate의 동거 — gpt.py의 28줄과 engine.py의 한 페이지

이 챕터를 닫기 전에 한 가지 사소한 *코드의 동거*를 짚어두자. 4A에서 우리가 `gpt.py`를 따라 읽을 때, 일부러 28줄을 빼두고 *10장에서 본다*고 약속했었다. `gpt.py:484-512`. 그것이 바로 *느린 reference generate*다.

```python
@torch.inference_mode()
def generate(self, tokens, max_tokens, temperature=1.0, top_k=None, seed=42):
    """
    Naive autoregressive streaming inference.
    To make it super simple, let's assume:
    - batch size is 1
    - ids and the yielded tokens are simple Python lists and ints
    """
    assert isinstance(tokens, list)
    device = self.get_device()
    rng = None
    if temperature > 0:
        rng = torch.Generator(device=device)
        rng.manual_seed(seed)
    ids = torch.tensor([tokens], dtype=torch.long, device=device) # add batch dim
    for _ in range(max_tokens):
        logits = self.forward(ids) # (B, T, vocab_size)
        logits = logits[:, -1, :] # (B, vocab_size)
        if top_k is not None and top_k > 0:
            v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
            logits[logits < v[:, [-1]]] = -float('Inf')
        if temperature > 0:
            logits = logits / temperature
            probs = F.softmax(logits, dim=-1)
            next_ids = torch.multinomial(probs, num_samples=1, generator=rng)
        else:
            next_ids = torch.argmax(logits, dim=-1, keepdim=True)
        ids = torch.cat((ids, next_ids), dim=1)
        token = next_ids.item()
        yield token
```

이건 *KV cache 없는, 매 step prompt 전체를 다시 forward하는, 멍청한* generate다. 28줄밖에 안 된다. *읽기 쉽다*. 그게 이 함수의 *목적*이다 — *Engine의 빠른 generate가 무엇을 빠르게 만들었는지를 한눈에 비교할 수 있는 reference*. `if __name__ == "__main__":` 아래에 *두 generate 결과가 같은지*를 확인하는 *self-test*도 들어 있다(`engine.py:307-357`).

```python
# common hyperparameters
kwargs = dict(max_tokens=64, temperature=0.0)
prompt_tokens = tokenizer.encode("The chemical formula of water is", prepend=bos_token_id)
# generate the reference sequence using the model.generate() function
generated_tokens = []
torch.cuda.synchronize()
t0 = time.time()
stream = model.generate(prompt_tokens, **kwargs)
for token in stream:
    generated_tokens.append(token)
    chunk = tokenizer.decode([token])
    print(chunk, end="", flush=True)
print()
torch.cuda.synchronize()
t1 = time.time()
print(f"Reference time: {t1 - t0:.2f}s")
```

이걸 직접 돌려보면 — temperature=0(=argmax)으로 *결정적*이게 만들어두고 — 두 generate가 *비트 단위로 같은 토큰 시퀀스*를 낸다. Engine은 KV cache를 쓰고 model은 cache 없이 매번 다시 돌리는데, *결과가 같다*. 거기서 안심한 다음 *몇 배 빠른지*를 wall-clock으로 잰다.

*이런 self-test가 코드 옆에 깔려 있다*는 점이 nanochat의 미덕이다. *내가 짠 빠른 코드와 내가 짠 느린 코드의 결과가 같은가*를 한 줄로 검증할 수 있다. 우리가 직접 추론 엔진을 짠다고 했을 때, 이런 *reference + fast* 쌍을 한 자리에 두는 패턴을 *기억해두자*. 큰 작품일수록 fast가 reference와 *조금씩 어긋난다*는 사실이 *어느 날 뼈아프게* 발견되곤 한다.

## 10.12 추론 옵션 — 무엇을 어떻게 돌릴까

추론을 띄울 때 우리가 만질 수 있는 *손잡이*가 몇 개 있다. 정리해두자.

**`--source` (`sft` | `rl`)**: 어느 학습 단계의 체크포인트를 쓸지. SFT는 *대화*를 가르친 모델, RL은 *수학 문제 풀이*가 더 단단해진 모델. *말투의 자연스러움*은 SFT가 약간 더 부드럽고, *GSM8K 식의 단계적 풀이*는 RL이 더 단단하다. 그 trade-off가 *작은 작품에서는 미묘*하다. 둘 다 띄워서 같은 질문을 비교해보자.

**`--temperature`** (default 0.6 in chat_cli, 0.8 in chat_web): 분포의 *날카로움/평평함*. 낮을수록 *결정적*, 높을수록 *무작위에 가까움*. 산수 문제는 *낮게*, 자유로운 대화는 *조금 높게*가 일반적인 직관이다. 0이면 argmax.

**`--top-k`** (default 50): 상위 k개 토큰만 후보로. 0이면 *전체 vocab*. 너무 크면 *이상한 토큰*이 가끔 나오고, 너무 작으면 *답이 단조*해진다.

**`--max-tokens`** (chat_web default 512): 한 응답의 *최대 길이*. 모델이 `<|assistant_end|>`를 *제때 뱉지 않으면* 이걸로 잘린다. SFT가 잘 끝내는 법을 *충분히 학습한 작품*이면 잘리는 일이 드물다.

**`--num-gpus`** (chat_web): GPU 몇 개에 모델을 복제할지. 동시 사용자 수와 직결된다.

**seed**: chat_cli는 *고정 seed*(=`42`), chat_web은 *요청마다 random*. seed가 고정이면 *같은 prompt에 같은 응답*이 보장된다(temperature가 0이 아니어도). 평가·디버깅에 유용하다.

이 손잡이들을 *조합하면* nanochat 하나로 *여러 표정의 챗봇*을 만들 수 있다. temperature=0.2 + top_k=10이면 *진지하고 또박또박한 산수 모델*, temperature=1.0 + top_k=200이면 *조금 더 발랄한 대화 모델*. *같은 가중치인데* 표정이 달라진다는 건 — 사실 LLM serving의 묘미 중 하나다.

손잡이가 *왜* 이렇게 적은지도 잠깐 생각해보자. 큰 LLM 시스템들은 *수십 개의 sampling parameter*를 갖고 있다. nucleus sampling의 top_p, repetition penalty, presence penalty, frequency penalty, logit bias, stop sequences, system prompt, function definitions … *손잡이가 많을수록 표정도 다양*하지만 *어떤 손잡이가 무엇을 하는지*가 점점 안 보인다. nanochat은 *5~6개의 본질적 손잡이*만 둔다. temperature, top_k, max_tokens, seed, source, num_gpus. *그게 전부*다. *적은 만큼 손에 잡힌다*. 우리가 책에서 따라가기에 *이만한 작품이 별로 없다*.

## 10.13 추론 모드의 모델, 두 얼굴을 정리하며

이제 챕터를 닫자. 우리가 한 일을 한 줄씩 짚어두면 다음과 같다.

학습 시점의 모델과 추론 시점의 모델은 *같은 가중치, 다른 인프라*다. 학습은 한 덩어리 forward + backward이고, 추론은 *prefill + decode + KV cache*다.

KV cache는 `(n_layers, B, T_max, n_kv_heads, head_dim)` 모양의 *큰 텐서 두 개*다. 미리 할당하고, in-place로 업데이트하고, batch element마다 다른 위치를 *int32 cache_seqlens*로 들고 다닌다. `prefill(other)` 메서드 한 줄로 *batch=1 prompt를 num_samples로 복제*하는 트릭이 가능해진다.

Engine.generate는 prefill 1번 → KV cache 복제 → decode 루프 N번을 *한 함수*에 묶었다. 매 step `sample_next_token`이 토큰을 뽑고, 각 RowState가 *자기 사연*을 갱신하고, *forced_tokens deque*가 있으면 그쪽을 먼저 쓴다.

Tool use FSM은 단 17줄이다. `<|python_start|>` 들어오면 식 모으기 시작, `<|python_end|>`에서 도구 함수 호출, 결과를 `<|output_start|>` + 결과 토큰들 + `<|output_end|>`로 deque에 줄 세운다. *모델의 입을 잠깐 외부 계산기가 빌리는* 일이 이 짧은 코드에 다 들어 있다.

`use_calculator`는 *3초 timeout 화이트리스트* 인라인 평가. 순수 수식 또는 `.count(`. 안전한 fallback과 *빈 builtins* 약속으로 *간단하지만 충분한* 안전망. 진짜 sandbox는 `nanochat/execution.py`의 *별도 프로세스 + 256MB 메모리 제한 + 위험 함수 비활성화*에 있다.

chat_cli는 *100줄*. 한 turn의 prompt를 special token으로 감싸고, `assistant_start`를 priming으로 박고, Engine.generate의 stream을 *콘솔에 한 토큰씩* 흘려보낸다.

chat_web은 *407줄*. WorkerPool로 GPU N개에 모델을 복제하고, FastAPI의 SSE로 *브라우저에 한 토큰씩* 흘려보내고, UTF-8 멀티바이트 안전망으로 *한글·이모지가 깨지지 않게* 누적 디코드한다. abuse 방지 가드 다섯 줄이 *공개 데모용 방어선*을 친다.

`gpt.py`에 *짧고 느린 reference generate* 28줄을, `engine.py`에 *길고 빠른 production generate* 한 페이지를 — 한 자리에 둔다. 두 결과가 같다는 self-test로 *내 빠른 코드를 안심하고 쓰는 길*이 깔린다.

마지막으로 *이 모든 코드의 기여*를 한 줄로 정리하자면 — *그것은 결국 "모델과의 대화"라는 일을 가능하게 만든다*. 우리가 9장까지 *학습*한 가중치가, 10장의 *357 + 407 + 100줄*에 의해 *말을 한다*. 8천 줄의 작품 가운데 *천 줄도 안 되는* 이 부분이 *모든 학습의 결과물을 사용자에게 보여주는 일*을 맡는다. 이 비중이 *큰 LLM 시스템의 정직한 단면*이다 — 학습 코드가 추론 코드보다 *훨씬 무겁다*. 그래서 학습이 길고, 추론은 *짧지만 매끈해야* 한다.

기억해두자. 추론은 *학습과 다른 모드의 모델*이다. 같은 nn.Module이지만 *다른 인프라가 둘러싼다*. KV cache 한 덩어리, FSM 17줄, SSE 한 generator. 이 세 가지가 *대화*라는 일을 만든다.

자, 11장으로 가자. 우리가 10장까지 따라 읽은 모든 일을 *한 페이지의 markdown*으로 도장 찍는 챕터다. `report.md`. *우리가 진짜로 GPT-2급에 도달했다는 증거*가 한 페이지에 어떻게 정리되는지를 본다.

그 전에 — 우리는 방금 한 가지 일을 한 번 더 했다. *우리가 학습한 모델에게 "What is 9 times 8?"이라고 물었다. 모델이 `<|python_start|>9*8<|python_end|>`를 뱉었고, Engine이 `<|output_start|>72<|output_end|>`를 forced_tokens에 넣었고, 모델이 그 72를 자기 입으로 받아 답을 끝맺었다.*

`72라고 답한다.`
