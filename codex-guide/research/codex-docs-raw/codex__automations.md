# Scheduled tasks

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Schedule recurring tasks to run in the background. Review active, paused, and
completed tasks and recent runs in **Scheduled**. You can combine scheduled
tasks with [skills](https://learn.chatgpt.com/docs/build-skills) for more complex work.

<ContentModeSwitch group="codex-surface" id="app">

In the ChatGPT desktop app, scheduled tasks can work with local projects and
run in the project directory or an isolated worktree. Keep the computer on and
the app running when a scheduled task needs local files.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

When scheduled tasks are enabled for your workspace, create them from Chat or
ChatGPT Work on the web and manage their runs from **Scheduled**. Web tasks
can use uploaded context and connected tools, but they can't work directly in
a folder on your computer.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

Codex CLI doesn't provide the Scheduled management interface. Use ChatGPT web
or the desktop app to create and manage scheduled tasks. The CLI can help you
prepare and test a prompt, skill, or script first.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

The IDE extension doesn't provide the Scheduled management interface. Use
ChatGPT web or the desktop app to create and manage scheduled tasks. The IDE
extension can help you prepare and test a prompt, skill, or workspace change
first.

</ContentModeSwitch>

<a id="managing-tasks"></a>
<a id="ask-codex-to-create-or-update-automations"></a>
<a id="ask-chatgpt-to-create-or-update-scheduled-tasks"></a>
<a id="thread-automations"></a>
<a id="scheduled-tasks-in-threads"></a>
<a id="scheduled-tasks-in-chats"></a>
<a id="schedule-work-from-a-task"></a>
<a id="schedule-a-task-inside-a-chat"></a>
<a id="test-automations"></a>
<a id="test-scheduled-tasks"></a>
<a id="worktree-cleanup-for-automations"></a>
<a id="worktree-cleanup-for-scheduled-tasks"></a>
<a id="permissions-and-security-model"></a>
<a id="examples"></a>
<a id="automatically-create-new-skills"></a>
<a id="stay-up-to-date-with-your-project"></a>
<a id="combining-automations-with-skills-to-fix-your-own-bugs"></a>
<a id="combining-scheduled-tasks-with-skills-to-fix-your-own-bugs"></a>

<ContentModeSwitch group="codex-surface" id="web">

## Manage scheduled tasks on the web

Open **Scheduled** to review task status and recent runs. Use a standalone scheduled task
when each run should start from the saved prompt. Use a scheduled task in a
chat when you want ChatGPT to return to the same chat with its existing
context.

Scheduled tasks on the web can use uploaded files, connected tools, skills, and
plugins available to that chat. They don't keep a local folder or
worktree available between runs. Put durable instructions in the task prompt
or an attached skill, and keep required source material in an accessible
project, upload, or connected service.

Before you schedule a task, test its prompt in a regular web chat.
Review the first few runs, then adjust the prompt, tools, or cadence if the
results are too broad or need additional context.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

For example, schedule a task to evaluate telemetry errors and submit fixes,
or to create reports about recent codebase changes. For ongoing work that
should keep using the same context, [schedule a task inside an existing chat](#schedule-a-task-inside-a-chat).

For project-scoped scheduled tasks, keep the machine powered on and the ChatGPT
desktop app running. The selected project must still be available on disk when
the task is scheduled to run.

In Git repositories, you can choose whether a scheduled task runs in your local
project or on a new [worktree](https://learn.chatgpt.com/docs/environments/git-worktrees). Both options run in the
background. Worktrees keep changes from scheduled tasks separate from unfinished local
work, while running in your local project can modify files you are still
working on. In non-version-controlled projects, scheduled tasks run directly in the
project directory.

You can also leave the model and reasoning effort on their default settings, or
choose them explicitly if you want more control over how the scheduled task runs.

If a scheduled task uses `gpt-5.4` or `gpt-5.4-mini` with ChatGPT sign-in,
update it before those models retire on August 31, 2026. Replace `gpt-5.4` with
`gpt-5.6-terra` and `gpt-5.4-mini` with `gpt-5.6-luna`.

<Illustration description="ChatGPT composer ready to create a scheduled task with 5.6 Sol Extended selected.">
  <CodexScheduledTasksIllustration
    variant="manage"
    ariaLabel="ChatGPT composer ready to create a scheduled task with 5.6 Sol Extended selected."
  />
</Illustration>

Scheduled tasks run unattended with your default sandbox settings. Start with the
narrowest access that lets the task succeed, and grant network or broader file
access only when required. [Understand sandboxing](https://learn.chatgpt.com/docs/sandboxing).

## Manage scheduled tasks

Find all scheduled tasks and their runs on **Scheduled** in the ChatGPT desktop
app sidebar.

The **Scheduled** view acts as your inbox. Scheduled task runs with findings
appear there, and an unread indicator shows when a run needs your attention.

<Illustration description="Scheduled tasks page with All, Active, and Paused filters and three scheduled tasks.">
  <CodexScheduledTasksIllustration
    variant="inbox"
    ariaLabel="Scheduled tasks page with All, Active, and Paused filters and three scheduled tasks."
  />
</Illustration>

Standalone scheduled tasks start a new chat for each scheduled run and report
results in **Scheduled**. Use them when each run should be independent or when one
scheduled task should run across one or more projects. If you need a custom
cadence, use the custom schedule controls. For an advanced schedule, edit its
RFC 5545 recurrence rule (RRULE), such as
`RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0`.

For Git repositories, each scheduled task can run either in your local project or
on a dedicated background [worktree](https://learn.chatgpt.com/docs/environments/git-worktrees). Use
worktrees when you want to isolate scheduled-task changes from unfinished local
work. Use local mode when you want the scheduled task to work directly in your main
checkout, keeping in mind that it can change files you are actively editing.
In non-version-controlled projects, scheduled tasks run directly in the project
directory. You can have the same scheduled task run on more than one project.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,web">

Scheduled tasks created with ChatGPT Work on the web, or with ChatGPT Work or
Codex in the desktop app, can use plugins. Scheduled tasks can also use
skills. To keep scheduled tasks maintainable and shareable across teams, use
[skills](https://learn.chatgpt.com/docs/build-skills) to define the action and provide tools and context.
Select or invoke a specific skill in the task prompt when the workflow shouldn't
rely on automatic tool selection.

## Ask ChatGPT to create or update scheduled tasks

You can create and update scheduled tasks from a ChatGPT or Codex chat.
Describe the work, the schedule, and whether each scheduled run should return to
the current chat or start a new chat. ChatGPT can draft the prompt, choose the
right destination, and update the scheduled task when its scope or cadence
changes.

For example, ask ChatGPT to schedule a follow-up from the current chat while a
deployment finishes, or ask it to create a standalone scheduled task that checks
a project on a recurring schedule.

Skills can also create or update scheduled tasks. For example, a skill for
babysitting a pull request could set up a scheduled task that checks the
PR status with the GitHub plugin and fixes new review feedback.

## Schedule a task inside a chat

Schedule a task inside an existing chat when you want ChatGPT to return to that chat
on a schedule. The scheduled task uses the chat's existing context instead of
starting from a new prompt each time.

Scheduled tasks in a chat can use minute-based intervals for active follow-up
loops, or daily and weekly schedules when you need a check-in at a specific
time.

Schedule a task inside a chat for:

- checking a long-running operation until it finishes
- polling Slack, GitHub, or another connected source when the results should
  stay in the same chat
- reminding ChatGPT to continue a review loop at a fixed cadence
- running a skill-driven workflow that uses plugins, such as checking PR status
  and addressing new feedback
- continuing an ongoing research or triage chat without losing its context

Use a standalone scheduled task when each run should be independent or when
findings should appear as separate runs in **Scheduled**.

When you schedule a task inside a chat, make the prompt durable. It should describe
what ChatGPT should do on each scheduled run, how to decide whether there is
anything important to report, and when to stop or ask you for input.

## Test scheduled tasks

Before you schedule a task, test the prompt manually in a regular chat
first. This helps you confirm:

- The prompt is clear and scoped correctly.
- The selected or default model, reasoning effort, and tools behave as expected.
- The resulting output is reviewable.

When you start scheduling runs, review the first few outputs and adjust the
prompt or cadence as needed.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="app">

In the ChatGPT desktop app, you can explicitly trigger a skill in a scheduled
task prompt by using `$skill-name`.

## Worktree cleanup for scheduled tasks

If you choose worktrees for Git repositories, frequent schedules can create
many worktrees over time. Archive scheduled runs you no longer need, and avoid
pinning runs unless you intend to keep their worktrees.

## Permissions and security model

Scheduled tasks run unattended and use your default sandbox settings.

For a plain-language explanation of these boundaries, see the
[sandboxing overview](https://learn.chatgpt.com/docs/sandboxing). For filesystem and network
rules, see [Permissions](https://learn.chatgpt.com/docs/permissions).

- If your sandbox mode is **read-only**, tool calls fail if they require
  modifying files, accessing network, or working with apps on your computer.
  Consider updating sandbox settings to workspace write.
- If your sandbox mode is **workspace-write**, tool calls fail if they require
  modifying files outside the workspace, accessing network, or working with apps
  on your computer. You can selectively allowlist commands to run outside the
  sandbox using [rules](https://learn.chatgpt.com/docs/agent-configuration/rules).
- If your sandbox mode is **full access**, background scheduled tasks carry
  elevated risk, as ChatGPT may change files, run commands, and access network
  without asking. Consider updating sandbox settings to workspace write, and
  using [rules](https://learn.chatgpt.com/docs/agent-configuration/rules) to selectively define which commands the agent
  can run with full access.

If you are in a managed environment, admins can restrict these behaviors using
admin-enforced requirements. For example, they can disallow `approval_policy =
"never"` or constrain allowed sandbox modes. See
[Admin-enforced requirements (`requirements.toml`)](https://learn.chatgpt.com/docs/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml).

Scheduled tasks use `approval_policy = "never"` when your organization policy
allows it. If admin requirements disallow `approval_policy = "never"`,
scheduled tasks fall back to the approval behavior of your selected permission
mode.

## Examples

### Automatically create new skills

```markdown
Scan all of the `~/.codex/sessions` files from the past day and if there have been any issues using particular skills, update the skills to be more helpful. Personal skills only, no repo skills.

If there’s anything we’ve been doing often and struggle with that we should save as a skill to speed up future work, let’s do it.

Definitely don't feel like you need to update any- only if there's a good reason!

Let me know if you make any.
```

### Stay up-to-date with your project

```markdown
Look at the latest remote origin/master or origin/main . Then produce an exec briefing for the last 24 hours of commits that touch <DIRECTORY>

Formatting + structure:

- Use rich Markdown (H1 workstream sections, italics for the subtitle, horizontal rules as needed).
- Preamble can read something like “Here’s the last 24h brief for <directory>:”
- Subtitle should read: “Narrative walkthrough with owners; grouped by workstream.”
- Group by workstream rather than listing each commit. Workstream titles should be H1.
- Write a short narrative per workstream that explains the changes in plain language.
- Use bullet points and bolding when it makes things more readable
- Feel free to make bullets per person, but bold their name

Content requirements:

- Include PR links inline (e.g., [#123](...)) without a “PRs:” label.
- Do NOT include commit hashes or a “Key commits” section.
- It’s fine if multiple PRs appear under one workstream, but avoid per‑commit bullet lists.

Scope rules:

- Only include changes within the current cwd (or main checkout equivalent)
- Only include the last 24h of commits.
- Use `gh` to fetch PR titles and descriptions if it helps.
  Also feel free to pull PR reviews and comments
```

### Combining scheduled tasks with skills to fix your own bugs

Create a new skill that tries to fix a bug introduced by your own commits by creating a new `$recent-code-bugfix` and [store it in your personal skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills).

```markdown
---
name: recent-code-bugfix
description: Find and fix a bug introduced by the current author within the last week in the current working directory. Use when a user wants a proactive bugfix from their recent changes, when the prompt is empty, or when asked to triage/fix issues caused by their recent commits. Root cause must map directly to the author’s own changes.
---

# Recent Code Bugfix

## Overview

Find a bug introduced by the current author in the last week, implement a fix, and verify it when possible. Operate in the current working directory, assume the code is local, and ensure the root cause is tied directly to the author’s own edits.

## Workflow

### 1) Establish the recent-change scope

Use Git to identify the author and changed files from the last week.

- Determine the author from `git config user.name`/`user.email`. If unavailable, use the current user’s name from the environment or ask once.
- Use `git log --since=1.week --author=<author>` to list recent commits and files. Focus on files touched by those commits.
- If the user’s prompt is empty, proceed directly with this default scope.

### 2) Find a concrete failure tied to recent changes

Prioritize defects that are directly attributable to the author’s edits.

- Look for recent failures (tests, lint, runtime errors) if logs or CI outputs are available locally.
- If no failures are provided, run the smallest relevant verification (single test, file-level lint, or targeted repro) that touches the edited files.
- Confirm the root cause is directly connected to the author’s changes, not unrelated legacy issues. If only unrelated failures are found, stop and report that no qualifying bug was detected.

### 3) Implement the fix

Make a minimal fix that aligns with project conventions.

- Update only the files needed to resolve the issue.
- Avoid adding extra defensive checks or unrelated refactors.
- Keep changes consistent with local style and tests.

### 4) Verify

Attempt verification when possible.

- Prefer the smallest validation step (targeted test, focused lint, or direct repro command).
- If verification cannot be run, state what would be run and why it wasn’t executed.

### 5) Report

Summarize the root cause, the fix, and the verification performed. Make it explicit how the root cause ties to the author’s recent changes.
```

Afterward, create a new scheduled task:

```markdown
Check my commits from the last 24h and submit a $recent-code-bugfix.
```

</ContentModeSwitch>