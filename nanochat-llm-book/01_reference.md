# nanochat 책 레퍼런스

이 문서는 챕터 저자가 그대로 인용·발췌해서 쓸 수 있는 단일 사실 출처다. 모든 코드 인용은 워크트리 안의 절대 경로(`/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/nanochat/nanochat/...`)를 단축해서 `nanochat/...` 형식으로 표기한다. 외부 인용에는 출처를 단다.

---

## 0. 책의 전제

### "$100 ChatGPT" 발상과 Karpathy의 의도

Karpathy는 2025년 10월 13일 [GitHub Discussion #1](https://github.com/karpathy/nanochat/discussions/1)과 X(트위터)에서 nanochat을 공개했다. 핵심 문구 한 줄: *"the best ChatGPT that $100 can buy."* 의도는 다음 세 가지가 한 자리에 있다는 점이다.

1. **하나의 단일 리포지토리**가 토크나이저 학습 → 사전학습(pretraining) → 미드트레이닝(midtraining) → SFT → RL → 추론 엔진 → ChatGPT 스타일 Web UI까지 전부 다룬다. 코드 총량은 약 8,000줄(README #1 commenter, [HN 토론](https://news.ycombinator.com/item?id=45569350) 참조).
2. **8XH100 한 노드**에서 약 3시간 동안 돌리면 GPT-2(2019, 약 $43K)와 동급 — 정확히는 [DCLM CORE 지표](https://arxiv.org/abs/2406.11794)에서 GPT-2의 0.256525를 넘기는 — 모델이 나온다. 현재 시점 spot 인스턴스 기준 ~$15, 정가 기준 ~$48~$92 사이.
3. **단 하나의 복잡도 다이얼 `--depth`** 만 돌리면 다른 모든 하이퍼파라미터(width, head 수, LR 보정, 학습 토큰 수, weight decay)가 컴퓨트-옵티멀하게 자동 결정된다. d4(런CPU 데모)부터 d26(GPT-2급)까지 같은 코드로 미니시리즈가 만들어진다(`runs/miniseries.sh`, [#420 discussion](https://github.com/karpathy/nanochat/discussions/420)).

Karpathy는 [HN 댓글](https://news.ycombinator.com/item?id=45569350)에서 "코드 대부분을 손으로 직접 쳤다. claude/codex agent를 몇 번 써봤지만 잘 안 됐다 — 아마 이 리포가 학습 데이터 분포에서 너무 멀리 떨어져 있어서 그런 듯하다"고 밝혔다. 이건 책 전반에 흐르는 톤이다: **'AI를 쓰는 게 아니라 만드는 코드는 여전히 사람이 짜야 한다'**는 입장.

리포 명칭은 사전학습만 다뤘던 [nanoGPT](https://github.com/karpathy/nanoGPT)에서 따왔고, modded-nanoGPT([Keller Jordan](https://github.com/KellerJordan/modded-nanogpt))의 GPT-2 speedrun 리더보드 문화·Muon 옵티마이저·여러 구현 디테일을 차용했다. fineweb·smoltalk 등 데이터셋은 HuggingFace가 공급한다.

### 대상 독자가 이미 갖춘 것·새로 배워야 할 것

이 책의 독자는:
- PyTorch와 파이썬을 다룬다 (`torch.nn.Module`, `torch.compile`, autograd, DDP의 개념은 안다)
- GPU 환경에 익숙하다 (`nvidia-smi`, OOM, bf16/fp16/fp32의 의미는 안다)
- ChatGPT는 써봤지만 내부가 어떻게 굴러가는지는 모른다
- "내가 직접 한 번 처음부터 끝까지 굴려보고 싶다"는 동기가 있다

새로 배워야 할 것:
- 토크나이저(BPE)가 왜 필요한가, vocab_size·compression_ratio가 모델 성능에 어떤 영향을 주는가
- pretraining vs midtraining vs SFT vs RL이 각각 무엇을 가르치는가
- Transformer 아키텍처의 최신 변종(RoPE, RMSNorm, SwiGLU/ReLU², GQA, sliding window attention, value embeddings)
- 옵티마이저: AdamW가 무엇이고 Muon이 왜 등장했는가
- 학습 인프라: bf16/fp8, FlashAttention, BOS-aligned bestfit dataloader, ZeRO-2 스타일 분산
- 평가: CORE score, bits-per-byte, MMLU·ARC·GSM8K·HumanEval이 무엇을 측정하는가
- 추론: KV cache, sampling temperature/top-k, tool use(calculator/Python)

---

## 1. LLM 학습 파이프라인 개관

`runs/speedrun.sh`가 그대로 보여주는 정설 시퀀스다. 각 단계가 "무엇을 가르치는가"와 "무엇으로 검증하는가"가 다르다.

| 단계 | 입력 | 출력 | 가르치는 것 | 검증 지표 |
|------|------|------|-------------|-----------|
| Tokenizer | 약 2B chars의 FineWeb 텍스트 | `tokenizer.pkl` (vocab 32,768) | 바이트열을 의미 단위로 묶기 (BPE) | compression ratio (vs GPT-2/GPT-4) |
| Pretrain | FineWeb 약 11B tokens (d24 기준 12:1 토큰:파라미터) | `base_checkpoints/d24/` | 다음 토큰 예측 (causal LM) | val_bpb, CORE |
| Midtrain | (현 master에서는 SFT에 통합됨) | — | (구판) 채팅·다중선택·도구 사용 사전 노출 | val_bpb |
| SFT | SmolTalk(460K) + MMLU·GSM8K(epochs) + identity(2 epochs) + SpellingBee | `chatsft_checkpoints/d24/` | 대화 포맷, multiple choice, 도구 사용, personality | ChatCORE (centered ARC/MMLU/GSM8K/HumanEval/SpellingBee) |
| RL (선택) | GSM8K train | `chatrl_checkpoints/d24/` | 수학 reasoning을 보상 기반으로 강화 | GSM8K pass@k |
| Inference | (모델 + 사용자 입력) | 토큰 스트림 | — | 정성 평가, latency, 메모리 |

핵심 통찰 — **'대화 능력'은 pretraining에서는 안 생긴다.** Pretrain된 base 모델은 "The capital of France is" → "Paris" 같은 *문장 완성*만 한다. ChatGPT처럼 답하려면 SFT 단계에서 `<|user_start|>...<|user_end|><|assistant_start|>...<|assistant_end|>` 같은 특수 토큰 구조와 어시스턴트로서의 역할을 학습시켜야 한다. 이건 토크나이저에 9개의 `SPECIAL_TOKENS`가 박혀 있는 이유다(`nanochat/tokenizer.py:13-25`).

또 하나의 통찰 — **'능력'은 데이터로 가르치는 것이 코드로 가르치는 것보다 흔하다.** SpellingBee/identity 챗봇 사례가 이를 보여준다([#139](https://github.com/karpathy/nanochat/discussions/139), [#164](https://github.com/karpathy/nanochat/discussions/164)). 새 능력 추가 = synthetic data 생성 → SFT mix에 추가.

---

## 2. nanochat 코드 지도

### 2.1 디렉토리 트리

```
nanochat/
├── nanochat/           # 라이브러리 (재사용 가능한 모듈)
│   ├── gpt.py              # GPT nn.Module
│   ├── tokenizer.py        # BPE: HF 호환 / rustbpe+tiktoken
│   ├── optim.py            # MuonAdamW (1GPU + ZeRO-2 distributed)
│   ├── dataloader.py       # BOS-aligned bestfit-crop dataloader
│   ├── dataset.py          # parquet 셰드 다운로드/iter
│   ├── engine.py           # KV-cache 추론 엔진 (+ tool use FSM)
│   ├── flash_attention.py  # FA3 / SDPA 디스패처
│   ├── fp8.py              # 자체 미니 FP8 학습 (torchao 대체, ~150줄)
│   ├── core_eval.py        # DCLM CORE 22-task 평가
│   ├── loss_eval.py        # bits-per-byte 평가
│   ├── checkpoint_manager.py
│   ├── common.py           # COMPUTE_DTYPE, ddp setup, GPU TFLOPS 테이블
│   ├── execution.py        # 샌드박스 Python 실행 (HumanEval용)
│   ├── report.py           # markdown 학습 리포트 생성
│   └── ui.html             # 챗봇 프론트엔드
├── scripts/            # CLI 진입점
│   ├── tok_train.py / tok_eval.py
│   ├── base_train.py / base_eval.py
│   ├── chat_sft.py / chat_rl.py / chat_eval.py
│   └── chat_cli.py / chat_web.py
├── tasks/              # 데이터셋·평가 정의
│   ├── common.py           # Task base class, TaskMixture
│   ├── arc.py mmlu.py gsm8k.py humaneval.py smoltalk.py
│   ├── spellingbee.py      # 합성 spelling/counting task
│   └── customjson.py       # jsonl 대화 파일을 task로
├── runs/               # 풀 파이프라인 쉘 스크립트
│   ├── speedrun.sh         # 8XH100, GPT-2급 d24
│   ├── runcpu.sh           # CPU/MPS d6 데모
│   ├── scaling_laws.sh
│   └── miniseries.sh
├── dev/                # 보조 도구
│   └── gen_synthetic_data.py  # OpenRouter로 identity 대화 생성
└── tests/test_engine.py
```

### 2.2 모듈별 요약

각 항목은 챕터 저자가 코드를 다시 열지 않아도 인용할 수 있도록 *책임 한 줄 + 핵심 시그니처 + 설계 결정 + 외부 개념 매핑 + 인용용 라인 범위* 형식이다.

---

#### `nanochat/common.py` — 컴퓨트 환경의 단일 진실

**책임:** dtype 자동선택, DDP 초기화, GPU FLOPS 테이블, 로깅 보조.

**핵심:**
- `COMPUTE_DTYPE` — 모듈 임포트 시점에 자동 결정되는 전역 dtype. CUDA SM 80+ → bf16, 그 미만 → fp32, CPU/MPS → fp32. `NANOCHAT_DTYPE` 환경변수로 오버라이드 (`common.py:13-31`).
- `compute_init(device_type)` → `(ddp, ddp_rank, ddp_local_rank, ddp_world_size, device)` 튜플. NCCL 백엔드로 process group을 초기화하거나 단일 GPU/CPU/MPS 모드를 결정 (`common.py:173-208`).
- `get_peak_flops(device_name)` — H100/A100/3090 등의 BF16 peak FLOPS 하드코딩 테이블. MFU 계산에 쓰임 (`common.py:227-278`).

**설계 결정:** Karpathy는 `torch.amp.autocast`를 *쓰지 않는다*. 대신 master weight는 fp32로 두고, custom `Linear` 클래스가 forward에서 `weight.to(x.dtype)`로 캐스팅한다(`gpt.py:45-50`). 임베딩은 메모리 절약 차원에서 직접 `COMPUTE_DTYPE`로 저장한다(`gpt.py:260-266`). 이 디자인은 "어디서 어떤 정밀도가 쓰이는지 한눈에 보이는" 정합성을 우선한다.

**의존 개념:** mixed precision training, NCCL, DDP. → §3 "FP8 training" 항목과 연결.

---

#### `nanochat/tokenizer.py` — GPT-4 스타일 BPE

**책임:** 두 가지 BPE 백엔드(HF tokenizers / rustbpe+tiktoken)를 같은 API 뒤에 둔다. 대화 렌더링과 도구 호출 토큰 삽입을 함께 책임진다.

**핵심:**
- `SPLIT_PATTERN` — GPT-4 정규식 pretokenizer 변형. `\p{N}{1,3}` → `\p{N}{1,2}` (32K vocab에서 숫자에 토큰을 덜 쏟게 함). `tokenizer.py:30`.
- `SPECIAL_TOKENS` — 9개: `<|bos|>`, `<|user_start|>`, `<|user_end|>`, `<|assistant_start|>`, `<|assistant_end|>`, `<|python_start|>`, `<|python_end|>`, `<|output_start|>`, `<|output_end|>` (`tokenizer.py:13-25`).
- `RustBPETokenizer.train_from_iterator(text_iter, vocab_size)` — rustbpe로 학습하고, mergeable_ranks를 추출해 `tiktoken.Encoding`을 만든다. 학습은 rust로, 추론은 tiktoken으로(빠른 C++ 백엔드) (`tokenizer.py:170-190`).
- `render_conversation(conv, max_tokens=2048)` → `(ids, mask)`. mask=1은 *어시스턴트가 학습받을* 토큰들. user 메시지·BOS·python output은 mask=0. python 도구 호출 부분은 mask=1 (assistant가 *호출을* 결정해야 하므로) (`tokenizer.py:266-350`).
- `render_for_completion(conv)` — 마지막 assistant 메시지를 제거하고 `<|assistant_start|>`까지만 남겨 RL이나 inference에 prime. (`tokenizer.py:367-385`).

**설계 결정:** 학습은 rust, 추론은 tiktoken — Karpathy는 HuggingFace tokenizers가 "really confusing"하다고 명시했다 (`tokenizer.py:6`). 32K vocab은 작은 모델에서 cross-entropy loss와 lm_head 메모리 모두에 영향. token_bytes(`tok_train.py:79-91`)는 각 토큰이 차지하는 utf-8 바이트 수를 사전계산해 bits-per-byte 평가를 가능하게 한다.

**의존 개념:** BPE (Sennrich et al. 2016), tiktoken, byte-level fallback. → §3 "BPE 토크나이저" 항목.

---

#### `nanochat/gpt.py` — GPT nn.Module

**책임:** Transformer 본체. modded-nanoGPT의 최신 트릭들을 흡수했다.

**핵심 구조 (`gpt.py:154-481`):**
```
tokens → wte (embed) → norm → smear gate
       → for each block:
            x = resid_lambdas[i] * x + x0_lambdas[i] * x0
            x = block(x, value_embedding(idx), cos_sin, window_size, kv_cache)
            if i == n_layer//2: x_backout = x
       → x - backout_lambda * x_backout
       → norm
       → lm_head
       → softcap = 15 * tanh(logits/15)
       → cross_entropy (또는 logits 반환)
```

**중요 시그니처:**
- `GPTConfig(sequence_len=2048, vocab_size=32768, n_layer=12, n_head=6, n_kv_head=6, n_embd=768, window_pattern="SSSL")` (`gpt.py:28-39`)
- `CausalSelfAttention.forward(x, ve, cos_sin, window_size, kv_cache)` (`gpt.py:82-126`) — q/k에 RoPE → QK norm → q,k 둘 다 ×1.2 (sharper attention) → flash_attn (training) or flash_attn_with_kvcache (inference). value embeddings는 절반 layer에만(`has_ve(layer_idx, n_layer)`).
- `MLP` — c_fc → ReLU² (`F.relu(x).square()`) → c_proj. bias 없음 (`gpt.py:129-139`).
- `init_weights()` — 임베딩 std=0.8, lm_head std=0.001 (작게), c_q/c_k/c_v는 Uniform(±√3/√n_embd), c_proj와 mlp.c_proj는 모두 0으로 초기화 (`gpt.py:201-266`). 모델은 *meta 디바이스*에서 init되고 `to_empty(device)` 후 `init_weights()`로 실제 데이터를 채운다 — 큰 모델의 메모리 spike를 피하는 패턴.
- `estimate_flops()` — 6 × (matmul params) + 12hq × effective_seq_len per layer. sliding window를 고려한 PaLM(2204.02311) 공식 (`gpt.py:317-343`).
- `setup_optimizer(unembedding_lr=0.004, embedding_lr=0.2, matrix_lr=0.02, ...)` — param_groups를 7개로 쪼개고 dmodel_lr_scale = (model_dim/768)^-0.5로 AdamW LR을 보정. matrix_params는 shape별로 묶어서 Muon 그룹화 (`gpt.py:374-414`).

**설계 결정과 외부 개념:**
- **RoPE** (Su et al., RoFormer 2021, [arXiv 2104.09864](https://arxiv.org/abs/2104.09864)) — `_precompute_rotary_embeddings(seq_len, head_dim, base=100000)`. base=10000이 GPT/Llama 1세대, 100000이 더 긴 컨텍스트용. nanochat은 100K를 쓴다 (`gpt.py:268-283`).
- **RMSNorm** (Zhang & Sennrich 2019, [arXiv 1910.07467](https://arxiv.org/abs/1910.07467)) — `F.rms_norm(x, (x.size(-1),))`. **learnable param 없음** (`gpt.py:42-43`). layernorm보다 가볍고 작은 모델에서 거의 동등한 성능.
- **QK norm** — q와 k를 RoPE 적용 후 한 번 더 RMSNorm. 출력 변동을 잡아 attention을 안정화 (Henry et al. 2020 / Llama류 차용).
- **ReLU²** (Shazeer 2020 변종) — SwiGLU 대신 채택. 게이트 1개, parameter 적음, 작은 모델에 적합.
- **Value Embeddings (ResFormer)** — 절반 layer마다 별도 embedding을 KV stream에 더한다. 12채널 입력 게이트(`ve_gate`)가 `3 * sigmoid(...)`로 (0,3) 범위 multiplier를 생성 (`gpt.py:91-95`). [#481](https://github.com/karpathy/nanochat/discussions/481)에서 "added ~150M params with near-zero FLOPs"로 인용.
- **Per-layer learnable scalars (resid_lambdas, x0_lambdas)** — 각 layer에서 residual을 얼마나 강하게 흘려보낼지(`1.15→1.05`), 초기 임베딩을 얼마나 다시 섞을지(`0.20→0.05`) 학습되는 스칼라. modded-nanoGPT의 idea (`gpt.py:180-181, 232-239`).
- **Smear** — 이전 토큰의 임베딩을 현재 위치에 섞는 cheap bigram trick. `smear_gate` (24채널 → 1) + `smear_lambda` (`gpt.py:182-184, 432-449`).
- **Backout** — 중간(n_layer//2) 레이어 residual을 cache했다가 최종 norm 직전에 빼서 "low-level feature를 제거" (`gpt.py:185-186, 460-464`).
- **Sliding Window Attention** — window_pattern="SSSL" → S(short, 1/4 context=512), S, S, L(full, 2048). 마지막 layer는 항상 L. SDPA fallback일 때는 효율이 크게 떨어진다(경고 출력) (`gpt.py:285-312`, `base_train.py:114-117`).
- **GQA (Group-Query Attention)** — n_head ≠ n_kv_head일 때 활성화. 현재 speedrun config는 둘이 같다(GQA off), 미니시리즈는 head_dim=128 기준 자동 결정.
- **Logit softcap** = 15 × tanh(logits/15), fp32에서 (Gemma-2식). `loss explosion`을 막는다 (`gpt.py:468-472`).
- **vocab pad to 64배수** — DDP·tensor core를 위해 32,768 → 32,768 (이미 64의 배수). 출력은 forward에서 crop (`gpt.py:166-170, 469-470`).
- **Untied embeddings** — `wte`와 `lm_head`가 별개 weight. Karpathy는 일찍이 weight tying이 작은 모델에서 가성비가 떨어진다고 봤다.

---

#### `nanochat/optim.py` — Muon + AdamW

**책임:** matrix 파라미터에는 Muon, 나머지(embedding, lm_head, scalar)에는 AdamW. 단일 GPU(`MuonAdamW`)와 ZeRO-2 분산(`DistMuonAdamW`) 두 버전.

**핵심:**
- `adamw_step_fused(p, grad, exp_avg, exp_avg_sq, step_t, lr_t, beta1_t, beta2_t, eps_t, wd_t)` — `@torch.compile(dynamic=False, fullgraph=True)` 데코레이터로 single graph. 0-D CPU tensor 인자로 LR을 넘겨서 LR이 step마다 바뀌어도 graph가 재컴파일되지 않음. decoupled weight decay → momentum update → bias correction → param update를 한 그래프에 (`optim.py:21-50`).
- `muon_step_fused(...)` — momentum → Polar Express orthogonalization → variance reduction (NorMuon) → cautious weight decay → param update를 한 fused graph에 (`optim.py:91-148`).

**Muon 알고리즘 (`optim.py:54-130`):**
1. Nesterov momentum: `g = lerp(grad, momentum_buffer, momentum)` (β=0.85→0.97 warmup, 0.97→0.90 warmdown — `base_train.py:372-382`).
2. Polar Express orthogonalization — Newton-Schulz의 개선판. coefficients는 5번 iteration용 quintic polynomial (`optim.py:82-89`). 입력이 tall/wide냐에 따라 `X.mT @ X` 또는 `X @ X.mT` 경로. 결과: `g ≈ U·V^T` (G의 SVD에서 singular value를 다 1로 친). [Polar Express paper 2505.16932](https://arxiv.org/abs/2505.16932).
3. **NorMuon variance reduction** ([arXiv 2510.05491](https://arxiv.org/abs/2510.05491)) — neuron-wise(row/col) adaptive scaling. orthogonalize 후에도 row마다 norm이 들쭉날쭉하므로 factored second moment로 보정.
4. **Cautious weight decay** — `mask = (g * params) >= 0`. update와 *부호가 같은* 파라미터에만 weight decay를 적용 (`optim.py:147-148`). 코사인 스케줄로 0까지 (`base_train.py:385-386`).

**DistMuonAdamW의 3-phase async (`optim.py:299-535`):**
- Phase 1: 모든 그룹에 대해 `reduce_scatter`/`all_reduce` async launch.
- Phase 2: future.wait → 로컬 슬라이스로 update 계산 → `all_gather` launch (이전 update가 끝나기 전에 다음 future를 기다리는 식으로 overlap).
- Phase 3: 모든 gather를 wait, Muon 그룹은 stacked buffer에서 원본 param에 copy back.

AdamW 그룹은 size에 따라 분기: < 1024 elements면 all_reduce(작아서 scatter 안 함), 그 이상은 reduce_scatter+local update+all_gather. Muon은 *parameters per group*을 rank별로 chunk.

**설계 결정:** "no PyTorch DDP" — 자체 분산을 짠다. 이유: optimizer state까지 sharding하려면 PyTorch DDP만으로는 부족(FSDP가 있지만 복잡). 또 Muon은 stacked tensor 위에서 작동하므로 그룹 단위 통신 패턴이 자연스럽다.

**의존 개념:**
- **AdamW** (Loshchilov & Hutter 2017, [arXiv 1711.05101](https://arxiv.org/abs/1711.05101)) — decoupled weight decay.
- **Muon** ([Keller Jordan, 2024](https://kellerjordan.github.io/posts/muon/)) — "MomentUm Orthogonalized by Newton-schulz". 다른 옵티마이저 대비 nanoGPT speedrun에서 ~35% 빠른 수렴 보고됨. Embedding/0,1-D param에는 쓰면 *안 됨* (그래서 split).
- **ZeRO-2** (DeepSpeed ZeRO) — optimizer state sharding.
- **Polar Express** ([2505.16932](https://arxiv.org/abs/2505.16932)) — Newton-Schulz를 quintic + safety factor로 더 빠르게 수렴시킨 변종.
- **NorMuon** ([2510.05491](https://arxiv.org/abs/2510.05491)) — Muon의 per-neuron variance reduction.

---

#### `nanochat/dataloader.py` — BOS-aligned Best-Fit Cropping

**책임:** parquet에서 토큰화한 문서들을 (B, T+1) 텐서 row로 패킹.

**알고리즘 (`dataloader.py:74-161`):**
1. parquet 파일들에서 doc batch를 가져와 토크나이저로 인코드(`<|bos|>` prepend).
2. 버퍼에 doc들을 쌓아둠.
3. 각 row(길이 T+1=2049)에 대해:
   - 버퍼에서 *가장 큰 doc that fits entirely*를 골라 넣는다 (best-fit).
   - 더 못 넣으면 *가장 짧은 doc*을 crop해서 남은 자리 정확히 채운다.
4. 결과 row → inputs(첫 T토큰), targets(둘째 T토큰).

**성격:**
- 모든 row가 BOS로 시작 → 모든 토큰이 BOS까지 attend 가능, 문서 경계가 깨끗.
- 100% utilization (no padding), 대신 약 35% 토큰은 cropping으로 버려짐.
- pinned CPU 버퍼 → 단일 HtoD copy로 효율적.
- distributed: rank별로 다른 row_group을 처리. `resume_state_dict={pq_idx, rg_idx, epoch}`로 정확 재개.

**대안:** 옛 `tokenizing_distributed_data_loader`는 doc 경계 무시하고 토큰을 그냥 이어 붙임. 토큰을 한 톨도 안 버리지만, 한 row에 여러 문서가 끊긴 채 섞여서 "문맥 혼란"이 생긴다. `dataloader.py:10-16`에서 trade-off 명시. midtraining 단계가 필요했던 이유 중 하나는 옛 dataloader의 잡음 보정 — bestfit으로 옮긴 뒤로 midtraining이 별도 단계로 필요 없어졌다(speedrun.sh가 SFT 바로 호출).

`tasks.common.TaskMixture`와 SFT의 `sft_data_generator_bos_bestfit`은 비슷한 best-fit 알고리즘을 conversations에 적용하지만, **cropping이 아니라 padding**(남은 자리에 BOS, target은 -1 ignore_index)을 쓴다. 대화를 토막내면 안 되므로 (`chat_sft.py:187-305`).

---

#### `nanochat/engine.py` — KV-cache 추론 + Tool use FSM

**책임:** prefill → decode 루프, KV-cache 관리, calculator/Python tool 호출.

**핵심:**
- `KVCache(batch_size, num_heads, seq_len, head_dim, num_layers, device, dtype)` — FA3의 `flash_attn_with_kvcache` API에 맞춘 (B, T, H, D) 레이아웃. `cache_seqlens`는 int32, 배치 요소별 위치 추적. `prev_embedding`은 smear용 ((`engine.py:82-138`).
- `Engine.generate(tokens, num_samples, max_tokens, temperature, top_k, seed)` — generator. 한 번의 prefill로 prompt 처리 → `kv_cache.prefill(other_cache)`로 num_samples만큼 KV를 복제 → decode 루프. 각 row가 독립적으로 종료(`<|assistant_end|>` 또는 `<|bos|>`).
- **Tool use FSM:** decode 중에 `<|python_start|>` 토큰을 보면 `in_python_block=True`, 그 사이 토큰을 모았다가 `<|python_end|>`가 나오면 `use_calculator(expr)` 또는 (확장 가능한) 실행기로 평가. 결과를 `<|output_start|> ... <|output_end|>`로 **forced_tokens**에 넣어 *모델이 샘플링한 것처럼* 다음 step에 강제 주입 (`engine.py:255-272`).
- `use_calculator(expr)` — 화이트리스트 기반 safe eval. 숫자/연산자만 있는 식, 또는 `.count(` 메서드 호출만 허용 (SpellingBee 패턴). 5초 timeout (`engine.py:46-79`).

**설계 결정:** Engine은 "tokens in, tokens out"만 안다. 토크나이저는 special token id를 알려주는 용도로만 쓰임. RL 학습 시 mask=1(샘플링)/mask=0(forced/prompt)을 함께 반환해 *모델이 직접 생성한 토큰만* loss에 들어가게 한다(`engine.py:244-249`, `chat_rl.py:130-140`).

**의존 개념:** KV cache, paged attention(미적용), tool augmented LM. `nanochat/execution.py`는 더 무거운 sandbox(HumanEval용)이고 calculator는 가벼운 인라인 eval.

---

#### `nanochat/flash_attention.py` — FA3/SDPA 디스패처

**책임:** Hopper(SM 90, H100)에서는 Flash Attention 3 커널, 그 외에는 PyTorch SDPA fallback. API는 FA3와 동일.

**핵심:**
- `_load_flash_attention_3()` — `kernels` 라이브러리로 `varunneal/flash-attention-3`을 가져옴. SM이 9.x가 *아니면* None 반환 (Ada=8.9, Blackwell=10.x는 SDPA로 떨어진다 — FA3는 sm90만 컴파일됨) (`flash_attention.py:23-38`).
- `flash_attn_func(q, k, v, causal, window_size)` — training용. FA3 native layout (B, T, H, D). SDPA fallback은 (B, H, T, D)로 transpose.
- `flash_attn_with_kvcache(q, k_cache, v_cache, k, v, cache_seqlens, causal, window_size)` — inference. FA3는 cache를 in-place 업데이트.

**중요한 trade-off:** FA3는 *bf16 또는 fp8만 지원*. fp16/fp32 학습은 SDPA 강제. SDPA에서 sliding window는 explicit mask로 구현해야 해서 효율이 크게 떨어진다 → `base_train.py:114-117`에서 사용자가 fp16/fp32 + sliding window 조합을 쓰면 "GPU utilization will be terrible" 경고.

**의존 개념:** FlashAttention (Dao et al. 2022, [arXiv 2205.14135](https://arxiv.org/abs/2205.14135)), FlashAttention 2/3. PyTorch SDPA는 표준 `F.scaled_dot_product_attention`.

---

#### `nanochat/fp8.py` — 자체 미니 FP8 학습

**책임:** torchao의 `Float8Linear`(~2000줄)를 ~150줄로 단순화. tensorwise dynamic scaling만 지원.

**원리 (`fp8.py:8-31`):**
```
Linear forward:   out  = input @ weight.T
Linear backward:  d_in = d_out @ weight
                  d_w  = d_out.T @ input
```
세 matmul 각각을 FP8로 감싼다:
1. `scale = FP8_MAX / max(|tensor|)` (tensorwise = 텐서 전체 1 스칼라)
2. `fp8_tensor = clamp(tensor * scale, ±FP8_MAX).to(fp8)`
3. `torch._scaled_mm`(cuBLAS FP8 kernel) — bf16 대비 ~2× 빠름
4. dequantize는 `_scaled_mm`이 inverse scale로 내부 처리

**FP8 dtype 선택:**
- `float8_e4m3fn` (exp 4, mantissa 3, range [-448, 448]) — input/weight (정밀도 우선)
- `float8_e5m2` (exp 5, mantissa 2, range [-57344, 57344]) — gradient (range 우선)

**주요 클래스 (`fp8.py:125-227`):**
- `_Float8Matmul(torch.autograd.Function)` — `@torch._dynamo.allow_in_graph`로 torch.compile에서 opaque node로 취급. forward/backward 각각 _scaled_mm 호출 3개.
- `Float8Linear(nn.Linear)` — `_Float8Matmul.apply(input_2d, self.weight)`로 forward.
- `convert_to_float8_training(model, config, module_filter_fn)` — 모든 nn.Linear를 Float8Linear로 swap (weight·bias share).

**활성화 조건 (`base_train.py:167-192`):** `--fp8` 플래그 + CUDA. 16의 배수 차원 + min(in,out) ≥ 128인 Linear만 변환. 평가 중에는 `disable_fp8` 컨텍스트 매니저로 일시적으로 nn.Linear로 swap back(`base_train.py:194-240`).

**기여:** [#481](https://github.com/karpathy/nanochat/discussions/481) 리더보드 #2에서 d26 + fp8로 2.91h, val_bpb 0.74504, CORE 0.2578 달성. fp8은 small/medium 모델에서는 큰 이득이 없지만 d24+에서는 의미 있다.

**의존 개념:** FP8 학습 (Micikevicius et al., NVIDIA Transformer Engine), [Float8 paper](https://arxiv.org/abs/2209.05433). torchao tensor subclass 방식 vs nanochat의 single autograd.Function 방식의 trade-off는 docstring(`fp8.py:43-69`)에 자세히.

---

#### `nanochat/core_eval.py` — DCLM CORE 22-task 평가

**책임:** base model을 ICL(in-context learning) 22개 task에서 평가. accuracy → centered_result → 22개 mean = CORE metric.

**작동:**
- `eval_bundle.zip`을 다운로드, `core.yaml`에서 task 목록을 읽음 ([`base_eval.py:92-117`](path)).
- 각 task에 대해 task_type ∈ {multiple_choice, schema, language_modeling} 분기 (`core_eval.py:182-241`).
- few-shot example들을 random sample (seed=1234+idx) — `evaluate_example`이 idx마다 deterministic.
- 한 sequence의 각 위치에서 cross-entropy loss를 구해 (`forward_model`, `core_eval.py:144-164`), 정답 옵션의 평균 loss가 최소인지 비교.
- DDP에서는 stride로 example 분산 처리, `all_reduce(SUM)`으로 결과 통합.
- `centered_result = (acc - 0.01 * random_baseline) / (1.0 - 0.01 * random_baseline)` — random chance를 0으로 정규화(`base_eval.py:162`).

**왜 CORE인가:** [DataComp-LM 논문 (Li et al. 2024, arXiv 2406.11794)](https://arxiv.org/abs/2406.11794)이 정한 22개 ICL task의 centered mean. random은 0, perfect는 1. GPT-2 (1.6B)의 reference CORE = 0.256525. 작은 base model에서도 안정적이고 신호가 약하지 않다(reading comprehension, commonsense, world knowledge 골고루).

**참고:** speedrun config는 `--core-metric-every=2000`, `--core-metric-max-per-task=500`로 학습 중간에도 평가. 평가 비용이 들어 default는 sample 수를 제한한다.

---

#### `nanochat/loss_eval.py` — bits per byte

**책임:** vocab-size-invariant한 loss 지표.

**공식:** `bpb = total_nats / (log(2) * total_bytes)`. `total_nats`는 valid 토큰의 cross-entropy 합. `total_bytes`는 각 target token이 utf-8로 차지하는 바이트 수의 합 (special token은 0) (`loss_eval.py:60-65`).

**왜 필요한가:** vocab을 바꾸면 평균 cross-entropy도 자동으로 바뀐다(어휘가 작아질수록 토큰당 정보량이 줄어 loss가 작아 보일 수 있음). bpb는 *바이트당 비트*로 정규화하므로 vocab_size 16K vs 32K vs 100K를 그대로 비교할 수 있다.

`token_bytes`는 토크나이저 학습 직후에 사전계산해서 `tokenizer/token_bytes.pt`로 저장 (`tok_train.py:79-91`).

speedrun #5 baseline: val_bpb = 0.74833 (d24, [#481](https://github.com/karpathy/nanochat/discussions/481)). 이 수치는 책 본문에서 학습 진척의 hard metric으로 인용 가능.

---

#### `nanochat/checkpoint_manager.py` — ckpt save/load

- 모델은 rank 0이 `model_{step:06d}.pt`로 저장 (state_dict 단일 파일).
- 옵티마이저는 *rank별로* shard를 저장 (`optim_{step:06d}_rank{rank:d}.pt`).
- 메타데이터는 JSON. user_config(argparse args), model_config, dataloader_state_dict, loop_state 등.
- `find_largest_model(checkpoints_dir)` — 디렉토리에서 `d{number}` 패턴 중 가장 큰 것을 자동 선택 (`checkpoint_manager.py:118-135`).
- `_patch_missing_keys` — 옛 체크포인트에 `resid_lambdas`/`x0_lambdas`가 없으면 1/0으로 채워넣음(아키텍처 변천 흡수, `checkpoint_manager.py:30-40`).

---

#### `scripts/base_train.py` — 사전학습

**기본 흐름:**
1. argparse → wandb init → DDP/MFU/COMPUTE_DTYPE 출력.
2. tokenizer, token_bytes 로드.
3. `build_model_meta(depth)` → meta device에 모델 생성 → `to_empty(device)` → `init_weights()`.
4. (선택) FP8 변환.
5. `torch.compile(model, dynamic=False)`.
6. **Scaling laws 기반 hyperparameter 자동 결정** (`base_train.py:248-316`):
   - `target_tokens = target_param_data_ratio * num_scaling_params` (default 12:1; Chinchilla 20보다 작음 — Muon이 더 효율적이라는 경험적 보정).
   - `B_REF = 2^19 = 524288` tokens at d12.
   - `predicted_batch_size = B_REF * (target_tokens/D_REF)^0.383` (Power Lines paper [2505.13738](https://arxiv.org/abs/2505.13738)).
   - LR scale ∝ √(B/B_ref).
   - weight_decay scale = base × √(B/B_ref) × (D_ref/D) (T_epoch framework [2405.13698](https://arxiv.org/abs/2405.13698)).
7. data loader 초기화 → 첫 batch prefetch.
8. LR 스케줄: linear warmup 40 → constant → linear warmdown(warmdown_ratio=0.65) to final_lr_frac=0.05.
9. Muon momentum: 0.85→0.97 first 400 steps, 0.97→0.90 during warmdown.
10. weight_decay: cosine to zero.
11. 학습 루프: grad_accum_steps만큼 forward/backward → optimizer step → wandb log → 가끔 eval/sample/checkpoint.

**가비지 컬렉터 트릭 (`base_train.py:586-594`):** 첫 step 후 `gc.collect(); gc.freeze(); gc.disable()`. 5000 step마다만 수동 collect. GC가 ~500ms씩 잡아먹는 걸 방지.

**speedrun config:**
- `--depth=24 --target-param-data-ratio=8 --device-batch-size=16 --fp8` 
- ratio 8은 "약간 undertrained"되지만 wall-clock을 줄이려는 의도.

**runcpu config:**
- `--depth=6 --head-dim=64 --window-pattern=L --max-seq-len=512 --device-batch-size=32 --total-batch-size=16384 --num-iterations=5000`
- M3 Max에서 약 30분.

---

#### `scripts/chat_sft.py` — 지도 미세조정

**데이터 믹스 (`chat_sft.py:163-180`):**
```python
SmolTalk(train)                  # 460K rows, 일반 대화
CustomJSON(identity)             # 1000 rows × 2 epochs (oversample)
MMLU(auxiliary_train) × 3 epochs # 100K/epoch, multiple choice
GSM8K(train) × 4 epochs          # 8K/epoch, 수학 + 도구
SimpleSpelling(size=200K)        # spelling
SpellingBee(size=80K)            # counting letters
```
`TaskMixture`는 deterministic shuffle 후 인덱싱.

**손실 마스킹:** `render_conversation`이 어시스턴트 답변과 tool call에는 mask=1, 그 외(user, BOS, python output, padding)에는 mask=0. `targets[mask==0] = -1` (ignore_index). 따라서 모델은 "어시스턴트가 어떻게 답해야 하는지"만 학습.

**LR 스케줄:** init_lr_frac=0.8 (pretrain 끝값이 거의 0이므로 다시 LR을 키움), warmdown_ratio=0.5, final 0.

**평가:** `ChatCORE` = 6개 task의 centered accuracy 평균 (`chat_sft.py:366-396`). 각 task의 baseline accuracy(`{ARC-Easy: 0.25, GSM8K: 0.0, ...}`)를 빼고 (1-baseline)로 정규화.

**옵티마이저 warm-start:** pretraining의 optimizer state(특히 Muon momentum buffer)를 로드해서 시작. 단 LR은 reset (`chat_sft.py:141-149`).

---

#### `scripts/chat_rl.py` — REINFORCE-ish ("GRPO")

Karpathy의 명시: "I put GRPO in quotes because we actually end up with something a lot simpler and more similar to just REINFORCE" (`chat_rl.py:3-11`).

**무엇을 *안* 하는가:**
1. KL regularization to reference model — *없음* (no trust region)
2. PPO ratio + clip — *없음* (on-policy니까)
3. z-score advantage `(r-μ)/σ` — 아니고 그냥 `r - μ`
4. sequence-level normalization — 아니고 token-level (DAPO 스타일)

**작동 (`chat_rl.py:85-146, 220-301`):**
1. `engine.generate_batch(prompt_tokens, num_samples=16, temperature=1.0, top_k=50, ...)` — 한 GSM8K 문제에 16개 답안을 샘플링.
2. 각 답안에 대해 `gsm8k.reward(conv, response)` = 정답 일치 시 1.0, 아니면 0.0.
3. `advantages = rewards - rewards.mean()`.
4. `logp = -model(inputs, targets, loss_reduction='none')` — 토큰별 log-prob.
5. `pg_obj = (logp * advantages.unsqueeze(-1)).sum() / num_valid_tokens / num_passes / examples_per_rank`.
6. `loss = -pg_obj` → backward.
7. eval은 pass@k (k=1..device_batch_size) on GSM8K test.

**대상 task:** 현재 GSM8K만. tool use가 있는 도메인이라서 보상 신호가 깨끗.

**의존 개념:** REINFORCE (Williams 1992), PPO (Schulman 2017), GRPO (DeepSeek), DAPO 토큰 정규화. nanochat 구현은 이 중 PPO의 ratio/clip을 빼고 KL도 빼서 minimalist. 작은 모델에서는 *데이터셋 multiplexing이 RL보다 비용 대비 효과*가 더 크다는 입장(speedrun에는 RL 안 포함됨).

---

#### `scripts/chat_cli.py` / `scripts/chat_web.py` — 인터페이스

**CLI (`chat_cli.py`):** 단순 REPL. 사용자 입력을 `<|user_start|>...<|user_end|>`로 감싸고 `<|assistant_start|>` 토큰을 prime → `engine.generate(conversation_tokens, ...)` 스트림을 `print(..., end="", flush=True)`. 'clear'로 새 대화, 'quit'/'exit'로 종료. `-p`로 단일 응답.

**Web (`chat_web.py`):** FastAPI. `/chat/completions`는 SSE 스트림. abuse 방지로 메시지 ≤ 500개, 메시지당 ≤ 8000자, 전체 ≤ 32000자, temperature [0,2], top_k [0,200], max_tokens [1,4096]. `WorkerPool`에 GPU 수만큼 모델을 로드하고 asyncio.Queue로 round-robin. 다중 사용자 동시 처리.

UTF-8 멀티바이트 토큰 처리(`chat_web.py:285-301`): replacement character(`�`)가 끝에 있으면 yield하지 않고 다음 토큰까지 누적. 이모지/한글이 깨지지 않게.

---

#### `runs/speedrun.sh` — 풀 파이프라인 (8XH100, ~3시간, ~$48~$92)

```bash
# 1) Setup
uv sync --extra gpu && source .venv/bin/activate

# 2) Report header
python -m nanochat.report reset

# 3) Tokenizer (~2B chars / 8 shards download → train → eval)
python -m nanochat.dataset -n 8
python -m nanochat.dataset -n 170 &        # 백그라운드로 추가 셰드
python -m scripts.tok_train               # vocab 32768
python -m scripts.tok_eval                # GPT-2/4 대비 compression

# 4) Pretrain
torchrun --standalone --nproc_per_node=8 -m scripts.base_train -- \
    --depth=24 --target-param-data-ratio=8 \
    --device-batch-size=16 --fp8 --run=$WANDB_RUN
torchrun --standalone --nproc_per_node=8 -m scripts.base_eval -- --device-batch-size=16

# 5) SFT
curl -L -o $NANOCHAT_BASE_DIR/identity_conversations.jsonl \
    https://karpathy-public.s3.us-west-2.amazonaws.com/identity_conversations.jsonl
torchrun --standalone --nproc_per_node=8 -m scripts.chat_sft -- --device-batch-size=16 --run=$WANDB_RUN
torchrun --standalone --nproc_per_node=8 -m scripts.chat_eval -- -i sft

# 6) (talk to it)
# python -m scripts.chat_cli -p "Why is the sky blue?"
# python -m scripts.chat_web

# 7) Report
python -m nanochat.report generate
```

#### `runs/runcpu.sh` — CPU/MPS 데모 (M3 Max에서 ~40분 토탈)

`--extra cpu` → d6 모델, max_seq_len=512, window_pattern=L, 5K steps pretrain → 1500 steps SFT. CORE 평가는 비활성화(`--core-metric-every=-1`). 결과 품질은 낮지만 코드 경로를 다 밟아볼 수 있다.

### 2.3 데이터 흐름 다이어그램 (텍스트)

```
FineWeb parquets ──► dataset.py (download/iter) ──► tokenizer (rustbpe train)
                                                          │
                                                          ▼
                                                   tokenizer.pkl + token_bytes.pt
                                                          │
                ┌─────────────────────────────────────────┤
                ▼                                         │
       dataloader (BOS-aligned bestfit-crop)              │
                │                                         │
                ▼                                         │
       GPT (meta init → to_empty → init_weights)          │
       MuonAdamW (Muon for matrices, AdamW for rest)      │
                │                                         │
                ▼                                         │
       base_train loop:                                   │
         forward/backward → optimizer step                │
         eval (val_bpb, CORE) every N steps               │
         sample every N steps                             │
                │                                         │
                ▼                                         │
       base_checkpoints/d24/model_{step}.pt               │
                │                                         │
                ▼                                         │
       SmolTalk + GSM8K + MMLU + identity + SpellingBee   │
            ──► TaskMixture                               │
                │                                         │
                ▼                                         │
       chat_sft (BOS-aligned bestfit-pad)                 │
                │                                         │
                ▼                                         │
       chatsft_checkpoints/d24/                           │
                │                                         │
                ├──► chat_rl (GSM8K rollouts)             │
                │     → chatrl_checkpoints/d24/           │
                │                                         │
                └──► Engine (KVCache + tool FSM)          │
                       ├──► chat_cli                      │
                       └──► chat_web (FastAPI + ui.html)  │
                                                          │
       report.md ◄── nanochat/report.py ◄─────────────────┘
```

---

## 3. 코드가 의존하는 외부 개념

각 항목마다: **정의 / 정설 / 코드 어디서 어떻게 구현되는가 / 인용용 라인**.

### 3.1 Transformer / Self-Attention

**정설:** Vaswani et al., "Attention Is All You Need" (NeurIPS 2017, [arXiv 1706.03762](https://arxiv.org/abs/1706.03762)). Q·K·V → softmax(QK^T/√d_k) → V로 가중 합산. Multi-head로 d_model을 h개로 쪼개서 병렬 attention. Encoder-decoder 구조에서 후에 GPT-2/3에서는 **decoder-only causal LM**으로 단순화.

**nanochat:** `CausalSelfAttention` (`gpt.py:65-126`). decoder-only, causal mask. 큰 차이점들:
- positional encoding이 sinusoidal/learned가 아니라 **RoPE**.
- normalization이 LN이 아니라 **RMSNorm**.
- bias 없음, lm_head는 untied, MLP는 SwiGLU/GELU 대신 **ReLU²**.

### 3.2 RoPE (Rotary Positional Embedding)

**정설:** Su et al., "RoFormer: Enhanced Transformer with Rotary Position Embedding" (2021, [arXiv 2104.09864](https://arxiv.org/abs/2104.09864)). Q, K 벡터를 *복소 평면에서 회전*시켜 position을 인코딩. 두 위치 m, n의 dot product가 (m-n)에만 의존 — 상대 위치 정보가 자연스럽게 들어감. Llama, Mistral, GPT-NeoX 등 거의 모든 현대 LLM이 채택.

**nanochat:** `_precompute_rotary_embeddings(seq_len, head_dim, base=100000)` (`gpt.py:268-283`). 채널을 2개씩 묶어 `(x1, x2) → (x1*cos - x2*sin, x1*sin + x2*cos)` 회전. `apply_rotary_emb(x, cos, sin)` (`gpt.py:57-63`). base=10000 (원전)이 아니라 **100000**을 쓴다 — 더 긴 컨텍스트를 일반화하기 위함.

### 3.3 RMSNorm

**정설:** Zhang & Sennrich, "Root Mean Square Layer Normalization" (NeurIPS 2019, [arXiv 1910.07467](https://arxiv.org/abs/1910.07467)). LayerNorm = (x - μ)/σ × γ + β. RMSNorm = x / RMS(x) × γ (mean centering 생략, bias 생략). 90%의 효과를 30%의 비용으로.

**nanochat:** `def norm(x): return F.rms_norm(x, (x.size(-1),))` (`gpt.py:42-43`). **learnable γ도 없다** (`gpt.py:9` 주석). 작은 모델에서는 γ가 사실상 1에 머무는 경향이 있어서 통째로 제거. attn 직전·MLP 직전·lm_head 직전 + Q, K에 추가로 한번 더(QK norm).

### 3.4 SwiGLU vs ReLU²

**정설:** Shazeer, "GLU Variants Improve Transformer" (2020, [arXiv 2002.05202](https://arxiv.org/abs/2002.05202)). SwiGLU = (Swish(xW) ⊙ (xV))W2. parameter 1.5×, FLOPs 1.5×. Llama가 채택해서 사실상 표준.

**nanochat:** ReLU² = `F.relu(x).square()` (`gpt.py:135-139`). c_fc → ReLU → square → c_proj. 게이트가 없으니 parameter는 그대로 4× hidden. So et al., "Primer" (2021)에서 ReLU²이 GELU와 비슷하거나 약간 낫다고 보고했고, modded-nanoGPT가 채택 후 nanochat이 그대로 가져옴. 작은 모델 친화적.

### 3.5 BPE 토크나이저

**정설:** Sennrich, Haddow & Birch, "Neural Machine Translation of Rare Words with Subword Units" (ACL 2016, [arXiv 1508.07909](https://arxiv.org/abs/1508.07909)). 가장 빈번한 byte pair를 반복적으로 merge해 vocab을 생성. OOV 문제 해소.

**nanochat:** 두 구현(`tokenizer.py`):
- `HuggingFaceTokenizer` — 학습/추론 모두 HF tokenizers. 디버그·복잡함.
- `RustBPETokenizer` — Karpathy의 rustbpe로 학습 + tiktoken으로 추론. 운영 default.

특이점: `SPLIT_PATTERN`이 GPT-4 정규식의 `\p{N}{1,3}` → `\p{N}{1,2}`. 작은 vocab에서 숫자에 토큰을 덜 낭비. `tok_eval.py`가 GPT-2(50K)·GPT-4(100K)·ours(32K)의 compression ratio를 비교 (Karpathy 보고: FineWeb 텍스트에서 4.8× compression — [#481](https://github.com/karpathy/nanochat/discussions/481)).

**도구 호출용 special token**이 토크나이저 단에 박혀 있는 게 핵심 디자인 결정. tokenizer가 모델보다 먼저 정해지므로 도구 사용을 *나중에 추가*하기 어렵다는 점은 책에서 한 번 짚어줄 만하다.

### 3.6 AdamW + Muon (split optimizer)

**AdamW (정설):** Loshchilov & Hutter, "Decoupled Weight Decay Regularization" (ICLR 2019, [arXiv 1711.05101](https://arxiv.org/abs/1711.05101)). Adam = bias-corrected EMA of gradients & squared gradients. AdamW = weight decay를 update에서 분리.

**Muon (정설):** [Keller Jordan, 2024 blog post](https://kellerjordan.github.io/posts/muon/). MomentUm Orthogonalized by Newton-schulz. 2D 행렬 파라미터 W의 update를 SGD-momentum으로 모은 뒤 *직교화* — Newton-Schulz iteration으로 SVD U·V^T를 근사. modded-nanoGPT에서 NanoGPT (124M)를 90초만에 학습시키는 데 핵심 역할.

**왜 split:**
- Muon은 행렬에만 적합. 0/1-D (스칼라/임베딩)에 쓰면 의미 없음.
- 임베딩과 lm_head는 sparsity가 크고 row마다 update 강도가 매우 다름 → AdamW가 자연스러움.

**nanochat:** 7개 param group (`gpt.py:393-401`). embedding/lm_head/value_embeds/resid_lambdas/x0_lambdas/smear/matrices. matrices는 shape별로 묶음(stacking을 위해). 위 §2.2 `optim.py` 항목에서 상세.

### 3.7 Chinchilla Scaling Laws

**정설:** Hoffmann et al., "Training Compute-Optimal Large Language Models" (NeurIPS 2022, [arXiv 2203.15556](https://arxiv.org/abs/2203.15556)). 70M ~ 16B 모델 400+개 학습 결과: **고정 compute budget에서 optimal은 model_size × 20 ≈ tokens**. GPT-3 (175B, 300B tokens)는 *심하게 undertrained*였다(이상은 약 3.5T tokens).

**nanochat:** `--target-param-data-ratio` default = **12** (Chinchilla 20보다 작음). Karpathy의 이유:
- Muon이 AdamW보다 sample-efficient → 더 적은 토큰으로 충분.
- 속도 우선의 speedrun(d24)은 8까지 내림 (`speedrun.sh:73`).
- 미니시리즈 v1([#420](https://github.com/karpathy/nanochat/discussions/420))은 **8:1**로 보고.

`get_scaling_params(model)` = transformer matrices + lm_head (embedding 제외, Kaplan 스타일과 Chinchilla 사이의 절충) (`base_train.py:263-274`). Power Lines paper의 `Bopt ∝ D^0.383`로 batch_size도 자동 조정.

### 3.8 FlashAttention

**정설:** Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness" (NeurIPS 2022, [arXiv 2205.14135](https://arxiv.org/abs/2205.14135)). attention을 tile 단위로 처리하고 softmax를 online으로 계산 → HBM ↔ SRAM traffic 감소. wall-clock 2-4× 빠름. FlashAttention 2(2023)는 work partitioning 개선. FlashAttention 3(2024)는 Hopper TMA/WGMMA 활용으로 H100에서 더 빠름.

**nanochat:** `flash_attention.py`의 디스패처. **FA3는 Hopper SM90 + bf16/fp8만 지원** — 사용자가 Ada/Blackwell이거나 fp16/fp32라면 자동 SDPA fallback (성능 떨어짐). [#481](https://github.com/karpathy/nanochat/discussions/481): FA3 도입으로 ~9% tok/sec 향상.

### 3.9 FP8 Training

**정설:** Micikevicius et al., "FP8 Formats for Deep Learning" (2022, [arXiv 2209.05433](https://arxiv.org/abs/2209.05433)). NVIDIA H100이 도입한 8-bit float. 두 포맷: E4M3 (정밀도) / E5M2 (range). 학습 중에 input/weight는 E4M3, gradient는 E5M2. dynamic per-tensor scaling으로 overflow 방지. bf16 대비 ~2× 빠른 matmul.

**nanochat:** `nanochat/fp8.py`. torchao의 ~2000줄 대신 ~150줄 자체 구현. tensorwise scaling만 지원. `torch._scaled_mm`(cuBLAS FP8 kernel)을 직접 호출. weight 자체는 fp32 유지하고 matmul 시점에만 quantize.

### 3.10 KV cache 추론

**정설:** Transformer inference에서 t 시점에 새 토큰을 생성할 때, t-1까지의 K·V는 변하지 않으므로 cache. prefill(prompt 전체를 한 번에) + decode(토큰 한 개씩) 두 phase. 큰 모델일수록 KV cache가 메모리 병목.

**nanochat:** `KVCache` (`engine.py:82-138`) — pre-allocated `(n_layers, B, T_max, n_kv_heads, head_dim)` 텐서. `cache_seqlens` (int32, per-batch). FA3의 `flash_attn_with_kvcache`가 in-place 업데이트. `prefill()` 메서드로 batch=1 prefill 후 num_samples로 broadcast (RL/parallel sampling용).

### 3.11 평가 벤치마크

#### CORE
- **정의:** DCLM 논문의 22개 ICL task centered accuracy 평균. `centered = (acc - 0.01·random_baseline) / (1 - 0.01·random_baseline)`.
- **GPT-2 reference:** 0.256525 (1.6B 파라미터, 168시간 학습, 2019). [README](https://github.com/karpathy/nanochat#time-to-gpt-2-leaderboard).
- **속한 task들:** reading comprehension, commonsense, world knowledge 류 (ARC, HellaSwag, LAMBADA, PIQA, SciQ, WinoGrande, ... — 정확 목록은 eval_bundle/core.yaml에). 정답이 단답인 multiple choice / schema / language modeling 3가지 유형.
- **언제 쓰는가:** base model 평가. SFT 후에는 chatcore.

#### bits-per-byte
- **정의:** `loss / (log(2) · bytes)`. vocab-size에 invariant.
- **언제 쓰는가:** train/val 둘 다. wandb의 `val/bpb`.

#### MMLU
- Hendrycks et al. 2021, [arXiv 2009.03300](https://arxiv.org/abs/2009.03300). 57개 학문 분야의 4지선다 14K test + 100K auxiliary_train. base model 평가용으로는 CORE 안에 포함, SFT에서는 별도 task로 학습+평가 (`tasks/mmlu.py`).
- nanochat은 `render_mc`로 `Multiple Choice question: ...\n- choice=A\n- choice=B\n...\n\nRespond only with the letter`. choice→letter 매핑 순서가 작은 모델에서는 중요(공백·token 경계 트릭).

#### ARC-Easy / ARC-Challenge
- Clark et al. 2018, [arXiv 1803.05457](https://arxiv.org/abs/1803.05457). 초·중등 과학 4지선다.

#### GSM8K
- Cobbe et al. 2021, [arXiv 2110.14168](https://arxiv.org/abs/2110.14168). 초등 grade school math 8K. solution이 자연어 + `<<expr=result>>` 계산기 호출. nanochat의 `tasks/gsm8k.py`가 이 `<<>>`를 파싱해서 `{"type":"python","text":expr}`와 `{"type":"python_output","text":result}` 파트로 변환 — **자연스럽게 calculator tool use 학습**. `extract_answer`는 `#### N` 패턴.
- chat_rl 의 유일한 task. reward = 답 일치 시 1.0.

#### HumanEval
- Chen et al. 2021, [arXiv 2107.03374](https://arxiv.org/abs/2107.03374). 코드 생성. nanochat에서는 `nanochat/execution.py`의 sandbox로 생성한 코드를 실제로 실행해 unit test 통과 여부 평가. README의 SpellingBee와 함께 ChatCORE 6개 task에 들어감.

#### ChatCORE
- nanochat 자체 정의 (`chat_sft.py:382-396`). ARC-Easy/Challenge/MMLU/GSM8K/HumanEval/SpellingBee의 centered accuracy 평균. baseline은 각각 {0.25, 0.25, 0.25, 0.0, 0.0, 0.0}. CORE가 base 모델용이면, ChatCORE는 SFT 이후 chat 모델용.

### 3.12 chat_rl.py가 쓰는 RL 알고리즘

코드 확인 결과: **vanilla REINFORCE에 가까운, *advantage = reward - mean reward*만 적용한 단순화된 policy gradient**. Karpathy가 "GRPO"라고 부르지만:
- KL penalty 없음
- PPO ratio·clip 없음 (on-policy니까)
- token-level normalization (DAPO 스타일)
- importance sampling 없음

각 GSM8K 질문에 대해 num_samples=16 답안을 만들고, advantage를 빼고, log-prob × advantage로 surrogate objective. → 보고된 결과로는 GSM8K pass@1을 끌어올리는 데 효과적.

**의존 개념:**
- REINFORCE (Williams 1992)
- PPO (Schulman et al. 2017, [arXiv 1707.06347](https://arxiv.org/abs/1707.06347))
- GRPO (DeepSeek-Math 2024, [arXiv 2402.03300](https://arxiv.org/abs/2402.03300)) — Group Relative Policy Optimization. nanochat은 group의 mean만 빼는 부분만 차용.
- DAPO (2025, ByteDance) — 토큰 정규화 아이디어.

---

## 4. 실습 시나리오

### 4.1 CPU/MPS 미니 학습 (M3 Max ~40분)

`runs/runcpu.sh`의 단계:

```bash
export NANOCHAT_BASE_DIR="$HOME/.cache/nanochat"
uv sync --extra cpu && source .venv/bin/activate

# (1) 데이터 셰드 8개 (~800MB)
python -m nanochat.dataset -n 8

# (2) 토크나이저 학습 (~34초 on M3 Max)
python -m scripts.tok_train --max-chars=2000000000
python -m scripts.tok_eval

# (3) d6 pretrain (~30분)
python -m scripts.base_train \
    --depth=6 --head-dim=64 \
    --window-pattern=L \
    --max-seq-len=512 \
    --device-batch-size=32 --total-batch-size=16384 \
    --eval-every=100 --eval-tokens=524288 \
    --core-metric-every=-1 \
    --sample-every=100 \
    --num-iterations=5000
python -m scripts.base_eval --device-batch-size=1 --split-tokens=16384 --max-per-task=16

# (4) SFT (~10분)
curl -L -o $NANOCHAT_BASE_DIR/identity_conversations.jsonl \
    https://karpathy-public.s3.us-west-2.amazonaws.com/identity_conversations.jsonl
python -m scripts.chat_sft \
    --max-seq-len=512 --device-batch-size=32 --total-batch-size=16384 \
    --eval-every=200 --eval-tokens=524288 \
    --num-iterations=1500

# (5) chat
python -m scripts.chat_cli -p "What is the capital of France?"
```

**산출 경로:** `~/.cache/nanochat/`:
- `tokenizer/tokenizer.pkl`, `tokenizer/token_bytes.pt`
- `pretrain_data/*.parquet` (FineWeb 셰드)
- `base_checkpoints/d6/model_005000.pt`, `meta_005000.json`, `optim_005000_rank0.pt`
- `chatsft_checkpoints/d6/...`
- `report/header.md, tokenizer-training.md, base-model-training.md, ...`

**기대 품질:** 매우 낮음. README는 "model should be able to say that it is Paris. It might even know that the color of the sky is blue. Sometimes the model likes it if you first say Hi before you ask it questions." 정성 시연용.

**왜 CORE를 끄나:** `--core-metric-every=-1`. d6에서는 CORE 신호가 너무 약해 시간만 잡아먹는다.

### 4.2 8XH100 풀 스피드런 (~$48, ~3시간)

`runs/speedrun.sh` 그대로. 위 §2.2 speedrun config 참조. 주요 산출:

1. **Tokenizer report:** GPT-2/4 대비 압축률.
2. **Pretrain report:** val_bpb ≈ 0.745, CORE ≈ 0.258, MFU ~50%.
3. **SFT report:** ChatCORE, ARC-Easy ~0.39, MMLU ~0.32, GSM8K ~0.05 ([#1](https://github.com/karpathy/nanochat/discussions/1) 인용).
4. **Final `report.md`** — 헤더(GPU·시간·git commit·bloat metrics) + 각 단계 + Summary 테이블.

**리더보드 우승 디테일** (Feb 2026 #5 [autoresearch round 1](https://github.com/karpathy/nanochat/discussions/481)):
- 1.80h, val_bpb 0.71808, CORE 0.2690 — GPT-2를 *짧은 시간에* 능가.
- 누적된 개선들: FP8, batch 1M tokens, ClimbMix 데이터셋 전환, hyperparameter sweep (320개 실험!), Polar Express, NorMuon, cautious WD, value embeddings, smear, backout.

**런타임에 wandb로 보는 그래프:**
- `val_bpb` vs `step`, `total_training_time`, `total_training_flops`
- `core_metric`
- `train/mfu` (목표: H100에서 50%+)
- `train/tok_per_sec`
- VRAM utilization

### 4.3 산출물 위치 정리

| 무엇 | 어디 | 누가 만드나 |
|------|------|------------|
| 토크나이저 | `$NANOCHAT_BASE_DIR/tokenizer/{tokenizer.pkl, token_bytes.pt}` | `tok_train.py` |
| Pretrain 데이터 | `$NANOCHAT_BASE_DIR/pretrain_data/*.parquet` | `nanochat.dataset` |
| Base ckpt | `base_checkpoints/d{depth}/model_*.pt + meta_*.json + optim_*_rank*.pt` | `base_train.py` |
| SFT ckpt | `chatsft_checkpoints/d{depth}/...` | `chat_sft.py` |
| RL ckpt | `chatrl_checkpoints/d{depth}/...` | `chat_rl.py` |
| Identity 합성 데이터 | `$NANOCHAT_BASE_DIR/identity_conversations.jsonl` | `dev/gen_synthetic_data.py` |
| Eval bundle | `$NANOCHAT_BASE_DIR/eval_bundle/` | `base_eval.py`가 자동 다운로드 |
| 학습 리포트 | `$NANOCHAT_BASE_DIR/report/*.md` → `./report.md` | `nanochat.report` |
| wandb 로그 | https://wandb.ai (project: nanochat, nanochat-sft, nanochat-rl) | 학습 스크립트 |

---

## 5. 평가

### 5.1 CORE score가 왜 GPT-2 capability의 기준인가

DCLM([2406.11794](https://arxiv.org/abs/2406.11794))은 *동일한 평가 프로토콜* 안에서 다양한 모델/데이터의 성능을 비교하려는 testbed다. CORE는 그 안에서 22개 task의 **centered accuracy 평균**으로 정의된다. centered = (accuracy - random baseline) / (1 - random baseline). 따라서:
- random chance만 맞히면 0.
- 모두 맞히면 1.
- 평균이라 한두 task 운에 흔들리지 않음.

GPT-2 1.6B (XL)의 reference는 0.256525. nanochat의 README는 이 점수를 *기준선*으로 두고 "time to GPT-2"를 우승 지표로 삼는다. base 모델의 *raw capability*가 SFT 이후 정성적 chat 품질의 *상한*을 거의 결정하기 때문에 base 단계에서 CORE를 trace한다.

**한계:** CORE는 base 모델용. SFT 이후 chat 능력은 ChatCORE 같은 별도 평가가 필요. 또 CORE 0.26은 GPT-2 *capability*이지 *대화 품질*은 아니다 — "kindergartener level" (README §"Reproduce and talk to GPT-2").

### 5.2 bits-per-byte vs cross-entropy loss

같은 데이터를 두고 다른 vocab으로 평가하면 loss 수치가 비교 불가능하다. bpb로 정규화하면:
- vocab 16K vs 32K vs 100K를 같은 단위로 비교.
- 토크나이저 자체의 *효율*도 간접적으로 반영됨 — bytes/token이 높은 토크나이저는 같은 loss라도 더 많은 정보를 한 토큰에 압축.

**해석:** val_bpb = 0.748 (speedrun #1)이면 평균적으로 한 바이트의 텍스트를 0.748비트로 인코딩할 수 있다. 영어 텍스트의 Shannon entropy는 약 1.3 bit/byte로 알려져 있으므로 0.7 근방은 꽤 좋은 압축.

### 5.3 벤치마크별 평가 방식 한눈에

| Task | 형식 | 평가 방식 | nanochat 구현 |
|------|------|----------|---------------|
| MMLU | 4지선다 (A/B/C/D) | base: 옵션별 NLL 비교 / chat: 어시스턴트가 letter 토큰 1개 생성 후 letters 안에서 매칭 | `tasks/mmlu.py`, `chat_sft.py:382-396` |
| ARC | 4지선다 (과학) | 동일 | `tasks/arc.py` |
| GSM8K | 자유 서술 + 최종 숫자 | `extract_answer(#### N)` 정규식 매칭 | `tasks/gsm8k.py` |
| HumanEval | 코드 생성 | sandbox 실행 + assert 통과 | `tasks/humaneval.py` + `execution.py` |
| SpellingBee | 자유 서술 + #### N | gsm8k와 동일 | `tasks/spellingbee.py` |
| CORE 22-task | 다양 (mc/schema/lm) | autoregressive loss로 옵션 비교 | `nanochat/core_eval.py` |

**Pass@k** (RL): 한 문제에 k개 샘플 중 하나라도 맞으면 success. k=1, 2, 4, 8 보통. `chat_rl.py:228-237`.

---

## 6. 자기 챗봇 만들기 (커스터마이징)

### 6.1 Identity 주입 (personality)

**원천 가이드:** [#139](https://github.com/karpathy/nanochat/discussions/139).

**작동 방식:**
1. `dev/gen_synthetic_data.py`로 OpenRouter API를 호출해 1000개 합성 대화 생성. 다양성을 위해 4축 sampling:
   - topic categories (identity, architecture, training, capabilities, limitations, comparisons, history, technical_deep_dive, philosophical) — 9개 카테고리, 각 5-10 항목.
   - 12개 persona (curious beginner, ML researcher, ...).
   - 10개 conversation dynamics (short Q&A, deep technical, skeptical, learning journey, ...).
   - 7개 first-message style (simple greetings, multilingual, typos, caps, ...).
2. knowledge base(`knowledge/self_knowledge.md`)를 system prompt에 제공해 큰 모델(예: Gemini Flash)이 *정확한 사실*로 대화를 만들게 한다.
3. JSON schema로 structured output 강제.
4. 결과: `~/.cache/nanochat/identity_conversations.jsonl` — 1000줄, 각 줄은 `[{"role":"user",...}, {"role":"assistant",...}, ...]` 형식.
5. `chat_sft.py`가 이걸 `CustomJSON(filepath=...)`로 두 번(`_ for _ in range(2)`) mix해서 2 epochs 오버샘플 (`chat_sft.py:167-168`).
6. SFT 재실행 → 모델이 "I'm nanochat, an open source chatbot ..." 류로 일관되게 답함.

**커스터마이즈 포인트:** `gen_synthetic_data.py`의 `topics`, `personas`, `dynamics`, `first_messages` 딕셔너리를 수정 + `knowledge` 파일을 자기 정체성으로 교체.

### 6.2 새 능력 추가 (strawberry 가이드)

**원천 가이드:** [#164](https://github.com/karpathy/nanochat/discussions/164).

**아이디어:** "How many r in strawberry?" 같은 token-level 작업은 LLM이 약하다 (tokenizer가 'strawberry'를 하나의 토큰으로 보거나 segment해서 char 단위 추론이 어렵다). 해법: SFT 데이터로 *명시적인 char-by-char 추론 예제*를 다량 학습시키기.

**SpellingBee task (`tasks/spellingbee.py`):**
- 370K 영어 단어 word list에서 단어 + (90% 단어 내 글자, 10% 임의 글자)를 sample.
- user message: 50개 템플릿(영/중/한/스/불/독/일) 중 하나로 랜덤 포맷.
- assistant 답안 구조:
  1. 단어를 `s,t,r,a,w,b,e,r,r,y` 형식으로 spell (comma·no-space로 토큰 경계 강제 — Karpathy 지적: " a"와 "a"는 다른 토큰).
  2. 1:s 2:t 3:r hit! count=1 4:a ... 형식으로 카운터 진행.
  3. 자기검증: `'strawberry'.count('r')` python tool 호출 → 결과 비교.
  4. `#### 3` 최종 답.
- 정답은 `word.count(letter)`로 만들고, parts 형식의 conversation 반환.
- SFT mix에 80K 추가 + SimpleSpelling 200K (단순 철자만, 토큰화 인지를 데우는 용도).

**일반화:** 새 능력 X를 가르치려면:
1. `tasks/X.py`에 `Task` 서브클래스를 만든다. `get_example(idx)`가 conversation을 반환.
2. assistant 답은 *step-by-step reasoning*과 도구 호출(있다면)을 포함.
3. user message 표현을 다양하게 (template 30+개).
4. `chat_sft.py`의 `train_tasks` 리스트에 추가.
5. mid/SFT 풀 재학습.
6. (선택) `chat_rl.py`에서 RL로 정확도 추가 finetune.

### 6.3 토크나이저 압축률 측정

`scripts/tok_eval.py`가 GPT-2(50K), GPT-4(100K), 자기 tokenizer(32K)를 동일 텍스트(영문 뉴스, 한국어, 코드, LaTeX 수학, 영문 과학, FineWeb train/val)에 대해 비교. metric은 `ratio = bytes/tokens` — 높을수록 효율적인 압축.

**관찰 (Karpathy 보고):** 32K vocab에서 FineWeb train 4.8× compression (1 토큰 ≈ 4.8 bytes). GPT-4 (100K)보다 약간 떨어지지만 lm_head 파라미터를 ~3× 적게 쓰므로 작은 모델에서 유리. 한국어는 모든 토크나이저에서 ratio가 낮다(2-3×) — 학습 데이터에 영어가 압도적이라.

---

## 7. 자주 막히는 곳

### 7.1 OOM과 `--device-batch-size` 튜닝

- README: 80GB 미만 GPU면 `--device-batch-size`를 32→16→8→4→2→1로 내려라.
- 메모리 잡식자 순서: lm_head logits (`(B, T, vocab_size)` fp32) > attention KV during backward > optimizer state (Muon momentum + factored second moment + AdamW exp_avg + exp_avg_sq) > activations.
- `expandable_segments:True` (`base_train.py:14`) — PyTorch 메모리 fragmentation 완화.
- gradient accumulation: total_batch_size를 그대로 두고 device_batch_size만 줄이면 `grad_accum_steps`가 자동 증가 → 같은 효과, 더 느림.

### 7.2 CPU/MPS 한계

- MPS는 일부 int64 < 0 비교 커널이 없음 → `loss_eval.py:36`에서 `int32`로 cast하는 분기.
- M3 Max에서 d6 학습 5K steps ~30분. d20+는 비현실적.
- FA3는 CUDA-only. MPS는 SDPA로 떨어지고 sliding window는 explicit mask 빌드.
- `NANOCHAT_DTYPE=float32` 강제가 안전.

### 7.3 dtype 자동선택 표

| HW | default | 변경 | 비고 |
|----|---------|------|------|
| H100/A100 (SM ≥ 80) | bf16 | NANOCHAT_DTYPE=float32로 강제 fp32 | FA3는 bf16만 |
| V100/T4 (SM < 80) | fp32 | NANOCHAT_DTYPE=float16 → GradScaler 자동 활성 | fp16은 RL 미지원 |
| CPU/MPS | fp32 | — | 그대로 두는 게 좋다 |

### 7.4 분산 vs 단일 GPU vs CPU

- `torchrun --standalone --nproc_per_node=8 -m scripts.base_train`: 8 rank, ZeRO-2 optimizer sharding, ~3시간 H100.
- `python -m scripts.base_train`: 단일 GPU. `is_ddp_requested=False`, optimizer는 `MuonAdamW` (`DistMuonAdamW` 대신).
- `python -m scripts.base_train --depth=4 --max-seq-len=512 --device-batch-size=1 ...`: CPU/MPS 데모.

### 7.5 학습이 발산하면

- `train/loss`가 갑자기 튀어오르면: logit softcap(`gpt.py:468-472`)이 잡아주긴 하지만 LR이 너무 크거나 batch가 너무 작거나 데이터 노이즈.
- val_bpb가 학습 loss와 크게 벌어지면 overfit — `--target-param-data-ratio`를 늘리거나 더 많은 셰드 다운로드.
- fp16 학습 중 NaN: `GradScaler`가 자동 처리하지만 distributed에서는 모든 rank가 `found_inf`를 동기화해야 함 (`base_train.py:533-535`).

### 7.6 평가가 이상하면

- MMLU에 백슬래시 공백이 들어가면 letter token이 달라져 정답률이 떨어진다. `render_mc`의 `=A` (공백 없음)가 의도된 것 (`tasks/common.py:112-131`).
- HumanEval 코드가 무한루프면 `execution.py`의 timeout(5s) + RLIMIT_AS(256MB)가 잡아준다.
- CORE squad task만 reference 대비 31% vs 37%로 약간 떨어진다는 알려진 차이 — Karpathy의 TODO (`core_eval.py:5-6`).

---

## 8. 참고문헌

### nanochat 공식 자료
- [GitHub repo](https://github.com/karpathy/nanochat) — README, 코드, eval_bundle.
- [Discussion #1: 원 nanochat 소개 (Oct 13 2025)](https://github.com/karpathy/nanochat/discussions/1)
- [Discussion #139: Identity 주입 가이드](https://github.com/karpathy/nanochat/discussions/139)
- [Discussion #164: strawberry / 능력 추가 가이드](https://github.com/karpathy/nanochat/discussions/164)
- [Discussion #420: Jan 7 miniseries v1](https://github.com/karpathy/nanochat/discussions/420)
- [Discussion #481: Beating GPT-2 for &lt;$100 — 최적화 여정](https://github.com/karpathy/nanochat/discussions/481)
- [Discussion #498: autoresearch round 1](https://github.com/karpathy/nanochat/pull/498)
- [DeepWiki nanochat](https://deepwiki.com/karpathy/nanochat) — Devin/Cognition 자동 생성 위키.

### 관련 리포지토리
- [nanoGPT](https://github.com/karpathy/nanoGPT) — pretraining만 다루는 전작.
- [modded-nanoGPT (Keller Jordan)](https://github.com/KellerJordan/modded-nanogpt) — Muon, GPT-2 speedrun.
- [Muon optimizer 블로그 (Keller Jordan)](https://kellerjordan.github.io/posts/muon/)

### 데이터셋
- [HuggingFace FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) — 1.53B rows, ODC-BY, 교육 품질 필터링된 Common Crawl.
- [HuggingFace SmolTalk](https://huggingface.co/datasets/HuggingFaceTB/smoltalk) — 1.1M synthetic SFT 데이터, Apache 2.0.
- [MMLU (cais/mmlu)](https://huggingface.co/datasets/cais/mmlu)
- [GSM8K (openai/gsm8k)](https://huggingface.co/datasets/openai/gsm8k)
- [ARC (allenai/ai2_arc)](https://huggingface.co/datasets/allenai/ai2_arc)
- [HumanEval (openai/openai_humaneval)](https://huggingface.co/datasets/openai/openai_humaneval)
- ClimbMix (NVIDIA, speedrun #4부터 사용)

### 핵심 논문
- Vaswani et al., "Attention Is All You Need" — [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Radford et al., "Language Models are Unsupervised Multitask Learners" (GPT-2) — [paper PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Brown et al., "Language Models are Few-Shot Learners" (GPT-3) — [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Sennrich, Haddow & Birch, "Neural Machine Translation of Rare Words with Subword Units" (BPE) — [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)
- Su et al., "RoFormer: Enhanced Transformer with Rotary Position Embedding" — [arXiv:2104.09864](https://arxiv.org/abs/2104.09864)
- Zhang & Sennrich, "Root Mean Square Layer Normalization" — [arXiv:1910.07467](https://arxiv.org/abs/1910.07467)
- Shazeer, "GLU Variants Improve Transformer" — [arXiv:2002.05202](https://arxiv.org/abs/2002.05202)
- So et al., "Primer: Searching for Efficient Transformers for Language Modeling" (ReLU²) — [arXiv:2109.08668](https://arxiv.org/abs/2109.08668)
- Loshchilov & Hutter, "Decoupled Weight Decay Regularization" (AdamW) — [arXiv:1711.05101](https://arxiv.org/abs/1711.05101)
- Hoffmann et al., "Training Compute-Optimal Large Language Models" (Chinchilla) — [arXiv:2203.15556](https://arxiv.org/abs/2203.15556)
- Kaplan et al., "Scaling Laws for Neural Language Models" — [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)
- Dao et al., "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness" — [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
- Micikevicius et al., "FP8 Formats for Deep Learning" — [arXiv:2209.05433](https://arxiv.org/abs/2209.05433)
- Li et al., "DataComp-LM: In search of the next generation of training sets" — [arXiv:2406.11794](https://arxiv.org/abs/2406.11794)
- Hendrycks et al., "Measuring Massive Multitask Language Understanding" (MMLU) — [arXiv:2009.03300](https://arxiv.org/abs/2009.03300)
- Cobbe et al., "Training Verifiers to Solve Math Word Problems" (GSM8K) — [arXiv:2110.14168](https://arxiv.org/abs/2110.14168)
- Chen et al., "Evaluating Large Language Models Trained on Code" (HumanEval) — [arXiv:2107.03374](https://arxiv.org/abs/2107.03374)
- Clark et al., "Think you have Solved Question Answering? Try ARC" — [arXiv:1803.05457](https://arxiv.org/abs/1803.05457)
- Williams, "Simple statistical gradient-following algorithms for connectionist reinforcement learning" (REINFORCE), Machine Learning 1992.
- Schulman et al., "Proximal Policy Optimization Algorithms" — [arXiv:1707.06347](https://arxiv.org/abs/1707.06347)
- DeepSeek-Math (GRPO) — [arXiv:2402.03300](https://arxiv.org/abs/2402.03300)
- Amsel et al., "Polar Express Sign Method" — [arXiv:2505.16932](https://arxiv.org/abs/2505.16932)
- NorMuon variance reduction — [arXiv:2510.05491](https://arxiv.org/abs/2510.05491)
- Power Lines (batch size scaling) — [arXiv:2505.13738](https://arxiv.org/abs/2505.13738)
- T_epoch framework (weight decay scaling) — [arXiv:2405.13698](https://arxiv.org/abs/2405.13698)
- PaLM (FLOPs counting) — [arXiv:2204.02311](https://arxiv.org/abs/2204.02311)

### 커뮤니티 토론
- [Hacker News: NanoChat – The best ChatGPT that $100 can buy](https://news.ycombinator.com/item?id=45569350) — Karpathy의 "AI agent가 안 도와줬다" 발언과 그에 대한 토론. AI 코딩 도구의 한계, 학습 cost accessibility에 대한 우려.
- [Hacker News: Nanochat (2nd thread)](https://news.ycombinator.com/item?id=45575051)
- BigGo: "Karpathy's $100 NanoChat Sparks Community Training Frenzy" (2025-10-14) — [기사](https://biggo.com/news/202510140113_nanochat-100-dollar-chatgpt-clone-community-reaction)
- Sarah Glasmacher: "Nanochat by Andrej Karpathy" — [블로그](https://www.sarahglasmacher.com/nanochat-by-andrej-karpathy/)
- David Aronchick: "The $100 ChatGPT" — [DEV.to](https://dev.to/david_aronchick_ea415de50/the-100-chatgpt-why-karpathys-nanochat-represnts-the-next-big-thing-3459)
- José David Baena: "The Muon Optimizer Explained" — [블로그](https://josedavidbaena.com/blog/nanochat/muon-optimizer-explained)
- Karpathy on X: 발표 트윗 — [twitter.com/karpathy/status/1977755427569111362](https://x.com/karpathy/status/1977755427569111362)

### 인프라
- [uv](https://docs.astral.sh/uv/) — Python package manager.
- [Lambda Cloud](https://lambda.ai/service/gpu-cloud) — 8XH100 ~$24/hr.
- [tiktoken](https://github.com/openai/tiktoken)
- [Wandb](https://wandb.ai/) — 학습 모니터링.

---

## 9. 리서치 한계 (커버하지 못한 영역)

이 레퍼런스가 *지금* 커버 못 한 / 약하게 다룬 영역들. 챕터 저자가 보강이 필요하다고 판단되면 추가 리서치 필요.

1. **Reddit / OKKY / velog 한국어 커뮤니티 후기** — 두 번째 웹 검색에서 r/LocalLLaMA 직접 결과가 안 나왔다. 한국어 커뮤니티에서 nanochat 후기는 아직 충분히 잘 색인되지 않은 것으로 보임. 책 본문에서 "현장 경험담"을 인용해야 한다면 영어권 HN 토론과 영문 블로그 두세 개로 일부 보강했지만, 한국 개발자의 1인칭 후기는 부족하다.

2. **dev/LOG.md, dev/LEADERBOARD.md 본문** — 코드 분석에서는 보지 않았다. Karpathy의 일별 진척 기록이 들어 있을 가능성이 있다. 챕터 5 (평가)나 챕터 7 (자주 막히는 곳)을 쓸 때 추가 정독 가능.

3. **`tasks/customjson.py`, `tasks/smoltalk.py`, `tasks/humaneval.py`, `tasks/arc.py`** — 외형/시그니처만 파악. SFT data flow 이해엔 충분하지만 각 task의 평가 디테일을 깊이 다루지 않았다.

4. **scaling_laws.sh / miniseries.sh** — 본문을 직접 읽지 않았다. miniseries v1의 d10~d20 hyperparameter table은 [#420](https://github.com/karpathy/nanochat/discussions/420)에서 인용했다.

5. **FineWeb 가공 (`dev/repackage_data_reference.py`)** — pretraining 데이터 셰드 생성 디테일. 별도 챕터를 쓸 정도는 아니지만 "데이터가 어떻게 디스크에 놓이는가" 한 박스 정도는 필요할 수 있다.

6. **chat_eval.py 본문** — SFT/RL 평가의 정확한 정답 추출 로직. 챕터 5에서 인용하려면 한 번 더 읽어봐야 한다.

7. **`nanochat/dataset.py`** — parquet 셰드 다운로드 URL, retry, 손실 복구. 인프라 디테일.

8. **`nanochat/ui.html` 프론트엔드** — JS/CSS 코드. 책 본문에서는 "FastAPI + 단일 HTML 파일"로 충분히 다룰 수 있다.

9. **autoresearch (Karpathy)** — [#481](https://github.com/karpathy/nanochat/discussions/481)·[#498](https://github.com/karpathy/nanochat/pull/498)에서 언급되는 "autoresearch round 1, round 2"는 *Karpathy가 LLM agent로 hyperparameter sweep을 자동화한 시도*로 보이지만, 구체적 방법은 X 글타래에 흩어져 있어 본 레퍼런스에서는 일반 서술로만 다뤘다. 챕터 작성 시 별도 인용 검토.

10. **DCLM CORE의 22 task 정확 목록** — `eval_bundle/core.yaml`에 있다(코드 분석에서 직접 파일을 열지는 않았다). 챕터 5에서 task 목록을 표로 보여주려면 한 번 다운로드해서 정리 필요.
