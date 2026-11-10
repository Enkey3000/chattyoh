# Problem Statement

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Product Owner · **Status:** Draft — *hypotheses, not yet validated with users*
**Feeds:** `product-vision.md`, `target-users.md`, `01-prd.md` · **Evidence level:** reasoning plus a working prototype; no user research has been done yet.

## 1. Problem statement (one paragraph)

People who turn ideas into software or content products currently move between many disconnected tools: an AI chat assistant, a project tracker, documents, design tools, code editors, test and deployment services. Context is lost at every hand-off, AI output is hard to trust or audit, and quality checks and approvals live in people's heads rather than in the workflow. As a result, small teams and solo builders spend their time re-explaining context, re-checking AI output, and chasing missing approvals instead of making progress.

## 2. Who has the problem

| Group | How the problem shows up |
|---|---|
| Solo makers and founders | Re-pasting context between tools; no structured path from idea to plan to build; unsure what AI output to trust |
| Small product and development teams | Requirements, tasks, tests and releases tracked in different places; no consistent quality gates |
| Admins and security reviewers | No visibility into what AI agents did, who approved it, or what data was sent where |
| Agencies | Repeating the same process across client projects with uneven quality |

## 3. Symptoms (what we expect to observe)

1. Time lost re-entering the same context in each tool.
2. AI-generated work accepted without review, or rejected because it cannot be traced.
3. Work advancing past quality checks that were skipped or forgotten.
4. Agents or automations running without clear limits, approvals or logs.
5. Data lost or confusing because tools do not agree on identity (names vs. IDs) or state.

## 4. Root causes

| Root cause | Consequence |
|---|---|
| Tools are organized by function, not by the project's lifecycle | Hand-offs break; no shared context |
| AI is added as a feature, not as a controlled participant in the workflow | No approvals, limits or audit for AI actions |
| Quality gates are social conventions | Easily skipped; not enforceable or measurable |
| Prototypes and demos present simulated results as real | Users cannot tell what is trustworthy |

## 5. Impact if unsolved

Slower delivery, avoidable rework, lower trust in AI output, security and compliance exposure from unmanaged agents, and burnout from context switching. *(Impact sizes are to be measured; see the validation plan.)*

## 6. Existing alternatives and their gaps

| Category (examples of the type, not a competitive claim) | Strength | Gap for this problem |
|---|---|---|
| General AI chat assistants | Fast, flexible conversation | No project structure, gates, approvals or audit |
| AI app builders and no-code tools | Quick first version | Weak lifecycle (spec, test, review, release) and governance |
| IDE assistants | Strong in code | Not a shared workspace for non-coding roles; limited approvals |
| Project and document tools | Good organization | AI is shallow; no agent control; separate from building |

## 7. Scope of the problem we address

**In scope (MVP):** one workspace with a shared project context; chat; documents with approval; agents with limits and approvals; audit; safe data handling; accessible UI on web, desktop and phone.
**Out of scope (MVP):** real deployment infrastructure, marketplaces, billing, SSO, real-time co-editing (see PRD non-goals).

## 8. What success looks like

A user gets from idea to a first project in minutes (PRD-M-01), AI output is labeled and reviewable (PRD-G-03), sensitive actions always show a human approval (PRD-G-02), and nothing is lost silently.

## 9. Assumptions to validate

| ID | Assumption | How to test | Decide by |
|---|---|---|---|
| PS-01 | Target users switch tools often enough that context loss is a top-three pain | 8–10 interviews; diary study | Before PRD sign-off |
| PS-02 | Users value approvals and audit for AI actions (not just speed) | Interview questions; prototype walkthrough | Before MVP-1 |
| PS-03 | One shared project context across modes is clearer than separate tools | Usability tests on the prototype | Before MVP-0 exit |
| PS-04 | Users will tolerate preview labels on unfinished features in exchange for honesty | Beta feedback | During beta |
| PS-05 | Teams will adopt a new workspace instead of extending existing tools | Pilot with 3 teams | Before 1.0 |

## 10. Validation plan

Interviews with at least 10 people across the four groups; observe two real "idea to first working project" sessions; run the prototype with 5 users per persona; record pain-point frequency and severity; revise this document and the PRD with findings.
