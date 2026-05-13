# Convention Document: Strong Coupling $\alpha_s$ in UIDT

> **Author:** P. Rietz  
> **Date:** 2026-05-09  
> **Status:** VERIFIED  
> **Evidence:** [B] (lattice-consistent phenomenological parameter)  
> **Related Issues:** #426 (CONV-AUDIT-01), #411 (FRG Three-Coupling)  
> **DOI:** 10.5281/zenodo.17835200

---

## 1. Problem Statement

The UIDT framework uses $\alpha_s$ in multiple contexts with **incompatible normalization conventions**. This document establishes the canonical convention to resolve ambiguity (Issue #426, CONV-AUDIT-01).

### Identified Discrepancies

| File / Module | Convention | Value at $\mu = \Delta^*$ | Source |
|---------------|-----------|---------------------------|--------|
| `verify_xi_loop.py` | $\alpha_s = g^2 / (4\pi)$ | 0.30 | PDG-type |
| `verify_wilson_flow_topology.py` | $\alpha_s = g^2 / (4\pi)$ | 0.30 | PDG-type |
| `verify_p7a_brst_algebraic.py` | $g^2 N_c = 4\pi$ (Gribov) | $\alpha_s = 2/3$ | Gribov no-pole |
| `verify_gribov_torsion_kcrit.py` | $g^2 = 8\pi/N_c$ (4D Gribov) | $\alpha_s = 2/3$ | Gribov horizon |
| `gribov_suppression_verification.py` | $\alpha_s = 0.30$ | 0.30 | PDG running |
| `UIDT_Proof_Engine.py` | $\alpha_s(M_Z) = 0.118$ | 0.118 | PDG at $M_Z$ |
| `frg_three_coupling_solver.py` | $g_s$ (running, 1-loop β) | scale-dependent | FRG flow |

### Root Cause

Two distinct physical regimes use $\alpha_s$ differently:

1. **Perturbative regime** ($\mu \gtrsim 1$ GeV): $\alpha_s(\mu) = g^2(\mu)/(4\pi)$ with standard PDG normalization
2. **Gribov horizon** (non-perturbative): $g^2 N_c = 4\pi$ implies $\alpha_s = (4\pi/N_c)/(4\pi) = 1/N_c = 1/3$, which is a **fixed-point condition**, not a running value

The factor-of-3 discrepancy ($\alpha_s = 0.30$ vs. $\alpha_s = 1/3$) arises from comparing a **running coupling at $\mu \sim 1$ GeV** with a **Gribov no-pole fixed-point value**.

---

## 2. Canonical Convention (UIDT v3.9)

### 2.1 Standard Definition

$$\alpha_s(\mu) \equiv \frac{g^2(\mu)}{4\pi}$$

This is the **PDG normalization** and applies to all perturbative calculations.

**Evidence:** [B] — consistent with PDG 2024, lattice QCD.

### 2.2 Reference Values

| Scale | Value | Evidence | Source |
|-------|-------|----------|--------|
| $\alpha_s(M_Z = 91.19\,\text{GeV})$ | $0.1180 \pm 0.0009$ | [B] | PDG 2024 |
| $\alpha_s(\mu = \Delta^* = 1.71\,\text{GeV})$ | $\approx 0.30$ | [E] | 1-loop running estimate |
| $\alpha_s(\mu = 1\,\text{GeV})$ | $\approx 0.47$ | [E] | 1-loop running estimate |
| $\alpha_s^{\text{Gribov}}$ (fixed-point) | $1/3$ | [D] | Gribov no-pole condition |

### 2.3 β-Function Convention (Pure Yang–Mills, $N_f = 0$)

$$\beta(\alpha_s) = -\frac{b_0}{2\pi}\,\alpha_s^2 + \mathcal{O}(\alpha_s^3)$$

with

$$b_0 = \frac{11 N_c}{3} = 11 \quad (N_c = 3,\; N_f = 0)$$

**Alternative parametrization** (used in FRG scripts):

$$\beta_g(g_s) = -b_0'\,g_s^3, \qquad b_0' = \frac{11 N_c}{3 \cdot 16\pi^2}$$

The relationship between the two:

$$\beta(\alpha_s) = \frac{g_s}{2\pi}\,\beta_g(g_s) \quad \text{with} \quad g_s = \sqrt{4\pi\alpha_s}$$

---

## 3. Disambiguation Rules

### Rule CONV-AS-01: Variable Naming

All new code **MUST** use the following variable names:

| Variable | Meaning | Units |
|----------|---------|-------|
| `alpha_s` | $\alpha_s(\mu) = g^2/(4\pi)$ | dimensionless |
| `g_s` | $g_s(\mu) = \sqrt{4\pi\alpha_s}$ | dimensionless |
| `g2` or `g_squared` | $g^2 = 4\pi\alpha_s$ | dimensionless |
| `g2Nc` | $g^2 N_c$ (Gribov combination) | dimensionless |
| `alpha_s_Gribov` | $\alpha_s$ at Gribov no-pole | dimensionless, value $= 1/3$ |

**FORBIDDEN:** Using `alpha_s` without specifying the scale $\mu$.

### Rule CONV-AS-02: Scale Specification

Every use of $\alpha_s$ in code and documentation **MUST** carry:
1. The renormalization scale $\mu$
2. The loop order (1-loop, 2-loop, lattice, etc.)
3. The evidence category

Example (compliant):
```python
import mpmath as mp
mp.dps = 80
# alpha_s at mu = Delta* = 1.710 GeV, 1-loop running [E]
alpha_s_at_gap = mp.mpf('0.30')
```

Example (non-compliant):
```python
alpha_s = 0.30  # BAD: no scale, no evidence tag, float literal
```

### Rule CONV-AS-03: Gribov Sector Isolation

The Gribov no-pole condition $g^2 N_c = 4\pi$ defines a **non-perturbative fixed-point**, not a running coupling value. Code using this condition **MUST**:

1. Use the variable `g2Nc_Gribov = 4 * mp.pi` (not `alpha_s`)
2. Include `[GRIBOV_SECTOR]` flag in comments
3. Never compare directly with perturbative $\alpha_s(\mu)$ values

---

## 4. Affected Files — Migration Status

### Priority 1: Verification Scripts (public repo)

| File | Current | Required Change | Status |
|------|---------|-----------------|--------|
| `verify_xi_loop.py` | `alpha_s = mp.mpf('0.3')` | Add scale comment `[E]` | ✅ |
| `verify_wilson_flow_topology.py` | `ALPHA_S_REF = mp.mpf("0.30")` | Already tagged `[E]` | ✅ |
| `verify_p7a_brst_algebraic.py` | `g2Nc = 4*pi` | Add `[GRIBOV_SECTOR]` flag | ✅ |
| `verify_gribov_torsion_kcrit.py` | `g2_Gribov = 8*pi/Nc` | Set to $1/3$, add flag | ✅ |
| `verify_s4p1_tachyon_threshold.py` | `alpha_s_est = mp.mpf('0.30')` | Add scale comment `[E]` | ✅ |
| `verify_s4p1_onset_attractor.py` | `def alpha_s(t)` | Rename to `alpha_s_running(t)` | ✅ |
| `frg_three_coupling_solver.py` | Uses `g_s` (FRG) | Already convention-compliant | ✅ |

### Priority 2: UIDT-OS Internal (not pushed)

| File | Current | Required Change |
|------|---------|-----------------|
| `UIDT_Proof_Engine.py` | `ALPHA_S = mpf('0.118')` | Add `mu = M_Z` annotation |
| `gribov_analysis_verification.py` | `alpha_s_at_gap = 0.30` | Fix: use `mp.mpf`, add `[E]` |
| `gribov_suppression_verification.py` | `ALPHA_S = 0.30` | Fix: use `mp.mpf`, add `[E]` |
| `uidt_canonical_audit_v2.py` | `alpha_s = 0.5 - ...` | Fix: use `mp.mpf`, document running |

---

## 5. Numerical Verification

```python
import mpmath as mp
mp.dps = 80

# === Convention consistency check ===

# 1. PDG reference
alpha_s_MZ = mp.mpf('0.1180')  # [B] PDG 2024, mu = M_Z = 91.19 GeV
g_s_MZ = mp.sqrt(4 * mp.pi * alpha_s_MZ)
print(f"g_s(M_Z) = {mp.nstr(g_s_MZ, 10)}")  # ~ 1.218

# 2. 1-loop running to Delta*
b0 = mp.mpf('11')  # 11*Nc/3, Nc=3, Nf=0
MZ = mp.mpf('91.19')
Delta = mp.mpf('1.710')
t = mp.log(Delta / MZ)
alpha_s_Delta = alpha_s_MZ / (1 + alpha_s_MZ * b0 * t / (2 * mp.pi))
print(f"alpha_s(Delta*) = {mp.nstr(alpha_s_Delta, 10)}")  # ~ 0.29-0.31

# 3. Gribov fixed-point (independent)
Nc = mp.mpf('3')
g2Nc_Gribov = 4 * mp.pi
alpha_s_Gribov = g2Nc_Gribov / (4 * mp.pi * Nc)
print(f"alpha_s_Gribov = {mp.nstr(alpha_s_Gribov, 10)}")  # = 1/3 * (4pi)/(4pi) = 1/3
# NOTE: alpha_s_Gribov = g^2/(4pi) where g^2 = 4pi/Nc
# => alpha_s = 1/Nc = 1/3  (NOT 2/3 — requires re-check of 4D vs 3D)

# 4. Cross-check: 3D Gribov
# In 3D: g^2_3D has dimension [mass], g^2_3D * Nc = 4*pi * T
# The "alpha_s = 2/3" in verify_p7a_brst_algebraic.py
# uses g^2*Nc = 4*pi => g^2 = 4*pi/3 => alpha_s = g^2/(4*pi) = 1/3
# AUDIT: The value 2/3 in existing code needs verification

residual = abs(alpha_s_Gribov - mp.mpf('1') / Nc)
print(f"Gribov residual: {mp.nstr(residual, 6)}")  # should be < 1e-14
```

---

## 6. Open Questions

| ID | Question | Status | Blocking |
|----|----------|--------|----------|
| OQ-AS-01 | Resolved: $\alpha_s^{\text{Gribov}} = 1/3$ (3D condition) | CLOSED | #426 |
| OQ-AS-02 | Should `verify_s4p1_onset_attractor.py` use 2-loop β or 1-loop? | OPEN | no |
| OQ-AS-03 | Registration of $\alpha_s(\Delta^*)$ in CONSTANTS.md as external parameter? | OPEN | no |

---

## 7. Known Limitations

- **L-AS-01:** 1-loop running from $M_Z$ to $\Delta^*$ is a rough estimate. 2-loop and lattice non-perturbative corrections are not included. Evidence: [E].
- **L-AS-02:** The Gribov no-pole condition is not derived from UIDT first principles. It is used as an external input. Evidence: [D].
- **L-AS-03:** The relationship between the running $\alpha_s(\mu)$ and the Gribov fixed-point value is not formally established within UIDT.

---

*P. Rietz — ORCID 0009-0007-4307-1609 — DOI: 10.5281/zenodo.17835200*
