# 17 — Gap Analysis

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Tech Lead · **Status:** Draft (refresh every sprint)
**Sources:** prototype platform audit (IDs B-, S-, A-), PoC plan, `01-prd.md` … `04-security-measures.md` · **Downstream:** `18-execution-guide.md`

Current state = the front-end prototype (web, desktop, mobile shells). Priority: High / Medium / Low. Status: Open, Partly fixed in prototype (not carried to the product), Planned.

| ID | Area | Current state | Target | Requirement | Audit ref | Priority | Effort | Status |
|---|---|---|---|---|---|---|---|---|
| GAP-01 | Persistence | Browser storage; whole database in one key | Server database plus IndexedDB cache; per-record writes | SRS-NFR-DATA-01, SRS-NFR-PERF-01 | B-01, B-07 | High | L | Partly fixed in prototype |
| GAP-02 | Data safety | Safe mode and storage warnings exist in prototype only | Validated, versioned data; visible write errors | SRS-NFR-DATA-01 | B-01, B-02 | High | M | Partly fixed in prototype |
| GAP-03 | Identity | None | OIDC, sessions, MFA | SRS-FR-AUTH-001…003 | S-02 | High | L | Open |
| GAP-04 | Tenancy | Three local databases | Server tenancy with RLS | SRS-FR-WS-001 | S-02 | High | L | Open |
| GAP-05 | Authorization | Roles list only | Server-enforced roles and object checks | SRS-FR-WS-002, SEC-C-02 | S-02 | High | M | Open |
| GAP-06 | Integrity | Links by name; statuses editable | ID links; server-side rules module | SRS-NFR-DATA-02, SRS-NFR-INT-01 | B-03, B-04 | High | M | Open |
| GAP-07 | Concurrency | Job and chat races fixed in prototype | Tenant-bound jobs; reply IDs | SRS-NFR-CONC-01, SRS-FR-CHAT-003 | B-05, B-06 | High | M | Partly fixed in prototype |
| GAP-08 | Secrets | Plain text in client storage and exports | Secrets manager; masked; excluded from exports | SEC-C-04, SRS-FR-IO-001 | S-01 | High | M | Open |
| GAP-09 | AI | Runtime-dependent; fallback text | Gateway, streaming, quotas, approvals | SRS-FR-CHAT-002, SRS-FR-AGENT-003/004 | — | High | L | Open |
| GAP-10 | Agent sandbox | Simulated runs | Approval-first agents; sandbox for code tools | SRS-FR-AGENT-004, SEC-C-10 | — | Medium | L | Open |
| GAP-11 | Integrations | Simulated | Real, one at a time; label until real | SRS-FR-UI-002 | B-10 | Medium | L | Open (non-goal for MVP) |
| GAP-12 | Honesty labels | Only some features labeled | Consistent labels everywhere | SRS-FR-UI-002 | B-10 | High | S | Open |
| GAP-13 | Settings | Several saved but unused | Wire up or remove | SRS-FR-CHAT-002 | B-09 | Medium | S | Open |
| GAP-14 | Accessibility | Contrast, dialogs, live regions, targets, menus | WCAG 2.2 AA verified | SRS-NFR-A11Y-01 | A-01…A-07 | Medium | M | Open |
| GAP-15 | Performance | Slow search and actions on large lists | Pagination, virtualization, debounce | SRS-NFR-PERF-01 | B-07 | Medium | M | Open |
| GAP-16 | Delivery | Four copies of one HTML file | One codebase plus bridges | SRS-NFR-COMPAT-01, SRS-NFR-MAINT-01 | — | Medium | L | Open |
| GAP-17 | Quality | Ad-hoc browser scripts | CI suite and RTM check | SRS-NFR-MAINT-01 | — | Medium | M | Planned |
| GAP-18 | Security pipeline | None | SAST, SCA, secrets, SBOM, DAST | SEC-C-11, SEC-C-14 | S-03 | High | M | Planned |
| GAP-19 | PWA/offline | Not installable; no offline | Real manifest and service worker (public assets) | SRS-NFR-COMPAT-01 | B-08 | Low | S | Open |
| GAP-20 | Website | Placeholders, overstated claims, no form backend | Accurate claims, legal pages, working contact flow | PRD-G-03 | — | Medium | S | Open |
| GAP-21 | Desktop shell | Never run; outdated Electron; Cmd+H clash | Run on real machines; current Electron; hardening | SRS-NFR-COMPAT-01 | S-06 | Medium | M | Open |
| GAP-22 | Mobile shell | Never compiled; backup exposure; store risk | Device builds; exclude backups; native value | SRS-NFR-COMPAT-01 | S-07 | Medium | M | Open |
| GAP-23 | Observability | None | Logs, traces, metrics, alerts | SRS-NFR-OBS-01 | — | Medium | M | Open |
| GAP-24 | Privacy | No policy or disclosures | Policy, consent, export/erasure | SRS-NFR-PRIV-01, SEC-C-15 | S-05 | Medium | M | Open |

**Effort:** S ≤ 3 days, M ≈ 1–2 weeks, L > 2 weeks (single engineer, rough).

**Reading the table:** items marked *Partly fixed in prototype* have working logic in the prototype that should be reimplemented server-side; they are not done for the product.
