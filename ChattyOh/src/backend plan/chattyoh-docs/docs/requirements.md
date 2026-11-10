# Requirements

**Project:** ChattyOh Inc · **Generated from:** `docs/02-srs.md` by `tools/gen_requirements.py` — **do not edit by hand**; change the SRS and regenerate.
**Purpose:** a readable register of every requirement grouped by product feature, with priority, release slice, verification method and linked user stories. Detail, rationale, architecture decisions and security controls for each requirement are in the SRS; traceability to tests and APIs is in `11-rtm.md`.

## Summary

45 requirements: MVP-0 = 15, MVP-1 = 24, MVP-2 = 6.

Priority comes from the PRD feature (Must / Should); quality-attribute requirements are Must. Slice: MVP-0 walking skeleton, MVP-1 complete core, MVP-2 hardening (see `15-mvp-pattern.md`).

## Accounts and workspaces (Personal, Team) with roles (PRD-F-01)

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-AUTH-001 | The system shall authenticate users through an OpenID Connect provider and establish a server-side session. | MVP-0 | Test | US-001 |
| SRS-FR-AUTH-002 | The system shall support optional multi-factor authentication and shall require re-authentication before sensitive actions (role change, export, agent deployment approval). | MVP-1 | Test | US-002 |
| SRS-FR-AUTH-003 | The system shall let users list and revoke active sessions and shall invalidate a session on the server at logout. | MVP-1 | Test | US-003 |
| SRS-FR-WS-001 | The system shall let a user create, rename and switch workspaces (Personal, Team); each workspace is an isolated tenant. | MVP-0 | Test | US-004 |
| SRS-FR-WS-002 | The system shall let Owners and Admins invite members and assign roles; role changes shall be audited. | MVP-1 | Test | US-005, US-006 |

## Projects, tasks and a lifecycle model (PRD-F-02)

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-WS-003 | The system shall provide create, read, update and archive operations for projects, which shall be referenced by immutable ID. | MVP-0 | Test | US-007 |
| SRS-FR-WS-004 | The system shall change a project's lifecycle stage only through an action that enforces gates: the action shall be refused while the project has failing tests or open Critical findings. | MVP-1 | Test | US-009 |
| SRS-FR-WS-005 | The system shall archive projects without destroying data and shall let authorized users restore them. | MVP-1 | Test | US-010 |
| SRS-FR-TASK-001 | The system shall provide create, read, update and delete operations for tasks linked to a project by ID. | MVP-0 | Test | US-011 |
| SRS-FR-TASK-002 | The system shall support task status, priority, due date, filtering and search, with validated inputs. | MVP-1 | Test | US-012 |

## ChatMode with a real LLM (PRD-F-03)

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-CHAT-001 | The system shall provide conversations that users can create, rename, delete and export. | MVP-0 | Test | US-014 |
| SRS-FR-CHAT-002 | The system shall stream model replies through the LLM gateway and shall show the model used and whether the reply is real or a fallback. | MVP-0 | Test | US-013 |
| SRS-FR-CHAT-003 | The system shall bind each reply to a message ID and shall allow only one pending reply per conversation (further sends are queued or refused with a visible reason). | MVP-0 | Test | US-015 |
| SRS-FR-CHAT-004 | The system shall support slash commands that create and list items through the same domain actions as the UI, so gates and permissions apply. | MVP-1 | Test | US-016 |
| SRS-FR-CHAT-005 | The system shall let a user stop a running reply and shall cancel the upstream request. | MVP-1 | Test | US-017 |

## SpecMode documents (PRD-F-04)

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-DOC-001 | The system shall provide documents of defined types (BRD, PRD, SRS, Architecture, API Docs, Test Plan, Security, Runbook) with create, read, update and archive. | MVP-1 | Test | US-018 |
| SRS-FR-DOC-002 | The system shall generate document drafts through the gateway, label them as drafts, and shall never include another tenant's data in the prompt. | MVP-1 | Test | US-019 |
| SRS-FR-DOC-003 | The system shall enforce the workflow Draft → In review → Approved, allow approval only by roles permitted in section 2, and audit each transition. | MVP-1 | Test | US-020 |
| SRS-FR-DOC-004 | The system shall keep a version history of documents and let authorized users restore a previous version. | MVP-2 | Test | US-021 |

## Agents with approvals (PRD-F-05)

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-AGENT-001 | The system shall provide agent definitions (name, type, model, instructions, tool allow-list) with validated tool arguments. | MVP-1 | Test | US-022 |
| SRS-FR-AGENT-002 | The system shall let a user test an agent and record the result; an agent shall reach *Testing* status only when its configuration and test prompts pass. | MVP-1 | Test | US-023 |
| SRS-FR-AGENT-003 | The system shall refuse to deploy an agent that has not passed testing and shall require human approval when the workspace policy enables it. | MVP-1 | Test | US-024 |
| SRS-FR-AGENT-004 | The system shall run agents through the gateway within enforced step, time and cost limits and shall require human approval, showing exact arguments, before any sensitive tool call. | MVP-1 | Test | US-025 |
| SRS-FR-AGENT-005 | The system shall record each execution with agent version, input, output, tool calls, cost, duration and approver. | MVP-1 | Test | US-026 |
| SRS-FR-AGENT-006 | The system shall let authorized users pause and resume a deployed agent. | MVP-2 | Test | US-027 |

## Audit, notifications, import/export, backup (PRD-F-06)

Priority: **Should**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-AUDIT-001 | The system shall write append-only audit events for security-relevant actions and let only Owners and Admins read them. | MVP-0 | Test | US-006, US-028 |
| SRS-FR-AUDIT-002 | The system shall create in-app notifications for approvals, failures and completions and let users mark them read. | MVP-1 | Test | US-029 |
| SRS-FR-IO-001 | The system shall export workspace data as versioned JSON that contains no secret values or tokens. | MVP-1 | Test | US-030 |
| SRS-FR-IO-002 | The system shall import data only after schema validation, size limits and a preview, and shall merge without overwriting existing records. | MVP-1 | Test | US-031 |
| SRS-FR-IO-003 | The system shall support backup and restore with a schema version and shall snapshot current data before a restore. | MVP-2 | Test | US-032 |

## Accessible, consistent UI (PRD-F-07)

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-UI-001 | The UI shall provide top navigation (Home, MyModes, platform groups), a collapsible sidebar and a menu with Expand All and Collapse All. | MVP-0 | Test | US-033 |
| SRS-FR-UI-003 | The UI shall offer light and dark themes and remember the user's choice. | MVP-0 | Test | US-035 |
| SRS-NFR-A11Y-01 | Core journeys shall meet WCAG 2.2 AA: contrast, dialog focus management, live regions for status messages, minimum target size, keyboard operability and reduced-motion support. | MVP-1 | Test | US-036 |

## Quality attributes and cross-cutting rules

Priority: **Must**

| ID | Requirement | Slice | Verification | User stories |
|---|---|---|---|---|
| SRS-FR-UI-002 | The UI shall visibly label any simulated, preview or planned feature. | MVP-0 | Inspection | US-034 |
| SRS-NFR-PERF-01 | API p95 latency shall be ≤ 300 ms for CRUD operations at the target load; UI interaction feedback shall be ≤ 100 ms; lists of 5,000 records shall stay responsive through pagination or virtualization. | MVP-1 | Test | US-040 |
| SRS-NFR-AVAIL-01 | Monthly availability shall be ≥ 99.5%, with recovery time objective 4 h and recovery point objective 15 min. | MVP-2 | Test | US-042 |
| SRS-NFR-DATA-01 | No write failure shall be silent: the user shall be told. Stored data shall be schema-versioned, validated on load, and a safe mode shall keep the app usable and preserve a copy when data is invalid. | MVP-0 | Test | US-037 |
| SRS-NFR-DATA-02 | Entities shall reference each other by immutable ID, never by display name. | MVP-0 | Test | US-008 |
| SRS-NFR-INT-01 | Business rules (gates, approvals) shall be enforced server-side in one rules module; clients shall not be able to bypass them by editing status fields. | MVP-1 | Test | US-009 |
| SRS-NFR-CONC-01 | Background jobs and streamed replies shall carry the tenant and entity IDs that started them and shall write results only there, even if the user switches workspace. | MVP-0 | Test | US-015 |
| SRS-NFR-PRIV-01 | The system shall provide data export, erasure and retention controls and shall disclose AI processing to users. | MVP-2 | Inspection | US-039 |
| SRS-NFR-OBS-01 | Logs, traces and metrics shall be structured, carry request and tenant IDs, and contain no secrets or personal content. | MVP-1 | Test | US-041 |
| SRS-NFR-COMPAT-01 | The product shall run on current evergreen browsers, Windows/macOS/Linux (Electron shell), and iOS/Android (WebView shell) from one UI codebase. | MVP-2 | Test | US-038 |
| SRS-NFR-MAINT-01 | Code shall be TypeScript strict; domain logic coverage ≥ 80%; CI shall fail when a requirement has no linked test. | MVP-0 | Analysis | US-043 |
| SRS-NFR-SEC-01 | The controls in `04-security-measures.md` shall be implemented, verified in CI where automatable, and tested through incident exercises. | MVP-1 | Test | US-044 |
