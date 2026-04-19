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

### L6-FRG: FRG Derivation of γ — Minimal Truncation (S F² Sector)
**Status:** 🔬 ACTIVE RESEARCH — linked to GAP-FRG-001

**Description:**  
The FRG analysis of Claim UIDT-C-070 (eta_* ≈ 0.072, Evidence D) is based on a minimal
truncation with the following deliberate methodological compromises:

- **η_A = 0:** Gluon anomalous dimension set to zero (background-field approximation).
  Gluon fluctuations in the anomalous dimension scheme are not fully captured.
- **Massless scalar:** The scalar S is treated as massless (w_S → 0 limit).
- **4×4 truncation only:** The coupling space is {g², λ_S, κ², κ²} without higher operators.
- **LPA (Local Potential Approximation):** No momentum-dependent vertex projection (∂_p²).
  The beta-functions are evaluated at p² = 0 only.
- **Litim regulator in conformal window:** The threshold functions are evaluated in the
  w → 0 limit, suppressing IR mass effects.

**Impact on current results:**  
- The anomalous dimension η_* ≈ 0.072 is a truncation-dependent result (Evidence D).
- Complex eigenvalues (±0.654i) of the stability matrix indicate a spiralling RG flow
  in the IR — classified as a truncation artefact from missing higher operators (S²F²).
- The gap Δη ≈ 0.009 between η_* and the phenomenological threshold ≈ 0.063 is
  consistent with the expected effect of missing gluon fluctuations.

**What this limitation does NOT affect:**  
- The canonical value γ = 16.339 (Evidence A-) is independent of this truncation.
  It is a kinematic calibration, not derived from the FRG run.
- The Yang-Mills spectral gap Δ* = 1.710 ± 0.015 GeV (Evidence A) is not affected.

**Condition for Resolution:**  
See clay-submission/GAP_ANALYSIS_CLAY.md → GAP-FRG-001 for the full solution path.
Resolution requires a momentum-dependent vertex projection (∂_p²) and a
self-consistent Dyson resummation in the full (S, A) propagator matrix.

---

### L8: UV Hierarchy Gap — Pure γ⁻¹² Model
**Status:** ⚠️ DOCUMENTED GAP [Evidence E — Research Mode]

**Description:**
The pure γ⁻¹² suppression model (without the 99-step
RG cascade) shows a significant discrepancy relative
to the empirical cosmological constant:

- ρ_DE = (1/π²)·Δ⁴·γ⁻¹² = 2.393×10⁻¹⁵ GeV⁴ [E]
- ρ_vac (empirical, Planck 2018) ≈ 4.33×10⁻⁴⁷ GeV⁴ [C]
- Ratio: ρ_DE / ρ_vac ≈ 5.53×10³¹ [E]

UV Hierarchy test (Planck scale):
- Λ_UV⁴·γ⁻¹² ≈ 6.12×10⁶¹ GeV⁴ [E]
- Residual divergence factor: ~1.41×10¹⁰⁸ [E]

γ sensitivity (δγ = 0.0047, canonical):
- Relative ρ_DE variation: 0.345% [A-]

**Impact:**
- γ⁻¹² alone is NOT sufficient to resolve the
  cosmological constant problem
- The 99-step RG cascade (L5) is load-bearing for
  cosmological calibration — removing it exposes
  a ~31 OOM gap
- The perturbation test (ε = 10⁻²⁰ GeV) confirms
  γ⁻¹² independence: δρ/ρ₀ = 4ε/Δ (γ cancels)

**Relationship to L3 and L5:**
L3 documents the residual factor ~2.3 WITH the
full 99-step RG cascade. L8 documents the gap
WITHOUT the cascade. Both are valid statements
about different model configurations.
L5 (N=99 unjustified) is the mechanistic root cause
of this limitation.

**Condition for Resolution:**
First-principles derivation of the RG cascade
depth N=99 from the Yang-Mills spectrum (→ L5).
Until L5 is resolved, cosmological calibration
remains at maximum Evidence [C].

**[TENSION ALERT]:** ρ_DE(pure γ⁻¹²) vs. ρ_vac:
Gap = 31 orders of magnitude [E vs. C].

---

## Resolved Limitations (Historical)

### L6: Spectral Gap vs. Particle Mass [RESOLVED — superseded by L6-FRG above]
**Status:** ✅ CLARIFIED (2025-12-25)

**Previous Issue:**  
Δ = 1.710 GeV was sometimes conflated with glueball mass.

**Resolution (2025-12-25):**  
Δ is the SPECTRAL GAP of Yang-Mills Hamiltonian, NOT a particle mass.
Glueball identification explicitly WITHDRAWN [E].

*Note: The label L6 has been reused for L6-FRG (active, 2026-04-06).
This historical entry is preserved for audit continuity.*

---

### L7: VEV Value [RESOLVED]
**Status:** ✅ CORRECTED

**Previous Issue:**  
v = 0.854 MeV in Framework v3.2

**Resolution (v3.6.1):**  
Corrected to v = 47.7 MeV. Old value was erroneous.

---

## Limitation Impact Matrix

| ID      | Limitation                          | Impact on Claims              | Priority    |
|---------|--------------------------------------|-------------------------------|-------------|
| L1      | 10¹⁰ factor                         | λ_UIDT [C→D if unresolved]    | 🔴 High     |
| L2      | Electron mass                        | m_e formula approximate       | 🟡 Medium   |
| L3      | Vacuum energy                        | ρ_vac factor 2.3              | 🟢 Accepted |
| L4      | γ not from RG                        | γ remains [A-] not [A]        | 🔴 High     |
| L5      | N=99 unjustified                     | RG cascade phenomenological   | 🟡 Medium   |
| L6-FRG  | FRG minimal truncation (C-070)       | η_* Evidence D, not upgradable| 🔴 High     |
| L8      | UV Hierarchy Gap (pure γ⁻¹²)         | ρ_DE/ρ_vac = 5.53×10³¹ [E]    | 🔴 High     |

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
