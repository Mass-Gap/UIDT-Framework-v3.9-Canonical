#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 MODULE: OPTIMIZED LATTICE CLASS
===========================================
Status: Canonical / Clean State / Vectorized
Description: High-Performance Lattice class with GPU support (CuPy) 
             and fully vectorized HMC updates using the Cayley-Hamilton kernel.
"""

import numpy as np

# 1. GPU/CPU Configuration
try:
    import cupy as cp
    xp = cp
    def to_gpu(arr): return cp.asarray(arr)
    def to_cpu(arr): return arr.get()
except ImportError:
    xp = np
    def to_gpu(arr): return arr
    def to_cpu(arr): return arr

# 2. Math Kernel Import (v3.6.1 Precision)
try:
    # Must match the filename with underscores defined previously
    from UIDTv3_6_1_su3_expm_cayley_hamiltonian_Modul import su3_expm_hybrid
except ImportError:
    print("⚠️ WARNING: UIDTv3_2_cayley_hamiltonian module not found.")
    print("   Falling back to slow scipy.linalg.expm.")
    from scipy.linalg import expm
    def su3_expm_hybrid(A, xp_local=xp):
        # Slow fallback
        if xp_local == np:
            return np.array([expm(m) for m in A])
        else:
            return cp.array([expm(m) for m in cp.asnumpy(A)])

# =============================================================================
# 3. CORE LATTICE CLASS
# =============================================================================

class UIDTLatticeOptimized:
    """
    UIDT v3.6.1 Optimized Lattice
    Features:
    - Fully vectorized Wilson Gauge Force
    - Cayley-Hamilton SU(3) Updates (10-50x speedup)
    - Memory-aligned GPU structures
    """
    
    def __init__(self, cfg, kappa=0.500, Lambda=1.0, 
                 m_S=1.705, lambda_S=0.417, v_vev=0.0477): # v3.6.1 Clean State
        
        self.cfg = cfg
        self.Nx = cfg.N_spatial
        self.Ny = cfg.N_spatial
        self.Nz = cfg.N_spatial
        self.Nt = cfg.N_temporal
        
        # Physics Parameters
        self.kappa = kappa
        self.Lambda = Lambda
        self.m_S = m_S
        self.lambda_S = lambda_S
        self.v_vev = v_vev
        
        # --- Optimized Initialization (Scalar Field S) ---
        # S(x) = v_vev + fluctuations
        shapeS = (self.Nx, self.Ny, self.Nz, self.Nt)
        
        # Reproducible random state
        seed = getattr(cfg, 'seed', 42)
        rng = xp.random.RandomState(seed + 7)
        
        S_init = (v_vev + 1e-3 * rng.randn(*shapeS)).astype(float)
        
        self.S = S_init
        self.Ps = xp.zeros_like(self.S) # Conjugate momentum
        
        # --- Initialization (Gauge Field U) ---
        # Cold Start: U = Identity
        shapeU = (self.Nx, self.Ny, self.Nz, self.Nt, 4, 3, 3)
        self.U = to_gpu(xp.zeros(shapeU, dtype=complex))
        
        # Fill diagonal with 1.0 (Identity matrices)
        for i in range(3):
            self.U[..., i, i] = 1.0
            
        self.Pu = None # Momentum P is generated fresh each trajectory
        
        # Performance Monitoring
        self.acceptance_rate = 0.0
        self.avg_delta_H = 0.0
        
    def update_U_vectorized(self, Pu, step_size):
        """
        Fully vectorized Link Update using Cayley-Hamilton.
        U' = exp(i * P * dt) * U
        """
        # Anti-hermitian matrix element for SU(3) group generation
        # Pu is hermitian, so i*Pu is anti-hermitian
        A = 1j * Pu * step_size
        
        # Batch-Update of all links simultaneously (High-Performance Kernel)
        expA = su3_expm_hybrid(A, xp_local=xp)
        
        # Vectorized Matrix Multiplication
        self.U = xp.matmul(expA, self.U)
        
    def update_S_vectorized(self, Ps, step_size):
        """Vectorized Scalar Field Update (Leapfrog)"""
        self.S = self.S + step_size * Ps
        
    def gauge_force_vectorized(self):
        """
        Fully vectorized Gauge Force calculation (Derivative of Wilson Action).
        Uses periodic boundary conditions via xp.roll.
        
        Returns:
            F (Tensor): Force matrices for the momentum update P_dot = F
        """
        U = self.U
        beta = self.cfg.beta
        
        # Initialize Force Tensor
        F = xp.zeros_like(U, dtype=complex)
        
        # Pre-allocate staple_sum (Optimization: moved out of loop)
        staple_sum = xp.zeros_like(U[..., 0, :, :])

        # Calculate Staples for each direction mu
        for mu in range(4):
            staple_sum.fill(0)
            
            for nu in range(4):
                if nu == mu:
                    continue
                    
                # --- Positive Staple ---
                # U_nu(x+mu) * U_mu_dag(x+nu) * U_nu_dag(x)
                
                U_nu_x_plus_mu = self.roll_matrix(U, nu, mu, forward=True)
                
                # U_mu(x+nu)^dagger
                U_mu_x_plus_nu_dag = self.roll_matrix(U, mu, nu, forward=True).conj().swapaxes(-1, -2)
                
                # U_nu(x)^dagger
                U_nu_x_dag = U[..., nu, :, :].conj().swapaxes(-1, -2)
                
                staple_pos = xp.matmul(U_nu_x_plus_mu, 
                                     xp.matmul(U_mu_x_plus_nu_dag, U_nu_x_dag))
                
                # --- Negative Staple ---
                # U_nu_dag(x+mu-nu) * U_mu(x-nu) * U_nu(x-nu)
                
                # U_nu_dag(x+mu-nu) -> requires shifting back nu, then forward mu
                U_nu_dag_x_plus_mu_minus_nu = self.roll_matrix(
                    U, nu, mu, forward=True, shift_second_axis=nu, shift_second_dir=-1
                ).conj().swapaxes(-1, -2)
                
                # U_mu(x-nu)
                U_mu_x_minus_nu = self.roll_matrix(U, mu, nu, forward=False)
                
                # U_nu(x-nu)
                U_nu_x_minus_nu = self.roll_matrix(U, nu, nu, forward=False)
                
                staple_neg = xp.matmul(U_nu_dag_x_plus_mu_minus_nu,
                                     xp.matmul(U_mu_x_minus_nu, U_nu_x_minus_nu))
                
                staple_sum += staple_pos + staple_neg
            
            # --- Force Calculation ---
            # F_mu = -beta/3 * TA(U_mu * staple_sum_dag)
            # where TA(X) = (X - X_dag)/2 - Tr(X-X_dag)/6 * I
            
            # U_mu * Staple_dag
            M = xp.matmul(U[..., mu, :, :], staple_sum.conj().swapaxes(-1, -2))
            
            # Anti-Hermitian Part (times 2)
            M_ah = M - M.conj().swapaxes(-1, -2)
            
            # Make Traceless
            trace = xp.trace(M_ah, axis1=-2, axis2=-1)
            M_ah_trless = M_ah - (trace[..., None, None] / 3.0) * xp.eye(3, dtype=complex)
            
            # Final Scaling: F = -i * (beta/6) * M_ah_trless
            # (Matches standard HMC convention P_dot = Force)
            F[..., mu, :, :] = (-1j) * (beta / 6.0) * M_ah_trless
        
        return F
    
    def roll_matrix(self, U, target_idx, axis_idx, forward=True, 
                    shift_second_axis=None, shift_second_dir=0):
        """
        Helper for periodic shifts (Toroidal Boundary Conditions).
        OPTIMIZED: Uses array slicing instead of xp.roll for better performance.
        
        Args:
            U: Gauge field
            target_idx: The link direction (nu/mu) we want to fetch
            axis_idx: The axis along which we shift
            forward: True (+1 step in lattice), False (-1 step)
            shift_second_axis: Optional secondary shift (for negative staples)
        """
        # Select component
        tensor = U[..., target_idx, :, :]
        
        # --- Primary Shift ---
        # forward=True -> shift=-1 (left shift). [0, 1, 2] -> [1, 2, 0]
        # Slicing: [1:] + [:1]
        # forward=False -> shift=1 (right shift). [0, 1, 2] -> [2, 0, 1]
        # Slicing: [-1:] + [:-1]

        # Create slices dynamically for arbitrary axis
        sl_1 = [slice(None)] * tensor.ndim
        sl_2 = [slice(None)] * tensor.ndim
        
        if forward:
            sl_1[axis_idx] = slice(1, None)
            sl_2[axis_idx] = slice(None, 1)
            p1 = tensor[tuple(sl_1)]
            p2 = tensor[tuple(sl_2)]
            res = xp.concatenate((p1, p2), axis=axis_idx)
        else:
            sl_1[axis_idx] = slice(-1, None)
            sl_2[axis_idx] = slice(None, -1)
            p1 = tensor[tuple(sl_1)]
            p2 = tensor[tuple(sl_2)]
            res = xp.concatenate((p1, p2), axis=axis_idx)

        # --- Secondary Shift ---
        if shift_second_axis is not None:
            # shift_second_dir: -1 (left/forward) or 1 (right/backward)
            # If dir is -1, treat as forward=True
            # If dir is 1, treat as forward=False
            is_fwd_2 = (shift_second_dir == -1)
            
            sl_1 = [slice(None)] * res.ndim
            sl_2 = [slice(None)] * res.ndim
            
            if is_fwd_2:
                sl_1[shift_second_axis] = slice(1, None)
                sl_2[shift_second_axis] = slice(None, 1)
                p1 = res[tuple(sl_1)]
                p2 = res[tuple(sl_2)]
                res = xp.concatenate((p1, p2), axis=shift_second_axis)
            else:
                sl_1[shift_second_axis] = slice(-1, None)
                sl_2[shift_second_axis] = slice(None, -1)
                p1 = res[tuple(sl_1)]
                p2 = res[tuple(sl_2)]
                res = xp.concatenate((p1, p2), axis=shift_second_axis)
            
        return res