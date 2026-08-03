# Pets

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Pets are optional animated companions for following work. Where a pet appears
and what it shows depend on the interface you use. Choosing a pet changes its
appearance, not how ChatGPT completes tasks.



  

    <CodexPetsDemo client:load mobileAlignment="left" />
  


<ContentModeSwitch group="codex-surface" id="app">

## Use a floating pet

In the ChatGPT desktop app, a pet can float above other app windows and help
you follow activity across your chats.

### Choose and wake a pet

1. Open the profile menu at the bottom of the app and select **Pets**. You can
   also open [**Settings**](codex://settings) and go to **Pets**.
2. Choose a built-in or custom pet.
3. Enter `/pet`, or open the command menu and select **Wake Pet**.

Select **Tuck Away Pet** in **Settings > Pets** or the command menu, or enter
`/pet` again, to hide the pet. Your selection and the pet's position persist
when you reopen the app.

When you select a custom pet, it also appears in your **Profile** view.

### Understand pet status

| Status          | Meaning                                                  |
| --------------- | -------------------------------------------------------- |
| **Running**     | A chat is actively working.                              |
| **Needs input** | A chat needs your approval, answer, or another decision. |
| **Ready**       | A chat has completed and has unread activity.            |
| **Blocked**     | A chat failed or encountered a system error.             |

When more than one chat has activity, the pet prioritizes chats that need
input, followed by blocked, ready, and running chats. Open the activity tray to
choose a chat.

Select the pet to return to ChatGPT, or select an activity to open its chat.
The activity tray is separate from [system
notifications](https://learn.chatgpt.com/docs/notifications?surface=app).

### Follow Computer Use

On macOS, the [Computer Use](https://learn.chatgpt.com/docs/computer-use) picture-in-picture window can
attach to an awake pet. Move the pet, and the window follows.

### Create a custom pet

1. Open **Settings > Pets** and select **Create your own pet**.
2. The app installs the bundled `hatch-pet` skill, reloads skills, and opens a
   new chat.
3. Describe the pet you want and send the prompt.
4. When the task finishes, return to **Settings > Pets**, select **Refresh**,
   and choose your new pet.

Custom pets created in the desktop app are stored locally on your computer.
They don't automatically sync to ChatGPT web.

### Reduce animation

Pets respect your operating system's reduced motion setting. When reduced
motion is enabled, the pet uses a still frame instead of sprite animation.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

## Choose a pet on the web

If Pets are available for your account and workspace, open **Settings >
Personalization > Pet > Select pet**. Choose a built-in pet, or choose
**Default** to use ChatGPT without a pet.

A web pet appears inside supported ChatGPT Work chats. It doesn't provide the
desktop app's floating overlay, activity tray, or `/pet` command.

### Upload a custom pet

Select **Upload pet** to add a custom sprite sheet. The file must be a
transparent PNG or WebP, exactly 1536 × 1872 pixels, and no larger than 20 MiB.
You can edit, download, refresh, or delete uploaded pets from the same setting.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">

## Choose a terminal pet

In an interactive Codex CLI session:

- Enter `/pets` or `/pet` to open the pet picker.
- Enter `/pets <name>` to choose a pet directly.
- Enter `/pets off` to disable terminal pets.

The picker includes built-in pets and compatible custom pets installed on your
computer. A terminal pet reports activity for the current CLI session. It uses
**Running**, **Needs input**, **Ready**, and **Blocked** states, but it doesn't
provide the desktop app's multiple-chat activity tray.

Terminal pets require iTerm2 3.6 or later, or a terminal with Kitty graphics or
Sixel support. They are unavailable inside tmux and Zellij.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">

## Pets in the IDE extension

The Codex IDE extension doesn't provide a pet picker or floating pet overlay.
Use the ChatGPT desktop app or Codex CLI when you want to use your own pet.

</ContentModeSwitch>




## Related docs

- [Notifications](https://learn.chatgpt.com/docs/notifications)
- [Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [ChatGPT desktop app settings](https://learn.chatgpt.com/docs/reference/settings#pets)