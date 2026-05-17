#!/usr/bin/env python3
"""
UIDT v3.9 — Session-2 Phase-8 ledger-sync verification.

Purpose
-------
Verify the arithmetic used by the Session-2 / Phase-8 constants and
ledger staging addendum. This script is intentionally narrow: it checks
only the corrected formula, the canonical E_T threshold value, the
S4-P1 numerical chain, and the exact RG constraint.

Evidence policy
---------------
- gamma = 16.339 remains [A-].
- gamma_bare = 49/3 remains [D] Stratum III.
- gamma_pred remains [D] Stratum III.
- No evidence-category promotion is performed by this script.

Numerical policy
----------------
All comparisons involving decimal ledger inputs and rational reconstructions
use explicit residual checks. Exact mp.mpf equality is reserved only for
constructs that are expected to close exactly through the same construction
path. This avoids brittle decimal/rational equality failures while preserving
UIDT's <1e-14 residual discipline.

Reproduction
------------
python verification/scripts/verify_session2_phase8_sync.py
"""

from __future__ import annotations

import mpmath as mp


def _assert_residual(
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
    print(f"[PASS] {label} residual:", mp.nstr(residual, 80))
    return residual


def main() -> None:
    mp.dps = 80

    tight_tolerance = mp.mpf("1e-70")
    proof_tolerance = mp.mpf("1e-14")

    nc = mp.mpf(3)
    gamma_ledger = mp.mpf("16.339")
    delta_star_mev = mp.mpf("1710")
    e_t_mev = mp.mpf("2.44")
    kappa = mp.mpf(1) / mp.mpf(2)
    lambda_s = mp.mpf(5) / mp.mpf(12)

    gamma_bare = (2 * nc + 1) ** 2 / nc
    gamma_wrong_denominator = (2 * nc + 1) ** 2 / (nc**2)
    delta_gamma_required = gamma_ledger - gamma_bare

    k_crit_mev = 4 * mp.pi * e_t_mev
    v_s4p1_mev = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_crit_mev
    delta_gamma_np = (nc**2 - 1) / (4 * mp.pi**2) * (v_s4p1_mev / delta_star_mev)
    gamma_pred = gamma_bare + delta_gamma_np
    gamma_pred_residual = abs(gamma_pred - gamma_ledger)

    rg_residual = abs(5 * kappa**2 - 3 * lambda_s)

    _assert_residual(
        "gamma_bare formula corrected",
        gamma_bare,
        mp.mpf(49) / mp.mpf(3),
        tight_tolerance,
    )
    print("[INFO] gamma_bare:", mp.nstr(gamma_bare, 80))

    _assert_residual(
        "wrong denominator rejected as 49/9",
        gamma_wrong_denominator,
        mp.mpf(49) / mp.mpf(9),
        tight_tolerance,
    )
    assert gamma_wrong_denominator != gamma_bare
    print("[INFO] rejected wrong denominator:", mp.nstr(gamma_wrong_denominator, 80))

    expected_delta_gamma_required = mp.mpf(17) / mp.mpf(3000)
    _assert_residual(
        "Delta_gamma_required = 17/3000",
        delta_gamma_required,
        expected_delta_gamma_required,
        tight_tolerance,
    )
    assert delta_gamma_required > 0
    print("[INFO] Delta_gamma_required:", mp.nstr(delta_gamma_required, 80))

    expected_kcrit = mp.mpf(
        "30.6619442990363820073953994208079481497643733379010328127154592209242881253534"
    )
    _assert_residual(
        "k_crit = 4*pi*E_T for E_T=2.44 MeV",
        k_crit_mev,
        expected_kcrit,
        tight_tolerance,
    )
    print("[INFO] k_crit:", mp.nstr(k_crit_mev, 80), "MeV")

    expected_gamma_pred = mp.mpf(
        "16.338962439648224784189299741156296927101016473597870996977246409594812352084401"
    )
    _assert_residual(
        "gamma_pred chain",
        gamma_pred,
        expected_gamma_pred,
        tight_tolerance,
    )
    print("[INFO] gamma_pred:", mp.nstr(gamma_pred, 80))
    print("[INFO] |gamma_pred - gamma_ledger|:", mp.nstr(gamma_pred_residual, 80))

    assert rg_residual < proof_tolerance, mp.nstr(rg_residual, 80)
    print("[PASS] RG constraint residual:", mp.nstr(rg_residual, 80))

    print("ALL SESSION-2 PHASE-8 SYNC CHECKS PASSED")


if __name__ == "__main__":
    main()
