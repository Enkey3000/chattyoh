# 13 — Penetration Testing Plan

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Security Lead · **Status:** Draft
**Upstream:** `07-threat-model.md`, `03-architecture.md` · **Downstream:** `10-release-deployment-plan.md` (gate REL-04)

## 1. Objectives

Independently validate that the controls in `04-security-measures.md` hold under attack, find issues missed by automated tools, and confirm fixes before release.

## 2. Scope

| ID | In-scope target | Focus threats |
|---|---|---|
| PT-01 | Web application (staging) | THR-S-002, THR-I-001, THR-T-002 |
| PT-02 | REST API and SSE endpoints | THR-S-003, THR-T-001, THR-E-001, THR-I-001 |
| PT-03 | Authentication and session handling | THR-S-001, THR-S-002 |
| PT-04 | LLM gateway, chat and document generation | THR-T-003, THR-I-003, THR-D-001 |
| PT-05 | Agents, tools and sandbox | THR-E-002, THR-E-003, THR-E-005, THR-D-003 |
| PT-06 | Import/export and file handling | THR-T-004, THR-I-002, THR-D-002 |
| PT-07 | Electron desktop app | THR-E-004, THR-S-005, THR-T-006 |
| PT-08 | Flutter mobile app and WebView bridge | THR-S-005, THR-I-005 |
| PT-09 | Infrastructure and configuration (cloud, containers, CI/CD) | THR-T-005, THR-S-004 |

**Out of scope:** production systems (unless agreed), social engineering of staff, physical attacks, denial-of-service beyond agreed rate tests, third-party provider infrastructure.

## 3. Methodology

OWASP ASVS (target Level 2), OWASP Web Security Testing Guide, OWASP API Security Top 10, OWASP Top 10 for LLM applications, OWASP Mobile Application Security Testing Guide, and electron security guidance. Grey-box: testers receive documentation, the OpenAPI spec, the threat model and test accounts.

## 4. Test accounts and environment

Staging, production-like, isolated from real data. Accounts: two tenants, each with an Owner, Admin, Developer and Viewer; one account without MFA, one with MFA. Testers use dedicated source IPs and a test identifier header so activity can be told apart in logs.

## 5. Rules of engagement

Written authorization before start; testing windows agreed; no data exfiltration beyond proof; stop and notify immediately on a critical finding or accidental impact; no testing against production without separate approval; all findings reported only to the named contacts; confidentiality agreement in place.

## 6. Key test areas

Authentication and session fixation/replay; broken object-level and function-level authorization (every endpoint with foreign IDs and lower roles); tenant isolation and RLS bypass; gate bypass through direct status edits; injection (SQL, NoSQL, command, template); XSS and CSP bypass; CSRF and CORS; SSRF through tools; prompt-injection and indirect injection via documents and web content; agent approval bypass and tool-scope abuse; sandbox escape attempts; rate-limit and cost-abuse; import fuzzing (`__proto__`, huge arrays, deep nesting); secrets exposure in exports, logs, bundles and backups; Electron IPC abuse, navigation and permission handling; mobile bridge message abuse, backup exposure; dependency and build pipeline review.

## 7. Schedule and resourcing

One external team, 2 weeks of testing after the feature freeze (before the release gate), plus 1 week for fix verification. Internal security review and automated DAST run earlier and continuously.

## 8. Reporting and remediation

Report includes: executive summary, scope, method, findings with severity (CVSS plus business impact), reproduction steps, evidence, affected requirement/threat IDs, and recommended fixes.

| Severity | Fix target | Release impact |
|---|---|---|
| Critical | 48 hours | Blocks release |
| High | 7 days | Blocks release |
| Medium | 30 days | Needs approved plan |
| Low | Backlog | None |

Retest is mandatory for Critical and High findings. Results feed the Threat Model, RTM and regression tests.

## 9. Acceptance

The plan is complete when scope, dates, authorization, budget and contacts are approved, and the retest slot is reserved.
