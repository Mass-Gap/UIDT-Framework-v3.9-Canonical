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

Entry points and configs:
- core/uidt_proof_engine.py: CLI-style executable module (if __name__ == "__main__").
- verification/requirements.txt: pinned runtime for verification suite.
- .editorconfig, .gitattributes, .gitignore: formatting and VCS norms.

Separation of concerns:
- Mathematical kernels and high-precision numerics in core/ and modules/
- Tests and compliance checks in verification/
- Canonical constants, evidence, and governance in CANONICAL/, LEDGER/, and UIDT-OS/
- Manuscript and reproducibility materials in clay-submission/, docs/, manuscript/

#### 3. Test Strategy  
- Framework: pytest (see verification/requirements.txt)
- Layout: tests reside in verification/tests/ with test_*.py naming
- Scope:
  - Unit tests: cover individual scientific modules (e.g., test_geometric_operator.py, test_harmonic_predictions.py, test_lattice_topology.py, test_photonic_isomorphism.py)
  - System/compliance: documentation and simulation compliance checks (test_public_docs_compliance.py, test_simulation_compliance.py, test_reference_traceability.py, test_modules_language.py)
  - Engine verification: test_uidt_proof_engine.py validates proof engine contracts
- Mocking: Prefer real numerical pathways. Do not mock mpmath; precision and flows are part of correctness. Avoid stubbing scientific kernels; use deterministic seeds and fixed constants from canonical sources instead.
- Coverage expectations: Emphasize critical numerical pathways, invariant checks, and governance constraints. Include regression tests when adjusting precision, constants, or IO pathways.
- When to write tests:
  - Unit tests for new utilities, adapters, or non-core helpers
  - Integration tests when connecting modules to verification/data pipelines or RAG/adapter layers (e.g., UIDT-OS adapters)
  - Compliance tests for documentation traceability, evidence categories, or public-facing artifacts

#### 4. Code Style  
- Language: Python 3 with scientific stack. Keep code deterministic and numerically stable.
- Precision discipline:
  - Always set mp.dps = 80 locally in modules using mpmath
  - Never centralize mp.dps configuration; do not override below 80
- Typing and interfaces:
  - Provide explicit docstrings including units (e.g., GeV, GeV⁴)
  - Favor clear parameter names (Delta, Gamma, Kappa) consistent with docs and LEDGER
- Naming conventions:
  - Files: snake_case.py
  - Classes: PascalCase (e.g., UIDT_Prover)
  - Functions/vars: snake_case with domain-specific symbols where appropriate (e.g., Delta_star)
- Documentation style:
  - High-class English, scientifically precise
  - Include references/DOIs in module headers where relevant
  - Tag quantitative claims with evidence categories when appropriate in comments/docstrings
  - Prestige/closure wording is strictly forbidden unless a quantitative claim is validated at Category A/A-. Terms such as "ultimate", "holy grail", "definitive solution", or "resolved" MUST NOT be used otherwise. Cosmological statements (e.g., Hubble tension) are capped at Category C and must never be framed as "resolved".
  - Stratum separation is mandatory for scientific claims:
    - Stratum I (Empirical): Direct measurements with uncertainties (±; statistical/systematic; covariance) and primary sources.
    - Stratum II (Consensus): Current field status (e.g., "tension persists") with review/meta-analysis citation.
    - Stratum III (UIDT): Interpretative mapping to UIDT parameters and constructs.
  - Uncertainties: All numerical claims must specify the uncertainty model (statistical/systematic), covariance handling, and comparison metric (e.g., z-score, σ-agreement). Internal calibrations are never to be presented as empirical ground truth.
- Error handling:
  - Use explicit assertions for invariants (e.g., RG fixed point residuals, contraction L < 1)
  - Prefer fail-fast with informative error messages over silent degradation
- Logging/prints:
  - For CLI-like scripts, structured prints are acceptable for traceability
  - For library code, return values and raise exceptions; avoid printing in core routines where not required by verification contracts

#### 5. Common Patterns  
- Banach contraction fixed-point iterations for mass-gap style problems
- Explicit hierarchical decomposition of physical contributions (e.g., Δ⁴, γ-suppression, EW hierarchy, π⁻² factor)
- Deterministic numerical pipelines with pinned dependencies
- Governance constraints reflected in code (protected paths, evidence category tagging)
- Test organization by domain component and compliance dimensions

Reusable utilities and adapters:
- verification/scripts and UIDT-OS adapters provide orchestration and dataset/RAG utilities; prefer wrapping external services via small adapters that keep core deterministic and pure.

#### 6. Do's and Don'ts  
- Do
  - Set mp.dps = 80 in every module using mpmath
  - Keep algorithms and parameter flows in core/ and modules/ intact unless explicitly reviewed
  - Add docstrings with units, sources, and evidence categories where applicable
  - Add regression tests for any change that can affect numerical outputs or governance checks
  - Use canonical constants from CANONICAL/ and UIDT-OS/CANONICAL/ as read-only references
  - Respect repository governance: do not commit protected paths or internal secrets
- Don't
  - Do not modify mathematical core logic in core/ or modules/
  - Do not centralize or reduce precision settings; never mock mpmath
  - Do not introduce new physics claims beyond LEDGER/CLAIMS.json
  - Do not write local absolute paths into repo files
  - Do not change numerical behavior via DRY/SOLID refactors without validation
  - Do not perform refactors or "optimizations" that can jeopardize 80-digit stability. This includes replacing physically calibrated constants ("magic numbers") with dynamic variables, removing seemingly unused mpmath imports or guards, or introducing CPU/GPU math kernels that alter numerical pathways/rounding.

#### 7. Tools & Dependencies  
- Key libraries: mpmath (80+ digits), numpy, scipy, pandas, matplotlib, seaborn, pytest
- Orchestration and data: dvc, mlflow, pandera, great-expectations (with version guards), Prefect
- LLM/RAG utilities (auxiliary, optional for core numerics): langgraph, llama-index, unstructured, sentence-transformers, chroma store adapters; FastAPI/uvicorn for services
- Setup:
  - Use verification/requirements.txt to create a pinned environment for tests
  - Run pytest from repository root or verification/; prefer: python -m pytest verification/ -v --tb=short

#### 8. Other Notes  
- Evidence governance:
  - Adhere to LEDGER/CLAIMS.json categories; update only through documented processes
  - Classify quantitative statements in code comments where appropriate [A/A-/B/C/D/E]
- Protected paths and policies (summarized):
  - Never commit: UIDT-OS/, SECURITY.md, AGENTS.md, .claude/, .mcp.json, any .env files
  - Avoid touching releases/, docs/, or CANONICAL/ without explicit approval (often read-only)
- PR merge conditions:
  - Every PR must include: (1) a Claims Table (claim, evidence category, source), (2) a Reproduction Note (single command to reproduce quantitative tests), and (3) a successful DOI/arXiv resolution check for all cited sources. Phantom or hallucinated references are grounds for immediate rejection.
- Release naming:
  - Avoid semantic tags like v4.0. Releases must follow: update_Date_meaningfultitle-ticket-number
- Generation guidance for LLMs:
  - Maintain numerical determinism; prefer pure functions; inject configuration rather than global state, except mp.dps local setting
  - Keep outputs reproducible; pin versions; avoid network access at runtime in tests
  - Tests must never reduce precision or mock mpmath
  - When adding modules, include local precision guard and invariant assertions for RG relations
## Visualization Policy (Instructions for Jules)

- **Elite Scientific Standards:** Whenever generating scientific visualizations, plots, or diagrams, act at the absolute top-tier, world-class level (Nature/Science publication standard).
- **Epistemic Seriousness:** Visualizations must be highly evidential, strictly data-driven, and utterly serious. Avoid any decorative elements, 3D gimmicks, or visual clutter. Maximize information density (UIDT standard) and ensure perfect axes labeling, error bars, and methodological transparency.
- **Strict Repository Placement (File System Laws):**
  - Save raw plot data and verification visuals strictly in `verification/data/visualizations/` (never in `verification/scripts/` or root).
  - Save publication-ready, finalized figures directly to `manuscript/figures/` or `docs/assets/`.
  - **NEVER** save images or plots in the root directory, `UIDT-OS/**`, or any protected internal folders.

## Visualization Policy (Instructions for Jules)

- **Elite Scientific Standards:** Whenever generating scientific visualizations, plots, or diagrams, act at the absolute top-tier, world-class level (Nature/Science publication standard).
- **Epistemic Seriousness:** Visualizations must be highly evidential, strictly data-driven, and utterly serious. Avoid any decorative elements, 3D gimmicks, or visual clutter. Maximize information density (UIDT standard) and ensure perfect axes labeling, error bars, and methodological transparency.
- **Strict Repository Placement (File System Laws):**
  - Save raw plot data and verification visuals strictly in `verification/data/visualizations/` (never in `verification/scripts/` or root).
  - Save publication-ready, finalized figures directly to `manuscript/figures/` or `docs/assets/`.
  - **NEVER** save images or plots in the root directory, `UIDT-OS/**`, or any protected internal folders.
