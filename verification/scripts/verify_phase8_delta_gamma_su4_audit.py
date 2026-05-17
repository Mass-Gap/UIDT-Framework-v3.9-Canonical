#!/usr/bin/env python3
"""
UIDT v3.9 — Phase 8 delta-gamma and SU(4) audit.

Scope
-----
This script executes the first concrete Phase-8 research pass after PR #459.
It uses the corrected assumptions:

1. gamma_bare(Nc) = (2*Nc + 1)^2 / Nc
2. gamma_bare(3) = 49/3
3. k_crit = 4*pi*E_T = 30.661944... MeV for E_T = 2.44 MeV
4. gamma = 16.339 remains [A-]

It does not claim a first-principles proof. It records four outcomes:

- P1a: the required correction Delta_gamma_required = 17/3000.
- P1b: the perturbative one-loop coefficient that would be required if
       Delta_gamma = C * alpha_s/(4*pi) with alpha_s(1.5 GeV)=0.326.
- P1c: the corrected S4-P1 non-perturbative shift and its residual.
- P5:  the SU(4) gamma_bare cross-check and the N_SU4 definition tension.

Evidence policy
---------------
- [A] only for exact arithmetic constraints, including RG residual = 0.
- [D] for UIDT conjectural mappings and predictions.
- [E] / TENSION for the SU(4) N-definition conflict.

Numerical policy
----------------
All comparisons involving decimal ledger inputs and rational reconstructions
use explicit residual checks. Exact mp.mpf equality is reserved only for
constructs that are expected to close exactly through the same construction
path. This avoids brittle decimal/rational equality failures while preserving
UIDT's <1e-14 residual discipline.

Reproduction
------------
python verification/scripts/verify_phase8_delta_gamma_su4_audit.py
"""

from __future__ import annotations

import mpmath as mp


def nstr(value: mp.mpf) -> str:
    """Return full high-precision text for audit output."""
    return mp.nstr(value, 80)


def assert_residual(
    label: str,
    value: mp.mpf,
    expected: mp.mpf,
    tolerance: mp.mpf,
) -> mp.mpf:
    """Fail fast unless |value - expected| is below tolerance."""
    residual = abs(value - expected)
    assert residual < tolerance, (
        f"{label} residual {mp.nstr(residual, 80)} exceeds "
        f"tolerance {mp.nstr(tolerance, 20)}"
    )
    print(f"[PASS] {label} residual:", nstr(residual))
    return residual


def main() -> None:
    mp.dps = 80

    tight_tolerance = mp.mpf("1e-70")
    proof_tolerance = mp.mpf("1e-14")

    gamma_ledger = mp.mpf("16.339")
    delta_star_mev = mp.mpf("1710")
    e_t_mev = mp.mpf("2.44")
    alpha_s_ref = mp.mpf("0.326")
    kappa = mp.mpf(1) / mp.mpf(2)
    lambda_s = mp.mpf(5) / mp.mpf(12)

    nc3 = mp.mpf(3)
    nc4 = mp.mpf(4)

    # P1a — Corrected SU(3) bare-gamma conjecture.
    gamma_bare_su3 = (2 * nc3 + 1) ** 2 / nc3
    wrong_gamma_bare_su3 = (2 * nc3 + 1) ** 2 / (nc3**2)
    delta_gamma_required = gamma_ledger - gamma_bare_su3

    assert_residual(
        "gamma_bare_SU3 = 49/3",
        gamma_bare_su3,
        mp.mpf(49) / mp.mpf(3),
        tight_tolerance,
    )
    assert_residual(
        "rejected_wrong_denominator_SU3 = 49/9",
        wrong_gamma_bare_su3,
        mp.mpf(49) / mp.mpf(9),
        tight_tolerance,
    )
    assert gamma_bare_su3 != wrong_gamma_bare_su3

    expected_delta_gamma_required = mp.mpf(17) / mp.mpf(3000)
    assert_residual(
        "Delta_gamma_required = 17/3000",
        delta_gamma_required,
        expected_delta_gamma_required,
        tight_tolerance,
    )
    assert delta_gamma_required > 0

    print("[P1a] gamma_bare_SU3:", nstr(gamma_bare_su3))
    print("[P1a] rejected_wrong_denominator_SU3:", nstr(wrong_gamma_bare_su3))
    print("[P1a] Delta_gamma_required:", nstr(delta_gamma_required))

    # P1b — Required one-loop coefficient under a minimal alpha_s/(4*pi) ansatz.
    # This is not a derivation. It is a scale audit for the missing diagrammatic coefficient.
    required_c_alpha_over_4pi = delta_gamma_required * 4 * mp.pi / alpha_s_ref
    required_c_alpha_over_pi = delta_gamma_required * mp.pi / alpha_s_ref
    required_c_alpha_over_16pi2 = delta_gamma_required * 16 * mp.pi**2 / alpha_s_ref

    assert required_c_alpha_over_4pi > 0
    assert required_c_alpha_over_4pi < 1

    print("[P1b] alpha_s_ref:", nstr(alpha_s_ref))
    print("[P1b] C_required if Delta_gamma = C*alpha_s/(4*pi):", nstr(required_c_alpha_over_4pi))
    print("[P1b] C_required if Delta_gamma = C*alpha_s/pi:", nstr(required_c_alpha_over_pi))
    print("[P1b] C_required if Delta_gamma = C*alpha_s/(16*pi^2):", nstr(required_c_alpha_over_16pi2))
    print("[P1b] STATUS: SCALE-CONSISTENT BUT NOT DERIVED [D]")

    # P1c — Corrected S4-P1 chain using canonical E_T.
    k_crit_mev = 4 * mp.pi * e_t_mev
    v_s4p1_mev = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_crit_mev
    delta_gamma_np = (nc3**2 - 1) / (4 * mp.pi**2) * (v_s4p1_mev / delta_star_mev)
    gamma_pred = gamma_bare_su3 + delta_gamma_np
    residual_to_gamma = abs(gamma_pred - gamma_ledger)
    residual_to_delta_required = abs(delta_gamma_np - delta_gamma_required)
    ratio_delta_np_to_required = delta_gamma_np / delta_gamma_required

    expected_kcrit = mp.mpf(
        "30.6619442990363820073953994208079481497643733379010328127154592209242881253534"
    )
    expected_gamma_pred = mp.mpf(
        "16.338962439648224784189299741156296927101016473597870996977246409594812352084401"
    )

    assert k_crit_mev > 0
    assert v_s4p1_mev > 0
    assert delta_gamma_np > 0
    assert residual_to_gamma > proof_tolerance
    assert residual_to_gamma < mp.mpf("1e-3")

    assert_residual(
        "k_crit = 4*pi*E_T for E_T=2.44 MeV",
        k_crit_mev,
        expected_kcrit,
        tight_tolerance,
    )
    assert_residual(
        "gamma_pred chain",
        gamma_pred,
        expected_gamma_pred,
        tight_tolerance,
    )

    print("[P1c] k_crit_mev:", nstr(k_crit_mev))
    print("[P1c] v_S4P1_mev:", nstr(v_s4p1_mev))
    print("[P1c] Delta_gamma_NP:", nstr(delta_gamma_np))
    print("[P1c] gamma_pred:", nstr(gamma_pred))
    print("[P1c] residual_to_gamma:", nstr(residual_to_gamma))
    print("[P1c] residual_to_Delta_gamma_required:", nstr(residual_to_delta_required))
    print("[P1c] ratio_Delta_gamma_NP_to_required:", nstr(ratio_delta_np_to_required))
    print("[P1c] STATUS: PARTIAL NUMERICAL HIT [D], NOT [A]")

    # P5 — SU(4) cross-check.
    gamma_bare_su4 = (2 * nc4 + 1) ** 2 / nc4
    assert_residual(
        "gamma_bare_SU4 = 81/4",
        gamma_bare_su4,
        mp.mpf(81) / mp.mpf(4),
        tight_tolerance,
    )

    # N definition tension:
    # Handover-style constant-b0 rule: N = Nc^2 * 11.
    # Pure-YM one-loop beta coefficient: b0(Nc) = 11*Nc/3, giving N = Nc^2*b0(Nc).
    n_su4_constant_b0_11 = nc4**2 * mp.mpf(11)
    b0_su4_pure_ym = mp.mpf(11) * nc4 / mp.mpf(3)
    n_su4_pure_ym_b0 = nc4**2 * b0_su4_pure_ym
    n_su4_difference = n_su4_pure_ym_b0 - n_su4_constant_b0_11
    n_su4_relative_difference = n_su4_difference / n_su4_constant_b0_11

    assert_residual(
        "N_SU4 constant-b0 convention = 176",
        n_su4_constant_b0_11,
        mp.mpf(176),
        tight_tolerance,
    )
    assert_residual(
        "N_SU4 pure-YM b0 convention = 704/3",
        n_su4_pure_ym_b0,
        mp.mpf(704) / mp.mpf(3),
        tight_tolerance,
    )
    assert_residual(
        "N_SU4 relative difference = 1/3",
        n_su4_relative_difference,
        mp.mpf(1) / mp.mpf(3),
        tight_tolerance,
    )
    assert n_su4_difference > 0

    print("[P5] gamma_bare_SU4:", nstr(gamma_bare_su4))
    print("[P5] N_SU4_constant_b0_11:", nstr(n_su4_constant_b0_11))
    print("[P5] b0_SU4_pure_YM:", nstr(b0_su4_pure_ym))
    print("[P5] N_SU4_pure_YM_b0:", nstr(n_su4_pure_ym_b0))
    print("[P5] N_SU4_definition_difference:", nstr(n_su4_difference))
    print("[P5] N_SU4_relative_difference:", nstr(n_su4_relative_difference))
    print("[P5] STATUS: [TENSION ALERT] N_SU4 definition conflict")

    # [A] invariant check retained.
    rg_residual = abs(5 * kappa**2 - 3 * lambda_s)
    assert rg_residual < proof_tolerance, nstr(rg_residual)
    print("[A] RG_CONSTRAINT residual:", nstr(rg_residual))

    print("ALL PHASE-8 DELTA-GAMMA / SU4 AUDIT CHECKS PASSED")


if __name__ == "__main__":
    main()
