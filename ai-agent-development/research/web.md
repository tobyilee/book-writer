<!-- 검색 시점: 2026-07-25 기준 -->
# 웹 리서치: AI Agent 개발 (통합)

<!-- 병합 출처: web_frameworks.md (web-researcher #1 — 프레임워크·오케스트레이션·도구호출 프로토콜·런타임/샌드박스)
     + web_data_eval.md (web-researcher #2 — 벡터DB·검색·임베딩·eval/관측성·가드레일·RAG 파이프라인)
     원본 2개 파일도 보존한다. 이 파일은 fact-checker의 1차 대조 근거다. -->

> **버전 열 규율:** 모든 버전·라이선스·활동 신호는 2026-07-25에 `gh api` / PyPI / npm 레지스트리 / 공식 문서 fetch로 실제 확인한 값이다.
> **증거 등급 주의:** 표의 버전·라이선스·날짜 열은 등급 A(결정론적 API 호출). 비용·한도 수치와 블로그 인용문은 등급 B(페이지 요약 경유)로, 인용 전 원문 대조가 필요하다. 상세는 각 파트 상단 참조.

---

# PART 1 — 프레임워크 · 오케스트레이션 · 프로토콜 · 런타임

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


---

# PART 2 — 데이터 · 벡터DB · 임베딩 · 평가 · 가드레일

<!-- 검색 시점: 2026-07-25 기준 -->

# 웹 리서치 (web-researcher #2): 데이터·벡터 DB·임베딩·평가·가드레일

**담당 축:** `[축 3]` 데이터·벡터 DB / `[축 4]` 평가·모니터링·가드레일 / `[축 6]` 용도별 조합의 원재료
**담당 아님:** 프레임워크·런타임·MCP (web-researcher #1)
**대상 독자:** LLM API는 써봤지만 에이전트를 직접 설계·배포·운영해본 적 없는 백엔드/풀스택 개발자·테크리드

## 이 문서의 검증 방법론 (fact-checker 필독)

버전·라이선스·활동 신호 열은 **2026-07-25에 실제 API 호출로 확인한 값**이다. 확인 경로는 셋뿐이다.

- `gh api repos/{owner}/{repo}/releases/latest` → `tag_name`, `published_at`
- `gh api repos/{owner}/{repo}` → `license.spdx_id`, `pushed_at`, `stargazers_count`, `archived`
- `https://pypi.org/pypi/{pkg}/json` → `.info.version` / `https://registry.npmjs.org/{pkg}/latest` → `.version`

확인하지 못한 셀은 **추측하지 않고 `미확인`으로 남겼다.** 문서 하단 "미확인 항목 목록"에 전부 모아두었다. 본문에서 이 셀을 근거로 단정을 쓰면 안 된다.

> **가장 위험한 두 열에 대한 경고**
> 1. **벤치마크 점수** — 대부분의 리더보드(MTEB, SWE-bench, GAIA)는 JS 렌더링이라 정적 fetch로 점수를 못 읽었다. **Terminal-Bench 2.0만 실제 점수를 확보**했다. 나머지는 전부 `미확인`이다. 기억으로 채우지 마라.
> 2. **임베딩 가격** — OpenAI는 **공식 페이지 두 곳이 서로 다른 값을 말한다**(아래 자료 3 참조). Cohere는 현재 가격 페이지에서 토큰 단가를 아예 걷어냈다.

---

## 표 1. 벡터 DB·검색 엔진 `[축 3]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| pgvector | Postgres 확장 | `v0.8.5` (git tag) | https://github.com/pgvector/pgvector | `NOASSERTION` (GitHub API 판정; 실제 라이선스 문구는 미확인) | 이미 쓰는 Postgres에 벡터 타입·인덱스를 더한다 — 새 인프라가 없다 | pushed 2026-07-11, ★22,338. `releases/latest`가 404 (릴리스 미등록, 태그만 운영) | 2026-07-25 |
| pgvectorscale | pgvector 성능 확장 | `0.9.0` (2025-11-04) | https://github.com/timescale/pgvectorscale/releases/tag/0.9.0 | `PostgreSQL` | pgvector에 StreamingDiskANN 인덱스를 얹는다 | pushed 2026-04-30, ★3,097. **릴리스 20개월·푸시 3개월 정체 — 구버전 정보일 수 있음** | 2026-07-25 |
| Qdrant | 전용 벡터 DB | `v1.18.3` (2026-07-17) | https://github.com/qdrant/qdrant/releases/tag/v1.18.3 | `Apache-2.0` | Query API의 `prefetch` 기반 다단계 쿼리 + RRF/DBSF 융합 | pushed 2026-07-25 (당일), ★33,573 | 2026-07-25 |
| Weaviate | 전용 벡터 DB | `v1.38.6` (2026-07-21) | https://github.com/weaviate/weaviate/releases/tag/v1.38.6 | `BSD-3-Clause` | `alpha` 하나로 키워드↔벡터 비중을 조절하는 하이브리드 | pushed 2026-07-25 (당일), ★16,648 | 2026-07-25 |
| Milvus | 전용 벡터 DB | `v2.6.21` (2026-07-24) | https://github.com/milvus-io/milvus/releases/tag/v2.6.21 | `Apache-2.0` | 다중 벡터 필드 동시 ANN + 내장 BM25로 sparse 임베딩 자동 생성 | pushed 2026-07-25 (당일), ★45,373. PyPI `pymilvus` 3.0.0 (2026-05-07) | 2026-07-25 |
| Pinecone | 매니지드 벡터 DB | `미확인 (managed service, 버전 개념 없음)` | https://docs.pinecone.io/guides/index-data/indexing-overview | 상용 (프로프라이어터리) | 서버리스 인덱스 — 운영 부담이 0에 가장 가깝다 | 매니지드. 가격은 표 5 | 2026-07-25 |
| Chroma | 임베디드→서버 벡터 DB | `1.5.9` (2026-05-05) | https://github.com/chroma-core/chroma/releases/tag/1.5.9 | `Apache-2.0` | 프로토타입에서 `pip install`만으로 시작하는 최단 경로 | pushed 2026-07-25 (당일), ★28,873. PyPI `chromadb` 1.5.9 / npm `chromadb` 3.5.0 | 2026-07-25 |
| LanceDB | 임베디드 벡터 DB | Python SDK `0.34.0` (2026-07-02). **GitHub `releases/latest`는 `v0.32.0-beta.3` (프리릴리스)** | https://pypi.org/pypi/lancedb/json · https://github.com/lancedb/lancedb/releases | `Apache-2.0` | Lance 컬럼 포맷 위의 임베디드 DB — 객체 스토리지에 바로 얹힌다 | pushed 2026-07-25, ★10,988. 안정 태그 없이 beta 채널로 굴러가는 릴리스 관행 (`v0.33.0-beta.0`이 최신 태그) | 2026-07-25 |
| Turbopuffer | 매니지드 (객체 스토리지 네이티브) | `미확인 (managed service, 버전 개념 없음)` | https://turbopuffer.com/docs | 상용 | "object-storage native" — 캐시되면 인메모리급, 안 되면 훨씬 싸다 | 매니지드. 공식 문서 주장: "4T+ documents, 10M+ writes/s, 25k+ queries/s" | 2026-07-25 |
| Vespa | 검색+ML 플랫폼 | `v8.719.5` (2026-07-07) | https://github.com/vespa-engine/vespa/releases/tag/v8.719.5 | `Apache-2.0` | 검색·랭킹·ML 추론을 한 엔진에서 — 가장 무겁고 가장 강력 | pushed 2026-07-25 (당일), ★7,029 | 2026-07-25 |
| Elasticsearch | 검색 엔진 (+벡터) | `v9.4.4` (2026-07-21) | https://github.com/elastic/elasticsearch/releases/tag/v9.4.4 | `NOASSERTION` (Elastic License 계열 — SPDX 미판정) | retriever 문법 + RRF로 lexical/vector 하이브리드 | pushed 2026-07-25, ★77,597 | 2026-07-25 |
| OpenSearch | 검색 엔진 (+벡터) | `3.7.0` (2026-06-09) | https://github.com/opensearch-project/OpenSearch/releases/tag/3.7.0 | `Apache-2.0` | Elasticsearch의 Apache-2.0 포크 — 라이선스가 선택 이유 | pushed 2026-07-24, ★13,374 | 2026-07-25 |
| Redis (RediSearch) | 인메모리 (+벡터) | `v2.10.31` (2026-06-17) | https://github.com/RediSearch/RediSearch/releases/tag/v2.10.31 | `NOASSERTION` (RSAL 계열 — SPDX 미판정) | 이미 캐시로 쓰는 Redis에 벡터 인덱스를 겸업 | pushed 2026-07-24, ★6,191 | 2026-07-25 |
| MongoDB Atlas Vector Search | 매니지드 문서 DB (+벡터) | `미확인 (managed service, 버전 개념 없음)` | https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/ | 상용 | 문서 DB 안에서 HNSW/ENN — 최대 8,192차원, 양자화 지원 | 매니지드 | 2026-07-25 |
| sqlite-vec | SQLite 확장 | `v0.1.9` (2026-03-31) | https://github.com/asg017/sqlite-vec/releases/tag/v0.1.9 | `Apache-2.0` | 단일 파일 SQLite에 벡터 검색 — 서버가 아예 없다 | pushed 2026-05-18, ★7,929. **4개월 정체 + 0.1.x 대 버전** | 2026-07-25 |
| FAISS | 라이브러리 (DB 아님) | `v1.14.3` (2026-06-13) | https://github.com/facebookresearch/faiss/releases/tag/v1.14.3 | `MIT` | ANN 알고리즘 라이브러리 — 영속성·필터·API는 직접 짠다 | pushed 2026-07-24, ★40,582. PyPI `faiss-cpu` 1.14.3 | 2026-07-25 |
| Typesense | 검색 엔진 (+벡터) | `v30.2` (2026-04-19) | https://github.com/typesense/typesense/releases/tag/v30.2 | `GPL-3.0` | 오타 허용 즉시 검색이 본업, 벡터는 겸업 | pushed 2026-07-18, ★26,354 | 2026-07-25 |
| Meilisearch | 검색 엔진 (+벡터) | `v1.50.0` (2026-07-20) | https://github.com/meilisearch/meilisearch/releases/tag/v1.50.0 | `NOASSERTION` (MIT 계열 — SPDX 미판정) | DX 우선 검색 엔진, 하이브리드 축 겸비 | pushed 2026-07-24, ★58,722 | 2026-07-25 |

**소계: 18개**

### 하이브리드 검색 구현이 갈리는 지점 (공식 문서 확인분) `[축 3]`

| 엔진 | 융합 방식 | 확인된 세부 | 1차 소스 |
|------|----------|-----------|---------|
| Qdrant | RRF, DBSF | RRF의 `k` 상수 조절 v1.16.0+, 가중 RRF v1.17.0+, Formula Queries v1.14.0+. DBSF는 "3-sigma extremes as endpoints"로 정규화. 리스코어 전용 벡터는 `m=0`으로 HNSW 비활성 권장 | https://qdrant.tech/documentation/concepts/hybrid-queries/ |
| Weaviate | Relative Score Fusion (v1.24부터 기본), Ranked Fusion | `alpha=1`은 순수 벡터, `alpha=0`은 순수 키워드. 키워드 측은 `BM25F`. **기본 alpha 값은 미확인** | https://docs.weaviate.io/weaviate/search/hybrid |
| Milvus | RRF Ranker, Weighted Ranker | 여러 벡터 필드에 ANN 동시 실행 후 병합. **내장 BM25로 텍스트 필드에서 sparse 임베딩 자동 생성**, `SPARSE_FLOAT_VECTOR` + `SPARSE_INVERTED_INDEX` | https://milvus.io/docs/multi-vector-search.md |
| Elasticsearch | RRF | retriever 문법으로 full-text와 vector 쿼리 랭킹 병합. Elastic Cloud Serverless·Elastic Stack 모두 GA. **`rank_constant`/`rank_window_size` 기본값은 해당 페이지에서 미확인** | https://www.elastic.co/docs/solutions/search/hybrid-search |

**책에 쓸 값:** 하이브리드는 "지원한다/안 한다"가 아니라 **융합 알고리즘이 무엇이고 조절 손잡이가 몇 개인가**로 갈린다. Weaviate는 `alpha` 하나(직관적), Qdrant는 prefetch+fusion+formula(표현력 높음), Milvus는 sparse 생성까지 엔진이 대신한다(BM25 파이프라인을 안 짜도 된다).

---

## 표 2. 임베딩 모델 `[축 3]`

**차원·컨텍스트·가격 전부 공식 모델/가격 페이지 확인분이다.** 확인 못 한 셀은 `미확인`.

| 모델 | 제공 형태 | 버전/세대 (2026-07-25 기준) | 차원 | 최대 입력 | 가격 (per 1M tokens) | 1차 소스 | 확인일 |
|------|---------|------------------------|------|---------|-------------------|---------|--------|
| `text-embedding-3-small` | OpenAI API | 3세대 | **1,536** (기본, `dimensions`로 축소 가능) — 가이드 원문: "the length of the embedding vector is `1536` for `text-embedding-3-small`" | **8,192 tokens** (가이드 명시) | **$0.02** (모델 카드) | 차원·입력: https://developers.openai.com/api/docs/guides/embeddings · 가격: https://developers.openai.com/api/docs/models/text-embedding-3-small | 2026-07-25 |
| `text-embedding-3-large` | OpenAI API | 3세대 | **3,072** (기본, 축소 가능) — 가이드 원문: "or `3072` for `text-embedding-3-large`" | **8,192 tokens** (가이드 명시) | **$0.13** (모델 카드). ⚠️ 가격 페이지는 $0.065라는 **포럼 보고**가 있음 — 자료 3 참조 | 차원·입력: https://developers.openai.com/api/docs/guides/embeddings · 가격: https://developers.openai.com/api/docs/models/text-embedding-3-large | 2026-07-25 |
| `text-embedding-ada-002` | OpenAI API | 2세대 (레거시) | `미확인` (가이드에 차원 명시 없음 — 흔히 1,536이라 하나 이번 세션 미확인) | **8,192 tokens** (가이드 명시) | `미확인` | https://developers.openai.com/api/docs/guides/embeddings | 2026-07-25 |
| `embed-v4.0` | Cohere API | v4 | **선택형: 256 / 512 / 1024 / 1536(기본)** | **128k tokens** | `미확인` (가격 페이지에 토큰 단가 없음 — Model Vault 시간당 요금만: Small $4.00/h·$2,500/mo, Medium $5.00/h·$3,250/mo) | https://docs.cohere.com/docs/cohere-embed · https://cohere.com/pricing | 2026-07-25 |
| `embed-english-v3.0` / `embed-multilingual-v3.0` | Cohere API | v3 (레거시) | 1,024 | 512 tokens | `미확인` | https://docs.cohere.com/docs/cohere-embed | 2026-07-25 |
| `embed-*-light-v3.0` | Cohere API | v3 light | 384 | 512 tokens | `미확인` | https://docs.cohere.com/docs/cohere-embed | 2026-07-25 |
| `voyage-4-large` | Voyage API | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.12** | https://docs.voyageai.com/docs/embeddings · https://docs.voyageai.com/docs/pricing | 2026-07-25 |
| `voyage-4` | Voyage API | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.06** | 동일 | 2026-07-25 |
| `voyage-4-lite` | Voyage API | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.02** | 동일 | 2026-07-25 |
| `voyage-4-nano` | **오픈 웨이트** | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | 자체 호스팅 (API 단가 `미확인`) | https://docs.voyageai.com/docs/embeddings | 2026-07-25 |
| `voyage-code-3` | Voyage API | 코드 특화 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.18** | 동일 | 2026-07-25 |
| `voyage-context-4` | Voyage API | 컨텍스트형 | `미확인` | `미확인` | **$0.12** | https://docs.voyageai.com/docs/pricing | 2026-07-25 |
| `gemini-embedding-2` | Google Gemini API | 2세대 | **유연: 128–3072 (권장 768/1536/3072)** | 8,192 tokens | **텍스트 $0.20** / 이미지 $0.45 / 오디오 $6.50 / 비디오 $12.00. Batch API는 "50% of the default Embedding price" | https://ai.google.dev/gemini-api/docs/embeddings · https://ai.google.dev/gemini-api/docs/pricing | 2026-07-25 |
| `gemini-embedding-001` | Google Gemini API | 1세대 | `미확인` | `미확인` | **텍스트 $0.15** | https://ai.google.dev/gemini-api/docs/pricing | 2026-07-25 |
| `jina-embeddings-v5-omni` | Jina API | v5 | Matryoshka (하한 `미확인`) | 32k tokens | `미확인` (무료 체험 10M tokens) | https://jina.ai/embeddings/ | 2026-07-25 |
| `jina-embeddings-v5-text` | Jina API / 오픈 | v5 | Matryoshka, **최소 32차원까지** | 8,192 tokens | `미확인`. small 677M / nano 239M 파라미터 | https://jina.ai/embeddings/ | 2026-07-25 |
| BGE (FlagEmbedding) | 오픈 모델·라이브러리 | `v1.4.0` (2026-04-22) | 모델별 상이 (`미확인`) | 모델별 상이 (`미확인`) | 자체 호스팅 | https://github.com/FlagOpen/FlagEmbedding/releases/tag/v1.4.0 | 2026-07-25 |
| ColBERT (late-interaction) | 오픈 라이브러리 | `v0.2.22` (2025-08-11) | late-interaction (단일 벡터 아님) | `미확인` | 자체 호스팅 | https://github.com/stanford-futuredata/ColBERT/releases/tag/v0.2.22 | 2026-07-25 |
| Nomic Embed | API / 오픈 | `미확인` (문서 URL 404) | `미확인` | `미확인` | `미확인` | 접근 실패 — "수집 한계" 참조 | 2026-07-25 |

**소계: 19개**

### 표 2-1. 리랭커 `[축 3]`

| 모델 | 제공 형태 | 버전 | 컨텍스트 | 가격 (per 1M tokens) | 1차 소스 | 확인일 |
|------|---------|------|---------|-------------------|---------|--------|
| `rerank-v4.0-pro` | Cohere API | v4 | `미확인` | `미확인` (Model Vault: Medium $5.00/h·$3,250/mo, Large $10.00/h·$6,500/mo) | https://docs.cohere.com/docs/rerank | 2026-07-25 |
| `rerank-v4.0-fast` | Cohere API | v4 | `미확인` | `미확인` | 동일 | 2026-07-25 |
| `rerank-v3.5` | Cohere API | v3.5 | **4,096 tokens** | `미확인` | 동일 | 2026-07-25 |
| `rerank-2.5` | Voyage API | v2.5 | `미확인` | **$0.05** | https://docs.voyageai.com/docs/pricing | 2026-07-25 |
| `rerank-2.5-lite` | Voyage API | v2.5 lite | `미확인` | **$0.02** | 동일 | 2026-07-25 |
| BGE reranker | 오픈 (FlagEmbedding) | `v1.4.0` (2026-04-22) | `미확인` | 자체 호스팅 | https://github.com/FlagOpen/FlagEmbedding | 2026-07-25 |
| `rerankers` (통합 래퍼) | 오픈 라이브러리 | `0.6.0` (2024-11-12) | — | 자체 호스팅 | https://github.com/AnswerDotAI/rerankers/releases/tag/0.6.0 | 2026-07-25 |

**소계: 7개** · ⚠️ `rerankers`는 릴리스 2024-11, 푸시 2025-12-20 — **약 20개월 정체, 구버전 정보일 수 있음**

### 표 2-2. MTEB 리더보드 현황 `[축 3]`

| 항목 | 확인된 사실 | 출처 |
|------|-----------|------|
| 패키지 버전 | `2.18.6` (2026-07-22 릴리스), PyPI `mteb` 2.18.6 (2026-07-22) | https://github.com/embeddings-benchmark/mteb/releases/tag/2.18.6 |
| 라이선스·활동 | `Apache-2.0`, pushed 2026-07-24, ★3,369 — **매우 활발** | `gh api` |
| 벤치마크 갈래 | MTEB(원본), MMTEB(2025년 도입 다국어 확장), MTEB(eng, v2) | README |
| 리더보드 위치 | https://huggingface.co/spaces/mteb/leaderboard | README |
| **모델별 점수** | **`미확인`** — HF Space가 JS/Docker 렌더링이라 정적 fetch 시 "Fetching metadata from the HF Docker repository..." 로딩 화면만 나옴 | 직접 fetch 실패 |
| 과적합·오염 논쟁 | README에는 **관련 경고 문구 없음** (없다는 사실 자체를 확인) | README |

> **책에 쓸 때:** MTEB 순위표의 특정 모델·점수를 본문에 박지 마라. 확인이 안 됐고, 순위는 주 단위로 바뀐다. "리더보드는 출발점이지 결론이 아니다 — 자기 도메인 데이터로 다시 재라"는 서술이 안전하고 실무적으로도 옳다.

---

## 표 3. eval·관측성 `[축 4]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| Langfuse | trace + eval (OSS+클라우드) | 메인 리포(플랫폼) `v3.224.1` (2026-07-23). PyPI `langfuse` **4.14.1** (2026-07-20), npm `langfuse` 3.38.20 | https://github.com/langfuse/langfuse/releases/tag/v3.224.1 | `NOASSERTION` (SPDX 미판정) | 셀프호스팅 가능한 LLM 관측성 — 무료 자체 운영이 기본 옵션 | pushed 2026-07-25 (당일), ★31,828 | 2026-07-25 |
| ↳ Langfuse 버전 체계 주의 | — | 메인 리포 태그는 `v3.x`, Python SDK는 `4.x`, JS SDK는 `3.38.x` — **세 계열이 서로 다르다** | 릴리스 노트 본문이 플랫폼 기능(cloud AI features, api)을 다루므로 `v3.224.1`은 **플랫폼/서버 라인으로 판단**되나, **서버↔SDK 대응 관계는 미확인** | — | **"Langfuse 4.x"라고 쓰면 제품 버전으로 오독된다.** 본문에서 버전을 언급할 땐 반드시 "Python SDK 4.14.1" / "플랫폼 v3.224.1"처럼 계열을 특정하라 | — | 2026-07-25 |
| LangSmith | trace + eval (매니지드) | `미확인 (managed service, 버전 개념 없음)` | https://www.langchain.com/pricing-langsmith | 상용 | LangChain 생태계와 가장 밀착된 트레이싱 | 매니지드. 가격은 표 5 | 2026-07-25 |
| Braintrust | eval 플랫폼 (매니지드) | `미확인 (managed service)`. SDK: PyPI `braintrust` 0.30.1 (2026-07-21), npm `braintrust` 3.24.0 | https://www.braintrust.dev/pricing | 상용 (SDK `autoevals`는 MIT) | 실험·프롬프트 플레이그라운드 중심의 eval 워크플로 | `autoevals` 최신 `js-0.3.0` (2026-06-09), pushed 2026-07-24 | 2026-07-25 |
| Arize Phoenix | OSS 관측성 + eval | `arize-phoenix-v19.6.0` (2026-07-24). PyPI `arize-phoenix` 19.6.0 (2026-07-24) | https://github.com/Arize-ai/phoenix/releases/tag/arize-phoenix-v19.6.0 | `NOASSERTION` (SPDX 미판정) | OpenTelemetry 기반 로컬 실행 가능한 trace UI | pushed 2026-07-25 (당일), ★10,728 | 2026-07-25 |
| W&B Weave | trace + eval | `v0.53.2` (2026-07-16). PyPI `weave` 0.53.2 (2026-07-16) | https://github.com/wandb/weave/releases/tag/v0.53.2 | `Apache-2.0` | 기존 W&B 실험 관리 워크플로의 연장선 | pushed 2026-07-25 (당일), ★1,108 | 2026-07-25 |
| Helicone | LLM 프록시·관측성 | `v2025.08.21-1` (2025-08-21) | https://github.com/Helicone/helicone/releases/tag/v2025.08.21-1 | `Apache-2.0` | 게이트웨이 프록시 한 줄로 붙는 관측성 | pushed 2026-07-25 (당일), ★5,993. **릴리스 태그는 11개월 정체 but 코드는 당일 푸시 — 릴리스를 태깅 안 하는 관행** | 2026-07-25 |
| OpenLLMetry (Traceloop) | OTel 기반 계측 SDK | `0.62.1` (2026-06-28). npm `@traceloop/node-server-sdk` 0.27.0 | https://github.com/traceloop/openllmetry/releases/tag/0.62.1 | `Apache-2.0` | 벤더 중립 OTel 계측 — 백엔드를 나중에 갈아탈 수 있다 | pushed 2026-07-13, ★7,325 | 2026-07-25 |
| **OTel GenAI semantic conventions** | 스펙 | **별도 리포로 분리됨** (`open-telemetry/semantic-conventions-genai`). 릴리스 태그 없음. 코어 semconv는 `v1.43.0` (2026-07-03) | https://github.com/open-telemetry/semantic-conventions-genai | `Apache-2.0` | 벤더 중립 GenAI 트레이스 스키마의 표준 후보 | **상태: `Status: Development`** (stable 아님). pushed 2026-07-24, ★192 | 2026-07-25 |
| Ragas | RAG eval 라이브러리 | `v0.4.3` (2026-01-13). PyPI `ragas` 0.4.3 (2026-01-13) | https://github.com/explodinggradients/ragas/releases/tag/v0.4.3 | `Apache-2.0` | RAG 특화 지표(faithfulness 등)의 사실상 표준 | ⚠️ pushed **2026-02-24** — 5개월 정체. **리포가 `vibrantlabsai/ragas`로 이전됨** (릴리스 URL이 그쪽으로 리다이렉트). ★14,981 | 2026-07-25 |
| DeepEval | LLM eval 프레임워크 | `v4.1.3` (2026-07-12). PyPI `deepeval` 4.1.3 (2026-07-22) | https://github.com/confident-ai/deepeval/releases/tag/v4.1.3 | `Apache-2.0` | pytest 스타일로 쓰는 LLM 단위 테스트 | pushed 2026-07-24, ★17,108 | 2026-07-25 |
| promptfoo | eval + 레드팀 CLI | `0.121.19` (2026-07-14). npm `promptfoo` 0.121.19 | https://github.com/promptfoo/promptfoo/releases/tag/0.121.19 | `MIT` | 선언적 YAML로 CI에 꽂는 eval + 레드팀 | pushed 2026-07-24, ★23,580. ⚠️ **PyPI `promptfoo` 0.1.4는 동일 프로젝트가 아님 — npm이 정본** | 2026-07-25 |
| Inspect AI (UK AISI) | eval 프레임워크 | **PyPI `inspect-ai` 0.3.249 (2026-07-21)**. GitHub `releases/latest` 404, 태그는 `release/2025-11-28` 형식 | https://pypi.org/pypi/inspect-ai/json · https://github.com/UKGovernmentBEIS/inspect_ai | `MIT` | 정부 AI 안전 기관이 만든 에이전트 eval — 솔버/스코어러 추상화 | pushed 2026-07-24, ★2,405 | 2026-07-25 |
| OpenAI Evals | eval 프레임워크 | `미확인` (릴리스·태그 미등록) | https://github.com/openai/evals | `NOASSERTION` (SPDX 미판정) | eval 레지스트리 형태의 원조 구현 | ⚠️ pushed **2026-04-14** — 3개월 정체, ★18,996 | 2026-07-25 |
| HELM (Stanford CRFM) | 벤치마크 하네스 | `v0.5.16` (2026-04-30) | https://github.com/stanford-crfm/helm/releases/tag/v0.5.16 | `Apache-2.0` | 다면 평가(정확도·견고성·공정성) 학술 하네스 | pushed 2026-07-01, ★2,864 | 2026-07-25 |
| autoevals (Braintrust) | LLM-as-judge 스코어러 | `js-0.3.0` (2026-06-09) | https://github.com/braintrustdata/autoevals/releases/tag/js-0.3.0 | `MIT` | 바로 쓰는 judge 스코어러 모음 | pushed 2026-07-24, ★977 | 2026-07-25 |

**소계: 15개**

### 표 3-1. OTel GenAI semantic conventions — 이 책에서 가장 중요한 "표준" 사실 `[축 4]`

2026-07-25 확인 결과, 이 스펙에는 **두 가지 중요한 변화**가 있다. 둘 다 본문에서 단정하기 전에 반드시 반영해야 한다.

| 항목 | 확인된 사실 | 출처 |
|------|-----------|------|
| **리포 분리** | GenAI semconv가 코어 `semantic-conventions`에서 **별도 리포로 이전**됐다. 기존 문서 URL(`opentelemetry.io/docs/specs/semconv/gen-ai/`)은 "moved to the OpenTelemetry GenAI semantic conventions repository ... no longer maintained in the current location" 안내만 남았다 | https://opentelemetry.io/docs/specs/semconv/gen-ai/ |
| **안정성 상태** | **`Status: Development`** — stable도, experimental 승격도 아니다 | https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/README.md |
| 정의 범위 | Events(입출력), Exceptions, Metrics, **Model Spans**, **Agent Spans** | 동일 |
| 벤더별 규약 | Anthropic, Azure AI Inference, AWS Bedrock, OpenAI + **MCP 가이던스** | 동일 |
| 코어 semconv 버전 | `v1.43.0` (2026-07-03) — GenAI 리포는 Weaver로 코어 의존성 관리 | `gh api` + 리포 README |
| GenAI 리포 릴리스 | **태그된 릴리스 없음** (`releases` 비어 있음), ★192, pushed 2026-07-24 | `gh api` |

> **책에 쓸 값 (중요):** "OTel GenAI semconv를 따르면 벤더 중립 관측성이 된다"는 서술은 **현재 시점에서 과장**이다. 상태가 `Development`이고 리포가 막 분리됐으며 릴리스 태그조차 없다. 정확한 서술은 "표준화가 진행 중이고, **Agent Spans까지 규약 범위에 들어왔다**. 지금 붙이면 스키마 변경을 감수해야 한다" 쪽이다. Agent Spans가 규약에 포함됐다는 사실 자체가 이 책 독자에게 중요한 신호다.

---

## 표 4. 에이전트 벤치마크 (제품·리더보드 축) `[축 4]`

**⚠️ 이 표의 점수 열은 대부분 `미확인`이다.** 리더보드가 클라이언트 렌더링이라 정적 fetch로 점수를 못 읽었다. 유일한 예외가 Terminal-Bench 2.0이다.

| 벤치마크 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 리더보드 최고 점수 | 확인일 |
|---------|---------------------|-------------|---------|------------|----------|-----------------|--------|
| SWE-bench | `v4.1.0` (git tag). PyPI `swebench` 4.1.0 (2025-09-11) | https://github.com/SWE-bench/SWE-bench | `MIT` | 실제 GitHub 이슈를 실제 테스트로 채점 | ⚠️ pushed **2026-04-01** — 4개월 정체, ★5,484. `releases/latest` 404 | **`미확인`** — swebench.com 리더보드 fetch 시 본문이 truncate돼 점수 미노출. splits: Verified/Multilingual/Lite/Full/Multimodal | 2026-07-25 |
| Terminal-Bench | 리포 태그 없음. PyPI `terminal-bench` **0.2.18 (2025-09-26)** — 리포 pushed 2026-07-11이므로 **PyPI가 리포보다 낡음** | https://www.tbench.ai/leaderboard · https://github.com/laude-institute/terminal-bench | `Apache-2.0` | 터미널에서 끝까지 해내는지 — 에이전트 하네스째로 평가 | pushed 2026-07-11, ★2,482. 리더보드에 1.0 / 2.0 / 2.1 공존 | **확인됨 (2.0):** 1위 NexAU-AHE (GPT-5.5) **84.7% ±2.1**, 2위 LemonHarness **84.5% ±2.6**, 3위 Capy (GPT-5.5) **83.1% ±2.1**, 4위 Codex CLI (GPT-5.5) **82.2% ±2.2**, 6위 WOZCODE (Claude Opus 4.7) **80.2% ±2.1**, 7위 TongAgents (Gemini 3.1 Pro) **80.2% ±2.6** | 2026-07-25 |
| τ-bench 계열 | 리포 `sierra-research/tau2-bench` (릴리스·태그 없음). **README는 현재 버전을 τ³-bench(tau3-bench)로 기술** | https://github.com/sierra-research/tau2-bench | `MIT` | 고객 응대 도메인(airline·retail·telecom·banking_knowledge·mock) 시뮬레이션 + 음성·지식 검색 평가 | pushed 2026-07-24, ★1,660 | **`미확인`** — 리포 페이지에 수치 베이스라인 없음 | 2026-07-25 |
| GAIA | `미확인` | https://huggingface.co/spaces/gaia-benchmark/leaderboard | `미확인` | 도구 사용이 필수인 일반 어시스턴트 과제 | HF Space | **`미확인`** — Space가 로딩 화면만 반환 | 2026-07-25 |
| WebArena | `v0.2.0` (**2023-10-21**) | https://github.com/web-arena-x/webarena/releases/tag/v0.2.0 | `Apache-2.0` | 자체 호스팅 웹 환경에서의 브라우저 에이전트 평가 | ⚠️ pushed 2025-11-26, ★1,556. **릴리스 2023년 — 구버전 정보일 수 있음, 사실상 정체** | `미확인` | 2026-07-25 |
| AgentBench | 릴리스·태그 없음 | https://github.com/THUDM/AgentBench | `Apache-2.0` | 8개 환경 다면 에이전트 평가 | ⚠️ pushed **2026-02-08** — 5개월 정체, ★3,602 | `미확인` | 2026-07-25 |

**소계: 6개**

> **책에 쓸 값:** 벤치마크 활동 신호가 극명하게 갈린다. Terminal-Bench(pushed 2026-07-11, 리더보드 2.1까지)와 τ-bench 계열(pushed 2026-07-24)은 살아 있고, WebArena(2023년 릴리스)·AgentBench(5개월 정체)는 사실상 멈췄다. "표준 벤치마크"로 나열하면 독자를 죽은 벤치마크로 보낸다. 신선도까지 같이 적어야 한다.
> **Terminal-Bench 2.0 점수는 상단이 80%대로 몰려 있고 오차범위가 ±2%대**라 1~5위 간 차이는 통계적으로 겹친다. "1위 모델" 식 서술보다 "상단이 포화 구간에 들어섰다"가 정확하다.

---

## 표 5. 가드레일 `[축 4]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| Guardrails AI | 입출력 검증 프레임워크 | `v0.10.2` (2026-06-04). PyPI `guardrails-ai` 0.10.2 | https://github.com/guardrails-ai/guardrails/releases/tag/v0.10.2 | `Apache-2.0` | validator 허브 방식의 선언적 입출력 검증 | pushed 2026-07-24, ★7,203 | 2026-07-25 |
| NeMo Guardrails | 대화 흐름 레일 | `v0.23.0` (2026-07-01). PyPI `nemoguardrails` 0.23.0 | https://github.com/NVIDIA/NeMo-Guardrails/releases/tag/v0.23.0 | `NOASSERTION` (SPDX 미판정) | Colang DSL로 대화 흐름 자체를 제약 | pushed 2026-07-25 (당일), ★6,786. **리포가 `NVIDIA-NeMo/Guardrails`로 이전** (릴리스 URL 리다이렉트) | 2026-07-25 |
| OpenAI Moderation | 콘텐츠 안전 API | `omni-moderation-latest` | https://developers.openai.com/api/docs/guides/moderation | 상용 API | **무료**, 이미지 입력 지원(최대 20MB), 13개 카테고리 | 매니지드 | 2026-07-25 |
| Azure AI Content Safety | 콘텐츠 안전 + 에이전트 안전 | API 버전 `미확인` (문서에 GA/preview 혼재) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview | 상용 | **Prompt Shields**(탈옥·주입 탐지) + **Task adherence API**(에이전트 도구 사용 이탈 탐지) | 문서 갱신 2026-06-05. F0/S0 티어 | 2026-07-25 |
| Llama Guard | 오픈 안전 분류 모델 | `미확인` (모델 카드 페이지 본문 fetch 실패) | https://github.com/meta-llama/PurpleLlama | `NOASSERTION` (Llama 라이선스 계열) | 자체 호스팅 가능한 입출력 안전 분류기 | pushed 2026-07-24, ★4,309. 릴리스 태그 없음 | 2026-07-25 |
| Prompt Guard | 오픈 주입 탐지 모델 | `미확인` | https://github.com/meta-llama/PurpleLlama | `NOASSERTION` | 프롬프트 인젝션·탈옥 전용 소형 분류기 | PurpleLlama 리포 동일 | 2026-07-25 |
| OpenAI Agents SDK guardrails | 프레임워크 내장 가드레일 | 리포 `openai/openai-agents-python` pushed 2026-07-25, ★28,160 | https://openai.github.io/openai-agents-python/guardrails/ | `MIT` | input/output 가드레일 + **tripwire 예외로 실행 즉시 중단** | pushed 2026-07-25 (당일) | 2026-07-25 |
| Rebuff | 프롬프트 인젝션 방어 | `v0.1.1` (**2024-01-20**) | https://github.com/protectai/rebuff/releases/tag/v0.1.1 | `Apache-2.0` | (역사적 참조용) 다층 인젝션 탐지 | ❌ **`archived: true` — 아카이브된 죽은 프로젝트.** pushed 2024-08-07, ★1,515 | 2026-07-25 |
| invariant | 에이전트 분석·가드레일 | 릴리스·태그 없음 | https://github.com/invariantlabs-ai/invariant | `Apache-2.0` | 에이전트 트레이스에 대한 규칙 기반 검사 | ⚠️ pushed **2026-01-12** — 6개월 정체, ★436 | 2026-07-25 |
| Lakera | 상용 인젝션 방어 | `미확인` | — | 상용 | (제품 상세 확인 실패) | 리포 접근 실패 — "수집 한계" 참조 | 2026-07-25 |

**소계: 10개**

### 표 5-1. 가드레일 아키텍처 패턴 (벤더 권장 배치) `[축 4]` `[축 6]`

공식 문서에서 확인한 배치 패턴만 적는다.

| 패턴 | 벤더가 말하는 것 | 1차 소스 |
|------|---------------|---------|
| **입력 가드레일 + tripwire 중단** | OpenAI Agents SDK: "Input guardrails run only for the first agent in the chain", "Output guardrails run only for the agent that produces the final output". 발동 시 `{Input,Output}GuardrailTripwireTriggered` 예외를 **즉시 raise하고 실행을 중단**한다 | https://openai.github.io/openai-agents-python/guardrails/ |
| **값싼 모델로 먼저 걸러라** | 같은 문서: 가드레일 함수 안에 별도 검증 에이전트를 두는 패턴. "a lightweight model runs guardrail checks before deploying expensive models, thereby reducing costs for blocked requests" | 동일 |
| **탈옥·주입은 전용 분류기로** | Azure **Prompt Shields**: "Scans text for the risk of a User input attack on a Large Language Model." 입력 한도 10K자, 문서 최대 5개·총 10K자 | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview |
| **도구 사용 이탈 감시 (에이전트 특화)** | Azure **Task adherence API** (preview): "Detects when tool use by AI agents is misaligned, unintended, or premature in the context of a user interaction." 입력 한도 **100K자** | 동일 |
| **환각을 출력단에서 잡기** | Azure **Groundedness detection** (preview): LLM 응답이 제공된 소스에 근거하는지 판정. grounding source 최대 55,000자, 쿼리 최대 7,500자·최소 3단어 | 동일 |
| **도구 호출 승인 게이트 / 최소권한** | Claude Code 문서: 기본적으로 파일 쓰기·Bash·MCP 도구에 **권한을 요청**한다. 완화 수단 3종 — ① auto mode(별도 classifier가 "scope escalation, unknown infrastructure, or hostile-content-driven actions"만 차단), ② 허용목록(`npm run lint` 등 개별 허용), ③ **OS 레벨 샌드박싱**(파일시스템·네트워크 제한). 비대화형 배치 실행 시 `--allowedTools`로 권한 축소 권장 | https://code.claude.com/docs/en/best-practices |
| **결정적 게이트는 훅으로** | 같은 문서: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." 예: "a hook that blocks writes to the migrations folder" | 동일 |

> **책에 쓸 값:** 가드레일을 "필터 하나"로 그리면 안 된다. 확인된 배치는 **4층**이다 — ① 입력단 주입·탈옥 분류기(Prompt Shields / Prompt Guard) → ② 실행 중 도구 호출 승인·권한 축소(허용목록 / 샌드박스 / auto-mode classifier) → ③ 출력단 근거성·콘텐츠 검사(Groundedness / Moderation) → ④ 결정적 훅(어드바이저리 지시가 아니라 코드로 강제). 그리고 "advisory 지시 vs deterministic 훅"의 구분은 이 책 독자가 가장 자주 틀리는 지점이다.

---

## 표 6. RAG 파이프라인·인덱싱·청킹 `[축 3]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| LlamaIndex (인덱싱 축) | RAG 프레임워크 | `v0.14.23` (2026-06-24). PyPI 0.14.23, npm `llamaindex` 0.12.1 | https://github.com/run-llama/llama_index/releases/tag/v0.14.23 | `MIT` | 인덱스·리트리버 추상화가 가장 촘촘하다 | pushed 2026-07-25 (당일), ★51,078 | 2026-07-25 |
| Haystack | RAG·검색 파이프라인 | **`v3.0.0` (2026-07-20 — 메이저 릴리스 5일 전)** | https://github.com/deepset-ai/haystack/releases/tag/v3.0.0 | `Apache-2.0` | 명시적 파이프라인 그래프로 조립 | pushed 2026-07-25 (당일), ★26,010. **v3.0.0이 갓 나옴 — v2 기준 자료는 구버전** | 2026-07-25 |
| Unstructured | 문서 파싱·전처리 | `0.24.1` (2026-07-11) | https://github.com/Unstructured-IO/unstructured/releases/tag/0.24.1 | `Apache-2.0` | 잡다한 파일 포맷을 요소 단위로 정규화 | pushed 2026-07-23, ★15,197 | 2026-07-25 |
| Docling | 문서 변환 | `v2.115.0` (2026-07-23) | https://github.com/docling-project/docling/releases/tag/v2.115.0 | `MIT` | PDF 레이아웃·표 구조를 살려서 변환 | pushed 2026-07-24, **★63,754 (이 표 최다)** | 2026-07-25 |
| Chonkie | 청킹 라이브러리 | `v1.7.0` (2026-07-07) | https://github.com/chonkie-inc/chonkie/releases/tag/v1.7.0 | `MIT` | 청킹만 전담하는 경량 라이브러리 | pushed 2026-07-24, ★4,565. 리포가 `feyninc/chonkie`로 이전 (릴리스 URL 리다이렉트) | 2026-07-25 |
| Cognee | 메모리·graph RAG | `v1.4.0.dev0` (2026-07-20, **dev 프리릴리스**) | https://github.com/topoteretes/cognee/releases/tag/v1.4.0.dev0 | `Apache-2.0` | 에이전트 메모리를 그래프로 | pushed 2026-07-25 (당일), ★29,300. **최신 태그가 `.dev0` — 안정 버전 미확인** | 2026-07-25 |
| Microsoft GraphRAG | graph RAG | `v3.1.1` (2026-07-18) | https://github.com/microsoft/graphrag/releases/tag/v3.1.1 | `MIT` | 엔티티 그래프 + 커뮤니티 요약으로 전역 질의 | pushed 2026-07-25 (당일), ★34,827 | 2026-07-25 |

**소계: 7개**

### 표 6-1. 청킹·컨텍스트 공급 실무 수치 (출처 있는 것만) `[축 3]`

| 지침 | 확인된 수치 | 출처 | 신선도 |
|------|-----------|------|--------|
| 청크 크기 (일반) | "usually no more than a few hundred tokens" | Anthropic, Contextual Retrieval | **2024-09-19 — 구버전 정보일 수 있음** |
| 청크 크기 (작게) | **128–256 tokens** | Pinecone, Chunking strategies | 발행일 미확인 |
| 청크 크기 (크게) | **512–1024 tokens** | 동일 | 발행일 미확인 |
| 고정 크기 전략 | 임베딩 모델 최대 컨텍스트에 맞춤 (예: `llama-text-embed-v2` 1024, `text-embedding-3-small` 8196) | 동일 | 발행일 미확인 |
| 오버랩 | **`미확인`** — Pinecone 청킹 문서에 구체 수치 없음, Anthropic 글에도 없음 | — | — |
| 청킹 전략 이름 | ① 고정 크기 ② 문장·문단 분할 ③ recursive character ④ 문서 구조 기반(PDF/HTML/Markdown/LaTeX) ⑤ semantic chunking ⑥ **contextual chunking with LLMs** | Pinecone | 발행일 미확인 |
| 컨텍스트 보강 효과 | Contextual Embeddings 단독: top-20 검색 실패율 **35% 감소** (5.7% → 3.7%). + Contextual BM25: **49% 감소** (5.7% → 2.9%). + 리랭킹까지: **67% 감소** (5.7% → 1.9%) | Anthropic, Contextual Retrieval | **2024-09-19 — 모델이 바뀌었으므로 수치는 재현 보장 없음. "이 실험에서"를 반드시 붙여라** |

> **오버랩 수치는 어떤 1차 소스에서도 확인하지 못했다.** 흔히 "10~20% 오버랩"이라 말하지만 이번 세션에서 공식 문서 근거를 찾지 못했다. 본문에 숫자를 박지 말고 "오버랩은 모델·문서 구조에 따라 조정하는 튜닝 대상"으로 서술하라.

---

## 6. 벡터 DB 선택 축 — "우리 규모에 pgvector로 충분한가" `[축 3]` `[축 6]`

독자가 실제로 묻는 질문에 맞춰, **확인된 사실로만** 축을 세운다.

### 축 A. 내장(기존 DB 겸업) vs 전용 엔진

| 갈림길 | 내장형 (pgvector / Redis / MongoDB Atlas / sqlite-vec) | 전용형 (Qdrant / Weaviate / Milvus / Pinecone) |
|--------|--------------------------------------|-----------------------------------|
| 새 인프라 | 없음 — 이미 운영하는 DB에 확장/인덱스만 | 새 서비스 하나를 운영 대상에 추가 |
| 트랜잭션 정합성 | 본문·메타데이터와 **같은 트랜잭션** 안에서 갱신 | 원본 DB와 인덱스 사이 동기화 파이프라인이 별도 필요 |
| 확인된 한계 | **pgvector: HNSW/IVFFlat 인덱스는 `vector` 최대 2,000차원.** `halfvec` 4,000, `bit` 64,000, `sparsevec` 비영요소 1,000. 타입 자체는 `vector`/`halfvec` 최대 16,000차원 | Milvus는 다중 벡터 필드 동시 ANN + 내장 BM25, Qdrant는 prefetch 다단계 쿼리 등 검색 표현력이 앞선다 |
| 1차 소스 | https://github.com/pgvector/pgvector · https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/ | 표 1 각 행 |

> **이 축에서 나오는 가장 실용적인 결론(양쪽 수치 모두 1차 소스 직접 확인):** pgvector에서 **`text-embedding-3-large`의 기본 3,072차원은 HNSW 인덱스 한계(2,000)를 넘는다.**
> — 3,072는 OpenAI 임베딩 가이드 원문("or `3072` for `text-embedding-3-large`"), 2,000은 pgvector README에서 각각 직접 확인했다. **두 숫자가 서로 다른 1차 소스에서 왔고 둘 다 인용문으로 뒷받침된다** — 이 결론은 fact-checker 대조를 통과할 수 있는 형태다. 그래서 선택은 셋 중 하나다 — ① 차원 축소(`dimensions` 파라미터로 1536 이하), ② `halfvec`(4,000까지), ③ 전용 엔진. **"pgvector로 충분한가"가 인덱스 차원 한계라는 아주 구체적인 숫자에서 갈린다**는 것이 이 책이 줄 수 있는 실무 지식이다. MongoDB Atlas는 최대 8,192차원이므로 이 제약이 없다.

### 축 B. 하이브리드 검색 지원 깊이
표 1-1 참조. "지원/미지원"이 아니라 **융합 알고리즘 수와 조절 손잡이 수**로 갈린다. Milvus만 **BM25 sparse 임베딩 생성까지 엔진이 대신한다**(파이프라인 코드가 줄어든다).

### 축 C. 운영 부담 (스펙트럼)
`sqlite-vec`(서버 없음, 단일 파일) → `Chroma`/`LanceDB`(임베디드) → `pgvector`(기존 Postgres) → `Qdrant`/`Weaviate`/`Milvus`(전용 서비스 운영) → `Vespa`(가장 무거움) → `Pinecone`/`Turbopuffer`/`MongoDB Atlas`(매니지드, 운영 부담을 돈으로 치환)

### 축 D. 스케일 임계점 (벤더가 스스로 말하는 숫자)
- Turbopuffer 공식 문서: "4T+ documents, 10M+ writes/s, and 25k+ queries/s" 서비스 중. 쓰기 지연 "p90=248ms for 512KB upserts", **콜드 쿼리 "p90=1214ms on 1M documents"** (캐시 미적용/미고정 시)
- → **책에 쓸 값:** 객체 스토리지 기반 설계는 **캐시 히트 여부가 지연을 5배 이상 가른다**. "싸다"의 대가가 콜드 스타트라는 걸 벤더가 자기 문서에 적어 놨다. 이건 아키텍처 트레이드오프를 가르치기에 아주 좋은 1차 인용이다.
- Pinecone 확인된 한계: 메타데이터 **레코드당 40KB**, sparse 벡터 비영값 **1,000개**, `top_k` 최대 **1,000**, 쿼리 결과 크기 **4MB**, sparse 인덱스 쓰기 **10 QPS**·읽기 **100 QPS**. 10만 네임스페이스 초과 시 문의
- Azure Content Safety 처리량(가드레일 쪽 임계점): F0 5 RPS / S0 1000 RP10S, Groundedness 50 RPS

### 축 E. 라이선스 (조직에서 실제로 막히는 축)
`Apache-2.0`: Qdrant, Milvus, Chroma, LanceDB, Vespa, OpenSearch, sqlite-vec / `BSD-3-Clause`: Weaviate / `MIT`: FAISS / `GPL-3.0`: **Typesense** / `NOASSERTION`(비-OSI 계열 주의): **Elasticsearch, Redis(RediSearch)**, pgvector(판정 불가)
> Typesense의 GPL-3.0과 Elasticsearch/Redis의 소스 가용 라이선스는 사내 배포 정책에서 실제로 걸린다. 라이선스는 성능 열 다음이 아니라 성능 열과 같은 급으로 다뤄야 한다.

---

## 7. 벡터 DB가 필요 없는 경우 (1차 소스 근거) `[축 3]` `[축 6]`

이 책에서 가장 값진 절이 될 수 있는 부분이다. **벤더·모델 제공자가 스스로 "안 써도 된다"고 말한 근거만** 모았다.

### 근거 1 — 코퍼스가 작으면 그냥 다 넣어라 (가장 명확한 1차 인용)

> "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods."
> — Anthropic, *Introducing Contextual Retrieval*, **2024-09-19**
> https://www.anthropic.com/news/contextual-retrieval

- **20만 토큰 / 약 500페이지**라는 구체적 임계값이 제공자 공식 발표문에 박혀 있다.
- 신선도 주의: 2024-09 글이다. 그 사이 컨텍스트 창은 더 커졌으므로 이 임계값은 **보수적 하한**으로 읽는 게 맞다. 본문에서는 "2024년 Anthropic 기준 20만 토큰"으로 연도를 반드시 붙여라.
- 프롬프트 캐싱과 함께 쓰면 비용 논리도 바뀐다는 점이 같은 글의 맥락이다.

### 근거 2 — 코딩 에이전트는 인덱스 대신 탐색 도구를 쓴다

Claude Code 공식 문서에서 확인된 코드베이스 탐색 방식은 **임베딩 인덱스가 아니라 에이전틱 탐색**이다.

- 파일을 직접 읽고(`@` 참조), 명령을 실행하며 자율적으로 문제를 해결하는 구조: "Claude Code can read your files, run commands, make changes, and autonomously work through problems"
- 탐색이 컨텍스트를 잡아먹는 문제는 **인덱스가 아니라 서브에이전트로** 해결한다: "When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries"
- 외부 시스템 조회도 인덱스가 아니라 **CLI 도구**를 권장한다: "CLI tools are the most context-efficient way to interact with external services"
- 실패 패턴으로 **범위 없는 탐색**을 명시: "The infinite exploration. You ask Claude to 'investigate' something without scoping it. Claude reads hundreds of files, filling the context." → 처방은 "Scope investigations narrowly or use subagents"
- 1차 소스: https://code.claude.com/docs/en/best-practices

> ⚠️ **정직한 한계 표기:** 이 문서에는 "우리는 RAG/임베딩 인덱스를 쓰지 않는다"는 **명시적 부정 문장이 없다.** 확인된 것은 "문서 전반이 인덱스 없는 에이전틱 탐색(파일 읽기·명령 실행·서브에이전트·CLI)을 전제로 기술돼 있다"는 사실뿐이다. 본문에서 "공식적으로 인덱싱을 쓰지 않는다고 밝혔다"고 쓰면 과장이다. **"공식 문서가 권장하는 워크플로는 인덱스가 아니라 탐색 도구와 서브에이전트 기반이다"**가 확인 가능한 서술의 상한선이다.

### 근거 3 — 검색 실패의 상당 부분은 리랭킹으로 해결된다 (DB 교체 전에 할 일)

Anthropic 실험(2024-09-19)에서 top-20 검색 실패율은 **5.7% → 1.9%**로 떨어졌는데, 그 경로는 벡터 DB 교체가 아니라 **컨텍스트 보강 + BM25 병용 + 리랭킹**이었다.
> **책에 쓸 값:** "검색이 안 맞는다 → 벡터 DB를 바꾼다"는 흔한 오진이다. 같은 DB에서 ① 하이브리드(BM25 병용) ② 컨텍스트 보강 청킹 ③ 리랭커 세 가지가 먼저다. 리랭커 단가는 임베딩보다 싸다(Voyage `rerank-2.5-lite` $0.02/1M).

### 근거 4 — 첫 단계 후보 축소용이지 정답 도출용이 아니다

Turbopuffer 공식 문서는 자기 제품 포지션을 이렇게 규정한다: "first-stage retrieval to efficiently narrow millions of documents ... down to tens or hundreds"
> 벡터 검색은 **1차 후보 축소기**다. 정답을 고르는 건 리랭커와 LLM이다. 이 프레이밍이 명확하면 "벡터 검색 정확도"에 과투자하는 실수를 막을 수 있다.

### 근거 5 — 정형 데이터는 SQL이 맞다
확인된 1차 소스를 이번 세션에서 찾지 못했다. 논리적으로 자명하지만 **인용 가능한 벤더 문장을 확보하지 못했으므로** 본문에서 출처를 붙이지 말고 저자 주장으로 쓰거나, fact-checker 단계에서 별도 확인을 요청하라. → "미확인 항목 목록"에 기재.

---

## 8. 자료별 신선도·신뢰성 카드

축 태그와 신뢰성 등급을 붙인 개별 자료 카드. (표에 이미 반영된 리포·레지스트리 조회는 생략)

### 자료 1: Anthropic — Introducing Contextual Retrieval `[축 3]`
- 출처: https://www.anthropic.com/news/contextual-retrieval
- 저자·날짜: Anthropic, **2024-09-19**
- 신뢰성: **최상** (모델 제공자 1차 발표, 수치와 방법 명시)
- 핵심 주장: 청크에 문맥을 덧붙여 임베딩하고 BM25를 병용하면 검색 실패율이 크게 떨어진다. 20만 토큰 미만 코퍼스는 RAG 자체가 불필요하다.
- 인용 가능한 구절: "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods." / 청크는 "usually no more than a few hundred tokens"
- 신선도 경고: **약 22개월 전 자료. 수치는 "2024년 실험 기준"으로 못 박아야 한다.**
- 관련 섹션: 데이터·RAG 챕터 도입부, "벡터 DB가 필요 없는 경우", 청킹 실무

### 자료 2: OpenTelemetry GenAI semantic conventions `[축 4]`
- 출처: https://github.com/open-telemetry/semantic-conventions-genai · https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/README.md
- 저자·날짜: OpenTelemetry, pushed **2026-07-24** (릴리스 태그 없음)
- 신뢰성: **최상** (스펙 1차 소스)
- 핵심 주장: GenAI 규약이 코어 semconv에서 분리돼 독립 리포로 운영된다. 상태는 `Development`. **Agent Spans**와 MCP 가이던스가 규약 범위에 포함.
- 인용 가능한 구절: "Status: Development" / 구 문서 위치는 "no longer maintained in the current location"
- 관련 섹션: 관측성 챕터 — "표준은 어디까지 왔나"

### 자료 3: OpenAI 임베딩 가격의 공식 페이지 간 불일치 `[축 3]` ⚠️
- 출처: https://developers.openai.com/api/docs/models/text-embedding-3-large (모델 카드) vs 가격 페이지
- 확인 내용: 모델 카드 fetch 결과 `text-embedding-3-large` = **$0.13 / 1M tokens**, `text-embedding-3-small` = **$0.02 / 1M tokens** (둘 다 직접 fetch). 한편 3-large를 **$0.065**로 표기한다는 보고가 있다 — 단 **이 $0.065는 내가 직접 fetch한 값이 아니라 WebSearch가 요약한 OpenAI 개발자 포럼 글(2025-08 시점 보고)의 내용이다.** 가격 페이지 자체는 도달 실패(수집 한계 6번).
- 신뢰성: **최상** (모델 카드 직접 확인) — 단, **공식 표면 간 불일치 가능성**으로 단일 값 단정은 불가
- ⚠️ 두 값의 출처 등급이 다르다: **$0.13 = 직접 fetch(검증됨)**, **$0.065 = 포럼 글의 검색 요약(미검증)**. fact-checker는 후자를 확인된 사실로 취급하면 안 된다.
- 관련 섹션: 임베딩 비용 계산 예시
- **fact-checker 지시:** 본문에 임베딩 단가를 쓸 경우 반드시 "모델 카드 기준 $0.13(2026-07 확인), 가격 페이지와 불일치 보고 있음"처럼 출처 표면을 특정하라. 이 값으로 총비용 계산 예시를 만들면 배수 오류가 난다.

### 자료 4: Claude Code Best practices `[축 1]` `[축 4]`
- 출처: https://code.claude.com/docs/en/best-practices (구 URL `anthropic.com/engineering/claude-code-best-practices`에서 308 리다이렉트)
- 저자·날짜: Anthropic, 발행일 미표기 (문서 상시 갱신형)
- 신뢰성: **최상** (제공자 공식 문서)
- 핵심 주장: 에이전트 품질의 지배 변수는 **컨텍스트 예산**과 **검증 루프**다. "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."
- 인용 가능한 구절: "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from." / "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." / 실패 패턴 "The trust-then-verify gap. Claude produces a plausible-looking implementation that doesn't handle edge cases."
- 관련 섹션: 에이전트 원리(축 1), 가드레일·권한 설계(축 4), 평가 루프 설계

### 자료 5: OpenAI Agents SDK — Guardrails `[축 4]`
- 출처: https://openai.github.io/openai-agents-python/guardrails/
- 신뢰성: **최상** (공식 프레임워크 문서)
- 인용 가능한 구절: "Input guardrails run only for the first agent in the chain" / "Output guardrails run only for the agent that produces the final output" / 발동 시 "immediately raise ... exception and halt the Agent execution"
- 관련 섹션: 가드레일 챕터 — 배치 위치와 비용 논리

### 자료 6: Azure AI Content Safety Overview `[축 4]`
- 출처: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview
- 저자·날짜: Microsoft, 문서 갱신 **2026-06-05** (ms.date 2025-09-16)
- 신뢰성: **최상**
- 핵심 주장: 콘텐츠 안전이 "유해 표현 필터"를 넘어 **에이전트 행동 감시**로 확장됐다 — Task adherence(도구 사용 이탈 탐지), Groundedness(근거성).
- 인용 가능한 구절: Task adherence는 "Detects when tool use by AI agents is misaligned, unintended, or premature in the context of a user interaction."
- 관련 섹션: 가드레일 챕터 — 에이전트 특화 안전 장치

### 자료 7: Turbopuffer Docs `[축 3]`
- 출처: https://turbopuffer.com/docs
- 신뢰성: **최상** (벤더 1차, 다만 성능 주장은 자사 측정치)
- 인용 가능한 구절: "as fast as in-memory search engines when cached, but far cheaper to run" / 콜드 쿼리 "p90=1214ms on 1M documents" / "first-stage retrieval to efficiently narrow millions of documents ... down to tens or hundreds"
- 관련 섹션: 벡터 DB 아키텍처 트레이드오프, 스케일 임계점

### 자료 8: pgvector README `[축 3]`
- 출처: https://github.com/pgvector/pgvector
- 신뢰성: **최상**
- 인용 가능한 사실: HNSW·IVFFlat 모두 `vector` **2,000차원 한계**, `halfvec` 4,000, `bit` 64,000, `sparsevec` 비영요소 1,000. 타입 한계는 16,000차원. 튜닝: "indexes build significantly faster when the graph fits into `maintenance_work_mem`", `hnsw.ef_construction` 기본 64, `hnsw.ef_search` 기본 40
- 관련 섹션: "우리 규모에 pgvector로 충분한가"

### 자료 9: Terminal-Bench 2.0 리더보드 `[축 4]`
- 출처: https://www.tbench.ai/leaderboard/terminal-bench/2.0
- 신뢰성: **최상** (공식 리더보드 직접 fetch)
- 확인 시점 스냅샷: 1위 84.7%±2.1 (NexAU-AHE / GPT-5.5), 10위 77.3%±2.2 (Droid / GPT-5.3-Codex)
- 신선도 경고: **리더보드는 상시 변동.** 본문에 쓸 때 "2026-07-25 확인 기준"을 반드시 병기하라.
- 관련 섹션: 평가 챕터 — 에이전트 벤치마크 읽는 법

### 자료 10: Pinecone 가격·인덱싱 문서 `[축 3]`
- 출처: https://www.pinecone.io/pricing/ · https://docs.pinecone.io/guides/index-data/indexing-overview
- 신뢰성: **최상**
- 확인된 수치: Starter 무료(2GB / 쓰기 2M / 읽기 1M / egress 1GB), Builder $20/mo(10GB / 5M / 2M), Standard $50/mo 최소 + 스토리지 $0.33/GB/mo·쓰기 $4–4.50/M·읽기 $16–18/M, Enterprise $500/mo 최소 + 쓰기 $6–6.75/M·읽기 $24–27/M
- 관련 섹션: 축 6 비용 비교

---

## 9. 축 6을 위한 조합 원재료 (데이터·eval 스택) `[축 6]`

표에서 확인된 사실만으로 구성 가능한 조합 축. **점수·성능 우열이 아니라 제약 조건으로** 갈라 놨다.

| 상황 | 데이터 계층 | eval·관측성 계층 | 가드레일 계층 | 근거 |
|------|-----------|---------------|-------------|------|
| 코퍼스 20만 토큰 미만 | **벡터 DB 없음** — 전체를 프롬프트에 | 트레이스만 (Langfuse 셀프호스팅 무료) | 입력 분류기 + 출력 검사 | Anthropic 2024-09 (연도 병기 필수) |
| 이미 Postgres 운영, 차원 ≤1536 | pgvector (HNSW) | Langfuse 또는 Phoenix (둘 다 셀프호스팅) | OpenAI Moderation(무료) | pgvector README 2,000차원 한계 |
| 차원 3072 유지 필요 | `halfvec`(4,000) / MongoDB Atlas(8,192) / 전용 엔진 | 동일 | 동일 | pgvector·Atlas 문서 |
| 하이브리드 검색이 핵심 | Milvus(내장 BM25) / Qdrant(prefetch+RRF/DBSF) / Elasticsearch(RRF retriever) | Ragas(단, 5개월 정체) 또는 DeepEval | — | 표 1-1 |
| 운영 인력 없음 | Pinecone / Turbopuffer / Atlas | LangSmith / Braintrust (매니지드) | Azure Content Safety | 표 5 가격 |
| 라이선스가 Apache-2.0이어야 함 | Qdrant / Milvus / Chroma / LanceDB / OpenSearch | Phoenix(SPDX 미판정 주의) / Weave / promptfoo(MIT) | Guardrails AI / OpenAI Agents SDK(MIT) | 표 라이선스 열 |
| CI에 eval 게이트를 꽂아야 함 | — | **promptfoo**(선언적 YAML) / DeepEval(pytest 스타일) / Inspect AI | — | 표 3 |
| 검색 품질이 안 나올 때 (DB 교체 전) | 하이브리드 + 컨텍스트 청킹 + 리랭커(Voyage `rerank-2.5-lite` $0.02/1M) | — | — | Anthropic 5.7%→1.9% 경로 |

---

## 10. 수집 한계 (접근 실패·판단 유보)

1. **JS 렌더링 리더보드 3종 실패** — MTEB(`huggingface.co/spaces/mteb/leaderboard`), GAIA(`gaia-benchmark/leaderboard`)는 HF Docker Space 로딩 화면만 반환. SWE-bench(`swebench.com`)는 본문이 truncate돼 점수 미노출. → 세 벤치마크의 점수는 전부 `미확인`. 정적 fetch로는 불가하며 브라우저 렌더링이 필요하다.
2. **Nomic 문서 404** — `https://docs.nomic.ai/atlas/embeddings-and-retrieval/guides/embedding-model-comparison` HTTP 404. Nomic Embed 관련 모든 셀 `미확인`. (`nomic-ai/contrastors`는 pushed 2025-03-26로 정체 상태이며 임베딩 모델 배포 리포가 아닌 것으로 보여 표에서 제외)
3. **Llama Guard 4 모델 카드 본문 미확보** — `llama.com` → `developer.meta.com` 리다이렉트 후에도 페이지 제목만 반환, 본문 없음. 파라미터 수·멀티모달 여부·hazard 카테고리 수(S1–S14 여부)·라이선스명 전부 `미확인`.
4. **Lakera 미확인** — `lakeraai/*` 리포 추정 경로 404. 제품 상세·버전 확인 실패.
5. **Cohere 토큰 단가 부재** — 현재 `cohere.com/pricing`은 Model Vault(시간당/월 정액)만 노출하고 Embed/Rerank 토큰 단가를 제공하지 않는다. FAQ에 레거시 Command 계열 토큰 단가만 언급. → Cohere 임베딩/리랭크 단가는 `미확인`.
6. **OpenAI 임베딩·moderation 가격 페이지 도달 실패** — `platform.openai.com/docs/pricing` → `developers.openai.com/api/docs/pricing` 리다이렉트 후 fetch했으나 임베딩·moderation 표가 응답에 포함되지 않음(LLM 모델 표만). `developers.openai.com/api/pricing`은 404. 모델 카드 개별 페이지로 우회해 3-small/3-large만 확보. `ada-002` 단가 `미확인`.
7. **OpenAI embeddings 가이드의 "pages per dollar" 표기 — 오염된 fetch를 격리한 기록** — 최초 fetch 시 가이드 문서가 가격을 "62,500 pages per dollar" 식으로 표기했고, fetch 요약 모델이 이를 잘못된 ¢/1M 값으로 환산했다(0.016¢/1M 등). **이 환산값은 전부 폐기했고 표에 넣지 않았다.** 가격은 모델 카드의 명시적 $/1M 값만 채택.
   - ⚠️ **그런데 차원·입력토큰 수치도 최초에 같은 응답에서 왔다.** 같은 응답의 가격을 신뢰할 수 없다고 판정했으면 차원도 같이 의심해야 한다 — 그래서 **가격을 일절 묻지 않는 별도 프롬프트로 재fetch**해서 인용문까지 확보했다: 1,536("the length of the embedding vector is `1536` for `text-embedding-3-small`"), 3,072("or `3072` for `text-embedding-3-large`"), 8,192(세 모델 공통). **모델 카드 페이지에는 차원·입력 한도가 없다**(별도 확인). 이 재검증 덕에 축 A의 핵심 결론이 인용문 기반으로 서게 됐다.
8. **"정형 데이터는 SQL로"에 대한 1차 소스 미확보** — 논리적으로 자명하나 인용 가능한 벤더 문장을 찾지 못했다. 저자 주장으로 처리하고 출처를 붙이지 말라.
9. **오버랩 권장 수치 미확보** — Pinecone 청킹 문서·Anthropic 글 모두 구체 오버랩 수치 없음.
10. **Weaviate `alpha` 기본값 미확보** — 문서가 `alpha=1`/`alpha=0`의 의미는 설명하나 기본값은 해당 페이지에 없음.
11. **Elasticsearch RRF 파라미터 기본값 미확보** — `rank_constant`·`rank_window_size` 기본값이 하이브리드 검색 페이지에 없음.
12. **Pinecone 최대 차원 미확보** — 인덱싱 개요 페이지에 dense 벡터 최대 차원 명시 없음.
13. **SPDX `NOASSERTION` 항목** — GitHub API가 라이선스를 판정하지 못한 항목(Elasticsearch, Redis/RediSearch, Meilisearch, pgvector, Langfuse, Phoenix, NeMo Guardrails, PurpleLlama, openai/evals)은 실제 라이선스 문구를 개별 확인하지 않았다. 본문에서 라이선스를 단정하지 말라.
14. **리포 이전(rename) 4건** — Ragas(`explodinggradients` → `vibrantlabsai`), NeMo Guardrails(`NVIDIA` → `NVIDIA-NeMo/Guardrails`), Chonkie(`chonkie-inc` → `feyninc`), 기타. 기존 URL은 리다이렉트되지만 **책에 URL을 박을 때 리다이렉트 후 주소를 쓰는 편이 안전**하다.

---

## 11. 미확인 항목 목록 (fact-checker 대조 기준 — 본문에서 단정 금지)

### 벤치마크 점수 (가장 위험)
- SWE-bench 리더보드 전 splits 최고 점수 — `미확인`
- GAIA 리더보드 전 점수 — `미확인`
- MTEB 리더보드 모델별 점수·순위 — `미확인`
- τ-bench / τ²-bench / τ³-bench 베이스라인 점수 — `미확인`
- WebArena 점수 — `미확인`
- AgentBench 점수 — `미확인`
- (확인된 유일 항목: Terminal-Bench 2.0 상위 10 — 2026-07-25 스냅샷)

### 임베딩·리랭커 가격·스펙 (두 번째로 위험)
- `text-embedding-ada-002` 단가 — `미확인`
- `text-embedding-ada-002` 차원 — `미확인` (가이드가 3-small/3-large 차원만 명시. 통념은 1,536이지만 이번 세션 미확인 — **본문에 1536을 박지 마라**)
- OpenAI moderation 가격 — "무료"만 확인, 세부 단가 `미확인`
- Langfuse 플랫폼↔SDK 버전 대응 관계 — `미확인` (계열이 셋으로 갈림)
- Cohere `embed-v4.0` 토큰 단가 — `미확인`
- Cohere `embed-*-v3.0` 계열 토큰 단가 — `미확인`
- Cohere `rerank-v4.0-pro` / `rerank-v4.0-fast` / `rerank-v3.5` 토큰 단가 — `미확인`
- Cohere `rerank-v4.0` 계열 컨텍스트 길이 — `미확인`
- Voyage `rerank-2.5` / `rerank-2.5-lite` 컨텍스트 길이 — `미확인`
- `voyage-context-4` 차원·컨텍스트 — `미확인`
- `voyage-4-nano` API 단가 — `미확인`
- `gemini-embedding-001` 차원·최대 입력 — `미확인`
- Jina `v5-omni` / `v5-text` 가격 — `미확인`
- Jina `v5-omni` Matryoshka 차원 하한 — `미확인`
- BGE 개별 모델 차원·컨텍스트 — `미확인`
- ColBERT 컨텍스트 — `미확인`
- Nomic Embed 모델명·차원·컨텍스트·라이선스 — `미확인` (문서 404)

### 버전
- pgvector 릴리스 발행일 — `미확인` (태그 `v0.8.5`만 확인, `releases/latest` 404)
- Azure AI Content Safety API 버전 — `미확인`
- Llama Guard 버전·파라미터 수·멀티모달·hazard 카테고리 수·라이선스명 — `미확인`
- Prompt Guard 버전 — `미확인`
- Lakera 버전·제품 상세 — `미확인`
- OpenAI Evals 버전 — `미확인` (릴리스·태그 미등록)
- Nomic Embed 버전 — `미확인`
- LanceDB 안정 릴리스 태그 — GitHub 최신 태그가 전부 beta (PyPI 0.34.0을 안정 기준으로 채택)
- Cognee 안정 릴리스 — 최신 태그가 `v1.4.0.dev0` (프리릴리스)
- GAIA 버전·라이선스 — `미확인`

### 매니지드 서비스 (버전 개념 없음 — 공백이 아니라 정답 셀)
- Pinecone, Turbopuffer, MongoDB Atlas Vector Search, LangSmith, Braintrust(플랫폼), Langfuse Cloud → `미확인 (managed service, 버전 개념 없음)`
- (셀프호스트 버전이 따로 있는 Langfuse는 `v3.224.1`로 별도 확인)

### 기타 스펙·수치
- 청킹 오버랩 권장 수치 — `미확인`
- Weaviate `alpha` 기본값 — `미확인`
- Elasticsearch `rank_constant` / `rank_window_size` 기본값 — `미확인`
- Pinecone dense 벡터 최대 차원 — `미확인`
- Turbopuffer per-GB / per-query / per-write 단가 — `미확인` (플랜 최소액만 확인: Launch $16/mo, Scale $256/mo, Enterprise ≥$4,096/mo + 35% 프리미엄)
- MongoDB Atlas 유사도 메트릭 종류 — `미확인`
- Langfuse 셀프호스팅 라이선스 종류 — `미확인` ("open source and you can self-host it for free"만 확인)
- Pinecone 청킹 문서 발행일 — `미확인`
- "정형 데이터는 SQL" 1차 소스 — `미확인`
- SPDX `NOASSERTION` 9건의 실제 라이선스 문구 — `미확인`

---

## 12. 집계

| 표 | 카테고리 | 도구 수 |
|----|---------|--------|
| 표 1 | 벡터 DB·검색 엔진 | 18 |
| 표 2 | 임베딩 모델 | 19 |
| 표 2-1 | 리랭커 | 7 |
| 표 3 | eval·관측성 | 15 |
| 표 4 | 에이전트 벤치마크 | 6 |
| 표 5 | 가드레일 | 10 |
| 표 6 | RAG 파이프라인·청킹 | 7 |
| **합계** | | **82** |

(표 2-2 MTEB는 표 3의 도구가 아니라 리더보드 현황 블록으로 별도 집계 제외. 표 1-1·5-1·6-1은 도구 표가 아닌 패턴·수치 표.)

**활동 신호 요약 (2026-07-25 기준)**
- 당일(2026-07-25) 푸시된 활발한 프로젝트: Qdrant, Weaviate, Milvus, Chroma, LanceDB, Vespa, Elasticsearch, Langfuse, Phoenix, Weave, Helicone, LlamaIndex, Haystack, Cognee, GraphRAG, NeMo Guardrails, OpenAI Agents SDK
- ⚠️ 정체(3개월 이상 푸시 없음): pgvectorscale(2026-04-30), Ragas(2026-02-24), OpenAI Evals(2026-04-14), SWE-bench(2026-04-01), AgentBench(2026-02-08), invariant(2026-01-12), sqlite-vec(2026-05-18), ColBERT(2025-10-14), rerankers(2025-12-20), WebArena(2025-11-26)
- ❌ 아카이브(죽은 프로젝트): **Rebuff** (`archived: true`, 마지막 릴리스 2024-01-20)
- 🔀 리포 이전: Ragas, NeMo Guardrails, Chonkie
- 📌 갓 나온 메이저: **Haystack v3.0.0 (2026-07-20, 5일 전)** — v2 기준 자료는 모두 구버전
