# ChatGPT Voice

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Powered by GPT-Live, ChatGPT Voice lets you talk through ideas and coordinate
tasks in Chat, Work, and Codex in the ChatGPT desktop app. Start work, check
progress, or change direction without switching back to typing.

ChatGPT Voice is available in the ChatGPT desktop app with ChatGPT Plus,
Pro, Business, Edu, and Enterprise plans. Enterprise and Edu availability
begins with a two-week early-access period before the feature becomes available
by default. You can also use ChatGPT Voice through
[Remote on iOS](https://learn.chatgpt.com/docs/remote-connections#set-up-mobile-access) after pairing
your phone with a desktop host. Availability also depends on rollout status and
workspace settings. See [feature availability](https://learn.chatgpt.com/docs/pricing#feature-availability).

<Illustration description="Interactive ChatGPT Voice conversation with microphone and speaker controls.">
  <CodexVoiceAgentIllustration />
</Illustration>

## Start talking

1. Open a new, empty chat or task in the ChatGPT desktop app.
2. Select **Start new voice chat** before sending a message.
3. The first time you start a voice chat, allow microphone access, choose a
   voice, and review screen context on macOS.
4. Start talking. Select **End** when you finish.

A chat or task must begin in voice mode to use ChatGPT Voice. Chats or tasks that
start in another mode offer voice dictation instead. To resume an earlier voice
chat, open it and select **Start voice chat**.

You can set a shortcut in **Settings > Voice > Voice chat hotkey**.

## Have a conversation

ChatGPT Voice supports natural turn-taking. You can interrupt ChatGPT
during a response, ask a follow-up, or change direction. If ChatGPT starts work,
keep talking to check progress or steer the task.

## Delegate and coordinate work

ChatGPT Voice can start separate threads for longer tasks, check existing threads,
and send follow-up instructions. It brings progress, blockers, and results back
to your voice conversation so you can keep talking while work continues.

For example:

- “Review today's launch brief and summarize decisions that need approval.”
- “Start a Codex task to run the tests and investigate anything that doesn't pass.”
- “Check active tasks and summarize anything blocking progress.”

ChatGPT Voice follows the same [permissions](https://learn.chatgpt.com/docs/permission-modes) as
the tasks it directs in Chat, Work, and Codex in the ChatGPT desktop app.

## Show ChatGPT what you see

On macOS, turn on **Screen context** in **Settings > Voice**, then say, “Take a
look at this.” ChatGPT can take an
[appshot](https://learn.chatgpt.com/docs/appshots#permissions-and-safety) of your frontmost window and
use it as context. Your organization can disable this capability.

An appshot can include the window's image and accessible text, including content
outside the visible scroll area. macOS may request **Screen & System Audio
Recording** and **Accessibility** permissions. Avoid sharing windows that
contain sensitive information, including text outside the visible scroll area.

## ChatGPT Voice and voice dictation

Use ChatGPT Voice for a live conversation with ChatGPT. Use [voice
dictation](https://learn.chatgpt.com/docs/prompting#use-voice-dictation) when you only want to turn
speech into prompt text before sending it.

## Limits and troubleshooting

Only one voice chat can be active across the ChatGPT desktop app at a time.
Voice conversations use a separate, plan-dependent allowance measured in rolling
five-hour windows. Tasks started through Voice continue to use your Codex usage
budget. ChatGPT notifies you when you reach either limit. See [Voice pricing and
limits](https://learn.chatgpt.com/docs/pricing#chatgpt-voice-in-desktop).

If you can't start a voice chat, confirm that ChatGPT Voice is available for your
plan, rollout, and workspace. Then check microphone permissions and whether a
voice chat is already active in another app window. If screen context isn't
available, check **Settings > Voice**, Appshots permissions, and your
organization's restrictions.