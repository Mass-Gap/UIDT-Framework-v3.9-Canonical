# Claims-Tabelle S4-P1 v2 (Vollherleitung)

**Datum:** 2026-04-29  
**Branch:** TKT-20260429-S4P1-tachyon-threshold-frg  
**Verifikation:** `python verification/scripts/verify_s4p1_onset_attractor.py`

## Claims

| ID | Behauptung | Evidenz | Reproduktion |
|---|---|---|---|
| C-S4P1-01 | κ̃₀^attr = −0.01030923381 (universeller IR-Attractor) | [D] | verify_attractor() |
| C-S4P1-02 | Onset ist IR-Attractor, nicht durch κ̃₀ allein steuerbar | [D] | ODE-Analyse im Dokument |
| C-S4P1-03 | k_crit = E_T·4π = 30.662 MeV, δ < 0.13 MeV vs. Bisection | [D*] | verify_casimir_consistency() |
| C-S4P1-04 | Regulator-Unabhängigkeit: |ratio−1| < 1e-5 bei ω_A≈3080 | [D] | verify_regulator_independence() |
| C-S4P1-05 | LO α_s=const führt zu k_crit(LO)=1196 MeV → physikalisch falsch | [D] | Kommentar im Verifikationsscript |

## Evidenz-Upgrade-Pfad

- [D*] → [C]: Erfordert S4-P2 (formale NLO-Herleitung) ODER Lattice-Bestätigung
- Offene Fragen: nichtlineare Flow-Terme, nicht-perturbatives α_s im IR

## Betroffene Ledger-Parameter

| Parameter | Wert | Evidenz | Berührt? |
|---|---|---|---|
| Δ* | 1.710 GeV | [A] | Nein (Input) |
| E_T | 2.44 MeV | [C] | Ja (k_crit-Skala) |
| γ | 16.339 | [A-] | Ja (γ = Δ*/k_IR) |
| v | 47.7 MeV | [A] | Nein |
