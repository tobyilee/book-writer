# 부록 C. 더 읽을거리 — 난이도 태그 카탈로그

10장이 다음 걸음의 **방향**을 그려준 지도였다면, 이 부록은 그 걸음마다 **언제 어떤 자료를 펼지**를 난이도와 성격으로 줄 세운 카탈로그다. 10장의 포인터가 분기마다 한두 건을 꽂는 이정표라면, 이 부록은 같은 주제를 가로로 눕혀 ★ → ★★ → ★★★로 이어지는 계단을 만들어둔 책장에 가깝다. 한꺼번에 다 읽으려 들지 말고, 지금 이 순간 손에 닿는 한 건만 고르자.

## 난이도 태그의 뜻

- **★** 한 시간 이내. 영상·블로그·한국어 자료 위주. 입문 직후 커피 한 잔 분량으로 소화된다.
- **★★** 반나절에서 하루. 영어 기술 블로그, 논문 해설, 공식 문서. 어느 정도 기반이 필요하지만 손에 잡힌다.
- **★★★** 여러 날. 원논문, 수식, 구현. 해당 분야로 깊이 파고들 때 펴자.

분류는 딱딱하지 않게 읽어두자. ★ 자료를 하루에 다 끝내도 좋고, ★★★을 한 달에 걸쳐 나눠 읽어도 이상하지 않다.

## C.1 기초 이론 — 트랜스포머·어텐션·임베딩

- **★** 3Blue1Brown "Neural Networks" 시리즈 (Ch.5 Transformers, Ch.6 Attention, 한국어 자막). **3장에 들어가기 전**에 한 번, **3장을 덮고 나서** 한 번 더 보기를 권한다.
- **★** Illustrated Transformer 한국어 번역판(nlpinkorean). 3장 어텐션 그림을 펼치기 **직후**에 펴면 문장이 잘 붙는다.
- **★★** Hugging Face LLM Course. 2~5장 내용을 공식 문서 톤으로 복습하고 싶을 때.
- **★★** The Annotated Transformer (Harvard NLP). 수식과 PyTorch 코드를 나란히 읽고 싶을 때.
- **★★★** Vaswani et al. 2017, *Attention Is All You Need* (arXiv:1706.03762). 3장을 읽고 나서, 10장 "논문 한 편 혼자 읽기" 박스의 시연 순서대로 도전하기 좋다.

## C.2 손 실습 — from scratch · 미니 GPT

- **★** Karpathy, *Let's build GPT* (2023, 2시간 영상). 4장의 뼈대가 이 영상이다. 4장을 열기 **전 주말**에 한 번 돌려보자.
- **★★** `build-nanogpt` 저장소. 영상과 한 줄씩 짝을 이룬 코드. 4장 실습 중 막히면 여기와 대조하면 된다.
- **★★** `nanochat` 저장소(2025, Karpathy 최신작). nanoGPT deprecation 이후의 승계 경로. 한 사이클을 더 크게 돌려보고 싶을 때.
- **★★** Karpathy `minbpe`. 2장 토크나이저 손 실습의 원본.
- **★★★** GPT-2 원본 구현(OpenAI). 4장 미니 GPT와 같은 계열의 "실제 배포 모델"이 어떻게 생겼는지 비교해보고 싶을 때.

## C.3 파인튜닝·PEFT — LoRA·QLoRA·SFT·DPO

- **★** SK DevOcean, *Gemma 한국어 요약 파인튜닝*. 한국어 블로그로 가장 빠른 입구. 6장 실습 착수 전에 훑으면 낯섦이 줄어든다.
- **★** SK DevOcean, *Instruction Tuning* 해설. 5장 Instruction Tuning 절과 짝.
- **★★** HuggingFace PEFT 공식 문서. 6장에서 `peft` API가 헷갈릴 때 곧바로 펴면 된다.
- **★★** Unsloth Kaggle 노트북 모음 + GitHub Issue #1132 ("Fine tuning without GPU"). GPU 없는 독자의 6장 대안 경로.
- **★★** unfinishedgod, *Llama 3 파인튜닝 + HF Hub 업로드*. 6장 실습 완주 후 본인 모델 공개까지의 한국어 길잡이.
- **★★★** Dettmers et al. 2023, *QLoRA* (arXiv:2305.14314). "왜 4-bit로도 학습이 되는가"의 원문. 6장 전체를 두 번째로 돌릴 때.
- **★★★** Rafailov et al. 2023, *Direct Preference Optimization* (arXiv:2305.18290). 10장 "심화 파인튜닝" 분기의 핵심 논문.

## C.4 Scaling Laws · 정렬 — Pretraining·RLHF·CAI

- **★★** Chinchilla 블로그 해설 (DeepMind / HuggingFace). "파라미터 1 : 토큰 20" 법칙을 그림 한 장으로 감 잡기.
- **★★** OpenAI InstructGPT 블로그 + "1.3B가 175B를 이긴" 사건 해설. 5장의 감정 피크를 복습할 때.
- **★★★** Kaplan et al. 2020 / Hoffmann et al. 2022 (Chinchilla) / Llama 1·2·3 논문. 5장 Scaling Laws 3막 서사의 원문 세트.
- **★★★** Ouyang et al. 2022, *InstructGPT* (arXiv:2203.02155). 5장 RLHF 3단계의 원문.
- **★★★** Bai et al. 2022, *Constitutional AI* (arXiv:2212.08073). 5장 말미, Claude 계보의 차별점을 본문으로 확인하고 싶을 때.

## C.5 API·서비스 연결 — Python·Java

- **★** Spring AI 공식 문서의 `ChatClient` Getting Started. 7장 Java 실습의 바로 그 출발선.
- **★** LangChain4j README + examples. 7장의 "provider 스왑" 데모가 어디서 왔는지 확인하고 싶을 때.
- **★★** Spring AI Advisor·Observation 공식 블로그 + Baeldung *Introduction to Spring AI*. 7장 Advisor/관측성 절을 더 깊이 들여다볼 때.
- **★★** Thinking Machines Lab, *Defeating Nondeterminism in LLM Inference* ("Temperature=0 is a Lie" 계열). 7장 당혹감 절의 원문 근거.
- **★★** Lilian Weng, *Prompt Engineering* (OpenAI 블로그). 7장 프롬프트 기본기 절의 뼈대.
- **★★★** Wei 2022 CoT(arXiv:2201.11903) / Wang 2022 Self-Consistency / Yao 2022 ReAct. 7장에서 살짝만 건드린 프롬프트 연구의 원문 3종.

## C.6 RAG·벡터 검색

- **★** LlamaIndex Getting Started + velog·SK하이닉스 한국어 RAG 튜토리얼 1~2건. 8장 실습 들어가기 전 워밍업.
- **★** smallcherry, *RAG 프로젝트는 왜 실패하는가* (velog). 8장 실패 패턴 3종의 예고편.
- **★★** BGE-M3 모델 카드 + 한국어 임베딩 품질 비교 리포트. 3장에서 미뤄둔 BERT 계열 임베딩 논의를 8장 실습 시점에 결산할 때.
- **★★** pgvector / Chroma / Qdrant 공식 문서. 8장에서 벡터 DB 교체를 고민할 때 나란히 펴두면 편하다.
- **★★** 당근페이 FDS RAG 여정, SK하이닉스 RAG 플랫폼 성능 평가. 9장 케이스 스터디의 원문. "내 서비스에서 RAG를 돌리면 뭐가 터지는가"의 예습.
- **★★★** Lewis et al. 2020, *Retrieval-Augmented Generation* (arXiv:2005.11401) + 최신 RAG 서베이. 8장을 넘어 RAG 연구사를 통째로 훑고 싶을 때.

## C.7 거버넌스·Red-teaming

- **★** KISA *인공지능(AI) 보안 안내서*. 9장 거버넌스 절에서 법무·컴플라이언스 팀과 대화할 때의 한국어 1차 근거.
- **★★** Microsoft Prompt Shields 공식 문서 + Azure 블로그. 9장 입력 필터 절의 표준 도구.
- **★★** NVIDIA NeMo Guardrails 공식 문서. 9장에서 대화 흐름 자체를 가드레일로 잡고 싶을 때.
- **★★** garak / PyRIT / Promptfoo 저장소 README. 배포 전 red-team 스위트를 CI에 붙이고 싶을 때 순서대로 훑으면 된다.
- **★★★** HELM Safety (Stanford CRFM, arXiv:2211.09110). 9장 평가 하네스 절의 표준 벤치마크.
- **★★★** Meta Llama Guard 논문 + PurpleLlama 저장소. 입출력 분류기를 자체 모델로 돌리고 싶을 때.

## C.8 한국어 실무 레퍼런스

- **★** 카카오페이, *백엔드 개발자의 시선으로 풀어본 LLM 내부 동작 원리*. 1장 공감 인용의 원문. 지친 밤에 다시 펴면 기분이 좀 낫다.
- **★** 카카오페이, *페이증권 춘시리 AI봇*. 7·9장에서 "보안이 제일 어렵더라"의 원문.
- **★** 토스 테크, *고성능 GPU 클러스터 도입기* + *LLM 쉽고 빠르게 서빙하기*. 서문의 "요리하라고 해서 왔는데 프라이팬이 없어요"와 9장 운영 관점.
- **★★** SK하이닉스 RAG 플랫폼 구축·평가 시리즈(AWS Tech Blog). 8·9장에서 "RAG가 만능이 아닌" 수치를 인용할 때.
- **★★** 당근 GenAI 플랫폼 + 당근페이 FDS. 7장 "API 키 관리부터 막힌다"의 실제 사례.
- **★★** 스캐터랩 핑퐁팀, *RLHF로 피드백 학습시키기*. 5장 RLHF 절의 한국어 실전 기록.
- **★★★** LY Corp, *별도 가드레일이 왜 필요한가* + 카카오 *Kanana Safeguard* 기술블로그. 한국어 거버넌스 사례 중 가장 단단한 두 축. 9장 거버넌스 절을 재집필할 기세로 읽어도 아깝지 않다.

## C.9 에이전트·멀티모달·심화 — 10장 분기 보강

- **★★** Anthropic, *Building Effective Agents* + OpenAI Function Calling 가이드. 10장 에이전트 분기의 공식 입문.
- **★★** MCP (Model Context Protocol) 공식 스펙. 10장 에이전트·Tool Use 분기의 2025~2026 표준 후보.
- **★★** OpenAI Whisper / TTS 공식 문서 + VLM 튜토리얼(LLaVA, Idefics). 10장 멀티모달 분기의 첫 삽.
- **★★★** vLLM / SGLang 공식 문서 + TensorRT-LLM 가이드. 10장 추론 최적화 분기.
- **★★★** Mixtral MoE 논문(Jiang et al. 2024) + DeepSeek-V2/V3 기술 보고서. 10장 "심화 파인튜닝 + 아키텍처" 분기의 한 단계 위.
- **★★★** MT-Bench(arXiv:2306.05685), Chatbot Arena 논문. 10장 평가·안전 분기의 기준점.

## 마무리

목록이 길다고 기죽지 말자. 카테고리 하나당 **★ 딱 하나부터** 펴보는 걸로 충분하다. 그 한 시간짜리 자료가 손에 익으면 ★★가 반나절로 줄고, ★★ 몇 편이 몸에 배면 ★★★ 원논문의 초록이 생각보다 가깝게 읽힌다. 이 카탈로그는 덮어두고 필요할 때만 다시 펴면 된다. 지금 이 순간, 가장 궁금한 한 줄을 먼저 골라보자.
