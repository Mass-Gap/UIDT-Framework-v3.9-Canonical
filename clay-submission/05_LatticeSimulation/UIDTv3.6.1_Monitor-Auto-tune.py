#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT v3.6.1 MONITOR & AUTO-TUNE MODULE
======================================
Status: Canonical / Clean State
Description: Adaptive step-size control and performance benchmarking logic
             for the UIDT HMC simulation engine.
Context: Optimized for v3.6.1 parameters (VEV=47.7 MeV, Gamma=16.339).
"""

import numpy as np
import time

# Note: This module is designed to be mixed into the main Lattice class.
# It assumes 'self' has access to 'acceptance_rate', 'step_size',
# 'hmc_trajectory', and 'omelyan_integrator_2nd_order'.

def adaptive_hmc_step_size(self, target_acceptance=0.8, adjustment_rate=0.05):
    """
    Automatische Anpassung der Schrittweite basierend auf Akzeptanzrate.
    Optimiert für UIDT v3.6.1 HMC-Stabilität.
    """
    current_rate = self.acceptance_rate
    
    if current_rate < target_acceptance - 0.1:
        # Zu niedrige Akzeptanz: kleinere Schritte
        self.step_size *= (1.0 - adjustment_rate)
        print(f"🔻 Step size decreased to {self.step_size:.4f} (acceptance: {current_rate:.3f})")
    elif current_rate > target_acceptance + 0.1:
        # Zu hohe Akzeptanz: größere Schritte (effizienter)
        self.step_size *= (1.0 + adjustment_rate)
        print(f"🔺 Step size increased to {self.step_size:.4f} (acceptance: {current_rate:.3f})")
    
    return self.step_size

def performance_benchmark(self, n_trajectories=100):
    """
    Benchmark der Performance-Optimierungen.
    Vergleicht Standard-Leapfrog mit v3.6.1 Omelyan+Cayley-Hamilton Integrator.
    """
    print("🚀 Performance Benchmark für UIDT HMC (v3.6.1 Engine)")
    print("=" * 50)
    
    # Test mit verschiedenen Methoden
    # self.hmc_trajectory refers to standard leapfrog
    # self.omelyan_integrator_2nd_order refers to the optimized v3.6.1 integrator
    methods = {
        'Original Leapfrog': self.hmc_trajectory,
        'Omelyan + Cayley-Hamilton': self.omelyan_integrator_2nd_order
    }
    
    for name, method in methods.items():
        print(f"\n📊 Testing: {name}")
        
        times = []
        acceptances = []
        
        for i in range(n_trajectories):
            start_time = time.time()
            # Führe Trajektorie aus
            accepted, delta_H = method()
            end_time = time.time()
            
            times.append(end_time - start_time)
            acceptances.append(accepted)
        
        avg_time = np.mean(times)
        acceptance_rate = np.mean(acceptances)
        
        print(f"   ⏱️  Average time: {avg_time:.4f}s")
        print(f"   ✅ Acceptance rate: {acceptance_rate:.3f}")
        # Avoid division by zero if time is extremely small (mock run)
        perf = 1.0 / avg_time if avg_time > 0 else float('inf')
        print(f"   🎯 Performance: {perf:.2f} trajectories/s")
    
    return times, acceptances