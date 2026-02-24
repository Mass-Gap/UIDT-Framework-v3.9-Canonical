import sys

class JulesUIDTTools:
    def mpmath_tool(self, eq_str, expected, tol):
        import mpmath
        mpmath.mp.dps = 80
        try:
            # Evaluate the expression using python's eval
            # This handles "2+2" -> 4
            # We wrap in mpmathify to ensure it's treated as mpf for comparison
            val = eval(eq_str)
            result = mpmath.mpmathify(val)
            expected_mp = mpmath.mpmathify(expected)

            diff = abs(result - expected_mp)
            if diff < tol:
                print(f"VERIFIED: {eq_str} = {result} (expected {expected_mp})")
                return True
            else:
                print(f"FAILED: {eq_str} = {result} (expected {expected_mp}), diff {diff} >= {tol}")
                return False
        except Exception as e:
            print(f"ERROR: Could not evaluate '{eq_str}': {e}")
            return False

    def commit_tool(self, summary, type, ev_cat):
        msg = f"[UIDT-v3.9] {type}: {summary} (Evidence: {ev_cat})"
        print(f"COMMIT MSG: {msg}")
        return msg

    def supabase_tool(self, table):
        print(f"SUPABASE QUERY: SELECT * FROM {table}")
        return True

    def falsification_tool(self, param, val):
        print(f"FALSIFICATION CHECK: {param} = {val}")
        return True
