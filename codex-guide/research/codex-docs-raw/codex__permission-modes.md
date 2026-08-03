# Permissions

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

{/* vale Microsoft.FirstPerson = NO */}

## Permission modes

Permissions control how ChatGPT (in the desktop app) and Codex (in the CLI or IDE) handle local actions, such as editing files, running commands, and using the internet. The mode you choose sets the boundary
for what ChatGPT can do on its own and what needs review.

For most work, start with **Ask for approval**. It lets ChatGPT work within the
current workspace and pauses before reaching beyond that boundary.

Select different modes below to understand how each one works.

<PermissionModeSelectorDemo client:load />

## Enable modes

When you're using the ChatGPT desktop app for the first time, you need to enable modes in application settings.

**Ask for approval** is always available. To add **Approve for me** (called
**Auto&#45;review** in settings) or **Full access** to the permissions menu, open
**Settings > General** in the ChatGPT desktop app, then turn on the mode under
**Permissions**. Enabling a mode makes it available in the menu; it doesn't
select the mode or change an existing chat.

<Illustration description="Permission visibility controls showing Default permissions, automatic review, and Full access.">
  <PermissionModeSettingsIllustration ariaLabel="Permission visibility controls showing Default permissions, automatic review, and Full access." />
</Illustration>

The available modes can depend on your local configuration and your
  organization's requirements. A mode that isn't allowed appears disabled.

## How permissions work

Two controls work together:

- The **sandbox** defines which files and network resources ChatGPT can access.
- **Approvals** determine when ChatGPT pauses before an action or sends the
  request to automatic review.

Changing who reviews a request doesn't expand the sandbox. For example,
**Approve for me** keeps the same workspace boundary as **Ask for approval**;
it sends requests to cross that boundary to automatic review.

Use the permissions control below the composer in the ChatGPT desktop app or
IDE extension.

<Illustration description="Approval-mode menu with Approve for me selected.">
  <PermissionModeComposerIllustration ariaLabel="Approval-mode menu with Approve for me selected." />
</Illustration>

In the CLI, enter `/permissions`. For technical details, see
[Sandbox](https://learn.chatgpt.com/docs/sandboxing), [automatic review](https://learn.chatgpt.com/docs/sandboxing/auto-review), or
[permission profiles](https://learn.chatgpt.com/docs/permissions).