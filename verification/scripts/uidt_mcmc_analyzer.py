"""
UIDT MCMC Data Analyzer v1.0
============================
Author: Philipp Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0

Performs statistical analysis on high-precision MCMC batches.
Calculates mean and standard deviation for Delta* [A] and gamma [A-].
"""

import pandas as pd
import glob
import os
import json

def perform_analysis():
    data_dir = 'verification/data/mcmc_batches/'
    csv_files = glob.glob(os.path.join(data_dir, 'batch_*.csv'))
    
    if not csv_files:
        print(f"No sample files found in {data_dir}")
        return

    all_data = []
    for f in csv_files:
        df = pd.read_csv(f)
        # Only take batches with multiple samples (assumed if rows > 1)
        if len(df) > 1:
            all_data.append(df)
    
    if not all_data:
        print("No valid multi-sample batches found.")
        return
        
    combined_df = pd.concat(all_data, ignore_index=True)
    
    stats = {
        'delta': {
            'mean': float(combined_df['delta'].mean()),
            'std': float(combined_df['delta'].std()),
            'min': float(combined_df['delta'].min()),
            'max': float(combined_df['delta'].max())
        },
        'gamma': {
            'mean': float(combined_df['gamma'].mean()),
            'std': float(combined_df['gamma'].std()),
            'min': float(combined_df['gamma'].min()),
            'max': float(combined_df['gamma'].max())
        },
        'kappa': {
            'mean': float(combined_df['kappa'].mean()),
            'std': float(combined_df['kappa'].std())
        },
        'sample_size': len(combined_df)
    }
    
    report_path = 'verification/data/mcmc_interim_report.json'
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(stats, f, indent=2)
        
    print(f"--- MCMC STATISTICAL ANALYSIS (N={stats['sample_size']}) ---")
    print(f"Delta*: {stats['delta']['mean']:.6f} +/- {stats['delta']['std']:.6f} [A]")
    print(f"Gamma:  {stats['gamma']['mean']:.6f} +/- {stats['gamma']['std']:.6f} [A-]")
    print(f"Kappa:  {stats['kappa']['mean']:.6f} +/- {stats['kappa']['std']:.6f} [A]")
    print(f"Results stored in: {report_path}")

if __name__ == "__main__":
    perform_analysis()
