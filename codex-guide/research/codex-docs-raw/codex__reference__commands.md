# Commands

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use these commands and keyboard shortcuts to navigate the app.

## Keyboard shortcuts

|             | Action              | Shortcut                                                                                                               |
| ----------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **General** |                     |                                                                                                                        |
|             | Command menu        | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>K</kbd>      |
|             | Settings            | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>,</kbd>                                                                          |
|             | Keyboard shortcuts  | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>/</kbd>                                                       |
|             | Open folder         | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>O</kbd>                                                                          |
|             | Navigate back       | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>[</kbd>                                                                          |
|             | Navigate forward    | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>]</kbd>                                                                          |
|             | Increase font size  | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>+</kbd>                                                                          |
|             | Decrease font size  | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>-</kbd>                                                                          |
|             | Toggle sidebar      | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>B</kbd>                                                                          |
|             | Open review tab     | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd>                                                                      |
|             | Toggle review panel | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>B</kbd>                                                         |
|             | Toggle bottom panel | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>J</kbd>                                                                          |
|             | Toggle terminal     | <kbd>Ctrl</kbd> + <kbd>`</kbd>                                                                                         |
|             | Clear the terminal  | <kbd>Ctrl</kbd> + <kbd>L</kbd>                                                                                         |
| **Chat**    | Quick chat          | <kbd>Cmd</kbd> + <kbd>Option</kbd> + <kbd>N</kbd> (macOS) or <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>N</kbd> (Windows) |
|             | New chat            | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>N</kbd> or <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd>      |
|             | Search chats        | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>G</kbd>                                                                          |
|             | Find in chat        | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>F</kbd>                                                                          |
|             | Previous chat       | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>[</kbd>                                                       |
|             | Next chat           | <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>]</kbd>                                                       |
| **Input**   | Dictation           | <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd>                                                                      |

To find, customize, or reset shortcuts, open **Settings > Keyboard Shortcuts**.
You can search by command name or switch the search field into keystroke mode
and press the shortcut you want to find.

<a id="search-past-tasks-and-find-in-a-task"></a>

## Search past chats and find in a chat

Use chat search (<kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>G</kbd>) to reopen a past
chat. When expanded matching is available, it can also match chat content and
Git branch names, so you can search for a phrase from the chat or a
branch such as `fix/login-redirect`.

Use **Find in chat** (<kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>F</kbd>) after opening
a chat to find text within it. It doesn't search across other chats.

For actions that start with `/`, see [Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands).

## Deep links

The ChatGPT desktop app keeps the `codex://` URL scheme for compatibility, so
links can open specific parts of the app directly. Encode query string values
before adding them to a URL.

### Supported links

Use these canonical forms when you create links. The sections below list the full reference by link type.

| Deep link                                                                   | Opens                                                   |
| --------------------------------------------------------------------------- | ------------------------------------------------------- |
| `codex://threads/new`                                                       | A new local chat.                                       |
| `codex://new?<query>`                                                       | A new local chat with at least one query parameter.     |
| `codex://threads/<thread-id>`                                               | A local chat. `<thread-id>` is its technical thread ID. |
| `codex://settings`                                                          | Settings.                                               |
| `codex://settings/connections/<connection-type>`                            | Computer, device, or SSH connection settings.           |
| `codex://settings/connections/ssh/add?name=<ssh-config-host>`               | Adds a host from your SSH config to Codex.              |
| `codex://skills`                                                            | Skills.                                                 |
| `codex://automations`                                                       | Scheduled with the create flow open.                    |
| `codex://plugins/install/<plugin-name>?marketplace=<marketplace-name>`      | The install flow for a plugin from a known marketplace. |
| `codex://plugins/<plugin-id>`                                               | A plugin detail page.                                   |
| `codex://plugins/<plugin-name>?marketplacePath=<absolute-marketplace-path>` | A local plugin detail page from a local marketplace.    |
| `codex://pets/install?name=<pet-name>&imageUrl=<https-image-url>`           | The pet install flow.                                   |

<a id="tasks"></a>

### Chats

Use these links when you need to open an existing local chat or start a new one.

| Deep link                     | Opens                                                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `codex://threads/<thread-id>` | A local chat. `<thread-id>` is its technical thread ID.                                                      |
| `codex://threads/new`         | A new local chat.                                                                                            |
| `codex://threads/new?<query>` | A new local chat with optional query parameters.                                                             |
| `codex://new?<query>`         | A new local chat. Include at least one of `prompt`, `path`, or `originUrl`; otherwise the link does nothing. |

For `codex://threads/new` or `codex://new`, add any of these query parameters as needed; you can combine them in the same URL.

| Query parameter              | Required | What it does                                                                                                                                                  |
| ---------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt=<text>`              | No       | Sets the initial composer text.                                                                                                                               |
| `path=<absolute-path>`       | No       | Opens the new chat in a local workspace. `path` must be an absolute path to a local directory. When valid, Codex uses that directory as the active workspace. |
| `originUrl=<git-remote-url>` | No       | Matches one of your current workspace roots by Git remote URL. If `path` is also present, Codex resolves `path` first.                                        |

Example: [Show me some fun stats about how I've been using Codex](codex://threads/new?prompt=Show%20me%20some%20fun%20stats%20about%20how%20I%27ve%20been%20using%20Codex)

<a id="start-a-task-with-a-plugin"></a>

#### Start a chat with a plugin

To help users start a plugin-backed chat, include a plugin mention in the
prompt before you encode it:

```text
[@Example](plugin://example@openai-curated) Summarize this document: https://example.com/document/123
```

Encode the complete prompt as a URI component—for example, with
`encodeURIComponent` in JavaScript—and pass it to the `prompt` parameter:

```text
codex://new?prompt=%5B%40Example%5D(plugin%3A%2F%2Fexample%40openai-curated)%20Summarize%20this%20document%3A%20https%3A%2F%2Fexample.com%2Fdocument%2F123
```

The link opens a new chat with the decoded prompt in the composer. It doesn't
send the prompt automatically. After the user sends it, Codex can use an
installed plugin in that chat. If the plugin isn't installed but is available
to the user, Codex asks the user to install it and connect any required connectors.
After setup, the user can select **Continue** to resume the same chat. Workspace
settings can limit which plugins a user can install. For plugin installation
and permission details, see [Plugins](https://learn.chatgpt.com/docs/plugins).

### Settings

Use these links when you need to open Settings or a specific settings page.

| Deep link                                                     | Opens                                                                                        |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `codex://settings`                                            | Settings.                                                                                    |
| `codex://settings/browser-use`                                | Browser settings.                                                                            |
| `codex://settings/computer-use/google-chrome`                 | Google Chrome settings for computer use.                                                     |
| `codex://settings/connections`                                | Remote connections settings.                                                                 |
| `codex://settings/connections/computer`                       | Settings for controlling this Mac or PC from another device.                                 |
| `codex://settings/connections/devices`                        | Settings for controlling other devices.                                                      |
| `codex://settings/connections/ssh`                            | SSH connection settings.                                                                     |
| `codex://settings/connections/ssh/add?name=<ssh-config-host>` | Adds the named host alias as a Codex-managed connection, then opens SSH connection settings. |

The `name` value must match a host alias in `~/.ssh/config`. The link disables
automatic connection for the added host. If Codex can't find the named host, it
opens SSH connection settings and shows an error.

Unsupported `codex://settings/...` paths open the main Settings page.

### Skills

Use these links when you need to open Skills.

| Deep link        | Opens   |
| ---------------- | ------- |
| `codex://skills` | Skills. |

### Scheduled

Use these links when you need to open **Scheduled**.

| Deep link             | Opens                                |
| --------------------- | ------------------------------------ |
| `codex://automations` | Scheduled with the create flow open. |

### Plugins

Plugin links use different forms depending on whether you are installing from a marketplace, opening a plugin, or working from a local `marketplace.json`. For plugin basics, see [Plugins](https://learn.chatgpt.com/docs/plugins). For local or repo marketplace setup, see [Build plugins](https://developers.openai.com/plugins/build/plugins#build-your-own-curated-plugin-list).

#### Plugin install

Use this form to open the install flow for a plugin from a marketplace that Codex already knows about.

| Deep link                                                              | Opens                                           |
| ---------------------------------------------------------------------- | ----------------------------------------------- |
| `codex://plugins/install/<plugin-name>?marketplace=<marketplace-name>` | The plugin detail or install flow for a plugin. |

| Query parameter                  | Required | What it does                                                                    |
| -------------------------------- | -------- | ------------------------------------------------------------------------------- |
| `marketplace=<marketplace-name>` | Yes      | Identifies the marketplace. For an OpenAI-curated plugin, use `openai-curated`. |

The install link accepts only the `marketplace` query parameter. If Codex can't find the requested marketplace or plugin, it opens the Plugins page instead.

#### Plugin detail

| Deep link                     | Opens                 |
| ----------------------------- | --------------------- |
| `codex://plugins/<plugin-id>` | A plugin detail page. |

`<plugin-id>` must identify the plugin. For an OpenAI-curated plugin, use the form `<plugin-name>@openai-curated`.

Codex-generated plugin links can also include these query parameters. Omit both when you write a link manually.

| Query parameter    | Required | What it does                                                                                                                                    |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `hostId=<host-id>` | No       | Identifies the Codex host that owns the plugin context, such as `local` or one of your configured remote connections. Codex provides these IDs. |
| `source=manage`    | No       | Preserves the app's plugin-management entry point. It's not admin-only.                                                                         |

Example: [Open the OpenAI Developers plugin](codex://plugins/openai-developers@openai-curated)

#### Local plugin

For local or repo marketplace setup, see [Build plugins](https://developers.openai.com/plugins/build/plugins#build-your-own-curated-plugin-list).

| Deep link                                                                   | Opens                                                |
| --------------------------------------------------------------------------- | ---------------------------------------------------- |
| `codex://plugins/<plugin-name>?marketplacePath=<absolute-marketplace-path>` | A local plugin detail page from a local marketplace. |

| Query parameter                               | Required | What it does                                                                                               |
| --------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------- |
| `marketplacePath=<absolute-marketplace-path>` | Yes      | Absolute path to the local `marketplace.json`, for example `/Users/alex/.agents/plugins/marketplace.json`. |
| `mode=share`                                  | No       | Opens the share flow for that local plugin.                                                                |

### Pets

Use these links to open the pet install flow when that feature is enabled.

| Deep link                                                         | Opens                 |
| ----------------------------------------------------------------- | --------------------- |
| `codex://pets/install?name=<pet-name>&imageUrl=<https-image-url>` | The pet install flow. |

| Query parameter                | Required | What it does                                                                                |
| ------------------------------ | -------- | ------------------------------------------------------------------------------------------- |
| `name=<pet-name>`              | Yes      | Sets the pet name. The value must contain at least one non-whitespace character.            |
| `imageUrl=<https-image-url>`   | Yes      | Provides an absolute HTTPS URL for the pet image or sprite sheet.                           |
| `description=<text>`           | No       | Adds a description to the install flow.                                                     |
| `spriteVersionNumber=<1-or-2>` | No       | Selects the sprite-sheet format. The default is `1`; the only other supported value is `2`. |

The install link accepts only these query parameters. Invalid names, non-HTTPS
image URLs, unsupported sprite versions, or extra path segments cause the link
to do nothing.

## See also

- [Features](https://learn.chatgpt.com/docs/features)
- [Settings](https://learn.chatgpt.com/docs/reference/settings)
- [Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands)