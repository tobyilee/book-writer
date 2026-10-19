# 웹 리서치: AI-native SDLC playbook — 코스가 참조만 하고 설명하지 않는 것들

- 검색 시점: 2026-10-19 (모든 "확인일"은 이 날짜)
- 범위: 코스 1차 자료(`research/primary/`)는 재수집하지 않음. 이 파일은 코스가 **가리키기만 하는** 공식 사양·근거·비교 대상을 채운다.
- 기준 버전: Claude Code **v2.1.303 (2026-10-18)** — 체인지로그 최상단 항목. 코스 본문의 예시는 `requiredMinimumVersion: "2.1.193"`을 쓰므로, 코스 집필 시점(2026-08-21 claude.com 미러)과 현행 문서 사이의 차이는 각 자료의 "코스와의 차이" 줄에 적었다.
- 신뢰성 등급: 최상 = 공식 문서·릴리스 노트·1차 연구 기관·회사 엔지니어링 블로그 / 중 = 2차 보도·커뮤니티 정리·개인 블로그 / 하 = 출처 불명.
- 2025년 이전 자료에는 "구버전 정보일 수 있음"을 붙였다.

---

## A. Claude Code 공식 문서 (code.claude.com/docs) — v2.1.303/2026 기준

### 자료 1: Hooks reference (훅 이벤트·exit code·JSON 결정 포맷·matcher)
- 출처: https://code.claude.com/docs/en/hooks
- 저자·날짜: Anthropic 공식 문서. 페이지에 "last updated" 없음. 문서 내 버전 표기: `onFailure`는 v2.1.295+, `if` 경로 매칭 변경 v2.1.214, command 플러그인 소스 v2.1.229+. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 훅 이벤트는 코스가 쓰는 PreToolUse/PostToolUse 외에 30종 이상. exit code 2가 "차단"이지만 PostToolUse에서는 차단 효과 없음(이미 실행됨, stderr만 Claude에게 보임). JSON 출력이 더 세밀한 제어. PreToolUse `permissionDecision`은 allow/deny/**ask**/defer 4값. 훅 타입은 command/http/mcp_tool/prompt/agent 5종.
- 인용 가능한 구절:
  > 이벤트 표(발췌, "When it fires" 원문): `SessionStart` "When a session begins or resumes" · `UserPromptSubmit` "When a prompt is submitted, before Claude processes it" · `PreToolUse` "Before a tool call executes. Can block it" · `PermissionRequest` "When a tool call needs a permission decision" · `PostToolUse` "After a tool call succeeds" · `PostToolUseFailure` "After a tool call fails" · `SubagentStart` "When a subagent is spawned" · `SubagentStop` "When a subagent finishes" · `Stop` "When Claude finishes responding" · `InstructionsLoaded` "When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context" · `ConfigChange` "When a configuration file changes during a session" · `WorktreeCreate` "When a worktree is being created" · `PreCompact` "Before context compaction" · `SessionEnd` "When a session terminates"
  > "Exit 0 means success, and is the intended exit code when you print JSON for structured control."
  > "Exit with code 2 to block the action." — 단, 효과는 이벤트별: "it blocks a `PreToolUse` tool call and a `UserPromptSubmit` prompt, but has no blocking effect on `PostToolUse`, where it only shows stderr to Claude."
  > "Exit code 1 without valid JSON output is a non-blocking error... If your hook is meant to enforce a policy, use `exit 2`."
  > "Exit codes only let you block or stay silent, but JSON output gives you finer-grained control."
  > `permissionDecision`: "`\"allow\"` skips the permission prompt, except for actions no mode auto-approves and reads from network paths... `\"deny\"` prevents the tool call. `\"ask\"` prompts the user to confirm. `\"defer\"` exits gracefully so the tool can be resumed later. Deny and ask rules are still evaluated regardless of what the hook returns."
  > `permissionDecisionReason`: "For `\"ask\"`, shown to the user in the permission prompt. ... For `\"deny\"`, shown to Claude. For `\"allow\"` and `\"defer\"`, written to the debug log only."
  > "When multiple PreToolUse hooks return different decisions, precedence is `deny` > `defer` > `ask` > `allow`."
  > `updatedInput`: "Modifies the tool's input parameters before execution. Replaces the entire input object, so include unchanged fields alongside modified ones."
  > Stop 훅: "The `stop_hook_active` field is `true` when Claude Code is already continuing as a result of a stop hook." / "Claude Code applies an 8-consecutive-continuation cap: after stop hooks have continued the turn eight times in a row, Claude Code overrides the next block and ends the turn. ... To raise the cap, set `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`."
  > Stop 출력: `decision` "`\"block\"` prevents Claude from stopping. Omit to allow Claude to stop." / `reason` "Required when `decision` is `\"block\"`. Tells Claude why it should continue."
  > PostToolUse 출력: `decision` "`\"block\"` adds the `reason` next to the tool result. Claude still sees the original output; to replace it, use `updatedToolOutput`."
  > SessionStart: "A hook that only adds context can print it without building JSON, because Claude Code adds a SessionStart hook's plain-text stdout to Claude's context."
  > matcher: `"*"`, `""`, 생략 = 전부. 영숫자·`_`·`-`·공백·`,`·`|`만 있으면 정확 문자열 또는 목록(예 `Edit|Write`). 그 외는 "treated as an unanchored JavaScript regular expression." MCP: "To match every tool from a server, append `.*` to the server prefix. The `.*` is required." 예: `mcp__memory__.*`, `mcp__.*__write.*`
  > `args` 필드: "Argument list. When present, `command` is resolved as an executable and spawned directly with `args` as the argument vector, with no shell involved."
  > 설정 위치 표: `~/.claude/settings.json`(All your projects, 공유 불가) · `.claude/settings.json`(Single project, "Yes, can be committed") · `.claude/settings.local.json`(gitignored) · Managed policy settings(Organization-wide, admin-controlled) · Plugin `hooks/hooks.json` · Skill frontmatter("Rest of the session once invoked") · Subagent frontmatter("While that subagent is running")
  > `CLAUDE_PROJECT_DIR`: "the project root where the session started." 워크트리에 들어가도 고정.
  > 타임아웃: "`UserPromptSubmit` hooks have a default timeout of 30 seconds for `command`, `http`, and `mcp_tool` types, shorter than the 600-second default for those types on most other events."
  > 비동기: "set `\"async\": true` to run the hook in the background while Claude continues working. Async hooks can't block or control Claude's behavior"
  > 보안: "Command hooks execute shell commands with your full user permissions. They can modify, delete, or access any files your user account can access. Review and test all hook commands before adding them to your configuration."
  > 워크스페이스 신뢰: "**`-p` or SDK session**: Claude Code never shows the dialog and treats the folder as trusted, so hooks committed in a repository's `.claude/settings.json` run in a folder you've never trusted" / "Before you script `claude -p` over a repository you didn't write, review its `.claude/` settings files, start with `--bare`, or turn hooks off for that run with `--settings '{\"disableAllHooks\": true}'`."
  > 보안 모범사례: "Validate and sanitize inputs" · "Always quote shell variables: use `\"$VAR\"` not `$VAR`" · "Block path traversal: check for `..` in file paths" · "Use absolute paths" · "Skip sensitive files: avoid `.env`, `.git/`, keys, etc."
- 코스와의 차이: 코스 레슨 6의 `PostToolUse` + `exit 2` 패턴은 문서상 "차단이 아니라 메시지 전달"임 — 코스도 "A hook that runs after an edit cannot undo it, so exit code 2 puts the script's message in front of Claude"라고 정확히 썼다. 코스 레슨 11의 `permissionDecision` 3값(allow/ask/deny)에 현행 문서는 `defer`를 추가. 훅 타입이 코스 설명(command)보다 넓다(prompt/agent/http/mcp_tool).
- 관련 섹션: Build-훅 가드레일(레슨 6), Deploy-승인 게이트(레슨 11), Test-테스트 파일 보호(레슨 8), Maintain-SessionStart 컨텍스트 주입

### 자료 2: Hooks guide (입문·입력 JSON·prompt/agent 훅)
- 출처: https://code.claude.com/docs/en/hooks-guide
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 훅 = "결정론적 제어". CLAUDE.md는 권고, 훅은 보장. stdin으로 JSON 입력(session_id, cwd, hook_event_name, tool_name, tool_input). 판단이 필요한 조건은 prompt/agent 훅.
- 인용 가능한 구절:
  > "Hooks are user-defined shell commands. Claude Code runs them at specific points in its lifecycle, which gives you deterministic control: certain actions always happen rather than relying on the LLM to choose to run them."
  > "For decisions that require judgment rather than deterministic rules, you can also use prompt-based hooks or agent-based hooks that use a Claude model to evaluate conditions."
  > 입력 필드: "Every event includes common fields like `session_id`, a unique ID for the session, and `cwd`, the working directory when the event fired" / PreToolUse는 `hook_event_name`, `tool_name`, `tool_input`("For Bash, its `command` field holds the shell command.")
  > 보호 파일 예시: ".env, package-lock.json, or anything in .git/" 를 PreToolUse 스크립트가 `exit 2`로 차단, "Claude receives feedback explaining why the edit was blocked, so it can adjust its approach."
  > 포매터 예시: `"command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"` (PostToolUse, matcher Edit|Write)
  > 병렬 훅 결합: "The deny takes precedence, so Claude Code blocks the command and shows Claude the guardrail's stderr."
  > "Other events use different decision patterns. For example, `PostToolUse` and `Stop` hooks use a top-level `decision: \"block\"` field, while `PermissionRequest` uses `hookSpecificOutput.decision.behavior`."
  > prompt 훅: "Instead of running a shell command, Claude Code sends your prompt and the hook's input data to a Claude model to make the decision." 기본 timeout 30초. agent 훅: "a longer default timeout of 60 seconds and up to 50 tool-use turns."
  > ConfigChange: "The matcher filters by configuration type: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, or `skills`. To block a change from taking effect, exit with code 2 or return `{\"decision\": \"block\"}`."
- 관련 섹션: 레슨 5/6 "CLAUDE.md vs skill vs hook" 선택 기준, 레슨 8 테스트 파일 잠금

### 자료 3: Skills (SKILL.md 구조·frontmatter·커맨드 통합)
- 출처: https://code.claude.com/docs/en/skills
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 스킬 위치 5곳(Enterprise/Personal/Project/Nested/Plugin). frontmatter는 전부 선택, `description` 권장. description+when_to_use 합계 1,536자에서 잘림. `.claude/commands/*.md`는 스킬에 통합됨. "CLAUDE.md의 절차가 길어지면 스킬로" 가 공식 기준.
- 인용 가능한 구절:
  > 위치: Enterprise `.claude/skills/<skill-name>/SKILL.md` in the managed settings directory · Personal `~/.claude/skills/<skill-name>/SKILL.md` · Project `.claude/skills/<skill-name>/SKILL.md` · Nested `<subdir>/.claude/skills/<skill-name>/SKILL.md` · Plugin `<plugin>/skills/<skill-name>/SKILL.md`
  > "Where you save a skill decides which sessions load it." 이름 충돌 시 "Enterprise over personal, and personal over project."
  > frontmatter 필드: `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility`
  > "All fields are optional. Only `description` is recommended so Claude knows when to use the skill."
  > "A field name must match the table exactly, hyphens included: Claude Code ignores a field it doesn't recognize without reporting an error."
  > "Put the key use case first: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing to reduce context usage."
  > `disable-model-invocation: true` → "Claude can't invoke the skill on its own." / `user-invocable: false` → "Only Claude can invoke the skill."
  > "**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working." / "Prefer a skill for new work, since skills also support supporting files."
  > "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files."
  > "Once a skill loads, its content stays in context across turns, so every line is a recurring token cost."
  > **CLAUDE.md vs 스킬 기준:** "Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it."
- 코스와의 차이: 코스 레슨 3의 "organization-level slash command"는 현행 문서상 스킬(SKILL.md)로 쓰는 것이 권장 경로. 코스 레슨 6의 `secure-api-review` 예시 frontmatter(name/description)는 현행과 호환.
- 관련 섹션: 레슨 6 스킬, 레슨 3 spec 생성 커맨드, 레슨 2 intent.md 템플릿 스킬

### 자료 4: Subagents (.claude/agents·frontmatter·격리)
- 출처: https://code.claude.com/docs/en/sub-agents
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 서브에이전트는 자기 컨텍스트 창·시스템 프롬프트·도구·권한을 가진다. 정의 위치 5단계 우선순위. `isolation: worktree`로 워크트리 격리, `memory`로 세션 간 학습, `maxTurns`로 상한.
- 인용 가능한 구절:
  > 우선순위: Managed settings(1) · `--agents` CLI flag(2) · `.claude/agents/`(3) · `~/.claude/agents/`(4) · Plugin `agents/`(5)
  > "**Project subagents** (`.claude/agents/`) are ideal for subagents specific to a codebase. Check them into version control so your team can use and improve them collaboratively."
  > "Only `name` and `description` are required."
  > 필드: `tools` "Inherits every tool available to subagents if omitted." · `model` "`sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5-5`, or `inherit`" · `permissionMode` "`default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, or `manual`" · `maxTurns` "When the subagent reaches the limit, Claude Code returns its output marked as partial" · `skills` "The full skill content is injected, not only the description." · `memory` "`user`, `project`, or `local`. Enables cross-session learning" · `isolation` "Set to `worktree` to run the subagent in a temporary git worktree ... The worktree is automatically cleaned up if the subagent makes no changes"
  > "Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history, the skills you've already invoked, or the files Claude has already read."
  > "Subagents receive only this system prompt plus basic environment details like the working directory, not the Claude Code system prompt."
  > 내장: Explore "A fast, read-only agent optimized for searching and analyzing codebases." · Plan "A research agent used during plan mode to gather context before presenting a plan." · General-purpose "A capable agent for complex, multi-step tasks that require both exploration and action."
  > 호출: "Claude uses each subagent's description to decide when to delegate tasks." / 명시 호출 예 `Use the test-runner subagent to fix failing tests` / `@"code-reviewer (agent)" look at the auth changes` / `claude --agent code-reviewer`
- 코스와의 차이: 코스 레슨 7의 `verifier.md`(name/description/tools)는 현행 스키마와 호환. 코스가 언급하지 않는 `isolation: worktree`·`memory`·`maxTurns`는 책에서 "병렬 세션 vs 서브에이전트" 경계를 설명할 때 유용.
- 관련 섹션: 레슨 7 병렬 세션·서브에이전트, 레슨 8 verifier(신선한 컨텍스트) 근거

### 자료 5: Memory — CLAUDE.md 계층·@import·rules·auto memory
- 출처: https://code.claude.com/docs/en/memory
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (AGENTS.md 직접 읽기 v2.1.277+)
- 신뢰성: 최상
- 핵심 주장: CLAUDE.md는 "context, not enforced configuration". 4계층(Managed/User/Project/Local) + 상위 디렉터리는 시작 시, 하위 디렉터리는 접근 시 로드. `@import` 최대 4홉. 권장 크기 200줄 미만. `.claude/rules/`로 경로 스코프 분할. 코스의 "under a page" 지침의 공식 근거.
- 인용 가능한 구절:
  > "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead. The more specific and concise your instructions, the more consistently Claude follows them."
  > 위치 표: Managed policy — macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`, Linux/WSL `/etc/claude-code/CLAUDE.md`, Windows `C:\Program Files\ClaudeCode\CLAUDE.md` · User `~/.claude/CLAUDE.md` · Project `./CLAUDE.md` or `./.claude/CLAUDE.md` · Local `./CLAUDE.local.md` ("add to `.gitignore`")
  > "CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand."
  > "All discovered files are concatenated into context rather than overriding each other. Across the directory tree, content is ordered from the filesystem root down to your working directory."
  > "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. ... Imports help you organize a long file but don't reduce its context cost, because imported files also load at launch."
  > "**Consistency**: if two instructions contradict each other, Claude may pick one arbitrarily."
  > "CLAUDE.md files can import additional files using `@path/to/import` syntax. ... Imported files can recursively import other files, with a maximum depth of four hops."
  > "Import parsing skips Markdown code spans and fenced code blocks. To mention a path in your CLAUDE.md without importing it, wrap it in backticks"
  > `/init`: "If a CLAUDE.md already exists, `/init` suggests improvements rather than overwriting it." / `CLAUDE_CODE_NEW_INIT=1`이면 "`/init` asks which artifacts to set up: CLAUDE.md files, skills, and hooks."
  > `.claude/rules/`: "Rules can also be scoped to specific file paths, so they only load into context when Claude works with matching files" (frontmatter `paths:` 글롭)
  > Auto memory: "Loaded into ... Every session (first 200 lines or 25KB)" / 표: "Who writes it — You(CLAUDE.md) / Claude(Auto memory)"
  > Managed CLAUDE.md: "Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings." / 분업 표: "Block specific tools, commands, or file paths → Managed settings: `permissions.deny`" · "Code style and quality guidelines → Managed CLAUDE.md"
  > AGENTS.md: "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it."
- 관련 섹션: 레슨 5 CLAUDE.md, 레슨 10 "리뷰 발견 → CLAUDE.md 환류", 레슨 9 CLAUDE.md 변경이 eval 트리거인 이유

### 자료 6: Headless / 비대화형 (`claude -p`)
- 출처: https://code.claude.com/docs/en/headless
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (`--bare` 동작 강화 v2.1.286, `--permission-prompts` v2.1.259+)
- 신뢰성: 최상
- 핵심 주장: `-p`가 CI의 기본 진입점. `--output-format text|json|stream-json`, `--json-schema`로 구조화 출력. `--allowedTools`는 권한 규칙 문법. `dontAsk`는 프롬프트가 날 모든 호출을 거부. `--bare`는 CLAUDE.md·훅·스킬 등을 건너뛰어 CI 재현성을 높이며 "future release에서 -p의 기본값이 될 것".
- 인용 가능한 구절:
  > "Claude Code exits with code 0 on success and a non-zero code when the run fails, so your scripts can branch on the exit status."
  > "Add `--bare` to reduce startup time by skipping auto-discovery of hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md."
  > "Bare mode is useful for CI and scripts where you need the same result on every machine."
  > "Without `--bare`, a `-p` session runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted."
  > "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."
  > 출력 포맷: "`text` (default): plain text output · `json`: structured JSON with result, session ID, and metadata · `stream-json`: newline-delimited JSON for real-time streaming"
  > "With `--output-format json`, the response payload includes `total_cost_usd` and a per-model cost breakdown"
  > "To get output conforming to a specific schema, use `--output-format json` with `--json-schema` ... with the structured output in the `structured_output` field."
  > "The `--allowedTools` flag uses permission rule syntax. The trailing ` *` enables prefix matching, so `Bash(git diff *)` allows any command starting with `git diff`. The space before `*` is important: without it, `Bash(git diff*)` would also match `git diff-index`."
  > `dontAsk`: "Claude Code denies every call that would otherwise prompt, which is useful for locked-down CI runs. Actions that need no approval in Manual mode still run, such as file reads in your working directories and the read-only command set, and so do actions your `--allowedTools` entries or `permissions.allow` rules cover."
  > `--permission-prompts none`: "Pass `--permission-prompts none` when nobody is available to answer permission prompts, for example in a scheduled job."
  > "Piped stdin is capped at 10MB."
  > 리뷰 스크립트 예: `gh pr diff "$1" | claude -p --append-system-prompt "You are a security engineer. Review for vulnerabilities." --output-format json`
  > "User-invoked skills and custom commands work. Include `/skill-name` in the prompt string and Claude Code expands it before running."
- 코스와의 차이: 코스 레슨 9가 "`--bare`는 CLAUDE.md·스킬·훅을 건너뛰므로 eval 워크플로에 넣지 말라"고 한 것과 정합. 코스 레슨 12의 `--permission-mode dontAsk` 설명("denies any call that would otherwise prompt")도 정합.
- 관련 섹션: 레슨 9 CI evals, 레슨 12 CI/CD, 레슨 13 헤드리스 진단 러너

### 자료 7: CLI reference (플래그 정의)
- 출처: https://code.claude.com/docs/en/cli-reference
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 책에서 쓰일 플래그의 정식 정의. `--permission-mode` 7값(manual 별칭 포함). `--worktree`가 `<repo>/.claude/worktrees/<name>`에 생성. `--max-turns`·`--max-budget-usd`는 print 모드 전용.
- 인용 가능한 구절:
  > `--permission-mode`: "Accepts `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`, or `manual` as an alias for `default`."
  > `--allowedTools`: "Tools that execute without prompting for permission, apart from reads from network paths. ... To restrict which tools are available, use `--tools` instead."
  > `--disallowedTools`: "A bare tool name removes the matching tools from Claude's context: `\"Edit\"` removes Edit, `\"*\"` removes every tool, and `\"mcp__*\"` removes every MCP tool."
  > `--bare`: "Minimal mode: skip auto-discovery of hooks, skills, custom commands, subagents, installed plugins, MCP servers, auto memory, and CLAUDE.md so scripted calls start faster."
  > `--worktree`, `-w`: "Start Claude in an isolated git worktree at `<repo>/.claude/worktrees/<name>`. If you don't give a name, Claude Code generates one. Pass `#<number>`, a GitHub pull request URL, or a GitLab merge request URL to fetch that PR or MR from `origin` and branch the worktree from it"
  > `--max-turns`: "Limit the number of agentic turns (print mode only). Exits with an error when the limit is reached. No limit by default."
  > `--max-budget-usd`: "Stop the run once estimated spend on API calls reaches this amount (print mode only)."
  > `--json-schema`: "Get validated JSON output matching a JSON Schema after the agent completes its workflow (print mode only)."
  > `--agent`: "Specify an agent for the current session (overrides the `agent` setting)"
  > `--dangerously-skip-permissions`: "Skip permission prompts. Equivalent to `--permission-mode bypassPermissions`."
  > `--restricted`: "Use it when an evaluation harness drives `claude` on a shared machine and Claude Code must not run commands or read that machine's user and project settings." (v2.1.248+)
  > `claude setup-token`: "Generate a long-lived OAuth token for CI and scripts. Prints the token to the terminal without saving it. Requires a Claude subscription."
  > 시스템 프롬프트 선택 지침: "Use an append flag when Claude should remain a coding assistant that also follows your extra rules ... Use a replacement flag when the surface, identity, or permission model differs from Claude Code's, like a non-coding agent in a pipeline that no human watches."
- 관련 섹션: 레슨 7 `claude --worktree`, 레슨 9/12 `-p` 플래그, 부록 "플래그 치트시트"

### 자료 8: Permission modes — plan mode·auto mode·dontAsk
- 출처: https://code.claude.com/docs/en/permission-modes
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (auto 모드 기본 시작 v2.1.283+)
- 신뢰성: 최상
- 핵심 주장: v2.1.283부터 대화형 세션의 **기본 시작 모드가 auto**(분류기 모델이 사람 대신 검토). plan 모드는 읽기 전용이며 승인 전 편집 차단, `Ctrl+G`로 플랜을 에디터에서 직접 편집. 승인 옵션에 "Yes, and use auto mode". `dontAsk`는 CI용. 분류기는 3회 연속/20회 누적 차단 시 프롬프트로 폴백.
- 인용 가능한 구절:
  > 모드 표: `default` "Reads only" · `acceptEdits` "Reads, file edits, and common filesystem commands" · `plan` "Reads, plus classifier-approved commands when auto mode is available" · `dontAsk` "File reads inside your working directories and pre-approved tools; anything that would prompt is denied — Locked-down CI and scripts" · `bypassPermissions` "Everything — Isolated containers and VMs only"
  > "With Claude Code v2.1.283 or later, auto mode is the built-in starting permission mode for interactive terminal and VS Code sessions."
  > "Modes set the baseline. Layer permission rules on top to pre-approve or block specific tools. Deny rules block in every mode, including `bypassPermissions`."
  > 플랜 모드: "Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Except in interactive terminal sessions with bypass permissions available, edits stay blocked until you approve the plan."
  > "Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`." / CLI: `claude --permission-mode plan`
  > 승인 옵션: "**Yes, and use auto mode**: approve and start in auto mode. If auto mode isn't available to your session ... this option reads **Yes, auto-accept edits**." / "**No, keep planning**: stay in plan mode and tell Claude what to change."
  > "Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds."
  > "To make plan mode the default for a project's terminal sessions, set `defaultMode` to `plan` in `.claude/settings.json`"
  > auto 모드: "A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read. Explicit ask rules still force a prompt."
  > "The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude \"don't push\" or \"wait until I review before deploying\", the classifier blocks matching actions even when the default rules would allow them." / "Boundaries are not stored as rules. ... For a hard guarantee, add a deny rule instead."
  > 폴백: "if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting."
  > CI 셋업 표: "Run in CI with an exact allowlist — `claude -p \"run the test suite\" --permission-mode dontAsk --allowedTools \"Bash(npm test)\" \"Read\"`"
  > "`permissions.defaultMode` values `auto` and `bypassPermissions` don't take effect from project or local settings; set them in user or managed settings instead"
  > 조직 차단: "To prevent developers from using auto mode, set `disableAutoMode` to `\"disable\"` in managed settings."
  > `-p` 시작 모드: "`default` in sessions that fetch feature flags. In sessions that don't, such as on a third-party provider or with telemetry off, `auto` with Claude Code v2.1.285 or later" (체인지로그 2.1.302: 서드파티·텔레메트리 off·신규 설치는 다시 `default`)
- 코스와의 차이: 코스 레슨 4의 "auto mode" 단락은 선택 기능처럼 쓰였지만 현행은 **기본값**. 책은 "플랜 → 승인 → auto"가 기본 흐름임을 전제해야 한다.
- 관련 섹션: 레슨 4 플랜 모드, 레슨 7 "승인 대기 없는 병렬 세션", 레슨 12 dontAsk

### 자료 9: Settings — 파일 위치·우선순위·managed 전용 키
- 출처: https://code.claude.com/docs/en/settings (키별 상세는 /docs/en/settings-reference)
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 우선순위 Managed > `--settings` > `.claude/settings.local.json` > `.claude/settings.json` > `~/.claude/settings.json`. `permissions.allow`는 스코프 간 병합(단 `allowManagedPermissionRulesOnly`면 예외). 일부 보안 키는 더 엄격한 하위 값을 존중.
- 인용 가능한 구절:
  > "In order, highest precedence first: 1. **Managed settings**: settings your organization deploys, by a `managed-settings.json` file, an MDM policy, or server-managed settings from the claude.ai console. Nothing in your own settings files or `--settings` overrides a managed key"
  > 표: User `~/.claude/settings.json` "You, in every project on this machine" · Project local `.claude/settings.local.json` "You, in this one project only. Claude Code keeps it out of git when it creates the file" · Managed `managed-settings.json` "Security policy and compliance requirements"
  > "Commit `.claude/settings.json` so everyone who clones the repository gets the same permissions, hooks, and plugins. Each teammate can still override it for themselves in their own `.claude/settings.local.json`"
  > "When Claude asks permission to run a Bash command and you choose \"Yes, and don't ask again\", Claude Code saves that approval as an `allow` rule in `.claude/settings.local.json`."
  > "Your organization's allow rules still apply alongside yours. That's expected: Claude Code merges `permissions.allow` across scopes, unless your organization sets `allowManagedPermissionRulesOnly`."
  > 예시 규칙 문법: `"Bash(npm run lint)"`, `"Bash(npm run test *)"`, deny `"Read(./.env)"`, `"Read(./.env.*)"`; JSON 스키마 `https://json.schemastore.org/claude-code-settings.json`
  > "**`--settings`**: pass a key as JSON, inline or as a path to a file. Claude Code applies it above your user, project, and local files and below managed settings."
  > "Run `/status` inside Claude Code to see which settings sources are active."
- 코스와의 차이: 코스 레슨 11의 managed 예시 키(`allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `allowManagedMcpServersOnly`, `disableSideloadFlags`, `strictKnownMarketplaces`, `requiredMinimumVersion`, `disableBypassPermissionsMode`, `sandbox.*`)는 settings-reference의 managed-only 키 — 개인·소규모 팀 책에서는 "팀 공유 `.claude/settings.json` + 개인 `settings.local.json`" 두 층이 실질 범위.
- 관련 섹션: 레슨 11 managed settings(조직 → 팀 번역), 레슨 7 "권한을 리포에서 통제"

### 자료 10: Worktrees — 병렬 세션 격리
- 출처: https://code.claude.com/docs/en/worktrees
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: `--worktree`는 `.claude/worktrees/<name>/`에 `worktree-<name>` 브랜치로 생성. 기본 베이스는 원격 기본 브랜치(`"fresh"`). 종료 시 정리 프롬프트. 격리 중 메인 체크아웃 편집·git 리다이렉트 차단. `.worktreeinclude`로 `.env` 복사. 서브에이전트도 `isolation: worktree`.
- 인용 가능한 구절:
  > "Running each Claude Code session in its own worktree gives it a separate copy of the files to edit, so one session can build a feature while a second fixes a bug."
  > "By default, the worktree is created under `.claude/worktrees/<name>/` at your repository root, on a new branch named `worktree-<name>`"
  > "Add `.claude/worktrees/` to your `.gitignore` so worktree contents don't appear as untracked files in your main checkout."
  > "A worktree is a fresh checkout, so initialize your development environment there ... To carry gitignored files such as `.env` into every new worktree automatically, add a `.worktreeinclude` file."
  > 정리: "**The worktree is clean**: for an unnamed session, Claude removes the worktree and its branch automatically." / "**The worktree has work in it**: Claude prompts you to keep or remove the worktree."
  > "Non-interactive runs with `-p` have no exit prompt, so Claude doesn't clean up their worktrees"
  > 격리 4검사: "**File edits**: Claude Code blocks an `Edit`, `Write`, or `NotebookEdit` that targets a path in the main checkout." / "**Git redirects**: Claude Code blocks a Bash or Monitor command that redirects git into the main checkout."
  > 베이스 브랜치: "`\"fresh\"` (default): branch from the repository's default branch on the remote, usually `main`" / "`\"head\"`: branch from your current local `HEAD`"
  > 훅 경로: "**`${CLAUDE_PROJECT_DIR}` stays put** ... **`cwd` follows Claude**: the `cwd` field in the hook's input JSON is the worktree root"
  > 권한 공유: "choosing \"Yes, and don't ask again\" for a Bash command in a worktree session saves the rule to the main checkout's `.claude/settings.local.json`, so it applies in the main checkout and in every other worktree"
- 코스와의 차이: 코스 레슨 7 `claude --worktree feature-auth` / `fix-rate-limit` 예시와 정합. 코스가 생략한 `.worktreeinclude`·정리 규칙·격리 검사는 개인 개발자가 바로 부딪히는 실무 포인트.
- 관련 섹션: 레슨 7 병렬 세션, 레슨 9 eval 워크플로의 `git worktree add --detach`

### 자료 11: GitHub Actions (claude-code-action v1)
- 출처: https://code.claude.com/docs/en/github-actions (액션 저장소 https://github.com/anthropics/claude-code-action)
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (리뷰 결과 PR 게시 v2.1.229+)
- 신뢰성: 최상
- 핵심 주장: `/install-github-app`로 설치, 시크릿은 `ANTHROPIC_API_KEY` 또는 `CLAUDE_CODE_OAUTH_TOKEN`(`claude setup-token`). `prompt` 유무로 interactive(@claude 대기)/automation 모드 자동 판별. 트리거는 write 권한 사람만, 봇 차단. `claude_args`로 CLI 플래그 전달. 리뷰는 `code-review` 플러그인 스킬 + `--comment`.
- 인용 가능한 구절:
  > "Mention `@claude` in a pull request or issue comment to have Claude analyze code, implement changes, and push commits. You can also give the Claude Code GitHub Action a prompt to run automatically on any GitHub event."
  > "**Quick setup**: run `/install-github-app` from Claude Code. Claude Code installs the GitHub App, adds your authentication secret, and prepares the workflow pull request for you" / "For either path, you need admin access to the repository."
  > "`CLAUDE_CODE_OAUTH_TOKEN`: an OAuth token that authenticates with your Claude subscription, available on Pro, Max, Team, and Enterprise plans. Generate one by running `claude setup-token` locally."
  > 모드: "**Interactive mode**: when the workflow provides no `prompt` input, Claude waits for the trigger phrase, `@claude` by default" / "**Automation mode**: when the workflow provides a `prompt` input, Claude runs without waiting for a mention"
  > 트리거 검사: "**Write access**: on issue and pull request events, the triggering user must have write access to the repository." / "**Human actor**: on every event, the Claude Code GitHub Action rejects a bot actor unless you list it in `allowed_bots`, which keeps bots from triggering Claude in a loop."
  > 리뷰 워크플로 핵심 입력: `plugin_marketplaces: "https://github.com/anthropics/claude-code.git"` / `plugins: "code-review@claude-code-plugins"` / `prompt: "/code-review:code-review --comment ${{ github.repository }}/pull/${{ github.event.pull_request.number }}"` / `claude_args: '--allowedTools "mcp__github_inline_comment__create_inline_comment"'`
  > "**`--comment`**: Claude posts its review on the pull request, as an inline comment on each issue it finds or as one summary comment when it finds none. Without it, Claude posts nothing, and you read the findings in the workflow run log."
  > "Claude skips draft and closed pull requests, pull requests it judges not to need a review, such as automated or trivial ones, and pull requests that already have a comment from Claude."
  > "On public repositories, GitHub withholds secrets from runs triggered by fork pull requests, so the review runs only on pull requests from branches in the same repository."
  > 비용: "Set `--max-turns` in `claude_args` to limit iterations · Set workflow-level timeouts to avoid runaway jobs · Use GitHub's concurrency controls to limit parallel runs"
  > "GitHub doesn't trigger workflows on commits made with the default `GITHUB_TOKEN`."
  > 클라우드: `use_bedrock: "true"` / `use_vertex: "true"` / `use_foundry: "true"` — "you authenticate through OIDC identity federation instead of a Claude API key"
  > 베타 → v1: "Replace `direct_prompt` with `prompt` · Move CLI options such as `max_turns` and `model` into `claude_args`. `custom_instructions` ... becomes `--append-system-prompt`"
- 관련 섹션: 레슨 10 PR 리뷰 루프(@claude 수정 루프), 레슨 12 CI/CD, 레슨 3 "intent 머지 → spec PR 자동 생성" 배관

### 자료 12: Code Review 관리형 서비스 (+ REVIEW.md 커스터마이즈 + 심각도)
- 출처: https://code.claude.com/docs/en/code-review · https://code.claude.com/docs/en/code-review-customize · https://code.claude.com/docs/en/code-review-pull-requests
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (`@claude review` 구독 동작 변경 2026-07)
- 신뢰성: 최상
- 핵심 주장: Team/Enterprise 플랜 전용 관리형 서비스. 4단계(Find→Verify→Rank→Post). 승인/차단 안 함, check run은 실패로 끝나지 않음. `REVIEW.md`(루트·서브디렉터리, **베이스/기본 브랜치에서만 읽음**)와 `CLAUDE.md`로 조정. 심각도 Important/Nit/Pre-existing. check run 마지막 줄에 기계 판독 가능 집계. 로컬 `/code-review`는 REVIEW.md를 읽지 않음.
- 인용 가능한 구절:
  > "Several agents read each change alongside the surrounding code, looking for issues such as logic errors, security vulnerabilities, or broken edge cases. A verification step checks findings against the code before they're reported."
  > "A review never approves or blocks the pull request, so the decision to merge stays with your team."
  > "**Plans**: Team and Enterprise" / "Run `/code-review` in your Claude Code session on any plan"
  > "By default, Code Review focuses on correctness: bugs that would break production, not formatting preferences or missing test coverage."
  > 4단계: "1. **Find**: several agents examine the diff and the surrounding code in parallel. 2. **Verify**: a verification step checks the candidate findings against the code and filters out false positives. 3. **Rank**: the findings that remain are deduplicated and ranked by severity. 4. **Post**"
  > 리뷰 레벨: Quick / Standard("The default level") / Deep
  > "**Which instructions it follows**: `REVIEW.md` from the base or default branch and never from the pull request's own changes."
  > "The Code Review service and the local `/code-review` command are two separate tools, and they read different files. The service reads both `CLAUDE.md` and `REVIEW.md`. The `/code-review` command ... reads your `CLAUDE.md` files and not `REVIEW.md`."
  > REVIEW.md 예시 항목: "Reserve Important for findings that would break behavior, leak data, or block a rollback" / "Report at most five Nits per review." / "Anything CI already enforces: lint, formatting, type errors" / "Log lines don't include email addresses, user IDs, or request bodies"
  > 심각도: 🔴 Important "A bug that should be fixed before merging" · 🟡 Nit "A minor issue, worth fixing but not blocking" · 🟣 Pre-existing "A bug that exists in the codebase but wasn't introduced by this PR"
  > "The check run concludes as neutral ... It never concludes as a failure, so a finished review doesn't fail a required check."
  > 기계 판독: `gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'` → "`{\"nit\": 1, \"normal\": 2, \"pre_existing\": 0}`" / "**`normal` is above zero**: fail the job if you want to gate the merge. The `normal` key holds the count of Important findings"
  > 코멘트 명령: `@claude review`(1회) · `@claude review always`(푸시마다 구독) · "You need write, maintain, or admin permission on the repository."
  > "If the repository also runs the Claude Code GitHub Action in interactive mode with its default `@claude` trigger phrase, an `@claude review` comment starts the Action as well. To keep the two apart, set the Action's `trigger_phrase` input to a different phrase."
  > 비교 표: Code Review(Anthropic infra, Team/Enterprise) · `/code-review`(세션, Anyone) · Ultrareview(cloud sandbox) · GitHub Actions/GitLab(own CI runners) · 자작 subagent/skill
- 코스와의 차이: 코스 레슨 10은 "managed Code Review (research preview)"로 표기 — 현행 문서에는 "research preview" 라벨 없음, Team/Enterprise 플랜 조건 명시. 코스의 `REVIEW.md` 예시(Passes/Important/Cap nits/Do not report) 구조는 현행 예시와 거의 일치. 코스의 "severity counts ... machine-readable tally" 문장이 가리키는 것이 `bughunter-severity` 주석. **개인/소규모 팀(Pro/Max)에게는 `/code-review`·claude-code-action이 현실 경로.**
- 관련 섹션: 레슨 10 PR 리뷰 루프

### 자료 13: Commands — /review·/security-review·/code-review·/init 등
- 출처: https://code.claude.com/docs/en/commands
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (`/review`가 `/code-review` 별칭이 된 것 v2.1.223)
- 신뢰성: 최상
- 핵심 주장: `/review`는 이제 `/code-review`의 별칭. `/security-review`는 origin 기본 브랜치와의 diff를 보안 관점으로 검토. `/batch`는 5~30 서브에이전트 워크트리 병렬. `/verify`·`/goal`·`/simplify`는 번들 스킬.
- 인용 가능한 구절:
  > "**Before you ship.** `/diff` shows what changed. `/code-review` checks the current diff for correctness bugs and can apply the findings with `--fix`; pass a PR number, such as `/code-review high 1234`, to review a pull request instead. `/review` is an alias. `/code-review ultra` runs a multi-agent review in the cloud. `/security-review` checks the diff for security vulnerabilities."
  > `/review`: "Alias of `/code-review` ... Before v2.1.223, `/review` was a separate command that ran a single-pass, read-only review of a GitHub pull request by number"
  > `/security-review`: "Analyze the changes on your current branch for security vulnerabilities. Reviews the diff between your branch and origin's default branch, identifying risks like injection, auth issues, and data exposure. Needs an `origin` remote"
  > `/init`: "Initialize project with a `CLAUDE.md` guide. Set `CLAUDE_CODE_NEW_INIT=1` for an interactive flow that also walks through skills, hooks, and personal memory files. If `/init` finds OpenAI Codex or Google Gemini CLI configuration, it offers to carry it over with `/import`"
  > `/plan [description]`: "Enter plan mode directly from the prompt."
  > `/batch <instruction>`: "Researches the codebase, decomposes the work into 5 to 30 independent units, and presents a plan. Once approved, spawns one background subagent per unit in an isolated worktree. Each subagent implements its unit, runs tests, and publishes its change."
  > `/verify`: "Confirm a code change does what it should by building your project's app, running it, and observing the result, rather than relying on tests or type checks."
  > `/goal [condition|clear]`: "Claude keeps working across turns until the condition is met"
  > `/simplify`: "Four review agents run in parallel, covering reuse of existing helpers, simplification, efficiency, and whether the change is at the right level of abstraction. The review doesn't look for correctness bugs."
  > `/ultrareview`: "Includes 3 free runs on Pro and Max, then requires usage credits"
  > `/install-github-app`: "Works only with github.com repositories."
  > `/permissions`: "Manage allow, ask, and deny rules for tool permissions. ... Alias: `/allowed-tools`"
  > `/memory`: "Edit `CLAUDE.md` files, enable or disable auto memory, and view auto memory entries"
- 관련 섹션: 레슨 10(로컬 리뷰 대안), 레슨 8(`/verify`·`/goal`로 피드백 루프), 레슨 5(`/init`)

### 자료 14: Best practices (공식 문서판; 구 anthropic.com/engineering 글의 후신)
- 출처: https://code.claude.com/docs/en/best-practices (https://www.anthropic.com/engineering/claude-code-best-practices 는 이 페이지로 308 리다이렉트)
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. 원 블로그(2025-04)와 달리 날짜 미표기.
- 신뢰성: 최상
- 핵심 주장: 모든 모범사례의 뿌리는 "컨텍스트 창은 빨리 차고, 차면 성능이 떨어진다". 검증 수단 제공 → 플랜 모드(Explore/Plan/Implement/Commit) → CLAUDE.md 간결 → 서브에이전트로 조사 격리 → `-p` 팬아웃 → Writer/Reviewer 두 세션 → 적대적 리뷰 서브에이전트.
- 인용 가능한 구절:
  > "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."
  > "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."
  > "Claude stops when the work looks done. Without a check it can run, \"looks done\" is the only signal available, and you become the verification loop"
  > 게이트 단계: "**In one prompt** ... **Across a session**: set the check as a `/goal` condition ... **As a deterministic gate**: a Stop hook runs your check as a script and blocks the turn from ending until it passes ... **By a second opinion**: a verification subagent"
  > "Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned, or a screenshot of the result."
  > "Letting Claude jump straight to coding can produce code that solves the wrong problem. Use plan mode to separate exploration from execution." / 4단계 Explore → Plan → Implement → Commit
  > "Plan mode is useful, but also adds overhead. ... If you could describe the diff in one sentence, skip the plan."
  > CLAUDE.md: "Keep it concise. For each line, ask: *\"Would removing this cause Claude to make mistakes?\"* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
  > 포함/제외 표: Include "Bash commands Claude can't guess · Code style rules that differ from defaults · Testing instructions and preferred test runners · Repository etiquette (branch naming, PR conventions) · Architectural decisions specific to your project · Developer environment quirks · Common gotchas" / Exclude "Anything Claude can figure out by reading code · Standard language conventions · Detailed API documentation (link to docs instead) · Information that changes frequently · Long explanations or tutorials · File-by-file descriptions · Self-evident practices like \"write clean code\""
  > "If Claude keeps skipping one instruction, add emphasis such as \"IMPORTANT\" to that line alone. If you emphasize many lines, none of them stands out."
  > 훅: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." / "Claude can write hooks for you. Try prompts like *\"Write a hook that runs eslint after every file edit\"*"
  > 인터뷰 → 스펙: "I want to build [brief description]. Interview me in detail using the AskUserQuestion tool. ... Keep interviewing until we've covered everything, then write a complete spec to SPEC.md." / "Once the spec is complete, start a fresh session to execute it." / "The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step that proves the feature works."
  > "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh"
  > 팬아웃: `for file in $(cat files.txt); do claude -p "Migrate $file from Python 2 to Python 3. Return OK or FAIL." --allowedTools "Edit,Bash(git commit *)" --permission-mode dontAsk; done`
  > Writer/Reviewer: "A fresh context improves code review since Claude won't be biased toward code it just wrote."
  > 적대적 리뷰: "A reviewer running in a fresh subagent context sees only the diff and the criteria you give it, not the reasoning that produced the change" / 주의: "A reviewer prompted to find gaps will usually report some, even when the work is sound ... Tell the reviewer to flag only gaps that affect correctness or the stated requirements"
  > 실패 패턴: "The kitchen sink session" · "Correcting over and over" · "The over-specified CLAUDE.md" · "The trust-then-verify gap — If you can't verify it, don't ship it." · "The infinite exploration"
- 관련 섹션: 레슨 3(인터뷰→spec.md의 개인 버전), 레슨 4, 5, 7, 8, 10 전반

### 자료 15: Sandboxing (OS 수준 격리)
- 출처: https://code.claude.com/docs/en/sandboxing
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 셸 명령만 격리(파일 도구·MCP·훅은 바깥). macOS Seatbelt, Linux/WSL2 bubblewrap+socat. 기본 off, `/sandbox`로 켬. auto-allow 모드면 샌드박스 내 명령은 프롬프트 없이 실행. `failIfUnavailable`·`allowUnsandboxedCommands:false`로 게이트화.
- 인용 가능한 구절:
  > "The Bash sandbox is a boundary that the operating system enforces around the shell commands Claude runs on your machine. ... Because the operating system applies the limits while a command runs, Claude Code can run sandboxed commands without asking you to approve each one."
  > "The sandbox covers shell commands only. Claude's file tools, MCP servers, and hooks run outside it."
  > "The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed."
  > "**macOS**: sandboxing uses the built-in Seatbelt framework" / "**Linux and WSL2**: the sandbox relies on `bubblewrap` and `socat`"
  > "Claude Code builds the sandbox on the open source `@anthropic-ai/sandbox-runtime` package."
  > 네트워크: "No direct route out. Connections go through a proxy on your machine that checks each host against your allowed domains, which start empty."
  > "By default, if the sandbox can't start because a dependency is missing or the platform is unsupported, Claude Code runs commands without sandboxing. To make Claude Code exit at startup instead, set `sandbox.failIfUnavailable` to `true`."
  > "You can disable the unsandboxed retry by setting `\"allowUnsandboxedCommands\": false`"
  > 예: `claude --settings '{"sandbox": {"enabled": true, "allowUnsandboxedCommands": false}}'`
- 관련 섹션: 레슨 11 managed `sandbox` 블록의 개인 버전, 레슨 12 "sandboxed execution"

### 자료 16: Monitoring (OpenTelemetry 메트릭·이벤트)
- 출처: https://code.claude.com/docs/en/monitoring-usage
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19. (체인지로그 2.1.301: `tool_decision`에 `classifier_verdict`·`permission_mode` 추가, 2.1.287: `user_prompt`에 `prompt_text`)
- 신뢰성: 최상
- 핵심 주장: 코스가 "OpenTelemetry export"라고 부르는 것의 실체. 기본 off. 메트릭 8종, 이벤트(user_prompt, tool_result, api_request, api_error, tool_decision 등). 프롬프트 내용은 기본 마스킹. 리포 설정으로는 텔레메트리를 켤 수 없음.
- 인용 가능한 구절:
  > 활성화: `export CLAUDE_CODE_ENABLE_TELEMETRY=1` / `OTEL_METRICS_EXPORTER=otlp` / `OTEL_LOGS_EXPORTER=otlp` / `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`
  > 메트릭: `claude_code.session.count` · `claude_code.lines_of_code.count` · `claude_code.pull_request.count` · `claude_code.commit.count` · `claude_code.cost.usage`(USD) · `claude_code.token.usage` · `claude_code.code_edit_tool.decision` · `claude_code.active_time.total`(s)
  > `claude_code.tool_decision`: "Logged when a tool permission decision is made (accept/reject)." 속성 `decision` "Either `\"accept\"` or `\"reject\"`" / `source` 값 `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, `"user_reject"`
  > `claude_code.tool_result`: 속성 `tool_name`, `success`, `duration_ms`, `decision_source`, `tool_use_id`, `error_type`
  > `claude_code.api_request`: `model`, `cost_usd`, `duration_ms`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`
  > 프라이버시: "`OTEL_LOG_USER_PROMPTS` | Enable logging of user prompt content (default: disabled)" / "Claude Code ignores the OpenTelemetry exporter variables in a repository's `.claude/settings.json` and `.claude/settings.local.json`, so a repository can't use them to turn telemetry on"
  > `user.id`: "Random anonymous identifier generated on first run and persisted in `~/.claude.json`. It contains no personal information"
- 코스와의 차이: 코스 레슨 7·11이 "concurrent sessions per engineer ... counted from the OpenTelemetry export", "Every hook decision is written to the OpenTelemetry export"라 함 → 실제 이벤트명은 `session.count`·`tool_decision(source="hook")`. 개인 개발자는 OTel 백엔드 대신 `--output-format json`의 `total_cost_usd`·세션 로그로 대체 가능.
- 관련 섹션: 레슨 7, 8, 11, 13 측정 지표의 데이터 소스

### 자료 17: Agent SDK overview
- 출처: https://code.claude.com/docs/en/agent-sdk/overview
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 코스 레슨 13이 "Agent SDK for a service that receives webhooks"라 부른 것. Claude Code와 같은 도구·에이전트 루프·컨텍스트 관리를 Python/TypeScript 라이브러리로 제공. 다른 언어는 `claude -p --output-format json` 서브프로세스.
- 인용 가능한 구절:
  > "The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript."
  > "To drive the same agent loop from a language other than Python or TypeScript, run the CLI as a subprocess with the `-p` flag and `--output-format json`."
  > 기능 표: Built-in tools · Hooks · Subagents · MCP · Permissions("Control which tools run automatically, which need approval") · Sessions · "Skills, commands, and memory — Load automatically from your project's `.claude/` and from `~/.claude/`, same as Claude Code" · Plugins
  > "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods"
- 관련 섹션: 레슨 13 Maintain 루프의 러너 선택(CI `-p` vs SDK 서비스)

### 자료 18: Claude Code 체인지로그 (2026-09~10 발췌)
- 출처: https://code.claude.com/docs/en/changelog
- 저자·날짜: Anthropic 공식. 최상단 **2.1.303 (October 18, 2026)**. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 책이 다루는 기능들이 아직 활발히 변하는 중이라는 증거. 책에 "2.1.3xx/2026 기준"을 못 박을 근거.
- 인용 가능한 구절 (버전·날짜·원문):
  > 2.1.302 (Oct 16, 2026): "Changed `claude -p` and Agent SDK sessions with no permission mode to start in `default` mode on third-party providers, with telemetry off or on a fresh install; `--permission-mode auto` keeps auto"
  > 2.1.301 (Oct 15, 2026): "Added `classifier_verdict` and `permission_mode` to OpenTelemetry `tool_decision` events, so auto mode classifier decisions can be told apart from permission rules"
  > 2.1.300 (Oct 14, 2026): "Changed hooks: `updatedInput` from PreToolUse and PermissionRequest hooks is now validated like Claude's own input: unknown keys are dropped, and input the tool rejects denies the call"
  > 2.1.299 (Oct 14, 2026): "Changed `UserPromptSubmit` hooks to run before a skill or custom slash command expands, so a hook that blocks the prompt now also stops its embedded shell commands" / "Fixed plan mode running a write ... that a `PreToolUse` hook or a mod's `tool.check` hook allowed"
  > 2.1.295 (Oct 8, 2026): "Added `onFailure: \"block\"` for command and HTTP hooks: a hook that can't start, times out, or exits with an unexpected code blocks the action instead of letting it through" / "Changed subagents to preload at most 32 skills from the `skills` field"
  > 2.1.294 (Oct 8, 2026): "Fixed `prompt` and `agent` hooks written as instructions (such as \"Block commands that...\") allowing what they should block"
  > 2.1.292 (Oct 6, 2026): "Added an `effort` parameter to the Agent tool, so Claude runs a sub-agent at the effort level you ask for" / "Fixed plan mode not being restored when resuming a session"
  > 2.1.290 (Oct 5, 2026): "Changed `/code-review` at medium effort to also report cleanup and CLAUDE.md conventions findings on models without tuned review settings, including Opus 5.5 and Sonnet 5.5"
  > 2.1.288 (Oct 2, 2026): "Added `--max-findings <n>|all` to /code-review" / "Fixed PreToolUse and PermissionRequest hooks being skipped when matching them failed or the tool's input could not be serialized to JSON; the call is now blocked"
  > 2.1.286 (Sep 30, 2026): "Changed `--bare` to connect only the MCP servers named on the command line, send the model no system reminders, and start no background tasks" / "Improved commit guidance: when your project or user skills include one named `verify`, Claude is now told to run it right before committing, except for docs-only and tests-only commits"
  > 2.1.285 (Sep 29, 2026): "Changed `claude -p` and Python Agent SDK sessions on third-party providers or with telemetry off to start in auto mode when no permission mode is configured" (→ 2.1.302에서 다시 default로)
- 관련 섹션: 서문 "이 책의 버전 기준", 각 장의 "구버전 주의" 박스

---

## B. Anthropic 공식 블로그·엔지니어링·릴리스

### 자료 19: Building effective agents
- 출처: https://www.anthropic.com/engineering/building-effective-agents
- 저자·날짜: Erik S., Barry Zhang. "Published Dec 19, 2024". 확인일 2026-10-19. **구버전 정보일 수 있음(2024)** — 단, 개념 정의는 여전히 인용되는 고전.
- 신뢰성: 최상
- 핵심 주장: 워크플로(미리 정한 코드 경로) vs 에이전트(LLM이 스스로 경로 결정) 구분. 다섯 가지 워크플로 패턴. 코딩 에이전트가 잘 되는 이유 = 테스트로 검증 가능.
- 인용 가능한 구절:
  > "Workflows are systems where LLMs and tools are orchestrated through predefined code paths." / Agents: LLMs "dynamically direct their own processes and tool usage."
  > 패턴: Prompt chaining · Routing · Parallelization · Orchestrator-workers · Evaluator-optimizer
  > 원칙: "Maintain **simplicity** in your agent's design." / "Prioritize **transparency** by explicitly showing the agent's planning steps." / "Carefully craft your agent-computer interface (ACI) through thorough tool **documentation and testing**."
  > 코딩: "Code solutions are verifiable through automated tests;" / "Agents can iterate on solutions using test results as feedback;" / agents must "gain \"ground truth\" from the environment at each step"
- 관련 섹션: 레슨 8 피드백 루프의 이론적 근거("ground truth"), 레슨 13 orchestrator-workers로 Maintain 루프 설명

### 자료 20: Writing effective tools for agents
- 출처: https://www.anthropic.com/engineering/writing-tools-for-agents
- 저자·날짜: Ken Aizawa. 2025-09-11. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 도구는 적게·의도적으로, 네임스페이스로 구분, 고신호 컨텍스트 반환, 토큰 효율, 설명은 신입에게 쓰듯. 평가 루프(프로토타입→평가→분석→에이전트와 반복).
- 인용 가능한 구절:
  > "More tools don't always lead to better outcomes."
  > "Namespacing (grouping related tools under common prefixes) can help delineate boundaries between lots of tools"
  > "They should prioritize contextual relevance over flexibility, and eschew low-level technical identifiers."
  > "We suggest implementing some combination of pagination, range selection, filtering, and/or truncation"
  > "Avoid ambiguity by clearly describing (and enforcing with strict data models) expected inputs and outputs."
  > "Start by standing up a quick prototype of your tools." / "Simply concatenate the transcripts from your evaluation agents and paste them into Claude Code."
- 관련 섹션: 레슨 12 "deployment as MCP tools(release/status/rollback)" 설계 근거 — 서버 네임스페이스 `deploy-dev/staging/prod`가 allowlist 경계가 되는 이유

### 자료 21: Effective context engineering for AI agents
- 출처: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 저자·날짜: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield (Applied AI). "Published Sep 29, 2025". 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 컨텍스트는 유한 자원(attention budget, context rot). 시스템 프롬프트는 "right altitude". 적시(just-in-time) 검색. 장기 과제 기법 = compaction·structured note-taking·sub-agent. CLAUDE.md는 "naively dropped into context up front".
- 인용 가능한 구절:
  > "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens"
  > "Context, therefore, must be treated as a finite resource with diminishing marginal returns."
  > "The right altitude is the Goldilocks zone between two common failure modes."
  > "tools should be self-contained, robust to error, and extremely clear with respect to their intended use."
  > 세 기법: "compaction, structured note-taking, and multi-agent architectures." / "Structured note-taking, or agentic memory, is a technique where the agent regularly writes notes." / "specialized sub-agents can handle focused tasks with clean context windows."
  > "CLAUDE.md files are naively dropped into context up front."
- 관련 섹션: 레슨 5 "under a page" 이유, 레슨 7 서브에이전트 이유, 레슨 2~4 intent/spec/plan 파일 = 구조화된 노트

### 자료 22: Demystifying evals for AI agents
- 출처: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 저자·날짜: Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe. "Published Jan 09, 2026". 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 코스 레슨 9 "20~50개 과제"의 출처. 용어(eval/task/trial/grader/transcript/outcome). 그레이더 3종. 포화(saturation)와 "살아 있는 스위트". pass@k vs pass^k. 코딩은 결정론적 그레이더가 자연스럽다.
- 인용 가능한 구절:
  > "An **evaluation** (\"eval\") is a test for an AI system" / "A **task** (a.k.a **problem** or **test case**) is a single test with defined inputs and success criteria." / "Each attempt at a task is a **trial**." / "A **grader** is logic that scores some aspect of the agent's performance." / "The **outcome** is the final state in the environment at the end of the trial."
  > "Agent evaluations typically combine three types of graders: code-based, model-based, and human."
  > "We see teams delay building evals because they think they need hundreds of tasks." / "In reality, 20-50 simple tasks drawn from real failures is a great start." / "Evals get harder to build the longer you wait."
  > "**Eval saturation** occurs when an agent passes all of the solvable tasks, leaving no room for improvement." / "An eval suite is a living artifact that needs ongoing attention and clear ownership to remain useful."
  > pass@k "measures the likelihood that an agent gets at least one correct solution in _k_ attempts." / pass^k "measures the probability that _all k_ trials succeed."
  > "Deterministic graders are natural for coding agents because software is generally straightforward to evaluate" / SWE-bench Verified: "a solution passes only if it fixes the failing tests without breaking existing ones."
- 관련 섹션: 레슨 9 continuous evals(개인용 축소판: 5~10개 과제도 가치), 레슨 13 "incident → eval"

### 자료 23: How Anthropic teams use Claude Code
- 출처: https://claude.com/blog/how-anthropic-teams-use-claude-code (anthropic.com/news 경로는 여기로 리다이렉트)
- 저자·날짜: Anthropic. 2025-07-24. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 팀별 실사용. 수치 발언은 보수적으로 인용(모든 수치는 자가 보고).
- 인용 가능한 구절:
  > Data Infrastructure: 장애 중 "saving them 20 minutes of valuable time during a system outage"
  > Security Engineering: "Problems that typically take 10-15 minutes of manual scanning now resolve 3x as quickly."
  > Inference: "What normally requires an hour of Google searching now takes 10-20 minutes—an 80% reduction in research time."
  > Growth Marketing: "generates hundreds of new ads in minutes instead of hours."
  > Product Design: GitHub Actions로 PR 코멘트 자동화, Figma 파일에서 빌드하는 자율 루프.
  > 결론: 가장 성공한 팀은 Claude Code를 코드 생성기가 아니라 "thought partner"로 다룬다(페이지 요약 표현).
- 주의: 이 페이지에는 "Claude가 코드의 n%를 작성" 류의 수치 **없음**. 그 수치는 자료 24·25에 있다.
- 관련 섹션: 레슨 13 Maintain(장애 대응), 레슨 10(PR 코멘트 자동화 사례)

### 자료 24: How Anthropic secures its AI-native software development lifecycle
- 출처: https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle
- 저자·날짜: Jason Clinton, Deputy CISO, Anthropic. 2026-07-21. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 코스와 같은 6단계 프레임의 **보안 측** 실측치. Claude가 머지 코드의 약 80%를 작성, 엔지니어 분기당 산출 약 8배, 실질 리뷰 코멘트 PR 비율 16%→54%. "하드 게이트는 PreToolUse 훅이 아니라 CI에 둔다".
- 인용 가능한 구절:
  > "Claude authors about 80% of the code merged into our codebase today."
  > 엔지니어는 2021~2025 대비 분기당 약 8배 코드 출하(페이지 요약). 내부 Claude Tag가 전체 코드의 절반 이상을 머지.
  > 실질 리뷰 코멘트를 받은 PR 비율 16% → 54%.
  > 과거 claude.ai 장애 원인 버그의 약 1/3은 현 자동화 프로세스로 잡혔을 것.
  > Intercom: PR의 19% 자동 승인, 브레이킹 체인지 다운타임 35% 감소.
  > Code 단계: 보안 코딩 지침은 CLAUDE.md와 조직 스킬에; 에이전트가 PR 전에 `/security-review` 실행; "Some customers use a PreToolUse hook as a harder gate, but Anthropic places its hard code review gate in CI."
  > Test(CI): 여러 좁은 리뷰 에이전트가 PR마다 실행되고 "must prove their findings"; "Entire codebases have strict human approval processes."; 모든 승인 로깅, 위험 가중 샘플을 사람이 재검.
  > Monitor: 알림 트리아지 에이전트는 세 가지 권한만(문서 작성·채널 게시·프로덕션 로그 읽기), 수정 배포 불가.
  > 원칙: "Connect security agents to organizational context." / "Limit the blast radius (Principle of Least Agency)." / "Automated reviews are a different type of risk that is controlled differently." / "Dynamic testing should match deployment cadence." / "Give every agent a single-purpose identity with the minimum permissions for its job." / "The security engineer's job evolves from monitoring bugs to monitoring loops."
- 관련 섹션: 레슨 10(리뷰 레이어), 레슨 11(훅 vs CI 게이트 위치), 레슨 13(트리아지 에이전트 최소 권한), 서문(수치)

### 자료 25: Introducing Claude Tag
- 출처: https://www.anthropic.com/news/introducing-claude-tag
- 저자·날짜: Anthropic. 2026-06-23. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 코스 레슨 13 "Claude on call with Claude Tag"의 1차 출처. Slack 팀원으로 참여, 채널 범위 메모리, Enterprise/Team 베타, Opus 4.8 기반, 관리자 감사 로그·지출 한도.
- 인용 가능한 구절:
  > "available today in beta for Claude Enterprise and Team customers."
  > "@Claude learns over time." (채널에서 컨텍스트 축적; 비공개 채널 보고 안 함)
  > "Today, 65% of our product team's code is created by our internal version of Claude Tag."
  > "Claude Tag works with Opus 4.8."
  > 관리자: 채널별 도구·정보 접근 지정, 조직/채널별 토큰 지출 한도, "a log of everything @Claude has done, along with who requested each task"(페이지 요약)
- 주의: 코스 본문의 "incident channel first responder" 묘사는 발표 페이지에 직접 없음(2차 블로그 묘사). 개인·소규모 팀(Pro/Max)에는 해당 없음 — 책은 대안(Slack webhook → `claude -p`, 또는 Routines)으로 번역.
- 관련 섹션: 레슨 13

### 자료 26: 2026 Claude 모델 라인업·릴리스 노트 (agentic coding 관련)
- 출처: https://platform.claude.com/docs/en/about-claude/models/overview · https://platform.claude.com/docs/en/release-notes/overview
- 저자·날짜: Anthropic 공식 문서. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 2026-10 현재 라인업은 Fable 5.1 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5, 전부 1M 컨텍스트·128K 출력. 코스가 쓰인 2026-08 시점(Opus 4.8·Sonnet 5·Fable 5)과 다르다.
- 인용 가능한 구절 (릴리스 노트 원문):
  > 2026-10-07: "We've launched **Claude Haiku 5.5** (`claude-haiku-5-5`), our most capable model tuned for high-volume and latency-sensitive work. It has a 1M token context window, 128k max output tokens, and adaptive thinking"
  > 2026-09-28: "We've launched **Claude Sonnet 5.5** (`claude-sonnet-5-5`)."
  > 2026-09-22: "We've launched **Claude Opus 5.5** (`claude-opus-5-5`), a model for long-running agentic coding and knowledge work. It has a 1M token context window by default, 128k max output tokens, and always-on adaptive thinking, at $4 / $20 USD per MTok (Claude Opus 5 is $5 / $25)."
  > 2026-09-01: "We've launched **Claude Fable 5.1** (`claude-fable-5-1`), the successor to Claude Fable 5 for long-running agentic coding, knowledge work, and research ... at $10 / $50 USD per MTok"
  > 2026-06-30: "We've launched **Claude Sonnet 5** (`claude-sonnet-5`) ... at introductory pricing of $2 / $10 per MTok (made the standard price on August 10, 2026). ... Claude Sonnet 5 also uses a new tokenizer that produces approximately 30% more tokens for the same text."
  > 2026-06-09: "We've launched **Claude Fable 5** (`claude-fable-5`), our most capable model open to all customers, alongside **Claude Mythos 5** (`claude-mythos-5`) for Project Glasswing participants."
  > 2026-05-28: "We've launched **Claude Opus 4.8** ... On Claude Opus 4.8, the effort parameter defaults to `high` across all surfaces, including Claude Code and the Messages API."
  > 2026-04-16: "We've launched Claude Opus 4.7, our most capable model for complex reasoning and agentic coding, at the same $5 / $25 per MTok pricing as Opus 4.6." / "We've added the `xhigh` effort level on Claude Opus 4.7. `xhigh` sits between `high` and `max` and is tuned for long-running agentic and coding tasks (over 30 minutes) with token budgets in the millions."
  > 2026-03-13: "The 1M token context window is out of beta for Claude Opus 4.6 and Sonnet 4.6, at standard pricing."
  > 모델 표(현행): Fable 5.1 "For demanding reasoning and long-horizon agentic work" $10/$50 · Opus 5.5 "For long-running agentic coding and knowledge work" $4/$20 · Sonnet 5.5 "The best combination of speed and intelligence" $2/$10 · Haiku 5.5 "From $0.10 / input MTok" — 모두 "Context window 1M tokens / Max output 128K tokens / Reliable knowledge cutoff Jun 2026"
  > "If you're unsure which model to use, start with Claude Opus 5.5 for most workloads."
- 주의: 웹 검색에서 나온 SWE-bench Verified 수치(Opus 4.7 87.6%, Opus 4.8 88.6%, Sonnet 5 85.2%, Fable 5 95.0% 등)는 **3자 집계 사이트** 출처로 1차 확인 실패 → 본문 사용 금지, 필요하면 각 모델 "What's new" 페이지에서 fact-checker가 재확인.
- 관련 섹션: 서문(버전 기준), 레슨 9(모델 교체가 eval 트리거인 이유 — 2026년 한 해에 Opus 4.7→4.8→5→5.5, Sonnet 5→5.5 등 6회 이상 교체)

---

## C. SDLC·DevOps 측정 1차 소스

### 자료 27: DORA 네 가지(현 다섯 가지) 핵심 지표 정의
- 출처: https://dora.dev/guides/dora-metrics-four-keys/
- 저자·날짜: DORA (Google Cloud). 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: throughput(변경 리드타임·배포 빈도·실패 배포 복구 시간) vs instability(변경 실패율·배포 재작업률). MTTR → Failed Deployment Recovery Time으로 용어 변경, 4→5 지표.
- 인용 가능한 구절:
  > "Throughput is a measure of how many changes can move through the system over a period of time."
  > Change lead time: "The amount of time it takes for a change to go from committed to version control to deployed in production."
  > Deployment frequency: "The number of deployments over a given period or the time between deployments."
  > Failed deployment recovery time: "The time it takes to recover from a deployment that fails and requires immediate intervention."
  > "Instability is a measure of how well the software deployments go."
  > Change fail rate: "The ratio of deployments that require immediate intervention following a deployment."
  > Deployment rework rate: "The ratio of deployments that are unplanned but happen as a result of an incident in production."
  > 용어: "the move from MTTR to Failed Deployment Recovery Time" / "the original four keys" → "the current five-metric model"
- 관련 섹션: 레슨 12 "Lagging indicator: DORA measures", 레슨 13 control band 대상 지표, 책 전체 leading/lagging 프레임

### 자료 28: DORA 2024 — Accelerate State of DevOps Report 2024 (AI 도입 효과 수치)
- 출처: https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report (보고서 페이지 https://dora.dev/research/2024/dora-report/)
- 저자·날짜: Nathen Harvey(DORA Lead), Derek DeBellis(Researcher). 2024-10-23. 확인일 2026-10-19. **구버전 정보일 수 있음(2024)** — 2025·2026 보고서가 방향을 수정함(자료 29·30 참조).
- 신뢰성: 최상
- 핵심 주장: AI 도입 25% 증가 ↔ 문서 품질 +7.5%, 코드 품질 +3.4%, 리뷰 속도 +3.1%, 그러나 처리량 −1.5%, 안정성 −7.2%(추정). 응답자 39%는 AI 코드에 신뢰 거의 없음.
- 인용 가능한 구절:
  > "More than 75 percent of respondents said that they rely on AI for at least one daily professional responsibility."
  > "A 25% increase in AI adoption is associated with improvements in several key areas:" "7.5% increase in documentation quality" "3.4% increase in code quality" "3.1% increase in code review speed"
  > "However, despite AI's potential benefits, our research revealed a critical finding: AI adoption may negatively impact software delivery performance. As AI adoption increased, it was accompanied by an estimated decrease in delivery throughput by 1.5%, and an estimated reduction in delivery stability by 7.2%."
  > "39% of the respondents reported little to no trust in AI-generated code."
  > "Our data suggest that improving the development process does not automatically improve software delivery — at least not without proper adherence to the basics of successful software delivery, like small batch sizes and robust testing mechanisms."
  > "AI has positive impacts on many important individual and organizational factors which foster the conditions for high software delivery performance. But, AI does not appear to be a panacea."
  > dora.dev 보고서 페이지: "AI adoption significantly increases individual productivity, flow, and job satisfaction." / "However, it also negatively impacts software delivery stability and throughput."
- 관련 섹션: 레슨 1 "왜 프로세스가 병목인가"의 수치 근거, 레슨 8·12 "small batch + robust testing"

### 자료 29: DORA 2025 — State of AI-assisted Software Development
- 출처: https://blog.google/technology/developers/dora-report-2025/ (보고서 페이지 https://dora.dev/research/2025/dora-report/, 역량 모델 https://dora.dev/ai/capabilities-model/report/)
- 저자·날짜: Ryan J. Salva (Google Cloud). 2025-09-23. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 약 5,000명 조사. AI 도입 90%(+14%p), 하루 중앙값 2시간. 2024와 달리 **처리량과는 양의 연관**, 그러나 불안정성도 함께 증가(자료 30 "balancing" 글에서 명시). "AI는 거울이자 증폭기". 7개 팀 유형, 7개 역량 모델.
- 인용 가능한 구절:
  > "nearly 5,000 technology professionals globally."
  > "AI adoption among software development professionals has surged to 90%, marking a 14% increase from last year." / "a median of two hours daily to working with it."
  > "AI adoption is now linked to higher software delivery throughput, meaning teams are releasing more software and applications." / "the ongoing challenge remains of ensuring software works as intended before it's delivered to users."
  > AI "can act as a 'mirror and a multiplier.'" / "In cohesive organizations, AI boosts efficiency. In fragmented ones, it highlights weaknesses."
  > dora.dev 보고서 페이지: "AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses." / "The greatest returns on AI investment come not from the tools themselves, but from a strategic focus on the underlying organizational system."
  > 역량 모델 페이지: "serves as a practical guide to the seven capabilities that amplify the benefits of AI." (Last updated: November 25, 2025)
  > 팀 유형 예: "Harmonious high-achievers", "Legacy bottleneck" (전체 7종 이름은 보고서 본문·인포그래픽에만 있어 미확인)
- 주의: 7개 역량 이름(clear AI stance, healthy data ecosystems, AI-accessible internal data, strong version control practices, working in small batches, user-centric focus, quality internal platforms)은 2차 자료(InfoQ·LeadDev 등)에서 반복되지만 이번 fetch에서 1차 페이지 원문으로는 확인 못 함 → fact-checker가 보고서 PDF로 대조.
- 관련 섹션: 레슨 1(2024→2025 변화), 레슨 13(측정의 조직적 맥락), 레슨 5·6(version control·small batches 역량과 CLAUDE.md/plan.md 연결)

### 자료 30: DORA 2026 — "Balancing AI tensions" 인사이트 + ROI of AI-assisted Software Development 보고서
- 출처: https://dora.dev/insights/balancing-ai-tensions/ (1차) · https://dora.dev/ai/roi/report/ (1차 안내 페이지) · https://www.infoq.com/news/2026/05/dora-roi-ai-assisted-dev-report/ (2차 요약)
- 저자·날짜: Balancing — Jessica Baolin, Nathen Harvey, 2026-03-10. ROI 보고서 — Google Cloud DORA, "2026.01" 판(dora.dev 페이지 Last updated 2026-04-22). InfoQ — Matt Saunders, 2026-05-11. 확인일 2026-10-19.
- 신뢰성: 최상(dora.dev) / 중(InfoQ 요약, 수치는 보고서 PDF 대조 필요)
- 핵심 주장: "AI 도입 ↑ = 처리량 ↑ **그리고** 불안정성 ↑"가 공식 문구. 대응책은 작은 배치·테스트 자동화(수동 리뷰 최적화보다 ROI 높음). ROI 보고서는 J-curve(학습·검증세로 일시 하락), 리뷰 병목, 변경실패율 가정 5%→6%.
- 인용 가능한 구절:
  > (dora.dev, 2026-03-10) "higher AI adoption is associated with an increase in both software delivery throughput and software delivery instability."
  > "Enforcing the discipline of working in small batches is a critical countermeasure to the risks of AI-assisted development."
  > "Forcing large AI-generated changes into reviewable, testable units"
  > "Velocity gains for an individual author frequently translate into a significantly increased cognitive load" (리뷰어에게)
  > "Investing in robust test automation for faster feedback may provide a better return on investment" (수동 리뷰 최적화 대비)
  > (InfoQ 요약, 보고서 인용) Nathen Harvey: "Without this foundation, AI creates localized pockets of productivity that are often lost in downstream chaos." / "The greatest returns on AI investment come not from the tools themselves"
  > (InfoQ 요약) J-curve를 "the tuition cost of transformation"이라 부름; 500인 조직 예시 모델 $11.6M 수익 vs $8.4M 투자(ROI 39%, 회수 약 8개월); "Treat these calculations as a high-uncertainty estimate meant to spark a conversation."; 샘플 계산기의 변경실패율 가정 5%→6%.
- 관련 섹션: 레슨 8(테스트 자동화 ROI), 레슨 10(리뷰어 인지 부하 → AI 리뷰 레이어 정당화), 레슨 4·7(작은 배치 = plan 단위 분할)

### 자료 31: SPACE 프레임워크
- 출처: 원문 https://queue.acm.org/detail.cfm?id=3454124 (403으로 직접 fetch 실패) · 저자 소속 페이지 https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/ · 해설 https://github.blog/enterprise-software/devops/measuring-enterprise-developer-productivity/
- 저자·날짜: Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Tom Zimmermann, Brian Houck, Jenna Butler. ACM Queue, Vol 19(1), pp. 20–48, 2021-02. GitHub Blog 해설: Kevin Alwell, 2021-03-10(2022-02-04 수정). 확인일 2026-10-19. **구버전 정보일 수 있음(2021)** — 프레임워크 자체는 변하지 않음.
- 신뢰성: 최상(원문·저자 기관) / 중(GitHub Blog 해설)
- 핵심 주장: 생산성은 단일 지표로 못 잰다. 5차원 S/P/A/C/E. 최소 3차원, 지각(설문) 측정 포함.
- 인용 가능한 구절:
  > (MS Research 요약) "Developer productivity is about more than an individual's activity levels" / "it cannot be measured by a single metric or dimension." / "The SPACE framework captures different dimensions of productivity"
  > (GitHub Blog) 5차원: "S – Satisfaction & Well Being / P – Performance / A – Activity / C – Collaboration & Communication / E – Efficiency & Flow"
  > (GitHub Blog, Forsgren et al. 인용) "Performance is the outcome of a system or process." / "Activity is a count of actions or outputs completed in the course of performing work."
  > (GitHub Blog) "No single measure can be taken alone to draw conclusions about productivity. Teams and organizations should leverage at least three of the dimensions to gain deeper insight into how your teams are working."
- 코스와의 연결: 코스의 leading(과정) / lagging(결과) 지표는 SPACE의 Activity·Efficiency(선행)와 Performance(지연)에 대응. 코스 레슨 7 "share of the day spent steering rather than waiting"은 Efficiency & flow 차원.
- 관련 섹션: 레슨 13 측정 프레임, 서문 "무엇을 재지 말 것인가"

### 자료 32: Accelerate (Forsgren·Humble·Kim, 2018)
- 출처: https://itrevolution.com/product/accelerate/
- 저자·날짜: Nicole Forsgren, Jez Humble, Gene Kim. 2018-03-27. 확인일 2026-10-19. **구버전 정보일 수 있음(2018)** — DORA 지표의 원전으로만 인용.
- 신뢰성: 최상(출판사 페이지)
- 핵심 주장: 네 가지 핵심 지표의 뿌리. 4년간 State of DevOps 연구에 기반.
- 인용 가능한 구절:
  > 제목: "Accelerate: The Science of Lean Software and DevOps: Building and Scaling High Performing Technology Organizations"
  > "Through four years of groundbreaking research" / "rigid statistical methods to measure software performance and what drives it." / "The famously dubbed DORA metrics."
- 관련 섹션: 참고문헌, 레슨 12·13 각주

---

## D. 업계 비교 (공식 문서 기준, 간략)

### 자료 33: GitHub Copilot coding agent / cloud agent
- 출처: https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks · https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent (현재 "Copilot cloud agent"로 리브랜딩된 페이지)
- 저자·날짜: GitHub Docs. 날짜 미표기. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 이슈 할당/채팅/PR에서 시작, 클라우드 임시 환경에서 작업, 작업당 PR 1개. 지침 파일로 `copilot-instructions.md`, `**/AGENTS.md`, `/CLAUDE.md`, `/GEMINI.md`를 읽음(=CLAUDE.md가 사실상 공용 포맷). `copilot-setup-steps.yml`로 환경 준비. `@copilot` 코멘트로 반복.
- 인용 가능한 구절:
  > "Copilot cloud agent can research a repository, plan changes, and implement them in the background." / "an ephemeral cloud development environment, rather than your local IDE."
  > "Copilot can only work on one branch at a time and can open one pull request per task."
  > "If a ruleset or branch protection rule is incompatible with Copilot cloud agent, access to the agent is blocked."
  > 좋은 과제: "A clear description of the problem to be solved or the work required." / "Complete acceptance criteria on what a good solution looks like (for example, should there be unit tests?)." / "Directions about which files need to be changed."
  > "Copilot cloud agent supports a number of different types of custom instructions files:" `/.github/copilot-instructions.md`, `/.github/instructions/**/*.instructions.md`, `**/AGENTS.md`, `/CLAUDE.md`, `/GEMINI.md`
  > "You can configure a `copilot-setup-steps.yml` file to pre-install these dependencies before the agent starts working"
  > "Mention `@copilot` in comments on the pull request." / "Copilot only responds to comments from people who have write access to the repository."
  > 과제 선택: "Tasks involving security, personally identifiable information, authentication repercussions" 는 사람이 직접.
- 비교 포인트: 코스의 spec.md/plan.md에 해당하는 것이 Copilot에서는 "잘 쓴 이슈 + acceptance criteria". 훅 같은 결정론적 게이트 개념은 없고 브랜치 보호에 의존.
- 관련 섹션: 레슨 3·4(스펙 입력 비교), 레슨 10(에이전트 PR 반복)

### 자료 34: OpenAI Codex GitHub Action (CI 리뷰)
- 출처: https://learn.chatgpt.com/docs/github-action (developers.openai.com/codex/github-action 에서 308 리다이렉트)
- 저자·날짜: OpenAI Docs. 날짜 미표기. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: `openai/codex-action@v1`이 Codex CLI를 설치하고 `codex exec`를 실행. 샌드박스 3값, `safety-strategy` 기본 `drop-sudo`. PR 리뷰 예시는 두 잡(리뷰 → 코멘트 게시).
- 인용 가능한 구절:
  > "run Codex in CI/CD jobs, apply patches, or post reviews from a GitHub Actions workflow."
  > 액션: "openai/codex-action@v1" / 입력 `prompt` 또는 `prompt-file`("Inline instructions or a repository path to Markdown or text with your task."), `codex-args`, `model`, `effort`, `sandbox`, `safety-strategy`(기본 `drop-sudo`), `output-file`, `allow-users`, `allow-bots`
  > `sandbox` 값: `workspace-write`, `read-only`, `danger-full-access`
  > 예시 "Codex pull request review": `pull_request`(opened, synchronize, reopened) → `prompt-file: .github/codex/prompts/review.md`, `output-file: codex-output.md` → 두 번째 잡이 PR 코멘트로 게시.
- 비교 포인트: Claude의 `--permission-mode dontAsk` + `--allowedTools` ↔ Codex의 `sandbox` + `safety-strategy`. AGENTS.md 사용 여부는 이 페이지에 없음(AGENTS.md 문서는 404로 미확인).
- 관련 섹션: 레슨 10·12 비교 박스

### 자료 35: Cursor — Rules와 Bugbot
- 출처: https://cursor.com/docs/context/rules · https://cursor.com/docs/bugbot
- 저자·날짜: Cursor Docs. 날짜 미표기. 확인일 2026-10-19.
- 신뢰성: 최상
- 핵심 주장: 규칙은 `.cursor/rules/*.mdc`(+AGENTS.md 지원), 4유형, 500줄 이하 권장. **Bugbot(PR 리뷰)은 `.cursor/rules`를 읽지 않고 `.cursor/BUGBOT.md`를 읽음** — Claude Code의 "CLAUDE.md(세션) vs REVIEW.md(리뷰)" 분리와 같은 구조. Autofix는 Cloud Agent를 스폰.
- 인용 가능한 구절:
  > "Stored in `.cursor/rules`, version-controlled and scoped to your codebase." / "Project rules must use the `.mdc` extension." / "Cursor supports AGENTS.md in the project root and subdirectories."
  > 유형: Always Apply · Apply Intelligently · Apply to Specific Files · Apply Manually (frontmatter `description`, `globs`, `alwaysApply`)
  > "Keep rules under 500 lines." / "Split large rules into multiple, composable rules."
  > "Bugbot reviews pull requests and identifies bugs, security issues, and code quality problems." / "It runs automatically on each PR update or manually when triggered."
  > "Create `.cursor/BUGBOT.md` files to provide project-specific context for reviews." / "Bugbot always includes the root `.cursor/BUGBOT.md` file"
  > "Cursor project rules (`*.mdc` files in `.cursor/rules/`) do not apply to Bugbot runs."
  > "Bugbot Autofix automatically spawns a Cloud Agent to fix bugs found during PR reviews." / 수동 트리거: "commenting `cursor review` or `bugbot run` on any PR" / "Bugbot uses usage-based billing."
- 관련 섹션: 레슨 5(규칙 파일 비교), 레슨 10(리뷰 전용 지침 파일 패턴의 업계 수렴)

---

## E. 한국어 자료 (SDLC 프로세스 변화 중심)

### 자료 36: 토스 테크 — Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기
- 출처: https://toss.tech/article/harness-for-team-productivity
- 저자·날짜: 김용성 (토스페이먼츠 Node.js Developer). 2026-02-26. 확인일 2026-10-19.
- 신뢰성: 최상(회사 엔지니어링 블로그)
- 핵심 주장: 같은 LLM이라도 "작업 전 컨텍스트 설계" 여부로 결과 차이가 크다. 개인 역량에 맡기지 말고 Claude Code 플러그인(Hook·slash command)으로 팀 워크플로를 배포해 조직의 **저점(floor)**을 올린다. 플러그인 = "실행 가능한 SSOT". 예: main 커밋 시 feature 브랜치 생성 유도 Hook, `/new-feature` 하나로 Jira 이슈→브랜치→계획 승인→PR. 지식은 Global/Domain/Local 3계층. 정량 수치 없음.
- 인용 가능한 구절:
  > "현재 많은 개발팀이 LLM을 도입하고 있지만, 냉정하게 들여다보면 그것은 '각자도생'에 가깝습니다."
  > "차이는 단 하나, 작업 전에 컨텍스트를 설계했느냐의 여부입니다." / "이것은 코딩 실력의 차이가 아닙니다."
  > "문서 관리의 패러다임이 '기록'에서 '실행'으로 바뀌는 셈입니다."
  > "플러그인 코드가 업데이트되면, 팀원들의 에이전트 행동 양식도 즉시 업데이트됩니다."
  > "기존의 린터(Linter)가 단순히 에러를 뱉고 차단했다면, 플러그인은 팀의 규율에 맞게 행동을 교정(Align)해주는 가이드 역할을 수행할 수 있습니다."
  > "B 엔지니어도 `/new-feature` 하나로 A 엔지니어와 동일한 품질의 워크플로우를 실행하게 됩니다."
  > "결국 이 모든 흐름이 향하는 곳은 '우리 조직에 최적화된 하네스(Harness)의 구축'이라고 생각합니다."
- 관련 섹션: 레슨 5·6(CLAUDE.md/스킬을 "실행 가능한 SSOT"로), 레슨 6 훅 가드레일의 한국 사례, 레슨 2~4 intent→plan 흐름의 slash command화

### 자료 37: 토스 테크 — 개발자는 AI에게 대체될 것인가
- 출처: https://toss.tech/article/will-ai-replace-developers
- 저자·날짜: 정세훈 (토스 Node.js Developer). 2026-01-21. 확인일 2026-10-19.
- 신뢰성: 최상(회사 엔지니어링 블로그; 단 인용 수치는 외부 조사)
- 핵심 주장: 위임 = 업무의 추상화. "무엇을 위임할지"는 사람이 정한다. 판단·맥락·조율·최종 책임은 사람. 플랫폼은 되돌릴 수 있는 변경·명확한 diff·승인 단계를 제공해야. 주니어 견습 사다리 붕괴 우려.
- 인용 가능한 구절:
  > "AI에게 특정 역할을 위임한다는 것은 결국 업무를 추상화하는 행위입니다."
  > "잘못된 추상화는 추상화가 없는 것보다 더 나쁩니다."
  > "'위임하기 어려운 것'은 고정된 속성이 아니라, 기술 발전에 따라 계속 이동하는 일시적인 경계일 뿐입니다."
  > "AI가 대신할 수 없었던 판단, 맥락, 조율의 지점을 의식적으로 인식해야 합니다."
  > "'위임해야 하는가, 하면 안 되는가'는 우리가 결정해야 합니다."
  > "결과적으로 AI가 모든 인력을 대체하는 것이 아니라, 견습 사다리를 제거하고 있습니다."
- 관련 섹션: 레슨 1 "Humans remain accountable", 레슨 11 승인 게이트의 철학, 운영자 학습 루프(주니어/견습) 각주

### 자료 38: LY Corporation(LINE) Tech-Verse 2026 — 멀티 에이전트 협업으로 재설계하는 개발 프로세스
- 출처: https://techblog.lycorp.co.jp/ko/techverse2026-219
- 저자·날짜: LY Corporation 기술 블로그(Tech-Verse 2026 공식 기사, 행사 2026-06-29). 발표자 미표기(페이지 하단 Mac Van Duy, Ngo Xuan Trinh 소개). 확인일 2026-10-19.
- 신뢰성: 최상(회사 엔지니어링 블로그)
- 핵심 주장: 병목은 코드 생성이 아니라 "의도→스펙, 검증, 리뷰 준비"의 사람 조율. proposer/challenger 에이전트 토론 + orchestrator. 스펙·빌드·전달 3단계. 사람은 시작(의도)·끝(승인)·에스컬레이션에만 개입. 정량 결과 없음.
- 인용 가능한 구절:
  > "AI 코딩에서 어려운 점은 더 이상 코드를 생성하는 것이 아닙니다." / "진짜 어려운 부분은 그 밖의 모든 과정입니다."
  > "기본적으로 사람은 전략적인 단계에서만 개입합니다."
  > "최종 판단은 여전히 사람 엔지니어가 내리지만, 이제 각 단계 간 인수인계를 수동으로 조율할 필요는 없습니다."
  > "스펙이 부실하면 전체 파이프라인도 부실해집니다."
  > "신뢰는 우연에 기대는 리뷰가 아니라 반복 가능한 통제에서 나옵니다."
  > "목표는 시스템이 항상 옳다고 가장하는 것이 아닙니다."
- 관련 섹션: 레슨 1(병목 재정의), 레슨 3(spec 단계 질문), 레슨 8(verifier를 "challenger"로), 레슨 13(confidence gate between stages)

### 자료 39: GeekNews — Claude Code로 좋은 결과 얻기 / Claude Code 6주 사용기
- 출처: https://news.hada.io/topic?id=22425 (원문 https://www.dzombak.com/blog/2025/08/getting-good-results-from-claude-code/) · https://news.hada.io/topic?id=22375 (원문 https://blog.puzzmo.com/posts/2025/07/30/six-weeks-of-claude-code/)
- 저자·날짜: GN⁺ 요약, 2025-08-09 / 2025-08-07 (원문 2025-08 / 2025-07-30). 확인일 2026-10-19. **구버전 정보일 수 있음(2025)** — 기능 설명이 아닌 프로세스 교훈이라 인용 가치 유지.
- 신뢰성: 중(커뮤니티 요약; 원문은 개인 블로그)
- 핵심 주장: 좋은 결과 = 명확한 사양서 + 빌드/린트/테스트 문서화 + 에이전트 자체 리뷰 + `~/.claude/CLAUDE.md`의 개인 규칙(TDD, 3회 시도 제한). 최종 품질 책임은 PR에 이름이 들어가는 사람. 6주 사용기: 기술 부채가 "일정 확보→대규모 투입" 공식에서 벗어남, "Post-Junior" 수준 보조.
- 인용 가능한 구절:
  > (22425) "명확한 사양서 작성" / "프로젝트 구조 문서화" / "프로페셔널 환경에서는 PR에 자신의 이름이 들어가는 이상, **최종 품질 책임은 본인**에게 있다고 강조" / "AI 생성 코드는 종종 **논리적 오류**, **성능 저하**, **불완전한 테스트** 등의 문제가 있음"
  > (22375) "Claude Code는 **'Post-Junior(숙련 주니어 이상)' 수준의 보조 프로그래머**" / "**설계/품질/최종 컨트롤은 인간 엔지니어**가 담당" / "기존의 '기술 부채는 일정 확보→대규모 투입' 공식이 깨지고"
  > 댓글(22375, zxavi 2025-08-07): "$200 결제하고 한시간만에 4년짜리 난제를 해결했습니다."
- 관련 섹션: 레슨 2~3(개인판 intent/spec), 레슨 5(개인 `~/.claude/CLAUDE.md`), 레슨 10(책임 소재)

### 자료 40: GPTers — 챗봇처럼 쓰던 Claude Code, '한 팀처럼' 일하게 만든 후기
- 출처: https://www.gpters.org/nocode/post/review-claude-code-used-66bvFFIDz2WN8U4
- 저자·날짜: 갓생오리 (지피터스). 페이지 표기 "4달 전"(≈2026-06). 확인일 2026-10-19.
- 신뢰성: 중(커뮤니티 후기)
- 핵심 주장: PM 1 + 전문 에이전트 6(planner, software-architect, ui-designer, android-developer, code-reviewer, qa) 구조. "한 워크스페이스 = 한 프로젝트". 반복 지시는 방침으로 고정, 자주 쓰는 작업은 스킬로. 단계별 승인 게이트 + 하네스 파일 커밋 차단 pre-commit 훅. 설정 파일이 길면 인식 저하.
- 인용 가능한 구절:
  > "워크스페이스는 하나의 프로젝트에 대해서만 책임지고 동작해야 한다"
  > "매번 같은 설명을 반복해야 했습니다." / "한 번 정해두니 다음부터는 안 알려줘도 에이전트가 알아서 지킵니다."
  > "AI 한 명에게 모든 걸 시키니 역할이 섞이고 결과가 들쭉날쭉했거든요."
  > "혼자 다 쓰지 않고, 각 파일마다 AI와 대화하면서 \"무엇을 넣으면 좋을지, 뺄지\" 토론하며 한 줄 한 줄 채워나갔습니다."
  > "설정 파일이 너무 길면 AI가 제대로 인식하지 못할 수 있어서 분량을 조절했습니다."
- 관련 섹션: 레슨 5(CLAUDE.md 길이), 레슨 6(스킬화 기준), 레슨 7(역할별 서브에이전트), 레슨 11(개인 수준 승인 게이트)

### 자료 41: HEROPY — Claude Code 핵심 정리
- 출처: https://www.heropy.dev/p/4weJmr
- 저자·날짜: HEROPY.DEV (박영웅). 날짜 미표기. 확인일 2026-10-19.
- 신뢰성: 중(확인된 저자의 개인 기술 블로그; 공식 문서 요약 성격)
- 핵심 주장: CLAUDE.md 로드 순서(User→Project→Local), 모순 지침 금지, 플랜 모드 = 읽기 전용, PreToolUse로 위험 명령 차단, 서브에이전트 = 컨텍스트 오염 방지, 팀 공유는 `.claude/settings.json` 커밋 + local/`CLAUDE.local.md`는 gitignore.
- 인용 가능한 구절:
  > "CLAUDE.md는 Claude Code가 프로젝트에 대한 지침과 컨텍스트를 기억하는 메모리 파일입니다."
  > "따라서 모순되는 지침이 없도록 관리해야 합니다."
  > "Hooks는 Claude Code의 생명주기 특정 시점에 자동으로 실행되는 사용자 정의 셸 명령 또는 LLM 프롬프트입니다."
  > "특히 도구 실행 전에 동작하는 `PreToolUse`는 실행 자체를 막을 수 있어서 위험한 명령을 차단하는 데 사용합니다."
  > "Sub Agents는 특정 작업을 위한 전문화된 독립 AI 어시스턴트입니다."
  > "프로젝트 설정(`.claude/settings.json`): 팀 전체가 공유해야 하는 권한 규칙, 허용된 도구 등을 정의합니다."
- 관련 섹션: 한국어 용어 표기 참고(훅/서브에이전트/플랜 모드/승인 모드), 레슨 5·7·11

### 자료 42: 브런치 — CLAUDE.md 완전 정복 01화
- 출처: https://brunch.co.kr/@aideveloper/273
- 저자·날짜: 에이전트김 (@aideveloper). 2026-03-20. 확인일 2026-10-19.
- 신뢰성: 중(개인 블로그)
- 핵심 주장: "README는 사람이, CLAUDE.md는 AI가 읽는 문서". 3줄로 시작해 키워라. 구체적·실행 가능한 지시. 프로젝트 파일은 Git 공유, 개인 파일은 로컬.
- 인용 가능한 구절:
  > "README는 사람이 읽는 문서입니다." / "CLAUDE.md는 AI가 읽는 문서입니다."
  > "처음부터 완벽한 CLAUDE.md를 만들려고 할 필요는 없습니다."
  > "CLAUDE.md에는 AI가 작업 판단에 실제로 활용할 수 있는 구체적이고 실행 가능한 지시를 담아야 합니다."
  > "이 파일은 Git으로 버전을 관리하며, 팀 멤버 누구나 같은 규칙으로 Claude Code를 사용할 수 있게 합니다."
- 관련 섹션: 레슨 5 오프닝 비유 후보

---

## F. 코스 본문 ↔ 현행 문서 차이 요약 (fact-checker용 표)

| 코스 표현 (2026-08 기준) | 현행 문서 (2026-10-19, v2.1.303) | 출처 |
|---|---|---|
| "managed Code Review (research preview)" | "research preview" 라벨 없음. Team/Enterprise 플랜. `/code-review`는 모든 플랜 | 자료 12 |
| `/review`로 PR 리뷰 | `/review`는 `/code-review` 별칭(v2.1.223+) | 자료 13 |
| auto mode는 선택 기능처럼 서술 | v2.1.283+ 대화형 세션 기본 시작 모드 | 자료 8 |
| `permissionDecision` allow/ask/deny | + `defer` | 자료 1 |
| 훅 = 스크립트(command) | 5종: command/http/mcp_tool/prompt/agent | 자료 1·2 |
| "organization-level slash command" | 커맨드는 스킬에 통합, 새 작업은 SKILL.md 권장 | 자료 3 |
| `requiredMinimumVersion: "2.1.193"` | 최신 2.1.303 | 자료 18 |
| "OpenTelemetry export"로 세션 수·훅 결정 집계 | 메트릭 `claude_code.session.count`, 이벤트 `tool_decision(source="hook")` | 자료 16 |
| 모델: Opus 4.8·Sonnet 5·Fable 5 시대 | Fable 5.1 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5 | 자료 26 |
| `--bare`는 CLAUDE.md·스킬·훅 건너뜀 | 동일 + MCP·백그라운드 작업도 제한(v2.1.286), "-p 기본값이 될 예정" | 자료 6 |
| DORA 2024: AI 도입 ↑ → 처리량 −1.5%, 안정성 −7.2% | DORA 2025/2026: 처리량 ↑ **그리고** 불안정성 ↑ | 자료 28·29·30 |

---

## 수집 한계
- 접근 실패한 자료: ACM Queue SPACE 원문(403) — MS Research·GitHub Blog로 대체; GitHub Copilot "about coding agent" 구 URL(404, cloud agent로 리브랜딩됨); OpenAI Codex AGENTS.md 문서(404); 아임웹 Medium 팀 도입기(403); wikidocs @jaehong "에이전틱 코드 리뷰"(403, 146 PR·4도구 실험 원출처 미확인); youngju.dev 두 글(본문 비어 있음); 토스 "Data First, AI Native" 커리어 글(본문 비어 있음); 우아한형제들·카카오·네이버 D2에서 Claude Code 도입기 **검색 결과 없음**(사람 중심 코드리뷰 문화 글만 존재).
- 1차 원문 미확인 수치: DORA 2025 "7개 역량" 이름, DORA 2026 ROI 보고서 수치(InfoQ 2차), 2026 모델별 SWE-bench 점수(3자 집계) — 본문 사용 전 PDF/모델 페이지 대조 필요.
- 의도적으로 제외: 커뮤니티 토론(Reddit/HN/GeekNews 댓글 다수)과 논문은 다른 리서처 담당. 강의 판매 페이지·날짜 없는 나열형 가이드(wikidocs 일반 가이드, lilys 요약 등)는 제외. Claude Design·Cowork(코스 레슨 2~3 언급)은 비개발자 도구라 이 책 범위 밖으로 보고 수집하지 않음.
