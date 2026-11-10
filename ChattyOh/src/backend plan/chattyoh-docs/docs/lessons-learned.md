# Lessons Learned

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Tech Lead + Product Owner · **Status:** Living document — add an entry after every sprint, release or incident
**Sources:** the front-end prototype build, its platform audit (IDs B-, S-, A-) and the documentation work. Each lesson links to the requirement, decision or gap it informs.

Status: **Applied** (done in the prototype), **Planned** (in the documents, not built), **Open** (needs a decision).

## 1. Engineering and data

| ID | What happened | Lesson | Action | Links | Status |
|---|---|---|---|---|---|
| L-01 | Records were linked by display name; renaming a project silently broke tests and release gates (audit B-03) | Relationships must use immutable IDs | Use IDs everywhere | ARCH-ADR-003, SRS-NFR-DATA-02, GAP-06 | Planned |
| L-02 | Rules lived in the UI; editing a status directly bypassed them (B-04) | Business rules belong on the server in one place | Rules module; gated fields read-only | ARCH-ADR-004, SRS-NFR-INT-01, GAP-06 | Planned |
| L-03 | A finished deployment wrote its result into whichever workspace was open (B-05) | Background work must carry its tenant and entity IDs | Tenant-bound idempotent jobs | ARCH-ADR-008, SRS-NFR-CONC-01 | Applied in prototype; planned for product |
| L-04 | Two quick chat messages mixed up AI replies (B-06) | Update by message ID, never "the last item"; limit pending replies | Reply IDs; one pending reply per conversation | SRS-FR-CHAT-003 | Applied in prototype; planned for product |
| L-05 | Full browser storage still showed "Saved" (B-01) | Never report success before the write is confirmed | Surface storage errors; size limits | SRS-NFR-DATA-01 | Applied in prototype; planned for product |
| L-06 | Damaged stored data crashed the app (B-02) | Validate data on load; keep a copy; offer safe mode | Schema validation, versioning, safe mode | SRS-NFR-DATA-01, ARCH-ADR-009 | Applied in prototype; planned for product |
| L-07 | Saving the whole database on every change made imports and large lists slow (B-07) | Write per record; paginate or virtualize lists; debounce search | Server storage; IndexedDB cache | SRS-NFR-PERF-01, GAP-15 | Planned |
| L-08 | The same UI was copied into four files (app, desktop, mobile, previews); every fix had to be rebuilt four times | One codebase with a small platform bridge | Shared UI; shells only add a bridge | ARCH-ADR-007, GAP-16 | Planned |
| L-09 | A 424 KB embedded logo made up most of every page's weight | Optimize assets; never embed large images | Compressed logo (~15–20 KB) | SRS-NFR-PERF-01 | Open |

## 2. Product and honesty

| ID | What happened | Lesson | Action | Links | Status |
|---|---|---|---|---|---|
| L-10 | Simulated results (random test outcomes, fake "connection OK") looked real | Anything simulated must be labeled; avoid random results | Preview/Simulated labels; no fake outcomes | PRD-G-03, SRS-FR-UI-002 | Planned |
| L-11 | Settings existed that nothing used (temperature, autonomy, limits) | Do not ship controls that do nothing | Wire up or remove | GAP-13 | Open |
| L-12 | The public website described integrations the product only simulates | Marketing may describe only released features | Claims review gate before release | REL-11, GAP-20, RSK-03 | Open |
| L-13 | A "PWA" without a real manifest or service worker was not installable or offline | Do not claim a capability until it is verified | Real manifest and service worker on own hosting | GAP-19 | Open |

## 3. Quality, accessibility and testing

| ID | What happened | Lesson | Action | Links | Status |
|---|---|---|---|---|---|
| L-14 | Browser tests found issues review missed (for example the phone header overflowing) | Test in real browsers early and often, including narrow screens | Playwright smoke suite per PR | 06-test-plan.md | Planned |
| L-15 | A test failed because the page restored a different view after reload, not because of a bug | Tests must reset state and not depend on the previous page | Isolated, seeded tests | TC strategy | Planned |
| L-16 | Contrast, dialog focus, live regions and target sizes were fixed only after the first audit | Build accessibility in from the first component | axe in CI; accessible components | SRS-NFR-A11Y-01, GAP-14 | Planned |
| L-17 | Native shells could not be built or run in the authoring environment | Mark anything unrun as unverified; put device builds in the plan early | PoC-05; CI builds | GAP-21, GAP-22 | Planned |
| L-18 | A keyboard shortcut collided with an operating-system shortcut | Check reserved shortcuts per platform | Shortcut review | GAP-21 | Open |

## 4. Security and platform constraints

| ID | What happened | Lesson | Action | Links | Status |
|---|---|---|---|---|---|
| L-19 | Secrets were stored in plain text and appeared in exports | Treat secrets as a separate class from day one | Secrets manager; masked; excluded from exports | SEC-C-04, GAP-08 | Planned |
| L-20 | A public contact form could not safely accept and hide submissions with the hosting's built-in storage | Public forms need a real backend or form service | Choose a form service or API endpoint | GAP-20 | Open |
| L-21 | The AI runtime available to the hosted prototype did not exist outside it | Define the AI path per platform up front (gateway, keys, fallbacks) | LLM gateway; per-platform keys handling | ARCH-ADR-006 | Planned |
| L-22 | A model identifier used in the desktop and mobile builds could not be verified | Never hard-code unverifiable identifiers; make them configuration | Config-driven model IDs | PoC-01 | Open |

## 5. Process and documentation

| ID | What happened | Lesson | Action | Links | Status |
|---|---|---|---|---|---|
| L-23 | Building first and auditing later produced a long list of fixable-but-avoidable defects | Shift security, accessibility and data-integrity thinking left | Threat model and requirements before features | 07-threat-model.md | Applied (docs) |
| L-24 | A shared ID scheme let a script catch a traceability gap immediately | Stable IDs plus a CI check beat manual tracking | Keep `tools/rtm.py` as a CI gate | 11-rtm.md | Applied (docs) |
| L-25 | A scripting slip (shell brace expansion) wrote a file to the wrong place and lost another | Verify every generated file exists and has the expected content | Post-write checks; run tools from the repo root | Playbook | Applied |
| L-26 | One document held requirements in two places would drift | Each fact lives in one place; other documents link by ID or are generated | `requirements.md` is generated from the SRS | 02-srs.md | Applied |

## 6. What went well (keep doing)

- Small, testable slices with an immediate browser check after each change.
- A single ID scheme across requirements, tests, threats and APIs.
- Honest status labels ("designed, not executed", "results pending").
- Writing negative and abuse test cases alongside normal ones.

## 7. Open lessons to validate

Whether the WebView mobile approach is accepted by app stores; whether users value approvals enough to accept the extra step; real LLM cost per active workspace; how much accessibility work the shared UI needs after the first assistive-technology test.

## 8. How to add an entry

Copy a row; give it the next L-number; state what happened (facts only), the lesson, the action, links to IDs, and status. Review during each sprint retrospective.
