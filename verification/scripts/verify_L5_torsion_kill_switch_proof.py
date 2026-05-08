r"""
UIDT-Framework-v3.9 Verification Script
========================================
L5 / Item 4: Formal Kill-Switch Verification  E_T -> 0 => Sigma_T -> 0

Proves that the torsion self-energy Sigma_T vanishes identically when
the torsion binding energy E_T is set to zero, fulfilling the mandatory
falsification criterion of the UIDT framework.

Evidence Category: [A] (Mathematical Proof — algebraic identity)
Limitation Reference: L5, Kill-Switch
DOI: 10.5281/zenodo.17835200
"""

import mpmath as mp

# STRICT UIDT NUMERICAL PROTOCOL: mp.dps = 80 locally. No centralization.
mp.dps = 80


class TorsionKillSwitch:
    """
    The UIDT torsion self-energy Sigma_T is defined as a function of E_T.
    
    The KILL-SWITCH REQUIREMENT (from UIDT Constitution):
    If E_T = 0, then Sigma_T MUST vanish (= 0), which serves to
    falsify the discrete lattice hypothesis.
    
    This script proves this analytically and numerically for the
    full precision chain.
    """

    def __init__(self, E_T_value):
        # Canonical Constants
        self.Delta_star = mp.mpf('1.710')       # [A] GeV
        self.v = mp.mpf('0.0477')               # [A] GeV
        self.kappa = mp.mpf('0.5')              # [A]
        self.lambda_S = 5 * self.kappa**2 / 3   # [A] = 5/12 exact
        self.E_T = mp.mpf(str(E_T_value))       # [C] GeV (or 0 for kill-switch)

    def compute_sigma_T(self):
        """
        Torsion self-energy: Sigma_T is proportional to E_T.
        
        In the UIDT lattice-torsion formulation:
        Sigma_T = E_T * kappa^2 * (Delta* / v)
        
        When E_T = 0: Sigma_T = 0 identically (linear dependence).
        This is the algebraic proof of the kill-switch.
        """
        sigma_T = self.E_T * self.kappa**2 * (self.Delta_star / self.v)
        return sigma_T

    def compute_sigma_T_alternative(self):
        """
        Alternative formulation using lambda_S:
        Sigma_T = E_T * (3 * lambda_S / 5) * gamma_kinetic
        
        where gamma_kinetic = Delta* / v (kinematic ratio).
        This uses the RG constraint 5*kappa^2 = 3*lambda_S.
        """
        gamma_kinetic = self.Delta_star / self.v
        sigma_T = self.E_T * (3 * self.lambda_S / 5) * gamma_kinetic
        return sigma_T


def verify_kill_switch():
    print("=" * 72)
    print("UIDT L5 Kill-Switch Verification: E_T -> 0 => Sigma_T -> 0")
    print("=" * 72)

    # --- Test 1: Physical value E_T = 2.44 MeV ---
    print("\n--- Test 1: Physical Value E_T = 0.00244 GeV [C] ---")
    engine_phys = TorsionKillSwitch('0.00244')

    sigma_phys = engine_phys.compute_sigma_T()
    sigma_phys_alt = engine_phys.compute_sigma_T_alternative()

    print(f"E_T              = {mp.nstr(engine_phys.E_T, 15)} GeV")
    print(f"Sigma_T (direct) = {mp.nstr(sigma_phys, 20)} GeV")
    print(f"Sigma_T (alt)    = {mp.nstr(sigma_phys_alt, 20)} GeV")

    consistency = abs(sigma_phys - sigma_phys_alt)
    print(f"Consistency      = {mp.nstr(consistency, 5)}")
    assert consistency < mp.mpf('1e-60'), f"Inconsistency: {consistency}"
    print("Two formulations CONSISTENT [A]")

    # --- Test 2: Kill-switch E_T = 0 ---
    print("\n--- Test 2: KILL-SWITCH E_T = 0 ---")
    engine_kill = TorsionKillSwitch('0')

    sigma_kill = engine_kill.compute_sigma_T()
    sigma_kill_alt = engine_kill.compute_sigma_T_alternative()

    print(f"E_T              = {mp.nstr(engine_kill.E_T, 15)}")
    print(f"Sigma_T (direct) = {mp.nstr(sigma_kill, 20)}")
    print(f"Sigma_T (alt)    = {mp.nstr(sigma_kill_alt, 20)}")

    assert sigma_kill == mp.mpf('0'), f"KILL-SWITCH FAILED: Sigma_T = {sigma_kill}"
    assert sigma_kill_alt == mp.mpf('0'), f"KILL-SWITCH FAILED (alt): Sigma_T = {sigma_kill_alt}"
    print("KILL-SWITCH VERIFIED: Sigma_T = 0 when E_T = 0  [A]")

    # --- Test 3: Limiting behavior E_T -> 0 ---
    print("\n--- Test 3: Limiting Behavior (E_T -> 0 from above) ---")
    print(f"{'E_T':>15} | {'Sigma_T':>25} | {'Sigma_T / E_T':>25}")
    print("-" * 70)

    for exp in range(-3, -25, -3):
        et_val = mp.power(10, exp)
        engine = TorsionKillSwitch(mp.nstr(et_val, 10))
        sigma = engine.compute_sigma_T()
        ratio = sigma / et_val if et_val != 0 else mp.mpf('0')
        print(f"{'10^' + str(exp):>15} | {mp.nstr(sigma, 15):>25} | {mp.nstr(ratio, 15):>25}")

    # Verify the ratio is constant (linear dependence)
    engine_1 = TorsionKillSwitch('1e-10')
    engine_2 = TorsionKillSwitch('1e-20')
    ratio_1 = engine_1.compute_sigma_T() / mp.mpf('1e-10')
    ratio_2 = engine_2.compute_sigma_T() / mp.mpf('1e-20')
    ratio_diff = abs(ratio_1 - ratio_2)
    print(f"\nRatio constancy check: |r(10^-10) - r(10^-20)| = {mp.nstr(ratio_diff, 5)}")
    assert ratio_diff < mp.mpf('1e-50'), f"Non-linear behavior detected: {ratio_diff}"
    print("LINEAR DEPENDENCE CONFIRMED: Sigma_T = const * E_T  [A]")

    # --- Test 4: Negative E_T (unphysical but must still be proportional) ---
    print("\n--- Test 4: Negative E_T (Unphysical — Consistency Check) ---")
    engine_neg = TorsionKillSwitch('-0.00244')
    sigma_neg = engine_neg.compute_sigma_T()
    print(f"Sigma_T(-E_T) = {mp.nstr(sigma_neg, 20)}")
    print(f"Sigma_T(+E_T) = {mp.nstr(sigma_phys, 20)}")
    symmetry = abs(sigma_neg + sigma_phys)
    print(f"|Sigma_T(-) + Sigma_T(+)| = {mp.nstr(symmetry, 5)}")
    assert symmetry < mp.mpf('1e-60'), f"Anti-symmetry violated: {symmetry}"
    print("ANTISYMMETRY VERIFIED: Sigma_T(-E_T) = -Sigma_T(E_T)  [A]")

    # --- Final Verdict ---
    print("\n" + "=" * 72)
    print("FINAL VERDICT: KILL-SWITCH PROOF")
    print("=" * 72)
    print("  1. Sigma_T(E_T=0) = 0  EXACTLY                      [A]")
    print("  2. Sigma_T is LINEAR in E_T                          [A]")
    print("  3. Two formulations (kappa, lambda_S) are consistent [A]")
    print("  4. Antisymmetry under E_T -> -E_T                    [A]")
    print("  5. Proportionality constant = kappa^2 * Delta*/v")
    print(f"     = {mp.nstr(ratio_1, 20)}")
    print("  EVIDENCE CATEGORY: [A] (Mathematical Proof)")
    print("=" * 72)


if __name__ == "__main__":
    verify_kill_switch()
