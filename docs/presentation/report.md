# README presentation audit and delivery record

Date: 2026-10-31 (Asia/Shanghai). Work is local; publishing and metadata edits are not authorized for this task. Baseline: bfaf02c, clean worktree; remote main matched that SHA at inspection. Source manifest remains version 0.1.1. LICENSE is unchanged.

## Positioning and copy

Chosen headline: **Turn vague ideas into clear website plans.** Compared with “Your idea is messy. Your website plan doesn't have to be.” it states the outcome faster, avoids calling a beginner's idea messy, and accurately stops short of promising an automatically completed production website. The supporting sentence names Codex, requirements, sketches, and optional implementation. Three differentiators map directly to SKILL.md and its references: adaptive questions; independent requirements/sketch approval; simple AI-guided technical decisions.

## Before → after and content migration

| Dimension | Actual previous state | Local change | Purpose |
|---|---|---|---|
| First screen | Chinese heading and technical introduction | English value-led hero, language links, three action links | Explain the outcome before the internals |
| Brand | No branding/demo asset directory | Original dark terminal concept artwork and social cover | Consistent recognizable presentation |
| Differentiators | Distributed through workflow description | Three-column table with concrete benefits | Show how planning differs from code-first prompting |
| Demo | Text example and historical test records | New independently executed fictional-studio demo; assets documented separately | Verifiable workflow instead of invented testimonials |
| Installation | Accurate installer/manual methods | Same commands, three-step Quick Start, later detailed fallback | Lower initial effort without changing compatibility claims |
| Languages | Chinese only | Full English and Chinese counterparts | Support international and Chinese readers |
| Discovery | No explicit metadata proposal | Prepared description/topics/social instructions, not remotely applied | Make discovery work reviewable |
| Support | Contribution links, no natural Star invitation | Invitation after useful material plus actual Issues/contribution links | Invite voluntary support, never gate functionality |

All previous technical content is retained in previous-guide.zh-CN.md. Mode rules, installation commands, six files, helper requirements, recovery, safeguards, license, and limitations remain in both READMEs; deeper explanations also live in usage.md. The old portfolio example is retained in the archive and complemented by the new studio record. The archive's local links are rebased, not discarded.

## Reference inspection

Read the actual stablyai/orca main README via raw.githubusercontent.com: centered identity, restrained badges, language switch, main product visual, feature/support links. Reused only the information architecture, no visual assets, logos, claims, or wording. The rendered Orca repository request returned HTTP 403, but the specified v1.4.245 Release page was successfully read separately: version notes and downloadable assets serve a different purpose from an ongoing README introduction. The official github/docs Markdown source confirms Topics rules (lowercase letters/numbers/hyphens, ≤50 characters, ≤20 topics). No Orca images were downloaded or reused. Current Release publication status is not inferred from tags.

## Verification

Final command results and demo results are recorded after execution below. Actual GitHub rendering of these **unpushed** changes cannot be confirmed by visiting the old public README. Local browser Markdown rendering is a separate, limited check; GitHub sanitizer, themes, and mobile rendering require a post-push review.

## Metadata / authorization

See discovery.md for the exact proposed description/topics and Social Preview upload route. None is applied. No push, PR, release, default-branch change, account access, or repository settings mutation is performed. No Discussions link is advertised without verifying that the feature is enabled.

## Visitor review scenarios

- A, beginner: the headline describes a plan, Quick Start begins with installation and a copyable idea, and language links are visible. Remaining obstacle: Codex access and host-specific discovery still need to be understood; both are disclosed.
- B, Codex developer: installer command, manual copy, Skill path, manifest scope, and helper requirements are directly discoverable. Remaining obstacle: not every host marketplace has been verified.
- C, contributor: documentation links lead to instructions, scenarios, validation, contribution rules, changelog and release process; Issues is the feedback route. Remaining obstacle: many supporting documents remain Chinese; the English usage guide covers core operations.

These are structured editorial walkthroughs by the implementing agent, not results from three recruited human participants.

## Growth observation

Use growth-30-days.md after actual publication. No baseline traffic, stars, click-through or installation conversion has been fabricated. Rolling Traffic windows overlap; save snapshots at Day 0/7/14/21/30 and avoid summing overlapping visitors. Growth is neither promised nor causally attributed to the README alone.

## Final executed results

- **PASS** `python3 scripts/check_presentation.py`: both language entries, local links and Markdown anchors, language-shared media/install command, image decoding, 2:1 social cover under 1 MB. Separate negative probes rejected a missing link and corrupt GIF. The checker requires the environment's Pillow; no core dependency or CI was changed.
- **PASS** `.venv/bin/python scripts/validate.py` and `.venv/bin/python -m unittest discover -s tests -q`: existing **36 tests** executed and passed on the current local presentation changes, no skips. No claim of exhaustive model behavior follows from them.
- **PASS** state checker on assets/demo/recorded-run: requirements r2 and wireframe r1 independently confirmed before the driver's explicit development request. Full raw and browseable transcripts preserve all four turns.
- **PASS** original studio browser verification: five nav anchors, Work/back-to-top, loaded original local artwork, keyboard skip, zero page errors/overflow at 1280×900 and 390×844. Evidence: assets/demo/recorded-run/verification/browser-results.json. Email delivery and full accessibility audit were not run.
- **PASS** independent capture: real site screenshots at 1280px and 390px; seven GIF frames (real message excerpts, actual wireframe, explicit approvals, actual website). The comparison is a labeled document graphic. Temporary capture service closed in finally, original agent's 4187 service stopped; no action was taken on prior unrelated 8765 state.
- **PASS** local browser README rendering at 390px and 1280px for English and Chinese: all local images loaded, one H1, no document-wide horizontal overflow; wide tables scroll. This uses temporary markdown-it-py 3.0.0 and local GitHub-inspired CSS, not the GitHub renderer. Evidence: render-results.json and the four README preview PNGs in this directory.
- **PASS** `git diff --check`; protected tracked files compared against HEAD: LICENSE, core Skill/references/scripts, existing tests, manifest, dependencies, and CI are unchanged. Only README and new presentation resources/helpers are included.
- **NOT RUN** actual GitHub rendering of the unpushed versions, social-card application, metadata mutation, remote CI of these local changes, all-host installation discovery, traffic/growth measurements, and production deployment.

Initial failures were retained as limitations rather than hidden: binding a temporary local server required supported sandbox escalation, then capture passed; the initial link scan found two transcript screenshot links whose genuine files had not yet been copied, fixed by including the actual original screenshots. The demo's document checker rejected generic phase/status labels; the agent corrected its documents to the existing schema. Neither tests nor Skill instructions were relaxed.

## Media inventory

| Asset | Actual dimensions | Approximate size | Meaning |
|---|---|---|---|
| assets/branding/hero.png | 1774×887 | 1.29 MB | Original concept artwork, not a screenshot |
| assets/branding/social-preview.jpg | 1774×887 | 131 KB | Same composition, JPEG encoding, not remotely applied |
| assets/demo/walkthrough.gif | 1280×800, 7 frames | 302 KB | Labeled transcript replay + actual final browser view |
| assets/demo/studio-desktop.png | 1280×2870 | 286 KB | Actual full-page website screenshot |
| assets/demo/studio-mobile.png | 390×3674 | 217 KB | Actual mobile website screenshot |
| assets/demo/before-after.png | 1280×800 | 126 KB | Actual input/output quotes in a designed comparison |

No fake stars, customer testimonials, downloads, speedups, or conversion claims are present. The artwork's 2:1 cover is larger than the suggested 1280×640 and remains under the 1 MB upload recommendation. Static text, transcript and screenshots provide alternatives to GIF playback. Inspect actual GitHub mobile readability after an authorized push; local checks cannot certify that renderer.
