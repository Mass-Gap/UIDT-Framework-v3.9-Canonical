"""
Raumzeit API Connector
----------------------
Static JSON connector mapping cblab/raumzeit layer profile outputs to UIDT.
Ensures 80-digit mpmath precision is applied immediately upon data ingestion.

DOI: 10.5281/zenodo.17835200
"""

import json
import mpmath as mp

# STRICT ANTI-TAMPERING RULE 1
mp.dps = 80

class RaumzeitConnector:
    def __init__(self, json_path=None):
        self.json_path = json_path
        
    def load_layer_profiles(self):
        """
        Loads layer thicknesses strictly as mp.mpf objects to preserve limits.
        """
        if not self.json_path:
            # Fallback to mock baseline for ablation tests without external files
            return self._generate_mock_baseline()
            
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Safely parse exact floats
            layers = [mp.mpf(str(layer['thickness'])) for layer in data.get('layers', [])]
            return layers
        except FileNotFoundError:
            raise RuntimeError(f"Static raumzeit JSON not found at {self.json_path}.")
            
    def _generate_mock_baseline(self):
        """
        Provides a structurally consistent baseline representing a v9a_fast graph.
        """
        # Distributes causal density simulating gamma convergence
        pseudo_gamma = mp.mpf('16.339')
        target_vol = pseudo_gamma ** mp.mpf('-12.0')
        baseline_depth = target_vol ** mp.mpf('0.25')  # depth = vol^(1/4)
        
        # 4 identical layers forming the baseline metric
        return [baseline_depth / mp.mpf('4.0')] * 4
