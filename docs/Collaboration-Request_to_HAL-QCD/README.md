```markdown
# UIDT Framework v3.9 — Canonical Implementation

## Overview

This repository hosts the **canonical reference implementation** of the **Unified Information‑Density Theory (UIDT)**, version **3.9**.  
The framework provides **high‑precision numerical infrastructure** for the verification of vacuum spectral gaps and the computation of chromomagnetic mass splittings in heavy‑baryon spectroscopy.

UIDT v3.9 is designed for **audit‑grade reproducibility**, **extended‑precision numerics**, and **formal compatibility with lattice‑QCD workflows**, including HAL QCD interfaces.

---

## Key Applications (v3.9)

### Ξ<sub>cc</sub> Isospin Splitting
- **Prediction:**  
  \[
  \Delta M(\Xi_{cc}) = 1.504\ \text{MeV}
  \]
- **Method:** Four‑term chromomagnetic decomposition  
- **Status:** Verified against internal consistency checks

### Vacuum Spectral Gap
- **Result:**  
  \[
  \Delta^\* = 1.71003504674\ldots\ \text{GeV}
  \]
- **Precision:** 80‑digit numerical verification  
- **Status:** Proven (Category A)

### HAL QCD Integration
- Formal interface for **cc‑diquark NBS wave‑function data**
- Designed for direct ingestion of HAL QCD lattice outputs

---

## Core Parameter Ledger

| Parameter | Symbol | Value | Category |
|---------|--------|-------|----------|
| Spectral Gap | \(\Delta^\*\) | 1.710 GeV | **A** (Proven) |
| Gamma Invariant | \(\gamma\) | 16.339 | **A‑** (Phenomenological) |
| Isospin Splitting | \(\Delta M(\Xi_{cc})\) | 1.504 MeV | **B** (Verified) |

---

## Quick Start

### Prerequisites
- Python **3.10+**
- `mpmath` — required for ≥80‑digit precision arithmetic
- `pytest` — verification and regression test suite

### Installation
```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical
pip install -r requirements.txt
```

---

## Verification

To reproduce the **80‑digit residual checks** and **fixed‑point convergence tests**:

```bash
pytest verification/tests/
```

All verification routines are deterministic and seed‑controlled.

---

## Citation

If you use this framework in academic or technical work, please cite:

> **Rietz, P.** (2026).  
> *UIDT v3.9: Lattice‑QCD Determination of \(|\psi_{cc}(0)|^2\) for the Ξ<sub>cc</sub> Diquark System.*  
> Zenodo.  
> **DOI:** 10.5281/zenodo.19157809


---

## Contact & Collaboration

- **Author:** Philipp Rietz  
- **Email:** uidt-framework@outlook.com  
- **ORCID:** 0009‑0007‑4307‑1609  

Collaboration requests, replication reports, and formal critiques are welcome.

---

## Disclaimer

⚠️ **Active Research Programme**

UIDT is under continuous development.  
**Transparency takes precedence over narrative closure.**

- Tensions in **H₀** and **S₈** are explicitly documented.
- No cosmological tension is declared “solved.”
- All claims are traceable to code, numerics, or cited datasets.

---

© 2026 — UIDT Research Programme  
Licensed for academic use with attribution.
```