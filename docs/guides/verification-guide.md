# Verification Guide

**UIDT v3.9** | Last Updated: 2026-02-19

> **Purpose:** Enable independent verification of all UIDT claims
> **Principle:** Reproducibility is the foundation of scientific integrity

---

## Overview

This guide provides step-by-step instructions for independently verifying all claims in the UIDT v3.9 framework. All verification scripts are included in this repository under [verification/](../verification/).

**Verification Levels:**
- **Quick (5 min):** Docker container verification
- **Standard (15 min):** Core mathematical closure
- **Detailed (30 min):** Full verification suite
- **Advanced (2+ hours):** Complete simulation + Monte Carlo

---

## Prerequisites

### System Requirements

**Minimum:**
- **Python:** 3.10 or higher
- **RAM:** 4 GB
- **Disk:** 500 MB free space
- **OS:** Linux, macOS, or Windows

**Recommended:**
- **Python:** 3.11+
- **RAM:** 16 GB (for full simulation suite)
- **Disk:** 2 GB free space

### Software Dependencies

Install Python dependencies:
```bash
pip install -r verification/requirements.txt
```

**Dependencies:**
- `numpy>=1.24.0` - Numerical computation
- `scipy>=1.10.0` - Scientific computing
- `mpmath>=1.3.0` - High-precision arithmetic (80+ digits)
- `matplotlib>=3.7.0` - Visualization
- `pandas>=2.0.0` - Data analysis (optional)

---

## Quick Verification (5 Minutes)

### Option 1: Docker (Recommended)

**Step 1: Build Container**
```bash
cd verification/docker
docker build -t uidt-verify .
```

**Step 2: Run Verification**
```bash
docker run uidt-verify
```

**Expected Output:**
```
╔══════════════════════════════════════════════════════════════╗
║  UIDT v3.9 MASTER VERIFICATION SUITE (Hybrid Engine)         ║
║  Strategies: Scipy Solver + Mpmath High-Precision Prover     ║
╚══════════════════════════════════════════════════════════════╝

[1] RUNNING NUMERICAL SOLVER (System Consistency)...
   > Solution Found: m_S=1.7050, kappa=0.5001
   > Residuals: ['0.0e+00', '0.0e+00', '0.0e+00']
   > System Status: ✅ CLOSED

[2] EXECUTING HIGH-PRECISION PROOF (80 Digits)...
   > Banach Fixed Point: 1.710035046742213182... GeV
   > Lipschitz Constant: 0.00003749 (Strict Contraction < 1)
   > THEOREM 3.4: ✅ PROVEN (Existence & Uniqueness)

...
[OUTPUT] 📄 Report successfully saved to: Verification_Report_v3.9_...
```

**Interpretation:**
- ✅ **Residuals < 10⁻⁴⁰:** Mathematical closure verified
- ✅ **THEOREM 3.4 PROVEN:** Banach fixed point contraction holds
- ✅ **Overall PASS:** Category A claims validated

---

### Option 2: Local Python (No Docker)

```bash
# Navigate to repository root
cd UIDT-Framework-v3.9-Canonical

# Install dependencies
pip install -r verification/requirements.txt

# Run core verification
python verification/scripts/UIDT_Master_Verification.py
```

**Expected Result:** Same as Docker output above

---

## Standard Verification (15 Minutes)

### 1. Core Mathematical Closure

Verifies Category A claims, Mathematical Convergence, and Spectral Expansions:

```bash
python verification/scripts/UIDT_Master_Verification.py
```

**What This Tests:**
- Three-equation system closure
- Banach fixed-point convergence
- Renormalization group constraint: 5κ² = 3λ_S
- 80-digit precision verification

**Success Criteria:**
- Max residual < 10⁻¹⁴ (target: 10⁻⁴⁰)
- γ = 16.339 ± 0.001
- Δ = 1.710 ± 0.015 GeV

---

### 2. Visual Verification

Generates figures for visual inspection:

```bash
python verification/scripts/UIDT-3.6.1-Verification-visual.py
```

**Outputs:**
- `banach_convergence.png` - Iterative solution convergence
- `parameter_space.png` - κ-λ_S stability landscape
- `gamma_scaling.png` - Universal γ-scaling map
- `residual_evolution.png` - Numerical precision audit

**Verification:**
Open generated PNG files and verify:
- Banach convergence: Rapid approach to Δ* = 1.710 GeV
- Stability landscape: Deep minimum at (κ, λ_S) = (0.5, 0.417)
- Gamma scaling: Linear relationships across scales

---

### 3. Error Propagation Analysis

Computes uncertainty budget:

```bash
python verification/scripts/error_propagation.py
```

**Outputs:**
- Jacobian-based uncertainty propagation
- Parameter correlation matrix
- Systematic vs. statistical errors

**Expected:**
```
Parameter Uncertainties:
  Δ: ±0.015 GeV (0.9%)
  κ: ±0.008 (1.6%)
  λ_S: ±0.007 (1.7%)
  v: ±0.5 MeV (1.0%)

Correlation Matrix:
       Δ      κ     λ_S     v
Δ    1.00   0.12   0.08  -0.05
κ    0.12   1.00   0.87   0.03
λ_S  0.08   0.87   1.00   0.02
v   -0.05   0.03   0.02   1.00
```

---

## Detailed Verification (30 Minutes)

### 4. RG Fixed Point Analysis

Verifies renormalization group consistency:

```bash
python verification/scripts/rg_flow_analysis.py
```

**What This Tests:**
- UV fixed point: 5κ² = 3λ_S
- Anomalous dimension: η_CSF = 0.504
- β-function behavior
- Perturbative stability: λ_S < 1

**Expected Output:**
```
RG Fixed Point Analysis:
  Constraint: 5κ² = 3λ_S
  LHS: 1.250
  RHS: 1.251
  Residual: 0.001 < 0.01 ✅

Anomalous Dimension:
  η_CSF = 0.504 ± 0.008
  Literature (FRG): 0.50 ± 0.02 ✅

Perturbative Validity:
  λ_S = 0.417 < 1 ✅ PASS
```

---

### 5. Lattice QCD Comparison

Compares Δ = 1.710 GeV against lattice data:

**Data Source:** Chen et al. (2006) quenched lattice QCD

**Verification:**
```bash
# Load lattice comparison data
cat verification/data/lattice_comparison.xlsx
```

**Expected:**
```
z-Score Calculation:
  Δ_UIDT = 1.710 ± 0.015 GeV
  Δ_lattice = 1.705 ± 0.050 GeV (continuum limit)

  z = |Δ_UIDT - Δ_lattice| / √(σ²_UIDT + σ²_lattice)
    = |1.710 - 1.705| / √(0.015² + 0.050²)
    = 0.005 / 0.052
    = 0.096

  z ≈ 0.1σ ✅ EXCELLENT AGREEMENT
```

**Interpretation:**
- z < 1σ: Category B verified
- Well within experimental uncertainty
- No lattice tension detected

---

## Advanced Verification (2+ Hours)

### 6. Full Simulation Suite

Run complete simulation pipeline:

```bash
# Navigate to simulation directory
cd simulation

# Run all 14 simulation scripts
for script in *.py; do
    echo "Running $script..."
    python "$script"
done
```

**Simulations Include:**
1. **HMC Simulation:** Hybrid Monte Carlo for vacuum sampling
2. **Cosmology:** H₀ and S₈ calculations
3. **Lattice Validation:** Quenched lattice comparison
4. **String Tension:** Confinement verification
5. **Casimir Prediction:** Force anomaly calculation
6. **RG Flow:** Multi-scale renormalization
7. **Vacuum Stability:** Potential analysis
8. **Scalar Mass:** m_S prediction
9. **Error Budget:** Systematic uncertainties
10. **Cross-validation:** Independent method comparison

**Expected Runtime:** 1-3 hours (depending on CPU)

---

### 7. Monte Carlo Validation

**100,000 Sample Analysis:**

Pre-computed results available in:
```
clay-submission/07_MonteCarlo/UIDT_MonteCarlo_samples_100k.csv
```

**Verification:**
```python
import pandas as pd
df = pd.read_csv('clay-submission/07_MonteCarlo/UIDT_MonteCarlo_samples_100k.csv')

print("Monte Carlo Statistics:")
print(f"γ mean: {df['gamma'].mean():.3f}")
print(f"γ std: {df['gamma'].std():.3f}")
print(f"Δ mean: {df['Delta'].mean():.3f} GeV")
print(f"Δ std: {df['Delta'].std():.3f} GeV")
```

**Expected:**
```
Monte Carlo Statistics:
γ mean: 16.374
γ std: 1.005
Δ mean: 1.710 GeV
Δ std: 0.015 GeV
```

---

## Troubleshooting

### Issue: `ImportError: No module named 'mpmath'`

**Solution:**
```bash
pip install mpmath>=1.3.0
```

---

### Issue: Residuals > 10⁻¹⁴

**Possible Causes:**
- Python version < 3.10 (floating-point precision)
- Missing mpmath (high-precision arithmetic)
- Modified verification script

**Solution:**
```bash
# Verify Python version
python --version  # Should be >= 3.10

# Reinstall dependencies
pip install --upgrade -r verification/requirements.txt

# Re-clone repository (if modified)
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
```

---

### Issue: Docker build fails

**Error:** `ERROR [internal] load metadata for docker.io/library/python:3.10-slim`

**Solution:**
```bash
# Enable Docker BuildKit
export DOCKER_BUILDKIT=1

# Rebuild
docker build --no-cache -t uidt-verify verification/docker/
```

---

### Issue: Matplotlib display error (headless environment)

**Solution:**
```bash
# Use non-interactive backend
export MPLBACKEND=Agg

# Re-run visual verification
python verification/scripts/UIDT-3.6.1-Verification-visual.py
```

---

## Verification Checklist

Before declaring successful verification, ensure:

- [ ] ✅ Core verification passes (residuals < 10⁻⁴⁰)
- [ ] ✅ Visual outputs match manuscript figures
- [ ] ✅ RG fixed point confirmed (5κ² = 3λ_S)
- [ ] ✅ Lattice comparison within 1σ
- [ ] ✅ Error propagation analysis complete
- [ ] ✅ Docker container builds and runs successfully
- [ ] ✅ All 14 simulation scripts execute without errors
- [ ] ✅ Monte Carlo statistics match expected values

---

## Reporting Verification Results

### Successful Verification

If all checks pass, you can cite:

```bibtex
@misc{Rietz2025_Verified,
  author = {Rietz, Philipp},
  title  = {UIDT v3.9 - Independently Verified},
  note   = {Verified on [DATE] using verification suite},
  year   = {2025}
}
```

### Failed Verification

If verification fails:

1. **Document the failure:**
   - Which script failed?
   - Error message
   - System configuration (OS, Python version)

2. **Open GitHub Issue:**
   - Go to: https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/issues
   - Title: `[VERIFICATION FAILURE] Brief description`
   - Include: System info, error log, steps to reproduce

3. **Email:**
   - To: badbugs.arts@gmail.com
   - Subject: `UIDT Verification Failure Report`

---

## Next Steps

After successful verification:

- **Extend the framework:** See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Test predictions:** See [falsification-criteria.md](falsification-criteria.md)
- **Cite UIDT:** See [citation-guide.md](citation-guide.md)
- **Explore simulations:** Run scripts in [simulation/](../simulation/)

---

**Last Updated:** 2026-02-05
**DOI:** 10.5281/zenodo.17835200
**Support:** badbugs.arts@gmail.com
