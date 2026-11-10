# ChattyOh project overview

ChattyOh is a proposed agent-assisted workspace for makers and teams. It brings project context, chat, specification documents, agents, review, and audit history into one product, while keeping approvals and lifecycle gates under human control.

## Product direction

The product vision is to help a user move from an idea to a planned, documented, tested project without losing context across tools. The MVP direction is web-first, with desktop and mobile shells reusing the same interface.

The current deliverable is **a prototype plus draft plans**, not a production service. The existing app has no production backend, accounts, or real integrations; actions described in the plans are target behavior unless explicitly identified as implemented.

## Personas and core journey

- **Maker:** turns an idea into a project and working plan.
- **Team lead:** coordinates work, roles, tasks, and quality gates.
- **Admin/security reviewer:** reviews access, approvals, and audit history.
- **Agency lead:** manages multiple client workspaces with consistent processes.

The main journey is: create a workspace and project, plan through chat, generate and review documents, configure and test an agent, obtain approval for sensitive actions, then inspect the recorded result.

## Documentation

- [Architecture](architecture.md) — proposed system boundaries and data flow.
- [API design](api-design.md) — REST resources and streaming contract.
- [Data model](data-model.md) — tenant-scoped entities and persistence rules.
- [Product spec](product-spec.md) — goals, personas, scope, and user stories.
- [Lessons learned](lessons-learned.md) — prototype findings and follow-up actions.

The full source documentation set, including the OpenAPI contract, security controls, threat model, test plans, traceability matrix, and delivery guide, is preserved under `src/backend plan/chattyoh-docs/`.

## Visual artifacts

The diagrams in `assets/` describe the **planned** architecture. The prototype flow PDF and wireframe are design artifacts. Screenshots are marked as prototype or concept views so they are not mistaken for shipped functionality.
