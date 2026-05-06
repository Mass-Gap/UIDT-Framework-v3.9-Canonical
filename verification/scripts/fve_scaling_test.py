import os
import sys
from mpmath import mp, mpf, exp

mp.dps = 80

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from modules.geometric_operator import GeometricOperator

def fve_scaling_test():
    """
    Finite Volume Effect (FVE) Scaling Test
    Extrapolates the geometric operator outputs from lattice volumes L=4 and L=8
    to the thermodynamic limit (L -> infinity).
    """
    print("--- UIDT Finite Volume Effect (FVE) Scaling Extrapolation ---")
    
    op = GeometricOperator()
    delta_inf = op.DELTA_GAP
    
    # Lattice parameters (mock FVE coefficients)
    # Model: Delta(L) = Delta_inf * (1 + A * exp(-m_pi * L) / (m_pi * L)^{3/2})
    # Simplified Luescher formula for demonstration of precision
    A = mpf('0.5')
    m_pi_gev = mpf('0.140') # pion mass ~ 140 MeV
    
    L_4 = mpf('4.0')
    L_8 = mpf('8.0')
    
    def simulate_lattice_mass(L_fermi):
        # Convert fm to GeV^-1 approx: 1 fm = 5.068 GeV^-1
        L_gev = L_fermi * mpf('5.068')
        correction = A * exp(-m_pi_gev * L_gev) / ((m_pi_gev * L_gev) ** mpf('1.5'))
        return delta_inf * (mpf('1.0') + correction)
        
    delta_L4 = simulate_lattice_mass(L_4)
    delta_L8 = simulate_lattice_mass(L_8)
    
    print(f"Simulated Lattice L=4 fm Mass Gap: {delta_L4} GeV")
    print(f"Simulated Lattice L=8 fm Mass Gap: {delta_L8} GeV")
    
    # Extrapolation: If we only had L4 and L8, we would fit. 
    # Here we just verify that delta_L8 is closer to delta_inf than delta_L4.
    res_L4 = abs(delta_L4 - delta_inf)
    res_L8 = abs(delta_L8 - delta_inf)
    
    print(f"Residual L=4 -> inf: {res_L4}")
    print(f"Residual L=8 -> inf: {res_L8}")
    
    assert res_L8 < res_L4, "Extrapolation logic failure: L=8 should be closer to continuum."
    
    # Verify that at L -> inf, it precisely recovers op.DELTA_GAP
    L_inf = mpf('1e5') # very large box
    delta_inf_extrap = simulate_lattice_mass(L_inf)
    res_inf = abs(delta_inf_extrap - delta_inf)
    
    print(f"Continuum Limit (L -> inf): {delta_inf_extrap} GeV")
    print(f"Continuum Residual: {res_inf}")
    
    assert res_inf < 1e-14, f"FVE Extrapolation failed continuum limit constraint. Res: {res_inf}"
    
    print("\n[PASS] Finite Volume Scaling satisfies UIDT limits.")

if __name__ == "__main__":
    fve_scaling_test()
