<!-- 검색 시점: 2026-06-10 기준 -->
# 웹 리서치: AI Agentic Coding의 4대 엔지니어링 (Prompt / Context / Harness / Loop)

> 수집 방법: WebSearch + WebFetch (1차 소스 우선). 빠르게 변하는 주제이므로 발행일·버전을 못 박았다. tech-book 신선도 규율 적용.

---

## 자료 1: Andrej Karpathy — "+1 for context engineering over prompt engineering" (X/Twitter)
- 출처: https://x.com/karpathy/status/1937902205765607626
- 저자·날짜: Andrej Karpathy, 2025-06-25 (Tobi Lütke 트윗 약 1주 후)
- 신뢰성: 최상 (1차 발언, 용어 대중화의 분수령)
- 핵심 주장: "prompt engineering"은 일상적으로 LLM에 주는 짧은 작업 설명을 연상시키지만, 산업용 LLM 앱에서는 "context engineering"이 더 정확한 표현이다. 컨텍스트 엔지니어링은 다음 단계에 딱 맞는 정보로 컨텍스트 윈도를 채우는 섬세한 기술이자 과학이다.
- 인용 가능한 구절: "context engineering is the delicate art and science of filling the context window with just the right information for the next step."
- 관련 섹션: 개념·정의(Context Engineering), 기원·대중화

## 자료 2: tobi lutke — "I really like the term context engineering" (X/Twitter)
- 출처: https://x.com/tobi/status/1935533422589399127
- 저자·날짜: Tobi Lütke (Shopify CEO), 2025-06-19 (조회 190만, 북마크 8,600 — Zep 블로그 보도)
- 신뢰성: 최상 (용어를 촉발한 1차 발언)
- 핵심 주장: "context engineering"이 "prompt engineering"보다 핵심 역량을 더 잘 설명한다 — LLM이 작업을 그럴듯하게 풀 수 있도록 모든 컨텍스트를 제공하는 기술.
- 인용 가능한 구절: "I really like the term 'context engineering' over prompt engineering. It describes the core skill better: the art of providing all the context for the task to be plausibly solvable by the LLM."
- 관련 섹션: 개념·정의(Context Engineering), 기원·대중화

## 자료 3: Anthropic — "Effective context engineering for AI agents"
- 출처: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 저자·날짜: Anthropic Engineering, 2025-09-29
- 신뢰성: 최상 (벤더 1차, 가장 권위 있는 정의)
- 핵심 주장: 컨텍스트 엔지니어링 = "LLM 추론 중에 최적의 토큰(정보) 집합을 큐레이션·유지하는 전략 집합"으로, 프롬프트 밖에 들어오는 모든 정보를 포함한다. 프롬프트 엔지니어링의 자연스러운 다음 단계. 에이전트 정의 = "LLMs autonomously using tools in a loop."
- 인용 가능한 구절:
  - "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."
  - "Context must be treated as a finite resource with diminishing marginal returns."
  - "Good context engineering means finding the smallest possible set of high-signal tokens that maximize desired outcome likelihood."
  - 에이전트: "LLMs autonomously using tools in a loop."
- 핵심 전략 4가지: Compaction(대화 이력 요약 후 재초기화), Structured Note-Taking(컨텍스트 밖 노트 영속화), Sub-Agent Architectures(전용 서브에이전트가 깨끗한 컨텍스트로 작업 후 요약 반환), Just-in-Time Context(경량 식별자 유지 + 런타임 동적 로드).
- context rot 언급: 토큰 수 증가 시 정보 회상 정확도 하락, 모든 모델이 attention budget 전반에서 이 저하를 보임.
- 관련 섹션: 개념·정의(Context Engineering), 실무 적용 팁, 용어 간 관계

## 자료 4: Anthropic — "Building Effective Agents"
- 출처: https://www.anthropic.com/research/building-effective-agents (Simon Willison 보도: https://simonwillison.net/2024/Dec/20/building-effective-agents/)
- 저자·날짜: Anthropic, 2024-12-19 (Simon Willison 2024-12-20 보도)
- 신뢰성: 최상 (벤더 1차, agentic 패턴의 표준 레퍼런스)
- 핵심 주장: Workflow(LLM·툴을 미리 정의된 코드 경로로 오케스트레이션) vs Agent(LLM이 자기 프로세스·툴 사용을 동적으로 지휘) 구분. 5가지 워크플로 패턴: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. "가장 단순한 해법을 먼저 찾고, 필요할 때만 복잡도를 올려라."
- 인용 가능한 구절: "Workflows are systems where LLMs and tools are orchestrated through predefined code paths... agents are systems where LLMs dynamically direct their own processes and tool usage."
- 관련 섹션: 개념·정의(Loop/Harness), 용어 간 관계, 논쟁점

## 자료 5: Geoffrey Huntley — "Ralph Wiggum as a software engineer"
- 출처: https://ghuntley.com/ralph/
- 저자·날짜: Geoffrey Huntley, 2025-07-14
- 신뢰성: 최상 (Ralph loop의 정전 1차 소스)
- 핵심 주장: Ralph = 같은 프롬프트를 신선한 컨텍스트로 반복 실행하는 결정론적 에이전틱 루프. 본질은 `while :; do cat PROMPT.md | claude-code ; done`. 파일시스템이 반복 간 영속 메모리, 루프당 한 작업이 핵심 제약, 서브에이전트가 병렬 처리.
- 인용 가능한 구절:
  - "That's the beauty of Ralph - the technique is deterministically bad in an undeterministic world."
  - "Cost of a $50k USD contract, delivered, MVP, tested + reviewed....$297 USD." (검증 필요 — 저자 자체 주장, 단일 사례)
  - "LLMs are surprisingly good at reasoning about what is important to implement."
- 도구: Claude Code(주), Amp, ripgrep, Rust(컴파일 백프레셔), LLVM(CURSED 프로젝트).
- 관련 섹션: 개념·정의(Loop Engineering), 대표 사례, 논쟁점(비용·신뢰성)

## 자료 6: Simon Willison — "Designing agentic loops"
- 출처: https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
- 저자·날짜: Simon Willison, 2025-09-30
- 신뢰성: 최상 (영향력 큰 실무자, agentic-engineering 태그 운영)
- 핵심 주장: 에이전틱 루프 = "목표 달성을 위해 툴을 루프로 실행." "Designing agentic loops"는 매우 새로운 스킬. YOLO 모드(모든 액션 자동 승인)는 위험하지만 생산성의 핵심. 안전 설계 3전략: 샌드박스, 외부 머신(GitHub Codespaces 권장), 위험 감수. 깨끗하게 통과하는 테스트 스위트가 에이전트 가치를 크게 증폭.
- 인용 가능한 구절:
  - "An AI agent is an LLM wrecking its environment in a loop." (Solomon Hykes 인용)
  - "The value you can get from coding agents... is massively amplified by a good, cleanly passing test suite."
- 관련 섹션: 개념·정의(Loop Engineering), 실무 적용 팁, 논쟁점(안전)

## 자료 7: LangChain (Harrison Chase) — "The rise of context engineering"
- 출처: https://blog.langchain.com/the-rise-of-context-engineering/
- 저자·날짜: Harrison Chase (LangChain CEO), 2025-06-23
- 신뢰성: 최상 (프레임워크 벤더 1차, Tobi/Karpathy 직후 정식화)
- 핵심 주장: 컨텍스트 엔지니어링 = "올바른 정보와 툴을, 올바른 형식으로, 동적으로 제공해 LLM이 작업을 그럴듯하게 해내게 만드는 시스템 구축." 에이전트가 신뢰성 없게 동작하는 대부분의 근본 원인은 적절한 컨텍스트·지침·툴이 모델에 전달되지 않았기 때문.
- 인용 가능한 구절: "Context engineering is building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task." (Tobi Lutke·Ankur Goyal·Walden Yan 의견 기반)
- 관련 섹션: 개념·정의(Context Engineering), 실무 적용 팁

## 자료 8: Hugging Face — "Harness, Scaffold, and the AI Agent Terms Worth Getting Right"
- 출처: https://huggingface.co/blog/agent-glossary
- 저자·날짜: Sergio Paniego, Aritra Roy Gosthipaty, 2026-05-25
- 신뢰성: 최상 (플랫폼 1차, 용어 구분 정의의 출처)
- 핵심 주장: Model(텍스트 in/out) / Scaffold(행동 정의층: 시스템 프롬프트·툴 설명·파싱·기억) / Harness(실행층: 모델 호출·툴콜 처리·중단 결정) / Agent = Model + Harness. Scaffold는 모델이 "무엇"을 보는가, Harness는 "어떻게" 실행하는가.
- 인용 가능한 구절:
  - "The execution layer inside the agent: it calls the model, handles its tool calls, decides when to stop." (harness)
  - "Agent = Model + Harness."
- 관련 섹션: 개념·정의(Harness Engineering), 용어 간 관계·구분 기준

## 자료 9: MindStudio — "What Is an Agent Harness? The Architecture Behind Claude Code, Codex, and Cursor"
- 출처: https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained
- 저자·날짜: MindStudio (2026, 정확 일자 미상 — 콘텐츠 마케팅, 신뢰성 중)
- 신뢰성: 중 (정리형, 1차 아님 — 정의는 HF 글로 교차검증됨)
- 핵심 주장: 에이전트 하네스 = 모델을 액션·툴 사용·컨텍스트 기억·에러 처리·다단계 목표 수행이 가능한 무언가로 바꾸는 시스템. "모델과 현실 세계 사이의 모든 것." Agent = Model + Harness. 9개 핵심 컴포넌트(컨텍스트 관리·툴 실행·메모리·에러 관리 등).
- 인용 가능한 구절: "An agent harness is everything between the language model and the real world. The harness decides what that text can touch."
- 관련 섹션: 개념·정의(Harness Engineering)

## 자료 10: MindStudio — "What Is Loop Engineering? The New Meta for AI Coding Agents"
- 출처: https://www.mindstudio.ai/blog/what-is-loop-engineering-ai-coding-agents
- 저자·날짜: MindStudio, 2026 (정확 일자 미상)
- 신뢰성: 중 (정리형 — Addy Osmani 출처는 별도 교차검증)
- 핵심 주장: Loop engineering = AI 에이전트를 직접 매 프롬프트 타이핑하는 대신, 스케줄에 따라 프롬프트하는 시스템을 설계하는 실천. 무엇을·언제 프롬프트하고 결과가 수용 가능한지 결정하는 자율 시스템을 최적화. "act, observe, reason, repeat." 6월 2026 Addy Osmani가 Peter Steinberger·Anthropic Boris Cherny의 논점 위에서 대중화.
- 인용 가능한 구절: "Loop engineering optimizes the autonomous system that decides what to prompt, when to prompt it, and whether the result is acceptable."
- 관련 섹션: 개념·정의(Loop Engineering), 기원·대중화

## 자료 11: OpenAI — "Custom instructions with AGENTS.md" (Codex 공식 문서)
- 출처: https://developers.openai.com/codex/guides/agents-md / 표준: https://agents.md/
- 저자·날짜: OpenAI Developers, 2026 기준 (지속 갱신 문서)
- 신뢰성: 최상 (벤더 1차 문서)
- 핵심 주장: AGENTS.md = 표준 Markdown. AI 코딩 에이전트에게 컨텍스트·지침(빌드 단계·테스트·컨벤션)을 주는 전용·예측 가능한 장소. README는 사람용, AGENTS.md는 에이전트용. Codex는 작업 전 AGENTS.md를 읽어 instruction chain을 구성(글로벌 → 프로젝트 루트 → cwd 하향 탐색, AGENTS.override.md 우선).
- 인용 가능한 구절: "AGENTS.md is a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project."
- 관련 섹션: 대표 사례(도구 생태계), 실무 적용 팁

## 자료 12: Google — "Provide context with GEMINI.md files" (Gemini CLI 공식 문서)
- 출처: https://geminicli.com/docs/cli/gemini-md/ / GitHub: https://github.com/google-gemini/gemini-cli
- 저자·날짜: Google Gemini, 2025 출시 후 지속 갱신 (Apache 2.0 오픈소스)
- 신뢰성: 최상 (벤더 1차 문서)
- 핵심 주장: GEMINI.md = 영속 컨텍스트 파일. 프로젝트별 지침·페르소나·코딩 스타일 정의. CLI가 여러 위치(~/.gemini/GEMINI.md 글로벌, 워크스페이스·상위 디렉토리)에서 파일을 찾아 연결(concatenate)해 매 프롬프트와 함께 모델에 전송. 계층적 컨텍스트 시스템.
- 인용 가능한 구절: "Context files, which use the default name GEMINI.md, are a powerful feature for providing instructional context to the Gemini model."
- 관련 섹션: 대표 사례(도구 생태계)

## 자료 13: Princeton — SWE-agent 공식 페이지 / GitHub
- 출처: https://github.com/SWE-agent/SWE-agent (논문: https://arxiv.org/abs/2405.15793)
- 저자·날짜: Princeton NLP, NeurIPS 2024 (arXiv 2024-05)
- 신뢰성: 최상 (학술 1차 + 오픈소스 구현)
- 핵심 주장: GitHub 이슈를 받아 자동으로 고치는 에이전트. Agent-Computer Interface(ACI)가 핵심 기여. 하네스 엔지니어링의 학술적 뿌리.
- 인용 가능한 구절: "SWE-agent takes a GitHub issue and tries to automatically fix it, using your LM of choice."
- 관련 섹션: 대표 사례(Harness), 기원, 학술

## 자료 14: 패스트캠퍼스 — "전현준의 하네스 엔지니어링: Claude Code · Codex 완벽 가이드"
- 출처: https://fastcampus.co.kr/data_online_harness
- 저자·날짜: 패스트캠퍼스 (2026 기준 강좌)
- 신뢰성: 중 (교육 상품 — "harness engineering" 한국어 대중화 사례로서 가치)
- 핵심 주장: "모델을 코드베이스·터미널·CI에 연결하는 런타임 — 컨텍스트를 어떻게 모으고, 툴을 어떻게 호출하고, 변경을 어떻게 적용하고, 안전장치를 어디에 두는가." "나만의 하네스를 설계하는 방법" — 한국 현업 대상 하네스 엔지니어링 교육이 이미 상품화됨.
- 인용 가능한 구절: "AI 시대에는 단순히 코드를 많이 작성하는 것이 아니라 AI 에이전트가 제대로 일하도록 환경을 설계하는 개발 방식이 중요해지고 있으며..."
- 관련 섹션: 실무 적용 팁(한국), 기원·대중화(하네스)

## 자료 15: Aider (Paul Gauthier) — GitHub / 공식
- 출처: https://github.com/Aider-AI/aider
- 저자·날짜: Paul Gauthier, 첫 릴리스 2023, 최신 커밋 2026-03-03 기준 (GitHub 41.6k stars / 2026-03 기준)
- 신뢰성: 최상 (오픈소스 1차)
- 핵심 주장: 터미널 기반 AI 페어 프로그래밍. 로컬 git 리포에서 코드 편집, 변경 자동 커밋. repository map(함수 시그니처·파일 구조)으로 전체 코드베이스 컨텍스트 제공. Claude·GPT-4o·DeepSeek 등 거의 모든 LLM 연결.
- 인용 가능한 구절: "aider is AI pair programming in your terminal."
- 관련 섹션: 대표 사례(도구 생태계 — 모델 무관 하네스)

## 수집 한계
- X(Twitter) 트윗 본문은 검색 결과의 인용 구절로 확보(직접 페이지 렌더 제한). 날짜·문구는 다중 2차 소스(Zep, LangChain, learnprompting 등)로 교차검증함.
- "loop engineering" 용어의 Addy Osmani/Peter Steinberger/Boris Cherny 귀속은 MindStudio 정리글 1건 기반 — 1차 출처(Osmani 원문)는 미확보, 커뮤니티 트랙에서 보강 권장.
