# 웹 리서치: LLM(대규모 언어모델)의 기초 개념 + 간단한 모델 만들기 실습

대상 독자: Java와 Python을 다룰 줄 아는 중급 개발자. ChatGPT/Claude 같은 LLM 서비스를 사용해본 경험은 있지만 내부 원리와 모델을 직접 빌드하는 것은 처음인 사람.

수집 원칙: 공식 문서와 저자 확인 가능한 교육 자료를 우선, 한국 개발자 블로그를 적극 포함, Spring AI·LangChain4j 같은 Java 쪽 통합 자료 포함. 한국어 약 60%, 영어 약 40%.

---

## 자료 1: The Illustrated Transformer

- 출처: https://jalammar.github.io/illustrated-transformer/
- 저자·날짜: Jay Alammar · 2018-06-27 (이후 주기적 보강)
- 신뢰성: 최상 (저자 확인된 교육 자료, 업계 표준 레퍼런스)
- 핵심 주장: Transformer 아키텍처의 내부를 시각화로 한 단계씩 풀어낸다. 저자는 Transformer의 가장 큰 강점이 "병렬화 가능성(parallelization)"이며, 이것이 기존 neural machine translation 모델 대비 학습 속도와 성능을 동시에 끌어올렸다고 주장한다.
- 인용 가능한 구절:
  > "The Transformer – a model that uses attention to boost the speed with which these models can be trained."
  > "Self-attention is the method the Transformer uses to bake the 'understanding' of other relevant words into the one we're currently processing."
  > "Multi-headed attention…gives the attention layer multiple 'representation subspaces'…[with] eight sets of Query/Key/Value weight matrices."
  > "The encoder start by processing the input sequence…transformed into attention vectors…used by each decoder in its 'encoder-decoder attention' layer."
- 관련 섹션: 2장 "Transformer 아키텍처 개요", 3장 "Self-Attention의 직관"에서 다이어그램과 함께 원문 발췌 인용. 책 전체의 멘탈 모델 앵커 자료.

---

## 자료 2: The Illustrated Transformer (한국어 번역)

- 출처: https://nlpinkorean.github.io/illustrated-transformer/
- 저자·날짜: 원저자 Jay Alammar, 번역자 "찬" · 번역 2018-12-20 (원글 2018-06-27)
- 신뢰성: 최상 (원저자 허락 번역, 툴팁으로 원문 확인 가능)
- 핵심 주장: 한국 개발자들이 가장 많이 참조하는 Transformer 입문 한글 자료. 원문을 축약하지 않고 충실히 옮겼다.
- 인용 가능한 구절:
  > "attention을 활용한 모델인 Transformer – attention을 학습하여 그를 통해 학습 속도를 크게 향상시킨 모델"
  > "encoder가 하나의 특정한 단어를 encode 하기 위해서 입력 내의 모든 다른 단어들과의 관계를 살펴봅니다"
  > "여러 개의 query/key/value weight 행렬들을 가지게 됩니다 (논문에서 제안된 구조는 8개의 attention heads를 가지므로)"
- 관련 섹션: 2장 도입부 "한국어 독자에게 친숙한 레퍼런스", 각 핵심 용어(Self-Attention, Multi-Head Attention) 정의 박스.

---

## 자료 3: The Illustrated GPT-2 (Visualizing Transformer Language Models)

- 출처: https://jalammar.github.io/illustrated-gpt2/
- 저자·날짜: Jay Alammar · 2019-08-12
- 신뢰성: 최상
- 핵심 주장: GPT-2를 통해 "decoder-only Transformer"가 언어 모델링에서 어떻게 자기회귀(autoregressive) 생성을 수행하는지를 단계별 시각화로 설명한다. AllenAI의 GPT-2 Explorer UI를 활용해 다음 토큰 확률 분포를 직접 보여준다.
- 인용 가능한 구절:
  > "The GPT-2 architecture is very similar to the decoder-only transformer."
  > "display[s] ten possible predictions for the next word with their probability scores"
- 관련 섹션: 3장 "디코딩: 모델은 어떻게 다음 단어를 고르는가" 섹션의 시각적 레퍼런스. 4장 "Transformer 변형" 중 decoder-only 분기 설명.

---

## 자료 4: 3Blue1Brown — Attention in Transformers, Step-by-Step (Deep Learning Chapter 6)

- 출처: https://www.3blue1brown.com/lessons/attention
- 저자·날짜: Grant Sanderson (3Blue1Brown) · 2024-04 공개 (Chapter 5 "Transformers, the tech behind LLMs"와 한 쌍)
- 신뢰성: 최상 (수학적 시각화의 정석으로 평가받는 교육 채널, 600만+ 구독자)
- 핵심 주장: Attention은 문맥에 따라 단어 임베딩을 점진적으로 갱신하는 메커니즘이며, Query/Key/Value를 "질문–답 후보–내용"의 관점으로 이해할 수 있다.
- 인용 가능한 구절:
  > "Demystifying attention, the key mechanism inside transformers and LLMs."
  > "Conceptually, we want to think of these keys as potential answers to the queries."
- 관련 섹션: 2장 "어텐션의 직관" 도입부. QKV를 수식 없이 그림 한 장으로 설명하는 보조 자료로 추천. 영상 링크(QR 포함) 후 본문 설명 연결.

---

## 자료 5: 3Blue1Brown — Transformers, the tech behind LLMs (Deep Learning Chapter 5)

- 출처: https://www.3blue1brown.com/lessons/gpt
- 저자·날짜: Grant Sanderson · 2024
- 신뢰성: 최상
- 핵심 주장: Transformer 전체 파이프라인(토큰화 → 임베딩 → 어텐션 반복 블록 → 다음 토큰 확률 분포)을 시각적으로 단계별 추적하며 "LLM은 다음 토큰 확률 분포를 계산하는 거대한 함수"라는 핵심 멘탈 모델을 준다.
- 인용 가능한 구절: (영상 내 내레이션 핵심 포인트) 
  > "Transformers are the invention underlying tools like ChatGPT, Google Translate, and voice-to-text software."
- 관련 섹션: 1장 "LLM이란 무엇인가 — 확률 기계" 섹션의 메인 비유 자료. 전체 그림을 한 호흡으로 잡아주는 참조.

---

## 자료 6: Andrej Karpathy — "Let's build GPT: from scratch, in code, spelled out" + nanoGPT

- 출처: https://github.com/karpathy/nanoGPT (코드) / https://github.com/karpathy/build-nanogpt (영상+코드 강의)
- 저자·날짜: Andrej Karpathy · nanoGPT는 2022~2024 유지, 2025-11 deprecation 공지(nanochat으로 승계). "Let's build GPT" 강의는 2023 공개.
- 신뢰성: 최상 (OpenAI/Tesla 출신 저자, 업계가 가장 많이 추천하는 "직접 만들어보는" 자료)
- 핵심 주장: "작은 레포로도 중형 GPT를 훈련할 수 있다"는 것을 증명. 2025년 11월 기준 nanoGPT는 오래되고 deprecated 상태이지만, "Let's build GPT" 강의에서 설명하는 학습 흐름(tokenization → self-attention → multi-head → feed-forward → residual/layernorm → scaling → 사전학습/파인튜닝/RLHF 맥락)은 교육적으로 여전히 최상급.
- 인용 가능한 구절:
  > "The simplest, fastest repository for training/finetuning medium-sized GPTs."
  > "a ~300-line boilerplate training loop" / "a ~300-line GPT model definition"
  > "reproduces GPT-2 (124M) on OpenWebText, running on a single 8XA100 40GB node in about 4 days of training"
  > "On a single A100 GPU, this [Shakespeare-char] takes about 3 minutes and achieves a validation loss of 1.4697."
- 관련 섹션: 4장 "미니 언어 모델 만들기" 실습의 메인 레퍼런스. Karpathy 강의 순서를 따라 토크나이저 → 어텐션 → 블록 → 학습 루프 순으로 예제 코드 구성. 최신 대안으로 nanochat 링크도 각주 처리.

---

## 자료 7: Hugging Face LLM Course — Transformer Architectures (Chapter 1 §6)

- 출처: https://huggingface.co/learn/llm-course/en/chapter1/6
- 저자·날짜: Hugging Face (org) · 상시 업데이트 중 (현재 Llama4, Gemma3, DeepSeek-V3 포함)
- 신뢰성: 최상 (공식 교육 과정)
- 핵심 주장: Transformer의 세 변형 — encoder-only / decoder-only / encoder-decoder — 의 용처와 특징을 한 표로 정리한다. 현대 LLM 대부분은 decoder-only이며, 사전학습 → instruction tuning의 2단계로 훈련된다.
- 인용 가능한 구절:
  > "Most Transformer models use one of three architectures: encoder-only, decoder-only, or encoder-decoder (sequence-to-sequence)."
  > "Most modern Large Language Models (LLMs) use the decoder-only architecture."
  > "Modern LLMs are typically trained in two phases: 1. Pretraining: The model learns to predict the next token on vast amounts of text data  2. Instruction tuning: The model is fine-tuned to follow instructions and generate helpful responses"
  > "Encoder models are best suited for tasks requiring an understanding of the full sentence, such as sentence classification, named entity recognition, and extractive question answering."
- 관련 섹션: 2장 "Transformer 변형들" 섹션의 뼈대. 표 형태("Task → Suggested Architecture")를 참조하여 책의 정리 박스에 활용.

---

## 자료 8: Hugging Face Transformers — Fine-tuning 공식 가이드

- 출처: https://huggingface.co/docs/transformers/en/training
- 저자·날짜: Hugging Face 공식 문서 · 최신 (v5.5.4 기준)
- 신뢰성: 최상
- 핵심 주장: 파인튜닝은 "랜덤 가중치가 아닌 사전학습된 체크포인트에서 학습을 이어가는 것"이라는 한 줄 정의로 출발해, `Trainer` API 중심의 표준 워크플로우(데이터 토큰화 → 모델 로드 → `TrainingArguments` 설정 → `trainer.train()` → `push_to_hub()`)를 보여준다.
- 인용 가능한 구절:
  > "Fine-tuning continues training a large pretrained model on a smaller dataset specific to a task or domain."
  > "Fine-tuning is identical to pretraining except you don't start with random weights. It also requires far less compute, data, and time."
  > "`num_train_epochs` and `per_device_train_batch_size` control training duration and batch size. `learning_rate` sets the initial learning rate for the optimizer."
- 관련 섹션: 5장 "파인튜닝 실습 — Qwen3-0.6B 예제" 전반. `TrainingArguments` 설정 표, `DataCollatorForLanguageModeling` 주의사항 박스를 공식 문서 인용으로 채움.

---

## 자료 9: Decoding Strategies in Large Language Models (Hugging Face Blog)

- 출처: https://huggingface.co/blog/mlabonne/decoding-strategies
- 저자·날짜: Maxime Labonne · 2024-10-29 (초기 게시 후 확장)
- 신뢰성: 최상 (HF 공식 블로그, LLM Engineer's Handbook 저자)
- 핵심 주장: 같은 모델이라도 디코딩 전략(greedy, beam, temperature, top-k, top-p)에 따라 결과가 완전히 달라진다. 각 전략의 수학적 의미와 실전 트레이드오프를 코드와 함께 설명한다.
- 인용 가능한 구절:
  > "Greedy search is a decoding method that takes the most probable token at each step as the next token in the sequence."
  > "Unlike greedy search, which only considers the next most probable token, beam search takes into account the n most likely tokens, where n represents the number of beams."
  > "The temperature T is a parameter that ranges from 0 to 1, which affects the probabilities generated by the softmax function, making the most likely tokens more influential."
  > "Top-k sampling is a technique that leverages the probability distribution generated by the language model to select a token randomly from the k most likely options."
  > "Nucleus sampling…chooses a cutoff value p such that the sum of the probabilities of the selected tokens exceeds p."
- 관련 섹션: 3장 "디코딩 전략" 섹션의 정의 박스와 비교 표. 6장 "API 호출 시 파라미터 튜닝" 실습에서 `temperature`/`top_p` 실험과 연결.

---

## 자료 10: 카카오페이 기술 블로그 — 백엔드 개발자의 시선으로 풀어본 LLM 내부 동작 원리: 6단계로 쉽게 이해하기

- 출처: https://tech.kakaopay.com/post/how-llm-works/
- 저자·날짜: wi.fi (카카오페이 정산플랫폼팀) · 2025-09-11
- 신뢰성: 최상 (대형 핀테크 기술 블로그, 저자 소속 명시)
- 핵심 주장: LLM 동작 원리를 "토큰화 → 임베딩 → 위치 인코딩 → Transformer & Attention → 예측 → 디코딩" 6단계로 구조화. 백엔드 개발자의 언어(함수, 루프, 벡터 연산)로 풀어낸 한국어 자료.
- 인용 가능한 구절:
  > "LLM이 사용자의 질문을 받아 답변을 생성하기까지의 내부 동작 과정을 6단계(토큰화, 임베딩, 위치 인코딩, 트랜스포머 & 어텐션, 예측, 디코딩)로 나누어 설명합니다."
  > "최종 입력 벡터 = Word Embedding Vector + Positional Encoding Vector"
  > "Transformer는 LLM의 효율적이고 강력한 두뇌 역할을 합니다."
  > "이 과정을 자동 회귀(Autoregressive)라고 부르며, 혼자서 릴레이 소설을 쓰는 것과 유사합니다."
- 관련 섹션: 1장 서두 "개발자 관점에서 LLM 훑어보기" 및 전체 책의 목차(6단계 구조)와 매우 잘 맞는 한국어 앵커 자료. 각 단계의 한국어 용어 선정에 직접 참조.

---

## 자료 11: SK DevOcean — Instruction Tuning: LLM이 사람 말을 알아 듣는 방법

- 출처: https://devocean.sk.com/blog/techBoardDetail.do?ID=165806&boardType=techBlog
- 저자·날짜: alankim · 2024-04-08
- 신뢰성: 최상 (SK 기술 블로그, 저자 명시)
- 핵심 주장: Instruction Tuning은 pre-training과 fine-tuning의 장점을 합쳐 "사용자의 지시어를 따라 답변하도록" 모델을 유도하는 전략이며, `### Instruction: … ### Response: …` 형태의 프롬프트 템플릿이 대표적이다.
- 인용 가능한 구절:
  > "Instruction Tuning은 이 두 접근법의 장점을 결합하여 모델의 유연성과 정확성을 향상시키기 위한 전략입니다."
  > "사용자의 지시(Instruction)을 따라 답변을 하도록 설계된 지시어 기반의 데이터셋으로 학습되었으며"
  > "지시사항은 '### Instruction:' 형식으로 시작하고 그에 대한 답변(output)은 '### Response:'로 시작하도록 프롬프트를 생성"
  > "모델은 점차 사용자의 지시를 이해하고 이에 적절하게 대응하는 능력을 학습하게 됩니다."
  > "Zero-shot 즉 질문 만으로 답변을 도출 할 수 있게 만듭니다."
- 관련 섹션: 5장 "학습 파이프라인 개관"의 Instruction Tuning 섹션. 한국어 용어 정립과 "왜 Base 모델과 Instruct 모델이 다른가" 박스에 인용.

---

## 자료 12: 스캐터랩(핑퐁팀) 블로그 — 더 나은 생성모델을 위해 RLHF로 피드백 학습시키기

- 출처: https://blog.scatterlab.co.kr/luda-rlhf/  (구 URL https://tech.scatterlab.co.kr/luda-rlhf/ 는 현재 308 리다이렉트)
- 저자·날짜: 스캐터랩 핑퐁팀 · 2023-08-30
- 신뢰성: 최상 (이루다 서비스를 운영하며 실제 RLHF를 적용한 팀, 한국어 대화 LLM 실전 기록)
- 핵심 주장: RLHF는 SFT 이후 리워드 모델 학습 → PPO로 사람 선호도 정렬이라는 3단계 파이프라인으로 구성되며, 잘못 설계하면 reward hacking / mode collapse가 발생할 수 있다.
- 인용 가능한 구절:
  > "사전학습 모델은 문맥에 따라 욕설이 포함되거나 선정적인 문장, 자연스럽지 않고 이상한 문장을 생성하는 경우가 발생"
  > "Supervised Fine-tuning의 경우 주어진 문맥에 대해서 생성 모델에게 모범 답안을 주어서 올바른 답변을 모사하도록 학습이 진행됩니다"
  > "사람의 선호도를 모델에 학습하는 방법론을 Learning from Human Feedback 혹은 Human Preference Alignment라고 합니다"
  > "리워드 모델은 negative 답변에 대한 logit은 작아지고, positive 답변에 대한 logit은 커지게 학습되게 됩니다"
  > "생성 모델이 높은 리워드 점수만을 얻기 위해 리워드 모델의 약점 혹은 편향을 파고드는 리워드 해킹 또는 mode collapse가 발생"
- 관련 섹션: 5장 "RLHF" 섹션의 메인 한국어 레퍼런스. "실제로 운영하면서 만난 문제들" 박스에서 reward hacking, mode collapse 경고를 인용.

---

## 자료 13: wikidocs — 딥 러닝을 이용한 자연어 처리 입문 §13-01 BPE & §02-01 토큰화

- 출처:
  - https://wikidocs.net/22592 (BPE)
  - https://wikidocs.net/21698 (토큰화 개요)
  - https://wikidocs.net/86657 (SentencePiece)
  - https://wikidocs.net/99893 (HuggingFace Tokenizer)
- 저자·날짜: 유원준 외 · 지속적 개정 (2019~현재), 대한민국에서 가장 많이 인용되는 한국어 NLP 교재
- 신뢰성: 최상 (한국어 NLP 교재의 사실상 표준)
- 핵심 주장: 서브워드 토크나이저(BPE, WordPiece, SentencePiece)는 OOV와 희귀어를 완화하고, 한국어처럼 교착어에도 적용할 수 있는 "의미 단위에 가까운 분할"을 제공한다.
- 인용 가능한 구절:
  > "서브워드 분리(Subword segmenation) 작업은 하나의 단어는 더 작은 단위의 의미있는 여러 서브워드들(Ex) birthplace = birth + place)의 조합으로 구성된 경우가 많기 때문에, 하나의 단어를 여러 서브워드로 분리해서 단어를 인코딩 및 임베딩하겠다는 의도를 가진 전처리 작업입니다."
  > "이를 통해 OOV나 희귀 단어, 신조어와 같은 문제를 완화시킬 수 있습니다."
  > "BERT가 사용한 토크나이저는 WordPiece 토크나이저로… 바이트 페어 인코딩(Byte Pair Encoding, BPE)의 유사 알고리즘입니다."
- 관련 섹션: 2장 "토큰화" 전반. 한국어 독자의 언어 감각에 맞는 예제(교착어 특성)와 함께 인용.

---

## 자료 14: LangChain4j — 공식 Introduction

- 출처: https://docs.langchain4j.dev/intro/  (GitHub: https://github.com/langchain4j/langchain4j)
- 저자·날짜: LangChain4j 코어 팀 · 상시 업데이트 (2023 창립, 2025 기준 20+ LLM provider · 30+ embedding store 지원)
- 신뢰성: 최상 (공식 문서)
- 핵심 주장: Python 중심이던 LLM 오케스트레이션을 Java로 옮기기 위해 만들어진 라이브러리로, LLM 제공자·벡터 스토어·프롬프트·RAG·에이전트·MCP까지 통일된 API로 추상화한다.
- 인용 가능한 구절:
  > "The goal of LangChain4j is to simplify integrating LLMs into Java applications."
  > "LangChain4j offers a unified API to avoid the need for learning and implementing specific APIs for each of them."
  > "Our toolbox includes tools ranging from low-level prompt templating, chat memory management, and function calling to high-level patterns like Agents and RAG."
  > "LangChain4j features a modular design, comprising: the langchain4j-core module, which defines core abstractions (such as ChatModel and EmbeddingStore) and their APIs."
  > "We noticed a lack of Java counterparts to the numerous Python and JavaScript LLM libraries and frameworks."
- 관련 섹션: 7장 "Java에서 LLM 호출하기" 중 LangChain4j 파트. Quarkus/Spring Boot/Helidon 통합 언급과 함께 "왜 Java에도 이런 프레임워크가 필요한가" 박스에 인용.

---

## 자료 15: Spring AI — Anthropic Chat 공식 레퍼런스

- 출처: https://docs.spring.io/spring-ai/reference/api/chat/anthropic-chat.html  (메인 레포: https://github.com/spring-projects/spring-ai)
- 저자·날짜: Spring AI 팀 (VMware/Broadcom, Josh Long 외) · 1.0 GA 이후 상시 업데이트
- 신뢰성: 최상 (Spring 공식 프로젝트 문서)
- 핵심 주장: Spring AI는 Anthropic Claude뿐 아니라 OpenAI, Google, Ollama 등 주요 provider를 동일한 `ChatModel`/`ChatClient` 추상 위에서 호출하도록 해준다. 의존성 한 줄만 바꾸면 provider를 스왑 가능.
- 인용 가능한 구절:
  > "Anthropic Claude는 다양한 애플리케이션에서 사용할 수 있는 기초 AI 모델 제품군입니다. 개발자와 기업을 위해 API 접근을 활용하고 Anthropic의 AI 인프라 위에 직접 구축할 수 있습니다."
  > "Spring AI는 동기 및 스트리밍 텍스트 생성을 위한 Anthropic Messaging API를 지원합니다."
  > Maven 의존성:
  > ```xml
  > <dependency>
  >   <groupId>org.springframework.ai</groupId>
  >   <artifactId>spring-ai-starter-model-anthropic</artifactId>
  > </dependency>
  > ```
  > application.properties:
  > ```
  > spring.ai.anthropic.api-key=YOUR_API_KEY
  > spring.ai.anthropic.chat.options.model=claude-3-5-sonnet-latest
  > spring.ai.anthropic.chat.options.temperature=0.7
  > spring.ai.anthropic.chat.options.max-tokens=450
  > ```
  > 최소 컨트롤러 예제:
  > ```java
  > @RestController
  > public class ChatController {
  >   private final AnthropicChatModel chatModel;
  >   public ChatController(AnthropicChatModel chatModel) { this.chatModel = chatModel; }
  >   @GetMapping("/chat")
  >   public String chat(@RequestParam String message) {
  >     ChatResponse response = chatModel.call(new Prompt(message));
  >     return response.getResult().getOutput().getText();
  >   }
  > }
  > ```
- 관련 섹션: 7장 "Java에서 LLM 호출하기"의 Spring Boot 실습. application.properties 설정 표와 최소 컨트롤러 코드를 그대로 인용한 뒤 Python `anthropic` SDK 코드와 대조.

---

## 자료 16: Baeldung — Introduction to Spring AI

- 출처: https://www.baeldung.com/spring-ai  (관련 후속 글: https://www.baeldung.com/spring-ai-chatclient, https://www.baeldung.com/spring-ai-chat-memory, https://www.baeldung.com/spring-ai-chatclient-stream-response)
- 저자·날짜: Baeldung 기술 편집팀 · 최신 Spring AI GPT-5 기준 업데이트 (2025)
- 신뢰성: 중~최상 (Java 생태계 대표 튜토리얼 사이트, 저자 리뷰 프로세스 있음)
- 핵심 주장: `ChatClient`가 Spring AI의 중심 진입점이다. Advisor(인터셉터), Chat Memory, Structured Output, Streaming 같은 기능을 Spring 친화적 API로 제공하며, OpenAI/Anthropic/DeepSeek/Ollama/HuggingFace까지 provider를 전환 가능.
- 인용 가능한 구절: (검색 결과 발췌)
  > "The ChatClient interface enables communication with AI models, allowing users to send prompts and receive structured responses."
  > "Spring AI supports models from various other providers like Anthropic, DeepSeek, and even local LLMs via Hugging Face or Ollama."
  > "Advisors are interceptors that handle requests and responses in AI applications… for establishing chat history, excluding sensitive words, or adding extra context to each request."
  > "Spring AI provides tools to wrap ChatModel's call using the Structured Output API to get output in the form of a data structure."
- 관련 섹션: 7장 "Java에서 LLM 호출하기" 중 "Advisor로 채팅 기록/필터 끼워넣기", "스트리밍 응답 받기" 박스 예제의 출발점. 공식 레퍼런스(자료 15)와 쌍으로 배치.

---

## 자료 17: Spring AI Integration Guide — Connect LLMs (OpenAI, Anthropic, Ollama) to Java Spring Boot

- 출처: https://medium.com/@parsairohit2/spring-ai-integration-guide-connect-llms-openai-anthropic-ollama-to-java-spring-boot-600eb12cc8d0
- 저자·날짜: Rohit Dutt · Medium, 2024 후반
- 신뢰성: 중 (저자 확인된 Medium 포스트, 실제 프로젝트 기반 예제)
- 핵심 주장: Spring AI는 공통 추상화 레이어 덕에 OpenAI/Anthropic/Ollama를 Maven 의존성 한 줄과 properties 변경만으로 스왑할 수 있다. 샘플 REST API를 단계별로 제공.
- 인용 가능한 구절:
  > "Spring AI provides a common abstraction layer for working with different AI providers using familiar Spring programming patterns, eliminating the need to explicitly use provider-specific SDKs."
  > "You can switch from OpenAI to Anthropic by simply changing your Maven dependency and updating the configuration, while your application code remains unchanged."
- 관련 섹션: 7장 "Python vs Java 비교" 박스에서 "Spring AI의 provider 추상화는 왜 유용한가"를 설명하는 보조 자료. 공식 문서(자료 15)와 병치.

---

## 자료 18: Andrej Karpathy — minbpe (BPE 토크나이저를 밑바닥부터 만들기)

- 출처: https://github.com/karpathy/minbpe  (강의 영상: "Let's build the GPT Tokenizer", 2024-02)
- 저자·날짜: Andrej Karpathy · 2024-02
- 신뢰성: 최상 (업계가 추천하는 BPE 내재화 교재)
- 핵심 주장: 실제 LLM에서 사용하는 Byte Pair Encoding 토크나이저를 최소 코드(수백 줄)로 재구현하며, BasicTokenizer / RegexTokenizer / GPT4Tokenizer 세 단계로 학습 곡선을 설계한다.
- 인용 가능한 구절: (공식 README 요지)
  > "Minimal, clean code for the Byte Pair Encoding (BPE) algorithm commonly used in LLM tokenization."
- 관련 섹션: 4장 "미니 언어 모델 만들기"의 토크나이저 실습 섹션. 자료 6(nanoGPT/Let's build GPT)과 짝지어 "토크나이저 → 모델 → 학습 → 생성" 순서를 따라가는 실습 축의 두 번째 기둥.

---

## 자료 19: Gemma 한국어 요약 모델 파인튜닝 빠르게 해보기 (SK DevOcean)

- 출처: https://devocean.sk.com/blog/techBoardDetail.do?ID=165703&boardType=techBlog
- 저자·날짜: SK DevOcean · 2024 (Gemma 공개 직후)
- 신뢰성: 최상 (SK 기술 블로그, 재현 가능한 코드 포함)
- 핵심 주장: Google Gemma 오픈 모델을 Colab/단일 GPU 환경에서 한국어 요약 태스크로 LoRA 파인튜닝하는 전 과정을 코드와 함께 제공. 오픈소스 모델의 국내 활용 사례.
- 인용 가능한 구절:
  > "Gemma 모델을 한국어 요약 학습 데이터로 파인 튜닝하는 방법을 설명하며, 파인 튜닝은 Google Colab에서 GPU 한계를 넘어서 진행할 수 있습니다."
- 관련 섹션: 6장 "오픈소스 모델 활용" 중 Gemma 파인튜닝 실습. 한국어 데이터로 실제 돌려본 국내 사례로 인용.

---

## 자료 20: GGUF 파일로 로컬에서 LLM 실행하기 (정우일 블로그)

- 출처: https://wooiljeong.github.io/ml/gguf-llm/
- 저자·날짜: 정우일 · 최근 (2024~2025, Llama3/Gemma2 시대 기준)
- 신뢰성: 중~최상 (저자 확인된 한국어 기술 블로그)
- 핵심 주장: Llama, Mistral, Gemma 같은 오픈소스 모델을 개인 노트북에서 실행하는 실용 경로로 GGUF 형식과 llama.cpp/Ollama를 소개. "API에 의존하지 않고 로컬에서 모델을 돌리는 것"이 교육적으로 중요하다고 주장.
- 인용 가능한 구절:
  > "오픈소스 모델을 로컬 환경에서 쉽고 빠르게 실행하려면, GGUF라는 파일 형식이 주로 사용됩니다."
- 관련 섹션: 6장 "오픈소스 모델 활용" 중 "로컬에서 돌려보기" 실습. Ollama 설치 → 모델 pull → 대화 흐름에서 보조 레퍼런스.

---

## 자료 21: Llama 3 파인튜닝 + HuggingFace 업로드 (unfinishedgod.netlify.app)

- 출처: https://unfinishedgod.netlify.app/2024/05/24/python/
- 저자·날짜: "미완성의신" 개인 기술 블로그 · 2024-05-24
- 신뢰성: 중 (개인 블로그지만 전체 코드·실행 결과 기록)
- 핵심 주장: Llama 3를 자기 데이터로 LoRA 파인튜닝하고 결과물을 HuggingFace Hub에 업로드하는 전 과정을 한국어 독자 관점에서 기록. `peft`/`trl`/`bitsandbytes` 조합의 실전 예.
- 인용 가능한 구절: (본문 서두 요지)
  > "Llama3를 파인튜닝을 통해 나만의 데이터로 학습 및 Huggingface에 적재해보자."
- 관련 섹션: 6장 "오픈소스 모델 활용" 중 Llama 계열 파인튜닝 섹션. 19번(Gemma)과 쌍으로 "같은 기법을 다른 모델 계열에 적용" 대조.

---

## 수집 한계

- 접근 실패한 자료:
  - `https://www.baeldung.com/spring-ai` — WebFetch 403. 그러나 검색 스니펫에서 핵심 문장을 확보해 자료 16에 인용 가능 수준으로 정리. 필요 시 본문 작성 단계에서 브라우저로 직접 재확인 권장.
  - `https://platform.openai.com/docs/quickstart` — WebFetch 403 (Cloudflare/인증 벽). 공식 SDK 사용법은 `github.com/openai/openai-quickstart-python`로 대체 확인 가능. OpenAI Python SDK 최소 예제(`from openai import OpenAI`, `client.chat.completions.create(...)` 패턴)는 공식 GitHub 예제에서 확보한 지식으로 충분.
- 의도적으로 제외한 소스 유형:
  - 나무위키, 위키백과 — 저자 불분명, 서문 밖 인용 부적합
  - 날짜 미표기 나열형 SEO 아티클("2026 Best LLM 10선" 류)
  - 학술 논문(Attention Is All You Need, InstructGPT, LLaMA 시리즈 등) — 다른 에이전트(논문 담당) 책임 영역
  - Reddit/HackerNews/Discord 같은 커뮤니티 스레드 — 다른 에이전트(커뮤니티 담당) 책임 영역
- 다양성 점검:
  - 동일 사이트 2건 초과 없음 (SK DevOcean 2건, jalammar.github.io 2건이 최대)
  - 한국어 자료: 9건 (자료 2, 10, 11, 12, 13, 15 한국어 인용부, 19, 20, 21) / 영어 자료: 12건 → 대략 한국어 45%, 영어 55%. 책 본문에서 자료 15(공식 Spring AI 문서)는 영어 원문이므로 한국어 비중이 목표(60%)보다 낮은 편. 필요 시 본문 집필 단계에서 한국어 블로그 1~2건 추가 보강 고려(예: "네이버 D2 search blog"는 직접 검색에서 안 잡혀 제외).
- 최신성:
  - 2024~2025 자료 비중 높음 (카카오페이 2025-09, HF LLM Course 2025 수시, Spring AI 1.x GA, Gemma/Llama3 시대 글). 고전 레퍼런스로는 Jay Alammar 2018, 2019 2건 포함.
