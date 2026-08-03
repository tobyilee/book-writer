# Models

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

<ContentModeSwitch group="codex-surface" id="app">



  


## Choose a model

In the ChatGPT desktop app, use the model and reasoning control beneath the
composer to choose an available model and adjust its reasoning effort.

Higher reasoning effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  

  <CodexModelSwitcher client:visible className="lg:mt-7" />



</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="web">



  


## Choose a model

These recommendations apply to **ChatGPT Work** on the web. Use the
model and reasoning control beneath the composer to choose an available model
and adjust its reasoning effort.

Higher reasoning effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  

  <CodexModelSwitcher client:visible className="lg:mt-7" />



</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="cli">



  


## Choose a model

In an interactive CLI session, use `/model` to switch models or adjust
reasoning effort. You can also choose a model when you launch Codex with
`--model` or its `-m` alias:

```bash
codex --model gpt-5.6
```


The same option works with non-interactive runs. For example:

```bash
codex exec -m gpt-5.6 "Review the current changes"
```


Higher reasoning effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  

  <CodexReasoningLevelTerminal
    client:load
    className="lg:mt-7 lg:justify-self-end"
  />



</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" id="ide">



  


## Choose a model

Use the model switcher below the composer to choose an available model and
reasoning effort.

Higher reasoning effort can improve results for complex tasks, but it takes
longer and uses more tokens. Start with the default effort and increase it when
the task needs deeper planning or analysis.

**Ultra** mode goes
beyond a single-agent run. It uses
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to accelerate complex work,
making it useful for larger tasks that can be split across subagents.

  

  <CodexModelSwitcher client:visible forceDark className="lg:mt-7" />



</ContentModeSwitch>

<a id="recommended-models"></a>
<a id="other-models"></a>
<a id="deprecated-codex-models"></a>
<a id="configure-your-default-local-model"></a>
<a id="choose-a-model-for-cloud-tasks"></a>

<ContentModeSwitch group="codex-surface" ids="app,web,cli,ide">

## Recommended models



  <ModelDetails
    client:load
    name="gpt-5.6-sol"
    slug="gpt-5.6-sol"
    imageLabel="5.6 Sol"
    wallpaperUrl="/images/api/models/gpt-5.6-sol.webp"
    description="Flagship GPT-5.6 model with the strongest capability for complex coding, computer use, research, and cybersecurity."
    data={{
      features: [
        {
          title: "Capability",
          value: "",
          icons: [
            "openai.SparklesFilled",
            "openai.SparklesFilled",
            "openai.SparklesFilled",
            "openai.SparklesFilled",
            "openai.SparklesFilled",
          ],
        },
        {
          title: "Speed",
          value: "",
          icons: ["openai.Flash", "openai.Flash"],
        },
        { title: "ChatGPT desktop app", value: true },
        { title: "ChatGPT web", value: true },
        { title: "Codex CLI", value: true },
        { title: "Codex IDE extension", value: true },
        { title: "Codex cloud", value: true },
        { title: "ChatGPT Credits", value: true },
        { title: "API Access", value: true },
      ],
    }}
  />

<ModelDetails
  client:load
  name="gpt-5.6-terra"
  slug="gpt-5.6-terra"
  imageLabel="5.6 Terra"
  wallpaperUrl="/images/api/models/gpt-5.6-terra.webp"
  description="Balanced GPT-5.6 model for everyday work, with performance competitive with GPT-5.5 at a lower cost."
  data={{
    features: [
      {
        title: "Capability",
        value: "",
        icons: [
          "openai.SparklesFilled",
          "openai.SparklesFilled",
          "openai.SparklesFilled",
          "openai.SparklesFilled",
        ],
      },
      {
        title: "Speed",
        value: "",
        icons: ["openai.Flash", "openai.Flash", "openai.Flash"],
      },
      { title: "ChatGPT desktop app", value: true },
      { title: "ChatGPT web", value: true },
      { title: "Codex CLI", value: true },
      { title: "Codex IDE extension", value: true },
      { title: "Codex cloud", value: false },
      { title: "ChatGPT Credits", value: true },
      { title: "API Access", value: true },
    ],
  }}
/>

<ModelDetails
  client:load
  name="gpt-5.6-luna"
  slug="gpt-5.6-luna"
  imageLabel="5.6 Luna"
  wallpaperUrl="/images/api/models/gpt-5.6-luna.webp"
  description="Fast and affordable GPT-5.6 model that delivers strong capability at the lowest cost in the family."
  data={{
    features: [
      {
        title: "Capability",
        value: "",
        icons: [
          "openai.SparklesFilled",
          "openai.SparklesFilled",
          "openai.SparklesFilled",
        ],
      },
      {
        title: "Speed",
        value: "",
        icons: ["openai.Flash", "openai.Flash", "openai.Flash", "openai.Flash"],
      },
      { title: "ChatGPT desktop app", value: true },
      { title: "ChatGPT web", value: true },
      { title: "Codex CLI", value: true },
      { title: "Codex IDE extension", value: true },
      { title: "Codex cloud", value: false },
      { title: "ChatGPT Credits", value: true },
      { title: "API Access", value: true },
    ],
  }}
/>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">
  <ModelDetails
    client:load
    name="gpt-5.3-codex-spark"
    slug="gpt-5.3-codex-spark"
    imageLabel="5.3 Codex Spark"
    wallpaperUrl="/images/codex/codex-wallpaper-2.webp"
    description="Text-only research preview model optimized for near-instant, real-time coding iteration. Available to ChatGPT Pro users."
    data={{
      features: [
        {
          title: "Capability",
          value: "",
          icons: ["openai.SparklesFilled", "openai.SparklesFilled"],
        },
        {
          title: "Speed",
          value: "",
          icons: [
            "openai.Flash",
            "openai.Flash",
            "openai.Flash",
            "openai.Flash",
            "openai.Flash",
          ],
        },
        { title: "ChatGPT desktop app", value: true },
        { title: "ChatGPT web", value: false },
        { title: "Codex CLI", value: true },
        { title: "Codex IDE extension", value: true },
        { title: "Codex cloud", value: false },
        { title: "ChatGPT Credits", value: false },
        { title: "API Access", value: false },
      ],
    }}
  />
</ContentModeSwitch>




Start with the default Power setting, which uses `gpt-5.6-sol` with medium
  reasoning. Move toward **Smarter** for deeper reasoning or **Faster** for
  faster, lower-cost work. Open **Advanced** when you want `gpt-5.6-luna` or a
  specific model, reasoning effort, or speed.

## Choosing Sol, Terra, and Luna

Codex offers three GPT-5.6 models: **Sol** for detail and polish, **Terra** as the
everyday workhorse, and **Luna** for clear, repeatable work. If you are unsure,
start with Sol.

### Where each model shines

- **Sol, for complex, open-ended work.** Choose Sol for ambiguous, difficult, or
  high-value tasks that need extra analysis, judgment, or polish, such as
  complex code changes, deep research, or polished documents. For narrower
  tasks, define what done looks like to keep the work focused.
- **Terra, the pragmatic all-rounder.** Choose Terra for everyday work that
  needs strong reasoning and tool use when you do not need Sol's full depth. It
  is a natural starting point for work you previously gave GPT-5.5.
- **Luna, for clear, repeatable tasks.** Choose Luna for specific, high-volume
  tasks when you know what a good result looks like, such as extraction,
  classification, transformation, and structured summaries.

### Pick a reasoning effort

Use the lowest reasoning effort that produces the result you need. Increase it
for tasks that need more planning, analysis, or checking.

- **Light** in the ChatGPT desktop app, ChatGPT Work on the web, and IDE extension, or **Low** in the
  CLI, suits quick, well-scoped tasks.
- **Medium** balances speed and depth for tasks that need more planning.
- **High** and **Extra High** suit difficult work with multiple steps, sources,
  or tradeoffs.

There is no exact mapping from GPT-5.5 reasoning efforts to GPT-5.6. Try a
familiar task at a lower setting and adjust based on the result.

### Know when to use Max or Ultra

**Max** gives the selected model more time to reason about a single task. Use it
for the hardest problems, when depth matters more than speed or usage. If you
don't see Max in your options, you'll have to enable it in your app settings.

**Ultra** uses [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) to handle
separate parts of a complex task in parallel. Choose it when you can divide the
work into meaningful parts. Most tasks do not need Max or Ultra.

If Ultra doesn't appear in the desktop app's model slider, go to
**Settings** > **Configuration**, then turn on **Ultra in model picker slider**.

</ContentModeSwitch>

<ContentModeSwitch group="codex-surface" ids="app,cli,ide">

## Other models

When you sign in with ChatGPT, Codex works best with the recommended models listed above.

**
    GPT-5.4 and GPT-5.4 mini retire from Codex on August 31, 2026.
  ** 
  If you sign in with ChatGPT, replace `gpt-5.4` with `gpt-5.6-terra` and
  `gpt-5.4-mini` with `gpt-5.6-luna` in saved configurations, custom agents, and
  scheduled tasks. The OpenAI API and Codex authenticated with your own API key
  aren't affected.

<ToggleSection title="View other models">
  

    <ModelDetails
      client:load
      name="gpt-5.5"
      slug="gpt-5.5"
      imageLabel="5.5"
      wallpaperUrl="/images/api/models/gpt-5.5.jpg"
      description="Previous-generation frontier model for complex coding, computer use, knowledge work, and research workflows."
      data={{
        features: [
          {
            title: "Capability",
            value: "",
            icons: [
              "openai.SparklesFilled",
              "openai.SparklesFilled",
              "openai.SparklesFilled",
              "openai.SparklesFilled",
            ],
          },
          {
            title: "Speed",
            value: "",
            icons: ["openai.Flash", "openai.Flash", "openai.Flash"],
          },
          { title: "ChatGPT desktop app", value: true },
          { title: "ChatGPT web", value: true },
          { title: "Codex CLI", value: true },
          { title: "Codex IDE extension", value: true },
          { title: "Codex cloud", value: false },
          { title: "ChatGPT Credits", value: true },
          { title: "API Access", value: true },
        ],
      }}
    />

    <ModelDetails
      client:load
      name="gpt-5.4"
      slug="gpt-5.4"
      imageLabel="5.4"
      wallpaperUrl="/images/api/models/gpt-5.4.jpg"
      description="Frontier model for professional work with strong coding, reasoning, tool use, and agentic workflow capabilities."
      data={{
        features: [
          {
            title: "Capability",
            value: "",
            icons: [
              "openai.SparklesFilled",
              "openai.SparklesFilled",
              "openai.SparklesFilled",
            ],
          },
          {
            title: "Speed",
            value: "",
            icons: ["openai.Flash", "openai.Flash", "openai.Flash"],
          },
          { title: "ChatGPT desktop app", value: true },
          { title: "ChatGPT web", value: true },
          { title: "Codex CLI", value: true },
          { title: "Codex IDE extension", value: true },
          { title: "Codex cloud", value: false },
          { title: "ChatGPT Credits", value: true },
          { title: "API Access", value: true },
        ],
      }}
    />

    <ModelDetails
      client:load
      name="gpt-5.4-mini"
      slug="gpt-5.4-mini"
      imageLabel="5.4 Mini"
      wallpaperUrl="/images/api/models/gpt-5-mini.jpg"
      description="Fast, efficient mini model for responsive coding tasks and subagents."
      data={{
        features: [
          {
            title: "Capability",
            value: "",
            icons: ["openai.SparklesFilled", "openai.SparklesFilled"],
          },
          {
            title: "Speed",
            value: "",
            icons: [
              "openai.Flash",
              "openai.Flash",
              "openai.Flash",
              "openai.Flash",
            ],
          },
          { title: "ChatGPT desktop app", value: true },
          { title: "ChatGPT web", value: true },
          { title: "Codex CLI", value: true },
          { title: "Codex IDE extension", value: true },
          { title: "Codex cloud", value: false },
          { title: "ChatGPT Credits", value: true },
          { title: "API Access", value: true },
        ],
      }}
    />

  

</ToggleSection>

You can also point Codex at any model and provider that supports either the [Chat Completions](https://platform.openai.com/docs/api-reference/chat) or [Responses APIs](https://platform.openai.com/docs/api-reference/responses) to fit your specific use case.

Support for the Chat Completions API is deprecated and will be removed in
  future releases of Codex.

## Deprecated Codex models

The `gpt-5.4` and `gpt-5.4-mini` models retire from Codex with ChatGPT sign-in
on August 31, 2026. Replace `gpt-5.4` with `gpt-5.6-terra` and
`gpt-5.4-mini` with `gpt-5.6-luna` in workspace defaults, saved model
settings, managed configurations, custom agents, and scheduled tasks.

The `gpt-5.2` and `gpt-5.3-codex` models are already deprecated in Codex when
you sign in with ChatGPT. Update scripts, configuration files, and
`codex exec --model` commands that still reference those models.

The OpenAI API and Codex authenticated with your own API key aren't affected
by the GPT-5.4 retirement. For current API model availability, see the
[API models page](https://developers.openai.com/api/docs/models).

## Configure your default local model

The ChatGPT desktop app, Codex CLI, and IDE extension use the same `config.toml`
[configuration file](https://learn.chatgpt.com/docs/config-file/config-basic). To specify a model, add a
`model` entry to your configuration file. If you don't specify a model, the
ChatGPT desktop app, Codex CLI, or IDE extension uses a recommended model.

```toml
model = "gpt-5.6"
```


## Choose a model for cloud chats

Currently, you can't change the default model for Codex cloud chats.

</ContentModeSwitch>