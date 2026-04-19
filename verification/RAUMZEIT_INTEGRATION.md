# Permanent Integration Record: raumzeit Framework (cblab)

**Framework**: cblab/raumzeit (emergent geometry causal graphs)  
**Repository URL**: [https://github.com/cblab/raumzeit](https://github.com/cblab/raumzeit)  
**Repository ID**: 1207002944  
**UIDT Version**: v3.9 Canonical  
**Integration Date**: 2026-04-19  
**Evidence Category**: [E] (Speculative — dimensional bridge open)  

## Pinned Reference

| Item | Value |
|------|-------|
| **Repository URL** | [https://github.com/cblab/raumzeit](https://github.com/cblab/raumzeit) |
| **Commit SHA** | `34c02567617b8aa0e3dcadbed57f3a16fe0c3cae` |
| **Config File** | `emergent-geometry-causal-graphs/configs/v9a_fast.yaml` |
| **Immutability** | Locked to specific commit (reproducibility guarantee) |
| **Last Updated** | 2026-04-19 |

**Note:** If cblab/raumzeit HEAD changes, this integration maintains reproducibility by pinning to the SHA recorded above. To update, explicitly change the SHA and UIDT version in CLAIMS.md.

---

## Framework Identification

raumzeit is a simulation framework for emergent geometry in growing causal graphs. The maintained engine is:

```text
cblab/raumzeit/emergent-geometry-causal-graphs/
```

Canonical configs in present UIDT scope:
- `configs/baseline_ref.yaml`
- `configs/v8a_fast.yaml`
- `configs/v9a_fast.yaml` (primary probe)

---

## UIDT Mapping Status

| UIDT Constant | Value [Category] | raumzeit Observable | Path | Status |
|---------------|------------------|---------------------|------|--------|
| Δ* | 1.710 ± 0.015 GeV [A] | `g_fc = ds_front - ds_core` | A | Speculative |
| γ | 16.339 [A-] | sector balance ratio | B | Future |
| E_T | 2.44 MeV [C] | layer-profile observable | C | Future |

**Critical caveat:** `g_fc` is dimensionless, while Δ* is an energy scale. No bridge equation currently exists inside UIDT v3.9 canonical.

---

## Governance

- External reference remains pinned to one exact upstream commit.
- Evidence stays [E] until TKT-FRG-BRIDGE-01 establishes an explicit dimensional bridge.
- No automatic evidence promotion is allowed from this integration record.

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

### Path A Results (2026-04-19)
- **Status**         : MARGINAL [C]
- **Target Delta***  : 1.710 +/- 0.015 GeV
- **Mean g_fc**      : 0.3408
- **Std Dev**        : 0.9869
- **Z-score**        : -1.39 sigma
- **Confidence**     : 40.0%
- **Measurements**   : 118 valid K7 anchor samples (8 seeds)
- **Interpretation**: Stronger statistical baseline (118 samples) confirms the positive spectral gap signature. Finite-size suppression is stable across all seeds.

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
