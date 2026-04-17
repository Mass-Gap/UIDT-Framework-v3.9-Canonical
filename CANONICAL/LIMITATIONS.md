# UIDT Known Limitations v3.7.2

> **PURPOSE:** Transparent documentation of unresolved issues  
> **PRINCIPLE:** Acknowledge what we don't know

---

## Active Limitations (Unresolved)

### L1: Geometric Scale Factor (Ill-Defined)
**Status:** 🔬 HIGHEST PRIORITY — PROBLEM STATEMENT REQUIRES CLARIFICATION

**Description:**  
Previous versions stated "a factor of ~10¹⁰" without specifying reference scales.
mpmath 80-dps analysis (TKT-20260416-L1L4L5-analysis.md) reveals:

  λ_UIDT / r_conf = 0.660 nm / 0.197 fm = 3.35 × 10⁶ ≈ 10^6.5 (NOT 10¹⁰)

The actual ratio depends on which UV/IR scales are compared. No energy ratio
in the Standard Model yields exactly 10¹⁰. Closest approach: λ_UIDT/r_conf ≈ α⁻³ × 1.302.

**Impact:**  
- λ_UIDT calibrated [C] instead of derived [A]
- The problem is real but was previously ill-defined

**Condition for Resolution:**  
1. Precisely define which UV and IR scales are compared
2. Derive the geometric factor from first principles (topology, holography, or α⁻³ connection)

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

### L7: Gribov Horizon Crossing
**Status:** 🔬 ACTIVE RESEARCH [GRIBOV_HORIZON_CROSSING]

**Description:**  
Der analytische Fixpunkt des projizierten 2x2-Systems erzwingt \(\tilde{\kappa}^{2*} = \pi^2 \approx 9.87\). Dieser Wert liegt tief im Infraroten, jenseits des klassischen Gribov-Pols (\(\tilde{\kappa}^2 = 1.0\)). Der Vorhersagewert für \(\tilde{\lambda}_{SF}^* \approx 16.449\) ist streng auf Evidenz D limitiert, bis das System um einen dynamischen, selbstkonsistenten Gribov-Zwanziger-Limes erweitert wird.

---

### L8: X³ Mixing Omitted
**Status:** 🔬 ACTIVE RESEARCH [X3_MIXING_OMITTED]

**Description:**  
Die Rückkopplung des Tripel-Gluon-Operators (X³-Einmischung) aus dem SMEFT-Sektor (\(+ \frac{1}{2} g_3^2 C_A C_G\)) wurde in der aktuellen Truncation vernachlässigt.

---

### L9: Z₂ Symmetry Collapse
**Status:** 🔬 ACTIVE RESEARCH [Z2_SYMMETRY_COLLAPSE]

**Description:**  
Das minimale Skalar-Gauge-System kollabiert ohne explizite Symmetriebrechung deterministisch. Die Theorie stützt sich axiomatisch darauf, dass \(S\) an die Spuranomalie (Trace Anomaly) koppelt, um diesen Kollaps abzuwenden (siehe UIDT-C-072).

---

## Resolved Limitations (Historical)

### L6-FRG: Truncation Artifact - Spiral RG Flow [RESOLVED]
**Status:** ✅ CLOSED (v3.9.6)

**Previous Issue:**  
Spiralförmiger RG-Fluss im Infraroten durch fehlende Symmetrie-Relationen z.B. komplexe Eigenwerte an Fixpunkten.

**Resolution:**  
Das Artefakt wurde durch exakte RG-Constraint-Projektion (\(5\kappa^2 = 3\lambda_{SF}\)) im 80-dps-Solver eliminiert. Die Stabilitätsmatrix ist nun beweisbar rein reell.

---

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
| L1      | Geometric scale (~10^6.5, ill-defined)| λ_UIDT [C→D if unresolved]    | 🔴 High     |
| L2      | Electron mass                        | m_e formula approximate       | 🟡 Medium   |
| L3      | Vacuum energy                        | ρ_vac factor 2.3              | 🟢 Accepted |
| L4      | γ not from RG                        | γ remains [A-] not [A]        | 🔴 High     |
| L5      | N=99 unjustified                     | RG cascade phenomenological   | 🟡 Medium   |
| L7      | Gribov Horizon Crossing              | λ_SF* strictly Evidence D     | 🔴 High     |
| L8      | X³ Mixing Omitted                    | Impacts truncation stability  | 🟡 Medium   |
| L9      | Z₂ Symmetry Collapse                 | Axiomatic Trace Anomaly req.  | 🔴 High     |

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
