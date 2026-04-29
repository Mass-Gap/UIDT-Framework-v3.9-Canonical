# GitHub Release Asset Guide

**Purpose:** Step-by-step instructions for attaching the 3 Monte Carlo
diagnostic plot JPGs (and optionally the 19 MB CSV) as GitHub Release Assets.

---

## 1. Prerequisites

- GitHub CLI installed (`gh --version ≥ 2.0`)
- Authenticated to GitHub CLI: `gh auth login`
- Raw chain CSV available locally at
  `simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv`
  (download from Zenodo: `doi.org/10.5281/zenodo.17554179`)
- Plots reproduced locally via `PLOTS_REGISTRY.md` reproduction code

---

## 2. Create the Release Tag

```bash
# from repo root, on main branch
git tag v3.9-mc-plots
git push origin v3.9-mc-plots
```

---

## 3. Create the Release with Assets (GitHub CLI)

```bash
gh release create v3.9-mc-plots \\
  --title "UIDT v3.9 — Monte Carlo Diagnostic Plots" \\
  --notes """\
UIDT v3.9 Monte Carlo validation assets.

**Raw chain CSV (19 MB):**
Stored on Zenodo: https://doi.org/10.5281/zenodo.17554179

**Plot JPGs (3 files):**
Generated from the Zenodo CSV via PLOTS_REGISTRY.md.

Verification:
  pytest verification/tests/test_monte_carlo_summary.py -v
  python verification/scripts/verify_monte_carlo_research_notes.py ...
""" \\
  UIDT_joint_Delta_gamma_hexbin.jpg \\
  UIDT_histograms_Delta_gamma_Psi.jpg \\
  UIDT_gamma_vs_Psi_scatter.jpg
```

---

## 4. (Optional) Attach the 19 MB CSV

If you want the raw chain directly accessible from the Release
(in addition to Zenodo):

```bash
gh release upload v3.9-mc-plots \\
  simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv
```

> Note: Zenodo DOI [10.5281/zenodo.17554179](https://doi.org/10.5281/zenodo.17554179)
> provides a permanent reference. The GitHub Release Asset is a convenience mirror.

---

## 5. Verify

```bash
gh release view v3.9-mc-plots
# expected: 3 plot assets + optional CSV listed
```

---

## 6. Git LFS Fallback

If Release Assets are not suitable (e.g., private repo, CI download needed):

```bash
# one-time setup
git lfs install
echo '*.jpg filter=lfs diff=lfs merge=lfs -text' >> .gitattributes
echo '*.csv filter=lfs diff=lfs merge=lfs -text' >> .gitattributes
git add .gitattributes
git commit -m "chore: enable Git LFS for jpg and csv"
git lfs track simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv
git add simulation/monte_carlo/UIDT_MonteCarlo_samples_100k.csv
git commit -m "feat: track raw chain CSV via Git LFS"
git push origin main
```

Git LFS storage limit on GitHub Free: 1 GB. The 19 MB CSV fits comfortably.

---

## 7. Cross-references

| Document | Location |
|---|---|
| Plot axis specs + code | `simulation/monte_carlo/PLOTS_REGISTRY.md` |
| Zenodo archive page | https://doi.org/10.5281/zenodo.17554179 |
| MC verification test | `verification/tests/test_monte_carlo_summary.py` |
| MC evidence verifier | `verification/scripts/verify_monte_carlo_research_notes.py` |
| STRATUM II results | `simulation/monte_carlo/STRATUM_II_RESULTS.md` |
