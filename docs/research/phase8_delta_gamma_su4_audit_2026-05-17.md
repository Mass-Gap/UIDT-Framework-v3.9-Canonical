# Phase 8 Delta-Gamma / SU(4) Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-17  
> **Branch:** `TKT-2026-05-17-phase8-research-delta-gamma-su4`  
> **Stacked on:** PR #459 / `TKT-2026-05-17-session2-ledger-sync-phase8`  
> **DOI:** `10.5281/zenodo.17835200`  
> **Status:** Research audit. No evidence-category promotion.  

---

## Abstract

This audit executes the first Phase-8 research pass after the Session-2 ledger sync corrections staged in PR #459. It uses the corrected assumptions:

\[
\gamma_{\mathrm{bare}}(N_c)=\frac{(2N_c+1)^2}{N_c},\qquad \gamma_{\mathrm{bare}}(3)=\frac{49}{3},
\]

and

\[
k_{\mathrm{crit}} = 4\pi E_T = 30.661944299036382\ldots\,\mathrm{MeV}
\]

for canonical \(E_T=2.44\,\mathrm{MeV}\) [C]. The audit documents three results:

1. The required correction from \(49/3\) to \(\gamma=16.339\) [A-] is exactly \(17/3000\) [D].
2. A minimal perturbative ansatz \(\Delta\gamma=C\alpha_s/(4\pi)\) would require \(C\approx0.2184\) for \(\alpha_s=0.326\), which is scale-plausible but not derived [D].
3. The corrected S4-P1 chain yields \(\gamma_{\mathrm{pred}}=16.338962439648224\ldots\), missing \(\gamma\) by \(3.7560\times10^{-5}\), hence a partial numerical hit [D], not an [A] closure.

The SU(4) cross-check gives \(\gamma_{\mathrm{bare}}^{SU(4)}=81/4=20.25\) [D]. It also exposes a new N-definition tension: the handover-style rule \(N_{SU(4)}=16\cdot11=176\) conflicts with the pure-YM one-loop coefficient \(b_0(SU(4))=44/3\), which gives \(N_{SU(4)}=704/3\). This is a `[TENSION ALERT]` and must be resolved before using SU(4) to promote the L1 ansatz.

---

## Stratum I — Empirical / External Anchors

No new external numerical lattice datum is promoted in this audit. The SU(4) step is an internal falsification design, not a lattice-data extraction.

A targeted RAG pass over saved literature candidates found these source-backed anchors:

| Source-backed item | Status in this audit | Use |
|---|---|---|
| B. Lucini, M. Teper, U. Wenger, *Glueballs and k-strings in SU(N) gauge theories*, JHEP 06 (2004) 012, arXiv:hep-lat/0404008 | identified as key SU(N) glueball reference | future SU(4) table extraction |
| A. Athenodorou, M. Teper, *SU(N) gauge theories in 3+1 dimensions: glueball spectrum, string tensions and topology*, JHEP 12 (2021) 082, arXiv:2106.00364 | identified as modern SU(N) glueball reference | future SU(4) continuum comparison |
| Bonanno / D'Elia / Lucini / Vadacchino large-N glueball/topology works | identified as follow-up family | not used for numeric promotion |
| ResearchGate / non-peer-reviewed mass-gap PDFs | ignored for promotion | not used |

The RAG result provided references but not a clean SU(4) continuum table in this pass. Therefore no [B] lattice claim is made.

---

## Stratum II — Standard Field-Theory Context

For pure Yang-Mills, the conventional one-loop beta-function coefficient scales as

\[
b_0(N_c)=\frac{11N_c}{3}.
\]

Thus, for SU(3), \(b_0=11\), but for SU(4), \(b_0=44/3\). Any SU(4) extrapolation using a fixed value \(b_0=11\) must be explicitly marked as a UIDT-internal convention rather than the standard pure-YM coefficient.

This distinction is the source of the Phase-8 SU(4) N-definition tension.

---

## Stratum III — UIDT Research Results

### P1a — Required correction from corrected γ_bare

Using

\[
\gamma_{\mathrm{bare}}(3)=\frac{49}{3}
\]

and

\[
\gamma_{\mathrm{ledger}}=16.339,
\]

one obtains

\[
\Delta\gamma_{\mathrm{required}}
= \gamma_{\mathrm{ledger}}-\gamma_{\mathrm{bare}}
= 16.339-\frac{49}{3}
= \frac{17}{3000}
=0.005666666666666666\ldots.
\]

**Evidence:** [D] Stratum III. This is exact arithmetic conditional on the conjecture, not a first-principles QFT derivation.

### P1b — Minimal perturbative coefficient scale audit

Assume only as a scale audit:

\[
\Delta\gamma=C\frac{\alpha_s}{4\pi}.
\]

For \(\alpha_s(1.5\,\mathrm{GeV})=0.326\), the required coefficient is

\[
C=\Delta\gamma_{\mathrm{required}}\frac{4\pi}{\alpha_s}
=0.21843384503487314950\ldots.
\]

Additional normalisations:

\[
\Delta\gamma=C\frac{\alpha_s}{\pi}\quad\Rightarrow\quad C=0.05460846125871828737\ldots,
\]

\[
\Delta\gamma=C\frac{\alpha_s}{16\pi^2}\quad\Rightarrow\quad C=2.74492065142771528049\ldots.
\]

**Interpretation:** These coefficients are not absurdly large. However, no Feynman-diagram self-energy calculation has produced them. Therefore this is **scale-consistent but not derived** [D].

### P1c — Corrected S4-P1 non-perturbative chain

Using canonical \(E_T=2.44\,\mathrm{MeV}\) [C]:

\[
k_{\mathrm{crit}}=4\pi E_T
=30.6619442990363820073953994208079481497643733379010328127154592209242881253534\,\mathrm{MeV}.
\]

Then

\[
v_{\mathrm{S4P1}}=\sqrt{\frac{12}{5}}k_{\mathrm{crit}}
=47.501279853002942537113076541729462153073066147889843469285377735931108003048118\,\mathrm{MeV}.
\]

With \(N_c=3\) and \(\Delta^*=1710\,\mathrm{MeV}\):

\[
\Delta\gamma_{\mathrm{NP}}
=\frac{N_c^2-1}{4\pi^2}\frac{v_{\mathrm{S4P1}}}{\Delta^*}
=0.0056291063148914508559664078229635937676831402645376636439130762614790187510676005.
\]

Thus

\[
\gamma_{\mathrm{pred}}
=\frac{49}{3}+\Delta\gamma_{\mathrm{NP}}
=16.338962439648224784189299741156296927101016473597870996977246409594812352084401.
\]

Residual:

\[
|\gamma_{\mathrm{pred}}-16.339|
=0.000037560351775215810700258843703072898983526402129003022753590405187647915599098885.
\]

The ratio to the required correction is

\[
\frac{\Delta\gamma_{\mathrm{NP}}}{\Delta\gamma_{\mathrm{required}}}
=0.99337170262790309222936608640534007664996592903605829010230757555512095607075002.
\]

**Interpretation:** This is a partial numerical hit [D]. The residual is larger than \(10^{-14}\), so it is not [A]. It is below \(10^{-3}\), so it remains worth retaining as a Phase-8 research vector.

### P5 — SU(4) cross-check

Corrected formula:

\[
\gamma_{\mathrm{bare}}(4)=\frac{(2\cdot4+1)^2}{4}=\frac{81}{4}=20.25.
\]

This is algebraically consistent with the corrected denominator.

However, the proposed SU(4) step-number extension is not yet internally consistent.

Handover-style convention:

\[
N_{SU(4)}=16\cdot11=176.
\]

Pure-YM beta coefficient:

\[
b_0(SU(4))=\frac{44}{3}.
\]

Then

\[
N_{SU(4)}=16\cdot\frac{44}{3}=\frac{704}{3}=234.666666666666\ldots.
\]

Difference:

\[
\frac{704}{3}-176=\frac{176}{3}=58.666666666666\ldots,
\]

relative difference:

\[
\frac{1}{3}=33.333333333333\ldots\%.
\]

**Status:** `[TENSION ALERT]`. SU(4) cannot be used for claim promotion until the N-definition is fixed.

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|---|
| P8-P1A-001 | Corrected SU(3) bare-gamma conjecture | \(49/3\) | [D] | III | `verify_phase8_delta_gamma_su4_audit.py` | PASS | Fails if denominator is forced to \(N_c^2\). |
| P8-P1A-002 | Required correction | \(17/3000\) | [D] | III | script | PASS | Fails L1 if physical correction is negative or >0.012. |
| P8-P1B-001 | One-loop coefficient scale under \(\alpha_s/(4\pi)\) ansatz | \(C=0.2184338450\ldots\) | [D] | III | script | SCALE-CONSISTENT | Not a derivation; requires explicit diagrammatic computation. |
| P8-P1C-001 | Corrected S4-P1 \(\Delta\gamma_{NP}\) | \(0.0056291063\ldots\) | [D] | III | script | PARTIAL HIT | Fails if full Wetterich flow does not reproduce shift. |
| P8-P1C-002 | Corrected S4-P1 \(\gamma_{pred}\) | \(16.338962439648224\ldots\) | [D] | III | script | PARTIAL HIT | Not [A]; residual > \(10^{-14}\). |
| P8-P5-001 | SU(4) bare-gamma prediction | \(81/4=20.25\) | [D] | III | script | PASS | Fails if SU(4) lattice observable contradicts scaling. |
| P8-P5-002 | SU(4) N-definition conflict | 176 vs 704/3 | [E]/TENSION | III | script + standard beta coefficient | OPEN | Must resolve before SU(4) is used for promotion. |

---

## Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_delta_gamma_su4_audit.py
```

Expected terminus:

```text
ALL PHASE-8 DELTA-GAMMA / SU4 AUDIT CHECKS PASSED
```

---

## Verified References

| DOI/arXiv/PR | Status | Used for | Evidence Tag |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT canonical identity | n/a |
| PR #459 | open / draft | corrected Phase-8 assumptions | [D] context |
| PR #367 | merged repository PR | Session-2 γ_bare context | [D] |
| PR #369 | merged repository PR | S4-P1 tachyon chain | [D] |
| PR #362 | merged repository PR | `[NO-GO-STEP5]` | [D] |
| PR #358 | merged repository PR | L1/L4/L5 no-go constraints | [D/E] context |
| JHEP 06 (2004) 012 / arXiv:hep-lat/0404008 | identified in RAG pass | future SU(N)/SU(4) glueball extraction | no promotion |
| JHEP 12 (2021) 082 / arXiv:2106.00364 | identified in RAG pass | future modern SU(N) benchmark extraction | no promotion |

No external [B] claim is made in this audit.

---

## Acceptance Status

`[PARTIAL PASS / NO-GO MIXED]`

- P1 is **not complete**: no first-principles 1-loop self-energy calculation exists yet.
- The perturbative coefficient scale is plausible but not derived.
- S4-P1 remains the strongest numerical vector, but only [D].
- SU(4) formula scaling is algebraically coherent for γ_bare.
- SU(4) N scaling has a 33.33% definition tension and is blocked for promotion.

---

## Next Logical Steps

1. Perform the explicit scalar self-energy calculation \(\Pi_S(p^2)\) at \(p=\Delta^*\), rather than only coefficient-scale auditing.
2. Resolve the SU(4) N-definition: fixed \(b_0=11\) convention vs pure-YM \(b_0=11N_c/3\).
3. Extract actual SU(4) continuum glueball values from peer-reviewed SU(N) lattice tables.
4. Run regulator-independence checks for S4-P1 using the corrected \(k_{crit}=30.6619442990\ldots\,\mathrm{MeV}\).
