# ChattyOh Inc — Project Documentation Plan

**Version:** 1.0 (draft for review)\
**Date:** November 6, 2026\
**Applies to:** the ChattyOh platform (web app, public website, desktop and mobile builds)\
**Companion files:** `cursorrules.md` and `cursorsecurityrules.md` (built from sections 6 to 9 of this plan)

## 1. Purpose and how to use this plan

This plan defines **which documents the project needs, in what order, who owns them, what each must contain, and when each is "done"**. It also seeds the four documents that drive everything else (PRD, SRS, Architecture, Security Measures) with a short baseline, so the Cursor rule files can be written now and refined as those documents mature.

Use it three ways:

- **Planning:** sections 2 to 5 give the sequence, owners and timeline.
- **Writing:** section 5 is a per-document brief (inputs, contents, acceptance criteria).
- **Building:** sections 6 to 9 are the baseline requirements, architecture decisions and security controls that the Cursor rules enforce.

**Assumptions to confirm** (see section 12): team of 3 to 5 people, web-first launch, cloud hosting, an external LLM provider, and a GDPR-style privacy baseline. Durations are estimates and should be adjusted once the team and dates are known.

## 2. The document chain at a glance

```
PoC spikes (de-risk, start early)
   ↓
PRD → SRS → Architecture → Security Measures → OpenAPI
                                   ↓                 ↓
                            Threat Model        Test Plan → Test Cases → UAT Plan
                                   ↓                 ↓
                       Pen Testing Plan     Release/Deployment Plan → Incident Response Plan
                                   ↓                 ↓
                         RTM (spans everything, updated continuously)
                                   ↓
        MVP pattern → Playbook → Gap analysis → Execution guide
                                   ↓
                  cursorrules.md + cursorsecurityrules.md
```

**Ordering note.** You listed the PoC after the penetration testing plan. The PoC *report* is finalized there, but the PoC *spikes* should start in Phase 0, in parallel with the PRD, because they test the riskiest assumptions (real LLM streaming through a gateway, tenant isolation, agent approvals) before the SRS and Architecture lock those assumptions in. The plan below follows that approach.

## 3. Operating principles

1. **One source of truth per fact.** Requirements live in the PRD/SRS only. Other documents *link* to IDs; they do not restate requirements.
2. **Everything gets an ID.** Stable IDs make the RTM possible (section 4).
3. **Docs are versioned like code.** Markdown in the repository, reviewed by pull request, tagged with the release they describe.
4. **Each document has an owner, a reviewer and a definition of done** (section 5). "Draft" documents cannot be used as inputs for a release gate.
5. **Honesty rule.** Any capability that is simulated or planned is labeled that way in every document, the UI and the website. (This comes straight from the platform audit.)
6. **Change control.** Changes to an approved document require a change note listing affected IDs and downstream documents.
7. **Security is a thread, not a phase.** Security Measures, Threat Model, Pen Testing Plan and Incident Response Plan are inputs to design, not afterthoughts.

### Roles (RACI shorthand)

| Role | Typical responsibilities |
| --- | --- |
| **PO** Product Owner | PRD, UAT plan, MVP pattern, release go/no-go |
| **TL** Tech Lead / Architect | SRS (with PO), Architecture, OpenAPI, execution guide |
| **SEC** Security Lead | Security Measures, Threat Model, Pen Testing Plan, Incident Response Plan |
| **QA** QA Lead | Test Plan, Test Cases, RTM upkeep, UAT facilitation |
| **OPS** DevOps / SRE | Release/Deployment Plan, Incident Response Plan (runbooks), playbook |
| **LEG** Legal / Compliance (advisory) | Privacy, terms, claims review |

## 4. Traceability model

**ID scheme**

| Prefix | Meaning | Example |
| --- | --- | --- |
| `PRD-G`, `PRD-F`, `PRD-M` | Goal, feature, metric | `PRD-F-012` |
| `SRS-FR`, `SRS-NFR` | Functional / non-functional requirement | `SRS-FR-CHAT-003` |
| `ARCH-ADR` | Architecture decision record | `ARCH-ADR-004` |
| `SEC-C` | Security control | `SEC-C-09` |
| `API-` | OpenAPI operation (`operationId`) | `API-createProject` |
| `THR-` | Threat (STRIDE category in the ID) | `THR-S-007` |
| `TC-` | Test case | `TC-CHAT-021` |
| `UAT-` | UAT scenario | `UAT-004` |
| `REL-`, `INC-`, `PT-` | Release step, incident runbook, pen-test scope item | `INC-03` |

**RTM columns:** PRD item → SRS requirement(s) → ADR/architecture component → SEC control(s) → API operation(s) → Threat(s) → Test case(s) → UAT scenario → Release version → Status. Rule: *no requirement is "done" without at least one passing test case; no high-rated threat is "closed" without a control and a test.*

## 5. Document-by-document plan

### 5.1 Summary table

| # | Document | Owner | Main inputs | Feeds | Target (weeks, from start) |
| --- | --- | --- | --- | --- | --- |
| 1 | PRD | PO | Vision, spec, audit | SRS, UAT, MVP | 1–3 |
| 2 | SRS | TL + PO | PRD | Architecture, OpenAPI, Test Plan | 2–4 |
| 3 | Architecture | TL | SRS, PoC | Security, OpenAPI, Release | 3–5 |
| 4 | Security Measures | SEC | SRS, Architecture | Threat Model, OpenAPI, tests | 3–5 |
| 5 | OpenAPI | TL | SRS, Architecture, Security | Test Cases, clients | 4–6 |
| 6 | Test Plan | QA | SRS, Architecture, Security | Test Cases, UAT, Release | 4–6 |
| 7 | Threat Model | SEC | Architecture, OpenAPI | Pen Test Plan, Test Cases | 4–6 |
| 8 | Test Cases | QA | SRS, OpenAPI, Threat Model | RTM, CI | 5–8 |
| 9 | UAT Plan | PO + QA | PRD, Test Plan | Release | 6–8 |
| 10 | Release/Deployment Plan | OPS | Architecture, Test Plan | Incident Response | 6–8 |
| 11 | RTM | QA | All of the above | Gap analysis, release gate | 3→ ongoing |
| 12 | Incident Response Plan | SEC + OPS | Threat Model, Release Plan | Pen Test, playbook | 7–9 |
| 13 | Pen Testing Plan | SEC | Threat Model, Architecture | Release gate | 7–9 |
| 14 | PoC (report) | TL | Spikes from Phase 0 | Architecture, MVP | 0–2 (spikes), final by 9 |
| 15 | MVP pattern | PO + TL | PRD, PoC | Playbook, Execution guide | 2–3 draft, final by 9 |
| 16 | Playbook | OPS + TL | MVP, Release, Incident | Execution guide | 9–10 |
| 17 | Gap analysis | TL | RTM, audit, PoC | Execution guide | 9–10 (refreshed each sprint) |
| 18 | Execution guide | TL | All | Team | 10 |

### 5.2 Briefs

**1. PRD (Product Requirements Document)**

- *Purpose:* what we are building, for whom, and how we will know it works.
- *Contents:* vision and problem; personas; goals and non-goals; feature list with priorities (MoSCoW); user journeys; MVP scope boundary; success metrics; assumptions, risks, dependencies; open questions.
- *Done when:* every feature has an ID, a priority and an acceptance statement; PO and TL have signed off; non-goals are explicit (for example: no real marketplace publishing in MVP).

**2. SRS (Software Requirements Specification)**

- *Purpose:* testable, unambiguous requirements derived from the PRD.
- *Contents:* scope; actors and roles; functional requirements grouped by capability; non-functional requirements with numbers (performance, availability, accessibility, privacy, data integrity, compatibility); data requirements; external interfaces; constraints; glossary.
- *Done when:* each requirement is atomic, uses "shall", has an ID and a verification method (test, inspection, analysis); every PRD feature maps to at least one requirement.

**3. Architecture**

- *Purpose:* how the system is built to satisfy the SRS.
- *Contents:* context and container diagrams; component responsibilities; data model and tenancy; async jobs; AI/LLM gateway; deployment topology; cross-cutting concerns (logging, config, errors); ADRs with trade-offs; quality-attribute scenarios; migration path from the current prototype.
- *Done when:* every NFR has an architectural answer; ADRs exist for each irreversible choice; PoC results are reflected.

**4. Security Measures**

- *Purpose:* the concrete controls the product implements.
- *Contents:* control catalog (ID, description, where enforced, how verified); authentication and authorization model; data protection; secrets management; AI-specific controls; supply chain; logging and audit; backup and recovery; privacy handling.
- *Done when:* each control names an owner, an enforcement point in the architecture and a test; gaps against the audit findings are listed.

**5. OpenAPI specification**

- *Purpose:* the contract between clients (web, desktop, mobile) and the API.
- *Contents:* paths and operations with stable `operationId`; schemas; auth schemes; error model; pagination, idempotency and rate-limit headers; streaming endpoints (SSE/WebSocket documented alongside); examples.
- *Done when:* the spec validates with a linter, generated types compile, and every operation is linked to an SRS requirement and a security control.

**6. Test Plan**

- *Purpose:* the strategy for proving the requirements are met.
- *Contents:* scope and exclusions; test levels (unit, integration, contract, end-to-end, accessibility, performance, security); tools; environments and data; entry/exit criteria; defect severity and triage; reporting; risk-based priorities; automation targets.
- *Done when:* exit criteria are measurable (for example: all Critical/High cases pass, no open Critical or High defects, 80% domain-logic coverage).

**7. Threat Model**

- *Purpose:* find and rank what can go wrong before attackers do.
- *Contents:* assets and trust boundaries; data-flow diagrams; STRIDE analysis per flow; AI-specific threats (prompt injection, data exfiltration through tools, excessive agency, model supply chain); abuse cases; risk rating; mitigations mapped to `SEC-C` controls; residual risk.
- *Done when:* every High risk has a mitigation and a linked test; the model is reviewed whenever the architecture changes.

**8. Test Cases**

- *Purpose:* executable verification, traced to requirements and threats.
- *Contents:* ID, linked requirement/threat, preconditions, steps, expected result, data, automation status. Include negative and abuse cases (for example: cross-tenant access, oversized input, malformed stored data).
- *Done when:* every requirement and every High threat has at least one case; automated cases run in CI.

**9. UAT Plan**

- *Purpose:* confirm the product works for real users and real jobs.
- *Contents:* participants and roles; scenarios taken from PRD journeys; acceptance criteria; environment and data; schedule; defect handling; sign-off form.
- *Done when:* sign-off criteria are agreed in advance by the PO; scenarios cover each MVP persona.

**10. Release and Deployment Plan**

- *Purpose:* how a build reaches users safely.
- *Contents:* environments and promotion path; versioning and change log; pre-release gates (tests, security scans, approvals); deployment strategy (staged rollout, feature flags); data migrations; rollback procedure and triggers; monitoring and success checks; communication plan; go/no-go checklist.
- *Done when:* a rollback has been rehearsed in staging and the checklist is accepted by PO, TL, SEC and OPS.

**11. RTM (Requirements Traceability Matrix)**

- *Purpose:* prove coverage from requirement to test to release.
- *Contents:* the columns in section 4; generated from IDs where possible; coverage report.
- *Done when:* the matrix is generated by a script in CI and fails the build if a requirement has no test.

**12. Incident Response Plan**

- *Purpose:* how we detect, contain, recover from and learn from incidents.
- *Contents:* severity levels; roles and on-call; detection sources; runbooks per scenario (credential leak, data exposure, tenant isolation failure, prompt-injection abuse, AI provider outage, failed deployment); communication and legal notification steps; evidence handling; post-incident review template.
- *Done when:* a tabletop exercise has been run for at least three scenarios and findings fed back.

**13. Penetration Testing Plan**

- *Purpose:* independent validation of the security controls.
- *Contents:* scope (web, API, desktop, mobile, AI features); rules of engagement; methodology (OWASP ASVS, OWASP Top 10 for web, API and LLM applications); test accounts and environments; reporting and retest rules; severity-to-fix SLAs.
- *Done when:* scope and schedule are approved; remediation and retest are budgeted before the release date.

**14. PoC (Proof of Concept) report**

- *Purpose:* de-risk the assumptions the design depends on.
- *Contents:* hypotheses; spike design; results with evidence; decision (adopt, adapt, reject); impact on ADRs.
- *Done when:* each hypothesis has a recorded outcome. Suggested spikes: LLM gateway with streaming and cancellation; tenant isolation with row-level security; agent run with human approval; offline-capable web client with IndexedDB; Electron and Flutter wrapper builds on real devices.

**15. MVP pattern**

- *Purpose:* the rule for deciding what is in the first release and how later releases grow.
- *Contents:* the "walking skeleton" pattern (thin end-to-end slice first, then widen); scope filter (value, risk, effort); in/out list; feature-flag approach; labeling rule for simulated or preview features; exit criteria for MVP.
- *Done when:* the in/out list traces to PRD IDs and is accepted by PO and TL.

**16. Playbook**

- *Purpose:* repeatable procedures for the team.
- *Contents:* branching and review workflow; how to add an entity or endpoint (spec, migration, tests, docs); release day; hotfix; on-call; dependency updates; how to run a security review; how to update documents and the RTM.
- *Done when:* a new team member can ship a small change using only the playbook.

**17. Gap analysis**

- *Purpose:* current state versus target, with a prioritized plan.
- *Contents:* dimension-by-dimension comparison (functional, data, security, quality, operations); gap, impact, effort, priority; owner and target sprint. Seeded in section 10 from the platform audit.
- *Done when:* every gap has an owner and a date; refreshed every sprint.

**18. Execution guide**

- *Purpose:* the step-by-step path from today to MVP release.
- *Contents:* epics and milestones; sprint plan; dependency order; definition of ready and done; quality gates; risk register; reporting cadence; decision log.
- *Done when:* milestones have dates, owners and exit criteria, and the first two sprints are fully specified.

## 6. Baseline: PRD (seed for `cursorrules.md`)

**Vision.** One agent-assisted workspace to take an idea from conversation to a deployed, documented, tested product, with the human always in control.

**Goals**

- `PRD-G-01` Reduce time from idea to first working project (target: first project created in under 10 minutes).
- `PRD-G-02` Keep humans in control: approvals for sensitive actions.
- `PRD-G-03` Be trustworthy: label simulated or preview features; keep an audit trail.
- `PRD-G-04` Work on web first, then desktop and mobile from the same codebase.

**Personas:** solo maker; product/dev team lead; admin or security reviewer; agency delivery lead.

**MVP in scope**

- `PRD-F-01` Accounts and workspaces (Personal, Team) with roles.
- `PRD-F-02` Projects, tasks and a lifecycle status model.
- `PRD-F-03` ChatMode with a real LLM, streaming, history, commands.
- `PRD-F-04` SpecMode: generate, edit and approve documents.
- `PRD-F-05` Agents: create, test, approve, run; execution history.
- `PRD-F-06` Audit log, notifications, import/export, backup/restore.
- `PRD-F-07` Accessible UI (WCAG 2.2 AA), light and dark themes.

**MVP out of scope:** real cloud deployments and marketplace publishing, SSO/SCIM, billing, real-time co-editing, native UI rewrite, offline AI.

**Metrics:** activation rate; weekly active workspaces; document acceptance rate; agent run success rate; p95 latency; accessibility defects; defect escape rate.

## 7. Baseline: SRS (seed for `cursorrules.md`)

**Functional groups:** `FR-AUTH` sign-in, sessions, roles; `FR-WS` workspaces and projects; `FR-CHAT` conversations and commands; `FR-DOC` document generation and approval; `FR-AGENT` agents and executions; `FR-TASK` tasks; `FR-AUDIT` audit and notifications; `FR-IO` import/export.

**Key non-functional requirements**

| ID | Requirement |
| --- | --- |
| `SRS-NFR-PERF-01` | API p95 ≤ 300 ms for CRUD; UI interaction feedback ≤ 100 ms; lists of 5,000 records stay responsive (pagination or virtualization). |
| `SRS-NFR-AVAIL-01` | 99.5% monthly availability for MVP; recovery time objective 4 h, recovery point objective 15 min. |
| `SRS-NFR-DATA-01` | No silent data loss: every failed write is reported to the user; schema versioned with migrations; stored data validated on load with a safe-mode fallback. |
| `SRS-NFR-DATA-02` | Entities reference each other by immutable ID, never by display name. |
| `SRS-NFR-INT-01` | Business rules (release gates, approval requirements) are enforced server-side in one rules module; clients cannot bypass them by editing status fields. |
| `SRS-NFR-CONC-01` | Background jobs and streamed replies are bound to the tenant and entity IDs that started them; replies are matched to messages by ID. |
| `SRS-NFR-A11Y-01` | WCAG 2.2 AA: contrast, focus management in dialogs, live regions for status messages, minimum target size, reduced-motion support. |
| `SRS-NFR-PRIV-01` | Retention and deletion controls; export of a user's data; disclosure of AI processing. |
| `SRS-NFR-OBS-01` | Structured logs, traces and metrics with no secrets or personal content. |
| `SRS-NFR-COMPAT-01` | Current evergreen browsers; desktop (Windows, macOS, Linux); iOS and Android through the shared codebase. |
| `SRS-NFR-MAINT-01` | TypeScript strict mode; 80% coverage on domain logic; automated RTM check in CI. |

## 8. Baseline: Architecture (seed for `cursorrules.md`)

**Target shape (modular monolith first):** clients (web SPA/PWA; Electron and Flutter shells hosting the same UI) → API (NestJS, REST described by OpenAPI, SSE/WebSocket for streaming) → domain modules (identity, workspace/project, chat, docs, agents, tasks, audit) → PostgreSQL (row-level security; pgvector later), Redis, S3-compatible storage → background workers (BullMQ) → **LLM gateway** (provider-agnostic, policy and quota enforcement) → observability (OpenTelemetry).

**Reference stack (from your spec, trimmed for MVP):** Next.js or Vite with React and TypeScript, Tailwind, Zustand and TanStack Query; NestJS; PostgreSQL with Prisma; Redis with BullMQ; S3-compatible storage; Playwright and Vitest; GitHub Actions; Docker. Search, vector store and Kubernetes are deferred until needed.

| ADR | Decision |
| --- | --- |
| `ARCH-ADR-001` | Modular monolith first; split services only when a boundary proves necessary. |
| `ARCH-ADR-002` | OpenAPI-first: the spec is written first; types and clients are generated. |
| `ARCH-ADR-003` | Immutable IDs for all relationships; display names are attributes. |
| `ARCH-ADR-004` | All business rules live in a server-side domain layer; UI only requests actions. |
| `ARCH-ADR-005` | Tenant isolation through `tenant_id` on every row plus database row-level security. |
| `ARCH-ADR-006` | Every LLM call goes through the gateway; no provider keys in clients. |
| `ARCH-ADR-007` | One shared UI codebase; platform differences are isolated behind a small bridge interface (web, Electron, Flutter). |
| `ARCH-ADR-008` | Background jobs are idempotent and carry the tenant and entity IDs that created them. |
| `ARCH-ADR-009` | Client persistence (offline cache) uses IndexedDB with schema versions; never `localStorage` for secrets or tokens. |

## 9. Baseline: Security Measures (seed for `cursorsecurityrules.md`)

| ID | Control |
| --- | --- |
| `SEC-C-01` | Authentication through OpenID Connect with multi-factor option; short-lived sessions; secure, HttpOnly, SameSite cookies. |
| `SEC-C-02` | Authorization is deny-by-default, checked server-side on every request (roles plus project-level attributes). |
| `SEC-C-03` | Tenant isolation enforced in the data layer (row-level security) and tested with cross-tenant cases. |
| `SEC-C-04` | Secrets only in a secrets manager; never in the client, logs, exports, backups or prompts. |
| `SEC-C-05` | TLS 1.2 or higher everywhere; encryption at rest; key rotation. |
| `SEC-C-06` | Validate all input against schemas at the boundary; limit sizes; reject unknown fields. |
| `SEC-C-07` | Encode all output; strict Content Security Policy; no inline script without nonce or hash. |
| `SEC-C-08` | Rate limits, quotas and spending limits per user, tenant and agent. |
| `SEC-C-09` | AI safety: prompt-injection defenses, tool allow-lists, output validation, human approval for sensitive actions. |
| `SEC-C-10` | Agent sandboxing: execution time, step and cost limits; no ambient credentials. |
| `SEC-C-11` | Supply chain: lockfiles, vulnerability scanning, SBOM, pinned versions that are at least 14 days old, signed builds. |
| `SEC-C-12` | Immutable audit log of security-relevant events; logs contain no secrets or personal content. |
| `SEC-C-13` | Encrypted backups, tested restores, documented retention and deletion. |
| `SEC-C-14` | Secure SDLC gates in CI: SAST, secret scanning, dependency scan, container scan, license check. |
| `SEC-C-15` | Privacy: data minimization, consent for AI processing, data export and erasure. |
| `SEC-C-16` | Incident response runbooks tested at least twice a year. |

## 10. Gap analysis seed (from the platform audit)

| Area | Current state (prototype) | Target | Priority |
| --- | --- | --- | --- |
| Persistence | Browser storage; whole database in one key | Server database plus IndexedDB cache; per-record writes; migrations | High |
| Identity | None | OIDC, roles, tenant isolation | High |
| Integrity | Rules in the UI; links by name; statuses editable | Server rules; ID links; derived statuses | High |
| Secrets | Plain text in client storage and exports | Secrets manager; masked in all outputs | High |
| AI | Runtime-dependent; fallback text | LLM gateway; streaming; approvals; quotas | High |
| Integrations | Simulated | Real, one at a time, each labeled until real | Medium |
| Accessibility | Contrast, dialog focus, live regions, target size gaps | WCAG 2.2 AA verified | Medium |
| Quality | Ad-hoc browser scripts | CI suite, RTM check, performance tests | Medium |
| Delivery | Four copies of one HTML file | One codebase; platform bridges; signed builds | Medium |
| Website | Placeholders; overstated claims; no real form backend | Accurate claims; legal pages; working contact flow | Medium |
| Native builds | Never compiled or run | CI builds; device testing; store readiness | Medium |

## 11. Timeline and phases

| Phase | Weeks | Deliverables | Gate to leave the phase |
| --- | --- | --- | --- |
| 0 Discovery | 0–2 | PoC spikes, PRD draft, MVP pattern draft | Spike results reviewed |
| 1 Definition | 1–5 | PRD, SRS, Architecture, Security Measures | Four documents approved |
| 2 Contracts and risk | 3–6 | OpenAPI, Threat Model | Spec lints; High threats mitigated on paper |
| 3 Verification design | 4–8 | Test Plan, Test Cases, UAT Plan, Pen Testing Plan | RTM shows full coverage plan |
| 4 Release readiness | 6–9 | Release/Deployment Plan, Incident Response Plan, RTM baseline | Rollback and tabletop rehearsed |
| 5 Execution | 9–10 | PoC report, MVP pattern, playbook, gap analysis, execution guide | Go decision for build |

Documents in phases 2 to 4 overlap with early implementation of the walking skeleton; they must not block it.

## 12. Decisions needed from you

1. **Hosting and cloud provider** (affects deployment plan and IaC).
2. **Identity provider** (build vs. managed OIDC).
3. **LLM provider(s)** and data-handling terms (affects gateway design and privacy text).
4. **Compliance targets** (GDPR only, or SOC 2 / ISO 27001 as well).
5. **Team size and dates** (calibrates the timeline).
6. **Native apps:** keep the WebView approach, or plan a native Flutter UI after MVP.
7. **Tenancy:** single database with row-level security (recommended) or separate databases for enterprise.

## 13. How the two Cursor rule files are built

| File | Built from | What it does |
| --- | --- | --- |
| `cursorrules.md` | PRD (section 6), SRS (7), Architecture (8) | Tells the AI coding assistant what the product is, the stack, structure, conventions, data and API rules, testing and accessibility requirements, and the definition of done, with ID references for traceability. |
| `cursorsecurityrules.md` | Security Measures (9), Threat Model categories (STRIDE and AI risks), SRS security NFRs | Defines secure-by-default coding rules, forbidden patterns, AI/agent safety rules, supply-chain and CI gates, and what requires human security review. |

When the real PRD, SRS, Architecture and Security Measures are approved, update the files and bump their version; every rule carries the ID of the requirement, decision or control it enforces so changes are easy to trace.

## 14. Definition of done for this plan

- Owners, reviewers and dates assigned for all 18 documents.
- Section 12 decisions recorded.
- Repository folder structure created: `/docs/01-prd` … `/docs/18-execution-guide`, plus `/docs/rtm` and `/rules`.
- Cursor rule files committed and linked from the README.
