# 16 — Engineering Playbook

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owners:** DevOps + Tech Lead · **Status:** Draft
**Upstream:** `10-release-deployment-plan.md`, `12-incident-response-plan.md`, `15-mvp-pattern.md` · **Companion:** `rules/cursorrules.md`, `rules/cursorsecurityrules.md`

## 1. Principles

Small changes, reviewed, tested, traceable. Every change links to a requirement ID. Security and accessibility are part of "done". The documents are code: versioned and reviewed.

## 2. Daily workflow

1. Pick a ticket linked to requirement ID(s).
2. Branch `feat|fix|chore/<ticket>-<slug>`.
3. Write or update the OpenAPI spec first (if the API changes), then tests, then code.
4. Run lint, type-check and tests locally.
5. Open a pull request (template below); CI runs all gates.
6. Review by a code owner; security review if triggered (see security rules).
7. Merge by squash with a Conventional Commit message; CI deploys to staging.

**Pull request template:** requirement IDs · ADR IDs · security controls touched · tests added · screenshots (UI) · migration and rollback notes · checklist from `cursorsecurityrules.md`.

## 3. How to add an entity or endpoint

1. Add or change schemas and operations in `packages/contracts/openapi.yaml` with `operationId`, `x-srs` and `x-sec`.
2. Run spec lint and regenerate types.
3. Add a Prisma migration (reversible; expand → migrate → contract for breaking changes); add RLS policy and tenant column.
4. Implement domain rules in the rules module; controller only validates and delegates.
5. Add tests: unit (rules), integration (API + database), negative cases (other tenant, lower role, bad input), contract.
6. Add or update test cases in `docs/08-test-cases.md` and run `tools/rtm.py`.
7. Update the UI through generated clients; add axe and keyboard checks.

## 4. Updating documents

Change a requirement → update `02-srs.md` and affected documents in the same pull request → run `tools/rtm.py` → add a change note (what, why, affected IDs). Approved documents change only through reviewed pull requests; Product Owner approves PRD/SRS changes, Tech Lead approves Architecture changes, Security Lead approves Security/Threat changes.

## 5. Release day

Follow `10-release-deployment-plan.md`: gates → staging smoke → blue-green deploy → staged traffic → 24-hour watch → release notes. Name the Release Manager, on-call engineer and rollback owner beforehand.

## 6. Hotfix

Branch from the production tag; minimal fix plus regression test; expedited review (code owner + security if relevant); deploy through the same pipeline; back-merge to main; incident note if severity ≥ SEV-3.

## 7. On-call

Primary and secondary roster; acknowledge alerts within the severity target; follow runbooks INC-01…INC-08; hand over with a written summary; blameless reviews.

## 8. Dependency updates

Weekly automated PRs; choose versions published ≥ 14 days ago; review changelogs and install scripts; run full CI; security-sensitive packages need a security review.

## 9. Running a security review

Trigger: any item in section 1 of `cursorsecurityrules.md`. Steps: read the diff against the threat model; check authorization and tenant scoping; check validation and encoding; check secrets and logging; check AI/agent controls; record findings and result in the PR.

## 10. Incident and bug handling

Report in the incident channel; follow `12-incident-response-plan.md`; every fixed bug adds a regression test linked to the requirement.

## 11. Definition of ready and done

**Ready:** linked requirement, acceptance criteria, design/API notes, test approach, owner. **Done:** see `rules/cursorrules.md` section 13.
