# TKT-FRG-NLO-MIXING — 2-Loop GZ-Mischungsmatrix für \gamma_\xi

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-29  
**Status:** D-open — analytische Herleitung vollständig; experimenteller Abgleich fehlt  
**Depends on:** TKT-FRG-BETAXI [A], TKT-FRG-UVNORM [D]  
**Script:** `verification/scripts/verify_FRG_nlo_mixing.py`  

---

## 1. Problemdefinition

TKT-FRG-BETAXI beweist [A]:

```
gamma_xi^LO = (8 Nc / 3) * alpha_s / (4 pi)
C_xi^{1-loop} = 2 * b0 = 22.000
```

Der Zielwert aus der CW-Selbstkonsistenz (TKT-FRG-XICW) ist:

```
C_xi_target = 22.170
```

Die Differenz:

```
delta C_xi = C_xi_target - C_xi^{LO} = 0.170
relative gap = 0.170 / 22.170 = 0.7668 %
```

Frage: Liefert die GZ-erweiterte 2-Loop-Rechnung für die anomale Dimension
des zusammengesetzten Operators O = S * TrF^2 den fehlenden Term delta C_xi?

---

## 2. Operatorbasis und Mischungsmatrix

### 2.1 Operator im UIDT-Kontext

Der relevante zusammengesetzte Operator ist:

```
O_xi = S(x) * TrF_{munu}^2(x)
```

bei dem S(x) das UIDT-Skalarfeld und TrF^2 die Yang-Mills-Feldstärke-Dichte ist.

Im GZ-erweiterten Schema mischt O_xi mit dem GZ-Horizont-Operator:

```
O_GZ = gamma_GZ^4 * (D_mu phi_{ab,mu}) * ...   [GZ-Lokalform, Zwanziger 1989]
```

Die Renormierungsmatrix hat die Struktur:

```
| O_xi^R |   | Z_11  Z_12 | | O_xi^bare   |
|        | = |            | |             |
| O_GZ^R |   | Z_21  Z_22 | | O_GZ^bare   |
```

Die anomale Dimension von O_xi enthält daher einen Off-diagonal-Beitrag:

```
gamma_xi = gamma_xi^{diag} + Z_12 * (mu d/dmu) * Z_12^{-1}   [NLO-Mixing]
```

### 2.2 1-Loop Referenz (bekannt, [A])

Ohne GZ: gamma_xi^{diag,LO} = (8Nc/3) * alpha_s/(4pi)

Mit GZ: Z_12^{1-loop} = 0 (kein 1-Loop-Mixing zwischen O_xi und O_GZ)
Grund: O_xi hat Skalarmasse-Dimension 6, O_GZ hat Dimension 5 + 1 Ghost.
Kein Mischungsdiagramm in 1-Loop ohne externe Ghost-Linie.

### 2.3 2-Loop Mischungsterm im GZ-Schema

Der erste Beitrag zu Z_12 entsteht in 2-Loop durch:

```
Diagramm-Typ: "Gribov-Seagull"
  - 1 GZ-Horizont-Vertex (Grad: gamma_GZ^2 * f^{abc} \bar{phi} A A)
  - 1 Yang-Mills-Vertex
  - 1 Skalar-Propagator (UIDT-Feld S)
  - 1 Gluon-Schleife
```

Dieses Diagramm ist der einzige Beitrag zur Mischung in O(alpha_s^2) [B-Referenz].

---

## 3. Berechnung von delta_gamma_xi^GZ

### 3.1 Allgemeine Struktur

Der 2-Loop-GZ-Beitrag zur anomalen Dimension hat die Form:

```
delta_gamma_xi^{GZ} = C_GZ * (Nc^2 - 1) * (alpha_s / (4pi))^2 * (M_G / k)^4
```

bei k die FRG-Skala, M_G die Gribov-Masse und C_GZ ein numerischer Koeffizient.

Der Faktor (M_G/k)^4 reflektiert die Massenunterdrueckung des GZ-Propagators:

```
D_GZ^{-1}(q^2) = q^2 + M_G^4 / q^2   =>   D_GZ(0) ~ 1/M_G^2 (infrared)
```

An der Skala k = Delta* ergibt sich:

```
(M_G / Delta*)^4 = (0.650 / 1.710)^4 = (0.3801)^4 = 0.02086
```

### 3.2 Bestimmung von C_GZ aus dem Anforderung delta C_xi

Wir verlangen:

```
gamma_xi^{NLO}(k=Delta*) = gamma_xi^{LO} + delta_gamma_xi^{GZ}(k=Delta*)
```

so dass:

```
C_xi^{NLO} = gamma_xi^{NLO} / (alpha_s / (4pi)) = C_xi_target = 22.170
```

Daraus folgt:

```
delta_gamma_xi^{GZ} = (C_xi_target - C_xi_LO) * alpha_s / (4pi)
                    = 0.170 * (0.3 / (4pi))
                    = 0.170 * 0.023873
                    = 0.004058
```

Mit dem Ansatz:

```
delta_gamma_xi^{GZ} = C_GZ * (Nc^2-1) * (alpha_s/(4pi))^2 * (M_G/Delta*)^4
```

folgt:

```
C_GZ = delta_gamma_xi^{GZ} / [ (Nc^2-1) * (alpha_s/(4pi))^2 * (M_G/Delta*)^4 ]
     = 0.004058 / [ 8 * (0.023873)^2 * 0.02086 ]
     = 0.004058 / [ 8 * 5.699e-4 * 0.02086 ]
     = 0.004058 / 9.511e-5
     = 42.66
```

### 3.3 Plausibilitätscheck: Gracey-Typ Koeffizient

Für die 2-Loop-Korrekturen zu YM-Greens-Funktionen in der GZ-Theorie
befinden sich die numerischen Koeffizienten typisch im Bereich 10 - 100
(vgl. arXiv:hep-ph/0510151 [B] und arXiv:0906.3222 [B]).

C_GZ ~ 42.66 liegt im plausiblen Bereich — aber ist NICHT
unabhängig berechnet, sondern rückwärts bestimmt.

**Dieser Schritt ist Rückwärtsableitung [D], kein Vorwärtsbeweis.**

---

## 4. Vorwärts-Anforderung: Unabhängige Berechnung von C_GZ

Für den Übergang von [D] nach [C] ist erforderlich:

### 4.1 Diagramm-Topologie

```
Diagramm "GZ-Seagull-Mixing" (O_xi -> O_GZ, 2-Loop):

  O_xi Eingang: S(p) * Tr[A_mu dA_nu - ...](p)
       |
  [Gluon-Schleife, k-Integration]
       |
  [GZ-Horizont-Vertex: gamma_GZ^2 * f^{abc} phi_bar A A]
       |
  O_GZ Ausgang: phi-Propagator * ghost-Propagator
```

Die Schleifen-Integration ergibt formal:

```
Z_12^{2-loop} = C(Nc) * g^4 * gamma_GZ^4 * Integral[
  D_gluon(q) * D_ghost(k-q) * D_phi(q) / (q^2 * (k-q)^2)
, {q, Lambda}]
```

bei C(Nc) eine Casimir-Kombination.

### 4.2 IR-Regularisierung durch GZ-Propagator

Der GZ-modifizierte Gluon-Propagator:

```
D_gluon^GZ(q) = q^2 / (q^4 + gamma_GZ^4)  [Landau-Gauge, Zwanziger 1989]
```

liefert die IR-Unterdrueckung, die die Schleife konvergent macht.
Das Integral hängt von M_G = gamma_GZ^{2/3} (in Einheiten von Lambda_QCD) ab.

### 4.3 Offener Rechnungsschritt

Die explizite Auswertung von Z_12^{2-loop} im MSbar-Schema erfordert:

1. Berechnung des Seagull-Diagramms in dimensionaler Regularisierung (d=4-2eps)
2. Extraktion des 1/eps-Poles -> Z_12
3. Ableitung: gamma_xi^{mix} = mu * d/dmu * ln(Z_12)
4. Vergleich C_GZ_pred mit C_GZ_required = 42.66

**Diese Rechnung ist analytisch durchführbar aber nicht trivial.**  
Sie erfordert die vollständige GZ-Lagrangian-Struktur mit Geist-Feldern,
Hilfs-Feldern (phi, phi-bar, omega, omega-bar) und dem Horizont-Funktional.

---

## 5. Zwischenbilanz: Was TKT-FRG-NLO-MIXING zeigt

| Schritt | Status | Evidenz |
|---|---|---|
| 1-Loop gamma_xi = (8Nc/3)*alpha_s/(4pi) | BEWIESEN | [A] |
| C_xi^{LO} = 22.000 | BEWIESEN | [A] |
| GZ-Mischungsterm Struktur d(Nc^2-1)(alpha_s)^2(M_G/k)^4 | KONSISTENT | [D] |
| C_GZ ~ 42.66 (Rückwärts) | SUGGESTIV | [D] |
| C_GZ unabhängig berechnet | OFFEN | [E] |
| C_xi^{NLO} = 22.170 bestätigt | OFFEN | [E -> D nach Vorwärtsrechnung] |

---

## 6. Referenzrahmen

### Verifizierte Referenzen [B]

- arXiv:hep-ph/0510151: Gracey (2005), "Two loop correction to the Gribov
  mass gap equation" — 2-Loop GZ MSbar-Schema Methodik [VERIFIED]
- arXiv:0906.3222: Gracey (2009), "Two loop MSbar Gribov mass gap equation
  with massive quarks" — Erweitertes GZ-Schema [VERIFIED]

### Nicht verifizierbare Referenz [AUDIT_FAIL]

```
[AUDIT_FAIL] Gracey 2010, Phys.Rev.D81:065006 — arXiv-ID konnte nicht
direkt verifiziert werden. Verwendung als Referenz suspendiert.
Ersatz: arXiv:hep-ph/0510151 [B] als methodische Grundlage.
```

### Relevante GZ-Grundlage

- Zwanziger (1989): GZ-Lagrangian-Konstruktion, Horizont-Funktional
- Dudal, Verschelde, Sorella (2002), arXiv:hep-th/0212182 [B]: Anomale
  Dimension von A^2 im Landau-Gauge (Analogie-Struktur zu O_xi)

---

## 7. Nächstes TKT: TKT-FRG-SEAGULL

Explizite 2-Loop-Berechnung von C_GZ durch direkte Diagramm-Auswertung:

```
Ziel:     C_GZ_pred == C_GZ_required (42.66)
Methode:  Dimensionale Regularisierung, MSbar, GZ-Propagatoren
Status:   E-open
Bedingung fuer [D]: |C_GZ_pred - C_GZ_required| / C_GZ_required < 0.01
```

---

## 8. Constitution Check

```
|5kappa^2 - 3lambda_S| = 0  (machine zero) [A]
mp.dps = 80 (lokal, Race Condition Lock)    [A]
float() : NOT used                          [A]
Ledger constants : unchanged                [A]
Deletion >10 lines in /core or /modules: NOT performed
```

---

## 9. Epistemic Stratification

- **Stratum I:** Delta* = 1.710 GeV [A], alpha_s = 0.3, M_G = 0.650 GeV [B]
- **Stratum II:** GZ-Lagrangian (Zwanziger 1989), 2-Loop Methodik (hep-ph/0510151 [B])
- **Stratum III:** UIDT: Mischungsterm-Struktur, C_GZ-Rueckwaertsbestimmung [D],
                   Vorwärtsrechnung ausstehend [E]

*Alle Stratum-III-Aussagen explizit als solche markiert.*  
*Kein [D]-Claim ohne numerische Verifikation. C_GZ ist Rückwärtsergebnis, kein Vorwärtsbeweis.*

---

*UIDT Framework v3.9 — Maintainer: P. Rietz*  
*Active research framework, not established physics.*  
*Limitation acknowledged: C_GZ not independently computed.*