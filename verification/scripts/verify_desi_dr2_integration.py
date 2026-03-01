import os
import random
import sympy as sp
from mpmath import mp, mpf, sqrt, ln

# Enforce high precision globally for mpmath operations
mp.dps = 80

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# --- Configuration ---
# UIDT Theoretical Values (Derived from Vacuum Dressing)
# w_a derived from holographic amplification L^4 * (delta_gamma/gamma_inf) ~ 1.30
UIDT_W0 = mpf('-0.99')
UIDT_WA = mpf('-1.30')

# Union3 / DESI DR2 / DESY5 Observational Constraints
# Source: DESI Collaboration / arXiv:2503.14738 Reference values
OBS_W0_MEAN = mpf('-0.667')
OBS_W0_ERR = mpf('0.09')
OBS_WA_MEAN = mpf('-1.09')
OBS_WA_ERR = mpf('0.37')
CORRELATION = mpf('0.3')  # Typical positive correlation

# MCMC Parameters
N_SAMPLES = 50000
BURN_IN = 5000
STEP_SCALE_W0 = mpf('0.05')
STEP_SCALE_WA = mpf('0.2')

# Output Path
OUTPUT_DIR = "verification/results/"

# --- Ensure Reproducibility ---
# Sets a fixed seed strictly to guarantee run-to-run 80-dps accuracy reproductions
random.seed(42)

# --- Compute Covariance Matrix explicitly ---
# cov = [[sigma_w0**2, rho*sigma_w0*sigma_wa], [rho*sigma_w0*sigma_wa, sigma_wa**2]]
cov_11 = OBS_W0_ERR ** 2
cov_12 = CORRELATION * OBS_W0_ERR * OBS_WA_ERR
cov_21 = cov_12
cov_22 = OBS_WA_ERR ** 2

# determinant of 2x2: ad - bc
det_cov = cov_11 * cov_22 - cov_12 * cov_21

# inverse of 2x2: 1/det * [[d, -b], [-c, a]]
inv_cov_11 = cov_22 / det_cov
inv_cov_12 = -cov_12 / det_cov
inv_cov_21 = -cov_21 / det_cov
inv_cov_22 = cov_11 / det_cov

def log_likelihood(w0, wa):
    """Calculate the log likelihood manually with mpmath for higher precision."""
    d_w0 = w0 - OBS_W0_MEAN
    d_wa = wa - OBS_WA_MEAN
    
    # chi2 = diff^T * inv_cov * diff 
    chi2 = inv_cov_11 * (d_w0 ** 2) + (inv_cov_12 + inv_cov_21) * d_w0 * d_wa + inv_cov_22 * (d_wa ** 2)
    return -mpf('0.5') * chi2

def normal_sample(mean, std):
    """Box-Muller transform using pure Python `random` and `mpmath`."""
    u1 = mpf(random.random())
    u2 = mpf(random.random())
    
    if u1 == mpf('0.0'): 
        u1 = mpf('1e-50')
        
    z0 = sqrt(-mpf('2.0') * ln(u1)) * mp.cos(mpf('2.0') * mp.pi * u2)
    return mean + z0 * std

def metropolis_hastings(n_samples, burn_in):
    """Custom MCMC Metropolis-Hastings utilizing entirely mpmath objects."""
    samples_w0 = []
    samples_wa = []
    
    current_w0 = OBS_W0_MEAN
    current_wa = OBS_WA_MEAN
    current_log_prob = log_likelihood(current_w0, current_wa)
    
    accepted = 0
    total_steps = n_samples + burn_in
    
    for i in range(total_steps):
        prop_w0 = normal_sample(current_w0, STEP_SCALE_W0)
        prop_wa = normal_sample(current_wa, STEP_SCALE_WA)
        
        prop_log_prob = log_likelihood(prop_w0, prop_wa)
        ratio_log = prop_log_prob - current_log_prob
        
        u = mpf(random.random())
        if u == mpf('0.0'): 
            u = mpf('1e-50')
        
        if ln(u) < ratio_log:
            current_w0 = prop_w0
            current_wa = prop_wa
            current_log_prob = prop_log_prob
            accepted += 1
            
        if i >= burn_in:
            samples_w0.append(current_w0)
            samples_wa.append(current_wa)
            
    print(f"MCMC Acceptance Rate: {(accepted / total_steps) * 100:.2f}%")
    return samples_w0, samples_wa

# --- Statistical Analysis ---
def compute_mean(arr):
    return sum(arr) / len(arr)

def compute_variance(arr, mean_val):
    return sum([(x - mean_val)**2 for x in arr]) / (len(arr) - 1)

def compute_covariance(arr1, arr2, mean1, mean2):
    return sum([(arr1[i] - mean1) * (arr2[i] - mean2) for i in range(len(arr1))]) / (len(arr1) - 1)

def run_integration_verification():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"--- DESI-DR2 Integration Verification (UIDT v3.9) ---")
    print(f"Target: Illustrative comparison of UIDT (w0={UIDT_W0}, wa={UIDT_WA}) against constraints at 80 dps precision.")

    print("\n[1] Running MCMC Chain (Custom Metropolis-Hastings via mpmath)...")
    chain_w0, chain_wa = metropolis_hastings(N_SAMPLES, BURN_IN)

    mean_w0 = compute_mean(chain_w0)
    mean_wa = compute_mean(chain_wa)
    var_w0 = compute_variance(chain_w0, mean_w0)
    var_wa = compute_variance(chain_wa, mean_wa)
    std_w0 = sqrt(var_w0)
    std_wa = sqrt(var_wa)
    cov_samp = compute_covariance(chain_w0, chain_wa, mean_w0, mean_wa)

    # Calculate Mahalanobis Distance (Z-score in 2D) explicitly via derived covariance inversion
    samp_det = var_w0 * var_wa - cov_samp**2
    samp_inv_11 = var_wa / samp_det
    samp_inv_12 = -cov_samp / samp_det
    samp_inv_21 = -cov_samp / samp_det
    samp_inv_22 = var_w0 / samp_det

    diff_w0 = UIDT_W0 - mean_w0
    diff_wa = UIDT_WA - mean_wa

    mah_sq = samp_inv_11 * (diff_w0**2) + (samp_inv_12 + samp_inv_21) * diff_w0 * diff_wa + samp_inv_22 * (diff_wa**2)
    mahalanobis_dist = sqrt(mah_sq)

    print(f"\n[2] Statistical Results (80 dps precision):")
    print(f"  Reference MCMC Mean: w0 = {mp.nstr(mean_w0, 5)} +/- {mp.nstr(std_w0, 5)}")
    print(f"  Reference MCMC Mean: wa = {mp.nstr(mean_wa, 5)} +/- {mp.nstr(std_wa, 5)}")
    print(f"  UIDT Prediction:  w0 = {mp.nstr(UIDT_W0, 5)}, wa = {mp.nstr(UIDT_WA, 5)}")
    print(f"  --> Mahalanobis Distance (Sigma): {mp.nstr(mahalanobis_dist, 5)} sigma")
    print("  --> STATUS: ILLUSTRATIVE ONLY (PLACEHOLDER CONSTRAINTS; NOT EXTERNAL VALIDATION)")

    print("\n[3] Symbolic Reconstruction of Vacuum Energy Density rho_DE(z)...")
    z = sp.symbols('z', real=True, positive=True)
    w0_sym, wa_sym = sp.symbols('w0 wa', real=True)
    rho0_sym = sp.symbols('rho_DE0', real=True, positive=True)

    w_z_prime = w0_sym + wa_sym * (sp.symbols('z_prime', real=True, positive=True) / (1 + sp.symbols('z_prime', real=True, positive=True)))
    integrand = (1 + w_z_prime) / (1 + sp.symbols('z_prime', real=True, positive=True))
    definite_integral = sp.integrate(integrand, (sp.symbols('z_prime', real=True, positive=True), 0, z))

    rho_de_expr = rho0_sym * sp.exp(3 * definite_integral)
    rho_de_simplified = sp.simplify(rho_de_expr)

    print(f"  Analytic Form of rho_DE(z) [CPL]:")
    sp.pprint(rho_de_simplified)

    eval_val = rho_de_simplified.subs({
        z: sp.Float('2.33', 80),
        w0_sym: sp.Float('-0.99', 80),
        wa_sym: sp.Float('-1.30', 80),
        rho0_sym: sp.Float('1.0', 80)
    }).evalf(80)

    print(f"\n  Numerical Check at z=2.33 (Ly-alpha) with UIDT params:")
    print(f"  rho_DE(2.33) / rho_DE(0) = {mp.nstr(mpf(str(eval_val)), 5)}")

    print("\n[4] Generating Visualization...")
    if not HAS_MATPLOTLIB:
        print("  Matplotlib not available; skipping plot generation.")
        print("\n--- Verification Complete (no-plot mode) ---")
        return

    # Visualizations
    chain_w0_float = [float(x) for x in chain_w0[::10]]
    chain_wa_float = [float(x) for x in chain_wa[::10]]

    plt.figure(figsize=(8, 6))
    plt.scatter(chain_w0_float, chain_wa_float, s=1, alpha=0.1, color='gray', label='Reference MCMC Chain')

    def plot_ellipse(mean, cov, scale, color, label):
        import math
        cov_arr = [[float(cov[0][0]), float(cov[0][1])], [float(cov[1][0]), float(cov[1][1])]]
        tr = cov_arr[0][0] + cov_arr[1][1]
        det = cov_arr[0][0] * cov_arr[1][1] - cov_arr[0][1] * cov_arr[1][0]
        gap = math.sqrt(abs(tr*tr - 4*det))
        lambda1 = (tr + gap) / 2
        lambda2 = (tr - gap) / 2
        
        v1_x = cov_arr[0][1]
        v1_y = lambda1 - cov_arr[0][0]
        if v1_x == 0 and v1_y == 0: v1_x, v1_y = 1, 0
        norm = math.sqrt(v1_x**2 + v1_y**2)
        v1_x, v1_y = v1_x/norm, v1_y/norm
        angle = math.degrees(math.atan2(v1_y, v1_x))
        
        width = 2 * math.sqrt(abs(lambda1)) * scale
        height = 2 * math.sqrt(abs(lambda2)) * scale
        
        ellipse = Ellipse(xy=(float(mean[0]), float(mean[1])), width=width, height=height, 
                          angle=angle, edgecolor=color, fc='None', lw=1.5, label=label)
        plt.gca().add_patch(ellipse)

    import math
    scale1 = math.sqrt(2.30)
    scale2 = math.sqrt(6.18)
    cov_2d = [[var_w0, cov_samp], [cov_samp, var_wa]]
    
    plot_ellipse([mean_w0, mean_wa], cov_2d, scale1, 'blue', '1-sigma')
    plot_ellipse([mean_w0, mean_wa], cov_2d, scale2, 'cyan', '2-sigma')

    uidt_w0_f, uidt_wa_f = float(UIDT_W0), float(UIDT_WA)
    plt.scatter([uidt_w0_f], [uidt_wa_f], color='red', s=100, marker='*', label='UIDT v3.9 Prediction')
    plt.text(uidt_w0_f + 0.02, uidt_wa_f + 0.05, f"UIDT\n({uidt_w0_f:.2f}, {uidt_wa_f:.2f})", color='red')

    obs_w0, obs_wa = float(OBS_W0_MEAN), float(OBS_WA_MEAN)
    err_w0, err_wa = float(OBS_W0_ERR), float(OBS_WA_ERR)
    plt.xlim(obs_w0 - 5*err_w0, obs_w0 + 5*err_w0)
    plt.ylim(obs_wa - 4*err_wa, obs_wa + 4*err_wa)

    plt.xlabel('w0 (Equation of State)')
    plt.ylabel('wa (Evolution)')
    plt.title(f'DESI-DR2 Integration: UIDT v3.9 vs Reference\nSigma = {float(mahalanobis_dist):.2f}')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plot_path = os.path.join(OUTPUT_DIR, "desi_dr2_integration.png")
    plt.savefig(plot_path)
    print(f"  Plot saved to: {plot_path}")
    print("\n--- Verification Complete ---")

if __name__ == '__main__':
    run_integration_verification()
