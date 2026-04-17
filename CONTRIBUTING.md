# Contributing to UIDT Canonical

Thank you for your interest in the Information-Geometric Constraint Framework (UIDT). As this is a **canonical scientific record and active research framework**, contributions are strictly regulated to ensure data integrity.

> [!NOTE]
> UIDT is an **active research framework**, not established physics. Contributions that improve reproducibility, documentation, or external validation are especially welcome. Core constants are analytically derived and immutable; see below.

## 🧪 Scientific Integrity Policy

**The Core Constants are Immutable:**
The values for $\Delta$ (1.710 GeV) and $\gamma$ (16.339) are analytically derived from the theory's core Lagrangian. They **cannot be "tuned" or changed** via pull requests unless a mathematical error in the derivation itself is proven.

### ✅ What We Accept
* **Code Optimization:** Improvements to the Python simulation scripts (speed, memory usage) that *reproduce the exact same physics*.
* **Documentation:** Fixes to typos, clearer explanations, or translations.
* **Visualization:** New plotting scripts to visualize the data in novel ways.
* **External Validation:** Scripts that compare UIDT predictions against new external datasets (e.g., Euclid, future DESI releases).
* **Limitation Documentation:** Well-reasoned additions to the known limitations register (L1–L5) with evidence category assigned.

### ❌ What We Reject
* **Parameter Tuning:** Attempts to manually fit $\Delta$ or $\gamma$ to data. The theory is parameter-free within the QFT sector.
* **Non-Canonical Physics:** Pull requests introducing arbitrary scalar potentials not derived from the information-density axiom.
* **Overclaiming:** PRs that upgrade evidence categories (e.g., D → A) without a complete mathematical proof and explicit maintainer review.

## 🛠 How to Submit
1.  **Fork** the repository.
2.  Create a branch: `git checkout -b feature/your-description`.
3.  **Verify** your changes: Run `python verification/scripts/UIDT_Master_Verification.py` to ensure residuals are still $< 10^{-14}$.
4.  Submit a **Pull Request** using the format `feat|fix|docs: <description> TKT-<ticket>` with a list of affected constants and their evidence categories.

---
*By contributing, you agree that your code will be licensed under CC BY 4.0.*
