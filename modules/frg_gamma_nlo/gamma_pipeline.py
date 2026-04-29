"""
[UIDT-v3.9] FRG/NLO — Full Pipeline: lambda_3(UV) -> Z_phi(IR) -> gamma
========================================================================

This module chains Steps 1-4 into a single reproducible pipeline:

  Step 1: Lagrangian RG constraint verification
  Step 2: UV coupling derivation (phi* -> lambda_3)
  Step 3: FRG flow Z_phi(k), UV -> IR
  Step 4: Compare Z_phi(IR) with gamma = 16.339

EPISTEMIC STATUS:
  [A]  Steps 1-2 (Lagrangian, regulators, threshold functions)
  [D]  Step 3-4 (flow result, gamma identification)
  Evidence never auto-upgraded in this pipeline.

RUN:
  python -m modules.frg_gamma_nlo.gamma_pipeline [n_steps]

Exit codes:
  0 = Z_phi(IR) within delta_gamma = 0.0047 of gamma = 16.339
  1 = deviation within 10 * delta_gamma  (marginal)
  2 = deviation > 10 * delta_gamma  (flow not converging)
"""

from __future__ import annotations

import sys
import mpmath as mp

from modules.frg_gamma_nlo.lagrangian import get_ledger, verify_rg_constraint
from modules.frg_gamma_nlo.fixedpoint_potential import derive_uv_couplings, fixedpoint_report
from modules.frg_gamma_nlo.flow_equations import run_frg_flow, flow_report


def _set_precision() -> None:
    mp.dps = 80


def run_gamma_pipeline(n_steps: int = 2000) -> dict:
    """
    Execute the full FRG gamma derivation pipeline.

    Returns:
        dict with keys:
          'rg_status'     : RG constraint pass/fail
          'phi_star'      : dimensionless VEV [D]
          'lambda_3'      : cubic coupling at UV [D]
          'z_ir'          : Z_phi(k->0) [D]
          'gamma_target'  : 16.339 [A-]
          'deviation'     : |Z_phi(IR) - gamma| [D]
          'within_delta'  : bool, deviation < delta_gamma
          'evidence'      : '[D]' always
          'flow_result'   : full dict from run_frg_flow()
          'uv_couplings'  : full dict from derive_uv_couplings()
    """
    _set_precision()

    # Step 1: RG constraint
    residual, rg_status = verify_rg_constraint()
    if rg_status != "PASS":
        raise RuntimeError(f"[RG_CONSTRAINT_FAIL] {rg_status}")

    L = get_ledger()

    # Step 2: UV couplings from fixed-point potential
    uv = derive_uv_couplings()

    # Step 3: FRG flow with lambda_3(UV) != 0
    flow = run_frg_flow(
        n_steps=n_steps,
        lambda_3_uv=uv["lambda_3"],
        lambda_4_uv=uv["lambda_4"],
    )

    # Step 4: Compare
    z_ir = flow["z_ir"]
    gamma_target = L["GAMMA"]
    deviation = abs(z_ir - gamma_target)
    delta_gamma = L["DELTA_GAMMA"]

    return {
        "rg_status":    rg_status,
        "phi_star":     uv["phi_star"],
        "lambda_3":     uv["lambda_3"],
        "z_ir":         z_ir,
        "gamma_target": gamma_target,
        "deviation":    deviation,
        "delta_gamma":  delta_gamma,
        "within_delta": deviation < delta_gamma,
        "evidence":     "[D]",
        "flow_result":  flow,
        "uv_couplings": uv,
    }


def pipeline_report(result: dict) -> str:
    _set_precision()
    lines = [
        "+================================================================+",
        "|  UIDT FRG/NLO GAMMA PIPELINE: Full Derivation Report          |",
        "+================================================================+",
        "",
        "PIPELINE SUMMARY:",
        f"  RG constraint      : {result['rg_status']}",
        f"  phi* (VEV) [D]     : {mp.nstr(result['phi_star'], 10)}",
        f"  lambda_3(UV) [D]   : {mp.nstr(result['lambda_3'], 10)}",
        f"  Z_phi(IR) [D]      : {mp.nstr(result['z_ir'], 20)}",
        f"  gamma_target [A-]  : {mp.nstr(result['gamma_target'], 20)}",
        f"  Deviation          : {mp.nstr(result['deviation'], 6)}",
        f"  delta_gamma [A-]   : {mp.nstr(result['delta_gamma'], 4)}",
        f"  Within tolerance   : {result['within_delta']}",
        f"  Evidence           : {result['evidence']}",
        "",
    ]

    if result["within_delta"]:
        lines += [
            "RESULT: Z_phi(IR) WITHIN delta_gamma OF gamma = 16.339  [D]",
            "  Numerical pipeline consistent with gamma derivation hypothesis.",
            "  To upgrade [D] -> [C]: perform N-step convergence study.",
            "  To upgrade [C] -> [A]: provide analytic proof or rigorous bounds.",
        ]
    else:
        lines += [
            "RESULT: Z_phi(IR) OUTSIDE delta_gamma",
            f"  Deviation = {mp.nstr(result['deviation'], 6)} > delta_gamma = {mp.nstr(result['delta_gamma'], 4)}",
            "  Possible causes:",
            "    - phi* identification (Stratum III) needs refinement",
            "    - NLO truncation insufficient; higher-order terms needed",
            "    - N-step convergence not yet reached (increase n_steps)",
        ]

    lines += [
        "",
        "LIMITATION L4 STATUS:",
        "  gamma = 16.339 remains [A-] until analytic proof closes.",
        "  This pipeline is [D]: numerical evidence, not a proof.",
        "",
        "DOI: 10.5281/zenodo.17835200",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    _set_precision()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    result = run_gamma_pipeline(n_steps=n)
    print(fixedpoint_report(result["uv_couplings"]))
    print()
    print(flow_report(result["flow_result"]))
    print()
    print(pipeline_report(result))
    # Exit codes
    dev = result["deviation"]
    dg = result["delta_gamma"]
    if dev < dg:
        sys.exit(0)
    elif dev < mp.mpf("10") * dg:
        sys.exit(1)
    else:
        sys.exit(2)
