# Troubleshooting

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Frequently Asked Questions

### Files appear in the side panel that Codex didn't edit

If your project is inside a Git repository, the review panel automatically
shows changes based on your project's Git state, including changes that Codex
didn't make.

In the review pane, you can switch between staged changes and changes not yet
staged, and compare your branch with main.

If you want to see only the changes of your last Codex turn, switch the diff
pane to the **Last turn** view.

[Learn more about how to use the review pane](https://learn.chatgpt.com/docs/code-review?surface=app).

### Remove a project from the sidebar

To remove a project from the sidebar, hover over the name of your project, click
the three dots and choose "Remove." To restore it, re-add the
project using the **Add new project** button next to **Chats** or using

<kbd>Cmd</kbd>+<kbd>O</kbd>.

<a id="find-archived-threads"></a>
<a id="find-archived-tasks"></a>

### Find archived chats

Archived chats can be found in [Settings](codex://settings). When you unarchive
a chat, it reappears in its original sidebar location.

<a id="only-some-threads-appear-in-the-sidebar"></a>
<a id="only-some-tasks-appear-in-the-sidebar"></a>

### Only some chats appear in the sidebar

The sidebar lets you filter chats based on the state of a project. If you're
missing chats, select the filter icon next to **Chats**, then select
**Chronological**. If you still don't see the chat, open
[Settings](codex://settings) and check **Archived chats**.

### Code doesn't run on a worktree

Worktrees are created in a different directory and inherit files checked into
Git by default. Depending on how you manage dependencies and tooling for your
project, you might have to run setup scripts on your worktree using a
[local environment](https://learn.chatgpt.com/docs/environments/local-environment) or copy ignored setup files
with [`.worktreeinclude`](https://learn.chatgpt.com/docs/environments/git-worktrees#copy-ignored-local-files-into-managed-worktrees).
Alternatively, you can check out the changes in your regular local project. See
the [worktrees documentation](https://learn.chatgpt.com/docs/environments/git-worktrees) to learn more.

### App doesn't pick up a teammate's shared local environment

The local environment configuration must be inside the `.codex` folder at the
root of your project. If you are working in a monorepo with more than one
project, make sure you open the project in the directory that contains the
`.codex` folder.

### Codex asks to access Apple Music

Depending on your task, Codex may need to navigate the file system. Certain
directories on macOS, including Music, Downloads, or Desktop, require
additional approval from the user. If Codex needs to read your home directory,
macOS prompts you to approve access to those folders.

<a id="automations-create-many-worktrees"></a>

### Scheduled tasks create many worktrees

Frequent scheduled tasks can create many worktrees over time. Archive scheduled
runs you no longer need and avoid pinning runs unless you intend to keep their
worktrees.

### Recover a prompt after selecting the wrong target

If you started a chat with the wrong target (**Local**, **Worktree**, or **Cloud**) by accident, you can cancel the current run and recover your previous prompt by pressing the up arrow key in the composer.

### Feature is working in the Codex CLI but not in the ChatGPT desktop app

The ChatGPT desktop app and Codex CLI can include different Codex versions, so
features may reach one surface before the other. Experimental features might
also land in Codex CLI first.

To get the version of the Codex CLI on your system run:

```bash
codex --version
```

To get the version of Codex bundled with your ChatGPT desktop app, use the
retained `Codex.app` compatibility bundle path:

```bash
/Applications/Codex.app/Contents/Resources/codex --version
```

## Feedback and logs

Type <kbd>/</kbd> into the message composer to provide feedback for the team. If
you trigger feedback in an existing chat, you can choose to share the
existing session along with your feedback. After submitting your feedback,
you'll receive a session ID that you can share with the team.

To report an issue:

1. Find [existing issues](https://github.com/openai/codex/issues) on the Codex GitHub repo.
2. [Open a new GitHub issue](https://github.com/openai/codex/issues/new?template=2-bug-report.yml&steps=Uploaded%20thread%3A%20019c0d37-d2b6-74c0-918f-0e64af9b6e14)

More logs are available in the following locations:

- App logs (macOS): `~/Library/Logs/com.openai.codex/YYYY/MM/DD`
- Session transcripts: `$CODEX_HOME/sessions` (default: `~/.codex/sessions`)
- Archived sessions: `$CODEX_HOME/archived_sessions` (default: `~/.codex/archived_sessions`)

If you share logs, review them first to confirm they don't contain sensitive
information.

## Stuck states and recovery patterns

If a chat appears stuck:

1. Check whether Codex is waiting for an approval.
2. Open the terminal and run a basic command like `git status`.
3. Start a new chat with a smaller, more focused prompt.

If you cancel worktree creation by mistake and lose your prompt, press the up
arrow key in the composer to recover it.

## Terminal issues

**Terminal appears stuck**

1. Close the terminal panel.
2. Reopen it with <kbd>Ctrl</kbd>+<kbd>`</kbd>.
3. Re-run a basic command like `pwd` or `git status`.

If commands behave differently than expected, validate the current directory and
branch in the terminal first.

If it continues to be stuck, wait until your active chats are complete and restart the app.

**Fonts aren't rendering correctly**

Codex uses the same font for the review pane, integrated terminal and any other code displayed inside the app. You can configure the font inside the [Settings](codex://settings) pane as **Code font**.