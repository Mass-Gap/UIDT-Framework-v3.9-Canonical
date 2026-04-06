## Summary

Enforce Python naming convention (L-FS-03): Rename `UIDTv3.6.1_HMC_Optimized.py` to `uidt_v3_6_1_hmc_optimized.py`. Dots in version numbers break Python imports and violate File System Law L-FS-03.

## Ticket Reference

**Ticket ID:** TKT-2026-04-06-001  
**Plan:** File Structure Optimization (o1)  
**Priority:** HIGH

## Changes

### File Operations
- ✅ Renamed `simulation/UIDTv3.6.1_HMC_Optimized.py` → `simulation/uidt_v3_6_1_hmc_optimized.py`

### Documentation Updates
- ✅ Updated `docs/data-availability.md`
- ✅ Updated `filesystem-tree.md`
- ✅ Updated `clay-submission/04_Certificates/SHA256_MANIFEST.txt`
- ✅ Updated `clay-submission/08_Documentation/DATA_AVAILABILITY.md`

## File System Laws Enforced

- **L-FS-03:** Python naming convention - `snake_case`, version numbers as `v3_6_1` (not `v3.6.1`)

## Affected Constants

**None** - This is a file organization change with no impact on physical constants or mathematical operations.

## Evidence Category

**None** - No scientific claims affected.

## Limitation Impact

**None** - No impact on known limitations (L1-L6).

## Verification

- [x] File successfully renamed
- [x] All documentation references updated
- [x] No imports broken (file is standalone simulation script)
- [x] `.gitignore` does not explicitly list moved path
- [ ] Verification suite run (not applicable - standalone script)

## Review Gates

- **A. Parameter Consistency:** N/A (no parameters changed)
- **B. Evidence Classification:** N/A (no scientific claims)
- **C. Language Quality:** ✅ Documentation updated in English
- **D. Numerical Precision:** N/A (no numerical changes)
- **E. Citation Integrity:** ✅ DOI preserved
- **F. UIDT-OS Compliance:** ✅ No UIDT-OS files modified
- **G. Strata Separation:** ✅ No core/ or modules/ touched

## Reproduction Note

This change does not affect reproducibility. The file is a standalone simulation script with no dependencies in the verification pipeline.

## DOI/arXiv Resolvability

**DOI:** 10.5281/zenodo.17835200 ✅ Resolvable

## Next Steps

This is ticket 1 of 23 in the File Structure Optimization Plan. After merge:
- Continue with TKT-002 through TKT-015 (remaining simulation file renames)
- Batch similar renames to reduce PR overhead

## Checklist

- [x] Branch created from updated `main`
- [x] File renamed using `smartRelocate`
- [x] Documentation references updated
- [x] Commit message follows Trae protocol
- [x] PR body includes all required sections
- [ ] Awaiting review approval (DO NOT self-merge)

---
**Maintainer:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Generated:** 2026-04-06
