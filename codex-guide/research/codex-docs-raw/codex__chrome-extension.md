# Chrome extension

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use the Chrome extension to let ChatGPT control your Chrome browser. ChatGPT can
read or act on sites where you're already signed in, such as LinkedIn,
Salesforce, Gmail, or internal tools.

To let ChatGPT control its built-in browser instead, use `@Browser`. The
[built-in browser](https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app)
supports sign-in and keeps browsing work inside ChatGPT without using your
Chrome profile.

ChatGPT can also switch between tools as a task requires, using plugins when a
dedicated integration is available, Chrome when it needs logged-in browser
context, and the built-in browser for localhost.



  <Alert
    client:load
    color="warning"
    variant="soft"
    description="Treat page content as untrusted context, and review the website before allowing ChatGPT to continue."
  />



## Use ChatGPT from Chrome

Open ChatGPT beside the page you're viewing to ask about the page or continue
into tasks that can use its context alongside local files and connected apps.
ChatGPT can use context from your open tabs when a task needs it.

1. Open the page you want to work with.
2. Select ChatGPT from the Chrome toolbar or **Extensions** menu. On macOS, you
   can also press <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd>.
3. Ask a question about the page or give ChatGPT a task.

The panel stays with the tab where you opened it. Chats you start in Chrome
are available in the ChatGPT app, and you can open recent ChatGPT chats in
Chrome, so you can continue work in either place.

<Illustration description="ChatGPT open beside the current Chrome tab.">
  <ChromeSidePanelIllustration
    ariaLabel="ChatGPT open beside the current Chrome tab."
    backgroundImage="/images/codex/codex-wallpaper-1.webp"
  />
</Illustration>

## Set up the Chrome extension

In the ChatGPT desktop app, open the Plugins Directory and install **Chrome**.
Other Chromium-based browsers aren't currently supported. Follow the setup flow
to:

1. Install the [Chrome
   extension](https://chromewebstore.google.com/detail/chatgpt/hehggadaopoacecdllhhajmbjkdcmajg).
2. Approve Chrome's permission prompts.
3. Open Chrome and confirm the ChatGPT side chat loads.

<Illustration description="Computer Use settings showing Google Chrome connected through the Chrome extension.">
  <ComputerUseSettingsIllustration
    ariaLabel="Computer Use settings showing Google Chrome connected through the Chrome extension."
    aspectRatio="3 / 1"
    controlRows={[
      {
        id: "chrome",
        title: "Google Chrome",
        description: "Connected to browser extension for additional control",
        icon: "chrome",
        enabled: true,
        connected: true,
        manageLabel: "Manage",
      },
    ]}
    showAlwaysAllowedApps={false}
  />
</Illustration>

## Start a Chrome task from ChatGPT

After the plugin setup is complete, start a new ChatGPT Work or Codex chat. ChatGPT
can use Chrome automatically when a task needs a website and you're already
signed in to Chrome. You can also invoke it directly in a prompt:

```text
@Chrome open Salesforce and update the account from these call notes.
```

If Chrome isn't already open, ChatGPT can open it. Chrome browser tasks run in
Chrome tab groups so the work for a task stays grouped together.

## Control website access

By default, ChatGPT asks before it interacts with each new website. ChatGPT bases
the prompt on the website host, such as `example.com`.

When ChatGPT asks to use a website, you can choose the option that matches the
task and your risk tolerance:

- **Allow once** to let ChatGPT use the website one time.
- **Allow for this site** so ChatGPT can use the website again without asking.
- **Allow for all sites** so ChatGPT can use websites without asking.
- **Decline** to prevent ChatGPT from using the website.

### Manage allowed and blocked websites

In the ChatGPT desktop app, go to **Settings** > **Computer Use**, then select
**Manage** next to **Google Chrome** to manage an allowlist and blocklist for
domains. The allowlist contains domains ChatGPT can use without asking again.
The blocklist contains domains ChatGPT shouldn't use.

Removing a domain from the allowlist means ChatGPT asks again before using it.
Removing a domain from the blocklist means ChatGPT can ask again instead of
treating the domain as blocked.

#### Allow for all sites <ElevatedRiskBadge class="ml-2" />

If you select **Allow for all sites**, ChatGPT no longer asks for confirmation
before using websites. Only choose this option if you trust ChatGPT to use any
website open in Chrome.

#### Browser history <ElevatedRiskBadge class="ml-2" />

Browser history can include sensitive telemetry, internal URLs, search terms,
and activity from Chrome sessions on signed-in devices. If you allow ChatGPT to
access browser history, relevant history entries can become part of the context
ChatGPT uses for the task. Malicious or misleading page content can increase the
risk that ChatGPT copies this data somewhere unintended.

ChatGPT asks when it wants to use browser history. ChatGPT scopes history access to
the request, and history doesn't have an always-allow option.

## Data and security

### Chrome extension permissions

Chrome asks you to accept extension permissions when you install the extension.
The permission prompt may include:

- Access the page debugger
- Read and change all your data on all websites
- Read and change your browsing history on all your signed-in devices
- Display notifications
- Read and change your bookmarks
- Manage your downloads
- Communicate with cooperating native applications
- View and manage your tab groups

These Chrome permissions make the extension capable of operating browser
workflows. ChatGPT still uses its own confirmations, settings, allowlists, and
blocklists before using websites or browser history during a task.

### Memories

Computer Use follows your Memories setting. If Memories is on, ChatGPT can
use relevant saved memories while working in Chrome. If Memories is off, browser
control doesn't use memories.

### What OpenAI stores from browsing

OpenAI doesn't store a separate complete record of your Chrome actions from the
extension. OpenAI stores browser activity only when it becomes part of the ChatGPT
context, such as text ChatGPT reads from a page, screenshots, tool calls,
summaries, messages, or other content included in the chat.

Your ChatGPT data controls apply to content processed in context.
Avoid sending secrets or highly sensitive data through browser tasks unless
they're required and you are present to review each prompt.

## Troubleshooting

If ChatGPT can't connect to Chrome, first confirm the website ChatGPT is trying to
access isn't in the blocklist in Settings. If the website isn't blocked, work
through these checks:

1. Update the ChatGPT desktop app. If you have more than one ChatGPT or Codex
   desktop app installed, update each one or remove copies you no longer use.
2. Close the ChatGPT side panel, restart Chrome, then reopen the extension from
   the Chrome toolbar or **Extensions** menu. Confirm the side chat loads. If
   it doesn't load or mentions a missing native host, remove and re-add the
   Chrome plugin from **Plugins** in the ChatGPT desktop app, then follow the
   setup flow again.
3. In the app, select ChatGPT and turn on Work in the switcher, or select Codex. Open
   **Plugins** and confirm that the Chrome plugin is on. If the plugin is off,
   turn it on and try the task again.
4. Make sure you are using the same Chrome profile where the extension is
   installed. If you use more than one Chrome profile, install and enable the
   extension in the active profile.
5. Start a new ChatGPT Work or Codex chat and try the Chrome task again. This can
   clear chat-specific connection state.
6. Restart the ChatGPT desktop app, then try again. If the extension still
   doesn't connect, uninstall the Chrome extension, remove and re-add the Chrome
   plugin from **Plugins**, and follow the setup flow again.
7. If the side chat loads but ChatGPT still can't use Chrome, run `/feedback`
   in the app and include the chat ID when you contact support.

### Upload files

If a Chrome task needs to upload a file from your computer, allow the Chrome
extension to access file URLs in Chrome:

1. In Chrome, open the extensions icon in the toolbar, then click **Manage
   Extensions**.
2. On the extension card, click **Details**.
3. Turn on **Allow access to file URLs**.

After you change the setting, start the Chrome task again.