# 10 — Release and Deployment Plan

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** DevOps/SRE · **Status:** Draft
**Upstream:** `03-architecture.md`, `06-test-plan.md`, `09-uat-plan.md` · **Downstream:** `12-incident-response-plan.md`, `16-playbook.md`

## 1. Release model

Slices **MVP-0**, **MVP-1** and **MVP-2** (see `15-mvp-pattern.md`) ship as semantic versions `0.x` (beta) and `1.0` (general availability). Web releases are continuous after gates pass; desktop and mobile releases follow release candidates.

## 2. Environments and promotion

Local → CI → Staging → Production. Promotion requires the gates in section 3. Production deploys need approval from the Release Manager and the Security Lead (for security-relevant changes).

## 3. Pre-release gates

| Gate | Evidence |
|---|---|
| REL-01 | All P1 test cases pass; no open Critical/High defects (RTM report) |
| REL-02 | RTM check passes: every requirement has a passing test |
| REL-03 | Security scans clean: SAST, secrets, dependencies, containers/IaC, SBOM published |
| REL-04 | DAST on staging complete; pen-test findings of High or above fixed and retested |
| REL-05 | Accessibility checks pass; manual walkthrough done |
| REL-06 | Performance budgets met (`SRS-NFR-PERF-01`) |
| REL-07 | UAT signed off |
| REL-08 | Database migrations reviewed, tested on a production-size copy, and reversible |
| REL-09 | Rollback rehearsed in staging |
| REL-10 | Monitoring, alerts and on-call roster ready; incident plan current |
| REL-11 | Privacy policy, terms and AI disclosure published; website claims reviewed against real features |
| REL-12 | Release notes and change log approved |

## 4. Deployment strategy

Web/API: blue-green with automated health checks, then staged traffic (5% → 25% → 100%) behind feature flags. Workers drain before switchover. Database migrations use expand → migrate → contract so old and new code can run together. Desktop: signed and notarized installers, staged auto-update. Mobile: staged rollout in each store.

## 5. Rollback

| Trigger | Action |
|---|---|
| Error rate > 2% for 5 minutes, p95 latency > 2× budget, or a failed health check | Automatic traffic shift back to the previous version |
| Security regression or data-integrity bug | Manual rollback and incident (INC-03 or INC-02) |
| Migration problem | Stop at expand phase; run reverse migration; restore from backup if needed |

Rollback target time: 15 minutes for web/API. Backups are verified before each release.

## 6. Monitoring and success checks

Watch for 24 hours: availability, error rate, latency, LLM errors and cost, queue depth, sign-in failures, authorization denials. Success: no alert above threshold; metrics within 10% of the previous release.

## 7. Communication

Release notes to users; status page for incidents; internal announcement to support; stakeholder summary after the monitoring window.

## 8. Go/No-go checklist

- [ ] REL-01 … REL-12 complete
- [ ] Product Owner, Tech Lead, Security Lead and DevOps approve
- [ ] On-call engineer named
- [ ] Rollback owner named
- [ ] Communication scheduled
