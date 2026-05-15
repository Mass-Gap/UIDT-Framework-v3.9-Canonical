#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.9 HMC – Vectorized + Momentum-Fix
==========================================
Author: Philipp Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0

PATCHES vs. UIDTv3_6_1_HMC_Real.py
------------------------------------
PATCH-1 (Vectorized Loops):
  avg_plaquette()   -> avg_plaquette_vec()   via np.roll
  scalar_action()   -> S_scalar_vec()        via np.roll
  scalar_force()    -> F_scalar_vec()        via np.roll
  gauge_action()    -> S_gauge_vec()         via np.roll
  kinetic_vev()     -> scalar_kin_vev_vec()  via np.roll

PATCH-2 (Momentum Normalization):
  random_su3_algebra() -> random_su3_algebra_normalized()
  Fix: P /= sqrt(Tr(P P†))
  Reason: Unnormalized momenta had <Tr(P P†)> ~= 8.43 instead of 1,
          causing <|Delta_H|> ~= 1108 and 0% acceptance rate.

Affected constants (evidence category unchanged):
  Delta* = 1.710 +/- 0.015 GeV  [A]
  gamma  = 16.339               [A-]
  kappa  = 0.500                [A-]
  lambda_S = 0.417              [A-]
  M_S  = 1.705                  [A-]
"""

import numpy as np
import time
import argparse
from dataclasses import dataclass
from typing import Any, Tuple
from scipy.linalg import expm
from mpmath import mp

# Precision: local per UIDT Race Condition Lock
mp.dps = 80


# =============================================================================
# IMMUTABLE PARAMETER LEDGER -- DO NOT MODIFY
# =============================================================================

@dataclass
class UIDTConstants:
    KAPPA:        Any = mp.mpf("0.500")
    LAMBDA_S:     Any = mp.mpf("0.417")
    M_S:          Any = mp.mpf("1.705")
    TARGET_DELTA: Any = mp.mpf("1.710035046742")
    TARGET_GAMMA: Any = mp.mpf("16.339")
    GLUON_CONDENSATE: float = 0.277


# =============================================================================
# PATCH-2: NORMALIZED SU(3) MOMENTA
# =============================================================================

def random_su3_algebra_normalized() -> np.ndarray:
    """
    Generate normalized su(3) algebra element with Tr(P P†) = 1.

    FIX vs. original random_su3_algebra():
      Original lacked normalization -> <Tr(P P†)> ~= 8.43
      This caused <|Delta_H|> ~= 1108 and 0% HMC acceptance rate.
    """
    H = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    H = (H + H.conj().T) / 2
    H = H - np.trace(H) / 3 * np.eye(3)
    P = 1j * H
    norm = np.sqrt(np.real(np.trace(P @ P.conj().T)))
    return P / norm if norm > 1e-14 else P


def project_su3(U: np.ndarray) -> np.ndarray:
    """Project single 3x3 matrix to SU(3) via QR decomposition."""
    Q, _ = np.linalg.qr(U)
    d = np.linalg.det(Q)
    return Q / (d ** (1 / 3))


# =============================================================================
# PATCH-1: VECTORIZED LATTICE OPERATIONS
# =============================================================================

def avg_plaquette_vec(U: np.ndarray, Nt: int, Ns: int, Nd: int) -> float:
    """
    Vectorized average plaquette via np.roll.
    Replaces O(Nt*Ns^3*Nd^2) Python loop with NumPy batch operations.
    """
    total = 0.0
    count = 0
    for mu in range(Nd):
        for nu in range(mu + 1, Nd):
            Um = U[..., mu, :, :]
            Un = U[..., nu, :, :]
            Un_xmu = np.roll(Un, -1, axis=mu)
            Um_xnu = np.roll(Um, -1, axis=nu)
            P = (Um
                 @ Un_xmu
                 @ np.swapaxes(Um_xnu, -1, -2).conj()
                 @ np.swapaxes(Un, -1, -2).conj())
            total += np.sum(
                np.real(np.trace(P.reshape(-1, 3, 3), axis1=-2, axis2=-1))
            ) / 3.0
            count += Nt * Ns ** 3
    return total / count


def S_gauge_vec(U: np.ndarray, Nt: int, Ns: int, Nd: int, beta: float) -> float:
    """Vectorized Wilson gauge action."""
    s = 0.0
    for mu in range(Nd):
        for nu in range(mu + 1, Nd):
            Um = U[..., mu, :, :]
            Un = U[..., nu, :, :]
            P = (Um
                 @ np.roll(Un, -1, axis=mu)
                 @ np.swapaxes(np.roll(Um, -1, axis=nu), -1, -2).conj()
                 @ np.swapaxes(Un, -1, -2).conj())
            s += np.sum(
                1.0 - np.real(
                    np.trace(P.reshape(-1, 3, 3), axis1=-2, axis2=-1)
                ) / 3.0
            )
    return beta * s


def S_scalar_vec(S: np.ndarray, m_S: float, lam: float) -> float:
    """Vectorized UIDT scalar action."""
    kin = sum(
        0.5 * (np.roll(S, -1, axis=ax) - S) ** 2
        for ax in range(4)
    )
    pot = 0.5 * m_S ** 2 * S ** 2 + 0.25 * lam * S ** 4
    return float(np.sum(kin) + np.sum(pot))


def F_scalar_vec(S: np.ndarray, m_S: float, lam: float) -> np.ndarray:
    """Vectorized scalar field force F = -dS/dS(x)."""
    lap = sum(
        np.roll(S, -1, axis=ax) + np.roll(S, 1, axis=ax)
        for ax in range(4)
    )
    return -m_S ** 2 * S - lam * S ** 3 + (lap - 8 * S)


def scalar_kin_vev_vec(S: np.ndarray) -> float:
    """Vectorized <(grad S)^2> measurement."""
    return float(np.mean(sum((np.roll(S, -1, axis=ax) - S) ** 2 for ax in range(4))))


# =============================================================================
# GAUGE FORCE (site-by-site, SU(3) algebra projection required)
# =============================================================================

def F_gauge_site(U, t, z, y, x, mu, Nt, Ns, Nd, beta):
    """
    Gauge force at single site.
    Site-by-site loop retained: SU(3) traceless anti-Hermitian
    projection requires per-link matrix access.
    """
    staple = np.zeros((3, 3), dtype=complex)
    sizes = [Nt, Ns, Ns, Ns]
    c = [t, z, y, x]

    def sh(i, d):
        return (c[i] + d) % sizes[i]

    for nu in range(Nd):
        if nu == mu:
            continue
        cm = list(c); cm[mu] = sh(mu, 1)
        cn = list(c); cn[nu] = sh(nu, 1)
        cnb = list(c); cnb[nu] = sh(nu, -1)
        cmnb = list(cm); cmnb[nu] = (cm[nu] - 1) % sizes[nu]

        sf = (U[cm[0], cm[1], cm[2], cm[3], nu]
              @ U[cn[0], cn[1], cn[2], cn[3], mu].conj().T
              @ U[t, z, y, x, nu].conj().T)
        sb = (U[cmnb[0], cmnb[1], cmnb[2], cmnb[3], nu].conj().T
              @ U[cnb[0], cnb[1], cnb[2], cnb[3], mu].conj().T
              @ U[cnb[0], cnb[1], cnb[2], cnb[3], nu])
        staple += sf + sb

    Om = U[t, z, y, x, mu] @ staple
    F = (beta / 3.0) * (Om - Om.conj().T)
    return F - np.trace(F) / 3.0 * np.eye(3)


# =============================================================================
# HMC LATTICE CLASS
# =============================================================================

class UIDTLattice:

    def __init__(self, Ns: int = 8, Nt: int = 16, beta: float = 6.0):
        self.Ns = Ns
        self.Nt = Nt
        self.Nd = 4
        self.beta = beta
        self.constants = UIDTConstants()
        self.m_S = float(self.constants.M_S)
        self.lam  = float(self.constants.LAMBDA_S)

        self.U = np.zeros((Nt, Ns, Ns, Ns, 4, 3, 3), dtype=complex)
        for idx in np.ndindex(Nt, Ns, Ns, Ns, 4):
            self.U[idx] = np.eye(3, dtype=complex)
        self.S = np.zeros((Nt, Ns, Ns, Ns))
        self.Pu = None
        self.Ps = None

    def _init_momenta(self):
        """PATCH-2: Normalized momenta."""
        self.Pu = np.zeros(
            (self.Nt, self.Ns, self.Ns, self.Ns, self.Nd, 3, 3), dtype=complex
        )
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            self.Pu[idx] = random_su3_algebra_normalized()
        self.Ps = np.random.randn(self.Nt, self.Ns, self.Ns, self.Ns)

    def kinetic_energy(self) -> float:
        T = sum(
            0.5 * np.real(np.trace(self.Pu[idx] @ self.Pu[idx].conj().T))
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd)
        )
        return T + 0.5 * np.sum(self.Ps ** 2)

    def hamiltonian(self) -> float:
        return (self.kinetic_energy()
                + S_gauge_vec(self.U, self.Nt, self.Ns, self.Nd, self.beta)
                + S_scalar_vec(self.S, self.m_S, self.lam))

    def _apply_gauge_force(self, coeff: float):
        for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
            t, z, y, x, mu = idx
            self.Pu[idx] -= coeff * F_gauge_site(
                self.U, t, z, y, x, mu,
                self.Nt, self.Ns, self.Nd, self.beta
            )

    def omelyan_trajectory(
        self, n_steps: int = 20, step_size: float = 0.015
    ) -> Tuple[bool, float]:
        """
        Omelyan 2nd-order symplectic integrator.
        PATCH-1: scalar force vectorized.
        PATCH-2: normalized momenta.
        """
        xi = 0.193
        gam = 0.5 - xi
        eps = step_size

        U_old = self.U.copy()
        S_old = self.S.copy()
        self._init_momenta()
        H_i = self.hamiltonian()

        self._apply_gauge_force(xi * eps)
        self.Ps -= xi * eps * F_scalar_vec(self.S, self.m_S, self.lam)

        for step in range(n_steps):
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                self.U[idx] = project_su3(
                    expm(gam * eps * self.Pu[idx]) @ self.U[idx]
                )
            self.S += 0.5 * eps * self.Ps
            self._apply_gauge_force((1 - 2 * xi) * eps)
            self.Ps -= (1 - 2 * xi) * eps * F_scalar_vec(self.S, self.m_S, self.lam)
            for idx in np.ndindex(self.Nt, self.Ns, self.Ns, self.Ns, self.Nd):
                t, z, y, x, mu = idx
                self.U[idx] = project_su3(
                    expm(gam * eps * self.Pu[idx]) @ self.U[idx]
                )
            self.S += 0.5 * eps * self.Ps
            if step < n_steps - 1:
                self._apply_gauge_force(2 * xi * eps)
                self.Ps -= 2 * xi * eps * F_scalar_vec(self.S, self.m_S, self.lam)

        self._apply_gauge_force((1 - xi) * eps)
        self.Ps -= (1 - xi) * eps * F_scalar_vec(self.S, self.m_S, self.lam)

        H_f = self.hamiltonian()
        dH = H_f - H_i
        accepted = np.random.rand() < np.exp(-dH)
        if not accepted:
            self.U = U_old
            self.S = S_old

        return accepted, dH

    def measure(self) -> dict:
        """Vectorized measurements (PATCH-1)."""
        return {
            "plaquette": avg_plaquette_vec(self.U, self.Nt, self.Ns, self.Nd),
            "kinetic_vev": scalar_kin_vev_vec(self.S),
        }


# =============================================================================
# RUN FUNCTION
# =============================================================================

def run_hmc(Ns: int = 4, Nt: int = 8, beta: float = 6.0,
            n_therm: int = 200, n_meas: int = 500, n_skip: int = 5,
            md_steps: int = 20, step_size: float = 0.015,
            verbose: bool = True) -> dict:
    """
    Production HMC run with PATCH-1 and PATCH-2 active.
    Recommended minimum: Ns=4, Nt=8, n_therm=200, n_meas=500.
    """
    constants = UIDTConstants()

    if verbose:
        print("=" * 65)
        print("  UIDT v3.9 HMC -- Vectorized + Momentum-Fix")
        print("=" * 65)
        print(f"  Lattice:  {Ns}^3 x {Nt}")
        print(f"  beta:     {beta}")
        print(f"  Therm:    {n_therm}  |  Meas: {n_meas}  |  Skip: {n_skip}")
        print(f"  MD:       {md_steps} steps, eps={step_size}")
        print(f"  PATCH-1:  scalar ops vectorized via np.roll")
        print(f"  PATCH-2:  Tr(P P†)=1 momentum normalization")
        print("=" * 65)

    lattice = UIDTLattice(Ns=Ns, Nt=Nt, beta=beta)
    t0 = time.time()

    if verbose:
        print("\nThermalization ...")
    acc_therm = []
    for i in range(n_therm):
        acc, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        acc_therm.append(acc)
        if verbose and (i + 1) % max(1, n_therm // 5) == 0:
            m = lattice.measure()
            print(f"  [{i+1:4d}] <P>={m['plaquette']:.5f}  "
                  f"acc={np.mean(acc_therm[-20:]):.0%}")

    plaq_l, kv_l, dH_l, acc_l = [], [], [], []
    if verbose:
        print("\nMeasurements ...")
    for i in range(n_meas):
        acc, dH = lattice.omelyan_trajectory(n_steps=md_steps, step_size=step_size)
        acc_l.append(acc)
        if (i + 1) % n_skip == 0:
            m = lattice.measure()
            plaq_l.append(m["plaquette"])
            kv_l.append(m["kinetic_vev"])
            dH_l.append(dH)
            if verbose and (i + 1) % max(1, n_meas // 4) == 0:
                kv = m["kinetic_vev"]
                g = (float(constants.TARGET_DELTA) / np.sqrt(kv)
                     if kv > 1e-12 else float("nan"))
                print(f"  [{i+1:4d}] <P>={m['plaquette']:.5f}  "
                      f"<(gradS)^2>={kv:.5f}  gamma={g:.3f}")

    elapsed = time.time() - t0
    N = len(plaq_l)
    p_mean  = np.mean(plaq_l); p_err  = np.std(plaq_l) / np.sqrt(N)
    kv_mean = np.mean(kv_l);   kv_err = np.std(kv_l)   / np.sqrt(N)
    acc_rate = np.mean(acc_l)
    gamma_m = (float(constants.TARGET_DELTA) / np.sqrt(kv_mean)
               if kv_mean > 1e-12 else float("nan"))

    if verbose:
        print("\n" + "=" * 65)
        print("  RESULTS")
        print("=" * 65)
        print(f"  Runtime:          {elapsed:.1f} s")
        print(f"  Acceptance rate:  {acc_rate:.2%}")
        print(f"  <P>:              {p_mean:.6f} +/- {p_err:.6f}")
        print(f"  <(gradS)^2>:      {kv_mean:.6f} +/- {kv_err:.6f}")
        print(f"  gamma measured:   {gamma_m:.4f}")
        print(f"  gamma ledger[A-]: {float(constants.TARGET_GAMMA):.4f}")
        print("=" * 65)

    return {
        "plaquette": p_mean, "plaquette_err": p_err,
        "kinetic_vev": kv_mean, "kinetic_vev_err": kv_err,
        "gamma": gamma_m, "acceptance": acc_rate,
        "runtime": elapsed,
        "measurements": {"plaquette": plaq_l, "kinetic_vev": kv_l},
    }


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UIDT v3.9 HMC - Vectorized")
    parser.add_argument("--Ns",        type=int,   default=4)
    parser.add_argument("--Nt",        type=int,   default=8)
    parser.add_argument("--beta",      type=float, default=6.0)
    parser.add_argument("--n_therm",   type=int,   default=200)
    parser.add_argument("--n_meas",    type=int,   default=500)
    parser.add_argument("--n_skip",    type=int,   default=5)
    parser.add_argument("--md_steps",  type=int,   default=20)
    parser.add_argument("--step_size", type=float, default=0.015)
    parser.add_argument("--seed",      type=int,   default=42)
    args, _ = parser.parse_known_args()
    np.random.seed(args.seed)
    run_hmc(
        Ns=args.Ns, Nt=args.Nt, beta=args.beta,
        n_therm=args.n_therm, n_meas=args.n_meas, n_skip=args.n_skip,
        md_steps=args.md_steps, step_size=args.step_size,
        verbose=True,
    )
