
import math

def run_lhcb_scan():
    # UIDT Constants
    gamma = 16.339
    gamma_inv = 1.0 / gamma
    gamma_inv2 = 1.0 / (gamma**2)
    gamma_inv3 = 1.0 / (gamma**3)

    # Experimental Data (HFLAV 2024 / LHCb 2024 snippets)
    # R(D)
    RD_exp = 0.342
    RD_exp_err = 0.026
    RD_SM = 0.298
    RD_SM_err = 0.004

    # R(D*)
    RDs_exp = 0.287
    RDs_exp_err = 0.012
    RDs_SM = 0.254
    RDs_SM_err = 0.005

    # R(K) - 2022 LHCb Result (consistent with SM)
    RK_exp = 1.0
    RK_exp_err = 0.0
    RK_SM = 1.0
    RK_SM_err = 0.0

    print("=== UIDT LHCb Anomaly Scan (Research Mode) ===")
    print(f"Gamma = {gamma}")
    print(f"Gamma^-1 = {gamma_inv:.5f}")
    print(f"Gamma^-2 = {gamma_inv2:.5f}")
    print(f"Gamma^-3 = {gamma_inv3:.5f}")
    print("")

    calculate_residuals(RD_exp, RD_exp_err, RD_SM, RD_SM_err, "R(D)")
    calculate_residuals(RDs_exp, RDs_exp_err, RDs_SM, RDs_SM_err, "R(D*)")
    calculate_residuals(RK_exp, RK_exp_err, RK_SM, RK_SM_err, "R(K)")

def calculate_residuals(R_exp, R_exp_err, R_SM, R_SM_err, label):
    # UIDT Constants for local scope if needed (though passed in run_lhcb_scan, but for clarity)
    gamma = 16.339
    gamma_inv = 1.0 / gamma
    gamma_inv2 = 1.0 / (gamma**2)
    gamma_inv3 = 1.0 / (gamma**3)

    delta = abs(R_exp - R_SM) # Absolute residual as anomaly magnitude
    delta_err = math.sqrt(R_exp_err**2 + R_SM_err**2)

    print(f"--- {label} ---")
    print(f"Exp: {R_exp:.4f} +/- {R_exp_err:.3f}")
    print(f"SM : {R_SM:.4f} +/- {R_SM_err:.3f}")
    print(f"Delta (Anomaly): {delta:.4f} +/- {delta_err:.4f}")

    # Check proportionality to gamma^-n
    print(f"Delta / gamma^-1 ({gamma_inv:.4f}): {delta / gamma_inv:.4f}")
    print(f"Delta / gamma^-2 ({gamma_inv2:.4f}): {delta / gamma_inv2:.4f}")
    print(f"Delta / gamma^-3 ({gamma_inv3:.4f}): {delta / gamma_inv3:.4f}")
    print("")

if __name__ == "__main__":
    run_lhcb_scan()
