# TKT-FRG-CONFINEMENT: Gribov-Zwanziger Randbedingungen im FRG-Flow

**Ticket:** TKT-FRG-CONFINEMENT  
**Follows from:** TKT-20260416-Phase3b-XI-LOOP.md  
**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-16  
**Stratum:** III  
**Evidence:** D (Konsistenz-Check) + E-open (Ableitung ausstehend)  
**Constitution compliance:** mpmath dps=80, no float(), RG-constraint machine zero

---

## Objective

Analyse der Gribov-Zwanziger (GZ) Struktur als Confinement-Randbedingung
für den FRG-Flow und Bestimmung des erreichbaren Teilresultats für
Limitation L4 (γ nicht aus RG abgeleitet).

---

## Gribov-Zwanziger Propagator als IR-Randbedingung

Der GZ-Gluon-Propagator im Landau-Eichung:

```
D_A^GZ(q²) = q² / (q⁴ + M_G⁴)
```

Effektive Wellenfunktionsrenormierung:

```
Z_gluon^GZ(k) = k⁴ / (k⁴ + M_G⁴)
```

Gitter-Literaturwert: M_G ≈ 0.65 GeV (quenched SU(3); Cucchieri & Mendes 2007,
Bogolubsky et al. 2009, Boucaud et al. 2011).

### Numerische Werte Z_gluon^GZ(k)

| k | Z_gluon^GZ(k) | Regime |
|---|---|---|
| Δ* = 1.71 GeV | 0.97955 | UV: Gluonen propagieren frei |
| M_G = 0.65 GeV | 0.50000 | Confinement-Schwelle |
| 0.30 GeV | 0.03473 | Tiefes IR: stark unterdrückt |
| E_geo = 104.7 MeV | 0.000672 | Vakuum-Resonanz: praktisch null |

---

## GZ-Deformierter FRG-Flow

Modifizierter Wetterich-Regler:

```
R_k^GZ(q²) = R_k^Litim(q²) × Z_gluon^GZ(k²)
           = (k² - q²)θ(k² - q²) × k⁴/(k⁴ + M_G⁴)
```

FRG-Ergebnis: Z_k(k=E_geo)|_GZ ≈ 1.25

Das entspricht γ_FRG = 1.25 (Abweichung 92% von γ = 16.339).

---

## Ursachenanalyse: Warum Z_k/Z_S ≠ γ

γ in UIDT ist ein **Quotienten zweier unabhängiger Skalen**:

```
γ = Δ* / E_geo = (YM-Spektrallücke) / (Skalar-VEV-Resonanz)
```

Beide Skalen entstammen verschiedenen Mechanismen:
- **Δ*** ist durch den nicht-perturbativen SU(3) Yang-Mills Sektor bestimmt (Confinement)
- **E_geo = v/√2** ist durch spontane Symmetriebrechung des Vakuum-Skalars bestimmt

Ein einfacher Z_k-Flow in LPA reproduziert γ nicht, weil er nur **einen** Sektor beschreibt.

### Was für eine vollständige Ableitung nötig ist

1. Vollständig gekoppelter YM+Skalar FRG-Flow
2. Nachweis: v_FRG = Δ*/γ emerges without external input
3. Oder: externe Gitter-QCD-Berechnung von v/Δ*

Dies ist ein numerisch schweres, monatelange Arbeit erforderndes Problem.

---

## Positives Teilresultat: Confinement-Konsistenz [Evidenz D]

Das GZ-Gluon-Bild ist **konsistent** mit dem UIDT-Skalensystem.

**Bedingung:** Die GZ-Dekopplungsskala M_G muss im Confinement-Fenster liegen:

```
E_geo < M_G < Δ*
```

**Numerisch:**
```
104.7 MeV  <  650 MeV  <  1710 MeV
```

ERFÜLLT. [Evidenz D]

### Logarithmische Fensterstruktur

Der gesamte RG-Lauf wird durch M_G asymmetrisch geteilt:

| Bereich | Logarithmische Länge | Anteil |
|---|---|---|
| UV: Δ* → M_G | 0.967 | 34.6% |
| IR: M_G → E_geo | 1.826 | 65.4% |
| Gesamt: Δ* → E_geo | 2.794 = ln(γ) | 100% |

---

## Neue Konjektur UIDT-C-06A [E-open]

Beobachtung: Das Confinement-Fenster teilt den RG-Lauf im Verhältnis:

```
f_UV = ln(Δ*/M_G) / ln(γ) = 0.34625
f_IR = ln(M_G/E_geo) / ln(γ) = 0.65375
```

**UIDT-C-06A [E-open, Stratum III]:** Der Anteil f_UV ≈ 1/e = 0.3679 (Abweichung 6.1%).
Falls f_UV = 1/e exakt wäre, folgte:

```
M_G = Δ* × exp(-1/e) = Δ* × 0.6922 ≈ 1.184 GeV
```

Dies liegt jedoch 82% über dem Gitter-Wert M_G = 0.65 GeV.
**Bewertung:** Konjektur nicht stützbar. f_UV = 1/e als strukturell relevante Zahl
bedarf weiterer Untersuchung. [E-open, spekulativ]

---

## Vollständige L4-Statusmatrix

| Ansatz | Methode | Ergebnis | Status |
|---|---|---|---|
| UIDT-C-05V: Δη=1 | 1-Schleifen ξ-Loop | Tautologisch | WITHDRAWN |
| LPA Einfrierungsskala | k_freeze = sqrt(ρ/ρ̃) | 301 MeV ≠ E_geo | Inkonsistent |
| GZ-Flow Z_k | RK4, Litim+GZ | Z_k(E_geo) = 1.25 | γ_FRG ≠ 16.339 |
| Confinement-Konsistenz | E_geo < M_G < Δ* | Erfüllt | **D** |
| Vollständiger YM+S FRG | Nicht durchgeführt | — | E-open |

**L4 STATUS: E-open** (Limitation bleibt bestehen; ehrlich dokumentiert)

---

## Konklusion

Die Analyse von drei Phasen (LPA, 1-Schleifen ξ-Loop, GZ-Confinement) belegt:

1. γ kann nicht durch einfache 1-Schleifen-Rechnungen im Skalar-Sektor erzeugt werden
2. Die GZ-Struktur ist konsistent mit dem UIDT-Skalensystem (positives Teilresultat)
3. Eine vollständige First-Principles-Ableitung von γ erfordert den vollständig
   gekoppelten nicht-perturbativen YM+Skalar FRG
4. Limitation L4 bleibt offen — Transparenz hat Priorität über Narrative

---

## Constitution Compliance

- mpmath dps=80 lokal deklariert
- kein float() verwendet
- RG-Constraint |5κ² - 3λ_S| = 0 (machine zero)
- Ledger-Konstanten unverändert
- Negative Ergebnisse vollständig dokumentiert
- Konjektur UIDT-C-06A als E-open und spekulativ markiert
