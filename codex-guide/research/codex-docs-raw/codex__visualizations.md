# Visualizations

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Visualizations turn questions, ideas, and information into charts, maps,
diagrams, calculators, simulations, and interactive explanations you can explore
in a ChatGPT chat. Use one when adjusting inputs or seeing a
relationship would make an answer easier to understand, compare, practice, or
act on.

The Visualizations preview is rolling out. Availability can depend on your
  plan, platform, account, and workspace settings.

<ContentModeSwitch group="codex-surface" id="app">

The Visualizations preview is rolling out in the ChatGPT desktop app. When
**Visualize** is available, type `@` in the composer, start entering
`Visualize`, and select **Visualize** under **Plugins**. The composer adds a
**Visualize** tag before your request.

If **Visualize** doesn't appear, use ChatGPT on the web or try again after the
preview reaches your account.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">

In a supported Chat or ChatGPT Work chat, type `@` in the composer,
start entering `Visualize`, and select **Visualize** under **Plugins**. Its
description is **Create visualizations and interactive tools**. The composer
adds a **Visualize** tag before your request.

You can also type `@Visualize` and select the matching suggestion.

</ContentModeSwitch>





## Check availability

| Surface                     | Current availability                                                          |
| --------------------------- | ----------------------------------------------------------------------------- |
| ChatGPT on the web          | Available to supported accounts in Chat and ChatGPT Work                      |
| ChatGPT desktop app         | Rolling out in preview                                                        |
| ChatGPT mobile apps         | Rolling out to eligible accounts; composer controls can differ by app version |
| Codex CLI and IDE extension | Visualization rendering isn't supported                                       |

The **Visualize** suggestion is the reliable sign that the preview is enabled
for your account. During the rollout, availability can differ across accounts,
workspaces, and app versions, even on the same plan.

## Choose when a visualization helps

ChatGPT can choose a visual format when it materially improves the answer. You
can also tag `@Visualize` when you specifically want an interactive result.

Ask for the smallest format that fits the job:

- Use a diagram for labeled relationships or a process.
- Use a chart or plot for named numeric data and comparisons.
- Use a map for geographic information.
- Use an interactive visualization when inputs, time, motion, or spatial
  relationships should change.
- Use a [Site](https://learn.chatgpt.com/docs/sites) when you need a durable hosted application with a
  shareable URL, permissions, or persistent data.

## Prompt with an outcome and controls

A strong request names the outcome, source material, question, and useful
interactions. Try this example:



**Prompt:**

```text
@Visualize how supply and demand determine a market price. Let me shift each curve, mark the equilibrium, and explain how price and quantity change.
```

Tell ChatGPT which information to use, such as content already in the
chat, pasted data, an attached file, or an available connected source.
For complex requests, choose a higher reasoning setting when one is available.

## Explore interactive examples

These examples reproduce three visualizations from the GPT-5.6 launch page.
Use their controls to see how a focused prompt can become an interactive
explanation, lab, or teaching tool.

<Illustration description="Three interactive ChatGPT visualization examples: a spirograph with adjustable geometry, a wave interference lab with a movable probe, and a tokenizer explainer with editable text and tokenization steps.">
  <VisualizationExampleGallery client:visible />
</Illustration>

## Refine and continue

Continue in the same chat and describe the change you want. Useful
follow-ups include:

- Add or remove a control, filter, comparison, or annotation.
- Correct the source data, units, labels, or assumptions.
- Simplify a slow result by aggregating, binning, or sampling the data.
- Add a concise text summary and a data table.
- Make every control keyboard accessible and add visible focus states.
- Use labels or patterns as well as color, and remove looping motion.
- Turn the result into a Site when it should be hosted and revisited.

A follow-up can create a replacement visualization instead of editing the
original result in place. Review the new version before relying on it.

## Share or reuse a result

Use the chat's standard **Share** action when it's available. Review
the entire shared chat first, including its source data and earlier
messages. A visualization is generally a snapshot of the information available
when ChatGPT created it, not a live dashboard that stays synchronized with a
connected source.

Generated download controls and export formats can vary by result. If an export
doesn't work, ask ChatGPT for the underlying data in a simpler format or ask it
to turn the visualization into a Site.

## Improve accessibility

Generated visualizations aim to use semantic controls, visible focus, readable
contrast, and reduced motion, but the result can vary. Check the visualization
before sharing it. Ask ChatGPT to add a text summary and data table, label axes
and units, avoid relying on color alone, and make controls work from a keyboard.

## Recover from a failed result

Visualizations can take a minute or longer to generate. If the result is blank
or missing, wait for the response to finish, reload the chat once, and
then retry. If it still fails:

- Ask for a smaller or simpler visualization.
- Aggregate or bin data, sample fewer points, or reduce precision in a large dataset.
- Remove a generated control or library that isn't working.
- Verify important values, geographic boundaries, and source assumptions.
- Ask for a chart, diagram, table, or Site instead.

Use the same data-handling judgment you use for any ChatGPT chat. Only
include sensitive information when your organization permits it, and review
the full chat before you share it.

## Related docs

- [Sites](https://learn.chatgpt.com/docs/sites)
- [Projects and chats](https://learn.chatgpt.com/docs/projects)
- [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer)
- [Image generation](https://learn.chatgpt.com/docs/image-generation)