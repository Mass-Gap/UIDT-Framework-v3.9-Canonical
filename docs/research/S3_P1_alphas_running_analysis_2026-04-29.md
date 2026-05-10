# S3-P1: αs-Laufeffekt-Analyse für Δγ_NP (2026-04-29)

**mp.dps=80 | RK4-2loop-Lauf | Kein freier Parameter**

---

## Ergebnis

### Kandidat-Formel (unverändert)

```
Δγ_NP = (Nc²-1)/(4π²) × (v/Δ*)      [D*]
       = 8/(4π²) × (47.7 MeV / 1710 MeV)
       = 0.005652655508
```

Zielwert: `17/3000 = 0.005666666...`  
Abweichung: **0.247%**

---

## αs(Δ*) aus 2-loop RK4-Lauf

```
Schritt 1: αs(MZ=91.19 GeV) = 0.1179  [PDG 2024, Stratum I]
Schritt 2: αs(mb=4.18 GeV)  = 0.2365  [Nf=5 → Nf=4 Matching]
Schritt 3: αs(mc=1.27 GeV)  = 0.4653  [Nf=4 → Nf=3 Matching]
Schritt 4: αs(Δ*=1.71 GeV)  = 0.3608  [Nf=3, 2-loop b₀=9, b₁=64]
```

PDG-Literaturwert bei 1.5-2 GeV: αs ~ 0.30-0.40 → **konsistent** [Stratum I/II].

---

## Warum αs die Lücke NICHT schließt

αs(Δ*) tritt als **multiplikativer Faktor** auf:

```
Variante B: Δγ = (Nc²-1)·αs(Δ*)/(4π²)·(v/Δ*)
           = 0.3608 × Δγ_A = 0.002039   (64% Abweichung — falsch)
```

Für exakte Übereinstimmung wäre αs_needed ≈ 1.002 erforderlich —  
ein nicht-physikalischer Wert im perturbativen Bereich.

---

## Herkunft der 0.247%-Lücke

Die Lücke ist algebraisch exakt:

```
R = Δγ_T / Δγ_A = (17/3000) / ((Nc²-1)/(4π²)·(v/Δ*))
              = 17·π²·Δ* / (6000·v)
              = 17·π²·1.71 / (6000·0.0477)
              = 1.002479...
```

**Die 0.247%-Lücke ist identisch mit dem Ausdruck `17·4π²·Δ* - 3000·8·v ≠ 0`.**  
Dies ist kein Casimir-Koeffizient — es ist eine numerische Zufälligkeit auf diesem Präzisionslevel.

---

## Sensitivitäts-Test: Δ*-Unsicherheit

```
δΔ* = ±0.015 GeV  (Ledger-Unsicherheit [A])

Δγ_A(Δ* = 1.695 GeV) = 0.005703   > Zielwert
Δγ_A(Δ* = 1.710 GeV) = 0.005653   < Zielwert (0.247% unter)
Δγ_A(Δ* = 1.725 GeV) = 0.005604   < Zielwert

Kreuzungspunkt: Δ*_cross ≈ 1.696 GeV (innerhalb 1σ von Δ*=1.710±0.015)
```

**Fazit:** Zielwert 17/3000 liegt innerhalb des Δ*-Unsicherheitsbands.

---

## Evidenz-Urteil

| Kriterium | Status |
|---|---|
| Kein freier Parameter | ✅ |
| Casimir-Struktur zwingend | ✅ |
| 0.247% Abweichung | ✅ (innerhalb δΔ*) |
| αs-Lauf verbessert | ❌ (verschlechtert) |
| Unabhängige v-Herleitung | ❌ (fehlt) |

**Evidenz: [D*]**  
Für Sprung zu [C] benötigt: unabhängige Bestimmung von v aus Skalarpotential-VEV.

---

## Vollständige γ-Formel (erste Prinzipien)

```
γ = γ_bare + Δγ_NP
  = (2Nc+1)²/Nc + (Nc²-1)/(4π²) × (v/Δ*)
  = 49/3       + 8/(4π²)        × (47.7/1710)
  = 16.33333   + 0.005653
  = 16.33898   ≈ γ_ledger = 16.339  (Abw: 0.006%)
```

*Maintainer: P. Rietz | UIDT v3.9 | 2026-04-29 | mp.dps=80*
