# 웹 리서치: Harness Engineering for Agentic Coding Tools

수집일: 2026-04-20. 대상 독자: 하네스 엔지니어링을 학습·실무에 적용하려는 개발자.
우선순위: 공식 문서(Anthropic, OpenAI) > 1차 저자 블로그(Huntley, Karpathy, HumanLayer, Cline) > 커뮤니티 요약.

---

## 1. Claude Code 하네스 메커니즘

### 1.1 CLAUDE.md / AGENTS.md / GEMINI.md 규약

- 공식 문서: https://code.claude.com/docs/en/memory — CLAUDE.md는 프로젝트 루트에서 상향 트래버스하며 모든 레벨이 병합되어 컨텍스트에 삽입된다(추가적, 비대체적).
- AGENTS.md 표준: https://agents.md/ — Linux Foundation 산하 Agentic AI Foundation이 관리하는 오픈 스탠다드. Claude Code, Codex, Gemini CLI, Cursor, Copilot이 공통 인식. 60,000+ OSS 프로젝트가 채택. "closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."
- 비교 가이드: https://thepromptshelf.dev/blog/cursorrules-vs-claude-md/ — 실무자들은 "AGENTS.md가 사실상 유니버설 스탠다드"라고 평가.
- 대형 모노레포 패턴: https://dev.to/myougatheaxo/claude-code-in-monorepos-hierarchical-claudemd-and-package-scoped-instructions-1il9 — 루트 CLAUDE.md는 "시스템이 어떻게 맞물리는지" 설명(connective tissue), 패키지별 CLAUDE.md는 프레임워크 특정 규약. 깊은 파일이 우선.
- Virtual Monorepo 패턴: https://medium.com/devops-ai/the-virtual-monorepo-pattern-how-i-gave-claude-code-full-system-context-across-35-repos-43b310c97db8 — 35개 개별 repo를 로컬 디렉터리에 같이 두고 상위 CLAUDE.md로 시스템 전체 맥락을 주입.

핵심 실천:
- 60줄 미만 유지(공식 가이드 권장). "라우터"로 설계, 상세는 skill/subagent로 분산.
- 팀 공유: `.claude/settings.json` + 루트 CLAUDE.md는 커밋, `.claude/settings.local.json`은 gitignore.
- 중첩 규칙: 구체성이 높을수록 하위 디렉터리에 배치.

Gotcha:
- 조직 단위에서는 CLAUDE.md 업데이트가 드리프트의 주요 원인. PR 리뷰 체크리스트에 "규약 변경 시 CLAUDE.md 업데이트" 항목 추가 필요.
- 바이트 한도(32 KiB in Codex, `project_doc_max_bytes`) 초과 시 조용히 잘림.

### 1.2 Subagents

- 공식 문서: https://code.claude.com/docs/en/sub-agents
- 모범 사례: https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/

프런트매터 필드: `name`, `description`(필수), `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`.

핵심 규칙:
- `tools` 생략 시 부모 스레드의 모든 툴(MCP 포함) 상속. 타이트한 통제를 위해서는 반드시 화이트리스트.
- `description`이 자동 위임의 기반. 구체적인 트리거 시나리오를 명시해야 Claude가 적절히 호출.
- `isolation: worktree`로 독립 파일시스템 복사본 → 병렬 실행 시 충돌 제거.
- 컨텍스트 오염 방지: "탐색·로그가 메인 스레드를 더럽히지 않도록" 격리된 컨텍스트로 푸시.

### 1.3 Slash commands와 Skills

- 공식 Skills 문서: https://code.claude.com/docs/en/skills
- 요약: https://www.producttalk.org/how-to-use-claude-code-features/

실무 정리:
- `.claude/commands/*.md`와 `.claude/skills/*/SKILL.md`는 이제 동일한 `/slash-command` 인터페이스로 통합.
- Slash command = 사용자 호출, 단일 파일 프롬프트.
- Skill = 모델이 자동 호출, 다중 파일(스크립트·템플릿 포함), 프런트매터로 `disable-model-invocation`, `user-invocable`, `allowed-tools` 제어.
- **Output styles(`/output-style`)는 v2.1.73에서 deprecated**. 더 이상 권장되지 않음.
- Plan mode(`/plan` 또는 Shift+Tab): Explore-스타일 subagent에 리포지토리 스캔을 위임해 메인 스레드 토큰 보호.

### 1.4 Hooks

1차 출처: https://code.claude.com/docs/en/hooks-guide — 전체 이벤트 스키마 포함.

이벤트 목록(v2.1 기준):
`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `Elicitation`, `ElicitationResult`, `SessionEnd`.

통신 규약(인용, 원문):
> "Exit 0: the action proceeds… Exit 2: the action is blocked. Write a reason to stderr, and Claude receives it as feedback so it can adjust."

핵심 실용 예(공식 문서에서 직접 발췌):
- 보호 파일 차단(PreToolUse):
  ```bash
  PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")
  # … matches → exit 2 with stderr message
  ```
- 컴팩션 후 컨텍스트 재주입(SessionStart + `matcher: "compact"`).
- PermissionRequest를 JSON으로 자동 승인(`{"decision":{"behavior":"allow"}}`).
- Hook 3종: `"type": "command"` / `"http"` / `"prompt"`(Haiku 판정) / `"agent"`(서브에이전트 검증, 기본 60초, 최대 50턴).

보안 관점:
> "A hook that returns permissionDecision: 'deny' blocks the tool even in bypassPermissions mode or with --dangerously-skip-permissions. This lets you enforce policy that users cannot bypass."
— 즉, PreToolUse hook은 Ralph-스타일 자율 루프에서도 파괴적 명령 게이트로 쓸 수 있는 **유일한 강제 지점**.

Gotcha:
- Stop hook 무한 루프: `stop_hook_active` 필드를 읽어 조기 return하지 않으면 continue 폭주.
- 쉘 프로필(`~/.zshrc`)의 무조건 `echo`가 hook JSON 출력 앞에 섞여 JSON 파싱 실패 → `[[ $- == *i* ]]` 가드.
- `PermissionRequest`는 non-interactive(-p) 모드에서 fire 안 함 → 자동화에선 `PreToolUse`로 대체.

### 1.5 MCP 서버 통합과 권한 모델

- 공식: https://code.claude.com/docs/en/mcp
- 보안: https://prefactor.tech/blog/how-to-secure-claude-code-mcp-integrations-in-production, https://modelcontextprotocol.io/specification/draft/basic/security_best_practices

이중 방어(인용):
> "Even if a server is configured, Claude cannot use its tools without explicit permission. (…) allowing mcp__github__* grants access to all tools from the github MCP server."

핵심:
- 툴 이름 규약 `mcp__<server>__<tool>`. 패턴 허용/거부 가능.
- 기본적으로 WebSearch, WebFetch는 security상 비활성. `allowedTools`에 추가해야 활성.
- OAuth 2.1 + PKCE, capability-level scope 권고. PAT를 env var에 박는 방식은 오픈소스 MCP 서버의 50%+에서 아직 쓰이는 레거시 패턴이며 위험.

### 1.6 settings.json 스코프와 권한

- 공식: https://code.claude.com/docs/en/settings

스코프 계층:
1. User: `~/.claude/settings.json` (모든 프로젝트).
2. Project committed: `.claude/settings.json`.
3. Project local: `.claude/settings.local.json`(gitignore).
4. Managed policy settings(엔터프라이즈, 최우선).

평가 순서: deny → ask → allow. 첫 매치 승. Array 설정(allow/deny 배열)은 스코프 간에 concat·dedupe되어 병합. 프로젝트 deny가 user allow를 항상 이김.

---

## 2. Codex CLI 하네스 메커니즘

### 2.1 AGENTS.md 조회 순서

출처: https://developers.openai.com/codex/guides/agents-md

Codex 조회 순서(세션 시작 시 한 번):
1. Global: `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md`.
2. Project: 루트→현재 디렉터리 각 레벨에서 `AGENTS.override.md` → `AGENTS.md` → `project_doc_fallback_filenames`의 fallback들. 해당 레벨에서 첫 번째 비어있지 않은 파일만 사용.
3. 누적 바이트가 `project_doc_max_bytes`(기본 32 KiB) 도달 시 추가 중단.
4. 루트→current로 내려가면서 concat, 뒤가 우선.

### 2.2 Sandbox와 Approval 모드

출처: https://developers.openai.com/codex/agent-approvals-security

Sandbox 모드(정확한 이름):
- `workspace-write` — 버전 관리 폴더의 기본값, 워크스페이스 읽기/쓰기.
- `read-only` — 읽기만.
- `danger-full-access` — 모든 제한 해제(권장 안 함).

Approval 정책:
- `on-request` — 샌드박스 경계·네트워크 액세스 이탈 시 질의. 인터랙티브 기본.
- `never` — 질의 안 함. 비인터랙티브 전용.
- `untrusted` — 안전한 read는 자동 승인, state-mutating은 질의.
- `granular` — sandbox/rules/MCP/permissions/skills 범주별 선택적 승인.

관계: "Sandbox enforces technical boundaries; approval enforces interaction boundaries." 두 레이어는 독립.

Gotcha:
- `--dangerously-bypass-approvals-and-sandbox` → 모든 보호 제거.
- `.git`, `.agents`, `.codex`는 쓰기 가능 모드에서도 read-only 유지.
- Web search는 기본 cached, `"live"` 지정 시 prompt injection 노출 급상승.

### 2.3 Claude Code와의 발산 지점

출처: https://thoughts.jock.pl/p/ai-coding-harness-agents-2026, https://www.builder.io/blog/codex-vs-claude-code

- Codex는 **OS-enforced sandbox**(Seatbelt/Landlock 계열)로 샌드박스가 first-class. Claude Code는 permission rule·hook이 first-class.
- Codex는 unsupervised autonomy에 가까움(full-auto, 클라우드 실행 1–30분 비동기). Claude Code는 plan mode·hook로 supervised autonomy.
- 벤치마크(Figma→Code 클론): Claude Code가 Codex보다 토큰 ~4× 소비(6.2M vs 1.5M). 장시간 복잡 과제는 Claude Code가, 병렬 독립 과제는 Codex가 유리.
- 장시간 세션: Claude Code는 2시간+ 세션에서 초기 결정을 잊는 드리프트. CLAUDE.md + slash command 재주입으로 완화. Codex는 세션마다 AGENTS.md 다시 로딩(한 번만).

---

## 3. 타 툴 공통/전이 패턴

### 3.1 Cursor Rules

출처: https://cursor.com/docs/context/rules, https://blog.atlan.com/engineering/cursor-rules/

- 레거시 `.cursorrules`(루트 단일 파일, deprecation 예정) → **Project Rules `.cursor/rules/*.mdc`**로 마이그레이션.
- MDC 포맷: 메타데이터+본문. path glob으로 스코프 지정 가능(예: `src/backend/**`에서만 활성).
- Memory Bank 패턴: 메모리 파일을 먼저 읽고 계획→질문→실행.
- User rules(설정): 개인 코딩 스타일, Project rules(`.cursor/rules`): 팀 표준.

### 3.2 Aider

출처: https://aider.chat/docs/usage/modes.html, https://www.claudemdeditor.com/aider-conventions-guide

- `CONVENTIONS.md`를 `--read`로 지정하면 시작 시 자동 read-only 주입.
- Architect/Editor 모드: 강한 모델(o1 계열)이 설계, 빠른 모델(GPT-4o, Sonnet)이 파일 편집. 분업으로 cost-quality 최적화.
- Auto-commit 기본 on: 매 변경을 descriptive 메시지로 git commit → 자연스러운 롤백 포인트.

### 3.3 Cline / Continue / Windsurf

출처: https://cline.bot/blog/how-to-think-about-context-engineering-in-cline, https://cline.bot/blog/unlocking-persistent-memory-how-clines-new_task-tool-eliminates-context-window-limitations, https://www.arsturn.com/blog/understanding-windsurf-memories-system-persistent-context

실증 관찰:
> "AI coding performance dips when context windows exceed 50%" — Cline 공식 블로그.

Cline 패턴:
- **Focus Chain**: 태스크 시작 시 todo 생성, 기본 6 메시지마다 재주입 → 드리프트 완화.
- **`new_task` tool**: 컨텍스트 사용률 50% 초과 시 자체 핸드오프. `.clinerules`로 핸드오프 트리거·패키징 규칙 정의.
- **Memory Bank**: `productContext/systemPatterns/techContext/activeContext/progress` 5개 MD 파일을 repo에 커밋.

Windsurf: 자동 생성 Memories + 수동 Rules(`.windsurfrules`)의 로컬/글로벌 분리.

전이 가능(tool-agnostic) 패턴:
- Markdown 메모리 파일 + 세션 시작 시 재주입.
- 컨텍스트 사용률 임계치에서 요약-핸드오프.
- Path-scoped rules로 모노레포 패키지 분리.

툴 고유:
- Claude Code의 hook 체계, Codex의 OS-sandbox, Cursor의 MDC 메타데이터는 직접 이식 어려움.

---

## 4. 실무 엔지니어링 관행

### 4.1 Anthropic "Building Effective Agents"

출처(1차): https://www.anthropic.com/research/building-effective-agents
쿡북: https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents

5가지 워크플로 패턴:
1. Prompt Chaining — 순차 호출 + 검증 게이트.
2. Routing — 분류 후 전문 경로.
3. Parallelization — voting(다수결) 또는 sectioning(독립 분할).
4. Orchestrator-Workers — 중앙 LLM이 동적 분해·위임.
5. Evaluator-Optimizer — 생성/평가 루프, 반복 개선.

핵심 인용:
> "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. (…) simple, composable patterns rather than complex frameworks."

Tool 설계 권고: 명확한 문서·예제·경계, 자연스러운 텍스트에 가까운 포맷, 문자열 이스케이프·라인 카운팅 같은 포매팅 오버헤드 회피, "poka-yoke" 설계로 실수 방지.

### 4.2 팀 규모 CLAUDE.md

출처: https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents

HumanLayer의 harness 성숙도 기준(인용 요약):
> "A basic production harness = CLAUDE.md + type checks + occasional subagents (covers ~15% of requirements). A complete harness = custom architectural rules, machine-readable constraint documents, dynamic tool scoping, verification hooks, cost dashboards (~80%)."

공유 컨텍스트 규칙: 루트 AGENTS.md는 빌드·테스트·컨벤션, 하위 패키지 AGENTS.md는 그 패키지 특유의 패턴만.

### 4.3 Worktree 기반 병렬 실행

출처: https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees, https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe

- Claude Code CLI: `--worktree` 플래그 또는 subagent frontmatter `isolation: worktree`.
- 비-git VCS(SVN, Perforce, Mercurial): `WorktreeCreate`/`WorktreeRemove` hook로 커스텀 로직 주입.
- 자동 정리: `cleanupPeriodDays` 경과 + 커밋 안 된 변경·untracked 파일·unpushed 커밋 없을 때만 제거.

실무 운영:
> "While Claude is working in one worktree, you can be reviewing what finished in another. You're not directing the agent — you're directing the workflow."

### 4.4 비용·토큰 예산 관리

출처: https://code.claude.com/docs/en/costs, https://branch8.com/posts/claude-code-token-limits-cost-optimization-apac-teams

- `/cost` 명령: 세션 토큰 통계.
- Extended thinking 기본 on → output token으로 과금. `/effort`, `/config`, `MAX_THINKING_TOKENS=8000`으로 절감.
- Hook로 preprocessing: 파일 크기·토큰 추정 후 입력 필터링.
- AI Gateway(Kong, Maxim 등)로 중앙 비용 캡·감사 로그.

### 4.5 Observability

출처: https://github.com/ColeMurray/claude-code-otel, https://github.com/phuryn/claude-usage

- Claude Code는 로컬에 토큰·모델·세션·프로젝트 JSONL 로그 작성(플랜 무관).
- OpenTelemetry exporter로 Prometheus/Grafana에 연결 가능.
- Kong AI Gateway로 모든 API 요청 인터셉트 → 토큰 메타데이터 로깅 + 인프라 레벨 예산 enforce(출처: https://konghq.com/blog/engineering/claude-code-governance-with-an-ai-gateway).

### 4.6 Ralph Loop(Geoffrey Huntley)

출처(1차): https://ghuntley.com/ralph/, https://ghuntley.com/loop/
역사: https://www.humanlayer.dev/blog/brief-history-of-ralph

핵심 구조(인용):
```bash
while :; do cat PROMPT.md | claude-code ; done
```

3-phase · 2-prompt · 1-loop:
- PLANNING 프롬프트: specs vs code 갭 분석 → 우선순위 TODO. 구현·커밋 금지.
- BUILDING 프롬프트: 계획 존재 가정, 한 태스크 선택·구현·테스트(backpressure)·커밋.

운영 원칙:
- 루프당 한 가지만("operator must trust the LLM to decide what's the most important thing").
- 주 에이전트가 최대 500 병렬 subagent 스케줄(탐색·기록용), build/test는 단일 subagent로 backpressure.
- 플랜 메모리를 stack 메모리처럼 취급, 세션 간 재사용 최소화.

실패 모드:
- Ripgrep 기반 코드 탐색이 오탐 → "don't assume an item is not implemented" 힌트 필수.
- 컨텍스트 clip이 ~147–152k에서 발생(advertised 200k 대비 실효 하한).
- `git reset --hard` 또는 rescue 프롬프트 없이는 깨진 코드베이스 복구 어려움.
- 보안: `--dangerously-skip-permissions` 필수 → **샌드박스가 유일 방어선**.

### 4.7 Karpathy Software 3.0과 AutoResearch

출처(1차): https://github.com/karpathy/autoresearch
연설/인터뷰: https://www.latent.space/p/s3
해설: https://thenewstack.io/karpathy-autonomous-experiment-loop/, https://buttondown.com/verified/archive/the-karpathy-loop-inside-the-autoresearch-repo/

3가지 원시 요소(인용):
1. **Editable asset**: "the single file the agent is permitted to modify" — 검색공간을 해석 가능하게 유지, 모든 가설을 diff로 리뷰.
2. **Scalar metric**: "the single number that determines whether a change was an improvement" — AutoResearch에서는 `val_bpb`(validation bits per byte), 낮을수록 개선. **인간 판단 불필요**.
3. **Time-boxed cycle**: 5분 고정 훈련 → 어떤 변경을 해도 직접 비교 가능. "approx 12 experiments/hour, 100 experiments while you sleep."

Karpathy 인용(Software 3.0):
> "Demo is works.any(), product is works.all()."
> "Make it easy, fast to win [on verification]. Keep AI on tight leash [on generation]."

Partial Autonomy Slider: Tab → Agent mode → Full auto까지 슬라이더. Tesla Autopilot level 비유.

일반화: "Any system that exposes a scriptable asset, produces a measurable scalar outcome, and tolerates a time-boxed evaluation cycle is a candidate." → DB 쿼리 최적화(asset=쿼리 설정, metric=p95 latency), 티켓 라우팅(asset=분류 프롬프트, metric=hold-out 정확도).

### 4.8 Self-verifying/Self-improving 루프

출처: https://arxiv.org/html/2411.13768v3, https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

- Eval-driven development: 에이전트 기능 만들기 전에 eval 정의(TDD의 에이전트 버전).
- Reflection/Self-refine/MUSE 패턴: 에이전트가 자기 최근 행동 비판 → 절차적 가이던스 기록 → 이후 툴 호출·라우팅을 가이던스로 조건화.
- Offline eval(baseline) + Online eval(프로덕션 모니터) 이중 루프.

### 4.9 안전: 샌드박스·자격증명·파괴 명령 게이팅

출처: https://code.claude.com/docs/en/sandboxing, https://github.com/kenryu42/claude-code-safety-net, https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/

핵심 인용:
> "Sandboxing handles unknown threats; Safety Net handles known destructive patterns that sandboxing permits."
> "Never put secrets inside a sandbox. API keys, tokens, database credentials… can be read and exfiltrated by a context-injected agent."

Safety Net 패턴(kenryu42 GitHub):
- PreToolUse hook에서 `rm -rf`, `git reset --hard`, `git push --force`, `DROP TABLE`, `:(){:|:&};:` 등 블랙리스트 패턴을 검사 → exit 2로 차단.
- Sandbox 바깥에서 자격증명 주입(예: 1Password CLI로 one-shot)하여 agent 프로세스 주소공간에 secret이 상주하지 않도록.

---

## 5. 미비·저논의 주제

### 5.1 AI 생성 코드의 테스트 전략

출처: https://blog.dagworks.io/p/test-driven-development-tdd-of-llm, https://www.guild.ai/glossary/unit-testing-ai-agents

- Deterministic unit tests(고전) + LLM-as-judge(주관 기준) + Snapshot eval(회귀).
- Golden dataset을 커밋 → PR CI에서 회귀 감지. pytest 플러그인 (`pytest-deepeval`, `langsmith-pytest`).
- Vercel Agent 사례(https://vercel.com/docs/agent/pr-review): 생성된 패치를 격리 샌드박스에서 빌드·테스트·린트 → 통과한 것만 PR에 제안.

### 5.2 AI 생성 diff에 대한 PR 리뷰 워크플로

출처: https://code.claude.com/docs/en/code-review, https://github.com/qodo-ai/pr-agent, https://www.augmentcode.com/tools/github-copilot-ai-code-review

- Claude Code의 Code Review: 전문 subagent fleet이 전체 코드베이스 맥락에서 로직 오류·보안·엣지케이스·회귀를 inline comment로 게시. 타임아웃 시 블로킹 하지 않음.
- Rollback 관점 리뷰: "issues that would break behavior, leak data, or block a rollback" — 비가역 마이그레이션·스코프 없는 DB 쿼리·로직 오류를 Important 레벨로 승격.

### 5.3 루프가 잘못됐을 때 Rollback/Recovery

- Aider auto-commit + Ralph 루프의 per-iteration commit → `git reflog` + `git reset --hard <prior_sha>`로 단일 루프 되돌리기.
- Worktree isolation → 주 워크스페이스 오염 없음, 실패한 worktree는 삭제로 끝.
- PreCompact hook으로 critical state 스냅샷 저장 → 컴팩션 복구.

### 5.4 팀 규모 하네스

- CLAUDE.md/AGENTS.md는 git-committed. `settings.json`(공유)와 `settings.local.json`(개인) 분리 준수.
- 엔터프라이즈 managed policy settings로 조직 전체 deny 규칙 강제.
- Kong AI Gateway 같은 중간 레이어로 **팀 단위 API 키 감사·예산 캡**(출처: https://konghq.com/blog/engineering/claude-code-governance-with-an-ai-gateway).
- Subagent 정의와 skill을 플러그인으로 패키지화 → 조직 내부 marketplace에서 배포.

### 5.5 Write-access MCP 서버 보안 모델

출처: https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/, https://www.practical-devsecops.com/mcp-security-vulnerabilities/, https://obot.ai/resources/learning-center/mcp-security/

"GitHub Prompt Injection Data Heist" 사례: 악성 issue 본문이 MCP 툴에 write 권한을 트리거 → private repo 데이터 유출.

실무 방어:
- Progressive scope: 처음은 discovery/read-only, 필요 시점에만 승격.
- Short-lived scoped tokens + 정기 순환. PAT를 env var에 두는 관행 폐기.
- 툴 단위 전용 자격증명(공용 서비스 어카운트 ×).
- OAuth 2.1 + PKCE 필수, capability-level scope.
- Prompt injection은 전송 계층 무관 → PreToolUse hook에서 MCP 응답의 지시문 패턴(`ignore previous instructions`, `repository_dispatch`) 차단.

---

## 참고: 인용 가능한 핵심 구절(책 집필 시 직접 인용 가능)

- (Anthropic) "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."
- (Cline) "AI coding performance dips when context windows exceed 50%."
- (Karpathy) "Demo is works.any(), product is works.all()."
- (Huntley) "these days i approach everything as a loop."
- (Codex docs) "Sandbox mode: What Codex can do technically. Approval policy: When Codex must ask you before it executes an action."
- (Claude Code docs) "Hooks provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them."
- (HumanLayer) "Without a shared vocabulary for harness engineering, teams cannot diagnose what is missing or compare their approaches across different organizations."
- (NVIDIA) "Sandboxing handles unknown threats; Safety Net handles known destructive patterns that sandboxing permits."

---

## 수집 자료 인덱스(우선도 순)

1차 공식 문서:
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/costs
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/skills
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/agent-approvals-security
- https://developers.openai.com/codex/security
- https://www.anthropic.com/research/building-effective-agents
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://www.anthropic.com/engineering/managed-agents
- https://agents.md/
- https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
- https://cursor.com/docs/context/rules

1차 저자/엔지니어 블로그:
- https://ghuntley.com/ralph/
- https://ghuntley.com/loop/
- https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
- https://www.humanlayer.dev/blog/brief-history-of-ralph
- https://github.com/karpathy/autoresearch
- https://www.latent.space/p/s3
- https://cline.bot/blog/how-to-think-about-context-engineering-in-cline
- https://cline.bot/blog/unlocking-persistent-memory-how-clines-new_task-tool-eliminates-context-window-limitations
- https://aider.chat/docs/usage/modes.html
- https://konghq.com/blog/engineering/claude-code-governance-with-an-ai-gateway
- https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/
- https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/

이차 해설·실천 정리:
- https://alexop.dev/posts/understanding-claude-code-full-stack/
- https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/
- https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
- https://dev.to/myougatheaxo/claude-code-in-monorepos-hierarchical-claudemd-and-package-scoped-instructions-1il9
- https://medium.com/devops-ai/the-virtual-monorepo-pattern-how-i-gave-claude-code-full-system-context-across-35-repos-43b310c97db8
- https://thoughts.jock.pl/p/ai-coding-harness-agents-2026
- https://www.builder.io/blog/codex-vs-claude-code
- https://thenewstack.io/karpathy-autonomous-experiment-loop/
- https://buttondown.com/verified/archive/the-karpathy-loop-inside-the-autoresearch-repo/
- https://arxiv.org/html/2411.13768v3
- https://github.com/ColeMurray/claude-code-otel
- https://github.com/kenryu42/claude-code-safety-net
- https://github.com/qodo-ai/pr-agent
- https://vercel.com/docs/agent/pr-review
