"""
ralph_loop_mc_validator.py
UIDT Framework (v3.9) - External MC Data Validation (Stratum I to III)
Evidence Category: [B]

This script strictly performs deterministic data ingestion from external Lattice QCD Monte Carlo
sources and compares them against the canonical UIDT ledger.
S0-Directive: NO DATA GENERATION. NO MOCK DATA. STRICT mp.dps=80 precision.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
import mpmath as mp

# 1. LOCAL PRECISION INITIALIZATION (S0-Directive: No centralization)
mp.dps = 80

class ClaimsLedger:
    """Stratum III: Reads canonical constants dynamically from LEDGER/CLAIMS.json."""
    def __init__(self, ledger_path: Path):
        self.ledger_path = ledger_path

    def load_canonical_gamma(self) -> mp.mpf:
        """Parses LEDGER/CLAIMS.json for UIDT-C-002 to extract gamma without float conversion."""
        with open(self.ledger_path, 'r', encoding='utf-8') as f:
            ledger = json.load(f)

        for claim in ledger.get("claims", []):
            if claim.get("id") == "UIDT-C-002":
                statement = claim.get("statement", "")
                # Expected string: "Gamma Invariant γ = 16.339 (kinetic VEV)"
                match = re.search(r'γ\s*=\s*([\d\.]+)', statement)
                if match:
                    return mp.mpf(match.group(1))
        raise ValueError("Canonical gamma (UIDT-C-002) not found in ledger.")


class MCObserver:
    """Stratum I: Data Ingestion Layer."""
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def ingest_gamma_samples(self) -> list[mp.mpf]:
        """Reads CSV row by row, converting string directly to mp.mpf. ZERO FLOAT LEAKS."""
        samples = []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Assuming CSV column is named 'gamma'
                val_str = row.get('gamma')
                if val_str is None:
                    continue
                samples.append(mp.mpf(val_str))
        return samples


class StatisticalEvaluator:
    """80-dps Evaluation Layer."""
    @staticmethod
    def calculate_mean(samples: list[mp.mpf]) -> mp.mpf:
        n = mp.mpf(str(len(samples)))
        if n == 0:
            return mp.mpf('0')
        return sum(samples) / n

    @staticmethod
    def calculate_variance(samples: list[mp.mpf], mean_val: mp.mpf) -> mp.mpf:
        n = mp.mpf(str(len(samples)))
        if n <= mp.mpf('1'):
            return mp.mpf('0')
        variance = sum((x - mean_val)**2 for x in samples) / (n - mp.mpf('1'))
        return variance

    @staticmethod
    def calculate_z_score(mc_mean: mp.mpf, canonical_val: mp.mpf, variance: mp.mpf, n_samples: int) -> mp.mpf:
        if n_samples == 0 or variance == mp.mpf('0'):
            return mp.mpf('0')
        std_err = mp.sqrt(variance) / mp.sqrt(mp.mpf(str(n_samples)))
        return mp.fabs(mc_mean - canonical_val) / std_err


class TraceabilityLogger:
    """Handles verification logging (Audit Trail)."""
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_results(self, n_samples: int, mc_mean: mp.mpf, variance: mp.mpf, z_score: mp.mpf, canonical: mp.mpf):
        # Using mp.nstr() to safely serialize 80-dps objects to JSON strings
        log_data = {
            "stratum_I_samples": n_samples,
            "mc_mean_80dps": mp.nstr(mc_mean, 80),
            "mc_variance_80dps": mp.nstr(variance, 80),
            "canonical_target_80dps": mp.nstr(canonical, 80),
            "z_score": mp.nstr(z_score, 80),
            "significance": "CONSISTENT" if z_score < mp.mpf('1.0') else "TENSION"
        }
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="External MC Data Validator (Stratum I -> III)")
    parser.add_argument("--data", type=str, required=True, help="Path to external MC samples CSV")
    parser.add_argument("--ledger", type=str, default="LEDGER/CLAIMS.json", help="Path to UIDT canonical ledger")
    parser.add_argument("--log", type=str, default="verification/logs/mc_validation_run.json", help="Path to output log")
    args = parser.parse_args()

    # 1. Stratum III: Load Canonical Constants
    ledger = ClaimsLedger(Path(args.ledger))
    canonical_gamma = ledger.load_canonical_gamma()

    # 2. Stratum I: Ingest MC Data (No Float Leaks)
    observer = MCObserver(Path(args.data))
    mc_samples = observer.ingest_gamma_samples()
    n_samples = len(mc_samples)

    if n_samples == 0:
        print("No valid gamma samples found. Terminating.")
        sys.exit(1)

    # 3. 80-dps Evaluation Layer
    mean_mc = StatisticalEvaluator.calculate_mean(mc_samples)
    var_mc = StatisticalEvaluator.calculate_variance(mc_samples, mean_mc)
    z_score = StatisticalEvaluator.calculate_z_score(mean_mc, canonical_gamma, var_mc, n_samples)

    # 4. Stratum Comparison & Logging
    logger = TraceabilityLogger(Path(args.log))
    logger.log_results(n_samples, mean_mc, var_mc, z_score, canonical_gamma)

    print(f"Validation complete. Z-Score: {mp.nstr(z_score, 10)}. Details logged to {args.log}")

if __name__ == "__main__":
    main()
