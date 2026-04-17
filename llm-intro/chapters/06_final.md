# 6장. 오픈 모델 파인튜닝 — QLoRA로 한국어 태스크 붙이기

<!-- 개정: 2026-04-17 Critical C1(도입 메타 제거, 상황 가정으로 뒤집기), C2(마무리 절 3박 압축 + 중복 요약 제거), Should 6건 반영, 분량 약 3,400자 감축 -->

월요일 아침 슬랙이 울린다. "간단한 파인튜닝 한번 해 주실 수 있죠?" 라는 한 줄이 올라와 있다. 5장까지 따라왔다면 머리에는 Pretraining, Scaling Laws, Instruction Tuning, RLHF가 대략 들어와 있다. 그런데 막상 이 한 줄을 받아 드는 순간 손이 어디로 가야 할지 잠깐 얼어붙는다. 도구는 뭘 까는가. 모델은 뭘 고르는가. 데이터는 어떤 모양이어야 하는가. GPU는 있는가. 그 얼어붙는 순간을 이 장에서 미리 풀어 두자. 이야기로 따라가 봤던 정렬의 한가운데를 이제 **우리 손으로** 건드려 본다. 정확히는 SFT(Supervised Fine-Tuning) 한 조각이다. RM과 PPO는 이번에도 이야기로 남겨 두지만, "Base 모델에 지시를 따르는 습관을 입히는" 가장 실전적인 지점은 오늘 직접 해 본다. 사용할 도구는 HuggingFace 생태계의 네 라이브러리(`transformers`, `peft`, `trl`, `bitsandbytes`). 모델은 Llama 3 8B Instruct. 기법은 **QLoRA**. 태스크는 4장부터 우리를 따라온 "사내 개발 문서 요약/Q&A" 그 문제다. 같은 문제를 다르게 푼다. 같이 얹어 보자.

## 6.1 지금 우리가 어디에 있나

매 장 같은 자리에 서는 이 지도를 이번에도 먼저 펴 두자. 책 한 권이 걷는 길 위에서 6장이 어느 좌표인지부터 맞추고 들어간다.

```
  서문 ─ 1장 ─ 2장 ─ 3장 ─ 4장 ─ 5장 ─ ★ 6장 ─ 7장 ─ 8장 ─ 9장 ─ 10장
  (왜) (지도) (토큰) (어텐션) (from  (스케일·  (QLoRA   (API ·  (RAG) (통합) (다음)
                              scratch) 정렬)    파인튜닝) Spring)
                              ──────────────   ───────────────────────
                              같은 "사내 개발 문서 요약/Q&A"를 네 번
```

4·6·7·8장의 공통 태스크가 한 문제라는 사실을 다시 상기하자. 4장에서 1~3MB 한국어 코퍼스로 미니 GPT를 **밑바닥부터** 쌓아 풀었다. 품질은 귀여웠지만 "LLM이 조건부 확률 + 샘플링이구나"가 몸에 들어왔다. 5장은 그 미니 모델이 왜 "요약해 줘"에 요약을 안 해 줬는지, 그 공백을 정렬이 어떻게 메우는지를 역사로 따라갔다. 이제 6장은 그 실물을 **오픈 가중치 모델 위에서** 쥐어 본다. Llama 3 8B는 Meta가 15T 토큰으로 먹여 구운, 4장 미니 GPT의 **1,000만~1억 배** 규모짜리 거인이다. 그 어깨 위에 얇은 층 하나를 더 얹는 것이 이 장의 일이다. 7장은 같은 태스크를 API로, 8장은 RAG로 푼다. 네 답을 6장 끝에서 단단히 하고 넘어가자.

한 가지 미리 인정하자. 파인튜닝은 처음 해 보면 묘하게 **허무하다**. 학습 스크립트 `.train()` 한 줄 아래로 수십 분~몇 시간이 조용히 흐른다. 3·4장처럼 코드 한 줄씩 쌓는 맛이 이 장에는 없다. 대신 다른 근육을 얻는다. 거대한 오픈 모델을 **골라 오고, 데이터 쌍을 만들고, 설정을 맞추고, 결과를 평가하는** 현업 감각이다.

---

## 6.2 왜 전체를 안 고치고 저랭크만 고치는가 — PEFT·LoRA·QLoRA

5장 정렬 파이프라인의 SFT 단계를 한국어 도메인에 맞춰 **다시 돌리는** 장면을 상상해 보자. 원칙대로라면 Llama 3 8B의 80억 파라미터를 전부 역전파로 업데이트해야 한다. **풀 파인튜닝(full fine-tuning)**이다. 문제는 비용이다.

풀 파인튜닝이 요구하는 것을 세어 보자. 80억 파라미터를 bfloat16으로 들고 있으면 가중치만 **16GB**, Adam 옵티마이저 상태가 FP32 1·2차 모멘트로 **64GB**, 그래디언트 16GB, 활성값 수십 GB. 대략 **100~160GB VRAM**이다. A100·H100 두 장을 기본으로 요구한다. 웬만한 스타트업 서버룸도 이 숫자 앞에서 멈칫한다.

그렇다면 질문은 이렇게 바뀐다. **꼭 전체 파라미터를 건드려야 할까?** 도메인 적응을 한다고 해서 80억 개 전체가 다 움직여야 할까?

이 질문의 답이 **PEFT(Parameter-Efficient Fine-Tuning)** 가족이다. 작은 모듈만 학습시키고 원본은 얼린다(frozen). 2021년 Microsoft의 **LoRA(Low-Rank Adaptation)**가 대표 멤버이고, 2023년 University of Washington 팀이 여기에 4비트 양자화를 결합한 것이 **QLoRA**다. 오픈 모델 파인튜닝의 표준 기법이라 해도 무리가 없다.

LoRA의 아이디어는 한 줄로 졸일 수 있다. **"모델 원본 가중치 `W`는 얼려 두고, 그 위에 `W + ΔW` 꼴로 얹는 `ΔW`를 저랭크(low-rank) 행렬 두 개의 곱으로 근사한다."** 그림으로 먼저 잡아 보자.

```
  원본 레이어 (얼어 있음)          LoRA 어댑터 (학습됨)
  ┌─────────────────────┐        ┌────────┐   ┌────────┐
  │                     │        │        │   │        │
  │       W             │   +    │   A    │ × │   B    │
  │  (예: 4096×4096)    │        │(4096×r)│   │(r×4096)│
  │                     │        │        │   │        │
  └─────────────────────┘        └────────┘   └────────┘

  파라미터 수:  16,777,216                  2 × 4,096 × r
  r=16일 때:                                131,072  (≈ 0.78%)
```

`W`는 보통 어텐션 블록의 Q/K/V/Out 프로젝션 행렬, FFN의 업·다운 프로젝션 행렬 같은 큰 정사각 행렬들이다. 그 위에 덧붙는 `ΔW = A · B` 두 조각만 새로 학습시킨다. `A`는 `d × r`, `B`는 `r × d`. `r`이 **랭크(rank)**이고 보통 8, 16, 32, 64 같은 작은 수로 잡는다. `d=4096`, `r=16`이면 `131,072`. 원본이 `16,777,216`이니 **학습 파라미터가 원래의 0.78%**로 쪼그라든다. 8B 모델 전체로 보면 대략 **4천만~1억** 파라미터만 학습시키면 된다. 나머지 79억 개는 얼어 있다.

의심이 따라온다. **"그렇게 조금만 고쳐서 도메인 적응이 제대로 되나?"** 답은 두 갈래. 경험적으로 LoRA 논문과 후속 연구가 다양한 태스크에서 "풀 파인튜닝에 근접한 성능"을 반복 보였다. 이론적으로는 큰 사전학습 모델의 업데이트 행렬이 **내재 차원(intrinsic dimension)이 낮다**—도메인 적응 같은 국소적 변화는 파라미터 공간의 좁은 부분공간 안에서 표현되고, 그 부분공간을 `A · B`로 근사한 것이 LoRA다.

학습 파라미터가 1%로 줄면 학습 상태 메모리도 그만큼 줄어든다. 옵티마이저 64GB가 0.6GB로, 그래디언트 16GB가 0.16GB로 내려앉는다. 그런데 **원본 가중치 16GB**는 순전파에 꼭 필요하기 때문에 얼린 채로도 VRAM에 올려 놓아야 한다. 16GB 이하의 소비자 GPU에서는 이 16GB만으로도 이미 턱이 찬다.

**QLoRA**는 이 마지막 16GB를 한 번 더 접는다. 원본 가중치를 **4비트**로 양자화해 메모리에 올리면 16GB가 **4~5GB**로 내려간다. 기발함은 세 가지. 첫째 **NF4(Normal Float 4)**—가중치가 대체로 정규분포를 따른다는 관찰을 근거로 비트 분포를 맞춘 포맷. 둘째 **이중 양자화**—양자화 상수까지 한 번 더 양자화한다. 셋째 학습 시에만 **부분적으로 dequantize**해 16비트로 계산하고, 저장은 4비트로 되돌린다. 계산 정확도는 지키면서 메모리만 영리하게 아낀다.

결과는 극적이다. Llama 3 8B 원본 16GB → QLoRA 로딩 시 약 **5GB**. 어댑터 수백 MB와 학습 상태 1~2GB가 얹혀도 총 **8~10GB VRAM**. 소비자 GPU 한 장에 들어온다. "1.5장의 GPU" 대신 "1장의 GPU"로 만들어 준 기법이다.

한 문장으로 QLoRA를 요약해 보자. **"원본은 4비트로 얼려 두고, 그 위에 저랭크 어댑터만 16비트로 학습시킨다."** 이 한 줄이 2024~2025년 오픈 모델 파인튜닝의 기본 문법이다. 수식 한 줄까지 같이 붙여 두고 싶다면 이렇다.

> `h = W_quantized(x) + (B · A)(x)`

`W_quantized`는 4비트로 얼어 있고, `A`와 `B`만 bfloat16으로 경사 하강한다. 이 공식이 머리에 들어오면, 이제 실제로 돌려 볼 차례다.

---

## 6.3 VRAM 현실 — 16GB로 어디까지 가는가

이론은 깔끔하지만 현실은 숫자다. 커뮤니티 경험을 일관되게 종합하면 대략 이런 그림이다.

> "The absolute minimum is around 12–16 GB VRAM using QLoRA ... for smoother performance, 24 GB is realistic minimum." [커뮤니티:r/LocalLLaMA]

이 두 문장이 이 장의 모든 VRAM 이야기를 압축한다. Llama 3 8B를 QLoRA로 파인튜닝할 때, 시퀀스 길이(seq_len)와 배치 크기(batch_size)를 어떻게 잡느냐에 따라 VRAM이 꽤 민감하게 움직인다. 2025년 전후의 일반적인 감각은 다음 표 정도로 요약된다.

| GPU | VRAM | seq_len | batch_size | gradient accumulation | 체감 |
|---|---|---|---|---|---|
| RTX 3060 / T4 (Colab 무료) | 16GB | 512 | 1 | 16 | 간당간당. LoRA rank 16까지 |
| RTX 4080 / A5000 | 16~24GB | 1024 | 2 | 8 | 안정. rank 32, 짧은 epoch 가능 |
| RTX 4090 / A6000 | 24GB | 2048 | 4 | 4 | 원활. rank 64, 3 epoch |
| A100 40GB / L40S | 40GB+ | 4096 | 8+ | 2 | 여유. 실전 프로젝트급 |
| A100 80GB / H100 | 80GB | 8192 | 16+ | 1 | QLoRA는 오버킬. 풀 파인튜닝 고려 |

이 표 앞에서 두 가지는 기억해 두자. 하나, 숫자는 **8B 기준**이다. 13B는 1.5배, 70B는 QLoRA여도 24GB 두 장이 필요하다. 다른 하나는 **gradient accumulation**이 VRAM 부족을 시간으로 바꿔 주는 협상 카드라는 점이다. 무료 T4에서는 시간을, 4090에서는 메모리를 주로 아낀다.

16GB가 최소지만 12GB에서도 돌린 사례가 커뮤니티에 올라온다. seq_len 256, rank 8, batch 1 고정이라 **품질이 아슬아슬**한 영역이다. PoC로는 쓸 만하지만 프로덕션용은 16GB 이상을 권한다. **GPU 없는 독자는 이 장을 완주할 수 없는가?** 그렇지 않다. 6.9절에서 세 가지 무료 경로를 정리한다. 지금은 GPU가 있다는 전제로 표준 경로를 따라간다.

---

## 6.4 HuggingFace 스택 — 네 라이브러리가 각자 무엇을 하는가

코드를 돌리기 전에, 이번 실습에서 쓸 네 라이브러리가 어떤 역할 분담을 하는지부터 한 번 정리해 두자. 이 구분이 머리에 들어오면 이후 에러 메시지를 읽을 때 훨씬 덜 찜찜하다.

```
┌─────────────────────────────────────────────────────────────┐
│  transformers  │  모델·토크나이저·Config의 본체 창고.         │
│                │  Llama 3 8B Instruct 가중치와 토크나이저를  │
│                │  from_pretrained 한 줄로 불러온다.           │
├────────────────┼────────────────────────────────────────────┤
│  bitsandbytes  │  4비트·8비트 양자화 커널. QLoRA의 핵심.     │
│                │  BitsAndBytesConfig로 로딩 방식을 지정한다.  │
├────────────────┼────────────────────────────────────────────┤
│  peft          │  LoRA/QLoRA 어댑터 구조 그 자체.            │
│                │  LoraConfig로 r·alpha·target_modules를 잡고 │
│                │  get_peft_model로 원본 모델에 얹는다.        │
├────────────────┼────────────────────────────────────────────┤
│  trl           │  SFT·DPO·PPO 등 정렬 기법의 학습 루프.       │
│                │  SFTTrainer가 이 장의 주연이다. Hugging     │
│                │  Face Trainer 위에 프롬프트 포맷·토큰      │
│                │  마스킹·패딩 처리를 얹어 놓았다.             │
└─────────────────────────────────────────────────────────────┘
```

`transformers`가 "모델과 토크나이저"를 제공하고, `bitsandbytes`가 그 모델을 "4비트로 로드"하고, `peft`가 거기에 "LoRA 어댑터를 얹고", `trl`의 `SFTTrainer`가 "실제 학습 루프를 돌린다." 역할이 깔끔하게 네 등분이다. `peft`의 `get_peft_model`은 `transformers` 모델 객체를 입력으로 받고, `trl`의 `SFTTrainer`는 `peft` 모델을 자연스럽게 받는다. Lego 블록처럼 맞물린다.

이 책 집필 시점(2026년 초) 기준 무난한 조합은 이렇다.

```
transformers    >= 4.45
peft            >= 0.12
trl             >= 0.11
bitsandbytes    >= 0.43
accelerate      >= 0.34
```

`accelerate`는 네 라이브러리 사이에서 디바이스 매핑·분산 학습을 매개한다. 버전이 살짝만 어긋나도 `ImportError`나 미묘한 `RuntimeError`가 나기 쉬우니 실습 저장소의 `requirements.txt` 핀을 그대로 쓰자. 그리고 **HuggingFace 스택은 매 분기 얼굴을 바꾼다.** 큰 틀(네 라이브러리가 어디서 만나는지)은 유지되지만 인자 이름·기본값은 슬쩍 바뀐다. 6개월 뒤 독자라면 공식 문서 최신 예제를 대조하는 습관을 붙이자.

자, 준비는 됐다. 이제 데이터부터 만진다.

---

## 6.5 데이터셋 준비 — 공통 태스크를 SFT 쌍으로 바꾸기

5장에서 본 SFT 템플릿 기억나는지. `### Instruction:`과 `### Response:`로 "지시-응답" 쌍을 수천~수만 건 모아 파인튜닝하는 방식. Llama 3는 자체 채팅 템플릿이 따로 있지만, 구조적으로 하는 일은 같다. 우리가 지금 해야 할 첫 일은 **4장에서 쓴 한국어 코퍼스를 이 SFT 쌍 포맷으로 바꾸는 것**이다.

4장의 "사내 개발 문서" 코퍼스를 상상해 보자. 모두의 말뭉치·나무위키 덤프에서 기술 문서를 골라 문단 단위로 잘라 둔 상태다. SFT는 **"지시 → 답변"** 쌍을 요구하니, 각 문단에 요약을 짝으로 붙여야 한다. 문제는 요약 쪽이다. 수천 건을 사람이 직접 요약해 줄 라벨러가 없다면, 그 정답 문자열은 **어디서** 오는가?

실무 해법은 두 가지다. 첫째, **합성 데이터(synthetic data)**. 이미 정렬된 상용 모델(GPT-4, Claude 등)에게 요약을 시켜 정답으로 쓴다. 스승의 지식을 학생에게 옮기는 것이라 **distillation** 계열로 분류된다. 둘째, **사람이 직접 작성**. 품질은 높지만 비싸고 느리다.

이 책은 첫 경로를 택한다. 한 가지 짚어 두자. **합성 데이터로 학습한 모델의 상한선은 스승 모델의 품질이다.** GPT-4의 잘못된 습관까지 같이 학습된다. 상용 모델 이용 약관이 "다른 경쟁 모델 학습에 출력을 쓰지 말 것"을 명시하는 경우가 많아, 사내 프로젝트에서 강행하려 하면 법무팀과 껄끄러운 대화가 생길 수 있다. **프로덕션으로 가려면 라이선스와 약관을 반드시 재확인**하자. 실습 저장소는 비상업·연구 범위로 제공한다.

이제 쌍을 만들어 보자. 아래 스크립트는 4장에서 쓴 문단 텍스트 파일(`corpus.jsonl`)을 읽어 OpenAI API로 요약을 붙이고, SFT 포맷인 `sft_pairs.jsonl`로 저장한다.

```python
# make_sft_pairs.py
import json, os, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SYSTEM = "너는 신중한 한국어 개발 문서 요약가다. 입력된 문단을 3문장 이내로 간결하게 요약한다."

def summarize(text: str) -> str:
    """스승 모델에게 요약을 시켜 정답 문자열을 받아 온다."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": f"다음 문단을 3문장 이내로 요약해 줘:\n\n{text}"},
        ],
        temperature=0.3,
        max_tokens=300,
    )
    return resp.choices[0].message.content.strip()

def main(src="corpus.jsonl", dst="sft_pairs.jsonl", limit=2000):
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for i, line in enumerate(fin):
            if i >= limit:
                break
            doc = json.loads(line)
            try:
                summary = summarize(doc["text"])
            except Exception as e:
                print(f"[{i}] skip: {e}")
                continue
            fout.write(json.dumps({
                "instruction": "다음 사내 개발 문서를 3문장 이내로 요약해 줘.",
                "input": doc["text"],
                "output": summary,
            }, ensure_ascii=False) + "\n")
            if i % 50 == 0:
                print(f"[{i}] ok")
            time.sleep(0.2)  # API rate limit 여유

if __name__ == "__main__":
    main()
```

`temperature=0.3`은 의도적으로 낮게 잡았다. 학습 정답은 **일관돼야** 한다. 0.7로 올리면 같은 문단의 요약 스타일이 들쭉날쭉해져 모델이 "이 태스크는 어떤 형식이지"를 학습하는 데 혼선이 생긴다. 4장 디코딩 루프의 손잡이가 여기서 **학습 데이터 품질 손잡이**로 바뀐 셈이다. `max_tokens=300`은 길이 안전장치, `time.sleep(0.2)`는 rate limit 대응이다.

생성된 `sft_pairs.jsonl` 한 줄은 대략 이런 모양이 된다.

```json
{"instruction": "다음 사내 개발 문서를 3문장 이내로 요약해 줘.",
 "input": "본 문서는 사용자 인증 모듈의 설계를 기술한다. OAuth 2.0 기반이며 ...",
 "output": "이 문서는 OAuth 2.0 기반의 사용자 인증 모듈 설계를 다룬다. Access Token과 Refresh Token을 분리 관리하는 구조다. 토큰 만료 시 자동 재발급 정책에 따른다."}
```

2,000건은 실전 기준 **꽤 적은 편**이다(오픈 SFT 데이터셋은 보통 1만~10만 단위). 다만 **LoRA는 적은 데이터에도 잘 수렴**해 2,000건으로도 "요약 습관"은 확실히 잡힌다. 이 규모는 API 비용을 커피 한 잔 수준으로 묶고 Colab T4에서 1~2시간 안에 끝내려는 타협치다. 회사 프로젝트라면 5,000~20,000건으로 시작해 품질을 보고 늘려 가자.

학습/검증/테스트 분할도 꼭 해 두자. 2,000건이면 1,800 / 100 / 100 정도. 저장소에 한 줄짜리 분할 스크립트를 같이 넣어 두었다.

```python
import json, random
random.seed(42)

with open("sft_pairs.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f]
random.shuffle(rows)

splits = {"train": rows[:1800], "val": rows[1800:1900], "test": rows[1900:]}
for name, data in splits.items():
    with open(f"sft_{name}.jsonl", "w", encoding="utf-8") as f:
        for r in data:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
print({k: len(v) for k, v in splits.items()})
```

val은 학습 중 loss를 모니터링하는 용도, test는 학습이 끝난 뒤 before/after 비교용. 이 분할을 뒤섞어 쓰면 나중에 평가 숫자가 **수상하게 좋아 보이는** 일이 생긴다. 한 번 정해 두면 손대지 않는 편이 낫다.

---

## 6.6 학습 스크립트 — `BitsAndBytesConfig`, `LoraConfig`, `SFTTrainer`

이제 본격적으로 파인튜닝 스크립트를 쓴다. 핵심은 50줄 안쪽이다. 먼저 환경 설치부터.

```bash
pip install "transformers>=4.45" "peft>=0.12" "trl>=0.11" \
            "bitsandbytes>=0.43" "accelerate>=0.34" datasets
huggingface-cli login   # Llama 3 가중치 접근 토큰 입력
```

Llama 3는 Meta의 Acceptable Use Policy 동의가 필요하다. HuggingFace 계정으로 모델 페이지(`meta-llama/Meta-Llama-3-8B-Instruct`)에서 "Request access"를 누르고 승인을 받아야 `from_pretrained`가 통과한다. 대개 몇 분에서 몇 시간 안에 승인된다.

스크립트는 다섯 조각. (1) BitsAndBytes 설정, (2) 모델·토크나이저 로드, (3) LoRA 설정, (4) 데이터셋 포맷팅, (5) SFTTrainer 초기화 및 학습.

```python
# train_qlora.py
import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

BASE_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
OUTPUT_DIR = "./llama3-8b-doc-summary-lora"

# (1) 4비트 양자화 설정 — QLoRA의 심장
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NF4 포맷
    bnb_4bit_compute_dtype=torch.bfloat16,  # 계산은 bf16
    bnb_4bit_use_double_quant=True,      # 이중 양자화
)

# (2) 모델·토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token   # Llama 3는 pad_token이 없다
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
model = prepare_model_for_kbit_training(model)  # 4비트 학습 호환 처리

# (3) LoRA 어댑터 설정
lora_config = LoraConfig(
    r=16,                                # 랭크
    lora_alpha=32,                       # 스케일 계수 (보통 r의 2배)
    target_modules=[                     # 어디에 어댑터를 붙일지
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# 출력 예: trainable params: 41,943,040 || all params: 8,072,204,288 || trainable%: 0.5196

# (4) 데이터셋 로드 및 포맷팅
def format_example(row):
    """Llama 3 chat template으로 감싼다."""
    messages = [
        {"role": "system",    "content": "너는 신중한 한국어 개발 문서 요약가다. 입력 문단을 3문장 이내로 요약한다."},
        {"role": "user",      "content": f"{row['instruction']}\n\n{row['input']}"},
        {"role": "assistant", "content": row["output"]},
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False)

train_ds = load_dataset("json", data_files="sft_train.jsonl", split="train")
val_ds   = load_dataset("json", data_files="sft_val.jsonl",   split="train")

# (5) SFTTrainer 설정 및 학습
sft_config = SFTConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,       # 실효 배치 16
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=100,
    bf16=True,
    max_seq_length=1024,
    packing=False,                       # 짧은 샘플 이어붙이기 비활성화
    report_to="none",
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    formatting_func=format_example,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model(OUTPUT_DIR)   # LoRA 어댑터만 저장됨 (수백 MB)
```

이 50줄이 오픈 모델 파인튜닝의 현실적 최소 단위다. 한 조각씩 왜 이렇게 썼는지 풀어 두자.

`BitsAndBytesConfig`의 네 필드가 QLoRA의 심장이다. `load_in_4bit`는 "4비트 저장" 선언, `nf4`는 6.2절의 NF4 포맷, `compute_dtype=bfloat16`이 **저장은 4비트지만 계산은 bf16**이라는 dequantize 전략의 핵심이다. `use_double_quant`는 메모리를 조금이라도 더 아끼려면 켜 두자.

`prepare_model_for_kbit_training`은 임베딩·LayerNorm을 fp32로 돌리고 gradient checkpointing을 켠다. **이 줄을 빼먹으면 첫 스텝부터 NaN이 터진다. 토비도 반나절 날려 본 함정이다.**

`LoraConfig`의 `target_modules`는 `q_proj`, `k_proj`, `v_proj`, `o_proj`(3장 어텐션 네 프로젝션)와 `gate_proj`, `up_proj`, `down_proj`(FFN SwiGLU 세 행렬). **이 일곱 전부에 얹는 것이 Llama/Mistral 표준**이다. 어텐션만 붙이는 것보다 FFN까지 포함해야 품질이 잘 나온다는 QLoRA 원 논문 결론을 현장이 그대로 따른다. `r=16`이 무난한 기본값, `lora_alpha=32`는 관습적으로 `2 * r`.

`SFTConfig`에서 `batch_size=2, accumulation=8`이 실효 배치 16을 만든다. `learning_rate=2e-4`는 LoRA 경험값으로 풀 파인튜닝의 1e-5~5e-5보다 **한두 자릿수 높다**. 학습 파라미터가 적어 큰 스텝도 안정적이다. `warmup_ratio=0.03` + cosine은 2024년 이후 디폴트. `packing=False`는 **샘플 경계가 섞이지 않아** 디버깅이 쉽다.

자, 이제 실행하자.

```bash
python train_qlora.py
```

A6000(48GB)에서 대략 2시간, 4090(24GB)에서 3~4시간, Colab T4에서 6~8시간 걸린다. 학습이 돌아가는 동안 로그가 어떻게 찍히는지 이어서 같이 읽어 보자.

---

## 6.7 학습 로그 읽기 — loss 곡선과 마주치는 두 가지 문제

학습이 시작되면 터미널에 이런 로그가 흐른다.

```text
{'loss': 2.4183, 'grad_norm': 1.82, 'learning_rate': 5.5e-05, 'epoch': 0.02}
{'loss': 2.1947, 'grad_norm': 1.64, 'learning_rate': 1.1e-04, 'epoch': 0.04}
{'loss': 1.9206, 'grad_norm': 1.45, 'learning_rate': 1.6e-04, 'epoch': 0.06}
{'loss': 1.7458, 'grad_norm': 1.29, 'learning_rate': 2.0e-04, 'epoch': 0.08}
{'loss': 1.6103, 'grad_norm': 1.18, 'learning_rate': 2.0e-04, 'epoch': 0.09}
...
{'loss': 1.3521, 'grad_norm': 0.97, 'learning_rate': 1.9e-04, 'epoch': 0.50}
{'loss': 1.2084, 'grad_norm': 0.88, 'learning_rate': 1.6e-04, 'epoch': 1.00}
{'eval_loss': 1.2312, 'eval_runtime': 48.2, 'epoch': 1.00}
{'loss': 1.0938, 'grad_norm': 0.81, 'learning_rate': 1.2e-04, 'epoch': 1.50}
{'loss': 1.0124, 'grad_norm': 0.76, 'learning_rate': 7.2e-05, 'epoch': 2.00}
{'eval_loss': 1.1876, 'eval_runtime': 48.5, 'epoch': 2.00}
{'loss': 0.9472, 'grad_norm': 0.72, 'learning_rate': 2.9e-05, 'epoch': 2.50}
{'loss': 0.9085, 'grad_norm': 0.69, 'learning_rate': 2.0e-06, 'epoch': 3.00}
{'eval_loss': 1.1854, 'eval_runtime': 48.6, 'epoch': 3.00}
{'train_runtime': 7412.3, 'train_samples_per_second': 0.73, 'epoch': 3.0}
```

각 필드를 담담하게 읽어 보자. `loss`는 학습 배치의 cross-entropy. 처음 2.4에서 시작해 3 epoch 동안 0.9까지 떨어졌다—건강한 수렴이다. `eval_loss`는 val 세트 값. 1.23 → 1.19 → 1.19로 거의 정체다. **train_loss는 떨어지는데 eval_loss가 멈췄다**는 건 과적합 신호다. 3 epoch에서 멈춘 게 적절했다.

`grad_norm`은 학습 초반에 높고 점차 줄어드는 게 정상. 갑자기 튀어 오르면 **gradient explosion** 경고다. `learning_rate`는 cosine 스케줄에 따라 2e-4까지 올랐다가 마지막에 거의 0이 된다.

여기까지 매끄럽게 돌았다면 운이 좋은 쪽이다. 실전 파인튜닝에서 처음 해 보면 거의 반드시 마주치는 두 가지 문제가 있다. 미리 예방주사를 맞아 두자.

**문제 1 — 첫 스텝부터 loss가 NaN.**

```text
{'loss': nan, 'grad_norm': nan, ...}
```

로그가 `nan`으로 찍히기 시작하면 이후 학습은 의미가 없다. 원인은 대부분 세 가지다. (a) `prepare_model_for_kbit_training(model)`을 빼먹었다. (b) `bnb_4bit_compute_dtype`를 `float16`으로 잡았는데 수치 안정성이 떨어진다. `bfloat16`으로 바꾸는 편이 낫다. (c) 학습률이 너무 높다. 2e-4에서 시작해도 특정 모델에서는 터질 수 있다. 1e-4나 5e-5로 낮춰서 재시도하자.

**문제 2 — loss가 1.5~2.0 근방에서 내려가지 않음.**

```text
{'loss': 1.8423, 'epoch': 0.5}
{'loss': 1.8511, 'epoch': 1.0}
{'loss': 1.8287, 'epoch': 1.5}
```

수치가 미동도 하지 않는 상황. 원인은 주로 두 가지다. (a) 프롬프트 템플릿이 잘못됐다. `tokenizer.apply_chat_template`을 쓰지 않고 raw 문자열을 넘겼을 때, Llama 3 특유의 `<|begin_of_text|>`·`<|start_header_id|>` 등 특수 토큰이 제대로 박히지 않아 모델이 혼란스러워한다. (b) **`target_modules`가 비어 있거나 잘못됐다**. 예컨대 `q_proj`만 지정하고 나머지를 뺐다면 어댑터가 너무 좁아 학습이 거의 되지 않는다. `model.print_trainable_parameters()` 출력을 다시 확인해 학습 파라미터 비율이 0.3~0.8% 대에 있는지 본다. 0에 가깝다면 타깃 모듈 설정이 어긋난 것이다.

**두 문제 모두 예상할 수 있는 함정이다.** 미리 알고 들어가면 30분 만에 해결된다. 모르고 들어가면 반나절 날린다. 토비가 실제로 반나절을 날려 본 경험을 그대로 옮겨 놓았다고 생각하자.

학습이 끝났다면 **중요한 파일**은 `adapter_model.safetensors`와 `adapter_config.json` 두 개, 전체 수백 MB. 8B 원본(16GB)의 **1%도 안 되는 크기**다. 이 얇은 둘만 있으면 어디서든 같은 Base 위에 얹어 같은 효과를 재현할 수 있다. LoRA의 또 다른 매력이다.

---

## 6.8 평가의 첫 맛 — ROUGE의 한계와 수작업 채점

학습이 끝났으니 평가다. 실전에서 "파인튜닝했습니다"보다 중요한 말이 "**얼마나 좋아졌습니까**"다. 이 질문에 답하려면 두 가지가 필요하다. (a) before/after를 나란히 볼 테스트 셋, (b) 품질을 재는 기준.

먼저 before/after 샘플을 뽑자. 아래 스크립트는 100건짜리 test 세트에 대해 (1) 파인튜닝 전 Llama 3 8B Instruct와 (2) 파인튜닝 후 모델의 출력을 나란히 생성한다.

```python
# compare_before_after.py
import json, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

BASE = "meta-llama/Meta-Llama-3-8B-Instruct"
ADAPTER = "./llama3-8b-doc-summary-lora"

bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.bfloat16)
tok = AutoTokenizer.from_pretrained(BASE)
base_model = AutoModelForCausalLM.from_pretrained(BASE, quantization_config=bnb, device_map="auto")
tuned_model = PeftModel.from_pretrained(base_model, ADAPTER)

def ask(model, text: str) -> str:
    msgs = [
        {"role": "system", "content": "너는 신중한 한국어 개발 문서 요약가다. 입력 문단을 3문장 이내로 요약한다."},
        {"role": "user",   "content": f"다음 사내 개발 문서를 3문장 이내로 요약해 줘.\n\n{text}"},
    ]
    prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=200, temperature=0.3, do_sample=True)
    return tok.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()

with open("sft_test.jsonl", encoding="utf-8") as f, open("compare.jsonl", "w", encoding="utf-8") as out:
    for line in f:
        row = json.loads(line)
        before = ask(base_model, row["input"])
        after  = ask(tuned_model, row["input"])
        out.write(json.dumps({
            "input":  row["input"],
            "gold":   row["output"],
            "before": before,
            "after":  after,
        }, ensure_ascii=False) + "\n")
```

`PeftModel.from_pretrained`는 4비트 Base 위에 어댑터를 올린다. 어댑터의 경량성 덕에 "켰다 껐다" 하는 트릭으로 동작한다.

샘플 세 개를 눈으로 읽어 보자.

### 샘플 1 — 기대한 대로 좋아진 경우

**입력 문단:**
```
본 문서는 사용자 인증 모듈의 설계를 기술한다. OAuth 2.0 기반이며,
Access Token과 Refresh Token을 분리 관리한다. Access Token의 만료 시간은
1시간, Refresh Token은 30일로 설정된다. 토큰 갱신은 /auth/refresh 엔드포인트에서 이루어지며,
Refresh Token 탈취 대응을 위해 rotating 전략을 사용한다. ...
```

**Before (원본 Llama 3 8B Instruct):**
```
본 문서는 사용자 인증 시스템의 전체 설계를 담고 있으며, OAuth 2.0 프로토콜에 기반하여 구성된
견고한 인증 체계를 제공합니다. Access Token과 Refresh Token을 분리 관리하는 것이 특징이며,
토큰 탈취 상황에 대비한 다양한 보안 메커니즘이 포함되어 있습니다. 전반적으로 현대적인
인증 아키텍처를 따르며, 보안과 사용성을 모두 고려한 설계라 할 수 있습니다.
```

**After (QLoRA 파인튜닝):**
```
OAuth 2.0 기반 사용자 인증 모듈의 설계 문서다. Access Token(1시간)과 Refresh Token(30일)을
분리 관리하며, /auth/refresh 엔드포인트에서 갱신한다. 탈취 대응을 위해 rotating 전략을 쓴다.
```

Before는 **원문에 없는 칭찬**("견고한", "현대적인")을 끼워 넣고 세부 숫자·엔드포인트 이름을 빠뜨렸다. After는 숫자와 엔드포인트를 담고 군더더기가 거의 없다. "사내 문서 요약"의 감각에 훨씬 가깝다.

### 샘플 2 — 거의 차이가 없는 경우

**입력:** 짧은 FAQ 한 줄짜리 문단.

**Before:**
```
이 문서는 배포 전 체크리스트 항목을 안내한다. 테스트 통과, 보안 검토, 성능 측정을
사전에 수행해야 함을 강조한다. 배포 후 모니터링도 필수로 제시한다.
```

**After:**
```
배포 전 체크리스트 문서다. 테스트 통과, 보안 검토, 성능 측정을 수행해야 한다.
배포 후 모니터링이 필수다.
```

실질적으로 같은 수준. 입력이 짧고 단순하면 Base가 이미 잘 해서 파인튜닝 기여분이 미미하다. **전체 샘플의 40~50%는 before/after가 거의 같다.** 성능 측정은 "전체 평균"보다 **긴 문서·복잡한 문서의 개선**에 집중하는 편이 의미 있다.

### 샘플 3 — 오히려 나빠진 경우

**입력:** 코드 스니펫이 섞인 문단.

**Before:**
```
이 문서는 Kafka 컨슈머 그룹 설정 방법을 설명한다. `group.id`와 `auto.offset.reset` 옵션이
주요 설정이며, 재시작 시 오프셋 동작을 결정한다. 예제 코드와 설명이 함께 제공된다.
```

**After:**
```
Kafka 컨슈머 그룹 설정에 관한 문서다. group.id와 auto.offset.reset이 주요 옵션이다.
재시작 시 오프셋 동작을 결정한다.
```

After에서 백틱 문자가 사라졌다. 개발 문서 요약에 코드 이름이 **일반 텍스트로 섞이면** 마크다운 렌더링·검색 인덱싱에서 문제가 생긴다. 원인은 스승 모델의 학습 데이터에서 백틱이 일관되지 않았던 것이다. **학습 데이터 품질이 그대로 학생에게 이식된** 전형적인 예다. 데이터 생성 프롬프트에 "코드 이름은 백틱으로 감싸라"를 명시하거나 후처리 regex로 보정해야 한다.

파인튜닝이 **은총알이 아니다**. 어떤 케이스는 좋아지고, 어떤 케이스는 비슷하고, 어떤 케이스는 오히려 나빠진다. 이 **혼재된 결과를 정직하게 측정하는 도구**가 필요하다.

### ROUGE·BLEU의 한국어 한계

고전 지표인 **ROUGE**(요약)와 **BLEU**(번역)는 "정답과 생성물 사이의 n-gram 겹침"을 센다. 한국어에선 제약이 세 가지다. 첫째, **형태소 분석이 필요하다**—"빌려갔다"와 "빌려 갔다"가 n-gram 단위로 달라, 토큰화에 따라 점수가 10%p 이상 흔들린다. 둘째, **paraphrase에 약하다**—"OAuth 2.0 기반 인증"과 "OAuth 2.0을 기반으로 한 인증"은 의미는 같지만 n-gram이 다르다. 셋째, **사실성(factuality)을 못 잡는다**—원문에 없는 수식어를 덧붙인 Before 샘플 1이 ROUGE 점수는 더 잘 나올 수 있다. 겹치는 n-gram이 많기 때문이다.

실전에서는 세 가지 평가를 **같이 쓴다.**

- **ROUGE-L(F1)** — 방향은 잡아 주는 대략의 지표.
- **LLM-as-Judge** — GPT-4·Claude에게 두 요약을 보여주고 "어느 쪽이 낫냐"를 판정하게 시킴. 2024년 이후 사실상 표준이 되었다.
- **수작업 채점** — 테스트 셋에서 20~50건을 뽑아 사람이 직접 1~5점으로 점수를 매김. 가장 비싸지만 가장 믿을 만하다.

이 장에서는 간단한 수작업 채점표만 돌려 본다. LLM-as-Judge의 구현은 7장에서 API를 본격적으로 만질 때 다시 다룬다.

### 수작업 채점표

아래는 실제로 테스트 샘플 10건에 대해 저자가 직접 채점한 결과다. 기준은 네 축이다. 각 축 1~5점.

- **사실성(faithfulness)** — 원문에 없는 정보를 덧붙이지 않았는가
- **완결성(coverage)** — 중요한 정보를 빠뜨리지 않았는가
- **간결성(conciseness)** — 군더더기 없이 요약했는가
- **가독성(readability)** — 한국어가 자연스러운가

| 샘플 | Before (사실/완결/간결/가독) 평균 | After 평균 | 차이 |
|---|---|---|---|
| 1 (인증 모듈) | 3 / 4 / 2 / 5 → 3.50 | 5 / 5 / 5 / 5 → 5.00 | +1.50 |
| 2 (배포 체크) | 4 / 4 / 4 / 5 → 4.25 | 4 / 4 / 5 / 5 → 4.50 | +0.25 |
| 3 (Kafka) | 5 / 4 / 4 / 5 → 4.50 | 4 / 4 / 5 / 4 → 4.25 | -0.25 |
| 4 (로깅 설계) | 3 / 3 / 3 / 5 → 3.50 | 4 / 4 / 4 / 5 → 4.25 | +0.75 |
| 5 (API 라우팅) | 4 / 3 / 3 / 5 → 3.75 | 5 / 4 / 5 / 5 → 4.75 | +1.00 |
| 6 (DB 마이그레이션) | 3 / 4 / 3 / 5 → 3.75 | 5 / 5 / 5 / 5 → 5.00 | +1.25 |
| 7 (캐시 전략) | 4 / 4 / 3 / 5 → 4.00 | 4 / 4 / 5 / 5 → 4.50 | +0.50 |
| 8 (모니터링) | 3 / 3 / 3 / 5 → 3.50 | 4 / 4 / 4 / 5 → 4.25 | +0.75 |
| 9 (배치 스케줄러) | 3 / 4 / 3 / 5 → 3.75 | 5 / 4 / 5 / 5 → 4.75 | +1.00 |
| 10 (장애 회복) | 4 / 4 / 4 / 5 → 4.25 | 5 / 5 / 5 / 5 → 5.00 | +0.75 |
| **평균** | **3.88** | **4.63** | **+0.75** |

10건 평균 3.88 → 4.63, **0.75점 상승**. 특히 **간결성(3.2 → 4.8)**이 두드러졌다. Base의 "견고한 아키텍처", "포괄적인 설계" 같은 **공허한 수식어** 습관이 줄었다. Instruct 모델의 상품화된 "도움 주는 어시스턴트 말투"를 우리 도메인의 "담담한 요약" 톤으로 밀어 놓은 효과다. 3번 샘플처럼 **살짝 나빠진 경우**도 정직하게 기록하자. 숨기면 다음 프로젝트에서 같은 함정을 또 밟는다.

한 가지만 기억하자. **"파인튜닝의 성공"은 한 숫자로 말하기 어렵다.** 어떤 축은 많이, 어떤 샘플은 거꾸로 간다. 이 불균일함을 받아들이고 **iteration 단위로 개선하는** 게 현업 감각이다. "데이터 → 학습 → 평가 → 데이터"의 루프를 몇 바퀴 돈다.

---

## 6.9 GPU 없는 독자 — Colab, Kaggle, AutoTrain

여기까지 읽으면서 "나는 GPU가 없는데 이 장이 나와 상관있는 장인가" 싶었다면, 이 절이 바로 당신의 절이다. 커뮤니티에서도 비슷한 탄식이 지속적으로 올라온다.

> "I thought I needed a GPU for local LLMs until I tried this lean model." [커뮤니티:r/LocalLLaMA]

결론부터 말하면 **완주할 수 있다.** 세 가지 무료·저비용 경로가 있다.

### 경로 1 — Colab 무료 T4 + Unsloth (가장 빠른 첫 완주)

Google Colab의 무료 티어는 T4 GPU 16GB를 3시간 제한으로 준다. 시간이 좀 빠듯하지만, **Unsloth** 라이브러리를 쓰면 학습 속도가 2~5배 빨라져서 Llama 3 8B QLoRA를 한 번 완주할 수 있다.

```python
# Colab 셀 한두 개로 설치
!pip install unsloth
!pip install --upgrade --force-reinstall --no-cache-dir \
    "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
```

Unsloth의 API는 우리가 본 `transformers`+`peft` 조합보다 단순하다. 커스텀 CUDA 커널로 attention·LoRA 연산을 최적화했다. 품질은 거의 같고 VRAM은 30% 정도 덜 먹는다. Colab처럼 턱에 찬 환경에서는 결정적이다. 지원 모델이 Llama·Mistral·Gemma·Qwen 계열로 제한적이고 업데이트가 빨라 예제 코드가 자주 바뀌니, 공식 Colab 노트북 링크를 그대로 쓰는 편이 안전하다.

체크리스트:

- [ ] Colab 런타임에서 **GPU → T4** 선택
- [ ] 데이터는 Google Drive에 올려 마운트
- [ ] 학습 데이터를 500~1000건으로 줄여 시작 (2000건은 3시간 한도 아슬아슬)
- [ ] epoch는 2로, max_seq_length는 512로 조정
- [ ] 학습 중간 저장 `save_steps=50`으로 짧게 (런타임 끊겨도 재개 가능)

### 경로 2 — Kaggle 2×T4 (무료의 정점)

Kaggle Notebook은 **GPU T4 × 2** 조합을 무료로 준다. 메모리 32GB(16GB × 2)를 합쳐 쓸 수 있어서 batch_size·seq_len을 훨씬 여유 있게 잡을 수 있다. 세션 시간도 9시간으로 넉넉하다. 단점은 설정이 Colab보다 조금 불편하고, 인터넷 접근이 제한될 수 있어서 HuggingFace Hub 로그인을 미리 secrets에 박아야 한다는 점.

다중 GPU를 쓰려면 `accelerate config`로 분산 설정을 한 번 만들어 주고, `SFTConfig`에서 `ddp_find_unused_parameters=False`만 추가해 주면 된다. Kaggle의 공식 QLoRA 템플릿 노트북이 있으니 복붙해서 시작하자.

### 경로 3 — HuggingFace AutoTrain (코드 없이)

코드를 한 줄도 안 쓰고 파인튜닝을 돌리고 싶다면 HuggingFace의 **AutoTrain Spaces**가 선택지다. GUI에 데이터셋을 업로드하고 모델과 하이퍼파라미터를 드롭다운으로 고르면 백엔드에서 학습이 돈다. GPU는 HF가 제공하는 유료 티어(시간당 몇 달러) 또는 무료 Tier(매우 제한적)를 쓴다.

장점은 진입 장벽이 낮다는 것. 단점은 **커스터마이징이 어렵다**는 것. 학습이 실패하거나 품질이 기대와 다를 때 "왜 그런지"를 추적하기가 힘들다. 이 책의 관점에서는 "처음에 한 번 맛보기"로는 괜찮지만, 두 번째 iteration부터는 경로 1 또는 2로 넘어가는 편이 낫다. 무엇이 안에서 도는지 보이지 않으면, 같은 실수를 반복하기 때문이다.

### 한 줄로 고르는 방법

| 상황 | 추천 경로 |
|---|---|
| 처음이고 빠르게 한 번 돌려 보고 싶다 | Colab + Unsloth |
| 넉넉한 환경에서 2~3회 iteration을 돌리고 싶다 | Kaggle 2×T4 |
| 코드를 전혀 쓰고 싶지 않다 | HF AutoTrain (일회성으로만) |
| 프로덕션급 어댑터를 뽑아야 한다 | 유료 GPU 임대 (RunPod, Lambda Labs, vast.ai) |

유료 임대는 시간당 $0.3~1 수준이라 학습 몇 번 값이 두 자릿수 달러 안쪽이다. "GPU가 없다"는 2026년에 더는 핑계가 되지 못한다.

---

## 6.10 iOS vs Android — 오픈 모델이 이 장의 주인공인 이유

5장에서 잠깐 짚었지만 이 장의 맥락에서 한 번 더 이야기할 가치가 있다. 2020년대 LLM 생태계는 두 진영으로 갈렸다.

**iOS형**은 OpenAI GPT-4, Anthropic Claude, Google Gemini다. 모델 가중치는 공개하지 않고 API만 제공한다. 장점은 품질이 가장 높고 운영 부담이 없다는 것. 단점은 가중치를 만질 수 없다는 것. 톤을 바꾸고 싶어도 프롬프트 엔지니어링에서 멈춘다. 데이터가 민감해서 외부로 보낼 수 없다면 아예 선택지에서 빠진다.

**Android형**은 Meta Llama 3, Alibaba Qwen, Google Gemma, Mistral 같은 **오픈 가중치(open weights)** 모델들이다. 가중치가 공개되어 있고, 상용 이용도 허용(라이선스별로 조건은 다르다)된다. 품질은 iOS의 바로 뒤를 쫓는다. 장점은 분명하다. 로컬에서 돌릴 수 있고, 파인튜닝할 수 있고, 배포 방식을 내가 고른다. 단점은 운영 부담이 전부 내 몫이라는 것.

그리고 이 두 진영 사이에는 **본질적인 차이** 하나가 있다.

> **iOS형은 프롬프트까지만 건드린다. Android형은 가중치까지 건드린다.**

6장이 이 책에서 특별한 위치에 있는 이유가 이 한 줄이다. **자기 모델 가중치를 손에 쥐고 조금 고친다.** 이게 이 장에서만 가능한 감각이다. 4장에서 from scratch로 모델을 만들 때도 가중치를 만졌지만, 규모가 귀여웠다. 7장에서 API를 부를 때는 상용 모델의 가중치를 건드릴 수 없다. **오픈 모델 + QLoRA**의 조합만이, 8B짜리 거인의 가중치 위에 내 도메인의 얇은 층을 올리는 감각을 준다. iOS 진영이 제공하지 못하는, Android 진영만의 특권이다.

실무로 번역하면 이렇다. 민감 데이터 사내 프로젝트, 오프라인 엣지 배포, API 비용이 장기 부담인 대규모 서비스, 회사 고유의 톤·스키마를 모델에 박아야 하는 경우—이런 상황에서 **6장의 기법이 선택지로 올라온다.** 그렇지 않다면 7장(API)이나 8장(RAG)이 더 실무적이다. 9장에서 네 해법을 비교하는 플로차트를 그릴 때, 6장이 "가중치 레벨까지 내려가야 할 이유가 명확한 경우"의 분기로 자리잡는다.

그리고 **오픈 모델은 사라지지 않는다.** API 제공자가 "이 모델은 deprecated입니다"라며 내리는 건 클라우드 시대의 새로운 위험이다. 오픈 가중치 모델은 한 번 받아 두면 내 디스크에서 영원히 돈다. **재현성과 장기 운영**의 보험이고, API 사용료가 싸져도 쉽게 대체되지 않는 가치다.

---

## 6.11 4장에서 본 그 어텐션이 여기서도 돈다

이 장을 닫기 전에 한 가지 감각을 짚고 가자. 우리가 방금 건드린 Llama 3 8B 내부에서 돌고 있는 계산은, 3장에서 그림으로 본 것과 4장에서 손으로 쌓은 것과 **동일한 구조**다.

`target_modules`에 써 넣은 `q_proj`, `k_proj`, `v_proj`, `o_proj`. 3장 회의실 비유에서 Q는 "내가 던지는 질문", K는 "답 후보의 간판", V는 "실제 내용", `o_proj`는 여러 헤드 출력을 합친 뒤의 출력 프로젝션이다. 4장에서 `nn.Linear(d_model, d_model)` 네 개로 직접 쌓은 바로 그 레이어들이다. Llama 3 8B는 이 네 레이어가 32개 블록 × 32개 헤드로 병렬 동작한다. **구조는 똑같다. 숫자만 크다.**

`gate_proj`, `up_proj`, `down_proj`는 FFN의 SwiGLU. 4장의 `Linear → GeLU → Linear` 두 층짜리를 세 층으로 확장한 변형일 뿐이다. **같은 계열의 아이디어**다.

QLoRA로 이 일곱 행렬에 어댑터를 얹는 건, **4장에서 쌓은 블록에 어댑터를 얹는 것과 본질적으로 같은 일**이다. 규모만 다르다. **손으로 쌓은 감각이 그대로 스케일 업 된다**는 것이 이 두 장이 연결되는 지점이다.

이 연결을 잡으면 파인튜닝이 "어텐션 블록의 Q·K·V 행렬에 저랭크 덧셈을 더했더니 모델의 습관이 바뀌었다"로 읽힌다. 엔지니어링적으로 단단한 이해다. 6장에서 얻어야 할 가장 큰 감각이 이거다.

---

## 6.12 HF Hub에 올려 두자 — 어댑터가 한 사람의 서명이 되는 순간

마지막으로 한 가지만 더. 파인튜닝이 끝났으면 **그 결과를 HuggingFace Hub에 올려 두자.** 실무 경력 문서에 "파인튜닝 경험 있음"이라 쓰는 것보다, `huggingface.co/yourname/llama3-8b-doc-summary-lora` 한 줄을 보여 주는 편이 훨씬 강력하다.

업로드는 한 줄이다.

```python
from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="./llama3-8b-doc-summary-lora",
    repo_id="yourname/llama3-8b-doc-summary-lora",
    repo_type="model",
)
```

저장소에 `README.md`(모델 카드)도 같이 넣자. (a) Base 모델, (b) 학습 데이터, (c) 평가 숫자, (d) 의도된 용도와 한계—네 가지면 6개월 뒤 내가 다시 봐도, 남이 봐도 재현할 수 있다. HuggingFace 기본 템플릿 빈칸만 채우면 된다.

공개해 두면 **커뮤니티의 시선이 닿는다.** 같은 태스크를 하던 다른 개발자가 "이 어댑터를 내 데이터에도 얹어 봤는데 잘 되더라" 하는 피드백을 주기도 한다. unfinishedgod의 Llama 3 한국어 파인튜닝 [웹:unfinishedgod]도, SK DevOcean의 Gemma 한국어 요약 LoRA [웹:SK-DevOcean]도 그렇게 공개된 참고점이다. 우리 어댑터도 같은 계보의 한 칸을 차지한다. 회사에서 공개하기 어려우면 **private 저장소**라도 충분하다. 중요한 건 "내 노트북 안에만 자고 있는 파일"이 "같은 Base 위에 올려 돌릴 수 있는 공통 산출물"이 되는 감각이다.

---

## 마무리

이 장에서 우리는 거인의 어깨 위에 얇은 층 하나를 얹는 감각을 손으로 쥐었다. "간단한 파인튜닝 한번 해 주세요"를 받았을 때 이제 무엇부터 물어야 할지가 손끝에 있다—데이터 몇 건, GPU 뭐, 톤·길이, Base 모델 뭐, 평가 기준. 이 다섯 질문이 프로젝트의 절반을 설계한다. 공통 태스크의 두 번째 답도 손에 쥐었다. 4장의 from-scratch 요약과, 오픈 모델 위에 얹은 오늘의 요약이 나란히 있다. 다음 7장에서 같은 태스크를 API 한 줄로 풀 때, 이 숫자가 비교의 기준점이 된다.

한 가지만 정직하게 덧붙이자. **파인튜닝은 은총알이 아니다.** 샘플의 40~50%는 before/after가 거의 같고 일부는 오히려 나빠진다. 그래서 실무의 1원칙은 여전히 **"첫 직감이 fine-tune이면 red flag"**다. 프롬프트 엔지니어링(7장)과 RAG(8장)를 먼저 해 보고, 톤·구조·도메인 어휘의 미세 조정이 꼭 필요할 때 파인튜닝이 들어온다.

7장에서는 **"만드는 관점"에서 "쓰는 관점"으로 회전**한다. 우리가 방금 만든 어댑터를 포함해 기존 상용 모델까지 전부 "API로 호출되는 함수"로 다루기 시작한다. 방금 `SFTConfig`에 적어 넣은 `temperature=0.3`이 API 파라미터에서 어떻게 같은 손잡이로 나오는지 같이 확인한다. 그리고 Java 개발자라면 기다렸을 Spring AI와 LangChain4j가 거기서 무대에 오른다. 같이 넘어가 보자.
