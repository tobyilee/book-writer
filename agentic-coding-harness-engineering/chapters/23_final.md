# 23장. 오픈소스 풍경 — Claude Code·Codex CLI·Cursor·OpenHands·Aider

도구 후보가 너무 많다. Claude Code, Codex CLI, Cursor Agent, Gemini CLI, Aider, OpenHands, Cline, Continue, Goose, Roo Code. 멀티에이전트 프레임워크까지 보면 LangGraph, CrewAI, AutoGen, MetaGPT, CAMEL이 또 있다. 새 회사에 들어가거나 새 프로젝트를 시작할 때, *어느 자리에 어느 도구를 놓을지* 결정해야 한다. 솔직히 좀 난감하다.

블로그를 보면 다 좋다고 한다. "Cursor가 진짜다" "아니다, Claude Code다" "Codex CLI가 OpenAI의 진심이다" "OSS만 쓰자, 그게 진짜 자유다." 어느 글이 맞는가? 다 맞다, 다 틀리다. 정답은 없고, 다만 좌표가 있다. 23장은 그 좌표를 그리는 자리다.

## 도구를 *비교*하기 전에 — 비교의 축을 합의하자

흔한 실수가 있다. "Cursor가 좋아? Claude Code가 좋아?"라는 질문에 누군가는 UX로, 누군가는 가격으로, 누군가는 OSS냐 아니냐로 답한다. 같은 질문에 서로 다른 축으로 답하니 대화가 *겉돈다*.

도구를 비교하기 전에 *어느 축으로 볼지*부터 합의하자. 23장에서는 8개 축을 쓴다.

| 축 | 보는 것 |
|----|---------|
| **격리(Isolation)** | sandbox-exec / Docker / devcontainer 지원, Lethal Trifecta 대응 |
| **MCP** | Model Context Protocol 1급 지원 여부, 권한 모델 |
| **서브에이전트(Subagents)** | 본 에이전트가 다른 에이전트를 호출하는 패턴 1급 지원 |
| **메모리** | AGENTS.md / CLAUDE.md / .cursorrules / 디렉토리 cascade |
| **오픈성** | OSS / 부분 OSS / 클로즈드 |
| **운영 성숙도** | 후크·플러그인·프로덕션 운영 사례의 두께 |
| **관측(Observability)** | 트레이스·토큰 카운팅 1급 통합 (15장 5축 메트릭과 연결) |
| **비용 통제** | 일일 한도·throttling·팀별 분배 1급 지원 |

마지막 두 축 — *관측·비용 통제* — 이 v1에는 없었다. 15장에서 우리가 6번째 카테고리(관측·비용)를 본격적으로 다뤘으니 도구 비교에도 그 자리가 있어야 한다. 사실 이 두 축이 운영 단계의 성패를 가른다 — 도구가 멋져 보여도 트레이스가 안 잡히면 회귀를 못 본다.

## 1차 CLI 셋 — Claude Code · Codex CLI · Gemini CLI

가장 많이 비교되는 셋이다.

**Claude Code (Anthropic).** 1차 CLI. Subagents·Skills·Hooks·Plugins·MCP의 다섯 축 모두에서 가장 풍부한 1급 지원을 갖췄다.[^claude-code] 한국어 docs도 운영된다. 후크 시스템이 특히 강하다 — PreToolUse·PostToolUse·UserPromptSubmit 같은 단계마다 파이썬/셸 스크립트를 끼워 넣을 수 있다. 내가 이 책을 쓰는 이 자리도 Claude Code 위에서 굴러간다. 운영 성숙도는 — 솔직히 — 셋 중 가장 두껍다.

**Codex CLI (OpenAI).** GPT-5/Codex 모델 기반. AGENTS.md 표준을 사실상 주도한 자리다.[^openai-harness] 1M 줄 LOC 자율 작성 실험의 운영 노하우가 그대로 녹아 있다. 격리는 sandbox-exec(macOS)/Linux user namespaces 1급 지원. 서브에이전트와 후크는 — Claude Code 대비 — *덜 발달한* 자리다. 다만 GPT-5의 성능을 그대로 쓰고 싶다면 1차 선택지다.

**Gemini CLI (Google).** 1M 컨텍스트가 가장 큰 매력이다.[^gemini-cli] 큰 코드베이스를 한 번에 인지시키는 자리에서 강하다. 다만 후크·서브에이전트·관측 통합은 셋 중 가장 *얇다*. 2026년 들어 빠르게 따라잡고 있지만, 아직 1차 후보로 들기엔 운영 사례 두께가 모자라다.

세 1차 CLI를 한 줄로 정리하면 — *Claude Code = 가장 두꺼운 운영 성숙도*, *Codex CLI = AGENTS.md 표준의 본가*, *Gemini CLI = 1M 컨텍스트의 무기*. 자기 팀의 *주요 병목*이 어디인지에 따라 선택이 달라진다.

## IDE 통합 — Cursor의 자리

**Cursor Agent.** IDE 통합 일류다.[^cursor-best] 2026년 Subagents·Background Agents·Plan mode가 합류하면서 *IDE 안에서* 본격적인 멀티에이전트 워크플로를 만들 수 있게 됐다.[^cursor-subagents] [^cursor-changelog] UX 통합은 — 솔직히 — 다른 어떤 도구보다 매끄럽다. 코드 위 인라인 편집, 프로젝트 전체 검색, 멀티파일 변경의 미리보기가 한 화면에서 이어진다.

다만 격리는 Cursor 본체가 자체적으로 다루기보다 *호스트 OS에 의존*하는 자리다. 후크는 1급 지원이 약하다. MCP는 1급 지원이 됐지만 권한 모델은 — 16장에서 본 Lethal Trifecta 관점에서 — 다른 1차 CLI 대비 표면이 *더 넓다*. IDE 안에서 모든 게 한 컨텍스트에 모이기 때문이다.

요약 — Cursor는 *개발자 1인의 생산성*에서는 1등급이다. 다만 팀 전체의 격리·관측·비용 통제 거버넌스를 짜야 한다면 1차 CLI(Claude Code, Codex CLI)와 *함께* 쓰는 자리가 자연스럽다.

## 인디 OSS — Aider의 자리

**Aider.** 인디 OSS 표준이다.[^aider] 듀얼 모델과 repo-map이 핵심이다. Architect 모델이 결정하고 Editor 모델이 구현하는 분리 — 13장 Generator-Evaluator 사상의 가벼운 변종이다. repo-map은 큰 코드베이스를 정적 분석으로 그래프화해 *관련 파일만* 컨텍스트에 들이는 우아한 해법이다.

Aider의 매력은 *철학*에 있다. 한 사람이 git 위에서 깔끔하게 일하는 자리에 최적화돼 있다. 자동 커밋, diff 기반 변경, 모델 비용 트래킹이 1급 지원된다. 다만 후크·서브에이전트·MCP는 1차 CLI 대비 얇다. 사내 프로덕션 통합용보다는 *개인 개발자의 일급 도구*로 자리잡았다.

## 일반 목적 OSS — OpenHands의 자리

**OpenHands (구 OpenDevin).** OSS 일반 목적 에이전트다.[^openhands-paper] 가장 큰 차별점은 — *평가 하네스가 1급 시민*이라는 점이다.[^openhands-eval] 사내에서 평가 인프라부터 짜고 싶다면 OpenHands가 자연스러운 출발점이다. Docker 기반 격리, 다양한 LLM 백엔드, 평가 회귀 자동화가 *기본*으로 들어 있다.

운영 성숙도는 1차 CLI 대비 얇다. UX도 거칠다. 다만 *연구·평가 워크플로*에서는 OpenHands의 자리가 1차 CLI보다 자연스럽다. 22장에서 본 Inspect Evals와도 잘 짝이 맞는다.

## VS Code 통합 OSS — Cline · Continue · Goose · Roo

**Cline (구 Claude Dev).** VS Code 통합, 무료 OSS.[^cline] 데스크톱 통합이 깔끔하고 MCP 1급 지원. 가벼운 자리에서 강하다.

**Continue.** OSS 코파일럿/에이전트, 기업 자체 호스팅에 강점.[^continue] 사내 보안 정책상 외부 모델 API를 못 쓰는 환경에서 자체 호스팅 모델과 짝지어 자주 쓰인다. 24장에서 본격적으로 다룰 한국 사내 환경 케이스다.

**Goose (Block).** 데스크톱 에이전트, MCP 1급 시민.[^goose] 엔터프라이즈 IT 환경에서의 운영 사례가 두껍게 쌓이고 있다.

**Roo Code.** Cline 포크, 멀티에이전트와 커스텀 모드 강점.[^roo] 한 도구 안에서 여러 인격(Architect/Coder/Reviewer)을 갈아 끼우는 워크플로를 1급 지원한다.

이 넷은 — 솔직히 — 1차 CLI와 비교하면 *운영 두께*에서 한 단계 뒤다. 다만 *VS Code 안에서 다 끝내고 싶은 자리* 또는 *무료 OSS 우선* 같은 제약이 있다면 1차 후보로 든다.

## 멀티에이전트 프레임워크 — LangGraph · CrewAI · AutoGen

여기는 코딩 에이전트 *하네스*가 아니라 *멀티에이전트 오케스트레이션* 프레임워크 자리다. 14장에서 단일 vs 다중을 정리한 그 합의 위에서 — *다중*을 직접 짤 때 어느 도구를 쓸지의 자리다.

| 프로젝트 | 모델 | 특징 |
|---------|------|------|
| **LangGraph (LangChain)** | 그래프 기반 상태머신 | 산업 표준 |
| **CrewAI** | 역할 기반 협업 | 빠른 프로토타이핑 |
| **AutoGen (Microsoft)** | 대화형 멀티에이전트 | 학술 영향력 |
| **MetaGPT** | SOP 기반 가상 회사 | 페이퍼 영향 |
| **CAMEL** | 역할 시뮬레이션 | 초기 페이퍼 |

**LangGraph**가 산업 표준 자리에 가장 가깝다. 그래프 기반 상태머신 모델이 프로덕션 디버깅에 유리하다. **CrewAI**는 빠른 프로토타이핑에 좋다 — 역할 기반 협업이 시연용으로 매끄럽다. **AutoGen**은 학술 영향력이 가장 큰 페이퍼를 가졌다.

다만 14장의 합의를 잊지 말자. *쓰기 위주 의존성 강한 작업은 단일, 읽기 위주 병렬 가능 작업은 다중.* 멀티에이전트 프레임워크를 잡기 *전에* 자기 작업이 어느 쪽인지를 먼저 정하자. 도구를 먼저 정해 놓고 작업을 거기에 끼우면, 매번 *과적합한 시스템*을 짠다.

## 시그니처 인용 박스

> "AI is fast when it knows the answer; dangerous when it doesn't."
>
> *AI는 답을 알 때는 빠르고, 모를 때는 위험하다.*
>
> — **Pragmatic Engineer**, *Learnings from two years of using AI tools for software engineering*[^pragmatic-twoyears]

이 한 줄이 23장 도구 풍경 위에 떠 있어야 한다. 어떤 도구를 골라도 *모델이 답을 모르는 자리*에서는 위험이 있다. 그 위험을 막는 것이 도구의 비교축이 아니라 *하네스*다. Cursor가 좋아도, Claude Code가 좋아도 — 하네스가 모자라면 똑같이 무너진다. 도구 선택은 *시작*이지 *완성*이 아니다.

Addy Osmani가 같은 자리에서 더 정확하게 박았다.

> "They look more like each other than their underlying models do."
>
> *도구들은 그들이 굴리는 모델보다 *서로* 더 닮아 있다.*
>
> — Addy Osmani[^osmani]

같은 모델 위에서 도구 차이는 *생각보다 얇다*. 진짜 차이는 — 다시 — 하네스에서 난다. 도구는 하네스의 *외피*일 뿐이다.

## 실습 박스 — 자기 팀 워크플로에 8열 비교표 채우기

이번 주 안에 끝낼 수 있는 실습이다.

자기 팀이 *지금 쓰고 있는* 도구와 *후보로 보고 있는* 도구를 합쳐 5~7개를 정한다. 그 위에 위의 8열 비교표를 채운다 — *솔직하게* 채우자. 마케팅 페이지 카피를 그대로 옮기지 말고, *우리 팀의 실제 사용 경험*과 *문서를 직접 읽고 검증한 결과*로 채운다.

| 도구 | 격리 | MCP | 서브에이전트 | 메모리 | 오픈성 | 운영성숙도 | 관측 | 비용통제 |
|------|------|-----|-------------|--------|--------|----------|------|---------|
| Claude Code | | | | | | | | |
| Codex CLI | | | | | | | | |
| Cursor | | | | | | | | |
| Aider | | | | | | | | |
| (자기팀 후보) | | | | | | | | |

각 칸을 ○/△/× 3단계로 적자. 5단계는 사람이 일관성을 못 지킨다. 다 채운 뒤에 *비어 있거나 ×인 칸*을 본다. 그 자리가 자기 팀이 다음 분기에 *직접 짜야 할* 하네스 자리다. 가령 관측 열이 모두 △라면 — 15장의 5축 메트릭이 다음 우선순위다.

이 실습의 목적은 *완벽한 도구 선정*이 아니다. 도구 선택의 *근거를 8개 축으로 명시화*하는 거다. 그러면 다음 주 회의에서 "Cursor가 좋아 Claude Code가 좋아"라는 대화가 — *어느 축에서 어느 도구가 어떻게 다른가*로 바뀐다. 그게 더 빠르다.

## 정리해보자

기억해두자. **도구가 너무 많다 — 그래서 정답은 없고, 다만 좌표가 있다.** 8개 축(격리·MCP·서브에이전트·메모리·오픈성·운영성숙도·관측·비용통제)으로 비교하면 도구의 차이가 *명시적*으로 드러난다. 그 위에서 자기 팀의 병목이 어느 축인지를 보고 도구를 골라야 한다.

도구는 하네스의 외피다. 같은 모델 위에서 도구 차이는 — Osmani의 말처럼 — 모델 차이보다 얇다. 진짜 차이는 우리가 그 위에 올리는 *시스템 프롬프트, 도구 정의, AGENTS.md, 후크, 권한 게이트, 관측·비용 메트릭*에서 난다. 그게 23장이 끝까지 잊지 말자고 권하는 자리다.

도구를 골랐다면 — 한국에서 누가 무엇을 하는지를 보자. 24장은 우리 동네 지도다. 글로벌 자료만 좇다 보면 우리 동네를 모르는 부끄러움이 — 누구에게나 — 한 번쯤 찾아온다. 그 자리부터 솔직하게 시작하자.

[^claude-code]: Anthropic Claude Code. https://code.claude.com/docs/ko/overview
[^openai-harness]: OpenAI, *Harness engineering: leveraging Codex in an agent-first world*, 2026-02. https://openai.com/index/harness-engineering/
[^gemini-cli]: Google Gemini CLI/Code Assist 공식 문서.
[^cursor-best]: Cursor, *Best practices for coding with agents*. https://cursor.com/blog/agent-best-practices
[^cursor-subagents]: Cursor docs, *Subagents*. https://cursor.com/docs/subagents
[^cursor-changelog]: Cursor 2.4 changelog. https://cursor.com/changelog/2-4
[^aider]: Aider GitHub. https://github.com/paul-gauthier/aider
[^openhands-paper]: OpenHands team. *OpenHands: An Open Platform for AI Software Developers as Generalist Agents*. arXiv:2407.16741. https://arxiv.org/abs/2407.16741
[^openhands-eval]: OpenHands Evaluation Harness docs. https://docs.openhands.dev/openhands/usage/developers/evaluation-harness
[^cline]: Cline (구 Claude Dev) GitHub.
[^continue]: Continue.dev GitHub.
[^goose]: Block Goose GitHub.
[^roo]: Roo Code GitHub.
[^pragmatic-twoyears]: Pragmatic Engineer, *Learnings from two years of using AI tools for software engineering*. https://newsletter.pragmaticengineer.com/p/two-years-of-using-ai
[^osmani]: Addy Osmani, *Agent Harness Engineering*. https://addyosmani.com/blog/agent-harness-engineering/
