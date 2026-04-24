"""
[UIDT-v3.9] Hybrid Verification: Spectral Gap Search (raumzeit ↔ UIDT)
Path A — Direct spectral gap validation via causal-set K7 measurements

DIMENSIONAL BRIDGE EQUATION: MISSING (TKT-FRG-BRIDGE-01 open)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
g_fc [dimensionless] <-> Δ* [GeV] mapping requires:

  1. N-scaling law: g_fc(N → ∞) → g_fc_inf
     Current assumption: g_fc_inf ≈ 1.710 (UNJUSTIFIED)

  2. Normalization: g_fc_inf / E_ref = Δ*
     where E_ref is undefined in emergent geometry framework

  3. Dimensional analysis gap:
     - g_fc: dimensionless (spectral dimension difference)
     - Δ*: energy [GeV]
     - No derivation bridging these in UIDT v3.9 canonical

Until TKT-FRG-BRIDGE-01 provides bridge equation:
  Evidence Category: [E] SPECULATIVE ONLY
  Upgrade path: [E] → [D] (post-reproduction with explicit bridge)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Claim: C-100: g_fc clustering signal
Evidence: [E] (Numerical coincidence, no dimensional justification)
Limitation: L4 (RG-flow derivation), PLUS dimensional bridge open
External: cblab/raumzeit (ID: 1207002944) [E-compatible only]
DOI: 10.5281/zenodo.17835200
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path
from typing import NamedTuple, Optional


# =====================================================================
# Canonical constants (read-only -- rule 03-canonical-constants.md)
# =====================================================================

import mpmath as mp
mp.dps = 80  # Constitution §3: local precision — do NOT centralize

DELTA_STAR_GEV = mp.mpf("1.710")      # +/- 0.015  [A]
DELTA_TOLERANCE = mp.mpf("0.015")     # 1-sigma canonical tolerance
GAMMA_INVARIANT = mp.mpf("16.339")    # [A-] calibrated, NOT derived
KAPPA = mp.mpf("0.500")               # +/- 0.008  [A]
LAMBDA_S = (mp.mpf("5") * KAPPA**2) / mp.mpf("3")
E_T_MEV = mp.mpf("2.44")              # [C] lattice torsion binding energy
V_MEV = mp.mpf("47.7")                # [A] vacuum expectation value


# =====================================================================
# Data structures
# =====================================================================

class SpectralGapMeasurement(NamedTuple):
    """Single K7 fixed-anchor measurement from raumzeit batch output.

    Field semantics follow diagnostics_k7.py :: measure_anchor() exactly:
        ds_global   -- spectral dimension of the full BFS region
        ds_core     -- spectral dimension of inner 50% by graph distance
        ds_mid      -- spectral dimension of middle 30%
        ds_front    -- spectral dimension of outer 20%
        g_fc        -- ds_front - ds_core  (the UIDT gap proxy)
        g_fm        -- ds_front - ds_mid
        g_mc        -- ds_mid   - ds_core
        iso_defect  -- branch isotropy coefficient-of-variation
        region_nodes-- number of nodes in the sampled BFS region
    """
    step: int
    anchor_id: int
    ds_global: Optional[float]
    ds_core: Optional[float]
    ds_mid: Optional[float]
    ds_front: Optional[float]
    g_fc: Optional[float]
    g_fm: Optional[float]
    g_mc: Optional[float]
    iso_defect: Optional[float]
    dv_global: Optional[float]
    region_nodes: int


class HybridVerificationResult(NamedTuple):
    """
    Stratum I/II observables ONLY.
    Stratum III interpretation (evidence category, UIDT mapping)
    belongs in report text, not here.
    """
    gap_proxy_mean: Optional[float]
    gap_proxy_std: Optional[float]
    gap_proxy_z_score: Optional[float]
    proximity_label: str
    n_measurements: int
    confidence: float


# =====================================================================
# I/O
# =====================================================================

def parse_k7_measurements(results_json: Path) -> list[SpectralGapMeasurement]:
    with open(results_json, encoding="utf-8") as fh:
        data = json.load(fh)

    raw_records = data.get("observables_k7", [])
    if not raw_records and isinstance(data, list):
        raw_records = data

    measurements: list[SpectralGapMeasurement] = []
    for rec in raw_records:
        measurements.append(SpectralGapMeasurement(
            step=int(rec.get("step", 0)),
            anchor_id=int(rec.get("anchor_id", -1)),
            ds_global=rec.get("ds_global"),
            ds_core=rec.get("ds_core"),
            ds_mid=rec.get("ds_mid"),
            ds_front=rec.get("ds_front"),
            g_fc=rec.get("g_fc"),
            g_fm=rec.get("g_fm"),
            g_mc=rec.get("g_mc"),
            iso_defect=rec.get("iso_defect"),
            dv_global=rec.get("dv_global"),
            region_nodes=int(rec.get("region_nodes", 0)),
        ))
    return measurements


# =====================================================================
# Validation engine
# =====================================================================

def validate_spectral_gap(measurements: list[SpectralGapMeasurement]) -> HybridVerificationResult:
    """Verify if g_fc is consistent with Δ* = 1.710 GeV."""
    mp.dps = 80

    valid_gaps = [m.g_fc for m in measurements if m.g_fc is not None]
    if len(valid_gaps) < 3:
        return HybridVerificationResult(
            gap_proxy_mean=None,
            gap_proxy_std=None,
            gap_proxy_z_score=None,
            proximity_label="INSUFFICIENT_DATA",
            n_measurements=len(valid_gaps),
            confidence=0.0,
        )

    mean_gap = statistics.mean(valid_gaps)
    std_gap = statistics.stdev(valid_gaps) if len(valid_gaps) > 1 else 0.0

    mean_gap_mpf = mp.mpf(str(mean_gap))
    std_gap_mpf = mp.mpf(str(std_gap)) if std_gap > 0 else mp.mpf("1e-6")

    deviation = abs(mean_gap_mpf - DELTA_STAR_GEV)
    z_score_mpf = (mean_gap_mpf - DELTA_STAR_GEV) / max(std_gap_mpf, mp.mpf("1e-6"))
    z_score = float(z_score_mpf)

    if deviation <= DELTA_TOLERANCE:
        proximity_label = "WITHIN_TOLERANCE"
        confidence = 0.85
    elif deviation <= mp.mpf("2") * DELTA_TOLERANCE:
        proximity_label = "NEAR_TOLERANCE"
        confidence = 0.60
    elif abs(z_score_mpf) < mp.mpf("2.0"):
        proximity_label = "MARGINAL"
        confidence = 0.40
    else:
        proximity_label = "OUTSIDE"
        confidence = 0.10

    return HybridVerificationResult(
        gap_proxy_mean=mean_gap,
        gap_proxy_std=std_gap,
        gap_proxy_z_score=z_score,
        proximity_label=proximity_label,
        n_measurements=len(valid_gaps),
        confidence=confidence,
    )


def _auxiliary_statistics(measurements: list[SpectralGapMeasurement]) -> str:
    lines = []

    ds_globals = [m.ds_global for m in measurements if m.ds_global is not None]
    if ds_globals:
        if len(ds_globals) > 1:
            lines.append(
                f"  ds_global    : {statistics.mean(ds_globals):.4f} +/- {statistics.stdev(ds_globals):.4f}"
            )
        else:
            lines.append(f"  ds_global    : {ds_globals[0]:.4f}")

    dv_globals = [m.dv_global for m in measurements if m.dv_global is not None]
    if dv_globals:
        if len(dv_globals) > 1:
            lines.append(
                f"  dv_global    : {statistics.mean(dv_globals):.4f} +/- {statistics.stdev(dv_globals):.4f}"
            )
        else:
            lines.append(f"  dv_global    : {dv_globals[0]:.4f}")

    iso_vals = [m.iso_defect for m in measurements if m.iso_defect is not None]
    if iso_vals:
        if len(iso_vals) > 1:
            lines.append(
                f"  iso_defect   : {statistics.mean(iso_vals):.4f} +/- {statistics.stdev(iso_vals):.4f}"
            )
        else:
            lines.append(f"  iso_defect   : {iso_vals[0]:.4f}")

    g_fm_vals = [m.g_fm for m in measurements if m.g_fm is not None]
    if g_fm_vals:
        lines.append(f"  g_fm (front-mid) : {statistics.mean(g_fm_vals):.4f}")

    g_mc_vals = [m.g_mc for m in measurements if m.g_mc is not None]
    if g_mc_vals:
        lines.append(f"  g_mc (mid-core)  : {statistics.mean(g_mc_vals):.4f}")

    return "\n".join(lines)


# =====================================================================
# Report generation
# =====================================================================

def report_verification(
    result: HybridVerificationResult,
    measurements: list[SpectralGapMeasurement] | None = None,
    output_file: Path | None = None,
) -> str:
    mean_str = f"{result.gap_proxy_mean:.4f}" if result.gap_proxy_mean is not None else "N/A"
    std_str = f"{result.gap_proxy_std:.4f}" if result.gap_proxy_std is not None else "N/A"
    z_str = f"{result.gap_proxy_z_score:+.2f}" if result.gap_proxy_z_score is not None else "N/A"

    if result.proximity_label == "WITHIN_TOLERANCE":
        evidence_category = "[E]"
        status = "WITHIN_TOLERANCE"
        interpretation = "SPECULATIVE NUMERICAL COINCIDENCE — dimensional bridge unresolved."
    elif result.proximity_label == "NEAR_TOLERANCE":
        evidence_category = "[E]"
        status = "NEAR_TOLERANCE"
        interpretation = "NEAR match, but still speculative because no bridge equation exists."
    elif result.proximity_label == "MARGINAL":
        evidence_category = "[E]"
        status = "MARGINAL"
        interpretation = "Moderate numerical proximity only; no evidential upgrade permitted."
    elif result.proximity_label == "INSUFFICIENT_DATA":
        evidence_category = "[E]"
        status = "INSUFFICIENT_DATA"
        interpretation = "Too few valid K7 measurements for any statistical statement."
    else:
        evidence_category = "[E]"
        status = "OUTSIDE"
        interpretation = "No numerical proximity to Δ* observed in current run."

    rg_lhs = mp.mpf("5") * KAPPA**2
    rg_rhs = mp.mpf("3") * LAMBDA_S
    rg_residual = abs(rg_lhs - rg_rhs)
    rg_status = "PASS" if rg_residual < mp.mpf("1e-14") else "[RG_CONSTRAINT_FAIL]"

    report = f"""
+================================================================+
|  UIDT-RAUMZEIT HYBRID VERIFICATION: PATH A (Spectral Gap)     |
+================================================================+

CANONICAL TARGET:
  Delta* = {mp.nstr(DELTA_STAR_GEV, 6)} +/- {mp.nstr(DELTA_TOLERANCE, 4)} GeV  [A]
  Source : UIDT v3.9 Banach Fixed-Point Proof (Theorem 1)

EMERGENT PROXY (raumzeit):
  g_fc   = ds(front) - ds(core)
  Method : K7 fixed-anchor diagnostics (random walker d_s)
  Config : v9a_fast.yaml (enable_v9_ball_coherence: true)

MEASUREMENT SUMMARY:
  Mean g_fc      : {mean_str}
  Std Dev        : {std_str}
  Z-score        : {z_str} sigma
  Valid samples  : {result.n_measurements}

CONSISTENCY CHECK:
  Status         : {status}
  Evidence Cat.  : {evidence_category}
  Confidence     : {result.confidence:.1%}

INTERPRETATION:
  {interpretation}

DIMENSIONAL BRIDGE STATUS:
  TKT-FRG-BRIDGE-01 remains open.
  g_fc is dimensionless; Delta* carries GeV units.
  No category upgrade above [E] is permitted in this script.
"""

    if measurements:
        aux = _auxiliary_statistics(measurements)
        if aux:
            report += f"\nAUXILIARY DIAGNOSTICS:\n{aux}\n"

    report += f"""
REFERENCES:
  UIDT Theory : DOI 10.5281/zenodo.17835200
  External Ref : cblab/raumzeit (ID: 1207002944)
  Config Pin   : commit 34c02567617b8aa0e3dcadbed57f3a16fe0c3cae
  K7 Diagnostic: diagnostics_k7.py :: measure_anchor()
  K2 Base      : diagnostics_k2.py :: _estimate_spectral_dimension()
  Config       : emergent-geometry-causal-graphs/configs/v9a_fast.yaml

RG FIXED-POINT CONSTRAINT (read-only verification):
  5*kappa^2          = {mp.nstr(rg_lhs, 20)}
  3*lambda_S         = {mp.nstr(rg_rhs, 20)}
  Residual           = {mp.nstr(rg_residual, 5)}
  Status             = {rg_status}
"""

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(report, encoding="utf-8")

    return report


# =====================================================================
# CLI entry point
# =====================================================================

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python hybrid_uidt_raumzeit_spectral_gap.py <results.json> [--output report.txt]")
        return 1

    results_path = Path(sys.argv[1])
    output_path: Path | None = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    if not results_path.exists():
        print(f"ERROR: file not found: {results_path}")
        return 2

    measurements = parse_k7_measurements(results_path)
    if not measurements:
        print("ERROR: no K7 measurements found in input file.")
        return 2

    result = validate_spectral_gap(measurements)
    report = report_verification(result, measurements, output_path)
    print(report)

    if result.proximity_label == "WITHIN_TOLERANCE":
        return 0
    elif result.proximity_label in ("NEAR_TOLERANCE", "MARGINAL"):
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
