# UIDT Evidence Classification System v3.7.2

> **PURPOSE:** Standardized classification of all UIDT claims  
> **PRINCIPLE:** Every quantitative claim MUST be tagged with A–E

---

## Evidence Categories

### Category A — Analytically Proven
**Definition:** Mathematical proof with residuals < 10⁻¹⁴

**Requirements:**
- Complete derivation steps in LaTeX
- Numerical verification with mpmath/high-precision
- Residual threshold: |residual| < 10⁻¹⁴
- Independent reproduction possible

**Examples:**
- Δ = 1.710 ± 0.015 GeV (spectral gap) [A]
- κ = 0.500 ± 0.008 [A]
- λ_S = 5κ²/3 = 0.41̄6̄ ± 0.007 [A]
- 5κ² = 3λ_S constraint [A]
- v = 47.7 MeV [A]

---

### Category A- — Phenomenologically Determined
**Definition:** High-precision determination without first-principles derivation

**Requirements:**
- Clear methodology documented
- Numerical precision established
- Acknowledges phenomenological nature
- Open research question for theoretical derivation

**Examples:**
- γ = 16.339 (kinetic VEV) [A-]
- γ = 16.374 ± 1.005 (MC mean) [A-]

**Note:** γ is NOT derived from RG first principles. The RG derivation remains an active research field [E].

---

### Category B — Numerically Verified / Lattice Consistent
**Definition:** Agreement with independent numerical/lattice calculations

**Requirements:**
- z-score < 1σ for consistency
- Reference to external calculation
- Statistical methodology documented

**Examples:**
- Lattice QCD consistency: z = 0.37σ [B]
- Branch 1 residual: 3.2×10⁻¹⁴ [B]
- Numerical closure: < 10⁻¹⁴ [B]

---

### Category C — Calibrated to External Data
**Definition:** Fitted to observational/experimental data

**Requirements:**
- Explicit data source cited
- Fitting methodology documented
- **Cannot claim independent prediction**
- Cosmology claims MAXIMUM Category C

**Examples:**
- H₀ = 70.4 ± 0.16 km/s/Mpc (DESI DR2) [C]
- λ_UIDT = 0.660 ± 0.005 nm [C]
- S₈ = 0.814 ± 0.009 [C]

> ⚠️ **RULE:** ALL cosmology claims are Category C or lower. Never A/B.

---

### Category D — Predictive, Unverified
**Definition:** Theoretical prediction awaiting experimental test

**Requirements:**
- Clear falsification criterion
- No experimental confirmation yet
- Listed in LEDGER/FALSIFICATION.md

**Examples:**
- Casimir anomaly: +0.59% at 0.66 nm [D]
- Scalar mass m_S = 1.705 ± 0.015 GeV [D]
- LHC scalar resonance 1.5-1.9 GeV [D]
- Casimir optimal distance d = 0.854 nm [D]

---

### Category E — Speculative / Open / Withdrawn
**Definition:** Exploratory ideas or retracted claims

**Sub-types:**
- **E (speculative):** Research hypotheses, unproven
- **E (open):** Active research questions
- **E (withdrawn):** Previously claimed, now retracted

**Examples:**
- γ RG derivation from first principles [E-open]
- Glueball identification at 1.71 GeV [E-withdrawn, 2025-12-25]
- N=99 RG steps justification [E-open]
- 10¹⁰ geometric factor derivation [E-open]

---

## Upgrade/Downgrade Rules

### Upgrade Path
```
E → D: Theoretical foundation established
D → C: Calibration to data achieved
C → B: Independent numerical verification
B → A-: Systematic derivation (phenomenological)
A- → A: First-principles derivation with < 10⁻¹⁴ residuals
```

### Downgrade Triggers
```
A → B: Residuals exceed 10⁻¹⁴
B → C: Lattice inconsistency (z > 3σ)
C → D: Data source invalidated
D → E: Experimental falsification
Any → E-withdrawn: Explicit retraction
```

### Documentation Requirement
Every category change MUST be logged in `LEDGER/CLAIMS.json` with:
- Timestamp
- Previous category
- New category
- Justification
- Reference

---

## Quick Reference

| Category | Residual Threshold | Cosmology Allowed? | Requires Derivation? |
|----------|-------------------|-------------------|---------------------|
| A | < 10⁻¹⁴ | ❌ Never | ✅ Full |
| A- | N/A | ❌ Never | ⚠️ Phenomenological |
| B | z < 1σ | ❌ Never | ✅ Numerical |
| C | N/A | ✅ Maximum | ❌ Calibration only |
| D | N/A | ✅ Yes | ❌ Prediction only |
| E | N/A | ✅ Yes | ❌ Speculative |

---

**CITATION:** Rietz, P. (2025). UIDT v3.7.2. DOI: 10.5281/zenodo.17835200
