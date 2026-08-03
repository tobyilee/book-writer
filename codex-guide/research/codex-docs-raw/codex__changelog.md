ChatGPT & Codex changelog
 Latest updates to ChatGPT and Codex
 All updates General ChatGPT desktop app Remote Codex CLI 
 July 2026 June 2026 May 2026 April 2026 March 2026 February 2026 January 2026 December 2025 November 2025 October 2025 September 2025 August 2025 June 2025 May 2025 
 July 2026 
 li+li]:mt-12"> 2026-07-31 
 GPT-5.4 and GPT-5.4 mini retire from Codex on August 31 
 On August 31, 2026, GPT-5.4 and GPT-5.4 mini will no longer be available in
Codex for users signed in with ChatGPT. GPT-5.4 and GPT-5.4 mini will remain
available on the OpenAI API and Codex sessions authenticated with an API key.
 Switch to their recommended replacements:
 Replace gpt-5.4 with gpt-5.6-terra (GPT-5.6 Terra).
 Replace gpt-5.4-mini with gpt-5.6-luna (GPT-5.6 Luna).
 Before the cutoff, update workspace defaults, saved model settings, managed
configurations, custom agents, and scheduled tasks that use either model.
 See Codex models and
 workspace model availability 
for details.
 2026-07-30 
 Browser upgrades, multi-repository review, and image editing 26.727 
 The latest ChatGPT desktop app update makes browsing, reviewing code, and
editing generated images faster and easier.
 Browse and find context faster
 Type in the built-in browser’s address bar to revisit pages from your
browsing history or search Google when there’s no match.
 Manage your browsing history in Settings, and let ChatGPT search that
history when a task needs to find a page you visited before.
 Use the Chrome extension to mention open tabs or bring highlighted page
text into your side chat.
 Ask questions about any YouTube video in the Chrome extension and get
answers in seconds.
 Right-click a webpage and select Ask ChatGPT .
 Learn more about the built-in browser and the
 Chrome extension .
 Review changes across repositories
 See all repositories in a multi-folder project 
and the lines changed in each one. Select Review to inspect diffs across
those repositories without switching between separate review views.
 Refine generated images
 Open generated images in an expanded viewer, and switch between Focused view 
and Canvas view . Add comments across images, choose the ones you want, and
send targeted edits without leaving your conversation. Learn more about
 image generation .
 Other improvements and bug fixes
 Added a new “Activity view” in the sidebar to view which chats you engaged with recently and require attention. Click the bell or use Cmd / Ctrl + Opt + U to change to the new view.
 Updated browser settings to show only supported browsers.
 Improved Windows installation reliability when package file paths are long.
 Other performance and bug fixes.
 2026-07-29 
 Sign in with ChatGPT (beta) 
 Sign in with ChatGPT is beginning to roll out in beta across select plugins and
partner sites, starting with Airtable, GitLab, HubSpot, Notion, Supabase, and
Vercel.
 When you connect a supported plugin from the ChatGPT plugin directory, you can
use Sign in with ChatGPT to create or link an account with that service in fewer
steps. On participating partner sites, you can also select Sign in with
ChatGPT to create or access your account.
 This makes it easier to start working with supported tools in ChatGPT and Codex.
 When you sign in, the partner receives only your name, email address, and profile
picture, if available. You must still review and approve each plugin’s requested
access as a separate step.
 2026-07-27 
 ChatGPT for iOS 1.2026.202 
 Improvements and bug fixes
 Voice conversations now use your selected ChatGPT voice and show usage-limit warnings.
 Improved task reconnection and continuity when returning to the app or unlocking with Face ID.
 Composer autocomplete now matches desktop plugin mentions and includes skills from installed plugins.
 Selected-text references remain available after sending so you can preview them again.
 Improved goal controls with clearer progress when pausing or resuming.
 Inline visualizations now render tables and visual themes more reliably.
 Large workspace diffs are more responsive.
 Fixed restored tasks changing the selected model.
 Prevented the composer from becoming stuck after a prompt started.
 Corrected browser and computer tool labels, icons, and placeholder output.
 2026-07-23 
 ChatGPT Voice and multi-folder projects 26.715 
 Powered by GPT-Live, ChatGPT Voice lets you talk through work and coordinate
tasks in Chat, Work, and Codex in the ChatGPT desktop app.
 Start a new chat or task in voice mode, then ask ChatGPT to start, check, or
steer work in other threads. On macOS, turn on Screen context to share an
 appshot of your frontmost window.
 Voice is available with Plus, Pro, Business, Edu, and Enterprise plans in the
desktop app and through Remote on iOS .
 Local projects in the ChatGPT desktop app can now include multiple related
folders. From a project’s menu, select Edit project to add folders and choose
the primary folder. New chats, Git operations, and automatic discovery of
 AGENTS.md , skills, and config.toml use the primary folder. Secondary
folders remain available for file search, reading, and editing.
 Get started with ChatGPT Voice and multi-folder local
projects .
 2026-07-20 
 ChatGPT for iOS 1.2026.195 
 New features
 Added support for rendering Mermaid diagrams inline in task transcripts.
 Added support for interactive forms in Codex tasks.
 Added support for restoring unsent prompts when switching between tasks,
hosts, and workspaces.
 Improvements and bug fixes
 Improved task lists to sort by recent activity and show unavailable hosts when
creating a task.
 Improved the composer with selected-text previews and smoother new-task
transitions.
 Improved goals with support for resuming blocked or usage-limited runs.
 Improved plan progress, Fast controls, and inline dictation.
 Improved Remote onboarding, composer guidance, and iPad navigation.
 Fixed an issue that could close the app when duplicate task-list entries
appeared while starting a task.
 Fixed iOS 18 task actions and task-list styling.
 Fixed composer spacing, attachment menu padding, and duplicate transcription
indicators.
 2026-07-13 
 ChatGPT for iOS 1.2026.188 
 New features
 Added support for inline visualizations in Codex tasks.
 Improvements and bug fixes
 Improved creating and managing tasks from conversations, with reliable links
to newly created tasks.
 Improved tool activity styling and progress indicators.
 Improved file-opening feedback.
 Improved the composer so controls remain visible above the keyboard for long
prompts and larger text sizes.
 Fixed Fast mode selection and restoration for each task.
 Fixed initial prompts ignoring the selected approval preset.
 Fixed autocomplete backgrounds and task rows becoming unresponsive during
swipe gestures.
 2026-07-09 
 Codex joins the ChatGPT desktop app 26.707 
 Codex is now part of the ChatGPT desktop app on macOS and Windows. Existing
Codex app users can update as usual and keep their projects, settings, and
workflows. You can make Codex the default view and, on macOS, keep the Codex
app icon.
 New features
 Edit Markdown and code directly in the app, use inline annotations, and ask
Codex to revise selected content.
 Use PR Chat to review GitHub pull requests and ask Codex about changes in
context. Send inline review feedback, inspect proposed patches, and edit,
accept, or reject them without leaving the app.
 Connect custom domains to published Sites.
 Performance improvements and bug fixes
 Made Computer Use faster with GPT-5.6.
 Made task and subagent activity easier to follow while Codex works.
 Simplified plugin management by moving it into Settings.
 Improved permission handling when resuming tasks or sending follow-ups.
 Added clearer Full access warnings and a dialog when combining Full access with Ultra.
 Improved macOS and Windows setup, including macOS installation, Git-backed
workflows, and Computer Use on Windows.
 Fixed task resumption for local projects and onboarding retry loops.
 Fixed scrolling in pull request reviews and expanded Mermaid diagram labels.
 Improved mobile connection reliability and fixed video rendering for SSH
projects.
 Additional performance improvements and bug fixes.
 2026-07-06 
 ChatGPT for iOS 1.2026.181 
 New features
 Added support for creating, searching, opening, forking, and managing Codex
tasks directly from a conversation.
 Added filters for staged, unstaged, branch, and last-turn changes, with controls
for comparing branches.
 Added support for adding selected transcript text directly to the composer.
 Added previews for image and file attachments before sending.
 Added inline Photos and Camera pickers to the attachment menu.
 Added a connection shortcut and support for SSH hosts using private keys or no
credentials.
 Added usage limits and credit details to the task menu.
 Improvements and bug fixes
 Improved the task list with consistent task terminology, clearer delegated
task titles, and a Needs input status.
 Improved initial task loading and foreground recovery.
 Improved autocomplete by selecting the first result automatically and
accepting it with Return.
 Improved model, reasoning, and Fast settings so changes remain scoped to the
current task.
 Improved task-management and dynamic tool activity presentation.
 Improved side chats to open directly when only one conversation is available.
 Improved plugin autocomplete with installed plugins and their icons.
 Improved workspace diff accuracy and expand-and-collapse navigation.
 Improved recovery by preserving thread state across reconnects and host
pairings across sign-out.
 Fixed stuck thread-list loading, prompt mode deadlocks, stale images, and
microphone permission alerts.
 Fixed shake to undo and keyboard refocusing after sending a prompt.
 June 2026 
 li+li]:mt-12"> 2026-06-25 
 Codex Remote reaches general availability 
 Codex Remote has reached general availability. Use Codex from the ChatGPT mobile
app to start or continue work on a connected Mac or Windows host, review
progress, and approve actions from your phone.
 Remote Control now uses authenticated one-to-one QR pairing between each iOS or
Android device and each host. Update the ChatGPT mobile app and Codex App to the
latest versions before connecting. Connections used since June 8, 2026, remain
paired; older inactive connections need to pair again.
 The new DigitalOcean plugin 
lets Codex provision a DigitalOcean Droplet, configure SSH access, and connect
it to the Codex App as a remote workspace.
 See Remote connections for setup and
troubleshooting.
 2026-06-22 
 ChatGPT for iOS 1.2026.167 
 New features
 Added per-host personality settings with Friendly and Pragmatic options.
 Added support for editing goals directly in the composer.
 Added a link from forked conversations back to the original thread.
 Improvements and bug fixes
 Improved side chat visibility with separate conversations above the composer.
 Improved composer autocomplete for commands, skills, and plugins from any
prefix.
 Improved progress visibility for subagents, tasks, and worktree creation.
 Fixed long threads loading.
 Improved workspace file search, code review drafts, steering, and host setup
and recovery.
 Fixed Face ID unlocking, stopping responses, collapsed sections, and dark-mode
host indicators.
 2026-06-18 
 Record & Replay and remote task handoff 26.616 
 New features
 Added Record & Replay , a macOS feature that turns
a demonstrated workflow into a reusable skill. Initial availability excludes
the European Economic Area, the United Kingdom, and Switzerland. You or your
administrator must also enable Computer Use.
 Added bulk actions to automation run history so you
can mark every run as read or archive eligible runs.
 Added thread handoff between local and remote hosts ,
so you can move a thread to a matching project on a connected host and
continue it there. Codex can also coordinate the handoff for you.
 Performance improvements and bug fixes
 Added new deep links to manage SSH connections.
 Improved Browser Use so visible-tab routing and annotations persist when a
draft browser session moves to the server.
 Additional performance improvements and bug fixes.
 2026-06-16 
 More Codex features in the EEA, UK, and Switzerland 
 More Codex app capabilities are rolling out to users in the European Economic
Area, the United Kingdom, and Switzerland:
 Computer Use is available on macOS and Windows in
these regions, so Codex can operate desktop apps by seeing, clicking, and
typing.
 The Codex Chrome extension is available for
browser tasks that need signed-in Chrome context, working across tabs in the
background without taking over your browser.
 Memories can remember useful preferences, recurring
workflows, tech stacks, and repository conventions when enabled. Memories are
off by default in the European Economic Area, the United Kingdom, and
Switzerland.
 Chronicle is available as an opt-in research
preview for ChatGPT Pro subscribers on macOS, helping Codex build memories
from recent screen context.
 2026-06-15 
 ChatGPT for iOS 1.2026.160 
 New features
 Added a workspace file browser for previewing files and linking workspace paths
into prompts.
 Added a directory picker for choosing a workspace folder when starting a new
thread.
 Added controls to expand or collapse all diffs while reviewing changed files.
 Added MCP approval choices for allowing requested actions in the current chat
or across chats.
 Added LaTeX rendering in Codex messages and plans.
 Improvements and bug fixes
 Improved status indicators for running threads, queued prompts, side chats,
and subagents.
 Improved pairing and onboarding with clearer errors, manual pairing-code
support, and more reliable host selection after pairing.
 Improved task-list recovery, reconnect state, host-specific refresh, and
thread performance.
 Improved Codex profile sharing, activity history, and settings layout.
 Improved goal workflows with a composer shortcut, desktop-aligned goal message
actions, and better resumed question handling.
 Improved assistant message actions, transcript layout, and public rate-limit
names.
 Fixed stuck thread-list swipe actions, duplicate messages when reopening a new
thread, spawned subagents appearing as top-level task rows, and misleading
connection errors when sending prompts.
 2026-06-11 
 Usage resets and Browser Developer mode 26.609 
 New features
 Added rate-limit reset banking for Plus and Pro users, including one free
reset at launch and
 referral invitations for
earning more during the current promotion. Eligible Business members can
invite coworkers to earn shared workspace credits through a separate
referral program.
 Added Developer mode for Browser use in
Chrome and the Codex in-app browser. It gives Codex controlled Chrome
DevTools Protocol (CDP) access for performance profiling and deeper debugging
of network traffic, console output, runtime errors, and page state.
 Added the /init command to the app composer for creating project
instructions with the same initialization workflow as the Codex CLI.
 Added customizable macOS Dock icons with light and dark Codex variants.
 Added Computer Use for Enterprise users outside the European Economic Area,
the United Kingdom, and Switzerland.
 Added support for configuring per-app access controls for Computer Use on
Windows.
 Added an Unread chats section to the command menu, with the most recently
updated unread chat selected by default.
 Performance improvements and bug fixes
 Made Browser use up to 2x faster through CDP and DOM snapshot optimizations
that reduce browser round trips.
 Made command, browser, integration, and source activity summaries easier to
understand, and improved how completed chats present files, automations, and
other durable output.
 Improved plugin management by including workspace plugins, refreshing plugin
state more reliably after installation or removal, and letting you upload a
new version of an already-shared plugin without changing its access.
 Improved usage-limit errors with inline plan and workspace guidance,
including reset timing when available.
 Added Cmd + Enter and Ctrl + Enter as
shortcuts for submitting custom approval feedback.
 Fixed Browser use download handling and improved Developer mode recovery and
diagnostics.
 Fixed scheduled automations so they honor the selected approval mode, and
fixed manual project ordering, Browser tab dragging, MCP app sizing after
right-pane transitions, and clickable ChatGPT thread mentions.
 Fixed issues affecting background agent tab restoration, commit and pull
request message generation, sidebar pull request status updates, Codex Mobile
QR pairing, remote-control MFA, remote SSH installation and connection,
updater prompts, and overlay positioning at non-default zoom levels.
 Additional performance improvements and bug fixes.
 2026-06-09 
 Codex app 26.608 
 New features
 Added Import to Codex flows for importing supported setup
from Claude Code and Claude Cowork, including during onboarding.
 Revamped plugins screen with separate tabs, marketplace and
category filters, keyboard navigation, and clearer install actions.
 Expanded Settings search to find options from more panels, including Git and
pets.
 Performance improvements and bug fixes
 Fixed goal timer overlap in narrow layouts.
 Reduced unread notifications while an active goal continues running.
 Kept review diff ordering consistent with the file tree.
 Improved window rendering on systems that don’t support translucent
backdrops, including Windows 10.
 Additional performance improvements and bug fixes.
 2026-06-09 
 ChatGPT for iOS 1.2026.153 
 New features
 Added support for choosing a branch, creating a worktree, and running an
environment setup script for new threads.
 Added a Codex profile screen with usage stats and token activity charts.
 Added /goal support for creating and managing goals from Codex Mobile.
 Added inline review comments when viewing changed files.
 Added support for asking in side chat from selected transcript text.
 Added support for editing the latest sent prompt.
 Improvements and bug fixes
 Improved attachment support on Windows hosts.
 Skills and plugins now appear directly inline in the composer.
 Improved side chat and queued prompt visibility while a thread is running.
 Improved message styling, navigation, tool activity, Face ID behavior,
archived-thread browsing, and thread UI polish.
 2026-06-04 
 Codex app updates 26.602 
 New features
 Added activity insights and share cards to the
 Profile section . You can review Codex usage
highlights and save a profile card; sharing is available on consumer ChatGPT
plans.
 Performance improvements and bug fixes
 Improved Computer Use startup readiness and appshot error reporting.
 Fixed browser and review UI issues, including fullscreen browser composer
controls, hex color swatches, terminal scrollbar alignment, and animated diff
stat alignment.
 Expanded onboarding with more role choices so Codex can tailor first-run
suggestions more accurately.
 Fixed configuration writes after plugin installation.
 Additional performance improvements and bug fixes.
 2026-06-02 
 Build and deploy websites with Sites 
 Sites is now available in preview in the Codex app. Use the
Sites plugin to create, save, deploy, and inspect websites, dashboards, internal
tools, web apps, and games hosted by OpenAI.
 Open Sites in the app sidebar to return to your projects and manage hosted
environment variables and secrets.
 ChatGPT Business workspaces include Sites by default. ChatGPT Enterprise admins
can enable Sites for the appropriate roles through role-based access control
(RBAC).
 2026-06-02 
 ChatGPT for iOS 1.2026.146 
 New features
 Added an optional Face ID or passcode lock for Codex.
 Added a new settings screen for choosing Queue or Steer as the default
follow-up behavior and toggling line wrapping for code diffs.
 Added support for connecting to Windows machines over SSH.
 Improvements and bug fixes
 Added support for /side <prompt> to start a side
conversation with an initial question.
 Improved follow-up prompts, the Codex home screen, and viewing changed files.
 Fixed issues with reconnecting, archiving threads, loading tasks, and
connecting to hosts.
 2026-06-01 
 Use Codex with Amazon Bedrock 
 Codex can now use supported OpenAI models available through Amazon Bedrock.
Configure Amazon Bedrock as your model provider to run
Codex locally with AWS-managed authentication, account controls, and billing.
 2026-06-01 
 Terminal placement controls 26.601 
 New features
 Added Default terminal location in General settings .
When the bottom panel is enabled, choose whether the terminal shortcut and
environment actions open terminal tabs in the bottom panel or the right panel.
 Performance improvements and bug fixes
 Additional performance improvements and bug fixes.
 May 2026 
 li+li]:mt-12"> 2026-05-29 
 Computer use and mobile access on Windows 26.527 
 New features
 Computer Use now works on Windows. Codex can
operate Windows desktop apps by seeing, clicking, and typing in the
foreground while it works.
 Remote control now supports Windows devices. You
can start Codex work on a Windows device from ChatGPT on iOS or Android, or
from a Mac running Codex, and check its progress remotely.
 The Profile section now shows your profile
details, usage stats, and token activity.
 Added thread coordination for local projects and worktrees, including
separate background threads when explicitly requested.
 Expanded search for past Codex app threads to include conversation content
and Git branch names.
 Added stable identicons for background subagents across the app.
 Improved keyboard shortcut settings with keypress search and a reset-all
action.
 Improved Chrome context capture for Google Docs, Sheets, and Slides tabs.
 Performance improvements and bug fixes
 Additional performance improvements and bug fixes.
 2026-05-26 
 GPT-5.3-Codex and GPT-5.2 deprecated 
 GPT-5.3-Codex and GPT-5.2 are now deprecated as user-selectable models in Codex
for users signed in with ChatGPT. API-key workflows aren’t affected.
 Use a current Codex model, such as GPT-5.5, GPT-5.4, or GPT-5.4 mini. See
 Codex models for model availability
and Codex pricing for credit rates.
 2026-05-25 
 ChatGPT for iOS 1.2026.139 
 New features
 Added Spotlight and Shortcuts support for opening Codex Mobile directly.
 Added browsing for archived Codex threads.
 Added /side for opening a side conversation.
 Added options to save or copy rendered images.
 Improvements and bug fixes
 Improved iPad keyboard shortcuts.
 Improved setup and relaunch reliability.
 Fixed issues with task progress, loading archived threads, previewing code
changes, and switching hosts.
 2026-05-21 
 Appshots, goal mode, and more 26.519 
 Appshots are now available in the Codex app on macOS. Press
both Command keys to send the frontmost app window to Codex with a screenshot
and available text, so Codex can work from context in another app without you
copying, pasting, or describing it manually.
 This launch also includes:
 Goal mode is no longer an experimental feature
and is available in the Codex app, IDE extension, and CLI. With Goal mode, you
can have Codex drive toward a specific objective for hours or even days.
 Remote computer use , so Codex can use
desktop apps after your Mac locks, including remotely via Codex Mobile. Codex
scopes locked use to active, trusted computer use turns and includes
safeguards such as short-lived authorization, covered displays, relock on
local input, and manual-unlock fallback.
 Plugin sharing 
through marketplace sources is available for ChatGPT Business. Enterprise
support is coming soon. Teams can distribute reusable plugin bundles that
include skills, MCP servers, and lifecycle hooks.
 Advanced in-app browser annotations 
let you tweak styling such as font size, colors, and spacing directly using
annotations. This gives Codex a clearer signal for changes.
 Browser-use improvements across in-app browser & Chrome:
 Codex can now download and extract all image assets from a page much more
quickly.
 Codex can now extract structured data from pages more effectively and find
information more quickly with a read-only JS sandbox.
 Chrome extension will create less clutter when using it. Codex will no longer
create tab groups when taking over existing tabs, and at the end of a task for
handoff. Instead, it uses tab icons to indicate status.
 Significantly improved reliability for browser use. We fixed bugs on Windows,
flaky availability of the plugin to non geo-blocked regions, and many other
issues impacting performance.
 2026-05-18 
 ChatGPT for iOS 1.2026.132 
 New features
 Added support for opening completed Codex tasks directly from iOS
notifications.
 Added the ability to open changed files directly while reviewing a task.
 Improvements and bug fixes
 Improved task resume, reconnection, and foreground reliability.
 Improved task progress updates, code review, and message composition.
 2026-05-14 
 Work with Codex from anywhere 
 You can now use Codex from the ChatGPT mobile app by connecting it to a Mac
running the Codex app. Codex runs from the connected host, so the same projects,
files, credentials, plugins, skills, and configuration are available from your
phone.
 See Remote connections for mobile setup, choosing
a host, what comes from the connected machine, and SSH hosts. This launch also
includes Hooks general availability,
 Codex access tokens for trusted automation,
and Enterprise admin setup guidance.
 2026-05-11 
 Expanded Auto-review documentation 
 Added a dedicated
 Auto-review page covering the
reviewer lifecycle, trigger conditions, failure behavior, and local or managed
configuration.
 Also updated the Agent approvals & security 
and Sandbox docs so they explain more clearly how
Auto-review relates to the sandbox boundary.
 2026-05-08 
 Codex app 26.506 
 New features
 Added an in-app trust review flow for hooks and kept Hooks settings reachable even before hooks are fully configured.
 Performance improvements and bug fixes
 Restored tooltip-wrapped dropdowns that could stop opening after the tooltip rewrite.
 Preserved in-progress message edits across thread switches.
 Fixed several desktop workflow regressions, including Ctrl+V paste in the Windows terminal, opening modified external links outside the in-app browser, and keeping feedback slash commands attached to the right thread.
 Improved loading and panel polish by showing model loading while a thread resumes, hiding unavailable model controls during load, and bundling summary-panel layout and hover fixes.
 Kept the Computer Use settings control visible even when uninstalled and disabled problematic extension hover panels.
 Additional performance improvements and bug fixes.
 2026-05-07 
 Codex for Chrome 
 With the new extension for Chrome, Codex is even better at working with apps
and websites in your browser. It works in parallel across tabs in the
background without taking over your browser, and you stay in control of which
websites Codex can use.
 Learn more in the Codex Chrome extension documentation .
 2026-05-06 
 Codex analytics governance docs update 
 Updated the Codex enterprise governance guide with more detailed coverage of the
Analytics dashboard charts, data export options, and enterprise Analytics API
endpoints.
 2026-05-05 
 Create Codex access tokens 
 ChatGPT Enterprise workspace owners and admins can allow permitted members to
create Codex access tokens for trusted, non-interactive Codex local workflows.
Members can use access tokens to run Codex from scripts, schedulers, and private
CI runners with their ChatGPT workspace identity.
 Learn more in Access tokens .
 2026-05-05 
 Codex app 26.429 
 New features
 Added dictation cleanup plus a configurable dictation dictionary for names, file paths, and code symbols.
 Added zoom and download controls to the image lightbox.
 Performance improvements and bug fixes
 Improved voice and dictation error messages for microphone, connection, and quota failures.
 Fixed in-app browser comment markers so they stay aligned across scrolling, zoom, and responsive layout changes.
 Made pull request creation and recovery flows more reliable by preserving newly created pull request state, classifying more app-server failures as restart-required, and stopping exhausted remote reconnect loops.
 Additional performance improvements and bug fixes.
 April 2026 
 li+li]:mt-12"> 2026-04-24 
 Codex app 26.423 
 New features
 Added a tooltip on realtime delegation messages to clarify that Codex uses the surrounding voice conversation as context.
 Performance improvements and bug fixes
 Fixed search in long review files so next and previous results reliably jump to off-screen matches.
 Kept embedded MCP app panels from restarting or losing state during fullscreen changes and thread reloads.
 Fixed several desktop regressions, including tray crashes when the local connection is missing, duplicate macOS fullscreen menu entries, and broken global dictation hotkeys on older macOS versions.
 Additional performance improvements and bug fixes.
 2026-04-23 
 GPT-5.5 and Codex app updates 
 GPT-5.5 is now available in Codex 
as OpenAI’s newest frontier model for complex coding, computer use, knowledge
work, and research workflows.
 GPT-5.5 in Codex
 GPT-5.5 is the recommended choice for most Codex tasks when it appears in your
model picker. It’s especially useful for implementation, refactors, debugging,
testing, validation, and knowledge-work artifacts.
 To switch to GPT-5.5:
 In the CLI, start a new thread with:
 codex --model gpt-5.5 
Or use /model during a session.
 In the IDE extension, choose GPT-5.5 from the model selector in the composer.
 In the Codex app, choose GPT-5.5 from the model selector in the composer.
 If you don’t see GPT-5.5 yet, update the CLI, IDE extension, or Codex app to
the latest version. During the rollout, continue using GPT-5.4 if GPT-5.5 is
not yet available.
 Browser use in the Codex app
 The Codex app can now let Codex operate the in-app browser for local
development servers and file-backed pages. Ask Codex to use the browser when it
needs to click through a rendered UI, reproduce a visual bug, or verify a local
fix inside the app.
 Browser use runs through the bundled Browser plugin. In settings, you can
manage the plugin and review allowed or blocked websites.
 Automatic approval reviews
 Codex can route eligible approval prompts through an automatic reviewer agent
before the request runs. When configured, the Codex app shows an automatic
review item with the review status and risk level, so you can see whether the
reviewer approved, denied, stopped, or timed out before deciding.
 2026-04-20 
 Codex app 26.417 
 New features
 Added local branch search and non-image file pasting in the composer.
 Added collapsible sidebar sections, tray usage-limit surfacing, and a command-palette theme switcher.
 Performance improvements and bug fixes
 Made review faster and more stable with better diff batching and preserved diff and search state.
 Fixed projectless cwd and permissions handling, default file opening, spreadsheet suggestions, and remote-control reconnect issues.
 Additional performance improvements and bug fixes.
 2026-04-16 
 Codex can now help with more of your work 26.415 
 Codex is becoming a broader workspace for getting work done with AI. This
update makes it easier to start work with less setup, verify what Codex is
building, create richer outputs, and keep momentum across longer-running tasks.
 Verify more of your work
 The Codex app now includes an early in-app browser . You
can open local or public pages that don’t require sign-in, comment directly on
the rendered page, and ask Codex to address page-level feedback.
 Computer use lets Codex operate macOS apps by seeing,
clicking, and typing, which helps with native app testing, simulator flows,
low-risk app settings, and GUI-only bugs.
 The feature isn’t available in the European Economic Area, the United Kingdom, or
Switzerland at launch.
 Start, follow, and steer work
 Chats are threads you can start
without choosing a project folder first. They’re useful for research, writing,
planning, analysis, source gathering, and tool-driven work that doesn’t begin in
a codebase.
 For work that needs a later check-in,
 thread automations can wake up
the same thread on a schedule while preserving the conversation context. Use
them to check a long-running process, watch for updates, or continue a
follow-up loop without starting from scratch.
 The task sidebar makes plans, sources,
generated artifacts, and summaries easier to follow while Codex works.
 Context-aware suggestions 
can also help you pick up relevant follow-ups when you start or return to Codex.
 Stronger for software development
 Codex now brings more of the pull request workflow into the app. You can
inspect GitHub pull requests in the
sidebar, review comments in the diff, review changed files, then ask Codex to
explain feedback, make changes, check them, and keep the review moving.
 Review richer outputs
 The artifact viewer can preview
generated files such as PDF files, spreadsheets, documents, and presentations in
the sidebar before you commit or share them. Memories ,
where available, can also carry useful context from past tasks into future
threads, including stable preferences, project conventions, and recurring work
patterns.
 Other features
 Remote connections - We’re gradually rolling out SSH remote connections in alpha
 Support for multiple terminals 
 macOS menu bar and Windows system tray support
 Multi-window support 
 Intel Mac support 
 New plugins 
 Improved thread and tool rendering
 2026-04-12 
 Codex app 26.410 
 New features
 Added command-menu file search, including Cmd+P routing into workspace file search.
 Added rich previews in the sidebar file viewer for images, PDFs, and Markdown.
 Added terminal tabs per thread, a selected-text Ask Codex overlay, and a Help menu feedback entry.
 Performance improvements and bug fixes
 Improved review diff whitespace handling and search highlighting.
 Fixed in-app browser address bar and external-open issues, plus several file viewer and side-panel bugs.
 Additional performance improvements and bug fixes.
 2026-04-10 
 Codex app 26.409 
 New features
 Added Windows Store updater support.
 Expanded pull request workflows with an activity timeline, PR-page commenting, and push choices in the push modal.
 Added workspace file tabs in the thread side panel, drag-and-drop tab reordering, run action editing, and a logout confirmation dialog.
 Performance improvements and bug fixes
 Improved pull request board performance and comment flyouts.
 Improved update and navigation resilience, and fixed projectless visibility, unread-state, and pinned-row edge cases.
 Additional performance improvements and bug fixes.
 2026-04-09 
 Codex app 26.406 
 New features
 Added collapsible inline review comments and inline or detached review modes.
 Added a Git summary and Sources section in the thread side panel.
 Added a New Quick Chat command and local video embeds in the app.
 Performance improvements and bug fixes
 Preserved thread scroll position per conversation and unread state across windows.
 Improved review refresh reliability, and fixed dictation loss, right-panel reset, and GitHub reconnect messaging.
 Additional performance improvements and bug fixes.
 2026-04-07 
 Codex model availability update 
 We’re updating model availability for users who sign in with ChatGPT. Starting
April 7, the model picker no longer shows gpt-5.2-codex ,
 gpt-5.1-codex-mini , gpt-5.1-codex-max , gpt-5.1-codex , gpt-5.1 , or
 gpt-5 . On April 14, we’ll remove those models from Codex for ChatGPT sign-in.
 Users can still choose from gpt-5.4 , gpt-5.4-mini , gpt-5.3-codex , and
 gpt-5.2 . ChatGPT Pro users can also choose gpt-5.3-codex-spark .
 To use another API-supported model in Codex, sign in with an API key or
configure a model provider.
 2026-04-01 
 Codex app 26.325, 26.331, 26.401 
 New features
 Added workspace settings to the app.
 Added “Don’t ask again” handling and polish for custom MCP approval panels.
 Added native Windows updater support, including MSIX support, plus a Windows system tray menu so Codex can stay resident after the last window closes.
 Added app and file @ mentions in the automation composer, surfaced subagent diff stats in the composer, and added artifact cards for generated file citations.
 Added a Quick Chat app-menu shortcut, a review file tree open menu, early heartbeat automation affordances in threads, and image support for remote connections.
 Performance improvements and bug fixes
 Fixed review panel scroll jumps and PR status actions while a conversation is still running.
 Fixed several multi-window issues, plus @ -mention results, duplicate project labeling, Windows runGit behavior, and revert, unstage, and stage-all actions.
 Improved remote-thread and sidebar polish, Windows update recovery, unsupported-version guidance, and overall thread search speed.
 Fixed sticky review issues such as diff hunk expansion, header overlap, archive-thread crashes, and window-zoom shell sizing.
 Additional performance improvements and bug fixes.
 March 2026 
 li+li]:mt-12"> 2026-03-25 
 Build and install plugins in Codex 
 Codex now supports plugins : installable bundles that package skills, app
integrations, and MCP server configuration for reusable workflows.
 Plugins are available in the Codex app, CLI, and IDE extensions.
 You can install curated plugins from the plugin directory, or scaffold a local
plugin with @plugin-creator and test it with workspace-scoped or home-scoped
marketplaces.
 Learn more in the plugins documentation .
 Plugin structure
 Every plugin is a folder with a required .codex-plugin/plugin.json manifest
and optional supporting files:
 my-plugin/ 
 .codex-plugin/ 
 plugin.json # Required: plugin manifest 
 skills/ # Optional: packaged skills 
 .app.json # Optional: app or connector mappings 
 .mcp.json # Optional: MCP server configuration 
 assets/ # Optional: icons, logos, screenshots 
 Install plugins per-user or per-repo
 You can install plugins for just yourself with
 ~/.agents/plugins/marketplace.json and ~/.codex/plugins/ , or for everyone
on a project with .agents/plugins/marketplace.json and a repo-local plugin
directory such as ./plugins/ .
 Curated plugins and local development
 Codex surfaces curated public plugins in the plugin directory. Codex also ships
with the built-in @plugin-creator skill to help you scaffold a plugin, add a
local marketplace entry, and test it before sharing it with teammates.
 2026-03-25 
 Codex app 26.324 
 New features
 Redesigned the skills and plugins browse and manage pages.
 Added per-window zoom and a clearer edited-files state in review.
 Added automation titles and icons in the sidebar, plus bundled Raycast themes.
 Performance improvements and bug fixes
 Kept loaded threads and projects visible during reconnects and made navigation feel faster.
 Fixed archive freezes, markdown wrapping, hotkey-window regressions, and several permissions, terminal, and worktree issues.
 Additional performance improvements and bug fixes.
 2026-03-24 
 Codex app 26.323 
 New features
 Added search for past Codex app threads, including a sidebar shortcut and keyboard shortcuts for jumping to recent threads.
 Added a one-click option to archive all local threads in a project.
 Synced key settings between the Codex app and the VS Code extension, and added a settings entry point in the extension.
 Performance improvements and bug fixes
 Additional performance improvements and bug fixes.
 2026-03-20 
 Codex app 26.320 
 New features
 Added Floating Composer v2.
 Added terminal shortcuts for jumping by word and line.
 Improved plugin discovery surfaces and file-path rendering for saved images.
 Performance improvements and bug fixes
 Fixed sidebar crashes when subagent turn items are missing.
 Fixed pop-out thread routing and preserved local paths for composer image attachments.
 Additional performance improvements and bug fixes.
 2026-03-19 
 Codex app 26.318, 26.319 
 New features
 Added skills to the @ menu so you can insert them from the composer alongside other mentions.
 Cmd/Ctrl+F now starts with your current text selection, which makes searching reviews and diffs faster, alongside broader review navigation improvements such as a refreshed file tree and percentage-based file tree resizing.
 Added a branded loading shimmer while the app starts.
 Performance improvements and bug fixes
 Improved collapsed diff summaries in review.
 Fixed slash-command focus and composer alignment issues, and polished plugin cards and step details.
 Additional performance improvements and bug fixes.
 2026-03-18 
 Codex app 26.317 
 New features
 You can now fork a conversation from an earlier message, not just the latest turn.
 Added slash commands for switching models and reasoning levels, and made slash commands work in the middle of a draft prompt.
 Added notifications for plan mode questions so it’s easier to notice when Codex needs input.
 Performance improvements and bug fixes
 Fixed thread handoff and subagent navigation issues across worktrees and the VS Code extension.
 Additional performance improvements and bug fixes.
 2026-03-17 
 Introducing GPT-5.4 mini in Codex 
 GPT-5.4 mini is now available in Codex as a fast, efficient model for lighter
coding tasks and subagents.
 It improves over GPT-5 mini across coding, reasoning, image understanding, and
tool use while running more than 2x faster. In Codex, GPT-5.4 mini uses 30% as
much of your included limits as GPT-5.4, so comparable tasks can last about
3.3x longer before you hit those limits.
 GPT-5.4 mini is available in the Codex app, the CLI, the IDE extension, and
Codex on the web. GPT-5.4 mini is also available in the API.
 Use GPT-5.4 mini for codebase exploration, large-file review, processing
supporting documents, and other less reasoning-intensive subagent work. For
more complex planning, coordination, and final judgment, start with GPT-5.4.
 To switch to GPT-5.4 mini:
 In the CLI, start a new thread with:
 codex --model gpt-5.4-mini 
Or use /model during a session.
 In the IDE extension, choose GPT-5.4 mini from the model selector in the
composer.
 In the Codex app, choose GPT-5.4 mini from the model selector in the
composer.
 If you don’t see GPT-5.4 mini yet, update the CLI, IDE extension, or Codex app
to the latest version.
 2026-03-16 
 Codex app 26.313 
 New features
 Added back and forward buttons in the header so you can move between recent screens more quickly.
 Added an Open in Finder , Open in Explorer , or Open in File Manager action from thread menus to jump straight to a thread’s project folder.
 Performance improvements and bug fixes
 Improved resume and thread error toasts with clearer details when something goes wrong.
 Additional performance improvements and bug fixes.
 2026-03-12 
 Codex app 26.312 
 Themes
 Change the Codex app appearance in Settings by choosing a base theme,
adjusting accent, background, and foreground colors, and changing the UI and
code fonts. You can also share your custom theme with friends.
 Revamped Automations
 You can now choose whether automations run locally or on a worktree, define
custom reasoning levels and models, and use templates to find inspiration for
new automations.
 Performance improvements and bug fixes
 Various bug fixes and performance improvements.
 2026-03-11 
 Codex app 26.311 
 New features
 Codex can now read the integrated terminal for the current thread, so it can check the status of a running development server or refer back to failed build output while it works with you.
 Performance improvements and bug fixes
 Additional performance improvements and bug fixes.
 2026-03-05 
 Introducing GPT-5.4 in Codex 
 GPT-5.4 is now available in Codex as OpenAI’s most capable and efficient
frontier model for professional work.
 It combines recent advances in reasoning, coding, and agentic workflows in one
model, and it’s the recommended choice for most Codex tasks.
 In Codex, GPT-5.4 is the first general-purpose model with native computer-use
capabilities. GPT-5.4 in Codex includes experimental support for the 1M
context window. It supports complex workflows across applications and
long-horizon tasks, with stronger tool use and tool search that help agents
find and use the right tools more efficiently.
 GPT-5.4 is available everywhere you can use Codex: the Codex app, the CLI, the
IDE extension, and Codex Cloud on the web. GPT-5.4 is also available in the
API.
 To switch to GPT-5.4:
 In the CLI, start a new thread with:
 codex --model gpt-5.4 
Or use /model during a session.
 In the IDE extension, choose GPT-5.4 from the model selector in the
composer.
 In the Codex app, choose GPT-5.4 from the model selector in the composer.
 If you don’t see GPT-5.4 yet, update the CLI, IDE extension, or Codex app to
the latest version.
 2026-03-05 
 Codex app 26.305 
 Performance improvements and bug fixes
 Improved remote connections with clearer connection errors, better status updates, and clearer host labels in thread and settings views.
 Fixed copy and paste shortcuts in the integrated terminal on Windows.
 Fixed an issue where archived pinned threads could reappear in the sidebar.
 Fixed an issue where repeated codex://new links could stop prefilling a new conversation when the app was already open.
 Additional performance improvements and bug fixes.
 2026-03-04 
 Codex app 26.304 
 Codex app for Windows
 The Codex app is now available on Windows. The app gives you one interface
for working across projects, running parallel agent threads, and reviewing
results in one place.
 The Codex app runs natively on Windows using PowerShell and a native Windows
sandbox for bounded permissions, so you can use Codex on Windows without
moving your workflow into WSL, onto a virtual machine, or by deactivating the
sandbox.
 The Windows app includes the same core features as the rest of the Codex app:
 Skills to discover and extend Codex
capabilities.
 Automations to run work in the background.
 Worktrees to handle independent tasks in the same
project.
 If you prefer to develop in WSL, you can also switch the Codex agent and the
integrated terminal to run there.
 Download it from the
 Microsoft Store 
and sign in with your ChatGPT account or an API key. For setup and
configuration details, see Setup , Use WSL with the
Codex app , and Customize the
app for your development setup .
 2026-03-03 
 Codex app 26.303 
 New features
 Added a Worktrees setting to turn automatic cleanup of Codex-managed worktrees on or off.
 Added Handoff support for moving a thread between Local and Worktree .
 Added an explicit English option in the language menu.
 Performance improvements and bug fixes
 Improved GitHub and pull request workflows.
 Improved approval prompts and app connection sign-in flows.
 Additional performance improvements and bug fixes.
 February 2026 
 li+li]:mt-12"> 2026-02-28 
 Codex app 26.228 
 Performance improvements and bug fixes
 Fixed a regression where conversation and task views could stop updating while Codex was streaming a response.
 Additional performance improvements and bug fixes.
 2026-02-27 
 Codex app 26.227 
 New features
 Added pull request status badges in task rows and PR buttons, including draft, open, merged, and closed states.
 Added a Worktrees setting to choose how many Codex-managed worktrees to keep before older ones are cleaned up.
 Performance improvements and bug fixes
 Improved scrolling and navigation in long conversations and code review, including fixes for thread jumpiness, sidebar jitter, and diff scrolling.
 Improved app startup reliability and keyboard zoom behavior.
 Additional performance improvements and bug fixes.
 2026-02-26 
 Codex app 26.226 
 New features
 Added new MCP shortcuts in the composer, including install keyword suggestions and an MCP server submenu in Add context .
 Added support for @mentions and skill mentions in inline review comments.
 Performance improvements and bug fixes
 Improved rendering of MCP tool calls and Mermaid diagram error handling.
 Fixed an issue where stopped terminal commands could continue appearing as running.
 Additional performance improvements and bug fixes.
 2026-02-17 
 Codex app 26.217 
 New features
 Added drag-and-drop support to reorder queued messages.
 Added a warning when the selected model is downgraded.
 Improvements and bug fixes
 Improved file workflows with fuzzy file search and better attachment recovery after restart.
 Additional performance improvements and bug fixes.
 2026-02-12 
 Introducing GPT-5.3-Codex-Spark 
 Today, we’re releasing a research preview of GPT-5.3-Codex-Spark ,
a smaller version of GPT-5.3-Codex and our first model designed for real-time
coding. Codex-Spark is optimized to feel near-instant, delivering more than 1000 tokens per second while remaining highly capable for real-world coding tasks.
 Codex-Spark is available in research preview for ChatGPT Pro users in
the latest Codex app, CLI, and IDE extension. This release also marks the first
milestone in our partnership with Cerebras.
 At launch, Codex-Spark is text-only with a 128k context window. During
the research preview, usage has separate model-specific limits and doesn’t
count against standard Codex limits. During high demand, access may slow down
or queue while we balance reliability across users.
 To switch to GPT-5.3-Codex-Spark:
 In the CLI, start a new thread with:
 codex --model gpt-5.3-codex-spark 
Or use /model during a session.
 In the IDE extension, choose GPT-5.3-Codex-Spark from the model selector in
the composer.
 In the Codex app, choose GPT-5.3-Codex-Spark from the model selector in the
composer.
 If you don’t see GPT-5.3-Codex-Spark yet, update the CLI, IDE extension, or
Codex app to the latest version.
 GPT-5.3-Codex-Spark isn’t available in the API at launch.
For API-key workflows, continue using gpt-5.2-codex .
 2026-02-12 
 Codex app 26.212 
 New features
 Support for GPT-5.3-Codex-Spark
 Added conversation forking
 Added floating pop-out window to take a conversation with you
 Bug fixes
 Improved performance and bug fixes
 Alpha testing for the Codex app on Windows is also starting. Sign up here to be a potential alpha tester.
 2026-02-10 
 Codex app 26.210 
 New features
 Added branch search in the branch picker.
 Added clearer guidance for entering plan mode when you type plan in the composer.
 Added support for parallel approvals.
 Improvements and bug fixes
 Additional performance improvements and bug fixes.
 2026-02-09 
 GPT-5.3-Codex in Cursor and VS Code 
 Starting today, GPT-5.3-Codex is available natively in Cursor and VS Code.
 API access is starting with a small set of customers as part of a phased
release.
 This is the first model treated as a high security capability under the
Preparedness Framework.
 Safety controls will continue to scale, and API access will expand over the
next few weeks.
 2026-02-08 
 Codex app 26.208 
 New features
 Added MCP and personality actions to the command palette.
 Updated follow-up behavior to queue by default.
 Improvements and bug fixes
 Additional performance improvements and bug fixes.
 2026-02-06 
 Codex app 26.206 
 New features
 Added a file-reference action to reveal files directly in your OS file manager.
 Improvements and bug fixes
 Improved handling of large reviews by removing the overall diff-size cap in the review pane.
 Additional performance improvements and bug fixes.
 2026-02-05 
 Introducing GPT-5.3-Codex 
 Today we’re releasing GPT-5.3-Codex ,
the most capable agentic coding model to date for complex, real-world software
engineering.
 GPT-5.3-Codex combines the frontier coding performance of GPT-5.2-Codex with
stronger reasoning and professional knowledge capabilities, and runs 25% faster
for Codex users. It’s also better at collaboration while the agent is
working—delivering more frequent progress updates and responding to steering in
real time.
 GPT-5.3-Codex is available with paid ChatGPT plans everywhere you can use
Codex: the Codex app, the CLI, the IDE extension, and Codex Cloud on the web.
API access for the model will come soon.
 To switch to GPT-5.3-Codex:
 In the CLI, start a new thread with:
 codex --model gpt-5.3-codex 
Or use /model during a session.
 In the IDE extension, make sure you are signed in with ChatGPT, then choose
GPT-5.3-Codex from the model selector in the composer.
 In the Codex app, make sure you are signed in with ChatGPT, then choose
GPT-5.3-Codex from the model selector in the composer.
 If you don’t see GPT-5.3-Codex, update the CLI, IDE extension, or Codex app
to the latest version.
 For API-key workflows, continue using gpt-5.2-codex while API support rolls
out.
 2026-02-05 
 Codex app 26.205 
 New features
 Support for GPT-5.3-Codex .
 Added mid-turn steering. Submit a message while Codex is working to direct its behavior.
 Attach or drop any file type.
 Bug fixes
 Fix flickering of the app.
 2026-02-04 
 Codex app 26.204 
 New features
 Added Zed and Textmate as options to open files and folders.
 Added PDF preview in the review panel.
 Bug fixes
 Performance improvements.
 2026-02-03 
 Codex app 26.203 
 New features
 Added thread renaming on double-click in the thread list.
 Improvements and bug fixes
 Renamed Sync to Handoff and added clearer source/destination stats in the handoff UI.
 Additional performance improvements and bug fixes.
 2026-02-02 
 Introducing the Codex app 
 Codex app
 The Codex app for macOS is a desktop interface for running agent threads in parallel and collaborating with agents on long-running tasks. It includes a project sidebar, thread list, and review pane for tracking work across projects.
 Key features:
 Multitask across projects 
 Built-in worktree support 
 Voice dictation 
 Built-in Git tooling 
 Skills 
 Automations 
 For a limited time, ChatGPT Free and Go include Codex , and Plus, Pro, Business, Enterprise, and Edu plans get double rate limits . Those higher limits apply in the app, the CLI, your IDE, and the cloud.
 Learn more in the Introducing the Codex app blog post.
 Check out the Codex app documentation for more.
 Get started with the Codex app 
 January 2026 
 li+li]:mt-12"> 2026-01-28 
 Web search is now enabled by default 
 Codex now enables web search for local tasks in the Codex CLI and IDE Extension.
By default, Codex uses a web search cache, which is an OpenAI-maintained index of web results. Cached mode returns pre-indexed results instead of fetching live pages, while live mode fetches the most recent data from the web. If you are using --yolo or another full access sandbox setting , web search defaults to live results. To disable this behavior or switch modes, use the web_search configuration option:
 web_search = "cached" (default; serves results from the web search cache)
 web_search = "live" (fetches the most recent data from the web; same as --search )
 web_search = "disabled" to remove the tool
 To learn more, check out the configuration documentation .
 2026-01-23 
 Team Config for shared configuration 
 Team Config groups the files teams use to standardize Codex across repositories and machines. Use it to share:
 config.toml defaults
 rules/ for command controls outside the sandbox
 skills/ for reusable workflows
 Codex loads these layers from .codex/ folders in the current working directory, parent folders, and the repo root, plus user ( ~/.codex/ ) and system ( /etc/codex/ ) locations. Higher-precedence locations override lower-precedence ones.
 Admins can still enforce constraints with requirements.toml , which overrides defaults regardless of location.
 Learn more in Team Config .
 2026-01-22 
 Custom prompts deprecated 
 Custom prompts are now deprecated. Use skills for reusable instructions and workflows instead.
 2026-01-14 
 GPT-5.2-Codex API availability 
 GPT-5.2-Codex is now available in the API and for users who sign into Codex with the API.
 To learn more about using GPT-5.2-Codex check out our API documentation .
 December 2025 
 li+li]:mt-12"> 2025-12-19 
 Agent skills in Codex 
 Codex now supports agent skills : reusable bundles of instructions (plus optional scripts and resources) that help Codex reliably complete specific tasks.
 Skills are available in both the Codex CLI and IDE extensions.
 You can invoke a skill explicitly by typing $skill-name (for example, $skill-installer or the experimental $create-plan skill after installing it), or let Codex select a skill automatically based on your prompt.
 Learn more in the skills documentation .
 Folder-based standard (agentskills.io)
 Following the open agent skills specification , a skill is a folder with a required SKILL.md and optional supporting files:
 my-skill/ 
 SKILL.md # Required: instructions + metadata 
 scripts/ # Optional: executable code 
 references/ # Optional: documentation 
 assets/ # Optional: templates, resources 
 Install skills per-user or per-repo
 You can install skills for just yourself in ~/.codex/skills , or for everyone on a project by checking them into .codex/skills in the repository.
 Codex also ships with a few built-in system skills to get started, including $skill-creator and $skill-installer . The $create-plan skill is experimental and needs to be installed (for example: $skill-installer install the create-plan skill from the .experimental folder ).
 Curated skills directory
 Codex ships with a small curated set of skills inspired by popular workflows at OpenAI. Install them with $skill-installer , and expect more over time.
 2025-12-18 
 Introducing GPT-5.2-Codex 
 Today we are releasing GPT-5.2-Codex , the most advanced agentic coding model yet for complex, real-world software engineering.
 GPT-5.2-Codex is a version of GPT-5.2 further optimized for agentic coding in Codex, including improvements on long-horizon work through context compaction, stronger performance on large code changes like refactors and migrations, improved performance in Windows environments, and significantly stronger cybersecurity capabilities.
 Starting today, the CLI and IDE Extension will default to gpt-5.2-codex for users who are signed in with ChatGPT. API access for the model will come soon.
 If you have a model specified in your config.toml configuration file , you can instead try out gpt-5.2-codex for a new Codex CLI session using:
 codex --model gpt-5.2-codex 
 You can also use the /model slash command in the CLI. In the Codex IDE Extension you can select GPT-5.2-Codex from the dropdown menu.
 If you want to switch for all sessions, you can change your default model to gpt-5.2-codex by updating your config.toml configuration file :
 model = "gpt-5.2-codex” 
 2025-12-04 
 Introducing Codex for Linear 
 Assign or mention @Codex in an issue to kick-off a Codex cloud task. As Codex works, it posts updates back to Linear, providing a link to the completed task so you can review, open a PR, or keep working.
 To learn more about how to connect Codex to Linear both locally through MCP and through the new integration, check out the Codex for Linear documentation .
 November 2025 
 li+li]:mt-12"> 2025-11-24 
 Usage and credits fixes 
 Minor updates to address a few issues with Codex usage and credits:
 Adjusted all usage dashboards to show “limits remaining” for consistency. The CLI previously displayed “limits used.”
 Fixed an issue preventing users from buying credits if their ChatGPT subscription was purchased via iOS or Google Play.
 Fixed an issue where the CLI could display stale usage information; it now refreshes without needing to send a message first.
 Optimized the backend to help smooth out usage throughout the day, irrespective of overall Codex load or how traffic is routed. Before, users could get unlucky and hit a few cache misses in a row, leading to much less usage.
 2025-11-18 
 Introducing GPT-5.1-Codex-Max 
 Today we are releasing GPT-5.1-Codex-Max , our new frontier agentic coding model.
 GPT‑5.1-Codex-Max is built on an update to our foundational reasoning model, which is trained on agentic tasks across software engineering, math, research, and more. GPT‑5.1-Codex-Max is faster, more intelligent, and more token-efficient at every stage of the development cycle–and a new step towards becoming a reliable coding partner.
 Starting today, the CLI and IDE Extension will default to gpt-5.1-codex-max for users that are signed in with ChatGPT. API access for the model will come soon.
 For non-latency-sensitive tasks, we’ve also added a new Extra High ( xhigh ) reasoning effort, which lets the model think for an even longer period of time for a better answer. We still recommend medium as your daily driver for most tasks.
 If you have a model specified in your config.toml configuration file , you can instead try out gpt-5.1-codex-max for a new Codex CLI session using:
 codex --model gpt-5.1-codex-max 
 You can also use the /model slash command in the CLI. In the Codex IDE Extension you can select GPT-5.1-Codex from the dropdown menu.
 If you want to switch for all sessions, you can change your default model to gpt-5.1-codex-max by updating your config.toml configuration file :
 model = "gpt-5.1-codex-max” 
 2025-11-13 
 Introducing GPT-5.1-Codex and GPT-5.1-Codex-Mini 
 Along with the GPT-5.1 launch in the API , we are introducing new gpt-5.1-codex-mini and gpt-5.1-codex model options in Codex, a version of GPT-5.1 optimized for long-running, agentic coding tasks and use in coding agent harnesses in Codex or Codex-like harnesses.
 Starting today, the CLI and IDE Extension will default to gpt-5.1-codex on macOS and Linux and gpt-5.1 on Windows.
 If you have a model specified in your config.toml configuration file , you can instead try out gpt-5.1-codex for a new Codex CLI session using:
 codex --model gpt-5.1-codex 
 You can also use the /model slash command in the CLI. In the Codex IDE Extension you can select GPT-5.1-Codex from the dropdown menu.
 If you want to switch for all sessions, you can change your default model to gpt-5.1-codex by updating your config.toml configuration file :
 model = "gpt-5.1-codex” 
 2025-11-07 
 Introducing GPT-5-Codex-Mini 
 Today we are introducing a new gpt-5-codex-mini model option to Codex CLI and the IDE Extension. The model is a smaller, more cost-effective, but less capable version of gpt-5-codex that provides approximately 4x more usage as part of your ChatGPT subscription.
 Starting today, the CLI and IDE Extension will automatically suggest switching to gpt-5-codex-mini when you reach 90% of your 5-hour usage limit, to help you work longer without interruptions.
 You can try the model for a new Codex CLI session using:
 codex --model gpt-5-codex-mini 
 You can also use the /model slash command in the CLI. In the Codex IDE Extension you can select GPT-5-Codex-Mini from the dropdown menu.
 Alternatively, you can change your default model to gpt-5-codex-mini by updating your config.toml configuration file :
 model = "gpt-5-codex-mini” 
 2025-11-06 
 GPT-5-Codex model update 
 We’ve shipped a minor update to GPT-5-Codex:
 More reliable file edits with apply_patch .
 Fewer destructive actions such as git reset .
 More collaborative behavior when encountering user edits in files.
 3% more efficient in time and usage.
 October 2025 
 li+li]:mt-12"> 2025-10-30 
 Credits on ChatGPT Pro and Plus 
 Codex users on ChatGPT Plus and Pro can now use on-demand credits for more Codex usage beyond what’s included in your plan. Learn more. 
 2025-10-22 
 Tag @Codex on GitHub Issues and PRs 
 You can now tag @codex on a teammate’s pull request to ask clarifying questions, request a follow-up, or ask Codex to make changes. GitHub Issues now also support @codex mentions, so you can kick off tasks from any issue, without leaving your workflow.
 2025-10-06 
 Codex is now GA 
 Codex is now generally available with 3 new features — @Codex in Slack, Codex SDK, and new admin tools.
 @Codex in Slack
 You can now questions and assign tasks to Codex directly from Slack. See the Slack guide to get started.
 Codex SDK
 Integrate the same agent that powers the Codex CLI inside your own tools and workflows with the Codex SDK in Typescript. With the new Codex GitHub Action, you can easily add Codex to CI/CD workflows. See the Codex SDK guide to get started.
 import { Codex } from "@openai/codex-sdk" ; 
 const agent = new Codex (); 
 const thread = await agent. startThread (); 
 const result = await thread. run ( "Explore this repo" ); 
 console. log (result); 
 const result2 = await thread. run ( "Propose changes" ); 
 console. log (result2); 
 New admin controls and analytics
 ChatGPT workspace admins can now edit or delete Codex Cloud environments. With managed config files, they can set safe defaults for CLI and IDE usage and monitor how Codex uses commands locally. New analytics dashboards help you track Codex usage and code review feedback. Learn more in the enterprise admin guide. 
 Availability and pricing updates
 The Slack integration and Codex SDK are available to developers on ChatGPT Plus, Pro, Business, Edu, and Enterprise plans starting today, while the new admin features will be available to Business, Edu, and Enterprise.
Beginning October 20, Codex Cloud tasks will count toward your Codex usage. Review the Codex pricing guide for plan-specific details.
 September 2025 
 li+li]:mt-12"> 2025-09-23 
 GPT-5-Codex in the API 
 GPT-5-Codex is now available in the Responses API, and you can also use it with your API Key in the Codex CLI.
We plan on regularly updating this model snapshot.
It is available at the same price as GPT-5. You can learn more about pricing and rate limits for this model on our model page .
 2025-09-15 
 Introducing GPT-5-Codex 
 New model: GPT-5-Codex
 GPT-5-Codex is a version of GPT-5 further optimized for agentic coding in Codex.
It’s available in the IDE extension and CLI when you sign in with your ChatGPT account.
It also powers the cloud agent and Code Review in GitHub.
 To learn more about GPT-5-Codex and how it performs compared to GPT-5 on software engineering tasks, see our announcement blog post .
 Image outputs
 When working in the cloud on front-end engineering tasks, GPT-5-Codex can now display screenshots of the UI in Codex web for you to review. With image output, you can iterate on the design without needing to check out the branch locally.
 New in Codex CLI
 You can now resume sessions where you left off with codex resume .
 Context compaction automatically summarizes the session as it approaches the context window limit.
 Learn more in the latest release notes 
 August 2025 
 li+li]:mt-12"> 2025-08-27 
 Late August update 
 IDE extension (Compatible with VS Code, Cursor, Windsurf)
 Codex now runs in your IDE with an interactive UI for fast local iteration. Easily switch between modes and reasoning efforts.
 Sign in with ChatGPT (IDE & CLI)
 One-click authentication that removes API keys and uses ChatGPT Enterprise credits.
 Move work between local ↔ cloud
 Hand off tasks to Codex web from the IDE with the ability to apply changes locally so you can delegate jobs without leaving your editor.
 Code Reviews
 Codex goes beyond static analysis. It checks a PR against its intent, reasons across the codebase and dependencies, and can run code to validate the behavior of changes.
 2025-08-21 
 Mid August update 
 Image inputs
 You can now attach images to your prompts in Codex web. This is great for asking Codex to implement frontend changes or follow up on whiteboarding sessions.
 Container caching
 Codex now caches containers to start new tasks and followups 90% faster, dropping the median start time from 48 seconds to 5 seconds. You can optionally configure a maintenance script to update the environment from its cached state to prepare for new tasks. See the docs for more.
 Automatic environment setup
 Now, environments without manual setup scripts automatically run the standard installation commands for common package managers like yarn, pnpm, npm, go mod, gradle, pip, poetry, uv, and cargo. This reduces test failures for new environments by 40%.
 June 2025 
 li+li]:mt-12"> 2025-06-13 
 Best of N 
 Codex can now generate multiple responses simultaneously for a single task, helping you quickly explore possible solutions to pick the best approach.
 Fixes & improvements
 li+li]:mt-1 text-default [&_p]:m-0"> Added some keyboard shortcuts and a page to explore them. Open it by pressing ⌘-/ on macOS and Ctrl+/ on other platforms.
 Added a “branch” query parameter in addition to the existing “environment”, “prompt” and “tab=archived” parameters.
 Added a loading indicator when downloading a repo during container setup.
 Added support for cancelling tasks.
 Fixed issues causing tasks to fail during setup.
 Fixed issues running followups in environments where the setup script changes files that are gitignored.
 Improved how the agent understands and reacts to network access restrictions.
 Increased the update rate of text describing what Codex is doing.
 Increased the limit for setup script duration to 20 minutes for Pro and Business users.
 Polished code diffs: You can now option-click a code diff header to expand/collapse all of them.
 2025-06-03 
 June update 
 Agent internet access
 Now you can give Codex access to the internet during task execution to install dependencies, upgrade packages, run tests that need external resources, and more.
 Internet access is off by default. Plus, Pro, and Business users can enable it for specific environments, with granular control of which domains and HTTP methods Codex can access. Internet access for Enterprise users is coming soon.
 Learn more about usage and risks in the docs .
 Update existing PRs
 Now you can update existing pull requests when following up on a task.
 Voice dictation
 Now you can dictate tasks to Codex.
 Fixes & improvements
 li+li]:mt-1 text-default [&_p]:m-0"> Added a link to this changelog from the profile menu.
 Added support for binary files: When applying patches, all file operations are supported. When using PRs, only deleting or renaming binary files is supported for now.
 Fixed an issue on iOS where follow up tasks where shown duplicated in the task list.
 Fixed an issue on iOS where pull request statuses were out of date.
 Fixed an issue with follow ups where the environments were incorrectly started with the state from the first turn, rather than the most recent state.
 Fixed internationalization of task events and logs.
 Improved error messages for setup scripts.
 Increased the limit on task diffs from 1 MB to 5 MB.
 Increased the limit for setup script duration from 5 to 10 minutes.
 Polished GitHub connection flow.
 Re-enabled Live Activities on iOS after resolving an issue with missed notifications.
 Removed the mandatory two-factor authentication requirement for users using SSO or social logins.
 May 2025 
 li+li]:mt-12"> 2025-05-22 
 Reworked environment page 
 It’s now easier and faster to set up code execution.
 Fixes & improvements
 li+li]:mt-1 text-default [&_p]:m-0"> Added a button to retry failed tasks
 Added indicators to show that the agent runs without network access after setup
 Added options to copy git patches after pushing a PR
 Added support for unicode branch names
 Fixed a bug where secrets were not piped to the setup script
 Fixed creating branches when there’s a branch name conflict.
 Fixed rendering diffs with multi-character emojis.
 Improved error messages when starting tasks, running setup scripts, pushing PRs, or disconnected from GitHub to be more specific and indicate how to resolve the error.
 Improved onboarding for teams.
 Polished how new tasks look while loading.
 Polished the followup composer.
 Reduced GitHub disconnects by 90%.
 Reduced PR creation latency by 35%.
 Reduced tool call latency by 50%.
 Reduced task completion latency by 20%.
 Started setting page titles to task names so Codex tabs are easier to tell apart.
 Tweaked the system prompt so that agent knows it’s working without network, and can suggest that the user set up dependencies.
 Updated the docs.
 2025-05-19 
 Codex in the ChatGPT iOS app 
 Start tasks, view diffs, and push PRs—while you’re away from your desk.