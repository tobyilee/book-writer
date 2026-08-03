# Speed

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

**ChatGPT Work and Codex share usage.** Both use the same
  pricing, credits, and usage limits. See [Codex pricing](https://learn.chatgpt.com/docs/pricing) for
  details.

## Fast mode

Codex offers the ability to increase the speed of the model for increased
credit consumption.

Fast mode increases supported model speed by 1.5x and consumes credits at a
higher rate than Standard mode. It currently supports GPT-5.6, GPT-5.5, and
GPT-5.4. GPT-5.6 and GPT-5.5 consume credits at 2.5x the Standard rate;
GPT-5.4 consumes credits at 2x the Standard rate.

Use `/fast on`, `/fast off`, or `/fast status` in the CLI to change or inspect
the current setting. You can also persist the default with `service_tier =
"fast"` plus `[features].fast_mode = true` in `config.toml`. Fast mode is
available in the ChatGPT desktop app, Codex CLI, and IDE extension when you
sign in with ChatGPT. Fast mode is a ChatGPT credit feature. With an API key,
Codex uses API token pricing instead, and ChatGPT credit multipliers don't
apply. API Priority processing has its own billing rate; for GPT-5.6, it costs
2x the Standard API token rate.

<VideoPlayer
  src="/videos/codex/fast-mode-demo.mp4"
  class="[&_video]:mx-auto [&_video]:max-h-[400px] [&_video]:max-w-full [&_video]:w-auto"
/>

## Codex-Spark

GPT-5.3-Codex-Spark is a separate fast, less-capable Codex model optimized for
near-instant, real-time coding iteration. Unlike fast mode, which speeds up a
supported model at a higher credit rate, Codex-Spark is its own model choice
and has its own usage limits.

During research preview Codex-Spark is only available for ChatGPT Pro subscribers.