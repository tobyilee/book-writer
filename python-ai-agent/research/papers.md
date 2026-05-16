# 논문 리서치 — Python AI Agent

> 수집 시점: 2026-05-16. arXiv·ACL·Semantic Scholar 인덱스를 통해 메타데이터 확인된 항목 중심.

## A. 추론·도구·행동 통합 (Tool Use 기반 골격)

### ReAct: Synergizing Reasoning and Acting in Language Models
- 저자: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- arXiv: [2210.03629](https://arxiv.org/abs/2210.03629) (2022-10 최초 제출, ICLR 2023)
- 핵심 기여: reasoning trace와 action을 interleave해 LLM이 계획을 추적·갱신하고 외부 환경과 상호작용.
- 수치: HotpotQA·Fever에서 hallucination·error propagation 완화. ALFWorld +34%p, WebShop +10%p (imitation·RL 대비 절대 성공률 향상, 단 1~2개 in-context example).
- 책 활용: Part 1의 ReAct 직접 구현 챕터의 이론적 토대. "Thought / Action / Observation" 토큰 인터리브 프롬프트가 그대로 인용 가능.

### Toolformer: Language Models Can Teach Themselves to Use Tools
- Schick et al., Meta AI. arXiv 2302.04761.
- 기여: 자기-감독 방식으로 도구 호출을 학습 데이터에 삽입.
- 책 활용: "왜 모델이 도구를 부르는가"의 학습 관점 곁가지. 본문은 API 호출 측면만 짚으면 됨.

### MRKL Systems
- Karpas et al. (AI21), 2022. arXiv 2205.00445.
- 기여: LLM + 외부 지식 소스/이산 추론을 결합한 모듈러 neuro-symbolic 아키텍처. function calling 사고의 선조.

## B. 자기 성찰·반복 개선

### Reflexion: Language Agents with Verbal Reinforcement Learning
- Noah Shinn 외. arXiv [2303.11366](https://arxiv.org/abs/2303.11366).
- 기여: 외부 보상 대신 "언어적 자기 피드백"을 episodic memory에 저장 → 다음 시도 개선.
- 수치: HumanEval pass@1 91% (당시 SOTA GPT-4 80% 초과).
- 책 활용: Part 1의 에러 처리·재시도·자기 비평 챕터. 메모리 챕터와도 연결.

## C. 계획·탐색

### Tree of Thoughts (ToT)
- Yao 외. arXiv [2305.10601](https://arxiv.org/abs/2305.10601) (NeurIPS 2023).
- 기여: thought 단위 트리 탐색 + self-evaluation으로 deliberate decision making.
- 수치: Game of 24에서 GPT-4 CoT 4% → ToT 74%.
- 코드: [princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm).
- 책 활용: "단순 CoT의 한계와 탐색형 reasoning" 챕터의 정량 근거.

### Plan-and-Solve Prompting
- Wang 외. arXiv [2305.04091](https://arxiv.org/abs/2305.04091) (ACL 2023).
- 기여: zero-shot CoT의 missing-step 오류 보완을 위해 (1) plan을 먼저 만들고 (2) plan을 따라 실행.
- 책 활용: Plan-and-Execute 패턴 직접 구현 챕터.

### Language Agent Tree Search (LATS)
- arXiv 2310.04406. ReAct + Tree Search 통합.
- 책 활용: ToT/ReAct를 책에서 다룬 뒤 "다음 단계" 포인터로 짧게 언급.

## D. 외부 세계 학습 (예시: 임바디드)

### Voyager: An Open-Ended Embodied Agent with Large Language Models
- Wang 외. arXiv [2305.16291](https://arxiv.org/abs/2305.16291).
- 기여: Minecraft 환경에서 자동 커리큘럼 + skill library + iterative prompting으로 lifelong learning.
- 책 활용: "스킬 라이브러리"라는 메타 패턴(과거 성공 경로를 재사용 가능한 함수로 저장) 소개에 한 페이지.

## E. 멀티 에이전트

### AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
- Wu 외, Microsoft. arXiv [2308.08155](https://arxiv.org/abs/2308.08155) (ICLR 2024 Workshop).
- 기여: 대화 단위 멀티 에이전트 프레임워크. nested chat, group chat 등 유연한 토폴로지.
- 책 활용: LangGraph 멀티 에이전트 챕터에서 "AutoGen은 동일한 문제를 conversation 추상으로 접근, LangGraph는 graph 추상으로 접근" 대비.

### MetaGPT: Meta Programming for Multi-Agent Collaborative Framework
- Hong 외. arXiv 2308.00352.
- 기여: SOP(표준 운영 절차) 기반 소프트웨어 엔지니어링 에이전트.

### ChatDev
- Qian 외. arXiv 2307.07924 + IBM 개요 [What is ChatDev?](https://www.ibm.com/think/topics/chatdev).
- 기여: 가상 소프트웨어 회사 시뮬레이션.

### CAMEL: Communicative Agents for "Mind" Exploration of Large Scale Language Model Society
- Li 외. arXiv 2303.17760.
- 기여: role-playing 기반 2~3 에이전트 협력. Inception prompting.

> Multi-agent 비교: MetaGPT/ChatDev는 chain/SOP 같은 정해진 구조, AutoGen은 nested/group으로 더 유연, CAMEL은 role-play 2~3개 — 책에서 "LangGraph 이전 멀티 에이전트 시도들" 절에 비교표로 정리하면 좋다.

## F. 도구 사용 벤치마크

### ToolBench
- arXiv 2307.16789, [GitHub OpenBMB/ToolBench](https://github.com/OpenBMB/ToolBench) (ICLR'24 spotlight).
- 규모: 16,000+ API, 3,451 tools. DFSDT 기반 solution path. ToolEval(LLM-based 채점).
- 다른 사용 사례: [sambanova/toolbench](https://github.com/sambanova/toolbench) 평가 스위트.

### API-Bank
- Li 외. arXiv [2304.08244](https://arxiv.org/abs/2304.08244) (EMNLP 2023).
- 규모: 73 도구, 314 dialog, 753 API call. 1,888 dialog × 2,138 API train set.
- 책 활용: "도구 호출 평가" 챕터의 정량 비교 자료.

## G. Agentic RAG 및 최신 동향

### Agentic Retrieval-Augmented Generation: A Survey
- Singh 외. arXiv [2501.09136](https://arxiv.org/abs/2501.09136).
- 기여: Agentic RAG taxonomy — reflection·planning·tool use·multi-agent collab을 RAG 파이프라인에 내장. Agentic Document Workflows(ADW) 개념 제시.
- 책 활용: LangGraph 챕터에서 "RAG + 상태 기반 에이전트"의 학술 backbone.

### Memory in the Age of AI Agents: A Survey
- 2026-03 arXiv [2603.07670](https://arxiv.org/html/2603.07670v1). 자율 LLM 에이전트의 메모리 메커니즘·평가 정리.
- 책 활용: Part 1 메모리 챕터의 분류 기준(short-term / long-term / episodic / semantic) 출처.

### Agentic AI: Architectures, Taxonomies, and Applications
- arXiv [2601.12560](https://arxiv.org/pdf/2601.12560). 2026년 시점 종합 분류.

### Towards Agentic RAG with Deep Reasoning
- arXiv [2507.09477](https://arxiv.org/abs/2507.09477). RAG + reasoning 결합.

### From Language to Action: A Review of LLMs as Autonomous Agents and Tool Users
- arXiv 2508.17281. 도구 사용 관점 리뷰.

## H. 책에 인용할 만한 핵심 수치 (즉시 사용 가능)

| 주장 | 수치 | 출처 |
|---|---|---|
| ReAct가 ALFWorld에서 imitation/RL 대비 절대 성공률 향상 | +34%p | Yao et al. 2022 |
| ReAct WebShop 성공률 향상 | +10%p | Yao et al. 2022 |
| Reflexion HumanEval pass@1 | 91% (GPT-4 80%) | Shinn et al. 2023 |
| ToT Game of 24 성공률 | 4% (CoT) → 74% (ToT) | Yao et al. 2023 |
| ToolBench 규모 | 16k+ API, 3,451 tools | Qin et al. 2023 |
| API-Bank | 73 도구, 753 API call | Li et al. 2023 |
| 함수 호출 토큰 오버헤드 | ~346 토큰/호출 | TokenMix 2026 가이드 |
| 함수 호출 정확도 | 97–99% | TokenMix 2026 가이드 |

## I. 책 챕터 매핑

- Part 1 ReAct 구현 → ReAct 원논문 (필수 인용)
- Part 1 reasoning loop → Plan-and-Solve, Reflexion
- Part 1 메모리 → "Memory in the Age of AI Agents" 서베이
- Part 1 도구 사용 → MRKL, Toolformer
- Part 2 LangChain의 한계 → (학술 자료보다 블로그/커뮤니티가 적합 — 웹 리서치 참조)
- Part 3 멀티 에이전트 → AutoGen, MetaGPT, ChatDev, CAMEL
- Part 3 평가 → ToolBench, API-Bank
- 전 영역 trend → Agentic RAG Survey 2025, Memory Survey 2026
