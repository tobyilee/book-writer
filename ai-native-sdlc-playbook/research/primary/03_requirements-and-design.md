<!-- source: https://academy.claude.com/courses/ai-native-sdlc-playbook/requirements-and-design -->

 Requirements and design · The AI-native SDLC playbook · Claude Academy

Claude AcademyExploreResources
Search

Loading
ExploreResourcesCourses

Lesson 3 of 14 · The AI-native SDLC playbookRequirements and design

- Academy
- /Courses
- /The AI-native SDLC playbookThe AI-native SDLC playbook

# Requirements and design

Lesson 35 min
Once the product owner approves the `intent.md`, Claude takes it and produces a requirements and design spec. This is guided by the organization's skills(opens in new tab) for brand, security, compliance, and UX.

The product owner reviews that spec, but doesn't write it. The goal of this process is to create a spec the engineering team can plan against, with flagged areas of concern.

Front-end work is the clearest example. Once the `intent.md` is accepted, the product owner mocks the design up in Claude Design(opens in new tab) from the `intent.md`, iterates on the mock, and then exports it to Claude Code to build.

## What changes

TraditionalAI-native
Requirements and design are separate phases run by separate teams. Analysts formalize the idea into requirements, and designers then parse those back into a design. The separation exists for accountability, but it is slow and lossy.Both phases happen in a single prompted session. Claude takes `intent.md` and produces a requirements and design spec, constrained by the organization's skills, with areas of concern flagged.

## Getting started

- Prerequisites: Write an `intent.md` file, with brand, security, compliance, and UX policies written as skills.

- Infrastructure: A product owner with Claude access. No engineering skill is required.

## How to execute it

- The product owner opens a session with the organization's skills available and attaches the `intent.md`.

- The product owner's prompt points at the intent, names the constraints, and demands flagged concerns. Run it by hand at first, then codify it as an organization-level slash command. From there make the acceptance of `intent.md` in the intent home the trigger, with a non-interactive job that fires on the merge, runs the pass with the organization's skills loaded, and commits `spec.md` as a pull request (the CI/CD play in Stage 5: Deploy covers the plumbing). From that point the product owner's first involvement is the review.

- The same product owner reviews the spec against the idea. Does the spec solve the stated problem, and are the open questions from `intent.md` answered or carried forward?

- Work through the flagged concerns first as they are the points an analyst would have escalated. The product owner resolves each one with its policy owner before engineering sees the spec.

- Commit `spec.md` alongside `intent.md`. The file pair records what was asked for and what was decided.

- The product owner decides whether the spec and intent progress to build, consulting a technical lead for anything the organization classes as higher risk. A human teammate always makes this call, and accepting the spec is what starts the plan mode play in Stage 3: Build.

## What it looks like

The prompt:

Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.
Copy prompt

The `intent.md` behind this example comes from an insurer that wants customers to see the status of a claim in its portal. In it, `claims-api` is the portal's backend and `claims-core` is the older internal system that holds the claims. The prompt above turns it into this `spec.md`:

markdown
`# Spec: claims status self-service
From: intent.md (J. Ortiz, claims operations). Status: ready for product owner review.
Skills applied: secure-api-review, brand-voice, portal-ux.

## Requirements
- R1. A signed-in customer sees status, next step and expected date for each open claim.
- R2. Status is one of four states: received, in review, approved, paid.
- R3. The response carries those three fields and nothing else.
- R4. What the customer sees is at most 60 seconds old.

## Design
- New endpoint GET /claims/{id}/status in claims-api, behind the gateway JWT.
- claims-api reads the claim from claims-core. The portal never calls claims-core.
- New StatusPanel on the portal claims page. It caches each answer for 60 seconds.

## How each constraint in the intent is met
| Constraint | Met by |
| :---- | :---- |
| No new PII in the portal session | R3. None of the three fields is tagged pii in the schema. |
| Existing authentication only | The gateway JWT. No new login, token or role. |

## Open questions from the intent
- Do third-party loss adjusters need access too? Not answered. Carried forward as concern 1.

## Areas of concern
1. Loss adjusters have no portal account. Giving them access breaks "existing
 authentication only", so they are left out of this spec. Owner: security.
2. The portal-ux skill says every status shows a date. The brand-voice skill says
 never to state a payment date as a commitment. I cannot satisfy both as written.
 Proposed label: "Estimated date". Owner: compliance.
3. claims-core allows 50 requests a second. The 60-second cache should keep the
 portal under that, but nobody has load tested it. Owner: claims-core team.`

The requirements are numbered so the plan and the review can cite them. Concern 2 sets two skills against each other, the kind of clash the prompt tells Claude to flag.

## Governance considerations

Instead of policy conflicts being discovered in a review weeks later, the live policy is read and applied while the spec is written. The organization's skills are applied as constraints on the spec. The spec, the prompt that produced it, and the skill versions in force are all logged in version control. The product owner signs off on the spec, and routes flagged concerns to the named policy owners.

## How to measure it

- Leading indicator: Elapsed time between the `intent.md` commit and the `spec.md` commit for the same change (two Git timestamps), compared with the old requirements-plus-design cycle.

- Lagging indicator: Requirements rework after build starts. Count `spec.md` commits dated after the first `plan.md` commit for the same change. Git log will give this directly.

Previous lessonCapture as intent.mdNext lessonClaude Code plan mode as the default starting point

Lesson 3 of 14 · The AI-native SDLC playbookRequirements and design

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
