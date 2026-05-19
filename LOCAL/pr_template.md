[UIDT-v3.9] LOCAL/scripts/arxiv_scan.py: Literature & Falsification Radar
### Objective
Implemented `LOCAL/scripts/arxiv_scan.py` to continuously monitor ArXiv for new publications concerning the Lattice QCD glueball spectrum, DESI dark energy equation of state, and Casimir effect anomaly precision measurements. The script parses XML data and matches results against Falsification Triggers from `CANONICAL/FALSIFICATION.md`. If a trigger is hit (e.g. DESI $w = -1.00 \pm 0.01$), an Emergency Epistemic Report is generated for Opus 4.7 evaluation. Execution leaves standard traces in `LOCAL/logs/traceability.json`.

### Evidence Status & Claims
- Affected Constants: N/A
- Evidence Category: N/A
- Residual Check: N/A

Author: P. Rietz
Mode: OUTPUT-MODE
