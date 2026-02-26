"""
Verification Script: Heavy Quark Spectroscopy Predictions
UIDT Framework TICK-20260224-Phase3_Discoveries
"""

import sys
from mpmath import mp, mpf

# Local precision initialization
mp.dps = 80

import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from modules.harmonic_predictions import HarmonicPredictor

def verify_heavy_quark_predictions():
    print("="*60)
    print("UIDT VERIFICATION: HEAVY QUARK PREDICTIONS (LHCb)")
    print("="*60)
    
    # Fundamental anchor frequency derived from Topology
    f_vac_gev = mpf('0.10710') 
    
    # Initialize predictor
    predictor = HarmonicPredictor(vacuum_freq_gev=f_vac_gev)
    
    m_omega, err_omega = predictor.predict_omega_bbb()
    m_tetra, err_tetra = predictor.predict_tetraquark_cccc()
    
    print("\n[1] Derivation Chain")
    print(f"    f_vac  = {f_vac_gev * 1000} MeV")
    print(f"    M(Omega_bbb) = 135 * f_vac = {float(m_omega):.4f} GeV ± {float(err_omega):.2f} GeV")
    print(f"    M(cccc)  = 42 * f_vac  = {float(m_tetra):.4f} GeV ± {float(err_tetra):.2f} GeV")
    
    # Cross-reference known targets and error magnitudes
    target_omega = mpf('14.4585')
    target_tetra = mpf('4.4982')
    
    target_err_omega = mpf('0.0675')
    target_err_tetra = mpf('0.0210')
    
    residual_omega = abs(m_omega - target_omega)
    residual_tetra = abs(m_tetra - target_tetra)
    
    err_residual_omega = abs(err_omega - target_err_omega)
    err_residual_tetra = abs(err_tetra - target_err_tetra)
    
    print("\n[2] Numerical Constraint Check")
    print(f"    Omega_bbb Residual: {residual_omega}")
    print(f"    cccc Residual:  {residual_tetra}")
    print(f"    Omega_bbb Delta Residual: {err_residual_omega}")
    print(f"    cccc Delta Residual: {err_residual_tetra}")
    
    # Assert mass predictions and error propagations
    if (residual_omega < mpf('1e-4') and residual_tetra < mpf('1e-4') and
        err_residual_omega < mpf('1e-14') and err_residual_tetra < mpf('1e-14')):
        print("\n    [PASS] Both predictions and uncertainties match internal consistency targets.")
    else:
        print("\n    [FAIL] Targets do not match harmonic factors.")
        sys.exit(1)

if __name__ == "__main__":
    verify_heavy_quark_predictions()
