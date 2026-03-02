# UIDT Data Registry

This directory contains the public-facing, immutable reference data for the UIDT Framework.
Structure follows the standard **Canonical Data Architecture**.

## Structure

- **`canonical/`**  
  Contains the mathematical and physical constants, evidence categories, and core parameters.  
  👉 [CONSTANTS.md](canonical/CONSTANTS.md)

- **`ledger/`**  
  Contains the `CLAIMS.json` single-source-of-truth database for all scientific claims, their verification status, and evidence grades [A-E].  
  👉 [CLAIMS.json](ledger/CLAIMS.json)

## Usage

These files are the **Public API** for UIDT constants.
Verification scripts and documentation should reference these paths.

*Note: Internal UIDT-OS agents may maintain a synchronized copy in `UIDT-OS/` for operational autonomy, but `data/` is the authoritative source for consumers.*
