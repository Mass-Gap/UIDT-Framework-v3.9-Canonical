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
            <span className="label">{claim.id} — {claim.title}</span>
            <div className="value">{claim.value} {claim.unit}</div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              {claim.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClaimsLedger;
