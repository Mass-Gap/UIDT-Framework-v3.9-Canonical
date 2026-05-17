#!/usr/bin/env python3
"""
UIDT v3.9 — Phase 8.2 P5 SU(4) scaling cross-check.

This script audits the corrected Session-2 bare-gamma scaling law

    gamma_bare(Nc) = (2Nc + 1)^2 / Nc

against the previously incorrect denominator Nc^2 and records the SU(4)
consequence. It does not compare to a numerical lattice gamma observable,
because no such UIDT gamma observable is established in SU(4). Therefore the
result is an algebraic falsification-readiness check, not an evidence upgrade.

External lattice anchor
-----------------------
Athenodorou & Teper, "SU(N) gauge theories in 3+1 dimensions: glueball
spectrum, string tensions and topology", JHEP 12 (2021) 082,
DOI: 10.1007/JHEP12(2021)082, arXiv:2106.00364.

Reproduction
------------
python verification/scripts/verify_phase8_su4_crosscheck.py
"""

from __future__ import annotations

import mpmath as mp


def gamma_bare_correct(nc: mp.mpf) -> mp.mpf:
    return (2 * nc + 1) ** 2 / nc


def gamma_bare_wrong(nc: mp.mpf) -> mp.mpf:
    return (2 * nc + 1) ** 2 / (nc**2)


def main() -> None:
    mp.dps = 80

    nc3 = mp.mpf(3)
    nc4 = mp.mpf(4)

    gamma_su3 = gamma_bare_correct(nc3)
    gamma_su4 = gamma_bare_correct(nc4)
    wrong_su3 = gamma_bare_wrong(nc3)
    wrong_su4 = gamma_bare_wrong(nc4)

    n_su3 = nc3**2 * mp.mpf(11)
    n_su4 = nc4**2 * mp.mpf(11)

    gamma_ledger = mp.mpf("16.339")
    delta_su3 = gamma_ledger - gamma_su3

    assert gamma_su3 == mp.mpf(49) / mp.mpf(3)
    assert gamma_su4 == mp.mpf(81) / mp.mpf(4)
    assert wrong_su3 == mp.mpf(49) / mp.mpf(9)
    assert wrong_su4 == mp.mpf(81) / mp.mpf(16)
    assert wrong_su3 != gamma_su3
    assert wrong_su4 != gamma_su4
    assert n_su3 == mp.mpf(99)
    assert n_su4 == mp.mpf(176)
    assert delta_su3 == mp.mpf(17) / mp.mpf(3000)

    print("[PASS] corrected SU(3) gamma_bare =", mp.nstr(gamma_su3, 80))
    print("[PASS] rejected wrong SU(3) denominator =", mp.nstr(wrong_su3, 80))
    print("[PASS] predicted SU(4) gamma_bare =", mp.nstr(gamma_su4, 80))
    print("[PASS] rejected wrong SU(4) denominator =", mp.nstr(wrong_su4, 80))
    print("[PASS] N_SU(3) = Nc^2 * 11 =", mp.nstr(n_su3, 80))
    print("[PASS] N_SU(4) = Nc^2 * 11 =", mp.nstr(n_su4, 80))
    print("[PASS] SU(3) Delta_gamma_required =", mp.nstr(delta_su3, 80))
    print("[RESULT] SU(4) cross-check is falsification-ready [D], not validated [B]")
    print("ALL PHASE-8 P5 SU(4) CROSS-CHECKS PASSED")


if __name__ == "__main__":
    main()
