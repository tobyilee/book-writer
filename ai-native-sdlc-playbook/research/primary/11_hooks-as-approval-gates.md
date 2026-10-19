<!-- source: https://academy.claude.com/courses/ai-native-sdlc-playbook/hooks-as-approval-gates -->

 Hooks as approval gates · The AI-native SDLC playbook · Claude Academy

Claude AcademyExploreResources
Search

Loading
ExploreResourcesCourses

Lesson 11 of 14 · The AI-native SDLC playbookHooks as approval gates

- Academy
- /Courses
- /The AI-native SDLC playbookThe AI-native SDLC playbook

# Hooks as approval gates

Lesson 117 min
The build phase used hooks as guardrails, allowing or blocking actions with no human involved (Stage 3: Build). A hook can also ask, pausing the action until the person running the session confirms it. When the approver is someone else, such as a release manager, the hook looks for their recorded approval and blocks until it exists.

The play sits in Stage 5: Deploy because the release gate is the clearest case, but hooks are not deploy-specific: they run wherever Claude acts. For example, hooks can block edits to migrations and infra without a change ticket during Stage 3: Build, and stop the agent editing test files during a fix task in Stage 4: Test.

## Getting started

- Prerequisites: None.

- Infrastructure: A written list of the approvals the change process requires.

## How to execute it

- Engineering leadership, with change management and compliance, lists the human approval gates that must survive, such as change management sign-off, release authorization, and edits to protected paths.

- The platform engineer expresses each gate as a hook, a script that runs before Claude acts that can allow, ask, or block.

- Team hooks go in `.claude/settings.json` in Git, and non-negotiable hooks go in managed settings owned by the platform or IT admin, where individual engineers cannot switch them off.

- A block should explain itself, so when a hook stops an action, the reason and the route to approval appear in Claude's output.

## What it looks like

This example is an insurer's customer portal, released to dev, staging, and production. Deployment runs through MCP tools, one server per environment, and each server has a `release` tool.

The entry below is a standalone example in the project's `.claude/settings.json`. Its matcher catches `release` on every server. The empty `args` list makes Claude Code run the script directly instead of through a shell:

json
`{
 "hooks": {
 "PreToolUse": [
 {
 "matcher": "mcp__deploy-.*__release",
 "hooks": [
 { "type": "command",
 "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/release-gate.sh",
 "args": [] }
 ]
 }
 ]
 }
}`

The gate itself, `.claude/hooks/release-gate.sh`:

bash
`#!/bin/bash
# Release gate. dev: allow. staging: ask. production: an approved change ticket for this version, or block.
input=$(cat)
tool=$(jq -r '.tool_name' <<<"$input")
version=$(jq -r '.tool_input.version' <<<"$input")
ticket=$(jq -r '.tool_input.ticket // empty' <<<"$input")

decide() { # decide <allow|ask|deny> <reason>
 jq -n --arg decision "$1" --arg reason "$2" '{hookSpecificOutput: {
 hookEventName: "PreToolUse",
 permissionDecision: $decision,
 permissionDecisionReason: $reason}}'
 exit 0
}

case "$tool" in
 mcp__deploy-dev__release)
 decide allow "dev needs no approval" ;;
 mcp__deploy-staging__release)
 [ "$GITHUB_REF" = "refs/heads/main" ] && decide allow "pipeline release from main"
 decide ask "This ships $version to staging. Approve only if you own this release." ;;
 mcp__deploy-prod__release)
 route="Open a change ticket at https://change.example.com/new for version $version, \
wait for the release manager to approve it, then call release again with that ticket number."
 [[ "$ticket" =~ ^CHG-[0-9]+$ && "$version" =~ ^[0-9a-f]{7,40}$ ]] ||
 decide deny "Production needs an approved change ticket. $route"
 if approver=$(/usr/local/bin/change-ticket show --ticket "$ticket" --format json |
 jq -er --arg v "$version" 'select(.state == "approved" and .version == $v) | .approver' 2>/dev/null); then
 decide allow "$ticket approved by $approver"
 fi
 decide deny "$ticket is not approved for version $version. $route" ;;
 *)
 decide deny "No release rule for $tool. Add one to release-gate.sh first." ;;
esac`

In the script, `version` and `ticket` are the inputs Claude passes to the `release` tool. `change-ticket` stands for your change system's own command-line tool. The gate depends on the agent having no way to write to the records it reads.

In a non-interactive run nobody can answer an `ask`, so Claude Code denies the call. That is why the gate allows staging from the pipeline on `main`, where the approved merge is the approval.

The gate has a limit. An engineer could set `GITHUB_REF` by hand in their own session, although doing that skips only the prompt they would have answered themselves.

The reason on an `ask` is shown to the person. The reason on a `deny` is shown to Claude, so the block message names the route to approval for Claude to pass on. The staging result comes first, then production with no ticket:

json
`{
 "hookSpecificOutput": {
 "hookEventName": "PreToolUse",
 "permissionDecision": "ask",
 "permissionDecisionReason": "This ships 4f2c9e1 to staging. Approve only if you own this release."
 }
}`

json
`{
 "hookSpecificOutput": {
 "hookEventName": "PreToolUse",
 "permissionDecision": "deny",
 "permissionDecisionReason": "Production needs an approved change ticket. Open a change ticket at https://change.example.com/new for version 4f2c9e1, wait for the release manager to approve it, then call release again with that ticket number."
 }
}`

## Governance considerations

Hooks are the approval gates. The gate condition is enforced every time, for everyone. Allow and block decisions are logged with a timestamp. The gate also defines what counts as approval, whether that's an approved change ticket or the release manager's sign-off.

## Managed settings for a regulated enterprise

Managed settings for a regulated enterprise, deployed by the platform team via mobile device management (MDM) or the admin console. Engineers cannot edit or override any of the settings therein. See below:

json
`{
 "permissions": {
 "deny": [
 "Read(.env*)", "Read(./secrets/**)",
 "WebFetch", "Bash(curl *)", "Bash(wget *)"
 ],
 "allow": [
 "Bash(git *)", "Bash(make build)",
 "Bash(make test)", "Bash(make lint)"
 ],
 "disableBypassPermissionsMode": "disable"
 },
 "allowManagedPermissionRulesOnly": true,
 "sandbox": {
 "enabled": true,
 "failIfUnavailable": true,
 "allowUnsandboxedCommands": false,
 "network": { "allowedDomains": ["git.internal.example.com", "registry.npmjs.org"] },
 "credentials": {
 "files": [
 { "path": "~/.ssh", "mode": "deny" },
 { "path": "~/.aws/credentials", "mode": "deny" }
 ],
 "envVars": [ { "name": "GITHUB_TOKEN", "mode": "deny" } ]
 }
 },
 "allowManagedHooksOnly": true,
 "disableSideloadFlags": true,
 "allowManagedMcpServersOnly": true,
 "strictKnownMarketplaces": [
 { "source": "github", "repo": "example-corp/approved-plugins" }
 ],
 "requiredMinimumVersion": "2.1.193"
}`

What the settings do, in control terms:

- `permissions.deny` keeps secrets out of the agent's context and blocks arbitrary network egress through tools. `permissions.allow` pre-approves the safe inner loop so the deny list doesn't turn into prompt fatigue.

- `disableBypassPermissionsMode` plus `allowManagedPermissionRulesOnly` means no engineer, project file, or command-line flag can widen the rules.

- `sandbox` covers what permissions cannot. A tool-level deny on WebFetch doesn't stop a shell command reaching the network, whereas the OS-level domain allowlist blocks egress outright, so the two enforce one objective at different layers. `failIfUnavailable` and `allowUnsandboxedCommands` turn the sandbox into a precondition, meaning Claude Code refuses to start when the sandbox cannot initialize and a command that fails inside the sandbox cannot be retried outside it.

- `credentials` handles a case the deny rules miss. `permissions.deny` governs Claude's file tools, but a sandboxed shell command could still read `~/.ssh` or `~/.aws/credentials` by default. This block denies those reads and strips the listed secrets from the environment of sandboxed commands.

- `allowManagedHooksOnly` means only hooks defined in managed settings run; hooks in user, project, and local settings are blocked, including the standalone `.claude/settings.json` example above. To keep this play's approval gate enforced, define it in the managed file's own `hooks` block.

- `disableSideloadFlags` and `strictKnownMarketplaces` mean that any skill, agent, hook, or MCP server on an engineer's machine came through the organization's approved plugin marketplace and not from a home directory. The marketplace allowlist controls what can be installed, and the flags that would sideload a plugin, agent, or MCP config for a single run are rejected at startup.

- `allowManagedMcpServersOnly` makes the agent's tool surface an allowlist owned by the platform team.

- `requiredMinimumVersion` refuses to start on a version below the approved floor, so the controls are enforced by a build the organization has actually assessed.

Treat the example as a starting point to customize to your own environment. Each deny rule removes some capability, and the right balance depends on the data classification of the repo. The settings reference(opens in new tab) documents all keys, including the managed-only ones.

## How to measure it

For the hooks themselves:

- Leading indicator: Time spent waiting on each approval gate. Every hook decision is written to the OpenTelemetry export with a timestamp and an allow or block verdict, so the wait is visible per gate.

- Lagging indicator: Gate violations reaching production before and after hooks, from the incident tracker.

Previous lessonAI in the PR review loopNext lessonCI/CD integration and deployment

Lesson 11 of 14 · The AI-native SDLC playbookHooks as approval gates

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
- Managed settings for a regulated enterprise
- How to measure it
© 2026 Anthropic PBC

- Privacy choices
- Privacy policy
- Usage policy
