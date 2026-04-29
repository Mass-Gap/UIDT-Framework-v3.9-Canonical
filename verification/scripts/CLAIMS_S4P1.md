# S4-P1 Claims — Tachyonischer Übergang YM+Scalar FRG

## Claims Table

| ID | Claim | Formel | Evidenz | Quelle |
|----|-------|--------|---------|--------|
| C-S4P1-01 | FRG-VEV-Relation | v = sqrt(12/5) * k_crit | [D] | Session-2 Analyse |
| C-S4P1-02 | k_crit Kandidat | k_crit = E_T * 4π (0.42% Abw.) | [D*] | S4-P1 Herleitung |
| C-S4P1-03 | Konsistenz mit δE_T | Abweichung < δk(E_T) | [D*] | verify_s4p1_tachyon_threshold.py |
| C-S4P1-04 | v-Vorhersage | v = E_T * 4π * sqrt(12/5) = 47.50 MeV | [D*] | Kette aus C-S4P1-01,02 |
| C-S4P1-05 | γ-Kette geschlossen | γ_pred = 16.33896 (0.00023% Abw.) | [D*] | Vollständige Kette |

## Reproduction

```bash
cd verification/scripts
python verify_s4p1_tachyon_threshold.py
```

Erwartet: Alle [OK]-Checks bestehen, Abweichungen innerhalb E_T-Unsicherheit.

## Offene Punkte

- [ ] S4-P1a: FRG-Simulation mit k_IR = E_T
- [ ] S4-P1b: Analytischer Onset-Beweis via Wetterich-Trace
- [ ] S4-P1c: Regulator-Unabhängigkeitscheck (Litim vs. smooth)
- [ ] S4-P1d: Formaler Evidenz-Upgrade [D*] → [C] nach S4-P1a

## Affected Ledger Constants

| Konstante | Wert | Evidenz | Änderung |
|-----------|------|---------|----------|
| v | 47.7 MeV | [A] | KEINE |
| E_T | 2.44 MeV | [C] | KEINE |
| γ | 16.339 | [A-] | KEINE |
