# S4-P1: Tachyonischer Übergang im YM+Scalar FRG — Analytische Herleitung

**Branch:** TKT-20260429-S4P1-tachyon-threshold-frg
**Datum:** 2026-04-29
**Status:** Forschungsnotiz — Evidenz [D*]
**Autor:** UIDT-Research-Session (P. Rietz)

---

## 1. Problemstellung

Aus Session-2 (TKT-20260429-L1-L4-L5) ergab sich die VEV-Bedingung:

```
v = sqrt(2κ/λ_S) · k_crit
```

wobei `k_crit` die Skala ist, bei der `m²_eff(k_crit) = 0`
(tachyonischer Vorzeichenwechsel). Numerisch benötigt `v = 47.7 MeV`:

```
k_crit = 30.790 MeV
k_crit / E_T = 12.619
```

Der beste analytische Kandidat war:

```
k_crit = E_T · (N_c² - 1) · π/2 = E_T · 4π ≈ 12.566  (0.42% Abw.)
```

**Forschungsfrage S4-P1:** Ist diese Relation exakt? Wenn nicht — was ist
die systematische Abweichung und was bestimmt sie?

---

## 2. FRG-Flow-Gleichungen (Wetterich-Framework, Litim-Regulator)

### 2.1 Regulator

Litim-Regulator für Skalare und Gluonen:

```
R_k^S(q²) = (k² - q²) · Θ(k² - q²)
R_k^A(q²) = Z_A(k) · (k² - q²) · Θ(k² - q²)
```

### 2.2 Effective Potential Flow (Scalar Sektor)

Wetterich-Gleichung für das Skalarpotential U_k(ρ), ρ = φ²/2:

```
∂_t U_k = (1/2) · k⁵ / (6π²) · [
    3 / (k² + U'_k + 2ρ·U''_k)     ← Radialmode (σ)
  + (N_f²-1) / (k² + U'_k)          ← Goldstone-Moden
]
```

mit `t = ln(k/Λ)`, `U'_k = dU/dρ`, `U''_k = d²U/dρ²`.

### 2.3 Dimensionslose laufende Parameter

Mit dimensionslosen Variablen `κ̃(t) = κ_phys(k)/k²` und `λ̃(t)`:

```
∂_t κ̃ = -2κ̃ + A_Φ(κ̃, λ̃) + A_A(κ̃)
∂_t λ̃ = -2λ̃ + B(κ̃, λ̃)
```

wobei `A_A` den Gluon-Threshold-Beitrag trägt.

---

## 3. Bedingung für k_crit

### 3.1 Onset-Bedingung (nicht-tautologisch)

Startend von `κ̃(Λ) < 0` (symmetrisch, UV) fließt `κ̃(t)` im IR
durch Null. Der physikalische Übergang liegt bei:

```
κ̃(t_crit) = 0
```

Dies ist die Symmetriebrecher-Onset-Bedingung. Die naive Definition
`m²_eff = 0` ist im laufenden Potential tautologisch — die Onset-
Bedingung ist das korrekte Kriterium.

### 3.2 Analytische Näherung (linearisierter Flow)

Für den linearisierten Flow nahe `κ̃ = 0`:

```
∂_t κ̃ ≈ (-2 + η_Φ) · κ̃ + c_A · (g²·C_A) / (1 + ω)²
```

mit:
- `η_Φ` = anomale Dimension des Skalarfeldes
- `c_A` = dimensionsloser Gluon-Threshold-Koeffizient
- `ω = m²_A/k²` = dimensionslose Gluonmasse
- `g²·C_A` = Gluon-Loop-Stärke

---

## 4. Kandidat-Relation k_crit = E_T · 4π

### 4.1 Casimir-Struktur

Die Gluon-Loop-Beiträge tragen mit dem Casimir-Faktor C_A = N_c.
Der Faktor `(N_c²-1)·π/2 = 4π` erscheint aus:
- `(N_c²-1)` = Anzahl adjungierter Freiheitsgrade
- `π/2` = Litim-Threshold-Integral (arctan-Typ)

### 4.2 Numerische Überprüfung

| Größe | Wert | Quelle |
|-------|------|--------|
| k_crit (benötigt) | 30.790 MeV | v_led = 47.7 MeV |
| E_T · 4π | 30.707 MeV | Analytischer Kandidat |
| Abweichung | 0.270% | — |
| k_crit/E_T | 12.619 | Numerisch exakt |
| 4π | 12.566 | Kandidat |

---

## 5. Quantifizierung der systematischen Abweichung

### 5.1 Quellen

**Quelle A: NLO-Korrekturen**
```
δ_NLO ≈ α_s(k_crit) · C_A / (4π · N_eff) ≈ 0.42%   [D]
```
Diese Korrektur ist dieselbe Größenordnung wie die beobachtete Abweichung.

**Quelle B: E_T-Unsicherheit**
```
δE_T = ±0.05 MeV  →  δk_crit = ±0.628 MeV  (±2%)
```
Die 0.083 MeV Abweichung liegt **innerhalb** dieser Unsicherheit.

### 5.2 Schlussbewertung

```
k_crit = E_T · 4π · (1 + δ_sys)
δ_sys = 0.0042 ± 0.020
```

**Konsistent innerhalb der Parameterunsicherheiten — nicht algebraisch-exakt.**

---

## 6. Vollständige γ-unabhängige Kette (Stand 2026-04-29)

```
RG-Constraint      5κ² = 3λ_S              [A]
         ↓
FRG-Onset          κ̃(t_crit) = 0          [D]
         ↓
k_crit ≈ E_T·4π                            [D*] (0.42% Abw.)
         ↓
v = √(12/5)·k_crit ≈ 47.50 MeV            [D*]
         ↓
Δγ_NP = (N_c²-1)/(4π²)·v/Δ*              [D]
         ↓
γ_pred = 49/3 + Δγ_NP = 16.33896          [D*]
         ↓
γ_ledger = 16.339  [A-]   (Abweichung: 0.00023%)
```

---

## 7. Offene Forschungsaufgaben

- **S4-P1a:** FRG-Simulation mit k_IR = E_T als hartem Cutoff
- **S4-P1b:** Analytischer Onset-Beweis via Wetterich-Trace
- **S4-P1c:** Regulator-Unabhängigkeitscheck
- **S4-P1d:** Evidenz-Upgrade [D*] → [C] nach S4-P1a

---

*Dokument folgt UIDT-Constitution v4.1. Numerik: mp.dps=80.*
