# 08 — Test Cases

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** QA Lead · **Status:** Draft
**Upstream:** `02-srs.md`, `07-threat-model.md`, `06-test-plan.md` · **Downstream:** `11-rtm.md`

Levels: **U** unit · **I** integration/API · **E2E** end-to-end · **Sec** security · **A11y** accessibility · **Perf** performance · **Proc** process/analysis. Priority: P1 must pass for release; P2 should; P3 may be deferred with approval. Every case is automated unless noted; "Manual" cases are listed in `09-uat-plan.md` or the pen-test plan.

| ID | Title | Req | Threat | Level | Pri | Expected |
|---|---|---|---|---|---|---|
| TC-AUTH-001 | Sign in through OIDC creates a server-side session | SRS-FR-AUTH-001 | THR-S-001 | E2E | P1 | User lands signed in; session exists server-side |
| TC-AUTH-002 | Repeated failed sign-ins are rate-limited and generic | SRS-FR-AUTH-001 | THR-S-001 | Sec | P1 | Lockout after threshold; no account enumeration |
| TC-AUTH-003 | MFA enrolment and step-up before sensitive action | SRS-FR-AUTH-002 | THR-S-001 | E2E | P2 | Role change requires recent auth or MFA |
| TC-AUTH-004 | Logout and revoke invalidate the session on the server | SRS-FR-AUTH-003 | THR-S-002 | I | P1 | Old token returns 401 immediately |
| TC-AUTH-005 | Tokens never appear in localStorage, URLs or logs | SRS-FR-AUTH-003,SRS-FR-UI-001 | THR-S-002 | Sec | P1 | Scan finds no token in storage, URL or log output |
| TC-WS-001 | Workspaces are isolated; switching shows only own data | SRS-FR-WS-001 | THR-S-003 | I | P1 | No records from other tenants appear |
| TC-WS-002 | Cross-tenant read and write attempts are denied (ID sweep) | SRS-FR-WS-001,SRS-FR-WS-003 | THR-I-001,THR-S-003 | Sec | P1 | 403/404 for every foreign ID; audited |
| TC-WS-003 | Invites and role changes are audited; Viewer cannot edit | SRS-FR-WS-002 | THR-R-001 | I | P1 | Audit events present; Viewer writes refused |
| TC-WS-004 | Role-escalation attempts are rejected | SRS-FR-WS-002 | THR-E-001 | Sec | P1 | Developer cannot grant Admin; request denied and audited |
| TC-WS-005 | Project CRUD by ID; renaming keeps links and gates | SRS-FR-WS-003,SRS-NFR-DATA-02 | THR-T-001 | I | P1 | Tests, tasks and findings still linked after rename |
| TC-WS-006 | Advance is refused while tests fail | SRS-FR-WS-004 | THR-T-001 | I | P1 | Action returns gate error; stage unchanged |
| TC-WS-007 | Advance is refused while a Critical finding is open | SRS-FR-WS-004 | THR-T-001 | I | P1 | Action returns gate error; stage unchanged |
| TC-WS-008 | Direct update of a gated status field is rejected | SRS-FR-WS-004,SRS-NFR-INT-01 | THR-T-001 | Sec | P1 | PATCH with status returns 400/403 |
| TC-WS-009 | Archive and restore a project | SRS-FR-WS-005 | | I | P2 | Data preserved; restore returns project; audited |
| TC-TASK-001 | Task CRUD linked by project ID | SRS-FR-TASK-001 | | I | P1 | Create, read, update, delete work; project link by ID |
| TC-TASK-002 | Task filters, search, status and priority | SRS-FR-TASK-002 | | I | P2 | Filtered results correct; invalid values rejected |
| TC-TASK-003 | Injection payloads in search and filters are inert | SRS-FR-TASK-002 | THR-T-002 | Sec | P1 | No SQL error or data leak; parameterized queries |
| TC-CHAT-001 | Conversation create, rename, delete, export | SRS-FR-CHAT-001 | | E2E | P1 | Operations succeed and persist |
| TC-CHAT-002 | Streamed reply shows model and source | SRS-FR-CHAT-002 | THR-S-004 | E2E | P1 | Chunks stream; model and real/fallback label visible |
| TC-CHAT-003 | Provider outage shows a clear fallback notice | SRS-FR-CHAT-002,SRS-NFR-AVAIL-01 | THR-D-005 | I | P2 | Notice within 3 s; app remains usable |
| TC-CHAT-004 | Reply attaches to the right message; second send blocked | SRS-FR-CHAT-003,SRS-NFR-CONC-01 | | E2E | P1 | Replies match their messages; send blocked with reason |
| TC-CHAT-005 | Slash commands use domain actions (gates apply) | SRS-FR-CHAT-004 | THR-T-001 | I | P2 | /advance on failing project refused like UI |
| TC-CHAT-006 | Stop cancels the upstream request | SRS-FR-CHAT-005 | THR-D-001 | I | P1 | Upstream aborted; no further tokens billed |
| TC-CHAT-007 | Prompt-injection corpus does not change system behavior | SRS-FR-CHAT-002 | THR-T-003 | Sec | P1 | System rules and permissions unchanged |
| TC-DOC-001 | Document CRUD for all types | SRS-FR-DOC-001 | | I | P1 | All types create, read, update, archive |
| TC-DOC-002 | Draft is labeled; other tenants' data never in prompt | SRS-FR-DOC-002 | THR-I-003 | Sec | P1 | Prompt capture contains only current tenant data |
| TC-DOC-003 | Approval only by permitted roles; audited | SRS-FR-DOC-003 | THR-R-001 | I | P1 | Developer approval refused; transitions audited |
| TC-DOC-004 | Version history and restore | SRS-FR-DOC-004 | | I | P2 | Previous version restored; new version recorded |
| TC-AGT-001 | Agent CRUD; tool allow-list and arguments validated | SRS-FR-AGENT-001 | THR-E-005 | I | P1 | Unknown tools and bad arguments rejected |
| TC-AGT-002 | URL tools block private and metadata addresses (SSRF) | SRS-FR-AGENT-001 | THR-E-005 | Sec | P1 | 169.254.x.x, 10.x, localhost blocked |
| TC-AGT-003 | Agent test records pass or fail | SRS-FR-AGENT-002 | | I | P1 | Status Testing only after a pass |
| TC-AGT-004 | Deploy refused if untested; approval required | SRS-FR-AGENT-003 | THR-E-002,THR-R-001 | I | P1 | Refusal without test; approval recorded |
| TC-AGT-005 | Step, time and cost limits stop runaway runs | SRS-FR-AGENT-004 | THR-D-003,THR-D-001 | I | P1 | Run stops at limit with clear status |
| TC-AGT-006 | Sensitive tool call needs approval with exact arguments | SRS-FR-AGENT-004 | THR-E-002 | Sec | P1 | Tool not executed until approved |
| TC-AGT-007 | Sandbox: no network, no host access, limits enforced | SRS-FR-AGENT-004 | THR-E-003 | Sec | P1 | Escape attempts fail; limits enforced |
| TC-AGT-008 | Execution history is complete | SRS-FR-AGENT-005 | | I | P2 | Version, input, output, tools, cost, approver recorded |
| TC-AGT-009 | Pause and resume a deployed agent | SRS-FR-AGENT-006 | | I | P3 | Paused agent refuses runs; resume restores |
| TC-AUD-001 | Audit events are append-only and admin-only | SRS-FR-AUDIT-001 | THR-R-002 | Sec | P1 | Non-admin denied; update/delete impossible |
| TC-AUD-002 | Notifications for approvals and failures; mark read | SRS-FR-AUDIT-002 | | I | P2 | Notifications created and cleared |
| TC-IO-001 | Export contains no secrets or tokens | SRS-FR-IO-001 | THR-I-002 | Sec | P1 | Scan of export finds no secret values |
| TC-IO-002 | Import validates schema, size and hostile JSON | SRS-FR-IO-002 | THR-T-004,THR-D-002 | Sec | P1 | Oversized or `__proto__` payload rejected; preview shown |
| TC-IO-003 | Backup and restore with snapshot and version | SRS-FR-IO-003 | THR-I-005 | I | P2 | Snapshot taken; restore succeeds; version checked |
| TC-UI-001 | Navigation: MyModes, groups, Expand All, Collapse All | SRS-FR-UI-001 | | E2E | P2 | All menus open and close; routes work |
| TC-UI-002 | Simulated or preview features are labeled | SRS-FR-UI-002 | | E2E | P1 | Label present on every flagged feature |
| TC-UI-003 | Theme choice persists | SRS-FR-UI-003 | | E2E | P3 | Theme restored after reload |
| TC-UI-004 | XSS payloads render inert everywhere | SRS-FR-UI-001,SRS-NFR-SEC-01 | THR-S-002 | Sec | P1 | No script executes in any page |
| TC-NFR-001 | API p95 ≤ 300 ms; 5,000-row list stays responsive | SRS-NFR-PERF-01 | THR-D-002 | Perf | P1 | Meets budget at target load |
| TC-NFR-002 | Availability probe and failover drill | SRS-NFR-AVAIL-01 | THR-D-004 | Perf | P2 | RTO and RPO met in drill |
| TC-NFR-003 | Write failures are shown; no silent loss | SRS-NFR-DATA-01 | | I | P1 | Failed save shows error; data not reported saved |
| TC-NFR-004 | Corrupted stored data opens safe mode, keeps copy | SRS-NFR-DATA-01 | | I | P1 | App usable; original copy retained |
| TC-NFR-005 | Background job writes to the originating tenant | SRS-NFR-CONC-01 | THR-S-003 | I | P1 | Result in original tenant after workspace switch |
| TC-NFR-006 | Gate rules module is the only writer of gated state | SRS-NFR-INT-01 | THR-T-001 | I | P1 | Static check and tests show single write path |
| TC-NFR-007 | axe, keyboard, contrast, target size, focus, reduced motion | SRS-NFR-A11Y-01 | | A11y | P1 | No Critical/Serious findings; manual walkthrough passes |
| TC-NFR-008 | Data export, erasure and retention honored | SRS-NFR-PRIV-01 | THR-I-003 | I | P2 | Erased data unrecoverable; retention applied |
| TC-NFR-009 | Logs and traces contain no secrets or personal content | SRS-NFR-OBS-01 | THR-I-002,THR-I-004 | Sec | P1 | Redaction tests pass; request IDs present |
| TC-NFR-010 | Browser and OS matrix including both shells | SRS-NFR-COMPAT-01 | THR-S-005,THR-E-004,THR-T-006 | E2E | P2 | Core journeys pass on all targets |
| TC-NFR-011 | Coverage ≥ 80% on domain logic; RTM check fails when uncovered | SRS-NFR-MAINT-01 | THR-T-005 | Proc | P1 | CI gate blocks uncovered requirements |
| TC-NFR-012 | Lockfile, vulnerability scan, SBOM, 14-day version rule | SRS-NFR-SEC-01 | THR-T-005 | Sec | P1 | Pipeline fails on violation |
| TC-NFR-013 | TLS configuration, HSTS, CSP and security headers | SRS-NFR-SEC-01 | THR-S-004 | Sec | P1 | Scanner grade ≥ A; headers present |
| TC-NFR-014 | LLM quotas, spend caps and flood limits | SRS-NFR-SEC-01 | THR-D-001,THR-D-004 | Sec | P1 | Requests beyond limit refused; alerts raised |
| TC-NFR-015 | Incident tabletop (INC-01 and INC-03) executed | SRS-NFR-SEC-01 | | Proc | P2 | Findings recorded and actioned |
