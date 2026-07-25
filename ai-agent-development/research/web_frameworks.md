<!-- 검색 시점: 2026-07-25 기준 -->
<!-- 담당: web-researcher #1 (프레임워크 / 오케스트레이션 / 도구 호출 프로토콜 / 런타임·샌드박스) -->
<!-- 데이터·벡터DB·평가·가드레일은 web-researcher #2 담당 — 이 파일에 없음 -->

# 웹 리서치 (#1): AI Agent 프레임워크 · 오케스트레이션 · 프로토콜 · 런타임

## 이 문서의 검증 규율 (fact-checker 필독)

- **버전 열은 전부 2026-07-25에 실제 호출로 확인한 값이다.** 수집 방법: `gh api repos/{owner}/{repo}/releases/latest`, `gh api repos/{owner}/{repo}`, `pypi.org/pypi/{pkg}/json`, `registry.npmjs.org/{pkg}/latest`, 그리고 스펙 사이트 직접 fetch.
- 확인하지 못한 셀은 **`미확인`**으로 남겼다. 추측으로 채운 셀은 없다. 미확인 셀 전체 목록은 문서 하단 「미확인 항목 목록」에 있다.
- 라이선스 열의 값은 GitHub `license.spdx_id` 또는 npm `license` 필드의 **기계 판정값**이다. `NOASSERTION`·`null`은 GitHub가 분류하지 못한 것이므로 그대로 미확인 처리했다 (BSL·커스텀 라이선스 가능성 있음 — 본문에서 "오픈소스"라고 단정하면 안 되는 항목).
- **1차 소스만 URL로 실었다** — GitHub Releases, 패키지 레지스트리, 공식 문서, 스펙 사이트. 블로그 요약은 별도 「자료」 섹션으로 분리했다.
- 활동 신호는 `pushed_at`(마지막 커밋 push)과 릴리스 `published_at`의 간격으로 판단했다. 이 간격이 벌어진 프로젝트는 그렇게 표시했다.

### ⚠️ 증거 등급이 두 가지다 — 섞어 쓰면 안 된다

| 등급 | 무엇이 여기 속하나 | 신뢰도 |
|------|------------------|--------|
| **A · 결정론적 API** | 표 A~D의 **버전·라이선스·스타·날짜** 열 전부. `gh api` / PyPI JSON / npm registry 직접 호출값 | 그대로 인용 가능 |
| **B · WebFetch 요약 경유** | 「비용·지연·동시성」 섹션의 **모든 수치**, 「자료」 섹션의 모든 인용문·한국어 블로그 수치 | **인용 전 원문 대조 필요** |

B등급은 페이지를 소형 모델이 요약한 결과다. **실제로 이번 세션에서 B등급 오류가 1건 발견됐다** — 우아한형제들 글의 컨텍스트 감소 수치를 1차 요약이 "약 20,000 bytes → 약 1,000 bytes"로 뭉갰으나, 재요청으로 원문을 확인하니 실제로는 규모별 3행 표(41,944→1,763 / 29,386→668 / 9,749→539)였다. 아래 §7·§9에서 재확인을 거친 항목은 **✅원문확인**으로, 거치지 않은 항목은 **⚠️요약경유**로 표시했다.

### ⚠️ 인용 가능 버전 vs 인용하면 안 되는 버전

버전을 **본문 산문에 박아 넣을 때**의 규칙이다. 확인된 값이라도 배포 주기가 빠르면 출간 시점에 이미 틀린다.

| 안정 — 값을 그대로 써도 됨 | 불안정 — "0.2.x / 2026-07 기준" 형태로만, 또는 아예 쓰지 말 것 |
|---|---|
| MCP 스펙 `2025-11-25` (8개월간 불변) · A2A `1.0.0` · AGENTS.md(버전 없음) · 매니지드 서비스(버전 개념 없음) | Claude Agent SDK `v0.2.128`/`v0.3.220` (일 단위 배포 — 며칠 내 틀림) · Wasmtime `v47.0.2` (월간 메이저) · Pydantic AI `v2.18.0`·CrewAI `1.15.6`·Agno `v2.8.2`·E2B·Daytona (주 단위) |
| 메이저 버전만 쓰는 건 대체로 안전 (예: "LangGraph 1.x", "Pydantic AI 2.x", "ADK 2.x") | 패치 버전을 산문에 박는 것은 전 항목 금지 |

---

## 0. 이번 조사에서 나온 "책의 뼈대를 바꿀 수 있는" 발견 5개

계획 단계에서 먼저 읽어야 하는 항목이다. 전부 1차 소스로 확인했다.

1. **Microsoft Agent Framework가 AutoGen·Semantic Kernel의 공식 후속으로 명문화됐다.** Microsoft Learn 원문: *"The Agent Framework is the direct successor, created by the same teams. ... In short, Agent Framework is the next generation of both Semantic Kernel and AutoGen."* 여기에 AutoGen 레포의 정체 신호가 겹친다 — 최신 릴리스 `python-v0.7.5`(**2025-09-30**), 마지막 push **2026-04-15**.
   > **⚠️ 서술 경계선 (fact-checker 필독).** 확인된 사실은 위 두 줄까지다. **Microsoft는 AutoGen의 폐기(deprecation) 공지를 낸 적이 없고, 레포도 아카이브되지 않았다**(`archived: false`, 2026-07-25 확인). 같은 Learn 페이지는 오히려 *"Both Semantic Kernel and AutoGen have benefited significantly from the open-source community"*라고 쓴다. 따라서 **"AutoGen은 개발이 중단됐다/종료됐다/죽었다"는 이 문서의 추론이며 인용 가능한 근거가 없다.** 본문에 쓸 수 있는 표현은 "공식 후속이 있다"(인용 가능) + "릴리스가 10개월 정지 상태다"(날짜로 검증 가능)까지다. → 실무 결론은 그대로 유효하다: **신규 프로젝트를 AutoGen으로 시작하라고 권하는 서술은 근거가 없다.** [축 2]
2. **2026년의 새 용어는 "agent harness"이고, 벤더 3곳이 동시에 채택했다.** LangChain `deepagents`("The batteries-included agent harness"), AWS Strands(레포가 `strands-agents/sdk-python` → **`strands-agents/harness-sdk`**로 개명, 제품명 "Strands Harness"), Microsoft Agent Framework(3대 기능 축의 하나가 **Harness**: 계획·todo 추적·컨텍스트 압축·파일 접근·메모리·don't-ask-again 승인·관측). 한국에서도 우아한형제들·AWS Korea가 같은 용어를 쓴다. → **"프레임워크 위에 한 층 더 있다(SDK → harness)"가 이 책의 축 2/축 6을 관통하는 서사가 될 수 있다.** [축 2][축 6]
3. **LangChain 생태계가 3층으로 정리됐다.** 공식 문서 기준: `langgraph`(저수준 오케스트레이션 런타임) → `langchain`(고수준 에이전트/`create_agent`) → `deepagents`(harness 층). 문서가 직접 *"you don't need to use LangChain to use LangGraph"*라고 못 박는다. → 독자의 가장 흔한 혼란("LangChain이랑 LangGraph 뭐가 다른가")을 공식 문서 인용으로 해소 가능. [축 2]
4. **Pydantic AI·Agno·CrewAI·Strands가 모두 메이저 버전을 넘겼다** (각각 2.18.0 / 2.8.2 / 1.15.6 / 1.50.1). 2025년 자료 기준의 "0.x 실험 단계" 서술은 전부 낡았다. [축 2]
5. **MCP 스펙의 현행 리비전은 `2025-11-25`다.** `modelcontextprotocol.io/specification/latest`가 이 리비전의 schema를 authoritative로 지목한다. 2026년에 새 리비전이 나오지 않았다 — 즉 **스펙은 안정화 국면이고, 움직이는 건 SDK와 레지스트리다.** [축 1]

---

## 1. 표 A — 에이전트 프레임워크 [축 2] (주력), [축 1] (원리 정의 부분)

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| **LangGraph** (Python) | 프레임워크·저수준 그래프 런타임 | `1.2.9` (릴리스 2026-07-10) | https://github.com/langchain-ai/langgraph/releases/tag/1.2.9 | MIT | 명시적 상태 그래프 + 체크포인터로 durable execution·HITL·time travel을 프레임워크가 보장 | 활발 (push 2026-07-25, ★38,104) | 2026-07-25 |
| **LangGraph** (JS) | 프레임워크 | `1.4.8` (npm `@langchain/langgraph`) | https://www.npmjs.com/package/@langchain/langgraph | MIT | 위와 동일, TS 포트 (버전 라인이 Python과 다름 — 혼동 주의) | 활발 | 2026-07-25 |
| **LangChain** (core) | 고수준 에이전트 프레임워크 | `langchain-core==1.5.1` (2026-07-23) | https://github.com/langchain-ai/langchain/releases/tag/langchain-core%3D%3D1.5.1 | MIT | 1.x부터 자기 정의를 "The agent engineering platform"으로 변경, `create_agent`가 표준 진입점 | 매우 활발 (push 2026-07-25, ★142,568) | 2026-07-25 |
| **deepagents** | harness (프레임워크 상위 층) | `deepagents==0.6.12` (릴리스 2026-06-25) | https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.6.12 | MIT | LangGraph 위에 계획·서브에이전트·컨텍스트 관리를 얹은 "batteries-included agent harness" | 활발 (push 2026-07-25, ★26,792 — 릴리스보다 커밋이 앞서감) | 2026-07-25 |
| **CrewAI** | 프레임워크·역할 기반 멀티에이전트 | `1.15.6` (2026-07-24) | https://github.com/crewAIInc/crewAI/releases/tag/1.15.6 | MIT | 역할(role)·목표(goal) 선언으로 팀을 구성하는 Crews + 이벤트 기반 Flows 이원 구조 | 매우 활발 (push 2026-07-25, ★56,111) | 2026-07-25 |
| **Microsoft Agent Framework** | 프레임워크 (AutoGen+SK 후속) | `1.12.1` (PyPI `agent-framework`, 2026-07-23) | https://pypi.org/project/agent-framework/ | MIT | AutoGen의 추상화 + Semantic Kernel의 엔터프라이즈 기능 통합 + 그래프 워크플로 + Harness. .NET/Python/Go | 활발 (push 2026-07-24, ★12,386). Go는 **public preview** | 2026-07-25 |
| **AutoGen** | 프레임워크 (**공식 후속 존재**) | `python-v0.7.5` (릴리스 **2025-09-30**) / PyPI `autogen-agentchat` `0.7.5` (2025-09-30) | https://github.com/microsoft/autogen/releases/tag/python-v0.7.5 | `CC-BY-4.0` (GitHub 판정 — 코드 라이선스는 **미확인**) | 멀티에이전트 대화(GroupChat) 패턴의 원류 | 릴리스 후 **약 10개월 경과**, 마지막 push 2026-04-15, **`archived: false`**. 공식 후속 = Agent Framework (MS Learn 명문). **폐기 공지는 없음 — "중단"으로 서술 금지** | 2026-07-25 |
| **Semantic Kernel** | 프레임워크 (**후속 있음**) | `dotnet-1.78.0` (2026-07-07) | https://github.com/microsoft/semantic-kernel/releases/tag/dotnet-1.78.0 | MIT | .NET 진영의 커널/플러그인 모델. 유지보수는 계속되나 신규는 Agent Framework 권고 | 유지보수 활발 (push 2026-07-24, ★28,364) | 2026-07-25 |
| **Agno** | 프레임워크·고성능 런타임 | `v2.8.2` (2026-07-24) / PyPI `agno` `2.8.2` | https://github.com/agno-agi/agno/releases/tag/v2.8.2 | Apache-2.0 | 자기 정의를 "Build, run, and manage agent platforms" — 프레임워크 + 런타임/플랫폼 일체형 | 매우 활발 (push 2026-07-25, ★41,417) | 2026-07-25 |
| **Pydantic AI** | 프레임워크·타입 안전 | `v2.18.0` (2026-07-25) / PyPI `pydantic-ai` `2.18.0` | https://github.com/pydantic/pydantic-ai/releases/tag/v2.18.0 | MIT | Pydantic 스키마로 입출력·의존성 주입을 타입 검증. FastAPI 개발자에게 가장 익숙한 모델 | 매우 활발 (당일 릴리스, ★18,803) | 2026-07-25 |
| **Mastra** | 프레임워크 (TypeScript) | `1.52.1` (npm `@mastra/core`) / GitHub 릴리스 `@mastra/core@1.51.0` (2026-07-15) | https://www.npmjs.com/package/@mastra/core | Apache-2.0 (npm 필드) / 레포는 `NOASSERTION` | TS 네이티브 풀스택: 에이전트+워크플로+RAG+eval+로컬 dev playground 일체 | 활발 (push 2026-07-25, ★26,549). **npm이 GitHub 릴리스보다 앞선다** | 2026-07-25 |
| **OpenAI Agents SDK** (Python) | 프레임워크·경량 | `v0.18.3` (2026-07-17) | https://github.com/openai/openai-agents-python/releases/tag/v0.18.3 | MIT | 추상화 최소화. 원시 개념 5개(Agents/Handoffs/Guardrails/Sessions/Runner) + 내장 트레이싱 | 활발 (push 2026-07-25, ★28,160). **1.0 미만** | 2026-07-25 |
| **OpenAI Agents SDK** (JS) | 프레임워크·경량 | `v0.13.5` (2026-07-17) / npm `@openai/agents` `0.13.5` | https://github.com/openai/openai-agents-js/releases/tag/v0.13.5 | MIT | 위 + 음성 에이전트(voice agents) 지원 | 활발 (★3,465) | 2026-07-25 |
| **OpenAI Swarm** | 교육용 실험 (**공식 후속 존재**) | 릴리스 없음 (태그 발행 이력 자체가 없음) | https://github.com/openai/swarm | MIT | Agents SDK의 전신. 레포 자기 소개가 *"Educational framework"*, Agents SDK 문서가 이를 *"our previous experimentation for agents, Swarm"*으로 규정 | 릴리스 0개, push 2026-04-15, ★21,858, **`archived: false`**. 후속은 Agents SDK (공식). **"폐기됨"은 추론 — 공식 폐기 공지 미확인** | 2026-07-25 |
| **Claude Agent SDK** (Python) | 프레임워크·harness | `v0.2.128` (2026-07-25) | https://github.com/anthropics/claude-agent-sdk-python/releases/tag/v0.2.128 | MIT | Claude Code의 에이전트 루프(파일 도구·서브에이전트·훅·권한)를 그대로 라이브러리로 노출 | 매우 활발 (당일 릴리스, ★7,718). 릴리스 번호가 3자리 = 초고빈도 배포 | 2026-07-25 |
| **Claude Agent SDK** (TS) | 프레임워크·harness | `v0.3.220` (2026-07-25) / npm `@anthropic-ai/claude-agent-sdk` `0.3.220` | https://github.com/anthropics/claude-agent-sdk-typescript/releases/tag/v0.3.220 | **미확인** (GitHub `null`, npm "SEE LICENSE IN README.md" — Anthropic 커스텀) | 위 + TS 우선 | 매우 활발 (당일 릴리스, ★1,655) | 2026-07-25 |
| **Google ADK** (Python) | 프레임워크·엔터프라이즈 | `v2.5.0` (2026-07-16) / PyPI `google-adk` `2.5.0` | https://github.com/google/adk-python/releases/tag/v2.5.0 | Apache-2.0 | 코드 우선 + 템플릿 워크플로 에이전트(Sequential/Parallel/Loop) + 2.0부터 그래프 워크플로. A2A·MCP 내장 | 활발 (push 2026-07-25, ★20,875) | 2026-07-25 |
| **Google ADK** (Go) | 프레임워크 | `v2.1.0` (2026-07-23) | https://github.com/google/adk-go/releases/tag/v2.1.0 | Apache-2.0 | Go 진영 최대 규모 에이전트 프레임워크 (★8,524) | 활발 (push 2026-07-25) | 2026-07-25 |
| **Google ADK** (Java) | 프레임워크 | `v1.7.0` (2026-07-20) | https://github.com/google/adk-java/releases/tag/v1.7.0 | Apache-2.0 | JVM 백엔드 팀의 선택지 (★1,660) | 활발 (push 2026-07-24) | 2026-07-25 |
| **Strands Agents** (Python) | 프레임워크 → harness | `1.50.1` (PyPI `strands-agents`, 2026-07-24) | https://pypi.org/project/strands-agents/ | Apache-2.0 | 모델 주도(model-driven) 최소 설정. AWS가 사내 프로덕션 시스템에서 추출 | 활발. **레포가 `strands-agents/harness-sdk`로 개명됨** | 2026-07-25 |
| **Strands Agents** (TS) | 프레임워크 → harness | `typescript/v1.11.1` (2026-07-24) | https://github.com/strands-agents/harness-sdk/releases/tag/typescript/v1.11.1 | Apache-2.0 | 위의 TS SDK. Python과 버전 라인 완전 별개 (1.50 vs 1.11) | 활발 (★6,691) | 2026-07-25 |
| **LlamaIndex** | 프레임워크 (**포지션 이동**) | `v0.14.23` (2026-06-24) / PyPI `llama-index-core` `0.14.23` | https://github.com/run-llama/llama_index/releases/tag/v0.14.23 | MIT | 자기 정의가 "the leading **document agent and OCR** platform"으로 이동 — 범용 에이전트 프레임워크 경쟁에서 문서 처리로 특화 | 활발 (push 2026-07-25, ★51,078) but 릴리스 1개월 경과. **여전히 0.x** | 2026-07-25 |
| **smolagents** | 프레임워크·코드 에이전트 | `v1.26.0` (**2026-05-29**) / PyPI `smolagents` `1.26.0` | https://github.com/huggingface/smolagents/releases/tag/v1.26.0 | Apache-2.0 | "agents that think in code" — 액션을 JSON이 아닌 Python 코드로 생성 | **완만**: 릴리스 2개월 경과, push 2026-07-21 (★28,526) | 2026-07-25 |
| **DSPy** | 프롬프트/프로그램 최적화 (프레임워크 인접) | `3.2.1` (**2026-05-05**) / PyPI `dspy` `3.2.1` | https://github.com/stanfordnlp/dspy/releases/tag/3.2.1 | MIT | "programming—not prompting": 시그니처+옵티마이저로 프롬프트를 컴파일 | **완만**: 릴리스 2.5개월 경과, push 2026-07-24 (★36,364) | 2026-07-25 |
| **Cloudflare Agents SDK** | 프레임워크 + 런타임 일체 | `0.19.0` (npm `agents`) | https://www.npmjs.com/package/agents | MIT | Durable Objects를 에이전트 세션 = 상태 단위로 매핑. 프레임워크와 실행환경이 분리되지 않는 설계 | 활발 (push 2026-07-24, ★5,310) | 2026-07-25 |

**프레임워크 표 소계: 25개 행 (도구 단위로는 21개 프로젝트)**

---

## 2. 표 B — 오케스트레이션 · 워크플로 · durable execution [축 5], [축 6]

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| **Temporal** (서버) | durable execution 플랫폼 | `v1.31.2` (2026-07-08) | https://github.com/temporalio/temporal/releases/tag/v1.31.2 | MIT | 이벤트 히스토리 + 리플레이로 "완주 보장". 결정론 제약이 대가 | 매우 활발 (push 2026-07-25, ★21,832) | 2026-07-25 |
| **Temporal** (Python SDK) | SDK | `1.30.0` (2026-07-02) / PyPI `temporalio` `1.30.0` | https://github.com/temporalio/sdk-python/releases/tag/1.30.0 | MIT | 서버 버전과 SDK 버전이 별개 (둘 다 1.3x대라 혼동 주의) | 활발 | 2026-07-25 |
| **Temporal** (TS SDK) | SDK | `v1.21.1` (2026-07-24) | https://github.com/temporalio/sdk-typescript/releases/tag/v1.21.1 | MIT | — | 활발 (push 2026-07-25) | 2026-07-25 |
| **Restate** | durable execution (경량) | `v1.7.2` (2026-07-06) | https://github.com/restatedev/restate/releases/tag/v1.7.2 | **미확인** (GitHub `NOASSERTION` — BSL 등 가능) | 단일 바이너리로 durable 실행·상태·큐·통신을 제공. Temporal보다 운영 부담 낮음을 소구 | 활발 (push 2026-07-24, ★4,212) | 2026-07-25 |
| **Restate** (TS SDK) | SDK | `v1.16.2` (2026-07-16) | https://github.com/restatedev/sdk-typescript/releases/tag/v1.16.2 | MIT | — | 활발 (★114 — SDK 레포는 별도) | 2026-07-25 |
| **Inngest** (서버) | 워크플로 오케스트레이션 | `v1.38.1` (2026-07-21) | https://github.com/inngest/inngest/releases/tag/v1.38.1 | **미확인** (GitHub `NOASSERTION`) | 이벤트 기반 step function. 서버리스/서버/엣지 모두에서 실행 | 활발 (push 2026-07-25, ★5,645) | 2026-07-25 |
| **Inngest** (JS SDK) | SDK | `4.13.0` (npm `inngest`) | https://www.npmjs.com/package/inngest | Apache-2.0 | SDK는 Apache-2.0 — 서버와 라이선스가 다름 | 활발 | 2026-07-25 |
| **Prefect** | 데이터/일반 워크플로 | `3.8.0` (2026-07-23) | https://github.com/PrefectHQ/prefect/releases/tag/3.8.0 | Apache-2.0 | 파이썬 함수에 데코레이터만 붙이는 낮은 진입 장벽. 데이터 파이프라인 출신 | 매우 활발 (push 2026-07-25, ★23,476) | 2026-07-25 |
| **Dagster** | 데이터 오케스트레이션 | `1.13.15` (2026-07-23) | https://github.com/dagster-io/dagster/releases/tag/1.13.15 | Apache-2.0 | 자산(asset) 중심 모델 — 에이전트보다 데이터 계보 추적에 최적 | 매우 활발 (push 2026-07-24, ★15,896) | 2026-07-25 |
| **DBOS** (Python) | durable execution (DB 기반) | `2.28.0` (2026-07-21) / PyPI `dbos` `2.28.0` | https://github.com/dbos-inc/dbos-transact-py/releases/tag/2.28.0 | MIT | 외부 오케스트레이터 없이 **Postgres 하나로** durable 워크플로. 라이브러리로 임베드 | 활발 (push 2026-07-24, ★1,493) | 2026-07-25 |
| **Cloudflare Workflows** | 매니지드 durable execution | `미확인 (managed service, 버전 개념 없음)` | https://developers.cloudflare.com/workflows/reference/limits/ | 매니지드 (해당 없음) | Workers 위에서 step 단위 재시도·1년 sleep. 아래 「비용·지연·한도」에 수치 전문 | 문서 유지 중 | 2026-07-25 |
| **AWS Bedrock AgentCore Runtime** | 매니지드 에이전트 런타임 | `미확인 (managed service, 버전 개념 없음)` | https://aws.amazon.com/ko/blogs/tech/harness-engineering-from-deep-insight/ (2차 — 공식 문서 미확인) | 매니지드 (해당 없음) | Strands 등으로 만든 에이전트를 매니지드로 실행. 코드 실행은 Fargate로 분리하는 패턴이 권고됨 | **1차 소스 미확인** — 아래 「수집 한계」 참조 | 2026-07-25 |

**오케스트레이션 표 소계: 12개 행 (프로젝트 9개)**

---

## 3. 표 C — 도구 호출 프로토콜 · 규약 [축 1] (핵심)

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| **MCP (스펙)** | 도구 호출 프로토콜 스펙 | **리비전 `2025-11-25`** (현행 latest) | https://modelcontextprotocol.io/specification/latest | **미확인** (레포 `NOASSERTION`) | JSON-RPC 2.0 기반. 서버가 Resources/Prompts/Tools 제공, 클라이언트가 Sampling/Roots/Elicitation 제공 | 스펙은 **안정화**: 2025-11-25 이후 새 리비전 없음. 레포 push 2026-07-23 (★8,678) | 2026-07-25 |
| **MCP Python SDK** | SDK | `v1.28.1` (2026-06-26) / PyPI `mcp` `1.28.1` | https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.28.1 | MIT | 서버·클라이언트 양쪽. FastMCP 스타일 데코레이터 | 활발 (push 2026-07-24, ★23,717) | 2026-07-25 |
| **MCP TypeScript SDK** | SDK | `v1.29.0` (**2026-03-30**) / npm `@modelcontextprotocol/sdk` `1.29.0` | https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v1.29.0 | MIT (npm) / 레포 `NOASSERTION` | TS 서버·클라이언트 | **릴리스 정체**: 4개월 경과했으나 push는 2026-07-24 (★12,947) — main은 계속 움직임 | 2026-07-25 |
| **MCP Registry** | MCP 서버 디스커버리 | `v1.8.0` (2026-07-13) | https://github.com/modelcontextprotocol/registry/releases/tag/v1.8.0 | **미확인** (`NOASSERTION`) | 커뮤니티 MCP 서버 레지스트리 — "어디서 서버를 찾나" 문제의 공식 답 | 활발 (push 2026-07-25, ★7,066) | 2026-07-25 |
| **A2A (Agent2Agent)** | 에이전트 간 통신 프로토콜 | `v1.0.0` (릴리스 2026-05-28, 스펙 사이트도 1.0.0) | https://a2a-protocol.org/latest/specification/ | Apache-2.0 | 불투명한(opaque) 에이전트끼리 협업. Agent Card·Task·Message·Artifact + SSE 스트리밍 + 웹훅 푸시. 바인딩 3종(JSON-RPC 2.0 / gRPC / HTTP+JSON) | **1.0 도달 후 안정** (릴리스 2개월 경과, push 2026-07-23, ★24,998) | 2026-07-25 |
| **A2A JS SDK** | SDK | `1.0.0` (npm `@a2a-js/sdk`) | https://www.npmjs.com/package/@a2a-js/sdk | Apache-2.0 | — | — | 2026-07-25 |
| **AGENTS.md** | 에이전트 지시 파일 규약 | `미확인 (버전 표기 없는 규약)` | https://agents.md/ | 미확인 | "README for agents". **Linux Foundation 산하 Agentic AI Foundation**이 스튜어드. 60k+ 오픈소스 프로젝트 채택, 60개+ 도구 지원 (OpenAI Codex·Gemini CLI·Devin·Claude·Copilot·Cursor·Zed 등) | 확산 국면 | 2026-07-25 |
| **OpenAI function calling / tool use** | 벤더 API 스펙 | `미확인 (API 스펙 — 버전 태그 없음)` | https://platform.openai.com/docs/guides/function-calling (미fetch) | 해당 없음 | 도구 호출의 사실상 원형 스키마 | — | 2026-07-25 |

**프로토콜 표 소계: 8개 행 (프로젝트/규약 6개)**

> **fact-checker 주의:** MCP 리비전을 "2025-06-18"로 쓴 자료가 아직 많다. **현행은 `2025-11-25`**이며 이는 스펙 사이트의 `/specification/latest`가 직접 지목하는 값이다. 또한 A2A를 "Google 프로젝트"로만 쓰면 부정확하다 — 스펙 사이트는 `a2aproject` 커뮤니티 거버넌스를 명시하고, Linux Foundation 귀속은 이번 세션에서 **확인하지 못했다**(AGENTS.md의 Linux Foundation 귀속은 확인됨).

---

## 4. 표 D — 런타임 · 샌드박스 · 격리 [축 5] (주력)

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| **E2B** | 코드 실행 샌드박스 (매니지드) | CLI `@e2b/cli@2.15.1` (2026-07-24) / PyPI `e2b` `2.35.0` / npm `@e2b/code-interpreter` `2.7.0` | https://github.com/e2b-dev/E2B/releases/tag/%40e2b/cli%402.15.1 | Apache-2.0 | pause/resume로 샌드박스 상태를 무기한 보존. 재개 ~1초 | 매우 활발 (push 2026-07-25, ★13,098) | 2026-07-25 |
| **Daytona** | 코드 실행 인프라 | GitHub `v0.190.0` (2026-06-23) / PyPI `daytona` `0.200.2` (2026-07-24) | https://github.com/daytonaio/daytona/releases/tag/v0.190.0 | **미확인** (GitHub `null`) | "AI 생성 코드 실행용 secure & elastic 인프라"로 재포지셔닝 | 활발 (push 2026-07-24, ★72,170 — 이 표 최대). **SDK가 서버 릴리스보다 앞섬** | 2026-07-25 |
| **Modal** | 서버리스 컴퓨트 + Sandbox | 클라이언트 `1.5.3` (PyPI `modal`, 2026-07-23) | https://modal.com/docs/guide/sandbox | Apache-2.0 (클라이언트) / 서비스는 매니지드 | `Sandbox.create()`로 "untrusted user or agent code"용 컨테이너. GPU 워크로드 병행 강점 | 활발 (push 2026-07-25) | 2026-07-25 |
| **Vercel Sandbox** | 샌드박스 (매니지드) | SDK `2.9.0` (npm `@vercel/sandbox`) / 서비스 `미확인 (managed service, 버전 개념 없음)` | https://vercel.com/docs/sandbox | Apache-2.0 (SDK) | **Firecracker microVM 명시**. 영속 샌드박스가 기본값 + 스냅샷 + 멀티에이전트용 Linux 사용자 격리 | 문서 최신 (last_updated 2026-06-30) | 2026-07-25 |
| **Cloudflare Sandbox SDK** | 샌드박스 (엣지) | `@cloudflare/sandbox@0.12.4` (2026-07-21) / npm 동일 | https://github.com/cloudflare/sandbox-sdk/releases/tag/%40cloudflare/sandbox%400.12.4 | Apache-2.0 (npm) / 레포 `NOASSERTION` | Cloudflare 엣지 위 샌드박스, Durable Objects·Agents SDK와 한 몸 | 활발 (push 2026-07-24, ★1,076). **0.x — API 변동 가능** | 2026-07-25 |
| **Cloudflare Durable Objects** | 상태·체크포인트 프리미티브 | `미확인 (managed service, 버전 개념 없음)` | https://developers.cloudflare.com/durable-objects/platform/limits/ | 매니지드 | 단일 스레드 객체 + SQLite 스토리지 = 에이전트 세션 상태의 자연스러운 단위 | 문서 유지 중 | 2026-07-25 |
| **Fly.io Machines** | microVM (매니지드) | `미확인 (managed service, 버전 개념 없음)` | https://fly.io/docs/machines/ | 매니지드 | 공식 표현: *"fast-launching VMs; they can be started and stopped at subsecond speeds"* + REST API로 수명주기 직접 제어 | 문서 유지 중 | 2026-07-25 |
| **Firecracker** | microVM 하이퍼바이저 (셀프호스팅) | `v1.16.1` (2026-07-02) | https://github.com/firecracker-microvm/firecracker/releases/tag/v1.16.1 | Apache-2.0 | 위 매니지드 샌드박스 다수의 실제 기반. 직접 운영도 가능 | 활발 (push 2026-07-24, ★35,638) | 2026-07-25 |
| **gVisor** | 컨테이너 격리 커널 | `release-20260721.0` (2026-07-21, 날짜 기반 롤링 릴리스 — GitHub Releases는 미사용, 태그만 발행) | https://github.com/google/gvisor/tags | Apache-2.0 | 유저스페이스 커널로 syscall 가로채기 — microVM보다 가볍고 컨테이너보다 강한 격리 | 매우 활발 (push 2026-07-25, ★18,858) | 2026-07-25 |
| **Docker (moby)** | 컨테이너 런타임 | `docker-v29.6.2` (2026-07-16) | https://github.com/moby/moby/releases/tag/docker-v29.6.2 | Apache-2.0 | 기본 격리 수준. 신뢰할 수 없는 코드에는 단독으로 불충분 | 매우 활발 (push 2026-07-25, ★71,894) | 2026-07-25 |
| **Podman** | 컨테이너 런타임 (rootless) | `v6.0.2` (2026-07-22) | https://github.com/podman-container-tools/podman/releases/tag/v6.0.2 | Apache-2.0 | 데몬리스·rootless가 기본 | 활발 (push 2026-07-24, ★32,360). **레포가 `containers/` → `podman-container-tools/`로 이전됨** | 2026-07-25 |
| **Wasmtime** | WebAssembly 런타임 | `v47.0.2` (2026-07-21) | https://github.com/bytecodealliance/wasmtime/releases/tag/v47.0.2 | Apache-2.0 | capability 기반(WASI) 격리 — 기본이 "아무것도 못 함" | 매우 활발 (push 2026-07-25, ★18,420). 메이저 버전 47 = 월간 메이저 배포 | 2026-07-25 |
| **WasmEdge** | WebAssembly 런타임 | `0.17.1` (2026-07-06) | https://github.com/WasmEdge/WasmEdge/releases/tag/0.17.1 | Apache-2.0 | 엣지·서버리스 지향 Wasm 런타임 (CNCF) | 활발 (push 2026-07-25, ★10,740) | 2026-07-25 |
| **Javy** | JS→Wasm 툴체인 | `v9.0.0` (2026-06-12) | https://github.com/bytecodealliance/javy/releases/tag/v9.0.0 | Apache-2.0 | 에이전트가 만든 JS를 Wasm으로 격리 실행하는 경로 | 완만 (push 2026-07-06, ★2,710) | 2026-07-25 |

**런타임 표 소계: 14개 행 (프로젝트 14개)**

---

## 5. 설계 철학 · 언제 무엇을 고르나 [축 6] 원재료, [축 2]

research-lead가 "용도별 추천 스택"을 합성할 때 쓸 축이다. 각 항목의 근거는 위 표의 1차 소스와 아래 「자료」 섹션.

### 축 1: 명시적 그래프 상태 ↔ 역할 기반 자율 위임

- **LangGraph (명시적 극단).** 공식 정의: *"a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents"*이며 *"mix deterministic, hand-coded steps with LLM-driven agentic steps in the same graph"*가 가능하다고 한다. 상태·노드·엣지·체크포인터를 개발자가 직접 쓴다. **고를 때:** 감사 추적·재개·HITL 승인이 요구사항일 때. 상태 전이를 코드로 설명할 수 있어야 하는 규제 도메인. **대가:** 보일러플레이트. 문서 스스로 초보자에게는 `langchain`의 `create_agent`를 권한다.
- **CrewAI (역할 위임 극단, 단 이원 구조).** Crews는 역할·목표 선언으로 팀을 만들고 위임을 LLM이 결정한다. 그런데 CrewAI는 여기서 멈추지 않고 **Flows**를 별도로 뒀다 — 공식 문서 기준 Flows는 *"event-driven workflows requiring state management, conditional branching, human oversight, or orchestration across multiple crews"*용이며 `@start`·`@listen`·`@router`·`@persist` 프리미티브를 쓴다. **즉 CrewAI 자신이 "자율 위임만으로는 프로덕션이 안 된다"를 제품 구조로 인정한 셈이다.** 이 관찰이 축 6에서 강력한 논거가 된다.
- **Microsoft Agent Framework (양쪽을 표로 갈라놓음).** 공식 문서가 대놓고 표를 제공한다 — 에이전트는 "open-ended or conversational / autonomous tool use and planning", 워크플로는 "well-defined steps / explicit control over execution order / multiple agents must coordinate". 그리고 못을 박는다: *"If you can write a function to handle the task, do that instead of using an AI agent."* → **이 한 문장이 이 책의 축 1 또는 첫 챕터 오프닝으로 쓸 만하다.**
- **Google ADK (템플릿 중간항).** 완전 자율(LlmAgent)과 완전 명시(그래프) 사이에 **Sequential / Parallel / Loop** 3종 템플릿 워크플로 에이전트를 둔다. 2.0부터 그래프 워크플로도 추가. **고를 때:** "그래프까지는 과하고 자율은 불안한" 다수 사례. GCP 배포(Agent Runtime·Cloud Run·GKE)가 이미 정해진 조직.

### 축 2: 언어·타입 시스템 정합성 (백엔드 개발자에게 가장 실질적인 선택 기준)

- **Pydantic AI** — 타입 안전과 의존성 주입. FastAPI/Pydantic 스택이면 학습 곡선이 거의 없다. v2.18.0으로 성숙.
- **Mastra** — TS 네이티브 풀스택(에이전트+워크플로+RAG+eval+로컬 playground). Node/Next.js 팀의 기본값 후보.
- **Google ADK** — **Python·TypeScript·Go·Java·Kotlin 5개 언어.** JVM 백엔드 팀이 언어를 바꾸지 않고 들어갈 수 있는 사실상 유일한 대형 선택지(adk-java v1.7.0).
- **Microsoft Agent Framework** — .NET·Python·Go(preview). C# 조직의 답.
- **Agno / smolagents / DSPy** — Python 전용.

### 축 3: SDK ↔ harness (2026년의 새 층)

여기가 이번 리서치의 가장 신선한 발견이다. "프레임워크를 고른다"가 더 이상 마지막 결정이 아니다.

- **SDK 층**: 루프·도구 호출·핸드오프만 제공 (OpenAI Agents SDK — 원시 개념 5개, *"very few abstractions"*).
- **harness 층**: 여기에 계획·todo 추적·컨텍스트 압축·파일/메모리 접근·도구 승인 정책·관측을 **미리 조립해서** 준다.
  - `deepagents` — "The batteries-included agent harness" (LangGraph 위).
  - **Strands Harness** — 레포 자체가 `harness-sdk`로 개명. AWS가 *"Built from production systems inside Amazon"*이라 소개.
  - **Microsoft Agent Framework의 Harness** — 공식 설명: *"An opinionated agent with batteries-included capabilities for long, multi-step tasks — planning and todo tracking, context compaction, file access and memory, don't-ask-again tool approval, and observability."*
  - **Claude Agent SDK** — Claude Code의 harness를 그대로 라이브러리화한 형태.
- **고를 때:** 긴 다단계 작업(코딩 에이전트·리서치 에이전트)이면 harness부터 본다. 짧은 도구 호출 1~3회짜리면 SDK만으로 충분하고 harness는 오히려 비용·지연을 늘린다.

### 축 4: 신뢰성을 어디서 얻나 — 프레임워크 내장 ↔ 외부 durable execution

- **프레임워크 내장**: LangGraph 체크포인터, CrewAI `@persist()`, Cloudflare Durable Objects(Agents SDK), Agent Framework 워크플로 체크포인팅.
- **외부 위임**: Temporal / Restate / DBOS / Inngest / Cloudflare Workflows에 에이전트 스텝을 태운다.
  - **Temporal**의 공식 정의: *"Durable Execution ensures that your application behaves correctly despite adverse conditions by guaranteeing that it will run to completion."* 메커니즘은 이벤트 히스토리 + 리플레이, 대가는 **결정론 제약**(워크플로 코드가 재실행 가능해야 함 — LLM 호출은 Activity로 밀어내야 한다는 설계 귀결).
  - **DBOS**는 별도 오케스트레이터 없이 **Postgres 하나로** 같은 보장을 라이브러리로 제공한다 → 이미 Postgres를 쓰는 백엔드 팀에게 운영 부담이 가장 낮은 경로.
  - **Restate**는 단일 바이너리로 durable 실행+상태+통신을 묶어 Temporal보다 운영 진입 장벽을 낮추는 포지션.
- **판단 기준 초안:** 에이전트 실행이 (a) 분 단위를 넘고 (b) 외부 부작용(결제·발송·쓰기)을 만들고 (c) 중간 실패 후 재개해야 하면 → 외부 durable execution. 그 외에는 프레임워크 내장 체크포인터로 충분.

### 축 5: 격리 강도 ↔ 시작 지연 (실행환경 선택의 유일한 진짜 트레이드오프)

강한 격리부터: **microVM (Firecracker — Vercel Sandbox·Fly Machines·E2B 계열)** > **유저스페이스 커널 (gVisor)** > **컨테이너 (Docker/Podman)** > **Wasm capability 샌드박스 (Wasmtime/WasmEdge — 격리는 강하나 syscall/생태계 제약이 큼)**.

- 신뢰할 수 없는 **에이전트 생성 코드**를 돌린다면 컨테이너 단독은 불충분하다. Vercel Sandbox는 *"Each sandbox runs in a secure Firecracker microVM with its own filesystem and network"*를 명시하고, Modal Sandbox도 *"secure containers for executing untrusted user or agent code"*로 규정한다. (Modal·E2B의 구체적 격리 기술명은 이번 세션 문서에서 **확인 못 함** — 하단 미확인 목록 참조.)
- Wasm은 "기본이 아무것도 못 함"이라 격리 모델로는 가장 깔끔한데, 에이전트가 만든 코드가 임의 패키지를 설치하려 들면 곧 막힌다. → **에이전트 코드 실행에는 microVM, 플러그인/도구 자체의 격리에는 Wasm**이라는 분업이 현실적.

---

## 6. 공식 레퍼런스 아키텍처 · 스타터 템플릿 [축 6]

| 벤더 | 권장 조합 / 템플릿 | URL | 확인일 |
|------|------------------|-----|--------|
| Cloudflare | `create-cloudflare@latest --template cloudflare/agents-starter` — Agents SDK + Durable Objects + Workflows + Browser/Sandbox/AI Search/MCP 툴 | https://developers.cloudflare.com/agents/ | 2026-07-25 |
| Microsoft | Agent Framework + Microsoft Foundry (`Microsoft.Agents.AI.Foundry`, `pip install agent-framework`, `go get github.com/microsoft/agent-framework-go`). 마이그레이션 가이드 2종(from Semantic Kernel / from AutoGen) 공식 제공 | https://learn.microsoft.com/en-us/agent-framework/overview/ | 2026-07-25 |
| Google | ADK + Agent Runtime(Agent Platform) / Cloud Run / GKE, "native, one-command deployment to Google Cloud". A2A·MCP 내장 | https://adk.dev/ | 2026-07-25 |
| AWS (한국팀) | **Deep Insight** 레퍼런스 구현 — Bedrock AgentCore Runtime(추론) + **Fargate(코드 실행 분리)** + S3(중간 저장·HITL) + Private Subnet/VPC Endpoint(완전 네트워크 격리). Self-Hosted(로컬)와 Managed(프로덕션) 2버전 분리 운영 | 코드: https://github.com/aws-samples/sample-deep-insight / 해설: https://aws.amazon.com/ko/blogs/tech/harness-engineering-from-deep-insight/ | 2026-07-25 |
| OpenAI | Agents SDK + 내장 트레이싱 → OpenAI eval/파인튜닝/distillation 스위트로 연결 | https://openai.github.io/openai-agents-python/ | 2026-07-25 |
| LangChain | 3층 스택: `langgraph`(런타임) → `langchain`/`create_agent` → `deepagents`(harness) | https://docs.langchain.com/oss/python/langgraph/overview | 2026-07-25 |
| Vercel | Sandbox + 멀티에이전트 격리(에이전트별 Linux 사용자 + 그룹 공유) + 영속 샌드박스/스냅샷 | https://vercel.com/docs/sandbox/multi-agent | 2026-07-25 |

> **축 6 합성 힌트 (research-lead용):** 위 7개를 보면 벤더별 "정답 스택"이 사실상 **자기 플랫폼 락인 축**으로 갈린다. 반면 플랫폼 중립 조합은 `Pydantic AI 또는 LangGraph` + `Temporal/DBOS` + `E2B/Modal` + `MCP` 형태로 수렴한다. 이 대비 자체가 챕터 하나 값이다.

---

## 7. 비용 · 지연 · 동시성 — 1차 소스 수치 [축 5], [축 6]

> **이 섹션 전체가 증거 등급 B다** (§0 위의 표 참조). URL은 모두 공식 문서 1차 소스지만, 수치는 WebFetch 요약을 경유했다. **본문에 특정 금액·한도를 박아 넣기 전에 해당 URL을 다시 열어 대조하라.** 요금은 특히 변동이 잦으니 "2026-07 기준" 단서를 함께 쓸 것.

### Cloudflare Workflows (https://developers.cloudflare.com/workflows/reference/limits/, 확인 2026-07-25)

| 항목 | Free | Paid |
|------|------|------|
| 워크플로당 최대 step | 1,024 | 10,000 (기본) → 25,000 설정 가능 |
| step당 최대 재시도 | 10,000 | 10,000 |
| step당 CPU 시간 | 10ms | 30초 (기본) → 5분 설정 가능 |
| step당 wall clock | 무제한 | 무제한 |
| step 결과 크기 | 1MiB (2^20 bytes) | 1MiB |
| 인스턴스당 상태 영속 | 100MB | 1GB |
| 상태 보존 기간 | 3일 | 30일 |
| 최대 sleep | **365일 (1년)** | 365일 |
| 동시 실행 인스턴스 | 100 | **50,000** |
| 큐잉 인스턴스 | 100,000 | 2,000,000 |
| 인스턴스 생성 레이트 | 100/초 | 300/초 (계정), 100/초 (워크플로별) |

핵심: `waiting` 상태 인스턴스는 동시성 한도에 **포함되지 않는다**. → 사람 승인을 며칠 기다리는 에이전트를 수만 개 띄워도 과금·한도 모델이 버틴다.

### Cloudflare Durable Objects (https://developers.cloudflare.com/durable-objects/platform/limits/, 확인 2026-07-25)

- 객체당 SQLite 스토리지 **10GB** (Workers Paid) / KV 백엔드는 무제한
- 요청당 CPU 시간 기본 **30초**, `limits.cpu_ms`로 **5분**까지. *"Each incoming HTTP request or WebSocket message resets the remaining available CPU time to 30 seconds."*
- SQLite 백엔드: 키+값 합계 **2MB** 초과 불가 / KV 백엔드: 키 **2KiB**, 값 **128KiB**
- 객체 개수: 무제한 / WebSocket 수신 메시지 최대 **32MiB**
- SQL 제약: 테이블당 컬럼 100, row/BLOB 2MB, SQL 문 길이 100KB, 바인드 파라미터 100

### Vercel Sandbox (https://vercel.com/docs/sandbox/pricing, 문서 last_updated 2026-06-16, 확인 2026-07-25)

| 항목 | Hobby | Pro | Enterprise |
|------|-------|-----|-----------|
| 최대 실행 시간 | **45분** | **24시간** | 24시간 |
| 동시 샌드박스 | 10 | 2,000 | 2,000+ |
| 최대 vCPU / 메모리 | 4 / 8GB | 8 / 16GB | 32 / 64GB |
| vCPU 할당 레이트 | 40 vCPU / 10분 | 200 vCPU / 분 | 400 vCPU / 분 |
| 컨트롤 플레인 레이트 | 1,000 req/분 | 10,000 req/분 | 100,000 req/분 |
| Active CPU 단가 | 5시간/월 무료 | **$0.128/시간** | $0.128/시간 |
| 프로비저닝 메모리 | 420 GB-시간/월 무료 | **$0.0212/GB-시간** | 동일 |
| 샌드박스 생성 | 5,000/월 무료 | **$0.60 / 1M회** | 동일 |
| 데이터 전송(송신) | 20GB/월 | $0.15/GB | 동일 |

- 기본 timeout **5분** (`timeout` 옵션, `sandbox.extendTimeout()`로 연장). 기본 **2 vCPU**, vCPU당 **2GB** 메모리. 디스크는 전 플랜 **32GB** ephemeral NVMe. 열 수 있는 포트 15개.
- **I/O 대기 시간은 Active CPU로 과금되지 않는다** — *"Time spent waiting for I/O (such as network requests, database queries, or AI model calls) does not count toward Active CPU."* → LLM 응답을 기다리는 에이전트에 유리한 과금 모델. 이건 책에서 짚을 만한 비직관적 사실이다.
- 공식 예시 원가: 5분/2vCPU AI 코드 검증 ≈ **$0.03**, 30분/4vCPU 빌드+테스트 ≈ **$0.34**, 2시간/8vCPU ≈ **$2.73** (100% CPU 사용 가정).
- 스냅샷 기본 만료 **최종 사용 후 30일**. 리전은 현재 **`iad1` 전용**.
- 시작: *"Sandboxes start in milliseconds"* (구체 수치는 문서 미제시).

### E2B (https://e2b.dev/docs/sandbox/persistence, 확인 2026-07-25)

- 연속 실행 한도: **Pro 24시간 / Hobby 1시간**. 기본 timeout **5분**(설정 가능).
- **pause ≈ 1GiB RAM당 4초**, **resume ≈ 1초**. pause된 샌드박스는 **무기한 보존**(자동 만료 없음), `kill()`로만 종료. 파일시스템 + 메모리 상태 모두 보존. **pause/resume 후 연속 실행 한도가 리셋된다** → 24시간 한도를 사실상 우회하는 운영 패턴.

### Modal Sandbox (https://modal.com/docs/guide/sandbox, 확인 2026-07-25)

- 기본 최대 수명 **5분**, `timeout` 파라미터로 **최대 24시간**. 유휴 timeout 옵션 있음.
- 수명주기 5단계: Created → Scheduled → Started → Ready(옵션) → Finished.
- 콜드 스타트 수치·격리 기술·동시성 한도는 이 페이지에 **없음**(미확인).

### Modal 요금 (https://modal.com/pricing, 확인 2026-07-25) ⚠️요약경유

**Sandbox는 일반 컴퓨트보다 요율이 3배 비싸다** — 이건 축 6 스택 비교에서 놓치면 안 되는 비직관적 사실이다.

| 항목 | 일반 컴퓨트 (Standard) | **Sandbox + Notebooks** |
|------|----------------------|------------------------|
| CPU | `$0.0000131 / core / sec` | **`$0.00003942 / core / sec`** (약 3.0배) |
| 메모리 | `$0.00000222 / GiB / sec` | **`$0.00000667 / GiB / sec`** (약 3.0배) |

- 1 core = 물리 코어 = **2 vCPU 상당**, 최소 할당 **0.125 core**. 볼륨 `$0.09/GiB/월` (월 1TiB 무료).
- GPU(초당): B300 `$0.001972` / H100 `$0.001097` / A100 80GB `$0.000694` / L4 `$0.000222` / T4 `$0.000164`
- 플랜: **Starter** $0 + 컴퓨트, 크레딧 $30/월, 컨테이너 **100개**, GPU 동시성 10, 시트 3 / **Team** $250 + 컴퓨트, 크레딧 $100/월, 컨테이너 **1,000개**, GPU 동시성 50, 시트 무제한 / **Enterprise** 커스텀
- **Vercel Sandbox와의 대조 (축 6용 환산):** Modal Sandbox CPU `$0.00003942/core/sec` × 3600 = **약 $0.142/core-시간**(= 2 vCPU 기준). Vercel은 **Active CPU만** `$0.128/시간`으로 과금하고 **I/O 대기는 미과금**. → LLM 응답 대기가 지배적인 에이전트(위 AWS 실측: 추론이 코드 실행의 61배)에서는 **과금 모델의 차이가 요율 차이보다 크게 작용한다.** 이 대비가 이 책의 비용 챕터 핵심 논거가 될 수 있다.
  > ⚠️ 위 환산은 **이 문서가 직접 계산한 값**이며 어느 벤더도 공표하지 않았다. 과금 단위(core vs vCPU, Active CPU vs wall clock)가 서로 달라 완전한 등가 비교가 아니다. 본문에 쓸 때는 반드시 이 단서를 붙일 것.

### AWS Deep Insight 실측치 (2차 소스 — AWS Korea 기술블로그, 2026-04-22)

프로덕션 멀티에이전트 1세션 실측. **비용·지연 감각을 주는 유일한 실측 세트라 가치가 높지만, 벤더 블로그(2차)임을 본문에 표시해야 한다.**

| 항목 | 수치 |
|------|------|
| 세션 분석 시간 | 22.5분 |
| 처리 거래 건수 | 830건 |
| Fargate 실행 횟수 | 79회 |
| 순수 코드 실행 시간 | **19.8초** |
| **LLM 추론 시간 / 코드 실행 시간** | **61배** |
| 세션당 추정 비용 | **$4.13 USD** |
| 그중 Bedrock 토큰 비용 비중 | **약 98%** |
| 산출 리포트 크기 | 1.3MB (DOCX) |

→ **"에이전트 비용은 사실상 토큰 비용이다(98%). 컴퓨팅 최적화는 두 번째 문제다"**는 이 책의 운영 챕터에서 반복해서 쓸 수 있는 수치다.

---

## 8. 원리 축 — 공식 문서의 정의만 [축 1]

학술 계보는 paper-researcher 담당. 여기는 **벤더 공식 문서가 뭐라고 정의했는지**만 인용 가능한 형태로 모았다.

### 자료 1: Anthropic — Building effective agents
- 출처: https://www.anthropic.com/engineering/building-effective-agents
- 저자·날짜: Anthropic Engineering, **2024-12-19** (⚠️ **1년 7개월 경과 — 프레임워크 언급 부분은 구버전 정보일 수 있음. 단 정의·패턴 분류는 업계 표준으로 계속 인용된다**)
- 신뢰성: **최상** (1차·벤더 공식)
- 인용 가능한 구절 (정의 원문):
  - Workflows: *"Systems where LLMs and tools are orchestrated through predefined code paths."*
  - Agents: *"Systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."*
- 워크플로 패턴 5종 (이 분류가 업계 공용어가 됐다): prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer
- 판단 기준: 워크플로는 예측 가능한 고정 서브태스크·일관성 우선. 에이전트는 단계를 미리 정할 수 없는 열린 문제. 대가는 *"higher costs, and the potential for compounding errors"*이며 *"extensive testing in sandboxed environments, along with appropriate guardrails"*를 요구.
- 총괄 지침: *"Start with simple prompts"*, 단순한 해법이 부족할 때만 복잡도를 더한다.
- 관련 섹션: **1장(에이전트란 무엇인가) / 축 1 정의 절**. 이 책 전체의 개념 정초로 쓸 1순위 인용.

### 자료 2: Microsoft — Agent Framework Overview
- 출처: https://learn.microsoft.com/en-us/agent-framework/overview/
- 저자·날짜: Microsoft Learn, `ms.date` **2026-07-08**, updated **2026-07-10**
- 신뢰성: **최상** (1차·벤더 공식, 최신)
- 인용 가능한 구절:
  - *"If you can write a function to handle the task, do that instead of using an AI agent."*
  - *"The Agent Framework is the direct successor, created by the same teams. ... In short, Agent Framework is the next generation of both Semantic Kernel and AutoGen."*
  - Harness 정의: *"An opinionated agent with batteries-included capabilities for long, multi-step tasks — planning and todo tracking, context compaction, file access and memory, don't-ask-again tool approval, and observability."*
- 3대 기능 축: **Agents / Harness / Workflows**. 기반 블록: model clients, agent session(상태), context providers(메모리), middleware(가로채기), MCP clients(도구).
- 에이전트 vs 워크플로 판단 표(공식): 에이전트 = 열린/대화형·자율 도구 사용과 계획·단일 LLM 호출로 충분 / 워크플로 = 단계가 정의됨·실행 순서 명시 제어·다수 에이전트 조율 필요.
- 관련 섹션: **1장(정의)·프레임워크 서베이 장(AutoGen 사망 진단)·harness 장**. Anthropic 정의와 나란히 놓으면 "두 벤더가 같은 결론에 도달했다"는 서술이 가능.

### 자료 3: Temporal — Understanding Temporal (Durable Execution)
- 출처: https://docs.temporal.io/evaluate/understanding-temporal
- 저자·날짜: Temporal 공식 문서 (발행일 표기 없음 — 상시 갱신 문서)
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: *"Durable Execution ensures that your application behaves correctly despite adverse conditions by guaranteeing that it will run to completion."*
- 핵심 개념: Workflow(코드로 쓰인 비즈니스 로직) / Activity(외부 상호작용 단위, 자동 재시도) / Event History(모든 단계의 영속 로그) / Replay(워커 크래시 후 히스토리로 상태 재구성) / 결정론 제약. 문서 비유: *"the ultimate autosave."*
- ⚠️ 이 페이지는 **AI 에이전트를 언급하지 않는다**. "Temporal이 에이전트용으로 만들어졌다"고 쓰면 사실 오류. 에이전트 적용은 커뮤니티/응용 층의 이야기다.
- 관련 섹션: **운영·신뢰성 장 / 축 5**.

### 자료 4: LangChain — LangGraph Overview (1.x)
- 출처: https://docs.langchain.com/oss/python/langgraph/overview
- 저자·날짜: LangChain 공식 문서 (상시 갱신, 1.x 기준)
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: *"a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents"* / *"mix deterministic, hand-coded steps with LLM-driven agentic steps in the same graph"* / *"you don't need to use LangChain to use LangGraph"*
- 3층 구조 명시: LangGraph(저수준 런타임) / LangChain agents(*"prebuilt architectures for common LLM and tool-calling loops"*, 초보자 권장) / Deep Agents(*"a higher harness layer adding planning, subagents, and context management atop LangGraph"*)
- 핵심 개념: `StateGraph`, `MessagesState`, `add_node`, `START`/`END` 엣지, 컴파일→invoke, persistence(실패 후 재개), HITL interruption, memory, durable execution, streaming, time travel
- 관련 섹션: **프레임워크 서베이 장(LangChain vs LangGraph 혼란 해소)·harness 장**.

### 자료 5: MCP Specification (현행 리비전 2025-11-25)
- 출처: https://modelcontextprotocol.io/specification/latest
- 저자·날짜: MCP 프로젝트, 리비전 **2025-11-25** (현행 latest, 2026-07-25 확인)
- 신뢰성: **최상** (스펙 1차)
- 아키텍처: JSON-RPC 2.0, 상태 유지 연결, 능력 협상(capability negotiation). 3역할 — **Hosts**(연결을 시작하는 LLM 앱) / **Clients**(호스트 내 커넥터) / **Servers**(컨텍스트·능력 제공).
- 서버가 제공: **Resources**(컨텍스트·데이터) / **Prompts**(템플릿 메시지·워크플로) / **Tools**(모델이 실행하는 함수)
- 클라이언트가 제공: **Sampling**(서버 주도 재귀 LLM 호출) / **Roots**(URI·파일시스템 경계) / **Elicitation**(서버 주도 추가 정보 요청)
- 유틸리티: 설정, 진행 추적, 취소, 에러 보고, 로깅
- 인용 가능한 보안 구절: *"Tools represent arbitrary code execution and must be treated with appropriate caution."* / *"descriptions of tool behavior such as annotations should be considered untrusted, unless obtained from a trusted server."*
- 설계 계보: 스펙 스스로 **Language Server Protocol(LSP)**에서 영감을 얻었다고 밝힌다 → 백엔드 개발자에게 MCP를 설명하는 최적의 비유.
- 관련 섹션: **도구 호출 프로토콜 장 / 축 1**. Sampling·Elicitation은 대부분의 한국어 자료가 빠뜨리는 클라이언트 측 기능이라 차별점이 된다.

### 자료 6: A2A Protocol Specification v1.0.0
- 출처: https://a2a-protocol.org/latest/specification/
- 저자·날짜: a2aproject 커뮤니티, **v1.0.0** (GitHub 릴리스 2026-05-28)
- 신뢰성: **최상** (스펙 1차)
- 핵심 개념(원문 인용): **Agent Card** — *"A JSON metadata document published by an A2A Server, describing its identity, capabilities, skills, service endpoint, and authentication requirements"*; **Task** — *"The fundamental unit of work managed by A2A, identified by a unique ID. Tasks are stateful and progress through a defined lifecycle"*; **Message** — role은 "user"/"agent", 하나 이상의 `Parts` 포함; **Artifact** — 에이전트 산출물; **Streaming**(SSE); **Push Notifications** — *"server-initiated HTTP POST requests to a client-provided webhook URL"*
- 바인딩 3종: JSON-RPC 2.0 / gRPC / HTTP+JSON(REST)
- 설계 목표: 내부 상태·도구에 접근하지 않고 **opaque한** 에이전트끼리 상호운용.
- **MCP와의 대비(책에서 반드시 구분해야 하는 지점):** MCP = 에이전트↔도구/컨텍스트(수직). A2A = 에이전트↔에이전트(수평). 둘은 경쟁이 아니라 직교하며, Google ADK는 양쪽을 동시에 내장한다.
- 관련 섹션: **도구 호출 프로토콜 장 / 멀티에이전트 장 / 축 1**.

### 자료 7: OpenAI Agents SDK 공식 문서
- 출처: https://openai.github.io/openai-agents-python/
- 저자·날짜: OpenAI 공식 문서 (상시 갱신)
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: *"build agentic AI apps in a lightweight, easy-to-use package with very few abstractions"* / 에이전트 루프 정의 — *"a built-in agent loop that handles tool invocation, sends results back to the LLM, and continues until the task is complete"* / Swarm 관계 — *"a production-ready upgrade of our previous experimentation for agents, Swarm"*
- 원시 개념 5개: **Agents, Handoffs, Guardrails, Sessions, Runner** + 내장 트레이싱
- 관련 섹션: **1장 에이전트 루프 정의(가장 간결한 공식 정의)·프레임워크 서베이 장**.

### 자료 8: AGENTS.md
- 출처: https://agents.md/
- 저자·날짜: Agentic AI Foundation (**Linux Foundation 산하**) 스튜어드. 버전·발행일 표기 없음
- 신뢰성: **최상** (규약 1차 사이트)
- 인용 가능한 구절: *"a README for agents: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project."*
- 채택 규모: **60k+ 오픈소스 프로젝트**, **60개+ 도구** 지원. 명시된 벤더/도구: OpenAI Codex, Google Jules·Gemini CLI, Cognition Devin·Windsurf, Anthropic Claude, GitHub Copilot, JetBrains Junie, Cursor, Factory, Aider, VS Code, Zed, Warp, UiPath 외.
- 포지셔닝: README는 사람용으로 간결히, AGENTS.md는 에이전트용 상세 컨텍스트. (사이트 본문은 CLAUDE.md를 언급하지 않는다 — "CLAUDE.md를 대체한다"고 쓰면 근거 없음.)
- 관련 섹션: **도구 호출 프로토콜/규약 장 · harness 장**. 독자가 당장 자기 레포에 적용할 수 있는 유일한 "오늘 할 일"이라 실천 절로 좋다.

### 자료 9: Google ADK 공식 사이트
- 출처: https://adk.dev/ (구 `google.github.io/adk-docs`에서 **301 리다이렉트** — 낡은 URL 인용 주의)
- 저자·날짜: Google 공식 (상시 갱신)
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: *"the open-source agent development framework that lets you build, debug, and deploy reliable AI agents at enterprise scale"* / 배포 — *"native, one-command deployment to Google Cloud"*
- 언어 5종: Python, TypeScript, Go, Java, Kotlin. 모델은 *"almost any generative AI model"* (Gemini 네이티브 + 타 제공자 어댑터 + 로컬 모델)
- 워크플로: sequential / loop / parallel 템플릿 + **2.0부터 그래프 기반 워크플로**
- 구성요소: custom tools, MCP tools, OpenAPI tools, skills, sessions, memory, artifacts. 배포 대상: Agent Runtime(Agent Platform), Cloud Run, GKE. **A2A·MCP 양쪽 지원.**
- 관련 섹션: **프레임워크 서베이 장(다언어·엔터프라이즈 축)·축 6**.

### 자료 10: CrewAI Flows 공식 문서
- 출처: https://docs.crewai.com/en/concepts/flows
- 저자·날짜: CrewAI 공식 문서 (상시 갱신, 1.x 기준)
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: Flows는 *"A powerful feature designed to streamline the creation and management of AI workflows. Flows allow developers to combine and coordinate coding tasks and Crews efficiently"*
- Crews vs Flows 판단: Crews = 명확한 목표를 가진 정의된 태스크를 에이전트가 수행하는 자기완결 단위. Flows = 이벤트 기반, 상태 관리·조건 분기·사람 감독·복수 Crew 조율이 필요할 때.
- Flow 프리미티브: `@start()`, `@listen()`, `@router()`, 상태 관리(비구조/Pydantic BaseModel 구조), `@persist()`(재시작 간 상태 복구)
- 관련 섹션: **프레임워크 서베이 장 · 축 1(자율 위임의 한계)**. "역할 기반 자율 위임의 대표 프레임워크가 스스로 명시적 워크플로 층을 추가했다"는 논거의 근거.

### 자료 11: Cloudflare Agents 공식 문서
- 출처: https://developers.cloudflare.com/agents/
- 저자·날짜: Cloudflare 공식 문서 (상시 갱신)
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: *"each agent session has a durable identity, local SQL storage, real-time connections, scheduled work, and recoverable execution"* / Workers 대비 추가분 — *"state, sessions, routing, WebSockets, scheduling, fibers, and observability"*
- 스타터: `create-cloudflare@latest --template cloudflare/agents-starter`. 내장 도구: Browser, Sandbox, AI Search, MCP, Payments. 모델은 OpenAI·Anthropic·Gemini 등 자유.
- ⚠️ Durable Objects가 상태를 어떻게 뒷받침하는지는 이 페이지가 **명시하지 않는다**(패키지가 DO 위에 서는 건 별도 문서). "이 페이지가 DO 기반이라고 말한다"고 인용하면 부정확.
- 관련 섹션: **실행환경 장(프레임워크와 런타임이 분리되지 않는 설계) / 축 5·6**.

### 자료 12: Vercel Sandbox 공식 문서
- 출처: https://vercel.com/docs/sandbox (문서 last_updated **2026-06-30**)
- 저자·날짜: Vercel 공식
- 신뢰성: **최상** (1차)
- 인용 가능한 구절: *"Each sandbox runs in a secure Firecracker microVM with its own filesystem and network."* / *"Sandboxes start in milliseconds."*
- 특징: Amazon Linux 2023, 런타임 `node26`/`node24`(기본)/`node22`/`python3.13`, `vercel-sandbox` 사용자 + sudo, 작업 디렉터리 `/vercel/sandbox`. **영속 샌드박스가 기본값**(stop 시 자동 저장·재개), 스냅샷, 태그, Drives(베타), **멀티에이전트 격리**(에이전트별 Linux 사용자 + 그룹으로 파일 공유), Docker·VPN·FUSE 같은 시스템 특권 프로세스 실행 가능.
- 관련 섹션: **실행환경 장 / 축 5**. "멀티에이전트를 OS 사용자 단위로 격리"는 다른 벤더에 없는 구체적 설계라 인용 가치 높음.

---

## 9. 한국어 자료 (대상 독자 = 한국 백엔드/테크리드) [축 5], [축 6]

### 자료 13: 우아한형제들 — 하네스 엔지니어링(harness engineering)으로 팀 맞춤형 AI 환경 구축하기
- 출처: https://techblog.woowahan.com/26177/
- 저자·날짜: **이재홍, 2026-04-17**
- 신뢰성: **중** (회사 엔지니어링 블로그 — 저자 확인됨, 1차 소스는 아님)
- 핵심 주장: 프롬프트 개인 역량이 아니라 **팀 규약을 AI 환경에 구조화**하는 것이 성능을 가른다. Cursor의 Rules(코딩 컨벤션 전달)와 Skills(워크플로 자동화)로 팀 전용 하네스를 구성.
- 인용 가능한 구절:
  - *"AI가 길을 잃지 않고 안정적으로 일할 수 있도록 외부 통제 환경을 구축하는 것을 의미합니다."*
  - *"최근 업계에서 이를 '하네스 엔지니어링(harness engineering)'이라고 부르며 중요성을 강조하고 있는 것도 같은 맥락일 것입니다."*
- 수치 **✅원문확인** (2026-07-25 재fetch로 원문 문장 대조 완료):
  - 원문: *"프로젝트 환경을 기준으로는 AI가 처리해야 할 데이터량이 평균 96.5% 절감되었습니다."*
  - 원문: *"(1회 작업당 평균 약 6,800 토큰 절감 예상)"*
  - 원문 표의 규모별 실측 — 대규모 **41,944 bytes → 1,763 bytes** / 중규모 **29,386 bytes → 668 bytes** / 소규모 **9,749 bytes → 539 bytes**
  - 호출 횟수: 표의 모든 도메인 규모에서 **4회 → 1회**
  - 🔴 **정정 이력:** 이 문서의 최초 판은 위 3행 표를 "약 20,000 bytes → 약 1,000 bytes"로 뭉갠 값을 실었다(WebFetch 요약 아티팩트). **그 값은 원문에 존재하지 않는다.** 본문에 바이트 수치를 쓸 때는 위 3행 중 하나를 그대로 쓰거나 "평균 96.5% 절감"만 인용하라.
- 도구: Cursor IDE(Rules/Skills), Node.js 전처리 스크립트, openapi-typescript.
- 관련 섹션: **컨텍스트 엔지니어링 / harness 장 / 도구 설계 장**. 한국 독자에게 "우리 회사도 이러고 있다"는 근접성을 주는 오프닝 소재. 수치가 구체적이라 인용 가치 높음.

### 자료 14: AWS Korea — 하네스 엔지니어링으로 본 Deep Insight: 로컬 개발에서 프로덕션 운영까지의 설계 여정
- 출처: https://aws.amazon.com/ko/blogs/tech/harness-engineering-from-deep-insight/
- 저자·날짜: Yoonseo Kim, Jesam Kim, Jiyun Park, Kyutae Park Ph.D., Gonsoo Moon, Chloe Kwak — **2026-04-22**
- 신뢰성: **중** (벤더 기술블로그. 단 실측 수치를 공개하고 코드가 공개돼 검증 가능 → 이 등급 내 상위)
- 핵심 주장: 프로덕션 멀티에이전트의 성패는 모델이 아니라 **실행 환경 설계**(격리·중간 저장소·네트워크 경계)에서 갈린다.
- 인용 가능한 구절:
  - 하네스 정의: *"에이전트가 실행되는 제어 환경과 규칙 모음을 말합니다. 마구(馬具)처럼 에이전트의 행동을 묶고, 방향을 잡고, 안전하게 제어하는 구조입니다."*
  - 격리 근거: *"에이전트가 생성한 코드를 Runtime 내부에서 그대로 실행하면 악성코드나 무한루프가 같은 세션에서 돌고 있는 에이전트 로직에 영향을 줄 수 있습니다."*
- 3대 설계 결정: ① **코드 실행 환경 분리**(AWS Fargate — 측정 결과 LLM 추론 시간이 코드 실행 시간의 **61배**) ② **S3 중간 저장소**(분산 데이터 허브 + HITL 피드백) ③ **완전 네트워크 격리**(Private Subnet + VPC Endpoint/PrivateLink + Security Groups, 퍼블릭 인터넷 미경유)
- 사용 서비스: Bedrock AgentCore Runtime, Fargate, ALB, S3, VPC Endpoints/PrivateLink, CloudWatch Logs, ECR
- 실측치 **⚠️요약경유** (원문 문장 대조 미완 — 인용 전 재확인 필요): 세션 22.5분 / 830건 처리 / Fargate 79회 / 순수 코드 실행 19.8초 / **세션당 $4.13** / **Bedrock 토큰이 비용의 약 98%** / 리포트 1.3MB DOCX. 특히 "61배"와 "98%"는 이 책에서 반복 인용될 가치가 큰 수치이므로 **저술 전에 원문 문장을 확보해 둘 것.**
- 인상적 사례: 검증 에이전트가 **2회 실패 후 스스로 진단 스크립트를 작성해 3회째 자력 복구**(인간 개입 없음) → reflection/self-correction의 실무 일화로 축 1에 쓸 수 있다.
- 코드: https://github.com/aws-samples/sample-deep-insight (한국어/영문 워크숍 제공)
- 관련 섹션: **실행환경 장(최고 우선순위 사례) / 운영·비용 장 / 축 5·6**. 한국어로 된 프로덕션 실측 데이터가 이 정도 구체성으로 공개된 사례는 드물다.

### 자료 15: LY Corporation — 멀티 에이전트 협업으로 재설계하는 개발 프로세스 (Tech-Verse 2026)
- 출처: https://techblog.lycorp.co.jp/ko/techverse2026-219
- 저자·날짜: LY Corporation Tech-Verse 2026 세션 (한국어판). **정확한 발행일 미확인**
- 신뢰성: **중** (컨퍼런스 세션 기록 — 본문 미검증, 검색 스니펫 기준)
- 핵심 주장: 조율 과정을 **'제안자(proposer)' vs '도전자(challenger)'** 전문가 간 단계적 토론 구조로 재설계해 산출물을 만든다.
- ⚠️ **본문을 직접 fetch하지 않았다.** 내용 인용 전에 원문 확인 필요 — 하단 「수집 한계」 참조.
- 관련 섹션: **멀티에이전트 패턴 장(적대적/토론 패턴) / 축 1**.

---

## 10. fact-checker를 위한 "자주 틀리는 주장" 대조표

본문에 아래 형태의 문장이 나오면 이 표와 대조하라.

| 흔한 (틀린) 서술 | 2026-07-25 확인된 사실 |
|---|---|
| "AutoGen은 Microsoft의 대표(최신 권장) 에이전트 프레임워크다" | ❌ 최신 릴리스 2025-09-30(`python-v0.7.5`), 마지막 push 2026-04-15. 공식 후속은 Microsoft Agent Framework(`1.12.1`) |
| "AutoGen은 개발이 중단됐다 / 종료됐다 / deprecated다" | ⚠️ **근거 없음.** 레포 `archived: false`, 폐기 공지 없음. 쓸 수 있는 건 "공식 후속이 있다" + "릴리스 10개월 정지"까지 |
| "Swarm은 폐기됐다" | ⚠️ 같은 이유로 과한 서술. "교육용 실험이며 Agents SDK가 공식 후속"까지가 근거 있는 범위 |
| "Semantic Kernel이 Microsoft의 최신 권장" | ❌ SK는 유지보수 중(`dotnet-1.78.0`)이나 공식 후속은 Agent Framework. 마이그레이션 가이드가 공식 제공됨 |
| "MCP 최신 스펙은 2025-06-18" | ❌ 현행 리비전은 **2025-11-25** |
| "LangChain과 LangGraph는 같은 것 / LangGraph는 LangChain이 필요하다" | ❌ 공식 문서: *"you don't need to use LangChain to use LangGraph"* |
| "Pydantic AI / CrewAI / Agno는 아직 0.x 초기 단계" | ❌ 각각 `2.18.0` / `1.15.6` / `2.8.2` |
| "LlamaIndex는 범용 에이전트 프레임워크다" | ⚠️ 자기 정의가 "document agent and OCR platform"으로 이동. 버전도 여전히 `0.14.x` |
| "Strands는 strands-agents/sdk-python에 있다" | ⚠️ 레포가 `strands-agents/harness-sdk`로 개명됨 |
| "Podman은 containers/podman이다" | ⚠️ `podman-container-tools/podman`으로 이전 |
| "ADK 문서는 google.github.io/adk-docs" | ⚠️ `adk.dev`로 301 리다이렉트 |
| "Swarm은 OpenAI의 경량 에이전트 프레임워크다" | ⚠️ 교육용 실험. 공식적으로 Agents SDK가 그 "production-ready upgrade" |
| "Temporal은 AI 에이전트를 위해 만들어졌다" | ❌ 공식 개념 문서는 AI 에이전트를 언급하지 않는다 |
| "E2B/Modal은 Firecracker를 쓴다" | ⚠️ **미확인**. Firecracker 명시 확인된 건 **Vercel Sandbox**뿐 |
| "A2A는 Linux Foundation 프로젝트다" | ⚠️ **미확인**. Linux Foundation 귀속이 확인된 건 **AGENTS.md**(Agentic AI Foundation) |
| "MCP/Restate/Inngest/Daytona는 오픈소스다" | ⚠️ GitHub 라이선스 판정이 `NOASSERTION`/`null` — 단정 금지. 개별 확인 필요 |

---

## 11. 미확인 항목 목록 (research-lead 보고용)

버전·라이선스 셀에서 `미확인`으로 남긴 것 전부. **본문에서 이 값들을 단정하면 fact-checker가 차단해야 한다.**

**버전 미확인 (6건)**
1. ~~**gVisor**~~ — ✅ **해소됨.** `gh api repos/google/gvisor/tags`로 확인: 최신 태그 `release-20260721.0`(2026-07-21). GitHub Releases를 쓰지 않고 날짜 기반 태그만 발행하는 모델. 본문에서 gVisor 버전을 쓸 때는 semver가 아니라 이 날짜 태그 형식이어야 한다.
2. **Cloudflare Workflows** — `미확인 (managed service, 버전 개념 없음)` ✅ 의도된 값
3. **Cloudflare Durable Objects** — `미확인 (managed service, 버전 개념 없음)` ✅ 의도된 값
4. **Fly.io Machines** — `미확인 (managed service, 버전 개념 없음)` ✅ 의도된 값
5. **AWS Bedrock AgentCore Runtime** — `미확인 (managed service, 버전 개념 없음)`. 추가로 **공식 문서를 fetch하지 못했다** (2차 소스만 확보)
6. **AGENTS.md** — 규약에 버전 표기 자체가 없음 (사이트에 version/date 없음)
7. **OpenAI function calling 스펙** — platform.openai.com 문서를 이번 세션에 fetch하지 못함. 버전 태그도 없는 API 스펙

**라이선스 미확인 (8건)**

> 추가 확인(2026-07-25): `gh api repos/{r}/license`로 재조회한 결과 **Restate·Inngest·MCP 스펙 레포는 모두 GitHub가 `"Other"`로 판정**한다 — 즉 표준 SPDX 라이선스가 아닌 **커스텀 라이선스**가 실재한다는 뜻이다(파일 부재가 아님). Daytona는 `/license` 엔드포인트가 404(라이선스 파일 자체를 GitHub가 못 찾음). **따라서 이 4건을 본문에서 "오픈소스"로 서술하면 안 된다.** 정확한 라이선스명은 각 레포의 LICENSE 파일 원문을 읽어야 확정된다.

8. **AutoGen** — GitHub 판정 `CC-BY-4.0` (문서 라이선스로 보임, 코드 라이선스 별도 확인 필요)
9. **Claude Agent SDK (TypeScript)** — GitHub `null`, npm "SEE LICENSE IN README.md"
10. **MCP 스펙 레포** — `NOASSERTION`
11. **MCP Registry** — `NOASSERTION`
12. **MCP TypeScript SDK (레포)** — 레포 `NOASSERTION` / npm 필드는 MIT
13. **Restate (서버)** — `NOASSERTION` (BSL 계열 가능성)
14. **Inngest (서버)** — `NOASSERTION` (SDK는 npm 기준 Apache-2.0)
15. **Daytona** — GitHub `null`
16. **Mastra (레포)** / **Cloudflare Sandbox SDK (레포)** — 둘 다 `NOASSERTION`, npm 필드는 각각 Apache-2.0

**기술 사실 미확인 (5건)**
17. **E2B의 격리 기술** — Firecracker microVM 여부가 fetch한 문서 어디에도 명시되지 않음
18. **E2B 신규 샌드박스 시작 지연(ms)** — 문서에 수치 없음 (pause/resume 수치만 있음)
19. **E2B vCPU/RAM/디스크 한도 + 요금 전체** — `e2b.dev/docs/limits`·`e2b.dev/docs/pricing` 모두 404
20. **Modal Sandbox의 격리 기술·콜드 스타트** — 공식 가이드 페이지에 없음. (동시성은 요금 페이지에서 **확보됨**: Starter 컨테이너 100개 / Team 1,000개)
20b. **durable execution 4종(Temporal·Restate·Inngest·DBOS)의 요금·운영 비용** — 미수집. 축 6 최대 공백
21. **Fly Machines의 격리 기술(Firecracker)·콜드 스타트 수치·CPU/메모리 한도** — `/docs/machines/` 인덱스에 없음 (하위 페이지 필요)
22. **A2A의 Linux Foundation 귀속 여부** — 스펙 사이트는 `a2aproject` 커뮤니티만 명시

---

## 12. 수집 한계 (접근 실패 · 미완 항목)

**HTTP 404로 접근 실패**
- `https://e2b.dev/docs/limits` → 404. E2B의 리소스 한도 표를 확보 못 함. 대체로 `/docs/sandbox`·`/docs/sandbox/persistence`에서 시간 한도만 확보.
- `https://e2b.dev/docs/pricing` → 404. **E2B 요금을 확보하지 못했다.** E2B 문서 사이트가 Mintlify로 이전된 듯하며(`e2b.mintlify.site/llms.txt` 참조 안내가 나옴) 경로 규칙이 바뀐 것으로 보인다. 재시도 경로: `e2b.mintlify.site/llms.txt`로 목차를 먼저 받고 실제 경로 확인, 또는 `e2b.dev/pricing`(docs 하위가 아닌 루트).

**비용 데이터 커버리지 (축 6 관련 — 부분적으로만 채워짐)**
- ✅ 확보: **Vercel Sandbox**(전체 요금표+한도), **Modal**(요율+플랜), **Cloudflare Workflows/Durable Objects**(한도 전체 — 단 요금은 미확보), **AWS Deep Insight**(실측 세션 원가, 2차)
- ❌ 미확보: **E2B 요금**(위 404), **Daytona 요금**, **durable execution 카테고리 전체의 요금·운영 비용**(Temporal Cloud / Restate Cloud / Inngest / DBOS Cloud). 이 카테고리는 "언제 이걸 고르나"가 운영 비용에 가장 크게 좌우되는데 수치가 0건이다. **축 6의 가장 큰 데이터 공백이다.**
- 재시도 경로: `temporal.io/pricing`, `restate.dev/pricing`, `inngest.com/pricing`, `dbos.dev/pricing`, `e2b.dev/pricing`. 후속 리서치 또는 저술 중 보강 대상으로 research-lead에 인계한다.
- `https://strandsagents.com/latest/` → 404. 루트 `https://strandsagents.com/`으로 우회 성공(레포 개명 확인).
- `https://techblog.woowahan.com/23404/` → 404. 검색으로 올바른 URL(`/26177/`) 재탐색 후 성공.

**리다이렉트**
- `https://google.github.io/adk-docs/` → `https://adk.dev/` (301). 재요청으로 해결. **낡은 URL을 인용한 자료가 많으니 본문에는 `adk.dev`를 써야 한다.**

**본문 미확인 (인용 전 확인 필요)**
- **LY Corporation Tech-Verse 2026 세션**(자료 15) — 검색 스니펫만 확보, 본문 fetch 안 함. proposer/challenger 구조 서술을 인용하려면 원문 확인 필수.
- **AWS Bedrock AgentCore 공식 문서** — 미fetch. AgentCore 관련 서술은 현재 AWS Korea 블로그(2차)에만 근거한다.
- **OpenAI function calling 공식 가이드** — 미fetch.

**의도적으로 다루지 않은 영역 (담당 분리)**
- 벡터 DB·임베딩·RAG 데이터 파이프라인 → web-researcher #2 (축 3)
- 평가(eval)·트레이싱/관측 도구(Langfuse·LangSmith·Braintrust 등)·가드레일 → web-researcher #2 (축 4). 단 프레임워크 **내장** 기능으로서의 트레이싱·guardrail 언급은 표에 남겼다(OpenAI Agents SDK의 Guardrails/tracing, Mastra의 eval 등) — #2와 겹칠 수 있으니 research-lead가 병합 시 중복 제거할 것.
- 학술 논문·에이전트 아키텍처 계보 → paper-researcher
- 커뮤니티 여론·실패담 → community-researcher

**커버리지 대비 미수집 (씨앗 목록 중)**
- 씨앗 목록의 항목 중 **표에 넣지 못한 것은 없다.** 다만 `Firecracker`·`gVisor`·`Docker/Podman`·`Wasm 런타임`은 버전·라이선스만 확인했고 **에이전트 문맥에서의 공식 문서 서술은 확인하지 않았다**(이들은 에이전트 전용 도구가 아니므로 1차 문서가 에이전트를 언급하지 않는다).
- 씨앗 목록에 없었으나 **추가한 것**: LangChain(core), deepagents, Microsoft Agent Framework, OpenAI Swarm(폐기 확인용), Cloudflare Agents SDK, MCP Registry, A2A JS SDK, Javy, AWS Bedrock AgentCore(2차 근거), Google ADK Go/Java.

---

## 13. 집계

- **표에 들어간 총 도구 개수: 59개 행 / 고유 프로젝트·서비스 50개**
  - 표 A 프레임워크: **25행** (프로젝트 21개)
  - 표 B 오케스트레이션·durable execution: **12행** (프로젝트 9개)
  - 표 C 도구 호출 프로토콜·규약: **8행** (프로젝트·규약 6개)
  - 표 D 런타임·샌드박스: **14행** (프로젝트 14개)
- **버전이 실제 호출로 확인된 행: 52행** (매니지드 4건 + 규약/스펙 2건 + gVisor 1건은 정당하게 `미확인`)
- **자료(인용 가능 소스) 항목: 15건** — 1차 공식 12건(신뢰성 최상) + 회사/벤더 블로그 3건(신뢰성 중, 그중 한국어 2건)
- **한국어 자료 비중: 15건 중 3건** (우아한형제들, AWS Korea, LY Corporation)
