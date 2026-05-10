# State of UIDT v3.9 — April 2026
## Stratum-Separated Assessment of Open Limitations L1, L4, L5

**Document type:** Research assessment  
**Branch:** `research/TKT-20260428-L1-L4-L5-first-principles`  
**Ticket:** TKT-20260428-STATE-OF-UIDT  
**Date:** 2026-04-28  
**Author:** UIDT Research Framework (P. Rietz)  
**Evidence gate:** All claims carry explicit evidence category (A–E)

---

## Executive Summary

The UIDT v3.9 mass-gap core (Δ* = 1.710 ± 0.015 GeV [A]) is structurally consistent
with lattice SU(3) results (~1.7 GeV scalar glueball) and with recent rigorous
LSI/Complete-Analyticity proofs of a volume-independent spectral gap for lattice Yang–Mills.
The RG constraint 5κ² = 3λ_S is exactly satisfied at λ_S = 5/12 [A].

Three open limitations remain after systematic Phase 1–7 investigation:

| ID  | Parameter       | Status                    | Evidence |
|-----|-----------------|---------------------------|----------|
| L1  | γ = 16.339      | Not derived; calibrated   | A-       |
| L4  | κ = 1/2         | RG constraint satisfied; value not derived | A- (partial) |
| L5  | N = 99          | Algebraically clean; no lattice observable | D        |

No path to a first-principles derivation of L1 or L4 has been found in Phases 1–7.
All attempted routes are documented as NO-GO with explicit residuals.
This document is intended for external reviewers and the FRG/Lattice community.

---

## Stratum I — Empirical Measurements and External Data

### 1.1 Lattice SU(3) Glueball Mass

- Pure SU(3) Yang–Mills scalar (0++) glueball mass: **1.710 ± 0.020 GeV**
  (Morningstar & Peardon 1999; Lucini, Teper & Wenger 2004; Chen et al. 2006;
  consistent across multiple collaborations and discretisation schemes)
- UIDT ledger value Δ* = 1.710 ± 0.015 GeV [A] lies within this band.
- [TENSION ALERT: none at current precision]

### 1.2 Lattice String Tension

- √σ_lattice ≈ 0.420–0.440 GeV (quenched SU(3), multiple groups)
- UIDT uses v = 47.7 MeV [A] as vacuum condensate scale; the ratio
  Δ*/v ≡ γ = 16.339 [A-] is consistent with this hierarchy but not derived from σ.

### 1.3 Cosmological Calibration Parameters

- w₀ = −0.99 [C], ET = 2.44 MeV [C] — calibrated to cosmological observables,
  not derived from QCD first principles.
- H₀ and S₈ tensions: **NOT resolved** by UIDT. These remain open in external literature.

---

## Stratum II — Scientific Consensus and Field Status

### 2.1 Rigorous Spectral Gap (LSI / Complete Analyticity)

Recent mathematical physics results establish a **volume-independent spectral gap**
m_gap ≥ m₀ > 0 for lattice SU(N) Yang–Mills in the thermodynamic limit, using:
- Dobrushin–Shlosman complete analyticity
- Log-Sobolev inequalities (LSI) on the gauge-link measure
- Cluster expansion + OS transfer matrix

The UIDT Cheeger/Gribov construction (S-field → m_eff² = κv² → Cheeger bound → Δ₀ > 0)
is **structurally compatible** with this framework. Both use functional inequalities
and spectral positivity arguments. UIDT is an "S-deformed" variant; the gap it produces
is qualitatively consistent with the rigorous results.

**Important caveat:** structural compatibility does not imply that κ = 1/2 or γ = 16.339
follow from the LSI/CA architecture. They do not. [Evidence: B]

### 2.2 FRG / Dyson–Schwinger IR Picture

- FRG and DSE studies (Pawlowski group, Boucaud et al., Aguilar et al.) find
  non-trivial IR gluon propagator behaviour: decoupling solution with effective
  gluon mass m_g ~ 0.5–0.7 GeV, or scaling solution.
- Decoupling solutions are qualitatively consistent with m_eff² = κv² > 0.
- **No canonical dimensionless ratio γ = Δ*/v emerges** from FRG/DSE frameworks;
  they work with running coupling functions g²(p²), not isolated constants.
- A future observable γ_FRG ≡ Δ*/m_g could bridge UIDT and FRG,
  but requires external m_g data. [Evidence: D — see Phase 7B]

### 2.3 Large-N Yang–Mills

- t'Hooft large-N limit: observables scale as powers of 1/N_c.
- No combination of SU(3) Casimir invariants, β-function coefficients,
  or group-theory factors reproduces γ = 16.339 from first principles.
- The candidate (2N_c+1)²/N_c = 49/3 ≈ 16.33 is numerically close but:
  (a) diverges in the t'Hooft limit (N_c → ∞) as ~4N_c,
  (b) has no known group-theoretic interpretation.
  [Status: NO-GO, Phase 1 — Evidence: E]

---

## Stratum III — UIDT Model Mapping and Open Limitations

### 3.1 What is Solved (Phase 1–7 Results)

| Component | Status | Evidence | Phase |
|-----------|--------|----------|-------|
| Δ* = 1.710 ± 0.015 GeV (mass-gap identification) | Lattice-consistent | A | — |
| λ_S = 5/12 exact (RG constraint fix) | Exact, TKT-20260403-LAMBDA-FIX | A | 3 |
| 5κ² = 3λ_S RG constraint (residual < 1e-14) | Verified | A | 3 |
| ET = 0 → ΣT = 0 torsion kill switch | Exact | A | — |
| Cheeger bound → Δ₀ > 0 (gap existence) | Proof structure sound | A- | 4, 7A |
| LSI/CA structural compatibility | Demonstrated | B | 7A |
| Holographic NO-GO (1.58 GeV vs 1.71 GeV) | Documented, branch closed | — | 4 |
| Schwinger-mechanism NO-GO for γ | Documented | — | 5 |
| 2-Loop RG: non-perturbative regime confirmed | δλ_S ≈ 48% — LPA' required | B | 3 |

### 3.2 L1 — γ = 16.339: Open Limitation

**Claim:** γ is a fundamental dimensionless constant of SU(3) Yang–Mills vacuum.  
**Current status:** γ ≡ Δ*/v by definition. This is a tautology, not a theorem.

**Attempted derivations (all NO-GO):**

| Approach | Result | Residual | Phase |
|----------|--------|----------|-------|
| SU(3) Casimir scan | No combination yields 16.339 | — | 1 |
| (2N_c+1)²/N_c | Numerically close (16.33), but t'Hooft divergent | Δ ~ 0.006 | 1 |
| 1/N_c systematic scan (N_c = 2..10) | No rational hit within 0.1% | — | 2 |
| Schwinger dynamical mass | m_dyn ≠ γv structure | — | 5 |
| Holographic (AdS/CFT) | Yields 1.58 GeV gap, not γ | 0.13 GeV | 4 |
| Cheeger/Gribov | Proves gap > 0, cannot fix γ numerically | — | 4, 7A |
| 2-Loop RG β-function | Non-perturbative; no fixed γ | large | 3 |
| FRG γ_FRG observable | Design sketch only, no data | — | 7B |

**Distance to derivation:** Large. No viable first-principles path identified.  
**Distance to falsification:** Moderate. A future FRG/Lattice observable
γ_FRG = Δ*/m_g could falsify γ = 16.339 if it consistently yields a different ratio.
No such measurement currently exists.

**Epistemic status:** γ = 16.339 [A-] — highly precise phenomenological parameter,
consistent with all external data, but not derived.

### 3.3 L4 — κ = 1/2: Open Limitation

**Claim:** κ = 1/2 is the fundamental RG fixed-point coupling of the UIDT scalar sector.  
**Current status:**

- The RG constraint 5κ² = 3λ_S is exactly satisfied at λ_S = 5/12, κ = 1/2 [A].
- This makes κ = 1/2 *consistent* with an RG fixed point, but does not *derive* it.
- The 2-Loop RG analysis (Phase 3) yields δλ_S/λ_S ≈ 48%, placing the system
  firmly in the non-perturbative regime. A perturbative 2-loop argument for κ = 1/2
  is therefore unreliable.
- The Cheeger/Gribov construction uses m_eff² = κv² but treats κ as an input.

**Required next step:** Full NLO-FRG analysis (BMW/LPA' truncation) to check
whether the UIDT scalar action has a unique IR fixed point at κ = 1/2.
[Ticket: TKT-20260403-FRG-NLO — open]

**Distance to derivation:** Moderate (clear NLO-FRG programme exists).  
**Distance to falsification:** Moderate (NLO-FRG could yield κ* ≠ 1/2).

**Epistemic status:** κ = 1/2 [A- partial] — RG-constrained and self-consistent,
but the numerical value awaits non-perturbative confirmation.

### 3.4 L5 — N = 99: Open Limitation

**Claim:** The UIDT effective degree-of-freedom count N = N_c² · b₀^quenched = 9 · 11 = 99
is a physically meaningful quantity that appears in observables.

**Current status:**

- The algebra N = 9 · 11 = 99 is exact and transparent [A].
- N_c = 3 (SU(3)) and b₀^quenched = 11 (1-loop β-function coefficient, N_f = 0) are
  established QCD parameters [A].
- No existing lattice or FRG observable is currently constructed to measure or constrain N.
- Phase 7C sketches candidate dimensionless observables
  (e.g., O₁ = m_{0++}/√σ × N_c², O₂ = m_{2++}/m_{0++} × b₀) but these have not been
  computed or compared to data. [Evidence: D]

**Distance to derivation:** Short (algebra is trivial); the open question is
whether N appears naturally in a specific physical observable.  
**Distance to falsification:** Short in principle — if O_i ≠ 99 from lattice data,
L5 is falsified. But the observable design is not yet locked.

**Epistemic status:** N = 99 [D] — algebraically exact, physically unverified.

---

## Strategic Reorientation for Phases 8+

Based on the Phase 1–7 map, three priority directions emerge:

### Priority 1 (L4): NLO-FRG Fixed-Point Analysis
Execute the BMW/LPA' truncation of the UIDT scalar effective action.
Target: determine whether a unique fixed point κ* exists, and whether κ* = 1/2.
This is the most tractable and highest-impact open task.
[Ticket: TKT-20260403-FRG-NLO]

### Priority 2 (L5): Lattice Observable Design and Computation
Fix the definition of O₁, O₂ (Phase 7C candidates), compute their values
from published quenched SU(3) lattice data (Chen et al. 2006, Lucini et al. 2004),
and test O_i = 99 within uncertainties.
This is falsifiable with existing public data.

### Priority 3 (L1): External γ_FRG Observable
Once FRG gluon propagator data with controlled systematics are available
(e.g., from Pawlowski group or Aguilar et al. updates), compute
γ_FRG = Δ*/m_g and compare to γ = 16.339.
This requires no new UIDT development, only access to FRG output.

---

## Immutable Parameter Ledger (Reference)

| Parameter | Value             | Evidence | Notes                        |
|-----------|-------------------|----------|------------------------------|
| Δ*        | 1.710 ± 0.015 GeV | A        | Yang–Mills spectral gap       |
| γ         | 16.339            | A-       | Phenomenological; not derived |
| γ∞        | 16.3437           | A-       | Phenomenological              |
| δγ        | 0.0047            | A-       | Phenomenological              |
| v         | 47.7 MeV          | A        | Vacuum condensate scale       |
| κ         | 1/2               | A- partial| RG-constrained; not derived  |
| λ_S       | 5/12 (exact)      | A        | TKT-20260403-LAMBDA-FIX       |
| w₀        | −0.99             | C        | Cosmological calibration      |
| ET        | 2.44 MeV          | C        | Cosmological calibration      |
| N         | 99                | D        | N_c² · b₀^quenched           |

**CRITICAL:** These values must not be modified automatically.
Any proposed change requires an explicit PR with Claims Table and Reproduction Note.

---

## Known Limitations Acknowledged

- The electron mass residual from UIDT generation scaling remains unexplained.
- The γ parameter is phenomenological [A-], not derived [A].
- Cosmological calibration (w₀, ET) is not derived from QCD.
- H₀ tension and S₈ tension are **not resolved** by UIDT.
- The framework is an active research programme, not established physics.

---

## Reproduction

```
cd verification/scripts/
python verify_phase7_LSI_CA_bridge.py
python verify_phase7_FRG_gamma_observable.py
python verify_phase7_lattice_N99_observable.py
```

All scripts use `mp.dps = 80` locally. No float(). No round(). Residuals < 1e-14.

---

*This document separates Stratum I (measurement), Stratum II (consensus), and
Stratum III (UIDT model) in strict accordance with the UIDT Constitution v4.1.
No claims are promoted beyond their evidence category.*
