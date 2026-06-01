# 논문 리서치 — 프롬프트 기법·LLM 평가 학술 근거

> 검색 시점: 2026-06-01. arXiv/NeurIPS 1차 식별자 확인.

## 1. 프롬프트 기법 원논문

### In-context / few-shot learning
- **Brown et al. (2020), "Language Models are Few-Shot Learners" (GPT-3)** — arXiv:2005.14165, NeurIPS 2020. 175B 파라미터. gradient 업데이트 없이 텍스트만으로 task+few-shot 데모 제공하는 **in-context learning** 개념의 출발점. 프롬프트 안의 예시가 곧 학습 신호라는 패러다임 정립.

### Chain-of-Thought (CoT)
- **Wei et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"** — arXiv:2201.11903, NeurIPS 2022. few-shot 예시에 추론 단계(중간 reasoning)를 넣으면 복잡 과제 성능이 크게 향상. 산술·상식·기호 추론에서 큰 폭 개선. "Let's think step by step"류 reasoning 유도의 학술 근거.

### Self-Consistency
- **Wang et al. (2022), "Self-Consistency Improves Chain of Thought Reasoning in Language Models"** — arXiv:2203.11171. greedy decoding 대신 여러 reasoning path를 샘플링→다수결로 최종 답 선택. CoT를 개선. eval/앙상블 관점에서 중요.

### ReAct (Reasoning + Acting)
- **Yao et al. (2022), "ReAct: Synergizing Reasoning and Acting in Language Models"** — arXiv:2210.03629. 추론 trace와 task action을 교차 생성. HotpotQA·Fever에서 hallucination·오류 전파 완화(Wikipedia API 연동). ALFWorld·WebShop에서 imitation/RL 대비 +34%/+10%. 1–2개 in-context 예시만으로. **에이전트형 프롬프트(코딩 에이전트 포함)의 이론적 뿌리.**

### Tree of Thoughts (ToT)
- **Yao et al. (2023), "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"** — arXiv:2305.10601. 여러 reasoning 경로를 트리로 탐색·백트래킹. 복잡 탐색·계획 과제에서 단일 CoT 능가.

## 2. LLM 평가 방법론 논문

### LLM-as-a-Judge (핵심)
- **Zheng et al. (2023), "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"** — arXiv:2306.05685, NeurIPS 2023 Datasets&Benchmarks. 강한 LLM judge(GPT-4)가 인간 선호와 **80%+ 일치**(인간끼리 일치 수준과 동급). 동시에 **편향 식별**: position bias(위치), verbosity bias(길수록 선호), self-enhancement bias(자기 모델 선호), 제한된 추론 능력. 완화책 제안. **LLM-as-judge의 신뢰성과 한계를 동시에 보여주는 정전 논문.**

### LLM-as-Judge 신뢰성 후속 (보조)
- "Can You Trust LLM Judgments? Reliability of LLM-as-a-Judge" — arXiv:2412.12509. judge 신뢰성 정량 평가.
- "The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge" — arXiv:2509.26072. judge가 인지하지 못한 shortcut 편향. (보조 — 본문 비중 조절)

## 3. 종합·서베이

- **Schulhoff et al. (2024/2025), "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques"** — arXiv:2406.06608 (최신판 2025-02-26). PRISMA 기반 머신지원 체계적 리뷰. **용어 33개, 텍스트 프롬프팅 기법 58개 분류, 타 모달리티 40개.** agents(브라우징·계산기 등 외부 도구 결합 프롬프팅)까지 포함. 책의 기법 분류 체계 백본으로 적합.
- **Sahoo et al. (2024/2025), "A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications"** — arXiv:2402.07927 (최신판 2025-03-16). 응용 영역별 29+ 기법 분류, 방법론·모델·데이터셋 요약.

## 4. 본문 활용 매핑
- "기법은 마법이 아니라 검증된 연구의 산물" — CoT(2201.11903)·few-shot(2005.14165)·self-consistency(2203.11171)·ReAct(2210.03629)·ToT(2305.10601)로 각 기법의 출처 명시.
- eval 챕터의 LLM-as-judge 신뢰성/편향 논의 → Zheng 2306.05685를 1차 근거로, position/verbosity/self-enhancement 편향을 반드시 경고.
- 기법 전수·분류는 The Prompt Report(2406.06608)를 권위 출처로.

## 5. 리서치 한계 (논문)
- 세 **특정 모델(Opus 4.8/GPT-5.5/Gemini 3.5 Flash) 자체에 대한 동료심사 논문은 없음**(상용 모델 — 공식 문서/시스템카드가 1차). 학술 근거는 *기법*과 *평가 방법론* 일반에 적용.
- effort/thinking_level 같은 신규 제어 파라미터의 학술 평가는 아직 빈약 — 공식 문서 의존.

## 참고문헌 (arXiv ID)
- Brown 2020, arXiv:2005.14165
- Wei 2022, arXiv:2201.11903
- Wang 2022, arXiv:2203.11171
- Yao 2022 (ReAct), arXiv:2210.03629
- Yao 2023 (ToT), arXiv:2305.10601
- Zheng 2023, arXiv:2306.05685
- Schulhoff 2024/25 (Prompt Report), arXiv:2406.06608
- Sahoo 2024/25 (survey), arXiv:2402.07927
- (보조) arXiv:2412.12509, arXiv:2509.26072
