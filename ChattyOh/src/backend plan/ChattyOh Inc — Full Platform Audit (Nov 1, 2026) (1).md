# ChattyOh Inc — Full Platform Audit

**Date:** November 1, 2026\
**Scope:** web app, public website, Electron desktop build, Flutter mobile build\
**Purpose:** a reference for later reading: what is incomplete, what is broken, what needs attention, and which best practices are missing.

## 1. How to read this document

**Severity**

- **High**: loses data, breaks core behavior, or is misleading to users. Fix before showing the product to real users.
- **Medium**: a real gap or defect that does not lose data. Fix before launch.
- **Low**: polish, hygiene or future-proofing.

**Evidence labels**

- **Tested**: I reproduced it in a headless Chromium browser during this audit.
- **Code review**: found by reading the code; not exercised at runtime.
- **Not run**: could not be checked here (see section 11).

## 2. Executive summary

The four builds are good **prototypes**. The UI shell, navigation, the generic record engine, dashboards, bottom navigation on mobile, the native bridges and the phone preview all work in the tests I could run. They are **not production software yet**, for five reasons:

1. **Data can be lost silently.** When browser storage fills up, the app says "Saved" but nothing is stored (tested). Corrupted stored data can stop the app from rendering (tested).
2. **The integrity rules are cosmetic.** Release gates (failing tests, Critical findings, agent testing) can be bypassed by renaming a project or by editing a status directly (tested). Projects and tests are linked by *name*, not by ID.
3. **There is no backend, no accounts and no real integrations.** Teams, roles, secrets, deployments, tests, domains and marketplaces are all local or simulated. The public website describes many of these as real.
4. **Two real concurrency bugs:** a finished deployment writes its result into whichever workspace is open at that moment, and quick successive chat messages can lose or misplace AI replies (both tested).
5. **Neither native build has ever been compiled or run.** The Electron and Flutter projects are unverified (no Electron or Flutter toolchain in the audit environment).

### Top 10 actions, in order

| # | Action | Effort |
| --- | --- | --- |
| 1 | Surface storage errors and move data to IndexedDB (fixes silent data loss, quota, and speed) | M |
| 2 | Validate and migrate stored data on load; add a "safe mode" so a bad record can never brick the app | S |
| 3 | Link records by ID instead of name; enforce gates in one place (not in the edit form) | M |
| 4 | Fix the workspace-leak and chat-race bugs | S |
| 5 | Align website claims with what the product really does (or label features "preview") | S |
| 6 | Replace placeholders (address, email, phone, social links, legal pages) and give the contact form a real destination | S |
| 7 | Fix accessibility basics: contrast, focus handling in dialogs, live regions, tap targets, reduced motion | M |
| 8 | Compress the logo (424 KB of the app's 512 KB) and remove dead code | S |
| 9 | Move to one source of truth plus a build step; stop maintaining four copies of the same HTML | M |
| 10 | Add automated tests and CI; compile and run the Electron and Flutter builds on real machines | M |

## 3. Scorecard

| System | What works (tested) | Main gaps | Ready for |
| --- | --- | --- | --- |
| **Web app** (claude.ai artifact) | Navigation, 17 record collections with create/edit/delete/search/import/export, command box, chat, dashboards, 4 workspaces-style data stores, dark mode | Data-loss and integrity bugs, simulated integrations, no auth, accessibility | Internal demo / usability testing |
| **Public website** (claude.ai artifact) | All sections render, theme toggle, mobile menu, forms validate and save locally, icons render | Placeholders, forms go nowhere, overstated claims, SEO and legal gaps, private "Launch App" link | Preview only; not publishable as-is |
| **Desktop (Electron)** | Renderer page and bridge tested in a browser with a simulated desktop API | Never launched; unsigned; outdated Electron version; no auto-update | Developer testing after first real run |
| **Mobile (Flutter)** | Mobile page and bridge tested in a browser with a simulated native channel; phone preview works | Dart code never compiled; store-review risk; backups unencrypted | Developer testing after first real build |

## 4. Confirmed bugs and defects (tested)

| ID | Sev | System | Finding | Evidence and fix |
| --- | --- | --- | --- | --- |
| **B-01** | High | Web app and all builds | **Silent data loss when storage is full.** Saving a 6 MB record shows "Saved", but the record is gone after reload. The store swallows write errors. | Tested. Catch the error and tell the user; move data to IndexedDB (far larger quota); add a size cap per field. |
| **B-02** | High | Web app and all builds | **Corrupted stored data crashes rendering.** If a collection is not an array (for example `convs: "oops"`), the page throws `filter is not a function` at load and on every navigation. The only recovery is clearing site data. | Tested. Validate data on load, wrap the side-panel render in the same try/catch as the main view, and offer "Reset / restore backup" when validation fails. |
| **B-03** | High | Web app | **Renaming a project breaks its links.** Tests and findings reference projects by name. After renaming "Pulse Mobile", a failing test no longer blocks the project from advancing. | Tested. Store `projectId` on tests, findings and deployments; display the name by lookup. |
| **B-04** | High | Web app | **Gates can be bypassed by editing.** The Edit form lets anyone set an agent to *Deployed* without testing it, or a test to *Passed*, or a finding to *Resolved*. | Tested for agent status. Make gated statuses read-only in forms, derive them from actions, and keep the rules in one function the UI calls. |
| **B-05** | High | Web app | **Workspace leak.** A deployment started in one workspace finishes 1.6 s later and writes its result log and notification into whichever workspace is active then. The original record stays stuck on *Building*. | Tested (log appeared in the Team workspace; none in Personal). Capture the workspace key when the job starts and write results to that store. |
| **B-06** | High | Web app, desktop, mobile (when AI is connected) | **Chat race.** Sending a second message before the first reply arrives produced `msg one, …, msg two, REPLY[one]`: one reply lost and the other placed under the wrong message. | Tested with a delayed AI bridge. Give each message an ID, update by ID, and disable Send (or queue) while a reply is pending. |
| **B-07** | Medium | Web app | **Slow at scale.** Every write re-serializes the entire database. Importing 400 records took about 1.2 s (cost grows with the square of the record count); with 3,000 rows a search keystroke took about 0.95 s and one row action about 1.7 s. | Tested. Batch writes, debounce search, paginate or virtualize tables, and use IndexedDB with per-record writes. |
| **B-08** | Medium | Web app | **PWA requirement not met.** The manifest is created from a `blob:` URL and there is no service worker, so the app is not reliably installable and has no offline mode. | Tested (no registration; manifest URL is a blob). Ship a real `manifest.webmanifest`, icons in several sizes, and a service worker when hosted on your own domain. |
| **B-09** | Medium | Web app | **Settings that do nothing.** Temperature, max output tokens, autonomy level, execution limit, default language and editor theme are saved but never read anywhere. | Tested by code search. Wire them up or remove them; settings that look functional but are not are misleading. |
| **B-10** | Medium | Web app | **Simulated outcomes look real.** Test runs pass 85% of the time at random, deployments succeed 92% at random, "connection OK" is fake, and agent runs fall back to canned text when no AI is connected. Only the Deployments page says "simulated". | Code review. Label every simulated action in the UI, and remove random failures from anything a user might trust. |
| **B-11** | Low | Web app | **Dead code.** The original static `gen`, `mode`, `home` and `chat` functions and an unused sidebar-group renderer are still in the file, overridden at runtime by the new engine. | Tested by code search. Delete them (part of moving to a build step). |
| **B-12** | Low | Website | **Reduced-motion not honored for scripted motion.** The CSS disables animations, but the typing effect and the auto-advancing mode pipeline run on JavaScript timers and keep moving. The pipeline also has no pause button. | Code review. Check `prefers-reduced-motion` in JavaScript and add Pause (WCAG 2.2.2). |

## 5. Not complete, simulated, or only partly built

### 5.1 Features in your reference spec that are not implemented

- **Chat tools:** voice input and conversation, image generation, web search, deep research, code interpreter, tool selection, conversation folders/tags/pins/branching, message edit/regenerate/stop, conversation sharing.
- **Design (CompMode):** infinite canvas, layers, artboards, screenshot-to-design. Designs are records with a contrast check and a code-snippet generator only.
- **Development (DevMode, VibeMode):** code editor, debugger, terminal beyond the command parser, Git operations, live preview, codebase indexing, generated applications. The "Terminal" runs the app's own commands, not a shell.
- **Testing and review:** no real test runners (Playwright, Jest, k6 and others), no SAST/DAST, dependency or secret scanning. Findings are entered by hand.
- **Deployment:** no real hosting, DNS, domains, SSL, or app-store/marketplace submission. Records change status on a timer.
- **Agents:** no orchestration graph, handoffs, schedules, triggers, memory, tool permissions or MCP. Agents are named instruction sets; "Run" is one model call (or canned text).
- **Knowledge bases:** "Index" only counts chunks. There is no embedding, retrieval or search over content.
- **Platform:** no sign-in, roles enforcement (RBAC/ABAC), SSO/MFA, billing or credits, real-time collaboration, push notifications, command palette (Ctrl+K only focuses search), resizable or draggable panels, multiple project tabs, persistent layouts.
- **Context panel:** read-only summary; no editing.
- **No undo**, version history, or soft delete (delete is permanent).

### 5.2 Things that exist but are shallow

- **Workspaces** (Personal, Team, Organization) are three separate **local** databases on one device. There is no sharing, sync, invitation delivery or permission model. The Members page is a list, not access control.
- **Section pages share data.** The 183 menu entries map to 17 collections. For example, "Security Dashboard" and "Compliance" both show the same review-findings list. Sixteen entries have no specific mapping and fall back to their mode's default list: ChatMode (New Chat, Chat History, Deep Research, Voice Mode), VibeMode (New Application, Version Control), DevMode (Development Dashboard, Frontend / Backend / Database / API Development, Git Management, Debugging), and the Import Application pages in TestMode, RevMode and PushMode. Users may reasonably expect real features behind these names.
- **Analytics** are computed from local records only; there is no usage tracking.
- **Import/export** is JSON only; the backup file has no version or schema stamp.

## 6. Security and privacy

| ID | Sev | Finding |
| --- | --- | --- |
| **S-01** | High | **Secrets are stored in plain text** in browser storage and are **included in exports and backups**. On mobile the automatic backup file (documents folder) can be captured by device backups. Do not store real credentials until there is encrypted storage (OS keychain on desktop/mobile; a server-side vault for web). |
| **S-02** | High | **No authentication or authorization.** Anyone with the device (or the shared link, if the artifact is shared) has full access. Roles in the Members page are not enforced. |
| **S-03** | Medium | **No Content Security Policy** on any build. The single-file design needs inline scripts, so a CSP requires nonces or hashes from a build step. |
| **S-04** | Medium | **Restore and import validate almost nothing** (restore checks only that `projects` is an array; import accepts any object keys). Add schema validation and size limits. |
| **S-05** | Medium | **Privacy disclosures are missing.** Chat text is sent to an AI provider (through the Claude runtime in the web app; directly from the main process or Dart in desktop and mobile). The website collects email addresses. A privacy policy and consent text are needed before real use. |
| **S-06** | Low | **Electron:** developer tools are available in the production menu; no permission-request handler (deny camera, microphone, location by default); no `will-attach-webview` guard. |
| **S-07** | Low | **Mobile:** Android auto-backup is on by default; set `android:allowBackup="false"` or exclude the data file. The app mirrors the whole database to a file every few seconds when it changes. |
| **S-08** | Info | **Cross-site scripting:** I injected a script payload into 12 places (project, task, file, ticket, member, agent, secret and help-article names; chat; display name; global search) and visited every affected page. Nothing executed. Output escaping is consistent. Keep it that way as features are added. |
| **S-09** | Info | **No external network requests** were made by the app on load (no third-party scripts, fonts or trackers). |

## 7. Accessibility (WCAG 2.2 AA)

Checked with scripted inspection and computed contrast. **Not checked with a screen reader.**

**What is good:** `lang` is set; all buttons and inputs have accessible names; images have alt text; the app has header, nav, aside and main landmarks; headings start at one H1 on most pages.

**What needs attention**

| ID | Sev | Finding |
| --- | --- | --- |
| **A-01** | Medium | **Contrast failures** (ratio, need 4.5:1 for text): white on the cyan end of the gradient **2.31:1** (header, primary buttons); status tags: warning **2.11:1**, success **2.81:1**, error **3.74:1**. Passing: muted text 4.7–5.1:1 (light) and 6.97:1 (dark), brand blue on light 5.55:1, tabs 8.45:1, website footer 12.85:1. Darken tag text colors and keep gradient text over the darker part of the gradient (or use dark text on cyan). |
| **A-02** | Medium | **Dialogs:** they have `role="dialog"` and receive focus, but have no accessible name, Tab can leave the dialog, and focus is not returned to the trigger on close. |
| **A-03** | Medium | **Notifications:** the toast is not in a live region, so screen readers are not told when something was saved or blocked. Add `role="status"`. |
| **A-04** | Medium | **Target size:** on the app home screen all 40 visible controls are under 44 px; on mobile 53 of 58 are under 44 px (WCAG 2.2's minimum is 24 px; platform guidance is 44 px). The small row-action buttons are the main offenders. |
| **A-05** | Medium | **Menus:** top-bar dropdown triggers and the hamburger have no `aria-expanded` / `aria-haspopup`, and dropdowns are not arrow-key navigable. The chat list entries are `div`s that act as buttons and cannot be reached by keyboard. |
| **A-06** | Low | The app has no footer landmark, no skip link, the chat view has no H1, tables lack captions and header scope, and status is sometimes conveyed by color alone. |
| **A-07** | Medium | **Website:** no `<main>` landmark; 9 of 40 controls under 44 px; animated content ignores reduced-motion (see B-12). |

## 8. Performance and size

| Metric | Result |
| --- | --- |
| App first render | about 160 ms (local file, headless Chromium) |
| App page weight | 512 KB, of which the embedded logo is **424 KB (83%)** |
| Website page weight | 449 KB (mostly the same logo) |
| Logo optimization (measured) | 192 px quantized PNG about 12 KB; 256 px about 17 KB; WebP 192 px about 10 KB. Using one of these would cut each page to roughly 100 KB. Keep the full-size original in your brand assets. |
| DOM size | about 680 nodes on Home; about 1,900 on a long table view |
| Large tables | no pagination or virtualization (see B-07) |

Other items: every desktop/mobile copy of the app repeats the same payload; the mobile bridge sends the full database across the native channel every 3 seconds when data changes (acceptable at small sizes, wasteful as data grows).

## 9. Per-system notes

### 9.1 Web app

- Published as a claude.ai artifact, which means the address is not on your domain, availability depends on that service, and the page is private unless shared. For a public launch, host it yourself (any static host works for the current design).
- The AI features (chat, "Generate", agent Run) use the Claude runtime available **inside claude.ai**. Outside it, they fall back to the local assistant and templates. I verified only the fallback path, not live Claude replies.
- The PWA install button and runtime manifest are present but see B-08.

### 9.2 Public website

- **Placeholders** still in the page: street address, email address, phone number (4 occurrences); all **7 social links** point to `#`; Privacy, Terms, Security and Status in the footer are plain text, not links.
- **Contact form and newsletter** store data on the visitor's device and offer a "send by email" fallback. Nothing reaches you. (A shared database was ruled out because visitors who can write would also be able to read other submissions.) Use a form service or your own endpoint.
- **"Launch App"** points to a private artifact; visitors will see an error unless the artifact is shared or you replace the link with the hosted app's address.
- **Claims vs reality:** the site and its stats mention AWS/Azure/GCP deployment, app-store publishing, Playwright/Cypress/k6 testing, 17+ languages and security scanning. The app **simulates** most of these. Either mark them "preview/roadmap" or build them before advertising. This is a legal and trust risk, not just a content issue.
- **SEO and sharing:** has title and description; missing Open Graph and Twitter tags, canonical link and a favicon in the file itself (the favicon was set in the publishing tool). No sitemap or robots file.
- **Social icons:** I rendered them and all seven are recognizable (X, LinkedIn, Facebook, Instagram, YouTube, GitHub, TikTok). They were written from memory, so compare them with each brand's current official assets and brand guidelines (for example Instagram's gradient glyph and YouTube's red) before launch. Discord, Threads and WhatsApp are not included.

### 9.3 Desktop (Electron) — not run

- **Verified:** syntax of `main.js` and `preload.js`; the renderer page and bridge in a browser with a simulated desktop API; save dialog, menu events and AI path through that simulation.
- **Unverified:** actual launch, native menus, dialogs, `safeStorage`, packaging with electron-builder.
- **Attention:** Electron 33 is likely out of support by now: choose a current major version before shipping. **Cmd+H** is bound to "Home" but is the macOS system shortcut for Hide; change it. Production builds should disable DevTools, deny permission requests, and add a CSP. No code signing, notarization (macOS) or auto-update is configured. On some Linux systems `safeStorage` is unavailable, so the key cannot be saved. The window position is restored without checking that the monitor still exists. The default model id `claude-sonnet-5-5` is unverified. AI replies are not streamed.

### 9.4 Mobile (Flutter) — not compiled

- **Verified:** the mobile page, bottom navigation, back-button logic, restore-on-wipe logic and bridge messages, against a simulated native channel; the phone preview wrapper.
- **Unverified:** the Dart code has never been analyzed or built; dependency versions were chosen from memory.
- **Attention:** it is a **WebView wrapper**, and Apple may reject thin web wrappers under its minimum-functionality guideline; add real native value (share, files, secure storage are a start) and plan for review. Accessibility inherits all web findings (section 7). Confirm that localStorage persists across launches on a real iPhone with the `https://app.chattyoh.local/` base URL (the backup mechanism is a safety net, not a substitute). `share_plus` changed its API in newer major versions; the pinned version is older. `PopScope` needs Flutter 3.24 or newer. No signing, store listings, privacy labels or data-safety forms yet.

## 10. Engineering best practices not yet in place

| Area | Today | Recommended |
| --- | --- | --- |
| Source structure | One 500 KB HTML file per platform; four near-identical copies | One source repository; build step (for example Vite) that produces web, desktop and mobile bundles with a platform bridge |
| Version control and CI | None | Git, pull requests, CI running lint, unit tests and the browser tests below |
| Automated tests | None delivered (I ran ad-hoc browser scripts) | Keep and extend these as a regression suite: \~70 checks already exist |
| Data layer | Whole DB in one storage key; names as keys | IndexedDB, IDs, schema version and migrations, transactions |
| Errors | Uncaught errors reach the console only | Global error boundary, user-facing messages, optional error reporting |
| Typing and linting | Plain JavaScript in globals | TypeScript, ESLint, modules instead of globals |
| Security headers | None | CSP, no inline handlers, dependency audit once packages are used |
| Documentation | Chat history only | README, architecture note, data-model note, release checklist |
| Release process | Manual | Semantic versions, change log, signed builds, staged rollout |
| Observability | None | Error and performance monitoring (opt-in), structured logs |

## 11. What was tested and what was not

**Tested (automated, headless Chromium, local files)**

- Web app: 24 functional checks (create/edit/delete, search, persistence, gates, deploy flow, agent run, chat, every one of the 183 sections renders, settings and theme, top-bar actions, workspace separation, phone-width layout).
- This audit: XSS probes at 12 locations; data-integrity and gate-bypass cases; workspace leak; storage quota; malformed data; performance with 400 imports and 3,000 rows; accessibility and tap-target scans; contrast calculations; section-to-page mapping for all 183 entries; chat race with a delayed bridge.
- Website: forms, theme, pipeline, mobile menu, overflow, anchors, placeholder and meta checks, icon rendering.
- Desktop renderer: 10 checks with simulated and real-style bridge. Mobile page: 21 checks with simulated native channel and the phone preview.

**Not tested**

- Real Claude replies (the AI runtime exists only inside claude.ai).
- Electron and Flutter builds (no toolchains here); installers; app-store builds.
- Browsers other than Chromium (Safari and Firefox behaviors, including Safari's storage eviction rules).
- Screen readers (NVDA, JAWS, VoiceOver, TalkBack), real phones and tablets, slow networks.
- Load beyond 3,000 records; multi-tab use of the same workspace (two tabs can overwrite each other's data).
- Legal review of claims, privacy policy and terms.

## 12. Suggested roadmap

**Now (about 1 to 2 weeks)**

1. B-01, B-02, B-05, B-06: storage errors, safe mode, workspace-safe jobs, chat message IDs.
2. A-01 to A-03: contrast, dialog focus and names, live region for toasts.
3. Website: real address, email and phone; social URLs; legal pages; honest feature wording; a real form destination; Open Graph tags.
4. Compress the logo; delete dead code.
5. Run Electron and Flutter on real machines and fix whatever the first build reveals.

**Next (about 1 to 2 months)**

1. Move to a repository with a build step and tests; deploy the web app and website on your own domain with a real manifest and service worker.
2. Re-model data with IDs and migrations; IndexedDB; pagination.
3. Enforce gates in one rules module; remove placeholder settings or implement them.
4. Decide the AI path per platform (streaming, key handling, model selection) and document it.

**Later**

1. Backend: accounts, roles, shared workspaces, encrypted secrets, audit trail on the server.
2. Real integrations one at a time (Git hosting first, then CI/test runners, then cloud deploy), each replacing a simulated feature.
3. A native Flutter UI if the WebView approach does not meet store, performance or accessibility needs.

## 13. Appendix: contrast measurements

| Pair | Ratio | Result |
| --- | --- | --- |
| Muted text on light page (#587092 on #F1F7FE) | 4.70 | Pass |
| Muted text on white card | 5.06 | Pass |
| Muted text, dark mode (#8CA6C8 on #0B1A31) | 6.97 | Pass |
| White on brand blue (#0A5BD9) | 5.98 | Pass |
| White on cyan (#12B5FF) | 2.31 | **Fail** |
| Tab text on navy | 8.45 | Pass |
| Success tag text on its tint | 2.81 | **Fail** |
| Warning tag text on its tint | 2.11 | **Fail** |
| Error tag text on its tint | 3.74 | **Fail** |
| Brand blue text on light page | 5.55 | Pass |
| Dark-mode brand text (#2F8DFF on #0B1A31) | 5.28 | Pass |
| Website footer text | 12.85 | Pass |
