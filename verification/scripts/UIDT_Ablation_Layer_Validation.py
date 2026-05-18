"""
UIDT Ablation Layer Validation
------------------------------
Cross-Validation of Causal Set Dimensionality vs UIDT Constants.
"""

import sys
import os
import mpmath as mp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from modules.causal_integration.ablation_diagnostics import AblationDiagnostics

mp.dps = 80

def main():
    diagnostic = AblationDiagnostics()
    print("--- UIDT ABLATION LAYER VALIDATION ---")
    print("Executing Myrheim-Meyer dimensional scaling vs Gamma (16.339)")
    
    sweep_results = diagnostic.run_dimension_sweep()
    
    print("\n[Results]")
    for res in sweep_results:
        dim = res['dimension']
        gamma = mp.nstr(res['emergent_gamma'], 6)
        res_err = mp.nstr(res['residual'], 15)
        
        status = "PASS (Consistent)" if res['residual'] < mp.mpf('1.0') else "DEVIATION"
        print(f"Dimension D={dim} | Emergent Gamma: {gamma} | Residual: {res_err} | {status}")
        
    # Strictly require D=4 to match phenomenological baseline
    d4_res = [r for r in sweep_results if r['dimension'] == 4][0]
    if d4_res['residual'] > mp.mpf('1e-10'):
        print("\nWARNING: Baseline 4D topology does not resolve to Gamma=16.339.")
        print("This isolates limitation L4 scaling failure.")
    else:
        print("\nSUCCESS: 4D geometric scalar strongly matches UIDT Constants.")

if __name__ == "__main__":
    main()
