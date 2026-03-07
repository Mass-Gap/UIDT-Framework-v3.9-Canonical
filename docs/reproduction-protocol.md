# UIDT v3.9 Reproduction Protocol

## Execution Modes

### Core Baseline (Recommended for audits)
```bash
python verification/scripts/UIDT_Core_Baseline.py
```
- **Scope:** Category A mathematical core only
- **Exit 0:** All core claims verified (residuals < 1e-14, L < 1)
- **Exit 1:** Core verification failed

### Full Master Runner
```bash
python verification/scripts/UIDT_Master_Verification.py
```
- **Scope:** All pillars (Core + Cosmology + Laboratory + Photonics)
- **Soft fails:** Non-critical modules (C/D) may be skipped without halting execution
- **Exit 0:** Core passed; peripherals may have warnings (yellow output)
- **Exit 1:** Core failure or critical system error

## Canonical Parameters
The following values are immutable for verification purposes:
- Mass Gap: Δ = 1.710 ± 0.015 GeV [A]
- Gamma: γ = 16.339 [A-]
- VEV: v = 47.7 MeV [A]
- Torsion Energy: E_T = 2.44 MeV [D]

## Directory Structure
- `core/`: Mathematical logic (Banach, RG) - **Do not modify**
- `modules/`: Physical extensions (CSF, Topology)
- `verification/scripts/`: Execution runners
- `verification/tests/`: Native precision tests

## Troubleshooting
If `UIDT_Master_Verification.py` reports warnings for Pillar II/IV:
1. Run `UIDT_Core_Baseline.py` first. If it passes, the core theory is intact.
2. Check `requirements.txt` for missing dependencies.
3. Verify that `modules/` are in the PYTHONPATH.
