import re

FILE_PATH = 'CANONICAL/LIMITATIONS.md'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# I will just write a new file segment using string replacement since I have the full lines

new_active = """### L7: Gribov Horizon Crossing
**Status:** 🔬 ACTIVE RESEARCH [GRIBOV_HORIZON_CROSSING]

**Description:**  
Der analytische Fixpunkt des projizierten 2x2-Systems erzwingt \\(\\tilde{\\kappa}^{2*} = \\pi^2 \\approx 9.87\\). Dieser Wert liegt tief im Infraroten, jenseits des klassischen Gribov-Pols (\\(\\tilde{\\kappa}^2 = 1.0\\)). Der Vorhersagewert f\u00fcr \\(\\tilde{\\lambda}_{SF}^* \\approx 16.449\\) ist streng auf Evidenz D limitiert, bis das System um einen dynamischen, selbstkonsistenten Gribov-Zwanziger-Limes erweitert wird.

---

### L8: X³ Mixing Omitted
**Status:** 🔬 ACTIVE RESEARCH [X3_MIXING_OMITTED]

**Description:**  
Die R\u00fcckkopplung des Tripel-Gluon-Operators (X\u00b3-Einmischung) aus dem SMEFT-Sektor (\\(+ \\frac{1}{2} g_3^2 C_A C_G\\)) wurde in der aktuellen Truncation vernachl\u00e4ssigt.

---

### L9: Z₂ Symmetry Collapse
**Status:** 🔬 ACTIVE RESEARCH [Z2_SYMMETRY_COLLAPSE]

**Description:**  
Das minimale Skalar-Gauge-System kollabiert ohne explizite Symmetriebrechung deterministisch. Die Theorie st\u00fctzt sich axiomatisch darauf, dass \\(S\\) an die Spuranomalie (Trace Anomaly) koppelt, um diesen Kollaps abzuwenden (siehe UIDT-C-072).

---
"""

new_resolved = """### L6-FRG: Truncation Artifact - Spiral RG Flow [RESOLVED]
**Status:** ✅ CLOSED (v3.9.6)

**Previous Issue:**  
Spiralf\u00f6rmiger RG-Fluss im Infraroten durch fehlende Symmetrie-Relationen z.B. komplexe Eigenwerte an Fixpunkten.

**Resolution:**  
Das Artefakt wurde durch exakte RG-Constraint-Projektion (\\(5\\kappa^2 = 3\\lambda_{SF}\\)) im 80-dps-Solver eliminiert. Die Stabilit\u00e4tsmatrix ist nun beweisbar rein reell.

---
"""

# Find L6-FRG and remove it from Active Limitations
match = re.search(r'(### L6-FRG: FRG Derivation of γ.*?---\n)', content, re.DOTALL)
if match:
    content = content.replace(match.group(1), new_active)

# Find Historical Limitations header to append new resolved
hist_header = '## Resolved Limitations (Historical)\n'
content = content.replace(hist_header, hist_header + '\n' + new_resolved)

# Update matrix
old_matrix_row = '| L6-FRG  | FRG minimal truncation (C-070)       | η_* Evidence D, not upgradable| 🔴 High     |'
new_rows = """| L7      | Gribov Horizon Crossing              | λ_SF* strictly Evidence D     | 🔴 High     |
| L8      | X³ Mixing Omitted                    | Impacts truncation stability  | 🟡 Medium   |
| L9      | Z₂ Symmetry Collapse                 | Axiomatic Trace Anomaly req.  | 🔴 High     |"""

content = content.replace(old_matrix_row, new_rows)

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated {FILE_PATH}.")
