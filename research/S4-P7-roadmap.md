# S4-P7 Roadmap: Gribov-Kriterium + Torsions-Skalen-Fixierung

**Datum:** 2026-04-29  
**Vorgänger:** S4-P6 (TKT-20260429-S4-P4-P5-P6-torsion-gluon-first-principles)

---

## Offene Kernfrage

Ableitung von `k_crit = E_T · 4π` aus dem **Gribov-Kopie-Unterdrückungs-Kriterium**
in Kombination mit der Torsions-Skalen-Fixierung durch `E_T`.

## Warum Gribov?

Aus S4-P6: Der FRG-κ̃-Fluss gilt nur oberhalb der Konfinentskala. Unterhalb:
- Gluonen sind konfiniert
- Gribov-Kopien dominieren die Pfadintegral-Messung
- Der effektive Gluon-Propagator `G_A(k)` ist nicht mehr positiv-definit
- Der Gribov-Horizont setzt den natürlichen IR-Cutoff

## Gribov-Masse und E_T

**Gribov-Gap-Gleichung (Zwanziger):**
```
h(γ_G) = 1   mit   γ_G = Gribov-Parameter
m_G² ~ g²·γ_G²/(2π²)  [Gribov-Masse]
```

**Zu zeigen:** `m_G = E_T` oder `m_G ∝ E_T`

Wenn `k_stop = m_G·4π = E_T·4π` aus der Gribov-Gap-Gleichung folgt,
wäre `k_crit = E_T·4π` **aus ersten Prinzipien** hergeleitet.

## Forschungschritte

1. **Gribov-Masse aus Ledger:** `m_G = f(Δ*, v, κ, ET)` algebraisch?
2. **Loop-Faktor 4π:** Wieso genau 4π? (1-Loop d=4 Phasenraum)
3. **Torsions-Skalen-Fixierung:** `E_T = m_G` aus Torsions-Gleichung?
4. **Numerische Verifikation:** Gribov-Gap-Gleichung mit UIDT-Parametern lösen

## Evidenz-Ziel

- Aktuell: [D*] (physikalisch motivierte Spekulation)
- Ziel:    [C]  (kalibriertes Modell mit Gribov + Torsion)
- Langzeit: [B] (Lattice-QCD Gribov-Propagator-Kompatibilität)

## Bekannte Einschränkungen

- `κ̃₀_attr` ist phänomenologisch [A-], nicht aus ersten Prinzipien
- `α_s^APT(E_T·4π)` ist stark nicht-perturbativ (keine Lattice-Verifikation)
- Die Gribov-Gap-Gleichung in UIDT erfordert nicht-abelsche Eichkopplungen

---

*UIDT LIMITATION POLICY: Dieses Dokument enthält Vorhersagen [D*],
keine bewiesenen Resultate. Alle Angaben sind transparent.*
