# UIDT Gamma Derivation Program — Internal Whitepaper v0.1
# Status: [E] Working Document | Not for external citation
# Author: P. Rietz | Assisted: Perplexity/Sonnet | Date: 2026-03-15
# Language: English (repository standard)

---

## 1. Problem Statement

The UIDT Framework has a mathematically closed core for the spectral gap Δ*:
- Banach Fixed-Point Theorem proves existence and uniqueness of Δ* = 1.710 GeV [A]
- RG constraint 5κ² = 3λ_S holds with residual < 10⁻¹⁴ at 80 dps [A]

However, γ = 16.339 (Gamma Invariant) remains [A-]: phenomenologically calibrated
from the kinetic VEV definition. No derivation from first principles exists.

**Central open question (Limitation L4):**
Does γ = 16.339 follow uniquely from the UIDT field equations / SU(3) structure,
or is it an irreducible free parameter?

If γ can be derived: the UIDT core closes completely.
If not: the framework remains a constrained phenomenological model, not a proof.

---

## 2. Inventory of Gamma-Related Claims

All values from LEDGER/CLAIMS.json v3.9.0 + CANONICAL/CONSTANTS.md v3.9.4.

| Claim ID | Statement | Evidence | Status |
|----------|-----------|----------|--------|
| C-002 | γ = 16.339 (kinetic VEV) | A- | Calibrated — NOT derived |
| C-003 | γ_MC = 16.374 ± 1.005 | A- | Monte Carlo statistical mean |
| C-016 | γ from RG first principles | E | Open — perturbative RG gives γ* ≈ 55.8 |
| C-031 | γ = 16.339 exact (kinetic) | A- | Duplicate of C-002 for traceability |
| C-040 | γ from RG first principles | E | Duplicate of C-016 in v3.7.2 series |
| C-043 | γ_∞ = 16.3437 ± 0.0005 (L→∞) | B | Finite-size scaling extrapolation |
| C-052 | γ_SU3 = (2Nc+1)²/Nc = 49/3 ≈ 16.333 | E | SU(3) conjecture — 0.037% deviation |
| δγ | δγ = γ_∞ − γ_kin = 0.0047 | B | Vacuum dressing shift — real, reproducible |

**Key numerical fact:**
γ_kin = 16.339, γ_∞ = 16.3437, γ_SU3 = 49/3 = 16.3333...
All three lie within a 0.066% band. This is either:
(a) a deep algebraic relationship to be proven, or
(b) a coincidence to be disproven.

**IMPORTANT — z_FSS audit result (2026-03-15):**
- γ_kin vs γ_∞: z = 9.4σ at σ_∞=0.0005 — they are NOT the same within FSS uncertainty
- γ_SU3=49/3 vs γ_∞: z = 20.7σ — SU(3) conjecture is outside FSS band
- γ_kin vs γ_MC: z = 0.035σ — fully consistent ✓
- γ_SU3 vs γ_MC: z = 0.040σ — fully consistent ✓
- INTERPRETATION: The three γ values cluster numerically but are statistically
  distinct at the precision of γ_∞. The FSS band σ=0.0005 is the tightest
  constraint. Any derived γ must hit within z < 3 of γ_∞.

---

## 3. Candidate Derivation Routes

These are the structured search paths for γ derivation.
Status of each: [E] speculative until proven. LLM may assist in routes (i)-(iv) only.

### Route (i) — SU(3) Casimir / Algebraic [C-052 extension]
Conjecture: γ = (2Nc+1)²/Nc at Nc=3 from SU(3) color algebra.
- Current match: 49/3 = 16.333... vs γ=16.339 → Δ=0.006 (0.037%)
- Within γ_MC uncertainty band ✓, but outside γ_∞ FSS band (z=20.7σ) ✗
- Derivation needed: Show that the kinetic VEV operator, when evaluated in the
  SU(3) representation, yields exactly (2Nc+1)²/Nc.
- Alternative: Is the true formula (2Nc+1)²/Nc + correction(δγ) where
  δγ=0.0047 is the vacuum dressing shift?
- Key question: Which group-theoretic structure produces this combination?
  Candidates: C₂(adj)=N, dim(adj)=N²-1, ratio of Casimirs, ...

### Route (ii) — Banach Fixed-Point for γ [new]
Conjecture: γ satisfies an operator equation T(γ) = γ derived from the
UILT field equations (not from the Δ*-equation).
- Requires: explicit form of T(γ) from P. Rietz Lagrangian / field equations.
- LLM can help reformulate known equations into contraction form.
- mpmath can verify Lipschitz constant L < 1 if T is provided.

### Route (iii) — RG Flow Infrared Fixed Point [C-016 resolution]
The perturbative RG gives γ* ≈ 55.8 (wrong by factor ~3.4).
Question: Does a non-perturbative or resummed RG flow have a second
fixed point near γ = 16.339?
- This requires non-perturbative RG (functional RG / Wetterinck equation).
- LLM can structure the search, but equations must come from P. Rietz.

### Route (iv) — Dimensional / Scale Matching
γ appears in E_geo = Δ/γ = 104.66 MeV.
Known QCD scales: Λ_QCD ≈ 200-300 MeV, f_π ≈ 93 MeV.
Note: f_π = 92.9 MeV is close to E_geo = 104.66 MeV (ratio ≈ 1.127).
This is a [E] numerical observation only — requires P. Rietz to evaluate.

---

## 4. Falsification Criteria for each Route

Any proposed derivation of γ must simultaneously satisfy ALL of:

| Constraint | Required | Source |
|------------|----------|--------|
| γ_formal ≈ γ_kin | < 0.1% deviation | C-002 [A-] |
| γ_formal within 3σ_∞ of γ_∞ | z < 3 (σ_∞=0.0005) | C-043 [B] |
| γ_formal within 1σ of γ_MC | z < 1 (σ_MC=1.005) | C-003 [A-] |
| 5κ² = 3λ_S | residual < 10⁻¹⁴ | C-010 [A] |
| E_geo = Δ/γ_formal | ≈ 104.66 MeV | C-048 [C] |
| No circular argument | γ not used to derive γ | Constitution |

**Note from z_FSS audit:** The γ_∞ FSS band (σ=0.0005) is so tight that
the canonical γ_kin=16.339 itself fails it at z=9.4σ. This suggests that
either σ_∞ is underestimated, or γ_kin and γ_∞ are genuinely distinct
quantities (dressed vs. bare), and the derivation target should be γ_∞,
not γ_kin. **This distinction is a key open question for P. Rietz to resolve.**

---

## 5. Role of LLM vs. P. Rietz

| Task | LLM can do | P. Rietz must do |
|------|-----------|------------------|
| Enumerate algebraic candidates | ✓ | — |
| Reformulate equations into operator form | ✓ | provide equations |
| Compute symbolic traces / Casimir products | ✓ | verify |
| Write mpmath test code | ✓ | authorize |
| Run falsification battery | ✓ | review results |
| Declare a route proven | ✗ | exclusively |
| Assign evidence category A or A- | ✗ | exclusively (OPUS) |
| Modify Ledger γ value | ✗ | exclusively |

---

## 6. Next Concrete Steps

**Step 1 (done):** gamma_constraint_test.py deployed. Run it to verify baseline.

**Step 2 (P. Rietz):** Clarify whether derivation target is γ_kin or γ_∞.
  - If γ_kin: tolerance ±0.001 on derived value.
  - If γ_∞: the SU(3) conjecture 49/3 fails by z=20.7σ and must be abandoned.

**Step 3 (P. Rietz):** Provide explicit form of kinetic VEV operator O_kin.
  γ = <0|O_kin|0> / <normalization> — algebraic entry point for Route (i).

**Step 4 (LLM):** Evaluate SU(3) Casimir route against O_kin definition.
  Output: list of algebraic steps + mpmath verification.

**Step 5:** If Route (i) fails: proceed to Route (ii).
  Requires T(γ) from UIDT field equations (P. Rietz input).

**Step 6:** Surviving candidate → OPUS decision on evidence category.

---

## 7. Evidence Upgrade Path for γ

Current: γ = 16.339 [A-] (phenomenological)

[A-] → [B]: Derived from algebraic structure, z < 1 vs γ_MC, z < 3 vs γ_∞.
[B]  → [A]: Banach fixed-point proven, residual < 10⁻¹⁴ at 80 dps,
             independently reproduced by external auditor.

**Note:** The upgrade cannot be self-assigned. OPUS decision required.

---

*End of Whitepaper v0.1 — [E] Working Document*
*Key open question added 2026-03-15: Is derivation target γ_kin or γ_∞?*
*Next revision: after P. Rietz input on Step 2 + Step 3.*
