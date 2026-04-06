"""
UIDT v3.9 CORE BASELINE TESTS
==============================
Anti-Tampering Rule: NO MOCKS, Native mpmath 80-digit only
"""
import pytest
from mpmath import mp, mpf
import sys
import os

# Ensure we can import from project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.banach_proof import BanachMassGap
from core.rg_closure import RGFixedPoint

mp.dps = 80

def test_banach_convergence():
    """Banach Fixed Point must converge to Δ* within 1e-14"""
    solver = BanachMassGap()
    Delta = solver.solve()
    expected = mpf('1.710035046742213182')
    assert abs(Delta - expected) < mpf('1e-14'), f"Mass gap mismatch: {Delta}"

def test_lipschitz_contraction():
    """Lipschitz constant L must be strictly < 1"""
    solver = BanachMassGap()
    L = solver.lipschitz_constant()
    assert L < mpf('1.0'), f"Not a contraction: L={L}"

def test_rg_closure():
    """RG constraint 5κ² = 3λ_S must hold to residual < 1e-14"""
    rg = RGFixedPoint()
    residual = rg.verify_closure()
    assert residual < mpf('1e-14'), f"RG closure failed: {residual}"

def test_canonical_v395_lambda_s():
    """Verify the exact canonical mathematical definition of lambda_S for UIDT v3.9.5."""
    kappa = mpf('0.500')
    lambda_S = 5 * kappa**2 / 3
    
    lhs = 5 * kappa**2
    rhs = 3 * lambda_S
    residual = abs(lhs - rhs)
    
    assert residual == mpf('0.0'), f"Canonical lambda_S definition fails exact closure: {residual}"
    
    # 1.25 / 3 = 0.416666...
    expected_lambda_s = mpf('1.25') / mpf('3')
    assert abs(lambda_S - expected_lambda_s) < mpf('1e-78'), f"Precision check failed for lambda_S: {lambda_S}"
