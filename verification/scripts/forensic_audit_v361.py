import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
import os

def run_forensics(file_path):
    if not os.path.exists(file_path):
        print(f"Fehler: Datei {file_path} nicht gefunden.")
        return

    print(f"Lese Daten für Forensik-Test ein aus: {file_path}")
    # We read only a subset for faster forensics if needed, but 100k is fine for pandas
    df = pd.read_csv(file_path)
    
    print("\n--- 1. AUTOKORRELATIONS-TEST (Lag-1) ---")
    acf_gamma = df['gamma'].autocorr(lag=1)
    acf_delta = df['Delta'].autocorr(lag=1)
    print(f"Autokorrelation gamma: {acf_gamma:.5f}")
    print(f"Autokorrelation Delta: {acf_delta:.5f}")
    
    if abs(acf_gamma) < 0.05:
        print("-> STATUS: FAILED (No autocorrelation. Likely independent random data.)")
    elif abs(acf_gamma) > 0.99:
        print("-> STATUS: WARNING (High autocorrelation. Chain might be frozen.)")
    else:
        print("-> STATUS: PASSED (Healthy MCMC signature detected.)")

    print("\n--- 2. PHYSIK-CONSTRAINT-TEST (5k^2 = 3L_S) ---")
    # Residual check
    residuals = np.abs(5 * (df['kappa']**2) - 3 * df['lambda_S'])
    max_res = residuals.max()
    mean_res = residuals.mean()
    print(f"Maximaler Constraint-Fehler: {max_res:.20e}")
    print(f"Mittlerer Constraint-Fehler: {mean_res:.20e}")
    
    if max_res > 1e-14:
        print("-> STATUS: FAILED (Constraint violation detected! Category [A] non-compliant.)")
    else:
        print("-> STATUS: PASSED (Constraint exact to < 1e-14.)")

    print("\n--- 3. STATISTISCHER ALIGNMENT-TEST (Means vs v3.6.1 Canonical) ---")
    m_gamma = df['gamma'].mean()
    m_delta = df['Delta'].mean()
    m_kappa = df['kappa'].mean()
    
    print(f"Mean gamma: {m_gamma:.5f} (Target: 16.339)")
    print(f"Mean Delta: {m_delta:.5f} (Target: 1.710)")
    print(f"Mean kappa: {m_kappa:.5f} (Target: 0.500)")
    
    err_gamma = abs(m_gamma - 16.339)
    if err_gamma < 0.01:
         print("-> STATUS: PASSED (Statistical alignment OK.)")
    else:
         print("-> STATUS: WARNING (Statistical drift detected.)")

    print("\n--- 4. VERTEILUNGS-SIGNATUR ---")
    g_skew = skew(df['gamma'])
    g_kurt = kurtosis(df['gamma'])
    print(f"Schiefe (Skewness): {g_skew:.5f}")
    print(f"Wölbung (Kurtosis): {g_kurt:.5f}")
    
    if abs(g_skew) < 0.0001:
        print("-> STATUS: WARNING (Symmetry is too perfect. Might be synthetic.)")
    else:
        print("-> STATUS: PASSED (Natural asymmetry detected.)")

if __name__ == "__main__":
    path = r'verification/data/UIDT_MonteCarlo_samples_100k_v361.csv'
    run_forensics(path)
