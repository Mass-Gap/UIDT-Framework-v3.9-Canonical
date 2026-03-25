# verification/scripts/verify_rt_geodesics_gamma.py
#
# Verification script: RT-geodesic gamma_eff scan vs. bare gamma
# UIDT Framework v3.9
#
# Runs a deterministic scan over RT-geodesic configurations,
# computes gamma_eff^RT per configuration, and compares against
# canonical ledger values:
#   gamma     = 16.339   [A-]  (dressed, phenomenological)
#   gamma_inf = 16.3437  [B]   (bare, FSS extrapolation)
#   delta_gamma = 0.0047 [B/D] (vacuum dressing shift)
#
# Output: verification/data/rt_geodesics_gamma.csv
#
# Usage:
#   python verification/scripts/verify_rt_geodesics_gamma.py
#
# Author: P. Rietz
# DOI: 10.5281/zenodo.17835200

import csv
from pathlib import Path
from typing import Any, Dict, List, Tuple

from modules import rt_geodesics


def _init_mp() -> Any:
    """
    Local mpmath initialization for this verification script.

    Precision is set HERE and ONLY here for this script.
    Do NOT centralize mp.mp.dps into a shared config or global variable.
    (Race-condition lock — UIDT Constitution requirement.)
    """
    import mpmath as mp
    mp.mp.dps = 80
    return mp


def run_rt_geodesic_scan() -> List[Dict[str, Any]]:
    """
    Run the RT-geodesic scan over the default configuration set.

    Returns
    -------
    list of dict, each containing:
        - 'config_id' (str)
        - 'gamma_eff_rt' (mpmath.mpf)
    """
    mp = _init_mp()

    configs = rt_geodesics.generate_default_rt_configs()
    results: List[Dict[str, Any]] = []

    for cfg in configs:
        invariants = rt_geodesics.compute_rt_geodesic_invariants(cfg)
        gamma_eff_rt = rt_geodesics.effective_gamma_from_geodesics(invariants)

        if not isinstance(gamma_eff_rt, mp.mpf):
            gamma_eff_rt = mp.mpf(gamma_eff_rt)

        results.append(
            {
                "config_id": cfg.get("config_id", "UNSPECIFIED"),
                "gamma_eff_rt": gamma_eff_rt,
            }
        )

    return results


def compare_to_bare_gamma(
    scan_results: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Compare RT-derived gamma_eff^RT values against canonical ledger constants.

    Canonical values (read-only, MUST NOT be modified):
        gamma       = 16.339   [A-]
        gamma_inf   = 16.3437  [B]
        delta_gamma = 0.0047   [B/D]

    Parameters
    ----------
    scan_results : list of dict
        Output of run_rt_geodesic_scan().

    Returns
    -------
    per_config : list of dict
        Per-configuration results including residuals.
    summary : dict
        Aggregate statistics (min/max residuals, reference constants).
    """
    mp = _init_mp()

    # Canonical ledger values — read-only references, never modify.
    gamma_dressed = mp.mpf("16.339")    # [A-]
    gamma_inf = mp.mpf("16.3437")       # [B]
    delta_gamma = mp.mpf("0.0047")      # [B/D]

    per_config: List[Dict[str, Any]] = []
    res_abs_list: List[Any] = []
    res_rel_list: List[Any] = []

    for entry in scan_results:
        ge = entry["gamma_eff_rt"]
        res_abs = mp.fabs(ge - gamma_inf)
        res_rel = res_abs / gamma_inf

        res_abs_list.append(res_abs)
        res_rel_list.append(res_rel)

        per_config.append(
            {
                "config_id": entry["config_id"],
                "gamma_eff_rt": ge,
                "res_abs_vs_gamma_inf": res_abs,
                "res_rel_vs_gamma_inf": res_rel,
            }
        )

    if res_abs_list:
        res_abs_min = min(res_abs_list)
        res_abs_max = max(res_abs_list)
        res_rel_min = min(res_rel_list)
        res_rel_max = max(res_rel_list)
    else:
        res_abs_min = mp.mpf("0.0")
        res_abs_max = mp.mpf("0.0")
        res_rel_min = mp.mpf("0.0")
        res_rel_max = mp.mpf("0.0")

    summary: Dict[str, Any] = {
        "gamma_dressed": gamma_dressed,
        "gamma_inf": gamma_inf,
        "delta_gamma": delta_gamma,
        "res_abs_min": res_abs_min,
        "res_abs_max": res_abs_max,
        "res_rel_min": res_rel_min,
        "res_rel_max": res_rel_max,
    }

    return per_config, summary


def _write_csv(results: List[Dict[str, Any]], csv_path: Path) -> None:
    """
    Write per-configuration RT results to CSV.

    All numerical values are formatted via mpmath.nstr() to avoid
    float() casts and potential TypeErrors with mp.mpf objects.
    (UIDT Constitution: no intentional crashes, no float() for core numerics.)
    """
    mp = _init_mp()

    fieldnames = [
        "config_id",
        "gamma_eff_rt",
        "res_abs_vs_gamma_inf",
        "res_rel_vs_gamma_inf",
    ]

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    "config_id": row["config_id"],
                    "gamma_eff_rt": mp.nstr(row["gamma_eff_rt"], 30),
                    "res_abs_vs_gamma_inf": mp.nstr(
                        row["res_abs_vs_gamma_inf"], 30
                    ),
                    "res_rel_vs_gamma_inf": mp.nstr(
                        row["res_rel_vs_gamma_inf"], 30
                    ),
                }
            )


def main() -> None:
    """
    Entry point for the RT-geodesic gamma_eff verification pipeline.

    Usage
    -----
    python verification/scripts/verify_rt_geodesics_gamma.py
    """
    mp = _init_mp()

    print("[UIDT-v3.9] RT-geodesic gamma_eff scan starting...")

    scan_results = run_rt_geodesic_scan()
    per_config, summary = compare_to_bare_gamma(scan_results)

    output_path = Path("verification") / "data" / "rt_geodesics_gamma.csv"
    _write_csv(per_config, output_path)

    print(f"Output CSV : {output_path}")
    print(
        f"gamma (dressed) [A-] : {mp.nstr(summary['gamma_dressed'], 10)}"
    )
    print(
        f"gamma_inf       [B]  : {mp.nstr(summary['gamma_inf'], 10)}"
    )
    print(
        f"delta_gamma     [B/D]: {mp.nstr(summary['delta_gamma'], 6)}"
    )
    print(
        f"Residual |gamma_eff^RT - gamma_inf| / gamma_inf "
        f"in [{mp.nstr(summary['res_rel_min'], 6)}, "
        f"{mp.nstr(summary['res_rel_max'], 6)}]"
    )
    print(
        "Evidence cap: RT-derived quantities <= [B]/[D], Stratum III."
    )


if __name__ == "__main__":
    main()
