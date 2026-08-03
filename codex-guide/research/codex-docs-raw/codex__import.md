# Import from another agent

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use the import flow to bring your instructions, settings, skills, plugins,
projects, and recent work from other agents into the ChatGPT desktop app. The
app imports supported items directly and lets you finish setup for any imported
plugins or connections that need authorization.

Importing doesn't change or delete your existing agent setup.

<Illustration description="ChatGPT import screen for choosing other AI apps to import from.">
  <ExternalAgentImportIllustration step="providers" />
</Illustration>

## Start an import

<WorkflowSteps>

1. In the ChatGPT desktop app, open **Settings > Import**. If **Import** isn't
   available as a settings section yet, open **General** and find **Import other
   agent setup**.
2. Select **Import**.
3. Choose the agents you want to import from, then select **Continue**.
4. On **Select items to import**, choose what to bring over, then select **Continue**.
5. After the import finishes, open an imported project or chat to continue working.

</WorkflowSteps>

<Illustration description="ChatGPT import screen for selecting setup, projects, and recent chats to import.">
  <ExternalAgentImportIllustration step="items" />
</Illustration>

## How importing works

The import flow checks both your user-level setup and your existing projects.
User-level setup comes from files on your machine. Project-level setup comes
from files in the repositories and folders you select.

When you import, ChatGPT:

1. Detects supported setup and recent work.
2. Imports the items you select.
3. Leaves your existing agent setup unchanged.
4. Checks whether imported plugins or connections still need setup.
5. Shows a status card when you need to finish setup.

## What ChatGPT can import

| Imported item               | Destination                                          |
| --------------------------- | ---------------------------------------------------- |
| Instruction files           | [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)  |
| `settings.json`             | [`config.toml`](https://learn.chatgpt.com/docs/config-file/config-basic)     |
| Skills                      | [Skills](https://learn.chatgpt.com/docs/build-skills)                        |
| Plugins                     | Plugins                                              |
| Existing project folders    | Projects using the same folders                      |
| Chats from the last 30 days | ChatGPT chats                                        |
| MCP server configuration    | [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp)         |
| Hooks                       | [Codex hooks](https://learn.chatgpt.com/docs/hooks)                          |
| Slash commands              | [Skills](https://learn.chatgpt.com/docs/build-skills)                        |
| Subagents                   | [Codex agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) |

## Finish setup after importing

When the import completes, the app shows a status card in the lower-left corner.
If an imported plugin or connection still needs setup, the card calls it out.

When the app flags an item that needs attention, select **Finish** and follow the
prompts to complete setup.

## What to review after importing

Review imported setup before you rely on it, especially:

- Tool restrictions or permissions in imported skills and agents.
- MCP server settings that use custom authentication, headers, environment
  variables, or transports. You may need to sign in again.
- Hooks whose behavior may differ after import.
- Plugins, marketplaces, or other setup that needs manual follow-up.
- Prompt templates or command-style prompts that depend on arguments, shell
  interpolation, or file-path placeholders.

## After you import

Once the import finishes, open one of your imported projects and continue from
there. See [Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt) for guidance on starting your
next task.