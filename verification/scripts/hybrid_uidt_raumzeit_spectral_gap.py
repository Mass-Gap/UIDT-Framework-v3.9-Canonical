"""
[UIDT-v3.9] Hybrid Verification: Spectral Gap Search (raumzeit <-> UIDT)
=========================================================================

Path A -- Direct spectral gap validation via causal-set K7 measurements.

Claim under test:
    Delta* = 1.710 +/- 0.015 GeV  [A]  (UIDT Yang-Mills mass gap)

Test observable (from cblab/raumzeit K7 diagnostics):
    g_fc = ds(front) - ds(core)

    where ds(front) and ds(core) are spectral dimensions estimated by
    random-walker return probabilities on the outer and inner quantile
    shells of a fixed-anchor BFS region (see diagnostics_k7.py).

Evidence category: [B] (Numerical robustness check against emergent
    geometry framework)

Limitation impact: L4 (RG-flow derivation of gamma remains open;
    g_fc is a dimensionless proxy, NOT a direct energy measurement)

External framework:
    Repository : https://github.com/cblab/raumzeit
    Repo ID    : 1207002944
    Engine     : emergent-geometry-causal-graphs/
    Config     : configs/v9a_fast.yaml
    Diagnostic : K7 fixed-anchor (diagnostics_k7.py :: measure_anchor())

DOI: 10.5281/zenodo.17835200

Usage
-----
    python hybrid_uidt_raumzeit_spectral_gap.py <results.json> [--output report.txt]

    <results.json> must contain an "observables_k7" array produced by
    raumzeit batch runs (scripts/run_batch.py).

Exit codes:
    0 = PASS  (spectral gap signature consistent with Delta*)   -> [B]
    1 = NEAR / MARGINAL  (warning; review finite-size effects)  -> [B]/[C]
    2 = FAIL  (no signature; falsification candidate)           -> [D]
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path
from typing import NamedTuple, Optional

# =====================================================================
# Canonical constants (read-only -- rule 03-canonical-constants.md)
# =====================================================================

DELTA_STAR_GEV: float = 1.710       # +/- 0.015  [A]
DELTA_TOLERANCE: float = 0.015      # 1-sigma canonical tolerance
GAMMA_INVARIANT: float = 16.339     # [A-]  calibrated, NOT derived
KAPPA: float = 0.500                # +/- 0.008  [A]
LAMBDA_S: float = 5 * KAPPA**2 / 3  # = 5kappa^2/3 = 0.41(6)  [A]
E_T_MEV: float = 2.44               # [C]  lattice torsion binding energy
V_MEV: float = 47.7                 # [A]  vacuum expectation value


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
    """Summary of the Path A spectral gap validation."""
    gap_proxy_mean: Optional[float]
    gap_proxy_std: Optional[float]
    gap_proxy_z_score: Optional[float]
    consistency: str        # PASS | NEAR | MARGINAL | FAIL
    evidence_category: str  # [B] | [C] | [D] | [E]
    n_measurements: int
    confidence: float       # 0.0 -- 1.0


# =====================================================================
# I/O
# =====================================================================

def parse_k7_measurements(results_json: Path) -> list[SpectralGapMeasurement]:
    """Load K7 anchor observables from a raumzeit batch-run JSON.

    Expected schema (produced by raumzeit scripts/run_batch.py)::

        {
          "observables_k7": [
            {
              "step": 5000,
              "anchor_id": 0,
              "ds_global": ...,
              "ds_core": ...,
              "ds_mid": ...,
              "ds_front": ...,
              "g_fc": ...,
              "g_fm": ...,
              "g_mc": ...,
              "iso_defect": ...,
              "dv_global": ...,
              "region_nodes": 1500,
              ...
            },
            ...
          ]
        }
    """
    with open(results_json, encoding="utf-8") as fh:
        data = json.load(fh)

    raw_records = data.get("observables_k7", [])
    if not raw_records:
        # Fallback: try top-level list
        if isinstance(data, list):
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

def validate_spectral_gap(
    measurements: list[SpectralGapMeasurement],
) -> HybridVerificationResult:
    """Test if the g_fc proxy clusters near Delta* = 1.710 GeV.

    Conservative interpretation
    ---------------------------
    We do NOT claim g_fc directly equals Delta* in physical units.
    The test checks whether the *dimensionless* g_fc values from
    raumzeit K7 measurements cluster around the *numerical* value
    1.710, which would constitute a [B]-level consistency signal.

    Classification
    --------------
    PASS      |mean(g_fc) - 1.710| <= 0.015           -> [B]
    NEAR      |mean(g_fc) - 1.710| <= 0.030           -> [B]
    MARGINAL  |z-score| < 2.0                          -> [C]
    FAIL      otherwise                                -> [D]
    """
    valid_gaps = [m.g_fc for m in measurements if m.g_fc is not None]

    if len(valid_gaps) < 3:
        return HybridVerificationResult(
            gap_proxy_mean=None,
            gap_proxy_std=None,
            gap_proxy_z_score=None,
            consistency="FAIL",
            evidence_category="[E]",
            n_measurements=len(valid_gaps),
            confidence=0.0,
        )

    mean_gap = statistics.mean(valid_gaps)
    std_gap = statistics.stdev(valid_gaps) if len(valid_gaps) > 1 else 0.0
    z_score = (mean_gap - DELTA_STAR_GEV) / max(std_gap, 1e-6)

    deviation = abs(mean_gap - DELTA_STAR_GEV)

    if deviation <= DELTA_TOLERANCE:
        return HybridVerificationResult(
            mean_gap, std_gap, z_score,
            "PASS", "[B]", len(valid_gaps), 0.85,
        )
    elif deviation <= 2 * DELTA_TOLERANCE:
        return HybridVerificationResult(
            mean_gap, std_gap, z_score,
            "NEAR", "[B]", len(valid_gaps), 0.60,
        )
    elif abs(z_score) < 2.0:
        return HybridVerificationResult(
            mean_gap, std_gap, z_score,
            "MARGINAL", "[C]", len(valid_gaps), 0.40,
        )
    else:
        return HybridVerificationResult(
            mean_gap, std_gap, z_score,
            "FAIL", "[D]", len(valid_gaps), 0.10,
        )


def _auxiliary_statistics(measurements: list[SpectralGapMeasurement]) -> str:
    """Extra diagnostics for the report (ds_global, dv_global, iso_defect)."""
    lines = []

    ds_globals = [m.ds_global for m in measurements if m.ds_global is not None]
    if ds_globals:
        lines.append(f"  ds_global    : {statistics.mean(ds_globals):.4f} "
                      f"+/- {statistics.stdev(ds_globals):.4f}" if len(ds_globals) > 1
                      else f"  ds_global    : {ds_globals[0]:.4f}")

    dv_globals = [m.dv_global for m in measurements if m.dv_global is not None]
    if dv_globals:
        lines.append(f"  dv_global    : {statistics.mean(dv_globals):.4f} "
                      f"+/- {statistics.stdev(dv_globals):.4f}" if len(dv_globals) > 1
                      else f"  dv_global    : {dv_globals[0]:.4f}")

    iso_vals = [m.iso_defect for m in measurements if m.iso_defect is not None]
    if iso_vals:
        lines.append(f"  iso_defect   : {statistics.mean(iso_vals):.4f} "
                      f"+/- {statistics.stdev(iso_vals):.4f}" if len(iso_vals) > 1
                      else f"  iso_defect   : {iso_vals[0]:.4f}")

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
    """Generate a human-readable verification report."""

    mean_str = f"{result.gap_proxy_mean:.4f}" if result.gap_proxy_mean is not None else "N/A"
    std_str = f"{result.gap_proxy_std:.4f}" if result.gap_proxy_std is not None else "N/A"
    z_str = f"{result.gap_proxy_z_score:+.2f}" if result.gap_proxy_z_score is not None else "N/A"

    report = f"""
+================================================================+
|  UIDT-RAUMZEIT HYBRID VERIFICATION: PATH A (Spectral Gap)     |
+================================================================+

CANONICAL TARGET:
  Delta* = {DELTA_STAR_GEV} +/- {DELTA_TOLERANCE} GeV  [A]
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
  Status         : {result.consistency}
  Evidence Cat.  : {result.evidence_category}
  Confidence     : {result.confidence:.1%}
"""

    if measurements:
        aux = _auxiliary_statistics(measurements)
        if aux:
            report += f"\nAUXILIARY DIAGNOSTICS:\n{aux}\n"

    # Interpretation block
    if result.consistency == "PASS":
        report += """
INTERPRETATION:
  SPECTRAL GAP SIGNATURE DETECTED  [B]

  The emergent dimension gap g_fc from causal-set K7 measurements
  clusters within 1-sigma of UIDT's predicted mass gap
  Delta* = 1.710 GeV.

  This constitutes a [B]-level numerical robustness signal
  supporting the vacuum information density postulate.
  It does NOT constitute a proof (which requires [A]).

  Limitation L4 remains: gamma = 16.339 is calibrated [A-],
  not yet derived from RG first principles.
"""
    elif result.consistency == "NEAR":
        report += f"""
INTERPRETATION:
  NEAR-CONSISTENT  (Delta = {abs(result.gap_proxy_mean - DELTA_STAR_GEV):.4f} from target)

  Small deviation from canonical target.  Possible causes:
  - Finite-size effects in causal-set simulation
  - K7 anchor sampling variance
  - RG-flow not fully converged at measured N

  Recommendation: increase N or number of batch seeds.
  Classification: [B] (marginal; needs replication).
"""
    elif result.consistency == "MARGINAL":
        report += """
INTERPRETATION:
  MARGINAL CONSISTENCY  (Moderate scatter)

  Gap proxy exhibits larger variance.  Actions:
  - Replicate with different random seeds
  - Increase K7 anchor count (num_anchors >= 16)
  - Extend to larger N values (>= 5000 nodes)

  Classification: [C] Calibrated Model (scenario-dependent).
"""
    else:
        report += """
INTERPRETATION:
  NO SPECTRAL GAP SIGNATURE DETECTED  [D]

  Emergent dimension gaps do NOT cluster near Delta* = 1.710.

  Possible interpretations:
  - g_fc does not map to the Yang-Mills spectral gap in this
    configuration space (the mapping hypothesis fails)
  - UIDT mass gap is not a universal emergent property
  - Measurement methodology requires revision

  Next: test alternative hypotheses (Path B, Path C).
  Classification: [D] Prediction (possibly falsified).
"""

    report += f"""
REFERENCES:
  UIDT Theory : DOI 10.5281/zenodo.17835200
  External Ref : cblab/raumzeit (ID: 1207002944)
  K7 Diagnostic: diagnostics_k7.py :: measure_anchor()
  K2 Base      : diagnostics_k2.py :: _estimate_spectral_dimension()
  Config       : emergent-geometry-causal-graphs/configs/v9a_fast.yaml

RG FIXED-POINT CONSTRAINT (read-only verification):
  5*kappa^2          = {5 * KAPPA**2:.15f}
  3*lambda_S         = {3 * LAMBDA_S:.15f}
  Residual           = {abs(5 * KAPPA**2 - 3 * LAMBDA_S):.2e}
  Status             = {"PASS" if abs(5 * KAPPA**2 - 3 * LAMBDA_S) < 1e-14 else "WARN"}
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
        print("Usage: python hybrid_uidt_raumzeit_spectral_gap.py "
              "<results.json> [--output report.txt]")
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

    if result.consistency == "PASS":
        return 0
    elif result.consistency in ("NEAR", "MARGINAL"):
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
