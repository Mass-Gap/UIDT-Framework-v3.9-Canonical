# TKT-FRG-TACHYON S2-a: γ_emergent — Upgrade-Run

**Branch:** `TKT-20260429-hp-csv-lambda-patch-s2a`  
**Date:** 2026-04-29  
**Evidence category:** [D] → candidate [C] if |Δγ| < δγ = 0.0047  

---

## Motivation

S1 (N_steps=4000, tol=1e-5) lieferte γ_emergent = 16.3296, |Δγ| = 0.0094 ≈ 2×δγ.  
Wurde als numerische Auflösungsgrenze identifiziert, nicht als physikalische Abweichung.  
S2-a erhöht auf N_steps=10.000, Toleranz 1e-14, kappa/lambda_S als exakte Ledger-Werte.

---

## HP-CSV Patch (dieser Branch)

| Spalte | Wert | Evidence | Begründung |
|:---|:---|:---|:---|
| `lambda_S_exact` | 5/12 = 0.4166̄ (80 Stellen) | [A] | Aus 5κ²=3λ_S mit κ=1/2, residual=0 |
| `kappa_mean` | 0.5 (bereits vorhanden) | [A] | exakt 1/2 |

RG-Constraint nach Patch: `5·(1/2)² = 3·(5/12)` → residual = 0 exakt.  
`[RG_CONSTRAINT_FAIL]` in PR #382 damit **GESCHLOSSEN**.

---

## S2-a Parameter

| Parameter | Wert | Quelle |
|:---|:---|:---|
| N_steps | 10.000 | S2-a Anforderung |
| Toleranz |F| | 1e-14 | UIDT-Numerik-Standard |
| k_UV | 1710 MeV (= Δ*) | LEDGER [A] |
| k_IR | 1 MeV | IR-Cutoff |
| α_s(k_UV) | 0.3 | perturbativ |
| m²_S(Λ) | −(344 MeV)² | SVZ-Motivation [B], S1-Konsistenz |
| κ | 1/2 exakt | LEDGER [A] |
| λ_S | 5/12 exakt | LEDGER [A] |
| mp.dps | 80 | UIDT-Standard |

---

## Evidence-Upgrade-Pfad

```
S1: N=4000,  tol=1e-5  → γ_emergent=16.3296  |Δγ|=0.0094=2×δγ  [D]
S2-a: N=10000, tol=1e-14 → Ergebnis ausstehend
  → wenn |Δγ| < 0.0047: [D] → [C] (Kandidat)
  → wenn |Δγ| ≥ 0.0047: [TENSION ALERT] bleibt, S2-b geplant
```

---

## Reproduktion

```bash
python verification/scripts/frg_tachyon_s2a.py
```

Erwartete Ausgabe:
```
[RG_CONSTRAINT: PASS] residual = 0.0
[S2-a] FRG-Tachyon flow N_steps=10000, tol=1e-14
...
[S2-a RESULTS]
  k_crit         = ... MeV
  gamma_emergent = ...  [D]
  |Δγ|           = ...
```

---

## Offene Flags nach diesem Branch

| Flag | Status |
|:---|:---|
| `[RG_CONSTRAINT_FAIL]` | ✅ GESCHLOSSEN (λ_S in HP-CSV, residual=0) |
| `[TENSION ALERT] γ_emergent` | ⏳ abhängig von S2-a Laufzeit |
| `[TENSION ALERT] δγ NLO` | 🔴 offen (PR #358, TKT-20260403-FRG-NLO) |

---

*UIDT Framework v3.9 — Maintainer: P. Rietz*  
*UIDT ist ein aktives Forschungsframework, kein etabliertes Physik-Modell.*
