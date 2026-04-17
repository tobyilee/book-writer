# 논문 리서치: LLM의 기초 개념과 실습 (입문자용 책의 학술 근거 자료)

> **대상 독자:** Java/Python 중급 개발자. ChatGPT는 써봤지만 내부는 블랙박스. 수학적 증명은 축약, 직관·결과·비유 위주.
> **수집 편수:** 9편 (서베이 1편 포함)
> **조사 시점:** 2026-04-17

---

## 논문 1: Attention Is All You Need

- **저자·연도:** Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (2017)
- **발표처:** NeurIPS 2017 (최초 arXiv 공개 2017-06-12)
- **arXiv ID:** 1706.03762
- **피인용수:** 130,000+ (2026-04 기준, Google Scholar, 역대 AI 논문 중 최상위권)

**요약 (3~5문장):**
기존 번역 모델은 RNN·LSTM 또는 CNN에 의존해 순차 계산 때문에 병렬화가 어려웠다. 이 논문은 순환·합성곱을 모두 제거하고 오직 어텐션(Attention)만으로 구성된 Transformer 아키텍처를 제안한다. WMT 2014 영-독 번역에서 28.4 BLEU, 영-불 41.8 BLEU로 당시 SOTA를 경신했고, GPU 8장으로 3.5일 학습이라는 효율도 보였다. 이후 BERT·GPT·Llama·ChatGPT까지 거의 모든 대형 언어모델의 토대가 되었다.

**방법론 요약 (비전공자 눈높이):**
- 문장을 토큰(단어 조각) 시퀀스로 입력 → 각 토큰이 같은 문장 내 "어떤 토큰을 얼마나 참조할지" 스스로 가중치를 학습하는 **Self-Attention**을 도입.
- 여러 "시점"을 동시에 보는 **Multi-Head Attention**으로 문법·의미·위치 등 다양한 관계를 병렬 포착.
- 순서 정보는 **Positional Encoding**(사인/코사인 주기 함수)을 더해 보존.
- RNN과 달리 모든 단어를 한꺼번에 처리 → **GPU 병렬화에 최적화**.

**핵심 수치·결과:**
- WMT'14 En→De: **28.4 BLEU** (+2.0 vs 당시 최고)
- WMT'14 En→Fr: **41.8 BLEU** (SOTA)
- 학습 시간: **3.5일 / 8 GPU** (기존 대비 1/10 수준)

**인용할 만한 문장:**
> "The Transformer ... based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."

**독자 전달 방식 제안:**
- 비유: "회의실에서 발표자 한 명(RNN)이 순서대로 말하던 방식 → 참석자 전원이 서로를 동시에 보며 중요도에 따라 고개를 돌리는 방식(Self-Attention)으로 바뀐 것."
- Java 개발자 관점: "Stream의 `forEach`(순차)에서 `parallelStream`(병렬)으로 전환된 효과 + 각 요소가 다른 요소를 주목할 수 있는 기능 추가."
- 실습 연결: HuggingFace `transformers`로 pretrained 모델 불러오기 → Attention map 시각화 데모.

---

## 논문 2: Language Models are Unsupervised Multitask Learners (GPT-2)

- **저자·연도:** Radford, Wu, Child, Luan, Amodei, Sutskever (2019)
- **발표처:** OpenAI Technical Report (arXiv 등재 없음; OpenAI 블로그 + PDF 공개)
- **PDF:** https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
- **피인용수:** 14,000+ (Semantic Scholar)

**요약 (3~5문장):**
GPT-2는 1.5B 파라미터의 Transformer 디코더 전용 모델로, WebText(Reddit 링크 기반 40GB 텍스트)로 사전학습되었다. 핵심 주장은 "충분히 큰 언어모델은 태스크별 파인튜닝 없이도 제로샷(zero-shot)으로 다양한 NLP 태스크를 수행한다"는 것. 독해·번역·요약·QA 8개 벤치마크 중 7개에서 SOTA 또는 준-SOTA를 달성했다. 공개 직후 "너무 위험해서 전체 가중치를 공개할 수 없다"는 OpenAI의 단계적 공개 논란으로 AI 안전 담론의 분기점이 되었다.

**방법론 요약 (비전공자 눈높이):**
- GPT-1 대비 모델을 10배 키우고(1.5B), 데이터도 더 깨끗하고 크게(WebText 8백만 페이지).
- 태스크 지시를 **프롬프트(자연어)** 로 주면 모델이 알아서 수행 — "Translate English to French: ..."처럼.
- 파인튜닝 없이 "언어모델링" 한 가지 목표만으로 학습했는데 번역·요약까지 되는 **이머전트(emergent) 거동** 관찰.

**핵심 수치·결과:**
- 모델 크기: **1.5B 파라미터** (GPT-1 117M의 약 13배)
- 학습 데이터: **40GB WebText** (800만 웹페이지)
- LAMBADA 퍼플렉시티: **35.76 → 8.63** (SOTA 경신)
- 8개 LM 벤치마크 중 7개에서 zero-shot SOTA

**인용할 만한 문장:**
> "Large language models trained on sufficiently diverse datasets are able to perform well across many domains and datasets ... suggesting high-capacity models ... learn to perform a surprising amount of tasks without the need for explicit supervision."

**독자 전달 방식 제안:**
- 서사: ChatGPT의 "조상". BERT(2018)가 "문장 이해" 챔피언이라면 GPT-2는 "문장 생성" 챔피언. 오늘날 ChatGPT가 프롬프트 하나로 번역·요약·코딩까지 하는 특성의 출발점.
- 강조: "태스크를 프로그래밍(fine-tune)하지 말고, **설명(prompt)해라**" — 이 패러다임 전환이 여기서 시작.
- 실습 연결: HuggingFace에서 `gpt2` 모델을 직접 로드해 한 문장 이어쓰기 → 파라미터 수가 품질에 미치는 영향 체감.

---

## 논문 3: Language Models are Few-Shot Learners (GPT-3)

- **저자·연도:** Brown et al. (총 31명, Tom B. Brown 외) (2020)
- **발표처:** NeurIPS 2020 (Best Paper Award)
- **arXiv ID:** 2005.14165
- **피인용수:** 40,000+

**요약 (3~5문장):**
GPT-3는 175B 파라미터로 GPT-2보다 100배 이상 큰 모델이다. 이 논문의 진짜 발견은 크기 자체가 아니라 **"In-Context Learning"** — 프롬프트 안에 몇 개 예시만 주면(few-shot), 파라미터를 전혀 업데이트하지 않고도 새 태스크를 수행한다는 점이다. 번역·QA·산술·코드 생성·신규 단어 사용 등 광범위한 태스크에서 파인튜닝된 전용 모델과 견줄 만한 성능을 보였다. 또한 인간이 쓴 것과 구별이 어려운 뉴스 기사를 생성해 사회적 영향 논의를 촉발했다.

**방법론 요약 (비전공자 눈높이):**
- GPT-2와 동일한 디코더 전용 Transformer, 단순히 **"더 크게, 더 많은 데이터로"** 확장.
- 학습은 pretraining 한 번만. 테스트 시에는 가중치 고정(frozen).
- 프롬프트에 넣는 예시 개수에 따라 **zero-shot / one-shot / few-shot(보통 10~100개)** 으로 평가.

**핵심 수치·결과:**
- 파라미터: **175B** (디코더 전용 Transformer 96층)
- 학습 데이터: **약 300B 토큰** (Common Crawl, WebText2, Books, Wikipedia)
- TriviaQA few-shot: **71.2%** (파인튜닝 SOTA 와 유사)
- 산술(2자리 덧셈) few-shot: **100%** (모델이 클수록 선형 개선)
- "사람이 만든 뉴스와 구별" 정확도: **52%**(거의 무작위 수준)

**인용할 만한 문장:**
> "Humans can generally perform a new language task from only a few examples or from simple instructions — something which current NLP systems still largely struggle to do."
> "Scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even becoming competitive with prior state-of-the-art fine-tuning approaches."

**독자 전달 방식 제안:**
- 비유: "IDE의 자동완성"이 드디어 "페어 프로그래머"가 된 순간. 같은 모델에 질문만 바꾸면 번역기, QA봇, 계산기가 된다.
- Java/Python 개발자용 훅: "함수 호출 대신 프롬프트 호출"이라는 새 인터페이스. 이 논문이 "프롬프트 엔지니어링"이라는 직군의 탄생점.
- 실습 연결: OpenAI API로 `temperature=0`에서 few-shot 예시 0/1/3/10개를 바꿔가며 정답률 관찰.

---

## 논문 4: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

- **저자·연도:** Devlin, Chang, Lee, Toutanova (Google) (2018)
- **발표처:** NAACL 2019 (Best Long Paper)
- **arXiv ID:** 1810.04805
- **피인용수:** 100,000+ (NLP 논문 중 최다 인용)

**요약 (3~5문장):**
BERT는 Transformer의 **인코더만** 사용해 양방향 문맥(왼쪽+오른쪽)을 동시에 읽도록 사전학습한 모델이다. 학습 목표는 (1) 문장의 15% 단어를 가리고 맞추는 **Masked Language Modeling(MLM)**, (2) 두 문장이 이어지는지 판별하는 **Next Sentence Prediction**. 사전학습한 BERT에 출력층 하나만 얹고 파인튜닝하면 11개 NLP 태스크에서 SOTA를 경신했다. GPT가 "생성" 계보라면 BERT는 "이해·분류·검색" 계보의 원조.

**방법론 요약 (비전공자 눈높이):**
- GPT: 왼쪽→오른쪽 한 방향으로만 예측 (다음 단어).
- BERT: 문장 중간 단어를 가려놓고 양쪽 문맥을 동시에 보며 맞추기 → "빈칸 채우기 시험" 방식.
- 사전학습 후 분류·QA·NER 등 각 태스크에 소량 데이터로 **fine-tuning**.

**핵심 수치·결과:**
- GLUE 평균: **80.5%** (+7.7%p)
- MultiNLI 정확도: **86.7%** (+4.6%p)
- SQuAD v1.1 F1: **93.2** / v2.0 F1: **83.1**
- 모델 크기: BERT-Base 110M / BERT-Large 340M

**인용할 만한 문장:**
> "BERT is conceptually simple and empirically powerful."
> "Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers."

**독자 전달 방식 제안:**
- 비유: GPT는 "소설가(앞을 보며 이어 쓴다)", BERT는 "독자·검토자(문장 전체를 읽고 의미를 판정한다)".
- 개발자 관점: 오늘날 검색 엔진·추천·챗봇 의도 분류 등 "읽고 이해하는" 프로덕션 NLP의 다수가 BERT 계열(RoBERTa, DeBERTa, DistilBERT 등).
- 실습 연결: `transformers`의 `bert-base-uncased`로 감정 분류 파인튜닝 15분 실습.

---

## 논문 5: Scaling Laws for Neural Language Models

- **저자·연도:** Kaplan, McCandlish, Henighan, Brown et al. (OpenAI) (2020)
- **발표처:** arXiv (사전인쇄), 2020-01-23
- **arXiv ID:** 2001.08361
- **피인용수:** 6,500+

**요약 (3~5문장):**
언어모델의 손실(loss)이 모델 크기(N), 데이터 크기(D), 연산량(C) 각각에 대해 **단순한 거듭제곱 법칙(power law)** 을 따른다는 것을 7자릿수 범위에서 실증했다. 즉 N·D·C를 몇 배 늘리면 loss가 얼마나 줄지 수식으로 예측 가능하다. 아키텍처 세부(깊이 vs 너비 등)는 넓은 범위에서 거의 영향 없음. 이 법칙이 GPT-3의 "무작정 크게 키우자"는 결정을 정당화했고, 이후 업계의 스케일 경쟁의 출발점이 됐다.

**방법론 요약 (비전공자 눈높이):**
- 파라미터 수, 데이터 크기, GPU 연산량을 여러 조합으로 바꿔가며 수백 번 학습.
- log-log 그래프에 찍으니 거의 **직선(=거듭제곱 법칙)**.
- 결론: 고정 예산이 있을 때 "큰 모델을 **수렴 전까지만** 학습"하는 게 최적.

**핵심 수치·결과:**
- Loss ∝ N^{-0.076}, D^{-0.095}, C^{-0.050} (대략)
- 7자릿수 범위(모델 10³~10⁹ 파라미터)에서 일관
- 컴퓨트 최적 할당: **N ∝ C^{0.73}**, D ∝ C^{0.27} (이 비율은 후에 Chinchilla가 수정)

**인용할 만한 문장:**
> "Larger models are significantly more sample-efficient, such that optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence."

**독자 전달 방식 제안:**
- 비유: "요리 재료(데이터) × 조리기구 크기(모델) × 가열 시간(컴퓨트)"의 조합에 따라 맛(품질)이 **예측 가능한 곡선**을 그린다.
- 임팩트 포인트: "GPT-3는 도박이 아니라 계산이었다" — 만들기 전에 어느 정도 성능이 나올지 예측하고 들어간 프로젝트였음.
- 주의: 2년 뒤 Chinchilla(논문 6)가 이 법칙의 **D 비율을 상향 수정**했다는 점을 세트로 소개.

---

## 논문 6: Training Compute-Optimal Large Language Models (Chinchilla)

- **저자·연도:** Hoffmann et al. (DeepMind) (2022)
- **발표처:** NeurIPS 2022
- **arXiv ID:** 2203.15556
- **피인용수:** 3,500+

**요약 (3~5문장):**
DeepMind는 70M~16B 파라미터 × 5B~500B 토큰 조합으로 **400+ 개 모델을 학습**해 "고정 컴퓨트에서 최적 크기·데이터 비율"을 재측정했다. 결론은 Kaplan(2020)이 과소추정했다는 것 — **파라미터 1개당 토큰 약 20개**가 최적. 이를 검증하려 70B 파라미터 Chinchilla를 Gopher(280B)와 동일 컴퓨트로 학습, 거의 모든 벤치마크에서 Gopher·GPT-3·Jurassic을 능가했다. MMLU에서 67.5%(Gopher 대비 +7%p). 현재 대부분의 LLM(LLaMA 포함)이 이 "Chinchilla 스케일링"을 기본 가이드라인으로 삼는다.

**방법론 요약 (비전공자 눈높이):**
- 세 가지 실험 설계(IsoFLOP, 고정 모델 크기 스윕, 파라메트릭 손실 피팅)로 교차 검증.
- 핵심 발견: **모델 크기 2배 늘릴 때 데이터도 2배** 늘려야 함(선형 1:1).
- 기존 LLM(GPT-3 175B를 300B 토큰으로 학습)은 **심각하게 데이터 부족**.

**핵심 수치·결과:**
- **모델 파라미터당 토큰 ≈ 20** (컴퓨트 최적)
- Chinchilla: **70B 파라미터 × 1.4T 토큰** = Gopher(280B × 300B)와 동일 컴퓨트
- MMLU: Chinchilla **67.5%** vs Gopher 60.0%
- 150+ 다운스트림 태스크에서 일관된 우위

**인용할 만한 문장:**
> "For compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens should also be doubled."
> "Current large language models are significantly undertrained."

**독자 전달 방식 제안:**
- 비유: "용량 큰 솥에 재료를 너무 조금 넣으면 안 된다" — 모델이 아무리 커도 먹는 데이터가 적으면 잠재력을 못 쓴다.
- 업계 영향: LLaMA(7B를 1T 토큰으로), Llama 2(2T 토큰)가 모두 이 법칙 적용. "왜 요즘 LLM은 작아도 강한가?"의 답.
- 실습 연결: 같은 컴퓨트로 "크게 조금" vs "작게 많이" 학습한 결과 비교 데모 아이디어.

---

## 논문 7: Training Language Models to Follow Instructions with Human Feedback (InstructGPT)

- **저자·연도:** Ouyang, Wu, Jiang et al. (OpenAI) (2022)
- **발표처:** NeurIPS 2022
- **arXiv ID:** 2203.02155
- **피인용수:** 11,000+

**요약 (3~5문장):**
GPT-3는 똑똑하지만 사용자 의도와 어긋난 답·거짓말·유해 발화를 했다. 이 논문은 **(1) 지도학습 파인튜닝(SFT) → (2) 보상모델 학습 → (3) PPO 강화학습(RLHF)** 3단계로 "사람이 선호하는 답"을 하도록 정렬(alignment)했다. 놀라운 결과: **1.3B InstructGPT가 175B GPT-3보다 사람 평가에서 선호됨**. 파라미터 100배 적어도 정렬이 맞으면 이긴다. ChatGPT(2022-11)의 직계 전신.

**방법론 요약 (비전공자 눈높이):**
- **Step 1 (SFT):** 라벨러가 "좋은 답변" 예시를 직접 작성 → GPT-3 파인튜닝.
- **Step 2 (Reward Model):** 같은 프롬프트에 대한 여러 답변을 라벨러가 순위매김 → 이 순위를 예측하는 보상모델 학습.
- **Step 3 (RLHF):** 보상모델을 점수판 삼아 정책(LLM)을 PPO로 강화학습.

**핵심 수치·결과:**
- **1.3B InstructGPT vs 175B GPT-3**: 라벨러 선호율 85% vs 15% (100배 작은 모델이 이김)
- TruthfulQA 진실성: **+25%p**
- 유해 출력 감소: **-25%**
- 환각(hallucination): 21% → 17%

**인용할 만한 문장:**
> "Fine-tuning with human feedback is a promising direction for aligning language models with human intent."
> "Labelers significantly prefer InstructGPT outputs over outputs from GPT-3 ... despite having 100× fewer parameters."

**독자 전달 방식 제안:**
- 비유: "지식 많은 대학원생(GPT-3) → 고객 응대 교육 받은 컨설턴트(InstructGPT)". IQ는 같아도 소통 매너가 다르다.
- 핵심 메시지: **"Scale is not enough. Alignment matters."** 이 발견이 ChatGPT 열풍의 직접적 원인.
- 개발자 실습: OpenAI Fine-tuning API로 SFT만 흉내 내보기 → 작은 데이터에서도 톤·스타일 변화 체감.

---

## 논문 8: Constitutional AI: Harmlessness from AI Feedback

- **저자·연도:** Bai et al. (Anthropic) (2022)
- **발표처:** arXiv (Anthropic Technical Report)
- **arXiv ID:** 2212.08073
- **피인용수:** 2,000+

**요약 (3~5문장):**
InstructGPT의 RLHF는 유해 답변 식별에 **인간 라벨링** 이 필수라 비용·일관성 문제가 크다. Anthropic은 "AI가 자기 답변을 스스로 비판·수정"하도록 하는 **Constitutional AI(CAI)** 를 제안한다. 사람은 "원칙(헌법)"만 몇 문장 써주면 AI가 그 원칙에 비춰 자기 출력을 리뷰·수정·선호 판정(RLAIF). 결과: 유해한 질문에 회피하지 않고 "왜 답하지 않는지 설명하는" 비-회피적·비-공격적 어시스턴트 달성. Claude의 핵심 학습 기법.

**방법론 요약 (비전공자 눈높이):**
- **SL 단계:** 초기 모델이 응답 생성 → 같은 모델이 "헌법 조항"에 비춰 자기 비평 → 자기 수정 → 수정본으로 파인튜닝.
- **RL 단계:** 모델이 답변 2개 생성 → 다른 모델이 "어느 쪽이 더 원칙에 맞나" 판정 → 이 AI 선호로 보상모델 학습 → PPO (**RLAIF**).
- 중간에 **Chain-of-Thought** 추론을 넣어 투명성 향상.

**핵심 수치·결과:**
- 유해 라벨링 **인간 개입 0** (원칙만 사람이 제공)
- 유해성(harmlessness)·도움성(helpfulness) 파레토 프런티어에서 RLHF보다 **비-회피성** 크게 개선
- 헌법 16개 원칙(예: "가장 무해하고 덜 비판적이며 인종차별·성차별이 적은 응답을 선택하라")

**인용할 만한 문장:**
> "The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'."
> "These methods make it possible to control AI behavior more precisely and with far fewer human labels."

**독자 전달 방식 제안:**
- 비유: RLHF = "매 건마다 상사가 OK/NG 도장" / CAI = "회사 행동강령을 주고 직원이 스스로 검토". 확장성이 다르다.
- 현재 상품 연결: "당신이 지금 Claude를 쓰고 있다면 그건 이 논문의 기법으로 훈련된 모델" — 입문 독자에게 친숙한 지점.
- 책에서의 역할: "Alignment 기법의 진화 타임라인"(SFT → RLHF → RLAIF/CAI)에 세 번째 칸으로 배치.

---

## 논문 9: Llama 2: Open Foundation and Fine-Tuned Chat Models

- **저자·연도:** Touvron, Martin, Stone et al. (Meta, 67명) (2023)
- **발표처:** arXiv (Meta AI Technical Report), 2023-07-18
- **arXiv ID:** 2307.09288
- **피인용수:** 13,000+

**요약 (3~5문장):**
7B·13B·70B 파라미터의 **상용 허용 오픈 가중치** 모델. Meta는 pretraining(2T 토큰, Chinchilla 법칙 이상으로 데이터 증량) + SFT + **RLHF(PPO + Rejection Sampling)** 를 모두 공개했다. Llama 2-Chat은 오픈소스 챗 모델 중 SOTA, 도움성에서는 ChatGPT(3.5)에 근접하고 안전성에서는 근접-상회 평가를 받았다. 출간과 함께 공개 생태계(HuggingFace, llama.cpp, Ollama)가 폭발적으로 성장 → "로컬 LLM"의 실용화 분기점.

**방법론 요약 (비전공자 눈높이):**
- Pretraining: 공개 데이터 2T 토큰(LLaMA 1 대비 40% 증가), 컨텍스트 4K.
- **Ghost Attention(GAtt)** : 여러 턴 대화에서 시스템 지시가 흐려지지 않게 하는 기법.
- RLHF를 반복적으로 수행하며 **Rejection Sampling + PPO** 를 같이 적용.
- Helpfulness·Safety **각각의 별도 보상모델** 을 운영하는 게 특징.

**핵심 수치·결과:**
- 모델: **7B / 13B / 70B**
- 사전학습 토큰: **2T** (Llama 1 1T의 2배)
- 컨텍스트 윈도우: **4096 토큰**
- Llama-2-70B-Chat 승률: GPT-3.5 대비 **36% 승 / 32% 무승부 / 32% 패** (Meta 인간평가 기준)

**인용할 만한 문장:**
> "Our fine-tuned LLMs, called Llama 2-Chat, are optimized for dialogue use cases. Our models outperform open-source chat models on most benchmarks we tested, and ... may be a suitable substitute for closed-source models."

**독자 전달 방식 제안:**
- 비유: "Android of LLMs". iOS(GPT-4, Claude)도 있지만 누구나 포팅·튜닝 가능한 오픈 플랫폼의 도래.
- 개발자 훅: **"당신의 MacBook에서 돌아가는 GPT-3.5급 모델"** — `ollama run llama2` 한 줄로 실습.
- 책 구성 제안: "API 호출형 LLM vs 로컬 LLM"의 장을 열 때 이 논문을 기초로 배치. Java/Python에서 `llama.cpp` HTTP 서버 호출 예제.

---

## 논문 10 (서베이): A Survey of Large Language Models

- **저자·연도:** Zhao, Zhou, Li et al. (Renmin University + Tsinghua) (2023, v19 최신 2026-03)
- **발표처:** arXiv (초안, 2026년 4월 현재 v19까지 지속 업데이트)
- **arXiv ID:** 2303.18223
- **피인용수:** 6,000+ (LLM 서베이 중 최다 피인용)

**요약 (3~5문장):**
LLM 분야 전체를 조감하는 **대표 서베이 논문**. 통계적 언어모델 → 신경망 LM → Pretrained LM → LLM(100B+)의 진화 흐름, GPT·LLaMA·PaLM·Gemini 등 주요 계열의 계보도, Pretraining/Fine-tuning/Prompting/Alignment 4대 기법 체계, 평가 벤치마크·데이터셋·오픈 라이브러리까지 한 편으로 망라. **Emergent Abilities**(임계 스케일 초과 시 질적 도약)를 강조하며, 입문자가 전체 지형도를 먼저 잡는 데 가장 유용. v19까지 지속 업데이트돼 2025~2026 최신 모델도 반영.

**방법론 요약 (비전공자 눈높이):**
- 이 논문은 실험 논문이 아니라 **지형도**. 500+ 편 LLM 문헌을 카테고리·연대·기술계보로 정리.
- 주요 파트: (1) Pretraining, (2) Adaptation Tuning(SFT·RLHF 등), (3) Utilization(프롬프팅·CoT·ICL), (4) Capacity Evaluation, (5) 자원·데이터·코드 목록.

**핵심 내용:**
- "Emergent ability": 작은 모델엔 없던 능력이 특정 크기 이상에서 "갑자기" 등장 (예: few-shot 수학, 지시 따르기).
- ICL(In-Context Learning), CoT(Chain-of-Thought), RAG, Tool Use 등 모든 주요 기법의 역사와 상호관계 제공.

**인용할 만한 문장:**
> "When the parameter scale exceeds a certain level, these enlarged language models not only achieve a significant performance improvement but also show some special abilities that are not present in small-scale language models."
> "LLM advances will revolutionize the way how we develop and use AI algorithms."

**독자 전달 방식 제안:**
- 책의 **오리엔테이션 장**에서 "이 분야는 지금 어디쯤 와 있는가?"의 지도로 사용.
- 참고도서 목록의 첫 자리에 배치 — 독자가 심화 학습 시 돌아가 볼 허브.
- 한 문장 요약: "LLM 생태계의 위키피디아. 각 개별 논문(1~9번)을 어디에 위치시킬지 보여주는 좌표계."

---

## 수집 메타데이터

- **시기 균형:** 2017(1편) · 2018(1편) · 2019(1편) · 2020(2편) · 2022(3편) · 2023(2편, 서베이는 2026 버전까지 업데이트 중) — 고전·최신 고루 포함.
- **주제 균형:**
  - 아키텍처: #1(Transformer), #4(BERT)
  - 스케일: #2(GPT-2), #3(GPT-3), #5(Kaplan), #6(Chinchilla)
  - 정렬(Alignment): #7(InstructGPT/RLHF), #8(Constitutional AI)
  - 오픈/생태계: #9(Llama 2)
  - 서베이: #10(Zhao 2023)
- **모두 arXiv 또는 공식 PDF로 접근 가능.** Abstract 기반으로 작성. 본문 수치는 abstract·공식 발표 자료·널리 알려진 값 교차 확인.

## 출처 (Sources)

- [Semantic Scholar — Language Models are Unsupervised Multitask Learners](https://www.semanticscholar.org/paper/Language-Models-are-Unsupervised-Multitask-Learners-Radford-Wu/9405cc0d6169988371b2755e573cc28650d14dfe)
- [OpenAI — GPT-2 official PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- arXiv abstract 페이지: 1706.03762, 2005.14165, 1810.04805, 2001.08361, 2203.15556, 2203.02155, 2212.08073, 2307.09288, 2303.18223
