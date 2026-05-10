# Independent Reproduction Protocol

**Status: Open invitation**  
**Maintainer: P. Rietz**  
**Last reviewed: 2026-05-10**

---

## 1. Motivation

All current numerical verification uses the UIDT Python implementation under `core/` and
`modules/`.  LLM-based audits and internal Docker verification are *not* substitutes for
independent reproduction.  This protocol defines what "independent reproduction" means and
how external contributors can carry it out.

---

## 2. Reproduction Rules

1. Do **not** copy any file from this repository into your reproduction.
2. Derive every equation from the published manuscript (arXiv / Zenodo DOI listed in CITATION.cff).
3. Use a different programming language (Julia, C++, Mathematica, or Fortran acceptable).
4. Use 50+ significant digits (e.g., Julia `BigFloat`, C++ `__float128`, Mathematica arbitrary precision).
5. Report residuals in the format specified in Section 4.

---

## 3. Target Quantities

| Quantity | UIDT value | Tolerance | Source equation |
|----------|-----------|-----------|----------------|
| Δ* (mass-gap) | 1.710 GeV | ± 0.015 GeV | Eq. (3.14) in v3.7.1 |
| γ (kinetic vacuum parameter) | 16.339 | ± 0.005 | Eq. (4.7) |
| ET (torsion binding energy) | 2.44 MeV | ± 0.05 MeV | Eq. (5.3) |
| RG fixed-point: 5κ² − 3λS | 0 | < 1e-14 | Eq. (6.2) |
| Banach contraction rate L | ≈ 3.7×10⁻⁵ | < 1e-4 | Theorem 3.1 |

---

## 4. Reporting Format

Open a GitHub Issue with label `independent-reproduction` and include:

```
Language / library:   <e.g. Julia 1.10, BigFloat>
Precision digits:     <e.g. 64>
Δ* reproduced:        <value ± uncertainty>
γ reproduced:         <value>
ET reproduced:        <value MeV>
RG residual:          <|5κ²−3λS|>
Banach L reproduced:  <value>
Method notes:         <brief description of your approach>
Code repository:      <URL or attachment>
```

---

## 5. Milestones

| Milestone | Description | Status |
|-----------|-------------|--------|
| M-IR-1 | First external reproduction (any language) | ⬜ Open |
| M-IR-2 | Reproduction by a lattice QCD practitioner | ⬜ Open |
| M-IR-3 | Formal mathematical review of Theorem 3.1 | ⬜ Open |
| M-IR-4 | Published independent result citing UIDT | ⬜ Open |

---

## 6. LLM Audit Scope (Clarification)

LLM-based audits are permitted **only** for:
- Dimensional consistency checks
- Algebraic identity verification
- Literature search and citation checking
- Code linting and structure review

LLM audits do **not** constitute independent reproduction and must never be cited as such.
