# Verification Reproduction Protocol

**One-Command Reproducibility for UIDT Framework v3.9**

## Quick Start (Docker)

```bash
# Clone repository
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical

# Run full verification suite
docker run --rm -v $(pwd):/workspace -w /workspace python:3.11-slim bash -c "
  pip install -q mpmath==1.3.0 pytest==7.4.0 numpy==1.24.0 scipy==1.11.0 &&
  python verification/scripts/verify_all.py
"
```

**Expected Runtime:** ~2 hours (8 CPU cores, 16GB RAM)  
**Expected Output:** All Category A claims pass with residuals < 10^-14

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows (WSL2)
- **Python:** 3.11 or higher
- **RAM:** 16GB recommended (8GB minimum)
- **CPU:** 8 cores recommended (4 cores minimum)
- **Disk:** 5GB free space

### Software Dependencies
```bash
pip install mpmath==1.3.0 pytest==7.4.0 numpy==1.24.0 scipy==1.11.0
```

## Step-by-Step Reproduction

### 1. Clone Repository
```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical
```

### 2. Install Dependencies
```bash
pip install -r verification/requirements.txt
```

### 3. Run Verification Suite

#### Full Verification (All Tests)
```bash
python verification/scripts/verify_all.py
```

#### Individual Components
```bash
# Spectral Gap: Δ = 1.710 GeV [A]
python verification/scripts/verify_spectral_gap.py

# RG Fixed Point: 5κ² = 3λ_S [A]
python verification/scripts/verify_rg_fixed_point.py

# Cosmology: H₀, Ω_m, w₀ [C]
python verification/scripts/verify_cosmology.py

# Quark Masses: Generation scaling [D]
python verification/scripts/verify_quark_masses.py
```

#### Pytest Suite
```bash
pytest verification/tests/ -v --tb=short
```

### 4. Generate Audit Reports
```bash
python verification/audits/framework_integrity_audit.py
python verification/audits/parameter_drift_detector.py
```

## Expected Results

### Category A Claims (Residual < 10^-14)
- **Spectral Gap:** Δ = 1.710 ± 0.015 GeV
- **RG Fixed Point:** 5κ² = 3λ_S (residual < 10^-14)
- **Coupling Constants:** κ = 0.500 ± 0.008, λ_S = 5κ²/3 ≈ 0.41̄6̄ ± 0.007

### Category A- Claims (Phenomenological)
- **Scaling Parameter:** γ = 16.339 (calibrated, not RG-derived)

### Category C Claims (Calibrated)
- **Hubble Constant:** H₀ = 70.4 ± 0.16 km/s/Mpc (DESI-aligned)
- **Matter Density:** Ω_m = 0.307 ± 0.004
- **Dark Energy EoS:** w₀ = -0.99 ± 0.02

### Category D Claims (Predicted)
- **Scalar Glueball:** m_S = 1.705 ± 0.015 GeV (unconfirmed)
- **Quark Mass Hierarchy:** Generation scaling law

## SHA256 Checksums

Verify integrity of key verification scripts:

```bash
sha256sum verification/scripts/verify_spectral_gap.py
# Expected: [to be computed after finalization]

sha256sum verification/scripts/verify_rg_fixed_point.py
# Expected: [to be computed after finalization]
```

## REANA Workflow (CERN CAP)

For CERN Analysis Preservation:

```bash
# Install REANA client
pip install reana-client

# Run workflow
reana-client run -f verification/reana.yaml
```

See `verification/reana.yaml` for full workflow specification.

## Troubleshooting

### Issue: Import Errors
**Solution:** Ensure you're in the repository root and Python 3.11+ is active.

### Issue: Precision Warnings
**Solution:** Verify `mpmath.dps = 80` is set in each verification script.

### Issue: Memory Errors
**Solution:** Increase available RAM or reduce lattice size in simulations.

### Issue: Slow Performance
**Solution:** Use Docker with `--cpus=8` flag or run on HPC cluster.

## Verification Checklist

- [ ] All Category A claims pass with residual < 10^-14
- [ ] All Category A- claims match phenomenological values
- [ ] All Category C claims align with DESI/JWST/ACT data
- [ ] No falsification criteria triggered (L1-L6)
- [ ] Audit reports show no parameter drift
- [ ] Docker reproduction succeeds
- [ ] SHA256 checksums match

## Contact

**Maintainer:** Philipp Rietz  
**Email:** badbugs.arts@gmail.com  
**ORCID:** 0009-0007-4307-1609  
**DOI:** 10.5281/zenodo.17835200

## License

CC-BY-4.0 - See LICENSE.md

---
**Last Updated:** 2026-04-07  
**Framework Version:** 3.9
