# ChattyOh Inc — Project Documentation Pack (v0.1 drafts)

Eight foundation documents, eighteen numbered delivery documents, the OpenAPI contract, the Cursor rule files and a traceability tool. Everything is **draft for review**: the numbers marked *proposed* and the decisions in `docs/01-prd.md` section 9 need your confirmation.

## Structure

```
docs/            numbered documents 01–18 (Markdown) and docs/rtm/rtm.csv
packages/contracts/openapi.yaml   API contract (OpenAPI 3.1)
rules/           cursorrules.md, cursorsecurityrules.md
tools/rtm.py     generates the RTM and fails CI when traceability breaks
tools/gen_requirements.py   regenerates docs/requirements.md from the SRS
```

## Foundation documents (start here)

| File | Purpose | Notes |
|---|---|---|
| `docs/problem-statement.md` | The problem, who has it, root causes, assumptions to validate | Hypotheses; no user research yet |
| `docs/product-vision.md` | Vision, mission, principles, horizons, metrics | |
| `docs/target-users.md` | Personas, jobs to be done, priorities, research plan | Proto-personas |
| `docs/user-stories.md` | 44 stories with acceptance criteria, linked to PRD and SRS | Checked by `tools/rtm.py` |
| `docs/requirements.md` | Readable register of all 45 requirements | **Generated** from the SRS by `tools/gen_requirements.py` |
| `docs/architecture.md` | One-page overview | Detail lives in `03-architecture.md` |
| `docs/roadmap.md` | Now / Next / Later, milestones, post-1.0 candidates | Dates relative and provisional |
| `docs/lessons-learned.md` | 26 lessons from the prototype build and audit | Living document |

## Document index

| # | Document | Owner | Status |
|---|---|---|---|
| 01 | `docs/01-prd.md` Product Requirements | Product Owner | Draft |
| 02 | `docs/02-srs.md` Software Requirements (45 requirements) | Tech Lead + PO | Draft |
| 03 | `docs/03-architecture.md` Architecture (11 ADRs) | Tech Lead | Draft |
| 04 | `docs/04-security-measures.md` Security Measures (16 controls) | Security Lead | Draft |
| 05 | `docs/05-openapi.md` + `packages/contracts/openapi.yaml` (55 operations) | Tech Lead | Draft; structure checked, not run through a full OpenAPI validator |
| 06 | `docs/06-test-plan.md` Test Plan | QA Lead | Draft |
| 07 | `docs/07-threat-model.md` Threat Model (28 threats) | Security Lead | Draft |
| 08 | `docs/08-test-cases.md` Test Cases (60 designed) | QA Lead | Designed, **not executed** |
| 09 | `docs/09-uat-plan.md` UAT Plan (10 scenarios) | PO + QA | Draft |
| 10 | `docs/10-release-deployment-plan.md` Release/Deployment | DevOps | Draft |
| 11 | `docs/11-rtm.md` RTM | QA Lead | **Generated** by `tools/rtm.py` |
| 12 | `docs/12-incident-response-plan.md` (8 runbooks) | Security + DevOps | Draft; legal wording to confirm |
| 13 | `docs/13-pen-testing-plan.md` | Security Lead | Draft |
| 14 | `docs/14-poc-report.md` | Tech Lead | Plan only; **results pending** |
| 15 | `docs/15-mvp-pattern.md` | PO + TL | Draft |
| 16 | `docs/16-playbook.md` | DevOps + TL | Draft |
| 17 | `docs/17-gap-analysis.md` (24 gaps) | Tech Lead | Draft; refresh each sprint |
| 18 | `docs/18-execution-guide.md` | Tech Lead | Draft; dates relative |

## Traceability

IDs: `PRD-F/G/M/N`, `SRS-FR-*`, `SRS-NFR-*`, `ARCH-ADR-*`, `SEC-C-*`, `API-<operationId>`, `THR-<S|T|R|I|D|E>-*`, `TC-*`, `UAT-*`, `REL-*`, `INC-*`, `PT-*`, `PoC-*`, `GAP-*`.

```bash
pip install pyyaml
python tools/rtm.py            # regenerate docs/11-rtm.md and docs/rtm/rtm.csv
python tools/gen_requirements.py   # refresh docs/requirements.md after SRS edits
python tools/rtm.py --check    # CI gate: exit 1 on broken links or uncovered requirements/High threats
```

Current result: 45 of 45 requirements have a designed test case and a user story; all 15 High threats have a control and a test case; 0 errors, 0 warnings. **This shows traceability, not that anything has been built or passed.**

## Before relying on this pack

1. Confirm the seven decisions (hosting, identity provider, LLM provider, compliance target, team and dates, mobile approach, tenancy).
2. Have Legal review the incident, privacy and notification wording.
3. Run the PoC spikes (document 14) and update the architecture and SRS with the results.
4. Calibrate dates in document 18 to the real team.
5. Add the pack to the repository as described in `rules/cursorrules.md`.
