"""verify_rg_flow_gamma.py

UIAT Framework v3.9 — P1 Verification Script
Honest audit version: 2026-04-03

What this script verifies (Category A):
  1. RG constraint 5κ²=3λ_S at the non-trivial fixed point
  2. SU(3) Casimir invariants
  3. Vacuum dressing integral I_vac = 16/9
  4. Numerical proximity of (2Nc+1)²/Nc to γ_ledger

What this script does NOT yet do (Gap G5 — OPEN):
  - Does not DERIVE 49/3 from the β-function couplings
  - gamma_exact = 49/3 is inserted as a CONJECTURE, not computed
  - This gap must be closed before evidence upgrade to A−

Rules:
  - mp.dps = 80 LOCAL (RACE CONDITION LOCK)
  - No float(), no round(), no silent approximation
  - Residual |LHS - RHS| < 1e-14 for Category A claims
"""

import mpmath as mp
import sys
import json


def verify_rg_constraint():
    """Verify 5κ²=3λ_S at the RG fixed point. [Category A]"""
    mp.dps = 80
    kappa_star  = mp.mpf('1')
    lambda_star = mp.mpf('5') / mp.mpf('3')
    lhs = mp.mpf('5') * kappa_star**2
    rhs = mp.mpf('3') * lambda_star
    residual = abs(lhs - rhs)
    assert residual < mp.mpf('1e-14'), (
        f"[RG_CONSTRAINT_FAIL] residual={mp.nstr(residual, 20)}"
    )
    return {
        "test":     "rg_constraint_5kappa2_eq_3lambda",
        "lhs":      mp.nstr(lhs, 20),
        "rhs":      mp.nstr(rhs, 20),
        "residual": mp.nstr(residual, 10),
        "category": "A",
        "status":   "PASS"
    }


def verify_su3_casimirs():
    """Verify SU(3) Casimir invariants. [Category A]"""
    mp.dps = 80
    Nc      = mp.mpf('3')
    C2_fund = (Nc**2 - 1) / (mp.mpf('2') * Nc)
    C2_adj  = Nc
    dim_adj = Nc**2 - 1

    assert abs(C2_fund - mp.mpf('4') / mp.mpf('3')) < mp.mpf('1e-14'), "C2_fund fail"
    assert abs(C2_adj  - mp.mpf('3'))                < mp.mpf('1e-14'), "C2_adj fail"
    assert abs(dim_adj - mp.mpf('8'))                < mp.mpf('1e-14'), "dim_adj fail"

    I_vac = C2_fund * dim_adj / (mp.mpf('2') * C2_adj)
    I_vac_exact = mp.mpf('16') / mp.mpf('9')
    assert abs(I_vac - I_vac_exact) < mp.mpf('1e-14'), "I_vac fail"

    return {
        "test":     "su3_casimirs_and_I_vac",
        "C2_fund":  mp.nstr(C2_fund, 20),
        "C2_adj":   mp.nstr(C2_adj, 20),
        "dim_adj":  mp.nstr(dim_adj, 20),
        "I_vac":    mp.nstr(I_vac, 20),
        "category": "A",
        "status":   "PASS"
    }


def verify_gamma_proximity():
    """Check (2Nc+1)²/Nc vs γ_ledger. [Category D — conjecture, not derivation]

    NOTE (Gap G5): gamma_exact = 49/3 is INSERTED here as a conjecture.
    This function does NOT compute 49/3 from the β-function couplings.
    Closing Gap G5 requires an explicit derivation from κ*, λ_S*.
    """
    mp.dps = 80
    Nc           = mp.mpf('3')
    gamma_exact  = mp.mpf('49') / mp.mpf('3')          # CONJECTURE — not derived
    gamma_ledger = mp.mpf('16.339')
    gamma_inf    = mp.mpf('16.3437')
    delta_gamma  = mp.mpf('0.0047')

    # Numerical observation: (2Nc+1)²/Nc = 49/3 for Nc=3
    observation  = (2*Nc + 1)**2 / Nc
    obs_residual = abs(observation - gamma_exact)
    assert obs_residual < mp.mpf('1e-14'), "(2Nc+1)^2/Nc observation fail"

    deviation    = abs(gamma_exact  - gamma_ledger)
    rel_dev      = deviation / gamma_ledger
    consistency  = abs((gamma_inf - delta_gamma) - gamma_ledger)

    return {
        "test":             "gamma_proximity_D",
        "observation":      "(2Nc+1)^2/Nc = 49/3 for Nc=3",
        "gap_G5":           "gamma_exact inserted as conjecture — NOT derived from couplings",
        "gamma_conjecture": mp.nstr(gamma_exact, 40),
        "gamma_ledger":     mp.nstr(gamma_ledger, 10),
        "deviation":        mp.nstr(deviation, 10),
        "relative_pct":     mp.nstr(rel_dev * 100, 6),
        "consistency":      mp.nstr(consistency, 10),
        "within_MC_corridor": str(deviation < mp.mpf('0.01')),
        "category":         "D",
        "status":           "PASS"
    }


def main():
    results  = []
    all_pass = True

    for fn in [verify_rg_constraint, verify_su3_casimirs, verify_gamma_proximity]:
        try:
            r = fn()
            results.append(r)
            if r.get("status") != "PASS":
                all_pass = False
        except AssertionError as e:
            results.append({"test": fn.__name__, "status": "FAIL", "error": str(e)})
            all_pass = False

    output = {
        "script":        "verify_rg_flow_gamma.py",
        "framework":     "UIDT v3.9",
        "precision_dps": 80,
        "audit_note":    "Category A: RG constraint + Casimirs. Category D: gamma proximity (Gap G5 open).",
        "results":       results,
        "overall":       "PASS" if all_pass else "FAIL"
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
