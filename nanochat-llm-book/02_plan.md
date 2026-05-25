# 책 저술 계획 (v2 — 리뷰 반영)

> 이 계획은 `01_reference.md`(Phase 1 리서치 종합)와 `nanochat/` 코드 트리, `toby-book-writing-style.md`, 그리고 `03_review_log.md`의 리뷰 피드백을 통합한 두 번째 판본이다. 모든 코드 인용의 라인 번호는 *이번 라운드에서 직접 재검증*했다 — `gpt.py`는 512줄, `tokenizer.py`는 406줄, `optim.py`는 535줄, `engine.py`는 357줄 등.

## 라운드 2의 핵심 변경 요약

1. **4장이 두 챕터(4A·4B)로 쪼개졌다.** 5.5만 자 한 챕터의 *완성 위험*과 *독자 포기 위험*을 모두 줄이기 위해. 그 결과 전체 챕터 수는 **10 → 12장**.
2. **RL이 9장(독립 챕터)으로 승격됐다.** 8장은 *순수한 SFT*만 다루고 RL은 별도 호흡으로. 후반부 곡선이 *6→7→8→9→10*의 더 풍성한 진폭을 갖는다.
3. **7장 평가가 2.5만 자로 짧아져 골짜기가 더 깊어졌다.** 골짜기는 *짧고 깊을수록* 다음 봉우리가 높아진다.
4. **모든 `gpt.py` 라인 인용에서 "481줄"이 사라졌다.** 정확한 라인 범위로 교체. 다른 파일의 라인 번호도 모두 재검증.
5. **8장 SFT 실습의 결과 약속이 솔직하게 낮춰졌다.** README 원문("kindergartener level")을 본문에 *기대치 조정 박스*로 노출.
6. **2장에 "같은 한국어 문장의 세 토크나이저 비교 표"가 들어갔다.** 한국어 독자의 *aha*가 책 초반에 일어난다.
7. **10장 calculator 데모가 *speedrun d24 체크포인트 다운로드*를 권장 경로로 명시.** d6 1500-step 모델로는 tool use가 안정적이지 않다는 *기술적 사실*을 박스로.
8. **부록 B가 B-1(에러 메시지 읽는 법) + B-2(트러블슈팅 시나리오)로 분리.** 부록 A의 디렉토리 맵은 *책 앞 면지 한 페이지 + 부록 A 4천 자*로 쪼갰다.
9. **전체 분량 목표를 약 33~36만 자(본문)로 *현실화*.** 한국어 IT 서적의 상위권을 벗어나지 않는 선.

라운드 1에서 *유지한* 결정과 리뷰가 *무시 가능*하다고 명시한 권고는 §8(라운드 1에서 옮긴 추천)와 §9(반영하지 않은 권고)에 사유와 함께 정리.

---

## 1. 책 제목 후보 (3개)

리뷰 §I.1의 "검색 약하다"는 권고는 *반영하지 않는다* (사유는 §9-1). 다만 *부제는 강화*했다.

### 후보 A (추천) — **나노챗 해부학**
- **부제 (강화 버전):** **한 GPU 노드 3시간으로 ChatGPT를 만든다 — 카르파시 nanochat 8천 줄 코드 해부**
- **슬러그:** `nanochat-anatomy`
- **Logline:** ChatGPT를 만든다는 게 정확히 어떤 코드를 짠다는 뜻인지, 카르파시의 nanochat을 한 줄씩 따라 읽으며 손에 쥐어보는 책.
- **강조하는 정체성:** "해부학"이라는 단어가 책의 실제 활동(코드를 펴고 한 줄씩 들여다보기)을 정확히 묘사한다. 부제에 *결과 약속*("3시간으로 ChatGPT") + *분량 약속*("8천 줄") + *원작자 이름*("카르파시")이 모두 들어가 마케팅과 정체성을 양립시킨다.

### 후보 B — **밑바닥부터 만드는 ChatGPT**
- **부제:** nanochat 코드로 따라가는 토크나이저, 사전학습, SFT, RL, 그리고 추론
- **슬러그:** `chatgpt-from-scratch`
- **Logline:** 토크나이저부터 챗 UI까지, "내가 만든 모델과 대화"라는 한 문장을 위해 8천 줄의 코드와 8XH100 한 노드가 어떻게 협력하는지 처음부터 끝까지.
- **강조하는 정체성:** 한국어 IT 베스트셀러 클리셰의 의식적 차용. 검색에 강하다.

### 후보 C — **GPT-2를 100달러에 재현하기**
- **부제:** nanochat으로 읽는 현대 LLM 학습 파이프라인
- **슬러그:** `gpt2-for-100-dollars`
- **Logline:** "$100 ChatGPT"라는 카르파시의 도발적 슬로건이 진짜로 가능한지, 코드와 GPU 시간과 평가 지표를 모두 따져가며 검증한다.
- **강조하는 정체성:** 가장 도발적이고 입소문에 강하지만 *결과 약속이 좁아* 8~10장의 정렬·자기 챗봇 챕터를 가린다.

### 추천: **후보 A — 「나노챗 해부학」 (강화 부제 포함)**

리뷰 §I의 비판(*"마케팅적으로 전문가용"*)은 정당하지만, 책의 *진짜 차별점*은 "8천 줄 한 작품을 끝까지 따라간다"이고 "해부학"이 그 정체성에 가장 가까운 메타포다. 검색 노출은 부제로 보완한다 — *"한 GPU 노드 3시간으로 ChatGPT를 만든다"*가 그 일을 한다.

### 슬러그 운영 규칙 (리뷰 §I.3 반영)

| 위치 | 슬러그 | 사용처 |
|---|---|---|
| 작업 디렉토리 | `nanochat-llm-book` | 리서치·계획·챕터 초안 (Phase 1~3) |
| 책 매니페스트 `slug` | `nanochat-anatomy` | `book_manifest.json` 확정 시점부터 |
| EPUB 파일명 | `나노챗-해부학-v{version}.epub` | 빌드 산출물 |
| 책 소개 markdown | `나노챗-해부학-v{version}.md` | 빌드 산출물 |

작업용 슬러그(`nanochat-llm-book`)와 산출용 슬러그(`nanochat-anatomy`)의 분리는 *Phase 5(편집·확정)에서 일괄 전환*한다.

---

## 2. 책 특성

### 장르
**기술서 70% + 실습서 25% + 회고형 에세이 5%**의 혼합. 각 챕터마다 *실습 박스*, 챕터 첫·끝 문단의 *수사적 질문*. 4A·5장은 *밀도 높은 기술서*, 10장은 *동적인 실습서*, 12장은 *회고 에세이*에 더 가깝다.

### 분량
- **페이지 수:** 약 320~360페이지 (12장 + 서문·에필로그·부록).
- **글자 수:** 본문 약 **33~36만 자** + 서문·에필로그·부록 약 5만 자 = 총 **약 38만 자** (한국어 원고지 약 1,900매).
- **챕터별 분포는 균등하지 않다.** 가장 긴 챕터(4A 골격, 6 사전학습)는 3만~3.5만 자, 가벼운 챕터(9 RL, 11 report)는 2만 자대.

### 난이도
**중급.** 전제·가르치는 것은 라운드 1과 동일.

### 독자 여정

| 시작 시점 (1장 펴기 전) | 끝났을 때 (12장 덮은 뒤) |
|---|---|
| "ChatGPT가 어떻게 굴러가는지 궁금하다." | "내 GPU에서 나만의 작은 ChatGPT를 학습시켜 봤다." |
| "토크나이저·트랜스포머·SFT·RL이라는 단어를 들어봤지만 흐릿하다." | "각 단계가 무엇을 *가르치는지*, 무엇으로 *검증하는지* 한 문장으로 설명할 수 있다." |
| "PyTorch는 쓰지만 LLM 학습 코드는 못 짠다." | "GPT nn.Module을 직접 읽고 수정해서 다시 학습 돌릴 수 있다." |
| "Muon? 그게 뭐지?" | "왜 임베딩에는 AdamW를, matrix에는 Muon을 쓰는지 동료에게 설명해줄 수 있다." |
| "한 번 직접 굴려보고 싶긴 한데, 어디부터 손대야 할지 모르겠다." | "speedrun.sh를 처음부터 끝까지 분석해서 자신만의 미니 파이프라인을 작성했다." |
| "ChatGPT는 마법 같은 블랙박스다." | "마법은 아니다. 8천 줄의 코드와 수십 편의 논문이 얽혀 있는 정교한 작품이다." |

### 차별점

라운드 1과 동일하되 한 가지를 추가한다:

7. **한국어 독자의 *aha*가 책 초반에 일어난다.** 2장의 한국어 토크나이저 비교 표가 그 일을 한다. 12장 마지막 절과 부록 D가 그 *aha*를 *행동*("내 한국어 데이터로 토크나이저를 다시 학습시켜본다")으로 연결한다.

---

## 3. 챕터 구성

총 **12장 + 서문 + 에필로그 + 부록 4개**.

내러티브 곡선의 큰 그림: 오리엔테이션(1장) → 토크나이저 직관(2장) + 학습(3장) → **GPT 골격(4A) + modded 트릭(4B)** → 옵티마이저(5장) → **사전학습 클라이맥스(6장)** → 평가의 골짜기(7장) → SFT(8장) → **RL(9장)** → **추론·챗봇 클라이맥스(10장)** → report로 도장 찍기(11장) → 회고와 한국어로 가는 길(12장).

각 챕터에 **정서적 톤** 한 줄 표기.

---

### 1장. 왜 우리는 ChatGPT를 직접 만들려 하는가
- **핵심 질문:** "GPT-2를 100달러에 재현한다"는 카르파시의 도발이 정확히 무엇을 약속하고, 우리가 그 안에서 무엇을 손에 쥘 수 있는가?
- **주요 내용:**
  1. nanochat 공개의 맥락 — [Discussion #1](https://github.com/karpathy/nanochat/discussions/1)의 "the best ChatGPT that $100 can buy".
  2. nanoGPT → modded-nanoGPT → nanochat 가계도.
  3. 책의 약속과 그 한계.
  4. 사전 지식 점검표.
  5. 환경 구축: `uv sync --extra cpu` (또는 `--extra gpu`), `NANOCHAT_BASE_DIR` 설정, GPU/CPU/MPS 분기.
  6. 작품의 *층위* — `nanochat/`(라이브러리) vs `scripts/`(CLI) vs `tasks/`(데이터) vs `runs/`(쉘).
  7. **(추가)** `nanochat.dataset` 한 문단 — "셰드 한 개가 약 100MB, 다운로드는 ~30초, `-n 2`면 약 1분"이라는 *측정값* (리뷰 §A.4 반영).
  8. **(추가)** 5줄짜리 *맛보기 인터랙션* — `python -m scripts.tok_eval` 출력 한 줄을 미리 보여줘 2장의 *aha* 사다리 만들기 (리뷰 §B.3 반영).
  9. 책의 코드 인용 규칙 — 5줄 이하는 본문, 5~20줄은 박스, 20줄 초과는 *코드 펴기 신호*(파일 경로 한 줄)로 (리뷰 §F.1 반영).
  10. 두 가지 읽기 방식: 풀 GPU 노드 vs 노트북 정성 검증.
- **코드 인용:** `README.md`, `runs/speedrun.sh`(서두 30줄), `runs/runcpu.sh`(서두), `pyproject.toml`(extras), `nanochat/dataset.py`(다운로드 함수 한 단락).
- **실습 [CPU/GPU 공통, 10분]:** `uv sync --extra cpu` → `python -m nanochat.dataset -n 2` → 셰드 두 개와 다운로드 시간 측정. 그리고 한 줄 인터랙션으로 special token 출력.
- **예상 분량:** **3만 자** (라운드 1의 2만 자에서 증가, 리뷰 §B.3 반영).
- **의존성:** 없음.
- **정서적 톤:** 호기심·기대. "함께 코드를 펴자"는 청유형이 가장 짙다.

---

### 2장. 토크나이저는 모델이 세상을 보는 단위다
- **핵심 질문:** 왜 우리는 글자가 아니라 *byte pair*를 본단 말인가? 그리고 *한국어*는 왜 모든 토크나이저에서 비싸진단 말인가?
- **주요 내용:**
  1. BPE의 직관 — `"strawberry"`가 어떻게 토큰으로 쪼개지는가, 왜 `count('r')`이 어려워지는가.
  2. GPT-4 정규식 `SPLIT_PATTERN`과 그 변형 (`\p{N}{1,3}` → `\p{N}{1,2}`)이 왜 작은 vocab에서 중요한가.
  3. 9개의 `SPECIAL_TOKENS`가 *왜 토크나이저 단에 박혀 있는지* — 도구 사용을 나중에 추가하기 어렵게 만드는 결정의 무게.
  4. 두 구현(`RustBPETokenizer` vs `HuggingFaceTokenizer`).
  5. `token_bytes.pt`의 정체와 bits-per-byte의 사전 준비.
  6. `render_conversation`의 mask=1/0 — 어시스턴트가 학습받는 토큰의 경계.
  7. **(추가·필수) "같은 한국어 문장의 세 토크나이저 비교 표"** (리뷰 §E.2 반영):

      예시 문장: **"안녕하세요, 저는 토비입니다."**

      | 토크나이저 | vocab | 토큰 수 | 대표 분할 (앞 5개) | bytes/token |
      |---|---|---|---|---|
      | GPT-2 (50K) | 50,257 | ~18 | `ìķ`, `Ī`, `ëħķ`, `íķĺ`, `ìĦ¸` | 약 2.0 |
      | GPT-4 cl100k_base (100K) | 100,277 | ~8 | `안`, `녕`, `하세요`, `,`, ` 저` | 약 4.5 |
      | nanochat 32K (FineWeb로 학습) | 32,768 | ~22 | byte-level fallback에 가까움 | 약 1.7 |

      (수치는 책 본문 작성 시 직접 측정해 *정확*히 박는다 — 위는 *방향성을 보여주는 예시*).

      *이 표가 한국어 독자의 첫 aha다 — "내 모국어가 어떻게 보이는지"가 토큰 수의 차이로 즉시 보인다.*
- **코드 인용 (라인 재검증 완료):** `nanochat/tokenizer.py:13-25` (특수토큰 9개), `:30` (SPLIT_PATTERN), `:163-263` (RustBPETokenizer 클래스 골격), `:266-365` (render_conversation), `:367-388` (render_for_completion).
- **실습 [CPU 30분]:** `tiktoken`으로 GPT-2/GPT-4 토크나이저 로드 + nanochat 32K로 같은 문장(영문/한글/코드) 토큰화 → 비교 표 재현.
- **예상 분량:** 3.5만 자.
- **의존성:** 1장.
- **정서적 톤:** 시각적 충격 + *aha*. 한국어 비교 표가 그 *aha*를 일으킨다.

---

### 3장. 토크나이저를 학습시키고 평가하기
- **핵심 질문:** 우리의 32K 토크나이저는 GPT-2(50K)·GPT-4(100K)와 비교해 얼마나 효율적인가? 그리고 그 차이가 모델 학습에 *얼마나* 영향을 주는가?
- **주요 내용:**
  1. `scripts/tok_train.py` 전체 — 2B chars의 FineWeb을 어떻게 흘려보내는가.
  2. `scripts/tok_eval.py`로 영문 뉴스·한국어·코드·LaTeX·과학 텍스트의 compression ratio 측정.
  3. 한국어가 *왜* 모든 토크나이저에서 ratio가 낮은가 — 학습 데이터 분포의 직접적 결과 (2장의 *aha*를 *데이터*로 확장).
  4. `token_bytes.pt` 사전계산 — bpb 평가의 기반.
  5. vocab_size 트레이드오프 — `lm_head` 메모리·CE loss·compression의 균형.
  6. "능력을 토크나이저로 가르치진 못한다 — 도구 호출 토큰만 박을 수 있을 뿐" 회고.
- **코드 인용:** `scripts/tok_train.py` 전체 (rust 학습 + tiktoken export), `scripts/tok_eval.py` (ratio 측정 루프).
- **실습 [CPU 1시간]:** `python -m nanochat.dataset -n 8` → `python -m scripts.tok_train --max-chars=2000000000` → `python -m scripts.tok_eval` → 결과 표를 책의 표와 비교.
- **예상 분량:** 2.5만 자.
- **의존성:** 2장.
- **정서적 톤:** 손에 잡히는 결과의 만족.

---

### 4A장. GPT 모듈의 골격 — embed/forward/init/FLOPs
- **핵심 질문:** 카르파시가 한 파일에 담아둔 GPT 모듈의 *기본 골격*은 무엇인가? Vaswani 2017의 원형 트랜스포머와 비교해 *기본 결정들*은 어떻게 갱신되었는가?
- **주요 내용:**
  1. `GPTConfig` 한 줄 읽기 — `n_layer`, `n_head`, `n_kv_head`, `window_pattern`이 모델의 *모양*을 어떻게 결정하는가.
  2. forward 한 페이지짜리 의사코드 — embed → smear → blocks → backout → norm → lm_head → softcap. (4A는 *큰 그림*만, 세부 트릭은 4B에서.)
  3. **RoPE 깊이 있게:** Su et al. 2021의 직관, `base=100000`을 쓴 이유, `_precompute_rotary_embeddings`의 channel-pair 회전.
  4. **RMSNorm은 왜 learnable γ가 *없는가*** — 작은 모델에서 γ가 1에 머무는 경향, `F.rms_norm(x, (x.size(-1),))` 한 줄로 끝내는 결단.
  5. **QK norm + 1.2× sharpening** — attention 발산 방지의 작은 트릭.
  6. **MLP — ReLU² vs SwiGLU** — Primer 논문의 발견, 작은 모델 친화성, `F.relu(x).square()` 한 줄.
  7. `init_weights` — meta device 초기화·`to_empty`·임베딩 std=0.8·lm_head std=0.001의 한 줄짜리 의미들.
  8. `estimate_flops` — PaLM 식 6N + 12hq, sliding window 보정 (sliding window 자체는 4B에서 자세히).
- **코드 인용 (라인 재검증 완료, `gpt.py`는 *총 512줄*):**
  - `nanochat/gpt.py:29-39` (`GPTConfig`)
  - `nanochat/gpt.py:42-43` (`norm` 함수 — `F.rms_norm` 한 줄)
  - `nanochat/gpt.py:45-50` (`Linear` 커스텀 클래스 — fp32 master + forward 캐스팅)
  - `nanochat/gpt.py:57-63` (`apply_rotary_emb`)
  - `nanochat/gpt.py:65-126` (`CausalSelfAttention` 전체 — RoPE 적용·QK norm·1.2× sharpening·FA3 디스패치)
  - `nanochat/gpt.py:129-140` (`MLP` — ReLU²)
  - `nanochat/gpt.py:142-152` (`Block`)
  - `nanochat/gpt.py:154-200` (`GPT.__init__` 골격)
  - `nanochat/gpt.py:202-266` (`init_weights`)
  - `nanochat/gpt.py:268-283` (`_precompute_rotary_embeddings`)
  - `nanochat/gpt.py:317-343` (`estimate_flops`)
  - `nanochat/gpt.py:416-482` (`forward` — 4A는 *전체 흐름*만, 세부 트릭은 4B)
- **실습 [CPU/MPS 30분, 3단계]** (리뷰 §D.1 반영):
  - (a) d4 모델을 meta device에서 init → 파라미터 수·`estimate_flops` 출력.
  - (b) `window_pattern`을 "SSSL"에서 "L"로 바꿔 attention mask shape 비교 (4B의 sliding window 사전 준비).
  - (c) **`init_weights`의 임베딩 std=0.8을 std=0.1로 바꿔보고 forward output 분포를 히스토그램으로 확인** — *초기화의 영향*을 시각적으로.
- **예상 분량:** **3만 자** (라운드 1의 5.5만 자에서 4A·4B로 양분).
- **의존성:** 2~3장 (토큰 단위 사고).
- **정서적 톤:** 외과의의 집중. 챕터가 *읽힐 수 있는 길이*로 줄었으므로 호흡이 끊기지 않는다.

---

### 4B장. modded-nanoGPT가 더한 7가지 트릭
- **핵심 질문:** 카르파시가 modded-nanoGPT 커뮤니티에서 가져온 *현대화 패치*들은 정확히 무엇이고, 왜 작은 모델에서 의미가 있는가?
- **주요 내용 (7가지 트릭, 각각 한 절씩, 직관 메타포 포함 — 리뷰 §C.1):**
  1. **Value embeddings (ResFormer)** — 절반 layer에만 KV stream에 더해지는 별도 임베딩. 12채널 `ve_gate` × `3 * sigmoid` → (0, 3) 범위 multiplier. *직관 메타포:* "attention의 메모장에 같은 단어를 다시 한 번 적어두는 것".
  2. **Per-layer learnable scalars** — `resid_lambdas`(1.15→1.05), `x0_lambdas`(0.20→0.05). modded-nanoGPT의 발명. *직관:* "각 layer마다 residual 흐름의 음량을 *학습*된 볼륨 노브로 조절한다".
  3. **Smear** — 이전 토큰 임베딩을 현재에 섞는 cheap bigram trick. `smear_gate`(24채널 → 1) + `smear_lambda`. *직관:* "직전 단어를 *살짝 흐릿하게* 현재에 비춰둔다".
  4. **Backout** — 중간(`n_layer//2`) 레이어 residual을 cache했다가 최종 norm 직전에 빼서 low-level feature를 제거. *직관:* "그림을 다 그린 뒤 *초벌 스케치 선*을 지우는 단계".
  5. **Sliding window attention** — `window_pattern="SSSL"` → S(short, 1/4 context=512), S, S, L(full). SDPA fallback에서 *왜* 끔찍한가.
  6. **Untied embedding** — `wte`와 `lm_head`가 별개 weight. 작은 모델에서 weight tying의 가성비.
  7. **Logit softcap = 15 × tanh(logits/15)** (fp32) — Gemma-2 식 안정화. `loss explosion` 방지.
  - 마지막 절: **"여기까지 7개 트릭. 차 한 잔 마시고 5장으로 가자."** (리뷰 §F.1의 호흡 박스 권고 반영 — 한 챕터를 *완주*했다는 감각 만들기.)
- **코드 인용 (라인 재검증 완료):**
  - `nanochat/gpt.py:53-55` (`has_ve` — value embedding 활성 layer 판별)
  - `nanochat/gpt.py:78-100` (`CausalSelfAttention`의 value embedding gate)
  - `nanochat/gpt.py:177-186` (per-layer scalars 선언: `resid_lambdas`, `x0_lambdas`, `smear_gate`, `smear_lambda`, `backout_lambda`)
  - `nanochat/gpt.py:188-200` (`value_embeds` ModuleDict 구성)
  - `nanochat/gpt.py:230-244` (init_weights의 lambda·smear·backout 초기화)
  - `nanochat/gpt.py:285-312` (`_compute_window_sizes` — sliding window 패턴 파싱)
  - `nanochat/gpt.py:432-450` (smear forward — training 경로와 KV cache 경로 분기)
  - `nanochat/gpt.py:452-464` (backout forward — `x_backout` cache → final norm 직전 빼기)
  - `nanochat/gpt.py:466-472` (softcap 적용)
  - `nanochat/flash_attention.py:48-105` (SDPA fallback 경고와 sliding window 비용)
- **실습 [CPU/MPS 20분]:** d4 모델에서 `backout_lambda`를 0으로 강제했을 때 vs 그대로일 때 — forward output 분포 비교. *"backout이 정말 뭔가를 *빼고 있는지*"*를 직접 확인.
- **예상 분량:** **2.5만 자.**
- **의존성:** 4A장.
- **정서적 톤:** *현대화 패치 노트의 정밀함.* 챕터 마지막의 "차 한 잔" 박스가 5장 진입의 *예고된 휴식*이 된다.

---

### 5장. 옵티마이저는 왜 두 개인가 — AdamW와 Muon
- **핵심 질문:** 카르파시는 왜 매트릭스 파라미터에는 Muon을, 임베딩과 스칼라에는 AdamW를 *섞어서* 쓰는가? Muon은 정확히 무엇을 하는가?
- **주요 내용:**
  1. AdamW 30초 복습 — Adam + decoupled weight decay.
  2. Muon의 직관 — "momentum으로 모은 gradient를 *직교화*한다".
  3. Newton-Schulz iteration이 SVD `U·V^T`를 근사한다는 시각적 그림.
  4. **Polar Express** ([2505.16932](https://arxiv.org/abs/2505.16932)) — Newton-Schulz의 quintic 변종, 5회 iteration용 계수.
  5. **NorMuon** ([2510.05491](https://arxiv.org/abs/2510.05491)) — neuron-wise variance reduction.
  6. **Cautious weight decay** — update와 부호 같은 param에만 WD.
  7. 왜 임베딩에 Muon을 쓰면 *안 되는가*.
  8. `setup_optimizer`의 7개 param group — embedding/lm_head/value_embeds/scalars/matrices(shape별).
  9. `dmodel_lr_scale = (model_dim/768)^-0.5`의 의미.
  10. `@torch.compile(dynamic=False, fullgraph=True)` + 0-D CPU tensor argument trick — LR이 step마다 바뀌어도 graph 재컴파일 안 됨.
  11. (선택 박스) `DistMuonAdamW`의 3-phase async — Phase 1 reduce_scatter launch → Phase 2 wait+local update+all_gather launch → Phase 3 wait+copy back. "PyTorch DDP를 안 쓰는 이유."
- **수식 정책 (리뷰 §C.2, 조건부 반영):** *Newton-Schulz의 단 한 줄 점화식*만 본문에 박는다 — `X_{n+1} = a·X_n + b·X_n·X_n^T·X_n + c·(X_n·X_n^T)^2·X_n` 한 줄. 그 한 줄이 quintic coefficient의 *튜닝 대상*을 보여주는 *유일한* 사다리. 다른 모든 곳에서는 코드와 그림으로 풀어준다. *수식 한 줄 양보*는 서문에서 미리 예고한다.
- **코드 인용 (라인 재검증 완료, `optim.py`는 *총 535줄*):**
  - `nanochat/optim.py:22-50` (`adamw_step_fused` — `@torch.compile(dynamic=False, fullgraph=True)`)
  - `nanochat/optim.py:54-89` (Polar Express coefficient + orthogonalization 함수)
  - `nanochat/optim.py:92-148` (`muon_step_fused` — NorMuon + cautious WD)
  - `nanochat/optim.py:154-297` (`MuonAdamW` 단일 GPU 버전)
  - `nanochat/optim.py:299-535` (`DistMuonAdamW` 3-phase async — *박스로 옮긴다*)
  - `nanochat/gpt.py:374-414` (`setup_optimizer` — 7개 param group, `dmodel_lr_scale`)
- **실습 [CPU 15분]:** 작은 (1024×1024) random matrix에 `muon_step_fused`를 5번 돌려서 SVD와 비교. ***시각적 numpy 코드*** — 매 iteration마다 `‖X_n - U·V^T‖`의 거리 곡선을 plot. (수식 양보가 *불필요*한 사다리.)
- **예상 분량:** **3만 자.**
- **의존성:** 4A·4B장.
- **정서적 톤:** 약간의 경외 → 친숙함. 4B의 "차 한 잔" 직후라 호흡이 살아 있다.

---

### 6장. 사전학습, 드디어 loss가 떨어진다
- **핵심 질문:** 우리가 5장까지 준비한 모든 것이 *마침내* 사전학습 루프 안에서 어떻게 협업하는가? 그리고 우리는 wandb 그래프에서 무엇을 보아야 하는가?
- **주요 내용:**
  1. `base_train.py`의 큰 그림 — argparse → DDP setup → meta init → torch.compile → scaling laws → data loader → loop.
  2. **(추가)** `nanochat/common.py`의 `_detect_compute_dtype`·`compute_init`·`get_peak_flops` — *컴퓨트 환경의 단일 진실*. H100/A100/CPU/MPS에서 같은 코드가 다르게 도는 코드적 답 (리뷰 §A.3 반영).
  3. **공식 셋, 한눈에 (박스 처리, 리뷰 §C.4):**
     - Chinchilla 20 → nanochat 12 (default) / speedrun 8 (`--target-param-data-ratio`)
     - Power Lines: `B_opt ∝ D^0.383` ([2505.13738](https://arxiv.org/abs/2505.13738))
     - T_epoch WD scaling: `WD ∝ √(B/B_ref) × (D_ref/D)` ([2405.13698](https://arxiv.org/abs/2405.13698))
     - 본문에서는 *효과가 어떤 그래프로 보이는지*만.
  4. **BOS-aligned bestfit-crop dataloader** — 왜 padding 대신 crop인가, 35% 토큰을 *버리는* 결정의 무게.
  5. LR schedule — linear warmup 40 → constant → warmdown(ratio=0.65)을 final 0.05까지.
  6. Muon momentum schedule — 0.85→0.97 warmup, 0.97→0.90 warmdown.
  7. **FP8 training (자체 미니 구현, 266줄)** — torchao 대비 단순화, E4M3/E5M2 선택, `torch._scaled_mm`.
  8. **FlashAttention 3 디스패처** — SM90+bf16/fp8 only, fallback의 위험.
  9. **GC freeze trick** — 첫 step 후 `gc.collect(); gc.freeze(); gc.disable()`.
  10. **(추가) "체크포인트 한 박스" — `checkpoint_manager.py`** (리뷰 §A.1·A.2 반영):
      - `_patch_missing_keys`의 *옛 체크포인트 호환성* (lambda·smear·backout이 없는 옛 ckpt 자동 패치)
      - optimizer state가 *rank별로* shard로 저장되는 ZeRO-2의 물리적 흔적
      - `find_largest_model`의 `d{N}` 패턴 정렬
      - *재현성에 대한 책*이라는 정체성을 강화.
  11. wandb 그래프 — val_bpb, MFU, tok/sec, VRAM.
  12. 학습이 발산하면 — logit softcap, LR 조정, 데이터 노이즈.
- **코드 인용 (라인 재검증 완료, `base_train.py`는 *총 630줄*):**
  - `scripts/base_train.py:14-16` (`expandable_segments` 환경변수)
  - `scripts/base_train.py:58-68` (argparse — target-param-data-ratio, warmup-steps, warmdown-ratio)
  - `scripts/base_train.py:129-192` (`build_model_meta` → FP8 변환)
  - `scripts/base_train.py:196-240` (`disable_fp8` 컨텍스트 매니저)
  - `scripts/base_train.py:263-316` (`get_scaling_params` + Chinchilla/Power Lines/T_epoch 자동 결정)
  - `scripts/base_train.py:360-386` (`get_lr_multiplier`, `get_muon_momentum`, `get_weight_decay`)
  - `scripts/base_train.py:586-594` (`gc.freeze()` 트릭)
  - `nanochat/common.py:17-31` (`_detect_compute_dtype`)
  - `nanochat/common.py:150-208` (`get_dist_info`, `compute_init`)
  - `nanochat/common.py:227-278` (`get_peak_flops` H100/A100/3090 테이블)
  - `nanochat/dataloader.py:10-23` (기존 dataloader 대비 trade-off 주석)
  - `nanochat/dataloader.py:74-162` (BOS-aligned bestfit-crop)
  - `nanochat/fp8.py:82-122` (`_to_fp8`, `_to_col_major`)
  - `nanochat/fp8.py:125-228` (`_Float8Matmul`, `Float8Linear`)
  - `nanochat/fp8.py:243-266` (`convert_to_float8_training`)
  - `nanochat/flash_attention.py:23-67` (FA3 로드 + `_resolve_use_fa3`)
  - `nanochat/checkpoint_manager.py:23-40` (`_patch_missing_config_keys`, `_patch_missing_keys`)
  - `nanochat/checkpoint_manager.py:42-76` (`save_checkpoint`, `load_checkpoint` — rank shard 패턴)
  - `nanochat/checkpoint_manager.py:118-148` (`find_largest_model`, `find_last_step`)
- **실습 [두 단계]** (리뷰 §D.2 반영 — *현실적 대안 사다리* 추가):
  - **[CPU/MPS 40분]:** d6 모델로 `runcpu.sh`의 base_train 부분 실행. val_bpb가 떨어지는 곡선 확인.
  - **[GPU, 사다리 표]:**
    | 환경 | depth | 시간 | 비용 | 기대 val_bpb |
    |---|---|---|---|---|
    | 8×H100 spot | d24 | 3시간 | ~$48 | 0.745 (GPT-2급) |
    | A100 1장 | d12 | 24시간 | ~$24 | 1.0 근처 (작은 모델) |
    | RTX 4090 1장 | d8 | 12시간 | (로컬) | 1.2 근처 (장난감급) |
    각 줄이 *기대 결과 수치*까지 제시 — 독자가 *자기 환경에서 무엇을 얻는지*를 *결정*할 수 있게.
- **예상 분량:** **3.5만 자.**
- **의존성:** 2~5장.
- **정서적 톤:** **전반부 클라이맥스 — 통합의 돌파.** *"내가 만든 토크나이저, 내가 읽은 GPT 모듈, 내가 이해한 Muon이 *한 그래프 위에서* 협력한다."*

---

### 7장. 우리가 만든 게 정말 GPT-2급인지 어떻게 아는가
- **핵심 질문:** "GPT-2와 동급"이라는 주장은 무엇으로 *측정되는가*? 그 측정법은 왜 그렇게 정의되었고, 어떤 한계를 가지는가?
- **주요 내용 (의도된 골짜기 — 짧고 농밀):**
  1. **bits-per-byte** — 왜 cross-entropy loss로 vocab을 바꾼 모델을 비교하면 안 되는가. 영어 텍스트 1.3 bit/byte와 우리의 0.745의 의미.
  2. **CORE 22-task** — DCLM 논문이 *왜* 22개를 골랐는가. centered accuracy: `(acc - 0.01·random) / (1 - 0.01·random)`.
  3. GPT-2 1.6B의 reference 0.256525.
  4. `core_eval.py`의 task_type 분기 — multiple_choice / schema / language_modeling.
  5. `evaluate_example`의 deterministic seed (1234+idx).
  6. DDP에서 stride 분산 + `all_reduce(SUM)`.
  7. *(짧은 박스)* "CORE squad만 reference 대비 떨어지는 알려진 차이" — Karpathy의 TODO.
  8. **평가에 흔들리지 않는 법** — sample 수, baseline, 체크포인트 시점 점검.
  9. *(다리 박스 — 8장 예고)* "base 모델은 *대화하지 못한다*. 8장에서 *어떻게* 대화 능력을 가르치는지 보자."
- **정서적 톤 (리뷰 §F.2 반영):** *"숫자를 의심하는 차분한 회의 + 영어 용어를 의역하지 않는 정밀함".* CORE·centered·bpb는 영어 표기 그대로 유지 — 평가의 *건조함*이 *정밀함*으로 읽히게.
- **코드 인용 (라인 재검증 완료):**
  - `nanochat/loss_eval.py:9-65` (`evaluate_bpb` 전체 — 65줄짜리 파일 통째로 인용 가능)
  - `nanochat/core_eval.py:17-83` (`render_prompts_mc/schema/lm`)
  - `nanochat/core_eval.py:113-164` (`batch_sequences_*`, `forward_model`)
  - `nanochat/core_eval.py:168-241` (`evaluate_example`)
  - `nanochat/core_eval.py:244-262` (`evaluate_task` — DDP stride + all_reduce)
- **실습 [CPU/MPS 20분 또는 GPU 5분]:** d6 (또는 d24) base 체크포인트에 `base_eval.py`를 돌려 val_bpb·CORE 출력 → 책의 표와 비교.
- **예상 분량:** **2.5만 자** (라운드 1의 3만에서 감소, 리뷰 §G.1 반영).
- **의존성:** 6장.

---

### 8장. 대화하는 모델을 만든다 — SFT
- **핵심 질문:** 사전학습된 base 모델이 *왜* 대화를 못 하는가, 그리고 우리는 *데이터*로 어떻게 대화 능력을 가르치는가?
- **주요 내용 (RL은 9장으로 이동 — 리뷰 §B.4):**
  1. base 모델의 정체 — "The capital of France is" → "Paris" 하는 *문장 완성기*.
  2. 9개 SPECIAL_TOKENS의 부활.
  3. **Midtraining의 운명** — bestfit dataloader로 옮긴 뒤 SFT에 통합됨.
  4. **(필수)** `tasks/customjson.py` 한 단락 (리뷰 §A.2 반영) — 65줄짜리 *진입점*. identity 합성·자기 챗봇·새 능력 추가가 모두 이 한 파일을 통과한다. 친절한 에러 메시지 *"HINT (Oct 21 2025)... If you recently did a git pull..."*를 한 박스로 인용해 카르파시 식 사용자 친화성도 보여준다.
  5. SFT 데이터 믹스 (`chat_sft.py:164-180`):
     - SmolTalk(train) 460K 일반 대화
     - `CustomJSON(filepath=identity_conversations.jsonl)` × 2 epochs
     - MMLU(auxiliary_train) × 3 epochs
     - GSM8K(train) × 4 epochs
     - SimpleSpelling 200K + SpellingBee 80K
  6. `TaskMixture`의 deterministic shuffle.
  7. **손실 마스킹의 철학** — `render_conversation`의 mask=1/0 결정.
  8. **BOS-aligned bestfit-pad** (cropping이 아니라 padding) — 대화를 *토막내면 안 되므로*.
  9. SFT의 LR schedule — init_lr_frac=0.8, warmdown_ratio=0.5, 옵티마이저 state warm-start (Muon momentum).
  10. **ChatCORE** = 6개 task의 centered accuracy 평균.
  11. **반 페이지짜리 다리 박스 (리뷰 §C.3 반영):**
      | 지표 | 대상 | task 수 | baseline | 어디서 |
      |---|---|---|---|---|
      | CORE | base 모델 | 22 | random per task | `base_eval.py` |
      | ChatCORE | chat 모델 | 6 | {0.25, 0.25, 0.25, 0.0, 0.0, 0.0} | `chat_sft.py:363-396` |
      *"같은 *centered* 트릭, 다른 task 모음, 다른 baseline."*
  12. **능력은 데이터로 가르친다** — Identity injection ([#139](https://github.com/karpathy/nanochat/discussions/139))와 SpellingBee ([#164](https://github.com/karpathy/nanochat/discussions/164))의 두 사례.
  13. *(필수 박스) "기대치 조정"* (리뷰 §D.3, 최우선 반영):

      > **이 챕터의 실습 결과에 대한 정직한 박스**
      >
      > README는 d6+5K pretrain+1500 SFT 모델을 *"kindergartener level. Sometimes the model likes it if you first say Hi before you ask it questions"*라고 표현한다. 우리의 CPU 실습도 *그 정도*다.
      >
      > "What is the capital of France?"에 대해:
      > - 운이 좋으면 "Paris"라고 한 단어 답이 나온다.
      > - 더 흔하게는 "The capital of France is Paris, which is a city ..." 같은 *완성형 문장*이 나오거나, 살짝 엇나간다.
      > - 가끔은 *전혀 엉뚱한 답*이 나온다. *그게 정상이다.*
      >
      > 진짜 한 줄 답을 보고 싶다면 두 가지 옵션:
      > 1. **d12로 8K step SFT** — A100 1장 6시간 옵션.
      > 2. **카르파시가 공개한 speedrun d24 체크포인트 다운로드** — 10장에서도 쓴다.
- **코드 인용 (라인 재검증 완료, `chat_sft.py`는 *총 519줄*):**
  - `scripts/chat_sft.py:26-33` (imports — TaskMixture/GSM8K/MMLU/SmolTalk/CustomJSON/SpellingBee)
  - `scripts/chat_sft.py:63-78` (argparse — chatcore, mmlu-epochs, gsm8k-epochs)
  - `scripts/chat_sft.py:163-183` (train_dataset 정의 — *반드시 그대로 인용*)
  - `scripts/chat_sft.py:187-305` (`sft_data_generator_bos_bestfit` — bestfit-pad)
  - `scripts/chat_sft.py:314-322` (`get_lr_multiplier`)
  - `scripts/chat_sft.py:324-335` (`get_muon_momentum`)
  - `scripts/chat_sft.py:363-396` (ChatCORE evaluation)
  - `nanochat/tokenizer.py:266-365` (`render_conversation` — mask=1/0)
  - `tasks/customjson.py`(짧은 발췌 — 친절한 에러 메시지 포함)
  - `tasks/gsm8k.py`(`<<expr=result>>` 파싱)
  - `tasks/spellingbee.py`(템플릿과 합성 답안)
- **실습 [CPU/MPS 15분]:** d6 SFT 1500 steps → `chat_cli`로 한국어·영어 두 질문 던지기. 위 박스의 *기대치*를 본문이 *명시*하므로 *결과가 한 줄이 아니어도* 책이 거짓말한 게 아니다.
- **(선택 실습 — 실험적):** OpenRouter 키로 `dev/gen_synthetic_data.py` 실행 → 자기 identity 1000줄 합성 → SFT 재실행 → 모델이 자기 이름을 답하는지 확인.
- **예상 분량:** **3만 자** (라운드 1의 4.5만에서 RL 분리·기대치 박스 추가 후 감소).
- **의존성:** 6장 (base ckpt), 7장 (평가 감각).
- **정서적 톤:** "능력을 *주입하는 법*"에 대한 비밀이 풀리는 만족.

---

### 9장. 강화학습이 더하는 것 — "GRPO" in quotes
- **핵심 질문:** SFT가 *데이터로* 대화 능력을 가르쳤다면, RL은 *추가로* 무엇을 가르치는가? 그리고 카르파시는 왜 "GRPO"를 *따옴표* 친 채 쓰는가?
- **주요 내용:**
  1. RL이 *왜 필요한가* — SFT가 모방을 가르치고, RL은 *결과*를 가르친다.
  2. `chat_rl.py:3-11`의 자조적 docstring 인용 — *"I put GRPO in quotes because we actually end up with something a lot simpler and more similar to just REINFORCE"*.
  3. **무엇을 *안* 하는가:**
     - KL regularization to reference model — *없음*
     - PPO ratio + clip — *없음*
     - z-score advantage — 아니고 그냥 `r - μ`
     - sequence-level normalization — 아니고 token-level (DAPO 스타일)
  4. `engine.generate_batch` — 한 GSM8K 문제에 16개 답안 샘플링.
  5. advantages = rewards - rewards.mean().
  6. token-level loss와 `pg_obj` 계산.
  7. **GSM8K가 *왜* 유일한 RL task인가** — reward signal이 깨끗하고 tool use가 있는 도메인.
  8. pass@k 평가.
  9. *(작은 박스)* "RL이 *비용 대비 효과*를 가지려면" — 작은 모델에서는 데이터 다양화가 RL보다 효율적이라는 카르파시의 입장. speedrun이 RL을 *안* 포함하는 이유.
- **코드 인용 (라인 재검증 완료, `chat_rl.py`는 *총 332줄*):**
  - `scripts/chat_rl.py:3-11` (자조적 docstring — *그대로 인용*)
  - `scripts/chat_rl.py:86-146` (`get_batch` — sampling + advantage)
  - `scripts/chat_rl.py:150-237` (`run_gsm8k_eval` — pass@k)
  - `scripts/chat_rl.py:210-227` (`get_lr_multiplier`)
  - `tasks/gsm8k.py` (reward 함수)
- **실습 [GPU 권장, 1시간]:** speedrun d24 SFT 체크포인트로 GSM8K 100문제 RL fine-tune → pass@1이 어떻게 변하는지 측정. *(CPU는 비현실적 — 박스로 명시.)*
- **예상 분량:** **2만 자.**
- **의존성:** 8장 (SFT ckpt).
- **정서적 톤:** *"추가 봉우리"* — 클라이맥스(10장) 직전의 *마지막 오르막*. 토비 스타일의 "물론 ~다. 하지만 ~"가 자주 등장하는 챕터.

---

### 10장. 추론은 다른 모드의 모델이다 — Engine, KV cache, 도구 호출, 그리고 대화
- **핵심 질문:** 학습 시점과 추론 시점에서 같은 nn.Module이 *어떻게 다르게* 작동하는가? 그리고 우리는 어떻게 *직접 학습한 모델과 대화*하는가?
- **주요 내용:**
  1. prefill vs decode의 두 phase.
  2. **KV cache** — `(n_layers, B, T_max, n_kv_heads, head_dim)` pre-allocated tensor.
  3. `cache_seqlens` (int32, per-batch).
  4. `Engine.generate` 한 페이지 의사코드.
  5. `kv_cache.prefill(other_cache)`로 batch=1 prompt를 num_samples로 *복제*.
  6. **Tool use FSM** — `<|python_start|>` → 토큰 누적 → `<|python_end|>` → `use_calculator(expr)` → `<|output_start|> ... <|output_end|>`를 forced_tokens에 주입.
  7. `use_calculator`의 화이트리스트 safe eval — 5초 timeout, `.count(` 메서드만 허용.
  8. `nanochat/execution.py`의 무거운 sandbox — HumanEval용 RLIMIT_AS 256MB + timeout.
  9. **`chat_cli`** — 가장 단순한 REPL.
  10. **`chat_web` + ui.html** — FastAPI SSE 스트림, `WorkerPool` round-robin, UTF-8 멀티바이트 토큰 안전 처리.
  11. 추론 옵션 — temperature, top_k, sampling seed.
  12. *(필수 박스) "calculator 데모는 어떤 모델로 가능한가"* (리뷰 §D.4 반영):

      > **현실적인 calculator 데모 경로**
      >
      > Tool use FSM은 SFT가 GSM8K 4 epochs를 충분히 학습해야 모델이 스스로 `<|python_start|>`를 sample할 줄 알게 된다. d6+1500 step에서는 *대화 자체*가 안정적이지 않다.
      >
      > 권장 경로:
      > 1. **카르파시 공개 speedrun d24 SFT 체크포인트 다운로드** (URL: 본문에 명시).
      > 2. `python -m scripts.chat_web --source=<다운받은 ckpt 경로>`로 띄운다.
      > 3. 브라우저에서 "9 곱하기 8은?"이라고 묻고 *진짜로* calculator 호출이 스트림에 나오는지 확인한다.
      >
      > d6 1500-step 모델로도 calculator가 *가끔* 호출되지만 신뢰할 수 없다. *이 챕터의 클라이맥스를 진짜로 맛보려면 speedrun ckpt를 받자.*
  13. *(추가 박스) "한국어 질문은 어떻게 되나"* (리뷰 §E.3 반영):

      > 한국어로 물어보면 영어로 답하거나 깨진다. 그게 nanochat의 *학습 데이터 분포*다 — fineweb-edu와 smoltalk 모두 영어 중심. 12장 마지막 절에서 *이걸 어떻게 고치는지* 다룬다.
  14. *클라이맥스 닫음* (리뷰 §F.3 반영): 챕터 마지막 단락은 *수사적 질문이 아닌 한 문장*으로 닫는다 — *"`72라고 답한다.`"*
- **코드 인용 (라인 재검증 완료, `engine.py`는 *총 357줄*, `chat_web.py`는 *총 407줄*):**
  - `nanochat/engine.py:26-44` (`timeout`, `eval_with_timeout`)
  - `nanochat/engine.py:46-79` (`use_calculator`)
  - `nanochat/engine.py:82-140` (`KVCache` — `prefill`, `advance`, `get_pos`)
  - `nanochat/engine.py:141-158` (`sample_next_token`)
  - `nanochat/engine.py:160-167` (`RowState` — `forced_tokens`, `in_python_block`)
  - `nanochat/engine.py:169-357` (`Engine.generate` — prefill + decode + tool FSM)
  - `nanochat/gpt.py:484-512` (`generate` 메서드 — *4A에서 빠진 28줄을 여기서 보강*)
  - `scripts/chat_cli.py` 전체
  - `scripts/chat_web.py:87-141` (`Worker`, `WorkerPool`)
  - `scripts/chat_web.py:143-216` (`ChatRequest`, validation)
  - `scripts/chat_web.py:255-345` (`generate_stream`, `chat_completions` — SSE)
  - `scripts/chat_web.py:285-301` (UTF-8 안전 yield)
  - `nanochat/execution.py`(짧은 발췌 — RLIMIT_AS + timeout)
- **실습 [CPU/MPS 또는 GPU 10분]:** speedrun d24 SFT 체크포인트 다운로드 → `chat_web` 띄우기 → 한국어 인사 + 영어 산수 질문 + GSM8K-식 단어 문제 세 가지 입력 → calculator 호출 토큰이 스트림에 나오는지 확인.
- **예상 분량:** **3만 자.**
- **의존성:** 8~9장.
- **정서적 톤:** **클라이맥스 — 책 전체의 정점.** *"내 모델이 답한다."*

---

### 11장. report.md — 우리의 작품에 도장 찍기
- **핵심 질문:** 우리가 *진짜로* GPT-2급에 도달했다는 증거는 어떻게 한 페이지의 markdown으로 정리되는가?
- **주요 내용 (짧고 농밀, 리뷰 §H.3·H.4 반영):**
  1. `nanochat.report`의 *markdown 자동 보고서* — 헤더 + 각 단계 + Summary 테이블.
  2. *(필수)* `report.md`의 *실제 한 페이지* 통째 인용 — 헤더(GPU·시간·git commit·bloat metrics) + Summary 테이블. *재현성의 증거*가 책에 그대로.
  3. 리포트 안의 각 수치 읽기 — val_bpb, CORE, ChatCORE, MFU, tok/sec, wall-clock.
  4. 리더보드 컨텍스트 — [#481 leaderboard](https://github.com/karpathy/nanochat/discussions/481)의 1.80h / val_bpb 0.71808 / CORE 0.2690 (GPT-2 *능가*).
  5. **"내가 학습한 모델을 공유하는 법"** (리뷰 §H.4 반영) — HF Hub 업로드 명령 한 줄 + `chat_web`을 ngrok으로 외부 노출하는 한 줄. *책 너머의 행동*.
- **코드 인용:**
  - `nanochat/report.py` 전체 (짧은 모듈)
  - `report.md` 실제 한 페이지 (외부 산출물 — 한국어 캡션 포함해 인용)
- **실습 [CPU/MPS 10분]:** `python -m nanochat.report generate` → 자기 `report.md`를 열어 책 안의 페이지와 비교.
- **예상 분량:** **2만 자.**
- **의존성:** 6~10장 (모든 단계의 산출이 모임).
- **정서적 톤:** 정리·증거. *"우리가 진짜로 한 일을 한 페이지로 본다."*

---

### 12장. 8천 줄을 덮으며 — Harness, 자기 챗봇, 그리고 한국어로 가는 길
- **핵심 질문:** 우리가 따라온 이 코드가 사실은 *무엇이었는가*? 그리고 *나만의 한국어 챗봇*을 만들고 싶다면 어디부터 손대야 하는가?
- **주요 내용:**
  1. nanochat 전체를 *harness*로 다시 보기.
  2. `--depth` 한 다이얼로 d4부터 d26까지 — *(추가)* 미니시리즈 표 한 페이지 (리뷰 §H.1):

      | depth | params (M) | tokens | wall-clock (8×H100) | val_bpb | CORE |
      |---|---|---|---|---|---|
      | d4 | ~10 | ~80M | 5분 | 1.8 | 0.05 |
      | d8 | ~50 | ~480M | 30분 | 1.3 | 0.10 |
      | d12 | ~150 | ~1.8B | 1.5h | 1.0 | 0.18 |
      | d24 | ~560 | ~6.7B | 3h | 0.745 | 0.258 |

      (수치는 [#420 miniseries](https://github.com/karpathy/nanochat/discussions/420)와 [#481](https://github.com/karpathy/nanochat/discussions/481)에서 인용·추정. 본문 작성 시 정확한 값으로 갱신.)
  3. **Karpathy의 "autoresearch"** — LLM agent로 hyperparameter sweep 자동화한 시도와 한계.
  4. **자기 챗봇 4단계 레시피:**
     - (a) `knowledge/self_knowledge.md` 작성
     - (b) `gen_synthetic_data.py` 커스터마이즈
     - (c) SFT 재실행
     - (d) `chat_web` 시연
  5. **새 능력 추가 레시피** (SpellingBee 패턴 일반화).
  6. **(추가·강화) "한국어로 가는 길"** (리뷰 §E.1·E.3 반영) — *5천 자 한 절*:
     - AI-Hub·KoCommonCrawl에서 한국어 코퍼스 받는 법.
     - `tok_train.py`의 `--max-chars`와 special token 호환성.
     - 한국어 SmolTalk 대체재 (KoAlpaca, KoVicuna 등).
     - 한국어 평가의 어려움.
     - "그래서 작은 한국어 nanochat을 어떻게 시작하는가" — 짧은 액션 가이드.
  7. nanochat의 한계 — 영어 위주, 12B 토큰의 한계, RL이 GSM8K만, multimodal 없음, agent loop 없음.
  8. 다음 책장.
  9. *닫음 (리뷰 §G.2 반영, *과도하지 않게*):* "처음 질문에 답하는 단락" 직후, 청유형 한 줄로 닫는다 — *"당신의 nanochat을 한 번 만들어 두자."*
- **코드 인용:** `nanochat/report.py`, `runs/miniseries.sh`, `runs/scaling_laws.sh`, `dev/gen_synthetic_data.py`, `tasks/spellingbee.py`.
- **실습 [선택, GPU + OpenRouter 키 필요]:** 자기 identity 1000줄을 합성 → SFT 재실행 → 모델이 "나는 누구다"를 답하는지 확인.
- **예상 분량:** **2.5만 자.**
- **의존성:** 책 전체.
- **정서적 톤:** **정리와 다정한 작별.** 토비 식 청유형의 마지막 한 줄.

---

## 4. 내러티브 아크 (재구성)

### 12장 곡선의 큰 그림

```
난이도 ↑                                          
       │                          ┌── 10장 (대화·도구) ←★ 정점 ──┐
       │                     ┌── 9장 (RL) ──┘                    │
       │              ┌── 8장 (SFT) ──┘                          │
       │       ┌── 6장 (사전학습) ★ ──┐                          │
       │ ┌── 5장 ──┘                  │                          │
       │ │ ┌── 4B ──┘   7장 (골짜기) ─┘                          │
       │ │ │┌── 4A ──┘                                           │
       │ │ ││                                  11장(증거) 12장(회고)
       │ │ │└── 3장 (토크나이저 학습)
       │ │ └── 2장 (토크나이저 직관)
       │ └── 1장 (오리엔테이션)
       │
       └─────────────────────────────────────────────────────► 시간
```

**중요한 명시 (리뷰 §G.3 반영):** *4A·4B는 *오르막*이지 *봉우리*가 아니다. 봉우리는 6장과 10장이다.* 4A·4B 끝의 정서는 "통제감을 얻었다"이고, 6장과 10장 끝은 "성취감을 얻었다"이다. 본문에서도 이 차이를 한 줄로 명시한다.

### 어디서 출발해서 어느 봉우리들을 지나는가

1. **1장 평지 워밍업.** 환경 + 측정값 + 맛보기 인터랙션.
2. **2장 첫 aha** — 한국어 토크나이저 비교 표.
3. **3장 첫 만족** — *내가 학습한 토크나이저*.
4. **4A·4B 두 단계 오르막** — 골격(외과 수술) + 트릭(현대화 패치 노트). 4B 마지막 "차 한 잔" 박스가 *완주 감각*을 만든다.
5. **5장 정밀함의 오르막** — Muon. Newton-Schulz의 *시각화*가 사다리.
6. **6장 전반부 클라이맥스** — 통합의 돌파.
7. **7장 의도된 골짜기** — 짧고 깊은 회의. *영어 용어 그대로*의 정밀함.
8. **8장 오르막** — *데이터로 능력을 가르치는* 만족. *기대치 조정 박스*가 정직함을 지킨다.
9. **9장 마지막 오르막** — RL이 추가로 더하는 것. 클라이맥스 직전의 *추가 봉우리*.
10. **10장 책 전체의 정점** — *내 모델이 답한다*. 마지막 한 줄: *"`72라고 답한다.`"*
11. **11장 증거의 정리** — `report.md`. 정점의 *흥분을 가라앉히는* 차분함.
12. **12장 다정한 작별 + 한국어로 가는 길** — *"당신의 nanochat을 한 번 만들어 두자."*

### 독자의 정서적 곡선

| 챕터 | 정서 |
|---|---|
| 1장 | 호기심·기대 |
| 2장 | **aha (한국어)** |
| 3장 | 첫 만족 |
| 4A장 | 통제감 (외과 수술) |
| 4B장 | 통제감 + 작은 완주 ("차 한 잔") |
| 5장 | 약간의 경외 → 친숙함 |
| 6장 | **돌파·통합** |
| 7장 | 회의·차분 |
| 8장 | 비밀이 풀리는 만족 + 정직한 기대치 |
| 9장 | 추가 봉우리의 흥분 |
| 10장 | **성취·환희 — 책의 정점** |
| 11장 | 정리·증거 |
| 12장 | 다정한 작별 |

### 클라이맥스는 어디인가

**10장.** *직접 학습한(또는 다운받은 speedrun) 모델과 처음으로 대화하는 순간.* 6장의 사전학습 클라이맥스는 *내부적 성취*(loss가 떨어진다)이고 10장은 *외부적 성취*(대화한다)다. 두 봉우리 사이 7장의 짧고 깊은 골짜기 + 8~9장의 두 단계 오르막이 *진폭*을 만든다.

---

## 5. 부록·전후 페이지 (재정리)

### 서문 (약 1만 자)
- 카르파시 트윗을 처음 본 순간의 정서.
- 누구를 위한 책인가, 무엇이 아닌가.
- *코드 인용 규칙* — 5/20줄 임계와 *코드 펴기 신호*.
- *수식 양보 예고* — 5장에 단 한 줄의 Newton-Schulz 점화식이 등장한다는 사실.
- 실습 박스 표기 — `[CPU 30분]`·`[GPU 5분]`·`[선택·실험적]`.
- 저자(Toby-AI) 메모.
- 감사.

### 에필로그 (약 5천 자)
- 책을 다 쓴 시점의 회고.
- 카르파시의 "AI agent가 안 도와줬다" 발언을 정면으로 다룬다.
- 다음 책장.

### 책 앞 면지 한 페이지 (리뷰 §J.3 반영)
- 디렉토리 맵 다이어그램 한 장 — *책을 들고 다닐 수 있는 지도*.

### 부록 A — 모듈 한 줄 요약과 데이터 흐름 (약 4천 자)
- `nanochat/`/`scripts/`/`tasks/`/`runs/` 각 파일의 *한 문장 요약*.
- 데이터 흐름 다이어그램 (레퍼런스 §2.3의 재정리).

### 부록 B-1 — 에러 메시지를 읽는 법 (약 2천 자) (리뷰 §H.2 신설)
- CUDA OOM 메시지의 *어느 두 줄을 먼저 보는가*.
- `torch.compile` fall-back 경고 — 무시해도 되는 경우와 아닌 경우.
- FA3 빌드 실패 — kernels 라이브러리의 fallback이 자동으로 일어나는지 확인하는 한 줄.
- NCCL timeout — DDP에서 한 rank가 죽었을 때의 *증상*.
- *한국어 독자가 영어 에러 앞에서 멈추는 지점*에 대한 *메타 가이드*.

### 부록 B-2 — 트러블슈팅 시나리오 (약 1.3만 자)
- OOM과 `--device-batch-size` 튜닝.
- CPU/MPS 한계와 우회 (loss_eval의 int32 cast 분기 등).
- dtype 자동선택 표.
- 분산 vs 단일 GPU vs CPU.
- 학습이 발산하면.
- 평가가 이상하면 (MMLU letter 토큰 함정 등).
- 첫 다운로드가 끊겼을 때 — `nanochat.dataset`의 resume.

### 부록 C — 용어집 + 참고문헌 (약 1.5만 자)
- 용어집: BPE, RoPE, RMSNorm, ReLU², SwiGLU, GQA, sliding window, value embeddings, smear, backout, Muon, Newton-Schulz, Polar Express, NorMuon, cautious WD, ZeRO-2, FlashAttention, FP8, KV cache, prefill, decode, REINFORCE, GRPO, DAPO, CORE, ChatCORE, bits-per-byte, MMLU, ARC, GSM8K, HumanEval, SpellingBee, midtraining, SFT, RL, harness.
- 핵심 논문 26편의 한 줄 요약 + 원문 링크.
- nanochat 공식 자료 (Discussion 번호별 한 줄 요약).
- 한국어 학습 자료.

### 부록 D — 한국어 데이터로 nanochat 변형하기 (약 8천 자, 12장 본문과 짝)
- 한국어 코퍼스 정제 — AI-Hub, KoCommonCrawl, 모두의 말뭉치.
- `tok_train.py`의 `--max-chars` 조정과 vocab_size 트레이드오프.
- 한국어 SmolTalk 대체재.
- 한국어 평가의 어려움 — KMMLU·KoBEST의 짧은 소개.
- 짧은 액션 가이드: *"한국어 nanochat 작은 한 판 돌리기"*.

---

## 6. 표지 컨셉 (러프) — 부제만 갱신

라운드 1의 키 이미지·색감·타이포 방향은 그대로. 부제만 강화 버전으로 교체:

- **메인 타이틀:** **나노챗 해부학**
- **부제 (강조):** 한 GPU 노드 3시간으로 ChatGPT를 만든다
- **부제 (작게):** 카르파시 nanochat 8천 줄 코드 해부

---

## 7. 슬러그·매니페스트 운영 표 (리뷰 §I.3 반영)

| 영역 | 값 |
|---|---|
| 작업 디렉토리 (Phase 1~3) | `nanochat-llm-book/` |
| 최종 슬러그 (Phase 5에서 전환) | `nanochat-anatomy` |
| `book_manifest.json`의 `slug` | `nanochat-anatomy` |
| `book_manifest.json`의 `title` | `나노챗 해부학` |
| `book_manifest.json`의 `subtitle` | `한 GPU 노드 3시간으로 ChatGPT를 만든다 — 카르파시 nanochat 8천 줄 코드 해부` |
| `book_manifest.json`의 `author` | `Toby-AI` (기본값) |
| `book_manifest.json`의 `license` | `CC BY-NC-SA 4.0` (기본값) |
| EPUB 파일명 | `나노챗-해부학-v{version}.epub` |
| 책 소개 markdown | `나노챗-해부학-v{version}.md` |

---

## 8. 라운드 1에서 *유지한* 결정

- **「나노챗 해부학」 제목 유지** (부제는 강화).
- **이중 클라이맥스 + 골짜기 구조 유지** (단, 챕터 번호 재정렬).
- **수식 한 줄 양보 (5장 Newton-Schulz)** — 리뷰가 *조건부*로 허용한 것을 *받아들였다*. numpy 시각화로 보완.
- **부록 D 한국어 — 본문 12장 마지막 절 + 부록 D 분리 운영.** 5천 자가 *너무 짧다*는 비판은 12장 절을 5천 자로, 부록 D를 8천 자로 분리해 합쳐 1.3만 자로 키워 해소.

---

## 9. 라운드 1·리뷰 권고 중 *반영하지 않은* 것 (사유 포함)

1. **「나노챗 해부학」을 더 검색 친화적인 제목으로 바꾸자는 권고 (리뷰 §I.1)는 *반영하지 않는다*.** 책의 *진짜 차별점*은 "8천 줄 한 작품을 끝까지 따라간다"이고 "해부학"이 그 정체성에 가장 가까운 메타포다. 부제 강화로 검색·결과 약속을 보완.
2. **5장 수식 *전면 허용*은 *조건부*로만 반영.** 단 한 줄(Newton-Schulz 점화식)만 본문에 허용하고, 나머지 모든 곳은 코드와 그림으로. 토비 스타일의 *수식 거리두기*를 *예외적 한 줄*로 유지하는 균형.
3. **12장을 *새 질문*으로 닫자는 권고 (리뷰 §G.2)는 *과도*하다고 본다.** 토비 스타일의 *다정한 작별*은 *닫힌 원*에 더 어울린다. "당신의 nanochat을 한 번 만들어 두자"라는 청유형 한 줄이면 *열린 닫음*이 *과도하지 않게* 달성된다.
4. **목표 분량을 *32~38만 자*로 낮추라는 권고 (리뷰 §J.1)는 *부분 반영*.** 본문 33~36만 자 + 부속 5만 자 = 약 38만 자 총합으로 *현실화*하되, 32만 자는 *너무 짧다*고 판단 — 4A·4B 분리 + RL 9장 승격 + report 11장 신설로 챕터 수가 늘었고, 각각의 호흡을 살리려면 38만 자 총합이 필요.

---

## 보고용 요약

### 갱신된 02_plan.md 경로
`/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/nanochat/nanochat-llm-book/02_plan.md`

### 변경된 챕터 구조 요약

- **10장 → 12장.** 4장이 4A·4B로 분리(리뷰 Top 1), RL이 9장으로 승격(리뷰 Top 4), report가 11장 신설(리뷰 §H.3·H.4).
- **분량 합계:** 본문 약 **33~36만 자** + 부속 약 5만 자 = **총 약 38만 자 / 320~360페이지**.
- **챕터별 분량:** 1장 3만 / 2장 3.5만 / 3장 2.5만 / **4A장 3만** / **4B장 2.5만** / 5장 3만 / **6장 3.5만** / **7장 2.5만** / 8장 3만 / **9장 2만** / **10장 3만** / 11장 2만 / 12장 2.5만 = 약 33.5만 자.

### 가장 큰 변경 한 줄

**4장 한 챕터(5.5만 자)를 4A·4B 두 챕터로 쪼개고, RL을 8장에서 분리해 9장으로 승격해 전체 구조를 10장 → 12장으로 재설계 — 곡선의 *오르막은 더 자주, 봉우리는 더 또렷하게*.**

### 무시한 리뷰 권고 한 줄

**제목 「나노챗 해부학」을 유지하기로 한 결정 — 책의 *진짜 차별점*("8천 줄 한 작품을 끝까지 따라간다")에 가장 가까운 메타포이기 때문. 검색 노출은 강화된 부제("한 GPU 노드 3시간으로 ChatGPT를 만든다")로 보완.**
