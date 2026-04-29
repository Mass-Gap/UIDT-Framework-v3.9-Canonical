# UIDT Framework Simulation Scripts

**Lattice QCD and Cosmological Simulations for v3.9**

## Purpose

This directory contains standalone simulation scripts for:
- **Lattice QCD:** Hybrid Monte Carlo (HMC) simulations with SU(3) gauge group
- **Cosmology:** ΛCDM parameter evolution and DESI alignment
- **Validation:** Evidence analysis and lattice validation
- **Monte Carlo Data:** Statistical validation dataset (v3.3) → see `monte_carlo/`

All simulations use parameters from `CANONICAL/CONSTANTS.md` and are designed to validate claims in `LEDGER/CLAIMS.json`.

## Dependencies

```bash
pip install mpmath==1.3.0 numpy==1.24.0 scipy==1.11.0 matplotlib==3.7.0
```

**Optional (GPU acceleration):**
```bash
pip install cupy-cuda11x  # For CUDA 11.x
```

## Monte Carlo Validation Data

The `monte_carlo/` subdirectory contains the complete statistical validation dataset
for the UIDT Ω framework (v3.3):

| File | Description |
|:---|:---|
| `monte_carlo/README.md` | Full dataset documentation |
| `monte_carlo/UIDT_MonteCarlo_summary.csv` | Mean/std/CI for Δ, γ, Ψ (N=100k) |
| `monte_carlo/UIDT_MonteCarlo_summary_table_short.csv` | Abbreviated summary |
| `monte_carlo/UIDT_MonteCarlo_correlation_matrix.csv` | 8×8 Pearson-r matrix |
| `monte_carlo/UIDT_MonteCarlo_summary_table.tex` | LaTeX publication table |
| `monte_carlo/UIDT_HighPrecision_mean_values.csv` | mpmath 80-digit precision means |
| `monte_carlo/PLOTS_REGISTRY.md` | Plot catalog + reproduction code |
| `monte_carlo/DATA_NOTE.md` | Note: 19 MB raw CSV → Zenodo DOI 10.5281/zenodo.17554179 |

**Raw 100k sample chain (19 MB):** archived at Zenodo  
https://doi.org/10.5281/zenodo.17554179

**Key results (N=100,000):**

| Parameter | Mean | Std | LEDGER | Evidence |
|:---|:---|:---|:---|:---|
| Δ* (GeV) | 1.7100444 | 0.0149928 | 1.710 ± 0.015 | [A] |
| γ | 16.373948 | 1.005125 | 16.339 | [A-] |
| Ψ | 1291.759 | 159.125 | — | [A-] |

## Simulation Scripts

### Lattice QCD Simulations

| Script | Purpose | Evidence Category | Runtime |
|--------|---------|-------------------|---------|
| `uidt_v3_6_1_hmc_optimized.py` | GPU-optimized HMC pipeline | [A] | ~4 hours |
| `uidt_v3_6_1_hmc_real.py` | Full real-valued HMC with SU(3) | [A] | ~6 hours |
| `uidt_v3_6_1_lattice_validation.py` | Lattice spacing validation | [B] | ~1 hour |
| `uidt_v3_6_1_ape_smearing.py` | APE smearing for noise reduction | [B] | ~30 min |
| `uidt_v3_6_1_su3_expm_cayley_hamiltonian.py` | SU(3) exponential map | [A] | ~2 hours |

### Cosmological Simulations

| Script | Purpose | Evidence Category | Runtime |
|--------|---------|-------------------|---------|
| `uidt_v3_6_1_cosmology_simulator.py` | ΛCDM evolution with UIDT parameters | [C] | ~1 hour |
| `uidt_cosmic_simulation.py` | Cosmic structure formation | [C] | ~2 hours |

### Analysis & Validation

| Script | Purpose | Evidence Category | Runtime |
|--------|---------|-------------------|---------|
| `uidt_v3_6_1_evidence_analyzer.py` | Evidence classification validation | [A-E] | ~15 min |
| `uidt_v3_6_1_test.py` | Unit tests for simulation modules | [A] | ~5 min |
| `uidt_visual_3_6_1.py` | Visualization of lattice configurations | — | ~10 min |

### Integrators & Utilities

| Script | Purpose | Evidence Category | Runtime |
|--------|---------|-------------------|---------|
| `uidt_v3_6_1_omelyna_integrator2o.py` | Omelyan 2nd-order symplectic integrator | [A] | ~30 min |
| `uidt_v3_6_1_monitor_autotune.py` | HMC parameter auto-tuning | [B] | ~1 hour |
| `uidt_v3_6_1_update_vector.py` | Gauge field update routines | [A] | ~20 min |
| `uidt_v3_6_1_scalar_analyse.py` | Scalar field analysis | [D] | ~15 min |

## Execution Order

For full validation pipeline:

```bash
# 0. Monte Carlo baseline verification (fast)
python -m pytest verification/tests/test_monte_carlo_summary.py -v

# 1. Lattice Validation
python simulation/uidt_v3_6_1_lattice_validation.py

# 2. HMC Simulation (choose one)
python simulation/uidt_v3_6_1_hmc_optimized.py  # GPU
# OR
python simulation/uidt_v3_6_1_hmc_real.py       # CPU

# 3. Evidence Analysis
python simulation/uidt_v3_6_1_evidence_analyzer.py

# 4. Cosmology Validation
python simulation/uidt_v3_6_1_cosmology_simulator.py

# 5. Visualization
python simulation/uidt_visual_3_6_1.py
```

## Connection to Core Modules

Simulations import from:
- `modules/geometric_operator.py` — Geometric operator construction
- `modules/lattice_topology.py` — Lattice discretization
- `core/uidt_proof_engine.py` — Core proof logic

## Evidence Categories of Parameters Used

| Parameter | Value | Category | Source |
|-----------|-------|----------|--------|
| Δ | 1.710 ± 0.015 GeV | [A] | `CANONICAL/CONSTANTS.md` |
| κ | 0.500 ± 0.008 | [A] | `CANONICAL/CONSTANTS.md` |
| λ_S | 5κ²/3 ≈ 0.41̄ 6̄ ± 0.007 | [A] | `CANONICAL/CONSTANTS.md` |
| γ | 16.339 | [A-] | `CANONICAL/CONSTANTS.md` |
| v | 47.7 MeV | [A] | `CANONICAL/CONSTANTS.md` |
| H₀ | 70.4 ± 0.16 km/s/Mpc | [C] | `CANONICAL/CONSTANTS.md` |

## Configuration

All simulations read parameters from `CANONICAL/CONSTANTS.md`. To modify:

1. **DO NOT** edit simulation scripts directly
2. Update `CANONICAL/CONSTANTS.md` (requires dual approval)
3. Re-run verification suite to ensure consistency

## Output Format

See `simulation/DATA_FORMAT.md` for detailed specification of:
- Lattice configurations (ILDG-compatible)
- Ensemble specifications
- Gauge field storage format

## Performance Notes

- **GPU Acceleration:** `uidt_v3_6_1_hmc_optimized.py` requires CUDA-capable GPU
- **Memory:** Lattice simulations require ~8GB RAM minimum
- **Parallelization:** Use `OMP_NUM_THREADS` environment variable for CPU parallelization

## Troubleshooting

### Issue: CUDA Out of Memory
**Solution:** Reduce lattice size in configuration or use CPU version

### Issue: Slow Convergence
**Solution:** Run `uidt_v3_6_1_monitor_autotune.py` to optimize HMC parameters

### Issue: Numerical Instability
**Solution:** Verify `mpmath.dps = 80` is set and check for NaN values in output

## References

- FLAG 2024 Review: arXiv:2411.04268
- ILDG Data Format: https://www.lqcd.org/ildg/
- HMC Algorithm: Duane et al., Phys. Lett. B 195 (1987) 216
- MC Validation Data: https://doi.org/10.5281/zenodo.17554179

## Contact

**Maintainer:** Philipp Rietz  
**Email:** badbugs.arts@gmail.com  
**ORCID:** 0009-0007-4307-1609

---
**Last Updated:** 2026-04-29  
**Framework Version:** 3.9
