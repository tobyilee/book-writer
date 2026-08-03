# Developer commands

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<ContentModeSwitch group="codex-surface" id="web">

ChatGPT web has its own composer command menu. Type `/` to see the actions
available in the current chat. It doesn't expose the ChatGPT desktop app or CLI
command set; the Codex slash commands, CLI subcommands, and flags in this
reference don't apply to ChatGPT web.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

## ChatGPT desktop app commands

The general [Commands](https://learn.chatgpt.com/docs/reference/commands) page covers app navigation,
chat shortcuts, keyboard customization, and deep links for chats, settings,
skills, scheduled tasks, plugins, and pets.

The [Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands) page covers the commands
available from the app composer, including `/feedback`, `/goal`, `/init`,
`/mcp`, `/plan`, `/review`, and `/status`.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

## How to read this reference

This page catalogs every documented Codex CLI command and flag. Use the interactive tables to search by key or description. Each section indicates whether the option is stable or experimental and calls out risky combinations.

The CLI inherits most defaults from `~/.codex/config.toml`. Any
  `-c key=value` overrides you pass at the command line take
  precedence for that invocation. See [Config
  basics](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence) for more
  information.

## Global flags

<ConfigTable client:load options={globalFlagOptions} />

These options apply to the base `codex` command. Most propagate to commands;
see the notes above or the relevant command help for exceptions. For propagated
flags, follow the relevant command help. For example, `codex exec --oss ...`
applies `--oss` to `exec`.

## Command overview

The Maturity column uses feature maturity labels such as Experimental, Beta,
  and Stable. See [Feature Maturity](https://learn.chatgpt.com/docs/feature-maturity) for how to
  interpret these labels.

<ConfigTable
  client:load
  options={commandOverview}
  secondColumnTitle="Maturity"
  secondColumnVariant="maturity"
/>

## Command details

### `codex` (interactive)

Running `codex` with no subcommand launches the interactive terminal UI (TUI). The agent accepts the global flags above plus image attachments. Web search defaults to cached mode; use `--search` to switch to live browsing. For low-friction local work, use `--sandbox workspace-write --ask-for-approval on-request`.

Use `--remote ws://host:port` or `--remote wss://host:port` to connect the TUI to an app server started with `codex app-server --listen ws://IP:PORT`. For a local Unix socket, use `--remote unix://` for the default socket or `--remote unix://PATH` for an explicit path. Add `--remote-auth-token-env <ENV_VAR>` when the server requires a bearer token for WebSocket authentication.

### `codex app-server`

Launch the Codex app server locally. This is primarily for development and debugging and may change without notice.

<ConfigTable client:load options={appServerOptions} />

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

<ConfigTable client:load options={appOptions} />

`codex app` opens an installed ChatGPT desktop app, or starts the installer when
the app is missing. On macOS, Codex opens the provided workspace path; on
Windows, it prints the path to open after installation.

### `codex debug app-server send-message-v2`

Send one message through app-server's V2 thread/turn flow using the built-in app-server test client.

<ConfigTable client:load options={debugAppServerSendMessageV2Options} />

This debug flow initializes with `experimentalApi: true`, starts a thread, sends a turn, and streams server notifications. Use it to reproduce and inspect app-server protocol behavior locally.

### `codex debug models`

Print the raw model catalog Codex sees as JSON.

<ConfigTable client:load options={debugModelsOptions} />

Use `--bundled` when you want to inspect only the catalog bundled with the current binary, without refreshing from the remote models endpoint.

### `codex debug prompt-input`

Render the exact model-visible prompt input list as JSON. Use this when
debugging instruction discovery, session context, or prompt construction.

<ConfigTable client:load options={debugPromptInputOptions} />

### `codex apply`

Apply the most recent diff from a Codex cloud chat to your local repository. You must authenticate and have access to the chat.

<ConfigTable client:load options={applyOptions} />

Codex prints the patched files and exits non-zero if `git apply` fails (for example, due to conflicts).

### `codex review`

Run a code review non-interactively. Choose exactly one review target, or pass
custom review instructions as a prompt.

<ConfigTable client:load options={reviewOptions} />

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

<ConfigTable client:load options={archiveOptions} />

### `codex delete`

Permanently delete a saved interactive session by session ID or session name.
Use this only when you want to remove the transcript instead of hiding it from
active session lists.

```bash
codex delete <SESSION>
codex delete <SESSION_UUID> --force
```

<ConfigTable client:load options={deleteOptions} />

Use `--force` only with a session UUID. Named sessions still require
confirmation so Codex doesn't delete a repeated or ambiguous name without a prompt.

### `codex cloud`

Interact with Codex cloud chats from the terminal. The default command opens an interactive picker; `codex cloud exec` submits a task directly, and `codex cloud list` returns recent chats for scripting or quick inspection.

<ConfigTable client:load options={cloudExecOptions} />

Authentication follows the same credentials as the main CLI. Codex exits non-zero if the task submission fails.

#### `codex cloud list`

List recent cloud chats with optional filtering and pagination.

<ConfigTable client:load options={cloudListOptions} />

Plain-text output prints a task URL followed by status details. Use `--json` for automation. The JSON payload contains a `tasks` array plus an optional `cursor` value. Each task includes `id`, `url`, `title`, `status`, `updated_at`, `environment_id`, `environment_label`, `summary`, `is_review`, and `attempt_total`.

### `codex completion`

Generate shell completion scripts and redirect the output to the appropriate location, for example `codex completion zsh > "${fpath[1]}/_codex"`.

<ConfigTable client:load options={completionOptions} />

### `codex doctor`

Generate a local diagnostic report before filing a support issue or
while investigating a broken Codex installation. The report checks installation,
configuration, authentication, runtime, Git, terminal, app-server, and thread
inventory health.

<ConfigTable client:load options={doctorOptions} />

### `codex features`

Manage feature flags stored in `$CODEX_HOME/config.toml`. The `enable` and
`disable` commands persist changes so they apply to future sessions. The
`features` subcommand doesn't accept `--profile`.

<ConfigTable client:load options={featuresOptions} />

### `codex exec`

Use `codex exec` (or the short form `codex e`) for scripted or CI-style runs that should finish without human interaction.

<ConfigTable client:load options={execOptions} />

Codex writes formatted output by default. Add `--json` to receive newline-delimited JSON events (one per state change). The optional `resume` subcommand lets you continue non-interactive tasks. Use `--last` to pick the most recent session from the current working directory, or add `--all` to search across all sessions:

<ConfigTable client:load options={execResumeOptions} />

### `codex execpolicy`

Check `execpolicy` rule files before you save them. `codex execpolicy check` accepts one or more `--rules` flags (for example, files under `~/.codex/rules`) and emits JSON showing the strictest decision and any matching rules. Add `--pretty` to format the output. The `execpolicy` command is currently in preview.

<ConfigTable client:load options={execpolicyOptions} />

### `codex login`

Authenticate the CLI with a ChatGPT account, API key, or access token. With no flags, Codex opens a browser for the ChatGPT OAuth flow.

<ConfigTable client:load options={loginOptions} />

`codex login status` exits with `0` when credentials are present, which is helpful in automation scripts.

### `codex logout`

Remove saved credentials for both API key and ChatGPT authentication. This command has no flags.

### `codex mcp`

Manage Model Context Protocol server entries stored in `~/.codex/config.toml`.

<ConfigTable client:load options={mcpCommands} />

The `add` subcommand supports both stdio and streamable HTTP transports:

<ConfigTable client:load options={mcpAddOptions} />

OAuth actions (`login`, `logout`) only work with streamable HTTP servers (and only when the server supports OAuth).

### `codex plugin`

Install, list, and remove plugins from configured marketplaces.

<ConfigTable client:load options={pluginCommands} />

`codex plugin add --json` prints `pluginId`, `name`, `marketplaceName`,
`version`, `installedPath`, and `authPolicy`. `codex plugin list --json` prints
`installed` and `available` arrays. Entries include `pluginId`, `name`,
`marketplaceName`, `version`, `installed`, `enabled`, `source`, `installPolicy`,
`authPolicy`, and, when available, `marketplaceSource` with the configured
marketplace source type and value. `codex plugin remove --json` prints
`pluginId`, `name`, and `marketplaceName`.

### `codex plugin marketplace`

Manage plugin marketplace sources that Codex can browse and install from.

<ConfigTable client:load options={marketplaceCommands} />

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

<ConfigTable client:load options={resumeOptions} />

### `codex fork`

Fork a previous interactive session into a new chat. By default, `codex fork` opens the session picker; add `--last` to fork your most recent session instead.

When the current and saved session directories differ, `codex fork` uses the
same working-directory prompt and `tui.resume_cwd` setting as `codex resume`.

<ConfigTable client:load options={forkOptions} />

### `codex sandbox`

Use the sandbox helper to run a command under the same policies Codex uses internally.

#### macOS seatbelt

<ConfigTable client:load options={sandboxMacOptions} />

#### Linux Landlock

<ConfigTable client:load options={sandboxLinuxOptions} />

#### Windows

<ConfigTable client:load options={sandboxWindowsOptions} />

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

## Related resources

- [Codex CLI overview](https://learn.chatgpt.com/docs/codex/cli): installation, upgrades, and quick tips.
- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic): persist defaults like the model and provider.
- [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced): profiles, providers, sandbox tuning, and integrations.
- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md): conceptual overview of Codex agent capabilities and best practices.

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

Expected: Codex exits immediately. Save or commit any important work first.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

Use these commands to control Codex from the VS Code Command Palette. You can also bind them to keyboard shortcuts.

## Assign a key binding

To assign or change a key binding for a Codex command:

1. Open the Command Palette (**Cmd+Shift+P** on macOS or **Ctrl+Shift+P** on Windows/Linux).
2. Run **Preferences: Open Keyboard Shortcuts**.
3. Search for `Codex` or the command ID (for example, `chatgpt.newChat`).
4. Select the pencil icon, then enter the shortcut you want.

## Extension commands

| Command                   | Default key binding                        | Description                                             |
| ------------------------- | ------------------------------------------ | ------------------------------------------------------- |
| `chatgpt.addToThread`     | -                                          | Add selected text range as context for the current chat |
| `chatgpt.addFileToThread` | -                                          | Add the entire file as context for the current chat     |
| `chatgpt.newChat`         | macOS: `Cmd+N`<br />Windows/Linux: `Ctrl+N` | Create a new chat                                       |
| `chatgpt.newCodexPanel`   | -                                          | Create a new Codex panel                                |
| `chatgpt.openCommandMenu` | -                                          | Open the Codex command menu                             |
| `chatgpt.openSidebar`     | -                                          | Open the Codex sidebar panel                            |

Slash commands let you control Codex without leaving the composer. Use them to check status, switch between local and cloud mode, or send feedback.

## Use a slash command

1. In the Codex composer, type `/`.
2. Select a command from the list, or keep typing to filter (for example, `/status`).
3. Press **Enter**.

## Available slash commands

| Slash command        | Description                                                                             |
| -------------------- | --------------------------------------------------------------------------------------- |
| `/approve`           | Approve one retry of a recent automatic-review denial, when automatic review is active. |
| `/cloud`             | Run the chat in the cloud, when cloud execution is available.                           |
| `/cloud-environment` | Choose the cloud environment for the chat.                                              |
| `/compact`           | Compact the current chat's context.                                                     |
| `/fast`              | Turn a catalog-provided Fast service tier on or off, when available.                    |
| `/feedback`          | Open the feedback dialog to submit feedback and optionally include logs.                |
| `/fork`              | Copy a local chat into a new local chat.                                                |
| `/goal`              | Set a persistent goal for Codex to work toward.                                         |
| `/ide-context`       | Turn automatic IDE context on or off.                                                   |
| `/init`              | Generate an `AGENTS.md` scaffold for the current project.                               |
| `/local`             | Run the chat in your local workspace.                                                   |
| `/mcp`               | Open MCP status to view connected servers.                                              |
| `/memories`          | Configure whether the chat can use or generate memories, when Memories is available.    |
| `/model`             | Choose the model for the current chat.                                                  |
| `/personality`       | Choose how Codex responds, when the current model supports personalities.               |
| `/plan`              | Toggle plan mode for multi-step planning.                                               |
| `/project`           | Choose a project for new chats.                                                         |
| `/reasoning`         | Choose the reasoning effort for the current chat.                                       |
| `/review`            | Start code review mode to review uncommitted changes or compare against a base branch.  |
| `/side`              | Start a temporary side chat without interrupting the main chat.                         |
| `/status`            | Show the chat ID, context usage, and rate limits.                                       |
| `/worktree`          | Run the chat in a new Git worktree.                                                     |

</ContentModeSwitch>