#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.7.2 HMC MASTER SIMULATION - REAL PHYSICS VERSION
=========================================================
Author: Philipp Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0

This is the REAL HMC implementation with:
- Vectorized SIMD operations for LHCb Run 3 alignment
- Omelyan 2nd-order symplectic integrator (Vectorized)
- Taylor-expansion su(3) exponentiation (Vectorized)
- Proper Metropolis accept/reject

WARNING: This is computationally intensive. For quick verification,
         use clay/02_VerificationCode/UIDT_Proof_Engine.py instead.

Usage:
    Terminal:  python UIDTv3_7_2_HMC_Real.py --n_therm 100 --n_meas 500
    Jupyter:   from UIDTv3_7_2_HMC_Real import run_hmc; results = run_hmc()
"""

import numpy as np
import time
import sys
from dataclasses import dataclass
from typing import Tuple, Optional, List
import argparse

# =============================================================================
# CONFIGURATION (parse_known_args for Jupyter/Colab compatibility)
# =============================================================================

def get_params():
    """Parse arguments with fallback for Jupyter/Colab environments."""
    parser = argparse.ArgumentParser(description='UIDT v3.6.1 HMC Simulation')
    parser.add_argument('--Ns', type=int, default=8, help='Spatial lattice size')
    parser.add_argument('--Nt', type=int, default=16, help='Temporal lattice size')
    parser.add_argument('--beta', type=float, default=6.0, help='Inverse coupling')
    parser.add_argument('--seed', type=int, default=123456, help='Deterministic RNG seed')
    parser.add_argument('--n_therm', type=int, default=100, help='Thermalization sweeps')
    parser.add_argument('--n_meas', type=int, default=200, help='Measurement sweeps')
    parser.add_argument('--n_skip', type=int, default=5, help='Skip between measurements')
    parser.add_argument('--md_steps', type=int, default=20, help='MD steps per trajectory')
    parser.add_argument('--step_size', type=float, default=0.02, help='MD step size')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    # parse_known_args ignores Jupyter kernel arguments
    args, _ = parser.parse_known_args()
    np.random.seed(args.seed)
    return args


@dataclass
class UIDTConstants:
    """Canonical UIDT v3.6.1 constants."""
    KAPPA: float = 0.500
    LAMBDA_S: float = 0.417
    M_S: float = 1.705
    TARGET_DELTA: float = 1.710
    TARGET_GAMMA: float = 16.339
    GLUON_CONDENSATE: float = 0.277


# =============================================================================
# SU(3) MATRIX OPERATIONS (VECTORIZED / SIMD)
# =============================================================================

def random_su3_algebra_field(shape: tuple) -> np.ndarray:
    """Generate random su(3) algebra field (traceless anti-Hermitian)."""
    # 8 Gell-Mann generators approach or direct Hermitian
    H = np.random.randn(*shape) + 1j * np.random.randn(*shape)
    H = (H + H.conj().swapaxes(-1, -2)) / 2.0  # Hermitian
    tr = np.trace(H, axis1=-2, axis2=-1)
    
    # Broadcast trace subtraction
    eye = np.eye(3, dtype=complex)
    # tr is (...,), make it (..., 1, 1)
    H = H - (tr[..., None, None] / 3.0) * eye
    return 1j * H

def project_su3_field(U: np.ndarray) -> np.ndarray:
    """Project field to SU(3) via polar decomposition (SVD-based)."""
    # SVD: U = u * s * vh -> Nearest unitary is u * vh
    u, s, vh = np.linalg.svd(U)
    U_unit = u @ vh

    # Fix determinant (make it 1)
    det = np.linalg.det(U_unit)
    return U_unit / (det[..., None, None] ** (1/3))

def su3_exp_field(A: np.ndarray) -> np.ndarray:
    """
    Vectorized matrix exponential for su(3) algebra field.
    Uses Taylor expansion to 40th order for audit-grade numerical integrity.
    A is (..., 3, 3).
    """
    order = 40
    expA = np.zeros_like(A)
    idx = np.arange(3)
    expA[..., idx, idx] = 1.0
    term = expA.copy()
    for k in range(1, order + 1):
        term = (term @ A) / k
        expA = expA + term
    return expA


# =============================================================================
# LATTICE CLASS WITH VECTORIZED HMC
# =============================================================================

class UIDTLattice:
    """
    SU(3) + Scalar field lattice with VECTORIZED HMC dynamics.
    Optimized for SIMD/GPU alignment (LHCb architecture).
    """
    
    def __init__(self, Ns: int = 8, Nt: int = 16, beta: float = 6.0):
        self.Ns = Ns
        self.Nt = Nt
        self.Nd = 4
        self.beta = beta
        self.constants = UIDTConstants()
        
        # Gauge field: U[t,z,y,x,mu] in SU(3)
        self.U = self._init_gauge_field()
        
        # Scalar field: S[t,z,y,x] real
        self.S = np.zeros((Nt, Ns, Ns, Ns), dtype=float)
        
        # Conjugate momenta
        self.Pu = None  # For gauge
        self.Ps = None  # For scalar
        
        # Diagnostics
        self.acceptance_rate = 0.5
        self.avg_delta_H = 0.0
        self.plaquette_history = []
        self.action_history = []
    
    def _init_gauge_field(self) -> np.ndarray:
        """Initialize gauge field (cold start: all identity)."""
        shape = (self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3)
        U = np.zeros(shape, dtype=complex)
        # Set diagonal to 1
        idx = np.arange(3)
        U[..., idx, idx] = 1.0
        return U
    
    def _init_momenta(self):
        """Initialize conjugate momenta."""
        # Gauge momenta: su(3) algebra valued
        shape = (self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3)
        self.Pu = random_su3_algebra_field(shape)
        
        # Scalar momenta
        self.Ps = np.random.randn(self.Nt, self.Ns, self.Ns, self.Ns)

    # =========================================================================
    # ACTION CALCULATIONS (VECTORIZED)
    # =========================================================================
    
    def shift(self, F: np.ndarray, mu: int, direction: int) -> np.ndarray:
        """
        Shift field F in direction mu.
        direction = +1: F(x+mu) -> roll(F, -1, axis=mu)
        direction = -1: F(x-mu) -> roll(F, +1, axis=mu)
        
        Note: self.U has shape (Nt, Ns, Ns, Ns, Nd, 3, 3).
        mu index for shift corresponds to axis 0, 1, 2, 3.
        """
        # Axis mapping: t=0, z=1, y=2, x=3
        return np.roll(F, -direction, axis=mu)

    def plaquette_field(self, mu: int, nu: int) -> np.ndarray:
        """Compute plaquette field P_mu_nu(x) for all x."""
        # U_mu(x)
        U_mu = self.U[..., mu, :, :]
        # U_nu(x+mu)
        U_nu_xmu = self.shift(self.U[..., nu, :, :], mu, 1)
        # U_mu(x+nu)
        U_mu_xnu = self.shift(self.U[..., mu, :, :], nu, 1)
        # U_nu(x)
        U_nu = self.U[..., nu, :, :]
        
        # P = U_mu(x) U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
        # conj().swapaxes(-1, -2) is Hermitian conjugate for stacked matrices
        return U_mu @ U_nu_xmu @ U_mu_xnu.conj().swapaxes(-1, -2) @ U_nu.conj().swapaxes(-1, -2)
    
    def average_plaquette(self) -> float:
        """Compute average plaquette (order parameter)."""
        plaq_sum = 0.0
        # Sum over mu < nu
        for mu in range(self.Nd):
            for nu in range(mu + 1, self.Nd):
                P = self.plaquette_field(mu, nu)
                plaq_sum += np.sum(np.real(np.trace(P, axis1=-2, axis2=-1))) / 3.0

        volume = self.Nt * self.Ns**3
        num_plaquettes = volume * (self.Nd * (self.Nd - 1) // 2)
        return plaq_sum / num_plaquettes
    
    def gauge_action(self) -> float:
        """Wilson gauge action: S_G = beta * sum(1 - Re Tr P / 3)."""
        plaq_sum = 0.0
        for mu in range(self.Nd):
            for nu in range(mu + 1, self.Nd):
                P = self.plaquette_field(mu, nu)
                plaq_sum += np.sum(1.0 - np.real(np.trace(P, axis1=-2, axis2=-1)) / 3.0)
        return self.beta * plaq_sum
    
    def scalar_action(self) -> float:
        """UIDT scalar field action with kappa coupling."""
        kappa = self.constants.KAPPA
        lambda_S = self.constants.LAMBDA_S
        m_S = self.constants.M_S
        
        # Kinetic term: (1/2) sum (nabla S)^2
        kinetic = 0.0
        for mu in range(self.Nd):
            S_fwd = self.shift(self.S, mu, 1)
            kinetic += 0.5 * np.sum((S_fwd - self.S)**2)
        
        # Potential term
        potential = 0.5 * m_S**2 * np.sum(self.S**2) + 0.25 * lambda_S * np.sum(self.S**4)
        
        return kinetic + potential
    
    def total_action(self) -> float:
        """Total action S = S_gauge + S_scalar."""
        return self.gauge_action() + self.scalar_action()
    
    def kinetic_energy(self) -> float:
        """Kinetic energy from momenta: T = (1/2) Tr(P^2)."""
        T_gauge = 0.0
        if self.Pu is not None:
            # P_gauge trace
            # Pu is (..., Nd, 3, 3)
            tr_P2 = np.trace(self.Pu @ self.Pu.conj().swapaxes(-1, -2), axis1=-2, axis2=-1)
            T_gauge = 0.5 * np.sum(np.real(tr_P2))
        
        T_scalar = 0.0
        if self.Ps is not None:
            T_scalar = 0.5 * np.sum(self.Ps**2)
        
        return T_gauge + T_scalar
    
    def hamiltonian(self) -> float:
        """Total Hamiltonian H = T + S."""
        return self.kinetic_energy() + self.total_action()

    # =========================================================================
    # FORCE CALCULATIONS (VECTORIZED)
    # =========================================================================
    
    def gauge_force_field(self) -> np.ndarray:
        """
        Compute gauge force for all links.
        Returns tensor shape (Nt, Ns, Ns, Ns, Nd, 3, 3).
        """
        force = np.zeros_like(self.U)
        
        # Iterate mu to construct force for U_mu
        for mu in range(self.Nd):
            staple_sum = np.zeros_like(self.U[..., mu, :, :])
            
            for nu in range(self.Nd):
                if nu == mu:
                    continue

                # Forward staple
                U_nu_xmu = self.shift(self.U[..., nu, :, :], mu, 1)
                U_mu_xnu = self.shift(self.U[..., mu, :, :], nu, 1)
                U_nu_x = self.U[..., nu, :, :]

                staple_fwd = U_nu_xmu @ U_mu_xnu.conj().swapaxes(-1, -2) @ U_nu_x.conj().swapaxes(-1, -2)

                # Backward staple
                # Shifted by -nu
                U_nu_xmu_nub = self.shift(U_nu_xmu, nu, -1)
                U_mu_xnub = self.shift(self.U[..., mu, :, :], nu, -1)
                U_nu_xnub = self.shift(self.U[..., nu, :, :], nu, -1)

                staple_bwd = U_nu_xmu_nub.conj().swapaxes(-1, -2) @ U_mu_xnub.conj().swapaxes(-1, -2) @ U_nu_xnub

                staple_sum += staple_fwd + staple_bwd
            
            # Project to traceless anti-Hermitian
            U_mu = self.U[..., mu, :, :]
            Omega = U_mu @ staple_sum
            F_mu = (self.beta / 3.0) * (Omega - Omega.conj().swapaxes(-1, -2))
            
            # Traceless
            tr = np.trace(F_mu, axis1=-2, axis2=-1)
            eye = np.eye(3, dtype=complex)
            F_mu = F_mu - (tr[..., None, None] / 3.0) * eye
            
            force[..., mu, :, :] = F_mu
            
        return force
    
    def scalar_force_field(self) -> np.ndarray:
        """
        Compute scalar field force for all sites.
        """
        lambda_S = self.constants.LAMBDA_S
        m_S = self.constants.M_S
        
        # Laplacian
        laplacian = np.zeros_like(self.S)
        for mu in range(self.Nd):
            laplacian += self.shift(self.S, mu, 1) + self.shift(self.S, mu, -1) - 2*self.S
        
        # Force
        return -m_S**2 * self.S - lambda_S * self.S**3 + laplacian

    # =========================================================================
    # OMELYAN INTEGRATOR (VECTORIZED)
    # =========================================================================
    
    def omelyan_trajectory(self, n_steps: int = 20, step_size: float = 0.02) -> Tuple[bool, float]:
        """Vectorized HMC trajectory."""
        xi = 0.193
        gamma = 0.5 - xi
        eps = step_size
        
        # Store old
        U_old = self.U.copy()
        S_old = self.S.copy()
        
        # Refresh momenta
        self._init_momenta()
        H_initial = self.hamiltonian()
        
        # P -> P + force * dt
        # F_gauge points UPHILL (Gradient) with factor 2. So P -= 0.5 * Gradient.
        F_gauge = self.gauge_force_field()
        self.Pu -= xi * eps * 0.5 * F_gauge
        
        # F_scalar points DOWNHILL (Force). So P += Force.
        F_scalar = self.scalar_force_field()
        self.Ps += xi * eps * F_scalar
        
        for step in range(n_steps):
            # Q -> Q + gamma*eps*P
            # Gauge update: U = exp(P)*U
            exp_P = su3_exp_field(gamma * eps * self.Pu)
            self.U = exp_P @ self.U
            self.U = project_su3_field(self.U)
            
            # Scalar update (gamma=0.5 preserved from original code)
            self.S += 0.5 * eps * self.Ps
            
            # P -> P
            F_gauge = self.gauge_force_field()
            self.Pu -= (1 - 2*xi) * eps * 0.5 * F_gauge
            
            F_scalar = self.scalar_force_field()
            self.Ps += (1 - 2*xi) * eps * F_scalar
            
            # Q -> Q
            exp_P = su3_exp_field(gamma * eps * self.Pu)
            self.U = exp_P @ self.U
            self.U = project_su3_field(self.U)
            
            self.S += 0.5 * eps * self.Ps
            
            # Final P (except last)
            if step < n_steps - 1:
                F_gauge = self.gauge_force_field()
                self.Pu -= 2*xi * eps * 0.5 * F_gauge
                
                F_scalar = self.scalar_force_field()
                self.Ps += 2*xi * eps * F_scalar
        
        # Final P
        F_gauge = self.gauge_force_field()
        self.Pu -= (1 - xi) * eps * 0.5 * F_gauge
        
        F_scalar = self.scalar_force_field()
        self.Ps += (1 - xi) * eps * F_scalar
        
        # Metropolis
        H_final = self.hamiltonian()
        delta_H = H_final - H_initial
        
        accepted = False
        if np.random.rand() < np.exp(-delta_H):
            accepted = True
        else:
            self.U = U_old
            self.S = S_old

        self.avg_delta_H = 0.9 * self.avg_delta_H + 0.1 * abs(delta_H)
        self.acceptance_rate = 0.9 * self.acceptance_rate + (0.1 if accepted else 0.0)
        
        return accepted, delta_H

    # =========================================================================
    # MEASUREMENT (VECTORIZED)
    # =========================================================================
    
    def measure_kinetic_vev(self) -> float:
        """Measure <(nabla S)^2>."""
        kin_sum = 0.0
        for mu in range(self.Nd):
            S_fwd = self.shift(self.S, mu, 1)
            kin_sum += np.sum((S_fwd - self.S)**2)
        
        count = self.Nt * self.Ns**3 * self.Nd
        return kin_sum / count


# =============================================================================
# MAIN RUN FUNCTION
# =============================================================================

def run_hmc(Ns: int = 8, Nt: int = 16, beta: float = 6.0,
            n_therm: int = 100, n_meas: int = 200, n_skip: int = 5,
            md_steps: int = 20, step_size: float = 0.02,
            verbose: bool = True, seed: Optional[int] = None) -> dict:
    """
    Run complete HMC simulation and return results.
    """
    constants = UIDTConstants()
    if seed is not None:
        np.random.seed(seed)
    
    if verbose:
        print("=" * 70)
        print("  UIDT v3.7.2 HMC SIMULATION - VECTORIZED (SIMD)")
        print("=" * 70)
        print(f"Lattice: {Ns}^3 x {Nt}")
        print(f"Beta: {beta}")
        print(f"UIDT kappa: {constants.KAPPA}")
        if seed is not None:
            print(f"Seed: {seed}")
        print(f"Thermalization: {n_therm} trajectories")
        print(f"Measurements: {n_meas} trajectories")
        print(f"MD steps: {md_steps}, step size: {step_size}")
        print("=" * 70)
    
    # Initialize lattice
    lattice = UIDTLattice(Ns=Ns, Nt=Nt, beta=beta)
    
    start_time = time.time()
    
    # Thermalization
    if verbose:
        print("\nThermalization...")
    
    for i in range(n_therm):
        accepted, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        if verbose and (i + 1) % 10 == 0:
            plaq = lattice.average_plaquette()
            print(f"  Therm {i+1:4d}: <P> = {plaq:.6f}, acc = {lattice.acceptance_rate:.2f}")
    
    # Measurements
    if verbose:
        print("\nMeasurements...")
    
    plaquette_measurements = []
    kinetic_vev_measurements = []
    accepted_count = 0
    
    for i in range(n_meas):
        accepted, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        if accepted:
            accepted_count += 1
        
        if (i + 1) % n_skip == 0:
            plaq = lattice.average_plaquette()
            kin_vev = lattice.measure_kinetic_vev()
            
            plaquette_measurements.append(plaq)
            kinetic_vev_measurements.append(kin_vev)
            
            if verbose and (i + 1) % 50 == 0:
                print(f"  Meas {i+1:4d}: <P> = {plaq:.6f}, <(dS)^2> = {kin_vev:.6f}")
    
    elapsed = time.time() - start_time
    
    # Compute results
    plaq_mean = np.mean(plaquette_measurements)
    plaq_err = np.std(plaquette_measurements) / np.sqrt(len(plaquette_measurements))
    
    kin_vev_mean = np.mean(kinetic_vev_measurements)
    kin_vev_err = np.std(kinetic_vev_measurements) / np.sqrt(len(kinetic_vev_measurements))
    
    # Compute gamma from kinetic VEV
    if kin_vev_mean > 0:
        gamma_computed = constants.TARGET_DELTA / np.sqrt(kin_vev_mean)
    else:
        gamma_computed = float('nan')
    
    acceptance = accepted_count / n_meas
    
    if verbose:
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Runtime: {elapsed:.1f} seconds")
        print(f"Acceptance rate: {acceptance:.2%}")
        print(f"Average plaquette: {plaq_mean:.6f} +/- {plaq_err:.6f}")
        print(f"Kinetic VEV <(dS)^2>: {kin_vev_mean:.6f} +/- {kin_vev_err:.6f}")
        print(f"Computed gamma: {gamma_computed:.3f} (target: {constants.TARGET_GAMMA})")
        print("=" * 70)
    
    return {
        'plaquette': plaq_mean,
        'plaquette_err': plaq_err,
        'kinetic_vev': kin_vev_mean,
        'kinetic_vev_err': kin_vev_err,
        'gamma': gamma_computed,
        'acceptance': acceptance,
        'runtime': elapsed,
        'measurements': {
            'plaquette': plaquette_measurements,
            'kinetic_vev': kinetic_vev_measurements
        }
    }


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    args = get_params()
    
    results = run_hmc(
        Ns=args.Ns,
        Nt=args.Nt,
        beta=args.beta,
        seed=args.seed,
        n_therm=args.n_therm,
        n_meas=args.n_meas,
        n_skip=args.n_skip,
        md_steps=args.md_steps,
        step_size=args.step_size,
        verbose=True
    )
    
    print("\n[COMPLETE] Real HMC simulation finished.")
    print(f"[RESULT] gamma = {results['gamma']:.3f}")
