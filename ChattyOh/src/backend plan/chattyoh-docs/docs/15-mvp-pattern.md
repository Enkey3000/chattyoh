# 15 — MVP Pattern

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owners:** Product Owner + Tech Lead · **Status:** Draft
**Upstream:** `01-prd.md`, `14-poc-report.md` · **Downstream:** `16-playbook.md`, `18-execution-guide.md`

## 1. The pattern: walking skeleton, then widen

1. **Walking skeleton (MVP-0):** the thinnest end-to-end slice that touches every layer: sign-in → workspace → project → streamed chat → audit event, on real infrastructure, with CI, tests and accessibility baseline.
2. **Complete the core (MVP-1):** add the remaining must-have features on top of the skeleton, with their gates, approvals and tests.
3. **Harden and broaden (MVP-2):** resilience, privacy, history, compatibility and the desktop and mobile shells.

Each slice is shippable behind feature flags and passes the release gates in `10-release-deployment-plan.md` at its own level.

## 2. Scope filter for every candidate feature

Score 1–5 on **user value**, **risk reduction** (does it test a risky assumption?), **effort** (5 = small), **dependency** (does anything need it first?). Build when value + risk reduction + dependency − (6 − effort) is high *and* it traces to a PRD ID. Anything without a PRD ID waits.

## 3. In and out

| PRD item | MVP-0 | MVP-1 | MVP-2 | Notes |
|---|---|---|---|---|
| PRD-F-01 Accounts and workspaces | Sign-in, workspace | Roles, invites, MFA, sessions | | |
| PRD-F-02 Projects, tasks | Project and task CRUD | Gates, archive, filters | | |
| PRD-F-03 ChatMode | Streaming chat | Commands, stop | | |
| PRD-F-04 SpecMode | | Documents, generation, approval | Version history | |
| PRD-F-05 Agents | | Create, test, approve, run, history | Pause/resume | |
| PRD-F-06 Audit, import/export | Audit events | Notifications, export, import | Backup/restore | |
| PRD-F-07 Accessible UI | Navigation, themes, labels | WCAG 2.2 AA verified | | |
| PRD-G-04 Desktop and mobile | | | Electron and Flutter shells | One UI codebase |
| **Out (non-goals)** | Real deployments, marketplaces, SSO/SCIM, billing, co-editing, native mobile UI, offline AI, real test runners, IDE, design canvas | | | See PRD section 2 |

## 4. Rules for incomplete or simulated features

- Hidden behind a flag unless it is clearly labeled **Preview** or **Simulated** in the UI, API docs and website (SRS-FR-UI-002).
- No random success or failure presented as real results.
- Marketing and website copy may describe only features that exist in the released slice.

## 5. Exit criteria per slice

| Slice | Exit criteria |
|---|---|
| MVP-0 | Skeleton deployed to staging; P1 cases for its requirements pass; CI gates running; cross-tenant suite green; data-integrity cases (SRS-NFR-DATA-01/02, SRS-NFR-CONC-01) pass |
| MVP-1 | All MVP-1 requirements verified; UAT scenarios 001–009 pass; pen-test retest complete; accessibility checks clean |
| MVP-2 | Hardening and shells complete; availability drill done; UAT-010 passes; release gates REL-01…REL-12 met |

## 6. Feature flags

Flags per slice and per feature; default off in production until the slice's exit criteria are met; flags removed after a release is stable.

## 7. After MVP

Candidate next items (ranked by the same filter): real integrations one by one (source control first), real test execution, deployment targets, SSO, billing, native mobile UI.
