import os
import sys

# Ensure precise arithmetic per UIDT rules
import mpmath
mpmath.mp.dps = 80

def derive_weff():
    """
    Simulates the differential flow of the vacuum information density S(t)
    on a FRW background and calculates the effective equation of state w_eff(S).
    """
    print("==================================================")
    print("UIDT RESEARCH-MODE: Analytical Derivation of w_eff")
    print("==================================================")
    
    # ----------------------------------------------------
    # 1. Canonical Constants (mpmath precision)
    # ----------------------------------------------------
    # Category A: Mathematical proven / exact mappings
    v = mpmath.mpf('0.0477')  # 47.7 MeV in GeV
    kappa = mpmath.mpf('0.5')
    
    # RG Constraint: 5*\kappa^2 = 3*\lambda_S
    lambda_s = (mpmath.mpf('5') * kappa**2) / mpmath.mpf('3')
    
    # Torsion gap E_T (Category C)
    E_t = mpmath.mpf('0.00244')  # 2.44 MeV in GeV
    
    # Effective potential shifted by E_T for macroscopic late-time boundary
    # V(S) = (lambda_s / 4) * (S^2 - v_eff^2)^2
    # The torsion gap slightly offsets the true minimum.
    # We define v_eff such that the energy at the minimum is strictly positive,
    # or the VEV is shifted. Let's shift v to v_eff.
    v_eff = v + E_t
    
    print(f"[*] Vacuum VEV (canonical):  {v}")
    print(f"[*] Effective VEV (w/ E_T):  {v_eff}")
    print(f"[*] Coupling lambda_s:       {lambda_s}")
    
    # ----------------------------------------------------
    # 2. Differential Equation Setup
    # ----------------------------------------------------
    # We solve: S''(t) + 3H S'(t) + V'(S) = 0
    # where V(S) = (lambda_s / 4) * (S^2 - v_eff^2)^2
    # V'(S) = lambda_s * S * (S^2 - v_eff^2)
    # rho_S = 1/2 S'^2 + V(S)
    # p_S   = 1/2 S'^2 - V(S)
    # w_eff = p_S / rho_S
    
    def V(S):
        return (lambda_s / mpmath.mpf('4')) * (S**2 - v_eff**2)**2
        
    def dV_dS(S):
        return lambda_s * S * (S**2 - v_eff**2)
        
    # Standard scalar FRW relation: H = sqrt((8*pi*G/3) * rho_S)
    # Since we are in the vacuum topology mapping, we use a normalized G_eff
    # such that H_eff = sqrt(rho_S).
    def H_eff(rho):
        if rho <= 0:
            return mpmath.mpf('0')
        return mpmath.sqrt(rho)
        
    # Initial conditions (Pre-geometric inflation start)
    # S starts near 0 (unbroken symmetry state)
    S_t = mpmath.mpf('0.0001')
    S_dot = mpmath.mpf('0.0')
    
    dt = mpmath.mpf('0.001')
    t_max = mpmath.mpf('50.0')
    
    t = mpmath.mpf('0.0')
    
    # Trackers for convergence
    w_eff_current = mpmath.mpf('0')
    rho_current = mpmath.mpf('0')
    p_current = mpmath.mpf('0')
    
    print("\n[*] Starting RK4 Integration of Vacuum Trajectory...")
    print(f"{'Time':<10} | {'S(t)':<20} | {'w_eff':<20} | {'rho_S':<20}")
    print("-" * 75)
    
    step_count = 0
    while t < t_max:
        # Calculate thermodynamics
        V_current = V(S_t)
        rho_current = mpmath.mpf('0.5') * S_dot**2 + V_current
        p_current   = mpmath.mpf('0.5') * S_dot**2 - V_current
        
        # Prevent division by zero
        if rho_current > 1e-60:
            w_eff_current = p_current / rho_current
        else:
            w_eff_current = mpmath.mpf('-1.0')
            
        # Print status every certain interval
        if step_count % 5000 == 0:
            print(f"{float(t):<10.3f} | {float(S_t):<20.8f} | {float(w_eff_current):<20.8f} | {float(rho_current):<20.8e}")
            
        # RK4 for S''(t) = - 3 H_eff(rho) S'(t) - dV_dS(S_t)
        # Let state Y = [S, S_dot]
        # dY/dt = [S_dot, -3*H*S_dot - dV_dS(S)]
        
        def derivatives(S, S_d):
            r = mpmath.mpf('0.5') * S_d**2 + V(S)
            h = H_eff(r)
            return S_d, -mpmath.mpf('3') * h * S_d - dV_dS(S)
            
        # RK4 Steps
        k1_S, k1_Sd = derivatives(S_t, S_dot)
        
        S_mid1 = S_t + mpmath.mpf('0.5') * dt * k1_S
        Sd_mid1 = S_dot + mpmath.mpf('0.5') * dt * k1_Sd
        k2_S, k2_Sd = derivatives(S_mid1, Sd_mid1)
        
        S_mid2 = S_t + mpmath.mpf('0.5') * dt * k2_S
        Sd_mid2 = S_dot + mpmath.mpf('0.5') * dt * k2_Sd
        k3_S, k3_Sd = derivatives(S_mid2, Sd_mid2)
        
        S_end = S_t + dt * k3_S
        Sd_end = S_dot + dt * k3_Sd
        k4_S, k4_Sd = derivatives(S_end, Sd_end)
        
        S_t = S_t + (dt / mpmath.mpf('6')) * (k1_S + mpmath.mpf('2')*k2_S + mpmath.mpf('2')*k3_S + k4_S)
        S_dot = S_dot + (dt / mpmath.mpf('6')) * (k1_Sd + mpmath.mpf('2')*k2_Sd + mpmath.mpf('2')*k3_Sd + k4_Sd)
        
        t += dt
        step_count += 1

    print("-" * 75)
    print(f"[*] Final S(t):     {S_t}")
    print(f"[*] Final S'(t):    {S_dot}")
    print(f"[*] Final w_eff:    {w_eff_current}")
    
    # ----------------------------------------------------
    # 3. Verification of Limits
    # ----------------------------------------------------
    print("\n[*] Convergence Verification")
    # Expected VEV
    vev_residual = abs(S_t - v_eff)
    print(f"    VEV Residual:   {vev_residual}")
    
    # Expected w_eff stabilization near -1 (actually we want to show it goes to -1 or -0.99)
    w_expected = mpmath.mpf('-1.0')
    w_residual = abs(w_eff_current - w_expected)
    print(f"    w_eff Residual: {w_residual}")
    
    # If residual is extremely small, it reached strict de Sitter.
    # To get w_eff = -0.99, we need a residual non-zero kinetic energy or a modified potential.
    # Since we are in RESEARCH-MODE, we will document this finding.
    if w_residual < mpmath.mpf('1e-10'):
        print("\n[RESULT] Trajectory converged to strict de Sitter (w_eff = -1) [Category A-].")
        print("To stabilize at w_eff = -0.99 [Category C], a residual macroscopic kinetic flow")
        print("or a structural perturbation (e.g. holographic mapping) is required.")

if __name__ == "__main__":
    derive_weff()
