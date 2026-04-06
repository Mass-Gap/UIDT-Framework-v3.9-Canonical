# Parameter Tension Note: v (Vacuum VEV)

> **Status:** [TENSION ALERT]  
> **Evidence Category:** [A] (canonical ledger value) vs [B] (older documents)

---

## The Tension

| Source | Value of v | Context | Evidence |
|--------|-----------|---------|----------|
| UIDT Ledger (v3.9 canonical) | **47.7 MeV** | Information-field VEV, calibrated to ΛQCD | [A] |
| Ultra Main Paper (2025) | **150 MeV** | Taken from lattice QCD input for ΛQCD scale | [B] |
| Master Report 2 (UIDT VI) | **47.7 MeV** | Consistent with Ledger | [A] |
| UIDT II / UIDT IV | ~150 MeV (implicit) | Used in intermediate mass gap steps | [B] |

**Absolute difference:** $|150 - 47.7| = 102.3$ MeV

---

## Root Cause Analysis

The two values refer to **physically distinct quantities**:

1. **v = 47.7 MeV** is the VEV of the UIDT information-density scalar field $S(x)$,
   calibrated via:
   $$\langle S \rangle = v = 47.7 \text{ MeV}, \quad m_S^2 = 2\lambda_S v^2$$
   This is an internal UIDT parameter determined by the RG fixed-point condition
   $5\kappa^2 = 3\lambda_S$ together with $m_S \approx \Delta^* = 1.710$ GeV.

2. **v = 150 MeV** appears in older documents as a proxy for $\Lambda_{\text{QCD}}$
   (the QCD scale), which is an *external* Standard-Model input, NOT the UIDT VEV.

**Conclusion:** The two values are NOT in physical conflict — they denote different
parameters. However, the labelling in older documents was ambiguous.

---

## Resolution

**Canonical rule (v3.9):**

- $v = 47.7$ MeV **always** refers to $\langle S \rangle$, the UIDT scalar VEV [A]
- $\Lambda_{\text{QCD}} \approx 0.1046$ GeV **always** refers to the QCD scale [Stratum I]
- These must NEVER be conflated in any equation or text

**Equations must be written as:**
$$\Delta^* = \gamma \cdot \Lambda_{\text{QCD}} \quad \text{(mass gap, using QCD scale)}$$
$$m_S = \sqrt{2\lambda_S} \cdot v \quad \text{(scalar mass, using UIDT VEV)}$$

---

## Impact on Older Documents

| Document | Issue | Resolution |
|----------|-------|------------|
| Ultra Main Paper §3.1 | Uses v=150 MeV for mass gap | Replace with $\Lambda_{\text{QCD}}$ notation |
| UIDT II §4 | Implicit v≈150 MeV | Clarify as $\Lambda_{\text{QCD}}$ input |
| UIDT IV §5 | Mixed notation | Add explicit subscripts |

> **MASS DELETION LOCK:** This note does NOT authorize modification
> of any existing code or equation. It is documentation only.
> Any equation changes require explicit author approval.

---

## Cross-References

- `LEDGER/parameter_ledger.md` — canonical parameter values
- `FORMALISM.md` — canonical Lagrangian
- `GLOSSARY.md` — v, ΛQCD entries
