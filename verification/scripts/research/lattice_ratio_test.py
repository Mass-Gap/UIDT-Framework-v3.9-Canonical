"""
Lattice Ratio Test (TKT-016)
"""
import mpmath as mp
mp.dps = 80

def check_ratio():
    delta = mp.mpf('1.710')
    lambda_qcd = mp.mpf('0.244')
    
    ratio = delta / lambda_qcd
    print(f"Ratio: {ratio}")
    
    if abs(ratio - 16.339) > 1:
        print("Hypothesis FALSIFIED.")

if __name__ == "__main__":
    check_ratio()
