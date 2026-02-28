# Quality Criteria for Evidence-Based Pull Requests (UIDT)

## 1. Language Constraints (Non-Negotiable)
- No prestige/closure language: “ultimate”, “holy grail”, “definitive solution”, “resolved” unless the claim is Category A/A- with the required numerical residual threshold.
- Cosmology: never claim “resolved” for H₀/S₈ tensions; cosmology claims are capped at Category C.

## 2. Evidence Stratification (Required Structure)
Every PR that touches scientific claims must explicitly separate:
- **Stratum I (Empirical):** direct measurements with stated uncertainties and a citation.
- **Stratum II (Consensus):** current field-level status (“tension persists”, “model-dependent”, etc.) with an appropriate review citation if available.
- **Stratum III (UIDT):** interpretive mapping to UIDT parameters, labeled as interpretive/hypothetical if not externally validated.

## 3. Citation & DOI Requirements
- Every external numeric value must have at least one of:
  - DOI that resolves via doi.org
  - arXiv identifier + arXiv DOI (10.48550/arXiv.xxxxx)
  - Publisher URL (only if DOI is unavailable)
- The cited paper must actually contain the stated value in the stated context (no “nearby” or “similar” paper substitution).
- Bibliography entries must include resolvable identifiers (DOI or arXiv), not placeholders.

## 4. Numerical Claims & Uncertainty Budgets
- Do not quote “tight” uncertainties unless they appear explicitly in the cited source and you state what they represent (stat/sys/SN covariance, etc.).
- Any z-score or “σ agreement” statement must specify:
  - Which two quantities are compared
  - How the combined uncertainty was constructed
  - Whether correlations are included (and if not, explicitly marked heuristic)
- Comparisons must never treat UIDT-internal calibrated values as empirical ground truth.

## 5. Implementation Checklists (PR Gate)
Before a PR is merged, the submitter must provide:
- A “Claims Table” listing each claim, its evidence category, and the source identifier(s).
- A “Reproduction Note” (one command) to reproduce every quantitative check.
- A DOI/arXiv resolvability check result for all cited identifiers.

