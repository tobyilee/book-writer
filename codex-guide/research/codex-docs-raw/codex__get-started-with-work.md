# Get started with ChatGPT Work

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<VideoPlayer src="https://cdn.openai.com/devhub/superapp-video-v1.mp4" />

<a id="introducing-work-mode"></a>

## Introducing ChatGPT Work

ChatGPT Work is a way to delegate real work to ChatGPT.

Use Chat when you want an answer, explanation, brainstorm, or short draft.
Use ChatGPT Work when you want ChatGPT to complete a task with a clear outcome, such as a
brief, deck, analysis, recurring update, workflow, or file you can review and
use. Learn more about [using Chat and ChatGPT Work together](https://learn.chatgpt.com/docs/use-chatgpt).

ChatGPT Work can use your files, plugins, and approved tools to retrieve information,
create finished files, run workflows, and complete work that is ready for you to
review. You can follow progress, answer questions, change direction, and
approve important actions.

On the [desktop app](https://learn.chatgpt.com/docs/app), ChatGPT Work can also use local files, apps, and the
browser when those tools are available.

If you have used Codex for non-coding work, you can stay in Codex or use
ChatGPT Work instead. ChatGPT Work gives you the same core capabilities with
an experience designed for everyday work.

## What to try first

<VideoPlayer src="https://cdn.openai.com/devhub/videos-learn/selectnoonboarding.mp4" />

First, switch to **Work**. Then choose your first task.
Good tasks have a clear outcome, a few source materials, and an output you can
review.

### Choose local or cloud work

In the desktop app, open the composer control labeled **Work locally**. If
**Cloud** appears as an option, choose it when you want ChatGPT Work to keep
running after you close the app or turn off your computer, or when you want to
continue the chat from the web or mobile app. Keep **Work locally** selected when
the task needs files or apps on your computer.

Cloud is also useful for scheduled tasks that research or check websites over
time because their runs don't depend on your computer being awake.

Here are three common use cases you can get started with:

### Create a presentation

Use ChatGPT Work to turn notes, docs, research, or meeting materials into a structured
deck.

<CodexScreenshot
  alt="A presentation created in ChatGPT Work"
  lightSrc="/codex/get-started-with-work/create-presentation.webp"
  darkSrc="/codex/get-started-with-work/create-presentation.webp"
  maxHeight={520}
  class="my-6 p-4 md:p-8"
/>



**Example prompt:**

```text
Review the attached source materials and create an eight-slide presentation for [audience]. Focus on the main themes, include supporting evidence, and flag anything that needs human review. Return a draft for my review.
```

### Create a comparison spreadsheet

Use ChatGPT Work to turn notes, files, or research into a spreadsheet that compares
options and helps you make a decision.

<CodexScreenshot
  alt="A comparison spreadsheet created in ChatGPT Work"
  lightSrc="/codex/get-started-with-work/comparison-spreadsheet.webp"
  darkSrc="/codex/get-started-with-work/comparison-spreadsheet.webp"
  maxHeight={520}
  class="my-6 p-4 md:p-8"
/>



**Example prompt:**

```text
Create a spreadsheet comparing the options for [decision]. Use the attached notes and source materials. Include the most important criteria, score each option, flag risks or missing information, and add a summary tab with a recommendation and next steps.
```

### Set up a recurring update

Use scheduled tasks when you want ChatGPT Work to repeat, monitor, or refresh something
over time.

<CodexScreenshot
  alt="A recurring update scheduled in ChatGPT Work"
  lightSrc="/codex/get-started-with-work/recurring-update.webp"
  darkSrc="/codex/get-started-with-work/recurring-update.webp"
  maxHeight={520}
  class="my-6 p-4 md:p-8"
/>



**Example prompt:**

```text
Every Monday morning, review new updates from @Slack and @Google Drive for [project]. Refresh the meeting agenda with decisions, blockers, owners, and open questions. Send me a draft before sharing it.
```

Learn more about [scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app).

<a id="best-practices-for-using-work"></a>
<a id="best-practices-for-using-work-mode"></a>

## Best practices for using ChatGPT Work

Use ChatGPT Work when you want ChatGPT to complete a task, create a file, or manage work
over time. It is a good fit for tasks that:

- Use multiple sources, plugins, tools, or steps.
- Would take meaningful time to complete manually.
- Produce an output you will review, edit, or reuse.
- Need to be repeated, monitored, or updated over time.

To get a better result, tell ChatGPT the outcome you need, the sources or plugins
to use, any constraints to follow, what good looks like, and when to stop for
review or approval.

**Instead of:** Make me a presentation about our customer research.



**Example prompt:**

```text
Review the attached interview notes and survey results. Create an eight-slide presentation for the product leadership meeting. Focus on the three most common customer problems, include supporting evidence, separate findings from recommendations, and flag any claims that are not well supported. Use @Google Drive for the source docs. Return a draft for my review before treating it as final.
```

Learn more about [prompting for ChatGPT Work](https://learn.chatgpt.com/docs/prompting#prompting-for-work).

## Add plugins for more context and better outputs

<CodexScreenshot
  alt="The plugins library in ChatGPT Work"
  lightSrc="/codex/get-started-with-work/plugins.webp"
  darkSrc="/codex/get-started-with-work/plugins.webp"
  maxHeight={520}
  class="my-6 p-4 md:p-8"
/>

Plugins connect ChatGPT Work to tools your team uses, like Slack, Google Drive,
SharePoint, email, calendars, customer relationship management systems, and
project trackers.

- Select **Plugins** in the left sidebar to view the plugins library.
- Install the plugins most relevant to your work.
- To point ChatGPT to a specific tool, type `@` and the plugin name in your prompt.

Learn more about [plugins](https://learn.chatgpt.com/docs/plugins).

<a id="use-work-mode-efficiently"></a>

## Use ChatGPT Work efficiently

ChatGPT Work is best for substantial tasks that involve multiple steps, sources, or
tools, or require a completed deliverable. Longer or more complex tasks may use
more credits because ChatGPT is doing more on your behalf. Focus on the value of
the completed result, rather than the number of prompts.

Keep the task focused by setting useful boundaries. For example: “use only
these sources,” “compare the top five options,” or “stop before sending
anything.”

Use Chat instead for quick questions, short rewrites, and decisions where you
only need advice.

Learn more about [working efficiently](https://learn.chatgpt.com/docs/prompting#prompting-for-work).

## More use cases

Explore practical ChatGPT Work workflows for common teams and tasks.

<CodexCollectionList
  slugs={[
    "productivity-and-collaboration",
    "business-operations",
    "data-science",
    "finance",
    "sales",
    "life-sciences",
    "education",
  ]}
/>