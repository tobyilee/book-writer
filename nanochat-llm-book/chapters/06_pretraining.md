# 6장. 사전학습, 드디어 loss가 떨어진다

5장의 마지막 페이지에서 우리는 `setup_optimizer`가 7개의 param group을 만들어내는 장면을 함께 봤다. 임베딩에는 AdamW, 매트릭스 파라미터에는 Muon — Newton-Schulz iteration이 SVD를 근사하는 그 단정한 다섯 줄짜리 점화식까지. 그 화면을 닫고 잠깐 숨을 골랐다면, 이제 그 옵티마이저를 *진짜로 굴려볼* 차례다.

여기까지 우리가 손에 쥔 것들을 한 번 세어보자. 2장에서 32K vocab의 한국어 토큰 분포를 봤다. 3장에서 `token_bytes.pt`를 디스크에 저장했다. 4A장에서 `GPTConfig`의 한 줄로 모델의 *모양*을 결정짓는 법을 알았고, 4B장에서는 value embeddings·smear·backout 같은 7개 트릭이 어떤 모양으로 forward에 끼어드는지 손으로 만져봤다. 5장에서는 `MuonAdamW`가 어떻게 작동하는지, Polar Express의 quintic coefficient가 왜 그 다섯 줄에 박혀 있는지 *읽었다*.

그런데 *읽기*만 해서는 모르는 게 한 가지 있다. 이 모든 조각이 *한 루프 안에서 동시에 굴러갈 때* 정확히 어떤 일이 벌어지는가. wandb 페이지를 켜고 그래프를 들여다보면 무엇이 보이는가. `val_bpb`가 1.0에서 0.745로 떨어지는 그 곡선의 *모양*은 어떻게 생겼는가. 학습이 발산하기 직전, 화면에서 어떤 신호가 먼저 떠오르는가.

이 모든 질문에 대한 답이 한 파일에 들어 있다 — `scripts/base_train.py`, 총 631줄. 그 한 파일이 어떻게 우리가 5장까지 준비한 모든 것을 *오케스트레이션*하는지, 그리고 그 결과로 무엇이 디스크와 wandb에 남는지를 함께 따라가보자.

이번 장의 정서는 *돌파*다. 토비의 문체로 *드디어*가 자연스럽게 나오는 챕터다. 내가 만든 토크나이저, 내가 읽은 GPT 모듈, 내가 이해한 Muon이 *한 그래프 위에서* 협력하는 장면을 — 가능한 한 손에 잡히게 — 그려보자.

## base_train.py를 한 페이지로 펴면

`base_train.py`의 큰 그림부터 한눈에 잡아보자. 631줄을 다 외울 필요는 없다. 다만 *어떤 단계가 어떤 순서로 일어나는지*를 한 번 머릿속에 박아두면, 이 챕터의 나머지가 한결 가볍게 읽힌다.

```
1. argparse 파싱 + 환경 변수 (expandable_segments)
2. compute_init → device, DDP, COMPUTE_DTYPE 출력
3. tokenizer 로드 + token_bytes 로드
4. build_model_meta → meta device init → to_empty → init_weights
5. (선택) FP8 변환
6. torch.compile(model, dynamic=False)
7. Scaling laws → target_tokens · batch_size · LR scale · WD scale 결정
8. dataloader 초기화 + 첫 batch prefetch
9. LR / Muon momentum / WD 스케줄러 함수 정의
10. while True 루프:
     - eval (val_bpb, CORE)
     - sample (7개 프롬프트)
     - save_checkpoint
     - grad_accum_steps × (forward → backward → next batch)
     - optimizer.step + zero_grad
     - wandb log
     - gc.freeze 트릭 (첫 step 후 한 번)
```

11단계처럼 보이지만, 사실은 *세 덩어리*다. **첫째**, 컴퓨트 환경을 묻고 답하는 단계(1~3). **둘째**, 모델과 옵티마이저를 *준비*하는 단계(4~7). **셋째**, 데이터를 흘려보내며 *루프*를 도는 단계(8~10).

이 세 덩어리는 각각 *질문 하나*에 답한다. 첫째 덩어리는 *"우리는 어떤 하드웨어 위에 서 있는가?"*에 답한다. 둘째 덩어리는 *"이 하드웨어에 맞춘 학습 레시피는 무엇인가?"*에 답한다. 셋째 덩어리는 *"그 레시피로 정말 loss가 떨어지는가?"*에 답한다.

흥미로운 건, 이 세 질문의 답이 *모두 자동화*되어 있다는 점이다. 사용자가 직접 결정해야 하는 건 단 하나 — `--depth`다. 나머지는 코드가 *자신을 둘러싼 환경을 보고* 알아서 결정한다. 카르파시의 nanochat이 *"한 다이얼만 돌리면 된다"*고 자랑하는 그 다이얼이 정확히 이 자동화의 결과다.

### "expandable_segments=True"라는 첫 줄

`base_train.py`의 가장 위로 올라가 보자. import 문도 시작하기 전, 14~15번째 줄에 한 줄짜리 마법이 있다.

```python
# scripts/base_train.py:14-16
import os
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
import gc
```

별 게 아닌 한 줄 같지만, 이건 PyTorch CUDA caching allocator의 동작을 *바꾸는* 환경변수다. 기본 allocator는 한 번 잡은 메모리 블록을 다른 크기로 쓸 수 없다 — fragmentation이 쌓이면 같은 VRAM 안에서 큰 텐서가 안 들어가는 *난감한* 상황이 생긴다. `expandable_segments=True`는 allocator가 *큰 가상 주소 공간*을 미리 예약해두고 실제 메모리는 필요할 때만 매핑하게 해준다.

이게 왜 첫 줄에 박혀 있는가? *환경변수는 PyTorch가 import되는 순간 한 번만 읽힌다*. `import torch` 뒤에 설정하면 늦다. 그래서 *모든 import보다 먼저* 박아둔다. 작은 디테일이지만, 학습 도중 OOM이 나서 모든 게 무너지는 걸 한 번이라도 겪어본 사람이라면 이 한 줄의 무게를 안다.

### argparse 한 페이지

다음으로 argparse 영역을 보자. 58~80번째 줄 사이에 학습의 모든 하이퍼파라미터가 *기본값과 함께* 정의돼 있다.

```python
# scripts/base_train.py:58-68
parser.add_argument("--target-param-data-ratio", type=float, default=12,
                    help="calculate num_iterations to maintain data:param ratio (Chinchilla=20, -1 = disable)")
parser.add_argument("--device-batch-size", type=int, default=32, ...)
parser.add_argument("--total-batch-size", type=int, default=-1,
                    help="total batch size in tokens. ... (-1 = auto-compute optimal)")
parser.add_argument("--embedding-lr", type=float, default=0.3, ...)
parser.add_argument("--unembedding-lr", type=float, default=0.008, ...)
parser.add_argument("--weight-decay", type=float, default=0.28, ...)
parser.add_argument("--matrix-lr", type=float, default=0.02, ...)
parser.add_argument("--scalar-lr", type=float, default=0.5, ...)
parser.add_argument("--warmup-steps", type=int, default=40, ...)
parser.add_argument("--warmdown-ratio", type=float, default=0.65, ...)
parser.add_argument("--final-lr-frac", type=float, default=0.05, ...)
```

여기서 눈에 띄는 게 두 가지다. 첫째, `--target-param-data-ratio`의 기본값이 *12*다. Chinchilla 논문의 정설인 *20*보다 작다. 이건 카르파시가 *경험적으로* 보정한 값이다 — Muon이 AdamW보다 효율적이라서, 같은 토큰 수로 더 큰 모델을 학습할 수 있다는 직관이 깔려 있다. speedrun에서는 이 값을 더 낮춰 *8*로 쓴다.

둘째, `--total-batch-size`의 기본값이 *-1*이다. 다른 값이 *-1*이면 "꺼라"는 뜻인데, 여기서는 "*자동 계산해라*"라는 뜻이다. 이 자동 계산이 곧 우리가 한 박스 뒤에서 펴볼 *공식 셋*이 하는 일이다.

argparse의 모든 항목에 *명시적인 기본값*이 박혀 있다는 것. 그리고 그 기본값들이 *함께 굴러갈 때 의미가 생기게* 튜닝되어 있다는 것. 이게 nanochat이 "한 다이얼만 돌려도 된다"고 자신하는 이유다. 우리는 그 한 다이얼(`--depth`)을 돌리면서, 코드가 *다른 모든 다이얼을 어떻게 자동으로 조정하는지* 옆에서 지켜보면 된다.

## 컴퓨트 환경의 단일 진실 — common.py

자동화된 학습 레시피의 첫 단계는 *우리가 어떤 하드웨어 위에 서 있는지*를 묻는 것이다. H100인가 A100인가, 아니면 노트북의 M3 Max인가. bf16을 쓸 수 있는가, fp16밖에 못 쓰는가. 분산 학습인가 단일 노드인가.

이 모든 질문에 *한 곳*에서 답하는 모듈이 있다. `nanochat/common.py`다. 이 파일이 *컴퓨트 환경에 대한 단일 진실(single source of truth)*이다.

### COMPUTE_DTYPE — 자동 분기의 시작점

`common.py`의 17~31줄을 펴자.

```python
# nanochat/common.py:17-31
_DTYPE_MAP = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}
def _detect_compute_dtype():
    env = os.environ.get("NANOCHAT_DTYPE")
    if env is not None:
        return _DTYPE_MAP[env], f"set via NANOCHAT_DTYPE={env}"
    if torch.cuda.is_available():
        capability = torch.cuda.get_device_capability()
        if capability >= (8, 0):
            return torch.bfloat16, f"auto-detected: CUDA SM {capability[0]}{capability[1]} (bf16 supported)"
        return torch.float32, f"auto-detected: CUDA SM {capability[0]}{capability[1]} (pre-Ampere, bf16 not supported, using fp32)"
    return torch.float32, "auto-detected: no CUDA (CPU/MPS)"
COMPUTE_DTYPE, COMPUTE_DTYPE_REASON = _detect_compute_dtype()
```

겨우 15줄이지만, 이 함수가 *모든 모듈*의 dtype 결정에 영향을 미친다. 우선순위는 명확하다 — `NANOCHAT_DTYPE` 환경변수가 있으면 그것을, 없으면 GPU compute capability를 보고 결정. SM 8.0 이상(Ampere A100, Hopper H100)이면 bf16, 그 이하(V100, T4 같은 옛 GPU)면 fp32. CUDA가 아예 없으면 (M3 Max의 MPS, 그냥 CPU) fp32로 간다.

`COMPUTE_DTYPE`은 *전역 상수*다. `import`되는 순간 한 번 결정되고, 다른 모듈들이 이 상수를 *읽어서* 자기 동작을 바꾼다. 예를 들어 4A장에서 본 `Linear` 커스텀 클래스의 forward 캐스팅, 5장의 `adamw_step_fused`의 master fp32 + compute dtype 분리, 그리고 6장에서 곧 볼 FP8 학습의 evaluation fallback — 이 모든 곳이 `COMPUTE_DTYPE`을 *참조*한다.

흥미로운 디테일 한 가지. bf16이 아니면 SDPA fallback이 강제된다는 건 4B장에서 얘기했다. 그래서 `base_train.py`의 `:114-117`에는 다음과 같은 *친절한 경고*가 박혀 있다.

```python
# scripts/base_train.py:114-117
if args.window_pattern != "L":
    print0(f"WARNING: SDPA has no support for sliding window attention "
           f"(window_pattern='{args.window_pattern}'). Your GPU utilization will be terrible.")
    print0("WARNING: Recommend using --window-pattern L for full context attention "
           "without alternating sliding window patterns.")
```

*"GPU utilization will be terrible."* — 영어가 약간 거칠지만, 이 한 줄 경고가 *수많은 사용자가 노트북에서 sliding window를 시도하다 좌절하는 미래*를 미리 막는다. CPU/MPS 환경에서는 `--window-pattern=L`을 쓰는 편이 낫다는 것. 이 책의 후반부 실습에서 `runcpu.sh`가 `--window-pattern=L`을 박아두는 건 같은 이유다.

### get_dist_info와 compute_init — DDP 분기

다음으로 분산 학습 설정을 보자. `common.py:150-208`까지가 분산 setup의 한 페이지다.

```python
# nanochat/common.py:150-160
def get_dist_info():
    if is_ddp_requested():
        assert all(var in os.environ for var in ['RANK', 'LOCAL_RANK', 'WORLD_SIZE'])
        ddp_rank = int(os.environ['RANK'])
        ddp_local_rank = int(os.environ['LOCAL_RANK'])
        ddp_world_size = int(os.environ['WORLD_SIZE'])
        return True, ddp_rank, ddp_local_rank, ddp_world_size
    else:
        return False, 0, 0, 1
```

`torchrun --nproc_per_node=8`으로 띄우면 토치런이 자동으로 `RANK`, `LOCAL_RANK`, `WORLD_SIZE`를 환경변수로 박아준다. 그 환경변수가 있으면 DDP 모드, 없으면 단일 프로세스 모드. 깔끔하다.

그 다음 `compute_init`이 *디바이스를 정한다*.

```python
# nanochat/common.py:173-208 (요약)
def compute_init(device_type="cuda"):
    torch.manual_seed(42)
    if device_type == "cuda":
        torch.set_float32_matmul_precision("high")  # TF32 matmul
    is_ddp_requested, ddp_rank, ddp_local_rank, ddp_world_size = get_dist_info()
    if is_ddp_requested and device_type == "cuda":
        device = torch.device("cuda", ddp_local_rank)
        torch.cuda.set_device(device)
        dist.init_process_group(backend="nccl", device_id=device)
        dist.barrier()
    else:
        device = torch.device(device_type)
    return is_ddp_requested, ddp_rank, ddp_local_rank, ddp_world_size, device
```

CUDA + DDP면 NCCL backend로 프로세스 그룹 init. 단일 노드면 그냥 `device = torch.device("cuda")` 또는 `torch.device("mps")` 또는 `torch.device("cpu")`. 모든 경우에서 *같은 함수가 같은 시그니처로 다섯 개를 리턴*한다. 그래서 `base_train.py`의 어느 줄을 봐도 `ddp_rank == 0`처럼 깔끔한 조건을 쓸 수 있다.

생각해보자. 만약 이 함수가 없었다면, `base_train.py`의 매 줄마다 *"지금 분산이야 단일이야?"*를 따져야 했을 것이다. 그건 *끔찍한 일이다*. 환경 분기를 *한 곳에 집중*시키는 게 *컴퓨트 환경의 단일 진실*이라는 표현의 진짜 의미다.

### get_peak_flops — MFU의 분모

마지막으로 한 가지 흥미로운 함수가 더 있다. `get_peak_flops(device_name)` — 학습 중 wandb에서 보게 될 *MFU(Model FLOPs Utilization)* 지표의 *분모*를 제공하는 함수다.

```python
# nanochat/common.py:227-267 (요약)
def get_peak_flops(device_name: str) -> float:
    name = device_name.lower()
    _PEAK_FLOPS_TABLE = (
        (["gb200"], 2.5e15),
        (["b200"], 2.25e15),
        (["h200"], 989e12),
        (["h100", "nvl"], 835e12),
        (["h100", "pcie"], 756e12),
        (["h100"], 989e12),
        (["a100"], 312e12),
        (["mi300x"], 1.3074e15),
        (["4090"], 165.2e12),
        (["3090"], 71e12),
        ...
    )
    for patterns, flops in _PEAK_FLOPS_TABLE:
        if all(p in name for p in patterns):
            return flops
    logger.warning(f"Peak flops undefined for: {device_name}, MFU will show as 0%")
    return float('inf')
```

이 함수는 *하드코딩된 룩업 테이블*이다. H100 SXM은 BF16 peak 989 TFLOPS, A100은 312 TFLOPS, RTX 4090은 165 TFLOPS, 옛 3090은 71 TFLOPS. 이 숫자가 *분모*로 들어가서, 실제 학습 중 측정된 `flops_per_sec`를 이 peak로 나눈 게 MFU다. H100에서 MFU 50%가 나온다는 건 *peak의 절반인 ~495 TFLOPS로 굴리고 있다*는 뜻이다.

테이블에 없는 GPU(예를 들어 우리 손에 익숙하지 않은 클라우드 인스턴스의 변종)면 `float('inf')`를 리턴해서 MFU가 0%로 표시된다. *틀린 추측을 하지 않는다*는 게 이 함수의 디자인 철학이다. "잘못된 MFU 30%"보다 "MFU 0% (모르는 GPU)"가 *덜 거짓말*이라는 입장.

세 가지 함수 — `_detect_compute_dtype`, `get_dist_info`, `get_peak_flops` — 가 모여 *컴퓨트 환경의 단일 진실*을 만든다. 같은 코드가 H100에서, A100에서, MPS에서, CPU에서 *다르게 굴러가게* 하는 *코드적 답*이 여기 있다.

## 공식 셋, 한눈에 — Scaling Laws의 자동 적용

이제 본격적인 자동화로 들어가보자. `base_train.py:263-316`의 50줄 남짓이 nanochat의 *지능*이 가장 두드러지는 영역이다. 이 짧은 영역에서 세 가지 공식이 *깔끔하게* 협업해서 `num_iterations`, `total_batch_size`, `learning_rate_scale`, `weight_decay_scale` 네 값을 동시에 결정한다.

> ### 공식 셋, 한눈에
>
> nanochat의 사전학습이 `--depth` 한 다이얼만으로 굴러갈 수 있는 건 다음 세 공식이 동시에 작동하기 때문이다. 본문에서는 이 셋이 *어떤 그래프로 보이는지*만 따라가자.
>
> **1. 데이터 :파라미터 비율 (Chinchilla 보정)**
>
> ```
> target_tokens = target_param_data_ratio × num_scaling_params
> ```
>
> 정설인 Chinchilla(20:1)보다 작은 **12:1** (nanochat default), speedrun은 **8:1**. Muon이 AdamW보다 효율적이라는 경험적 보정. `num_scaling_params`는 transformer matrices + lm_head (embedding은 제외 — Kaplan 스타일과 Chinchilla 스타일의 절충).
>
> **2. 최적 배치 사이즈 — Power Lines 논문**
>
> ```
> predicted_batch_size = B_REF × (target_tokens / D_REF)^0.383
> ```
>
> 출처: [arXiv 2505.13738](https://arxiv.org/abs/2505.13738). `B_REF = 2^19 = 524,288` 토큰 (d12 기준), `D_REF`는 d12의 compute-optimal 토큰 수. 효과: d12 → d24로 토큰 수가 늘면 batch도 `2^0.383 ≈ 1.3배` 커진다.
>
> **3. Weight Decay 스케일링 — T_epoch 프레임워크**
>
> ```
> λ = λ_ref × √(B/B_ref) × (D_ref/D)
> ```
>
> 출처: [arXiv 2405.13698](https://arxiv.org/abs/2405.13698). 핵심 직관: *T_epoch = B/(η·λ·D)* 가 일정하게 유지되어야 한다. LR 스케일링이 `η ∝ √(B/B_ref)`니까, weight decay는 `√(B/B_ref) × (D_ref/D)`로 자동 보정.

세 공식의 코드 구현을 직접 보면 더 잘 보인다.

```python
# scripts/base_train.py:268-302 (요약)
num_scaling_params = get_scaling_params(model)
target_tokens = int(args.target_param_data_ratio * num_scaling_params)

# Reference: d12
d12_ref = build_model_meta(12)
D_REF = args.target_param_data_ratio * get_scaling_params(d12_ref)
B_REF = 2**19  # 524,288 tokens

# 2) Optimal batch size (Power Lines)
if total_batch_size == -1:
    batch_size_ratio = target_tokens / D_REF
    predicted_batch_size = B_REF * batch_size_ratio ** 0.383
    total_batch_size = 2 ** round(math.log2(predicted_batch_size))

# 3) LR scaling (η ∝ √(B/B_ref))
batch_lr_scale = (total_batch_size / B_REF) ** 0.5

# 4) Weight decay scaling (T_epoch framework)
weight_decay_scaled = args.weight_decay * math.sqrt(total_batch_size / B_REF) * (D_REF / target_tokens)
```

코드를 펴 놓고 보면 *그렇게 복잡하지 않다*. 35줄 안에 끝난다. 그런데 이 짧은 코드가 *깊이 d6의 노트북 모델*과 *깊이 d24의 8XH100 모델*에 모두 *정확히 들어맞는* 하이퍼파라미터를 만들어낸다.

생각해보자. 이게 없다면 어떤 일이 벌어지는가. 우리가 d12로 잘 굴러가던 학습 스크립트를 d24로 *그냥 옮기면* — batch size가 너무 작아서 GPU가 놀거나, LR이 너무 작아서 학습이 안 진행되거나, weight decay가 너무 강해서 모델이 과대 정규화되거나. 이 세 가지 *난감한 상황*이 동시에 터진다.

세 공식이 *함께* 굴러가니까 그런 일이 안 난다. 한 다이얼만 돌려도 다른 모든 다이얼이 *서로 보정하면서* 따라온다. 이게 nanochat의 자동화가 *가짜 자동화*가 아닌 이유다.

### 그래프 위에서는 어떻게 보이는가

세 공식의 결과는 wandb 한 페이지에서 *세 곡선의 모양*으로 나타난다.

**`target_tokens` 곡선:** depth를 d12 → d24로 두 배 키우면, target_tokens는 약 *4배* 커진다 (모델 파라미터가 ~4배 늘기 때문). 학습 시간도 그대로 4배 늘어난다. wandb의 `total_training_time` 축이 그걸 보여준다.

**`total_batch_size` 곡선:** target_tokens가 4배 커지면 batch는 `4^0.383 ≈ 1.74배` 커진다. depth가 두 배가 되면 batch도 거의 두 배. wandb의 `train/tok_per_sec`이 *눈에 띄게* 늘어나는 게 이 효과다.

**`weight_decay_scaled` 곡선:** batch가 1.74배 커지면 √보정으로 1.32배, D 보정으로 1/4배, 합쳐서 **0.33배**. 즉 *weight decay가 더 약해진다*. 큰 모델은 *덜 정규화해도 된다*는 직관과 맞는다.

wandb에서 *step* 축이 아니라 *flops* 축으로 곡선을 보면 더 흥미롭다. 같은 flops를 쓴 d6와 d24가 *어떻게 다른 val_bpb*에 도달하는지 비교할 수 있다. 카르파시가 `runs/scaling_laws.sh`를 따로 둔 이유가 여기에 있다 — scaling law의 *경험적 검증*이 코드 안에 들어가 있다.

## BOS-aligned bestfit-crop — 35%를 *버리는* 결정

이제 데이터 흐름으로 내려가보자. 모델과 옵티마이저가 준비됐다 해도, 데이터가 어떻게 흘러들어가느냐에 따라 학습의 품질이 *완전히 달라진다*.

옛 dataloader는 *토큰을 한 톨도 안 버렸다*. 문서를 토크나이즈해서 한 줄로 길게 이어 붙이고, 학습 시퀀스 길이(2048)만큼씩 잘라 썼다. 메모리 효율은 100%였지만, *한 시퀀스 안에 여러 문서가 끊긴 채 섞여*서 모델이 *문맥 혼란*을 겪었다. *"이전 문장이 다른 문서의 문장이라는 걸 모델은 모른다"*는 거다.

nanochat은 이 문제를 *데이터 35%를 *버리는* 대신* 한 시퀀스 = 한 BOS로 시작하는 깨끗한 문서 묶음으로 해결했다. `dataloader.py:1-17`에 그 trade-off 주석이 그대로 박혀 있다.

```python
# nanochat/dataloader.py:1-17
"""
Distributed dataloaders for pretraining.

BOS-aligned bestfit:
   - Every row starts with BOS token
   - Documents packed using best-fit algorithm to minimize cropping
   - When no document fits remaining space, crops a document to fill exactly
   - 100% utilization (no padding), ~35% tokens cropped at T=2048

Compared to the original tokenizing_distributed_data_loader:
BOS-aligned loses ~35% of tokens to cropping, but ensures that
there are fewer "confusing" tokens in the train/val batches as every token can
now attend back to the BOS token and sees the full context of the document.
"""
```

*"~35% tokens cropped at T=2048"* — *35%를 *버린다*는 결정의 무게*를 코드 주석에 그대로 박아둔 솔직함이 인상적이다. 데이터를 한 톨이라도 더 짜내고 싶은 본능을 *명시적으로* 거스르는 결정이다.

왜 이게 더 나은가? 직관적으로 한 번 풀어보자. attention은 *시퀀스 안의 모든 위치*를 본다. 한 시퀀스에 *위키피디아 한 단락 + 뉴스 한 단락 + 코드 한 토막*이 끊긴 채 섞여 있다고 해보자. 모델은 "다음 토큰을 예측하려면 어디까지를 문맥으로 봐야 하는가?"를 *추측해야 한다*. 학습 신호의 일부가 *문서 경계가 어디인지*를 알아내는 데 쓰여버린다.

반면 BOS-aligned면 *모든 시퀀스가 BOS로 시작*한다. 모델은 `attend back to the BOS token`만 하면 된다. 모든 토큰이 *깨끗한 문맥*에서 학습된다. 그래서 같은 step 수로도 *더 빨리 수렴*한다.

### Best-fit 알고리즘 — 짧은 코드의 영리함

`bestfit` 부분의 핵심은 한 페이지 안에 들어간다. `dataloader.py:74-162`를 펴자.

```python
# nanochat/dataloader.py:122-151 (요약)
while True:
    for row_idx in range(B):
        pos = 0
        while pos < row_capacity:
            # Ensure buffer has documents
            while len(doc_buffer) < buffer_size:
                refill_buffer()

            remaining = row_capacity - pos

            # Find largest doc that fits entirely
            best_idx = -1
            best_len = 0
            for i, doc in enumerate(doc_buffer):
                doc_len = len(doc)
                if doc_len <= remaining and doc_len > best_len:
                    best_idx = i
                    best_len = doc_len

            if best_idx >= 0:
                doc = doc_buffer.pop(best_idx)
                doc_len = len(doc)
                row_buffer[row_idx, pos:pos + doc_len] = torch.tensor(doc, dtype=torch.long)
                pos += doc_len
            else:
                # No doc fits - crop shortest in buffer to fill remaining
                shortest_idx = min(range(len(doc_buffer)), key=lambda i: len(doc_buffer[i]))
                doc = doc_buffer.pop(shortest_idx)
                row_buffer[row_idx, pos:pos + remaining] = torch.tensor(doc[:remaining], dtype=torch.long)
                pos += remaining
```

알고리즘 자체는 *교과서적인 best-fit packing*이다. 버퍼에서 *남은 자리에 들어가는 가장 큰 문서*를 찾아 채워 넣고, 더 안 들어가면 *가장 짧은 문서*를 *정확히 잘라* 빈자리를 메운다. 결과적으로 시퀀스 길이 `T+1 = 2049`이 *padding 없이* 100% 채워진다 (다만 마지막 문서는 잘렸으니 *crop된 토큰들은 학습에서 버려진다*).

조금 더 들여다보면 흥미로운 디테일이 있다. 한 시퀀스에 *여러 문서*가 들어갈 수 있다 (한 문서가 짧으면). 그래도 *모든 문서는 BOS로 시작*한다 (`refill_buffer`에서 `tokenizer.encode(doc_batch, prepend=bos_token, ...)`가 그 일을 한다). 그래서 한 시퀀스 안에 BOS가 여러 번 나타나기도 한다 — 이건 *의도된* 거다. 모델은 BOS를 *문서 경계의 명시적 신호*로 학습한다.

또 하나의 디테일. `cpu_buffer = torch.empty(2 * B * T, dtype=torch.long, pin_memory=use_cuda)` — *pinned CPU 버퍼*를 미리 잡아둔다. CUDA로 데이터를 보낼 때 pinned 메모리에서 보내면 *한 번의 HtoD copy*로 끝난다. 안 그러면 PyTorch가 *내부적으로 staging*을 하느라 한 단계가 더 들어간다. 작은 디테일이지만, 학습 step의 50ms를 줄이는 영리함이다.

### Resume의 깨끗한 디자인

`dataloader_state_dict = {"pq_idx": pq_idx, "rg_idx": rg_idx, "epoch": epoch}` — 매 yield마다 *현재 위치*를 dictionary로 함께 리턴한다. 학습이 중간에 끊겼다 재개될 때 이 상태를 *그대로 넣어주면* 같은 위치에서 다시 시작한다.

체크포인트가 저장될 때 이 state도 함께 저장된다 (`base_train.py:491`의 `"dataloader_state_dict": dataloader_state_dict`). 재개할 때는 `load_checkpoint`로 받아서 dataloader 생성자에 넣어준다. *Resume이 깨끗하게 닫힌 디자인*이다. 학습이 끊겼다 다시 도는 거대한 실험에서 *데이터를 재방문 vs 누락*하는 그 *찜찜한 어긋남*이 안 생긴다.

데이터를 35% 버리는 *대담함*과 resume을 깨끗하게 처리하는 *세심함*이 한 파일에 공존한다. 카르파시의 코드 미학이다.

## LR schedule — warmup, constant, warmdown의 세 구간

이제 학습 루프의 스케줄러로 가보자. 사전학습의 LR 스케줄은 *세 구간*으로 나뉜다.

```python
# scripts/base_train.py:360-369
def get_lr_multiplier(it):
    warmup_iters = args.warmup_steps              # default 40
    warmdown_iters = round(args.warmdown_ratio * num_iterations)  # default 0.65 × N
    if it < warmup_iters:
        return (it + 1) / warmup_iters
    elif it <= num_iterations - warmdown_iters:
        return 1.0
    else:
        progress = (num_iterations - it) / warmdown_iters
        return progress * 1.0 + (1 - progress) * args.final_lr_frac  # to 0.05
```

세 구간이 어떻게 생겼는지 *시각적으로* 그려보자. 가로축이 step, 세로축이 LR multiplier (0~1)이라 했을 때:

```
LR mult ↑
  1.0     ___________________________  
         /                            \
         |                             \
         |                              \
         |                               \
         |                                \
  0.05   |                                 \___
         |________________________________________
         0   40                              N
            warmup       constant       warmdown
```

40 step 동안 0에서 1까지 선형 워밍업, 그 뒤 *대부분의 학습 기간*은 LR=1.0로 평지, 마지막 65% 구간(warmdown_ratio=0.65)에서 0.05까지 *천천히 내려간다*. 

세 구간이 각각 어떤 역할을 하는지 잠깐 생각해보자. **Warmup**은 *초기 폭주를 막는다*. 모델의 초기 weight 분포가 안정되지 않은 상태에서 큰 LR로 때리면 loss가 발산한다. 40 step이라는 짧은 워밍업으로 충분한 건, init_weights에서 임베딩 std=0.8, lm_head std=0.001처럼 *이미 안정적인 초기화*가 깔려 있기 때문이다 (4A장 참조).

**Constant** 구간이 *대부분의 학습*을 차지한다. 35% 정도 — 학습 시간의 1/3가량. 이 구간에서 *진짜 학습*이 일어난다. wandb의 `train/loss` 곡선이 가장 *가파르게* 떨어지는 영역이다.

**Warmdown**은 *수렴을 안정시킨다*. LR을 천천히 낮추면서 모델이 더 *날카로운 최저점*에 안착하게 한다. 흥미롭게도 nanochat은 *cosine decay*가 아니라 *linear decay*를 쓴다. 카르파시의 modded-nanoGPT에서 가져온 선택이다 — linear가 wandb 그래프에서 *더 깨끗한 직선*으로 보이고, 실험 결과로도 큰 차이가 없다는 입장.

### 왜 final_lr_frac이 *0*이 아니고 *0.05*인가

마지막에 LR이 0이 아니라 0.05까지만 내려간다. 이 디테일이 한 가지를 가능하게 한다 — *SFT 단계에서 base 모델의 학습을 *이어서* 진행*하는 것. SFT의 `init_lr_frac=0.8`은 base 학습 끝의 LR(0.05)이 너무 작아서, SFT 시작 시점에 LR을 *다시 키운다*. 0이었다면 *영원히 0*에서 시작해야 했을 거다. 0.05라는 *작지만 0은 아닌 값*이 base → SFT 전환의 *부드러운 다리*가 된다.

## Muon momentum schedule — 0.85→0.97→0.90

Muon에는 LR뿐 아니라 *momentum 스케줄*도 따로 있다. 5장에서 Muon의 *Nesterov momentum*이 gradient를 *모아두는 메모리*라고 했다. 이 메모리의 *기억 강도*를 학습 단계에 따라 조절한다.

```python
# scripts/base_train.py:372-382
def get_muon_momentum(it):
    warmdown_iters = round(args.warmdown_ratio * num_iterations)
    warmdown_start = num_iterations - warmdown_iters
    if it < 400:
        frac = it / 400
        return (1 - frac) * 0.85 + frac * 0.97
    elif it >= warmdown_start:
        progress = (it - warmdown_start) / warmdown_iters
        return 0.97 * (1 - progress) + 0.90 * progress
    else:
        return 0.97
```

세 구간으로 갈리는 게 LR 스케줄과 비슷하지만, *값*이 다르다.

```
momentum ↑
  0.97    __________________________
         /                          \
         |                           \
  0.90   |                            \____
         |
  0.85   /
         |____________________________________
         0      400              warmdown    N
```

**0~400 step**: 0.85에서 0.97까지 *키운다*. 초반에는 gradient가 들쭉날쭉하니까 *덜 기억*하는 게 안전하다. 학습이 안정될수록 *더 기억*해도 된다.

**400 step 이후 ~ warmdown 시작**: 0.97 평지. 학습의 본격적인 구간.

**Warmdown 동안**: 0.97에서 0.90까지 *내린다*. LR이 줄어드는 동안 momentum도 *살짝 약하게* 만들어서, 끝물에 모델이 *너무 한 방향으로만 밀려가는 걸* 막는다.

이 스케줄이 *왜* 이 값들로 튜닝됐는지의 *완전한 이유*는 사실 누구도 모른다. modded-nanoGPT 커뮤니티의 *수많은 sweep 결과*가 모여 만들어진 값이다. 카르파시도 [#481 leaderboard](https://github.com/karpathy/nanochat/discussions/481)에서 *"hyperparameter sweep (320개 실험)"*을 언급한다. *경험적으로 잘 굴러가는 값*이지, *수학적으로 도출된 값*은 아니다.

기억해두자. 이런 *마법 같은 숫자*가 코드에 박혀 있을 때, 거기엔 *수많은 실험의 무게*가 들어가 있다. 우리가 그 숫자를 그냥 *받아들이는* 것은 *순응*이 아니라 *공동체에 대한 신뢰*다.

## FP8 training — torchao 대비 단순한 ~150줄

이제 학습을 *더 빠르게* 만드는 트릭으로 가보자. **FP8 training**이다. 5장에서 우리는 `Linear`가 fp32 master + bf16 compute로 굴러간다는 걸 봤다. FP8은 한 단계 더 내려간다 — *matmul만 fp8*로, weight 자체는 fp32 유지.

### 왜 *직접 구현*했는가

PyTorch 생태계에는 이미 `torchao.float8`이라는 *2000줄짜리* 라이브러리가 있다. tensor subclass·계층적 설정·여러 scaling recipe — 모든 걸 다 지원한다. 그런데 카르파시는 *이걸 그대로 쓰는 대신* 한 파일에 ~150줄로 *다시 짰다*.

이유는 `nanochat/fp8.py`의 docstring(43~69줄)에 길게 적혀 있다. *교육적 명료성*. 2000줄짜리 라이브러리는 *블랙박스*다. 학습자가 "FP8이 정확히 *어디서* 일어나는가"를 *손가락으로 짚을 수* 없다. 반면 150줄짜리 자체 구현은 *한 페이지에 모든 게 보인다*. nanochat의 정체성과 맞는 결정이다.

핵심 함수 두 개를 펴 보자.

```python
# nanochat/fp8.py:82-107
@torch.no_grad()
def _to_fp8(x, fp8_dtype):
    """Dynamically quantize a tensor to FP8 using tensorwise scaling."""
    fp8_max = torch.finfo(fp8_dtype).max
    amax = x.float().abs().max()
    scale = fp8_max / amax.double().clamp(min=EPS)
    scale = scale.float()
    x_scaled = x.float() * scale
    x_clamped = x_scaled.clamp(-fp8_max, fp8_max)
    x_fp8 = x_clamped.to(fp8_dtype)
    inv_scale = scale.reciprocal()
    return x_fp8, inv_scale
```

26줄이지만 *모든 게 보인다*. FP8 dtype의 max 값을 가져온다 (E4M3는 448, E5M2는 57344). 텐서의 absolute max를 구한다. `scale = fp8_max / amax`로 *전체 텐서를 FP8 범위로 매핑*하는 scale 하나를 구한다. 곱해서 clamp하고 FP8로 cast. inverse scale은 나중에 dequantize에 쓰려고 함께 리턴.

`tensorwise scaling`이라는 표현의 의미가 이 한 함수에 있다 — *텐서 전체에 단 하나의 scale*. 만약 *rowwise*면 각 행에 별도 scale을 두는데, 그러면 cuBLAS가 아니라 CUTLASS kernel이 필요하다. 더 정확하지만 더 느리다. nanochat은 *간단함을 위해* tensorwise만 지원한다.

### 세 GEMM의 FP8 wrapping

Linear의 forward 한 번에는 *세 개의 matmul*이 들어간다.
- **Forward**: `out = input @ weight.T` (한 번)
- **Backward**: `d_in = d_out @ weight` (한 번)
- **Backward**: `d_w = d_out.T @ input` (한 번)

`_Float8Matmul`은 이 셋을 각각 `torch._scaled_mm`(cuBLAS FP8 kernel)으로 감싼다.

```python
# nanochat/fp8.py:125-153 (요약)
@torch._dynamo.allow_in_graph
class _Float8Matmul(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input_2d, weight):
        input_fp8, input_inv = _to_fp8(input_2d, torch.float8_e4m3fn)
        weight_fp8, weight_inv = _to_fp8(weight, torch.float8_e4m3fn)
        ctx.save_for_backward(input_fp8, input_inv, weight_fp8, weight_inv)
        output = torch._scaled_mm(
            input_fp8, weight_fp8.t(),
            scale_a=input_inv, scale_b=weight_inv,
            out_dtype=input_2d.dtype,
            use_fast_accum=True,
        )
        return output
```

흥미로운 디테일이 두 가지 있다. 첫째, `@torch._dynamo.allow_in_graph` — `torch.compile`이 이 autograd.Function을 *opaque node*로 취급하게 만든다. dynamo가 내부를 분해하려 들지 않는다. 둘째, `use_fast_accum=True` — 누적을 *더 낮은 정밀도*로 한다. forward에는 OK, backward에는 `False`로 *더 정확한 gradient*. 작은 디자인 결정이지만 모델의 *수렴*에 영향을 준다.

### E4M3 vs E5M2 — 정밀도와 range의 분기

FP8에는 두 포맷이 있다. 4A장에서도 한 번 봤지만 다시 정리하자.

- **`float8_e4m3fn`**: exponent 4 bit, mantissa 3 bit. 범위 [-448, 448], 정밀도 높음. **input과 weight**에 쓴다.
- **`float8_e5m2`**: exponent 5 bit, mantissa 2 bit. 범위 [-57344, 57344], range 높음. **gradient**에 쓴다.

왜 gradient만 다른가? Gradient는 *작은 값에서 큰 값까지* 동적 범위가 넓다. 정밀도보다 *언더플로우/오버플로우 방지*가 더 중요하다. 그래서 *exponent를 한 bit 더 주는* E5M2.

이걸 코드에서 보면 `_to_fp8`이 *forward에서는 `torch.float8_e4m3fn`*, *backward에서는 `torch.float8_e5m2`*로 호출된다. 한 함수가 *어떤 dtype을 인자로 받느냐*에 따라 다르게 굴러간다. 깔끔하다.

### 활성화 조건과 evaluation fallback

`base_train.py:167-192`에 FP8 활성화 조건이 박혀 있다.

```python
# scripts/base_train.py:178-185 (요약)
def fp8_module_filter(mod: nn.Module, fqn: str) -> bool:
    if not isinstance(mod, nn.Linear):
        return False
    if mod.in_features % 16 != 0 or mod.out_features % 16 != 0:
        return False
    if min(mod.in_features, mod.out_features) < 128:
        return False
    return True
```

*16의 배수* + *최소 차원 128 이상*인 Linear만 FP8로 변환된다. FP8 matmul kernel의 하드웨어 요구사항이다. 작은 Linear (예: 스칼라용 linear)는 그대로 bf16에 남는다. 깨끗한 디자인이다.

또 한 가지 영리함. *평가 중에는 FP8을 끄고 bf16으로 돌아간다*. `disable_fp8` 컨텍스트 매니저가 그 일을 한다 (`base_train.py:196-240`).

```python
# scripts/base_train.py:196-240 (요약)
@contextmanager
def disable_fp8(model):
    """Temporarily swap Float8Linear modules with nn.Linear for BF16 evaluation."""
    fp8_locations = []
    for name, module in model.named_modules():
        if 'Float8' in type(module).__name__:
            ...
    # Swap Float8Linear -> Linear
    for parent, attr_name, fp8_module in fp8_locations:
        linear = Linear(
            fp8_module.in_features, fp8_module.out_features,
            ..., device="meta",  # meta to avoid VRAM spike
        )
        linear.weight = fp8_module.weight  # share, don't copy
        ...
        setattr(parent, attr_name, linear)
    try:
        yield
    finally:
        for parent, attr_name, fp8_module in fp8_locations:
            setattr(parent, attr_name, fp8_module)
```

*평가의 정확도*를 위해 FP8을 일시적으로 *나*Linear로 swap한다. `device="meta"`로 *VRAM spike를 피하고*, `linear.weight = fp8_module.weight`로 *weight를 공유* — copy하지 않는다. `with`가 끝나면 다시 FP8로 복귀. *학습 속도(FP8)*와 *평가 정확도(bf16)*를 *동시에* 잡는 한 페이지짜리 트릭이다.

이게 *작은 영리함*의 누적이다. 카르파시가 FP8을 직접 구현하면서 *모든 디테일을 자기 손으로 깎아낸* 결과다. d24+ 모델에서 ~2× 빠른 wall-clock과 거의 동일한 val_bpb를 얻는 트레이드오프 — [#481 리더보드 #2](https://github.com/karpathy/nanochat/discussions/481)에서 d26 + fp8로 2.91h, val_bpb 0.74504, CORE 0.2578를 달성한 게 그 증거다.

## FlashAttention 3 디스패처 — SM90+bf16/fp8만

FP8이 matmul을 빠르게 만든다면, **FlashAttention 3**는 attention을 빠르게 만든다. 4B장에서 sliding window의 *SDPA fallback이 끔찍한* 이유를 얘기했는데, 그 끔찍함을 *피하는* 코드가 `nanochat/flash_attention.py`에 있다.

```python
# nanochat/flash_attention.py:23-38
def _load_flash_attention_3():
    """Try to load Flash Attention 3 (requires Hopper GPU, sm90)."""
    if not torch.cuda.is_available():
        return None
    try:
        major, _ = torch.cuda.get_device_capability()
        # FA3 kernels are compiled for Hopper (sm90) only
        # Ada (sm89), Blackwell (sm100) need SDPA fallback until FA3 is recompiled
        if major != 9:
            return None
        import os
        os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
        from kernels import get_kernel
        return get_kernel('varunneal/flash-attention-3').flash_attn_interface
    except Exception:
        return None
```

H100(sm90)만 FA3를 쓴다. RTX 4090(Ada, sm89)이나 Blackwell B100(sm100)은 *fallback*. 왜? FA3 kernel이 H100 전용으로 컴파일됐기 때문이다 — Hopper의 TMA(Tensor Memory Accelerator), WGMMA(Warp Group Matrix Multiply Accumulate) 같은 *Hopper 전용 instruction*을 활용한다. 다른 아키텍처에서는 *컴파일이 안 된다*.

`_resolve_use_fa3`는 한 단계 더 나간다.

```python
# nanochat/flash_attention.py:48-61
def _resolve_use_fa3():
    """Decide once whether to use FA3, based on availability, override, and dtype."""
    if _override_impl == 'fa3':
        assert HAS_FA3, "Cannot override to FA3: not available on this hardware"
        return True
    if _override_impl == 'sdpa':
        return False
    if HAS_FA3:
        # FA3 Hopper kernels only support bf16 and fp8
        from nanochat.common import COMPUTE_DTYPE
        if COMPUTE_DTYPE == torch.bfloat16:
            return True
        return False
    return False
```

H100이 있어도 *bf16이 아니면* SDPA로 떨어진다. FA3가 *bf16/fp8만 지원*하기 때문이다. fp32로 학습하면 — 가능은 하지만 — FA3가 안 굴러간다.

### Fallback의 위험

이 디스패처가 *조용히* 동작하기 때문에, 학습자가 *자기 GPU가 FA3를 안 쓰고 있다는 걸 모를* 수도 있다. 그래서 `base_train.py:103-117`이 학습 시작 시점에 *큰 글씨로 경고*한다.

```python
# scripts/base_train.py:103-117 (요약)
using_fa3 = USE_FA3
if using_fa3:
    print0("✓ Using Flash Attention 3 (Hopper GPU detected), efficient, new and awesome.")
else:
    print0("!" * 80)
    if HAS_FA3 and COMPUTE_DTYPE != torch.bfloat16:
        print0(f"WARNING: Flash Attention 3 only supports bf16, but COMPUTE_DTYPE={COMPUTE_DTYPE}. Using PyTorch SDPA fallback")
    else:
        print0("WARNING: Flash Attention 3 not available, using PyTorch SDPA fallback")
    print0("WARNING: Training will be less efficient without FA3")
    if args.window_pattern != "L":
        print0(f"WARNING: SDPA has no support for sliding window attention ...")
    print0("!" * 80)
```

`!`이 80번 반복되는 줄이 *위아래로* 박혀 있다. 시각적으로 *놓칠 수가 없게* 만들어둔 거다. 작은 디테일이지만, *학습자가 자기 환경의 한계를 모르고* 8시간 돌린 뒤에 *"왜 이렇게 느리지?"* 하는 *난감한 상황*을 막는다.

기억해두자. *fallback*은 코드가 굴러가게 해주지만, *경고가 없으면* 사용자는 자기가 *느린 경로*에 있다는 걸 모른다. 좋은 디스패처는 *조용한 fallback + 시끄러운 경고*다.

## GC freeze trick — 첫 step의 500ms 도둑

학습 루프 한가운데에 *눈에 안 띄는 한 줄*이 있다. `base_train.py:586-594`다.

```python
# scripts/base_train.py:586-594
# The garbage collector is sadly a little bit overactive and for some poorly understood reason,
# it spends ~500ms scanning for cycles quite frequently, just to end up cleaning up very few tiny objects each time.
# So we manually manage and help it out here
if first_step_of_run:
    gc.collect() # manually collect a lot of garbage from setup
    gc.freeze() # immediately freeze all currently surviving objects and exclude them from GC
    gc.disable() # nuclear intervention here: disable GC entirely except:
elif step % 5000 == 0: # every 5000 steps...
    gc.collect() # manually collect, just to be safe for very, very long runs
```

주석이 솔직하다. *"poorly understood reason"*. 어떤 이유로 Python GC가 *매번 ~500ms씩 잡아먹는다*. *적은 객체를 청소하면서* 500ms를 쓴다. 학습 step이 한 번에 ~100~200ms 걸리는 걸 생각하면, GC가 *step 하나 분량*의 시간을 *그냥 가져간다*.

해결책은 *극단적*이다.

1. `gc.collect()` — 일단 setup에서 쌓인 *진짜 쓰레기*를 한 번 청소.
2. `gc.freeze()` — *지금 살아 있는 모든 객체*를 GC 대상에서 *영구 제외*. 모델 weight, optimizer state, 버퍼 — 다.
3. `gc.disable()` — GC를 *완전히* 끈다.
4. *5000 step마다 한 번씩* `gc.collect()`로 *혹시 모를 누수*만 정리.

주석의 *"nuclear intervention"*이라는 표현이 솔직하다. 이건 *권장 패턴*이 아니다. 보통의 Python 코드라면 *번거롭다*고 할 만한 *과도한 개입*이다. 그런데 학습 루프는 *수만 step*을 돈다. step당 500ms × 10,000 step = 83분. *83분을 그냥 GC에 헌납하는 일*이 *끔찍한 일이다*.

그래서 *극단적인 트릭*이 정당화된다. *"poorly understood"*라고 솔직하게 인정하고 — 카르파시도 *왜 GC가 그렇게 동작하는지 100% 이해하지 못한다* — 그럼에도 *효과는 검증된* 트릭. 사전학습의 *작은 영리함*들 중 가장 *솔직한* 한 줄이다.

이 트릭은 *언제 안 써도 되는가*? CPU/MPS 환경의 단기 실험. d6를 5000 step만 돌리는 우리의 노트북 실습 같은 경우. GC가 500ms씩 잡아먹어도 *체감이 안 된다*. 그래서 `runcpu.sh`에서도 이 줄이 *그냥 실행되긴 한다*. 다만 효과가 *느껴지지 않을 뿐*이다.

## 체크포인트 한 박스 — 재현성에 대한 책

> ### 체크포인트 한 박스
>
> nanochat의 체크포인트 관리는 *3장의 토크나이저 학습부터 11장의 report.md까지* 모든 단계를 *재현 가능*하게 만든다. `nanochat/checkpoint_manager.py`의 *195줄*이 그 책임을 진다.
>
> **세 가지 파일이 한 step에 함께 저장된다:**
>
> ```
> base_checkpoints/d24/
>   model_005000.pt        # 모델 state_dict (rank 0만)
>   optim_005000_rank0.pt  # 옵티마이저 state (rank별)
>   optim_005000_rank1.pt
>   optim_005000_rank2.pt
>   ...
>   optim_005000_rank7.pt  # 8XH100이면 rank 8개
>   meta_005000.json       # 메타데이터 (config, loop state, dataloader state)
> ```
>
> *Optimizer state가 rank별로 shard되는 게* ZeRO-2 스타일 분산의 *물리적 흔적*이다. 5장에서 본 `DistMuonAdamW`의 *3-phase async*가 *각 rank마다 다른 optimizer state slice*를 갖고 있기 때문에, 저장도 *rank마다 따로* 한다. Resume할 때는 *내 rank의 shard*만 읽어 들이면 된다.
>
> **`_patch_missing_keys` — 옛 체크포인트 호환성**
>
> ```python
> # nanochat/checkpoint_manager.py:30-40
> def _patch_missing_keys(model_data, model_config):
>     """Add default values for new parameters that may be missing in old checkpoints."""
>     n_layer = model_config.n_layer
>     if "resid_lambdas" not in model_data:
>         model_data["resid_lambdas"] = torch.ones(n_layer)
>         log0(f"Patching missing resid_lambdas in model data to 1.0")
>     if "x0_lambdas" not in model_data:
>         model_data["x0_lambdas"] = torch.zeros(n_layer)
>         log0(f"Patching missing x0_lambdas in model data to 0.0")
> ```
>
> 4B장의 *per-layer learnable scalars*가 추가되기 *전*의 체크포인트를 *그대로 로드*할 수 있게 해주는 마법. `resid_lambdas`가 없으면 1로(항등 스케일링), `x0_lambdas`가 없으면 0으로(기능 비활성). nanochat이 *진화하는* 동안 *옛 모델을 버리지 않게* 해주는 한 함수.
>
> **`find_largest_model` — d{N} 패턴 정렬**
>
> ```python
> # nanochat/checkpoint_manager.py:118-135
> def find_largest_model(checkpoints_dir):
>     model_tags = [f for f in os.listdir(checkpoints_dir) if os.path.isdir(...)]
>     candidates = []
>     for model_tag in model_tags:
>         match = re.match(r"d(\d+)", model_tag)
>         if match:
>             model_depth = int(match.group(1))
>             candidates.append((model_depth, model_tag))
>     if candidates:
>         candidates.sort(key=lambda x: x[0], reverse=True)
>         return candidates[0][1]
>     model_tags.sort(key=lambda x: os.path.getmtime(...), reverse=True)
>     return model_tags[0]
> ```
>
> `base_checkpoints/` 디렉토리에 `d4/`, `d6/`, `d12/`, `d24/`가 섞여 있을 때 *가장 큰 것*을 자동으로 골라준다. 정규식 `d(\d+)`로 매칭, 숫자 추출, 정렬, top-1. 만약 *d{N}* 패턴이 안 맞으면 *가장 최근에 수정된* 것으로 fallback. 10장에서 `chat_cli`나 `chat_web`을 띄울 때 *명시적으로 모델을 지정하지 않으면* 이 함수가 *조용히 가장 큰 모델*을 골라준다.
>
> **이 모든 게 모이면 — 재현성에 대한 책**
>
> 카르파시가 [README](https://github.com/karpathy/nanochat)에서 *"the best ChatGPT that $100 can buy"*를 자신할 수 있는 건, *재현 가능한 한 페이지의 report*가 매번 *같은 방식으로* 만들어지기 때문이다. config는 JSON으로, weight는 .pt로, optimizer는 rank-shard로, dataloader 상태는 meta에. 11장에서 우리가 다룰 `report.md`는 이 모든 메타데이터를 *모아 한 페이지로 정리*한 산물이다.

위 박스가 길지만, 한 번 읽어두면 11장이 한결 가볍게 읽힌다. *재현성*은 단순히 "결과를 다시 만들 수 있다"가 아니라 *"실험의 모든 디테일이 디스크에 남아 있다"*는 더 강한 의미다. nanochat의 모든 체크포인트는 그 강한 의미를 만족한다.

## wandb 그래프 — 무엇을 봐야 하는가

이제 학습이 *진행되는 중*에 우리가 *어떤 화면을 봐야 하는지*로 가보자. `base_train.py:568-580`에 wandb log가 어떤 모양으로 들어가는지 박혀 있다.

```python
# scripts/base_train.py:568-580 (요약)
if step % 100 == 0:
    log_data = {
        "step": step,
        "total_training_flops": flops_so_far,
        "total_training_time": total_training_time,
        "train/loss": debiased_smooth_loss,
        "train/lrm": lrm,
        "train/dt": dt,
        "train/tok_per_sec": tok_per_sec,
        "train/mfu": mfu,
        "train/epoch": epoch,
    }
    wandb_run.log(log_data)
```

매 100 step마다 9개 메트릭을 wandb로 보낸다. 그리고 eval이 돌 때마다(`base_train.py:430-435`) `val/bpb`와 `total_training_time`이 따로 들어간다. CORE eval은(`:447-452`) `core_metric`이.

이걸 wandb 페이지에서 보면 *네 개의 핵심 곡선*이 떠오른다.

### 곡선 1: `val/bpb` — 사전학습의 단일 진실

가장 중요한 곡선이다. 가로축이 step 또는 total_training_flops, 세로축이 bpb. d24 모델이라면 시작점이 ~3.0 (random에 가까운 값) 정도, 끝점이 ~0.745 정도. *오른쪽 아래로 가파르게 떨어지는* 곡선.

이 곡선의 *모양*을 한 번 자세히 보자.

- **첫 500 step**: 가파르게 떨어진다. *모델이 토크나이저의 frequency를 익히는* 구간. 가장 흔한 토큰을 예측만 해도 loss가 크게 줄어든다.
- **500 ~ 5000 step**: 천천히 내려간다. *문법과 단순 의미*를 익힌다.
- **5000 step ~ 끝**: 거의 *평지에 가까운 완만한 내림*. *세계 지식과 추론*을 익히는 영역. *작은 개선이 큰 의미*를 갖는다.

곡선의 모양이 *세 단계*로 보이는 게 정설이다. *Karpathy의 [README](https://github.com/karpathy/nanochat#time-to-gpt-2-leaderboard)*가 보여주는 그래프도 이 모양이다.

### 곡선 2: `train/mfu` — 하드웨어를 얼마나 잘 쓰고 있는가

MFU(Model FLOPs Utilization)는 *peak FLOPS 대비 실제 사용한 FLOPS의 비율*이다. H100에서 50%를 목표로 한다 — peak 989 TFLOPS의 절반인 ~495 TFLOPS로 굴린다는 뜻.

이 곡선이 *평지에 가까우면 좋다*. 갑자기 떨어지면 *뭔가 잘못된 신호다*. 가능한 원인:

- **OOM 직전**: VRAM이 부족해서 PyTorch가 *swap을 시도*. 매 step의 dt가 늘어난다.
- **NCCL 통신 지연**: 분산 학습에서 한 rank가 *느려졌을 때*. 다른 rank들이 *기다린다*.
- **데이터로딩 병목**: dataloader의 `refill_buffer`가 *느려졌을 때*. forward는 끝났는데 *다음 batch가 안 들어옴*.

CPU/MPS에서는 `get_peak_flops`가 `float('inf')`를 리턴하니까 MFU가 *항상 0%*로 나온다. 노트북 환경에서는 이 곡선을 보지 않아도 된다.

### 곡선 3: `train/tok_per_sec` — 처리량

초당 학습 토큰 수. H100 한 장에서 d24 + fp8 + FA3로 ~50K~100K tok/s 정도. 8XH100이면 *그 8배*. 곡선이 *평지에 가까워야 한다*. 갑자기 떨어지면 데이터로딩이나 OOM swap 같은 *난감한 상황*의 신호다.

### 곡선 4: VRAM utilization

wandb의 자동 시스템 메트릭에 들어 있다. `gpu0/memory.allocated/bytes` 같은 이름. *학습 시작 직후 한 번에 차오른 뒤 평지*가 정상이다. *천천히 오르면* 메모리 누수, *갑자기 떨어지면* PyTorch가 *free하고 다시 잡는 중*.

### 종합 — 한 화면에 네 개

좋은 wandb 대시보드는 *이 네 개를 한 화면*에 둔다. `val/bpb`가 잘 떨어지고 있는가, `train/mfu`가 안정적인가, `tok_per_sec`이 일정한가, VRAM이 평지인가. 학습 첫 30분 동안 *이 네 개가 다 OK*면 — 그 학습은 *끝까지 잘 돌아갈 가능성이 매우 높다*.

반대로 *첫 30분에 한 곡선이라도 이상하면* 빨리 멈추고 *원인을 찾는 편이 낫다*. 8XH100 노드 시간으로 따지면 *30분이 ~$8*. 작은 비용으로 큰 *난감한 상황*을 막을 수 있다.

## 학습이 발산하면 — 세 가지 신호

`val_bpb`가 잘 떨어지다가 *갑자기 튀어오르면* 어떻게 해야 할까? 사전학습은 *수만 step짜리 마라톤*이라, 한 번 발산하면 *그동안의 시간이 다 날아간다*. *끔찍한 일이다*.

세 가지 신호와 세 가지 대응을 함께 살펴보자.

### 신호 1: train/loss가 갑자기 튄다

가장 흔한 발산이다. *어느 한 batch에 outlier가 있어서* 한 step의 gradient가 *수십 배*로 커진 경우. 보통은 logit softcap (`gpt.py:466-472`의 `softcap = 15 * tanh(logits/15)`)이 잡아준다. 그래도 안 잡히면 — 두 가지를 의심한다.

**(a) LR이 너무 크다.** `--matrix-lr=0.02`가 default인데, 작은 batch에서 이걸 그대로 쓰면 *과도하게 큰 step*. `--matrix-lr=0.01`로 절반으로 줄이고 재시작.

**(b) Batch가 너무 작다.** `--total-batch-size=-1`로 자동을 쓰는데, 자동 계산이 *작은 값*을 골랐을 수 있다. *명시적으로 더 큰 값*을 박아준다. 예를 들어 `--total-batch-size=524288`.

### 신호 2: val_bpb는 떨어지는데 train/loss가 발산한다

이건 *데이터 노이즈*의 신호다. 일부 시퀀스가 *깨진 인코딩*이거나 *비정상적으로 긴 토큰 시퀀스*. 평가는 fineweb의 *깨끗한 부분*만 보니까 val은 멀쩡한데, train이 *오염된 시퀀스*를 만나면 갑자기 튄다.

대응: dataloader의 buffer_size를 키워서 *문서 다양성*을 늘리거나, 데이터셋을 *한 번 더 청소*한다. 또는 `gradient_clipping`을 추가한다 (nanochat default는 clipping을 *안* 쓰는데, 발산이 자주 나면 0.5~1.0 정도로 추가하는 편이 낫다).

### 신호 3: 첫 step부터 loss가 너무 크다

`train/loss`가 step 0에서 *~12*보다 훨씬 크다 (vocab_size 32K의 log = 10.4 정도가 random baseline). 초기화가 잘못됐다는 신호다.

대응: `init_weights`의 imbed std를 조정하거나(4A장 참조), torch.compile 캐시를 지우고 재시작. 4A장 실습에서 std=0.1로 바꿔봤을 때의 효과를 떠올려보자 — *초기화의 영향*이 *눈에 보였다*.

### 발산은 *실패가 아니다*

기억해두자. 학습이 발산하는 건 *실패*가 아니라 *피드백*이다. wandb 곡선이 *튀어오르는 순간*이 바로 *어떤 가설을 확인할 수 있는 기회*다. 어떤 하이퍼파라미터를 조정해서 *왜* 안정화되는지를 보면, 그게 *진짜 학습*이다. 카르파시가 *320개의 hyperparameter sweep*을 [#481](https://github.com/karpathy/nanochat/discussions/481)에서 자랑하는 건 *각 실험이 무언가를 가르쳤기* 때문이다.

물론 *피드백을 위해 8XH100을 의도적으로 발산시키는 건* 비싸다. 그래서 *작은 모델에서 빠른 실험*을 먼저 해보는 게 좋다. d6 + 5000 step으로 *한 번에 30분*이면 *난감한 상황*을 *값싸게* 한 번 경험할 수 있다.

## 챕터 끝 실습

이제 직접 굴려볼 차례다. 두 단계로 나누자.

### [CPU/MPS 40분] d6 사전학습 — `runcpu.sh`의 base_train

먼저 노트북에서 한 판 굴려보자. M3 Max 기준 약 30~40분. RTX 4090이 있다면 더 빨리 끝난다.

전제 — `runcpu.sh`의 (1)~(2) 단계는 이미 끝나야 한다. 즉 토크나이저 학습이 완료돼서 `~/.cache/nanochat/tokenizer/{tokenizer.pkl, token_bytes.pt}`가 존재해야 한다. 그리고 데이터셰드 8개도 받아둬야 한다.

```bash
# 환경 설정 (이전 챕터에서 이미 했다면 스킵)
export NANOCHAT_BASE_DIR="$HOME/.cache/nanochat"

# d6 사전학습 — 약 30~40분
python -m scripts.base_train \
    --depth=6 --head-dim=64 \
    --window-pattern=L \
    --max-seq-len=512 \
    --device-batch-size=32 --total-batch-size=16384 \
    --eval-every=100 --eval-tokens=524288 \
    --core-metric-every=-1 \
    --sample-every=100 \
    --num-iterations=5000
```

각 옵션의 의미를 한 줄씩 정리해두자.

- `--depth=6`: 6개 layer. 가장 작은 의미 있는 크기.
- `--head-dim=64`: H100에서는 128이 default인데, CPU에서는 64로 줄여 memory pressure를 낮춤.
- `--window-pattern=L`: full context. sliding window의 SDPA fallback이 *끔찍하니까* 꺼둔다.
- `--max-seq-len=512`: 짧은 시퀀스. 2048은 노트북에서 OOM 위험.
- `--device-batch-size=32 --total-batch-size=16384`: 한 step에 16,384 토큰. grad accumulation = 1 (단일 프로세스).
- `--eval-every=100`: 매 100 step마다 val_bpb 평가.
- `--core-metric-every=-1`: CORE 평가는 끔. d6에서는 신호가 너무 약하고 시간만 잡아먹는다.
- `--sample-every=100`: 매 100 step마다 7개 프롬프트로 sample을 생성. *모델이 점점 말이 되어가는 과정*을 관찰할 수 있다.
- `--num-iterations=5000`: 5,000 step.

학습이 돌기 시작하면 콘솔에 *step 진행 + val_bpb + sample 출력*이 차례로 떠오른다.

**step 0~500**: 모델이 *random에 가깝다*. sample은 *완전한 횡설수설*. `train/loss`가 매우 빠르게 떨어진다.

**step 500~2000**: sample이 *영어처럼 보이기 시작*한다. 문법은 안 맞아도 *영어 단어*는 나온다. val_bpb가 2.0 근처에서 안정.

**step 2000~5000**: sample이 *문장처럼 들린다*. 다만 *의미*는 어색하다. *"The capital of France is"* 같은 단순한 prompt에 *Paris*가 아닌 *완성형 문장*이 나올 수 있다.

학습이 끝나면 다음을 확인하자.

```bash
ls -la $NANOCHAT_BASE_DIR/base_checkpoints/d6/
# model_005000.pt, meta_005000.json, optim_005000_rank0.pt
```

세 파일이 있어야 한다. *재현성에 대한 책*의 박스에서 본 그 세 파일이다.

그리고 wandb를 안 썼더라도 콘솔 출력의 *최종 line*에 `Minimum validation bpb: X.XXXXXX`가 박혀 있을 거다. M3 Max에서 d6 + 5000 step이면 *1.5~1.8 정도*가 정상이다.

곡선을 시각화하고 싶다면, 콘솔 출력을 파일로 저장한 뒤 `grep` 한 줄로 뽑아 plot할 수도 있다.

```bash
# 학습 로그를 저장하면서 돌리려면
python -m scripts.base_train ... 2>&1 | tee /tmp/d6_train.log
# 학습 후 val_bpb 곡선 추출
grep "Validation bpb" /tmp/d6_train.log
```

### [GPU, 사다리 표] 환경별 기대 결과

GPU 자원이 있다면 더 큰 모델을 시도할 수 있다. 환경에 따라 *기대할 수 있는 결과*가 다르니, 사다리 표로 정리해두자.

| 환경 | depth | 시간 | 비용 | 기대 val_bpb |
|---|---|---|---|---|
| 8×H100 spot | d24 | 3시간 | ~$48 | **0.745** (GPT-2급) |
| 8×H100 spot + fp8 | d26 | 2.9시간 | ~$46 | **0.745** ([#481 #2](https://github.com/karpathy/nanochat/discussions/481)) |
| A100 1장 | d12 | 24시간 | ~$24 | **1.0 근처** (작은 모델) |
| RTX 4090 1장 | d8 | 12시간 | (로컬) | **1.2 근처** (장난감급) |
| M3 Max (CPU/MPS) | d6 | 40분 | (로컬) | **1.5~1.8** (코드 검증용) |

각 줄을 한 줄씩 해석해보자.

**8×H100 spot, d24, 3시간, val_bpb 0.745**: nanochat의 *정설 경로*. `runs/speedrun.sh`가 그대로 돌리는 거다. GPT-2의 reference CORE 0.256525와 *동급의 결과*. 클라우드 spot 인스턴스를 잡을 수 있다면 *지금 당장 시작할 수 있는* 가장 빠른 경로.

**8×H100 spot + fp8, d26, 2.9시간**: [#481 리더보드 #2](https://github.com/karpathy/nanochat/discussions/481)가 도달한 결과. FP8 학습을 켜면 *깊이를 d24 → d26으로 늘려도 시간이 오히려 줄어든다*. wall-clock과 final val_bpb의 *동시 개선*. 다만 *fp8 hardware 요구사항* 때문에 H100+에서만 의미가 있다.

**A100 1장, d12, 24시간, val_bpb 1.0 근처**: 가성비가 좋은 클라우드 옵션. 한 장의 A100을 24시간 빌리는 비용 ~$24. *GPT-2급은 아니지만* — val_bpb 1.0이면 *영어 문법은 거의 다 익힌* 수준이다. SFT를 얹으면 *기본적인 대화*는 가능하다.

**RTX 4090 1장, d8, 12시간**: 로컬에서 가능한 가장 큰 실험. *24GB VRAM*에 d8 모델이 *겨우 들어간다*. FA3가 안 굴러가니까 SDPA fallback. `--window-pattern=L`로 sliding window 끄는 게 *필수*.

**M3 Max, d6, 40분**: 우리가 위에서 한 실습. *코드 검증용*. *진짜 모델*은 아니다.

기억해두자. 한 줄 위로 올라갈 때마다 *수치는 좋아지지만 시간/돈이 4배씩 늘어난다*. 자기 환경에 맞는 줄을 *고르는* 게 *정직한 학습*이다. *"꼭 GPT-2급을 만들어야지"*가 아니라, *"내가 가진 자원에서 가장 의미 있는 실험을 해보자"*가 더 건강하다.

## 마무리

여기까지 따라왔다면, 우리는 한 가지 큰 봉우리를 *함께 넘었다*. 631줄짜리 `base_train.py`가 *어떻게* 우리가 5장까지 준비한 모든 조각을 *오케스트레이션*하는지, 그리고 그 결과로 *어떤 곡선*이 wandb에 떠오르는지, *어떤 신호*가 발산의 전조인지를 봤다.

이번 챕터의 정서는 *돌파*다. 토비의 *"드디어"*가 어울리는 챕터다. 2장의 토크나이저, 3장의 token_bytes, 4A의 GPT 골격, 4B의 7개 트릭, 5장의 MuonAdamW — 이 모든 게 *한 그래프 위에서 협력*하는 장면. *"내가 만든 토크나이저, 내가 읽은 GPT 모듈, 내가 이해한 Muon이 함께 굴러간다."*

그 협력의 결과로 우리는 *어떤 모델*을 얻었다. 8XH100에서 3시간 돌렸다면 val_bpb 0.745, CORE 0.258 정도의 *GPT-2급 base 모델*. M3 Max에서 40분 돌렸다면 val_bpb 1.5~1.8 정도의 *코드 검증용 미니 모델*. 어느 쪽이든, 디스크에는 *세 개의 파일*이 남았다 — `model_*.pt`, `optim_*_rank*.pt`, `meta_*.json`.

그런데, 잠깐 멈추고 *솔직한 질문* 하나를 던져보자. 우리가 *진짜로* GPT-2급에 도달했다고 어떻게 *확신*할 수 있는가? *val_bpb 0.745*라는 숫자는 *어디서 나온 것이고*, *무엇을 측정한 것이고*, *무엇을 측정하지 못하는가*?

이 질문이 다음 챕터의 문턱이다. 6장의 *돌파의 흥분*을 잠깐 가라앉히고, 7장에서는 *차분한 회의*로 우리가 만든 것의 *정체*를 따져보자. bits-per-byte의 정의, CORE 22-task의 구성, centered accuracy의 trick, 그리고 *평가의 한계*까지. 사전학습의 *결과*를 *제대로 측정*하는 법을 함께 알아보자.

봉우리를 오른 뒤에는 *내려가는 길*도 정직하게 살펴봐야 한다. 7장의 *짧고 깊은 골짜기*에서, 우리가 만든 것의 *진짜 모양*을 함께 들여다보자.
