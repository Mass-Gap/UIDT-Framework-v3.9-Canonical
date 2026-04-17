import json

with open('LEDGER/CLAIMS.json', 'r') as f:
    data = json.load(f)

for claim in data['claims']:
    if claim['id'] == 'UIDT-C-049':
        print("OLD UIDT-C-049 NOTES:")
        print(claim['notes'])
        # Also need to update the notes of UIDT-C-049 to refer to 4.0σ PDG 2025 tension instead of 3.75σ FLAG tension.
        claim['notes'] = claim['notes'].replace("3.75σ FLAG tension (pre-QED)", "4.0σ PDG 2025 tension")
        print("\nNEW UIDT-C-049 NOTES:")
        print(claim['notes'])
        break

with open('LEDGER/CLAIMS.json', 'w') as f:
    json.dump(data, f, indent=2)
