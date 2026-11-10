# 06 — Test Plan

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** QA Lead · **Status:** Draft
**Upstream:** `02-srs.md`, `03-architecture.md`, `04-security-measures.md` · **Downstream:** `08-test-cases.md`, `09-uat-plan.md`, `10-release-deployment-plan.md`

## 1. Objectives and scope

Prove that the MVP meets the SRS, that security controls work, and that the product is accessible, performant and safe to release. **In scope:** web app, API, LLM gateway, agent execution, Electron and Flutter shells (shell behavior and bridge). **Out of scope for MVP:** simulated or non-goal features (see PRD non-goals), load beyond the stated targets, third-party provider internals.

## 2. Test levels and tools

| Level | Purpose | Tools | Runs |
|---|---|---|---|
| Unit | Domain rules, validators, utilities | Vitest | Every commit |
| Integration / API | Endpoints, database, RLS, jobs | Vitest + Supertest, Testcontainers | Every commit |
| Contract | API matches OpenAPI | Schemathesis or Dredd, spec lint (Spectral) | Every commit |
| End-to-end | Key journeys in a browser | Playwright | Every PR (smoke), nightly (full) |
| Accessibility | WCAG 2.2 AA | axe-core in Playwright, manual keyboard and screen-reader checks | Every PR; manual per release |
| Performance | Latency, large lists | k6, Lighthouse CI | Nightly; before release |
| Security | SAST, SCA, secrets, DAST, abuse cases | Semgrep/CodeQL, Dependabot/OSV, gitleaks, OWASP ZAP | Every PR (static); staging (DAST) |
| Shell tests | Electron and Flutter bridge and packaging | Playwright for Electron, `flutter test` + device farm | Per release candidate |
| Exploratory / UAT | Real-world use | Manual | Before release |

## 3. Test data and environments

Seeded fixtures per tenant; no production data in test environments; synthetic LLM responses for deterministic tests plus a small live-model suite run nightly. Environments: CI (ephemeral), Staging (production-like). Secrets for tests come from the CI secret store and are never committed.

## 4. Entry and exit criteria

| Stage | Entry | Exit |
|---|---|---|
| Integration testing | Build green; contracts lint clean | All P1 integration cases pass |
| UAT | Integration exit met; staging deployed | UAT sign-off criteria met (`09-uat-plan.md`) |
| Release | UAT sign-off; pen-test retest done | No open Critical/High defects; all P1 cases pass; coverage ≥ 80% on domain logic; RTM check passes; accessibility checks have no Critical/Serious findings |

## 5. Defect management

| Severity | Definition | Fix SLA before release |
|---|---|---|
| Critical | Data loss, security breach, system unusable | Block release; fix immediately |
| High | Core function broken, no workaround; gate bypass | Block release |
| Medium | Function impaired with workaround | Fix or approved deferral |
| Low | Cosmetic, minor | Backlog |

Defects are linked to requirement and test IDs; every fixed defect adds a regression test.

## 6. Priorities (risk-based)

1. Tenant isolation, authorization and gate enforcement (THR-I-001, THR-E-001, THR-T-001).
2. Data integrity: write errors, safe mode, ID relations, job tenancy (SRS-NFR-DATA-01/02, SRS-NFR-CONC-01).
3. AI safety: injection, approvals, limits, sandbox (SEC-C-09/10).
4. Accessibility and performance budgets.
5. Everything else by priority P1 → P3.

## 7. Automation targets

≥ 90% of P1 cases automated; manual cases limited to UAT, screen-reader checks, device checks and pen-test items.

## 8. Reporting

Daily CI dashboard; weekly quality report (pass rate, open defects by severity, coverage, RTM coverage); release readiness report at the gate.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Non-deterministic LLM output makes tests flaky | Mock gateway for most tests; assert on structure and rules, not wording |
| Device coverage for mobile shell | Device farm; focus on bridge and back-button behavior |
| Late security findings | Threat-model-driven cases written early; pen test scheduled before freeze |
