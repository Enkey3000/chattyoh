# 01 — Product Requirements Document (PRD)

**Project:** ChattyOh Inc · **Version:** 0.1 (draft for review) · **Owner:** Product Owner · **Status:** Draft
**Downstream:** `02-srs.md`, `09-uat-plan.md`, `15-mvp-pattern.md` · **Companion rules:** `rules/cursorrules.md`

> Items marked *proposed* are targets for the Product Owner to confirm. IDs are stable; do not renumber.

## 1. Overview

**Vision.** One agent-assisted workspace that takes an idea from conversation to a deployed, documented and tested product, with the human always in control.

**Problem.** Builders juggle separate tools for chat, design, documentation, coding, testing, review, deployment and automation. Context is lost between tools, AI output is hard to trust, and approvals and audit trails are missing.

**Opportunity.** One project context shared by nine modes (ChatMode, VibeMode, CompMode, SpecMode, DevMode, TestMode, RevMode, PushMode, GentMode) so each mode can hand work to the next.

**Current state.** A working front-end prototype (web, desktop and mobile shells) with browser-only storage. It proves the navigation and record model; it has no accounts, backend or real integrations. See `17-gap-analysis.md`.

## 2. Goals and non-goals

| ID | Goal | Measure |
|---|---|---|
| PRD-G-01 | Shorten the time from idea to first working project | PRD-M-01 |
| PRD-G-02 | Keep humans in control: approvals for sensitive actions, visible limits | PRD-M-04 |
| PRD-G-03 | Be trustworthy: label simulated or preview features, never lose data silently, keep an audit trail | PRD-M-06 |
| PRD-G-04 | One codebase for web, desktop and mobile | PRD-M-07 |

| ID | Non-goal (MVP) |
|---|---|
| PRD-N-01 | Real cloud deployments, domains and marketplace publishing |
| PRD-N-02 | SSO/SCIM, billing and metering |
| PRD-N-03 | Real-time co-editing |
| PRD-N-04 | A native (non-WebView) mobile UI |
| PRD-N-05 | Offline AI |
| PRD-N-06 | Real test runners, code editor/IDE, design canvas |

## 3. Personas

| Persona | Needs | Key modes |
|---|---|---|
| **Maker** (solo founder) | Turn ideas into plans and working projects quickly | Chat, Spec, Gent |
| **Team lead** | Organize work, assign roles, keep quality gates | Projects, Tasks, Rev |
| **Admin / security reviewer** | See who did what; control approvals and data | Audit, Members |
| **Agency lead** | Run several client workspaces with consistent quality | Workspaces, Spec |

## 4. Features

| ID | Feature | Priority | Acceptance statement | Slice |
|---|---|---|---|---|
| PRD-F-01 | Accounts and workspaces (Personal, Team) with roles | Must | A user can sign in, create a workspace, invite a member and assign a role; members see only their workspace data | MVP-0/1 |
| PRD-F-02 | Projects, tasks and a lifecycle model | Must | A user can create projects and tasks, and advance a project only when quality gates allow it | MVP-0/1 |
| PRD-F-03 | ChatMode with a real LLM | Must | A user can chat with streamed replies, stop a reply, and create items with slash commands | MVP-0/1 |
| PRD-F-04 | SpecMode documents | Must | A user can generate, edit, submit and approve a document; approval is audited | MVP-1 |
| PRD-F-05 | Agents with approvals | Must | A user can create, test, approve and run an agent within enforced limits; runs are recorded | MVP-1 |
| PRD-F-06 | Audit, notifications, import/export, backup | Should | Admins can read the audit log; users can export, import and restore workspace data safely | MVP-0/1/2 |
| PRD-F-07 | Accessible, consistent UI | Must | Core journeys pass WCAG 2.2 AA checks; navigation, theme and labeling rules are met | MVP-0/1 |

## 5. Key user journeys

| ID | Journey |
|---|---|
| J-01 | Sign up → create workspace → first project (target ≤ 10 minutes) |
| J-02 | Plan a project in chat → create tasks with slash commands |
| J-03 | Generate a PRD draft → edit → submit for review → approve |
| J-04 | Create an agent → test → approve deployment → run a task → review the run |
| J-05 | Try to advance a project with failing tests → see the block → fix → advance |

## 6. Success metrics (proposed targets)

| ID | Metric | Target |
|---|---|---|
| PRD-M-01 | Activation: new users who create a first project within 10 minutes | ≥ 60% |
| PRD-M-02 | Weekly active workspaces | Baseline set during beta |
| PRD-M-03 | Generated documents that reach *Approved* | ≥ 40% |
| PRD-M-04 | Agent runs that complete successfully within limits | ≥ 90% |
| PRD-M-05 | API p95 latency for CRUD operations | ≤ 300 ms |
| PRD-M-06 | Open Critical/High accessibility or data-integrity defects at release | 0 |
| PRD-M-07 | Share of UI code shared across web, desktop and mobile | ≥ 95% |

## 7. MVP boundary

Defined in `15-mvp-pattern.md`: slices **MVP-0** (walking skeleton), **MVP-1** (complete core features) and **MVP-2** (hardening and breadth). Everything under Non-goals is out.

## 8. Assumptions, risks, dependencies

| ID | Item | Mitigation |
|---|---|---|
| ASM-01 | Web-first launch; desktop and mobile shells follow the same UI | ARCH-ADR-007: shells carry no business logic |
| ASM-02 | A managed OIDC identity provider will be used | Decision needed (section 9) |
| ASM-03 | One external LLM provider at launch, behind a gateway | The gateway keeps providers swappable |
| ASM-04 | GDPR-style privacy baseline; no regulated health or payment data | Revisit if scope changes |
| RSK-01 | LLM cost or latency exceeds budget | Quotas, caching, model tiers; PoC-02 |
| RSK-02 | Prompt injection or agent misuse | Controls SEC-C-09 and SEC-C-10; Threat Model |
| RSK-03 | Marketing claims outrun real features | PRD-G-03; labeling requirement SRS-FR-UI-002 |
| RSK-04 | A store rejects the WebView mobile app | Add native value; plan a native UI after MVP |
| DEP-01 | Hosting, identity and LLM provider contracts | Decisions in section 9 |

## 9. Open questions (decisions needed)

1. Hosting and cloud provider. 2. Identity provider (managed or self-built). 3. LLM provider(s) and data-handling terms. 4. Compliance target (GDPR only, or also SOC 2 / ISO 27001). 5. Team size and dates. 6. Tenancy model for enterprise customers.

## 10. Approval

| Role | Name | Date | Decision |
|---|---|---|---|
| Product Owner | | | |
| Tech Lead | | | |
| Security Lead | | | |
