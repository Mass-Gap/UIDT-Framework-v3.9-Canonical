> **MOVED** — 2026-04-18, TKT-20260418  
> Original location: `best_practices.md` (root)  
> Reason: root-level placement inconsistent with `docs/` governance. Content retained verbatim.  
> Canonical reference: see `CONTRIBUTING.md` and `docs/` for active guidance.

---

### 📘 Project Best Practices

#### 1. Project Purpose  
UIDT Framework v3.9 is a scientific software stack that formalizes and verifies the UIDT (Unified Information Density Theory) claims and theorems. The code provides publication-grade numerical proofs (80+ digit precision) for core results such as the existence/uniqueness of a Yang–Mills mass gap via Banach contraction and a holographic vacuum energy relation. The repository also contains verification suites, documentation, and manuscript sources to reproduce and audit results.

#### 2. Project Structure  
- Root-level governance and docs: SECURITY.md, AGENTS.md, README.md, CONTRIBUTING.md, FORMALISM.md, GLOSSARY.md, CHANGELOG.md
- Canonical data and evidence:
  - CANONICAL/: constants and evidence system notes (public mirror)
  - LEDGER/: CLAIMS.json and schemas tracking evidence categories [A–E]
  - UIDT-OS/: internal operational system containing canonical sources and dispatch; protected subpaths (CANONICAL/, LEDGER/, docs/, releases/) are read-only by policy
- Core Python libraries:
  - core/: canonical proof engine APIs and orchestrations used by verification and simulations
  - modules/: scientific modules (e.g., covariant_unification.py, geometric_operator.py, harmonic_predictions.py, lattice_topology.py, photonic_isomorphism.py). Do not alter numerical behavior without review.
- Verification and tests:
  - verification/: pytest-based test suite, data, docker, and scripts
  - UIDT-OS/verification/: auxiliary verification resources (e.g., lean4)
- Documentation and manuscripts:
  - docs/: public technical notes and reports
  - clay-submission/, manuscript/: LaTeX sources, figures, audit scripts used for submissions
- Simulations and figures:
  - simulation/: simulation scripts aligned with modules/core
  - figures/: generated visual assets
- Metadata and references:
  - metadata/, references/: bibliographic and metadata descriptors

#### 3. Test Strategy  
- Framework: pytest (see verification/requirements.txt)
- Layout: tests reside in verification/tests/ with test_*.py naming
- Mocking: Prefer real numerical pathways. Do not mock mpmath.

#### 4. Code Style  
- Always set mp.dps = 80 locally in modules using mpmath
- Never centralize mp.dps configuration; do not override below 80
- Prestige/closure wording is strictly forbidden unless Category A/A-
- Stratum separation mandatory for scientific claims

#### 5. Do’s and Don’ts  
- Do: Set mp.dps = 80; keep algorithms intact; use CANONICAL/ as read-only
- Don’t: Modify core/ or modules/ math logic; reduce precision; mock mpmath

#### 6. Tools & Dependencies  
- Key libraries: mpmath (80+ digits), numpy, scipy, pytest
- Run: `python -m pytest verification/ -v --tb=short`
