# Security Policy

## Supported Versions

| Version | Supported |
|---------|----------|
| v3.9.x  | ✅ Active |
| v3.7.x  | ⚠️ Critical fixes only |
| < v3.7  | ❌ End of life |

## Reporting a Vulnerability

If you discover a security vulnerability, a data integrity issue, or a scientific
error with security implications in this repository, please report it responsibly.

**Contact:** badbugs.arts@gmail.com  
**Subject format:** `[SECURITY] UIDT v3.9 - <Brief Description>`

**Response timeline:**
- Acknowledgment: within 48 hours
- Initial assessment: within 7 days
- Resolution or public disclosure decision: within 30 days

## Scope

This policy covers:
- Verification scripts (`verification/scripts/`)
- Core proof engine (`core/`)
- Physical modules (`modules/`)
- Canonical parameter files (`CANONICAL/`)
- Ledger and claims database (`LEDGER/`)

## Out of Scope

- Theoretical disputes about the UIDT framework (use GitHub Issues instead)
- Minor documentation typos

## Dependencies

Security-relevant dependencies are pinned to standard scientific computing libraries:
`numpy`, `scipy`, `mpmath`, `matplotlib`. No network-facing services are included.

## Docker

Docker environments in `verification/docker/` run without root privileges
and use a minimal attack surface.

**License:** CC BY 4.0 — P. Rietz (ORCID: 0009-0007-4307-1609)
