# 🏛️ UIDT Framework (v3.9 Canonical)
**Vacuum Information Density as the Fundamental Geometric Scalar**

The Unified Information-Density Theory (UIDT) is a theoretical framework proposing an information-geometric approach to the Yang-Mills Mass Gap and vacuum energy.

To ensure strict scientific integrity, this repository operates on a **Three-Layer Architecture**, strictly separating rigorous mathematical proofs from phenomenological calibrations and known limitations.

## 📐 Layer 1: The Mathematical Core [Category A]
**Status:** Mathematically closed, 80-digit precision verified.
This layer contains the load-bearing foundation of the UIDT framework. It relies purely on the Yang-Mills Hamiltonian and an information-geometric scalar coupling.
*   **Result:** Constructive derivation of a unique positive spectral gap $\Delta^* = 1.710 \pm 0.015$ GeV.
*   **Method:** Banach Fixed-Point mapping of a non-linear operator over a coupled system (Vacuum Stability, Mass Gap, RG Fixed Point equations).
*   **Verification:** Verified to $< 10^{-14}$ residuals using `mpmath` at 80-digit precision (see `/verification`).
*   **Note:** This is a spectral gap of the Hamiltonian, *not* a direct claim of a specific particle mass.

## 🔭 Layer 2: Empirical Calibration & Cosmology [Category C]
**Status:** Phenomenological, calibrated to external data (DESI, JWST).
This layer explores the macroscopic consequences of the $\gamma$-scaling invariant ($\gamma = 16.339$).
*   **Cosmology:** The framework provides a dynamic dark energy equation of state ($w_0 = -0.99$), calibrated to DESI Year-3 data.
*   **Vacuum Energy:** Establishes a hierarchical scaling mechanism that significantly suppresses the QFT vacuum energy expectation, though it does not resolve it completely from first principles.

## 🛑 Layer 3: Known Limitations & Open Questions (The "Honesty Ledger")
We actively maintain a ledger of anomalies where the current UIDT framework fails to match observation from pure first principles. These are open research questions:
1. **The $10^{10}$ Holographic Gap (L1):** The theoretical QCD information length ($2.64 \times 10^{-20}$ m) requires an unexplained geometric scaling factor of $\sim 10^{10}$ to match the macroscopically calibrated scale ($0.66$ nm). This mechanism is currently unknown.
2. **The Electron Mass Discrepancy (L2):** Simple $\gamma$-scaling power laws fail for the lepton sector. The prediction for the electron mass deviates by ~23% from the observed $0.511$ MeV.
3. **The Gamma Origin (L4):** While $\gamma = 16.339$ emerges as a highly consistent kinetic VEV, its reduction from the perturbative fixed point (55.8) currently lacks a fully closed, rigorous mathematical proof.

*For full details on our evidence grading system, see [`docs/evidence-classification.md`](docs/evidence-classification.md) and [`data/ledger/CLAIMS.json`](data/ledger/CLAIMS.json).*