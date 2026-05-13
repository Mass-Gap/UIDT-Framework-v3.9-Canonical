# AGENTS.md - UIDT Framework v3.9 Agent Governance

> **INTERNAL DOCUMENT** - Do NOT commit this file to public repositories.
> This file defines the operating constraints for all AI agents working on the UIDT project.

## Document Status
- Version: 13 (AGENTS-13)
- Classification: Internal / Governance
- Maintainer: P. Rietz (@badbugs.arts)
- Last updated: 2025

---

## 1. Agent Hierarchy

### 1.1 Principal Investigator (PI)
- **Identity**: P. Rietz (@badbugs.arts)
- **Role**: Sole authority for protected-path modifications, releases, canonical constant updates
- **Scope**: Unlimited (within project governance)
- **Approval required for**: All protected-path PRs, release tags, CANONICAL/ changes

### 1.2 Jules Junior Lead (JJL)
- **Identity**: Jules (AI assistant operating under PI supervision)
- **GitLab**: Operates via CI/CD pipeline or MR comments
- **Permitted scope**:
  - Classification labels in comments and docstrings
  - Documentation updates (docs/, README sections)
  - Verification/test additions (add only, never delete >10 lines)
  - Non-critical bug fixes in non-protected paths
- **Forbidden scope**:
  - core/, modules/, CANONICAL/, LEDGER/, clay-submission/
  - Any file tagged [PROTECTED] or [CANONICAL]
  - Self-merge or self-approval of own PRs
  - Modifying gamma=16.339 or any A-calibrated constant
  - Committing UIDT-OS, SECURITY.md internal details

### 1.3 Sub-Agents (Numerical/Literature/Doc/Guardian)
- **uidt-numerical-verifier**: mpmath residual verification (mp.dps=80)
- **uidt-literature-scanner**: DOI/arXiv validation, UNVERIFIED-DOI tagging
- **uidt-doc-formatter**: Academic English formatting, LaTeX output
- **uidt-guardian-consensus**: Cross-agent consistency and governance audit
- **Permitted**: Read access to all non-protected files, write to agent-output/, reports/
- **Forbidden**: Direct commits to any git branch

---

## 2. Canonical Constants (SSOT)

| Constant | Value | Uncertainty | Classification | Notes |
|---|---|---|---|---|
| gamma | 16.339 | +/- 1.005 | A- | Never upgrade to A without Clay proof |
| delta | 1.710 | +/- 0.015 | A- | |
| kappa | 0.500 | +/- 0.008 | A- | |
| lambda_s | 0.417 | +/- 0.007 | B | |
| H0 | 70.4 | +/- 0.16 | C | Cosmological - Category C cap |
| w0 | -0.99 | - | C | Cosmological - Category C cap |
| M_s | 1.705 | +/- 0.015 | B | |

**Classification rules**:
- **A**: Mathematically proven to Clay/Millennium standard (none yet)
- **A-**: Numerically verified to mp.dps=80, residual < 1e-14, multi-method convergence
- **B**: Strongly supported by multiple independent calculations
- **C**: Category ceiling for all cosmological claims, regardless of internal confidence

---

## 3. Governance Rules (Summary)

### Rule 01 - Single Source of Truth (SSOT)
- CANONICAL/ and LEDGER/ are the sole sources of truth for all constants and claims
- No agent may derive or override canonical constants without PI approval

### Rule 02 - Branch Protection
- main branch: protected, no direct push, no self-merge
- All PRs require codeowner approval (@badbugs.arts)
- PRs touching protected paths require explicit PI review comment

### Rule 03 - Evidence Tagging
- All evidence must have: stratum label, uncertainty, source DOI/arXiv
- Unverified DOIs: tag as UNVERIFIED-DOI
- AI-generated content without verification: tag as AI-ARTIFACT-RISK

### Rule 04 - Release Protocol
- Tags v3.9.* are protected, created by Maintainers only
- Each release requires: Zenodo DOI coordination, PI approval, CHANGELOG entry
- arXiv submission coordinated with release

### Rule 05 - Self-Merge Prohibition
- No agent (human or AI) may merge their own MR
- Violation is grounds for immediate PR closure

### Rule 06 - Numerical Verification Standard
- All numerical claims require mpmath verification with mp.dps >= 80
- Residual must be < 1e-6 (preferred: < 1e-14 for A- classification)
- Inline float calculations are insufficient for canonical verification

### Rule 07 - Cosmological Claims Cap
- All cosmological/observational claims are capped at Category C
- No cosmological claim may be elevated to A or A- regardless of internal confidence

### Rule 08 - Confidentiality
- UIDT-OS internal architecture details must NEVER be committed
- SECURITY.md internal threat model must NEVER be exposed
- AGENTS.md itself must NEVER be committed to public repositories
- Local absolute paths and personal config files must NEVER be committed

---

## 4. Workflow: Agent PR Protocol

1. Agent creates branch from main (never commits directly to main)
2. Agent opens MR as **Draft** using UIDT_Contribution template
3. Agent completes governance checklist in MR description
4. For protected paths: Agent requests PI review via MR comment
5. PI reviews, approves, and removes Draft status
6. CI pipeline runs all audit stages (pre-audit through synthesis)
7. PI merges (never the agent)
8. Release tag created by PI only

---

## 5. Prohibited Actions (All Agents)

- Modify core/, modules/, CANONICAL/, LEDGER/ without PI approval
- Change gamma=16.339 or any A-calibrated constant
- Self-merge or self-approve PRs
- Commit local config files (.env, .trae, .claude, local paths)
- Commit UIDT-OS, SECURITY.md internal details, AGENTS.md
- Elevate cosmological claims above Category C
- Use inline floats for canonical numerical verification
- Delete evidence labels or stratum tags
- Merge non-Draft PRs without running full CI pipeline

---

*This document is the operating constitution for all UIDT project agents.*
*Violations of these rules will result in immediate PR closure and agent scope review.*