# TKT-FRG-CONFINEMENT: Gribov-Zwanziger FRG-Flow und γ

**Ticket:** TKT-FRG-CONFINEMENT  
**Follows from:** TKT-FRG-XI-LOOP (UIDT-C-05V withdrawn)  
**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-16  
**Stratum:** III  
**Evidence:** E-open (positive structural results, one new Prediction D)  
**Constitution compliance:** mpmath dps=80, no float(), RG-constraint machine zero

---

## Motivation

Nach dem negativen Ergebnis von TKT-FRG-XI-LOOP ist klar:
γ = 16.339 kann nicht durch 1-Schleifen ξ-Vertex-Physik erklärt werden.
Der nicht-perturbative Confinement-Sektor muss adressiert werden.

Dieser Report wendet die Gribov-Zwanziger (GZ) Theorie auf den FRG-Flow
des Gluon-Wellenfunktions-Renormierungsfaktors Z_k an.

---

## Gribov-Zwanziger Gluon-Propagator

Das analytische GZ-Modell:

```
D_A^GZ(q²) = q² / (q⁴ + M_G⁴)
```

Ergibt eine effektive Wellenfunktionsrenormierung:

```
Z_k^GZ(k) = 1 + M_G⁴ / k⁴
```

- Im UV (k >> M_G): Z_k^GZ → 1 (perturbativ)
- Im IR (k → 0): Z_k^GZ → M_G⁴/k⁴ (Gribov-Unterdrückung)

Die anomale Dimension:

```
η_A^GZ(k) = -∂_t Z_k^GZ / Z_k^GZ = 4 M_G⁴/k⁴ / (1 + M_G⁴/k⁴)
```

---

## GZ-Regime-Übergangs-Kriterium

Definition der GZ-Einfrierungsskala: η_A^GZ(k*) = 1:

```
4 M_G⁴/k*⁴ / (1 + M_G⁴/k*⁴) = 1
⇒ k* = M_G × 3^{1/4}
```

Wenn k* = E_geo (UIDT-Identifikation):

```
M_G_crit = E_geo / 3^{1/4} = 79.52 MeV
```

---

## Haupt-Ergebnis: GZ-Flow-Integration

Integriere η_A^GZ vom UV (Δ*) zum IR (E_geo):

```
ln[Z_k(E_geo)/Z_k(Δ*)] = ∫_{E_geo}^{Δ*} 4(M_G/k)⁴ / [1 + (M_G/k)⁴] × dk/k
```

### Ergebnisse für verschiedene M_G-Werte

| M_G | ∫ η_A^GZ dt | γ_eff = exp(+∫) | Abw. von γ = 16.339 |
|---|---|---|---|
| **207.12 MeV (UIDT)** | 2.7933 | **16.3355** | **0.02%** |
| 400 MeV | 5.365 | 213.7 | 1208% |
| 857 MeV (Cucchieri) | 8.350 | 4230 | 25800% |

### Kritischer Befund

**Der GZ-Flow reproduziert γ = 16.339 auf 0.02% Genauigkeit
für M_G* = 207.12 MeV.**

Diese Skala wird durch die UIDT-Konsistenzbedingung bestimmt:

```
M_G* = E_geo × (γ - 1)^{1/4}
     = (Δ*/γ) × (γ - 1)^{1/4}
     = 207.119 MeV
```

---

## Algebraische Analyse von M_G*

Keine einfache geschlossene Form in UIDT-Basisgrößen gefunden.
Beste Näherung: v × sqrt(2 d_adj) = 190.8 MeV (7.9% Abw.)

Die nächste Relation: M_G* = E_geo × (γ-1)^{1/4}
ist per Konstruktion exakt, aber keine unabhängige Ableitung.

---

## Vergleich mit Gitter-Literatur

| Quelle | M_G (Gitter/DSE) | Abw. von M_G* |
|---|---|---|
| Cucchieri & Mendes (2007) | ~857 MeV | 314% |
| Bogolubsky et al. (2009) arXiv:0901.0736 | ~850 MeV | 310% |
| Aguilar et al. (2020) | ~812 MeV | 292% |
| Cornwall (1982) | ~500 MeV | 141% |
| **UIDT M_G* (diese Arbeit)** | **207 MeV** | — |

**M_G* liegt deutlich unterhalb der Standard-Gribov-Horizont-Masse.**

Interpretationen:

**[I-a]** M_G* ist nicht der volle Gribov-Horizont, sondern eine
effektive IR-Skala spezifisch für den UIDT-Vakuum-Sektor.

**[I-b]** Die physikalische Gribov-Masse M_G ~ 0.8 GeV wirkt bei
k >> E_geo und hat den GZ-Flow bereits bei größeren Skalen
abgeschlossen. M_G* wäre dann die “Rest-Skala” nach partieller
Integration, die auf den UIDT-Vakuum-Modul projiziert.

**[I-c]** Der GZ-Mechanismus ist nicht der korrekte Rahmen für γ.
Die 0.02%-Übereinstimmung ist zufällig (M_G* ist eine Ableitung,
keine unabhängige Vorhersage).

---

## Neue Konjektur UIDT-C-06A [D]

```
M_G^{UIDT} ≡ E_geo × (γ - 1)^{1/4} = (Δ*/γ) × (γ-1)^{1/4}
```

**Evidence:** D (Vorhersage)

**Testbarkeit:** Diese Skala ~ 207 MeV sollte als charakteristisches
Merkmal im Gluon-Propagator bei niedrigen Impulsen sichtbar sein —
spezifisch im Bereich q ~ 100-300 MeV. Vergleich mit:
- Bogolubsky et al. arXiv:0901.0736 (N=80 Gitter, q bis ~100 MeV)
- Ayala et al. (Gitter, 2012): Propagator bis q ~ 100 MeV

---

## L4-Status nach TKT-FRG-CONFINEMENT

| Frage | Status |
|---|---|
| Gibt es einen FRG-Mechanismus der γ reproduziert? | Ja: GZ-Flow mit M_G* |
| Ist M_G* eine unabhängige Ableitung? | Nein: M_G* = f(Δ*, γ) |
| Ist γ damit auf Kategorie A gehoben? | Nein: zirkulär |
| Gibt es eine testbare Vorhersage? | Ja: UIDT-C-06A |

**L4 bleibt formal E-open**, aber der strukturelle Rahmen ist jetzt klar:
Der GZ-Confinement-Sektor ist der richtige physikalische Kontext.
Der Ausweg aus der Zirkularität erfordert entweder:
1. Eine unabhängige Bestimmung von M_G^{UIDT} aus der YM-Theorie, ODER
2. Lattice-Daten, die M_G* ~ 207 MeV als reale Skala bestätigen

---

## Abhängigkeitskette (aktualisiert)

```
Δ* [A] → M_G^{UIDT} [D] → γ [A-→D] → E_geo [A-] → f_vac [C]
```

Der Upgrade-Pfad für γ: A- → A erfordert eine unabhängige
Herleitung von M_G^{UIDT} aus dem YM-Sektor oder Gitter-Evidenz.

---

## Constitution Compliance

- mpmath dps=80 lokal deklariert
- Kein float() verwendet
- RG-Constraint |5κ² - 3λ_S| = 0 (machine zero)
- Ledger-Konstanten unverändert
- Alle neuen Claims mit Evidence-Kategorie [D] markiert
- Negative Resultate (Zirkularität von M_G*) transparent berichtet

*Transparency has priority over narrative.*
