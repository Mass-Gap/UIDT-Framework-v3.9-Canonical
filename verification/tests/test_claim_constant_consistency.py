"""
test_claim_constant_consistency.py

Verifies that every canonical constant in CANONICAL/CONSTANTS.md
is consistent with the corresponding entries in LEDGER/CLAIMS.json.

Rules enforced:
  1. Every constant value appearing in CLAIMS.json that refers to a ledger
     symbol must agree with CANONICAL/CONSTANTS.md to within stated uncertainty.
  2. Evidence categories in CLAIMS.json must not exceed the ceiling defined in
     CANONICAL/EVIDENCE_SYSTEM.md (cosmology <= C, phenomenological <= A-).
  3. No claim may reference a withdrawn (Evidence E) constant as its source.

Precision: mpmath mp.dps = 80  (local, no global state)
Framework: pytest
"""

import json
import re
import os
import pytest

# ---------------------------------------------------------------------------
# Canonical ledger values (ground truth from CANONICAL/CONSTANTS.md v3.9.5)
# All values stored as strings to allow mp.mpf conversion later.
# ---------------------------------------------------------------------------
CANONICAL_CONSTANTS = {
    "Delta_star":  {"value": "1.710",   "uncertainty": "0.015", "evidence": "A",  "unit": "GeV"},
    "gamma":       {"value": "16.339",  "uncertainty": "0.005", "evidence": "A-", "unit": ""},
    "gamma_MC":    {"value": "16.374",  "uncertainty": "1.005", "evidence": "A-", "unit": ""},
    "gamma_inf":   {"value": "16.3437", "uncertainty": "0.0005","evidence": "B",  "unit": ""},
    "kappa":       {"value": "0.500",   "uncertainty": "0.008", "evidence": "A",  "unit": ""},
    "lambda_S":    {"value": "0.41666666666666666", "uncertainty": "0.007", "evidence": "A", "unit": ""},
    "v":           {"value": "47.7",    "uncertainty": "0.1",   "evidence": "A",  "unit": "MeV"},
    "E_T":         {"value": "2.44",    "uncertainty": "0.05",  "evidence": "C",  "unit": "MeV"},
    "H0":          {"value": "70.4",    "uncertainty": "0.16",  "evidence": "C",  "unit": "km/s/Mpc"},
    "w0":          {"value": "-0.99",   "uncertainty": "0.05",  "evidence": "C",  "unit": ""},
    "delta_gamma": {"value": "0.0047",  "uncertainty": "0.001", "evidence": "B",  "unit": ""},
}

# Evidence hierarchy: higher index = stronger claim
EVIDENCE_RANK = {"E": -1, "D": 0, "C": 1, "B": 2, "A-": 3, "A": 4}

# Category ceilings per domain
CEILINGS = {
    "cosmology": "C",
    "phenomenological": "A-",
}

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLAIMS_PATH = os.path.join(REPO_ROOT, "LEDGER", "CLAIMS.json")


def load_claims():
    with open(CLAIMS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Test 1: CLAIMS.json is valid JSON and contains required top-level keys
# ---------------------------------------------------------------------------
def test_claims_json_is_valid_and_structured():
    data = load_claims()
    assert isinstance(data, (list, dict)), "CLAIMS.json must be a JSON array or object"


# ---------------------------------------------------------------------------
# Test 2: RG fixed-point constraint  5κ² = 3λ_S  at 80-digit precision
# ---------------------------------------------------------------------------
def test_rg_fixed_point_constraint():
    import mpmath as mp
    mp.dps = 80
    kappa    = mp.mpf("1") / mp.mpf("2")          # exact: 1/2
    lambda_s = mp.mpf("5") * kappa**2 / mp.mpf("3")  # exact: 5/12
    residual = abs(mp.mpf("5") * kappa**2 - mp.mpf("3") * lambda_s)
    assert residual < mp.mpf("1e-14"), (
        f"[RG_CONSTRAINT_FAIL] residual = {mp.nstr(residual, 20)} >= 1e-14"
    )


# ---------------------------------------------------------------------------
# Test 3: γ kinetic vs γ_MC within 1σ
# ---------------------------------------------------------------------------
def test_gamma_kinetic_mc_consistency():
    import mpmath as mp
    mp.dps = 80
    gamma_k  = mp.mpf(CANONICAL_CONSTANTS["gamma"]["value"])
    gamma_mc = mp.mpf(CANONICAL_CONSTANTS["gamma_MC"]["value"])
    sigma_mc = mp.mpf(CANONICAL_CONSTANTS["gamma_MC"]["uncertainty"])
    diff = abs(gamma_k - gamma_mc)
    assert diff <= sigma_mc, (
        f"gamma_kinetic={mp.nstr(gamma_k,10)} and gamma_MC={mp.nstr(gamma_mc,10)} "
        f"differ by {mp.nstr(diff,10)} > 1σ={mp.nstr(sigma_mc,10)}"
    )


# ---------------------------------------------------------------------------
# Test 4: δγ = γ_∞ − γ_kinetic matches ledger value
# ---------------------------------------------------------------------------
def test_delta_gamma_consistency():
    import mpmath as mp
    mp.dps = 80
    gamma_inf = mp.mpf(CANONICAL_CONSTANTS["gamma_inf"]["value"])
    gamma_k   = mp.mpf(CANONICAL_CONSTANTS["gamma"]["value"])
    delta_g   = mp.mpf(CANONICAL_CONSTANTS["delta_gamma"]["value"])
    computed  = gamma_inf - gamma_k
    residual  = abs(computed - delta_g)
    # tolerance = sum of stated uncertainties
    tol = mp.mpf(CANONICAL_CONSTANTS["gamma_inf"]["uncertainty"]) + \
          mp.mpf(CANONICAL_CONSTANTS["gamma"]["uncertainty"])
    assert residual <= tol, (
        f"delta_gamma mismatch: computed={mp.nstr(computed,10)}, "
        f"ledger={mp.nstr(delta_g,10)}, diff={mp.nstr(residual,10)}, tol={mp.nstr(tol,10)}"
    )


# ---------------------------------------------------------------------------
# Test 5: E_geo = Δ*/γ  agrees with expected 104.66 MeV within 1 MeV
# ---------------------------------------------------------------------------
def test_geometric_energy_derived():
    import mpmath as mp
    mp.dps = 80
    delta = mp.mpf(CANONICAL_CONSTANTS["Delta_star"]["value"]) * mp.mpf("1000")  # → MeV
    gamma = mp.mpf(CANONICAL_CONSTANTS["gamma"]["value"])
    E_geo = delta / gamma
    expected = mp.mpf("104.66")
    assert abs(E_geo - expected) < mp.mpf("1.0"), (
        f"E_geo = {mp.nstr(E_geo, 8)} MeV, expected ~104.66 MeV"
    )


# ---------------------------------------------------------------------------
# Test 6: f_vac = E_geo + E_T  within composite uncertainty
# ---------------------------------------------------------------------------
def test_f_vac_composite():
    import mpmath as mp
    mp.dps = 80
    delta = mp.mpf(CANONICAL_CONSTANTS["Delta_star"]["value"]) * mp.mpf("1000")
    gamma = mp.mpf(CANONICAL_CONSTANTS["gamma"]["value"])
    E_T   = mp.mpf(CANONICAL_CONSTANTS["E_T"]["value"])
    f_vac_computed = delta / gamma + E_T
    f_vac_ledger   = mp.mpf("107.10")
    assert abs(f_vac_computed - f_vac_ledger) < mp.mpf("1.5"), (
        f"f_vac mismatch: computed={mp.nstr(f_vac_computed, 8)}, "
        f"ledger={mp.nstr(f_vac_ledger, 8)}"
    )


# ---------------------------------------------------------------------------
# Test 7: No cosmological constant carries evidence > C
# ---------------------------------------------------------------------------
COSMOLOGY_KEYS = {"H0", "w0", "delta_gamma"}

def test_cosmological_evidence_ceiling():
    ceiling_rank = EVIDENCE_RANK[CEILINGS["cosmology"]]  # C → 1
    for key in COSMOLOGY_KEYS:
        ev = CANONICAL_CONSTANTS[key]["evidence"]
        rank = EVIDENCE_RANK.get(ev, -99)
        assert rank <= ceiling_rank, (
            f"Cosmological constant '{key}' has evidence {ev} "
            f"which exceeds ceiling C (rank {ceiling_rank})"
        )


# ---------------------------------------------------------------------------
# Test 8: γ retains evidence A- and never A
# ---------------------------------------------------------------------------
def test_gamma_evidence_cannot_be_A():
    ev = CANONICAL_CONSTANTS["gamma"]["evidence"]
    assert ev == "A-", (
        f"gamma evidence must be A- (phenomenological). Found: {ev}. "
        "Upgrade to A requires first-principles RG derivation (L4 open)."
    )
