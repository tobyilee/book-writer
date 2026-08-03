# Build plugins

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

To build or submit a plugin, use the complete
[builder documentation on developers.openai.com](https://developers.openai.com/plugins).



  <ButtonLink href="/plugins" color="primary" variant="solid" size="lg">
    Build and submit a plugin
  </ButtonLink>



This page provides a brief introduction. A plugin is an installable package
that can include skills, an MCP server, or both. An MCP server can also return
optional UI.

ChatGPT and Codex share one universal plugin directory. Publish a public plugin
once to make the same listing discoverable from supported surfaces in both
products. During development, use a local marketplace to test the package
before submitting it to the universal directory.

Start with a skill when you are still iterating on one personal workflow.
Build a plugin when you want to share that workflow, package related skills,
connect to an external service, or distribute a stable capability to a team.

## Create a plugin with `@plugin-creator`

For the fastest setup, use the built-in `@plugin-creator` skill in ChatGPT Work
mode or `$plugin-creator` in Codex.

<CodexScreenshot
  alt="Plugin creator skill in ChatGPT"
  lightSrc="/images/codex/plugins/plugin-creator.png"
  darkSrc="/images/codex/plugins/plugin-creator-dark.png"
/>

Describe the outcome, the skills or MCP server to include, and whether you want
a local marketplace entry for testing. For example:

```text
@plugin-creator Create a plugin named meeting-follow-up.
Include a skill that turns meeting notes into decisions, owners, and next steps.
Add it to a personal marketplace so I can test it locally.
```

The skill creates the required `.codex-plugin/plugin.json` manifest, organizes
the plugin folder, and can add the plugin to a local marketplace.

<CodexScreenshot
  alt="Invoking the plugin creator skill"
  lightSrc="/images/codex/plugins/plugin-creator-invoke.png"
  darkSrc="/images/codex/plugins/plugin-creator-invoke-dark.png"
/>

After it finishes:

1. Review `.codex-plugin/plugin.json`.
2. Check each bundled skill under `skills/`.
3. Refresh ChatGPT or Codex and install the plugin from its local marketplace
   source.
4. Test the plugin in a new conversation with representative requests.

If the plugin includes an MCP server, first build and test that server, then
give `@plugin-creator` the registered connection details. Follow the complete
[MCP server workflow](https://developers.openai.com/plugins/build/mcp-server)
for tools, authentication, deployment, and testing.

## Create a skills-only plugin manually

A minimal plugin contains a manifest and at least one skill:

```text
meeting-follow-up/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── meeting-follow-up/
        └── SKILL.md
```

Create `.codex-plugin/plugin.json`:

```json
{
  "name": "meeting-follow-up",
  "version": "1.0.0",
  "description": "Turn meeting notes into decisions and next steps",
  "skills": "./skills/"
}
```

Then add `skills/meeting-follow-up/SKILL.md`:

```md
---
name: meeting-follow-up
description: Extract decisions, owners, and next steps from meeting notes.
---

Review the meeting notes. Return:

1. Decisions
2. Action items with owners
3. Open questions
```

Use a stable plugin name in kebab case. Keep the skill description specific
enough for ChatGPT and Codex to recognize when the workflow applies.

Use `@plugin-creator` to add the folder to a local marketplace, then install and
test it before sharing it.

## Continue with the builder documentation

For complete builder documentation, use the
[Plugins documentation](https://developers.openai.com/plugins/). It covers:

- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [Building skills](https://developers.openai.com/plugins/build/skills)
- [Building an MCP server](https://developers.openai.com/plugins/build/mcp-server)
- [Adding optional UI](https://developers.openai.com/plugins/build/chatgpt-ui)
- [Packaging a plugin](https://developers.openai.com/plugins/build/plugins)
- [Testing a plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Submitting and publishing](https://developers.openai.com/plugins/deploy/submission)

To browse, install, enable, or remove plugins, see [Use
plugins](https://learn.chatgpt.com/docs/plugins).