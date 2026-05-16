# 웹 리서치 — Python AI Agent (From-scratch → LangChain → LangGraph)

> 수집 시점: 2026-05-16. 메인 스레드에서 직접 수집(서브에이전트 도구가 노출되지 않은 환경).

## 1. OpenAI / Anthropic 공식 SDK 패턴

### OpenAI Function Calling (Tool Use)
- 공식 가이드: [Function calling | OpenAI API](https://developers.openai.com/api/docs/guides/function-calling), [Using tools](https://developers.openai.com/api/docs/guides/tools)
- 핵심 원칙(2026 기준):
  - "Intern Test" — 인턴이 함수 설명만 보고도 쓸 수 있어야 한다.
  - 파라미터 최소화 — 코드로 알 수 있는 값(예: `order_id`)은 인자로 받지 마라.
  - enum과 객체로 invalid state를 표현 불가능하게 만들어라.
  - 응답에 `tool_calls`는 0개·1개·여러 개일 수 있고, 각각 `id`·`function.name`·JSON-encoded `arguments`를 갖는다. 항상 배열로 처리한다.
- 비용/정확도 수치: 함수 호출은 호출당 평균 ~346토큰의 오버헤드. 정확도 97–99%, tool 한계 128개([TokenMix Blog](https://tokenmix.ai/blog/function-calling-guide), [ofox.ai 2026 가이드](https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/)).
- o3/o4-mini: tool 사용을 chain-of-thought에 통합해 native하게 학습했다([o3/o4-mini Cookbook](https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide)).

### Anthropic Claude Tool Use
- 공식: [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works), [Implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use), [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
- 에이전트 루프 모델: "model reasons → tool runs → result appended as user turn → model reasons again." 매 iteration마다 도구 호출 여부를 검사.
- 두 가지 실행 모드:
  - **Server-executed tools** — Anthropic 인프라 내부에서 루프가 돈다(예: web search, code execution). 단일 요청이 여러 단계 도구 호출을 자동 처리.
  - **Client-executed tools** — 애플리케이션이 루프를 운전한다. 모든 호출이 round-trip이다.
- [Temporal: Basic Agentic Loop with Claude](https://docs.temporal.io/ai-cookbook/agentic-loop-tool-call-claude-python) — 파이썬 구현 레퍼런스.

### 워크플로 vs 에이전트 (Anthropic 에세이)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — 핵심 정의·5가지 워크플로 패턴.
- **워크플로**: LLM과 도구가 사전에 정해진 코드 경로로 조율되는 시스템.
- **에이전트**: LLM이 자신의 프로세스·도구 사용을 동적으로 지시하고 통제하는 시스템.
- 5가지 워크플로 패턴: **prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer**.
- 권고: "가장 단순한 해법부터. 필요할 때만 복잡도 올려라. 에이전트 시스템을 아예 만들지 않는 것이 답일 수도 있다."

## 2. ReAct 및 From-scratch 구현 자료

- 원논문: [ReAct (Yao et al. 2022, arXiv:2210.03629)](https://arxiv.org/abs/2210.03629).
- From-scratch 구현 리포지토리:
  - [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation) — Simon Willison 스타일.
  - [KansSoftware/simple-re-act-agent-from-scratch](https://github.com/KansSoftware/simple-re-act-agent-from-scratch) — OpenAI GPT 기반 Thought/Action/Observation 루프.
  - [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch) — Gemini용 다양한 변형.
  - [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch) — function calling·메모리·ReAct를 black-box 없이.
- 튜토리얼:
  - [Daily Dose of DS — ReAct from scratch](https://www.dailydoseofds.com/ai-agents-crash-course-part-10-with-implementation/).
  - [Tadeo Donegana — ReAct Agent framework by scratch](https://tadeodonegana.com/posts/react-agent-framework-by-scratch-python/).
  - [shafiqulai.github.io — ReAct AI Agent without any framework](https://shafiqulai.github.io/blogs/blog_3.html).
- 패턴 요지: Think → Act → Observe → Respond 루프를 신중하게 짠 프롬프트 + 출력 파싱 + 도구 실행으로 구현.

## 3. LangChain 핵심 추상

- 공식: [LangChain Expression Language](https://python.langchain.com/docs/concepts/lcel/).
- **Runnable**: LCEL의 모든 객체가 상속받는 추상 연산 단위. `.invoke()`, `.batch()`, `.stream()`, `.ainvoke()` 등 공통 인터페이스.
- **LCEL**: `prompt | llm | parser` 같은 파이프 합성. `__or__()` 오버로드 기반. 자동으로 스트리밍·배치·async·병렬 처리.
- LangChain 0.3 이후 LCEL이 권장 방식이다.
- 한국어 자료:
  - [teddylee777/langchain-kr (위키독스 기반 한국어 튜토리얼)](https://github.com/teddylee777/langchain-kr).
  - [WikiDocs — 랭체인LangChain 노트](https://wikidocs.net/book/14314).
  - [Velog — LangChain & LangGraph Study (aldente0630)](https://velog.io/@aldente0630/LangChain-LangGraph-Study).

## 4. LangGraph 핵심 추상

- 공식: [LangGraph repo](https://github.com/langchain-ai/langgraph), [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents), [langgraph-supervisor](https://reference.langchain.com/python/langgraph/supervisor/).
- **StateGraph** — TypedDict 기반 상태 객체에 노드(함수)와 엣지(라우팅)를 더해 사이클 가능한 그래프 정의.
- **Supervisor 패턴** — `create_supervisor()`가 StateGraph 인스턴스를 반환. 컴파일 시 `checkpointer`/`store`로 short/long-term memory 부착.
- 2026년 권고: 별도 supervisor 라이브러리보다 **tool-calling 기반 supervisor**가 컨텍스트 엔지니어링 측면에서 더 권장됨.
- Multi-agent 패턴 분류(공식 가이드): supervisor, hierarchical, swarm, handoff.
- 한국어 자료:
  - [Velog — 랭그래프(LangGraph): 효율적인 AI 워크플로우 구축](https://velog.io/@kwon0koang/%EB%9E%AD%EA%B7%B8%EB%9E%98%ED%94%84-LangGraph-...).
  - [Velog — LangGraph란 무엇이고 언제 쓰면 좋을까? (ohback)](https://velog.io/@ohback/LangGraph).
  - [Velog — LangChain Academy: Introduction to LangGraph Module 1~4 (euisuk-chung)](https://velog.io/@euisuk-chung/%EA%B0%95%EC%9D%98-LangChain-Academy-Introduction-to-LangGraph).

## 5. LangChain 비판과 대안

- [Designveloper — Why Developers Say LangChain Is "Bad"](https://www.designveloper.com/blog/is-langchain-bad/).
- [Medium / Woyera — 6 Reasons why Langchain Sucks](https://medium.com/@woyera/6-reasons-why-langchain-sucks-b6c99c98efbe).
- [Shashank Guda — Challenges & Criticisms of LangChain](https://shashankguda.medium.com/challenges-criticisms-of-langchain-b26afcef94e7).
- [safjan.com — Problems with Langchain and how to minimize their impact](https://safjan.com/problems-with-Langchain-and-how-to-minimize-their-impact/).
- Hamel Husain의 nuanced 입장: LangChain 전체에 대한 "considered harmful" 글은 없음. 다만 **LangSmith는 LangChain을 안 써도 강력하다**고 추천. 컨설팅에 LangSmith를 사용한다고 트윗·블로그에서 명시([Why Your AI Product Needs Evals — Humanloop interview](https://humanloop.com/blog/why-your-product-needs-evals), [hamel.dev/blog/posts/evals](https://hamel.dev/blog/posts/evals/)).
- 대표 비판 요지:
  - 의존성/추상 레이어 비대 → 깊이 이해하기 어렵다.
  - API 잦은 breaking changes, 문서 시차.
  - 로깅·내부 동작 불투명.
  - 단순한 use case에 과한 wrapper.
- Simon Willison: "tools-in-a-loop 패턴이 paper상 매력적이지만 자주 쓸 가치가 있는지 확신 못 한다." 보안 관점 "lethal trifecta" 경고 — 사적 데이터 + 신뢰할 수 없는 콘텐츠 + 외부 통신 능력을 동시에 갖춘 에이전트는 위험([simonwillison.net/tags/llm-tool-use/](https://simonwillison.net/tags/llm-tool-use/), ["I think 'agent' may finally have a widely enough agreed upon definition"](https://simonw.substack.com/p/i-think-agent-may-finally-have-a)).
- 대안 미니멀 프레임워크: [smolagents (Hugging Face)](https://github.com/huggingface/smolagents) — ~1,000줄. Code agent(파이썬 코드 자체를 액션으로 출력) 방식. JSON tool call 대비 단계·LLM 호출 ~30% 절감 주장.

## 6. 평가·관찰성 도구

- LangSmith — LangChain/LangGraph 통합 강함. 추적·평가에 강하나 framework coupling + per-seat pricing 부담([LangSmith vs Arize vs Braintrust](https://anudeepsri.medium.com/langsmith-vs-arize-vs-braintrust-e397e4728a76)).
- Braintrust — eval lifecycle(데이터셋 → 스코어링 → 프로덕션 모니터링 → CI gate) 통합. CI/CD에 강함([Braintrust 공식 비교 글](https://www.braintrust.dev/articles/langsmith-vs-braintrust)).
- Ragas — RAG 전용 메트릭(faithfulness, answer relevancy 등). 자체 모니터링은 없음.
- DeepEval — Python 친화, CI 자동화.
- Arize Phoenix — 엔터프라이즈 모니터링 성향.
- 추천 매칭: RAG + LangChain stack → RAGAS + LangSmith. Mixed stack → DeepEval + Braintrust.

## 7. 프로덕션 에이전트 사례 (공개 아키텍처)

- [Claude Code 공식 동작 문서](https://code.claude.com/docs/en/how-claude-code-works) — gather context → take action → verify results 3단계 루프, CLAUDE.md를 메모리로 활용, MCP로 외부 도구 연결.
- [Mindstudio — Why Cursor, Claude Code, and Devin Use grep, Not Vectors](https://www.mindstudio.ai/blog/is-rag-dead-what-ai-agents-use-instead) — 코드베이스 이해에 vector DB 대신 grep + 명시적 context.
- Cursor — IDE 내장 inline 모델 + Background Agents(별도 VM).
- Devin — 완전 격리 클라우드 IDE + 비동기 task delegation.
- [AI Coding Agents 2026 ranking](https://www.digitalapplied.com/blog/ai-coding-agents-claude-code-cursor-codex-replit-2026), [Codegen blog ranking](https://codegen.com/blog/best-ai-coding-agents/) — 자율성 vs 감독 스펙트럼 정리.

## 8. 프로덕션 페인포인트 (실제 보고)

- **무한 루프** — 15분 동안 60+ 스텝, $0.08 작업이 $12로 폭증. 4시간 검출 지연 시 총 $2,847 보고 사례([LLM Tool-Calling in Production — Medium](https://medium.com/@komalbaparmar007/llm-tool-calling-in-production-rate-limits-retries-and-the-infinite-loop-failure-mode-you-must-2a1e2a1e84c8), [agentpatterns.tech — Infinite Loop](https://www.agentpatterns.tech/en/failures/infinite-loop)).
- 토큰 폭증 예시: 1회 500토큰 → 15회 4M토큰.
- 환각 tool name·malformed JSON → 대부분 프레임워크가 crash 또는 silently 넘어감.
- 권고: iteration·token·time·spend의 하드 캡, 토큰 예산.
- LangGraph 프로덕션 후일담: 외부 호출마다 try-catch + 재시도 직접 작성. race condition·stale state·에이전트 stuck. Grid Dynamics는 LangGraph + Redis가 "brittle in practice"라 평가하고 일부 이탈([Grid Dynamics 사례](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics)).

## 9. 보안·가드레일

- [OWASP LLM Top 10 (2025) — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html).
- 직접 injection vs 간접 injection(웹·파일·이메일 등 외부 콘텐츠 경유).
- 에이전트 특화 위협: Thought/Observation Injection, Tool Manipulation, Context Poisoning.
- 완화: action screening(도구 호출을 user intent 대비 검증), **Dual-LLM 패턴**(privileged LLM은 도구 보유·신뢰 못 할 컨텐츠 못 읽음 / quarantined LLM은 컨텐츠 읽되 도구 없음), input/output 분류기, least privilege scope.
- 가드레일 LLM도 LLM이라 injection에 취약 → 다층 방어로 봐야 함.
- [Simon Willison — The lethal trifecta](https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents).

## 10. 한국어 종합

- [LinkStartAI — LangChain 솔직 후기 (한국어)](https://www.linkstartai.com/ko/agents/langchain) — 가격·장단점·대안.
- [WikiDocs — 03. 에이전트(Agent)](https://wikidocs.net/262586).
- 한국 서적 시장: 교보문고에 "AI 에이전트 개발, LLM RAG ADK MCP LangChain A2A" 류 통합서 출간 중([교보문고 상품 페이지](https://product.kyobobook.co.kr/detail/S000217241525)). 시장 형성 시점.
