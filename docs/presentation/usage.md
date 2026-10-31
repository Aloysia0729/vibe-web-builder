# Usage, installation, and recovery

This guide complements the [English README](../../README.md) and [完整中文说明](../../README.zh-CN.md). The [previous Chinese guide](previous-guide.zh-CN.md) preserves the original content for comparison.

## A first project

Describe your purpose, audience, pages, features, and visual preferences in your own words. Any of these may be unclear. The Skill extracts what is known and asks at most 1–3 new questions per round. AI suggestions, assumptions, unresolved items, and user-confirmed facts remain distinct. Choosing a mode does not itself confirm the complete requirements.

For a portfolio, a reasonable planning-only flow is: describe the audience and work → review a requirements summary → explicitly confirm it → review the page sketch and interactions → independently accept the sketch → receive six documents and stop. A static site can be enough; no database is added just because the project is a website. The studio demonstration follows this workflow with actual recorded outputs.

To implement later, explicitly request development mode. Valid confirmations carry over. Implement MVP tasks first, record observable acceptance results, then extend. Do not treat a prototype's local data as verified production persistence.

## Project documents

The six templates live in the Skill's assets/templates directory and are copied into the target website's docs/web-builder directory, not into the installed Skill. Only affected documents should change each turn. Page and interaction IDs connect the sitemap, interaction rules, sketches, tasks, and evidence.

The optional tool commands in both READMEs accept an existing project directory. Initialization refuses an existing document directory. State checking catches mismatched versions, missing confirmation evidence, or planning mode entering implementation, but cannot certify that a person actually approved anything. Never edit a pending tag to simulate consent.

## Pause, continue, change

Say “pause and save progress.” The next action, remaining tasks, issues, test results, mode, and stage should be saved. In a new session, say “continue this project.” The agent reads files and actual code before acting; it does not rely on hidden chat memory.

Business changes such as replacing an email address display with a contact form affect requirements, interactions, design, and tasks. Increment revisions and invalidate affected confirmations. A visual-only change preserves requirements approval but needs a new sketch review. Keep still-valid implementation rather than restarting everything. Missing or conflicting documents require conservative recovery, not an overwrite with fresh templates. See [the complete recovery rules](../../skills/vibe-web-builder/references/project-resumption.md).

## FAQ

- **Planning only?** Say so explicitly. Even two approvals do not authorize application creation in planning mode.
- **No technical experience?** Decide business outcomes; the agent recommends technical choices and explains material cost/function tradeoffs.
- **References unavailable?** The agent discloses what it could not read and suggests a direction without claiming observations.
- **No browser?** Text wireframes or Mermaid remain possible; browser interactions and responsive checks stay unrun.
- **Skill not found?** Check the full folder, SKILL.md, host search paths, and restart requirements. Try explicit invocation. Copying files successfully does not prove host discovery.
- **Python unavailable?** The core instructions and templates can be used manually; only helper scripts need Python/PyYAML.
- **Existing project?** Inspect its instructions, dependencies, lockfile, architecture, CI, and user changes before extending it.

## Checks and authorization

Use existing build/type/test tools where applicable, plus representative interactions, routes, input validation, responsive layouts, and basic accessibility. Record command, directory, exit status, scope, and current-run evidence. Failed checks receive bounded, targeted repairs and relevant retests, not disabled assertions or indefinite retries. Unrun, skipped, inferred, and passed results stay distinct.

Only actual needs justify credentials or service integration. Use secure configuration channels, never chat logs or Git. Requirements/sketch approval is separate from permission for account access, secret use, payment, cloud resources, production modifications, deployment, pushes, or destructive data operations. The Skill adds no dedicated key; Codex access itself remains a host prerequisite.
