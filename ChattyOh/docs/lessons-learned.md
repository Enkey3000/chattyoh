# Lessons learned

This is the living lessons register from the existing ChattyOh prototype and its platform audit. The prototype is useful for navigation and usability demonstrations, but its local-only data and simulated integrations must not be mistaken for production functionality.

The complete original register (26 lessons, with links and Applied/Planned/Open status) is preserved in `src/backend plan/chattyoh-docs/docs/lessons-learned.md`. High-priority lessons are summarized here to keep the project entry point actionable.

## Data integrity and tenant boundaries

- **Never report a write as successful when storage rejected it.** Surface failures and preserve recoverable data; move from whole-database browser storage to a versioned persistence layer.
- **Validate stored data before rendering.** Corruption should lead to a safe recovery mode, not a blank or unusable application.
- **Link records by immutable IDs.** Display-name changes must not break tests, findings, deployments, or lifecycle rules.
- **Enforce business gates on the server.** Clients must request actions; they must not be able to set a project, test, or agent directly to a gated state.
- **Capture tenant context when work begins.** Async results must write to the original workspace, even if a user switches context while a job is running.
- **Bind streamed replies to message IDs.** Overlapping or delayed responses must not be lost or attached to the wrong conversation message.

## Product honesty and safety

- Mark every simulated, preview, or planned feature in the UI and documentation.
- Do not describe local workspace switching as collaboration, a list of members as enforced access control, or a status timer as a real deployment.
- Keep credentials out of browser storage and exports; use platform secure storage or a server-side secrets manager.
- Establish real integrations one at a time with validation and error reporting rather than random or canned success.

## Delivery and accessibility

- Maintain one shared UI source rather than several drifting copies.
- Add automated tests and CI before production claims; native builds must be compiled and exercised on target platforms.
- Verify contrast, keyboard focus, live status announcements, target sizes, and reduced motion in the core journeys.
- Treat docs, traceability, rollback, incident response, and security reviews as part of delivery rather than post-launch cleanup.

## Status

The follow-up architecture and security controls are **planned**. The full audit records reproducible prototype findings, including silent storage failures, corrupted-data crashes, editable gates, workspace-crossing async writes, and misplaced chat replies. No production remediation should be marked complete until it is implemented and verified.
