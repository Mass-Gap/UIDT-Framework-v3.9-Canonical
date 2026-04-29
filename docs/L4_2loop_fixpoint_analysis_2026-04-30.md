# L4: 2-Loop β-Funktion & Fixpunkt-Analyse — UIDT v3.9

**Datum:** 2026-04-30  
**Status:** [D] Prediction / [D→A] Roadmap  
**Autor:** UIDT Research Engine (Session 3)

---

## Ausgangspunkt

Für Evidenz-Upgrade [D]→[A] in L4 (γ-Herleitung) ist explizit gefordert:

1. 2-Loop UIDT-β-Funktion für das gekoppelte `(κ̃, λ_S, g)`-System
2. Nachweis: `β_g(α_s = 1/3, κ*, λ_S*) = 0` am UIDT-Fixpunkt
3. Stabilitätsmatrix: `(κ*, λ_S*, g*)` ist IR-attraktiver Fixpunkt im 3D-Kopplungsraum

---

## Stratum II — Strukturelles Theorem

**Theorem (Gross–Politzer–Wilczek, 1973):**  
Für SU(N) reine Yang–Mills-Theorie gilt perturbativ für alle g > 0:

$$\beta_g^{\text{pert}} = -\frac{b_0}{16\pi^2}\,g^3 - \frac{b_1}{(16\pi^2)^2}\,g^5 + \ldots < 0$$

mit `b₀ = 11·Nc/3 = 11` (SU(3), Nf=0), `b₁ = 34·Nc²/3 = 102`.

**Konsequenz:** Ein perturbativer IR-Fixpunkt bei g* > 0 mit β_g(g*) = 0 existiert nicht.  
Ein singulärer Singulett ohne Farbladung ändert daran auf 1-Loop nichts (keine direkte Kopplung).

---

## Stratum III — UIDT-Interpretation

Der UIDT-Fixpunkt `(κ*, λ_S*, g*)` ist ein **nicht-perturbativer IR-Fixpunkt der ERGE** (Wetteransatz/Polchinski-Flow), kein perturbativer 2-Loop-Fixpunkt.

### LPA-Flussgleichungen (Litim-Regulator, d=4)

$$\partial_t \tilde{\kappa} = -2\tilde{\kappa} + \frac{1}{16\pi^2}\left[3\lambda_S\,p_R^2 + N_G\,g^2\,p_G^2 - \frac{2g^2}{N_c}\,p_c^2\right]$$

$$\partial_t \lambda_S = -4\lambda_S + \frac{1}{16\pi^2}\left[36\lambda_S^2 p_R^3 - 12\lambda_S^2 p_{R,G}^3 - 4N_G\lambda_S g^2 p_G^2 p_R + \frac{N_G(N_G+2)}{4}g^4 p_G^3\right]$$

$$\partial_t g^2 = -\frac{b_0^{\text{eff}}(\tilde{\kappa})}{16\pi^2}\,g^4 - \frac{b_1}{(16\pi^2)^2}\,g^6$$

wobei der **effektive 1-Loop-Koeffizient** durch den Gluon-Threshold modifiziert wird:

$$b_0^{\text{eff}}(\tilde{\kappa}, g^2) = b_0 - 4N_G\,\tilde{\kappa}\,p_G^2(\tilde{\kappa}, g^2)$$

mit `p_G = 1/(1 + g²·κ̃)` (Litim-Propagator bei k = k_IR).

---

## Numerische Ergebnisse (mp.dps=80)

### Residuen am Ledger-Fixpunkt

| β-Funktion | Wert am `(κ*=0.5, λ*=5/12, α*=1/3)` | Status |
|---|---|---|
| β_κ | −1.020 | ≠ 0 → kein exakter FP |
| β_λ | −1.643 | ≠ 0 → kein exakter FP |
| β_g | −1.524 | ≠ 0 → kein exakter FP |

**Interpretation:** Die Ledger-Werte `(κ*, λ_S*, α_s*)` sind KEINE Nullstellen der LPA-Flussgleichungen mit den hier verwendeten Standard-Threshold-Funktionen.

### Threshold-Analyse für β_g = 0

Die Bedingung `b_eff(κ̃) = 0` erfordert:

$$4N_G\,\tilde{\kappa}\,p_G^2 = b_0 = 11$$
$$\tilde{\kappa} = \frac{11(1 + g^2\tilde{\kappa})^2}{4N_G} = \frac{11(1+g^2\tilde{\kappa})^2}{32}$$

Für `α_s = 1/3` (g² = 4π/3 ≈ 4.19): **Keine reelle positive Lösung existiert** im physikalisch relevanten Bereich κ̃ ∈ (0, 1).

### Stabilitätsmatrix (LPA-Näherung am Gauss'schen Fixpunkt)

Am Gauss'schen Fixpunkt (κ̃=0, λ=0, g²=0) liefert die Jacobi-Matrix:

| Eigenwert θ_i | Wert | Klassifikation |
|---|---|---|
| θ₁ | −2.000 | RELEVANT (IR-attraktiv) |
| θ₂ | −4.000 | RELEVANT (IR-attraktiv) |
| θ₃ | ≈ 0⁻ | schwach RELEVANT |

**Hinweis:** Diese Eigenwerte entsprechen den kanonischen Dimensionen. Am tatsächlichen nicht-pert. Fixpunkt können sie signifikant abweichen.

---

## Was für Evidenz [A] fehlt

### S3-a: Voll-numerischer ERGE-Solver

**Erforderlich:**
- Truncation: Glueballpotential `V(ρ_G)` + Skalarpotential `U(ρ_S)` + Portal `ξ(ρ_S, ρ_G)`
- Gluon + Ghost-Sektor explizit (keine effektive Threshold-Näherung)
- Referenz: Pawlowski/Fischer/Gies (Prog.Part.Nucl.Phys. 74, 2014)
- Ziel: `|β(κ*, λ*, g*)| < 1e-14` am nicht-pert. Fixpunkt

**Erwarteter Aufwand:** Mehrwöchige numerische Studie (Gitter auf 3D-Kopplungsraum)

### S3-b: Nachweis β_g^ERGE = 0

Die Threshold-Struktur von β_g^ERGE unterscheidet sich fundamental von β_g^pert:

$$\beta_g^{\text{ERGE}} = -\frac{b_0^{\text{eff}}(\tilde{\kappa}, g^2)}{16\pi^2}\,g^4 + \text{Gluon-Ghost-Anomalie}$$

Der Gluon-Ghost-Beitrag zur anomalen Dimension η_A kann β_g^ERGE zum Verschwinden bringen, **aber nur wenn η_A = b₀·g²/(16π²) exakt**, was nur im vollen ERGE-System ohne LPA überprüft werden kann.

### S3-c: Vollständige Stabilitätsmatrix

Die LPA unterschätzt die kritischen Exponenten durch Vernachlässigung von:
- `η_A(k)`: anomale Dimension des Gluon-Feldes
- `η_S(k)`: anomale Dimension des Skalar-Feldes
- Vertex-Korrekturen der Portal-Kopplung ξ

---

## RG-Constraint-Status

Am numerischen LPA-Fixpunkt (nahe Gauss): `5κ²` ≈ 9.8e-14, `3λ_S` ≈ 5.3e-19.

**[RG_CONSTRAINT_FAIL]** bei (κ̃, λ_S) ≠ (0.5, 5/12).

Dies bestätigt: Der Ledger-Fixpunkt ist **kein** LPA-Fixpunkt, sondern muss durch eine truncation jenseits LPA stabilisiert werden.

---

## Evidenz-Klassifikation

| Aussage | Klasse | Begründung |
|---|---|---|
| β_g^pert < 0 für alle g > 0 (YM) | [A] | Gross-Politzer-Wilczek Theorem |
| UIDT-FP ist nicht-perturbativer ERGE-FP | [D] | Konsistent, nicht bewiesen |
| θ₁,₂ < 0 am Gauss'schen FP | [A] | Kanonische Analyse |
| θ₁,₂,₃ < 0 am nicht-pert. FP (κ*, λ*, g*) | [D] | Offen, erfordert S3-a,b,c |
| β_g^ERGE(g*,κ*,λ*) = 0 | [D] | Offen |

---

## Nächste Schritte

1. **S3-a**: Implementation eines vereinfachten ERGE-Solvers mit Gluon-Ghost-Truncation (Referenz: Fischer-Pawlowski 2009, Phys.Rev.D80:025023)
2. **S3-b**: Scan des (κ̃, g²)-Raums nach β_g^ERGE = 0 Nullfläche
3. **S3-c**: Eigenwert-Analyse der vollen 3×3 Stabilitätsmatrix mit η_A, η_S

**Bekannte Limitation:** Ohne Gitter-QCD-Verifikation der anomalen Dimensionen η_A(k) verbleibt die Evidenzklasse bei [D].
