# 5장. 옵티마이저는 왜 두 개인가 — AdamW와 Muon

*하나면 될 텐데 왜 두 개일까?*

3장에서 토크나이저 하나, 4장에서 모델 하나를 만들었다. 그런데 nanochat의 학습 스크립트를 열고 옵티마이저 부분을 들여다보면, *두 개*의 옵티마이저가 한 모델 위에서 동시에 굴러간다. 이름도 묘하다 — `MuonAdamW`. 마치 정체불명의 합성어를 만나는 기분이다. 임베딩에는 AdamW가, 행렬에는 Muon이 붙고, 둘이 같은 `step()` 호출 안에서 사이좋게 자기 몫을 처리한다.

처음 보면 *난감하다*. 옵티마이저는 모델 학습에서 가장 추상적인 부품이다. 모델은 눈으로 따라가면 어찌어찌 그림이 그려지는데, 옵티마이저는 그라디언트 하나 받아서 파라미터 하나 갱신하는 *블랙박스*다. 그 블랙박스가 *두 개* 있다고? 그것도 *섞어서* 쓴다고? 이런 의문이 생기는 게 자연스럽다.

그렇다면 한 번 천천히 풀어보자. 이 챕터에서는 카르파시가 왜 두 옵티마이저를 *섞어 썼는지*, Muon이 정확히 무엇을 하는지, Newton-Schulz iteration이 SVD를 어떻게 흉내내는지를 코드 한 줄 한 줄 따라가며 살핀다. 그리고 — 이 책 전체에서 *거의 유일한* — 수식 한 줄을 만나게 된다. 그 한 줄이 왜 한 줄로 충분한지도 끝에 가서 알게 될 것이다.

호흡은 천천히 가져가자. 4B의 차 한 잔 이후 처음 만나는 챕터라서, *기술서의 밀도*를 유지하면서도 한 박자 쉬어가는 페이스로 가도 괜찮다.

---

## AdamW, 30초 복습

먼저 AdamW부터 정리하고 들어가자. *이미 잘 알고 있다*고 느끼는 독자도 많을 텐데, Muon을 이해하려면 AdamW가 *어떤 일을 하는 옵티마이저인지* 그 본질을 짚고 가야 한다. 30초만 양해를 구한다.

가장 단순한 옵티마이저는 SGD다. 그라디언트의 *반대 방향*으로 파라미터를 한 스텝씩 이동시킨다. 한 줄로 쓰면 이렇다.

```python
p = p - lr * grad
```

여기에 *모멘텀*을 붙이면 한 단계 똑똑해진다. 매번 그라디언트를 새로 받지 않고, 이전 그라디언트들의 가중 평균을 누적해서 사용한다. 골짜기 옆면에서 흔들리지 않고 *바닥 방향으로 미끄러져 내려가는* 효과가 난다.

Adam은 여기에 두 가지 보정을 더 얹었다. 첫째는 *2차 모멘트*. 그라디언트의 *제곱*도 평균을 내서, 각 파라미터마다 *분산이 큰 차원*에서는 보폭을 줄이고, *분산이 작은 차원*에서는 보폭을 키운다. 둘째는 *bias correction*. 초기 몇 스텝에서는 모멘텀이 0에서 시작하니까 EMA가 *과소평가*된다 — 그걸 `1 - β^t`로 나눠서 보정한다. 모든 파라미터에 대해 *적응적 학습률*을 만들어내는 셈이다.

여기까지가 Adam이다. 그러면 W는 뭘까? *Decoupled weight decay*. weight decay(파라미터를 0 쪽으로 끌어당기는 정규화)를 *그라디언트에 더하는* 게 아니라, *파라미터 업데이트와 분리해서* 따로 적용한다는 뜻이다. Loshchilov와 Hutter가 2017년에 "이렇게 분리하면 Adam의 일반화 성능이 정말로 좋아진다"고 보고한 [작은 변경](https://arxiv.org/abs/1711.05101)이다. 지금은 사실상 모든 트랜스포머 학습의 *기본값*이 됐다.

nanochat의 `adamw_step_fused`를 직접 보자. `optim.py:21-50`.

```python
@torch.compile(dynamic=False, fullgraph=True)
def adamw_step_fused(
    p: Tensor,              # (32768, 768) - parameter tensor
    grad: Tensor,           # (32768, 768) - gradient, same shape as p
    exp_avg: Tensor,        # (32768, 768) - first moment, same shape as p
    exp_avg_sq: Tensor,     # (32768, 768) - second moment, same shape as p
    step_t: Tensor,         # () - 0-D CPU tensor, step count
    lr_t: Tensor,           # () - 0-D CPU tensor, learning rate
    beta1_t: Tensor,        # () - 0-D CPU tensor, beta1
    beta2_t: Tensor,        # () - 0-D CPU tensor, beta2
    eps_t: Tensor,          # () - 0-D CPU tensor, epsilon
    wd_t: Tensor,           # () - 0-D CPU tensor, weight decay
) -> None:
    # Weight decay (decoupled, applied before the update)
    p.mul_(1 - lr_t * wd_t)
    # Update running averages (lerp_ is cleaner and fuses well)
    exp_avg.lerp_(grad, 1 - beta1_t)
    exp_avg_sq.lerp_(grad.square(), 1 - beta2_t)
    # Bias corrections
    bias1 = 1 - beta1_t ** step_t
    bias2 = 1 - beta2_t ** step_t
    # Compute update and apply
    denom = (exp_avg_sq / bias2).sqrt() + eps_t
    step_size = lr_t / bias1
    p.add_(exp_avg / denom, alpha=-step_size)
```

거의 *수도코드* 수준이다. 한 줄 한 줄이 AdamW 정의서의 한 줄에 정확히 대응한다.

- `p.mul_(1 - lr_t * wd_t)` — decoupled weight decay. 업데이트 *전에* 파라미터를 살짝 0 방향으로 끌어당긴다.
- `exp_avg.lerp_(grad, 1 - beta1_t)` — 1차 모멘트 EMA 갱신. `lerp_(x, w)`는 `(1-w)*self + w*x`라서, 결과적으로 `β1 * exp_avg + (1-β1) * grad`가 된다.
- `exp_avg_sq.lerp_(grad.square(), 1 - beta2_t)` — 2차 모멘트.
- `bias1 = 1 - β1^t`, `bias2 = 1 - β2^t` — bias correction.
- `denom = sqrt(exp_avg_sq / bias2) + eps` — *분산의 제곱근*.
- `p.add_(exp_avg / denom, alpha=-step_size)` — 최종 업데이트.

복잡한 옵티마이저처럼 보이지만, *AdamW의 사양서*를 PyTorch로 그대로 받아 적은 것이다. *추가된 트릭이 하나도 없다*. 다만 nanochat은 이 함수에 `@torch.compile(dynamic=False, fullgraph=True)`를 붙여놨다. 이 데코레이터에 대한 이야기는 뒤에서 따로 다룬다 — 한 가지 *기억해두자*. 이게 단순한 컴파일 가속이 아니라 *0-D CPU 텐서 인자*와 한 쌍으로 등장하는 트릭이라는 점.

자, 30초 끝났다. AdamW는 *각 파라미터마다 독립적으로* 적응적 LR을 만들어 업데이트한다. 한 파라미터의 모멘텀은 다른 파라미터의 모멘텀과 *상호작용하지 않는다*. 그라디언트가 들어오면 EMA를 갱신하고, 분산으로 나누고, 끝이다.

— *바로 이 "독립적"이라는 점*이, 다음 절에서 Muon과 가르는 결정적인 차이가 된다.

---

## Muon, 한 문장으로

Muon은 [Keller Jordan이 2024년에 제안한](https://kellerjordan.github.io/posts/muon/) 옵티마이저다. 이름이 재미있다 — *MomentUm Orthogonalized by Newton-schulz*. 첫 글자를 모으면 Muon. *입자가속기에서 가져온 이름이 아니라 영문 acronym*이다.

직관은 한 문장으로 요약된다.

> momentum으로 모은 gradient를 *직교화*해서 업데이트로 쓴다.

이게 끝이다. 나머지는 전부 *그 한 문장을 어떻게 실현하느냐*에 대한 디테일이다.

먼저 *직교화*가 무슨 뜻인지부터 시각적으로 잡고 가자. 행렬 G가 SVD로 `G = U Σ V^T`로 분해된다고 하자. 여기서 Σ는 대각행렬, 그 대각 원소가 *특이값*(singular values)이다. 이 특이값들이 G가 어느 방향으로 *얼마나* 늘리는지를 알려준다. 큰 특이값에 대응하는 방향은 크게 늘어나고, 작은 특이값에 대응하는 방향은 거의 무시된다.

*직교화*란 무엇인가? Σ를 *항등행렬*로 만드는 것이다. 즉 `G ≈ U V^T`. 모든 특이값을 *1로 통일*한다. *모든 방향이 똑같이 중요해진다*.

비유로 풀면 이렇다. momentum으로 그라디언트를 누적하면, 시간이 지나면서 *한 방향으로 뭉치는* 경향이 생긴다. 가장 큰 특이값에 대응하는 방향이 *지배적*이 되고, 다른 방향들은 상대적으로 작아진다. 학습이 *한쪽으로만 빠르게 가고 다른 쪽은 천천히 가는* 비대칭이 생긴다는 뜻이다.

직교화는 그 뭉침을 *부풀려* 모든 축으로 펼치는 일이다. 한 방향으로 쏠려있던 업데이트의 에너지를 *모든 직교 방향에 골고루* 분배한다. 결과적으로 행렬의 *모든 row와 column*이 비슷한 강도로 갱신된다. *이게 어떻게 학습 속도를 올리느냐?* — 이론적 정당화는 [Keller Jordan의 블로그 글](https://kellerjordan.github.io/posts/muon/)에 자세하다. 핵심 직관은 "한 방향으로 쏠린 업데이트는 *낭비*다 — 모델은 모든 차원에서 학습할 잠재력이 있는데 한 쪽으로만 가니까"라는 것.

Keller Jordan은 modded-nanoGPT 리포에서 124M GPT-2를 *90초만에* 학습시키는 데 이 트릭이 핵심 역할을 했다고 보고한다. AdamW 대비 *약 35%* 빠른 수렴이다. 작은 변경 하나가 학습 시간을 35% 줄인다 — 이게 Muon이 modded-nanoGPT 커뮤니티에서 *센세이션*을 일으킨 이유다.

물론 공짜는 아니다. 직교화는 *행렬 연산*이다. SVD를 매 스텝 계산하면 GPU가 견디지 못한다. 그래서 Keller Jordan은 *Newton-Schulz iteration*이라는 영리한 근사를 가져왔다. 다음 절의 주인공이 그것이다.

---

## Newton-Schulz iteration — SVD의 *흉내내기*

Newton-Schulz iteration은 한 줄로 표현되는 *반복 점화식*이다. 행렬의 *직교 인자 부분*만 골라서, *SVD를 안 풀고*, GPU에서 *bf16으로 안정적으로* 계산할 수 있다. 이게 가능한 이유는 점화식이 *행렬 곱셈만으로* 구성되기 때문이다 — `tensor cores`가 가장 잘 하는 일.

이 책의 거의 모든 곳에서 수식은 코드로 풀린다. 1장에서 *수식 양보 예고*를 했던 그 약속, 기억하는가? 이 챕터에서만 *한 줄 양보*한다. 왜냐하면 Newton-Schulz 점화식만큼은 *수식 한 줄이 코드보다 명확*하기 때문이다. 그 한 줄이 *튜닝 대상*을 직접 가리키고, 다음 절에서 다룰 Polar Express가 *무엇을 바꾸는지*를 즉시 보여준다.

자, 그럼 그 한 줄을 만나보자.

> `X_{n+1} = a·X_n + b·X_n·X_n^T·X_n + c·(X_n·X_n^T)^2·X_n`

이게 *quintic Newton-Schulz iteration*이다. X를 5차 다항식으로 갱신한다. 항이 세 개다: `X` 한 개, `X·X^T·X` 한 개, `(X·X^T)^2·X` 한 개. 계수 a, b, c는 *튜닝 대상*이다. *바로 이게 quintic의 의미*. 다항식의 차수가 5라서 "quintic"이라고 부른다.

이 점화식이 왜 SVD `U·V^T`를 *흉내내는가*?

원리는 이렇다. 행렬 X의 SVD가 `X = U Σ V^T`라면, X를 위 점화식에 넣어 갱신하면 *U와 V는 그대로* 두고 Σ만 *어떤 함수 p(σ)로 변환*된다. 그 함수 p가 *5차 다항식*이고, 계수 a, b, c가 그 5차 다항식을 결정한다. 만약 p(σ)를 잘 골라서 *모든 σ를 1로 보내는 함수*에 가깝게 만들면, 몇 번의 반복 끝에 X는 `U·V^T`에 *수렴*한다.

비유하자면, 점화식은 *singular value들을 1로 끌고 가는 컨베이어 벨트*다. 한 스텝 돌릴 때마다 σ는 1쪽으로 한 발짝씩 다가간다. 컨베이어의 기울기를 결정하는 게 a, b, c. 잘 고른 계수면 5번 만에 충분히 가깝게 수렴한다.

코드로 보면 이렇다 (`optim.py:115-129`):

```python
# Polar express
X = g.bfloat16() if COMPUTE_DTYPE == torch.bfloat16 else g
X = X / (X.norm(dim=(-2, -1), keepdim=True) * 1.01 + 1e-6)
if g.size(-2) > g.size(-1): # Tall matrix
    for a, b, c in polar_express_coeffs[:ns_steps]:
        A = X.mT @ X
        B = b * A + c * (A @ A)
        X = a * X + X @ B
else: # Wide matrix (original math)
    for a, b, c in polar_express_coeffs[:ns_steps]:
        A = X @ X.mT
        B = b * A + c * (A @ A)
        X = a * X + B @ X
g = X
```

수식 한 줄과 코드를 *나란히* 놓고 보면 즉시 대응이 보인다.

- `A = X @ X.mT` — `X·X^T`. 한 번의 matmul.
- `A @ A` — `(X·X^T)^2`. 또 한 번의 matmul.
- `B = b * A + c * (A @ A)` — `b·X·X^T + c·(X·X^T)^2`. 행렬 합.
- `X = a * X + B @ X` — `a·X + b·X·X^T·X + c·(X·X^T)^2·X`. *바로 그 점화식*.

매 스텝마다 행렬 곱 *세 번*. 5번 반복하면 곱셈 15회. (1024×1024) 행렬에 대해 H100에서 *밀리초 단위*로 끝난다. *SVD를 직접 풀었으면* 같은 일을 하는 데 수십 배 시간이 걸렸을 것이다.

한 가지 *주의해야 한다*. 위 코드에서 `if g.size(-2) > g.size(-1)`로 *tall*인지 *wide*인지 분기한다. 왜 그럴까? 원래 Newton-Schulz는 `X·X^T·X`를 쓰지만, *tall*(행이 열보다 많음)일 때는 `X^T·X`가 더 작은 행렬이라서 `X @ (X.mT @ X)`로 *분배해서* 계산하면 메모리·연산이 훨씬 적게 든다. *수학적으로 동치*인데, 작은 쪽을 먼저 곱하는 게 효율적이다. *기본적인 결합법칙*이지만, GPU에서 큰 차이를 만든다.

그리고 점화식 직전에 X를 *정규화*하는 줄이 있다.

```python
X = X / (X.norm(dim=(-2, -1), keepdim=True) * 1.01 + 1e-6)
```

이건 *왜* 필요한가? Newton-Schulz는 *입력의 singular value가 0~1 범위에 있을 때*만 안정적으로 수렴한다. 정규화 없이 σ가 2, 3이 되면 점화식이 *발산*해버린다. 그래서 일단 행렬 전체의 Frobenius norm으로 나눠서 *singular value들이 1 이하로 들어가게* 만들어주는 단계다. `* 1.01`은 안전 마진. `+ 1e-6`은 0으로 나누기 방지.

물론 정규화로 *작아진 만큼* 결과 X의 스케일이 작아진다. 하지만 우리는 결국 `U V^T`라는 *방향 정보만* 가져갈 거라서, 스케일이 줄어든 건 *상관없다*. 학습률(`lr`)이 마지막에 곱해질 때 보정된다.

여기까지가 Newton-Schulz의 *시각적* 정체다. 5차 다항식 한 줄, 행렬 곱 15회, bf16에서 안정. *그것뿐*이다.

---

## Polar Express — Newton-Schulz의 *튜닝된 친척*

위 코드를 다시 보면 `polar_express_coeffs`라는 리스트가 등장한다. Newton-Schulz라고 부르긴 하는데, 사실 nanochat이 쓰는 *정확한* 변종은 **Polar Express**다 ([arXiv:2505.16932](https://arxiv.org/abs/2505.16932)). Noah Amsel, David Persson, Christopher Musco, Robert M. Gower의 2025년 논문이다.

차이가 뭘까? *기본 골격은 같다*. Quintic 점화식 — `X_{n+1} = a·X_n + b·X·X^T·X + c·(X·X^T)^2·X`. 다른 건 *계수 a, b, c를 매 스텝마다 다르게 쓴다*는 점.

원래 Keller Jordan이 modded-nanoGPT에서 쓴 Newton-Schulz는 5번의 반복 *내내 같은 계수*를 썼다. 단순하고 잘 작동했다. Polar Express의 통찰은 이렇다 — "*매 스텝마다 다른 계수를 쓰면, 같은 5번 반복으로도 더 빨리 수렴할 수 있다.*"

비유하자면, 컨베이어 벨트의 *기울기*를 매 스텝마다 바꾸는 것이다. 처음에는 가파르게(σ를 빠르게 1로 끌고), 나중에는 완만하게(미세 조정). *step-by-step optimized*.

코드로는 `optim.py:81-89`:

```python
# Coefficients for Polar Express (computed for num_iters=5, safety_factor=2e-2, cushion=2)
# From https://arxiv.org/pdf/2505.16932
polar_express_coeffs = [
    (8.156554524902461, -22.48329292557795, 15.878769915207462),
    (4.042929935166739, -2.808917465908714, 0.5000178451051316),
    (3.8916678022926607, -2.772484153217685, 0.5060648178503393),
    (3.285753657755655, -2.3681294933425376, 0.46449024233003106),
    (2.3465413258596377, -1.7097828382687081, 0.42323551169305323),
]
```

5개의 `(a, b, c)` 튜플. 5번 반복용. `safety_factor=2e-2, cushion=2`는 논문이 *수렴 보장 영역*을 어떻게 잡았는지를 가리키는 파라미터다. *논문을 다 읽지 않아도* — 우리는 결과 계수만 가져다 쓰면 된다.

첫 스텝의 a를 보자. **8.156**. 어마어마하게 큰 값이다. b는 **-22.48**, c는 **15.88**. *극단적인 계수로 시작*한다. 이게 σ를 강하게 1쪽으로 밀어주는 단계다. 두 번째 스텝부터 계수가 *부드러워진다* — a=4, b=-2.8, c=0.5. 그 후로는 점점 *세밀한 조정*으로 들어간다.

흥미로운 디테일 — 이 계수들은 *모델 학습마다 다시 계산할 필요가 없다*. 한 번 계산해놓은 상수다. nanochat은 *논문이 발표한 계수를 그대로 박아두고* 쓴다. *수치 최적화 문제를 미리 풀어 놓은 답*인 셈이다.

여기서 *주석 한 줄*에 주목해보자.

```python
# Coefficients for Polar Express (computed for num_iters=5, safety_factor=2e-2, cushion=2)
```

이 한 줄이 *Polar Express의 정신*을 압축한다. 계수는 *반복 횟수에 맞춰* 최적화된다. ns_steps=5라고 가정하고 *5단계로 최대한 빠르게 수렴*하도록 풀어놓은 답이다. 만약 ns_steps=3으로 쓰고 싶다면? 계수를 *다시 계산*해야 한다. 단순히 앞의 3개를 가져다 쓰면 *원하는 수렴*이 안 나온다. *기억해두자*.

그리고 한 가지 *물론 ~다. 하지만 ~* 패턴. *물론* Newton-Schulz가 더 간단하고 직관적이다. *하지만* Polar Express는 *논문의 보장된 수렴 영역 안에서 같은 시간 안에 더 정확*하다. 차이가 모델 학습 결과에서 눈에 띌 만큼 큰가? — 카르파시는 commits 로그에서 "Polar Express로 바꾸고 작은 개선이 있었다"고 보고했다. 거대한 차이는 아니지만, *제대로 보정한 계수*를 쓰면 *공짜로 살짝 더 빨리* 수렴한다.

이게 *현대 ML 엔지니어링의 미학*이다. 큰 알고리즘 하나로 끝나는 게 아니라, *작은 개선들*이 *겹겹이* 쌓여서 모델을 만든다. Polar Express는 그 작은 개선의 한 층이다.

---

## NorMuon — 직교화 후의 *마지막 한 줄 조정*

여기서 멈춰도 될 것 같다. momentum으로 누적해서, Polar Express로 직교화하고, 학습률로 곱해 업데이트한다. *Muon의 전형적인 동작*이다.

그런데 *난감한 사실 하나*가 남아 있다. 직교화 결과 X가 *완전한* `U V^T`가 아니라는 점이다. *직교 행렬*의 *근사*다. *근사인 만큼* row마다 norm이 *완벽히 동일하지는 않다*.

`optim.py:62-64`의 주석을 보자.

```python
# ...this iteration therefore does not produce UV^T but rather something like US'V^T
# where S' is diagonal with S_{ii}' ~ Uniform(0.5, 1.5), which turns out not to hurt model
# performance at all relative to UV^T
```

번역하면 — "*Newton-Schulz의 결과는 정확한 `UV^T`가 아니라 `US'V^T`에 가깝다. 여기서 S'의 대각 원소는 대략 0.5~1.5 사이로 흩어져 있다. 모델 성능에는 큰 영향이 없더라.*"

*큰 영향이 없더라*. 하지만 *작은 영향*은 있다. row마다 업데이트 크기가 들쭉날쭉이라는 뜻이다. 어떤 row는 1.5배 크게 갱신되고, 어떤 row는 0.5배만 갱신된다.

여기서 **NorMuon**이 등장한다. [arXiv:2510.05491](https://arxiv.org/abs/2510.05491) — *Neuron-wise variance reduction in Muon*. 직교화 후에도 row(또는 column)마다 norm이 *불균등*한 문제를 *factored second moment*로 보정하는 트릭이다.

*Factored second moment*가 뭔지부터 천천히 보자. AdamW에서 `exp_avg_sq`는 *각 파라미터마다 따로* 분산을 저장했다. 같은 모양의 텐서다. NorMuon에서는 그렇게 안 한다. *row별* 또는 *column별*로 *하나의 스칼라*를 저장한다.

코드로 보면 (`optim.py:131-142`):

```python
# Variance reduction
beta2 = beta2_t.to(g.dtype)
v_mean = g.float().square().mean(dim=red_dim, keepdim=True)
red_dim_size = g.size(red_dim)
v_norm_sq = v_mean.sum(dim=(-2, -1), keepdim=True) * red_dim_size
v_norm = v_norm_sq.sqrt()
second_momentum_buffer.lerp_(v_mean.to(dtype=second_momentum_buffer.dtype), 1 - beta2)
step_size = second_momentum_buffer.clamp_min(1e-10).rsqrt()
scaled_sq_sum = (v_mean * red_dim_size) * step_size.float().square()
v_norm_new = scaled_sq_sum.sum(dim=(-2, -1), keepdim=True).sqrt()
final_scale = step_size * (v_norm / v_norm_new.clamp_min(1e-10))
g = g * final_scale.to(g.dtype)
```

복잡해 보인다. 천천히 풀어보자.

1. `v_mean = g.square().mean(dim=red_dim, keepdim=True)` — *row(또는 column)별* 제곱 평균. 한 row가 평균적으로 얼마나 큰 값들로 채워져 있는지.
2. `v_norm = sqrt(v_mean.sum() * red_dim_size)` — 전체 norm. *원래의 크기*를 기억해둔다.
3. `second_momentum_buffer.lerp_(v_mean, 1 - beta2)` — EMA로 row별 분산 누적. AdamW의 exp_avg_sq와 비슷하다.
4. `step_size = buffer.rsqrt()` — 분산의 역수. *큰 분산의 row는 적게 갱신, 작은 분산의 row는 크게 갱신*.
5. `final_scale = step_size * (v_norm / v_norm_new)` — 한 가지 *세심한 보정*. row별로 다르게 스케일링하면 전체 norm이 변해버리니까, *원래의 v_norm*과 일치하게 다시 *전역 보정*한다.
6. `g = g * final_scale` — 적용.

*핵심 직관 한 줄*. *직교화로 균일하지 않게 나온 row들의 norm을, 그동안 누적된 row별 분산으로 평탄화한다.* 그게 NorMuon이다.

비유하자면 — 컨베이어 벨트(Polar Express)로 SVD를 거의 균일하게 만들었지만, 미세한 *높낮이*가 남아 있다. NorMuon은 그 높낮이를 *기억해 두었다가 거꾸로 보정*한다.

저장 공간이 *factored*라는 게 중요하다. 만약 g가 (768, 3072)라면, *full second moment*는 그대로 (768, 3072) 메모리를 차지해야 한다. NorMuon은 *row별 또는 column별* 평균만 저장한다 — (768, 1) 또는 (1, 3072). *행/열 중 짧은 쪽*에 차원을 축소한다. *메모리 효율*이 압도적이다.

코드의 `red_dim` 결정 로직을 보자 (`optim.py:256`):

```python
red_dim = -1 if shape[-2] >= shape[-1] else -2
```

*tall*(행이 더 많음)이면 `red_dim=-1` (column 방향으로 평균). *wide*(열이 더 많음)이면 `red_dim=-2` (row 방향으로 평균). *항상 작은 쪽에 축소*해서 더 큰 통계량 텐서를 만들지 않게 한다.

`second_momentum_buffer`의 모양도 그래서 *2차원이 아니라 사실상 1차원*에 가깝다. `(num_params, shape[-2], 1)` 또는 `(num_params, 1, shape[-1])`. *broadcasting으로 작동*한다. 메모리는 *원본 파라미터의 1/min(shape[-2], shape[-1])* 수준이다. 768 차원이라면 *약 1/768*. *엄청난 절약*이다.

여기까지가 NorMuon. *직교화의 잔여 불균형을 마지막에 다듬는 변종*.

---

## Cautious Weight Decay — *update와 같은 부호*에만

Muon의 마지막 줄을 보자.

```python
# Cautious weight decay + parameter update
lr = lr_t.to(g.dtype)
wd = wd_t.to(g.dtype)
mask = (g * stacked_params) >= 0
stacked_params.sub_(lr * g + lr * wd * stacked_params * mask)
```

*맨 마지막 줄*. weight decay가 *그냥* 적용되지 않는다. `mask`로 *필터링*된다.

`mask = (g * stacked_params) >= 0`. g와 stacked_params를 곱한 게 *0 이상*이면 True. 즉, *update와 파라미터가 같은 부호*일 때만 True.

여기에 weight decay가 *곱해진다*. mask가 False인 곳, 즉 *update와 파라미터의 부호가 반대인* 곳에서는 weight decay가 *적용되지 않는다*.

왜 이렇게 하는가? *직관*은 이렇다.

Weight decay는 파라미터를 0 쪽으로 끌어당긴다. 그런데 *그라디언트도 이미 같은 방향(0 쪽)으로 끌어당기는 경우가 있다*. 그럴 때는 *둘이 협력*한다 — weight decay가 도움이 된다. 하지만 *그라디언트는 파라미터를 더 크게 만들려고 하는데, weight decay만 거꾸로 0으로 끌어당기는 경우*가 있다. 그런 *충돌 상황*에서는 weight decay가 *학습을 방해*한다.

"Cautious"라는 이름이 그래서 붙었다. *조심스럽게* — *update와 같은 부호*일 때만 weight decay를 건다.

부등호 정밀하게 짚어두자. `(g * stacked_params) >= 0` — `g`는 직교화·NorMuon까지 다 거친 *최종 업데이트 방향*이고, `stacked_params`는 *현재 파라미터*다. update는 *나중에* `-= lr * g`로 적용된다 (`sub_`). 즉 g가 *양수*면 파라미터는 *작아진다*. g와 파라미터가 *같은 부호*라는 건 — 예컨대 둘 다 양수일 때 — 업데이트는 파라미터를 *0 쪽으로* 끌어당긴다. weight decay와 *같은 방향*이다. 그래서 mask=True, weight decay 적용.

반대로 g가 음수이고 파라미터가 양수라면 — 업데이트는 파라미터를 *더 크게 만든다*. 이때 weight decay를 또 적용하면 *둘이 싸운다*. 그래서 mask=False, weight decay *제외*.

*기억해두자*. Cautious weight decay는 *충돌이 없는 곳에만* WD를 건다. 그라디언트와 정규화가 *협력*할 때만.

그리고 한 가지 더 — nanochat에서는 weight decay를 *코사인 스케줄*로 0까지 가져간다 (`base_train.py:385-386`). 학습 초반에는 weight decay가 살아 있고, 끝에 가까워질수록 *사라진다*. 이건 6장에서 자세히 다룬다.

여기까지가 Muon의 *전체*다. 한 함수에 다 들어있다 — `muon_step_fused`, 56줄 (`optim.py:92-148`).

1. Nesterov momentum (lerp 두 번).
2. Polar express orthogonalization (5번 반복).
3. NorMuon variance reduction.
4. Cautious weight decay + 업데이트.

이 *네 단계*가 *한 fused graph*에 들어가서 한 번에 실행된다. Python 오버헤드 없이.

---

## 왜 임베딩에 Muon을 쓰면 *안 되는가*

여기까지 오면 자연스러운 질문이 떠오른다. *그렇게 좋은 Muon인데, 왜 모든 파라미터에 쓰지 않지?*

답은 두 가지다.

**첫 번째 — Muon은 2D 행렬에만 작동한다.** Newton-Schulz iteration이 `X·X^T·X` 같은 행렬 곱을 쓰기 때문이다. 0차원(스칼라)이나 1차원(벡터)에는 *그 곱 자체가 정의되지 않는다*. nanochat 모델 안에는 학습 가능한 *스칼라*가 있다 — `resid_lambdas`, `x0_lambdas`, `smear_lambda`, `backout_lambda` 등. 이들에게 Muon을 적용하는 건 *문법적으로* 안 된다.

`optim.py:168-171`의 주석을 직접 보자.

```python
# Some warnings:
# - The Muon optimizer should not be used for the embedding layer, the final fully connected layer,
# or any {0,1}-D parameters; those should all be optimized by a standard method (e.g., AdamW).
# - To use it with 4D convolutional filters, it works well to just flatten their last 3 dimensions.
```

*경고문*이다. 카르파시가 *의도적으로 박아두었다*. "embedding, final FC, 0/1차원 파라미터에는 Muon을 *쓰지 말 것*."

**두 번째 — 임베딩과 lm_head는 *sparse update*다.** 임베딩 테이블이 `(32768, 768)`이라고 하자. 32768개 토큰 중 한 배치에 등장하는 토큰은 *몇 천 개* 정도. 등장하지 않은 토큰의 row는 *그라디언트가 0*이다. 즉 그라디언트 행렬의 *대부분의 row가 0*이다. *극단적으로 sparse*하다.

이 sparse한 그라디언트에 *직교화*를 적용하면 어떻게 될까? *부풀려진다*. Muon의 본질은 "한쪽으로 쏠린 update를 모든 방향으로 펼친다"는 것. *0인 row를 활성화시키는 셈*이다. 등장하지도 않은 토큰의 임베딩이 *흔들린다*. *학습이 안 되는 게 아니라, 오히려 학습을 망치는* 결과를 낳는다.

또 row마다 *update 강도가 매우 다르다*. 흔한 토큰("the", " ", ".")의 row는 *매번* 갱신되고, 희귀 토큰의 row는 *가끔만* 갱신된다. 이런 *불균등한 update density*는 *AdamW의 적응적 분산 보정*과 잘 맞는다. *각 row가 독립적으로* 자기 분산을 추적하면 된다. Muon은 *행렬 전체에 한꺼번에 작용*하니까 이런 sparse-friendly 성질이 없다.

*그래서 split*. 임베딩, lm_head, value_embeds, 그리고 모든 스칼라 파라미터는 *AdamW*로. 트랜스포머 블록 내부의 *2D 행렬들*(attention의 Q/K/V/O, MLP의 fc_in/fc_out)은 *Muon*으로.

*직관적인 결정*이다. *Muon이 잘 작동하는 행렬형 파라미터*에는 Muon을, *Muon이 작동하지 않거나 위험한 sparse·scalar 파라미터*에는 AdamW를. *나눠서 쓴다*.

이런 분리 자체가 새로운 발상은 아니다. modded-nanoGPT에서 이미 표준이 된 패턴이다. 다만 nanochat은 *어떻게 그 분리를 깔끔하게 코드로 표현하느냐*에서 한 단계 더 나아갔다. 다음 절의 `setup_optimizer`가 그 답이다.

---

## `setup_optimizer` — 7개의 param group

`gpt.py:374-414`. 한 번 천천히 같이 읽어보자.

```python
def setup_optimizer(self, unembedding_lr=0.004, embedding_lr=0.2, matrix_lr=0.02, weight_decay=0.0, scalar_lr=0.5):
    model_dim = self.config.n_embd
    ddp, rank, local_rank, world_size = get_dist_info()

    # Separate out all parameters into groups
    matrix_params = list(self.transformer.h.parameters())
    value_embeds_params = list(self.value_embeds.parameters())
    embedding_params = list(self.transformer.wte.parameters())
    lm_head_params = list(self.lm_head.parameters())
    resid_params = [self.resid_lambdas]
    x0_params = [self.x0_lambdas]
    smear_params = [self.smear_gate.weight, self.smear_lambda, self.backout_lambda]
    assert len(list(self.parameters())) == len(matrix_params) + len(embedding_params) + len(lm_head_params) + len(value_embeds_params) + len(resid_params) + len(x0_params) + len(smear_params)
```

먼저 *모든 파라미터를 7개 그룹으로 나눈다*. 그 7개를 살피자.

1. **matrix_params** — `self.transformer.h.parameters()`. 트랜스포머 블록 내부의 모든 가중치 행렬. attention Q/K/V/O, MLP fc_in/fc_out. *2D 행렬*들이다. → Muon.

2. **value_embeds_params** — value embeddings (4B에서 본 그 *value embeddings*). 첫 두 블록에서 토큰별 value를 더해주는 임베딩이다. 임베딩의 일종이라 → AdamW.

3. **embedding_params** — `self.transformer.wte.parameters()`. *입력 임베딩 테이블*. *각 토큰 ID → 768차 벡터* 사전. → AdamW.

4. **lm_head_params** — *출력 임베딩*(언어 모델 헤드). vocab 위에 logit 계산하는 행렬. 임베딩과 weight-tying이 안 된 *별도 파라미터*다. → AdamW.

5. **resid_params** — `self.resid_lambdas`. 4B에서 본 *residual lambda*. 매 블록마다 residual을 어느 정도 섞을지를 *학습 가능한 스칼라*로 가지고 있다. → AdamW.

6. **x0_params** — `self.x0_lambdas`. 마찬가지로 4B에서 본 *x0 mixing weight*. *학습 가능 스칼라*. → AdamW.

7. **smear_params** — `[self.smear_gate.weight, self.smear_lambda, self.backout_lambda]`. *smear*와 *backout*에 관련된 작은 가중치들. 일부는 작은 텐서, 일부는 스칼라. → AdamW.

그리고 *맨 마지막 assert*가 *날카로운 안전 장치*다.

```python
assert len(list(self.parameters())) == len(matrix_params) + ... + len(smear_params)
```

*모든 파라미터의 합*이 *위 7개 그룹의 합*과 같은지 *런타임에 검증*한다. 모델 정의에 새 파라미터를 추가하면서 setup_optimizer에 빠뜨리면 — *즉시 빨간불*이 켜진다. *난감한 디버깅*을 *컴파일 타임에 가까운 시점*으로 끌어올렸다.

*기억해두자*. 이런 assert는 *번거롭다고 느낄 수 있지만*, 모델을 *진화시키는 책*인 nanochat의 정신에서는 *반드시 있어야* 한다. 매번 새 파라미터 그룹을 추가할 때 *놓치지 않게* 해준다.

자, 그룹을 다 나눴다. 이제 *각 그룹에 어떤 lr·beta·weight_decay를 줄지*가 남았다. 그 부분이 *재미있다*.

```python
# Scale the LR for the AdamW parameters by ∝1/√dmodel (tuned for 768 dim model)
dmodel_lr_scale = (model_dim / 768) ** -0.5
print0(f"Scaling the LR for the AdamW parameters ∝1/√({model_dim}/768) = {dmodel_lr_scale:.6f}")

# Build param_groups with all required fields explicit
param_groups = [
    # AdamW groups (embeddings, lm_head, scalars)
    dict(kind='adamw', params=lm_head_params, lr=unembedding_lr * dmodel_lr_scale, betas=(0.8, 0.96), eps=1e-10, weight_decay=0.01),
    dict(kind='adamw', params=embedding_params, lr=embedding_lr * dmodel_lr_scale, betas=(0.8, 0.995), eps=1e-10, weight_decay=0.001),
    dict(kind='adamw', params=value_embeds_params, lr=embedding_lr * dmodel_lr_scale * 0.5, betas=(0.8, 0.995), eps=1e-10, weight_decay=0.01),
    dict(kind='adamw', params=resid_params, lr=scalar_lr * 0.01, betas=(0.8, 0.95), eps=1e-10, weight_decay=0.05),
    dict(kind='adamw', params=x0_params, lr=scalar_lr, betas=(0.96, 0.95), eps=1e-10, weight_decay=0.0),  # higher beta1 for x0
    dict(kind='adamw', params=smear_params, lr=0.2, betas=(0.8, 0.95), eps=1e-10, weight_decay=0.0),
]
# Muon groups (matrix params, grouped by shape for stacking)
for shape in sorted({p.shape for p in matrix_params}):
    group_params = [p for p in matrix_params if p.shape == shape]
    param_groups.append(dict(
        kind='muon', params=group_params, lr=matrix_lr,
        momentum=0.95, ns_steps=5, beta2=0.9, weight_decay=weight_decay,
    ))
```

크게 *두 가지* 흥미로운 디테일이 있다. 하나씩 보자.

---

## `dmodel_lr_scale = (model_dim/768)^-0.5`

`(model_dim / 768) ** -0.5`. 이게 무엇인가?

nanochat은 *여러 크기의 모델*을 지원한다. depth 4 (작음)부터 depth 32까지 (큼). 모델이 커지면 `model_dim`이 커진다 — d4면 256, d20이면 1280, d32면 1536(혹은 더 큼).

*기본 하이퍼파라미터들*(unembedding_lr, embedding_lr, scalar_lr)은 *768 차원 모델 기준으로 튜닝*되어 있다 (768은 GPT-2 small의 model_dim). 모델 크기를 바꿔도 *같은 LR*을 쓰면 *큰 모델일수록 너무 크다*. *작은 모델일수록 너무 작다*.

*경험적인 보정*이 `1 / sqrt(model_dim / 768)`이다. *μP 스케일링 법칙*에서 영감을 받은 보정이다 — *모델이 커질수록 LR은 1/√dim 비율로 줄어들어야* 비슷한 학습 동역학을 유지한다는 이론.

`d4` 모델 (`model_dim=256`)이라면? `(256/768)^-0.5 = sqrt(3) ≈ 1.73`. AdamW LR이 *1.73배 커진다*. 작은 모델일수록 *상대적으로 큰 LR*을 쓴다.

`d32` 모델 (`model_dim=1536`)이라면? `(1536/768)^-0.5 = 1/sqrt(2) ≈ 0.71`. AdamW LR이 *0.71배 작아진다*. 큰 모델은 *살살*.

*깔끔한 한 줄*이다. 모델 크기와 LR을 *자동으로 연결*해준다. 사용자가 `depth`만 바꿔도 AdamW LR은 *알아서 적절히 조정*된다. *번거로운 튜닝*을 한 줄로 해결.

*주의해야 한다*. 이 스케일은 *AdamW 그룹에만* 적용된다. Muon 그룹의 LR(`matrix_lr=0.02`)에는 *적용되지 않는다*. Muon은 자체적으로 *행렬 모양에 따른 보정*을 한다 — `muon_step_fused`를 호출하는 코드를 보면 (`optim.py:265`):

```python
self._muon_lr_t.fill_(group["lr"] * max(1.0, shape[-2] / shape[-1])**0.5)
```

*tall matrix*(행이 열보다 많음)에서는 `sqrt(row/col)` 배만큼 LR을 *올린다*. 행렬이 *세로로 길면 더 큰 LR*. 직교화의 결과를 행 방향으로 더 크게 만들기 위한 보정이다. *Muon만의 행렬 모양 보정*이라서, AdamW의 dmodel_lr_scale과는 *독립적*이다.

---

## Muon 그룹은 *shape별*로 묶인다

`setup_optimizer`의 *맨 마지막 루프*.

```python
for shape in sorted({p.shape for p in matrix_params}):
    group_params = [p for p in matrix_params if p.shape == shape]
    param_groups.append(dict(
        kind='muon', params=group_params, lr=matrix_lr,
        momentum=0.95, ns_steps=5, beta2=0.9, weight_decay=weight_decay,
    ))
```

*shape별로 묶어서* param group을 만든다. *왜 그렇게 하는가?*

답은 `muon_step_fused`에 있다. `optim.py:258-260`을 다시 보자.

```python
# Stack grads and params (NOTE: this assumes all params have the same shape)
stacked_grads = torch.stack([p.grad for p in params])
stacked_params = torch.stack(params)
```

*torch.stack*. 한 그룹의 모든 파라미터를 *하나의 텐서*로 쌓는다. 그리고 `muon_step_fused`는 그 stacked 텐서에 *한 번에* 직교화·variance reduction을 적용한다.

*torch.stack은 모양이 같은 텐서들만 쌓을 수 있다*. (768, 3072)와 (768, 768)을 같이 못 쌓는다. *그래서 shape별로 묶어야 한다*.

이 디자인의 장점은 *대단하다*. 트랜스포머에서 같은 모양의 행렬이 *수십 개*씩 등장한다 — 모든 블록의 Q, 모든 블록의 K, 모든 블록의 V, 모든 블록의 O, 모든 블록의 fc_in, 모든 블록의 fc_out. d20 모델이면 *블록이 20개*라서, Q 한 종류만 해도 20개의 같은 모양 행렬이 있다.

이걸 *한 stacked 텐서*로 쌓아서 `muon_step_fused`에 *한 번* 던지면 — Newton-Schulz의 15회 행렬 곱이 *20개에 대해 batched*로 돌아간다. GPU의 *batched matmul*은 단일 matmul보다 *훨씬 효율적*이다. *기억해두자*. nanochat의 Muon이 빠른 *진짜 이유*는 알고리즘이 빨라서가 아니라, *stacking으로 batched matmul*을 활용하기 때문이다.

shape별 그룹화는 *Muon에만 적용*된다. AdamW는 파라미터를 *개별적으로* 처리한다 (`_step_adamw`의 `for p in group['params']` 루프). AdamW는 *적응적 분산*이 *파라미터마다 독립*이라서 stacking 이점이 없다.

여기서 *재미있는 우연*이 있다. nanochat의 트랜스포머에서 Q, K, V, O가 *하나의 fused QKVO 텐서로 합쳐져 있지 않다*. 일부 다른 구현(예: GPT-NeoX, Megatron)에서는 attention의 4개 weight를 *하나의 큰 텐서*로 fused한다. nanochat은 그렇게 안 한다. *왜?* — 코드 주석을 보자 (`optim.py:78`):

```python
# - Makes no assumptions about model architecture (e.g. that attention weights are fused into QKVO format)
```

*"모델 구조에 대한 가정을 하지 않는다"*. nanochat의 Muon은 *fused QKVO를 강제하지 않는다*. 대신 *shape가 같으면 자동으로 stacking으로 batched* 처리한다. *유연하고 일반적인 디자인*이다.

---

## `@torch.compile` + 0-D CPU 텐서 트릭

이제 *기술적으로 가장 영리한* 부분으로 들어가자. 두 fused 함수에 모두 붙어 있는 데코레이터.

```python
@torch.compile(dynamic=False, fullgraph=True)
def adamw_step_fused(...):
    ...

@torch.compile(dynamic=False, fullgraph=True)
def muon_step_fused(...):
    ...
```

`torch.compile`은 PyTorch 2.x의 *그래프 컴파일러*다. 함수 안의 PyTorch 연산을 *추적*해서 *하나의 최적화된 그래프*로 만든다. Python 인터프리터 오버헤드가 사라지고, 텐서 연산들이 *fused kernel*로 합쳐진다. 효과? — *훨씬 빠르다*. CPU-GPU launch overhead가 줄어들고, 메모리 대역폭이 절약된다.

옵션 두 개를 보자.

- `dynamic=False` — *동적 shape를 가정하지 않음*. 매번 같은 shape가 들어온다고 가정. 그래서 컴파일이 *한 번만* 일어난다.
- `fullgraph=True` — *graph break를 허용하지 않음*. 함수 전체를 *하나의 그래프*로 만들어야 한다. 만약 중간에 graph break가 일어나면 *에러*를 낸다. 디버깅과 성능 보장을 위한 옵션이다.

*문제는 이거다*. `torch.compile`은 *입력의 모양과 값*이 *동일한 패턴*일 때만 캐시된 그래프를 쓴다. 입력이 바뀌면 *재컴파일*. *재컴파일은 느리다*. *처음 컴파일하는 데만 몇 초 걸린다*.

학습 중에는 *매 스텝마다 LR이 다르다*. cosine schedule이든 linear warmup이든, *step마다 새로운 LR*이 들어간다. 만약 LR을 *Python float*로 넘기면 — `torch.compile`은 그걸 *상수*로 인식해서 *매 스텝 재컴파일*한다. 학습이 *완전히 망가진다*. *난감한 일이다*.

*해결책이 영리하다*. *LR을 0-D CPU 텐서*로 넘긴다. 

```python
self._adamw_lr_t = torch.tensor(0.0, dtype=torch.float32, device="cpu")
```

매 스텝마다 *그 텐서의 값만 바꾼다*.

```python
self._adamw_lr_t.fill_(group['lr'])
```

`torch.compile`은 텐서 *인자*는 *상수가 아니라 변수*로 본다. 텐서 *값*이 달라져도 *컴파일된 그래프는 재사용*된다. *재컴파일이 일어나지 않는다*.

*0-D CPU* 텐서인 이유도 있다. *GPU 텐서*로 넘기면 *GPU에 한 번 sync*가 일어나야 해서 비싸다. *CPU 텐서*로 넘기면 *값을 그대로 그래프에 전달*할 수 있고, GPU는 *비동기로 그 값을 받아 사용*한다.

함수 시그니처를 다시 보자.

```python
step_t: Tensor,         # () - 0-D CPU tensor, step count
lr_t: Tensor,           # () - 0-D CPU tensor, learning rate
beta1_t: Tensor,        # () - 0-D CPU tensor, beta1
beta2_t: Tensor,        # () - 0-D CPU tensor, beta2
eps_t: Tensor,          # () - 0-D CPU tensor, epsilon
wd_t: Tensor,           # () - 0-D CPU tensor, weight decay
```

*모든 하이퍼파라미터가 0-D CPU 텐서*다. step count도, LR도, beta도, eps도, weight decay도. *전부* `.fill_()`로 매 스텝 갱신된다.

이 트릭 하나로 `torch.compile`의 *컴파일 비용*과 *런타임 가속*을 동시에 얻는다. 그래프는 *처음 한 번*만 컴파일되고, *모든 step에서 재사용*된다. *깔끔하고 영리하다*.

*기억해두자*. 이건 nanochat이 *발명한 트릭*은 아니다. PyTorch 커뮤니티에서 *2.x compile을 깊이 쓰는 사람들*이 공유하는 패턴이다. 다만 nanochat은 그걸 *옵티마이저 안에 깊이 통합*했다 — 단순히 외부에서 호출만 하는 게 아니라, *클래스의 일부로* 0-D CPU 텐서들을 *관리*한다.

---

## (선택 박스) `DistMuonAdamW` — 3-phase async, *PyTorch DDP를 안 쓰는 이유*

> **이 절은 분산 학습에 관심 있는 독자를 위한 *선택적 깊이*다. 처음 읽을 때 건너뛰어도 다음 챕터를 이해하는 데 문제없다. 한 번 마음먹고 읽으면 *PyTorch의 분산 통신 API*에 대한 감각이 한 단계 늘어난다.**

`MuonAdamW`는 단일 GPU 버전이다. *학습이 정말로 일어나는 곳*은 다중 GPU 분산 환경이다. nanochat은 이를 위해 `DistMuonAdamW`를 따로 만들었다 (`optim.py:299-536`). *PyTorch DDP를 쓰지 않고* 자체 분산을 짠다.

*왜 DDP를 안 쓰는가?* — 두 가지 이유다.

첫째, **ZeRO-2 스타일 옵티마이저 state sharding**. 옵티마이저 state가 GPU 메모리의 *상당 부분*을 차지한다. AdamW는 파라미터마다 `exp_avg`, `exp_avg_sq` 두 개를 저장한다. 파라미터의 *3배 메모리*다. 1B 파라미터 모델이면 옵티마이저 state만 *12GB* (fp32). DDP는 *모든 rank가 모든 옵티마이저 state를 복제*한다. *낭비*가 크다. ZeRO-2는 *옵티마이저 state를 rank별로 나눠* 저장한다. 같은 메모리로 *더 큰 모델*을 학습할 수 있다. PyTorch에도 *FSDP*가 있지만, 디자인이 *훨씬 복잡*하다. nanochat은 *교육용*이라서 *직접 ZeRO-2를 구현*한다.

둘째, **Muon은 stacked tensor 위에서 작동**한다. 일반 DDP는 *파라미터별로* gradient를 reduce한다. Muon은 *그룹 단위*로 stacking된 텐서를 다룬다. *그 단위*에 맞춰 통신을 *그룹 단위로* 일으키는 게 자연스럽다.

`DistMuonAdamW.step()`의 *3-phase 구조*를 보자 (`optim.py:509-535`).

```python
@torch.no_grad()
def step(self):
    rank = dist.get_rank()
    world_size = dist.get_world_size()

    # Phase 1: launch all async reduce ops
    reduce_infos: list[dict] = []
    for group in self.param_groups:
        if group['kind'] == 'adamw':
            reduce_infos.append(self._reduce_adamw(group, world_size))
        elif group['kind'] == 'muon':
            reduce_infos.append(self._reduce_muon(group, world_size))
        else:
            raise ValueError(f"Unknown optimizer kind: {group['kind']}")

    # Phase 2: wait for reduces, compute updates, launch gathers
    gather_list: list[dict] = []
    for group, info in zip(self.param_groups, reduce_infos):
        if group['kind'] == 'adamw':
            self._compute_adamw(group, info, gather_list, rank, world_size)
        elif group['kind'] == 'muon':
            self._compute_muon(group, info, gather_list, rank)
        else:
            raise ValueError(f"Unknown optimizer kind: {group['kind']}")

    # Phase 3: wait for gathers, copy back
    self._finish_gathers(gather_list)
```

세 단계가 *분리되어 있다*. 각 단계의 역할은 이렇다.

**Phase 1 — reduce launch.** 모든 그룹에 대해 `reduce_scatter`(혹은 `all_reduce`)를 *async로 launch*한다. *기다리지 않는다*. 백그라운드로 돌게 두고 다음으로 넘어간다. PyTorch는 *NCCL 비동기 큐*를 가지고 있어서, *함수가 즉시 반환*되고 *실제 통신은 GPU에서 진행*된다.

**Phase 2 — wait + compute + gather launch.** 각 그룹마다 *한 번에 하나씩* 처리한다. 먼저 *해당 그룹의 future*를 wait. 그라디언트가 도착하면 *로컬 slice에 대해 update 계산*. 계산이 끝나면 *all_gather*를 또 async로 launch. 

*핵심은 overlap*이다. *한 그룹의 wait가 끝나면 곧장 다음 그룹의 wait로 가지 않고, 일단 update 계산을 한다*. 그 동안 *다음 그룹의 reduce는 계속 백그라운드에서 진행*된다. 그리고 *이 그룹의 all_gather가 백그라운드로 launch*된 다음에야 *다음 그룹의 wait*로 넘어간다. *계산과 통신이 겹쳐서 일어난다*. *idle time이 줄어든다*.

**Phase 3 — gather wait + copy back.** 모든 all_gather가 끝나길 기다린 뒤, *Muon 그룹*에 대해서는 stacked buffer에서 *원본 파라미터로 copy back*한다 (AdamW는 in-place 업데이트라 copy 필요 없음).

AdamW 그룹은 *크기에 따라 분기*한다 (`_reduce_adamw`, `optim.py:371-387`).

```python
if p.numel() < 1024:
    # Small params: all_reduce (no scatter/gather needed)
    future = dist.all_reduce(grad, op=dist.ReduceOp.AVG, async_op=True).get_future()
    param_infos[p] = dict(future=future, grad_slice=grad, is_small=True)
else:
    # Large params: reduce_scatter
    ...
```

*1024 elements보다 작으면* `all_reduce`. *스칼라*나 *작은 bias*는 어차피 *너무 작아서 scatter할 필요가 없다*. 모든 rank가 *전체*를 가지고 가는 게 *오히려 효율적*이다.

*크면* `reduce_scatter`. 그라디언트의 *1/N*만 각 rank가 받는다. *그 1/N에 대해서만* optimizer update를 계산. 그리고 `all_gather`로 *전체*를 다시 모은다. 옵티마이저 state도 *1/N만 저장*한다 — ZeRO-2의 본질.

Muon은 *항상 stacked + chunked*. 한 그룹의 K개 파라미터를 *world_size로 나눠* 각 rank가 *K/N개* 파라미터를 owned한다. *그 부분에 대해서만 Muon 계산*. 그리고 `all_gather`로 결과를 모음.

여기서 *padding* 처리가 등장한다 (`_reduce_muon`, `optim.py:389-408`).

```python
chunk_size = (len(params) + world_size - 1) // world_size
padded_num_params = chunk_size * world_size
...
stacked_grads = torch.empty(padded_num_params, *shape, dtype=dtype, device=device)
stacked_grads[:len(params)].copy_(grad_stack)
if len(params) < padded_num_params:
    stacked_grads[len(params):].zero_()
```

K가 world_size로 *나누어 떨어지지 않으면* — 예를 들어 19개 파라미터를 4 GPU에 나눠야 하면 — *0으로 패딩*해서 *20개로 만든다*. reduce_scatter가 *균등한 chunk size*를 요구하기 때문이다. *난감하지만* 어쩔 수 없다. 패딩된 부분은 *계산에서 무시*된다.

*Buffer 재사용*도 흥미롭다 (`optim.py:496-498`).

```python
# Reuse stacked_grads buffer for all_gather output
stacked_params = info["stacked_grads"]
future = dist.all_gather_into_tensor(stacked_params, updated_params, async_op=True).get_future()
```

`reduce_scatter`의 *입력 버퍼*를 `all_gather`의 *출력 버퍼*로 *그대로 재사용*한다. 둘이 같은 모양 `(padded_num_params, *shape)`이라서 *동시에 살아 있을 필요가 없다*. *메모리 절약*이 크다.

물론 *이 모든 게 PyTorch DDP를 직접 쓰면 한 줄로 끝난다*. 하지만 *교육용 코드*가 *목적이 아닌* nanochat에게는, *분산의 메커니즘을 코드로 드러내는* 게 더 중요하다. 그리고 *FSDP*를 쓰지 않고도 *ZeRO-2 동작*을 *530줄 정도*로 *완전히 구현*해 보였다는 게 — 이 책 *전체의 정신*과도 통하는 결정이다.

*기억해두자*. 분산 학습은 *복잡하지만 무서운 마법은 아니다*. *async ops*, *3-phase 구조*, *padding과 chunk*, *buffer 재사용*. 이 네 가지만 손에 익으면 *DDP나 FSDP 없이도* 자기 분산 옵티마이저를 짤 수 있다. *지금 당장 짜라는 뜻은 아니다*. 그저 *어디에 무엇이 있는지* 감각만 가져가자.

---

## 실습 — Newton-Schulz가 정말 SVD를 흉내내는가? [CPU 15분]

이론은 충분히 봤다. 이제 *직접* 확인해보자. Newton-Schulz iteration이 *정말로* `U V^T`에 수렴하는지, 매 iteration마다 SVD와의 거리가 얼마나 줄어드는지를.

준비물 — Python, NumPy, matplotlib. CPU로 충분하다. *15분*이면 된다.

```python
import numpy as np
import matplotlib.pyplot as plt

# 1024x1024 random matrix
np.random.seed(42)
G = np.random.randn(1024, 1024).astype(np.float32)

# 정답: SVD로 U·V^T 계산
U, S, Vt = np.linalg.svd(G, full_matrices=False)
target = U @ Vt  # 이것이 우리가 흉내내려는 직교 행렬

# Polar Express 계수 (optim.py에서 그대로 가져옴)
polar_express_coeffs = [
    (8.156554524902461, -22.48329292557795, 15.878769915207462),
    (4.042929935166739, -2.808917465908714, 0.5000178451051316),
    (3.8916678022926607, -2.772484153217685, 0.5060648178503393),
    (3.285753657755655, -2.3681294933425376, 0.46449024233003106),
    (2.3465413258596377, -1.7097828382687081, 0.42323551169305323),
]

# Newton-Schulz / Polar Express iteration
X = G / (np.linalg.norm(G, 'fro') * 1.01 + 1e-6)  # 정규화
distances = [np.linalg.norm(X - target, 'fro')]

print(f"Step 0: ‖X - U V^T‖_F = {distances[0]:.4f}")
for i, (a, b, c) in enumerate(polar_express_coeffs, 1):
    # X is wide(or square) here, so use X @ X.T branch
    A = X @ X.T
    B = b * A + c * (A @ A)
    X = a * X + B @ X
    dist = np.linalg.norm(X - target, 'fro')
    distances.append(dist)
    print(f"Step {i}: ‖X - U V^T‖_F = {dist:.4f}")

# 거리 곡선 plot
plt.figure(figsize=(8, 5))
plt.plot(distances, marker='o', linewidth=2)
plt.xlabel('Iteration')
plt.ylabel('‖X - U V^T‖_F (Frobenius distance)')
plt.title('Polar Express convergence to SVD U·V^T')
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.savefig('polar_express_convergence.png', dpi=100, bbox_inches='tight')
print("Saved plot to polar_express_convergence.png")
```

직접 돌려보자. CPU에서 *몇 초* 안에 끝난다. 

기대되는 출력은 대략 이렇다.

```
Step 0: ‖X - U V^T‖_F = 31.xxxx
Step 1: ‖X - U V^T‖_F = 11.xxxx
Step 2: ‖X - U V^T‖_F = 1.xxxx
Step 3: ‖X - U V^T‖_F = 0.0xxx
Step 4: ‖X - U V^T‖_F = 0.00xx
Step 5: ‖X - U V^T‖_F = 0.000x
```

(정확한 수치는 random seed와 정규화 방식에 따라 조금씩 다를 수 있다 — *경향성*만 확인하면 된다.)

*보이는가?* 거리가 *지수적으로 빠르게* 0으로 수렴한다. *5번만에* `U V^T`에 *거의 정확히* 일치한다. 첫 step의 큰 계수(a=8.15)가 *멀리 있던 X를 단숨에 1근처로 끌어당기고*, 그 다음 step들이 *세밀하게 미세조정*한다. *컨베이어 벨트 비유*가 *눈으로 보인다*.

*몇 가지 실험을 더 해보자*. *기억해두면 좋다*.

1. **계수를 *전부 같은 값*으로 바꿔보자.** 예를 들어 `(3.5, -3.0, 1.0)`을 5번 반복. 수렴이 *훨씬 느릴 것*이다. *Polar Express의 step-by-step optimized 계수*가 *왜 중요한지* 직접 보인다.

2. **`G`를 *극단적인 값*으로 만들어보자.** `G = np.random.randn(1024, 1024) * 100`. 정규화 단계 *없이* 점화식을 돌리면 — *발산*한다. *정규화가 왜 필수*인지 직접 본다.

3. **`tall matrix`로 바꿔보자.** `G = np.random.randn(2048, 1024)`. 그러면 `if g.size(-2) > g.size(-1)` 분기를 타야 한다. 코드를 `X.T @ X` 경로로 바꿔보자.

```python
# Tall matrix: X.T @ X 경로
for a, b, c in polar_express_coeffs:
    A = X.T @ X
    B = b * A + c * (A @ A)
    X = a * X + X @ B
```

*수학적으로 동치*인데 *연산량이 다르다*. (2048×1024)와 (1024×2048)의 곱 결과는 같지만, *더 작은 차원*에서 시작하면 *intermediate matrix*가 작아진다. *기억해두자*. *수학적으로 같아도 계산 순서*가 효율을 바꾼다.

이 실습 한 번이면 Newton-Schulz에 대한 *추상적 두려움*은 사라진다. *5번의 행렬 곱으로 SVD 흉내내기* — 손으로 만져본 사람만 *진짜로 안다*고 말할 수 있다.

---

## 마무리 — 옵티마이저는 준비됐다

다섯 절에 걸쳐 *옵티마이저의 안*을 다 들여다봤다. 처음에는 *난감했던* 두 옵티마이저의 동거가 — 어느덧 *명료한 분리*로 보인다.

요약하자면 이렇다.

- **AdamW** — 임베딩, lm_head, value_embeds, 그리고 모든 *스칼라/벡터* 파라미터에. 각 파라미터마다 독립적인 적응적 LR. *Sparse-friendly*. 30초 복습 끝.
- **Muon** — 트랜스포머 블록의 *2D 행렬*들에. momentum으로 모은 그라디언트를 *직교화*. *Newton-Schulz 점화식 한 줄*을 5번 반복. *35% 빠른 수렴*.
- **Polar Express** — Newton-Schulz의 *step-by-step optimized* 계수 변종. 같은 5번 반복으로 더 정확히 수렴.
- **NorMuon** — 직교화의 *잔여 불균형*을 factored second moment로 평탄화. *Per-neuron variance reduction*.
- **Cautious weight decay** — *update와 같은 부호*의 파라미터에만 WD 적용. 정규화와 그라디언트가 *싸우지 않게*.
- **`setup_optimizer`의 7개 param group** — 모델의 모든 파라미터를 *기능별로 분류*. *assert*로 누락 방지.
- **`dmodel_lr_scale`** — 모델 크기에 따라 AdamW LR을 *자동 보정*. `(model_dim/768)^-0.5`.
- **`@torch.compile` + 0-D CPU 텐서** — 매 step LR이 바뀌어도 *재컴파일 없이* 그래프 재사용.
- **`DistMuonAdamW`** — 3-phase async로 계산과 통신을 overlap. *PyTorch DDP 없이* ZeRO-2를 직접 구현.

*수식 한 줄 양보*도 약속대로 끝났다. Newton-Schulz 점화식 `X_{n+1} = a·X_n + b·X·X^T·X + c·(X·X^T)^2·X` — 한 줄. 그 한 줄이 Polar Express 계수의 *튜닝 대상*을 보여주고, NorMuon의 *잔여 불균형*을 가리키고, GPU에서 *왜 batched matmul로 빠른지*를 설명했다. *한 줄로 충분*했다.

*다음에 우리가 할 일*은? — 옵티마이저는 준비됐다. 토크나이저도 모델도 준비됐다. *이제 루프 안에서 모든 게 협업하는 걸 보자*.

6장은 *사전학습의 진짜 클라이맥스*다. `base_train.py` 한 파일에서 — 우리가 5장까지 *분리해서* 만들어온 부품들이 *한 그래프 위에서* 협력한다. 학습률은 cosine schedule을 그리고, Muon momentum은 0.85에서 0.97로 warmup되고, weight decay는 코사인으로 줄어들고, wandb 그래프에서 val_bpb는 *드디어 떨어지기 시작*한다.

차 한 잔, 하나 더 두고 6장으로 넘어가자.
