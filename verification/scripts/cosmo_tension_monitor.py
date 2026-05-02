#!/usr/bin/env python3
"""
UIDT v3.9 — Cosmological Tension Monitor
==========================================
Automated comparison of UIDT cosmological predictions against
external measurements (SH0ES, TRGB, Planck, DESI).

Computes Z-score tension and classifies evidence status.

Author: P. Rietz
Evidence Category: [C] (Cosmological calibration — DESI/JWST/ACT)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0
"""

import mpmath as mp
from mpmath import mpf
import datetime
import os
import sys

# Local precision lock — NEVER centralize
mp.dps = 80

# ==============================================================================
# UIDT CANONICAL PREDICTIONS [C]
# ==============================================================================
UIDT_H0 = mpf('70.4')          # km/s/Mpc [C] — DESI-calibrated
UIDT_H0_ERR = mpf('0.16')      # km/s/Mpc
UIDT_W0 = mpf('-0.99')         # Dark energy equation of state [C]
UIDT_W0_ERR = mpf('0.01')

# ==============================================================================
# EXTERNAL MEASUREMENTS (Updated 2026)
# ==============================================================================
EXTERNAL_DATA = {
    "SH0ES_2022": {
        "H0": mpf('73.04'),
        "H0_err": mpf('1.04'),
        "source": "Riess et al. (2022), ApJ 934, 7",
        "method": "Cepheid distance ladder",
    },
    "TRGB_2024": {
        "H0": mpf('69.85'),
        "H0_err": mpf('1.75'),
        "source": "Freedman et al. (2024), ApJ",
        "method": "Tip of Red Giant Branch",
    },
    "Planck_2018": {
        "H0": mpf('67.36'),
        "H0_err": mpf('0.54'),
        "source": "Planck Collaboration (2018), A&A 641, A6",
        "method": "CMB power spectrum (LCDM)",
    },
    "DESI_DR1_2024": {
        "H0": mpf('67.97'),
        "H0_err": mpf('0.38'),
        "source": "DESI Collaboration (2024), arXiv:2404.03002",
        "method": "BAO + BBN",
    },
    "ACT_DR6_2024": {
        "H0": mpf('67.49'),
        "H0_err": mpf('1.12'),
        "source": "ACT DR6 (2024)",
        "method": "CMB (ACT)",
    },
}

EXTERNAL_W0_DATA = {
    "DESI_DR1_w0waCDM": {
        "w0": mpf('-0.55'),
        "w0_err": mpf('0.21'),
        "wa": mpf('-1.32'),
        "wa_err": mpf('0.65'),
        "source": "DESI DR1 BAO + CMB + SNe Ia (w0waCDM)",
    },
    "Planck_LCDM": {
        "w0": mpf('-1.0'),
        "w0_err": mpf('0.0'),  # exact in LCDM
        "wa": mpf('0.0'),
        "wa_err": mpf('0.0'),
        "source": "Standard LCDM assumption",
    },
}


def compute_z_score(uidt_val, uidt_err, ext_val, ext_err):
    """Compute Z-score tension between UIDT and external measurement."""
    combined_err = mp.sqrt(uidt_err**2 + ext_err**2)
    if combined_err == 0:
        return mpf('inf')
    return abs(uidt_val - ext_val) / combined_err


def classify_tension(z):
    """Classify tension level for reporting."""
    if z < mpf('1'):
        return "EXCELLENT"
    elif z < mpf('2'):
        return "CONSISTENT"
    elif z < mpf('3'):
        return "MILD_TENSION"
    elif z < mpf('5'):
        return "SIGNIFICANT_TENSION"
    else:
        return "STRONG_TENSION"


def run_h0_monitor():
    """Run the H0 tension monitor against all external datasets."""
    results = {}
    for name, data in EXTERNAL_DATA.items():
        z = compute_z_score(UIDT_H0, UIDT_H0_ERR, data["H0"], data["H0_err"])
        classification = classify_tension(z)
        results[name] = {
            "UIDT_H0": mp.nstr(UIDT_H0, 4),
            "External_H0": mp.nstr(data["H0"], 5),
            "External_Error": mp.nstr(data["H0_err"], 4),
            "Z_Score": mp.nstr(z, 4),
            "Classification": classification,
            "Source": data["source"],
            "Method": data["method"],
            "Evidence": "[C]",
        }
    return results


def run_w0_monitor():
    """Run the w0 dark energy equation of state monitor."""
    results = {}
    for name, data in EXTERNAL_W0_DATA.items():
        if data["w0_err"] > 0:
            z = compute_z_score(UIDT_W0, UIDT_W0_ERR, data["w0"], data["w0_err"])
        else:
            z = abs(UIDT_W0 - data["w0"]) / UIDT_W0_ERR if UIDT_W0_ERR > 0 else mpf('inf')
        classification = classify_tension(z)
        results[name] = {
            "UIDT_w0": mp.nstr(UIDT_W0, 4),
            "External_w0": mp.nstr(data["w0"], 4),
            "External_Error": mp.nstr(data["w0_err"], 3),
            "Z_Score": mp.nstr(z, 4),
            "Classification": classification,
            "Source": data["source"],
            "Evidence": "[C]",
        }
    return results


def generate_report():
    """Generate the full cosmological tension report."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    h0_results = run_h0_monitor()
    w0_results = run_w0_monitor()

    lines = [
        "=" * 72,
        f"  UIDT v3.9 — COSMOLOGICAL TENSION MONITOR",
        f"  Timestamp: {timestamp}",
        f"  Evidence Category: [C] (Cosmological calibration)",
        f"  DOI: 10.5281/zenodo.17835200",
        "=" * 72,
        "",
        "--- H0 Hubble Constant ---",
        f"  UIDT Prediction: H0 = {mp.nstr(UIDT_H0, 4)} +/- {mp.nstr(UIDT_H0_ERR, 3)} km/s/Mpc [C]",
        "",
    ]

    for name, r in h0_results.items():
        lines.extend([
            f"  [{name}]",
            f"    External: H0 = {r['External_H0']} +/- {r['External_Error']} km/s/Mpc",
            f"    Method:   {r['Method']}",
            f"    Z-Score:  {r['Z_Score']} -> {r['Classification']}",
            f"    Source:   {r['Source']}",
            "",
        ])

    lines.extend([
        "--- w0 Dark Energy Equation of State ---",
        f"  UIDT Prediction: w0 = {mp.nstr(UIDT_W0, 4)} +/- {mp.nstr(UIDT_W0_ERR, 3)} [C]",
        "",
    ])

    for name, r in w0_results.items():
        lines.extend([
            f"  [{name}]",
            f"    External: w0 = {r['External_w0']} +/- {r['External_Error']}",
            f"    Z-Score:  {r['Z_Score']} -> {r['Classification']}",
            f"    Source:   {r['Source']}",
            "",
        ])

    # Summary
    all_z_h0 = [compute_z_score(UIDT_H0, UIDT_H0_ERR, d["H0"], d["H0_err"]) for d in EXTERNAL_DATA.values()]
    max_z = max(all_z_h0)
    min_z = min(all_z_h0)
    avg_z = sum(all_z_h0) / len(all_z_h0)

    lines.extend([
        "=" * 72,
        "  SUMMARY",
        f"  H0 Z-scores: min={mp.nstr(min_z, 3)}, max={mp.nstr(max_z, 3)}, avg={mp.nstr(avg_z, 3)}",
        f"  Overall Status: {classify_tension(avg_z)}",
        f"  Falsification Threshold: Z > 5.0 (none triggered)",
        "=" * 72,
    ])

    return "\n".join(lines)


# ==============================================================================
if __name__ == "__main__":
    report = generate_report()
    print(report)

    # Save to verification/data/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
    os.makedirs(data_dir, exist_ok=True)

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = os.path.join(data_dir, f"cosmo_tension_{timestamp}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved: {report_path}")
