# TKT-FRG-TACHYON S2-a: γ_emergent — Fix v2 + Methodischer Befund

**Branch:** `TKT-20260429-hp-csv-lambda-patch-s2a`  
**Date:** 2026-04-30  
**Evidence category:** [D] → kandidiert [C] wenn |Δγ| < δγ = 0.0047  

---

## Methodischer Befund aus dem S2-a Testlauf

**Ergebnis des ersten Laufs:** `k_crit: NOT REACHED`

**Ursache (diagnostiziert, kein physikalischer Befund):**

Der UV-Startwert `m2_0 = -(344 MeV)²` war bereits **tachyonisch** (< 0).
Die Detektionslogik prüft auf Übergang `m² > 0 → m² < 0`.
Ein bereits negatives m² erzeugt keinen detektierbaren Vorzeichenwechsel.

**Physikalisch korrekte Randbedingung:**

| Parameter | S2-a v1 (falsch) | S2-a v2 (korrigiert) | Begründung |
|:---|:---|:---|:---|
| m2_0 | −(344 MeV)² | **+(κ̃₀* · k_UV)²** | UV-Phase: Skalar massiv |
| κ̃₀* | — | 0.04877718 [D] aus S1 | S1-Bisection-Ergebnis |
| m_UV | — | **~83.4 MeV** | κ̃₀* · 1710 MeV |

**Herkunft von |m_S| ~ 344 MeV:** Das ist die IR-Vakuumskala aus SVZ-Gluon-Kondensat [B] —
nicht die UV-Startmasse. SVZ gibt den Wert des Kondensats bei k→0, nicht bei k = k_UV.

---

## S2-a v2 Parameter

| Parameter | Wert | Quelle |
|:---|:---|:---|
| N_steps | 10.000 | S2-a Anforderung |
| Toleranz |F| | 1e-14 | UIDT-Numerik-Standard |
| k_UV | 1710 MeV | LEDGER [A] |
| k_IR | 1 MeV | IR-Cutoff |
| α_s(k_UV) | 0.3 | perturbativ |
| m2_0 | +(83.4 MeV)² > 0 | S1 κ̃₀* [D] |
| λ_S | 5/12 exakt | LEDGER [A] |
| κ | 1/2 exakt | LEDGER [A] |
| mp.dps | 80 | UIDT-Standard |

---

## HP-CSV Patch (dieser Branch) — Status

`[RG_CONSTRAINT_FAIL]` aus PR #382: **GESCHLOSSEN**  
Residual 5·(1/2)² − 3·(5/12) = **0 exakt**

---

## Evidence-Upgrade-Pfad

```
S1:    N=4000,  tol=1e-5,  m2_0<0 (SVZ-IR) → γ_emergent=16.3296  |Δγ|=2×δγ  [D]
S2-a v1: m2_0<0 (bug)                       → k_crit NOT REACHED  [NULL]
S2-a v2: m2_0>0 (UV-massiv, fix)            → Ergebnis ausstehend
  → |Δγ| < 0.0047: [D] → [C] (Kandidat)
  → |Δγ| ≥ 0.0047: [TENSION ALERT] → S2-b (engere Bisection κ̃₀*)
```

---

## Reproduktion

```bash
git checkout TKT-20260429-hp-csv-lambda-patch-s2a
python verification/scripts/frg_tachyon_s2a.py
```

Laufzeit: ~5–15 Min (N_steps=10.000, mp.dps=80).

---

## Offene Flags

| Flag | Status |
|:---|:---|
| `[RG_CONSTRAINT_FAIL]` | ✅ GESCHLOSSEN |
| `[TENSION ALERT] γ_emergent` | ⏳ S2-a v2 ausstehend |
| `[TENSION ALERT] δγ NLO` | 🔴 offen (PR #358) |

---

*UIDT Framework v3.9 — Maintainer: P. Rietz*  
*UIDT ist ein aktives Forschungsframework, kein etabliertes Physik-Modell.*
