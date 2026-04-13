# UIDT Core Proof Engine

**Mathematical Core of the Yang-Mills Mass Gap Proof**

## Overview

This directory contains the protected mathematical core implementing the constructive proof of the Yang-Mills mass gap via Banach fixed-point theorem.

## Modules

| Module | Purpose | Evidence Category |
|--------|---------|-------------------|
| `uidt_proof_engine.py` | Main proof engine, Banach contraction | [A] |
| `rg_closure.py` | RG fixed point: 5κ² = 3λ_S | [A] |
| `banach_proof.py` | Banach fixed-point construction | [A] |

## API Overview

### `uidt_proof_engine.py`
```python
from core.uidt_proof_engine import UIDTProofEngine

engine = UIDTProofEngine(precision=80)
result = engine.verify_spectral_gap()
# Returns: {'Delta': mpf('1.710'), 'residual': mpf('< 1e-14')}
```

### Entry Points
- `verify_spectral_gap()` — Δ = 1.710 GeV [A]
- `verify_rg_fixed_point()` — 5κ² = 3λ_S [A]
- `compute_banach_contraction()` — Fixed-point existence [A]

## Evidence Categories

All claims in `core/` are **Category A** (residual < 10^-14).

## Claim References

- **C-001:** Δ = 1.710 ± 0.015 GeV
- **C-010:** 5κ² = 3λ_S (residual < 10^-14)
- **C-006:** λ_S = 5κ²/3 ≈ 0.41̄6̄ ± 0.007

## Protected Status

⚠️ **DUAL APPROVAL REQUIRED** for any changes to `core/`.

---
**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)
