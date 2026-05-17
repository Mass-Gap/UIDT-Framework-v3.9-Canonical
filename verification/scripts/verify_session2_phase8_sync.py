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

Reproduction
------------
python verification/scripts/verify_session2_phase8_sync.py
"""

from __future__ import annotations

import mpmath as mp


def main() -> None:
    mp.dps = 80

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

    assert gamma_bare == mp.mpf(49) / mp.mpf(3), mp.nstr(gamma_bare, 80)
    print("[PASS] gamma_bare formula corrected:", mp.nstr(gamma_bare, 80))

    assert gamma_wrong_denominator == mp.mpf(49) / mp.mpf(9), mp.nstr(
        gamma_wrong_denominator, 80
    )
    assert gamma_wrong_denominator != gamma_bare
    print("[PASS] rejected wrong denominator:", mp.nstr(gamma_wrong_denominator, 80))

    assert delta_gamma_required == mp.mpf(17) / mp.mpf(3000), mp.nstr(
        delta_gamma_required, 80
    )
    assert delta_gamma_required > 0
    print("[PASS] Delta_gamma_required:", mp.nstr(delta_gamma_required, 80))

    expected_kcrit = mp.mpf(
        "30.6619442990363820073953994208079481497643733379010328127154592209242881253534"
    )
    assert abs(k_crit_mev - expected_kcrit) < mp.mpf("1e-78"), mp.nstr(
        abs(k_crit_mev - expected_kcrit), 80
    )
    print("[PASS] k_crit = 4*pi*E_T:", mp.nstr(k_crit_mev, 80), "MeV")

    expected_gamma_pred = mp.mpf(
        "16.338962439648224784189299741156296927101016473597870996977246409594812352084401"
    )
    assert abs(gamma_pred - expected_gamma_pred) < mp.mpf("1e-78"), mp.nstr(
        abs(gamma_pred - expected_gamma_pred), 80
    )
    print("[PASS] gamma_pred chain:", mp.nstr(gamma_pred, 80))
    print("[INFO] |gamma_pred - gamma_ledger|:", mp.nstr(gamma_pred_residual, 80))

    assert rg_residual == 0
    print("[PASS] RG constraint residual:", mp.nstr(rg_residual, 80))

    print("ALL SESSION-2 PHASE-8 SYNC CHECKS PASSED")


if __name__ == "__main__":
    main()
