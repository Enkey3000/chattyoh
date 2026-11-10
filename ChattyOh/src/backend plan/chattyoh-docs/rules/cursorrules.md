# cursorrules.md — ChattyOh Inc

**Version:** 1.0 (draft) · **Status:** derived from the baselines in *Project Documentation Plan v1.0* (sections 6–8). Update when the approved PRD, SRS and Architecture change.
**Companion:** `cursorsecurityrules.md` (security rules). If the two ever conflict, **the security rules win**.

Every rule below ends with the ID of the requirement or decision it enforces, for example `[SRS-NFR-DATA-02]`. Mention relevant IDs in commit messages and pull requests.

---

## 0. How to use these rules

- Read this file and `cursorsecurityrules.md` before generating or editing code.
- Precedence when sources disagree: **security rules → SRS → Architecture (ADRs) → PRD → these rules → your own judgment.**
- If a request would break a rule, **say so and propose a compliant alternative**. Do not silently comply, and do not silently ignore the rule.
- If something is unclear or not covered, **ask** before guessing. Prefer a short question over a large wrong change.
- Keep changes small and focused: one concern per change, with tests.

## 1. Product context (PRD)

ChattyOh is one agent-assisted workspace that takes an idea from conversation to a deployed, documented, tested product, with the human always in control. `[PRD-G-01]`

Nine modes (ChatMode, VibeMode, CompMode, SpecMode, DevMode, TestMode, RevMode, PushMode, GentMode) share one project context. Users can enter any mode independently.

**MVP scope (build these first):** accounts and workspaces `[PRD-F-01]`, projects and tasks `[PRD-F-02]`, ChatMode with a real LLM `[PRD-F-03]`, SpecMode document generation and approval `[PRD-F-04]`, agents with approvals `[PRD-F-05]`, audit log, notifications and import/export `[PRD-F-06]`, accessible light/dark UI `[PRD-F-07]`.

**Out of MVP:** real cloud deployments, marketplace publishing, SSO/SCIM, billing, real-time co-editing, a native UI rewrite. Do not build these unless asked.

**Honesty rule `[PRD-G-03]`:** any feature that is simulated, preview or planned must be labeled as such in the UI, in API docs and in code comments. Never generate random pass/fail outcomes or fake "success" states without a visible "Simulated" label.

## 2. Stack and repository layout

**Language and tooling:** TypeScript with `strict: true` everywhere `[SRS-NFR-MAINT-01]`. ESLint + Prettier. Node LTS. pnpm workspaces.

**Frontend:** React, Tailwind CSS, shadcn/ui, Lucide icons, Zustand for client state, TanStack Query for server state. **Backend:** NestJS, PostgreSQL with Prisma, Redis with BullMQ, S3-compatible storage. **Tests:** Vitest, Playwright, axe for accessibility. **CI:** GitHub Actions. `[ARCH reference stack]`

Do not introduce a new framework, database, queue or major library without an ADR. Prefer what is already in the repository.

```
/apps
  /web            # React SPA/PWA (single UI codebase)         [ARCH-ADR-007]
  /desktop        # Electron shell: loads the web build + bridge
  /mobile         # Flutter shell: WebView + bridge
  /api            # NestJS modular monolith                    [ARCH-ADR-001]
/packages
  /contracts      # OpenAPI spec + generated types/clients     [ARCH-ADR-002]
  /domain         # business rules, shared types, validators   [ARCH-ADR-004]
  /ui             # shared components
  /config         # eslint, tsconfig, tailwind presets
/docs             # numbered documents 01-prd … 18-execution-guide, /rtm
/rules            # cursorrules.md, cursorsecurityrules.md
```

## 3. Architecture rules

1. **Modular monolith first.** Add modules (identity, workspace/project, chat, docs, agents, tasks, audit) inside `/apps/api`. Do not create microservices. `[ARCH-ADR-001]`
2. **OpenAPI first.** Change `/packages/contracts/openapi.yaml` first, regenerate types, then implement. Never hand-write API types that duplicate generated ones. `[ARCH-ADR-002]`
3. **Business rules live on the server, in the domain layer only.** The UI requests actions ("advance project"); it never sets gated fields (status, approvals, deployed state) directly. `[ARCH-ADR-004, SRS-NFR-INT-01]`
4. **No logic in controllers or components.** Controllers validate and delegate; domain services decide; repositories talk to the database.
5. **Tenant context everywhere.** Every query, job and cache key includes `tenantId`. `[ARCH-ADR-005, SEC-C-03]`
6. **All LLM calls go through the LLM gateway module.** No provider SDK calls from controllers, components or clients. `[ARCH-ADR-006]`
7. **Platform differences live behind one bridge interface** (`web`, `electron`, `flutter`). Feature code must not check which platform it runs on; it calls the bridge (`saveFile`, `openFile`, `secureStorage`, `share`, `onMenu`, `back`). `[ARCH-ADR-007]`
8. **Background jobs are idempotent** and carry `tenantId` and the entity IDs that created them. A job must write its result to the tenant and entity it started for, even if the user has switched workspace. `[ARCH-ADR-008, SRS-NFR-CONC-01]`

## 4. Data and domain rules

1. **Relationships use immutable IDs, never display names.** Renaming an entity must not break links, gates or reports. `[ARCH-ADR-003, SRS-NFR-DATA-02]`
2. **Derived and gated fields are not user-editable.** Project stage, test status, review status, deployment status and agent status change only through domain actions that enforce preconditions (for example: cannot advance with failing tests or an open Critical finding; cannot deploy an untested agent). `[SRS-NFR-INT-01]`
3. **No silent data loss.** Every write returns success or a typed error; the UI must show failures. Never show "Saved" before the write is confirmed. `[SRS-NFR-DATA-01]`
4. **Validate stored and imported data on load.** Use schemas (zod). On invalid data: keep a copy, repair what is safe, tell the user, and never crash the app or overwrite the original. `[SRS-NFR-DATA-01]`
5. **Schema versioning and migrations.** Every database change is a Prisma migration; every client-side stored shape has a `schemaVersion` and a migration function.
6. **Client persistence:** IndexedDB (with versioned schema) for offline cache. **Never** store tokens, secrets or personal data in `localStorage`. `[ARCH-ADR-009, SEC-C-04]`
7. **Size limits:** cap text fields (default 200,000 characters), list sizes and import sizes; reject over-limit input with a clear message. `[SEC-C-06]`
8. **Lists must scale:** server-side pagination or virtualization for anything that can exceed 200 rows; debounce search (≥250 ms); batch writes (no per-record full-database serialization). `[SRS-NFR-PERF-01]`
9. **Soft delete where recovery matters** (documents, projects, agents); hard delete only for explicit erasure requests. Deletions are audited.

## 5. API rules

1. REST resources are plural nouns, JSON, `camelCase`. Every operation has a stable `operationId`. `[ARCH-ADR-002]`
2. Standard error body: `{ code, message, details?, requestId }`. Never leak stack traces or internal IDs of other tenants.
3. All list endpoints are paginated (`cursor`, `limit` ≤ 100) and filterable; mutating endpoints accept an `Idempotency-Key` header.
4. Streaming (SSE or WebSocket) endpoints support cancellation and carry a message ID so replies attach to the correct message. `[SRS-NFR-CONC-01]`
5. Version breaking changes (`/v1`, `/v2`); never change the meaning of an existing field.
6. Every operation declares its security requirement and required permission in the spec. `[SEC-C-02]`

## 6. Frontend rules

1. **Functional components + hooks.** Co-locate component, test and styles. Keep components under ~200 lines; extract hooks for logic.
2. **No global mutable state, no `window.*` APIs for features, no inline event handler strings, no `innerHTML` with dynamic data.** Use React rendering (it escapes by default). `[SEC-C-07]`
3. **Accessibility is a requirement, not polish `[SRS-NFR-A11Y-01]`:**
   - Meet WCAG 2.2 AA contrast (4.5:1 text, 3:1 large text and UI components). Do not place white text on the light cyan end of the brand gradient; use the dark brand blue or dark text.
   - Use real `<button>`, `<a>`, `<label>`; clickable `div`s are not allowed.
   - Dialogs: `role="dialog"`, accessible name, focus trap, restore focus on close, close on Escape.
   - Status and toast messages use a live region (`role="status"`).
   - Menus and disclosure widgets expose `aria-expanded`/`aria-haspopup` and support arrow keys.
   - Minimum target size 24×24 px (aim for 44×44 on touch). Respect `prefers-reduced-motion` in CSS **and** JavaScript timers; provide pause for auto-advancing content.
   - Do not convey status by color alone.
4. **Theme:** use design tokens (CSS variables) for the brand palette (deep navy, royal blue, cyan, steel gray). Light and dark themes must both pass contrast checks.
5. **Performance budgets:** initial JS ≤ 250 KB gzip for the main route; images optimized (logo ≤ 20 KB at 256 px, WebP/SVG preferred; never embed large base64 images). UI feedback ≤ 100 ms. `[SRS-NFR-PERF-01]`
6. **Labels for non-real features:** use the shared `<SimulatedBadge />` for any simulated or preview functionality. `[PRD-G-03]`
7. **Errors:** wrap each route and side panel in an error boundary with a recovery action (reload, safe mode, export data). One failing panel must not blank the page.
8. **Internationalization-ready:** no hard-coded user-facing strings in logic; use the i18n helper for text.

## 7. AI and chat rules (non-security)

1. Chat messages have stable IDs. A reply updates the message it belongs to, found by ID, never "the last item". While a reply is pending, either queue the next message or disable Send with a visible reason. `[SRS-NFR-CONC-01]`
2. Support streaming and a Stop button; cancel the upstream request on stop.
3. Settings must be real: if the UI offers temperature, max tokens or autonomy level, the gateway must apply them. Remove any setting that is not wired up. `[PRD-G-03]`
4. Show which model answered and whether the answer came from the real gateway or a fallback. Fallback text must say it is a fallback.
5. Agent runs record: agent ID and version, input, output, tool calls, cost, duration and approver. They appear in the audit log. `[FR-AGENT, SEC-C-12]`
6. Document generation produces **drafts**; approval is a separate, audited user action. `[FR-DOC]`

## 8. Desktop and mobile shells

1. Shells contain no business logic. They host the web build and implement the bridge only. `[ARCH-ADR-007]`
2. File save/open, share, secure key storage and back-button handling go through the bridge with a plain-browser fallback so the same UI runs everywhere.
3. Electron: context isolation on, sandbox on, no Node in the renderer, minimal preload API, deny new windows and external navigation. Flutter: the WebView may load only the app origin; external links open in the system browser. (See security rules for the full list.)
4. Keep keyboard shortcuts out of OS-reserved combinations (for example Cmd+H on macOS).

## 9. Testing and traceability

1. **Every requirement gets at least one test**; name tests with the ID: `it('TC-CHAT-021 [SRS-FR-CHAT-003] attaches reply to correct message', …)`.
2. **Test pyramid:** unit tests for domain rules (≥ 80% coverage on `/packages/domain`), integration tests for API + database, contract tests against the OpenAPI spec, Playwright end-to-end for key journeys, axe checks on every page, performance checks on large lists. `[SRS-NFR-MAINT-01]`
3. **Write negative and abuse cases:** cross-tenant access, over-size input, malformed stored data, double-submit, workspace switch during a running job, status edited directly.
4. **Regression rule:** every bug fix adds a failing test first.
5. **RTM:** keep `/docs/rtm/rtm.csv` current; CI fails if a requirement ID has no linked test. Do not delete or skip tests to make a build pass.
6. Tests must not depend on random outcomes; inject a seeded random source or fake clock.

## 10. Errors, logging and observability

1. Use typed errors in the domain layer; map them to HTTP errors in one place.
2. Structured JSON logs with `requestId`, `tenantId`, `userId`. **Never log secrets, tokens, prompts or document contents.** `[SRS-NFR-OBS-01, SEC-C-12]`
3. Add traces around gateway calls and background jobs; emit metrics for latency, error rate and queue depth.
4. User-facing errors are actionable and honest ("Storage is full: changes were not saved"), never silent.

## 11. Code style

- Names: `camelCase` variables/functions, `PascalCase` types/components, `kebab-case` files, `SCREAMING_SNAKE_CASE` constants.
- Prefer small pure functions; avoid classes except for NestJS providers.
- No `any` (use `unknown` + narrowing); no non-null assertions without a comment; no commented-out code; no dead code.
- Comments explain **why**, not what. Link requirement/ADR IDs where non-obvious.
- Do not copy large blocks between apps; extract to `/packages`.

## 12. Git and pull requests

- Branch: `feat|fix|chore/<ticket>-<slug>`. Conventional Commits (`feat(chat): …`).
- PR description must list: requirement IDs, ADR IDs (if any), security controls touched, tests added, screenshots for UI changes, and a rollback note for data or API changes.
- A PR touching authentication, authorization, tenant isolation, cryptography, secrets, the LLM gateway or agent execution **requires human security review** (see security rules).
- Keep PRs under ~400 changed lines where possible.

## 13. Definition of done

A change is done only when **all** are true:

- [ ] Linked to requirement ID(s); RTM updated.
- [ ] OpenAPI updated first and contract tests pass (if API changed).
- [ ] Unit/integration/e2e tests added and passing; no skipped tests.
- [ ] Accessibility checks pass (axe + keyboard walkthrough for new UI).
- [ ] No new `any`, lint or type errors; coverage not reduced.
- [ ] Security checklist in `cursorsecurityrules.md` completed.
- [ ] Failures are visible to the user; no silent catch blocks.
- [ ] Simulated/preview behavior is labeled.
- [ ] Docs and change log updated.

## 14. Anti-patterns to avoid (learned from the prototype audit)

| Do not | Do instead |
|---|---|
| Link records by name | Link by immutable ID `[SRS-NFR-DATA-02]` |
| Enforce rules only in the UI or edit forms | Enforce in the server domain layer `[SRS-NFR-INT-01]` |
| Swallow storage errors and show "Saved" | Return/raise errors and show them `[SRS-NFR-DATA-01]` |
| Keep the whole database under one storage key | Per-record writes; IndexedDB/server `[SRS-NFR-PERF-01]` |
| Replace "the last message" when an async reply arrives | Update by message ID `[SRS-NFR-CONC-01]` |
| Let timers write into whichever workspace is active | Carry `tenantId` + entity ID in the job `[ARCH-ADR-008]` |
| Offer settings that do nothing | Wire them up or remove them `[PRD-G-03]` |
| Randomly succeed/fail "test runs" or "deployments" | Real execution, or a clearly labeled simulation `[PRD-G-03]` |
| Copy the whole app into each platform | One codebase + bridges `[ARCH-ADR-007]` |
| Embed a 400 KB base64 logo in every page | Optimized asset (≤ 20 KB), cached `[SRS-NFR-PERF-01]` |
| Crash on malformed stored data | Validate, repair, keep a copy, tell the user `[SRS-NFR-DATA-01]` |

## 15. When to stop and ask

Stop and ask a human before: changing the data model or migrations on populated tables; adding or upgrading a major dependency; changing authentication, authorization, tenancy or encryption; altering an approved requirement or ADR; deleting data; adding any network call to a new host; shipping a feature that is simulated but not labeled.
