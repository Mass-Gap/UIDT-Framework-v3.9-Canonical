from mpmath import mp


# Global precision setting for UIDT verification (Canonical)
PRECISION = 80


def setup_precision():
    """
    Sets the global precision for mpmath to the required standard.
    This ensures numerical stability for the Banach Fixed-Point Iteration.
    """
    mp.dps = PRECISION
