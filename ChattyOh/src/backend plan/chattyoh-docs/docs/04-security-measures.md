# 04 — Security Measures

**Project:** ChattyOh Inc · **Version:** 0.1 (draft) · **Owner:** Security Lead · **Status:** Draft
**Upstream:** `02-srs.md`, `03-architecture.md` · **Downstream:** `05-openapi.md`, `07-threat-model.md`, `rules/cursorsecurityrules.md`

## 1. Control catalog

| ID | Control | Enforcement point | Verification | Owner |
|---|---|---|---|---|
| SEC-C-01 | Authentication through OIDC with optional MFA; short-lived sessions; Secure, HttpOnly, SameSite cookies; server-side revocation | identity module, API gateway | Auth integration tests; session expiry tests | Security Lead |
| SEC-C-02 | Deny-by-default authorization on every request, object-level, using roles plus project attributes | NestJS guards, rules module | Role and object-level negative tests; route-permission lint | Tech Lead |
| SEC-C-03 | Tenant isolation in the data layer (tenant_id plus PostgreSQL row-level security) | Prisma middleware, RLS policies | Cross-tenant test suite (fails closed) | Tech Lead |
| SEC-C-04 | Secrets only in a secrets manager; never in clients, logs, exports, backups or prompts | Secrets service, logger redaction | Secret scanning; export and backup tests | Security Lead |
| SEC-C-05 | TLS 1.2+ everywhere; encryption at rest; key rotation | Edge, storage config | TLS scan; key-rotation drill | DevOps |
| SEC-C-06 | Schema validation of all inputs, size limits, reject unknown fields | zod / OpenAPI validation middleware | Fuzz and property tests; size-limit tests | Tech Lead |
| SEC-C-07 | Output encoding, strict CSP, security headers, no inline script without nonce | React, header middleware | XSS payload e2e tests; CSP report review | Tech Lead |
| SEC-C-08 | Rate limits, quotas and spending limits per user, tenant and agent | Edge limiter, LLM gateway | Load and abuse tests | DevOps |
| SEC-C-09 | AI safety: prompt-injection defenses, tool allow-lists, output validation, human approval for sensitive actions | LLM gateway, tool layer | Injection test corpus; approval-flow tests | Security Lead |
| SEC-C-10 | Agent sandboxing: time, step and cost limits; no ambient credentials; no network by default | Execution service | Sandbox escape and limit tests | Security Lead |
| SEC-C-11 | Supply chain: lockfiles, vulnerability scanning, SBOM, versions ≥ 14 days old, signed builds | CI pipeline | SCA scan; install-script review; version-age check | DevOps |
| SEC-C-12 | Immutable audit log of security-relevant events; logs free of secrets and personal content | Audit module, logger | Log-content tests; tamper checks | Security Lead |
| SEC-C-13 | Encrypted backups, tested restores, documented retention and deletion | Ops runbooks | Quarterly restore drill | DevOps |
| SEC-C-14 | Secure SDLC gates in CI: SAST, secret scan, dependency scan, container/IaC scan, license check | CI pipeline | Pipeline fails on violations | DevOps |
| SEC-C-15 | Privacy: data minimization, consent for AI processing, data export and erasure | Data modules, UI | Export/erasure tests; consent review | Product Owner |
| SEC-C-16 | Incident response runbooks tested at least twice a year | Runbooks (`12-incident-response-plan.md`) | Tabletop exercises | Security Lead |

## 2. Authentication and session model

- Authorization-code flow with PKCE against the managed OIDC provider; the API trusts only tokens it validates (signature, issuer, audience, expiry).
- Access tokens ≤ 15 minutes; refresh tokens rotate and are revocable; web sessions use HttpOnly cookies. Desktop and mobile shells store tokens in the OS keychain or keystore, never in WebView storage.
- Sensitive actions (role change, data export, agent deployment approval) require recent authentication (≤ 5 minutes) or MFA step-up.
- Failed sign-ins are rate-limited per account and per IP; responses are generic.

## 3. Authorization model

Roles and permissions are defined in `02-srs.md` section 2. Rules: the server derives user and tenant from the session, never from the request body; every query is tenant-scoped (RLS); object-level checks protect against ID guessing; gated transitions are validated in the rules module.

## 4. Data classification and handling

| Class | Examples | Handling |
|---|---|---|
| Secret | API keys, tokens, secret values | Secrets manager only; never logged or exported; masked in UI |
| Confidential | Documents, conversations, agent instructions, prompts | Encrypted at rest; tenant-isolated; not logged; sent to the LLM only via the gateway |
| Internal | Audit events, metrics | Access by Owners/Admins and operators; retained per policy |
| Public | Marketing site content | No restrictions |

## 5. AI-specific measures (SEC-C-09, SEC-C-10)

1. System instructions stay separate from untrusted content; untrusted content is delimited and marked as data.
2. Tools are allow-listed per agent with typed, validated arguments and read-only scope by default.
3. Sensitive actions require human approval that shows the exact action and arguments.
4. Per-run limits: steps, time, tool calls and cost; loop detection; kill switch.
5. Model output is validated (schema) before use and never executed or interpolated into SQL, shell or HTML.
6. Retrieval queries carry tenant and permission filters inside the query.
7. Prompts and outputs are not written to application logs.

## 6. Audit events (SEC-C-12)

Sign-in, sign-in failure, logout, session revoke, role change, member invite/removal, project gate refusal and transition, document approval, agent test/deploy/run/approval, export, import, backup/restore, secret access, permission denial, configuration change. Each event: actor, action, target ID, tenant, time, request ID, result.

## 7. Privacy (SEC-C-15)

Disclose AI processing at first use; data minimization in prompts; export and erasure endpoints; retention settings per workspace; sub-processor list published; privacy policy and terms published before launch.

## 8. Secure development lifecycle (SEC-C-11, SEC-C-14)

Required CI gates, in order: lint and type-check → unit and integration tests → secret scan → SAST → dependency scan → container and IaC scan → SBOM → end-to-end and accessibility tests → DAST on staging. Code owners must review changes to authentication, authorization, tenancy, cryptography, secrets, the gateway and agent execution.

## 9. Gaps against the prototype

| Audit ID | Finding | Control that closes it |
|---|---|---|
| S-01 | Secrets stored in plain text and included in exports | SEC-C-04 |
| S-02 | No authentication or authorization | SEC-C-01, SEC-C-02, SEC-C-03 |
| S-03 | No Content Security Policy | SEC-C-07 |
| S-04 | Weak validation of restore and import | SEC-C-06 |
| S-05 | Missing privacy disclosures | SEC-C-15 |
| S-06 | Desktop hardening gaps (DevTools, permissions) | SEC-C-14 and platform rules |
| S-07 | Mobile backup exposure | SEC-C-04, SEC-C-13 |

## 10. Exceptions

A control may be waived only with a written exception: risk description, compensating control, owner, expiry date (≤ 90 days) and Security Lead approval. Exceptions are listed in the RTM notes.
