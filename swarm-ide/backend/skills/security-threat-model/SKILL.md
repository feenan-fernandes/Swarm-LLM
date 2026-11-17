---
name: security-threat-model
description: Evaluates application trust boundaries, unsanitized inputs, secret leakage risks, authentication gates, and attack surfaces before code synthesis.
---

# `security-threat-model` — Security & Attack Surface Auditing

Based on the Trail of Bits and OWASP agent threat modeling standards, this skill guides agents in identifying vulnerabilities, mapping trust boundaries, and hardening software against exploits before code deployment.

## The STRIDE Attack Surface Framework

When reviewing code, architecture, or API routes, evaluate against the 6 core threat vectors:

1. **Spoofing**:
   - Are API endpoints or RPC methods authenticated?
   - Can an attacker forge headers, tokens, or user IDs (`req.user.id` vs unsanitized `req.body.userId`)?
2. **Tampering**:
   - Are file paths passed to disk writes validated against directory traversal (`../` or absolute paths)?
   - Are command arguments safely escaped (using `shlex.quote` or subprocess lists, never raw `shell=True` string formatting)?
3. **Repudiation**:
   - Are security-critical actions (payments, permission changes, deletions) logged with timestamps and actor identities in an append-only log?
4. **Information Disclosure**:
   - Are database connection strings, API keys, or private tokens committed to code or logged in error messages?
   - Do error handlers return generic messages to end users while keeping stack traces internal?
5. **Denial of Service**:
   - Are regular expressions protected against catastrophic backtracking (ReDoS)?
   - Are file upload sizes, JSON payload sizes, and rate limits strictly capped?
6. **Elevation of Privilege**:
   - Are role-based access checks (RBAC) enforced on the server, not solely in frontend UI logic?

## Pre-Commit Security Checklist
Before finalizing code:
- [ ] No hardcoded passwords, bearer tokens, or sensitive credentials in git.
- [ ] All database queries parameterized (zero raw SQL string concatenation).
- [ ] All subprocess execution uses list arguments without unescaped shell expansion.
- [ ] Cross-Site Scripting (XSS): No unsanitized `dangerouslySetInnerHTML` or `innerHTML`.
- [ ] User file paths validated against workspace root bounds.
