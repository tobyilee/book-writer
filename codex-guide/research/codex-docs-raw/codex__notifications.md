# Notifications

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Notifications let you know when work needs attention. Their controls and
delivery channels vary by surface.

<ContentModeSwitch group="codex-surface" id="app">

## Configure desktop notifications

Open [**Settings**](codex://settings) to choose whether turn-completion alerts
appear never, only while ChatGPT is in the background, or always. Separate
controls let you turn permission and question notifications on or off. Your
operating system may ask you to grant notification permission to the ChatGPT
desktop app.

<a id="follow-task-activity-with-a-pet"></a>

### Follow chat activity with a pet

In the ChatGPT desktop app, a floating pet is another way to follow chat
activity while you work in other apps. It can show when a chat is **Running**,
**Needs input**, **Ready**, or **Blocked**.

See [Pets](https://learn.chatgpt.com/docs/pets?surface=app) to choose a pet, understand its status, or
create your own.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

## Configure web notifications

Open **Settings > Notifications** to manage the notification categories and
channels available to your account. Depending on the category and account,
channels can include push, email, or SMS. Use **Manage tasks** from the task
notification settings to open **Scheduled**.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

## Configure CLI notifications

For terminal and external notifications, see
[Notifications](https://learn.chatgpt.com/docs/config-file/config-advanced#notifications) in the
advanced configuration guide. You can choose when the TUI emits a notification
and whether Codex runs an external program when a turn completes.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

<a id="follow-task-activity-in-the-ide"></a>

## Follow chat activity in the IDE

The IDE extension doesn't provide separate notification controls. Keep the
chat open to follow its activity. To run an external program when a turn
completes, configure `notify` on the connected Codex host. See
[Notifications](https://learn.chatgpt.com/docs/config-file/config-advanced#notifications) in the
advanced configuration guide.

</ContentModeSwitch>

## Related docs

- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [Scheduled tasks](https://learn.chatgpt.com/docs/automations)
- [Pets](https://learn.chatgpt.com/docs/pets)