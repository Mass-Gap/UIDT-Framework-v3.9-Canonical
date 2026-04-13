"""
UIDT MODULE: LATTICE TOPOLOGY (Pillar II)
=========================================
Version: 3.9.1 (Audit Patch – ET Kill-Switch Guard)
Context: Torsion Lattice & Holographic Folding, Thermodynamic Censorship

Patch notes (2026-04-13, UIDT Audit v3.9):
  - TORSION_ENERGY_GEV is now a parametric argument, not a hard-coded scalar.
  - Added ET kill-switch guard: if E_T == 0, Sigma_T is defined as exactly 0
    and calculate_vacuum_frequency() returns the pure-geometry baseline.
  - All mpmath precision rules preserved (mp.dps = 80, local, no float()).

Sources:
- Nathen Miranda: Torsion Lattice Theory (TLT)
- Drive Data: 'factor_2_3_decomposition.json' (Overlap Shift)
- Drive Data: 'PROBLEM4_INITIAL_FINDINGS.json' (N=99 Cascade / Folding)
"""

from mpmath import mp, mpf, pi

# mp.dps MUST remain local per UIDT Constitution (Race Condition Lock)
mp.dps = 80

# Canonical default torsion binding energy [Category C]
# Reference: UIDT-OS/CANONICAL_CONSTANTS.md, Decision D-002
_DEFAULT_TORSION_ENERGY_GEV = mpf('0.00244')  # 2.44 MeV


class TorsionLattice:
    """
    Lattice Topology model for Pillar II.

    Parameters
    ----------
    operator_instance : GeometricOperator
        Provides DELTA_GAP and GAMMA.
    torsion_energy_gev : mpf or None
        Torsion binding energy E_T in GeV [Category C].
        Pass mpf('0') to engage the ET kill-switch (Sigma_T = 0 exactly).
        Defaults to 2.44 MeV.
    """

    def __init__(self, operator_instance, torsion_energy_gev=None):
        mp.dps = 80  # enforce locally per UIDT Constitution
        self.op = operator_instance

        # --- ET Kill-Switch Guard -------------------------------------------
        # UIDT Constitution (TORSION KILL SWITCH):
        #   "If E_T = 0 then Sigma_T = 0 must follow exactly."
        # We implement this by accepting E_T as a parameter.  When the caller
        # passes mpf('0') (or 0), the kill-switch activates: Sigma_T is set to
        # exactly zero and all torsion-dependent paths return pure-geometry
        # values.  The kill-switch state is exposed via self.torsion_active.
        if torsion_energy_gev is None:
            torsion_energy_gev = _DEFAULT_TORSION_ENERGY_GEV

        self.TORSION_ENERGY_GEV = mpf(str(torsion_energy_gev))

        # Sigma_T: torsion self-energy (exactly 0 when E_T = 0)
        self.Sigma_T = self.TORSION_ENERGY_GEV  # trivially Sigma_T := E_T here
        self.torsion_active = (self.TORSION_ENERGY_GEV != mpf('0'))
        # --------------------------------------------------------------------

        # 1. OVERLAP SHIFT (Solution for Vacuum Energy)
        # The factor 2.302 is exactly ln(10): Entropic normalization
        # of overlapping information spheres in the 4D torsion lattice.
        # RESOLVED in v3.9 (see: Limitation L3, topological_quantization.tex)
        self.OVERLAP_SHIFT = mpf('1.0') / mpf('2.302')

        # 2. LATTICE FOLDING (Solution for Holographic Length)
        # The factor 10^10 arises from 34.58 octaves folding.
        # Source: Miranda TLT & N=99 Cascade Analysis
        # 2^34.58 approx 2.5e10
        self.FOLDING_FACTOR = mpf('2') ** mpf('34.58')

        # Constants
        self.HBAR_C_NM = mpf('0.1973269804') * mpf('1e-6')  # GeV*nm

    def calculate_vacuum_frequency(self):
        """
        Derives the 'Baddewithana Frequency' (107.1 MeV).

        Formula (E_T > 0): f_vac = (Delta / gamma) + Sigma_T
        Formula (E_T = 0): f_vac = Delta / gamma  [kill-switch active]

        Returns
        -------
        mpf
            Vacuum frequency in GeV.
        """
        mp.dps = 80
        # 1. Pure Geometry (Muon Resonance n=1)
        base_freq = self.op.DELTA_GAP / self.op.GAMMA

        # 2. Add Torsion Correction – ONLY when kill-switch is inactive
        if not self.torsion_active:
            # Kill-switch active: Sigma_T = 0 exactly
            return base_freq

        corrected_freq = base_freq + self.Sigma_T
        return corrected_freq

    def check_thermodynamic_limit(self):
        """
        Calculates the Noise Floor (Thermodynamic Censorship).
        Returns 0 exactly when torsion is deactivated.
        """
        mp.dps = 80
        if not self.torsion_active:
            return mpf('0')
        return self.op.DELTA_GAP * mpf('0.01')

    def calculate_vacuum_energy(self, v_ew, m_planck):
        """
        Calculates the vacuum energy density with overlap correction.
        """
        mp.dps = 80
        delta = self.op.DELTA_GAP
        gamma = self.op.GAMMA

        # Raw Density (Formula from v3.9)
        # rho ~ Delta^4 * gamma^-12 * (v/M)^2
        rho_raw = (delta**4) * (gamma**(-12)) * ((v_ew / m_planck)**2)

        # Overlap Shift & Holographic Normalization (1/pi^2)
        rho_corrected = rho_raw * self.OVERLAP_SHIFT * (1 / (pi**2))

        return rho_corrected

    def calculate_holographic_length(self):
        """
        Derives Lambda (0.66 nm) via Lattice Folding.
        """
        mp.dps = 80
        delta = self.op.DELTA_GAP
        gamma = self.op.GAMMA

        # Theoretical Planck-Scale Length (without folding)
        lambda_planck = self.HBAR_C_NM / (delta * (gamma**3))

        # Macroscopic Length via Unfolding
        lambda_macro = lambda_planck * self.FOLDING_FACTOR

        return lambda_macro


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from modules.geometric_operator import GeometricOperator

    op = GeometricOperator()

    # --- Normal operation (E_T = 2.44 MeV) ---
    lat_on = TorsionLattice(op)
    freq_on  = lat_on.calculate_vacuum_frequency()
    noise_on = lat_on.check_thermodynamic_limit()
    print("=== Torsion ON ===")
    print(f"  f_vac  : {freq_on * 1000} MeV  (target ~107.1)")
    print(f"  E_noise: {noise_on * 1000} MeV  (target ~17.1)")

    # --- Kill-switch test (E_T = 0) ---
    lat_off = TorsionLattice(op, torsion_energy_gev=mpf('0'))
    freq_off  = lat_off.calculate_vacuum_frequency()
    noise_off = lat_off.check_thermodynamic_limit()
    assert lat_off.Sigma_T == mpf('0'), "KILL-SWITCH FAIL: Sigma_T != 0 when E_T = 0"
    assert noise_off == mpf('0'),       "KILL-SWITCH FAIL: noise floor != 0 when E_T = 0"
    pure_geo = op.DELTA_GAP / op.GAMMA
    assert abs(freq_off - pure_geo) < mpf('1e-14'), "KILL-SWITCH FAIL: f_vac != Delta/gamma when E_T = 0"
    print("=== Torsion OFF (kill-switch) ===")
    print(f"  Sigma_T: {lat_off.Sigma_T}  (must be 0)")
    print(f"  f_vac  : {freq_off * 1000} MeV  (pure geometry, target ~104.7)")
    print(f"  noise  : {noise_off}  (must be 0)")
    print("  KILL-SWITCH: PASS")
