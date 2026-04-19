# Permanent Integration Record: cblab/raumzeit

**Document type**: External Framework Integration Reference
**Repository**: Mass-Gap/UIDT-Framework-v3.9-Canonical
**External framework**: cblab/raumzeit
**Repository ID**: 1207002944
**URL**: https://github.com/cblab/raumzeit
**Integration date**: 2026-04-19
**UIDT version**: v3.9 Canonical
**Status**: Active — Path A: Spectral Gap Search
**DOI**: 10.5281/zenodo.17835200

---

## 1. Framework Identification

**raumzeit** is a simulation framework for emergent geometry in growing
causal graphs.  It tests whether purely local, weighted edge rules can
stabilise macroscopic diffusion geometry.  The maintained engine is:

```
cblab/raumzeit/emergent-geometry-causal-graphs/
```

Canonical configs (exactly three models in scope):

| Config | Role | V9 Term |
|--------|------|---------|
| `configs/baseline_ref.yaml` | Control baseline | Off |
| `configs/v8a_fast.yaml` | Contrast (no V9) | Off |
| `configs/v9a_fast.yaml` | **PRIMARY** (UIDT probe) | Ball coherence ON |

Canonical batch definition: `configs/paper_batch_ref.yaml`.

---

## 2. UIDT ↔ raumzeit Constant Mapping

| UIDT Constant | Value [Category] | raumzeit Observable | Path | Status |
|---------------|------------------|---------------------|------|--------|
| Δ\* | 1.710 ± 0.015 GeV [A] | `g_fc = ds_front − ds_core` (K7) | **A** | **THIS PR** |
| γ | 16.339 [A-] | sector\_balance\_ratio (V9 ball coherence) | B | Future |
| E\_T | 2.44 MeV [C] | `log₂(peak_layer_ratio)` (layer profiles) | C | Future |
| κ | 0.500 ± 0.008 [A] | V9\_ALPHA tuning parameter | Config | Proxy |
| λ\_S | 5κ²/3 = 0.41̄6̄ ± 0.007 [A] | V9\_W\_REDUNDANT weight | Config | Proxy |

---

## 3. K1–K7 Diagnostic Hierarchy

The K-diagnostic suite in raumzeit measures emergent geometric properties
at multiple scales.  Each diagnostic maps to a potential UIDT observable:

| K | Source file | Primary function | Observable | UIDT Mapping |
|---|------------|------------------|------------|--------------|
| K1 | `diagnostics_k1.py` | `measure_k1()` | H\_degree, mean\_weight, max\_level | Baseline structure |
| K2 | `diagnostics_k2.py` | `measure_k2_global()` | `ds_est` (spectral dim.), `dv_est` (volume growth) | Spectral scaling |
| K3 | `diagnostics_k7.py` | `estimate_isotropy_defect()` | `iso_defect` (CV of branch counts) | Geometric isotropy |
| K4 | `diagnostics_k4.py` | `measure_k4_global()` | `mean_herf`, `path_efficiency` | Transport properties |
| K5 | `diagnostics_k5.py` | `measure_k5_global()` | `shell_entropy`, `peak_shell` | Radial structure (→ E\_T) |
| K6 | `diagnostics_k7.py` | `rank_quantile_partition_from_dist()` | core/mid/front node sets | Quantile stratification |
| **K7** | **`diagnostics_k7.py`** | **`measure_anchor()`** | **`g_fc`**, ds\_core, ds\_front | **Δ\* proxy (PRIMARY)** |

---

## 4. Critical API Reference

### 4.1 K7 Fixed-Anchor Measurement (`diagnostics_k7.py`)

```python
def measure_anchor(g: GraphState, anchor: dict, config: dict) -> dict | None:
    """
    Returns a dict with fields:
        ds_global, ds_core, ds_mid, ds_front,
        g_fm, g_mc, g_fc,              # <-- g_fc is the UIDT gap proxy
        iso_defect, dv_global,
        region_nodes, shadow_mean_degree, ...
    """
```

Key implementation details:
1. BFS region sampled from fixed seed (`sample_bfs_region_from_seed`)
2. Shadow adjacency built over region (`_build_shadow_adjacency`)
3. Return probabilities estimated via random walker (`_estimate_return_probabilities`)
4. Spectral dimension from log-ratio of return probs (`_estimate_spectral_dimension`)
5. Region partitioned into core (50%), mid (30%), front (20%) by graph distance
6. Stratified spectral dims computed; `g_fc = ds_front - ds_core`

### 4.2 Spectral Dimension Estimator (`diagnostics_k2.py`)

```python
def _estimate_spectral_dimension(return_probs: dict[str, float]) -> float | None:
    """
    d_s = -2 * ln(P_b / P_a) / ln(b / a)
    for consecutive time pairs (a, b) in taus = [2, 4, 8, 16].
    Returns mean over valid pairs.
    """
```

### 4.3 V9 Ball Coherence (archive — reference monolith)

The V9 term in `v9a_fast.yaml` enables mesoscopic ball coherence:
- Rewards edges that enhance sphere shell balance
- Suppresses redundant inner overlap
- Tunable via `V9_ALPHA`, `V9_W_SECTOR`, `V9_W_REDUNDANT`

---

## 5. Batch Execution Protocol

```bash
# From raumzeit repository root:
cd emergent-geometry-causal-graphs/

# Canonical reproduction:
python scripts/run_batch.py --config configs/paper_batch_ref.yaml
python scripts/summarize_results.py
python scripts/make_reference_figures.py

# UIDT-specific (Path A — spectral gap):
python scripts/run_batch.py --config configs/v9a_fast.yaml
# Output: results/<run_id>/observables.json  (contains observables_k7 array)
```

Full reproducibility details: `emergent-geometry-causal-graphs/REPRODUCIBILITY.md`.

---

## 6. Path A Validation Protocol

### Hypothesis

The dimensionless dimensional gap `g_fc = ds(front) - ds(core)` from
K7 fixed-anchor measurements clusters near the numerical value 1.710,
matching UIDT's predicted Yang-Mills spectral gap Δ\* = 1.710 ± 0.015 GeV.

### Validation thresholds

| Result | Criterion | Evidence | Exit code |
|--------|-----------|----------|-----------|
| PASS | \|mean(g\_fc) − 1.710\| ≤ 0.015 | [B] | 0 |
| NEAR | \|mean(g\_fc) − 1.710\| ≤ 0.030 | [B] | 1 |
| MARGINAL | \|z-score\| < 2.0 | [C] | 1 |
| FAIL | Otherwise | [D] | 2 |

### Execution

```bash
# From UIDT repository:
python verification/scripts/hybrid_uidt_raumzeit_spectral_gap.py \
    /path/to/raumzeit/results/observables.json \
    --output verification_reports/path_a_results.txt
```

---

## 7. Limitations & Caveats

### L4 (RG-Flow Derivation)

γ = 16.339 is calibrated [A-], not yet derived from RG first principles.
The raumzeit sector-balance ratio may provide a numerical pathway to
validate the RG cascade, but this requires Path B implementation.

### Mapping Caveat

The g\_fc proxy is a *dimensionless* quantity from graph-distance
stratification.  Its numerical coincidence with Δ\* = 1.710 GeV
(a physical energy scale) does NOT imply dimensional equivalence.
A rigorous mapping requires establishing the lattice spacing and
continuum limit of the causal-set framework.

### Finite-Size Effects

K7 measurements at small N (< 1000 nodes) exhibit increased variance.
Recommendations: N ≥ 2000, num\_anchors ≥ 8, multiple random seeds.

---

## 8. Governance

- **Approval chain**: Code review → Guardian consensus → P. Rietz sign-off
- **Evidence category**: [B] (numerical robustness vs. emergent framework)
- **Protected constants**: All UIDT canonical values are read-only
- **External reference**: Immutable (cblab/raumzeit, ID: 1207002944)
- **Branch**: `TKT-20260419-hybrid-raumzeit-spectral-gap`
- **Anti-tampering**: Additive only; no deletions in `core/` or `modules/`

---

## 9. References

```bibtex
@misc{raumzeit2026,
    author = {cblab},
    title  = {raumzeit: Simulation Framework for Emergent Geometry
              in Growing Causal Graphs},
    url    = {https://github.com/cblab/raumzeit},
    year   = {2026},
    note   = {Repository ID: 1207002944}
}

@article{UIDT2026,
    author    = {Rietz, Philipp},
    title     = {Vacuum Information Density as the Fundamental
                 Geometric Scalar},
    year      = {2026},
    doi       = {10.5281/zenodo.17835200},
    publisher = {Zenodo},
    version   = {3.9 Canonical}
}
```

---

*Maintainer: P. Rietz — DOI: 10.5281/zenodo.17835200*
*Do not modify canonical constants or evidence categories without PI approval.*
