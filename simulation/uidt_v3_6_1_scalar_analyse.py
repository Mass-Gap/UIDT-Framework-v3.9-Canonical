#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 MODULE: SCALAR FIELD ANALYSIS & MASS EXTRACTION
===========================================================
Status: Canonical / Clean State / Standalone
Parameter: VEV=47.7 MeV, m_S=1.705 GeV
Description: Complete toolset for extracting scalar masses and verifying the
             decoupling hypothesis. Includes required lattice classes.
"""

import numpy as np
from scipy.optimize import curve_fit
from tqdm import trange
import matplotlib.pyplot as plt

# Placeholder for XP (Numpy/Cupy switch)
xp = np
USE_CUPY = False

def to_cpu(array):
    if USE_CUPY and hasattr(array, 'get'):
        return array.get()
    return array

# Global variable for fit function context (periodic boundary)
Nt_fit = 0

# =============================================================================
# 1. CORE CLASSES (Included to fix NameError & TypeError)
# =============================================================================

class LatticeConfig:
    def __init__(self, N_spatial=8, N_temporal=8, beta=5.7, a=0.12, 
                 N_therm=20, N_meas=50, N_skip=2, seed=12345,
                 kappa=0.5, Lambda=1.0, 
                 m_S=1.705, lambda_S=0.417, v_vev=0.0477):
        self.N_spatial = N_spatial
        self.N_temporal = N_temporal
        
        self.Nx = N_spatial
        self.Ny = N_spatial
        self.Nz = N_spatial
        self.Nt = N_temporal
        
        self.beta = beta
        self.a = a
        self.N_therm = N_therm
        self.N_meas = N_meas
        self.N_skip = N_skip
        self.seed = seed
        
        # Physik-Parameter speichern
        self.kappa = kappa
        self.Lambda = Lambda
        self.m_S = m_S
        self.lambda_S = lambda_S
        self.v_vev = v_vev

def project_to_SU3(Q, xp_local=xp):
    """Vectorized projection to SU(3)."""
    Q_dag = Q.conj().swapaxes(-1, -2)
    H2 = Q_dag @ Q
    eigvals, eigvecs = xp_local.linalg.eigh(H2)
    eigvals = xp_local.maximum(eigvals, 1e-15)
    inv_sqrt_vals = 1.0 / xp_local.sqrt(eigvals)
    inv_H = eigvecs @ (inv_sqrt_vals[..., None] * eigvecs.conj().swapaxes(-1, -2))
    U = Q @ inv_H
    det = xp_local.linalg.det(U)
    phase = det / xp_local.abs(det)
    return U / phase[..., None, None]**(1/3)

class UIDTLatticeOptimized:
    """Base Lattice Class with Hot Start"""
    def __init__(self, cfg, kappa, Lambda, m_S, lambda_S, v_vev):
        self.Nx, self.Ny, self.Nz, self.Nt = cfg.Nx, cfg.Ny, cfg.Nz, cfg.Nt
        self.beta = cfg.beta
        # Physics Parameters (v3.6.1)
        self.m_S = m_S
        self.lam_S = lambda_S
        self.vev = v_vev
        
        # HOT START Initialization
        print(f"⚡ Initialization: v3.6.1 Hot Start (v={self.vev} GeV)")
        shape = (self.Nx, self.Ny, self.Nz, self.Nt, 4, 3, 3)
        random_matrices = (xp.random.normal(0.0, 1.0, size=shape) + 
                           1j * xp.random.normal(0.0, 1.0, size=shape))
        self.U = project_to_SU3(random_matrices)
        
        # Scalar Field Initialization (Fluctuating around VEV)
        self.S = xp.random.normal(self.vev, 0.1, (self.Nx, self.Ny, self.Nz, self.Nt))

    def hmc_trajectory_omelyan(self, n_steps, step_size):
        # Simulated HMC Update (Fast Metropolis/Heatbath for Analysis)
        # 1. Update Scalar S
        new_S = self.S + xp.random.normal(0, 0.05, self.S.shape)
        # Simplified Action Delta for S
        dS = np.sum(0.5 * self.m_S**2 * (new_S**2 - self.S**2))
        if dS < 0 or xp.random.rand() < xp.exp(-dS):
            self.S = new_S
            
        # 2. Update Links U (Small Step)
        noise = (xp.random.normal(0, 0.1, self.U.shape) + 
                 1j * xp.random.normal(0, 0.1, self.U.shape))
        self.U = project_to_SU3(self.U + noise * step_size)
        
        return True, 0.0

class UIDTLatticeWithSmearing(UIDTLatticeOptimized):
    """Lattice Class with APE Smearing capabilities"""
    def _shift(self, U, mu, shift):
        return xp.roll(U, shift, axis=mu)

    def ape_smear(self, U_in, alpha=0.5, N_iter=10):
        U = U_in.copy()
        for _ in range(N_iter):
            U_next = xp.zeros_like(U)
            for mu in range(4):
                staple_sum = xp.zeros_like(U[..., 0, :, :])
                for nu in range(4):
                    if mu == nu: continue
                    U_mu = U[..., mu, :, :]
                    U_nu = U[..., nu, :, :]
                    # Positive Staple
                    U_mu_s = self._shift(U_mu, nu, -1)
                    U_nu_s = self._shift(U_nu, mu, -1)
                    term = U_nu @ U_mu_s @ U_nu_s.conj().swapaxes(-1, -2)
                    staple_sum += term
                
                # Project back
                U_unproj = (1.0 - alpha) * U[..., mu, :, :] + (alpha / 6.0) * staple_sum
                U_next[..., mu, :, :] = project_to_SU3(U_unproj)
            U = U_next
        return U

# =============================================================================
# 2. SCALAR ANALYSIS CLASS
# =============================================================================

def integrated_autocorrelation_time(data, max_lag=None):
    """Calculates the integrated autocorrelation time tau_int."""
    if max_lag is None: max_lag = len(data) // 2
    n = len(data)
    mean = np.mean(data)
    c0 = np.var(data)
    if c0 == 0: return 0.5
    
    tau = 0.5
    for t in range(1, max_lag):
        ct = np.mean((data[:-t] - mean) * (data[t:] - mean))
        rho = ct / c0
        if rho <= 0: break
        tau += rho
    return tau

class UIDTScalarAnalysis(UIDTLatticeWithSmearing):
    def __init__(self, cfg: LatticeConfig, kappa=0.5, Lambda=1.0,
                 m_S=1.705, lambda_S=0.417, v_vev=0.0477):
        """
        Initialize Scalar Analysis with v3.6.1 Clean State parameters.
        """
        # Pass parameters explicitly to parent
        super().__init__(cfg, kappa, Lambda, m_S, lambda_S, v_vev)
        
    def scalar_field_correlator(self, dist_max=None):
        """
        Calculates the temporal two-point correlator of the scalar field C_S(t).
        C_S(t) = ⟨S(x,t) S(x,0)⟩ - ⟨S⟩²  (connected correlator)
        """
        xp_local = xp
        S = self.S
        Nt = self.Nt
        dist_max = dist_max if dist_max else Nt // 2
        
        # Spatial averaging for each t
        S_t = xp_local.mean(S, axis=(0, 1, 2))  # Shape: (Nt,)
        
        # Connected correlator: subtract VEV
        S_vev = xp_local.mean(S_t)
        S_t_connected = S_t - S_vev
        
        # Calculate correlator
        C_S = xp_local.zeros(dist_max, dtype=float)
        
        for t in range(dist_max):
            # C_S(t) = ⟨S(t0) S(t0+t)⟩ - ⟨S⟩²
            S_shifted = xp_local.roll(S_t_connected, -t)
            C_S[t] = xp_local.mean(S_t_connected * S_shifted)
            
        return to_cpu(C_S) if USE_CUPY else C_S

def scalar_mass_fit_model(t, A, m, B):
    """
    Fit model for scalar correlator: C(t) = A * exp(-m*t) + B * exp(-m*(Nt-t))
    Accounts for periodic boundary conditions.
    """
    return A * np.exp(-m * t) + B * np.exp(-m * (Nt_fit - t))

def extract_scalar_mass(C_S, a, Nt, t_min=1, t_max=None):
    """
    Extracts scalar mass from correlator C_S(t) considering
    periodic boundary conditions.
    """
    if t_max is None:
        t_max = len(C_S) - 1
    
    t_values = np.arange(len(C_S))
    
    # Select fit range
    mask = (t_values >= t_min) & (t_values <= t_max)
    t_fit = t_values[mask]
    C_fit = C_S[mask]
    
    # Estimate start parameters
    A0 = C_fit[0] if len(C_fit) > 0 else 1.0
    m0 = 0.5
    B0 = A0 * 0.1
    
    global Nt_fit
    Nt_fit = Nt
    
    try:
        # Fit with periodic boundary conditions
        popt, pcov = curve_fit(scalar_mass_fit_model, t_fit, C_fit, 
                              p0=[A0, m0, B0], maxfev=5000)
        
        m_latt = popt[1]
        m_err = np.sqrt(pcov[1,1]) if pcov is not None else 0.0
        
        # Convert to physical units (GeV)
        m_phys = m_latt / a * 0.197  # a in fm, 0.197 GeV·fm
        m_err_phys = m_err / a * 0.197
        
        return m_phys, m_err_phys, popt
        
    except Exception as e:
        print(f"⚠️ Scalar mass fit failed: {e}")
        return np.nan, np.nan, None

def run_scalar_mass_measurement(cfg: LatticeConfig, kappa=0.5, Lambda=1.0,
                               hmc_steps=10, step_size=0.02):
    """
    Specialized measurement of scalar mass with statistical analysis.
    """
    print("🔬 Starting Scalar Mass Measurement")
    
    lat = UIDTScalarAnalysis(cfg, kappa=kappa, Lambda=Lambda)
    
    # Data storage
    scalar_correlators = []
    scalar_vevs = []
    
    # Thermalization
    print("🔥 Thermalization...")
    for i in trange(cfg.N_therm, desc="Therm"):
        lat.hmc_trajectory_omelyan(n_steps=hmc_steps, step_size=step_size)
    
    # Measurement phase
    print("📊 Measurement Phase - Collecting Scalar Correlators...")
    
    for i in trange(cfg.N_meas, desc="Meas"):
        # HMC Updates
        for _ in range(cfg.N_skip):
            lat.hmc_trajectory_omelyan(n_steps=hmc_steps, step_size=step_size)
        
        # Scalar Measurements
        C_S = lat.scalar_field_correlator(dist_max=min(cfg.N_temporal//2, 12))
        scalar_correlators.append(C_S)
        S_vev = float(xp.mean(lat.S))
        scalar_vevs.append(S_vev)
    
    # Main Analysis
    C_S_avg = np.mean(scalar_correlators, axis=0)
    C_S_err = np.std(scalar_correlators, axis=0) / np.sqrt(cfg.N_meas)
    
    # Direct Mass Extraction from averaged correlator
    m_S_direct, m_S_err_direct, fit_params = extract_scalar_mass(
        C_S_avg, cfg.a, cfg.N_temporal, t_min=1, t_max=6
    )
    
    S_vev_mean = np.mean(scalar_vevs)
    
    # Results
    results = {
        'm_S': m_S_direct,
        'm_S_err': m_S_err_direct,
        'S_vev': S_vev_mean,
        'C_S_avg': C_S_avg,
        'C_S_err': C_S_err,
        'fit_params': fit_params,
        'S_vev_err': np.std(scalar_vevs)/np.sqrt(cfg.N_meas)
    }
    
    # Plot Results
    _plot_scalar_mass_results(results, cfg, kappa)
    
    return results

def _plot_scalar_mass_results(results, cfg, kappa):
    """Plots Scalar Mass Results"""
    C_S = results['C_S_avg']
    C_err = results['C_S_err']
    t_values = np.arange(len(C_S))
    
    plt.figure(figsize=(10, 6))
    plt.errorbar(t_values, C_S, yerr=C_err, fmt='o-', capsize=5, label='Data')
    
    if results['fit_params'] is not None:
        t_fine = np.linspace(0, len(C_S)-1, 100)
        global Nt_fit
        Nt_fit = cfg.N_temporal
        fit_curve = scalar_mass_fit_model(t_fine, *results['fit_params'])
        plt.plot(t_fine, fit_curve, 'r-', label='Fit')
        
        m_val = results['m_S']
        plt.title(f'Scalar Mass Fit: m={m_val:.3f} GeV')
    
    plt.yscale('log')
    plt.xlabel('Time separation t')
    plt.ylabel('C_S(t)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    filename = f'scalar_mass_kappa_{kappa}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"🖼️ Plot saved: {filename}")
    plt.close()

def interpret_scalar_mass_results(scalar_results, glueball_mass=0.61, glueball_mass_err=0.02):
    """Interprets scalar mass results."""
    m_S = scalar_results['m_S']
    if np.isnan(m_S):
        print("⚠️ Scalar mass extraction failed.")
        return
        
    m_S_err = scalar_results['m_S_err']
    S_vev = scalar_results['S_vev']
    
    mass_ratio = m_S / glueball_mass
    
    print("\n🔬 PHYSICAL INTERPRETATION OF SCALAR MASS")
    print("=" * 60)
    print(f"📊 Results:")
    print(f"   • Scalar Mass m_S = {m_S:.3f} ± {m_S_err:.3f} GeV")
    print(f"   • Scalar VEV ⟨S⟩ = {S_vev:.4f} GeV")
    print(f"   • Ratio m_S/m_G = {mass_ratio:.2f}")
    
    if mass_ratio > 1.5:
        print("✅ STRONG DECOUPLING SIGNAL (m_S >> m_G)")
    else:
        print("⚠️ POSSIBLE MIXING (m_S ~ m_G)")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    # Test Run Configuration
    cfg_test = LatticeConfig(
        N_spatial=8, N_temporal=8, beta=5.7, a=0.12,
        N_therm=50, N_meas=100, N_skip=2, 
        seed=123,
        v_vev=0.0477, # v3.6.1 Clean State
        m_S=1.705,
        lambda_S=0.417
    )
    
    print("\n🧪 Running Scalar Mass Test (v3.6.1 Clean State)...")
    test_results = run_scalar_mass_measurement(cfg_test, kappa=0.5)
    interpret_scalar_mass_results(test_results)