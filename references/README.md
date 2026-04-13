# References Directory

Bibliographic references and citation management for the UIDT Framework.

## Contents

- **REFERENCES.bib:** Master BibTeX file with all cited works
- **citation_guide.md:** How to cite UIDT in your publications
- **external_data.md:** External data sources (DESI, FLAG, lattice QCD)

## Citation Format

### UIDT Framework (General)
```bibtex
@misc{rietz2026uidt,
  author = {Rietz, P.},
  title = {Vacuum Information Density as the Fundamental Geometric Scalar},
  year = {2026},
  doi = {10.5281/zenodo.17835200},
  url = {https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical},
  note = {UIDT Framework v3.9}
}
```

### Specific Version
```bibtex
@software{rietz2026uidt_v395,
  author = {Rietz, P.},
  title = {UIDT Framework v3.9.5},
  year = {2026},
  month = {April},
  doi = {10.5281/zenodo.17835200},
  version = {3.9.5},
  url = {https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/releases/tag/v3.9.5}
}
```

### Specific Claim
```bibtex
@misc{rietz2026uidt_massgap,
  author = {Rietz, P.},
  title = {Yang-Mills Mass Gap from Vacuum Information Density},
  year = {2026},
  doi = {10.5281/zenodo.17835200},
  note = {UIDT-C-001: Mass Gap $\Delta = 1.710 \pm 0.015$ GeV [A]}
}
```

## External Data Sources

### Cosmology
- **DESI DR2:** Dark Energy Spectroscopic Instrument Data Release 2
  - H₀ = 70.4 ± 0.16 km/s/Mpc
  - w₀ = -0.99 ± 0.05
  - Citation: DESI Collaboration (2024)

### Lattice QCD
- **FLAG 2024:** Flavour Lattice Averaging Group
  - Quark masses, decay constants, form factors
  - Citation: Aoki et al. (2024)

- **Morningstar et al. (2024):** Glueball spectrum
  - Δ_lattice = 1.710 ± 0.040 GeV
  - Citation: Morningstar, C., et al. (2024)

### Particle Physics
- **PDG 2024:** Particle Data Group
  - Fundamental constants, particle properties
  - Citation: Workman et al. (2024)

## Citation Guidelines

### When to Cite UIDT
- Using UIDT parameters (Δ, γ, κ, λ_S, v)
- Comparing with UIDT predictions
- Building on UIDT formalism
- Replicating UIDT calculations

### How to Cite
1. **General Framework:** Cite main DOI (10.5281/zenodo.17835200)
2. **Specific Version:** Cite version tag (e.g., v3.9.5)
3. **Specific Claim:** Cite claim ID (e.g., UIDT-C-001)
4. **Code:** Cite GitHub repository + commit hash

### Attribution Requirements
- **Code (MIT License):** Attribution optional but appreciated
- **Documentation (CC BY 4.0):** Attribution REQUIRED
- **Data (CC0):** Attribution optional (public domain)

## BibTeX Management

### Adding New References
1. Add entry to `REFERENCES.bib`
2. Use consistent citation keys: `author_year_keyword`
3. Include DOI when available
4. Verify entry with `bibtex` or `biber`

### Citation Key Format
```
lastname_year_keyword
```

Examples:
- `rietz_2026_uidt` (general framework)
- `morningstar_2024_glueball` (lattice QCD)
- `desi_2024_dr2` (cosmology data)

### Required Fields
- **@article:** author, title, journal, year, volume, pages, doi
- **@misc:** author, title, year, doi, url
- **@software:** author, title, year, version, doi, url

## External Data Availability

### Open Access
- ✅ DESI DR2: Public (https://data.desi.lbl.gov/)
- ✅ FLAG 2024: Public (https://flag.unibe.ch/)
- ✅ PDG 2024: Public (https://pdg.lbl.gov/)
- ✅ UIDT Code: Public (GitHub)
- ✅ UIDT Data: Public (Zenodo)

### Restricted Access
- ❌ None (all data sources are open access)

## Citation Metrics

### UIDT Framework
- **Citations:** (to be tracked via Google Scholar, INSPIRE-HEP)
- **Downloads:** (tracked via Zenodo, GitHub)
- **Forks:** (tracked via GitHub)
- **Stars:** (tracked via GitHub)

### Target Metrics (2026-2027)
- >100 citations within 2 years
- >1000 downloads from Zenodo
- >50 GitHub stars
- >10 independent replications

## Related Files

- `REFERENCES.bib` - Master BibTeX file
- `docs/metadata.yaml` - Dublin Core metadata
- `clay-submission/metadata.yaml` - Clay Math metadata
- `CANONICAL/CONSTANTS.md` - Parameter definitions with citations

---

**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**DOI:** 10.5281/zenodo.17835200  
**Last Updated:** 2026-04-07
