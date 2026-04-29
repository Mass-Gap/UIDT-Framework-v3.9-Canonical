import json
from pathlib import Path

class LedgerSync:
    def __init__(self, ledger_path="LEDGER/CLAIMS.json", canonical_path="CANONICAL/CONSTANTS.md"):
        self.ledger_path = Path(ledger_path)
        self.canonical_path = Path(canonical_path)

    def get_canonical_constants(self):
        """Reads constants from CANONICAL/CONSTANTS.md"""
        constants = {}
        if not self.canonical_path.exists():
            return constants

        with open(self.canonical_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Basic parsing, e.g., "Δ* = 1.710 ± 0.015 GeV [A]"
                if '=' in line and '[' in line and ']' in line:
                    parts = line.split('=')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        value_part = parts[1].split('[')[0].strip()
                        constants[name] = value_part
        return constants

    def get_ledger_claims(self):
        """Reads claims from LEDGER/CLAIMS.json"""
        claims = []
        if not self.ledger_path.exists():
            return claims

        with open(self.ledger_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                claims = data.get('claims', [])
            except json.JSONDecodeError:
                pass
        return claims

    def generate_injection_payload(self):
        """Generates a payload that can be injected into metadata headers."""
        constants = self.get_canonical_constants()
        claims = self.get_ledger_claims()

        payload = {
            "version": "v3.9",
            "constants": constants,
            "claims_count": len(claims),
            "source": "SSoT Sync"
        }
        return payload

def main():
    print("Running Global SSoT Sync...")
    syncer = LedgerSync()
    payload = syncer.generate_injection_payload()
    print(f"Generated Payload: {json.dumps(payload, indent=2)}")
    print("SSoT Sync complete. Ready for metadata injection.")

if __name__ == "__main__":
    main()
