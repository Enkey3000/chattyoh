# Roadmap

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Product Owner · **Status:** Draft — *dates are relative weeks from project start and provisional until the team and decisions are confirmed*
**Upstream:** `product-vision.md`, `15-mvp-pattern.md` · **Detail:** `18-execution-guide.md`

## 1. Now / Next / Later

| Horizon | Theme | Content | Exit signal |
|---|---|---|---|
| **Now** (weeks 0–6) | Foundations and walking skeleton | Decisions confirmed; PoC spikes; repo and CI; sign-in, workspaces, projects, tasks, streamed chat, audit, accessible shell → **MVP-0** | MVP-0 on staging; cross-tenant suite green; data-integrity cases pass |
| **Next** (weeks 7–12) | Complete the core | Roles and gates, documents with approval, agents with approvals, import/export, notifications, performance and accessibility → **MVP-1** | UAT scenarios 001–009 pass; no open Critical/High defects |
| **Then** (weeks 13–16) | Harden and release | Version history, pause/resume, backup/restore, privacy, availability, Electron and Flutter shells, pen test, release candidate → **1.0** | Gates REL-01…REL-12 met; UAT-010 passes |
| **Later** (after 1.0) | Real integrations and growth | Source control, real test execution, deployment targets, SSO, billing, collaboration, templates, native mobile UI, agent marketplace | Chosen by metrics and user research |

## 2. Milestones

| Milestone | Target week | Criteria |
|---|---|---|
| M0 Decisions and PoC | 2 | Seven open decisions made; PoC-01/03/06 results |
| M1 Requirements baselined | 5 | PRD, SRS, Architecture, Security Measures approved |
| M2 MVP-0 (alpha, internal) | 6 | Skeleton live on staging |
| M3 MVP-1 (private beta) | 12 | Core features complete; UAT 001–009 |
| M4 Release candidate | 15 | Pen-test retest passed; shells built |
| M5 1.0 general availability | 16 | All release gates met |

## 3. Themes and outcomes

| Theme | Outcome | Related |
|---|---|---|
| Trust | Honest labels, audit, approvals, no silent loss | PRD-G-02, PRD-G-03 |
| Speed to first value | First project in ≤ 10 minutes | PRD-M-01 |
| Everywhere | Web, desktop and phone from one codebase | PRD-G-04 |
| Safe at scale | Isolation, quotas, performance, availability | SRS-NFR-* |

## 3a. Post-1.0 candidates (ranked with the MVP scope filter)

1. Source-control integration (read first, then write with approval).
2. Real test execution through a runner integration.
3. One real deployment target with approvals and rollback.
4. SSO and SCIM for larger teams.
5. Billing and usage metering.
6. Shared templates and an agent library.
7. Native mobile UI if the WebView approach limits quality or store acceptance.

## 4. Dependencies

Identity provider, LLM provider and hosting decisions block M1. The OpenAPI spec precedes each feature. Shells depend on a stable web UI. Pen test needs a feature freeze. Legal review precedes release (privacy, terms, claims).

## 5. Assumptions and risks

Assumes a team of 4–5 engineers plus design, QA and DevOps. Main risks: late decisions (RR-01), PoC failures (RR-02), accessibility effort (RR-04), store review (RR-06), scope creep (RR-07). See `18-execution-guide.md` section 6.

## 6. Review cadence

Roadmap reviewed at the end of each two-week sprint and at each milestone; changes require Product Owner approval and are recorded in the decision log.
