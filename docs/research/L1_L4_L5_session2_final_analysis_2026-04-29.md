# L1/L4/L5 Session-2: Finale Strukturanalyse (2026-04-29)

**mp.dps=80 | Verifikationsscript: 6/6 PASS**

---

## Kritische Strukturanalyse: Die γ-Triade

### Drei Punkte auf der γ-Achse

| Symbol | Wert | Bedeutung | Evidenz |
|---|---|---|---|
| γ_bare | 49/3 = 16.33333... | Casimir-Kombination (2Nc+1)²/Nc | [D] |
| γ_ledger | 16.339 = 49017/3000 | Phänomenologischer Parameter | [A−] |
| γ_inf | 16.3437 | IR-Grenzwert des Flows | [A−] |

### Geometrie

```
γ_bare = 49/3 = 16.3333...
          |
          | d₁ = 17/3000 = 0.005667 = 1.206·δγ
          |
γ_ledger = 16.339
          |
          | d₂ = 0.0047 = δγ (exakt, per Definition)
          |
γ_inf    = 16.3437

Gesamtabstand: γ_inf - γ_bare = 17/3000 + δγ = 0.01037 = 2.206·δγ
```

### Algebraische Fakten

- `gcd(49017, 3000) = 3`, also: **γ_ledger = 16339/1000** (vollständig gekürzt)
- **16339 ist prim** → keine Faktorisierung in Casimir-Terme möglich
- `γ_inf - γ_ledger = 0.0047 = δγ` exakt → γ_inf = γ_led + δγ (per Ledger-Definition)

**Konsequenz:** γ_ledger ist ein phänomenologischer Dezimalwert. Die Differenz  
`17/3000` zum algebraisch exakten `γ_bare = 49/3` hat **keinen Casimir-Ursprung**.

---

## P1: 2-loop Fixpunkt-Analyse

### 1-loop Fixpunkt
```
β_γ^(1) = (g²/16π²) × (c₁·γ + c₂)
c₁ = CA/Nc = 1,  c₂ = -(2Nc+1)²/Nc = -49/3
γ* = -c₂/c₁ = 49/3   ← tautologisch identisch mit γ_bare
```

### 2-loop Fixpunkt-Verschiebung
```
δγ = g²/(16π²) × (d₁·γ_bare + d₂)/c₁
d₁ = CA·b₀ = 33 (Standard)

Für d₂=0:         δγ = 12.87  (2271× zu groß)
Für d₂=CA²=9:    δγ = 13.08  (2309× zu groß)
Für d₂=-b₁/5.28: δγ = 0.0057  (← Zielwert, aber d₂=-538.8)
```

Kein Standard-Casimir-Koeffizient als d₂ reproduziert δγ = 0.00567.
**Benötigt: d₂ = -538.8** (= -5.28·b₁ = kein physikalischer Wert).

### Schlussfolgerung P1

γ_bare = 49/3 ist algebraisch begründet, aber die Verschiebung
γ_ledger - γ_bare = 17/3000 ist **nicht-perturbativen Ursprungs** [NP].

**Kandidatenerklärung:**
```
Δγ_NP = <G²>_vac × f(ET, v, Δ*) / Δ*⁴
```
wobei f() aus dem UIDT-Vakuumkondensatsektor stammt.
Dieser Ansatz ist offen und erfordert Session 3.

---

## P2: LPA Wetterinck-Flow

### Quenched (Session 2a): Kein Nulldurchgang
- m² bleibt monoton negativ
- Gluon-Loop dominiert und verstärkt tachyonischen Bereich

### Unquenched + laufendes g²(k) (Session 2b): Numerisch instabil
- m² divergiert bei t ≈ -0.56 (Nenner k²+m² → 0)
- IR-Freeze bei g²(k_freeze) stabilisiert nicht ausreichend
- Parameterscan: kein stabiler Nulldurchgang für physikalische Startwerte

### Benötigte Verbesserungen für Session 3
1. **Regulierter Propagator:** Litim-Regulator direkt im Nenner: `k² + m² + R_k(q²)`
2. **Stiff-ODE-Solver:** Adaptive Schrittweite (Runge-Kutta 4/5)
3. **IR-Konfinement-Eingabe:** g²(k) mit Gribov-Zwanziger-IR-Verhalten

---

## P3: ΣT Ergebnis

| Methode | ΣT |
|---|---|
| Dimensionsanalyse (Sess. 1) | 0.949 keV |
| Geometrisch via χ_top (Sess. 2) | 0.300 keV |

**Konsistent: ΣT ~ sub-keV.** Auf Δ*-Skala (GeV) physikalisch vernachlässigbar.
L5 qualitativ [D] stabil.

---

## P4: Gitter-Neuformulierung

**Bisheriger Vergleich (m_g aus Gluon-Propagator) ist kategorial falsch.**

Korrekte P4-Formulierung für Session 3:
- Suche Gitter-Messungen des **adjungierten Skalar-Propagators** in SU(3)
- Alternativ: MCRG-Flow-Analyse (Monte-Carlo RG)
- Alternativ: Willson-Loop-Skalierung mit Skalar-Kopplung

---

## Gesamtstatus

| Aufgabe | Status | Evidenz | Session-3-Task |
|---|---|---|---|
| L1: γ_bare=49/3 | ✅ Casimir-exakt | [D] | Bestätigung durch Gitter |
| L1: Δγ_1loop | ❌ 34-540× zu groß | [D] | NP-Kondensatbeitrag |
| L4: μ_UV=559 MeV | ✅ SVZ-kompatibel | [D/B] | Wetterinck mit Ad.-Schr. |
| L4: LPA-Konvergenz | ❌ Numerisch instabil | [D] | Stiff-ODE + Litim korrekt |
| L5: ΣT | ✅ sub-keV konsistent | [D] | Lagrangian-Herleitung |
| RG: 5κ²=3λS | ✅ Residual=0.0 | **[A]** | — |

---

## Session-3 Roadmap

```
[S3-P1] NP-Kondensatbeitrag Δγ_NP
        Ansatz: Δγ = <G²>_vac × (v/Δ*)^2 × c
        Prüfe ob c ein Casimir-Wert ist
        Erwartung: Δγ ≈ 0.006 für c ~ CA

[S3-P2] Adaptiver LPA-Solver (RK45)
        Stiff-ODE mit Litim-Regulator exakt
        Ziel: γ_emerg aus Nulldurchgang

[S3-P3] ΣT aus Pfadintegral
        VEV des topol. Operators exakt berechnen

[S3-P4] Gitter-Literatur: adjungierter Skalar
        Suche nach FRG-Gitter-QCD Studien
```

---

*Maintainer: P. Rietz | UIDT Framework v3.9 | 2026-04-29 | mp.dps=80*
