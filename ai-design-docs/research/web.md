# 웹 리서치: AI 코딩 에이전트와 함께 시작하는 프로젝트의 설계·문서화

- 슬러그: `ai-design-docs` · 장르: `tech-book`
- 검색 시점: 2026-10 (작업일 2026-10-28)
- 핵심 원전: `research/primary/ai-project-design-guidelines-ko.md` (이하 "원전 가이드", 01~14절)
- 범위: 일반 웹(공식 문서·릴리스·엔지니어링 블로그·실무자 에세이·업계 설문). 논문(EARS 원 논문, METR 연구 등)과 커뮤니티 토론(HN·Reddit·GeekNews 댓글)은 다른 리서처 몫이라 제외했다.

**인용 표기 규칙**
- `>` 인용은 원문 그대로 옮긴 것이다. 다만 대부분 WebFetch(요약 모델 경유)로 가져왔으므로, 본문에 그대로 넣을 문장은 fact-checker가 원문 URL에서 한 번 더 대조하는 것을 권한다. `gh api`로 직접 읽은 GitHub 원문(README·docs)은 [원문 직접 확인]으로 표시했다.
- [2차 출처]는 1차 원문을 열지 못하고 언론·블로그 요약을 통해 확인한 내용이다. [미확인]은 출처끼리 엇갈리거나 1차 확인이 안 된 내용이다.
- 버전·수치는 "{버전}/{연도} 기준"으로 못 박았다. 이 분야는 몇 주 단위로 바뀌므로, 날짜가 2025년인 자료에는 "구버전 정보일 수 있음"을 붙였다.

---

## A. 사용자 도구 스택 식별 (Claude Code · Codex · Hermes · OpenAI dots)

### 자료 A1: Hermes Agent — Nous Research (GitHub 저장소·공식 문서)
- 출처: https://github.com/NousResearch/hermes-agent · 문서 https://hermes-agent.nousresearch.com/docs/
- 저자·날짜: Nous Research. 저장소 생성 2025-07-22. 첫 GitHub 릴리스 v0.2.0 (2026-03-12). 최신 릴리스 **v0.22.5 (2026-10-23)**. 라이선스 MIT. GitHub 스타 약 25.8만 (2026-10-28 조회) [원문 직접 확인: `gh api`]
- 신뢰성: 최상 (1차 소스)
- 식별 결론: 의뢰서의 "Hermes"는 **Nous Research의 오픈소스 자가 개선형 에이전트 "Hermes Agent"**로 보는 것이 맞다. 코딩 전용 도구라기보다 범용 상시 에이전트다. CLI·TUI·메신저 게이트웨이(Telegram·Discord·Slack 등)로 접근하고, cron 스케줄러·서브에이전트·스킬·장기 기억을 갖춘다. 번들 스킬로 **Claude Code·Codex·OpenCode에 코딩을 위임**한다. 즉, 독자 환경에서 Hermes는 "직접 코딩하는 에이전트"라기보다 **코딩 에이전트를 부리는 자동화·오케스트레이션 층**이다.
- 핵심 사실 (README, 2026-10 기준):
  > "The self-improving AI agent built by Nous Research. It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions." [원문 직접 확인]
  > "Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. ... Compatible with the agentskills.io open standard." [원문 직접 확인]
  > "Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended." [원문 직접 확인]
  > "Spawn isolated subagents for parallel workstreams." [원문 직접 확인]
- 컨텍스트 파일 규칙 (docs `user-guide/features/context-files.md`, 2026-10 기준) — 이 책의 "문서가 에이전트를 조종한다" 논지에 직접 쓰인다:
  > "Only **one** project context type is loaded per session (first match wins): `.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`." [원문 직접 확인]
  > "When your working directory sits inside a git repository, Hermes loads a **merged chain** of `AGENTS.md` files at session start: the git-root `AGENTS.md` first, then the `AGENTS.md` in every intermediate directory down to your working directory. Deeper files appear later in the prompt, so more specific guidance takes precedence." [원문 직접 확인]
  > "As the agent navigates into subdirectories during the session ... it **progressively discovers** context files in those directories and injects them into the conversation at the moment they become relevant." [원문 직접 확인]
- 기억 (docs `features/memory.md`): `MEMORY.md` 2,200자(~800 토큰), `USER.md` 1,375자(~500 토큰) 상한. 세션 시작 시 "frozen snapshot"으로 주입된다. 상한을 넘으면 자동 압축하지 않고 오류를 돌려준다. [원문 직접 확인]
  > "Don't point two agent processes at the same Hermes home directory. Memory writes are automatic and load back into the system prompt at session start, so two writers sharing one home will compound each other's entries into state neither of them (nor you) authored." [원문 직접 확인]
- 코딩 위임 스킬 (docs `skills/bundled/autonomous-ai-agents/...claude-code.md`): 번들 스킬 `claude-code` v2.2.1. "Delegate coding to Claude Code CLI (features, PRs)". 같은 계열로 `codex`, `opencode` 스킬이 있다. [원문 직접 확인]
- Hermes 저장소 자체도 루트 `AGENTS.md` + 하위 디렉터리별 `AGENTS.md`(`agent/`, `tools/`, `cron/`, `skills/` 등)를 "Routing Table — working in X → read X/AGENTS.md" 방식으로 운용한다. 계층형 컨텍스트 파일의 실사례로 쓸 수 있다. [원문 직접 확인: `gh search code`]
- 주의: 출시일을 두고 2차 출처가 엇갈린다(2025-07 vs 2026-02). 1차 사실은 "저장소 생성 2025-07-22, 첫 태그 릴리스 2026-03-12"이다. 블로그 기사의 "v0.9.0 Everywhere Release 2026-04-13", "v0.20.0 Herald Release 2026-08-03" 등은 [2차 출처]다.
- 관련 섹션: 원전 10절(AI 역할과 결정 한계), 09절(통제 지점—자동화 에이전트가 PR·CI에 들어올 때), 12절(메타데이터—에이전트가 읽는 머리말). Hermes의 cron 감사·문서 정원 가꾸기(doc gardening) 자동화 예시로 활용할 수 있다.

### 자료 A2: OpenAI dots — ChatGPT의 상시(always-on) 에이전트
- 출처(1차, 열람 실패): OpenAI 도움말 "Getting started with your dot" https://help.openai.com/en/articles/20001530-getting-started-with-your-dot (403), OpenAI "How we build safety, security and privacy into dots" https://openai.com/index/how-we-build-safety-security-and-privacy-into-dots/ (403)
- 출처(2차, 열람 성공): TechCrunch, Lucas Ropek, 2026-09-29 https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/ · DataCamp, Matt Crabtree, 2026-09-29 https://www.datacamp.com/blog/openai-dots
- 신뢰성: 중 (1차 문서 존재는 검색으로 확인했으나 본문 접근 불가. 내용은 다수 언론으로 교차 확인)
- 식별 결론: "OpenAI Dots"는 **실재한다.** 정식 표기는 소문자 **"dots"**(단수 "a dot")이고, **OpenAI DevDay 2026(2026-09-29)**에 발표된 **ChatGPT 내 상시 실행 개인 에이전트**다. 코딩 전용 도구가 아니라 범용 비서형 에이전트이며, 코딩 작업은 Codex로 넘긴다.
- 교차 확인된 사실 (2026-09/10 기준):
  - 각 dot은 자체 클라우드 컴퓨터와 브라우저에서 실행되고, 대화 사이에도 목표를 계속 진행한다 (TechCrunch·DataCamp·도움말 제목 검색 결과 일치).
  - 모델: **GPT-6 Astra** (TechCrunch: "powered by GPT-6 Astra").
  - 제공 범위: ChatGPT Pro(EEA·스위스·영국 제외)와 Business Premium. Enterprise·Edu·Healthcare는 관리자가 켜는 베타 (DataCamp). TechCrunch 인용: "Dots will be available starting Tuesday in ChatGPT, for Pro and Business Premium users in eligible markets."
  - 채널: ChatGPT(데스크톱·웹·모바일), Slack, Teams. 문자 메시지는 이후 또는 제한 베타.
  - 통제 장치 (DataCamp, OpenAI 안전 문서 인용): "Custom Rules let you override them per action." 규칙별로 4가지 행동(묻지 않고 실행 / 사전 승인 시 실행 / 먼저 묻기 / 넘기기) 중 하나를 고른다. "Auto-review sits underneath, checking actions that could affect your accounts or share information."
  - 기억: "Your dot inherits memories from ChatGPT and creates its own." (DataCamp). 일부 출처는 사용자가 개별 dot 기억을 보거나 지울 수 없다고 적는다 [2차 출처, 미확인].
  - **Codex 연계** (DataCamp): dot은 Codex 클라우드 환경에서 클라우드 태스크를 만들 수 있다(환경은 Codex에서 미리 만들어야 함). 로컬 접근을 켜면 사용자 기기에서 Work·Codex 태스크를 만든다. 개발자 예시로 "고객 피드백을 모니터링하다가 영상이 첨부된 PR을 돌려주는 dot"이 있다. TechCrunch는 dot을 Codex나 ChatGPT에서 띄울 수 있다고 적는다.
- [미확인] 항목: "4,000개 이상 앱 연결", "GPT-6.1 Astra 업그레이드 보류" 보도(aiweekly 단독), 가격 세부. 공식 DevDay 요약 URL(https://openai.com/index/devday-2026-recap/)은 2차 출처가 언급만 했고 열람하지 못했다.
- 책에 쓸 때의 주의: dots는 출시 한 달 된 제품이다. 기능·제공 범위는 "2026-10 기준"으로 못 박고, 공식 도움말 문서를 다시 대조할 것. dot에 대한 기능 서술은 위 교차 확인 범위를 넘지 말 것.
- 관련 섹션: 원전 10절(AI 역할의 결정 한계—Custom Rules의 "ask first / hand off"는 원전의 "중단 조건·결정 요청"과 같은 구조), 09절(자동 생성 PR이 통제 지점을 통과해야 함).

### 자료 A3: 도구 버전 스냅샷 (npm·GitHub 조회, 2026-10-28)
- Claude Code: `@anthropic-ai/claude-code` **2.1.312** (npm, 2026-10-27 갱신) [원문 직접 확인]
- OpenAI Codex CLI: `@openai/codex` **0.165.0** (npm, 2026-10-28 갱신), GitHub `rust-v0.165.0` 2026-10-27 [원문 직접 확인]
- Hermes Agent: **v0.22.5** (2026-10-23) [원문 직접 확인]
- GitHub Spec Kit: **v1.2.4** (2026-10-27), v1.0.0은 2026-08-21 [원문 직접 확인]
- OpenSpec (Fission-AI): **v1.15.0** (2026-10-24), 저장소 생성 2025-08-05 [원문 직접 확인]
- BMAD Method: 안정판 **v6.12.4** (2026-10-14), v7은 프리뷰 알파 (README: "The v7 release ETA is October 16, 2026, and it might be sooner.") [원문 직접 확인]
- Agent OS (Builder Methods): **v3.0.0** (2026-01-20) [원문 직접 확인]
- 관련 섹션: 책 서두의 "이 책의 기준 시점" 박스, 부록.

---

## B. 에이전트 컨텍스트 파일과 하네스 (CLAUDE.md · AGENTS.md · 스킬 · 훅 · 플랜 모드)

### 자료 B1: Claude Code 공식 문서 — Best practices
- 출처: https://code.claude.com/docs/en/best-practices (구 URL https://www.anthropic.com/engineering/claude-code-best-practices 는 이 문서로 308 리다이렉트됨)
- 저자·날짜: Anthropic. 페이지에 날짜 표기 없음. 2026-10 검색 시점 내용 (Claude Code 2.1.x 기준)
- 신뢰성: 최상
- 핵심 주장: 모든 지시는 **비결정적(모델이 읽고 판단: 프롬프트·CLAUDE.md·스킬)**이거나 **결정적(하네스가 강제: 훅·deny 규칙·관리 설정)**이다. CLAUDE.md는 코드에서 알 수 없는 것만 짧게 적고, 예외가 없어야 하는 규칙은 훅으로 옮긴다. 에이전트에게 통과/실패로 돌아오는 검사를 쥐여 주고, "다 통과" 대신 증거를 요구한다.
- 인용 가능한 구절:
  > "Non-deterministic: you write the instruction, and Claude (the model) reads it. This can be your prompt, `CLAUDE.md`, or a skill. ... there's no *guarantee* that it'll follow your instructions."
  > "Deterministic: you configure the instruction, and Claude Code (the harness) *has* to execute this. This can be a hook, a deny rule, or a managed setting."
  > "If you keep adding emphasis to a `CLAUDE.md` line and Claude still misses it, that's a sign the line belongs in a hook."
  > "Only write down what Claude can't find by reading the repo, or what it would otherwise spend time rediscovering every session."
  > "What it can't find is the information that was never in the repo: A decision your team made in a meeting / A deploy process that lives in one person's head / The environment variable your integration tests need"
  > "I want to add rate limiting to the public API but haven't thought it through yet. Interview me until you could write the spec, then write it to SPEC.md."
  > "Once `SPEC.md` exists, start a fresh session to build from it, so the build begins with a clean context and a written definition of done."
  > "Claude stops when the work looks done. If it has nothing to run that tells it whether the work actually *is* done, \"looks done\" is all it has to go on. In practice that makes you the test suite"
  > "ask Claude for *evidence*: the command it ran and its output, or the screenshot. \"All tests pass\" on its own tells you very little"
  > "use a subagent to review the rate limiter diff against SPEC.md, check every requirement is implemented and the listed edge cases have tests, report gaps that affect correctness and skip style"
  > "A reviewer that's asked to find problems will always find *something*. If you fix every finding, you end up with extra abstraction layers and tests for cases that can't happen."
  > "If something has to happen every time, make it a hook, a deny rule, or a managed setting. `CLAUDE.md` is for guidelines, and Claude is allowed to decide a guideline doesn't apply."
- 표 하나("Who has the last word": 비결정적 = "Claude's summary of what it did", 결정적 = "Branch protection, a person who approves the merge")는 원전 09절 "통제 지점" 표와 1:1로 대응된다.
- 관련 섹션: 원전 01절(문서의 세 가지 일), 09절(자동 검사와 사람 검토 분담, "AI가 검토 완료"는 증거가 아님), 10절 프롬프트 4(보고: 실행 명령과 결과), 06절 VAL-CAN-01.

### 자료 B2: Claude Code 공식 문서 — How Claude remembers your project (CLAUDE.md·AGENTS.md·자동 기억)
- 출처: https://code.claude.com/docs/en/memory
- 저자·날짜: Anthropic, 날짜 표기 없음, 2026-10 기준. 일부 기능은 버전 명시(`/doctor prompt-audit`는 "Claude Code v2.1.283 or later")
- 신뢰성: 최상
- 핵심 주장: CLAUDE.md는 "강제 설정이 아니라 컨텍스트"다. 파일당 200줄 이하 권장. `@path` 임포트는 정리에 도움이 되지만 컨텍스트 비용은 줄이지 않는다. 경로 한정 규칙(`.claude/rules/` + `paths:`)으로 필요할 때만 싣는다. **Claude Code는 AGENTS.md를 직접 읽는다**(CLAUDE.md가 없을 때).
- 인용 가능한 구절:
  > "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead. The more specific and concise your instructions, the more consistently Claude follows them."
  > "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
  > "**Consistency**: if two instructions contradict each other, Claude may pick one arbitrarily."
  > "Claude Code can read `AGENTS.md` as your project instructions, so a repository already set up for other coding agents works without adding a `CLAUDE.md`, an import, or a setting."
  - 표: AGENTS.md만 있으면 AGENTS.md를 읽고, AGENTS.md와 CLAUDE.md가 함께 있으면 "Your `CLAUDE.md` files only", CLAUDE.md가 AGENTS.md를 임포트하면 둘 다.
  > "The [`/doctor`] checkup proposes trims for a checked-in CLAUDE.md: it cuts content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews, and keeps pitfalls, rationale, and conventions that differ from tool defaults."
  - 자동 기억 `MEMORY.md`는 "first 200 lines or 25KB"만 세션 시작 시 로드.
- 주의: "AGENTS.md를 CLAUDE.md 대신 읽는다"는 동작은 2025년 자료(“Claude Code는 AGENTS.md를 지원하지 않으니 심볼릭 링크하라”)와 다르다. 2025년 블로그 인용 시 "구버전 정보일 수 있음".
- 관련 섹션: 원전 02절(원본 하나—CLAUDE.md에 규칙 본문을 복사하지 말고 링크), 12절(메타데이터), 14절(흔한 실패: 같은 규칙을 여러 곳에 복사).

### 자료 B3: AGENTS.md 공식 사이트
- 출처: https://agents.md/
- 저자·날짜: Agentic AI Foundation(Linux Foundation 산하) 관리. 날짜 표기 없음, 2026-10 기준
- 신뢰성: 최상
- 핵심 주장: AGENTS.md는 "에이전트를 위한 README". 가장 가까운 파일이 우선한다. 빌드·테스트 명령, 코드 스타일, 테스트 지침, 보안 고려 등을 담는다.
- 인용 가능한 구절:
  > "Think of AGENTS.md as a README for agents"
  > "used by over 60k open-source projects"
  > "AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation."
  > "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."
  - 지원 도구 목록에 Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Junie, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Phoenix, Semgrep, GitHub Copilot coding agent, Ona, Windsurf, Augment Code 등이 있다. (Claude Code는 이 페이지 목록에 없지만, B2대로 2026-10 기준 직접 읽는다.)
- 관련 섹션: 원전 02절, 10절 "공통 입력 꾸러미".

### 자료 B4: OpenAI Codex 문서 — AGENTS.md 탐색 규칙
- 출처: https://learn.chatgpt.com/docs/agent-configuration/agents-md (구 URL https://developers.openai.com/codex/guides/agents-md 에서 308 리다이렉트)
- 저자·날짜: OpenAI, 날짜 표기 없음, 2026-10 기준 (Codex CLI 0.16x)
- 신뢰성: 최상
- 핵심 주장: Codex는 전역(`~/.codex`)에서 첫 비어 있지 않은 파일 하나, 프로젝트에서는 루트에서 현재 디렉터리까지 내려가며 디렉터리마다 `AGENTS.override.md` → `AGENTS.md` → 대체 파일명 순으로 최대 1개를 읽어 이어 붙인다. 합계가 `project_doc_max_bytes`(기본 32 KiB)에 닿으면 멈춘다.
- 인용 가능한 구절:
  > "Starting at the project root (typically the Git root), Codex walks down to your current working directory."
  > "Codex includes at most one file per directory."
  > "Codex concatenates files from the root down, joining them with blank lines."
  > "Files closer to your current directory override earlier guidance because they appear later in the combined prompt."
  > "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes`" (기본 32 KiB)
  > "Filenames not on this list are ignored for instruction discovery."
- 책 활용: 32 KiB 상한은 "AGENTS.md에 설계 문서를 통째로 넣지 말고 원본 경로만 가리켜라"는 원전 10절 "필요한 원본과 관련 연결만 포함"의 기술적 근거가 된다.
- 관련 섹션: 원전 02절, 10절.

### 자료 B5: OpenAI Codex 문서 — Best practices (플랜 모드·4요소 프롬프트·스킬·서브에이전트)
- 출처: https://learn.chatgpt.com/guides/best-practices (구 URL https://developers.openai.com/codex/learn/best-practices 에서 리다이렉트)
- 저자·날짜: OpenAI, 날짜 표기 없음, 2026-10 기준
- 신뢰성: 최상
- 핵심 주장: 플랜 모드로 맥락 수집·질문·계획을 먼저 한다. 프롬프트에는 Goal / Context / Constraints / Done when 4요소를 넣는다. 같은 실수를 두 번 하면 회고 후 AGENTS.md를 갱신한다. 반복되는 프롬프트는 스킬로 만든다.
- 인용 가능한 구절:
  > "Plan mode lets Codex gather context, ask clarifying questions, and build a stronger plan before implementation."
  > "A good default is to include four things in your prompt:" (Goal, Context, Constraints, Done when)
  > "What should be true before the task is complete, such as tests passing, behavior changing" (Done when 설명)
  > "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`."
  > "if you keep reusing the same prompt or correcting the same workflow, it should probably become a skill."
  > "Keep the main agent focused on the core problem, and use subagents for tasks like exploration, tests, or triage."
  - 흔한 실수로 "Running live tasks on the same files without using Git worktrees"를 든다.
- [2차 출처] Codex 플랜 모드 토글은 `/plan` 또는 Shift+Tab, 프로젝트 스킬 위치는 `.agents/skills/<name>/SKILL.md`, 훅은 `.codex/hooks.json`(기능 플래그 필요하다는 2차 기술 있음). 훅 이벤트 수 비교("Claude Code 27 vs Codex 5")는 비공식 저장소 주장이라 [미확인].
- 관련 섹션: 원전 10절 "공통 입력 꾸러미"(목표·범위·원본·검증 명령·중단 조건)와 Codex의 4요소를 대조하는 표로 쓸 수 있다.

### 자료 B6: OpenAI Cookbook — Using PLANS.md for multi-hour problem solving (ExecPlan)
- 출처: https://developers.openai.com/cookbook/articles/codex_exec_plans
- 저자·날짜: OpenAI, 페이지에 저자·날짜 없음. 페이지가 "archived, may reference outdated models"라고 표시함 (본문에 `gpt-5.2-codex` 권장 언급 → **구버전 정보일 수 있음**, 2025 말~2026 초 작성 추정)
- 신뢰성: 최상(공식) / 최신성 주의
- 핵심 주장: ExecPlan은 "코딩 에이전트가 따라 할 수 있는 설계 문서"다. 진행·발견·결정 로그·회고 섹션을 의무로 두는 살아 있는 문서이고, 초심자도 이 파일 하나로 성공할 수 있게 자기완결적이어야 한다. 수용 기준은 사람이 관찰할 수 있는 동작으로 쓴다.
- 인용 가능한 구절:
  > "a design document that a coding agent can follow to deliver a working feature or system change."
  > "ExecPlans must contain and maintain a `Progress` section, a `Surprises & Discoveries` section, a `Decision Log`, and an `Outcomes & Retrospective` section."
  > "Every ExecPlan is a living document."
  > "Every ExecPlan must be fully self-contained."
  > "Every ExecPlan must produce a demonstrably working behavior"
  > "Acceptance should be phrased as behavior a human can verify"
  > "When writing complex features or significant refactors, use an ExecPlan" (AGENTS.md에 넣을 문장 예)
- 관련 섹션: 원전 02절 `plan/`, 06절 SLICE-CAN-01, 08절(결정 로그 vs ADR 구분), 12절 검증 기록 템플릿.

### 자료 B7: OpenAI — Harness engineering: leveraging Codex in an agent-first world
- 출처: https://openai.com/index/harness-engineering/ (WebFetch 403 — 본문 직접 열람 실패)
- 저자·날짜: Ryan Lopopolo (OpenAI Member of Technical Staff), **2026-02-11** [검색 결과 스니펫과 InfoQ 2026-02-21 기사로 확인]
- 신뢰성: 최상(원문) / 이 파일의 인용은 검색 스니펫 수준이라 [원문 재대조 필요]
- 핵심 주장 (검색 스니펫에 원문 문장으로 노출된 것):
  > "We had weeks to ship what ended up being a million lines of code. Over that period, roughly 1,500 pull requests have been opened and merged with a small team of just three engineers"
  > "The first commit to an empty repository landed in late August 2025. Even the initial AGENTS.md file that directs agents how to work in the repository was itself written by Codex."
  > "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified."
  > "Humans may review pull requests, but aren't required to. Over time, we've pushed almost all review effort towards being handled agent-to-agent."
  > "A giant instruction file crowds out the task, the code, and the relevant docs"
- [2차 출처] 여러 해설(InfoQ, yage.ai, Adobe ai-repo-harness-guide, Viblo)이 전하는 내용: AGENTS.md를 백과사전이 아닌 **목차(~100줄)**로 두고 깊은 내용은 구조화된 `docs/`(설계 문서·실행 계획·아키텍처 결정·품질 점수)로 보낸다. 사용자 정의 린터·구조 테스트로 의존 방향을 강제한다. 주기적 "garbage collection"(문서 정원 가꾸기)으로 drift를 치운다. "what Codex cannot see does not exist"라는 표현. Martin Fowler의 LinkedIn 정리: "Harness includes context engineering, architectural constraints, and garbage collection." (InfoQ 인용)
  - "~100줄" 수치는 Viblo 한 곳만 명시 → [미확인].
- 관련 섹션: 원전 02절(원본 책임), 09절(문서 CI: 링크·ID 누락 검사), 14절. 국내 사례 D1~D3의 "하네스" 용어 원류.

### 자료 B8: Anthropic Engineering — Effective context engineering for AI agents
- 출처: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 저자·날짜: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (Anthropic Applied AI), **2025-09-29** — 구버전 정보일 수 있음(원리 위주라 유효성은 높음)
- 신뢰성: 최상
- 핵심 주장: 컨텍스트는 유한한 주의 예산이다. 원하는 결과 확률을 최대화하는 "가장 작은 고신호 토큰 집합"을 찾는 것이 목표다. 필요할 때 불러오기(just-in-time), 압축(compaction), 구조화된 노트, 서브에이전트가 장기 작업 기법이다.
- 인용 가능한 구절:
  > "the smallest possible set of high-signal tokens"
  > "the model’s ability to accurately recall information from that context decreases." (context rot)
  > "have an “attention budget” that they draw on when parsing large volumes of context."
  > "a technique where the agent regularly writes notes persisted to memory outside of the context window."
  > "specialized sub-agents can handle focused tasks with clean context windows."
  > "CLAUDE.md files are naively dropped into context up front"
- 관련 섹션: 원전 10절 "모든 문서를 무조건 넣기보다 필요한 원본과 관련 연결만 포함", 12절(머리말로 원본·연결을 한눈에).

### 자료 B9: Birgitta Böckeler — Context Engineering for Coding Agents (martinfowler.com)
- 출처: https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
- 저자·날짜: Birgitta Böckeler (Thoughtworks), **2026-02-05**
- 신뢰성: 최상 (확인된 저자, 정기 연재)
- 핵심 주장: 코딩 에이전트의 컨텍스트를 지시(instructions)·가이던스(규칙)·컨텍스트 인터페이스·스킬로 나누고, "누가 로드를 결정하는가(LLM/사람/에이전트 소프트웨어)"로 분류한다. 지시를 많이 줘도 실행은 결국 LLM 해석에 달려 있다.
- 인용 가능한 구절:
  > "Context engineering is curating what the model sees so that you get a better result." (Bharani Subramaniam 정의 인용)
  > "Allowing the LLM to decide when to load context is a prerequisite for running agents in an unsupervised way."
  > "A human invocation of context gives us control, but reduces the level of automation overall."
  > "Some context features are triggered by the agent software itself, at deterministic points in time."
  > "Once the agent gets all these instructions and guidance, execution still depends on how well the LLM interprets them!"
  > "build context like rules files up gradually, and not pump too much stuff in there right from the start."
- 관련 섹션: 원전 07절 "AI 검토를 과신하지 않는 법", 11절(문서 양은 위험에 맞춤).

### 자료 B10: Agent Skills 오픈 표준 (agentskills.io)
- 출처: https://agentskills.io/
- 저자·날짜: Anthropic 기원, 오픈 표준. 날짜 표기 없음, 2026-10 기준
- 신뢰성: 최상
- 핵심 주장: 스킬은 `SKILL.md`(이름·설명 메타데이터 + 지시)를 담은 폴더다. 발견(이름·설명만) → 활성화(전체 SKILL.md 로드) → 실행의 점진적 공개(progressive disclosure)로 컨텍스트를 아낀다. Claude Code(`.claude/skills/`), Codex(`.agents/skills/`), Hermes(agentskills.io 호환 명시)가 모두 이 형식을 쓴다.
- 인용 가능한 구절:
  > "Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows."
  > "packaging procedural knowledge and company-, team-, and user-specific context into portable, version-controlled folders that agents load on demand."
  > "The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products."
- 관련 섹션: 원전 02절 `guides/`(같은 일을 일관되게 수행하는 방법) — guides의 절차를 스킬로 승격하는 연결점.

### 자료 B11: GitHub Blog — How to write a great agents.md: Lessons from over 2,500 repositories
- 출처: https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
- 저자·날짜: Matt Nigh, 2025-11-19 (2025-11-25 갱신) — 구버전 정보일 수 있음
- 신뢰성: 최상
- 핵심 주장: 좋은 에이전트 파일은 명령·테스트·구조·코드 스타일·git 워크플로·경계의 6영역을 다루고, 경계를 "항상 / 먼저 묻기 / 절대 금지" 3단으로 둔다.
- 인용 가능한 구절:
  > "Most agent files fail because they’re too vague."
  > "cover the six core areas: Commands, testing, project structure, code style, git workflow, and boundaries."
  > "Three-tier boundaries: Set clear rules using always do, ask first, never do."
  > "One real code snippet showing your style beats three paragraphs describing it."
  > "“Never commit secrets” was the most common helpful constraint."
  > "Start simple. Test it. Add detail when your agent makes mistakes."
- 관련 섹션: 원전 10절 역할별 "금지"·"중단 조건". "Ask first" 층이 원전의 "결정 요청을 남긴다"에 대응.

### 자료 B12: Claude Code 플랜 모드 (공식 문서 검색 결과)
- 출처: https://code.claude.com/docs/en/permission-modes , https://code.claude.com/docs/en/common-workflows
- 저자·날짜: Anthropic, 2026 기준 (검색 엔진 캐시가 약 105일 전이라고 표시 → 세부는 재확인 필요)
- 신뢰성: 최상 (단, 이 항목은 검색 결과 요약 경유)
- 핵심 내용: Shift+Tab으로 모드 순환하거나 프롬프트 앞에 `/plan`, 또는 `claude --permission-mode plan`. 플랜 모드에서 Claude는 파일을 읽고 탐색 명령을 실행하며 계획을 쓰지만 소스를 편집하지 않는다. 계획을 승인하면 플랜 모드를 빠져나가 편집을 시작한다. `.claude/settings.json`의 `defaultMode: plan`으로 기본값 지정 가능. 데스크톱 앱에서는 Shift+Tab 순환이 다르다.
- 관련 섹션: 원전 10절 프롬프트 4 "계획·변경 목록을 먼저 제시", 03절 단계 5.

---

## C. 스펙 주도 개발(SDD) 도구와 비판

### 자료 C1: GitHub Blog — Spec-driven development with AI: Get started with a new open source toolkit
- 출처: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- 저자·날짜: Den Delimarsky (Principal PM), **2025-09-02** — 출시 당시 글, 명령어 표기는 구버전일 수 있음
- 신뢰성: 최상
- 핵심 주장: 코드보다 스펙을 먼저 쓴다. 스펙은 코드가 어떻게 동작해야 하는지에 대한 계약이며 공유된 단일 진실이 된다. Specify → Plan → Tasks → Implement.
- 인용 가능한 구절:
  > "Instead of coding first and writing docs later, in spec-driven development, you start with a (you guessed it) spec."
  > "This is a contract for how your code should behave"
  > "Specs become the shared source of truth."
  > "living, executable artifacts that evolve with the project"
  > "It generates small, reviewable chunks that each solve a specific piece of the puzzle." (Tasks 단계)
- 관련 섹션: 원전 01절 C(변경의 제어 장치), 02절.

### 자료 C2: GitHub Spec Kit 저장소 README (현행)
- 출처: https://github.com/github/spec-kit
- 저자·날짜: GitHub. 저장소 생성 2025-08-21, v1.0.0 2026-08-21, 최신 **v1.2.4 (2026-10-27)**. 스타 약 14.3만 [원문 직접 확인]
- 신뢰성: 최상
- 핵심 내용 (v1.2.x 기준): 최소 흐름은 `/speckit-constitution` → `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`. "Repeat implement and converge until convergence reports `Converged`." 확장으로 버그 수정(`/speckit-bug-assess|fix|test`), 사전 평가(`/speckit-assess-intake|research|define|shape|decide`)가 있다. "Run these skills in your agent's chat, not your terminal, one at a time, reviewing each result before continuing." [원문 직접 확인]
- 버전 주의: 2025년 자료의 명령은 `/speckit.specify`(점), 그 이전은 `/specify` 형태였다. 2026 v1.x README는 하이픈(`/speckit-specify`)과 "skills" 용어를 쓴다. 카카오페이 사례(D4)의 `clarify`·`analyze` 단계는 구버전 흐름이다. 책에서는 "Spec Kit v1.2/2026-10 기준"으로 못 박을 것.
- 관련 섹션: 원전 03절(여섯 번의 작은 합의) — constitution ≈ guides/ADR, specify ≈ spec/, plan ≈ architecture/ADR, tasks ≈ plan/. 원전 07절(Design Ready)과 `/speckit-assess-decide`의 "Stopping with a documented reason is also a [valid outcome]" 대조.

### 자료 C3: Kiro 공식 문서 — Specs / Feature specs / Steering, 그리고 GA 공지
- 출처: https://kiro.dev/docs/specs/ (2026-10-15 갱신) · https://kiro.dev/docs/specs/feature-specs/ (2026-08-04 갱신) · https://kiro.dev/docs/steering/ (2026-10-21 갱신) · https://kiro.dev/blog/general-availability/ (2025-11-17)
- 저자·날짜: AWS Kiro 팀. 프리뷰 2025-07-14 [2차 출처 다수 일치], **GA 2025-11-17** [공식 블로그]
- 신뢰성: 최상
- 핵심 내용:
  - 스펙 = `requirements.md`(또는 `bugfix.md`) + `design.md` + `tasks.md`.
  > "Captures user stories, acceptance criteria, or bug analysis in structured notation" (requirements.md)
  > "Documents technical architecture, sequence diagrams, and implementation considerations" (design.md)
  > "Provides a detailed implementation plan with discrete, trackable tasks" (tasks.md)
  - 요구사항은 **EARS**(Easy Approach to Requirements Syntax): `WHEN [condition/event] THE SYSTEM SHALL [expected behavior]`. 예: "WHEN a user submits a form with invalid data THE SYSTEM SHALL display validation errors next to the relevant fields"
  - Requirements-First(Requirements → Design → Tasks)와 Design-First(Design → Requirements → Tasks) 두 흐름. 후자는 "strict non-functional constraints or existing design documents"가 있는 프로젝트용.
  - Steering: "Steering gives Kiro persistent knowledge about your project through markdown files." 기본 `product.md`·`tech.md`·`structure.md`. 포함 모드 always / fileMatch / manual. "Kiro supports providing steering directives via the AGENTS.md standard."
  - GA: "property-based testing for spec correctness (which measures whether your code actually matches what you specified)" / "The Kiro agent is now available in your terminal."
- 관련 섹션: 원전 06절 Given/When/Then 수용 기준 ↔ EARS 비교, 02절 product-brief ↔ steering `product.md`, 05절 NFR을 측정식으로.
- 주의: 2차 출처 일부는 Kiro GA를 2026-03 또는 2026-05로 적는다 → 공식 블로그 2025-11-17이 맞다.

### 자료 C4: Birgitta Böckeler — Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl
- 출처: https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- 저자·날짜: Birgitta Böckeler, **2025-10-15** — 도구 버전은 구버전(당시 프리뷰/초기) 정보일 수 있음. 분류 틀은 유효
- 신뢰성: 최상
- 핵심 주장: SDD를 spec-first / spec-anchored / spec-as-source 3수준으로 나눈다. 세 도구 모두 실제로는 대부분 spec-first다. 작은 버그에 과한 절차, 마크다운 리뷰 부담, 거짓 통제감, MDD(모델 주도 개발)의 재현 위험을 지적한다.
- 인용 가능한 구절:
  > "A well thought-out spec is written first, and then used in the AI-assisted development workflow for the task at hand." (spec-first)
  > "The spec is kept even after the task is complete, to continue using it for evolution and maintenance." (spec-anchored)
  > "The spec is the main source file over time, and only the spec is edited by the human, the human never touches the code." (spec-as-source)
  > "the workflow was like using a sledgehammer to crack a nut."
  > "To be honest, I'd rather review code than all these markdown files."
  > "repetitive, both with each other, and with the code that already existed."
  > "just because the windows are larger, doesn't mean that AI will properly pick up on everything that's in there."
  > "Ultimately, MDD never took off for business applications"
  > "Are we making something worse in the attempt of making it better?" (Verschlimmbesserung)
- 관련 섹션: 원전 01절 "문서 완성률 100% 대신 다음 구현을 시작해도 되는가", 11절(위험에 맞춘 문서 양), 14절 흔한 실패 "문서 양을 진척으로 판단". 원전의 입장은 spec-anchored에 가깝지만 "테스트 통과가 문서와 다른 동작을 자동 승인하지 않는다"(02절)로 spec-as-source와 선을 긋는다.

### 자료 C5: Thoughtworks Technology Radar — Spec-driven development (Assess)
- 출처: https://www.thoughtworks.com/radar/techniques/spec-driven-development
- 저자·날짜: Thoughtworks, **2025-11-05 (Vol. 33)**, 링 **Assess**. 페이지에 "no longer on the current edition" 표시(2026-10 시점)
- 신뢰성: 최상
- 핵심 주장: SDD는 떠오르는 접근이지만 워크플로가 복잡하고 독단적이며, 리뷰하기 어려운 긴 스펙을 만들고, 대상 사용자가 불분명하다. AI에 손으로 세밀한 규칙을 짜 넣는 방식은 확장되지 않는다는 "쓴 교훈"을 다시 배우는 중일 수 있다.
- 인용 가능한 구절:
  > "Spec-driven development is an emerging approach to AI-assisted coding workflows."
  > "the workflows remain elaborate and opinionated"
  > "some generate lengthy spec files that are hard to review"
  > "We may be relearning a bitter lesson"
  > "handcrafting detailed rules for AI ultimately doesn't scale"
- [미확인] Vol. 34(2026-04) 이후 SDD 링 변화는 확인하지 못했다. Vol. 34의 중심 주제가 "AI 가속 코드 생성으로 인한 인지 부채(cognitive debt)"였다는 2차 보도가 있다.
- 관련 섹션: 원전 11절, 14절.

### 자료 C6: OpenSpec (Fission-AI) README
- 출처: https://github.com/Fission-AI/OpenSpec · https://openspec.dev
- 저자·날짜: Fission-AI, 저장소 생성 2025-08-05, 최신 **v1.15.0 (2026-10-24)**, 스타 약 7.3만 [원문 직접 확인]
- 신뢰성: 최상
- 핵심 내용: 기존 코드베이스(brownfield) 우선. 변경 단위 폴더 `openspec/changes/<name>/`에 `proposal.md`(왜·무엇), `specs/`(요구사항+시나리오), `design.md`, `tasks.md`를 만들고, 적용 후 archive하면서 기준 스펙(`openspec/specs/`)을 갱신하는 **변경 제안(delta) 모델**. 팀용 "Stores"(별도 저장소에 스펙 보관, 베타).
- 인용 가능한 구절 [원문 직접 확인]:
  > "→ fluid not rigid → iterative not waterfall → easy not complex → built for brownfield not just greenfield"
  > "The app SHALL let users switch between light and dark themes, defaulting to the system preference." / "- **WHEN** the user clicks the theme toggle - **THEN** the app switches to dark mode and persists the choice" (스펙 예시: SHALL + WHEN/THEN 시나리오)
  > "Your AI writes these; you review the plan before any code is written."
  > "One source of truth your whole team and every coding agent can read, across every repo."
- 관련 섹션: 원전 08절(결정 변경 시 새 기록 + 계보 보존) ↔ OpenSpec의 change → archive 흐름, 09절 "영향 매트릭스"와 proposal.md 대조.

### 자료 C7: BMAD Method README
- 출처: https://github.com/bmad-code-org/BMAD-METHOD · https://docs.bmad-method.org
- 저자·날짜: BMad Code, 저장소 생성 2025-04-13, 안정판 **v6.12.4 (2026-10-14)**, v7 프리뷰 알파. 스타 약 5.5만 [원문 직접 확인]
- 신뢰성: 최상 (단 자기 소개 문서)
- 핵심 주장: 코딩 어시스턴트는 구현은 잘하지만 말하지 않은 가정을 코드로 굳힌다. 결정을 명시하고 다음 작업의 컨텍스트로 보존하며, 작업 규모에 맞춰 절차를 줄이거나 늘린다(작은 변경은 바로 빌드). 제품·아키텍처·UX·개발·테스트 관점의 전문 에이전트를 쓴다. Claude Code·Codex 플러그인 마켓플레이스로 배포.
- 인용 가능한 구절 [원문 직접 확인]:
  > "Coding assistants are effective at implementation, but they often turn unstated assumptions into code."
  > "decisions stay explicit, context carries forward, and the process sizes itself to the work. Small changes go straight to build. Complex work gets the depth it needs."
  > "**Durable context** — Carry product and technical decisions forward instead of re-explaining them in every chat."
- 관련 섹션: 원전 10절(역할 분리), 11절(위험에 맞춘 양), 04절 "AI가 그럴듯하게 채운 빈칸을 확정하지 않는다".

### 자료 C8: Agent OS / Tessl (보조)
- Agent OS: https://github.com/buildermethods/agent-os — "Agent OS is a system for injecting your codebase standards and writing better specs for spec-driven development." v3.0.0 (2026-01-20) [원문 직접 확인]. 신뢰성: 최상(자기 소개).
- Tessl: https://docs.tessl.io — Böckeler(C4)와 Thoughtworks(C5)가 spec-as-source를 탐색하는 유일한 도구로 소개("takes a more radical approach in which the specification itself becomes the maintained artifact"). Tessl 문서는 "the full framework is currently part of Tessl's closed beta program"이라고 적는다 [검색 스니펫]. 2026 초 레지스트리가 "스킬 패키지 매니저"로 축이 옮겨 갔다는 일본 블로그 주장은 [미확인].
- 관련 섹션: 원전 01절 핵심 원칙(원본 하나)과 spec-as-source의 차이 설명.

### 자료 C9: SDD 비판 — "재발명된 폭포수" 논쟁 (2차 출처 묶음)
- 출처: Scott Logic "Putting Spec Kit Through Its Paces: Radical Idea or Reinvented Waterfall?" (2025-11-26, 원문 미열람, 제목·날짜만 2차 출처 codemyspec.com로 확인) · Conffab "Your Spec Driven Workflow Is Just Waterfall With Extra Steps" (2025-12-09) · GeekNews 정리 https://news.hada.io/topic?id=24400
- 신뢰성: 중 (원문 미확인)
- 핵심 내용 [2차 출처]: Spec Kit으로 만든 간단한 기능 하나가 "파일 8개, 약 1,300줄"이 됐다는 사례, 맥락 인식 부족·과도한 문서화·이중 코드 리뷰·거짓 안정감 지적(GeekNews 정리). 반론으로 "스펙 워크플로는 느린 리뷰·테스트 부재·불명확한 소유권을 보완하지 못하지만 그 약점을 드러낸다"(Wavect).
- 관련 섹션: 원전 01절 "이 흐름은 한 번만 통과하는 폭포수 절차가 아닙니다", 11절 첫 주 예시 "하루가 밀렸다고 게이트를 생략하지 않습니다". 책은 이 논쟁에 "위험 기반 Design Ready(07절)"로 답할 수 있다.

---

## D. 국내 엔지니어링 블로그 (한국어)

### 자료 D1: 토스테크 — Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기
- 출처: https://toss.tech/article/harness-for-team-productivity
- 저자·날짜: 김용성 (토스페이먼츠 Node.js Developer), **2026-02-26**
- 신뢰성: 최상 (회사 엔지니어링 블로그)
- 핵심 주장: 팀의 LLM 활용이 개인기("각자도생")에 머물러 격차가 크다. 결과 차이는 작업 전 컨텍스트 설계 여부다. 팀 규칙(린트·브랜치 전략·테스트 정책)을 Claude Code 플러그인으로 묶어 마켓플레이스로 배포하면 저점을 끌어올린다. 문서가 '기록'에서 '실행'으로 바뀐다.
- 인용 가능한 구절:
  > "현재 많은 개발팀이 LLM을 도입하고 있지만, 냉정하게 들여다보면 그것은 '각자도생'에 가깝습니다."
  > "차이는 단 하나, 작업 전에 컨텍스트를 설계했느냐의 여부입니다."
  > "기존의 린터(Linter)가 단순히 에러를 뱉고 차단했다면, 플러그인은 팀의 규율에 맞게 행동을 교정(Align)해주는 가이드 역할을 수행할 수 있습니다."
  > "달라진 것은 모듈의 내부가 '코드'에서 '프롬프트와 에이전트 로직'으로 바뀌었을 뿐입니다."
  > "문서 관리의 패러다임이 '기록'에서 '실행'으로 바뀌는 셈입니다."
  > "플러그인 코드가 업데이트되면, 팀원들의 에이전트 행동 양식도 즉시 업데이트됩니다."
  - 예시: main 브랜치에서 커밋하려 하면 플러그인 Hook이 감지해 feature 브랜치를 만들도록 유도.
- 관련 섹션: 원전 01절 C, 09절(문서를 통제 지점에 연결), 02절 `guides/`.

### 자료 D2: 우아한형제들 기술블로그 — 하네스 엔지니어링(harness engineering)으로 팀 맞춤형 AI 환경 구축하기
- 출처: https://techblog.woowahan.com/26177/
- 저자·날짜: 이재홍, **2026-04-17**
- 신뢰성: 최상
- 핵심 주장: 하네스 엔지니어링은 AI가 길을 잃지 않게 하는 외부 통제 환경 구축이다. Rules는 프로젝트 특화 컨벤션만 담고 glob 경로로 범위를 한정한다. Skills는 스크립트·CLI를 실행해 데이터를 가공한다(Swagger → 타입·Mock·React Query 훅·테스트, PR 본문). AI가 코드 전체를 탐색하게 두지 말고 스크립트가 필요한 메타데이터만 JSON으로 요약해 넘긴다.
- 인용 가능한 구절:
  > "이는 AI가 길을 잃지 않고 안정적으로 일할 수 있도록 외부 통제 환경을 구축하는 것을 의미합니다."
  > "모든 질문에 정의된 Rules를 무조건 포함하는 것이 아니라, globs에 지정한 경로의 파일들을 작업할 때만 해당 규칙이 활성화됩니다."
  > "React 컴포넌트 작성 방법, TypeScript 기본 문법 등 LLM의 기본 지식은 제외하고, ‘프로젝트 특화 규칙’만 포함시켜"
  > "AI가 직접 전체 코드를 탐색하도록 두는 대신, 스크립트가 먼저 실행되어 코드 생성에 필요한 메타데이터만 JSON 형태로 요약해 AI에게 전달하는 방식입니다."
  > "‘AI가 일할 환경과 맥락을 잘 설계해 두고, 넘겨줄 데이터를 최적화하는 것’이 생산성의 핵심이라고 느꼈습니다."
- 관련 섹션: 원전 05절 계약 체크포인트(API 스키마=OpenAPI가 원본 → 타입 생성), 02절 "API 스키마를 별도 파일로 관리한다면 그 스키마를 계약의 원본으로".

### 자료 D3: 컬리 기술 블로그 — OMS에서 Claude AI를 활용하여 변화된 업무 방식
- 출처: https://helloworld.kurly.com/blog/oms-claude-ai-workflow/
- 저자·날짜: 이준환 (컬리 OMS팀), **2025-12-24** (Claude Code v2.0.72, Opus 4.5 기준 — 구버전 정보일 수 있음)
- 신뢰성: 최상
- 핵심 주장: PM 1명 + 엔지니어 3명이 12개 MSA를 운영하며, 역할별 AI 컨텍스트(CLAUDE.md, ai-context 문서, skills)로 "TPM AI 1 + MSA AI 11"을 운용한다. AI 답변은 신입 개발자 제안처럼 검증한다. 코드 작성 시간은 줄고 설계 논의·리뷰 시간은 늘었다.
- 인용 가능한 구절:
  > "AI 답변을 신입 개발자의 제안이라고 생각하고 검증"
  > "AI가 작성한 코드를 신규 입사 개발자가 작성한 코드라고 가정하고 리뷰"
  > "코드 작성 시간은 줄었지만, 코드 품질과 설계 논의는 오히려 증가"
  > "코드 리뷰 시간이 오히려 더 많아짐"
  > "main 브랜치에 머지되는 순간 개인의 코드는 우리 모두의 코드가 됩니다."
- 관련 섹션: 원전 10절(사람이 최종 소유할 결정), 07절 "AI 검토를 과신하지 않는 법", 서문의 문제 제기.

### 자료 D4: 카카오페이 기술 블로그 — SDD (spec-kit) 에이전트 코딩 실전기
- 출처: https://tech.kakaopay.com/post/ifkakao-agentic-coding/
- 저자·날짜: wayne.cai (카카오페이 AI 플랫폼팀), **2026-03-13** (if(kakao) 발표 기반 추정)
- 신뢰성: 최상
- 핵심 주장: 프로젝트가 고도화될수록 무분별한 코드 생성과 환각이 생겨 Spec Kit 기반 SDD를 도입했다. 마음에 안 들면 코드를 고치지 말고 specify로 돌아가 스펙을 재정의한다. 문서·토큰이 많이 나오고, constitution을 가끔 무시하며, 간단한 개발엔 애매하다. 개발자 역할이 "스펙을 검증하고 테스트를 설계하는 사람"으로 바뀐다.
- 인용 가능한 구절:
  > "에이전틱 코딩은 개발 생산성을 높여주지만 프로젝트가 고도화될수록 무분별한 코드 생성과 환각 문제가 발생하여"
  > "constitution → specify ↔ clarify → plan → tasks → analyze → implement" (당시 Spec Kit 흐름 — 현행 v1.2와 다름, C2 참조)
  > "각 단계에서 마음에 안 드는 부분이 있다면 직접 수정하지 않고 specify 로 돌아가 스펙을 재정의하는 것이 좋습니다."
  > "마지막 단계에서는 AI가 생성한 코드를 검토하고 수정하는 시간이 점점 더 길어졌습니다."
  > "일단 파이프라인을 거치면 개발문서가 굉장히 많이 만들어 집니다 이에 따른 토큰도 많이 소모합니다."
  > "constitution에 있는 말을 가끔 안 들을 때도 있습니다."
  > "간단한 개발은 어떻게 해야 할지 애매합니다."
  > "개발자의 역할은 '코드를 작성하는 사람'에서 '스펙을 검증하고 테스트를 설계하는 사람'으로 점점 변화할 것이라고 생각합니다."
  - 개발 기간 단축은 "크게"라고만 서술, 수치 없음.
- 관련 섹션: 원전 11절(위험에 맞춘 문서 양 — "간단한 개발은 애매"에 대한 답), 08절(구현 중 새 규칙은 승인 경로로 되돌림 ↔ "specify로 돌아가라"), B1(constitution 무시 → 훅으로 강제).

### 자료 D5: LY Corporation 기술 블로그 — ODW #4: 코파일럿에서 파일럿으로, 에이전틱 코딩으로 구현부터 PR까지 자동화
- 출처: https://techblog.lycorp.co.jp/ko/from-copilot-to-pilot-agentic-coding-implementation-to-pr-automation
- 저자·날짜: Hirano Keisuke (LY Corporation, Yahoo! Finance 프런트엔드). 페이지에 날짜 표기 없음, URL 슬러그로 2026-01-29 추정 [미확인]
- 신뢰성: 최상 (한국어판)
- 핵심 주장: Jira·Confluence 명세를 MCP로 연결해 기존 프로세스를 유지한 채 구현 계획을 먼저 세운다. 사람은 스펙 작성과 테스트·리뷰·릴리스의 최종 책임을, AI는 구현 계획·구현·PR 작성·초기 리뷰를 맡는다.
- 인용 가능한 구절:
  > "에이전틱 코딩을 안정적으로 수행하기 위한 핵심은 초기에 구현 계획을 수립해 재작업을 줄이는 것입니다."
  > "테스트/리뷰/릴리스 역시 최종적으로는 사람이 책임지는 한편, 구현 계획 수립/구현/PR 작성/초기 리뷰는 AI에게 맡기는 형태로 구성했습니다."
  > "AI가 작성한 코드를 사람이 책임을 진다는 인식이 반드시 필요합니다."
  > "저품질 코드는 리뷰어의 부담을 증가시키고 프로덕트의 기술 부채로 이어질 수 있습니다."
- 보조: 같은 블로그 "Claude Code Action: 조직 전반의 코드 품질을 지키는 AI 코드 리뷰 플랫폼화" https://techblog.lycorp.co.jp/ko/building-ai-code-review-platform-with-claude-code-action — 리뷰 프롬프트를 중앙 관리하고 호출 수·성공 여부를 DORA 대시보드로 추적 [검색 요약].
- 관련 섹션: 원전 10절(역할과 결정 한계 — 이 사례의 분업표가 원전 역할표의 실사례), 09절.

### 자료 D6: 기타 국내 자료 (인덱스, 본문 미확인)
- 카카오테크 "Beyond Vibe Coding to Agentic Coding: 카카오의 AI 협업 개발 실험" https://tech.kakao.com/posts/711 (저자 benedict.lee, 본문 미추출)
- 카카오테크 "생산성 혁신의 실험: AI 마일리지 프로그램" https://tech.kakao.com/posts/762
- 우아한형제들 "배달의민족 전자계약서 화면 개편기"(2026-09-15, 홍영민) — "AI가 적게 읽어도 되도록 구조를 먼저 설계" [검색 요약, 미확인]
- 달레(Dale Seo) "스펙 주도 개발: 바이브 코딩을 넘어 AI 에이전트와 일하는 법" https://daleseo.com/spec-driven-development/ (개인 블로그, 미열람)
- 당근·네이버 D2의 AI 코딩 에이전트 도입 글은 이번 검색에서 찾지 못했다.

---

## E. 실무자 에세이 (계획·스펙·검증 습관)

### 자료 E1: Harper Reed — My LLM codegen workflow atm
- 출처: https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/
- 저자·날짜: Harper Reed, **2025-02-16** — 모델명이 구버전(ChatGPT 4o/o3, o1, r1)
- 신뢰성: 최상 (확인된 저자 블로그)
- 핵심 주장: 아이디어 다듬기(대화형 LLM이 한 번에 하나씩 질문) → `spec.md` → 추론 모델로 계획(`prompt_plan.md`, `todo.md`) → 실행. 실행 성패는 계획 단계가 좌우한다.
- 인용 가능한 구절:
  > "Ask me one question at a time so we can develop a thorough, step-by-step spec for this idea."
  > "I like to save it as `spec.md` in the repo."
  > "There are so many options available for execution. The success really depends on how well step 2 went."
  > "This entire process will take maybe 15 minutes."
  > "This is working well NOW, it will probably not work in 2 weeks, or it will work twice as well."
- 관련 섹션: 원전 14절 "30분 빠른 시작", 10절 프롬프트 1(아이디어를 설계 질문으로). B1의 "Interview me until you could write the spec"이 이 패턴의 공식화.

### 자료 E2: Kent Beck — Augmented Coding: Beyond the Vibes
- 출처: https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes (구 tidyfirst.substack.com에서 301)
- 저자·날짜: Kent Beck, **2025-06-25**
- 신뢰성: 최상
- 핵심 주장: 바이브 코딩은 코드가 아닌 동작만 신경 쓴다. 증강 코딩은 코드·복잡도·테스트·커버리지를 신경 쓴다. `plan.md`의 다음 테스트 하나씩 TDD로 진행한다. 에이전트 이탈 신호 3가지.
- 인용 가능한 구절:
  > "In vibe coding you don't care about the code, just the behavior of the system."
  > "In augmented coding you care about the code, its complexity, the tests, & their coverage."
  > "Always follow the instructions in plan.md." (시스템 프롬프트 첫 줄)
  > 경고 신호: "Loops." / "Functionality I hadn't asked for (even if it was a reasonable next step)." / "Any indication that the genie was cheating, for example by disabling or deleting tests."
- 관련 섹션: 원전 10절 프롬프트 4 "금지: 범위 밖 리팩터링, 테스트 삭제로 통과 만들기, 미실행 검증 주장" — Beck의 세 신호와 거의 같다.

### 자료 E3: Simon Willison — Vibe engineering
- 출처: https://simonwillison.net/2025/Oct/7/vibe-engineering/
- 저자·날짜: Simon Willison, **2025-10-07** (2026-02 추기: "Agentic Engineering"이 더 널리 쓰이는 용어가 됨)
- 신뢰성: 최상
- 핵심 주장: 숙련 개발자가 LLM으로 작업을 가속하되 결과에 책임지는 방식. 자동화 테스트, 사전 계획, 포괄적 문서, 버전 관리 습관, 자동화, 리뷰 문화, 수동 QA, 리서치, 프리뷰 환경 등 기존 공학 관행이 그대로 증폭기가 된다.
- 인용 가능한 구절:
  > "seasoned professionals accelerate their work with LLMs"
  > "Sitting down to hack something together goes much better if you start with a high level plan."
  > "Write good documentation first and the model may be able to build the matching implementation from that input alone."
  > "lets it use APIs from other areas without reading the code first." (문서의 효용)
- 보조 [2차 출처]: Willison은 2025-09 "designing agentic loops", 2026-02-23 "Agentic Engineering Patterns" 연재를 시작했다(원문 미열람).
- 관련 섹션: 원전 01절, 09절(코드 CI·출시 게이트).

### 자료 E4: Addy Osmani — How to write a good spec for AI agents
- 출처: https://addyosmani.com/blog/good-spec/ (O'Reilly Radar 재게재 https://oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents)
- 저자·날짜: Addy Osmani, **2026-01-13**
- 신뢰성: 최상
- 핵심 주장: 읽기 전용 모드로 먼저 계획한 뒤 실행·반복한다. 스펙은 PRD처럼 구조화하고(명령·테스트·구조·스타일·git·경계 6영역, B11 인용), 경계는 Always / Ask first / Never 3단. 한 번에 한 작업. 자가 점검을 스펙에 넣는다. 스펙은 살아 있는 문서.
- 인용 가능한 구절:
  > "Plan first in read-only mode, then execute and iterate continuously."
  > "Kick off your project with a concise high-level spec, then have the AI expand it into a detailed plan."
  > "Treat your AI spec as a structured document (PRD) with clear sections, not a loose pile of notes."
  > "too many directives causing it to follow none of them well." ("curse of instructions")
  > "small, focused context beats one giant prompt."
  > "After implementing, compare the result with the spec and confirm all requirements are met."
  > "Don’t write it and forget it."
- 관련 섹션: 원전 04절(짧은 제품 합의서), 10절 공통 입력 꾸러미, 12절.

### 자료 E5: Anthropic — How Anthropic teams use Claude Code
- 출처: https://claude.com/blog/how-anthropic-teams-use-claude-code (PDF: https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf , 한국어판 https://claude.com/ko/resources/articles/how-anthropic-teams-use-claude-code)
- 저자·날짜: Anthropic, **2025-07-24** — 구버전 정보일 수 있음
- 신뢰성: 최상
- 핵심 내용: 인프라팀은 CLAUDE.md로 파이프라인 의존성을 파악하고, 보안팀은 의사코드 → TDD → 주기적 점검, 제품 디자인팀은 설계 단계에서 오류 상태·로직 흐름·시스템 상태를 매핑해 엣지 케이스를 찾는다.
- 인용 가능한 구절:
  > "asking Claude for pseudocode, guiding it through test-driven development, and checking in periodically" (Security Engineering)
  > "mapping out error states, logic flows, and system statuses to identify edge cases during design" (Product Design)
  > "set up autonomous loops where Claude Code writes the code for the new feature, runs tests, and iterates continuously" (Product Design)
- [2차 출처, 미확인] "Inference 팀 R&D 시간 80% 단축", "Vim 모드 코드 70%를 Claude가 작성" 수치는 PDF 원문 대조 필요.
- 관련 섹션: 원전 05절 "화면보다 먼저 상태와 경계" — 제품 디자인팀 사례가 직접 근거.

### 자료 E6: Anthropic — 2026 Agentic Coding Trends Report
- 출처: https://resources.anthropic.com/2026-agentic-coding-trends-report (PDF https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)
- 저자·날짜: Anthropic, 2026-01-21 [2차 출처 @IT 기준, 일부 출처는 4월로 표기 → 미확인]
- 신뢰성: 중 (본문 미열람)
- 핵심 내용 [2차 출처]: 개별 AI 보조 → 협업하는 에이전트 팀으로의 이동 등 8개 트렌드. "60% of work" 등 수치는 원문 미확인.
- 관련 섹션: 서문 배경 (본문에 수치 인용 시 PDF 대조 필수).

---

## F. 설계·문서화 고전과 예제 뒷받침 (ADR · 설계 문서 · 계약 · 멱등성 · 아웃박스)

### 자료 F1: Michael Nygard — Documenting Architecture Decisions
- 출처: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- 저자·날짜: Michael Nygard, **2011-11-15** (고전)
- 신뢰성: 최상
- 핵심 주장: 아키텍처적으로 중요한 결정만 ADR로 남긴다. Title·Context·Decision·Status·Consequences. 뒤집힌 결정도 지우지 않고 superseded로 표시한다. 저장소 안에 순번으로 둔다.
- 인용 가능한 구절:
  > "those that affect the structure, non-functional characteristics, dependencies, interfaces, or construction techniques."
  > "One ADR describes one significant decision for a specific project."
  > "We will keep ADRs in the project repository under doc/arch/adr-NNN.md"
  > "ADRs will be numbered sequentially and monotonically. Numbers will not be reused."
  - 상태: proposed / accepted / deprecated / superseded("mark it as superseded")
- 관련 섹션: 원전 08절(Draft → Accepted → Superseded, "Accepted ADR의 결론을 조용히 덮어쓰지 않습니다").

### 자료 F2: MADR — Markdown Architectural Decision Records
- 출처: https://adr.github.io/madr/
- 저자·날짜: ADR GitHub 조직, **MADR 4.0.0 (2024-09-17)** 기준
- 신뢰성: 최상
- 핵심 내용: 필수 섹션 "Context and Problem Statement", "Considered Options", "Decision Outcome". 선택 "Decision Drivers", "Consequences", "Confirmation", "Pros and Cons of the Options", "More Information". 상태는 front matter: `status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123"`.
- 책 활용: MADR의 "Confirmation"(결정 준수를 어떻게 확인할지)은 원전 08절 "결정, 근거, 부작용, 검증 증거를 남깁니다"와 연결. front matter 상태 필드는 원전 12절 공통 머리말과 결합 가능.
- 관련 섹션: 원전 08절, 12절.

### 자료 F3: Malte Ubl — Design Docs at Google
- 출처: https://www.industrialempathy.com/posts/design-docs-at-google/
- 저자·날짜: Malte Ubl, **2020-07-06**
- 신뢰성: 최상 (확인된 저자, 전 Google)
- 인용 가능한 구절:
  > "The design doc documents the high level implementation strategy and key design decisions"
  > "things that could reasonably be goals, but are explicitly chosen not to be goals." (non-goals)
  > "This section lists alternative designs that would have reasonably achieved similar outcomes."
  > "write down the trade-offs you made in designing your software."
  > "At the center of that decision lies whether the solution to the design problem is ambiguous" (설계 문서를 쓸지 판단 기준)
  > "A clear indicator that a doc might not be necessary are design docs that are really implementation manuals."
  > "If the designed system hasn't shipped yet, then definitely update the doc."
- 관련 섹션: 원전 04절 "비범위", 08절 "실제로 고려한 대안과 비용", 11절(문서가 필요 없는 경우).

### 자료 F4: Gergely Orosz — Companies Using RFCs or Design Docs and Examples of These
- 출처: https://blog.pragmaticengineer.com/rfcs-and-design-docs/
- 저자·날짜: Gergely Orosz, 2022-06-21 (2024-02-07 갱신)
- 신뢰성: 최상
- 핵심 내용: RFC·설계 문서는 가정을 명확히 하고 계획을 일찍 회람해 더 빨리 만들게 한다. Uber의 RFC 프로세스는 "used up to around 2019"이고 서비스 RFC는 "List of approvers"로 시작했다. Google·Uber·HashiCorp·Monzo·Airbnb·Amazon·Spotify 등 사례.
- 인용 가능한 구절:
  > "clarifying assumptions and circulating plans earlier."
  > "Writing a doc is not a perfunctory gesture." (Stedi 내부 메모 인용)
- 관련 섹션: 원전 03절 각 단계의 "검토자", 09절 설계 PR.

### 자료 F5: Martin Fowler — GivenWhenThen (bliki)
- 출처: https://martinfowler.com/bliki/GivenWhenThen.html
- 저자·날짜: Martin Fowler, **2013-08-21**
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Given-When-Then is a style of representing tests - or as its advocates would say - specifying a system's behavior"
  > "It's an approach developed by Daniel Terhorst-North and Chris Matts as part of Behavior-Driven Development (BDD)."
  > "The given part describes the state of the world before you begin the behavior you're specifying in this scenario."
  > "His four phases are Setup (Given), Exercise (When), Verify (Then) and Teardown." (Meszaros Four-Phase Test 대응)
- 관련 섹션: 원전 06절 AC-CAN-01~05, 12절 수용 기준 템플릿. EARS(C3)·OpenSpec WHEN/THEN(C6)과 비교표.

### 자료 F6: Stripe — Designing robust and predictable APIs with idempotency / Idempotent requests 문서
- 출처: https://stripe.com/blog/idempotency (Brandur Leach, **2017-02-22**) · https://docs.stripe.com/api/idempotent_requests (2026-10 기준)
- 신뢰성: 최상
- 핵심 주장: 네트워크는 신뢰할 수 없고, 실패한 요청은 클라이언트를 불확실한 상태에 둔다. 클라이언트가 만든 고유 키로 재시도를 안전하게 한다. 지수 백오프 + 지터.
- 인용 가능한 구절 (블로그):
  > "Networks are unreliable."
  > "Any one of these leaves the client that made the request in an uncertain situation."
  > "a client generates a unique ID to identify just that operation"
  > "Furthermore, it's also a good idea to mix in an element of randomness."
- 인용 가능한 구절 (API 문서, 2026-10 기준):
  > "For API v1, Stripe saves the status code and body of the first request made with a given idempotency key after endpoint execution begins. Retries with the same key return the saved response, including `500` errors."
  > "Idempotency keys are up to 255 characters long. Avoid using sensitive data (for example, email addresses or personal identifiers) as idempotency keys."
  > "For API v1, you can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned."
  > "The idempotency layer compares incoming parameters to those of the original request and errors if they’re not the same to prevent accidental misuse."
  > "If incoming parameters fail validation, or the request conflicts with another request that’s executing concurrently, we don’t save the idempotent result"
  - API v2는 "retries don’t repeat successful operations"로 동작이 다르다.
- 관련 섹션: 원전 06절 API-CAN-01("재전송 → 기존 requestId", "동일 키+다른 입력 → 409"), 06절 주의문 "멱등키 보존 기간 ... 반드시 결정해야 합니다. 키 기록 정리 후에도 예약·시도 이력과 업무 제약이 중복 환불을 방어해야 합니다." — Stripe의 "24시간 후 정리, 정리된 키를 재사용하면 새 요청"이 바로 이 경고의 실례다.

### 자료 F7: IETF draft — The Idempotency-Key HTTP Header Field
- 출처: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (본문 확인은 -07: https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html)
- 저자·날짜: J. Jena, S. Dalal (httpapi WG). -07은 2025-10-15. **최신 -08은 2026-10-22**, Active Internet-Draft, RFC 미발행 (2026-10-28 조회)
- 신뢰성: 최상 (단 초안 단계)
- 핵심 내용 (-07 기준): 키 누락 → 400, 같은 키로 원 요청 처리 중 재시도 → 409, 같은 키를 다른 페이로드로 재사용 → **422**. 선택적 "idempotency fingerprint".
  > "The HTTP Idempotency-Key request header field can be used to make non-idempotent HTTP methods" (POST, PATCH 등을 장애 허용으로)
  > "If there is an attempt to reuse an idempotency key with a different request payload, the resource SHOULD reply with a HTTP `422` status code." (요지; 원문 문장은 재대조 필요)
- 책 활용: 원전 06절 API-CAN-01은 "동일 키 + 다른 입력 → 409 IDEMPOTENCY_CONFLICT"를 택했다. 원전도 "HTTP 상태 코드는 이 예제의 선택입니다"라고 명시하므로, IETF 초안(422)·Stripe(오류)와의 차이를 ADR 사례로 쓸 수 있다. -08에서 상태 코드가 바뀌었는지는 미확인.
- 관련 섹션: 원전 06절, 08절(ADR 예).

### 자료 F8: Chris Richardson — Pattern: Transactional outbox (microservices.io)
- 출처: https://microservices.io/patterns/data/transactional-outbox.html
- 저자·날짜: Chris Richardson, 날짜 표기 없음 (고전 패턴 문서)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "How to atomically update the database and send messages to a message broker?"
  > "store the message in the database as part of the transaction that updates the business entities"
  > "A separate process then sends the messages to the message broker."
  > "The Message relay might publish a message more than once."
  > "As a result, a message consumer must be idempotent"
- 관련 섹션: 원전 06절 EVT-CAN-01 "outbox는 '정확히 한 번'을 보장하지 않으므로 수신자 중복 처리도 필요합니다" — 1:1 근거.

### 자료 F9: Pact 문서 — 계약 테스트
- 출처: https://docs.pact.io/
- 저자·날짜: Pact Foundation, 2026-10 기준
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Pact is a code-first tool for testing HTTP and message integrations using `contract tests`."
  > "Contract testing is a technique for testing an integration point by checking each application in isolation"
  - 소비자 테스트 실행 중 계약이 생성되며("is generated during the execution of the automated consumer tests"), 소비자가 실제 쓰는 부분만 검증한다.
- 관련 섹션: 원전 05절 계약 체크포인트, 06절 SLICE-CAN-01 "계약·실패 가짜 서버 작성", 09절 영향 매트릭스 "소비자 테스트".

### 자료 F10: OpenAPI Specification 3.2.0
- 출처: https://spec.openapis.org/oas/v3.2
- 저자·날짜: OpenAPI Initiative, **3.2.0 = 2025-09-19** 발표 (같은 날 3.1.2 패치) [Wikipedia·Speakeasy 교차 확인, 공식 릴리스 노트 미열람]
- 신뢰성: 최상(스펙) / 날짜는 2차 교차 확인
- 보조: Swagger 오픈소스 도구의 3.2.0 일반 지원은 2026-04 [2차 출처]. 3.3/4.0 일정 미정.
- 관련 섹션: 원전 02절 "API 스키마를 OpenAPI 등 별도 파일로 관리한다면 그 스키마를 계약의 원본으로", 12절 `references: [architecture/contracts/cancellation.yaml]`.

---

## G. 업계 설문·수치 (원문 1차 우선)

### 자료 G1: Stack Overflow Developer Survey 2025 — AI
- 출처: https://survey.stackoverflow.co/2025/ai
- 날짜·표본: 2025-07-29 발표, 49,000명+ / 177개국 [2차 출처로 표본 확인]
- 신뢰성: 최상 — 2025 기준, 2026 조사(G2)로 대체된 수치
- 수치 (원문 문장):
  > "84% of respondents are using or planning to use AI tools in their development process."
  > "This year we can see 51% of professional developers use AI tools daily." (차트 50.6%)
  > "More developers actively distrust the accuracy of AI tools (46%) than trust it (33%)."
  > "AI agents are not yet mainstream." (에이전트 업무 사용: 매일 14.1%, 매주 9%, 월간·간헐 7.8%; 52%는 에이전트를 안 쓰거나 자동완성만)
  > "The biggest single frustration, cited by 66% of developers" ("거의 맞지만 완전히 맞지는 않은" 답)
  > "Most respondents are not vibe coding (72%)."
- 관련 섹션: 서문(2025→2026 변화의 출발점).

### 자료 G2: Stack Overflow Developer Survey 2026 — 결과 발표 블로그 + AI 페이지
- 출처: https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/ (Ryan Donovan, **2026-10-06**) · https://survey.stackoverflow.co/2026/ai
- 표본: "more than 30,000 people took the survey" (2026 조사는 "human developers only"로 진행, 2026-06-23 개시 공지)
- 신뢰성: 최상
- 수치 (원문 문장, 2026 기준):
  > "73% of respondents who indicate using AI coding assistants/agents use them daily."
  > "Coding assistants and agents have pulled ahead as the dominant use case for AI (66%)." (챗봇 63%)
  > "The agents of choice are Claude Code (66%) and GitHub Copilot (59%)."
  > "When they develop with AI, it's primarily generating code in familiar areas (67%) and debugging (61%)," 프로덕션 배포·운영·장애 대응은 20%
  > "to trust what the AI gives requires source attribution (93%)."
  > "62% of all respondents view AI at least somewhat positively, while that jumps to 71% for daily users."
  > "But developers care more about quality (75%) over cost (38%) when it comes to shaping prompts and picking models."
  - AI 페이지: 매일 사용자 중 하루 4시간+ 30.9%(n=10,926). 신뢰 문항 — "when they can easily validate the answers" 48%, 중요 업무 결정이 아닌 대부분 작업 16%. 상위 작업(n=12,547): 익숙한 영역 코드 생성 69.3%, 디버깅·리팩터링 63.8%, 테스트 작성·개선 58.1%, 낯선 영역 코드 생성 56.0%.
  - 2026-04 펄스 조사(같은 블로그 계열 보도): 에이전트 사용 59%로 거의 2배, Claude Code 41% → 55% [2차 출처 요약, 원문 재대조 필요].
- [미확인/주의] Codex 30%·Cursor 26%·Google Antigravity 16% 수치는 달레 블로그(2026-10-11, https://daleseo.com/stack-overflow-survey-2026/)에만 있고 공식 블로그·AI 페이지 추출본에는 없었다. "신뢰 31% → 87%"도 같은 블로그가 "질문 보기 변경으로 조건부 응답이 신뢰로 집계"되었다고 경고했다:
  > "Stack Overflow는 어느 정도라도 AI를 신뢰하는 비율이 작년 31%에서 올해 87%로 크게 늘었다고 소개하는데, 이 숫자는 조심해서 읽을 필요가 있습니다." (달레)
  > 저자 해석: "신뢰가 늘었다"보다 "검증을 전제로 쓰는 방식이 자리 잡았다"가 정확하다. 중요한 업무 결정까지 맡긴다는 응답 "6.6%에 불과" (달레)
- 관련 섹션: 서문, 07절 "AI 검토를 과신하지 않는 법"(신뢰 = 검증 가능성 전제), 독자 도구 스택 정당화(Claude Code 66%).

### 자료 G3: DORA — 2025 State of AI-assisted Software Development
- 출처: https://blog.google/technology/developers/dora-report-2025/ (Ryan J. Salva, **2025-09-23**) · 보고서 https://cloud.google.com/devops/state-of-devops · AI Capabilities Model https://dora.dev/ai/capabilities-model/report (2025-11-25 갱신)
- 표본: "nearly 5,000 technology professionals"
- 신뢰성: 최상 — 2025 기준(DORA 2026 연례 AI 보고서는 검색 시점에 확인 못함; 2026-04 "ROI of AI-assisted Software Development" v2026.1은 별도 존재)
- 수치 (Google 블로그 원문 기준):
  - AI 채택 "surged to 90%", 전년 대비 14%(포인트로 해석) 증가
  - 중앙값 하루 2시간 AI 사용
  - 80%+가 생산성 향상 인식, 59%가 코드 품질에 긍정적 영향
  - 30%는 AI를 "a little"(23%) 또는 "not at all"(7%) 신뢰
  - AI는 "mirror and a multiplier" — 응집된 조직에선 효율을 키우고, 파편화된 조직에선 약점을 드러낸다
- 보조 [2차 출처]: 2025 보고서는 2024와 달리 AI 채택이 처리량(throughput) 향상과 연결됐지만 불안정성(instability)도 함께 증가. 보고서 자체는 백분율이 아닌 표준화 효과 크기를 쓴다.
- AI Capabilities Model 7개 역량: 이름 전체를 1차로 확인하지 못함. 2차로 확인된 항목 — "clear and communicated AI stance", "healthy data ecosystems", "AI-accessible internal data", "strong version control practices", "working in small batches", "user-centric focus", "quality internal platforms" [미확인: 정확한 명칭은 보고서 대조 필요].
- 관련 섹션: 원전 06절·11절(작은 수직 기능 = small batches), 09절(버전 관리·롤백), 02절(AI가 접근 가능한 내부 데이터 = 권위 있는 원본).

### 자료 G4: JetBrains — State of Developer Ecosystem 2025 / 2026 AI 코딩 에이전트 조사
- 출처: 2025 보고서 https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/ (2025-10-15) · 2026 에이전트 조사 https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/ (403, 미열람) · 보도 i-programmer, Janet Swift, 2026-09-02 https://www.i-programmer.info/news/99-professional/19118-jetbrains-reveals-widespread-adoption-of-ai-coding-agents-.html
- 신뢰성: 중 (JetBrains 원문 403 → 언론 경유)
- 수치 (2026 기준, i-programmer 보도):
  - 표본 "more than 15,000 developers worldwide", 조사 기간 2026-04~05 (다른 보도는 5~7월로 적어 엇갈림 [미확인])
  - 전문 개발자의 90%가 업무에서 AI 코딩 에이전트를 최소 주 1회, 68%가 매일 사용 ("early results")
  - 업무 사용 에이전트: Claude Code 39%(2025 조사 3%에서), GitHub Copilot 21%(29%에서), **Codex 16%(0%에서)**, Cursor 12%, JetBrains AI Assistant·Junie 9%(13%에서). 미국은 Claude Code 47%
  - 인지도: Copilot·Claude Code 79%, Cursor 75%, Codex 65%(11%에서)
- 2025 수치 [2차 출처]: "85% of developers use AI regularly"(InfoWorld 보도) — JetBrains 원문에서 미확인. 2026-01 기준 "74%가 개발자 전용 AI 도구 채택"(JetBrains 리서치 글, 검색 스니펫).
- 관련 섹션: 서문(독자 도구 스택이 업계 주류임을 보이는 근거 — Claude Code·Codex 급성장).

### 자료 G5: GitHub Octoverse 2025
- 출처: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-TypeScript-to-1/
- 저자·날짜: GitHub Staff, **2025-10-28** (2026-02-28 갱신). 집계 기간 2024-09-01~2025-08-31 [2차 출처]
- 신뢰성: 최상 — Octoverse 2026은 2026-10-28 검색 시점에 미발행으로 보임
- 수치 (원문 문장):
  > "180 million-plus developers now work and build on GitHub"
  > "Every second, more than one new developer on average joined GitHub—over 36 million in the past year."
  > "80% of new developers on GitHub use Copilot in their first week."
  > "A first glimpse of coding agent shows 1+ million pull requests that were created between May 2025 and September 2025."
  > "518.7M pull requests merged (+29% YoY)" / "merged 43.2 million pull requests on average each month (+23% YoY)"
  > "72.6% of developers who use Copilot code review said it improved their effectiveness."
  - TypeScript가 2025-08 월간 기여자 기준 1위 [2차 출처 다수 일치]
  - 커밋 수는 본문에 "nearly 1 billion"과 "more than 986M" 두 표현이 섞여 있음
- 관련 섹션: 서문, 09절(에이전트가 만든 PR이 대량으로 들어오는 현실 → 통제 지점 필요).

---

## 원전 가이드 절별 매핑 (research-lead·planner용 요약)

| 원전 절 | 뒷받침 자료 |
|---|---|
| 01 문서의 세 가지 일 | B1(결정적/비결정적), C1(스펙=계약), D1(기록→실행), E3 |
| 02 원본 하나 | B2(AGENTS/CLAUDE 읽기 규칙), B3, B4(32 KiB), B7(목차형 AGENTS.md), C6(single source of truth), D2, F10 |
| 03 여섯 번의 작은 합의 | C2(Spec Kit 단계), C3(Kiro 3파일), C7(BMAD 규모 조절), E1, F4 |
| 04 짧은 제품 합의서 | B1(SPEC.md 인터뷰), C3(steering product.md), E4, F3(non-goals) |
| 05 상태와 경계 먼저 | E5(제품 디자인팀 오류 상태 매핑), F6, F8, F9 |
| 06 취소 기능 끝까지 | F5(GWT), C3(EARS), C6(WHEN/THEN), F6·F7(멱등키·상태 코드 선택), F8(outbox), F9(계약 테스트) |
| 07 Design Ready | C2(`/speckit-assess-decide`), C4·C5·C9(과잉 명세 비판), B9("illusion of control"), G2(검증 전제 신뢰) |
| 08 ADR·승격 | F1, F2, F3, B6(Decision Log), C6(change→archive) |
| 09 통제 지점 | B1(훅·Stop hook·증거 요구), B7(린터·구조 테스트·GC), D1(플러그인 훅), D5(분업), G5 |
| 10 AI 역할과 결정 한계 | A1(Hermes 위임), A2(dots Custom Rules), B5(4요소 프롬프트), B11(Always/Ask/Never), E2(이탈 신호), D3·D5 |
| 11 위험에 맞춘 양 | C4·C5·C9, C7, D4("간단한 개발은 애매"), B9 |
| 12 메타데이터 | F2(MADR front matter), B10(SKILL.md 메타데이터), B2 |
| 13 착수 전 체크리스트 | B1, B6(self-contained), E4(self-check) |
| 14 최소 유효 기준선 | E1(15분), B1("Keep CLAUDE.md short"), B9("build context gradually") |

---

## 수집 한계

- **수집 건수:** 본 항목 52건(A3·B12·C8·C9·D6의 묶음 항목 포함 시 60건 이상 URL). 도구 버전 7종 1차 조회.
- **접근 실패(403/차단):** OpenAI 계열 다수 — `openai.com/index/harness-engineering/`, `openai.com/index/how-we-build-safety-security-and-privacy-into-dots/`, `help.openai.com/...getting-started-with-your-dot`. JetBrains 블로그 2026 글 2건, adtmag, betanews 403. web.archive.org는 이 환경에서 접근 불가. → harness engineering·dots는 검색 스니펫과 언론 보도로 교차 확인했고, 해당 인용에 [원문 재대조 필요]·[2차 출처]를 붙였다.
- **식별 결론:** Hermes = Nous Research Hermes Agent (1차 확인, v0.22.5/2026-10-23). OpenAI Dots = OpenAI "dots", DevDay 2026(2026-09-29) 발표 ChatGPT 상시 에이전트 (실재 확인, 단 1차 문서 본문은 열람 실패 → 기능 서술은 TechCrunch·DataCamp 교차 범위로 제한).
- **미확인으로 남긴 수치:** Stack Overflow 2026의 Codex 30%·Cursor 26%(달레 블로그 단독), JetBrains 2026 조사 기간(4~5월 vs 5~7월), DORA AI Capabilities Model 7개 정확한 명칭, harness engineering의 "AGENTS.md ~100줄", Anthropic 팀 사례의 80%·70% 수치, Thoughtworks Radar Vol.34 이후 SDD 링, IETF 멱등키 초안 -08의 상태 코드 변경 여부.
- **다양성 규칙 예외:** martinfowler.com 3건(Böckeler 2건 + GivenWhenThen), github.blog 3건, code.claude.com 2건+. 의뢰서가 이 출처들을 명시 요청했고 각각 다른 주제라 유지했다.
- **언어 비율:** 한국어 1차 자료 약 6건(토스·우아한형제들·컬리·카카오페이·LY Corp·달레). 목표(60~70%)에 못 미친다. 이 주제의 1차 소스(공식 문서·스펙·설문)가 영어라 불가피했다. 당근·네이버 D2·카카오테크(본문) 사례는 찾지 못했거나 본문을 추출하지 못했다.
- **의도적 제외:** 학술 논문(EARS 원 논문 Mavin et al. 2009, METR 생산성 연구, arXiv의 SDD·컨텍스트 엔지니어링 논문)은 paper-researcher 몫. HN·Reddit·GeekNews 댓글 토론은 community-researcher 몫. SEO성 나열 블로그(도구 비교 "Top 7" 류)는 제외했다.
