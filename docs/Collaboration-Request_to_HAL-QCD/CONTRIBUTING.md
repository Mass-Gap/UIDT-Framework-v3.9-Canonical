```markdown
# Contributing to the UIDT Framework v3.9

Thank you for your interest in contributing to the **Unified Information‑Density Theory (UIDT)** framework.  
UIDT is an independent, open research programme committed to **mathematical rigor**, **numerical reproducibility**, and **epistemic transparency**. Contributions are evaluated under strict scientific standards.

---

## 1. Mathematical Standards (Non‑Negotiable)

All contributions **must** comply with the following requirements:

### Precision
- All numerical computations **must** use `mpmath` with a minimum precision of  
  ```python
  mp.dps = 80
  ```
- Lower precision is not acceptable for physical quantities.

### No Floating‑Point Leakage
- Use of native Python `float()` for physical constants or derived quantities is **strictly prohibited**.
- All constants must be represented as `mpmath.mpf`.

### Verification
- Every new module **must** include `pytest`‑based verification tests.
- Residuals must satisfy:
  \[
  |\text{residual}| < 10^{-40}
  \]
- Tests failing this threshold will not be reviewed.

---

## 2. Evidence Classification System

Each claim, parameter, or numerical result must be explicitly tagged using the **UIDT Evidence Ledger**:

| Category | Definition |
|--------|------------|
| **A** | Analytic proof (Lipschitz / Banach fixed‑point confirmed) |
| **B** | Numerical consistency with external data (e.g. Lattice QCD) |
| **C** | Calibrated to empirical benchmarks (e.g. DESI, Planck) |

Evidence tags must be stated **explicitly** in code comments and pull‑request descriptions.

---

## 3. Epistemic Transparency

### Language Discipline
- Avoid *closure language* such as **“solved”**, **“proven”**, or **“final”** unless referring to **Category A** results.
- Numerical convergence alone does **not** constitute proof.

### Falsification Windows
- Every new feature must document:
  - Known limitations
  - Sensitivity bounds
  - Explicit falsification criteria

### Ledger Integrity
- Any modification of core ledger constants  
  \[
  \Delta^*,\ \gamma
  \]
  requires:
  - Formal review
  - Version increment
  - Updated Zenodo release

---

## 4. Collaboration with HAL QCD

For contributions involving **NBS wave functions** or the **cc‑diquark system**:

- Data **must** be provided in standardized **JSON** format.
- Uncertainties must be separated into:
  - Statistical
  - Systematic
- Contributions upgrading **Evidence Category B → A‑** are **high priority**.

---

## 5. Submission Process

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b research/new-splitting-method
   ```
3. Include a **Claims Table** in the pull‑request description specifying Evidence Categories.
4. Ensure all `mpmath` tests pass with **zero precision leakage**.
5. Submit the pull request for review.

---

## Contact

**UIDT Framework Coordination**  
📧 uidt-framework@outlook.com  

---

### Scientific Note

UIDT is an **active research programme**.  
Transparency takes precedence over narrative coherence.  
Tensions in \( H_0 \) and \( S_8 \) are documented and tracked, **not declared resolved**.
```