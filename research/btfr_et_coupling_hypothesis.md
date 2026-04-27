# BTFR / Spacetime Plasticity — ET Coupling Hypothesis

**Status:** Hypothesis  
**Evidence category:** D (prediction, not yet verified)  
**Created:** 2026-04-27  
**Author:** P. Rietz (UIDT Framework)

---

## Hypothesis Statement

The UIDT torsion energy scale ET = 2.44 MeV [C] may be related to the
relaxation timescale tau_relax of the BTFR/Spacetime Plasticity mechanism
(Rhythm 2026) via a dimensional argument:

    tau_relax^{-1} ~ ET / hbar

## Numerical Estimate

Using ET = 2.44 MeV = 3.909e-13 J, hbar = 1.055e-34 J*s:

    tau_relax^{-1} ~ 3.909e-13 / 1.055e-34 ~ 3.71e21 s^{-1}
    tau_relax       ~ 2.7e-22 s

Alternative (ET^2 / hbar*c^2 scaling):

    tau_relax ~ 10^{-28} s  (reheating window for GUT-scale inflation)

The correct dimensional combination must be derived from first principles
in the Spacetime Plasticity framework before any publication claim.

## Falsification Condition

Falsified if the BTFR relaxation timescale computed from Theorem V.3
(Rhythm 2026) is incompatible with the range 10^{-28}--10^{-22} s
at >= 2sigma, or if the covariant extension shifts the timescale
beyond this window by more than two orders of magnitude.

## Required Next Steps

1. Compute tau_relax from the Bernoulli-ODE solution (Theorem V.3)
   for canonical BTFR parameters (v_f, a0, M_b).
2. Identify the correct dimensional combination among
   ET/hbar, ET^2/(hbar*c^2), ET^2/(hbar*c).
3. Promote to Evidence C and create a module only if timescales agree
   within two orders of magnitude.

## Relation to UIDT Ledger

| Parameter | Value    | Evidence | Ledger status         |
|-----------|----------|----------|-----------------------|
| ET        | 2.44 MeV | C        | Immutable -- do not modify |
| tau_relax | TBD      | D        | Not yet in ledger     |

**ET is fixed. tau_relax is the prediction, not the input.**
