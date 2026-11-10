# 09 — User Acceptance Testing (UAT) Plan

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owners:** Product Owner + QA Lead · **Status:** Draft
**Upstream:** `01-prd.md`, `06-test-plan.md` · **Downstream:** `10-release-deployment-plan.md`

## 1. Objective

Confirm that real users can complete the key journeys on staging and that the product meets the PRD acceptance statements.

## 2. Participants

| Role | Count | Responsibility |
|---|---|---|
| Product Owner | 1 | Owns acceptance decisions |
| Representative users (maker, team lead, admin) | 6–8 | Execute scenarios, report issues |
| QA facilitator | 1 | Runs sessions, records results |
| Accessibility tester (assistive-technology user, if available) | 1–2 | Executes UAT-009 |

## 3. Environment and data

Staging, production-like, seeded with sample workspaces; real accounts for testers; no production data. LLM calls use the real provider with a capped budget.

## 4. Scenarios

| ID | Scenario | PRD | Req | Acceptance |
|---|---|---|---|---|
| UAT-001 | New user signs up, creates a workspace and a first project | PRD-F-01,PRD-F-02 | SRS-FR-AUTH-001,SRS-FR-WS-001,SRS-FR-WS-003 | Completed within 10 minutes without help by ≥ 80% of testers |
| UAT-002 | Team lead invites a developer and assigns tasks; a viewer cannot edit | PRD-F-01,PRD-F-02 | SRS-FR-WS-002,SRS-FR-TASK-001 | Roles behave as specified; audit shows changes |
| UAT-003 | Plan a project in chat and create tasks with slash commands | PRD-F-03 | SRS-FR-CHAT-002,SRS-FR-CHAT-004 | Streamed reply appears; tasks created; Stop works |
| UAT-004 | Generate a PRD draft, edit it, submit for review, approve | PRD-F-04 | SRS-FR-DOC-002,SRS-FR-DOC-003 | Draft is labeled; only permitted roles approve |
| UAT-005 | Create an agent, test it, approve deployment, run a task | PRD-F-05 | SRS-FR-AGENT-001,SRS-FR-AGENT-003,SRS-FR-AGENT-004 | Approval shown with exact action; run recorded |
| UAT-006 | Try to advance a project with failing tests, then fix and advance | PRD-F-02 | SRS-FR-WS-004 | Block is clear and actionable; advance works after fix |
| UAT-007 | Admin reviews the audit log and notifications | PRD-F-06 | SRS-FR-AUDIT-001,SRS-FR-AUDIT-002 | Events are complete and understandable |
| UAT-008 | Export a workspace, reset, import it back | PRD-F-06 | SRS-FR-IO-001,SRS-FR-IO-002,SRS-FR-IO-003 | No data lost; secrets absent from export |
| UAT-009 | Keyboard-only and screen-reader walkthrough of the core journey | PRD-F-07 | SRS-NFR-A11Y-01,SRS-FR-UI-001 | No blockers; all controls reachable and named |
| UAT-010 | Use the product on desktop shell, phone shell and browser | PRD-G-04 | SRS-NFR-COMPAT-01 | Same features and data; shell features (save, share, back) work |

## 5. Schedule

Preparation (1 week) → sessions (1 week) → fixes and re-test (1 week) → sign-off meeting.

## 6. Defects and decisions

Defects are logged with severity (see Test Plan). UAT passes when all scenarios pass, no Critical or High defects remain, and the Product Owner signs.

## 7. Sign-off

| Role | Name | Date | Decision (Accept / Accept with conditions / Reject) |
|---|---|---|---|
| Product Owner | | | |
| QA Lead | | | |
| Security Lead | | | |
