# UIDT Known Limitations v3.7.2

> **PURPOSE:** Transparent documentation of unresolved issues  
> **PRINCIPLE:** Acknowledge what we don't know

---

## Active Limitations (Unresolved)

### L1: 10¹⁰ Geometric Factor
**Status:** 🔬 HIGHEST PRIORITY

**Description:**  
The ratio λ_UIDT / λ_theoretical involves a factor of ~10¹⁰ that lacks first-principles derivation.

**Impact:**  
- λ_UIDT calibrated [C] instead of derived [A]
- Undermines claim of "parameter-free" theory

**Condition for Resolution:**  
Derive geometric factor from fundamental principles (topology, holography, etc.)

---

### L2: Electron Mass Discrepancy
**Status:** ⚠️ PARTIAL

**Description:**  
Electron mass formula shows 23% residual (was 3.2% in earlier versions).

**Impact:**  
- m_e prediction remains approximate
- Electroweak sector not fully integrated

**Condition for Resolution:**  
Improved electroweak coupling in UIDT framework

**Note:** v3.6.1 patch addressed some issues but not fully resolved.

---

### L3: Vacuum Energy Residual
**Status:** ✅ ACCEPTED

**Description:**  
Vacuum energy prediction ρ_vac differs from Λ_QCD calibration by factor ~2.3.

**Impact:**  
- Order-of-magnitude correct (vs. 10¹²⁰ problem)
- Factor 2.3 within theoretical uncertainty

**Resolution:**  
Accepted as within framework tolerance. 99-step RG cascade + π⁻² normalization addresses 10¹²⁰ catastrophe.

---

### L4: γ Not Derived from RG
**Status:** 🔬 ACTIVE RESEARCH

**Description:**  
γ = 16.339 is phenomenologically determined from kinetic VEV, NOT derived from RG flow equations.

**Impact:**  
- γ is Category [A-] not [A]
- Claims of "first-principles" derivation are INCORRECT
- Perturbative RG gives γ* ≈ 55.8 (factor 3.4 discrepancy)

**Condition for Resolution:**  
- Show γ = 49/3 = (2Nc+1)²/Nc from QCD
- OR derive from non-perturbative FRG
- OR accept as empirical constant

**Note:** In RESEARCH-MODE, exploring γ derivation is permitted with [E] tag.

---

### L5: N=99 RG Steps Unjustified
**Status:** 🔬 ACTIVE RESEARCH

**Description:**  
The 99-step RG cascade is empirically chosen; no theoretical derivation exists.

**Impact:**  
- Vacuum energy suppression mechanism phenomenological
- Raises question: why exactly 99?

**Condition for Resolution:**  
Physical/mathematical derivation of N=99 from first principles

**Hypotheses:**
- Related to number of SM degrees of freedom?
- Holographic dimension counting?
- Accidental numerical coincidence?

---

## Resolved Limitations (Historical)

### L6: Spectral Gap vs. Particle Mass [RESOLVED]
**Status:** ✅ CLARIFIED

**Previous Issue:**  
Δ = 1.710 GeV was sometimes conflated with glueball mass.

**Resolution (2025-12-25):**  
Δ is the SPECTRAL GAP of Yang-Mills Hamiltonian, NOT a particle mass.
Glueball identification explicitly WITHDRAWN [E].

---

### L7: VEV Value [RESOLVED]
**Status:** ✅ CORRECTED

**Previous Issue:**  
v = 0.854 MeV in Framework v3.2

**Resolution (v3.6.1):**  
Corrected to v = 47.7 MeV. Old value was erroneous.

---

## Limitation Impact Matrix

| ID | Limitation | Impact on Claims | Priority |
|----|------------|-----------------|----------|
| L1 | 10¹⁰ factor | λ_UIDT [C→D if unresolved] | 🔴 High |
| L2 | Electron mass | m_e formula approximate | 🟡 Medium |
| L3 | Vacuum energy | ρ_vac factor 2.3 | 🟢 Accepted |
| L4 | γ not from RG | γ remains [A-] not [A] | 🔴 High |
| L5 | N=99 unjustified | RG cascade phenomenological | 🟡 Medium |

---

## Falsification Triggers

If any of these occur, UIDT requires major revision:

1. **Lattice QCD:** Δ ≠ 1.710 GeV at >3σ
2. **Casimir:** |ΔF/F| < 0.1% at d ≈ 0.66 nm (no anomaly)
3. **DESI:** w = -1.00 ± 0.01 exactly (pure ΛCDM)
4. **LHC:** Scalar excluded in 1.5-1.9 GeV window

See `LEDGER/FALSIFICATION.md` for details.

---

**CITATION:** Rietz, P. (2025). UIDT v3.7.2. DOI: 10.5281/zenodo.17835200
