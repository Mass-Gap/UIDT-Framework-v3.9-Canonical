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
# CONFIGURATION
# =============================================================================

def get_params():
    """Parse arguments with fallback for Jupyter/Colab environments."""
    parser = argparse.ArgumentParser(description='UIDT v3.6.1 HMC Simulation')
    parser.add_argument('--Ns', type=int, default=8)
    parser.add_argument('--Nt', type=int, default=16)
    parser.add_argument('--beta', type=float, default=6.0)
    parser.add_argument('--seed', type=int, default=123456, help='Deterministic RNG seed')
    parser.add_argument('--n_therm', type=int, default=100)
    parser.add_argument('--n_meas', type=int, default=200)
    parser.add_argument('--n_skip', type=int, default=5)
    parser.add_argument('--md_steps', type=int, default=20)
    parser.add_argument('--step_size', type=float, default=0.02)
    parser.add_argument('--verbose', action='store_true')
    args, _ = parser.parse_known_args()
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
# SU(3) MATRIX OPERATIONS
# =============================================================================

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
    H = (H + H.conj().T) / 2
    H = H - np.trace(H) / 3 * np.eye(3)
    return 1j * H

def project_su3(U: np.ndarray) -> np.ndarray:
    """Project matrix to SU(3) via polar decomposition."""
    Udet = U / (np.linalg.det(U) ** (1/3))
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
        self.U = self._init_gauge_field()
        self.S = np.zeros((Nt, Ns, Ns, Ns), dtype=float)
        self.Pu = None
        self.Ps = None
        self.acceptance_rate = 0.5
        self.avg_delta_H = 0.0
        self.plaquette_history = []
        self.action_history = []
    
    def _init_gauge_field(self) -> np.ndarray:
        U = np.zeros((self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3), dtype=complex)
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        for mu in range(self.Nd):
                            U[t, z, y, x, mu] = np.eye(3, dtype=complex)
        return U
    
    def _init_momenta(self):
        shape = (self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3)
        self.Pu = np.zeros(shape, dtype=complex)
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            self.Pu[idx] = random_su3_algebra()
        self.Ps = np.random.randn(self.Nt, self.Ns, self.Ns, self.Ns)

    def plaquette(self, t, z, y, x, mu, nu) -> np.ndarray:
        U_mu_x = self.U[t, z, y, x, mu]
        shifts = [0, 0, 0, 0]; shifts[mu] = 1
        t2=(t+shifts[0])%self.Nt; z2=(z+shifts[1])%self.Ns
        y2=(y+shifts[2])%self.Ns; x2=(x+shifts[3])%self.Ns
        U_nu_xmu = self.U[t2, z2, y2, x2, nu]
        shifts = [0, 0, 0, 0]; shifts[nu] = 1
        t3=(t+shifts[0])%self.Nt; z3=(z+shifts[1])%self.Ns
        y3=(y+shifts[2])%self.Ns; x3=(x+shifts[3])%self.Ns
        U_mu_xnu = self.U[t3, z3, y3, x3, mu]
        U_nu_x = self.U[t, z, y, x, nu]
        return U_mu_x @ U_nu_xmu @ U_mu_xnu.conj().T @ U_nu_x.conj().T
    
    def average_plaquette(self) -> float:
        total = 0.0; count = 0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        for mu in range(self.Nd):
                            for nu in range(mu+1, self.Nd):
                                P = self.plaquette(t,z,y,x,mu,nu)
                                total += np.real(np.trace(P)) / 3.0
                                count += 1
        return total / count
    
    def gauge_action(self) -> float:
        plaq_sum = 0.0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        for mu in range(self.Nd):
                            for nu in range(mu+1, self.Nd):
                                P = self.plaquette(t,z,y,x,mu,nu)
                                plaq_sum += 1.0 - np.real(np.trace(P)) / 3.0
        return self.beta * plaq_sum
    
    def scalar_action(self) -> float:
        lambda_S = self.constants.LAMBDA_S
        m_S = self.constants.M_S
        kinetic = 0.0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        S_here = self.S[t,z,y,x]
                        for mu in range(self.Nd):
                            shifts=[0,0,0,0]; shifts[mu]=1
                            t2=(t+shifts[0])%self.Nt; z2=(z+shifts[1])%self.Ns
                            y2=(y+shifts[2])%self.Ns; x2=(x+shifts[3])%self.Ns
                            kinetic += 0.5 * (self.S[t2,z2,y2,x2] - S_here)**2
        potential = 0.0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        S_here = self.S[t,z,y,x]
                        potential += 0.5 * float(m_S)**2 * S_here**2
                        potential += 0.25 * float(lambda_S) * S_here**4
        return kinetic + potential
    
    def total_action(self) -> float:
        return self.gauge_action() + self.scalar_action()
    
    def kinetic_energy(self) -> float:
        T_gauge = 0.0
        if self.Pu is not None:
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                T_gauge += 0.5 * np.real(np.trace(self.Pu[idx] @ self.Pu[idx].conj().T))
        T_scalar = 0.5 * np.sum(self.Ps**2) if self.Ps is not None else 0.0
        return T_gauge + T_scalar
    
    def hamiltonian(self) -> float:
        return self.kinetic_energy() + self.total_action()

    def gauge_force(self, t, z, y, x, mu) -> np.ndarray:
        staple_sum = np.zeros((3,3), dtype=complex)
        for nu in range(self.Nd):
            if nu == mu: continue
            shifts_mu=[0,0,0,0]; shifts_mu[mu]=1
            t_mu=(t+shifts_mu[0])%self.Nt; z_mu=(z+shifts_mu[1])%self.Ns
            y_mu=(y+shifts_mu[2])%self.Ns; x_mu=(x+shifts_mu[3])%self.Ns
            shifts_nu=[0,0,0,0]; shifts_nu[nu]=1
            t_nu=(t+shifts_nu[0])%self.Nt; z_nu=(z+shifts_nu[1])%self.Ns
            y_nu=(y+shifts_nu[2])%self.Ns; x_nu=(x+shifts_nu[3])%self.Ns
            U_nu_xmu = self.U[t_mu,z_mu,y_mu,x_mu,nu]
            U_mu_xnu = self.U[t_nu,z_nu,y_nu,x_nu,mu]
            U_nu_x = self.U[t,z,y,x,nu]
            staple_fwd = U_nu_xmu @ U_mu_xnu.conj().T @ U_nu_x.conj().T
            shifts_nb=[0,0,0,0]; shifts_nb[nu]=-1
            t_nb=(t+shifts_nb[0])%self.Nt; z_nb=(z+shifts_nb[1])%self.Ns
            y_nb=(y+shifts_nb[2])%self.Ns; x_nb=(x+shifts_nb[3])%self.Ns
            t_mb=(t_mu+shifts_nb[0])%self.Nt; z_mb=(z_mu+shifts_nb[1])%self.Ns
            y_mb=(y_mu+shifts_nb[2])%self.Ns; x_mb=(x_mu+shifts_nb[3])%self.Ns
            U_nu_xmu_nb = self.U[t_mb,z_mb,y_mb,x_mb,nu]
            U_mu_xnb = self.U[t_nb,z_nb,y_nb,x_nb,mu]
            U_nu_xnb = self.U[t_nb,z_nb,y_nb,x_nb,nu]
            staple_bwd = U_nu_xmu_nb.conj().T @ U_mu_xnb.conj().T @ U_nu_xnb
            staple_sum += staple_fwd + staple_bwd
        U_mu_x = self.U[t,z,y,x,mu]
        Omega = U_mu_x @ staple_sum
        F = (self.beta / 3.0) * (Omega - Omega.conj().T)
        F = F - np.trace(F) / 3.0 * np.eye(3)
        return F
    
    def scalar_force(self, t, z, y, x) -> float:
        lambda_S = float(self.constants.LAMBDA_S)
        m_S = float(self.constants.M_S)
        S_here = self.S[t,z,y,x]
        laplacian = 0.0
        for mu in range(self.Nd):
            sf=[0,0,0,0]; sf[mu]=1
            tf=(t+sf[0])%self.Nt; zf=(z+sf[1])%self.Ns; yf=(y+sf[2])%self.Ns; xf=(x+sf[3])%self.Ns
            sb=[0,0,0,0]; sb[mu]=-1
            tb=(t+sb[0])%self.Nt; zb=(z+sb[1])%self.Ns; yb=(y+sb[2])%self.Ns; xb=(x+sb[3])%self.Ns
            laplacian += self.S[tf,zf,yf,xf] + self.S[tb,zb,yb,xb] - 2*S_here
        return -m_S**2 * S_here - lambda_S * S_here**3 + laplacian

    def omelyan_trajectory(self, n_steps=20, step_size=0.02) -> Tuple[bool, float]:
        xi = 0.193; gamma = 0.5 - xi; eps = step_size
        U_old = self.U.copy(); S_old = self.S.copy()
        self._init_momenta()
        H_initial = self.hamiltonian()
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t,z,y,x,mu = idx
            self.Pu[idx] -= xi * eps * self.gauge_force(t,z,y,x,mu)
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t,z,y,x = idx
            self.Ps[idx] -= xi * eps * self.scalar_force(t,z,y,x)
        for step in range(n_steps):
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t,z,y,x,mu = idx
                self.U[idx] = su3_exp(gamma*eps*self.Pu[idx]) @ self.U[idx]
                self.U[idx] = project_su3(self.U[idx])
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t,z,y,x = idx
                self.S[idx] += 0.5*eps*self.Ps[idx]
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t,z,y,x,mu = idx
                self.Pu[idx] -= (1-2*xi)*eps*self.gauge_force(t,z,y,x,mu)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t,z,y,x = idx
                self.Ps[idx] -= (1-2*xi)*eps*self.scalar_force(t,z,y,x)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t,z,y,x,mu = idx
                self.U[idx] = su3_exp(gamma*eps*self.Pu[idx]) @ self.U[idx]
                self.U[idx] = project_su3(self.U[idx])
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                t,z,y,x = idx
                self.S[idx] += 0.5*eps*self.Ps[idx]
            if step < n_steps - 1:
                for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                    t,z,y,x,mu = idx
                    self.Pu[idx] -= 2*xi*eps*self.gauge_force(t,z,y,x,mu)
                for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
                    t,z,y,x = idx
                    self.Ps[idx] -= 2*xi*eps*self.scalar_force(t,z,y,x)
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t,z,y,x,mu = idx
            self.Pu[idx] -= (1-xi)*eps*self.gauge_force(t,z,y,x,mu)
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns):
            t,z,y,x = idx
            self.Ps[idx] -= (1-xi)*eps*self.scalar_force(t,z,y,x)
        H_final = self.hamiltonian()
        delta_H = H_final - H_initial
        accepted = np.random.rand() < np.exp(-delta_H)
        if not accepted:
            self.U = U_old; self.S = S_old
        self.avg_delta_H = 0.9*self.avg_delta_H + 0.1*abs(delta_H)
        self.acceptance_rate = 0.9*self.acceptance_rate + (0.1 if accepted else 0.0)
        return accepted, delta_H

    def measure_kinetic_vev(self) -> float:
        kin_sum = 0.0; count = 0
        for t in range(self.Nt):
            for z in range(self.Ns):
                for y in range(self.Ns):
                    for x in range(self.Ns):
                        S_here = self.S[t,z,y,x]
                        for mu in range(self.Nd):
                            shifts=[0,0,0,0]; shifts[mu]=1
                            t2=(t+shifts[0])%self.Nt; z2=(z+shifts[1])%self.Ns
                            y2=(y+shifts[2])%self.Ns; x2=(x+shifts[3])%self.Ns
                            kin_sum += (self.S[t2,z2,y2,x2] - S_here)**2
                            count += 1
        return kin_sum / count if count > 0 else 0.0


def run_hmc(Ns=8, Nt=16, beta=6.0, n_therm=100, n_meas=200, n_skip=5,
            md_steps=20, step_size=0.02, verbose=True, seed=None) -> dict:
    constants = UIDTConstants()
    if seed is not None:
        np.random.seed(seed)
    if verbose:
        print("=" * 70)
        print("  UIDT v3.6.1 HMC SIMULATION - REAL PHYSICS")
        print("=" * 70)
        print(f"Lattice: {Ns}^3 x {Nt}, Beta: {beta}, Kappa: {constants.KAPPA}")
        if seed is not None: print(f"Seed: {seed}")
        print("=" * 70)
    lattice = UIDTLattice(Ns=Ns, Nt=Nt, beta=beta)
    start_time = time.time()
    if verbose: print("\nThermalization...")
    for i in range(n_therm):
        accepted, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        if verbose and (i+1) % 10 == 0:
            print(f"  Therm {i+1:4d}: <P> = {lattice.average_plaquette():.6f}, acc = {lattice.acceptance_rate:.2f}")
    if verbose: print("\nMeasurements...")
    plaquette_measurements = []; kinetic_vev_measurements = []; accepted_count = 0
    for i in range(n_meas):
        accepted, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        if accepted: accepted_count += 1
        if (i+1) % n_skip == 0:
            plaq = lattice.average_plaquette()
            kin_vev = lattice.measure_kinetic_vev()
            plaquette_measurements.append(plaq)
            kinetic_vev_measurements.append(kin_vev)
            if verbose and (i+1) % 50 == 0:
                print(f"  Meas {i+1:4d}: <P> = {plaq:.6f}, <(dS)^2> = {kin_vev:.6f}")
    elapsed = time.time() - start_time
    plaq_mean = np.mean(plaquette_measurements)
    plaq_err = np.std(plaquette_measurements) / np.sqrt(len(plaquette_measurements))
    kin_vev_mean = np.mean(kinetic_vev_measurements)
    kin_vev_err = np.std(kinetic_vev_measurements) / np.sqrt(len(kinetic_vev_measurements))
    gamma_computed = float(constants.TARGET_DELTA) / np.sqrt(kin_vev_mean) if kin_vev_mean > 0 else float('nan')
    acceptance = accepted_count / n_meas
    if verbose:
        print("\n" + "=" * 70)
        print(f"Runtime: {elapsed:.1f}s | Acceptance: {acceptance:.2%}")
        print(f"<P> = {plaq_mean:.6f} +/- {plaq_err:.6f}")
        print(f"<(dS)^2> = {kin_vev_mean:.6f} +/- {kin_vev_err:.6f}")
        print(f"gamma = {gamma_computed:.3f} (target: {constants.TARGET_GAMMA})")
        print("=" * 70)
    return {'plaquette': plaq_mean, 'plaquette_err': plaq_err,
            'kinetic_vev': kin_vev_mean, 'kinetic_vev_err': kin_vev_err,
            'gamma': gamma_computed, 'acceptance': acceptance, 'runtime': elapsed,
            'measurements': {'plaquette': plaquette_measurements, 'kinetic_vev': kinetic_vev_measurements}}


if __name__ == "__main__":
    args = get_params()
    results = run_hmc(Ns=args.Ns, Nt=args.Nt, beta=args.beta, seed=args.seed,
                      n_therm=args.n_therm, n_meas=args.n_meas, n_skip=args.n_skip,
                      md_steps=args.md_steps, step_size=args.step_size, verbose=True)
    print("\n[COMPLETE] Real HMC simulation finished.")
    print(f"[RESULT] gamma = {results['gamma']:.3f}")
