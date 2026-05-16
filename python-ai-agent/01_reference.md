# Python AI Agent (맨땅 → LangChain → LangGraph) 종합 레퍼런스

> 작성: 2026-05-16 / 책 슬러그: `python-ai-agent`
> 근거 산출물: `research/web.md`, `research/papers.md`, `research/community.md`
> 대상 독자: Python을 알고 LLM 기초(프롬프트 엔지니어링·API 호출)는 있으나, 에이전트를 만들어본 적 없는 개발자.

---

## 1. 개요 — 왜 지금 이 책인가 (2026년 시점)

2022년 가을의 ReAct 논문 이래 ~3년 반 동안 "LLM이 도구를 부른다"는 발상은 학술 호기심에서 **일상 도구**로 옮겨왔다. 2026년 5월 기준 코딩 일선에서 가장 친숙한 에이전트가 Claude Code, Cursor, Devin이라는 사실이 그 증거다. 그러나 이 변화는 모두에게 매끄럽지 않다. 입문자는 두 갈래의 문에 동시에 부딪힌다.

1. **개념의 안개** — "에이전트"라는 단어는 사람마다 다른 뜻으로 쓰인다. Simon Willison은 2025년에야 "이 단어가 합의된 정의를 가질 수 있게 된 것 같다"고 썼다([substack](https://simonw.substack.com/p/i-think-agent-may-finally-have-a)).
2. **프레임워크 선택의 안개** — LangChain은 가장 많이 쓰이는 동시에 가장 많이 욕먹는다. LangGraph는 "그래도 상태가 있는 시스템엔 이게 답"이라는 평과 "Redis와 묶었더니 brittle"이라는 후일담이 공존한다([Temporal/Grid Dynamics](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics)).

이 책의 위치는 분명하다. **추상 레이어를 거꾸로 한 번 벗겨본 뒤 다시 입혀본다.** 맨땅에서 OpenAI/Anthropic SDK만 가지고 ReAct 루프를 직접 짠 사람만이 LangChain의 `Runnable`이 어떤 보일러플레이트를 대신해 주는지 진짜로 안다. 그리고 LangGraph가 왜 "DAG가 아니라 그래프"여야 했는지는, 사이클이 필요한 상황을 직접 만나본 사람만 체감한다.

2026년의 또 다른 사실은, 가장 잘 돌아가는 에이전트(Claude Code, Cursor)도 결국 **단순 루프 + 좋은 도구 + 좋은 컨텍스트 엔지니어링**이라는 것이다([Mindstudio](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead)). 화려한 그래프가 아니다. 이 책은 그래서 화려함이 아닌 **본질에서 시작해 필요한 만큼만 추상화하는 길**을 선택한다.

---

## 2. 핵심 개념 정의

각 정의 옆에 대표 출처를 단다. 책 본문 인용은 이 표를 1차 근거로 삼는다.

| 용어 | 정의 | 대표 출처 |
|---|---|---|
| **Tool use (Function calling)** | LLM이 외부 도구의 호출을 요청하고, 그 결과를 자신의 다음 토큰 생성에 사용하는 패턴. 동일 개념의 두 이름. | [OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling) · [Anthropic Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · [Simon Willison llm-tool-use](https://simonwillison.net/tags/llm-tool-use/) |
| **Agent (좁은 정의)** | "LLM이 자신의 프로세스와 도구 사용을 동적으로 지시하며, 작업 수행 방식의 통제권을 모델이 쥐는 시스템." Anthropic의 정의. | [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) |
| **Workflow** | LLM과 도구가 **사전에 정해진 코드 경로**로 조율되는 시스템. 자율성이 낮은 쪽 끝. | [Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) |
| **ReAct** | reasoning trace와 action을 interleave해 생성하는 프롬프트 패턴(Thought → Action → Observation 반복). | [Yao et al. 2022, arXiv:2210.03629](https://arxiv.org/abs/2210.03629) |
| **Plan-and-Solve** | 먼저 plan을 만들고, plan을 따라 subtask를 수행하는 prompting. Zero-shot CoT의 missing-step 오류 보완. | [Wang et al. 2023, arXiv:2305.04091](https://arxiv.org/abs/2305.04091) |
| **Reflexion** | 외부 보상 대신 **언어적 자기 피드백**을 episodic memory에 저장해 다음 시도를 개선. | [Shinn et al. 2023, arXiv:2303.11366](https://arxiv.org/abs/2303.11366) |
| **Tree of Thoughts (ToT)** | thought 단위 트리 탐색 + self-evaluation으로 deliberate decision making. | [Yao et al. 2023, arXiv:2305.10601](https://arxiv.org/abs/2305.10601) |
| **Memory (에이전트 관점)** | short-term(컨텍스트 윈도우 내) / long-term(persisted) / episodic(과거 trial의 자기 메모) / semantic(지식)의 4축. | [Memory in the Age of AI Agents (2026-03 survey)](https://arxiv.org/html/2603.07670v1) |
| **Runnable (LangChain)** | LCEL의 추상 연산 단위. `.invoke()`, `.batch()`, `.stream()`, `.ainvoke()` 공통 인터페이스. `__or__()` 오버로딩으로 `prompt \| llm \| parser` 합성. | [LangChain LCEL 공식](https://python.langchain.com/docs/concepts/lcel/) |
| **LCEL** | LangChain Expression Language. 0.3 이후 LangChain의 권장 합성 방식. 스트리밍·배치·async·병렬을 자동 처리. | [LangChain LCEL 공식](https://python.langchain.com/docs/concepts/lcel/) |
| **StateGraph (LangGraph)** | TypedDict 상태 + 노드(함수) + 엣지(라우팅)로 정의되는 **사이클 가능한** 그래프. 체크포인터·스토어로 메모리 부착. | [LangGraph 공식](https://docs.langchain.com/oss/python/langgraph/workflows-agents) |
| **Supervisor pattern** | 중앙 supervisor 노드가 LLM 추론으로 worker 노드에 작업을 위임하고, 결과를 모아 다음 단계를 결정. 라우팅 로직은 코드, 의사결정은 LLM. | [langgraph-supervisor 문서](https://reference.langchain.com/python/langgraph/supervisor/) |
| **Agentic RAG** | reflection·planning·tool use·multi-agent collab을 RAG 파이프라인에 내장해 동적으로 retrieval 전략을 운용하는 패러다임. | [Agentic RAG Survey arXiv:2501.09136](https://arxiv.org/abs/2501.09136) |

> 다섯 가지 워크플로 패턴(Anthropic 분류)은 책 전반에 반복 등장하므로 함께 못 박는다: **prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer**.

---

## 3. From-scratch 영역 — Part 1을 위한 자료

### 3.1 SDK 직접 사용 시 골격

OpenAI와 Anthropic은 표면 차이가 있어도, 에이전트 루프 관점에선 **같은 추상**을 노출한다.

- 공통 루프(Anthropic의 단순 서술): `model reasons → tool runs → result appended as user turn → model reasons again`([How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)).
- 한 응답에 `tool_calls`가 0개·1개·여러 개일 수 있고, 각각 `id`·`name`·JSON-encoded `arguments`를 가진다 → **항상 배열로 가정하고 처리**([OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling)).
- 두 가지 실행 모드:
  - Server-executed (Anthropic web_search·code execution 등): 한 번 요청에 여러 도구가 서버 측에서 자동 실행됨.
  - Client-executed: 매 호출이 round-trip. 책 Part 1은 이쪽을 직접 구현한다.

### 3.2 도구 설계 원칙 (2026 기준 공식 권고)

- "Intern Test" — 인턴이 도구 설명만 보고도 올바르게 쓸 수 있어야 한다.
- 파라미터 최소화 — 코드로 알 수 있는 값(예: `order_id`)을 LLM에게 채우게 하지 마라.
- enum과 객체 스키마로 invalid state를 표현 불가능하게 만들어라.
- 함수 호출은 호출당 평균 **~346 토큰** 오버헤드, 정확도 **97–99%**, 도구 한계 **128개**(OpenAI 기준)이다([TokenMix 2026 비교 가이드](https://tokenmix.ai/blog/function-calling-guide)).
- Anthropic 측 도구 작성 가이드는 별도 페이지로 정리되어 있다([Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).

### 3.3 ReAct 패턴 — 직접 구현 자료

- 원논문: [arXiv:2210.03629](https://arxiv.org/abs/2210.03629). **HotpotQA·Fever에서 hallucination·error propagation 완화. ALFWorld +34%p, WebShop +10%p**(절대 성공률, imitation/RL 대비, in-context example 1~2개만 사용).
- From-scratch 구현 레퍼런스:
  - [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation) — Simon Willison 스타일 미니멀 구현.
  - [KansSoftware/simple-re-act-agent-from-scratch](https://github.com/KansSoftware/simple-re-act-agent-from-scratch) — Thought/Action/Observation 루프.
  - [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch) — function calling·memory·ReAct를 black-box 없이 단계별.
  - [Tadeo Donegana — ReAct Agent framework by scratch](https://tadeodonegana.com/posts/react-agent-framework-by-scratch-python/).
  - [shafiqulai blog — Create ReAct AI Agent from Scratch using Python Without any Framework](https://shafiqulai.github.io/blogs/blog_3.html).

### 3.4 Reasoning loop의 확장 — 책에서 어디까지 다룰까

- **Plan-and-Solve** ([arXiv:2305.04091](https://arxiv.org/abs/2305.04091)) — 단순 CoT의 missing-step 오류를 보완. 책 Part 1 후반.
- **Reflexion** ([arXiv:2303.11366](https://arxiv.org/abs/2303.11366)) — verbal self-reflection을 episodic memory에 저장. HumanEval pass@1 **91%**(GPT-4 baseline 80%).
- **Tree of Thoughts** ([arXiv:2305.10601](https://arxiv.org/abs/2305.10601)) — Game of 24에서 CoT **4%** → ToT **74%**. "단순 CoT가 안 되는 영역" 정량 근거.
- **Voyager** ([arXiv:2305.16291](https://arxiv.org/abs/2305.16291)) — skill library 메타 패턴(과거 성공 경로를 재사용 가능한 함수로 누적). 책에서 한 페이지로 충분.

### 3.5 메모리

- 분류: short-term / long-term / episodic / semantic. 출처: [Memory in the Age of AI Agents survey](https://arxiv.org/html/2603.07670v1).
- From-scratch에서 다룰 것: conversation history를 유한 윈도우로 자르기, summary buffer, 외부 저장소로의 spillover, episodic memory(Reflexion 스타일).

### 3.6 흔한 함정 (Part 1 챕터 후반 또는 도입 anecdote로)

- **무한 루프** — 종료 조건 없는 reasoning loop. 실제 보고: 15분에 60+ 스텝, $0.08짜리가 $12로. 4시간 검출 지연 시 누적 **$2,847**, 토큰 1회 500 → 15회 4M([Medium — LLM Tool-Calling in Production](https://medium.com/@komalbaparmar007/llm-tool-calling-in-production-rate-limits-retries-and-the-infinite-loop-failure-mode-you-must-2a1e2a1e84c8), [The Stochastic Tax — DEV](https://dev.to/piyooshrai/the-stochastic-tax-why-your-ai-agent-is-a-financial-liability-and-how-to-fix-it-jgc), [agentpatterns.tech — Infinite Loop](https://www.agentpatterns.tech/en/failures/infinite-loop)).
- **환각 tool name·malformed JSON** — 대부분 프레임워크가 crash 또는 silently 통과. 직접 짤 때만 보인다.
- **context overflow** — history 무한 누적.
- **재시도 미설계** — exponential backoff·idempotency 없이 retry 돌리면 비용 폭주.
- 권고: iteration 캡, 토큰 캡, 시간 캡, 비용 캡(하드 캡 4종 세트).

---

## 4. LangChain 영역 — Part 2를 위한 자료

### 4.1 무엇을 추상화하는가

LangChain이 대신해 주는 것은 크게 네 가지다.

1. **공통 인터페이스** — 서로 다른 LLM·임베딩·벡터스토어·도구를 동일한 `Runnable` 인터페이스로 통일.
2. **합성** — `prompt | llm | parser`의 LCEL 파이프 합성. 스트리밍·배치·async·병렬을 자동 처리.
3. **통합** — 수백 개의 통합(integration) 모듈(벡터 DB, 로더, retriever, callback).
4. **관찰성** — LangSmith trace로 매 단계의 입출력 가시화.

근거: [LangChain LCEL 공식 개념 페이지](https://python.langchain.com/docs/concepts/lcel/), [Pinecone — LCEL Explained](https://www.pinecone.io/learn/series/langchain/langchain-expression-language/), [Medium Part 8 — Runnables](https://medium.com/@abhishekjainindore24/langchain-part-8-runnables-2d72b58ff3a5), [Medium Feb 2026 — Production-Ready Pipelines with Runnables](https://medium.com/@sajo02/building-production-ready-ai-pipelines-with-langchain-runnables-a-complete-lcel-guide-2f9b27f6d557).

### 4.2 코드 패턴 (책에서 인용할 골격)

- `prompt | llm | StrOutputParser()` — 가장 단순한 LCEL.
- `RunnableParallel`, `RunnablePassthrough` — 병렬·분기.
- `with_retry()`, `with_fallbacks()` — 내장 회복력.
- Tool 정의 → `@tool` 데코레이터 또는 `BaseTool` 상속 → Agent Executor에 묶기.
- 메모리: `ConversationBufferMemory` 류는 deprecated 흐름, LangGraph + checkpointer로 이동 권장.
- RAG: `Retriever` → `Document` → `Chain`의 표준 파이프라인.

### 4.3 LangChain 비판 — 책에서 균형 잡기

비판은 3개 이상 소스에서 반복되는 항목만 추린다([Designveloper](https://www.designveloper.com/blog/is-langchain-bad/), [Woyera](https://medium.com/@woyera/6-reasons-why-langchain-sucks-b6c99c98efbe), [Shashank Guda](https://shashankguda.medium.com/challenges-criticisms-of-langchain-b26afcef94e7), [safjan](https://safjan.com/problems-with-Langchain-and-how-to-minimize-their-impact/), [TechTide](https://techtidesolutions.com/blog/is-langchain-bad/), [Latenode community](https://community.latenode.com/t/whats-behind-the-negative-sentiment-towards-langchain-in-the-developer-community-and-corporate-environments/39043)).

1. **추상화 과잉** — OpenAI 한 줄 호출이 클래스 3개를 거친다.
2. **breaking changes** — minor 버전 간 API 깨짐, 튜토리얼 빠르게 무효화.
3. **문서 vs 실제 불일치** — 예제가 그대로 안 돈다.
4. **로깅·디버깅 부재** — 어떤 프롬프트가 실제로 나갔는지 추적 어려움(LangSmith로 해결).
5. **숨은 비용** — 기본 retry·fallback이 토큰 더 씀.
6. **production-grade error handling 없음** — try/catch·재시도 직접 작성.

옹호 의견([Hamel Husain tweet](https://x.com/HamelHusain/status/1755406853566247242), [hamel.dev — Why Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/), [Humanloop 인터뷰](https://humanloop.com/blog/why-your-product-needs-evals)):

> "처음엔 LC에 짜증냈다. 그런데 업계 사람들과 일해 보니 다들 langchain을 쓰고 있더라. 시간이 지나 이유를 알게 됐다 — 그들은 사용자에게 광적으로 귀를 기울인다." — Hamel Husain (요지 의역)

핵심 nuance: Hamel은 LangChain 본체가 아니어도 **LangSmith 단독 사용**을 추천한다. 책의 입장으로 받아들일 만한 권고 — "LangChain은 골라 쓰는 라이브러리, 통째로 삼키는 종교 아님."

### 4.4 미니멀 대안

- [smolagents (Hugging Face)](https://github.com/huggingface/smolagents) — ~1,000줄. Code agent(파이썬 코드를 액션으로). JSON tool call 대비 단계·LLM 호출 **~30% 절감** 주장([HF blog](https://huggingface.co/blog/smolagents)).
- [Anthropic patterns + smolagents 결합 예시](https://huggingface.co/blog/Sri-Vigneshwar-DJ/building-effective-agents-with-anthropics-best-pra).
- 책 Part 2 결말에 "LangChain이 너무 무거우면 어디로 갈 수 있나"의 보기로 짧게 언급.

---

## 5. LangGraph 영역 — Part 3을 위한 자료

### 5.1 왜 LangGraph가 필요한가

LCEL은 본질적으로 **DAG**(directed acyclic graph)다. 그러나 실제 에이전트는 다음을 요구한다:

- **사이클** — "한 번 더 시도", "조건이 만족될 때까지 반복".
- **상태(state)** — 노드 간 공유되는 누적 메모리.
- **human-in-the-loop** — 특정 노드에서 사람의 승인을 기다림.
- **persistence/checkpointing** — 실패 시 재개, 장시간 대화의 부활.
- **멀티 에이전트 핸드오프** — 다른 에이전트에게 작업 위임.

근거: [Workflows and agents — LangChain 공식](https://docs.langchain.com/oss/python/langgraph/workflows-agents), [LangGraph repo](https://github.com/langchain-ai/langgraph).

### 5.2 핵심 API

- `StateGraph(StateTypedDict)` — TypedDict로 상태 스키마 선언.
- `add_node(name, fn)` — 노드는 `state -> partial state` 함수.
- `add_edge(from, to)` / `add_conditional_edges(from, route_fn)` — 정적/조건부 라우팅.
- `compile(checkpointer=..., store=...)` — short/long-term memory 부착.
- `interrupt(state)` — human-in-the-loop 일시정지 지점.

### 5.3 멀티 에이전트 패턴

| 패턴 | 설명 | 출처 |
|---|---|---|
| **Supervisor** | 중앙 supervisor가 LLM 추론으로 worker에 위임, 결과 수집, 종결 결정. | [langgraph-supervisor](https://reference.langchain.com/python/langgraph/supervisor/), [GitHub repo](https://github.com/langchain-ai/langgraph-supervisor-py) |
| **Hierarchical** | supervisor가 또 다른 supervisor를 갖는 트리 구조. | [LifetidesHub 2026 가이드](https://www.lifetideshub.com/docs/langgraph-multi-agent-orchestration/) |
| **Swarm / Handoff** | 동등한 에이전트가 도구 호출로 서로 권한 이양. | LangChain 공식 multi-agent 가이드 |
| **Tool-calling supervisor** | 별도 supervisor 라이브러리 대신 도구 호출로 위임 — 2026년 권장. | LangChain 공식 권고 |

### 5.4 학술적 다른 길

LangGraph 이전에도 멀티 에이전트 시도는 있었다. 책에서는 비교표로 짧게 소개한다.

| 프레임워크 | 추상 | 특징 | 출처 |
|---|---|---|---|
| **AutoGen** (Microsoft) | conversation | nested chat·group chat. 가장 유연. | [arXiv:2308.08155](https://arxiv.org/abs/2308.08155), [GitHub microsoft/autogen](https://github.com/microsoft/autogen) |
| **MetaGPT** | SOP(표준 운영 절차) | 소프트웨어 엔지니어링 특화. | arXiv:2308.00352 |
| **ChatDev** | 가상 회사 시뮬레이션 | 역할별 직무 SOP. | [IBM 개요](https://www.ibm.com/think/topics/chatdev) |
| **CAMEL** | role-play 2~3 에이전트 | Inception prompting. | arXiv:2303.17760 |

**책의 정리 한 줄:** "AutoGen은 같은 문제를 *대화*로, LangGraph는 *그래프*로 풉다."

### 5.5 LangGraph 실전 사례·페인포인트

- 공식 사례: [LangChain case studies — Klarna, Elastic 등](https://docs.langchain.com/oss/python/langgraph/case-studies). 공급사 측 narrative이므로 외부 비판과 같이 쓸 것.
- 실패담: [Temporal / Grid Dynamics](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics) — LangGraph + Redis "brittle in practice", race condition·stale state·디버깅 난이도. 이후 일부 컴포넌트 이탈.
- [Galileo — Continuously Improve Your LangGraph Multi-Agent System](https://galileo.ai/blog/evaluate-langgraph-multi-agent-telecom) — 고객 1명 문의에 수십 번의 LLM 호출과 agent handoff, 어느 컴포넌트가 실패했는지 추적이 detective work.
- 시사: 멀티 에이전트는 "에이전트 수 늘릴수록 마법"이 아니라 "context loss·핸드오프 ping-pong"이 즉시 문제로 떠오른다.

---

## 6. 공통 주제 — 평가·관찰성·프로덕션·비용·안전성

### 6.1 평가·관찰성 도구 비교

| 도구 | 강점 | 약점 / 주의 |
|---|---|---|
| **LangSmith** | LangChain/LangGraph 통합 최강, trace 시각화 우수. | framework coupling, per-seat 가격. CI/CD quality gate는 제한. |
| **Braintrust** | dataset → scoring → 프로덕션 모니터링 → CI gate까지 한 시스템. | 협업·팀 전제 설계. |
| **Ragas** | RAG 메트릭(faithfulness, answer relevancy)에 특화. | 자체 모니터링 없음. |
| **DeepEval** | Python 친화·CI 자동화. | 시각화는 부족. |
| **Arize Phoenix** | 엔터프라이즈 모니터링. | 작은 팀엔 무거움. |

출처: [LangSmith vs Arize vs Braintrust (Medium Mar 2026)](https://anudeepsri.medium.com/langsmith-vs-arize-vs-braintrust-e397e4728a76), [DeepEval alternatives 2026 — Braintrust](https://www.braintrust.dev/articles/deepeval-alternatives-2026), [EVAL #006 비교 (DEV)](https://dev.to/ultraduneai/eval-006-llm-evaluation-tools-ragas-vs-deepeval-vs-braintrust-vs-langsmith-vs-arize-phoenix-3p11).

추천 조합:
- RAG 위주 + LangChain stack → **RAGAS + LangSmith**.
- Mixed stack + CI gate 중시 → **DeepEval + Braintrust**.

### 6.2 비용 통제 (하드 캡 4종)

프로덕션 권고:
- **iteration cap** (e.g. 최대 25스텝).
- **token cap** (요청·세션·일별).
- **time cap** (한 세션 60초·등).
- **spend cap** (USD/세션).

근거 사례: [Codieshub — Prevent Agent Loops and Spiraling Costs](https://codieshub.com/for-ai/prevent-agent-loops-costs), [Modexa — The Agent Loop Problem](https://medium.com/@Modexa/the-agent-loop-problem-when-smart-wont-stop-ccbf8489180f), [ZenML — Agent Deployment Gap](https://www.zenml.io/blog/the-agent-deployment-gap-why-your-llm-loop-isnt-production-ready-and-what-to-do-about-it).

### 6.3 안전성 — OWASP LLM Top 10 (2025)

- **LLM01: Prompt Injection** — 직접/간접 두 종류. 간접은 RAG·웹·이메일 같은 외부 콘텐츠 경유.
- 에이전트 특화 위협: Thought/Observation Injection, Tool Manipulation, Context Poisoning.
- 완화 기법:
  - **Action screening** — 도구 호출을 원래 user intent와 대조해 drift 시 거부.
  - **Dual-LLM 패턴** — privileged LLM은 도구 보유하되 untrusted content를 직접 읽지 않음. quarantined LLM은 content는 읽되 도구 없음.
  - input·output 분류기 (regex만으로는 부족, 모델 기반 분류기 권장).
  - least privilege scope, 사람 승인이 필요한 destructive action.
- 가드레일 LLM도 LLM이라 자체 injection에 취약 → **다층 방어**.

출처: [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), [Lakera — Indirect Prompt Injection](https://www.lakera.ai/blog/indirect-prompt-injection).

### 6.4 Simon Willison의 lethal trifecta

> "사적 데이터 접근 + 신뢰할 수 없는 콘텐츠 노출 + 외부 통신 능력. 이 셋을 동시에 가진 에이전트는 공격자가 데이터 유출을 트리거하기 쉽다."

출처: [Simon Willison — The lethal trifecta for AI agents](https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents). 책 보안 챕터의 한 페이지짜리 액자.

### 6.5 도구 사용 벤치마크

- **ToolBench** (ICLR'24 spotlight): 16,000+ API, 3,451 tools. DFSDT 기반 solution path. ToolEval(LLM judge), StableToolBench(가상 API 서버 + GPT-4 judge). [GitHub OpenBMB/ToolBench](https://github.com/OpenBMB/ToolBench).
- **API-Bank** (EMNLP 2023): 73 도구, 314 dialog, 753 API call. [arXiv:2304.08244](https://arxiv.org/abs/2304.08244).

### 6.6 프로덕션 에이전트 — 공개 아키텍처에서 배우기

- **Claude Code** ([공식 동작 문서](https://code.claude.com/docs/en/how-claude-code-works), [Augment 가이드](https://www.augmentcode.com/guides/claude-agent-sdk-agent-loops-tool-calls)): 3단계 루프(gather context → take action → verify), CLAUDE.md를 메모리로, MCP로 외부 도구.
- **Cursor**: IDE 내장 inline 모델 + Background Agents(별도 VM).
- **Devin**: 격리된 클라우드 환경에서 plan/write/test/PR을 비동기로.
- 의외 인사이트 ([Mindstudio](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead)): 이들 모두 코드 이해에 **벡터 DB가 아니라 grep + 명시적 컨텍스트**를 쓴다. "RAG = vector DB"는 흔한 오해.

---

## 7. 현장의 페인포인트 (챕터 오프닝 anecdote 후보)

각 챕터의 hook으로 쓸 만한 실제 사례·인용을 묶는다.

1. **"$0.08짜리 작업이 $2,847로 폭증한 4시간"** — 무한 루프·비용 통제 챕터. ([Medium 출처](https://medium.com/@komalbaparmar007/llm-tool-calling-in-production-rate-limits-retries-and-the-infinite-loop-failure-mode-you-must-2a1e2a1e84c8))
2. **"에이전트가 고객 한 명 질문에 핑퐁만 30번"** — 멀티 에이전트 챕터. ([Galileo](https://galileo.ai/blog/evaluate-langgraph-multi-agent-telecom))
3. **"OpenAI API 한 줄을 부르려고 클래스 셋을 거친 날"** — LangChain 추상화 챕터.
4. **"Claude Code는 vector DB 없이 grep만 쓴다"** — 컨텍스트 엔지니어링 챕터. ([Mindstudio](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead))
5. **Hamel Husain: "처음엔 LangChain에 짜증냈는데, 업계 사람들은 다 쓰고 있더라"** — LangChain 입장 정리 챕터.
6. **Simon Willison: "에이전트라는 단어가 합의된 정의를 가질 수 있게 된 것 같다"** — 1장 정의 도입.
7. **"LangGraph + Redis가 brittle in practice였다 (Grid Dynamics)"** — Part 3 도입 또는 상태 관리 챕터.
8. **"$50/min을 태우며 reasoning loop가 돌고 있는데 모니터링은 'up'"** — 관찰성 챕터.

입문자가 가장 자주 막히는 지점(여러 소스에서 반복):

| 카테고리 | 구체적 문제 | 책에서 다룰 위치 |
|---|---|---|
| 도구 호출 | malformed JSON, hallucinated tool name, silent failure | Part 1 도구 직접 구현 → Part 2 LangChain 처리 비교 |
| 무한 루프 | 종료 조건 없는 reasoning loop, 비용 폭증 | Part 1 reasoning loop 챕터 |
| 메모리 | conversation history 무한 누적 → context overflow | Part 1 메모리 챕터 |
| 디버깅 | "그래서 모델이 뭘 봤지?" 추적 안 됨 | Part 2 LangSmith 도입 시점 |
| 에러 처리 | retry·backoff·idempotency 부재 | Part 1 후반부 |
| Prompt injection | 외부 콘텐츠가 도구 호출을 유도 | 공통 보안 챕터 |
| 한국어 | 프롬프트 한국어 성능 편차, tool 설명 영어 혼합 | 한국어 부록 (선택) |

---

## 8. 참고문헌 (카테고리별)

### 8.1 공식 문서 / 가이드
- OpenAI. [Function calling](https://developers.openai.com/api/docs/guides/function-calling).
- OpenAI. [Using tools](https://developers.openai.com/api/docs/guides/tools).
- OpenAI. [o3/o4-mini Function Calling Guide](https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide).
- Anthropic. [Tool use with Claude — Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).
- Anthropic. [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works).
- Anthropic. [How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use).
- Anthropic. [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
- Anthropic. [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents).
- Anthropic. [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works).
- LangChain. [LCEL 개념 페이지](https://python.langchain.com/docs/concepts/lcel/).
- LangChain. [Workflows and agents (LangGraph)](https://docs.langchain.com/oss/python/langgraph/workflows-agents).
- LangChain. [langgraph-supervisor 참조](https://reference.langchain.com/python/langgraph/supervisor/).
- LangChain. [LangGraph case studies](https://docs.langchain.com/oss/python/langgraph/case-studies).
- Temporal. [Basic Agentic Loop with Claude and Tool Calling](https://docs.temporal.io/ai-cookbook/agentic-loop-tool-call-claude-python).

### 8.2 학술 논문 (arXiv·ACL)
- Yao, S. et al. (2022). **ReAct: Synergizing Reasoning and Acting in Language Models.** arXiv:[2210.03629](https://arxiv.org/abs/2210.03629).
- Wang, L. et al. (2023). **Plan-and-Solve Prompting.** arXiv:[2305.04091](https://arxiv.org/abs/2305.04091). ACL 2023.
- Shinn, N. et al. (2023). **Reflexion: Language Agents with Verbal Reinforcement Learning.** arXiv:[2303.11366](https://arxiv.org/abs/2303.11366).
- Yao, S. et al. (2023). **Tree of Thoughts: Deliberate Problem Solving with Large Language Models.** arXiv:[2305.10601](https://arxiv.org/abs/2305.10601). NeurIPS 2023. [Code repo](https://github.com/princeton-nlp/tree-of-thought-llm).
- Wang, G. et al. (2023). **Voyager: An Open-Ended Embodied Agent with LLMs.** arXiv:[2305.16291](https://arxiv.org/abs/2305.16291).
- Wu, Q. et al. (2023). **AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.** arXiv:[2308.08155](https://arxiv.org/abs/2308.08155). ICLR 2024 Workshop.
- Hong, S. et al. (2023). **MetaGPT: Meta Programming for Multi-Agent Collaborative Framework.** arXiv:2308.00352.
- Qian, C. et al. (2023). **Communicative Agents for Software Development (ChatDev).** arXiv:2307.07924.
- Li, G. et al. (2023). **CAMEL: Communicative Agents for "Mind" Exploration of LLM Society.** arXiv:2303.17760.
- Schick, T. et al. (2023). **Toolformer.** arXiv:2302.04761.
- Karpas, E. et al. (2022). **MRKL Systems.** arXiv:2205.00445.
- Li, M. et al. (2023). **API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs.** arXiv:[2304.08244](https://arxiv.org/abs/2304.08244). EMNLP 2023.
- Qin, Y. et al. (2023). **ToolBench / ToolLLM.** arXiv:2307.16789. ICLR'24 spotlight. [GitHub](https://github.com/OpenBMB/ToolBench).
- Zhou, A. et al. (2023). **Language Agent Tree Search (LATS).** arXiv:[2310.04406](https://arxiv.org/pdf/2310.04406).
- Singh, A. et al. (2025). **Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG.** arXiv:[2501.09136](https://arxiv.org/abs/2501.09136).
- (2026). **Memory in the Age of AI Agents: A Survey.** arXiv:[2603.07670](https://arxiv.org/html/2603.07670v1).
- (2026). **Agentic AI: Architectures, Taxonomies, and Applications.** arXiv:[2601.12560](https://arxiv.org/pdf/2601.12560).

### 8.3 비판·논쟁 글
- Husain, H. [Tweet on LangChain (2024-02)](https://x.com/HamelHusain/status/1755406853566247242).
- Husain, H. [Why Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/).
- Humanloop. [Why Your AI Product Needs Evals — interview with Hamel Husain](https://humanloop.com/blog/why-your-product-needs-evals).
- Willison, S. [llm-tool-use tag index](https://simonwillison.net/tags/llm-tool-use/).
- Willison, S. [I think 'agent' may finally have a widely enough agreed upon definition](https://simonw.substack.com/p/i-think-agent-may-finally-have-a).
- Willison, S. [Large Language Models can run tools in your terminal with LLM 0.26](https://simonw.substack.com/p/large-language-models-can-run-tools).
- Willison, S. [The lethal trifecta for AI agents](https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents).
- HN. [The unreasonable effectiveness of an LLM agent loop with tool use](https://hn.nuxt.dev/item/43998472).
- Designveloper. [Why Developers Say LangChain Is "Bad"](https://www.designveloper.com/blog/is-langchain-bad/).
- Woyera (Medium). [6 Reasons why Langchain Sucks](https://medium.com/@woyera/6-reasons-why-langchain-sucks-b6c99c98efbe).
- Guda, S. (Medium). [Challenges & Criticisms of LangChain](https://shashankguda.medium.com/challenges-criticisms-of-langchain-b26afcef94e7).
- safjan.com. [Problems with Langchain and how to minimize their impact](https://safjan.com/problems-with-Langchain-and-how-to-minimize-their-impact/).
- TechTide Solutions. [Is LangChain Bad? A Research-Backed Look](https://techtidesolutions.com/blog/is-langchain-bad/).
- Latenode community. [Negative sentiment towards LangChain](https://community.latenode.com/t/whats-behind-the-negative-sentiment-towards-langchain-in-the-developer-community-and-corporate-environments/39043).
- Turkovic, I. [Rails + RubyLLM vs LangChain in 2026](https://www.ivanturkovic.com/2026/05/03/rails-rubyllm-vs-langchain-2026/).

### 8.4 패턴·구현 자료 (블로그·튜토리얼·코드)
- mattambrogi. [agent-implementation](https://github.com/mattambrogi/agent-implementation).
- KansSoftware. [simple-re-act-agent-from-scratch](https://github.com/KansSoftware/simple-re-act-agent-from-scratch).
- arunpshankar. [react-from-scratch](https://github.com/arunpshankar/react-from-scratch).
- pguso. [ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch).
- Tadeo Donegana. [ReAct Agent framework by scratch (Python)](https://tadeodonegana.com/posts/react-agent-framework-by-scratch-python/).
- Shafiqul AI. [Create ReAct AI Agent from Scratch using Python Without any Framework](https://shafiqulai.github.io/blogs/blog_3.html).
- Daily Dose of DS. [Implementing ReAct Agentic Pattern From Scratch](https://www.dailydoseofds.com/ai-agents-crash-course-part-10-with-implementation/).
- Hugging Face. [smolagents repo](https://github.com/huggingface/smolagents).
- Hugging Face blog. [Introducing smolagents](https://huggingface.co/blog/smolagents).
- HF blog. [Building Effective Agents with Anthropic's Best Practices and smolagents](https://huggingface.co/blog/Sri-Vigneshwar-DJ/building-effective-agents-with-anthropics-best-pra).
- Pinecone. [LCEL Explained](https://www.pinecone.io/learn/series/langchain/langchain-expression-language/).

### 8.5 평가·관찰성 비교
- Anudeep (Medium). [LangSmith vs Arize vs Braintrust (Mar 2026)](https://anudeepsri.medium.com/langsmith-vs-arize-vs-braintrust-e397e4728a76).
- Braintrust. [DeepEval alternatives 2026](https://www.braintrust.dev/articles/deepeval-alternatives-2026).
- Braintrust. [LangSmith vs Braintrust](https://www.braintrust.dev/articles/langsmith-vs-braintrust).
- DEV. [EVAL #006 — RAGAS vs DeepEval vs Braintrust vs LangSmith vs Arize Phoenix](https://dev.to/ultraduneai/eval-006-llm-evaluation-tools-ragas-vs-deepeval-vs-braintrust-vs-langsmith-vs-arize-phoenix-3p11).
- Inference.net. [LLM Evaluation Tools Comparison 2026](https://inference.net/content/llm-evaluation-tools-comparison/).

### 8.6 프로덕션·실패 사례
- Medium / Yamishift. [LLM Tool-Calling in Production: Rate Limits, Retries, and the "Infinite Loop"](https://medium.com/@komalbaparmar007/llm-tool-calling-in-production-rate-limits-retries-and-the-infinite-loop-failure-mode-you-must-2a1e2a1e84c8).
- DEV / piyooshrai. [The Stochastic Tax](https://dev.to/piyooshrai/the-stochastic-tax-why-your-ai-agent-is-a-financial-liability-and-how-to-fix-it-jgc).
- agentpatterns.tech. [Infinite Agent Loop](https://www.agentpatterns.tech/en/failures/infinite-loop).
- Modexa (Medium). [The Agent Loop Problem](https://medium.com/@Modexa/the-agent-loop-problem-when-smart-wont-stop-ccbf8489180f).
- Codieshub. [How to Prevent Infinite Loops and Spiraling Costs](https://codieshub.com/for-ai/prevent-agent-loops-costs).
- ZenML. [The Agent Deployment Gap](https://www.zenml.io/blog/the-agent-deployment-gap-why-your-llm-loop-isnt-production-ready-and-what-to-do-about-it).
- OneUptime. [Monitoring AI Agents in Production: The Observability Gap](https://oneuptime.com/blog/post/2026-03-14-monitoring-ai-agents-in-production/view).
- Temporal. [Prototype to production-ready agentic AI — Grid Dynamics](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics).
- Galileo. [Continuously Improve Your LangGraph Multi-Agent System](https://galileo.ai/blog/evaluate-langgraph-multi-agent-telecom).
- Mindstudio. [Why Cursor, Claude Code, Devin Use grep, Not Vectors](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead).
- Mindstudio. [Claude Code vs Cursor](https://www.mindstudio.ai/blog/claude-code-vs-cursor).
- digitalapplied. [AI Coding Agents: Claude Code vs Cursor vs Codex 2026](https://www.digitalapplied.com/blog/ai-coding-agents-claude-code-cursor-codex-replit-2026).

### 8.7 보안
- OWASP. [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).
- OWASP Cheat Sheet. [LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
- OWASP Cheat Sheet. [AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html).
- Lakera. [Indirect Prompt Injection](https://www.lakera.ai/blog/indirect-prompt-injection).
- Datadog. [LLM guardrails best practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/).
- AppSec Santa. [LLM Guard 2026](https://appsecsanta.com/llm-guard).

### 8.8 한국어 자료
- teddylee777. [langchain-kr (한국어 튜토리얼 GitHub)](https://github.com/teddylee777/langchain-kr).
- WikiDocs. [랭체인LangChain 노트](https://wikidocs.net/book/14314).
- WikiDocs. [03. 에이전트(Agent)](https://wikidocs.net/262586).
- Velog / aldente0630. [LangChain & LangGraph Study](https://velog.io/@aldente0630/LangChain-LangGraph-Study).
- Velog / kwon0koang. [랭그래프(LangGraph): 효율적인 AI 워크플로우 구축](https://velog.io/@kwon0koang/%EB%9E%AD%EA%B7%B8%EB%9E%98%ED%94%84-LangGraph-%ED%9A%A8%EC%9C%A8%EC%A0%81%EC%9D%B8-AI-%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0-%EA%B5%AC%EC%B6%95).
- Velog / ohback. [LangGraph란 무엇이고 언제 쓰면 좋을까?](https://velog.io/@ohback/LangGraph).
- Velog / euisuk-chung. [LangChain Academy: Introduction to LangGraph Module 1](https://velog.io/@euisuk-chung/%EA%B0%95%EC%9D%98-LangChain-Academy-Introduction-to-LangGraph).
- LinkStartAI. [LangChain 솔직 후기 (한국어)](https://www.linkstartai.com/ko/agents/langchain).
- 교보문고. [요즘 AI 에이전트 개발 — 통합서 (출판 시장)](https://product.kyobobook.co.kr/detail/S000217241525).

---

## 9. 논쟁점·열린 질문 (책에서 입장을 정해야 할 지점)

### 9.1 "LangChain vs Bare LLM SDK" — 책의 권고
- **관점 A (LangChain 옹호)**: 통합 폭, LangSmith trace, 빠른 PoC. 업계 표준으로 사실상 안착.
- **관점 B (Bare SDK 권장)**: 추상화 과잉·breaking change·로깅 부재. 입문자는 SDK로 시작해 본질을 익히는 게 낫다.
- **이 책의 입장 (제안)**: Part 1에서 SDK로 본질을 깊게 만진 뒤, Part 2에서 LangChain을 *선별적으로* 도입한다. "LangChain은 골라 쓰는 라이브러리, 통째로 삼키는 종교가 아니다."

### 9.2 "Agent vs Workflow" — Anthropic의 권고를 따를 것인가
- **관점 A (Anthropic)**: 자율성은 비용이다. 가능하면 워크플로로, 정말 필요할 때만 에이전트.
- **관점 B (LangGraph community)**: 상태·사이클·핸드오프가 필요하면 즉시 그래프로 가는 게 낫다.
- **이 책의 입장 (제안)**: Anthropic의 "단순함 우선"을 디폴트로 채택하되, 사이클·핸드오프가 필요한 진짜 사례에서만 LangGraph를 꺼낸다.

### 9.3 "에이전트의 정의"
- 책 1장에서 정의를 못 박고 가야 한다. Simon Willison의 "tools in a loop"가 가장 실용적 정의. Anthropic의 "동적 자기 지시"는 좁은 정의. 둘을 병기하고 책에서는 **"LLM이 도구를 부르는 루프"**를 작업 정의로 채택할 것을 제안.

### 9.4 "벡터 DB는 정말 필요한가"
- **관점 A**: RAG는 vector DB가 사실상 표준.
- **관점 B (Mindstudio·실무 관찰)**: 가장 잘 동작하는 코드 에이전트(Claude Code·Cursor·Devin)는 grep과 명시적 컨텍스트를 쓴다.
- **이 책의 입장 (제안)**: "벡터는 한 선택지, 명시적 컨텍스트가 더 잘 통하는 영역도 있다"고 균형 잡아 서술.

### 9.5 "멀티 에이전트는 진짜 필요한가"
- 회의적 신호: 핑퐁 30회, context loss, 디버깅 detective work.
- 권고: supervisor + 1~2 worker 정도가 입문 한계. 그 이상은 "혼자 잘 짠 한 에이전트"가 보통 이긴다.

### 9.6 "한국어 환경에서의 특수성"
- 한국어 자료는 입문 튜토리얼 위주, 프로덕션 후일담은 영어권 대비 빈약. (확인 필요, 단정 금지)
- 책의 다수 사례는 영어권 자료를 빌려 쓰되, 한국어 부록으로 한국어 프롬프트·tool description 작성 팁을 짧게 보강.

---

## 10. 리서치 한계 (커버하지 못한 영역)

- **로컬 모델 기반 에이전트** (Llama/Qwen/Mistral local). 본 리서치는 OpenAI/Anthropic 중심. 책에서 별도 부록이 필요하다면 추가 리서치 권고.
- **MCP (Model Context Protocol)** 심층 — Claude Code 맥락에서만 짧게 언급. 표준 자체에 한 챕터를 줄 경우 별도 리서치 필요.
- **MAS 학술 평가 벤치마크** — multi-agent 협력 평가 벤치마크(예: AgentBench, GAIA)는 메타데이터 정도만 확인. 책 평가 챕터를 깊이 가져갈 경우 추가 자료 권고.
- **국내 프로덕션 사례** — 한국 기업의 LangChain/LangGraph 도입 후일담은 공개 자료가 적어 anecdote 수집 못 함. 인터뷰·블로그 후속 조사 시 보강 가능.
- **비용 모델링** — 토큰 가격은 모델·시점에 따라 빠르게 변한다. 책에서는 절대 금액 대신 **비율(예: 5x 폭증)**로 서술 권고.
- **익명 주장**: 일부 페인포인트(예: "30번 핑퐁")는 단일 블로그 출처. 다중 출처 교차 검증은 했으나 수치 자체는 anecdotal로 표기.

---

> 이 문서는 챕터 저술가가 사실 확인 없이 직접 인용할 수 있도록 모든 수치·인용에 출처를 붙였다. 책의 입장(9장)은 제안이며, 저술 계획 단계(book-planner)에서 확정한다.
