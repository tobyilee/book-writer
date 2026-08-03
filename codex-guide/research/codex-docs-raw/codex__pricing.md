# Pricing

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

**ChatGPT Work and Codex share usage.** ChatGPT Work usage inside
  ChatGPT uses the same pricing, credits, and usage limits as Codex.

<h2 class="sr-only">Pricing options</h2>

<ContentSwitcher
  id="codex-pricing-plans"
  initialValue="individual"
  options={[
    {
      label: "Individual",
      value: "individual",
    },
    {
      label: "Business / Enterprise",
      value: "business-enterprise",
    },
  ]}
>
  

    

      <PricingCard
        name="Free"
        subtitle="Explore Codex capabilities on quick coding tasks."
        price="$0"
        interval="/month"
        ctaLabel="Get Free"
        ctaHref="https://chatgpt.com/plans/free/"
      />
      <PricingCard
        name="Go"
        subtitle="Use Codex for lightweight coding tasks."
        price="$8"
        interval="/month"
        ctaLabel="Get Go"
        ctaHref="https://chatgpt.com/plans/go"
      />
      <PricingCard
        name="Plus"
        subtitle="Power a few focused coding sessions each week."
        price="$20"
        interval="/month"
        ctaLabel="Get Plus"
        ctaHref="https://chatgpt.com/explore/plus?utm_internal_source=openai_developers_codex"
      >
        - Codex on the web, in the CLI, in the IDE extension, and on iOS
        - Cloud-based integrations like automatic code review and Slack
          integration
        - The GPT-5.6 model family, including Sol, Terra, and Luna
        - GPT-5.6 Luna for higher usage limits on lighter-weight or high-volume
          workloads
        - Flexibly extend usage with [ChatGPT credits](#credits-overview)
        - Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
          Plus plan
      </PricingCard>
      <PricingCard
        name="Pro"
        subtitle="Choose 5x or 20x higher rate limits than Plus."
        priceEyebrow="From"
        price="$100"
        interval="/month"
        ctaLabel="Get Pro"
        ctaHref="https://chatgpt.com/explore/pro?utm_internal_source=openai_developers_codex"
        highlight="Everything in Plus and:"
        footnoteLabel="*Learn more about limits on both tiers."
        footnoteHref="https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans"
      >
        - Access to GPT-5.3-Codex-Spark (research preview), a fast Codex model
          for day-to-day coding tasks
        - 5x or 20x more Codex usage than Plus*
        - Unlimited ChatGPT Voice on the $200/month tier; tasks still draw from
          your Codex usage budget
        - Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
          Pro plan
      </PricingCard>
      <PricingCard
        name="API Key"
        subtitle="Great for automation in shared environments like CI."
        price=""
        interval=""
        ctaLabel="Learn more"
        ctaHref="/codex/auth"
        highlight=""
      >
        - Codex in the CLI, SDK, or IDE extension
        - No cloud-based features (GitHub code review, Slack, etc.)
        - Model availability follows the API models available to your key
        - Pay only for the tokens Codex uses, based on [API
          pricing](https://platform.openai.com/docs/pricing)
      </PricingCard>
    


  


  

    

      <PricingCard
        name="Business"
        subtitle="Bring Codex into your startup or growing business."
        price="$20"
        interval="/ user / month*"
        ctaLabel="Get Business"
        ctaHref="https://chatgpt.com/team-sign-up"
        footnoteLabel="*2+ users, billed annually. $25 per user per month when billed monthly."
      >
        - Access ChatGPT and Codex across desktop and mobile apps
        - Larger virtual machines to run cloud chats faster
        - Flexibly extend usage with [ChatGPT credits](#credits-overview)
        - A secure, dedicated workspace with essential admin controls, SAML SSO,
          and MFA
        - No training on your business data by default. [Learn
          more](https://openai.com/business-data/)
        - Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
          Business plan
      </PricingCard>
      <PricingCard
        name="Enterprise & Edu"
        subtitle="Unlock Codex for your entire organization with enterprise-grade functionality."
        interval=""
        ctaLabel="Contact sales"
        ctaHref="https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex"
        highlight="Everything in Business and:"
      >
        - Priority request processing
        - Enterprise-level security and controls, including SCIM, EKM, user
          analytics, domain verification, and role-based access control
          ([RBAC](https://help.openai.com/en/articles/11750701-rbac))
        - Audit logs and usage monitoring via the [Compliance
          API](https://chatgpt.com/admin/api-reference#tag/Codex-Tasks)
        - Data retention and data residency controls
        - Other [ChatGPT features](https://chatgpt.com/pricing) as part of the
          Enterprise plan
      </PricingCard>
    


    

      <PricingCard
        class="codex-pricing-card--span-two"
        name="API Key"
        subtitle="Great for automation in shared environments like CI."
        price=""
        interval=""
        ctaLabel="Learn more"
        ctaHref="/codex/auth"
        highlight=""
      >
        - Codex in the CLI, SDK, or IDE extension
        - No cloud-based features (GitHub code review, Slack, etc.)
        - Model availability follows the API models available to your key
        - Pay only for the tokens Codex uses, based on [API
          pricing](https://platform.openai.com/docs/pricing)
      </PricingCard>
    


  

</ContentSwitcher>

## Invite friends and coworkers

Eligible users can send Codex invitations from the profile menu in the
lower-left corner of the app. Choose **Invite a friend** on an eligible personal
plan or **Invite a coworker** in an eligible Business workspace, enter the
recipient's email address, and send the invitation.

The invitation dialog shows the current reward, recipient requirements, invite
limits, and when rewards expire for your plan or promotion. Personal and
Business referral programs have separate rewards and eligibility rules.
Referrals aren't currently available for ChatGPT Enterprise.

From June 11 through June 24, 2026, eligible Plus and Pro users can invite up to
three friends. When an eligible recipient sends their first Codex message, both
people receive a banked rate-limit reset. Banked rate-limit resets are usable for
30 days after they're granted. Business referrals use separate shared-workspace
credit rewards; review the
[current terms](https://help.openai.com/en/articles/20001271) before you send an
invitation.

## Frequently asked questions

### How much does Sites cost?

[Sites](https://learn.chatgpt.com/docs/sites) is included with eligible ChatGPT plans during public
beta. Availability depends on your plan, region, and workspace settings.

### What are the usage limits for my plan?

The number of messages you can send depends on the model used, size and
complexity of your tasks, and whether you run them locally or in the cloud.
Small scripts or routine functions may consume only a fraction of your
allowance, while larger projects, long-running tasks, or extended sessions that
require the agent to hold more context will use significantly more per message.

Tasks that look similar can consume different amounts of your allowance. Model
choice, context, reasoning, tool use, retrieval, and caching all affect usage,
so prompt length alone isn't a reliable estimate.

Choose the GPT-5.6 model that best fits your work:

- **Sol** is built for the hardest work—complex reasoning, ambiguous problems,
  advanced coding, and high-stakes decisions.
- **Terra** is the everyday workhorse for production tasks, reporting, document
  analysis, coding, and work that requires sound judgment.
- **Luna** is optimized for fast, high-volume work such as routing,
  classification, extraction, support, background automation, and focused coding
  tasks.



  <ContentSwitcher
    id="codex-usage-limits"
    initialValue="plus"
    align="right"
    options={[
      {
        label: "Plus",
        value: "plus",
      },
      {
        label: "Pro 5x",
        value: "pro",
      },
      {
        label: "Pro 20x",
        value: "pro-20x",
      },
      {
        label: "Business",
        value: "business",
      },
      {
        label: "API Key",
        value: "api-key",
      },
    ]}
  >
    

      
Plus


      <table>
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col" style="text-align:center">
              Local Messages[\*](#shared-limits-plus) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Cloud chats[\*](#shared-limits-plus) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Code Reviews / 5h
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GPT-5.6 Sol</td>
            <td style="text-align:center">10-100</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Terra</td>
            <td style="text-align:center">25-200</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Luna</td>
            <td style="text-align:center">250-2,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.5</td>
            <td style="text-align:center">15-80</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4</td>
            <td style="text-align:center">20-100</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4 mini</td>
            <td style="text-align:center">60-350</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="4" style="text-align:center">
              <a id="shared-limits-plus" class="footnote">
                *The usage limits for local messages and cloud chats share a
                **five-hour window**. Additional weekly limits may apply.
              </a>
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              For Enterprise/Edu users with flexible pricing, there are no
              fixed rate limits - usage scales with
              [credits](#credits-overview)
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              Enterprise and Edu plans without flexible pricing have the same
              per-seat usage limits as Plus for most features
            </td>
          </tr>
        </tfoot>
      </table>
    

    

      
Pro 5x


      <table>
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col" style="text-align:center">
              Local Messages[\*](#shared-limits-pro) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Cloud chats[\*](#shared-limits-pro) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Code Reviews / 5h
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GPT-5.6 Sol</td>
            <td style="text-align:center">50-500</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Terra</td>
            <td style="text-align:center">125-1,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Luna</td>
            <td style="text-align:center">1,250-10,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.5</td>
            <td style="text-align:center">75-400</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4</td>
            <td style="text-align:center">100-500</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4 mini</td>
            <td style="text-align:center">300-1750</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="4" style="text-align:center">
              <a id="shared-limits-pro" class="footnote">
                *The usage limits for local messages and cloud chats share a
                **five-hour window**. Additional weekly limits may apply.
              </a>
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              For Enterprise/Edu users with flexible pricing, there are no
              fixed rate limits - usage scales with
              [credits](#credits-overview)
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              Enterprise and Edu plans without flexible pricing have the same
              per-seat usage limits as Plus for most features
            </td>
          </tr>
        </tfoot>
      </table>
    

    

      
Pro 20x


      <table>
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col" style="text-align:center">
              Local Messages[\*](#shared-limits-pro-20x) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Cloud chats[\*](#shared-limits-pro-20x) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Code Reviews / 5h
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GPT-5.6 Sol</td>
            <td style="text-align:center">200-2,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Terra</td>
            <td style="text-align:center">500-4,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Luna</td>
            <td style="text-align:center">5,000-40,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.5</td>
            <td style="text-align:center">300-1600</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4</td>
            <td style="text-align:center">400-2000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4 mini</td>
            <td style="text-align:center">1200-7000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="4" style="text-align:center">
              <a id="shared-limits-pro-20x" class="footnote">
                *The usage limits for local messages and cloud chats share a
                **five-hour window**. Additional weekly limits may apply.
              </a>
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              For Enterprise/Edu users with flexible pricing, there are no
              fixed rate limits - usage scales with
              [credits](#credits-overview)
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              Enterprise and Edu plans without flexible pricing have the same
              per-seat usage limits as Plus for most features
            </td>
          </tr>
        </tfoot>
      </table>
    

    

      
Business


      <table>
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col" style="text-align:center">
              Local Messages[\*](#shared-limits-business) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Cloud chats[\*](#shared-limits-business) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Code Reviews / 5h
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GPT-5.6 Sol</td>
            <td style="text-align:center">10-100</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Terra</td>
            <td style="text-align:center">25-200</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Luna</td>
            <td style="text-align:center">250-2,000</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.5</td>
            <td style="text-align:center">15-80</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4</td>
            <td style="text-align:center">20-100</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4 mini</td>
            <td style="text-align:center">60-350</td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="4" style="text-align:center">
              <a id="shared-limits-business" class="footnote">
                *The usage limits for local messages and cloud chats share a
                **five-hour window**. Additional weekly limits may apply.
              </a>
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              For Enterprise/Edu users with flexible pricing, there are no
              fixed rate limits - usage scales with
              [credits](#credits-overview)
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              Enterprise and Edu plans without flexible pricing have the same
              per-seat usage limits as Plus for most features
            </td>
          </tr>
        </tfoot>
      </table>
    

    

      
API Key


      <table>
        <thead>
          <tr>
            <th scope="col"></th>
            <th scope="col" style="text-align:center">
              Local Messages[\*](#shared-limits-api-key) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Cloud chats[\*](#shared-limits-api-key) / 5h
            </th>
            <th scope="col" style="text-align:center">
              Code Reviews / 5h
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GPT-5.6 Sol</td>
            <td style="text-align:center">
              [Usage-based](https://platform.openai.com/docs/pricing)
            </td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Terra</td>
            <td style="text-align:center">
              [Usage-based](https://platform.openai.com/docs/pricing)
            </td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.6 Luna</td>
            <td style="text-align:center">
              [Usage-based](https://platform.openai.com/docs/pricing)
            </td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.5</td>
            <td style="text-align:center">
              [Usage-based](https://platform.openai.com/docs/pricing)
            </td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4</td>
            <td style="text-align:center">
              [Usage-based](https://platform.openai.com/docs/pricing)
            </td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
          <tr>
            <td>GPT-5.4 mini</td>
            <td style="text-align:center">
              [Usage-based](https://platform.openai.com/docs/pricing)
            </td>
            <td style="text-align:center">Not available</td>
            <td style="text-align:center">Not available</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="4" style="text-align:center">
              <a id="shared-limits-api-key" class="footnote">
                *The usage limits for local messages and cloud chats share a
                **five-hour window**. Additional weekly limits may apply.
              </a>
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              For Enterprise/Edu users with flexible pricing, there are no
              fixed rate limits - usage scales with
              [credits](#credits-overview)
            </td>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              Enterprise and Edu plans without flexible pricing have the same
              per-seat usage limits as Plus for most features
            </td>
          </tr>
        </tfoot>
      </table>
    


  </ContentSwitcher>



Usage limits are shared with other agentic features once pricing for those
features is effective. This currently includes [ChatGPT for
Excel](https://help.openai.com/articles/20001063) on Plus and Pro.

Speed configurations increase credit consumption for all applicable models, so
they also use included limits faster. Fast mode consumes credits at a higher
rate for supported models. See [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) for supported models and
rates. Image generations also use included limits ~3-5x faster on average,
depending on image quality and size. GPT-5.3-Codex-Spark is in research preview
for ChatGPT Pro users only, and isn't available in the API at launch. Because it
runs on specialized low-latency hardware, usage is governed by a separate usage
limit that may adjust based on demand.

### ChatGPT Voice in Desktop

ChatGPT Voice on desktop uses a separate, plan-dependent allowance measured in
rolling five-hour windows. Tasks started through Voice use your existing Codex
usage budget. ChatGPT notifies you when you reach either limit.

ChatGPT Voice in Desktop uses a duplex model: GPT-Live manages the live
conversation, while GPT-5.6 Terra starts and coordinates tasks in the app.

- **Plus:** Approximately 15–30 minutes
- **Pro 5x ($100/month):** Approximately 1–2.5 hours
- **Pro 20x ($200/month):** Unlimited voice access
- **Business:** Approximately 45 minutes
- **Enterprise / Edu (legacy):** Approximately 45 minutes

Unlimited voice access doesn't make Codex tasks unlimited. Tasks started through
ChatGPT Voice continue to use your existing Codex usage budget.

For Business, Edu, and Enterprise workspaces with credit-based or pay-as-you-go
billing, Desktop voice costs approximately 6 credits per minute. ChatGPT Voice
in Desktop is not available via API Key currently.

### What happens when you hit usage limits?

We want you to be able to complete work already in progress. If you reach your
usage limits during an active turn, the agent will be able to continue working
on that turn, subject to fair use limits.

ChatGPT Plus and Pro users who reach their usage limit can purchase additional
credits to continue working without needing to upgrade their existing plan.

Business, Edu, and Enterprise plans with [flexible
pricing](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)
can purchase additional workspace credits to continue working.

If you are approaching usage limits, you can also switch to a smaller model to
make your usage limits last longer.

All users may also run extra local chats using an API key, with usage charged at
[standard API rates](https://platform.openai.com/docs/pricing).

<a id="image-generation-usage-limits"></a>

### How does image generation count toward usage limits?

Image generation counts toward the same general usage limits as local
messages and cloud chats. Image generations use included limits 3-5x faster on
average than similar turns without image generation, depending on
image quality and size. After you reach your included limits, image generation
also draws from [credits](#credits-overview).

Image generation isn't available on the Free plan. When you use Codex with an
API key, API pricing applies to image generation instead of included ChatGPT
usage limits.

### Where can I see my current usage limits?

You can find your current limits in the [usage
dashboard](https://chatgpt.com/codex/settings/usage). If you want to see your
remaining limits during an active Codex CLI session, you can use `/status`.

Check the dashboard every week or two to understand your pace and remaining
capacity. If usage is higher than expected, consider whether a smaller model or
tighter task scope would still produce a useful result.

### What are tokens and credits?

Tokens are small units of information that ChatGPT reads and writes. Your
prompt, files, chat history, tool results, and ChatGPT's response all
use tokens.

Credits translate token usage into a simpler unit for tracking and managing
consumption. The credit cost varies by model, context, reasoning, and tools.
After you reach your included limits, available credits let you continue
working.

Usage is calculated in credits per million input tokens, cached input tokens,
and output tokens. [Learn more about
tokens](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them).

The rate card below shows the credit cost per million tokens for models and
features.

A small subset of Enterprise customers should continue using the legacy rate
card until we migrate you to the new token-based pricing. For more information,
[contact OpenAI
sales](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex).



  <table>
    <thead>
      <tr>
        <th scope="col">Credits per 1M tokens</th>
        <th scope="col" style="text-align:center">
          Input Tokens
        </th>
        <th scope="col" style="text-align:center">
          Cached input tokens
        </th>
        <th scope="col" style="text-align:center">
          Output Tokens
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>GPT-5.6 Sol</td>
        <td style="text-align:center">125 credits</td>
        <td style="text-align:center">12.5 credits</td>
        <td style="text-align:center">750 credits</td>
      </tr>
      <tr>
        <td>GPT-5.6 Terra</td>
        <td style="text-align:center">50 credits</td>
        <td style="text-align:center">5 credits</td>
        <td style="text-align:center">300 credits</td>
      </tr>
      <tr>
        <td>GPT-5.6 Luna</td>
        <td style="text-align:center">5 credits</td>
        <td style="text-align:center">0.5 credits</td>
        <td style="text-align:center">30 credits</td>
      </tr>
      <tr>
        <td>GPT-5.5</td>
        <td style="text-align:center">125 credits</td>
        <td style="text-align:center">12.50 credits</td>
        <td style="text-align:center">750 credits</td>
      </tr>
      <tr>
        <td>GPT-5.4</td>
        <td style="text-align:center">62.50 credits</td>
        <td style="text-align:center">6.250 credits</td>
        <td style="text-align:center">375 credits</td>
      </tr>
      <tr>
        <td>GPT-5.4 mini</td>
        <td style="text-align:center">18.75 credits</td>
        <td style="text-align:center">1.875 credits</td>
        <td style="text-align:center">113 credits</td>
      </tr>
      <tr>
        <td>GPT-5.3-Codex-Spark</td>
        <td colspan="3" style="text-align:center">
          research preview
        </td>
      </tr>
      <tr>
        <td>GPT-Image-2 (image)</td>
        <td style="text-align:center">200 credits</td>
        <td style="text-align:center">50 credits</td>
        <td style="text-align:center">750 credits</td>
      </tr>
      <tr>
        <td>GPT-Image-2 (text)</td>
        <td style="text-align:center">125 credits</td>
        <td style="text-align:center">31.25 credits</td>
        <td style="text-align:center">250 credits</td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td colspan="4" style="text-align:center">
          GPT-5.6 usage averages 5-40 credits per message.
        </td>
      </tr>
      <tr>
        <td colspan="4" style="text-align:center">
          Fast mode consumes credits at a higher rate for supported models. See
          [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) for rates.
        </td>
      </tr>
    </tfoot>
  </table>



Speed configurations will increase credit consumption for all models that apply.
Fast mode consumes credits at a higher rate for supported models. See
[Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) for supported models and rates.

[Learn more about credits in ChatGPT Plus and
Pro.](https://help.openai.com/en/articles/12642688)

[Learn more about credits in ChatGPT Business, Enterprise, and
Edu.](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)

### What counts as Code Review usage?

Code Review usage applies only when Codex runs reviews through GitHub—for
example, when you tag `@Codex` for review in a pull request or enable automatic
reviews on your repository. Reviews run locally or outside of GitHub count
toward your general usage limits.

### What can I do to make my usage limits last longer?

The usage limits and credits above are average rates. You can try the following
tips to maximize your limits:

- **Control the size of your prompts.** Be precise with the instructions you
  give the agent, but remove unnecessary context.
- **Limit source material.** Provide only relevant files and, when possible,
  narrow the sources or date range.
- **Match the output to the need.** Define the audience, format, and length, and
  separate required work from optional improvements.
- **Reduce the size of your AGENTS.md.** If you work on a larger project, you
  can control how much context you inject through AGENTS.md files by [nesting
  them within your repository](https://learn.chatgpt.com/docs/agent-configuration/agents-md#layer-project-instructions).
- **Limit the number of MCP servers you use.** Every
  [MCP](https://learn.chatgpt.com/docs/extend/mcp) server adds more context to your messages and uses
  more of your limit. Disable MCP servers when you don’t need them.
- **Switch to a smaller model for routine tasks.** Using GPT-5.6 Terra or
  GPT-5.6 Luna can extend your local-message usage limits, depending on the
  model you switch from.

For guidance on choosing and scoping tasks, see [Use Work
efficiently](https://learn.chatgpt.com/docs/prompting#use-work-efficiently).

## Feature availability

<CodexPlanFeatureMatrix
  client:load
  data={{
    plans: [
      { id: "plus", shortLabel: "Plus", label: "ChatGPT Plus" },
      { id: "pro", shortLabel: "Pro", label: "ChatGPT Pro" },
      {
        id: "business",
        shortLabel: "Business",
        label: "ChatGPT Business",
      },
      {
        id: "enterprise",
        shortLabel: "Enterprise",
        label: "Enterprise / Education",
      },
      { id: "api", shortLabel: "API Key", label: "API Key" },
    ],
    sections: [
      {
        title: "Access and surfaces",
        features: [
          {
            name: "Codex cloud",
            href: "/codex/cloud",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "ChatGPT Work on the web",
            href: "/codex/get-started-with-work",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "ChatGPT desktop app for local chats",
            href: "/codex/app",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Codex CLI",
            href: "/codex/cli",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "IDE extension",
            href: "/codex/ide",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Codex SDK, `codex exec`, and scriptable workflows",
            shortName: "Codex SDK and scripting",
            href: "/codex/codex-sdk",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Codex access tokens for trusted automation",
            shortName: "Automation access tokens",
            href: "/codex/enterprise/access-tokens",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "ChatGPT for Excel",
            href: "https://help.openai.com/articles/20001063",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
        ],
      },
      {
        title: "Models and multimodal",
        features: [
          {
            name: "GPT-5.6",
            href: "/codex/models",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Fast mode",
            href: "/codex/agent-configuration/speed",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Codex-Spark research preview",
            href: "/codex/models",
            availability: {
              plus: "unavailable",
              pro: "available",
              business: "unavailable",
              enterprise: "unavailable",
              api: "unavailable",
            },
          },
          {
            name: "Image generation and editing",
            href: "/codex/image-generation?surface=app",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Voice dictation",
            href: "/codex/prompting#use-voice-dictation",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "ChatGPT Voice",
            href: "/codex/features/voice",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Web search",
            href: "/codex/web-search?surface=app",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
        ],
      },
      {
        title: "Local features",
        features: [
          {
            name: "Local code review with `/review`",
            shortName: "Local code review",
            href: "/codex/prompting#do-a-local-code-review",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Auto-review for approval requests",
            href: "/codex/sandboxing/auto-review",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Sandboxing and permission controls",
            href: "/codex/permissions",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Project and standalone scheduled tasks",
            shortName: "Scheduled tasks",
            href: "/codex/automations",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Scheduled tasks",
            href: "/codex/automations",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Worktrees and built-in Git tools",
            shortName: "Built-in Git tools",
            href: "/codex/environments/git-worktrees",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Local environments and repeatable actions",
            shortName: "Repeatable actions",
            href: "/codex/environments/local-environment",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Appshots",
            href: "/codex/appshots",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "unavailable",
              api: "available",
            },
          },
        ],
      },
      {
        title: "Browser and remote control",
        features: [
          {
            name: "Built-in browser previews and comments",
            shortName: "Built-in browser",
            href: "/codex/browser?surface=app",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Computer Use in the browser",
            href: "/codex/browser?surface=app#app-computer-use-in-the-browser",
            availability: {
              plus: "limited",
              pro: "limited",
              business: "limited",
              enterprise: "limited",
              api: "limited",
            },
          },
          {
            name: "Use ChatGPT with Chrome",
            shortName: "Chrome browser control",
            href: "/codex/chrome-extension",
            availability: {
              plus: "limited",
              pro: "limited",
              business: "limited",
              enterprise: "limited",
              api: "limited",
            },
          },
          {
            name: "Computer Use",
            href: "/codex/computer-use",
            limitedFootnote: "region",
            availability: {
              plus: "limited",
              pro: "limited",
              business: "limited",
              enterprise: "limited",
              api: "limited",
            },
          },
          {
            name: "Record & Replay (macOS)",
            shortName: "Record & Replay",
            href: "/codex/extend/record-and-replay",
            limitedFootnote: "region",
            availability: {
              plus: "limited",
              pro: "limited",
              business: "limited",
              enterprise: "limited",
              api: "limited",
            },
          },
          {
            name: "SSH remote connections",
            shortName: "SSH remote",
            href: "/codex/remote-connections#connect-to-an-ssh-host",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Mobile remote control",
            href: "/codex/remote-connections",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Browser in ChatGPT Web",
            href: "/codex/browser?surface=web",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
        ],
      },
      {
        title: "Customization and extensions",
        features: [
          {
            name: "Custom instructions with `AGENTS.md`",
            shortName: "Custom instructions",
            href: "/codex/agent-configuration/agents-md",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Skills",
            href: "/codex/build-skills",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Plugins",
            href: "/codex/plugins",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "limited",
            },
            limitedFootnote: "plugins",
          },
          {
            name: "Plugin sharing",
            href: "https://developers.openai.com/plugins/build/plugins#share-a-local-plugin-with-your-workspace",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Connectors",
            href: "/codex/plugins",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "MCP",
            href: "/codex/extend/mcp",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Subagents and custom agents",
            shortName: "Subagents",
            href: "/codex/agent-configuration/subagents",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Memories",
            href: "/codex/customization/memories",
            availability: {
              plus: "limited",
              pro: "limited",
              business: "limited",
              enterprise: "limited",
              api: "limited",
            },
          },
          {
            name: "Chronicle",
            href: "/codex/customization/chronicle",
            availability: {
              plus: "unavailable",
              pro: "limited",
              business: "unavailable",
              enterprise: "unavailable",
              api: "unavailable",
            },
          },
        ],
      },
      {
        title: "Cloud and integrations",
        features: [
          {
            name: "Codex cloud chats",
            shortName: "Cloud chats",
            href: "/codex/cloud",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Cloud environments and setup scripts",
            shortName: "Cloud environments",
            href: "/codex/environments/cloud-environment",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Cloud agent internet access controls",
            shortName: "Internet controls",
            href: "/codex/cloud/internet-access",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Sites",
            href: "/codex/sites",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "GitHub issue and PR delegation with `@codex`",
            shortName: "GitHub delegation",
            href: "/codex/third-party/github#give-codex-other-tasks",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "GitHub code review and automatic PR reviews",
            shortName: "GitHub PR reviews",
            href: "/codex/third-party/github",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Slack cloud integration",
            shortName: "Slack integration",
            href: "/codex/third-party/slack",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Linear cloud integration",
            shortName: "Linear integration",
            href: "/codex/third-party/linear",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
        ],
      },
      {
        title: "Admin, security, and analytics",
        features: [
          {
            name: "SAML SSO, MFA, and workspace user management",
            shortName: "Workspace management",
            href: "/codex/enterprise/admin-setup",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "`requirements.toml` managed config",
            shortName: "`requirements.toml` config",
            href: "/codex/enterprise/managed-configuration",
            availability: {
              plus: "available",
              pro: "available",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Cloud-managed config policies",
            shortName: "Cloud-managed policies",
            href: "/codex/enterprise/managed-configuration#cloud-managed-requirements",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "available",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "ChatGPT workspace RBAC and custom roles",
            shortName: "RBAC and roles",
            href: "/codex/enterprise/roles-and-workspace-permissions",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "SCIM, EKM, and domain verification",
            shortName: "SCIM, EKM, and domains",
            href: "/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Enterprise retention and residency controls",
            shortName: "Retention and residency",
            href: "/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "No training on API or business data by default",
            shortName: "No default training",
            href: "https://openai.com/business-data/",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "available",
              enterprise: "available",
              api: "available",
            },
          },
          {
            name: "Analytics dashboard",
            href: "/codex/enterprise/workspace-analytics",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Analytics API",
            href: "/codex/enterprise/analytics-api",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Compliance API and audit logs",
            shortName: "Compliance and audit logs",
            href: "/codex/enterprise/compliance-api",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
          {
            name: "Codex Security for connected GitHub repositories",
            shortName: "Codex Security",
            href: "/codex/security",
            availability: {
              plus: "unavailable",
              pro: "unavailable",
              business: "unavailable",
              enterprise: "available",
              api: "unavailable",
            },
          },
        ],
      },
    ],
  }}
/>

<div
  id="codex-plan-region-limits"
  className="not-prose mt-3 text-sm text-secondary"
>
  <sup>*</sup> Feature is currently limited to only specific regions. Check the
  individual feature documentation to learn more about geo restrictions.


<div
  id="codex-plan-plugin-limits"
  className="not-prose mt-1 text-sm text-secondary"
>
  <sup>†</sup> Some first party plugins are not available.