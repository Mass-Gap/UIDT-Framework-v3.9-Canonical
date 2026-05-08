r"""
UIDT-Framework-v3.9 Verification Script
========================================
L4 / Item 2: 1-Loop Scalar Self-Energy Pi_S(p^2) at p = Delta*

Computes the momentum-dependent 1-loop scalar bubble integral
(Passarino-Veltman B_0 function) with internal mass m = v = 47.7 MeV
and external momentum p = Delta* = 1.710 GeV to extract the
anomalous dimension contribution Delta_gamma_1loop.

Evidence Category: [D] (Numerical Prediction — Path B hypothesis test)
Limitation Reference: L4
DOI: 10.5281/zenodo.17835200
"""

import mpmath as mp

# STRICT UIDT NUMERICAL PROTOCOL: mp.dps = 80 locally. No centralization.
mp.dps = 80


class ScalarSelfEnergy:
    """
    1-loop scalar self-energy for the UIDT vacuum information-density field.
    
    The scalar potential is V(phi) = (1/2) m^2 phi^2 + (lambda_S/4!) phi^4
    where m = v (vacuum expectation value) and lambda_S = 5*kappa^2/3.
    
    The 1-loop self-energy (bubble diagram) in d=4 with dimensional 
    regularization (MS-bar scheme) is:
    
    Pi_S(p^2) = (lambda_S / (32 pi^2)) * integral_0^1 dx 
                * ln[ (mu^2) / (m^2 - x(1-x) p^2) ]
    
    The anomalous dimension contribution is:
    
    gamma_phi = - d(ln Z_phi) / d(ln mu^2)
    
    where Z_phi = 1 - d Pi_S / d p^2 | _{p^2 = mu^2 = Delta*^2}
    """

    def __init__(self):
        # Canonical Constants (UIDT v3.9.6)
        self.Delta_star = mp.mpf('1.710')       # [A] GeV
        self.v = mp.mpf('0.0477')               # [A] GeV
        self.kappa = mp.mpf('0.5')              # [A]
        self.lambda_S = 5 * self.kappa**2 / 3   # [A] = 5/12 exact
        self.N_c = mp.mpf('3')                  # SU(3)

        # Derived
        self.m_sq = self.v**2                    # scalar mass squared
        self.p_sq = self.Delta_star**2           # external momentum squared
        self.mu_sq = self.p_sq                   # renormalization scale = Delta*

    def _integrand_pi(self, x):
        """Integrand of the scalar bubble: ln[mu^2 / (m^2 - x(1-x)*p^2)]"""
        denominator = self.m_sq - x * (1 - x) * self.p_sq
        if denominator <= 0:
            # Above threshold: use analytic continuation
            # ln(mu^2 / |D|) + i*pi -> take real part only
            return mp.log(self.mu_sq / abs(denominator))
        return mp.log(self.mu_sq / denominator)

    def _integrand_dpi_dp2(self, x):
        """
        Integrand of d Pi_S / d p^2:
        d/dp^2 [ ln(mu^2 / (m^2 - x(1-x)p^2)) ] = x(1-x) / (m^2 - x(1-x)p^2)
        """
        denominator = self.m_sq - x * (1 - x) * self.p_sq
        if abs(denominator) < mp.mpf('1e-60'):
            return mp.mpf('0')  # regulate at threshold
        return x * (1 - x) / denominator

    def compute_self_energy(self):
        """Compute Pi_S(p^2) at p^2 = Delta*^2."""
        prefactor = self.lambda_S / (32 * mp.pi**2)
        integral = mp.quad(self._integrand_pi, [0, 1])
        return prefactor * integral

    def compute_dpi_dp2(self):
        """Compute d Pi_S / d p^2 at p^2 = Delta*^2."""
        prefactor = self.lambda_S / (32 * mp.pi**2)
        integral = mp.quad(self._integrand_dpi_dp2, [0, 1])
        return prefactor * integral

    def compute_wave_function_renormalization(self):
        """
        Z_phi = 1 - d Pi_S / d p^2
        Anomalous dimension: eta = -d ln Z / d ln mu^2
        """
        dpi = self.compute_dpi_dp2()
        Z_phi = 1 - dpi
        return Z_phi, dpi

    def compute_anomalous_dimension_1loop(self):
        """
        At 1-loop in the scalar sector:
        eta_1loop = lambda_S / (16 pi^2) * correction_factor
        
        The correction factor encodes the momentum dependence at p = Delta*.
        """
        Z_phi, dpi = self.compute_wave_function_renormalization()
        
        # eta = p^2 * d/dp^2 [Pi(p^2)] / Z_phi (standard definition)
        eta = self.p_sq * dpi / Z_phi
        return eta, Z_phi, dpi

    def verify(self):
        print("=" * 72)
        print("UIDT L4: 1-Loop Scalar Self-Energy at p = Delta*")
        print("=" * 72)

        # --- Input parameters ---
        print("\n--- Canonical Inputs ---")
        print(f"Delta*    = {mp.nstr(self.Delta_star, 15)} GeV  [A]")
        print(f"v         = {mp.nstr(self.v, 15)} GeV  [A]")
        print(f"kappa     = {mp.nstr(self.kappa, 15)}      [A]")
        print(f"lambda_S  = {mp.nstr(self.lambda_S, 15)}      [A]")
        print(f"m^2       = {mp.nstr(self.m_sq, 15)} GeV^2")
        print(f"p^2       = {mp.nstr(self.p_sq, 15)} GeV^2")
        print(f"p^2 / m^2 = {mp.nstr(self.p_sq / self.m_sq, 10)}  (deep UV regime)")

        # --- RG constraint check ---
        print("\n--- RG Constraint ---")
        rg_residual = abs(5 * self.kappa**2 - 3 * self.lambda_S)
        print(f"|5 kappa^2 - 3 lambda_S| = {mp.nstr(rg_residual, 5)}")
        assert rg_residual < mp.mpf('1e-60'), "RG constraint violated!"
        print("RG constraint: PASS")

        # --- Self-energy computation ---
        print("\n--- 1-Loop Self-Energy Pi_S(Delta*^2) ---")
        Pi_S = self.compute_self_energy()
        print(f"Pi_S(Delta*^2) = {mp.nstr(Pi_S, 20)}")

        # --- Derivative ---
        print("\n--- d Pi_S / d p^2 ---")
        eta, Z_phi, dpi = self.compute_anomalous_dimension_1loop()
        print(f"d Pi_S / d p^2 = {mp.nstr(dpi, 20)}")
        print(f"Z_phi          = {mp.nstr(Z_phi, 20)}")
        print(f"eta_1loop      = {mp.nstr(eta, 20)}")

        # --- Target comparison ---
        print("\n--- Gap Analysis ---")
        gamma_bare = mp.mpf('49') / mp.mpf('3')
        gamma_ledger = mp.mpf('16.339')
        delta_gamma_target = gamma_ledger - gamma_bare

        print(f"Target delta_gamma = {mp.nstr(delta_gamma_target, 20)}")
        print(f"eta_1loop (scalar) = {mp.nstr(eta, 20)}")
        print(f"Ratio eta/target   = {mp.nstr(eta / delta_gamma_target, 10)}")

        # --- Assessment ---
        print("\n--- Physical Assessment ---")
        print(f"The 1-loop scalar self-energy at p = Delta* produces:")
        print(f"  eta_1loop = {mp.nstr(eta, 15)}")
        print(f"This is the SCALAR SECTOR contribution only.")
        print(f"The full anomalous dimension requires gluon-ghost-scalar")
        print(f"coupled system via BMW-FRG (beyond current calculation).")
        print(f"Evidence Category: [D] (numerical prediction, not proof)")

        print("\n" + "=" * 72)
        print("VERIFICATION COMPLETE")
        print("=" * 72)

        return {
            'Pi_S': Pi_S,
            'dPi_dp2': dpi,
            'Z_phi': Z_phi,
            'eta_1loop': eta,
            'delta_gamma_target': delta_gamma_target,
            'evidence': '[D]',
        }


if __name__ == "__main__":
    engine = ScalarSelfEnergy()
    results = engine.verify()
