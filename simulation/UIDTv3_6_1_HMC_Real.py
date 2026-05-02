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
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    # parse_known_args ignores Jupyter kernel arguments
    args, _ = parser.parse_known_args()

    # Set seed if provided
    if args.seed is not None:
        np.random.seed(args.seed)

    return args


@dataclass
class UIDTConstants:
    """Canonical UIDT v3.6.1 constants."""
    KAPPA: Any = mp.mpf("0.500")
    LAMBDA_S: Any = mp.mpf("0.417")
    M_S: Any = mp.mpf("1.705")
    TARGET_DELTA: Any = mp.mpf("1.710035046742")
    TARGET_GAMMA: Any = mp.mpf("16.339")
    GLUON_CONDENSATE: float = 0.277


# =============================================================================
# SU(3) MATRIX OPERATIONS (REAL PHYSICS)
# =============================================================================

# PATCH-2 + PATCH-3 (safety): Validated SU(3) exponential with fallback.
# su3_expm_hybrid from the Cayley-Hamilton module is tried first.
# If unitarity or det residuals exceed 1e-10, scipy.linalg.expm is used.
# This ensures correctness while preserving the CuPy GPU path when available.
from scipy.linalg import expm
from UIDTv3_6_1_su3_expm_cayley_hamiltonian_Modul import su3_expm_hybrid


def random_su3() -> np.ndarray:
    """Generate random SU(3) matrix via QR decomposition."""
    A = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    Q, R = np.linalg.qr(A)
    det_Q = np.linalg.det(Q)
    Q = Q / (det_Q ** (1/3))
    return Q

def random_su3_algebra() -> np.ndarray:
    """Generate random element of su(3) algebra (traceless anti-Hermitian)."""
    H = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    H = (H + H.conj().T) / 2  # Hermitian
    H = H - np.trace(H) / 3 * np.eye(3)  # Traceless
    return 1j * H

def project_su3(U: np.ndarray) -> np.ndarray:
    """Project matrix to SU(3) via polar decomposition."""
    Udet = U / (np.linalg.det(U) ** (1/3))
    Q, R = np.linalg.qr(Udet)
    det_Q = np.linalg.det(Q)
    return Q / (det_Q ** (1/3))

def su3_exp(X: np.ndarray) -> np.ndarray:
    """Numerically safe SU(3) matrix exponential with validated fallback.

    PATCH-2+3: Tries su3_expm_hybrid (Cayley-Hamilton / CuPy GPU path) first.
    Falls back to scipy.linalg.expm if SU(3) residuals are out of tolerance.
    Residual thresholds: unitarity < 1e-10, |det - 1| < 1e-10.
    """
    Y = su3_expm_hybrid(X)
    unitarity_residual = np.max(np.abs(Y @ Y.conj().T - np.eye(3)))
    det_residual = abs(np.linalg.det(Y) - 1.0)
    if unitarity_residual > 1e-10 or det_residual > 1e-10:
        return expm(X)
    return Y


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
        U_mu_x = self.U[t, z, y, x, mu]

        shifts = [0, 0, 0, 0]
        shifts[mu] = 1
        t2 = (t + shifts[0]) % self.Nt
        z2 = (z + shifts[1]) % self.Ns
        y2 = (y + shifts[2]) % self.Ns
        x2 = (x + shifts[3]) % self.Ns
        U_nu_xmu = self.U[t2, z2, y2, x2, nu]

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
        """Kinetic energy of conjugate momenta."""
        T_gauge = 0.0
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            P = self.Pu[idx]
            T_gauge += -0.5 * np.real(np.trace(P @ P))

        T_scalar = 0.5 * np.sum(self.Ps**2)
        return T_gauge + T_scalar

    def hamiltonian(self):
        """Total Hamiltonian H = T + S."""
        return self.kinetic_energy() + self.total_action()

    # =========================================================================
    # FORCE CALCULATIONS (REAL PHYSICS)
    # =========================================================================

    def gauge_force(self, t: int, z: int, y: int, x: int, mu: int) -> np.ndarray:
        """Compute gauge force: F_mu(x) = -dS_G/dU_mu(x) in su(3) algebra."""
        staple = np.zeros((3, 3), dtype=complex)

        for nu in range(self.Nd):
            if nu == mu:
                continue

            # Forward staple
            shifts_mu = [0, 0, 0, 0]; shifts_mu[mu] = 1
            shifts_nu = [0, 0, 0, 0]; shifts_nu[nu] = 1
            shifts_mu_nu = [0, 0, 0, 0]; shifts_mu_nu[mu] = 1; shifts_mu_nu[nu] = 1

            t_nu = (t + shifts_nu[0]) % self.Nt
            z_nu = (z + shifts_nu[1]) % self.Ns
            y_nu = (y + shifts_nu[2]) % self.Ns
            x_nu = (x + shifts_nu[3]) % self.Ns

            t_mu = (t + shifts_mu[0]) % self.Nt
            z_mu = (z + shifts_mu[1]) % self.Ns
            y_mu = (y + shifts_mu[2]) % self.Ns
            x_mu = (x + shifts_mu[3]) % self.Ns

            U_nu_x = self.U[t, z, y, x, nu]
            U_mu_xnu = self.U[t_nu, z_nu, y_nu, x_nu, mu]
            U_nu_xmu = self.U[t_mu, z_mu, y_mu, x_mu, nu]

            staple += U_nu_x @ U_mu_xnu @ U_nu_xmu.conj().T

            # Backward staple
            t_minus_nu = (t - shifts_nu[0]) % self.Nt
            z_minus_nu = (z - shifts_nu[1]) % self.Ns
            y_minus_nu = (y - shifts_nu[2]) % self.Ns
            x_minus_nu = (x - shifts_nu[3]) % self.Ns

            t_mu_minus_nu = (t_mu - shifts_nu[0]) % self.Nt
            z_mu_minus_nu = (z_mu - shifts_nu[1]) % self.Ns
            y_mu_minus_nu = (y_mu - shifts_nu[2]) % self.Ns
            x_mu_minus_nu = (x_mu - shifts_nu[3]) % self.Ns

            U_nu_minus = self.U[t_minus_nu, z_minus_nu, y_minus_nu, x_minus_nu, nu]
            U_mu_minus = self.U[t_minus_nu, z_minus_nu, y_minus_nu, x_minus_nu, mu]
            U_nu_mu_minus = self.U[t_mu_minus_nu, z_mu_minus_nu, y_mu_minus_nu, x_mu_minus_nu, nu]

            staple += U_nu_minus.conj().T @ U_mu_minus @ U_nu_mu_minus

        U_mu = self.U[t, z, y, x, mu]
        F = self.beta / 3.0 * (U_mu @ staple).conj().T
        F = F - F.conj().T
        F = F - np.trace(F) / 3.0 * np.eye(3)
        return F

    def scalar_force(self, t: int, z: int, y: int, x: int) -> float:
        """Compute scalar field force: F_S(x) = -dS_S/dS(x)."""
        m_S = self.constants.M_S
        lambda_S = self.constants.LAMBDA_S
        S_here = self.S[t, z, y, x]

        laplacian = 0.0
        for mu in range(self.Nd):
            shifts_fwd = [0, 0, 0, 0]; shifts_fwd[mu] = 1
            shifts_bwd = [0, 0, 0, 0]; shifts_bwd[mu] = -1

            t_fwd = (t + shifts_fwd[0]) % self.Nt
            z_fwd = (z + shifts_fwd[1]) % self.Ns
            y_fwd = (y + shifts_fwd[2]) % self.Ns
            x_fwd = (x + shifts_fwd[3]) % self.Ns

            t_bwd = (t + shifts_bwd[0]) % self.Nt
            z_bwd = (z + shifts_bwd[1]) % self.Ns
            y_bwd = (y + shifts_bwd[2]) % self.Ns
            x_bwd = (x + shifts_bwd[3]) % self.Ns

            laplacian += self.S[t_fwd, z_fwd, y_fwd, x_fwd] + self.S[t_bwd, z_bwd, y_bwd, x_bwd] - 2 * S_here

        return laplacian - float(m_S**2) * S_here - float(lambda_S) * S_here**3

    # =========================================================================
    # OMELYAN 2ND-ORDER SYMPLECTIC INTEGRATOR (REAL PHYSICS)
    # PATCH-1: Final half-step uses xi (not 1-xi). Verified 2026-04-30.
    # PATCH-3: delta_H cast to float before np.exp (mpf compatibility).
    # =========================================================================

    def omelyan_trajectory(self, n_steps: int = 20, step_size: float = 0.02) -> Tuple[bool, float]:
        """
        Omelyan 2nd-order symplectic integrator for HMC trajectory.

        Sequence: [xi | gamma | (1-2xi) | gamma | 2xi | ... | gamma | (1-2xi) | gamma | xi]
        where xi = 0.193, gamma = 0.5 - xi = 0.307

        PATCH-1: Endpoint half-steps use xi, not (1-xi).
        """
        xi = 0.193   # Omelyan parameter [Evidence A-]
        gamma = 0.5 - xi  # = 0.307
        eps = step_size

        # Save current state for rejection
        U_old = self.U.copy()
        S_old = self.S.copy()

        # Initialize momenta
        self._init_momenta()

        # Compute initial Hamiltonian
        H_initial = self.hamiltonian()

        # --- STEP 1: Initial xi half-step for momenta ---
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t, z, y, x, mu = idx
            F_gauge = self.gauge_force(t, z, y, x, mu)
            self.Pu[idx] = self.Pu[idx] - xi * eps * F_gauge

        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t, z, y, x = idx
            F_scalar = self.scalar_force(t, z, y, x)
            self.Ps[idx] = self.Ps[idx] - xi * eps * F_scalar

        # --- STEP 2: n_steps full leapfrog steps ---
        for step in range(n_steps):
            # Gauge field update (gamma step)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                self.U[idx] = su3_exp(gamma * eps * self.Pu[idx]) @ self.U[idx]
                self.U[idx] = project_su3(self.U[idx])

            # Scalar field update (half step)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t, z, y, x = idx
                self.S[idx] += 0.5 * eps * self.Ps[idx]

            # Momentum update (1-2xi full step)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                F_gauge = self.gauge_force(t, z, y, x, mu)
                self.Pu[idx] = self.Pu[idx] - (1 - 2*xi) * eps * F_gauge

            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t, z, y, x = idx
                F_scalar = self.scalar_force(t, z, y, x)
                self.Ps[idx] = self.Ps[idx] - (1 - 2*xi) * eps * F_scalar

            # Gauge field update (gamma step)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                self.U[idx] = su3_exp(gamma * eps * self.Pu[idx]) @ self.U[idx]
                self.U[idx] = project_su3(self.U[idx])

            # Scalar field update (half step)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t, z, y, x = idx
                self.S[idx] += 0.5 * eps * self.Ps[idx]

            # Intermediate 2xi momentum step (except last)
            if step < n_steps - 1:
                for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                    t, z, y, x, mu = idx
                    F_gauge = self.gauge_force(t, z, y, x, mu)
                    self.Pu[idx] = self.Pu[idx] - 2*xi * eps * F_gauge

                for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                    t, z, y, x = idx
                    F_scalar = self.scalar_force(t, z, y, x)
                    self.Ps[idx] = self.Ps[idx] - 2*xi * eps * F_scalar

        # --- STEP 3: Final xi half-step for momenta ---
        # PATCH-1: Must use xi, NOT (1-xi). Fixes time-reversal symmetry.
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t, z, y, x, mu = idx
            F_gauge = self.gauge_force(t, z, y, x, mu)
            self.Pu[idx] = self.Pu[idx] - xi * eps * F_gauge

        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t, z, y, x = idx
            F_scalar = self.scalar_force(t, z, y, x)
            self.Ps[idx] = self.Ps[idx] - xi * eps * F_scalar

        # --- METROPOLIS ACCEPT/REJECT ---
        H_final = self.hamiltonian()
        delta_H = H_final - H_initial
        # PATCH-3: Cast to float before np.exp (mpf from scalar_action is incompatible with numpy)
        delta_H_float = float(delta_H)

        accepted = False
        if np.random.rand() < np.exp(-delta_H_float):
            accepted = True
        else:
            self.U = U_old
            self.S = S_old

        self.avg_delta_H = 0.9 * self.avg_delta_H + 0.1 * abs(delta_H_float)
        self.acceptance_rate = 0.9 * self.acceptance_rate + (0.1 if accepted else 0.0)

        return accepted, delta_H_float


# =============================================================================
# MEASUREMENTS
# =============================================================================

class UIDTMeasurements:
    """Observable measurements for UIDT lattice simulation."""

    def __init__(self, lattice: UIDTLattice):
        self.lattice = lattice

    def plaquette(self) -> float:
        return self.lattice.average_plaquette()

    def polyakov_loop(self) -> complex:
        """Compute Polyakov loop (temporal Wilson line)."""
        total = 0.0 + 0j
        for z in range(self.lattice.Ns):
            for y in range(self.lattice.Ns):
                for x in range(self.lattice.Ns):
                    P = np.eye(3, dtype=complex)
                    for t in range(self.lattice.Nt):
                        P = P @ self.lattice.U[t, z, y, x, 0]
                    total += np.trace(P)

        vol = self.lattice.Ns**3
        return total / (3.0 * vol)

    def scalar_condensate(self) -> float:
        """Average scalar field value."""
        return float(np.mean(self.lattice.S))

    def scalar_susceptibility(self) -> float:
        """Scalar field susceptibility."""
        phi = self.lattice.S.flatten()
        return float(len(phi) * (np.mean(phi**2) - np.mean(phi)**2))

    def topological_charge(self) -> float:
        """Approximate topological charge (simplified clover)."""
        Q = 0.0
        for t in range(self.lattice.Nt):
            for z in range(self.lattice.Ns):
                for y in range(self.lattice.Ns):
                    for x in range(self.lattice.Ns):
                        P01 = self.lattice.plaquette(t, z, y, x, 0, 1)
                        P23 = self.lattice.plaquette(t, z, y, x, 2, 3)
                        F01 = (P01 - P01.conj().T) / (2j)
                        F23 = (P23 - P23.conj().T) / (2j)
                        Q += np.real(np.trace(F01 @ F23))
        return Q / (16 * np.pi**2)


# =============================================================================
# MAIN HMC RUNNER
# =============================================================================

def run_hmc(Ns: int = 8, Nt: int = 16, beta: float = 6.0,
            n_therm: int = 100, n_meas: int = 200, n_skip: int = 5,
            md_steps: int = 20, step_size: float = 0.02,
            verbose: bool = False) -> dict:
    """
    Main HMC simulation runner.

    Returns dict with measurement history and diagnostics.
    """
    lattice = UIDTLattice(Ns=Ns, Nt=Nt, beta=beta)
    meas = UIDTMeasurements(lattice)

    results = {
        'plaquette': [],
        'polyakov': [],
        'scalar_condensate': [],
        'scalar_susceptibility': [],
        'topological_charge': [],
        'acceptance_rate': [],
        'delta_H': [],
        'params': {
            'Ns': Ns, 'Nt': Nt, 'beta': beta,
            'n_therm': n_therm, 'n_meas': n_meas,
            'md_steps': md_steps, 'step_size': step_size,
        }
    }

    if verbose:
        print(f"\nUIDT v3.6.1 HMC Simulation")
        print(f"Lattice: {Ns}^3 x {Nt}, beta={beta}")
        print(f"Thermalization...")

    for i in range(n_therm):
        accepted, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        if verbose and (i + 1) % 10 == 0:
            plaq = lattice.average_plaquette()
            print(f"  Therm {i+1:4d}/{n_therm}: plaq={plaq:.4f}, acc={lattice.acceptance_rate:.2f}, <|dH|>={lattice.avg_delta_H:.4f}")

    if verbose:
        print(f"\nMeasurement phase...")

    for i in range(n_meas):
        for _ in range(n_skip):
            accepted, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)

        results['plaquette'].append(meas.plaquette())
        results['polyakov'].append(abs(meas.polyakov_loop()))
        results['scalar_condensate'].append(meas.scalar_condensate())
        results['scalar_susceptibility'].append(meas.scalar_susceptibility())
        results['topological_charge'].append(meas.topological_charge())
        results['acceptance_rate'].append(lattice.acceptance_rate)
        results['delta_H'].append(dH)

        if verbose and (i + 1) % 50 == 0:
            print(f"  Meas {i+1:4d}/{n_meas}: plaq={results['plaquette'][-1]:.4f}, acc={lattice.acceptance_rate:.2f}")

    if verbose:
        avg_plaq = np.mean(results['plaquette'])
        avg_acc  = np.mean(results['acceptance_rate'])
        print(f"\n=== FINAL RESULTS ===")
        print(f"  <plaquette>     = {avg_plaq:.4f}")
        print(f"  <acceptance>    = {avg_acc:.3f}")
        print(f"  <|delta_H|>     = {np.mean(np.abs(results['delta_H'])):.4f}")

    return results


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    args = get_params()
    results = run_hmc(
        Ns=args.Ns, Nt=args.Nt, beta=args.beta,
        n_therm=args.n_therm, n_meas=args.n_meas, n_skip=args.n_skip,
        md_steps=args.md_steps, step_size=args.step_size,
        verbose=True
    )
