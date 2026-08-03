# 그룹 F: 색인 대조로 발견한 누락 페이지 (15 URL) — 검색 2026-08-02 기준

<!-- 검색 시점: 2026-08-02 기준 -->
<!-- 수집 방법: 경로 끝 `.md` + curl 원문 markdown. `.md`가 404인 4개 페이지는 HTML을 pandoc으로 변환해 복원. -->
<!-- 중대 주의: `/codex/cli/reference`의 플래그 표는 `.md`에서 `<ConfigTable client:load options={...}/>` 자리표시자로만 나온다. 실제 표 29개는 Astro island props(JSON)에서 복원해 아래에 전량 수록했다. `.md`만 받은 수집은 CLI 플래그 전체를 놓친다. -->

## 이 그룹의 수집 결과 요약

- **15/15 전량 수집 성공.** 접근 실패 0건.
- 단, 15개 URL은 **실제로는 13개의 고유 문서**다. 문서 사이트가 표면(surface) 파라미터 기반으로 재편되면서 별칭이 생겼다 (아래 별칭 표 참조).
- 색인(`llms.txt`)에 **없는** 페이지 1개를 추가 발견해 함께 수집했다: `/codex/reference/slash-commands` (ChatGPT 데스크톱 앱 슬래시 명령).

### URL → 캐노니컬 경로 별칭 표 (2026-08-02 기준)

`developers.openai.com/codex/*`는 전부 `learn.chatgpt.com/docs/*`로 301된다. 색인의 경로와 실제 문서 경로가 다르다.

| 색인상 경로 (llms.txt) | 실제 캐노니컬 경로 | 비고 |
|---|---|---|
| `/codex/cli/reference` | `/docs/developer-commands?surface=cli` | ↓ 아래와 **동일 문서** |
| `/codex/cli/slash-commands` | `/docs/developer-commands?surface=cli` | ↑ 위와 **동일 문서** |
| `/codex/ide/commands` | `/docs/developer-commands?surface=ide` | ↓ 아래와 **동일 문서** |
| `/codex/ide/slash-commands` | `/docs/developer-commands?surface=ide` | ↑ 위와 **동일 문서** |
| `/codex/app/settings` | `/docs/reference/settings` | `/codex/reference/settings`와 동일 |
| `/codex/app/commands` | `/docs/reference/commands` | |
| `/codex/app/windows` | `/docs/windows/windows-app` | |
| `/codex/ide/settings` | `/docs/developer-settings?surface=ide` | |
| `/codex/overview` | `/docs` | `.md` 없음 → HTML 복원 |
| `/codex/learn/best-practices` | `/guides/best-practices` | `.md` 없음 → HTML 복원 |
| `/codex/guides/build-ai-native-engineering-team` | `/guides/build-ai-native-engineering-team` | `.md` 없음 → HTML 복원 |
| `/codex/community/codex-for-oss` | `/community/codex-for-oss` | `.md` 없음 → HTML 복원 |
| `/codex/custom-prompts` | `/docs/custom-prompts` | |
| `/codex/enterprise/usage-limits` | `/docs/enterprise/usage-limits` | |
| `/codex/sites` | `/docs/sites` | |

> **Phase 4 fact-checker 주의:** 책에서 URL을 인용할 때 `developers.openai.com/codex/...` 형태는 아직 살아 있으나(301) 최종 도착지는 `learn.chatgpt.com`이다. 두 도메인을 섞어 쓰면 독자가 혼란스럽다. 한쪽으로 통일하고, "2026-08-02 기준 리다이렉트됨"을 명시할 것.

---

## 자료 1: Developer commands (Codex CLI 레퍼런스) ★최우선

- URL: https://learn.chatgpt.com/codex/cli/reference (캐노니컬: `https://learn.chatgpt.com/docs/developer-commands?surface=cli`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (OpenAI 공식 1차 문서)
- 저자·날짜: OpenAI (발행일 미표기 — 문서에 날짜 메타 없음. 버전 대신 "Maturity" 라벨로 안정성 표기)
- **동일 문서:** `/codex/cli/slash-commands`와 바이트 단위로 동일하다. 두 URL은 한 페이지의 두 섹션(플래그 레퍼런스 + 슬래시 명령)일 뿐이다.

### 핵심 내용

이 페이지 하나가 (a) `codex` 전역 플래그, (b) 28개 서브커맨드 개요와 각각의 플래그, (c) 60여 개 내장 슬래시 명령을 모두 담는다. 책의 레퍼런스 장(章)의 골격이 될 문서.

문서가 직접 밝히는 우선순위 규칙 — 인용 가능:

> "The CLI inherits most defaults from `~/.codex/config.toml`. Any `-c key=value` overrides you pass at the command line take precedence for that invocation."

### 수집 기법 경고 (다른 수집자에게 반드시 공유할 것)

`.md` 원문에는 플래그 표가 **없다**. 이런 자리표시자만 있다:

```
<ConfigTable client:load options={globalFlagOptions} />
<ConfigTable client:load options={commandOverview} secondColumnTitle="Maturity" ... />
```

실제 표 데이터 29개는 HTML의 `<astro-island component-export="ConfigTable" props="...">` 안 JSON에 들어 있다. 아래는 그 29개 표를 전부 복원한 것이다 — **한 줄도 줄이지 않았다.**

### 명령·플래그 전량 (원문 표 복원, 2026-08-02 기준)

## Global flags

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `PROMPT` | string |  | Optional text instruction to start the session. Omit to launch the TUI without a pre-filled message. |
| `--image, -i` | path[,path...] |  | Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag. |
| `--model, -m` | string |  | Override the model set in configuration (for example `gpt-5.6-terra`). |
| `--oss` | boolean | `false` | Use a local open source model provider. Codex uses `--local-provider`, your configured `oss_provider`, or prompts you to choose between LM Studio and Ollama. |
| `--local-provider` | lmstudio \| ollama |  | Choose the local provider used with `--oss`, overriding `oss_provider` for this run. |
| `--profile, -p` | string |  | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--sandbox, -s` | read-only \| workspace-write \| danger-full-access |  | Select the sandbox policy for model-generated shell commands. |
| `--ask-for-approval, -a` | untrusted \| on-request \| never |  | Control when Codex pauses for human approval before running a command. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | boolean | `false` | Run every command without approvals or sandboxing. Only use inside an externally hardened environment. |
| `--dangerously-bypass-hook-trust` | boolean | `false` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--cd, -C` | path |  | Set the working directory for the agent before it starts processing your request. |
| `--search` | boolean | `false` | Enable live web search (sets `web_search = "live"` instead of the default `"cached"`). |
| `--add-dir` | path |  | Grant additional directories write access alongside the main workspace. Repeat for multiple paths. |
| `--no-alt-screen` | boolean | `false` | Disable alternate screen mode for the TUI (overrides `tui.alternate_screen` for this run). |
| `--remote` | ws://host:port \| wss://host:port \| unix:// \| unix://PATH |  | Connect to a remote app-server endpoint over WebSocket or a Unix socket. Supported for `codex`, `codex resume`, `codex fork`, `codex archive`, `codex delete`, and `codex unarchive`; other subcommands reject remote mode. |
| `--remote-auth-token-env` | ENV_VAR |  | Read a bearer token from this environment variable and send it when connecting with `--remote`. Requires `--remote`; tokens are only sent over `wss://` URLs or local-only `ws://` URLs. |
| `--strict-config` | boolean | `false` | Error when `config.toml` contains fields this Codex version does not recognize. Supported by runtime commands such as `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `mcp-server`, and `exec-server`. |
| `--enable` | feature |  | Force-enable a feature flag (translates to `-c features.<name>=true`). Repeatable. |
| `--disable` | feature |  | Force-disable a feature flag (translates to `-c features.<name>=false`). Repeatable. |
| `--config, -c` | key=value |  | Override configuration values. Values parse as TOML if possible; otherwise the literal string is used. |

These options apply to the base `codex` command. Most propagate to commands;
see the notes above or the relevant command help for exceptions. For propagated
flags, follow the relevant command help. For example, `codex exec --oss ...`
applies `--oss` to `exec`.

## Command overview

The Maturity column uses feature maturity labels such as Experimental, Beta,
  and Stable. See [Feature Maturity](https://learn.chatgpt.com/docs/feature-maturity) for how to
  interpret these labels.

| Key/Flag | Maturity | Description |
|---|---|---|
| `codex` | stable | Launch the terminal UI. Accepts the global flags above plus an optional prompt or image attachments. |
| `codex app-server` | experimental | Launch the Codex app server for local development or debugging over stdio, WebSocket, or a Unix socket. |
| `codex remote-control` | experimental | Run or manage remote control for the local app-server, or create a short-lived pairing code. |
| `codex app` | stable | Launch the ChatGPT desktop app on macOS or Windows. On macOS, Codex can open a workspace path; on Windows, Codex prints the path to open. |
| `codex debug app-server send-message-v2` | experimental | Debug app-server by sending a single V2 message through the built-in test client. |
| `codex debug models` | experimental | Print the raw model catalog Codex sees, including an option to inspect only the bundled catalog. |
| `codex debug prompt-input` | experimental | Render the model-visible prompt input list as JSON, optionally with a prompt and images. |
| `codex apply` | stable | Apply the latest diff generated by a Codex cloud chat to your local working tree. Alias: `codex a`. |
| `codex review` | stable | Run a non-interactive review of uncommitted changes, a base branch diff, a commit, or custom review instructions. |
| `codex archive` | stable | Archive a saved interactive session by session ID or session name. |
| `codex delete` | stable | Permanently delete a saved interactive session by session ID or session name. |
| `codex cloud` | experimental | Browse or execute Codex cloud chats from the terminal without opening the TUI. Alias: `codex cloud-tasks`. |
| `codex completion` | stable | Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell. |
| `codex doctor` | stable | Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal, app-server, and thread inventory issues. |
| `codex features` | stable | List feature flags and persistently enable or disable them in `config.toml`. |
| `codex exec` | stable | Run Codex non-interactively. Alias: `codex e`. Stream results to stdout or JSONL and optionally resume previous sessions. |
| `codex execpolicy` | experimental | Evaluate execpolicy rule files and see whether a command would be allowed, prompted, or blocked. |
| `codex login` | stable | Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token piped over stdin. |
| `codex logout` | stable | Remove stored authentication credentials. |
| `codex mcp` | stable | Manage Model Context Protocol servers (list, add, remove, authenticate). |
| `codex plugin marketplace` | stable | Add, list, upgrade, or remove plugin marketplaces from Git or local sources. |
| `codex plugin` | stable | Install, list, and remove plugins from configured marketplace sources. |
| `codex mcp-server` | stable | Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex. |
| `codex resume` | stable | Continue a previous interactive session by ID or resume the most recent chat. |
| `codex fork` | stable | Fork a previous interactive session into a new chat, preserving the original transcript. |
| `codex sandbox` | stable | Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes. |
| `codex update` | stable | Check for and apply a Codex CLI update when the installed release supports self-update. |
| `codex unarchive` | stable | Restore an archived interactive session by session ID or session name. |

## Command details

### `codex` (interactive)

Running `codex` with no subcommand launches the interactive terminal UI (TUI). The agent accepts the global flags above plus image attachments. Web search defaults to cached mode; use `--search` to switch to live browsing. For low-friction local work, use `--sandbox workspace-write --ask-for-approval on-request`.

Use `--remote ws://host:port` or `--remote wss://host:port` to connect the TUI to an app server started with `codex app-server --listen ws://IP:PORT`. For a local Unix socket, use `--remote unix://` for the default socket or `--remote unix://PATH` for an explicit path. Add `--remote-auth-token-env <ENV_VAR>` when the server requires a bearer token for WebSocket authentication.

### `codex app-server`

Launch the Codex app server locally. This is primarily for development and debugging and may change without notice.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--stdio` | boolean | `false` | Use stdio transport. Equivalent to `--listen stdio://` and mutually exclusive with `--listen`. |
| `--listen` | stdio:// \| ws://IP:PORT \| unix:// \| unix://PATH \| off | `stdio://` | Transport listener URL. Use `stdio://` for JSONL, `ws://IP:PORT` for a TCP WebSocket endpoint, `unix://` for the default Unix socket, `unix://PATH` for a custom Unix socket, or `off` to disable the local transport. |
| `--ws-auth` | capability-token \| signed-bearer-token |  | Authentication mode for app-server WebSocket clients. If omitted, WebSocket auth is disabled; non-local listeners warn during startup. |
| `--ws-token-file` | absolute path |  | File containing the shared capability token. Use with `--ws-auth capability-token` unless you provide `--ws-token-sha256` instead. |
| `--ws-token-sha256` | hexadecimal SHA-256 digest |  | Expected SHA-256 digest for capability-token authentication. Use instead of `--ws-token-file` when the client token comes from another source. |
| `--ws-shared-secret-file` | absolute path |  | File containing the HMAC shared secret used to validate signed JWT bearer tokens. Required with `--ws-auth signed-bearer-token`. |
| `--ws-issuer` | string |  | Expected `iss` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-audience` | string |  | Expected `aud` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-max-clock-skew-seconds` | number | `30` | Clock skew allowance when validating signed bearer token `exp` and `nbf` claims. Requires `--ws-auth signed-bearer-token`. |
| `--analytics-default-enabled` | boolean | `false` | Defaults analytics to enabled for first-party app-server clients unless the user opts out in config. |

`codex app-server --listen stdio://` keeps the default JSONL-over-stdio behavior, and `codex app-server --stdio` is an alias for that transport. `--listen ws://IP:PORT` enables WebSocket transport for app-server clients. The server accepts `ws://` listen URLs; use TLS termination or a secure proxy when clients connect with `wss://`. Use `--listen unix://` to accept WebSocket handshakes on Codex's default Unix socket, or `--listen unix:///absolute/path.sock` to choose a socket path. If you generate schemas for client bindings, add `--experimental` to include gated fields and methods.

### `codex remote-control`

Run `codex remote-control` to start remote control in the foreground. Use
`codex remote-control start` to start the local app-server daemon with remote
control enabled, and `codex remote-control stop` to stop it. Managed
remote-control clients and SSH remote workflows use these commands; they aren't
a replacement for `codex app-server --listen` when you're building a local
protocol client.

After the daemon is running, use `codex remote-control pair` to create and
print a short-lived manual pairing code. Add `--json` to any remote-control
command for machine-readable output. For `pair`, the JSON response includes
`pairingCode`, `manualPairingCode`, `environmentId`, and `expiresAt`.

### `codex app`

Launch the ChatGPT desktop app from the terminal on macOS or Windows. On macOS,
Codex can open a specific workspace path; on Windows, Codex prints the path to
open.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `PATH` | path | `.` | Workspace path for the ChatGPT desktop app. On macOS, Codex opens this path; on Windows, Codex prints the path. |
| `--download-url` | url |  | Advanced override for the ChatGPT desktop app installer URL used during install. |

`codex app` opens an installed ChatGPT desktop app, or starts the installer when
the app is missing. On macOS, Codex opens the provided workspace path; on
Windows, it prints the path to open after installation.

### `codex debug app-server send-message-v2`

Send one message through app-server's V2 thread/turn flow using the built-in app-server test client.

| Key/Flag | Type | Description |
|---|---|---|
| `USER_MESSAGE` | string | Message text sent to app-server through the built-in V2 test-client flow. |

This debug flow initializes with `experimentalApi: true`, starts a thread, sends a turn, and streams server notifications. Use it to reproduce and inspect app-server protocol behavior locally.

### `codex debug models`

Print the raw model catalog Codex sees as JSON.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--bundled` | boolean | `false` | Skip refresh and print only the model catalog bundled with the current Codex binary. |

Use `--bundled` when you want to inspect only the catalog bundled with the current binary, without refreshing from the remote models endpoint.

### `codex debug prompt-input`

Render the exact model-visible prompt input list as JSON. Use this when
debugging instruction discovery, session context, or prompt construction.

| Key/Flag | Type | Description |
|---|---|---|
| `PROMPT` | string | Optional user prompt appended after the session context. |
| `--image, -i` | path[,path...] | Attach one or more images to the user prompt. Separate multiple paths with commas or repeat the flag. |

### `codex apply`

Apply the most recent diff from a Codex cloud chat to your local repository. You must authenticate and have access to the chat.

| Key/Flag | Type | Description |
|---|---|---|
| `TASK_ID` | string | Identifier of the Codex cloud chat whose diff should be applied. |

Codex prints the patched files and exits non-zero if `git apply` fails (for example, due to conflicts).

### `codex review`

Run a code review non-interactively. Choose exactly one review target, or pass
custom review instructions as a prompt.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `PROMPT` | string \| - (read stdin) |  | Custom review instructions. Use `-` to read the instructions from stdin. |
| `--uncommitted` | boolean | `false` | Review staged, unstaged, and untracked changes. |
| `--base` | branch |  | Review changes against the specified base branch. |
| `--commit` | SHA |  | Review the changes introduced by the specified commit. |
| `--title` | string |  | Set the commit title shown in the review summary. Requires `--commit`. |
| `--strict-config` | boolean | `false` | Error when `config.toml` contains fields this Codex version does not recognize. |

`--uncommitted`, `--base`, `--commit`, and a custom `PROMPT` conflict with one
another. Use `--title` only with `--commit`.

### `codex archive` and `codex unarchive`

Archive or restore a saved interactive session by session ID or session name.
Use these commands when you want to clean up the session picker without deleting
the transcript. Session IDs take precedence over session names.

```bash
codex archive <SESSION>
codex unarchive <SESSION>
```

| Key/Flag | Type | Description |
|---|---|---|
| `SESSION` | session ID \| session name | Saved session to archive or restore. Session IDs take precedence over session names. |
| `--remote` | ws://host:port \| wss://host:port \| unix:// \| unix://PATH | Connect to a remote app-server endpoint before changing archive state. |
| `--remote-auth-token-env` | ENV_VAR | Read a bearer token from this environment variable when `--remote` requires authentication. |

### `codex delete`

Permanently delete a saved interactive session by session ID or session name.
Use this only when you want to remove the transcript instead of hiding it from
active session lists.

```bash
codex delete <SESSION>
codex delete <SESSION_UUID> --force
```

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `SESSION` | session ID \| session name |  | Saved session to delete. Session IDs take precedence over session names. |
| `--force` | boolean | `false` | Delete without prompting. The session argument must be a UUID; names still require interactive confirmation. |
| `--remote` | ws://host:port \| wss://host:port \| unix:// \| unix://PATH |  | Connect to a remote app-server endpoint before deleting the session. |
| `--remote-auth-token-env` | ENV_VAR |  | Read a bearer token from this environment variable when `--remote` requires authentication. |

Use `--force` only with a session UUID. Named sessions still require
confirmation so Codex doesn't delete a repeated or ambiguous name without a prompt.

### `codex cloud`

Interact with Codex cloud chats from the terminal. The default command opens an interactive picker; `codex cloud exec` submits a task directly, and `codex cloud list` returns recent chats for scripting or quick inspection.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Task prompt. If omitted, Codex prompts interactively for details. |
| `--env` | ENV_ID |  | Target Codex cloud environment identifier (required). Use `codex cloud` to list options. |
| `--attempts` | 1-4 | `1` | Number of assistant attempts (best-of-N) Codex cloud should run. |

Authentication follows the same credentials as the main CLI. Codex exits non-zero if the task submission fails.

#### `codex cloud list`

List recent cloud chats with optional filtering and pagination.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--env` | ENV_ID |  | Filter tasks by environment identifier. |
| `--limit` | 1-20 | `20` | Maximum number of tasks to return. |
| `--cursor` | string |  | Pagination cursor returned by a previous request. |
| `--json` | boolean | `false` | Emit machine-readable JSON instead of plain text. |

Plain-text output prints a task URL followed by status details. Use `--json` for automation. The JSON payload contains a `tasks` array plus an optional `cursor` value. Each task includes `id`, `url`, `title`, `status`, `updated_at`, `environment_id`, `environment_label`, `summary`, `is_review`, and `attempt_total`.

### `codex completion`

Generate shell completion scripts and redirect the output to the appropriate location, for example `codex completion zsh > "${fpath[1]}/_codex"`.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `SHELL` | bash \| zsh \| fish \| power-shell \| elvish | `bash` | Shell to generate completions for. Output prints to stdout. |

### `codex doctor`

Generate a local diagnostic report before filing a support issue or
while investigating a broken Codex installation. The report checks installation,
configuration, authentication, runtime, Git, terminal, app-server, and thread
inventory health.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--json` | boolean | `false` | Emit a redacted machine-readable support report. |
| `--summary` | boolean | `false` | Show grouped check rows and the final count summary only. |
| `--all` | boolean | `false` | Expand long lists in the detailed human-readable report. |
| `--no-color` | boolean | `false` | Disable ANSI color in human-readable output. |
| `--ascii` | boolean | `false` | Use ASCII status labels and separators in human-readable output. |

### `codex features`

Manage feature flags stored in `$CODEX_HOME/config.toml`. The `enable` and
`disable` commands persist changes so they apply to future sessions. The
`features` subcommand doesn't accept `--profile`.

| Key/Flag | Type | Description |
|---|---|---|
| `List subcommand` | codex features list | Show known feature flags, their maturity stage, and their effective state. |
| `Enable subcommand` | codex features enable <feature> | Persistently enable a feature flag in `$CODEX_HOME/config.toml`. |
| `Disable subcommand` | codex features disable <feature> | Persistently disable a feature flag in `$CODEX_HOME/config.toml`. |

### `codex exec`

Use `codex exec` (or the short form `codex e`) for scripted or CI-style runs that should finish without human interaction.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `PROMPT` | string \| - (read stdin) |  | Initial instruction for the task. Use `-` to pipe the prompt from stdin. |
| `--image, -i` | path[,path...] |  | Attach images to the first message. Repeatable; supports comma-separated lists. |
| `--model, -m` | string |  | Override the configured model for this run. |
| `--oss` | boolean | `false` | Use a local open source provider. Codex uses `--local-provider` or your configured `oss_provider`, and exits with an error if neither is set. |
| `--local-provider` | lmstudio \| ollama |  | Choose the local provider used with `--oss`, overriding `oss_provider` for this run. |
| `--sandbox, -s` | read-only \| workspace-write \| danger-full-access |  | Sandbox policy for model-generated commands. Defaults to configuration. |
| `--profile, -p` | string |  | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--full-auto` | boolean | `false` | Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | boolean | `false` | Bypass approval prompts and sandboxing. Dangerous—only use inside an isolated runner. |
| `--dangerously-bypass-hook-trust` | boolean | `false` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--cd, -C` | path |  | Set the workspace root before executing the task. |
| `--skip-git-repo-check` | boolean | `false` | Allow running outside a Git repository (useful for one-off directories). |
| `--ephemeral` | boolean | `false` | Run without persisting session rollout files to disk. |
| `--ignore-user-config` | boolean | `false` | Do not load `$CODEX_HOME/config.toml`. Authentication still uses `CODEX_HOME`. |
| `--ignore-rules` | boolean | `false` | Do not load user or project execpolicy `.rules` files for this run. |
| `--output-schema` | path |  | JSON Schema file describing the expected final response shape. Codex validates tool output against it. |
| `--color` | always \| never \| auto | `auto` | Control ANSI color in stdout. |
| `--json, --experimental-json` | boolean | `false` | Print newline-delimited JSON events instead of formatted text. |
| `--output-last-message, -o` | path |  | Write the assistant’s final message to a file. Useful for downstream scripting. |
| `Resume subcommand` | codex exec resume [SESSION_ID] |  | Resume an exec session by ID or add `--last` to continue the most recent session from the current working directory. Add `--all` to consider sessions from any directory. Accepts an optional follow-up prompt. |
| `-c, --config` | key=value |  | Inline configuration override for the non-interactive run (repeatable). |

Codex writes formatted output by default. Add `--json` to receive newline-delimited JSON events (one per state change). The optional `resume` subcommand lets you continue non-interactive tasks. Use `--last` to pick the most recent session from the current working directory, or add `--all` to search across all sessions:

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `SESSION_ID` | uuid \| session name |  | Resume the specified session. Omit and use `--last` to continue the most recent session. |
| `--last` | boolean | `false` | Resume the most recent chat from the current working directory. |
| `--all` | boolean | `false` | Include sessions outside the current working directory when selecting the most recent session. |
| `--image, -i` | path[,path...] |  | Attach one or more images to the follow-up prompt. Separate multiple paths with commas or repeat the flag. |
| `PROMPT` | string \| - (read stdin) |  | Optional follow-up instruction sent immediately after resuming. |

### `codex execpolicy`

Check `execpolicy` rule files before you save them. `codex execpolicy check` accepts one or more `--rules` flags (for example, files under `~/.codex/rules`) and emits JSON showing the strictest decision and any matching rules. Add `--pretty` to format the output. The `execpolicy` command is currently in preview.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--rules, -r` | path (repeatable) |  | Path to an execpolicy rule file to evaluate. Provide multiple flags to combine rules across files. |
| `--pretty` | boolean | `false` | Pretty-print the JSON result. |
| `COMMAND...` | var-args |  | Command to be checked against the specified policies. |

### `codex login`

Authenticate the CLI with a ChatGPT account, API key, or access token. With no flags, Codex opens a browser for the ChatGPT OAuth flow.

| Key/Flag | Type | Description |
|---|---|---|
| `--with-api-key` | boolean | Read an API key from stdin (for example `printenv OPENAI_API_KEY \| codex login --with-api-key`). |
| `--with-access-token` | boolean | Read an access token from stdin (for example `printenv CODEX_ACCESS_TOKEN \| codex login --with-access-token`). |
| `--device-auth` | boolean | Use OAuth device code flow instead of launching a browser window. |
| `status subcommand` | codex login status | Print the active authentication mode and exit with 0 when logged in. |

`codex login status` exits with `0` when credentials are present, which is helpful in automation scripts.

### `codex logout`

Remove saved credentials for both API key and ChatGPT authentication. This command has no flags.

### `codex mcp`

Manage Model Context Protocol server entries stored in `~/.codex/config.toml`.

| Key/Flag | Type | Description |
|---|---|---|
| `list` | --json | List configured MCP servers. Add `--json` for machine-readable output. |
| `get <name>` | --json | Show a specific server configuration. `--json` prints the raw config entry. |
| `add <name>` | -- <command...> \| --url <value> | Register a server using a stdio launcher command or a streamable HTTP URL. Supports `--env KEY=VALUE` for stdio transports. |
| `remove <name>` |  | Delete a stored MCP server definition. |
| `login <name>` | --scopes scope1,scope2 | Start an OAuth login for a streamable HTTP server (servers that support OAuth only). |
| `logout <name>` |  | Remove stored OAuth credentials for a streamable HTTP server. |

The `add` subcommand supports both stdio and streamable HTTP transports:

| Key/Flag | Type | Description |
|---|---|---|
| `COMMAND...` | stdio transport | Executable plus arguments to launch the MCP server. Provide after `--`. |
| `--env KEY=VALUE` | repeatable | Environment variable assignments applied when launching a stdio server. |
| `--url` | https://… | Register a streamable HTTP server instead of stdio. Mutually exclusive with `COMMAND...`. |
| `--bearer-token-env-var` | ENV_VAR | Environment variable whose value is sent as a bearer token when connecting to a streamable HTTP server. |
| `--oauth-client-id` | CLIENT_ID | OAuth client identifier for a streamable HTTP MCP server. Requires `--url`. |
| `--oauth-resource` | RESOURCE | OAuth resource parameter to include during login for a streamable HTTP MCP server. Requires `--url`. |

OAuth actions (`login`, `logout`) only work with streamable HTTP servers (and only when the server supports OAuth).

### `codex plugin`

Install, list, and remove plugins from configured marketplaces.

| Key/Flag | Type | Description |
|---|---|---|
| `add <plugin[@marketplace]>` | [--marketplace, -m NAME] [--json] | Install a plugin from a configured marketplace. Use `--marketplace` or `-m` when the plugin argument omits `@marketplace`. |
| `list` | [--marketplace, -m NAME] [--available --json] [--json] | List installed plugins. With `--json`, output has `installed` and `available` arrays; `--available` includes uninstalled marketplace plugins and requires `--json`. |
| `remove <plugin[@marketplace]>` | [--marketplace, -m NAME] [--json] | Remove an installed plugin from local config and cache. Use `--json` for automation-friendly output. |
| `marketplace` |  | Manage configured marketplace sources. See `codex plugin marketplace` below. |

`codex plugin add --json` prints `pluginId`, `name`, `marketplaceName`,
`version`, `installedPath`, and `authPolicy`. `codex plugin list --json` prints
`installed` and `available` arrays. Entries include `pluginId`, `name`,
`marketplaceName`, `version`, `installed`, `enabled`, `source`, `installPolicy`,
`authPolicy`, and, when available, `marketplaceSource` with the configured
marketplace source type and value. `codex plugin remove --json` prints
`pluginId`, `name`, and `marketplaceName`.

### `codex plugin marketplace`

Manage plugin marketplace sources that Codex can browse and install from.

| Key/Flag | Type | Description |
|---|---|---|
| `add <source>` | [--ref REF] [--sparse PATH] [--json] | Install a plugin marketplace from GitHub shorthand, a Git URL, an SSH URL, or a local marketplace root directory. `--sparse` is supported only for Git sources and can be repeated. |
| `list` | [--json] | Show plugin marketplaces Codex is currently considering and the root path for each marketplace. |
| `upgrade [marketplace-name]` | [--json] | Refresh one configured Git marketplace, or all configured Git marketplaces when no name is provided. |
| `remove <marketplace-name>` | [--json] | Remove a configured plugin marketplace. |

`codex plugin marketplace add` accepts GitHub shorthand such as `owner/repo` or
`owner/repo@ref`, HTTP or HTTPS Git URLs, SSH Git URLs, and local marketplace
root directories. Use `--ref` to pin a Git ref, and repeat `--sparse PATH` to
use a sparse checkout for Git-backed marketplace repositories.

`codex plugin marketplace list` prints in-scope marketplace names and roots,
including implicitly discovered default marketplaces and configured marketplace
snapshots.

Add `--json` to marketplace add, list, upgrade, or remove commands for
automation-friendly output. Marketplace add JSON includes `marketplaceName`,
`installedRoot`, and `alreadyAdded`; list JSON includes a `marketplaces` array
with `name`, `root`, and optional `marketplaceSource`; upgrade JSON includes
`selectedMarketplaces`, `upgradedRoots`, and `errors`; remove JSON includes
`marketplaceName` and `installedRoot`.

### `codex mcp-server`

Run Codex as an MCP server over stdio so that other tools can connect. This command inherits global configuration overrides and exits when the downstream client closes the connection.

### `codex resume`

Continue an interactive session by ID or resume the most recent chat. `codex resume` scopes `--last` to the current working directory unless you pass `--all`. It accepts the same global flags as `codex`, including model and sandbox overrides.

If the current working directory differs from the session's saved directory,
Codex asks which directory to use. Set
[`tui.resume_cwd`](https://learn.chatgpt.com/docs/config-file/config-reference) to `"current"` or
`"session"` to reuse that choice without a prompt. An explicit `--cd` (`-C`)
override takes precedence over `tui.resume_cwd`.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `SESSION_ID` | uuid \| session name |  | Resume the specified session. Omit and use `--last` to continue the most recent session. |
| `--last` | boolean | `false` | Skip the picker and resume the most recent chat from the current working directory. |
| `--all` | boolean | `false` | Include sessions outside the current working directory when selecting the most recent session. |
| `--include-non-interactive` | boolean | `false` | Include non-interactive sessions in the picker and `--last` selection. |

### `codex fork`

Fork a previous interactive session into a new chat. By default, `codex fork` opens the session picker; add `--last` to fork your most recent session instead.

When the current and saved session directories differ, `codex fork` uses the
same working-directory prompt and `tui.resume_cwd` setting as `codex resume`.

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `SESSION_ID` | uuid |  | Fork the specified session. Omit and use `--last` to fork the most recent session. |
| `--last` | boolean | `false` | Skip the picker and fork the most recent chat automatically. |
| `--all` | boolean | `false` | Show sessions beyond the current working directory in the picker. |

### `codex sandbox`

Use the sandbox helper to run a command under the same policies Codex uses internally.

#### macOS seatbelt

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--profile, -p` | NAME |  | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permission-profile, -P` | NAME |  | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | DIR |  | Working directory used for profile resolution and command execution. Requires `--permission-profile`. |
| `--include-managed-config` | boolean | `false` | Include managed requirements while resolving an explicit permissions profile. Requires `--permission-profile`. |
| `--allow-unix-socket` | path |  | Allow the sandboxed command to bind or connect Unix sockets rooted at this path. Repeat to allow multiple paths. |
| `--log-denials` | boolean | `false` | Capture macOS sandbox denials with `log stream` while the command runs and print them after exit. |
| `--config, -c` | key=value |  | Pass configuration overrides into the sandboxed run (repeatable). |
| `COMMAND...` | var-args |  | Shell command to execute under macOS Seatbelt. Everything after `--` is forwarded. |

#### Linux Landlock

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--profile, -p` | NAME |  | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permission-profile, -P` | NAME |  | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | DIR |  | Working directory used for profile resolution and command execution. Requires `--permission-profile`. |
| `--include-managed-config` | boolean | `false` | Include managed requirements while resolving an explicit permissions profile. Requires `--permission-profile`. |
| `--config, -c` | key=value |  | Configuration overrides applied before launching the sandbox (repeatable). |
| `COMMAND...` | var-args |  | Command to execute under Landlock + seccomp. Provide the executable after `--`. |

#### Windows

| Key/Flag | Type | Default | Description |
|---|---|---|---|
| `--profile, -p` | NAME |  | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permission-profile, -P` | NAME |  | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | DIR |  | Working directory used for profile resolution and command execution. Requires `--permission-profile`. |
| `--include-managed-config` | boolean | `false` | Include managed requirements while resolving an explicit permissions profile. Requires `--permission-profile`. |
| `--config, -c` | key=value |  | Configuration overrides applied before launching the sandbox (repeatable). |
| `COMMAND...` | var-args |  | Command to execute under the native Windows sandbox. Provide the executable after `--`. |

### `codex update`

Check for and apply a Codex CLI update when the installed release supports self-update. Debug builds print a message telling you to install a release build instead.

## Flag combinations and safety tips

- Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM.
- When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`.
- Pair `--json` with `--output-last-message` in CI to capture machine-readable progress and a final natural-language summary.

## Interactive shortcuts

- Type `@` to search for a file in the workspace and add its path to the prompt.
- Press <kbd>Up</kbd> or <kbd>Down</kbd> to restore draft history.
- Press <kbd>Ctrl</kbd>+<kbd>R</kbd> to search prompt history, then press <kbd>Enter</kbd> to use a match or <kbd>Esc</kbd> to cancel.
- Press <kbd>Ctrl</kbd>+<kbd>O</kbd> or run `/copy` to copy the latest completed Codex output.
- Prefix a line with `!` to run a local shell command under the current approval and sandbox settings.
- Press <kbd>Tab</kbd> while Codex is working to queue a follow-up prompt, slash command, or shell command for the next turn.
- Press <kbd>Enter</kbd> while Codex is working to inject new instructions into the current turn.
- Press <kbd>Esc</kbd> twice with an empty composer to edit the previous user message and fork the chat from that point.
- Press <kbd>Ctrl</kbd>+<kbd>C</kbd> or run `/exit` to close the session.


### 슬래시 명령 전량 (동 문서 후반부 = `/codex/cli/slash-commands`)

Slash commands give you fast, keyboard-first control over Codex. Type `/` in
the composer to open the slash popup, choose a command, and Codex will perform
actions such as switching models, adjusting permissions, or summarizing long
chats without leaving the terminal.

This guide shows you how to:

- Find the right built-in slash command for a task
- Steer an active session with commands like `/model`, `/fast`,
  `/personality`, `/permissions`, `/approve`, `/raw`, `/agent`, and `/status`

## Built-in slash commands

Codex ships with the following commands. Open the slash popup and start typing
the command name to filter the list.

When a chat is already running, you can type a slash command and press `Tab` to
queue it for the next turn. Codex parses queued slash commands when they run, so
command menus and errors appear after the current turn finishes. Slash
completion still works before you queue the command.

| Command                                                                                     | Purpose                                                         | When to use it                                                                                             |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [`/permissions`](#update-permissions-with-permissions)                                      | Set what Codex can do without asking first.                     | Relax or tighten approval requirements mid-session, such as switching between Auto and Read Only.          |
| [`/ide`](#include-ide-context-with-ide)                                                     | Include open files, current selection, and other IDE context.   | Pull editor context into the next prompt without re-explaining what's open in your IDE.                    |
| [`/keymap`](#remap-tui-shortcuts-with-keymap)                                               | Remap TUI keyboard shortcuts.                                   | Inspect and persist custom shortcut bindings in `config.toml`.                                             |
| [`/vim`](#toggle-vim-mode-with-vim)                                                         | Toggle Vim mode for the composer.                               | Switch between Vim normal/insert behavior and the default composer editing mode.                           |
| [`/setup-default-sandbox`](#set-up-the-elevated-windows-sandbox-with-setup-default-sandbox) | Set up the elevated agent sandbox (Windows only).               | Replace the degraded Windows sandbox after Codex offers the elevated setup.                                |
| [`/sandbox-add-read-dir`](#grant-sandbox-read-access-with-sandbox-add-read-dir)             | Grant sandbox read access to an extra directory (Windows only). | Unblock commands that need to read an absolute directory path outside the current readable roots.          |
| [`/agent`, `/subagents`](#switch-agent-threads-with-agent)                                  | Switch the active agent thread.                                 | Inspect or continue work in a spawned subagent thread.                                                     |
| [`/apps`](#browse-apps-with-apps)                                                           | Browse apps (connectors) and insert them into your prompt.      | Attach an app as `$app-slug` before asking Codex to use it.                                                |
| [`/plugins`](#browse-plugins-with-plugins)                                                  | Browse installed and discoverable plugins.                      | Inspect plugin tools, install suggested plugins, or manage plugin availability.                            |
| [`/hooks`](#view-and-manage-lifecycle-hooks-with-hooks)                                     | View and manage lifecycle hooks.                                | Inspect configured hooks, trust new or changed hooks, or disable non-managed hooks before they run.        |
| [`/clear`](#clear-the-terminal-and-start-a-new-chat-with-clear)                             | Clear the terminal and start a fresh chat.                      | Reset the visible UI and chat context together when you want a fresh start.                                |
| [`/rename`](#rename-the-current-chat-with-rename)                                           | Rename the current chat.                                        | Give a saved session a recognizable name without leaving the TUI.                                          |
| [`/archive`](#archive-the-current-session-with-archive)                                     | Archive the current session and exit Codex.                     | Remove the current session from active session lists without deleting its transcript.                      |
| [`/delete`](#delete-the-current-session-with-delete)                                        | Permanently delete the current session and exit Codex.          | Remove the transcript and descendant sessions when archiving isn't enough.                                 |
| [`/compact`](#keep-transcripts-lean-with-compact)                                           | Summarize the visible chat to free tokens.                      | Use after long runs so Codex retains key points without blowing the context window.                        |
| [`/copy`](#copy-the-latest-response-with-copy)                                              | Copy the latest completed Codex output.                         | Grab the latest finished response or plan text without manually selecting it. You can also press `Ctrl+O`. |
| [`/diff`](#review-changes-with-diff)                                                        | Show the Git diff, including files Git isn't tracking yet.      | Review Codex's edits before you commit or run tests.                                                       |
| [`/exit`](#exit-the-cli-with-quit-or-exit)                                                  | Exit the CLI (same as `/quit`).                                 | Alternative spelling; both commands exit the session.                                                      |
| [`/experimental`](#toggle-experimental-features-with-experimental)                          | Toggle experimental features.                                   | Enable options such as Network proxy or Prevent sleep while running.                                       |
| [`/approve`](#approve-an-auto-review-denial-with-approve)                                   | Approve one retry of a recent auto review denial.               | Retry a command or action that the auto reviewer denied.                                                   |
| [`/memories`](#configure-memories-with-memories)                                            | Configure memory use and generation.                            | Turn memory injection or memory generation on or off without leaving the TUI.                              |
| [`/skills`](#use-skills-with-skills)                                                        | Browse and use skills.                                          | Improve task-specific behavior by selecting a relevant local skill.                                        |
| [`/import`](#import-claude-code-configuration-with-import)                                  | Import Claude Code setup, project files, and recent chats.      | Migrate supported external-agent artifacts into Codex configuration and local files.                       |
| [`/feedback`](#send-feedback-with-feedback)                                                 | Send logs to the Codex maintainers.                             | Report issues or share diagnostics with support.                                                           |
| [`/init`](#generate-agentsmd-with-init)                                                     | Generate an `AGENTS.md` scaffold in the current directory.      | Capture persistent instructions for the repository or subdirectory you're working in.                      |
| [`/logout`](#sign-out-with-logout)                                                          | Sign out of Codex.                                              | Clear local credentials when using a shared machine.                                                       |
| [`/mcp`](#list-mcp-tools-with-mcp)                                                          | List configured Model Context Protocol (MCP) tools.             | Check which external tools Codex can call during the session; add `verbose` for server details.            |
| [`/mention`](#highlight-files-with-mention)                                                 | Attach a file to the chat.                                      | Point Codex at specific files or folders you want it to inspect next.                                      |
| [`/model`](#set-the-active-model-with-model)                                                | Choose the active model (and reasoning effort, when available). | Switch between models such as `gpt-5.6-luna` and `gpt-5.6-terra` before running a task.                    |
| [`/fast`](#toggle-fast-mode-with-fast)                                                      | Toggle a Fast service tier when the model catalog exposes one.  | Turn the current model's Fast tier on or off and persist the selection.                                    |
| [`/plan`](#switch-to-plan-mode-with-plan)                                                   | Switch to plan mode and optionally send a prompt.               | Ask Codex to propose an execution plan before implementation work starts.                                  |
| [`/goal`](#set-or-view-a-task-goal-with-goal)                                               | Set, edit, pause, resume, view, or clear a task goal.           | Give Codex a persistent target to track while a larger task runs.                                          |
| [`/personality`](#set-a-communication-style-with-personality)                               | Choose a communication style for responses.                     | Make Codex more concise, more explanatory, or more collaborative without changing your instructions.       |
| [`/ps`](#check-background-terminals-with-ps)                                                | Show background terminals and their recent output.              | Check long-running commands without leaving the main transcript.                                           |
| [`/stop`](#stop-background-terminals-with-stop)                                             | Stop all background terminals.                                  | Cancel background terminal work started by the current session.                                            |
| [`/fork`](#fork-the-current-chat-with-fork)                                                 | Fork the current chat into a new chat.                          | Branch the active session to explore a new approach without losing the current transcript.                 |
| [`/app`](#continue-in-the-desktop-app-with-app)                                             | Continue the current session in the ChatGPT desktop app.        | Move from the TUI to the desktop app on macOS or Windows.                                                  |
| [`/side`, `/btw`](#start-a-side-chat-with-side)                                             | Start an ephemeral side chat.                                   | Ask a focused follow-up without disrupting the main chat's transcript.                                     |
| [`/raw`](#toggle-raw-scrollback-with-raw)                                                   | Toggle raw scrollback mode.                                     | Make terminal selection and copying less formatted while reviewing long output.                            |
| [`/resume`](#resume-a-saved-chat-with-resume)                                               | Resume a saved chat from your session list.                     | Continue work from a previous CLI session without starting over.                                           |
| [`/new`](#start-a-new-chat-with-new)                                                        | Start a new chat inside the same CLI session.                   | Reset the chat context without leaving the CLI when you want a fresh prompt in the same repo.              |
| [`/quit`](#exit-the-cli-with-quit-or-exit)                                                  | Exit the CLI.                                                   | Leave the session immediately.                                                                             |
| [`/review`](#ask-for-a-working-tree-review-with-review)                                     | Ask Codex to review your working tree.                          | Run after Codex completes work or when you want a second set of eyes on local changes.                     |
| [`/status`](#inspect-the-session-with-status)                                               | Display session configuration and token usage.                  | Confirm the active model, approval policy, writable roots, and remaining context capacity.                 |
| [`/usage`](#view-account-usage-with-usage)                                                  | View account token usage or use a rate-limit reset.             | Inspect daily, weekly, or cumulative ChatGPT token activity from inside the TUI.                           |
| [`/debug-config`](#inspect-config-layers-with-debug-config)                                 | Print config layer and requirements diagnostics.                | Debug precedence and policy requirements, including experimental network constraints.                      |
| [`/statusline`](#configure-footer-items-with-statusline)                                    | Configure TUI status-line fields interactively.                 | Pick and reorder footer items (model/context/limits/git/tokens/session) and persist in config.toml.        |
| [`/title`](#configure-terminal-title-items-with-title)                                      | Configure terminal window or tab title fields interactively.    | Pick and reorder title items such as project, status, thread, branch, model, and task progress.            |
| [`/theme`](#choose-a-syntax-theme-with-theme)                                               | Choose a syntax-highlighting theme.                             | Preview and persist a terminal syntax-highlighting theme.                                                  |
| [`/pets`, `/pet`](#choose-a-terminal-pet-with-pets)                                         | Choose or hide a terminal pet.                                  | Personalize the TUI with a built-in or custom ambient pet.                                                 |

`/quit` and `/exit` both exit the CLI. Use them only after you have saved or
committed any important work.

Use `/permissions` to adjust what Codex can do without asking first. Use
`/approve` only when you need to retry a recent action that automatic review
denied.

## Control your session with slash commands

The following workflows keep your session on track without restarting Codex.

### Set the active model with `/model`

1. Start Codex and open the composer.
2. Type `/model` and press Enter.
3. Choose a model such as `gpt-5.6-luna` or `gpt-5.6-terra` from the popup.

Expected: Codex confirms the new model in the transcript. Run `/status` to verify the change.

### Toggle Fast mode with `/fast`

1. Type `/fast` to turn the current model's Fast service tier on.
2. Type `/fast` again to turn it off.

Expected: Codex toggles the tier and saves the selection. In the TUI footer,
you can also show a Fast mode status-line item with `/statusline`.

Fast tier commands are catalog-driven. If the current model doesn't advertise a
Fast tier, Codex won't show `/fast`.

### Set a communication style with `/personality`

Use `/personality` to change how Codex communicates without rewriting your prompt.

1. In an active chat, type `/personality` and press Enter.
2. Choose a style from the popup.

Expected: Codex confirms the new style in the transcript and uses it for later
responses in the chat.

Codex supports `friendly`, `pragmatic`, and `none` personalities. Use `none`
to disable personality instructions.

If the active model doesn't support personality-specific instructions, Codex hides this command.

### Switch to plan mode with `/plan`

1. Type `/plan` and press Enter to switch the active chat into plan
   mode.
2. Optional: provide inline prompt text (for example, `/plan Propose a
migration plan for this service`).
3. You can paste content or attach images while using inline `/plan` arguments.

Expected: Codex enters plan mode and uses your optional inline prompt as the first planning request.

While Codex is already working, `/plan` is temporarily unavailable.

### Set or view a task goal with `/goal`

1. Type `/goal <objective>` to set the goal, for example `/goal Finish the migration and keep tests green`.
2. Type `/goal` to view the current goal.
3. Use `/goal edit` to revise the objective. Use `/goal pause`, `/goal resume`, or `/goal clear` to pause, resume, or remove it.

Expected: Codex keeps the goal attached to the active chat while work continues.

Goal objectives must be non-empty and at most 4,000 characters. For longer
instructions, put the details in a file and point the goal at that file.

### Toggle experimental features with `/experimental`

1. Type `/experimental` and press Enter.
2. Toggle the features you want (for example, Network proxy or Prevent sleep while running), then restart Codex if the prompt asks you to.

Expected: Codex saves your feature choices to config and applies them on restart.

### Approve an auto review denial with `/approve`

Use `/approve` when the automatic reviewer denied a recent action and you want
Codex to retry it once.

1. Type `/approve`.
2. Confirm the retry when Codex shows the relevant denied action.

Expected: Codex retries that denied action once under the current session
policy.

### Configure memories with `/memories`

1. Type `/memories`.
2. Choose whether Codex should use existing memories, generate new memories, or
   keep memory behavior disabled.

Expected: Codex updates the relevant memory settings for future sessions.

### Use skills with `/skills`

1. Type `/skills`.
2. Pick the skill you want Codex to apply.

Expected: Codex inserts the selected skill context so the next request follows
that skill's instructions.

### Import Claude Code configuration with `/import`

1. Type `/import`.
2. Choose the Claude Code setup, project files, or recent chats you want to migrate.

Expected: Codex opens the external-agent import picker and imports the selected
supported artifacts into Codex configuration and local files.

Run `/import` from a local TUI session. It's unavailable while a task is running,
in remote sessions, and while connected to the local app-server daemon.

<a id="clear-the-terminal-and-start-a-new-chat-with-clear"></a>
<a id="clear-the-terminal-and-start-a-new-task-with-clear"></a>

### Clear the terminal and start a new chat with `/clear`

1. Type `/clear` and press Enter.

Expected: Codex clears the terminal, resets the visible transcript, and starts
a fresh chat in the same CLI session.

To name the new chat as you create it, run `/clear release prep`.

Unlike <kbd>Ctrl</kbd>+<kbd>L</kbd>, `/clear` starts a new chat.

<kbd>Ctrl</kbd>+<kbd>L</kbd> only clears the terminal view and keeps the current
chat. Codex disables both actions while a task is in progress.

### Archive the current session with `/archive`

1. Type `/archive` and press Enter.
2. Confirm that you want to archive the current session and exit Codex.

Expected: Codex archives the current session and closes the interactive TUI.
Codex keeps the session transcript stored locally; restore it later with
`codex unarchive <SESSION>`.

`/archive` is unavailable while a task is running.

### Delete the current session with `/delete`

1. Type `/delete` and press Enter.
2. Confirm that you want to delete the current session and exit Codex.

Expected: Codex deletes the current session transcript and closes the
interactive TUI. Deletion is permanent and also removes spawned descendant
sessions.

`/delete` is unavailable while a chat is running or in a side chat.

### Update permissions with `/permissions`

1. Type `/permissions` and press Enter.
2. Select the approval preset that matches your comfort level, for example
   `Auto` for hands-off runs or `Read Only` to review edits. When named
   permission profiles are active, the picker also shows configured custom
   profiles and their descriptions.

Expected: Codex announces the updated policy. Future actions respect the
updated approval mode until you change it again.

### Include IDE context with `/ide`

1. Type `/ide`.
2. Add optional inline text if you want to explain what Codex should do with the
   current IDE selection or open files.

Expected: Codex includes available IDE context in the next prompt.

### Toggle Vim mode with `/vim`

1. Type `/vim`.
2. Continue editing in the composer.

Expected: Codex toggles composer Vim mode for the current session. To make Vim
mode the default for new sessions, set `tui.vim_mode_default = true` in
`config.toml`.

### Set up the elevated Windows sandbox with `/setup-default-sandbox`

This command appears only on Windows when Codex is using the degraded
restricted-token sandbox.

1. Type `/setup-default-sandbox`.
2. Follow the administrator setup flow.

Expected: Codex configures the elevated Windows sandbox and selects the
corresponding automatic approval preset.

### Copy the latest response with `/copy`

1. Type `/copy` and press Enter.

Expected: Codex copies the latest completed Codex output to your clipboard.

If a turn is still running, `/copy` uses the latest completed output instead of
the in-progress response. The command is unavailable before the first completed
Codex output and immediately after a rollback.

You can also press <kbd>Ctrl</kbd>+<kbd>O</kbd> from the main TUI to copy the
latest completed response without opening the slash command menu.

### Toggle raw scrollback with `/raw`

1. Type `/raw`, `/raw on`, or `/raw off`.

Expected: Codex toggles raw scrollback mode, which makes terminal selection and
copying more direct. You can also use the default <kbd>Alt</kbd>+<kbd>R</kbd>
binding or persist the default with `tui.raw_output_mode = true`.

### Grant sandbox read access with `/sandbox-add-read-dir`

This command is available only when running the CLI natively on Windows.

1. Type `/sandbox-add-read-dir C:\absolute\directory\path` and press Enter.
2. Confirm the path is an existing absolute directory.

Expected: Codex refreshes the Windows sandbox policy and grants read access to
that directory for later commands that run in the sandbox.

### Inspect the session with `/status`

1. In any chat, type `/status`.
2. Review the output for the active model, approval policy, writable roots, and
   current token usage. When the TUI connects remotely, the output also
   shows the remote address and the server version.

Expected: Codex prints a summary confirming that it's operating where you
expect.

### View account usage with `/usage`

1. Type `/usage` to open the usage menu.
2. Choose whether to show token activity or redeem an available earned reset.
3. To open token activity directly, type `/usage daily`, `/usage weekly`, or `/usage cumulative`.

Expected: Codex opens usage actions or shows account token activity for the
selected view. If the session doesn't have Codex service account auth, Codex
shows a sign-in requirement.

### Inspect config layers with `/debug-config`

1. Type `/debug-config`.
2. Review the output for config layer order (lowest precedence first), on/off
   state, and policy sources.

Expected: Codex prints layer diagnostics plus policy details such as
`allowed_approval_policies`, `allowed_sandbox_modes`, `mcp_servers`, `rules`,
`enforce_residency`, and `experimental_network` when configured.

Use this output to debug why an effective setting differs from `config.toml`.

### Configure footer items with `/statusline`

1. Type `/statusline`.
2. Use the picker to toggle and reorder items, then confirm.

Expected: The footer status line updates immediately and persists to
`tui.status_line` in `config.toml`.

Available status-line items include model, model+reasoning, context stats, rate
limits, git branch, token counters, session id, current directory/project root,
and Codex version.

### Configure terminal title items with `/title`

1. Type `/title`.
2. Use the picker to toggle and reorder items, then confirm.

Expected: The terminal window or tab title updates immediately and persists to
`tui.terminal_title` in `config.toml`.

Available title items include app name, project, spinner, status, thread, git
branch, model, and task progress.

### Choose a syntax theme with `/theme`

1. Type `/theme`.
2. Preview a theme from the picker, then confirm.

Expected: Codex updates syntax highlighting and persists the choice to
`tui.theme` in `config.toml`.

### Choose a terminal pet with `/pets`

1. Type `/pets` (or `/pet`) to open the pet picker.
2. Choose a built-in or custom pet, or turn pets off.

Expected: Codex displays the selected ambient pet in supported terminals and
persists the selection. You can also type `/pets off` to hide it.

### Remap TUI shortcuts with `/keymap`

Use `/keymap` to inspect, update, and persist keyboard shortcut bindings for the TUI.

1. Type `/keymap`.
2. Pick the shortcut context and action you want to change.
3. Enter the new binding or remove the existing one.

Expected: Codex updates the active keymap and writes the custom binding to `tui.keymap` in `config.toml`.

Key bindings use names such as `ctrl-a`, `shift-enter`, and `page-down`. Context-specific bindings override `tui.keymap.global`; an empty binding list unbinds the action.

### Check background terminals with `/ps`

1. Type `/ps`.
2. Review the list of background terminals and their status.

Expected: Codex shows each background terminal's command plus up to three
recent, non-empty output lines so you can gauge progress at a glance.

Background terminals appear when `unified_exec` is in use; otherwise, the list may be empty.

### Stop background terminals with `/stop`

1. Type `/stop`.
2. Confirm if Codex asks before stopping the listed terminals.

Expected: Codex stops all background terminals for the current session. `/clean`
is still available as an alias for `/stop`.

### Keep transcripts lean with `/compact`

1. After a long exchange, type `/compact`.
2. Confirm when Codex offers to summarize the chat so far.

Expected: Codex replaces earlier turns with a concise summary, freeing context
while keeping critical details.

### Review changes with `/diff`

1. Type `/diff` to inspect the Git diff.
2. Scroll through the output inside the CLI to review edits and added files.

Expected: Codex shows changes you've staged, changes you haven't staged yet,
and files Git hasn't started tracking, so you can decide what to keep.

### Highlight files with `/mention`

1. Type `/mention` followed by a path, for example `/mention src/lib/api.ts`.
2. Select the matching result from the popup.

Expected: Codex adds the file to the chat, ensuring follow-up turns reference it directly.

<a id="start-a-new-conversation-with-new"></a>

### Start a new chat with `/new`

1. Type `/new` and press Enter.

Expected: Codex starts a fresh chat in the same CLI session, so you
can switch chats without leaving your terminal.

To name the new chat as you create it, run `/new bug bash`.

Unlike `/clear`, `/new` doesn't clear the current terminal view first.

<a id="rename-the-current-chat-with-rename"></a>
<a id="rename-the-current-task-with-rename"></a>

### Rename the current chat with `/rename`

1. Type `/rename <name>`, or type `/rename` to open the naming prompt.
2. Enter a short name that will help you find the chat later.

Expected: Codex updates the saved chat name without changing its transcript.

<a id="resume-a-saved-conversation-with-resume"></a>

### Resume a saved chat with `/resume`

1. Type `/resume` and press Enter.
2. Choose the session you want from the saved-session picker.

Expected: Codex reloads the selected chat's transcript so you can pick
up where you left off, keeping the original history intact.

<a id="fork-the-current-conversation-with-fork"></a>

### Fork the current chat with `/fork`

1. Type `/fork` and press Enter.

Expected: Codex clones the current chat into a new chat with a fresh
ID, leaving the original transcript untouched so you can explore an alternative
approach in parallel.

If you need to fork a saved session instead of the current one, run
`codex fork` in your terminal to open the session picker.

### Continue in the desktop app with `/app`

On macOS and Windows, type `/app` to open the current session in the ChatGPT
desktop app. If the app isn't installed or running, Codex shows an error asking
you to install or launch it.

Expected: The desktop app opens the same saved chat so you can continue there.

<a id="start-a-side-conversation-with-side"></a>

### Start a side chat with `/side`

Use `/side` to start an ephemeral fork from the current chat without switching away from the main chat.

1. Type `/side` to open a side chat.
2. Optionally add inline text, for example `/side Check whether this plan has an obvious risk`.
3. Return to the parent chat after the focused detour finishes.

Expected: Codex opens a side chat whose transcript is separate from
the parent chat. While you are in side mode, the TUI continues to show the
parent chat's status so you can see whether the main chat is still running.

`/side` is unavailable inside another side chat and during review mode.

### Generate `AGENTS.md` with `/init`

1. Run `/init` in the directory where you want Codex to look for persistent instructions.
2. Review the generated `AGENTS.md`, then edit it to match your repository conventions.

Expected: Codex creates an `AGENTS.md` scaffold you can refine and commit for
future sessions.

### Ask for a working tree review with `/review`

1. Type `/review`.
2. Follow up with `/diff` if you want to inspect the exact file changes.

Expected: Codex summarizes issues it finds in your working tree, focusing on
behavior changes and missing tests. It uses the current session model unless
you set `review_model` in `config.toml`.

### List MCP tools with `/mcp`

1. Type `/mcp`.
2. Review the list to confirm which MCP servers and tools are available.

Expected: You see the configured Model Context Protocol (MCP) tools Codex can call in this session.

Use `/mcp verbose` to include detailed server diagnostics. If you pass anything other than `verbose`, Codex shows the command usage.

### Browse apps with `/apps`

1. Type `/apps`.
2. Pick an app from the list.

Expected: Codex inserts the app mention into the composer as `$app-slug`, so
you can immediately ask Codex to use it.

### Browse plugins with `/plugins`

1. Type `/plugins`.
2. Choose a marketplace tab, then pick a plugin to inspect its capabilities or available actions.

Expected: Codex opens the plugin browser so you can review installed plugins,
discoverable plugins that your configuration allows, and installed plugin state.
Press <kbd>Space</kbd> on an installed plugin to toggle its enabled state.

### View and manage lifecycle hooks with `/hooks`

1. Type `/hooks`.
2. Choose a hook event to inspect the matching handlers.
3. Trust, disable, or re-enable non-managed hooks as needed.

Expected: Codex opens the hook browser so you can review configured lifecycle
hooks. Managed hooks appear as managed and can't be disabled from the user hook
browser.

### Switch agent threads with `/agent`

1. Type `/agent` or `/subagents` and press Enter.
2. Select the thread you want from the picker.

Expected: Codex switches the active thread so you can inspect or continue that
agent's work.

### Send feedback with `/feedback`

1. Type `/feedback` and press Enter.
2. Follow the prompts to include logs or diagnostics.

Expected: Codex collects the requested diagnostics and submits them to the
maintainers.

### Sign out with `/logout`

1. Type `/logout` and press Enter.

Expected: Codex clears local credentials for the current user session.

### Exit the CLI with `/quit` or `/exit`

1. Type `/quit` (or `/exit`) and press Enter.


### 수치·버전·모델명 (원문 표기 그대로, 2026-08-02 기준)

| 항목 | 원문 표기 | 출처 위치 |
|---|---|---|
| 모델명 예시 (플래그 설명) | `gpt-5.6-terra` | `--model, -m` 설명 |
| 모델명 예시 (`/model` 팝업) | `gpt-5.6-luna`, `gpt-5.6-terra` | `/model` 섹션 |
| `codex cloud exec --attempts` 범위 | `1-4`, 기본값 `1` | cloud 표 |
| `codex cloud list --limit` 범위 | `1-20`, 기본값 `20` | cloud list 표 |
| `--ws-max-clock-skew-seconds` 기본값 | `30` | app-server 표 |
| `/goal` 목표 문자열 상한 | "at most 4,000 characters" | `/goal` 섹션 |
| `/ps` 출력 줄 수 | "up to three recent, non-empty output lines" | `/ps` 섹션 |
| 웹 검색 기본 모드 | `web_search = "cached"` (기본), `--search`로 `"live"` | 전역 플래그 |
| `codex completion` 지원 셸 | `bash \| zsh \| fish \| power-shell \| elvish`, 기본 `bash` | completion 표 |

**성숙도(Maturity) 라벨 — experimental로 표기된 명령 (2026-08-02 기준):** `codex app-server`, `codex remote-control`, `codex debug app-server send-message-v2`, `codex debug models`, `codex debug prompt-input`, `codex cloud`, `codex execpolicy`. 나머지 21개는 `stable`.
→ 책에서 "Codex CLI 명령"을 소개할 때 이 7개는 **"실험적 — 예고 없이 바뀔 수 있음"**을 반드시 병기해야 한다. 문서 자체가 `codex app-server`에 대해 "may change without notice"라고 못 박는다.

### 제약·주의사항 (원문)

- `--uncommitted`, `--base`, `--commit`, 커스텀 `PROMPT`는 **서로 충돌**한다. `--title`은 `--commit`과만 쓴다.
- `--force`는 세션 UUID와만 쓴다. 이름 지정 세션은 항상 확인 프롬프트를 거친다.
- `--dangerously-bypass-approvals-and-sandbox`(별칭 `--yolo`)는 "Only use inside an externally hardened environment".
- `--exec --full-auto`는 **deprecated**. "Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used."
- MCP OAuth 액션(`login`/`logout`)은 streamable HTTP 서버에서만, 그것도 서버가 OAuth를 지원할 때만 작동한다.
- `--remote`는 `codex`, `codex resume`, `codex fork`, `codex archive`, `codex delete`, `codex unarchive`에서만 지원. "other subcommands reject remote mode."
- `--remote-auth-token-env` 토큰은 "only sent over `wss://` URLs or local-only `ws://` URLs".
- `/import`는 로컬 TUI 세션에서만. "unavailable while a task is running, in remote sessions, and while connected to the local app-server daemon."
- `/side`는 다른 side chat 안에서와 review 모드에서 사용 불가.
- `/plan`은 Codex가 작업 중일 때 일시적으로 사용 불가.

### Claude Code 대응 관점 메모 (문서 근거 있는 범위만)

문서가 **직접** Claude Code를 언급하는 지점이 있다 — 추측이 아니다:

- **`/import`** — 원문: "Import Claude Code setup, project files, and recent chats." / "Choose the Claude Code setup, project files, or recent chats you want to migrate." → Codex가 Claude Code로부터의 **공식 마이그레이션 경로**를 내장하고 있다. 책의 "Claude Code에서 넘어오기" 장의 1차 근거.
- `AGENTS.md` ↔ Claude Code의 `CLAUDE.md`: `/init`이 "Generate an `AGENTS.md` scaffold in the current directory" — Claude Code `/init`과 같은 이름·같은 역할. 계층(전역 `~/.codex` → repo → 하위 디렉터리, "more specific file closer to your current directory, that guidance wins")도 대응 구조.
- `/compact`, `/status`, `/model`, `/review`, `/mcp`, `/resume`, `/clear` — 이름과 역할이 Claude Code 내장 슬래시 명령과 대응. 단 **`/clear`의 의미가 다르다**: Codex의 `/clear`는 터미널을 지우고 **새 chat을 시작**하며, <kbd>Ctrl</kbd>+<kbd>L</kbd>이 "터미널 뷰만 지우고 현재 chat 유지"다. Claude Code 사용자가 가장 헷갈릴 지점 — 책에서 반드시 짚을 것.
- Codex에만 있는 것: `/fork`(전사 복제), `/side`·`/btw`(임시 곁가지 chat), `/goal`(지속 목표), `/personality`, `/pets`, `/raw`, `/keymap`, `/statusline`, `/title`, `/theme`, `/vim`.
- `codex mcp-server` — Codex 자신을 MCP 서버로 노출. "Useful when another agent consumes Codex." → Claude Code가 Codex를 도구로 부르는 구성이 문서상 가능하다.

### 관련 섹션 (레퍼런스 문서 배치 힌트)

- CLI 레퍼런스 장 전체의 뼈대 (전역 플래그 표 → 명령별 표)
- "Claude Code에서 Codex로" 마이그레이션 장 (`/import`, `AGENTS.md`, 슬래시 명령 대응표)
- 보안·샌드박스 장 (`--sandbox`, `--ask-for-approval`, `--yolo` 경고, `codex sandbox` 3종 OS)
- 자동화·CI 장 (`codex exec`, `--json`, `--output-last-message`, `--output-schema`)
- 플러그인·마켓플레이스 장 (`codex plugin`, `codex plugin marketplace`)

---

## 자료 2: Slash commands in Codex CLI

- URL: https://learn.chatgpt.com/codex/cli/slash-commands (캐노니컬: `/docs/developer-commands?surface=cli`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)
- **자료 1과 동일 문서다.** `curl`로 받은 두 `.md`가 48,301바이트로 바이트 단위 일치. 내용은 자료 1의 "슬래시 명령 전량" 섹션에 이미 전부 수록했다.
- 색인(llms.txt)의 설명문: "Slash commands in Codex CLI: Control Codex during interactive sessions"
- 관련 섹션: 자료 1과 동일. **책에서 두 개의 별도 문서로 취급하지 말 것.**

---

## 자료 3: ChatGPT usage limits and spend controls ★최우선

- URL: https://learn.chatgpt.com/codex/enterprise/usage-limits (캐노니컬: `/docs/enterprise/usage-limits`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)
- 저자·날짜: OpenAI (발행일 미표기)

### ★ 결정적 발견: 이 페이지에는 수치가 하나도 없다

커뮤니티 리서치에서 확인된 "2026-06-16 전후 한도 소모 10~20배 급등" 논쟁과 대조할 **공식 수치를 이 페이지는 제공하지 않는다.** 페이지 전문이 37줄이고, 구체적 숫자·요금·쿼터·리셋 주기가 **단 하나도 없다.** 정책 범위 설명 + 헬프센터 링크로만 구성된 포인터 페이지다.

이것 자체가 fact-check 가능한 사실이다:

> **2026-08-02 기준, OpenAI 공식 Codex 문서의 사용량 한도 페이지는 구체적 한도 수치를 게시하지 않는다.** 수치는 help.openai.com 헬프센터 문서로 위임돼 있다.

### 인용 가능한 구절 (원문 그대로)

> "ChatGPT workspace usage limits and spend controls apply to eligible activity under the plan for the workspace. Depending on the plan, this can include some Codex activity. **These controls aren't a universal Codex limit system and don't govern OpenAI API Platform billing.**"

> "Usage controls don't configure feature entitlement or permissions, although **exhausted limits can pause access to eligible features.** They don't affect source-system permissions or govern Platform API usage or billing."

적용 조건 (원문 목록 그대로):

> - The organization's agreement uses shared or purchased ChatGPT workspace credits.
> - Eligible Codex activity can consume those credits.
> - Administrators need user guardrails, workspace-level spend controls, or usage notifications supported by the current plan.

### 수치·요금·한도

**없음.** 페이지가 위임하는 곳 (여기에 실제 수치가 있을 것 — 미수집, 본 그룹 범위 밖):

- `https://help.openai.com/en/articles/20001001` — "Manage usage limits and overages in ChatGPT Enterprise and Edu"
- `https://help.openai.com/en/articles/20001155` — "Managing credits and spend controls in ChatGPT Business"

### Phase 4 fact-checker에게 (중요)

1. 커뮤니티발 "10~20배 급등" 주장은 **공식 문서로 확인도 반박도 불가능**하다. 책에서 쓴다면 반드시 "커뮤니티 관측·주장"으로 귀속하고 공식 확인 불가를 병기할 것. 판정 등급: **⚠️ (출처는 있으나 1차 확인 불가)**.
2. 개인 요금제(Plus/Pro) 한도는 이 엔터프라이즈 페이지의 범위가 **아니다**. 원문이 "aren't a universal Codex limit system"이라고 명시적으로 선을 긋는다. 개인 요금제 한도를 다루려면 `/codex/pricing`(다른 수집자 담당)을 봐야 한다.
3. 어떤 수치든 인용 시 "{연도·월} 기준"을 못 박을 것. 이 영역은 문서가 헬프센터로 위임돼 있어 예고 없이 바뀐다.

### 관련 섹션

- 요금·한도 장 (단, 이 페이지는 "공식 문서가 수치를 안 준다"는 **부정적 근거**로만 쓸 수 있다)
- 엔터프라이즈 도입 장 (spend control 개념 정의)
- "커뮤니티 논쟁 검증" 성격의 칼럼/사이드바

---

## 자료 4: Custom Prompts ★최우선

- URL: https://learn.chatgpt.com/codex/custom-prompts (캐노니컬: `/docs/custom-prompts`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)

### ★ 결정적 발견: 이 기능은 deprecated다

원문 첫 문장:

> "**Custom prompts are deprecated.** Use [skills](https://learn.chatgpt.com/docs/build-skills) for reusable instructions that Codex can invoke explicitly or implicitly."

> "Custom prompts (deprecated) let you turn Markdown files into reusable prompts that you can invoke as slash commands in both the Codex CLI and the Codex IDE extension."

Deprecated 사유도 원문에 있다 — 왜 skills가 후계인지:

> "Custom prompts require explicit invocation and live in your local Codex home directory (for example, `~/.codex`), so they're not shared through your repository. If you want to share a prompt (or want Codex to implicitly invoke it), use skills."

→ 차이의 축 두 개: **명시적 호출 전용 vs 암묵적 호출 가능**, **로컬 전용 vs 저장소 공유 가능**.

### 설정 키·문법 (원문 그대로)

디렉터리: `~/.codex/prompts/` — 최상위 `.md` 파일만 스캔. 하위 디렉터리 무시. 비-Markdown 파일 무시.

프런트매터 + 본문 예시 (원문 코드 블록 그대로):

```markdown
---
description: Prep a branch, commit, and open a draft PR
argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
---

Create a branch named `dev/<feature_name>` for this work.
If files are specified, stage them first: $FILES.
Commit the staged changes with a clear message.
Open a draft PR on the same branch. Use $PR_TITLE when supplied; otherwise write a concise summary yourself.
```

디렉터리 생성:

```bash
mkdir -p ~/.codex/prompts
```

호출 (원문 그대로):

```text
/prompts:draftpr FILES="src/pages/index.astro src/lib/api.ts" PR_TITLE="Add hero animation"
```

플레이스홀더 규약 (원문 목록):

| 항목 | 원문 규약 |
|---|---|
| Description | YAML 프런트매터 `description:` — 팝업에서 명령 이름 아래 표시 |
| Argument hint | `argument-hint: KEY=<value>` |
| 위치 플레이스홀더 | `$1` ~ `$9` (공백 구분 인자), `$ARGUMENTS`는 전체 |
| 명명 플레이스홀더 | 대문자 `$FILE`, `$TICKET_ID` 등. `KEY=value`로 전달. 공백 포함 값은 따옴표 (`FOCUS="loading state"`) |
| 리터럴 `$` | `$$` → `$` 하나 |

### 제약·주의사항

- 프롬프트 파일을 편집한 뒤 **Codex를 재시작하거나 새 chat을 열어야** 반영된다. 최초 생성 시에도 재시작 필요 (CLI 세션 재시작, IDE 확장은 reload).
- 슬래시 메뉴에서 `/prompts:<name>` 형태로 노출된다.

### Claude Code 대응 관점 메모

- **`~/.codex/prompts/*.md` ↔ Claude Code의 커스텀 슬래시 명령(`~/.claude/commands/*.md` 계열)** — 구조가 거의 1:1이다: Markdown 파일 = 명령, YAML 프런트매터의 `description`, 인자 플레이스홀더(`$1`~`$9`, `$ARGUMENTS`)까지 동일 관용. 대응물이라는 가설은 문서 구조상 강하게 뒷받침된다.
- 단, **중요한 차이**: Codex는 이 경로를 **deprecated 처리하고 skills(`SKILL.md`)로 일원화**했다. 별도 수집된 `/codex/build-skills`가 후계 문서다. Claude Code는 커스텀 슬래시 명령과 Skill을 **둘 다 유지**한다.
- `/prompts:` 네임스페이스 접두사는 Claude Code에는 없는 Codex 고유 관용.
- **책 집필 시 주의:** 이 기능을 "Codex의 커스텀 슬래시 명령 만들기"로 소개하면 **deprecated 기능을 추천하는 셈**이 된다. 반드시 skills 우선으로 서술하고, custom prompts는 "기존 사용자를 위한 레거시"로 배치할 것.
- 저장소 공유가 필요하면 skills를 쓰라는 것이 공식 권고 — Claude Code의 프로젝트 `.claude/commands/`(저장소 커밋 가능)와 대비되는 지점.

### 관련 섹션

- 커스터마이징 장 (레거시 경고와 함께)
- "Claude Code에서 Codex로" 마이그레이션 장 (커스텀 명령 대응표 — deprecated 표시 필수)

---

## 자료 5: Best practices ★최우선

- URL: https://learn.chatgpt.com/codex/learn/best-practices (캐노니컬: `https://learn.chatgpt.com/guides/best-practices`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차, OpenAI 자체 운영 경험 포함)
- 수집 비고: `.md`가 404 → HTML을 pandoc 변환해 복원

### 핵심 주장

전체를 관통하는 프레임: **"설정하고 개선해 나가는 팀원"으로 다루라.**

> "Codex works best when you treat it less like a one-off assistant and more like **a teammate you configure and improve over time**."

전체 워크플로 순서를 문서가 직접 요약한다 — 책의 목차 골격으로 그대로 쓸 수 있다:

> "start with the right context for the task, use `AGENTS.md` for durable guidance, configure Codex to match your workflow, connect external systems with MCP, turn repeated work into skills, and automate stable workflows."

### 인용 가능한 구절

프롬프트 4요소 (원문 그대로) — 책에서 표로 만들기 좋다:

> - **Goal:** What are you trying to change or build?
> - **Context:** Which files, folders, docs, examples, or errors matter for this task? You can @ mention certain files as context.
> - **Constraints:** What standards, architecture, safety requirements, or conventions should Codex follow?
> - **Done when:** What should be true before the task is complete, such as tests passing, behavior changing, or a bug no longer reproducing?

프롬프트가 완벽하지 않아도 된다는 솔직한 서술:

> "Codex is already strong enough to be useful even when your prompt isn't perfect. You can often hand it a hard problem with minimal setup and still get a strong result. Clear prompting isn't required to get value, but it does make results more reliable, especially in larger codebases or higher-stakes tasks."

`AGENTS.md` 정의 — 가장 인용하기 좋은 한 줄:

> "Think of `AGENTS.md` as **an open-format README for agents**."

> "Keep it practical. **A short, accurate `AGENTS.md` is more useful than a long file full of vague rules.** Start with the basics, then add new rules only after you notice repeated mistakes."

> "**When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`.**"

품질 문제가 사실은 설정 문제라는 지적:

> "**Many quality issues are really setup issues**, like the wrong working directory, missing write access, wrong model defaults, or missing tools and connectors."

Skills 판단 기준:

> "A good rule of thumb: **if you keep reusing the same prompt or correcting the same workflow, it should probably become a skill.**"

skills와 scheduled tasks의 역할 분담:

> "**skills define the method and scheduled tasks define the schedule.** If a workflow still needs a lot of steering, turn it into a skill first. Once it's predictable, scheduling it can save time."

chat 단위 원칙:

> "**Keep one chat per coherent unit of work.** If the work is still part of the same problem, staying in the same chat is often better because it preserves the reasoning trail. Fork only when the work truly branches."

### 수치·모델·설정 (2026-08-02 기준)

| 항목 | 원문 표기 |
|---|---|
| OpenAI 내부 코드리뷰 적용률 | **"At OpenAI, Codex reviews 100% of PRs."** |
| Reasoning 레벨 | Low / Medium / High / **Extra High** — "Low for faster, well-scoped tasks / Medium or High for more complex changes or debugging / **Extra High for long, agentic, reasoning-heavy tasks**" |
| Skill 착수 규모 | "Start with **2 to 3 concrete use cases**" |
| MCP 착수 규모 | "Start with **one or two tools** that clearly remove a manual loop" |
| 개인 스킬 경로 | `$HOME/.agents/skills` |
| 팀 공유 스킬 경로 | `.agents/skills` (저장소 내 체크인) |
| 개인 설정 | `~/.codex/config.toml` |
| 저장소 설정 | `.codex/config.toml` |
| 프로필 오버라이드 | `$CODEX_HOME/profile-name.config.toml` |
| 전역 AGENTS.md | `~/.codex` |
| 스킬 스캐폴딩 도구 | `$skill-creator` 스킬 |
| Plan 모드 토글 | `/plan` 또는 **Shift+Tab** |
| MCP 전송 방식 | "Codex supports both **STDIO and Streamable HTTP servers with OAuth**." |

### 코드/설정 예시

설정 계층 권고 (원문 그대로):

```
- Keep personal defaults in ~/.codex/config.toml
  (Settings > Configuration > Open config.toml in the ChatGPT desktop app)
- Keep repo-specific behavior in .codex/config.toml
- Use command-line overrides only for one-off situations (if you use the CLI)
```

좋은 `AGENTS.md`가 담아야 할 것 (원문 목록):

> - repo layout and important directories
> - How to run the project
> - Build, test, and lint commands
> - Engineering conventions and PR expectations
> - Constraints and do-not rules
> - What done means and how to verify work

긴 chat 관리용 CLI 슬래시 명령 (원문 목록 그대로):

> - `/experimental` to toggle experimental features and add to your `config.toml`
> - `/resume` to resume a saved chat
> - `/fork` to create a new chat while preserving the original transcript
> - `/compact` when the chat is getting long and you want a summarized version of earlier context. **Codex also compacts chats automatically**
> - `/agent` when you are running parallel agents and want to switch between the active agent thread
> - `/theme` to choose a syntax highlighting theme
> - `/apps` to use ChatGPT apps directly in Codex
> - `/status` to inspect the current session state

skills가 유용한 반복 업무 (원문 목록): Log triage / Release note drafting / PR review against a checklist / Migration planning / Telemetry or incident summaries / Standard debugging flows

scheduled tasks 후보 (원문 목록): Summarizing recent commits / Scanning for likely bugs / Drafting release notes / Checking CI failures / Producing standup summaries / Running repeatable analysis workflows on a schedule

### ★ "흔한 실수" 목록 (원문 그대로 — 챕터 오프닝용 최상급 소재)

> - Overloading the prompt with durable rules instead of moving them into `AGENTS.md` or a skill
> - Not letting the agent see its work by not giving details on how to best run build and test commands
> - Skipping planning on multi-step and complex tasks
> - Giving Codex full permission to your computer before you understand the workflow
> - Running live tasks on the same files without using Git worktrees
> - Scheduling a recurring task before it's reliable manually
> - Treating Codex like something you have to watch step by step instead of using it in parallel with your own work
> - Using one chat for an entire project instead of one chat per coherent outcome. This leads to bloated context and worse results over time

### 제약·주의사항

- 신규 사용자는 기본 권한으로 시작하라: "Keep approval and sandboxing tight by default, then loosen permissions only for trusted repos or specific workflows **once the need is clear**."
- MCP는 필요할 때만: "Add tools only when they unlock a real workflow. **Do not start by wiring in every tool you use.**"
- 스킬은 처음부터 완벽할 필요 없다: "Don't try to cover every edge case up front."

### Claude Code 대응 관점 메모

- `AGENTS.md` ↔ `CLAUDE.md`: 계층 구조(전역/repo/하위 디렉터리, 가까운 것이 이김), `/init` 스캐폴딩, "짧고 정확한 것이 낫다"는 조언까지 대응. **"Codex가 같은 실수를 두 번 하면 회고를 시켜 AGENTS.md를 갱신하라"**는 조언은 Claude Code 운영 노하우와 그대로 겹친다.
- Plan 모드 **Shift+Tab** 토글 — Claude Code의 모드 전환 키와 같은 관용.
- `$HOME/.agents/skills` / `.agents/skills` 경로는 Claude Code의 `.claude/skills`와 대응하되 **디렉터리 이름이 벤더 중립(`.agents`)**이라는 점이 다르다. 이 명명 선택 자체가 책에서 다룰 만한 논점.
- `$skill-creator`, `$app-slug` 등 **`$` 접두사로 스킬·앱을 명시 호출**하는 관용은 Codex 고유 (Claude Code는 `/`).
- Codex는 chat 관리 명령이 훨씬 풍부하다(`/fork`, `/side`, `/agent`, `/goal`). Claude Code 사용자에게 "새로 배울 것"으로 묶어 소개하기 좋다.

### 관련 섹션

- 입문 장 / 프롬프트 장 (4요소 프레임, reasoning 레벨 선택)
- `AGENTS.md` 장 (핵심 인용 다수)
- 설정 장 (config.toml 3계층)
- MCP 장 / Skills 장 / 자동화 장
- **마지막 장 또는 각 장 말미의 "흔한 실수"** — 위 8개 목록이 그대로 쓸 수 있는 재료

---

## 자료 6: Overview (ChatGPT / Codex 랜딩)

- URL: https://learn.chatgpt.com/codex/overview (캐노니컬: `https://learn.chatgpt.com/docs`)
- 검색: 2026-08-02 기준
- 신뢰성: **중** (내용이 아니라 마케팅 랜딩 페이지 — 산문 정보량이 거의 없다)
- 수집 비고: `.md` 404 → HTML 복원. 복원 결과 본문 대부분이 **UI 목업 일러스트레이션**이고 산문은 한 문단뿐이다.
- 색인상 제목: "ChatGPT — Use ChatGPT for ambitious work and software development"

### 핵심 내용 (실질적으로 이게 전부)

> "Start with a goal, idea, or task. ChatGPT can gather context, take action, and produce something useful."

홈 화면 목업이 노출하는 진입 4분류 (원문 그대로) — 제품이 스스로 정의한 유스케이스 축:

> - Explore and understand code
> - Build a new feature, app, or tool
> - Review code and suggest changes
> - Fix issues and failures

목업 사이드바 항목: New chat (⌘N) / Search (⌘K) / Scheduled / Plugins / Sites / Pull requests / Pinned / Projects / Chats

### 수치·모델명 (2026-08-02 기준)

| 항목 | 원문 표기 | 비고 |
|---|---|---|
| UI 목업의 모델 선택 표시 | **"5.6 Sol Extra High"** | ⚠️ 목업 스크린샷 내 문자열이다. 실사용 모델 카탈로그의 정식 표기가 아닐 수 있다 |

> **Phase 4 fact-checker 주의:** `5.6 Sol`은 CLI 레퍼런스가 예시로 드는 `gpt-5.6-luna` / `gpt-5.6-terra`와 **다른 세 번째 이름**이다. 세 이름이 같은 계열의 다른 티어인지 확인되지 않았다. 모델 라인업을 서술하려면 `/codex/models`(다른 수집자 담당)를 1차 출처로 삼고, 이 목업 문자열은 **단독 근거로 쓰지 말 것.** 판정: **⚠️ 교차 확인 필요.**

### 제약

- 이 페이지는 책의 사실 근거로서 가치가 낮다. "제품이 스스로를 어떻게 포지셔닝하는가"의 근거로만 쓸 것.
- 페이지가 링크하는 `/codex/use-cases`는 **404다** (아래 "미수집 잔여 URL" 참조).

### 관련 섹션

- 도입부 / "Codex란 무엇인가" 장의 포지셔닝 인용
- 유스케이스 4분류는 책 전체 구조의 참조점으로 쓸 만하다

---

## 자료 7: Building an AI-Native Engineering Team

- URL: https://learn.chatgpt.com/codex/guides/build-ai-native-engineering-team (캐노니컬: `https://learn.chatgpt.com/guides/build-ai-native-engineering-team`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차 + 외부 연구 인용 + 실명 고객 사례)
- 수집 비고: `.md` 404 → HTML 복원

### 핵심 주장

SDLC 7단계(Plan → Design → Build → Test → Review → Document → Deploy/Maintain) 각각에 대해 **Delegate / Review / Own** 3분할 표를 제시한다. 이 프레임이 이 문서의 골격이자 가장 재사용 가치가 높은 자산이다.

### ★ 수치·연구 인용 (원문 그대로, 출처 귀속 주의)

| 항목 | 원문 표기 | 귀속 |
|---|---|---|
| 모델 지속 추론 시간 | "**as of August 2025**, METR found that leading models could complete **2 hours and 17 minutes** of continuous work with roughly **50% confidence** of producing a correct answer" | **METR 연구** (OpenAI 자체 측정 아님) |
| 능력 배증 주기 | "task length **doubling about every seven months**" | 동 문맥 |
| 과거 대비 | "Only a few years ago, models could manage about **30 seconds** of reasoning" | 동 문맥 |
| 코드리뷰 소요 시간 | "On average, developers spend **2–5 hours per week** conducting code reviews." | 출처 미표기 ⚠️ |
| OpenAI 내부 효과 | "work that once required **weeks** now being delivered in **days**" | OpenAI 자체 주장 |

> **Phase 4 fact-checker 필독:**
> 1. "2시간 17분 / 50% 신뢰도"는 **METR의 연구 결과**이지 OpenAI의 측정이 아니다. 인용 시 반드시 METR로 귀속하고 **"2025년 8월 기준"**을 병기할 것. 이 책이 2026년에 나온다면 **1년 이상 묵은 수치**다 — "구버전 정보일 수 있음" 표시 대상.
> 2. "7개월마다 배증"이 사실이라면 2025-08 → 2026-08은 약 1.7배증 구간이다. 원문 수치를 현재 시점으로 **외삽하지 말 것** (문서에 없는 계산이다).
> 3. "주당 2~5시간 코드리뷰"는 **출처가 표기되지 않은 수치**다. 인용한다면 "OpenAI 가이드의 주장"으로 귀속. 판정: **⚠️**.
> 4. 이 페이지 전체가 마케팅 성격의 리더십 가이드다. 기술적 사실(플래그·API)의 근거로 쓰지 말 것.

### 인용 가능한 구절

역할 이동의 핵심 문장:

> "In practice, this shifts much of the mechanical 'build work' from engineers to agents. **The agent becomes the first-pass implementer; the engineer becomes the reviewer, editor, and source of direction.**"

여전히 사람이 소유하는 것:

> "**True ownership of code—especially for new or ambiguous problems—still rests with engineers**, and certain challenges exceed the capabilities of current models."

테스트가 진실의 원천이 된다는 관점 — 책에서 강조할 만한 반전:

> "as agents remove barriers to generating code, **tests serve a more and more important function as a source of truth for application functionality.** Since agents can run the test suite and iterate based on the output, defining high quality tests is often the first step to allowing an agent to build a feature."

AI 코드리뷰의 한계에 대한 솔직한 서술:

> "models must be trained specifically to identify P0 and P1-level bugs, and tuned to provide concise, high-signal feedback; **overly verbose responses are ignored just as easily as noisy lint warnings.**"

> "Code review doesn't necessarily make the pull request process faster, especially if it finds meaningful bugs – **but it does prevent defects and outages.**"

리뷰 도구 선택 조언:

> "Select a product that has a model specifically trained on code review. **We've found that generalized models often nitpick and provide a low signal to noise ratio.**"

### 실명 고객 사례 (원문 그대로 — 책의 사례 소재)

| 회사 | 원문 |
|---|---|
| **Cloudwalk** | "Engineers, PMs, designers, and operators at Cloudwalk use Codex daily to turn specs into working code whether they need a script, a new fraud rule, or a full microservice delivered in minutes." |
| **Sansan** | "Sansan uses Codex review for **race conditions and database relations**, which are issues humans often overlook. Codex has also been able to catch improper hard-coding and even anticipates future scalability concerns." |
| **Virgin Atlantic** | "Virgin Atlantic uses Codex to strengthen how teams deploy and maintain their systems. The Codex VS Code Extension gives engineers a single place to investigate logs, trace issues across code and data, and review changes through **Azure DevOps MCP and Databricks Managed MCPs**." |

### 능력 4분류 표 (원문 그대로)

| Capability | What It Enables |
|---|---|
| **Unified context across systems** | A single model can read code, configuration, and telemetry, providing consistent reasoning across layers that previously required separate tooling. |
| **Structured tool execution** | Models can now call compilers, test runners, and scanners directly, producing verifiable results rather than static suggestions. |
| **Persistent project memory** | Long context windows and techniques like compaction allow models to follow a feature from proposal to deployment, remembering previous design choices and constraints. |
| **Evaluation loops** | Model outputs can be tested automatically against benchmarks—unit tests, latency targets, or style guides—so improvements are grounded in measurable quality. |

### 단계별 착수 체크리스트 (원문 그대로 — 실천 섹션 재료)

**Build:** Start with well specified tasks / Have the agent use a planning tool via MCP, or by writing a PLAN.md file that is committed to the codebase / Check that the commands the agent attempts to execute are succeeding / Iterate on an AGENTS.md file that unlocks agentic loops like running tests and linters to receive feedback

**Test:** Guide the model to implement tests as a separate step, and **validate that new tests fail before moving to feature implementation** / Set guidelines for test coverage in your AGENTS.md file / Give the agent specific examples of code coverage tools it can call

**Review:** Curate examples of gold-standard PRs ... Save this as an evaluation set to measure different tools / Select a product that has a model specifically trained on code review / **Define how your team will measure whether reviews are high quality. We recommend tracking PR comment reactions as a low-friction way to mark good and bad reviews.** / Start small but rollout quickly once you gain confidence

**Design:** Use a multi-modal coding agent that accepts both text and image input / Integrate design tools via MCP / Programmatically expose component libraries with MCP / Build workflows that map designs → components → implementation / **Utilize typed languages (e.g. Typescript) to define valid props and subcomponents for the agent**

### Claude Code 대응 관점 메모

- Delegate / Review / Own 3분할은 **벤더 중립 프레임**이다. Claude Code 병행 사용 팀에도 그대로 적용된다 — 책에서 "도구 무관 운영 원칙" 장의 근거로 쓸 수 있다.
- 문서가 Claude Code를 언급하지는 않는다. 대응 서술은 이 페이지 근거로 하지 말 것.

### 관련 섹션

- 팀 도입 / 조직 운영 장 (이 문서 하나로 한 장이 나온다)
- 코드리뷰 장 (Sansan 사례, 리뷰 품질 측정법)
- 테스트 장 ("테스트가 진실의 원천" 논지)
- 서문 / 도입부 (METR 수치 — 단, 연도 병기 필수)

---

## 자료 8: Codex for Open Source

- URL: https://learn.chatgpt.com/codex/community/codex-for-oss (캐노니컬: `https://developers.openai.com/community/codex-for-oss`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차, 프로그램 안내)
- 수집 비고: `.md` 404 → HTML 복원

### 핵심 내용

> "Open-source maintainers can apply for API credits, six months of ChatGPT Pro with Codex, and Codex Security."

> "Over the past year, the **Codex Open Source Fund ($1 million)** has supported projects that need API credits, including teams using Codex to power GitHub pull request workflows."

### 수치·프로그램 조건 (2026-08-02 기준)

| 항목 | 원문 표기 |
|---|---|
| 기금 규모 | **"$1 million"** (Codex Open Source Fund) |
| 제공 기간 | **"six months of ChatGPT Pro with Codex"** |
| Codex Security | **"conditional access"** — "for core maintainers with write access" |
| 기간 표현 | "Over the past year" (기준 시점 명시 없음 ⚠️) |

프로그램 구성 (원문 목록 그대로):

> - Six months of ChatGPT Pro with Codex for day-to-day coding, triage, review, and maintainer workflows
> - Conditional access to Codex Security for repositories that need deeper security coverage
> - API credits through the Codex Open Source Fund for projects that use Codex in pull request review, maintainer automation, release workflows, or other core OSS work

### ★ 주목할 서술: 경쟁 도구를 명시적으로 허용한다

> "Developers should code in the tools they prefer, whether that's Codex, **OpenCode, Cline, pi, OpenClaw**, or something else, and this program supports that work."

링크된 저장소 (원문 그대로):
- OpenCode — `https://github.com/anomalyco/opencode`
- Cline — `https://github.com/cline/cline`
- pi — `https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent`
- OpenClaw — `https://github.com/openclaw/openclaw`

→ OpenAI 공식 문서가 **경쟁 코딩 에이전트를 실명으로 열거하며 지원 대상에 포함**한다. 책에서 "Codex의 생태계 포지셔닝"을 다룰 때 강한 1차 근거.

### 모델명

> "Given **GPT-5.4's** capabilities, the team reviews Codex Security access case by case to ensure these workflows get the care and diligence they require."

> ⚠️ **fact-checker 주의:** 이 페이지는 **GPT-5.4**를 언급하는데, CLI 레퍼런스는 `gpt-5.6-terra`/`gpt-5.6-luna`를, 오버뷰 목업은 "5.6 Sol"을 표시한다. **문서 간 모델 버전이 불일치**한다 — 이 페이지가 갱신이 덜 된 것으로 보인다. 모델 서술은 `/codex/models`를 1차 출처로 삼을 것. 판정: **🕒 (구버전 정보 가능성 높음)**.

### 지원 자격 (원문)

> "If you're a core maintainer or run a widely used public project, apply. If your project doesn't fit the criteria but it plays an important role in the ecosystem, **apply anyway and explain why.**"

- 신청 폼: `https://openai.com/form/codex-for-oss/`
- 약관: `/codex/codex-for-oss-terms` (색인에 없는 페이지 — 존재는 확인됨, 본 그룹 범위 밖)

### 관련 섹션

- 부록 "무료·할인 이용 경로"
- 생태계·포지셔닝 장 (경쟁 도구 열거 인용)

---

## 자료 9: ChatGPT desktop app — Commands (앱 명령·단축키·딥링크)

- URL: https://learn.chatgpt.com/codex/app/commands (캐노니컬: `/docs/reference/commands`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)

### 핵심 내용

ChatGPT 데스크톱 앱의 (a) 키보드 단축키 전량, (b) `codex://` **딥링크 URL 스킴** 전량. 딥링크는 다른 문서에 없는 고유 정보다.

### 키보드 단축키 전량 (원문 표 그대로)

| 구분 | Action | Shortcut |
|---|---|---|
| **General** | Command menu | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> 또는 <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>K</kbd> |
| | Settings | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>,</kbd> |
| | Keyboard shortcuts | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>/</kbd> |
| | Open folder | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>O</kbd> |
| | Navigate back | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>[</kbd> |
| | Navigate forward | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>]</kbd> |
| | Increase font size | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>+</kbd> |
| | Decrease font size | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>-</kbd> |
| | Toggle sidebar | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>B</kbd> |
| | Open review tab | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> |
| | Toggle review panel | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>B</kbd> |
| | Toggle bottom panel | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>J</kbd> |
| | Toggle terminal | <kbd>Ctrl</kbd> + <kbd>`</kbd> |
| | Clear the terminal | <kbd>Ctrl</kbd> + <kbd>L</kbd> |
| **Chat** | Quick chat | <kbd>Cmd</kbd> + <kbd>Option</kbd> + <kbd>N</kbd> (macOS) 또는 <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>N</kbd> (Windows) |
| | New chat | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>N</kbd> 또는 <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> |
| | Search chats | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>G</kbd> |
| | Find in chat | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>F</kbd> |
| | Previous chat | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>[</kbd> |
| | Next chat | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>]</kbd> |
| **Input** | Dictation | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd> |

### 딥링크 `codex://` 전량 (원문 표 그대로)

정식 형태 요약표:

| Deep link | Opens |
|---|---|
| `codex://threads/new` | A new local chat. |
| `codex://new?<query>` | A new local chat with at least one query parameter. |
| `codex://threads/<thread-id>` | A local chat. `<thread-id>` is its technical thread ID. |
| `codex://settings` | Settings. |
| `codex://settings/connections/<connection-type>` | Computer, device, or SSH connection settings. |
| `codex://settings/connections/ssh/add?name=<ssh-config-host>` | Adds a host from your SSH config to Codex. |
| `codex://skills` | Skills. |
| `codex://automations` | Scheduled with the create flow open. |
| `codex://plugins/install/<plugin-name>?marketplace=<marketplace-name>` | The install flow for a plugin from a known marketplace. |
| `codex://plugins/<plugin-id>` | A plugin detail page. |
| `codex://plugins/<plugin-name>?marketplacePath=<absolute-marketplace-path>` | A local plugin detail page from a local marketplace. |
| `codex://pets/install?name=<pet-name>&imageUrl=<https-image-url>` | The pet install flow. |

**chat 링크 쿼리 파라미터** (원문 표):

| Query parameter | Required | What it does |
|---|---|---|
| `prompt=<text>` | No | Sets the initial composer text. |
| `path=<absolute-path>` | No | Opens the new chat in a local workspace. `path` must be an absolute path to a local directory. When valid, Codex uses that directory as the active workspace. |
| `originUrl=<git-remote-url>` | No | Matches one of your current workspace roots by Git remote URL. If `path` is also present, Codex resolves `path` first. |

**설정 딥링크** (원문 표):

| Deep link | Opens |
|---|---|
| `codex://settings` | Settings. |
| `codex://settings/browser-use` | Browser settings. |
| `codex://settings/computer-use/google-chrome` | Google Chrome settings for computer use. |
| `codex://settings/connections` | Remote connections settings. |
| `codex://settings/connections/computer` | Settings for controlling this Mac or PC from another device. |
| `codex://settings/connections/devices` | Settings for controlling other devices. |
| `codex://settings/connections/ssh` | SSH connection settings. |
| `codex://settings/connections/ssh/add?name=<ssh-config-host>` | Adds the named host alias as a Codex-managed connection, then opens SSH connection settings. |

**플러그인 딥링크 파라미터** (원문 표):

| Query parameter | Required | What it does |
|---|---|---|
| `marketplace=<marketplace-name>` | Yes | Identifies the marketplace. For an OpenAI-curated plugin, use `openai-curated`. |
| `hostId=<host-id>` | No | Identifies the Codex host that owns the plugin context, such as `local` or one of your configured remote connections. Codex provides these IDs. |
| `source=manage` | No | Preserves the app's plugin-management entry point. It's not admin-only. |
| `marketplacePath=<absolute-marketplace-path>` | Yes (local) | Absolute path to the local `marketplace.json`, for example `/Users/alex/.agents/plugins/marketplace.json`. |
| `mode=share` | No | Opens the share flow for that local plugin. |

**펫 딥링크 파라미터** (원문 표):

| Query parameter | Required | What it does |
|---|---|---|
| `name=<pet-name>` | Yes | Sets the pet name. The value must contain at least one non-whitespace character. |
| `imageUrl=<https-image-url>` | Yes | Provides an absolute HTTPS URL for the pet image or sprite sheet. |
| `description=<text>` | No | Adds a description to the install flow. |
| `spriteVersionNumber=<1-or-2>` | No | Selects the sprite-sheet format. **The default is `1`; the only other supported value is `2`.** |

### 코드/설정 예시 (원문 그대로)

플러그인 멘션을 포함한 프롬프트:

```text
[@Example](plugin://example@openai-curated) Summarize this document: https://example.com/document/123
```

인코딩 후 딥링크:

```text
codex://new?prompt=%5B%40Example%5D(plugin%3A%2F%2Fexample%40openai-curated)%20Summarize%20this%20document%3A%20https%3A%2F%2Fexample.com%2Fdocument%2F123
```

### 제약·주의사항

- "Encode query string values before adding them to a URL."
- 딥링크는 프롬프트를 composer에 넣을 뿐 **자동 전송하지 않는다**: "It doesn't send the prompt automatically."
- `codex://new?<query>`는 `prompt`, `path`, `originUrl` 중 **최소 하나가 없으면 아무 동작도 하지 않는다.**
- 지원하지 않는 `codex://settings/...` 경로는 메인 Settings로 열린다.
- SSH `name` 값은 `~/.ssh/config`의 host alias와 일치해야 한다. 링크는 해당 host의 자동 연결을 비활성화한다.
- 펫 링크: 잘못된 이름, 비-HTTPS 이미지 URL, 미지원 sprite 버전, 추가 경로 세그먼트는 **링크를 무동작으로 만든다.**
- `codex://` 스킴은 **하위호환용으로 유지**되는 것이다: "The ChatGPT desktop app **keeps** the `codex://` URL scheme for compatibility" → 제품이 ChatGPT 앱으로 리브랜딩되는 과정의 흔적. 책에서 명명 변천을 다룰 근거.

### Claude Code 대응 관점 메모

- 딥링크 URL 스킴은 Claude Code에 대응물이 없는 **Codex(데스크톱 앱) 고유 기능**이다. 사내 툴·대시보드에서 Codex 작업을 킥오프하는 통합 패턴으로 소개할 가치가 있다.
- 문서가 Claude Code를 언급하지 않으므로 그 이상의 대응 주장은 하지 말 것.

### 관련 섹션

- 데스크톱 앱 장 (단축키 표 그대로)
- 통합·자동화 장 (딥링크 — 사내 도구 연동 레시피)

---

## 자료 10: ChatGPT desktop app — Settings

- URL: https://learn.chatgpt.com/codex/app/settings (캐노니컬: `/docs/reference/settings`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)
- **별칭 주의:** `/codex/reference/settings`와 동일 문서(5,038바이트 일치).

### 핵심 내용

데스크톱 앱 설정 패널의 섹션별 안내. **설정 키가 아니라 UI 메뉴 서술**이라 `config.toml` 키 표는 없다.

설정 열기: 앱 메뉴 또는 <kbd>Cmd</kbd>+<kbd>,</kbd> (macOS) / <kbd>Ctrl</kbd>+<kbd>,</kbd> (Windows). 딥링크 `codex://settings`.

### 설정 섹션별 내용 (원문 근거)

| 섹션 | 내용 |
|---|---|
| **General** | 멀티라인 프롬프트에 <kbd>Cmd</kbd>+<kbd>Enter</kbd> 요구 설정, **Prevent sleep while running**, **Follow-up behavior**(실행 중 보낸 메시지가 현재 실행을 steer할지 다음 실행을 기다릴지) |
| **Profile** | activity insights, lifetime tokens, peak tokens, streaks, longest task, token activity. 프로필 사진·표시 이름·사용자명 수정, 사용 하이라이트 프로필 카드 저장. **"Sharing profile cards is available on consumer ChatGPT plans."** 자격 있는 사용자는 **Invite a friend**(개인 요금제) / **Invite a coworker**(Business 워크스페이스) |
| **Keyboard shortcuts** | 바인딩 변경·초기화. 명령명 검색 또는 키스트로크 검색 |
| **Notifications** | 턴 완료 알림 시점, 알림 권한 요청 여부 |
| **Appearance** | 베이스 테마, accent/background/foreground 색, UI·코드 폰트. **"You can also share your custom theme with friends."** |
| **Pets** | 내장/커스텀 펫 선택. `/pet`, **Wake Pet**, **Tuck Away Pet**로 오버레이 제어 |
| **Browser** | 번들 Browser 플러그인 설치·활성화, Chrome 확장 설정, 허용/차단 사이트 관리. "ChatGPT asks before using a website unless you've allowed it." |
| **Computer Use** | 데스크톱 앱 접근 권한 검토. macOS는 **Screen Recording / Accessibility** 권한을 시스템 설정에서 회수 |
| **Personalization** | **Friendly / Pragmatic / None** 기본 personality. "Use **None** to disable personality instructions." 커스텀 지시 편집은 **`AGENTS.md`의 personal instructions를 갱신한다** |
| **Suggested prompts** | 컨텍스트 인식 후속 제안 |
| **Memories** | 과거 chat 컨텍스트 이월 (사용 가능한 경우) |
| **Archived chats** | 날짜·프로젝트 컨텍스트와 함께 목록. **Unarchive**로 복원 |
| **Keep a chat near your work** | 활성 chat을 별도 창으로 pop out. **Always on top** 옵션 |

### ★ 주목할 연결점

> "Editing custom instructions updates your **personal instructions in `AGENTS.md`**."

→ GUI 설정과 `AGENTS.md` 파일이 **같은 저장소를 공유**한다. CLI·IDE·앱이 설정 계층을 공유한다는 best-practices의 서술과 맞물리는 구체적 증거.

Personality 3종(`friendly`, `pragmatic`, `none`)은 CLI `/personality`의 값과 **정확히 일치**한다 (자료 1 교차 확인 완료 ✅).

### 관련 섹션

- 데스크톱 앱 장
- 설정 통합 장 (GUI ↔ `AGENTS.md` ↔ `config.toml` 관계)

---

## 자료 11: ChatGPT desktop app for Windows

- URL: https://learn.chatgpt.com/codex/app/windows (캐노니컬: `/docs/windows/windows-app`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)

### 핵심 내용

Windows 네이티브 실행(PowerShell + Windows 샌드박스) vs WSL2 실행의 선택과 트레이드오프. 한국 개발자 독자 비중을 고려하면 실용 가치가 높은 장.

> "It runs natively on Windows using PowerShell and the Windows sandbox, or you can configure it to run in Windows Subsystem for Linux 2 (WSL2)."

### ★ 버전 수치 (2026-08-02 기준 — fact-check 대상)

| 항목 | 원문 표기 |
|---|---|
| WSL1 지원 종료 | **"WSL1 was supported through Codex `0.114`. Starting in Codex `0.115`, the Linux sandbox moved to `bubblewrap`, so WSL1 is no longer supported."** |

> 이 문서 전체에서 **유일하게 구체적 Codex 버전 번호가 나오는 지점**이다. `0.114` / `0.115` 경계와 `bubblewrap` 전환은 fact-checker가 대조할 수 있는 명확한 사실. 인용 시 "Codex 0.115 이후" 형태로 못 박을 것.

### 설정 키·명령 (원문 그대로)

Microsoft Store ID: `9PLM9XGG6VKS`

설치:

```powershell
winget install --id 9PLM9XGG6VKS -s msstore
```

권장 개발 도구 설치 (원문 코드 블록 그대로):

```powershell
winget install --id Git.Git
winget install --id OpenJS.NodeJS.LTS
winget install --id Python.Python.3.14
winget install --id Microsoft.DotNet.SDK.10
winget install --id GitHub.cli
```

> ⚠️ 이 목록의 `Python.Python.3.14`, `Microsoft.DotNet.SDK.10`은 **2026-08-02 기준 문서 표기**다. 버전 고정 패키지 ID이므로 시간이 지나면 낡는다. 책에 넣는다면 "문서 기준 예시이며 최신 버전으로 바꿔 쓰라"는 단서를 달 것. 판정: **🕒**.

PowerShell 실행 정책 오류와 해결 (원문 그대로):

```text
npm.ps1 cannot be loaded because running scripts is disabled on this system.
```

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

WSL에서 Windows Codex 홈 공유:

```bash
export CODEX_HOME=/mnt/c/Users/<windows-user>/.codex
```

### 경로·환경 변수

| 항목 | 값 |
|---|---|
| Windows Codex 홈 | `%USERPROFILE%\.codex` |
| 홈 오버라이드 환경변수 | `CODEX_HOME` |
| WSL 파일시스템 접근 | 파일 탐색기에 `\\wsl$\` 입력 |
| 권장 프로젝트 접근 경로 | `/mnt/<drive>/...` |

### 통합 터미널 선택지 (원문 목록)

> PowerShell / Command Prompt / Git Bash / WSL

- "This change applies only to new terminal sessions." 이미 열린 터미널이 있으면 앱 재시작 또는 새 chat 필요.

### 권장 개발 도구와 이유 (원문 그대로)

> - **Git**: Powers the review panel in the ChatGPT desktop app and lets you inspect or revert changes.
> - **Node.js**: A common tool that the agent uses to perform tasks more efficiently.
> - **Python**: A common tool that the agent uses to perform tasks more efficiently.
> - **.NET SDK**: Useful when you want to build native Windows apps.
> - **GitHub CLI**: Powers GitHub-specific functionality in the ChatGPT desktop app.

GitHub CLI 설치 후 `gh auth login` 필요.

### 제약·주의사항 (원문)

- **전체 접근 모드 경고:** "Running Codex in full access mode means Codex is not limited to your project directory and might perform unintentional destructive actions that can lead to data loss."
- 샌드박스 적용법: "To apply sandbox protections in either mode, select **Ask for approval** beneath the composer before sending messages to Codex."
- 에이전트를 WSL로 바꾸면 **반드시 앱을 재시작**해야 한다: "The change doesn't take effect until you restart."
- Windows 네이티브 에이전트를 쓸 거라면 프로젝트를 Windows 파일시스템에 두는 편이 낫다: "This setup is more reliable than opening projects directly from the WSL filesystem."
- WSL의 CLI는 Linux 홈을 쓰므로 **설정·인증·세션 히스토리가 Windows 앱과 자동 공유되지 않는다.**
- Git 미설치 시 리뷰 패널 등 일부 기능 불가.
- `\\wsl$` 경로로 연 프로젝트는 Git 감지가 안 될 수 있다 (알려진 제약, 워크어라운드는 `/mnt/<drive>/`).
- 관리자 권한이 필요하면 **앱 자체를 관리자로 실행**한다 — "The Codex agent inherits that permission level."
- `Cmder`가 열기 대화상자에 없으면 시작 메뉴에 추가 후 재시작.
- 에이전트와 통합 터미널은 **독립적으로** 설정된다. "You can keep the agent in WSL and still use PowerShell in the terminal."

### 관련 섹션

- Windows 환경 설정 장 (한국 독자 대상 실용 가치 높음)
- 샌드박스·보안 장 (Windows 샌드박스 vs bubblewrap)
- 트러블슈팅 부록 (실행 정책, Git 감지, Cmder)

---

## 자료 12: Codex IDE extension — Developer commands

- URL: https://learn.chatgpt.com/codex/ide/commands (캐노니컬: `/docs/developer-commands?surface=ide`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)
- **동일 문서:** `/codex/ide/slash-commands`와 바이트 단위 동일(4,875바이트). 자료 13은 이 문서와 같다.

### VS Code 확장 명령 전량 (원문 표 그대로)

| Command | Default key binding | Description |
|---|---|---|
| `chatgpt.addToThread` | - | Add selected text range as context for the current chat |
| `chatgpt.addFileToThread` | - | Add the entire file as context for the current chat |
| `chatgpt.newChat` | macOS: `Cmd+N`<br>Windows/Linux: `Ctrl+N` | Create a new chat |
| `chatgpt.newCodexPanel` | - | Create a new Codex panel |
| `chatgpt.openCommandMenu` | - | Open the Codex command menu |
| `chatgpt.openSidebar` | - | Open the Codex sidebar panel |

키 바인딩 지정 절차 (원문): Command Palette(**Cmd+Shift+P** / **Ctrl+Shift+P**) → **Preferences: Open Keyboard Shortcuts** → `Codex` 또는 명령 ID(예: `chatgpt.newChat`) 검색 → 연필 아이콘.

### IDE 슬래시 명령 전량 (원문 표 그대로)

| Slash command | Description |
|---|---|
| `/approve` | Approve one retry of a recent automatic-review denial, when automatic review is active. |
| `/cloud` | Run the chat in the cloud, when cloud execution is available. |
| `/cloud-environment` | Choose the cloud environment for the chat. |
| `/compact` | Compact the current chat's context. |
| `/fast` | Turn a catalog-provided Fast service tier on or off, when available. |
| `/feedback` | Open the feedback dialog to submit feedback and optionally include logs. |
| `/fork` | Copy a local chat into a new local chat. |
| `/goal` | Set a persistent goal for Codex to work toward. |
| `/ide-context` | Turn automatic IDE context on or off. |
| `/init` | Generate an `AGENTS.md` scaffold for the current project. |
| `/local` | Run the chat in your local workspace. |
| `/mcp` | Open MCP status to view connected servers. |
| `/memories` | Configure whether the chat can use or generate memories, when Memories is available. |
| `/model` | Choose the model for the current chat. |
| `/personality` | Choose how Codex responds, when the current model supports personalities. |
| `/plan` | Toggle plan mode for multi-step planning. |
| `/project` | Choose a project for new chats. |
| `/reasoning` | Choose the reasoning effort for the current chat. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/side` | Start a temporary side chat without interrupting the main chat. |
| `/status` | Show the chat ID, context usage, and rate limits. |
| `/worktree` | Run the chat in a new Git worktree. |

### ★ 표면 간 슬래시 명령 차이 (교차 대조 결과 — 책의 핵심 표가 될 자산)

CLI(자료 1)·IDE(이 자료)·앱(자료 15) 세 표면의 슬래시 명령이 **서로 다르다.** 이 차이 자체가 책의 고유 가치다.

| 명령 | CLI | IDE | 데스크톱 앱 |
|---|---|---|---|
| `/cloud`, `/cloud-environment` | ✗ | ✓ | ✓ |
| `/local` | ✗ | ✓ | ✓ |
| `/project` | ✗ | ✓ | ✓ |
| `/reasoning` | ✗ (CLI는 `/model`에 통합) | ✓ | ✓ |
| `/worktree` | ✗ | ✓ | ✓ |
| `/ide-context` | ✗ (CLI는 `/ide`) | ✓ | ✗ |
| `/task` | ✗ | ✗ | ✓ |
| `/pet` | ✓ (`/pets`, `/pet`) | ✗ | ✓ |
| `/permissions`, `/sandbox-add-read-dir`, `/setup-default-sandbox` | ✓ | ✗ | ✗ |
| `/keymap`, `/vim`, `/raw`, `/theme`, `/statusline`, `/title` | ✓ | ✗ | ✗ |
| `/archive`, `/delete`, `/rename`, `/new`, `/clear`, `/resume` | ✓ | ✗ | ✗ |
| `/apps`, `/plugins`, `/hooks`, `/skills`, `/import` | ✓ | ✗ | ✗ |
| `/agent`, `/subagents` | ✓ | ✗ | ✗ |
| `/diff`, `/mention`, `/copy`, `/ps`, `/stop` | ✓ | ✗ | ✗ |
| `/usage`, `/debug-config`, `/experimental`, `/logout`, `/quit`, `/exit` | ✓ | ✗ | ✗ |
| `/app` | ✓ | ✗ | ✗ |
| 공통 (3면 모두) | \multicolumn — `/approve` `/compact` `/fast` `/feedback` `/fork` `/goal` `/init` `/mcp` `/memories` `/model` `/personality` `/plan` `/review` `/side` `/status` | | |

> **CLI가 압도적으로 명령이 많다.** 슬래시 명령 수: CLI 약 60개 > 앱 24개 > IDE 22개. 책에서 "CLI를 주력으로 쓰라"는 실무 권고의 1차 근거가 된다.

### Claude Code 대응 관점 메모

- `chatgpt.*` 명령 ID 네임스페이스 — 확장이 여전히 `chatgpt` 접두사를 쓴다. Codex ↔ ChatGPT 브랜드 통합의 흔적.
- IDE 확장의 슬래시 명령 집합은 Claude Code의 VS Code 확장보다 **클라우드 실행 전환(`/cloud`, `/local`, `/worktree`)에 무게**가 있다. 로컬/클라우드 전환은 Codex의 차별점.

### 관련 섹션

- IDE 확장 장
- **표면별 기능 비교 표** (CLI/IDE/앱 — 위 대조표가 그대로 재료)

---

## 자료 13: Codex IDE extension slash commands

- URL: https://learn.chatgpt.com/codex/ide/slash-commands (캐노니컬: `/docs/developer-commands?surface=ide`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)
- **자료 12와 동일 문서다.** 두 `.md`가 4,875바이트로 바이트 단위 일치. 내용은 자료 12에 전량 수록했다.
- 색인상 설명: "Codex IDE extension slash commands: Reference for slash commands in the Codex IDE extension"
- 관련 섹션: 자료 12와 동일. **별도 문서로 취급하지 말 것.**

---

## 자료 14: Codex IDE extension — Developer settings

- URL: https://learn.chatgpt.com/codex/ide/settings (캐노니컬: `/docs/developer-settings?surface=ide`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)

### 핵심 주장: 설정이 두 층으로 갈린다

> - "**Codex settings** control agent behavior shared with Codex CLI, including the model, reasoning effort, permissions, sandbox, MCP servers, and personalization. **Codex reads these settings from `config.toml`.**"
> - "**Editor settings** control how the extension behaves inside VS Code and compatible editors. These settings use **`chatgpt.*` keys** in the editor's settings system."

이 이분법이 IDE 장의 뼈대다. 명시적 경계 선언도 있다:

> "The `chatgpt.*` keys above **belong to the IDE extension and don't go in `config.toml`.**"

### 에디터 설정 키 전량 (원문 표 그대로)

| Setting | Default | Description |
|---|---|---|
| `chatgpt.commentCodeLensEnabled` | `true` | Show CodeLens above `TODO` comments so Codex can address them. |
| `chatgpt.openOnStartup` | `false` | Focus the Codex sidebar when the extension finishes starting. |
| `chatgpt.followUpQueueMode` | `queue` | Choose whether messages sent during a run wait for the next run (`queue`) or steer the current run (`steer`). The extension treats the legacy `interrupt` value as `steer`. Press <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd> to invert the behavior for one message. |
| `chatgpt.composerEnterBehavior` | `enter` | Choose whether <kbd>Enter</kbd> always sends (`enter`), <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>Enter</kbd> sends multiline prompts (`cmdIfMultiline`), or the modifier is always required (`cmdAlways`). |
| `chatgpt.reviewDelivery` | `inline` | Run `/review` in the current chat when possible (`inline`) or start a separate review chat (`detached`). |
| `chatgpt.localeOverride` | Auto | Set the preferred language for the Codex UI. Leave empty to detect it automatically. |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | `false` | Windows only: Run Codex in WSL when WSL is available. Use this when your repositories and tooling live in WSL2 or when you need Linux-native tooling. **Changing this setting reloads VS Code.** |
| `chatgpt.cliExecutable` | Unset | **Development only:** Set the path to the Codex CLI executable. You don't need this setting unless you're developing the Codex CLI; **manually overriding the bundled executable can prevent parts of the extension from working.** |
| `chat.fontSize` | Editor default | Control chat text in the Codex sidebar, including chat content and the composer. |
| `chat.editor.fontSize` | Editor default | Control code-rendered content in Codex chats, including code snippets and diffs. |

### 설정 접근 경로 (원문)

- Codex 설정: Codex 사이드바 기어 아이콘 → **Codex Settings**. 또는 **Open config.toml**로 활성 설정 레이어를 직접 편집.
- 에디터 설정: 에디터 설정에서 `@ext:openai.chatgpt`, `Codex`, 또는 설정 이름 검색.
- 확장 ID: **`openai.chatgpt`**
- "The extension also honors VS Code's built-in chat font settings for Codex chat surfaces." (`chat.fontSize`, `chat.editor.fontSize`가 `chatgpt.*`가 아닌 이유)

### ★ 주목할 점

- `chatgpt.localeOverride` — **UI 언어 설정이 존재한다.** 한국어 독자 대상 책이라면 언급 가치가 있다 (한국어 지원 여부 자체는 이 문서로 확인 불가 — 별도 확인 필요).
- `chatgpt.cliExecutable`에 대한 경고가 이례적으로 강하다. "번들된 CLI를 바꾸지 말라"는 것 — CLI와 확장의 버전 결합이 강하다는 뜻.
- `chatgpt.runCodexInWindowsSubsystemForLinux`는 자료 11(Windows 앱)의 WSL 전환과 **같은 결정을 IDE 쪽에서 하는 스위치**다. 교차 참조 필요.

### Claude Code 대응 관점 메모

- "에이전트 설정(`config.toml`, CLI와 공유) vs 에디터 설정(`chatgpt.*`)" 이분법은 Claude Code의 "`.claude/settings.json` vs VS Code 확장 설정" 구도와 대응한다. 다만 Codex는 **CLI와 IDE가 같은 `config.toml`을 읽는다**는 점을 훨씬 전면에 내세운다.
- `followUpQueueMode`의 `queue`/`steer` 구분 — 실행 중 메시지가 현재 턴을 조종할지 다음 턴을 기다릴지. Claude Code에서 실행 중 입력의 동작과 비교해 설명하면 좋은 지점.

### 관련 섹션

- IDE 확장 장 (설정 표 그대로)
- 설정 통합 장 (3표면 설정 계층 정리)

---

## 자료 15: Sites

- URL: https://learn.chatgpt.com/codex/sites (캐노니컬: `/docs/sites`)
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)

### 핵심 내용

> "Sites lets ChatGPT create, host, refine, and share websites, web apps, and games."

**공개 베타 상태다** — 원문 경고:

> "**Sites is in public beta.** Availability can depend on your plan, region, and workspace settings. **Plan-specific usage limits apply across all Sites during the beta.** ChatGPT shows the current limits and notifies you as you approach one. Reaching a limit can prevent you from creating a Site, adding storage, or keeping a high-usage Site public, but you can still edit and manage existing Sites."

> ⚠️ 자료 3(usage-limits)과 마찬가지로 **구체적 수치는 문서에 없다.** "ChatGPT shows the current limits"라며 런타임 UI로 위임한다. 사용량 한도에 관한 이 문서군의 일관된 패턴이다 — 책에서 지적할 만한 관찰.

### ★ 가장 중요한 경고 (원문)

> "**Every Sites deployment URL is a production deployment.** If you want to review a build before it becomes live, ask ChatGPT to save a version without deploying it."

### 표면별 지원 차이 (원문 근거)

| 표면 | Sites 지원 |
|---|---|
| ChatGPT 데스크톱 앱 | ✓ 관리 뷰 있음 |
| ChatGPT 웹 | ✓ **More > Sites** 또는 `chatgpt.com/sites` |
| **Codex CLI** | ✗ "Sites doesn't have a standalone Codex CLI management view." 로컬 프로젝트 편집·테스트만 가능 |
| **IDE 확장** | ✗ "Sites doesn't have a standalone IDE extension management view." 로컬 소스 편집·테스트만 |

### 설정 파일·스토리지 (원문 그대로)

링크 정보는 `.openai/hosting.json`에 저장된다. 프로비저닝된 예시:

```json
{
  "project_id": "<project-id>",
  "d1": "DB",
  "r2": null
}
```

> "A newly created local starter can begin without a `project_id`; Sites adds one after it provisions the hosted project."

**스토리지 선택 표** (원문 그대로):

| Site need | What to ask Sites for |
|---|---|
| Content-led website or landing page | A Site with no persistent application state unless the experience requires it |
| Saved records, user progress, or game scores | **D1**, a relational database for durable structured data |
| Images, documents, audio, video, or other uploads | **R2**, object storage for files |
| Uploaded files with searchable metadata | D1 for metadata and R2 for file contents |
| Internal site that needs the current workspace user's identity | Workspace-authenticated user identity |
| Public sign-in or an external identity provider | An authentication-enabled Site |

> 🔎 **관찰:** `D1`·`R2`는 Cloudflare의 제품명이다. 문서는 Cloudflare를 언급하지 않지만 명명이 일치한다. 책에서 "Cloudflare 기반으로 보인다"고 **단정하지 말 것** — 문서에 근거가 없다. 판정: **추측 금지 영역.**

### Sign in with ChatGPT (원문 그대로)

```html
<a href="/signin-with-chatgpt">Sign in with ChatGPT</a>
<a href="/signout-with-chatgpt">Sign out</a>
```

서버로 전달되는 요청 헤더:

- `oai-authenticated-user-email` — 인증된 이메일 주소
- `oai-authenticated-user-full-name` — 비어 있지 않은 프로필 이름일 수 있음. **"Treat it as optional and fall back to the email address."**

> "Keep authorization decisions in server-side code, and don't depend on name-split headers."

### 배포 2단계 (원문)

> 1. **Save a version.** ChatGPT builds a deployable version. For a local source project, ChatGPT associates the version with the Git commit used for the build.
> 2. **Deploy a version.** ChatGPT publishes a saved version and reports the production URL when deployment succeeds.

### 공유 옵션 (원문 목록)

> - **Owner and workspace admins**
> - **Selected active users or groups**, where supported
> - **Anyone in the workspace**, where supported
> - **Anyone on the internet**, only when public publishing is enabled

- 새 Site의 기본값: 소유자 + 워크스페이스 관리자만.
- "In Enterprise workspaces, **public publishing is off by default** and must be enabled by an admin."
- "Sharing lets people visit the Site; **it doesn't let them edit it.**"

### 프롬프트 예시 (원문 코드 블록 그대로)

```text
Build a project request dashboard for my operations team. Let team members
submit requests, see who owns each one, update the status, and filter the list.
Require people to sign in with their workspace account, and keep the request
data saved between visits.
```

```text
Deploy this project with Sites. Check whether it is compatible, make any
required changes, and give me the deployment URL.
```

```text
Add player scores and avatar uploads to this game. Keep the scores and uploaded
avatars between visits.
```

```text
Change this Site's access to everyone in my workspace after showing me the
current Site and confirming its URL.
```

Sites 워크플로 명시적 시작법: 프롬프트에 "website"라는 단어를 넣거나 **`@Sites`** 멘션.

### 제약·주의사항 (원문)

- **애널리틱스:** "Analytics is currently available for Sites that **aren't owned by an Enterprise workspace.**" 지표는 unique visitors + page views (SDK 불필요).
- **커스텀 도메인:** "Sites doesn't register domains for you." / "**Custom domains aren't available in Enterprise workspaces at launch.**"
- **데이터 레지던시 미지원:** "Sites doesn't support **data residency or inference residency at launch.** This includes deployed Sites, Site code, D1 and R2 data and file storage, generated artifacts, and logs." → 한국 기업 도입 검토 시 결정적 제약. 책에서 반드시 짚을 것.
- **삭제 불가역:** "Deleting a Site permanently removes it. **You can't restore a deleted Site.**" 삭제 시 Site slug 입력 요구.
- **비밀값:** "Don't store these values in `.openai/hosting.json`." 환경변수·시크릿은 Site 설정에서 관리. 환경값 변경 후에는 재배포 요청 필요.
- **금지 용도 (원문 그대로):** "Don't use Sites to process **Protected Health Information or payment-card data**; target children under 13 or the applicable age of digital consent; enable financial transactions; distribute malware; enable phishing; impersonate people or organizations; or otherwise violate OpenAI policies."
- 미지원: "Some frameworks, private networks, databases, background services, and hosting patterns aren't supported." (구체 목록 없음)

### 참조 링크

- Sites showcase: `https://developers.openai.com/showcase`
- 헬프센터 정책: `https://help.openai.com/en/articles/20001339` (Creating and managing ChatGPT Sites), `https://help.openai.com/en/articles/20001340` (privacy)

### 관련 섹션

- Sites 장 (베타 경고 + 제약 목록을 앞세울 것)
- 엔터프라이즈 도입 장 (데이터 레지던시 미지원, 애널리틱스 제외, 커스텀 도메인 제외 — 3중 제약)

---

## 보너스 자료 (색인에 없어 추가 수집): Slash commands (ChatGPT 데스크톱 앱)

- URL: https://learn.chatgpt.com/docs/reference/slash-commands
- 검색: 2026-08-02 기준
- 신뢰성: **최상** (공식 1차)
- **발견 경위:** 자료 9(`/codex/app/commands`)가 이 페이지를 링크하는데, `llms.txt` 색인에는 **없다.** 배정 148개 어디에도 포함될 수 없는 페이지다. 앱 표면의 슬래시 명령을 다루는 유일한 문서이므로 수집했다.

### 앱 슬래시 명령 전량 (원문 표 그대로)

| Slash command | Description |
|---|---|
| `/approve` | Approve one retry of a recent automatic-review denial, when automatic review is active. |
| `/cloud` | Run the chat in the cloud, when cloud execution is available. |
| `/cloud-environment` | Choose the cloud environment for the chat. |
| `/compact` | Compact the current chat's context. |
| `/fast` | Turn a catalog-provided Fast service tier on or off, when available. |
| `/feedback` | Open the feedback dialog to submit feedback and optionally include logs. |
| `/fork` | Copy a local chat into a new local chat **or worktree**. |
| `/goal` | Set a persistent goal for ChatGPT to work toward; **use `/plan` first to shape it**. |
| `/ide-context` | Turn **shared** IDE context on or off. |
| `/init` | Generate an `AGENTS.md` scaffold for the current project. |
| `/local` | Run the chat in the **selected local project**. |
| `/mcp` | Open MCP status to view connected servers. |
| `/memories` | Configure whether the chat can use or generate memories, when Memories is available. |
| `/model` | Choose the model for the current chat. |
| `/pet` | Wake or tuck away the desktop pet. |
| `/personality` | Choose how Codex responds, when the current model supports personalities. |
| `/plan` | Toggle plan mode for multi-step planning. |
| `/project` | Choose a project for new chats. |
| `/reasoning` | Choose the reasoning effort for the current chat. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/side` | Start a temporary side chat without interrupting the main chat. |
| `/status` | Show the chat ID, context usage, and rate limits. |
| `/task` | Start a chat without a project. |
| `/worktree` | Run the chat in a new Git worktree. |

### 추가 관용 (원문)

> "You can also explicitly invoke skills by typing `$` in the chat composer."

> "Enabled skills also appear in the slash command list. **Custom prompts appear as `/prompts:<name>` commands.**"

→ 자료 4(custom prompts)의 `/prompts:` 네임스페이스가 앱 표면에서도 동일하게 작동함을 교차 확인 ✅.

### `/goal` 상세 (원문)

> "Use `/goal` in the app composer to start Goal mode. A goal is a persistent objective that ChatGPT works toward until it finishes the task, pauses, or needs more input. **To define the goal with ChatGPT first, start with `/plan`, then set the refined goal with `/goal`.**"

> "When a goal is active, the app shows its progress above the composer. Use the buttons in that progress row to pause or resume the goal, edit the goal text, or clear the goal instead of typing another slash command. You can keep steering ChatGPT with follow-up messages while the goal runs."

### 관련 섹션

- 데스크톱 앱 장
- 표면별 슬래시 명령 비교표 (자료 12의 대조표에 이 데이터가 들어감)

---

## 수집 한계 및 fact-checker 인계 사항

1. **`.md` 자리표시자 문제 (최중요).** `/codex/cli/reference`처럼 `<ConfigTable>` 컴포넌트를 쓰는 페이지는 `.md`만 받으면 표가 통째로 사라진다. 다른 수집자가 담당한 `/codex/config-file/config-reference`, `/codex/security/cli/reference` 등도 **같은 문제일 가능성이 높다.** 해당 담당자에게 HTML astro-island 추출을 권고할 것. (추출 스크립트: `scratchpad/decode.py`, `scratchpad/merge.py`)
2. **모델명이 문서 간 불일치한다.** `gpt-5.6-terra` / `gpt-5.6-luna`(CLI 레퍼런스) vs `5.6 Sol Extra High`(오버뷰 목업) vs `GPT-5.4`(codex-for-oss). `/codex/models`를 단일 출처로 삼아야 한다.
3. **사용량 한도 수치는 공식 문서에 없다.** usage-limits와 Sites 모두 "런타임 UI 또는 헬프센터 참조"로 위임한다. 커뮤니티발 수치 주장은 1차 확인이 불가능하다.
4. **발행일 메타가 전 페이지에 없다.** 어느 문서에도 published/updated 날짜가 표기되지 않는다. 신선도 판정은 "검색 시점 2026-08-02"와 내용상 버전 단서(`0.114`/`0.115`, `Python.Python.3.14` 등)에만 의존해야 한다.
5. **`/codex/custom-prompts`는 deprecated 기능이다.** 이 페이지를 근거로 "이렇게 커스텀 명령을 만드세요"라고 쓰면 안 된다.
6. **자료 6(overview)과 자료 7(ai-native)은 마케팅 문서다.** 기술적 사실의 근거로 쓰지 말고, 포지셔닝·조직론의 근거로만 쓸 것.

---

## 접근 실패 URL

**배정 15개 중 접근 실패: 0건.** 전량 수집 성공.

다만 `.md` 형식으로는 실패해 우회한 건이 있어 기록한다:

| URL | `.md` 결과 | 우회 방법 | 최종 |
|---|---|---|---|
| `https://developers.openai.com/codex/overview.md` | 404 (SPA HTML 반환) | `https://learn.chatgpt.com/docs` HTML → pandoc | ✅ 수집 |
| `https://developers.openai.com/codex/learn/best-practices.md` | 404 | `https://learn.chatgpt.com/guides/best-practices` HTML → pandoc | ✅ 수집 |
| `https://developers.openai.com/codex/guides/build-ai-native-engineering-team.md` | 404 | `https://learn.chatgpt.com/guides/build-ai-native-engineering-team` HTML → pandoc | ✅ 수집 |
| `https://developers.openai.com/codex/community/codex-for-oss.md` | 404 | `https://developers.openai.com/community/codex-for-oss` HTML → pandoc | ✅ 수집 |
| `https://learn.chatgpt.com/codex/cli/reference.md` | 200이나 **플래그 표 29개 누락** | HTML astro-island props(JSON) 디코드 | ✅ 표 전량 복원 |

**진짜 접근 실패 (본 그룹 범위 밖, 참고용):**

| URL | 결과 | 비고 |
|---|---|---|
| `https://developers.openai.com/codex/use-cases` | **404** | 자료 6(overview)이 링크하는 페이지인데 죽어 있다. 공식 문서 내 깨진 링크 |
| `https://developers.openai.com/codex/llms-full.txt` | **404** | 색인에는 등재돼 있으나 실제로는 없다 |
| `https://learn.chatgpt.com/llms.txt` | **404** | 모든 `.md` 문서 헤더가 이 URL을 "완전한 색인"으로 안내하는데 **죽어 있다.** 살아 있는 색인은 `https://developers.openai.com/llms.txt` 뿐이다 |

---

## 미수집 잔여 URL

### 방법

`curl -sSL https://developers.openai.com/llms.txt`(2026-08-02, 107,052바이트)에서 `/codex/` 경로를 전부 추출 → **140개**. 여기서 메타 파일 2개(`/codex/llms.txt`, `/codex/llms-full.txt`)를 빼면 **실제 문서 페이지 138개**.

추가로, 수집한 15개 페이지 본문에 등장하는 모든 `/codex/`·`/docs/` 링크를 추출해 색인과 역대조했다.

### ① 색인 총량과 배정 총량의 불일치 (확인 요망)

| 항목 | 수 |
|---|---|
| 2026-08-02 색인의 `/codex/` 경로 | 140 |
| 그중 메타 파일 (`llms.txt`, `llms-full.txt`) | 2 |
| **실제 문서 페이지** | **138** |
| 이번 그룹 F 배정 | 15 |
| 색인상 나머지 (동료 5명 담당분이어야 함) | **123** |
| 그런데 동료 배정 규모는 | **133** |

→ **약 10개의 차이**가 난다. 동료 배정 목록에 (a) 이미 사라진 페이지, (b) 리다이렉트로 통합된 중복 별칭, (c) `/codex/` 밖 경로가 섞여 있을 가능성이 높다. **동료 배정 목록 133개를 받아 색인 138개와 직접 대조해야 확정된다** — 나는 그 목록을 갖고 있지 않아 이 이상 좁힐 수 없다.

특히 이번 그룹만으로도 **별칭 중복이 4건**(cli/reference≡cli/slash-commands, ide/commands≡ide/slash-commands) 나왔다. 133개에도 같은 유형의 중복이 있을 것으로 강하게 의심된다.

### ② 색인에 없어 아무에게도 배정되지 않은 페이지 (진짜 누락)

수집 페이지 본문 링크를 역추적해 발견. **색인 138개 어디에도 없다.**

| 경로 | 상태 | 성격 | 조치 |
|---|---|---|---|
| `/codex/reference/slash-commands` | ✅ 200 (4,677 B) | **고유 문서** — ChatGPT 데스크톱 앱 슬래시 명령. 앱 표면 슬래시 명령을 다루는 유일한 페이지 | **본 그룹에서 수집 완료** (위 "보너스 자료") |
| `/codex/codex-for-oss-terms` | ✅ 200 | 고유 문서 — Codex for OSS 프로그램 약관 | **미수집.** 법무 성격이라 책 본문 가치는 낮음. 필요 시 추가 수집 권장 |
| `/codex/developer-commands` | ✅ 200 (54,013 B) | **캐노니컬 상위 문서** — cli/ide/app/web 4개 표면을 `ContentModeSwitch`로 묶은 상위 페이지. CLI 부분은 자료 1과 동일하고 표면 안내 래퍼가 추가됨 | **실질 수집 완료** (자료 1 + 자료 12가 이 문서의 두 표면) |
| `/codex/reference/commands` | ✅ 200 | `/codex/app/commands`의 캐노니컬 (별칭) | **수집 완료** (자료 9) |
| `/codex/reference/settings` | ✅ 200 (5,038 B) | `/codex/app/settings`의 캐노니컬 (별칭) | **수집 완료** (자료 10) |
| `/codex/use-cases` | ❌ 404 | overview가 링크하나 죽음 | 수집 불가 |

**요약: 이 그룹의 재대조로 새로 발견한 미배정 고유 문서는 2개** — `/codex/reference/slash-commands`(수집 완료)와 `/codex/codex-for-oss-terms`(미수집, 우선순위 낮음).

### ③ 색인 138개 중 그룹 F 배정 15개를 제외한 123개 (동료 담당분 — 확인용 전량 목록)

아래가 2026-08-02 색인에 있으면서 그룹 F 배정이 **아닌** 경로다. 동료 5명의 133개와 이 123개를 대조하면 ①의 불일치가 즉시 드러난다.

```
/codex/administration
/codex/agent-approvals-security
/codex/agent-configuration/agents-md
/codex/agent-configuration/rules
/codex/agent-configuration/speed
/codex/agent-configuration/subagents
/codex/amazon-bedrock
/codex/app
/codex/app-server
/codex/appshots
/codex/artifacts-viewer
/codex/auth
/codex/automations
/codex/browser
/codex/build-plugins
/codex/build-skills
/codex/chrome-extension
/codex/cli
/codex/cli-customization
/codex/cloud
/codex/cloud/internet-access
/codex/code-review
/codex/codex-sdk
/codex/computer-use
/codex/config-file/config-advanced
/codex/config-file/config-basic
/codex/config-file/config-reference
/codex/config-file/config-sample
/codex/config-file/environment-variables
/codex/configuration
/codex/customization/chronicle
/codex/customization/memories
/codex/customization/overview
/codex/cyber-safety
/codex/developers
/codex/enterprise/access-tokens
/codex/enterprise/admin-setup
/codex/enterprise/analytics-api
/codex/enterprise/apps-and-connectors
/codex/enterprise/compliance-api
/codex/enterprise/governance
/codex/enterprise/groups-and-provisioning
/codex/enterprise/managed-configuration
/codex/enterprise/roles-and-workspace-permissions
/codex/enterprise/skills
/codex/enterprise/windows-deployment
/codex/enterprise/work-admin-faq
/codex/enterprise/workspace-analytics
/codex/enterprise/workspace-model-availability
/codex/environments/cloud-environment
/codex/environments/git-worktrees
/codex/environments/local-environment
/codex/environments/modes
/codex/extend/mcp
/codex/extend/record-and-replay
/codex/feature-maturity
/codex/features
/codex/features/codex-micro
/codex/features/voice
/codex/get-started-with-work
/codex/github-action
/codex/glossary
/codex/hooks
/codex/ide
/codex/image-generation
/codex/image-inputs
/codex/import
/codex/integrated-terminal
/codex/long-running-work
/codex/mcp-server
/codex/models
/codex/non-interactive-mode
/codex/notifications
/codex/open-source
/codex/permission-modes
/codex/permissions
/codex/personalize
/codex/pets
/codex/plugins
/codex/pricing
/codex/projects
/codex/prompting
/codex/quickstart
/codex/reference/troubleshooting
/codex/remote-connections
/codex/resources
/codex/sandboxing
/codex/sandboxing/auto-review
/codex/security
/codex/security-administration
/codex/security/cli
/codex/security/cli/bulk-scans
/codex/security/cli/ci
/codex/security/cli/faq
/codex/security/cli/reference
/codex/security/faq
/codex/security/plugin
/codex/security/plugin/changelog
/codex/security/plugin/code-changes
/codex/security/plugin/deep-scans
/codex/security/plugin/export-findings
/codex/security/plugin/fix-findings
/codex/security/plugin/scans
/codex/security/plugin/security-hardening
/codex/security/plugin/triage-backlog
/codex/security/plugin/vulnerability-reports
/codex/security/plugin/workbench
/codex/security/sdk
/codex/security/setup
/codex/security/threat-model
/codex/skills-and-plugins
/codex/third-party/github
/codex/third-party/linear
/codex/third-party/slack
/codex/use-chatgpt
/codex/videos
/codex/visualizations
/codex/web
/codex/web-search
/codex/whats-new
/codex/windows/windows-sandbox
/codex/windows/wsl
```

### ④ 다른 수집자에게 즉시 전달할 권고

1. **`/codex/config-file/config-reference`, `/codex/security/cli/reference`, `/codex/permissions`, `/codex/hooks` 담당자는 `.md` 결과에 `<ConfigTable`이 있는지 즉시 확인하라.** 있으면 설정 키 표가 통째로 빠진 것이다.
2. **`/codex/whats-new`는 이 책의 신선도 앵커다.** 릴리스 날짜·버전이 유일하게 명시될 가능성이 높은 페이지 — fact-checker의 1차 대조 원장으로 지정할 것을 권한다.
3. **`/codex/models`를 모델명의 단일 출처로 확정하라.** 현재 문서 3곳이 서로 다른 모델명을 쓴다.
4. **`/codex/pricing`이 개인 요금제 한도의 유일한 후보다.** usage-limits는 엔터프라이즈 전용이고 수치가 없다.
