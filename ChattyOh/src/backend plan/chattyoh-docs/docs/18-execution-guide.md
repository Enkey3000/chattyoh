# 18 — Execution Guide

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Tech Lead · **Status:** Draft
**Upstream:** all previous documents · **Assumption:** team of 4–5 engineers, one designer, QA and DevOps shared; two-week sprints. Dates are relative (weeks from project start) and must be recalibrated once the team and dates are known.

## 1. Epics

| ID | Epic | Requirements | Slice |
|---|---|---|---|
| E1 | Foundations: repo, CI, environments, identity, tenancy | SRS-FR-AUTH-001, SRS-FR-WS-001, SRS-NFR-MAINT-01, SRS-NFR-SEC-01 | MVP-0 |
| E2 | Core data and rules: projects, tasks, rules module, audit | SRS-FR-WS-003, SRS-FR-TASK-001, SRS-FR-AUDIT-001, SRS-NFR-DATA-01/02, SRS-NFR-CONC-01 | MVP-0 |
| E3 | Chat and gateway | SRS-FR-CHAT-001…005 | MVP-0/1 |
| E4 | UI shell, accessibility, labels | SRS-FR-UI-001…003, SRS-NFR-A11Y-01 | MVP-0/1 |
| E5 | Roles, gates, tasks complete | SRS-FR-AUTH-002/003, SRS-FR-WS-002/004/005, SRS-FR-TASK-002, SRS-NFR-INT-01 | MVP-1 |
| E6 | Documents | SRS-FR-DOC-001…003 | MVP-1 |
| E7 | Agents with approvals | SRS-FR-AGENT-001…005 | MVP-1 |
| E8 | Import/export, notifications, observability, performance | SRS-FR-IO-001/002, SRS-FR-AUDIT-002, SRS-NFR-OBS-01, SRS-NFR-PERF-01 | MVP-1 |
| E9 | Hardening and shells: history, pause/resume, backup, privacy, availability, Electron, Flutter | SRS-FR-DOC-004, SRS-FR-AGENT-006, SRS-FR-IO-003, SRS-NFR-PRIV-01, SRS-NFR-AVAIL-01, SRS-NFR-COMPAT-01 | MVP-2 |

## 2. Sprint plan

| Sprint | Weeks | Goal | Exit |
|---|---|---|---|
| S0 | 0–2 | PoC spikes; PRD draft; repo and CI skeleton | PoC-01, -03, -06 results |
| S1 | 3–4 | Foundations (E1) and data/rules core (E2) | Sign-in, tenant isolation suite green |
| S2 | 5–6 | Chat and gateway (E3), UI shell (E4) → **MVP-0 on staging** | MVP-0 exit criteria |
| S3 | 7–8 | Roles, gates, tasks (E5); documents (E6) | Gates and approvals verified |
| S4 | 9–10 | Agents (E7); import/export, notifications (E8) | Agent approval flow verified |
| S5 | 11–12 | Observability, performance, accessibility; UAT start → **MVP-1** | UAT scenarios 001–009 |
| S6 | 13–14 | Hardening and shells (E9); pen test; fixes | Pen-test retest passed |
| S7 | 15–16 | Release candidate, UAT-010, go/no-go → **1.0** | REL-01…REL-12 |

Documentation phases (see the Documentation Plan) run in parallel: Security Measures, OpenAPI and Threat Model finish by week 6; Test Plan, Test Cases, UAT and Pen Test Plan by week 8; Release and Incident Plans by week 9; RTM runs in CI from week 3.

## 3. Dependency order

Identity and tenancy → rules module and audit → chat and gateway → documents and agents (need gateway and approvals) → import/export → shells. The OpenAPI spec is updated before each feature; the shells start after the web UI is stable (week 9+), with PoC-05 earlier.

## 4. Quality gates

Every pull request: lint, type-check, tests, secret scan, SAST, dependency scan, RTM check. Every sprint: demo, RTM and gap-analysis refresh. Every slice: its exit criteria. Release: REL-01…REL-12.

## 5. Team agreements

Definition of ready and done (playbook section 11); pull requests under ~400 lines; two-reviewer rule for security-sensitive code; no merging with failing gates; bugs add regression tests; honest labels for incomplete features.

## 6. Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| RR-01 | Identity or LLM provider decision delayed | Medium | High | Decide by week 2; abstract behind interfaces | PO |
| RR-02 | Gateway or RLS PoC fails | Low | High | Fallback designs in ADRs; early PoC | TL |
| RR-03 | Agent features outgrow capacity | Medium | Medium | Approval-first agents; defer sandbox features | TL |
| RR-04 | Accessibility work underestimated | Medium | Medium | Build components accessible from the start; axe in CI | TL |
| RR-05 | Late security findings | Medium | High | Threat-model-driven tests; pen test before freeze | SEC |
| RR-06 | Store review problems for mobile | Medium | Medium | Early submission of a test build; native value | PO |
| RR-07 | Scope creep from non-goals | High | Medium | MVP scope filter; change control | PO |

## 7. Reporting

Weekly status: progress against sprint goal, RTM coverage, open defects by severity, risks, decisions needed. Monthly: metrics from PRD section 6 once available.

## 8. Decision log (template)

| Date | Decision | Options considered | Rationale | Owner | Linked IDs |
|---|---|---|---|---|---|

## 9. Immediate next steps (first two weeks)

1. Confirm the seven open decisions (PRD section 9).
2. Create the repository with the folder structure and rules files; add CI with the RTM check.
3. Start PoC-01, PoC-03 and PoC-06.
4. Review and approve PRD and SRS (change control from then on).
5. Draft the OpenAPI spec for MVP-0 operations and lint it.
6. Replace placeholders and overstated claims on the public website, or label features as preview.
