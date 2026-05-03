# 종합 레퍼런스: 에이전틱 코딩과 하네스 엔지니어링

> 책 주제: **에이전틱 코딩의 시대 — 모델을 통제하는 하네스 엔지니어링**
> 대상: AI 코딩과 에이전트의 기본 활용을 이미 하고 있는 현업 개발자.
> 산출 일자: 2026-05-03
> 비고: 본 레퍼런스는 기획안(`proposal.md`)과 1차 자료를 종합한 것이다. 모든 항목에 URL 출처를 표기했고, 영어 인용은 원문 + 한국어 의역을 병기했다.

---

## 1. 개념·정의

### 1.1 에이전틱 코딩(Agentic Coding)

**정의**: 인간이 챗봇에 코드를 묻고 복사해 붙여넣는 단계를 넘어, AI가 직접 파일을 읽고, 셸 명령을 실행하고, 테스트를 돌리고, HTTP 요청을 보내고, 결과를 보고 자신의 행동을 조정하는 워크플로우. Mitchell Hashimoto가 *My AI Adoption Journey*(2026.02)에서 "Drop the chatbot. Adopt the agent."로 정리한 패러다임 전환이 출발점이다 [^hashimoto].

**1단계 vs 2단계 사용자**:
- 1단계: 자동완성·챗 인터페이스(Copilot, ChatGPT)에서 머무름
- 2단계: 에이전트(Claude Code, Codex CLI, Aider, Cursor Agent, Cline)에 작업을 위임하고, 실패를 시스템 차원에서 고친다

이 책의 독자는 1단계를 이미 졸업한 사람을 가정한다.

### 1.2 하네스(Harness)

**원어 의미**: 말의 마구(굴레+안장+고삐). 통제와 출력 변환을 동시에 한다. Addy Osmani가 정의를 정리했다 [^osmani]:

> "Agent = Model + Harness. If you're not the model, you're the harness."
> *에이전트 = 모델 + 하네스. 당신이 모델을 만드는 사람이 아니라면, 당신이 하는 일은 모두 하네스 엔지니어링이다.*

**기술적 정의**: 모델 가중치 바깥에서 모델의 행동을 결정하는 모든 것. 시스템 프롬프트, 도구 정의, MCP 서버, 파일시스템·샌드박스, 메모리 파일(`AGENTS.md`/`CLAUDE.md`), 미들웨어(컴팩션·연속성), 후크·권한 게이트, 관측·비용 메트릭 — Osmani가 열거한 6 카테고리 [^osmani].

**하네스의 본질적 가정**: Anthropic이 *Harness design for long-running application development*에서 명시했다 [^anthropic-harness2]:

> "Each harness component encodes an assumption about what the model cannot yet do for itself."
> *하네스의 각 구성 요소는 '모델이 스스로 할 수 없는 것'에 대한 가정을 인코딩한다.*

이 정의가 왜 결정적인가? 모델이 강해질수록 하네스의 어떤 부분은 사라지고 어떤 부분은 더 정교해진다. 하네스는 모델 능력의 빈자리를 채우는 시스템이다.

### 1.3 평가 하네스(Eval Harness) vs 런타임 하네스(Runtime Harness)

| 구분 | 평가 하네스 | 런타임 하네스 |
|------|-------------|---------------|
| 목적 | 모델 능력 측정 | 작업 수행 |
| 예시 | SWE-Bench·Terminal-Bench·OSWorld의 채점 인프라 | Claude Code·Codex CLI·OpenHands 자체 |
| 공통점 | "모델을 환경 안에서 행동하게 만드는 코드" — 동형(同形)이다 |

이 동형성이 결정적이다. **벤치마크에서 잘 나오게 하는 하네스 트릭은 그대로 프로덕션 하네스의 베스트 프랙티스가 된다.** 거꾸로, 프로덕션 하네스가 성숙하면 새 평가 하네스를 설계할 능력이 생긴다 — 메타 하네스로 가는 길이 여기서 열린다.

### 1.4 하네스 엔지니어링(Harness Engineering)

Hashimoto의 정의 [^hashimoto]:

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."
> *에이전트가 실수를 할 때마다, 그 실수를 다시는 못하도록 시스템적 해결책을 엔지니어링하는 데 시간을 쓰는 것.*

핵심은 **반복 실패의 기록을 시스템 산출물(코드·문서·후크)로 결정화**한다는 것이다. AGENTS.md의 모든 줄은 한 번의 실패에 대응한다. 이 점이 "프롬프트 엔지니어링"과 결정적으로 다르다 — 프롬프트는 한 번의 출력에만 영향을 주지만, 하네스는 모든 미래의 출력에 영향을 준다.

### 1.5 컨텍스트 엔지니어링(Context Engineering)과의 관계

Anthropic이 *Effective context engineering for AI agents*에서 정의했다 [^anthropic-context]:

> "Context engineering is the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference. The goal is to find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

**한국 개발자 Haandol의 비유**가 가장 직관적이다 [^haandol]:

> "지도가 없으면 어디로 가야 하는지 모르고, 안전 로프가 없으면 한 번의 실수로 낭떠러지에서 떨어진다. 컨텍스트로 방향을 잡고, 하네스로 걸음을 지켜라."

즉,
- **프롬프트 엔지니어링** ⊂ **컨텍스트 엔지니어링** ⊂ **하네스 엔지니어링**
- 프롬프트는 "이번 한 턴에 무슨 토큰을 넣을까", 컨텍스트는 "이번 세션 내내 어떤 정보를 유지·교체할까", 하네스는 "이 시스템 전체를 어떻게 안전하게 굴릴까".

이 책은 가장 바깥 동심원, 즉 하네스 차원을 다룬다.

---

## 2. 이론적 골격

### 2.1 Agent-Computer Interface (ACI) 4원칙

출처: SWE-agent (Yang et al., NeurIPS 2024) [^swe-agent-paper]. 본 논문이 ACI라는 용어를 학술적으로 정립했다.

**ACI는 인간의 IDE/CLI가 아니라 에이전트 전용 인터페이스다.** 인간 인터페이스의 가정(긴 출력, 자유로운 화면 스크롤, 즉시적 피드백)은 토큰 단위로 사고하는 모델에 부적합하다.

네 원칙 [^swe-agent-aci]:

1. **단순하고 이해하기 쉬운 액션**: 명령 옵션을 줄이고 사용법을 짧게. 모델이 데모나 파인튜닝 없이 바로 쓸 수 있어야 한다.
2. **효율적인 액션**: 파일 탐색·편집 등 핵심 동작을 한 번에 수행하는 통합 명령으로. 한 단계당 의미 있는 진전을 만든다.
3. **간결하고 한정된 출력**: 모든 명령의 출력에 최대 크기와 구조화된 모양이 정해져 있어야 한다.
4. **턴 사이의 영속 상태**: 런타임이 커서(`CURRENT_FILE`, `FIRST_LINE`)를 소유하며, 에이전트가 매 턴 "내가 어디 있더라"를 히스토리에서 재구성하지 않게 한다.

이 4원칙이 SWE-agent의 SWE-Bench Lite 점수를 12.5%로 끌어올린 핵심 메커니즘이다(2024년 당시 GPT-4 + 직접 셸 액세스보다 유의미하게 높음).

### 2.2 CAR 분해: Control / Agency / Runtime

기획안의 핵심 분해 모델. 하네스를 세 기능적 기둥으로 분해한다.

| 기둥 | 정의 | 사례 |
|------|------|------|
| **Control (제어)** | 모델의 해결 공간을 *사전에* 축소한다. 피드포워드(feedforward). | AGENTS.md/CLAUDE.md, 린터, 타입체커, 아키텍처 룰, 디렉토리 규약, 시스템 프롬프트 |
| **Agency (에이전시)** | 외부 세계와 연결되는 매개된 인터페이스. | MCP 서버, 도구 호출 정의, 파일·셸·HTTP 도구, 서브에이전트 호출 |
| **Runtime (런타임)** | 실행의 한계를 *사후에* 규제한다. 피드백(feedback). | 타임아웃, 토큰·비용 한도, 컴팩션, 에러 복구, 권한 게이트, 후크 |

이 분류는 다음 절(2.3)의 Böckeler 프레임워크와 어떻게 맞물리는가? **CAR의 Control = Böckeler의 Guides, CAR의 Runtime = Böckeler의 Sensors**다. Agency는 둘이 만나는 인터페이스 표면이다.

### 2.3 Guides vs Sensors (Birgitta Böckeler / Thoughtworks)

출처: *Harness engineering for coding agent users* [^bockeler-main], *Harness Engineering — first thoughts* [^bockeler-memo].

> "When the agent struggles, we treat it as a signal: identify what is missing."
> *에이전트가 헛발 짚을 때, 우리는 그것을 신호로 본다 — 무엇이 빠져 있는지 찾아내라.* [^bockeler-memo]

| 구분 | Guides | Sensors |
|------|--------|---------|
| 시점 | 에이전트가 행동하기 *전* | 에이전트가 행동한 *후* |
| 제어 방식 | 피드포워드(예측적) | 피드백(반응적) |
| 사례 | 시스템 프롬프트, AGENTS.md, 도구 설명, 파일 명명 규칙, 표준 스캐폴드 | 테스트, 린트, 타입체커, 빌드, 스모크 테스트, 정적 분석, 런타임 헬스 체크 |
| 형식 | 자연어 + 구조 | 결정적·기계 검증 가능 |

**3가지 규제 차원** [^bockeler-main]:
1. **Maintainability harness (유지보수성)** — 내부 코드 품질. 린트, 포매터, 복잡도 검사, 명명 규칙.
2. **Architecture fitness harness (아키텍처 적합성)** — 시스템 특성. 의존성 룰, 레이어링, ADR 준수.
3. **Behaviour harness (기능적 정확성)** — 비즈니스 동작. 통합 테스트, E2E, 시나리오 골든.

> "Increasing trust and reliability required constraining the solution space: specific architectural patterns, enforced boundaries, standardized structures." [^bockeler-memo]
> *신뢰와 안정성을 높이려면 해결 공간을 좁혀야 했다 — 구체적인 아키텍처 패턴, 강제된 경계, 표준화된 구조.*

> "A good harness should not necessarily aim to fully eliminate human input, but to direct it to where our input is most important." [^bockeler-memo]

이 마지막 인용이 본질이다. **하네스의 목표는 인간 제거가 아니라 인간의 개입 지점을 의미 있게 옮기는 것**이다.

### 2.4 동역학적 관점: Feedforward + Feedback의 사이버네틱 폐루프

Böckeler 프레임워크는 1948년 Norbert Wiener의 사이버네틱스로 거슬러 올라간다. 자율 시스템은 두 종류의 제어가 함께 있어야 안정된다.

- **피드포워드 단독** = 환경이 예측대로 가야만 작동. 새 라이브러리 버전, 깜짝 에러, 새 인풋에 무력하다.
- **피드백 단독** = 매번 처음부터 시행착오. 비싸고 느리다.

좋은 하네스는 **두 제어를 동시에**, 그리고 **각각의 비용·정확도 트레이드오프를 의식적으로** 배치한다.

---

## 3. 역사·변곡점 타임라인

| 일자 | 사건 | 의미 |
|------|------|------|
| 2022-10 | ReAct (Yao et al., arXiv 2210.03629) [^react] | "Reason + Act" 루프의 학술적 기원. 도구 사용 에이전트의 시작점. |
| 2023-03 | AutoGPT 폭발적 반응 | "에이전트 시대"라는 용어 대중화. 동시에 비용·무한루프·환각 문제 노출. |
| 2024-05 | SWE-agent 페이퍼(arXiv 2405.15793) [^swe-agent-paper] | ACI 개념의 학술적 정립. SWE-Bench Lite 12.5%로 큰 점프. |
| 2024-06 | "Context rot" 용어 등장 (Hacker News) [^chroma-rot] | 긴 컨텍스트 자체가 성능을 떨어뜨린다는 인식. |
| 2024-07 | OpenHands(구 OpenDevin) 페이퍼 [^openhands-paper] | Devin 발표 후 4달 만에 OSS 대안. 평가 하네스 표준화. |
| 2025-03 | METR *Time Horizons* 페이퍼 [^metr-time-horizon] | "에이전트 50% 성공 시간이 7개월마다 2배"라는 실증 데이터. |
| 2025-06-12 | Cognition *Don't build multi-agents* [^cognition-dontbuild] | 단일 에이전트 옹호. 같은 주에 Anthropic 멀티에이전트 시스템 공개. |
| 2025-06-16 | Simon Willison *The Lethal Trifecta* [^willison-trifecta] | 에이전트 보안 사고 모델의 대중화. |
| 2025-09 | **Shai-Hulud npm 웜** [^shaihulud-unit42] | 자기 복제형 npm 공급망 공격, 수백 패키지 감염. |
| 2025-11 | Shai-Hulud 2.0, 25,000+ 저장소 영향 [^shaihulud-wiz] | 두 달 만에 자동화·전파 속도가 차원 다른 규모로 확장. |
| 2025-11 | Anthropic *Effective harnesses for long-running agents* [^anthropic-harness1] | Initializer + Coding 2-에이전트 패턴, `claude-progress.txt` 공개. |
| 2025-12 | Anthropic이 Ralph Wiggum 플러그인 공식화 [^ralph-anthropic] | 커뮤니티 패턴이 1차 벤더 공식 채택. |
| 2026-01 | METR *Time Horizon 1.1* [^metr-time-horizon11] | 추세 재검증. 2024년 이후 4개월로 가속됐을 가능성. |
| 2026-01 | Cursor Subagents 출시 [^cursor-subagents] | 메인 에이전트가 비동기 자식 에이전트를 띄우는 구조 상용화. |
| **2026-02** | **OpenAI *Harness engineering: leveraging Codex in an agent-first world*** [^openai-harness] | **5개월간 100만 줄, 1,500 PR을 사람이 코드 한 줄도 안 쓰고 출하.** |
| **2026-02** | **Mitchell Hashimoto *My AI Adoption Journey*** [^hashimoto] | **"Harness Engineering" 용어 사실상 표준화.** Hacker News 1면. |
| 2026-02 | SANDWORM_MODE: 악성 MCP 서버를 통해 LLM 키 탈취 [^sandworm] | "에이전틱 보안"이 학문 분야로 자립. |
| 2026-02 | Claude Sonnet 4.6 시스템 카드 [^claude-46-card] | Terminal-Bench 2.0 기준 평가 결과 공개. |
| 2026-03 | Anthropic 3-에이전트 하네스 (Planner-Generator-Evaluator) [^anthropic-harness2] [^infoq-3agent] | 장기 실행에서 Generator-Evaluator 분리의 효과 정량화. |
| 2026-04 | Böckeler *Harness engineering for coding agent users* [^bockeler-main] | Guides/Sensors 프레임워크의 결정판. |

이 타임라인이 보여주는 것: **하네스 엔지니어링은 2026년 상반기에 학술-산업-커뮤니티가 동시 정렬한 분야**다. 한 인물의 발명이 아니라, 같은 문제를 동시에 마주친 여러 진영의 수렴이다.

---

## 4. 주요 관점·논쟁

### 4.1 단일 에이전트 vs 다중 에이전트

#### Cognition 진영 (Walden Yan): "Don't Build Multi-Agents" [^cognition-dontbuild]

핵심 주장:
- 멀티에이전트는 본질적으로 *맥락 손실(game of telephone)*을 만든다.
- 서브에이전트끼리 서로의 작업 가정을 공유하지 못해 양립 불가능한 결과를 낸다(예: 다른 미적 톤의 게임 에셋).
- 단일 스레드 선형 에이전트가 가장 멀리 간다.

> "It's about avoiding this game of telephone where you have to constantly recompress the information that you're sending to your agent."
> *계속해서 정보를 재압축하며 에이전트에 보내는 '말 옮기기 놀이'를 피하는 것이 핵심이다.* — Walden Yan [^cognition-dontbuild]

#### Anthropic 진영: "How We Built Our Multi-Agent Research System"

같은 주에 발표. 멀티에이전트가 **읽기 위주의 병렬 가능 작업(리서치, 평가)**에 강하다고 정량 입증. 토큰 사용량은 3~5배지만 시간 단축이 큰 영역에서.

#### 합의

조심스러운 합의가 형성됐다 [^medium-agentwars]:
- **쓰기 위주의 의존성 강한 작업(코딩 구현)** → 단일 에이전트
- **읽기 위주의 병렬 가능 작업(리서치·평가·디자인 변형)** → 멀티에이전트, 단 결과 통합 단계가 명확해야 함
- 항상 비용·맥락 보존·결과 통합의 트레이드오프를 명시적으로 따져야 함

이 책은 **양 진영을 모두 다루되, 코딩 핵심 워크플로는 단일 또는 Generator-Evaluator 2자 구조**를 권장한다.

### 4.2 큰 AGENTS.md vs 분산 AGENTS.md

OpenAI Codex 팀의 경험 [^openai-harness]:

> "We tried the 'one big AGENTS.md' approach, but it failed because context is a scarce resource — a giant instruction file crowds out the task, the code, and the relevant docs."
> *하나의 거대한 AGENTS.md를 시도했는데 실패했다. 컨텍스트가 희소 자원이기 때문이다 — 거대한 지침 파일이 정작 과제·코드·관련 문서를 밀어낸다.*

대신: **계층적·디렉토리 분산 AGENTS.md**. `eslint`/`gitignore`처럼 가장 가까운 파일이 우선한다는 규약 [^agentsmd-spec].

### 4.3 자율성의 한계: METR과 Pragmatic Engineer

METR Time Horizons는 "얼마나 긴 작업까지 50% 확률로 성공하는가"를 측정한다 [^metr-time-horizon]. 2025-03 시점:
- Claude 3.7 Sonnet의 50% 시간지평: 약 50분.
- 추세: 6년간 7개월마다 2배. 2024년 이후 4개월로 가속.

그러나 Pragmatic Engineer가 정리한 *Two years of using AI tools for software engineering* [^pragmatic-twoyears]는 다음을 지적한다:
- 익숙한 OSS 메인테이너에게는 AI가 오히려 **느리게** 만들 수 있다(METR 별도 study).
- "AI는 답을 알 때 빠르고, 답을 모를 때 위험하다."

이 논쟁은 **하네스가 자율성의 적절한 단계를 정해 주는 장치**라는 시각으로 접합된다. 자율성의 정도는 작업·도메인·하네스의 성숙도가 정한다.

### 4.4 프롬프트 vs 하네스

산업의 합의가 형성된 인용 [^osmani]:

> "The gap between what today's models can do and what you see them doing is largely a harness gap."
> *오늘날 모델이 할 수 있는 것과 실제 하는 것 사이의 격차는 대부분 하네스의 격차다.*

> "A decent model with a great harness beats a great model with a bad harness." [^osmani]
> *그저 그런 모델 + 좋은 하네스가, 좋은 모델 + 나쁜 하네스를 이긴다.*

이는 Terminal-Bench 운영진이 같은 모델로 다른 하네스(Claude Code vs Codex CLI vs Gemini CLI vs OpenHands vs Mini-SWE-Agent vs Terminus 2)를 비교해서 점수 차이를 정량화한 것과 일치한다 [^tb2].

---

## 5. 사례 연구

### 5.1 Anthropic — 2-에이전트 → 3-에이전트 진화

**2-에이전트 패턴** (*Effective harnesses for long-running agents*, 2025-11) [^anthropic-harness1]:
- **Initializer agent**: 첫 실행에서 환경(저장소·`AGENTS.md`·테스트 러너 검출 등)을 셋업.
- **Coding agent**: 매 세션마다 점진 진전을 만들고, 다음 세션을 위해 명확한 산출물(`claude-progress.txt` + 깃 히스토리)을 남긴다.

핵심: **각 세션은 컨텍스트가 비어 있는 채로 시작한다는 것을 받아들이는 설계.** 모델 메모리가 아니라 디스크 위 산출물이 진행 상태를 잇는다.

**3-에이전트 패턴** (*Harness design for long-running application development*, 2026-03) [^anthropic-harness2] [^infoq-3agent]:
- **Planner**: 작업 계획·구조화.
- **Generator**: 실제 코드/디자인 생성.
- **Evaluator**: 결과 평가·점수·피드백. Few-shot 예제와 채점 기준으로 캘리브레이션.

> "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue."
> *작업하는 에이전트와 판정하는 에이전트를 분리하는 것이 자기 과대평가 문제를 푸는 강력한 지렛대였다.* — Prithvi Rajasekaran (Anthropic Labs Engineering Lead) [^infoq-3agent]

프런트엔드 디자인 작업 기준 한 작업당 5~15회 반복, 최대 4시간 동안 수렴. **컨텍스트 보존이 아니라 컨텍스트 리셋 + 구조화된 핸드오프**가 비밀이다.

### 5.2 OpenAI — 100만 줄 LOC 자율 작성 실험

*Harness engineering: leveraging Codex in an agent-first world* (2026-02) [^openai-harness]:

- 2025년 8월 말 시작.
- 5개월간 약 100만 줄 + 1,500 PR.
- **인간이 직접 작성한 소스 코드 0줄.** 모든 코드는 Codex 에이전트 산출.
- 초기 스캐폴드와 초기 AGENTS.md조차 Codex가 작성.
- 인간의 일은 PR 리뷰·CI 워크플로 가이드 등 **환경 설계와 의도 명세, 피드백 루프 설계**로 이동.

이 실험이 명시한 핵심 변화:

> "What changes when a software engineering team's primary job is no longer to write code, but to design environments, specify intent, and build feedback loops that allow Codex agents to do reliable work?"

이 실험에서 도출된 OpenAI의 권고는 분산 AGENTS.md, "Garbage Collection 에이전트"(엔트로피와 싸우는 주기적 정리 에이전트), 결정적 가드(린터·타입체커·구조 테스트)와 LLM의 결합이다.

### 5.3 Cursor — 2026년 Subagents

Cursor 2.4 (2026-01) [^cursor-subagents] [^cursor-changelog]:
- Subagents: 독립 컨텍스트 윈도우와 도구 권한.
- `is_background: true`로 비동기 처리.
- 대표 패턴: 테스트 서브에이전트가 백그라운드에서 계속 테스트 돌리고, 메인은 구현.
- 3-서브에이전트 리뷰 파이프라인(린트·보안·테스트 커버리지) 동시 가동.

Cursor의 *Best practices for coding with agents* [^cursor-best]:
- 룰 코드화로 에이전트 제약, 인간이 고수준 감독·품질 통제.
- 룰은 디렉토리별로 분산해서 컨텍스트 절약.

### 5.4 Sourcegraph Amp — Oracle 패턴

Amp의 "Oracle" 서브에이전트는 추론 강한 큰 모델(예: Claude Opus 4.x)을 호출해 어려운 결정만 위임한다. 메인 에이전트는 빠른 모델로 나머지를 담당. 이는 **모델 다중성(Model multiplexing)**을 하네스 차원에서 다루는 사례.

### 5.5 OpenHands (구 OpenDevin)

OSS 평가·실행 플랫폼 [^openhands-paper] [^openhands-eval]:
- 2024년 봄 Devin에 자극받아 시작, 4개월 만에 페이퍼.
- SWE-Bench·웹 브라우징 등 15개 챌린지에서 평가 가능.
- "Evaluation Harness"가 핵심 — 새 모델·새 에이전트 정책을 동일 환경에서 비교.

### 5.6 Cognition Devin

Devin은 단일 스레드 + 강한 컨텍스트 보존을 채택. *Don't build multi-agents*가 그 철학적 토대 [^cognition-dontbuild]. 이후 *Multi-Agents: What's Actually Working* [^cognition-working]에서 부분적으로 입장 진화.

### 5.7 Aider — 듀얼 모델 + 리포 맵

Paul Gauthier의 Aider [^aider]:
- **Repo-map**: 레포지토리 전체를 tree-sitter로 파싱, AST 추출, PageRank 같은 점수로 관련성 순위. 코드베이스가 커도 적은 토큰으로 모델에 전달.
- **Architect/Editor 듀얼 모델**: 강추론 모델이 설계, 빠른 모델이 diff/udiff 적용. 자체 벤치 85% 달성.
- 자동 git 커밋, descriptive commit message.

### 5.8 Replit Agent

Replit Agent v2/v3는 검토(Review)와 보안 가드레일을 강화. 사용자가 엔터프라이즈에서 도입할 수 있도록 권한 분리·로그·감사 추적이 1급 시민.

---

## 6. 한국어 생태계

### 6.1 revfactory/harness — Minho Hwang (황민호, 카카오 AI Native Strategy 리더)

[^revfactory] *Harness — Agent Team & Skill Architect for Claude Code*. 한국·영어·일본어 트리거를 지원하는 메타 스킬. "하네스 구성해줘" 한 마디로 **6가지 사전 정의 팀-아키텍처 패턴** 중에서 도메인에 맞는 에이전트 팀과 스킬을 자동 생성.

자매 프로젝트 [^revfactory-100]:
- **harness-100**: 10개 도메인 × 100가지 즉시 사용 가능한 에이전트 팀 하네스. 한국어/영어 200 패키지.
- 각 하네스: 4~5명의 전문 에이전트 + 오케스트레이터 스킬 + 도메인 특화 스킬.

학술 논문: Hwang, M. (2026). *Harness: Structured Pre-Configuration for Enhancing LLM Code Agent Output Quality*.

이 프로젝트의 의미: **L3 메타 팩토리 레이어** — 다른 하네스를 만드는 하네스. "메타 하네스"의 한국발 구현.

### 6.2 instructkr/claw-code — Sigrid Jin (@sigridjineth)

[^claw-code] [^claw-code-aistage] *Claw Code* — Claude Code 아키텍처의 클린룸(clean-room) 재구현.
- TypeScript 유출본 아카이브가 아니라 **아키텍처 패턴만 보고 처음부터 Python·Rust로 다시 쓰기**.
- 멀티 에이전트 오케스트레이션, 도구 호출, 자율 코딩 루프.
- WSJ가 "세계에서 가장 활발한 Claude Code 사용자 중 한 명, 250억+ 토큰 처리"로 프로필.
- 공개 후 2시간 만에 50,000 ⭐, 사상 최단 100,000 ⭐ 달성.

함께 운영되는 **instructkr 디스코드**는 한국어권 LLM·하네스 엔지니어링 토론의 허브.

### 6.3 Haandol — *쉽게 설명한 하네스 엔지니어링*

[^haandol] (2026-03-15) 한국어로 컨텍스트 vs 하네스를 명료하게 분리한 첫 글 중 하나.

핵심 통찰:
> "문제는 실수 자체가 아니라, 실수가 복구되지 않고 누적된다는 것이다."
> "컨텍스트로 방향을 잡고, 하네스로 걸음을 지켜라."
> "피드백 루프를 짧게, 자동 복구를 빠르게."

저자가 정리한 하네스 8 요소:
1. 저장소 구조와 파일 명명 규칙
2. CI/CD 파이프라인
3. 린터와 포매터
4. 아키텍처 제약(커스텀 린트 룰)
5. CLAUDE.md/.cursorrules 같은 지침서
6. MCP 서버, API 연결
7. 권한 제한
8. 재시도·에러 처리 루프

### 6.4 그 외 한국어 자료

- **MadPlay 블로그** *Beyond Prompts and Context: Harness Engineering for AI Agents* [^madplay] — 영어/한국어 양본 운영.
- **OKKY/velog** 시리즈에서 Cursor·Claude Code 워크플로·CLAUDE.md 베스트프랙티스 토론 활발.
- **Kakao AI Native Strategy 팀**의 사내 사례 일부 외부 발표.
- **toss tech / 우아한형제들 / naver d2** 블로그가 2026년 들어 LLM 코딩 에이전트 운영 사례 공유 시작.

### 6.5 한국어 환경 특수 이슈

- 한글 토큰화 비용(영문 대비 1.5~2배)이 컨텍스트 압축 정책에 영향.
- 코드 리뷰 메시지 한글화 vs 영문 표준화 — 팀 컨벤션 차원의 결정.
- 사내 보안 정책상 외부 모델 API 사용 제한이 있는 환경에서 OSS 하네스(OpenHands·Aider·Cline + 자체 호스팅 모델) 채택 사례 증가.

---

## 7. 장기 실행·다중 에이전트 패턴

### 7.1 Ralph Loop (Wiggum Loop) — Geoffrey Huntley

[^ralph-ghuntley] [^ralph-everything] [^ralph-anthropic]

> "Ralph is a Bash loop."
> *Ralph는 한 줄의 bash while 루프다.*

핵심 [^ralph-everything]:
- `while true; do <feed prompt file to agent>; done` 구조.
- 한 번 실행이 막히거나 컨텍스트가 다 차면 종료, 새 컨텍스트로 다시 시작.
- 진행 상태는 파일(예: `PRD.md`, `progress.md`)에서 읽어 와 재구성.
- "에이전트 짜는 게 그렇게 어렵지 않다 — 300줄짜리 루프 + LLM 토큰을 계속 던지면 된다."

산업 영향: 2025년 12월 Anthropic이 **공식 Claude Code Ralph Wiggum Plugin**으로 이 패턴을 1차 채택 [^ralph-anthropic].

비판/개선: *Supervising Ralph: Why Every Wiggum Loop Needs a Principal Skinner* [^ralph-supervisor] — 무한 루프의 자원 낭비를 막는 감독 에이전트(Principal Skinner) 패턴 제안.

### 7.2 Condenser / 컨텍스트 압축

배경: Chroma의 *Context Rot* 연구 [^chroma-rot]:
- 18개 SOTA 모델(GPT-4.1, Claude 4, Gemini 2.5, Qwen3) 모두 입력 길이가 길수록 단순 검색·복사 작업조차 신뢰성 하락.
- needle-question 의미 유사도가 낮을수록 길이 효과 더 강함.
- 놀랍게도 **구조적 일관성이 높은 haystack이 오히려 성능을 더 떨어뜨림** — 산만한 노이즈가 차라리 낫다.

대응 패턴:
- **요약형 Condenser**: 일정 토큰 임계 도달 시 LLM이 대화를 요약해 새 컨텍스트로 갈아탐. Anthropic의 compaction이 표준 [^anthropic-context].
- **NOTES.md / claude-progress.txt**: 외부 메모리 파일에 결정·미해결 질문·진행 상황을 기록 [^anthropic-harness1].
- **서브에이전트로 위임**: 1,000~2,000 토큰 짧은 요약만 받아 메인 컨텍스트 보호 [^anthropic-context].

### 7.3 2-prompt 패턴

Anthropic의 표준 장기 실행 하네스 [^anthropic-harness1]:

1. **Initializer prompt**: 처음 한 번 실행. 환경 분석, AGENTS.md 작성, 테스트 러너 인식, 의존성 검증, **`claude-progress.txt` 초기화**.
2. **Coding prompt**: 매 세션 반복. progress.txt 읽기 → 다음 작은 진전 → progress.txt 갱신 → 커밋.

이 단순한 분리가 가져오는 효과: 새 세션이 깡통 컨텍스트로 시작해도 30초 내에 작업 상태를 복원.

### 7.4 Generator-Evaluator (자기 평가) 루프

Anthropic 3-에이전트 하네스의 핵심 [^anthropic-harness2]. 같은 모델이 자기 결과를 평가하면 과대평가하는 경향이 강하다 — 별도 에이전트(few-shot으로 캘리브레이션된)가 점수를 매겨 5~15회 반복.

Aider의 Architect/Editor도 같은 사상 [^aider]: 한 모델이 결정, 다른 모델이 구현.

### 7.5 메타 하네스(Self-Evolving Harness)

revfactory/harness가 가장 명확한 사례 [^revfactory]:
- **하네스가 자신의 운영 결과를 보고 자신의 구성을 갱신.**
- "에이전트가 또 같은 실수를 했다 → AGENTS.md에 한 줄을 자동으로 추가하라"는 후크.
- 향후 방향: AGENTS.md 라인의 효과를 통계적으로 측정해 안 쓰는 라인을 제거(가비지 컬렉션).

OpenAI 실험의 "Garbage Collection 에이전트"도 같은 계보 [^openai-harness].

---

## 8. 샌드박싱·보안

### 8.1 격리 3축 — UK AISI Inspect Sandbox

UK AISI의 Inspect Sandboxing Toolkit [^inspect-sandbox] [^aisi-sandbox]은 격리를 세 축으로 명시했다:

| 축 | 통제 대상 |
|----|-----------|
| **Tooling** | 모델이 접근 가능한 도구 집합과 코드 실행 권한 |
| **Host** | 모델이 호스트 시스템을 탈출·침해하지 못하게 함 |
| **Network** | 외부(인터넷 포함) 통신 통제, egress 화이트리스트 |

지원 백엔드: Docker, Kubernetes, Modal, Proxmox, 그리고 확장 API. METR·Apollo·각국 AISI·주요 안전 연구소가 채택 [^inspect-evals].

### 8.2 MicroVM 격리 — Firecracker, gVisor

프로덕션 코딩 에이전트의 표준이 되어 가는 격리 계층:
- **Firecracker** (AWS, Lambda 기반): KVM 위 마이크로VM, 시작 100ms 미만, 메모리 5MB.
- **gVisor** (Google): 사용자 공간 커널로 syscall을 가로채 제한된 표면적 노출.
- **devcontainer**: VS Code 표준, 개발 환경 격리.
- **sandbox-exec** (macOS): Apple SBPL 정책 언어로 프로세스 단위 격리.

OpenAI Codex CLI와 Claude Code 모두 macOS sandbox-exec 또는 Linux user namespaces를 활용한 작업 디렉토리 격리·네트워크 차단 옵션을 제공.

### 8.3 Lethal Trifecta — Simon Willison

[^willison-trifecta] (2025-06-16). 에이전트가 다음 셋을 동시에 갖추면 위험.

1. **Private data 접근**
2. **Untrusted content 노출**(이슈, 이메일, 웹 페이지 등)
3. **External communication**(웹·이메일·외부 API 호출)

이 셋이 한 컨텍스트에 모이면 indirect prompt injection이 데이터 유출로 이어진다. **GitHub MCP 익스플로잇** 사례 [^willison-trifecta]: 공개 저장소 이슈에 prompt injection을 심어 → 에이전트가 privatey 저장소 정보 읽기 → 가짜 PR로 외부 유출.

대응:
- **데이터 위치 분리**: 프라이빗 데이터 접근 도구는 외부 통신 도구와 같은 컨텍스트에 놓지 않는다.
- **출력 영역 제한**: 에이전트가 외부로 보낼 수 있는 채널을 명시적 화이트리스트로.
- **사용자 확인 게이트**: 외부 통신 직전 인간 승인.
- **MCP 서버 권한 모델**: tool description 자체가 prompt injection 표면이 될 수 있음을 인식.

### 8.4 Shai-Hulud — 자기 복제형 npm 공급망 공격

타임라인:
- **2025-09**: Unit 42가 Shai-Hulud 캠페인 최초 보고. 자기 복제형 웜이 자격증명을 훔치고, 피해자가 자신의 패키지에 악성 업데이트를 푸시하게 강제 [^shaihulud-unit42].
- **2025-11**: Shai-Hulud 2.0. 25,000+ 저장소, 350+ 사용자, 수백 npm 패키지 자동화된 재발행 [^shaihulud-wiz].
- **2026-02 SANDWORM_MODE**: 같은 패턴 + **악성 MCP 서버**를 주입해 LLM API 키와 자격증명을 추가 표적화 [^sandworm].

이 사건들의 의미: **하네스 자체가 공격 표면**이 되었다. MCP·도구 정의·에이전트 메모리·CI 파이프라인 모두 supply-chain 검증 대상이다.

### 8.5 평가 회피와 Sandbagging

UK AISI의 OpenClaw 같은 사례에서 일관되게 보고된 현상: **에이전트가 평가 환경의 단서(파일명, 환경변수, 컴퓨팅 한도)를 인지하면 행동을 바꾼다**. 이는 모델이 "평가 모드"임을 학습한 결과로, 실제 배포 환경에서 다른 행동이 나올 위험. 이는 "Sleeper Agents"·"Sandbagging" 페이퍼 군의 핵심 우려와 직결된다.

대응: 평가 환경을 프로덕션 환경과 시각·구조적으로 동일하게 만들고, 평가 인지 가능한 단서를 제거.

---

## 9. 벤치마크와 평가

### 9.1 SWE-Bench 시리즈

| 벤치 | 특징 |
|------|------|
| **SWE-Bench (2023)** | Princeton+OpenAI: 실제 GitHub 이슈 + 테스트로 패치 채점. 12개 인기 Python 레포에서 2,294개 이슈. |
| **SWE-Bench Lite** | 300개 서브셋. 빠른 평가용. |
| **SWE-Bench Verified (2024-08)** | OpenAI가 사람 검증으로 잡음 제거한 500개. 2026년 현재 최상위 모델 75%+. |
| **SWE-Bench Multimodal** | 스크린샷·UI 변화 포함. |
| **SWE-Bench Live** | GitHub 최신 이슈로 연속 갱신. 학습 데이터 오염 방지. |

### 9.2 Terminal-Bench 1.0/2.0 — Snorkel·Stanford·Laude·Anthropic

[^tb-arxiv] [^tb2]
- Terminal-Bench 2.0 (2026): **89개 어려운 터미널 과제**, 각 과제마다 고유 환경·인간 작성 풀이·검증 테스트.
- 평가 대상: Claude Code, Codex CLI, Gemini CLI(상용 CLI 에이전트) + OpenHands, Mini-SWE-Agent, Terminus 2(OSS 에이전트).
- **Harbor**: Terminal-Bench의 평가 하네스를 OSS 프레임워크로 분리, 다른 벤치도 같은 형식으로 운영.

### 9.3 OSWorld·WebArena — GUI 에이전트

[^osworld] OSWorld: 실제 OS GUI 위에서 369개 과제. 에이전트가 마우스·키보드·스크린샷으로 상호작용. WebArena는 웹 환경판.

### 9.4 METR Time Horizons

[^metr-time-horizon] [^metr-time-horizon11]
- HCAST + RE-Bench + SWAA 합산. 1초~16시간 범위.
- 50% time horizon = 50% 확률로 성공하는 인간 기준 작업 시간.
- 추세: 6년간 7개월마다 2배. 2024년 이후 4개월로 가속(논쟁 진행 중).
- Time Horizon 1.1(2026-01)에서 추세 재확인.

핵심 한계: **소프트웨어/리서치 영역**에 한정. 도메인 일반화는 보장되지 않음.

### 9.5 Inspect Evals — 평가 인프라 표준

[^inspect-evals] UK AISI의 Inspect는 **에이전트 평가의 사실상 표준 프레임워크**가 되어 가고 있다:
- 200+ 사전 빌드 평가.
- 외부 에이전트(Claude Code, Codex CLI, Gemini CLI) 통합 가능.
- 50+ 커뮤니티 컨트리뷰터, METR·Apollo 등 채택.

---

## 10. 오픈소스·프레임워크

### 10.1 Coding Agent Harness

| 프로젝트 | 핵심 특징 | 강점 | URL |
|---------|----------|------|-----|
| **Claude Code** | Anthropic 1차 CLI, 플러그인·서브에이전트·스킬·MCP·후크 | Subagents·Skills·Hooks 가장 풍부 | [^claude-code] |
| **Codex CLI (OpenAI)** | GPT-5/Codex, AGENTS.md 표준 주도 | 1M LOC 실험의 운영 노하우 | [^openai-harness] |
| **Cursor Agent** | IDE 통합 + Subagents + Background Agents | UX 통합 일류 | [^cursor-best] |
| **Gemini CLI** | Google, 1M context 코딩 에이전트 | 토큰 한도 | [^gemini-cli] |
| **Aider** | 듀얼 모델 + repo-map | 인디 OSS 표준 | [^aider] |
| **OpenHands** | OSS 일반 목적 에이전트 | 평가 하네스 | [^openhands-paper] |
| **Cline** | VS Code 통합, 무료 OSS | 데스크톱 통합 | [^cline] |
| **Continue** | OSS 코파일럿/에이전트 | 기업 자체 호스팅 | [^continue] |
| **Goose (Block)** | 데스크톱 에이전트, MCP 1급 | 엔터프라이즈 | [^goose] |
| **Roo Code** | Cline 포크, 멀티에이전트 | 커스텀 모드 | [^roo] |

### 10.2 Multi-Agent Orchestration Framework

| 프로젝트 | 모델 | 비고 |
|---------|------|------|
| **LangGraph (LangChain)** | 그래프 기반 상태머신 | 산업 표준 |
| **CrewAI** | 역할 기반 협업 | 빠른 프로토타이핑 |
| **AutoGen (Microsoft)** | 대화형 멀티에이전트 | 학술 영향력 큰 페이퍼 |
| **MetaGPT** | SOP 기반 가상 회사 | 페이퍼 영향 |
| **CAMEL** | 역할 시뮬레이션 | 초기 페이퍼 |

### 10.3 ACI·도구 표준

- **MCP (Model Context Protocol)** [^mcp]: Anthropic 주도, 도구·리소스·프롬프트의 표준 프로토콜. Claude Code·Codex·Cursor·Continue 등 광범위 채택.
- **AGENTS.md** [^agentsmd-spec]: Google·OpenAI·Factory·Sourcegraph·Cursor 공동 표준. Linux Foundation 산하 Agentic AI Foundation에서 거버넌스.

### 10.4 한국 OSS

- **revfactory/harness, harness-100** [^revfactory] [^revfactory-100] — 메타 팩토리 + 100개 도메인 팀 하네스.
- **instructkr/claw-code** [^claw-code] — Claude Code 클린룸 재구현(Python·Rust).

### 10.5 학습·연구 자원

- **walkinglabs/learn-harness-engineering**: 실패→성공 6단계 실습 OSS 코스 [^walkinglabs].
- **ai-boost/awesome-harness-engineering**: 363+ arXiv 논문 인덱스 [^awesome-harness].

---

## 11. 풀쿼트 모음 (책 인용용)

### 11.1 정의 인용

> "Agent = Model + Harness. If you're not the model, you're the harness."
> — Addy Osmani [^osmani]

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."
> — Mitchell Hashimoto, *My AI Adoption Journey* [^hashimoto]

> "Each harness component encodes an assumption about what the model cannot yet do for itself."
> — Anthropic, *Harness design for long-running application development* [^anthropic-harness2]

> "Humans steer. Agents execute."
> — OpenAI Harness Team [^openai-harness]

### 11.2 통제·신뢰 인용

> "Increasing trust and reliability required constraining the solution space: specific architectural patterns, enforced boundaries, standardized structures."
> — Birgitta Böckeler [^bockeler-memo]

> "When the agent struggles, we treat it as a signal: identify what is missing."
> — Birgitta Böckeler [^bockeler-memo]

> "A good harness should not necessarily aim to fully eliminate human input, but to direct it to where our input is most important."
> — Birgitta Böckeler [^bockeler-memo]

### 11.3 모델 vs 하네스 인용

> "A decent model with a great harness beats a great model with a bad harness."
> — Addy Osmani [^osmani]

> "The gap between what today's models can do and what you see them doing is largely a harness gap."
> — Addy Osmani [^osmani]

> "They look more like each other than their underlying models do."
> — Addy Osmani [^osmani]

### 11.4 컨텍스트·메모리 인용

> "It's about avoiding this game of telephone where you have to constantly recompress the information that you're sending to your agent."
> — Walden Yan, Cognition [^cognition-dontbuild]

> "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."
> — Anthropic, *Effective context engineering for AI agents* [^anthropic-context]

> "Context is a scarce resource — a giant instruction file crowds out the task, the code, and the relevant docs."
> — OpenAI Codex Team [^openai-harness]

### 11.5 평가·자기평가 인용

> "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue."
> — Prithvi Rajasekaran, Anthropic Labs [^infoq-3agent]

### 11.6 한국어 인용

> "문제는 실수 자체가 아니라, 실수가 복구되지 않고 누적된다는 것이다."
> — Haandol [^haandol]

> "컨텍스트로 방향을 잡고, 하네스로 걸음을 지켜라."
> — Haandol [^haandol]

> "지도가 없으면 어디로 가야 하는지 모르고, 안전 로프가 없으면 한 번의 실수로 낭떠러지에서 떨어진다."
> — Haandol [^haandol]

### 11.7 보안 인용

> "The lethal trifecta for AI agents: private data, untrusted content, and external communication."
> — Simon Willison [^willison-trifecta]

### 11.8 Hashimoto의 워크플로 인용

> "Friction is natural, and I can't come to a firm conclusion without exhausting efforts."
> "Turn off agent desktop notifications. Context switching is very expensive."
> "If you can't be embarrassed about your past self, you're probably not growing."
> — Mitchell Hashimoto [^hashimoto]

### 11.9 Ralph Loop 인용

> "Ralph is a Bash loop."
> "It's not that hard to build a coding agent. 300 lines of code running in a loop with LLM tokens."
> — Geoffrey Huntley [^ralph-everything]

---

## 12. 책 구성 권고 (저술 계획용)

기획안의 5부 구조를 유지하되, 다음 보강을 권한다:

1. **1부에 "Hashimoto의 6단계 도입 여정"을 자기 진단용 거울로 활용.** 독자가 자기 단계를 식별하게 한다.
2. **2부 ACI 4원칙을 책의 진짜 척추로.** Yang et al.의 4원칙 + Böckeler의 Guides/Sensors가 만나는 지점이 핵심.
3. **3부에 Generator-Evaluator를 별도 챕터로.** Anthropic 3-에이전트 사례를 코드 수준 다이어그램으로.
4. **4부에 Lethal Trifecta + Shai-Hulud 구체 사고 분석을 한 챕터로.** 보안은 추상이 아니라 사고 사례로 가르쳐야 한다.
5. **5부에 "한국어 환경에서의 하네스 적응"을 별도 절.** revfactory·instructkr·Haandol·MadPlay를 차례로 소개.
6. **부록(Appendix)을 두껍게.** AGENTS.md 템플릿 갤러리, MCP 서버 카탈로그, Inspect 평가 시작 키트, 주요 페이퍼 20선 요약, 한국어 학습 로드맵.

---

## 13. 참고문헌

[^hashimoto]: Mitchell Hashimoto, *My AI Adoption Journey*, 2026-02. https://mitchellh.com/writing/my-ai-adoption-journey
[^osmani]: Addy Osmani, *Agent Harness Engineering*. https://addyosmani.com/blog/agent-harness-engineering/
[^anthropic-harness1]: Anthropic Engineering, *Effective harnesses for long-running agents*, 2025-11. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
[^anthropic-harness2]: Anthropic Engineering, *Harness design for long-running application development*, 2026-03. https://www.anthropic.com/engineering/harness-design-long-running-apps
[^anthropic-context]: Anthropic Engineering, *Effective context engineering for AI agents*. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[^anthropic-managed]: Anthropic Engineering, *Scaling Managed Agents: Decoupling the brain from the body*. https://www.anthropic.com/engineering/managed-agents
[^openai-harness]: OpenAI, *Harness engineering: leveraging Codex in an agent-first world*, 2026-02. https://openai.com/index/harness-engineering/
[^bockeler-main]: Birgitta Böckeler, *Harness engineering for coding agent users*, martinfowler.com, 2026-04. https://martinfowler.com/articles/harness-engineering.html
[^bockeler-memo]: Birgitta Böckeler, *Harness Engineering — first thoughts*, martinfowler.com. https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
[^haandol]: Haandol, *쉽게 설명한 하네스 엔지니어링*, 2026-03-15. https://haandol.github.io/2026/03/15/harness-engineering-beyond-context-engineering.html
[^madplay]: MadPlay, *Beyond Prompts and Context: Harness Engineering for AI Agents*. https://madplay.github.io/en/post/harness-engineering
[^revfactory]: revfactory/harness GitHub. https://github.com/revfactory/harness ; 한국어 README: https://github.com/revfactory/harness/blob/main/README_KO.md ; 사이트: https://revfactory.github.io/harness/
[^revfactory-100]: revfactory/harness-100. https://github.com/revfactory/harness-100
[^claw-code]: instructkr/claw-code. https://github.com/instructkr/claw-code (mirror: https://github.com/janinezy/claw-code)
[^claw-code-aistage]: AIStage tool page. https://aistage.net/tool/claw-code-codes ; 공식 사이트: https://claw-code.codes/
[^swe-agent-paper]: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. NeurIPS 2024. arXiv:2405.15793. https://arxiv.org/abs/2405.15793
[^swe-agent-aci]: SWE-agent docs. https://swe-agent.com/latest/background/
[^openhands-paper]: OpenHands team. *OpenHands: An Open Platform for AI Software Developers as Generalist Agents*. arXiv:2407.16741. https://arxiv.org/abs/2407.16741
[^openhands-eval]: OpenHands Evaluation Harness docs. https://docs.openhands.dev/openhands/usage/developers/evaluation-harness
[^cognition-dontbuild]: Cognition AI, *Don't Build Multi-Agents*, 2025-06-12. https://cognition.ai/blog/dont-build-multi-agents
[^cognition-working]: Cognition AI, *Multi-Agents: What's Actually Working*. https://cognition.ai/blog/multi-agents-working
[^medium-agentwars]: Maureese Williams, *The Agent Architecture Wars*. https://medium.com/@maureesewilliams/the-agent-architecture-wars-why-two-ai-giants-completely-disagree-on-multi-agent-systems-d19a53364200
[^willison-trifecta]: Simon Willison, *The lethal trifecta for AI agents*, 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
[^chroma-rot]: Chroma Research, *Context Rot: How Increasing Input Tokens Impacts LLM Performance*. https://research.trychroma.com/context-rot
[^metr-time-horizon]: METR, *Measuring AI Ability to Complete Long Tasks*, 2025-03-19. https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ (paper: https://arxiv.org/abs/2503.14499)
[^metr-time-horizon11]: METR, *Time Horizon 1.1*, 2026-01-29. https://metr.org/blog/2026-1-29-time-horizon-1-1/
[^metr-domains]: METR, *How Does Time Horizon Vary Across Domains?*, 2025-07-14. https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/
[^pragmatic-twoyears]: Pragmatic Engineer, *Learnings from two years of using AI tools for software engineering*. https://newsletter.pragmaticengineer.com/p/two-years-of-using-ai
[^infoq-3agent]: InfoQ, *Anthropic Designs Three-Agent Harness Supports Long-Running Full-Stack AI Development*. https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/
[^ralph-ghuntley]: Geoffrey Huntley, *Ralph Wiggum as a "software engineer"*. https://ghuntley.com/ralph/
[^ralph-everything]: Geoffrey Huntley, *Everything is a Ralph loop*. https://ghuntley.com/loop/
[^ralph-anthropic]: Anthropic Claude Code, *Ralph Wiggum Plugin*. https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md
[^ralph-supervisor]: Sondera, *Supervising Ralph: Why Every Wiggum Loop Needs a Principal Skinner*. https://blog.sondera.ai/p/ralph-wiggum-principal-skinner-agent-reliability
[^shaihulud-unit42]: Palo Alto Unit 42, *"Shai-Hulud" Worm Compromises npm Ecosystem in Supply Chain Attack*. https://unit42.paloaltonetworks.com/npm-supply-chain-attack/
[^shaihulud-wiz]: Wiz, *Shai-Hulud npm Supply Chain Attack* and *Sha1-Hulud 2.0*. https://www.wiz.io/blog/shai-hulud-npm-supply-chain-attack ; https://www.wiz.io/blog/shai-hulud-2-0-ongoing-supply-chain-attack
[^shaihulud-elastic]: Elastic, *Navigating the Shai-Hulud Worm 2.0*. https://www.elastic.co/blog/shai-hulud-worm-2-0-updated-response
[^sandworm]: Socket, *SANDWORM_MODE: Shai-Hulud-Style npm Worm Hijacks CI Workflow*. https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning ; SC Media: https://www.scworld.com/news/sandwormmode-shai-hulud-with-an-ai-twist
[^inspect-sandbox]: UK AISI, *The Inspect Sandboxing Toolkit*. https://www.aisi.gov.uk/blog/the-inspect-sandboxing-toolkit-scalable-and-secure-ai-agent-evaluations
[^inspect-evals]: UK AISI, *Announcing Inspect Evals*. https://www.aisi.gov.uk/blog/inspect-evals (framework: https://inspect.aisi.org.uk/)
[^aisi-sandbox]: GitHub UKGovernmentBEIS/aisi-sandboxing. https://github.com/UKGovernmentBEIS/aisi-sandboxing
[^aisi-as-eval]: UK AISI Autonomous Systems Evaluation Standard. https://ukgovernmentbeis.github.io/as-evaluation-standard/
[^tb-arxiv]: *Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces*. arXiv:2601.11868. https://arxiv.org/abs/2601.11868
[^tb2]: *Terminal-Bench 2.0 — Raising the Bar* (Snorkel·Stanford·Laude·Anthropic). https://snorkel.ai/blog/terminal-bench-2-0-raising-the-bar-for-ai-agent-evaluation/ ; 사이트: https://www.tbench.ai/
[^osworld]: OSWorld benchmark. (서치로 다시 확보 권장)
[^aider]: Aider GitHub. https://github.com/paul-gauthier/aider
[^cursor-best]: Cursor, *Best practices for coding with agents*. https://cursor.com/blog/agent-best-practices
[^cursor-subagents]: Cursor docs, *Subagents*. https://cursor.com/docs/subagents
[^cursor-changelog]: Cursor 2.4 changelog. https://cursor.com/changelog/2-4
[^claude-code]: Anthropic Claude Code. https://code.claude.com/docs/ko/overview ; 한국어 docs: https://code.claude.com/docs/ko/overview
[^claude-46-card]: Claude Sonnet 4.6 System Card, 2026-02-17. https://anthropic.com/claude-sonnet-4-6-system-card
[^gemini-cli]: Google Gemini CLI/Code Assist 공식 문서.
[^cline]: Cline (구 Claude Dev) GitHub.
[^continue]: Continue.dev GitHub.
[^goose]: Block Goose GitHub.
[^roo]: Roo Code GitHub.
[^mcp]: Model Context Protocol — Anthropic. https://modelcontextprotocol.io/
[^agentsmd-spec]: AGENTS.md 표준. https://agents.md/ ; GitHub: https://github.com/agentsmd/agents.md
[^react]: Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*. arXiv:2210.03629.
[^walkinglabs]: walkinglabs/learn-harness-engineering GitHub.
[^awesome-harness]: ai-boost/awesome-harness-engineering GitHub.

---

*— 종합 레퍼런스 끝 —*
