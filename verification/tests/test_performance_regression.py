import time
import sys

# ALWAYS local mpmath import and dps setup for UIDT tests
from mpmath import mp
mp.dps = 80

def test_banach_convergence():
    """
    Dummy Banach contraction test to measure performance regression.
    Simulates a root-finding/fixed-point iteration.
    """
    print("Starting Banach Convergence Test...")
    start_time = time.time()

    # Simple fixed-point iteration using high precision
    # e.g., finding sqrt(2) via x_{n+1} = 0.5 * (x_n + 2/x_n)
    x = mp.mpf('1.0')
    target = mp.mpf('2.0')

    # We do a large number of iterations to simulate workload
    for _ in range(5000):
        x = mp.mpf('0.5') * (x + target / x)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Convergence achieved in {duration:.4f} seconds.")

    # Residual check
    residual = abs(x*x - target)
    print(f"Residual: {residual}")

    if residual >= mp.mpf('1e-14'):
        print("ERROR: Residual exceeds threshold.")
        sys.exit(1)

    # Elite Tier Performance Check: must be < 2.5s
    if duration > 2.5:
        print(f"ERROR: Performance regression detected! Execution time {duration:.4f}s exceeds 2.5s limit.")
        sys.exit(1)

    print("Elite Tier Performance Check Passed.")

if __name__ == "__main__":
    test_banach_convergence()
