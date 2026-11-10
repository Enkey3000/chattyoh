# 05 — OpenAPI Specification

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Tech Lead · **Status:** Draft
**Contract file:** `packages/contracts/openapi.yaml` (OpenAPI 3.1) · **Upstream:** `02-srs.md`, `03-architecture.md`, `04-security-measures.md` · **Downstream:** `08-test-cases.md`, generated clients

## 1. Conventions

- **Spec first** (ARCH-ADR-002): change the YAML, lint, regenerate types, then implement. The first version of the file was generated from the operation inventory below; from now on edit the YAML directly.
- **Traceability:** every operation has `operationId` (referenced as `API-<operationId>`), `x-srs` (requirements), `x-sec` (controls) and `x-min-role`.
- **Auth:** bearer JWT (desktop/mobile shells) or HttpOnly session cookie (web). User and tenant are derived from the session; the workspace in the path must match a membership.
- **Errors:** `{code, message, details?, requestId}`; `404` is also used for other tenants' IDs (no existence leaks).
- **Pagination:** `cursor` and `limit` (≤ 100). **Idempotency:** `Idempotency-Key` on creating POSTs.
- **Gates:** project `stage`/`status`, document `status`, agent `status` and approvals are read-only; they change only through action endpoints, which return `409` with a `GateError` when refused.
- **Streaming:** `sendMessage` returns Server-Sent Events tagged with the reply message ID; a second send while a reply is pending returns `409`; `cancelMessage` stops the reply and the upstream request.
- **Limits:** text fields ≤ 200,000 characters; imports ≤ 2,000 records; unknown fields rejected.
- **Validation in CI:** Spectral lint, contract tests (Schemathesis/Dredd), type generation must compile.

## 2. Operation inventory (55 operations)

| Operation ID | Method and path | Min role | Requirements | Controls |
|---|---|---|---|---|
| API-getMe | `GET /v1/me` | any | SRS-FR-AUTH-001 | SEC-C-01 |
| API-listSessions | `GET /v1/sessions` | any | SRS-FR-AUTH-003 | SEC-C-01 |
| API-revokeSession | `DELETE /v1/sessions/{sessionId}` | any | SRS-FR-AUTH-003 | SEC-C-01, SEC-C-12 |
| API-enrollMfa | `POST /v1/mfa/enrollments` | any | SRS-FR-AUTH-002 | SEC-C-01 |
| API-listWorkspaces | `GET /v1/workspaces` | any | SRS-FR-WS-001 | SEC-C-03 |
| API-createWorkspace | `POST /v1/workspaces` | any | SRS-FR-WS-001 | SEC-C-03 |
| API-renameWorkspace | `PATCH /v1/workspaces/{workspaceId}` | owner | SRS-FR-WS-001 | SEC-C-02 |
| API-listMembers | `GET /v1/workspaces/{workspaceId}/members` | viewer | SRS-FR-WS-002 | SEC-C-02 |
| API-inviteMember | `POST /v1/workspaces/{workspaceId}/members` | admin | SRS-FR-WS-002 | SEC-C-02, SEC-C-12 |
| API-changeMemberRole | `PATCH /v1/workspaces/{workspaceId}/members/{memberId}` | admin | SRS-FR-WS-002, SRS-FR-AUTH-002 | SEC-C-02, SEC-C-12 |
| API-listProjects | `GET /v1/workspaces/{workspaceId}/projects` | viewer | SRS-FR-WS-003 | SEC-C-02, SEC-C-03 |
| API-createProject | `POST /v1/workspaces/{workspaceId}/projects` | developer | SRS-FR-WS-003 | SEC-C-02 |
| API-getProject | `GET /v1/workspaces/{workspaceId}/projects/{projectId}` | viewer | SRS-FR-WS-003 | SEC-C-02 |
| API-updateProject | `PATCH /v1/workspaces/{workspaceId}/projects/{projectId}` | developer | SRS-FR-WS-003, SRS-NFR-INT-01 | SEC-C-02, SEC-C-06 |
| API-archiveProject | `DELETE /v1/workspaces/{workspaceId}/projects/{projectId}` | developer | SRS-FR-WS-005 | SEC-C-12 |
| API-restoreProject | `POST /v1/workspaces/{workspaceId}/projects/{projectId}/restore` | developer | SRS-FR-WS-005 | SEC-C-12 |
| API-advanceProject | `POST /v1/workspaces/{workspaceId}/projects/{projectId}/actions/advance` | developer | SRS-FR-WS-004, SRS-NFR-INT-01 | SEC-C-02 |
| API-listTasks | `GET /v1/workspaces/{workspaceId}/tasks` | viewer | SRS-FR-TASK-002 | SEC-C-06 |
| API-createTask | `POST /v1/workspaces/{workspaceId}/tasks` | developer | SRS-FR-TASK-001 | SEC-C-02 |
| API-updateTask | `PATCH /v1/workspaces/{workspaceId}/tasks/{taskId}` | developer | SRS-FR-TASK-001, SRS-FR-TASK-002 | SEC-C-06 |
| API-deleteTask | `DELETE /v1/workspaces/{workspaceId}/tasks/{taskId}` | developer | SRS-FR-TASK-001 | SEC-C-02 |
| API-listConversations | `GET /v1/workspaces/{workspaceId}/conversations` | developer | SRS-FR-CHAT-001 | SEC-C-02 |
| API-createConversation | `POST /v1/workspaces/{workspaceId}/conversations` | developer | SRS-FR-CHAT-001 | SEC-C-02 |
| API-renameConversation | `PATCH /v1/workspaces/{workspaceId}/conversations/{conversationId}` | developer | SRS-FR-CHAT-001 | SEC-C-02 |
| API-deleteConversation | `DELETE /v1/workspaces/{workspaceId}/conversations/{conversationId}` | developer | SRS-FR-CHAT-001 | SEC-C-12 |
| API-exportConversation | `GET /v1/workspaces/{workspaceId}/conversations/{conversationId}/export` | developer | SRS-FR-CHAT-001 | SEC-C-04 |
| API-sendMessage | `POST /v1/workspaces/{workspaceId}/conversations/{conversationId}/messages` | developer | SRS-FR-CHAT-002, SRS-FR-CHAT-003 | SEC-C-08, SEC-C-09 |
| API-cancelMessage | `POST /v1/workspaces/{workspaceId}/conversations/{conversationId}/messages/{messageId}/cancel` | developer | SRS-FR-CHAT-005 | SEC-C-08 |
| API-runCommand | `POST /v1/workspaces/{workspaceId}/commands` | developer | SRS-FR-CHAT-004 | SEC-C-02, SEC-C-06 |
| API-listDocuments | `GET /v1/workspaces/{workspaceId}/documents` | viewer | SRS-FR-DOC-001 | SEC-C-02 |
| API-createDocument | `POST /v1/workspaces/{workspaceId}/documents` | developer | SRS-FR-DOC-001 | SEC-C-02 |
| API-getDocument | `GET /v1/workspaces/{workspaceId}/documents/{documentId}` | viewer | SRS-FR-DOC-001 | SEC-C-02 |
| API-updateDocument | `PATCH /v1/workspaces/{workspaceId}/documents/{documentId}` | developer | SRS-FR-DOC-001, SRS-FR-DOC-004 | SEC-C-12 |
| API-generateDocument | `POST /v1/workspaces/{workspaceId}/documents/{documentId}/generate` | developer | SRS-FR-DOC-002 | SEC-C-09 |
| API-transitionDocument | `POST /v1/workspaces/{workspaceId}/documents/{documentId}/transitions` | developer | SRS-FR-DOC-003 | SEC-C-02, SEC-C-12 |
| API-listDocumentVersions | `GET /v1/workspaces/{workspaceId}/documents/{documentId}/versions` | viewer | SRS-FR-DOC-004 | SEC-C-12 |
| API-restoreDocumentVersion | `POST /v1/workspaces/{workspaceId}/documents/{documentId}/versions/{version}/restore` | developer | SRS-FR-DOC-004 | SEC-C-12 |
| API-listAgents | `GET /v1/workspaces/{workspaceId}/agents` | viewer | SRS-FR-AGENT-001 | SEC-C-02 |
| API-createAgent | `POST /v1/workspaces/{workspaceId}/agents` | developer | SRS-FR-AGENT-001 | SEC-C-06, SEC-C-10 |
| API-updateAgent | `PATCH /v1/workspaces/{workspaceId}/agents/{agentId}` | developer | SRS-FR-AGENT-001 | SEC-C-10 |
| API-testAgent | `POST /v1/workspaces/{workspaceId}/agents/{agentId}/test` | developer | SRS-FR-AGENT-002 | SEC-C-09 |
| API-requestAgentDeployment | `POST /v1/workspaces/{workspaceId}/agents/{agentId}/deploy` | developer | SRS-FR-AGENT-003 | SEC-C-09, SEC-C-12 |
| API-pauseAgent | `POST /v1/workspaces/{workspaceId}/agents/{agentId}/pause` | admin | SRS-FR-AGENT-006 | SEC-C-02 |
| API-resumeAgent | `POST /v1/workspaces/{workspaceId}/agents/{agentId}/resume` | admin | SRS-FR-AGENT-006 | SEC-C-02 |
| API-runAgent | `POST /v1/workspaces/{workspaceId}/agents/{agentId}/runs` | developer | SRS-FR-AGENT-004 | SEC-C-08, SEC-C-09, SEC-C-10 |
| API-listExecutions | `GET /v1/workspaces/{workspaceId}/executions` | viewer | SRS-FR-AGENT-005 | SEC-C-12 |
| API-listApprovals | `GET /v1/workspaces/{workspaceId}/approvals` | admin | SRS-FR-AGENT-003, SRS-FR-DOC-003 | SEC-C-02 |
| API-decideApproval | `POST /v1/workspaces/{workspaceId}/approvals/{approvalId}/decision` | admin | SRS-FR-AGENT-003, SRS-FR-AGENT-004, SRS-FR-AUTH-002 | SEC-C-09, SEC-C-12 |
| API-listAuditEvents | `GET /v1/workspaces/{workspaceId}/audit-events` | admin | SRS-FR-AUDIT-001 | SEC-C-12 |
| API-listNotifications | `GET /v1/workspaces/{workspaceId}/notifications` | viewer | SRS-FR-AUDIT-002 | SEC-C-12 |
| API-markNotificationRead | `POST /v1/workspaces/{workspaceId}/notifications/{notificationId}/read` | viewer | SRS-FR-AUDIT-002 | SEC-C-02 |
| API-createExport | `POST /v1/workspaces/{workspaceId}/exports` | admin | SRS-FR-IO-001, SRS-NFR-PRIV-01 | SEC-C-04, SEC-C-15 |
| API-createImport | `POST /v1/workspaces/{workspaceId}/imports` | admin | SRS-FR-IO-002 | SEC-C-06 |
| API-createBackup | `POST /v1/workspaces/{workspaceId}/backups` | admin | SRS-FR-IO-003 | SEC-C-13 |
| API-restoreBackup | `POST /v1/workspaces/{workspaceId}/backups/{backupId}/restore` | owner | SRS-FR-IO-003, SRS-FR-AUTH-002 | SEC-C-13 |

## 3. Not yet specified

Webhooks, file upload endpoints, WebSocket alternatives, admin/operator APIs, billing. Add with their requirements when they enter scope.
