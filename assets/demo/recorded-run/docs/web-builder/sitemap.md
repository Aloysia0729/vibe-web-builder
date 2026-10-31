---
schema_version: 1
---

# Sitemap — requirements revision 2

## Page

| ID | Purpose / visitors | Route / entries | Modules | Actions / target | Scope |
|---|---|---|---|---|---|
| P01 | Introduce a fictional design studio to small businesses | `/`, logo and section anchors | Home, Services, Work, About, Contact, footer | I01 section links; I02 email; I03 back to top | MVP |

## Navigation
Home `#home` → Services `#services` → Work `#work` → About `#about` → Contact `#contact`. Logo and footer return to `#home`. Hero Explore our work links to `#work`; Email us and the contact address link to `mailto:hello@northstar.example`.

## Responsive and exceptional routes
Desktop navigation sits on one row. Mobile navigation wraps; no hamburger control is needed for five short links. Services and work cards stack on narrow screens. Section headings have scroll margin so navigation never hides them. There are no additional routes, project detail pages, authentication states, or application-specific error screens. Unknown anchors have no promised destination; all generated internal links must match existing IDs. Host-level unknown-route behavior will depend on a future host and is not implemented in planning mode.
