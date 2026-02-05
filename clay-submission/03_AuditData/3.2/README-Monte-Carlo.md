# ⚛️ UIDT $\Omega$ Monte Carlo Validation Data (v3.3)

**Author:** Philipp Rietz
**License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
**Canonical DOI (V3.2/V3.3):** [10.5281/zenodo.17554179](https://doi.org/10.5281/zenodo.17554179)
**Status:** [Validation Data (Technically Closed)](DOCS/STATUS_REPORT.md)

---

## 1. Overview

This repository contains the complete dataset from the final **Monte Carlo (MC) validation run** for the Unified Information-Density Theory (UIDT) $\Omega$ framework. This data serves as the non-perturbative statistical validation of the canonical parameters ($\mathbf{\Delta, \gamma, \kappa, m_S, \lambda_S}$) derived from the analytical 3-equation system.

The dataset includes the raw MC chain samples, high-precision mean values, parameter correlation matrices, and the final summary tables and plots used in the UIDT v3.3 publication.

### 🌟 Key Data Artifacts

* **Raw Data:** 100,000 high-thinning samples from the primary MC simulation (`UIDT_MonteCarlo_samples_100k.csv`).
* **High-Precision Means:** Final derived parameter values with high precision (`UIDT_HighPrecision_mean_values.csv`).
* **Correlation Analysis:** Full correlation matrix showing dependencies between parameters (`UIDT_MonteCarlo_correlation_matrix.csv`).
* **Plots:** Diagnostic plots including posterior distributions (corner plot) and parameter histograms.

---

## 2. File Manifest & Data Description

This section details the scientific purpose and content of each file in this data package.

### 2.1. Raw Simulation Data

| File | Description | Purpose & Context |
| :--- | :--- | :--- |
| **`UIDT_MonteCarlo_samples_100k.csv`** | Raw Monte Carlo Chain Data (100k samples). | **(Primary Artifact)** This file contains the thinned samples (100,000 steps) from the MC simulation. It serves as the "ground truth" for all subsequent analysis. The columns represent the canonical parameters (e.g., `m_S`, `kappa`, `lambda_S`, `Delta`, `gamma`). |
| **`UIDT_HighPrecision_mean_values.csv`** | High-Precision Parameter Means. | Contains the final, high-precision mean values (and standard deviations) for the canonical parameters, calculated by averaging the `100k_samples.csv` file. |

### 2.2. Summary Statistics & Tables

| File | Description | Purpose & Context |
| :--- | :--- | :--- |
| **`UIDT_MonteCarlo_summary.csv`** | Full Statistical Summary. | A comprehensive summary table including mean, median, 68% and 95% confidence intervals (CI), and standard deviation for all parameters. |
| **`UIDT_MonteCarlo_summary_table_short.csv`** | Abbreviated Summary. | A simplified version of the summary table, often used for quick reference or embedding in presentations. |
| **`UIDT_MonteCarlo_correlation_matrix.csv`** | Parameter Correlation Matrix. | A symmetric matrix showing the statistical correlation (Pearson r) between all parameters. Essential for understanding parameter degeneracies (e.g., the strong correlation between $\kappa$ and $\lambda_S$). |
| **`UIDT_MonteCarlo_summary_table.tex`** | LaTeX Publication Table. | The final, publication-ready LaTeX code for the summary table, formatted for direct inclusion in the UIDT v3.3 manuscript. |

### 2.3. Plots and Visualizations

| File | Description | Purpose & Context |
| :--- | :--- | :--- |
| **`image.png` (f45ac4e9...)** | (Assumed) Correlation Matrix Plot. | A heatmap visualization of the `correlation_matrix.csv` file. It graphically shows the strong positive correlation between $\kappa$ and $\lambda_S$ (confirming the $5\kappa^2 = 3\lambda_S$ RG-Fixpoint) and the anti-correlation between $m_S$ and $\Delta$. |
| **`image.png` (3413530b...)** | (Assumed) Posterior Distributions (Corner Plot). | **(Primary Plot)** This is the main diagnostic plot for the MC run. It shows the 1D marginalized histograms for each parameter (confirming Gaussianity/convergence) and the 2D contour plots showing the covariance between parameter pairs. |
| **`image.png` (e54d7ce0...)** | (Assumed) 1D Parameter Histograms. | A detailed view of the 1D marginalized posterior distributions (histograms) for the key parameters ($\Delta, \gamma, \kappa, m_S, \lambda_S$), allowing for a precise reading of the mean and confidence intervals. |

---

## 3. How to Use (Reproducibility)

To reproduce the analysis and plots from this dataset:

1.  **Load the Samples:**
    ```python
    import pandas as pd
    # Load the primary data source
    samples = pd.read_csv("UIDT_MonteCarlo_samples_100k.csv")
    ```

2.  **Verify High-Precision Means:**
    ```python
    # Calculate the mean for a parameter, e.g., 'gamma'
    mean_gamma = samples['gamma'].mean()
    std_gamma = samples['gamma'].std()
    print(f"Calculated gamma: {mean_gamma:.4f} +/- {std_gamma:.4f}")
    
    # Compare against the high-precision file
    hp_means = pd.read_csv("UIDT_HighPrecision_mean_values.csv", index_col=0)
    print(f"Stored mean: {hp_means.loc['gamma', 'mean']:.4f}")
    ```

3.  **Reproduce Plots:**
    * Use libraries like `matplotlib`, `seaborn`, or `corner` to regenerate the plots.
    * **Example (Corner Plot):**
        ```python
        import corner
        # Ensure 'corner' is installed: pip install corner
        fig = corner.corner(samples, labels=samples.columns, 
                            quantiles=[0.16, 0.5, 0.84], 
                            show_titles=True, title_fmt=".4f")
        fig.savefig("REPRODUCED_corner_plot.png")
        ```

---

## 4. License and Citation

This dataset is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

### How to Cite This Data

If you use this dataset in your research, please cite the canonical UIDT v3.2/v3.3 paper:

> **Rietz, P. (2025). *Unified Information-Density Theory (UIDT) v3.2: Canonical Formulation, Mathematical Consistency, and Empirical Testability*. Zenodo. https://doi.org/10.5281/zenodo.17554179**
