# Target Users

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Product Owner · **Status:** Draft — *proto-personas from reasoning; replace with research findings*
**Upstream:** `problem-statement.md`, `product-vision.md` · **Feeds:** `user-stories.md`, `09-uat-plan.md`

## 1. Segments

| Segment | Description | MVP priority |
|---|---|---|
| Solo makers | Individuals turning ideas into projects and products | Primary |
| Small product/dev teams (2–15) | Teams needing shared plan, roles and gates | Primary |
| Admins and security reviewers | People accountable for control and audit | Primary (as a role inside teams) |
| Agencies | Run several client workspaces | Secondary |
| Enterprises (SSO, compliance) | Large organizations | Later (non-goal for MVP) |

## 2. Personas

### P1 — Maker (solo founder)
- **Goals:** turn an idea into a plan and a working project fast; keep everything in one place.
- **Pains:** juggling tools; re-explaining context to AI; unsure which AI output to trust.
- **Behaviors:** works in bursts; starts with a conversation; prefers templates and commands.
- **Comfort with technology:** medium to high; not always an engineer.
- **Success means:** first project within 10 minutes (PRD-M-01); drafts they can edit and approve.
- **Key modes and features:** Chat, Documents, Agents, Projects (PRD-F-02…05).

### P2 — Team lead
- **Goals:** organize work, assign roles, keep quality gates, report status.
- **Pains:** gates skipped; scattered tools; unclear ownership.
- **Behaviors:** reviews and approves; invites members; checks progress weekly.
- **Success means:** projects only advance when tests and reviews allow it; clear roles.
- **Key features:** Workspaces and roles, Projects, Tasks, Gates (PRD-F-01, F-02).

### P3 — Admin / security reviewer
- **Goals:** see who did what; control approvals and data; satisfy privacy needs.
- **Pains:** invisible AI activity; weak audit; uncertain data handling.
- **Behaviors:** reads audit logs; approves sensitive actions; exports data.
- **Success means:** complete, trustworthy audit; approvals show exact actions; secrets never exposed.
- **Key features:** Audit, Approvals, Export/Import, Roles (PRD-F-05, F-06).

### P4 — Agency lead
- **Goals:** repeat a reliable process across clients; keep client data separate.
- **Pains:** inconsistent quality; mixed client data; manual reporting.
- **Behaviors:** many workspaces; templates; handoffs between team members.
- **Success means:** separate workspaces, consistent document flow and gates.
- **Key features:** Workspaces, Documents, Gates (PRD-F-01, F-02, F-04).

## 3. Jobs to be done

| Job | Personas |
|---|---|
| "Help me turn this idea into a plan I can act on" | P1, P4 |
| "Make sure nothing ships that fails our checks" | P2 |
| "Let me delegate to an AI agent without losing control" | P1, P3 |
| "Show me exactly what the AI did and who approved it" | P3 |
| "Keep my work safe and portable" | All |

## 4. Accessibility and context needs

Keyboard-only users, screen-reader users, low-vision users (contrast, zoom, reduced motion), users on phones with small targets, users on slow connections (progressive loading). These are requirements, not extras (SRS-NFR-A11Y-01).

## 5. Priority matrix (persona × feature)

| Feature | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| PRD-F-01 Accounts and workspaces | ● | ●● | ● | ●● |
| PRD-F-02 Projects, tasks, gates | ● | ●● | ○ | ●● |
| PRD-F-03 ChatMode | ●● | ● | ○ | ● |
| PRD-F-04 Documents | ●● | ● | ○ | ●● |
| PRD-F-05 Agents with approvals | ●● | ● | ●● | ○ |
| PRD-F-06 Audit, export | ○ | ● | ●● | ● |
| PRD-F-07 Accessible UI | ● | ● | ● | ● |

●● core · ● important · ○ minor

## 6. Anti-personas (not served in MVP)

Teams needing real-time co-editing; enterprises requiring SSO and SCIM on day one; users who want fully autonomous agents with no approvals.

## 7. Research plan and open questions

Interview 10+ people across P1–P4; recruit at least two assistive-technology users; observe real first-project sessions; capture current tools and costs; update personas after the first round and re-prioritize PRD features. Open questions: willingness to pay, team sizes, privacy expectations around AI processing, preferred devices.
