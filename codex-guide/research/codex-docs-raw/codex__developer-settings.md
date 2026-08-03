# Developer settings

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<ContentModeSwitch group="codex-surface" id="web">

ChatGPT web stores product and workspace preferences in ChatGPT settings. ChatGPT Work
chats run in a managed environment and don't read local Codex
configuration files. Use the controls your workspace exposes in ChatGPT
settings; workspace administrators may manage some settings for you.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

The general [Settings](https://learn.chatgpt.com/docs/reference/settings) page covers app preferences,
including profile, keyboard shortcuts, notifications, appearance,
personalization, memories, and archived chats.

## Project and terminal behavior

Choose where files open, how much command output appears in chats, and where
terminal tabs open by default.

## Code review

Under **Settings > Git**, use **Review delivery** to choose **Inline** to run
`/review` in the current chat when possible or **Detached** to start a separate
review chat.

## IDE extension sync

When the ChatGPT desktop app and IDE extension are open in the same project,
they share active chats and editor context. Turn on **IDE context** from the app
composer to let Codex use files currently open in your editor. Turn it off when
you want the app prompt to exclude that editor context.

You can open an app chat from the IDE extension and continue an IDE chat in the
app. Both surfaces use the same project to determine which chats and context to
share.

## Agent configuration

Codex agents in the app inherit the same configuration as the IDE extension and
CLI. Use the in-app controls for common settings, or edit `config.toml` for
advanced options. See [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
and [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) for details.

## Git

Use Git settings to standardize branch naming and choose whether Codex uses
force pushes. You can also set prompts that Codex uses to generate commit
messages and pull request descriptions.

## Integrations and MCP

Connect external tools through Model Context Protocol (MCP). Enable recommended
servers or add your own. If a server requires OAuth, the app starts the
authentication flow. These settings also apply to the Codex CLI and IDE
extension because MCP configuration lives in `config.toml`. See
[Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp) for details.

## Browser developer mode

Under **Developer mode**, turn on **Enable full CDP access** to let ChatGPT use
the Chrome DevTools Protocol for performance profiling and deeper browser
debugging. If your organization has disabled full CDP access, you can't enable
it locally. See [Developer mode](https://learn.chatgpt.com/docs/browser?surface=app#app-developer-mode) for setup,
risk, approval, and administrator requirements.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

Codex CLI reads your personal defaults from `~/.codex/config.toml`. Add a
`.codex/config.toml` file to a trusted project or subfolder when you need
project-specific overrides. The CLI and IDE extension share these configuration
layers.

## Inspect your settings

Use these commands to understand the effective settings for the current
session:

- Run `/status` to see the active model, approval policy, writable roots, and
  token usage.
- Run `/debug-config` to see the configuration layers in precedence order and
  the source of managed policy requirements.
- Start Codex with `--strict-config` to treat unrecognized `config.toml` keys as
  errors instead of ignoring them.

See [Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli) for the full
interactive command reference.

## Change settings for one run

Use a dedicated flag when one exists. Common examples include `--model`,
`--sandbox`, `--ask-for-approval`, `--profile`, and `--search`. Use `-c` or
`--config` to override any supported configuration key for one run:

```shell
codex --model gpt-5.5
codex --profile deep-review
codex --config model_reasoning_effort='"high"'
```

Command-line flags and `--config` values have the highest precedence. For the
complete flag list, see [Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli).

## Configuration layers

The CLI applies command-line flags and `--config` overrides before project,
profile, user, system, and built-in settings. Use that precedence to keep shared
defaults in configuration files and one-off changes on the command line.

For the complete order and common options, see [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic).

## Change settings in the TUI

The interactive terminal UI provides pickers for common session and display
settings:

| Goal                      | Command                                      | Related configuration                         |
| ------------------------- | -------------------------------------------- | --------------------------------------------- |
| Choose a model            | `/model`                                     | `model`, `model_reasoning_effort`             |
| Change permissions        | `/permissions`                               | Approval and sandbox settings                 |
| Choose a response style   | `/personality`                               | `personality`                                 |
| Configure optional tools  | `/experimental`, `/memories`                 | Feature-specific `config.toml` keys           |
| Customize the terminal UI | `/keymap`, `/statusline`, `/title`, `/theme` | Keys under `[tui]`                            |
| Set editing defaults      | `/vim`, `/raw`                               | `tui.vim_mode_default`, `tui.raw_output_mode` |

Some commands apply only to the current session, while some pickers offer to
save the choice. Set the related configuration key when you want a default for
future sessions. For the terminal theme, editor, completions, and shortcut
workflows, see [CLI customization](https://learn.chatgpt.com/docs/cli-customization).

## Settings references

- [Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) covers profiles, one-off overrides, and other advanced workflows.
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) lists the available keys and values.
- [Sample configuration](https://learn.chatgpt.com/docs/config-file/config-sample) provides a complete example file.
- [Environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables) documents variables used by the CLI and installer.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

The Codex IDE extension has two settings layers:

- **Codex settings** control agent behavior shared with Codex CLI, including the
  model, reasoning effort, permissions, sandbox, MCP servers, and
  personalization. Codex reads these settings from `config.toml`.
- **Editor settings** control how the extension behaves inside VS Code and
  compatible editors. These settings use `chatgpt.*` keys in the editor's
  settings system.

## Open Codex settings

Select the gear icon in the Codex sidebar, then select **Codex Settings**. Use
the settings panel for common agent controls, or select **Open config.toml** to
edit the active configuration layer directly.

For the configuration layer order and common keys, see [Config
basics](https://learn.chatgpt.com/docs/config-file/config-basic). For every supported `config.toml` key, see the
[Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Change an editor setting

To change a setting, follow these steps:

1. Open your editor settings.
2. Search for `@ext:openai.chatgpt`, `Codex`, or the setting name.
3. Update the value.

The extension also honors VS Code's built-in chat font settings for Codex chat surfaces.

## Editor settings reference

| Setting                                      | Default        | Description                                                                                                                                                                                                                                                                                |
| -------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `chatgpt.commentCodeLensEnabled`             | `true`         | Show CodeLens above `TODO` comments so Codex can address them.                                                                                                                                                                                                                             |
| `chatgpt.openOnStartup`                      | `false`        | Focus the Codex sidebar when the extension finishes starting.                                                                                                                                                                                                                              |
| `chatgpt.followUpQueueMode`                  | `queue`        | Choose whether messages sent during a run wait for the next run (`queue`) or steer the current run (`steer`). The extension treats the legacy `interrupt` value as `steer`. Press <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd> to invert the behavior for one message. |
| `chatgpt.composerEnterBehavior`              | `enter`        | Choose whether <kbd>Enter</kbd> always sends (`enter`), <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>Enter</kbd> sends multiline prompts (`cmdIfMultiline`), or the modifier is always required (`cmdAlways`).                                                                                      |
| `chatgpt.reviewDelivery`                     | `inline`       | Run `/review` in the current chat when possible (`inline`) or start a separate review chat (`detached`).                                                                                                                                                                                   |
| `chatgpt.localeOverride`                     | Auto           | Set the preferred language for the Codex UI. Leave empty to detect it automatically.                                                                                                                                                                                                       |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | `false`        | Windows only: Run Codex in WSL when WSL is available. Use this when your repositories and tooling live in WSL2 or when you need Linux-native tooling. Changing this setting reloads VS Code.                                                                                               |
| `chatgpt.cliExecutable`                      | Unset          | Development only: Set the path to the Codex CLI executable. You don't need this setting unless you're developing the Codex CLI; manually overriding the bundled executable can prevent parts of the extension from working.                                                                |
| `chat.fontSize`                              | Editor default | Control chat text in the Codex sidebar, including chat content and the composer.                                                                                                                                                                                                           |
| `chat.editor.fontSize`                       | Editor default | Control code-rendered content in Codex chats, including code snippets and diffs.                                                                                                                                                                                                           |

The `chatgpt.*` keys above belong to the IDE extension and don't go in
`config.toml`. For shared agent settings, use [Config
basics](https://learn.chatgpt.com/docs/config-file/config-basic), [Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced),
and the [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

</ContentModeSwitch>