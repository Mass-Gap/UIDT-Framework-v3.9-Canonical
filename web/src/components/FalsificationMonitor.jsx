import React from 'react';

const FalsificationMonitor = () => {
  const metrics = [
    {
      id: 'mass-gap',
      name: 'Mass-Gap (Δ*) vs Lattice QCD',
      value: '0.37σ',
      threshold: '> 3.0σ',
      status: 'SAFE',
      description: 'UIDT predicts 1.710 GeV. Current lattice mean is ~1.715 GeV.',
      color: 'var(--success)',
      evidence: '[A]'
    },
    {
      id: 'universal-scaling',
      name: 'Universal Scaling (γ) Tension',
      value: '4.20σ',
      threshold: '> 5.0σ',
      status: 'TENSION',
      description: 'Hubble tension calibration requires γ = 16.339. RG flow derives ~16.31.',
      color: 'var(--warning)',
      evidence: '[C]'
    },
    {
      id: 'scalar-exclusion',
      name: 'LHC Scalar Exclusion Bounds',
      value: 'Pending',
      threshold: 'M_S excluded at 1.7 GeV',
      status: 'AWAITING DATA',
      description: 'If ATLAS/CMS exclude a scalar at 1.7 GeV with 5σ, UIDT is strictly falsified.',
      color: 'var(--text-secondary)',
      evidence: '[D]'
    }
  ];

  return (
    <div className="falsification-dashboard" style={{ marginTop: '2rem', padding: '1.5rem', border: '1px solid var(--border-color)', borderRadius: '8px', background: 'rgba(0,0,0,0.2)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.25rem', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ color: 'var(--danger)' }}>⚠️</span> Epistemic Falsification Bounds
        </h2>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Strict Honesty Protocol</span>
      </div>
      
      <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', marginBottom: '1.5rem', lineHeight: 1.5 }}>
        A theory is only scientific if it is falsifiable. Below are the strict thresholds that, if breached, mathematically or empirically invalidate the UIDT framework.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
        {metrics.map(m => (
          <div key={m.id} style={{ padding: '1rem', border: `1px solid ${m.color}`, borderRadius: '4px', background: 'rgba(0,0,0,0.4)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span style={{ fontWeight: 600, fontSize: '0.9rem', color: m.color }}>{m.status}</span>
              <span className={`pill pill-${m.evidence.toLowerCase()[1]}`}>{m.evidence}</span>
            </div>
            <h3 style={{ fontSize: '1rem', margin: '0 0 0.5rem 0' }}>{m.name}</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>
              <span>Current: <strong>{m.value}</strong></span>
              <span>Falsifies at: <strong>{m.threshold}</strong></span>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0 }}>{m.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FalsificationMonitor;
