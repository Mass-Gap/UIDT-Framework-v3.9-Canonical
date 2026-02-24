import sys
import os
import numpy as np
import time
from scipy.linalg import expm

# Add the path to the simulation script
sys.path.append(os.path.abspath("clay-submission/05_LatticeSimulation"))

# Import necessary classes and functions
try:
    from UIDTv3_7_2_HMC_Real import UIDTLattice, UIDTConstants, run_hmc, random_su3_algebra, project_su3, random_su3
except ImportError:
    print("Error: Could not import UIDTv3_7_2_HMC_Real.py. Make sure the path is correct.")
    sys.exit(1)

# Use scipy expm for correctness
def su3_exp(X):
    return expm(X)

import UIDTv3_7_2_HMC_Real
UIDTv3_7_2_HMC_Real.su3_exp = su3_exp

# Constants for Metropolis
METROPOLIS_STEP_SCALE_GAUGE = 0.05  # Reduced step size
METROPOLIS_STEP_SCALE_SCALAR = 0.5

class MetropolisLattice(UIDTLattice):
    """
    Subclass of UIDTLattice to add Metropolis-Hastings updates.
    """
    def __init__(self, Ns=8, Nt=16, beta=6.0):
        super().__init__(Ns, Nt, beta)
        self.metropolis_acceptance_gauge = 0.0
        self.metropolis_acceptance_scalar = 0.0
        self.metropolis_steps_gauge = 0
        self.metropolis_steps_scalar = 0
        # Add noise to initial configuration
        self.add_noise()

    def add_noise(self):
        print("Adding noise to initial configuration...")
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            rand_alg = random_su3_algebra() * 0.1
            self.U[idx] = su3_exp(rand_alg) @ self.U[idx]
            self.U[idx] = project_su3(self.U[idx])

    def local_gauge_action_change(self, U_new, t, z, y, x, mu):
        # Calculate sum of staples (6 staples)
        staple_sum = np.zeros((3, 3), dtype=complex)

        for nu in range(self.Nd):
            if nu == mu:
                continue

            # Forward staple
            shifts_mu = [0, 0, 0, 0]
            shifts_mu[mu] = 1
            t_mu = (t + shifts_mu[0]) % self.Nt
            z_mu = (z + shifts_mu[1]) % self.Ns
            y_mu = (y + shifts_mu[2]) % self.Ns
            x_mu = (x + shifts_mu[3]) % self.Ns

            shifts_nu = [0, 0, 0, 0]
            shifts_nu[nu] = 1
            t_nu = (t + shifts_nu[0]) % self.Nt
            z_nu = (z + shifts_nu[1]) % self.Ns
            y_nu = (y + shifts_nu[2]) % self.Ns
            x_nu = (x + shifts_nu[3]) % self.Ns

            U_nu_xmu = self.U[t_mu, z_mu, y_mu, x_mu, nu]
            U_mu_xnu = self.U[t_nu, z_nu, y_nu, x_nu, mu]
            U_nu_x = self.U[t, z, y, x, nu]

            staple_fwd = U_nu_xmu @ U_mu_xnu.conj().T @ U_nu_x.conj().T

            # Backward staple
            shifts_nu_back = [0, 0, 0, 0]
            shifts_nu_back[nu] = -1
            t_nub = (t + shifts_nu_back[0]) % self.Nt
            z_nub = (z + shifts_nu_back[1]) % self.Ns
            y_nub = (y + shifts_nu_back[2]) % self.Ns
            x_nub = (x + shifts_nu_back[3]) % self.Ns

            t_mu_nub = (t_mu + shifts_nu_back[0]) % self.Nt
            z_mu_nub = (z_mu + shifts_nu_back[1]) % self.Ns
            y_mu_nub = (y_mu + shifts_nu_back[2]) % self.Ns
            x_mu_nub = (x_mu + shifts_nu_back[3]) % self.Ns

            U_nu_xmu_nub = self.U[t_mu_nub, z_mu_nub, y_mu_nub, x_mu_nub, nu]
            U_mu_xnub = self.U[t_nub, z_nub, y_nub, x_nub, mu]
            U_nu_xnub = self.U[t_nub, z_nub, y_nub, x_nub, nu]

            staple_bwd = U_nu_xmu_nub.conj().T @ U_mu_xnub.conj().T @ U_nu_xnub

            staple_sum += staple_fwd + staple_bwd

        U_old = self.U[t, z, y, x, mu]

        # Staple sum is path x+mu -> x.
        # Plaquette is U_mu(x) * Staple.
        # Trace of closed loop: Tr(U * Staple)
        term_new = np.real(np.trace(U_new @ staple_sum))
        term_old = np.real(np.trace(U_old @ staple_sum))

        delta_S = - (self.beta / 3.0) * (term_new - term_old)

        return delta_S

    def local_scalar_action_change(self, S_new, t, z, y, x):
        S_old = self.S[t, z, y, x]
        kinetic_change = 0.0
        for mu in range(self.Nd):
            shifts_fwd = [0, 0, 0, 0]
            shifts_fwd[mu] = 1
            t_f = (t + shifts_fwd[0]) % self.Nt
            z_f = (z + shifts_fwd[1]) % self.Ns
            y_f = (y + shifts_fwd[2]) % self.Ns
            x_f = (x + shifts_fwd[3]) % self.Ns
            S_fwd = self.S[t_f, z_f, y_f, x_f]
            term_fwd_new = 0.5 * (S_fwd - S_new)**2
            term_fwd_old = 0.5 * (S_fwd - S_old)**2
            shifts_bwd = [0, 0, 0, 0]
            shifts_bwd[mu] = -1
            t_b = (t + shifts_bwd[0]) % self.Nt
            z_b = (z + shifts_bwd[1]) % self.Ns
            y_b = (y + shifts_bwd[2]) % self.Ns
            x_b = (x + shifts_bwd[3]) % self.Ns
            S_bwd = self.S[t_b, z_b, y_b, x_b]
            term_bwd_new = 0.5 * (S_new - S_bwd)**2
            term_bwd_old = 0.5 * (S_old - S_bwd)**2
            kinetic_change += (term_fwd_new - term_fwd_old) + (term_bwd_new - term_bwd_old)

        m_S = self.constants.M_S
        lambda_S = self.constants.LAMBDA_S
        pot_new = 0.5 * m_S**2 * S_new**2 + 0.25 * lambda_S * S_new**4
        pot_old = 0.5 * m_S**2 * S_old**2 + 0.25 * lambda_S * S_old**4

        return kinetic_change + (pot_new - pot_old)

    def metropolis_sweep(self):
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t, z, y, x, mu = idx
            rand_alg = random_su3_algebra() * METROPOLIS_STEP_SCALE_GAUGE
            M = su3_exp(rand_alg)
            U_old = self.U[idx]
            U_new = M @ U_old
            U_new = project_su3(U_new)
            delta_S = self.local_gauge_action_change(U_new, t, z, y, x, mu)
            if delta_S <= 0 or np.random.rand() < np.exp(-delta_S):
                self.U[idx] = U_new
                self.metropolis_acceptance_gauge += 1.0
            self.metropolis_steps_gauge += 1

        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t, z, y, x = idx
            delta = (np.random.rand() - 0.5) * 2.0 * METROPOLIS_STEP_SCALE_SCALAR
            S_old = self.S[idx]
            S_new = S_old + delta
            delta_S = self.local_scalar_action_change(S_new, t, z, y, x)
            if delta_S <= 0 or np.random.rand() < np.exp(-delta_S):
                self.S[idx] = S_new
                self.metropolis_acceptance_scalar += 1.0
            self.metropolis_steps_scalar += 1

def run_metropolis(Ns=8, Nt=16, beta=6.0, n_therm=100, n_meas=200, n_skip=5, verbose=True):
    lattice = MetropolisLattice(Ns, Nt, beta)
    if verbose:
        print("Thermalization...")
    for i in range(n_therm):
        lattice.metropolis_sweep()
        if (i+1) % 10 == 0:
             print(f"  Therm {i+1}/{n_therm}")
    if verbose:
        print("Measurements...")
    plaquette_measurements = []
    for i in range(n_meas):
        lattice.metropolis_sweep()
        if (i+1) % n_skip == 0:
            plaq = lattice.average_plaquette()
            plaquette_measurements.append(plaq)
            if verbose and (i+1) % 10 == 0:
                print(f"  Meas {i+1}/{n_meas}: <P> = {plaq:.6f}")
    gauge_acc = lattice.metropolis_acceptance_gauge / lattice.metropolis_steps_gauge
    scalar_acc = lattice.metropolis_acceptance_scalar / lattice.metropolis_steps_scalar
    if verbose:
        print(f"Gauge Acceptance: {gauge_acc:.2%}")
        print(f"Scalar Acceptance: {scalar_acc:.2%}")
    return plaquette_measurements

def compute_autocorrelation(series):
    n = len(series)
    if n < 2: return 0.0
    mean = np.mean(series)
    var = np.var(series)
    if var < 1e-12: return 0.0 # Treat constant series as tau=0
    rho = []
    for t in range(n // 2):
        cov = 0.0
        for i in range(n - t):
            cov += (series[i] - mean) * (series[i+t] - mean)
        cov /= (n - t)
        rho.append(cov / var)
    tau = 0.5
    for t in range(1, len(rho)):
        if rho[t] <= 0: break
        tau += rho[t]
    return tau

if __name__ == "__main__":
    NS = 2
    NT = 4
    BETA = 6.0

    # HMC - Reduced Step Size
    print("\nRunning HMC (Tiny Lattice)...")
    hmc_results = run_hmc(Ns=NS, Nt=NT, beta=BETA, n_therm=20, n_meas=50, n_skip=1, md_steps=2, step_size=0.01, verbose=True)
    hmc_plaq = hmc_results['measurements']['plaquette']
    tau_hmc = compute_autocorrelation(hmc_plaq)

    # Metropolis
    print("\nRunning Metropolis (Tiny Lattice)...")
    metro_plaq = run_metropolis(Ns=NS, Nt=NT, beta=BETA, n_therm=20, n_meas=50, n_skip=1, verbose=True)
    tau_metro = compute_autocorrelation(metro_plaq)

    print("\n" + "="*40)
    print("ERGODICITY CHECK RESULTS")
    print("="*40)
    print(f"{'Algorithm':<15} | {'Tau (steps)':<10} | {'Mean Plaq':<10}")
    print("-" * 40)
    print(f"{'HMC':<15} | {tau_hmc:<10.2f} | {np.mean(hmc_plaq):<10.4f}")
    print(f"{'Metropolis':<15} | {tau_metro:<10.2f} | {np.mean(metro_plaq):<10.4f}")
    print("="*40)
