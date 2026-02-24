import sys
import os
import pytest
from mpmath import mp, mpf

# Add repository root to sys.path to resolve imports correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from modules.harmonic_predictions import HarmonicPredictor
except ImportError:
    # If run from verification/tests/, try a different import
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../modules')))
    from harmonic_predictions import HarmonicPredictor

# Set precision locally as per Anti-Tampering rules
mp.dps = 80

class TestHarmonicPredictor:
    def setup_method(self):
        """Setup method to initialize common test data."""
        # CRITICAL: Use strings to avoid float conversion artifacts
        self.vacuum_freq_gev = mpf('0.10710')
        self.delta_gap_gev = mpf('1.710')
        self.predictor = HarmonicPredictor(self.vacuum_freq_gev, self.delta_gap_gev)

    def test_initialization(self):
        """Test initialization of HarmonicPredictor."""
        # Residual check < 1e-14
        assert abs(self.predictor.f_vac - self.vacuum_freq_gev) < 1e-14
        assert abs(self.predictor.delta - self.delta_gap_gev) < 1e-14

    def test_predict_omega_bbb(self):
        """Test predict_omega_bbb calculation."""
        # Formula: f_vac * (3 * 54 - 27) = f_vac * 135
        expected = self.vacuum_freq_gev * 135
        actual = self.predictor.predict_omega_bbb()
        assert abs(actual - expected) < 1e-14

    def test_predict_tetraquark_cccc(self):
        """Test predict_tetraquark_cccc calculation."""
        # Formula: f_vac * (4 * 15 - 18) = f_vac * 42
        expected = self.vacuum_freq_gev * 42
        actual = self.predictor.predict_tetraquark_cccc()
        assert abs(actual - expected) < 1e-14

    def test_predict_x17_anomaly(self):
        """Test predict_x17_anomaly calculation."""
        # Formula: delta * 0.01
        expected = self.delta_gap_gev * mpf('0.01')
        actual = self.predictor.predict_x17_anomaly()
        assert abs(actual - expected) < 1e-14

    def test_predict_x2370_resonance(self):
        """Test predict_x2370_resonance calculation."""
        # Formula: f_vac * 22.13
        expected = self.vacuum_freq_gev * mpf('22.13')
        actual = self.predictor.predict_x2370_resonance()
        assert abs(actual - expected) < 1e-14

    def test_predict_glueball_tensor(self):
        """Test predict_glueball_tensor calculation."""
        # Formula: delta * sqrt(2)
        expected = self.delta_gap_gev * mp.sqrt(mpf('2'))
        actual = self.predictor.predict_glueball_tensor()
        assert abs(actual - expected) < 1e-14

    def test_predict_glueball_pseudoscalar(self):
        """Test predict_glueball_pseudoscalar calculation."""
        # Formula: delta * 1.5
        expected = self.delta_gap_gev * mpf('1.5')
        actual = self.predictor.predict_glueball_pseudoscalar()
        assert abs(actual - expected) < 1e-14

    def test_generate_report(self):
        """Test generate_report returns dictionary with correct keys and types."""
        report = self.predictor.generate_report()
        assert isinstance(report, dict)

        expected_keys = [
            "Omega_bbb_GeV", "Tetra_cccc_GeV", "X17_NoiseFloor_MeV",
            "X2370_Resonance_GeV", "Glueball_2++_GeV", "Glueball_0-+_GeV",
            "MassGap_0++_GeV", "Base_Freq_MeV", "Source"
        ]
        for key in expected_keys:
            assert key in report

        # Verify specific values (converted to float in report, so check within tolerance)
        # Note: report converts mpf to float, potentially losing precision, but should be close.
        # However, checking consistency is key.
        assert abs(report["Omega_bbb_GeV"] - float(self.predictor.predict_omega_bbb())) < 1e-14
        assert abs(report["X2370_Resonance_GeV"] - float(self.predictor.predict_x2370_resonance())) < 1e-14

    def test_check_proton_anchor(self):
        """Test check_proton_anchor calculation."""
        proton_mass_mev = mpf('938.27')
        result = self.predictor.check_proton_anchor(proton_mass_mev)

        f_vac_mev = self.vacuum_freq_gev * 1000
        ratio = proton_mass_mev / f_vac_mev
        target = mpf(35) / mpf(4)
        deviation = ratio - target

        assert abs(result["f_vac_MeV"] - float(f_vac_mev)) < 1e-14
        assert abs(result["ratio"] - float(ratio)) < 1e-14
        assert abs(result["deviation"] - float(deviation)) < 1e-14
