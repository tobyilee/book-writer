# Config basics

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Codex reads configuration details from more than one location. Your personal defaults live in `~/.codex/config.toml`, and you can add project overrides with `.codex/config.toml` files. For security, Codex loads project `.codex/` layers only when you trust the project.

## Codex configuration file

Codex stores user-level configuration at `~/.codex/config.toml`. To scope settings to a specific project or subfolder, add a `.codex/config.toml` file in your repo.

To open the configuration file from the Codex IDE extension, select the gear icon in the top-right corner, then select **Codex Settings > Open config.toml**.

The CLI and IDE extension share the same configuration layers. You can use them to:

- Set the default model and provider.
- Configure [approval policies and sandbox settings](https://learn.chatgpt.com/docs/agent-approvals-security#sandbox-and-approvals).
- Configure [MCP servers](https://learn.chatgpt.com/docs/extend/mcp).

## Configuration precedence

Codex resolves values in this order (highest precedence first):

1. CLI flags and `--config` overrides
2. Project config files: `.codex/config.toml`, ordered from the project root down to your current working directory (closest wins; trusted projects only)
3. [Profile](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles) files selected with `--profile profile-name` (`~/.codex/profile-name.config.toml`)
4. User config: `~/.codex/config.toml`
5. System config (if present): `/etc/codex/config.toml` on Unix
6. Built-in defaults

Use that precedence to set shared defaults in `config.toml` and keep [profile files](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles) focused on the values that differ.

If you mark a project as untrusted, Codex skips project-scoped `.codex/` layers, including project-local config, hooks, and rules. User and system config still load, including user/global hooks and rules.

For one-off overrides via `-c`/`--config` (including TOML quoting rules), see [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced#one-off-overrides-from-the-cli).

On managed machines, your organization may also enforce constraints via
  `requirements.toml` (for example, disallowing `approval_policy = "never"` or
  `sandbox_mode = "danger-full-access"`). See [Managed
  configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) and [Admin-enforced
  requirements](https://learn.chatgpt.com/docs/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml).

## Common configuration options

Here are a few options people change most often:

#### Default model

Choose the model Codex uses by default in the CLI and IDE.

```toml
model = "gpt-5.6"
```


#### Approval prompts

Control when Codex pauses to ask before running generated commands.

```toml
approval_policy = "on-request"
```

For behavior differences between `untrusted`, `on-request`, and `never`, see [Run without approval prompts](https://learn.chatgpt.com/docs/agent-approvals-security#run-without-approval-prompts) and [Common sandbox and approval combinations](https://learn.chatgpt.com/docs/agent-approvals-security#common-sandbox-and-approval-combinations).

#### Sandbox level

Adjust how much filesystem and network access Codex has while executing commands.

```toml
sandbox_mode = "workspace-write"
```

For mode-by-mode behavior (including protected `.git`/`.codex` paths and network defaults), see [Sandbox and approvals](https://learn.chatgpt.com/docs/agent-approvals-security#sandbox-and-approvals), [Protected paths in writable roots](https://learn.chatgpt.com/docs/agent-approvals-security#protected-paths-in-writable-roots), and [Network access](https://learn.chatgpt.com/docs/agent-approvals-security#network-access).

#### Permission profiles

Codex also supports named permission profiles for reusable filesystem and
network policies. Built-in profiles are `:read-only`, `:workspace`, and
`:danger-full-access`. Custom profiles use `[permissions.<name>]` tables and a
matching `default_permissions` value. See [Permissions](https://learn.chatgpt.com/docs/permissions).

#### Windows sandbox mode

When running Codex natively on Windows, set the native sandbox mode to `elevated` in the `windows` table. Use `unelevated` only if you don't have administrator permissions or if elevated setup fails.

```toml
[windows]
sandbox = "elevated"   # Recommended
# sandbox = "unelevated" # Fallback if admin permissions/setup are unavailable
```

#### Web search mode

Codex enables web search by default for local chats and serves results from a web search cache. The cache is an OpenAI-maintained index of web results, so cached mode returns pre-indexed results instead of fetching live pages. This reduces exposure to prompt injection from arbitrary live content, but you should still treat web results as untrusted. If you are using `--yolo` or another [full access sandbox setting](https://learn.chatgpt.com/docs/agent-approvals-security#common-sandbox-and-approval-combinations), web search defaults to live results. Choose a mode with `web_search`:

- `"cached"` (default) serves results from the web search cache.
- `"indexed"` permits external web access only when the search index gates the request.
- `"live"` fetches the most recent data from the web (same as `--search`).
- `"disabled"` turns off the web search tool.

```toml
web_search = "cached"  # default; serves results from the web search cache
# web_search = "indexed" # gate external web access through the search index
# web_search = "live"  # fetch the most recent data from the web (same as --search)
# web_search = "disabled"
```

#### Reasoning effort

Tune how much reasoning effort the model applies when supported.

```toml
model_reasoning_effort = "high"
```

#### Communication style

Set a default communication style for supported models.

```toml
personality = "friendly" # or "pragmatic" or "none"
```

You can override this later in an active session with `/personality` or per thread/turn when using the app-server APIs.

#### TUI keymap

Customize terminal shortcuts under `tui.keymap`. Selected composer actions fall back to matching `tui.keymap.global` bindings; context-specific bindings take precedence when supported. An empty list unbinds the action.

```toml
[tui.keymap.global]
open_transcript = "ctrl-t"

[tui.keymap.composer]
submit = ["enter", "ctrl-m"]

[tui.keymap.chat]
interrupt_turn = "f12"
```

#### Command environment

Control which environment variables Codex forwards to spawned commands.

```toml
[shell_environment_policy]
include_only = ["PATH", "HOME"]
```

#### Log directory

Override where Codex writes local log files. Setting `log_dir` explicitly also
enables the opt-in plaintext TUI log, `codex-tui.log`, in that directory.

```toml
log_dir = "/absolute/path/to/codex-logs"
```

For one-off runs, you can also set it from the CLI:

```bash
codex -c log_dir=./.codex-log
```

## Feature flags

Use the `[features]` table in `config.toml` to toggle optional and experimental capabilities.

### Common feature flags

| Key                  |        Default        | Maturity     | Description                                                                              |
| -------------------- | :-------------------: | ------------ | ---------------------------------------------------------------------------------------- |
| `apps`               |         true          | Stable       | Enable app (connector) integrations                                                      |
| `goals`              |         true          | Stable       | Enable persisted goals and automatic continuation                                        |
| `hooks`              |         true          | Stable       | Enable lifecycle hooks from `hooks.json` or inline `[hooks]`. See [Hooks](https://learn.chatgpt.com/docs/hooks). |
| `fast_mode`          |         true          | Stable       | Enable Fast mode selection and the `service_tier = "fast"` path                          |
| `memories`           |         false         | Experimental | Enable [Memories](https://learn.chatgpt.com/docs/customization/memories)                                         |
| `multi_agent`        |         true          | Stable       | Enable subagent collaboration tools                                                      |
| `personality`        |         true          | Stable       | Enable personality selection controls                                                    |
| `remote_plugin`      |         true          | Stable       | Enable the remote plugin catalog                                                         |
| `shell_snapshot`     |         true          | Stable       | Snapshot your shell environment to speed up repeated commands                            |
| `shell_tool`         |         true          | Stable       | Enable the default `shell` tool                                                          |
| `unified_exec`       | `true` except Windows | Stable       | Use the unified PTY-backed exec tool                                                     |
| `web_search`         |         true          | Deprecated   | Legacy toggle; prefer the top-level `web_search` setting                                 |
| `web_search_cached`  |         false         | Deprecated   | Legacy toggle that maps to `web_search = "cached"` when unset                            |
| `web_search_request` |         false         | Deprecated   | Legacy toggle that maps to `web_search = "live"` when unset                              |

This table lists common user-facing flags, not every internal or
  under-development feature. The Maturity column uses labels such as
  Experimental, Beta, and Stable. See [Feature
  Maturity](https://learn.chatgpt.com/docs/feature-maturity) for how to interpret these labels.

Omit feature keys to keep their defaults.

For lifecycle hook configuration, see [Hooks](https://learn.chatgpt.com/docs/hooks).

### Enabling features

- In `config.toml`, add `feature_name = true` under `[features]`.
- From the CLI, run `codex --enable feature_name`.
- To enable more than one feature, run `codex --enable feature_a --enable feature_b`.
- To disable a feature, set the key to `false` in `config.toml`.