# UIDT-Framework v3.9 — Canonical Filesystem Tree

> **Last updated:** 2026-03-12 (v3.9 canonical state, post PR #180–183)
> **Moved from root to docs/:** 2026-04-18 (TKT-20260418)
> **Status:** Authoritative reference for repository structure.
> Agents must not create directories outside this tree without explicit approval.

---

## Root Directory Structure

```
UIDT-Framework-v3.9-Canonical/
├── .editorconfig                     # Editor configuration
├── .gitattributes                    # Git attributes
├── .gitignore                        # Git ignore rules
├── CHANGELOG.md                      # Project change history
├── CITATION.cff                      # Citation information
├── CONTRIBUTING.md                   # Contribution guidelines
├── FORMALISM.md                      # Core equation reference (public)
├── GLOSSARY.md                       # Project glossary
├── LICENSE.md                        # License information
├── metadata.xml                      # Project metadata (Zenodo/OSF)
├── README.md                         # Project README
├── SECURITY.md                       # Public security & disclosure policy
├── .github/                          # GitHub Actions, templates
├── CANONICAL/                        # Canonical constants and evidence system
├── clay-submission/                  # Clay Mathematics Institute submission
├── core/                             # Core UIDT proof engine (protected)
├── docs/                             # Project documentation
├── figures/                          # Visual figures
├── LEDGER/                           # Claims, changelog, traceability
├── LOCAL/                            # Local runtime artifacts (logs, scripts, DB)
├── manuscript/                       # Main theoretical manuscript
├── metadata/                         # Zenodo/OSF/CodeMeta metadata files
├── modules/                          # Physical modules (protected)
├── references/                       # BibTeX references
├── simulation/                       # HMC/Lattice simulation code
└── verification/                     # Verification and validation system
```

> **Note:** `filesystem-tree.md`, `issue184.txt`, and `best_practices.md` were removed from root
> and moved to `docs/` or `docs/archival-notes/` per PR chore/root-cleanup-2-TKT-20260418.
> Architecture rule: no documentation or `.txt` files at repository root.

### Removed (obsolete — do NOT recreate)

| Directory | Reason | Canonical replacement |
|-----------|--------|-----------------------|
| `Supplementary_Results/` | Non-canonical root placement | `verification/results/` |
| `Supporting_Documents/` | Non-canonical root placement | `docs/` |
| `UIDT-OS/` | Replaced by `CANONICAL/` + `LEDGER/` + `LOCAL/` | see below |
| `data/` | Non-canonical root placement | `verification/data/` |
| `arxiv_scan.py` (root) | Scripts do not belong at root | `LOCAL/scripts/` |
| `filesystem-tree.md` (root) | Documentation belongs in `docs/` | `docs/filesystem-tree.md` |
| `best_practices.md` (root) | Documentation belongs in `docs/` | `docs/best_practices.md` |
| `issue184.txt` (root) | `.txt` files do not belong at root | `docs/archival-notes/issue184_attribution_baddewithana.md` |

---

## 1. CANONICAL/

Immutable canonical parameters, evidence system, and known limitations.
Modification requires dual approval + `LEDGER/CHANGELOG.md` entry.

```
CANONICAL/
├── CONSTANTS.md
├── EVIDENCE.md
├── EVIDENCE_SYSTEM.md
├── FALSIFICATION.md
└── LIMITATIONS.md
```

---

## 2. LEDGER/

Append-only claims database, changelog, and traceability map.

```
LEDGER/
├── CHANGELOG.md
├── CLAIMS.json
├── claims.schema.json
├── FALSIFICATION.md
└── tickets_new.json
```

---

## Architecture Rules (enforced)

- **No `tests/` at root** — always `verification/tests/`
- **No scripts at root** — always `LOCAL/scripts/` or `verification/scripts/`
- **No `tmp/`, `temp/`, `scratch/`** in public repo
- **No `Supplementary_*/`, `Supporting_*/`** at root
- **No `.txt` raw files at root** — move to `docs/archival-notes/`
- **No documentation markdown at root** except `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `FORMALISM.md`, `GLOSSARY.md`, `SECURITY.md`, `LICENSE.md`
- **`CANONICAL/`** is immutable — dual approval required for any change
- **`LEDGER/CLAIMS.json`** is append-only
- **`core/` and `modules/`** are protected — mass deletion (>10 lines) requires explicit confirmation

---

*Last structural update: 2026-04-18 (TKT-20260418 — root cleanup)*
