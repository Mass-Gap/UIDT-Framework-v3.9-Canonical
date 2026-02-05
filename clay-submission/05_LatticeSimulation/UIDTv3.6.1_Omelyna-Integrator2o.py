#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 OMELYAN INTEGRATOR MODULE
=====================================
Status: Canonical / Clean State
Description: Second-order symplectic integrator for the Hybrid Monte Carlo algorithm.
             Optimized for energy conservation in SU(3) gauge theory.
"""

import numpy as np

# Note: This module is designed to be mixed into the main Lattice class.
# It assumes 'self' has access to U, S, Pu, Ps, and force calculation methods.
# Placeholder for XP (Numpy/Cupy switch) handled in main context.

def omelyan_integrator_2nd_order(self, n_steps=10, step_size=0.02, lambda_omelyan=0.193):
    """
    Omelyan-Integrator 2. Ordnung für optimale Energieerhaltung.
    λ ≈ 0.193 minimiert den Fehler 4. Ordnung im Hamilton-System.
    """
    # Omelyan-Koeffizienten
    xi = lambda_omelyan
    gamma = 0.5 - xi
    
    # Initiale Momenta (Randomisierung)
    self.Pu = self.random_momenta()
    # Skalar-Impulse: Normalverteiltes Rauschen
    self.Ps = self.xp.array(np.random.randn(self.Nx, self.Ny, self.Nz, self.Nt), dtype=float)
    
    # Store initial configuration for Metropolis check
    U_old = self.U.copy()
    S_old = self.S.copy()
    
    # Initial Hamiltonian
    H_initial = self._compute_hamiltonian()
    
    # --- OMELYAN INTEGRATOR SCHLEIFE ---
    
    # 1. Initial half step for momenta (P)
    gauge_F = self.gauge_force_vectorized()
    scalar_F = self.scalar_force_field_vectorized()
    
    self.Pu = self.Pu - xi * step_size * gauge_F
    self.Ps = self.Ps - xi * step_size * scalar_F
    
    # 2. Multiple steps
    for step in range(n_steps):
        # Update coordinates (Q) - first half
        self.update_U_vectorized(self.Pu, gamma * step_size)
        self.update_S_vectorized(self.Ps, 0.5 * step_size)
        
        # Force computation at intermediate position
        gauge_F = self.gauge_force_vectorized()
        scalar_F = self.scalar_force_field_vectorized()
        
        # Update momenta (P) - full step
        self.Pu = self.Pu - (1 - 2*xi) * step_size * gauge_F
        self.Ps = self.Ps - (1 - 2*xi) * step_size * scalar_F
        
        # Update coordinates (Q) - second half
        self.update_U_vectorized(self.Pu, gamma * step_size)
        self.update_S_vectorized(self.Ps, 0.5 * step_size)
        
        # Final force update (except last step)
        if step < n_steps - 1:
            gauge_F = self.gauge_force_vectorized()
            scalar_F = self.scalar_force_field_vectorized()
            self.Pu = self.Pu - 2*xi * step_size * gauge_F
            self.Ps = self.Ps - 2*xi * step_size * scalar_F
    
    # 3. Final half step for momenta (P)
    gauge_F = self.gauge_force_vectorized()
    scalar_F = self.scalar_force_field_vectorized()
    self.Pu = self.Pu - (1 - xi) * step_size * gauge_F
    self.Ps = self.Ps - (1 - xi) * step_size * scalar_F
    
    # --- METROPOLIS ACCEPT/REJECT ---
    H_final = self._compute_hamiltonian()
    delta_H = float(H_final - H_initial)
    
    # Acceptance decision
    accepted = False
    if self.xp.random.rand() < self.xp.exp(-delta_H):
        accepted = True
        self.acceptance_rate = 0.9 * self.acceptance_rate + 0.1
    else:
        # Reject: restore old configuration
        self.U = U_old
        self.S = S_old
        self.acceptance_rate = 0.9 * self.acceptance_rate
    
    self.avg_delta_H = 0.9 * self.avg_delta_H + 0.1 * abs(delta_H)
    
    return accepted, delta_H

def _compute_hamiltonian(self):
    """
    Berechnet den Gesamt-Hamiltonian H = T + V für den Metropolis-Test.
    T = Kinetische Energie der Impulse (P)
    V = Potentielle Energie (Wirkung S)
    """
    # Kinetische Energie (Gauge)
    def kinetic_energy_Pu(Pu):
        Pu_flat = Pu.reshape(-1, 3, 3)
        # Tr(P^2) for SU(3) momenta
        traces = self.xp.real(self.xp.trace(self.xp.matmul(Pu_flat, Pu_flat), axis1=1, axis2=2))
        return 0.5 * self.xp.sum(traces)
    
    kin_gauge = kinetic_energy_Pu(self.Pu)
    
    # Kinetische Energie (Scalar)
    kin_scalar = 0.5 * self.xp.sum(self.Ps**2)
    
    # Potentielle Energie (Action S_total)
    pot_energy = self.uidt_action()
    
    return pot_energy + kin_gauge + kin_scalar