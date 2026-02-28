import numpy as np
import scipy.stats as stats
import sympy as sp
import os

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except Exception:
    HAS_MATPLOTLIB = False

# --- Configuration ---
# UIDT Theoretical Values (Derived from Vacuum Dressing)
# w_a derived from holographic amplification L^4 * (delta_gamma/gamma_inf) ~ 1.30
UIDT_W0 = -0.99
UIDT_WA = -1.30

# Union3 / DESY5 Observational Constraints (Approximate)
# Source: DESI Collaboration / Union3 (2024/2025)
OBS_W0_MEAN = -0.67
OBS_W0_ERR = 0.09
OBS_WA_MEAN = -1.27
OBS_WA_ERR = 0.37
CORRELATION = 0.3  # Slight positive correlation typical for w0-wa

# MCMC Parameters
N_SAMPLES = 50000
BURN_IN = 5000
STEP_SCALE = [0.05, 0.2]  # Step sizes for w0, wa

# Output Path
OUTPUT_DIR = "verification/results/"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"--- DESI-DR2 Integration Verification (UIDT v3.9) ---")
print(f"Target: Illustrative comparison of UIDT (w0={UIDT_W0}, wa={UIDT_WA}) against approximate constraints.")

# --- 1. MCMC Implementation (Metropolis-Hastings) ---

def log_likelihood(theta):
    w0, wa = theta
    # Covariance Matrix construction
    sigma_w0 = OBS_W0_ERR
    sigma_wa = OBS_WA_ERR
    rho = CORRELATION
    cov = np.array([[sigma_w0**2, rho * sigma_w0 * sigma_wa],
                    [rho * sigma_w0 * sigma_wa, sigma_wa**2]])
    inv_cov = np.linalg.inv(cov)

    diff = np.array([w0 - OBS_W0_MEAN, wa - OBS_WA_MEAN])
    chi2 = diff.T @ inv_cov @ diff
    return -0.5 * chi2

def metropolis_hastings(n_samples, burn_in):
    samples = np.zeros((n_samples, 2))
    current_theta = np.array([OBS_W0_MEAN, OBS_WA_MEAN])
    current_log_prob = log_likelihood(current_theta)

    accepted = 0
    for i in range(n_samples + burn_in):
        # Propose new state
        proposal = current_theta + np.random.normal(0, STEP_SCALE, 2)
        proposal_log_prob = log_likelihood(proposal)

        # Acceptance ratio
        ratio = np.exp(proposal_log_prob - current_log_prob)

        if np.random.rand() < ratio:
            current_theta = proposal
            current_log_prob = proposal_log_prob
            accepted += 1

        if i >= burn_in:
            samples[i - burn_in] = current_theta

    print(f"MCMC Acceptance Rate: {accepted / (n_samples + burn_in):.2%}")
    return samples

print("\n[1] Running MCMC Chain (Custom Metropolis-Hastings)...")
chain = metropolis_hastings(N_SAMPLES, BURN_IN)

# --- 2. Statistical Analysis ---

mean_w0 = np.mean(chain[:, 0])
mean_wa = np.mean(chain[:, 1])
std_w0 = np.std(chain[:, 0])
std_wa = np.std(chain[:, 1])

# Calculate Mahalanobis Distance (Z-score in 2D)
cov_matrix = np.cov(chain.T)
inv_cov = np.linalg.inv(cov_matrix)
diff = np.array([UIDT_W0 - mean_w0, UIDT_WA - mean_wa])
mahalanobis_dist = np.sqrt(diff.T @ inv_cov @ diff)

print(f"\n[2] Statistical Results:")
print(f"  Union3 MCMC Mean: w0 = {mean_w0:.4f} +/- {std_w0:.4f}")
print(f"  Union3 MCMC Mean: wa = {mean_wa:.4f} +/- {std_wa:.4f}")
print(f"  UIDT Prediction:  w0 = {UIDT_W0:.4f}, wa = {UIDT_WA:.4f}")
print(f"  --> Mahalanobis Distance (Sigma): {mahalanobis_dist:.4f} sigma")

if mahalanobis_dist < 1.0:
    print("  --> STATUS: ILLUSTRATIVE ONLY (PLACEHOLDER CONSTRAINTS; NOT EXTERNAL VALIDATION)")
else:
    print("  --> STATUS: ILLUSTRATIVE ONLY (PLACEHOLDER CONSTRAINTS; NOT EXTERNAL VALIDATION)")

# --- 3. Symbolic Reconstruction of rho_DE(z) ---

print("\n[3] Symbolic Reconstruction of Vacuum Energy Density rho_DE(z)...")

z = sp.symbols('z', real=True, positive=True)
w0, wa = sp.symbols('w0 wa', real=True)
rho0 = sp.symbols('rho_DE0', real=True, positive=True)

# CPL Parametrization w(z)
w_z = w0 + wa * (z / (1 + z))

# Friedmann Integral for Dark Energy Density
# rho_DE(z) = rho_DE,0 * exp(3 * integral_0^z (1 + w(z')) / (1 + z') dz')
integral_term = (1 + w_z) / (1 + z)
integral_result = sp.integrate(integral_term, z)
# Note: Indefinite integral needs limits [0, z].
# Integral of (1 + w0 + wa*z/(1+z))/(1+z) dz
# = Integral ( (1+w0)/(1+z) + wa*z/(1+z)^2 ) dz
# = (1+w0)*ln(1+z) + wa * (ln(1+z) + 1/(1+z))  <-- check this carefully manually or trust sympy

# Correct approach with limits
z_prime = sp.symbols('z_prime', real=True, positive=True)
w_z_prime = w0 + wa * (z_prime / (1 + z_prime))
integrand = (1 + w_z_prime) / (1 + z_prime)
definite_integral = sp.integrate(integrand, (z_prime, 0, z))

rho_de_expr = rho0 * sp.exp(3 * definite_integral)
rho_de_simplified = sp.simplify(rho_de_expr)

print(f"  Analytic Form of rho_DE(z) [CPL]:")
sp.pprint(rho_de_simplified)

# Evaluate at z=2.33 (Lyman-alpha anchor)
rho_func = sp.lambdify((z, w0, wa, rho0), rho_de_simplified, 'numpy')
rho_val = rho_func(2.33, UIDT_W0, UIDT_WA, 1.0)
print(f"\n  Numerical Check at z=2.33 (Ly-alpha) with UIDT params:")
print(f"  rho_DE(2.33) / rho_DE(0) = {rho_val:.4f}")

# --- 4. Visualization ---
print("\n[4] Generating Visualization...")
if not HAS_MATPLOTLIB:
    print("  Matplotlib not available; skipping plot generation.")
    print("\n--- Verification Complete (no-plot mode) ---")
    raise SystemExit(0)
plt.figure(figsize=(8, 6))

# Plot MCMC samples (thin out for file size)
plt.scatter(chain[::10, 0], chain[::10, 1], s=1, alpha=0.1, color='gray', label='Union3 MCMC Chain')

# Plot Contour Ellipses (1-sigma, 2-sigma)
confidence_ellipse = stats.multivariate_normal(mean=[mean_w0, mean_wa], cov=cov_matrix)
x = np.linspace(min(chain[:,0]), max(chain[:,0]), 100)
y = np.linspace(min(chain[:,1]), max(chain[:,1]), 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
plt.contour(X, Y, confidence_ellipse.pdf(pos), levels=[0.05, 0.32], colors=['blue', 'cyan'], linewidths=1.5, label='1/2-sigma')

# Plot UIDT Point
plt.scatter([UIDT_W0], [UIDT_WA], color='red', s=100, marker='*', label='UIDT v3.9 Prediction')
plt.text(UIDT_W0 + 0.02, UIDT_WA + 0.05, f"UIDT\n({UIDT_W0}, {UIDT_WA})", color='red')

plt.xlabel('w0 (Equation of State)')
plt.ylabel('wa (Evolution)')
plt.title(f'DESI-DR2 Integration: UIDT v3.9 vs Union3\nSigma = {mahalanobis_dist:.2f}')
plt.legend()
plt.grid(True, alpha=0.3)

plot_path = os.path.join(OUTPUT_DIR, "desi_dr2_integration.png")
plt.savefig(plot_path)
print(f"  Plot saved to: {plot_path}")

print("\n--- Verification Complete ---")
