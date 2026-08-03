# What's new

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

This weekly digest highlights ChatGPT and Codex features that can change how you
work, with examples and links to learn more. For every versioned update, bug fix,
and minor improvement, see the [Codex changelog](https://learn.chatgpt.com/docs/changelog).

## July 20–24, 2026

### Talk through work with ChatGPT Voice

[ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice), powered by GPT-Live, lets you talk
through work and coordinate tasks in Chat, Work, and Codex in the ChatGPT desktop
app. Start a new chat or task in voice mode, then ask ChatGPT to start, check, or
steer work in other threads.

On macOS, say, “Take a look at this” to share an [appshot](https://learn.chatgpt.com/docs/appshots) of
your frontmost window when **Screen context** is on.

Voice is available with Plus, Pro, Business, Edu, and Enterprise plans in the
desktop app and through [Remote on iOS](https://learn.chatgpt.com/docs/remote-connections#set-up-mobile-access).

### Work across multiple folders in one local project

Local projects in the ChatGPT desktop app can now include multiple related
folders. Choose a primary folder for new chats, Git operations, and automatic
discovery of `AGENTS.md`, skills, and `config.toml`. Secondary folders remain
available for file search, reading, and editing.

Open **Edit project** to [add folders and choose the primary
folder](https://learn.chatgpt.com/docs/projects#use-local-projects-for-folders-and-codebases).

[Read the July 23 release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-07-23-app).

## July 13–17, 2026

### Keep Work conversations and Projects together on desktop

The ChatGPT desktop app now keeps Chat and Work conversations together in the
ChatGPT view. Cloud Work conversations sync across web, mobile, and desktop;
local Work conversations stay on your computer. ChatGPT Projects are available
in the desktop app. Codex keeps its dedicated view and separate history for
developer workflows.

[Compare ChatGPT Work and Codex on
desktop](https://learn.chatgpt.com/docs/use-chatgpt#compare-chatgpt-work-and-codex-on-desktop) to choose the
view that fits your task.



**Prompt:**

```text
Open the Launch project, review its files and recent conversations, and continue the launch plan from the latest Work conversation.
```

### Control parallel Codex work with Codex Micro

On July 15, OpenAI and Work Louder launched
[Codex Micro](https://learn.chatgpt.com/docs/features/codex-micro), a limited-run physical control
surface for Codex in the ChatGPT desktop app. Its Agent Keys show the status of
up to six chats and switch between them. Customizable Command Keys, an analog
stick, and a dial can trigger common actions or skills, start push-to-talk, and
adjust reasoning effort without leaving the keyboard.

### Use GPT-5.6 through Amazon Bedrock

GPT-5.6 Sol, Terra, and Luna reached general availability through Amazon
Bedrock. Local ChatGPT Work and Codex surfaces can use the built-in
[`amazon-bedrock` provider](https://learn.chatgpt.com/docs/amazon-bedrock) with a Bedrock API key or the
AWS SDK credential chain. This includes Work and Codex in the ChatGPT desktop
app, Codex CLI, the IDE extension, and the Codex SDK.

### Inspect Codex task visualizations on iOS

ChatGPT for iOS 1.2026.188 added inline visualizations to Codex tasks and
improved creating and managing tasks from conversations, including reliable
links to newly created tasks. Read the
[July 13 iOS release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-07-13-mobile).

## July 6–10, 2026

<a id="take-on-ambitious-work-with-chatgpt-work"></a>

### Take on ambitious work in ChatGPT

[ChatGPT Work](https://learn.chatgpt.com/docs/get-started-with-work) in ChatGPT can gather context from
your files and [plugins](https://learn.chatgpt.com/docs/plugins),
take action across workflows, and create reviewable documents, presentations,
spreadsheets, Sites, and other finished work. Powered by
[GPT-5.6](https://learn.chatgpt.com/docs/models), it can break a goal into steps and work for hours while
you follow its progress, answer questions, change direction, and approve
important actions.

[Scheduled tasks](https://learn.chatgpt.com/docs/automations) can keep that work moving when you're away
by running once, on a schedule, when an event occurs, or while monitoring for
changes.



**Prompt:**

```text
Create a launch brief from the attached research and campaign template. Show me the plan and flag missing information before you build the final document, then adapt the approved brief into assets for three markets.
```

### Choose the right GPT-5.6 model

The [GPT-5.6 family](https://learn.chatgpt.com/docs/models#recommended-models) offers three recommended
models across ChatGPT Work, the ChatGPT desktop app, Codex CLI, and the Codex IDE
extension. Sol is the flagship for complex coding, computer use, research, and
security work. Terra balances capability and cost for everyday work, while Luna
is the fastest, lowest-cost option. The default **Power** setting uses Sol with
medium reasoning.

### Use Codex in the ChatGPT desktop app

On July 9, the Codex app merged into the
[ChatGPT desktop app](https://learn.chatgpt.com/docs/app) for macOS and Windows. Codex keeps its
dedicated coding experience alongside ChatGPT's Chat and Work. The Codex
experience includes inline editing in diffs, pull request review in the side panel, faster
[Computer Use](https://learn.chatgpt.com/docs/computer-use) powered by GPT-5.6, and multi-repository
projects.

Existing Codex app users can update as usual. You can make Codex the default
view, use the Codex logo as the app icon, and access desktop Codex projects from
the ChatGPT mobile app. The updated desktop app is available globally on every
ChatGPT plan, including Free.

## June 15–19, 2026

### Turn demonstrated workflows into reusable skills

[Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay) lets you show ChatGPT or
Codex a workflow on macOS and turn the demonstration into a reusable skill. Use
it for repetitive tasks that are easier to show than describe, then refine the
generated skill and replay it with new inputs. Initial availability excludes
the EEA, the United Kingdom, and Switzerland, and requires Computer Use.

<a id="continue-a-task-on-another-host"></a>

### Continue a chat on another host

[Chat handoff](https://learn.chatgpt.com/docs/remote-connections#hand-off-a-chat-between-hosts)
moves a chat and its Git state between your local computer and a connected
remote host. Codex can create or reuse a worktree on the destination, transfer
the chat, and continue from the matching project.

The same desktop release adds bulk actions to scheduled run history, so
you can mark every run as read or archive eligible runs together.

### Browse and review workspaces from iOS

In the ChatGPT mobile app, **Remote** added a workspace file browser, a
directory picker for new chats, expand-and-collapse controls for diffs, and
per-chat or cross-chat MCP approval choices on iOS.

Computer Use, the Chrome extension, Memories, and Chronicle also began
rolling out to the EEA, the United Kingdom, and Switzerland. Memories remain
off by default in those regions, and Chronicle is an opt-in research preview
for ChatGPT Pro subscribers on macOS.

Read the [June 15 iOS](https://learn.chatgpt.com/docs/changelog#codex-2026-06-15-mobile),
[June 16 availability](https://learn.chatgpt.com/docs/changelog#codex-2026-06-16-app), and
[June 18 app](https://learn.chatgpt.com/docs/changelog#codex-2026-06-18-app) release notes.

## June 8–12, 2026

### Debug web apps with Browser Developer mode

[Developer mode](https://learn.chatgpt.com/docs/browser?surface=app#app-developer-mode) gives Codex controlled
access to Chrome DevTools Protocol capabilities in Chrome and the built-in
browser. Codex can inspect network traffic, console output, runtime errors, and
page state while it profiles or debugs your app. Under **Developer mode** in
**Settings** > **Browser**, turn on **Enable full CDP access**. Codex asks for
explicit approval before it uses that access on a website.

Browser use is also up to twice as fast because CDP and DOM snapshot
optimizations reduce browser round trips.

<CodexScreenshot
  alt="Codex Browser settings with Developer mode enabled"
  lightSrc="/images/codex/app/browser-developer-mode-light.webp"
  darkSrc="/images/codex/app/browser-developer-mode-dark.webp"
  maxHeight="420px"
  variant="no-wallpaper"
/>



**Prompt:**

```text
Use @Browser to reproduce the slow checkout. Inspect the network timing and console errors, fix the cause, and verify the result.
```

### Bring your setup to Codex

New migration flows can import supported setup from other coding agents during
onboarding. The Codex app also added `/init` for creating project instructions,
plus improved plugin management, browser diagnostics, and completed-chat
summaries.

<a id="set-up-codex-tasks-from-ios"></a>

### Set up Codex chats from iOS

Remote on iOS can now choose a branch, create a worktree, run an environment
setup script, manage goals, and add inline review comments.

Read the [June 9 app](https://learn.chatgpt.com/docs/changelog#codex-2026-06-09-app),
[June 9 iOS](https://learn.chatgpt.com/docs/changelog#codex-2026-06-09-mobile), and
[June 11 app](https://learn.chatgpt.com/docs/changelog#codex-2026-06-11-app) release notes.

## June 1–5, 2026

### Build and deploy websites with Sites

[Sites](https://learn.chatgpt.com/docs/sites) lets ChatGPT create, save, deploy, and inspect websites,
dashboards, internal tools, web apps, and games hosted by OpenAI. Sites has a
dedicated entry point in ChatGPT on the web and desktop, where you can return to
projects and manage hosted environment values and secrets without assembling a
separate deployment stack.



**Prompt:**

```text
Build a responsive launch dashboard from this project with Sites. Validate it at mobile and desktop sizes, then save a version for review. Do not deploy it until I approve the saved version.
```

### Use Codex with Amazon Bedrock

You can [use Codex with Amazon Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock) for local
workflows with AWS-managed authentication, account controls, and billing.
Remote on iOS also added an optional in-app lock, follow-up behavior settings,
line wrapping for diffs, and SSH connections to Windows machines. The desktop
app added terminal placement controls and activity insights in the profile
view.

[Read all June 2026 release notes](https://learn.chatgpt.com/docs/changelog#month-2026-06).

## May 25–29, 2026

### Use Windows apps and control Codex remotely

[Computer use](https://learn.chatgpt.com/docs/computer-use#windows-foreground-use) added support for
seeing, clicking, and typing in Windows desktop apps. Install the Computer Use
plugin before starting. On Windows, Codex uses the active desktop and takes
over the foreground while the task runs. Remote connections also support
Windows. In the ChatGPT mobile app, open **Remote** to start work on a Windows
device, or use a Mac running the ChatGPT desktop app and check progress from
elsewhere.



**Prompt:**

```text
Use @Computer to open the Windows app, reproduce the export failure, save a diagnostic file, and summarize the exact steps that trigger the problem.
```

Remote on iOS also added Spotlight and Shortcuts entry points, archived-chat
browsing, `/side`, and options to save or copy rendered images. The desktop app
added chat coordination for local projects and worktrees, content and
branch-name search for past chats, and consistent visual identifiers for
background subagents.

Read the [May 25 iOS](https://learn.chatgpt.com/docs/changelog#codex-2026-05-25-mobile) and
[May 29 app](https://learn.chatgpt.com/docs/changelog#codex-2026-05-28-app) release notes.

## May 18–22, 2026

### Give Codex context from any Mac app with Appshots

[Appshots](https://learn.chatgpt.com/docs/appshots) send the frontmost app window to Codex with a
screenshot and available text when you press both Command keys. Codex gets
working context from design tools, dashboards, documents, and other apps
without requiring you to copy, paste, or describe what's on screen.



**Prompt:**

```text
Use this appshot as the visual reference. Match the selected screen in the app, then open a preview and compare spacing, typography, and color.
```

### Follow long-running goals

[Goal mode](https://learn.chatgpt.com/docs/prompting#goal-mode) left experimental status and is
available in the Codex app, IDE extension, and CLI for objectives that can take
hours or days. [Locked use](https://learn.chatgpt.com/docs/computer-use#locked-use) lets Codex
continue approved computer-use work after a Mac locks, including through
**Remote** in the ChatGPT mobile app. ChatGPT Business workspaces can also
[share reusable plugin bundles with workspace members](https://developers.openai.com/plugins/build/plugins#share-a-local-plugin-with-your-workspace).

[Read the May 21 launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-05-21).

## May 11–15, 2026

### Continue desktop work from mobile

In the ChatGPT mobile app, **Remote** connects to a Mac running the ChatGPT
desktop app. Because work runs on the connected host, your projects, files,
credentials, plugins, skills, and configuration remain available when you
continue from your phone. See [Remote connections](https://learn.chatgpt.com/docs/remote-connections)
to set up a host and pick up work from another device.

### Automate trusted workflows

Hooks reached general availability for running custom commands at key points in
the agent lifecycle. ChatGPT Enterprise admins can also enable
[Codex access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens) for trusted scripts,
schedulers, and private CI runners. Enterprise guidance expanded to cover
managed setup and controls for Codex.

[Read the May 14 launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-05-13-app).

## May 4–8, 2026

### Work across browser tabs with the Chrome extension

The [Chrome extension](https://learn.chatgpt.com/docs/chrome-extension) can work in
parallel across tabs in the background without taking over your browser. You
control which websites Codex can use, making it practical to combine research,
data entry, and verification across web apps in one task.



**Prompt:**

```text
Compare the open product pages, collect the plan limits in a table, cite each source tab, and flag any differences that need a manual check.
```

The Codex app also added dictation cleanup and a custom dictionary for names,
file paths, and code symbols. ChatGPT Enterprise workspace owners can allow
members to create [Codex access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens) for
trusted, non-interactive local workflows.

Read the [May 5 app](https://learn.chatgpt.com/docs/changelog#codex-2026-05-05-app),
[May 5 access-token](https://learn.chatgpt.com/docs/changelog#codex-2026-05-05), and
[Codex for Chrome](https://learn.chatgpt.com/docs/changelog#codex-2026-05-07) launch notes.

## April 20–24, 2026

### Use GPT-5.5 for complex work

[GPT-5.5](https://learn.chatgpt.com/docs/models) arrived in Codex as the recommended model for most
tasks, with strengths across implementation, debugging, testing, computer use,
research, and finished knowledge-work outputs.

### Let Codex operate the browser and review approvals

[Computer Use in the built-in browser](https://learn.chatgpt.com/docs/browser?surface=app#app-computer-use-in-the-browser)
lets Codex click through local development servers and file-backed pages to
reproduce issues and verify fixes. Eligible approval requests can also go
through [automatic approval review](https://learn.chatgpt.com/docs/sandboxing/auto-review),
which shows the review status and risk before the action runs.



**Prompt:**

```text
Use @Browser to open the local app, reproduce the checkout failure, fix it, and verify the flow end to end.
```

[Read the April 23 launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-04-23).

## April 13–17, 2026

### Preview and operate work in one place

The [built-in browser](https://learn.chatgpt.com/docs/browser?surface=app) added live previews and page
comments, while [Computer Use](https://learn.chatgpt.com/docs/computer-use) let Codex see and
operate macOS apps. Together, they made visual implementation and end-to-end
verification part of the same task as the code change.

<CodexScreenshot
  alt="ChatGPT desktop app with a local web page open in the built-in browser"
  lightSrc="/images/codex/app/in-app-browser-light.webp"
  darkSrc="/images/codex/app/in-app-browser-dark.webp"
  maxHeight="420px"
  variant="no-wallpaper"
/>

<a id="start-with-a-task-and-keep-it-moving"></a>

### Start with a chat and keep it moving

[Standalone chats](https://learn.chatgpt.com/docs/projects#start-without-a-project) made it
possible to begin without choosing a project folder. The same release added
[scheduled tasks inside a chat](https://learn.chatgpt.com/docs/automations#schedule-a-task-inside-a-chat),
pull-request context, richer file previews, and [Memories](https://learn.chatgpt.com/docs/customization/memories) for
work that spans chats.

[Read the April 16 Codex app release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-04-16-app).

## April 6–10, 2026

### Review and ship pull requests in the app

The review experience added collapsible inline comments, inline and detached
review modes, and clearer Git and source context. Pull-request activity,
comments, and push choices then moved into the app alongside workspace file
tabs, so you could inspect a change and respond without switching tools.

Read the [April 9](https://learn.chatgpt.com/docs/changelog#codex-2026-04-09-app) and
[April 10](https://learn.chatgpt.com/docs/changelog#codex-2026-04-10-app) Codex app release notes, or
learn how to [review changes in the app](https://learn.chatgpt.com/docs/code-review?surface=app).

## March 23–27, 2026

### Package workflows as plugins

[Plugins](https://learn.chatgpt.com/docs/plugins) launched as installable bundles of skills,
connectors, and MCP servers. They made complete workflows easier to discover,
install, and share, while redesigned plugin and skill pages made their contents
and status clearer. Search for past chats also arrived that week.

Read the [task search](https://learn.chatgpt.com/docs/changelog#codex-2026-03-24-app),
[plugins launch](https://learn.chatgpt.com/docs/changelog#codex-2026-03-25), and
[Codex app](https://learn.chatgpt.com/docs/changelog#codex-2026-03-25-app) release notes.

## March 16–20, 2026

### Branch earlier and choose tools from the composer

You could fork a chat from an earlier message, making it easier to try a new
approach without losing the original path. Model and reasoning commands became
available while drafting, enabled skills appeared in the `@` menu, and GPT-5.4
mini added a faster option for lighter tasks and subagents.

Read the [GPT-5.4 mini](https://learn.chatgpt.com/docs/changelog#codex-2026-03-17),
[chat control](https://learn.chatgpt.com/docs/changelog#codex-2026-03-18-app), and
[skill menu](https://learn.chatgpt.com/docs/changelog#codex-2026-03-19-app) release notes.

## March 9–13, 2026

### Schedule work with the right environment

[Scheduled tasks](https://learn.chatgpt.com/docs/automations) could run locally or in a worktree
with an explicit model and reasoning level. Reusable templates made common
tasks faster to configure, and custom themes made the workspace easier to
personalize.

<CodexScreenshot
  alt="Scheduled task settings in the ChatGPT desktop app"
  lightSrc="/images/codex/app/codex-automations-light.webp"
  darkSrc="/images/codex/app/codex-automations-dark.webp"
  maxHeight="420px"
  variant="no-wallpaper"
/>

### Let Codex inspect terminal output

Codex also learned to read the [integrated terminal](https://learn.chatgpt.com/docs/integrated-terminal#run-and-validate-your-project)
for the current chat. It could inspect a running development server or build
output directly instead of asking you to paste it.



**Prompt:**

```text
Every weekday, inspect changes from the last 24 hours, find one likely regression, fix it in a worktree, run the smallest relevant tests, and report the evidence.
```

Read the [March 11](https://learn.chatgpt.com/docs/changelog#codex-2026-03-11-app) and
[March 12](https://learn.chatgpt.com/docs/changelog#codex-2026-03-12-app) Codex app release notes.

## March 2–6, 2026

### Run Codex natively on Windows

The Codex app launched on [Windows](https://learn.chatgpt.com/docs/windows/windows-app) with native PowerShell
and sandbox support, plus worktrees, scheduled tasks, and skills. WSL remained
available for developers who preferred a Linux environment.

<CodexScreenshot
  alt="Codex app running natively on Windows"
  lightSrc="/images/codex/windows/codex-windows-light.webp"
  darkSrc="/images/codex/windows/codex-windows-dark.webp"
  maxHeight="420px"
  variant="no-wallpaper"
/>

<a id="move-tasks-between-local-and-worktree"></a>

### Move chats between Local and Worktree

[Local and Worktree handoff](https://learn.chatgpt.com/docs/environments/git-worktrees#working-between-local-and-worktree)
made it possible to move an active chat while preserving its context. GPT-5.4
also arrived in Codex that week for coding, computer use, and longer-context
workflows.

Read the [Windows launch](https://learn.chatgpt.com/docs/changelog#codex-2026-03-04-app),
[worktree handoff](https://learn.chatgpt.com/docs/changelog#codex-2026-03-03-app), and
[GPT-5.4](https://learn.chatgpt.com/docs/changelog#codex-2026-03-05) release notes.

## February 9–13, 2026

### Iterate in real time and branch an approach

GPT-5.3-Codex-Spark entered research preview as a near-instant model for
real-time coding iteration. The app also added chat forking and a
floating, always-on-top chat window, so you could explore another approach or
keep Codex beside an editor or browser.

Read the [Spark](https://learn.chatgpt.com/docs/changelog#codex-2026-02-12) and
[Codex app](https://learn.chatgpt.com/docs/changelog#codex-2026-02-12-app) release notes, or see the
current [model guide](https://learn.chatgpt.com/docs/models).

## February 2–6, 2026

### The Codex app launches on macOS

The Codex app launched as a desktop workspace for parallel project chats,
built-in Git review, worktrees, skills, scheduled tasks, and voice dictation.
Those capabilities now live in Codex in the [ChatGPT desktop app](https://learn.chatgpt.com/docs/app).

<CodexScreenshot
  alt="The original Codex app showing parallel project chats on macOS"
  lightSrc="/images/codex/app/codex-app-basic-light.webp"
  darkSrc="/images/codex/app/codex-app-basic-dark.webp"
  maxHeight="420px"
  variant="no-wallpaper"
/>

### Steer active work and add files

Mid-turn steering made it possible to redirect Codex without stopping an
active response, and file attachments expanded beyond images. These patterns
became the foundation for [steering and queuing](https://learn.chatgpt.com/docs/prompting#steering-and-queuing)
follow-ups with the context Codex needs.

Read the [Codex app launch notes](https://learn.chatgpt.com/docs/changelog#codex-2026-02-02) and
[February 5 app release notes](https://learn.chatgpt.com/docs/changelog#codex-2026-02-05-app).