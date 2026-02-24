#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 HMC MASTER SIMULATION - REAL PHYSICS VERSION
=========================================================
Author: Philipp Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0

This is the REAL HMC implementation with:
- Omelyan 2nd-order symplectic integrator (NOT placeholder)
- Actual molecular dynamics evolution
- Real force calculations from gauge + scalar action
- Proper Metropolis accept/reject

WARNING: This is computationally intensive. For quick verification,
         use clay/02_VerificationCode/UIDT_Proof_Engine.py instead.

Usage:
    Terminal:  python UIDTv3_6_1_HMC_Real.py --n_therm 100 --n_meas 500
    Jupyter:   from UIDTv3_6_1_HMC_Real import run_hmc; results = run_hmc()
"""

import numpy as np
import time
import sys
from dataclasses import dataclass
from typing import Tuple, Optional, List, Any
import argparse
from mpmath import mp

# Force precision locally (Anti-Tampering Rule)
mp.dps = 80

# =============================================================================
# CONFIGURATION (parse_known_args for Jupyter/Colab compatibility)
# =============================================================================

def get_params():
    """Parse arguments with fallback for Jupyter/Colab environments."""
    parser = argparse.ArgumentParser(description='UIDT v3.6.1 HMC Simulation')
    parser.add_argument('--Ns', type=int, default=8, help='Spatial lattice size')
    parser.add_argument('--Nt', type=int, default=16, help='Temporal lattice size')
    parser.add_argument('--beta', type=float, default=6.0, help='Inverse coupling')
    parser.add_argument('--n_therm', type=int, default=100, help='Thermalization sweeps')
    parser.add_argument('--n_meas', type=int, default=200, help='Measurement sweeps')
    parser.add_argument('--n_skip', type=int, default=5, help='Skip between measurements')
    parser.add_argument('--md_steps', type=int, default=20, help='MD steps per trajectory')
    parser.add_argument('--step_size', type=float, default=0.02, help='MD step size')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    # parse_known_args ignores Jupyter kernel arguments
    args, _ = parser.parse_known_args()
    return args


@dataclass
class UIDTConstants:
    """Canonical UIDT v3.6.1 constants."""
    # High-precision initialization via mpmath strings
    KAPPA: Any = mp.mpf('0.500')
    LAMBDA_S: Any = mp.mpf('0.417')
    M_S: Any = mp.mpf('1.705')
    TARGET_DELTA: Any = mp.mpf('1.710035046742')  # Precise Geometric Operator value
    TARGET_GAMMA: Any = mp.mpf('16.339')
    GLUON_CONDENSATE: Any = mp.mpf('0.277')


# =============================================================================
# SU(3) MATRIX OPERATIONS (REAL PHYSICS)
# =============================================================================

def random_su3() -> np.ndarray:
    """Generate random SU(3) matrix via QR decomposition."""
    A = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    Q, R = np.linalg.qr(A)
    # Ensure det(Q) = 1
    det_Q = np.linalg.det(Q)
    Q = Q / (det_Q ** (1/3))
    return Q

def random_su3_algebra() -> np.ndarray:
    """Generate random element of su(3) algebra (traceless anti-Hermitian)."""
    # 8 Gell-Mann generators
    coeffs = np.random.randn(8)
    A = np.zeros((3, 3), dtype=complex)
    
    # Simplified: traceless Hermitian, then multiply by i
    H = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    H = (H + H.conj().T) / 2  # Hermitian
    H = H - np.trace(H) / 3 * np.eye(3)  # Traceless
    return 1j * H

def project_su3(U: np.ndarray) -> np.ndarray:
    """Project matrix to SU(3) via polar decomposition."""
    # SVD-based projection
    Udet = U / (np.linalg.det(U) ** (1/3))
    # Reunitarize
    Q, R = np.linalg.qr(Udet)
    det_Q = np.linalg.det(Q)
    return Q / (det_Q ** (1/3))

def su3_exp(X: np.ndarray) -> np.ndarray:
    """Matrix exponential for su(3) algebra element."""
    from scipy.linalg import expm
    return expm(X)


# =============================================================================
# LATTICE CLASS WITH REAL HMC
# =============================================================================

class UIDTLattice:
    """
    SU(3) + Scalar field lattice with REAL HMC dynamics.
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
        U = np.zeros((self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3), dtype=complex)
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        for mu in range(self.Nd):
                            U[t, z, y, x, mu] = np.eye(3, dtype=complex)
        return U
    
    def _init_momenta(self):
        """Initialize conjugate momenta from Gaussian distribution."""
        # Gauge momenta: su(3) algebra valued
        shape = (self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3)
        self.Pu = np.zeros(shape, dtype=complex)
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            self.Pu[idx] = random_su3_algebra()
        
        # Scalar momenta
        self.Ps = np.random.randn(self.Nt, self.Ns, self.Ns, self.Ns)

    # =========================================================================
    # ACTION CALCULATIONS (REAL PHYSICS)
    # =========================================================================
    
    def plaquette(self, t: int, z: int, y: int, x: int, mu: int, nu: int) -> np.ndarray:
        """Compute single plaquette U_mu(x) U_nu(x+mu) U_mu^dag(x+nu) U_nu^dag(x)."""
        # Get link variables with periodic boundary conditions
        U_mu_x = self.U[t, z, y, x, mu]
        
        # Shift in mu direction
        shifts = [0, 0, 0, 0]
        shifts[mu] = 1
        t2 = (t + shifts[0]) % self.Nt
        z2 = (z + shifts[1]) % self.Ns
        y2 = (y + shifts[2]) % self.Ns
        x2 = (x + shifts[3]) % self.Ns
        U_nu_xmu = self.U[t2, z2, y2, x2, nu]
        
        # Shift in nu direction
        shifts = [0, 0, 0, 0]
        shifts[nu] = 1
        t3 = (t + shifts[0]) % self.Nt
        z3 = (z + shifts[1]) % self.Ns
        y3 = (y + shifts[2]) % self.Ns
        x3 = (x + shifts[3]) % self.Ns
        U_mu_xnu = self.U[t3, z3, y3, x3, mu]
        
        U_nu_x = self.U[t, z, y, x, nu]
        
        return U_mu_x @ U_nu_xmu @ U_mu_xnu.conj().T @ U_nu_x.conj().T
    
    def average_plaquette(self) -> float:
        """Compute average plaquette (order parameter)."""
        total = 0.0
        count = 0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        for mu in range(self.Nd):
                            for nu in range(mu + 1, self.Nd):
                                P = self.plaquette(t, z, y, x, mu, nu)
                                total += np.real(np.trace(P)) / 3.0
                                count += 1
        return total / count
    
    def gauge_action(self) -> float:
        """Wilson gauge action: S_G = beta * sum(1 - Re Tr P / 3)."""
        plaq_sum = 0.0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        for mu in range(self.Nd):
                            for nu in range(mu + 1, self.Nd):
                                P = self.plaquette(t, z, y, x, mu, nu)
                                plaq_sum += 1.0 - np.real(np.trace(P)) / 3.0
        return self.beta * plaq_sum
    
    def scalar_action(self) -> float:
        """UIDT scalar field action with kappa coupling."""
        kappa = self.constants.KAPPA
        lambda_S = self.constants.LAMBDA_S
        m_S = self.constants.M_S
        
        # Kinetic term: (1/2) sum (nabla S)^2
        kinetic = 0.0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        S_here = self.S[t, z, y, x]
                        for mu in range(self.Nd):
                            shifts = [0, 0, 0, 0]
                            shifts[mu] = 1
                            t2 = (t + shifts[0]) % self.Nt
                            z2 = (z + shifts[1]) % self.Ns
                            y2 = (y + shifts[2]) % self.Ns
                            x2 = (x + shifts[3]) % self.Ns
                            S_fwd = self.S[t2, z2, y2, x2]
                            kinetic += 0.5 * (S_fwd - S_here)**2
        
        # Potential term: (m^2/2) S^2 + (lambda/4) S^4
        potential = 0.0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        S_here = self.S[t, z, y, x]
                        potential += 0.5 * m_S**2 * S_here**2
                        potential += 0.25 * lambda_S * S_here**4
        
        return kinetic + potential
    
    def total_action(self) -> float:
        """Total action S = S_gauge + S_scalar."""
        return self.gauge_action() + self.scalar_action()
    
    def kinetic_energy(self) -> float:
        """Kinetic energy from momenta: T = (1/2) Tr(P^2)."""
        T_gauge = 0.0
        if self.Pu is not None:
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                T_gauge += 0.5 * np.real(np.trace(self.Pu[idx] @ self.Pu[idx].conj().T))
        
        T_scalar = 0.0
        if self.Ps is not None:
            T_scalar = 0.5 * np.sum(self.Ps**2)
        
        return T_gauge + T_scalar
    
    def hamiltonian(self) -> float:
        """Total Hamiltonian H = T + S."""
        return self.kinetic_energy() + self.total_action()

    # =========================================================================
    # FORCE CALCULATIONS (DERIVATIVES OF ACTION)
    # =========================================================================
    
    def gauge_force(self, t: int, z: int, y: int, x: int, mu: int) -> np.ndarray:
        """
        Compute gauge force at site (t,z,y,x,mu).
        F = -dS/dA = (beta/3) * sum_nu [staple(mu,nu)]_TA
        where _TA means traceless anti-Hermitian projection.
        """
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
            
            # Backward staple (similar construction)
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
        
        # Project to traceless anti-Hermitian
        U_mu_x = self.U[t, z, y, x, mu]
        Omega = U_mu_x @ staple_sum
        F = (self.beta / 3.0) * (Omega - Omega.conj().T)
        F = F - np.trace(F) / 3.0 * np.eye(3)
        
        return F
    
    def scalar_force(self, t: int, z: int, y: int, x: int) -> float:
        """
        Compute scalar field force at site.
        F_S = -dS/dS = -m^2 S - lambda S^3 + Laplacian(S)
        """
        kappa = self.constants.KAPPA
        lambda_S = self.constants.LAMBDA_S
        m_S = self.constants.M_S
        
        S_here = self.S[t, z, y, x]
        
        # Laplacian: sum over neighbors
        laplacian = 0.0
        for mu in range(self.Nd):
            shifts_fwd = [0, 0, 0, 0]
            shifts_fwd[mu] = 1
            t_f = (t + shifts_fwd[0]) % self.Nt
            z_f = (z + shifts_fwd[1]) % self.Ns
            y_f = (y + shifts_fwd[2]) % self.Ns
            x_f = (x + shifts_fwd[3]) % self.Ns
            
            shifts_bwd = [0, 0, 0, 0]
            shifts_bwd[mu] = -1
            t_b = (t + shifts_bwd[0]) % self.Nt
            z_b = (z + shifts_bwd[1]) % self.Ns
            y_b = (y + shifts_bwd[2]) % self.Ns
            x_b = (x + shifts_bwd[3]) % self.Ns
            
            laplacian += self.S[t_f, z_f, y_f, x_f] + self.S[t_b, z_b, y_b, x_b] - 2*S_here
        
        # Force = -dV/dS + laplacian
        force = -m_S**2 * S_here - lambda_S * S_here**3 + laplacian
        
        return force

    # =========================================================================
    # OMELYAN 2ND ORDER INTEGRATOR (REAL IMPLEMENTATION)
    # =========================================================================
    
    def omelyan_trajectory(self, n_steps: int = 20, step_size: float = 0.02) -> Tuple[bool, float]:
        """
        Execute one HMC trajectory using Omelyan 2nd-order integrator.
        
        The Omelyan integrator uses lambda = 0.193 for optimal energy conservation:
        P -> P - xi*eps*F
        Q -> Q + gamma*eps*P
        ...
        
        Returns:
            (accepted: bool, delta_H: float)
        """
        xi = 0.193  # Omelyan parameter
        gamma = 0.5 - xi
        eps = step_size
        
        # Store initial state for Metropolis
        U_old = self.U.copy()
        S_old = self.S.copy()
        
        # Initialize momenta
        self._init_momenta()
        
        # Initial Hamiltonian
        H_initial = self.hamiltonian()
        
        # --- OMELYAN INTEGRATOR ---
        
        # Step 1: P -> P - xi*eps*F (initial half-step)
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t, z, y, x, mu = idx
            F_gauge = self.gauge_force(t, z, y, x, mu)
            self.Pu[idx] = self.Pu[idx] - xi * eps * F_gauge
        
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t, z, y, x = idx
            F_scalar = self.scalar_force(t, z, y, x)
            self.Ps[idx] = self.Ps[idx] - xi * eps * F_scalar
        
        # Step 2: Multiple leapfrog steps
        for step in range(n_steps):
            # Q -> Q + gamma*eps*P (first half of position update)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                self.U[idx] = su3_exp(gamma * eps * self.Pu[idx]) @ self.U[idx]
                self.U[idx] = project_su3(self.U[idx])
            
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t, z, y, x = idx
                self.S[idx] = self.S[idx] + 0.5 * eps * self.Ps[idx]
            
            # P -> P - (1-2*xi)*eps*F (full momentum update)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                F_gauge = self.gauge_force(t, z, y, x, mu)
                self.Pu[idx] = self.Pu[idx] - (1 - 2*xi) * eps * F_gauge
            
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t, z, y, x = idx
                F_scalar = self.scalar_force(t, z, y, x)
                self.Ps[idx] = self.Ps[idx] - (1 - 2*xi) * eps * F_scalar
            
            # Q -> Q + gamma*eps*P (second half of position update)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                self.U[idx] = su3_exp(gamma * eps * self.Pu[idx]) @ self.U[idx]
                self.U[idx] = project_su3(self.U[idx])
            
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t, z, y, x = idx
                self.S[idx] = self.S[idx] + 0.5 * eps * self.Ps[idx]
            
            # Final force update (except last step)
            if step < n_steps - 1:
                for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                    t, z, y, x, mu = idx
                    F_gauge = self.gauge_force(t, z, y, x, mu)
                    self.Pu[idx] = self.Pu[idx] - 2*xi * eps * F_gauge
                
                for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                    t, z, y, x = idx
                    F_scalar = self.scalar_force(t, z, y, x)
                    self.Ps[idx] = self.Ps[idx] - 2*xi * eps * F_scalar
        
        # Step 3: Final half-step P -> P - (1-xi)*eps*F
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t, z, y, x, mu = idx
            F_gauge = self.gauge_force(t, z, y, x, mu)
            self.Pu[idx] = self.Pu[idx] - (1 - xi) * eps * F_gauge
        
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t, z, y, x = idx
            F_scalar = self.scalar_force(t, z, y, x)
            self.Ps[idx] = self.Ps[idx] - (1 - xi) * eps * F_scalar
        
        # --- METROPOLIS ACCEPT/REJECT ---
        H_final = self.hamiltonian()
        delta_H = H_final - H_initial
        
        accepted = False
        if np.random.rand() < np.exp(-delta_H):
            accepted = True
        else:
            # Reject: restore old configuration
            self.U = U_old
            self.S = S_old
        
        # Update diagnostics
        self.avg_delta_H = 0.9 * self.avg_delta_H + 0.1 * abs(delta_H)
        self.acceptance_rate = 0.9 * self.acceptance_rate + (0.1 if accepted else 0.0)
        
        return accepted, delta_H

    # =========================================================================
    # MEASUREMENT FUNCTIONS
    # =========================================================================
    
    def measure_kinetic_vev(self) -> float:
        """
        Measure <(nabla S)^2> - the kinetic VEV that determines gamma.
        gamma = Delta / sqrt(<(nabla S)^2>)
        """
        kin_sum = 0.0
        count = 0
        
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        S_here = self.S[t, z, y, x]
                        for mu in range(self.Nd):
                            shifts = [0, 0, 0, 0]
                            shifts[mu] = 1
                            t2 = (t + shifts[0]) % self.Nt
                            z2 = (z + shifts[1]) % self.Ns
                            y2 = (y + shifts[2]) % self.Ns
                            x2 = (x + shifts[3]) % self.Ns
                            S_fwd = self.S[t2, z2, y2, x2]
                            kin_sum += (S_fwd - S_here)**2
                            count += 1
        
        return kin_sum / count if count > 0 else 0.0


# =============================================================================
# MAIN RUN FUNCTION
# =============================================================================

def run_hmc(Ns: int = 8, Nt: int = 16, beta: float = 6.0,
            n_therm: int = 100, n_meas: int = 200, n_skip: int = 5,
            md_steps: int = 20, step_size: float = 0.02,
            verbose: bool = True) -> dict:
    """
    Run complete HMC simulation and return results.
    
    This is the REAL physics implementation - no mocks!
    """
    constants = UIDTConstants()
    
    if verbose:
        print("=" * 70)
        print("  UIDT v3.6.1 HMC SIMULATION - REAL PHYSICS")
        print("=" * 70)
        print(f"Lattice: {Ns}^3 x {Nt}")
        print(f"Beta: {beta}")
        print(f"UIDT kappa: {constants.KAPPA}")
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
        n_therm=args.n_therm,
        n_meas=args.n_meas,
        n_skip=args.n_skip,
        md_steps=args.md_steps,
        step_size=args.step_size,
        verbose=True
    )
    
    print("\n[COMPLETE] Real HMC simulation finished.")
    print(f"[RESULT] gamma = {results['gamma']:.3f}")
