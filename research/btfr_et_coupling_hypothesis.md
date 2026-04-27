# BTFR / Spacetime Plasticity — ET Coupling Hypothesis

**Status:** Hypothesis  
**Evidence category:** D (prediction, not yet verified)  
**Created:** 2026-04-27  
**Author:** P. Rietz (UIDT Framework)

---

## Hypothesis Statement

The UIDT torsion energy scale ET = 2.44 MeV [C] may be related to the
relaxation timescale τ_relax of the BTFR/Spacetime Plasticity mechanism
(Rhythm 2026, file 64656994) via a dimensional argument:

    τ_relax⁻¹ ~ ET² / ħ

## Numerical Estimate

Using ET = 2.44 MeV = 2.44 × 10⁶ eV:

    ET² = (2.44 × 10⁶ × 1.602 × 10⁻¹⁹ J)²
        ≈ (3.909 × 10⁻¹³ J)²
        ≈ 1.528 × 10⁻²⁵ J²

    ħ = 1.055 × 10⁻³⁴ J·s

    τ_relax⁻¹ ~ 1.528 × 10⁻²⁵ / 1.055 × 10⁻³⁴
              ≈ 1.45 × 10⁹ s⁻¹   [non-relativistic dimensional estimate]

**Note:** The more natural relativistic estimate uses ET²/(ħc) or ET/ħ
directly.  Using ET/ħ:

    ET = 2.44 MeV = 3.909 × 10⁻¹³ J
    τ_relax⁻¹ ~ ET / ħ ≈ 3.909 × 10⁻¹³ / 1.055 × 10⁻³⁴
              ≈ 3.71 × 10²¹ s⁻¹
    τ_relax   ≈ 2.7 × 10⁻²² s

This timescale is sub-nuclear (τ ~ 10⁻²² s), which is well above the
reheating window (τ_reheating ~ 10⁻³⁵–10⁻²⁸ s for GUT-scale inflation).
The original estimate τ ~ 10⁻²⁸ s quoted in the roadmap corresponds to
the ET²/(ħc²) scaling in natural units — this must be verified carefully
before any publication claim.

## Falsification Condition

The hypothesis is falsified if:
1. The BTFR relaxation timescale τ_relax, when computed from first principles
   in the Spacetime Plasticity framework, is incompatible with the range
   10⁻²⁸–10⁻²² s at the ≥ 2σ level.
2. The dimensional argument above does not survive covariant extension
   (i.e., the correct relativistic combination of ET produces a timescale
   outside the reheating window by more than two orders of magnitude).

## Required Next Steps

1. Compute τ_relax from the Bernoulli-ODE solution in Rhythm 2026 (Theorem V.3)
   for the canonical BTFR parameter set (v_f, a₀, M_b).
2. Compare with ET/ħ, ET²/(ħc²), and ET²/(ħc) to identify the correct
   dimensional combination.
3. Only if the timescales agree within two orders of magnitude should this
   hypothesis be promoted to Evidence C and a module created.

## Relation to UIDT Ledger

| Parameter | Value | Evidence | Ledger status |
|-----------|-------|----------|---------------|
| ET        | 2.44 MeV | C    | Immutable — do not modify |
| τ_relax   | TBD       | D    | Not yet in ledger |

**The ET ledger value must not be adjusted to match τ_relax.**  If the
coupling hypothesis holds, it is τ_relax that is predicted; ET is fixed.
