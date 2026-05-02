# Documentation — UIDT Framework v3.9

> **DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)  
> **Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)

## Directory Index

| Directory | Description | Files | Evidence Range |
|-----------|-------------|------:|---------------|
| [`theory/`](theory/) | Core UIDT formalism: derivations, proofs, Lagrangian sectors | 20 | [A] — [A-] |
| [`predictions/`](predictions/) | Experimental predictions: LHC, glueball spectrum, cosmology | 8 | [C] — [D] |
| [`evidence/`](evidence/) | Evidence classification system, limitations L1–L6, falsification criteria | 8 | — |
| [`research/`](research/) | Active research notes with session dates (FRG, gamma derivation, L1–L5) | 51 | [D] — [E] |
| [`audits/`](audits/) | Epistemic audits, formal reviews, and self-consistency checks | 14 | — |
| [`guides/`](guides/) | Verification guides, reproduction protocols, PR review workflow | 7 | — |
| [`governance/`](governance/) | Quality gate mapping, branch protection policies | 1 | — |
| [`qa/`](qa/) | PR evidence review history and quality criteria | 7 | — |
| [`archive/`](archive/) | Historical documents and superseded analyses | 4 | — |
| [`archival-notes/`](archival-notes/) | Archival clarifications and attribution records | 3 | — |
| [`bugfix/`](bugfix/) | Bug analysis documentation | 1 | — |
| [`reviewer_decisions/`](reviewer_decisions/) | External reviewer interaction records | 1 | — |

## Quick Start

- **New to UIDT?** Start with [`theory/theoretical_notes.md`](theory/theoretical_notes.md)
- **Reproduce results:** See [`guides/reproduction-protocol.md`](guides/reproduction-protocol.md)
- **Run verification:** See [`guides/verification-guide.md`](guides/verification-guide.md)
- **Evidence system:** See [`evidence/evidence-classification.md`](evidence/evidence-classification.md)
- **Known limitations:** See [`evidence/limitations.md`](evidence/limitations.md)

## Evidence Classification (Reference)

| Tag | Category | Threshold | Example |
|-----|----------|-----------|---------|
| **[A]** | Mathematically Proven | residual < 10⁻¹⁴ | Δ* = 1.710 GeV |
| **[A-]** | Phenomenologically Calibrated | permanent | 5κ² = 3λ_S |
| **[B]** | Lattice QCD Consistent | z ≈ 0.37σ | Mass gap lattice |
| **[C]** | Observationally Calibrated | DESI/JWST/ACT | H₀, w₀ |
| **[D]** | Predicted (Unconfirmed) | — | m_S, Casimir |
| **[E]** | Withdrawn / Speculative | — | f₀(1710) glueball |

---

*"Vacuum Information Density as the Fundamental Geometric Scalar"*  
*CC BY 4.0 — P. Rietz*
