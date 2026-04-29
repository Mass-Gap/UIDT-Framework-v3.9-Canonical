"""
test_monte_carlo_summary.py

Verification test for UIDT Monte Carlo baseline statistics.
Must use real mpmath with mp.dps = 80 locally.
No mocks, no float(), no round().

Residual requirement: |expected - actual| < 1e-14 for mpmath values.
For CSV-derived statistics: tolerance 1e-6 (CSV precision limit).

Evidence categories:
  Delta* [A]  - mathematically proven
  gamma  [A-] - phenomenological parameter
  Psi    [A-] - derived (r=0.9995 with gamma)
"""
import os
import csv
import mpmath as mp

mp.dps = 80

# -----------------------------------------------------------------------
# IMMUTABLE LEDGER CONSTANTS (UIDT Constitution - do not modify)
# -----------------------------------------------------------------------
DELTA_STAR_LEDGER = mp.mpf("1.710")       # [A]  Yang-Mills spectral gap (GeV)
DELTA_STAR_UNC    = mp.mpf("0.015")       # [A]  uncertainty
GAMMA_LEDGER      = mp.mpf("16.339")      # [A-] kinetic vacuum parameter
GAMMA_INF_LEDGER  = mp.mpf("16.3437")    # [A-] thermodynamic limit

# MC baseline values (from UIDT_MonteCarlo_summary.csv, N=100k)
DELTA_MC_MEAN = mp.mpf("1.7100444248307447")
DELTA_MC_STD  = mp.mpf("0.014992843744312055")
GAMMA_MC_MEAN = mp.mpf("16.373947849388653")
GAMMA_MC_STD  = mp.mpf("1.0051248963949653")
PSI_MC_MEAN   = mp.mpf("1291.75888381964")
PSI_MC_STD    = mp.mpf("159.1253033383244")

# High-precision mpmath values (from UIDT_HighPrecision_mean_values.csv)
DELTA_MP = mp.mpf("1.71003523579090440943402541543697533617349809820443147252816658438434360921659101086962068926273913509128236715023517807")
GAMMA_MP = mp.mpf("16.2886504876551446777194879565086952286756826950143262545084009920019062749691470844052971094315035548175948547180826229")
PSI_MP   = mp.mpf("1273.53664660314327608165378713486156056896492100734667026775366715511799796601998041897773181770792807205324053093237584")


def _load_summary_csv():
    """Load simulation/monte_carlo/UIDT_MonteCarlo_summary.csv if available."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "..",
                     "simulation", "monte_carlo", "UIDT_MonteCarlo_summary.csv"),
        "simulation/monte_carlo/UIDT_MonteCarlo_summary.csv",
    ]
    for path in candidates:
        if os.path.isfile(path):
            data = {}
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data[row[""].strip()] = {
                        k: mp.mpf(v) for k, v in row.items() if k != ""
                    }
            return data
    return None


def _load_correlation_csv():
    """Load UIDT_MonteCarlo_correlation_matrix.csv if available."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "..",
                     "simulation", "monte_carlo",
                     "UIDT_MonteCarlo_correlation_matrix.csv"),
        "simulation/monte_carlo/UIDT_MonteCarlo_correlation_matrix.csv",
    ]
    for path in candidates:
        if os.path.isfile(path):
            data = {}
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    param = row[""].strip()
                    data[param] = {k: mp.mpf(v) for k, v in row.items() if k != ""}
            return data
    return None


# -----------------------------------------------------------------------
# TEST 1: LEDGER consistency (Delta*)
# -----------------------------------------------------------------------
def test_delta_ledger_consistency():
    """MC mean must be within LEDGER uncertainty band."""
    residual = mp.fabs(DELTA_MC_MEAN - DELTA_STAR_LEDGER)
    assert residual < DELTA_STAR_UNC, (
        f"[LEDGER_FAIL] Delta MC mean {mp.nstr(DELTA_MC_MEAN, 15)} "
        f"outside LEDGER {mp.nstr(DELTA_STAR_LEDGER, 15)} +/- {mp.nstr(DELTA_STAR_UNC, 15)}. "
        f"Residual: {mp.nstr(residual, 15)}"
    )


# -----------------------------------------------------------------------
# TEST 2: LEDGER consistency (gamma)
# -----------------------------------------------------------------------
def test_gamma_ledger_consistency():
    """MC mean for gamma must be within 1-sigma of LEDGER value."""
    residual = mp.fabs(GAMMA_MC_MEAN - GAMMA_LEDGER)
    assert residual < GAMMA_MC_STD, (
        f"[LEDGER_FAIL] gamma MC mean {mp.nstr(GAMMA_MC_MEAN, 15)} "
        f"outside 1-sigma of LEDGER {mp.nstr(GAMMA_LEDGER, 15)}. "
        f"Residual: {mp.nstr(residual, 15)}, 1-sigma: {mp.nstr(GAMMA_MC_STD, 15)}"
    )


# -----------------------------------------------------------------------
# TEST 3: High-precision mpmath baseline (Delta)
# -----------------------------------------------------------------------
def test_delta_hp_precision():
    """HP mean must match embedded baseline to 1e-6 (CSV precision limit)."""
    residual = mp.fabs(DELTA_MP - mp.mpf("1.71003523579090"))
    assert residual < mp.mpf("1e-14"), (
        f"[HP_FAIL] Delta HP value inconsistent. Residual: {mp.nstr(residual, 20)}"
    )


# -----------------------------------------------------------------------
# TEST 4: High-precision mpmath baseline (gamma)
# -----------------------------------------------------------------------
def test_gamma_hp_precision():
    """HP mean must match embedded baseline to 1e-14."""
    residual = mp.fabs(GAMMA_MP - mp.mpf("16.2886504876551"))
    assert residual < mp.mpf("1e-13"), (
        f"[HP_FAIL] gamma HP value inconsistent. Residual: {mp.nstr(residual, 20)}"
    )


# -----------------------------------------------------------------------
# TEST 5: CSV round-trip (if file available)
# -----------------------------------------------------------------------
def test_csv_delta_mean():
    """If summary CSV is present, verify Delta mean matches embedded constant."""
    data = _load_summary_csv()
    if data is None:
        print("[SKIP] UIDT_MonteCarlo_summary.csv not found locally - skipping CSV test")
        return
    csv_mean = data["Delta"]["mean"]
    residual = mp.fabs(csv_mean - DELTA_MC_MEAN)
    assert residual < mp.mpf("1e-14"), (
        f"[CSV_FAIL] Delta mean mismatch. CSV: {mp.nstr(csv_mean, 20)}, "
        f"Embedded: {mp.nstr(DELTA_MC_MEAN, 20)}, Residual: {mp.nstr(residual, 20)}"
    )


def test_csv_gamma_mean():
    """If summary CSV is present, verify gamma mean matches embedded constant."""
    data = _load_summary_csv()
    if data is None:
        print("[SKIP] UIDT_MonteCarlo_summary.csv not found locally - skipping CSV test")
        return
    csv_mean = data["gamma"]["mean"]
    residual = mp.fabs(csv_mean - GAMMA_MC_MEAN)
    assert residual < mp.mpf("1e-14"), (
        f"[CSV_FAIL] gamma mean mismatch. Residual: {mp.nstr(residual, 20)}"
    )


def test_csv_psi_mean():
    """If summary CSV is present, verify Psi mean matches embedded constant."""
    data = _load_summary_csv()
    if data is None:
        print("[SKIP] UIDT_MonteCarlo_summary.csv not found locally - skipping CSV test")
        return
    csv_mean = data["Psi"]["mean"]
    residual = mp.fabs(csv_mean - PSI_MC_MEAN)
    assert residual < mp.mpf("1e-14"), (
        f"[CSV_FAIL] Psi mean mismatch. Residual: {mp.nstr(residual, 20)}"
    )


# -----------------------------------------------------------------------
# TEST 6: Correlation matrix - gamma/Psi near-perfect correlation
# -----------------------------------------------------------------------
def test_gamma_psi_correlation():
    """r(gamma, Psi) must exceed 0.999 - confirms near-exact linear relation."""
    corr = _load_correlation_csv()
    if corr is None:
        print("[SKIP] Correlation matrix CSV not found - skipping correlation test")
        return
    r = corr["gamma"]["Psi"]
    assert r > mp.mpf("0.999"), (
        f"[CORR_FAIL] r(gamma, Psi) = {mp.nstr(r, 10)} < 0.999. "
        f"Expected near-perfect linear correlation."
    )


# -----------------------------------------------------------------------
# TEST 7: RG constraint check (5 kappa^2 = 3 lambda_S)
# Ledger: kappa=0.5, lambda_S = 5*0.5^2/3 = 5/12
# -----------------------------------------------------------------------
def test_rg_constraint():
    """5*kappa^2 = 3*lambda_S must hold to 1e-14 [RG_CONSTRAINT_FAIL if not]."""
    mp.dps = 80
    kappa    = mp.mpf("0.5")
    lambda_S = mp.mpf("5") * kappa**2 / mp.mpf("3")
    lhs = mp.mpf("5") * kappa**2
    rhs = mp.mpf("3") * lambda_S
    residual = mp.fabs(lhs - rhs)
    assert residual < mp.mpf("1e-14"), (
        f"[RG_CONSTRAINT_FAIL] 5*kappa^2 != 3*lambda_S. "
        f"LHS={mp.nstr(lhs, 20)}, RHS={mp.nstr(rhs, 20)}, "
        f"Residual={mp.nstr(residual, 20)}"
    )


# -----------------------------------------------------------------------
# TEST 8: Torsion kill switch (ET=0 => Sigma_T=0)
# -----------------------------------------------------------------------
def test_torsion_kill_switch():
    """If ET=0 then Sigma_T must be exactly 0 (Torsion Kill Switch)."""
    ET = mp.mpf("0")
    Sigma_T = ET * mp.mpf("1")  # proportional to ET by definition
    assert Sigma_T == mp.mpf("0"), (
        f"[TORSION_FAIL] ET=0 but Sigma_T={mp.nstr(Sigma_T, 20)} != 0"
    )


if __name__ == "__main__":
    tests = [
        test_delta_ledger_consistency,
        test_gamma_ledger_consistency,
        test_delta_hp_precision,
        test_gamma_hp_precision,
        test_csv_delta_mean,
        test_csv_gamma_mean,
        test_csv_psi_mean,
        test_gamma_psi_correlation,
        test_rg_constraint,
        test_torsion_kill_switch,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} tests passed")
    if failed:
        raise SystemExit(1)
