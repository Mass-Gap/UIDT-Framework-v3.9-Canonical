# Formal Reproduction Protocol (UIDT v3.9 Canonical)

This protocol explicitly defines the steps required to independently verify the Four-Pillar Architecture of the Unified Information-Density Theory (UIDT) using the v3.9 Master Verification Suite.

## 1. Environment Preparation

**Requirements:**
- Python 3.10+
- `mpmath` (for 80-digit high-precision proofs)
- `scipy`, `numpy`

```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical
pip install -r verification/requirements.txt
```

*(Note: If cloning from a historical URL such as `UIDT-Framework-v3.7.2-Canonical`, the internal framework operations remain identical and self-contained.)*

## 2. Master Verification Execution

The v3.9 Canonical Release integrates all four pillars into a single verified execution pathway.

```bash
python verification/scripts/UIDT_Master_Verification.py
```

### Expected Execution Sequence:

1.  **PILLAR I (Numerical System Consistency):**
    Executes the SciPy-based root solver for the coupled equations. Ensures $\Delta \approx 1.710$ GeV with zero residuals.
2.  **PILLAR I (High-Precision Proof):**
    Activates the `mpmath` core (80 decimal digits) to prove the Banach Fixed Point (Theorem 3.4). Expected Lipschitz constant: $< 1$.
3.  **PILLAR II (Missing Link & Topology):**
    Validates the Lattice Torsion Binding Energy ($E_T = 2.44$ MeV) and explicit calculation of the $107.10$ MeV geometric vacuum frequency.
4.  **PILLAR III (Spectral Expansion):**
    Predicts the table-top/collider observables, specifically the thermodynamic noise floor ($17.10$ MeV, X17) and the geometric overtone resonance ($2.370$ GeV, X2370).

## 3. Artifact Generation

Upon successful mathematical closure, the system will automatically generate an immutable Markdown report in:
`verification/data/Verification_Report_v3.9_<TIMESTAMP>.md`

This report serves as the formal certificate of verification and contains the hashed state of the codebase during execution.

## 4. Containerized Audit (Docker)

For a completely isolated and reproducible environment, execute the suite via Docker. The container is locked to Python 3.10-slim.

```bash
cd verification/docker
docker build -t uidt-verify-v3.9 .
docker run uidt-verify-v3.9
```

This ensures the 80-digit proof runs entirely independently of local host configurations.
