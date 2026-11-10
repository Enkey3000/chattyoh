# Product specification

**Status:** Draft for product and technical review. Proposed targets and open decisions are not approved.

## Vision and problem

ChattyOh aims to be one agent-assisted workspace that takes an idea from conversation to a deployed, documented, and tested product while keeping people in control. Builders currently move context between chat, planning, documentation, coding, testing, review, and delivery tools; approvals and audit history are easy to lose.

The product direction shares one project context across nine modes: ChatMode, VibeMode, CompMode, SpecMode, DevMode, TestMode, RevMode, PushMode, and GentMode. The current prototype demonstrates navigation and record collections, but does not implement all capabilities represented by those labels.

## Personas

| Persona | Need | Primary outcomes |
|---|---|---|
| Maker / solo founder | Move from idea to a coherent plan quickly | Create a workspace/project, plan in chat, and generate specs |
| Team lead | Coordinate people and quality gates | Assign work, review status, and prevent invalid transitions |
| Admin / security reviewer | Control access and sensitive actions | Review roles, approvals, policies, and audit events |
| Agency lead | Repeat a reliable process across client workspaces | Organize projects and reuse approved workflows |

These are draft personas based on product planning, not validated user research.

## Goals and measures

- Reduce time from signup to first project; proposed target: 60% of new users create one within 10 minutes.
- Keep humans in control with explicit approvals, limits, and auditable state changes.
- Avoid silent data loss and visibly distinguish real, simulated, and preview behavior.
- Share at least 95% of UI code across web, desktop, and mobile shells.
- Track document acceptance and agent-run success during beta before setting stable operational baselines.

## MVP scope

**Must have:** accounts/workspaces and roles; projects/tasks with server-enforced lifecycle gates; chat with real LLM streaming and cancellation; specification documents with review/approval; agents with testing, approval, bounded execution, and history; accessible consistent UI.

**Should have:** audit views, notifications, safe import/export, backup and restore.

**Out of scope for MVP:** real cloud deployments and marketplace publishing, SSO/SCIM, billing, real-time co-editing, native mobile UI, offline AI, real test runners, a full IDE, and a design canvas.

## User stories

- As a maker, I want to create a workspace and first project quickly so I can begin planning without setup friction.
- As a maker, I want to plan in chat and create tasks from commands so the conversation remains connected to project work.
- As a team lead, I want failing tests or open critical findings to block project advancement so quality gates cannot be bypassed.
- As a reviewer, I want to inspect and approve a generated document so draft content is not treated as approved.
- As an admin, I want sensitive agent actions to require approval and be recorded so execution remains accountable.
- As a user, I want a streamed reply to stop cleanly and remain linked to its message so delayed replies cannot be misplaced.
- As a user, I want failed saves and simulated actions to be clearly reported so I can trust the state shown by the product.

The original 44 acceptance-criteria stories are preserved in `src/backend plan/chattyoh-docs/docs/user-stories.md`.

## Main journeys

1. Sign up → create workspace → create first project.
2. Plan in chat → create and organize tasks.
3. Generate a PRD draft → edit → submit for review → approve.
4. Create an agent → test → request approval → run within limits → inspect history.
5. Attempt a blocked lifecycle change → see the reason → resolve the failing condition → retry.

## Acceptance boundary and open decisions

The MVP is acceptable when the core journeys use real server-side authorization and persistence, invalid gated transitions are rejected by the server, chat streams are bound to message IDs, approvals and audit events are retained, and core journeys meet WCAG 2.2 AA.

Cloud provider, identity provider, LLM provider and data terms, compliance targets, team/timeline, and enterprise tenancy model remain undecided. The source PRD is `src/backend plan/chattyoh-docs/docs/01-prd.md`.
