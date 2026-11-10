# 02 — Software Requirements Specification (SRS)

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owners:** Tech Lead + Product Owner · **Status:** Draft
**Upstream:** `01-prd.md` · **Downstream:** `03-architecture.md`, `04-security-measures.md`, `05-openapi`, `06-test-plan.md`, `08-test-cases.md`

## 1. Introduction

**Purpose.** Testable requirements that implement the PRD. "Shall" marks a mandatory requirement. Every requirement has an ID, a PRD source, linked architecture decisions and security controls, a verification method and a release slice.

**Definitions.** *Tenant* = a workspace. *Gate* = a rule that blocks a state change until conditions hold (for example no failing tests). *Gateway* = the LLM gateway module. *Slice* = MVP-0, MVP-1 or MVP-2 (see `15-mvp-pattern.md`).

## 2. Actors and permissions

Roles: **Owner**, **Admin**, **Developer**, **Viewer**. Permissions are enforced server-side (SEC-C-02).

| Action | Owner | Admin | Developer | Viewer |
|---|---|---|---|---|
| Manage workspace settings, delete workspace | ✔ | – | – | – |
| Invite members, change roles | ✔ | ✔ | – | – |
| View audit log | ✔ | ✔ | – | – |
| Create/edit projects, tasks, documents, conversations | ✔ | ✔ | ✔ | – |
| Advance project (through gates) | ✔ | ✔ | ✔ | – |
| Approve documents | ✔ | ✔ | – | – |
| Approve agent deployment / sensitive agent actions | ✔ | ✔ | – | – |
| Run agents | ✔ | ✔ | ✔ | – |
| Export workspace data | ✔ | ✔ | – | – |
| Read projects, tasks, documents | ✔ | ✔ | ✔ | ✔ |

## 3. Functional requirements

Columns: **Source** = PRD item · **ADR** = architecture decision(s) · **SEC** = security control(s) · **Verif** = Test, Inspection or Analysis · **Slice** = release slice.

| ID | Requirement | Source | ADR | SEC | Verif | Slice |
|---|---|---|---|---|---|---|
| SRS-FR-AUTH-001 | The system shall authenticate users through an OpenID Connect provider and establish a server-side session. | PRD-F-01 | ARCH-ADR-010 | SEC-C-01 | Test | MVP-0 |
| SRS-FR-AUTH-002 | The system shall support optional multi-factor authentication and shall require re-authentication before sensitive actions (role change, export, agent deployment approval). | PRD-F-01 | ARCH-ADR-010 | SEC-C-01 | Test | MVP-1 |
| SRS-FR-AUTH-003 | The system shall let users list and revoke active sessions and shall invalidate a session on the server at logout. | PRD-F-01 | ARCH-ADR-010 | SEC-C-01,SEC-C-12 | Test | MVP-1 |
| SRS-FR-WS-001 | The system shall let a user create, rename and switch workspaces (Personal, Team); each workspace is an isolated tenant. | PRD-F-01 | ARCH-ADR-005 | SEC-C-03 | Test | MVP-0 |
| SRS-FR-WS-002 | The system shall let Owners and Admins invite members and assign roles; role changes shall be audited. | PRD-F-01 | ARCH-ADR-005 | SEC-C-02,SEC-C-12 | Test | MVP-1 |
| SRS-FR-WS-003 | The system shall provide create, read, update and archive operations for projects, which shall be referenced by immutable ID. | PRD-F-02 | ARCH-ADR-003 | SEC-C-02 | Test | MVP-0 |
| SRS-FR-WS-004 | The system shall change a project's lifecycle stage only through an action that enforces gates: the action shall be refused while the project has failing tests or open Critical findings. | PRD-F-02 | ARCH-ADR-004 | SEC-C-02 | Test | MVP-1 |
| SRS-FR-WS-005 | The system shall archive projects without destroying data and shall let authorized users restore them. | PRD-F-02 | ARCH-ADR-003 | SEC-C-12 | Test | MVP-1 |
| SRS-FR-TASK-001 | The system shall provide create, read, update and delete operations for tasks linked to a project by ID. | PRD-F-02 | ARCH-ADR-003 | SEC-C-02 | Test | MVP-0 |
| SRS-FR-TASK-002 | The system shall support task status, priority, due date, filtering and search, with validated inputs. | PRD-F-02 | ARCH-ADR-004 | SEC-C-06 | Test | MVP-1 |
| SRS-FR-CHAT-001 | The system shall provide conversations that users can create, rename, delete and export. | PRD-F-03 | ARCH-ADR-001 | SEC-C-02 | Test | MVP-0 |
| SRS-FR-CHAT-002 | The system shall stream model replies through the LLM gateway and shall show the model used and whether the reply is real or a fallback. | PRD-F-03 | ARCH-ADR-006,ARCH-ADR-011 | SEC-C-09 | Test | MVP-0 |
| SRS-FR-CHAT-003 | The system shall bind each reply to a message ID and shall allow only one pending reply per conversation (further sends are queued or refused with a visible reason). | PRD-F-03 | ARCH-ADR-008 | SEC-C-06 | Test | MVP-0 |
| SRS-FR-CHAT-004 | The system shall support slash commands that create and list items through the same domain actions as the UI, so gates and permissions apply. | PRD-F-03 | ARCH-ADR-004 | SEC-C-02,SEC-C-06 | Test | MVP-1 |
| SRS-FR-CHAT-005 | The system shall let a user stop a running reply and shall cancel the upstream request. | PRD-F-03 | ARCH-ADR-011 | SEC-C-08 | Test | MVP-1 |
| SRS-FR-DOC-001 | The system shall provide documents of defined types (BRD, PRD, SRS, Architecture, API Docs, Test Plan, Security, Runbook) with create, read, update and archive. | PRD-F-04 | ARCH-ADR-003 | SEC-C-02 | Test | MVP-1 |
| SRS-FR-DOC-002 | The system shall generate document drafts through the gateway, label them as drafts, and shall never include another tenant's data in the prompt. | PRD-F-04 | ARCH-ADR-006 | SEC-C-09 | Test | MVP-1 |
| SRS-FR-DOC-003 | The system shall enforce the workflow Draft → In review → Approved, allow approval only by roles permitted in section 2, and audit each transition. | PRD-F-04 | ARCH-ADR-004 | SEC-C-02,SEC-C-12 | Test | MVP-1 |
| SRS-FR-DOC-004 | The system shall keep a version history of documents and let authorized users restore a previous version. | PRD-F-04 | ARCH-ADR-003 | SEC-C-12 | Test | MVP-2 |
| SRS-FR-AGENT-001 | The system shall provide agent definitions (name, type, model, instructions, tool allow-list) with validated tool arguments. | PRD-F-05 | ARCH-ADR-003 | SEC-C-02,SEC-C-10 | Test | MVP-1 |
| SRS-FR-AGENT-002 | The system shall let a user test an agent and record the result; an agent shall reach *Testing* status only when its configuration and test prompts pass. | PRD-F-05 | ARCH-ADR-004 | SEC-C-09 | Test | MVP-1 |
| SRS-FR-AGENT-003 | The system shall refuse to deploy an agent that has not passed testing and shall require human approval when the workspace policy enables it. | PRD-F-05 | ARCH-ADR-004 | SEC-C-09,SEC-C-12 | Test | MVP-1 |
| SRS-FR-AGENT-004 | The system shall run agents through the gateway within enforced step, time and cost limits and shall require human approval, showing exact arguments, before any sensitive tool call. | PRD-F-05 | ARCH-ADR-006,ARCH-ADR-008 | SEC-C-08,SEC-C-09,SEC-C-10 | Test | MVP-1 |
| SRS-FR-AGENT-005 | The system shall record each execution with agent version, input, output, tool calls, cost, duration and approver. | PRD-F-05 | ARCH-ADR-008 | SEC-C-12 | Test | MVP-1 |
| SRS-FR-AGENT-006 | The system shall let authorized users pause and resume a deployed agent. | PRD-F-05 | ARCH-ADR-004 | SEC-C-02 | Test | MVP-2 |
| SRS-FR-AUDIT-001 | The system shall write append-only audit events for security-relevant actions and let only Owners and Admins read them. | PRD-F-06 | ARCH-ADR-004 | SEC-C-12 | Test | MVP-0 |
| SRS-FR-AUDIT-002 | The system shall create in-app notifications for approvals, failures and completions and let users mark them read. | PRD-F-06 | ARCH-ADR-008 | SEC-C-12 | Test | MVP-1 |
| SRS-FR-IO-001 | The system shall export workspace data as versioned JSON that contains no secret values or tokens. | PRD-F-06 | ARCH-ADR-004 | SEC-C-04,SEC-C-15 | Test | MVP-1 |
| SRS-FR-IO-002 | The system shall import data only after schema validation, size limits and a preview, and shall merge without overwriting existing records. | PRD-F-06 | ARCH-ADR-002 | SEC-C-06 | Test | MVP-1 |
| SRS-FR-IO-003 | The system shall support backup and restore with a schema version and shall snapshot current data before a restore. | PRD-F-06 | ARCH-ADR-009 | SEC-C-13 | Test | MVP-2 |
| SRS-FR-UI-001 | The UI shall provide top navigation (Home, MyModes, platform groups), a collapsible sidebar and a menu with Expand All and Collapse All. | PRD-F-07 | ARCH-ADR-007 | SEC-C-07 | Test | MVP-0 |
| SRS-FR-UI-002 | The UI shall visibly label any simulated, preview or planned feature. | PRD-G-03 | ARCH-ADR-007 | SEC-C-07 | Inspection | MVP-0 |
| SRS-FR-UI-003 | The UI shall offer light and dark themes and remember the user's choice. | PRD-F-07 | ARCH-ADR-007 | SEC-C-07 | Test | MVP-0 |

## 4. Non-functional requirements

| ID | Requirement | Source | ADR | SEC | Verif | Slice |
|---|---|---|---|---|---|---|
| SRS-NFR-PERF-01 | API p95 latency shall be ≤ 300 ms for CRUD operations at the target load; UI interaction feedback shall be ≤ 100 ms; lists of 5,000 records shall stay responsive through pagination or virtualization. | PRD-M-05 | ARCH-ADR-009 | SEC-C-08 | Test | MVP-1 |
| SRS-NFR-AVAIL-01 | Monthly availability shall be ≥ 99.5%, with recovery time objective 4 h and recovery point objective 15 min. | PRD-M-06 | ARCH-ADR-001 | SEC-C-13 | Test | MVP-2 |
| SRS-NFR-DATA-01 | No write failure shall be silent: the user shall be told. Stored data shall be schema-versioned, validated on load, and a safe mode shall keep the app usable and preserve a copy when data is invalid. | PRD-G-03 | ARCH-ADR-009 | SEC-C-13 | Test | MVP-0 |
| SRS-NFR-DATA-02 | Entities shall reference each other by immutable ID, never by display name. | PRD-G-03 | ARCH-ADR-003 | SEC-C-02 | Test | MVP-0 |
| SRS-NFR-INT-01 | Business rules (gates, approvals) shall be enforced server-side in one rules module; clients shall not be able to bypass them by editing status fields. | PRD-G-02 | ARCH-ADR-004 | SEC-C-02 | Test | MVP-1 |
| SRS-NFR-CONC-01 | Background jobs and streamed replies shall carry the tenant and entity IDs that started them and shall write results only there, even if the user switches workspace. | PRD-G-03 | ARCH-ADR-008 | SEC-C-03 | Test | MVP-0 |
| SRS-NFR-A11Y-01 | Core journeys shall meet WCAG 2.2 AA: contrast, dialog focus management, live regions for status messages, minimum target size, keyboard operability and reduced-motion support. | PRD-F-07 | ARCH-ADR-007 | SEC-C-07 | Test | MVP-1 |
| SRS-NFR-PRIV-01 | The system shall provide data export, erasure and retention controls and shall disclose AI processing to users. | PRD-G-03 | ARCH-ADR-005 | SEC-C-15 | Inspection | MVP-2 |
| SRS-NFR-OBS-01 | Logs, traces and metrics shall be structured, carry request and tenant IDs, and contain no secrets or personal content. | PRD-G-03 | ARCH-ADR-001 | SEC-C-12 | Test | MVP-1 |
| SRS-NFR-COMPAT-01 | The product shall run on current evergreen browsers, Windows/macOS/Linux (Electron shell), and iOS/Android (WebView shell) from one UI codebase. | PRD-G-04 | ARCH-ADR-007 | SEC-C-11 | Test | MVP-2 |
| SRS-NFR-MAINT-01 | Code shall be TypeScript strict; domain logic coverage ≥ 80%; CI shall fail when a requirement has no linked test. | PRD-G-04 | ARCH-ADR-002 | SEC-C-14 | Analysis | MVP-0 |
| SRS-NFR-SEC-01 | The controls in `04-security-measures.md` shall be implemented, verified in CI where automatable, and tested through incident exercises. | PRD-G-02 | ARCH-ADR-001 | SEC-C-05,SEC-C-11,SEC-C-14,SEC-C-16 | Test | MVP-1 |

## 5. Data requirements

Core entities (all carry `id`, `tenantId`, `createdAt`, `updatedAt`, `schemaVersion`): User, Workspace, Membership, Project, Task, Conversation, Message, Document, DocumentVersion, Agent, Execution, Approval, AuditEvent, Notification. Relationships use IDs. Field limits: text ≤ 200,000 characters, imports ≤ 2,000 records, uploads ≤ 10 MB.

## 6. External interfaces

REST API described in `packages/contracts/openapi.yaml`; streaming over Server-Sent Events; OIDC provider; LLM provider via the gateway; object storage; email/notification provider (later).

## 7. Constraints

TypeScript, NestJS, PostgreSQL (see `03-architecture.md`); privacy baseline ASM-04; MVP excludes PRD non-goals.

## 8. Verification

Each requirement is verified as stated in **Verif**. Test cases are in `08-test-cases.md`; coverage is checked by `tools/rtm.py` and recorded in `docs/rtm/`.

## 9. Open issues

Decisions listed in PRD section 9 may add or change requirements; changes follow the change-control rule in the playbook.
