# 14 — Proof of Concept (PoC) Plan and Report

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Tech Lead · **Status:** Plan approved for execution; **results pending**
**Downstream:** `03-architecture.md` (ADR updates), `15-mvp-pattern.md`

> Honest status: none of the spikes below has been run yet. The "prior evidence" column refers only to the existing front-end prototype, which does not prove the server-side hypotheses. Fill the Result and Decision columns as each spike completes.

## 1. Purpose

De-risk the assumptions the architecture depends on before the SRS and ADRs are frozen. Time-box each spike to 2–5 working days.

## 2. Hypotheses and spikes

| ID | Hypothesis | Spike design | Success criteria | Prior evidence | Result | Decision |
|---|---|---|---|---|---|---|
| PoC-01 | A gateway can stream replies from the chosen LLM provider with cancellation and per-reply IDs | NestJS endpoint with SSE; cancel endpoint; reply IDs; two overlapping messages | First token ≤ 1.5 s; cancel stops upstream within 1 s; replies never cross messages | Prototype's chat bridge works against a stand-in | Pending | Pending |
| PoC-02 | Quotas and spend caps can be enforced per user, tenant and agent without hurting latency | Redis counters, token estimation, hard stop | Overhead ≤ 20 ms p95; limits enforced under concurrent load | None | Pending | Pending |
| PoC-03 | Tenant isolation holds with `tenant_id` plus PostgreSQL RLS under Prisma | Two tenants, policies, middleware, hostile query tests | 0 cross-tenant rows in a 1,000-request ID sweep; policy tests fail closed | None | Pending | Pending |
| PoC-04 | Human approval can pause and resume an agent run safely | Worker job with approval step; resume after decision; timeout | Exact arguments shown; no tool call before approval; survives worker restart | Prototype approval dialog only | Pending | Pending |
| PoC-05 | The same UI runs in Electron and a Flutter WebView through a small bridge | Build both shells on real devices; bridge for save, share, secure storage, back | All bridge calls work; back button; storage persists across launches | Prototype shells tested in a browser only | Pending | Pending |
| PoC-06 | IndexedDB cache with versioned schema avoids silent loss and handles quota errors | Client store with migrations, error surfacing, large data | Failures always shown; corrupted data opens safe mode | Prototype safe-mode logic tested in browser | Pending | Pending |
| PoC-07 | Agent sandbox can run code with no network and strict limits at acceptable cost | Container with gVisor or equivalent; resource limits | Escape tests fail; start time ≤ 2 s; cost within budget | None | Pending | Pending |

## 3. Reporting template (per spike)

Hypothesis · Setup · What was measured · Results (with numbers/evidence) · Surprises · Decision (adopt / adapt / reject) · Impact on ADRs and requirements · Follow-ups.

## 4. Gate

The PoC report is complete when every hypothesis has a recorded result and decision, and the architecture and SRS reflect the outcome.
