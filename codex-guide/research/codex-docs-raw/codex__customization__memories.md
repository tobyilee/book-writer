# Memories

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Memories let ChatGPT and Codex carry useful context from earlier work into
future work.
ChatGPT web uses ChatGPT memory, while local Codex clients use a separate local
memory store and controls.

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

Keep required team guidance in `AGENTS.md` or checked-in documentation. Treat
memories as a helpful recall layer, not as the only source for rules that must
always apply.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

In the ChatGPT desktop app, use `/memories` to choose whether a chat can use
local memories or contribute to future memories. Manage the feature from
**Settings > Personalization** when you need to turn it on or off.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

Manage ChatGPT memory from **Settings > Personalization**. ChatGPT Work uses
the memory settings available to your account and workspace; it doesn't use a
local Codex memory store or local memory controls.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

In Codex CLI, use `/memories` in an interactive session to control whether the
current chat can use existing local memories or become an input for future
memories. See [Configure local memories](#configure-local-memories) if the
command isn't available.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

The IDE extension uses the connected Codex host's local memory store. When
memories are enabled for that host, use the same chat-level controls as Codex
CLI.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

[Chronicle](https://learn.chatgpt.com/docs/customization/chronicle) is a desktop-only feature that helps
Codex recover recent working context from your screen to build up memory.

</ContentModeSwitch>

<a id="how-memories-work"></a>
<a id="memory-storage"></a>
<a id="control-memories-per-thread"></a>
<a id="control-memories-per-chat"></a>
<a id="control-memories-per-task"></a>
<a id="review-memories"></a>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

## How local Codex memories work

After you enable memories, Codex can turn useful context from eligible prior
chats into local memory files. Codex skips active or short-lived sessions,
redacts secrets from generated memory fields, and updates memories in the
background instead of immediately at the end of every chat.

Memories may not update right away when a chat ends. Codex waits until a
chat has been idle long enough to avoid summarizing work that's still in
progress.

Memory generation can also skip a background pass when your Codex rate-limit
remaining percentage is below the configured threshold, so Codex doesn't spend
quota when you're near a limit.

## Local memory storage

Codex stores memories under your Codex home directory. By default, that's
`~/.codex`. See [Config and state locations](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations)
for how Codex uses `CODEX_HOME`.

The main memory files live under `~/.codex/memories/` and include summaries,
durable entries, recent inputs, and supporting evidence from prior chats.

Treat these files as generated state. You can inspect them when troubleshooting
or before sharing your Codex home directory, but don't rely on editing them by
hand as your primary control surface.

<a id="control-local-memories-per-task"></a>

## Control local memories per chat

In the ChatGPT desktop app and Codex TUI, use `/memories` to control memory behavior for
the current chat. Chat-level choices let you decide whether the current
chat can use existing memories and whether Codex can use the chat to
generate future memories.

Chat-level choices don't change your global memory settings.

## Review local memories

Don't store secrets in memories. Codex redacts secrets from generated memory
fields, but you should still review memory files before sharing your Codex home
directory or generated memory artifacts.

<a id="enable-memories"></a>
<a id="configuration"></a>

## Configure local memories

Local Codex memories are off by default. In the ChatGPT desktop app, open
**Settings > Personalization** and turn on **Enable memories**.

For config-based setup, add the feature flag to `config.toml`:

```toml
[features]
memories = true
```

For config file locations and the full list of memory-related settings, see
[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) and the [configuration
reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Common memory-specific settings include:

- `memories.generate_memories`: controls whether newly created chats can be
  stored as memory-generation inputs.
- `memories.use_memories`: controls whether Codex injects existing memories into
  future sessions.
- `memories.disable_on_external_context`: when `true`, keeps chats that used
  external context such as MCP tool calls, web search, or tool search out of
  memory generation. The older `memories.no_memories_if_mcp_or_web_search` key
  is still accepted as an alias.
- `memories.min_rate_limit_remaining_percent`: controls the minimum remaining
  Codex rate-limit percentage required before memory generation starts.
- `memories.extract_model`: overrides the model used for per-chat memory
  extraction.
- `memories.consolidation_model`: overrides the model used for global memory
  consolidation.

</ContentModeSwitch>