import mpmath as mp
import csv
import random

# [RESEARCH-MODE]
# Local precision enforcing
mp.mp.dps = 80

def load_data():
    file_path = 'clay-submission/03_AuditData/3.2/UIDT_MonteCarlo_samples_100k.csv'
    gamma_values = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        gamma_idx = header.index('gamma')
        for row in reader:
            gamma_values.append(mp.mpf(row[gamma_idx]))
    return gamma_values

def calc_mean(data):
    return sum(data) / len(data)

def calc_variance(data, mean):
    return sum((x - mean)**2 for x in data) / (len(data) - 1)

def calc_std(data, mean):
    return mp.sqrt(calc_variance(data, mean))

def jackknife(data):
    n = len(data)
    total_sum = sum(data)

    jk_means = []
    for x_i in data:
        mean_i = (total_sum - x_i) / (n - 1)
        jk_means.append(mean_i)

    mean_of_jk_means = sum(jk_means) / n
    jk_variance = (mp.mpf(n - 1) / n) * sum((m - mean_of_jk_means)**2 for m in jk_means)
    return mp.sqrt(jk_variance)

def bootstrap(data, n_boot=1000):
    n = len(data)
    boot_means = []

    for i in range(n_boot):
        sample = random.choices(data, k=n)
        mean = sum(sample) / n
        boot_means.append(mean)

    mean_of_boot_means = sum(boot_means) / n_boot
    boot_variance = sum((m - mean_of_boot_means)**2 for m in boot_means) / (n_boot - 1)
    return mp.sqrt(boot_variance)

if __name__ == "__main__":
    import sys

    print("Loading original 100k MC-samples...")
    sys.stdout.flush()
    data = load_data()
    n = len(data)

    mean = calc_mean(data)
    std = calc_std(data, mean)
    sem_analytical = std / mp.sqrt(n)

    print(f"Sample Mean: {mean}")
    print(f"Sample Std Deviation (sigma): {std}")
    print(f"Analytical SEM: {sem_analytical}")
    sys.stdout.flush()

    print("\nRunning Jackknife Resampling...")
    sys.stdout.flush()
    jk_err = jackknife(data)
    print(f"Jackknife SEM: {jk_err}")
    sys.stdout.flush()

    print("\nRunning Bootstrap Resampling (N_boot=1000)...")
    sys.stdout.flush()
    boot_err = bootstrap(data, 1000)
    print(f"Bootstrap SEM: {boot_err}")
    sys.stdout.flush()

    print("\nComparison:")
    print(f"Documented value in LEDGER [A-]: 1.005")
    print(f"Difference (Std - 1.005): {std - mp.mpf('1.005')}")
    print(f"Difference (Jackknife - 1.005): {jk_err - mp.mpf('1.005')}")
    print(f"Difference (Bootstrap - 1.005): {boot_err - mp.mpf('1.005')}")
    sys.stdout.flush()
