<!-- source: https://academy.claude.com/courses/ai-native-sdlc-playbook/claude-md -->

 The CLAUDE.md · The AI-native SDLC playbook · Claude Academy

Claude AcademyExploreResources
Search

Loading
ExploreResourcesCourses

Lesson 5 of 14 · The AI-native SDLC playbookThe CLAUDE.md

- Academy
- /Courses
- /The AI-native SDLC playbookThe AI-native SDLC playbook

# The CLAUDE.md

Lesson 53 min
`CLAUDE.md` gives Claude the context a new joiner would need, covering conventions, commands, architecture, and the mistakes the team sees most often. Knowledge that used to sit in people's heads and on wikis becomes a file the agent reads at the start of every session, maintained by the whole team and iterated on whenever a mistake is made.

## Getting started

- Prerequisites: None.

- Infrastructure: A repo, Claude Code installed, and one engineer who knows the codebase well.

## How to execute it

- Run `/init` in the repo. Claude generates a starting `CLAUDE.md` from what it finds.

- Cut the generated file down to what a new joiner would need on day one. Keep the build, test, and lint commands, the conventions that matter, and the things Claude keeps getting wrong.

- Check `CLAUDE.md` into Git at the repo root so the whole team shares one version and changes are reviewed like code.

- A working rule helps here. When Claude makes a mistake twice, the correction goes into `CLAUDE.md`.

- Keep it under a page, because Claude reads all of it at the start of a session and anything stale is taking up context for no benefit.

## What it looks like

This `CLAUDE.md` belongs to the repo for an insurer's customer portal. The older internal system that holds the claims is `claims-core`, and `intent/` keeps the planning files for each change.

`CLAUDE.md`:

markdown
`# Claims portal
## Commands
- Build: make build
- Test: make test (unit), make itest (integration, needs docker)
- Lint: make lint (runs in CI; fix before pushing)
- Run: make run (portal on :3000, claims-api on :8000)
## Conventions
- claims-api is Python 3.12 and FastAPI. portal is TypeScript and React.
- Every endpoint needs a test in claims-api/tests.
- Dates cross the API as ISO 8601, never as formatted text.
## Architecture
- portal/ is the customer site, claims-api/ is its backend, and
 intent/ holds the intent.md, spec.md and plan.md for each change.
- Only claims-api talks to claims-core. The portal never calls it.
- claims-core allows 50 requests a second. Cache reads; never poll it.
## Things Claude gets wrong
- Do not log request or response bodies in claims-api; they can hold PII.
- Do not bump dependency versions; the platform team owns them.`

## Governance considerations

`CLAUDE.md` is version controlled, so the instructions the agent works to are reviewable and auditable. Team conventions are applied through the file, changes to it are logged in Git history, and code owners approve those changes in PR review.

## How to measure it

- Leading indicator: How often Claude repeats a mistake `CLAUDE.md` should have caught. The corrections or changes to the `CLAUDE.md` should be tracked within the Git history.

- Lagging indicator: Time to first merged PR for a new member of the team from PR history.

Previous lessonClaude Code plan mode as the default starting pointNext lessonSkills as institutional knowledge

Lesson 5 of 14 · The AI-native SDLC playbookThe CLAUDE.md

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

- Getting started
- How to execute it
- What it looks like
- Governance considerations
- How to measure it
© 2026 Anthropic PBC

- Privacy choices
- Privacy policy
- Usage policy
