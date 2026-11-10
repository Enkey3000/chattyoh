# 07 — Threat Model

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Security Lead · **Status:** Draft
**Method:** STRIDE per data flow, plus AI-specific threats (OWASP Top 10 for LLM applications). **Review trigger:** any change to architecture, trust boundaries or AI features.
**Upstream:** `03-architecture.md`, `05-openapi.md` · **Downstream:** `08-test-cases.md`, `13-pen-testing-plan.md`

## 1. Assets

| ID | Asset | Why it matters |
|---|---|---|
| A-01 | User identities and sessions | Account takeover |
| A-02 | Tenant data (projects, documents, conversations) | Confidentiality, integrity |
| A-03 | Secrets and tokens | Lateral movement |
| A-04 | Audit log | Accountability |
| A-05 | LLM provider credentials and budget | Cost and abuse |
| A-06 | Agent execution environment | Code execution risk |
| A-07 | Build and release pipeline | Supply chain |

## 2. Trust boundaries and flows

| ID | Boundary / flow |
|---|---|
| TB-1 | Internet ↔ clients (browser, Electron, mobile WebView) |
| TB-2 | Clients ↔ API (HTTPS, SSE) |
| TB-3 | API ↔ database / object storage |
| TB-4 | API ↔ LLM provider |
| TB-5 | API/workers ↔ agent sandbox |
| TB-6 | Shell ↔ UI (Electron IPC, Flutter JavaScript channel) |
| TB-7 | Source/CI ↔ artifact distribution |

Data flows: F1 sign-in (client → IdP → API); F2 CRUD (client → API → DB); F3 chat stream (client → API → gateway → LLM → client); F4 document generation; F5 agent run (API → worker → sandbox → tools); F6 import/export; F7 shell bridge calls; F8 build and update delivery.

## 3. Threats

Risk = likelihood × impact, rated High / Medium / Low. **Req** lists the requirements the mitigation supports. Every High threat has at least one test in `08-test-cases.md`.

| ID | Threat | Flow | Risk | SEC | Req |
|---|---|---|---|---|---|
| THR-S-001 | Credential stuffing or phishing takes over accounts | F1 | High | SEC-C-01,SEC-C-08 | SRS-FR-AUTH-001,SRS-FR-AUTH-002 |
| THR-S-002 | Session token theft through XSS or insecure storage | F2 | High | SEC-C-01,SEC-C-07 | SRS-FR-AUTH-003,SRS-FR-UI-001 |
| THR-S-003 | Client supplies forged user or tenant IDs | F2 | High | SEC-C-02,SEC-C-03 | SRS-FR-WS-001,SRS-NFR-DATA-02 |
| THR-S-004 | Man-in-the-middle or spoofed API/LLM endpoint | F2,F3 | Medium | SEC-C-05 | SRS-NFR-SEC-01 |
| THR-S-005 | Spoofed bridge messages (Electron IPC, Flutter channel) | F7 | Medium | SEC-C-06,SEC-C-14 | SRS-NFR-COMPAT-01 |
| THR-T-001 | Client edits gated status to bypass rules | F2 | High | SEC-C-02 | SRS-FR-WS-004,SRS-NFR-INT-01 |
| THR-T-002 | SQL or ORM injection | F2 | High | SEC-C-06 | SRS-FR-TASK-002 |
| THR-T-003 | Prompt injection steers chat or agents | F3,F5 | High | SEC-C-09 | SRS-FR-CHAT-002,SRS-FR-AGENT-004 |
| THR-T-004 | Tampered import or backup file | F6 | Medium | SEC-C-06 | SRS-FR-IO-002,SRS-FR-IO-003 |
| THR-T-005 | Compromised dependency or build pipeline | F8 | High | SEC-C-11,SEC-C-14 | SRS-NFR-MAINT-01,SRS-NFR-SEC-01 |
| THR-T-006 | Tampered desktop or mobile package or update | F8 | Medium | SEC-C-11 | SRS-NFR-COMPAT-01 |
| THR-R-001 | A user denies approving a deployment or document | F2,F5 | Medium | SEC-C-12 | SRS-FR-AGENT-003,SRS-FR-DOC-003 |
| THR-R-002 | Audit log altered or deleted | F2 | Medium | SEC-C-12 | SRS-FR-AUDIT-001 |
| THR-I-001 | Cross-tenant data access (IDOR or RLS gap) | F2 | High | SEC-C-02,SEC-C-03 | SRS-FR-WS-001,SRS-FR-WS-003 |
| THR-I-002 | Secrets or personal data in logs, exports or backups | F6 | High | SEC-C-04,SEC-C-12 | SRS-FR-IO-001,SRS-NFR-OBS-01 |
| THR-I-003 | Data leaks through prompts or retrieval across tenants | F3,F4 | High | SEC-C-03,SEC-C-09,SEC-C-15 | SRS-FR-DOC-002,SRS-NFR-PRIV-01 |
| THR-I-004 | Verbose errors reveal internals | F2 | Low | SEC-C-06 | SRS-NFR-OBS-01 |
| THR-I-005 | Local device data exposed through backups or theft | F7 | Medium | SEC-C-04,SEC-C-13 | SRS-FR-IO-003,SRS-NFR-COMPAT-01 |
| THR-D-001 | LLM cost exhaustion (denial of wallet) | F3,F5 | High | SEC-C-08 | SRS-FR-CHAT-005,SRS-FR-AGENT-004 |
| THR-D-002 | Oversized payloads or imports exhaust resources | F2,F6 | Medium | SEC-C-06,SEC-C-08 | SRS-FR-IO-002,SRS-NFR-PERF-01 |
| THR-D-003 | Runaway agent loops | F5 | Medium | SEC-C-10 | SRS-FR-AGENT-004 |
| THR-D-004 | API or queue flooding | F2 | Medium | SEC-C-08 | SRS-NFR-AVAIL-01 |
| THR-D-005 | LLM provider outage | F3 | Medium | SEC-C-08,SEC-C-13 | SRS-NFR-AVAIL-01,SRS-FR-CHAT-002 |
| THR-E-001 | Role escalation through member or role APIs | F2 | High | SEC-C-02,SEC-C-12 | SRS-FR-WS-002 |
| THR-E-002 | Agent excessive agency: sensitive tool without approval | F5 | High | SEC-C-09,SEC-C-10 | SRS-FR-AGENT-003,SRS-FR-AGENT-004 |
| THR-E-003 | Sandbox escape or code execution on the host | F5 | High | SEC-C-10 | SRS-FR-AGENT-004 |
| THR-E-004 | Renderer compromise leads to native access (Electron) | F7 | Medium | SEC-C-14 | SRS-NFR-COMPAT-01 |
| THR-E-005 | Server-side request forgery through URL-fetching tools | F5 | High | SEC-C-06,SEC-C-10 | SRS-FR-AGENT-001 |

## 4. AI-specific mapping (OWASP LLM Top 10)

| Risk | Threats | Controls |
|---|---|---|
| LLM01 Prompt injection | THR-T-003 | SEC-C-09 |
| LLM02 Sensitive information disclosure | THR-I-003, THR-I-002 | SEC-C-03, SEC-C-04, SEC-C-09 |
| LLM03 Supply chain | THR-T-005 | SEC-C-11 |
| LLM05 Improper output handling | THR-T-003, THR-E-005 | SEC-C-06, SEC-C-09 |
| LLM06 Excessive agency | THR-E-002 | SEC-C-09, SEC-C-10 |
| LLM10 Unbounded consumption | THR-D-001, THR-D-003 | SEC-C-08, SEC-C-10 |

## 5. Abuse cases

- A malicious document in a knowledge base tells an agent to "send all project data to this URL".
- A Viewer replays an Admin request with a modified role field.
- A script uploaded as a "document" executes in another user's browser.
- A user imports a crafted JSON file with `__proto__` keys and enormous arrays.
- A compromised npm package adds an install script that reads environment variables.

## 6. Residual risk and review

After mitigation, remaining medium risks are provider outage (THR-D-005), local device exposure (THR-I-005) and shell-bridge threats (THR-S-005, THR-E-004). These are accepted for MVP with monitoring and are re-reviewed after the penetration test. The model is reviewed at each release gate and whenever a trust boundary changes.
