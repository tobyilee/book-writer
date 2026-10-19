<!-- source: https://academy.claude.com/courses/ai-native-sdlc-playbook/ai-in-the-pr-review-loop -->

 AI in the PR review loop · The AI-native SDLC playbook · Claude Academy

Claude AcademyExploreResources
Search

Loading
ExploreResourcesCourses

Lesson 10 of 14 · The AI-native SDLC playbookAI in the PR review loop

- Academy
- /Courses
- /The AI-native SDLC playbookThe AI-native SDLC playbook

# AI in the PR review loop

Lesson 105 min
Claude both gives and receives reviews. It reviews incoming PRs against the organization's policies and addresses review comments on its own PRs. This allows engineers to focus on behavior in their PR review, which boils down to judging intent and risk.

## What changes

TraditionalAI-native
Review capacity is planned around human output. A PR waits for a reviewer to read all of it, review quality varies with the reviewer's load, and the author chases while the backlog grows.All PRs get an identical set of review passes, with findings ranked by severity. Human attention moves up a level, to whether the change does what the plan intended and whether the risk is acceptable.

## Getting started

- Prerequisites: An updated `CLAUDE.md` file from Stage 3: Build, skills, if the review passes are to enforce written policies, and defined subagents.

- Infrastructure: A repo with the Claude integration installed, either the managed Code Review(opens in new tab) (research preview) service enabled by an admin or the claude-code-action running in your own CI, with model calls through Amazon Bedrock, Google Cloud's Vertex AI, or Microsoft Foundry where needed (the CI/CD play covers the deployment options). Branch protection policies that require a code owner's approval are also worthwhile.

## How to execute it

- The managed Code Review service is the fastest start. An admin enables it and selects repositories. Run the review in your own CI with the claude-code-action when you need control of the pipeline or want API calls routed through your own cloud agreement (the CI/CD play covers that plumbing).

- The tech lead writes the review policy as `REVIEW.md` at the repo root, divided into the passes the organization cares about: bugs and logical errors; security and vulnerabilities; compliance against the spec (`spec.md` from the requirements play), the implementation plan (`plan.md` from the plan mode play), and design principles. `REVIEW.md` also defines what counts as Important as opposed to a Nit, and what to skip.

- The tech lead sets the human threshold. Findings do not approve or block a PR on their own, and branch protection still requires approval from a code owner. A platform engineer who wants to gate merges on findings can read the severity counts that the check run publishes as a machine-readable tally.

- When a reviewer or the author tags `@claude` on a review comment, Claude addresses the comment and pushes the fix. The PR thread records both the request and the change. This fix loop runs through the claude-code-action. In the managed service, commenting `@claude review` requests a fresh review instead. For PRs Claude opened, go further and let Claude babysit the PR to merge. Teams wrap the loop in a custom slash command that sweeps the unresolved review comments and failing checks on the PR, addresses them, and pushes the fixes, until the PR is green and waiting only on code owner approval.

- Review findings feed back into `CLAUDE.md`. When a review flags a mistake for the second time, the correction goes into `CLAUDE.md` as part of that review, and because review reads `CLAUDE.md`, the mistake is caught from the next PR onwards. Review also flags when a change has made `CLAUDE.md` outdated.

- Once a month the tech lead tunes the setup by rating findings so the reviewer improves and by capping Nit volume in `REVIEW.md`. Generated paths and anything CI already enforces are excluded.

## What it looks like

`REVIEW.md`:

markdown
`# Review instructions
## Passes
Run three passes and tag each finding with its pass:
- Bugs: logic errors, broken edge cases, subtle regressions
- Security: injection risks, authentication gaps, PII in logs
- Compliance: the change matches spec.md, plan.md and our design principles
## What Important means here
Reserve Important for findings that would break behavior, leak data
or breach a policy. Style and naming are nits.
## Cap the nits
Report at most five nits per review; summarize the rest as a count.
## Do not report
Generated files under src/gen/ and anything CI already enforces.`

This example is what the check run lists for a pull request that adds a claim status panel to an insurer's customer portal, where `claims-core` is the older internal system behind the portal's backend:

SeverityFile:LineIssue
Important`portal/src/claims/StatusPanel.tsx:22`Compliance: the panel fetches on every render. `plan.md` says it must cache, because claims-core allows 50 requests a second
Important`claims-api/routes/status.py:31`Security: the error path logs the whole claims-core response, which includes `policy_holder_name`
Nit`claims-api/tests/test_status.py:8`Bugs: no test covers a `paid` claim with no expected date

The first finding exists only because the compliance pass reads the committed `plan.md`, which a reviewer looking at the diff alone would not have open.

## Governance considerations

Separation of duties is preserved, because the agent that wrote the code has no way to approve it. The review policy in `REVIEW.md` is applied to all PRs, and findings, fixes, ratings, and approvals are logged in the PR history, so the PR is the audit record. Approval comes from a human through branch protection, informed by the findings.

## How to measure it

- Leading indicator: Time to first review, which should fall to minutes, and the share of review comments resolved without a human touching the branch, with data stored directly on Git.

- Lagging indicator: Defects and vulnerabilities caught before merge set against those escaping to production, from the PR history and the incident tracker.

Previous lessonContinuous evals in CINext lessonHooks as approval gates

Lesson 10 of 14 · The AI-native SDLC playbookAI in the PR review loop

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
- Getting started
- How to execute it
- What it looks like
- Governance considerations
- How to measure it
© 2026 Anthropic PBC

- Privacy choices
- Privacy policy
- Usage policy
