import json

with open('LEDGER/CLAIMS.json', 'r') as f:
    data = json.load(f)

for claim in data['claims']:
    if claim['id'] == 'UIDT-C-044':
        print("OLD NOTES:")
        print(claim['notes'])

        # update the notes
        claim['notes'] = "E_T = f_vac − Δ/γ = 107.10 − 104.66 MeV. [Tension Alert]: Shows 4.0σ tension with PDG 2025 m_u=2.16±0.07 MeV. [Epistemological Correction]: Direct numerical comparison is methodologically incomplete (Stratum violation). The UIDT torsion energy (E_T) requires formal renormalization (matching from 'Bare Lattice-Schema' into the MS-bar scheme) before the deviation significance acts as a true falsification criterion. CONSTANTS.md v3.9.5 authoritative."
        print("\nNEW NOTES:")
        print(claim['notes'])
        break

with open('LEDGER/CLAIMS.json', 'w') as f:
    json.dump(data, f, indent=2)
