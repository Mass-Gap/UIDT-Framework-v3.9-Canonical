import sys
import os
from mpmath import mp, mpf

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from modules.covariant_unification import CovariantUnification

# AGENTS.md Anti-Centralization Rule: Local precision declaration
mp.dps = 80

def verify_su3_color_projection():
    print("="*70)
    print("UIDT VERIFICATION SUITE: SU(3) COLOR PROJECTION FACTOR [O2]")
    print("="*70)

    try:
        cu = CovariantUnification(gamma_uidt=mpf('16.339'))
    except Exception as e:
        print(f"Error initializing CovariantUnification: {e}")
        sys.exit(1)

    print("\n--- Section 1: Compute gamma_CSF ---")
    gamma_csf = cu.derive_csf_anomalous_dimension()
    print(f"Computed gamma_CSF : {gamma_csf}")

    if gamma_csf <= 0:
        print("[!] FATAL: gamma_CSF must be positive.")
        sys.exit(1)

    print("\n--- Section 2: Compute Ratio to FRG target ---")
    eta_csf_frg = mpf('0.504')
    ratio = eta_csf_frg / gamma_csf
    deviation = abs(ratio - mpf('3'))
    
    print(f"Target eta_CSF_FRG : {eta_csf_frg}")
    print(f"Ratio (eta/gamma)  : {ratio} (~ N_c)")
    print(f"Deviation from 3   : {deviation}")

    print("\n--- Section 3: Evidence Classification Block ---")
    print(f"Observation  : eta_CSF(FRG) / gamma_CSF(UIDT) ≈ 2.986 ≈ 3 = N_c(SU(3)).")
    print("Evidence     : [Category D - numerical coincidence].")
    print("The formula for gamma_CSF was not designed to produce this ratio.")
    print("The interpretation as macroscopic SU(3) color projection requires an")
    print("independent derivation connecting the conformal density mapping to")
    print("the color gauge group. Risk flag: post-hoc pattern matching.")
    print("="*70)

    return {
        "gamma_csf": mp.nstr(gamma_csf),
        "ratio": mp.nstr(ratio),
        "deviation": mp.nstr(deviation)
    }

if __name__ == "__main__":
    verify_su3_color_projection()
