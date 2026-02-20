#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 MODULE: STATISTICAL EVIDENCE ANALYZER
=================================================
Status: Canonical / Clean State
Description: Evaluates the empirical robustness of the UIDT framework 
             based on accumulated Z-Scores from Pillars I, II, and III.
"""

import numpy as np

def calculate_evidence_strength(z_scores):
    """
    Evaluates empirical evidence strength based on Z-Scores (Standard Deviations).
    
    Args:
        z_scores (list/array): List of absolute Z-scores from simulations.
        
    Returns:
        tuple: (Evidence Level String, Interpretation String)
    """
    # 1. Categorize Z-Scores
    # Strong: < 2 sigma (Indistinguishable from nature/experiment)
    strong_evidence = sum(1 for z in z_scores if z < 2.0)
    
    # Moderate: 2 sigma <= z < 3 sigma (Tension or statistical fluctuation)
    moderate_evidence = sum(1 for z in z_scores if 2.0 <= z < 3.0)
    
    # Weak/Falsified: >= 3 sigma (Significant deviation from reality)
    weak_evidence = sum(1 for z in z_scores if z >= 3.0)
    
    total_simulations = len(z_scores)
    
    # 2. Print Detailed Statistical Report
    print("\n📊 EMPIRICAL EVIDENCE ANALYSIS (UIDT v3.6.1)")
    print("=" * 60)
    print(f"   Total Metrics Evaluated: {total_simulations}")
    print("-" * 60)
    
    # Calculate percentages
    pct_strong = (strong_evidence / total_simulations) * 100
    pct_mod = (moderate_evidence / total_simulations) * 100
    pct_weak = (weak_evidence / total_simulations) * 100
    
    print(f"   ✅ Strong Evidence (Z < 2.0σ):      {strong_evidence}/{total_simulations} ({pct_strong:.1f}%)")
    print(f"   ⚠️ Moderate Evidence (2.0σ ≤ Z < 3.0σ): {moderate_evidence}/{total_simulations} ({pct_mod:.1f}%)")
    print(f"   ❌ Weak/Falsified (Z ≥ 3.0σ):       {weak_evidence}/{total_simulations} ({pct_weak:.1f}%)")
    print("-" * 60)
    
    # 3. Scientific Conclusion 
    ratio_strong = strong_evidence / total_simulations
    
    if ratio_strong >= 0.8:
        level = "HIGH EVIDENCE"
        interpretation = "Theory exhibits consistent agreement with physical reality."
    elif ratio_strong >= 0.6:
        level = "MODERATE EVIDENCE"
        interpretation = "Promising indications; further high-precision tests required."
    else:
        level = "LOW EVIDENCE"
        interpretation = "No robust empirical support found; model likely falsified."
        
    print(f"   🔍 CONCLUSION:  {level}")
    print(f"   📝 INTERPRETATION: {interpretation}")
    print("=" * 60 + "\n")
    
    return level, interpretation

# =============================================================================
# MAIN EXECUTION (Clean State Data)
# =============================================================================
if __name__ == "__main__":
    # Real Data from UIDT v3.6.1 "Clean State" Simulations:
    # 1. Mass Gap (HMC): 0.25 sigma (Pillar I)
    # 2. Hubble Tension (Cosmology): 0.01 sigma (Pillar II - Exact Resolution)
    # 3. Casimir Prediction: 1.10 sigma (Pillar III - Predictive Anomaly)
    # 4. Kappa Scan Optimum: 0.17 sigma (Parameter Tuning)
    # 5. Continuum Limit Extrapolation: 0.51 sigma (Systematic Error)
    
    z_scores_clean_state = [0.25, 0.01, 1.10, 0.17, 0.51]
    
    print("running evidence check on v3.6.1 clean state data...")
    evidence_level, interpretation = calculate_evidence_strength(z_scores_clean_state)