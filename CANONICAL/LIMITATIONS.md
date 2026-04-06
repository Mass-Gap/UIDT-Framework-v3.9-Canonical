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

**Note:** In RESEARCH-MODE, exploring γ derivation is permitted with [E] tag.  
**See also:** UIDT-C-070 (FRG fixed-point projection, Evidence D), UIDT-C-072 (Dilaton sourcing, Evidence B).

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

### L8: Z2 Symmetry Collapse — No Non-Trivial κ² Fixed Point in the ⟨S⟩=0 Phase
**Status:** 🔴 RESOLVED BY ARCHITECTURE DECISION (2026-04-06)

**Description:**  
`[Z2_SYMMETRY_COLLAPSE]` In the strict ⟨S⟩ = 0 phase, the Z₂ symmetry (S → −S) of the Yang–Mills scalar sector forbids a linear g²-source term in β_{κ²}. A Newton–Raphson solver on the minimal 3×3 system (g², λ̃_S, κ̃²) with mp.dps = 80 deterministically collapses κ² → 0 regardless of starting magnitude, as no RG mechanism can generate a non-zero ⟨S⟩ from a pure Yang–Mills vacuum without explicit symmetry breaking.

**Impact:**  
- The minimal S F² truncation (UIDT-C-070, Evidence D) does NOT possess a non-trivial κ² fixed point in this phase.
- The spiral complex eigenvalues previously observed are confirmed as truncation artefacts of the massless Z₂-symmetric sector.
- The Gatekeeper Run (2026-04-06, 3×3 system, mp.dps = 80) constitutes a deterministic proof of this theorem.

**Condition for Resolution:**  
Two architecturally valid resolutions exist:  
1. **VEV path (Evidence C):** Add a classical symmetry-breaking potential V(S) ∝ −m²S² + λ_S S⁴, inducing ⟨S⟩ = v_S ≠ 0. Generates the required linear κ-source term but introduces a Higgs-portal structure.
2. **Dilaton/Trace-Anomaly path (Evidence B):** Identify S with the dilaton — the Goldstone boson of broken scale invariance. The gluon condensate ⟨F²⟩ ≠ 0 provides a permanent UV source via the trace anomaly θ^μ_μ = (β(g)/2g) F²_μν, coupling S fundamentally to the QCD scale anomaly without requiring a classical VEV. This path is architecturally consistent with the title "Vacuum Information Density as the Fundamental Geometric Scalar" and is adopted in UIDT-C-072.

**Architecture Decision (2026-04-06):**  
The Dilaton/Trace-Anomaly path (Option 2) is canonically adopted. See UIDT-C-072.

---

### L9: FRG Truncation Artefact in γ Derivation (Dilaton Sector)
**Status:** 🔬 ACTIVE RESEARCH

**Description:**  
The FRG derivation of the γ mechanism (UIDT-C-070, C-072) operates with minimal truncation: η_A = 0 (background-field approximation, gluon fluctuations not fully captured), a single S F²-operator without higher-dimensional extensions (S²F², ∂²S F², ...), and the optimised Litim regulator in the w → 0 conformal limit.

**Impact:**  
- η_* ≈ 0.072 (current) vs. η_* ≈ 0.063 (phenomenological threshold). Gap Δη ≈ 0.009 attributed to missing gluon anomalous dimension η_A and higher operators.
- Complex IR eigenvalues of the stability matrix (spiralling RG flow) are a truncation artefact and do not invalidate the fixed-point existence, but limit the result to Evidence D/B pending extended truncation.
- Dilaton sourcing (C-072) upgrades the β_{κ²} structure; full 5×5 solver (g², λ̃_S, κ̃², η_A, C_dil) required for Evidence A.

**Condition for Resolution:**  
Extend truncation to include: (a) running η_A ≠ 0; (b) S²F² operator; (c) full momentum-dependent 2-point function Γ^(2)(p²) via Chebyshev projection. See `verification/scripts/solve_momentum_frg.py` (blueprint TKT-20260405).

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
| L8 | Z₂ collapse | κ²=0 in ⟨S⟩=0 phase; Dilaton path adopted | 🟢 Resolved by Architecture Decision |
| L9 | FRG truncation artefact (Dilaton sector) | η_* gap 0.009; complex eigenvalues | 🔴 High (blocks Evidence A for C-072) |

---

## Falsification Triggers

If any of these occur, UIDT requires major revision:

1. **Lattice QCD:** Δ ≠ 1.710 GeV at >3σ
2. **Casimir:** |ΔF/F| < 0.1% at d ≈ 0.66 nm (no anomaly)
3. **DESI:** w = -1.00 ± 0.01 exactly (pure ΛCDM)
4. **LHC:** Scalar excluded in 1.5-1.9 GeV window
5. **Lattice:** No gluon condensate ⟨F²⟩ ≠ 0 consistent with trace anomaly coupling (would invalidate UIDT-C-072 Dilaton path)

See `LEDGER/FALSIFICATION.md` for details.

---

**CITATION:** Rietz, P. (2025/2026). UIDT v3.9.5. DOI: 10.5281/zenodo.17835200
