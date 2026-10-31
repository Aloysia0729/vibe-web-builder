---
schema_version: 1
---

# Interaction specification — P01

| ID / task | Element and initial state | Action / input | Response and success | Exception / states | Acceptance |
|---|---|---|---|---|---|
| I01 / D1 | Visible section navigation; hero Explore our work | Click or keyboard Enter; no user data | Native anchor moves to matching section; address hash updates | No loading/empty/disabled state: local static anchors. Every target must exist. | Navigate each section by pointer and keyboard; heading remains visible on desktop/mobile. |
| I02 / D1 | Hero Email us and Contact address are visible links | Click or Enter; no form input or validation | Delegate mailto:hello@northstar.example to OS/email app | User may have no email handler; readable/selectable address remains available. No in-page success claim, delivery, or backend retry. No loading state. | Inspect correct mailto URI; verify address can be selected and link focused. Email delivery is not tested. |
| I03 / D1 | Logo and footer Back to top | Click or Enter | Move to #home | No loading or disabled state; Home ID always exists. | Focus visible; activate and verify Home target. |
| I04 / D1 | Skip to content link appears on focus | First Tab and Enter | Jump to focusable main content | No external dependency or loading | Keyboard user can bypass header. |

## Content and data
Work examples are static articles, not buttons or links to missing case studies. Display a clear Fictional demonstration project label on every card. No forms, account data, persistence, cookies, booking, payments, permissions, or external services.

## Accessibility / responsive acceptance
Use semantic header/nav/main/section/footer, one h1, ordered headings, descriptive link labels, visible focus, sufficient contrast, and no horizontal overflow at narrow widths. Respect prefers-reduced-motion; anchors may use ordinary native jumps. No custom animation required.

## Visitor flows
I01: Home → Explore our work → Work sample articles → Contact navigation → I02 email link.
I03: Footer → Back to top → Home. I04: first keyboard focus → main content.
