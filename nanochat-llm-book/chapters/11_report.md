# 11장. report.md — 우리의 작품에 도장 찍기

`72라고 답한다.`

앞 장 마지막 줄이 그렇게 끝났다. 우리의 모델은 *"What is 8 times 9?"*에 *72*라고 답했다. 손가락으로 박수를 한 번 쳐도 된다. 길게는 6장의 통합부터, 짧게는 9장의 RL 한 스텝까지, *모든 단계의 산출*이 한 줄의 답으로 모였다.

그런데, 잠시 흥분을 가라앉혀 보자. 한 가지 질문이 남아 있다.

> **우리가 *진짜로* GPT-2급에 도달했다고, 어떻게 *증명*할 것인가?**

`72라고 답한다`는 한 번의 일화다. 다음에 물으면 *72.5*라고 답할 수도 있고, *팔구는 칠십이*라고 답할 수도 있다. 한 번의 우연을 두고 "GPT-2급"이라 부를 수는 없다. 우리가 만든 모델이 *어떤 데이터로*, *몇 시간 동안*, *어떤 GPU에서*, *어떤 git commit*으로, *어떤 수치*에 도달했는지를 — *한 페이지의 종이*에 박아두지 않으면, 다음 누군가는 우리의 *진짜로*를 믿을 수 없다.

생각해보면 *남에게 자랑하기* 위해서가 아니더라도, 이 한 페이지는 우리 *자신*에게 필요하다. *한 달 뒤*에 똑같은 학습을 다시 돌렸는데 결과가 *다르게* 나온다고 해보자. 그때 *무엇이 달라졌는가*를 비교할 *기준점*이 없으면 난감하다. PyTorch 버전이 바뀌었나, 데이터가 갱신됐나, hyperparameter를 슬쩍 손댔던가 — 짚어볼 수 있는 *원본 스냅샷* 없이는 *내가 무엇을 하고 있는지* 가물가물해진다. 그러니 도장은 *남을 위해서*가 아니라 *내일의 나를 위해서* 찍는 셈이기도 하다.

이게 11장의 일이다. 짧고 농밀한 *증거의 장*. 자랑이 아니라 *측정된 사실의 정리*. 도장 한 번을 잘 찍어 두는 일이다.

`nanochat/report.py`라는 작은 모듈 하나가 이 일을 한다. *400줄 남짓*의 파일이지만, 책의 *마지막 도장*을 찍는 자리에 있다. 그 안을 펴보자.

---

## 11.1 `nanochat/report.py` — 작은 모듈이 책 전체를 요약한다

`report.py`를 처음 펴면 *왠지 미안한 듯한* 코멘트로 시작한다.

```python
# nanochat/report.py:1-3
"""
Utilities for generating training report cards. More messy code than usual, will fix.
"""
```

*"평소보다 더 지저분한 코드, 곧 정리할 것."* 카르파시다운 정직함이다. 한데 우리가 정직하게 말하자면, 이 코드는 *지저분한 코드*가 아니라 *최소 코드*다. 책의 *마지막 도장*을 찍는 모듈인데, 단 한 클래스(`Report`)와 단 세 메서드(`reset`, `log`, `generate`)로 일을 마친다. *더 줄일 데가 없다*.

이 클래스가 무엇을 하는지를, 학습이 시작되는 *순간*부터 따라가 보자.

### `reset()` — 학습 시작 시각에 헤더 한 장을 박는다

`runs/speedrun.sh`의 *제일 위*를 보면 이 한 줄이 있다.

```bash
# runs/speedrun.sh:46
python -m nanochat.report reset
```

이게 첫 도장이다. *학습이 시작되기 전*에, `$NANOCHAT_BASE_DIR/report/header.md`에 *지금 이 순간의 스냅샷*을 박아두는 일이다. `reset()`이 내부에서 `generate_header()`를 호출하고, 그게 뭘 모으는지 정직하게 보자.

```python
# nanochat/report.py:120-127
def generate_header():
    """Generate the header for a training report."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    git_info = get_git_info()
    gpu_info = get_gpu_info()
    sys_info = get_system_info()
    cost_info = estimate_cost(gpu_info)
```

네 종류를 모은다. *시각, git, GPU, 시스템.* 그리고 *비용 추정*까지. 각각이 *어떤 사실*을 박는지 한 줄씩 살펴보자.

**`get_git_info()`.** `git rev-parse --short HEAD`로 *현재 커밋 해시*를 박고, `git status --porcelain`으로 *작업 트리가 더러운지(dirty)* 표시한다. *깨끗한* 커밋이라면 누구나 *같은 코드*를 다시 펴서 재현할 수 있다. 더러우면? `(dirty)` 한 단어가 정직하게 들어간다. *"이 결과는 그 커밋이 *아닌* 어떤 변형으로 만들어졌습니다"*를 책에 박는 셈이다. 우리가 다른 사람의 보고서를 읽을 때, 이 한 단어가 *결과를 믿어도 되는지*를 가른다.

**`get_gpu_info()`.** `torch.cuda.device_count()`로 GPU 개수를 박고, `torch.cuda.get_device_properties(i).name`으로 모델명을 박는다. *어떤 H100인지*, *몇 장인지*, *총 VRAM이 얼마인지*가 그대로 들어간다. 우리가 8XH100에서 3시간을 돌렸다면 그 *기준*이 책에 박혀야 한다. 다른 사람이 4XA100으로 돌리면 같은 시간이 나올 리가 없다.

**`get_system_info()`.** CPU 코어 수, 메모리, Python 버전, PyTorch 버전. *왜* 이런 것까지 박는가? *재현이 안 될 때*의 디버그 단서가 되기 때문이다. PyTorch 마이너 버전 하나가 달라서 numerics가 바뀌는 일이 *실제로* 있다. 그래서 *적어둔다*.

**`estimate_cost()`.** 가장 *솔직한* 한 줄이다. H100당 시간당 $3, A100당 $1.79 같은 *고정 단가*를 코드 안에 박아두고, GPU 개수를 곱해 *시간당 비용*을 추산한다.

```python
# nanochat/report.py:93-98
default_rate = 2.0
gpu_hourly_rates = {
    "H100": 3.00,
    "A100": 1.79,
    "V100": 0.55,
}
```

*Lambda Cloud 기준*이라고 주석에 적혀 있다. *지금 spot 인스턴스의 $1.20인지*는 모른다. 그게 정직함이다 — *추산*임을 명시하고, *원자료*를 그대로 책에 박아둔다.

이 모든 게 모여서 *학습이 시작되기 전*에 한 장이 박힌다. 그게 *header.md*다. *증거의 기준선*이다.

### `log()` — 단계마다 *덤덤히* 한 줄씩 더한다

학습이 진행되면서, 각 단계가 자기 결과를 *얌전히* 보고서에 적어 둔다. `Report.log()`가 그 일이다.

```python
# nanochat/report.py:251-277
def log(self, section, data):
    """Log a section of data to the report."""
    slug = slugify(section)
    file_name = f"{slug}.md"
    file_path = os.path.join(self.report_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"## {section}\n")
        f.write(f"timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for item in data:
            if not item:
                continue
            if isinstance(item, str):
                f.write(item)
            else:
                for k, v in item.items():
                    if isinstance(v, float):
                        vstr = f"{v:.4f}"
                    elif isinstance(v, int) and v >= 10000:
                        vstr = f"{v:,.0f}"
                    else:
                        vstr = str(v)
                    f.write(f"- {k}: {vstr}\n")
        f.write("\n")
    return file_path
```

코드가 *수수하다*. 섹션 이름을 slugify해서 `tokenizer-training.md`, `base-model-training.md`, `chat-evaluation-rl.md` 같은 *짧은 markdown 한 장*을 만든다. dict가 들어오면 키-값을 *불릿*으로, float는 소수점 4자리로, 큰 정수는 *컴마*로 — 사람이 읽을 수 있는 단위로 박아둔다.

이게 *왜* 좋은가? 우리가 학습 스크립트 어디서든 `report.log("Base model training", [...])` 한 줄을 부르면 *그 단계의 사실*이 *그 자리에서* 박힌다는 점이다. wandb 같은 *비싼* 도구도, 별도의 *DB*도 필요 없다. *그냥 markdown 파일* 한 장씩.

`tok_train.py`는 `tokenizer-training.md`를 박고, `base_train.py`는 `base-model-training.md`와 `base-model-loss.md`를 박고, `chat_sft.py`는 `chat-sft.md`와 `chat-evaluation-sft.md`를, `chat_rl.py`는 `chat-rl.md`와 `chat-evaluation-rl.md`를 박는다. 9장의 짧은 RL 한 줄까지가 *자기 자리에 적힌다*. 책의 *목차*가 학습 중에 *자동으로* 쌓이는 셈이다.

### `generate()` — 마지막에 한 페이지로 *모은다*

학습이 끝나면 마지막 한 줄이 호출된다.

```bash
python -m nanochat.report generate
```

이 명령이 안에서 `Report.generate()`를 부르고, 그게 *흩어져 있던 markdown 조각들*을 정해진 순서로 *이어 붙인다*.

```python
# nanochat/report.py:208-218
EXPECTED_FILES = [
    "tokenizer-training.md",
    "tokenizer-evaluation.md",
    "base-model-training.md",
    "base-model-loss.md",
    "base-model-evaluation.md",
    "chat-sft.md",
    "chat-evaluation-sft.md",
    "chat-rl.md",
    "chat-evaluation-rl.md",
]
```

순서가 *책의 순서 그대로*다. 토크나이저(2~3장) → 사전학습(4A·4B·5·6장) → 평가(7장) → SFT(8장) → RL(9장). 책의 챕터 진행이 *그대로* 리포트의 순서다. 우연이 아니다. 카르파시가 *학습 파이프라인*을 짜면서 *그 자체가 리포트*가 되도록 설계했기 때문이다.

`generate()`의 마지막 일은 두 가지다. 하나는 *Summary 테이블*을 만드는 일.

```python
# nanochat/report.py:325-355
out_file.write("## Summary\n\n")
out_file.write(bloat_data)
out_file.write("\n\n")
all_metrics = set()
for stage_metrics in final_metrics.values():
    all_metrics.update(stage_metrics.keys())
all_metrics = sorted(all_metrics, key=lambda x: (x != "CORE", x == "ChatCORE", x))
stages = ["base", "sft", "rl"]
metric_width = 15
value_width = 8
header = f"| {'Metric'.ljust(metric_width)} |"
for stage in stages:
    header += f" {stage.upper().ljust(value_width)} |"
out_file.write(header + "\n")
```

`base`, `sft`, `rl` 세 단계의 *주요 metric*들을 한 표에 모은다. CORE는 *맨 위*, ChatCORE는 *맨 아래*, 나머지는 그 사이. *읽기 좋게 정렬한다*.

다른 하나는 *총 wall-clock 시간*을 계산하는 일.

```python
# nanochat/report.py:357-363
if start_time and end_time:
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    out_file.write(f"Total wall clock time: {hours}h{minutes}m\n")
```

`header.md`에 박혀 있던 *시작 시각*과 마지막 섹션의 *timestamp*의 차이. 우리가 *얼마나 오래 돌렸는지*가 한 줄로 박힌다. 단, RL 섹션은 *end_time 계산에서 빼버린다*. RL이 *실험적 단계*라서 그렇다 — RL을 돌릴 수도 있고 안 돌릴 수도 있는데, 그게 *총 학습 시간*에 들어가면 다른 사람들과 비교가 안 되니까. 정직한 결정이다.

마지막 한 줄은 *친절한 복사*다.

```python
# nanochat/report.py:367-368
print(f"Copying report.md to current directory for convenience")
shutil.copy(report_file, "report.md")
```

원본은 `$NANOCHAT_BASE_DIR/report/report.md`에 있지만, *편의*를 위해 현재 디렉토리에 한 부를 더 복사한다. 학습 끝나고 `ls`를 쳤을 때 *바로 보이는 자리*에 `report.md`가 있다. 그걸 펴서 친구에게 보내면 된다.

---

## 11.2 `report.md` 한 페이지 — *책의 마지막 증거*

자, 이제 *실제로 출력되는 한 페이지*를 보자. 책의 *마지막 증거*다. 우리의 nanochat 한 번 학습이 박아두는 *진짜 markdown*은 다음과 같이 생겼다. 한 페이지 안에 *학습의 모든 것*이 들어 있으니, *한 번도 빼먹지 않고* 통째로 읽어보자.

```markdown
# nanochat training report

Generated: 2026-03-09 14:23:51

## Environment

### Git Information
- Branch: master
- Commit: 6ed7d1d (clean)
- Message: autoresearch round 1: ClimbMix + NorMuon + value embeddings

### Hardware
- Platform: Linux
- CPUs: 26 cores (52 logical)
- Memory: 219.0 GB
- GPUs: 8x NVIDIA H100 80GB HBM3
- GPU Memory: 640.0 GB total
- CUDA Version: 12.6
- Hourly Rate: $24.00/hour

### Software
- Python: 3.10.14
- PyTorch: 2.5.1

### Bloat
- Characters: 287,432
- Lines: 8,107
- Files: 41
- Tokens (approx): 71,858
- Dependencies (uv.lock lines): 2,164

Run started: 2026-03-09 12:36:18

---

## Tokenizer training
timestamp: 2026-03-09 12:38:54

- vocab_size: 32,768
- max_chars: 2,000,000,000
- num_special_tokens: 9
- training_time_sec: 156.2

## Tokenizer evaluation
timestamp: 2026-03-09 12:39:11

- compression_ratio (FineWeb): 4.8042
- vs GPT-2 (50K):   +18.2% better
- vs GPT-4 (100K):  -2.1% slightly worse

## Base model training
timestamp: 2026-03-09 13:52:07

- depth: 26
- model_dim: 1664
- num_params: 622,034,944
- num_iterations: 21,400
- total_batch_size: 1,048,576
- max_seq_len: 2,048
- num_flops_per_token: 4.034e9
- final_lr: 3.8e-4
- mfu_avg: 0.5193
- tok_per_sec: 408,562
- val_bpb: 0.7181

## Base model evaluation
timestamp: 2026-03-09 14:09:42

- CORE: 0.2690

## Chat SFT
timestamp: 2026-03-09 14:17:28

- mix: smoltalk+mmlu+gsm8k+identity+spellingbee
- num_examples: 462,118
- num_epochs: 1
- training_time_sec: 423.7

## Chat evaluation SFT
timestamp: 2026-03-09 14:21:14

- ARC-Easy:       0.3892
- ARC-Challenge:  0.2718
- MMLU:           0.3206
- GSM8K:          0.0455
- HumanEval:      0.0732
- ChatCORE:       0.1184

## Chat RL
timestamp: 2026-03-09 14:23:33

- task: gsm8k
- num_steps: 200
- algorithm: GRPO

## Chat evaluation RL
timestamp: 2026-03-09 14:23:48

- GSM8K: 0.0789

## Summary

- Characters: 287,432
- Lines: 8,107
- Files: 41
- Tokens (approx): 71,858
- Dependencies (uv.lock lines): 2,164

| Metric          | BASE     | SFT      | RL       |
|-----------------|----------|----------|----------|
| CORE            | 0.2690   | -        | -        |
| ARC-Challenge   | -        | 0.2718   | -        |
| ARC-Easy        | -        | 0.3892   | -        |
| GSM8K           | -        | 0.0455   | 0.0789   |
| HumanEval       | -        | 0.0732   | -        |
| MMLU            | -        | 0.3206   | -        |
| ChatCORE        | -        | 0.1184   | -        |

Total wall clock time: 1h47m
```

*한 페이지*다. 헤더 한 장, 단계별 보고 일곱 장, Summary 표 한 장. *학습이 시작된 12:36*부터 *끝난 14:23*까지의 *모든 사실*이 여기 박혀 있다. 책 한 권을 통과해 온 *증거*가, 끝에서는 *이렇게 한 페이지*로 정리된다.

(주: 위 페이지는 [leaderboard #5의 운영 보고](https://github.com/karpathy/nanochat/discussions/481) 수치를 바탕으로 *재구성한 예시*다. 실제 `report.md`는 환경에 따라 줄 수가 약간 다르지만 *형식*은 그대로다.)

---

## 11.3 한 페이지 안의 수치들 — *어느 챕터에서 만난 이름인가*

위 페이지의 *모든 숫자*에는 이름이 있다. 우리가 책에서 *이미 한 번씩* 만난 이름들이다. 한 줄씩 *어디서 봤는지* 짚어 가며 다시 읽어보자.

**`Commit: 6ed7d1d (clean)`.** *git이 깨끗하다*는 한 단어. 우리가 *지금 이 commit*을 다시 체크아웃하면 *같은 결과*가 재현될 수 있다는 약속이다. 4A장에서 "code as the unit of reproducibility"를 말했던 그 약속의 *마지막 도장*이다.

**`Bloat / Lines: 8,107`.** *책의 부제목*이 여기서 정직하게 박힌다. 이 작은 모델을 만든 *전체 코드*가 8,107줄. 한 챕터씩 펴봤던 그 모든 파일을 합쳐 *그 정도*다. *작다*. 그 작음이 책 전체의 *주장*이었다.

**`vocab_size: 32,768`, `compression_ratio: 4.8042`.** *2장과 3장*에서 만난 수치다. *32,768개*의 토큰으로 FineWeb 영어 텍스트를 *4.8배* 압축한다. GPT-2의 50,257 vocab보다 *작은데도* 18.2% 더 잘 압축한다는 *이 한 줄*이, *우리의 토크나이저가 무엇이었는지*를 단번에 말한다.

**`depth: 26`, `model_dim: 1664`, `num_params: 622,034,944`.** *4A장*에서 만난 *세 다이얼*. depth 한 정수가 width, n_heads, learning rate를 *전부* 결정한다는 그 디자인 — *620M 파라미터* 모델이 *깊이 26이라는 한 정수*에서 자동으로 빚어졌다는 사실이 이 세 줄에 박혀 있다.

**`num_iterations: 21,400`, `total_batch_size: 1,048,576`.** *6장*에서 통합된 사전학습 루프. *2백만 토큰* 배치를 *21,400번*. 이 두 숫자의 곱(약 224억 토큰)이 *모델이 본 세상의 크기*다.

**`mfu_avg: 0.5193`.** *5장과 6장*의 *MFU*. H100 한 장의 peak FLOPS의 51.9%를 우리가 *실제로* 썼다. 50%를 넘긴다는 건 *카르파시 본인*도 *"목표"*로 적어둔 선이다. 그걸 넘긴 채로 학습이 끝났다.

**`tok_per_sec: 408,562`.** 8장의 H100 한 노드에서 초당 *40만 토큰*. 학습 중 wandb 그래프의 가장 위에 떠 있던 그 곡선이 *평균값* 한 줄로 박혔다.

**`val_bpb: 0.7181`.** *책의 첫 번째 정량 신호*. 7장에서 정밀하게 보았던 bits-per-byte. *영어 한 바이트*를 평균 0.72비트로 인코딩한다. 영어 텍스트의 Shannon entropy가 *약 1.3 bit/byte*로 알려져 있으니, 0.72는 *꽤 좋은 압축*이다. 한 줄로 *모델이 영어를 얼마나 잘 이해하는지*를 말한다.

**`CORE: 0.2690`.** *책 전체의 우승 선언*. 7장의 [DCLM CORE 22-task](https://arxiv.org/abs/2406.11794). GPT-2 (1.6B)의 reference CORE가 0.256525. 우리는 0.2690으로 *0.013점*만큼, *4.8%*만큼 *넘어섰다*. 그것도 *1시간 47분*에. 2019년 OpenAI가 *168시간* 들여 만든 그 GPT-2를, 우리가 *그 1/100의 시간*에 *능가*한 셈이다. *이 한 줄을 위해서* 책 11장이 흘러왔다.

**`ChatCORE: 0.1184`.** *8장과 9장*에서 정의한 *chat 모델용 평가*. ARC-Easy/Challenge, MMLU, GSM8K, HumanEval, SpellingBee 여섯 task의 *centered 평균*. 0.1184. *높지 않다.* 0.26인 base CORE에 비해 *절반보다 낮다*. 우리가 8장에서 *기대치 조정 박스*에 적었던 그대로 — *kindergartener level*이다. *작은 모델이 SFT로 얻을 수 있는 만큼만 얻었다*. 정직한 숫자다.

**`GSM8K: 0.0455 → 0.0789` (SFT → RL).** *9장에서 만난 짧은 RL의 도장*. 200스텝짜리 GRPO가 GSM8K 정답률을 *4.5%에서 7.9%로* 올렸다. *얼마 안 되는 폭*이지만, 우리가 *RL이 가능했다*는 사실의 *증거*는 이 한 줄로 충분하다.

**`Total wall clock time: 1h47m`.** *책 전체*가 *두 시간이 안 되는 시간*에 만들어졌다. 사람의 *낮잠 한 번*보다 짧은 시간에, 우리가 *학습한 LLM*이 완성됐다. *Time to GPT-2*의 우리 기록이다.

수치 한 줄이 *책의 한 챕터*다. 11장에서 *증거*라는 단어를 썼던 이유다.

---

## 11.4 리더보드 — *우리는 어디쯤에 있는가*

이 한 페이지의 *수치들*이 *얼마나 빨라진 것*인지, *맥락* 없이는 와닿기 어렵다. nanochat의 README는 그 *맥락*을 leaderboard 한 표로 박아두고 있다. [Time-to-GPT-2 Leaderboard](https://github.com/karpathy/nanochat#time-to-gpt-2-leaderboard) — *직접 그대로* 옮겨오자.

| # | time (h) | val_bpb | CORE | Description | Date | Commit |
|---|----------|---------|------|-------------|------|--------|
| 0 | 168 | – | 0.2565 | Original OpenAI GPT-2 checkpoint | 2019 | – |
| 1 | 3.04 | 0.74833 | 0.2585 | d24 baseline, slightly overtrained | Jan 29 2026 | 348fbb3 |
| 2 | 2.91 | 0.74504 | 0.2578 | d26 slightly undertrained **+fp8** | Feb 2 2026 | a67eba3 |
| 3 | 2.76 | 0.74645 | 0.2602 | bump total batch size to 1M tokens | Feb 5 2026 | 2c062aa |
| 4 | 2.02 | 0.71854 | 0.2571 | change dataset to NVIDIA ClimbMix | Mar 4 2026 | 324e69c |
| 5 | **1.80** | **0.71808** | **0.2690** | autoresearch round 1 | Mar 9 2026 | 6ed7d1d |
| 6 | 1.65 | 0.71800 | 0.2626 | autoresearch round 2 | Mar 14 2026 | a825e63 |

표 한 장에 *진화의 역사*가 다 들어 있다. 한 줄씩 *그 의미*를 짚어보자.

**Row 0.** *기준선*. 2019년의 OpenAI GPT-2 1.6B. *168시간 = 7일* 동안 학습했다. *CORE 0.2565*. 우리가 *넘어서야 할 선*이다.

**Row 1 (Jan 29 2026).** d24 baseline. *3.04시간*에 0.2585. *처음으로* GPT-2를 *넘었다*. 168시간이 *3시간*이 되는 데 *7년*이 걸렸다.

**Row 2 (Feb 2 2026).** +fp8. 깊이를 d26로 올리면서 fp8 활성. 9% tok/sec 향상. *2.91시간*. 4A장의 *수치 정밀도* 한 다이얼이 만든 폭이다.

**Row 3 (Feb 5 2026).** *Batch를 100만 토큰*으로. 5장에서 본 batch-size 다이얼이 효과를 냈다. *2.76시간*.

**Row 4 (Mar 4 2026).** *ClimbMix 데이터셋*으로 교체. FineWeb → ClimbMix. NVIDIA가 정제한 더 *효율 좋은* 데이터. 6장에서 "데이터가 가장 강한 다이얼"이라 적어둔 *바로 그 폭*. *2.02시간*. val_bpb가 *0.745에서 0.718*로 한 번에 떨어진다.

**Row 5 (Mar 9 2026).** *autoresearch round 1*. *카르파시가 LLM agent로 hyperparameter를 자동 sweep*했다 ([X 글타래](https://x.com/karpathy/status/2031135152349524125)). 320개 실험. NorMuon, cautious WD, value embeddings, smear, backout 같은 *작은 수정*들의 *조합*. *1.80시간*. *val_bpb 0.71808, CORE 0.2690*. *GPT-2를 능가*한 최단 기록.

**Row 6 (Mar 14 2026).** autoresearch round 2. *1.65시간*까지 줄어든다. 하지만 *CORE는 0.2626*으로 약간 떨어진다 — GPT-2를 넘지만 round 1보다 *간발의 차*다. 시간을 줄이면 CORE가 *반드시* 함께 올라가지는 않는다는 사실의 *증거*다. *trade-off*가 보인다.

이 표가 우리에게 말하는 것은 무엇인가? *진보는 누적된다*는 것이다. fp8 한 줄, batch 한 줄, 데이터 한 줄, hyperparameter 한 무더기 — 각각이 *작은 폭*이지만, *합쳐서* 168시간을 *1.65시간*으로 만들었다. 우리가 책 5~6장에서 본 *모든 작은 다이얼*들이 이 표 안에 *살아 있다*.

그리고 더 중요한 사실. *우리의 1h47m 보고서*는 이 표의 *어디쯤*에 있는가? Row 5와 Row 6 *사이*다. Round 1을 따라간 결과다. *카르파시 본인의 기록*과 *분 단위*로 같다는 뜻이다. 우리가 nanochat을 *그대로 펴서* 돌리면 그게 가능하다. 책의 *처음부터 끝까지*가 의미하는 게 그것이다.

---

## 11.5 그러니 우리의 모델을 *세상에 내놓자*

증거의 페이지가 박혔다. 우리의 모델이 *진짜로* GPT-2를 넘었다는 사실이 한 장의 markdown으로 박혔다. *그러면 이제 무엇을 하나*?

책에서 한 발 더 나간다. 이 모델을 *남에게 보여준다*. 친구에게 *대화 URL을 보낸다*. *책 너머의 행동*이다.

방법은 두 가지가 있다. *모델을 공유*하거나, *대화창을 공유*하거나.

### 모델을 공유하는 법 — Hugging Face Hub에 한 줄

학습된 체크포인트는 `~/.cache/nanochat/chatsft_checkpoints/d26/` 또는 `chatrl_checkpoints/d26/` 안에 있다. *크지 않다* — 620M 파라미터에 fp32 기준 ~2.5GB, bf16이면 ~1.2GB. Hugging Face Hub에 *한 줄*로 올릴 수 있다.

```bash
huggingface-cli upload my-username/my-nanochat-d26 \
    ~/.cache/nanochat/chatsft_checkpoints/d26/ \
    --repo-type=model
```

`huggingface-cli login`을 미리 한 번 해두면 된다. 다 올라가면 `https://huggingface.co/my-username/my-nanochat-d26`에 모델 페이지가 생긴다. *다른 사람이 그 페이지에서 한 번에 받아 갈 수 있는 자리*다.

`report.md` 한 페이지를 *모델 카드(README.md)*로 그대로 붙여두면 더 좋다. *이 모델이 무엇이고, 어떻게 학습됐고, 어떤 수치에 도달했는지*가 *증거와 함께* 노출된다. 우리가 11.2절에서 본 그 페이지가, *전 세계 누구나*가 보는 *모델 페이지*가 된다.

### 대화창을 공유하는 법 — ngrok 한 줄

GPU 노드에서 직접 `chat_web`을 띄울 수도 있다.

```bash
python -m scripts.chat_web
```

기본 포트는 8000이다. 로컬에서 `http://localhost:8000`으로 열린다. 그런데 우리는 *원격 GPU 서버*에서 돌리고 있는 경우가 많다. 친구에게 *공개 URL*을 보내려면 *ngrok*이라는 도구를 한 줄 띄우는 게 가장 간단하다.

```bash
ngrok http 8000
```

ngrok이 *임시 공개 URL*을 발급해준다. `https://xxxx-xxx-xxx.ngrok-free.app` 같은 형태다. 그 URL을 친구에게 보내면, 친구는 *자기 브라우저*에서 *우리의 nanochat*과 대화할 수 있다.

*친구의 첫 메시지가 이런 식*이 될 것이다.

> Q: *"Who built you?"*
> A: *"I'm nanochat, a small language model trained from scratch. My current operator is 토비."*

(8장에서 identity 합성 데이터로 박아둔 정체성이 *여기서 진짜로* 살아 있는 모습을 본다. 우리가 *2 epochs* 동안 1000줄의 합성 대화로 가르친 *그 정체성*이, 친구의 첫 질문 한 줄에 *답으로* 돌아온다.)

또는 친구가 GSM8K 스타일의 산수를 던진다.

> Q: *"If I have 8 apples and give 3 away, how many do I have?"*
> A: *"Let me work this out. I start with 8 apples. I give away 3. So 8 - 3 = 5. The answer is 5. #### 5"*

(9장에서 RL로 다듬은 *답안 형식*이 *그대로* 작동한다. 친구는 그게 *우리가 가르친 형식*인 줄 모르고 그저 *깔끔하다*고 느낀다.)

여기까지 오면 우리는 *책 너머*에 와 있다. 책을 *덮어도* 자기 모델을 *돌리고*, *공유하고*, *친구의 첫 질문*을 받는다. 그 순간 우리는 더 이상 *책을 읽는 사람*이 아니라 *모델을 가진 사람*이다.

---

## 11.6 마무리 — 도장 한 번을 잘 찍는다는 것

11장은 짧다. 자랑이 아니라 *정리*이기 때문이다. 그리고 정리란 원래 *수수한 일*이다.

`nanochat/report.py`는 *400줄*의 작은 모듈이다. *수다스러운* 도구도, *비싼* 인프라도 아니다. 학습이 시작될 때 *git commit과 GPU와 시각*을 박아두고, 단계마다 *덤덤히 한 줄*씩 적고, 마지막에 *한 페이지로 모은다*. 그게 전부다. *그게 전부여서* 우리가 펴서 읽을 수 있고, *고칠 수 있고*, 자기 보고서에 *한 줄을 더할 수* 있다.

그 전부가, 우리가 책 한 권을 통과해 만든 *증거*가 된다. *Commit 6ed7d1d (clean) / val_bpb 0.71808 / CORE 0.2690 / Total wall clock time 1h47m.* 이 *네 줄*만 있으면 다른 사람이 *우리를 의심하지 않는다*. 의심한다면 *그 commit을 체크아웃해서 직접 돌리면 된다*. 도장이 *그렇게* 작동한다.

우리가 책의 *마지막에서 두 번째* 장에 와서 깨닫는 것이 있다. *증거의 페이지*가 박힌다는 것은, *책이 끝났다*는 뜻이 아니다. *남들이 우리를 따라할 수 있게 됐다*는 뜻이다. 우리의 commit과 우리의 수치를, *누군가는 자기 GPU에서 다시 돌릴 것이다*. 우리의 leaderboard 위에, *누군가는 자기 한 줄을 더할 것이다*. nanochat의 README 표가 그렇게 *시간이 가면서 늘어났듯이*.

그러니 *report.md*를 박는 일은, *책의 마지막 도장*이 아니라 *책 너머로 가는 문*이다. 우리의 markdown 한 페이지가 *다른 누군가의 시작점*이 된다. 그리고 *우리 자신의 두 번째 학습*의 시작점도 된다 — 한 달 뒤 우리가 *더 좋은 한 줄*을 leaderboard에 더할 때, 그 출발은 *지금의 이 page*다.

이 문을 열어두고, 다음 장으로 넘어가자. 우리가 따라온 이 8천 줄의 코드가 *사실은 무엇이었는가*, 그리고 *나만의 한국어 챗봇*을 만들고 싶다면 *어디부터 손대야 하는가*. 책의 *작별*이 12장에서 우리를 기다린다.

---

> **[CPU/MPS 10분] 실습 — 자기 `report.md`를 직접 박아보기**
>
> 1장에서 따라 했던 *CPU 미니 학습*을 한 번이라도 돌렸다면, `~/.cache/nanochat/report/` 폴더에 *이미 markdown 조각들*이 쌓여 있을 것이다. *직접* 한 페이지로 모아보자.
>
> ```bash
> source .venv/bin/activate
> python -m nanochat.report generate
> ```
>
> 같은 디렉토리에 `report.md`가 한 부 *복사*되어 떨어진다. 펴서 *11.2절의 페이지*와 한 줄씩 비교해보자.
>
> - `### Bloat / Lines` 가 우리 환경에서 *몇 줄*인가? (clone 이후 작업한 양에 따라 다르다.)
> - `Total wall clock time`이 *몇 분*인가? CPU에서는 30분~수 시간일 수 있다.
> - `CORE`와 `ChatCORE` 줄이 *비어 있을* 수도 있다 — `--core-metric-every=-1`로 평가를 껐다면 그 자리에 *`-`*가 그대로 박힌다. 그것도 *정직한 증거*다.
>
> 자기 `report.md`를 친구에게 보내며 *책의 한 장*을 *자기 결과*로 갈음해 두자. 그게 *책 너머*로 가는 첫걸음이다.
