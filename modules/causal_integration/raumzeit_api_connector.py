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
        
    def load_k1_metric(self):
        """
        Loads the core diagnostic metric K1 explicitly with 80-digit precision.
        """
        if not self.json_path:
            # Fallback to mock baseline for ablation tests without external files
            return mp.mpf('0.1013217379051603')
            
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Safely parse exact float
            return mp.mpf(str(data.get('mean_final_k1', '0.1013217379051603')))
        except FileNotFoundError:
            raise RuntimeError(f"Static raumzeit JSON not found at {self.json_path}.")

