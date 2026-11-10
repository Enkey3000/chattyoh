# 12 — Incident Response Plan

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owners:** Security Lead + DevOps · **Status:** Draft
**Upstream:** `07-threat-model.md`, `10-release-deployment-plan.md` · **Downstream:** `13-pen-testing-plan.md`, `16-playbook.md`
*Legal and regulatory notification duties depend on jurisdiction and contracts; confirm the final wording with Legal before use.*

## 1. Objectives and scope

Detect, contain, eradicate and recover from security and availability incidents with minimal harm, preserve evidence, communicate clearly, and learn from each event. Applies to the web app, API, LLM gateway, agents, desktop and mobile shells, infrastructure and the build pipeline.

## 2. Roles

| Role | Responsibility |
|---|---|
| Incident Commander (IC) | Leads response, makes decisions, keeps the timeline |
| Security Lead | Investigation, containment advice, evidence handling |
| Operations Lead | Technical mitigation, rollback, restoration |
| Communications Lead | Customer, internal and regulator messages (with Legal) |
| Scribe | Records timeline and decisions |
| Legal/Privacy (advisory) | Notification duties, contracts |

An on-call roster covers 24/7 for production once the product has users.

## 3. Severity levels

| Level | Definition | Response target | Examples |
|---|---|---|---|
| SEV-1 | Confirmed data exposure, active compromise, or total outage | Acknowledge ≤ 15 min; IC engaged immediately | Cross-tenant data exposure; leaked production credentials |
| SEV-2 | Serious degradation or likely compromise | Acknowledge ≤ 1 h | Agent bypassed approvals; LLM provider outage affecting most users |
| SEV-3 | Limited impact, contained | Same business day | Single-user account takeover; failed deployment rolled back |
| SEV-4 | Minor, no user impact | Next business day | Scanner finding, policy violation |

## 4. Process

1. **Detect and report** — alerts, user reports, scans, pen-test findings. Anyone can declare an incident.
2. **Triage** — assign severity, name the IC, open an incident channel and record.
3. **Contain** — stop the harm: revoke credentials, disable features with flags, block IPs, pause agents, isolate tenants, roll back.
4. **Eradicate** — remove the cause: patch, rotate keys, remove malicious dependencies, fix configuration.
5. **Recover** — restore from known-good state, verify integrity, monitor closely.
6. **Communicate** — internal updates at set intervals; customer notices for confirmed impact; regulator notices where required.
7. **Review** — blameless post-incident review within 5 business days; actions tracked to completion; update Threat Model, controls and tests.

**Evidence handling:** preserve logs, snapshots and timelines before changing systems where possible; restrict access; record who handled what and when.

## 4a. Runbooks

| ID | Scenario | Severity (typical) |
|---|---|---|
| INC-01 | Credential or secret leak | SEV-1/2 |
| INC-02 | Data exposure or breach | SEV-1 |
| INC-03 | Tenant isolation failure | SEV-1 |
| INC-04 | Prompt injection or agent misuse | SEV-2 |
| INC-05 | LLM provider outage or cost runaway | SEV-2/3 |
| INC-06 | Failed or malicious deployment | SEV-2/3 |
| INC-07 | Availability attack or overload | SEV-2 |
| INC-08 | Supply-chain compromise | SEV-1/2 |

### INC-01 Credential or secret leak
Detect: secret-scan alert, provider notice, unusual API use. Contain: revoke and rotate the credential immediately; invalidate sessions if tokens are affected. Investigate: find scope and usage in logs; check git history and artifacts. Recover: deploy new secrets; confirm no further use. Follow-up: add or tighten scanning; remove the leak source.

### INC-02 Data exposure or breach
Contain: disable the exposing endpoint or feature; revoke access paths. Investigate: affected tenants, data types, time window. Notify: Legal decides on regulator and customer notices (some regimes require notice within 72 hours of awareness). Recover: fix, verify with tests, monitor. Follow-up: new regression tests; review related controls.

### INC-03 Tenant isolation failure
Contain: block the affected route(s) or put the product in read-only mode; verify RLS policies. Investigate: queries returning foreign rows; audit access logs for cross-tenant reads. Notify: affected tenants and Legal. Recover: patch and run the full cross-tenant suite before re-enabling. Follow-up: add the case to the suite; review code owner rules.

### INC-04 Prompt injection or agent misuse
Contain: pause the agent or disable the tool; revoke run tokens. Investigate: run records, tool calls, approvals. Recover: tighten allow-lists, strengthen validation, add the payload to the injection corpus. Follow-up: user notification if data was affected.

### INC-05 LLM provider outage or cost runaway
Contain: enable fallback notices; lower quotas; pause costly agents; apply spend caps. Recover: switch provider or model tier if available; reconcile cost. Follow-up: review quotas and alerts.

### INC-06 Failed or malicious deployment
Contain: roll back to the previous version; freeze deploys. Investigate: change set, pipeline logs, approver. Recover: restore data if migrations ran; verify. Follow-up: strengthen gates; review pipeline permissions.

### INC-07 Availability attack or overload
Contain: tighten rate limits, enable WAF rules, scale out, shed load. Recover: normal limits after stability. Follow-up: capacity and abuse-protection review.

### INC-08 Supply-chain compromise
Contain: stop builds; pin or remove the package; rotate any credentials the build could read. Investigate: SBOM, lockfile diff, install scripts. Recover: rebuild from clean state; verify artifacts. Follow-up: tighten the 14-day rule and install-script review.

## 5. Communication templates (outline)

Internal: what happened, impact, current actions, next update time. Customer: plain-language description, what data/functions were affected, what we did, what users should do, contact. Regulator: as advised by Legal.

## 6. Testing and maintenance

Tabletop exercise at least twice a year (INC-01 and INC-03 before launch); restore drill quarterly; contact lists reviewed monthly; plan updated after every SEV-1/2 and each major architecture change.

## 7. Metrics

Time to detect, acknowledge, contain and recover; number of incidents by severity; action-item completion rate.
