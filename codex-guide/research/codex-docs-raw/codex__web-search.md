# Web search

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

ChatGPT includes a first-party web search tool. Treat all web results as
untrusted input.

<ContentModeSwitch group="codex-surface" id="app">

In the ChatGPT desktop app, ask for current information in a chat. ChatGPT records
search activity with the other tool calls in the transcript.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

In ChatGPT web, ask for current information or sources. Search results and
citations appear in the chat when ChatGPT uses web search. Workspace
settings can limit whether search is available.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

In the CLI, pass `--search` to fetch live results for one run:

```bash
codex --search "Summarize the latest release notes for this dependency"
```

Searches appear as `web_search` items in the interactive transcript and in
`codex exec --json` output.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

In the IDE extension, ask Codex to search while you work in the editor. The
extension uses the connected Codex host's search mode. Search activity appears
in the chat transcript.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

## Configure local web search

For local Codex chats, Codex enables cached search by default. Cached mode uses
an OpenAI-maintained index instead of fetching arbitrary pages live, which
lowers—but doesn't remove—prompt injection risk.

Use live search when your task depends on the latest information. Set
`web_search = "live"` in `config.toml`. Set `web_search = "disabled"` to turn
the tool off. The `"indexed"` mode permits external web access only when the
search index gates the request. When Codex runs with full access, web search
defaults to live results. See [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
for config file locations and precedence.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

For network boundaries that apply to Codex cloud environments, see [Internet
access](https://learn.chatgpt.com/docs/cloud/internet-access).

</ContentModeSwitch>