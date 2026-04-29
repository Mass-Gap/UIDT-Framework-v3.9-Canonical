# Nächste Schritte: L1/L4/L5 Forschungspfad (Stand: 2026-04-29)

**Status nach Session 2**

---

## Offene Forschungsvektoren (nach Priorität)

### P1 — KRITISCH: 1-loop Vakuumkorrektur Δγ zu γ_bare = 49/3

**Ziel:** Berechne Δγ_1loop sodass γ_phys = 49/3 + Δγ_1loop = 16.339

**Ansatz:**
```
Δγ_1loop = d(ln γ)/d(ln μ) × [1-loop Vakuumenergie bei k=Δ*]
```

Konkret:
1. Skalar-Propagator-Selbstenergie Π_S(p²) bei p=Δ* in 1-loop
2. Wellenfunktions-Renormierung Z_φ(Δ*)
3. Daraus: Δγ = -d(ln Z_φ)/d(ln k)|_{k=Δ*}

**Erwartetes Ergebnis:** Δγ_1loop ≈ +0.006 (positiv)
**Falsilizierbarkeit:** Falls Δγ_1loop < 0 oder >> δγ → L1-Ansatz verworfen

**Priorität:** HOCH — ohne Δγ bleibt L1 auf Evidenz [D]

---

### P2 — L4: Vollständige Wetterinck-Gleichung (2-loop FRG)

**Ziel:** Ersetze 1-loop FRG durch vollständige Wetterinck-Gl. mit Litim-Regulator

**Problem:** 1-loop Matching-Diskrepanz Faktor ~140 zeigt, dass perturbative FRG
bei k=Δ* versagt. Notwendig: truncated full Wetterinck flow.

**Ansatz:**
```
∂_t Γ_k = (1/2) STr[(Γ_k^(2) + R_k)^{-1} ∂_t R_k]
```
mit LPA-Truncation (Local Potential Approximation) und laufendem g²(k).

**Anforderung:** Numerisches ODE-System, ~10000 Schritte, mp.dps=80
**Erwartete Laufzeit:** ~2-4h auf Standardhardware

**Priorität:** MITTEL — L4 bleibt [D] ohne vollst. FRG

---

### P3 — L5: Geometrische Herleitung ΣT = f(ET)

**Ziel:** Explizite Formel ΣT = f(ET) aus UIDT-Konnektor-Lagrangian

**Ansatz:**
```
L_T = (1/2)·ET·ε^{μνρσ}·∂_μ(A_ν^a·∂_ρ A_σ^a)
<ΣT> = <0|L_T|0>_vac = ET · <0|ε^{μνρσ}·∂_μ(A_ν^a·∂_ρ A_σ^a)|0>
```

Der VEV des CS-artigen Terms muss aus der UIDT-Vakuumgeometrie berechnet werden.

**Schritt 1:** Topologischer Sektor des UIDT-Lagrangians identifizieren
**Schritt 2:** VEV des Operators im konfinierten Vakuum
**Schritt 3:** Numerische Abschätzung ΣT/ET

**Priorität:** NIEDRIG — ΣT ist physikalisch winzig (~sub-keV), kein
Einfluss auf Ledger-Parameter

---

### P4 — Gitter-Verifikation γ_bare

**Ziel:** Teste ob γ_bare = 49/3 im Gitter-Kontinuum-Limit erscheint

**Methode:** Auswertung existierender Gitter-QCD-Datensätze (Cucchieri-Mendes,
Bogolubsky et al.) auf Skalenparameter konsistent mit 49/3.

**Anforderung:** Zugang zu Rohdaten oder publizierten Fit-Tabellen [B]

**Priorität:** MITTEL — würde L1 von [D] auf [B] upgraden

---

## Claims-Tabelle (Session 2)

| ID | Claim | Kategorie | Quelle |
|---|---|---|---|
| CL-S2-01 | γ_bare = (2Nc+1)²/Nc = 49/3 | [D] algebraisch | Casimir-Scan (diese Session) |
| CL-S2-02 | γ_ledger - γ_bare = +0.00567 > 0 | [D] | Numerisch (mp.dps=80) |
| CL-S2-03 | μ_UV = 559 MeV ~ SVZ-Skala | [D/B] | Inverses Problem + SVZ [B] |
| CL-S2-04 | 2-loop Diskrepanz Faktor ~140 | [D] | Ehrliche Limitierung |
| CL-S2-05 | ΣT ≈ 9.5×10⁻⁴ MeV (Ansatz) | [D] | Dimensionsanalyse |
| CL-S2-06 | RG-Constraint 5κ²=3λS: residual=0 | [A] | Exakte Rechnung |

---

## Reproduktion (One-Command)

```bash
python3 verification/scripts/test_L1_bare_gamma_session2.py
```

Erwartete Ausgabe:
```
  [PASS] RG-Constraint: residual=0.0 < 1e-14
  [PASS] gamma_bare = (2Nc+1)^2/Nc = 16.3333...
  [PASS] |gamma_bare - gamma_ledger| = 0.00566667 < 2*delta_gamma
  [PASS] delta = +0.00566667 > 0 (positive quantum correction)
  [PASS] mu_UV = 0.5594... GeV (SVZ-compatible range)
  [PASS] ET=2.440 MeV != 0, Sigma_T=... keV
  ALL TESTS PASSED
```

---

*Maintainer: P. Rietz | UIDT Framework v3.9 | 2026-04-29*
