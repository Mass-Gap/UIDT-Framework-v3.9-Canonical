"""
UIDT High-Precision MCMC Sampler v1.0
=====================================
Author: Philipp Rietz (ORCID: 0009-0007-4307-1609)
DOI: 10.5281/zenodo.17835200
License: CC BY 4.0

This script performs high-precision Monte Carlo lattice generation for 
canonical UIDT parameters [A/A-] using Parallel Tempering MCMC.
Precision is strictly enforced at 80-digit (mpmath).

Evidence Categories:
- Delta* [A]
- kappa [A]
- gamma [A-] (calibrated)
- lambda_S [A] (RG Fixed-Point: 5*kappa^2 = 3*lambda_S)
- v [A]

Usage:
    python verification/scripts/uidt_mcmc_sampler.py
"""

from mpmath import mp, mpf, exp, log, sqrt, cos, pi, nstr, power
import secrets
import json
import os

# Set 80-digit precision on the context
mp.dps = 80

class ArbitraryPrecisionPRNG:
    """High-entropy PRNG for 80-digit precision MCMC."""
    def __init__(self):
        self.two = mpf('2')
        self.two_256 = power(self.two, 256)

    def rand(self):
        """Generates a random mpf in [0, 1)."""
        bits = secrets.randbits(256)
        return mpf(bits) / self.two_256

    def uniform(self, a, b):
        return a + (b - a) * self.rand()

    def normal(self, mu, sigma):
        """Box-Muller transform for normal distribution."""
        u1 = self.rand()
        u2 = self.rand()
        while u1 == 0:
            u1 = self.rand()
        z0 = sqrt(-self.two * log(u1)) * cos(self.two * pi * u2)
        return mu + z0 * sigma

class UIDT_Hamiltonian:
    """Defines the energy action for the UIDT parameter space."""
    def __init__(self):
        # Canonical values [A/A-]
        self.DELTA_TARGET = mpf('1.710')
        self.DELTA_SIGMA = mpf('0.015')
        self.KAPPA_TARGET = mpf('0.500')
        self.KAPPA_SIGMA = mpf('0.008')
        self.GAMMA_CALIBRATED = mpf('16.339')
        self.V_TARGET = mpf('0.0477')
        
        self.ONE = mpf('1')
        self.TWO = mpf('2')
        self.THREE = mpf('3')
        self.FIVE = mpf('5')
        self.TOL_RG = mpf('1e-15')

    def action(self, params):
        """Negative log-likelihood of the parameters."""
        delta, gamma, kappa, lambda_s, v = params
        
        # 1. RG Fixed Point Constraint: 5*kappa^2 = 3*lambda_s [A]
        rg_residual = abs(self.FIVE * kappa**self.TWO - self.THREE * lambda_s)
        rg_penalty = (rg_residual / self.TOL_RG)**self.TWO

        # 2. Likelihoods
        delta_chi2 = ((delta - self.DELTA_TARGET) / self.DELTA_SIGMA)**self.TWO
        kappa_chi2 = ((kappa - self.KAPPA_TARGET) / self.KAPPA_SIGMA)**self.TWO
        gamma_chi2 = ((gamma - self.GAMMA_CALIBRATED) / mpf('0.001'))**self.TWO
        v_chi2 = ((v - self.V_TARGET) / mpf('0.0001'))**self.TWO

        return delta_chi2 + kappa_chi2 + gamma_chi2 + v_chi2 + rg_penalty

class ParallelTemperingMCMC:
    def __init__(self, hamiltonian, num_chains=4):
        self.h = hamiltonian
        self.prng = ArbitraryPrecisionPRNG()
        self.num_chains = num_chains
        base = mpf('1.5')
        self.temps = [base**i for i in range(num_chains)]
        
        self.states = []
        for _ in range(num_chains):
            state = [
                self.h.DELTA_TARGET,
                self.h.GAMMA_CALIBRATED,
                self.h.KAPPA_TARGET,
                self.h.FIVE * self.h.KAPPA_TARGET**self.h.TWO / self.h.THREE,
                self.h.V_TARGET
            ]
            self.states.append(state)
        
        self.energies = [self.h.action(s) for s in self.states]
        self.step_sizes = [mpf('0.01') for _ in range(num_chains)]
        self.acceptance_counts = [0 for _ in range(num_chains)]
        self.swap_attempts = 0
        self.swap_successes = 0
        self.iteration = 0

    def step(self):
        self.iteration += 1
        for i in range(self.num_chains):
            current_state = self.states[i]
            current_energy = self.energies[i]
            proposal = [p + self.prng.normal(mpf('0'), self.step_sizes[i]) for p in current_state]
            proposal[3] = self.h.FIVE * proposal[2]**self.h.TWO / self.h.THREE
            proposal_energy = self.h.action(proposal)
            delta_e = (proposal_energy - current_energy) / self.temps[i]
            if delta_e <= 0 or self.prng.rand() < exp(-delta_e):
                self.states[i] = proposal
                self.energies[i] = proposal_energy
                self.acceptance_counts[i] += 1

        if self.iteration % 10 == 0:
            self.swap_attempts += 1
            idx = secrets.randbelow(self.num_chains - 1)
            i, j = idx, idx + 1
            beta_i = self.h.ONE / self.temps[i]
            beta_j = self.h.ONE / self.temps[j]
            prob = exp((self.energies[idx] - self.energies[idx+1]) * (beta_i - beta_j))
            if self.prng.rand() < prob:
                self.states[i], self.states[j] = self.states[j], self.states[i]
                self.energies[i], self.energies[j] = self.energies[j], self.energies[i]
                self.swap_successes += 1

    def save_checkpoint(self, path):
        data = {
            'iteration': self.iteration,
            'states': [[nstr(p, 80) for p in s] for s in self.states],
            'energies': [nstr(e, 80) for e in self.energies],
            'step_sizes': [nstr(s, 80) for s in self.step_sizes],
            'acceptance_counts': self.acceptance_counts,
            'swap_attempts': self.swap_attempts,
            'swap_successes': self.swap_successes
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f)

    def load_checkpoint(self, path):
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            data = json.load(f)
        self.iteration = data['iteration']
        self.states = [[mpf(p) for p in s] for s in data['states']]
        self.energies = [mpf(e) for e in data['energies']]
        self.step_sizes = [mpf(s) for s in data['step_sizes']]
        self.acceptance_counts = data['acceptance_counts']
        self.swap_attempts = data['swap_attempts']
        self.swap_successes = data['swap_successes']

def run_batch(batch_size=1000, sample_interval=10):
    checkpoint_path = 'verification/data/mcmc_state.json'
    output_dir = 'verification/data/mcmc_batches/'
    
    h = UIDT_Hamiltonian()
    mcmc = ParallelTemperingMCMC(h)
    mcmc.load_checkpoint(checkpoint_path)
    
    samples = []
    for i in range(batch_size):
        mcmc.step()
        if i % sample_interval == 0:
            s = mcmc.states[0]
            e = mcmc.energies[0]
            samples.append([nstr(p, 80) for p in s] + [nstr(e, 80)])
    
    mcmc.save_checkpoint(checkpoint_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'batch_{mcmc.iteration}.csv'), 'w') as f:
        f.write("delta,gamma,kappa,lambda_s,v,energy\n")
        for row in samples:
            f.write(",".join(row) + "\n")

    return {
        'status': 'completed',
        'iterations': mcmc.iteration,
        'swap_rate': float(mcmc.swap_successes / mcmc.swap_attempts) if mcmc.swap_attempts > 0 else 0
    }

if __name__ == "__main__":
    result = run_batch()
    print(json.dumps(result))
