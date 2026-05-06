import React, { useState, useEffect } from 'react';
import { verifyIntegrity, verifyProvenance } from '../utils/desci_bridge';

const ClaimsLedger = () => {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadClaims = async () => {
      try {
        const response = await fetch('/UIDT-Framework-v3.9-Canonical/data/claims.json');
        const data = await response.json();
        
        // Dynamic verification of provenance for each claim
        const verifiedClaims = await Promise.all(data.claims.map(async (claim) => {
          const isSigned = await verifyProvenance('sig-placeholder', claim);
          return { ...claim, verified: isSigned };
        }));

        setClaims(verifiedClaims);
        setLoading(false);
      } catch (err) {
        console.error('Failed to load ledger:', err);
        setLoading(false);
      }
    };
    loadClaims();
  }, []);

  if (loading) return <div className="label">Loading Canonical Ledger...</div>;

  return (
    <div className="claims-explorer">
      <h2>Canonical Claims Explorer (DeSci Layer)</h2>
      <div className="data-grid">
        {claims.map((claim) => (
          <div key={claim.id} className="data-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <span className={`pill pill-${claim.evidence.toLowerCase()[0]}`}>
                {claim.evidence}
              </span>
              {claim.verified && <span className="verified-badge">Provenance Verified</span>}
            </div>
            <span className="label">{claim.id} — {claim.type.toUpperCase()}</span>
            <div className="value" style={{ fontSize: '1.1rem', fontWeight: '500' }}>{claim.statement}</div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              {claim.notes || 'No supplemental notes available for this canonical record.'}
            </p>
            <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', opacity: 0.6 }}>
              Status: <span style={{ color: claim.status === 'verified' ? 'var(--smaragd)' : 'inherit' }}>{claim.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClaimsLedger;
