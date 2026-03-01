import os
import re


def _read(repo_root: str, rel_path: str) -> str:
    path = os.path.join(repo_root, *rel_path.split("/"))
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_hmc_scripts_have_seed_argument():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    hmc_361 = _read(repo_root, "simulation/UIDTv3_6_1_HMC_Real.py")
    hmc_372 = _read(repo_root, "clay-submission/05_LatticeSimulation/UIDTv3_7_2_HMC_Real.py")

    for content in (hmc_361, hmc_372):
        assert "--seed" in content
        assert re.search(r"np\.random\.seed\(", content) is not None


def test_su3_taylor_orders_are_at_least_40():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    hmc_372 = _read(repo_root, "clay-submission/05_LatticeSimulation/UIDTv3_7_2_HMC_Real.py")
    val_361 = _read(repo_root, "simulation/UIDTv3.6.1_Lattice_Validation.py")

    assert re.search(r"order\s*=\s*40", hmc_372) is not None
    assert re.search(r"order\s*=\s*40", val_361) is not None

