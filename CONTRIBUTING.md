# Contributing to UIDT Canonical

Thank you for your interest in the Unified Information-Density Theory. As this is a **canonical scientific record**, contributions are strictly regulated to ensure data integrity.

## 🧪 Scientific Integrity Policy

**The Core Constants are Immutable:**
The values for $\Delta$ (1.710 GeV) and $\gamma$ (16.339) are analytically derived from the theory's core Lagrangian. They **cannot be "tuned" or changed** via pull requests unless a mathematical error in the derivation itself is proven.

### ✅ What We Accept
* **Code Optimization:** Improvements to the Python simulation scripts (speed, memory usage) that *reproduce the exact same physics*.
* **Documentation:** Fixes to typos, clearer explanations, or translations.
* **Visualization:** New plotting scripts to visualize the data in novel ways.
* **External Validation:** Scripts that compare UIDT predictions against new external datasets (e.g., Euclid, future DESI releases).

### ❌ What We Reject
* **Parameter Tuning:** Attempts to manually fit $\Delta$ or $\gamma$ to data. The theory is parameter-free.
* **Non-Canonical Physics:** Pull requests introducing arbitrary scalar potentials not derived from the information-density axiom.

## 🛠 How to Submit
1.  **Fork** the repository.
2.  Create a branch: `git checkout -b feature/optimization-name`.
3.  **Verify** your changes: Run `python UIDT-3.6.1-Verification.py` to ensure residuals are still $< 10^{-14}$.
4.  Submit a **Pull Request** with a description of your changes.

---
*By contributing, you agree that your code will be licensed under CC BY 4.0.*