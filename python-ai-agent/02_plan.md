# 맨손으로 짓는 AI 에이전트 — 저술 계획 (라운드 2 갱신)

> 작성: 2026-05-16 · 1차 작성 후 plan-reviewer 라운드 1 피드백 반영 / 기반: `01_reference.md`
> 작업 슬러그: `python-ai-agent` (표지·EPUB 제목 슬러그는 `bare-hands-ai-agent`)
> 대상 독자: Python을 알고 LLM 기초(프롬프트·API 호출)는 있으나 에이전트는 처음 만드는 개발자
> 변경 요약: 3장 분할로 신규 4장 추가, 12장 분할로 신규 13장 추가, 1장 분량 격상, 5종 워크플로 명시, 9장(→10장) 페인포인트 1개 삽입. 전체 12장 → 14장으로 확장.

---

## 1. 제목 (확정)

**맨손으로 짓는 AI 에이전트**
부제: *Python SDK에서 LangChain, LangGraph까지 — 같은 에이전트를 세 번 다시 짓는다*
slug: `bare-hands-ai-agent` (작업 슬러그는 `python-ai-agent` 그대로 유지)
컨셉 한 줄: 똑같은 에이전트를 세 가지 추상화 레벨로 세 번 짓는다. 그러면 추상이 무엇을 대신해 주는지 비로소 보인다.
톤: 실전 가이드 + 약간의 철학. 토비 문체의 "함께 짠다" 청유형이 가장 잘 맞는다.

리뷰어 의견을 받아 **A로 확정**. 라운드 1 후보 B·C는 보관용으로만 남긴다(아래 부록 비고 참조).

> 표지 디자인 메모: 짧은 인용·SNS에서 부제가 잘리면 "맨손=프레임워크 안 쓰는 책"으로 오해될 수 있다. 표지에서 부제 폰트를 본 제목의 ~80% 비중으로 유지할 것 (cover-designer 단계 전달).

### 1차 라운드의 다른 후보 (기록)
- **B. LLM 루프와 그래프** — 약간 학구적
- **C. Python으로 만드는 AI 에이전트 — 본질에서 시작해 추상화까지** — 검색 친화적이나 차별화 약함

---

## 2. 책 특성

| 항목 | 값 |
|---|---|
| 장르 | 실전 가이드(중급 입문서) — 개념 설명 + 점진적 코드 누적 + 비교 |
| 본문 분량 (한글 글자 수) | **약 125,000자 ± 10%** (코드 블록 제외) |
| 코드 분량 비중 | 본문 텍스트 약 70%, 코드/표 약 30%. 코드 글자 수는 별도 산정 |
| 챕터 수 | **14장** (도입 1 + Part 1 다섯 장 + Part 2 세 장 + Part 3 세 장 + 마무리 2) |
| 챕터 평균 분량 | 7,500~10,000자. 마무리 13·14장은 8,000~9,000자 수준 |
| 난이도 곡선 | 초중급 시작(API 호출 한 줄) → 중급 중간(ReAct 루프 직접 구현) → 중급 상단(LangGraph 상태/사이클/HITL) |
| 코드 예제 누적 | 1부에서 만든 `mini_agent.py`를 책 전체의 캐논으로. 7장에서 LangChain 버전, 10장에서 LangGraph 버전. 같은 작업을 세 번 다시 짓는 구조 |
| 인용·각주 정책 | reference.md를 1차 출처로 사용. URL은 각주가 아닌 문단 끝 괄호 인용 또는 챕터 말미 "참고 자료"로 묶음 |

### 독자 여정 (한 단락)

1장을 펴는 시점의 독자는 "에이전트라는 단어가 도대체 뭐를 가리키는지 모르겠고, LangChain 튜토리얼을 따라 해도 내가 만든 게 뭔지 감이 안 잡히는" 상태다. 1장에서 정의를 못 박고 — Claude Code/Cursor/Devin의 실제 모양까지 보고 — 나면, 2~6장에서 SDK 한 줄 호출에서 출발해 도구 호출, ReAct 루프, ReAct를 넘어선 패턴들(Plan-and-Solve·Reflexion·ToT), 메모리, 안전장치까지 차곡차곡 쌓는 동안 "아, 에이전트는 결국 *루프*고 LLM은 그 루프 안의 한 함수구나"를 체감한다. 7~9장에서 같은 에이전트를 LangChain으로 다시 지으면서 "그래, 이걸 매번 내가 다시 짤 수는 없지"와 "근데 이건 굳이 추상화할 필요가 있었나"를 동시에 느낀다. 10~12장에서 사이클·상태·HITL이 필요한 진짜 사례를 만나 LangGraph로 옮긴 뒤, 13장에서 평가·관찰성을, 14장에서 보안과 비용 통제를 정리하며 "이제 내가 만든 걸 프로덕션 근처에 둘 수 있겠다"는 자신감으로 책을 덮는다.

---

## 3. 내러티브 아크

이 책의 동력은 단순한 난이도 상승이 아니라 **동기 부여의 흐름**이다.

먼저 1장이 안개를 걷는다 — "에이전트가 뭐냐"는 질문에 답하지 않고서는 책 전체가 공중에 뜬다. Simon Willison의 "tools in a loop", Anthropic의 "동적 자기 지시"를 나란히 두고, 이 책에서는 **"LLM이 도구를 부르는 루프"**를 작업 정의로 채택한다고 못 박는다. 그리고 Claude Code/Cursor/Devin의 실제 아키텍처를 1,500자 분량의 명시적 섹션으로 분석한다 — 이들이 모두 "단순 루프 + 좋은 도구 + 좋은 컨텍스트"라는 사실이 이 책 전체 입장의 실증 근거다. Anthropic 5종 워크플로 패턴(prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)을 표로 한 번 박아두고, 이 표는 책 본문 전체의 참조 좌표가 된다.

Part 1(2~6장)은 의도적으로 LangChain을 *쓰지 않는다*. 입문자가 LangChain부터 배우면 길을 잃는 결정적 이유는, 자기가 짜야 할 코드의 모양을 본 적이 없어 추상화가 무엇을 대신해 주는지 모르기 때문이다. 그래서 OpenAI/Anthropic SDK만으로 (a) tool 정의·호출 round-trip, (b) ReAct 루프, (c) ReAct를 넘어선 패턴 변종들, (d) 메모리 관리, (e) 무한 루프/컨텍스트 폭주/에러 처리/비용 캡까지 직접 짠다. 6장 끝에서 독자 손에는 ~200줄짜리 `mini_agent.py`가 남는다. 이게 책의 캐논이다. ReAct 직접 구현(3장)과 학술 변종 비교(4장)를 분리한 이유는 둘 다 자기 페이스로 깊게 다루기 위해서다.

Part 2(7~9장)는 "이 mini_agent를 LangChain으로 다시 짜면 뭐가 줄어들고 뭐가 늘어나는가"라는 질문 하나로 시작한다. 7장에서 LCEL과 Runnable로 같은 에이전트를 다시 짜고, 줄어든 줄 수와 늘어난 추상의 깊이를 같이 본다 — 단순 줄 수가 아니라 *import 그래프 깊이*, *추상의 단 수*, *부작용* 같은 측정 가능한 좌표로. 그리고 5종 워크플로 패턴이 LCEL의 `RunnableParallel`·conditional 분기와 어떻게 1:1 매핑되는지를 한 표로 보여준다. 8장에서는 LangChain이 진짜로 빛나는 영역인 통합·도구 생태계·LangSmith trace를 다룬다. 9장에서는 비판을 정면으로 받는다 — 추상화 과잉·breaking change·로깅 부재. Hamel Husain의 "골라 쓰는 라이브러리"라는 입장을 책의 입장으로 채택한다. smolagents를 한 페이지로 짧게 언급한다.

Part 3(10~12장)은 "LangChain만으로 안 되는 진짜 상황이 무엇인지"부터 시작한다. LCEL은 DAG라 사이클이 없고, 상태 공유와 human-in-the-loop, persistence가 빠진다. 10장에서 의도적 페인포인트 하나를 직접 만나본다 — "검색 결과가 비면 재시도 한 번"이라는 단순 요구사항을 LCEL로 짜려다 막히는 30~50줄짜리 시퀀스. 그 막힌 자리에서 mini_agent의 LangGraph 버전이 자연스럽게 나온다. 5종 워크플로 중 orchestrator-workers와 evaluator-optimizer가 LangGraph가 필요한 자리라는 사실도 여기서 한 번 더 못 박는다. 11장에서 supervisor/swarm 멀티 에이전트 패턴을 (회의적 시선과 함께) 다루며, 12장에서 체크포인터·스토어로 장기 메모리와 HITL을 붙인다.

마무리는 13장과 14장으로 나누었다. 13장은 평가와 관찰성, 14장은 보안과 비용 통제. 라운드 1에서는 한 챕터에 압축했으나 8토픽 10,000자는 자료 카탈로그가 될 위험이 있어 둘로 쪼갰다. 보안은 책의 "프로덕션 근처에 둘 수 있겠다"는 마무리 약속의 절반을 차지한다 — OWASP 4종 + 완화 패턴 + dual-LLM + lethal trifecta가 한 챕터를 받을 만하다. 14장 마지막 한 문단으로 독자에게 다음 걸음 — 자기 도메인의 에이전트 짓기 — 을 권한다.

---

## 4. 책에서 정한 입장

reference.md 9장에서 미해결로 남겨둔 논쟁점에 대해 이 책이 채택할 입장.

| 논쟁 | 책의 입장 | 한 줄 근거 |
|---|---|---|
| **에이전트의 정의** | "LLM이 도구를 부르는 루프"를 작업 정의로 채택. Anthropic의 좁은 정의("동적 자기 지시")는 1장에서 병기 | Willison: "definition can finally exist" — 가장 합의에 가까운 정의 |
| **LangChain을 권장하는가** | Part 1은 SDK로 본질을 익힌 뒤, Part 2에서 **선별적으로** 도입. "골라 쓰는 라이브러리, 통째로 삼키는 종교가 아니다" | Hamel Husain의 nuance — LangSmith 단독 사용까지 포함 |
| **Agent vs Workflow** | Anthropic의 "단순함 우선"을 디폴트. 사이클·상태·핸드오프가 필요한 진짜 사례에서만 LangGraph | "자율성은 비용이다" — Anthropic Building Effective Agents |
| **벡터 DB는 필수인가** | "벡터는 한 선택지". 코드 컨텍스트는 grep + 명시적 컨텍스트가 더 잘 통하는 영역도 있다 | Claude Code/Cursor/Devin 사례 — Mindstudio |
| **멀티 에이전트는 진짜 필요한가** | 회의적. supervisor + 1~2 worker가 입문 한계, 그 이상은 "혼자 잘 짠 한 에이전트"가 보통 이긴다 | Galileo 핑퐁 30회, Grid Dynamics brittle 후일담 |
| **한국어 환경** | 본문은 영어권 자료 기반이되, **한국어 부록**에서 한국어 프롬프트·tool description·평가셋 팁을 짧게 보강 | 한국어 자료는 입문 튜토리얼 위주, 프로덕션 후일담 빈약 |

---

## 5. 다루지 않는 것 (독자 기대 관리)

- **RAG 본격 다루기** — 13장에 한 페이지짜리 위치 설명. "RAG 책이 따로 있어야 할 주제"
- **로컬 모델(Llama/Qwen/Mistral) 기반 에이전트** — OpenAI/Anthropic SDK 기준. 로컬은 부록 B에서 한 페이지
- **음성·멀티모달 에이전트** — 텍스트+tool calling 범위로 한정
- **MCP(Model Context Protocol) 심층** — Claude Code 맥락에서만 짧게
- **AutoGen·MetaGPT·CrewAI 본격 튜토리얼** — 비교표(11장) + 부록 B 진입 가이드만
- **공개 벤치마크(ToolBench·API-Bank) 측정 방법** — 13장 평가 4종 분류에서 "task eval" 항목에 한 줄로 위치만 명시
- **에이전트로 코드 짜기/Claude Code 사용법** — 책의 *주제*가 아니라 *영감의 사례*. 동작 원리만 1장에서 설명

---

## 6. 챕터 목록 (전체 14장)

> "참고 reference 섹션"은 `01_reference.md`의 섹션 번호.

---

### 1장. 에이전트라는 단어가 마침내 뜻을 가지게 되었다 (도입)

- **핵심 질문:** "에이전트"가 무엇이며, 2026년 현재 가장 잘 동작하는 에이전트는 어떻게 생겼는가?
- **챕터 오프닝 hook:** Simon Willison 2025년 인용 — *"I think agent may finally have a widely enough agreed upon definition"* (reference 7-6)
- **주요 내용:**
  - "에이전트"라는 단어의 안개 — 챗봇·자동화 스크립트·자율 비행체까지 같은 단어를 쓰는 풍토
  - 세 가지 정의 비교: Anthropic의 좁은 정의("LLM이 자기 프로세스를 동적으로 지시"), Simon Willison의 실용 정의("tools in a loop"), 학술적 정의(Russell & Norvig)
  - 이 책의 작업 정의 채택과 그 이유
  - Agent vs Workflow의 스펙트럼 — Anthropic의 권고 "단순함 우선"
  - **Anthropic 5종 워크플로 패턴 표** — prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer. 각 패턴의 한 줄 정의 + 예시 + 책 본문에서 다시 호출되는 위치(7장 LCEL 매핑 / 10장 LangGraph 매핑) 명시. 이 표는 책 전체의 참조 좌표
  - **"2026년 실세계 에이전트는 어떻게 생겼는가" — 명시적 1,500자 섹션**: Claude Code 3단계 루프(gather context → take action → verify, CLAUDE.md 메모리, MCP 외부 도구) / Cursor의 인라인 모델 + Background Agents 분리 / Devin의 비동기 격리 환경(plan/write/test/PR). 공통 발견 — 화려한 그래프가 아니라 단순 루프 + 좋은 도구 + 좋은 컨텍스트. "이 책에서 짤 mini_agent도 결국 이 모양에 수렴한다"가 1장 끝의 약속
  - 이 책이 가는 길 — 같은 에이전트를 세 번 다시 짓는다 (SDK / LangChain / LangGraph)
- **핵심 코드 예제:** 없음 (또는 "에이전트가 아니다" 4줄과 "에이전트다" 12줄 코드의 짝 — 둘 다 미완 상태로 보여 호기심 유도)
- **이전 챕터와의 연결:** 책의 시작
- **다음 챕터로의 연결:** "그럼 가장 단순한 형태의 루프 — 한 바퀴짜리 — 부터 직접 짜보자"
- **예상 분량:** **8,500자** (기존 7,000자에서 1,500자 상향, Claude Code/Cursor/Devin 섹션 + 5종 워크플로 표 수용)
- **참고 reference 섹션:** 1, 2, 6.6, 9.3

---

## Part 1 도입: 맨손으로 짓는 에이전트

> 이 책의 Part 1은 LangChain을 일부러 쓰지 않는다. 추상이 무엇을 대신해 주는지 알려면, 한 번은 자기가 짤 코드를 직접 봐야 한다. 이 부의 끝(6장)에 독자 손에는 ~200줄짜리 `mini_agent.py`가 남는다. 책 끝까지 이 코드를 들고 다닐 것이다.

---

### 2장. 함수 하나 부르기 — Tool Use의 정확한 모양

- **핵심 질문:** LLM이 도구를 부른다는 게 정확히 어떤 입출력의 모양인가?
- **챕터 오프닝 hook:** "ChatGPT가 계산기를 부른다" 같은 비유는 편하지만, 실제 코드를 처음 마주하면 모두가 같은 질문에 부딪힌다 — "그래서 이 JSON은 누가 만들고 누가 실행하는 거지?"
- **주요 내용:**
  - 함수 한 개짜리 round-trip의 전체 그림 — `messages → tool_calls → 실행 → tool result → messages`
  - OpenAI와 Anthropic SDK의 표면 차이, 추상 수준의 동일성
  - `tool_calls`가 배열이라는 사실의 의미 — 한 번에 0/1/N개가 다 가능하다
  - JSON-encoded `arguments`의 함정 — 파싱 에러는 흔한 일이다
  - 도구 한 개 정의하는 법: 함수 시그니처 → JSON schema → SDK 등록
  - 도구 설계 원칙: Intern Test, 파라미터 최소화, enum으로 invalid state 차단
  - 함수 호출의 측정값 — 호출당 ~346 토큰 오버헤드, 정확도 97–99%, OpenAI 128개 한도
- **핵심 코드 예제:** `get_weather(city: str)` 하나만 가진 1-shot tool-call. 모델이 부르면 실행하고 결과를 다시 모델에 돌려 최종 답변을 받는 30~50줄짜리 코드
- **이전 챕터와의 연결:** 1장에서 정의한 "루프"의 가장 작은 단위 — 한 바퀴짜리 루프
- **다음 챕터로의 연결:** "한 바퀴 더 돌려야 할 때는?" → ReAct 루프
- **예상 분량:** 9,000자
- **참고 reference 섹션:** 2, 3.1, 3.2

---

### 3장. 도구를 여러 번, 스스로 결정해서 — ReAct 루프 짓기

- **핵심 질문:** 모델이 도구를 한 번이 아니라 *필요한 만큼* 부르게 하려면 코드의 모양이 어떻게 바뀌어야 하는가?
- **챕터 오프닝 hook:** ReAct 논문(Yao et al. 2022)의 한 줄 — *"interleave reasoning traces and actions"*. 추상적으로 들리지만, 코드로 옮기면 while 루프 하나다
- **주요 내용:** (라운드 2: 학술 변종은 신규 4장으로 분리, 3장은 ReAct 본체에 집중)
  - ReAct = Thought → Action → Observation → Thought의 반복. SDK 사용 시 "Thought"는 모델 응답에 자연어로 묻혀 있고, "Action"은 `tool_calls`, "Observation"은 `tool` role 메시지로 들어간다는 사실
  - 가장 단순한 ReAct 루프 — while True 안에 SDK 호출, tool_calls 비어 있으면 break
  - 도구 추가하기 — 계산기, 웹 검색(가짜), 메모 — 세 개로 확장
  - 모델이 어떤 도구를 부르는지 *결정하는 능력*과 *결정에 실패하는 방식* — hallucinated tool name, malformed JSON
  - 종료 조건의 세 분류 — 자연 종료(tool_calls 없음), 강제 종료(iteration cap), 비정상 종료(에러)
  - `mini_agent.py` v1 완성 — 도구 N개를 받아 ReAct 루프를 도는 함수
  - reference §3.4의 학술 변종(Plan-and-Solve, Reflexion, ToT)은 다음 장에서 본격 다룬다는 한 줄 예고
- **핵심 코드 예제:** `mini_agent.py` v1 (~80줄). 도구 N개를 받아 ReAct 루프를 도는 함수. 책 끝까지 이 함수를 들고 간다
- **이전 챕터와의 연결:** 2장의 한 바퀴 round-trip을 while로 감쌌을 뿐이라는 통찰
- **다음 챕터로의 연결:** "ReAct만 알면 끝인가? — 단순 CoT가 풀지 못하는 영역의 학술 패턴들" → 4장
- **예상 분량:** **9,000자** (기존 11,000자에서 2,000자 축소, 학술 변종 분리)
- **참고 reference 섹션:** 3.3

---

### 4장. ReAct 너머 — 루프 모양의 변종들 (Plan-and-Solve, Reflexion, ToT) *[신규]*

- **핵심 질문:** ReAct가 잘 안 통하는 영역에서 어떤 루프 모양이 시도되었고, 입문자는 이 중 무엇을 언제 꺼내야 하는가?
- **챕터 오프닝 hook:** *"Game of 24를 단순 CoT로 풀면 4%, Tree of Thoughts로 풀면 74%다. 같은 모델이다."* (reference 3.4)
- **주요 내용:**
  - **Plan-and-Solve** (Wang et al. 2023) — 단순 CoT의 missing-step 오류를 보완. "먼저 plan을 만들고, plan을 따라 subtask를 수행". `mini_agent`에 plan 단계를 끼우면 어떻게 되는가의 30줄 변형
  - **Reflexion** (Shinn et al. 2023) — verbal self-reflection을 episodic memory에 저장. HumanEval pass@1 GPT-4 80% → 91%. 실패 trial의 자기 메모를 다음 시도 시스템 프롬프트에 끼우는 패턴. 코드 25줄
  - **Tree of Thoughts** (Yao et al. 2023) — thought 단위 트리 탐색 + self-evaluation. Game of 24 4%→74%의 정량 의미. "branching factor와 LLM 호출 수의 곱" 비용 관점
  - **Voyager** (Wang et al. 2023) — skill library 메타 패턴. 과거 성공 경로를 재사용 가능한 함수로 누적. 책 본문에서는 "디자인 영감"으로 한 페이지
  - **LATS** (Zhou et al. 2023) — Tree Search + Reflexion의 결합. 한 단락으로 위치만
  - 결정 가이드: 작업 성공률이 안정적이면 ReAct 그대로 / multi-step planning이 필요하면 Plan-and-Solve / 실패 trial에서 *학습*이 필요하면 Reflexion / 탐색·평가의 trade-off가 필요한 deliberate decision이면 ToT
  - "이 다섯 패턴이 결국 *루프 모양의 변형*이라는 사실, 그리고 LangChain·LangGraph가 이 변종들을 어떻게 흡수하는가"는 7장·10장의 호출 예고
- **핵심 코드 예제:** 세 가지 변종을 `mini_agent.py`에 끼운 *짧은 diff* 3개 (Plan-and-Solve 변형, Reflexion 변형, ToT는 의사코드)
- **이전 챕터와의 연결:** 3장 ReAct의 한계를 받아내는 자리
- **다음 챕터로의 연결:** "패턴이 뭐든 history는 길어진다. 기억을 어떻게 다룰까" → 5장
- **예상 분량:** 8,000자
- **참고 reference 섹션:** 3.4

---

### 5장. 기억의 모양 — 대화 history는 어디서 잘리고, 어디로 흘러가는가

- **핵심 질문:** 에이전트의 "기억"은 결국 무엇이며, 컨텍스트 윈도우를 넘기지 않으려면 어떤 전략을 쓰는가?
- **챕터 오프닝 hook:** Memory survey(2026)의 네 분류 — short-term / long-term / episodic / semantic. 이름은 멋지지만, 코드로 내려오면 결국 "리스트를 어떻게 자르느냐" 문제다
- **주요 내용:**
  - 메모리 4축 정의와 코드 매핑 — short-term=현재 messages, long-term=DB, episodic=과거 trial 자기 메모(4장 Reflexion 재인용), semantic=지식 베이스(RAG)
  - 가장 단순한 전략: sliding window (마지막 N턴만)
  - summary buffer — 오래된 턴을 한 줄 요약으로 갈음
  - 외부 저장소로 spillover — SQLite, JSON 파일로 시작해도 충분하다
  - RAG는 여기서 다루지 않는다는 선언 — semantic memory는 13장과 부록 B에서 위치만 잡는다
  - "Claude Code는 vector DB가 아니라 grep을 쓴다"의 시사 — 모든 메모리 문제가 RAG로 풀리는 건 아니다 (1장 사례 분석의 재인용)
- **핵심 코드 예제:** `mini_agent.py` v2 — 메모리 클래스(`Memory`)를 추가. sliding window + summary 두 모드 지원
- **이전 챕터와의 연결:** 3장 ReAct 루프와 4장 변종들의 공통 문제 — history가 매 iteration마다 길어진다
- **다음 챕터로의 연결:** "그런데 history만 잘 관리한다고 끝이 아니다. 루프 자체가 폭주하면?"
- **예상 분량:** 9,000자
- **참고 reference 섹션:** 2(메모리 행), 3.5, 9.4

---

### 6장. 무한 루프와 청구서 — 에이전트가 망가지는 다섯 가지 모양

- **핵심 질문:** 프로덕션 직전에 반드시 손에 익혀야 할 안전장치는 무엇이고, 어디에 끼워 넣어야 하는가?
- **챕터 오프닝 hook:** *"$0.08짜리 작업이 4시간 동안 무한 루프로 $2,847이 되었다"*. 토큰 1회 500이 15회 4M으로 폭증한 실제 사례 (reference 7-1)
- **주요 내용:**
  - 망가지는 다섯 가지 모양: 무한 루프 / 컨텍스트 overflow / hallucinated tool / malformed JSON / 재시도 폭주
  - 하드 캡 4종 세트: iteration cap, token cap, time cap, spend cap. 어디서 측정하고 어디서 끊는가
  - 재시도 전략 — exponential backoff, idempotent tool 설계, 5xx vs 4xx 구분
  - 도구 실행을 *격리*한다는 의미 — try/except로 감싸 모델에게 에러 메시지를 다시 던지면, 모델이 보통은 자기가 정정한다
  - prompt injection의 한 페이지짜리 미리보기 — Simon Willison의 lethal trifecta는 14장에서 본격적으로
  - 관찰성의 최소한 — print debugging부터 OpenTelemetry까지의 거리. LangSmith는 8장에서
- **핵심 코드 예제:** `mini_agent.py` v3 — 모든 안전장치를 끼운 최종 버전. ~200줄. 책 전체의 캐논 코드
- **이전 챕터와의 연결:** 2~5장에서 짠 코드의 운영 안전망. Part 1의 마지막
- **다음 챕터로의 연결:** "이걸 매번 내가 다시 짤 수는 없겠다"는 자연스러운 피로감 → Part 2
- **예상 분량:** 10,000자
- **참고 reference 섹션:** 3.6, 6.2, 7-1, 7-8

---

## Part 2 도입: LangChain — 추상화의 가치와 비용

> Part 1에서 짠 `mini_agent.py`를 LangChain으로 다시 짠다. 줄어든 줄 수와 늘어난 추상의 깊이를 동시에 보면, "LangChain은 종교가 아니라 골라 쓰는 라이브러리"라는 입장이 자연스럽게 따라온다. 이 부의 끝에 독자는 "이 모듈은 쓰겠고, 이 모듈은 안 쓰겠다"를 자기 기준으로 정할 수 있다.

---

### 7장. 같은 에이전트, 두 번째로 짓기 — LangChain과 LCEL

- **핵심 질문:** Part 1의 `mini_agent.py`를 LangChain으로 다시 짜면 어디가 줄어들고 어디가 늘어나는가?
- **챕터 오프닝 hook:** *"OpenAI API 한 줄을 부르려고 클래스 셋을 거친 날"* (reference 7-3). 농담 같지만, LCEL은 그 클래스 셋이 *왜* 거기 있는지 설명한다
- **주요 내용:**
  - LangChain이 대신해 주는 네 가지 — 공통 인터페이스, LCEL 합성, 통합 모듈, 관찰성
  - `Runnable` 추상: `.invoke()`, `.batch()`, `.stream()`, `.ainvoke()` 한 인터페이스의 의미
  - LCEL 파이프 합성 `prompt | llm | parser` — `__or__` 오버로딩의 가독성과 함정
  - `RunnableParallel`, `RunnablePassthrough` — 병렬과 분기를 *코드*가 아니라 *조합*으로 표현
  - **5종 워크플로 ↔ LCEL 매핑 표** (1장 표의 재호출): prompt chaining → `|` / routing → `RunnableBranch` / parallelization → `RunnableParallel` / orchestrator-workers·evaluator-optimizer → "LCEL로는 매끄럽지 않다, 10장 LangGraph에서 본다"
  - 도구 정의의 변화 — `@tool` 데코레이터와 `BaseTool` 상속. JSON schema를 손으로 안 써도 된다 (그리고 그 마법이 일으키는 inspect 부작용도 같이 본다)
  - mini_agent의 LangChain 버전 — 같은 동작, 줄어든 보일러플레이트
  - **"추상의 깊이" 측정 좌표 (라운드 2 보강)**: (a) `mini_agent.py`와 `mini_agent_lc.py`의 import 그래프 깊이 비교(직접 의존성 트리), (b) tool 등록 한 동작의 호출 트레이스 — SDK N줄 vs LangChain `BaseTool → Runnable → ABC` 추상 N단, (c) "추상이 늘어난 자리" 3~4개 구체 예: `@tool`의 inspect 마법, LCEL `__or__`의 부작용, `RunnableConfig` 전파, callback 흐름
  - 줄 수 비교 수치는 **저술 단계에서 실측 후 갱신**(예상치를 본문에 박아두지 않는다)
  - `with_retry()`, `with_fallbacks()`는 "내장된 회복력"이 아니라 "내장된 토큰 비용"이라는 점도 같이 본다 (9장 비판의 예고)
- **핵심 코드 예제:** mini_agent의 LangChain 재구현 `mini_agent_lc.py`. 1부 캐논과 줄 수·import 그래프·구성요소를 표로 3-way 비교
- **이전 챕터와의 연결:** 6장에서 완성된 SDK 버전과의 정면 비교
- **다음 챕터로의 연결:** "LangChain의 진짜 강점은 mini_agent 수준이 아니라 *생태계*다" → 8장
- **예상 분량:** 11,000자
- **참고 reference 섹션:** 2(워크플로 5종), 4.1, 4.2

---

### 8장. LangChain이 진짜로 빛나는 자리 — 통합, 도구 생태계, LangSmith

- **핵심 질문:** LangChain의 어떤 부분은 "내가 다시 짤 가치가 없는 것"인가?
- **챕터 오프닝 hook:** Hamel Husain의 한 줄 — *"처음엔 LC에 짜증냈다. 그런데 업계 사람들은 다 쓰고 있더라. 알고 보니 그들은 사용자에게 광적으로 귀를 기울인다"* (reference 7-5)
- **주요 내용:**
  - 통합(integration)의 양과 의미 — 벡터 DB, 로더, retriever, callback 수백 개를 다시 짤 일이 없다
  - 도구 생태계 — `langchain_community.tools` 안에 이미 있는 것들의 카탈로그 둘러보기
  - LangSmith trace 도입 — "그래서 모델이 뭘 봤지?"라는 6장의 질문에 처음으로 제대로 답한다
  - trace를 읽는 법 — 단계별 입출력, 토큰 비용, 시간. 디버깅 detective work의 종결
  - 평가의 한 페이지짜리 미리보기 — dataset, evaluator, run. 본격적인 평가는 13장
  - LangSmith는 LangChain 본체와 *분리해* 쓸 수 있다 — Hamel의 nuance
  - "이걸 쓰지 마라" 목록: 1차 deprecation 흐름(`ConversationBufferMemory`류, 0.3 이전 chain API)
- **핵심 코드 예제:** mini_agent_lc에 LangSmith trace 붙이기. 같은 실행을 trace 화면 발췌 또는 trace JSON 발췌로 보여준다
- **이전 챕터와의 연결:** 7장에서 본 LangChain의 *합성 측면*에 이어 *생태계 측면*
- **다음 챕터로의 연결:** "그렇다면 LangChain의 *나쁜* 부분은 무엇인가" → 9장
- **예상 분량:** 9,000자
- **참고 reference 섹션:** 4.1, 4.2, 6.1

---

### 9장. LangChain의 그늘 — 비판, 옹호, 그리고 골라 쓰기

- **핵심 질문:** LangChain을 *얼마나* 받아들이고 *어디서* 거절할지 어떻게 정할까?
- **챕터 오프닝 hook:** 3개 이상 소스에서 반복되는 6가지 비판 — 추상화 과잉, breaking change, 문서 vs 실제 불일치, 로깅 부재, 숨은 비용, production error handling 부재 (reference 4.3)
- **주요 내용:**
  - 6가지 비판을 항목별로 검증 — 어느 정도까지 사실이고, 어디부터 과장인가
  - breaking change의 실제 모양 — 0.1 → 0.2 → 0.3 사이의 주요 변경 사례 한두 개
  - "숨은 비용"이 가시화되는 자리 — `with_retry()`가 토큰을 어떻게 먹는지(7장 예고의 회수)
  - 옹호 의견 정리 — Hamel, 표준화의 가치, 사용자 응답성
  - smolagents — ~1,000줄짜리 대안. code agent 패러다임(파이썬 코드 자체를 액션으로). 한 페이지로 단정하게 소개
  - 이 책의 입장 명문화: "LangChain은 골라 쓰는 라이브러리, 통째로 삼키는 종교가 아니다". `langchain_core` + LangSmith까지만 쓰고 나머지는 직접 짜는 hybrid 패턴
  - 결정 트리: "이 기능이 필요하면 LangChain 쓰자 / 이 기능이면 직접 짜자"의 한 페이지 가이드
- **핵심 코드 예제:** 작은 코드 단편 3개 — (a) `with_retry()`의 토큰 비용 가시화, (b) smolagents 코드 에이전트 hello-world(8~12줄), (c) `langchain_core`만 쓰고 나머지는 SDK로 가는 hybrid 패턴
- **이전 챕터와의 연결:** 7·8장에서 본 좋은 면의 정직한 반대편
- **다음 챕터로의 연결:** "이제 LangChain이 *못 하는* 진짜 영역으로 간다" → Part 3
- **예상 분량:** 10,000자
- **참고 reference 섹션:** 4.3, 4.4

---

## Part 3 도입: LangGraph — 상태와 그래프로 다시 생각하기

> LangChain의 LCEL은 본질적으로 DAG다. 사이클·상태·HITL·persistence가 필요한 진짜 사례를 만나면 그래프가 필요하다. 이 부에서 mini_agent를 세 번째로, 마지막으로 다시 짓는다. 그러면 "에이전트는 루프"라는 1장의 정의가 "에이전트는 *상태를 가진 그래프 위의 루프*"로 자연스럽게 확장된다.

---

### 10장. LCEL의 한계와 그래프의 등장 — mini_agent를 세 번째로 짓기

- **핵심 질문:** LangChain의 chain만으로 안 되는 진짜 상황은 무엇이고, 그래프는 그것을 어떻게 푸는가?
- **챕터 오프닝 hook:** *"우리가 짜야 했던 것은 '한 번 더 시도'였다. LCEL에서는 그게 안 된다 — DAG이기 때문이다."*
- **주요 내용:** (라운드 2: 의도적 페인포인트 시퀀스를 본문 초반에 명시적으로 배치)
  - **[페인포인트 시퀀스 — 9장에서 10장으로 넘어오는 동력]**: 추가 요구사항 한 줄을 도입한다 — "웹 검색 도구의 결과가 비면 검색어를 다시 만들어 한 번 더 시도한다". 7장의 `mini_agent_lc`(LCEL 기반)에 이 요구사항을 끼우려 30~50줄짜리 시도를 한다. *실제로 막힌다* — chain이 DAG라 자기 자신으로 돌아오는 엣지가 없고, 조건부 분기는 가능해도 *루프*는 우회로(while + 재호출)로만 가능. 그 우회로 코드가 어떻게 추하게 부풀어 오르는지 보여준 뒤, 같은 동작을 `StateGraph`로 옮기면 어떻게 깔끔해지는지 보여준다
  - DAG가 못 하는 다섯 가지: 사이클, 공유 상태, HITL, persistence, 멀티 에이전트 핸드오프
  - StateGraph 핵심 API — TypedDict 상태, `add_node`, `add_edge`, `add_conditional_edges`, `compile`
  - 노드는 `state -> partial state` 함수다. 이게 LangGraph의 단 하나의 약속
  - 조건부 엣지 — 라우팅 로직은 코드, 의사결정은 LLM
  - mini_agent의 LangGraph 버전 — 같은 ReAct 루프를 그래프로 표현. 노드 두 개(LLM 추론, tool 실행), 엣지 하나의 조건 분기
  - **5종 워크플로 ↔ LangGraph 매핑 호출**: 7장 표의 미해결 두 칸(orchestrator-workers, evaluator-optimizer)이 마침내 LangGraph로 자연스럽게 떨어진다는 사실을 표로 못 박는다
  - 그래프 시각화 — `graph.get_graph().draw_mermaid()`로 흐름을 그림으로 본다
- **핵심 코드 예제:** (a) "재시도 한 번"의 LCEL 막힘 코드 30~50줄, (b) 같은 요구를 푼 `mini_agent_lg.py`. 1부/2부/3부 mini_agent 3-way 비교표(줄 수, 의존성, 변경 용이성, 사이클 가능성)
- **이전 챕터와의 연결:** 9장 결말에서 던진 "LangChain이 못 하는 영역"의 응답. 그리고 7장 5종 워크플로 매핑 표의 미해결 칸 회수
- **다음 챕터로의 연결:** "그래프가 진짜 필요한 사례 — 멀티 에이전트" → 11장
- **예상 분량:** 11,000자
- **참고 reference 섹션:** 2(워크플로 5종), 5.1, 5.2

---

### 11장. 여러 에이전트가 같이 일할 때 — Supervisor, Swarm, 그리고 회의 한 줌

- **핵심 질문:** 멀티 에이전트는 진짜로 더 똑똑한가, 아니면 그냥 더 복잡한가?
- **챕터 오프닝 hook:** *"고객 한 명 문의에 핑퐁이 30번 오갔다. 어디서 실패했는지 찾는 데 한나절이 걸렸다"* (reference 7-2, Galileo)
- **주요 내용:** (라운드 2: 4종 패턴 분류는 표 1장으로 압축, AutoGen/CrewAI 비교표는 부록 B로 이동해 본문 밀도 확보)
  - 멀티 에이전트 패턴 4종 — Supervisor / Hierarchical / Swarm·Handoff / Tool-calling supervisor. **표 한 장**으로 정리
  - Supervisor 패턴을 LangGraph로 — supervisor 노드 1개 + worker 노드 2~3개. 한 챕터 안에 완결되는 예제(리서치 에이전트 + 작성 에이전트 + 편집 에이전트). **목표 길이 50~80줄, 진짜로 80줄을 넘기지 않는다**
  - 핸드오프의 함정 — context loss, ping-pong, prompt drift. **핸드오프 ping-pong 시각화 1개** (같은 정보를 3번 다시 인용하는 모양)
  - AutoGen·MetaGPT·CrewAI는 **본문에서 한 단락만**, 자세한 비교표·진입 가이드는 부록 B로 — *대화*로 푸는 길과 *그래프*로 푸는 길의 한 줄 차이만 본문에 남긴다
  - 회의적 시선: Grid Dynamics의 "LangGraph + Redis brittle in practice" 후일담을 정직하게 소개
  - 이 책의 권고: supervisor + 1~2 worker가 입문 한계, 그 이상은 보통 "혼자 잘 짠 한 에이전트"가 이긴다
  - "그런데 정말 멀티가 필요한 자리"의 두 가지 — (1) 도메인이 명확히 분리된 도구 묶음, (2) 병렬 처리로 시간을 줄여야 하는 작업
- **핵심 코드 예제:** Supervisor 패턴 데모 — 3-agent 리서치 워크플로(리서처/라이터/에디터). 50~80줄
- **이전 챕터와의 연결:** 10장의 단일 에이전트 그래프를 다중으로 확장
- **다음 챕터로의 연결:** "여러 에이전트의 상태를 *어떻게 저장하고 부활시키는가*" → 12장
- **예상 분량:** 9,000자 (밀도 분배: 4종 패턴 표 800자 / Supervisor 데모 + 코드 2,800자 / 핸드오프 함정 1,500자 / 다른 프레임워크 한 단락 800자 / Grid Dynamics 1,200자 / 권고 + 멀티 필요 자리 1,900자)
- **참고 reference 섹션:** 5.3, 5.4, 5.5, 7-2, 7-7, 9.5

---

### 12장. 상태를 저장하고, 사람을 끼우고, 다시 깨우기 — Checkpointer와 HITL

- **핵심 질문:** 장시간 대화·승인 단계·실패 후 재개를 코드 한 줄로 추가하려면 무엇이 있어야 하는가?
- **챕터 오프닝 hook:** *"한 시간 전 대화의 다음 턴을 자연스럽게 이어 받는다. 비결은 모델이 똑똑해진 게 아니라, 그래프가 자기 상태를 저장해뒀기 때문이다."*
- **주요 내용:**
  - Checkpointer 추상 — 그래프 실행 매 step의 상태를 외부 저장소에 적는다. SQLite로 시작, Postgres로 옮긴다
  - `compile(checkpointer=...)` 한 줄로 추가되는 능력 — 시간 여행 디버깅, 실패 후 재개, 멀티 세션
  - Store 추상 — long-term memory(사용자별 프로필, 학습된 선호 등). short-term(checkpointer)과의 분담
  - `interrupt()` — 그래프가 특정 노드 앞에서 일시정지하고 사람의 입력을 기다린다. 승인이 필요한 destructive action에 필수
  - HITL UI의 최소 구현 — CLI에서 prompt, web에서는 webhook 패턴
  - 멀티 사용자/멀티 세션을 안전하게 — thread_id, user_id의 분리
  - 실패 시 재개의 정확한 모양 — checkpoint에서 마지막 성공 상태를 읽고, 실패한 노드부터 재시도
- **핵심 코드 예제:** mini_agent_lg에 SQLite checkpointer + interrupt 추가. "이 도구 호출을 정말 실행할까요? (y/n)"로 멈춰서는 데모
- **이전 챕터와의 연결:** 11장의 멀티 에이전트 그래프도 결국 같은 checkpointer로 다뤄진다
- **다음 챕터로의 연결:** "이제 짓는 법은 알았다. 그런데 *어떻게 측정하고 어떻게 안전하게 운영하는가*" → 13장
- **예상 분량:** 9,000자
- **참고 reference 섹션:** 5.1, 5.2

---

## 마무리 두 챕터 도입

> 라운드 1에서는 평가·관찰성·보안·비용을 한 챕터 10,000자에 압축했으나, 8토픽을 마무리에 욱여넣으면 자료 카탈로그가 된다. 그래서 13장은 평가와 관찰성, 14장은 보안과 비용 통제로 분리했다. 보안은 책의 "프로덕션 근처에 둘 수 있겠다"는 마무리 약속의 절반을 차지한다.

---

### 13장. 측정과 관찰성 — 평가 4종과 trace를 읽는 법

- **핵심 질문:** 에이전트가 *제대로 동작하는지*를 어떻게 측정하고, 망가지는 순간을 어떻게 *보는가*?
- **챕터 오프닝 hook:** *"분당 50달러를 태우며 reasoning loop가 돌고 있었다. 그런데 모니터링 대시보드의 status는 'up'이었다"* (reference 7-8)
- **주요 내용:**
  - 평가 4종 — unit eval(도구 호출 정확도), task eval(전체 작업 성공률), regression eval(이전 버전 대비), online eval(프로덕션 샘플링)
  - 공개 벤치마크 한 줄 위치 — "ToolBench, API-Bank가 있다. 측정 방법까지 들어가지는 않는다"
  - 도구 비교 — LangSmith / Braintrust / Ragas / DeepEval / Arize Phoenix. 본문에서는 **추천 조합 2종만 본격 다룸**: (RAG + LangChain stack) → RAGAS + LangSmith / (Mixed + CI gate) → DeepEval + Braintrust. **5종 도구 비교표 자체는 부록 C로 분리**
  - 관찰성 3축 — trace, metric, log. trace는 LangSmith, metric은 OpenTelemetry, log는 표준 로깅
  - "trace를 읽는 일상" — 실패한 한 trace를 읽고 어디서 막혔는지 찾아내는 5분짜리 워크스루
  - RAG의 위치 — 한 페이지로 "이건 별도 책"이라는 선언과 RAGAS의 의미 (semantic memory의 평가)
  - 평가셋을 어디서 시작하나 — 10개부터, golden set의 합리적 크기
- **핵심 코드 예제:** (a) LangSmith eval 한 개(unit eval), (b) DeepEval CI gate 설정 단편, (c) trace JSON에서 실패 원인 찾기 한 페이지
- **이전 챕터와의 연결:** 12장에서 상태를 저장했다면, 이제 그 상태가 *옳은지*를 본다
- **다음 챕터로의 연결:** "측정했으니 안전하게 운영하는 법" → 14장
- **예상 분량:** 8,000자
- **참고 reference 섹션:** 6.1, 6.5, 6.6, 7-8

---

### 14장. 안전하게 운영하기 — 보안, lethal trifecta, 비용 통제

- **핵심 질문:** 에이전트가 *나를 공격하는 상황*을 어떻게 막고, *나도 모르게 청구서가 폭주하는 상황*을 어떻게 막는가?
- **챕터 오프닝 hook:** Simon Willison의 lethal trifecta — *"사적 데이터 접근 + 신뢰할 수 없는 콘텐츠 노출 + 외부 통신 능력. 이 셋을 동시에 가진 에이전트는 공격자가 데이터 유출을 트리거하기 쉽다"* (reference 6.4)
- **주요 내용:**
  - **lethal trifecta 한 페이지 액자** — 세 능력의 교집합이 왜 위험한지, 자기 에이전트 설계에서 셋 중 무엇을 빼면 되는지
  - 보안 4종 위협 — direct prompt injection / indirect prompt injection / tool manipulation / context poisoning (OWASP LLM01:2025)
  - 완화 패턴 4종 — **Action screening** (도구 호출을 user intent와 대조해 drift 시 거부), **Dual-LLM 패턴** (privileged LLM은 도구 보유하되 untrusted content를 직접 안 읽음, quarantined LLM은 content 읽되 도구 없음), **least privilege scope**, **destructive action 사람 승인** (12장 `interrupt()`의 안전성 회수)
  - input·output 분류기 — regex만으로는 부족, 모델 기반 분류기 권장. 가드레일 LLM도 LLM이라 자체 injection에 취약 → 다층 방어
  - **비용 통제 4종 캡(6장 회수 + LangGraph 끼우기)** — iteration cap, token cap, time cap, spend cap. 6장 SDK 버전에서 짠 코드를 LangGraph state·middleware로 옮기는 패턴
  - 레이턴시 통제 — async, streaming, prefetch, parallel tool calls
  - 마지막 한 문단의 송사 — "이제 자기 도메인의 에이전트를 짓자. 이 책의 14장이 결국 한 문장으로 줄어든다 — *LLM이 도구를 부르는 루프를, 필요한 만큼만 추상화한다*"
- **핵심 코드 예제:** (a) Action screening 12줄 패턴, (b) Dual-LLM 분리 패턴 20줄, (c) 4종 캡을 LangGraph state에 끼운 데코레이터/미들웨어 패턴, (d) 비용 모니터링 hook
- **이전 챕터와의 연결:** 13장에서 본 trace에서 발견한 실패가 *공격*일 수도 있다는 시점 전환
- **다음 챕터로의 연결:** 본문의 끝. 부록으로
- **예상 분량:** 9,000자
- **참고 reference 섹션:** 6.2, 6.3, 6.4, 7-8

---

## 7. 부록

> 본문 외 부록을 세 개 둔다. 본문 분량 산정에는 포함하지 않는다. 라운드 2에서 부록 C(평가 도구 비교표)가 추가되었다.

- **부록 A: 한국어 환경 팁** (~3,000자) — 한국어 프롬프트의 tone 차이, tool description 영어/한국어 혼합, 한국어 평가셋 만들기, teddylee777/langchain-kr·WikiDocs 큐레이션
- **부록 B: 다루지 않은 길로 가는 지도** (~3,500자, 기존 2,000자에서 1,500자 확장) — 로컬 모델, MCP, AutoGen/CrewAI/MetaGPT 진입 가이드 **(각 프레임워크마다 "이걸로 시작하려면 여기를 읽으세요" 한 단락 명시)**, RAG 책, 음성/멀티모달, ChatDev — 각각 한 단락씩
- **부록 C: 평가/관찰성 도구 비교표 *[신규]*** (~2,000자) — LangSmith·Braintrust·Ragas·DeepEval·Arize Phoenix 5종 비교표 (강점·약점·가격 모델·언제 무엇). 13장에서 본문 압축을 위해 분리

---

## 8. 분량 합계 검증

| 챕터 | 라운드 1 → 라운드 2 |
|---|---|
| 1장 도입 | 7,000 → **8,500** (+1,500: Claude Code/Cursor/Devin 1,500자 섹션 + 5종 워크플로 표) |
| 2장 Tool Use | 9,000 (유지) |
| 3장 ReAct 루프 | 11,000 → **9,000** (-2,000: 학술 변종 분리) |
| **4장 ReAct 변종 *[신규]*** | — → **8,000** |
| 5장 메모리 | 9,000 (유지, 챕터 번호 +1) |
| 6장 망가지는 모양 | 10,000 (유지, 챕터 번호 +1) |
| 7장 LangChain 재구현 | 11,000 (유지, 챕터 번호 +1) |
| 8장 LangSmith·생태계 | 9,000 (유지, 챕터 번호 +1) |
| 9장 LangChain 비판 | 10,000 (유지, 챕터 번호 +1) |
| 10장 LangGraph 등장 | 11,000 (유지, 챕터 번호 +1, 페인포인트 시퀀스 본문 명시) |
| 11장 멀티 에이전트 | 9,000 (유지, 챕터 번호 +1, 밀도 분배 명시) |
| 12장 Checkpointer·HITL | 9,000 (유지, 챕터 번호 +1) |
| **13장 평가·관찰성 *[분리]*** | 10,000 일부 → **8,000** |
| **14장 보안·비용 *[분리]*** | 10,000 일부 → **9,000** |
| **본문 합계** | 115,000 → **128,500** |
| 부록 A | 3,000 |
| 부록 B (확장) | 2,000 → **3,500** |
| **부록 C *[신규]*** | — → **2,000** |
| **총합** | 120,000 → **137,000자** |

목표 범위(80,000~150,000) 안. 라운드 1 분량(120k) 대비 17k 증가 — 챕터 2개 추가와 1장 상향분이 주요 증분.

---

## 9. 자기 점검 (book-planning 체크리스트)

- [x] 모든 챕터가 핵심 질문에 답하고 있는가 — 각 챕터 핵심 질문 1줄로 명문화 (14장 전부)
- [x] 챕터 순서에 맥이 흐르는가 — Part 1(짓기) → Part 2(추상화) → Part 3(상태·그래프) → 마무리 둘(측정·안전). 부 도입글로 동기 부여 흐름 명시
- [x] 대상 독자 수준에 맞는가 — 2장에서 LLM 기초는 가정, function calling은 "정확히 어떤 모양"으로 짚고 감
- [x] 레퍼런스 주요 자료가 빠짐없이 배치되는가 — reference 섹션 1~7의 자료를 챕터별로 매핑 완료. §6.6(Claude Code 사례)은 1장 격상으로 핵심 자산화. §3.4(학술 변종)는 신규 4장으로 격상. §6.5(벤치마크)는 13장에 한 줄 위치 명시. 부록 A·B·C가 한국어/타 프레임워크/평가 도구 비교 흡수
- [x] 챕터 간 중복이 없는가 — 메모리는 5장(SDK)·8장(LangChain 권고)·12장(checkpointer/store)으로 *층위가 다르게* 다룸. 평가는 8장(미리보기)·13장(본격)·부록 C(도구 표)로 분리. 비용 캡은 6장(SDK 직접 구현)·14장(LangGraph 끼우기)로 회수 구조
- [x] 5종 워크플로 패턴이 본문에서 추적 가능한가 — 1장 표 도입 → 7장 LCEL 매핑 → 10장 LangGraph 매핑. 3회 호출되어 책 전체의 참조 좌표 역할
- [x] 페인포인트 동기가 챕터 간 흐름에서 살아 있는가 — 6장 끝(피로감), 9장 끝(LangChain 한계), 10장 본문 초반(LCEL 막힘 시퀀스), 11장 hook(핑퐁 30회), 13장 hook($50/min) — 각 전환점마다 손에 잡히는 페인포인트 1개
- [x] 분량 합계가 목표에 부합하는가 — 본문 128,500자, 부록 8,500자, 총 137,000자. 목표 범위(80k~150k) 안

---

## 10. 라운드 1 액션 아이템 반영 결과

| # | 액션 아이템 | 반영 결과 |
|---|---|---|
| 1 | 3장 분할 | 3장은 ReAct 본체로 좁혀 11,000→9,000자. 신규 4장 "ReAct 너머 — 루프 모양의 변종들" 8,000자 추가. Plan-and-Solve·Reflexion·ToT·Voyager·LATS 모두 본문에 자리 잡음 (부록행 아님) |
| 2 | 1장 Claude Code 사례 격상 | 1장 분량 7,000→8,500자. 그중 1,500자를 "2026년 실세계 에이전트는 어떻게 생겼는가" 명시 섹션으로 할당. Claude Code 3단계 루프 / Cursor 인라인+백그라운드 / Devin 비동기 격리 아키텍처. "이 책에서 짤 mini_agent도 결국 이 모양에 수렴한다"를 1장 끝 약속으로 명문화 |
| 3 | 5종 워크플로 패턴 명시적 자리 | 1장 주요 내용에 "5종 워크플로 패턴 표 — 책 전반의 참조 좌표"로 박음. 7장 LCEL 매핑 표 1회 호출, 10장 LangGraph 매핑 표 1회 호출 — 총 3회 명시적 등장으로 추적 가능 |
| 4 | 12장 분리 | **선택지 (a) 채택** — 13장(평가·관찰성) / 14장(보안·비용)으로 분할. 평가 도구 5종 비교표는 부록 C로 추가 분리해 본문 밀도 추가 확보 |
| 5 | 9장(→10장) 의도적 페인포인트 | 10장 본문 초반에 "검색 결과 비면 재시도" 요구사항을 LCEL로 짜다 막히는 30~50줄 시퀀스 명시. 같은 동작을 StateGraph로 푼 코드와 짝지어 등장. Part 3 도입글의 약속을 10장 본문이 받아내는 구조 |
| 추가 | 11장 밀도 분배 | 4종 패턴 표·Supervisor 데모·핸드오프 함정·다른 프레임워크 한 단락·Grid Dynamics·권고의 분배를 9,000자 안에서 자수로 명시. AutoGen/CrewAI 비교표는 부록 B로 이동 |
| 추가 | 7장 "추상의 깊이" 측정 좌표 | (a) import 그래프 깊이, (b) 호출 트레이스, (c) 추상 단 수 3~4개 구체 예. 줄 수 수치는 저술 단계 실측 후 갱신 (예상치 박지 않음) |
| 추가 | 부록 B AutoGen/CrewAI 진입 가이드 | 부록 B를 2,000→3,500자로 확장, 각 프레임워크별 "여기를 읽으세요" 한 단락 명시 |
| 추가 | 표지 메모 | 부제 폰트를 본 제목 80% 비중으로 유지 — cover-designer 단계 전달 |

---

## 11. 라운드 2 잔여 검토 사항 (라운드 3 또는 저술 단계로 송부)

이 계획이 챕터 저술 단계로 넘어가기 전 마지막으로 확인하고 싶은 두 가지.

1. **4장 신규 위치 적정성** — Plan-and-Solve/Reflexion/ToT를 *5장 메모리 앞*에 두는 것이 자연스러운가, 아니면 *6장 안전장치 뒤*가 자연스러운가. 현재는 "ReAct → 변종 → 메모리 → 안전" 순서. ReAct 직후에 변종을 보는 게 호기심 흐름상 가장 자연스럽다고 판단했으나, 저술 단계에서 한 번 더 점검 권고
2. **mini_agent.py 누적 버전 관리** — 6장 끝의 v3, 7장 LangChain 버전(`mini_agent_lc.py`), 10장 LangGraph 버전(`mini_agent_lg.py`)에 4장 변종(Plan-and-Solve, Reflexion)이 끼면 v2.5 같은 중간 분기가 생긴다. 저술 단계에서 "어떤 버전이 정본이고 어떤 게 분기"인지 명확히 표기할 것
