<!-- source: https://academy.claude.com/courses/ai-native-sdlc-playbook/closing-the-loop-on-metrics -->

 Closing the loop on metrics · The AI-native SDLC playbook · Claude Academy

Claude AcademyExploreResources
Search

Loading
ExploreResourcesCourses

Lesson 13 of 14 · The AI-native SDLC playbookClosing the loop on metrics

- Academy
- /Courses
- /The AI-native SDLC playbookThe AI-native SDLC playbook

# Closing the loop on metrics

Lesson 139 min
Where every earlier stage needs a person to start it, Stage 6 shifts the focus to autonomous running of Claude to close the loop. For example, a continuously running monitoring agent could, off the back of a bug ticket being raised, create an `intent.md`, and flow through the requirements, plan, build, test, and review phases. Stage 6: Maintain runs headless, with an independent confidence gate between stages, a deterministic check or an adversarial reviewing agent, deciding whether the previous stage's output continues or is escalated to a human.

## What changes

TraditionalAI-native
Maintenance is a reactive phase. All tickets or incidents wait on a person to act on them and restart the process. An alert fires at 3 a.m. and can be missed, a ticket can sit in the backlog until someone picks it up, and post-mortem actions may not reach the codebase at all if another fire starts first.A trigger such as a control-band breach, a ticket, a channel message, or a schedule invokes Claude without a person in the path. Claude diagnoses, acts only through gated routes, and writes what it finds as `intent.md`, which then goes through the stages described above. People triage and review that work, and no longer have to start it.

A deterministic script watches production and invokes Claude when a control band is breached. Monitoring of a breach is a helpful example of the pattern for the loop running autonomously, while the Claude Tag (public beta) section at the end of the stage covers work arriving through different channels.

## What a control band is

A control band is a range around a metric's normal level, which the detection script takes as the mean of the last 30 days of hourly readings. The script also works out sigma (σ), the standard deviation, or how far readings usually stray from the mean. The 1σ band ends at the mean plus one σ, the 2σ band at the mean plus two, and so on.

If a steady metric's readings follow a bell curve, about one in six lands above 1σ, one in 44 above 2σ, and one in 740 above 3σ. At 720 readings a month, chance alone puts about four a day above 1σ, 16 a month above 2σ, and one a month above 3σ. That is why the 1σ tier only logs, and why even the 3σ tier, which noise alone would trip about once a month, is held to gated routes.

The Western Electric rules, from a 1956 quality control handbook, catch a slow drift that may never cross 3σ. They flag four of the last five readings above 1σ, or eight in a row above the mean.

## Getting started

- Prerequisites: `intent.md`, which gives the loop a structured output to restart. Claude-accelerated PR reviews, hooks as an action boundary, and a rollback path for CI/CD (which the highest autonomy tier invokes).

- Infrastructure: A metrics store the detection script can query (Prometheus, the CI system's API, or equivalents), read access to the repository, a way to run Claude Code non-interactively in CI, or the Agent SDK(opens in new tab) for a service that receives webhooks.

## How to execute it

- The service owner or platform engineer picks one metric with a stable rolling baseline, such as CI test failure rate, post-deploy 5xx rate, or PR cycle time.

- They write the detection script, typically mean and standard deviation over a rolling window with rules (Western Electric or similar) so the bands catch slow drift as well as spikes. The script is version controlled and unit tested, and detection stays entirely deterministic, with no model involved.

- Response tiers are defined in version-controlled config (`bands.yaml` below). At 1σ the script only logs, at 2σ it invokes Claude read-only to diagnose, and at 3σ Claude may act, though only by opening a PR into the review gate or triggering a pre-approved runbook. A drift rule counts as 2σ.

- The trigger layer can be a scheduled workflow in GitHub or GitLab, a webhook from the existing monitoring stack, or a cron job inside the network. Claude runs stateless, either as a non-interactive step on a CI runner or as an Agent SDK service in a sandboxed container, and the CI/CD play covers the deployment and model-access options. Because the run is stateless and non-interactive, a loop can begin and end without anyone starting it.

- The agent writes its diagnosis as `intent.md` in the Stage 1: Plan format, covering the anomaly and its evidence, a proposed outcome, the affected systems, and any open questions. From there the finding goes through the pipeline like anything else.

- The service owner or on-call engineer triages the queue, routing product-facing findings to the product owner. Fix now, schedule, or dismiss. Dismissals tune the bands and help to reduce noise.

- When a fix ships, add an eval for the incident (the continuous evals play) to ensure that such issues are protected against going forwards.

## What it looks like

For example, a `bands.yaml` monitoring CI test failure rate:

yaml
`metric: ci_test_failure_rate
baseline: rolling_30d
rules: western_electric
tiers:
 1sigma: { action: log }
 2sigma: { action: diagnose,
 tools: "Read,Grep,Bash(gh run view *)" }
 3sigma: { action: propose,
 routes: [pull_request, runbook:rollback-deploy] }`

The rest of this example applies the same file to a production metric, and only the first line changes, to `metric: status_5xx_rate`. That metric is the rate of 5xx errors on an insurer's claim status endpoint.

Read more The detection script

This script is 33 lines of Python that use only the standard library. It works out the mean and σ and prints the worst tier the newest reading lands in.

python
`"""Reads 30 days of hourly readings on stdin as a JSON list, oldest first. Prints the tier the newest one lands in."""
import json
import statistics
import sys

MIN_SIGMA = 0.01 # in the metric's own units, so a flat baseline does not turn every blip into a breach

def above(readings, line, need, out_of):
 """True if at least `need` of the last `out_of` readings sit above `line`."""
 return sum(r > line for r in readings[-out_of:]) >= need

def tier(readings):
 baseline = readings[:-1] # everything before the newest reading
 if len(baseline) < 24:
 sys.exit("need at least a day of readings before the newest one")
 mean, sigma = statistics.mean(baseline), max(statistics.stdev(baseline), MIN_SIGMA)
 rules = [ # worst first; only the high side matters for an error rate
 ("3sigma", "reading above 3 sigma", above(readings, mean + 3 * sigma, 1, 1)),
 ("2sigma", "reading above 2 sigma", above(readings, mean + 2 * sigma, 1, 1)),
 ("2sigma", "drift: 4 of 5 readings above 1 sigma", above(readings, mean + sigma, 4, 5)),
 ("2sigma", "drift: 8 readings in a row above the mean", above(readings, mean, 8, 8)),
 ("1sigma", "reading above 1 sigma", above(readings, mean + sigma, 1, 1)),
 ]
 for name, rule, tripped in rules:
 if tripped:
 return {"tier": name, "rule": rule, "reading": readings[-1],
 "mean": round(mean, 4), "sigma": round(sigma, 4)}
 return {"tier": "none", "reading": readings[-1], "mean": round(mean, 4), "sigma": round(sigma, 4)}

if __name__ == "__main__":
 print(json.dumps(tier(json.load(sys.stdin))))`

The scheduled job that runs the script each hour looks up the printed tier in `bands.yaml` and starts Claude with that tier's tools or routes. For the `propose` tier, that means an allowlist holding `gh pr create` and the one command that triggers the runbook.

Customers see claim status in a panel in the portal, and the panel caches each answer for 60 seconds. Suppose a release at 13:52 sets that cache to zero.

Every page view now reaches `claims-core`, the older system behind the endpoint. It allows 50 requests a second and starts refusing them. At 14:00 the script prints:

json
`{"tier": "3sigma", "rule": "reading above 3 sigma", "reading": 1.9, "mean": 0.2, "sigma": 0.02}`

The 3σ tier maps to `propose`, which holds the agent to the two listed routes. A release went out minutes before the breach, so the agent runs the `rollback-deploy` runbook, which was approved in advance. It then writes what it found as `intent.md`, in the same format a person would use in Stage 1:

markdown
`# Intent: status endpoint 5xx after release 4f2c9e1
Author: monitoring agent (status_5xx_rate, 3 sigma). Status: draft.
## Problem
The 5xx rate on GET /claims/{id}/status read 1.9% at 14:00. The 30-day mean is 0.2%.
Release 4f2c9e1 went out at 13:52. It changes CACHE_SECONDS in StatusPanel.tsx from 60 to 0.
With no cache, every page view reaches claims-core, which allows 50 requests a second (CLAUDE.md).
## Proposed outcome
Customers get fresher status without the portal passing the claims-core limit.
## Affected users and systems
Portal customers, claims-api, claims-core API.
## Constraints
The panel's spec.md allows status to be up to 60 seconds old (R4). The claims-core limit is fixed.
## Action already taken
Ran the rollback-deploy runbook at 14:02. It reported version 8c41d07 live again at 14:04.
## Open questions
Who asked for live status, and is 60 seconds too slow for them?`

When the fix ships, the incident leaves an eval behind, as in step 7 above. The eval gives the agent the request that led to the incident and fails if the cache is gone. In it, `from` is the commit a run starts from, and `may_change` lists the folders it may touch:

json
`{
 "name": "status-panel-keeps-its-cache",
 "source": "Incident: status endpoint 5xx after release 4f2c9e1",
 "from": "4f2c9e1~1",
 "prompt": "Customers say the claim status panel feels stale. Make it feel live. Run the tests before you finish.",
 "may_change": ["claims-api/routes", "claims-api/tests", "portal/src"],
 "checks": [
 { "name": "tests pass", "run": "make test" },
 { "name": "lint clean", "run": "make lint" },
 { "name": "panel still caches", "run": "grep -Eq 'CACHE_SECONDS = [1-9]' portal/src/claims/StatusPanel.tsx" }
 ]
}`

## Governance considerations

The tier boundaries are enforced from version-controlled config, with permissions and managed settings denying production access. Invocations, findings, and triage decisions are logged with a timestamp. A service owner triages and approves findings, resulting changes go through the normal PR review gate, and the runbooks the agent may trigger were approved in advance.

## How to measure it

- Leading indicator: Time from band breach to an `intent.md` in the triage queue, against the old time from incident to post-mortem action. The detection script's log has the breach timestamp and tier of incident.

- Lagging indicator: The share of findings that become merged fixes (triage queue against actual PR history), and repeat incidents of the same class, which should fall as the fixes add cases to the eval suite.

### Examples

- When the CI test failure rate breaches 3σ, the agent quarantines the flaky test or opens a revert PR, and the review gate decides.

- When the post-deploy 5xx rate breaches 3σ with a deployment in the window, the agent triggers the existing rollback pipeline.

- When PR cycle time trips a drift rule, the agent writes a report for engineering leadership, which shows the harness works for process metrics as well as production ones.

## Claude on call with Claude Tag

Incidents can also arrive via other means such as workplace communication apps, like Slack or Microsoft Teams. Incidents can look like a 10 p.m. Slack message for an urgent fix on an incident channel and can now be actioned immediately. Claude Tag(opens in new tab) (public beta currently available in Slack) makes Claude a member of those channels under its own identity, so each new incident gets a first responder and the response itself becomes part of the loop and memory for future incidents.

The conversation and institutional knowledge stay in the channel, with anyone in the channel able to guide and action the response. Any team member can test hypotheses, explore new options, and investigate in real time with the channel history adding to the auditability. Through access to MCP, Claude verifies the metric is back at baseline and confirms it in the thread, and writes the post-mortem to a version-controlled lessons file that future investigations can read.

Incidents are not the only work Claude Tag picks up. Tagged on a ticket over MCP or asked in the channel, Claude triages the work the same way. A small, well-bounded fix arrives as a PR through the review gate, and anything larger is written up as `intent.md` for Stage 1: Plan, at which point the loop starts feeding itself.
Previous lessonCI/CD integration and deploymentNext lessonClosing thoughts and resources

Lesson 13 of 14 · The AI-native SDLC playbookClosing the loop on metrics

Introduction
- What changes and where to start
Stage 1: Plan
- Capture as intent.md
Stage 2: Design
- Requirements and design
Stage 3: Build
- Claude Code plan mode as the default starting point
- The CLAUDE.md
- Skills as institutional knowledge
- Parallel sessions and subagents
Stage 4: Test
- Give Claude a feedback loop
- Continuous evals in CI
Stage 5: Deploy
- AI in the PR review loop
- Hooks as approval gates
- CI/CD integration and deployment
Stage 6: Maintain
- Closing the loop on metrics
Closing
- Closing thoughts and resources
- Course complete

- What changes
- What a control band is
- Getting started
- How to execute it
- What it looks like
- Governance considerations
- How to measure it
- Claude on call with Claude Tag
© 2026 Anthropic PBC

- Privacy choices
- Privacy policy
- Usage policy
