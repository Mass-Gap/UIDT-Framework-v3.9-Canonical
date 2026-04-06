# Security Policy

## Scope

This security policy applies to the **UIDT Framework v3.9 Canonical Repository** (`Mass-Gap/UIDT-Framework-v3.9-Canonical`). The scope is strictly limited to:

- **Vulnerability Disclosure:** Security issues in public code, scripts, or documentation
- **Data Integrity:** Issues affecting the integrity of verification results or canonical constants
- **Reproducibility:** Problems that prevent independent verification of claims

**Out of Scope:**
- Internal operating system (`UIDT-OS/`) - not publicly accessible
- Private development tools and workflows
- Theoretical physics disputes (use GitHub Issues with `[FALSIFICATION]` tag instead)

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 3.9.x   | :white_check_mark: |
| 3.7.x   | :x:                |
| 3.6.x   | :x:                |
| < 3.6   | :x:                |

## Reporting a Vulnerability

### For Security Vulnerabilities

If you discover a security vulnerability, please report it via:

**Email:** badbugs.arts@gmail.com  
**Subject:** `[SECURITY] UIDT Framework v3.9 - [Brief Description]`

**Please include:**
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact on verification results or data integrity
4. Suggested fix (if available)

**Response Time:**
- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 7 days
- **Fix Timeline:** Depends on severity (Critical: 14 days, High: 30 days, Medium: 60 days)

### For Data Integrity Issues

If you find discrepancies in:
- Canonical constants (`CANONICAL/CONSTANTS.md`)
- Claims registry (`LEDGER/CLAIMS.json`)
- Verification results (`verification/data/`)

Please open a **public GitHub Issue** with the tag `[DATA-INTEGRITY]` and include:
1. Expected value (with evidence category)
2. Actual value found
3. Residual calculation
4. Potential falsification risk (L1-L6)

### For Reproducibility Issues

If you cannot reproduce verification results:
1. Check `clay-submission/REPRODUCE.md` for one-command reproduction
2. Verify `mpmath.dps = 80` is set in your environment
3. Open a GitHub Issue with tag `[REPRODUCIBILITY]` including:
   - Your environment (OS, Python version, mpmath version)
   - Command executed
   - Expected vs. actual output
   - Error messages or logs

## Disclosure Policy

We follow **Coordinated Vulnerability Disclosure**:

1. **Private Disclosure:** Report sent to maintainer
2. **Acknowledgment:** Maintainer confirms receipt within 48 hours
3. **Investigation:** Maintainer investigates and develops fix
4. **Fix Development:** Patch created and tested
5. **Public Disclosure:** After fix is deployed, vulnerability is disclosed publicly with credit to reporter

**Embargo Period:** 90 days maximum (or until fix is deployed, whichever comes first)

## Security Best Practices for Contributors

When contributing to UIDT Framework:

1. **Never commit secrets:** No API keys, passwords, or private keys
2. **Validate inputs:** All user inputs in scripts must be validated
3. **Use mpmath for precision:** Never use Python `float` for Category A claims
4. **Document assumptions:** All mathematical assumptions must be explicit
5. **Test edge cases:** Especially for numerical stability near boundaries

## Known Limitations (Not Security Issues)

The following are **known limitations** documented in `CANONICAL/LIMITATIONS.md` and are NOT security vulnerabilities:

- **L1:** 10¹⁰ geometric factor (unexplained)
- **L2:** Electron mass 23% residual
- **L3:** Vacuum energy factor 2.3 residual
- **L4:** γ = 16.339 not RG-derived [A-]
- **L5:** N = 99 RG steps empirically chosen
- **L6:** Glueball f₀(1710) retracted [E]

## Falsification Criteria

If you believe you have found evidence that **falsifies** the UIDT framework, please:

1. Open a GitHub Issue with tag `[FALSIFICATION]`
2. Provide mathematical proof or experimental data
3. Reference specific claims from `LEDGER/CLAIMS.json`
4. Calculate residuals using 80-digit precision

See `docs/governance/falsification-criteria.md` for thresholds.

## Contact

**Maintainer:** Philipp Rietz  
**Email:** badbugs.arts@gmail.com  
**ORCID:** 0009-0007-4307-1609  
**DOI:** 10.5281/zenodo.17835200

## Acknowledgments

We thank all security researchers who responsibly disclose vulnerabilities. Contributors will be credited in:
- `CHANGELOG.md`
- GitHub Security Advisories
- Zenodo release notes

---
**Last Updated:** 2026-04-07  
**Policy Version:** 1.0
