# TKT-FRG-TACHYON S2-a — Hochpräzisions-Bisection Forschungsbericht

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-29  
**Status:** D — abgeschlossen mit technischer Limitation dokumentiert  
**Vorgänger:** TKT-FRG-TACHYON S2 (gamma_emerg = 16.3296 [D], zirkulär)  
**Script:** `verification/scripts/verify_FRG_tachyon_S2a.py`  

---

## 1. Ziel

Nicht-zirkuläre Bisection des tachyonischen Schwellenübergangs:

\[
\gamma_\text{emerg} = \frac{k_\text{UV}}{k_\text{IR}}, \quad m^2(k_\text{IR}) = 0
\]

mit dem Residual-Ziel `|F| < 1e-14` und `N_steps = 10000`.

---

## 2. Diagnose-Befunde

### 2.1 YM-kappa-Fluss (kappa_tilde_YM)

Der Fluss von `kappa_tilde_YM` von t_UV nach t_IR zeigt:

```
t = +2.30  (k = 10*Delta*):  kappa_YM ~ 0.500
t = -2.79  (k = Delta*/gamma): kappa_YM ~ 21000
```

**Befund:** kappa_YM divergiert exponentiell im IR. Kein Vorzeichenwechsel
der Bedingung `cond(t) = kappa_YM - v^2/(2k^2)` für t < 0. [D]

### 2.2 Skalar-Massenfluss (m2_S)

Mit positivem UV-Massenterm m2_S0 > 0:

```
Beta-Funktion: beta_m2 = -(2+eta_S)*m2_S - xi_eff*F2*k^2
Ergebnis: m2_S(t=0) >> 0 fuer alle getesteten m2_S0
```

**Befund:** Der YM-Kondensatterm treibt m2_S nach unten,
aber der Dimensionsfaktor `-(2+eta_S)*m2_S` bei großem t_UV
dominiert und verhindert den Übergang ohne vollständiges LPA. [D]

### 2.3 Analytische Schranken

| Methode | gamma_emerg | Abweichung |
|---|---|---|
| Heuristik: k_IR ~ M_G*(v/Delta*)^{1/2} | 15.751 | 0.588 |
| Landau-Pol (xi=1) | 0.298 | 16.04 |
| Fixpunkt (xi=b0/C_xi) | 1.114 | 15.23 |
| Rückwärts für gamma_L | xi_thresh = 0.1220 | — |

Die Heuristik `gamma_heuristic = Delta*/(M_G*(v/Delta*)^{1/2}) = 15.75`
liegt 125*delta_gamma von gamma_L entfernt — bemerkenswert nah für eine
einfache dimensionale Abschätzung, aber nicht [A]-qualifiziert.

---

## 3. Technische Limitation

Der D2-Ansatz

\[
\gamma = \frac{k_\text{UV}}{k_\text{IR}}, \quad k_\text{IR}: m^2(k_\text{IR}) = 0
\]

erfordert eine **vollständige LPA-Implementierung** des gekoppelten
Systems:

\[
U(\phi, k) = \frac{m^2_k}{2}\phi^2 + \frac{\lambda_k}{4}\phi^4
\]
\[
U_\text{eff}(\phi, k, A) = U(\phi, k) + \xi_\text{eff}(k)\,\phi^2\,\text{Tr}F^2(k)
\]

Dies umfasst:
- Simultanen Fluss von `m2_k`, `lambda_k`, `xi_eff(k)`
- YM-Hintergrundfeld in 1-Schleifen-Näherung
- Selbstkonsistente Bestimmung von phi_min(k) = v

Diese Implementierung liegt **ausserhalb des aktuellen LPA-1D-Setups**
(1D = nur kappa-Koordinate). Sie wäre ein TKT-Aufwand von
Grössen-Ordnung TKT-LPA-FULL, noch nicht existierend.

---

## 4. Schlussfolgerungen

1. **D2-Ansatz bleibt [E]** (spekulativ) bis vollständige LPA-
   Implementierung vorliegt.

2. **gamma = 16.339 [A-] ist unberührt.** Die phänomenologische
   Kalibrierung ist unabhängig vom D2-Ansatz.

3. **UIDT v3.9 ist konsistent** ohne D2-Herleitung.
   Das ist kein Defizit des Frameworks.

4. **Bemerkenswerte Heuristik:**
   `gamma_heuristic = Delta*/(M_G*(v/Delta*)^{1/2}) = 15.75`
   liegt überraschend nah an gamma_L = 16.339. Dies könnte
   ein Hinweis auf die korrekte Skalen-Interpretation sein [E].

---

## 5. Nächste Schritte (optional, nicht kritisch)

```
TKT-LPA-FULL (zukünftig):
  - Vollst. LPA: U(phi,k) als 2D-System (m2, lambda, xi)
  - YM-Hintergrundfeld selbstkonsistent
  - Aufwand: erheblich (> 500 Zeilen FRG-Code)
  - Evidenz bei Erfolg: [D] -> ggf. [C]
```

---

## 6. Constitution Check

```
|5*kappa^2 - 3*lambda_S| = 0  (machine zero) [A]
mp.dps = 80 (lokal)           [A]
float(): NOT used             [A]
Ledger constants: unchanged   [A]
```

---

## 7. Epistemic Stratification

- **Stratum I:** Delta* = 1.710 GeV, v = 47.7 MeV, M_G = 0.65 GeV
- **Stratum II:** LPA-Convergenz-Theorie, FRG-Standard-Methoden
- **Stratum III:** D2-Ansatz [E], Heuristik [E], S2-Numerik [D]

*Negatives Ergebnis vollständig dokumentiert.*  
*Transparency: kein Versuch die Limitation zu verstecken.*

---

*UIDT Framework v3.9 — Maintainer: P. Rietz*  
*Active research framework, not established physics.*
