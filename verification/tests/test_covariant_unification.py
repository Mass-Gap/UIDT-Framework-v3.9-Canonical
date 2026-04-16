"""
Verification Test for Covariant Unification
===========================================
Ensures that the EoS placeholder and covariant unification methods
are callable and function to the specified high precision parameters.
"""

from mpmath import mp, mpf
from modules.covariant_unification import CovariantUnification

# UIDT Constitution Directive: Local precision initialization
mp.dps = 80

def test_covariant_unification_equation_of_state():
    """
    Verifies that the derive_equation_of_state method returns the valid
    DESI-calibrated [C] placeholder data. This is essential for the Master
    Verification Suite integrity.
    """
    cu = CovariantUnification()
    
    # Run the derivation method
    eos = cu.derive_equation_of_state()
    
    assert "w_0" in eos, "w_0 must be defined in EoS parameters"
    assert "w_a" in eos, "w_a must be defined in EoS parameters"
    assert "evidence" in eos, "Evidence category must be explicit"
    
    assert eos["w_0"] == mpf('-0.99'), "w_0 must match DESI placeholder -0.99 [C]"
    assert eos["w_a"] == mpf('+0.03'), "w_a must match DESI placeholder +0.03 [C]"
    assert eos["evidence"] == "C", "Evidence category must remain [C]"

def test_covariant_unification_ir_limit():
    """
    Verifies the topological protection at the Infrared Fixed Point.
    """
    cu = CovariantUnification()
    epsilon = mpf('1e-5')
    
    limit = cu.evaluate_ir_limit(epsilon)
    
    assert limit >= mpf('0'), "Residual limit should be semi-positive"
    # Basic check to see it returns a valid mpf
    assert type(limit) == type(mpf('1.0'))
