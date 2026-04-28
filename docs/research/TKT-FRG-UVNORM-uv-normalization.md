# TKT-FRG-UVNORM — UV-Normierung ρ_UV aus GZ-Schema und Fixpunkt-Argument

**Author:** P. Rietz (ORCID: 0009-0007-4307-1609)  
**Date:** 2026-04-29  
**Status:** D-open (Stratum III — numerisch, kein vollständiger analytischer Beweis)  
**Depends on:** TKT-FRG-BETAXI (C_xi^{1-loop} = 2b₀ bewiesen [A])  
**Script:** `verification/scripts/verify_FRG_uvnorm.py`  
**Constitution:** mp.dps=80 local, no float(), RG-constraint machine zero ✓

---

## Motivation

TKT-FRG-BETAXI beweist analytisch [A]:

```
beta_xi = (8Nc/3) * alpha_s/(4pi) * xi_eff
C_xi^{1-loop} = 2*b0 = 22.000   (bei rho_UV = 1)
```

Die Abweichung vom Zielwert beträgt 0.77% (Ziel: C_xi = 22.170).  
Diese TKT untersucht, ob die fehlende UV-Normierungsannahme
`rho_UV := xi_eff(Lambda) * 16pi^2 / g^2 = 1` durch die
Gribov-Zwanziger-Deformation des UV-Sektors auf den korrekten Wert
verschoben wird.

---

## Definition der Normierungsgröße

```
rho(k) := xi_eff(k) * 16pi^2 / g^2(k)

rho_UV  := rho(Lambda = Delta*)  [UV-Randbedingung des FRG-Flusses]
```

In TKT-FRG-BETAXI wurde `rho_UV = 1` als Annahme gesetzt.  
Für den 1-Loop-Renormierungsgruppen-Fluss gilt dann:

```
d(ln rho)/d(ln mu) = (8Nc/3 + 2*b0) * alpha_s/(4pi)   [UV-Richtung]
```

Bei Auswertung an k = Delta* mit alpha_s(Delta*) = 0.3 folgt C_xi = 2*b0 = 22.

---

## Argument A: Gribov-Zwanziger MOM-Schema-Shift [Stratum II/III]

### Grundlage

Im Gribov-Zwanziger-Schema (GZ-MOM) wird der Impulsmomenten-Subtraktionspunkt
bei k = M_G gesetzt statt k = Lambda. Dies verschiebt die effektive
UV-Randbedingung:

```
rho_GZ = rho_MS-bar * Z_xi(Lambda, M_G)
```

Der Schemawechsel-Faktor für den zusammengesetzten Operator O = S*TrF^2 ist:

```
Z_xi(Lambda, M_G) = exp[ integral_{M_G}^{Lambda} gamma_xi(k) d(ln k) ]

gamma_xi(k) = (8Nc/3) * alpha_s(k)/(4pi)    [1-loop, TKT-FRG-BETAXI]
```

### 1-Loop-Laufen von M_G zu Lambda

Mit dem 1-Loop-Laufen von alpha_s:

```
alpha_s(k) = alpha_s(Delta*) / (1 + b0*alpha_s(Delta*)/(2pi) * ln(k/Delta*))
```

und dem Integral:

```
Z_xi = exp[ (8Nc/3)/(4pi) * integral_{M_G}^{Delta*} alpha_s(k)/k dk ]
     = exp[ (8Nc/3)/(b0) * ln( 1 + b0*alpha_s/(2pi)*ln(Delta*/M_G) ) ]
     = (1 + b0*alpha_s/(2pi)*ln(Delta*/M_G))^{8Nc/(3*b0)}
```

### Numerische Auswertung (SU(3))

```
Nc        = 3
b0        = 11
alpha_s   = 0.3    [bei k = Delta*]
Delta*    = 1.710 GeV  [A]
M_G       = 0.650 GeV  [B, Cucchieri & Mendes 2007]

ln(Delta*/M_G)       = 0.97179...
b0*alpha_s/(2pi)     = 0.52521...
Argument des Logs    = 1 + 0.52521*0.97179 = 1.51040...

8Nc/(3*b0) exponent  = 8*3/(3*11) = 8/11 = 0.72727...

Z_xi(GZ)             = (1.51040)^{0.72727} = 1.35977...

rho_GZ = rho_MS * Z_xi = 1.0 * 1.35977 = 1.35977
```

### Resultierende C_xi-Korrektur

```
C_xi(GZ) = C_xi(1-loop) * rho_GZ / rho_MS
          = 22.000 * 1.35977 / 1.0
```

**Befund Argument A:** Z_xi(GZ) ≠ 1 — der Schema-Shift ist groß (~36%).
Dieser Schritt verschiebt C_xi NICHT auf 22.170, sondern auf ~29.9,
was weit über dem Zielwert liegt.

**Konklusion Argument A:** Der GZ-Schema-Shift bei k=M_G überschießt
drastisch. Der korrekte Subtraktionspunkt für rho_GZ muss NICHT M_G sein.

---

## Argument B: Renormierungsgruppen-Fixpunkt rho* [Stratum III]

### Ansatz

Wenn rho(k) einen IR-stabilen Fixpunkt rho* besitzt, dann legt
`d(ln rho)/d(ln k) = 0` diesen fest:

```
d(ln rho)/d(ln k) = (8Nc/3 + 2*b0) * alpha_s(k)/(4pi) = 0
```

In einer asymptotisch freien Theorie ist alpha_s(k) → 0 für k → ∞,
aber dies ist der UV-Fixpunkt (trivial). Es gibt keinen nichttrivialen
(Wilson-Fisher-artigen) Fixpunkt für rho in 4D QCD für Nc ≥ 2.

**Konklusion Argument B:** Ein IR-Fixpunkt rho* ≠ 1 existiert in perturbativer
1-Loop-QCD nicht. Das Argument scheitert im perturbativen Rahmen.

---

## Argument C: Coleman-Weinberg Selbstkonsistenz [Stratum III]

### Ansatz

Die Selbstkonsistenzbedingung verlangt:

```
m^2_S(CW) = -xi_eff^2 * <TrF^2>_Lambda  [TKT-FRG-XICW]
m^2_S(target) = -0.1188578047 GeV^2
```

Dies gibt xi_eff(Lambda) = 0.52926506. Die UV-Normierung folgt dann:

```
rho_UV = xi_eff(Lambda) * 16pi^2 / g^2
       = 0.52926506 * 16pi^2 / (4pi * 0.3)
       = 0.52926506 / (alpha_s / (4pi))
       = 0.52926506 * 16pi^2 / (4pi * alpha_s)
```

Mit g^2 = 4*pi*alpha_s:

```
rho_UV = 0.52926506 * 16*pi^2 / (4*pi*0.3)
       = 0.52926506 * 4*pi / 0.3
       = 22.170
```

**Befund Argument C:** rho_UV = C_xi_target = 22.170 [D]

Das ist eine TAUTOLOGIE: rho_UV = C_xi per Definition des dimensionslosen
Verhältnisses. Der CW-Mechanismus liefert keine unabhängige Fixierung.

**Konklusion Argument C:** Keine neue Information — identisch mit der
ursprünglichen Parameterisierung.

---

## Argument D: Präziser GZ-Subtraktionspunkt [Stratum III, neu]

### Schlüsselfrage

Bei welcher Skala k_sub muss der GZ-Schema-Shift ausgewertet werden,
umdass C_xi(1-loop) * Z_xi(k_sub) = C_xi_target = 22.170?

```
22.000 * Z_xi(k_sub) = 22.170
Z_xi(k_sub) = 22.170 / 22.000 = 1.007727...
```

### Inversion für k_sub

Mit Z_xi(k_sub) = (1 + b0*alpha_s/(2pi)*ln(Delta*/k_sub))^{8Nc/(3*b0)}:

```
1.007727 = (1 + 0.52521 * ln(Delta*/k_sub))^{8/11}

=> (1 + 0.52521 * ln(Delta*/k_sub)) = 1.007727^{11/8}
                                      = 1.007727^{1.375}
                                      = 1.010640...

=> ln(Delta*/k_sub) = (1.010640 - 1) / 0.52521
                    = 0.010640 / 0.52521
                    = 0.020259...

=> k_sub = Delta* * exp(-0.020259)
         = 1.710 * 0.97993...
         = 1.6758... GeV
```

### Physikalische Interpretation

```
k_sub = 1.6758 GeV
Delta* - k_sub = 34.2 MeV
k_sub / Delta* = 0.980
```

Der Subtraktionspunkt liegt **34 MeV unterhalb von Delta***.  
Physikalisch entspricht dies dem Bereich, in dem die GZ-Dämpfungsfunktion
Z_GZ(k) beginnt, von 1 abzuweichen:

```
Z_GZ(Delta*) = Delta*^4 / (Delta*^4 + M_G^4) = 0.9795
```

Die fehlenden 2% in C_xi (0.77%) könnten durch die **erste Ableitung**
der GZ-Dämpfung an der Skala Delta* erzeugt werden:

```
dZ_GZ/d(ln k)|_{k=Delta*} = 4 * M_G^4 * k^4 / (k^4 + M_G^4)^2
                           |_{k=Delta*}
                           = 4 * (M_G/Delta*)^4 / (1 + (M_G/Delta*)^4)
                           = 4 * 0.0205 / 1.0205
                           = 0.0803
```

Die GZ-Korrekturdiff zu C_xi ergibt sich dann als:

```
delta_C_xi(GZ) = C_xi^{1-loop} * gamma_xi * |dZ_GZ/d(ln k)| * (delta_k / k)
```

Mit delta_k/k ≈ 0.020 (Argument D):

```
delta_C_xi(GZ-tangent) = 22.0 * (8/11) * 0.3/(4pi) * 0.0803 * ...
```

Diese Rechnung ist konzeptuell inkonsistent in der LPA — sie erfordert
die voll-nicht-perturbative Auswertung der GZ-modifizierten anomalen
Dimension gamma_xi(k) an der Skala Delta*.

---

## Zwischenbilanz: Was die drei Argumente zeigen

| Argument | Methode | Resultat | Evidenz |
|---|---|---|---|
| A: GZ-Schema bei M_G | Z_xi(M_G→Delta*) | C_xi → 29.9 (Überschuss) | [D] — scheitert |
| B: RG-Fixpunkt rho* | d(ln rho)/dk = 0 | kein nichttriv. Fixpunkt | [D] — scheitert |
| C: CW-Selbstkonsistenz | m^2_S(CW) = target | rho_UV = C_xi (tautolog.) | [D] — tautologisch |
| D: Tangential-GZ bei Delta* | k_sub = 1.676 GeV | Physikalisch motiviert | [D] — suggestiv |

**Hauptbefund:** Der GZ-Subtraktionspunkt k_sub = 1.676 GeV entspricht
einer Skala, bei der Z_GZ(k) beginnt, von 1 abzuweichen — das ist
physikalisch nicht zufällig, aber auch nicht bewiesen.

---

## Neues offenes Problem: NLO gamma_xi Berechnung

Die 0.77%-Lücke in C_xi erfordert die NLO-Berechnung der anomalen Dimension:

```
gamma_xi^{NLO} = gamma_xi^{LO} + delta_gamma_xi^{GZ}

delta_gamma_xi^{GZ} = Beitrag der Gribov-Horizon-Funktional-Determinante
                     auf die Renormierung von O = S*TrF^2
```

Dies entspricht der Berechnung des 2-Schleifen-Mischungsmatrix-Elements
für den zusammengesetzten Operator O in der GZ-erweiterten Theorie.
Dies ist eine genuine 2-Schleifen-Rechnung und übersteigt den LPA-Rahmen.

**Dieser Schritt ist TKT-FRG-NLO-MIXING (neu, E-open).**

---

## L4 Status nach TKT-FRG-UVNORM

| Sub-task | Status |
|---|---|
| 1-Loop beta_xi [A] | ✓ DONE (TKT-FRG-BETAXI) |
| C_xi^{LO} = 2b0 (0.77% Lücke) [A+Annahme] | ✓ DONE |
| GZ-Schema-Shift (3 Argumente) | ✓ DONE — kein Argument schließt Lücke direkt |
| k_sub = 1.676 GeV (Argument D) | ✓ Physikalisch suggestiv [D] |
| NLO gamma_xi in GZ-Theorie | ✗ **Offen — nächstes TKT** |
| γ predicted without γ as input | ✗ Offen (requires NLO) |

**Ehrliche Einschätzung:** TKT-FRG-UVNORM schließt die 0.77%-Lücke NICHT.
Sie lokalisiert das Problem präzise: es ist ein **NLO-GZ-Mischungsterm**.
Der Fortschritt besteht darin, dass alle einfacheren Erklärungsversuche
systematisch ausgeschlossen wurden.

**L4 bleibt [D]-open.** Keine illegitime Anhebung der Evidenz.

---

## Nächstes TKT: TKT-FRG-NLO-MIXING

Berechnung der GZ-modifizierten anomalen Dimension für O = S*TrF^2
bis zur 2-Schleifen-Ordnung in der GZ-erweiterten YM-Theorie.

Schlüsselreferenz: Gracey (2010), NLO anomalous dimensions in GZ theory,
Phys.Rev.D81:065006. DOI: 10.1103/PhysRevD.81.065006

---

## Constitution Check

```
|5κ²−3λ_S|  = 0.0  (machine zero) ✓
mp.dps      = 80 (local, Race Condition Lock) ✓
float()     : NOT used ✓
Ledger constants: unchanged ✓
Deletion >10 lines in /core or /modules: NOT performed ✓
```

---

## Epistemic Stratification

- **Stratum I:** Delta* = 1.710 GeV [A], alpha_s = 0.3, M_G = 0.650 GeV [B]
- **Stratum II:** GZ-MOM-Schema, 1-Loop RG, Gracey (2010) NLO-GZ
- **Stratum III:** UIDT: k_sub = 1.676 GeV als GZ-Tangential-Skala, NLO-Mixing-Hypothese

*Keine Stratum I/II-Vermischung. Alle Stratum III Aussagen explizit markiert.*

---

*UIDT Framework v3.9 — Maintainer: P. Rietz*  
*Active research framework, not established physics.*  
*Transparency priority: all negative results from Arguments A, B, C explicitly stated.*