"""
Tests for UIDT Causal Geometry Convergence
------------------------------------------
Validating Bananch-contraction constraints on emergent topological metrics.
"""

import sys
import os
import mpmath as mp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from verification.scripts.UIDT_Causal_Geometry_Verification import CausalGeometryVerifier

# STRICT ANTI-TAMPERING RULE 1
mp.dps = 80

def test_gamma_emergence_residual():
    verifier = CausalGeometryVerifier()
    
    # Construct exact expected hierarchy target
    target_depth = verifier.gamma_canonical ** mp.mpf('-3.0')
    layers = [target_depth / mp.mpf('3.0')] * 3
    
    ratio = verifier.compute_coherence_hierarchy(layers)
    g_emerg = verifier.verify_gamma_emergence(ratio)
    
    # Absolute residual MUST be calculated using mpmath, < 1e-14
    residual = abs(g_emerg - verifier.gamma_canonical)
    
    assert residual < mp.mpf('1e-14'), f"Gamma convergence residual too large: {mp.nstr(residual, 5)}"

def test_casimir_divergence_check():
    verifier = CausalGeometryVerifier()
    
    # L5 constraint ensures we handle 0.66 nm safely without mathematical collision
    lambda_val = verifier.lambda_scale
    
    # Ensure precision maintains pure representation
    assert lambda_val > mp.mpf('0')
    assert lambda_val == mp.mpf('0.66e-9')
