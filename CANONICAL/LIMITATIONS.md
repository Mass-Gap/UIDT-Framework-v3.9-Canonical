# UIDT Known Limitations v3.9.5

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

**Note:** Claim UIDT-C-070 (Evidence C, upgraded 2026-04-06) provides a FRG mechanism for the
functional form γ ~ (Λ_UV/Λ_IR)^{η_*} via the YM ghost-gluon fixed point. This does NOT
upgrade γ to [A]; see L6 and L8 for truncation and LPA caveats.

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

### L6: FRG Derivation of γ — Minimal Truncation (v3.9.5)
**Status:** 🔬 ACTIVE RESEARCH  
**Claim:** UIDT-C-070 (Evidence C after 2026-04-06 upgrade, Stratum III)

**Description:**  
The FRG derivation of the γ-mechanism (Claim UIDT-C-070) was initiated with a minimal truncation with:
- η_A = 0 (background-field approximation; gluon fluctuations not fully accounted for)
- A single dimension-5 operator S F² without higher-dimensional operators (e.g. S² F²)
- An optimised Litim regulator in the w → 0 limit (conformal window)

The initial anomalous dimension η_* ≈ 0.072 (Evidence D) has been upgraded via the YM
ghost-gluon sector (see L8). The Cauchy deformation protocol ([CAUCHY_CLOSURE]) is
mandatory for all future momentum-dependent FRG runs.

**Condition for Resolution (Evidence C → B):**  
1. Full momentum projection (∂_{p²}) with Gauss-Chebyshev grid  
2. Inclusion of S²F² operator  
3. η_A running (non-zero)

---

### L8: YM Ghost-Gluon Sector — LPA Vertex-Dressing Gap (NEW — v3.9.5)
**Status:** 🔬 ACTIVE RESEARCH  
**Claim:** UIDT-C-070 (Evidence C, upgraded 2026-04-06)

**Description:**  
The YM ghost-gluon fixed-point run (`verification/scripts/solve_ym_ghosts.py`, mp.dps=80)
yields a dynamically generated gluon mass parameter w_g* = 0.076085851788367353521.
This replaces the previous Stratum-II external input (w_g = 0.25 from DSE/lattice).

The residual gap Δw_g ≈ 0.174 between w_g* and the DSE/lattice value (~0.25) is a known,
documented consequence of the LPA approximation with Z₁ = 1 (no vertex dressing). It is
**not** a numerical error.

**Numerical result (80-dps, deterministic):**
- η_c* = 0.022641406591847240692
- η_A* = 0.14097863338118157839
- w_g* = 0.076085851788367353521
- Stability eigenvalues: +0.999, +1.027, -2.140 (all real — no truncation artefact)
- All 3 residuals < 1e-75

**Physical interpretation:**  
w_g* > 0 confirms that Yang-Mills dynamics generates a non-trivial mass gap deterministically
in the LPA engine. The inequality w_g* > 0 is the fundamental result; the quantitative gap
to the DSE value is the expected LPA artefact.

**Impact:**  
- UIDT-C-070 upgraded from Evidence D to Evidence C (partial verification)
- γ = 16.339 remains strictly [A-] (see L4)
- w_g = 0.25 (Stratum II, external) no longer required as primary input

**Condition for Resolution (Evidence C → B):**  
Inclusion of vertex dressing (Z₁ ≠ 1) and full p²-dependent flow for the ghost-gluon vertex.
Expected to close the Δw_g ≈ 0.174 gap and push w_g* toward ~0.25.

**References:**
- Cyrol et al., arXiv:1605.01856 (Stratum II, verified)
- `verification/scripts/solve_ym_ghosts.py`
- `LEDGER/CLAIMS_C070_upgrade.json`

---

## Resolved Limitations (Historical)

### L7: Spectral Gap vs. Particle Mass [RESOLVED]
**Status:** ✅ CLARIFIED

**Previous Issue:**  
Δ = 1.710 GeV was sometimes conflated with glueball mass.

**Resolution (2025-12-25):**  
Δ is the SPECTRAL GAP of Yang-Mills Hamiltonian, NOT a particle mass.
Glueball identification explicitly WITHDRAWN [E].

---

## Limitation Impact Matrix

| ID | Limitation | Impact on Claims | Priority |
|----|------------|-----------------|----------|
| L1 | 10¹⁰ factor | λ_UIDT [C→D if unresolved] | 🔴 High |
| L2 | Electron mass | m_e formula approximate | 🟡 Medium |
| L3 | Vacuum energy | ρ_vac factor 2.3 | 🟢 Accepted |
| L4 | γ not from RG | γ remains [A-] not [A] | 🔴 High |
| L5 | N=99 unjustified | RG cascade phenomenological | 🟡 Medium |
| L6 | FRG truncation (S F²) | η_* ~ 0.072, Evidence D→C | 🟡 Medium |
| L8 | LPA vertex-dressing gap | w_g* = 0.076 vs DSE ~0.25 | 🟡 Medium |

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
