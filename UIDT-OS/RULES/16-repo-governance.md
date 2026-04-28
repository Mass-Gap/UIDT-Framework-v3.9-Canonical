---
alwaysApply: false
description: Apply for branching, PR titles, protected paths, or evidence tag changes.
---
# Repo Governance (Intelligent)

- Protected/internal paths are read-only for public changes: `UIDT-OS/**`, `.trae/**`, `.kiro/**`, `LOCAL/**`, `.claude/**`, `.mcp.json`, `SECURITY.md`, `AGENTS.md`.
- Never modify `CANONICAL/**` or `LEDGER/**` on `main` unless explicitly instructed.
- Never change evidence tags [A–E] without explicit instruction from P. Rietz.
- Always work on a ticket branch `TKT-YYYY-MM-DD-<transparent-name>-<id>`; never push directly to `main`.
- PR title format: `feat|fix|docs: <Description> (TKT-XXX)`.
- PR body must include the Quality-Gate checklist and list affected constants + evidence categories.
- γ is always calibrated [A-]; cosmology statements are capped at [C].
- **Branch Hygiene:** All local feature branches must be pushed to `origin` periodically. Abandoned or "forgotten" local branches violate the CERN/Clay reproducibility standard.
- **SLSA Integrity:** Any attempt to bypass automated SBOM generation or cryptographic signing in `release.yml` is a blocking violation. OIDC trust for Sigstore/Cosign must be maintained.
- **Zero-Trust Review:** Core physics modules (`core/`) and the SSOT ledger (`CANONICAL/`, `LEDGER/`) require a 3-agent consensus (Guardian Veto System) before being queued for Opus 4.7 merge.
- **Audit Readiness:** The repository must be 100% reproducible via the provided `Dockerfile` and `REPRODUCE.md` at any commit SHA.
