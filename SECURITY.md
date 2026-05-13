# Security Policy - UIDT Framework v3.9

## Reporting Security Issues

To report a security vulnerability, please contact the maintainer:

- **Maintainer**: P. Rietz (@badbugs.arts)
- **Method**: Open a confidential issue in this project

Do NOT create a public issue for security vulnerabilities.

## Supported Versions

| Version | Supported |
|---|---|
| v3.9.x | Yes (current) |
| < v3.9 | No |

## Security Principles

### Data Integrity
- Canonical constants are read-only in CI/CD scope
- Changes to CANONICAL/ and LEDGER/ require PI approval
- Commits tracked with SHA256 manifests in audit trail

### Access Control
- Branch main: protected, no direct push, no self-merge
- Release tags v3.9.*: Maintainers only
- CODEOWNERS routes all approvals to @badbugs.arts

### CI/CD Security
- All secrets stored as masked CI/CD variables (never in files)
- GH_TOKEN is masked and protected
- Deploy tokens are read-only
- Sub-agents have no git commit access

### AI Agent Security
- AI agents operate under scope limitations (see AGENTS.md)
- Sub-agents may not commit to any git branch directly
- Jules Junior Lead scope is limited to non-protected paths
- Agent outputs go to agent-output/ or reports/ directories

## Responsible Disclosure

Security researchers who report valid vulnerabilities will be credited (with permission) in the CHANGELOG.

## Known Constraints

- This is a research repository; security model is academic/collaborative
- Internal governance documents (UIDT-OS, local configs) must never be committed