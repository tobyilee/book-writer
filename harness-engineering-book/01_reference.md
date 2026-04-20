# Harness Engineering 레퍼런스 문서

_책 제목 후보: "Harness Engineering — Claude Code와 Codex를 현업 에이전틱 코딩에 제대로 쓰는 법"_
_대상 독자: 현업 소프트웨어 엔지니어 (Claude Code/Codex CLI 일상 사용). git·CI·테스트·보안 기본기 보유._
_컴파일 일자: 2026-04-20. 소스: `research/web-research.md`, `research/community-research.md`, `research/paper-research.md`, `DEVELOPER_CURRICULUM.md`_

이 문서는 책 집필을 위한 근거 수집본이다. 모든 주장은 가능한 한 출처와 함께 명기했고, 출처가 약하거나 커뮤니티 단일 증언인 내용은 "추정" 혹은 "검증 필요" 태그를 붙였다. 중복되는 주장은 가장 강한 출처 하나만 남겼다.

---

## 1. 개념·정의

### 1.1 "하네스 엔지니어링"이란

**정의 (이 책이 채택하는):** LLM을 생산 업무에 쓸 때, 단일 프롬프트가 아니라 **프롬프트 + 규칙 파일 + 루프 + 도구 권한 + 관측**을 한 덩어리로 조립한 운영 구조. 말 그대로 모델에 씌우는 "하네스(harness, 마구)"다.

**주의 — 이 용어는 업계 표준이 아니다.** HumanLayer의 Dexter Horthy가 2025–2026년에 걸쳐 밀어붙인 교수법적 프레이밍으로 Geoffrey Huntley, Cline, 커뮤니티가 뒤따라 받아쓰면서 정착하는 중이다. Linux Foundation Agentic AI Foundation이 AGENTS.md를 표준화한 것과는 층이 다르다. 책은 이 점을 반복해서 명시해야 한다 (출처: https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents, https://ghuntley.com/ralph/).

HumanLayer의 성숙도 정의 (인용):
> "A basic production harness = CLAUDE.md + type checks + occasional subagents (covers ~15% of requirements). A complete harness = custom architectural rules, machine-readable constraint documents, dynamic tool scoping, verification hooks, cost dashboards (~80%)."

### 1.2 3세대 구도 (프롬프트 → 에이전트 → 하네스)

주류 내러티브는 다음과 같다.
1. **Prompt 1.0** (2022–2023): "더 좋은 프롬프트"가 곧 경쟁력
2. **Agent 2.0** (2023–2025): 도구 호출·루프·RAG
3. **Harness 3.0** (2025–): 규칙·훅·서브에이전트·관측·비용 규율까지 한 스택

**한계와 반증:**
- 이 3세대 구분 자체가 **마케팅 용어**에 가깝다. 각 조각(템플릿, cron, 권한, 옵저버빌리티)은 10년 전부터 있던 것이다. 새로운 것은 조립 순서가 아니라 조립 대상(LLM)이다.
- MIT/METR RCT (2025, 16명 숙련 개발자): Cursor + Claude 3.5/3.7 기준 **실측 19% 감속 / 본인 체감 20% 가속** — 39%p의 인지-현실 갭. "하네스가 생산성을 준다"는 주장 자체에 대한 가장 강한 반증 중 하나다 (출처: https://www.allaboutai.com/comparison/windsurf-vs-cursor/ 요약 경유, 원전 METR 보고서).
- Anthropic 자체 연구: AI 보조 참여자의 **코드 이해도가 17% 낮음** (출처: https://www.anthropic.com/research/AI-assistance-coding-skills). 하네스 숙달과 엔지니어링 역량은 같은 방향이 아닐 수 있다.

책은 "하네스가 유효하다"를 전제하지 말고 **유효 조건**을 탐색하는 방식으로 가야 한다.

### 1.3 Glossary (용어 사전)

**(A) 하네스 파일 어휘**
- **GOAL** — 하네스가 수행할 최종 목표. "무엇을" 정의.
- **RULE** — 구속 조건 (스타일·금지·보안). "어떻게 하지 말 것."
- **Spec** — 입력/출력/성공·실패 기준. 소프트웨어 명세서와 동일 개념 차용.
- **Drift** — 루프가 길어질수록 에이전트가 초기 지시에서 멀어지는 현상. arXiv 2601.04170 "Agent Stability Index"가 측정치 제공. 추정치로 장기 에이전트의 ~절반에서 발생.
- **Permission** — 도구·파일 접근 통제 (Claude Code rules, Codex approval policy).
- **Knowledge** — 재사용 가능한 사실/레시피. skills, memory bank, notepad.

> 주의: "6-layer 하네스 (GOAL/RULE/Spec/Drift/Permission/Knowledge)"는 일부 강의의 **교수법 비유**다. 파일 6개를 만들라는 뜻이 아니다 (커리큘럼 Module 1).

**(B) Karpathy의 3요소** (출처: https://github.com/karpathy/autoresearch)
- **Editable asset** — 에이전트가 수정 권한을 가진 **단 하나의** 파일/객체. "검색 공간을 해석 가능하게 유지."
- **Scalar metric** — 개선 판정의 단일 숫자. AutoResearch에선 `val_bpb` (validation bits per byte). 인간 판단 불필요.
- **Time-box** — 고정된 평가 사이클. 5분 훈련 → 시간당 12 실험 → 수면 중 100 실험.

**(C) 루프 패턴**
- **Ralph Loop** (Huntley) — `while :; do cat PROMPT.md | claude-code; done`. 2-prompt (PLAN/BUILD) · 1-loop.
- **ReAct** (Yao et al. 2022, arXiv:2210.03629) — Thought → Action → Observation 인터리브.
- **Plan-and-Execute** — 계획 1회 + 실행 다회. LangChain 구현이 대표.
- **Reflexion** (Shinn et al. 2023, arXiv:2303.11366) — 시도 후 자기 비평 → 에피소드 메모리 → 재시도.

**(D) 관측·제어 어휘**
- **Back-pressure** (Huntley) — 외부 검증 (테스트·린터·타입체커)이 루프에 걸어주는 되먹임 압력. LLM 자체 검증은 보조.
- **Exit hook** — 루프 종료 조건. `--max-iterations`, 델타 정체 감지, 토큰 상한.
- **Guardrail** — 파괴적 행위를 모델이 우회할 수 없도록 강제하는 외부 레이어. Claude Code 훅의 `permissionDecision: "deny"`가 `--dangerously-skip-permissions`도 이긴다 (출처: Claude Code docs, https://code.claude.com/docs/en/hooks-guide).
- **Completion promise** (Ralph 커뮤니티) — 모델이 "완료했다"고 거짓 선언하는 실패 모드. 외부 검증 없이 믿으면 안 됨.
- **Overcooking / Undercooking** — 루프가 너무 오래 돌아 불필요한 기능을 발명 (overcooking) 또는 너무 일찍 멈춰 반쯤 된 기능만 남기는 것 (undercooking).

---

## 2. 주요 관점과 프레임워크

### 2.1 Karpathy 3요소 + Partial Autonomy Slider

Karpathy의 AutoResearch (2024) repo가 공식 1차 출처다. 핵심 원칙 (인용):
> "Demo is works.any(), product is works.all()."
> "Make it easy, fast to win [on verification]. Keep AI on tight leash [on generation]."

**Partial Autonomy Slider**: Tab 자동완성 → Agent mode → Full auto. Tesla Autopilot의 레벨 비유. 자율성은 상수가 아니라 **슬라이더**이며, 개입률(intervention rate)이 실제 측정 가능한 지표다.

**일반화 가능 조건**: "Any system that exposes a scriptable asset, produces a measurable scalar outcome, and tolerates a time-boxed evaluation cycle is a candidate." 예: DB 쿼리 최적화 (asset=쿼리 설정, metric=p95 latency), 티켓 라우팅 (asset=분류 프롬프트, metric=hold-out 정확도).

### 2.2 Huntley Ralph Loop — 진짜 메시지

Ralph Loop은 **"무한 루프가 좋다"**가 아니라 **"루프 안에 plan/build 분리와 back-pressure를 박아야 한다"**가 핵심이다.

운영 원칙:
- **한 루프 당 한 가지만.** "operator must trust the LLM to decide what's the most important thing."
- PLANNING 프롬프트 — specs vs code 갭 분석 → 우선순위 TODO. 구현·커밋 금지.
- BUILDING 프롬프트 — 계획 있음 가정, 한 태스크 선택·구현·테스트 (back-pressure) ·커밋.
- 주 에이전트가 최대 500 병렬 subagent 스케줄 (탐색·기록용). build/test는 단일 subagent로 backpressure.

**실패 모드 (실측):**
- Ripgrep 기반 탐색이 오탐 → "don't assume an item is not implemented" 힌트 필수.
- 컨텍스트 clip이 ~147–152k에서 발생 (광고 200k 대비 실효 하한).
- `--dangerously-skip-permissions` 필수 → **샌드박스가 유일 방어선**.
- Ralph는 **refactor, migration, cleanup, conformance** 등 "성공을 스크립트로 판별 가능한" 작업에서 빛난다. 판단이 필요한 greenfield에서는 실패 (HN #46672413, #46750937).

### 2.3 Zaharia/BAIR — Compound AI Systems 프레이밍

Berkeley BAIR 블로그 (2024): https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/

> "State-of-the-art AI results are increasingly obtained by compound systems with multiple components, not just monolithic models." Databricks 서베이: 60% RAG, 30% multi-step chains.

**책이 차용하는 프레이밍**: 독자는 "단일 모델을 프롬프트 해킹"하는 법이 아니라 **"복합 시스템을 설계"**하는 법을 배운다. 모든 챕터는 어떤 compound 패턴 (cascade, debate, tree, SOP)을 쓰는지 명시해야 한다.

### 2.4 Anthropic "Building Effective Agents" — 공식 가이드

출처: https://www.anthropic.com/research/building-effective-agents + cookbook https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents

5가지 워크플로 패턴:
1. **Prompt Chaining** — 순차 호출 + 검증 게이트
2. **Routing** — 분류 후 전문 경로
3. **Parallelization** — voting (다수결) 또는 sectioning (독립 분할)
4. **Orchestrator-Workers** — 중앙 LLM이 동적 분해·위임
5. **Evaluator-Optimizer** — 생성/평가 루프, 반복 개선

핵심 인용:
> "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. (…) simple, composable patterns rather than complex frameworks."

Tool 설계 권고 (Anthropic): 명확한 문서·예제·경계, 자연스러운 텍스트에 가까운 포맷, 포매팅 오버헤드 회피, "poka-yoke" 설계.

### 2.5 AGENTS.md 스펙 (Linux Foundation Agentic AI Foundation)

출처: https://agents.md/

- Linux Foundation 산하 Agentic AI Foundation이 관리. 60,000+ OSS 프로젝트 채택 (검증 필요 — Foundation 자체 집계).
- Claude Code, Codex CLI, Gemini CLI, Cursor, Copilot 공통 인식.
- 규칙: **"closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."**
- Codex의 조회 순서: Global (`~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md`) → Project (루트→현재 디렉터리 각 레벨에서 override→표준→fallback) → `project_doc_max_bytes` (기본 32 KiB) 한도까지 concat.

**Claude Code의 CLAUDE.md와의 관계**: Claude Code는 CLAUDE.md + AGENTS.md를 병행 읽는다. 상향 트래버스하며 각 레벨이 **병합 (비대체적)**되어 컨텍스트에 삽입.

### 2.6 50% 컨텍스트 규칙 (Cline 텔레메트리)

출처: https://cline.bot/blog/how-to-think-about-context-engineering-in-cline

> "AI coding performance dips when context windows exceed 50%."

- Cline의 자사 텔레메트리 관찰. 200k 광고 컨텍스트여도 **실효 품질은 ~100k (50%)에서 저하 시작**.
- 대응 패턴 — **Focus Chain**: 기본 6 메시지마다 todo 재주입. **`new_task` 툴**: 50% 초과 시 요약-핸드오프.
- 이 관찰은 Claude Code의 147–152k 컨텍스트 clip (advertised 200k) 현상과 일치한다.

**책에 적용**: "컨텍스트는 크기보다 **활성 점유율**이 KPI"라는 원리로 여러 챕터에 걸쳐 반복 주입.

---

## 3. 도구별 실체

### 3.1 Claude Code

**기본 메커니즘** (출처: Claude Code 공식 docs, https://code.claude.com/docs/en):

- **메모리 파일 (CLAUDE.md)**: 프로젝트 루트에서 상향 트래버스, 병합·비대체. 공식 권장 <60줄 (실무 합의: <200줄, HN #44957443).
- **서브에이전트**: 프런트매터 필드 `name`, `description`(필수), `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`. `tools` 생략 시 부모 상속. `isolation: worktree`로 독립 파일시스템.
- **Skills vs Slash commands**: 같은 `/slash-command` 인터페이스로 통합됨 (v2.1+). Slash command = 사용자 호출 단일 파일. Skill = 모델 자동 호출, 다중 파일, 프런트매터로 `disable-model-invocation`, `user-invocable`, `allowed-tools` 제어. `/output-style`은 v2.1.73에서 **deprecated**.
- **Hooks 이벤트** (v2.1 기준, 27종): `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `Elicitation`, `ElicitationResult`, `SessionEnd`.
- **Hook 통신 규약 (인용)**: "Exit 0: the action proceeds… Exit 2: the action is blocked. Write a reason to stderr, and Claude receives it as feedback so it can adjust."
- **Hook 강제력 (인용)**: "A hook that returns permissionDecision: 'deny' blocks the tool even in bypassPermissions mode or with --dangerously-skip-permissions." → 자율 루프에서 **유일한 강제 게이트**.
- **MCP 권한**: 툴 이름 규약 `mcp__<server>__<tool>`. WebSearch/WebFetch 기본 비활성.
- **Settings 스코프**: User → Project committed → Project local → Managed policy (엔터프라이즈, 최우선). 평가 순서 deny → ask → allow, 첫 매치 승. 프로젝트 deny가 user allow를 이김.

**토큰 특성**:
- Extended thinking 기본 on → output token 과금. `/effort`, `MAX_THINKING_TOKENS=8000`으로 절감.
- Figma→Code 벤치: Claude Code 6.2M 토큰 vs Codex CLI 1.5M. **약 4× 높음** (출처: https://www.builder.io/blog/codex-vs-claude-code).
- Max plan 세션 한도: 정상 agentic 태스크로 1.5시간 내 소진 보고 (GitHub issue #38335).
- 단일 프롬프트가 주간 한도의 10% 소비 사례 (issue #10065).
- Opus auto-compact 시 5 compaction agent가 병렬 스폰 → 세션 쿼터 65% 조용히 소비 (issue #41866).
- Feb 2026 regression (issue #42796): `file reads per edit` 70% 감소, 173 premature stops/17일, 12× user interrupts, full-file rewrites 2배. Anthropic 내부 유효성 인정.

### 3.2 Codex CLI (OpenAI)

**기본 메커니즘** (출처: https://developers.openai.com/codex/):

- **AGENTS.md 조회 순서** (§2.5 참조).
- **Sandbox 모드 (정확한 이름)**:
  - `workspace-write` — 기본값, 워크스페이스 읽기/쓰기. `.git`, `.agents`, `.codex`는 쓰기 가능 모드에서도 read-only 유지.
  - `read-only`
  - `danger-full-access` — 권장 안 함
- **Approval 정책**:
  - `on-request` — 샌드박스 경계·네트워크 이탈 시 질의. 인터랙티브 기본
  - `never` — 질의 안 함, 비인터랙티브 전용
  - `untrusted` — 안전한 read 자동 승인, state-mutating 질의
  - `granular` — 범주별 선택적 승인
- **관계 (인용)**: "Sandbox enforces technical boundaries; approval enforces interaction boundaries." 독립 2 레이어.
- **위험 플래그**: `--dangerously-bypass-approvals-and-sandbox` → 모든 보호 제거.
- **Web search**: 기본 cached, `"live"` 지정 시 prompt injection 노출 급상승.

**Claude Code와의 발산 지점**:
| 축 | Claude Code | Codex CLI |
|---|---|---|
| 샌드박스 | 약함 (훅·권한 rule 기반) | **강함 (OS-enforced Seatbelt/Landlock 계열)** |
| 자율성 | supervised (plan mode + 훅) | unsupervised에 가까움 (full-auto 1–30분 비동기) |
| 토큰 | 4× 높음 | 낮음 |
| 장시간 세션 | 2시간+ 세션에서 초기 결정을 잊음. drift 완화는 CLAUDE.md + slash command 재주입 | 세션마다 AGENTS.md 1회 로딩 |

(출처: https://thoughts.jock.pl/p/ai-coding-harness-agents-2026)

### 3.3 Cursor / Aider / Continue / Cline

**Cursor** (출처: https://cursor.com/docs/context/rules):
- 레거시 `.cursorrules` → **Project Rules `.cursor/rules/*.mdc`**. MDC 포맷 (메타데이터+본문), path glob로 스코프.
- Memory Bank 패턴, User rules vs Project rules 분리.
- **40 tool silent cap** — MCP 도구가 40개 넘으면 조용히 truncate (§5 참조).

**Aider** (출처: https://aider.chat/docs/usage/modes.html):
- `CONVENTIONS.md`를 `--read`로 자동 read-only 주입.
- **Architect/Editor 모드**: 강한 모델 (o1 계열)이 설계, 빠른 모델 (GPT-4o, Sonnet)이 편집. 비용-품질 최적화.
- Auto-commit 기본 on → 자연스러운 롤백 포인트.
- 오픈소스.

**Cline** (출처: https://cline.bot/blog/):
- **Focus Chain** (6 메시지마다 todo 재주입), `new_task` 툴 (50% 초과 시 핸드오프), Memory Bank (5개 MD 파일: productContext/systemPatterns/techContext/activeContext/progress).
- 50% 컨텍스트 규칙 원천.

**Continue / Windsurf**:
- Windsurf: 자동 생성 Memories + 수동 Rules (`.windsurfrules`) 로컬/글로벌 분리.

**공통·차이 매트릭스** (커리큘럼 Module 0 발췌, 주요 축):

| 축 | Claude Code | Codex CLI | Cursor | Aider |
|---|---|---|---|---|
| 설정 파일 | CLAUDE.md + AGENTS.md | AGENTS.md | .cursor/rules + AGENTS.md | CONVENTIONS.md |
| 서브에이전트 | 네이티브 | 없음 | 없음 | 없음 |
| 훅 | 풍부 (27 이벤트) | 제한적 | 없음 | 없음 |
| Skills | 풍부 | 없음 | 제한적 | 없음 |
| MCP | 성숙 | 성숙 | 성숙 (40 cap) | 실험적 |
| 토큰 경향 | 4× 높음 | 낮음 | 중간 | 낮음 (diff) |
| 샌드박스 | 약함 | 강함 (OS) | 약함 | 없음 |
| 오픈소스 | 아니오 | 아니오 | 아니오 | **예** |

**전이 가능 (tool-agnostic) 패턴**: Markdown 메모리 + 세션 시작 재주입, 컨텍스트 임계치 요약-핸드오프, Path-scoped rules. **툴 고유**: Claude 훅, Codex OS-sandbox, Cursor MDC 메타는 직접 이식 어렵다.

---

## 4. 학술 레퍼런스 (챕터 매핑 포함)

이 책이 활용할 논문 27편. 각 항목: 1–2문단 요약 + 책의 어느 챕터에서 쓸지.

### 4.1 루프 패턴 (Ch 3–4 예정)

**ReAct** (Yao et al. 2022, arXiv:2210.03629, ICLR 2023)
ReAct는 자유 추론 트레이스와 도구 호출을 단일 루프에서 인터리브한다. Ablation: 추론만 있으면 환각, 행동만 있으면 길을 잃는다. ALFWorld에서 imitation/RL baseline 대비 **34%p 절대 성공률 개선**. 현대 코딩 에이전트 (SWE-agent, Claude Code, Cursor agents)가 상속받은 정전 (canonical) 루프.
→ **Ch 3 "루프의 해부학"에서 Ralph와 대비하여 소개**. 모든 루프 예제의 "Thought / Action / Observation" 원자 단위로 쓸 것.

**Reflexion** (Shinn et al. 2023, arXiv:2303.11366, NeurIPS 2023)
시도 후 자기 비평 → 반성 텍스트를 에피소드 메모리에 저장 → 다음 시도. 가중치 업데이트 없이 자연어로만 학습. HumanEval **91% pass@1** (당시 SOTA GPT-4의 80% 초과).
→ **Ch 4 "자기 개선 루프"에서 Ralph의 완화형으로 제시**. "컨텍스트 윈도우와 구분되는 영속 메모리 채널"을 설계 원칙으로 삼는다.

**Self-Refine** (Madaan et al. 2023, arXiv:2303.17651, NeurIPS 2023)
단일 LLM이 generator, feedback-giver, refiner 3역을 외부 신호 없이 수행. 7개 태스크 평균 **~20%p 절대 개선**. 구체적·실행 가능한 feedback이 조건.
→ **Ch 3 "왜 루프가 원샷을 이기는가"의 도입 예제**.

**Tree of Thoughts** (Yao et al. 2023, arXiv:2305.10601, NeurIPS 2023)
CoT를 탐색 트리로 일반화. 각 스텝에서 후보 thoughts 생성 → 자체 평가 → 유망 분기 확장. Game of 24: **74% (ToT) vs 4% (CoT) GPT-4** — 20배 점프. 비용은 극적으로 증가.
→ **Ch 5 "test-time compute를 설계 변수로"에서 Snell과 묶어서 취급**.

**Chain-of-Verification (CoVe)** (Dhuliawala et al. 2023, arXiv:2309.11495, ACL 2024 Findings)
4-step: draft → plan verification Q → **independent** answer → synthesize. 독립 답변 스텝이 핵심 — 원 draft를 합리화하지 못하게.
→ **Ch 6 "검증 설계" 실습 과제의 기본 형태**.

### 4.2 검증 (Ch 6–7 예정)

**MT-Bench / LLM-as-a-Judge** (Zheng et al. 2023, arXiv:2306.05685, NeurIPS 2023 D&B)
GPT-4 judge가 인간 간 일치도와 동등 (>80%) 수준이나 **position bias, verbosity bias, self-enhancement bias** 3종이 체계적으로 존재. 완화: swap (A/B + B/A), reference-guided grading.
→ **Ch 6 개방 논문**. 모든 eval 챕터에서 "pairwise-with-swap"을 기본 프로토콜로.

**Judging the Judges** (Thakur et al. 2024, arXiv:2310.08419 / 2406.12624)
가장 큰 judge만 인간과 합리적 정렬, 그조차 inter-human에 못 미친다. 쌍별 일치도가 높아도 **absolute 스코어는 5점 차이**. **절대 스코어는 노이즈, relative ranking만 신뢰.**
→ **Ch 6 "LLM-as-judge의 한계" 섹션의 핵심 레퍼런스**.

**Constitutional AI** (Bai et al. 2022, Anthropic, arXiv:2212.08073)
Self-critique-and-revise (SL) + RLAIF 2단계. 명시적 "constitution" 기반. 현대 generator–critic 하네스의 이론적 토대, Claude 훈련의 기반.
→ **Ch 6 "Critic에게도 rubric이 필요하다"에서 인용**.

**Multi-Agent Debate** (Du et al. 2023, arXiv:2305.14325, ICML 2024)
여러 모델 인스턴스가 독립 답변 → 서로 추론을 debate → 수렴. 수학·전략 추론 크게 향상, 환각 감소. Black-box, fine-tune 불필요. 비용은 agent·round 선형.
→ **Ch 7 "비싼 검증: 언제 쓸 만한가"의 상한 예시**.

**RLAIF vs RLHF** (Lee et al. 2023, Google, arXiv:2309.00267, ICML 2024)
요약·대화·harmlessness에서 RLAIF가 RLHF와 동등. Direct-RLAIF는 초과. 합성 피드백이 인간 피드백의 대체가 될 수 있음.
→ **Ch 6 "LLM-judge 파이프라인을 1급 학습 신호로 본다"의 근거**.

### 4.3 코드 에이전트 (Ch 2, 8–9 예정)

**SWE-bench** (Jimenez et al. 2023, arXiv:2310.06770, ICLR 2024)
12개 인기 Python repo의 2,294 실제 이슈. 출시 당시 Claude 2가 **1.96%** 해결. HumanEval 스타일 합성과 실 엔지니어링의 거리를 폭로.
→ **Ch 2 "현실과 벤치마크 사이의 간극"** 중심 레퍼런스. 1.96% → 60%+ 진전을 내러티브 spine으로.

**SWE-agent** (Yang et al. 2024, arXiv:2405.15793, NeurIPS 2024)
**Agent-Computer Interface (ACI)** 개념 도입: "LM은 새로운 종류의 사용자다." 인간용 shell/editor가 LM에겐 나쁜 UX. 커스텀 ACI로 SWE-bench **~4%→12.5%**, HumanEvalFix 87.7%. 모델이 아니라 **하네스**가 헤드룸.
→ **Ch 8 "하네스 디자인이 모델 선택을 이긴다"의 spine**. 책 전체가 사실상 ACI 엔지니어링임을 명시.

**AutoCodeRover** (Zhang et al. 2024, arXiv:2404.05427, ISSTA 2024)
코드를 flat file이 아닌 AST·클래스/메서드 그래프로 취급. LLM + spectrum-based fault localization. SWE-bench-lite **19% @ $0.43/issue** — 경쟁자 대비 한 자릿수 저비용.
→ **Ch 9 "검색은 grep이 아니다"** 핵심 논거.

**Voyager** (Wang et al. 2023, arXiv:2305.16291, TMLR 2024)
Minecraft agent가 **스킬 라이브러리**를 자동 커리큘럼으로 성장. 각 스킬은 NL 설명으로 인덱스된 executable code. 3.3× 고유 아이템, 15.3× tech-tree 진도.
→ **Ch 9 "Skills as persistence"의 근거**. Claude Code Skills 설계가 이 아이디어의 직계.

**AI Agents That Matter** (Kapoor et al. 2024, Princeton, arXiv:2407.01502)
현 agent 문헌의 가장 날카로운 비판. 4가지 진단: accuracy-only 벤치가 비용 폭발을 가림, 연구 벤치가 사용자 필요와 괴리, 약한 holdout로 overfit, 평가가 비표준. **"SOTA agents are needlessly complex and costly."**
→ **Ch 1부터 마지막까지 관통하는 Contrarian 레퍼런스**. 모든 실습에 cost-accuracy Pareto 2축 요구.

**MetaGPT** (Hong et al. 2023, arXiv:2308.00352, ICLR 2024)
SOP (Standardized Operating Procedures)를 역할 특화 에이전트 프롬프트 시퀀스로 인코딩 (PM, architect, engineer, QA). SOP 스캐폴딩이 naive chaining의 cascading 환각을 실측 감소.
→ **Ch 8 "다중 에이전트가 아니라 SOP"** 섹션의 경고 사례.

**CodeAct** (Wang et al. 2024, arXiv:2402.01030, ICML 2024)
JSON/text action format을 **executable Python**으로 대체. 하나의 CodeAct 스텝이 Python control flow로 도구를 합성 → round-trip 감소. API-Bank에서 **+20% 성공률**.
→ **Ch 8 "tool call = code block"의 논거**. Claude Code bash 툴, Codex CLI 직접 실행이 이 가설의 상속자.

### 4.4 메트릭 (Ch 5, Capstone 예정)

**MINT** (Wang et al. 2023/2024, arXiv:2309.10691, ICLR 2024)
20 모델 평가. **"strong single-turn performance doesn't predict strong multi-turn performance."** Per-turn 개선 1–8% (tools), 2–17% (language feedback).
→ **Ch 5 "진짜 KPI는 multi-turn cost-per-resolution"** 근거.

**AgentBench** (Liu et al. 2023, arXiv:2308.03688, ICLR 2024)
8 환경 (OS, DB, KG, card-game, shopping, household, code). 3대 실패 모드: long-horizon reasoning, decision-making under uncertainty, instruction-following. 코드 훈련이 일관된 이득은 아님.
→ **Ch 5 "왜 에이전트가 실패하는가" 분류의 뼈대**.

### 4.5 보안 (Ch 10 예정)

**Not What You've Signed Up For — Indirect Prompt Injection** (Greshake et al. 2023, arXiv:2302.12173, AISec '23)
간접 인젝션 (데이터에 심은 악성 지시)의 첫 체계적 연구. Bing Chat, GPT-4 코드 완성에 실제 공격 시연. 데이터 탈취, 웜, 생태계 오염, 임의 코드 실행 분류.
→ **Ch 10 Day 1 토픽**. 웹·문서 retrieval 하네스의 기본 위협 모델.

**Instruction Hierarchy** (Wallace et al. 2024, OpenAI, arXiv:2404.13208)
System / developer / user / tool-output을 **우선순위-정렬**해야 한다. 데이터 생성 레시피로 훈련. GPT-3.5 변형에서 unseen injection에 대한 강건성 크게 상승. GPT-4o에 반영됨.
→ **Ch 10 "prompt schema를 security design으로"** 핵심.

**StruQ** (Chen et al. 2024, arXiv:2402.06363, USENIX Security 2025)
**구조적 방어**: 데이터와 지시를 별도 채널로 전달, fine-tune된 모델이 데이터 채널의 지시를 무시. Utility 손실 근사 0.
→ **Ch 10 "channel separation"** 섹션. 첫 번째로 가르칠 아키텍처 패턴.

**ToolEmu** (Ruan et al. 2023, arXiv:2309.15817, ICLR 2024)
LLM으로 툴을 시뮬레이션해 risky action 평가. 36 high-stakes tool, 144 test case. **가장 안전한 agent도 23.9% 실패**. 68.8% flagged failure가 실세계 실패.
→ **Ch 10 "production 전 안전성 평가의 표준"**.

**Agent-SafetyBench** (Zhang et al. 2024, Tsinghua, arXiv:2412.14470)
349 환경, 2,000 test case, 8 위험 범주. **16 인기 LLM agent 중 safety 60% 넘는 것 없음.** "Prompt-level 방어만으로는 부족."
→ **Ch 10 "왜 systemic safety인가"** 결론 근거.

**Sleeper Agents** (Hubinger et al. 2024, Anthropic, arXiv:2401.05566)
조건부 악성 (예: "year=2024이면 exploit 삽입") 이 SFT, RLHF, adversarial training을 견딘다. **Adversarial training이 제거 아닌 은폐**.
→ **Ch 10 "prompt injection 너머의 위협"** 사이드바. 본문 중심이 아니라 "당신이 모를 수 있는 것" 컨텍스트.

### 4.6 비용 (Ch 11 예정)

**FrugalGPT** (Chen, Zaharia, Zou 2023, Stanford, arXiv:2305.05176, TMLR 2024)
3 전략: prompt adaptation, LLM approximation, LLM **cascade**. Cascade 하나로 GPT-4 품질에서 **98% 비용 절감** 가능한 경우 존재.
→ **Ch 11 "cascade"** 기본 레퍼런스. 계산 예제 포함.

**RouteLLM** (Ong et al. 2024, Berkeley/Anyscale, arXiv:2406.18665, ICLR 2025)
ChatBot Arena preference 데이터로 **학습된 라우터**. 품질 유지하며 **2×+ 비용 절감**. 모델 쌍 변경에도 전이.
→ **Ch 11 "cascade vs 학습 라우터"** 대비.

**Speculative Decoding** (Leviathan, Kalman, Matias 2022/2023, Google, arXiv:2211.17192, ICML 2023 Oral)
작은 draft 모델이 K 토큰 제안 → 큰 모델이 병렬 검증. 분포 불변 증명. T5-XXL에서 **2–3× 속도**.
→ **Ch 11 "에이전트 루프가 production 지연시간에 작동하는 이유"** 한 다이어그램 챕터.

**Test-Time Compute Scaling** (Snell et al. 2024, Berkeley/Google DeepMind, arXiv:2408.03314)
Compute-optimal 테스트-타임 할당 (난이도 인식, 프롬프트 특화)이 best-of-N을 **4×** 효율로 이기고, 태스크에 따라 **14× 큰 모델**과 동등. "thinking harder" 모드 (o1, Claude thinking)의 이론적 기반.
→ **Ch 5 & Ch 11에서 이중 참조**. test-time compute를 모델 선택·컨텍스트 길이와 동급의 설계 변수로.

**Compound AI Systems** (Zaharia et al. 2024, BAIR 블로그)
§2.3 참조.
→ **서문과 Ch 1의 프레이밍 에세이**.

---

## 5. 사례와 Contrarian 증거

각 사례는 책에서 "주장 → 반증/제한 → 어떻게 다룰지" 구조로 쓴다.

### 5.1 MIT/METR RCT — 19% 감속 vs 20% 체감 가속
- 16명 숙련 개발자, Cursor + Claude 3.5/3.7, 실제 태스크.
- **측정상 19% 느려짐, 본인 체감은 20% 빨라짐. 39%p 갭.**
- 출처: METR 보고서 (2025). 커뮤니티 리서치 THEME 10 참조.
- **책에서**: 서문 첫 장면. "당신이 빨라졌다고 느낀다는 사실 자체가 증거가 아니다."

### 5.2 AGENTS.md 효과 실험
- HN #47034087 링크 논문: 개발자가 쓴 AGENTS.md는 **+4%**, LLM이 생성한 AGENTS.md는 **−3%**.
- 실천가 팁 (인용): "I only add information to AGENTS.md when the agent has failed at a task. Then I revert the desired changes, re-run, and see if the output has improved."
- 출처: https://news.ycombinator.com/item?id=47034087
- **책에서**: Ch (AGENTS.md 장)의 개방 Contrarian. "AGENTS.md를 LLM에게 쓰게 하면 역효과다."

### 5.3 GitHub Issue #42796 (Feb 2026 regression)
- 파워 유저 `stellaraccident`: 70% file-reads-per-edit 감소, 173 premature-stops/17일 (이전 0), 12× user interrupts, 전체 파일 rewrite 2배.
- Anthropic 스태프가 보고 유효성 인정.
- 출처: https://github.com/anthropics/claude-code/issues/42796
- **책에서**: "공식 changelog는 현실에 뒤진다. GitHub issue가 operational intelligence다." 챕터.

### 5.4 GitHub MCP 46k 토큰 팽창 / Cursor 40-tool silent cap
- GitHub 공식 MCP: 91 툴 = **46k 토큰**. 개별 비활성 불가. "went from 34k to 80k just by adding the GitHub MCP."
- 툴 선택 정확도 **95%→71%** (focused vs full GitHub MCP). 출처: https://eclipsesource.com/blogs/2026/01/22/mcp-context-overload/
- Cursor: 40 툴 초과 시 silent truncate.
- 출처: https://smcleod.net/2025/08/stop-polluting-context-let-users-disable-individual-mcp-tools/
- **책에서**: "MCP는 많을수록 좋다"의 반증.

### 5.5 MCP "weekend hype → production walkaway" — Perplexity 사례
- CTO Denis Yarats, Ask 2026: 자체 MCP 서버 출시 4개월 뒤 내부 사용 중단, 전통 API + CLI로 복귀. 사유: 컨텍스트 윈도우 소비 + clunky auth.
- Garry Tan (YC president): "MCP sucks honestly... I got sick of it and vibe coded a CLI wrapper instead."
- mcp2cli: MCP→CLI 변환으로 **99% 토큰 감소** 사례.
- 출처: https://news.ycombinator.com/item?id=47380270, https://dev.to/shreyaan/we-invented-mcp-just-to-rediscover-the-command-line-4n5c
- **책에서**: "MCP를 last resort로 쓰라" 섹션.

### 5.6 Claude Code 토큰 소비 ≈ 4× Codex CLI
- Figma→Code 클론 벤치마크: Claude Code 6.2M vs Codex 1.5M.
- 출처: https://www.builder.io/blog/codex-vs-claude-code
- **책에서**: 도구 선택 매트릭스.

### 5.7 Ralph Loop 어휘: Overcooking / Undercooking / Completion promise
- Leanware.co, alteredcraft, Huntley 커뮤니티 합의.
- Overcooking: 루프가 영원히 돎, 기능 발명, 불필요한 docs.
- Undercooking: 너무 일찍 멈춤, 반쪽 기능.
- Completion promise: 모델이 "끝났다"고 거짓 선언. 외부 검증 전까지 믿지 않기.
- **책에서**: Ch 3 루프 실패 분류.

### 5.8 Fake tests / Fake implementations
- HN #46691243 (edude03): agent가 `expect(true).to.be(true)` 형태 30개 unit test 작성, 자체 검증 게임.
- embedding-shape 사례: "Server-Sent Events" 라벨인데 실제는 HTTP 응답 큐잉.
- 출처: https://news.ycombinator.com/item?id=46691243
- **책에서**: Ch 6 "에이전트가 게임할 수 없는 검증 설계".

### 5.9 Anthropic 자체 skill-atrophy 발견
- AI 보조 참여자의 **코드 이해도 17% 낮음** vs hand-coder.
- CMU/Microsoft 연구: AI 의존도 ↑ → critical thinking ↓.
- 출처: https://www.anthropic.com/research/AI-assistance-coding-skills
- **책에서**: "왜 여전히 학습해야 하는가" 직접 대응 챕터.

### 5.10 Amazon Q 90-day freeze
- Q3 2025 사고 이후 Amazon이 90일 코드 배포 freeze 발령. Amazon Q의 "high blast radius changes" 최소 1건.
- 출처: 추정치 — 커뮤니티 인용, 원 기사 검증 필요.
- **책에서**: Ch 10 사이드바 "조직이 멈춘 사례".

### 5.11 GitHub "Prompt Injection Data Heist"
- 악성 issue 본문이 MCP 툴 write 권한을 트리거 → private repo 데이터 유출.
- 출처: https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/
- **책에서**: Ch 10 핵심 케이스.

### 5.12 rogue `postmark-mcp` (2025-09)
- 악성 npm MCP가 이메일 탈취.
- 출처: https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html
- **책에서**: Ch 10 MCP 공급망.

### 5.13 Worktree cleanup bug (#45645) & Mid-chat rollback (#29684)
- Claude Code cleanup이 stale `repositoryformatversion=1` 남김 → 다른 IDE AI agent 깨뜨림.
- Mid-chat rollback: Claude가 응답을 rollback해도 side effect (commit, file)는 persists → "orphaned commits, files in unknown states."
- 출처: https://github.com/anthropics/claude-code/issues/45645, #29684
- **책에서**: Ch 롤백/회복의 반례.

### 5.14 한국어 회고 — velog @softer
- SuperClaude 설치 오염, User/.claude + Project/.claude 이중 스코프 혼선, 프론트엔드 아키텍처 이해 취약.
- 처방: **Cornell-notes 스타일 색인화 CLAUDE.md**.
- 출처: https://velog.io/@softer/Claude-Code-%EC%82%AC%EC%9A%A9-%ED%9A%8C%EA%B3%A0
- **책에서**: Ch 2 로컬화된 예시.

### 5.15 한국어 진단 — velog @justn-hyeok
- Claude Code "이상 행동" 근본 원인 진단: adaptive thinking + effort downgrade.
- 환경변수 우회 (임시): `CLAUDE_CODE_EFFORT_LEVEL=high`, `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`.
- 출처: https://velog.io/@justn-hyeok/off-claude-code-adaptive-thinking
- **책에서**: Ch 운영 트러블슈팅 레시피.

---

## 6. 논쟁점 (Contrarian per-chapter)

챕터별 Contrarian 시그널. 각각 "주류 주장 → 반증/제한 → 책에서 어떻게 다룰지" 구조.

### Ch 1 — 하네스 입문
**주류**: "하네스가 생산성을 2–10× 올린다."
**반증**: MIT/METR RCT — 숙련 개발자 **19% 감속 / 20% 가속 체감**. Anthropic 자체 연구 — 코드 이해도 **17% 낮음**. "AI Agents That Matter" — accuracy-only 벤치가 비용 폭발을 가림.
**다룰 방식**: 서문 첫 장면으로 체감-측정 갭을 공개한다. 독자의 "내가 빨라졌다"는 감각부터 의심하게 만든다. 각 챕터 끝 "측정 숙제"를 붙인다.

### Ch 2 — CLAUDE.md / AGENTS.md
**주류**: "AGENTS.md를 잘 쓰면 성능이 오른다."
**반증**: HN #47034087 논문 — 사람이 쓴 건 **+4%**, LLM이 쓴 건 **−3%**. 60줄·200줄 공식 권장 자체가 "몰빵 금지"의 다른 이름.
**다룰 방식**: AGENTS.md를 "스타일 가이드"가 아닌 **"실패 로그"**로 재정의. 실패 후 추가 → revert → 재실행 → 차이 측정 루프 제시. "LLM에게 AGENTS.md 쓰게 하지 말 것"을 규칙으로.

### Ch 3 — 루프 (Ralph·ReAct)
**주류**: "Ralph Loop이 최신·최강이다."
**반증**: HN #46672413 "Ralph Wiggum Doesn't Work" — "greenfield에서 수백 달러 소비하고 실패." #46750937 "What Ralph loops are missing" — **계획 과정, 보안·데이터 모델링·성능 체크리스트 결여**. Ralph는 refactor, migration, cleanup, conformance 등 **스크립트로 성공을 판별 가능한** 태스크에서만 작동.
**다룰 방식**: Ralph를 "4개 루프 패턴 중 1개"로 자리매김. "판단이 필요한 태스크는 Ralph 부적합" 디스퀄리파이어 규칙을 선언.

### Ch 4 — Reflection·Self-Improvement
**주류**: "자기 비평 (Reflexion, Self-Refine)이 품질을 높인다."
**반증**: MT-Bench — self-bias +8~15%. 같은 모델이 자기 출력을 평가하면 체계적으로 높게 매김. Judge verbosity bias → 긴 답이 선호되는데 "길이에 가중치 두지 말라"고 명시해도 완화 부족.
**다룰 방식**: Reflexion은 "피드백이 **가능**한 태스크"에서만. Self-bias를 pairwise-with-swap + 별도 critic 모델로 완화하는 프로토콜을 제시.

### Ch 5 — 메트릭과 Goodhart
**주류**: "scalar metric이 있으면 자동화 가능하다."
**반증**: Kapoor "AI Agents That Matter" — accuracy-only 최적화는 비용 폭발을 가림. MINT — single-turn 성능이 multi-turn을 예측 못함. Flaky metric은 루프를 노이즈 추종기로 만든다.
**다룰 방식**: **Pareto 2축 (cost × accuracy)** 의무화. 모든 캡스톤 평가에 개입률 (intervention rate) 서브메트릭 추가.

### Ch 6 — 검증 (LLM-as-judge)
**주류**: "LLM-as-judge는 인간 수준이다" (MT-Bench 인용).
**반증**: Judging the Judges — 최대 judge만 인간과 정렬, 인간 간 일치도에 못 미침. Position/verbosity/self bias는 프롬프트로 완화 어려움. **Absolute 스코어는 노이즈**, relative ranking만 신뢰.
**다룰 방식**: pairwise-with-swap을 default 프로토콜로. 절대 점수 기반 리더보드는 실습에서 금지.

### Ch 7 — 다중 에이전트·서브에이전트
**주류**: "Agent team이 단일 agent보다 낫다."
**반증**: Arsturn 현실 분석 — auto-delegation hit-or-miss. 3–4× 토큰 multiplier. Reddit skeptic: "overhyped, falls apart in real world." MetaGPT — naive chaining은 cascading 환각.
**다룰 방식**: Decision tree 제시 — single-agent default → subagent (격리 목적) → team (coordination/critique이 가치일 때만). 항상 비용 multiplier 공시.

### Ch 8 — 도구·MCP
**주류**: "MCP가 많을수록 에이전트가 유능해진다."
**반증**: GitHub MCP 46k 토큰 / 91 툴, 개별 비활성 불가. 툴 선택 정확도 **95%→71%**. Perplexity의 weekend hype→walkaway. Cursor 40-tool silent cap은 문제의 인정. mcp2cli 99% 토큰 절감.
**다룰 방식**: "MCP는 last resort." 세션당 활성 툴 <20 권장. CLI 래퍼 선호. Perplexity 사례를 walkaway 교재로.

### Ch 9 — 서치와 컨텍스트
**주류**: "grep/ripgrep이면 충분하다."
**반증**: Ralph Huntley의 "don't assume an item is not implemented" 힌트. AutoCodeRover — AST·심볼 그래프가 grep 기반 SWE-agent를 저비용으로 이김.
**다룰 방식**: AST·LSP·심볼 그래프 retrieval를 Ch 9의 중심 기술로.

### Ch 10 — 보안·위협 모델
**주류**: "system prompt에 지시를 잘 쓰면 막을 수 있다."
**반증**: Agent-SafetyBench — **16 agent 모두 safety 60% 미만**. StruQ가 요구하는 것은 채널 분리 — 훈련 데이터가 아니라 **구조**. ToolEmu — 가장 안전한 agent도 23.9% 실패. Sleeper Agents — adversarial training은 은폐.
**다룰 방식**: 프롬프트 방어를 넘어 **아키텍처 방어** (sandbox, channel separation, instruction hierarchy, hook enforcement) 로 중심 이동.

### Ch 11 — 비용·CI·운영
**주류**: "강한 모델 하나 쓰면 해결."
**반증**: FrugalGPT — cascade로 **98% 절감** 가능한 경우 존재. RouteLLM — 학습 라우터로 2×+. Snell — test-time compute 4× 효율로 14× 큰 모델을 이김. Claude Code extended thinking 기본 on이 과금 주범.
**다룰 방식**: cascade/router/test-time compute 삼박자를 묶어서 가르침. 모든 실습에 실 토큰·$ 측정 필수.

### Ch 12 — 팀·조직 스케일
**주류**: "AI PR은 빠르니 좋다."
**반증**: Amazon Q 사고 → 90일 freeze. GitHub issue #29684 — mid-chat rollback이 orphaned commit 남김. "AI가 썼으니 통과" 관행이 리뷰 붕괴 유발.
**다룰 방식**: AI PR을 **일반 PR과 동일한 리뷰 강도**로. worktree isolation + merge 전 human gate 1회를 조직 정책으로.

> Contrarian 시그널 12개 확보 (요구 8개 초과).

---

## 7. 참고문헌

### 7.1 학술 논문 (arXiv·컨퍼런스)

**루프**
- Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023. arXiv:2210.03629. https://arxiv.org/abs/2210.03629
- Shinn, N., et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023. arXiv:2303.11366. https://arxiv.org/abs/2303.11366
- Madaan, A., et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS 2023. arXiv:2303.17651. https://arxiv.org/abs/2303.17651
- Yao, S., et al. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. arXiv:2305.10601. https://arxiv.org/abs/2305.10601
- Dhuliawala, S., et al. (2023). Chain-of-Verification Reduces Hallucination in LLMs. ACL 2024 Findings. arXiv:2309.11495. https://arxiv.org/abs/2309.11495

**검증**
- Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023 D&B. arXiv:2306.05685. https://arxiv.org/abs/2306.05685
- Thakur, A. S., et al. (2024). Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges. GEM 2025 (ACL Workshop). arXiv:2310.08419. https://arxiv.org/abs/2310.08419
- Bai, Y., et al. (Anthropic, 2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073. https://arxiv.org/abs/2212.08073
- Du, Y., et al. (2023). Improving Factuality and Reasoning in Language Models through Multiagent Debate. ICML 2024. arXiv:2305.14325. https://arxiv.org/abs/2305.14325
- Lee, H., et al. (Google, 2023). RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback. ICML 2024. arXiv:2309.00267. https://arxiv.org/abs/2309.00267

**코드 에이전트**
- Jimenez, C. E., et al. (2023). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR 2024. arXiv:2310.06770. https://arxiv.org/abs/2310.06770
- Yang, J., et al. (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS 2024. arXiv:2405.15793. https://arxiv.org/abs/2405.15793
- Zhang, Y., et al. (2024). AutoCodeRover: Autonomous Program Improvement. ISSTA 2024. arXiv:2404.05427. https://arxiv.org/abs/2404.05427
- Wang, G., et al. (2023). Voyager: An Open-Ended Embodied Agent with Large Language Models. TMLR 2024. arXiv:2305.16291. https://arxiv.org/abs/2305.16291
- Kapoor, S., et al. (Princeton, 2024). AI Agents That Matter. arXiv:2407.01502. https://arxiv.org/abs/2407.01502
- Hong, S., et al. (2023). MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework. ICLR 2024. arXiv:2308.00352. https://arxiv.org/abs/2308.00352
- Wang, X., et al. (2024). Executable Code Actions Elicit Better LLM Agents (CodeAct). ICML 2024. arXiv:2402.01030. https://arxiv.org/abs/2402.01030

**메트릭**
- Wang, X., et al. (2023/2024). MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback. ICLR 2024. arXiv:2309.10691. https://arxiv.org/abs/2309.10691
- Liu, X., et al. (2023). AgentBench: Evaluating LLMs as Agents. ICLR 2024. arXiv:2308.03688. https://arxiv.org/abs/2308.03688

**보안**
- Greshake, K., et al. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. AISec '23 (ACM CCS Workshop). arXiv:2302.12173. https://arxiv.org/abs/2302.12173
- Wallace, E., et al. (OpenAI, 2024). The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions. arXiv:2404.13208. https://arxiv.org/abs/2404.13208
- Chen, S., et al. (2024). StruQ: Defending Against Prompt Injection with Structured Queries. USENIX Security 2025. arXiv:2402.06363. https://arxiv.org/abs/2402.06363
- Ruan, Y., et al. (2023). ToolEmu: Identifying the Risks of LM Agents with an LM-Emulated Sandbox. ICLR 2024. arXiv:2309.15817. https://arxiv.org/abs/2309.15817
- Zhang, Z., et al. (Tsinghua, 2024). Agent-SafetyBench: Evaluating the Safety of LLM Agents. arXiv:2412.14470. https://arxiv.org/abs/2412.14470
- Hubinger, E., et al. (Anthropic, 2024). Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training. arXiv:2401.05566. https://arxiv.org/abs/2401.05566

**비용·효율**
- Chen, L., Zaharia, M., Zou, J. (Stanford, 2023). FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance. TMLR 2024. arXiv:2305.05176. https://arxiv.org/abs/2305.05176
- Ong, I., et al. (Berkeley/Anyscale, 2024). RouteLLM: Learning to Route LLMs with Preference Data. ICLR 2025. arXiv:2406.18665. https://arxiv.org/abs/2406.18665
- Leviathan, Y., Kalman, M., Matias, Y. (Google, 2022/2023). Fast Inference from Transformers via Speculative Decoding. ICML 2023 Oral. arXiv:2211.17192. https://arxiv.org/abs/2211.17192
- Snell, C., et al. (Berkeley/Google DeepMind, 2024). Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. arXiv:2408.03314. https://arxiv.org/abs/2408.03314
- Zaharia, M., et al. (Berkeley BAIR, 2024). The Shift from Models to Compound AI Systems. BAIR 블로그. https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/ (접속 2026-04-20)

> 합계 **27편** 충족. 각 논문의 챕터 매핑은 §4에 기재.

### 7.2 1차 웹 자료 (공식 문서·1차 저자)

Claude Code 공식 문서 (모두 접속 2026-04-20):
- Memory / CLAUDE.md. https://code.claude.com/docs/en/memory
- Sub-agents. https://code.claude.com/docs/en/sub-agents
- Skills. https://code.claude.com/docs/en/skills
- Hooks guide. https://code.claude.com/docs/en/hooks-guide
- MCP. https://code.claude.com/docs/en/mcp
- Settings. https://code.claude.com/docs/en/settings
- Sandboxing. https://code.claude.com/docs/en/sandboxing
- Costs. https://code.claude.com/docs/en/costs
- Code review. https://code.claude.com/docs/en/code-review

Codex CLI 공식 문서:
- AGENTS.md guide. https://developers.openai.com/codex/guides/agents-md
- Agent approvals & security. https://developers.openai.com/codex/agent-approvals-security
- Security. https://developers.openai.com/codex/security

Anthropic 엔지니어링 블로그:
- Building effective agents. https://www.anthropic.com/research/building-effective-agents
- Demystifying evals for AI agents. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Long-running Claude. https://www.anthropic.com/research/long-running-Claude
- AI-assistance coding skills study. https://www.anthropic.com/research/AI-assistance-coding-skills
- Managed agents. https://www.anthropic.com/engineering/managed-agents

표준·스펙:
- AGENTS.md 스펙 (Linux Foundation Agentic AI Foundation). https://agents.md/
- Model Context Protocol security best practices. https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
- Cursor Rules docs. https://cursor.com/docs/context/rules

1차 저자 블로그:
- Huntley, G. Ralph Wiggum as a Software Engineer. https://ghuntley.com/ralph/ (접속 2026-04-20)
- Huntley, G. these days i approach everything as a loop. https://ghuntley.com/loop/
- HumanLayer. Skill Issue — Harness Engineering for Coding Agents. https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
- HumanLayer. A Brief History of Ralph. https://www.humanlayer.dev/blog/brief-history-of-ralph
- Karpathy, A. autoresearch repo. https://github.com/karpathy/autoresearch
- Karpathy on Software 3.0 — Latent Space. https://www.latent.space/p/s3
- Cline. Context engineering in Cline (50% rule). https://cline.bot/blog/how-to-think-about-context-engineering-in-cline
- Cline. new_task tool for context handoff. https://cline.bot/blog/unlocking-persistent-memory-how-clines-new_task-tool-eliminates-context-window-limitations
- Aider. Architect/Editor modes. https://aider.chat/docs/usage/modes.html

### 7.3 2차 해설·실천 정리

- Alex Op. Understanding Claude Code full stack. https://alexop.dev/posts/understanding-claude-code-full-stack/
- Alex Op. Claude Code customization guide. https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/
- Pub Nub. Best practices for Claude Code sub-agents. https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
- dev.to / myougatheaxo. Claude Code in monorepos. https://dev.to/myougatheaxo/claude-code-in-monorepos-hierarchical-claudemd-and-package-scoped-instructions-1il9
- Medium / devops-ai. The Virtual Monorepo Pattern. https://medium.com/devops-ai/the-virtual-monorepo-pattern-how-i-gave-claude-code-full-system-context-across-35-repos-43b310c97db8
- thoughts.jock.pl. AI Coding Harness Agents 2026. https://thoughts.jock.pl/p/ai-coding-harness-agents-2026
- Builder.io. Codex vs Claude Code. https://www.builder.io/blog/codex-vs-claude-code
- New Stack. Karpathy autonomous experiment loop. https://thenewstack.io/karpathy-autonomous-experiment-loop/
- Buttondown / Verified. The Karpathy Loop inside autoresearch. https://buttondown.com/verified/archive/the-karpathy-loop-inside-the-autoresearch-repo/
- Kong Engineering. Claude Code governance with an AI Gateway. https://konghq.com/blog/engineering/claude-code-governance-with-an-ai-gateway
- Docker. MCP Horror Stories — GitHub Prompt Injection. https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/
- NVIDIA Developer. Practical security guidance for sandboxing agentic workflows. https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/
- eclipsesource. MCP context overload. https://eclipsesource.com/blogs/2026/01/22/mcp-context-overload/
- smcleod. Stop polluting context — let users disable MCP tools. https://smcleod.net/2025/08/stop-polluting-context-let-users-disable-individual-mcp-tools/
- incident.io. Shipping faster with Claude Code and git worktrees. https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees
- sngeth. Opencode permission rules protecting git worktrees. https://sngeth.com/opencode/ai/git/worktrees/terraform/2026/03/10/opencode-permission-rules-protecting-git-worktrees/
- Vercel. Agent PR review. https://vercel.com/docs/agent/pr-review
- Qodo. pr-agent. https://github.com/qodo-ai/pr-agent
- mindstudio. Claude Code agent teams vs sub-agents. https://www.mindstudio.ai/blog/claude-code-agent-teams-vs-sub-agents
- Arsturn. Are Claude Code subagents actually useful. https://www.arsturn.com/blog/are-claude-code-subagents-actually-useful-a-realistic-look-at-their-value
- minimaxir (Max Woolf). AI agent coding — skeptic tries it. https://minimaxir.com/2026/02/ai-agent-coding/
- allaboutai. Windsurf vs Cursor (MIT/METR RCT 요약 포함). https://www.allaboutai.com/comparison/windsurf-vs-cursor/
- The Hacker News. First malicious MCP server found. https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html
- ColeMurray. claude-code-otel. https://github.com/ColeMurray/claude-code-otel
- kenryu42. claude-code-safety-net. https://github.com/kenryu42/claude-code-safety-net

### 7.4 GitHub Issues (operational intelligence)

- anthropics/claude-code #42796 — Feb 2026 regression. https://github.com/anthropics/claude-code/issues/42796
- anthropics/claude-code #10065 — Long multi-step tasks dropped. https://github.com/anthropics/claude-code/issues/10065
- anthropics/claude-code #38335 — Max plan exhaustion. https://github.com/anthropics/claude-code/issues/38335
- anthropics/claude-code #41866 — Extreme token burn. https://github.com/anthropics/claude-code/issues/41866
- anthropics/claude-code #45645 — Worktree cleanup bug. https://github.com/anthropics/claude-code/issues/45645
- anthropics/claude-code #29684 — Mid-chat rollback. https://github.com/anthropics/claude-code/issues/29684

### 7.5 커뮤니티 토론 (Hacker News 등)

- Ask HN: evidence agentic coding works? #46691243. https://news.ycombinator.com/item?id=46691243
- Evaluating AGENTS.md #47034087. https://news.ycombinator.com/item?id=47034087
- AGENTS.md open format #44957443. https://news.ycombinator.com/item?id=44957443
- Ralph Wiggum Doesn't Work #46672413. https://news.ycombinator.com/item?id=46672413
- What Ralph Wiggum loops are missing #46750937. https://news.ycombinator.com/item?id=46750937
- MCP is dead; long live MCP #47380270. https://news.ycombinator.com/item?id=47380270
- Skeptic tries agent coding (Max Woolf) #47183527. https://news.ycombinator.com/item?id=47183527
- dev.to — We invented MCP just to rediscover the command line. https://dev.to/shreyaan/we-invented-mcp-just-to-rediscover-the-command-line-4n5c

### 7.6 한국어 커뮤니티 출처 (별도)

- velog @softer. "Claude Code 사용 회고" — 컨텍스트 오염, 과잉 엔지니어링, Cornell-notes CLAUDE.md 제안. https://velog.io/@softer/Claude-Code-사용-회고
- velog @justn-hyeok. "Claude Code가 요즘 이상하다면?" — adaptive thinking/effort level 진단과 환경변수 우회. https://velog.io/@justn-hyeok/off-claude-code-adaptive-thinking
- DEVOCEAN. "개발 파트너, AI 코딩 에이전트 체험기" — Copilot/Cursor/Windsurf/Junie/Jules 병행 사용 회고. https://devocean.sk.com/blog/techBoardDetail.do?ID=167592
- Toss Tech. "개발자는 AI에게 대체될 것인가." https://toss.tech/article/will-ai-replace-developers
- OKKY `claude-code` 태그. https://okky.kr/questions/tagged/claude-code
- hyperdev.matsuoka.com. When Claude forgets how to code. https://hyperdev.matsuoka.com/p/when-claude-forgets-how-to-code

---

## 8. 리서치 한계

커버하지 못한 영역 / 약한 영역을 명시한다. 책 집필 시 이 부분을 넘겨짚지 말 것.

1. **일본어·중국어 커뮤니티 미수집**: Qiita, 掘金, CSDN의 실무 회고는 이번 리서치에 포함되지 않았다. 한국어와는 또 다른 운영 현장 지식이 있을 가능성이 높다.
2. **Twitter/X와 YouTube 댓글**: 검색 API 제약으로 체계적 수집 실패. Karpathy 등의 최신 짧은 발언은 2차 소스 경유.
3. **Amazon Q 90-day freeze 사건**: 커뮤니티 인용에 의존. 1차 기사·인시던트 리포트 **검증 필요**.
4. **METR RCT 수치 (19%/20%)**: allaboutai 요약 경유. 원 보고서 직접 재확인 권장.
5. **arXiv 2601.04170 "Agent Stability Index"**: community-research에만 언급. 원 논문 직독 안 함 — 본문에서 인용 시 재검토.
6. **Claude Code Feb 2026 regression 수치 (70%, 173, 12×)**: 단일 파워유저 `stellaraccident` 보고. Anthropic이 유효성은 인정했으나 수치는 1인 측정.
7. **AGENTS.md 채택 수 "60,000+"**: Foundation 자체 집계. 검증 어려움.
8. **Claude Code 토큰 4× 벤치**: 단일 태스크 (Figma→Code) 1회 측정. 일반화 전제 시 주의.
9. **책의 성격상 추가 필요**: "팀 스케일"(팀당 CLAUDE.md 분기 전략, 반복 PR 처리), "IDE 플러그인 (Copilot/Continue) 특성", "온프레미스·에어갭 환경"은 얕게 다뤄졌다.
10. **법적·규제 컨텍스트**: AI 저작권, 기업 보안 규정 (SOC2·ISO27001) 상의 하네스 운영은 다루지 않았다. 챕터 스코프에서 의도적 제외.

**시간 편향**: Q1 2026 자료가 과대 대표. 2024–2025 자료는 상대적으로 적다. 빠르게 바뀌는 분야이므로 책 출간 시점에 §5 사례는 일부 날짜 확인이 필요할 수 있다.

---

_이 파일이 책 집필 Phase의 유일한 근거 문서다. 각 챕터가 본문에 인용을 박을 때 §4·§5·§6의 항목 번호를 트래킹하면 중복을 피할 수 있다._
