## PR Template: [UIDT-v3.9] BETA-W7: Glueball-Spectrum vs LHC Run 3 / LHCb Update

### Task Reference
- Task ID: BETA-W7
- Branch: research/TKT-20260428-GLUEBALL-LHC3
- Ticket: TKT-20260428-GLUEBALL-LHC3

### Claims Table
| Claim ID | Claim | Evidence Category | Source (DOI/arXiv) |
|----------|-------|-------------------|-------------------|
| CL-01 | $X(2370)$ mass $\approx 2.370 \text{ GeV}$ | [I] | arXiv:2503.13286 |
| CL-02 | $f_0(2100)$ mass $\approx 2.100 \text{ GeV}$ | [I] | EPJ Web of Conferences |
| CL-03 | UIDT $m_G$ prediction $\approx 3.420 \text{ GeV}$ | [D] | UIDT Framework v3.9 |

### Affected Constants
| Constant | Previous Value | New Value | Evidence Change |
|----------|---------------|-----------|----------------|
| $\Delta^*$ | 1.710 [A] | unchanged | — |
| γ | 16.339 [A-] | unchanged | — |

### Reproduction Note
One-command verification:
`python verification/scripts/verify_GLUEBALL-LHC3.py`
Expected output: tension differences calculated.

### DOI/arXiv Verification
- [X] All cited papers have verified DOI or arXiv ID
- [X] No [AUDIT_FAIL] papers cited

### Pre-flight Checklist
- [X] No float() introduced
- [X] mp.dps = 80 local in all functions
- [X] RG constraint maintained
- [X] No deletion > 10 lines in /core or /modules
- [X] Ledger constants unchanged
- [X] λ_S = 5/12 (exact, not 0.417)

### Stratum Declaration
- Stratum I content: Experimental data for $X(2370)$ and $f_0(2100)$.
- Stratum II content: Lattice QCD glueball predictions.
- Stratum III content: UIDT predictions and comparison ($m_G \sim 2\Delta^*$).
