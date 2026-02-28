
from mpmath import mp, mpf

# Local precision initialization
mp.dps = 80

def run_lhcb_scan():
    # UIDT Constants
    gamma = mpf('16.339')
    gamma_inv = mpf('1.0') / gamma
    gamma_inv2 = mpf('1.0') / (gamma**2)
    gamma_inv3 = mpf('1.0') / (gamma**3)

    # Experimental Data (HFLAV 2024 / LHCb 2024 snippets)
    # R(D)
    RD_exp = mpf('0.342')
    RD_exp_err = mpf('0.026')
    RD_SM = mpf('0.298')
    RD_SM_err = mpf('0.004')

    # R(D*)
    RDs_exp = mpf('0.287')
    RDs_exp_err = mpf('0.012')
    RDs_SM = mpf('0.254')
    RDs_SM_err = mpf('0.005')

    # R(K) - 2022 LHCb Result (consistent with SM)
    RK_exp = mpf('1.0')
    RK_exp_err = mpf('0.0')
    RK_SM = mpf('1.0')
    RK_SM_err = mpf('0.0')

    print("=== UIDT LHCb Anomaly Scan (Research Mode) ===")
    print(f"Gamma = {gamma}")
    print(f"Gamma^-1 = {mp.nstr(gamma_inv, 5)}")
    print(f"Gamma^-2 = {mp.nstr(gamma_inv2, 5)}")
    print(f"Gamma^-3 = {mp.nstr(gamma_inv3, 5)}")
    print("")

    calculate_residuals(RD_exp, RD_exp_err, RD_SM, RD_SM_err, "R(D)")
    calculate_residuals(RDs_exp, RDs_exp_err, RDs_SM, RDs_SM_err, "R(D*)")
    calculate_residuals(RK_exp, RK_exp_err, RK_SM, RK_SM_err, "R(K)")

def calculate_residuals(R_exp, R_exp_err, R_SM, R_SM_err, label):
    # UIDT Constants for local scope if needed (though passed in run_lhcb_scan, but for clarity)
    gamma = mpf('16.339')
    gamma_inv = mpf('1.0') / gamma
    gamma_inv2 = mpf('1.0') / (gamma**2)
    gamma_inv3 = mpf('1.0') / (gamma**3)

    delta = abs(R_exp - R_SM) # Absolute residual as anomaly magnitude
    delta_err = mp.sqrt(R_exp_err**2 + R_SM_err**2)

    print(f"--- {label} ---")
    print(f"Exp: {mp.nstr(R_exp, 4)} +/- {mp.nstr(R_exp_err, 3)}")
    print(f"SM : {mp.nstr(R_SM, 4)} +/- {mp.nstr(R_SM_err, 3)}")
    print(f"Delta (Anomaly): {mp.nstr(delta, 4)} +/- {mp.nstr(delta_err, 4)}")

    # Check proportionality to gamma^-n
    print(f"Delta / gamma^-1 ({mp.nstr(gamma_inv, 4)}): {mp.nstr(delta / gamma_inv, 4)}")
    print(f"Delta / gamma^-2 ({mp.nstr(gamma_inv2, 4)}): {mp.nstr(delta / gamma_inv2, 4)}")
    print(f"Delta / gamma^-3 ({mp.nstr(gamma_inv3, 4)}): {mp.nstr(delta / gamma_inv3, 4)}")
    print("")

if __name__ == "__main__":
    run_lhcb_scan()
