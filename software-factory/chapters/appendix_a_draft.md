# 부록 A. 모델·도구 스냅샷 (2026-09-28 기준)

이 부록은 개정판에서 통째로 교체될 부분이다. 본문이 모델을 이름 대신 빌더·리뷰어·설계자·워커라는 역할로 서술하고, 버전·가격·컨텍스트 같은 사실을 이곳 한 곳에 모은 이유가 여기에 있다. 3장에서 본 대로 Claude Opus 5.5와 GPT-6 Sol은 2026-09-22에, Grok 4.7은 그 전날 나왔다. Codex CLI는 알파 판이 하루에도 여러 번 나오고, Claude Code도 거의 매일 새 릴리스를 낸다. 이 표들은 책이 독자의 손에 닿을 즈음이면 이미 몇 칸이 낡아 있을 것이다.

표를 읽을 때 기억해 둘 규칙이 셋 있다. 첫째, 모든 값은 2026-09-28 조회 기준이며 벤더의 공식 문서·릴리스 노트·모델 페이지에서 가져왔다. 둘째, "—"는 그런 정보가 없다는 뜻이 아니다. 이 책의 리서치에서 1차 출처로 확인하지 못한 칸이라는 뜻이다. 2차 보도에만 나오는 값은 싣지 않았다. Muse Spark의 API 가격이 그런 경우다. 셋째, 벤치마크 점수는 싣지 않았다. 3장과 6장에서 본 대로 공개 벤치마크는 오염과 결함 테스트 문제를 안고 있고, 코딩 에이전트의 성능은 모델 하나보다 모델·하네스·컨텍스트·환경·피드백 신호의 합으로 움직인다. 모델을 고를 때는 점수표보다 자기 저장소의 홀드아웃 과제로 직접 재 보는 편이 낫다.

이 스냅샷을 갱신하는 일도 팩토리 운영의 일부다. 새 모델이 나오면 설정 한 곳의 모델 ID를 바꾸고, 회귀 eval을 돌리고, 하네스의 지침이 옛 모델에 맞춰 쓰인 곳이 없는지 점검하자. Claude Code v2.1.283에 추가된 `/doctor prompt-audit`가 바로 이 마지막 점검을 돕는 명령이다. 이 부록에 적힌 값도 같은 방식으로, 아래 A.5의 공식 문서에서 다시 확인하고 쓰기를 권한다.

## A.1 모델

| 모델 | 출시 | 모델 ID | 가격(1M 토큰당 입력 / 캐시 / 출력) | 컨텍스트 / 최대 출력 | 추론 설정 | 지식 컷오프 | 벤더가 말하는 용도 |
|---|---|---|---|---|---|---|---|
| Claude Opus 5.5 | 2026-09-22 | `claude-opus-5-5` | $4 / $0.20(캐시 읽기) / $20 | 1M / 128K | 적응형 사고 상시, effort 기본 `medium`(low~max 5단계) | 2026-06 | "For long-running agentic coding and knowledge work" |
| Claude Fable 5.1 | — | — | $10 / — / $50 | — | — | — | "demanding reasoning and long-horizon agentic work" |
| GPT-6 Sol | 2026-09-22 | `gpt-6-sol` | $2 / $0.2 / $10 | 1,050,000 / 128K | `none`·`low`·`medium`(기본)·`high`·`xhigh`·`max` | 2026-04-20 | "complex coding and agentic workflows" |
| GPT-6 Luna | 2026-09-22 | — | — | — | — | — | "focused, high-volume tasks" |
| Grok 4.7 | 2026-09-21 | `grok-4.7` | $2 / $0.50 / $6 (200k 이하) | 500k / — | `low`~`xhigh`(기본 `high`) | — | xAI의 코딩·지식노동용 최고 모델 |
| Muse Spark 1.3 | 2026-09-02 | — | —(2차 보도만 있어 싣지 않음) | 1M(1.1부터) / — | "max reasoning" 제공 | — | 비용 면의 강점을 내세움 |

표에 다 담지 못한 사실을 모델별로 덧붙인다.

- **Claude Opus 5.5·Fable 5.1** — Anthropic 모델 문서는 어떤 모델을 쓸지 모르겠다면 대부분의 작업을 Opus 5.5로 시작하고, 까다로운 추론·장기 에이전트 작업이나 높은 effort의 Opus 5.5로도 자기 eval이 모자랄 때 Fable 5.1을 쓰라고 권한다. Opus 5.5의 가격은 Opus 5보다 약 40% 낮다(벤더 발표). AWS·Google Cloud·Azure에서도 제공된다.
- **GPT-6 Sol·Luna** — 2026-09-22 ChatGPT Work와 Codex(Plus·Pro·Business·Enterprise·Edu)에 배포됐고 API로도 쓸 수 있다. API 가격은 GPT-5.6 프로모션 가격 대비 50% 낮다(벤더 발표). Codex CLI는 0.157.0부터 두 모델을 지원하며 Amazon Bedrock 경유도 포함한다. 커뮤니티에 보이는 "GPT-5.6 Sol" 표기는 이 책에서 쓰지 않는다.
- **Grok 4.7·Grok Build** — xAI의 현재 표기는 "SpaceXAI"다. 터미널 코딩 에이전트 Grok Build는 SuperGrok·X Premium Plus 구독자 대상이다. Grok Build의 최초 발표일은 자료마다 달라 적지 않는다.
- **Muse Spark 1.3·Muse Code** — Meta가 2026-04-08 처음 발표한 뒤 1.1(2026-07-09, Meta Model API 공개 프리뷰, 1M 컨텍스트)을 거쳐 1.3이 나왔다. Meta는 1.3이 직전 판보다 도구 호출을 약 20%, 토큰을 약 25% 덜 쓰고 프롬프트 인젝션 내성이 강해졌다고 밝혔다. 1.3은 Muse Code와 Meta Model API에서 제공된다. 가중치는 비공개이며 오픈 웨이트는 예고 단계다. 터미널 에이전트 Muse Code는 2026-08-05 베타로 나왔다.

## A.2 도구 버전

| 도구 | 기준 버전 | 날짜 | 메모 |
|---|---|---|---|
| Claude Code CLI | v2.1.283 | 2026-09-25 | 거의 매일 릴리스. 이 판에서 `/doctor prompt-audit`와 `deniedModels` 관리 설정 추가 |
| `anthropics/claude-code-action` | v1.0.235 | 2026-09-25 | 메이저 태그 `v1`은 2025-08-26 |
| Codex CLI | rust-v0.157.1(안정판) | 2026-09-26 | 0.157.0(2026-09-25)에서 GPT-6 Sol·Luna 추가. 같은 시기 알파는 0.159.0-alpha.11(2026-09-28) |
| `openai/codex-action` | v1.12(태그) | 최종 push 2026-09-19 | GitHub Releases 없이 태그만 있음 |
| GitHub Agentic Workflows(`gh aw`) | v0.89.21 | 2026-09-23 | 기술 프리뷰 2026-02-13, 아직 0.x |
| GitHub Spec Kit | v1.0.12 | 2026-09-25 | 저장소 생성 2025-08-21 |
| Gas Town | v1.2.1 | 2026-06-06 | 최종 push 2026-09-18 |
| Grok Build | v1.0.40 | 2026-09-20 | 2차 릴리스 추적 기준 |
| Wrangler(Workers Version URL용) | v4.21.0 이상 | 기능 발표 2025-07-22 | 문서 명칭이 "preview URLs"에서 "Version URLs"로 바뀜 |

## A.3 표면별 기능 매트릭스

3장의 "표면" 구분을 도구별로 펼친 표다. 여기서도 "—"는 이 책의 리서치에서 공식 문서로 확인하지 못했다는 뜻이다.

| 도구 | 헤드리스 | GitHub Actions | 클라우드 실행 | 스케줄·이벤트 | 관리형 리뷰 | AGENTS.md |
|---|---|---|---|---|---|---|
| Claude Code | `claude -p`, Agent SDK(Python·TypeScript) | `claude-code-action@v1` | Claude Code on the web, `claude --cloud` | 루틴(스케줄·API·GitHub 이벤트, research preview), 데스크톱 예약 작업, `/loop` | Claude Code Review(research preview, Team·Enterprise) | 읽는다(단독 또는 CLAUDE.md와 함께) |
| Codex | `codex exec`, Codex SDK(TypeScript) | `openai/codex-action` | Codex cloud(웹·GitHub·GitLab·Linear·Slack에서 시작) | —(Codex 팀의 automations 사용은 팟캐스트 보고) | `@codex review`, 자동 리뷰(P0·P1만) | 읽는다(리뷰 규칙은 가장 가까운 AGENTS.md의 `## Code Review Rules`) |
| Copilot cloud agent | — | Actions 기반 임시 개발 환경에서 실행(작업당 59분 상한) | GitHub 쪽에서 백그라운드 실행 | 이슈 할당(Jira 이슈 할당 포함) | — | — |
| GitHub Agentic Workflows | — | 마크다운을 `.lock.yml` 워크플로로 컴파일. 엔진: Copilot CLI(기본)·Claude Code·Codex·Gemini·Pi | — | Actions 트리거(예: 이슈 생성) | — | — |
| Grok Build | `-p` | — | — | — | — | 읽는다(플러그인·훅·스킬·MCP와 함께) |
| Muse Code | — | — | — | — | — | —(Muse Spark 1.1부터 MCP·스킬 지원 일반화) |

## A.4 자주 쓰는 헤드리스 플래그와 Actions 입력

본문 예제에 쓴 플래그와 입력만 모았다. 모두 해당 도구의 공식 문서·README에 적힌 이름이며, 옵션은 빠르게 바뀌므로 쓰기 전에 공식 문서를 다시 확인하자.

**`claude -p`(Claude Code 헤드리스, v2.1.28x 문서 기준)**

| 플래그 | 하는 일 |
|---|---|
| `--bare` | 훅·스킬·플러그인·MCP·CLAUDE.md 자동 탐색을 건너뛴다. 스크립트·SDK 호출에 권장되며 향후 `-p`의 기본값이 될 예정이다. 이 플래그 없이 `-p`를 돌리면 신뢰한 적 없는 폴더에서도 프로젝트 훅과 `.mcp.json` 서버가 실행된다 |
| `--output-format json` / `stream-json` | 구조화 출력. JSON 결과에 `total_cost_usd`와 모델별 비용이 들어 있다 |
| `--json-schema` | 출력 스키마 지정 |
| `--allowedTools "..."` | 허용할 도구 목록. 예: `Bash(git diff *)` |
| `--permission-mode auto` / `dontAsk` / `acceptEdits` | `dontAsk`는 원래 확인을 물었을 호출을 모두 거부한다. 잠근 CI 실행용 |
| `--permission-prompts none` | 무인 실행 |
| `--continue` / `--resume` | 이전 세션 이어 가기 |
| `--max-turns`, `--model` | 반복 횟수 상한, 모델 지정. `claude-code-action`의 `claude_args`로 넘기는 예가 공식 문서에 있다 |
| `--cloud "<작업>"`, `--teleport` | 작업을 클라우드 세션으로 보내기, 클라우드 세션을 로컬로 가져오기 |

**`codex exec`(Codex CLI 0.157.x 문서 기준)**

| 플래그·규칙 | 하는 일 |
|---|---|
| (기본) | read-only로 실행한다. git 저장소 안에서만 돈다 |
| `--sandbox workspace-write` | 작업 공간 쓰기 허용. `--full-auto`는 deprecated |
| `--json` | JSONL 이벤트 출력 |
| `--output-schema` | 출력 스키마 지정 |
| `-o` / `--output-last-message` | 마지막 메시지를 파일로 저장 |
| `codex exec resume --last` | 마지막 실행 이어 가기 |
| `--ephemeral` | 이름 그대로 일회성 실행. 세부 동작은 공식 문서에서 확인 |
| `--skip-git-repo-check` | git 저장소 밖에서 실행 |
| `CODEX_API_KEY` | CI에서는 호출 한 번에만 인라인으로 넘긴다. 저장소 코드를 체크아웃·실행하는 워크플로에서 잡 수준 환경변수로 두지 않는다 |

**GitHub Actions 입력**

| 액션·도구 | 입력 | 하는 일 |
|---|---|---|
| `anthropics/claude-code-action@v1` | `prompt` | 있으면 어떤 이벤트에서든 도는 automation 모드, 없으면 `@claude` 멘션을 기다리는 interactive 모드 |
| | `claude_args` | CLI 인자 전달(`--max-turns`, `--model`, `--allowedTools` 등) |
| | `anthropic_api_key` | 인증. 이 밖에 `CLAUDE_CODE_OAUTH_TOKEN`, OIDC 워크로드 아이덴티티 페더레이션 |
| | `allowed_bots` | 봇 액터는 기본 차단. 여기 적은 봇은 저장소 권한 검사를 받지 않으니 주의 |
| | `allowed_non_write_users` | 쓰기 권한 없는 사용자 허용. 권한을 최소로 줄인 워크플로에서만, 이때는 `GITHUB_TOKEN`으로 |
| | `include_comments_by_actor` | 공개 저장소에서 입력을 받아들일 작성자 허용 목록 |
| | `show_full_output` | 전체 출력 표시. 비밀 노출 위험으로 기본 비활성 |
| `openai/codex-action` | `safety-strategy` | `drop-sudo`(기본) / `unprivileged-user` / `read-only` / `unsafe` |
| | `permission-profile` | 신규 설정에는 `":workspace"` 권장(레거시 `sandbox` 입력 대신) |
| GitHub Agentic Workflows | 프런트매터 | 트리거(`on`)·권한(`permissions`)·도구·엔진을 적고, 쓰기는 `safe-outputs`로만. `gh aw compile`이 `.lock.yml`을 만든다 |

그 밖에 본문에 나온 명령: Ralph 공식 플러그인의 `/ralph-loop "<작업>" --completion-promise "COMPLETE" --max-iterations 50`, Cloudflare의 `npx wrangler preview --name "pr-<번호>" --json`과 `wrangler preview delete`, `wrangler versions upload --preview-alias`, Codex의 `@codex review`와 `@codex fix`, Claude Code Review의 `REVIEW.md`와 체크런의 기계 판독 줄 `bughunter-severity`.

## A.5 공식 문서 위치

| 대상 | 위치 | 메모 |
|---|---|---|
| Claude Code 문서 | `code.claude.com/docs/en/` 아래 `overview`, `headless`, `hooks`, `routines`, `code-review`, `claude-code-on-the-web`, `agents`, `workflows`, `costs`, `github-actions` | |
| Claude Code 릴리스 | `github.com/anthropics/claude-code/releases`, `CHANGELOG.md` | |
| Claude Code GitHub Action | `github.com/anthropics/claude-code-action` | |
| Ralph 공식 플러그인 | `github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum` | |
| Claude 모델 표 | `platform.claude.com/docs/en/about-claude/models/overview` | |
| Codex 문서 | `learn.chatgpt.com/docs/` 아래 `non-interactive-mode`, `cloud`, `third-party/github`, `codex-sdk` | 옛 주소 `developers.openai.com/codex/...`에서 리다이렉트된다 |
| Codex 릴리스 | `github.com/openai/codex/releases` | 알파가 하루에도 여러 번 나온다 |
| Codex GitHub Action | `github.com/openai/codex-action` | |
| GPT-6 Sol 모델 문서 | `developers.openai.com/api/docs/models/gpt-6-sol` | |
| GitHub Agentic Workflows | `github.github.com/gh-aw/` | |
| Copilot cloud agent | `docs.github.com/copilot/concepts/agents/coding-agent/about-coding-agent` | 문서 경로에 옛 이름(coding agent)이 남아 있다 |
| GitHub Spec Kit | `github.com/github/spec-kit`, `github.github.com/spec-kit/` | |
| Kiro 명세 문서 | `kiro.dev/docs/specs/` | |
| xAI 릴리스 노트 | `docs.x.ai/developers/release-notes` | |
| Muse Spark 1.3 | `research.meta.ai/blog/introducing-muse-spark-1-3` | |
| Cloudflare Workers Version URLs | `developers.cloudflare.com/workers/configuration/previews/` | |
| AWS Amplify PR 프리뷰 | `docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html` | |
| Factory | `factory.com` | 옛 주소 `factory.ai`에서 리다이렉트된다 |
